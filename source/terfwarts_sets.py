#!/usr/bin/env python3
"""Terfwarts: the places, each a flat painting per camera (film-quality rule 39), from Sam's references
(references/terfwarts/). MAP: View (one camera: where it stands, which way it looks, focal, horizon) and its
projection: top; hall() (shot 1: the Great Hall behind Harry's close-up); cloister() (the fan-vaulted corridor: both
directions, the shrunk door and GIRLS plaque at its north end); sheet() (every painting beside the refs).

Plan (terfwarts_plan.py): the corridor runs north-south, x 20..23.5, the door in its north end wall (z 26). Looking
south (the run, the boys) the tracery windows onto the garth are on the right (the west wall) and the stone bench on
the left; looking north (the door) they swap sides.

    python3 source/terfwarts_sets.py OUT.jpg
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
from ed import INK               # noqa: E402
from satire_style import rough   # noqa: E402

FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
STONE, STONE_LT, STONE_DK = (204, 178, 132), (226, 204, 160), (168, 142, 100)
FLAG, FLAG2 = (188, 170, 136), (172, 154, 122)
OAK, OAK_DK, OAK_LT = (104, 64, 34), (70, 42, 22), (132, 86, 48)
BRASS = (214, 176, 84)
GRASS, SKY = (112, 150, 78), (196, 214, 222)
W_HALF, SPRING, CROWN, BAY = 1.75, 2.9, 4.3, 2.6      # corridor half width, vault springing, crown, bay length (m)
DOOR_W, DOOR_SQ, DOOR_TOP = 1.1, 1.95, 2.55            # the shrunk door: width, square top, arch point (m)
PLAQUE = (2.18, 0.46, 0.15)                            # GIRLS plaque: centre height, width, height (m), on the door


class View:
    """One camera in the corridor: z (along the corridor), facing -1 south / +1 north, eye height h, focal f (px),
    horizon at screen y hy. A point (r, y, d): r metres to the right of the camera, y up, d ahead."""
    def __init__(self, z, facing, h, f, hy, x=21.75, cx=540.0):
        self.z, self.facing, self.h, self.f, self.hy, self.x, self.cx = z, facing, h, f, hy, x, cx

    def P(self, r, y, d):
        d = max(d, 0.05)
        return self.cx + r * self.f / d, self.hy + (self.h - y) * self.f / d

    def pxm(self, d):
        return self.f / d

    def floor_y(self, d, lift=0.0):
        return self.hy + (self.h - lift) * self.f / d

    def d_of(self, z):
        return (z - self.z) * self.facing

    def r_of(self, x):
        return (x - self.x) * self.facing        # facing north, east (x+) is to the right; facing south, west


# the cameras (plan CAMS keeps these numbers)
RUN = View(25.4, -1, 1.3, 1400, 820)
BOYS = View(25.6, -1, 1.45, 1300, 640)          # Myrtle's point of view, from just in front of the door
DOOR = View(22.0, +1, 1.25, 1600, 900)
_CACHE = {}


def _key(name, cam):
    return (name, round(cam.z, 4), round(cam.cx, 2), round(cam.cy, 2), B.SS)


def cached(name, cam, paint):
    k = _key(name, cam)
    if k not in _CACHE:
        img = B.canvas()
        paint(img, cam)
        _CACHE[k] = img
    return _CACHE[k].copy()


# ------------------------------------------------------------------------------------------------ the Great Hall
def hall(img, cam):
    """Shot 1, behind Harry's close-up (refs sorting-hat-scene-1/2, great-hall-*): the far end of the hall at night.
    Warm stone, two tall leaded windows (dark blue night), the staff table's cloth and candles below them, floating
    candles at many depths, a banner. Painted soft and dim so Harry and the Hat read first."""
    p = B.Pen(img, cam)
    box = lambda x0, y0, x1, y1, c, sd, lw=2.5: p.poly(rough([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 5, sd), c, INK, lw)
    box(-400, -400, 1480, 2400, (128, 92, 58), 1)                       # the far wall, warm stone in candlelight
    for i in range(14):                                                 # stone courses
        y = 120 + i * 78
        p.line([(-400, y), (1480, y + 6)], (112, 80, 50), 2)
    for wx in (40, 600):                                                # the tall leaded windows
        pts = [(wx, 1040), (wx, 260), (wx + 220, 40), (wx + 440, 260), (wx + 440, 1040)]
        p.poly(rough(pts, 4, wx), (44, 58, 92), INK, 3)
        for k in range(1, 4):                                            # mullions
            x = wx + k * 110
            p.line([(x, 1040), (x, 230 if k == 2 else 300)], (150, 120, 80), 7)
        for y in range(330, 1040, 120):                                 # transom
            p.line([(wx + 6, y), (wx + 434, y)], (150, 120, 80), 5)
        for y in range(300, 1040, 40):                                  # the lead diamonds, faint
            p.line([(wx + 8, y), (wx + 432, y + 30)], (62, 76, 108), 1.2)
            p.line([(wx + 8, y + 30), (wx + 432, y)], (62, 76, 108), 1.2)
    box(-400, 1040, 1480, 1110, (100, 70, 44), 3)                       # sill / panelling top rail
    box(-400, 1110, 1480, 2400, (84, 54, 34), 4)                        # oak panelling
    for x in range(-380, 1480, 150):
        p.poly(rough([(x, 1140), (x + 120, 1140), (x + 120, 1300), (x, 1300)], 3, x), (96, 62, 38), (60, 38, 22), 2)
    p.poly(rough([(460, 120), (620, 120), (620, 520), (540, 470), (460, 520)], 4, 9), (150, 34, 40), INK, 2.5)  # banner
    p.ell(540, 260, 44, 52, (206, 164, 62), INK, 2)
    box(-400, 1300, 1480, 1360, (240, 236, 222), 5)                     # the staff table's white cloth edge
    box(-400, 1360, 1480, 2400, (60, 40, 30), 6)
    for i, x in enumerate(range(-300, 1480, 210)):                      # candles and goblets on the staff table
        p.poly([(x - 7, 1300), (x - 7, 1210), (x + 7, 1210), (x + 7, 1300)], (244, 238, 220), INK, 1.6)
        p.ell(x, 1196, 6, 13, (255, 210, 110), None)
        g = x + 90
        p.poly([(g - 14, 1262), (g + 14, 1262), (g + 8, 1284), (g + 2, 1300), (g - 2, 1300), (g - 8, 1284)],
               (214, 176, 84), INK, 1.4)
    import random
    r = random.Random(7)
    for _ in range(46):                                                  # floating candles, many depths
        k = r.uniform(0.5, 1.2)
        x, y = r.uniform(-60, 1140), r.uniform(-120, 1000)
        h = 46 * k
        p.poly([(x - 6 * k, y), (x - 6 * k, y - h), (x + 6 * k, y - h), (x + 6 * k, y)], (240, 232, 210), INK, 1.2 * k)
        p.ell(x, y - h - 9 * k, 5 * k, 10 * k, (255, 214, 120), None)


# ------------------------------------------------------------------------------------------------ the cloister
def _quad(p, v, pts, fill, line=INK, lw=2.5):
    p.poly([v.P(*q) for q in pts], fill, line, lw)


def _pointed(cx, base, top, half, n=10):
    """A pointed (two-centred) arch from the left springing over the apex to the right one, as (x, height) pairs:
    each side an arc of a circle centred on the springing line (radius R so it meets the apex)."""
    h = top - base
    R = (half * half + h * h) / (2 * half)
    a1 = math.atan2(h, half - R)                       # the apex angle seen from the left arc's centre
    left = [(cx - half + R + R * math.cos(math.pi - (math.pi - a1) * i / n), base + R * math.sin(math.pi - (math.pi - a1) * i / n))
            for i in range(n + 1)]
    right = [(2 * cx - x, y) for x, y in reversed(left[:-1])]
    return left + right


def cloister(img, cam, v):
    """The fan-vaulted cloister (refs corridor, trio-hbo-cloister), honey stone, seen from View v. Looking south: the
    far arch at the end (z 0), tracery windows on the right onto the green garth, stone bench left. Looking north:
    the end wall with the shrunk carved door (refs door-1/2) and its GIRLS plaque."""
    p = B.Pen(img, cam)
    north = v.facing > 0
    d_end = v.d_of(26.0) if north else v.d_of(0.0)
    win = -1 if north else +1                       # which side (r sign) the windows are on
    dn = 0.35
    # the far end
    _quad(p, v, [(-W_HALF, 0, d_end), (W_HALF, 0, d_end), (W_HALF, SPRING + 0.4, d_end), (0, CROWN, d_end),
                 (-W_HALF, SPRING + 0.4, d_end)], STONE, INK, 2.5)
    if north:
        _end_wall(p, v, d_end)
    else:
        arch = [(x, y, d_end) for x, y in _pointed(0, 0.0, 3.6, 1.1)]
        p.poly([v.P(*q) for q in arch], (236, 222, 186), INK, 2)
        _quad(p, v, [(-1.1, 0, d_end), (1.1, 0, d_end), (1.1, 0.02, d_end - 3), (-1.1, 0.02, d_end - 3)], FLAG)
        for x in (-0.55, 0.0, 0.55):                                    # a tracery window beyond the arch
            p.line([v.P(x, 1.0, d_end + 2), v.P(x, 3.0, d_end + 2)], STONE_DK, 3)
    # the floor: flagstones
    _quad(p, v, [(-W_HALF, 0, dn), (W_HALF, 0, dn), (W_HALF, 0, d_end), (-W_HALF, 0, d_end)], FLAG)
    d = dn
    k = 0
    while d < d_end:
        d2 = min(d_end, d + 0.9)
        for i in range(5):
            r0 = -W_HALF + i * 0.7 + (0.35 if k % 2 else 0)
            r1 = min(W_HALF, r0 + 0.7)
            if r0 < W_HALF:
                _quad(p, v, [(r0, 0, d), (r1, 0, d), (r1, 0, d2), (r0, 0, d2)], FLAG if (i + k) % 3 else FLAG2,
                      (140, 124, 96), 1.2)
        d, k = d2, k + 1
    # the ceiling: two slopes, then a fan on every shaft
    for s in (-1, 1):
        _quad(p, v, [(s * W_HALF, SPRING, dn), (0, CROWN, dn), (0, CROWN, d_end), (s * W_HALF, SPRING, d_end)],
              STONE_LT, INK, 2)
    shafts = [z for z in [26.0 - i * BAY for i in range(12)] if dn < v.d_of(z) <= d_end + 0.01]
    for z in sorted(shafts, key=lambda zz: -v.d_of(zz)):
        ds = v.d_of(z)
        for s in (-1, 1):
            rim = []
            for i in range(13):
                a = math.pi * i / 12
                rim.append((s * (W_HALF - 0.95 * math.sin(a)), SPRING + 1.3 * math.sin(a), ds - 1.15 * math.cos(a)))
            rim = [q for q in rim if dn < q[2] <= d_end + 0.01]
            if len(rim) > 2:
                spr = (s * W_HALF, SPRING - 0.4, ds)
                p.poly([v.P(*spr)] + [v.P(*q) for q in rim], (236, 216, 176), INK, 1.8)
                for q in rim[1:-1:2]:
                    p.line([v.P(*spr), v.P(*q)], STONE_DK, 1.2)
    # the walls
    for s in (-1, 1):
        _quad(p, v, [(s * W_HALF, 0, dn), (s * W_HALF, SPRING, dn), (s * W_HALF, SPRING, d_end),
                     (s * W_HALF, 0, d_end)], STONE, INK, 2.5)
    bays = sorted([z for z in [26.0 - BAY / 2 - i * BAY for i in range(11)]], key=lambda zz: -v.d_of(zz))
    for z in bays:
        dc = v.d_of(z)
        a, b = dc - BAY / 2 + 0.25, dc + BAY / 2 - 0.25
        if b <= dn or a >= d_end:
            continue
        a, b = max(a, dn), min(b, d_end)
        # window side: a tall tracery window onto the garth
        r = win * W_HALF
        y0, y1, y2 = 0.85, 2.15, 2.75
        out = [(r, y0, a), (r, y1, a), (r, y2, (a + b) / 2), (r, y1, b), (r, y0, b)]
        _quad(p, v, out, SKY, INK, 2.2)
        _quad(p, v, [(r, y0, a), (r, 1.25, a), (r, 1.25, b), (r, y0, b)], GRASS, None)        # the garth's lawn
        _quad(p, v, [(r, 1.25, a), (r, 1.75, a), (r, 1.75, b), (r, 1.25, b)], (214, 190, 146), None)  # far range
        for k in range(1, 3):
            dk = a + (b - a) * k / 3
            p.line([v.P(r, y0, dk), v.P(r, y1 + 0.18, dk)], STONE_LT, max(2, 0.06 * v.f / dk))
        p.line([v.P(r, y1, a), v.P(r, y1, b)], STONE_LT, max(2, 0.05 * v.f / b))
        p.poly([v.P(*q) for q in out], None, INK, 2.2)
        _quad(p, v, [(r, 0.7, a), (r, y0, a), (r, y0, b), (r, 0.7, b)], STONE_LT, INK, 1.6)    # sill
        # bench side: blind tracery panels and the stone bench
        r = -win * W_HALF
        for k in range(3):
            pa, pb = a + (b - a) * k / 3 + 0.06, a + (b - a) * (k + 1) / 3 - 0.06
            p.poly([v.P(r, 0.75, pa), v.P(r, 2.2, pa), v.P(r, 2.55, (pa + pb) / 2), v.P(r, 2.2, pb),
                    v.P(r, 0.75, pb)], None, STONE_DK, 1.4)
    rb = -win * W_HALF
    rin = rb + win * 0.45
    _quad(p, v, [(rb, 0.45, dn), (rin, 0.45, dn), (rin, 0.45, d_end), (rb, 0.45, d_end)], STONE_LT)   # bench top
    _quad(p, v, [(rin, 0.0, dn), (rin, 0.45, dn), (rin, 0.45, d_end), (rin, 0.0, d_end)], STONE_DK)   # bench front
    for z in shafts:                                                    # the attached shafts at every bay
        ds = v.d_of(z)
        for s in (-1, 1):
            w = 0.09
            _quad(p, v, [(s * W_HALF, 0, ds - w), (s * W_HALF, SPRING, ds - w), (s * W_HALF, SPRING, ds + w),
                         (s * W_HALF, 0, ds + w)], STONE_LT, INK, 1.6)


def _end_wall(p, v, d):
    """The north end: the shrunk carved oak door (refs door-1/2) in a moulded pointed arch with clustered shafts,
    ring handles, the brass GIRLS plaque on its top panel."""
    for k, (half, top, c) in enumerate(((0.95, 3.25, STONE_DK), (0.85, 3.05, STONE_LT), (0.76, 2.88, STONE),
                                         (0.66, 2.72, STONE_LT))):
        pts = [(-half, 0)] + _pointed(0, 2.0, top, half) + [(half, 0)]
        p.poly([v.P(x, y, d) for x, y in pts], c, INK, 2)
    for s in (-1, 1):                                                   # clustered shafts either side
        for k, o in enumerate((0.62, 0.72, 0.82)):
            x = s * o
            p.poly([v.P(x - 0.03, 0, d), v.P(x - 0.03, 2.0, d), v.P(x + 0.03, 2.0, d), v.P(x + 0.03, 0, d)],
                   STONE_LT if k % 2 else STONE, INK, 1.4)
        p.poly([v.P(s * 0.6, 1.95, d), v.P(s * 0.85, 1.95, d), v.P(s * 0.85, 2.05, d), v.P(s * 0.6, 2.05, d)],
               STONE_DK, INK, 1.4)                                      # capitals
    hw = DOOR_W / 2
    door = [(-hw, 0)] + _pointed(0, DOOR_SQ, DOOR_TOP, hw) + [(hw, 0)]
    p.poly([v.P(x, y, d) for x, y in door], OAK, INK, 3)
    p.line([v.P(0, 0, d), v.P(0, DOOR_TOP, d)], OAK_DK, 3)              # the two leaves
    for leaf in (-1, 1):                                                # carved square panels, 2 x 4 a leaf
        for row in range(4):
            for col in range(2):
                x0 = leaf * (0.05 + col * 0.24) if leaf > 0 else -(0.05 + col * 0.24) - 0.2
                y0 = 0.12 + row * 0.42
                q = [(x0, y0), (x0 + 0.2, y0), (x0 + 0.2, y0 + 0.36), (x0, y0 + 0.36)]
                p.poly([v.P(x, y, d) for x, y in q], OAK_DK, INK, 1.4)
                p.poly([v.P(x0 + 0.04, y0 + 0.05, d), v.P(x0 + 0.16, y0 + 0.05, d), v.P(x0 + 0.16, y0 + 0.31, d),
                        v.P(x0 + 0.04, y0 + 0.31, d)], OAK_LT, None)
                cx, cy = v.P(x0 + 0.1, y0 + 0.18, d)
                p.ell(cx, cy, 0.035 * v.f / d, 0.05 * v.f / d, OAK, OAK_DK, 1.2)   # carved boss
    for s in (-1, 1):                                                   # ring handles
        cx, cy = v.P(s * 0.12, 1.0, d)
        rr = 0.06 * v.f / d
        p.ell(cx, cy, rr, rr, None, (60, 50, 30), 4)
        p.ell(cx, cy - rr, 0.022 * v.f / d, 0.022 * v.f / d, BRASS, INK, 1.4)
    pc, pw, ph = PLAQUE
    x0, y0 = v.P(-pw / 2, pc + ph / 2, d)
    x1, y1 = v.P(pw / 2, pc - ph / 2, d)
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], BRASS, INK, 2.4)


def plaque_box(v, cam=None):
    """The GIRLS plaque's box on screen (for KEEP_CLEAR and the text)."""
    pc, pw, ph = PLAQUE
    d = v.d_of(26.0)
    x0, y0 = v.P(-pw / 2, pc + ph / 2, d)
    x1, y1 = v.P(pw / 2, pc - ph / 2, d)
    if cam is not None:
        x0, y0 = (x0 - cam.cx) * cam.z + 540, (y0 - cam.cy) * cam.z + 960
        x1, y1 = (x1 - cam.cx) * cam.z + 540, (y1 - cam.cy) * cam.z + 960
    return x0, y0, x1, y1


def plaque_text(img, v, cam):
    """GIRLS on the plaque, in black serif-ish capitals, drawn after the painting so it stays crisp."""
    x0, y0, x1, y1 = plaque_box(v, cam)
    S = B.SS
    f = ImageFont.truetype(FONT, max(8, int((y1 - y0) * 0.72 * S)))
    ImageDraw.Draw(img).text(((x0 + x1) / 2 * S, (y0 + y1) / 2 * S), 'GIRLS', font=f, fill=(30, 22, 12), anchor='mm')


# ------------------------------------------------------------------------------------------------ the sheet
def sheet(out):
    B.SS = 1
    cam = B.Cam(1.0, 540, 960)
    tiles = [('Great Hall (shot 1)', cached('hall', cam, hall)),
             ('Cloister: the run (from the door)', cached('run', cam, lambda i, c: cloister(i, c, RUN))),
             ('Cloister: the boys (Myrtle sees)', cached('boys', cam, lambda i, c: cloister(i, c, BOYS))),
             ('The door (over the boys)', cached('door', cam, lambda i, c: cloister(i, c, DOOR)))]
    plaque_text(tiles[3][1], DOOR, cam)
    W = 1080
    img = Image.new('RGB', (W, 1060), (232, 228, 222))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 15)
    for i, (lab, t) in enumerate(tiles):
        th = t.convert('RGB').resize((260, 462))
        img.paste(th, (8 + i * 268, 40))
        d.text((8 + i * 268, 8), lab, font=f, fill=(30, 30, 30))
    for i, n in enumerate(('sorting-hat-scene-2', 'corridor', 'trio-hbo-cloister', 'door-1')):
        r = Image.open(os.path.join(HERE, '..', 'references', 'terfwarts', n + '.jpg')).convert('RGB')
        r.thumbnail((260, 480))
        img.paste(r, (8 + i * 268, 540))
        d.text((8 + i * 268, 1030), 'ref: ' + n, font=f, fill=(30, 30, 30))
    img.save(out, quality=88)


if __name__ == '__main__':
    sheet(sys.argv[1])
