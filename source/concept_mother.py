#!/usr/bin/env python3
"""Concept still: the mother at her kitchen island at Christmas, in a Waltz With Bashir-like style
(flat, realistic shapes with bold black outlines, hard shadow shapes, a warm/cold lighting split).

Usage:
    python3 concept_mother.py OUT.png
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H, S = 1920, 1080, 2
INK = (22, 16, 14)
img = Image.new('RGB', (W * S, H * S), (60, 30, 25))
d = ImageDraw.Draw(img)
rng = np.random.default_rng(3)


def spline(pts, closed=True, n=10):
    """Catmull-Rom: smooth, organic curves through the given points."""
    p = np.array(pts, float)
    if closed:
        p = np.vstack([p[-1], p, p[0], p[1]])
    else:
        p = np.vstack([p[0], p, p[-1]])
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed:
        out.append(p[-2])
    return [tuple(q) for q in out]


def sc(pts):
    return [(x * S, y * S) for x, y in pts]


def shape(pts, fill, line=3.0, smooth=True, col=INK):
    q = spline(pts) if smooth else list(pts)
    if fill is not None:
        d.polygon(sc(q), fill=fill)
    if line:
        d.line(sc(q + [q[0]]), fill=col, width=max(1, int(line * S)), joint='curve')


def stroke(pts, w=3.0, col=INK, smooth=True):
    q = spline(pts, closed=False) if smooth else list(pts)
    d.line(sc(q), fill=col, width=max(1, int(w * S)), joint='curve')


def rect(x0, y0, x1, y1, fill, line=2.0):
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill, outline=INK if line else None,
                width=int(line * S) if line else 0)


def ellipse(cx, cy, rx, ry, fill, line=2.0):
    d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], fill=fill,
              outline=INK if line else None, width=int(line * S) if line else 0)


# ---------------------------------------------------------------------------
# The kitchen
# ---------------------------------------------------------------------------
WALL, WALL_D = (128, 40, 34), (98, 28, 26)
CAB, CAB_D, CAB_L = (226, 214, 190), (186, 170, 144), (240, 232, 214)
TILE, TILE_D = (46, 86, 66), (34, 64, 50)
BRASS = (196, 150, 72)

rect(0, 0, W, H, WALL, 0)
for x in range(0, W, 48):  # a quiet striped wallpaper
    rect(x, 0, x + 18, 600, WALL_D, 0)
rect(0, 0, W, 38, CAB_L, 2)  # cornice
rect(0, 38, W, 46, CAB_D, 2)
# green tiled splashback
rect(0, 372, W, 610, TILE, 2)
for y in range(372, 610, 30):
    stroke([(0, y), (W, y)], 1.2, TILE_D, smooth=False)
    off = 0 if (y // 30) % 2 else 30
    for x in range(off, W, 60):
        stroke([(x, y), (x, y + 30)], 1.2, TILE_D, smooth=False)


def cabinet(x0, x1, y0, y1, doors):
    rect(x0, y0, x1, y1, CAB, 2.5)
    w = (x1 - x0) / doors
    for i in range(doors):
        a = x0 + i * w
        rect(a + 10, y0 + 12, a + w - 10, y1 - 12, CAB, 2)
        rect(a + 24, y0 + 28, a + w - 24, y1 - 28, CAB_D, 1.5)  # recessed shaker panel
        rect(a + 24, y0 + 28, a + w - 24, y0 + 36, CAB_L, 0)
        ellipse(a + (w - 22 if i % 2 == 0 else 22), y1 - 50, 5, 5, BRASS, 1.5)


cabinet(0, 560, 46, 372, 3)
cabinet(1500, W, 46, 372, 2)

# the window: dusk outside, snow on the houses across the street
WX0, WX1, WY0, WY1 = 990, 1450, 110, 560
sky = np.linspace(0, 1, (WY1 - WY0) * S)[:, None]
top, bot = np.array([30, 40, 72]), np.array([88, 104, 140])
grad = (top * (1 - sky) + bot * sky).astype(np.uint8)
grad = np.repeat(grad[:, None, :], (WX1 - WX0) * S, axis=1)
img.paste(Image.fromarray(grad.reshape((WY1 - WY0) * S, (WX1 - WX0) * S, 3)), (WX0 * S, WY0 * S))
d = ImageDraw.Draw(img)
# houses across the street
for hx, hw, hy in ((960, 260, 330), (1200, 300, 300), (1380, 160, 360)):
    shape([(hx, 470), (hx, hy + 60), (hx + hw / 2, hy), (hx + hw, hy + 60), (hx + hw, 470)], (40, 38, 52), 1.5,
          smooth=False)
    shape([(hx - 8, hy + 64), (hx + hw / 2, hy - 6), (hx + hw + 8, hy + 64), (hx + hw, hy + 70),
           (hx + hw / 2, hy + 10), (hx, hy + 70)], (236, 240, 248), 1.5, smooth=False)  # snow on the roof
    for wx in (hx + hw * 0.25, hx + hw * 0.65):
        rect(wx - 16, hy + 100, wx + 16, hy + 140, (236, 186, 90), 1.2)
shape([(WX0, 470), (WX1, 460), (WX1, WY1), (WX0, WY1)], (226, 232, 244), 1.5, smooth=False)  # snowy ground
for _ in range(160):
    x, y = rng.uniform(WX0, WX1), rng.uniform(WY0, WY1)
    r = rng.uniform(1.2, 3.2)
    ellipse(x, y, r, r, (245, 247, 252), 0)
# frame and glazing bars
FRAME = (236, 228, 212)
for x in (WX0, (WX0 + WX1) / 2, WX1):
    rect(x - 9, WY0, x + 9, WY1, FRAME, 2)
for y in (WY0, 260, 410, WY1):
    rect(WX0 - 9, y - 7, WX1 + 9, y + 7, FRAME, 2)
rect(WX0 - 30, WY1, WX1 + 30, WY1 + 22, CAB_L, 2.5)  # sill
# the garland: a green swag with red bows and warm lights
g_pts = [(WX0 - 40, 104), (WX0 + 110, 150), (1220, 132), (WX1 - 110, 150), (WX1 + 40, 104)]
for dy, col in ((10, (26, 58, 36)), (0, (40, 86, 50))):
    shape([(x, y + dy) for x, y in g_pts] + [(x, y + dy - 24) for x, y in reversed(g_pts)], col, 2)
for x, y in spline(g_pts, closed=False, n=6)[::2]:
    ellipse(x + rng.normal(0, 6), y - 10 + rng.normal(0, 5), 4, 4, (255, 214, 120), 0)
for bx, by in ((WX0 - 40, 100), (1220, 128), (WX1 + 40, 100)):
    shape([(bx, by), (bx - 30, by - 20), (bx - 34, by + 12)], (170, 24, 32), 2, smooth=False)
    shape([(bx, by), (bx + 30, by - 20), (bx + 34, by + 12)], (170, 24, 32), 2, smooth=False)
    shape([(bx - 4, by + 4), (bx - 16, by + 50), (bx - 6, by + 46)], (150, 20, 28), 2, smooth=False)
    shape([(bx + 4, by + 4), (bx + 16, by + 50), (bx + 6, by + 46)], (150, 20, 28), 2, smooth=False)
    ellipse(bx, by, 9, 8, (190, 30, 38), 2)

# back counter and a Christmas tree glowing at the far right
rect(0, 600, W, 626, (230, 226, 218), 2)
rect(0, 626, W, H, CAB, 2)
tree = [(1790, 330), (1700, 520), (1740, 520), (1650, 700), (1700, 700), (1610, 900), (1920, 900), (1920, 330)]
shape(tree, (24, 60, 38), 2.5, smooth=False)
for _ in range(60):
    x, y = rng.uniform(1650, 1915), rng.uniform(420, 890)
    if (x - 1790) > -(y - 330) * 0.5:
        ellipse(x, y, 4, 4, (255, 210, 110), 0)
for x, y, c in ((1760, 560, (170, 24, 32)), (1850, 640, (200, 170, 60)), (1720, 780, (170, 24, 32)),
                (1880, 820, (200, 170, 60)), (1800, 720, (170, 24, 32))):
    ellipse(x, y, 13, 13, c, 2)
# a brass pendant lamp over the island
stroke([(1290, 0), (1290, 58)], 2)
shape([(1225, 110), (1238, 76), (1290, 58), (1342, 76), (1355, 110)], BRASS, 2.5, smooth=False)
ellipse(1290, 110, 65, 9, (255, 236, 180), 2)

# ---------------------------------------------------------------------------
# The mother
# ---------------------------------------------------------------------------
HAIR, HAIR_L, HAIR_D = (44, 28, 22), (82, 54, 40), (24, 15, 12)
SKIN, SKIN_S, SKIN_D = (232, 186, 156), (198, 142, 114), (160, 104, 82)
KNIT, KNIT_S, KNIT_D = (222, 204, 176), (184, 164, 136), (150, 130, 104)

# long dark hair, behind her
shape([(842, 168), (904, 180), (934, 222), (930, 290), (938, 360), (962, 450), (972, 540), (950, 600),
       (905, 600), (880, 470), (800, 470), (760, 560), (720, 610), (690, 590), (720, 480), (748, 380),
       (752, 290), (770, 214)], HAIR, 3)
# the jumper: body
torso = [(812, 430), (760, 444), (676, 466), (652, 540), (660, 660), (676, 800), (978, 800), (992, 650),
         (996, 540), (978, 470), (902, 442), (874, 430)]
shape(torso, KNIT, 3)
shape([(676, 466), (652, 540), (660, 660), (676, 800), (730, 800), (716, 640), (706, 520)], KNIT_S, 0)  # shade
shape(torso, None, 3)
for x0, x1 in ((760, 770), (800, 805), (845, 845), (890, 885), (930, 922)):  # the knit's soft ribs
    stroke([(x0, 520), (x0 + 4, 640), (x1, 790)], 1.0, KNIT_S)
shape([(800, 760), (870, 772), (900, 800), (780, 800)], KNIT_S, 0)  # the jumper bunching at the counter
for pts in (((730, 560), (748, 620), (744, 690)), ((930, 540), (944, 610), (936, 690))):  # soft folds
    stroke(list(pts), 1.8, KNIT_D)
shape([(812, 468), (878, 466), (866, 484), (822, 486)], KNIT_S, 0)  # shadow cast by her hair and chin
# neck, with a hard shadow under the jaw
shape([(822, 352), (868, 360), (872, 438), (844, 452), (816, 436)], SKIN, 3)
shape([(822, 354), (868, 362), (866, 394), (844, 404), (820, 388)], SKIN_D, 0)
# crew neckline
shape([(800, 432), (842, 452), (884, 432), (890, 446), (842, 470), (794, 446)], KNIT_S, 2.5)

# the island: marble top and dark walnut front
MARBLE, MARBLE_S, WALNUT, WALNUT_D = (238, 234, 228), (206, 202, 196), (78, 48, 32), (54, 32, 22)
shape([(0, 800), (W, 800), (W, 880), (0, 880)], MARBLE, 3, smooth=False)
for _ in range(14):
    x = rng.uniform(0, W)
    stroke([(x, 802), (x + rng.uniform(-80, 80), 830), (x + rng.uniform(-160, 160), 878)], 1.1, (170, 166, 162))
shape([(0, 880), (W, 880), (W, 898), (0, 898)], MARBLE_S, 2, smooth=False)
shape([(0, 898), (W, 898), (W, H), (0, H)], WALNUT, 3, smooth=False)
for x in range(80, W, 320):
    rect(x, 930, x + 260, 1060, WALNUT, 2)
    rect(x + 10, 940, x + 250, 950, WALNUT_D, 0)

# the chopping board
BOARD, BOARD_S = (186, 128, 72), (148, 96, 52)
shape([(596, 806), (1176, 806), (1196, 852), (576, 852)], BOARD, 3, smooth=False)
shape([(576, 852), (1196, 852), (1196, 870), (576, 870)], BOARD_S, 3, smooth=False)
for y in (818, 830, 842):
    stroke([(600, y), (1180, y)], 1, (160, 108, 60), smooth=False)

# a sticky, glazed rack of ribs, charred at the edges
GLAZE, GLAZE_D, GLAZE_L, BONE = (140, 62, 24), (82, 32, 14), (222, 140, 64), (240, 228, 200)
shape([(806, 796), (1090, 786), (1116, 806), (1110, 842), (816, 850), (798, 826)], GLAZE, 3)
shape([(812, 836), (1110, 828), (1110, 842), (816, 850)], GLAZE_D, 0, smooth=False)
for x in range(836, 1100, 34):
    stroke([(x, 792), (x - 5, 846)], 2.2, GLAZE_D)
    shape([(x - 9, 845), (x + 3, 844), (x + 4, 856), (x - 10, 857)], BONE, 2)
for x, y in ((850, 800), (920, 797), (990, 794), (1050, 792)):
    stroke([(x, y), (x + 34, y - 2)], 3, GLAZE_L)
    stroke([(x + 6, y + 14), (x + 22, y + 13)], 2, GLAZE_L)
for x in (870, 960, 1040):  # char from the grill
    stroke([(x, 812), (x + 22, 822)], 3, (48, 20, 10))
# a rib already cut free, lying by the blade
shape([(716, 812), (786, 806), (792, 836), (722, 842)], GLAZE, 3)
stroke([(726, 816), (776, 812)], 2.5, GLAZE_L)
shape([(718, 840), (730, 840), (730, 854), (716, 854)], BONE, 2)

# her far arm, reaching to steady the meat
shape([(978, 470), (1004, 540), (1016, 640), (1040, 720), (1072, 786), (1036, 796), (1004, 730),
       (982, 650), (970, 560)], KNIT, 3)
shape([(1004, 730), (1036, 796), (1072, 786), (1060, 760)], KNIT_S, 0)
shape([(1044, 782), (1076, 776), (1082, 792), (1048, 798)], KNIT_S, 2)  # cuff
# her left hand flat on the ribs, fingers spread towards the blade
shape([(1040, 790), (1082, 786), (1102, 800), (1096, 818), (1054, 822), (1036, 806)], SKIN, 2.5)
for i, (fx, fy) in enumerate(((990, 802), (986, 812), (992, 822), (1004, 830))):
    shape([(1046, 797 + i * 7), (fx, fy), (fx - 1, fy + 5), (1044, 803 + i * 7)], SKIN, 1.8, smooth=False)
    ellipse(fx + 5, fy + 3, 3, 2, (236, 206, 190), 0)
shape([(1060, 818), (1040, 834), (1030, 836), (1034, 826), (1052, 814)], SKIN, 2)  # thumb
stroke([(1060, 800), (1090, 806)], 1.2, SKIN_S)

# her near arm, the cleaver held loosely, resting in the meat mid-cut
shape([(676, 466), (648, 540), (628, 640), (636, 700), (668, 736), (706, 734), (706, 704), (676, 672),
       (686, 580), (708, 510)], KNIT, 3)
shape([(648, 540), (628, 640), (636, 700), (660, 700), (652, 600), (668, 530)], KNIT_S, 0)
shape([(662, 726), (706, 722), (712, 742), (668, 746)], KNIT_S, 2)  # cuff
# the cleaver
STEEL, STEEL_D, STEEL_L, EDGE = (176, 182, 190), (118, 124, 134), (226, 230, 236), (246, 248, 252)
shape([(748, 704), (870, 712), (866, 822), (742, 814)], STEEL, 3, smooth=False)
shape([(748, 704), (870, 712), (869, 734), (747, 726)], STEEL_D, 0, smooth=False)  # the heavy spine
shape([(748, 704), (870, 712), (866, 822), (742, 814)], None, 3, smooth=False)
stroke([(744, 806), (866, 814)], 2.5, EDGE, smooth=False)  # the honed edge
stroke([(790, 748), (848, 752), (846, 790)], 3, STEEL_L, smooth=False)  # a streak of warm light on the flat
ellipse(854, 724, 7, 6, (60, 30, 25), 2)  # hanging hole
ellipse(760, 718, 3, 3, (90, 94, 102), 0)
shape([(748, 718), (700, 724), (688, 742), (746, 738)], (40, 26, 20), 2.5)  # handle
# her hand wrapped round the handle
shape([(690, 716), (736, 712), (752, 726), (748, 752), (708, 760), (686, 748)], SKIN, 2.5)
for fy in (726, 736, 746):
    stroke([(722, fy - 2), (748, fy)], 1.5, SKIN_D)
shape([(708, 716), (742, 704), (752, 712), (738, 722)], SKIN, 2)  # thumb over the top
shape([(690, 740), (708, 760), (686, 748)], SKIN_S, 0)

# ---------------------------------------------------------------------------
# Her face: three-quarters, turned towards her daughter off to the right, a gentle smile
# ---------------------------------------------------------------------------
face = [(836, 206), (880, 212), (900, 234), (906, 258), (899, 273), (904, 286), (913, 306), (920, 318),
        (913, 326), (904, 328), (904, 336), (905, 341), (900, 347), (901, 352), (895, 357), (893, 363),
        (880, 370), (858, 371), (831, 360), (808, 338), (792, 306), (792, 258), (806, 224)]
shape(face, SKIN, 3)
# the hard shadow on the side away from the window, and under the cheekbone
shape([(806, 224), (792, 258), (792, 306), (808, 338), (831, 360), (842, 358), (826, 336), (818, 300),
       (822, 258), (828, 230)], SKIN_S, 0)
shape([(824, 318), (846, 326), (870, 330), (852, 338), (830, 334)], (216, 164, 136), 0)
shape([(884, 276), (893, 298), (902, 316), (892, 320), (884, 300)], SKIN_S, 0)  # side of the nose
shape(face, None, 3)
ellipse(878, 324, 12, 6, (226, 170, 146), 0)  # a little colour in the cheek
# brows
stroke([(824, 267), (838, 260), (856, 258), (868, 262)], 3.4)
stroke([(882, 262), (892, 258), (899, 260)], 3.0)
# eyes: almond-shaped, looking right, soft lower lids
for cx, cy, w, h in ((846, 285, 16, 6.5), (888, 284, 8, 5.5)):
    shape([(cx - w, cy), (cx - w * 0.2, cy - h), (cx + w, cy - h * 0.2), (cx + w * 0.1, cy + h * 0.7)],
          (240, 232, 222), 1.5)
    ellipse(cx + w * 0.35, cy - h * 0.05, h * 0.95, h * 0.95, (86, 52, 34), 0)
    ellipse(cx + w * 0.35, cy - h * 0.05, h * 0.45, h * 0.45, INK, 0)
    ellipse(cx + w * 0.55, cy - h * 0.35, 1.4, 1.4, (250, 246, 240), 0)
    stroke([(cx - w - 2, cy + 1), (cx - w * 0.2, cy - h - 1), (cx + w + 3, cy - h * 0.3)], 3.6)  # upper lid, lashes
    stroke([(cx + w, cy - h * 0.3), (cx + w + 6, cy - h - 1)], 2.0)  # a lash flick
    stroke([(cx - w * 0.3, cy - h - 7), (cx + w * 0.8, cy - h - 4)], 1.3, SKIN_D)  # lid crease
    stroke([(cx - w * 0.6, cy + h * 0.6), (cx + w * 0.3, cy + h * 0.9)], 1.1, SKIN_D)  # lower lid
stroke([(898, 318), (896, 322), (902, 324)], 1.6)  # nostril
# lips: full, a gentle closed smile, corners lifting
LIP, LIP_D = (178, 96, 92), (140, 66, 66)
shape([(857, 344), (868, 340), (880, 341), (889, 338), (901, 341), (896, 345), (870, 346)], LIP_D, 1.2, smooth=False)
shape([(860, 346), (872, 348), (896, 346), (899, 349), (888, 355), (871, 354)], LIP, 1.2)
stroke([(850, 340), (857, 345), (872, 347), (888, 346), (900, 343)], 2.3)
stroke([(850, 340), (847, 336)], 1.5)  # the smile's soft crease
stroke([(874, 360), (884, 360)], 1.4, SKIN_S)
# her hair falling around her face, a soft side parting, a lock over her near shoulder
shape([(800, 222), (826, 196), (868, 194), (902, 214), (916, 246), (904, 240), (880, 224), (850, 222),
       (822, 240), (808, 262)], HAIR, 3)
shape([(806, 222), (792, 260), (786, 320), (776, 400), (760, 470), (744, 540), (752, 612), (782, 626),
       (792, 560), (798, 470), (806, 400), (812, 330), (818, 262)], HAIR, 3)
for pts in (([(830, 204), (812, 240), (800, 300), (790, 380), (774, 470), (762, 560)]),
            ([(860, 202), (894, 220), (910, 240)]), ([(846, 176), (800, 190), (776, 230)])):
    stroke(pts, 2, HAIR_L)
stroke([(904, 240), (918, 290), (922, 350), (940, 430)], 2.5)  # hair behind the far cheek
for pts in (((838, 182), (880, 186), (912, 214)), ((770, 300), (760, 420), (748, 520)),
            ((940, 380), (958, 470), (962, 540))):
    stroke(list(pts), 3.5, HAIR_L)

# ---------------------------------------------------------------------------
# The grade: warm lamplight, a cold edge from the window, a darkened vignette
# ---------------------------------------------------------------------------
out = img.resize((W, H), Image.LANCZOS)
a = np.asarray(out).astype(float) / 255
yy, xx = np.mgrid[0:H, 0:W]
vig = 1 - 0.42 * (((xx - W * 0.48) / (W * 0.62)) ** 2 + ((yy - H * 0.45) / (H * 0.75)) ** 2)
a *= np.clip(vig, 0.45, 1)[..., None]
warm = np.array([1.06, 0.98, 0.86])
cold = np.array([0.9, 0.98, 1.1])
mix = np.clip((xx - 800) / 900, 0, 1)[..., None] * 0.5
a = a * (warm * (1 - mix) + cold * mix)
a = np.clip(a, 0, 1) ** 1.05
Image.fromarray((a * 255).astype(np.uint8)).save(sys.argv[1], optimize=True)
print('saved', sys.argv[1])
