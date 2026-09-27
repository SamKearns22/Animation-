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
from materials import SKIN, EYE, KNIT, TROUSERS
import materials
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


def expression(smile=1.0, blink=0.0):
    """Her face units: the smile (0 none .. 1 full, every part of it in proportion) and a blink (0 open ..
    1 shut; the upper lids close, the lower rise a touch)."""
    units = {k: v * smile for k, v in C.SMILE.items()}
    for side in ('Left', 'Right'):
        k = side + 'UpperLidClosed'
        units[k] = units.get(k, 0.0) * (1 - blink) + blink
        k = side + 'LowerLidUp'
        units[k] = units.get(k, 0.0) + 0.15 * blink
    return units


def head_parts(smile=1.0, blink=0.0):
    """Her head and neck with an expression, in head coordinates (origin between the eyes, rest axes):
    ((lo, d, voxel), eyes). Each expression is made once (a minute) and kept; the amounts are rounded to
    steps small enough not to show (a tenth of the smile, a quarter of a blink)."""
    s, b = round(smile * 10) / 10, round(blink * 4) / 4
    if s == 1.0 and b == 0.0:
        return cached('mhhead', C.head_grid, mh_deps(), 0.001)
    return cached('mhhead_x', lambda s_, b_: C.head_grid(0.001, None, None, expression(s_, b_)),
                  mh_deps() + [expression], s, b)


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
    look = spec.get('head_look', spec.get('look_at'))
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
    J = pose.joints(M)
    bends = []
    for (oo, RR), part, s in (((o, R), hp[0], 'R'), ((ol, Rl), hp[1], 'L')):
        w = oo + RR @ part[1]
        bends.append(wrist_bend(RR, part[2], part[3], part[4], unit(J['elbow.' + s] - w)))
        hands.append((oo, RR, w))
    mid = eyes_mid_rest()
    Hc = pose.point(M, 'head', mid)
    Rh = M['head'][:3, :3]
    eye_look = spec.get('eye_look', spec.get('look_at'))    # the eyes may lead the head (see movement.md)
    if eye_look is not None:
        spec = dict(spec, gaze=tuple(Rh.T @ unit(np.asarray(eye_look) - Hc)))
    return dict(spec=spec, pose=pose, M=M, joints=J, hands=hands, bends=bends, grip_roll=roll,
                short=(short_r, short_l), head=(Hc, Rh), smile=spec.get('smile', 1.0), blink=spec.get('blink', 0.0))


def pose_key(state):
    """Numbers that fully describe the bent body (for caching the jumper and hair made for it)."""
    p = state['pose']
    return (np.round(p.position, 5).tolist(), round(p.yaw, 4),
            sorted((k, np.round(v, 5).tolist()) for k, v in p.rot.items()))


# ---------------------------------------------------------------------------
# The jumper and trousers, made over the bent body
# ---------------------------------------------------------------------------
JUMPER = dict(thick=0.012, drape=0.35, bridge=0.03, smooth=0.015, hem=0.085, cuff=0.014, voxel=0.0025,
              collar=('roll', ((0.004, 0.080, 0.021), (0.030, 0.075, 0.019), (0.051, 0.067, 0.016))))
TORSO_PIECES = {'hips', 'chest', 'head', 'thigh.L', 'thigh.R'}


def jumper_grid(state):
    import clothes
    return clothes.top(body(), state['pose'], state['joints'], JUMPER)


def trousers_grid(state):
    import clothes
    return clothes.bottoms(body(), state['pose'], state['joints'], JUMPER)


def get_jumper(state):
    import clothes
    return cached('jumper', jumper_grid_for, [clothes.top, JUMPER, clothes.TORSO, rig.Body.skin, rig.Body.surface,
                                              rig.Body.part_map, rig.drape, rig.robust_distance] + mh_deps(),
                  pose_key(state))


def jumper_grid_for(key):
    return jumper_grid(_STATE[0])


def get_trousers(state):
    import clothes
    return cached('trousers', lambda key: trousers_grid(_STATE[0]),
                  [clothes.bottoms, JUMPER, rig.Body.skin, rig.Body.surface] + mh_deps(), pose_key(state))


_STATE = [None]


# ---------------------------------------------------------------------------
# Hair: long, dark, parted a little to her right, lifted at the crown, falling in soft waves past the
# shoulders - on her right side forward over the shoulder, on her left behind it (hair.py does the work).
# ---------------------------------------------------------------------------
HAIRLINE = (0.066, 0.019, 0.047, 0.057)  # height at the middle, drop to 5 cm out, height and drop at the temple
HAIR = dict(scalp_c=(0.0, 0.026, -0.064), scalp_r=(0.0725, 0.0970, 0.0960), part=np.radians(-17.0),
            hairline=HAIRLINE, top=(30, 40), under=44, length_top=(0.24, 0.40), length_under=(0.24, 0.34),
            r_top=(0.0038, 0.0105), r_under=(0.0060, 0.0110), wave=(0.105, 0.34, 0.14), fullness=0.25,
            forward='right', crown_lift=0.0065, flyaways=(0, 0.0, 0.0), base=(0.0065, 0.013),
            box=((-0.28, -0.52, -0.32), (0.28, 0.18, 0.26)), voxel=0.0018, seed=2)


def get_hair(state, jumper):
    import hair
    H, Rh = state['head']
    return cached('hair', lambda key: hair.grid(HAIR, H, Rh, head_parts()[0], (jumper,)),
                  hair.DEPS + [HAIR, rig.smin, rig.robust_distance] + mh_deps(),
                  (np.round(H, 5).tolist(), np.round(Rh, 5).tolist(), torso_key(state)))


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


def build(b, state, pov=False):
    """Put her in the scene. pov: the camera is her eyes - leave out her head and hair."""
    J = state['joints']
    Hc, Rh = state['head']
    if not pov:
        # her head (with its own lids, nostrils and lips) and eyeballs, in head coordinates
        b.set_frame(Hc, Rh)
        b.group('head', margin=0.01)
        (lo, d, vox), eyes = head_parts(state['smile'], state.get('blink', 0.0))
        b.grid(lo, d, vox, SKIN, op=UNION)
        # the head is one rigid piece with some neck; trim it at the base of her neck (always inside the roll
        # collar), or when she bows her head the bottom of the neck swings back out through her jumper
        # - and trim off the shoulders the piece carries (behind and to each side of the neck), or they rise
        # above the jumper's shoulders when she bows her head
        b.set_frame((0, 0, 0), None)
        up = unit(J['neck01'] - J['spine02'])
        lat = J['shoulder.L'] - J['shoulder.R']
        lat = unit(lat - up * (lat @ up))
        fwd = np.cross(lat, up)
        fwd = fwd if fwd @ (Hc - J['neck02']) > 0 else -fwd
        planes = [(J['neck01'] - 0.01 * up, up)]
        for side in (1, -1):
            n = unit(-0.6 * side * lat + 0.6 * up + 0.5 * fwd)
            planes.append((J['neck02'] + 0.05 * side * lat, n))
        for c, n in planes:
            x = unit(np.cross(n, fwd if abs(n @ fwd) < 0.9 else lat))
            b.halfspace(c, np.stack([x, n, np.cross(x, n)], 1), SKIN, op=S.SUB)
        b.set_frame(Hc, Rh)
        for c, r in eyes:
            b.sphere(c, r, EYE, op=UNION)
        # hair
        lo, d, vox, flow = state['hair']
        b.set_frame((0, 0, 0), None)
        b.group('hair', disp=S.D_HAIR, dparams=[Hc[0], Hc[1], Hc[2], 0.09, 0.075, 0.0004], margin=0.01)
        b.grid(lo, d, vox, materials.HAIR, op=UNION)
    b.set_frame((0, 0, 0), None)
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
    # lip colour, fitted to her measured mouth (corners 22 mm out, lips from 52 to 73.5 mm below the eyes) when
    # smiling; as the smile relaxes the mouth line drops ~2 mm and the lower lip ~4 mm (measured on MakeHuman's
    # lip bones), so the colour follows
    rel = 1.0 - state.get('smile', 1.0)
    SP[100:106] = np.array([0.022, -0.0590, -0.0525, 0.0010, -0.0632, -0.0735]) + \
        rel * np.array([0.0005, -0.0021, 0.0, 0.0, -0.0021, -0.0042])
    SP[107:110] = (0.66, 0.38, 0.36)
    SP[110:114] = HAIRLINE
    SP[114] = 1.0  # the face's lids and lashes are real geometry: don't paint the old ones on


def pieces(state, pov=False):
    """Every grid of her in the scene, as (grid, origin, rotation) - origin/rotation None for world grids."""
    Hc, Rh = state['head']
    out = [] if pov else [(head_parts(state['smile'], state.get('blink', 0.0))[0], Hc, Rh),
                          (state['hair'][:3], None, None)]
    out += [(state['jumper'][:3], None, None), (state['trousers'], None, None)]
    for (o, R, _), part in zip(state['hands'], hand_parts()):
        out.append((part[0], o, R))
    return out


def colliders(state):
    """For the checks: her hands' surfaces in the world."""
    out = []
    for (o, R, _), part in zip(state['hands'], hand_parts()):
        out.append(o + surface_points(part[0]) @ R.T)
    return out
