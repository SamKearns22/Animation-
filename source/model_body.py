#!/usr/bin/env python3
"""MAP  model_body: anyone in any kit film drawn as a model body (investigation model-body-all, step 2, Sam's Y 25 Nov).
The film's own people code runs as it is (its poses, paths, cameras, times); every call that would draw a flat person
(midterminal_set.put) is caught instead, and that same skeleton (lying.from_views: the flat pose in metres) poses the
measured MakeHuman body of that person's build (solid_seat.build) by its own skin weights: one closed body, each
limb aimed AND stretched to the kit's joints, so hands and feet land where the flat drawing put them. Everything that
stands in the room (the set's own furniture faces, the door leaf, the wall round the doorway) goes into the SAME depth
pass as solids that hide but are not painted (the set's own flat drawing shows there), so what hides what is decided
by depth alone. House look: flat colours, house ink on silhouettes, part borders and depth folds, the house head
drawing (lying_flat, laid at the head's depth), circle hands as solid balls, held glasses as solids.

  rest(sp) ............. the build's rest body (cached): points, triangles, slot weights, rest joints, normals
  pose(k, sp) .......... the body on lying.Body k (world metres): 13 slots (trunk, neck, arms, forearms, thighs, shins,
                         feet), each an aim-and-stretch from its rest joint to the kit joint; the jacket pushed out
  suit_parts(..) ....... jacket / shirt / trousers / shoes / skin per dot from the rest point (clean painted edges)
  holdouts(cam, ..) .... the set's furniture faces as triangles (MS.items' own parts), the door leaf box
  frame(film, t) ....... one frame: the set with nobody in it, then the bodies, solids, heads; and its faults
  crossings(..) ........ body points inside a solid (desk, chair, door) deeper than 1 cm: the bar is 0

    python3 source/model_body.py still FILM T OUT.png
    python3 source/model_body.py clip FILM T0 T1 OUT.mp4 [--posted MP4]    side by side (posted | model body)
"""
import math
import os
import subprocess
import sys
import time

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bench_draw as BD     # noqa: E402
import bench_pose as BP     # noqa: E402
import solid_seat as SSE    # noqa: E402

W, H = 1080, 1920
INK = (24, 20, 22)
EASE_JACKET = 0.16          # the jacket stands this far off the skin (decimetres: 1.6 cm), so its hem steps out
SLOTS = ['trunk', 'neck', 'armL', 'armR', 'foreL', 'foreR', 'thighL', 'thighR', 'shinL', 'shinR', 'footL', 'footR']
HIDE = ('head', 'jaw', 'eye', 'oculi', 'tongue', 'levator', 'oris', 'orbicularis', 'risorius', 'temporalis',
        'special', 'mandible', 'wrist', 'finger', 'metacarpal', 'thumb')
_R = {}


def _u(a):
    a = np.asarray(a, float)
    return a / (np.linalg.norm(a) + 1e-12)


def _slot(bn):
    """MakeHuman bone -> slot (its side letter is MakeHuman's: .L at +x)."""
    s = bn[-1] if bn[-2:] in ('.L', '.R') else ''
    if bn.startswith(('upperarm',)):
        return 'arm' + s
    if bn.startswith(('lowerarm', 'wrist', 'finger', 'metacarpal', 'thumb')):
        return 'fore' + s
    if bn.startswith('upperleg'):
        return 'thigh' + s
    if bn.startswith('lowerleg'):
        return 'shin' + s
    if bn.startswith(('foot', 'toe')):
        return 'foot' + s
    if bn.startswith(('neck', 'head', 'jaw', 'eye', 'oculi', 'tongue', 'levator', 'oris', 'orbicularis', 'risorius',
                      'temporalis', 'special', 'mandible', 'tongue')):
        return 'neck'
    return 'trunk'


def rest(sp):
    R0 = SSE.rest(sp)                           # the build's mesh, skeleton, trouser shell (shared with solid_seat)
    key = tuple(sorted(R0['build'].items()))
    if key in _R:
        return _R[key]
    import mesh_sdf as MSD
    v, sk = R0['v'], R0['sk']
    G = np.zeros((len(v), len(SLOTS)))
    grp = np.zeros((len(v), 5))
    hide = np.zeros(len(v))
    for bn, (idx, w) in sk.weights.items():
        G[idx, SLOTS.index(_slot(bn))] += w
        grp[idx, BP._group(bn)] += w
        if bn.startswith(HIDE):
            hide[idx] += w
    G /= np.maximum(G.sum(1, keepdims=True), 1e-9)
    grp /= np.maximum(grp.sum(1, keepdims=True), 1e-9)
    hd = lambda b: sk.rest[b][:3, 3].copy()
    J = {}
    for s in 'LR':
        J['sh' + s], J['el' + s], J['wr' + s] = hd('upperarm01.' + s), hd('lowerarm01.' + s), hd('wrist.' + s)
        J['hip' + s], J['kn' + s], J['an' + s] = hd('upperleg01.' + s), hd('lowerleg01.' + s), hd('foot.' + s)
    J['pelvis'] = (J['hipL'] + J['hipR']) / 2
    J['neck'] = hd('neck01')
    J['head'] = hd('head')
    T = R0['tris']
    N = MSD.vertex_normals(v, T)
    if np.median(np.einsum('ij,ij->i', v - v.mean(0), N)) < 0:
        N = -N
    vc = R0['vc'].copy()                        # the trouser shell (solid_seat), then the jacket shell over the trunk
    jk = (grp[:, 0] + grp[:, 1] > 0.5) & (v[:, 1] > J['pelvis'][1] - 0.9)
    vc[jk] += N[jk] * EASE_JACKET
    foot = SSE._foot_pts(R0)
    keep = (hide[T].max(1) < 0.5) & ~foot[T].all(1)
    R = dict(v=v, vc=vc, T=T[keep], G=G, grp=grp, J=J, sk=sk, build=R0['build'], foot=foot, R0=R0)
    _R[key] = R
    return R


def _aim(a0, b0, a1, b1, s0, stretch=True):
    """Affine (M, from, to): rest segment a0->b0 onto a1->b1, uniform scale s0 across, stretched along."""
    u = _u(b0 - a0)
    Rm = BP._align(u, b1 - a1)
    k = np.linalg.norm(b1 - a1) / (np.linalg.norm(b0 - a0) * s0) if stretch else 1.0
    return Rm @ (s0 * (np.eye(3) + (k - 1) * np.outer(u, u))), a0, a1


def pose(k, sp):
    """World points of the posed body (and the rest points for painting): each slot aimed and stretched."""
    R = rest(sp)
    J, G, v = R['J'], R['G'], R['vc']
    K = {n: np.asarray(p, float) for n, p in k.items() if not isinstance(p, (str, bool))}
    # which MakeHuman side is which kit side: the one that keeps the body a turn of the rest body (never mirrored)
    fw = _u(k['fwd'])
    up = _u(K['neck'] - K['pelvis'])
    side = {'L': 'L', 'R': 'R'}
    a_rest = np.cross(J['hipL'] - J['hipR'], [0, 1, 0]) @ [0, 0, 1]
    a_kit = np.cross(K['hipL'] - K['hipR'], up) @ fw
    if np.sign(a_rest) != np.sign(a_kit):
        side = {'L': 'R', 'R': 'L'}             # mh side -> kit side
    Kk = {}
    for n in ('sh', 'el', 'wr', 'hip', 'kn', 'an'):
        for s in 'LR':
            Kk[n + s] = K[n + side[s]]
    leg0 = np.mean([np.linalg.norm(J['kn' + s] - J['hip' + s]) + np.linalg.norm(J['an' + s] - J['kn' + s]) for s in 'LR'])
    leg1 = np.mean([np.linalg.norm(Kk['kn' + s] - Kk['hip' + s]) + np.linalg.norm(Kk['an' + s] - Kk['kn' + s])
                    for s in 'LR'])
    s0 = leg1 / leg0                            # metres per decimetre
    A = {}
    # trunk: a full frame (across by the hips, up to the neck, forward), stretched to the kit's trunk length
    x0, y0 = _u(J['hipL'] - J['hipR']), _u(J['neck'] - J['pelvis'])
    x0 = _u(x0 - y0 * (x0 @ y0))
    x1 = _u(Kk['hipL'] - Kk['hipR'])
    x1 = _u(x1 - up * (x1 @ up))
    F0 = np.stack([x0, y0, np.cross(x0, y0)], 1)
    F1 = np.stack([x1, up, np.cross(x1, up)], 1)
    kt = np.linalg.norm(K['neck'] - K['pelvis']) / (np.linalg.norm(J['neck'] - J['pelvis']) * s0)
    A['trunk'] = (F1 @ np.diag([s0, s0 * kt, s0]) @ F0.T, J['pelvis'], K['pelvis'])
    Mt = A['trunk']
    tr = lambda p: Mt[0] @ (p - Mt[1]) + Mt[2]
    hd = _u(K['head'] - K['neck'])
    A['neck'] = (BP._align(Mt[0] @ (J['head'] - J['neck']), hd) @ Mt[0], J['neck'], tr(J['neck']))
    for s in 'LR':
        A['arm' + s] = _aim(J['sh' + s], J['el' + s], Kk['sh' + s], Kk['el' + s], s0)
        A['fore' + s] = _aim(J['el' + s], J['wr' + s], Kk['el' + s], Kk['wr' + s], s0)
        A['thigh' + s] = _aim(J['hip' + s], J['kn' + s], Kk['hip' + s], Kk['kn' + s], s0)
        A['shin' + s] = _aim(J['kn' + s], J['an' + s], Kk['kn' + s], Kk['an' + s], s0)
        # the foot flat on the floor, its toes along the kit's toe direction (turned only about the upright)
        toe = np.asarray(k['toe' + side[s]], float)
        toe = _u(toe - up * (toe @ up)) if abs(toe @ up) < 0.99 else fw
        f0 = np.array([0, 0, 1.0])
        Ry = BP._align(f0, toe)
        A['foot' + s] = (Ry @ (F1 @ F0.T if False else np.eye(3)) * s0, J['an' + s], Kk['an' + s])
    P = np.zeros((len(v), 3))
    for i, nm in enumerate(SLOTS):
        M, a, t = A[nm]
        P += G[:, i:i + 1] * ((v - a) @ M.T + t)
    # each shoe: the closed hull round that foot's posed points (solid_seat's shoe: no bare toes ever show)
    R = dict(R, T=np.concatenate([R['T']] + list(SSE._shoes(P, R['R0'], R['foot']))))
    return P, R


def real_skeleton(k, sp, kit_hip_h, seat=None, surfaces=(), held=()):
    """The kit's pose on the measured body's OWN lengths (the kit draws short legs and a long trunk): the trunk, neck
    and head keep the kit's directions; the whole upper body is raised by the difference in standing hip height (one
    number per person, so nothing pops); a seated bottom rests on the cushion (seat = (top y, x0, x1, z0, z1)); each
    hand and foot is sent where the film put it (hands raised with the body, feet left on the floor) by a two-bone
    reach that bends the way the kit's elbow and knee bend. A hand the flat drawing laid on a surface (its wrist over
    a top, from 15 cm above it down into it; surfaces = [(top y, x0, x1, z0, z1)]) rests on that top instead."""
    import lying as LY
    R = rest(sp)
    J, v = R['J'], R['v']
    s0 = sp.get('height', 1.75) / (v[:, 1].max() - v[:, 1].min())
    K = LY.Body({n: np.asarray(p, float) for n, p in k.items() if not isinstance(p, (str, bool))})
    sole = v[:, 1].min()
    raise_ = (J['pelvis'][1] - sole) * s0 - kit_hip_h
    upv = np.array([0, 1.0, 0])
    pel = K['pelvis'] + upv * raise_
    if seat is not None:
        top, x0, x1, z0, z1 = seat
        if x0 <= pel[0] <= x1 and z0 <= pel[2] <= z1:
            sit = top + 0.105 * sp.get('height', 1.75) / 1.75      # the hip joints 10.5 cm over the cushion
            pel[1] = max(pel[1], sit)
    lift = pel - K['pelvis']
    tdir = _u(K['neck'] - K['pelvis'])
    neck = pel + tdir * np.linalg.norm(J['neck'] - J['pelvis']) * s0
    hdir = _u(K['head'] - K['neck'])
    head = neck + hdir * np.linalg.norm(J['head'] - J['neck']) * s0 + tdir * 0.0
    out = K.copy()
    out['pelvis'], out['neck'] = pel, neck
    out['head'] = neck + hdir * 0.14 * sp.get('height', 1.75) / 1.75        # the house head's centre over the neck
    x1 = _u(K['hipL'] - K['hipR'])
    x1 = _u(x1 - tdir * (x1 @ tdir))
    x0, y0 = _u(J['hipL'] - J['hipR']), _u(J['neck'] - J['pelvis'])
    x0 = _u(x0 - y0 * (x0 @ y0))
    F0 = np.stack([x0, y0, np.cross(x0, y0)], 1)
    F1 = np.stack([x1, tdir, np.cross(x1, tdir)], 1)
    Rt = F1 @ F0.T
    sgn = 1.0
    fw = _u(np.asarray(k['fwd'], float))
    if np.cross(x1, tdir) @ fw < 0:              # the kit's L is MakeHuman's R: swap the rest sides
        sgn = -1.0
    tr = lambda p: Rt @ ((p - J['pelvis']) * s0) + pel
    for s in 'LR':
        m = s if sgn > 0 else {'L': 'R', 'R': 'L'}[s]
        sh, hip = tr(J['sh' + m]), tr(J['hip' + m])
        la, lf = np.linalg.norm(J['el' + m] - J['sh' + m]) * s0, np.linalg.norm(J['wr' + m] - J['el' + m]) * s0
        lt, ls = np.linalg.norm(J['kn' + m] - J['hip' + m]) * s0, np.linalg.norm(J['an' + m] - J['kn' + m]) * s0
        wr_t = K['wr' + s] + lift
        hang = _u(K['wr' + s] - K['sh' + s])
        if hang[1] < -0.75 and s not in held:   # an empty arm hanging at the side keeps the kit's direction from the
            wr_t = sh + hang * (la + lf) * 0.97  # shoulder (the measured hips are wider: sent to the kit's wrist,
        #                                          the elbows bowed out like hands on hips, chat 2)
        for top, a0, a1, b0, b1 in surfaces:
            w0 = K['wr' + s]
            if a0 <= w0[0] <= a1 and b0 <= w0[2] <= b1 and w0[1] < top + 0.15:
                wr_t = np.array([w0[0], top + 0.03 * sp.get('height', 1.75) / 1.75, w0[2]])
        pole = K['el' + s] - (K['sh' + s] + K['wr' + s]) / 2
        el, wr = LY.limb(sh, wr_t, la, lf, pole)
        an_t = K['an' + s].copy()
        polek = K['kn' + s] - (K['hip' + s] + K['an' + s]) / 2
        if np.linalg.norm(polek) < 1e-4:
            polek = fw
        kn, an = LY.limb(hip, an_t, lt, ls, polek)
        out['sh' + s], out['el' + s], out['wr' + s] = sh, el, wr
        out['hip' + s], out['kn' + s], out['an' + s] = hip, kn, an
    out['_reach'] = max([np.linalg.norm(out['wr' + s] - (K['wr' + s] + lift)) for s in 'LR'
                         if not (_u(K['wr' + s] - K['sh' + s])[1] < -0.75 and s not in held)] or [0.0])
    out['_foot'] = max(np.linalg.norm((out['an' + s] - K['an' + s])[[0, 2]]) for s in 'LR')   # (across the floor)
    return out


# ------------------------------------------------------------------------------------------------ clothes
PART_NAMES = ['skin', 'jacket', 'shirt', 'trousers', 'shoes', 'pocket', 'pin', 'hand', 'glass', 'mimosa', 'handset',
              'solid']
PIX = {n: i for i, n in enumerate(PART_NAMES)}


def suit_parts(rv, grp, R, sp):
    """A suit per dot from its rest point: the jacket over trunk and arms, open at the front (his: open all the way
    down, the white shirt between; hers: a V to the button, the top under it), trousers, shoes; the neck bare."""
    J = R['J']
    x, y, z = rv[:, 0], rv[:, 1], rv[:, 2]
    ax = np.abs(x)
    g = grp.argmax(1)
    hip, neck, sh = J['pelvis'][1], J['neck'][1], (J['shL'][1] + J['shR'][1]) / 2
    hem = hip - 0.9                              # the jacket's hem: below the seat (9 cm under the hip joints)
    part = np.full(len(rv), PIX['trousers'])
    upper = ((g == 0) | (g == 1)) & (y >= hem)
    part[upper] = PIX['jacket']
    collar = neck - 0.35
    part[(g == 3) | (y > collar + 0.2) & (g != 1)] = PIX['skin']
    # the front opening: a V from the collar (half width 0.62 dm at the collar) to the button, then open or closed
    button = hip + (sh - hip) * sp.get('v_button', 0.35 if sp.get('jacket_open', True) else 0.42)   # (R7 chat 8: a
    #                                             spec may set where the V closes, a share of hips to shoulders)
    u = np.clip((collar - y) / max(0.1, collar - button), 0, 1)
    vw = 0.62 * (1 - u) + 0.12 * u
    if sp.get('jacket_open', True):
        vw = np.where(y < button, 0.12 + 0.10 * np.clip((button - y) / max(0.1, button - hem), 0, 1), vw)
        gap = (y >= hem) & (y <= collar + 0.2)
    else:
        gap = (y >= button) & (y <= collar + 0.2)
    front = (z > 0.3) & (ax < vw) & gap & (g == 0)
    part[front] = PIX['shirt']
    part[front & (y < hip + 0.25)] = PIX['trousers']          # the waistband and fly under an open jacket
    if sp.get('who') == 'elsayed':                # the white pocket square on his left chest (MakeHuman's .L: +x)
        part[(g == 0) & (z > 0.3) & (x > 0.62) & (x < 1.02) & (y > sh - 1.05) & (y < sh - 0.82)] = PIX['pocket']
        part[(g == 0) & (z > 0.3) & (x > 0.75) & (x < 0.88) & (y > sh - 0.55) & (y < sh - 0.42)] = PIX['pin']
    if sp.get('who') == 'aoc':                    # the gold lapel pin
        part[(g == 0) & (z > 0.3) & (x > 0.62) & (x < 0.78) & (y > sh - 0.62) & (y < sh - 0.46)] = PIX['pin']
    ank = (J['anL'][1] + J['anR'][1]) / 2
    part[(g == 4) | ((g == 2) & (y < ank - 0.15))] = PIX['shoes']
    return part


def colours(sp):
    return {'skin': tuple(sp['skin']), 'jacket': tuple(sp['jacket']), 'shirt': tuple(sp['shirt']),
            'trousers': tuple(sp['trousers']), 'shoes': tuple(sp['shoe']), 'pocket': (250, 250, 250),
            'pin': (212, 170, 60), 'hand': tuple(sp['skin']), 'glass': (226, 238, 244), 'mimosa': (246, 166, 52),
            'handset': (40, 40, 46), 'solid': (0, 0, 0)}


# ------------------------------------------------------------------------------------------------ solids
def _tris_of_face(pts):
    pts = [np.asarray(p, float) for p in pts]
    if len(pts) < 3:
        return [], []
    P = np.array(pts)
    if np.linalg.norm(np.cross(P[1] - P[0], P[2] - P[0])) < 1e-9 and len(P) == 3:
        return [], []
    return P, [(0, i, i + 1) for i in range(1, len(P) - 1)]


def mesh_of_parts(parts):
    Ps, Ts, n = [], [], 0
    for part in parts:
        for f in part:
            P, T = _tris_of_face(f.pts)
            if len(T):
                Ps.append(P)
                Ts += [(a + n, b + n, c + n) for a, b, c in T]
                n += len(P)
    if not Ps:
        return None
    return np.concatenate(Ps), np.array(Ts, int)


def set_solids(MS, swap=None):
    """Every piece of furniture the set stands in the room, from its own faces (so the solids ARE what is drawn),
    one solid per box. swap(name, i, part) may hand back other solids for a box (a desk's kneehole: the flat set
    draws a desk as one block, but a seated person's knees go under it)."""
    out = []
    for ref, fn in MS.items(None):
        parts = (fn.__defaults__ or (None,))[0]
        if not isinstance(parts, list):
            continue
        nm = 'set@%.2f,%.2f' % (ref[0], ref[2])
        for i, part in enumerate(parts):
            got = swap(nm, i, part) if swap else None
            if got is not None:
                out += got
                continue
            m = mesh_of_parts([part])
            if m is not None:
                out.append(m + (f'{nm}#{i}',))
    return out


def box(lo, hi):
    P, T = BD._box(lo, hi)
    return P, T


def ball(c, r, n=14):
    return BD._ball(c, r, n)


def flute_mesh(hand, up, fwd, scale):
    """The film's flute (islamocommunism.flute, units about the hand, h 150) as a solid of turning: foot, stem,
    bowl; the bowl's lower part mimosa. Returns [(P, T, part)]."""
    up = _u(up)
    a = _u(np.cross(up, fwd))
    b = np.cross(a, up)
    h, w = 150.0, 22.5
    prof = [(w * 1.5, 46), (w * 1.5, 40), (2.6, 40), (2.6, -44), (w * 0.45, -44), (w * 0.9, -60), (w, -h + 30)]
    n = 14
    out = []
    pts, tris = [], []
    for i, (r, yy) in enumerate(prof):
        for kk in range(n):
            ang = 2 * math.pi * kk / n
            pts.append(hand + (a * math.cos(ang) * r + b * math.sin(ang) * r - up * yy) * scale)
    for i in range(len(prof) - 1):
        for kk in range(n):
            p0, p1 = i * n + kk, i * n + (kk + 1) % n
            q0, q1 = p0 + n, p1 + n
            tris += [(p0, p1, q1), (p0, q1, q0)]
    P = np.array(pts)
    T = np.array(tris)
    out.append((P, T, 'glass'))
    # the juice: a cone inside the bowl up to h - 50, drawn as its own solid just inside the glass's front
    prof2 = [(w * 0.42, -48), (w * 0.85, -62), (w * 0.9, -h + 50)]
    pts2 = [hand + (a * math.cos(2 * math.pi * kk / n) * r * 1.02 + b * math.sin(2 * math.pi * kk / n) * r * 1.02
                    - up * yy) * scale for r, yy in prof2 for kk in range(n)]
    tris2 = []
    for i in range(len(prof2) - 1):
        for kk in range(n):
            p0, p1 = i * n + kk, i * n + (kk + 1) % n
            tris2 += [(p0, p1, p1 + n), (p0, p1 + n, p0 + n)]
    top = len(pts2)
    pts2.append(hand + (-up * (-h + 50)) * scale)
    for kk in range(n):
        tris2.append(((len(prof2) - 1) * n + kk, (len(prof2) - 1) * n + (kk + 1) % n, top))
    out.append((np.array(pts2), np.array(tris2), 'mimosa'))
    return out


# ------------------------------------------------------------------------------------------------ the pass
def raster(cam, objs, scale, attrs_by_obj):
    """objs: [(P, T, part index per tri, name)]. Depth, part, object and the person's rest attributes per dot."""
    w, h = W * scale, H * scale
    zb = np.full((h, w), np.inf)
    pb = np.full((h, w), -1, np.int64)
    ob = np.full((h, w), -1, np.int64)
    na = 8
    ab = np.zeros((h, w, na))
    for oi, (P, T, tpi, nm) in enumerate(objs):
        xy, z = BD._proj(cam, P)
        att = attrs_by_obj.get(oi)
        BD._fill(np.ascontiguousarray(xy * scale, float), np.ascontiguousarray(z, float),
                 np.ascontiguousarray(T, np.int64), np.ascontiguousarray(tpi, np.int64), zb, pb, ob, oi,
                 float(cam.NEAR), ab if att is not None else np.zeros((1, 1, 1)),
                 np.ascontiguousarray(att, float) if att is not None else np.zeros((1, 1)), att is not None)
    return zb, pb, ob, ab


def ink(zb, pb, ob, solid, width):
    """House outlines on the drawn things only: an object or part change, or a depth fold, on the nearer side; never
    on a solid (the set's own drawing already has its lines there)."""
    h, w = zb.shape
    edge = np.zeros((h, w), bool)
    zf = np.where(np.isfinite(zb), zb, 1e3)
    obi = np.where(ob >= 0, ob, -1)
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        a = (slice(0, h - dy), slice(max(0, -dx), w - max(0, dx)))
        b = (slice(dy, h), slice(max(0, dx), w - max(0, -dx)))
        diff = (obi[a] != obi[b]) | (pb[a] != pb[b]) | (np.abs(zf[a] - zf[b]) > 0.03 + 0.02 * np.minimum(zf[a], zf[b]) / 4)
        near_a = zf[a] <= zf[b]
        edge[a] |= diff & near_a & (ob[a] >= 0)
        edge[b] |= diff & ~near_a & (ob[b] >= 0)
    edge &= ~solid
    if width > 1:
        from scipy import ndimage
        edge = ndimage.binary_dilation(edge, iterations=int(width // 2)) & ~solid
    return edge


def world_of(cam, zb, scale):
    h, w = zb.shape
    ys, xs = np.mgrid[0:h, 0:w]
    sx = (xs + 0.5) / scale - 540 - cam.shake[0]
    sy = (ys + 0.5) / scale - 960 - cam.shake[1]
    f, r, u = (np.asarray(v_, float) for v_ in (cam.f, cam.r, cam.u))
    d = f[None, None] + r[None, None] * (sx / cam.focal)[..., None] - u[None, None] * (sy / cam.focal)[..., None]
    return np.asarray(cam.pos, float)[None, None] + d * np.where(np.isfinite(zb), zb, 0)[..., None]


def crossings(P, solids_named, used):
    """Body points inside a box-like solid (its faces' bounding box shrunk 1 cm): (points, solid)."""
    out = {}
    Q = P[used]
    for Ps, Ts, nm in solids_named:
        if len(Ps) == 8 and nm.endswith('leaf'):  # a turned slab (front 0-3, back 4-7): tested in its own frame
            o = Ps[0]
            ax = [Ps[1] - o, Ps[3] - o, Ps[4] - o]
            u = np.stack([((Q - o) @ a) / (a @ a) for a in ax], 1)
            m = np.all((u > 0.0) & (u < 1.0), 1)
            m &= np.abs(((Q - o) @ ax[0]) / np.linalg.norm(ax[0]) - np.linalg.norm(ax[0]) / 2) < np.linalg.norm(ax[0]) / 2 - 0.01
            if m.any():
                out[nm] = out.get(nm, 0) + int(m.sum())
            continue
        lo, hi = Ps.min(0) + 0.01, Ps.max(0) - 0.01
        if (hi - lo).min() <= 0:
            continue
        m = np.all((Q > lo) & (Q < hi), 1)
        if m.any():
            out[nm] = out.get(nm, 0) + int(m.sum())
    return out
