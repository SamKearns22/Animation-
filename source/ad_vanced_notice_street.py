#!/usr/bin/env python3
"""MAP  Ad-Vanced Notice (8 Nov): shot 5, the Minneapolis street (notes/ad-vanced-notice.md, "Street elements";
brief rows 29-33). A Lake Street kind of block in winter, one locked camera on the near pavement; four ICE officers
beat a man curled up on the snow while Vance stands to their left, smiling at us; a slow push in on his face through
line 9. Flat painting (rule 39), every piece at its real size in metres; the push in is a zoom (for a flat painting
the same picture as a push), repainted at each zoom so it stays sharp.

    python3 source/ad_vanced_notice_street.py sheet OUT.jpg     the shot wide, mid push and at the end + the cast
    python3 source/ad_vanced_notice_street.py beat OUT.mp4      the beating alone, small (a movement clip)

Map: camera, zoom 40 | the painting 75 (sky 95, buildings 110, street 230, snow falling 300) | SET_BOXES 320 |
     the officers' gear 345 | the cast 420 | the man on the ground 455 | the beating 505 | draw_group 575 |
     BENCHMARK 625 | sheets 650

In the film: cam_at(z) -> Level; paint(cam) the street; snow(img, cam, t); draw_group(img, cam, t) the officers and
the man (far to near); place(cam, x, d) -> screen x, soles y, px per metre for anyone standing (Vance at VANCE_AT).
"""
import functools
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ad_vanced_notice_sets as ST   # noqa: E402  (Pen, layer, shrink, cut, box, wobbly, mix, Level)
import power_crime_cast as PC        # noqa: E402  (block lettering on the vests, rough edges)
import burnham as B                  # noqa: E402
import lying as LY                   # noqa: E402  the man curled on the snow: one 3D body
import moves                         # noqa: E402
import sets as S                     # noqa: E402
import views as V                    # noqa: E402
from ed import INK, curve            # noqa: E402
from satire_style import rough       # noqa: E402

W, H = ST.W, ST.H
Pen, layer, shrink, cut, box, wobbly, mix = ST.Pen, ST.layer, ST.shrink, ST.cut, ST.box, ST.wobbly, ST.mix
LW = ST.LW

# ---------------------------------------------------------------------------------------------- camera, zoom
# A level camera 1.6 m up on the near pavement, horizon y 800, focal 1625 (Sam, 8 Nov: 25% closer than the first
# build's 1300), its middle a little right of the frame's so the group and Vance both fit. Vance 5.0 m out, the
# officers and the man 6.9-7.6 m, the near kerb's snowbank 8.4 m, the road to 15 m, the far snowbank, the shopfronts.
H_CAM, HZ, FOCAL, CX = 1.6, 800.0, 1625.0, 572.0
D_FACADE, D_FAR_BANK, D_ROAD, D_NEAR_BANK = 18.0, 15.3, (9.0, 15.0), 8.4
VANCE_AT = (-1.1, 6.85)                  # world x, d (brief 31: to the left of them; Sam, 9 Nov: level with them)
MAN_AT = (0.7, 6.55)                     # the man's middle on the snow (Sam, 9 Nov: in front of their feet, all of him)
# The officers: (x, d, yaw, move, offset s): one kicks from his head end, side on; one stamps on his back from
# behind, facing us (his vest reads); two punch down from his feet end, side on, bent over him; each strikes every 1.36 s, a quarter period apart (about 3 blows a second, Q18).
PERIOD = 1.36
# (Sam, 9 Nov: he was buried behind their legs, a blow landed on his head, the blows on the right missed.) Now he
# lies in front of their feet; the kicker and one puncher stand nearer us, clear of him at either end, the stamper
# and the other puncher behind him; every blow is aimed at the height where it meets his outline on screen.
# (Sam, 9 Nov, later: he lies flat on his front, 1.7 m long, head to our left.)
OFFICERS = [('O1', -0.3, 6.35, 90, 'kick', 0.0),               # at his head end, kicking his upper back
            ('O3', 0.45, 7.2, 0, 'stomp', PERIOD * 0.25),      # behind him, facing us: stamps on his back
            ('O2', 1.32, 6.2, -90, 'punch', PERIOD * 0.5),     # kneeling beside his hips, punching down on them
            ('O4', 1.2, 7.25, 0, 'stomp', PERIOD * 0.75)]      # behind him, facing us: stamps on his legs
PUSH = {'O1': (0.05, 0.0), 'O3': (0.0, -0.04), 'O2': (-0.03, -0.03), 'O4': (0.0, -0.04)}   # (m right, m nearer us)


def cam_at(z=1.0, focus=None, to=None):
    """The camera zoomed z times about `focus` (a screen point at z = 1), that point moved to `to`."""
    if z == 1.0 or focus is None:
        return ST.Level(H_CAM, HZ, FOCAL, CX)
    tx, ty = to or focus
    return ST.Level(H_CAM, ty + z * (HZ - focus[1]), FOCAL * z, tx + z * (CX - focus[0]))


def place(cam, x, d):
    """Screen x, soles y and px per metre for someone standing at world (x, d)."""
    sx, sy = cam.p(x, d, 0.0)
    return sx, sy, cam.ppm(d)


def scam(cam):
    """The same camera as a sets.Cam (x, y up, z away), for the 3D body on the snow."""
    return S.Cam((0.0, H_CAM, 0.0), (0.0, H_CAM, 1.0), cam.f, shake=(cam.cx - 540.0, cam.hz - 960.0))


# ---------------------------------------------------------------------------------------------- the painting
SKY = [(196, 199, 205), (204, 207, 212), (212, 214, 218), (219, 221, 224)]
SNOW, SNOW_SH, SNOW_D = (240, 242, 246), (214, 220, 230), (196, 200, 208)
SLUSH, SLUSH_D = (168, 160, 150), (138, 130, 122)
CONCRETE = (176, 174, 170)
BRICK_RED, BRICK_BROWN, BRICK_TAN = (150, 66, 48), (122, 74, 56), (190, 150, 108)
STONE = (214, 204, 184)
GLASS, GLASS_L = (52, 62, 74), (98, 112, 128)
SIGN_GREEN, SIGN_RED, SIGN_BLUE = (30, 96, 64), (170, 36, 36), (36, 70, 140)


def _q(cam, pts):
    """World (x, d, z) points to the screen."""
    return [cam.p(x, d, z) for x, d, z in pts]


def _wall_box(cam, x0, x1, z0, z1, d=D_FACADE):
    return _q(cam, [(x0, d, z1), (x1, d, z1), (x1, d, z0), (x0, d, z0)])


def _ground(cam, x0, x1, d0, d1):
    return _q(cam, [(x0, d0, 0.0), (x1, d0, 0.0), (x1, d1, 0.0), (x0, d1, 0.0)])


def _sky(pen, cam):
    for k, c in enumerate(SKY):
        y0 = -40 + k * (cam.hz + 40) / 4
        pen.poly(wobbly(box(-60, y0, W + 60, cam.hz + 4), 3, 500 + k, 140), c, 0)


# The block (Sam, 8 Nov: "you can do shopfronts"; refs street-lake-800, street-uptown-winter): two- and three-storey
# brick, shops below with big windows, sign bands, awnings; flats above with tall sash windows and stone sills. Made-up
# names only (no real brands). (x0, x1, height, brick, storeys, sign, sign colour, awning colours)
BLOCK = [(-12.5, -6.2, 8.4, BRICK_BROWN, 2, 'BARBER', SIGN_BLUE, ((236, 236, 232), SIGN_BLUE)),
         (-6.2, -1.1, 8.0, BRICK_RED, 2, 'TAQUERIA LA PALMA', SIGN_GREEN, ((40, 128, 72), (236, 236, 232), (190, 40, 40))),
         (-1.1, 3.9, 11.2, BRICK_TAN, 3, 'LAVANDERIA  COIN LAUNDRY', SIGN_BLUE, ((236, 200, 60), (236, 236, 232))),
         (3.9, 9.2, 8.2, BRICK_RED, 2, 'HARDWARE', SIGN_RED, ((40, 96, 64), (236, 236, 232))),
         (9.2, 15.0, 8.6, BRICK_BROWN, 2, 'GROCERY', SIGN_GREEN, ((190, 40, 40), (236, 236, 232)))]
SHOP_Z = (0.55, 2.85)                    # shop windows
SIGN_Z = (3.05, 3.85)                    # the sign band
AWN = (2.95, 2.35, 1.1)                  # the awning: top at the wall, front edge height, how far it comes out


def _windows(b):
    """Each building's upper windows: (x0, x1, z0, z1)."""
    x0, x1, top, _, storeys = b[:5]
    out = []
    n = max(2, int((x1 - x0) / 1.7))
    w = 0.95
    for f in range(1, storeys):
        z0 = 4.45 + (f - 1) * 3.05
        for i in range(n):
            cx = x0 + (x1 - x0) * (i + 0.5) / n
            out.append((cx - w / 2, cx + w / 2, z0, z0 + 1.75))
    return out


def _shopfront(b):
    """(windows, door) on the shop floor: two big panes either side of a recessed door."""
    x0, x1 = b[0], b[1]
    m = (x0 + x1) / 2 + 0.6
    return [(x0 + 0.35, m - 0.75), (m + 0.75, x1 - 0.35)], (m - 0.55, m + 0.55)


def _building(pen, cam, i, b):
    x0, x1, top, col, storeys, sign, sign_c, awn = b
    d = D_FACADE
    pen.poly(cut(_wall_box(cam, x0, x1, 0.0, top), 1.2, 600 + i), col, LW)
    r = random.Random(610 + i)                                         # a few brick courses, hand-cut
    for k in range(26):
        z = r.uniform(0.6, top - 0.8)
        xx = r.uniform(x0 + 0.2, x1 - 1.0)
        pen.line(_q(cam, [(xx, d, z), (xx + r.uniform(0.3, 0.8), d, z)]), mix(col, (0, 0, 0), 0.18), 1.6)
    for f in range(1, storeys):                                         # a stone band at each floor
        z = 4.2 + (f - 1) * 3.05
        pen.poly(_wall_box(cam, x0, x1, z - 0.12, z), mix(STONE, col, 0.2), 1.5)
    # the cornice: a stone parapet stepping out, snow on top
    pen.poly(cut(_q(cam, [(x0 - 0.12, d - 0.1, top), (x1 + 0.12, d - 0.1, top), (x1 + 0.12, d - 0.1, top - 0.45),
                          (x0 - 0.12, d - 0.1, top - 0.45)]), 1.0, 620 + i), STONE, LW)
    pen.poly(wobbly(_q(cam, [(x0 - 0.12, d - 0.1, top + 0.16), (x1 + 0.12, d - 0.1, top + 0.16),
                             (x1 + 0.12, d - 0.1, top - 0.02), (x0 - 0.12, d - 0.1, top - 0.02)]), 1.2, 630 + i, 18),
             SNOW, 2)
    for k, (a, c, z0, z1) in enumerate(_windows(b)):                    # sash windows, stone sills with snow
        pen.poly(_wall_box(cam, a - 0.08, c + 0.08, z0 - 0.08, z1 + 0.18), STONE, 2)
        pen.poly(_wall_box(cam, a, c, z0, z1), GLASS, 2)
        pen.line(_q(cam, [(a, d, (z0 + z1) / 2), (c, d, (z0 + z1) / 2)]), (226, 222, 210), 3)   # the sash rail
        pen.poly(_q(cam, [(a + 0.12, d, z1 - 0.1), (a + 0.4, d, z1 - 0.1), (a + 0.12, d, z1 - 0.5)]), GLASS_L, 0)
        pen.poly(_wall_box(cam, a - 0.16, c + 0.16, z0 - 0.2, z0 - 0.06), STONE, 2)
        pen.poly(wobbly(_wall_box(cam, a - 0.15, c + 0.15, z0 - 0.06, z0 + 0.04), 0.8, 640 + 30 * i + k, 10), SNOW, 0)
    # the shop floor: sign band, big windows on a brick base, the recessed door
    pen.poly(cut(_wall_box(cam, x0 + 0.2, x1 - 0.2, SIGN_Z[0], SIGN_Z[1]), 1.0, 650 + i), sign_c, LW)
    sx, sy = cam.p((x0 + x1) / 2, d, sum(SIGN_Z) / 2)
    hgt = (SIGN_Z[1] - SIGN_Z[0]) * cam.ppm(d)
    size = min(hgt * 0.5, (x1 - x0 - 0.8) * cam.ppm(d) / max(6, len(sign)) * 1.55)
    pen.text((sx, sy), sign, size, (246, 244, 236), 'mm')
    wins, door = _shopfront(b)
    for k, (a, c) in enumerate(wins):
        pen.poly(_wall_box(cam, a, c, SHOP_Z[0], SHOP_Z[1]), GLASS, LW)
        n = max(1, int((c - a) / 1.3))
        for m in range(1, n):
            xm = a + (c - a) * m / n
            pen.line(_q(cam, [(xm, d, SHOP_Z[0]), (xm, d, SHOP_Z[1])]), (190, 186, 178), 3)
        pen.poly(_q(cam, [(a + 0.2, d, SHOP_Z[1] - 0.15), (a + 0.8, d, SHOP_Z[1] - 0.15), (a + 0.2, d, SHOP_Z[0] + 0.9)]),
                 GLASS_L, 0)
        r2 = random.Random(660 + 10 * i + k)                            # a lit interior: shelves and posters
        for q in range(3):
            u = r2.uniform(0.2, 0.75)
            xa = a + (c - a) * u
            pen.poly(_wall_box(cam, xa, xa + r2.uniform(0.25, 0.5), SHOP_Z[0] + 0.5, SHOP_Z[0] + r2.uniform(1.0, 1.6)),
                     r2.choice([(214, 190, 120), (196, 90, 70), (120, 160, 190), (230, 226, 210)]), 0)
    pen.poly(_wall_box(cam, door[0], door[1], 0.0, SHOP_Z[1]), (40, 40, 46), LW)
    pen.poly(_wall_box(cam, door[0] + 0.14, door[1] - 0.14, 0.25, SHOP_Z[1] - 0.25), GLASS_L, 2)
    # the awning over the windows and door: we look up at its striped front valance and dark underside
    a0, a1 = x0 + 0.25, x1 - 0.25
    zt, zf, out = AWN
    under = _q(cam, [(a0, d, zt), (a1, d, zt), (a1, d - out, zf), (a0, d - out, zf)])
    pen.poly(under, mix(awn[0], (0, 0, 0), 0.45), LW)
    n = max(4, int((a1 - a0) / 0.45))
    for k in range(n):
        ua, ub = a0 + (a1 - a0) * k / n, a0 + (a1 - a0) * (k + 1) / n
        pen.poly(_q(cam, [(ua, d - out, zf), (ub, d - out, zf), (ub, d - out, zf - 0.32), (ua, d - out, zf - 0.32)]),
                 awn[k % len(awn)], 0)
    pen.poly(_q(cam, [(a0, d - out, zf), (a1, d - out, zf), (a1, d - out, zf - 0.32), (a0, d - out, zf - 0.32)]), None,
             LW)
    pen.poly(wobbly(_q(cam, [(a0, d - out, zf + 0.1), (a1, d - out, zf + 0.1), (a1, d - out, zf - 0.01),
                             (a0, d - out, zf - 0.01)]), 1.0, 670 + i, 16), SNOW, 2)   # snow on the awning's edge


def _lamp(pen, cam, x, d):
    """A black street lamp (ref street-lake-800): a tall pole, a curved arm, a hanging lantern; snow on top."""
    ppm = cam.ppm(d)
    pen.poly(_q(cam, [(x - 0.07, d, 0), (x + 0.07, d, 0), (x + 0.05, d, 6.6), (x - 0.05, d, 6.6)]), (30, 32, 34), 2)
    pen.poly(_q(cam, [(x - 0.14, d, 0), (x + 0.14, d, 0), (x + 0.1, d, 0.9), (x - 0.1, d, 0.9)]), (30, 32, 34), 2)
    arm = [cam.p(x + 0.9 * math.sin(a), d, 6.6 + 0.5 * math.cos(a) - 0.2) for a in np.linspace(0, 1.9, 10)]
    pen.line(arm, INK, max(2.0, 0.09 * ppm))
    lx, ly = arm[-1]
    pen.poly([(lx - 0.22 * ppm, ly), (lx + 0.22 * ppm, ly), (lx + 0.16 * ppm, ly + 0.5 * ppm),
              (lx - 0.16 * ppm, ly + 0.5 * ppm)], (236, 230, 200), 2)
    pen.poly(wobbly([(lx - 0.26 * ppm, ly - 0.06 * ppm), (lx + 0.26 * ppm, ly - 0.06 * ppm), (lx + 0.22 * ppm, ly + 0.02 * ppm),
                     (lx - 0.22 * ppm, ly + 0.02 * ppm)], 0.5, int(x * 10), 8), SNOW, 2)


def _tree(pen, cam, x, d, seed):
    """A bare street tree (ref street-uptown-winter): a grey trunk forking into thin branches, snow on a few."""
    r = random.Random(seed)
    ppm = cam.ppm(d)
    col = (86, 80, 76)

    def branch(x0, z0, ang, ln, w, depth):
        x1, z1 = x0 + ln * math.sin(ang), z0 + ln * math.cos(ang)
        pen.line(_q(cam, [(x0, d, z0), (x1, d, z1)]), col, max(1.2, w * ppm))
        if depth < 4:
            for s in (-1, 1):
                branch(x1, z1, ang + s * r.uniform(0.3, 0.6), ln * r.uniform(0.62, 0.78), w * 0.62, depth + 1)
    pen.poly(_q(cam, [(x - 0.14, d, 0), (x + 0.14, d, 0), (x + 0.1, d, 2.6), (x - 0.1, d, 2.6)]), col, 2)
    for s in (-1, 0, 1):
        branch(x + s * 0.05, 2.5, s * 0.45 + r.uniform(-0.1, 0.1), 1.9, 0.14, 1)
    pen.poly(wobbly(_q(cam, [(x - 0.4, d - 0.4, 0.02), (x + 0.4, d - 0.4, 0.02), (x + 0.4, d + 0.4, 0.02),
                             (x - 0.4, d + 0.4, 0.02)]), 0.5, seed, 8), SNOW_SH, 0)


def _wires(pen, cam):
    """Two utility wires sagging across the sky over the block (approved, Street elements 1)."""
    for z, k in ((12.4, 0), (11.9, 1)):
        pts = [(x, 16.8, z - 0.9 * (1 - (x / 14.0) ** 2)) for x in np.linspace(-14, 14, 40)]
        pen.line(_q(cam, pts), (60, 60, 64), 2.0)


def _street(pen, cam):
    """The far pavement and its snowbank, the ploughed road with slush ruts, the near snowbank (behind the people),
    the shovelled near pavement they stand on."""
    pen.poly(_ground(cam, -80, 80, D_FAR_BANK, D_FACADE), (224, 226, 230), 0)          # the far pavement
    r = random.Random(700)
    pts = [(x, D_FAR_BANK, 0.0) for x in np.linspace(-60, 60, 2)]
    top = [(x, D_FAR_BANK - 0.2, 0.62 + 0.28 * math.sin(x * 1.3) * r.uniform(0.6, 1.0)) for x in np.linspace(60, -60, 220)]
    pen.poly(_q(cam, pts + top), SNOW, LW)                                                # the far snowbank
    pen.poly(wobbly(_q(cam, [(-60, D_FAR_BANK - 0.2, 0.0), (60, D_FAR_BANK - 0.2, 0.0), (60, D_FAR_BANK - 0.2, 0.2),
                             (-60, D_FAR_BANK - 0.2, 0.2)]), 1.0, 701, 30), SNOW_D, 0)
    d0, d1 = D_ROAD
    pen.poly(_ground(cam, -80, 80, d0, d1), (226, 226, 228), 0)                           # packed snow on the road
    for k, (a, b) in enumerate(((9.5, 9.95), (10.85, 11.35), (12.15, 12.65), (13.6, 14.1))):   # four wheel ruts
        pen.poly(wobbly(_ground(cam, -80, 80, a, b), 0.6, 710 + k, 40), SLUSH, 0)
        pen.poly(wobbly(_ground(cam, -80, 80, a + 0.12, b - 0.14), 0.4, 720 + k, 40), SLUSH_D, 0)
    for k in range(40):                                                                    # slush clods
        x, dd = r.uniform(-14, 14), r.uniform(d0 + 0.3, d1 - 0.3)
        rad = r.uniform(0.08, 0.25)
        ring = [(x + rad * math.cos(a), dd + rad * 0.6 * math.sin(a), 0.0) for a in np.linspace(0, 6.28, 9, endpoint=False)]
        pen.poly(_q(cam, ring), r.choice([SLUSH, SNOW_D, (232, 232, 234)]), 0)
    # the near snowbank along our kerb (waist high, lumpy, grimy at its foot)
    pts = [(x, D_NEAR_BANK + 0.5, 0.0) for x in (-60, 60)]
    top = [(x, D_NEAR_BANK + 0.3, 0.7 + 0.22 * math.sin(x * 1.7 + 0.5) + 0.08 * math.sin(x * 4.1)) for x in np.linspace(60, -60, 300)]
    pen.poly(_q(cam, pts + top), SNOW, LW)
    face = [(x, D_NEAR_BANK, 0.0) for x in (-60, 60)] + \
        [(x, D_NEAR_BANK, 0.45 + 0.15 * math.sin(x * 2.3)) for x in np.linspace(60, -60, 300)]
    pen.poly(_q(cam, face), SNOW_SH, 0)
    pen.poly(wobbly(_q(cam, [(-60, D_NEAR_BANK, 0.0), (60, D_NEAR_BANK, 0.0), (60, D_NEAR_BANK, 0.12),
                             (-60, D_NEAR_BANK, 0.12)]), 1.0, 730, 30), SNOW_D, 0)
    # the near pavement: shovelled, packed snow at the edges, bare concrete in the middle with slab joints
    pen.poly(_ground(cam, -80, 80, 0.5, D_NEAR_BANK), (228, 230, 234), 0)
    pen.poly(wobbly(_ground(cam, -80, 80, 3.2, 7.9), 0.25, 740, 30), CONCRETE, 0)
    for dd in np.arange(3.6, 7.9, 1.5):                                                    # slab joints
        pen.line(_q(cam, [(-60, dd, 0.0), (60, dd, 0.0)]), mix(CONCRETE, (0, 0, 0), 0.2), 2.0)
    for k in range(70):                                                                    # packed snow patches
        x, dd = r.uniform(-8, 8), r.uniform(3.0, 8.0)
        rad = r.uniform(0.15, 0.6)
        ring = [(x + rad * math.cos(a) * r.uniform(0.7, 1.1), dd + rad * 0.5 * math.sin(a) * r.uniform(0.7, 1.1), 0.0)
                for a in np.linspace(0, 6.28, 10, endpoint=False)]
        pen.poly(_q(cam, ring), r.choice([(228, 230, 234), (214, 216, 222), (238, 240, 244)]), 0)
    for k in range(30):                                                                    # rock salt and grit
        x, dd = r.uniform(-8, 8), r.uniform(2.5, 8.0)
        pen.ell(*cam.p(x, dd, 0.0), 0.02 * cam.ppm(dd), 0.012 * cam.ppm(dd), (150, 146, 140), 0)


@functools.lru_cache(maxsize=6)
def _painted(f, cx, hz):
    cam = ST.Level(H_CAM, hz, f, cx)
    lay = layer()
    pen = Pen(lay)
    _sky(pen, cam)
    _wires(pen, cam)
    for i, b in enumerate(BLOCK):
        _building(pen, cam, i, b)
    _tree(pen, cam, -6.2, 16.6, 801)                  # between the shopfronts, clear of the signs
    _tree(pen, cam, 9.2, 16.6, 802)
    _lamp(pen, cam, 3.9, 16.2)
    _lamp(pen, cam, -9.0, 16.2)
    _street(pen, cam)
    return shrink(lay)


def paint(cam):
    """The street through `cam` (a Level), as a 1080 x 1920 RGBA."""
    return _painted(round(cam.f, 2), round(cam.cx, 2), round(cam.hz, 2)).copy()


def snow(img, cam, t, near=None):
    """Light snow falling (Q22): flakes in the air from 3 to 17 m out, drifting down at about 0.9 m/s with a slow sway,
    flat white dots (no outline), smaller with distance. near=(d0, d1) only those between."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    r = random.Random(900)
    for k in range(340):
        dd = r.uniform(3.0, 17.0)
        x0 = r.uniform(-0.75, 0.75) * dd * 0.9
        z = (r.uniform(0, 14.0) - (0.9 + 0.3 * r.random()) * t) % 14.0
        x = x0 + 0.25 * math.sin(t * 0.9 + k)
        if near and not (near[0] <= dd < near[1]):
            continue
        sx, sy = cam.p(x, dd, z)
        rad = min(9.0, 0.028 * cam.ppm(dd))
        if -20 < sx < W + 20 and -20 < sy < H + 20:
            d.ellipse([sx - rad, sy - rad, sx + rad, sy + rad], fill=(250, 251, 253, 235))
    img.alpha_composite(lay)


# ---------------------------------------------------------------------------------------------- rule 83
def _set_boxes():
    """Every painted thing on the shop fronts in wall metres (x0, z0, x1, z1)."""
    out = []
    for i, b in enumerate(BLOCK):
        nm = b[5].split()[0].lower()
        out.append((f'{nm} sign', (b[0] + 0.2, SIGN_Z[0], b[1] - 0.2, SIGN_Z[1])))
        wins, door = _shopfront(b)
        for k, (a, c) in enumerate(wins):
            out.append((f'{nm} shop window {k + 1}', (a, SHOP_Z[0], c, SHOP_Z[1])))
        out.append((f'{nm} door', (door[0], 0.0, door[1], SHOP_Z[1])))
        out.append((f'{nm} awning', (b[0] + 0.25, AWN[1] - 0.32, b[1] - 0.25, AWN[0])))
        for k, (a, c, z0, z1) in enumerate(_windows(b)):
            out.append((f'{nm} window {k + 1}', (a - 0.16, z0 - 0.2, c + 0.16, z1 + 0.18)))
    return out


SET_BOXES = _set_boxes()
SET_MEANT = [(f'{b[5].split()[0].lower()} awning', f'{b[5].split()[0].lower()} {w}',
              'the awning hangs out in front of the top of its shop windows and door (we look up under it)')
             for b in BLOCK for w in ('shop window 1', 'shop window 2', 'door')]


# ---------------------------------------------------------------------------------------------- the officers' gear
# ICE officers as in real raids (Q17; refs ice-surge-1..3): coyote-tan or olive plate carriers, black patches with
# yellow POLICE and ICE (big on the back, smaller on the chest),
# black face masks (gaiters) up to the eyes, dark baseball caps, gloves, boots; a different build and different
# clothes under each vest.
VEST_TAN, VEST_OLIVE = (150, 132, 96), (92, 96, 70)          # (refs ice-surge-*: coyote tan and olive drab)
PATCH, PATCH_INK = (30, 30, 32), (236, 196, 54)               # black patches, yellow letters


def ice_vest(p, view, sp):
    col = sp.get('vest', VEST_TAN)
    dark = mix(col, (0, 0, 0), 0.35)
    l, r = PC._torso_box(view, sp)
    l2, r2 = PC._torso_box(view, sp, 470)
    p.poly(rough([(l + 14, 36), (r - 14, 36), (r - 4, 120), (r - 4, 200), (r2 - 6, 470), (l2 + 6, 470), (l + 4, 200),
                  (l + 4, 120)], 3, 5), col, INK, 2.4)
    if view in ('front', 'three'):
        o = 0 if view == 'front' else 0.3 * sp.get('shoulders', 150)
        p.poly([(l + 30, -2), (l + 80, -2), (l + 70, 60), (l + 30, 60)], col, INK, 2.0)       # shoulder straps
        p.poly([(r - 80, -2), (r - 30, -2), (r - 30, 60), (r - 70, 60)], col, INK, 2.0)
        for k in range(3):                                                                    # pouches
            x = l + 34 + k * (r - l - 68) / 3
            p.poly([(x, 340), (x + (r - l - 90) / 3, 340), (x + (r - l - 90) / 3, 445), (x, 445)], dark, INK, 1.6)
        PC._patch(p, o, 132, (r - l) * 0.62, 50, 'POLICE', PATCH, PATCH_INK)
        PC._patch(p, o, 210, (r - l) * 0.3, 40, 'ICE', PATCH, PATCH_INK)
        PC.body_cam(p, o + (r - l) * 0.26, 270)
    elif view in ('back', 'three_back'):
        PC._patch(p, (l + r) / 2, 170, (r - l) * 0.66, 56, 'POLICE', PATCH, PATCH_INK)
        PC._patch(p, (l + r) / 2, 240, (r - l) * 0.36, 46, 'ICE', PATCH, PATCH_INK)
    else:
        p.poly([(r - 54, 330), (r + 6, 330), (r + 6, 440), (r - 54, 440)], dark, INK, 1.6)
        PC._patch(p, -10, 150, 90, 40, 'ICE', PATCH, PATCH_INK)               # the side panel


def mask(p, view, sp, hx, hy):
    """A face mask pulled up to just under the eyes, over the nose and down round the neck."""
    hw, hh = sp.get('hw', 72), sp.get('hh', 90)
    col = sp.get('mask', (26, 26, 30))
    if view in ('back', 'three_back'):
        p.poly(curve([(hx - hw * 0.98, hy + 4), (hx + hw * 0.98, hy + 4), (hx + hw * 0.9, hy + hh * 0.9),
                      (hx + 46, hy + hh * 1.35), (hx - 46, hy + hh * 1.35), (hx - hw * 0.9, hy + hh * 0.9)], 3), col, INK, 2.4)
        return
    if view == 'side':
        pts = [(hx - hw * 0.55, hy + 10), (hx + hw * 0.5, hy + 8), (hx + hw * 1.06, hy + 14), (hx + hw * 1.1, hy + hh * 0.45),
               (hx + hw * 0.92, hy + hh * 0.86), (hx + 34, hy + hh * 1.32), (hx - 40, hy + hh * 1.32),
               (hx - hw * 0.62, hy + hh * 0.7)]
        p.poly(curve(pts, 3), col, INK, 2.4)
        return
    fx = hx + (0.4 * hw if view == 'three' else 0.0)
    pts = [(hx - hw * 1.03, hy + 2), (fx - hw * 0.3, hy + 10), (fx, hy + 4), (fx + hw * 0.3, hy + 10), (hx + hw * 1.03, hy + 2),
           (hx + hw * 0.96, hy + hh * 0.62), (hx + hw * 0.6, hy + hh * 0.95), (hx + 46, hy + hh * 1.34),
           (hx - 46, hy + hh * 1.34), (hx - hw * 0.6, hy + hh * 0.95), (hx - hw * 0.96, hy + hh * 0.62)]
    p.poly(curve(pts, 3), col, INK, 2.4)
    p.line([(fx, hy + 8), (fx, hy + hh * 0.5)], mix(col, (255, 255, 255), 0.12), 2.0)   # the nose's ridge


def cap(p, view, sp, hx, hy):
    """A plain dark baseball cap, pulled low."""
    hw, hh = sp.get('hw', 72), sp.get('hh', 90)
    col = sp.get('cap_c', (30, 32, 40))
    dark = mix(col, (0, 0, 0), 0.4)
    top, b1 = hy - hh * 1.1, hy - hh * 0.5
    if view == 'side':
        p.poly(curve([(hx - hw * 1.02, b1), (hx - hw * 0.96, hy - hh * 0.95), (hx - hw * 0.2, top), (hx + hw * 0.7, hy - hh * 0.98),
                      (hx + hw * 1.0, b1)], 3), col, INK, 2.4)
        p.poly(curve([(hx + hw * 0.8, b1 - 4), (hx + hw * 1.6, b1 + 8), (hx + hw * 1.54, b1 + 16), (hx + hw * 0.86, b1 + 8)], 3),
               dark, INK, 2.2)
        return
    o = 0.0 if view in ('front', 'back') else (0.2 * hw if view == 'three' else -0.2 * hw)
    p.poly(curve([(hx - hw * 1.0, b1), (hx - hw * 0.94, hy - hh * 0.9), (hx - hw * 0.5 + o, top + 6), (hx + o, top),
                  (hx + hw * 0.5 + o, top + 6), (hx + hw * 0.94, hy - hh * 0.9), (hx + hw * 1.0, b1)], 3), col, INK, 2.4)
    p.line([(hx + o, top + 4), (hx + o * 1.4, b1 - 4)], dark, 1.8)
    if view in ('front', 'three'):
        p.poly(curve([(hx - hw * 0.8 + o, b1 - 2), (hx + o * 1.5, b1 + 4), (hx + hw * 0.8 + o * 2, b1 - 2),
                      (hx + hw * 0.66 + o * 2, b1 + hh * 0.2), (hx + o * 1.5, b1 + hh * 0.26),
                      (hx - hw * 0.66 + o, b1 + hh * 0.2)], 3), dark, INK, 2.2)


# ---------------------------------------------------------------------------------------------- the cast
def _officer(name, skin, top, legs, vest, mask_c, shoulders, height, hw=72, hh=90, **kw):
    return dict(name=name, skin=skin, hw=hw, hh=hh, jaw='square', hair='crop', hair_c=(40, 32, 28), brow_c=(40, 32, 28),
                outfit='jumper', jacket=top, sleeve=top, trousers=legs, shoe=(30, 28, 26), shoulders=shoulders,
                vest=vest, mask=mask_c, cap_c=(30, 32, 40), glove=(26, 26, 30), mouth='set', brows='serious',
                height=height, full=True, pose='custom', seed=hash(name) % 97, **kw)


CAST = {'O1': _officer('ICE officer 1', B.PALE, (124, 126, 132), (96, 96, 78), VEST_TAN, (26, 26, 30), 170, 1.88,
                       hw=76),                                     # big; a grey hoodie, cargo trousers
        'O2': _officer('ICE officer 2', B.PINK, (44, 48, 58), (52, 72, 112), VEST_OLIVE, (150, 128, 96), 150, 1.80,
                       hw=68),                                     # lean; a dark jacket, jeans
        'O3': _officer('ICE officer 3', B.OLIVE, (74, 76, 82), (74, 74, 62), VEST_OLIVE, (26, 26, 30), 160, 1.83),
        'O4': _officer('ICE officer 4', B.PALE, (40, 46, 72), (40, 52, 84), VEST_TAN, (72, 74, 80), 178, 1.86,
                       hw=78, hh=92)}                              # heavy; a navy hoodie, dark jeans
# The man (invented, Hispanic, about 30): a tan canvas work jacket, jeans, work boots, short black hair.
# Sam, 9 Nov: older, Latino, moustached, thin: about 60, greying, lined, a long thin face, narrow shoulders.
MAN = dict(name='The man on the ground', skin=(176, 122, 84), hw=62, hh=94, jaw='long', hair='crop', hair_c=(112, 106, 100),
           brow_c=(90, 84, 80), age=True, creases=2, outfit='jumper', jacket=(168, 124, 70), sleeve=(168, 124, 70),
           trousers=(58, 78, 118), shoe=(96, 64, 36), shirt=(230, 226, 214), shoulders=126, height=1.70, full=True,
           pose='custom', seed=91)
TACHE = (120, 112, 104)                                            # a grey-brown moustache


OPEN = {'AI': 20.0, 'O': 16.0, 'E': 12.0, 'etc': 10.0, 'L': 10.0, 'U': 8.0, 'WQ': 8.0, 'FV': 4.0}   # side-on mouth
# opening by sound (Sam, 9 Nov: "better mouth movement": the kit's side-on head draws one small square for every sound)


def tache(p, view, sp, hx, hy):
    """His moustache (the kit has none for a plain face): a full one over the upper lip, front and side on. Side on it
    comes with his own mouth, drawn first: open by the sound being said (OPEN), teeth showing; closed, a line."""
    hw = sp.get('hw', 70)
    if view == 'side':
        m = str(sp.get('mouth', 'rest'))
        h = OPEN.get(m[2:], 0.0) if m.startswith('v:') else 0.0
        if h > 0:
            y0 = hy + 50
            p.poly(curve([(hx + 40, y0), (hx + 70, y0 - 2), (hx + 68, y0 + h), (hx + 52, y0 + h + 3), (hx + 40, y0 + h * 0.6)], 3),
                   (110, 28, 36), INK, 2.0)
            p.poly([(hx + 50, y0 + 1), (hx + 68, y0), (hx + 67, y0 + 4), (hx + 50, y0 + 5)], (244, 240, 230), None)
        else:
            p.line([(hx + 44, hy + 56), (hx + 66, hy + 54)], INK, 2.4)
        p.poly(curve([(hx + hw * 0.35, hy + 34), (hx + hw * 0.98, hy + 30), (hx + hw * 1.04, hy + 40),
                      (hx + hw * 0.9, hy + 50), (hx + hw * 0.4, hy + 46)], 3), TACHE, INK, 1.6)
    elif view in ('front', 'three'):
        fx = hx + (0.4 * hw if view == 'three' else 0.0)
        p.poly(curve([(fx - 34, hy + 50), (fx - 10, hy + 36), (fx, hy + 38), (fx + 10, hy + 36), (fx + 34, hy + 50),
                      (fx + 22, hy + 54), (fx, hy + 46), (fx - 22, hy + 54)], 3), TACHE, INK, 1.6)


def dress(j, sp):
    j['body_props'] = [ice_vest]
    j['head_props'] = [mask, cap]
    return j


# ---------------------------------------------------------------------------------------------- the man on the ground
def balled(sp):
    """Curled into a ball on his right side (brief 30), facing us: knees drawn up to his chest, both arms wrapped
    over his head, the head tucked down between them. (lying.curled with the arms over the head.)"""
    X = (0, -1, 0)
    hc = 0.82 * sp.get('shoulders', 150) * LY.M
    arms = {'R': ((0.74, 0.07, 0.2), (0.0, 0.3, 1.0)),              # the lower arm along the snow round his face
            'L': ((0.78, 0.3, 0.06), (0.1, 1.0, 0.5))}              # the upper one over the top of his head
    legs = {'R': ((-0.02, 0.055, 0.42), (0.4, 0.0, 1.0), (-0.9, 0, 0.3), (0, 0, -1)),
            'L': ((0.06, 0.2, 0.44), (0.5, 0.4, 1.0), (-0.9, -0.2, 0.4), (0, 0.3, -1))}
    k = LY._build((0, hc * B.HEM, 0), (0.22, hc * 0.95, 0.07), (0.58, hc, 0.1), X, (1, -0.3, 0.6),
                  (-0.1, -0.2, 1), arms, legs, sp, shrug={'R': (0.115, 0.07)})
    return LY._head_down(k, sp)


LY.POSES['ball'] = balled
LY.RESTS['ball'] = ['chest', 'pelvis', 'head', 'hair', 'thighR']


@functools.lru_cache(maxsize=1)
def man_body():
    """(Body, surfaces): lying at MAN_AT, his head to our left (towards Vance), his front to us."""
    return LY.lie(MAN, 'ball', MAN_AT[0], MAN_AT[1], 180.0)


def man_faults():
    k, surf = man_body()
    return LY.contact_faults(k, MAN, 'ball', surf, 'the man on the ground')


# ---------------------------------------------------------------------------------------------- the beating
def hit_times(off, t0=-3.0, t1=60.0):
    n0 = math.floor((t0 - off) / PERIOD)
    return [off + n * PERIOD for n in range(n0, int((t1 - off) / PERIOD) + 1)]


def _phase(t, off):
    """(the next strike's time, the last one's)."""
    n = math.floor((t - off) / PERIOD + 0.55)                        # the swing starts 0.55 periods before its hit
    return off + n * PERIOD, off + (n - 1) * PERIOD


def kick_pose(sp, t, off):
    """A low kick down into him (brief 30: kick): the knee chambers, the boot drives forward and down into his back,
    held a beat, back; arms out for balance, gloved fists."""
    th, _ = _phase(t, off)
    j, _ = moves.kick(sp, t, th, height=810.0, side='R')       # his upper back, 0.18 m up (he lies flat)
    sw = sp.get('shoulders', 150)
    V.arm_to(j, 'L', (-(sw + 60), 300.0, 60.0), 'out', 'fist')
    V.arm_to(j, 'R', (sw + 20, 320.0, -90.0), 'out', 'fist')
    j['lean'] = j.get('lean', 0) * 0.6 + 4
    return dress(j, sp)


def _unlean(y, z, lean):
    """The torso-frame point (y, z) that the pose's `lean` (degrees forward about the hips) carries to (y, z)."""
    L = math.radians(lean)
    dy = y - V.HIP_Y
    return V.HIP_Y + dy * math.cos(L) - z * math.sin(L), dy * math.sin(L) + z * math.cos(L)


CROUCH = 160.0                                                    # person units (0.24 m)


def kneel_punch_pose(sp, t, off):
    """Kneeling beside him, punching down on his hips (he lies flat: a standing punch can't reach). Knees on the
    snow, leaning over him: the fist pulled up by the shoulder, driven down, held, back."""
    th, _ = _phase(t, off)

    def kneel(lean, fist):
        j = V.standing(sp)
        j['bob'] = 218.0
        fl = 928 - 218.0
        for s_, sg in (('L', -1), ('R', 1)):
            j['foot' + s_] = (sg * 55, fl - 38, -230.0)
            j['knee_pole' + s_] = (0.0, 1.0, 1.0)
            j['toe' + s_] = 0.0
        j['lean'] = lean
        y, z = _unlean(*fist, lean)
        V.arm_to(j, 'R', (40.0, y, z), 'down', 'fist')
        y, z = _unlean(560.0, 160.0, lean)
        V.arm_to(j, 'L', (-40.0, y, z), 'out', 'fist')            # braced on his thigh
        return j
    back = kneel(20, (120.0, -60.0))
    hit = kneel(46, (590.0, 330.0))                               # down on his hips: 0.2 m off the snow
    j = moves.keyed(t, [(th - 0.75, hit), (th - 0.36, back), (th - 0.2, back), (th, hit), (th + 0.2, hit), (th + 0.62, hit)],
                    curve='fast' if th - 0.2 <= t < th else 'ease')
    return dress(j, sp)


def punch_pose(sp, t, off, h=0.58):
    """Bent over him, punching down (brief 30: punch; side on, where a downward blow reads): the fist pulled back
    by the shoulder, driven down into his side, a held impact, back; the other hand braced on his own knee."""
    th, _ = _phase(t, off)
    sw = sp.get('shoulders', 150)

    def bent(lean, fist):
        j = V.standing(sp)
        j['lean'] = lean
        y, z = _unlean(*fist, lean)
        V.arm_to(j, 'R', (40.0, y, z), 'down', 'fist')
        y, z = _unlean(640.0, 120.0, lean)
        V.arm_to(j, 'L', (-40.0, y, z), 'out', 'fist')            # braced on his own knee
        j['bob'] = CROUCH                                         # knees bent, down over him
        j['footR'] = (60, V.ANKLE_Y - CROUCH, -60.0)              # the back foot planted behind
        j['footL'] = (-60, V.ANKLE_Y - CROUCH, 110.0)
        return j
    back = bent(24, (200.0, -110.0))                              # (leaned y, z: up by the shoulder, pulled back)
    hit = bent(48, ((928 - CROUCH) - h / V.M_PER_UNIT, 330.0))   # straight down onto him, h metres off the snow
    j = moves.keyed(t, [(th - 0.75, hit), (th - 0.36, back), (th - 0.2, back), (th, hit), (th + 0.2, hit), (th + 0.62, hit)],
                    curve='fast' if th - 0.2 <= t < th else 'ease')
    return dress(j, sp)


def stomp_pose(sp, t, off):
    """Facing us from behind him, stamping down on his back (brief 30: kick): the knee lifted high, the boot driven
    down onto him, held, back; arms out for balance. Front on, his POLICE ICE vest reads."""
    th, _ = _phase(t, off)
    sw = sp.get('shoulders', 150)
    rest = V.standing(sp)
    lift = V.standing(sp)
    lift['footR'] = (50.0, 600.0, 170.0)
    lift['lean'] = -4
    down = V.standing(sp)
    down['footR'] = (40.0, 860.0, 430.0)                           # onto him: 0.65 m in front, 0.1 m up (he lies flat)
    down['lean'] = 8
    for j in (rest, lift, down):
        V.arm_to(j, 'L', (-(sw + 90), 300.0, 40.0), 'out', 'fist')
        V.arm_to(j, 'R', (sw + 90, 300.0, 40.0), 'out', 'fist')
    j = moves.keyed(t, [(th - 0.8, down), (th - 0.32, lift), (th - 0.18, lift), (th, down), (th + 0.2, down), (th + 0.62, down)],
                    curve='fast' if th - 0.18 <= t < th else 'ease')
    return dress(j, sp)


MOVES = {'kick': lambda sp, t, off: kick_pose(sp, t, off), 'punch': kneel_punch_pose, 'stomp': stomp_pose,
         'punch_hi': lambda sp, t, off: punch_pose(sp, t, off, h=0.47)}


def officer_pose(o, t):
    name, x, d, yaw, move, off = o
    sp = CAST[name]
    return MOVES[move](sp, t, off)


def flinch(t):
    """How hard he is flinching (0-1): a jolt on every blow, settling in 0.3 s (he flinches on every blow, Street 4)."""
    out = 0.0
    for o in OFFICERS:
        th, last = _phase(t, o[5])
        for h in (th, last):
            u = t - h
            if 0 <= u < 0.35:
                out = max(out, math.exp(-u / 0.1))
    return out


def impacts(t):
    """Each blow's shove on him (Sam, 9 Nov: he barely reacted): (metres right, metres nearer us, 0-1 strength),
    summed: up in two drawings, easing off over 0.3 s, the way the blow came."""
    dx = dz = e = 0.0
    for o in OFFICERS:
        th, last = _phase(t, o[5])
        for h in (th, last):
            u = t - h
            if 0 <= u < 0.45:
                k = min(1.0, u / 0.08) * math.exp(-max(0.0, u - 0.08) / 0.14)
                px, pz = PUSH[o[0]]
                dx, dz, e = dx + px * k, dz + pz * k, max(e, k)
    return dx, dz, e


def knock(t):
    """How far a blow has pushed his raised hand down (0-1): a ramp up over 0.14 s after each blow, easing off over
    0.35 s (Sam, 9 Nov: the arm snapped; the body's own jolt, flinch(), stays instant)."""
    out = 0.0
    for o in OFFICERS:
        th, last = _phase(t, o[5])
        for h in (th, last):
            u = t - h
            if 0 <= u < 0.49:
                out = max(out, u / 0.14 if u < 0.14 else math.exp(-(u - 0.14) / 0.15))
    return out


def blood(img, cam, t, t0):
    """Some blood (Q18): a small red patch on the snow by his head and a few drops, growing a little."""
    hx, hz = MAN_AT[0] - 0.7, MAN_AT[1] + 0.05                      # by his head on the snow
    g = 0.7 + 0.3 * min(1.0, max(0.0, (t - t0) / 6.0))
    lay = layer()
    pen = Pen(lay)
    r = random.Random(950)
    ring = [(hx - 0.08 + 0.17 * g * math.cos(a) * r.uniform(0.75, 1.1), -0.16 + hz + 0.1 * g * math.sin(a) * r.uniform(0.7, 1.1), 0.003)
            for a in np.linspace(0, 6.28, 14, endpoint=False)]
    pen.poly(_q(cam, ring), (176, 24, 30), 0)
    for i in range(6):
        x, dd = hx - 0.35 + r.uniform(-0.25, 0.3), hz - 0.25 + r.uniform(-0.15, 0.1)
        rad = r.uniform(0.012, 0.03) * (0.8 + 0.2 * g)
        pen.poly(_q(cam, [(x + rad * math.cos(a), dd + rad * 0.6 * math.sin(a), 0.003) for a in np.linspace(0, 6.28, 8)]),
                 (170, 22, 28), 0)
    img.alpha_composite(shrink(lay))


def _shadow(img, cam, x, d, w=0.36):
    """A soft flat shadow on the snow under someone standing (grey day: just a smudge where they touch)."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ring = [cam.p(x + w * math.cos(a), d + 0.2 * math.sin(a), 0.0) for a in np.linspace(0, 6.28, 20)]
    ImageDraw.Draw(lay).polygon(ring, fill=(70, 80, 100, 50))
    img.alpha_composite(lay)


def _person(img, cam, sp, x, d, yaw, j):
    B.SS = 1                                                       # (the film's drawing size: 1 = full frame)
    sx, sy, ppm = place(cam, x, d)
    s = 928 * V.M_PER_UNIT * sp['height'] / 1.75 * ppm / 928
    return V.person(img, B.Cam(1.0, 540, 960), sx, sy - 928 * s, s, dict(sp, mood='angry'), 0.0, yaw, j)


PLEAD = 1.9                                                       # seconds between his tries


def plead(k, t, f=0.0):
    """Sam, 8 Nov (note 48): he weakly tries to raise his hands to make them stop. His upper hand comes up off his
    head, open, held out towards them, trembling; it sags and drops back as a blow lands, then tries again. The
    lower forearm lifts a little off the snow with it. Bones keep their length (solved again each frame)."""
    u = (t % PLEAD) / PLEAD
    r = (0.5 - 0.5 * math.cos(2 * math.pi * min(1.0, u / 0.8))) if u < 0.8 else 0.0   # up slowly, then back
    r *= 0.85 * (1 - 0.8 * f)                                     # a blow knocks it down
    if r < 0.02:
        return k
    k = k.copy()
    tremble = np.array([0.0, 0.012 * math.sin(t * 2 * math.pi * 7.0), 0.008 * math.sin(t * 2 * math.pi * 5.0 + 1)])
    sh = k['shL']
    raised = sh + np.array([-0.16, 0.46, -0.3]) + tremble         # up over his shoulder, out towards us and them
    tgt = k['wrL'] * (1 - r) + raised * r
    pole0 = k['elL'] - (sh + k['wrL']) / 2                        # which way his elbow points now, curled up:
    pole0 = pole0 / (np.linalg.norm(pole0) + 1e-9)                # blended into the lifting arm's, so the bend never
    pole1 = np.array([0.2, -0.4, -1.0]) / 1.1                     # flips (Sam, 9 Nov: the arm twisted impossibly)
    pole = (1 - min(1.0, 3 * r)) * pole0 + min(1.0, 3 * r) * pole1
    k['elL'], k['wrL'] = LY.limb(sh, tgt, LY.UPPER, LY.FORE, pole)
    tgt = k['wrR'] + np.array([0.0, 0.08 * r, -0.04 * r])
    k['elR'], k['wrR'] = LY.limb(k['shR'], tgt, LY.UPPER, LY.FORE, k['elR'] - (k['shR'] + k['wrR']) / 2)
    return k


MAN_FACE = [None]                                                 # the man's face for this drawing (mouth, blink)


def beg(k, t, t0, face=None):
    """Sam, 9 Nov (the ending): he lifts his head off the snow and turns it up to Vance (to our left), the upper arm
    reaching out towards him, open hand: "Please, sir, help me." Eased in over 0.5 s from t0; the bend blended from
    the curled arm (no flip: note 52a)."""
    u = min(1.0, max(0.0, (t - t0) / 0.5))
    u = u * u * (3 - 2 * u)
    MAN_FACE[0] = {q: face[q] for q in ('mouth', 'blink') if q in face} if face else None
    if u <= 0:
        return k
    k = k.copy()
    to = np.array([-0.47, 0.5, -0.71])                            # from his head towards Vance's face
    hf0 = k['hfwd']
    hf = hf0 * (1 - u) + to * u
    hf = hf / np.linalg.norm(hf)
    up = np.array([0.0, 1.0, 0.0])
    hu = k['hup'] * (1 - u) + (up - hf * (up @ hf)) * u
    k['hfwd'], k['hup'] = hf, hu / np.linalg.norm(hu)
    lift = np.array([0.0, 0.07 * u, 0.0])                         # the head raised a little off the snow
    k['head'] = k['head'] + lift
    sh = k['shL']
    tremble = np.array([0.0, 0.01 * math.sin(t * 2 * math.pi * 6.0), 0.0])
    tgt = k['wrL'] * (1 - u) + (sh + np.array([-0.18, 0.46, -0.3]) + tremble) * u   # up towards him, clear of the boots
    pole0 = k['elL'] - (sh + k['wrL']) / 2
    pole0 = pole0 / (np.linalg.norm(pole0) + 1e-9)
    pole = pole0 * (1 - u) + np.array([0.0, -0.6, -0.8]) * u
    k['elL'], k['wrL'] = LY.limb(sh, tgt, LY.UPPER, LY.FORE, pole)
    return k


# ---- the man on the ground, flat (Sam, 9 Nov: the 3D body read as "a nightmarish balloon creature"): the same flat
# cartoon person as everyone else, drawn side on facing left in a seated pose (thighs level, shins down) and turned a
# quarter turn, so he kneels curled face down, his head to our left (towards Vance), knees under him, shins flat on
# the snow behind: the turtle a man being beaten curls into. Arms wrapped over the back of his head, elbows by his face.
def _lerp3(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


# Sam, 9 Nov (later): flat on the ground throughout. The flat drawing side on facing left, turned a quarter turn: he
# lies on his front, head to our left (towards Vance), arms over his head; during his line his head comes up and one
# arm rises weakly towards Vance.
def man_j(t, squash=0.0, beg=0.0):
    """Prone (before the quarter turn): arms up over his head (on the snow beyond it). A blow squashes him (squash);
    beg (0-1): his head lifts to look at Vance and his near arm rises weakly towards him, trembling."""
    j = V.standing(MAN)
    j['footL'] = (-60.0, V.ANKLE_Y, -30.0)                       # legs a little apart
    # (Sam, 9 Nov, twice: both arms on one side.) A hand each side of his head: the near one by his face (on the snow
    # side, drawn over the face), the far one over the back of his head (the sky side, behind it)
    V.arm_to(j, 'L', (-20.0, -200.0, 70.0), (0.0, 1.0, 0.6), 'fist')   # (on the snow, never below it)
    V.arm_to(j, 'R', (20.0, -235.0, -70.0), (0.0, 0.5, -1.0), 'fist')
    j['on_face'] = {'L'}
    j['head_dy'] = -18.0                                          # his neck shows
    tr = 8.0 * math.sin(t * 2 * math.pi * 6.0)
    if beg > 0.01:                                                # the face-side arm reaches out along the snow towards
        V.arm_to(j, 'L', _lerp3((-20.0, -200.0, 70.0), (-30.0, -340.0 + tr, 60.0 - 40.0 * beg), beg), (0.0, 1.0, 0.6),
                 'palm')                                          # Vance, below his face, lifted a little, trembling
        if beg > 0.4:
            j['on_face'] = set()                                  # (under his face now: his mouth must show)
    j['head_lean'] = -46.0 * beg + 6.0 * squash                    # a blow drives his face down
    j['head_props'] = [tache]
    return j


def man_draw(img, cam, t, beg_from=None, face=None):
    """Draw him at MAN_AT through `cam`, lying flat: shoved by each blow, eyes squeezed shut on the impact."""
    d = MAN_AT[1]
    ppm = cam.ppm(d)
    s = 928 * V.M_PER_UNIT * MAN['height'] / 1.75 * ppm / 928
    B.SS = 1
    sp = dict(MAN, **{q: v for q, v in (face or {}).items() if q in ('mouth', 'blink')})
    sp['mood'] = 'scared'
    dx, dz, e = impacts(t)                                      # (Sam, 9 Nov: they keep attacking in the ending too)
    if e > 0.35:
        sp['blink'] = True                                      # eyes squeezed shut as it lands
    beg = 0.0
    if beg_from is not None:
        u = min(1.0, max(0.0, (t - beg_from) / 0.6))
        beg = 0.8 * u * u * (3 - 2 * u)                          # weakly: never the whole way
    n = int(1500 * s) + 40
    c = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    ny = n * 0.28                                                # his neck on the canvas
    import handcheck
    was = handcheck.ACTIVE[0]
    handcheck.ACTIVE[0] = False       # he is drawn on his own small canvas, turned afterwards: the hand check expects
    try:                              # every person on the full frame; his hands looked at full size by hand (9 Nov)
        V.person(c, B.Cam(1.0, 540, 960), n / 2, ny, s, sp, 0.0, -90, man_j(t, e, beg))
    finally:
        handcheck.ACTIVE[0] = was
    r = c.rotate(90, resample=Image.BICUBIC)                     # a quarter turn about the canvas middle:
    # (x, y) goes to (n/2 + y - n/2, n/2 - x + n/2). Placed by his BODY, not by whatever is lowest (Sam, 9 Nov: he
    # hovered: a hand reaching below him was set on the snow): the front of his chest (0.66 of the shoulders out, the
    # side view's torso) lies on the snow, his hips at MAN_AT.
    ground = n / 2 + 0.66 * MAN['shoulders'] * s
    hip_x = n / 2 + (ny + 460.0 * s - n / 2)
    gx, gy = cam.p(MAN_AT[0] + dx + 0.12, d - dz, 0.0)
    _shadow(img, cam, MAN_AT[0], d, 0.9)
    img.alpha_composite(r, (int(round(gx - hip_x)), int(round(gy - ground))))


def draw_group(img, cam, t, t0=0.0, man=None):
    """The beating: the two behind him, the blood and the man, then the two kicking from either end (far to near)."""
    order = sorted(OFFICERS, key=lambda o: -o[2])
    back = [o for o in order if o[2] > MAN_AT[1] + 0.2]
    front = [o for o in order if o not in back]
    for o in back + front:
        _shadow(img, cam, o[1], o[2])
    pose = lambda o: officer_pose(o, t)                       # (they keep at it in the ending too: Sam, 9 Nov)
    for o in back:
        _person(img, cam, CAST[o[0]], o[1], o[2], o[3], pose(o))
    blood(img, cam, t, t0)
    beg_from, face = (man[1], man[2]) if man else (None, None)   # man=('beg', from, face): the ending
    man_draw(img, cam, t, beg_from, face)
    for o in front:
        _person(img, cam, CAST[o[0]], o[1], o[2], o[3], pose(o))


# ---------------------------------------------------------------------------------------------- rule 3: the references
BENCHMARK = [
    dict(place='The street (Minneapolis, winter)', refs=['street-lake-800.jpg', 'street-uptown-winter.jpg',
                                                         'street-lake-bloomington.jpg'], at=5.5,
         items=[('two- and three-storey brick commercial blocks, flat roofs, a stone parapet', 'done: 5 blocks, 8-11 m'),
                ('shops below: big plate-glass windows, a recessed door, a sign band', 'done: made-up names, no brands'),
                ('canvas awnings over the shop windows, striped valances', 'done: 5 colourings'),
                ('flats above: rows of tall sash windows on stone sills', 'done: sash rail, sills'),
                ('black street lamps: a tall pole, a curved arm, a lantern', 'done: two'),
                ('bare winter trees, grey, fine branches', 'done: two on the far pavement'),
                ('a flat white-grey overcast sky; wires over the street', 'done: grey bands, two wires'),
                ('a ploughed road: packed snow, grey-brown wheel ruts, slush', 'done: four ruts, clods'),
                ('waist-high snowbanks along both kerbs', 'done: near one behind the people'),
                ('snow on ledges, sills, awnings and the parapets', 'done; light snow falling (Q22)')]),
]


# ---------------------------------------------------------------------------------------------- sheets
def frame(t=1.0, z=1.0, focus=None, to=None, vance=None):
    cam = cam_at(z, focus, to)
    im = paint(cam)
    snow(im, cam, t, (7.6, 17.0))
    draw_group(im, cam, t)
    if vance:
        vance(im, cam, t)
    snow(im, cam, t, (3.0, 7.6))
    return im


def _vance(im, cam, t):
    import ad_vanced_notice_cast as AC
    import ad_vanced_notice_comp as CP
    CP.setup()
    sx, sy, ppm = place(cam, *VANCE_AT)
    _shadow(im, cam, *VANCE_AT)
    CP.person(im, AC.VANCE, sx, sy, ppm, 0, V.standing(AC.VANCE), mood='proud', mouth='rest')


def sheet(out):
    """The shot wide at four moments of the beating, and the cast in their gear (front and side)."""
    tiles = [(f'{t:.2f} s', frame(t, vance=_vance)) for t in (0.0, 0.34, 0.68, 1.02)]
    cast = Image.new('RGBA', (W, H), (226, 226, 230, 255))
    for i, (nm, sp) in enumerate(CAST.items()):
        for k, yaw in enumerate((0, 90)):
            j = dress(V.standing(sp), sp)
            x = 140 + i * 270 + (k * 110 - 55)
            V.person(cast, B.Cam(1.0, 540, 960), x, 300 + k * 760, 0.42, dict(sp, mood='angry'), 0.0, yaw, j)
    tiles.append(('the officers', cast))
    tw, th = 352, 626
    sh = Image.new('RGB', (3 * tw + 32, 2 * (th + 40) + 24), (226, 222, 214))
    for i, (lab, im) in enumerate(tiles):
        t = Image.new('RGB', (tw, th + 40), (20, 20, 24))
        t.paste(im.convert('RGB').resize((tw, th), Image.LANCZOS), (0, 40))
        ImageDraw.Draw(t).text((8, 8), lab, fill=(255, 255, 255))
        sh.paste(t, (8 + (i % 3) * (tw + 8), 8 + (i // 3) * (th + 48)))
    sh.save(out, quality=86)
    return out


def beat_clip(out, secs=2.8, fps=12):
    import subprocess
    import tempfile
    tmp = tempfile.mkdtemp()
    for n in range(int(secs * fps)):
        frame(n / fps, vance=_vance).convert('RGB').resize((540, 960)).save(f'{tmp}/f{n:04d}.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', f'{tmp}/f%04d.png', '-c:v',
                    'libx264', '-pix_fmt', 'yuv420p', '-crf', '28', out], check=True)
    return out


if __name__ == '__main__':
    print({'sheet': sheet, 'beat': beat_clip}[sys.argv[1]](sys.argv[2]))
