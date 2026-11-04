#!/usr/bin/env python3
"""MAP  MidTerminal (Sam, 4 Nov): the Oval Office, built once in 3D (metres) and seen through any camera. Sam's pick:
the gold-curtain, blue-carpet look (refs oval-1 and oval-3's lower half), flat cartoon style. References:
references/midterminal/oval-1..5.

What makes the place (the BENCHMARK list):
  - an OVAL room (real size about 10.9 x 8.8 m, ceiling 5.6 m): pale beige walls above a white panelled dado, a white
    cornice with dentils, a cream ceiling with a plaster ring
  - the desk end: three tall many-paned windows onto the garden, gold drapes between and beside them under one gold
    swag valance; the Resolute desk (dark carved wood, a panelled kneehole) with phones on it, a tall brown tufted
    leather chair; a low table under the middle window with family photos; the US flag and the President's navy flag
    either side
  - two wooden chairs with gold seats facing the desk
  - a deep blue oval carpet with a cream border of flowers edged in red and gold; the seal at its centre
  - the far end: a white fireplace with a portrait above it, two arched alcoves with shelves either side, two cream
    sofas facing each other, a low table with flowers, two yellow armchairs at the fire, a grandfather clock
  - four white panelled doors with pediments in the curved wall; portraits in gold frames over side tables with busts
No real person's portrait is drawn (the portraits are generic 18th-century gentlemen). The seal is a simplified
eagle-in-a-ring, no lettering.

Plan (x east, z north, y up): the room's centre at (0, 0); the desk end north (+z). Wall points by angle `a`
(degrees, 0 = north/the middle window, 90 = east). Desk centre (0, 3.0), its chair (0, 3.75) facing south (180).

    python3 source/midterminal_set.py test OUT.jpg     the room from four cameras, the cast placed
    python3 source/midterminal_set.py refs OUT.jpg     Sam's photos beside ours

Map: colours 45 | plan 85 | helpers 110 | walls 150 | windows 215 | fireplace, alcoves, doors, portraits 300 |
floor and carpet 420 | furniture 500 | render, people 690 | sheets 740
"""
import functools
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import sets as S                 # noqa: E402
from sets import Face, obox, cylinder, draw_parts, dk, lt, jit   # noqa: E402
from ed import INK               # noqa: E402

FLAT = S.FLAT
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
REFS = os.path.join(HERE, '..', 'references', 'midterminal')

# ---------------------------------------------------------------------------------------------- colours
WALL = (218, 208, 190)
WALL_MARK = (204, 192, 172)
DADO = (238, 234, 222)
CORNICE = (244, 240, 230)
CEIL = (240, 234, 216)
GOLD = (212, 166, 62)
GOLD_D = (168, 122, 40)
GOLD_L = (234, 196, 104)
WOOD = (112, 66, 36)
WOOD_D = (80, 46, 26)
WOOD_L = (146, 92, 52)
FLOOR = (156, 104, 60)
FLOOR_L = (140, 92, 52)
NAVY = (30, 46, 110)
NAVY_D = (22, 34, 84)
BORDER = (236, 226, 196)
RED = (176, 36, 40)
WHITE = (246, 244, 238)
LEATHER = (92, 54, 36)
SEAT = (214, 150, 70)
SOFA = (232, 220, 192)
YELLOW = (232, 190, 74)
SKY = (196, 216, 232)
TREE = (86, 128, 78)
TREE_D = (64, 100, 60)
LAWN = (116, 162, 90)
BRONZE = (70, 56, 46)

# ---------------------------------------------------------------------------------------------- the plan
A, BZ, CEIL_H = 4.42, 5.45, 5.6          # the oval's half-widths (x, z) and the ceiling
DADO_H, CORN_H = 0.95, 5.15
WINDOWS = (-34.0, 0.0, 34.0)             # window centres (angles); each about 1.25 m wide, 0.75 .. 4.0 m up
WIN_HALF = 10.0
DOORS = (-112.0, -70.0, 70.0, 112.0)
PORTRAITS = (-91.0, 91.0)
ALCOVES = (-148.0, 148.0)
FIRE = 180.0
DESK = (0.0, 3.0)
DESK_CHAIR = (0.0, 3.75)
VISITOR_CHAIRS = ((-0.85, 1.95), (0.85, 1.95))
SOFAS = ((-1.6, -2.7), (1.6, -2.7))
ARMCHAIRS = ((-0.8, -4.25), (0.8, -4.25))
FLAGS = ((-1.65, 4.55, 'us'), (1.65, 4.55, 'pres'))
PROP_SIZES = {'Resolute desk': (1.83, 0.76, 0.91), 'door': (1.1, 2.45), 'window': (1.25, 3.25)}
ROOMS = {'oval office': (-A, -BZ, A, BZ)}

CAMS = {
    'wide': dict(pos=(0.0, 1.7, -1.3), look=(0.0, 0.95, 4.0), focal=560),
    'desk': dict(pos=(0.0, 1.45, 0.4), look=(0.0, 1.2, 3.5), focal=880),
    'reverse': dict(pos=(0.4, 1.7, 4.4), look=(0.0, 0.7, -3.0), focal=560),
    'high': dict(pos=(-1.5, 4.9, -2.6), look=(0.3, 0.2, 1.4), focal=520),
}


def cam(name):
    c = CAMS[name]
    return S.Cam(c['pos'], c['look'], focal=c['focal'])


# ---------------------------------------------------------------------------------------------- helpers
def _pen(img):
    return B.Pen(img, FLAT)


def poly(img, cm, pts, fill, line=INK, lw=2.0):
    cm.poly(_pen(img), pts, fill, line, lw)


def lines(img, cm, pts, col=INK, lw=2.0):
    cm.line(_pen(img), [jit(q) for q in pts], col, lw)


def wp(a, y, inset=0.0):
    """The wall at angle a (degrees), height y; `inset` metres in towards the middle (or out, negative)."""
    x, z = A * math.sin(math.radians(a)), BZ * math.cos(math.radians(a))
    r = math.hypot(x, z)
    k = 1.0 - inset / r
    return (x * k, y, z * k)


def band(a0, a1, y0, y1, inset=0.0, step=3.0):
    """A piece of wall from angle a0 to a1, heights y0..y1, following the curve."""
    n = max(2, int(abs(a1 - a0) / step) + 1)
    aa = np.linspace(a0, a1, n)
    return [wp(a, y0, inset) for a in aa] + [wp(a, y1, inset) for a in aa[::-1]]


def floor_pt(a, r=1.0, y=0.0):
    return (A * r * math.sin(math.radians(a)), y, BZ * r * math.cos(math.radians(a)))


def wall_yaw(a):
    """The plan facing (degrees) of something standing against the wall at angle a, facing into the room."""
    x, _, z = wp(a, 0)
    return math.degrees(math.atan2(-x / A ** 2, -z / BZ ** 2))


def _persp(src, dst):
    M, bv = [], []
    for (x, y), (u, v) in zip(dst, src):
        M.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); bv.append(u)
        M.append([0, 0, 0, x, y, 1, -v * x, -v * y]); bv.append(v)
    return np.linalg.solve(np.array(M, float), np.array(bv, float)).tolist()


def paste_on(img, cm, quad, art):
    """A flat picture laid on a 3D rectangle (corners: top-left, top-right, bottom-right, bottom-left)."""
    if any(cm.depth(q) < cm.NEAR + 0.05 for q in quad):
        return
    ss = img.width / 1080.0
    dst = [(x * ss, y * ss) for x, y in (cm.project(q)[0] for q in quad)]
    x0, y0 = max(0, int(min(q[0] for q in dst)) - 1), max(0, int(min(q[1] for q in dst)) - 1)
    x1, y1 = min(img.width, int(max(q[0] for q in dst)) + 2), min(img.height, int(max(q[1] for q in dst)) + 2)
    if x1 <= x0 or y1 <= y0:
        return
    w, h = art.size
    co = _persp([(0, 0), (w, 0), (w, h), (0, h)], [(x - x0, y - y0) for x, y in dst])
    img.alpha_composite(art.transform((x1 - x0, y1 - y0), Image.PERSPECTIVE, co, Image.BILINEAR), (x0, y0))


def paste_tiled(img, cm, x0, x1, z0, z1, y, art, n=(8, 10)):
    """A big flat picture on the floor (x0..x1, z0..z1 seen from above, north up), in tiles, so the parts in front of
    the camera still draw when the camera stands over it."""
    w, h = art.size
    for i in range(n[0]):
        for k in range(n[1]):
            u0, u1 = i / n[0], (i + 1) / n[0]
            v0, v1 = k / n[1], (k + 1) / n[1]
            tile = art.crop((int(u0 * w), int(v0 * h), int(u1 * w), int(v1 * h)))
            if tile.getbbox() is None:
                continue
            xa, xb = x0 + (x1 - x0) * u0, x0 + (x1 - x0) * u1
            za, zb = z1 - (z1 - z0) * v0, z1 - (z1 - z0) * v1
            paste_on(img, cm, [(xa, y, za), (xb, y, za), (xb, y, zb), (xa, y, zb)], tile)


# ---------------------------------------------------------------------------------------------- walls, ceiling
def _skip(a):
    """Wall angles taken by windows (no dado or wallpaper drawn there; the window draws its own)."""
    return any(abs(a - c) < WIN_HALF for c in WINDOWS)


def walls(img, cm):
    poly(img, cm, [floor_pt(a, 1.0, CEIL_H) for a in range(0, 360, 4)], CEIL, INK, 2.0)
    poly(img, cm, [floor_pt(a, 0.42, CEIL_H - 0.01) for a in range(0, 360, 6)], lt(CEIL, 1.03), INK, 1.6)
    poly(img, cm, [floor_pt(a, 0.30, CEIL_H - 0.01) for a in range(0, 360, 6)], CEIL, dk(CEIL, 0.85), 1.4)
    for a0 in range(-180, 180, 4):
        a1 = a0 + 4
        poly(img, cm, band(a0, a1, DADO_H, CORN_H), WALL, None)
        poly(img, cm, band(a0, a1, 0.0, DADO_H), DADO, None)
        poly(img, cm, band(a0, a1, CORN_H, CEIL_H), CORNICE, None)
    rng = np.random.default_rng(3)
    for a in np.arange(-180, 180, 4.5):               # the wallpaper's small damask marks, in a lattice
        for k, y in enumerate(np.arange(1.3, CORN_H - 0.2, 0.45)):
            aa = a + (2.25 if k % 2 else 0.0)
            if _skip(aa):
                continue
            c = wp(aa, y, 0.005)
            d = 0.05
            q = [wp(aa, y + d, 0.005), wp(aa + 0.35, y, 0.005), wp(aa, y - d, 0.005), wp(aa - 0.35, y, 0.005)]
            poly(img, cm, q, WALL_MARK, None)
    del rng
    for y, col, lw in ((DADO_H, INK, 2.2), (DADO_H - 0.06, dk(DADO, 0.8), 1.4), (CORN_H, INK, 2.2),
                       (CORN_H + 0.12, dk(CORNICE, 0.8), 1.4), (CEIL_H - 0.01, INK, 2.2), (0.14, dk(DADO, 0.75), 1.6)):
        lines(img, cm, [wp(a, y, 0.006) for a in np.arange(-180, 181, 3)], col, lw)
    for a in np.arange(-180, 180, 1.2):                # the dentils under the cornice
        lines(img, cm, [wp(a, CORN_H + 0.02, 0.008), wp(a, CORN_H + 0.1, 0.008)], dk(CORNICE, 0.78), 1.2)
    for a in np.arange(-180, 180, 9.0):                # the dado's panels
        if _skip(a) or _skip(a + 9):
            continue
        q = band(a + 1.2, a + 7.8, 0.25, DADO_H - 0.16, 0.006)
        poly(img, cm, q, None, dk(DADO, 0.8), 1.4)


# ---------------------------------------------------------------------------------------------- windows and drapes
@functools.lru_cache(maxsize=1)
def garden_art():
    """The garden through the windows: sky, trees in clumps, the lawn (flat, painted once)."""
    w, h = 300, 780
    im = Image.new('RGBA', (w, h), SKY + (255,))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(11)
    for k in range(14):                                # tree clumps along the middle
        x, y, r = rng.uniform(-40, w + 40), rng.uniform(240, 470), rng.uniform(60, 110)
        d.ellipse([x - r, y - r, x + r, y + r], fill=TREE_D if k % 3 == 0 else TREE)
    d.rectangle([0, 520, w, h], fill=LAWN)
    d.rectangle([0, 600, w, h], fill=dk(LAWN, 0.92))
    return im


def window(img, cm, c):
    a0, a1 = c - WIN_HALF + 1.5, c + WIN_HALF - 1.5
    y0, y1 = 0.75, 4.0
    tl, tr, br, bl = wp(a0, y1, 0.01), wp(a1, y1, 0.01), wp(a1, y0, 0.01), wp(a0, y0, 0.01)
    poly(img, cm, band(c - WIN_HALF, c + WIN_HALF, 0.0, CORN_H), WALL, None)
    poly(img, cm, band(c - WIN_HALF, c + WIN_HALF, 0.0, y0 - 0.05), DADO, INK, 1.8)        # the panel under it
    poly(img, cm, band(c - WIN_HALF + 1.2, c + WIN_HALF - 1.2, 0.12, y0 - 0.2, 0.008), None, dk(DADO, 0.8), 1.4)
    paste_on(img, cm, [tl, tr, br, bl], garden_art())
    poly(img, cm, [tl, tr, br, bl], None, INK, 2.4)
    for k in range(1, 3):                              # muntins: 3 across, 8 down (white glazing bars)
        a = a0 + (a1 - a0) * k / 3
        poly(img, cm, band(a - 0.25, a + 0.25, y0, y1, 0.012), WHITE, None)
    for k in range(1, 8):
        y = y0 + (y1 - y0) * k / 8
        poly(img, cm, band(a0, a1, y - 0.025, y + 0.025, 0.012), WHITE, None)
    poly(img, cm, band(a0 - 0.6, a1 + 0.6, y0 - 0.08, y0, 0.03), WHITE, INK, 1.8)            # the sill
    poly(img, cm, band(a0, a1, (y0 + y1) / 2 - 0.05, (y0 + y1) / 2 + 0.05, 0.014), WHITE, INK, 1.4)   # the meeting rail


def drape(img, cm, a0, a1, top=4.7, bottom=0.0):
    """One gold drape, floor to valance, with fold lines; it stands a little proud of the wall."""
    poly(img, cm, band(a0, a1, bottom, top, 0.1, 1.5), GOLD, INK, 2.2)
    n = 4
    for k in range(1, n):
        a = a0 + (a1 - a0) * k / n
        lines(img, cm, [wp(a + 0.4, bottom + 0.05, 0.105), wp(a - 0.3, top - 0.6, 0.105)], GOLD_D, 1.8)
    lines(img, cm, [wp(a0 + 0.8, bottom + 0.05, 0.105), wp(a0 + 0.6, top - 0.4, 0.105)], GOLD_L, 2.0)
    poly(img, cm, band(a0, a1, bottom, bottom + 0.06, 0.106, 1.5), GOLD_D, INK, 1.4)          # a fringe at the hem


def valance(img, cm):
    """The swag valance across all three windows: a gold board, a swag dipping over each window, tails between."""
    lo, hi = WINDOWS[0] - WIN_HALF - 7, WINDOWS[-1] + WIN_HALF + 7
    poly(img, cm, band(lo, hi, 4.6, CORN_H - 0.02, 0.14, 1.5), GOLD, INK, 2.2)
    lines(img, cm, [wp(a, 4.95, 0.145) for a in np.arange(lo, hi + 0.1, 1.5)], GOLD_D, 1.6)
    for c in WINDOWS:
        pts = [wp(a, 4.62, 0.15) for a in np.linspace(c - 13, c + 13, 14)]
        pts += [wp(c + 13 * math.cos(math.pi * u), 4.62 - 0.55 * math.sin(math.pi * u), 0.15)
                for u in np.linspace(0, 1, 16)]
        poly(img, cm, pts, GOLD, INK, 2.2)
        for d in (0.18, 0.34):                         # the swag's soft folds
            lines(img, cm, [wp(c + 11 * math.cos(math.pi * u), 4.6 - (0.55 - d) * math.sin(math.pi * u), 0.152)
                            for u in np.linspace(0.08, 0.92, 12)], GOLD_D, 1.6)
    for c in (WINDOWS[0] - 16.5, (WINDOWS[0] + WINDOWS[1]) / 2, (WINDOWS[1] + WINDOWS[2]) / 2, WINDOWS[2] + 16.5):
        tail = [wp(c - 2.5, 4.62, 0.16), wp(c + 2.5, 4.62, 0.16), wp(c + 2.0, 3.85, 0.16), wp(c, 3.65, 0.16),
                wp(c - 2.0, 3.85, 0.16)]
        poly(img, cm, tail, GOLD_L, INK, 2.0)
        lines(img, cm, [wp(c, 4.6, 0.162), wp(c, 3.7, 0.162)], GOLD_D, 1.4)


def window_end(img, cm):
    for c in WINDOWS:
        window(img, cm, c)
    edges = [WINDOWS[0] - WIN_HALF - 7, WINDOWS[0] - WIN_HALF + 0.5]
    for k in range(len(WINDOWS) - 1):
        m = (WINDOWS[k] + WINDOWS[k + 1]) / 2
        drape(img, cm, WINDOWS[k] + WIN_HALF - 0.5, m - 0.6)
        drape(img, cm, m + 0.6, WINDOWS[k + 1] - WIN_HALF + 0.5)
    drape(img, cm, *edges)
    drape(img, cm, WINDOWS[-1] + WIN_HALF - 0.5, WINDOWS[-1] + WIN_HALF + 7)
    valance(img, cm)


# ---------------------------------------------------------------------------------------------- fireplace, alcoves, doors, portraits
@functools.lru_cache(maxsize=2)
def portrait_art(seed):
    """A generic 18th-century gentleman: dark ground, black coat, white stock, powdered grey hair (no real face)."""
    w, h = 300, 380
    im = Image.new('RGBA', (w, h), (64, 54, 44, 255))
    d = ImageDraw.Draw(im)
    d.ellipse([-60, 40, w + 60, h + 260], fill=(84, 72, 58))
    d.polygon([(40, h), (70, 250), (150, 220), (230, 250), (260, h)], fill=(30, 28, 30))      # coat
    d.polygon([(130, 225), (170, 225), (160, 290), (140, 290)], fill=(236, 232, 222))         # stock
    sk = (226, 186, 160) if seed == 0 else (214, 176, 150)
    d.ellipse([105, 105, 195, 225], fill=sk)
    d.ellipse([95, 80, 205, 150], fill=(206, 204, 200))                                        # powdered hair
    d.ellipse([92, 120, 118, 170], fill=(206, 204, 200))
    d.ellipse([182, 120, 208, 170], fill=(206, 204, 200))
    for x in (132, 168):
        d.ellipse([x - 5, 158, x + 5, 164], fill=(60, 40, 36))
    d.line([(138, 200), (162, 200)], fill=(150, 90, 84), width=3)
    return im


def framed(img, cm, a, y0, y1, half, seed, inset=0.02):
    tl, tr, br, bl = wp(a - half, y1, inset), wp(a + half, y1, inset), wp(a + half, y0, inset), wp(a - half, y0, inset)
    k = 0.85
    poly(img, cm, band(a - half - k, a + half + k, y0 - 0.12, y1 + 0.12, inset - 0.01, 1.0), GOLD, INK, 2.2)
    poly(img, cm, band(a - half - 0.35, a + half + 0.35, y0 - 0.05, y1 + 0.05, inset - 0.012, 1.0), GOLD_D, None)
    paste_on(img, cm, [tl, tr, br, bl], portrait_art(seed))
    poly(img, cm, [tl, tr, br, bl], None, INK, 1.8)


def fireplace(img, cm):
    c = FIRE
    h = 14.0
    poly(img, cm, band(c - h, c + h, 0.0, 1.38, 0.03, 1.0), WHITE, INK, 2.2)                # the marble surround
    poly(img, cm, band(c - h + 2.5, c + h - 2.5, 0.0, 1.12, 0.035, 1.0), lt(WHITE, 1.0), dk(WHITE, 0.82), 1.4)
    poly(img, cm, band(c - 7, c + 7, 0.0, 0.88, 0.04, 1.0), (34, 30, 30), INK, 2.2)          # the firebox
    for k in range(3):                                  # logs
        poly(img, cm, band(c - 4.5 + k * 0.6, c + 4.5 - k * 1.2, 0.08 + 0.12 * k, 0.2 + 0.12 * k, 0.15, 1.0),
             (110, 70, 40), INK, 1.4)
    poly(img, cm, band(c - h - 1.5, c + h + 1.5, 1.38, 1.48, -0.13, 1.0), WHITE, INK, 2.0)   # the mantel shelf
    for a, col in ((c - 9, (236, 236, 240)), (c + 9, (236, 236, 240))):                      # two vases on the mantel
        poly(img, cm, [wp(a - 0.8, 1.48, 0.12), wp(a + 0.8, 1.48, 0.12), wp(a + 1.1, 1.75, 0.12), wp(a, 1.85, 0.12),
                       wp(a - 1.1, 1.75, 0.12)], col, INK, 1.6)
        lines(img, cm, [wp(a - 0.7, 1.62, 0.122), wp(a + 0.7, 1.62, 0.122)], (40, 70, 160), 2.2)
    framed(img, cm, c, 2.05, 3.45, 6.0, 0)
    for k in range(-5, 6):                              # greenery along the mantel (ref 3)
        a = c + k * 2.4
        poly(img, cm, [wp(a - 1.4, 1.48, 0.1), wp(a, 1.66 + 0.04 * (k % 2), 0.1), wp(a + 1.4, 1.48, 0.1)], (70, 120, 70), INK, 1.2)


def alcove(img, cm, c):
    """An arched alcove: white surround, a half-dome shell at the top, shelves of books and china; a cupboard under."""
    h = 6.0
    poly(img, cm, band(c - h - 1.5, c + h + 1.5, 0.0, 4.1, 0.01, 1.0), WHITE, INK, 2.2)
    poly(img, cm, band(c - h - 0.8, c + h + 0.8, 0.0, 1.0, 0.02, 1.0), WHITE, INK, 1.8)        # the cupboard
    lines(img, cm, [wp(c, 0.08, 0.025), wp(c, 0.92, 0.025)], dk(WHITE, 0.8), 1.4)
    back = band(c - h, c + h, 1.1, 3.2, 0.015, 1.0)
    arch = [wp(c + h * math.cos(math.pi * u), 3.2 + 0.7 * math.sin(math.pi * u), 0.015) for u in np.linspace(0, 1, 14)]
    poly(img, cm, back[:len(back) // 2] + arch[::-1][::-1] + back[len(back) // 2:], dk(WALL, 0.92), INK, 2.0)
    poly(img, cm, arch + [wp(c, 3.2, 0.015)], lt(WHITE, 1.0), INK, 1.6)                       # the shell
    for u in np.linspace(0.12, 0.88, 6):
        lines(img, cm, [wp(c, 3.2, 0.018), wp(c + h * 0.9 * math.cos(math.pi * u), 3.2 + 0.62 * math.sin(math.pi * u), 0.018)],
              dk(WHITE, 0.78), 1.2)
    rng = np.random.default_rng(int(c) + 400)
    for y in (1.75, 2.45):                              # shelves, with books and plates
        poly(img, cm, band(c - h, c + h, y - 0.04, y, 0.03, 1.0), WHITE, INK, 1.4)
        a = c - h + 0.5
        while a < c + h - 1.0:
            w = rng.uniform(0.25, 0.55)
            if rng.random() < 0.3:
                ctr = wp(a + 0.6, y + 0.2, 0.03)
                poly(img, cm, [wp(a + 0.6 + 0.6 * math.cos(t), y + 0.2 + 0.18 * math.sin(t), 0.03)
                               for t in np.linspace(0, 2 * math.pi, 12, endpoint=False)], (232, 230, 236), INK, 1.2)
                del ctr
                a += 1.4
            else:
                col = [(150, 40, 40), (40, 70, 120), (60, 100, 70), (190, 160, 90)][int(rng.integers(4))]
                poly(img, cm, band(a, a + w, y, y + rng.uniform(0.24, 0.34), 0.04, 1.0), col, INK, 1.2)
                a += w + 0.05


def door(img, cm, c):
    """A white six-panel door in a moulded frame with a pediment (ref 5), a brass knob."""
    h = 4.7
    poly(img, cm, band(c - h - 1.0, c + h + 1.0, 0.0, 2.65, 0.01, 1.0), WHITE, INK, 2.2)       # the frame
    poly(img, cm, [wp(c - h - 1.6, 2.65, 0.02), wp(c + h + 1.6, 2.65, 0.02), wp(c + h + 1.2, 2.78, 0.02),
                   wp(c, 3.25, 0.02), wp(c - h - 1.2, 2.78, 0.02)], WHITE, INK, 2.2)          # the pediment
    lines(img, cm, [wp(c - h, 2.8, 0.022), wp(c, 3.12, 0.022), wp(c + h, 2.8, 0.022)], dk(WHITE, 0.8), 1.4)
    poly(img, cm, band(c - h, c + h, 0.0, 2.45, 0.015, 1.0), (240, 238, 230), INK, 2.0)
    for row, (y0, y1) in enumerate(((0.15, 0.9), (1.05, 1.55), (1.7, 2.3))):
        for sgn in (-1, 1):
            a0, a1 = (c - h + 0.7, c - 0.5) if sgn < 0 else (c + 0.5, c + h - 0.7)
            poly(img, cm, band(a0, a1, y0, y1, 0.02, 1.0), None, dk(WHITE, 0.8), 1.4)
    k = wp(c + h - 1.0, 1.0, 0.03)
    poly(img, cm, [(k[0] + 0.04 * math.cos(t), k[1] + 0.04 * math.sin(t), k[2]) for t in np.linspace(0, 6.28, 10)],
         GOLD, INK, 1.2)


def wall_things(img, cm):
    """Everything laid on the wall, far to near."""
    jobs = [((0.0, 2.0, BZ), window_end)] + \
           [(wp(FIRE, 2), fireplace)] + \
           [(wp(c, 2), functools.partial(alcove, c=c)) for c in ALCOVES] + \
           [(wp(c, 2), functools.partial(door, c=c)) for c in DOORS] + \
           [(wp(c, 2), functools.partial(lambda img, cm, c: framed(img, cm, c, 1.85, 2.95, 3.6, 1), c=c)) for c in PORTRAITS]
    for ref, fn in sorted(jobs, key=lambda j: -math.dist(j[0], cm.pos)):
        fn(img, cm)


# ---------------------------------------------------------------------------------------------- the floor and carpet
@functools.lru_cache(maxsize=1)
def carpet_art():
    """The oval carpet seen from above (one pixel a centimetre): deep blue, a cream border of flowers edged red and
    gold, and the seal at the middle: an eagle in a gold ring of stars."""
    RX, RZ = 3.8, 4.8
    W, H = int(RX * 200), int(RZ * 200)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = W / 2, H / 2

    def ell(k, fill, outline=None, width=0):
        d.ellipse([cx - cx * k, cy - cy * k, cx + cx * k, cy + cy * k], fill=fill, outline=outline, width=width)
    ell(1.0, RED + (255,), INK + (255,), 4)
    ell(0.985, GOLD + (255,))
    ell(0.97, BORDER + (255,))
    rng = np.random.default_rng(5)
    for t in np.linspace(0, 2 * math.pi, 120, endpoint=False):     # the flower garland round the border
        r = 0.915 + 0.02 * math.sin(t * 9)
        x, y = cx + cx * r * math.cos(t), cy + cy * r * math.sin(t)
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(70, 120, 70))
        col = [(196, 50, 60), (226, 140, 60), (200, 80, 120)][int(rng.integers(3))]
        d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=col)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(246, 220, 120))
    ell(0.86, GOLD + (255,))
    ell(0.85, NAVY + (255,))
    for t in np.linspace(0, 2 * math.pi, 36, endpoint=False):     # a faint inner ring of small stars in the blue
        x, y = cx + cx * 0.78 * math.cos(t), cy + cy * 0.78 * math.sin(t)
        d.regular_polygon((x, y, 9), 5, fill=lt(NAVY, 1.3))
    # the seal
    R = 190
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=GOLD, outline=INK, width=3)
    d.ellipse([cx - R + 18, cy - R + 18, cx + R - 18, cy + R - 18], fill=NAVY_D)
    for t in np.linspace(0, 2 * math.pi, 26, endpoint=False):
        x, y = cx + (R - 42) * math.cos(t), cy + (R - 42) * math.sin(t)
        d.regular_polygon((x, y, 9), 5, fill=WHITE)
    ey = cy + 6                                                      # the eagle, wings spread, a shield on its chest
    for sgn in (-1, 1):
        d.polygon([(cx + sgn * 14, ey - 30), (cx + sgn * 110, ey - 80), (cx + sgn * 118, ey - 40), (cx + sgn * 96, ey - 10),
                   (cx + sgn * 104, ey + 6), (cx + sgn * 70, ey + 10), (cx + sgn * 20, ey + 20)], fill=(120, 80, 40))
    d.polygon([(cx - 20, ey + 30), (cx + 20, ey + 30), (cx + 12, ey + 80), (cx - 12, ey + 80)], fill=(120, 80, 40))
    d.ellipse([cx - 18, ey - 76, cx + 18, ey - 36], fill=WHITE)
    d.polygon([(cx + 12, ey - 60), (cx + 30, ey - 54), (cx + 12, ey - 48)], fill=GOLD_L)
    d.rectangle([cx - 24, ey - 30, cx + 24, ey - 14], fill=(40, 60, 150))
    d.polygon([(cx - 24, ey - 14), (cx + 24, ey - 14), (cx + 22, ey + 22), (cx, ey + 36), (cx - 22, ey + 22)], fill=WHITE)
    for k in range(5):
        x = cx - 20 + k * 10
        d.line([(x, ey - 12), (x, ey + 26 - abs(k - 2) * 4)], fill=RED, width=5)
    return im.resize((W * 2, H * 2), Image.LANCZOS)    # smooth edges when the camera is close


def floor(img, cm):
    poly(img, cm, [floor_pt(a) for a in range(0, 360, 3)], FLOOR, INK, 2.0)
    for x in np.arange(-A + 0.3, A, 0.32):              # floorboards running north-south
        zz = BZ * math.sqrt(max(0.0, 1 - (x / A) ** 2)) - 0.02
        lines(img, cm, [(x, 0.001, -zz), (x, 0.001, zz)], FLOOR_L, 1.2)
    RX, RZ = 3.8, 4.8
    paste_tiled(img, cm, -RX, RX, -RZ, RZ, 0.003, carpet_art())


# ---------------------------------------------------------------------------------------------- furniture
def _at(x, z, yaw):
    def at(lx, ly, lz):
        q = S.rot_y((lx, ly, lz), yaw)
        return (x + q[0], ly, z + q[2])
    return at


def desk_parts():
    """The Resolute desk (1.83 x 0.91 x 0.76 m, dark carved oak), front to the room: two pedestals, the panelled
    kneehole door with an oval carving, a moulded top; phones and a box on it."""
    x, z = DESK
    yaw = 180.0
    at = _at(x, z, yaw)

    def front(img, cm, p):
        for sgn in (-1, 1):                            # the pedestals' carved panels
            u0, u1 = sgn * 0.88, sgn * 0.5
            for y0, y1 in ((0.08, 0.34), (0.38, 0.64)):
                cm.poly(p, [at(u0 + 0.04 * sgn * -1, y0, 0.457), at(u1, y0, 0.457), at(u1, y1, 0.457),
                            at(u0 + 0.04 * sgn * -1, y1, 0.457)], WOOD_L, INK, 1.4)
        cm.poly(p, [at(-0.42, 0.04, 0.457), at(0.42, 0.04, 0.457), at(0.42, 0.66, 0.457), at(-0.42, 0.66, 0.457)],
                WOOD_D, INK, 1.8)                      # the kneehole door
        cm.poly(p, [at(0.18 * math.cos(t), 0.35 + 0.2 * math.sin(t), 0.458) for t in np.linspace(0, 6.28, 16)],
                WOOD_L, INK, 1.6)                      # its oval carving
        cm.poly(p, [at(0.08 * math.cos(t), 0.35 + 0.09 * math.sin(t), 0.459) for t in np.linspace(0, 6.28, 12)],
                GOLD_D, INK, 1.2)
        cm.line(p, [at(-0.9, 0.7, 0.458), at(0.9, 0.7, 0.458)], WOOD_D, 1.6)
    parts = [obox(at(0, 0, 0), (1.83, 0.7, 0.91), yaw, {'all': WOOD, 'front': WOOD}, extras={'front': front}),
             obox(at(0, 0.7, 0), (1.9, 0.06, 0.97), yaw, {'all': WOOD_D, 'top': (96, 58, 32)})]
    for u in (-0.6, -0.3):                             # two phones (ref 3)
        parts.append(obox(at(u, 0.76, -0.12), (0.2, 0.06, 0.22), yaw, {'all': (36, 36, 40), 'top': (60, 62, 68)}))
    parts.append(obox(at(0.55, 0.76, -0.1), (0.24, 0.07, 0.16), yaw, {'all': (110, 40, 36), 'top': (130, 50, 44)}))
    return parts


def leather_chair_parts(x, z, facing):
    """A tall brown tufted leather desk chair (ref 1)."""
    at = _at(x, z, facing)

    def tufts(img, cm, p):
        for r in range(4):
            for c in range(3):
                q = at(-0.18 + 0.18 * c, 0.75 + 0.15 * r, -0.21)
                cm.poly(p, [(q[0] + 0.015 * math.cos(t), q[1] + 0.015 * math.sin(t), q[2]) for t in np.linspace(0, 6.28, 6)],
                        dk(LEATHER, 0.7), None)
    return [cylinder(at(0, 0, 0), 0.3, 0.05, {'side': (40, 40, 44), 'top': (54, 54, 60)}, n=10),
            cylinder(at(0, 0.05, 0), 0.04, 0.38, {'side': (60, 60, 66), 'top': (60, 60, 66)}, n=8),
            obox(at(0, 0.43, 0.02), (0.62, 0.12, 0.58), facing, {'all': LEATHER}),
            obox(at(0, 0.55, -0.26), (0.64, 0.82, 0.1), facing, {'all': LEATHER, 'front': lt(LEATHER, 1.1)},
                 extras={'front': tufts}),
            obox(at(-0.32, 0.55, 0.0), (0.08, 0.2, 0.5), facing, {'all': dk(LEATHER, 0.9)}),
            obox(at(0.32, 0.55, 0.0), (0.08, 0.2, 0.5), facing, {'all': dk(LEATHER, 0.9)})]


def wood_chair_parts(x, z, facing, seat=SEAT):
    """A wooden chair with a gold upholstered seat and back panel (refs 1, 3)."""
    at = _at(x, z, facing)
    parts = [obox(at(u, 0, w), (0.05, 0.44, 0.05), facing, {'all': WOOD}) for u in (-0.22, 0.22) for w in (-0.2, 0.2)]
    parts += [obox(at(0, 0.42, 0), (0.52, 0.08, 0.48), facing, {'all': seat, 'front': dk(seat, 0.85)}),
              obox(at(0, 0.5, -0.22), (0.5, 0.5, 0.05), facing, {'all': WOOD, 'front': seat}),
              obox(at(0, 1.0, -0.22), (0.54, 0.06, 0.06), facing, {'all': WOOD})]
    return parts


def sofa_parts(x, z, facing):
    """A cream three-seat sofa (ref 3): base, back, rolled arms, seat cushions."""
    at = _at(x, z, facing)
    L = 2.1
    parts = [obox(at(0, 0.0, 0), (L, 0.42, 0.85), facing, {'all': SOFA, 'front': dk(SOFA, 0.92)}),
             obox(at(0, 0.42, -0.33), (L, 0.45, 0.2), facing, {'all': SOFA}),
             obox(at(-L / 2 + 0.1, 0.42, 0.02), (0.2, 0.22, 0.8), facing, {'all': lt(SOFA, 1.02)}),
             obox(at(L / 2 - 0.1, 0.42, 0.02), (0.2, 0.22, 0.8), facing, {'all': lt(SOFA, 1.02)})]
    for k in range(3):
        u = -0.62 + 0.62 * k
        parts.append(obox(at(u, 0.42, 0.06), (0.6, 0.1, 0.6), facing, {'all': lt(SOFA, 1.03)}))
        parts.append(obox(at(u, 0.5, -0.2), (0.58, 0.36, 0.14), facing, {'all': lt(SOFA, 1.03)}))
    parts.append(obox(at(-0.6, 0.58, -0.08), (0.36, 0.34, 0.1), facing, {'all': (60, 90, 70)}))   # a green cushion (ref 2)
    parts.append(obox(at(0.6, 0.58, -0.08), (0.36, 0.34, 0.1), facing, {'all': (60, 90, 70)}))
    return parts


def armchair_parts(x, z, facing):
    """A yellow upholstered armchair with a high back (ref 3)."""
    at = _at(x, z, facing)
    return [obox(at(0, 0, 0), (0.8, 0.44, 0.8), facing, {'all': YELLOW, 'front': dk(YELLOW, 0.9)}),
            obox(at(0, 0.44, -0.32), (0.8, 0.62, 0.16), facing, {'all': YELLOW}),
            obox(at(-0.34, 0.44, 0.02), (0.12, 0.22, 0.72), facing, {'all': lt(YELLOW, 1.04)}),
            obox(at(0.34, 0.44, 0.02), (0.12, 0.22, 0.72), facing, {'all': lt(YELLOW, 1.04)}),
            obox(at(0, 0.44, 0.06), (0.56, 0.1, 0.6), facing, {'all': lt(YELLOW, 1.05)})]


def coffee_table_parts():
    """A low dark table between the sofas, a bowl of blue and white flowers on it (ref 3)."""
    x, z = 0.0, -2.7
    parts = [obox((x, 0.38, z), (0.85, 0.06, 1.5), 0, {'all': WOOD_D, 'top': WOOD}),
             obox((x, 0.0, z), (0.7, 0.38, 1.3), 0, {'all': dk(WOOD_D, 0.9)})]
    parts.append(cylinder((x, 0.44, z), 0.14, 0.1, {'side': WHITE, 'top': WHITE}, n=10))

    def flowers(img, cm, p):
        rng = np.random.default_rng(9)
        for _ in range(18):
            q = (x + rng.uniform(-0.17, 0.17), 0.58 + rng.uniform(0, 0.12), z + rng.uniform(-0.17, 0.17))
            r = 0.035
            col = (60, 90, 190) if rng.random() < 0.6 else WHITE
            cm.poly(p, [(q[0] + r * math.cos(t), q[1] + r * math.sin(t), q[2]) for t in np.linspace(0, 6.28, 7)], col, INK, 1.0)
    parts.append([Face([(x, 0.6, z)] * 3, None, None, None, 0, None)])
    parts[-1][0].draw = lambda img, cm, p: flowers(img, cm, p)
    return parts


def credenza_parts():
    """The low table under the middle window with family photos in frames (ref 1)."""
    x, z = 0.0, 4.75
    parts = [obox((x, 0.0, z), (2.0, 0.78, 0.42), 180, {'all': WOOD, 'top': WOOD_L})]
    for k, u in enumerate((-0.8, -0.5, -0.2, 0.15, 0.45, 0.78)):
        h = 0.22 + 0.06 * (k % 2)
        parts.append(obox((x + u, 0.78, z), (0.18, h, 0.03), 180, {'all': GOLD, 'front': (190, 196, 204)}))
    return parts


def flag_parts(x, z, kind):
    """A flag on a tall pole with a gold eagle finial, hanging in folds (the US flag: stripes and the blue canton; the
    President's: navy with a gold fringe)."""
    parts = [cylinder((x, 0, z), 0.16, 0.06, {'side': GOLD_D, 'top': GOLD}, n=10),
             cylinder((x, 0.06, z), 0.02, 2.7, {'side': (150, 110, 60), 'top': GOLD}, n=6)]
    top, low = 2.55, 1.0

    def cloth(img, cm, p):
        n = 7
        w = 0.5
        for k in range(n):                             # vertical folds, each its own strip
            u0, u1 = x - 0.03 + w * k / n, x - 0.03 + w * (k + 1) / n
            zz = z - 0.05 * (k % 2)
            hem = low + 0.25 * (k / n) + 0.04 * (k % 2)
            if kind == 'us':
                col = WHITE if k % 2 == 0 else dk(WHITE, 0.9)
            else:
                col = NAVY if k % 2 == 0 else NAVY_D
            pts = [(u0, top, zz), (u1, top, zz), (u1, hem, zz), (u0, hem, zz)]
            cm.poly(p, pts, col, INK, 1.4)
            if kind == 'us':
                for y in np.arange(hem + 0.1, top, 0.16):
                    cm.poly(p, [(u0, y, zz - 0.001), (u1, y, zz - 0.001), (u1, y + 0.07, zz - 0.001),
                                (u0, y + 0.07, zz - 0.001)], RED if k % 2 == 0 else dk(RED, 0.88), None)
            else:
                cm.poly(p, [(u0, hem, zz - 0.001), (u1, hem, zz - 0.001), (u1, hem + 0.07, zz - 0.001),
                            (u0, hem + 0.07, zz - 0.001)], GOLD, None)
        if kind == 'us':
            cm.poly(p, [(x - 0.03, top, z - 0.06), (x + 0.22, top, z - 0.06), (x + 0.22, top - 0.55, z - 0.06),
                        (x - 0.03, top - 0.55, z - 0.06)], NAVY, INK, 1.4)
            for k in range(6):
                q = (x + 0.02 + 0.07 * (k % 3), top - 0.1 - 0.15 * (k // 3), z - 0.061)
                cm.poly(p, [(q[0] + 0.018 * math.cos(t), q[1] + 0.018 * math.sin(t), q[2]) for t in np.linspace(0, 6.28, 6)],
                        WHITE, None)
        else:
            cm.poly(p, [(x + 0.12 + 0.1 * math.cos(t), top - 0.4 + 0.1 * math.sin(t), z - 0.06) for t in np.linspace(0, 6.28, 10)],
                    GOLD, INK, 1.2)
        # the finial: a gold ball and a small eagle
        cm.poly(p, [(x + 0.05 * math.cos(t), 2.82 + 0.05 * math.sin(t), z) for t in np.linspace(0, 6.28, 10)], GOLD, INK, 1.4)
        cm.poly(p, [(x - 0.12, 2.98, z), (x, 2.9, z), (x + 0.12, 2.98, z), (x + 0.03, 2.86, z), (x - 0.03, 2.86, z)],
                GOLD, INK, 1.2)
    parts.append([Face([(x, 2.0, z)] * 3, None, None, None, 0, None)])
    parts[-1][0].draw = lambda img, cm, p: cloth(img, cm, p)
    return parts


def clock_parts():
    """A grandfather clock against the wall left of the fireplace (ref 3)."""
    a = 157.0
    x, _, z = wp(a, 0, 0.3)
    yaw = wall_yaw(a)
    at = _at(x, z, yaw)

    def face(img, cm, p):
        c = at(0, 1.95, 0.16)
        cm.poly(p, [at(0.17 * math.cos(t), 1.95 + 0.17 * math.sin(t), 0.161) for t in np.linspace(0, 6.28, 16)],
                (240, 232, 210), INK, 1.4)
        cm.line(p, [c, at(0.0, 2.07, 0.162)], INK, 1.6)
        cm.line(p, [c, at(0.08, 1.95, 0.162)], INK, 1.6)
        cm.poly(p, [at(-0.12, 0.5, 0.161), at(0.12, 0.5, 0.161), at(0.12, 1.5, 0.161), at(-0.12, 1.5, 0.161)],
                dk(WOOD_D, 0.8), INK, 1.2)
    return [obox(at(0, 0, 0), (0.5, 0.35, 0.34), yaw, {'all': WOOD_D}),
            obox(at(0, 0.35, 0), (0.4, 1.35, 0.3), yaw, {'all': WOOD, 'front': WOOD}, extras={'front': face}),
            obox(at(0, 1.7, 0), (0.5, 0.55, 0.34), yaw, {'all': WOOD_D, 'front': WOOD_D}, extras={'front': face}),
            obox(at(0, 2.25, 0), (0.56, 0.12, 0.38), yaw, {'all': WOOD_D})]


def console_parts(a):
    """A side table against the wall under a portrait, a bronze bust on it (ref 1)."""
    x, _, z = wp(a, 0, 0.3)
    yaw = wall_yaw(a)
    at = _at(x, z, yaw)

    def bust(img, cm, p):
        S.blob3(img, cm, p, S.sphere_pts(at(0, 1.18, 0), 0.11, 8, 1.25), BRONZE, INK, 1.6)
        cm.poly(p, [at(-0.16, 0.88, 0), at(0.16, 0.88, 0), at(0.12, 1.04, 0), at(-0.12, 1.04, 0)], BRONZE, INK, 1.6)
    parts = [obox(at(0, 0.0, 0), (0.95, 0.8, 0.42), yaw, {'all': WOOD, 'top': WOOD_L}),
             obox(at(0, 0.8, 0), (0.18, 0.08, 0.18), yaw, {'all': (220, 220, 214)})]
    parts.append([Face([at(0, 1.1, 0)] * 3, None, None, None, 0, None)])
    parts[-1][0].draw = lambda img, cm, p: bust(img, cm, p)
    return parts


def items(people=None):
    """Everything standing in the room, each (reference point, draw(img, cam)), drawn far to near after the floor.
    people: [(x, z, draw)]."""
    out = []

    def part_item(parts, ref):
        return (ref, lambda img, cm, parts=parts: draw_parts(img, cm, parts, _pen(img)))
    out.append(part_item(credenza_parts(), (0.0, 0.5, 4.75)))
    for x, z, kind in FLAGS:
        out.append(part_item(flag_parts(x, z, kind), (x, 1.5, z)))
    out.append(part_item(leather_chair_parts(*DESK_CHAIR, 180.0), (DESK_CHAIR[0], 0.8, DESK_CHAIR[1] + 0.1)))
    out.append(part_item(desk_parts(), (DESK[0], 0.5, DESK[1])))
    for x, z in VISITOR_CHAIRS:
        out.append(part_item(wood_chair_parts(x, z, 0.0), (x, 0.5, z)))
    for (x, z), yaw in zip(SOFAS, (90.0, -90.0)):
        out.append(part_item(sofa_parts(x, z, yaw), (x, 0.5, z)))
    out.append(part_item(coffee_table_parts(), (0.0, 0.4, -2.7)))
    for x, z in ARMCHAIRS:
        out.append(part_item(armchair_parts(x, z, 0.0), (x, 0.5, z)))
    out.append(part_item(clock_parts(), wp(157.0, 1.0, 0.3)))
    for a in PORTRAITS:
        out.append(part_item(console_parts(a), wp(a, 0.5, 0.3)))
    for x, z, fn in people or []:
        out.append(((x, 1.0, z), fn))
    return out


def render(img, cm, people=None):
    """The room through `cm` on img (a frame: 1080 x 1920 times B.SS)."""
    img.paste(CEIL + (255,), (0, 0) + img.size)
    walls(img, cm)
    wall_things(img, cm)
    floor(img, cm)
    for ref, fn in sorted(items(people), key=lambda it: -math.dist(it[0], cm.pos)):
        fn(img, cm)
    return img


# ---------------------------------------------------------------------------------------------- people in it
def put(img, cm, sp, x, z, facing, j=None, t=0.0, head_yaw=None, lift=0.0):
    """Someone standing at floor point (x, z) facing `facing` (plan degrees), `lift` metres up (Satan floats), through
    the camera (netan_yahoo's put)."""
    import views as V
    f = sp.get('height', 1.75) / 1.75
    neck = 928 * V.M_PER_UNIT * f + lift
    if cm.depth((x, neck, z)) < 0.3:
        return None
    (Xn, Yn), k = cm.project((x, neck, z))
    (Xf, Yf), _ = cm.project((x, lift, z))
    s = max(1e-3, (Yf - Yn) / 928.0)
    fd = (math.sin(math.radians(facing)), math.cos(math.radians(facing)))
    yaw = cm.yaw_of((x, 0, z), fd)
    return V.person(img, FLAT, Xf, Yf - 928 * s, s, dict(sp, full=True, pose='custom'), t, yaw, j, head_yaw)


def put_seated(img, cm, sp, x, z, facing, t=0.0):
    """Someone seated on a chair the set draws, at (x, z) facing `facing` (newsdesk_set's way)."""
    import views as V
    import moves
    f = sp.get('height', 1.75) / 1.75
    neck = 928 * V.M_PER_UNIT * f
    (Xn, Yn), k = cm.project((x, neck, z))
    (Xf, Yf), _ = cm.project((x, 0.0, z))
    s = max(1e-3, (Yf - Yn) / 928.0)
    fd = (math.sin(math.radians(facing)), math.cos(math.radians(facing)))
    yaw = cm.yaw_of((x, 0, z), fd)
    j = moves.seated(sp)
    j['seated'] = False
    return V.person(img, FLAT, Xf, Yf - 928 * s, s, dict(sp, full=True, pose='custom'), t, yaw, j)


def test_people():
    """The test placing: Trump at the desk, Satan in front of it (left), Epstein by the right chair."""
    import midterminal_cast as MC
    tx, tz = DESK_CHAIR
    return [(tx, tz - 0.3, lambda im, c: put_seated(im, c, MC.TRUMP, tx, tz - 0.05, 180.0)),   # sorted at the seat's
            # front, so the chair's back covers him from behind and the desk covers his legs from the front
            (-1.25, 1.35, lambda im, c: put(im, c, MC.SATAN, -1.25, 1.35, 30.0)),
            (1.35, 1.25, lambda im, c: put(im, c, MC.EPSTEIN, 1.35, 1.25, -30.0))]


# ---------------------------------------------------------------------------------------------- sheets
def frame(name, people=True):
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 255))
    return render(img, cam(name), test_people() if people else None)


def test(out, people=True):
    B.SS = 1
    tiles = [(name, frame(name, people)) for name in ('wide', 'desk', 'reverse', 'high')]
    sheet = Image.new('RGB', (4 * 540 + 5 * 20, 960 + 90), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 30)
    for i, (name, img) in enumerate(tiles):
        sheet.paste(img.convert('RGB').resize((540, 960), Image.LANCZOS), (20 + i * 560, 70))
        d.text((20 + i * 560, 20), f'camera: {name}', font=f, fill=(30, 30, 30))
    sheet.save(out, quality=88)
    return out


def refsheet(out):
    """Rule 3 by hand: Sam's photos beside ours: the desk end (ref 1), the far end (ref 3 top), from above (ref 5)."""
    B.SS = 1
    H = 420

    def fit(im):
        return im.resize((int(im.width * H / im.height), H), Image.LANCZOS)
    rows = [('desk end', ['oval-1-desk-gold.jpg'], frame('wide', False).crop((0, 500, 1080, 1340))),
            ('fireplace end', ['oval-3-both-ends.jpg'], frame('reverse', False).crop((0, 500, 1080, 1340))),
            ('from above', ['oval-5-fisheye.jpg'], frame('high', False).crop((0, 400, 1080, 1440)))]
    tiles = []
    for label, refs, ours in rows:
        ims = [fit(Image.open(os.path.join(REFS, r)).convert('RGB')) for r in refs] + [fit(ours.convert('RGB'))]
        tiles.append((label, ims))
    W = max(sum(i.width for i in ims) + 20 * (len(ims) + 1) for _, ims in tiles)
    sheet = Image.new('RGB', (W, len(tiles) * (H + 70) + 20), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 28)
    y = 20
    for label, ims in tiles:
        d.text((20, y), f"{label}: Sam's photo left, ours right", font=f, fill=(30, 30, 30))
        x = 20
        for im in ims:
            sheet.paste(im, (x, y + 40))
            x += im.width + 20
        y += H + 70
    sheet.save(out, quality=88)
    return out


def picture(name='wide'):
    """One frame from a named camera, the cast placed: the kit catalogue's tile."""
    img = Image.new('RGBA', (1080 * B.SS, 1920 * B.SS), (0, 0, 0, 255))
    return render(img, cam(name), test_people())


def ghost(img, draw, tint=(232, 104, 44), alpha=0.72):
    """Draw someone as the hellfire ghost: onto their own layer, pulled towards fire orange, see-through (flat: no
    glow). draw(layer) draws them."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw(lay)
    a = np.asarray(lay).astype(np.float32)
    rgb = a[..., :3] * 0.45 + np.array(tint, np.float32) * 0.55
    out = np.dstack([rgb, a[..., 3] * alpha]).clip(0, 255).astype(np.uint8)
    img.alpha_composite(Image.fromarray(out, 'RGBA'))


COMP = [   # the key shots (rule 11): name, camera (pos, look, focal), who's in it
    ('1  Trump comes in: "Thank you, everyone, no more questions."', ((1.4, 1.6, -0.2), (4.0, 1.35, -2.0), 1050), 'door'),
    ('2  Trump: "Satan, what the f***?"  Satan floats before the desk', ((0.0, 1.55, -1.7), (-0.05, 1.4, 2.5), 1080), 'two'),
    ('3  Zoom out: Epstein\'s ghost fades in by the desk', ((0.2, 1.6, -1.4), (0.3, 1.4, 2.6), 780), 'three'),
    ('4  Epstein: "It\'s warm here."', ((1.0, 1.6, 0.9), (1.6, 1.6, 3.0), 1250), 'three'),
]


def to_cam(cm, x, z):
    """The plan facing that turns someone at (x, z) square to the lens (rule 38: front on)."""
    return math.degrees(math.atan2(cm.pos[0] - x, cm.pos[2] - z))


def comp(out):
    """The composition sheet: the 3-4 key shots, still, before anything is built to move."""
    import midterminal_cast as MC
    B.SS = 1
    dx, _, dz = wp(112.0, 0, 0.35)
    tiles = []
    for label, (pos, look, focal), who in COMP:
        cm = S.Cam(pos, look, focal=focal)
        ppl = []
        if who == 'door':
            ppl.append((dx, dz, lambda im, c: put(im, c, dict(MC.TRUMP, look=0.9), dx, dz, to_cam(c, dx, dz))))
        else:
            ppl.append((0.45, 2.15, lambda im, c: put(im, c, dict(MC.SATAN, look=-0.6 if who == 'two' else 0.8),
                                                        0.45, 2.15, to_cam(c, 0.45, 2.15), lift=0.3)))
            ppl.append((-0.7, 1.0, lambda im, c: put(im, c, dict(MC.TRUMP, look=0.8, frown=0.03), -0.7, 1.0, to_cam(c, -0.7, 1.0))))
        if who == 'three':
            ppl.append((1.6, 3.0, lambda im, c: ghost(im, lambda lay: put(lay, c, dict(MC.EPSTEIN, look=-0.8), 1.6, 3.0,
                                                                         to_cam(c, 1.6, 3.0), lift=0.25))))
        img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 255))
        render(img, cm, ppl)
        tiles.append((label, img))
    sheet = Image.new('RGB', (4 * 540 + 5 * 20, 960 + 110), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 20)
    for i, (label, img) in enumerate(tiles):
        sheet.paste(img.convert('RGB').resize((540, 960), Image.LANCZOS), (20 + i * 560, 90))
        d.multiline_text((20 + i * 560, 14), label.replace(': ', ':\n', 1).replace('  Satan', '\nSatan'), font=f, fill=(30, 30, 30))
    sheet.save(out, quality=88)
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'comp':
        print(comp(sys.argv[2]))
    elif sys.argv[1] == 'test':
        print(test(sys.argv[2], '--empty' not in sys.argv))
    elif sys.argv[1] == 'refs':
        print(refsheet(sys.argv[2]))
