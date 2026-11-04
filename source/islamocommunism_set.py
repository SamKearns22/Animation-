#!/usr/bin/env python3
"""MAP  Islamocommunism (Sam, 4 Nov): the White House north front, three years into Islamic communism. One locked
camera (shot 1), so one flat painting in layers (rule 39), drawn fresh each frame for what moves: the two flags wave,
the fountain plays, flying cars stream past in orderly lanes, families play on the lawn. References:
references/islamocommunism/ (White House 89a1ee64, 49db6798; St Basil's f176063d; Dome of the Rock 2ab87cb9;
flags 77252a6f, 9b28a4a2).

What makes the place (the BENCHMARK list, rule 3; ticked on the `refs` sheet):
  - the white north front: four Ionic columns under a pediment, the porch's three bays (door with a fanlight, a lantern
    hanging between the middle columns)
  - four windows each side of the porch on two floors; the lower ones under alternating triangular and curved heads
  - a balustrade along the roof, two chimneys behind it
  - the round fountain with a tall jet, inside a ring of red flowers edged in white
  - a row of round clipped bushes along the front; big trees both sides overlapping the ends; the green lawn
  - a flag on the roof above the entrance
  - NEW: the Dome of the Rock's gold dome on its blue-tiled drum behind the pediment (crescent on top)
  - NEW: two St Basil's onion spires either side (red brick towers, white arches; one blue-and-white twisted onion,
    one green with gold and red); plain gold tips, no crosses
  - NEW: the flag (red and green stripes; a navy canton of gold hammers and sickles and white crescents with stars)
    on the roof and on a tall pole on the lawn; flying cars in lanes above; families playing on the lawn

Frame coordinates are pixels of the 1080 x 1920 frame. The front is mapped from Sam's photo 89a1ee64 (cropped to
x 0-588, y 40-250, scaled to 1080 wide): `fx`, `fy` turn that crop's pixels into ours. Wind blows to the right (Sam, 4 Nov: turned round), so
both flags fly left from their poles (the canton stays at the pole). The Hook Text sits at y 410 in the sky, the heading
lower-left (x 60-640, y 1270-1490); nothing important is drawn under either (KEEP_CLEAR).

    python3 source/islamocommunism_set.py test OUT.jpg   the front at three times (things moving)
    python3 source/islamocommunism_set.py refs OUT.jpg   Sam's photos beside ours, the BENCHMARK list ticked
    python3 source/islamocommunism_set.py comp OUT.jpg   the composition sheet: the four key shots

Map: colours 50 | helpers 80 | sky, clouds, cars 110 | dome, spires 190 | building 290 | flag 410 | trees, hedges,
lawn, flower ring, fountain 500 | families 590 | paint 690 | sheets 720. Everything but the near car lanes is drawn
90 px higher than it shows (SHIFT, in paint), so read frame heights as the code's plus 90
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import sets as S                 # noqa: E402
from ed import INK               # noqa: E402

FLAT = S.FLAT
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
REFS = os.path.join(HERE, '..', 'references', 'islamocommunism')

# ---------------------------------------------------------------------------------------------- colours
SKY = (156, 204, 238)
CLOUD = (246, 248, 250)
WHITE = (246, 244, 238)
SHADE = (214, 214, 206)
RECESS = (196, 198, 192)
GLASS = (62, 78, 76)
GOLD = (226, 178, 58)
GOLD_D = (184, 136, 36)
TILE = (40, 92, 172)
TILE_D = (28, 62, 128)
TURQ = (92, 186, 196)
BRICK = (196, 82, 58)
BRICK_D = (156, 60, 44)
TREE = (74, 128, 66)
TREE_D = (52, 98, 52)
TREE_F = (98, 140, 92)
HEDGE = (46, 96, 50)
LAWN = (108, 176, 72)
LAWN_2 = (102, 169, 68)
FLOWER = (216, 36, 40)
FLOWER_D = (170, 24, 30)
WATER = (226, 240, 250)
POOL = (150, 196, 222)
F_RED = (196, 36, 44)
F_GREEN = (22, 130, 70)
F_NAVY = (34, 48, 112)
KEEP_CLEAR = [('hook text', (180, 315, 790, 500)), ('heading', (60, 1270, 640, 1490))]   # x0, y0, x1, y1 (frame)


# ---------------------------------------------------------------------------------------------- helpers
def pen(img):
    return B.Pen(img, FLAT)


def wob(pts, amt=1.6):
    """Hand-cut corners (the house look): each point nudged by its own fixed amount, the same every frame."""
    out = []
    for x, y in pts:
        h = hash((round(x, 1), round(y, 1))) & 0xffff
        out.append((x + ((h & 0xff) / 255 - 0.5) * 2 * amt, y + ((h >> 8) / 255 - 0.5) * 2 * amt))
    return out


def poly(img, pts, fill, line=INK, lw=2.4, amt=1.6):
    pen(img).poly(wob(pts, amt) if amt else pts, fill, line, lw)


def rect(img, x0, y0, x1, y1, fill, line=INK, lw=2.4):
    poly(img, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, line, lw)


def ell(img, cx, cy, rx, ry, fill, line=INK, lw=2.4):
    pen(img).ell(cx, cy, rx, ry, fill, line, lw)


def blob(cx, cy, r, seed, n=22, lump=0.16, squash=1.0):
    """A lumpy round shape (tree crowns, bushes, clouds): never a perfect circle."""
    rng = np.random.default_rng(seed)
    k = rng.uniform(-lump, lump, 5)
    ph = rng.uniform(0, 6.28, 5)
    pts = []
    for a in np.linspace(0, 2 * math.pi, n, endpoint=False):
        rr = r * (1 + sum(k[i] * math.sin((i + 2) * a + ph[i]) for i in range(5)) / 2.2)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * squash))
    return pts


def fx(x):
    """Sam's photo 89a1ee64 (the crop) to our frame, across."""
    return 540 + (x - 558) * 1.05


def fy(y):
    return 1090 + (y - 370) * 1.05


def ppm(y):
    """Pixels per metre on the lawn at frame height y (the front is about 18 px a metre)."""
    return 17 + max(0.0, y - 1090) * 0.15


# ---------------------------------------------------------------------------------------------- sky, clouds, cars
def sky(img):
    pen(img).d.rectangle([0, 0, img.width, img.height], fill=SKY)
    for cx, cy, r, sd in ((150, 520, 70, 1), (260, 500, 55, 2), (900, 470, 64, 3), (980, 490, 48, 4),
                          (620, 150, 60, 5), (720, 165, 48, 6)):
        poly(img, blob(cx, cy, r, sd, squash=0.55), CLOUD, None, amt=0)


CAR_COLS = [(214, 58, 52), (36, 160, 150), (242, 196, 60), (236, 236, 232), (60, 120, 200), (130, 190, 80)]
LANES = [   # y, direction (+1 right), speed px/s, spacing px, size, drawn behind the building?
    dict(y=575, dir=-1, speed=70, gap=150, s=0.42, behind=True, seed=4),
    dict(y=505, dir=1, speed=90, gap=180, s=0.55, behind=True, seed=3),
    dict(y=265, dir=-1, speed=150, gap=260, s=0.85, behind=False, seed=2),
    dict(y=175, dir=1, speed=180, gap=300, s=1.0, behind=False, seed=1),
]


def car(img, x, y, s, col, d):
    """A flying car: a rounded body with a bubble canopy, two hover pods underneath, speed streaks behind (flat)."""
    L, Hh = 130 * s, 34 * s
    back = x - d * L * 0.5
    for k, dy in enumerate((-0.25, 0.15, 0.45)):              # streaks: short white dashes behind, in the house style
        x0 = back - d * (14 + 10 * k) * s
        pen(img).line([(x0, y + dy * Hh), (x0 - d * (48 - 12 * k) * s, y + dy * Hh)], CLOUD, max(1.5, 5 * s))
    pts = []
    for a in np.linspace(0, 2 * math.pi, 26, endpoint=False):
        ca, sa = math.cos(a), math.sin(a)
        r = 1.0 + (0.12 * d * ca if sa < 0 else 0)            # the nose a touch fuller
        pts.append((x + ca * L * 0.5 * r, y + sa * Hh * (0.55 if sa < 0 else 0.5)))
    for sg in (-1, 1):                                         # hover pods
        ell(img, x + sg * L * 0.26, y + Hh * 0.55, L * 0.12, Hh * 0.22, (70, 74, 84), INK, 1.6)
    poly(img, pts, col, INK, 2.0, amt=0)
    ell(img, x + d * L * 0.08, y - Hh * 0.38, L * 0.22, Hh * 0.42, (190, 228, 246), INK, 1.8)   # canopy
    pen(img).line([(x - d * L * 0.42, y + Hh * 0.05), (x + d * L * 0.42, y + Hh * 0.05)], dk(col, 0.75), max(1, 2 * s))


def lane(img, ln, t):
    span = 1080 + 400
    rng = np.random.default_rng(ln['seed'])
    n = int(span // ln['gap']) + 1
    cols = [CAR_COLS[i] for i in rng.integers(0, len(CAR_COLS), n)]
    for i in range(n):
        x = (i * ln['gap'] + ln['dir'] * ln['speed'] * t) % span - 200
        bob = 2.5 * ln['s'] * math.sin(t * 3.1 + i * 1.7)
        car(img, x, ln['y'] + bob, ln['s'], cols[i], ln['dir'])


# ---------------------------------------------------------------------------------------------- dome, spires
def dome(img):
    """The Dome of the Rock's gold dome on its blue-tiled drum, behind the pediment."""
    cx, base, top_drum = 540, 860, 670
    rect(img, cx - 136, top_drum, cx + 136, base, TILE)
    rect(img, cx - 142, top_drum - 12, cx + 142, top_drum + 4, TURQ)                 # the rim
    for k in range(8):                                          # arched windows round the drum
        x = cx - 112 + k * 32
        poly(img, [(x - 8, 750), (x - 8, 718), (x, 706), (x + 8, 718), (x + 8, 750)], TILE_D, INK, 1.4, amt=0.6)
    pen(img).d.rectangle([cx - 136, 686, cx + 136, 694], fill=TURQ)                  # a tiled band
    for k in range(18):
        x = cx - 132 + k * 15
        pen(img).d.polygon([(x, 690), (x + 5, 685), (x + 10, 690), (x + 5, 695)], fill=(236, 236, 226))
    prof = []
    for s in np.linspace(0, 1, 24):                             # a slightly pointed dome
        prof.append((150 * (1 - s ** 2.1) ** 0.55, top_drum - 6 - s * 196))
    pts = [(cx - w, y) for w, y in prof] + [(cx + w, y) for w, y in prof[::-1]]
    pen(img).poly(pts, GOLD, None)
    shade = [(cx + w * 0.45, y) for w, y in prof] + [(cx + w, y) for w, y in prof[::-1]]
    pen(img).poly(shade, GOLD_D, None)                          # the shadow side, flat
    for f in (-0.75, -0.4, 0.0, 0.4, 0.75):                     # ribs
        pen(img).line([(cx + w * f, y) for w, y in prof[:-2]], GOLD_D, 1.6)
    pen(img).poly(pts, None, INK, 2.6)
    tip = top_drum - 202
    pen(img).line([(cx, tip + 4), (cx, tip - 30)], GOLD_D, 4)
    for yy, r in ((tip - 14, 7), (tip - 28, 5)):
        ell(img, cx, yy, r, r, GOLD, INK, 1.4)
    ell(img, cx, tip - 40, 14, 14, GOLD, INK, 1.6)              # the crescent, opening up
    ell(img, cx, tip - 48, 11, 11, SKY, None)


def onion(cx, base, w, h):
    pts = []
    for s in np.linspace(0, 1, 26):
        hw = w / 2 * (math.sin(math.pi * min(1.0, s * 1.45)) ** 0.8 * (1 - s) ** 0.5 + 0.12 * (1 - s))
        pts.append((hw, base - s * h))
    return [(cx - a, y) for a, y in pts] + [(cx + a, y) for a, y in pts[::-1]]


def spire(img, cx, kind):
    """A St Basil's tower: a red brick body with white trim and a row of small arches, a drum, a striped onion dome,
    a small gold onion and a spike on top."""
    rect(img, cx - 38, 700, cx + 38, 880, BRICK)
    for x in (cx - 13, cx + 13):
        pen(img).line([(x, 702), (x, 878)], BRICK_D, 2)
    for y in (735, 800):
        rect(img, cx - 40, y, cx + 40, y + 7, WHITE, INK, 1.4)
    for k in range(3):                                          # kokoshnik arches at the top of the body
        x = cx - 25 + k * 25
        poly(img, [(x - 11, 712), (x - 11, 698), (x, 684), (x + 11, 698), (x + 11, 712)], WHITE, INK, 1.4, amt=0.5)
    rect(img, cx - 28, 640, cx + 28, 700, BRICK)
    for k in range(4):
        x = cx - 19 + k * 12.7
        poly(img, [(x - 4, 690), (x - 4, 664), (x + 4, 664), (x + 4, 690)], (62, 46, 40), INK, 1.0, amt=0.4)
    shape = onion(cx, 646, 112, 128)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    cols = ((60, 104, 196), (240, 242, 236)) if kind == 'blue' else ((30, 140, 74), (238, 190, 58), (30, 140, 74),
                                                                       (204, 46, 40))
    for k in range(-8, 9):                                      # twisted stripes, masked by the onion
        y0, y1 = 520, 650
        x0 = cx + k * 16
        ld.polygon([(x0, y1), (x0 + 16, y1), (x0 + 16 + 70, y0), (x0 + 70, y0)], fill=cols[k % len(cols)] + (255,))
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).polygon(shape, fill=255)
    img.paste(lay, (0, 0), Image.fromarray(np.minimum(np.asarray(mask), np.asarray(lay)[..., 3])))
    pen(img).poly(shape, None, INK, 2.4)
    top = 646 - 128
    small = onion(cx, top + 4, 26, 30)
    pen(img).poly(small, GOLD, INK, 1.6)
    pen(img).line([(cx, top - 24), (cx, top - 58)], GOLD_D, 3)
    ell(img, cx, top - 40, 4, 4, GOLD, INK, 1.0)


# ---------------------------------------------------------------------------------------------- building
WIN_X = (205, 270, 330, 395, 720, 783, 845, 908)                # Sam's photo: four each side of the porch
COLS_X = (432, 516, 600, 684)


def window(img, x, y0, y1, head=None):
    w = 13 * 1.18
    rect(img, x - w - 3, y0 - 3, x + w + 3, y1 + 3, SHADE, INK, 1.6)
    rect(img, x - w, y0, x + w, y1, GLASS, INK, 1.6)
    d = pen(img)
    d.line([(x, y0), (x, y1)], WHITE, 2)
    for f in (0.33, 0.66):
        d.line([(x - w, y0 + (y1 - y0) * f), (x + w, y0 + (y1 - y0) * f)], WHITE, 2)
    if head == 'tri':
        poly(img, [(x - w - 7, y0 - 6), (x + w + 7, y0 - 6), (x, y0 - 22)], WHITE, INK, 1.6, amt=0.4)
    elif head == 'arc':
        pts = [(x + (w + 7) * math.cos(a), y0 - 6 - 14 * math.sin(a)) for a in np.linspace(0, math.pi, 12)]
        poly(img, pts, WHITE, INK, 1.6, amt=0)
    else:
        rect(img, x - w - 6, y0 - 9, x + w + 6, y0 - 4, WHITE, INK, 1.4)


def building(img):
    L, R = fx(165), fx(951)
    top, base = fy(175), 1092
    rect(img, L, top, R, base, WHITE)
    for cx in (fx(380), fx(735)):                               # chimneys
        rect(img, cx - 12, fy(118), cx + 12, fy(150), WHITE)
        rect(img, cx - 15, fy(118) - 6, cx + 15, fy(118), SHADE, INK, 1.4)
    rect(img, L - 4, fy(150), R + 4, fy(160), WHITE)            # the balustrade: rail, balusters, piers, plinth
    rect(img, L - 2, fy(160), R + 2, top - 2, WHITE)
    d = pen(img)
    x = L + 6
    while x < R - 4:
        d.line([(x, fy(161)), (x, top - 4)], SHADE, 2.2)
        x += 7
    for px in np.linspace(L, R, 13):
        rect(img, px - 6, fy(160), px + 6, top - 2, WHITE, INK, 1.4)
    rect(img, L - 6, top - 3, R + 6, top + 7, WHITE)            # cornice
    d.line([(L, fy(278)), (R, fy(278))], SHADE, 3)              # string course between the floors
    rect(img, fx(410), top, fx(706), base, RECESS)              # the porch's shadowed back wall
    for i, x in enumerate(WIN_X):
        window(img, fx(x), fy(222), fy(262))
        window(img, fx(x), fy(300), fy(342), 'tri' if i % 2 == 0 else 'arc')
    for x in (485, 632):
        window(img, fx(x), fy(222), fy(262))
        window(img, fx(x), fy(300), fy(342), 'arc')
    dx, w = fx(558), 22                                         # the door with its fanlight
    rect(img, dx - w - 6, fy(292), dx + w + 6, base, SHADE, INK, 1.6)
    rect(img, dx - w, fy(305), dx + w, base, (92, 70, 52), INK, 1.6)
    pen(img).line([(dx, fy(305)), (dx, base)], INK, 1.4)
    pts = [(dx + w * math.cos(a), fy(305) - 18 * math.sin(a)) for a in np.linspace(0, math.pi, 12)]
    poly(img, pts, (232, 214, 150), INK, 1.4, amt=0)
    d.line([(dx, fy(180)), (dx, fy(262))], INK, 1.6)            # the lantern on its chain
    poly(img, [(dx - 9, fy(262)), (dx + 9, fy(262)), (dx + 12, fy(290)), (dx, fy(298)), (dx - 12, fy(290))],
         (244, 220, 150), INK, 1.6, amt=0.5)
    rect(img, fx(405), base - 10, fx(711), base, SHADE, INK, 1.4)   # the porch floor's edge
    for x in COLS_X:                                            # four Ionic columns
        cx = fx(x)
        rect(img, cx - 13, fy(186), cx + 13, base - 10, WHITE, INK, 2.0)
        d.line([(cx + 6, fy(188)), (cx + 6, base - 12)], SHADE, 4)
        rect(img, cx - 19, fy(180), cx + 19, fy(188), WHITE, INK, 1.6)
        for sg in (-1, 1):
            ell(img, cx + sg * 17, fy(186), 5, 5, WHITE, INK, 1.4)
        rect(img, cx - 17, base - 16, cx + 17, base - 8, WHITE, INK, 1.4)
    rect(img, fx(410), fy(150), fx(706), fy(180), WHITE)         # entablature
    d.line([(fx(410), fy(166)), (fx(706), fy(166))], SHADE, 2)
    apex = (fx(558), fy(86))
    poly(img, [(fx(402), fy(152)), (fx(714), fy(152)), apex], WHITE, INK, 2.6, amt=0.8)   # pediment
    poly(img, [(fx(424), fy(146)), (fx(692), fy(146)), (apex[0], apex[1] + 13)], (236, 236, 228), INK, 1.4, amt=0.5)
    ell(img, apex[0], fy(126), 15, 9, WHITE, INK, 1.4)          # the oval in the tympanum
    return apex


# ---------------------------------------------------------------------------------------------- flag
def hammer_sickle(cx, cy, r):
    """Shapes in a cell of radius r (y down), as on Sam's reference 77252a6f: the sickle's handle lower left, its
    blade sweeping round the bottom and right and over the top to a point; the hammer's head upper left, its handle
    running down to the lower right."""
    out = []
    ox, oy, R = cx + 0.04 * r, cy - 0.02 * r, 0.6 * r
    outer, inner = [], []
    for s in np.linspace(0, 1, 22):
        th = math.radians(120 - s * 255)
        w = 0.19 * r * (1 - s) ** 0.75
        outer.append((ox + R * math.cos(th), oy + R * math.sin(th)))
        inner.append((ox + (R - w) * math.cos(th), oy + (R - w) * math.sin(th)))
    out.append(outer + inner[::-1])
    hx, hy = outer[0]                                           # the sickle's handle, down to the lower left
    ux, uy, w = -0.6, 0.8, 0.075 * r
    out.append([(hx - uy * w, hy + ux * w), (hx + uy * w, hy - ux * w), (hx + uy * w + ux * 0.34 * r, hy - ux * w + uy * 0.34 * r),
                (hx - uy * w + ux * 0.34 * r, hy + ux * w + uy * 0.34 * r)])
    a0, a1 = (cx + 0.5 * r, cy + 0.55 * r), (cx - 0.22 * r, cy - 0.2 * r)    # the hammer's handle
    dx, dy = a1[0] - a0[0], a1[1] - a0[1]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    hw = 0.065 * r
    out.append([(a0[0] + px * hw, a0[1] + py * hw), (a1[0] + px * hw, a1[1] + py * hw),
                (a1[0] - px * hw, a1[1] - py * hw), (a0[0] - px * hw, a0[1] - py * hw)])
    hc, hl, hh = (a1[0] + ux * 0.06 * r, a1[1] + uy * 0.06 * r), 0.3 * r, 0.11 * r   # the head, across the end
    out.append([(hc[0] - px * hl - ux * hh, hc[1] - py * hl - uy * hh), (hc[0] + px * hl - ux * hh, hc[1] + py * hl - uy * hh),
                (hc[0] + px * hl + ux * hh, hc[1] + py * hl + uy * hh), (hc[0] - px * hl + ux * hh, hc[1] - py * hl + uy * hh)])
    return out


def crescent(cx, cy, r):
    """A crescent opening to the right (Sam's reference 9b28a4a2), as one shape: no cut-out disc."""
    a, b, d = 0.58 * r, 0.47 * r, 0.24 * r
    x = (a * a - b * b + d * d) / (2 * d)
    f0 = math.acos(max(-1.0, min(1.0, x / a)))
    outer = [(a * math.cos(f), a * math.sin(f)) for f in np.linspace(f0, 2 * math.pi - f0, 30)]
    ps = math.atan2(outer[0][1], outer[0][0] - d)
    pe = math.atan2(outer[-1][1], outer[-1][0] - d) % (2 * math.pi)
    inner = [(d + b * math.cos(f), b * math.sin(f)) for f in np.linspace(pe, ps, 24)]
    return [(cx + px, cy + py) for px, py in outer + inner]


def star(cx, cy, r, rot=-90):
    return [(cx + (r if k % 2 == 0 else r * 0.42) * math.cos(math.radians(rot + k * 36)),
             cy + (r if k % 2 == 0 else r * 0.42) * math.sin(math.radians(rot + k * 36))) for k in range(10)]


def flag(img, pole_x, top, w, h, t, phase=0.0, amp=None):
    """The flag on its pole, flying RIGHT (wind from the left; Sam turned it round, 4 Nov), waving: 13 red and green stripes, a navy canton at the
    pole with two rows of three emblems, gold hammers and sickles and white crescents with stars in turn."""
    amp = h * 0.11 if amp is None else amp
    om = 2 * math.pi * 1.1

    def F(u, v):                                               # u: 0 at the pole .. 1 at the fly end; v: 0 top
        ph = om * t + phase - 2.6 * math.pi * u
        dy = amp * u * math.sin(ph)
        dx = w * u * (0.97 - 0.03 * math.cos(ph))
        return pole_x + dx, top + v * h + dy + u * h * 0.06     # the fly end droops a little

    def slope(u):
        ph = om * t + phase - 2.6 * math.pi * u
        return math.cos(ph)

    N = 18
    us = np.linspace(0, 1, N + 1)
    d = pen(img)
    for i in range(N):
        u0, u1 = us[i], us[i + 1]
        dim = 0.86 if slope((u0 + u1) / 2) < -0.2 else 1.0     # the folds turned away, flat and a little darker
        for j in range(13):
            v0, v1 = j / 13, (j + 1) / 13
            col = F_RED if j % 2 == 0 else F_GREEN
            if v1 <= 7 / 13 + 1e-6 and u1 <= 0.4 + 1e-6:
                col = F_NAVY
            col = tuple(int(c * dim) for c in col)
            d.poly([F(u0, v0), F(u1, v0), F(u1, v1), F(u0, v1)], col, None)
    cw, ch = 0.4, 7 / 13                                       # the canton's emblems, mapped through the wave
    for r_ in range(2):
        for c_ in range(3):
            cu, cv = cw * (c_ + 0.5) / 3, ch * (r_ + 0.5) / 2
            rr = min(cw * w / 3, ch * h / 2) * 0.42
            ku, kv = 1 / w, 1 / h
            if (r_ + c_) % 2 == 0:
                for shp in hammer_sickle(0, 0, rr):
                    d.poly([F(cu + x * ku, cv + y * kv) for x, y in shp], GOLD, None)
            else:
                d.poly([F(cu + x * ku, cv + y * kv) for x, y in crescent(-rr * 0.1, 0, rr * 1.1)], (240, 240, 232), None)
                d.poly([F(cu + x * ku, cv + y * kv) for x, y in star(rr * 0.22, 0, rr * 0.26)], (240, 240, 232), None)
    edge = [F(u, 0) for u in us] + [F(1, v) for v in np.linspace(0, 1, 6)] + [F(u, 1) for u in us[::-1]]
    d.poly(edge, None, INK, 2.2)


def pole(img, x, top, base, thick=5):
    pen(img).line([(x, base), (x, top)], (200, 200, 204), thick + 2)
    pen(img).line([(x - thick / 2 - 1, base), (x - thick / 2 - 1, top)], INK, 1.2)
    pen(img).line([(x + thick / 2 + 1, base), (x + thick / 2 + 1, top)], INK, 1.2)
    ell(img, x, top - thick, thick + 2, thick + 2, GOLD, INK, 1.4)


# ---------------------------------------------------------------------------------------------- trees, lawn, fountain
def far_trees(img):
    for cx, cy, r, sd in ((70, 980, 130, 21), (1010, 980, 130, 22), (40, 1060, 110, 23), (1050, 1060, 110, 24)):
        poly(img, blob(cx, cy, r, sd), TREE_D, INK, 2.4, amt=0)


def side_trees(img):
    for sg, x0 in ((-1, 0), (1, 1080)):
        tx = x0 - sg * 30
        rect(img, tx - 16, 920, tx + 16, 1100, (104, 78, 56), INK, 2.0)
        for k, (dx, dy, r, c) in enumerate(((0, 760, 125, TREE_D), (-sg * 25, 880, 125, TREE), (sg * 30, 650, 105, TREE),
                                            (-sg * 50, 990, 95, TREE_F))):
            poly(img, blob(tx + dx, dy, r, 30 + k + (5 if sg > 0 else 0)), c, INK, 2.6, amt=0)


def hedges(img):
    for k, x in enumerate(np.arange(fx(150), fx(965), 34)):
        poly(img, blob(x, 1084, 26, 50 + k, n=16, lump=0.1, squash=0.95), HEDGE if k % 2 else dk(HEDGE, 0.9),
             INK, 2.0, amt=0)


def dk(c, k):
    return tuple(int(v * k) for v in c)


def lawn(img):
    d = pen(img)
    d.d.rectangle([0, 1092, img.width, img.height], fill=LAWN)
    for k in range(-6, 8):                                     # mowing stripes running away from us
        x0 = 540 + k * 150
        if k % 2:
            d.poly([(540 + k * 40, 1100), (540 + (k + 1) * 40, 1100), (x0 + 150 * 1.0 + 150, 1920), (x0 + 150, 1920)],
                   LAWN_2, None)


RING = (540, 1236)
SHIFT = 90                                                      # the painting's drop in the frame (see paint)


def flower_ring(img):
    cx, cy = RING
    ell(img, cx, cy, 440, 84, FLOWER, INK, 2.4)
    rng = np.random.default_rng(7)
    d = pen(img).d
    for _ in range(420):                                       # flower dots, flat
        a = rng.uniform(0, 2 * math.pi)
        f = rng.uniform(0.9, 1.0)
        x, y = cx + 432 * f * math.cos(a), cy + 78 * f * math.sin(a)
        if (x - cx) ** 2 / 400 ** 2 + (y - cy) ** 2 / 64 ** 2 > 1.0:
            d.ellipse([x - 3, y - 2, x + 3, y + 2], fill=FLOWER_D if rng.random() < 0.5 else (240, 70, 60))
    ell(img, cx, cy, 398, 64, (238, 236, 228), INK, 1.8)        # the white edging
    ell(img, cx, cy, 384, 58, LAWN, INK, 1.4)
    ell(img, cx, cy + 4, 78, 16, (226, 226, 218), INK, 1.8)     # the basin
    ell(img, cx, cy + 2, 66, 11, POOL, INK, 1.2)


def fountain(img, t):
    cx, cy = RING
    top = 1040 + 8 * math.sin(t * 5.3)
    pts = []
    for s in np.linspace(0, 1, 14):                            # the jet: a lumpy white column, wider at the foot
        y = cy - (cy - top) * s
        w = 9 - 5 * s + 1.4 * math.sin(t * 17 + s * 9)
        pts.append((cx - w, y))
    for s in np.linspace(1, 0, 14):
        y = cy - (cy - top) * s
        w = 9 - 5 * s + 1.4 * math.sin(t * 13 + s * 11 + 1)
        pts.append((cx + w, y))
    poly(img, pts, WATER, INK, 1.6, amt=0)
    for sg in (-1, 1):                                         # spray falling back, short arcs
        for k in range(3):
            ph = (t * 1.7 + k / 3) % 1.0
            arc = [(cx + sg * (8 + 30 * q), top + 30 + 70 * q * q + ph * 20) for q in np.linspace(0, 1, 6)]
            pen(img).line(arc, WATER, 2.4)
    ell(img, cx, cy + 1, 30, 6, WATER, None)


# ---------------------------------------------------------------------------------------------- families
KIDS = [(232, 90, 70), (250, 200, 70), (90, 160, 220), (240, 150, 190), (120, 200, 120), (250, 140, 60)]
SKINS = [(236, 196, 166), (200, 150, 110), (140, 96, 66), (224, 176, 140), (96, 66, 48)]
HAIRS = [(40, 30, 26), (110, 70, 40), (210, 170, 90), (20, 18, 18), (150, 60, 40)]


def tiny(img, x, y, h, shirt, legs, skin, hair, arms=(0.3, 0.3), stride=0.0, sit=False, scarf=None):
    """A small far-off person standing (or sitting) with feet at (x, y), `h` pixels tall: flat shapes, one outline,
    circle hands. arms: each arm's angle from hanging (0) to straight up (1), left then right. stride: legs apart
    (-1..1). scarf: a headscarf colour (some of the mothers)."""
    p = pen(img)
    hr = h * 0.11
    hip = y - h * 0.46 if not sit else y - h * 0.08
    neck = hip - h * 0.32
    hy = neck - hr * 0.95
    lw = max(1.2, h * 0.075)
    if not sit:
        for sg in (-1, 1):
            fxp = x + sg * (h * 0.06 + stride * h * 0.14)
            p.line([(x + sg * h * 0.05, hip), (fxp, y)], INK, lw + 2.2)
            p.line([(x + sg * h * 0.05, hip), (fxp, y)], legs, lw)
    else:
        for sg in (-1, 1):
            p.line([(x + sg * h * 0.05, hip), (x + sg * h * 0.22, hip + h * 0.02)], INK, lw + 2.2)
            p.line([(x + sg * h * 0.05, hip), (x + sg * h * 0.22, hip + h * 0.02)], legs, lw)
    sw = h * 0.11
    for sg, a in zip((-1, 1), arms):                           # arms swung out round the shoulder
        ang = math.radians(-90 + sg * (20 + a * 150))
        sx, sy = x + sg * sw * 0.8, neck + h * 0.04
        ex, ey = sx + math.cos(ang) * h * 0.3, sy - math.sin(ang) * h * 0.3
        p.line([(sx, sy), (ex, ey)], INK, lw + 2.2)
        p.line([(sx, sy), (ex, ey)], shirt, lw)
        p.ell(ex, ey, h * 0.04, h * 0.04, skin, INK, 1.0)
    p.poly([(x - sw * 0.7, neck), (x + sw * 0.7, neck), (x + sw, hip + h * 0.02), (x - sw, hip + h * 0.02)], shirt, INK, 1.2)
    if scarf:
        p.ell(x, hy + hr * 0.15, hr * 1.25, hr * 1.3, scarf, INK, 1.2)
    else:
        p.ell(x, hy - hr * 0.2, hr * 1.02, hr * 0.85, hair, INK, 1.0)
    p.ell(x, hy, hr, hr, skin, INK, 1.2)
    if h > 50:                                                  # a laughing face: dot eyes, open smile
        for sg in (-1, 1):
            p.d.ellipse([x + sg * hr * 0.38 - 1.2, hy - hr * 0.2 - 1.2, x + sg * hr * 0.38 + 1.2, hy - hr * 0.2 + 1.2], fill=INK)
        p.d.chord([x - hr * 0.42, hy - hr * 0.1, x + hr * 0.42, hy + hr * 0.6], 0, 180, fill=(120, 40, 40))
    if not scarf:
        p.ell(x, hy - hr * 0.7, hr * 0.85, hr * 0.38, hair, None)


def families(img, t):
    """Background only, small simple loops: a picnic, children throwing a ball, a running child, a father with a
    child on his shoulders, a couple strolling, a child jumping."""
    # far left by the bushes: a father with a child on his shoulders, bobbing as he walks
    s = ppm(1150)
    bob = abs(math.sin(t * 4)) * 2
    x = 150 + 14 * math.sin(t * 0.6)
    tiny(img, x, 1150 - bob, 1.8 * s, (60, 90, 150), (50, 50, 60), SKINS[1], HAIRS[3], arms=(0.75, 0.75), stride=0.3 * math.sin(t * 4))
    tiny(img, x, 1150 - bob - 1.8 * s * 0.66, 0.9 * s, KIDS[1], (60, 60, 140), SKINS[1], HAIRS[3], arms=(0.8, 0.9))
    # far right: a couple strolling, one waving
    s = ppm(1150)
    for k, (dx, col, sc, sk) in enumerate(((0, (150, 60, 90), (40, 120, 90), SKINS[2]), (24, (230, 230, 220), None, SKINS[0]))):
        tiny(img, 830 + dx - 10 * math.sin(t * 0.5), 1152, 1.7 * s, col, (60, 60, 70), sk, HAIRS[k],
             arms=(0.1, 0.1 + (0.7 + 0.15 * math.sin(t * 9)) * k), stride=0.25 * math.sin(t * 3.2 + k), scarf=sc)
    # the picnic: a blanket, a mother and a grandfather sitting, a toddler bouncing
    s = ppm(1420)
    ell(img, 800, 1428, 92, 20, (230, 70, 60), INK, 1.8)
    for k in range(5):
        pen(img).line([(724 + k * 34, 1414), (742 + k * 34, 1442)], (246, 236, 220), 3)
    tiny(img, 760, 1420, 1.65 * s, (70, 130, 90), (60, 60, 70), SKINS[2], HAIRS[0], arms=(0.15, 0.55 + 0.35 * math.sin(t * 7)),
         sit=True, scarf=(200, 160, 60))
    tiny(img, 850, 1420, 1.75 * s, (170, 150, 120), (80, 70, 60), SKINS[3], (200, 200, 196), arms=(0.1, 0.2), sit=True)
    hop = abs(math.sin(t * 5.5)) * 14
    tiny(img, 805, 1440 - hop, 0.9 * s, KIDS[3], (90, 90, 160), SKINS[2], HAIRS[0], arms=(0.9, 0.9))
    # a child running back and forth across the right lawn
    s = ppm(1560)
    run = math.sin(t * 0.9)
    tiny(img, 820 + 90 * run, 1560 - abs(math.sin(t * 7)) * 5, 1.1 * s, KIDS[0], (50, 60, 120), SKINS[4], HAIRS[3],
         arms=(0.2 + 0.18 * math.sin(t * 7), 0.2 - 0.18 * math.sin(t * 7)), stride=math.sin(t * 7))
    # two children throwing a ball, lower left, under the heading
    s = ppm(1620)
    xa, xb, y = 170, 470, 1620
    per = 1.6
    q = (t % per) / per
    fwd = int(t // per) % 2 == 0
    bx = xa + (xb - xa) * (q if fwd else 1 - q)
    hk = 1.2 * s * 0.9
    by = y - hk - 110 * 4 * q * (1 - q)
    catch_a = (not fwd and q > 0.8) or (fwd and q < 0.2)
    catch_b = (fwd and q > 0.8) or (not fwd and q < 0.2)
    tiny(img, xa, y, 1.2 * s, KIDS[2], (60, 60, 80), SKINS[0], HAIRS[2], arms=(0.75 if catch_a else 0.1, 0.85 if catch_a else 0.2))
    tiny(img, xb, y, 1.15 * s, KIDS[4], (70, 50, 50), SKINS[3], HAIRS[4], arms=(0.85 if catch_b else 0.2, 0.75 if catch_b else 0.1))
    ell(img, bx, by, 10, 10, (250, 250, 246), INK, 1.6)
    pen(img).line([(bx - 9, by), (bx + 9, by)], (220, 50, 50), 2)
    # a child jumping for joy by the flower bed, right
    s = ppm(1330)
    jump = max(0.0, math.sin(t * 4.2)) * 26
    tiny(img, 650, 1330 - jump, 1.0 * s, KIDS[5], (60, 60, 120), SKINS[1], HAIRS[1], arms=(0.9, 0.9) if jump > 4 else (0.15, 0.15),
         stride=0.3 if jump > 4 else 0.0)


# ---------------------------------------------------------------------------------------------- paint
def paint(t, img=None):
    """The whole front at time t (seconds into shot 1), on a 1080 x 1920 frame."""
    B.SS = 1
    img = img or Image.new('RGBA', (1080, 1920), (0, 0, 0, 255))
    sky(img)
    for ln in LANES:
        if ln['behind']:
            lane(img, ln, t)
    far_trees(img)
    dome(img)
    spire(img, 300, 'blue')
    spire(img, 780, 'green')
    apex = building(img)
    side_trees(img)
    pole(img, apex[0], 640, apex[1] + 4, 4)                    # the roof flag above the entrance
    flag(img, apex[0], 646, 150, 86, t)
    hedges(img)
    lawn(img)
    flower_ring(img)
    fountain(img, t)
    families(img, t)
    pole(img, 680, 880, 1385, 7)                                # the flag on the lawn, flying right
    flag(img, 680, 888, 270, 156, t, phase=1.3)
    low = Image.new('RGBA', img.size, SKY + (255,))             # everything above moved down SHIFT px (the two-row
    low.paste(img.crop((0, 0, img.width, img.height - SHIFT)), (0, SHIFT))   # Hook Text clears the dome); the near
    img.paste(low)                                              # car lanes stay where they are
    for ln in LANES:
        if not ln['behind']:
            lane(img, ln, t)
    return img


def picture(t=0.6):
    """One frame: the kit catalogue's tile."""
    return paint(float(t))


# ---------------------------------------------------------------------------------------------- sheets
def heading(img, t_in=99.0):
    """The opening heading as the brief has it, lower-middle-left: 'USA', then a second later the line beneath."""
    d = ImageDraw.Draw(img)
    f1 = ImageFont.truetype(os.path.join(HERE, 'fonts', 'Anton-Regular.ttf'), 120)
    f2 = ImageFont.truetype(os.path.join(HERE, 'fonts', 'Anton-Regular.ttf'), 52)
    top = 1270
    box = d.textbbox((70, top), 'USA', font=f1, stroke_width=5)
    d.text((70, top - (box[1] - top)), 'USA', font=f1, fill=(255, 255, 255), stroke_width=5, stroke_fill=INK)
    y = box[3] - box[1] + top + 12
    if t_in >= 1.0:
        for row in ('THREE YEARS INTO', 'ISLAMIC COMMUNISM'):
            b = d.textbbox((74, y), row, font=f2, stroke_width=3)
            d.text((74, y - (b[1] - y)), row, font=f2, fill=(255, 255, 255), stroke_width=3, stroke_fill=INK)
            y += b[3] - b[1] + 8
    return y


HOOK = ('MAGAs Worst Nightmare', 410, None)  # Sam's words (4 Nov); two rows in the sky above the dome: finish.py --y 410


def hook(img, text=HOOK[0], y=HOOK[1]):
    import tempfile
    import hook_text as HT
    path = os.path.join(tempfile.mkdtemp(), 'hook.png')
    HT.card(1080, 1920, text, y, path, width=HOOK[2])
    img.alpha_composite(Image.open(path).convert('RGBA'))
    return img


def test(out):
    tiles = [(f't = {t:.1f} s', paint(t)) for t in (0.0, 0.7, 1.5)]
    sheet = Image.new('RGB', (3 * 360 + 4 * 12, 640 + 50), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 20)
    for i, (label, img) in enumerate(tiles):
        sheet.paste(img.convert('RGB').resize((360, 640), Image.LANCZOS), (12 + i * 372, 40))
        d.text((12 + i * 372, 10), label, font=f, fill=(30, 30, 30))
    sheet.save(out, quality=88)
    return out


BENCHMARK = [   # rule 3: what makes the place, and how ours has it
    ('white front, four Ionic columns under a pediment', 'yes: fluted-shade columns, scroll capitals, plain pediment with its oval'),
    ('porch: door with fanlight, hanging lantern', 'yes'),
    ('four windows each side, two floors', 'yes (my notes said three: Sam\'s photo shows four)'),
    ('lower windows: triangular and curved heads in turn', 'yes'),
    ('balustrade on the roof, two chimneys', 'yes'),
    ('round fountain, tall jet, red flower ring edged white', 'yes; the jet plays'),
    ('round bushes along the front; big trees both ends', 'yes'),
    ('flag on the roof above the entrance', 'yes: our flag, on the pediment'),
    ('gold dome on a blue-tiled drum (Dome of the Rock)', 'yes: crescent on top'),
    ('two onion spires (St Basil\'s)', 'yes: blue/white and green/gold/red; gold tips, no crosses'),
]


def refsheet(out):
    """Rule 3 by hand: Sam's photos beside ours, and the list ticked."""
    H = 420
    ours = paint(0.6).convert('RGB').crop((0, 380, 1080, 1460))

    def fit(im, h=H):
        return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    top = [fit(Image.open(os.path.join(REFS, r + '-image.jpg')).convert('RGB'), 300)
           for r in ('89a1ee64', '49db6798', 'f176063d', '2ab87cb9', '77252a6f', '9b28a4a2')]
    W = 1080
    sheet = Image.new('RGB', (W, 2000), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 22)
    fs = ImageFont.truetype(FONT, 15)
    d.text((16, 10), "Sam's references", font=f, fill=(30, 30, 30))
    x, y = 16, 44
    for im in top:
        im = fit(im, 150)
        if x + im.width > W - 16:
            x, y = 16, y + 160
        sheet.paste(im, (x, y))
        x += im.width + 10
    y += 175
    d.text((16, y), 'Ours (shot 1, cropped)', font=f, fill=(30, 30, 30))
    o = fit(ours, 470)
    sheet.paste(o, (16, y + 34))
    yy = y + 34
    for what, how in BENCHMARK:
        d.text((o.width + 32, yy), '✓ ' + what, font=fs, fill=(20, 90, 40))
        d.text((o.width + 52, yy + 20), how, font=fs, fill=(70, 70, 70))
        yy += 54
    sheet = sheet.crop((0, 0, W, max(y + 34 + 470, yy) + 16))
    sheet.save(out, quality=88)
    return out


COMP = [   # the key shots (rule 11): label, camera (pos, look, focal) or 'ext', who's where
    ('1  Outside, locked: cars stream, families play, both flags fly. "USA", then the line beneath', 'ext', None),
    ('2  Oval Office wide: Abdul at the desk on the phone (sceptical); Alex comes in by the door with two mimosas',
     ((-0.9, 1.6, -0.4), (1.5, 1.45, 2.7), 640), 'door'),
    ('3  Across the desk: she hands him a glass; the sips and the dialogue run', ((-0.15, 1.5, -0.25), (0.2, 1.35, 3.0), 980),
     'desk'),
    ('4  Closer, side on across the desk: "Invade Europe?" / "Invade Europe."  Clink', ((2.6, 1.55, 2.85), (-1.0, 1.42, 2.85), 1150),
     'clink'),
]


def comp(out):
    """The composition sheet: the four key shots, still (people in their places, no moves yet)."""
    import midterminal_set as MS
    import islamocommunism_cast as IC
    import views as V
    tiles = []
    for label, camdef, who in COMP:
        if camdef == 'ext':
            img = hook(paint(2.2))
            heading(img)
        else:
            B.SS = 1
            pos, look, focal = camdef
            cm = S.Cam(pos, look, focal=focal)
            ppl = []
            ex, ez = MS.DESK_CHAIR
            if who == 'door':
                dx, _, dz = MS.wp(70.0, 0, 0.45)
                ppl.append((ex, ez - 0.3, lambda im, c: MS.put_seated(im, c, dict(IC.ELSAYED, mood='sceptic', look=0.5), ex,
                                                                      ez - 0.05, MS.to_cam(c, ex, ez))))
                ppl.append((dx, dz, lambda im, c: MS.put(im, c, dict(IC.AOC, mood='smile', look=-0.8), dx, dz,
                                                         MS.to_cam(c, dx, dz))))
            else:
                ax, az = (0.55, 2.15) if who == 'desk' else (-0.3, 2.35)
                bx, bz = (-0.05, 3.55) if who == 'desk' else (0.0, 3.5)
                far = -1.2 if who == 'clink' else 0.0             # side on, the desk's near end hides their legs:
                ppl.append((bx + far, bz, lambda im, c: MS.put(im, c, dict(IC.ELSAYED, mood='smile', look=0.7), bx, bz,
                                                               MS.to_cam(c, bx, bz))))    # drawn before the desk
                ppl.append((ax + far, az, lambda im, c: MS.put(im, c, dict(IC.AOC, mood='hopeful' if who == 'clink' else 'smile',
                                                                     look=-0.7), ax, az, MS.to_cam(c, ax, az))))
            img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 255))
            MS.render(img, cm, ppl)
        tiles.append((label, img))
    tw, th = 400, 711
    sheet = Image.new('RGB', (4 * tw + 5 * 16, th + 150), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 17)
    for i, (label, img) in enumerate(tiles):
        x = 16 + i * (tw + 16)
        sheet.paste(img.convert('RGB').resize((tw, th), Image.LANCZOS), (x, 130))
        words, rows, row = label.split(), [], ''
        for wd in words:
            if d.textlength(row + ' ' + wd, font=f) > tw and row:
                rows.append(row)
                row = wd
            else:
                row = (row + ' ' + wd).strip()
        rows.append(row)
        d.multiline_text((x, 10), '\n'.join(rows[:5]), font=f, fill=(30, 30, 30))
    sheet.save(out, quality=88)
    return out


if __name__ == '__main__':
    cmd, out = sys.argv[1], sys.argv[2]
    print({'test': test, 'refs': refsheet, 'comp': comp}[cmd](out))
