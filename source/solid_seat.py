#!/usr/bin/env python3
"""MAP  solid_seat: seated legs from the measured body, for ANY kit person (proposal seated-legs-3d, Sam's "1",
25 Nov; Learn steps 1-2, R7 chat 6). The GTA bench's way of drawing (bench_pose: the MakeHuman body posed by its own
skin weights as ONE closed body; bench_draw: one depth pass, house flat colours, house ink on silhouettes, part
borders and depth jumps) taken out of the Jason/car code: the build comes from the person's kit spec, the joints from
the kit's own seated pose (sitting.realize: hips, knees, ankles in person units), the picture from the kit's own
camera (views.project and the person's Local), so the solid legs land exactly where the flat body expects them.
Nothing changes for any film unless its spec says seat_solid ('legs' or 'whole'): posted films are untouched.

  build(sp) .............. MakeHuman's six build numbers from the spec (woman/man, age, weight)
  rest(sp) ............... that build's rest body: points, triangles, bones, weights, joints; the trouser shell
  pose(j, sp) ............ the body on the kit joints (person units, kit frame: x across, y down, z forward); each
                           chain (thigh, shin) aimed AND stretched to the kit's bone, the foot flat on the floor,
                           the seat pressing the bottom and thighs flat where they rest on it
  draw(p, j, yaw, sp) .... the solid lower body (mode 'legs') into the picture under the flat torso; keeps its
                           depth for lay_over
  lay_over(img) .......... after the torso: whatever of the legs lies in front of the torso's front (knees, a crossed
                           top leg) drawn over the jacket, inked where it leaves it
  checks(j, sp, yaw) ..... seat and leg-leg crossings, each clothing part one piece (mesh and picture)
"""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bench_draw as BD     # noqa: E402
import bench_pose as BP     # noqa: E402

INK = (24, 20, 22)
SKIRT_BELOW = 0.5       # a knee-length skirt: its hem this far (rest decimetres) below the knee joint
TORSO_FRONT = 45.0      # person units in front of the hip joints: the jacket's front where it lies on the lap (7 cm; chat 7,
#                         was 80: the hem hid the thighs and the knees showed as balls under the hands); legs nearer
#                         than this are in front of the torso and drawn over it (lay_over; the legs only: the
#                         belly is under the jacket, chat 7: a trouser flap showed over the jacket's front)
EASE = 0.12             # trouser cloth this far off the skin (decimetres of the rest body: 1.2 cm)
HEM_K = 0.85            # the hem this share of the knee's width
KNEE_CLOTH = 0.72       # a trouser leg's half width at the knee and below (decimetres: 14.4 cm across; proposal)
TOUCH = 0.005 / 0.00152  # 5 mm in person units: deeper than this inside the other leg is a crossing (bench_move)
PRESS_ROUNDS = 6        # contact settling rounds (seat, leg on leg)
EDGE_R = 40.0           # the seat cushion's front edge: rounded over this many person units
BOTTOM_FADE = 70.0      # the bottom's fit fades over this height up to the waist (10 cm)
SPREAD = 0.5           # pressed flesh spreads out this much per unit pressed down (volume kept; chat 7)
SPREAD_R = 40.0         # directions ease in over this distance from the middle (no tearing where they meet)
SPREAD_H = 40.0         # ... fading over this height above the seat (6 cm)
SINK_MAX = 90.0         # deeper than this under the cushion's top is below the seat, not on it (14 cm)
HANG = 25.0             # a crossed top leg's foot tips this far down from square to its shin (relaxed)
SEAT_BLOCK = 40.0       # the cushion's thickness under its top (6 cm): a shin inside it crosses the seat
SEAT_SOFT = 6.0         # the bottom and thighs pressed flat on the seat: nothing deeper than this into the cushion
_REST = {}
LAST = {}


def _u(a):
    a = np.asarray(a, float)
    return a / (np.linalg.norm(a) + 1e-12)


def woman(sp):
    import views as V
    return sp.get('figure') in V.WOMAN_LEGS or sp.get('gender') == 'woman'


def build(sp):
    """MakeHuman's build numbers from the kit spec (no new numbers to tune per person: woman/man, age band)."""
    w = woman(sp)
    age = 0.75 if str((sp.get('kit_house') or {}).get('age', {}).get('age') or '') >= '60' else 0.55
    return dict(gender=0.0 if w else 1.0, age=age, muscle=0.5, weight=0.55 if w else 0.5, height=0.5,
                proportions=0.5)


def rest(sp):
    """The rest body for this build (cached by build): MakeHuman decimetres, y up, face +z."""
    b = build(sp)
    key = tuple(sorted(b.items()))
    if key in _REST:
        return _REST[key]
    import mhuman as H
    v, g = H.load_base()
    H.apply_macros(v, H.macro_values(**b))
    sk = H.Skeleton(v)
    tris = []
    for f in g['body']:
        tris.append((f[0], f[1], f[2]))
        if len(f) == 4:
            tris.append((f[0], f[2], f[3]))
    tris = np.array(tris, int)
    skirt = []
    for f in g.get('helper-skirt', []):
        skirt.append((f[0], f[1], f[2]))
        if len(f) == 4:
            skirt.append((f[0], f[2], f[3]))
    J = {}
    for s in 'LR':
        J['hip' + s] = sk.rest['upperleg01.' + s][:3, 3].copy()
        J['knee' + s] = sk.rest['lowerleg01.' + s][:3, 3].copy()
        J['ankle' + s] = sk.rest['foot.' + s][:3, 3].copy()
    # each point's transform group and side, from its bones' weights
    G = np.zeros((len(v), 7))                  # trunk, thighR, shinR, footR, thighL, shinL, footL (MakeHuman sides)
    for bn, (idx, w) in sk.weights.items():
        G[idx, _slot(bn)] += w
    G /= np.maximum(G.sum(1, keepdims=True), 1e-9)
    arm = np.zeros(len(v))
    for bn, (idx, w) in sk.weights.items():
        if bn.startswith(('upperarm', 'lowerarm', 'wrist', 'finger', 'metacarpal', 'thumb')):
            arm[idx] += w
    R = dict(v=v, tris=tris, skirt=np.array(skirt, int), sk=sk, J=J, G=G, build=b, arm=arm)
    R['vc'] = _cloth(R)
    _REST[key] = R
    return R


def _slot(bn):
    side = 0 if bn.endswith('.R') else 3 if bn.endswith('.L') else None
    if side is None:
        return 0
    if bn.startswith('upperleg'):
        return 1 + side
    if bn.startswith('lowerleg'):
        return 2 + side
    if bn.startswith(('foot', 'toe')):
        return 3 + side
    return 0


def _cloth(R):
    """The trouser shell on the rest body (one closed body still: the same points pushed out): every leg point
    EASE off the skin, and from the knee down no nearer the leg's line than KNEE_CLOTH (the cloth hangs straight from
    the knee, as a trouser leg does; the calf behind it keeps its own shape where it is fuller)."""
    v, J, G = R['v'].copy(), R['J'], R['G']
    for s, cols in (('R', (1, 2)), ('L', (4, 5))):
        legw = G[:, cols[0]] + G[:, cols[1]]
        m = legw > 0.15
        hip, knee, ank = J['hip' + s], J['knee' + s], J['ankle' + s]
        for a, b, lo in ((hip, knee, False), (knee, ank, True)):
            d = b - a
            t = ((v[m] - a) @ d) / (d @ d)
            sel = (t >= 0) & (t <= 1.0)
            idx = np.where(m)[0][sel]
            c = a + np.outer(t[sel], d)
            r = v[idx] - c
            rn = np.linalg.norm(r, axis=1)
            want = rn + EASE
            if lo:
                cl = KNEE_CLOTH * (1 - (1 - HEM_K) * t[sel])          # the leg narrows a little to the hem
                want = np.maximum(want, cl * np.clip(t[sel] * 4, 0, 1) + (rn + EASE) * (1 - np.clip(t[sel] * 4, 0, 1)))
            k = (want / np.maximum(rn, 1e-6))[:, None]
            f = np.clip(legw[idx] * 1.5, 0, 1)[:, None]   # blended out where the leg meets the trunk
            v[idx] = c + r * (1 + (k - 1) * f)
    return v


def _align(a, b):
    return BP._align(a, b)


def _hang(Rs, knee, ank, Tk, Ta):
    """A relaxed hanging foot's turn (MakeHuman frame): the rest foot carried onto the posed shin, then turned about
    the shin so its toes point forward (+z), then tipped down HANG degrees (a foot at rest points a little down)."""
    u2 = _u(ank - knee)
    s = _u(Ta - Tk)
    R1 = _align(u2, s)
    f0 = R1 @ np.array([0.0, 0.0, 1.0])
    f0p = _u(f0 - (f0 @ s) * s)
    z = np.array([0.0, 0.0, 1.0])
    fz = _u(z - (z @ s) * s)
    a = math.radians(HANG)
    f = _u(math.cos(a) * fz + math.sin(a) * s)
    return _align(fz, f) @ _align(f0p, fz) @ R1


def _kit_to_mh(p):
    return np.array([p[0], -p[1], p[2]], float)


def pose(j, sp, cloth=True):
    """Points (N,3) in the kit frame (person units: x across, y down, z forward), triangles, per-point slot weights,
    and the rest points (for the clothes by dot)."""
    import views as V
    R = rest(sp)
    v = R['vc'] if cloth else R['v']
    J, G = R['J'], R['G']
    kit = {'L': 'R', 'R': 'L'}                  # the kit's L (x < 0) is MakeHuman's .R (x < 0)
    T = {}
    for ks, ms in kit.items():
        T['hip' + ms] = _kit_to_mh(j['hip' + ks])
        T['knee' + ms] = _kit_to_mh(V.knee_of(j, ks))
        T['ankle' + ms] = _kit_to_mh(j['foot' + ks])
    leg_rest = np.mean([np.linalg.norm(J['knee' + s] - J['hip' + s]) + np.linalg.norm(J['ankle' + s] - J['knee' + s])
                        for s in 'LR'])
    s0 = (V.THIGH + V.SHIN) / leg_rest          # person units per decimetre
    A = []
    # trunk: rest hip middle -> kit hip middle; across by the hip spacing, else by s0
    h = (J['hipL'] + J['hipR']) / 2
    H_ = (T['hipL'] + T['hipR']) / 2
    sx = np.linalg.norm(T['hipL'] - T['hipR']) / np.linalg.norm(J['hipL'] - J['hipR'])
    lean = math.radians(j.get('lean', 0.0))
    c, sn = math.cos(lean), math.sin(lean)
    Rl = np.array([[1, 0, 0], [0, c, sn], [0, -sn, c]])     # forward lean tips the trunk about the hips
    A.append((Rl @ np.diag([sx, s0, s0]), h, H_))
    rots = {}
    for ms in 'RL':
        a, b = J['hip' + ms], J['knee' + ms]
        Ta, Tb = T['hip' + ms], T['knee' + ms]
        u = _u(b - a)
        Rt = _align(u, Tb - Ta)
        ka = np.linalg.norm(Tb - Ta) / (np.linalg.norm(b - a) * s0)
        A.append((Rt @ (s0 * (np.eye(3) + (ka - 1) * np.outer(u, u))), a, Ta))
        a2, b2 = J['knee' + ms], J['ankle' + ms]
        u2 = _u(b2 - a2)
        Rs = _align(Rt @ u2, T['ankle' + ms] - Tb) @ Rt
        ka2 = np.linalg.norm(T['ankle' + ms] - Tb) / (np.linalg.norm(b2 - a2) * s0)
        A.append((Rs @ (s0 * (np.eye(3) + (ka2 - 1) * np.outer(u2, u2))), a2, Tb))
        top = j.get('cross') == {'R': 'L', 'L': 'R'}[ms]
        if top:                                 # a crossed top leg's foot hangs from the ankle: its sole square to
            Rf = _hang(Rs, J['knee' + ms], J['ankle' + ms], Tb, T['ankle' + ms])   # the shin, toes forward and a
            #                                     little down (chat 7: carried with a turned shin it pointed out sideways:
            #                                     judges, "the crossed shoe floats out to the left")
        else:                                   # a foot on the floor stays flat, turned only about the upright
            yaw = math.radians(j.get('foot_yaw' + {'R': 'L', 'L': 'R'}[ms], 0.0) or 0.0)
            Rf = np.array([[math.cos(yaw), 0, math.sin(yaw)], [0, 1, 0], [-math.sin(yaw), 0, math.cos(yaw)]])
        A.append((Rf * s0, J['ankle' + ms], T['ankle' + ms]))
        rots[ms] = (Rt, Rs)
    # the slots' order in rest(): trunk, thighR, shinR, footR, thighL, shinL, footL
    P = np.zeros((len(v), 3))
    for k, (M, a, t) in enumerate(A):
        P += G[:, k:k + 1] * ((v - a) @ M.T + t)
    P[:, 1] *= -1                               # back to the kit frame (y down)
    seat = j.get('seat')
    sy = _seat_y(j)
    # what rests on the cushion: the bottom and the thighs, never a shin or foot hanging past its front edge (chat 7:
    # the calf behind the knee was lifted onto the rounded edge: a notch in the side view's calf)
    soft = (G[:, 2] + G[:, 3] + G[:, 5] + G[:, 6]) < 0.5
    if seat is not None and sy is not None:     # pressed flat on the cushion where it is under them
        # the cushion's front edge is rounded (EDGE_R): past it the thigh's underside leaves the seat gradually, never a
        # step (side view, chat 6: a notch where the pressed thigh met the free one)
        over, lim = _cushion(P, seat, sy)
        _fit_bottom(P, R, j, sp, sy)
        over, lim = _cushion(P, seat, sy)
        sunk = np.where(over & soft, np.clip(P[:, 1] - lim, 0, SINK_MAX), 0.0)
        _spread(P, R, j, sunk, lim)
    for _ in range(PRESS_ROUNDS):                # the seat and the other leg both press: settled in turn
        if seat is not None and sy is not None:
            over, lim = _cushion(P, seat, sy)
            on = over & soft & (P[:, 1] > lim) & (P[:, 1] < lim + SINK_MAX)
            P[on, 1] = lim[on]
        _press_legs(P, R, j)
    return P, R


def _fit_bottom(P, R, j, sp, sy):
    """The seated bottom as big as the one Sam accepted (v4, views._r7_bottom: figure-drawing measures, 12-13 cm behind
    the hip joints, about 1.15 times the hip width across on the seat; locked, 25 Nov): MakeHuman's standing pelvis is
    smaller (chat 7: 9 cm behind, 30 cm across: the jacket's hem hid it). The trunk below the waist is stretched out
    behind and sideways to that size, fading to nothing at the waist (the flat torso covers it there)."""
    import views as V
    b = np.array([q for q, _ in V._r7_bottom(j, sp, sy)])
    hl, hr = np.array(j['hipL'], float), np.array(j['hipR'], float)
    c = (hl + hr) / 2
    tw = R['G'][:, 0] * (R['arm'] < 0.05)
    low = (tw > 0.5) & (P[:, 1] > c[1])
    if low.sum() < 20:
        return
    back_now = c[2] - P[low, 2].min()
    half_now = np.abs(P[low, 0] - c[0]).max()
    kz = max(1.0, (c[2] - b[:, 2].min()) / back_now)
    kx = max(1.0, (np.abs(b[:, 0] - c[0]).max()) / half_now)
    f = tw * np.clip((P[:, 1] - (c[1] - BOTTOM_FADE)) / BOTTOM_FADE, 0, 1)   # 0 at the waist, 1 from the hips down
    P[:, 0] = c[0] + (P[:, 0] - c[0]) * (1 + (kx - 1) * f)
    behind = P[:, 2] < c[2]
    P[behind, 2] = c[2] + (P[behind, 2] - c[2]) * (1 + (kz - 1) * f[behind])


def _spread(P, R, j, sunk, lim):
    """Flesh pressed on a seat keeps its volume: what the cushion pushes up goes out sideways and back (a seated
    bottom and thighs are wider and deeper at the seat than standing; refs, and the hip breadth seated is about 1.3
    times the standing one). Each point near the seat moves out horizontally by SPREAD times the squash of the flesh
    under it, fading with its height above the seat (SPREAD_H): the bottom from its centre (out and back), a thigh
    from its own bone line (sideways only)."""
    if not (sunk > 0).any():
        return
    from scipy import ndimage
    cell = 16.0
    x0, z0 = P[:, 0].min() - 4 * cell, P[:, 2].min() - 4 * cell
    gx = ((P[:, 0] - x0) / cell).astype(int)
    gz = ((P[:, 2] - z0) / cell).astype(int)
    grid = np.zeros((gx.max() + 1, gz.max() + 1))
    on = sunk > 0
    np.maximum.at(grid, (gx[on], gz[on]), sunk[on])
    grid = ndimage.gaussian_filter(ndimage.maximum_filter(grid, size=5), 2.5)
    D = grid[gx, gz]
    h = np.clip(lim - (P[:, 1] - sunk), 0, None)       # height above the seat once pressed
    amt = SPREAD * D * np.exp(-h / SPREAD_H)
    G = R['G']
    hl, hr = np.array(j['hipL'], float), np.array(j['hipR'], float)
    c = (hl + hr) / 2
    trunk = G[:, 0]
    d_t = np.stack([P[:, 0] - c[0], P[:, 2] - c[2]], 1)
    r = np.linalg.norm(d_t, axis=1)
    d_t *= (np.minimum(r, SPREAD_R) / SPREAD_R / np.maximum(r, 1e-6))[:, None]
    d_t[:, 1] = np.minimum(d_t[:, 1], 0.0)     # out and back only: the lap's front is the thighs (chat 7: the crotch
    #                                            pushed forward showed as a jagged lump between the knees, front view)   # smooth through the middle (chat 7:
    side = _legside(R)                                                            # spikes at the crotch)
    d_l = np.stack([np.tanh((P[:, 0] - np.where(side > 0, hl[0], hr[0])) / SPREAD_R), np.zeros(len(P))], 1)
    d = d_t * trunk[:, None] + d_l * (1 - trunk)[:, None]
    P[:, 0] += amt * d[:, 0]
    P[:, 2] += amt * d[:, 1]


def _legside(R):
    """+1 for the kit's L leg (MakeHuman .R), -1 for the kit's R leg, 0 for the trunk, per point."""
    G = R['G']
    return G[:, 1:4].sum(1) - G[:, 4:7].sum(1)


def _tube(P, j, ks, pts):
    """Distance of pts from leg ks's bone line (kit joints), its place t along hip-knee-ankle (0-2), and that leg's
    own radius at each place (its points' 15th percentile distance there: the cloth's inner side)."""
    import views as V
    segs = ((np.array(j['hip' + ks], float), np.array(V.knee_of(j, ks), float)),
            (np.array(V.knee_of(j, ks), float), np.array(j['foot' + ks], float)))
    best = (np.full(len(pts), np.inf), np.zeros(len(pts)), np.zeros((len(pts), 3)))
    for i, (a, b) in enumerate(segs):
        d = b - a
        t = np.clip(((pts - a) @ d) / (d @ d), 0, 1)
        c = a + t[:, None] * d
        r = np.linalg.norm(pts - c, axis=1)
        m = r < best[0]
        best[0][m], best[1][m], best[2][m] = r[m], t[m] + i, c[m]
    return best


def _press_legs(P, R, j):
    """Legs never pass through each other: where they meet, the soft side gives (as the seat presses the bottom
    flat). Side by side: each leg's points stop at the plane between the knees. Crossed: the top leg's points that
    fall inside the under leg's cloth go out to its surface (the top leg rests ON the under leg)."""
    import views as V
    side = _legside(R)
    kL, kR = np.array(V.knee_of(j, 'L')), np.array(V.knee_of(j, 'R'))
    top = j.get('cross')
    if not top:
        xm = (kL[0] + kR[0]) / 2
        l, r = side > 0.5, side < -0.5
        P[l & (P[:, 0] > xm), 0] = xm
        P[r & (P[:, 0] < xm), 0] = xm
        return
    under = 'R' if top == 'L' else 'L'
    mine = (side > 0.5) if top == 'L' else (side < -0.5)
    oth = (side > 0.5) if under == 'L' else (side < -0.5)
    ro, to, _ = _tube(P, j, under, P[oth])
    bins = np.clip((to * 10).astype(int), 0, 19)
    rad = np.array([np.percentile(ro[bins == i], 85) if (bins == i).sum() > 5 else 0 for i in range(20)])
    idx = np.where(mine)[0]
    rm, tm, c = _tube(P, j, under, P[idx])
    rh = rad[np.clip((tm * 10).astype(int), 0, 19)]
    m = (rm < rh) & (tm > 0.02) & (tm < 1.9)
    d = P[idx[m]] - c[m]
    P[idx[m]] = c[m] + d / np.maximum(np.linalg.norm(d, axis=1), 1e-6)[:, None] * rh[m][:, None]
    # and the under leg gives where the top leg's calf lies over its knee (both are soft: neither passes through)
    ro, to, _ = _tube(P, j, top, P[mine])
    bins = np.clip((to * 10).astype(int), 0, 19)
    rad = np.array([np.percentile(ro[bins == i], 15) if (bins == i).sum() > 5 else 0 for i in range(20)])
    idx = np.where(oth)[0]
    rm, tm, c = _tube(P, j, top, P[idx])
    rh = rad[np.clip((tm * 10).astype(int), 0, 19)]
    m = (rm < rh) & (tm > 0.02) & (tm < 1.9)
    d = P[idx[m]] - c[m]
    P[idx[m]] = c[m] + d / np.maximum(np.linalg.norm(d, axis=1), 1e-6)[:, None] * rh[m][:, None]


def _cushion(P, seat, sy):
    """Which points are over the seat, and the cushion's top under each (its front edge rounded over EDGE_R)."""
    over = (np.abs(P[:, 0]) < seat.width) & (P[:, 2] > seat.rear) & (P[:, 2] < seat.front + EDGE_R)
    return over, sy + np.clip((P[:, 2] - seat.front + EDGE_R) / EDGE_R, 0, None) ** 2 * EDGE_R / 2


def _seat_y(j):
    import views as V
    try:
        return V._r7_seat(j)
    except Exception:
        return None


def _foot_pts(R):
    """The rest body's points below the ankle line: the foot (the shoe takes its place)."""
    J = R['J']
    return (R['v'][:, 1] < min(J['ankleL'][1], J['ankleR'][1]) + 0.25) & (R['arm'] < 0.05)


def _shoes(P, R, foot):
    """Each shoe: the closed hull round that foot's posed points (a smooth shoe: sole, toe cap, heel; the bare
    foot's toes never show; chat 6, the first sheet drew toes)."""
    from scipy.spatial import ConvexHull
    out = []
    side = _legside(R)
    for sg in (1, -1):
        idx = np.where(foot & (side * sg > 0))[0]
        if len(idx) < 4:
            continue
        h = ConvexHull(P[idx])
        out.append(idx[h.simplices])
    return out


def _parts(R, rv):
    """Clothes per dot from the rest point: shoes below the ankle line, trousers from the waist down, skin above."""
    J = R['J']
    ank = min(J['ankleL'][1], J['ankleR'][1])
    y = rv[:, 1]
    part = np.full(len(rv), BD.PART_IX['trousers'])
    part[y < ank + 0.25] = BD.PART_IX['shoes']
    return part


def draw(p, j, yaw, sp, scale=2):
    """The solid lower body into p.img through p.cam (the person's Local), waist down; colours, ink. Keeps the
    layer and its kit-frame depth in LAST for lay_over and the checks."""
    import views as V
    skirt = sp.get('skirt_solid')               # a skirt (the body's own skirt surface) over bare or tighted legs
    P, R = pose(j, sp, cloth=not skirt)
    hip_y = (R['J']['hipL'][1] + R['J']['hipR'][1]) / 2
    keep_pt = (R['v'][:, 1] < hip_y + 1.6) & (R['arm'] < 0.05)   # waist down, no arms (the flat torso covers the cut)
    foot = _foot_pts(R)
    T = R['tris'][keep_pt[R['tris']].all(1) & ~(foot[R['tris']].all(1))]
    T = np.concatenate([T] + [h for h in _shoes(P, R, foot)])
    img = p.img
    Wd, Hd = img.size
    a = math.radians(yaw)
    depth = -P[:, 0] * math.sin(a) + P[:, 2] * math.cos(a)
    sx = P[:, 0] * math.cos(a) + P[:, 2] * math.sin(a)
    sy = P[:, 1] + V._E[0] * depth
    xy = np.array([p.cam.P(x, y) for x, y in zip(sx, sy)], float)
    xy = xy * scale
    z = 3.0 - depth * V.M_PER_UNIT
    zb = np.full((Hd * scale, Wd * scale), np.inf)
    pb = np.full(zb.shape, -1, np.int64)
    ob = np.full(zb.shape, -1, np.int64)
    attrs = np.concatenate([R['v'], P, _legside(R)[:, None]], 1)
    ab = np.zeros(zb.shape + (attrs.shape[1],))
    objs = [T]
    if skirt:                                   # knee length: the surface cut a little below the knee line
        knee_y = (R['J']['kneeL'][1] + R['J']['kneeR'][1]) / 2
        Ts = R['skirt'][(R['v'][R['skirt']][:, :, 1] > knee_y - SKIRT_BELOW).all(1)]
        objs.append(Ts)
    for oi, To in enumerate(objs):
        BD._fill(np.ascontiguousarray(xy), np.ascontiguousarray(z), np.ascontiguousarray(To, np.int64),
                 np.zeros(len(To), np.int64), zb, pb, ob, oi, 0.01, ab, np.ascontiguousarray(attrs), True)
    m = ob >= 0
    pb[ob == 0] = _parts(R, ab[ob == 0][:, :3])
    if skirt:                                   # the body above the hem is under the skirt: it IS the skirt there
        under = (ob == 0) & (ab[..., 1] > knee_y - SKIRT_BELOW)                 # (chat 6: skin showed at the bum and
        ob[under] = 1                                                           # where a crossed thigh left it)
        pb[(ob == 0) & (pb == BD.PART_IX['trousers'])] = BD.PART_IX['skin']    # the legs below it: skin or tights
        pb[ob == 1] = BD.PART_IX['vest']                                        # (the skirt's own part for the ink)
    ls = np.where(ab[..., 6] > 0.5, 1, np.where(ab[..., 6] < -0.5, 2, 0))
    ls[ob != 0] = 0
    edge = BD.ink(zb, pb, ob, max(2, p.w(2.6)) * scale)
    between = np.zeros_like(edge)            # the house line wherever the two legs meet (they are two parts)
    for dy, dx in ((0, 1), (1, 0)):
        a_, b_ = ls[:ls.shape[0] - dy, :ls.shape[1] - dx], ls[dy:, dx:]
        e = (a_ > 0) & (b_ > 0) & (a_ != b_)
        between[:ls.shape[0] - dy, :ls.shape[1] - dx] |= e
    from scipy import ndimage
    edge |= ndimage.binary_dilation(between, iterations=max(1, int(max(2, p.w(2.6)) * scale // 2)))
    cols = {BD.PART_IX['trousers']: tuple(sp.get('trousers', (40, 40, 46))),
            BD.PART_IX['shoes']: tuple(sp.get('shoe', (30, 26, 24))),
            BD.PART_IX['skin']: tuple(sp.get('tights') or sp['skin']), BD.PART_IX['vest']: tuple(skirt or (0, 0, 0))}
    lay = np.zeros(zb.shape + (4,), np.uint8)
    for i, cc in cols.items():
        lay[pb == i, :3] = cc
    # the leg in shadow (the kit's own rule, views._r7_col: a crossed leg's under leg, or a turned view's far leg) at
    # R7_FAR, easing into the lap's tone where the leg joins the body (chat 7, judges at three-quarter: "thighs merge
    # into one dark mass"; v4 Sam accepted drew the far leg so)
    tr = (pb == BD.PART_IX['trousers']) & (ob == 0)
    for ks, sg in (('L', 1.0), ('R', -1.0)):
        dark = V._r7_col(j, sp, ks, yaw)
        base = cols[BD.PART_IX['trousers']]
        if dark == base:
            continue
        w = np.clip((ab[..., 6] * sg - 0.2) / 0.6, 0, 1)[tr]
        k = 1 - (1 - V.R7_FAR) * w
        lay[tr, :3] = (np.array(base, float)[None, :] * k[:, None]).astype(np.uint8)
    lay[m, 3] = 255
    lay[edge & m, :3] = INK
    lay[edge, 3] = 255
    L = Image.fromarray(lay, 'RGBA')
    if scale > 1:
        L = L.resize((Wd, Hd), Image.LANCZOS)
    img.alpha_composite(L) if img.mode == 'RGBA' else img.paste(L, (0, 0), L)
    zk = ab[..., 5][::scale, ::scale]           # kit-frame z (forward) per dot
    LAST.clear()
    LAST.update(layer=L, front=(m & (ab[..., 5] > TORSO_FRONT) & (np.abs(ab[..., 6]) > 0.5))[::scale, ::scale], m=m[::scale, ::scale], zk=zk,
                P=P, T=T, R=R, pb=pb[::scale, ::scale], edge=edge[::scale, ::scale], between=between[::scale, ::scale], ls=ls[::scale, ::scale], j=j, sp=sp, yaw=yaw)
    return L


def lay_over(img, p=None):
    """After the torso: the legs in front of the torso's front drawn over it (no hand-made list of which part:
    depth in the body's own frame decides), inked along the jacket where they leave it."""
    if not LAST:
        return
    from scipy import ndimage
    front = LAST['front']
    if not front.any():
        return
    a = np.asarray(LAST['layer']).copy()
    keep = ndimage.binary_dilation(front, iterations=1)
    a[~keep, 3] = 0
    # the torso: where the picture no longer shows the legs' own layer (it was drawn over them). The cut is inked only
    # where it meets the torso; below the hem the legs run on with no line (chat 7: a line across the thigh at the
    # jacket's front cut the bottom off from the leg in the side view, and the thighs from the lap in the others)
    lay = np.asarray(LAST['layer'])
    now = np.asarray(img.convert('RGBA') if img.mode != 'RGBA' else img)
    torso = LAST['m'] & (np.abs(now[..., :3].astype(int) - lay[..., :3].astype(int)).sum(-1) > 24)
    cut = keep & ~ndimage.binary_erosion(keep, iterations=2) & ~ndimage.binary_dilation(~LAST['m'], iterations=1)
    cut &= ndimage.binary_dilation(torso & ~keep, iterations=3)
    a[cut, :3] = INK
    a[cut, 3] = 255
    L = Image.fromarray(a, 'RGBA')
    img.alpha_composite(L) if img.mode == 'RGBA' else img.paste(L, (0, 0), L)


def checks(j=None, sp=None):
    """The last drawing's faults: seat crossings (points sunk into the cushion past SEAT_SOFT, none by build),
    leg-leg crossings (a point of one leg inside the other leg's cloth), each clothing part one piece."""
    from scipy import ndimage
    out = {}
    P, R, T = LAST['P'], LAST['R'], LAST['T']
    j = LAST['j']
    sy = _seat_y(j)
    seat = j.get('seat')
    if seat is not None and sy is not None:
        over, lim = _cushion(P, seat, sy)
        G = R['G']
        soft = (G[:, 2] + G[:, 3] + G[:, 5] + G[:, 6]) < 0.5
        used = np.zeros(len(P), bool)
        used[np.unique(T)] = True
        # the bottom and thighs sunk into the cushion past SEAT_SOFT (any depth); a shin or foot inside the cushion's
        # block (its top to SEAT_BLOCK under it, behind its front edge) (chat 7: shins hanging past the rounded edge
        # are below it, not in it)
        sink = used & over & soft & (P[:, 1] > lim + SEAT_SOFT)
        shin = used & ~soft & (P[:, 2] < seat.front) & (np.abs(P[:, 0]) < seat.width) & (P[:, 1] > sy + SEAT_SOFT) \
            & (P[:, 1] < sy + SEAT_BLOCK)
        out['seat crossings'] = int(sink.sum() + shin.sum())
    # leg against leg: each leg's points against the other's cloth (distance to its bone line below its own radius)
    G = R['G']
    J = R['J']
    used = np.unique(T)
    n = 0
    import views as V
    side = _legside(R)
    for ks, oks in (('L', 'R'), ('R', 'L')):
        mine = used[(side[used] > 0.6) if ks == 'L' else (side[used] < -0.6)]
        oth = used[(side[used] > 0.6) if oks == 'L' else (side[used] < -0.6)]
        ro, to, _ = _tube(P, j, oks, P[oth])        # the other leg's own radius along its bone line (its thinnest
        bins = np.clip((to * 10).astype(int), 0, 19)   # side at each place: the 15th percentile)
        rad = np.array([np.percentile(ro[bins == i], 15) if (bins == i).sum() > 5 else 0 for i in range(20)])
        rm, tm, _ = _tube(P, j, oks, P[mine])
        rh = rad[np.clip((tm * 10).astype(int), 0, 19)]
        n += int(((rm < rh - TOUCH) & (tm > 0.05) & (tm < 1.9)).sum())   # touching is not crossing (bench TOUCH)
    out['leg-leg crossings'] = n
    # each clothing part one piece: on the mesh (triangles of one part joined by shared points), and in the picture
    pb = LAST['pb']
    for nm, most in (('trousers', 1), ('shoes', 2)):
        lab, k = ndimage.label(pb == BD.PART_IX[nm])
        sizes = np.bincount(lab.ravel())[1:]
        big = int((sizes > max(40, sizes.max() * 0.01)).sum()) if k else 0
        out[nm + ' pieces (picture)'] = big if big > most else 0
    return out
