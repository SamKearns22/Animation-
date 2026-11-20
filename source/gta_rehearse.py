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
LEAD = 0.3                # an empty beat of junction before the car screams out
COPS = (LEAD + 0.85, LEAD + 1.45, LEAD + 2.05)


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


def shot2(t):
    img = B.canvas((240, 170, 170))
    states = [('tulip', car_at(t, LEAD, 1.0))] + [('cruiser', car_at(t, d, 0.55)) for d in COPS]
    cars = []
    for kind, st in states:
        c = G.Car(kind, pos=st['pos'], yaw=st['yaw'], roll=st['roll'], pitch=st['pitch'], steer=st['steer'], spin=st['spin'])
        c.st = st
        cars.append(c)
    cam = shot2_cam(t, cars)
    p = S.pen(img)
    street(img, cam, p)
    hydrant(img, cam, p, (-8.5, 16.8))         # on the pavement, clear of the car's way in
    tyre_smoke(img, cam, t, LEAD)
    live = [c for c in cars if c.st['s'] > -12 and cam.depth((c.pos[0], 1, c.pos[1])) > 0.5]
    for c in sorted(live, key=lambda c: -math.dist(cam.pos, (c.pos[0], 0.8, c.pos[1]))):
        G.draw_car(img, cam, c, t=t)
    block(img, cam, p, BLOCKS[0])             # the near block hides the cross street until the car rounds it
    light_wash(img, cam, cars[1:], t)
    return img


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
    elif len(a) >= 3 and a[0] == 'still2':
        shot2(float(a[1])).convert('RGB').resize((1080, 1920), Image.LANCZOS).save(a[2], quality=90)
    else:
        print(__doc__)
