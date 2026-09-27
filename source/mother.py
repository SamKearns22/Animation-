"""The mother: a woman of about 35, slim, 1.75 m, long dark hair, in a loose chunky rib-knit roll-neck jumper.

She is built on MakeHuman's measured body with its real skeleton (rig.py). A shot describes her with a
`spec` - where she stands, how she leans, where her head turns and her eyes look, what her hands are doing -
and `solve(spec)` works out the whole pose: her arms are bent (inverse kinematics) so her hands reach what
they hold, her wrists within their natural range. `build(b, state)` then puts her into the scene: the bent
body inside a jumper made for that pose, her MakeHuman head (smiling), her hands (closed round the cleaver,
pressing on the meat), and her hair, combed from the parting and let fall over her shoulders.

Slow pieces are cached on disk (cache.py): the head and hands once; the jumper and hair once per pose.
"""
import functools

import numpy as np

import character as C
import mesh_sdf
import mhuman as MH
import rig
import sdf3d as S
from cache import cached
from materials import SKIN, EYE, HAIR, KNIT, TROUSERS
from rig import unit
from sdf3d import rot, UNION

EYE_X, EYE_R = 0.0305, 0.0168     # MakeHuman's eyeballs (centres 61 mm apart), sized to fit its lids

# ---------------------------------------------------------------------------
# The pieces made once
# ---------------------------------------------------------------------------
_BODY = []


def body():
    if not _BODY:
        _BODY.append(rig.Body(C.SHAPE, C.FACE))
    return _BODY[0]


def mh_deps():
    return [C.base_body, C._grid_of, C._hand_faces, C.head_grid, C.right_hand, C.left_hand, C.FACE, C.SMILE,
            C.SHAPE, C.HANDLE_R, MH.Skeleton, MH.bone_matrix, MH.solve_grip, MH.face_units, MH.blend_units,
            MH.macro_values, MH.apply_macros, mesh_sdf.catmull_clark, mesh_sdf.mesh_to_sdf, mesh_sdf._band]


def head_parts():
    """Her head and neck, smiling, in head coordinates (origin between the eyes, rest axes):
    ((lo, d, voxel), eyes)."""
    return cached('mhhead', C.head_grid, mh_deps(), 0.001)


def hand_parts():
    """(right hand closed round the handle, left hand lying relaxed), see character.py."""
    return cached('mhhands', C.hands, mh_deps())


def eyes_mid_rest():
    """Midway between her eyeballs, in the body's rest frame (metres) - the origin of head coordinates."""
    b = body()
    cs = []
    for side in ('r', 'l'):
        idx = np.unique(np.concatenate([np.array(f) for f in b.groups['helper-%s-eye' % side]]))
        cs.append(b.v_dm[idx].mean(0))
    return b.to_m((cs[0] + cs[1]) / 2)


def surface_points(grid, step=3):
    """Points on a grid shape's surface (in its own frame), thinned out."""
    lo, d, voxel = grid
    idx = np.argwhere(np.abs(d[::step, ::step, ::step]) < 0.6 * voxel * step)
    return lo + idx * voxel * step


# ---------------------------------------------------------------------------
# Solving a pose
# ---------------------------------------------------------------------------
# natural wrist range: bending up/down (flexion) up to 50 degrees, sideways up to 25
BENDS = [(fl, dv) for fl in range(-50, 51, 5) for dv in range(-25, 26, 5)]


def wrist_bend(R, fore, wx, wz, fdir):
    """How the wrist must bend for the hand (turned R) to meet a forearm running towards fdir: returns
    (flexion, deviation, remaining error in degrees) - the least bend that does it."""
    v = R.T @ fdir
    best = None
    for fl, dv in BENDS:
        f = MH.axis_angle(wz, dv) @ MH.axis_angle(wx, fl) @ fore
        err = np.degrees(np.arccos(np.clip(f @ v, -1, 1)))
        cost = err + 0.1 * (abs(fl) + abs(dv))
        if best is None or cost < best[0]:
            best = (cost, fl, dv, err)
    return best[1:]


def place_right(pose, cleaver, pole, roll=None):
    """Her right hand closed round the cleaver's handle, overhand (back of the hand up, fingers curled round
    underneath, as for any chopping blade), turned about the handle so her arm can reach it with the wrist
    least bent. Returns (origin, R, roll)."""
    grid, wr, fore, wx, wz, back = hand_parts()[0]
    u = unit(cleaver.x)
    origin = cleaver.heel - u * 0.038
    k0 = unit(cleaver.R[:, 2] - u * (cleaver.R[:, 2] @ u))
    best = None
    rolls = [roll] if roll is not None else np.arange(0, 360, 4)
    for th_deg in rolls:
        th = np.radians(th_deg)
        k = k0 * np.cos(th) + np.cross(u, k0) * np.sin(th)
        R = np.stack([u, k, np.cross(u, k)], 1)
        w = origin + R @ wr
        e, short = pose.arm_ik('R', w, pole)
        fl, dv, err = wrist_bend(R, fore, wx, wz, unit(e - w))
        up = (R @ back)[1]
        sc = -err / 20 - 0.004 * (abs(fl) + abs(dv)) + 1.5 * (up > 0.75) + 0.5 * up - 30 * short
        if best is None or sc > best[0]:
            best = (sc, R, th_deg)
    return origin, best[1], best[2]


def place_left(pose, ham, along, press, pole):
    """Her left hand pressing down on the meat to hold it steady, fingers lying along it towards the blade
    (where they shouldn't be): turned about the vertical so her arm reaches it comfortably, tilted to sit on
    the curve of the ham, then pressed in `press` metres (the meat is dented round it). Returns (origin, R)."""
    grid, wr, fore, wx, wz = hand_parts()[1]
    palm = ham.c + along * ham.a
    palm[1] = ham.top_at(along)
    slope = along * ham.R[1] / (ham.R[0] ** 2 * np.sqrt(1 - (along / ham.R[0]) ** 2))
    n = unit(np.array([0, 1.0, 0]) - slope * ham.a)       # the ham's surface under her palm
    best = None
    for th in np.radians(np.arange(0, 360, 3)):
        h = np.array([np.cos(th), 0, np.sin(th)])
        x = unit(h - n * (n @ h))
        R = np.stack([x, n, np.cross(x, n)], 1)
        w = palm + R @ wr
        e, short = pose.arm_ik('L', w, pole)
        fl, dv, err = wrist_bend(R, fore, wx, wz, unit(e - w))
        sc = -err / 20 - 0.004 * (abs(fl) + abs(dv)) + 0.8 * (x @ -ham.a) - 30 * short
        if best is None or sc > best[0]:
            best = (sc, R)
    pts = surface_points(grid)
    R0 = best[1]
    settled = None
    for ax in np.arange(-15, 16, 3):
        for az in np.arange(-15, 16, 3):
            R = MH.axis_angle(R0[:, 0], ax) @ MH.axis_angle(R0[:, 2], az) @ R0
            lift = -ham.distance(palm + pts @ R.T).min() - press
            if settled is None or lift < settled[0]:
                settled = (lift, R)
    lift, R = settled
    origin = palm + n * lift
    for _ in range(6):  # the distance to the ham is approximate: measure again until the press is right
        origin = origin + np.array([0, 1.0, 0]) * (-ham.distance(origin + pts @ R.T).min() - press)
    return origin, R


def solve(spec):
    """Everything about her pose, from a shot's description of it. spec keys:
      position, yaw          where she stands (the middle of her feet on the floor) and which way she faces
      lean                   degrees she leans forward from the hips
      head                   (yaw, pitch, roll) of her head in degrees, relative to her body
      gaze                   direction her eyes look, in head coordinates
      look_at                or: a point she looks at (her head turns head_share of the way, eyes the rest)
      smile                  0..1
      cleaver, grip_roll     the cleaver in her right hand (and, to keep the grip steady through a shot, the
                             turn of the hand about the handle found in its first frame)
      ham, press_along, press   her left hand pressing on the ham
      poles                  points her right and left elbows point towards
    """
    b = body()
    pose = rig.Pose(b, spec['position'], spec.get('yaw', 0.0))
    lean = spec.get('lean', 0.0)
    for bone in ('spine04', 'spine03', 'spine02'):
        pose.rot[bone] = MH.axis_angle([1, 0, 0], lean / 3)
    look = spec.get('look_at')
    if look is not None:
        # the head turns most of the way towards what she looks at; the eyes do the rest
        pose.aim_head(np.eye(3))
        M0 = pose.matrices()
        d = pose.world_R().T @ unit(np.asarray(look) - pose.point(M0, 'head', eyes_mid_rest()))
        share = spec.get('head_share', 0.75)
        yaw, pitch = np.degrees(np.arctan2(d[0], d[2])), np.degrees(np.arcsin(-d[1]))
        roll = spec.get('head', (0, 0, 0))[2]
        pose.aim_head(rot(yaw * share, pitch * share, roll))
    else:
        pose.aim_head(rot(*spec.get('head', (0, 0, 0))))
    hands = []
    o, R, roll = place_right(pose, spec['cleaver'], spec['poles'][0], spec.get('grip_roll'))
    hp = hand_parts()
    w_r = o + R @ hp[0][1]
    ol, Rl = place_left(pose, spec['ham'], spec['press_along'], spec['press'], spec['poles'][1])
    w_l = ol + Rl @ hp[1][1]
    e_r, short_r = pose.arm_ik('R', w_r, spec['poles'][0])
    e_l, short_l = pose.arm_ik('L', w_l, spec['poles'][1])
    M = pose.matrices()
    J = {}
    for s in ('R', 'L'):
        J['shoulder.' + s] = pose.joint_world(M, 'upperarm01.' + s)
        J['elbow.' + s] = pose.joint_world(M, 'lowerarm01.' + s)
        J['wrist.' + s] = pose.joint_world(M, 'wrist.' + s)
    for bn in ('neck01', 'neck02', 'neck03', 'head', 'spine02', 'spine04', 'spine05'):
        J[bn] = pose.joint_world(M, bn)
    bends = []
    for (oo, RR), part, s in (((o, R), hp[0], 'R'), ((ol, Rl), hp[1], 'L')):
        w = oo + RR @ part[1]
        bends.append(wrist_bend(RR, part[2], part[3], part[4], unit(J['elbow.' + s] - w)))
        hands.append((oo, RR, w))
    mid = eyes_mid_rest()
    Hc = pose.point(M, 'head', mid)
    Rh = M['head'][:3, :3]
    if look is not None:
        spec = dict(spec, gaze=tuple(Rh.T @ unit(np.asarray(look) - Hc)))
    return dict(spec=spec, pose=pose, M=M, joints=J, hands=hands, bends=bends, grip_roll=roll,
                short=(short_r, short_l), head=(Hc, Rh), smile=spec.get('smile', 1.0))


def pose_key(state):
    """Numbers that fully describe the bent body (for caching the jumper and hair made for it)."""
    p = state['pose']
    return (np.round(p.position, 5).tolist(), round(p.yaw, 4),
            sorted((k, np.round(v, 5).tolist()) for k, v in p.rot.items()))


# ---------------------------------------------------------------------------
# The jumper and trousers, made over the bent body
# ---------------------------------------------------------------------------
JUMPER = dict(thick=0.012, drape=0.35, bridge=0.03, smooth=0.015, hem=0.085, cuff=0.014, voxel=0.0025,
              rolls=((0.004, 0.080, 0.021), (0.030, 0.075, 0.019), (0.051, 0.067, 0.016)))
TORSO_PIECES = {'hips', 'chest', 'head', 'thigh.L', 'thigh.R'}


def jumper_grid(state):
    J = state['joints']
    b = body()
    Vw = b.skin(state['pose'])
    vox = JUMPER['voxel']
    hem = J['spine05'][1] - JUMPER['hem']
    names = TORSO_PIECES | {'upperarm.R', 'forearm.R', 'upperarm.L', 'forearm.L'}
    sel = np.isin(b.label, [b.piece_names.index(n) for n in names if n in b.piece_names])
    sel[:] &= np.isin(np.arange(len(Vw)), b.skin_idx) & (Vw[:, 1] > hem - 0.02) & (Vw[:, 1] < J['neck02'][1] + 0.04)
    lo = Vw[sel].min(0) - 0.05
    hi = Vw[sel].max(0) + 0.05
    for s in ('R', 'L'):  # the cuffs reach a little past the wrists
        lo = np.minimum(lo, J['wrist.' + s] - 0.06)
        hi = np.maximum(hi, J['wrist.' + s] + 0.06)
    n = np.round((hi - lo) / vox).astype(int) + 1
    d = b.surface(Vw, lo, lo + (n - 1) * vox, vox)
    part = b.part_map(Vw, lo, d.shape, vox, [TORSO_PIECES, {'upperarm.R', 'forearm.R'}, {'upperarm.L', 'forearm.L'},
                                                  {'hand.R'}, {'hand.L'}, {'head'}])

    @functools.lru_cache(maxsize=None)
    def region_cached(ids):
        return region(list(ids))

    def region(ids):
        """Smooth signed distance to where the body is made of these parts (negative inside); measured at
        half resolution, which is plenty for cutting cloth."""
        from scipy import ndimage
        m = np.isin(part[::2, ::2, ::2], ids)
        r = (ndimage.distance_transform_edt(~m) - ndimage.distance_transform_edt(m)) * 2 * vox
        return ndimage.zoom(r.astype(np.float32), np.array(part.shape) / np.array(m.shape), order=1)[
            :part.shape[0], :part.shape[1], :part.shape[2]]
    f = d - JUMPER['thick']
    del d
    # the body of the jumper is loose: it bridges hollows (between the breasts, the small of the back) rather
    # than following the skin into them (the shape closed up by a 3 cm ball), hides small bumps (thick knit
    # over a bra: rounded off by a 1.5 cm ball), and hangs straight down from the bust and shoulder blades.
    # The sleeves keep closer to the arm (and don't drape into bat wings).
    # (these broad shapes are worked out at half resolution, then brought back to the full grid)
    from scipy import ndimage
    reg = region_cached((0,))
    torso = np.maximum(f, reg)[::2, ::2, ::2]   # the body of the jumper alone (a smooth cut, no jumps)
    v2 = 2 * vox
    r = JUMPER['bridge']
    torso = rig.robust_distance(rig.robust_distance(torso - r, v2) + r, v2)
    r = JUMPER['smooth']
    torso = rig.robust_distance(rig.robust_distance(torso + r, v2) - r, v2)
    torso = rig.drape(torso, v2, JUMPER['drape'])
    torso = ndimage.zoom(torso, np.array(f.shape) / np.array(torso.shape), order=1)[
        :f.shape[0], :f.shape[1], :f.shape[2]]
    w = np.clip(-reg / 0.02, 0, 1)
    f = w * torso + (1 - w) * np.minimum(f, torso)
    del torso, w
    axes = [lo[q] + np.arange(n[q]) * vox for q in range(3)]

    def window(c, r):
        """The part of the grid within r of c: its slices and coordinates (broadcastable)."""
        i0 = [max(int((c[q] - r - lo[q]) / vox), 0) for q in range(3)]
        i1 = [min(int((c[q] + r - lo[q]) / vox) + 1, n[q]) for q in range(3)]
        sl = tuple(slice(i0[q], i1[q]) for q in range(3))
        return sl, (axes[0][sl[0]][:, None, None], axes[1][sl[1]][None, :, None], axes[2][sl[2]][None, None, :])

    # cuffs: the sleeve ends just past the wrist, over the heel of the hand (cut only where the body is hand)
    for s, hid in (('R', 3), ('L', 4)):
        wr, el = J['wrist.' + s], J['elbow.' + s]
        fd = unit(wr - el)
        c = wr + fd * JUMPER['cuff']
        sl, (X, Y, Z) = window(wr, 0.25)
        beyond = -((X - c[0]) * fd[0] + (Y - c[1]) * fd[1] + (Z - c[2]) * fd[2])
        f[sl] = rig.smax(f[sl], -np.maximum(beyond, region_cached((hid,))[sl] - 0.03), 0.004)
    sl, _ = window(J['head'], 0.25)
    f[sl] = rig.smax(f[sl], -(region_cached((5,))[sl] - 0.02), 0.004)            # nothing on her head
    # the hem, round her hips
    j1 = min(int((hem + 0.02 - lo[1]) / vox) + 1, n[1])
    f[:, :j1] = rig.smax(f[:, :j1], hem - axes[1][:j1][None, :, None], 0.006)
    # the collar: take the jumper off her neck and head, then the soft roll neck, three rolls round the neck
    nb, na = J['neck01'], unit(J['neck03'] - J['neck01'])
    sl, (X, Y, Z) = window(nb, 0.30)
    g = f[sl]
    ax = (X - nb[0]) * na[0] + (Y - nb[1]) * na[1] + (Z - nb[2]) * na[2]
    rad = np.sqrt(np.maximum((X - nb[0]) ** 2 + (Y - nb[1]) ** 2 + (Z - nb[2]) ** 2 - ax ** 2, 0))
    g = rig.smax(g, -np.maximum(-(ax + 0.005), rad - 0.11), 0.006)   # her neck
    for h, R0, r in JUMPER['rolls']:
        g = rig.smin(g, np.sqrt((rad - R0) ** 2 + (ax - h) ** 2) - r, 0.012)
    f[sl] = rig.smax(g, -np.maximum(rad - 0.052, -ax), 0.004)  # the opening the neck comes out of
    f = f.astype(np.float32)
    knit_part = np.array([0, 1, 2, 1, 2, 0], np.float32)[np.maximum(part, 0)]  # hands count as their sleeves
    return lo, f, vox, knit_part


def trousers_grid(state):
    """Dark, slim trousers from the hem of the jumper down (below the worktop, rarely seen)."""
    J = state['joints']
    b = body()
    Vw = b.skin(state['pose'])
    vox = 0.004
    top = J['spine05'][1] - JUMPER['hem'] + 0.04
    sel = np.isin(np.arange(len(Vw)), b.skin_idx) & (Vw[:, 1] < top + 0.02) & (Vw[:, 1] > 0.55)
    sel &= np.isin(b.label, [b.piece_names.index(n) for n in ('hips', 'thigh.L', 'thigh.R', 'shin.L', 'shin.R')])
    lo, hi = Vw[sel].min(0) - 0.03, Vw[sel].max(0) + 0.03
    n = np.round((hi - lo) / vox).astype(int) + 1
    d = b.surface(Vw, lo, lo + (n - 1) * vox, vox) - 0.004
    Y = (lo[1] + np.arange(n[1]) * vox)[None, :, None]
    d = rig.smax(d, Y - top, 0.004)
    return lo, rig.robust_distance(d.astype(np.float32), vox), vox


def get_jumper(state):
    return cached('jumper', jumper_grid_for, [jumper_grid, JUMPER, TORSO_PIECES, rig.Body.skin, rig.Body.surface,
                                              rig.Body.part_map, rig.drape, rig.robust_distance] + mh_deps(),
                  pose_key(state))


def jumper_grid_for(key):
    return jumper_grid(_STATE[0])


def get_trousers(state):
    return cached('trousers', lambda key: trousers_grid(_STATE[0]),
                  [trousers_grid, JUMPER, rig.Body.skin, rig.Body.surface] + mh_deps(), pose_key(state))


_STATE = [None]


# ---------------------------------------------------------------------------
# Hair: long, dark, parted a little to her right, lifted at the crown, falling in soft waves past the
# shoulders - on her right side forward over the shoulder, on her left behind it. Built from locks combed from
# the parting and let fall under gravity over her head, jumper and shoulders.
# ---------------------------------------------------------------------------
SCALP_C, SCALP_R = np.array([0.0, 0.026, -0.064]), np.array([0.0725, 0.0970, 0.0960])
PART = np.radians(-17.0)             # the parting, round from the front of the head
HAIRLINE = (0.066, 0.019, 0.047, 0.057)  # height at the middle, drop to 5 cm out, height and drop at the temple
HAIR_BOX = (np.array([-0.28, -0.52, -0.32]), np.array([0.28, 0.18, 0.26]))  # round the head position


def _push_out_ellipsoid(p, c, r, margin):
    q = (p - c) / (r + margin)
    k = np.linalg.norm(q)
    if k < 1.0:
        return c + (p - c) / max(k, 1e-6)
    return p


def scalp_point(theta, elev, layer=0.0):
    """Point on the scalp (head coordinates): theta round from the front (+ towards her left), elev up from the
    widest line of the head."""
    q = np.array([np.cos(elev) * np.sin(theta), np.sin(elev), np.cos(elev) * np.cos(theta)])
    return SCALP_C + q * (SCALP_R + layer)


def grid_sampler(grid):
    """Distance and outward direction at a point, read from a distance grid (lo, d, voxel, ...)."""
    lo, d, vox = grid[0], grid[1], grid[2]

    def at(p):
        g = (p - lo) / vox
        i = np.floor(g).astype(int)
        if np.any(i < 1) or np.any(i >= np.array(d.shape) - 2):
            return 1.0, np.zeros(3)
        f = g - i

        def tri(o):
            c = d[i[0] + o[0]:i[0] + o[0] + 2, i[1] + o[1]:i[1] + o[1] + 2, i[2] + o[2]:i[2] + o[2] + 2]
            c = c[0] * (1 - f[0]) + c[1] * f[0]
            c = c[0] * (1 - f[1]) + c[1] * f[1]
            return c[0] * (1 - f[2]) + c[1] * f[2]
        n = np.array([tri((1, 0, 0)) - tri((-1, 0, 0)), tri((0, 1, 0)) - tri((0, -1, 0)),
                      tri((0, 0, 1)) - tri((0, 0, -1))])
        return float(tri((0, 0, 0))), n / max(np.linalg.norm(n), 1e-9)
    return at


def hair_locks(H, Rh, jumper, seed=2):
    """Paths of the locks (world coordinates) with their radii. Each lock is combed over the scalp from its
    root to a point at the side or back of the head, then falls under gravity over the shoulders."""
    rng = np.random.default_rng(seed)
    locks = []
    head_at = grid_sampler(head_parts()[0])
    body_at = grid_sampler(jumper)

    def off_skin(p, margin):
        """Keep a point at least `margin` off her skin (the real head, not just the scalp's egg shape)."""
        pl = Rh.T @ (p - H)
        for _ in range(3):
            dv, n = head_at(pl)
            if dv >= margin:
                break
            pl = pl + n * (margin - dv)
        return H + Rh @ pl

    def collide(p, layer):
        pl = Rh.T @ (p - H)
        pl = _push_out_ellipsoid(pl, SCALP_C, SCALP_R, layer)
        p = off_skin(H + Rh @ pl, 0.004 + layer)
        for _ in range(3):                       # and off her jumper: shoulders, roll neck, chest, arms
            dv, n = body_at(p)
            if dv >= 0.003 + layer:
                break
            p = p + n * (0.003 + layer - dv)
        return p

    def lock(th0, e0, thf, side, forward, length, r_flat, r_fall, layer, lift=0.0):
        pts = []
        for t in np.linspace(0, 1, 9):            # 1. over the scalp, from the root to where it starts to fall
            th = th0 + (thf - th0) * np.sqrt(t)
            el = e0 + (np.radians(4) - e0) * t * t
            q = H + Rh @ scalp_point(th, el, layer + lift * (1 - (1 - t) ** 2))
            pts.append(off_skin(q, r_flat + 0.0035 + layer))
        on_scalp = len(pts)
        p = pts[-1]                                # 2. falling
        d = pts[-1] - pts[-2]
        d /= np.linalg.norm(d)
        travelled, step = 0.0, 0.008
        wob = rng.uniform(0, 6.28)
        phase = rng.uniform(-0.5, 0.5)
        shoulder_y = H[1] - 0.10
        while travelled < length:
            force = np.array([0, -1.0, 0])
            pl = Rh.T @ (p - H)
            force += Rh @ np.array([np.sign(pl[0]) * 0.25, 0, 0]) * (pl[1] > -0.12)  # a little fullness
            # soft waves, in step from lock to lock (by height) so they read across the whole fall of hair
            wv = np.sin(2 * np.pi * p[1] / 0.105 + phase) * min(1.0, travelled / 0.06)
            force += Rh @ np.array([np.sign(pl[0]) * 0.34 * wv, 0, 0.14 * wv])
            if p[1] < shoulder_y:
                fwd = Rh @ np.array([0, 0, 1.0])
                fwd[1] = 0
                fwd = unit(fwd)
                sidev = np.cross([0, 1.0, 0], fwd)
                force += (side * -0.10 * sidev + (0.55 if forward else -0.40) * fwd) * \
                    min(1, (shoulder_y - p[1]) / 0.08)
            force += 0.03 * np.array([np.sin(travelled * 8 + wob), 0, np.cos(travelled * 6 + wob)])
            d = d * 0.75 + 0.25 * force
            d /= np.linalg.norm(d)
            p = collide(p + d * step, layer)
            travelled += step
            pts.append(p.copy())
        pts = np.array(pts)
        keep = list(range(on_scalp)) + list(range(on_scalp + 2, len(pts), 2))
        pts = pts[keep]
        t = np.linspace(0, 1, len(pts))
        grow = np.clip((np.arange(len(pts)) - on_scalp + 3) / 6.0, 0, 1)
        radii = (r_flat + (r_fall - r_flat) * grow) * np.clip((1 - t) / 0.35, 0.10, 1) ** 0.8
        locks.append((pts, radii))

    # the top layer, combed out from the parting to both sides (more of it to her left, the parting being off
    # to her right)
    for side in (-1, 1):
        n = 30 if side < 0 else 40
        for i in range(n):
            s = (i + rng.uniform(-0.3, 0.3)) / (n - 1)
            s = min(max(s, 0), 1)
            if s < 0.6:  # front half of the parting: forehead up to the top of the head
                th0, e0 = PART, np.radians(38 + (90 - 38) * s / 0.6)
            else:  # back half: over the top to the crown
                th0, e0 = np.pi * side, np.radians(90 - 35 * (s - 0.6) / 0.4)
            thf = side * np.radians(72 + 95 * s)  # front locks fall in front of the ear, back ones behind
            forward = side < 0 and s < 0.55
            lift = 0.0065 * np.clip(s / 0.35, 0, 1) ** 2 * (1 - 0.5 * np.clip((s - 0.7) / 0.3, 0, 1))  # crown
            lock(th0 + side * 0.03, e0, thf, side, forward, rng.uniform(0.26, 0.38), 0.0038, 0.0105,
                 0.0020 + 0.0030 * rng.random(), lift)
    # an under layer round the back and sides
    for k in range(44):
        side = -1 if k % 2 == 0 else 1
        th = side * np.radians(68 + 110 * (k // 2) / 21) + rng.uniform(-0.03, 0.03)  # ear, round the back
        e0 = np.radians(rng.uniform(8, 30))
        forward = side < 0 and abs(np.degrees(th)) < 110
        lock(th, e0, th, side, forward, rng.uniform(0.27, 0.32), 0.0060, 0.0110, 0.0010 + 0.0015 * rng.random())
    return locks


def hair_grid(H, Rh, jumper, voxel=0.0018, seed=2):
    """The hair as a grid of distances in world coordinates, plus the direction the hair runs in each cell.
    Each lock is a chain of tapered tubes; neighbouring locks are blended, then small gaps closed up so the
    hair falls as a continuous sheet with the locks still showing in it."""
    from scipy import ndimage
    locks = hair_locks(H, Rh, jumper, seed)
    lo, hi = H + HAIR_BOX[0], H + HAIR_BOX[1]
    nn = np.round((hi - lo) / voxel).astype(int) + 1
    d = np.full(nn, 0.05, np.float32)
    flow = np.zeros(tuple(nn) + (3,), np.float32)
    k = 0.008
    for pts, radii in locks:
        m = radii.max() + k + 0.01
        L0 = np.maximum(np.floor((pts.min(0) - m - lo) / voxel).astype(int), 0)
        L1 = np.minimum(np.ceil((pts.max(0) + m - lo) / voxel).astype(int) + 1, nn)
        if np.any(L1 <= L0):
            continue
        tmp = np.full(tuple(L1 - L0), 0.05, np.float32)
        ftmp = np.zeros(tuple(L1 - L0) + (3,), np.float32)
        for a, b_, ra, rb in zip(pts[:-1], pts[1:], radii[:-1], radii[1:]):
            mm = max(ra, rb) + k + 0.008
            i0 = np.maximum(np.floor((np.minimum(a, b_) - mm - lo) / voxel).astype(int), L0)
            i1 = np.minimum(np.ceil((np.maximum(a, b_) + mm - lo) / voxel).astype(int) + 1, L1)
            if np.any(i1 <= i0):
                continue
            xs = (lo[0] + np.arange(i0[0], i1[0]) * voxel)[:, None, None]
            ys = (lo[1] + np.arange(i0[1], i1[1]) * voxel)[None, :, None]
            zs = (lo[2] + np.arange(i0[2], i1[2]) * voxel)[None, None, :]
            dc = np_cone(xs, ys, zs, a, b_, ra, rb).astype(np.float32)
            sl = tuple(slice(i0[q] - L0[q], i1[q] - L0[q]) for q in range(3))
            blk = tmp[sl]
            closer = dc < blk
            fb = ftmp[sl]
            fb[closer] = (b_ - a) / max(np.linalg.norm(b_ - a), 1e-9)
            tmp[sl] = np.minimum(blk, dc)
        gs = tuple(slice(L0[q], L1[q]) for q in range(3))
        g = d[gs]
        closer = tmp < g
        fl = flow[gs]
        fl[closer] = ftmp[closer]
        d[gs] = rig.smin(g, tmp, k)
    # the hair lying on the head: the head's own surface lifted by 7-9 mm, everywhere above the hairline -
    # a soft curve 5 cm above the brows, dipping at the temples and in front of the ears
    hlo, hd, hvox = head_parts()[0]
    hhi = hlo + (np.array(hd.shape) - 1) * hvox
    xs = (lo[0] + np.arange(nn[0]) * voxel).astype(np.float32)
    ys = (lo[1] + np.arange(nn[1]) * voxel).astype(np.float32)
    zs = (lo[2] + np.arange(nn[2]) * voxel).astype(np.float32)
    base = np.full(nn, 0.05, np.float32)
    for i in range(nn[0]):  # a slab at a time, to keep memory modest
        X, Y, Z = np.meshgrid(xs[i:i + 1] - H[0], ys - H[1], zs - H[2], indexing='ij')
        lx = Rh[0, 0] * X + Rh[1, 0] * Y + Rh[2, 0] * Z
        ly = Rh[0, 1] * X + Rh[1, 1] * Y + Rh[2, 1] * Z
        lz = Rh[0, 2] * X + Rh[1, 2] * Y + Rh[2, 2] * Z
        coords = np.stack([(lx - hlo[0]) / hvox, (ly - hlo[1]) / hvox, (lz - hlo[2]) / hvox])
        hv = ndimage.map_coordinates(hd, coords.reshape(3, -1), order=1, mode='nearest').reshape(lx.shape)
        out = sum(np.maximum(np.maximum(hlo[q] - l, l - hhi[q]), 0) ** 2 for q, l in enumerate((lx, ly, lz)))
        hv = hv + np.sqrt(out)  # outside the head's box: keep counting the distance
        ax = np.abs(lx)
        y_hair = np.where(ax < 0.05, HAIRLINE[0] - HAIRLINE[1] * (ax / 0.05) ** 2,
                          HAIRLINE[2] - HAIRLINE[3] * np.clip((ax - 0.05) / 0.025, 0, 1))  # the hairline
        front = np.clip((lz + 0.035) / 0.02, 0, 1)
        edge = np.clip((ly - y_hair) / 0.014, 0, 1)
        edge = edge * edge * (3 - 2 * edge)
        thick = (0.0065 + 0.0065 * np.clip((ly - 0.03) / 0.08, 0, 1)) * (1 - front * 0.42 * (1 - edge))
        b_ = hv - thick
        # edges rounded off (a sharp edge would ripple when stored on the grid)
        b_ = -rig.smin(-b_, -(y_hair - ly) * front, 0.003)           # not over the face
        b_ = -rig.smin(-b_, -(-(ly + 0.03)), 0.004)                  # not down the neck
        # the parting: a fine line along the meridian at PART, from the hairline to the top of the head
        across = np.abs(lx * np.cos(PART) - (lz - SCALP_C[2]) * np.sin(PART))
        part = np.where((ly > 0.04) & (lz > SCALP_C[2]), 0.0022 - across, -0.02)
        b_ = -rig.smin(-b_, -part, 0.0025)
        base[i:i + 1] = np.where(np.isfinite(b_), b_, 0.05)
    d = rig.smin(d, base.astype(np.float32), 0.004)
    # close small gaps between locks: grow by 3.5 mm, re-measure, shrink back
    grow = 0.0035
    d = rig.robust_distance((d - grow).astype(np.float32), voxel) + grow
    d = rig.robust_distance(d.astype(np.float32), voxel)
    return lo, d, voxel, flow


def np_cone(X, Y, Z, a, b, r1, r2):
    """Rounded cone from a (radius r1) to b (radius r2), on a grid."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ba = b - a
    l2 = ba @ ba
    rr = r1 - r2
    a2 = l2 - rr * rr
    il2 = 1.0 / l2
    pax, pay, paz = X - a[0], Y - a[1], Z - a[2]
    y = pax * ba[0] + pay * ba[1] + paz * ba[2]
    z = y - l2
    xx = (pax * l2 - ba[0] * y) ** 2 + (pay * l2 - ba[1] * y) ** 2 + (paz * l2 - ba[2] * y) ** 2
    y2 = y * y * l2
    z2 = z * z * l2
    k = np.sign(rr) * rr * rr * xx
    return np.where(np.sign(z) * a2 * z2 > k, np.sqrt(xx + z2) * il2 - r2,
                    np.where(np.sign(y) * a2 * y2 < k, np.sqrt(xx + y2) * il2 - r1,
                             (np.sqrt(xx * a2 * il2) + y * rr) * il2 - r1))


def get_hair(state, jumper):
    H, Rh = state['head']
    return cached('hair', lambda key: hair_grid(H, Rh, jumper),
                  [hair_grid, hair_locks, scalp_point, grid_sampler, np_cone, rig.smin, rig.robust_distance, PART,
                   HAIRLINE, SCALP_C.tolist(), SCALP_R.tolist(), HAIR_BOX[0].tolist(), HAIR_BOX[1].tolist()]
                  + mh_deps(), (np.round(H, 5).tolist(), np.round(Rh, 5).tolist(), torso_key(state)))


def torso_key(state):
    """What the hair falls over, apart from the head: where she stands and how her spine, neck and
    shoulders are posed (her arms moving below the shoulders don't change how her hair hangs)."""
    p = state['pose']
    keep = ('spine', 'neck', 'clavicle', 'shoulder', 'head', 'root', 'pelvis')
    return (np.round(p.position, 5).tolist(), round(p.yaw, 4),
            sorted((k, np.round(v, 5).tolist()) for k, v in p.rot.items() if k.startswith(keep)))


# ---------------------------------------------------------------------------
# Into the scene
# ---------------------------------------------------------------------------
def prepare(state):
    """Make (or fetch from the cache) the pieces that depend on the pose."""
    _STATE[0] = state
    state['jumper'] = get_jumper(state)
    state['trousers'] = get_trousers(state)
    state['hair'] = get_hair(state, state['jumper'])
    return state


def build(b, state):
    J = state['joints']
    Hc, Rh = state['head']
    # her head (with its own lids, nostrils and lips) and eyeballs, in head coordinates
    b.set_frame(Hc, Rh)
    b.group('head', margin=0.01)
    (lo, d, vox), eyes = head_parts()
    b.grid(lo, d, vox, SKIN, op=UNION)
    for c, r in eyes:
        b.sphere(c, r, EYE, op=UNION)
    # hair
    lo, d, vox, flow = state['hair']
    b.set_frame((0, 0, 0), None)
    b.group('hair', disp=S.D_HAIR, dparams=[Hc[0], Hc[1], Hc[2], 0.09, 0.075, 0.0004], margin=0.01)
    b.grid(lo, d, vox, HAIR, op=UNION)
    # the jumper, its ribs running up the body and along the sleeves
    lo, d, vox, part = state['jumper']
    arms = []
    for s in ('R', 'L'):
        fd = unit(J['wrist.' + s] - J['elbow.' + s])
        arms += list(J['shoulder.' + s]) + list(J['elbow.' + s]) + list(J['wrist.' + s] + fd * JUMPER['cuff'])
    params = [J['spine02'][0], J['spine02'][2], 0.15, 0.0085, 0.0016] + arms + [0.075, J['neck01'][1]]
    b.group('body', disp=S.D_BODY, dparams=params, margin=0.02)
    b.grid(lo, d, vox, KNIT, op=UNION)
    off = b.grid_len                     # the part map rides along in the grid buffer
    b.grids.append(np.ascontiguousarray(part, dtype=np.float32).reshape(-1))
    b.grid_len += part.size
    b.groups[-1]['dparams'][25] = float(off)
    lo, d, vox = state['trousers']
    b.group('trousers', margin=0.01)
    b.grid(lo, d, vox, TROUSERS, op=UNION)
    # hands
    parts = hand_parts()
    for name, (o, R, _), part_ in zip(('right_hand', 'left_hand'), state['hands'], parts):
        b.set_frame(o, R)
        b.group(name, margin=0.01)
        b.grid(part_[0][0], part_[0][1], part_[0][2], SKIN, op=UNION)
    b.set_frame((0, 0, 0), None)


def fill_params(SP, state):
    """The face's painted details: where the eyes are and look, brows, lip colour, the hairline."""
    Hc, Rh = state['head']
    gaze = state['spec'].get('gaze', (0, 0, 1.0))
    SP[0:3] = Hc
    SP[3:12] = Rh.reshape(-1)
    for e, sx in ((0, -1), (1, 1)):
        SP[12 + 3 * e:15 + 3 * e] = Hc + Rh @ np.array([sx * EYE_X, 0, 0])
    SP[18:21] = Rh @ unit(gaze)
    SP[21] = np.arcsin(0.0059 / EYE_R)
    SP[22] = np.arcsin(0.0019 / EYE_R)
    SP[23:29] = [0.0017857, -0.0177143, 0.0239017, -0.0019560, 0.0204516, 0.0252633]  # (lids: geometry now)
    SP[29] = EYE_X
    SP[40:46] = [0.011, 0.056, 0.0168, 0.0050, 0.012, 0.0034]    # eyebrows
    # lip colour, fitted to her measured mouth (corners 22 mm out, lips from 52 to 73.5 mm below the eyes)
    SP[100:106] = [0.022, -0.0590, -0.0525, 0.0010, -0.0632, -0.0735]
    SP[107:110] = (0.66, 0.38, 0.36)
    SP[110:114] = HAIRLINE
    SP[114] = 1.0  # the face's lids and lashes are real geometry: don't paint the old ones on


def solid_boxes(state, pad=0.01):
    """Tight world boxes round each solid piece of her (for working out which part of the picture she can
    change): [(lo, hi), ...]."""
    def solid(grid, o=None, R=None):
        lo, d, vox = grid[0], grid[1], grid[2]
        idx = np.argwhere(d[::2, ::2, ::2] < 0)
        if not len(idx):
            return None
        a, b = lo + idx.min(0) * 2 * vox - pad, lo + idx.max(0) * 2 * vox + pad
        if R is None:
            return a, b
        corners = np.array([[x, y, z] for x in (a[0], b[0]) for y in (a[1], b[1]) for z in (a[2], b[2])])
        w = corners @ R.T + o
        return w.min(0), w.max(0)
    Hc, Rh = state['head']
    out = [solid(head_parts()[0], Hc, Rh), solid(state['hair']), solid(state['jumper']), solid(state['trousers'])]
    for (o, R, _), part in zip(state['hands'], hand_parts()):
        out.append(solid(part[0], o, R))
    return [x for x in out if x is not None]


def colliders(state):
    """For the checks: her hands' surfaces in the world."""
    out = []
    for (o, R, _), part in zip(state['hands'], hand_parts()):
        out.append(o + surface_points(part[0]) @ R.T)
    return out
