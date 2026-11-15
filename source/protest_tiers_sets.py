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
    python3 source/protest_tiers_sets.py vehicles OUT.jpg  the truck and helicopter sheet

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
    stays inside (a lit patch on smoke). Returns the mask. Draws in the shape's own box only (chat 10: speed)."""
    pts = [q for p in polys if len(p) > 2 for q in p]
    if not pts:
        return Image.new('L', (W, H), 0)
    pad = int(lw) + 4
    x0 = max(0, int(min(q[0] for q in pts)) - pad); y0 = max(0, int(min(q[1] for q in pts)) - pad)
    x1 = min(img.size[0], int(max(q[0] for q in pts)) + pad + 1); y1 = min(img.size[1], int(max(q[1] for q in pts)) + pad + 1)
    full = Image.new('L', (W, H), 0)
    if x1 <= x0 or y1 <= y0:
        return full
    m = _mask([[(x - x0, y - y0) for x, y in p] for p in polys], (x1 - x0, y1 - y0))
    if clip is not None:
        m = Image.fromarray(np.minimum(np.asarray(m), np.asarray(clip.crop((x0, y0, x1, y1)))))
    if line:
        k = 2 * int(round(lw / 2)) + 1
        img.paste(line, (x0, y0, x1, y1), mask=m.filter(ImageFilter.MaxFilter(k)))
    img.paste(fill, (x0, y0, x1, y1), mask=m)
    full.paste(m, (x0, y0))
    return full


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


def glow_disc(img, x, y, r, colour, steps=3, amt=0.22):
    """A flat light halo (lamps): a few stepped rings, lighter to the middle, no outline. Works on the disc's own box
    only (chat 10: repainting the whole frame per lamp made a painting take ~75 s)."""
    x0, y0, x1, y1 = int(max(0, x - r - 2)), int(max(0, y - r - 2)), int(min(W, x + r + 3)), int(min(H, y + r + 3))
    if x1 <= x0 or y1 <= y0:
        return
    box = img.crop((x0, y0, x1, y1))
    base = np.asarray(box.convert('RGB'), np.float32)
    for k in range(steps):
        rr = r * (1 - k / steps)
        m = np.asarray(_mask([[(x - x0 + rr * math.cos(a), y - y0 + rr * math.sin(a))
                               for a in np.linspace(0, 6.28, 28)]], (x1 - x0, y1 - y0)), np.float32)[..., None] / 255 * amt
        base = base * (1 - m) + np.array(colour, np.float32) * m
    img.paste(Image.fromarray(base.astype(np.uint8)).convert(img.mode), (x0, y0))


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


def smoke(img, lumps, tone, lit, line=INK, lw=3, fade=True):
    """Smoke as one lumpy shape (lumps = [(x, y, r)]): a shadowed side down and right, its lit side up and left, all kept inside the outline; with fade, it thins toward the top (chat 15, moves hunt 1: "flat cut-out
    blobs, no lit side, no thinning as they rise")."""
    if not lumps:
        return
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    m = shape(lay, [blob(x, y, r, 7 + i) for i, (x, y, r) in enumerate(lumps)], tone, line, lw)
    dark = tuple(int(c * .72) for c in tone)
    shape(lay, [blob(x + r * .24, y + r * .3, r * .62, 80 + i) for i, (x, y, r) in enumerate(lumps)], dark, None,
          clip=m)
    shape(lay, [blob(x - r * .25, y - r * .28, r * .55, 50 + i) for i, (x, y, r) in enumerate(lumps)], lit, None,
          clip=m)
    if fade:
        top = max(0, int(min(y - r for x, y, r in lumps)))
        bot = min(img.size[1], int(max(y + r for x, y, r in lumps)) + 1)
        if bot - top > 40:
            a = np.asarray(lay.getchannel('A'), np.float32)
            ramp = np.ones(img.size[1], np.float32)
            ramp[top:bot] = 0.5 + 0.5 * np.linspace(0, 1, bot - top) ** 0.7
            ramp[:top] = 0.5
            lay.putalpha(Image.fromarray((a * ramp[:, None]).astype(np.uint8)))
    img.alpha_composite(lay)


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


T1_CONTAINER = (0.8, 142.0)   # chat 15 (moves hunt 1: the container and knot did not read at phone size): was 165


def t1(t=0.0, marks=False):
    cam = CAMS['t1']
    img = Image.new('RGBA', (W, H), T1_SKY[0] + (255,))
    bands(img, 0, 240, T1_SKY, seed=1, amp=12)          # the dusk glow sits above the ridge, not behind it
    img.paste(T1_SKY[-1], (0, 230, W, int(cam.VY) + 30))
    # lit clouds low in the sky wedge
    for i, (x, y, r) in enumerate(((350, 250, 70), (470, 236, 60), (610, 262, 74), (560, 205, 40))):
        shape(img, [blob(x, y, r, 30 + i, squash=.45)], (226, 150, 140), (120, 80, 110), 2)
    # beyond the far end: the Collserola ridge (~7 km, 400-512 m) with Tibidabo's temple and the Collserola tower,
    # as seen up the Passeig (chat 10: fills the sky wedge the long lens leaves; the real view up the avenue)
    ridge = [(-10, cam.VY + 4)]
    for x in np.linspace(-10, W + 10, 40):
        hm = 300 + 170 * math.exp(-((x - 600) / 260) ** 2) + 18 * math.sin(x / 140) + 6 * math.sin(x / 41 + 1)
        ridge.append((x, cam.VY - cam.F * hm / 11000))
    shape(img, [ridge + [(W + 10, cam.VY + 4)]], (98, 76, 118), (62, 48, 84), 2)
    ridge2 = [(-10, cam.VY + 4)] + [(x, cam.VY - cam.F * (120 + 35 * math.sin(x / 150 + 2) + 10 * math.sin(x / 53)) /
                                     6000) for x in np.linspace(-10, W + 10, 40)] + [(W + 10, cam.VY + 4)]
    shape(img, [ridge2], (78, 68, 108), (56, 46, 80), 2)
    tx, ty = 600, cam.VY - cam.F * 462 / 11000
    k = cam.F / 11000                                      # px per m at the ridge
    shape(img, [[(tx - 22 * k, ty + 4), (tx - 22 * k, ty - 30 * k), (tx - 9 * k, ty - 30 * k), (tx - 9 * k, ty - 52 * k),
                 (tx + 9 * k, ty - 52 * k), (tx + 9 * k, ty - 30 * k), (tx + 22 * k, ty - 30 * k), (tx + 22 * k, ty + 4)],
                [(tx - 3 * k, ty - 52 * k), (tx + 3 * k, ty - 52 * k), (tx, ty - 72 * k)]], (70, 60, 96), (50, 42, 74), 1.6)
    cx2, cy2 = 455, cam.VY - cam.F * 400 / 10500
    k2 = cam.F / 10500
    shape(img, [[(cx2 - 2 * k2, cy2 + 4), (cx2 + 2 * k2, cy2 + 4), (cx2 + 1.2 * k2, cy2 - 288 * k2),
                 (cx2 - 1.2 * k2, cy2 - 288 * k2)],
                [(cx2 - 13 * k2, cy2 - 150 * k2), (cx2 + 13 * k2, cy2 - 150 * k2), (cx2 + 9 * k2, cy2 - 175 * k2),
                 (cx2 - 9 * k2, cy2 - 175 * k2)]], (70, 60, 96), (50, 42, 74), 1.4)
    glow_disc(img, cx2, cy2 - 290 * k2, 5, (255, 90, 80), steps=2, amt=.6)
    # far end (Diagonal, ~1.3 km): a line of fronts across the horizon
    shape(img, [[(0, cam.VY + 4)] + [(x, cam.VY - 48 - 14 * math.sin(x / 37) - 10 * (x % 90 < 30))
                                     for x in range(0, W + 30, 30)] + [(W, cam.VY + 4)]], (110, 90, 118), INK, 2)
    rng0 = np.random.default_rng(5)
    for x in range(8, W, 22):
        if rng0.random() < .4:
            y = cam.VY - rng0.uniform(12, 40)
            img.paste(WIN_L, (x, int(y), x + 5, int(y) + 5))
    # the avenue: wet road (it holds the dusk sky), pavements under the trees
    far = 1600
    img.paste(mix(ROAD_W, (70, 60, 90), .4), (0, int(cam.VY) - 2, W, int(cam.p(0, far)[1]) + 2))   # the far avenue
    quad(img, cam.p(-30.5, 40), cam.p(30.5, 40), cam.p(30.5, far), cam.p(-30.5, far), ROAD_W, None, amt=0)
    for s in (-1, 1):
        quad(img, cam.p(s * 30.5, 40), cam.p(s * 18, 40), cam.p(s * 18, far), cam.p(s * 30.5, far), (104, 96, 112),
             None, amt=0)
    # the dusk sky in the wet road (long soft streaks) and the lane lines
    for xx in (-12.5, -6.5, 6.5, 12.5):                   # dashed lane lines, 0.15 m wide, 4.5 m dashes, 7.5 m gaps
        for d in np.arange(42, 1200, 12):
            quad(img, cam.p(xx - .08, d), cam.p(xx + .08, d), cam.p(xx + .08, d + 4.5), cam.p(xx - .08, d + 4.5),
                 ROAD_L, None, amt=0)
    for xx in (-.25, .25):                                # the solid double centre line
        quad(img, cam.p(xx - .07, 42), cam.p(xx + .07, 42), cam.p(xx + .07, far), cam.p(xx - .07, far),
             mix(ROAD_W, ROAD_L, .6), None, amt=0)
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
                tr = np.random.default_rng(int(d) * 7 + xx + 3 * s)
                th, r = tr.uniform(7.5, 10.5), tr.uniform(3.2, 5.0)
                tx, ty = cam.p(s * xx + tr.uniform(-.6, .6), d, th)
                poly(img, [(bx - .25 * k, by), (bx + .25 * k, by), (tx + .2 * k, ty), (tx - .2 * k, ty)], (96, 86, 78),
                     INK, 1.4, 0)
                r = r * k
                td = mix(TREE_D, (30, 44, 40), tr.uniform(0, .5))
                tl = mix(TREE_L, (150, 140, 90), tr.uniform(0, .35))   # some caught by the lamps, some by the dusk
                m = shape(img, [blob(tx, ty - r * .5, r, int(d) + xx + s, squash=tr.uniform(.65, .9))], td, INK, 2)
                shape(img, [blob(tx - r * .3, ty - r * .85, r * .6, int(d) + 3)], tl, None, clip=m)
        if d % 27 < 9:
            for s in (-1, 1):
                k = cam.ppm(d)
                bx, by = cam.p(s * 16.5, d)
                if -60 < bx < W + 60:
                    _falques(img, bx, by, k)
    # chat 11 (hunt 1: "no wet-after-rain reflections"): each lamp and the container fire laid in the wet road as a
    # soft broken streak running toward us, about as long as the lamp is tall
    wet = Image.new('RGBA', img.size, (0, 0, 0, 0))

    def streak(x, y0, L, w, col, seed):                   # one tapering sliver broken into 2-3 lengths
        r = np.random.default_rng(seed)
        y = y0
        while y < y0 + L:
            l = L * r.uniform(.25, .45)
            u = (y - y0) / L
            ww = w * (1 - .6 * u)
            shape(wet, [[(x - ww, y), (x + ww, y), (x + ww * .5, y + l), (x - ww * .5, y + l)]], col, None)
            y += l + L * r.uniform(.06, .14)
    for d in np.arange(1300, 250, -9):
        if d % 27 < 9:
            k = cam.ppm(d)
            for s in (-1, 1):
                bx, by = cam.p(s * 15.6, d)
                if -20 < bx < W + 20:
                    streak(bx, by + 2, 6 * k, max(1.2, .3 * k), (255, 214, 140, 110), int(d) * 3 + s)
    cx_, cd_ = T1_CONTAINER
    fx, fy = cam.p(cx_, cd_)
    streak(fx, fy + 6, 5 * cam.ppm(cd_), .45 * cam.ppm(cd_), (250, 150, 60, 80), 7)
    img.alpha_composite(wet)
    # the burning street container just short of the line, with its fire (chat 15: nearer, d 142, so it reads)
    _container(img, cam, cx_, cd_, t)
    if marks:
        for x in np.arange(-11, 15, 2.8):
            person_mark(img, cam, x, 150)
        for x in (-3, -1.6, 2.4, 3.6):
            person_mark(img, cam, x, 124)
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
    glow_disc(img, lx + 70, lh + 8, 90, (255, 220, 150), amt=.12)
    shape(img, [[(lx + 48, lh - 6), (lx + 92, lh - 14), (lx + 86, lh + 6), (lx + 54, lh + 8)]], (255, 232, 170), INK, 2)
    # far pavement (wet), kerb, road; the window and lamp mirrored in the wet as broken streaks
    pv0, pv1 = cam.p(0, 14)[1], cam.p(0, 12)[1]
    img.paste((70, 70, 84), (0, int(pv0), W, int(pv1)))
    quad(img, (0, pv1), (W, pv1), (W, pv1 + 10), (0, pv1 + 10), (110, 110, 124), INK, 2)
    img.paste((40, 40, 52), (0, int(pv1 + 10), W, H))
    rng = np.random.default_rng(5)
    # chat 10: long broken streaks (dots read as rain on the lens): each a tall wobbly sliver, fading downward
    def streak(xc, w, y0, y1, col, seed):
        r = np.random.default_rng(seed)
        y = y0
        while y < y1:
            L = r.uniform(60, 180)
            ww = w * r.uniform(.5, 1)
            jit = r.uniform(-4, 4)
            shape(img, [[(xc - ww + jit, y), (xc + ww + jit, y), (xc + ww * .85 + jit, y + L), (xc - ww * .85 + jit, y + L)]],
                  mix(col, (40, 40, 52), min(1, .45 + (y - y0) / (y1 - y0) * .8)), None)
            y += L + r.uniform(8, 30)
    for i, xx in enumerate(np.arange(X(x0) + 30, X(x1) - 20, 48)):
        streak(xx + rng.uniform(-8, 8), rng.uniform(4, 9), pv1 + 14 + rng.uniform(0, 40), 1500, (226, 218, 192), 40 + i)
    streak(lx + 70, 12, pv1 + 14, 1500, (246, 214, 150), 7)
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
    # chat 10: the guns read as guns at phone size (were thin flat dashes): rifles hung on a pegboard above,
    # pistols in white cubbies below (de3)
    k = X(1) - X(0)                                         # px per m on the shop front
    for z in np.arange(1.5, 2.75, .12):                     # the pegboard's holes
        for x in np.arange(x0 + .08, x1 - .05, .12):
            img.paste((214, 212, 204), (int(X(x)), int(Y(z)), int(X(x)) + 3, int(Y(z)) + 3))
    for row, z in enumerate((2.45, 1.95)):
        for i, g in enumerate(np.arange(x0 + .15, x1 - 1.0, 1.25)):
            _rifle(img, X(g + .06 * row), Y(z), k, scope=(i + row) % 2 == 0, kind=(i + 2 * row) % 3)
    quad(img, (X(x0 + .05), Y(1.45)), (X(x1 - .05), Y(1.45)), (X(x1 - .05), Y(1.38)), (X(x0 + .05), Y(1.38)), SHELF,
         (150, 146, 136), 1.5)
    for z in (1.35, .98):                                   # two rows of cubbies, a pistol in most
        for i, x in enumerate(np.arange(x0 + .1, x1 - .3, .42)):
            quad(img, (X(x), Y(z)), (X(x + .38), Y(z)), (X(x + .38), Y(z - .33)), (X(x), Y(z - .33)), (250, 250, 246),
                 (170, 166, 156), 1.5, 0)
            if (i * 3 + int(z * 10)) % 5:
                _pistol(img, X(x + .07), Y(z - .1), k, flip=(i % 2 == 0))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))         # chat 11: glare and cracks kept inside the glass
    if glass in ('whole', 'starred'):                       # reflections: two pale diagonal bands on the glass
        for u in (.22, .7):
            xa = a[0] + (b[0] - a[0]) * u
            shape(lay, [[(xa, a[1]), (xa + 60, a[1]), (xa - 90, b[1]), (xa - 150, b[1])]], (232, 238, 244, 255), None)
    img_, img = img, lay
    if glass == 'starred':
        cx, cy = X(-.2), Y(1.5)
        for i, ang in enumerate(np.linspace(0, 6.28, 11, endpoint=False)):
            r = 120 + 70 * ((i * 5) % 3)
            poly(img, [(cx, cy), (cx + r * .5 * math.cos(ang + .2), cy + r * .5 * math.sin(ang + .2)),
                       (cx + r * math.cos(ang), cy + r * math.sin(ang))], None, (90, 100, 110), 2, 0)
        for r in (40, 80):
            poly(img, [(cx + r * math.cos(a_), cy + r * .9 * math.sin(a_)) for a_ in np.linspace(0, 6.28, 12)], None,
                 (90, 100, 110), 1.5, 0)
    img = img_
    box = (int(a[0]), int(a[1]), int(b[0]), int(b[1]))
    img.alpha_composite(lay.crop(box), dest=box[:2])
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


def _rifle(img, x, y, k, scope=False, kind=0):
    """A long gun side on, 1.0-1.1 m, muzzle left: barrel, receiver, magazine, grip, stock (a filled silhouette)."""
    L = (1.05, .95, 1.1)[kind] * k
    u = lambda a, b: (x + a * L, y + b * k)                 # noqa: E731  a along the gun 0..1, b metres down
    body = [u(0, -.01), u(.42, -.015), u(.45, -.035), u(.72, -.035), u(.74, -.02), u(1, -.03), u(1, .11),
            u(.93, .12), u(.78, .03), u(.72, .035), u(.70, .1), u(.665, .1), u(.67, .035), u(.6, .035),
            u(.57, .13 if kind == 1 else .02), u(.53, .13 if kind == 1 else .02), u(.53, .03), u(.42, .025), u(0, .015)]
    shape(img, [body], GUN, INK, 2)
    if kind == 2:                                           # a wooden stock and fore-end on the hunting rifle
        shape(img, [[u(.74, -.02), u(1, -.03), u(1, .11), u(.93, .12), u(.78, .03)]], (122, 78, 46), INK, 1.5)
    if scope:
        shape(img, [[u(.47, -.045), u(.7, -.045), u(.7, -.085), u(.47, -.085)]], (40, 42, 48), INK, 1.5)
        shape(img, [[u(.44, -.04), u(.48, -.04), u(.48, -.095), u(.44, -.095)]], (40, 42, 48), INK, 1.5)


def _pistol(img, x, y, k, flip=False):
    """A pistol side on (~0.2 m): slide, grip, trigger guard."""
    f = -1 if flip else 1
    ox = x + (.24 * k if flip else 0)
    u = lambda a, b: (ox + f * a * k, y + b * k)            # noqa: E731
    shape(img, [[u(0, -.04), u(.2, -.04), u(.2, .0), u(.17, .0), u(.165, .12), u(.12, .12), u(.115, .03),
                 u(.09, .03), u(.08, .05), u(.06, .05), u(.06, .0), u(0, .0)]], GUN, INK, 1.6)


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


def t3(t=0.0, marks=False, truck=None):
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
    # chat 11 (hunt 2: "Marianne a dark figure in a rock blob"): the smoke rises right of her, her bronze against sky
    smoke(img, [(640, 880, 100), (720, 780, 120), (850, 700, 150), (980, 770, 120), (1060, 860, 100), (900, 580, 120),
                (700, 660, 80), (1020, 620, 100)], (52, 48, 50), (86, 80, 82))
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
    _kiosk(img, cam, 7.0, 30, t)                            # chat 10: mid-right, behind the bikes (was off frame)
    if truck:                                               # chat 12: the water cannon, behind the police (d 11), the bikes
        globals()['truck'](img, cam, truck['x'], TRUCK_D3, t, 'drive', 'fr', truck.get('aim', 18), truck.get('flash', 0))
    _bikes(img, cam, 2.1, 14, t)                            # in the gap between the front line and the police
    front = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    _car(front, cam, t)
    if marks:
        for x in np.arange(-1.7, 1.05, .55):                # the front line, x 200-640 px
            person_mark(img, cam, x, 11.8)
        for x in (2.5, 3.0, 3.5):                           # the police, x 900-1080 px
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
    # chat 10: the drum slimmer and taller (fr1/fr2: about a third as wide as it is tall), its shadow side shaded
    quad(img, (cx - 2.7 * k, Z(5.0)), (cx + 2.7 * k, Z(5.0)), (cx + 2.2 * k, Z(15.4)), (cx - 2.2 * k, Z(15.4)), STONE_P)
    quad(img, (cx + 1.3 * k, Z(5.0)), (cx + 2.7 * k, Z(5.0)), (cx + 2.2 * k, Z(15.4)), (cx + 1.0 * k, Z(15.4)), STONE_S,
         None, amt=0)
    for z in (7.5, 12.8):                                   # carved bands round the drum
        quad(img, (cx - 2.6 * k, Z(z)), (cx + 2.6 * k, Z(z)), (cx + 2.6 * k, Z(z + .35)), (cx - 2.6 * k, Z(z + .35)),
             STONE_S, INK, 1.2, 0)
    quad(img, (cx - 2.8 * k, Z(15.4)), (cx + 2.8 * k, Z(15.4)), (cx + 2.5 * k, Z(16.2)), (cx - 2.5 * k, Z(16.2)), STONE_S)
    # three seated stone figures round the drum, and the bronze lion in front
    FIG, FIG_S, FIG_D = (224, 216, 200), (184, 174, 158), (150, 140, 126)   # chat 10: shaded, not white ghosts
    for (x, z, s) in ((-3.6, 5.0, 1), (3.6, 5.0, -1), (0, 7.8, 1)):
        X_ = lambda u: cx + (x + u * s) * k                 # noqa: E731  u mirrored so each figure faces out
        lap = [(X_(-1.5), Z(z)), (X_(1.5), Z(z)), (X_(1.4), Z(z + 1.6)), (X_(.2), Z(z + 2.0)), (X_(-1.2), Z(z + 1.8))]
        torso = [(X_(-1.1), Z(z + 1.6)), (X_(.5), Z(z + 1.8)), (X_(.4), Z(z + 3.6)), (X_(-.2), Z(z + 3.9)),
                 (X_(-1.0), Z(z + 3.5))]
        m = shape(img, [lap, torso], FIG, INK, 2)
        shape(img, [[(X_(.1), Z(z)), (X_(1.6), Z(z)), (X_(1.6), Z(z + 4)), (X_(.0), Z(z + 4))]], FIG_S, None, clip=m)
        for u in (-.7, .3, 1.0):                            # drapery folds falling over the knees
            poly(img, [(X_(u), Z(z + 1.7)), (X_(u + .15), Z(z + .9)), (X_(u - .05), Z(z + .1))], None, FIG_D, 2, 0)
        poly(img, [(X_(-.9), Z(z + 3.3)), (X_(.9), Z(z + 2.0)), (X_(1.3), Z(z + 1.4))], None, INK, 6, 0)   # the arm
        poly(img, [(X_(-.9), Z(z + 3.3)), (X_(.9), Z(z + 2.0)), (X_(1.3), Z(z + 1.4))], None, FIG_S, 3.5, 0)
        hx, hy = X_(-.4), Z(z + 4.45)
        IS.ell(img, hx, hy, .5 * k, .58 * k, FIG, INK, 2)
        shape(img, [[(hx - .52 * k, hy), (hx - .45 * k, hy - .5 * k), (hx + .1 * k, hy - .68 * k),
                     (hx + .5 * k, hy - .35 * k), (hx + .3 * k, hy - .15 * k), (hx - .3 * k, hy + .4 * k)]], FIG_D, INK, 1.5)
    poly(img, [(cx - 1.6 * k, Z(5.0)), (cx + 1.8 * k, Z(5.0)), (cx + 1.7 * k, Z(6.2)), (cx + .6 * k, Z(6.6)),
               (cx - 1.0 * k, Z(6.4)), (cx - 1.7 * k, Z(5.8))], BRONZE, INK, 2)       # the lion lying by the urn
    IS.ell(img, cx - 1.35 * k, Z(6.5), .55 * k, .5 * k, BRONZE, INK, 2)
    # Marianne: robe, Phrygian cap, the right arm up holding the olive branch, the tablet against her left side
    # chat 10: a full figure, 9.5 m (fr1): wide robe flaring at the feet, shoulders, head ~1.2 m
    body = [(cx - 2.0 * k, Z(16.2)), (cx + 2.0 * k, Z(16.2)), (cx + 1.5 * k, Z(18.5)), (cx + 1.25 * k, Z(21.5)),
            (cx + 1.4 * k, Z(22.9)), (cx + .6 * k, Z(23.6)), (cx - .6 * k, Z(23.6)), (cx - 1.4 * k, Z(22.8)),
            (cx - 1.5 * k, Z(20.5)), (cx - 1.7 * k, Z(18.0))]
    poly(img, body, BRONZE, INK, 2.4)
    for (xa, xb) in ((-.9, -.4), (.1, .3), (.8, .5)):      # robe folds
        poly(img, [(cx + xa * k, Z(16.4)), (cx + (xa + xb) / 2 * k, Z(19.5)), (cx + xb * k, Z(22.6))], None, BRONZE_L,
             2.4, 0)
    poly(img, [(cx - 1.3 * k, Z(21.2)), (cx + 1.2 * k, Z(21.6))], None, BRONZE_L, 3, 0)    # the belt
    IS.ell(img, cx, Z(24.3), .62 * k, .72 * k, BRONZE, INK, 2.4)
    poly(img, [(cx - .66 * k, Z(24.4)), (cx - .1 * k, Z(25.6)), (cx + .9 * k, Z(25.3)), (cx + .7 * k, Z(24.5))],
         BRONZE, INK, 2)                                     # the cap, its tip forward
    arm = [(cx + .9 * k, Z(23.0)), (cx + 1.5 * k, Z(25.4)), (cx + 1.7 * k, Z(27.6))]
    poly(img, arm, None, INK, 12, 0)
    poly(img, arm, None, BRONZE, 8, 0)
    IS.ell(img, cx + 1.7 * k, Z(27.6), .3 * k, .3 * k, BRONZE, INK, 2)    # the fist
    for j in range(6):                                      # the olive branch above her fist
        a = -2.0 + j * .3
        ex, ey = cx + 1.7 * k + 1.3 * k * math.cos(a), Z(27.6) + 1.3 * k * math.sin(a)
        poly(img, [(cx + 1.7 * k, Z(27.6)), (ex, ey)], None, (70, 84, 56), 3, 0)
        IS.ell(img, ex, ey, .18 * k, .1 * k, (96, 116, 70), INK, 1)
    quad(img, (cx - 1.9 * k, Z(18.2)), (cx - .8 * k, Z(18.4)), (cx - .7 * k, Z(21.0)), (cx - 1.8 * k, Z(20.8)),
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
    # chat 11 (hunt 2: "kiosk missing"): its cream poster panels and red PRESSE band make it read as a kiosk
    for sx in (-1, 1):
        quad(img, (bx + sx * w * .42, by - .5 * k), (bx + sx * w * .08, by - .5 * k), (bx + sx * w * .08, by - 1.7 * k),
             (bx + sx * w * .42, by - 1.7 * k), (236, 226, 196), INK, 1.5)
    quad(img, (bx - w / 2, by - 2.0 * k), (bx + w / 2, by - 2.0 * k), (bx + w / 2, by - 2.4 * k), (bx - w / 2, by - 2.4 * k),
         (180, 40, 36), INK, 1.5)
    text(img, (bx, by - 2.2 * k), 'PRESSE', int(.32 * k), (250, 240, 220))
    flames(img, bx + .35 * k, by - 3.0 * k, w * .8, 1.5 * k, t, seed=9)


def _bikes(img, cam, x, d, t):
    """A heap of rental bikes (green Lime, Velib), tumbled in the road between the lines, burning (fr4)."""
    k = cam.ppm(d)
    bx, by = cam.p(x, d)
    flames(img, bx, by - .2 * k, 2.2 * k, 1.4 * k, t, seed=7, n=7)
    rng = np.random.default_rng(12)
    for i in range(7):
        cx, cy = bx + (i - 3) * .3 * k + rng.uniform(-.1, .1) * k, by - (.3 + .3 * (i % 3)) * k
        a = math.radians(rng.uniform(-35, 35))
        ca, sa = math.cos(a), math.sin(a)
        colr = [(92, 196, 70), (120, 150, 170), (246, 130, 40)][i % 3]
        w1, w2 = (cx - .5 * k * ca, cy - .5 * k * sa), (cx + .5 * k * ca, cy + .5 * k * sa)
        for (wx, wy) in (w1, w2):
            IS.ell(img, wx, wy, .32 * k, .32 * k, None, (30, 30, 34), 5)
        top = (cx - .05 * k * sa, cy - .45 * k)
        poly(img, [w1, top, w2, w1], None, INK, 10, 0)
        poly(img, [w1, top, w2, w1], None, colr, 6, 0)
        poly(img, [top, (top[0] + .3 * k, top[1] - .25 * k)], None, INK, 5, 0)
        IS.ell(img, w1[0], w1[1] - .4 * k, .14 * k, .07 * k, (40, 40, 44), INK, 1.5)    # the saddle


def _car(img, cam, t):
    """The burnt-out estate car, foreground-left (fr3): drawn in the camera (chat 10; the draft was a flat block):
    rear face at d 6 (its right corner at x ~100 px, the rest off frame), the right side running away to d 10.7;
    charred paint, the glass gone, fire inside showing through the window holes and ~1.2 m over the roof."""
    X0, X1, D0, D1 = -3.15, -1.35, 6.0, 10.2          # chat 11: 0.15 m left, 0.5 m shorter, fire 1.5 m wide: clear of the monument
    P = lambda x, d, z: cam.p(x, d, z)                      # noqa: E731
    CH, CH_D, RUST = (74, 66, 64), (54, 48, 48), (128, 76, 52)
    # the fire first, its foot hidden inside the body: it climbs from behind the roofline (we look up at the car)
    k = cam.ppm(D0 + 1.5)
    gx, gy = P(X1 - .4, D0 + 1.8, 1.25)
    flames(img, gx, gy, 1.3 * k, 1.2 * k, t, seed=11, n=7)
    gx2, gy2 = P(X1 - .5, D0 + .2, 1.3)
    flames(img, gx2, gy2, .9 * cam.ppm(D0), .7 * cam.ppm(D0), t + .3, seed=13, n=4)
    side = [P(X1, D0, .3), P(X1, D1, .3), P(X1, D1, .85), P(X1, D1 - .7, .95), P(X1, D1 - 1.5, 1.45), P(X1, D0 + .3, 1.48), P(X1, D0, .98)]
    shape(img, [side], CH, INK, 3)
    shape(img, [[P(X1, D0 + 1.2, .5), P(X1, D0 + 2.6, .45), P(X1, D0 + 2.4, .85), P(X1, D0 + 1.4, .9)]], RUST, None)
    # chat 11 (hunt 1: "an orange van"): the rear is a car's, a body to the belt line and a cabin narrowing to the
    # roof; the window holes are charred black, the fire glowing only in their lower part
    rear = [P(X0, D0, .3), P(X1, D0, .3), P(X1, D0, .95), P(X1 - .14, D0, 1.48), P(X0 + .14, D0, 1.48), P(X0, D0, .95)]
    shape(img, [rear], CH_D, INK, 3)
    holes = [[P(X1, D0 + .25, 1.0), P(X1, D1 - 1.6, 1.0), P(X1, D1 - 1.6, 1.4), P(X1, D0 + .25, 1.4)],
             [P(X0 + .22, D0, 1.0), P(X1 - .22, D0, 1.0), P(X1 - .26, D0, 1.4), P(X0 + .26, D0, 1.4)]]
    m = shape(img, holes, (34, 28, 28), INK, 2.4)
    glow = [[P(X1, D0 + .25, 1.0), P(X1, D1 - 1.6, 1.0), P(X1, D1 - 1.9, 1.16), P(X1, D0 + 1.2, 1.2), P(X1, D0 + .25, 1.12)],
            [P(X0 + .22, D0, 1.0), P(X1 - .22, D0, 1.0), P(X1 - .4, D0, 1.15), P(X0 + .5, D0, 1.2)]]
    shape(img, glow, (250, 150, 50), None, clip=m)
    for xx in (D0 + 1.8, D0 + 3.0):                         # door pillars across the side hole
        shape(img, [[P(X1, xx - .06, 1.0), P(X1, xx + .06, 1.0), P(X1, xx + .06, 1.42), P(X1, xx - .06, 1.42)]], CH, INK, 2)
    shape(img, [[P(X1 - .12, D0, .85), P(X1 - .02, D0, .85), P(X1 - .02, D0, 1.12), P(X1 - .12, D0, 1.12)]],
          (150, 40, 30), INK, 1.5)                          # the tail light
    for dc in (D0 + .75, D1 - .95):                         # wheels: circles in the side's own plane
        tyre = [P(X1 + .02, dc + .34 * math.cos(a_), .34 + .34 * math.sin(a_)) for a_ in np.linspace(0, 6.28, 24)]
        hub = [P(X1 + .03, dc + .14 * math.cos(a_), .34 + .14 * math.sin(a_)) for a_ in np.linspace(0, 6.28, 16)]
        shape(img, [tyre], (36, 34, 36), INK, 2.4)
        shape(img, [hub], (110, 104, 100), None)


# ================================================================================================= T4
T4_SKY = [(92, 22, 24), (138, 36, 28), (186, 64, 32), (222, 104, 40), (246, 156, 64)]
OCHRE, OCHRE_D, TRIM = (222, 172, 72), (186, 138, 58), (150, 146, 140)
PASTEL = [(200, 150, 140), (214, 186, 140), (170, 170, 150), (206, 160, 120), (180, 140, 150)]
PINE, PINE_L = (40, 46, 34), (62, 66, 42)


def t4(t=0.0, marks=False, heli=None):
    cam = CAMS['t4']
    img = Image.new('RGBA', (W, H), T4_SKY[0] + (255,))
    bands(img, 0, cam.VY, T4_SKY, seed=4, amp=16)
    smoke(img, [(140, 300, 120), (300, 240, 110), (470, 290, 100), (620, 250, 110), (980, 320, 120), (860, 230, 90)],
          (78, 40, 38), (112, 58, 46))
    # the hills at the avenue's end, the far blocks and pines both sides
    shape(img, [[(0, cam.VY + 2), (120, cam.VY - 30), (300, cam.VY - 62), (420, cam.VY - 44), (520, cam.VY - 70),
                 (700, cam.VY - 38), (W, cam.VY - 20), (W, cam.VY + 2)]], (120, 70, 80), INK, 2)
    # chat 11: the far blocks seen front-on (were side faces only: a thin sliver), 6-11 storeys rising over the
    # pines (al2); the umbrella pines tall (~17 m) and broad so they make the dark wall down both sides (al2)
    rng = np.random.default_rng(41)
    for s, xin in ((-1, -14.0), (1, 15.0)):
        for i, d in enumerate(np.arange(380, 95, -38)):
            wd, h = rng.uniform(14, 22), rng.uniform(20, 34)
            xa = xin + s * rng.uniform(0, 6)
            xb = xa + s * wd
            xn = min(xa, xb, key=abs)                          # the edge nearest the avenue
            col = PASTEL[(i + (s > 0)) % 5]
            quad(img, cam.p(xn, d + 14), cam.p(xn, d), cam.p(xn, d, h), cam.p(xn, d + 14, h), mix(col, (60, 30, 30), .3),
                 INK, 1.6)                                    # the side toward the avenue, in shadow
            quad(img, cam.p(xa, d), cam.p(xb, d), cam.p(xb, d, h), cam.p(xa, d, h), col, INK, 1.6)
            k = cam.ppm(d)
            for fl in np.arange(3.2, h - 1.5, 3.0):
                for xx in np.arange(min(xa, xb) + 1.2, max(xa, xb) - 1.0, 2.6):
                    q = cam.p(xx, d, fl)
                    img.paste(mix(col, (40, 26, 30), .55), (int(q[0]), int(q[1] - 1.5 * k), int(q[0] + 1.2 * k) + 1,
                                                            int(q[1])))
    for s, x in ((-1, -8.0), (1, 9.0)):                      # umbrella pines down both sides
        for j, d in enumerate(np.arange(400, 30, -12)):
            if (s > 0 and d < 130) or (s < 0 and d < 76):
                continue
            k = cam.ppm(d)
            h = 15 + 3 * ((j * 7 + s) % 3)
            bx, by = cam.p(x, d)
            tx, ty = cam.p(x, d, h - 3)
            poly(img, [(bx - .25 * k, by), (bx + .25 * k, by), (tx + .18 * k, ty), (tx - .18 * k, ty)], (60, 40, 36),
                 INK, 1.2, 0)
            m = shape(img, [blob(tx - s * 1.2 * k, ty - 1.5 * k, 6.5 * k, int(d) + s * 7, squash=.42)], PINE, INK, 1.8)
            shape(img, [blob(tx - s * 2.2 * k, ty - 2.6 * k, 4.0 * k, int(d) + 3, squash=.38)], PINE_L, None, clip=m)
    if heli:                                                # chat 12: beyond the ministry, so it falls behind it
        helicopter(img, heli['x'], heli['y'], heli.get('s', 17), heli.get('turn', 0), heli.get('roll', 0), t,
                   heli.get('hit', False))
        if heli.get('under'):                               # chat 13: the film's fire trail and fireball, behind the ministry
            heli['under'](img)
    _ministry(img, cam, t)
    _bank(img, cam, t)
    # the avenue: dark tarmac in the firelight, a median line, the lane marks
    y0 = cam.VY + 1
    shape(img, [[(0, y0), (W, y0), (W, H), (0, H)]], (76, 50, 46), None)
    for xx in (-3.0, 3.0):
        for d in np.arange(9, 400, 9):
            quad(img, cam.p(xx - .1, d), cam.p(xx + .1, d), cam.p(xx + .1, d + 4), cam.p(xx - .1, d + 4), (150, 110, 80),
                 None, amt=0)
    truck(img, cam, TRUCK_X4, TRUCK_D4, t, 'toppled', 'al')     # chat 12: overturned at the shield line's right end
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
    d, xc = 64, 6.0                                         # chat 11: nearer (was d 80): the brief's centrepiece
    k = cam.ppm(d)
    Z = lambda z: cam.p(0, d, z)[1]                         # noqa: E731
    cx = cam.p(xc, d)[0]
    # the wing along the avenue, going away (x = 7, d 80 -> 125)
    a, b = cam.p(xc, 110), cam.p(xc, d)
    quad(img, a, b, cam.p(xc, d, 15), cam.p(xc, 110, 15), OCHRE_D)
    for z in (4.2, 8.0, 11.8):
        for dd in np.arange(d + 6, 106, 6):
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
    # the flag (chat 11: bigger, 3.6 x 2.4 m, and the black double-headed eagle drawn, not a dot)
    poly(img, [(cx, Z(16)), (cx, Z(23.5))], None, INK, 2.6, 0)
    fl = [(cx, Z(23.4)), (cx + 3.6 * k, Z(23.0)), (cx + 3.7 * k, Z(20.6)), (cx, Z(21.0))]
    poly(img, fl, (206, 28, 34), INK, 2)
    ex, ey, e = cx + 1.85 * k, Z(22.2), .5 * k
    eagle = [(ex - .35 * e, ey + 1.5 * e), (ex - .5 * e, ey + .5 * e),                      # tail, left hip
             (ex - 1.2 * e, ey + .7 * e), (ex - 2.2 * e, ey + .2 * e), (ex - 1.6 * e, ey + .05 * e),   # left wing
             (ex - 2.3 * e, ey - .4 * e), (ex - 1.6 * e, ey - .45 * e), (ex - 2.1 * e, ey - 1.0 * e),
             (ex - 1.2 * e, ey - .8 * e), (ex - .5 * e, ey - .3 * e),
             (ex - .7 * e, ey - 1.0 * e), (ex - 1.1 * e, ey - 1.05 * e), (ex - .7 * e, ey - 1.35 * e),  # left head
             (ex - .25 * e, ey - .9 * e), (ex, ey - .5 * e), (ex + .25 * e, ey - .9 * e),
             (ex + .7 * e, ey - 1.35 * e), (ex + 1.1 * e, ey - 1.05 * e), (ex + .7 * e, ey - 1.0 * e),   # right head
             (ex + .5 * e, ey - .3 * e), (ex + 1.2 * e, ey - .8 * e), (ex + 2.1 * e, ey - 1.0 * e),
             (ex + 1.6 * e, ey - .45 * e), (ex + 2.3 * e, ey - .4 * e), (ex + 1.6 * e, ey + .05 * e),
             (ex + 2.2 * e, ey + .2 * e), (ex + 1.2 * e, ey + .7 * e), (ex + .5 * e, ey + .5 * e),
             (ex + .35 * e, ey + 1.5 * e), (ex, ey + 1.1 * e)]
    poly(img, eagle, (22, 16, 16), None, 0, 0)
    # the roof alight (the brief's "blazing Education Ministry")
    flames(img, cam.p(xc + 9, d)[0], Z(15.2), 13 * k, 8 * k, t, seed=31, n=7)
    flames(img, cx - .4 * r, Z(16.1), 3.2 * k, 3.4 * k, t + .4, seed=32)    # chat 11: on the bay (the wing is hidden)


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
    # chat 17 (readability check; hunt 1 read a cut-off 'ANKA'): letters ~0.9 m tall, centred along the bank, in frame
    text(img, cam.p(x, 52, 5.6), 'BANKA', 52, (60, 46, 40))


# ================================================================================================= vehicles
# Chat 12 (sets stage, the plan's two rows): the water cannon truck (T3 driving in, French white and blue; T4
# overturned and burning, Albanian navy) and the police helicopter (T4; any turn, the moves stage steps it in 45-degree
# turns: side, three-quarter, front and their mirrors). Both flat, one outline each piece, drawn by the moves stage.
TRUCK_LIVERY = {'fr': dict(body=(236, 236, 232), band=(36, 70, 150), cab=(226, 228, 226), word='POLICE', ink=(36, 70, 150)),
                'al': dict(body=(44, 50, 70), band=(70, 80, 104), cab=(52, 58, 78), word='POLICIA', ink=(226, 226, 230))}
TRUCK_LEN, TRUCK_H = 9.8, 3.35
TRUCK_X4, TRUCK_D4 = 2.5, 30.0       # T4: cab end at screen ~640, behind the shield line's right half, rest off frame
HELI_HOME = (800, 290, 22)           # T4: where it hangs (x, y, px a metre): over the flag (top y 325), upper right
TRUCK_D3 = 16.0                      # T3: behind the police rows (d 11) and the bikes (d 14), in front of the kiosk


def truck(img, cam, x, d, t=0.0, state='drive', livery='fr', aim=18.0, flash=0.0):
    """The water cannon truck side-on at depth d, facing left, its front bumper at x (m). state 'drive': upright, the
    roof cannon at `aim` degrees above level; 'toppled': rolled over onto its roof, wheels up, charred and burning.
    flash 0..1: the blue roof lights lit. Returns the nozzle tip on screen (drive) or the fire's centre (toppled)."""
    L = TRUCK_LIVERY[livery]
    k = cam.ppm(d)
    flip = state == 'toppled'
    gx, gy = cam.p(x, d)

    def P(u, z):                                             # u back along the truck (m), z up (m): to screen
        if flip:
            z = TRUCK_H + .1 - z
        return gx + u * k, gy - z * k
    char = (lambda c: mix(c, (30, 24, 24), .62)) if flip else (lambda c: c)
    body, cab, band = char(L['body']), char(L['cab']), char(L['band'])
    # wheels first when upright (the body's skirt hides their tops); last when toppled (they stick up)
    def wheels():
        for u in (1.35, 6.25, 7.65):
            cx, cy = P(u, .55)
            IS.ell(img, cx, cy, .55 * k, .55 * k, (34, 32, 34), INK, max(2, k / 30))
            IS.ell(img, cx, cy, .24 * k, .24 * k, char((150, 150, 150)), None)
    # the chassis rail and bumper
    shape(img, [[P(-.08, .45), P(TRUCK_LEN, .45), P(TRUCK_LEN, .95), P(-.08, .95)]], char((60, 62, 66)), INK, max(2, k / 28))
    # the tank body: a long box, its rear top rounded
    tank = [P(2.45, .85), P(TRUCK_LEN, .85), P(TRUCK_LEN, 2.75), P(TRUCK_LEN - .25, 3.0), P(2.45, 3.0)]
    shape(img, [tank], body, INK, max(2.4, k / 24))
    if not flip:
        wheels()
    shape(img, [[P(2.45, 1.45), P(TRUCK_LEN, 1.45), P(TRUCK_LEN, 1.75), P(2.45, 1.75)]], band, None)
    for u in np.arange(3.6, TRUCK_LEN - .4, 1.55):          # panel seams
        poly(img, [P(u, .9), P(u, 2.95)], None, mix(body, INK, .35), max(1.2, k / 60), 0)
    f = max(12, int(.62 * k))
    cxw, cyw = P(6.2, 2.3)
    if flip:                                                 # rolled over: the word reads upside down, sooted
        lay = Image.new('L', (int(f * len(L['word']) * .8), int(f * 1.5)), 0)
        ImageDraw.Draw(lay).text((lay.width / 2, lay.height / 2), L['word'], anchor='mm', fill=255,
                                 font=ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), f))
        lay = lay.rotate(180)
        img.paste(mix(L['ink'], (40, 34, 34), .5), (int(cxw - lay.width / 2), int(cyw - lay.height / 2)), mask=lay)
    else:
        text(img, (cxw, cyw), L['word'], f, L['ink'])
    # the cab: flat armoured nose, a raked windscreen behind mesh, the door window
    cabp = [P(0, .55), P(0, 1.75), P(.38, 2.95), P(2.4, 3.05), P(2.4, .55)]
    shape(img, [cabp], cab, INK, max(2.4, k / 24))
    shape(img, [[P(0, 1.38), P(2.4, 1.38), P(2.4, 1.68), P(0, 1.68)]], band, None)
    glassc = (60, 74, 92) if not flip else (40, 26, 22)
    for win in ([P(.18, 1.95), P(.48, 2.8), P(1.45, 2.84), P(1.45, 1.95)], [P(1.62, 1.95), P(1.62, 2.84), P(2.22, 2.86), P(2.22, 1.95)]):
        m = shape(img, [win], glassc, INK, max(2, k / 30))
        if flip:                                              # the windows burnt out: fire glowing low inside
            lo = [win[0], win[3], (win[3][0], win[3][1] + (win[1][1] - win[0][1]) * .45),
                  (win[0][0], win[0][1] + (win[1][1] - win[0][1]) * .45)]
            shape(img, [lo], (250, 150, 50), None, clip=m)
        else:                                                 # the mesh: a few diagonal wires inside the glass
            x0_, x1_ = min(q[0] for q in win), max(q[0] for q in win)
            y0_, y1_ = min(q[1] for q in win), max(q[1] for q in win)
            sub = Image.new('L', (W, H), 0)
            dr = ImageDraw.Draw(sub)
            step = max(6, .22 * k)
            for xx in np.arange(x0_ - (y1_ - y0_), x1_, step):
                dr.line([(xx, y1_), (xx + (y1_ - y0_), y0_)], fill=255, width=max(1, int(k / 70)))
                dr.line([(xx, y0_), (xx + (y1_ - y0_), y1_)], fill=255, width=max(1, int(k / 70)))
            img.paste((96, 110, 124), (0, 0), mask=Image.fromarray(np.minimum(np.asarray(sub), np.asarray(m))))
    shape(img, [[P(-.1, .62), P(.22, .62), P(.22, .98), P(-.1, .98)]], char((70, 70, 74)), INK, 2)       # bumper end
    shape(img, [[P(.02, 1.12), P(.2, 1.12), P(.2, 1.32), P(.02, 1.32)]], char((250, 236, 170)), INK, 1.5)  # headlamp
    # the blue lights on the cab roof
    for u in (.55, 2.05):
        on = flash > .5 and not flip
        shape(img, [[P(u - .2, 3.0), P(u + .2, 3.0), P(u + .16, 3.2), P(u - .16, 3.2)]],
              (120, 170, 255) if on else char((40, 70, 160)), INK, 2)
        if on:
            lx, ly = P(u, 3.1)
            glow_disc(img, lx, ly, .55 * k, (150, 190, 255), amt=.3)
    # the roof cannon: a turret on the cab roof, the barrel aimed forward (left) and up
    tb = [P(.95, 3.02), P(1.95, 3.02), P(1.85, 3.38), P(1.05, 3.38)]
    shape(img, [tb], char((150, 152, 156)), INK, max(2, k / 30))
    a = math.radians(aim) * (-1 if flip else 1)
    bx, by = P(1.4, 3.3)
    tip = (bx - 1.45 * k * math.cos(a), by - 1.45 * k * math.sin(a))
    nx, ny = math.sin(a) * .13 * k, -math.cos(a) * .13 * k
    poly(img, [(bx + nx, by + ny), (tip[0] + nx * .8, tip[1] + ny * .8), (tip[0] - nx * .8, tip[1] - ny * .8),
               (bx - nx, by - ny)], char((120, 122, 128)), INK, max(2, k / 34), 0)
    if flip:
        wheels()
        # burning: the engine under the cab and the tank's belly, smoke from the wreck (the moves stage drives t)
        fx, fy = P(1.0, .6)
        flames(img, fx, fy + .2 * k, 2.6 * k, 2.2 * k, t, seed=71, n=6)
        fx2, fy2 = P(5.0, .45)
        flames(img, fx2, fy2 + .1 * k, 3.6 * k, 1.6 * k, t + .5, seed=72, n=7)
        return P(2.6, 1.0)
    return tip


def _hull(pts):
    pts = sorted(set((round(a, 2), round(b, 2)) for a, b in pts))
    if len(pts) < 3:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


HELI_BODY, HELI_BELLY, HELI_GLASS = (232, 234, 236), (34, 60, 130), (70, 96, 120)


def helicopter(img, cx, cy, s, turn=0.0, roll=0.0, t=0.0, hit=False, look=-10.0):
    """The police helicopter (a light twin like the Policia's AW109): white over a blue belly, POLICIA on the boom.
    (cx, cy): the cabin's centre on screen; s px a metre; turn 0 = side-on facing left, 90 = nose to us, 180 =
    facing right (the moves stage steps it in 45s: three drawn turns and their mirrors); roll tilts it in the frame
    (degrees, + = clockwise); look: we see it from below by this many degrees (the rotor disc opens). hit: the
    engine blackened and burning. Every part is a flat shape (the hull of its corners at this turn), one outline."""
    c, sn = math.cos(math.radians(turn)), math.sin(math.radians(turn))
    ce, se = math.cos(math.radians(look)), math.sin(math.radians(look))
    cr, sr = math.cos(math.radians(roll)), math.sin(math.radians(roll))

    def Q(x, y, z):                                         # x forward, y to its left, z up (m) -> screen, depth
        u = -x * c + y * sn
        dep = x * sn + y * c                                 # toward us
        v = z * ce + dep * se
        X, Y = u * s, -(v - 1.0) * s
        return cx + X * cr - Y * sr, cy + X * sr + Y * cr, dep

    def solid(pts3, fill, lw=None, clip=None, line=INK):
        q = [Q(*p)[:2] for p in pts3]
        return shape(img, [_hull(q)], fill, line, lw or max(2, s / 9), clip=clip)

    def ring(x, ry, z0, z1, n=10):                           # a cross-section loop at x
        return [(x, ry * math.cos(a), (z0 + z1) / 2 + (z1 - z0) / 2 * math.sin(a)) for a in np.linspace(0, 6.28, n, endpoint=False)]
    cabin = (ring(-1.7, .72, .4, 1.95) + ring(-.4, .9, .22, 2.1) + ring(1.0, .86, .25, 2.0) + ring(2.0, .6, .42, 1.62)
             + ring(2.75, .22, .8, 1.15))
    boom = ring(-1.4, .38, 1.0, 1.75, 8) + ring(-6.3, .14, 1.5, 1.8, 8)
    fin = [(-6.9, -.05, 1.45), (-6.9, .05, 1.45), (-6.2, -.05, 1.65), (-6.2, .05, 1.65), (-7.1, .05, 3.0),
           (-7.1, -.05, 3.0), (-6.75, .05, 3.0), (-6.75, -.05, 3.0)]
    tailr = [(-6.95 + .75 * math.cos(a), .32, 2.45 + .75 * math.sin(a)) for a in np.linspace(0, 6.28, 16, endpoint=False)]
    cowl = [(x, y, z) for x, zt in ((-2.0, 2.05), (-1.5, 2.45), (.5, 2.5), (1.0, 2.1)) for y in (-.62, .62) for z in (1.8, zt)]
    skids = [[(-1.3, sy, .02), (1.9, sy, .02), (2.2, sy, .18), (-1.3, sy, .1)] for sy in (-.95, .95)]
    struts = [[(x, sy * .95, .06), (x, sy * .55, .5)] for x in (-.7, 1.1) for sy in (-1, 1)]
    disc = [(5.6 * math.cos(a), 5.6 * math.sin(a), 2.75) for a in np.linspace(0, 6.28, 36, endpoint=False)]
    # parts drawn far to near: depth of each part's centre
    parts = [('boom', -3.9, 0.0), ('fin', -6.8, 0.0), ('tailr', -6.95, .32), ('skidL', .3, .95), ('skidR', .3, -.95),
             ('cabin', .3, 0.0)]
    parts.sort(key=lambda p: p[1] * sn + p[2] * c)
    lw = max(2, s / 9)
    for name, _, _ in parts:
        if name == 'boom':
            m = solid(boom, HELI_BODY)
            solid([(x, y, z) for x, y, z in boom if z < 1.38] + [(-6.3, 0, 1.5)], HELI_BELLY, clip=m, line=None)
            if abs(c) > .6:                                   # POLICIA on the boom when we see its side
                bx, by, _ = Q(-3.6, 0, 1.4)
                fs = max(8, int(.42 * s))
                lay = Image.new('L', (int(fs * 5), int(fs * 1.6)), 0)
                ImageDraw.Draw(lay).text((lay.width / 2, lay.height / 2), 'POLICIA', anchor='mm', fill=255,
                                         font=ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), fs))
                lay = lay.resize((max(1, int(lay.width * abs(c))), lay.height)).rotate(-roll, expand=True)
                img.paste((30, 50, 110), (int(bx - lay.width / 2), int(by - lay.height / 2)), mask=lay)
        elif name == 'fin':
            solid(fin, HELI_BELLY)
        elif name == 'tailr':
            q = [Q(*p)[:2] for p in tailr]
            if abs(sn) > .2 or True:
                hl = _hull(q)
                if len(hl) > 2:
                    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
                    ImageDraw.Draw(lay).polygon(hl, fill=(200, 205, 210, 120), outline=(60, 60, 64, 200))
                    img.alpha_composite(lay) if img.mode == 'RGBA' else img.paste(lay, (0, 0), lay)
        elif name.startswith('skid'):
            sy = .95 if name == 'skidL' else -.95
            for st in struts:
                if st[0][1] * sy > 0:
                    poly(img, [Q(*st[0])[:2], Q(*st[1])[:2]], None, (60, 62, 66), max(2, s / 7), 0)
            sk = skids[0] if sy < 0 else skids[1]
            solid(sk + [(x, y, z + .12) for x, y, z in sk], (70, 72, 76))
        else:
            solid(cowl, HELI_BODY if not hit else (46, 38, 38))
            m = solid(cabin, HELI_BODY)
            solid([(x, y, z) for x, y, z in cabin if z < .8] + [(2.75, 0, .8), (-1.7, 0, .8), (2.75, .3, .8), (-1.7, .3, .8),
                                                                (2.75, -.3, .8), (-1.7, -.3, .8)], HELI_BELLY, clip=m, line=None)
            gl = [(x, y, z) for x, y, z in cabin if x >= 1.0 and z > 1.0] + [(1.0, .82, 1.0), (1.0, -.82, 1.0), (2.3, .4, .9), (2.3, -.4, .9)]
            gm = solid(gl, HELI_GLASS, lw=max(1.5, s / 14), clip=m)
            if c > -.2 or True:                               # the cabin door window on the side toward us
                side = 1 if c >= 0 else -1
                dw = [(-.9, side * .84, 1.05), (.6, side * .84, 1.05), (.6, side * .84, 1.75), (-.9, side * .84, 1.7)]
                if abs(c) > .3:
                    solid(dw, HELI_GLASS, lw=max(1.5, s / 14), clip=m)
            poly(img, [Q(.2, 0, 2.35)[:2], Q(.2, 0, 2.78)[:2]], None, (60, 62, 66), max(2, s / 6), 0)   # the mast
            for e in (-1.5, -.6):                             # exhaust stubs
                pass
    # the main rotor: a pale disc (the blur) and two blades whose sweep the moves stage turns with t
    q = _hull([Q(*p)[:2] for p in disc])
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    dl.polygon(q, fill=(200, 206, 214, 105), outline=(90, 96, 104, 150))
    for k_ in range(2):
        a = 6.28 * (t * 5.0) + k_ * math.pi
        p0, p1 = Q(5.5 * math.cos(a), 5.5 * math.sin(a), 2.78), Q(-5.5 * math.cos(a), -5.5 * math.sin(a), 2.78)
        dl.line([p0[:2], p1[:2]], fill=(40, 40, 44, 230), width=max(2, int(s / 7)))
    img.alpha_composite(lay) if img.mode == 'RGBA' else img.paste(lay, (0, 0), lay)
    if hit:                                                   # the engine alight (the trail is the moves stage's)
        ex, ey, _ = Q(-.6, 0, 2.3)
        flames(img, ex, ey + .4 * s, 1.8 * s, 1.6 * s, t, seed=81, n=5)
    return Q(-.6, 0, 2.3)[:2]


def vehicles_sheet(out):
    """The two new vehicles drawn alone at size beside their references, and each in its shot (phone size)."""
    bg = (244, 240, 232)
    B.SS = 1
    S = Image.new('RGB', (2000, 2280), bg)
    d = ImageDraw.Draw(S)
    fb = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 30)
    fr = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans.ttf'), 21)
    d.text((20, 16), 'PROTEST TIERS: the water cannon truck and the police helicopter (sets stage, chat 12)', font=fb, fill=(20, 20, 20))
    # row 1: the truck, upright (T3, French) and overturned burning (T4, Albanian), drawn alone
    cam = Cam(0, 0, 1000, 0)
    for i, (st, lv, lab) in enumerate((('drive', 'fr', 'T3: driving in, cannon up, lights on'),
                                       ('toppled', 'al', 'T4: overturned, burning'))):
        im = Image.new('RGBA', (W, 560), bg + (255,))
        c2 = Cam(80, 470, 1000, 0.0)
        truck(im, c2, 0, 10.0, t=.4, state=st, livery=lv, flash=1.0)
        im = im.convert('RGB').resize((810, 420))
        S.paste(im, (20 + i * 830, 70))
        d.text((20 + i * 830, 494), lab, font=fr, fill=(50, 50, 50))
    # row 2: the helicopter's drawn turns and the hit
    for i, (tn, rl, hit, lab) in enumerate(((0, 0, False, 'side'), (45, 0, False, 'three-quarter'), (90, 0, False, 'front'),
                                             (135, 8, False, '3/4 (mirror)'), (200, 25, True, 'hit, spinning'))):
        im = Image.new('RGBA', (380, 330), bg + (255,))
        helicopter(im, 190, 175, 27, turn=tn, roll=rl, t=.13, hit=hit)
        S.paste(im.convert('RGB'), (20 + i * 392, 540))
        d.text((30 + i * 392, 872), lab, font=fr, fill=(50, 50, 50))
    # row 3: the references, then each in its shot at phone size
    x = 20
    for ref in ('al3-tirana-shield-line-water-cannon', 'de5-frankfurt-water-cannon-police-blue'):
        im = Image.open(os.path.join(REFS, ref + '.jpg')).convert('RGB')
        im.thumbnail((470, 360))
        S.paste(im, (x, 920))
        d.text((x, 920 + im.height + 4), ref.split('-')[0], font=fr, fill=(60, 60, 60))
        x += im.width + 14
    shot3 = paint('t3', .4, truck=dict(x=2.8, aim=20, flash=1.0)).resize((405, 720), Image.LANCZOS)
    shot4 = paint('t4', .4, heli=dict(x=HELI_HOME[0], y=HELI_HOME[1], s=HELI_HOME[2], turn=0)).resize((405, 720), Image.LANCZOS)
    S.paste(shot3, (x + 10, 920)); S.paste(shot4, (x + 430, 920))
    d.text((x + 10, 1645), 'T3 with the truck', font=fr, fill=(50, 50, 50))
    d.text((x + 430, 1645), 'T4 with both', font=fr, fill=(50, 50, 50))
    S = S.crop((0, 0, 2000, 1690))
    S.save(out, quality=88)
    return out


# ------------------------------------------------------------------------------------------------- rule 83, rule 3
SET_BOXES = {                       # chat 11: all measured from the drawing (each helper left out, the difference)
    't1': [('container', (446, 719, 578, 902)), ('domed corner', (822, 60, 945, 559))],
    't2': [('doorway', (0, 783, 113, 1173)), ('gun store window', (174, 754, 786, 1089)),
           ('shutter', (140, 647, 819, 1105)), ('WAFFEN band', (127, 535, 833, 641)), ('closed shop', (847, 663, 1080, 1173)),
           ('street lamp', (0, 94, 175, 1231))],
    't3': [('monument', (234, 453, 688, 1130)), ('kiosk', (848, 901, 1007, 1182)), ('bikes', (533, 1018, 993, 1280)),
           ('car', (0, 757, 228, 1360))],
    't4': [('ministry', (565, 313, 1080, 961)), ('bank', (0, 247, 231, 961)), ('toppled truck', (608, 823, 1079, 1174))],
}
SET_MEANT = {
    't2': [('street lamp', 'doorway', 'the lamp stands on the kerb 1.8 m in front of the doorway'),
           ('shutter', 'gun store window', 'the shutter is half down over the window (the brief)'),
           ('shutter', 'WAFFEN band', 'the shutter box sits right under the sign band'),
           ('street lamp', 'WAFFEN band', 'the lamp arm reaches toward the band, in front of it'),
           ('street lamp', 'gun store window', "the lamp's glow (only) touches the window's left edge"),
           ('street lamp', 'shutter', "the lamp's glow falls on the shutter's left edge, the lamp in front at the kerb")],
    't3': [('kiosk', 'bikes', 'the bike heap burns in front of the kiosk: two fires the brief names together'),
           ('monument', 'bikes', 'the bikes burn in the gap 66 m in front of the base (chat 10 decision; fr4)')],
    't4': [('toppled truck', 'ministry', 'the overturned truck burns on the avenue 34 m in front of the ministry (brief 30)')],
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
    elif cmd == 'vehicles':
        print(vehicles_sheet(sys.argv[2]))
    elif cmd == 'check':
        print('\n'.join(checks()) or 'rule 83: clean')
