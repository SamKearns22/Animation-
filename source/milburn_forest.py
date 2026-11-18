#!/usr/bin/env python3
"""Milburn, scene 6: the forest (chat 7, 17 Nov). Thick growth, deep green, shafts of light. Flat painted layers at
real depths that slide past at their own speeds as the camera travels right with the four (Sam's Y to the budget
stop: "the forest built as flat sliding layers"), and the effects from the greenery ahead: gunfire flashes, a
flamethrower's jet, two morning stars on chains.

MAP (rule 61)
  camera ........ CAM (level 1.4 m), YAW_VIEW (the drawn three-quarter view), V_EFF (how fast the ground slides
                  under a three-quarter walker), cam_x(t) (the camera's travel; eases to a stop on the gunfire)
  the world ..... ITEMS: every trunk, canopy clump, bush, fern and ground mark at (x, depth) in metres, made once
  layers ........ behind(t) (all behind the four: backdrop, light shafts, trunks 25/18/9 m, canopy, floor, the
                  track, undergrowth, the greenery ahead), in_front(t) (ferns and a trunk at 1.5 m: race past)
  effects ....... gunfire(img, t) (flashes in the leaves ahead, tracers over their heads), muzzle(img, X, Y, ang,
                  k, seed) (Swindon firing back), flame(img, t) (the jet whipping out of a bush), stars(img, t)
                  (two morning stars swinging down out of the trees)
  sheet ......... sheet(OUT): the forest empty at three moments, for looking at

    python3 source/milburn_forest.py sheet OUT.jpg
"""
import math
import os
import random
import sys
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ed import INK                 # noqa: E402
import milburn_sets as MS          # noqa: E402

W, H, SS = 1080, 1920, 2
CAM = MS.LevelCam(1.4, 990, 1450)
T0, T_GUN, T_FLAME, T_STARS, T1 = 31.3, 34.0, 34.8, 35.5, 38.9   # note 11: 2.7 s earlier
YAW_VIEW = 45.0                      # the three-quarter view the kit draws for yaw 40
V_EFF = 0.9 * math.sin(math.radians(YAW_VIEW))   # m/s across the screen: a walker's planted foot on the ground
STOP = 0.5                           # s: the camera eases to rest after the gunfire


def cam_x(t):
    """The camera's travel (m, to the right) since the shot began: walking pace, then easing to a stop."""
    t = max(T0, t)
    if t <= T_GUN:
        return V_EFF * (t - T0)
    u = min(1.0, (t - T_GUN) / STOP)
    return V_EFF * (T_GUN - T0) + V_EFF * STOP * (u - u * u / 2)


END_X = cam_x(T1)                    # where the camera rests (the greenery ahead is placed from here)

# colours: deep green, darker up in the canopy, hazier with distance
HAZE = (126, 168, 112)
CANOPY = (30, 72, 44)
LEAF = ((44, 104, 52), (58, 124, 60), (74, 142, 66))
BARK = (84, 66, 50)
BARK_D = (60, 46, 36)
EARTH = (122, 98, 66)
EARTH_D = (96, 76, 52)
FLOOR = (64, 92, 48)


def fog(c, d):
    """Colour c at depth d: hazier and paler the further off (flat steps, not a gradient per pixel)."""
    k = min(0.75, max(0.0, (d - 4.0) / 30.0))
    return MS.mix(c, HAZE, k)


def _P(x, d, z, cx):
    X, Y = CAM.p(x - cx, d, z)
    return X * SS, Y * SS


@lru_cache(None)
def items():
    """Every piece of the forest in metres: (depth, kind, x, args, seed)."""
    r = random.Random(606)
    out = []
    for d, n, rad in ((26.0, 26, 0.32), (18.0, 18, 0.38), (11.0, 12, 0.3), (8.0, 8, 0.24)):   # trunk rows
        span = d * 0.62 + 4
        for i in range(n):
            x = -span + 2 * span * (i + r.uniform(0.15, 0.85)) / n
            out.append((d + r.uniform(-1.0, 1.0), 'trunk', x, (rad * r.uniform(0.7, 1.3),), r.randrange(9999)))
    for d, n in ((18.0, 30), (11.0, 22), (8.0, 14)):                                         # canopy clumps
        span = d * 0.62 + 4
        for i in range(n):
            x = -span + 2 * span * (i + r.random()) / n
            out.append((d + r.uniform(-0.5, 0.5), 'clump', x, (r.uniform(3.6, 7.5), r.uniform(1.0, 1.8)),
                        r.randrange(9999)))
    for i in range(46):                                                                      # undergrowth behind
        d = r.uniform(6.2, 9.5)
        out.append((d, 'bush', r.uniform(-7, 9), (r.uniform(0.5, 1.2), r.uniform(0.6, 1.1)), r.randrange(9999)))
    for i in range(34):                                                                      # ferns behind the track
        d = r.uniform(5.9, 7.5)
        out.append((d, 'fern', r.uniform(-6, 8), (r.uniform(0.5, 0.9),), r.randrange(9999)))
    for i in range(30):                                                                      # nearer undergrowth
        d = r.uniform(2.0, 3.1)
        out.append((d, 'fern', r.uniform(-3, 5), (r.uniform(0.35, 0.6),), r.randrange(9999)))
    for i in range(170):                                                                     # leaf litter, roots
        d = r.uniform(3.3, 6.0)
        out.append((d, 'mark', r.uniform(-4, 7), (r.choice(('leaf', 'leaf', 'twig', 'stone')),), r.randrange(9999)))
    # the greenery ahead (screen right where the camera rests): thick bushes the attackers hide in
    for x, d, h, wd in ((1.6, 5.9, 1.5, 1.1), (2.3, 6.8, 1.9, 1.3), (1.3, 7.6, 1.7, 1.2), (2.4, 5.0, 1.2, 0.9),
                        (1.75, 4.3, 1.5, 0.8)):
        out.append((d, 'bush', END_X + x, (wd, h), r.randrange(9999)))
    return sorted(out, key=lambda q: -q[0])


AHEAD_GUNS = [(1.95, 6.1, 1.55), (2.45, 6.9, 1.85), (2.1, 7.7, 1.15), (2.6, 6.6, 0.95)]   # muzzles in the leaves
NOZZLE = (1.45, 4.35, 1.5)          # the flamethrower's nozzle pokes out of the nearest bush ahead
STAR_PIVOTS = [(0.15, 4.4, 4.6, T_STARS, 1), (-1.1, 4.9, 4.7, T_STARS + 0.3, -1)]   # (x, d, z, drop time, from)


# ------------------------------------------------------------------------------------------------ shapes
def _poly(d, pts, fill, line=2.4):
    MS._poly(d, [(x / SS, y / SS) for x, y in pts], fill, line)


def _blob(cx, cy, rx, ry, seed, n=14, rough=0.18):
    rr = random.Random(seed)
    rad = [1 - rough + rough * 2 * rr.random() for _ in range(n)]
    pts = []
    for i in range(n * 3):
        f = i / 3
        a, b = rad[int(f) % n], rad[(int(f) + 1) % n]
        w = f - int(f)
        k = a + (b - a) * w + 0.08 * math.sin(math.pi * w)
        q = 2 * math.pi * f / n
        pts.append((cx + rx * k * math.cos(q), cy + ry * k * math.sin(q)))
    return pts


def trunk(d, x, rad, seed, dep, cx):
    X0, Yg = _P(x - rad, dep, 0.0, cx)
    X1, _ = _P(x + rad, dep, 0.0, cx)
    if X1 < -200 or X0 > W * SS + 200:
        return
    col = fog(BARK, dep)
    top = -20
    flare = (X1 - X0) * 0.45
    pts = [(X0 + (X1 - X0) * 0.06, top), (X1 - (X1 - X0) * 0.06, top), (X1, Yg - flare * 1.4),
           (X1 + flare, Yg + 4), (X0 - flare, Yg + 4), (X0, Yg - flare * 1.4)]
    _poly(d, pts, col, 2.4 if dep < 15 else 1.6)
    rr = random.Random(seed)
    dark = fog(BARK_D, dep)
    for i in range(int(4 + 60 / dep)):                     # bark lines
        u = rr.uniform(0.2, 0.8)
        y0 = rr.uniform(0, Yg)
        ln = rr.uniform(40, 160) * SS * 8 / dep
        X = X0 + (X1 - X0) * u
        d.line([(X, y0), (X + rr.uniform(-4, 4), y0 + ln)], fill=dark, width=max(2, int(3 * SS * 6 / dep)))
    if rr.random() < 0.5 and dep < 20:                       # a branch going up into the canopy
        Xb, Yb = (X0 + X1) / 2, Yg * rr.uniform(0.25, 0.45)
        s = rr.choice((-1, 1))
        L = (X1 - X0) * 3.2
        _poly(d, [(Xb, Yb), (Xb + s * L, Yb - L * 0.9), (Xb + s * L * 1.05, Yb - L * 0.86), (Xb, Yb + (X1 - X0) * 0.3)],
              col, 1.8)


def clump(d, x, z, rad, seed, dep, cx):
    X, Y = _P(x, dep, z, cx)
    k = CAM.ppm(dep) * SS
    rr = random.Random(seed)
    col = fog(MS.mix(CANOPY, LEAF[0], rr.random() * 0.6), dep)
    pts = _blob(X, Y, rad * k * 1.3, rad * k * 0.75, seed, n=16, rough=0.22)
    _poly(d, pts, col, 2.0)
    for i in range(3):
        a = _blob(X + rr.uniform(-0.6, 0.6) * rad * k, Y + rr.uniform(-0.4, 0.1) * rad * k, rad * k * 0.45,
                  rad * k * 0.3, seed + i + 1, n=10)
        _poly(d, a, fog(MS.mix(col, LEAF[2], 0.35), dep), 0)


def bush(d, x, wd, h, seed, dep, cx):
    X, Yg = _P(x, dep, 0.0, cx)
    k = CAM.ppm(dep) * SS
    if X + wd * k < -100 or X - wd * k > W * SS + 100:
        return
    rr = random.Random(seed)
    base = fog(LEAF[rr.randrange(2)], dep)
    lumps = [(rr.uniform(-0.6, 0.6) * wd, rr.uniform(0.35, 0.8) * h, rr.uniform(0.35, 0.55) * wd) for _ in range(5)]
    lumps.sort(key=lambda q: q[1])
    for i, (ox, oz, r) in enumerate(lumps):
        _poly(d, _blob(X + ox * k, Yg - oz * k, r * k, r * k * 0.8, seed + i, n=12, rough=0.2),
              MS.mix(base, fog(LEAF[2], dep), 0.15 * i), 2.0)


def fern(d, x, h, seed, dep, cx, sway=0.0):
    X, Yg = _P(x, dep, 0.0, cx)
    k = CAM.ppm(dep) * SS
    if X + h * k < -100 or X - h * k > W * SS + 100:
        return
    rr = random.Random(seed)
    col = fog(LEAF[rr.randrange(3)], dep)
    n = rr.randint(5, 8)
    for i in range(n):
        a = math.radians(-90 + (i - (n - 1) / 2) * 24 + rr.uniform(-8, 8)) + sway
        L = h * k * rr.uniform(0.8, 1.15)
        bend = 0.9 * (a + math.pi / 2)                        # fronds arch over away from the middle
        sp = []
        for s in np.linspace(0, 1, 12):
            q = a + bend * s * s
            sp.append((X + math.cos(q) * L * s, Yg + math.sin(q) * L * s * 0.95))
        left, right = [], []
        for j, (px, py) in enumerate(sp):
            s = j / 11
            w = L * 0.12 * math.sin(math.pi * min(1.0, s * 1.1)) * (1.25 if j % 2 else 0.8)   # serrated
            if j + 1 < len(sp):
                dx, dy = sp[j + 1][0] - px, sp[j + 1][1] - py
            m = math.hypot(dx, dy) or 1
            left.append((px - dy / m * w, py + dx / m * w))
            right.append((px + dy / m * w, py - dx / m * w))
        _poly(d, left + right[::-1], col, 1.8)
        d.line(sp, fill=MS.mix(col, (20, 50, 30), 0.4), width=max(2, int(k * 0.012)))


def mark(d, x, kind, seed, dep, cx):
    X, Y = _P(x, dep, 0.0, cx)
    if X < -40 or X > W * SS + 40:
        return
    k = CAM.ppm(dep) * SS
    rr = random.Random(seed)
    if kind == 'leaf':
        col = rr.choice(((150, 110, 56), (166, 132, 64), (104, 84, 50), (128, 120, 60)))
        r = rr.uniform(0.05, 0.09) * k
        a = rr.uniform(0, math.pi)
        pts = [(X + r * math.cos(a) * math.cos(q) - r * 0.4 * math.sin(a) * math.sin(q) * 0.3,
                Y + 0.32 * (r * math.sin(a) * math.cos(q) + r * 0.4 * math.cos(a) * math.sin(q)))
               for q in np.linspace(0, 2 * math.pi, 10)]
        d.polygon(pts, fill=col)
    elif kind == 'twig':
        L = rr.uniform(0.15, 0.35) * k
        a = rr.uniform(-0.3, 0.3)
        d.line([(X - L * math.cos(a), Y - L * 0.2 * math.sin(a)), (X + L * math.cos(a), Y + L * 0.2 * math.sin(a))],
               fill=BARK_D, width=max(2, int(k * 0.02)))
    else:
        r = rr.uniform(0.04, 0.07) * k
        d.ellipse([X - r, Y - r * 0.45, X + r, Y + r * 0.35], fill=(132, 128, 118), outline=INK, width=2)


# ------------------------------------------------------------------------------------------------ layers
@lru_cache(None)
def _backdrop():
    """The deep, hazy green behind every trunk: darker up in the canopy (flat bands)."""
    img = Image.new('RGB', (W * SS, H * SS), HAZE)
    d = ImageDraw.Draw(img)
    hz = CAM.hz * SS
    for i, c in enumerate((CANOPY, MS.mix(CANOPY, HAZE, 0.25), MS.mix(CANOPY, HAZE, 0.5), MS.mix(CANOPY, HAZE, 0.75))):
        d.rectangle([0, i * hz / 5, W * SS, (i + 1) * hz / 5 + 2], fill=c)
    return img


def _shafts(img):
    """Shafts of light slanting down through the canopy (flat, pale, see-through)."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for x0, w in ((150, 60), (420, 110), (760, 70), (980, 90)):
        x0, w = x0 * SS, w * SS
        d.polygon([(x0, 0), (x0 + w, 0), (x0 + w + 520 * SS, CAM.hz * SS + 300 * SS),
                   (x0 + 520 * SS + w * 2.2, CAM.hz * SS + 300 * SS)], fill=(255, 248, 196, 34))
    img.alpha_composite(lay)


def behind(t):
    """Everything behind the four (RGBA, full size)."""
    cx = cam_x(t)
    img = _backdrop().convert('RGBA')
    d = ImageDraw.Draw(img)
    floor_y = CAM.p(0, 40.0, 0)[1] * SS
    d.rectangle([0, floor_y, W * SS, H * SS], fill=fog(FLOOR, 30))
    for dd, c in ((14.0, fog(FLOOR, 14)), (7.5, MS.mix(FLOOR, EARTH_D, 0.2))):
        d.rectangle([0, CAM.p(0, dd, 0)[1] * SS, W * SS, H * SS], fill=c)
    track = [CAM.p(0, 6.0, 0)[1] * SS, CAM.p(0, 3.2, 0)[1] * SS]
    d.rectangle([0, track[0], W * SS, track[1]], fill=EARTH)
    d.rectangle([0, track[1], W * SS, H * SS], fill=MS.mix(FLOOR, EARTH_D, 0.35))
    for edge in track:                                      # the track's ragged edges
        rr = random.Random(int(edge))
        pts = [(x * SS, edge + rr.uniform(-5, 5) * SS) for x in range(-20, W + 40, 30)]
        d.line(pts, fill=EARTH_D, width=3 * SS)
    shafts_done = False
    for dep, kind, x, a, seed in items():
        if dep < 3.2:
            continue
        if not shafts_done and dep < 10:
            _shafts(img)
            d = ImageDraw.Draw(img)
            shafts_done = True
        if kind == 'trunk':
            trunk(d, x, a[0], seed, dep, cx)
        elif kind == 'clump':
            clump(d, x, a[0], a[1], seed, dep, cx)
        elif kind == 'bush':
            bush(d, x, a[0], a[1], seed, dep, cx)
        elif kind == 'fern':
            fern(d, x, a[0], seed, dep, cx, 0.03 * math.sin(t * 1.7 + seed))
        else:
            mark(d, x, a[0], seed, dep, cx)
    return img.resize((W, H), Image.LANCZOS)


NEAR = [(-0.45, 1.5, 'trunk', 0.2), (0.4, 1.6, 'fern', 0.95), (1.5, 1.45, 'fern', 0.7), (-0.6, 1.4, 'fern', 0.8),
        (2.4, 1.55, 'fern', 1.0), (3.2, 1.5, 'fern', 0.75), (-2.0, 1.6, 'fern', 0.9)]


def in_front(t):
    """The nearest layer at about 1.5 m (RGBA): the undergrowth just in front of the track, ferns and a trunk that
    race past while the camera travels and wipe across the frame's foot."""
    cx = cam_x(t)
    img = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for dep, kind, x, a, seed in items():
        if dep < 3.2 and kind == 'fern':
            fern(d, x, a[0], seed, dep, cx, 0.04 * math.sin(t * 1.5 + seed))
    for i, (x, dep, kind, h) in enumerate(NEAR):
        if kind == 'trunk':
            trunk(d, x, h, 77, dep, cx)
        else:
            fern(d, x, h, 900 + i, dep, cx, 0.05 * math.sin(t * 1.3 + i))
    return img.resize((W, H), Image.LANCZOS)


# ------------------------------------------------------------------------------------------------ effects
class _FxCam:
    """The level camera in prepper_fx's terms: points are (x, up, depth) in metres; px per metre as k."""
    def __init__(self, t):
        self.cx = cam_x(t)

    def depth(self, p):
        return p[2]

    def project(self, p):
        return CAM.p(p[0] - self.cx, p[2], p[1]), CAM.ppm(p[2])

    def line(self, pen, pts, col, w):
        pen.line([self.project(q)[0] for q in pts], col, w)


def _fx():
    import prepper_fx as PF
    return PF


def gunfire(img, t):
    """Flashes in the leaves ahead (screen right) from the gunfire on, one frame each, never all at once; tracers
    whip over the four's heads to the left."""
    if t < T_GUN:
        return
    PF = _fx()
    cam = _FxCam(t)
    f = int(round(t * 12))
    for i, (x, d, z) in enumerate(AHEAD_GUNS):
        if (f + i * 2) % 3 == 0 and (t < 36.9 or (f + i) % 5 == 0):
            PF.flash(img, cam, (END_X + x, z, d), 0.42 if t < T_GUN + 0.25 else 0.32, seed=f * 7 + i)
    for i in range(10):                                      # tracers: start in the leaves, fly left over them
        t0 = T_GUN + 0.05 + i * 0.27
        u = (t - t0) / 0.32
        if 0 <= u <= 1:
            x, d, z = AHEAD_GUNS[i % len(AHEAD_GUNS)]
            a = (END_X + x, z, d)
            b = (END_X - 4.5, 1.9 + 0.35 * ((i * 7) % 3), 4.2 + 0.3 * (i % 3))
            PF.tracer(img, cam, a, b, u, length=0.9)


def muzzle(img, X, Y, k, seed, size=0.2):
    """A muzzle flash at a gun's mouth (screen X, Y; k px per metre there): the house's lumpy flash."""
    PF = _fx()

    class _S:
        def depth(self, p):
            return 1.0

        def project(self, p):
            return (X, Y), k
    PF.flash(img, _S(), (0, 0, 0), size, seed=seed)


def flame(img, t):
    """The flamethrower's blast (37.5): a jet whips out of the nearest bush ahead, left across the track at their
    chests, flickering and lashing up and down, then dies back into the bush (flat orange, yellow, pale core)."""
    u = t - T_FLAME
    if u < -0.4 or u > 1.6:
        return
    cx = cam_x(t)
    nx, nd, nz = NOZZLE
    nx += END_X
    lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    X0, Y0 = _P(nx, nd, nz, cx)
    k = CAM.ppm(nd) * SS
    a0 = math.radians(199)                                   # aimed left, a little up: over their ducked heads
    _poly(d, [(X0 + 0.12 * k, Y0 - 0.025 * k), (X0 - 0.06 * k, Y0 - 0.02 * k), (X0 - 0.06 * k, Y0 + 0.02 * k),
              (X0 + 0.12 * k, Y0 + 0.025 * k)], (60, 62, 68), 1.8)   # the nozzle poking out of the leaves
    if u > 0:
        reach = 1.6 * min(1.0, u / 0.16) * (1.0 if u < 1.0 else max(0.0, 1 - (u - 1.0) / 0.45))
        f = int(t * 24)
        whip = 0.16 * math.sin(u * 9.0) + 0.05 * math.sin(u * 23.0)
        if reach > 0.02:
            n = 16
            rr = random.Random(f)
            outer, inner, core = [], [], []
            for i in range(n + 1):
                s = i / n
                q = a0 + whip * s * s * 2.2
                L = reach * s
                px = X0 + math.cos(q) * L * k - 0.06 * k
                py = Y0 + math.sin(q) * L * k + 0.25 * k * s * s * math.sin(u * 6.0)
                w = (0.04 + 0.30 * s ** 0.8) * k * (0.85 + 0.3 * rr.random())
                outer.append((px, py, w))
            for col, sc, line in (((236, 104, 30), 1.0, 3.0), ((255, 196, 64), 0.62, 0), ((255, 246, 200), 0.3, 0)):
                for i, (px, py, w) in enumerate(outer):
                    if sc < 1 and i > n * (0.75 if sc > 0.5 else 0.55):
                        continue
                    r = w * sc
                    pts = _blob(px, py, r, r * 0.8, f * 31 + i, n=9, rough=0.25)
                    if line:
                        d.polygon(pts, fill=col, outline=INK, width=int(line))
                    else:
                        d.polygon(pts, fill=col)
                if line:                                        # re-fill the outline overlaps so it reads as one jet
                    for i, (px, py, w) in enumerate(outer):
                        d.polygon(_blob(px, py, w * 0.86, w * 0.68, f * 31 + i, n=9, rough=0.25), fill=col)
    img.alpha_composite(lay.resize(img.size, Image.LANCZOS))


def star_at(t, i):
    """(pivot X, Y, ball X, Y, radius px, k px/m) for morning star i at film time t, or None before it drops."""
    x, dd, z, t0, side = STAR_PIVOTS[i]
    if t < t0:
        return None
    cx = cam_x(t)
    L = 2.9
    u = t - t0
    if u < 0.25:                                             # drops down out of the canopy, already swinging
        a = side * math.radians(48)
        drop = L * (1 - (1 - u / 0.25) ** 2)
    else:
        a = side * math.radians(48) * math.cos((u - 0.25) * 2 * math.pi / 1.6) * math.exp(-0.18 * (u - 0.25))
        drop = L
    px, py = CAM.p(END_X + x - cx, dd, z)
    k = CAM.ppm(dd)
    bx, by = px + math.sin(a) * drop * k, py + math.cos(a) * drop * k
    return px, py, bx, by, 0.13 * k, k


def stars(img, t):
    """The two morning stars: spiked steel balls on chains swinging down out of the trees over their heads."""
    lay = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(len(STAR_PIVOTS)):
        s = star_at(t, i)
        if not s:
            continue
        px, py, bx, by, r, k = [v * SS for v in s[:5]] + [s[5] * SS]
        n = int(math.hypot(bx - px, by - py) / (0.07 * k)) + 1
        for j in range(n):                                   # the chain: links alternating face-on and edge-on
            u = (j + 0.5) / n
            cx, cy = px + (bx - px) * u, py + (by - py) * u
            ang = math.atan2(by - py, bx - px)
            lw, lh = (0.045 * k, 0.022 * k) if j % 2 else (0.045 * k, 0.008 * k)
            pts = [(cx + lw * math.cos(q) * math.cos(ang) - lh * math.sin(q) * math.sin(ang),
                    cy + lw * math.cos(q) * math.sin(ang) + lh * math.sin(q) * math.cos(ang))
                   for q in np.linspace(0, 2 * math.pi, 10)]
            d.polygon(pts, fill=(150, 154, 160), outline=INK, width=3)
        spin = t * 3.0 + i
        for m in range(12):                                  # the spikes
            q = spin + 2 * math.pi * m / 12
            b1, b2 = q - 0.2, q + 0.2
            d.polygon([(bx + r * 0.95 * math.cos(b1), by + r * 0.95 * math.sin(b1)),
                       (bx + r * 1.55 * math.cos(q), by + r * 1.55 * math.sin(q)),
                       (bx + r * 0.95 * math.cos(b2), by + r * 0.95 * math.sin(b2))],
                      fill=(196, 200, 206), outline=INK, width=3)
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=(84, 88, 96), outline=INK, width=4)
        d.ellipse([bx - r * 0.55, by - r * 0.6, bx - r * 0.1, by - r * 0.2], fill=(140, 146, 154))
    img.alpha_composite(lay.resize(img.size, Image.LANCZOS))


def sheet(out):
    tiles = []
    for t in (T0, T_GUN + 0.05, T_FLAME + 0.4, T_STARS + 0.5):
        img = behind(t)
        gunfire(img, t)
        flame(img, t)
        stars(img, t)
        img.alpha_composite(in_front(t))
        tiles.append(img.convert('RGB').resize((W // 2, H // 2)))
    s = Image.new('RGB', (W * 2, H // 2), 'white')
    for i, tl in enumerate(tiles):
        s.paste(tl, (i * W // 2, 0))
    s.save(out, quality=88)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
    else:
        print(__doc__)
