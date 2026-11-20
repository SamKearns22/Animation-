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

  KEYS ............ the key poses by name: K1 seated (gun flat on his chest), K2 knee up and turned to the window,
                    K3 head and shoulders out, K4 out to the waist turned back, gun arm straight at the lead cruiser,
                    K5 the recoil of K4
  pose(name, sp) .. a key pose as a lying.Body (k.pose = 'leanout': its arms are held up on purpose)
  at(t, sp) ....... the move in time: the keys and in-betweens (lying.blend), for the shot
  gun(...) ........ the pistol drawn on the skeleton, along the forearm's aim; reported to the body check (aim)
  car_faults(k) ... samples along every bone outside the car's solid parts (the window open)
  sheet(OUT) ...... the five-view pose sheet: each key pose from the front, three-quarter, side, three-quarter back
                    and behind, with the car's window frame, its faults written under each view

    python3 source/leanout.py sheet OUT.jpg
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
TARGET = (0.6, 1.0, -9.0)    # the lead cruiser's windscreen, behind on the right (car frame)
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
        ankles = {'L': (0.32, 0.30, 0.62), 'R': (0.52, 0.30, 0.62)}
        k = L._build((0.42, 0.56, -0.02), (0.42, 0.83, 0.0), (0.42, 1.14, 0.05), _v(1, 0, 0), _v(0, 1, 0.05),
                     _v(0, -0.05, 1), {'R': ((0.38, 0.98, 0.20), _v(0.6, -1, 0.2)),
                                       'L': ((0.30, 0.60, 0.30), _v(-0.6, -0.3, 0.4))},
                     {sd: (_v(*a), _v(0, 0.6, 1), _v(0, -0.1, 1), _v(0, 1, 0)) for sd, a in ankles.items()}, sp,
                     floor=None)
        k.pose = 'leanout'
        return k
    if name == 'K2':          # up on his knees on the seat, turned to the window, free hand on the window's top
        return _key((0.48, 0.80, 0.0), (0.78, 1.30, 0.0), (1, 0, -0.15), (1, -0.15, -0.1),
                    {'R': ('rel', ((-0.04, 0.02, 0.32), 'out')), 'L': ((0.84, 1.34, 0.18), _v(0.3, -1, 0.6))},
                    {'L': (0.52, SEAT + 0.05, 0.14), 'R': (0.50, SEAT + 0.05, -0.12)}, sp)
    if name == 'K3':          # head and shoulders out over the sill, turning back, gun up beside his head
        return _key((0.62, 0.90, 0.0), (0.98, 1.36, -0.04), (0.7, 0, -1), (0.5, 0, -1),
                    {'R': ('rel', ((0.06, 0.34, 0.16), 'out')), 'L': ((0.98, 0.99, 0.18), _v(1, -0.2, 0.5))},
                    {'L': (0.60, SEAT + 0.05, 0.16), 'R': (0.58, SEAT + 0.05, -0.12)}, sp)
    if name in ('K4', 'K5'):  # out to the waist over the sill, turned back, gun arm at the lead cruiser
        neck = _v(1.08, 1.32, -0.10)
        aim = _u(_v(*TARGET) - neck)
        if name == 'K5':      # the recoil: the arm kicks up 16 degrees
            aim = _u(aim + _v(0, 0.29, 0))
        return _key((0.68, 0.90, 0.02), tuple(neck), (0.35, 0, -1), (0.25, -0.05, -1),
                    {'R': ((0.9, 1.3, -0.7), _v(0.4, -1, 0)), 'L': ((1.00, 0.99, 0.14), _v(1, -0.3, 0.4))},
                    {'L': (0.64, SEAT + 0.05, 0.16), 'R': (0.60, SEAT + 0.05, -0.12)}, sp, aim=aim)
    raise KeyError(name)


KEYS = ['K1', 'K2', 'K3', 'K4', 'K5']


# ------------------------------------------------------------------------------------------------ the gun
def gun_pts(k):
    """The pistol in the car frame: (hand, muzzle), the barrel along the forearm."""
    wr, el = k['wrR'], k['elR']
    d = getattr(k, 'aim', None)
    d = _u(wr - el) if d is None else d
    hand = wr + d * 0.05
    return hand, hand + d * 0.17


def draw_gun(img, cam, k, report=True):
    import humancheck as HC
    p = B.Pen(img, S.FLAT)
    hand, muzzle = gun_pts(k)
    d = _u(muzzle - hand)
    down = _u(np.cross(d, _v(1e-3, 0, 1)) if abs(d[1]) > 0.9 else _v(0, -1, 0) - d * d[1])
    body = [hand - d * 0.03, muzzle, muzzle + down * 0.035, hand + down * 0.035]
    grip = [hand - d * 0.03, hand + d * 0.03, hand + d * 0.02 + down * 0.11, hand - d * 0.05 + down * 0.10]
    for poly in (grip, body):
        cam.poly(p, [tuple(q) for q in poly], (40, 40, 44), (14, 14, 16), 2.0)
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
    return out


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
    except F.FigureError as e:                           # the figure guard refused the drawing: a fault, said
        HC.frame_end(0.0)
        return img, [str(e).replace('figure check: ', '').split(' (never')[0]]
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


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        sheet(a[1] if len(a) > 1 else os.path.join(HERE, 'data', 'leanout-sheet.jpg'))
    else:
        print(__doc__)
