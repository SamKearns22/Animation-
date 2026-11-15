#!/usr/bin/env python3
"""Protest Tiers: the four places, one flat painting per locked camera (sets stage, chat 9, 15 Nov).

MAP
  cameras ........... CAMS: one level pinhole camera per tier in metres (x right, d away, z up); p(x, d, z), ppm(d)
  helpers ........... shape() (flat fill + ink outline round a union of polygons), bands(), quad(), wall()
  fire / smoke ...... flames(t) three-tone tongues; smoke() lumps with a lit side; the moves stage animates both
  t1 ................ Passeig de Gracia at dusk, wet: long lens from 12 m behind the march; Modernista fronts, the
                      domed corner, plane trees, Falques lamps; the burning street container
  t2 ................ Frankfurt at night, wet: the gun store square on; steel shutter (open 0.5-1) and the glass
                      ('whole', 'starred', 'gone') as states; WAFFEN band; doorway left, shuttered shop right
  t3 ................ Place de la Republique, day, camera 0.8 m: Marianne on her drum, reliefs, three seated
                      figures, the lion; Haussmann fronts; plane trees; black smoke beyond; kiosk, bike heap, the car
  t4 ................ Tirana avenue at dusk under a burning sky: the bank (left), the Education Ministry (rounded
                      corner bay, grey balconies, roof flag), pastel blocks and pines down to the hills
  SET_BOXES/MEANT ... rule 83, per tier; BENCHMARK (rule 3) per tier, ticked on the sheet
  sheet ............. each painting beside its references with its BENCHMARK list; blue 1.75 m marks where people go

    python3 source/protest_tiers_sets.py sheet OUT.jpg     the sets sheet for Sam
    python3 source/protest_tiers_sets.py alone OUTDIR      each painting full size (t1..t4.png)
    python3 source/protest_tiers_sets.py check             rule 83 overlaps

Every painting is drawn fresh for a time t (fires flicker); `paint(tier, t, **state)` returns (back, front): front is
an RGBA layer drawn over the people (T3: the car's near corner), or None.
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import burnham as B                 # noqa: E402
import islamocommunism_set as IS    # noqa: E402  (pen, wob, poly, blob: the house's hand-cut shapes)
from ed import INK                  # noqa: E402

W, H = 1080, 1920
REFS = os.path.join(ROOT, 'references', 'protest-tiers')
poly, blob = IS.poly, IS.blob

FIRE_R, FIRE_O, FIRE_Y, FIRE_L = (214, 62, 30), (246, 142, 36), (255, 222, 110), (120, 30, 22)


# ------------------------------------------------------------------------------------------------- cameras
class Cam:
    """A level pinhole camera: horizon at VY, centre line at VX, focal F px, height CH m."""
    def __init__(self, VX, VY, F, CH):
        self.VX, self.VY, self.F, self.CH = VX, VY, F, CH

    def p(self, x, d, z=0.0):
        return self.VX + self.F * x / d, self.VY + self.F * (self.CH - z) / d

    def ppm(self, d):
        return self.F / d


# T1: long lens from a 12 m balcony; the police line at d 185 (officers ~65 px), frame 29 m wide there.
# T2: a phone held up at 2.6 m on the near pavement, square to the gun store 14 m away (150 px a metre there).
# T3: 0.8 m off the paving; Marianne's monument 80 m away (24 px a metre), her head at y ~550.
# T4: 2.8 m, down the avenue; the shield line at d ~17 (115 px a metre), the ministry's corner at d 80.
CAMS = {'t1': Cam(480, 400, 6882, 12.0), 't2': Cam(480, 783, 2100, 2.6),
        't3': Cam(480, 1130, 1920, 0.8), 't4': Cam(470, 960, 2000, 2.8)}
SET_CAM = CAMS


# ------------------------------------------------------------------------------------------------- helpers
def _mask(polys, size=(W, H)):
    m = Image.new('L', size, 0)
    d = ImageDraw.Draw(m)
    for p in polys:
        if len(p) > 2:
            d.polygon([(float(x), float(y)) for x, y in p], fill=255)
    return m


def shape(img, polys, fill, line=INK, lw=3, clip=None):
    """One flat shape: the union of polys filled, with ONE outline round the whole (none inside). clip: a mask it
    stays inside (a lit patch on smoke). Returns the mask."""
    m = _mask(polys)
    if clip is not None:
        m = Image.fromarray(np.minimum(np.asarray(m), np.asarray(clip)))
    if line:
        k = 2 * int(round(lw / 2)) + 1
        img.paste(line, mask=m.filter(ImageFilter.MaxFilter(k)))
    img.paste(fill, mask=m)
    return m


def quad(img, a, b, c, d, fill, line=INK, lw=2.4, amt=1.2):
    poly(img, [a, b, c, d], fill, line, lw, amt)


def bands(img, y0, y1, colours, seed=0, amp=10, line=None):
    """Flat sky (or water) bands top to bottom with hand-cut wavy edges between them."""
    rng = np.random.default_rng(seed)
    n = len(colours)
    img.paste(colours[0], (0, int(y0), W, int(y1)))
    for i in range(1, n):
        yb = y0 + (y1 - y0) * i / n
        ph, f = rng.uniform(0, 6.3), rng.uniform(1.5, 3.0)
        top = [(x, yb + amp * math.sin(x / W * f * 6.28 + ph) + amp * .4 * math.sin(x / 90 + ph * 2))
               for x in np.linspace(-10, W + 10, 40)]
        shape(img, [top + [(W + 10, y1), (-10, y1)]], colours[i], line)


def glow_disc(img, x, y, r, colour, steps=3):
    """A flat light halo (lamps): a few stepped rings, lighter to the middle, no outline."""
    base = np.asarray(img.convert('RGB'), np.float32)
    for k in range(steps):
        rr = r * (1 - k / steps)
        m = np.asarray(_mask([[(x + rr * math.cos(a), y + rr * math.sin(a)) for a in np.linspace(0, 6.28, 28)]]),
                       np.float32)[..., None] / 255 * 0.22
        base = base * (1 - m) + np.array(colour, np.float32) * m
    img.paste(Image.fromarray(base.astype(np.uint8)).convert('RGBA'))


def mix(a, b, u):
    return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))


def text(img, xy, s, size, fill, anchor='mm', font='DejaVuSans-Bold.ttf'):
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', font), size)
    ImageDraw.Draw(img).text(xy, s, font=f, fill=fill, anchor=anchor)


# ------------------------------------------------------------------------------------------------- fire, smoke
def flames(img, x, y, w, h, t=0.0, seed=0, n=5, line=FIRE_L):
    """A fire standing on (x - w/2 .. x + w/2, y), h tall: red tongues with one dark-red outline, an orange body, a
    yellow core; every tongue sways and breathes on its own beat (the moves stage drives t)."""
    rng = np.random.default_rng(seed)
    off = np.sort(rng.uniform(-.42, .42, n))
    hs = rng.uniform(.55, 1.0, n)
    hs[n // 2] = 1.0
    ph = rng.uniform(0, 6.28, (n, 2))

    def tongues(k):
        out = []
        for i in range(n):
            cx = x + off[i] * w
            hh = h * hs[i] * k * (.86 + .14 * math.sin(6.28 * 2.3 * t + ph[i, 0]))
            ww = w / n * .95 * (.55 + .45 * k)
            sw = w * .10 * math.sin(6.28 * 1.6 * t + ph[i, 1])
            out.append([(cx - ww, y), (cx - ww * .95, y - hh * .32), (cx - ww * .4 + sw * .5, y - hh * .68),
                        (cx + sw, y - hh), (cx + ww * .45 + sw * .5, y - hh * .62), (cx + ww * .95, y - hh * .3),
                        (cx + ww, y)])
        return out
    shape(img, tongues(1.0), FIRE_R, line, max(2, w / 70))
    shape(img, tongues(.7), FIRE_O, None)
    shape(img, tongues(.4), FIRE_Y, None)


def smoke(img, lumps, tone, lit, line=INK, lw=3):
    """Smoke as one lumpy shape (lumps = [(x, y, r)]), its lit side up and left kept inside the outline."""
    m = shape(img, [blob(x, y, r, 7 + i) for i, (x, y, r) in enumerate(lumps)], tone, line, lw)
    shape(img, [blob(x - r * .25, y - r * .28, r * .55, 50 + i) for i, (x, y, r) in enumerate(lumps)], lit, None,
          clip=m)


def person_mark(img, cam, x, d, label=None):
    """A blue 1.75 m outline where a person stands (rough.py's mark): shows the true size at that depth."""
    (bx, by), (_, ty) = cam.p(x, d), cam.p(x, d, 1.75)
    h = by - ty
    dr = ImageDraw.Draw(img)
    dr.ellipse((bx - h * .07, ty, bx + h * .07, ty + h * .15), outline=(40, 110, 255), width=2)
    dr.rectangle((bx - h * .12, ty + h * .16, bx + h * .12, by), outline=(40, 110, 255), width=2)


# ================================================================================================= T1
T1_SKY = [(58, 60, 108), (86, 80, 134), (138, 98, 142), (196, 124, 130), (236, 162, 118)]
STONE = [(150, 128, 122), (168, 142, 128), (138, 120, 120), (176, 150, 132), (128, 112, 116)]
WIN_D, WIN_L = (50, 44, 60), (250, 204, 118)
ROAD_W, ROAD_L = (88, 82, 104), (132, 116, 146)
TREE_D, TREE_L = (52, 66, 54), (78, 92, 64)


def _t1_block(img, cam, s, d0, d1, h, tone, seed):
    """One block of fronts on side s (-1 left, +1 right) at x = 30.5 s, depths d0-d1: floors, bays, lit windows."""
    x = 30.5 * s
    a, b, c, e = cam.p(x, d0), cam.p(x, d1), cam.p(x, d1, h), cam.p(x, d0, h)
    quad(img, a, b, c, e, tone)
    rng = np.random.default_rng(seed)
    dark = mix(tone, (30, 26, 40), .35)
    # shop floor: a dark band with lit shop windows
    quad(img, a, b, cam.p(x, d1, 4.5), cam.p(x, d0, 4.5), dark, None)
    for k in np.arange(d0 + 2, d1 - 2, 6):
        quad(img, cam.p(x, k, .4), cam.p(x, k + 3, .4), cam.p(x, k + 3, 3.6), cam.p(x, k, 3.6),
             (240, 196, 120) if rng.random() < .6 else (90, 80, 96), None, amt=0)
    # floors: balcony rails as dark lines; bays (Modernista tribunes) as lighter strips
    for fl in np.arange(4.5, h - 3, 3.4):
        poly(img, [cam.p(x, d0, fl), cam.p(x, d1, fl)], None, (60, 50, 66), 1.6, 0)
        for k in np.arange(d0 + 3, d1 - 2, 5.5):
            lit = rng.random() < .22
            quad(img, cam.p(x, k, fl + .7), cam.p(x, k + 1.6, fl + .7), cam.p(x, k + 1.6, fl + 2.7),
                 cam.p(x, k, fl + 2.7), WIN_L if lit else WIN_D, None, amt=0)
    # cornice and roof edge
    quad(img, cam.p(x, d0, h - .8), cam.p(x, d1, h - .8), c, e, mix(tone, (255, 230, 200), .18), INK, 2)


def t1(t=0.0, marks=False):
    cam = CAMS['t1']
    img = Image.new('RGBA', (W, H), T1_SKY[0] + (255,))
    bands(img, 0, cam.VY + 30, T1_SKY, seed=1, amp=12)
    # lit clouds low in the sky wedge
    for i, (x, y, r) in enumerate(((350, 250, 70), (470, 236, 60), (610, 262, 74), (560, 205, 40))):
        shape(img, [blob(x, y, r, 30 + i, squash=.45)], (226, 150, 140), (120, 80, 110), 2)
    # far end (Diagonal, ~1.3 km): a low line of fronts across the horizon, and far trees
    shape(img, [[(0, cam.VY + 4)] + [(x, cam.VY - 22 - 10 * math.sin(x / 37) - 6 * (x % 90 < 30))
                                     for x in range(0, W + 30, 30)] + [(W, cam.VY + 4)]], (110, 90, 118), INK, 2)
    # the avenue: wet road (it holds the dusk sky), pavements under the trees
    far = 1600
    quad(img, cam.p(-30.5, 60), cam.p(30.5, 60), cam.p(30.5, far), cam.p(-30.5, far), ROAD_W, None, amt=0)
    for s in (-1, 1):
        quad(img, cam.p(s * 30.5, 60), cam.p(s * 18, 60), cam.p(s * 18, far), cam.p(s * 30.5, far), (104, 96, 112),
             None, amt=0)
    # the dusk sky in the wet road (long soft streaks) and the lane lines
    for k, xx in enumerate((-9, -3.5, 3.5, 9)):
        quad(img, cam.p(xx - .08, 186), cam.p(xx + .08, 186), cam.p(xx + .08, far), cam.p(xx - .08, far),
             (196, 186, 206), None, amt=0)
    for xx in (-14, -6, 1, 7, 13):
        quad(img, cam.p(xx - 1.4, 200), cam.p(xx + 1.4, 200), cam.p(xx + .9, 700), cam.p(xx - .9, 700), ROAD_L, None)
    # fronts both sides, blocks of 113 m with 20 m cross streets (Eixample), nearest first hidden off frame
    for s in (-1, 1):
        blocks = [(d, min(d + 113, 1400)) for d in np.arange(254, 1400, 133)]
        for i, (d0, d1) in enumerate(reversed(blocks)):
            _t1_block(img, cam, s, d0, d1, 24 + 3 * ((i + (s > 0)) % 3), STONE[(i * 2 + (s > 0)) % 5], 10 * i + s + 1)
    # the domed corner (es1): a round tower on the right-hand corner at d 520, its dome over the roofline
    cx, by = cam.p(30.5, 520)
    _, ty = cam.p(30.5, 520, 27)
    k = cam.ppm(520)
    quad(img, (cx - 4.2 * k, by), (cx + 4.2 * k, by), (cx + 4.2 * k, ty), (cx - 4.2 * k, ty), (184, 156, 136))
    for fl in np.arange(4.5, 26, 3.4):
        _, fy = cam.p(30.5, 520, fl)
        poly(img, [(cx - 4.2 * k, fy), (cx + 4.2 * k, fy)], None, (90, 72, 80), 1.6, 0)
        for dx in (-2.6, 0, 2.6):
            quad(img, (cx + (dx - .6) * k, fy - 2.6 * k), (cx + (dx + .6) * k, fy - 2.6 * k), (cx + (dx + .6) * k,
                 fy - .6 * k), (cx + (dx - .6) * k, fy - .6 * k), WIN_L if dx == 0 and fl > 15 else WIN_D, None, amt=0)
    dome = [(cx + 4.6 * k * math.cos(a), ty - 6.5 * k * math.sin(a)) for a in np.linspace(0, math.pi, 16)]
    shape(img, [dome + [(cx - 4.6 * k, ty + 2)]], (96, 104, 112), INK, 2.4)
    poly(img, [(cx - 3.4 * k, ty - 3.5 * k), (cx + 3.4 * k, ty - 3.5 * k)], None, (150, 160, 150), 2, 0)
    poly(img, [(cx, ty - 6.5 * k), (cx, ty - 9.5 * k)], None, INK, 2, 0)
    shape(img, [[(cx + 1.2 * k * math.cos(a), ty - 9.5 * k + 1.2 * k * math.sin(a)) for a in np.linspace(0, 6.3, 12)]],
          (200, 170, 90), INK, 1.5)
    # plane trees in two rows each side (x 19, 23), far to near; Falques lamps between them
    for d in np.arange(1300, 250, -9):
        for s in (-1, 1):
            for xx in (19, 23):
                if (d // 9 + xx) % 2:
                    continue
                k = cam.ppm(d)
                bx, by = cam.p(s * xx, d)
                if bx < -80 or bx > W + 80:
                    continue
                tx, ty = cam.p(s * xx, d, 8.5)
                poly(img, [(bx - .25 * k, by), (bx + .25 * k, by), (tx + .2 * k, ty), (tx - .2 * k, ty)], (96, 86, 78),
                     INK, 1.4, 0)
                r = 4.0 * k
                m = shape(img, [blob(tx, ty - r * .5, r, int(d) + xx + s, squash=.8)], TREE_D, INK, 2)
                shape(img, [blob(tx - r * .3, ty - r * .85, r * .6, int(d) + 3)], TREE_L, None, clip=m)
        if d % 27 < 9:
            for s in (-1, 1):
                k = cam.ppm(d)
                bx, by = cam.p(s * 16.5, d)
                if -60 < bx < W + 60:
                    _falques(img, bx, by, k)
    # the burning street container just short of the line (d 165), with its fire
    _container(img, cam, 0.6, 165, t)
    if marks:
        for x in np.arange(-11, 15, 2.8):
            person_mark(img, cam, x, 185)
        for x in (-3, -1.6, 2.4, 3.6):
            person_mark(img, cam, x, 160)
        for x in (-4, 0, 4):
            person_mark(img, cam, x, 110)
    return img, None


def _falques(img, bx, by, k):
    """The Passeig's ornate double lamp (Falques): a dark iron post 5.5 m, a scrolled arm, two lantern heads, lit."""
    top = by - 5.5 * k
    poly(img, [(bx - .14 * k, by), (bx + .14 * k, by), (bx + .08 * k, top), (bx - .08 * k, top)], (44, 40, 50), INK,
         1.2, 0)
    for s in (-1, 1):
        hx, hy = bx + s * .9 * k, top + .25 * k
        poly(img, [(bx, top + .6 * k), (bx + s * .5 * k, top - .1 * k), (hx, hy)], None, (44, 40, 50), 1.6, 0)
        glow_disc(img, hx, hy + .3 * k, 1.6 * k, (255, 214, 140))
        shape(img, [[(hx - .3 * k, hy), (hx + .3 * k, hy), (hx + .2 * k, hy + .7 * k), (hx - .2 * k, hy + .7 * k)]],
              (255, 226, 150), INK, 1.2)


def _container(img, cam, x, d, t):
    """A Barcelona street container (grey-green, 2.2 x 1.5 m), side on, wheels, the lid thrown open; burning."""
    k = cam.ppm(d)
    bx, by = cam.p(x, d)
    w, h = 2.2 * k, 1.45 * k
    flames(img, bx + .1 * k, by - h * .9, w * 1.25, 3.4 * k, t, seed=4)
    quad(img, (bx - w / 2, by - .2 * k), (bx + w / 2, by - .2 * k), (bx + w / 2 * .94, by - h), (bx - w / 2 * .94, by - h),
         (78, 98, 84))
    poly(img, [(bx - w / 2 * .94, by - h), (bx - w / 2 * 1.15, by - h - .6 * k)], None, (60, 78, 66), 4, 0)
    for s in (-1, 1):
        IS.ell(img, bx + s * w * .34, by - .12 * k, .14 * k, .14 * k, (30, 28, 34), INK, 1.5)
    poly(img, [(bx - w * .4, by - h * .55), (bx + w * .4, by - h * .55)], None, (56, 72, 62), 1.6, 0)


# ================================================================================================= T2
T2_WALL, T2_TRIM, T2_DARK = (58, 56, 70), (82, 80, 96), (28, 28, 36)
SHELF, GUN, INSIDE = (236, 232, 216), (44, 44, 50), (250, 246, 228)


def t2(t=0.0, shutter=0.5, glass='whole', marks=False):
    """shutter: how far up the steel shutter is (0.5 half, as the scene opens; 1 hauled right up)."""
    cam = CAMS['t2']
    img = Image.new('RGBA', (W, H), T2_WALL + (255,))
    k = cam.ppm(14)
    X = lambda x: cam.p(x, 14)[0]                          # noqa: E731
    Y = lambda z: cam.p(0, 14, z)[1]                       # noqa: E731
    # the building: plaster, a first-floor sill, upper windows (one lit), a stone plinth course
    for x0 in (-3.0, -0.4, 2.2):
        quad(img, (X(x0), Y(7.4)), (X(x0 + 1.3), Y(7.4)), (X(x0 + 1.3), Y(5.0)), (X(x0), Y(5.0)),
             (238, 196, 120) if x0 == 2.2 else (34, 34, 44), INK, 2)
        quad(img, (X(x0 - .15), Y(5.0)), (X(x0 + 1.45), Y(5.0)), (X(x0 + 1.45), Y(4.8)), (X(x0 - .15), Y(4.8)), T2_TRIM)
    quad(img, (0, Y(4.45)), (W, Y(4.45)), (W, Y(4.3)), (0, Y(4.3)), T2_TRIM, INK, 2)
    # left neighbour: a recessed doorway, house number, bell plate
    quad(img, (X(-3.4), Y(0)), (X(-2.45), Y(0)), (X(-2.45), Y(2.6)), (X(-3.4), Y(2.6)), T2_DARK)
    quad(img, (X(-2.8), Y(1.5)), (X(-2.6), Y(1.5)), (X(-2.6), Y(1.0)), (X(-2.8), Y(1.0)), (150, 150, 160), INK, 1.5)
    text(img, (X(-2.9), Y(2.95)), '22', int(.32 * k), (220, 220, 230))
    # right neighbour: a closed shop, its roller shutter down, tags sprayed on it
    quad(img, (X(2.45), Y(0)), (X(4.4), Y(0)), (X(4.4), Y(3.4)), (X(2.45), Y(3.4)), (112, 114, 124))
    for z in np.arange(.2, 3.3, .18):
        poly(img, [(X(2.45), Y(z)), (X(4.4), Y(z))], None, (88, 90, 100), 1.2, 0)
    for i, (x, z) in enumerate(((2.8, 1.4), (3.5, 2.1), (3.1, .7))):
        poly(img, [(X(x + .25 * j), Y(z + .25 * math.sin(j * 2.1 + i))) for j in range(5)], None,
             [(220, 70, 150), (70, 200, 220), (240, 220, 80)][i], 4, 0)
    # the gun store: dark mosaic-tiled base (de3), the big window, the shutter box, the WAFFEN band
    x0, x1 = -2.0, 2.0
    quad(img, (X(x0 - .2), Y(0)), (X(x1 + .2), Y(0)), (X(x1 + .2), Y(.45)), (X(x0 - .2), Y(.45)), (36, 40, 46))
    for z in (.15, .3):
        poly(img, [(X(x0 - .2), Y(z)), (X(x1 + .2), Y(z))], None, (60, 66, 72), 1, 0)
    for x in np.arange(x0 - .2, x1 + .2, .15):
        poly(img, [(X(x), Y(0)), (X(x), Y(.45))], None, (60, 66, 72), 1, 0)
    quad(img, (X(x0 - .2), Y(2.9)), (X(x1 + .2), Y(2.9)), (X(x1 + .2), Y(.45)), (X(x0 - .2), Y(.45)), (30, 30, 34))
    _window(img, X, Y, x0, x1, glass)
    _shutter(img, X, Y, x0, x1, shutter)
    quad(img, (X(x0 - .35), Y(3.55)), (X(x1 + .35), Y(3.55)), (X(x1 + .35), Y(4.25)), (X(x0 - .35), Y(4.25)),
         (26, 52, 46), INK, 3)
    text(img, ((X(x0) + X(x1)) / 2, Y(3.9)), 'WAFFEN', int(.5 * k), (238, 236, 226))
    # the street lamp at the near kerb, left, and its light on the wet pavement
    lx = X(-2.9) - 30
    _, lb = cam.p(0, 12.2)
    poly(img, [(lx - 5, lb), (lx + 5, lb), (lx + 3, cam.p(0, 12.2, 6)[1]), (lx - 3, cam.p(0, 12.2, 6)[1])],
         (40, 40, 48), INK, 1.5, 0)
    lh = cam.p(0, 12.2, 6)[1]
    poly(img, [(lx, lh), (lx + 70, lh - 10)], None, (40, 40, 48), 5, 0)
    glow_disc(img, lx + 70, lh + 8, 120, (255, 220, 150))
    shape(img, [[(lx + 48, lh - 6), (lx + 92, lh - 14), (lx + 86, lh + 6), (lx + 54, lh + 8)]], (255, 232, 170), INK, 2)
    # far pavement (wet), kerb, road; the window and lamp mirrored in the wet as broken streaks
    pv0, pv1 = cam.p(0, 14)[1], cam.p(0, 12)[1]
    img.paste((70, 70, 84), (0, int(pv0), W, int(pv1)))
    quad(img, (0, pv1), (W, pv1), (W, pv1 + 10), (0, pv1 + 10), (110, 110, 124), INK, 2)
    img.paste((40, 40, 52), (0, int(pv1 + 10), W, H))
    rng = np.random.default_rng(5)
    for xx in np.arange(X(x0) + 12, X(x1) - 12, 26):
        for y in np.arange(pv0 + 6, 1500, 34):
            if rng.random() < .55:
                L = rng.uniform(10, 26)
                shape(img, [[(xx - 3, y), (xx + 3, y), (xx + 2, y + L), (xx - 2, y + L)]],
                      mix((236, 226, 196), (40, 40, 52), (y - pv0) / 560), None)
    for y in np.arange(pv0 + 4, 1480, 30):
        if rng.random() < .7:
            shape(img, [[(lx + 64, y), (lx + 76, y), (lx + 74, y + 16), (lx + 66, y + 16)]],
                  mix((246, 214, 150), (40, 40, 52), (y - pv0) / 500), None)
    if marks:
        for x in (-2.6, -1.2, -.3, 1.0, 1.9):
            person_mark(img, cam, x, 13.4)
        for x in (-1.5, 0, 1.5):
            person_mark(img, cam, x, 3.4)
    return img, None


def _window(img, X, Y, x0, x1, glass):
    """The lit window (de3): white shelves of guns behind one big sheet of glass; 'starred' cracks, 'gone' leaves
    jagged teeth in the frame."""
    a, b = (X(x0), Y(2.75)), (X(x1), Y(.6))
    img.paste(INSIDE, (int(a[0]), int(a[1]), int(b[0]), int(b[1])))
    for z in (2.2, 1.6, 1.0):
        quad(img, (X(x0 + .1), Y(z)), (X(x1 - .1), Y(z)), (X(x1 - .1), Y(z - .08)), (X(x0 + .1), Y(z - .08)), SHELF,
             (150, 146, 136), 1.5)
        for g in np.arange(x0 + .25, x1 - .4, .5):          # a long gun lying on each shelf, stock right
            gy = Y(z + .1)
            gx0, gx1 = X(g), X(g + .38)
            poly(img, [(gx0, gy), (gx1, gy - 4), (gx1 + 12, gy + 6), (gx1 - 4, gy + 6), (gx0, gy + 4)], GUN, INK, 1.2)
    for x in (x0 + 1.3, x0 + 2.7):                          # two uprights holding the shelves
        quad(img, (X(x), Y(2.7)), (X(x) + 8, Y(2.7)), (X(x) + 8, Y(.6)), (X(x), Y(.6)), (200, 196, 184), None, amt=0)
    if glass in ('whole', 'starred'):                       # reflections: two pale diagonal bands on the glass
        for u in (.12, .62):
            xa = a[0] + (b[0] - a[0]) * u
            shape(img, [[(xa, a[1]), (xa + 60, a[1]), (xa - 90, b[1]), (xa - 150, b[1])]], (232, 238, 244), None)
    if glass == 'starred':
        cx, cy = X(-.2), Y(1.5)
        for i, ang in enumerate(np.linspace(0, 6.28, 11, endpoint=False)):
            r = 120 + 70 * ((i * 5) % 3)
            poly(img, [(cx, cy), (cx + r * .5 * math.cos(ang + .2), cy + r * .5 * math.sin(ang + .2)),
                       (cx + r * math.cos(ang), cy + r * math.sin(ang))], None, (90, 100, 110), 2, 0)
        for r in (40, 80):
            poly(img, [(cx + r * math.cos(a_), cy + r * .9 * math.sin(a_)) for a_ in np.linspace(0, 6.28, 12)], None,
                 (90, 100, 110), 1.5, 0)
    if glass == 'gone':                                     # teeth left in the frame
        rng = np.random.default_rng(8)
        for (ya, yb, s) in ((a[1], a[1], 1), (b[1], b[1], -1)):
            pts = [(a[0], ya)]
            for x in np.linspace(a[0], b[0], 14)[1:-1]:
                pts.append((x, ya + s * rng.uniform(8, 50)))
            pts.append((b[0], ya))
            shape(img, [pts], (210, 226, 236), (90, 100, 110), 2)
    quad(img, (a[0] - 6, a[1] - 6), (b[0] + 6, a[1] - 6), (b[0] + 6, b[1] + 6), (a[0] - 6, b[1] + 6), None,
         (150, 150, 160), 5, 0)


def _shutter(img, X, Y, x0, x1, up):
    """The steel roller shutter: its box under the sign band, slats down to the hem; up = 1 hides nothing, 0.5 covers
    the top half of the window."""
    zt, zb = 3.5, 2.9
    quad(img, (X(x0 - .25), Y(zt)), (X(x1 + .25), Y(zt)), (X(x1 + .25), Y(zb)), (X(x0 - .25), Y(zb)), (104, 106, 116))
    hem = .45 + (2.9 - .45) * up
    if hem < 2.88:
        quad(img, (X(x0 - .05), Y(2.9)), (X(x1 + .05), Y(2.9)), (X(x1 + .05), Y(hem)), (X(x0 - .05), Y(hem)),
             (146, 148, 158))
        for z in np.arange(hem + .09, 2.9, .09):
            poly(img, [(X(x0 - .05), Y(z)), (X(x1 + .05), Y(z))], None, (108, 110, 120), 1.4, 0)
        quad(img, (X(x0 - .08), Y(hem + .07)), (X(x1 + .08), Y(hem + .07)), (X(x1 + .08), Y(hem)),
             (X(x0 - .08), Y(hem)), (70, 72, 80))
    for x in (x0 - .12, x1 + .04):                          # the guide rails
        quad(img, (X(x), Y(2.9)), (X(x + .08), Y(2.9)), (X(x + .08), Y(.45)), (X(x), Y(.45)), (88, 90, 100))


# ================================================================================================= T3
T3_SKY = [(150, 190, 230), (170, 204, 236), (190, 216, 240), (208, 226, 242)]
CREAM, CREAM_D, SLATE = (226, 214, 190), (196, 184, 162), (112, 120, 136)
STONE_P, STONE_S, BRONZE, BRONZE_L = (236, 232, 222), (204, 198, 186), (78, 74, 62), (112, 104, 84)
PAVE = (182, 176, 168)


def t3(t=0.0, marks=False):
    cam = CAMS['t3']
    img = Image.new('RGBA', (W, H), T3_SKY[0] + (255,))
    bands(img, 0, cam.VY, T3_SKY, seed=3, amp=14)
    for i, (x, y, r) in enumerate(((180, 300, 90), (300, 280, 70), (860, 380, 80), (960, 360, 60))):
        shape(img, [blob(x, y, r, 70 + i, squash=.5)], (244, 246, 250), (150, 170, 196), 2)
    # Haussmann fronts round the square (d 140): cream stone, iron balconies on the 2nd and 5th floors, grey
    # mansard roofs with dormers; the boulevard gaps left and right of the monument
    for (xa, xb, d) in ((-60, -14, 150), (14, 70, 150), (-14, 14, 230)):
        k = cam.ppm(d)
        (ax, ay), (bx, _) = cam.p(xa, d), cam.p(xb, d)
        top = cam.p(0, d, 18)[1]
        quad(img, (ax, ay), (bx, ay), (bx, top), (ax, top), CREAM if d < 200 else CREAM_D)
        roof = cam.p(0, d, 22.5)[1]
        quad(img, (ax + 4, top), (bx - 4, top), (bx - 1.5 * k, roof), (ax + 1.5 * k, roof), SLATE)
        for x in np.arange(xa + 1.5, xb - 1, 3.2):
            px = cam.p(x, d)[0]
            for fl in (1, 2, 3, 4, 5):
                z = 3.6 + (fl - 1) * 2.9
                quad(img, (px, cam.p(0, d, z + 2.0)[1]), (px + 1.2 * k, cam.p(0, d, z + 2.0)[1]),
                     (px + 1.2 * k, cam.p(0, d, z)[1]), (px, cam.p(0, d, z)[1]), (96, 102, 114), None, amt=0)
            quad(img, (px + .1 * k, cam.p(0, d, 20.5)[1]), (px + 1.1 * k, cam.p(0, d, 20.5)[1]),
                 (px + 1.1 * k, cam.p(0, d, 19)[1]), (px + .1 * k, cam.p(0, d, 19)[1]), CREAM, INK, 1.2, 0)
        for z in (6.4, 15.1):
            poly(img, [(ax, cam.p(0, d, z)[1]), (bx, cam.p(0, d, z)[1])], None, (60, 60, 70), 2, 0)
        quad(img, (ax, ay), (bx, ay), (bx, cam.p(0, d, 3.4)[1]), (ax, cam.p(0, d, 3.4)[1]), CREAM_D, INK, 1.5)
    # the black smoke beyond the monument (fires round the square), Marianne pale against it (F3, F5)
    smoke(img, [(300, 860, 110), (420, 760, 130), (560, 700, 150), (700, 760, 120), (820, 840, 100), (640, 600, 120),
                (480, 620, 100), (760, 640, 90)], (52, 48, 50), (86, 80, 82))
    # plane trees in the square (d 95-120), both sides of the monument
    for i, (x, d) in enumerate(((-34, 110), (-24, 100), (-16, 120), (19, 105), (28, 98), (38, 115))):
        bx, by = cam.p(x, d)
        tx, ty = cam.p(x, d, 7)
        k = cam.ppm(d)
        poly(img, [(bx - .3 * k, by), (bx + .3 * k, by), (tx + .2 * k, ty), (tx - .2 * k, ty)], (110, 96, 84), INK, 1.5, 0)
        r = 5.5 * k
        m = shape(img, [blob(tx, ty - r * .6, r, 80 + i, squash=.85)], (88, 120, 76), INK, 2)
        shape(img, [blob(tx - r * .3, ty - r * .9, r * .6, 90 + i)], (124, 156, 96), None, clip=m)
    _marianne(img, cam)
    # the paved square: joints running to the horizon
    img.paste(PAVE, (0, int(cam.VY), W, H))
    for x in np.arange(-60, 61, 4):
        poly(img, [cam.p(x, 6), cam.p(x, 300)], None, (160, 154, 146), 1.2, 0)
    for d in (8, 10, 13, 17, 22, 30, 42, 60):
        poly(img, [(0, cam.p(0, d)[1]), (W, cam.p(0, d)[1])], None, (160, 154, 146), 1.2, 0)
    _kiosk(img, cam, 9.5, 32, t)
    _bikes(img, cam, 6.6, 21, t)
    front = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    _car(front, cam, t)
    if marks:
        for x in np.arange(-4.6, -.5, 1.0):
            person_mark(img, cam, x, 11.8)
        for x in (5.4, 6.2, 7.0, 7.8):
            person_mark(img, cam, x, 11)
    return img, front


def _marianne(img, cam):
    """The monument (fr1, fr2, fr3): round stepped base, the plinth ringed with bronze reliefs, the tall pale drum with
    three seated stone figures and the bronze lion, and Marianne in bronze, olive branch raised, the tablet held."""
    d = 80
    k = cam.ppm(d)
    cx = cam.p(0, d)[0]
    Z = lambda z: cam.p(0, d, z)[1]                         # noqa: E731
    for (r, z0, z1, c) in ((11, 0, .5, STONE_S), (10.2, .5, 1.0, STONE_P), (9.4, 1.0, 1.5, STONE_S)):
        quad(img, (cx - r * k, Z(z0)), (cx + r * k, Z(z0)), (cx + r * k, Z(z1)), (cx - r * k, Z(z1)), c, INK, 2)
    quad(img, (cx - 7.6 * k, Z(1.5)), (cx + 7.6 * k, Z(1.5)), (cx + 7.4 * k, Z(4.2)), (cx - 7.4 * k, Z(4.2)), STONE_S)
    for x in np.arange(-6.8, 6.8, 2.27):                    # bronze relief panels round the base
        quad(img, (cx + x * k, Z(1.9)), (cx + (x + 1.9) * k, Z(1.9)), (cx + (x + 1.9) * k, Z(3.8)), (cx + x * k, Z(3.8)),
             BRONZE, INK, 1.5)
        shape(img, [blob(cx + (x + .95) * k, Z(2.85), .55 * k, int(x * 10) + 200, squash=1.2)], BRONZE_L, None)
    poly(img, [(cx - 5.5 * k, Z(2.4)), (cx - 4.6 * k, Z(3.2)), (cx - 3.4 * k, Z(2.2)), (cx - 2.3 * k, Z(3.0))], None,
         (200, 40, 60), 3, 0)                               # graffiti on the base (brief)
    poly(img, [(cx + 2.0 * k, Z(2.0)), (cx + 2.8 * k, Z(3.1)), (cx + 3.6 * k, Z(2.1))], None, (40, 40, 40), 3, 0)
    quad(img, (cx - 7.6 * k, Z(4.2)), (cx + 7.6 * k, Z(4.2)), (cx + 7.0 * k, Z(5.0)), (cx - 7.0 * k, Z(5.0)), STONE_P)
    # the drum (tapering) with its cornice
    quad(img, (cx - 3.6 * k, Z(5.0)), (cx + 3.6 * k, Z(5.0)), (cx + 3.0 * k, Z(14.6)), (cx - 3.0 * k, Z(14.6)), STONE_P)
    poly(img, [(cx + 2.2 * k, Z(5.2)), (cx + 1.8 * k, Z(14.4))], None, STONE_S, 6, 0)
    quad(img, (cx - 3.5 * k, Z(14.6)), (cx + 3.5 * k, Z(14.6)), (cx + 3.2 * k, Z(15.6)), (cx - 3.2 * k, Z(15.6)), STONE_S)
    # three seated stone figures round the drum, and the bronze lion in front
    for (x, z, s) in ((-4.6, 5.0, 1), (4.6, 5.0, -1), (0, 6.6, 1)):
        body = [(cx + (x - 1.4) * k, Z(z)), (cx + (x + 1.4) * k, Z(z)), (cx + (x + 1.1) * k, Z(z + 2.6)),
                (cx + (x + .3 * s) * k, Z(z + 4.6)), (cx + (x - .9) * k, Z(z + 3.4))]
        poly(img, body, STONE_P, INK, 2)
        IS.ell(img, cx + (x + .2 * s) * k, Z(z + 5.1), .55 * k, .6 * k, STONE_P, INK, 2)
        poly(img, [(cx + (x - .7) * k, Z(z + 2.4)), (cx + (x + .9) * k, Z(z + 2.0))], None, STONE_S, 2, 0)
    poly(img, [(cx - 1.6 * k, Z(5.0)), (cx + 1.8 * k, Z(5.0)), (cx + 1.7 * k, Z(6.2)), (cx + .6 * k, Z(6.6)),
               (cx - 1.0 * k, Z(6.4)), (cx - 1.7 * k, Z(5.8))], BRONZE, INK, 2)       # the lion lying by the urn
    IS.ell(img, cx - 1.35 * k, Z(6.5), .55 * k, .5 * k, BRONZE, INK, 2)
    # Marianne: robe, Phrygian cap, the right arm up holding the olive branch, the tablet against her left side
    body = [(cx - 1.4 * k, Z(15.6)), (cx + 1.4 * k, Z(15.6)), (cx + 1.0 * k, Z(19.5)), (cx + .9 * k, Z(22.5)),
            (cx + .5 * k, Z(23.4)), (cx - .5 * k, Z(23.4)), (cx - 1.0 * k, Z(21.5)), (cx - 1.1 * k, Z(18.5))]
    poly(img, body, BRONZE, INK, 2.4)
    poly(img, [(cx - .2 * k, Z(16)), (cx + .3 * k, Z(20)), (cx - .1 * k, Z(22.6))], None, BRONZE_L, 2, 0)
    IS.ell(img, cx, Z(24.1), .55 * k, .65 * k, BRONZE, INK, 2.4)
    poly(img, [(cx - .55 * k, Z(24.3)), (cx + .2 * k, Z(25.4)), (cx + .8 * k, Z(24.9)), (cx + .6 * k, Z(24.3))],
         BRONZE, INK, 2)                                     # the cap, its tip forward
    arm = [(cx + .5 * k, Z(23.0)), (cx + 1.3 * k, Z(25.5)), (cx + 1.6 * k, Z(27.2))]
    poly(img, arm, None, INK, 9.5, 0)
    poly(img, arm, None, BRONZE, 6, 0)
    for j in range(5):                                      # the olive branch above her fist
        a = -1.9 + j * .32
        poly(img, [(cx + 1.6 * k, Z(27.2)), (cx + 1.6 * k + 1.0 * k * math.cos(a), Z(27.2) + 1.0 * k * math.sin(a))],
             None, (70, 84, 56), 3, 0)
    quad(img, (cx - 1.5 * k, Z(18.4)), (cx - .7 * k, Z(18.6)), (cx - .6 * k, Z(20.6)), (cx - 1.4 * k, Z(20.4)),
         BRONZE_L, INK, 2)                                   # the tablet of the Rights of Man


def _kiosk(img, cam, x, d, t):
    """A Paris newspaper kiosk (dark green, round onion roof with a finial), burning."""
    k = cam.ppm(d)
    bx, by = cam.p(x, d)
    w = 2.0 * k
    G, GD = (44, 78, 62), (30, 56, 44)
    quad(img, (bx - w / 2, by), (bx + w / 2, by), (bx + w / 2, by - 2.4 * k), (bx - w / 2, by - 2.4 * k), G)
    quad(img, (bx - w * .38, by - .9 * k), (bx + w * .38, by - .9 * k), (bx + w * .38, by - 2.0 * k),
         (bx - w * .38, by - 2.0 * k), GD, INK, 1.5)
    roof = [(bx - w * .62, by - 2.4 * k), (bx + w * .62, by - 2.4 * k), (bx + w * .36, by - 3.0 * k),
            (bx + w * .1, by - 3.5 * k), (bx - w * .1, by - 3.5 * k), (bx - w * .36, by - 3.0 * k)]
    poly(img, roof, G, INK, 2)
    poly(img, [(bx, by - 3.5 * k), (bx, by - 3.9 * k)], None, INK, 2, 0)
    flames(img, bx + .2 * k, by - 2.6 * k, w * 1.1, 1.8 * k, t, seed=9)


def _bikes(img, cam, x, d, t):
    """A heap of rental bikes (green Lime, Velib), tumbled in the road between the lines, burning (fr4)."""
    k = cam.ppm(d)
    bx, by = cam.p(x, d)
    flames(img, bx, by - .3 * k, 3.6 * k, 2.6 * k, t, seed=7, n=6)
    rng = np.random.default_rng(12)
    for i in range(7):
        cx, cy = bx + (i - 3) * .45 * k + rng.uniform(-.1, .1) * k, by - (.25 + .35 * (i % 3)) * k
        a = math.radians(rng.uniform(-35, 35))
        ca, sa = math.cos(a), math.sin(a)
        colr = [(92, 196, 70), (120, 150, 170), (246, 130, 40)][i % 3]
        w1, w2 = (cx - .5 * k * ca, cy - .5 * k * sa), (cx + .5 * k * ca, cy + .5 * k * sa)
        for (wx, wy) in (w1, w2):
            IS.ell(img, wx, wy, .32 * k, .32 * k, None, (30, 30, 34), 3)
        top = (cx - .05 * k * sa, cy - .45 * k)
        poly(img, [w1, top, w2], None, INK, 6, 0)
        poly(img, [w1, top, w2], None, colr, 3.5, 0)
        poly(img, [top, (top[0] + .3 * k, top[1] - .25 * k)], None, INK, 3, 0)


def _car(img, cam, t):
    """The burnt-out estate car, foreground-left (d 6): its near rear quarter only, the rest out of frame; the
    frame of it is dark, the glass gone, fire through the windows and over the roof."""
    k = cam.ppm(6)
    gx, gy = cam.p(-1.0, 6)
    flames(img, gx - 1.2 * k, gy - 1.25 * k, 2.4 * k, 1.9 * k, t, seed=11, n=6)
    body = [(-20, gy - .3 * k), (gx, gy - .3 * k), (gx + .08 * k, gy - .95 * k), (gx - .25 * k, gy - 1.05 * k),
            (gx - .55 * k, gy - 1.45 * k), (-20, gy - 1.5 * k)]
    poly(img, body, (66, 60, 60), INK, 3)
    win = [(gx - .62 * k, gy - 1.08 * k), (gx - .4 * k, gy - 1.35 * k), (-20, gy - 1.38 * k), (-20, gy - 1.08 * k)]
    poly(img, win, (250, 150, 50), INK, 2)
    poly(img, [(gx - .1 * k, gy - .95 * k), (gx - .1 * k, gy - .7 * k)], None, (150, 40, 30), 6, 0)  # the tail light
    IS.ell(img, gx - .9 * k, gy - .3 * k, .34 * k, .34 * k, (36, 34, 36), INK, 2.4)
    IS.ell(img, gx - .9 * k, gy - .3 * k, .14 * k, .14 * k, (90, 86, 86), None, 0)
    flames(img, gx - .55 * k, gy - 1.05 * k, .9 * k, .7 * k, t + .3, seed=13, n=3)


# ================================================================================================= T4
T4_SKY = [(92, 22, 24), (138, 36, 28), (186, 64, 32), (222, 104, 40), (246, 156, 64)]
OCHRE, OCHRE_D, TRIM = (222, 172, 72), (186, 138, 58), (150, 146, 140)
PASTEL = [(200, 150, 140), (214, 186, 140), (170, 170, 150), (206, 160, 120), (180, 140, 150)]
PINE, PINE_L = (40, 46, 34), (62, 66, 42)


def t4(t=0.0, marks=False):
    cam = CAMS['t4']
    img = Image.new('RGBA', (W, H), T4_SKY[0] + (255,))
    bands(img, 0, cam.VY, T4_SKY, seed=4, amp=16)
    smoke(img, [(140, 300, 120), (300, 240, 110), (470, 290, 100), (620, 250, 110), (980, 320, 120), (860, 230, 90)],
          (78, 40, 38), (112, 58, 46))
    # the hills at the avenue's end, the far blocks and pines both sides
    shape(img, [[(0, cam.VY + 2), (120, cam.VY - 30), (300, cam.VY - 62), (420, cam.VY - 44), (520, cam.VY - 70),
                 (700, cam.VY - 38), (W, cam.VY - 20), (W, cam.VY + 2)]], (120, 70, 80), INK, 2)
    for s, x in ((-1, -9.0), (1, 12.0)):
        for i, d in enumerate(np.arange(420, 120, -32)):
            if s > 0 and d < 145:
                continue
            k = cam.ppm(d)
            a, b = cam.p(x, d), cam.p(x, d + 30)
            h = 18 + 9 * ((i * 3 + s) % 3)
            quad(img, a, b, cam.p(x, d + 30, h), cam.p(x, d, h), PASTEL[(i + (s > 0)) % 5], INK, 1.6)
            for fl in np.arange(3.5, h - 2, 3.0):
                poly(img, [cam.p(x, d + 2, fl), cam.p(x, d + 28, fl)], None, (100, 70, 70), 1.2, 0)
    for s, x in ((-1, -7.0), (1, 9.5)):                      # umbrella pines down both sides
        for d in np.arange(400, 70, -14):
            if s > 0 and d < 150:
                continue
            k = cam.ppm(d)
            bx, by = cam.p(x, d)
            tx, ty = cam.p(x, d, 9)
            poly(img, [(bx - .2 * k, by), (bx + .2 * k, by), (tx + .15 * k, ty), (tx - .15 * k, ty)], (60, 40, 36),
                 INK, 1.2, 0)
            m = shape(img, [blob(tx, ty - 1.2 * k, 4.2 * k, int(d) + s * 7, squash=.45)], PINE, INK, 1.8)
            shape(img, [blob(tx - 1 * k, ty - 1.9 * k, 2.4 * k, int(d) + 3, squash=.4)], PINE_L, None, clip=m)
    _ministry(img, cam, t)
    _bank(img, cam, t)
    # the avenue: dark tarmac in the firelight, a median line, the lane marks
    y0 = cam.VY + 1
    shape(img, [[(0, y0), (W, y0), (W, H), (0, H)]], (76, 50, 46), None)
    for xx in (-3.0, 3.0):
        for d in np.arange(9, 400, 9):
            quad(img, cam.p(xx - .1, d), cam.p(xx + .1, d), cam.p(xx + .1, d + 4), cam.p(xx - .1, d + 4), (150, 110, 80),
                 None, amt=0)
    if marks:
        for j in range(8):
            person_mark(img, cam, 1.2 + j * .55, 17.5)
        for x in (-4, -2.5, -1.0, .2):
            person_mark(img, cam, x, 18.5)
        person_mark(img, cam, -2.2, 6.5)
    return img, None


def _ministry(img, cam, t):
    """The Education Ministry (al1): a 3-storey ochre corner block with grey trim; the rounded corner bay toward us
    with stacked grey balconies; the flag on the roof over the corner; burning on the roof."""
    d, xc = 80, 7.0
    k = cam.ppm(d)
    Z = lambda z: cam.p(0, d, z)[1]                         # noqa: E731
    cx = cam.p(xc, d)[0]
    # the wing along the avenue, going away (x = 7, d 80 -> 125)
    a, b = cam.p(xc, 125), cam.p(xc, d)
    quad(img, a, b, cam.p(xc, d, 15), cam.p(xc, 125, 15), OCHRE_D)
    for z in (4.2, 8.0, 11.8):
        for dd in np.arange(88, 122, 6):
            p0, p1 = cam.p(xc, dd, z), cam.p(xc, dd + 2.2, z + 2.4)
            quad(img, p0, (p1[0], p0[1]), p1, (p0[0], p1[1]), (70, 52, 46), None, amt=0)
    # the frontal wing to the right (d 80, x 9.5 -> 30)
    x0, x1 = cam.p(xc + 2.4, d)[0], W + 20
    quad(img, (x0, Z(0)), (x1, Z(0)), (x1, Z(15)), (x0, Z(15)), OCHRE)
    quad(img, (x0, Z(14.2)), (x1, Z(14.2)), (x1, Z(15.4)), (x0, Z(15.4)), TRIM)
    quad(img, (x0, Z(0)), (x1, Z(0)), (x1, Z(3.2)), (x0, Z(3.2)), mix(OCHRE, TRIM, .5))
    for z in (4.2, 8.0, 11.8):
        poly(img, [(x0, Z(z - .4)), (x1, Z(z - .4))], None, TRIM, 2.5, 0)
        for x in np.arange(x0 + .9 * k, x1, 3.0 * k):
            quad(img, (x, Z(z + 2.6)), (x + 1.3 * k, Z(z + 2.6)), (x + 1.3 * k, Z(z)), (x, Z(z)), (66, 50, 48), TRIM, 2)
    # the rounded corner bay: a half drum toward us, its stacked grey balconies, the corner flag
    r = 2.6 * k
    sides = [(cx + r * math.cos(a), 0) for a in np.linspace(math.pi, 0, 13)]
    shape(img, [[(x, Z(0)) for x, _ in sides] + [(x, Z(16)) for x, _ in reversed(sides)]], mix(OCHRE, (255, 240, 200),
                                                                                             .12), INK, 2.4)
    for z in (4.0, 7.8, 11.6):
        quad(img, (cx - r * 1.08, Z(z)), (cx + r * 1.08, Z(z)), (cx + r * 1.0, Z(z - .5)), (cx - r * 1.0, Z(z - .5)),
             (170, 170, 172))
        for x in np.arange(cx - r, cx + r, .35 * k):
            poly(img, [(x, Z(z)), (x, Z(z + 1.0))], None, (120, 120, 124), 1.4, 0)
        poly(img, [(cx - r * 1.05, Z(z + 1.0)), (cx + r * 1.05, Z(z + 1.0))], None, (120, 120, 124), 2, 0)
        for x in (-1.3, 0.3):
            quad(img, (cx + x * k, Z(z + 2.8)), (cx + (x + 1.0) * k, Z(z + 2.8)), (cx + (x + 1.0) * k, Z(z + .2)),
                 (cx + x * k, Z(z + .2)), (66, 50, 48), None, amt=0)
    IS.ell(img, cx, Z(16), r * 1.12, .4 * k, TRIM, INK, 2)
    poly(img, [(cx, Z(16)), (cx, Z(21))], None, INK, 2.2, 0)
    fl = [(cx, Z(21)), (cx + 2.4 * k, Z(20.7)), (cx + 2.5 * k, Z(19.4)), (cx, Z(19.3))]
    poly(img, fl, (200, 30, 36), INK, 1.8)
    IS.ell(img, cx + 1.25 * k, Z(20.1), .35 * k, .35 * k, (20, 16, 16), None, 0)   # the eagle, small at this size
    # the roof alight (the brief's "blazing Education Ministry")
    flames(img, cam.p(xc + 9, d)[0], Z(15.2), 13 * k, 8 * k, t, seed=31, n=7)
    flames(img, cam.p(xc + .8, 110)[0], cam.p(0, 110, 15)[1], 6 * cam.ppm(110), 5 * cam.ppm(110), t + .4, seed=32)


def _bank(img, cam, t):
    """The bank on the left (x -9, d 38 -> 70), its face toward the avenue: pale stone, pilasters, the tall
    ground-floor windows the Molotovs hit (lit warm), upper windows dark."""
    x = -9.0
    da, db = 34, 74
    a, b = cam.p(x, da), cam.p(x, db)
    quad(img, a, b, cam.p(x, db, 16), cam.p(x, da, 16), (176, 150, 132))
    quad(img, a, b, cam.p(x, db, 5), cam.p(x, da, 5), (156, 128, 114))
    quad(img, cam.p(x, da, 15), cam.p(x, db, 15), cam.p(x, db, 16.4), cam.p(x, da, 16.4), (196, 172, 150))
    for d in np.arange(da + 2, db - 2, 5):
        quad(img, cam.p(x, d, .6), cam.p(x, d + 2.6, .6), cam.p(x, d + 2.6, 4.2), cam.p(x, d, 4.2), (90, 70, 66))
        for z in (6.5, 10.5):
            quad(img, cam.p(x, d + .4, z), cam.p(x, d + 2.2, z), cam.p(x, d + 2.2, z + 2.6), cam.p(x, d + .4, z + 2.6),
                 (60, 46, 46), None, amt=0)
        poly(img, [cam.p(x, d + 3.8, 0), cam.p(x, d + 3.8, 15)], None, (140, 116, 104), 3, 0)
    text(img, (cam.p(x, 40, 5.6)[0] + 40, cam.p(x, 40, 5.6)[1] - 4), 'BANKA', 26, (60, 46, 40))


# ------------------------------------------------------------------------------------------------- rule 83, rule 3
SET_BOXES = {
    't1': [('container', (452, 846, 572, 912)), ('domed corner', (770, 190, 860, 540))],
    't2': [('doorway', (0, 793, 140, 1173)), ('gun store window', (180, 760, 780, 1100)),
           ('shutter', (150, 650, 810, 760)), ('WAFFEN band', (130, 540, 830, 650)), ('closed shop', (821, 670, 1080, 1173)),
           ('street lamp', (0, 200, 260, 1240))],
    't3': [('monument', (210, 500, 750, 1155)), ('kiosk', (720, 1050, 830, 1200)), ('bikes', (580, 1100, 900, 1210)),
           ('car', (0, 920, 260, 1390))],
    't4': [('ministry', (540, 520, 1080, 1032)), ('bank', (0, 520, 300, 1120))],
}
SET_MEANT = {
    't2': [('street lamp', 'doorway', 'the lamp stands on the kerb 1.8 m in front of the doorway'),
           ('shutter', 'gun store window', 'the shutter is half down over the window (the brief)'),
           ('shutter', 'WAFFEN band', 'the shutter box sits right under the sign band'),
           ('street lamp', 'WAFFEN band', 'the lamp arm reaches toward the band, in front of it')],
    't3': [('kiosk', 'bikes', 'the bike heap burns in front of the kiosk: two fires the brief names together')],
}

BENCHMARK = {
    't1': ['dusk sky, the avenue wet after rain, streetlights on (brief 5)',
           'stone fronts 6-8 storeys with balconies and bays (es1)', 'the domed corner tower (es1)',
           'plane trees lining both sides (es1)', 'ornate double lamps (es1)', 'the avenue to the vanishing point (brief 6)',
           'a burning street container at the line (es4, brief 7)', 'Eixample cross streets every block'],
    't2': ['night, wet street with reflections (brief 12)', 'gun store centre (re-staged 13 Nov)',
           'one big glass window, guns on white shelves (de3)', 'dark mosaic-tiled base (de3)',
           'steel shutter half raised (brief 12)', 'WAFFEN sign band (decision 12 Nov)',
           'shopfronts either side, a street lamp (de4)', 'dark building above for the headline'],
    't3': ['Marianne in bronze, olive branch raised, tablet (fr1)', 'tall pale stone drum (fr1)',
           'three seated stone figures and the bronze lion (fr1)', 'bronze relief panels round the base (fr1)',
           'round stepped base (fr2)', 'Haussmann fronts with mansard roofs (fr2)', 'trees round the square (fr2)',
           'graffiti on the base (brief 19)', 'black smoke behind Marianne (fr3)', 'daytime (brief 20)'],
    't4': ['burning dusk sky (brief 24-25)', 'very wide avenue (al2)', 'tall pines both sides (al2)',
           'pastel blocks down to the hills (al2)', 'the ministry: 3-storey ochre corner block, grey trim (al1)',
           'rounded corner with stacked grey balconies (al1)', 'flag on the roof (al1)',
           'the bank on the left (brief 25)', 'the ministry ablaze (brief 25)'],
}
REFS_OF = {'t1': ['es1-passeig-de-gracia-march', 'es4-barcelona-11nov-mossos-burning-container'],
           't2': ['de3-frankfurt-gun-shop-window-smashed', 'de4-frankfurt-berliner-str-road-sign-smash'],
           't3': ['fr1-marianne-monument-close', 'fr2-place-de-la-republique-wide', 'fr3-republique-17oct-burning-car-marianne'],
           't4': ['al1-education-ministry-tirana', 'al2-tirana-boulevard']}


def checks():
    import setcheck
    out = []
    for tier, boxes in SET_BOXES.items():
        out += [f'{tier}: {f}' for f in setcheck.faults(boxes, SET_MEANT.get(tier, ()))]
    return out


# ------------------------------------------------------------------------------------------------- painting, sheet
PAINT = {'t1': t1, 't2': t2, 't3': t3, 't4': t4}
TITLES = {'t1': 'T1 Passeig de Gracia, dusk', 't2': 'T2 Frankfurt gun store, night',
          't3': 'T3 Place de la Republique, day', 't4': 'T4 Tirana avenue, dusk'}


def paint(tier, t=0.0, look=True, **kw):
    """The painting with its front layer laid on, through the house look (paper, light edges, soft shadows)."""
    B.SS = 1
    back, front = PAINT[tier](t, **kw)
    if front is not None:
        back.alpha_composite(front)
    if look:
        import house_look
        return house_look.apply(back)
    return back.convert('RGB')


def alone(outdir):
    os.makedirs(outdir, exist_ok=True)
    for tier in PAINT:
        paint(tier, 0.4).save(os.path.join(outdir, tier + '.png'))
    paint('t2', 0.4, shutter=1.0, glass='gone').save(os.path.join(outdir, 't2-broken.png'))
    return outdir


def sheet(out):
    """One row per place: the painting (phone size), the same with blue 1.75 m marks where the people go, the
    references, and the BENCHMARK list."""
    PW, PH = 405, 720
    rows = []
    fb = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 30)
    fr = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans.ttf'), 21)
    for tier in PAINT:
        row = Image.new('RGB', (2000, PH + 70), (244, 240, 232))
        d = ImageDraw.Draw(row)
        d.text((20, 14), TITLES[tier], font=fb, fill=(30, 30, 30))
        row.paste(paint(tier, .4).resize((PW, PH), Image.LANCZOS), (20, 60))
        extra = paint('t2', .4, shutter=1.0, glass='gone') if tier == 't2' else paint(tier, .4, marks=True)
        row.paste(extra.resize((PW, PH), Image.LANCZOS), (20 + PW + 16, 60))
        d.text((20 + PW + 16, PH + 62), 'shutter up, glass gone' if tier == 't2' else 'blue: 1.75 m people',
               font=fr, fill=(60, 60, 60))
        x = 20 + 2 * PW + 40
        for ref in REFS_OF[tier]:
            im = Image.open(os.path.join(REFS, ref + '.jpg')).convert('RGB')
            im.thumbnail((360, 340))
            if x + im.width > 2000 - 20:
                break
            row.paste(im, (x, 60))
            d.text((x, 60 + im.height + 4), ref.split('-')[0], font=fr, fill=(60, 60, 60))
            x += im.width + 12
        y = 450
        for item in BENCHMARK[tier]:
            d.text((20 + 2 * PW + 40, y), '- ' + item, font=fr, fill=(40, 40, 40))
            y += 30
        rows.append(row)
    if True:
        pass
    S = Image.new('RGB', (2000, sum(r.height for r in rows) + 80), (244, 240, 232))
    ImageDraw.Draw(S).text((20, 20), 'PROTEST TIERS: the four places (sets stage). Paintings at phone size; people '
                                     'and moving things come next.', font=fb, fill=(20, 20, 20))
    y = 80
    for r in rows:
        S.paste(r, (0, y))
        y += r.height
    S.save(out, quality=88)
    return out


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'sheet':
        print(sheet(sys.argv[2]))
    elif cmd == 'alone':
        print(alone(sys.argv[2]))
    elif cmd == 'check':
        print('\n'.join(checks()) or 'rule 83: clean')
