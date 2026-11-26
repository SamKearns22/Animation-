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
SPREAD_FRONT = 70.0     # ... a thigh's spread fading to none over this distance to the seat's front edge (chat 14)
SPREAD_H = 40.0         # ... fading over this height above the seat (6 cm)
SINK_MAX = 90.0         # deeper than this under the cushion's top is below the seat, not on it (14 cm)
NECK_X = 1.0             # mode 'whole': the neck's width over the measured body's (the trunk eases to it above the shoulders)
NECK_LIFT = 40.0         # mode 'whole': the shoulders' tops and the neck's base raised this far (person units, 6 cm)
SHOE_HEM = True          # mode 'body': no bare foot under the shoe (chat 10, Sam's shoe notes; kittest shoe_shapes)
HEM_FILL = 6             # mode 'body': the largest fleck (dots) between hem and shoe the hem covers (chat 10)
SEAT_TROUSERS = True     # mode 'body': the trunk below the flat jacket's seated hem is trousers (chat 10; kittest
#                          jacket_under_hem switches it off to prove its check catches Sam's purple bottom)
HEM_OVERLAP = 20.0       # mode 'body': the solid starts this far (person units) above the flat jacket's hem (no gap)
BODY_TOP = 2.2           # mode 'body': the solid body stops this far (rest dm) below the shoulder joints (the
#                          waist: at 1.0 the bust showed past the flat jacket's front from the side, chat 8)
V_BUTTON = 0.72          # mode 'whole', her jacket: the V closes this share of the way from hips to shoulders (the
#                          flat May's: at mid chest; chat 8 had 0.42, an opening to the waist: Sam "you changed her clothes?")
LAPEL_X, SEAM_W = 1.05, 0.022   # her lapel's outer edge at the collar (rest dm off the middle); a drawn seam's half width
STRIPE_W, STRIPE_WAVE = 0.09, 0.035   # the patterned blouse's stripes: width and wave (rest dm; pattern_torso's 7 and 3 units)
ARM_SEAM = 0.6           # mode 'whole': the arm's own line stops this far (rest dm) below the shoulder joint
ARM_X = 1.25             # mode 'whole': a sleeve's thickness over the measured arm's (the house arm is stretched
#                          about 1.4 along: at 1.0 judges saw 'thin stiff tubes', chat 8)
HAND_R, HAND_OUT = 26.0, 12.0   # the house circle hand (satire_style.install_circle_hands): radius, past the wrist
HANG = 25.0             # a crossed top leg's foot tips this far down from square to its shin (relaxed)
SEAT_BLOCK = 40.0       # the cushion's thickness under its top (6 cm): a shin inside it crosses the seat
SEAT_SOFT = 6.0         # the bottom and thighs pressed flat on the seat: nothing deeper than this into the cushion
_REST = {}
LAST = {}
WHOLE_IX = {'jacket': 'body', 'shirt': 'dash', 'pocket': 'dash', 'pin': 'dash'}   # model_body's suit parts -> part ids here


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


def pose(j, sp, cloth=True, whole=False):
    """Points (N,3) in the kit frame (person units: x across, y down, z forward), triangles, per-point slot weights,
    and the rest points (for the clothes by dot). whole: the trunk, neck and arms too (_upper), not only the legs."""
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
    if whole:                                   # the trunk slot (arms ride on it) replaced by trunk, neck and arms
        M0, a0, t0 = A[0]
        P += _upper(j, sp, v, J, h, H_, sx, s0, Rl) - G[:, :1] * ((v - a0) @ M0.T + t0)
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


def _upper(j, sp, v, J, h, H_, sx, s0, Rl):
    """Mode 'whole' (Sam's pick, 25 Nov, option 2): the trunk, neck and arms of the measured body on the kit's own
    upper joints (MakeHuman frame, y up), weighted by model_body's twelve slots on the same points. The trunk keeps the
    legs' scale below the hips (so the seat, bottom and legs are exactly as in mode 'legs') and is stretched above
    them to the kit's shoulders (the house figure: a longer trunk and wider shoulders than the measured body), easing
    from the hip width to the shoulder width; the neck narrows back (NECK_X); each arm aimed and stretched to the
    kit's shoulder, elbow and wrist (leaned with the body, as views draws the flat arm)."""
    import views as V
    import model_body as MB
    M = MB.rest(sp)
    G12, J12 = M['G'], M['J']
    lean = j.get('lean', 0.0)
    T = {}
    for ks, ms in (('L', 'R'), ('R', 'L')):    # the kit's L (x < 0) is MakeHuman's .R
        for n in ('sh', 'el', 'wr'):
            T[n + ms] = _kit_to_mh(V.leaned(j[n + ks], lean))
    sh_r = (J12['shL'] + J12['shR']) / 2
    sh_k = (T['shL'] + T['shR']) / 2
    kt = (sh_k[1] - H_[1]) / ((sh_r[1] - h[1]) * s0)       # the house trunk's length over the body's
    sxs = (T['shL'][0] - T['shR'][0]) / (J12['shL'][0] - J12['shR'][0])   # across at the shoulders
    d = v - h
    u = np.clip(d[:, 1] / (sh_r[1] - h[1]), 0, 1)
    nk = np.clip((d[:, 1] - (sh_r[1] - h[1])) / max(1e-6, J12['neck'][1] - sh_r[1]), 0, 1)
    ax = (sx + (sxs - sx) * u) * (1 - nk) + s0 * NECK_X * nk
    # deep as it is wide (chat 8 judges, side view: stretched up and across but not front to back, "torso very thin,
    # tube-like", the head thrust forward of a flat chest): the depth keeps the body's own depth-to-width ratio
    az = ax * (s0 / sx) * (1 - nk) + s0 * NECK_X * nk
    tq = np.stack([d[:, 0] * ax, s0 * (d[:, 1] + (kt - 1) * np.maximum(d[:, 1], 0)), d[:, 2] * az], 1) @ Rl.T + H_
    out = (G12[:, 0:1] + G12[:, 1:2]) * tq       # trunk and neck
    for ms in 'LR':
        sh_t = T['sh' + ms]
        for slot, a, b, ta, tb in (('arm', 'sh', 'el', sh_t, T['el' + ms]), ('fore', 'el', 'wr', T['el' + ms], T['wr' + ms])):
            Ma, a0, a1 = MB._aim(J12[a + ms], J12[b + ms], ta, tb, s0 * ARM_X)
            k = MB.SLOTS.index(slot + ms)
            out += G12[:, k:k + 1] * ((v - a0) @ Ma.T + a1)
    # the house figure's shoulders sit high and square under the chin: everything above the shoulder joints (the
    # neck's base, the trapezius, the shoulders' tops) raised NECK_LIFT, eased in over the half decimetre below them
    # (chat 8, first sheet: a long bare neck between the chin and low sloping shoulders)
    r = np.clip((d[:, 1] - (sh_r[1] - h[1]) + 0.5) / 0.5, 0, 1)
    up = 1.0 - G12[:, 6:].sum(1)                  # not the legs
    out[:, 1] += NECK_LIFT * r * r * (3 - 2 * r) * up
    return out


def hands(j, sp):
    """The house circle hands as solid balls (kit frame): HAND_OUT past each wrist along the forearm, HAND_R round
    (satire_style's circle hand), so what hides a hand (a knee in front of it, the body) is decided by depth."""
    import views as V
    lean = j.get('lean', 0.0)
    out = []
    for sd in 'LR':
        el = np.array(V.leaned(j['el' + sd], lean), float)
        wr = np.array(V.leaned(j['wr' + sd], lean), float)
        c = wr + _u(wr - el) * HAND_OUT
        out.append(BD._ball(c, HAND_R, 16))
    return out


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
    seat = j.get('seat')
    if seat is not None and SPREAD_FRONT:      # R7 chat 14 (Sam's note 4: "knee to calf area could have smoother, less
        d_l *= np.clip((seat.front - P[:, 2]) / SPREAD_FRONT, 0, 1)[:, None]   # rugged lines"): little flesh to
        #                                        squash near the knee: the thigh's spread fades out before the seat's
        #                                        front edge (it bulged past the knee there, a lobe over the shin)
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
        g = 0.5 * (j.get('spec') or {}).get('leg_gap', 0.0)   # R7 chat 11 ('upright, apart'; Sam, 26 Nov: "a small
        #   gap that runs all the way down"): relaxed legs apart stop short of each other by this much, crotch to knee
        l, r = side > 0.5, side < -0.5
        P[l & (P[:, 0] > xm - g), 0] = xm - g
        P[r & (P[:, 0] < xm + g), 0] = xm + g
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


SHOE_LINE = 0.25         # the shoe's top over the ankle joint (decimetres); mode 'body' uses SHOE_LINE_BODY:
SHOE_LINE_BODY = -0.12   # a low court shoe, the trouser leg down over the ankle (Sam, 26 Nov, the hoof-high shoe:
#                          "Confused shoe shapes on side view")


def _foot_pts(R, line=None):
    """The rest body's points below the ankle line: the foot (the shoe takes its place)."""
    J = R['J']
    return (R['v'][:, 1] < min(J['ankleL'][1], J['ankleR'][1]) + (SHOE_LINE if line is None else line)) \
        & (R['arm'] < 0.05)


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
    mode = sp.get('seat_solid')
    whole = mode in ('whole', 'body')           # 'body' (Sam, chat 8): the whole solid body under the person's own
    arms = mode == 'whole'                      # flat outfit (views draws the torso, sleeves and hands over it as in
    P, R = pose(j, sp, cloth=not skirt, whole=whole)   # every film): no solid arms or hands, so never two pairs
    foot = _foot_pts(R, SHOE_LINE_BODY if (mode == 'body' and SHOE_HEM) else None)
    if whole:                                   # the whole person: every point but the head and hands (the house
        import model_body as MB                 # head and circle hands are drawn instead: views, and hands() here)
        M = MB.rest(sp)
        T = M['T_feet'] if (not arms and SHOE_HEM) else M['T']   # mode 'body': the leg down to its own shoe line
        if not arms:                            # under the flat outfit: no arms, and nothing above the chest (the
            sh_y = (M['J']['shL'][1] + M['J']['shR'][1]) / 2   # outfit's own neck and collar; chat 8: the solid neck
            low = (R['arm'] < 0.05) & (R['v'][:, 1] < sh_y - BODY_TOP)   # showed between the chin and the collar)
            T = T[low[T].all(1)]
        if SHOE_HEM:                            # the bare foot and the band of mixed triangles at the ankle never
            T = T[~foot[T].all(1)]              # drawn: the shoe's hull is the shoe, the leg's last row (cut at the
            #                                     shoe line by colour, below) meets it with no gap; the trouser leg ends in a
        #                                         clean ring over it (Sam, 26 Nov: "Shoes clipping on 3/4 view",
        #                                         "Confused shoe shapes on side view": the shin poked through the shoe)
        grp = M['grp']
    else:
        hip_y = (R['J']['hipL'][1] + R['J']['hipR'][1]) / 2
        keep_pt = (R['v'][:, 1] < hip_y + 1.6) & (R['arm'] < 0.05)   # waist down, no arms (the flat torso covers the cut)
        T = R['tris'][keep_pt[R['tris']].all(1) & ~(foot[R['tris']].all(1))]
        grp = np.zeros((len(P), 5))
    T = np.concatenate([T] + [h for h in _shoes(P, R, foot)])
    hand_objs = []
    if arms:
        for Ph, Th in hands(j, sp):
            hand_objs.append(Th + len(P))
            P = np.concatenate([P, Ph])
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
    nv = len(R['v'])
    if whole:                                   # which arm a point is on (+1 MakeHuman's .L, -1 .R, 0 neither)
        G12 = M['G']
        armside = (G12[:, 2] + G12[:, 4]) - (G12[:, 3] + G12[:, 5])
    else:
        armside = np.zeros(nv)
    attrs = np.concatenate([R['v'], P[:nv], _legside(R)[:, None], grp, armside[:, None]], 1)
    if len(P) > nv:                             # the hands' balls: no rest point of their own (their object says hand)
        attrs = np.concatenate([attrs, np.zeros((len(P) - nv, attrs.shape[1]))], 0)
        attrs[nv:, 3:6] = P[nv:]
    ab = np.zeros(zb.shape + (attrs.shape[1],))
    objs = [T]
    if skirt:                                   # knee length: the surface cut a little below the knee line
        knee_y = (R['J']['kneeL'][1] + R['J']['kneeR'][1]) / 2
        Ts = R['skirt'][(R['v'][R['skirt']][:, :, 1] > knee_y - SKIRT_BELOW).all(1)]
        objs.append(Ts)
    if whole:
        objs.append(np.zeros((0, 3), int))      # (object 1 is the skirt's)
        objs += hand_objs                       # objects 2, 3: the hands
    for oi, To in enumerate(objs):
        if not len(To):
            continue
        BD._fill(np.ascontiguousarray(xy), np.ascontiguousarray(z), np.ascontiguousarray(To, np.int64),
                 np.zeros(len(To), np.int64), zb, pb, ob, oi, 0.01, ab, np.ascontiguousarray(attrs), True)
    m = ob >= 0
    if mode == 'body' and SMOOTH_R:             # R7 chat 14 (Sam, 26 Nov, notes 3-4: "knee to calf area could have
        _smooth(zb, pb, ob, ab, SMOOTH_R * scale)   # smoother, less rugged lines"; the crotch's ragged ends): each leg's
        m = ob >= 0                             # and the trunk's outline smoothed (notches filled, steps rounded)
    if whole:                                   # the suit per dot (model_body.suit_parts), in this drawing's part ids
        # her jacket buttoned with a V (the flat kit's women's jackets), his open over the shirt, unless the spec says
        mp = MB.suit_parts(ab[ob == 0][:, :3], ab[ob == 0][:, 7:12], M,
                           dict(sp, jacket_open=sp.get('jacket_open', not woman(sp)),
                                v_button=sp.get('v_button', V_BUTTON if woman(sp) else 0.35)))
        name = {v_: k_ for k_, v_ in MB.PIX.items()}
        pb[ob == 0] = [BD.PART_IX[WHOLE_IX.get(name[q], name[q])] for q in mp]
        pb[ob >= 2] = BD.PART_IX['hand']
        if not arms and SHOE_HEM:               # the shoe's hull is all shoe, at _foot_pts' own ankle line (the suit's
            ank = min(R['J']['ankleL'][1], R['J']['ankleR'][1]) + SHOE_LINE_BODY   # line is higher: a trouser wedge)
            sh = (ob == 0) & (ab[..., 1] < ank + 0.02)
            pb[sh & (pb == BD.PART_IX['trousers'])] = BD.PART_IX['shoes']
            pb[(ob == 0) & ~sh & (pb == BD.PART_IX['shoes'])] = BD.PART_IX['trousers']   # the leg over the ankle
        if not arms and SHOE_HEM:               # the hem covers the shoe's top: a fleck of background (up to HEM_FILL
            TRx, SHx = BD.PART_IX['trousers'], BD.PART_IX['shoes']   # dots) between a trouser dot and the shoe under
            for c in np.where((pb == SHx).any(0))[0]:                # it is trousers (chat 10: the hanging foot's
                col = np.where(ob[:, c] == 0, pb[:, c], -1)           # heel, tipped HANG, left a sliver)
                ys = np.where(col == SHx)[0]
                tr = np.where(col[:ys[0]] == TRx)[0]
                if len(tr) and 1 < ys[0] - tr[-1] <= HEM_FILL * scale and (col[tr[-1] + 1:ys[0]] == -1).all():
                    r = slice(tr[-1] + 1, ys[0])
                    ob[r, c], pb[r, c], m[r, c] = 0, TRx, True
                    ab[r, c] = ab[tr[-1], c]
        if not arms and SEAT_TROUSERS:          # under the flat outfit (mode 'body'): below the flat jacket's seated
            low = (ob == 0) & (ab[..., 4] >= min(sp.get('bottom') or V.JACKET, 470) - HEM_OVERLAP)   # hem the
            #                                     trunk is her (from where it shows: chat 14, Sam's note 2, the jacket's
            #                                     part line at the hem showed as a stray line across Kemi's bottom)
            pb[low & (pb != BD.PART_IX['shoes'])] = BD.PART_IX['trousers']   # trousers' seat, never the solid's own
            #                                     jacket (Sam, 25 Nov, side view: "Is this bottom purple section
            #                                     supposed to be there or is it supposed to be trousers"; chat 10)
    else:
        pb[ob == 0] = _parts(R, ab[ob == 0][:, :3])
    if skirt:                                   # the body above the hem is under the skirt: it IS the skirt there
        under = (ob == 0) & (ab[..., 1] > knee_y - SKIRT_BELOW)                 # (chat 6: skin showed at the bum and
        ob[under] = 1                                                           # where a crossed thigh left it)
        pb[(ob == 0) & (pb == BD.PART_IX['trousers'])] = BD.PART_IX['skin']    # the legs below it: skin or tights
        pb[ob == 1] = BD.PART_IX['vest']                                        # (the skirt's own part for the ink)
    ls = np.where(ab[..., 6] > 0.5, 1, np.where(ab[..., 6] < -0.5, 2, 0))
    ls[ob != 0] = 0
    if mode == 'body':                          # R7 chat 14 (Sam, 26 Nov, note 2: "Stray horizontal line on butt"):
        soft = np.where((ob == 0) & (ls == 0), 1, 0)
        if sp.get('legs_soft'):                 # pose-test (26 Nov, standing and running on the body: a loose crease tick
            soft = np.where(ob == 0, ls + 1, 0)  # inside a bent knee): each leg one soft mass too (only specs that ask)
        edge = _ink(zb, pb, ob, max(2, p.w(2.6)) * scale, soft)   # the trunk is one soft mass:
    else:                                       # no line where it folds over itself (the seat-pressed bottom bulging
        edge = BD.ink(zb, pb, ob, max(2, p.w(2.6)) * scale)   # sideways); its outline and the legs' lines stay
    between = np.zeros_like(edge)            # the house line wherever the two legs meet (they are two parts)
    for dy, dx in ((0, 1), (1, 0)):
        a_, b_ = ls[:ls.shape[0] - dy, :ls.shape[1] - dx], ls[dy:, dx:]
        e = (a_ > 0) & (b_ > 0) & (a_ != b_)
        between[:ls.shape[0] - dy, :ls.shape[1] - dx] |= e
    if whole:                                   # an arm against the body is its own shape: the house line round
        J12 = M['J']                             # it wherever it lies on the trunk or the other arm, but never
        sh_y = (J12['shL'][1] + J12['shR'][1]) / 2   # across the shoulder's top, where the arm grows out of the body
        lab = np.where(ab[..., 12] > 0.5, 1, np.where(ab[..., 12] < -0.5, 2, 3))
        lab[(ob != 0) | ~m] = 0
        low = ab[..., 1] < sh_y - ARM_SEAM
        for dy, dx in ((0, 1), (1, 0)):
            a_, b_ = lab[:lab.shape[0] - dy, :lab.shape[1] - dx], lab[dy:, dx:]
            la, lb = low[:low.shape[0] - dy, :low.shape[1] - dx], low[dy:, dx:]
            e = (a_ > 0) & (b_ > 0) & (a_ != b_) & la & lb
            between[:lab.shape[0] - dy, :lab.shape[1] - dx] |= e
    from scipy import ndimage
    if mode == 'body':                          # R7 chat 14 (Sam's note 3, the tick in the crotch): where the legs only
        lb, nb = ndimage.label(between, structure=np.ones((3, 3)))   # touch deep in a gap (a few dots), no line
        if nb:
            sz = ndimage.sum(between, lb, range(1, nb + 1))
            between &= np.isin(lb, 1 + np.where(sz >= BETWEEN_MIN * scale)[0])
    edge |= ndimage.binary_dilation(between, iterations=max(1, int(max(2, p.w(2.6)) * scale // 2)))
    if mode == 'body':                          # R7 chat 14 (Sam's note 3): a speck of ink on its own (a tiny ring
        le, ne = ndimage.label(edge, structure=np.ones((3, 3)))   # where folds meet in the crotch) is no line
        if ne:
            sz = ndimage.sum(edge, le, range(1, ne + 1))
            edge &= np.isin(le, 1 + np.where(sz >= SPECK * scale * scale)[0])
    cols = {BD.PART_IX['trousers']: tuple(sp.get('trousers', (40, 40, 46))),
            BD.PART_IX['shoes']: tuple(sp.get('shoe', (30, 26, 24))),
            BD.PART_IX['skin']: tuple(sp.get('tights') or sp['skin']), BD.PART_IX['vest']: tuple(skirt or (0, 0, 0)),
            BD.PART_IX['body']: tuple(sp.get('jacket', (40, 40, 46))), BD.PART_IX['dash']: tuple(sp.get('shirt', (246,) * 3)),
            BD.PART_IX['hand']: tuple(sp.get('glove', sp['skin']))}
    if whole:                                   # the neck and face's skin is the person's own, never tights
        cols[BD.PART_IX['skin']] = tuple(sp['skin'])
    lay = np.zeros(zb.shape + (4,), np.uint8)
    for i, cc in cols.items():
        lay[pb == i, :3] = cc
    # the leg in shadow (the kit's own rule, views._r7_col: a crossed leg's under leg, or a turned view's far leg) at
    # R7_FAR, easing into the lap's tone where the leg joins the body (chat 7, judges at three-quarter: "thighs merge
    # into one dark mass"; v4 Sam accepted drew the far leg so)
    tr = (pb == BD.PART_IX['trousers']) & (ob == 0)
    far_ls = []
    for ks, sg in (('L', 1.0), ('R', -1.0)):
        dark = V._r7_col(j, sp, ks, yaw)
        base = cols[BD.PART_IX['trousers']]
        if dark == base:
            continue
        if mode == 'body':                          # R7 chat 14 (Sam, 26 Nov, note 1: "In 3/4 pose the legs are
            if not j.get('cross'):                  # different colour"): both legs one cloth (the line between them
                far_ls.append(1 if ks == 'L' else 2)   # (side by side only: the far leg also goes under the hem)
            continue                                # parts them); chat 15 (note 7: "On the crossed legs, they are
            #                                         still different colors"): crossed too, every pose
        w = np.clip((ab[..., 6] * sg - 0.2) / 0.6, 0, 1)[tr]
        k = 1 - (1 - V.R7_FAR) * w
        lay[tr, :3] = (np.array(base, float)[None, :] * k[:, None]).astype(np.uint8)
    if whole and 'pattern' in (sp.get('kit_extras') or ()):   # her patterned blouse (people_parts.pattern_torso:
        import people_parts as PPa                   # wavy upright stripes, no outlines), laid on the rest body so
        pc = np.array(sp.get('pattern') or PPa.BLOUSE_STRIPES, np.uint8)   # the stripes turn with her (Sam, chat 8:
        sh_m = (pb == BD.PART_IX['dash']) & (ob == 0)                      # "you changed her clothes?")
        xr, yr = ab[..., 0][sh_m], ab[..., 1][sh_m]
        k = np.floor((xr + STRIPE_WAVE * np.sin(yr / 0.28)) / STRIPE_W).astype(int) % len(pc)
        lay[sh_m, :3] = pc[k]
    if whole and woman(sp):                     # her jacket's lapels and the front closing below the V, as the flat
        J12 = M['J']                             # jacket draws them (Sam, chat 8: "you changed her clothes?")
        sh_y = (J12['shL'][1] + J12['shR'][1]) / 2
        collar, button = J12['neck'][1] - 0.35, sh_y * V_BUTTON
        jk = (pb == BD.PART_IX['body']) & (ob == 0) & (ab[..., 2] > 0.3) & (ab[..., 7] > 0.5)
        xr, yr = np.abs(ab[..., 0]), ab[..., 1]
        u = np.clip((collar - yr) / (collar - button), 0, 1)
        lapel = jk & (yr <= collar) & (yr >= button) & (np.abs(xr - (LAPEL_X * (1 - u) + 0.12 * u)) < SEAM_W)
        close = jk & (yr < button) & (xr < SEAM_W)
        lay[lapel | close, :3] = INK
    lay[m, 3] = 255
    lay[edge & m, :3] = INK
    lay[edge, 3] = 255
    if whole and not arms:                      # under the flat outfit, only what lies below its jacket's seated hem
        hem = min(sp.get('bottom') or V.JACKET, 470) - HEM_OVERLAP   # shows (kit y, down): no cut edge of the solid
        lay[(ab[..., 4] < hem) & (np.abs(ab[..., 6]) < 0.5), 3] = 0   # waist or bust past the jacket (chat 8: a tab
        #                                         and a notch); never the legs (their tops lie above the hem's line)
        lay[~m, 3] = np.where(edge[~m], lay[~m, 3], 0)
    L = Image.fromarray(lay, 'RGBA')
    if scale > 1:
        L = L.resize((Wd, Hd), Image.LANCZOS)
    img.alpha_composite(L) if img.mode == 'RGBA' else img.paste(L, (0, 0), L)
    zk = ab[..., 5][::scale, ::scale]           # kit-frame z (forward) per dot
    LAST.clear()
    LAST.update(mode=mode, whole=arms, far_ls=far_ls, layer=L, front=(m & (ab[..., 5] > TORSO_FRONT) & (np.abs(ab[..., 6]) > 0.5))[::scale, ::scale], m=m[::scale, ::scale], zk=zk,
                P=P[:nv], T=T, R=R, pb=pb[::scale, ::scale], edge=edge[::scale, ::scale], between=between[::scale, ::scale], ls=ls[::scale, ::scale], j=j, sp=sp, yaw=yaw,
                shown=(lay[..., 3] > 0)[::scale, ::scale], ky=ab[..., 4][::scale, ::scale], foot=foot)
    return L


BETWEEN_MIN = 14        # mode 'body': a line between the legs shorter than this (dots at 1x) is not drawn (chat 14)
SPECK = 60              # mode 'body': an ink piece smaller than this (dots at 1x) is a speck, not drawn (chat 14)
SMOOTH_R = 5.0          # mode 'body': outline smoothing radius (picture dots at 1x; chat 14)


def _smooth(zb, pb, ob, ab, r):
    """Each piece of the solid (either leg, the trunk) smoothed in the picture: notches narrower than about 2r filled
    and stair steps rounded (a disc closing, then a blur over r/2 held at half); filled dots take their nearest dot's
    depth and attributes, dots shaved off become empty. Pieces never grow into each other (the gap between apart
    legs stays)."""
    from scipy import ndimage
    o0 = ob == 0
    lab = np.where(ab[..., 6] > 0.5, 1, np.where(ab[..., 6] < -0.5, 2, 3))
    lab[~o0] = 0
    yy, xx = np.mgrid[-int(r):int(r) + 1, -int(r):int(r) + 1]
    disc = (yy ** 2 + xx ** 2) <= r * r
    any_obj = ob >= 0
    for k in (1, 2, 3):
        L = lab == k
        if L.sum() < 50:
            continue
        others = ndimage.binary_dilation(any_obj & ~L, iterations=2)
        Ls = ndimage.binary_closing(L, structure=disc)
        Ls = ndimage.gaussian_filter(Ls.astype(float), r / 2) > 0.5
        add = Ls & ~any_obj & ~others
        cut = L & ~Ls & ~others
        if add.any():
            _, (iy, ix) = ndimage.distance_transform_edt(~L, return_indices=True)
            ty, tx = iy[add], ix[add]
            zb[add], pb[add], ob[add], ab[add] = zb[ty, tx], pb[ty, tx], ob[ty, tx], ab[ty, tx]
            any_obj = ob >= 0
        if cut.any():
            zb[cut], pb[cut], ob[cut], ab[cut] = np.inf, -1, -1, 0


FOLD_MIN = 40           # mode 'body': a fold line (a depth jump inside one part) shorter than this many dots (at the
#                         drawing's 2x) that meets other ink at one place only is not drawn (Open Wounds chat 27:
#                         May's back calf over its thigh, a crease fading out in the open: a loose tick; the stubs
#                         there were 1-26 dots, the real fold lines 64 and up; kittest fold_stub)
FOLD_LOG = []           # each drawing's dropped folds' sizes (for the kittest)


def _ink(zb, pb, ob, width, soft, fold_min=None):
    """bench_draw.ink, but a depth jump between two dots of the same `soft` piece (a label above 0) is no line (one
    soft mass folding over itself: the trunk, each leg). fold_min: a fold (a jump inside one part, not on an
    outline or a part's edge) whose own piece of line is shorter than this is dropped: every house line closes or
    meets another along its length, never a stub fading out (kittest stray_ink)."""
    h, w = zb.shape
    fold_min = FOLD_MIN if fold_min is None else fold_min
    fold = np.zeros((h, w), bool)
    edge = np.zeros((h, w), bool)
    zf = np.where(np.isfinite(zb), zb, 1e3)
    pb = BD.INK_PART[np.clip(pb, -1, len(BD.PART_NAMES) - 1) + 1]
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        a = (slice(0, h - dy), slice(max(0, -dx), w - max(0, dx)))
        b = (slice(dy, h), slice(max(0, dx), w + min(0, dx)))
        jump = np.abs(zf[a] - zf[b]) > 0.03 + 0.02 * np.minimum(zf[a], zf[b]) / 4
        diff = (ob[a] != ob[b]) | (pb[a] != pb[b]) | (jump & ~((soft[a] > 0) & (soft[a] == soft[b])))
        near_a = zf[a] <= zf[b]
        hard = (ob[a] != ob[b]) | (pb[a] != pb[b])
        edge[a] |= hard & near_a & (ob[a] >= 0)
        edge[b] |= hard & ~near_a & (ob[b] >= 0)
        jf = diff & ~hard
        fold[a] |= jf & near_a & (ob[a] >= 0)
        fold[b] |= jf & ~near_a & (ob[b] >= 0)
    if fold_min:                                # a short fold that meets other ink at one place only (a stub
        from scipy import ndimage               # fading out in the open); a piece of a longer line between two
        own = fold & ~edge                      # others (a crossed leg's line, broken by the part edges) stays
        lab, n = ndimage.label(ndimage.binary_dilation(own, iterations=2), structure=np.ones((3, 3)))
        lab = np.where(own, lab, 0)
        size = ndimage.sum(own, lab, np.arange(1, n + 1)) if n else []
        dropped = []
        for i, sz in enumerate(size, 1):
            if sz >= fold_min:
                continue
            ys, xs = np.where(lab == i)
            y0, y1, x0, x1 = max(0, ys.min() - 8), ys.max() + 9, max(0, xs.min() - 8), xs.max() + 9
            me = lab[y0:y1, x0:x1] == i
            ring = ndimage.binary_dilation(me, iterations=4) & ~me
            other = (edge[y0:y1, x0:x1] | (fold[y0:y1, x0:x1] & ~me)) & ring
            if ndimage.label(other, structure=np.ones((3, 3)))[1] < 2:
                fold[y0:y1, x0:x1] &= ~me
                dropped.append(int(sz))
        FOLD_LOG.append(dropped)
    edge |= fold
    if width > 1:
        from scipy import ndimage
        edge = ndimage.binary_dilation(edge, iterations=int(width // 2))
    return edge


def lay_over(img, p=None):
    """After the torso: the legs in front of the torso's front drawn over it (no hand-made list of which part:
    depth in the body's own frame decides), inked along the jacket where they leave it."""
    if not LAST or LAST.get('whole'):           # (mode 'whole': no flat torso to lie over)
        return
    from scipy import ndimage
    front = LAST['front'].copy()
    for f in LAST.get('far_ls') or ():          # R7 chat 14 (Sam's note 1: the far leg "doesn't seem connected smoothly
        front &= LAST['ls'] != f                # to the body"): side by side, the far leg goes under the hem, never over
    if not front.any():                         # it (its top showed over the jacket as a notched lump)
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


SHOE_TALL = 0.36   # a shoe's height over its length (rest body): above it, an ankle-high hoof (chat 10)


def shoe_faults():
    """R7 chat 10 (Sam, 26 Nov: "Shoes clipping on 3/4 view", "Confused shoe shapes on side view";
    examples/sam-26nov-shoes-clipping-34.jpg, sam-26nov-shoe-shapes-side.jpg): in the last drawing, columns where
    trousers show below a shoe (the shin poking through it) or a gap between the trouser hem and the shoe, and a shoe
    taller than SHOE_TALL of its length. Returns the faults as text (empty: none)."""
    pb, shown, R, foot = LAST['pb'], LAST['shown'], LAST['R'], LAST['foot']
    TR, SH = BD.PART_IX['trousers'], BD.PART_IX['shoes']
    poke = gap = 0
    for c in range(pb.shape[1]):
        col = np.where(shown[:, c], pb[:, c], -1)
        ys = np.where(col == SH)[0]
        if not len(ys):
            continue
        poke += int(((col == TR) & (np.arange(len(col)) > ys[0] + 1)).sum() > 2)
        tr = np.where(col[:ys[0]] == TR)[0]
        gap += int(len(tr) and 1 < (col[tr[-1] + 1:ys[0]] == -1).sum() <= 8)   # a fleck, not the toe ahead of a shin
    out = []
    if poke > 3:
        out.append('trousers through the shoe in %d columns' % poke)
    if gap > 3:
        out.append('gap between hem and shoe in %d columns' % gap)
    v = R['v'][foot]
    if len(v):
        for sg in (1, -1):
            f = v[v[:, 0] * sg > 0]
            if len(f) > 3:
                k = (f[:, 1].max() - f[:, 1].min()) / max(1e-6, np.ptp(f[:, 2]))
                if k > SHOE_TALL:
                    out.append('shoe %.2f as tall as long' % k)
                    break
    return out


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
    # R7 chat 10: mode 'body' wears the person's posted jacket, which hangs straight: no bust bump or hip flare
    # turned (Sam's "way too curvaceous" crossed three-quarter; views.turned_curves_fault)
    if LAST.get('mode') == 'body' and V.LAST_TURNED:
        out['turned curves'] = len(V.turned_curves_fault())
    # R7 chat 10 (Sam, 25 Nov, side view: "Is this bottom purple section supposed to be there or is it supposed to be
    # trousers", examples/r7c10-purple-under-jacket-side.jpg): in mode 'body' no jacket or shirt colour of the solid
    # shows below the flat jacket's seated hem (dots, at the check's scale)
    if LAST.get('mode') == 'body':
        hem = min(LAST['sp'].get('bottom') or V.JACKET, 470)
        cloth = (pb == BD.PART_IX['body']) | (pb == BD.PART_IX['dash'])
        out['jacket under the hem'] = int((cloth & LAST['shown'] & (LAST['ky'] >= hem + 4)).sum())
        out['shoe faults'] = len(shoe_faults())
    return out


def apart_faults(img, sp):
    """R7 chat 11 (Sam, 26 Nov, on 'upright, apart', examples/sam-26nov-apart-spread-crotch.png): a front view of a
    person seated with the legs apart, read from the picture alone (any scale, so it reads Sam's own frame):
    'legs spread': the gap between the shins wider than 0.8 of a shin, or the legs wider than the jacket ("Those legs
    are sort of spread ... a bearing the crotch pose"; he wants "a small gap that runs all the way down");
    'jacket triangle': the jacket hangs below its hem's line between the thighs, or no trousers show under it there
    ("her purple jacket dips inward in a triangle, rather than having an appropriate trouser section in that area")."""
    a = np.asarray(img.convert('RGB')).astype(int)
    near = lambda c: np.abs(a - np.array(c)).sum(-1) <= 15
    T, J = near(sp.get('trousers', (40, 40, 46))), near(sp.get('jacket', (40, 40, 46)))
    jy, jx = np.where(J)
    if not len(jx) or not T.any():
        return ['no jacket or trousers in the picture']
    x0, x1 = np.percentile(jx, 1), np.percentile(jx, 99)
    W, cx = x1 - x0, int(round((x0 + x1) / 2))
    ink = max(2, int(W * 0.02))                       # an ink line between touching legs is no gap
    rows = np.where(T.any(1))[0]
    out = []
    gaps, legw, wide = [], [], 0
    for y in rows:
        xs = np.where(T[y])[0]
        lft, rgt = xs[xs < cx], xs[xs >= cx]
        if not len(lft) or not len(rgt):
            continue
        g = rgt.min() - lft.max() - 1
        gaps.append((y, g if g > ink else 0))
        legw.append((y, lft.max() - lft.min()))
        wide = max(wide, (xs.max() - xs.min()) - W)
    lo = [g for y, g in gaps if y > rows[0] + 0.6 * (rows[-1] - rows[0])]       # the shins: the lowest 40%
    lw = [w for y, w in legw if y > rows[0] + 0.6 * (rows[-1] - rows[0])]
    if lo and np.median(lo) > 0.8 * np.median(lw):
        out.append('legs spread: shin gap %.0f, shin %.0f' % (np.median(lo), np.median(lw)))
    if wide > 0.04 * W:
        out.append('legs spread: %.0f wider than the jacket' % wide)
    band = J[:, cx - ink:cx + ink + 1].mean(1) > 0.5   # the jacket down the middle, and at a third out each side
    tip = np.where(band)[0].max()
    side = max(np.where(J[:, int(cx + sg * W / 3)])[0].max() for sg in (-1, 1))
    tb = T[tip + 1:, cx - ink:cx + ink + 1].any(1)
    run = int(np.argmin(tb)) if not tb.all() else len(tb)
    if tip - side > 0.05 * W:
        out.append('jacket triangle: hangs %.0f below its hem between the thighs' % (tip - side))
    if run < 0.08 * W:
        out.append('jacket triangle: only %d of trousers under it' % run)
    return out


SHORT_TOP_NAVY = 0.8    # short_top_faults: the jacket colour under a hi-vis band at most this many hands tall anywhere
#                         (Sam's frame: 0.94; the fix, halfway through the blue as he asked: 0.62)
SHORT_TOP_DIP = 0.25    # ... and no deeper down the middle than at a third out by more than this many hands


def short_top_faults(img, sp):
    """R7 chat 13 (Sam, 26 Nov, on learn-sheet-kemi.jpg front: "Kemi's jacket is behaving like a suit jacket at the
    bottom, and we should have a solid block of trouser beginning about halfway through the blue";
    notes/learn/pose-kit/examples/sam-26nov-kemi-vest-hangs-like-jacket.jpg): a short top with a hi-vis band (a
    person whose kit_extras has 'workwear'), seated, read from the picture alone (any scale, a JPEG too; the hand
    lying on the lap is the ruler): under the band's lowest orange, the jacket colour runs no taller than
    SHORT_TOP_NAVY hands, and does not dip down the middle between the thighs (a suit jacket's hang). Returns the
    faults as text (empty: none)."""
    if 'workwear' not in (sp.get('kit_extras') or ()):
        return []
    a = np.asarray(img.convert('RGB')).astype(int)
    near = lambda c, tol: np.abs(a - np.array(c)).sum(-1) <= tol
    O = near(sp.get('work_c', (236, 112, 30)), 70)
    N = near(sp.get('jacket', (30, 34, 66)), 24)    # (36: a shaded trouser leg, 36,36,40, read as navy)
    K = near(sp.get('skin', (136, 96, 67)), 30)
    oy, ox = np.where(O)
    if not len(ox):
        return []                                     # no band in this view
    lows = {}
    for x in range(ox.min(), ox.max() + 1):
        col = np.where(O[:, x])[0]
        if len(col):
            lows[x] = col.max()
    band = int(np.median(list(lows.values())))
    hand = 0                                          # the tallest skin run below the band: a hand on the lap
    for x in range(ox.min(), ox.max() + 1):
        r = n = 0
        for y in range(band, a.shape[0]):
            n = n + 1 if K[y, x] else 0
            r = max(r, n)
        hand = max(hand, r)
    if hand < 6:
        return []                                     # no hand to measure by (C2: another ruler)
    runs = {}
    for x, lo in lows.items():
        if abs(lo - band) > 0.15 * hand or K[lo + 1:lo + int(0.3 * hand), x].any():
            continue                                  # an arm's orange sleeve or a hand, not the band
        k = lo + 1
        while k < a.shape[0] and not N[k, x] and k < lo + 0.25 * hand:   # the ink line under the band (blurred in a JPEG)
            k += 1
        n0 = k
        while k + 2 < a.shape[0] and (N[k, x] or N[k + 1, x] or N[k + 2, x]):
            k += 1
        if k > n0:
            runs[x] = (k - n0) / hand
    if len(runs) < 5:
        return []
    xs = np.array(sorted(runs)); cx = int(np.median(xs)); W = xs.max() - xs.min()
    mid = [runs[x] for x in xs if abs(x - cx) < 0.06 * W]
    side = [runs[x] for x in xs if abs(x - cx) > 0.2 * W]
    out = []
    every = float(max(runs.values()))
    if every > SHORT_TOP_NAVY:
        out.append('short top hangs like a jacket: %.2f hands of jacket colour under the band' % every)
    if mid and side and max(mid) - np.median(side) > SHORT_TOP_DIP:
        out.append('short top dips between the thighs: %.2f hands deeper in the middle' % (max(mid) - np.median(side)))
    return out


# ---- R7 chat 14: Sam's five notes on Kemi's sheets (26 Nov), each read from the picture alone (any scale, a JPEG too)
FAR_TONE = 0.15         # leg_tone_faults: the shadow tone's share of the trousers at most this (Sam's frame: 0.6)
OVER_HEM = 0.02         # leg_tone_faults: trousers lying on the outfit higher than its hem by this share of its width
LAST_RUGGED = [0.0]
RUGGED = 0.004          # rugged_faults: notch area (closing radius 1.5% of the width) per width squared at most this


def _masks(img, sp):
    a = np.asarray(img.convert('RGB')).astype(int)
    tr = np.array(sp.get('trousers', (40, 40, 46)), float)
    ink = a.max(-1) < 31
    base = (np.abs(a - tr).sum(-1) <= 20) & ~ink
    far = (np.abs(a - tr * 0.72).sum(-1) <= 8) & ~ink
    J = (np.abs(a - np.array(sp.get('jacket', (40, 40, 46)))).sum(-1) <= 20) & ~ink & ~base & ~far
    return a, ink, base, far, J


def leg_tone_faults(img, sp):
    """Sam, 26 Nov, note 1 (examples/sam-26nov-kemi-34-far-leg.jpg): "In 3/4 pose the legs are different colour and
    the darker right leg doesn't seem connected smoothly to the body as it is in the other poses". Legs side by side
    (not crossed): 'two tones': a shadow tone (R7_FAR) over FAR_TONE of the trousers. Kittest leg_tone. (The join, the
    far thigh's top showing over the hem as a notched lump, has no proven picture check yet: chat 14 tried trousers
    above the hem line and it missed Sam's frame.)"""
    a, ink, base, far, J = _masks(img, sp)
    out = []
    if base.sum() and far.sum() > FAR_TONE * base.sum():
        out.append('two tones: shadow leg %.2f of the trousers' % (far.sum() / base.sum()))
    return out


def stray_ink(img, sp, where=None):
    """Sam, 26 Nov, notes 2 and 3 ("Stray horizontal line on butt", examples/sam-26nov-kemi-side-bum-line-chair.jpg;
    "Stray vertical line in crotch", examples/sam-26nov-kemi-apart-crotch-line-knees.jpg): an ink line that ends in
    the open inside a fill (a loose end: one arc of ink round it, the rest no ink). Every house line closes or meets
    another. `where`: only ends inside this mask (the solid layer). Returns the ends (x, y). Kittest stray_ink."""
    import math as _m
    a = np.asarray(img.convert('RGB')).astype(int)
    tr = np.array(sp.get('trousers', (40, 40, 46)), float)
    k = np.clip(((a - np.array(INK)) * (tr - np.array(INK))).sum(-1) / ((tr - np.array(INK)) ** 2).sum(), 0, 1)
    blend = np.abs(a - (np.array(INK) + k[..., None] * (tr - np.array(INK)))).sum(-1) <= 12   # between ink and cloth
    ink = (a.max(-1) < 31) | (blend & (k < 0.5))   # chat 15 (Sam's note 6): on his phone picture (scaled, JPEG) a thin
    #                                                 line is a soft dark stroke, its middle above the house ink's 31
    runs = []
    for y in range(0, a.shape[0], 7):
        d = np.diff(np.r_[0, ink[y].astype(int), 0])
        runs += list(np.where(d == -1)[0] - np.where(d == 1)[0])
    w = max(2.0, float(np.median(runs))) if runs else 3.0
    R = 2.5 * w + 2
    n = max(24, int(2 * _m.pi * R))
    ang = np.linspace(0, 2 * _m.pi, n, endpoint=False)
    dy, dx = np.round(R * np.sin(ang)).astype(int), np.round(R * np.cos(ang)).astype(int)
    H, Wd = ink.shape
    trs = ((np.abs(a - tr).sum(-1) <= 20) | (np.abs(a - tr * 0.72).sum(-1) <= 8) | blend) & ~ink   # the trousers
    #                                             (and a line's soft edge on them: chat 15)
    seat = ((np.abs(a - np.array((58, 60, 68))).sum(-1) <= 16) | (np.abs(a - np.array((84, 86, 96))).sum(-1) <= 16))
    ends = []
    ys, xs = np.where(ink if where is None else ink & where)
    for y, x in zip(ys[::2], xs[::2]):
        yy, xx = y + dy, x + dx
        if yy.min() < 0 or xx.min() < 0 or yy.max() >= H or xx.max() >= Wd:
            continue
        ri = ink[yy, xx]
        rt = trs[yy, xx]
        if not ri.any() or ri.mean() >= 0.35 or (ri | rt | seat[yy, xx]).mean() < 0.97 or rt.mean() < 0.4:
            continue
        if int((np.diff(np.r_[ri, ri[:1]].astype(int)) == 1).sum()) == 1:
            if all(_m.hypot(x - u, y - v) > 3 * R for u, v in ends):
                ends.append((int(x), int(y)))
    return ends


def rugged_faults(img, sp):
    """Sam, 26 Nov, note 4 (examples/sam-26nov-kemi-apart-crotch-line-knees.jpg): "Front-facing pose knee to calf
    area could have smoother, less rugged lines": the trousers' outline notched (the pressed thigh's lobe stepping
    in to the shin, stair steps). Notch area: background a disc closing of the trousers fills, per width squared.
    Kittest rugged."""
    from scipy import ndimage
    a, ink, base, far, J = _masks(img, sp)
    T = ndimage.binary_dilation(base | far, iterations=2) | ink & ndimage.binary_dilation(base | far, iterations=4)
    cols = np.where(J.any(0))[0] if J.any() else np.where(T.any(0))[0]
    W = float(np.percentile(cols, 99) - np.percentile(cols, 1))
    r = max(3, int(0.015 * W))
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    disc = yy ** 2 + xx ** 2 <= r * r
    bg = a.min(-1) > 200                                # the sheet's light ground
    notch = ndimage.binary_closing(T, structure=disc) & ~T & bg
    k = notch.sum() / (W * W)
    LAST_RUGGED[0] = k
    return ['rugged outline: notches %.4f' % k] if k > RUGGED else []


def back_clip_faults(img, sp):
    """Sam, 26 Nov, note 5 (examples/sam-26nov-kemi-side-bum-line-chair.jpg): "Back of bum clips slightly into chair
    in side-on pose and needs stronger lining": from the side, the chair back's front edge (a dark upright line, the
    chair colour on its far side) is gone where the person passes over it, and the person's back there has no ink.
    Rows from the outfit's hem to the seat where, at the chair back's front edge, neither the chair's line nor an
    outline shows: a clip. Kittest back_clip."""
    a = np.asarray(img.convert('RGB')).astype(int)
    ink = a.max(-1) < 31
    chair = (np.abs(a - np.array((58, 60, 68))).sum(-1) <= 14) | (np.abs(a - np.array((84, 86, 96))).sum(-1) <= 14)
    # the chair back: the column band holding chair colour in most rows of its upper half
    rows = np.where(chair.any(1))[0]
    if not len(rows):
        return []
    colfrac = chair[rows[0]:rows[0] + max(10, (rows[-1] - rows[0]) // 3)].mean(0)
    cb = np.where(colfrac > 0.6)[0]
    if not len(cb):
        return []
    face = cb.max()                                     # the back's front edge (the person sits to its right)
    a_, ink_ = a[:, face + 1:face + 8], ink[:, face - 2:face + 6]
    T = np.abs(a - np.array(sp.get('trousers', (40, 40, 46)))).sum(-1) <= 20
    bad = [y for y in range(a.shape[0]) if T[y, face - 6:face + 1].sum() >= 4 and not ink_[y].any()]
    return ['back clip: %d rows of the person over the chair back with no line' % len(bad)] if len(bad) > 3 else []
