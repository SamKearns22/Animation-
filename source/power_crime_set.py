#!/usr/bin/env python3
"""Power Crime Action: the sets, each built once in 3D (metres, y up) and seen through cameras (guides/satire.md,
'One set, one plan'): Trafalgar Square (refs aerial-1..3, from-steps-1, gallery-1, column-*, lion-*, fountain-1),
the Met's TSG van (refs van-*), the interrogation room (refs interrogation-1..3) and the custody corridor (ref
corridor).

The square: Nelson's Column at the origin; north is +z (the National Gallery's terrace and steps), east is +x. The
fountains sit either side just north of the column; the paving runs north to the terrace wall; roads on the south,
east and west with buses; cream stone buildings all round; Big Ben far down Whitehall to the south.

    python3 source/power_crime_set.py test OUT_DIR      a still of each set from its main camera (working pictures)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import views as V                # noqa: E402
from ed import INK, curve        # noqa: E402
from satire_style import rough   # noqa: E402
from poker_mon_room import Cam3  # noqa: E402  the perspective camera (shared)

FLAT = B.Cam(1.0, 540, 960)
M_UNIT = V.M_PER_UNIT

# ------------------------------------------------------------------------------------------------ colours
SKY, CLOUD, CLOUD_D, CLOUD_G = (176, 194, 212), (248, 248, 250), (226, 230, 236), (190, 196, 206)   # overcast
PAVE, PAVE_D, PAVE_L = (196, 192, 184), (150, 146, 138), (210, 206, 198)
STONE, STONE_D = (226, 214, 190), (196, 182, 156)            # the cream Portland stone of the buildings
STONE_G, STONE_GD = (200, 200, 198), (172, 172, 170)          # the pale grey granite of the column and walls
SAND, SAND_D = (214, 176, 108), (178, 140, 76)                # the fountains' golden sandstone
WATER, WATER_D, WATER_L = (64, 190, 196), (40, 150, 160), (176, 232, 236)
BRONZE, BRONZE_D, BRONZE_L = (52, 58, 54), (34, 38, 36), (96, 104, 96)
WINDOW, WINDOW_D = (70, 84, 100), (48, 58, 70)
ROAD, ROAD_L = (78, 80, 86), (236, 236, 230)
BUS, BUS_D = (206, 30, 36), (160, 20, 26)
TREE, TREE_D = (80, 132, 70), (58, 100, 52)
IRON = (28, 28, 32)


def _pen(img):
    return B.Pen(img, FLAT)


def quad(img, cam, pts, fill, line=INK, lw=1.8):
    cam.poly(_pen(img), pts, fill, line, lw)


def box(img, cam, x0, x1, y0, y1, z0, z1, top, side, front, line=INK, lw=1.8):
    """A box's visible faces, drawn far to near."""
    faces = []
    c = cam.pos
    if c[1] > y1:
        faces.append(([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], top))
    if c[0] < x0:
        faces.append(([(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], side))
    if c[0] > x1:
        faces.append(([(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], side))
    if c[2] < z0:
        faces.append(([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], front))
    if c[2] > z1:
        faces.append(([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], front))
    for pts, col in sorted(faces, key=lambda f: -cam.depth(tuple(sum(q[i] for q in f[0]) / 4 for i in range(3)))):
        quad(img, cam, pts, col, line, lw)


def cylinder(img, cam, cx, cz, y0, y1, r0, r1, col, col_d, n=28, flutes=0, line=INK):
    """An upright cylinder (or cone): its silhouette, a flat shadow side away from the light (the east), its top."""
    if min(cam.depth((cx, y, cz)) for y in (y0, y1)) < max(r0, r1) + 0.4:
        return                                                   # behind or around the camera: not drawn
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    bot = [(cx + r0 * math.cos(a), y0, cz + r0 * math.sin(a)) for a in ang]
    top = [(cx + r1 * math.cos(a), y1, cz + r1 * math.sin(a)) for a in ang]
    to_cam = math.atan2(cam.pos[2] - cz, cam.pos[0] - cx)
    side = []
    for i in range(n):
        a = ang[i]
        d = math.cos(a - to_cam)
        if d > -0.05:
            side.append(i)
    p = _pen(img)
    if not side:
        return
    # the outline of the visible half: left edge up, across the top, right edge down
    lo = [cam.project(q)[0] for q in bot]
    hi = [cam.project(q)[0] for q in top]
    pts2 = lo + hi
    xs = [q[0] for q in pts2]
    # silhouette: the convex hull of the projected rims
    hull = V._hull(pts2)
    p.poly(hull, col, line, 2.0)
    for i in side:                                               # the shadow side: away from the sun (south-west)
        a = ang[i]
        if math.cos(a - math.radians(20)) > 0.3:
            j = (i + 1) % n
            q = [lo[i], lo[j], hi[j], hi[i]]
            p.poly(q, col_d, None)
    for k in range(flutes):                                       # flutes as thin lines on the near side
        a = to_cam + (k - flutes / 2 + 0.5) * (math.pi * 0.9 / flutes)
        p.line([cam.project((cx + r0 * math.cos(a), y0, cz + r0 * math.sin(a)))[0],
                cam.project((cx + r1 * math.cos(a), y1, cz + r1 * math.sin(a)))[0]], col_d, 1.2)
    if cam.pos[1] > y1:
        p.poly(hi, B.lt(col, 1.08) if hasattr(B, 'lt') else col, line, 1.6)
    p.poly(hull, None, line, 2.0)


def disc(img, cam, cx, y, cz, r, col, line=INK, lw=1.6, n=36):
    if cam.depth((cx, y, cz)) < r + 0.4:
        return
    cam.poly(_pen(img), [(cx + r * math.cos(a), y, cz + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)],
             col, line, lw)


_GL = {}


def text3(img, cam, txt, corners, col, font='Anton-Regular.ttf'):
    """Lettering laid flat onto a 3D rectangle (TL, TR, BR, BL), drawn once large (never pulses)."""
    import poker_mon_cast as PC
    key = (txt, col, font)
    if key not in _GL:
        f = ImageFont.truetype(os.path.join(HERE, 'fonts', font), 160)
        l, t_, r, b = f.getbbox(txt)
        im = Image.new('RGBA', (r - l + 16, b - t_ + 16), col + (0,))
        ImageDraw.Draw(im).text((8 - l, 8 - t_), txt, font=f, fill=col + (255,))
        _GL[key] = im
    q = [cam.project(c)[0] for c in corners]
    if any(cam.depth(c) < 0.3 for c in corners):
        return
    PC.place_image(img, FLAT, _GL[key], q)


# ------------------------------------------------------------------------------------------------ sky
def sky(img, cam, t=0.0):
    """An overcast autumn sky (Sam, 20 Oct: "add some cloudy weather"; refs crowd-low-1..3): a pale grey-blue, banks of
    big flat clouds with grey undersides drifting slowly, a grey haze along the horizon. Flat colours, one outline on
    the cloud tops only where they meet the sky."""
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, img.height], fill=SKY + (255,))
    p = _pen(img)
    rng = np.random.default_rng(3)
    far = 3000.0
    for layer, (n, el0, el1, size) in enumerate(((10, 0.03, 0.1, 1.3), (12, 0.1, 0.3, 1.1), (10, 0.28, 0.7, 1.0))):
        for k in range(n):
            az = rng.uniform(-1.4, 1.4) + 0.003 * t * (1 + layer)
            el = rng.uniform(el0, el1)
            for back in (0.0, math.pi):                 # clouds all round, so every camera direction has them
                a = az + back
                c = (cam.pos[0] + far * math.sin(a), cam.pos[1] + far * el, cam.pos[2] + far * math.cos(a))
                if cam.depth(c) <= 0:
                    continue
                (X, Y), k_ = cam.project(c)
                w = rng.uniform(0.2, 0.38) * k_ * far * size          # a cloud bank about 12-22 degrees across
                h = w * rng.uniform(0.22, 0.34)
                blobs = [(X + rng.uniform(-0.55, 0.55) * w, Y + rng.uniform(-0.35, 0.1) * h, rng.uniform(0.22, 0.4) * w)
                         for _ in range(7)]
                for bx, by, br in blobs:                    # the grey underside
                    p.ell(bx, by + br * 0.12, br, br * 0.5, CLOUD_G, None)
                for bx, by, br in blobs:                    # the lit tops
                    p.ell(bx, by - br * 0.12, br * 0.9, br * 0.46, CLOUD_D, None)
                for bx, by, br in blobs[:4]:
                    p.ell(bx, by - br * 0.22, br * 0.7, br * 0.34, CLOUD, None)
                p.poly([(X - w * 0.75, Y + h * 0.35), (X + w * 0.75, Y + h * 0.35), (X + w * 0.68, Y + h * 0.55),
                        (X - w * 0.68, Y + h * 0.55)], CLOUD_G, None)  # the flat base


# ------------------------------------------------------------------------------------------------ the square
SQ_X, SQ_S, SQ_N = 52.0, -24.0, 58.0         # the paved square: x from -SQ_X to SQ_X, z from SQ_S to SQ_N
TERRACE_Y, TERRACE_N = 3.6, 76.0             # the north terrace: its top, and the gallery's front
STEPS = (-11.0, 11.0)                        # the central staircase down from the terrace
FOUNTAINS = ((-21.0, 20.0), (21.0, 20.0))    # the two fountains' centres (just north of the column)
F_R = 8.5                                    # the quatrefoil basin's lobe distance
COL_BASE = 8.0                               # the column's stepped base: half-width
LIONS = [(-7.6, -9.0, -1), (7.6, -9.0, -1), (-7.6, 9.0, 1), (7.6, 9.0, 1)]   # (x, z, facing +z north / -z south)
GRANITE, GRANITE_D = (176, 172, 166), (150, 146, 140)


def quatrefoil(cx, cz, r, n=96):
    """The four-leaf-clover basin outline (refs aerial-1..3)."""
    pts = []
    for a in np.linspace(0, 2 * math.pi, n, endpoint=False):
        rr = r * (0.78 + 0.26 * abs(math.cos(2 * a)) ** 0.6)
        pts.append((cx + rr * math.cos(a), cz + rr * math.sin(a)))
    return pts


def ground(img, cam):
    """Roads round three sides with their markings; the square paved in pale granite slabs (the joints drawn near
    the camera), a darker granite border, the inlaid diamond and square round each fountain, a broad pale walk from
    the steps to the column (refs aerial-1..3)."""
    quad(img, cam, [(-900, 0, -900), (900, 0, -900), (900, 0, 400), (-900, 0, 400)], ROAD, None)
    for x0, x1, z0, z1 in ((-SQ_X - 22, SQ_X + 22, SQ_S - 26, SQ_S - 22), (-SQ_X - 22, -SQ_X - 18, SQ_S - 22, SQ_N + 26),
                           (SQ_X + 18, SQ_X + 22, SQ_S - 22, SQ_N + 26)):      # pavements beside the buildings
        quad(img, cam, [(x0, 0.005, z0), (x1, 0.005, z0), (x1, 0.005, z1), (x0, 0.005, z1)], PAVE_D, None)
    quad(img, cam, [(-SQ_X, 0.01, SQ_S), (SQ_X, 0.01, SQ_S), (SQ_X, 0.01, SQ_N), (-SQ_X, 0.01, SQ_N)], GRANITE, INK, 1.4)
    quad(img, cam, [(-SQ_X + 2, 0.011, SQ_S + 2), (SQ_X - 2, 0.011, SQ_S + 2), (SQ_X - 2, 0.011, SQ_N), (-SQ_X + 2, 0.011, SQ_N)],
         PAVE, None)
    quad(img, cam, [(-6, 0.012, COL_BASE + 1), (6, 0.012, COL_BASE + 1), (6, 0.012, SQ_N), (-6, 0.012, SQ_N)], PAVE_L, None)
    p = _pen(img)
    cx, cz = cam.pos[0], cam.pos[2]
    for x in np.arange(-SQ_X + 2, SQ_X - 1, 1.5):        # slab joints, only where they read (within 45 m)
        if abs(x - cx) < 45:
            cam.line(p, [(x, 0.013, max(SQ_S + 2, cz - 45)), (x, 0.013, min(SQ_N, cz + 45))], PAVE_D, 1.4)
    for z in np.arange(SQ_S + 2, SQ_N, 1.5):
        if abs(z - cz) < 45:
            cam.line(p, [(max(-SQ_X + 2, cx - 45), 0.013, z), (min(SQ_X - 2, cx + 45), 0.013, z)], PAVE_D, 1.4)
    for fx, fz in FOUNTAINS:                          # the inlaid diamond and square round each fountain
        for r, rot in ((15.0, 0.0), (11.5, math.pi / 4)):
            pts = [(fx + r * math.cos(rot + k * math.pi / 2), 0.015, fz + r * math.sin(rot + k * math.pi / 2)) for k in range(4)]
            cam.poly(p, pts, None, (120, 116, 110), 5.0)
    for z in (SQ_S - 6, SQ_S - 14):                  # lane markings on the south road
        for x in np.arange(-160, 160, 8):
            cam.line(p, [(x, 0.01, z), (x + 4, 0.01, z)], ROAD_L, 2.0)
    for x in (-SQ_X - 10, SQ_X + 10, 8.0):           # the side roads and Whitehall
        z1 = SQ_N + 20 if abs(x) > 20 else SQ_S - 26
        for z in np.arange(-700 if abs(x) < 20 else SQ_S - 22, z1 if abs(x) > 20 else SQ_S - 26, 8):
            cam.line(p, [(x, 0.01, z), (x, 0.01, z + 4)], ROAD_L, 2.0)


def edges(img, cam):
    """The square's sides: low granite parapets along the east and west with gaps for the stairs, black bollards and a
    kerb along the south road (refs aerial-2, lion-4)."""
    for sg in (-1, 1):
        x = sg * SQ_X
        for z0, z1 in ((SQ_S, -4.0), (4.0, 26.0), (34.0, SQ_N)):
            box(img, cam, min(x, x + sg * 0.6), max(x, x + sg * 0.6), 0, 1.1, z0, z1, GRANITE, GRANITE_D, GRANITE, INK, 1.4)
    p = _pen(img)
    for x in np.arange(-SQ_X, SQ_X, 2.4):
        if cam.depth((x, 0.5, SQ_S)) > 1:
            cam.line(p, [(x, 0, SQ_S), (x, 0.9, SQ_S)], IRON, 4.0)


def balustrade(img, cam, x0, x1, z, y, h=1.0, col=STONE_G, col_d=STONE_GD):
    """A stone balustrade along x at depth z, standing on y: a plinth, a row of balusters (bottle shapes as short
    thick strokes), a coping on top, posts every 6 m."""
    quad(img, cam, [(x0, y, z), (x1, y, z), (x1, y + 0.18, z), (x0, y + 0.18, z)], col, INK, 1.2)
    p = _pen(img)
    if abs(cam.depth(((x0 + x1) / 2, y, z))) < 160:
        for x in np.arange(x0 + 0.15, x1, 0.32):
            cam.line(p, [(x, y + 0.18, z), (x, y + h - 0.14, z)], col_d, 3.2)
            cam.line(p, [(x, y + 0.3, z), (x, y + h - 0.3, z)], col, 2.0)
    for x in np.arange(x0, x1 + 0.1, 6.0):
        quad(img, cam, [(x - 0.25, y, z), (x + 0.25, y, z), (x + 0.25, y + h + 0.1, z), (x - 0.25, y + h + 0.1, z)], col, INK, 1.2)
    quad(img, cam, [(x0, y + h - 0.14, z), (x1, y + h - 0.14, z), (x1, y + h, z), (x0, y + h, z)], col, INK, 1.2)


def lamp_standard(img, cam, x, y, z, h=5.5):
    """An ornate black lamp standard with twin lanterns (refs lion-4, crowd-low-2)."""
    if cam.depth((x, y + h / 2, z)) < 1:
        return
    p = _pen(img)
    cam.line(p, [(x, y, z), (x, y + h, z)], IRON, 4.0)
    cam.line(p, [(x - 0.7, y + h - 0.4, z), (x + 0.7, y + h - 0.4, z)], IRON, 3.0)
    for dx in (-0.7, 0.7):
        (X, Y), k = cam.project((x + dx, y + h - 0.1, z))
        p.poly([(X - 0.22 * k, Y + 0.3 * k), (X + 0.22 * k, Y + 0.3 * k), (X + 0.28 * k, Y - 0.25 * k), (X, Y - 0.45 * k),
                (X - 0.28 * k, Y - 0.25 * k)], (236, 228, 190), INK, 1.2)
    (X, Y), k = cam.project((x, y + 0.6, z))
    p.ell(X, Y, 0.18 * k, 0.4 * k, IRON, None)


def terrace(img, cam):
    """The north terrace (refs crowd-low-1..3, from-portico, protest-3): a granite wall 3.6 m high the length of the
    square with a stone balustrade on top, the broad central staircase with its landing and side walls, lamp standards
    along the top; the banners from Sam's photos tied along the balustrade (LIFT THE BAN, PEACE, DROP THE CHARGES)."""
    if cam.pos[1] > TERRACE_Y:                                   # its top is only seen from above
        quad(img, cam, [(-SQ_X, TERRACE_Y, SQ_N), (SQ_X, TERRACE_Y, SQ_N), (SQ_X, TERRACE_Y, TERRACE_N),
                        (-SQ_X, TERRACE_Y, TERRACE_N)], PAVE_L, INK, 1.4)
    p = _pen(img)
    for x0, x1 in ((-SQ_X, STEPS[0] - 1.2), (STEPS[1] + 1.2, SQ_X)):
        quad(img, cam, [(x0, 0, SQ_N), (x1, 0, SQ_N), (x1, TERRACE_Y, SQ_N), (x0, TERRACE_Y, SQ_N)], STONE_G, INK, 1.8)
        for y in np.arange(0.6, TERRACE_Y, 0.6):               # the wall's courses and blocks
            cam.line(p, [(x0, y, SQ_N - 0.01), (x1, y, SQ_N - 0.01)], STONE_GD, 1.0)
        for x in np.arange(x0, x1, 1.8):
            cam.line(p, [(x, 0.0, SQ_N - 0.01), (x, TERRACE_Y, SQ_N - 0.01)], STONE_GD, 0.8)
        quad(img, cam, [(x0, TERRACE_Y - 0.3, SQ_N - 0.02), (x1, TERRACE_Y - 0.3, SQ_N - 0.02), (x1, TERRACE_Y, SQ_N - 0.02),
                        (x0, TERRACE_Y, SQ_N - 0.02)], STONE_GD, INK, 1.2)     # the cornice
        balustrade(img, cam, x0, x1, SQ_N, TERRACE_Y)
        for x in np.arange(x0 + 4, x1, 12.0):
            lamp_standard(img, cam, x, TERRACE_Y, SQ_N + 1.2)
    for sg in (-1, 1):                                           # the staircase's side walls
        x = sg * (STEPS[1] + 0.6)
        box(img, cam, x - 0.6, x + 0.6, 0, TERRACE_Y + 1.0, SQ_N - 0.6, SQ_N + 6.0, STONE_G, STONE_GD, STONE_G, INK, 1.4)
        lamp_standard(img, cam, x, TERRACE_Y + 1.0, SQ_N - 0.4)
    n = 14
    for k in range(n):
        y0, y1 = TERRACE_Y * k / n, TERRACE_Y * (k + 1) / n
        z = SQ_N + (k / n) * 6.0
        if cam.pos[1] > y1:
            quad(img, cam, [(STEPS[0], y1, z), (STEPS[1], y1, z), (STEPS[1], y1, z + 6.0 / n), (STEPS[0], y1, z + 6.0 / n)],
                 PAVE_L, None)
        if cam.pos[2] < z:
            quad(img, cam, [(STEPS[0], y0, z), (STEPS[1], y0, z), (STEPS[1], y1, z), (STEPS[0], y1, z)], STONE_G, INK, 0.9)
    for x0, x1, txt, cloth, ink in ((-34.0, -18.0, 'LIFT THE BAN', (246, 244, 236), (200, 30, 40)),
                                    (-7.0, 7.0, 'PEACE', (246, 244, 236), (24, 24, 28)),
                                    (16.0, 36.0, 'DROP THE CHARGES', (196, 30, 40), (246, 244, 236))):
        y0, y1, zb = TERRACE_Y + 0.05, TERRACE_Y + 1.1, SQ_N - 0.05      # tied along the balustrade
        if x0 < STEPS[1] and x1 > STEPS[0]:                               # PEACE hangs across the top of the steps
            zb, y0, y1 = SQ_N + 6.2, TERRACE_Y + 0.1, TERRACE_Y + 1.1
        quad(img, cam, [(x0, y1, zb), (x1, y1, zb), (x1, y0, zb), (x0, y0, zb)], cloth, INK, 1.6)
        w = (x1 - x0) * 0.86
        cx = (x0 + x1) / 2
        text3(img, cam, txt, [(cx + w / 2, y1 - 0.15, zb - 0.01), (cx - w / 2, y1 - 0.15, zb - 0.01),   # read from
                              (cx - w / 2, y0 + 0.15, zb - 0.01), (cx + w / 2, y0 + 0.15, zb - 0.01)], ink)  # the south


def classical(img, cam, a0, a1, at, y0, h, axis='z', bays=None, col=STONE, col_d=STONE_D, seed=0, flag=False,
              storeys=3, portico=False):
    """A classical stone front (refs gallery-1, from-steps-1, column-fountain; never a blank wall): a rusticated
    ground storey (banded joints, arched windows and doors), a string course, pilasters between the bays, tall
    upper windows each under a small pediment, a heavy cornice and a balustrade along the roof. `axis` 'z': the
    front runs along x (from a0 to a1) at depth `at`; 'x': along z at x = `at`."""
    rng = np.random.default_rng(abs(int(seed)))

    def P(u, y):
        s = a0 + (a1 - a0) * u
        return (s, y, at) if axis == 'z' else (at, y, s)
    length = abs(a1 - a0)
    if cam.depth(P(0.5, y0 + h / 2)) < -length:
        return
    quad(img, cam, [P(0, y0), P(1, y0), P(1, y0 + h), P(0, y0 + h)], col, INK, 1.8)
    bays = bays or max(3, int(length / 4.6))
    p = _pen(img)
    g = min(4.6, h * 0.3)                                       # the rusticated ground storey
    for y in np.arange(y0 + 0.55, y0 + g, 0.55):
        cam.line(p, [P(0, y), P(1, y)], col_d, 1.0)
    quad(img, cam, [P(0, y0 + g), P(1, y0 + g), P(1, y0 + g + 0.4), P(0, y0 + g + 0.4)], col_d, INK, 1.2)
    up = (h - g - 2.2) / max(1, storeys - 1)
    for b in range(bays):
        u0, u1 = b / bays, (b + 1) / bays
        uc = (u0 + u1) / 2
        w = (u1 - u0) * 0.34
        if b > 0:                                                # a pilaster
            quad(img, cam, [P(u0 - 0.06 / bays, y0 + g + 0.4), P(u0 + 0.06 / bays, y0 + g + 0.4),
                            P(u0 + 0.06 / bays, y0 + h - 1.6), P(u0 - 0.06 / bays, y0 + h - 1.6)], B.lt(col, 1.05), INK, 0.9)
        door = b % 5 == 2
        top = y0 + (g * 0.85 if door else g * 0.75)
        bot = y0 if door else y0 + g * 0.25
        quad(img, cam, [P(uc - w, bot), P(uc + w, bot), P(uc + w, top), P(uc - w, top)], (64, 50, 40) if door else WINDOW, INK, 1.0)
        arch = [P(uc - w + 2 * w * (0.5 - 0.5 * math.cos(a)), top + (w * length) * 0.5 * math.sin(a)) for a in np.linspace(0, math.pi, 7)]
        if (w * length) * 0.5 < 1.2:
            quad(img, cam, arch, (64, 50, 40) if door else WINDOW, INK, 1.0)
        for s in range(1, storeys):                              # the upper windows, each with a pediment
            yb = y0 + g + 0.4 + (s - 1) * up + up * 0.18
            yt = yb + up * 0.62
            quad(img, cam, [P(uc - w * 0.8, yb), P(uc + w * 0.8, yb), P(uc + w * 0.8, yt), P(uc - w * 0.8, yt)],
                 WINDOW if rng.random() < 0.85 else WINDOW_D, INK, 1.0)
            for k in range(1, 3):                                 # glazing bars
                cam.line(p, [P(uc - w * 0.8, yb + (yt - yb) * k / 3), P(uc + w * 0.8, yb + (yt - yb) * k / 3)], (100, 112, 124), 0.8)
            quad(img, cam, [P(uc - w, yt + 0.1), P(uc + w, yt + 0.1), P(uc, yt + 0.6)], col_d, INK, 1.0)
    quad(img, cam, [P(0, y0 + h - 1.6), P(1, y0 + h - 1.6), P(1, y0 + h - 0.9), P(0, y0 + h - 0.9)], col_d, INK, 1.4)   # cornice
    quad(img, cam, [P(0, y0 + h - 0.9), P(1, y0 + h - 0.9), P(1, y0 + h), P(0, y0 + h)], col, INK, 1.0)
    for u in np.linspace(0, 1, max(6, int(length / 0.6))):      # the roof balustrade
        cam.line(p, [P(u, y0 + h), P(u, y0 + h + 0.8)], col_d, 2.0)
    quad(img, cam, [P(0, y0 + h + 0.8), P(1, y0 + h + 0.8), P(1, y0 + h + 1.0), P(0, y0 + h + 1.0)], col, INK, 1.0)
    if flag:                                                     # a flag on the roof (refs from-steps-1)
        fx = P(0.5, y0 + h + 1.0)
        cam.line(p, [fx, (fx[0], fx[1] + 7, fx[2])], IRON, 2.0)
        fl = [(fx[0], fx[1] + 7, fx[2]), (fx[0] + 3, fx[1] + 6.8, fx[2]), (fx[0] + 3, fx[1] + 5, fx[2]), (fx[0], fx[1] + 5.2, fx[2])]
        quad(img, cam, fl, (30, 50, 120), INK, 1.0)
        cam.line(p, [fl[0], fl[2]], (246, 246, 246), 2.0)
        cam.line(p, [fl[1], fl[3]], (246, 246, 246), 2.0)
    if portico:                                                  # a columned porch in the middle (Canada House, SA House)
        n = 6
        for k in range(n):
            u = 0.5 + (k - (n - 1) / 2) * 0.035
            q0 = P(u, y0 + 1.0)
            cylinder_at = (q0[0], q0[2])
            off = (1.6 if axis == 'z' else 0.0, 0.0 if axis == 'z' else 1.6)
            sg = 1 if cam.pos[2 if axis == 'z' else 0] > at else -1
            cx_, cz_ = (q0[0], q0[2] + sg * 1.6) if axis == 'z' else (q0[0] + sg * 1.6, q0[2])
            cylinder(img, cam, cx_, cz_, y0 + 1.0, y0 + h - 1.6, 0.45, 0.4, (240, 232, 214), col_d, n=12)


def facade(img, cam, x0, x1, z, y0, y1, storeys=4, bays=None, col=STONE, col_d=STONE_D, face=-1, axis='z', flag=False,
           seed=0):
    """A building front: now always the classical one (kept for the callers' signature)."""
    classical(img, cam, x0, x1, z, y0, y1 - y0, axis=axis, bays=bays, col=col, col_d=col_d, seed=seed, flag=flag,
              storeys=storeys)


def gallery(img, cam):
    """The National Gallery (refs gallery-1, from-steps-1, crowd-low-1..3): long classical wings on the terrace (a
    rusticated base, tall windows between pilasters, a cornice and a roof balustrade); the central portico on its
    podium: eight pale Corinthian columns, the entablature, the pediment; two yellow banners hanging between the
    columns; the grey ribbed dome on its drum with a lantern; a small domed cupola either side; St Martin's white
    steeple off to the east."""
    y0 = TERRACE_Y
    zd = TERRACE_N + 9                                           # the dome first: it stands behind the portico
    cylinder(img, cam, 0, zd, y0 + 15.5, y0 + 19.5, 6.2, 6.2, STONE, STONE_D, n=28)        # the drum
    for k in range(9):                                            # its windows (the near half)
        a = math.pi * (0.1 + 0.8 * k / 8)
        x, z = 6.25 * math.cos(math.pi + a), zd - 6.25 * math.sin(a)
        if cam.depth((x, y0 + 17, z)) < cam.depth((0, y0 + 17, zd)):
            quad(img, cam, [(x - 0.4, y0 + 16.2, z), (x + 0.4, y0 + 16.2, z), (x + 0.4, y0 + 18.6, z), (x - 0.4, y0 + 18.6, z)],
                 WINDOW, INK, 0.8)
    for k in range(6):                                            # the ribbed lead dome
        a0, a1 = k / 6 * math.pi / 2, (k + 1) / 6 * math.pi / 2
        cylinder(img, cam, 0, zd, y0 + 19.5 + 6 * math.sin(a0), y0 + 19.5 + 6 * math.sin(a1), 6.2 * math.cos(a0),
                 max(0.6, 6.2 * math.cos(a1)), (150, 158, 164) if k % 2 else (140, 148, 154), (118, 126, 132), n=28, flutes=8)
    cylinder(img, cam, 0, zd, y0 + 25.4, y0 + 28.0, 1.0, 0.8, STONE, STONE_D, n=12)        # the lantern
    cylinder(img, cam, 0, zd, y0 + 28.0, y0 + 29.2, 0.9, 0.05, (140, 148, 154), (118, 126, 132), n=10)
    for sg in (-1, 1):                                            # the cupolas either side
        cx = sg * 11.0
        cylinder(img, cam, cx, TERRACE_N + 6, y0 + 15.5, y0 + 18.0, 1.6, 1.6, STONE, STONE_D, n=16)
        cylinder(img, cam, cx, TERRACE_N + 6, y0 + 18.0, y0 + 20.0, 1.7, 0.2, (150, 158, 164), (118, 126, 132), n=16)
    for sg in (-1, 1):
        classical(img, cam, sg * 13, sg * 62, TERRACE_N + 2, y0, 13.0, bays=11, seed=40 + sg, storeys=2)
    box(img, cam, -13, 13, y0, y0 + 15.5, TERRACE_N + 2, TERRACE_N + 14, STONE, STONE_D, STONE, INK, 1.6)   # centre block
    classical(img, cam, -13, 13, TERRACE_N + 1.99, y0, 15.5, bays=5, seed=44, storeys=2)
    box(img, cam, -10, 10, y0, y0 + 1.4, TERRACE_N - 6, TERRACE_N + 2, PAVE_L, STONE_GD, STONE_G, INK, 1.4)  # podium
    p = _pen(img)
    for k in range(4):                                           # its steps
        z = TERRACE_N - 6 - 0.35 * (k + 1)
        quad(img, cam, [(-8, y0 + 1.4 * (3 - k) / 4, z), (8, y0 + 1.4 * (3 - k) / 4, z), (8, y0 + 1.4 * (4 - k) / 4, z),
                        (-8, y0 + 1.4 * (4 - k) / 4, z)], STONE_G, INK, 0.9)
    ztop = TERRACE_N - 5.2
    quad(img, cam, [(-10.2, y0 + 12.8, TERRACE_N - 6.2), (10.2, y0 + 12.8, TERRACE_N - 6.2), (10.2, y0 + 12.8, TERRACE_N + 2),
                    (-10.2, y0 + 12.8, TERRACE_N + 2)], STONE_D, INK, 1.2)     # the portico's ceiling (seen from below
    p2 = _pen(img)                                               # between the column tops: Sam, 20 Oct)
    for k in range(1, 6):                                        # its coffers
        z = TERRACE_N - 6.2 + k * 8.2 / 6
        cam.line(p2, [(-10.2, y0 + 12.79, z), (10.2, y0 + 12.79, z)], B.dk(STONE_D, 0.88), 1.0)
    for k in range(8):                                           # the columns
        x = -8.6 + 17.2 * k / 7
        cylinder(img, cam, x, ztop, y0 + 1.4, y0 + 12.0, 0.62, 0.55, (242, 236, 222), STONE_D, n=16, flutes=5)
        quad(img, cam, [(x - 0.55, y0 + 11.9, ztop - 0.62), (x + 0.55, y0 + 11.9, ztop - 0.62), (x + 0.8, y0 + 12.8, ztop - 0.8),
                        (x - 0.8, y0 + 12.8, ztop - 0.8)], (236, 228, 210), INK, 1.0)     # the capital, flaring out
        for dx in (-0.5, 0.0, 0.5):                              # its leaves
            cam.line(_pen(img), [(x + dx * 0.9, y0 + 12.0, ztop - 0.7), (x + dx * 1.3, y0 + 12.7, ztop - 0.8)], STONE_D, 1.2)
    for k, x in ((1, -8.6 + 17.2 * 1.5 / 7), (6, -8.6 + 17.2 * 5.5 / 7)):    # the yellow banners (refs crowd-low-1, 2)
        zb = ztop + 0.9
        quad(img, cam, [(x - 0.75, y0 + 11.6, zb), (x + 0.75, y0 + 11.6, zb), (x + 0.75, y0 + 5.2, zb), (x - 0.75, y0 + 5.2, zb)],
             (238, 196, 40), INK, 1.4)
        cam.line(p, [(x - 0.5, y0 + 10.6, zb - 0.01), (x + 0.5, y0 + 10.6, zb - 0.01)], (60, 50, 30), 2.0)
    box(img, cam, -10.2, 10.2, y0 + 12.8, y0 + 14.4, TERRACE_N - 6.2, TERRACE_N + 2, STONE, STONE_D, STONE, INK, 1.4)
    quad(img, cam, [(-10.2, y0 + 14.4, TERRACE_N - 6.2), (10.2, y0 + 14.4, TERRACE_N - 6.2), (0, y0 + 17.6, TERRACE_N - 6.2)],
         STONE, INK, 1.8)                                         # the pediment
    quad(img, cam, [(-8.6, y0 + 14.7, TERRACE_N - 6.21), (8.6, y0 + 14.7, TERRACE_N - 6.21), (0, y0 + 17.0, TERRACE_N - 6.21)],
         STONE_D, INK, 1.0)
    sx, sz = 70.0, TERRACE_N + 10                                 # St Martin-in-the-Fields
    classical(img, cam, sx - 10, sx + 10, sz - 8, 0, 14, bays=4, seed=46, storeys=2)
    box(img, cam, sx - 3, sx + 3, 14, 28, sz - 3, sz + 3, (244, 240, 230), STONE_D, (244, 240, 230))
    for h0, h1, r in ((28, 33, 2.4), (33, 37, 1.8), (37, 40, 1.3)):
        box(img, cam, sx - r, sx + r, h0, h1, sz - r, sz + r, (244, 240, 230), STONE_D, (244, 240, 230))
    cylinder(img, cam, sx, sz, 40, 52, 1.1, 0.05, (244, 240, 230), STONE_D, n=8)


def whitehall(img, cam):
    """South of the square: Whitehall running away to Big Ben, lined both sides with stone government buildings (so
    the road out of the square leads somewhere: Sam, 20 Oct), Big Ben's tower at the end."""
    for z0 in range(-46, -700, -60):
        z1 = z0 - 58
        classical(img, cam, z0, z1, -2.0, 0, 20 + (z0 % 7), axis='x', bays=12, seed=100 + z0, storeys=4)
        classical(img, cam, z0, z1, 18.0, 0, 22 - (z0 % 5), axis='x', bays=12, seed=200 + z0, storeys=4,
                  col=(232, 222, 200))
    bx, bz = 8.0, -760.0                                          # Big Ben
    box(img, cam, bx - 6, bx + 6, 0, 62, bz - 6, bz + 6, (206, 180, 120), (176, 150, 96), (206, 180, 120), INK, 1.0)
    box(img, cam, bx - 7, bx + 7, 62, 76, bz - 7, bz + 7, (206, 180, 120), (176, 150, 96), (206, 180, 120), INK, 1.0)
    if cam.pos[2] > bz + 7:
        disc_v(img, cam, bx, 69, bz + 7.05, 4.6, (244, 240, 228))
    cylinder(img, cam, bx, bz, 76, 98, 7.5, 0.4, (70, 78, 84), (54, 60, 66), n=4)
    classical(img, cam, -120, 140, -830, 0, 24, bays=40, seed=300, storeys=3, col=(206, 180, 120), col_d=(176, 150, 96))


def disc_v(img, cam, cx, cy, z, r, col):
    """A clock face: a disc facing the square, its hands at ten past ten."""
    pts = [(cx + r * math.cos(a), cy + r * math.sin(a), z) for a in np.linspace(0, 2 * math.pi, 30, endpoint=False)]
    quad(img, cam, pts, col, INK, 1.2)
    p = _pen(img)
    cam.line(p, [(cx, cy, z - 0.01), (cx - r * 0.5, cy + r * 0.3, z - 0.01)], INK, 1.6)
    cam.line(p, [(cx, cy, z - 0.01), (cx + r * 0.6, cy + r * 0.5, z - 0.01)], INK, 1.6)


def surroundings(cam, t):
    """The buildings, Whitehall and the traffic as (depth, draw) items, drawn far to near."""
    items = []
    south = [(-150, -60, 'Admiralty'), (-50, -2, 'A'), (18, 80, 'B'), (80, 160, 'C')]
    for a0, a1, nm in south:                                     # the south side, broken only by Whitehall
        items.append((cam.depth(((a0 + a1) / 2, 10, -46)),
                      lambda img, a0=a0, a1=a1, nm=nm: classical(img, cam, a0, a1, -46, 0, 22 if nm != 'Admiralty' else 18,
                                                                bays=int((a1 - a0) / 4.6), seed=a0 + 500, flag=nm == 'B',
                                                                storeys=4, col=(232, 222, 200) if nm == 'B' else STONE)))
    items.append((cam.depth((8, 10, -300)), lambda img: whitehall(img, cam)))
    items.append((cam.depth((-SQ_X - 26, 10, 10)), lambda img: classical(img, cam, -50, 70, -SQ_X - 26, 0, 22, axis='x',
                                                                         bays=24, seed=14, flag=True, portico=True)))
    items.append((cam.depth((SQ_X + 26, 10, 10)), lambda img: classical(img, cam, -50, 70, SQ_X + 26, 0, 24, axis='x',
                                                                        bays=24, seed=15, flag=True, portico=True,
                                                                        col=(232, 222, 200))))
    items.append((cam.depth((0, 10, TERRACE_N + 8)), lambda img: gallery(img, cam)))
    rng = np.random.default_rng(9)
    for side in (-1, 1):                                         # plane trees along the east and west edges
        for z in np.arange(-10, 52, 9.0):
            x = side * (SQ_X + 6)
            items.append((cam.depth((x, 5, z)), lambda img, x=x, z=z: tree(img, cam, x, z)))
    for v in traffic(t):
        items.append((cam.depth((v[1], 1.5, v[2])), lambda img, v=v: vehicle(img, cam, *v)))
    return items


def tree(img, cam, x, z):
    if cam.depth((x, 5, z)) < 1:
        return
    cam.line(_pen(img), [(x, 0, z), (x, 4, z)], (90, 66, 46), 3.0)
    (X, Y), k = cam.project((x, 6.5, z))
    r = 3.2 * k
    for dx, dy in ((-0.5, 0.1), (0.5, 0.1), (0, -0.4), (0, 0.3)):
        _pen(img).ell(X + dx * r, Y + dy * r, r * 0.7, r * 0.62, TREE_D, INK, 1.4)
    _pen(img).ell(X, Y - 0.1 * r, r * 0.8, r * 0.66, TREE, None)


CAR_COLS = [(196, 196, 200), (40, 44, 56), (150, 30, 36), (230, 230, 226), (70, 90, 120), (110, 112, 118), (30, 30, 34)]


def traffic(t):
    """Vehicles on the roads round the square (Sam, 20 Oct: no traffic): buses, black cabs and cars moving both ways
    along the south road, up and down the side roads and Whitehall. Each: (kind, x, z, heading, colour)."""
    out = []
    rng = np.random.default_rng(21)
    lanes = [((-200, SQ_S - 9), (1, 0), 6.0), ((200, SQ_S - 17), (-1, 0), 5.5), ((-SQ_X - 8, -60), (0, 1), 5.0),
             ((-SQ_X - 13, 120), (0, -1), 5.0), ((SQ_X + 8, 120), (0, -1), 5.5), ((SQ_X + 13, -60), (0, 1), 5.0),
             ((5.0, -60), (0, -1), 6.0), ((11.0, -600), (0, 1), 6.0)]
    for k, ((x0, z0), (dx, dz), v) in enumerate(lanes):
        span = 400.0 if abs(dx) else (180.0 if abs(x0) > 20 else 560.0)
        for i in range(5 if abs(dx) else 3):
            kind = ['bus', 'cab', 'car', 'cab', 'car', 'bus', 'car'][int(rng.integers(7))]
            off = (rng.uniform(0, span) + v * t) % span
            x, z = x0 + dx * off, z0 + dz * off
            out.append((kind, x, z, math.atan2(dz, dx), CAR_COLS[int(rng.integers(len(CAR_COLS)))]))
    return out


def obox(img, cam, cx, cz, heading, L, W, y0, y1, col, col_d, line=INK):
    """An oriented box (a vehicle's body): its faces seen from the camera, far to near."""
    ch, sh = math.cos(heading), math.sin(heading)

    def P(u, v, y):
        return (cx + u * ch - v * sh, y, cz + u * sh + v * ch)
    faces = [([P(-L / 2, -W / 2, y0), P(L / 2, -W / 2, y0), P(L / 2, -W / 2, y1), P(-L / 2, -W / 2, y1)], col),
             ([P(-L / 2, W / 2, y0), P(L / 2, W / 2, y0), P(L / 2, W / 2, y1), P(-L / 2, W / 2, y1)], col),
             ([P(L / 2, -W / 2, y0), P(L / 2, W / 2, y0), P(L / 2, W / 2, y1), P(L / 2, -W / 2, y1)], col_d),
             ([P(-L / 2, -W / 2, y0), P(-L / 2, W / 2, y0), P(-L / 2, W / 2, y1), P(-L / 2, -W / 2, y1)], col_d),
             ([P(-L / 2, -W / 2, y1), P(L / 2, -W / 2, y1), P(L / 2, W / 2, y1), P(-L / 2, W / 2, y1)], B.lt(col, 1.1))]
    vis = []
    c = (cx, (y0 + y1) / 2, cz)
    for pts, colr in faces:
        ctr = tuple(np.mean(pts, axis=0))
        if np.dot(np.subtract(ctr, c), np.subtract(cam.pos, ctr)) > 0:
            vis.append((cam.depth(ctr), pts, colr))
    for d, pts, colr in sorted(vis, key=lambda v: -v[0]):
        quad(img, cam, pts, colr, line, 1.2)
    return P


def vehicle(img, cam, kind, x, z, heading, colr):
    """A bus (red double-decker, 10.5 x 2.5 x 4.4 m), a black cab or a car, with windows and wheels."""
    if cam.depth((x, 1.5, z)) < 2:
        return
    if kind == 'bus':
        L, W, H, col = 10.5, 2.5, 4.4, BUS
    elif kind == 'cab':
        L, W, H, col = 4.6, 1.8, 1.8, (24, 24, 28)
    else:
        L, W, H, col = 4.3, 1.8, 1.45, colr
    P = obox(img, cam, x, z, heading, L, W, 0.35, H * (0.55 if kind != 'bus' else 1.0), col, B.dk(col, 0.8))
    if kind != 'bus':                                             # the cabin, narrower, with its windows
        P2 = obox(img, cam, x - 0.2 * math.cos(heading), z - 0.2 * math.sin(heading), heading, L * 0.55, W * 0.92,
                  H * 0.55, H, (60, 70, 84) if kind == 'car' else (40, 46, 56), (40, 46, 56))
        if kind == 'cab':
            (X, Y), k = cam.project((x, H + 0.12, z))
            _pen(img).poly([(X - 0.25 * k, Y - 0.08 * k), (X + 0.25 * k, Y - 0.08 * k), (X + 0.25 * k, Y + 0.08 * k),
                            (X - 0.25 * k, Y + 0.08 * k)], (246, 196, 40), INK, 1.0)
    else:
        for side in (-1, 1):
            v = side * W / 2 * 1.01
            if np.dot((-math.sin(heading) * side, 0, math.cos(heading) * side), np.subtract(cam.pos, P(0, v, 2))) <= 0:
                continue
            for y0, y1 in ((1.6, 2.4), (3.1, 3.9)):
                for i in range(6):
                    u0 = -4.8 + i * 1.65
                    quad(img, cam, [P(u0, v, y0), P(u0 + 1.4, v, y0), P(u0 + 1.4, v, y1), P(u0, v, y1)], WINDOW, INK, 0.9)
    p = _pen(img)
    for u in (-L * 0.32, L * 0.32):
        for side in (-1, 1):
            q = P(u, side * W / 2 * 1.02, 0.35)
            if cam.depth(q) > 1 and cam.depth(q) <= cam.depth(P(u, 0, 0.35)) + 0.5:
                (X, Y), k = cam.project(q)
                p.ell(X, Y, 0.36 * k, 0.36 * k, (24, 24, 26), INK, 1.2)


def bus(img, cam, x, z):
    vehicle(img, cam, 'bus', x, z, 0.0, BUS)


def fountain(img, cam, cx, cz, t):
    """A fountain (refs aerial-1..3, fountain-1, column-fountain): the four-leaf basin with its wide grey stone rim
    (people sit on it), turquoise water, the golden sandstone bowls in two tiers, a tall jet falling back."""
    out = quatrefoil(cx, cz, F_R)
    inn = quatrefoil(cx, cz, F_R - 0.7)
    rim_h = 0.55
    if cam.pos[1] > rim_h:
        quad(img, cam, [(x, rim_h, z) for x, z in out], STONE_G, INK, 1.8)
        quad(img, cam, [(x, 0.4, z) for x, z in inn], WATER, INK, 1.4)
    p = _pen(img)
    near = [i for i, (x, z) in enumerate(out) if (cam.pos[0] - cx) * (x - cx) + (cam.pos[2] - cz) * (z - cz) > 0]
    for i in near:                                              # the rim's outer face, nearest side
        j = (i + 1) % len(out)
        (x0, z0), (x1, z1) = out[i], out[j]
        quad(img, cam, [(x0, 0, z0), (x1, 0, z1), (x1, rim_h, z1), (x0, rim_h, z0)], STONE_GD, None)
    cam.poly(p, [(x, rim_h, z) for x, z in out], None, INK, 1.8)
    rng = np.random.default_rng(int(abs(cx)) + (1 if cx < 0 else 0))
    for k in range(10):                                         # ripples on the water
        a, r = rng.uniform(0, 2 * math.pi), rng.uniform(2.5, F_R - 2)
        x, z = cx + r * math.cos(a), cz + r * math.sin(a)
        cam.line(p, [(x - 0.6, 0.41, z), (x + 0.6, 0.41, z)], WATER_L, 1.6)
    cylinder(img, cam, cx, cz, 0.4, 1.4, 0.8, 0.7, SAND, SAND_D, n=18)                    # the stem
    cylinder(img, cam, cx, cz, 1.4, 2.0, 1.2, 3.0, SAND, SAND_D, n=24)                    # the lower bowl
    disc(img, cam, cx, 2.0, cz, 2.8, WATER)
    cylinder(img, cam, cx, cz, 2.0, 3.0, 0.4, 0.35, SAND, SAND_D, n=12)
    cylinder(img, cam, cx, cz, 3.0, 3.4, 0.5, 1.4, SAND, SAND_D, n=18)                    # the upper bowl
    jet(img, cam, cx, cz, t)


def jet(img, cam, cx, cz, t):
    """The tall jet: a white column of water rising to 6 m and spilling back over the bowls in lumpy falls (flat
    white shapes, flickering a little each frame; never a glow)."""
    p = _pen(img)
    if cam.depth((cx, 4, cz)) < 1:
        return
    (X0, Y0), k = cam.project((cx, 3.4, cz))
    (X1, Y1), _ = cam.project((cx, 6.2 + 0.25 * math.sin(t * 9), cz))
    w = 0.32 * k
    p.poly(rough([(X0 - w, Y0), (X1 - w * 0.5, Y1), (X1 + w * 0.5, Y1), (X0 + w, Y0)], 2, int(t * 12) % 7), (246, 250, 252), INK, 1.4)
    rng = np.random.default_rng(int(t * 12))
    for sg in (-1, 1):
        for r in (1.4, 2.9):
            for _ in range(3):
                a = rng.uniform(-0.6, 0.6) + (0 if sg > 0 else math.pi)
                x, z = cx + r * math.cos(a), cz + r * math.sin(a)
                (X, Y), kk = cam.project((x, 2.0 if r > 2 else 3.2, z))
                p.ell(X, Y, 0.18 * kk, 0.32 * kk, (236, 246, 250), None)


def column(img, cam):
    """Nelson's Column (refs column-1, column-lion, sizes 51.6 m): the stepped granite base, the tall square pedestal
    with a dark bronze panel on each face and a moulded ledge, the fluted pale grey shaft tapering a little, the dark
    bronze leafy capital, a round stand, Nelson in pale stone facing south."""
    for k, (h, w) in enumerate(((0.5, COL_BASE), (1.0, COL_BASE - 0.8), (1.5, COL_BASE - 1.6))):
        box(img, cam, -w, w, k * 0.5, h, -w, w, PAVE_L, STONE_GD, STONE_G, INK, 1.6)
    box(img, cam, -3.6, 3.6, 1.5, 10.5, -3.6, 3.6, STONE_G, STONE_GD, STONE_G)               # the pedestal
    p = _pen(img)
    for sg in (-1, 1):                                       # the bronze panels (south and north faces; east, west)
        z = sg * 3.61
        if (cam.pos[2] - z) * sg > 0:
            quad(img, cam, [(-2.6, 3.0, z), (2.6, 3.0, z), (2.6, 8.4, z), (-2.6, 8.4, z)], BRONZE, INK, 1.6)
            for kk in range(6):                              # figures in relief, suggested by a few lumps
                x = -2.2 + kk * 0.86
                cam.line(p, [(x, 3.4, z), (x + 0.2, 6.6, z)], BRONZE_L, 2.0)
        x = sg * 3.61
        if (cam.pos[0] - x) * sg > 0:
            quad(img, cam, [(x, 3.0, -2.6), (x, 3.0, 2.6), (x, 8.4, 2.6), (x, 8.4, -2.6)], BRONZE, INK, 1.6)
    box(img, cam, -4.0, 4.0, 10.5, 11.4, -4.0, 4.0, STONE_G, STONE_GD, STONE_G)              # the moulded ledge
    cylinder(img, cam, 0, 0, 11.4, 12.6, 2.4, 2.2, STONE_G, STONE_GD, n=28)                 # the drum
    cylinder(img, cam, 0, 0, 12.6, 42.0, 1.9, 1.55, STONE_G, STONE_GD, n=32, flutes=9)     # the shaft
    cylinder(img, cam, 0, 0, 42.0, 45.0, 1.6, 2.4, BRONZE, BRONZE_D, n=24)                 # the capital
    box(img, cam, -2.5, 2.5, 45.0, 45.6, -2.5, 2.5, BRONZE, BRONZE_D, BRONZE)
    cylinder(img, cam, 0, 0, 45.6, 47.0, 1.0, 0.9, STONE_G, STONE_GD, n=16)                # the round stand
    if cam.depth((0, 49, 0)) > 1:                           # Nelson: a pale stone figure, hat, coat, facing south
        (X, Y), k = cam.project((0, 49.3, 0))
        s = k
        p.poly(rough([(X - 0.55 * s, Y + 2.4 * s), (X + 0.55 * s, Y + 2.4 * s), (X + 0.5 * s, Y - 0.6 * s),
                      (X - 0.5 * s, Y - 0.6 * s)], 2, 3), (214, 210, 200), INK, 1.4)
        p.ell(X, Y - 1.0 * s, 0.32 * s, 0.38 * s, (214, 210, 200), INK, 1.4)
        p.poly([(X - 0.7 * s, Y - 1.2 * s), (X + 0.7 * s, Y - 1.2 * s), (X + 0.3 * s, Y - 1.55 * s), (X - 0.3 * s, Y - 1.55 * s)],
               (196, 192, 184), INK, 1.4)


def _hull(pts):
    """The convex outline of some frame points (monotone chain)."""
    pts = sorted(set((round(x, 1), round(y, 1)) for x, y in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], q) <= 0:
            hi.pop()
        hi.append(q)
    return lo[:-1] + hi[:-1]


# The lion (refs lion-1..4, Sam 20 Oct: "genuinely ridiculous... a massive hole in him"): a solid figure built from
# rounded lumps (each an egg shape: centre (u along the body from the tail end, v up from the block's top, dx across)
# and its half-sizes), lying like a sphinx: haunches folded, the long body, the chest up, the forelegs straight out
# with the paws together, the great mane round the head, the muzzle forward.
LION_BODY = [((1.0, 0.75, 0.0), (1.0, 0.75, 0.85)), ((2.4, 0.8, 0.0), (1.5, 0.8, 0.82)),
             ((3.7, 1.05, 0.0), (0.9, 1.05, 0.8)), ((1.1, 0.62, -0.5), (0.95, 0.62, 0.45)),
             ((1.1, 0.62, 0.5), (0.95, 0.62, 0.45))]
LION_LEGS = [((4.1, 0.45, s * 0.42), (5.9, 0.2, s * 0.42), 0.26) for s in (-1, 1)]
LION_PAWS = [((6.05, 0.17, s * 0.42), (0.34, 0.17, 0.28)) for s in (-1, 1)]
LION_MANE = [((4.1, 2.2, 0.0), (0.95, 1.4, 1.08))]
LION_FACE = [((4.7, 2.5, 0.0), (0.55, 0.72, 0.6)), ((5.15, 2.18, 0.0), (0.42, 0.4, 0.44))]


def lion(img, cam, x, z, facing):
    """A lion on its block at the column's corner: the long plain grey block (7 x 2.4 x 2.2 m, a lettered panel in
    its side) and the bronze lion on it, solid from every side (each part's lumps filled as one shape with one
    outline): body and legs, then the darker mane, then the face (eyes, nose and mouth on the side we see)."""
    L, Wd, H = 7.2, 2.4, 2.2
    z0, z1 = (z - 0.6, z - 0.6 + L) if facing > 0 else (z + 0.6 - L, z + 0.6)
    box(img, cam, x - Wd / 2, x + Wd / 2, 0, H, z0, z1, STONE_G, STONE_GD, STONE_G)
    side_x = x - Wd / 2 if cam.pos[0] < x else x + Wd / 2
    if abs(cam.pos[0] - x) > Wd / 2 + 0.3:                 # the lettered panel, on a side face we can see
        quad(img, cam, [(side_x, 0.5, z0 + 1.2), (side_x, 0.5, z1 - 1.2), (side_x, 1.6, z1 - 1.2),
                        (side_x, 1.6, z0 + 1.2)], STONE_GD, INK, 1.2)
    base = z0 + 0.4 if facing > 0 else z1 - 0.4

    def P(u, v, dx=0.0):
        return (x + dx, H + v, base + facing * u)
    if cam.depth(P(3.0, 1.5)) < 1.0:
        return
    pen = _pen(img)

    def egg(c, r, n=10):                                    # an egg shape's outline in the frame
        pts = []
        for a in np.linspace(0, math.pi, n):
            for b in np.linspace(0, 2 * math.pi, 2 * n, endpoint=False):
                pts.append(cam.project(P(c[0] + r[0] * math.cos(a), c[1] + r[1] * math.sin(a) * math.cos(b),
                                         c[2] + r[2] * math.sin(a) * math.sin(b)))[0])
        return _hull(pts)

    def rod(a, b, r):                                       # a rounded rod (a leg) between two points
        pts = []
        for c in (a, b):
            for th in np.linspace(0, 2 * math.pi, 14, endpoint=False):
                for ph in (-1.2, 0.0, 1.2):
                    pts.append(cam.project(P(c[0] + r * math.cos(th) * math.cos(ph), c[1] + r * math.sin(th) *
                                             math.cos(ph), c[2] + r * math.sin(ph)))[0])
        return _hull(pts)

    def part(shapes, fill, lw=1.8):                         # several lumps as one solid: ink under, then the fill
        for q in shapes:
            pen.poly(q, INK, INK, lw * 2)
        for q in shapes:
            pen.poly(q, fill, None)
    to_cam = (cam.pos[0] - x, cam.pos[2] - (base + facing * 4.5))
    front = to_cam[1] * facing > -0.3 * abs(to_cam[0])    # the camera ahead of (or beside) his head
    side = 1 if to_cam[0] > 0 else -1                      # which flank we see
    far = [egg(c, r) for c, r in LION_PAWS + LION_BODY if c[2] * side < 0]
    near = [egg(c, r) for c, r in LION_PAWS + LION_BODY if c[2] * side >= 0]
    legs = [rod(a, b, r) for a, b, r in LION_LEGS]
    mane = [egg(c, r) for c, r in LION_MANE]
    if not front:                                           # from behind, his mane is beyond his back
        part(mane, BRONZE_D)
    part(far + legs + near, BRONZE)
    # the near haunch's curve, the tail along the block, the toes
    cam.line(pen, [P(0.4, 0.2, side * 0.92), P(0.7, 1.05, side * 0.95), P(1.6, 1.15, side * 0.93),
                   P(2.0, 0.3, side * 0.9)], BRONZE_L, 1.6)
    cam.line(pen, [P(0.15, 0.1, side * 0.6), P(1.2, 0.05, side * 0.98), P(2.6, 0.05, side * 0.95)], BRONZE_L, 2.0)
    for sg in (-1, 1):
        for d in (-0.1, 0.1):
            cam.line(pen, [P(6.25, 0.05, sg * 0.42 + d), P(6.36, 0.2, sg * 0.42 + d)], INK, 1.2)
    if front:
        part(mane, BRONZE_D)
        c, r = LION_MANE[0]                                 # the mane's locks on the side we see
        for k in range(9):
            b = (k / 8.0 - 0.5) * 2.4
            top = P(c[0] + 0.2 * math.cos(b), c[1] + r[1] * 0.85, c[2] + r[2] * 0.75 * math.sin(b))
            bot = P(c[0] + r[0] * 0.6 * math.cos(b), c[1] - r[1] * 0.75, c[2] + r[2] * 0.85 * math.sin(b))
            mid = P(c[0] + r[0] * 0.95 * math.cos(b), c[1], c[2] + r[2] * 0.98 * math.sin(b))
            if cam.depth(mid) < cam.depth(P(*c)):
                cam.line(pen, [top, mid, bot], BRONZE_L, 1.4)
        part([egg(c, r) for c, r in LION_FACE], BRONZE, 1.6)
        for sg in (-1, 1):                                  # the eyes, under heavy brows
            e = P(5.1, 2.78, sg * 0.24)
            if cam.depth(e) < cam.depth(P(4.7, 2.5, 0.0)) + 0.1:
                (X, Y), k = cam.project(e)
                pen.ell(X, Y, 0.06 * k, 0.04 * k, INK, None)
                cam.line(pen, [P(5.14, 2.9, sg * 0.1), P(5.08, 2.92, sg * 0.38)], INK, 1.4)
        (X, Y), k = cam.project(P(5.56, 2.36, 0.0))        # the nose and the set mouth
        pen.ell(X, Y, 0.12 * k, 0.08 * k, INK, None)
        cam.line(pen, [P(5.48, 2.02, -0.22), P(5.56, 2.08, 0.0), P(5.48, 2.02, 0.22)], INK, 1.4)


def street_furniture(img, cam):
    """Black posts round the column's base and ornate black lamp posts (refs lion-4, column-1)."""
    p = _pen(img)
    for k in range(-5, 6):
        for x, z in ((k * 1.6, -COL_BASE - 1.5), (k * 1.6, COL_BASE + 1.5)):
            if cam.depth((x, 0.5, z)) > 1:
                cam.line(p, [(x, 0, z), (x, 0.9, z)], IRON, 4.0)
    for x, z in ((-10, -12), (10, -12), (-10, 12), (10, 12), (-34, 40), (34, 40), (-34, 4), (34, 4)):
        if cam.depth((x, 3, z)) < 1:
            continue
        cam.line(p, [(x, 0, z), (x, 4.2, z)], IRON, 5.0)
        (X, Y), k = cam.project((x, 4.6, z))
        p.poly([(X - 0.3 * k, Y + 0.4 * k), (X + 0.3 * k, Y + 0.4 * k), (X + 0.38 * k, Y - 0.3 * k), (X, Y - 0.6 * k),
                (X - 0.38 * k, Y - 0.3 * k)], (236, 228, 190), INK, 1.4)
        p.line([(X - 0.3 * k, Y + 0.4 * k), (X + 0.3 * k, Y + 0.4 * k)], IRON, 3.0)


def square_back(img, cam, t):
    """Everything in the square drawn before the people: the sky, the ground and roads, then the buildings, gallery,
    Whitehall, trees and traffic far to near, then the square's edges and the terrace."""
    sky(img, cam, t)
    ground(img, cam)
    for d, fn in sorted(surroundings(cam, t), key=lambda v: -v[0]):
        if d > -60:
            fn(img)
    edges(img, cam)
    terrace(img, cam)


def square_pieces(cam, t):
    """The square's solid pieces as (depth, draw) items, for sorting in with the people: the fountains, the column,
    the lions, the lamp posts."""
    items = []
    for fx, fz in FOUNTAINS:
        items.append((cam.depth((fx, 1, fz)), lambda img, fx=fx, fz=fz: fountain(img, cam, fx, fz, t)))
    items.append((cam.depth((0, 5, 0)), lambda img: (column(img, cam), street_furniture(img, cam))))
    for x, z, f in LIONS:
        items.append((cam.depth((x, 1.5, z + f * 2.5)), lambda img, x=x, z=z, f=f: lion(img, cam, x, z, f)))
    return items


# ------------------------------------------------------------------------------------------------ the van
VAN_L, VAN_W, VAN_H = 5.93, 2.02, 2.7             # sizes 'police van side' / 'police van back'
VAN_NAVY, VAN_NAVY_D = (30, 36, 58), (20, 24, 40)
VAN_YELLOW, VAN_BLUE = (226, 230, 40), (30, 70, 200)
CHEVRON_R = (216, 40, 40)


def van(img, cam, x, z, heading, t, doors=1.0, lights=False):
    """The Met's TSG van (refs van-front, van-back, van-back-open): a tall Sprinter in dark navy, one row of blue and
    yellow checks along the lower sides, POLICE in white along the top, TERRITORIAL SUPPORT GROUP on the rear side
    window, the yellow bonnet, the blue light bar; at the back two tall doors with red and yellow chevrons on the
    lower half, POLICE in red across the top; doors (0 shut .. 1 swung right round to the sides) showing the grey
    caged interior. `heading`: the way its front points (radians, 0 = +x)."""
    ch, sh = math.cos(heading), math.sin(heading)

    def W(u, y, v):                                    # u along the van from its back (0) to its front (L), v across
        return (x + (u - VAN_L / 2) * ch - v * sh, y, z + (u - VAN_L / 2) * sh + v * ch)
    hw = VAN_W / 2
    faces = []
    body_y0, roof = 0.45, VAN_H
    # the box: back, two sides, roof, the cab front (sloped bonnet)
    faces.append(('back', [W(0, body_y0, -hw), W(0, body_y0, hw), W(0, roof, hw), W(0, roof, -hw)]))
    faces.append(('sideL', [W(0, body_y0, hw), W(VAN_L - 0.9, body_y0, hw), W(VAN_L - 0.9, roof, hw), W(0, roof, hw)]))
    faces.append(('sideR', [W(0, body_y0, -hw), W(VAN_L - 0.9, body_y0, -hw), W(VAN_L - 0.9, roof, -hw), W(0, roof, -hw)]))
    faces.append(('roof', [W(0, roof, -hw), W(VAN_L - 0.9, roof, -hw), W(VAN_L - 0.9, roof, hw), W(0, roof, hw)]))
    faces.append(('screen', [W(VAN_L - 0.9, roof, -hw), W(VAN_L - 0.9, roof, hw), W(VAN_L - 0.3, 1.3, hw), W(VAN_L - 0.3, 1.3, -hw)]))
    faces.append(('bonnet', [W(VAN_L - 0.3, 1.3, -hw), W(VAN_L - 0.3, 1.3, hw), W(VAN_L, 1.05, hw), W(VAN_L, 1.05, -hw)]))
    faces.append(('nose', [W(VAN_L, body_y0, -hw), W(VAN_L, body_y0, hw), W(VAN_L, 1.05, hw), W(VAN_L, 1.05, -hw)]))
    faces.append(('cabL', [W(VAN_L - 0.9, body_y0, hw), W(VAN_L, body_y0, hw), W(VAN_L, 1.05, hw), W(VAN_L - 0.3, 1.3, hw),
                           W(VAN_L - 0.9, roof, hw)]))
    faces.append(('cabR', [W(VAN_L - 0.9, body_y0, -hw), W(VAN_L, body_y0, -hw), W(VAN_L, 1.05, -hw), W(VAN_L - 0.3, 1.3, -hw),
                           W(VAN_L - 0.9, roof, -hw)]))

    def facing(pts):
        a, b, c = pts[0], pts[1], pts[2]
        n = np.cross(np.subtract(b, a), np.subtract(c, a))
        ctr = np.mean(pts, axis=0)
        return float(np.dot(n, np.subtract(cam.pos, ctr)))
    centre = W(VAN_L / 2, 1.3, 0)
    vis = []
    for name, pts in faces:
        ctr = np.mean(pts, axis=0)
        out = np.subtract(ctr, centre)
        if np.dot(out, np.subtract(cam.pos, ctr)) > 0:
            vis.append((cam.depth(tuple(ctr)), name, pts))
    # wheels (under everything)
    p = _pen(img)
    for u in (0.9, VAN_L - 1.1):
        for v in (-hw, hw):
            if cam.depth(W(u, 0.36, v)) > 0.5:
                (X, Y), k = cam.project(W(u, 0.36, v))
                p.ell(X, Y, 0.36 * k, 0.36 * k, (24, 24, 26), INK, 1.6)
    for dep, name, pts in sorted(vis, key=lambda v: -v[0]):
        if name == 'back':
            if doors > 0.02:                                    # the open back: the grey caged interior
                quad(img, cam, pts, (150, 154, 160), INK, 1.6)
                quad(img, cam, [W(0.02, body_y0 + 0.05, -hw + 0.1), W(0.02, body_y0 + 0.05, hw - 0.1),
                                W(0.02, roof - 0.1, hw - 0.1), W(0.02, roof - 0.1, -hw + 0.1)], (40, 42, 48), INK, 1.4)
                quad(img, cam, [W(0.03, body_y0 + 0.05, -hw + 0.1), W(0.03, body_y0 + 0.05, hw - 0.1),
                                W(0.03, body_y0 + 0.2, hw - 0.1), W(0.03, body_y0 + 0.2, -hw + 0.1)], (40, 70, 160), None)
                for k in range(6):                              # the cage's bars
                    v = -hw + 0.3 + k * (VAN_W - 0.6) / 5
                    cam.line(p, [W(0.04, body_y0 + 0.3, v), W(0.04, roof - 0.2, v)], (110, 114, 120), 2.0)
            else:
                rear_doors(img, cam, W, hw, body_y0, roof, 0.0)
        elif name in ('sideL', 'sideR'):
            sg = 1 if name == 'sideL' else -1
            quad(img, cam, pts, VAN_NAVY, INK, 1.8)
            v = sg * (hw + 0.005)
            for k in range(8):                                  # the blue and yellow checks, one row
                u0 = 0.15 + k * (VAN_L - 1.1) / 8
                u1 = u0 + (VAN_L - 1.1) / 8
                quad(img, cam, [W(u0, 0.65, v), W(u1, 0.65, v), W(u1, 1.35, v), W(u0, 1.35, v)],
                     VAN_YELLOW if k % 2 == 0 else VAN_BLUE, None)
            for u0, u1 in ((0.3, 1.5), (1.9, 3.4), (3.7, 4.9)):  # tinted windows
                quad(img, cam, [W(u0, 1.6, v), W(u1, 1.6, v), W(u1, 2.3, v), W(u0, 2.3, v)], (40, 44, 56), INK, 1.2)
            if name == 'sideL':
                text3(img, cam, 'POLICE', [W(1.6, 2.62, v), W(3.6, 2.62, v), W(3.6, 2.4, v), W(1.6, 2.4, v)], (246, 246, 246))
            else:
                text3(img, cam, 'POLICE', [W(3.6, 2.62, v), W(1.6, 2.62, v), W(1.6, 2.4, v), W(3.6, 2.4, v)], (246, 246, 246))
        elif name == 'roof':
            quad(img, cam, pts, VAN_NAVY_D, INK, 1.6)
        elif name == 'screen':
            quad(img, cam, pts, (60, 70, 90), INK, 1.6)
        elif name == 'bonnet':
            quad(img, cam, pts, VAN_YELLOW, INK, 1.6)
        elif name == 'nose':
            quad(img, cam, pts, (24, 24, 28), INK, 1.6)
            for v in (-hw + 0.3, hw - 0.3):
                (X, Y), k = cam.project(W(VAN_L + 0.01, 0.85, v))
                p.ell(X, Y, 0.16 * k, 0.1 * k, (236, 236, 220), INK, 1.0)
        else:
            quad(img, cam, pts, VAN_NAVY, INK, 1.6)
            sg = 1 if name == 'cabL' else -1
            quad(img, cam, [W(VAN_L - 0.85, 1.4, sg * (hw + 0.005)), W(VAN_L - 0.4, 1.4, sg * (hw + 0.005)),
                            W(VAN_L - 0.8, 2.3, sg * (hw + 0.005)), W(VAN_L - 0.85, 2.3, sg * (hw + 0.005))], (60, 70, 90), INK, 1.2)
    if doors > 0.02:
        rear_doors(img, cam, W, hw, body_y0, roof, doors)
    # the light bar on the roof (flashing blue when on: flat blue, then dark; never a glow)
    on = lights and int(t * 6) % 2 == 0
    box_pts = [W(VAN_L - 1.3, roof, -0.7), W(VAN_L - 1.0, roof, -0.7), W(VAN_L - 1.0, roof + 0.18, -0.7), W(VAN_L - 1.3, roof + 0.18, -0.7)]
    for v0, v1, ph in ((-0.8, -0.05, 0), (0.05, 0.8, 1)):
        lit = lights and (int(t * 6) + ph) % 2 == 0
        quad(img, cam, [W(VAN_L - 1.3, roof + 0.02, v0), W(VAN_L - 1.0, roof + 0.02, v0), W(VAN_L - 1.0, roof + 0.02, v1),
                        W(VAN_L - 1.3, roof + 0.02, v1)], (80, 160, 255) if lit else (30, 50, 110), INK, 1.2)
        quad(img, cam, [W(VAN_L - 1.0, roof + 0.02, v0), W(VAN_L - 1.0, roof + 0.02, v1), W(VAN_L - 1.0, roof + 0.2, v1),
                        W(VAN_L - 1.0, roof + 0.2, v0)], (130, 200, 255) if lit else (40, 60, 130), INK, 1.2)
    return W


def rear_doors(img, cam, W, hw, y0, roof, open_):
    """The two tall back doors: red and yellow chevrons on the lower half, POLICE in red across the top, a fleet
    number; hinged at the sides, swinging right round to the sides as they open (0 shut, 1 fully open)."""
    for sg in (-1, 1):
        ang = open_ * math.radians(260)
        hinge_v = sg * hw

        def D(w, y):                                         # w across the door from its hinge (0) to its edge (hw)
            u = -math.sin(ang) * w
            v = hinge_v - sg * math.cos(ang) * w
            return W(u, y, v)
        pts = [D(0, y0), D(hw, y0), D(hw, roof), D(0, roof)]
        quad(img, cam, pts, VAN_NAVY, INK, 1.8)
        if open_ > 0.5:
            continue                                         # swung round: we see their inside faces (plain)
        for k in range(4):                                   # the chevrons
            w0, w1 = k * hw / 4, (k + 1) * hw / 4
            quad(img, cam, [D(w0, y0 + 0.1), D(w1, y0 + 0.1), D(w1, 1.45), D(w0, 1.45)],
                 VAN_YELLOW if k % 2 == 0 else CHEVRON_R, None)
        quad(img, cam, [D(0.15, 1.7), D(hw - 0.1, 1.7), D(hw - 0.1, 2.3), D(0.15, 2.3)], (40, 44, 56), INK, 1.2)
        w0, w1 = (hw - 0.05, 0.1) if sg > 0 else (0.1, hw - 0.05)
        text3(img, cam, 'POLICE', [D(w0, 2.6), D(w1, 2.6), D(w1, 2.42), D(w0, 2.42)], CHEVRON_R)


# ------------------------------------------------------------------------------------------------ the rooms
ROOM_X, ROOM_Z, ROOM_H = 2.6, 2.2, 2.7           # the interrogation room: walls at x = +-ROOM_X, z = +-ROOM_Z
TABLE = (1.2, 0.75, 0.74)                         # the metal table: length (x), depth (z), height
DOOR = (0.95, 0.92, 2.04)                         # the door in the back wall (+z): centre x, width, height
WALL_LO, WALL_HI = (70, 84, 80), (104, 116, 110)  # breeze block: darker below, paler above (ref interrogation-3)
CONCRETE = (120, 118, 112)


def room(img, cam, t, door=0.0):
    """The interrogation room (refs interrogation-1..3): breeze-block walls, darker below and paler above, a concrete
    floor with a blue line, the heavy grey metal door with its small window in the back wall (+z), the long dark
    one-way mirror on the left wall (-x), the lamp over the table. `door`: 0 shut .. 1 open (swings out into the corridor)."""
    X, Z, H = ROOM_X, ROOM_Z, ROOM_H
    quad(img, cam, [(-X, 0, -Z), (X, 0, -Z), (X, 0, Z), (-X, 0, Z)], CONCRETE, INK, 1.4)
    p = _pen(img)
    cam.line(p, [(-X + 0.3, 0.005, -Z + 0.3), (-X + 0.3, 0.005, Z - 0.3), (X - 0.3, 0.005, Z - 0.3),
                 (X - 0.3, 0.005, -Z + 0.3)], (40, 90, 170), 3.0)
    quad(img, cam, [(-X, H, -Z), (X, H, -Z), (X, H, Z), (-X, H, Z)], (44, 52, 50), INK, 1.4)    # the dim ceiling
    walls = [('back', [(-X, 0, Z), (X, 0, Z), (X, H, Z), (-X, H, Z)]), ('front', [(X, 0, -Z), (-X, 0, -Z), (-X, H, -Z), (X, H, -Z)]),
             ('left', [(-X, 0, -Z), (-X, 0, Z), (-X, H, Z), (-X, H, -Z)]), ('right', [(X, 0, Z), (X, 0, -Z), (X, H, -Z), (X, H, Z)])]
    for name, pts in walls:
        ctr = np.mean(pts, axis=0)
        if cam.depth(tuple(ctr)) < 0.2:
            continue
        inward = -np.array(ctr) * np.array([1, 0, 1])
        if np.dot(inward, np.subtract(cam.pos, ctr)) < 0:
            continue
        lo = [(q[0], min(q[1], 1.1), q[2]) for q in pts]
        quad(img, cam, pts, WALL_HI, INK, 1.6)
        quad(img, cam, lo, WALL_LO, None)
        a, b = pts[0], pts[1]
        for y in np.arange(0.2, H, 0.2):                     # the breeze-block courses
            cam.line(p, [(a[0], y, a[2]), (b[0], y, b[2])], B.dk(WALL_HI, 0.9), 1.0)
        cam.poly(p, pts, None, INK, 1.6)
        if name == 'left':                                    # the one-way mirror
            quad(img, cam, [(-X + 0.01, 1.0, -1.2), (-X + 0.01, 1.0, 1.2), (-X + 0.01, 2.0, 1.2), (-X + 0.01, 2.0, -1.2)],
                 (34, 38, 44), INK, 2.4)
            cam.line(p, [(-X + 0.02, 1.9, -0.9), (-X + 0.02, 1.2, -0.3)], (70, 76, 86), 2.0)
        if name == 'back':
            door_panel(img, cam, door, Z - 0.01)
    # the lamp on its cord, a cone shade (swaying very slightly: Sam may say no)
    sway = 0.03 * math.sin(t * 1.3)
    cam.line(p, [(0, H, 0), (sway, 1.95, 0)], INK, 1.6)
    (X0, Y0), k = cam.project((sway, 1.95, 0))
    p.poly([(X0 - 0.06 * k, Y0), (X0 + 0.06 * k, Y0), (X0 + 0.22 * k, Y0 + 0.2 * k), (X0 - 0.22 * k, Y0 + 0.2 * k)],
           (60, 66, 64), INK, 1.4)
    p.ell(X0, Y0 + 0.2 * k, 0.22 * k, 0.04 * k, (250, 246, 220), INK, 1.0)


def light_pool(img, cam):
    """The lamp's pool of light on the floor and table: a flat paler shape (no glow); the rest stays dim."""
    pts = [(1.4 * math.cos(a), 0.008, 1.1 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
    quad(img, cam, pts, (164, 160, 150), None)


def door_panel(img, cam, open_, z):
    """The heavy grey metal door, hinged on its left, swinging out into the corridor (Sam, 20 Oct: Jenkins came in
    through the door itself, and the doorway was black, not lit like the corridor); a small square window. Open,
    the doorway shows the lit corridor beyond: the white wall opposite, the pale floor, the red alarm bar, and the
    door itself swung back against the corridor wall."""
    cx, w, h = DOOR
    x0 = cx - w / 2
    ang = open_ * math.radians(100)

    def D(u, y):
        return (x0 + math.cos(ang) * u, y, z + math.sin(ang) * u)

    def slab(im):
        quad(im, cam, [D(0, 0), D(w, 0), D(w, h), D(0, h)], (140, 142, 146), INK, 2.0)
        quad(im, cam, [D(0.3, 1.45), D(0.62, 1.45), D(0.62, 1.75), D(0.3, 1.75)], (40, 44, 52), INK, 1.4)
        (X, Y), k = cam.project(D(w - 0.1, 1.0))
        _pen(im).ell(X, Y, 0.04 * k, 0.04 * k, (60, 60, 66), INK, 1.0)
    if open_ <= 0.01:
        slab(img)
        return
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    far, a, b = z + CORR_W, x0 - 4.0, x0 + w + 4.0
    quad(lay, cam, [(a, 0, z), (b, 0, z), (b, 0, far), (a, 0, far)], (196, 196, 192), INK, 1.4)
    quad(lay, cam, [(a, CORR_H, z), (b, CORR_H, z), (b, CORR_H, far), (a, CORR_H, far)], (236, 236, 232), INK, 1.4)
    quad(lay, cam, [(a, 0, far), (b, 0, far), (b, CORR_H, far), (a, CORR_H, far)], (240, 240, 236), INK, 1.6)
    cam.line(_pen(lay), [(a, 0.95, far - 0.01), (b, 0.95, far - 0.01)], (200, 40, 40), 3.0)
    slab(lay)
    clip_to_doorway(lay, cam, z)
    img.alpha_composite(lay)
    quad(img, cam, [(x0, 0, z), (x0 + w, 0, z), (x0 + w, h, z), (x0, h, z)], None, INK, 1.8)


def clip_to_doorway(lay, cam, z):
    """Keep only what shows through the doorway (for the corridor beyond it, and Jenkins until he is through)."""
    from PIL import ImageChops, ImageDraw
    cx, w, h = DOOR
    x0 = cx - w / 2
    pts = [cam.project(q)[0] for q in [(x0, 0, z), (x0 + w, 0, z), (x0 + w, h, z), (x0, h, z)]]
    mask = Image.new('L', lay.size, 0)
    ImageDraw.Draw(mask).polygon([(X * B.SS, Y * B.SS) for X, Y in pts], fill=255)
    lay.putalpha(ImageChops.multiply(lay.split()[3], mask))


def table(img, cam):
    """The grey metal table on steel legs (under the lamp)."""
    L, Dp, H = TABLE
    for x in (-L / 2 + 0.05, L / 2 - 0.05):
        for z in (-Dp / 2 + 0.05, Dp / 2 - 0.05):
            cam.line(_pen(img), [(x, 0, z), (x, H, z)], (120, 124, 130), 3.0)
    box(img, cam, -L / 2, L / 2, H - 0.04, H, -Dp / 2, Dp / 2, (176, 180, 184), (130, 134, 140), (130, 134, 140))


def chair(img, cam, x, z, facing):
    """A plain chair: wooden seat and back on a metal frame (ref interrogation-1)."""
    p = _pen(img)
    fx, fz = facing
    for dx, dz in ((-0.2, -0.2), (0.2, -0.2), (-0.2, 0.2), (0.2, 0.2)):
        cam.line(p, [(x + dx, 0, z + dz), (x + dx, 0.45, z + dz)], (110, 114, 120), 2.4)
    box(img, cam, x - 0.22, x + 0.22, 0.43, 0.47, z - 0.22, z + 0.22, (176, 128, 74), (140, 96, 52), (140, 96, 52))
    bx, bz = x - fx * 0.22, z - fz * 0.22
    nx, nz = -fz, fx
    quad(img, cam, [(bx - nx * 0.2, 0.62, bz - nz * 0.2), (bx + nx * 0.2, 0.62, bz + nz * 0.2),
                    (bx + nx * 0.2, 0.86, bz + nz * 0.2), (bx - nx * 0.2, 0.86, bz - nz * 0.2)], (176, 128, 74), INK, 1.4)


CORR_W, CORR_L, CORR_H = 2.4, 16.0, 2.6           # the custody corridor (ref corridor): x across, z along


def corridor(img, cam, t):
    """The custody corridor (ref corridor): white walls, heavy dark grey cell doors with hatches and signs, red alarm
    bars along the walls, strip lights down the ceiling, a pale grey speckled floor, a door at the far end. The
    interrogation room's door is on the left wall at z = 0 (the same door, seen from outside)."""
    W, L, H = CORR_W / 2, CORR_L, CORR_H
    quad(img, cam, [(-W, 0, -2), (W, 0, -2), (W, 0, L), (-W, 0, L)], (196, 196, 192), INK, 1.4)
    p = _pen(img)
    rng = np.random.default_rng(2)
    for _ in range(80):                                       # the speckle
        x, z = rng.uniform(-W, W), rng.uniform(-1.5, L)
        cam.line(p, [(x, 0.005, z), (x + 0.04, 0.005, z)], (160, 160, 156), 1.4)
    quad(img, cam, [(-W, H, -2), (W, H, -2), (W, H, L), (-W, H, L)], (236, 236, 232), INK, 1.4)
    for z in np.arange(0, L, 3.0):                            # strip lights
        quad(img, cam, [(-0.15, H - 0.01, z), (0.15, H - 0.01, z), (0.15, H - 0.01, z + 1.2), (-0.15, H - 0.01, z + 1.2)],
             (252, 252, 246), INK, 1.0)
    for sg in (-1, 1):
        x = sg * W
        quad(img, cam, [(x, 0, -2), (x, 0, L), (x, H, L), (x, H, -2)], (240, 240, 236), INK, 1.6)
        cam.line(p, [(x - sg * 0.01, 0.95, -2), (x - sg * 0.01, 0.95, L)], (200, 40, 40), 3.0)   # the alarm bar
        for k, z in enumerate(np.arange(2.5 if sg < 0 else 1.0, L - 1, 3.2)):
            cell_door(img, cam, x - sg * 0.01, z, sg)
    quad(img, cam, [(-W, 0, L), (W, 0, L), (W, H, L), (-W, H, L)], (232, 232, 228), INK, 1.6)          # the far wall
    quad(img, cam, [(W, 0, -2), (-W, 0, -2), (-W, H, -2), (W, H, -2)], (232, 232, 228), INK, 1.6)      # the near end
    quad(img, cam, [(0.5, 0, -1.99), (-0.5, 0, -1.99), (-0.5, 2.0, -1.99), (0.5, 2.0, -1.99)], (90, 94, 100), INK, 1.6)
    text3(img, cam, 'CUSTODY', [(-0.45, 2.35, -1.98), (0.45, 2.35, -1.98), (0.45, 2.15, -1.98), (-0.45, 2.15, -1.98)],
          (40, 44, 52))
    quad(img, cam, [(-0.5, 0, L - 0.01), (0.5, 0, L - 0.01), (0.5, 2.0, L - 0.01), (-0.5, 2.0, L - 0.01)], (90, 94, 100), INK, 1.6)
    # the interrogation room's door on the left wall at z = 0
    quad(img, cam, [(-W + 0.01, 0, -0.46), (-W + 0.01, 0, 0.46), (-W + 0.01, 2.04, 0.46), (-W + 0.01, 2.04, -0.46)],
         (140, 142, 146), INK, 2.0)
    quad(img, cam, [(-W + 0.02, 1.45, -0.16), (-W + 0.02, 1.45, 0.16), (-W + 0.02, 1.75, 0.16), (-W + 0.02, 1.75, -0.16)],
         (40, 44, 52), INK, 1.4)
    text3(img, cam, 'INTERVIEW 2', [(-W + 0.02, 2.35, 0.4), (-W + 0.02, 2.35, -0.4), (-W + 0.02, 2.15, -0.4), (-W + 0.02, 2.15, 0.4)],
          (40, 44, 52))


def cell_door(img, cam, x, z, sg):
    """A heavy cell door: dark grey, a hatch, a small sign, a handle."""
    quad(img, cam, [(x, 0, z - 0.45), (x, 0, z + 0.45), (x, 2.1, z + 0.45), (x, 2.1, z - 0.45)], (86, 90, 96), INK, 1.6)
    quad(img, cam, [(x - sg * 0.005, 1.0, z - 0.2), (x - sg * 0.005, 1.0, z + 0.2), (x - sg * 0.005, 1.3, z + 0.2),
                    (x - sg * 0.005, 1.3, z - 0.2)], (60, 62, 68), INK, 1.2)
    quad(img, cam, [(x - sg * 0.005, 1.5, z - 0.15), (x - sg * 0.005, 1.5, z + 0.15), (x - sg * 0.005, 1.75, z + 0.15),
                    (x - sg * 0.005, 1.75, z - 0.15)], (236, 236, 226), INK, 1.0)


# ------------------------------------------------------------------------------------------------ test
if __name__ == '__main__':
    if sys.argv[1] == 'test':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        B.SS = 1
        shots = {
            'square-wide': Cam3((0.0, 12.0, 70.0), (0.0, 6.0, 0.0), focal=900),
            'square-low': Cam3((6.0, 1.6, 34.0), (0.0, 4.0, 0.0), focal=1100),
            'lion-police': Cam3((-2.0, 1.7, 26.0), (9.0, 1.8, 10.0), focal=1300),
            'throw-side': Cam3((-20.0, 5.0, 52.0), (-34.0, 2.0, 26.0), focal=1000),
        }
        for name, cam in shots.items():
            img = B.canvas((0, 0, 0))
            square_back(img, cam, 0.0)
            for d, fn in sorted(square_pieces(cam, 0.0), key=lambda v: -v[0]):
                fn(img)
            if name == 'throw-side':
                van(img, cam, -44.0, 28.0, math.pi, 0.0, doors=1.0)
            img.convert('RGB').save(os.path.join(out, name + '.jpg'), quality=85)
        cam = Cam3((1.6, 1.5, -2.0), (-0.2, 1.0, 0.6), focal=1000)
        img = B.canvas((0, 0, 0))
        room(img, cam, 0.0, 0.0)
        light_pool(img, cam)
        table(img, cam)
        chair(img, cam, 0.0, 0.75, (0.0, -1.0))
        chair(img, cam, 0.0, -0.75, (0.0, 1.0))
        img.convert('RGB').save(os.path.join(out, 'room.jpg'), quality=85)
        cam = Cam3((0.6, 1.6, 8.0), (-0.4, 1.4, -1.0), focal=1000)
        img = B.canvas((0, 0, 0))
        corridor(img, cam, 0.0)
        img.convert('RGB').save(os.path.join(out, 'corridor.jpg'), quality=85)
        cam = Cam3((-6.0, 1.7, 6.0), (0.0, 1.3, 0.0), focal=1300)
        img = B.canvas((180, 180, 180))
        van(img, cam, 0.0, 0.0, 0.0, 0.0, doors=0.0, lights=True)
        img.convert('RGB').save(os.path.join(out, 'van.jpg'), quality=85)
