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
import body as B                 # noqa: E402  the one kit (burnham kept its own SS: the street drew at half size, chat 13)
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


def sky(img, cam=None):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for y in range(0, img.height, 6):
        k = y / img.height
        c = tuple(int(a + (b - a) * min(1, k * 1.6)) for a, b in zip(SKY_TOP, SKY_LOW))
        d.line([(0, y), (img.width, y)], fill=c + (255,), width=6)
    img.alpha_composite(lay)
    if cam is not None:
        backdrop(img, cam)


# ---- the backdrop (Sam, chat 11: "the street ends in blank void"; "some white cloud streaks"): Vice City far off at
# the end of every street, and cloud streaks, both at the horizon's distance: they turn with the camera, never slide
# past it (a city kilometres away does not move when a car drives 100 m).
FAR = 1500.0
HAZE = (246, 190, 178)                       # the sunset haze the far towers fade into
TOWER_COLS = [(250, 214, 226), (196, 234, 226), (252, 236, 196), (214, 214, 244), (250, 222, 200), (232, 214, 246),
              (178, 220, 236), (240, 240, 232)]


def _far(cam, az, el, dist=FAR):
    """A point `dist` from the camera at azimuth az (degrees from +z toward +x) and elevation el (degrees)."""
    a, e = math.radians(az), math.radians(el)
    return (cam.pos[0] + dist * math.cos(e) * math.sin(a), cam.pos[1] + dist * math.sin(e),
            cam.pos[2] + dist * math.cos(e) * math.cos(a))


def _mix(a, b, k):
    return tuple(int(x + (y - x) * k) for x, y in zip(a, b))


def _make_towers():
    """Downtown Vice City all round the horizon, densest down the two streets (azimuth 0 and 180) and the cross
    street (90, 270): pastel deco towers with stepped tops, glass towers, a few spires, palms in front."""
    rng = np.random.RandomState(1986)
    out = []
    for centre, spread, n in ((0, 26, 16), (180, 26, 16), (90, 30, 12), (270, 30, 12), (45, 40, 8), (135, 40, 8),
                              (225, 40, 8), (315, 40, 8)):
        for _ in range(n):
            az = centre + rng.normal(0, spread / 2.2)
            w = rng.uniform(2.2, 5.5)
            h = rng.uniform(4.0, 13.0) * (1.3 if abs(((az - centre) + 180) % 360 - 180) < 8 else 1.0)
            kind = rng.choice(['deco', 'glass', 'slab', 'spire'], p=[0.4, 0.25, 0.25, 0.1])
            out.append(dict(az=az, w=w, h=h, kind=kind, col=TOWER_COLS[rng.randint(len(TOWER_COLS))],
                            dist=FAR * rng.uniform(0.92, 1.0), seed=int(rng.randint(1 << 20))))
    out.sort(key=lambda b: -b['dist'])
    return out


TOWERS = _make_towers()
CLOUDS = [(az, el, ln * 1.3, th * 2.6) for az, el, ln, th in
          [(-8, 12, 26, 0.9), (14, 19, 34, 1.1), (172, 13, 30, 1.0), (196, 22, 22, 0.8), (190, 8, 18, 0.6),
           (80, 15, 28, 1.0), (102, 25, 20, 0.8), (262, 11, 30, 1.0), (285, 20, 24, 0.9), (40, 9, 22, 0.7),
           (140, 17, 26, 0.9), (225, 15, 28, 1.0), (320, 14, 26, 0.9), (-30, 28, 30, 1.0), (160, 30, 26, 0.9),
           # shot 2's upper sky (its low camera looks up to ~60 degrees; chat 13 judged one streak too few): chat 14
           (6, 38, 30, 1.1), (32, 45, 26, 1.0), (-16, 50, 24, 0.9), (20, 57, 22, 0.8)]]


def backdrop(img, cam):
    fwd = S._norm(S._sub(cam.at, cam.pos)) if hasattr(cam, 'at') else None
    p = S.pen(img)

    def seen(az, el=2.0):
        if fwd is None:
            return True
        q = S._norm(S._sub(_far(cam, az, el), cam.pos))
        return S._dot(q, fwd) > 0.05
    # cloud streaks: long thin lozenges, white over a pink belly
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    lp = S.pen(lay)
    for az, el, ln, th in CLOUDS:
        if not seen(az, el):
            continue
        for dy, col, k in ((-0.35 * th, (238, 176, 196), 1.0), (0.0, (255, 252, 250), 0.92)):
            pts = []
            for u in np.linspace(-1, 1, 15):
                pts.append(_far(cam, az + u * ln / 2, el + dy + th * 0.5 * (1 - u * u) ** 0.7 * (1 + 0.25 * math.sin(u * 7 + az))))
            for u in np.linspace(1, -1, 15):
                pts.append(_far(cam, az + u * ln / 2 * k, el + dy - th * 0.35 * (1 - u * u) ** 0.9))
            cam.poly(lp, pts, col + (235,), None, 0)
    img.alpha_composite(lay)
    # the far haze band the road runs into
    for az0 in range(0, 360, 30):
        if seen(az0 + 15, 0):
            cam.poly(p, [_far(cam, az0, -1.2), _far(cam, az0 + 31, -1.2), _far(cam, az0 + 31, 0.6), _far(cam, az0, 0.6)],
                     HAZE, None, 0)
    for b in TOWERS:
        if not seen(b['az'], b['h'] / 2):
            continue
        col = _mix(b['col'], HAZE, 0.35)
        dk = _mix(col, (120, 96, 120), 0.22)
        a0, a1, h, D = b['az'] - b['w'] / 2, b['az'] + b['w'] / 2, b['h'], b['dist']
        F = lambda az, el: _far(cam, az, el, D)
        if b['kind'] == 'deco':                         # stepped crown
            cam.poly(p, [F(a0, -1.2), F(a1, -1.2), F(a1, h * 0.8), F(a0, h * 0.8)], col, INK, 1.1)
            cam.poly(p, [F(a0 + b['w'] * 0.15, h * 0.8), F(a1 - b['w'] * 0.15, h * 0.8), F(a1 - b['w'] * 0.15, h * 0.92),
                         F(a0 + b['w'] * 0.15, h * 0.92)], col, INK, 1.1)
            cam.poly(p, [F(a0 + b['w'] * 0.32, h * 0.92), F(a1 - b['w'] * 0.32, h * 0.92), F(a1 - b['w'] * 0.32, h),
                         F(a0 + b['w'] * 0.32, h)], col, INK, 1.1)
            for el in np.arange(0.6, h * 0.78, 0.9):        # window bands
                cam.poly(p, [F(a0 + 0.2, el), F(a1 - 0.2, el), F(a1 - 0.2, el + 0.3), F(a0 + 0.2, el + 0.3)], dk, None, 0)
        elif b['kind'] == 'glass':                      # a blue-green glass tower catching the sunset
            gc = _mix((120, 170, 196), HAZE, 0.35)
            cam.poly(p, [F(a0, -1.2), F(a1, -1.2), F(a1, h), F(a0, h)], gc, INK, 1.1)
            cam.poly(p, [F(a0 + b['w'] * 0.15, h * 0.1), F(a0 + b['w'] * 0.35, h * 0.1), F(a0 + b['w'] * 0.35, h * 0.95),
                         F(a0 + b['w'] * 0.15, h * 0.95)], _mix(gc, (255, 220, 210), 0.45), None, 0)
        elif b['kind'] == 'spire':
            cam.poly(p, [F(a0, -1.2), F(a1, -1.2), F(a1, h * 0.75), F(a0, h * 0.75)], col, INK, 1.1)
            cam.poly(p, [F(a0 + b['w'] * 0.2, h * 0.75), F(a1 - b['w'] * 0.2, h * 0.75), F(b['az'], h * 1.15)], col, INK, 1.1)
        else:                                           # a plain slab with window rows
            cam.poly(p, [F(a0, -1.2), F(a1, -1.2), F(a1, h * 0.7), F(a0, h * 0.7)], col, INK, 1.1)
            for el in np.arange(0.5, h * 0.66, 0.7):
                cam.poly(p, [F(a0 + 0.25, el), F(a1 - 0.25, el), F(a1 - 0.25, el + 0.25), F(a0 + 0.25, el + 0.25)], dk, None, 0)
    # a row of palm silhouettes along the far boulevard, in front of the towers
    rng = np.random.RandomState(7)
    for az in np.arange(0, 360, 2.2):
        az2 = az + rng.uniform(-0.6, 0.6)
        if not seen(az2, 1):
            continue
        hh = rng.uniform(2.2, 3.6)
        D = FAR * 0.8
        pc = _mix((96, 120, 104), HAZE, 0.4)
        cam.line(p, [_far(cam, az2, -0.5, D), _far(cam, az2 + 0.12, hh, D)], pc, 1.4)
        for k in range(5):
            ang = -70 + k * 35
            cam.line(p, [_far(cam, az2 + 0.12, hh, D), _far(cam, az2 + 0.12 + 1.1 * math.sin(math.radians(ang)),
                                                              hh - 0.6 + 0.5 * math.cos(math.radians(ang)), D)], pc, 3.0)


def ground(img, cam, p):
    _quad(cam, p, [(-1400, 0, -1400), (1400, 0, -1400), (1400, 0, 1400), (-1400, 0, 1400)], ROAD, None, 0)
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
    sky(img, cam)
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

import leanout as LO              # noqa: E402  (WOB: Sam's v7 note 9, the two-second wobble)
WOB = LO.WOB
SHOT4_LEN = 6.2 + WOB            # chat 23: the dead cop's car wobbles two seconds before it crashes (Sam, v7 note 9)
SHOT3_LEN = 3.0                  # shot 3: the windscreen three-shot, world t -3..0, flowing straight into shot 4
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


# Lucia's wheel (degrees, + to the car's right) through shot 3 (world t -3..0): sharp jerks round the traffic, each
# answered by the car a beat later (a twitch of yaw and a roll away from the turn); calm by shot 4.
WHEEL3 = [(-3.0, 0), (-2.75, 0), (-2.55, 34), (-2.25, 30), (-2.05, -26), (-1.75, -22), (-1.55, 8), (-1.0, 4),
          (-0.80, 38), (-0.55, 34), (-0.35, -12), (-0.10, 0), (0.0, 0)]


def wheel3(t):
    if t <= WHEEL3[0][0] or t >= WHEEL3[-1][0]:
        return 0.0
    for a, b in zip(WHEEL3, WHEEL3[1:]):
        if a[0] <= t <= b[0]:
            return a[1] + (b[1] - a[1]) * smooth((t - a[0]) / (b[0] - a[0]))
    return 0.0


def tulip4(t):
    z = V4 * t
    x = LANE4 + 0.10 * math.sin(t * 1.7)
    yaw = math.degrees(math.atan(0.10 * 1.7 * math.cos(t * 1.7) / V4))
    w = wheel3(t - 0.12)                       # the car answers the wheel a beat late
    car = G.Car('tulip', pos=(x + 0.006 * w, z), yaw=yaw + 0.10 * w, roll=0.7 * math.sin(t * 2.3) - 0.07 * w, pitch=0.5,
                spin=z / 0.34)
    car.wheel = wheel3(t)
    car.open_windows = OPEN4
    return car


# ---- the lead cruiser's path: chasing, hit, slewing over the kerb and the hydrant into the shop front
# chat 21: Lucia pulls away as Jason climbs out: the lead cruiser drops back 3.8 m and edges 0.55 m out, so the
# lean-out's straight gun arm (leanout.TARGET, the approved K4) points at its windscreen (at 3.9 m the line ran
# through the Tulip's own back pillar). Shot 3 (t < 0) is untouched.
LEAD_DZ, LEAD_DX, LEAD_RAMP = 3.8, 0.55, 1.8


def _lead_track():
    dt = 1.0 / 240
    th = SHOTS[-1]
    rows, x, z, head, imp, hyd = [], None, None, 0.0, None, None
    for i in range(int(SHOT4_LEN / dt) + 2):
        t = i * dt
        u = t - th
        if u <= 0:
            x = LANE4 - 0.15 + LEAD_DX * smooth(t / LEAD_RAMP) + 0.3 * math.sin(t * 2.1 + 1.0)
            z = V4 * t - GAPS[0] - LEAD_DZ * smooth(t / LEAD_RAMP)
            head = math.degrees(math.atan(0.3 * 2.1 * math.cos(t * 2.1 + 1.0) / V4))
            yaw, lift, crush = head, 0.0, 0.0
        elif u <= WOB:                                           # v7 note 9: the dead weight on the wheel: the
            env = smooth(u / 0.35) * (1 - 0.35 * smooth((u - 1.3) / 0.7))   # car weaves across the lanes (2.5 swings,
            head = -14.0 * env * math.sin(2 * math.pi * u / 0.8)            # 0.5 m each way), still at speed
            x += V4 * math.sin(math.radians(head)) * dt
            z += V4 * math.cos(math.radians(head)) * dt
            yaw, lift, crush = head * 1.2, 0.0, 0.0
        elif imp is None:
            u2 = u - WOB
            head = 34.0 * smooth(u2 / 0.45)
            v = V4 * (1 - 0.25 * min(1.0, u2 / 0.8))
            x += v * math.sin(math.radians(head)) * dt
            z += v * math.cos(math.radians(head)) * dt
            yaw = head + 30.0 * smooth(u2 / 0.5)                # the back end swings out: it slews
            lift = 0.0
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
        if imp is None and u > WOB:
            for zc, amt in ((1.50, 1.0), (-1.40, 0.8)):
                wx = x + S.rot_y((0.86, 0, zc), yaw)[0]
                kerb += amt * max(0.0, 1 - abs(wx - KERB4) / 0.5)
        rows.append(dict(t=t, pos=(x, z), yaw=yaw, crush=crush, kerb=kerb, u=u))
    return rows, imp, _hydrant_spot(rows, imp)


def _inside(r, h, pad):
    """The hydrant point h in the car's own frame at row r: (across, along) and whether it is under the body."""
    a = math.radians(r['yaw'])
    dx, dz = h[0] - r['pos'][0], h[1] - r['pos'][1]
    lx, lz = dx * math.cos(a) - dz * math.sin(a), dx * math.sin(a) + dz * math.cos(a)
    return lx, lz, abs(lx) < 0.97 + pad and abs(lz) < 2.58 + pad


def _hydrant_spot(rows, imp):
    """v7 notes 6 and 7: the hydrant stands where the cruiser's front strikes it, and its stump is clear of the car
    once it has passed (at rest it sat UNDER the crashed car, so the water came up through the bonnet). Searched over
    the pavement: struck by the front (not the side), 0.15-0.5 s before the shop, the stump never under the car again."""
    if imp is None:
        return None
    best = None
    for hx in np.arange(KERB4 + 0.45, SHOP4 - 0.6, 0.15):
        for hz in np.arange(imp[1][1] - 6.0, imp[1][1] + 4.0, 0.15):
            hit = None
            for r in rows:
                if r['t'] > imp[0] + 0.05:
                    break
                lx, lz, ins = _inside(r, (hx, hz), 0.12)
                if ins:
                    hit = (r['t'], lz, abs(lx))
                    break
            if hit is None or hit[1] < 1.9 or not 0.15 <= imp[0] - hit[0] <= 0.5:
                continue
            if any(_inside(r, (hx, hz), 0.25)[2] for r in rows if r['t'] > hit[0] + 0.3):
                continue
            sc = abs(imp[0] - hit[0] - 0.3) + 0.2 * hit[2]         # about 0.3 s before the shop, near the middle
            if best is None or sc < best[0]:
                best = (sc, hit[0], (float(hx), float(hz)))
    return (best[1], best[2]) if best else None


LEAD, IMPACT, HYDRANT = _lead_track()
if IMPACT:
    LO.HOLD = (IMPACT[0], IMPACT[0] + 1.09)          # Jason's flinch and nod from the crash's own moment


def lead_at(t):
    if t < 0:                                  # shot 3 (before shot 4's clock): just chasing, close behind
        x = LANE4 - 0.15 + 0.3 * math.sin(t * 2.1 + 1.0)
        head = math.degrees(math.atan(0.3 * 2.1 * math.cos(t * 2.1 + 1.0) / V4))
        car = G.Car('cruiser', pos=(x, V4 * t - GAPS[0]), yaw=head, spin=(V4 * t - GAPS[0]) / 0.37)
        car.u = t - SHOTS[-1]
        return car
    r = LEAD[min(len(LEAD) - 1, max(0, int(round(t * 240))))]
    shatter = 0.0
    for ts, c in zip(SHOTS, CRAZE):
        if t >= ts:
            shatter = c
    u = r['u']
    u2 = u - WOB
    roll = -7.0 * smooth(u2 / 0.4) * (1 - smooth((u2 - 0.6) / 0.3)) if u2 > 0 else 0.0
    if 0 < u <= WOB:
        roll = 0.25 * r['yaw']                                 # the body leans out on each swing
    car = G.Car('cruiser', pos=r['pos'], yaw=r['yaw'], roll=roll + 3.0 * r['kerb'], pitch=2.5 * r['kerb'] - 3.0 * r['crush'],
                steer=(-22.0 * smooth(u2 / 0.3) if u2 > 0 else (0.9 * r['yaw'] if u > 0 else 0.0)), spin=(V4 * min(t, IMPACT[0]) - GAPS[0]) / 0.37,
                crush=r['crush'], shatter=shatter, lift=0.06 * r['kerb'])
    car.u = u
    return car


def chaser_at(t, i):
    """Cruisers 2 and 3: weaving behind; after the crash they swerve to the inner lane round it."""
    gap = GAPS[i]
    z = V4 * t - gap
    sw = smooth((t - (SHOTS[-1] + WOB + 0.2 + 0.35 * i)) / 0.7)
    x = LANE4 - 0.2 + 0.35 * math.sin(t * 1.9 + 2 * i) - 3.4 * sw
    dsw = 3.4 * (smooth((t + 0.02 - (SHOTS[-1] + WOB + 0.2 + 0.35 * i)) / 0.7) - sw) / 0.02
    yaw = math.degrees(math.atan((0.35 * 1.9 * math.cos(t * 1.9 + 2 * i) - dsw) / V4))
    return G.Car('cruiser', pos=(x, z), yaw=yaw, roll=-0.08 * yaw, pitch=0.4, steer=yaw * 0.8, spin=z / 0.37)


# ---- the camera: keys in the Tulip's own frame (x right, y up, z forward), eased from key to key
CAM4 = [  # (t, position, look-at, focal) in the Tulip's frame. B1 and B6 are shot 3's exact frame; chat 21: B3-B5 over
    # beside his window (the rebuilt lean-out's gun arm runs back beside the roof: from the old keys out by the front
    # wing it was hidden behind his own head, the "stump" again; over his shoulder it ran straight down the lens)
    (0.00, (0.00, 1.62, 4.40), (0.00, 1.02, -0.60), 2000),      # shot 3's exact frame (CAM3): the cut is invisible
    (0.45, (0.00, 1.62, 4.40), (0.00, 1.02, -0.60), 2000),
    # chat 24 (v7 note 4, the arm, THIRD time; Sam: "Shots 0.92-2:42 have the exact same arm problem"): every key
    # from chat 21 to 23 sat AHEAD of him (z +0.8) while he faces back at the cruiser, so we saw his back and the gun
    # arm ran away from the lens from behind his head: a tube with no shoulder, whatever its size. Now the lens goes
    # round to his FRONT side, out on the pavement a little behind him: his face and chest at three-quarters, the
    # gun arm 70 degrees across the line of sight (its full length, shoulder to hand), then a pan along his line of
    # fire onto the lead cruiser for shots 3 and 4 (the cruiser and his face cannot share a tall frame from here)
    (1.10, (2.20, 1.55, 2.30), (0.95, 1.20, -0.30), 1300),      # round the front corner as he rises to the window
    (1.70, (3.70, 1.35, -1.25), (0.80, 1.28, -0.60), 1650),     # his front side: face, chest, the arm across
    (2.40, (3.70, 1.35, -1.25), (0.75, 1.28, -0.80), 1650),     # held through shots 1 and 2
    (2.70, (3.70, 1.35, -1.25), (0.40, 1.27, -7.70), 1000),     # along his line of fire onto the cruiser
    (2.95, (3.70, 1.35, -1.25), (0.50, 1.28, -7.70), 1000),
    (3.10, (3.70, 1.35, -1.25), (0.45, 1.27, -7.75), 1225),     # the push for the hit (focal scaled to the distance)
    (3.50, (3.70, 1.35, -1.25), (0.40, 1.25, -7.80), 1225),
    (3.95, (1.90, 1.50, 0.80), (0.35, 1.05, -9.00), 1250),     # over the road beside his door (on the pavement
    (4.90, (1.90, 1.50, 0.80), (0.40, 1.05, -9.20), 1250),     # the passers-by walked through the lens)
    (5.10, (2.40, 1.45, 0.80), (1.37, 1.27, -8.20), 1100),
    (5.36, (2.90, 1.45, 0.80), (2.71, 1.29, -8.49), 1450),
    (3.70 + WOB, (2.00, 2.00, 4.50), (2.00, 0.50, -14.0), 1600),     # out ahead of the bonnet, looking back past him
    (4.55 + WOB, (2.00, 2.00, 4.50), (2.20, 0.50, -14.0), 1850),     # a slow push on the fire through the hold
    (5.15 + WOB, (1.55, 1.70, 2.80), (0.60, 1.20, -2.40), 1250),
    (5.75 + WOB, (0.00, 1.62, 4.40), (0.00, 1.02, -0.60), 2000),
    (6.20 + WOB, (0.00, 1.62, 4.40), (0.00, 1.02, -0.60), 2000),
]


CAM3 = ((0.00, 1.62, 4.40), (0.00, 1.02, -0.60), 2000)   # shot 3: just over the bonnet, level, the glass filling the frame


def shot3_cam(t, car):
    pos, at, focal = CAM3
    rng = np.random.RandomState(int((t + 10) * 24))
    return S.Cam(car.ground_pt(pos), car.ground_pt(at), focal, shake=(rng.uniform(-2.0, 2.0), rng.uniform(-1.6, 1.6)))


def shot3(t, record=None):
    return world4(t - SHOT3_LEN, shot3_cam, record)


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
        z = -300.0                   # from -300: shot 3 runs 3 s before shot 4 and looks back down the street
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
        z = -260.0
        while z < 200:
            z += rng.uniform(3.0, 9.0)
            out.append(dict(at=(side * rng.uniform(8.2, 9.5), z), face=rng.choice([0.0, 180.0, 90.0 * -side]),
                            i=len(out), walk=rng.uniform(0, 1)))
    return out


PEOPLE4 = _strip_people()
PALMS4 = [((7.6 if s < 0 else 9.2) * s, z) for k, (s, z) in enumerate((s, z) for z in np.arange(-280, 220, 21.0) for s in (-1, 1))
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


# ---- the passers-by (Sam, chat 11: "walking, watching, ducking at each shot, running from the crash", feet on the
# pavement every frame). Each is a walker (along the pavement) or a watcher (faces the road); at the first shot all
# within 45 m duck (crouch, arms over the head, a reaction delay by distance); after the crash those within 22 m of it
# run away from it, the rest stand up and stare at the fire.
WALK_V, RUN_V = 1.3, 4.6


def _stride(j, ph, amp, lift, swing):
    for sd, sg in (('L', 1), ('R', -1)):
        c = math.sin(ph) * sg
        j['foot' + sd] = (j['foot' + sd][0], ANKLE - lift * max(0.0, math.cos(ph) * sg), 6.0 + amp * c)
        w = j['wr' + sd]
        j['wr' + sd] = (w[0], w[1] - 0.25 * swing * abs(c), w[2] - swing * c)
        e = j['el' + sd]
        j['el' + sd] = (e[0], e[1], e[2] - 0.45 * swing * c)


ANKLE = V.ANKLE_Y


CRASH_Z = LEAD[-1]['pos'][1]      # where the crashed lead cruiser comes to rest on the pavement (chat 22: it moved 4 m
CRASH_CLEAR = 3.4                 # back with the drop-back; two passers-by ran through it): nobody stands within this


def crowd(pp, t):
    """(x, z, facing, joints, head direction) of passer-by pp at world time t. One on the crash's pavement who would be
    standing where the cruiser lands is moved along the pavement clear of it (chat 22), and runners run away from the
    crashed car itself, so no run crosses it."""
    if 'dz' not in pp:
        pp['dz'] = 0.0
        if IMPACT and pp['at'][0] > 0:
            zi = _crowd(pp, IMPACT[0])[1]
            if abs(zi - CRASH_Z) < CRASH_CLEAR:
                pp['dz'] = (CRASH_CLEAR - abs(zi - CRASH_Z)) * (1.0 if zi >= CRASH_Z else -1.0)
            for dz in sorted((d * 0.5 for d in range(-24, 25)), key=abs):   # and clear of the cruiser's whole path
                if not _in_path(pp, pp['dz'] + dz):                        # up the pavement (chat 22: a woman
                    pp['dz'] += dz                                         # crouched where it ploughed in)
                    break
    return _crowd(pp, t, pp['dz'])


def _in_path(pp, dz):
    """Does passer-by pp (moved dz along the pavement) stand within 2 m of the lead cruiser from 3.0 s on?"""
    for k in range(40):
        t = 3.0 + k * 0.05
        x, z = _crowd(pp, t, dz)[:2]
        c = lead_at(t)
        a = math.radians(c.yaw)
        dx, dzz = x - c.pos[0], z - c.pos[1]
        u = dx * math.cos(a) - dzz * math.sin(a)                 # across the car
        v = dx * math.sin(a) + dzz * math.cos(a)                 # along it
        if abs(u) < 1.0 + 2.0 and abs(v) < 2.5 + 2.0:         # 2 m: a crouch closer looks run over
            return True
    return False


def _crowd(pp, t, dz=0.0):
    x0, z0 = pp['at']
    z0 += dz
    side = 1 if x0 > 0 else -1
    walker = pp['walk'] > 0.45
    dirz = 1.0 if pp['face'] == 0.0 else -1.0
    sp = _walker(pp['i'])
    j = V.standing(sp)
    tz = V4 * t                                            # the Tulip's z: where the noise is
    t_duck = SHOTS[0] + 0.12 + 0.010 * abs(z0 - tz) + 0.08 * (pp['i'] % 3)
    near_fire = IMPACT is not None and abs(z0 - (IMPACT[1][1] + 2.6)) < 22 and side > 0 or (
        IMPACT is not None and abs(z0 - IMPACT[1][1]) < 14)
    ducks = abs(z0 - V4 * SHOTS[0]) < 45
    sees_fire = IMPACT is not None and abs(z0 - (IMPACT[1][1] + 2.6)) < 60     # chat 14: a man strolled past the fireball
    t_stop = min(t_duck if ducks else 99.0, IMPACT[0] + 0.3 if sees_fire else 99.0)
    z = z0 + (dirz * WALK_V * (min(t, t_stop) + 3.2) if walker else 0.0)
    F = (0.0, 0.0, dirz) if walker else (-side * 1.0, 0.0, 0.0)
    head = None
    if walker and t < t_stop:
        ph = (min(t, t_stop) + 3.2 + pp['walk'] * 3) * math.pi * 1.9
        _stride(j, ph, 120.0, 40.0, 70.0)
        j['bob'] = 6 * abs(math.sin(ph))
    duck = smooth((t - t_duck) / 0.22) if ducks else 0.0
    t_run = (IMPACT[0] + 0.15 + 0.05 * (pp['i'] % 4)) if (IMPACT and near_fire and (ducks or sees_fire)) else 99.0
    up = smooth((t - (IMPACT[0] + 0.5 if IMPACT else 99)) / 0.4) if ((ducks or sees_fire) and not near_fire) else 0.0
    duck *= 1 - up
    if t > t_run:                                          # run from the fire, along the pavement, away from it
        z_run = z0 + (dirz * WALK_V * (min(t_run, t_stop) + 3.2) if walker else 0.0)
        away = 1.0 if (z_run > CRASH_Z if side > 0 else z_run > IMPACT[1][1] + 2.6) else -1.0
        u = t - t_run
        z += away * RUN_V * max(0.0, u - 0.15) * smooth(u / 0.3)
        F = (0.0, 0.0, away)
        j = V.standing(sp)
        ph = u * math.pi * 3.2
        _stride(j, ph, 210.0, 90.0, 140.0)
        j['lean'] = 16.0
        j['bob'] = 10 * abs(math.sin(ph))
        duck = 0.4 * (1 - smooth(u / 0.5))
    if j.get('bob'):                                       # the bob lowers the whole drawing, feet too: lift the feet
        for sd in ('L', 'R'):                              # back by it so they stay on the pavement (chat 15: sunk)
            fx, fy, fz = j['foot' + sd]
            j['foot' + sd] = (fx, fy - j['bob'], fz)
    if duck > 0:                                           # a crouch: body down, knees bent, head down, arms over it
        bob = 230.0 * duck
        j['bob'] = j.get('bob', 0.0) + bob
        for sd, sg in (('L', -1), ('R', 1)):
            fx, fy, fz = j['foot' + sd]
            j['foot' + sd] = (fx + sg * 40 * duck, fy - bob, fz + 60 * duck)
            j['knee_pole' + sd] = (0.25 * sg, 0.0, 1.0)
        j['lean'] = j.get('lean', 0.0) + 34.0 * duck
        if duck > 0.3:
            for sd, sg in (('L', -1), ('R', 1)):
                V.arm_to(j, sd, (sg * 40.0, -150.0, 60.0), 'out', 'palm')
    if IMPACT and up > 0.0:                                # stood up again: the whole body turns to the fire (chat 14:
        fz = IMPACT[1][1] + 2.6                            # a head alone cannot turn round to a fire behind them)
        a0, a1 = math.atan2(F[0], F[2]), math.atan2(SHOP4 - x0, fz - z)
        da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        a = a0 + da * up                                   # turning round over 0.4 s, never a flip
        F = (math.sin(a), 0.0, math.cos(a))
        head = None
    elif IMPACT and t > IMPACT[0] + 0.2 and t < t_run and not walker:
        fz = IMPACT[1][1] + 2.6
        head = S._norm((SHOP4 - x0, 0.0, fz - z))           # staring at the fire
    elif ducks and t < t_duck and abs(z0 - tz) < 30:
        head = S._norm((LANE4 - x0, 0.0, tz - z))           # turning to the roar of the chase
    return x0, z, F, j, head


def strip_ground(img, cam, p):
    sky(img, cam)
    zc = cam.pos[2]
    z0, z1 = zc - 160, zc + 160
    _quad(cam, p, [(-60, 0, zc - 1400), (60, 0, zc - 1400), (60, 0, zc + 1400), (-60, 0, zc + 1400)], ROAD, None, 0)
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


def person_cached(img, cam, sp, key, neck, facing, lean=0.0, roll=0.0):
    if abs(roll) > 0.5:                               # tipped over sideways about the hips (the dead cop, v7 note 8)
        if cam.depth(neck) < 0.35:
            return
        (X, Y), k = cam.project(neck)
        s = k * sp.get('height', 1.75) / FIG_H
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        person_cached(lay, cam, sp, key, neck, facing, lean)
        piv = (X * B.SS, (Y + 420 * s) * B.SS)
        lay = lay.rotate(-roll, resample=Image.BICUBIC, center=piv)
        img.alpha_composite(lay) if img.mode == 'RGBA' else img.paste(lay, (0, 0), lay)
        return
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


def fig_to_world(cam, at, a, v, mpu):
    """A point in a drawn person's own frame (person units from the neck: x across, y down, z forward), drawn at yaw
    `a`, back in the world (metres; mpu = metres per unit): the inverse of to_fig, for the solid check."""
    right, toward = _axes(cam, at)
    r = math.radians(a)
    sx = v[0] * math.cos(r) + v[2] * math.sin(r)
    tw = -v[0] * math.sin(r) + v[2] * math.cos(r)
    return (at[0] + mpu * (sx * right[0] + tw * toward[0]), at[1] - mpu * v[1], at[2] + mpu * (sx * right[2] + tw * toward[2]))


BODY_PTS = ('hipL', 'hipR', 'footL', 'footR', 'shL', 'shR', 'elL', 'elR', 'wrL', 'wrR')


def body_pts3(cam, neck, a, j, mpu, who, lean=0.0):
    """A drawn person's joints (and the knees, the hips' middle, the chest, the top of the head) in the world, for
    solid_faults. neck is the drawing's anchor; the upper body tipped by `lean` about the hips as views draws it."""
    bob = j.get('bob', 0.0)
    up = lambda v: V.leaned(v, lean) if lean else v
    out = [('neck', fig_to_world(cam, neck, a, up((0.0, bob, 0.0)), mpu)),
           ('head top', fig_to_world(cam, neck, a, up((0.0, -195.0 + bob, 0.0)), mpu))]
    for k in BODY_PTS:
        if k in j:
            v = j[k]
            if k.startswith(('hip', 'foot')):
                v = (v[0], v[1] + bob, v[2])
            else:
                v = up((v[0], v[1] + bob, v[2]))
            out.append((k, fig_to_world(cam, neck, a, v, mpu)))
    for sd in 'LR':
        if 'hip' + sd in j and 'foot' + sd in j:
            h, f = j['hip' + sd], j['foot' + sd]
            out.append(('knee' + sd, fig_to_world(cam, neck, a, ((h[0] + f[0]) / 2, (h[1] + f[1]) / 2 + bob, (h[2] + f[2]) / 2 + 40), mpu)))
    out.append(('waist', fig_to_world(cam, neck, a, (0.0, 450.0 + bob, 0.0), mpu)))
    out.append(('chest', fig_to_world(cam, neck, a, up((0.0, 220.0 + bob, 0.0)), mpu)))
    return out


def unlean(v, lean):
    L = math.radians(lean)
    x, y, z = v
    return (x, y * math.cos(L) - z * math.sin(L), y * math.sin(L) + z * math.cos(L))


# ---- Jason: seated (pistol flat on his chest), climbing out through the OPEN window to sit on its sill, four shots,
# back in. Built in the car's own frame in metres (hips, facing, lean, ankles), so every body point is known for
# viewchecks.solid_faults; then drawn flat, his lower half rubbed out only by what of the car is in front of his hips,
# his upper half only by what is in front of his chest (gta_cars.cover_masks).
MPU_J = 1.85 / FIG_H              # metres per person unit (Jason is 1.85 m)
SEAT_HIPS = (0.42, 0.18, 0.0)          # low in the seat: his head clears the roof rail (1.47), chat 14
J4_KEYS = [  # (t, hips, facing (deg, + toward the car's right), lean (deg forward), ankle L, ankle R)
    (0.00, (0.42, 0.18, 0.00), 0, 0, (0.32, 0.33, 0.70), (0.52, 0.33, 0.70)),
    (0.35, (0.42, 0.18, 0.00), 0, 0, (0.32, 0.33, 0.70), (0.52, 0.33, 0.70)),
    (0.85, (0.62, 0.62, 0.00), 75, 30, (0.40, 0.33, 0.25), (0.55, 0.33, 0.30)),    # up and turned: head out first
    (1.40, (0.86, 1.03, -0.02), 125, 12, (0.48, 0.45, -0.05), (0.62, 0.45, 0.12)),  # on the sill, turning back
    (1.70, (0.88, 1.03, -0.02), 160, 4, (0.48, 0.45, -0.05), (0.62, 0.45, 0.12)),   # sat on the sill: legs inside;
    # turned 160 (was 140) square to the lead cruiser: at 140 the gun arm crossed his chest and hid behind his back,
    # the stump Sam flagged in chat 11 (rule 30, chat 15); now arm, gun and flash read past his left shoulder
    (4.30, (0.88, 1.03, -0.02), 160, 4, (0.48, 0.45, -0.05), (0.62, 0.45, 0.12)),
    (4.85, (0.86, 1.03, -0.02), 115, 14, (0.48, 0.45, -0.05), (0.62, 0.45, 0.12)),
    (5.30, (0.62, 0.62, 0.00), 70, 28, (0.40, 0.33, 0.25), (0.55, 0.33, 0.30)),
    (5.80, (0.42, 0.18, 0.00), 0, 0, (0.32, 0.33, 0.70), (0.52, 0.33, 0.70)),
    (6.20, (0.42, 0.18, 0.00), 0, 0, (0.32, 0.33, 0.70), (0.52, 0.33, 0.70)),
]
GRIP_J = (0.72, 1.50, 0.20)
HIDE_JASON = [False]
import leanout as LO             # noqa: E402  the lean-out (chat 21)
LO.GUN[0] = 1.5                   # the pistol 1.5x in the film: readable at phone size
LO.FIRE[:] = [1 / 24, 1 / 24]     # 12 drawings a second: each shot's flash lands on one drawing (chat 21: 3 of 4 fell between)
import humancheck as HC           # noqa: E402  the body check (proposal big-body-moves)       # his free hand on the roof's front corner, over the open window


def jason4(t):
    """Jason at t in the Tulip's frame: hips, facing, lean, ankles, aim weight (0 gun on chest .. 1 arm out at the lead
    cruiser), recoil (deg), flash, out (0 seated .. 1 on the sill)."""
    for k0, k1 in zip(J4_KEYS, J4_KEYS[1:]):
        if k0[0] <= t <= k1[0]:
            e = smooth((t - k0[0]) / (k1[0] - k0[0]))
            L = lambda a, b: tuple(x + (y - x) * e for x, y in zip(a, b)) if isinstance(a, tuple) else a + (b - a) * e
            hips, face, lean, al, ar = (L(k0[i], k1[i]) for i in range(1, 6))
            break
    else:
        hips, face, lean, al, ar = J4_KEYS[-1][1:]
    aim = smooth((t - 1.30) / 0.45) * (1 - smooth((t - 4.20) / 0.40))
    rec, flash = 0.0, 0.0
    for ts in SHOTS:
        w = t - ts
        if 0 <= w < 0.25:
            rec = max(rec, 16.0 * math.exp(-w / 0.07))
        if 0 <= w < 1.0 / 12:
            flash = 1.0
    out = smooth((hips[1] - 0.18) / 0.85)
    return dict(hips=hips, face=face, lean=lean - 0.25 * rec, al=al, ar=ar, aim=aim, rec=rec, flash=flash, out=out)


def _leaned_pt(v, lean):
    return V.leaned(v, lean)


def _unleaned_pt(v, lean):
    """The inverse of views.leaned: an upper-body point back to the upright frame the arms are posed in."""
    if not lean:
        return v
    L = math.radians(lean)
    x, y, z = v
    dy = y - V.HIP_Y
    return x, V.HIP_Y + dy * math.cos(L) - z * math.sin(L), z * math.cos(L) + dy * math.sin(L)


JSP = {}
_JN = {'shL': 'shL', 'elL': 'elL', 'wrL': 'wrL', 'shR': 'shR', 'elR': 'elR', 'wrR': 'wrR', 'hipL': 'hipL',
       'hipR': 'hipR', 'knL': 'kneeL', 'knR': 'kneeR', 'anL': 'footL', 'anR': 'footR', 'neck': 'neck',
       'head': 'head top', 'waist': 'waist', 'pelvis': 'hips'}


def jason_face(t):
    """Jason's face through shot 4 (the acting rows, B1-B6; shot 3 is t < 0: looking hard at us)."""
    f = dict(mood='stern', squint=0.35, frown=0.07)                       # B1, B6: shot 3's hard look
    if 0.28 <= t < 0.40:                                                  # eyes flick to the mirror
        f['look'] = -0.7
    if 0.5 <= t < 1.75:                                                   # B2: teeth set, squinting into the wind
        f.update(squint=0.75, frown=0.10, mouth='v:E')
    elif 1.75 <= t < 3.0:                                                 # B3/B4: along the arm, mouth tight
        f.update(squint=0.85 if t < SHOTS[2] else 0.95, frown=0.11, mouth='v:rest')
    imp = IMPACT[0] if IMPACT else 99.0
    if imp + 0.05 <= t < imp + 0.95:                                      # B5: brows up, a flat impressed "huh"
        f.update(squint=0.1, frown=-0.03, brow_up=0.035, mouth='v:O' if t < imp + 0.5 else 'v:rest')
    elif 3.0 <= t < 4.55 + WOB:
        f.update(squint=0.5, frown=0.06)
    if any(0.0 <= t - ts < 0.085 for ts in SHOTS):                        # a blink on each shot
        f['blink'] = True
    return f


def jason_layer(img, cam, tul, t, lead, info=None):
    """Jason (chat 21 rebuild): the approved lean-out (leanout.at, Sam's Y 21 Nov) in the moving Tulip, drawn through
    this camera with the house's flat pieces; the car hides his legs, the dash and the roof rail per bone half."""
    base = JSP.setdefault('sp', dict(GC.cast()['jason'], mood='stern', squint=0.35, frown=0.07))
    face = dict(base, **jason_face(t))
    nod = 0.30 * bump(t, 0.36, 0.42, 0.52)                               # B1: the small decisive nod
    al, kw, used = LO.film_layer(img, cam, tul, max(t, 0.0), base, face, nod=nod, hide=HIDE_JASON[0])
    if kw.firing:                                                         # the body check: the gun as drawn
        hand, muzzle = LO.gun_pts(kw)
        target = lead.body_pt((-0.35, 1.25, 0.9))
        m, b0, tg = cam.P(tuple(muzzle)), cam.P(tuple(hand)), cam.P(target)
        HC.aim('Jason', m, (m[0] - b0[0], m[1] - b0[1]), tg, firing=True)
    if info is not None:
        pts = [(_JN[n], tuple(kw[n])) for n in _JN]
        pts.append(('chest', tuple((kw['waist'] + kw['neck']) / 2)))
        pts.append(('gun hand', tuple(LO.gun_pts(kw)[0])))
        erase = []
        for n, poly, bone in used:
            a_, b_ = bone.split('-') if '-' in bone else (bone, bone)
            erase.append((n, poly, {_JN.get(a_, a_), _JN.get(b_, b_)}))
        info.update(toggle=lambda on: HIDE_JASON.__setitem__(0, not on), pts3=pts, erase=erase,
                    may_touch=('the tulip\'s seat',))


# ---- inside the Tulip (shot 3's three-shot and shot 4's ends): each person posed in the car's own frame (metres),
# then drawn flat at the size and turn the camera gives them; the glass and the body rub out what they hide.
WHEEL_C, WHEEL_R = (-0.42, 0.87, 0.47), 0.19          # Lucia's wheel: centre (car frame) and rim radius. Chat 26
#   (F9): 8 cm lower in every shot, as shots 5-8 had it since chat 16: at 0.95 its rim ran across her mouth in shots 3-4
#   and dropped at the cut to shot 5
WHEEL_TILT = math.radians(32)                        # its face tipped back toward her
LINE2 = (1.00, [(0.00, 'etc'), (0.12, 'FV'), (0.24, 'E'), (0.38, 'L'), (0.48, 'AI'), (0.70, 'O'), (0.86, 'etc'),
                (0.95, 'rest')])                     # "It's very loud." (shot 3 time, s): the wince lands on "loud"


def wheel_pt(rot, ang, r=WHEEL_R):
    """A point on the wheel's rim (car frame): ang 0 = 3 o'clock, 90 = 12 o'clock, turned by rot (+ to the right)."""
    a = math.radians(ang - rot)
    u = r * math.cos(a)
    v = r * math.sin(a)
    return (WHEEL_C[0] + u, WHEEL_C[1] + v * math.cos(WHEEL_TILT), WHEEL_C[2] - v * math.sin(WHEEL_TILT))


def mouth_at(t3, line):
    t0, keys = line
    u = t3 - t0
    if u < 0 or u > keys[-1][0]:
        return None
    m = keys[0][1]
    for k, v in keys:
        if u >= k:
            m = v
    return 'v:' + m


def seated(lay, cam, car, who, neck_l, t, hands=(), over=None, head_dir=None, props=(), feet_z=0.62):
    """One person in a seat: neck at neck_l (car frame), hands on world targets [(side, car-frame point, pole, shape)]."""
    sp = dict(GC.cast()[who], **(over or {}))
    m = sp.get('height', 1.75) / FIG_H
    neck = car.body_pt(neck_l)
    F = S._norm(car.body_dir((0, 0, 1)))
    F = S._norm((F[0], 0.0, F[2]))
    a = fig_yaw(cam, neck, F)
    fig = lambda w: tuple(c / m for c in to_fig(cam, neck, a, S._sub(w, neck)))
    j = V.standing(sp)
    for sd, dx in (('L', -0.14), ('R', 0.14)):                # sat down: feet forward under the dash
        f = fig(car.body_pt((neck_l[0] + dx, 0.28, neck_l[2] + feet_z)))
        j['foot' + sd] = f
    for sd, at, pole, shape in hands:
        # hands are given by the person's own left and right (the car's left and right, they face forward); the kit's
        # 'L' arm is the one on the picture's left when a person faces us, i.e. their RIGHT arm (views.standing; front
        # view shL x < 0). Given straight across, each hand reached over to the other side: Lucia's crossed grip, Sam's
        # v4 note 1 and v7 note 1 (rule 30: the first fix moved the grip points, never the arm they went to).
        V.arm_to(j, {'L': 'R', 'R': 'L'}[sd], fig(car.body_pt(at)), pole, shape)
    j['props'] += list(props)
    return person_at(lay, cam, sp, neck, F, t, j, head_dir)


def spinner(lay, cam, at, t, r=0.045):
    """Her fidget spinner: three lobes round a hub, flat to the camera, a blur of turn."""
    if cam.depth(at) < 0.3:
        return
    (X, Y), k = cam.project(at)
    p = S.pen(lay)
    R_ = r * k
    rot = t * 14.0
    for i in range(3):
        a = rot + i * 2 * math.pi / 3
        cx, cy = X + 0.62 * R_ * math.cos(a), Y + 0.62 * R_ * math.sin(a) * 0.8
        p.ell(cx, cy, 0.42 * R_, 0.42 * R_ * 0.8, (64, 200, 214), INK, 1.6)
        p.ell(cx, cy, 0.17 * R_, 0.17 * R_ * 0.8, (220, 240, 244), None, 0)
    p.ell(X, Y, 0.30 * R_, 0.24 * R_, (240, 90, 160), INK, 1.6)


def cash_case(lay, cam, car):
    """The bulging case of cash beside her on the back seat (car frame), notes poking out of the zip."""
    p = S.pen(lay)
    x0, x1, y0, y1, z0, z1 = 0.16, 0.66, 0.42, 1.04, -0.98, -0.72
    bul = 0.03
    C = lambda x, y, z: car.body_pt((x, y, z))
    faces = [([C(x0, y0, z1 + bul), C(x1, y0, z1 + bul), C(x1, y1, z1 + bul), C(x0, y1, z1 + bul)], (120, 74, 46)),
             ([C(x0, y1, z0), C(x1, y1, z0), C(x1, y1, z1 + bul), C(x0, y1, z1 + bul)], (146, 92, 58)),
             ([C(x0, y0, z0), C(x0, y1, z0), C(x0, y1, z1 + bul), C(x0, y0, z1 + bul)], (104, 64, 40))]
    for pts, col in faces:
        cam.poly(p, pts, col, INK, 2.0)
    for i, x in enumerate((0.24, 0.34, 0.45, 0.55)):          # notes squeezed out of the zip along the top edge
        h = 0.05 + 0.025 * (i % 2)
        cam.poly(p, [C(x - 0.05, y1 - 0.01, z1 + bul + 0.01), C(x + 0.05, y1 - 0.01, z1 + bul + 0.01),
                     C(x + 0.06, y1 + h, z1 + bul - 0.02), C(x - 0.04, y1 + h, z1 + bul - 0.02)], (128, 186, 120), INK, 1.4)
    cam.line(p, [C(0.36, y1 + 0.04, (z0 + z1) / 2), C(0.36, y1 + 0.10, (z0 + z1) / 2), C(0.46, y1 + 0.10, (z0 + z1) / 2),
                 C(0.46, y1 + 0.04, (z0 + z1) / 2)], (60, 40, 30), 3.0)


def bench(lay, cam, car):
    """The back bench's backrest and the parcel shelf behind it (dark vinyl): what she sits against."""
    p = S.pen(lay)
    C = lambda x, y, z: car.body_pt((x, y, z))
    cam.poly(p, [C(-0.80, 0.98, -1.30), C(0.80, 0.98, -1.30), C(0.80, 0.98, -1.75), C(-0.80, 0.98, -1.75)], (70, 60, 58), INK, 1.6)
    cam.poly(p, [C(-0.80, 0.45, -1.10), C(0.80, 0.45, -1.10), C(0.80, 1.00, -1.30), C(-0.80, 1.00, -1.30)], (96, 70, 60), INK, 1.8)
    for x in (-0.27, 0.27):                       # the seams of the three cushions
        cam.line(p, [C(x, 0.50, -1.12), C(x, 0.97, -1.29)], (70, 50, 44), 1.4)


def steering_wheel(lay, cam, car, rot):
    p = S.pen(lay)
    rim = [car.body_pt(wheel_pt(rot, a)) for a in range(0, 361, 15)]
    cam.line(p, rim, (36, 32, 34), 7.0)
    hub = car.body_pt(WHEEL_C)
    for a in (180, 0, 270):
        cam.line(p, [hub, car.body_pt(wheel_pt(rot, a, WHEEL_R * 0.92))], (44, 40, 42), 4.0)
    cam.line(p, [hub, car.body_pt((WHEEL_C[0], WHEEL_C[1] - 0.16, WHEEL_C[2] + 0.22))], (44, 40, 42), 6.0)


def tulip_inside(t):
    t3 = t + SHOT3_LEN                                  # shot 3's own clock
    def paint(lay, cam, car):
        rot = getattr(car, 'wheel', 0.0)
        # her: hunched over the spinner, eyes down on it; a wince (eyes squeezed, brows up) on "loud"
        mo = mouth_at(t3, LINE2)
        wince = bump(t3, LINE2[0] + 0.40, LINE2[0] + 0.62, LINE2[0] + 1.5)
        her_over = dict(mood='phone', gaze_dy=0.7 * (1 - wince), squint=0.75 * wince, frown=-0.04 - 0.05 * wince)
        if mo:
            her_over['mouth'] = mo
        fid = 0.012 * math.sin(t * 19.0)                 # the nervous fidget: hands working the spinner
        her_neck = (0.0, 0.91, -0.80)
        spin_at = (0.0 + fid, 0.87, -0.50)       # held up nearer her face (she sits 6 cm lower, chat 14)
        her_hands = [('L', (-0.05 + fid, 0.85, -0.53), 'down', 'fist'), ('R', (0.05 + fid, 0.87, -0.50), 'down', 'fist')]
        lu_over = dict(mood='stern', squint=0.45, frown=0.09, brow_up=-0.01)
        lu_neck = (-0.42, 0.94, 0.05)
        carry = 0.28 * rot                               # chat 26: shots 5-8's grip (ten and two, fed), so the cut keeps her hands
        lu_hands = [('L', wheel_pt(rot, 150 - carry), 'down', 'fist'), ('R', wheel_pt(rot, 30 - carry), 'down', 'fist')]
        # shot 4's acting rows (chat 21): her hands over her ears from the first shot ("it's very loud"), eyes squeezed
        # shut; a peek at the fireball (one hand off an ear); back to the spinner. Lucia: a tight glance at Jason as he
        # climbs past and back, a flinch blink on each shot, her eyes up to the mirror at the crash.
        imp = IMPACT[0] if IMPACT else 99.0
        ears = smooth((t - SHOTS[0] + 0.06) / 0.12) * (1 - smooth((t - (imp + 1.1)) / 0.3))
        peek = bump(t, imp + 0.1, imp + 0.4, imp + 1.4)
        her_dir = None
        if ears > 0.01:
            ear = lambda sd, g: (her_neck[0] + g * 0.10, her_neck[1] + 0.17, her_neck[2] + 0.02)
            mix = lambda a, b, k: tuple(x + (y - x) * k for x, y in zip(a, b))
            her_hands = [('L', mix(her_hands[0][1], ear('L', -1), ears), 'out', 'palm'),
                         ('R', mix(her_hands[1][1], ear('R', 1), ears * (1 - peek)), 'out', 'palm' if peek < 0.5 else 'fist')]
            if t < imp:
                her_over.update(squint=1.0 * ears, frown=-0.06, gaze_dy=0.0)
            if peek > 0.3:
                her_over.update(squint=0.0, frown=-0.02, brow_up=0.03, gaze_dy=0.0)
                her_dir = S._norm(car.body_dir((0.9, 0.0, -0.6)))
        lu_dir = None
        if 0.0 <= t and (bump(t, 0.55, 0.75, 1.15) > 0.3 or bump(t, 4.65 + WOB, 4.85 + WOB, 5.3 + WOB) > 0.3):
            lu_dir = S._norm(car.body_dir((1.0, 0.0, 0.35)))
        if any(0.0 <= t - ts < 0.1 for ts in SHOTS):
            lu_over['blink'] = True
        if imp + 0.05 <= t < imp + 1.0:
            lu_over['gaze_dy'] = -0.6
        bench(lay, cam, car)
        order = sorted([('case', (0.4, 0.7, -0.85)), ('her', her_neck), ('lucia', lu_neck)],
                       key=lambda s: -math.dist(car.body_pt(s[1]), cam.pos))
        for who, at in order:
            if who == 'case':
                cash_case(lay, cam, car)
            elif who == 'her':
                seated(lay, cam, car, 'her', her_neck, t, her_hands, her_over, head_dir=her_dir, feet_z=0.55)
                if ears < 0.5:
                    spinner(lay, cam, car.body_pt(spin_at), t, r=0.065)
            else:
                seated(lay, cam, car, 'lucia', lu_neck, t, lu_hands, lu_over, head_dir=lu_dir)
                steering_wheel(lay, cam, car, rot)
    return paint


def lead_cop_lean(t):
    """The lead cop's lean through shot 4 (acting rows): shot 1 ducks a little, shots 2-3 flinch back; shot 4 hits him:
    his head snaps back, then he slumps onto the wheel and stays there, dead weight, thrown on at the hydrant and the
    shop front (fix 3, note 9: never upright, never swaying)."""
    hit = SHOTS[3]
    if t < hit:
        lean = 0.0
        if 0 <= t - SHOTS[0] < 0.3:
            lean = 10 * (1 - (t - SHOTS[0]) / 0.3)
        for ts in SHOTS[1:3]:
            if 0 <= t - ts < 0.3:
                lean = -14 * (1 - (t - ts) / 0.3)
        return lean, False
    u = t - hit
    lean = -18 * bump(u, 0.0, 0.05, 0.14) + 16 * smooth((u - 0.08) / 0.32)   # chat 23: 40 put him under the dash
    #                                                     once he also tips onto the door (lead_cop_roll): head kept in view
    for te, amt in ((HYDRANT[0] if HYDRANT else 99, 10), (IMPACT[0] if IMPACT else 99, 16)):
        if t >= te:
            lean += amt * math.exp(-(t - te) / 0.18) * smooth((t - te) / 0.05)
    return lean, u > 0.04


def lead_cop_roll(t):
    """v7 note 8 (a repeat of v4 note 9: "no death reaction by officer, stays still"): the first fix slumped him
    FORWARD onto the wheel, which from in front (where the camera is) barely changes his outline. Now the shot throws
    his head back and to the side, then he slides down and over onto the door (degrees, + toward the door), and his
    dead weight lolls with each swing of the weaving car and is thrown at the hydrant and the shop."""
    u = t - SHOTS[3]
    if u < 0:
        return 0.0, 0.0
    roll = 14 * bump(u, 0.0, 0.06, 0.2) + 28 * smooth((u - 0.12) / 0.45)
    if 0 < u < WOB:
        roll += 9 * math.sin(2 * math.pi * u / 0.8 - 1.2) * smooth(u / 0.4)
    for te, amt in ((HYDRANT[0] if HYDRANT else 99, 8), (IMPACT[0] if IMPACT else 99, 14)):
        if t >= te:
            roll += amt * math.exp(-(t - te) / 0.25) * smooth((t - te) / 0.05)
    return roll, 0.05 * smooth((u - 0.12) / 0.45)               # and he slides 5 cm down the seat


def cop_inside(i, t, lead=False):
    def paint(lay, cam, car):
        F = S._norm(car.body_dir((0, 0, 1)))
        F = (F[0], 0.0, F[2])
        lean, dead = lead_cop_lean(t) if lead else (0.0, False)
        roll, drop = lead_cop_roll(t) if lead else (0.0, 0.0)
        sp = _cop(i)
        if dead:                                      # eyes shut, mouth slack
            sp = dict(sp, blink=True, mouth='v:O')
        neck = car.body_pt((-0.42, 1.12 - drop, 0.0))
        if roll:                                      # toward the door: which way is that on screen?
            (dx, _), _ = cam.project(car.body_pt((-1.0, 1.12, 0.0)))
            (nx, _), _ = cam.project(neck)
            roll = roll if dx > nx else -roll
        person_cached(lay, cam, sp, 'cop%d%s' % (i, 'dead' if dead else ''), neck, F, lean, roll=roll)
    return paint


def blood_items(cam, t, lead):
    """Shot 4 hits the lead cop (fix 3): a mist of blood bursts against the inside of the crazed windscreen and fades;
    spatter stays on the glass, riding with the car through the slew and the crash."""
    hit = SHOTS[3]
    u = t - hit
    if u < 0:
        return []
    fc = FxCam(cam)
    rng = np.random.RandomState(77)
    pieces = []
    # hunt 2 (chat 22): laid on the windscreen, the blood sat off to one side of his head from the side-on camera
    # (parallax: the glass is 0.9 m in front of him), and read as a red rose on the outside. Now it hangs just in
    # front of his head (drawn at the glass's depth, so always over his face from any camera), spatter finer
    # chat 23 (v7 note 5, "a 2D effect that doesn't turn with the windscreen"): the spatter is laid ON the inside of
    # the windscreen, each drop a flat shape in the glass's own plane (it tips and turns with the car through the
    # weave, the slew and the crash), streaks running out from where the shot came through in front of his face
    gy0, gz0, gy1, gz1 = 1.05, 1.08, 1.55, -0.02                    # the cruiser's windscreen: bottom and top edge
    e2 = np.array([0.0, gy1 - gy0, gz1 - gz0]) / math.hypot(gy1 - gy0, gz1 - gz0)   # up the glass
    e1 = np.array([1.0, 0.0, 0.0])
    def on_glass(x, y):
        v = (y - gy0) / (gy1 - gy0)
        return np.array([x, y, gz0 + (gz1 - gz0) * v - 0.012])
    c0 = on_glass(-0.40, 1.30)
    grow = min(1.0, u / 0.08)
    for n in range(34):                                # spatter: stays
        ang = rng.uniform(0, 2 * math.pi)
        dist = abs(rng.normal(0, 0.10)) * grow
        cen = c0 + (e1 * math.cos(ang) + e2 * math.sin(ang)) * dist
        r = rng.uniform(0.008, 0.026) * (1.2 if dist < 0.04 else 1.0)
        el = 1.0 + 3.0 * min(1.0, dist / 0.12)          # drops further out are streaks pointing away from the hole
        ra = e1 * math.cos(ang) + e2 * math.sin(ang)
        rb = e1 * -math.sin(ang) + e2 * math.cos(ang)
        poly = []
        for q in range(14):
            a = 2 * math.pi * q / 14
            w = cen + ra * (r * el * math.cos(a)) + rb * (r * math.sin(a) * (1 - 0.3 * max(0, math.cos(a))))
            sc, d = fc.screen(wz(lead.body_pt(tuple(w))))
            if d < 0.5:
                poly = []
                break
            poly.append((float(sc[0]), float(sc[1])))
        if poly:
            pieces.append((poly, (150, 14, 22), None, None))
    if u < 0.3:                                        # the mist at his head: a quick puff, gone in 0.3 s
        for n in range(9):
            x, y = -0.42 + rng.normal(0, 0.12), 1.22 + rng.normal(0, 0.06)
            k = n / 9.0
            if k > 1.0 - u / 0.3:
                continue
            r = (0.025 + 0.045 * min(1.0, u / 0.12)) * rng.uniform(0.6, 1.0)
            s, d = fc.screen(wz(lead.body_pt((x, y + 0.06 * u, 0.18))))
            if d > 0.5:
                pieces.append((FX._blob(s[0], s[1], fc.focal * r / d, 400 + n, n=8), (196, 42, 48), None, None))
    if not pieces:
        return []
    dd = cam.depth(lead.body_pt((-0.38, 1.27, 0.93)))
    spr = FX.pieces_sprite(pieces[::-1], dd, ol=1.2)
    return [(dd - 0.05, spr.paste)] if spr else []


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


def hydrant_flight(t):
    """v7 note 6 ("no hydrant strike, no physicality: it should be hit and smash forward, like any object hit by a
    car"): struck by the cruiser's front, the hydrant's body breaks off its stump and is thrown ahead of the car, a
    little faster than it, spinning end over end, bouncing on the pavement and skidding to rest. Returns its base and
    top (world, y up) or None before the strike."""
    if HYDRANT is None or t < HYDRANT[0]:
        return None
    th, (hx, hz) = HYDRANT
    a, b = lead_at(th - 0.02), lead_at(th + 0.02)
    v = np.array([(b.pos[0] - a.pos[0]) / 0.04, 0.0, (b.pos[1] - a.pos[1]) / 0.04]) * 1.15
    v[1] = 3.2
    p = np.array([hx, 0.42, hz])
    w = 14.0                                           # end over end (radians a second), slowing on each bounce
    ang, dt, T = 0.0, 1.0 / 240, th
    while T < t:
        p += v * dt
        v[1] -= 9.81 * dt
        ang += w * dt
        if p[1] < 0.28 and v[1] < 0:                  # the pavement (0.15) plus its half-thickness
            p[1] = 0.28
            v[1] = -0.35 * v[1]
            v[0] *= 0.7
            v[2] *= 0.7
            w *= 0.6
        T += dt
    d = np.array([v[0], 0.0, v[2]])
    d = d / (np.linalg.norm(d) or 1.0)
    axis = np.array([0.0, 1.0, 0.0]) * math.cos(ang) + d * math.sin(ang)
    return p - axis * 0.27, p + axis * 0.27


def hydrant_body(img, cam, p, ends, col=(232, 196, 60)):
    """The struck hydrant's body in flight: a yellow barrel from base to top (flat, one ink outline), its cap."""
    a, b = ends
    if cam.depth(tuple(a)) < 0.4 or cam.depth(tuple(b)) < 0.4:
        return
    (ax, ay), ka = cam.project(tuple(a))
    (bx, by), kb = cam.project(tuple(b))
    t_ = np.array([bx - ax, by - ay])
    n = np.array([-t_[1], t_[0]]) / (np.linalg.norm(t_) or 1.0)
    ra, rb = 0.14 * ka, 0.12 * kb
    body = [tuple(np.array([ax, ay]) + n * ra), tuple(np.array([bx, by]) + n * rb),
            tuple(np.array([bx, by]) - n * rb), tuple(np.array([ax, ay]) - n * ra)]
    pen = S.pen(img)
    pen.poly(body, G.dk_(col, 0.9), INK, 2.0)
    pen.ell(bx, by, rb, rb, col, INK, 2.0)
    m = (np.array([ax, ay]) * 0.45 + np.array([bx, by]) * 0.55)
    for sg in (-1, 1):                                 # the two side nozzles
        q = m + n * sg * (ra + 0.05 * ka)
        pen.ell(q[0], q[1], 0.045 * ka, 0.045 * ka, G.dk_(col, 0.85), INK, 1.6)


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
        r = rng.uniform(0.26, 0.36) * (1.0 + 0.5 * min(1.0, age))   # fatter (chat 14: a thin jet read as a black stick)
        if p[2] < 1.9:                                 # v7 note 7: water never drawn inside the cruiser's body
            car = lead_at(t)
            a_ = math.radians(car.yaw)
            dx, dz = p[0] - car.pos[0], p[1] - car.pos[1]
            lx, lz = dx * math.cos(a_) - dz * math.sin(a_), dx * math.sin(a_) + dz * math.cos(a_)
            if abs(lx) < 0.97 + r and abs(lz) < 2.58 + r:
                continue
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
for _k, _tb in enumerate(np.arange(SHOTS[-1] + WOB + 0.1, (IMPACT[0] if IMPACT else SHOT4_LEN), 1.0 / 24)):
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
            items.append((d, spr.paste))                  # at the stump's own depth (v7 note 7: d - 0.5 put it
            #                                               in front of the cruiser parked beside it)
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
    items += blood_items(cam, t, lead)
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


OPEN4 = ((1, 1),)                # the Tulip's open windows (side, pane): Jason's, wound down


def street_solid(q):
    x, y, z = q
    if abs(x) > SHOP4 + 0.05 and y < 12:
        for b in BLOCKS4:
            if b['side'] * x > 0 and b['z0'] < z < b['z1'] and y < b['h']:
                return 'a shop wall'
    g = 0.15 if abs(x) > KERB4 else 0.0
    if y < g - 0.03:
        return 'the pavement' if g else 'the road'
    return None


def solids4(cam, cars):
    """The solids of shot 4 for viewchecks.solid_faults: the street (road, pavement, shop walls) and every car."""
    out = [('street', 0, None, dict(solid=street_solid, cam=cam))]
    for nm, c in cars:
        ow = OPEN4 if nm == 'tulip' else ()
        out.append((nm + ' (solid)', 0, None, dict(solid=lambda q, c=c, ow=ow: G.solid_at(c, q, ow))))
    return out


def shot4(t, record=None):
    return world4(t, shot4_cam, record)


def world4(t, cam_fn, record=None):
    """One frame of the chase street at world time t (shot 4's clock: shot 3 is t < 0) through cam_fn(t, tulip)."""
    GC.cast()
    B.SS = 2                     # the cast loads at 1; the street, the cars and the people all draw at 2 here
    FX.SIZE = (1080 * B.SS, 1920 * B.SS)
    img = B.canvas((240, 170, 170))
    tul = tulip4(t)
    lead = lead_at(t)
    chasers = [chaser_at(t, 1), chaser_at(t, 2)]
    cam = cam_fn(t, tul)
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
        x, z, F_, j_, hd = crowd(pp, t)
        d = cam.depth((x, 1.0, z))
        if 0.2 < d < 70:
            sp_ = _walker(pp['i'])
            hgt = sp_.get('height', 1.75)
            m_ = hgt / FIG_H
            neck_ = (x, 0.15 + 928 * m_, z)
            (gx, gy), _ = cam.project((x, 0.15, z))
            (_, ty), _ = cam.project((x, 0.15 + hgt, z))
            a_ = fig_yaw(cam, neck_, F_)
            inf = dict(pts3=body_pts3(cam, neck_, a_, j_, m_, 'p', lean=j_.get('lean', 0.0)), ground_px=(gx, gy),
                       height_px=gy - ty)
            if d < 38:                    # near: posed every frame (walking, ducking, running)
                fn = lambda im, sp_=sp_, neck_=neck_, F_=F_, j_=j_, hd=hd: person_at(im, cam, sp_, neck_, F_, t, j_, hd)
            else:                         # far: the one standing drawing, scaled (too small to read a pose)
                fn = lambda im, pp=pp, neck_=neck_, F_=F_: person_cached(im, cam, _walker(pp['i']), pp['i'], neck_, F_)
            items.append((f"person {pp['i']}", d, fn, inf))
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
            fl = hydrant_flight(t)
            if fl is not None:
                items.append(('hydrant body', cam.depth(tuple((fl[0] + fl[1]) / 2)),
                              lambda im, fl=fl: hydrant_body(im, cam, S.pen(im), fl)))
    for k, (c, ins) in enumerate(((lead, cop_inside(0, t, True)), (chasers[0], cop_inside(1, t)), (chasers[1], cop_inside(2, t)))):
        d = cam.depth((c.pos[0], 0.8, c.pos[1]))
        if d > 0.5:
            items.append(('lead cruiser' if k == 0 else f'cruiser {k + 1}', d, lambda im, c=c, ins=ins: G.draw_car(im, cam, c, t=t, inside=ins)))
    items += [(f'effect {k}', d, fn) for k, (d, fn) in enumerate(fx_items(cam, t, lead))]
    d_t = cam.depth((tul.pos[0], 0.8, tul.pos[1]))

    jinf = {}

    def tulip_and_jason(im):
        G.draw_car(im, cam, tul, t=t, inside=tulip_inside(t))
        jason_layer(im, cam, tul, t, lead, jinf)
    items.append(('tulip and jason', d_t, tulip_and_jason, jinf))
    for e in sorted(items, key=lambda e: -e[1]):
        e[2](img)
    if record is not None:
        record += items
        record += solids4(cam, [('tulip', tul)] + [('lead cruiser', lead)] + [(f'cruiser {k + 2}', c) for k, c in enumerate(chasers)])
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
    hc = HC.Writer(os.path.basename(out))           # the body check, every person, every drawing
    for i in range(n):
        HC.frame_begin()
        im = frame_fn(i / fps)
        hc.frame(i / fps, HC.frame_end(i / fps))
        im.convert('RGB').resize((1080, 1920), Image.LANCZOS).save(os.path.join(d, f'f{i:04d}.png'))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(d, 'f%04d.png'),
                    '-vf', 'fps=24,format=yuv420p', '-c:v', 'libx264', '-crf', '22', '-preset', 'medium', out], check=True)
    print('wrote', out, f'{os.path.getsize(out) / 1e6:.1f} MB', n, 'drawings')
    hc.finish(out, named='--body-named' in sys.argv)


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
    elif len(a) >= 2 and a[0] == 'bodies':           # rule 17's other half: bodies through solids, feet on the ground
        import viewchecks as VC
        shots = {'shot2': (shot2, SHOT2_LEN), 'shot4': (shot4, SHOT4_LEN)}
        fr = None
        if '--every' in a:
            k = int(a[a.index('--every') + 1])
        else:
            k = 1
        faults = []
        for nm in [x for x in a[1:] if x.startswith('shot')]:
            fn, ln = shots[nm]
            faults += VC.solid_faults(fn, ln, step=k, label=nm)
        print('\n'.join(faults) or 'bodies: clean')
    elif len(a) >= 3 and a[0] == 'still4':
        shot4(float(a[1])).convert('RGB').resize((1080, 1920), Image.LANCZOS).save(a[2], quality=90)
    elif len(a) >= 2 and a[0] == 'shot3':
        fd = a[a.index('--frames') + 1] if '--frames' in a else None
        clip(shot3, SHOT3_LEN, a[1], fd)
    elif len(a) >= 2 and a[0] == 'shot34':                     # shot 3 straight into shot 4, as the film plays them
        fd = a[a.index('--frames') + 1] if '--frames' in a else None
        clip(lambda t: world4(t - SHOT3_LEN, shot3_cam if t < SHOT3_LEN else shot4_cam), SHOT3_LEN + SHOT4_LEN, a[1], fd)
    elif len(a) >= 3 and a[0] == 'still3':
        shot3(float(a[1])).convert('RGB').resize((1080, 1920), Image.LANCZOS).save(a[2], quality=90)
    elif len(a) >= 3 and a[0] == 'still2':
        shot2(float(a[1])).convert('RGB').resize((1080, 1920), Image.LANCZOS).save(a[2], quality=90)
    else:
        print(__doc__)
