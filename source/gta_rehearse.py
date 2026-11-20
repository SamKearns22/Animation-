#!/usr/bin/env python3
"""gta_rehearse: Grand Theft Autism's rehearsal clips (rule 8), before anything else moves: shot 2's swerve past the
low camera, shot 4's lean-out and crash. The street here is a STAND-IN (plain blocks, road, kerbs, palms) for
judging the movement; the real Vice City junction is the sets stage (rule 3, beside the game's pictures).

MAP
  PATH ............. shot 2's route: east along the cross street, a sliding right turn, a fishtail, south past the lens
  car_at ........... a car's state at time t on the route (delay for each cruiser): where, heading, slide, lean, steer
  street ........... the stand-in junction: road, lane lines, kerbs, pavements, four pastel blocks, palms, wires
  tyre_smoke ....... puffs left by the rear wheels while the car slides
  light_wash ....... the cruisers' red and blue washing over everything as they come
  shot2 ............ one frame of shot 2 (t from 0 to 4.1 s)
  clip ............. frames to an MP4 (12 drawings a second, played at 24)

    python3 source/gta_rehearse.py shot2 OUT.mp4 [--frames DIR]
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import sets as S                 # noqa: E402
import gta_cars as G             # noqa: E402
import gta_cast as GC            # noqa: E402
from ed import INK               # noqa: E402

FPS = 12
SKY_TOP, SKY_LOW = (236, 150, 172), (252, 196, 170)
ROAD = (112, 98, 112)
PAVE = (178, 158, 160)
KERB = (204, 190, 186)

# ------------------------------------------------------------------------------------------------ the route
LANE_Z = 25.5            # across the cross street's middle (kerbs at z 23 and 28)
ARC_X0, R = -10.5, 6.0   # the turn starts here and swings south on radius R (clears the kerb corner by a metre)
LANE_X = ARC_X0 + R      # the southbound lane down the main road (x = -4.5; kerb at -7)
A_LEN = 40.0             # straight before the turn (from x = -49)
B_LEN = math.pi / 2 * R


def route(s):
    """Point (x, z) and heading (degrees) at distance s along the route; s = 0 is the start of the turn."""
    if s < 0:
        return (ARC_X0 + s, LANE_Z), 90.0
    if s < B_LEN:
        a = s / R
        cx, cz = ARC_X0, LANE_Z - R
        return (cx + R * math.sin(a), cz + R * math.cos(a)), 90.0 + math.degrees(a)
    c = s - B_LEN
    return (LANE_X, LANE_Z - R - c), 180.0


def bump(x, a, peak, b):
    if x <= a or x >= b:
        return 0.0
    u = (x - a) / (peak - a) if x < peak else (b - x) / (b - peak)
    return u * u * (3 - 2 * u)


def car_at(t, delay=0.0, wild=1.0):
    """The car at time t: s from a speed that brakes into the turn and floors it out; the back end slides out
    through the turn (yaw ahead of the heading), the body leans out, a fishtail after."""
    u = t - delay
    s = 12.0 * (u - 0.3) + 2.6 * max(0.0, u - 1.1) ** 2
    (x, z), head = route(s)
    c = s - B_LEN
    if c > 0:                                # the fishtail: the car swings across the lane and back
        k = min(1.0, c / 3.0)
        off = wild * 0.8 * k * math.sin(c / 3.6) * math.exp(-c / 10.0)
        doff = wild * 0.8 * (k * math.cos(c / 3.6) / 3.6 - k * math.sin(c / 3.6) / 10.0) * math.exp(-c / 10.0)
        x -= off
        head += math.degrees(math.atan(doff))
    drift = wild * (26.0 * bump(s, -1.5, B_LEN + 0.5, B_LEN + 9.0) + 9.0 * math.sin(max(0, c) / 3.6) * bump(s, B_LEN, B_LEN + 6, B_LEN + 16))
    yaw = head + drift
    steer = (16.0 if 0 < s < B_LEN else 0.0) - 0.9 * drift
    roll = -6.0 * wild * bump(s, -2.0, B_LEN * 0.7, B_LEN + 6) + 2.5 * wild * math.sin(max(0, c) / 3.6) * bump(s, B_LEN, B_LEN + 6, B_LEN + 16)
    pitch = -1.0 if u > 1.1 else 0.6
    return dict(pos=(x, z), yaw=yaw, roll=roll, pitch=pitch, steer=max(-30, min(30, steer)), spin=s / 0.32, s=s, drift=drift)


# ------------------------------------------------------------------------------------------------ the stand-in street
BLOCKS = [  # (x0, x1, z0, z1, height, colour, name)
    (-60, -10.0, -60, 20.0, 9.0, (238, 196, 206), 'sw'),
    (-60, -10.0, 31.0, 80, 12.0, (190, 226, 214), 'nw'),
    (10.0, 60, 31.0, 80, 7.0, (246, 226, 168), 'ne'),
    (10.0, 60, -60, 20.0, 10.0, (200, 206, 236), 'se'),
]


def _quad(cam, p, pts, col, line=INK, lw=2.0):
    cam.poly(p, pts, col, line, lw)


def sky(img):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for y in range(0, img.height, 6):
        k = y / img.height
        c = tuple(int(a + (b - a) * min(1, k * 1.6)) for a, b in zip(SKY_TOP, SKY_LOW))
        d.line([(0, y), (img.width, y)], fill=c + (255,), width=6)
    img.alpha_composite(lay)


def ground(img, cam, p):
    _quad(cam, p, [(-200, 0, -200), (200, 0, -200), (200, 0, 200), (-200, 0, 200)], ROAD, None, 0)
    # pavements (raised 0.15) round each block, kerb faces toward the road
    for x0, x1, z0, z1, *_ in BLOCKS:
        ex0 = x0 if x0 < -50 else x0 - 0
        px0, px1 = (x0, x1 + 3.0) if x1 < 0 else (x0 - 3.0, x1)
        pz0, pz1 = (z0, z1 + 3.0) if z1 < 25 else (z0 - 3.0, z1)
        _quad(cam, p, [(px0, 0.15, pz0), (px1, 0.15, pz0), (px1, 0.15, pz1), (px0, 0.15, pz1)], PAVE, None, 0)
    for x0, x1, z0, z1, *_ in BLOCKS:
        kx = x1 + 3.0 if x1 < 0 else x0 - 3.0
        kz = z1 + 3.0 if z1 < 25 else z0 - 3.0
        zz = (z0, kz) if z1 < 25 else (kz, z1)
        xx = (x0, kx) if x1 < 0 else (kx, x1)
        _quad(cam, p, [(kx, 0, zz[0]), (kx, 0.15, zz[0]), (kx, 0.15, zz[1]), (kx, 0, zz[1])], KERB, INK, 1.4)
        _quad(cam, p, [(xx[0], 0, kz), (xx[0], 0.15, kz), (xx[1], 0.15, kz), (xx[1], 0, kz)], KERB, INK, 1.4)
    for z in np.arange(-40, 20.0, 1.5):          # paving slabs on the near pavement
        cam.line(p, [(-10.0, 0.152, z), (-7.0, 0.152, z)], (150, 130, 136), 1.2)
    for x in (-9.0, -8.0):
        cam.line(p, [(x, 0.152, -40), (x, 0.152, 20.0)], (150, 130, 136), 1.2)
    # lane lines: double yellow down the middle of the main road, white dashes, a stop line
    for dx in (-0.12, 0.12):
        _quad(cam, p, [(dx - 0.05, 0.01, -80), (dx + 0.05, 0.01, -80), (dx + 0.05, 0.01, 21), (dx - 0.05, 0.01, 21)], (236, 196, 70), None, 0)
        _quad(cam, p, [(dx - 0.05, 0.01, 30), (dx + 0.05, 0.01, 30), (dx + 0.05, 0.01, 120), (dx - 0.05, 0.01, 120)], (236, 196, 70), None, 0)
        for x0, x1 in ((-80, -9), (9, 80)):
            _quad(cam, p, [(x0, 0.01, LANE_Z + dx - 0.05), (x1, 0.01, LANE_Z + dx - 0.05), (x1, 0.01, LANE_Z + dx + 0.05),
                           (x0, 0.01, LANE_Z + dx + 0.05)], (236, 196, 70), None, 0)
    for z in np.arange(-80, 21, 6.0):
        for x in (-3.5, 3.5):
            _quad(cam, p, [(x - 0.06, 0.01, z), (x + 0.06, 0.01, z), (x + 0.06, 0.01, z + 3), (x - 0.06, 0.01, z + 3)], (236, 232, 228), None, 0)
    _quad(cam, p, [(-7.0, 0.01, 21.4), (0, 0.01, 21.4), (0, 0.01, 21.9), (-7.0, 0.01, 21.9)], (236, 232, 228), None, 0)
    for k in range(7):                       # a zebra crossing over the cross street's mouth
        x = -6.4 + k * 0.9
        _quad(cam, p, [(x, 0.01, 23.6), (x + 0.45, 0.01, 23.6), (x + 0.45, 0.01, 27.4), (x, 0.01, 27.4)], (226, 222, 218), None, 0)


def block(img, cam, p, b):
    x0, x1, z0, z1, h, col, name = b
    faces = S.obox(((x0 + x1) / 2, 0.15, (z0 + z1) / 2), (x1 - x0, h, z1 - z0), 0, cols={'all': col})
    for f in faces:
        if f.seen(cam):
            f.fill = G.shade(col, f.n, 0.25)
            cam.poly(p, f.pts, f.fill, INK, 2.2)
            n = f.n
            if abs(n[1]) > 0.5:
                continue
            # windows and a shop front on the faces that look onto the streets
            if abs(n[0]) > 0.5:
                xf = x1 if n[0] > 0 else x0
                along = [(xf + n[0] * 0.01, z) for z in np.arange(max(z0, -40) + 1.5, min(z1, 70) - 1.0, 3.2)]
                pts3 = lambda a, y0, y1, w: [(a[0], y0, a[1]), (a[0], y0, a[1] + w), (a[0], y1, a[1] + w), (a[0], y1, a[1])]
            else:
                zf = z1 if n[2] > 0 else z0
                along = [(x, zf + n[2] * 0.01) for x in np.arange(max(x0, -40) + 1.5, min(x1, 40) - 1.0, 3.2)]
                pts3 = lambda a, y0, y1, w: [(a[0], y0, a[1]), (a[0] + w, y0, a[1]), (a[0] + w, y1, a[1]), (a[0], y1, a[1])]
            for a in along:
                cam.poly(p, pts3(a, 0.4, 3.0, 2.4), (70, 84, 104), INK, 1.4)          # shop glass
                for y in np.arange(4.4, h - 1.2, 2.8):
                    cam.poly(p, pts3((a[0] + 0.5 * (n[2] != 0), a[1] + 0.5 * (n[0] != 0)), y, y + 1.4, 1.4),
                             (96, 112, 132), INK, 1.2)
            awn = G.dk_(col, 0.7)
            for a in along[::3]:
                cam.poly(p, pts3(a, 3.1, 3.6, 2.4), awn, INK, 1.2)


def palm(img, cam, p, at, h=7.0, seed=0):
    rng = np.random.RandomState(seed)
    x, z = at
    trunk = [(x + 0.18 * math.sin(k * 0.6), k * h / 6, z) for k in range(7)]
    for a, b in zip(trunk, trunk[1:]):
        cam.line(p, [a, b], INK, 7.0)
        cam.line(p, [a, b], (150, 118, 92), 4.6)
    top = trunk[-1]
    for i in range(8):
        ang = i / 8 * 2 * math.pi + rng.uniform(-0.2, 0.2)
        L = rng.uniform(2.0, 2.8)
        pts = []
        for k in range(6):
            r = L * k / 5
            pts.append((top[0] + r * math.cos(ang), top[1] - 0.45 * r * r / L, top[2] + r * math.sin(ang)))
        if any(cam.depth(q) < cam.NEAR for q in pts):
            continue
        sp = [cam.project(q)[0] for q in pts]
        left, right = [], []
        for k, (q, (X, Y)) in enumerate(zip(pts, sp)):
            w = 0.32 * math.sin(math.pi * k / 5) * cam.project(q)[1]
            left.append((X, Y - w))
            right.append((X, Y + w * 0.3))
        p.poly(left + right[::-1], (64, 120, 84), INK, 1.4)


def wires(img, cam, p):
    for x in (-7.6, 7.6):
        for z in (-20, 8, 36, 64):
            cam.line(p, [(x, 0, z), (x, 8.5, z)], (90, 70, 60), 3.0)
    for x, dy in ((-7.6, 0), (7.6, 0)):
        for z0, z1 in ((-20, 8), (8, 36), (36, 64)):
            pts = [(x, 8.2 - 0.6 * math.sin(math.pi * k / 8), z0 + (z1 - z0) * k / 8) for k in range(9)]
            cam.line(p, pts, (40, 30, 40), 1.4)


def hydrant(img, cam, p, at, col=(232, 196, 60)):
    x, z = at
    for part in (S.cylinder((x, 0.15, z), 0.13, 0.55, dict(side=G.dk_(col, 0.9), top=col)),
                 S.cylinder((x, 0.70, z), 0.10, 0.12, dict(side=G.dk_(col, 0.75), top=G.dk_(col, 0.9))),
                 S.cylinder((x, 0.15, z), 0.17, 0.08, dict(side=G.dk_(col, 0.8), top=col))):
        for f in part:
            if f.seen(cam):
                f.draw(img, cam, p)
    for sx in (-1, 1):
        cam.poly(p, [(x + sx * 0.12, 0.42, z - 0.05), (x + sx * 0.22, 0.42, z - 0.05), (x + sx * 0.22, 0.52, z - 0.05),
                     (x + sx * 0.12, 0.52, z - 0.05)], G.dk_(col, 0.85), INK, 1.4)


def street(img, cam, p, near_block=True):
    sky(img)
    ground(img, cam, p)
    far = [b for b in BLOCKS if b[6] != 'sw']
    for b in sorted(far, key=lambda b: -math.dist(cam.pos, ((b[0] + b[1]) / 2, 2, (b[2] + b[3]) / 2))):
        block(img, cam, p, b)
    for at, sd in (((8.6, 40.0), 1), ((-8.6, 44.0), 2), ((8.6, 12.0), 3), ((-14.0, 29.6), 4), ((8.6, -4.0), 5)):
        palm(img, cam, p, at, seed=sd)
    wires(img, cam, p)


# ------------------------------------------------------------------------------------------------ effects
def tyre_smoke(img, cam, t, delay, life=1.3):
    """Grey puffs left at the rear wheels while the car slides (drift over 8 degrees)."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    p = S.pen(lay)
    puffs = []
    for te in np.arange(max(0.0, t - life), t + 1e-6, 1.0 / 24):
        st = car_at(te, delay)
        if abs(st['drift']) < 8 or st['s'] < -2:
            continue
        car = G.Car('tulip', pos=st['pos'], yaw=st['yaw'])
        age = (t - te) / life
        for sx in (-1, 1):
            c = car.ground_pt((sx * 0.87, 0.25, -1.55))
            rng = np.random.RandomState(int(te * 1000) + sx)
            c = (c[0] + rng.normal(0, 0.3) * age, 0.3 + 1.2 * age, c[2] + rng.normal(0, 0.3) * age)
            puffs.append((math.dist(c, cam.pos), c, age, rng))
    for _, c, age, rng in sorted(puffs, key=lambda e: -e[0]):
        if cam.depth(c) < 0.3:
            continue
        (X, Y), k = cam.project(c)
        r = (0.45 + 1.4 * age) * k
        a = int(175 * (1 - age))
        pts = [(X + r * rng.uniform(0.8, 1.1) * math.cos(q), Y + r * rng.uniform(0.8, 1.1) * math.sin(q))
               for q in np.linspace(0, 2 * math.pi, 9, endpoint=False)]
        p.poly(pts, (226, 214, 220, a), None, 0)
    img.alpha_composite(lay)


def light_wash(img, cam, cars, t):
    red = blue = 0.0
    for car in cars:
        car.t = t
        r, b = G.flash(car)
        d = max(2.0, math.dist(cam.pos, (car.pos[0], 1.0, car.pos[1])))
        k = min(1.0, 6.0 / d) ** 2
        red += r * k
        blue += b * k
    if red > 0:
        img.alpha_composite(Image.new('RGBA', img.size, (255, 40, 60, int(min(32, 32 * red)))))
    if blue > 0:
        img.alpha_composite(Image.new('RGBA', img.size, (50, 90, 255, int(min(32, 32 * blue)))))


# ------------------------------------------------------------------------------------------------ shot 2
SHOT2_LEN = 4.1
LEAD2 = 0.3                # an empty beat of junction before the car screams out
HYD2 = (-8.5, 16.8)          # shot 2's hydrant: on the pavement, clear of the car's way in
COPS = (LEAD2 + 0.85, LEAD2 + 1.45, LEAD2 + 2.05)


def shot2_cam(t, cars):
    u = min(1.0, t / SHOT2_LEN)
    e = u * u * (3 - 2 * u)
    pos = (-7.6 - 0.5 * e, 0.4, 13.0 + 0.4 * e)
    at = (-3.6 - 2.6 * e, 3.4, 26.0)
    shake = [0.0, 0.0]
    for c in cars:
        d = math.dist((pos[0], pos[2]), c.pos)
        if d < 7:
            k = (7 - d) / 7
            shake[0] += 9 * k * math.sin(t * 61 + d)
            shake[1] += 7 * k * math.cos(t * 47 + d)
    return S.Cam(pos, at, 640, shake=tuple(shake))


def shot2(t, record=None):
    img = B.canvas((240, 170, 170))
    states = [('tulip', car_at(t, LEAD2, 1.0))] + [('cruiser', car_at(t, d, 0.55)) for d in COPS]
    cars = []
    for kind, st in states:
        c = G.Car(kind, pos=st['pos'], yaw=st['yaw'], roll=st['roll'], pitch=st['pitch'], steer=st['steer'], spin=st['spin'])
        c.st = st
        cars.append(c)
    cam = shot2_cam(t, cars)
    p = S.pen(img)
    street(img, cam, p)
    tyre_smoke(img, cam, t, LEAD2)
    live = [c for c in cars if c.st['s'] > -12 and cam.depth((c.pos[0], 1, c.pos[1])) > 0.5]
    items = [('getaway car' if c is cars[0] else f'cruiser {cars.index(c)}', math.dist(cam.pos, (c.pos[0], 0.8, c.pos[1])),
              lambda im, c=c: G.draw_car(im, cam, c, t=t)) for c in live]
    items.append(('hydrant', math.dist(cam.pos, (HYD2[0], 0.4, HYD2[1])), lambda im: hydrant(im, cam, S.pen(im), HYD2)))
    for _, _, draw in sorted(items, key=lambda it: -it[1]):   # far to near: the hydrant hides the cars behind it (rule 17)
        draw(img)
    if record is not None:                   # the depth check sees the picture before the lights' tint goes over it
        record += items
    block(img, cam, p, BLOCKS[0])             # the near block hides the cross street until the car rounds it
    if record is None:
        light_wash(img, cam, cars[1:], t)
    return img


OVERLAP_OK2 = []                 # rule 17: shot 2 has no meant overlaps
# ------------------------------------------------------------------------------------------------ shot 4
# The lean-out and the crash (rule 8, rehearsal 2). The Tulip runs north up a straight shop street at chase speed; the
# camera rides with it (its keys are in the car's own frame), starting on shot 3's windscreen three-shot, tracking
# left (round the car's front-right corner) with Jason as he leans out of the passenger window until it hangs
# outside beside him looking back down the street; four shots; the lead cruiser's windscreen crazes in front of its
# driver, it slews right over the kerb, through a hydrant (a water jet) and into a shop front (a fireball); then the
# camera and Jason go back in to shot 3's frame. Effects are flying_whales_fx's, drawn through FxCam.
import figure as FG              # noqa: E402
import flying_whales_fx as FX    # noqa: E402
import people as PK              # noqa: E402
import prepper_cast as PC        # noqa: E402
import views as V                # noqa: E402

SHOT4_LEN = 6.2
V4 = 16.0                        # chase speed, m/s
LANE4 = 5.0                      # the Tulip's lane: the outer northbound lane (kerb at x 7, shop fronts at x 10)
KERB4, SHOP4 = 7.0, 10.0
SHOTS = (1.95, 2.30, 2.62, 2.92)  # Jason's four shots: 1 sparks off the bonnet, 2-4 into the windscreen
CRAZE = (0.0, 0.5, 0.8, 1.0)
GAPS = (4.8, 13.5, 22.0)         # the cruisers behind the Tulip (m): the lead close enough to read at the shots         # the cruisers behind the Tulip (m)
FIG_H = 1128.0                   # a person's whole height in their own units (head top to soles)


def smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def tulip4(t):
    z = V4 * t
    x = LANE4 + 0.10 * math.sin(t * 1.7)
    yaw = math.degrees(math.atan(0.10 * 1.7 * math.cos(t * 1.7) / V4))
    return G.Car('tulip', pos=(x, z), yaw=yaw, roll=0.7 * math.sin(t * 2.3), pitch=0.5, spin=z / 0.34)


# ---- the lead cruiser's path: chasing, hit, slewing over the kerb and the hydrant into the shop front
def _lead_track():
    dt = 1.0 / 240
    th = SHOTS[-1]
    rows, x, z, head, imp, hyd = [], None, None, 0.0, None, None
    for i in range(int(SHOT4_LEN / dt) + 2):
        t = i * dt
        u = t - th
        if u <= 0:
            x = LANE4 - 0.15 + 0.3 * math.sin(t * 2.1 + 1.0)
            z = V4 * t - GAPS[0]
            head = math.degrees(math.atan(0.3 * 2.1 * math.cos(t * 2.1 + 1.0) / V4))
            yaw, lift, crush = head, 0.0, 0.0
        elif imp is None:
            head = 34.0 * smooth(u / 0.45)
            v = V4 * (1 - 0.25 * min(1.0, u / 0.8))
            x += v * math.sin(math.radians(head)) * dt
            z += v * math.cos(math.radians(head)) * dt
            yaw = head + 30.0 * smooth(u / 0.5)                 # the back end swings out: it slews
            lift = 0.0
            fx = x + 2.55 * math.sin(math.radians(yaw))         # the front's middle
            if hyd is None and fx > 8.1:
                hyd = (t, (fx, z + 2.55 * math.cos(math.radians(yaw))))
            cs = [(x + S.rot_y((sx * 0.97, 0, 2.58), yaw)[0]) for sx in (-1, 1)]
            if max(cs) >= SHOP4 + 0.9:                       # the nose goes through the shop glass
                imp = (t, (x, z), yaw)
            crush = 0.0
        else:
            ti, (xi, zi), yi = imp
            w = t - ti
            k = smooth(w / 0.12)
            x = xi + 0.28 * k * math.sin(math.radians(yi)) - 0.1 * smooth((w - 0.12) / 0.3) * math.sin(math.radians(yi))
            z = zi + 0.28 * k * math.cos(math.radians(yi))
            yaw, crush, lift = yi + 4.0 * k, k, 0.0
        # the kerb: a jolt as the front wheels then the back wheels go up it
        kerb = 0.0
        if imp is None and u > 0:
            for zc, amt in ((1.50, 1.0), (-1.40, 0.8)):
                wx = x + S.rot_y((0.86, 0, zc), yaw)[0]
                kerb += amt * max(0.0, 1 - abs(wx - KERB4) / 0.5)
        rows.append(dict(t=t, pos=(x, z), yaw=yaw, crush=crush, kerb=kerb, u=u))
    return rows, imp, hyd


LEAD, IMPACT, HYDRANT = _lead_track()


def lead_at(t):
    r = LEAD[min(len(LEAD) - 1, max(0, int(round(t * 240))))]
    shatter = 0.0
    for ts, c in zip(SHOTS, CRAZE):
        if t >= ts:
            shatter = c
    u = r['u']
    roll = -7.0 * smooth(u / 0.4) * (1 - smooth((u - 0.6) / 0.3)) if u > 0 else 0.0
    car = G.Car('cruiser', pos=r['pos'], yaw=r['yaw'], roll=roll + 3.0 * r['kerb'], pitch=2.5 * r['kerb'] - 3.0 * r['crush'],
                steer=-22.0 * smooth(u / 0.3) if u > 0 else 0.0, spin=(V4 * min(t, IMPACT[0]) - GAPS[0]) / 0.37,
                crush=r['crush'], shatter=shatter, lift=0.06 * r['kerb'])
    car.u = u
    return car


def chaser_at(t, i):
    """Cruisers 2 and 3: weaving behind; after the crash they swerve to the inner lane round it."""
    gap = GAPS[i]
    z = V4 * t - gap
    sw = smooth((t - (SHOTS[-1] + 0.2 + 0.35 * i)) / 0.7)
    x = LANE4 - 0.2 + 0.35 * math.sin(t * 1.9 + 2 * i) - 3.4 * sw
    dsw = 3.4 * (smooth((t + 0.02 - (SHOTS[-1] + 0.2 + 0.35 * i)) / 0.7) - sw) / 0.02
    yaw = math.degrees(math.atan((0.35 * 1.9 * math.cos(t * 1.9 + 2 * i) - dsw) / V4))
    return G.Car('cruiser', pos=(x, z), yaw=yaw, roll=-0.08 * yaw, pitch=0.4, steer=yaw * 0.8, spin=z / 0.37)


# ---- the camera: keys in the Tulip's own frame (x right, y up, z forward), eased from key to key
CAM4 = [  # (t, position, look-at, focal)
    (0.00, (0.00, 1.52, 3.95), (0.00, 1.02, -0.30), 1750),
    (0.45, (0.00, 1.52, 3.95), (0.00, 1.02, -0.30), 1750),
    (1.10, (2.35, 1.55, 3.45), (0.40, 1.10, -2.40), 1600),   # wide of the corner: no squeeze on a wide lens
    (1.70, (2.40, 2.30, 2.25), (-0.80, 0.85, -14.0), 1250),  # further back and higher: Jason whole, the cruiser bigger, his arm seen from above
    (3.00, (2.40, 2.25, 2.15), (-0.50, 0.90, -14.0), 1400),  # pushes in on the cruiser through the shots
    (3.50, (2.30, 1.87, 1.85), (1.60, 1.05, -15.0), 950),    # pans with the slew on a wider lens: jet and fireball in frame
    (4.55, (2.25, 1.87, 1.75), (1.50, 1.05, -15.0), 980),
    (5.15, (2.35, 1.55, 3.45), (0.40, 1.10, -2.40), 1600),
    (5.75, (0.00, 1.52, 3.95), (0.00, 1.02, -0.30), 1750),
    (6.20, (0.00, 1.52, 3.95), (0.00, 1.02, -0.30), 1750),
]


def _key(t):
    for a, b in zip(CAM4, CAM4[1:]):
        if a[0] <= t <= b[0]:
            e = smooth((t - a[0]) / (b[0] - a[0]))
            L = lambda p, q: tuple(x + (y - x) * e for x, y in zip(p, q))
            return L(a[1], b[1]), L(a[2], b[2]), a[3] + (b[3] - a[3]) * e
    return CAM4[-1][1], CAM4[-1][2], CAM4[-1][3]


def shot4_cam(t, car):
    pos, at, focal = _key(t)
    rng = np.random.RandomState(int(t * 24))
    shake = [rng.uniform(-2.5, 2.5), rng.uniform(-2.0, 2.0)]   # the road through the car
    for ts in SHOTS:                                            # each shot kicks the frame
        w = t - ts
        if 0 <= w < 0.16:
            shake[0] += 7 * (1 - w / 0.16) * (1 if int(ts * 100) % 2 else -1)
            shake[1] += 9 * (1 - w / 0.16)
    if IMPACT and 0 <= t - IMPACT[0] < 0.3:
        shake[1] += 6 * (1 - (t - IMPACT[0]) / 0.3) * math.sin(t * 90)
    return S.Cam(car.ground_pt(pos), car.ground_pt(at), focal, shake=tuple(shake))


# ---- the shop street (a stand-in until the sets stage: plain pastel shop blocks, palms, passers-by)
def _strip_blocks():
    rng = np.random.RandomState(44)
    out = []
    cols = [(238, 196, 206), (190, 226, 214), (246, 226, 168), (200, 206, 236), (250, 204, 170), (214, 196, 236),
            (236, 236, 222), (176, 220, 230)]
    for side in (-1, 1):
        z = -90.0
        while z < 230:
            w = rng.uniform(9, 17)
            out.append(dict(side=side, z0=z, z1=z + w, h=rng.uniform(5.0, 10.5), col=cols[rng.randint(len(cols))],
                            awn=cols[rng.randint(len(cols))], seed=int(rng.randint(1 << 20))))
            z += w
    return out


BLOCKS4 = _strip_blocks()


def _strip_people():
    rng = np.random.RandomState(7)
    out = []
    for side in (-1, 1):
        z = -60.0
        while z < 200:
            z += rng.uniform(3.0, 9.0)
            out.append(dict(at=(side * rng.uniform(8.2, 9.5), z), face=rng.choice([0.0, 180.0, 90.0 * -side]),
                            i=len(out), walk=rng.uniform(0, 1)))
    return out


PEOPLE4 = _strip_people()
PALMS4 = [((7.6 if s < 0 else 9.2) * s, z) for k, (s, z) in enumerate((s, z) for z in np.arange(-70, 220, 21.0) for s in (-1, 1))
          if (k + int(z / 21)) % 2 == 0]
_SP = {}


def _walker(i):
    if i not in _SP:
        cr = PK.crowds(GC.FILM)
        _SP[i] = PK.crowd_person(cr['walker'], i)
    return _SP[i]


def _cop(i):
    k = 'cop%d' % i
    if k not in _SP:
        _SP[k] = PK.crowd_person(PK.crowds(GC.FILM)['cop'], i)
    return _SP[k]


def strip_ground(img, cam, p):
    sky(img)
    zc = cam.pos[2]
    z0, z1 = zc - 160, zc + 160
    _quad(cam, p, [(-60, 0, z0), (60, 0, z0), (60, 0, z1), (-60, 0, z1)], ROAD, None, 0)
    for s in (-1, 1):
        _quad(cam, p, [(s * KERB4, 0.15, z0), (s * SHOP4, 0.15, z0), (s * SHOP4, 0.15, z1), (s * KERB4, 0.15, z1)], PAVE, None, 0)
        _quad(cam, p, [(s * KERB4, 0, z0), (s * KERB4, 0.15, z0), (s * KERB4, 0.15, z1), (s * KERB4, 0, z1)], KERB, INK, 1.4)
        _quad(cam, p, [(s * (KERB4 + 0.03), 0.152, z0), (s * (KERB4 + 0.25), 0.152, z0), (s * (KERB4 + 0.25), 0.152, z1),
                       (s * (KERB4 + 0.03), 0.152, z1)], KERB, None, 0)
        for z in np.arange(math.floor(z0 / 1.5) * 1.5, z1, 1.5):        # paving slabs
            if abs(z - zc) < 70:
                cam.line(p, [(s * (KERB4 + 0.25), 0.152, z), (s * SHOP4, 0.152, z)], (150, 130, 136), 1.0)
    for dx in (-0.12, 0.12):
        _quad(cam, p, [(dx - 0.05, 0.01, z0), (dx + 0.05, 0.01, z0), (dx + 0.05, 0.01, z1), (dx - 0.05, 0.01, z1)], (236, 196, 70), None, 0)
    for z in np.arange(math.floor(z0 / 6) * 6, z1, 6.0):
        for x in (-3.5, 3.5):
            _quad(cam, p, [(x - 0.06, 0.01, z), (x + 0.06, 0.01, z), (x + 0.06, 0.01, z + 3), (x - 0.06, 0.01, z + 3)], (236, 232, 228), None, 0)


def shop_block(img, cam, p, b, hole=None):
    """One shop block on the street, its front on the road: shop glass and doors under a sign band and striped
    awnings, two rows of windows above. hole: (z, t since impact) when the cruiser has burst into this front."""
    s = b['side']
    xf, xb = s * SHOP4, s * (SHOP4 + 14)
    x0, x1 = min(xf, xb), max(xf, xb)
    faces = S.obox(((x0 + x1) / 2, 0.15, (b['z0'] + b['z1']) / 2), (x1 - x0, b['h'], b['z1'] - b['z0']), 0, cols={'all': b['col']})
    for f in faces:
        if not f.seen(cam):
            continue
        cam.poly(p, f.pts, G.shade(b['col'], f.n, 0.25), INK, 2.2)
        if abs(f.n[0]) < 0.5:
            continue
        xo = xf - s * 0.01
        Q = lambda z0, z1, y0, y1: [(xo, y0, z0), (xo, y0, z1), (xo, y1, z1), (xo, y1, z0)]
        n = max(1, int((b['z1'] - b['z0']) / 4.2))
        wd = (b['z1'] - b['z0']) / n
        cam.poly(p, Q(b['z0'] + 0.3, b['z1'] - 0.3, 3.0, 3.75), G.dk_(b['awn'], 0.55), INK, 1.4)      # the sign band
        rng = np.random.RandomState(b['seed'])
        for k in range(n):
            za, zb = b['z0'] + k * wd + 0.35, b['z0'] + (k + 1) * wd - 0.35
            door = rng.rand() < 0.35
            cam.poly(p, Q(za, zb, 0.35, 2.75), (70, 84, 104), INK, 1.4)                                  # shop glass
            if door:
                zm = (za + zb) / 2
                cam.poly(p, Q(zm - 0.55, zm + 0.55, 0.2, 2.5), (96, 70, 70), INK, 1.4)
            cam.poly(p, Q(za + 0.2, za + 0.55, 0.5, 2.6), (120, 138, 156), None, 0)                    # a glint
            for y in np.arange(4.6, b['h'] - 1.0, 2.6):
                for zz in (za + 0.4, (za + zb) / 2 + 0.2):
                    if zz + 1.1 < zb:
                        cam.poly(p, Q(zz, zz + 1.1, y, y + 1.3), (96, 112, 132), INK, 1.2)
            # the awning: a striped slope out over the pavement
            ao = s * 1.1
            stripes = 6
            for q in range(stripes):
                c = b['awn'] if q % 2 == 0 else (246, 240, 232)
                zq0, zq1 = za + (zb - za) * q / stripes, za + (zb - za) * (q + 1) / stripes
                cam.poly(p, [(xo, 3.0, zq0), (xo, 3.0, zq1), (xo - ao, 2.55, zq1), (xo - ao, 2.55, zq0)], c, None, 0)
            cam.poly(p, [(xo, 3.0, za), (xo, 3.0, zb), (xo - ao, 2.55, zb), (xo - ao, 2.55, za)], None, INK, 1.4)
        if hole is not None:                                    # the burst front: a black ragged hole, fire inside
            zc, age = hole
            rr = np.random.RandomState(3)
            pts = [(xo - s * 0.02, 1.35 + 1.35 * math.sin(a) * rr.uniform(0.8, 1.05), zc + 1.9 * math.cos(a) * rr.uniform(0.8, 1.05))
                   for a in np.linspace(0, 2 * math.pi, 15, endpoint=False)]
            pts = [(x, max(0.18, y), z) for x, y, z in pts]
            cam.poly(p, pts, (44, 30, 36), INK, 2.0)
            cam.poly(p, [(x, 0.18 + (y - 0.18) * 0.45, zc + (z - zc) * 0.8) for x, y, z in pts], (150, 60, 40), None, 0)


S_REF = 0.32                     # passers-by and cops are drawn once at this size per view, then scaled (rule 61: fast)
_SPR = {}


def person_cached(img, cam, sp, key, neck, facing, lean=0.0):
    """A Glimpse (a passer-by, a cop through the glass): one drawing per (who, view, lean), scaled to the size the
    camera wants. Drawn fresh when it is nearer (bigger) than the drawing."""
    if cam.depth(neck) < 0.35:
        return
    (X, Y), k = cam.project(neck)
    if X < -400 or X > 1480 or Y < -500 or Y > 2600:
        return
    s = k * sp.get('height', 1.75) / FIG_H
    a = fig_yaw(cam, neck, facing)
    if s > S_REF * 1.1:
        j = V.standing(sp)
        j['lean'] = lean
        V.person(img, B.Cam(1.0), X, Y, s, sp, 0.0, a, j, None)
        return
    aq = int(round(a / 15.0)) * 15
    ck = (key, aq, int(round(lean / 4.0)))
    if ck not in _SPR:
        lay = Image.new('RGBA', (1080 * B.SS, 1920 * B.SS), (0, 0, 0, 0))
        j = V.standing(sp)
        j['lean'] = ck[2] * 4.0
        V.person(lay, B.Cam(1.0), 540, 700, S_REF, sp, 0.0, aq, j, None)
        bb = lay.getbbox()
        _SPR[ck] = (lay.crop(bb), (540 * B.SS - bb[0], 700 * B.SS - bb[1]))
    spr, (ax, ay) = _SPR[ck]
    f = s / S_REF
    w, h = max(1, int(spr.width * f)), max(1, int(spr.height * f))
    im = spr.resize((w, h), Image.LANCZOS)
    img.paste(im, (int(X * B.SS - ax * f), int(Y * B.SS - ay * f)), im)


def person_at(img, cam, sp, neck, facing, t=0.0, joints=None, head_dir=None):
    """A people-kit person drawn into the 3D street: the neck base at `neck` (world), facing `facing` (world, level);
    head_dir turns the head alone. Their size and facing come from the camera's ray to them (the perspective)."""
    if cam.depth(neck) < 0.35:
        return None
    (X, Y), k = cam.project(neck)
    if X < -400 or X > 1480 or Y < -500 or Y > 2600:
        return None
    s = k * sp.get('height', 1.75) / FIG_H
    a = fig_yaw(cam, neck, facing)
    hy = fig_yaw(cam, neck, head_dir) if head_dir is not None else None
    return V.person(img, B.Cam(1.0), X, Y, s, sp, t, a, joints, hy)


def _axes(cam, at):
    L = S._norm((at[0] - cam.pos[0], 0.0, at[2] - cam.pos[2]))
    right = S._norm(S._cross((0.0, 1.0, 0.0), L))
    return right, (-L[0], 0.0, -L[2])


def fig_yaw(cam, at, d):
    right, toward = _axes(cam, at)
    return math.degrees(math.atan2(S._dot(d, right), S._dot(d, toward)))


def to_fig(cam, at, a, w):
    """A world direction in a drawn person's own frame (x across, y down, z forward) for a person at `at` drawn at
    yaw `a` (degrees): the inverse of views.project."""
    right, toward = _axes(cam, at)
    sx, tw = S._dot(w, right), S._dot(w, toward)
    r = math.radians(a)
    return (sx * math.cos(r) - tw * math.sin(r), -w[1], sx * math.sin(r) + tw * math.cos(r))


def unlean(v, lean):
    L = math.radians(lean)
    x, y, z = v
    return (x, y * math.cos(L) - z * math.sin(L), y * math.sin(L) + z * math.cos(L))


# ---- Jason: seated (pistol flat on his chest), leaning out of the window, four shots, back in
SEAT_J = (0.42, 1.02, 0.05)
OUT_J = (1.24, 1.60, -0.15)       # sitting on the sill, his body outside the car beside the roof


def jason4(t):
    """Jason's state at t in the Tulip's frame: k (0 seated .. 1 out), neck, facing angle (degrees from forward,
    + toward the car's right), lean, aim weight (0 gun on chest .. 1 arm out at the lead cruiser), recoil, flash."""
    k = smooth((t - 0.35) / 1.25) * (1 - smooth((t - 4.55) / 1.05))   # a real climb: a beat to brace, then out
    neck = tuple(a + (b - a) * k for a, b in zip(SEAT_J, OUT_J))
    neck = (neck[0] - 0.12 * math.sin(math.pi * k), neck[1] + 0.05 * math.sin(math.pi * k), neck[2])   # up, then out
    aim = smooth((t - 1.15) / 0.5) * (1 - smooth((t - 4.25) / 0.45))
    rec, flash = 0.0, 0.0
    for ts in SHOTS:
        w = t - ts
        if 0 <= w < 0.25:
            rec = max(rec, 14.0 * math.exp(-w / 0.07))
        if 0 <= w < 1.0 / 12:
            flash = 1.0
    return dict(k=k, neck=neck, face=140.0 * k, lean=6.0 * k, aim=aim, rec=rec, flash=flash)


def jason_layer(img, cam, tul, t, lead):
    js = jason4(t)
    sp = GC.cast()['jason']
    neck = tul.body_pt(js['neck'])
    a_face = math.radians(tul.yaw + js['face'])
    F = (math.sin(a_face), 0.0, math.cos(a_face))
    target = lead.body_pt((-0.35, 1.25, 0.9))                 # the cruiser's windscreen in front of its driver
    look = S._norm(S._sub(target, neck))
    if cam.depth(neck) < 0.35:
        return
    yaw_fig = fig_yaw(cam, neck, F)
    j = V.standing(sp)
    j['lean'] = js['lean']
    sh = j['shR']                   # the outboard arm once he has turned round (views' R)
    # the aim: the shoulder-to-windscreen line in his own frame, kicked up by the recoil
    d = to_fig(cam, neck, yaw_fig, look)
    d = S._norm((d[0], d[1] - math.tan(math.radians(js['rec'])), d[2]))
    d = S._norm(unlean(d, js['lean']))
    reach = (FG.UPPER + FG.FORE) * 0.93
    aim_hand = S._add(sh, S._mul(d, reach))
    chest = (14.0, 175.0, 62.0)                             # the gun hand flat on his chest
    w = js['aim']
    hand = tuple(c + (a - c) * w for c, a in zip(chest, aim_hand))
    if w > 0.35:
        dd = S._sub(hand, sh)
        L = math.sqrt(S._dot(dd, dd))
        hand = S._add(sh, S._mul(dd, min(1.0, reach / max(L, 1e-6))))
    V.arm_to(j, 'R', hand, 'down' if w > 0.5 else 'in', 'fist')
    gun_dir = tuple(c + (a - c) * w for c, a in zip((0.15, -1.0, 0.25), d))
    if js['k'] > 0.05:                                      # the free hand grips the roof's edge as he climbs out
        grip = tul.body_pt((0.84, 1.36, 0.25))
        rel = S._mul(S._sub(grip, neck), 1.0 / (sp['height'] / FIG_H))
        g = unlean(to_fig(cam, neck, yaw_fig, rel), js['lean'])
        shl = j['shL']
        dg = S._sub(g, shl)
        Lg = math.sqrt(S._dot(dg, dg))
        rmax = (FG.UPPER + FG.FORE) * 0.95
        if Lg > rmax:
            g = S._add(shl, S._mul(dg, rmax / Lg))
        rest = j['wrL']
        kk = smooth((js['k'] - 0.05) / 0.3)
        V.arm_to(j, 'L', tuple(a + (b - a) * kk for a, b in zip(rest, g)), 'out', 'palm')
    j['props'].append(PC.glock('R', flash=js['flash'], aim3=S._norm(gun_dir), size=1.4))   # big enough to read on a phone
    j['grip'] = {'R'}
    head = look if w > 0.2 else F
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    (X, Y), kpx = cam.project(neck)
    V.person(lay, B.Cam(1.0), X, Y, kpx * sp['height'] / FIG_H, sp, t, yaw_fig, j, fig_yaw(cam, neck, head))
    # the car's lower body hides what of him is inside it (the door below the sill, the bonnet)
    mask = Image.new('L', img.size, 0)
    md = ImageDraw.Draw(mask)
    hw, yt, zl = 1.0, 0.97, 2.66
    boxes = [((1, 0, 0), [(hw, -3, -zl), (hw, yt, -zl), (hw, yt, zl), (hw, -3, zl)]),
             ((-1, 0, 0), [(-hw, -3, -zl), (-hw, yt, -zl), (-hw, yt, zl), (-hw, -3, zl)]),
             ((0, 0, 1), [(-hw, -3, zl), (hw, -3, zl), (hw, yt, zl), (-hw, yt, zl)]),
             ((0, 0, -1), [(-hw, -3, -zl), (hw, -3, -zl), (hw, yt, -zl), (-hw, yt, -zl)]),
             ((0, 1, 0), [(-hw, yt, 0.75), (hw, yt, 0.75), (hw, yt, zl), (-hw, yt, zl)]),      # the bonnet
             ((0, 1, 0), [(-hw, yt, -zl), (hw, yt, -zl), (hw, yt, -1.95), (-hw, yt, -1.95)])]  # the boot
    for n, pts in boxes:
        w3 = [tul.body_pt(q) for q in pts]
        nw = S._norm(tul.body_dir(n))
        if S._dot(nw, S._sub(cam.pos, w3[0])) <= 0:
            continue
        q2 = cam.clip(w3)
        if len(q2) > 2:
            md.polygon([(x * B.SS, y * B.SS) for x, y in q2], fill=255)
    a = np.asarray(lay.split()[3], np.uint8).copy()
    a[np.asarray(mask) > 0] = 0
    lay.putalpha(Image.fromarray(a))
    img.alpha_composite(lay)


def tulip_inside(t):
    def paint(lay, cam, car):
        c = GC.cast()
        F = S._norm(car.body_dir((0, 0, 1)))
        F = (F[0], 0.0, F[2])
        seats = [('her', (0.0, 0.98, -0.80)), ('lucia', (-0.42, 1.02, 0.05))]
        for who, at in sorted(seats, key=lambda s: -math.dist(car.body_pt(s[1]), cam.pos)):
            person_at(lay, cam, c[who], car.body_pt(at), F, t)
    return paint


def cop_inside(i, t, lead=False):
    def paint(lay, cam, car):
        F = S._norm(car.body_dir((0, 0, 1)))
        F = (F[0], 0.0, F[2])
        j = V.standing(_cop(i))
        if lead:                                          # flinches at each hit, thrown about in the slew
            for ts in SHOTS[1:]:
                if 0 <= t - ts < 0.3:
                    j['lean'] = -14 * (1 - (t - ts) / 0.3)
            u = getattr(car, 'u', 0)
            if u > 0:
                j['lean'] = 10 * math.sin(u * 9) * math.exp(-u)
        person_cached(lay, cam, _cop(i), 'cop%d' % i, car.body_pt((-0.42, 1.12, 0.0)), F, j.get('lean', 0.0))
    return paint


# ---- effects through flying_whales_fx (metres, z up there): FxCam turns our y-up world into theirs
class FxCam:
    def __init__(self, cam):
        self.cam, self.focal, self.size = cam, cam.focal * B.SS, (1080 * B.SS, 1920 * B.SS)

    def screen(self, p):
        q = (float(p[0]), float(p[2]), float(p[1]))
        (x, y), _ = self.cam.project(q)
        return np.array([x * B.SS, y * B.SS]), self.cam.depth(q)


def wz(p):
    return np.array([p[0], p[2], p[1]], float)


def jet_lumps(t):
    """The hydrant's water: a column thrown up from the broken stump, falling back round it."""
    if HYDRANT is None or t < HYDRANT[0]:
        return []
    th, (hx, hz) = HYDRANT
    out = []
    for tb in np.arange(th, t, 1.0 / 60):
        rng = np.random.RandomState(int(tb * 6000) % (1 << 30))
        age = t - tb
        v = np.array([rng.normal(0.1, 0.18), rng.normal(0.0, 0.18), rng.uniform(10.5, 13.0)])   # a column, not a spray
        ramp = min(1.0, (tb - th) / 0.15 + 0.4)
        v[2] *= ramp
        p = np.array([hx, hz, 0.55]) + v * age + np.array([0.35 * age, 0, -0.5 * FX.G * age * age])   # the wind leans its top
        if p[2] < 0.15:
            continue
        r = rng.uniform(0.16, 0.24) * (1.0 + 0.5 * min(1.0, age))
        out.append((p, r, rng.rand() < 0.6, v + np.array([0, 0, -FX.G * age])))
    return out


def glass_bits(t):
    """Shop glass thrown out of the burst front (pale blue chunks that land on the pavement and stay)."""
    if IMPACT is None or t < IMPACT[0]:
        return []
    ti, (xi, zi), yi = IMPACT
    zc = zi + 2.6 * math.cos(math.radians(yi))
    rng = np.random.RandomState(12)
    out = []
    for n in range(26):
        p0 = np.array([SHOP4 - 0.05, zc + rng.uniform(-1.8, 1.8), rng.uniform(0.4, 2.6)])
        v = np.array([-rng.uniform(2.0, 6.0), rng.uniform(-2.5, 2.5), rng.uniform(0.5, 4.5)])
        age = t - ti
        tl = (v[2] + math.sqrt(v[2] ** 2 + 2 * FX.G * (p0[2] - 0.16))) / FX.G     # when it lands
        a = min(age, tl)
        p = p0 + v * a + np.array([0, 0, -0.5 * FX.G * a * a])
        spin = rng.uniform(-12, 12) * a
        out.append((p, rng.uniform(0.06, 0.16), spin, int(rng.randint(1 << 20))))
    return out


def hit_bits(t, lead):
    """Each shot: a spark and glass grit off the cruiser where it hits (the first off the bonnet)."""
    out = []
    for n, ts in enumerate(SHOTS):
        age = t - ts
        if not (0 <= age < 0.35):
            continue
        at = lead.body_pt((-0.5, 0.92, 1.6)) if n == 0 else lead.body_pt((-0.40, 1.28, 0.95))
        rng = np.random.RandomState(50 + n)
        for q in range(9):
            v = np.array([rng.normal(0, 1.6), rng.normal(0, 1.6), rng.uniform(0.8, 3.0)])
            p = wz(at) + v * age + np.array([0, 0, -0.5 * FX.G * age * age])
            out.append((p, rng.uniform(0.025, 0.05), age * 9, int(rng.randint(1 << 20)), n == 0))
        out.append(('flash', wz(at), age, n))
    return out


SMOKE4 = []
if IMPACT:                       # one joined column: born inside the flame tips (so it grows out of the fire), rising
    _r = np.random.RandomState(31)
    _ti, (_xi, _zi), _yi = IMPACT
    _zc = _zi + 2.6 * math.cos(math.radians(_yi))
    for _k in range(44):         # the first ones where the fireball burns out, the rest out of the fire, close-packed
        _tb = _ti + 0.25 + _k * 0.065 + _r.uniform(0, 0.03)
        _y = 1.3 + _r.uniform(0, 0.7) + (1.6 if _k < 6 else 0.0)
        SMOKE4.append(FX.Puff(_tb, (SHOP4 - 0.5 + _r.uniform(-0.4, 0.3), _zc + _r.uniform(-0.9, 0.9), _y),
                              (_r.uniform(-0.8, -0.1), _r.uniform(-0.4, 0.4), _r.uniform(0.3, 1.0)), _r.uniform(1.6, 2.4),
                              _r.uniform(0.6, 0.9), _r.uniform(1.6, 2.3), 3.4, 'smoke', int(_r.randint(1 << 20)), tau=0.5))
TYRE4 = []
for _k, _tb in enumerate(np.arange(SHOTS[-1] + 0.1, (IMPACT[0] if IMPACT else SHOT4_LEN), 1.0 / 24)):
    _c = lead_at(_tb)
    for _sx in (-1, 1):
        _p = _c.ground_pt((_sx * 0.86, 0.3, -1.4))
        TYRE4.append(FX.Puff(_tb, wz(_p), (0, 0, 0.3), 0.5, 0.3, 1.0, 1.4, 'steam', 900 + 2 * _k + (_sx > 0)))


def fx_items(cam, t, lead):
    """The effects as (depth, draw) pairs, to sort in with the cars and people."""
    fc = FxCam(cam)
    items = []
    lumps = jet_lumps(t)
    if lumps:
        d = cam.depth((HYDRANT[1][0], 2.0, HYDRANT[1][1]))
        spr = FX.lumps_sprite(fc, lumps, d)
        if spr:
            items.append((d - 0.5, spr.paste))
    if IMPACT and t >= IMPACT[0]:
        ti, (xi, zi), yi = IMPACT
        front = lead_at(ti).body_pt((0.0, 1.0, 2.4))
        age = t - ti
        d = cam.depth(front)
        spr = FX.fireball_sprite(fc, wz(front) + np.array([-0.4, 0.0, -0.4 - 2.5 * min(age, 1.0)]), 1.8, age, 21, d)   # rises half as fast: stays on the car
        if spr:
            items.append((d - 3.0, spr.paste))                    # the fireball engulfs the car's front
        if age > 0.35:
            zc = zi + 2.6 * math.cos(math.radians(yi))
            spr = FX.fire_sprite(fc, np.array([SHOP4 - 0.2, zc, 0.25]), np.array([0, 1.0, 0]), 1.6, 2.4, t, 5, d)
            if spr:
                items.append((d + 0.5, spr.paste))
        spr = FX.puffs_sprite(fc, SMOKE4, t, d)
        if spr:
            items.append((d + 0.3, spr.paste))
        gl = glass_bits(t)
        its = [(FX.chunk_poly(fc, p, r, sp, sd), (196, 222, 236), None, None) for p, r, sp, sd in gl]
        spr = FX.pieces_sprite([i for i in its if i[0]], d, ol=3.0)
        if spr:
            items.append((d - 1.0, spr.paste))
    spr = FX.puffs_sprite(fc, TYRE4, t, 0)
    if spr:
        items.append((cam.depth((lead.pos[0], 0.5, lead.pos[1])) + 1.5, spr.paste))
    hb = hit_bits(t, lead)
    for h in hb:
        if isinstance(h[0], str):
            _, at, age, n = h
            if age < 1.0 / 12:
                s, dd = fc.screen(at)
                r = fc.focal * 0.16 / max(dd, 1.0)
                b = FX._blob(s[0], s[1], r, 70 + n, n=7)
                spr = FX.shape_sprite([((255, 210, 90), [b]), ((255, 250, 220), [FX._scaled(b, 0.5)])], dd, ol=3.0)
                if spr:
                    items.append((dd - 0.6, spr.paste))
    bits = [(FX.chunk_poly(fc, p, r, sp, sd), (255, 220, 120) if spark else (214, 232, 240), None, None)
            for p, r, sp, sd, spark in (h for h in hb if not isinstance(h[0], str))]
    spr = FX.pieces_sprite([b for b in bits if b[0]], 0, ol=2.5)
    if spr:
        items.append((cam.depth((lead.pos[0], 1.2, lead.pos[1])) - 2.0, spr.paste))
    return items


OVERLAP_OK4 = [('effect', 'lead cruiser', 'the fireball, flames and smoke engulf the crashed car on purpose (Sam: not hidden in smoke, but on fire)'),
               ('effect', 'hydrant', 'the water jet rises out of the broken hydrant'),
               ('effect', 'effect', 'smoke and fire overlap each other, both see-through')]


def shot4(t, record=None):
    GC.cast()
    B.SS = 2                     # the cast loads at 1; the street, the cars and the people all draw at 2 here
    FX.SIZE = (1080 * B.SS, 1920 * B.SS)
    img = B.canvas((240, 170, 170))
    tul = tulip4(t)
    lead = lead_at(t)
    chasers = [chaser_at(t, 1), chaser_at(t, 2)]
    cam = shot4_cam(t, tul)
    p = S.pen(img)
    strip_ground(img, cam, p)
    hole = None
    if IMPACT and t >= IMPACT[0]:
        hole = (IMPACT[1][1] + 2.6 * math.cos(math.radians(IMPACT[2])), t - IMPACT[0])
    blocks = [b for b in BLOCKS4 if -40 < (b['z0'] + b['z1']) / 2 - cam.pos[2] < 160 or True]
    for b in sorted(blocks, key=lambda b: -math.dist(cam.pos, (b['side'] * (SHOP4 + 7), b['h'] / 2, (b['z0'] + b['z1']) / 2))):
        if cam.depth((b['side'] * SHOP4, 1.0, b['z0'])) < -2 and cam.depth((b['side'] * SHOP4, 1.0, b['z1'])) < -2:
            continue
        if min(abs(b['z0'] - cam.pos[2]), abs(b['z1'] - cam.pos[2])) > 140 and not (b['z0'] < cam.pos[2] < b['z1']):
            continue
        h = hole if hole and b['side'] == 1 and b['z0'] < hole[0] < b['z1'] else None
        shop_block(img, cam, p, b, h)
    items = []
    for pp in PEOPLE4:
        x, z = pp['at']
        d = cam.depth((x, 1.0, z))
        if 0.2 < d < 70:
            a = math.radians(pp['face'])
            items.append((f"person {pp['i']}", d, lambda im, pp=pp, x=x, z=z, a=a: person_cached(
                im, cam, _walker(pp['i']), pp['i'], (x, 0.15 + _walker(pp['i']).get('height', 1.75) * 928 / FIG_H, z),
                (math.sin(a), 0.0, math.cos(a)))))
    for k, (x, z) in enumerate(PALMS4):
        d = cam.depth((x, 3.0, z))
        if 0.5 < d < 140:
            if True:                 # always drawn: a palm slides in from the frame's edge, never pops in mid-frame
                items.append((f'palm {k}', d, lambda im, x=x, z=z, k=k: palm(im, cam, S.pen(im), (x, z), seed=k)))
    if HYDRANT:
        hx, hz = HYDRANT[1]
        d = cam.depth((hx, 0.5, hz))
        if t < HYDRANT[0]:
            items.append(('hydrant', d, lambda im: hydrant(im, cam, S.pen(im), (hx, hz))))
        else:
            items.append(('hydrant', d, lambda im: hydrant_stump(im, cam, S.pen(im), (hx, hz))))
    for k, (c, ins) in enumerate(((lead, cop_inside(0, t, True)), (chasers[0], cop_inside(1, t)), (chasers[1], cop_inside(2, t)))):
        d = cam.depth((c.pos[0], 0.8, c.pos[1]))
        if d > 0.5:
            items.append(('lead cruiser' if k == 0 else f'cruiser {k + 1}', d, lambda im, c=c, ins=ins: G.draw_car(im, cam, c, t=t, inside=ins)))
    items += [(f'effect {k}', d, fn) for k, (d, fn) in enumerate(fx_items(cam, t, lead))]
    d_t = cam.depth((tul.pos[0], 0.8, tul.pos[1]))

    def tulip_and_jason(im):
        G.draw_car(im, cam, tul, t=t, inside=tulip_inside(t))
        jason_layer(im, cam, tul, t, lead)
    items.append(('tulip and jason', d_t, tulip_and_jason))
    for _, d, fn in sorted(items, key=lambda e: -e[1]):
        fn(img)
    if record is not None:
        record += items
    light_wash(img, cam, [lead] + chasers, t)
    return img


def hydrant_stump(img, cam, p, at, col=(232, 196, 60)):
    x, z = at
    for part in (S.cylinder((x, 0.15, z), 0.13, 0.22, dict(side=G.dk_(col, 0.9), top=(70, 60, 50))),
                 S.cylinder((x, 0.15, z), 0.17, 0.08, dict(side=G.dk_(col, 0.8), top=col))):
        for f in part:
            if f.seen(cam):
                f.draw(img, cam, p)



def clip(frame_fn, length, out, frames_dir=None, fps=FPS):
    import tempfile
    d = frames_dir or tempfile.mkdtemp()
    os.makedirs(d, exist_ok=True)
    n = int(round(length * fps))
    for i in range(n):
        im = frame_fn(i / fps)
        im.convert('RGB').resize((1080, 1920), Image.LANCZOS).save(os.path.join(d, f'f{i:04d}.png'))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(d, 'f%04d.png'),
                    '-vf', 'fps=24,format=yuv420p', '-c:v', 'libx264', '-crf', '22', '-preset', 'medium', out], check=True)
    print('wrote', out, f'{os.path.getsize(out) / 1e6:.1f} MB', n, 'drawings')


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == 'shot2':
        fd = a[a.index('--frames') + 1] if '--frames' in a else None
        clip(shot2, SHOT2_LEN, a[1], fd)
    elif len(a) >= 2 and a[0] == 'shot4':
        fd = a[a.index('--frames') + 1] if '--frames' in a else None
        clip(shot4, SHOT4_LEN, a[1], fd)
    elif len(a) >= 2 and a[0] == 'layers':           # rule 17: anything against anything, every listed thing
        import viewchecks as VC
        shots = {'shot2': (shot2, SHOT2_LEN, OVERLAP_OK2), 'shot4': (shot4, SHOT4_LEN, OVERLAP_OK4)}
        faults = []
        for nm in a[1:]:
            fn, ln, ok = shots[nm]
            faults += VC.layer_faults(fn, ln, allowed=ok, label=nm)
        print('\n'.join(faults) or 'layers: clean')
    elif len(a) >= 3 and a[0] == 'still4':
        shot4(float(a[1])).convert('RGB').resize((1080, 1920), Image.LANCZOS).save(a[2], quality=90)
    elif len(a) >= 3 and a[0] == 'still2':
        shot2(float(a[1])).convert('RGB').resize((1080, 1920), Image.LANCZOS).save(a[2], quality=90)
    else:
        print(__doc__)
