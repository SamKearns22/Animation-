#!/usr/bin/env python3
"""MAP  leanout: leaning out of a car window to shoot back, posed on the 3D skeleton (proposal big-body-moves,
Change 2; GTA shot 4, Sam 20 Nov: "kneeling on the seat, out to the waist, legs never seen").

Why: versions 3-4 of shot 4 built the climb out of the flat standing figure turned and stretched; the drawn body came
out "utterly inhuman" (arm out of the back, sausage arm, legs showing). Here every key pose is a 3D skeleton
(lying.Body, metres) in the car's own frame, drawn with the house's flat pieces (lying_flat.draw) and tested by the
body check (humancheck) and against the car's solid shape (gta_cars.solid_at), from five views, before any film
uses it.

The car's frame (gta_cars Tulip at the origin, yaw 0): x across (+ the car's right, the passenger's window side),
y up from the road, z forward. Window sill (belt) 0.95, roof 1.47, the front side window z -0.45..0.45, the
greenhouse's side at x 0.86 (belt) .. 0.70 (roof). The passenger's seat cushion top y 0.47, its middle x 0.42.

  KEYS ............ the key poses by name: K1 seated (gun flat on his chest), K2 up on his knees turned to the window (gun low),
                    K3 head and shoulders out, K4 out to the waist turned back, gun arm straight at the lead cruiser,
                    K5 the recoil of K4
  pose(name, sp) .. a key pose as a lying.Body (k.pose = 'leanout': its arms are held up on purpose)
  seated(sp, ..) .. K1 with the window-side hand anywhere (shots 5-8 gesture on this same body, chat 26)
  at(t, sp) ....... the move in time (TIMES: the beats of the acting rows): keys, eased in-betweens (lying.blend)
  strip(OUT) ...... the move every 0.1 s from the shot's two camera sides, each frame tested (body check, car)
  gun(...) ........ the pistol drawn on the skeleton, along the forearm's aim; reported to the body check (aim)
  car_faults(k) ... samples along every bone outside the car's solid parts (the window open)
  to_world ........ a car-frame skeleton put in the world with the moving car
  film_layer ...... Jason in a film frame: at(t) in the car, drawn through the film's camera, the car rubbing out
                    what it hides per bone half (_cover: legs behind the door, the dash, the roof rail), the flash
  sheet(OUT) ...... the five-view pose sheet: each key pose from the front, three-quarter, side, three-quarter back
                    and behind, with the car's window frame, its faults written under each view

    python3 source/leanout.py sheet OUT.jpg
    python3 source/leanout.py strip OUT.jpg
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import body as B             # noqa: E402
import lying as L            # noqa: E402
import sets as S             # noqa: E402

SILL, ROOF, SEAT = 0.95, 1.47, 0.47
WIN_X = 0.86                 # the greenhouse's side at the sill
TARGET = (0.05, 1.31, -7.68) # the lead cruiser's windscreen in front of its driver (car frame), where it sits
                             # through the four shots (GTA shot 4, chat 21: measured, +-0.35 m across them)
OPEN = ((1, 1),)             # the passenger's front window, wound down

L.HELD_ARMS.add('leanout')


def _v(*a):
    return np.array(a, float)


def _u(a):
    a = np.asarray(a, float)
    return a / (np.linalg.norm(a) + 1e-9)


def _key(pelvis, neck, fwd, hfwd, arms, knees, sp, aim=None):
    """A key pose: the spine (pelvis, neck), where the chest faces (fwd), where the face looks, the arms {side:
    (hand, elbow pole)}, kneeling on the seat {side: knee point}: each shin lies back along the cushion from its knee.
    aim: the gun hand's arm is straightened from its real shoulder along that direction (the forearm on the line)."""
    pelvis, neck = _v(*pelvis), _v(*neck)
    up = _u(neck - pelvis)
    fwd = _u(_v(*fwd) - up * np.dot(fwd, up))
    X = np.cross(up, fwd)                                  # the body's right (lying: fwd = X x up)
    legs = {}
    back = _u(_v(-fwd[0], 0, -fwd[2]))
    for sd, kn in knees.items():
        kn = _v(*kn)
        ank = kn + _u(back + _v(0, 0.22, 0)) * L.SHIN       # the shin back along the seat, the foot lifted a little
        legs[sd] = (ank, fwd + _v(0, 0.3, 0), _u(back + _v(0, -0.6, 0)), _v(0, 1, 0))
    waist = pelvis + up * 0.27
    k = L._build(pelvis, waist, neck, X, up, _v(*hfwd), {sd: ((0, 0, 0), _v(0, -1, 0)) for sd in 'LR'}, legs, sp,
                 floor=None)
    sg = {'R': 1, 'L': -1}
    real = {}
    for sd, (hand, pole) in arms.items():                  # 'rel': (right, up, forward) from that shoulder in the
        if isinstance(hand, str):                          # body's own frame; pole 'out': the elbow out and down
            continue
        real[sd] = [_v(*hand), pole]
    for sd, (hand, pole) in arms.items():
        if isinstance(hand, str):
            r, u_, f = pole[0]
            real[sd] = [k['sh' + sd] + X * r * sg[sd] + up * u_ + fwd * f, pole[1]]
        if isinstance(real[sd][1], str):
            real[sd][1] = X * sg[sd] - up * 0.6
    if aim is not None:
        real['R'][0] = k['shR'] + _u(aim) * (L.UPPER + L.FORE) * 0.985
    k = L._build(pelvis, waist, neck, X, up, _v(*hfwd), {sd: tuple(v) for sd, v in real.items()}, legs, sp,
                 floor=None)
    k.pose = 'leanout'
    if aim is not None:
        k.aim = _u(aim)                                    # the wrist turns the pistol onto the line
    return k


def pose(name, sp):
    """A key pose for this person (their shoulders set the arms' roots)."""
    if name == 'K1':          # seated, pistol flat on his chest (shot 3's frame)
        return seated(sp)
    if name == 'K2':          # up on his knees on the seat, turned to the window, free hand braced on the door
        #                       top, the gun held low and pointing down (chat 20: the gun hand folded across his
        #                       chest was refused from three-quarter front, and the hand on the roof crossed his face)
        k = _key((0.48, 0.80, 0.0), (0.76, 1.25, 0.0), (1, 0, -0.15), (1, -0.15, -0.1),   # head ducked under the roof
                 {'R': ('rel', ((0.10, -0.28, 0.10), 'out')), 'L': ((0.88, 1.03, 0.10), _v(0.8, -1, 0.6))},
                 {'L': (0.52, SEAT + 0.05, 0.14), 'R': (0.50, SEAT + 0.05, -0.12)}, sp)
        k.aim = _u((0.3, -1, -0.1))                         # the barrel's way (not aimed: the arm is not straightened)
        return k
    if name == 'K3':          # head and shoulders out over the sill, turning back, gun up beside his head
        k = _key((0.66, 0.90, 0.0), (1.04, 1.33, -0.04), (0.7, 0, -1), (0.5, 0, -1),   # chat 23: 6 cm further out,
        #                       3 cm lower: the drawn gun arm's shoulder was jammed under the roof edge (the arm's edge
        #                       test, v7 note 3; Sam's "black bars across his vest" in the hold, note 10 (e))
                 {'R': ('rel', ((0.0, 0.30, 0.10), 'out')), 'L': ((0.96, 1.07, 0.18), _v(1, 0, 0.6))},
                 {'L': (0.60, SEAT + 0.05, 0.16), 'R': (0.58, SEAT + 0.05, -0.12)}, sp)
        k.aim = _u((0, 1, 0.1))                             # muzzle up, beside his head (chat 20 critique: the hand
        return k                                            # laid on his head read as a gun to his forehead)
    if name in ('K4', 'K5'):  # out to the waist over the sill, turned back, gun arm at the lead cruiser
        neck = _v(1.08, 1.32, -0.10)
        aim = _u(_v(*TARGET) - neck)
        if name == 'K5':      # the recoil: the arm kicks up 26 degrees (chat 20 critique: 16 read as K4 again)
            aim = _u(aim + _v(0, 0.5, 0))
        return _key((0.68, 0.90, 0.02), tuple(neck), (0.35, 0, -1), (0.25, -0.05, -1),
                    {'R': ((0.9, 1.3, -0.7), _v(0.4, -1, 0)), 'L': ((0.96, 1.07, 0.14), _v(1, 0, 0.6))},   # free hand ON the door top, elbow above it (Sam, chat 22)
                    {'L': (0.64, SEAT + 0.05, 0.16), 'R': (0.60, SEAT + 0.05, -0.12)}, sp, aim=aim)
    raise KeyError(name)



K1_HAND_R = (0.38, 0.98, 0.20)       # K1: the right hand (window side) flat on his chest
K1_POLE_R = (0.6, -1, 0.2)


def seated(sp, hand_r=K1_HAND_R, pole_r=K1_POLE_R, dx=0.0, hfwd=(0, -0.05, 1)):
    """K1, seated, with the right hand (window side) anywhere: shots 5-8 draw Jason on this same skeleton so the cut
    from shot 4 does not change his body (chat 26, F10: shots 5-8 used the seated flat figure, another drawing).
    dx: the whole body slid across the seat (the corner's throw)."""
    ankles = {'L': (0.32, 0.30, 0.62), 'R': (0.52, 0.30, 0.62)}
    o = _v(dx, 0, 0)
    k = L._build(_v(0.42, 0.56, -0.02) + o, _v(0.42, 0.83, 0.0) + o, _v(0.42, 1.14, 0.05) + o, _v(1, 0, 0),
                 _v(0, 1, 0.05), _v(*hfwd), {'R': (_v(*hand_r) + o, _v(*pole_r)),
                                             'L': (_v(0.30, 0.60, 0.30) + o, _v(-0.6, -0.3, 0.4))},
                 {sd: (_v(*a) + o, _v(0, 0.6, 1), _v(0, -0.1, 1), _v(0, 1, 0)) for sd, a in ankles.items()}, sp,
                 floor=None)
    k.pose = 'leanout'
    k.aim = _u((0.85, 0.5, 0.2))                      # the pistol lies flat on his chest, barrel up across it (Sam 21 Nov: it was not drawn)
    k.firing = False
    return k

KEYS = ['K1', 'K2', 'K3', 'K4', 'K5']
FIRE = [0.0, 0.042]                  # the flash: seconds before and after each shot (one drawing at 24 a second)
SHOTS = (1.95, 2.30, 2.62, 2.92)       # the four shots (acting rows, B4)
# the move in time (shot 4's acting rows, beats B1-B6): (seconds, key); between two keys an eased in-between
WOB = 2.0                            # Sam, v7 note 9: the dead cop's car wobbles along the road for two seconds
#                                      before it turns and crashes: everything after the hit is this much later
TIMES = [(0.0, 'K1'), (0.5, 'K1'), (1.0, 'K2'), (1.4, 'K3'), (1.85, 'K4')] + \
        [x for t in SHOTS for x in ((t, 'K4'), (t + 0.04, 'K4'), (t + 0.10, 'K5'), (t + 0.28, 'K4'))] + \
        [(3.2 + WOB, 'K4'), (4.45 + WOB, 'K4'), (4.95 + WOB, 'K3'), (5.4 + WOB, 'K2'), (5.8 + WOB, 'K1'),
         (6.2 + WOB, 'K1')]      # Sam 21 Nov: stays upright out of the window after the crash (it sank to K3 at once)
_CACHE = {}


def _ease(u):
    return u * u * (3 - 2 * u)


def at(t, sp):
    """Jason's skeleton at t seconds into shot 4: the keys of TIMES, eased in-betweens (lying.blend: joints slide,
    directions turn, elbows and knees solved again so the bones keep their lengths); the gun's way turns with them.
    k.firing is True for the 0.06 s of each shot's kick."""
    key = id(sp)
    if key not in _CACHE:
        _CACHE[key] = {n: pose(n, sp) for n in KEYS}
    P = _CACHE[key]
    t = min(max(t, TIMES[0][0]), TIMES[-1][0])
    for (t0, a), (t1, b) in zip(TIMES, TIMES[1:]):
        if t0 <= t <= t1:
            break
    u = 0.0 if t1 <= t0 else _ease((t - t0) / (t1 - t0))
    ka, kb = P[a], P[b]
    k = L.blend(ka, kb, u) if a != b and u > 0 else L.blend(ka, ka, 0.0)
    k.pose = 'leanout'
    k.front = (a == 'K1' and u < 0.5) or (b == 'K1' and u >= 0.5)       # the chest-held pistol is drawn over his body
    da = getattr(ka, 'aim', None)
    db = getattr(kb, 'aim', None)
    if da is None:
        da = _u(ka['wrR'] - ka['elR'])
    if db is None:
        db = _u(kb['wrR'] - kb['elR'])
    if getattr(ka, 'aim', None) is not None or getattr(kb, 'aim', None) is not None:
        k.aim = _u(da + (db - da) * u)
    k.firing = any(s_ - FIRE[0] <= t < s_ + FIRE[1] for s_ in SHOTS)   # the flash frame, on the aim; the kick
    #                                                     follows it (FIRE: the film at 12 drawings a second sets
    #                                                     half a drawing each side, so every shot has one)
    if a != b and 0 < u < 1:
        k = _clear_arms(k, ka, kb, u, sp)
    if HOLD[0] < t < HOLD[1]:                 # the hold after the crash (chat 22, hunt 1: "frozen"): he flinches from
        h0, h1 = HOLD                         # (HOLD: set from the crash's own time by gta_rehearse)
        f = _hump(t, h0, h0 + 0.16, h0 + 0.54)  # the fireball (head away, toward the car's front), looks back at it,
        g = _hump(t, h0 + 0.44, h0 + 0.74, h1)  # a small nod of "got him"; the raised gun drifts with his look
        k['hfwd'] = _u(k['hfwd'] + _v(0.10 * f, 0.06 * f - 0.10 * g, 0.75 * f))
        if getattr(k, 'aim', None) is not None:
            k.aim = _u(k.aim + _v(0.12 * f - 0.06 * g, 0, 0.18 * f))
    return k


HOLD = (3.46 + WOB, 4.55 + WOB)


def _hump(t, a, peak, b):
    if t <= a or t >= b:
        return 0.0
    return _ease((t - a) / (peak - a)) if t < peak else _ease((b - t) / (b - peak))


def _clear_arms(k, ka, kb, u, sp):
    """An in-between whose arm passes through the car (the gun arm swinging up past the roof edge, chat 20): that arm
    alone is taken from a nearby moment (it leads or lags the body), held at its own shoulder, until it is clear."""
    bad = {sd for sd in 'LR' for a, _, _ in car_faults(k, sp) if a.endswith(sd) and a[:2] in ('sh', 'el')}
    for sd in bad:
        for v in [u + du for du in (0.08, -0.08, 0.16, -0.16, 0.25, -0.25, 0.35, -0.35, 0.5, -0.5)] + [0.0, 1.0]:
            v = min(1.0, max(0.0, v))
            m = L.blend(ka, kb, v)
            k2 = k.copy()
            k2.pose = 'leanout'
            for att in ('aim', 'firing', 'front'):
                if hasattr(k, att):
                    setattr(k2, att, getattr(k, att))
            sh = k['sh' + sd]
            pole = m['el' + sd] - (m['sh' + sd] + m['wr' + sd]) / 2
            k2['el' + sd], k2['wr' + sd] = L.limb(sh, sh + m['wr' + sd] - m['sh' + sd], L.UPPER, L.FORE, pole)
            if not any(a.endswith(sd) and a[:2] in ('sh', 'el') for a, _, _ in car_faults(k2, sp)):
                k = k2
                break
    return k


# ------------------------------------------------------------------------------------------------ the gun
GUN = [1.0]                  # the pistol's size: 1 on the pose sheet; the film draws it 1.5x to read on a phone


HAND3D = [True]              # real hands with fingers (hand3d_film) whenever the pistol is out (Sam 21 Nov, shot 4:
#                              "the hand on the door a blob"; F2/F13): the door hand hooked over the door top, the gun
#                              hand closed round the grip; the chest hold (k.front) keeps the circle hands
HAND3D_SCALE = 1.5           # the measured hand at the house arm's slimmed wrist (a cartoon man's hand, a little big)
HAND3D_WRIST = 0.45          # the forearm slims by this into the wrist (limbs.WRIST)


def _gun_down(d):
    return _u(np.cross(d, _v(1e-3, 0, 1)) if abs(d[1]) > 0.9 else _v(0, -1, 0) - d * d[1])


def gun_fist(k):
    """The gun hand as a real fist: (anchor = the grip's middle, A up the grip, B out of the back of the hand), with
    the fist's own wrist on the skeleton's wrist (the hand follows the arm; the pistol follows the hand)."""
    import hand3d_film as HF
    wr, el = k['wrR'], k['elR']
    d = getattr(k, 'aim', None)
    d = _u(wr - el) if d is None else _u(d)
    down = _gun_down(d)
    A = _u(-down + d * 0.16)                               # the grip rakes back, as drawn
    B = _u(np.cross(down, d))                              # the back of a right hand: the pistol's right side
    V, tris, mwr, fd = HF._mesh('grip', 'R')
    R = HF.frame_of(A, B)
    return wr - R @ (mwr * HAND3D_SCALE), A, B


def gun_pts(k):
    """The pistol in the car frame: (hand, muzzle), the barrel along the forearm. With real hands, the pistol sits
    in the fist: its grip's middle on the fist's handle line."""
    wr, el = k['wrR'], k['elR']
    d = getattr(k, 'aim', None)
    d = _u(wr - el) if d is None else d
    hand = wr + d * 0.05
    if HAND3D[0] and not getattr(k, 'front', False):
        anchor = gun_fist(k)[0]
        g = GUN[0]
        hand = anchor - d * (0.62 * -0.02 * g) - _gun_down(_u(d)) * (0.62 * 0.12 * g)
    return hand, hand + d * 0.17 * GUN[0]


def door_hand(k, car=None):
    """The free hand on the door top: (anchor = its wrist, A the fingers' way: out over the door's outer edge, B up
    out of the back of the hand), in k's frame (the car's, or the world's when car is given)."""
    if car is None:
        return k['wrL'], _v(1, -0.15, 0), _v(0, 1, 0)
    o = np.asarray(car.body_pt((0.0, 0.0, 0.0)), float)
    cd = lambda v: _u(np.asarray(car.body_pt(tuple(float(c) for c in v)), float) - o)   # noqa: E731
    return k['wrL'], cd((1, -0.15, 0)), cd((0, 1, 0))


def draw_gun(img, cam, k, report=True):
    import humancheck as HC
    if getattr(k, 'front', False):                        # Sam 21 Nov: no pistol in the chest hold, his hand empty
        return
    p = B.Pen(img, S.FLAT)
    hand, muzzle = gun_pts(k)
    d = _u(muzzle - hand)
    down = _gun_down(d)
    g = GUN[0]
    d0 = d
    if getattr(k, 'front', False):                      # held against his chest: the grip sits inside his fist (Sam 21 Nov)
        down0 = down
        hand = k['wrR'] - d0 * (-0.012 * g) - down0 * (0.074 * g)
    # a side-on pistol that reads at phone size (Sam 21 Nov: the plain dark wedge read as a second seatbelt):
    # a pale gunmetal slide with a dark muzzle block, the frame under it, a raked grip, a trigger guard, a highlight
    P = lambda a, b: hand + d * (0.62 * a * g) + down * (0.62 * b * g)
    slide = [P(-0.05, -0.012), P(0.19, -0.012), P(0.19, 0.045), P(-0.05, 0.045)]
    frame = [P(-0.03, 0.045), P(0.14, 0.045), P(0.14, 0.075), P(0.04, 0.085), P(-0.03, 0.075)]
    grip = [P(-0.05, 0.045), P(0.035, 0.045), P(0.015, 0.20), P(-0.075, 0.20)]
    guard = [P(0.04, 0.075), P(0.115, 0.075), P(0.10, 0.12), P(0.055, 0.12)]
    muzzle_blk = [P(0.165, -0.012), P(0.19, -0.012), P(0.19, 0.045), P(0.165, 0.045)]
    shine = [P(0.0, 0.0), P(0.15, 0.0), P(0.15, 0.014), P(0.0, 0.014)]
    for poly, col in ((guard, (46, 48, 56)), (grip, (44, 46, 54)), (frame, (70, 74, 84)), (slide, (132, 138, 152)),
                      (muzzle_blk, (30, 30, 36)), (shine, (200, 206, 218))):
        cam.poly(p, [tuple(q) for q in poly], col, (14, 14, 16), 2.4)
    if getattr(k, 'front', False):                       # his fist closed round the grip
        c = P(-0.02, 0.12)
        for sx, sy, r_ in ((-0.35, -0.2, 1.0), (0.3, 0.15, 1.0), (0.0, 0.5, 0.9)):
            ring = [tuple(c + d * (0.035 * g * (math.cos(a_) + sx)) + down * (0.035 * g * (math.sin(a_) + sy)))
                    for a_ in [i * math.pi / 6 for i in range(12)]]
            cam.poly(p, ring, (226, 184, 156), (14, 14, 16), 2.2)
    if report:
        m, b0, tg = cam.P(tuple(muzzle)), cam.P(tuple(hand)), cam.P(TARGET)
        HC.aim('Jason', m, (m[0] - b0[0], m[1] - b0[1]), tg, firing=True)


# ------------------------------------------------------------------------------------------------ the car
def car_faults(k, sp):
    """Bone samples inside the car's solid parts (the passenger's window open): [(joint pair, part)]."""
    import gta_cars as G
    car = G.Car('tulip', pos=(0.0, 0.0))
    out = []
    bones = [('neck', 'head'), ('pelvis', 'waist'), ('waist', 'neck')]
    bones += [(a + sd, b + sd) for sd in 'LR' for a, b in (('sh', 'el'), ('el', 'wr'), ('hip', 'kn'), ('kn', 'an'))]
    for a, b in bones:
        for u in np.linspace(0, 1, 9):
            w = k[a] + (k[b] - k[a]) * u
            part = G.solid_at(car, tuple(w), open_windows=OPEN, wall=0.07)
            if part:
                out.append((f'{a}-{b}', part, round(float(u), 2)))
                break
    for sd in 'LR':                       # the drawn arm is thick (Jason's 'arms 36 muscle': about 6 cm round the
        for a, b in (('sh', 'el'), ('el', 'wr')):   # bone): the bone clear of the window frame by less than that
            pa, pb = k[a + sd], k[b + sd]               # still drew the arm through it (v7 note 3, "Jason clips
            d = _u(pb - pa)                             # through two parts of the car": the pillar and the frame)
            n1 = _u(np.cross(d, _v(0, 1, 0)) if abs(d[1]) < 0.9 else np.cross(d, _v(1, 0, 0)))
            n2 = np.cross(d, n1)
            hit = None
            for u in np.linspace(0, 1, 7):
                c = pa + (pb - pa) * u
                for o in (n1, -n1, n2, -n2):
                    q_ = c + o * ARM_R
                    part = G.solid_at(car, tuple(q_), open_windows=OPEN, wall=0.07)
                    if part and any(w_ in part for w_ in FRAME_PARTS) and q_[1] > SILL + 0.06:   # (over the
                        #                                       sill rail is the arm resting on the door top: allowed)
                        hit = (f'{a}{sd}-{b}{sd}', part + " (the drawn arm's edge)", round(float(u), 2))
                        break
                if hit:
                    break
            if hit and not any(x[0] == f'{a}{sd}-{b}{sd}' for x in out):
                out.append(hit)
    for sd in 'LR':                       # a hand resting on the door top sits whole ON it: a wrist at the sill's
        w = k['wr' + sd]                  # edge has the bottom of its round hand cut off by the door line and reads
        if 0.86 < w[0] < 1.06 and abs(w[2]) < 0.9 and w[1] < SILL + HAND_R - 0.01:   # as sinking into it (Sam, chat 22)
            out.append((f'wr{sd}', 'hand cut by the door top', round(float(w[1] - SILL), 2)))
    return out


HAND_R = 0.07                             # the drawn round hand's reach past the wrist (m)
ARM_R = 0.055                             # the drawn arm's reach round its bone (m)
FRAME_PARTS = ('pillar', 'roof', 'windscreen', 'back screen', 'side window')


def car_frame(img, cam):
    """The car's side round the open window, as a guide on the pose sheet (door top, pillars, roof edge)."""
    p = B.Pen(img, S.FLAT)
    red = (190, 62, 48)
    door = [(0.985, 0.30, -0.9), (0.985, 0.30, 0.9), (0.985, SILL, 0.9), (0.985, SILL, -0.9)]
    cam.poly(p, door, red, (30, 20, 20), 2.0)
    cam.poly(p, [(0.985, SILL, -0.9), (0.985, SILL, 0.9), (-0.985, SILL, 0.9), (-0.985, SILL, -0.9)],
             (150, 42, 36), (30, 20, 20), 1.6)
    roof = [(0.70, ROOF, -0.75), (0.70, ROOF, 0.35), (-0.70, ROOF, 0.35), (-0.70, ROOF, -0.75)]
    cam.poly(p, roof, (170, 52, 42), (30, 20, 20), 2.0)
    for z0, z1 in ((0.50, 0.30), (-0.50, -0.40)):          # the windscreen pillar and the B pillar
        cam.poly(p, [(WIN_X, SILL, z0), (WIN_X, SILL, z0 + 0.06), (0.70, ROOF, z1 + 0.06), (0.70, ROOF, z1)],
                 (60, 60, 64), (20, 20, 20), 1.6)


def seat(img, cam):
    p = B.Pen(img, S.FLAT)
    cam.poly(p, [(0.15, SEAT, -0.30), (0.75, SEAT, -0.30), (0.75, SEAT, 0.30), (0.15, SEAT, 0.30)],
             (120, 90, 70), (30, 20, 20), 1.6)


# ------------------------------------------------------------------------------------------------ in the film
def to_world(k, car):
    """A car-frame skeleton put in the world with the car (gta_cars.Car.body_pt: its place, turn and lean)."""
    o = np.asarray(car.body_pt((0.0, 0.0, 0.0)), float)
    out = L.Body()
    for n, v in k.items():
        w = np.asarray(car.body_pt(tuple(float(c) for c in v)), float)
        out[n] = w if n in L.POINTS else _u(w - o)
    out.pose = 'leanout'
    if getattr(k, 'aim', None) is not None:
        out.aim = _u(np.asarray(car.body_pt(tuple(k.aim)), float) - o)
    out.firing = getattr(k, 'firing', False)
    out.front = getattr(k, 'front', False)
    return out


# the pieces the car may hide, each tested on its own sight line (gta_cars.cover_masks): each bone in 8 cm pieces
_BONES = [('neck', 'head'), ('waist', 'neck'), ('pelvis', 'waist')] + \
         [(a + sd, b + sd) for sd in 'LR' for a, b in (('sh', 'el'), ('el', 'wr'), ('hip', 'kn'), ('kn', 'an'))]


IN_CABIN = (WIN_X - 0.08, ROOF)   # a piece with its middle inside these (|x|, y; car frame) is in the cabin


def _cover(car, cam, kw, size, gun=None, kc=None):
    """Per pixel, what of the car is in front of the part of him drawn there: (solid, glass) float masks 0..1. Each
    pixel takes the masks of the nearest bone half on screen (the legs behind the door, the head under the roof rail,
    the arm out in the open air each get their own answer). Returns the masks and the car parts used.
    v7 note 2 ("we can see through the bonnet to Jason"): a piece is tested at its middle, but its drawn shape (the
    vest's hem, the hips, a hand on his thigh) reaches past it on screen; where the middle sat just above the dash
    line, nothing hid the shape's lower edge over the bonnet. So a piece inside the cabin (kc: the car-frame
    skeleton) also takes what hides his seat: the cabin's walls (bonnet, doors, boot) hide all of him inside them."""
    import gta_cars as G
    from scipy import ndimage
    q = 4                                                    # the label map at a quarter of the canvas
    W, H = size[0] // q, size[1] // q
    lab = Image.new('L', (W, H), 0)
    dr = ImageDraw.Draw(lab)
    segs = []
    for a, b in _BONES:
        pa, pb = kw[a], kw[b]
        n = max(2, int(math.ceil(float(np.linalg.norm(pb - pa)) / 0.08)))   # pieces of about 8 cm: the sill cuts
        for i in range(n):                                                   # the leaning chest where it really is
            segs.append((f'{a}-{b}', pa + (pb - pa) * i / n, pa + (pb - pa) * (i + 1) / n))
    if gun is not None:
        segs.append(('gun', gun[0], gun[1]))
    masks, used = [], []
    seat_m = None
    if kc is not None:
        seat_m = G.cover_masks(car, cam, tuple(car.body_pt((0.42, SEAT, 0.0))), size)
        used += [(n, pts, 'seat') for n, pts in seat_m[2]]
    inside = []                                              # per piece, in the same order as segs
    if kc is not None:
        for a, b in _BONES:
            ca, cb = np.asarray(kc[a], float), np.asarray(kc[b], float)
            n = max(2, int(math.ceil(float(np.linalg.norm(kw[b] - kw[a])) / 0.08)))
            for i in range(n):
                m = ca + (cb - ca) * (i + 0.5) / n
                inside.append(abs(m[0]) < IN_CABIN[0] and m[1] < IN_CABIN[1])
    for i, (nm, p0, p1) in enumerate(segs, 1):
        if cam.depth(tuple(p0)) <= cam.NEAR or cam.depth(tuple(p1)) <= cam.NEAR:
            masks.append(None)
            continue
        (x0, y0), kk = cam.project(tuple(p0))
        (x1, y1), _ = cam.project(tuple(p1))
        f = B.SS / q
        dr.line([(x0 * f, y0 * f), (x1 * f, y1 * f)], fill=i, width=max(1, int(0.05 * kk * f)))
        so, gl, us = G.cover_masks(car, cam, tuple((p0 + p1) / 2), size)
        if seat_m is not None and i <= len(inside) and inside[i - 1]:
            so = Image.fromarray(np.maximum(np.asarray(so), np.asarray(seat_m[0])))
        masks.append((so, gl))
        used += [(n, pts, nm) for n, pts in us]
    L_ = np.asarray(lab)
    if not L_.any():
        z = np.zeros((size[1], size[0]), np.float32)
        return z, z, used
    _, (iy, ix) = ndimage.distance_transform_edt(L_ == 0, return_indices=True)
    near = L_[iy, ix]
    near = np.repeat(np.repeat(near, q, 0), q, 1)
    near = np.pad(near, ((0, max(0, size[1] - near.shape[0])), (0, max(0, size[0] - near.shape[1]))), mode='edge')
    near = near[:size[1], :size[0]]
    sol = np.zeros((size[1], size[0]), np.float32)
    gls = np.zeros((size[1], size[0]), np.float32)
    for i, m in enumerate(masks, 1):
        if m is None:
            continue
        sel = near == i
        if sel.any():
            sol[sel] = np.asarray(m[0], np.float32)[sel] / 255
            gls[sel] = np.asarray(m[1], np.float32)[sel] / 255
    edge = np.zeros(near.shape, bool)                        # where two bone pieces meet, the label map's 4-pixel
    edge[:, 1:] |= near[:, 1:] != near[:, :-1]               # blocks cut a stair-step into his outline (Sam's
    edge[1:, :] |= near[1:, :] != near[:-1, :]               # door clip, chat 22): smooth the cut there only
    edge = ndimage.binary_dilation(edge, iterations=q)
    for arr in (sol, gls):                                   # smoothing only ever hides MORE: a blur alone let
        arr[edge] = np.maximum(arr, ndimage.gaussian_filter(arr, q * 0.8))[edge]   # him show half through the
    #                                                          bonnet where two pieces meet on its edge (v7 note 2)
    return sol, gls, used


def flash(img, cam, kw, age):
    """The muzzle flash at the muzzle on the shot's frame: a flat star, white heart (house look: one outline)."""
    hand, muzzle = gun_pts(kw)
    d = _u(muzzle - hand)
    tip = muzzle + d * 0.03
    if cam.depth(tuple(tip)) <= cam.NEAR:
        return
    (X, Y), kk = cam.project(tuple(tip))
    (X2, Y2), _ = cam.project(tuple(tip + d * 0.3))
    ang = math.atan2(Y2 - Y, X2 - X)
    r = max(10.0, 0.16 * kk) * (1.0 - 0.35 * age / 0.042)
    p = B.Pen(img, S.FLAT)
    for col, f in (((255, 196, 70), 1.0), ((255, 248, 214), 0.5)):
        pts = []
        for i in range(10):
            a = ang + i * math.pi / 5
            rr = r * f * (1.0 if i % 2 == 0 else 0.45) * (1.6 if i == 0 else 1.0)
            pts.append((X + rr * math.cos(a), Y + rr * math.sin(a)))
        p.poly(pts, col, (40, 24, 10) if f == 1.0 else None, 2.0 if f == 1.0 else 0)


def film_layer(img, cam, car, t, sp_pose, sp_face, nod=0.0, glass_dim=0.15, hide=False, k=None):
    """Jason in shot 4 at t: the move (at), put in the moving car, drawn with the house's flat pieces through the
    film's camera on his own layer; the car rubs out what of him it hides (legs behind the door, the dash, the roof
    rail), closed glass dims him a little. Returns (alpha drawn, body in the world, car parts used)."""
    import figure as F
    import gta_cars as G
    import lying_flat as LF
    k = at(t, sp_pose) if k is None else k              # k: a ready pose (shots 5-8: seated(), chat 26)
    if nod:                                                  # a small nod: the face dips and comes back
        k['hfwd'] = _u(k['hfwd'] + _v(0, -nod, 0))
        k['hup'] = _u(k['hup'] + _v(0, 0, nod * 0.6))
    kw = to_world(k, car)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    under = cam.depth(tuple(kw['wrR'])) > cam.depth(tuple(kw['neck'])) and not getattr(k, 'front', False)
    real = HAND3D[0] and not getattr(k, 'front', False)
    sp_draw = sp_face
    if real:                                           # the arms end at the wrist; the real hands go on below
        sp_draw = dict(sp_face, lying_hand_L='h3dL', lying_hand_R='h3dR' if under else 'none')
    if under:
        draw_gun(lay, cam, kw, report=False)
    try:
        with _real_hands(cam, kw, car, sp_face) if real else _nothing():
            LF.draw(lay, cam, kw, sp_draw, t)
    except F.FigureError as e:
        FILM_FAULTS.append(f'{t:.2f} s: Jason drawing stopped: {e}')
    if not under:
        draw_gun(lay, cam, kw, report=False)
        if real:                                       # the fist round the grip, over the pistol's grip
            import hand3d_film as HF
            a, A, B = gun_fist(kw)
            HF.draw(lay, cam, 'grip', 'R', a, A, B, sp_face['skin'], HAND3D_SCALE)
    if kw.firing:
        age = min(abs(t - s_) for s_ in SHOTS)
        flash(lay, cam, kw, age)
    sol, gls, used = _cover(car, cam, kw, img.size, gun=gun_pts(kw), kc=k)
    al = np.asarray(lay.split()[3], np.float32) * (1 - sol)
    lay.putalpha(Image.fromarray(al.astype(np.uint8)))
    if not hide:
        img.alpha_composite(lay)
        img.alpha_composite(G.glass_tint(img.size, al * gls * glass_dim))
    return al, kw, used


FILM_FAULTS = []


class _nothing:
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class _real_hands:
    """While Jason is drawn: an arm whose hand is 'h3dL' / 'h3dR' ends in the real hand (hand3d_film) at its place
    in the drawing order (an arm behind his body keeps its hand behind it too)."""
    def __init__(self, cam, kw, car, sp):
        self.cam, self.kw, self.car, self.sp = cam, kw, car, sp

    def __enter__(self):
        import hand3d_film as HF
        import limbs
        self.old, self.wr0 = B.gesture_hand, limbs.WRIST[0]
        limbs.WRIST[0] = HAND3D_WRIST
        old, me = self.old, self

        def gh(p, el, wr, shape, skin, *a, **kw_):
            if shape == 'h3dL':
                anc, A, B_ = door_hand(me.kw, me.car)
                return HF.draw(p.img, me.cam, 'edge', 'L', anc, A, B_, skin, HAND3D_SCALE)
            if shape == 'h3dR':
                anc, A, B_ = gun_fist(me.kw)
                return HF.draw(p.img, me.cam, 'grip', 'R', anc, A, B_, skin, HAND3D_SCALE)
            return old(p, el, wr, shape, skin, *a, **kw_)
        gh.point_finger = True
        B.gesture_hand = gh
        return self

    def __exit__(self, *a):
        import limbs
        B.gesture_hand, limbs.WRIST[0] = self.old, self.wr0
        return False


# ------------------------------------------------------------------------------------------------ the sheet
VIEWS5 = [(0, 'front'), (45, 'three-quarter'), (90, 'side (window)'), (135, 'three-quarter back'),
          (180, 'behind')]


def view_cam(k, deg, dist=4.2):
    """A camera at eye height round the body (0: ahead of the car looking back at him; 90: outside his window)."""
    mid = (k['pelvis'] + k['head']) / 2
    a = math.radians(deg)
    pos = mid + _v(math.sin(a) * dist, 0.15, math.cos(a) * dist)
    return S.Cam(tuple(pos), tuple(mid), focal=1000 * dist / 2.3)


def draw_view(sp, k, deg, guide=True):
    """One view: (picture, faults)."""
    import humancheck as HC
    import lying_flat as LF
    img = B.canvas((226, 222, 214))
    cam = view_cam(k, deg)
    HC.frame_begin()
    under = cam.depth(tuple(k['wrR'])) > cam.depth(tuple(k['neck']))   # the gun beyond his body: drawn first
    if guide:
        seat(img, cam)
    if under:
        draw_gun(img, cam, k, report=False)
    import figure as F
    try:
        LF.draw(img, cam, k, sp, 0.0)
    except F.FigureError as e:                           # the figure guard refused the drawing: a fault, said;
        faults = [str(e).replace('figure check: ', '').split(' (never')[0]]   # the half-drawn body is crossed out
        faults += [f'{w}: {x}' for _, w, kd, x in HC.frame_end(0.0)]          # (chat 20: K2 showed headless, read
        dr = ImageDraw.Draw(img)                                              # as a head fault)
        dr.line([(90, 380), (990, 1640)], fill=(200, 30, 20), width=14)
        dr.line([(990, 380), (90, 1640)], fill=(200, 30, 20), width=14)
        return img, faults
    if not under:
        draw_gun(img, cam, k, report=False)
    if guide and 30 < deg < 150:                         # from outside his window the door hides his knees
        _door_over(img, cam)
    if getattr(k, 'firing', False):                      # the gun as drawn against its target (the body check)
        hand, muzzle = gun_pts(k)                        # the target's line a metre on (the cruiser itself
        tg3 = muzzle + _u(_v(*TARGET) - muzzle)          # may sit behind this view's camera)
        (m, kk), b0, tg = cam.project(tuple(muzzle)), cam.P(tuple(hand)), cam.P(tuple(tg3))
        seen = math.hypot(m[0] - b0[0], m[1] - b0[1]) / (kk * 0.17)
        HC.aim('Jason', m, (m[0] - b0[0], m[1] - b0[1]), tg, firing=seen > 0.5)   # end on (pointing at or away
        #  from the lens) its drawn direction says nothing: judged from the views where the barrel shows its length
    faults = [f'{w}: {x}' for _, w, kd, x in HC.frame_end(0.0)]
    return img, faults


def _door_over(img, cam):
    """Seen from outside, the door (below the sill) is in front of his knees and seat: drawn over them."""
    p = B.Pen(img, S.FLAT)
    cam.poly(p, [(0.985, 0.30, -0.9), (0.985, 0.30, 0.9), (0.985, SILL, 0.9), (0.985, SILL, -0.9)],
             (190, 62, 48), (30, 20, 20), 2.0)
    cam.line(p, [(0.985, SILL, -0.9), (0.985, SILL, 0.9)], (30, 20, 20), 3.0)


def sheet(out, sp=None):
    import gta_cast as GC
    sp = sp or dict(GC.cast()['jason'], mood='stern', squint=0.35, frown=0.07)
    B.SS = 1
    font = ImageFont.truetype(B.SANS, 26)
    small = ImageFont.truetype(B.SANS, 18)
    cw, ch = 300, 420
    W, H = 150 + cw * len(VIEWS5), 60 + (ch + 80) * len(KEYS)
    sh = Image.new('RGB', (W, H), (246, 244, 238))
    d = ImageDraw.Draw(sh)
    d.text((12, 14), 'Shot 4 lean-out: key poses on the 3D skeleton, five views (car side drawn as a guide)',
           font=font, fill=(20, 20, 20))
    report = []
    for r, name in enumerate(KEYS):
        k = pose(name, sp)
        k.firing = name == 'K4'
        cf = car_faults(k, sp)
        y = 60 + r * (ch + 80)
        d.text((10, y + 10), name, font=font, fill=(20, 20, 20))
        d.text((10, y + 44), {'K1': 'seated', 'K2': 'knee up,\nturned', 'K3': 'head out', 'K4': 'out, aimed',
                              'K5': 'recoil'}[name], font=small, fill=(90, 90, 90))
        for c, (deg, label) in enumerate(VIEWS5):
            img, faults = draw_view(sp, k, deg)
            crop = img.convert('RGB').crop((90, 380, 990, 1640)).resize((cw - 10, ch), Image.LANCZOS)
            x = 150 + c * cw
            sh.paste(crop, (x, y))
            if r == 0:
                d.text((x + 4, 34), label, font=small, fill=(20, 20, 20))
            msg = 'OK' if not faults else '; '.join(f.split(': ', 1)[-1][:60] for f in faults)
            d.text((x + 4, y + ch + 4), msg[:34], font=small, fill=(20, 120, 40) if msg == 'OK' else (190, 60, 20))
            report += [f'{name} {label}: {f}' for f in faults]
        if cf:
            d.text((150, y + ch + 30), 'through the car: ' + '; '.join(f'{a} in {p}' for a, p, _ in cf)[:120],
                   font=small, fill=(190, 60, 20))
            report += [f'{name}: {a} goes through {p}' for a, p, _ in cf]
    sh.save(out, quality=88)
    print('\n'.join(report) or 'pose sheet: every key pose clean from every view, clear of the car')
    print('sheet:', out)
    return report


def strip(out, sp=None, step=0.25, views=(45, 100), fps=24):
    """The move as a strip: a frame every `step` seconds from each view in `views` (the shot's camera sides), and every
    film frame (fps) tested: body check from those views and the car's solid shape. Prints the faults."""
    import gta_cast as GC
    sp = sp or dict(GC.cast()['jason'], mood='stern', squint=0.35, frown=0.07)
    B.SS = 1
    report = []
    for i in range(int(TIMES[-1][0] * fps) + 1):
        t = i / fps
        k = at(t, sp)
        report += [f'{t:.2f} s: {a} goes through {p_}' for a, p_, _ in car_faults(k, sp)]
        for deg in views:
            report += [f'{t:.2f} s, {deg} deg: {f}' for f in draw_view(sp, k, deg, guide=False)[1]]
    ts = [round(x * step, 2) for x in range(int(TIMES[-1][0] / step) + 1)]
    cw, ch = 150, 210
    font = ImageFont.truetype(B.SANS, 16)
    sh = Image.new('RGB', (40 + cw * len(ts), 30 + ch * len(views)), (246, 244, 238))
    d = ImageDraw.Draw(sh)
    for r, deg in enumerate(views):
        for c, t in enumerate(ts):
            img, _ = draw_view(sp, at(t, sp), deg)
            sh.paste(img.convert('RGB').crop((90, 380, 990, 1640)).resize((cw - 4, ch - 4), Image.LANCZOS),
                     (40 + c * cw, 30 + r * ch))
            if r == 0:
                d.text((44 + c * cw, 6), f'{t:.2f}', font=font, fill=(20, 20, 20))
        d.text((4, 30 + r * ch + 8), f'{deg}', font=font, fill=(20, 20, 20))
    sh.save(out, quality=88)
    print('\n'.join(report) or f'move: every frame clean ({int(TIMES[-1][0] * fps) + 1} frames), clear of the car')
    print('strip:', out)
    return report


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'strip':
        strip(a[1] if len(a) > 1 else os.path.join(HERE, 'data', 'leanout-strip.jpg'))
    elif a and a[0] == 'sheet':
        sheet(a[1] if len(a) > 1 else os.path.join(HERE, 'data', 'leanout-sheet.jpg'))
    else:
        print(__doc__)
