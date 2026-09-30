#!/usr/bin/env python3
"""Listening & Learning: five candidate new looks, drawn as concept stills of the same moment
("It is my belief", 17.5 s): the pop star at the mic, sincere, spotlit. Made vertical (1080 x 1920)
from the start, inside the TikTok safe area, with the real burned-in caption.

Every look is drawn by code the same way a full film would be, so each still is honest to how the
film would really render. One shared figure (ginger hair, tattooed forearms, guitar on his back,
in-ear monitor, mic under the chin) is built with different proportions for each look, then drawn
with that look's own eyes, line, texture and palette.

Usage:
    python3 ll_looks.py stills OUT_DIR [pencil riso cutout inkwash stitch]
    python3 ll_looks.py sheet OUT.jpg CURRENT.png STILLS_DIR
"""
import math
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy.ndimage import gaussian_filter

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
TITLE_FONT = os.path.join(HERE, 'fonts', 'Anton-Regular.ttf')
W, H, SS = 1080, 1920, 2
CX = 480  # the middle of the TikTok safe area (x 60-900)
CAPTION = 'It is my belief'


# ---------------------------------------------------------------- basic helpers
def rgb(*c):
    return np.array(c, np.float32) / 255.0


def curve(pts, n=6, closed=True):
    """Catmull-Rom through the points: soft, hand-drawn curves."""
    p = np.asarray(pts, float)
    out = []
    m = len(p) if closed else len(p) - 1
    for i in range(m):
        p0 = p[i - 1] if (closed or i > 0) else p[0]
        p1, p2 = p[i], p[(i + 1) % len(p)]
        p3 = p[(i + 2) % len(p)] if (closed or i + 2 < len(p)) else p[-1]
        for u in np.linspace(0, 1, n, endpoint=False):
            out.append(tuple(0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                                    + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)))
    if not closed:
        out.append(tuple(p[-1]))
    return out


def oval(cx, cy, rx, ry, n=48, a0=0.0, a1=2 * math.pi, rot=0.0):
    c, s = math.cos(rot), math.sin(rot)
    return [(cx + rx * math.cos(a) * c - ry * math.sin(a) * s, cy + rx * math.cos(a) * s + ry * math.sin(a) * c)
            for a in np.linspace(a0, a1, n, endpoint=(a1 - a0 < 2 * math.pi - 1e-6))]


def limb(p1, p2, w1, w2, n=10):
    """A tapered capsule from p1 (width w1) to p2 (width w2)."""
    (x1, y1), (x2, y2) = p1, p2
    a = math.atan2(y2 - y1, x2 - x1)
    pts = [(x2 + w2 / 2 * math.cos(a + t), y2 + w2 / 2 * math.sin(a + t)) for t in np.linspace(-math.pi / 2, math.pi / 2, n)]
    pts += [(x1 + w1 / 2 * math.cos(a + t), y1 + w1 / 2 * math.sin(a + t)) for t in np.linspace(math.pi / 2, 3 * math.pi / 2, n)]
    return pts


def mask(polys, ss=SS, blur=0):
    if polys and isinstance(polys[0][0], (int, float, np.floating)):
        polys = [polys]
    im = Image.new('L', (W * ss, H * ss), 0)
    d = ImageDraw.Draw(im)
    for p in polys:
        d.polygon([(x * ss, y * ss) for x, y in p], fill=255)
    im = im.resize((W, H), Image.BOX)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(im, np.float32) / 255.0


def line_mask(pts, width, ss=SS, widths=None):
    """A stroke along the points. widths (one per point) makes a brush line that swells and tapers."""
    im = Image.new('L', (W * ss, H * ss), 0)
    d = ImageDraw.Draw(im)
    q = [(x * ss, y * ss) for x, y in pts]
    if widths is None:
        d.line(q, fill=255, width=max(1, int(width * ss)), joint='curve')
        for (x, y) in (q[0], q[-1]):
            r = width * ss / 2
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    else:
        for i in range(len(q) - 1):
            w = max(0.6, (widths[i] + widths[i + 1]) / 2) * ss
            d.line([q[i], q[i + 1]], fill=255, width=max(1, int(w)))
            r = widths[i + 1] * ss / 2
            d.ellipse([q[i + 1][0] - r, q[i + 1][1] - r, q[i + 1][0] + r, q[i + 1][1] + r], fill=255)
    im = im.resize((W, H), Image.BOX)
    return np.asarray(im, np.float32) / 255.0


_cache = {}


def noise(seed, scale):
    """Smooth value noise, 0..1, features about `scale` pixels across."""
    k = ('n', seed, scale)
    if k not in _cache:
        rng = np.random.default_rng(seed)
        small = rng.random((H // scale + 3, W // scale + 3)).astype(np.float32)
        im = Image.fromarray(small, 'F').resize(((W // scale + 3) * scale, (H // scale + 3) * scale), Image.BICUBIC)
        _cache[k] = np.clip(np.asarray(im)[:H, :W], 0, 1)
    return _cache[k]


def grain(seed, sigma=0.7):
    k = ('g', seed, sigma)
    if k not in _cache:
        rng = np.random.default_rng(seed)
        a = gaussian_filter(rng.random((H, W)).astype(np.float32), sigma)
        _cache[k] = (a - a.min()) / (a.max() - a.min() + 1e-9)
    return _cache[k]


def streaks(seed, angle, length):
    """Noise smeared along one direction: the texture of pencil strokes or paper fibres, 0..1."""
    k = ('s', seed, angle, length)
    if k not in _cache:
        S = int(math.hypot(W, H)) + 4
        rng = np.random.default_rng(seed)
        a = rng.random((S, S)).astype(np.float32)
        c = np.cumsum(np.pad(a, ((0, 0), (length, 0))), axis=1)
        a = (c[:, length:] - c[:, :-length]) / length
        im = Image.fromarray(gaussian_filter(a, 0.6), 'F').rotate(angle, resample=Image.BILINEAR)
        a = np.asarray(im)[(S - H) // 2:(S - H) // 2 + H, (S - W) // 2:(S - W) // 2 + W]
        lo, hi = np.percentile(a, 2), np.percentile(a, 98)
        _cache[k] = np.clip((a - lo) / (hi - lo), 0, 1)
    return _cache[k]


def shift(a, dx, dy):
    return np.roll(np.roll(a, dy, axis=0), dx, axis=1)


def put(cv, m, col, alpha=1.0):
    m = (m * alpha)[..., None]
    cv[:] = cv * (1 - m) + np.asarray(col, np.float32) * m


def ink(cv, m, col, alpha=1.0):
    """Multiply a transparent colour over what's there (ink, wash, overprinting)."""
    m = (m * alpha)[..., None]
    cv[:] = cv * (1 - m * (1 - np.asarray(col, np.float32)))


def darker(col, k):
    return np.asarray(col, np.float32) * k


# ---------------------------------------------------------------- the figure
class Figure:
    """The pop star, with proportions set per look. All shapes are polygons in frame pixels."""

    def __init__(self, head_cy=610, rx=76, ry=92, jaw=0.4, cheek=0.0, crown=1.0, neck=28, sh_y=745, sh_w=165,
                 hem_y=1080, hem_w=138, belly=10, floor=1370, leg_w=46, gap=8, arm=40, sleeve=150):
        self.__dict__.update(locals())
        del self.__dict__['self']
        cx = CX
        # head: an egg on top, a squarer jaw below, cheeks that can bulge for caricature
        pts = []
        for a in np.linspace(0, 2 * math.pi, 72, endpoint=False):
            c, s = math.cos(a), math.sin(a)
            if s > 0:  # lower half: blend towards a squarer jaw
                n = 2 + 3 * jaw
                x = np.sign(c) * abs(c) ** (2 / n) * rx
                y = abs(s) ** (2 / n) * ry
                x *= 1 + cheek * math.sin(a) ** 2 * (1 - math.sin(a)) * 3.0
            else:
                x, y = c * rx, s * ry * crown
            pts.append((cx + x, head_cy + y))
        self.head = pts
        self.ears = [oval(cx + sg * rx * 0.97, head_cy + 0.08 * ry, rx * 0.17, ry * 0.25) for sg in (-1, 1)]
        top = head_cy - ry * crown
        # short hair close to the skull, a small lift at the crown, a fringe swept to one side, sideburns
        outer = [(cx + rx * 1.04 * math.cos(a), head_cy + ry * crown * (1.06 + 0.06 * math.exp(-((a - 4.4) / 0.35) ** 2))
                  * math.sin(a)) for a in np.linspace(math.pi * 1.0, math.pi * 2.0, 18)]
        inner = [(cx + rx * 1.0, head_cy + 0.12 * ry), (cx + rx * 0.9, head_cy - 0.2 * ry),
                 (cx + rx * 0.62, head_cy - 0.4 * ry), (cx + rx * 0.2, head_cy - 0.48 * ry),
                 (cx - rx * 0.25, head_cy - 0.56 * ry), (cx - rx * 0.62, head_cy - 0.46 * ry),
                 (cx - rx * 0.9, head_cy - 0.2 * ry), (cx - rx * 1.0, head_cy + 0.12 * ry)]
        self.hair = curve(outer + inner, 4)
        self.hair_top = top
        self.neck = [(cx - neck, head_cy + ry * 0.7), (cx + neck, head_cy + ry * 0.7), (cx + neck + 4, sh_y + 14),
                     (cx - neck - 4, sh_y + 14)]
        mid = (sh_y + hem_y) / 2
        tee = [(cx - neck - 16, sh_y - 4), (cx - sh_w * 0.72, sh_y + 14), (cx - sh_w, sh_y + 56),
               (cx - sh_w - 26, sh_y + sleeve), (cx - sh_w + 22, sh_y + sleeve + 12), (cx - hem_w - belly, mid + 40),
               (cx - hem_w, hem_y), (cx + hem_w, hem_y), (cx + hem_w + belly, mid + 40),
               (cx + sh_w - 22, sh_y + sleeve + 12), (cx + sh_w + 26, sh_y + sleeve), (cx + sh_w, sh_y + 56),
               (cx + sh_w * 0.72, sh_y + 14), (cx + neck + 16, sh_y - 4)]
        self.tee = curve(tee, 4)
        self.collar = oval(cx, sh_y + 2, neck + 16, 16, 20, 0.1, math.pi - 0.1)
        self.legs = []
        for sg in (-1, 1):
            a_in, a_out = cx + sg * gap, cx + sg * (gap + 2 * leg_w)
            self.legs.append([(a_in, hem_y - 12), (a_out + sg * 6, hem_y - 12), (a_out - sg * 2, floor - 16),
                              (a_in + sg * 4, floor - 16)])
        self.shoes = [oval(cx + sg * (gap + leg_w + 12), floor - 6, leg_w + 16, 16) for sg in (-1, 1)]
        # left arm (his right, screen left) hangs from the sleeve
        s1 = (cx - sh_w - 4, sh_y + sleeve - 10)
        self.hand_l_at = (cx - sh_w - 12, hem_y + 4)
        self.arm_l = limb(s1, self.hand_l_at, arm, arm * 0.8)
        self.hand_l = oval(self.hand_l_at[0], self.hand_l_at[1] + 14, arm * 0.5, arm * 0.62)
        # right arm (screen right): elbow at his side, forearm up to the mic under his chin
        s2 = (cx + sh_w + 4, sh_y + sleeve - 10)
        self.elbow = (cx + sh_w + 30, sh_y + sleeve + 70)
        self.hand_r_at = (cx + rx * 0.95, head_cy + ry * 1.2)
        self.upper_r = limb(s2, self.elbow, arm, arm * 0.95)
        self.fore_r = limb(self.elbow, self.hand_r_at, arm * 0.95, arm * 0.78)
        self.hand_r = oval(self.hand_r_at[0] - 4, self.hand_r_at[1] + 2, arm * 0.62, arm * 0.52, rot=-0.5)
        self.mouth_at = (cx - rx * 0.02, head_cy + ry * 0.55)
        mh = (cx + rx * 0.3, head_cy + ry * 0.66)
        self.mic_head_at = mh
        self.mic = limb((self.hand_r_at[0] + 8, self.hand_r_at[1] + 10), mh, 14, 18)
        self.mic_head = oval(mh[0], mh[1], 15, 14)
        # the guitar slung on his back: neck and headstock over his (screen-left) shoulder
        g0, g1 = (cx - sh_w * 0.35, sh_y + 30), (cx - sh_w * 0.92, head_cy - ry * 0.55)
        self.gneck = limb(g0, g1, 20, 17)
        ga = math.atan2(g1[1] - g0[1], g1[0] - g0[0])
        g2 = (g1[0] + 60 * math.cos(ga), g1[1] + 60 * math.sin(ga))
        self.headstock = limb(g1, g2, 34, 30, 4)
        self.pegs = [(g1[0] + t * (g2[0] - g1[0]) + sg * 22 * math.cos(ga + math.pi / 2),
                      g1[1] + t * (g2[1] - g1[1]) + sg * 22 * math.sin(ga + math.pi / 2))
                     for t in (0.25, 0.55, 0.85) for sg in (-1, 1)]
        self.strap = [(cx - sh_w * 0.55, sh_y + 20), (cx + hem_w * 0.8, hem_y - 60)]
        # face positions
        self.eyes = [(cx + sg * rx * 0.4 - 4, head_cy - 0.02 * ry) for sg in (-1, 1)]

    def along(self, p, q, t):
        return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def spot_cone(floor, top_w=46, bot_w=330):
    return [(CX - top_w, 0), (CX + top_w, 0), (CX + bot_w, floor + 40), (CX - bot_w, floor + 40)]


# ---------------------------------------------------------------- caption (the same in every look)
def caption(img, text=CAPTION, y=1450):
    """Burned-in caption, drawn fresh on the vertical frame: white bold with a black edge, wrapped to at
    most 800 px, centred on x = 480, inside the safe area."""
    d = ImageDraw.Draw(img)
    size = 64
    font = ImageFont.truetype(FONT, size)
    words, rows, cur = text.split(), [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if cur and d.textlength(trial, font=font) > 800:
            rows.append(cur)
            cur = w
        else:
            cur = trial
    rows.append(cur)
    for i, row in enumerate(rows):
        yy = y - (len(rows) - 1 - i) * 76
        d.text((CX, yy), row, font=font, fill=(255, 255, 255), anchor='mm', stroke_width=6, stroke_fill=(0, 0, 0))


def to_img(cv):
    return Image.fromarray((np.clip(cv, 0, 1) * 255).astype(np.uint8), 'RGB')


# ================================================================ 1. coloured pencil (house style)
def look_pencil():
    """Coloured pencil on warm paper, in the family of Dam and The Salt: visible diagonal strokes, the
    paper showing through, outlines in a darker pencil of each shape's own colour (never black), real
    proportions, small almond eyes with a coloured iris and heavy lids."""
    F = Figure(head_cy=600, rx=68, ry=88, jaw=0.35, neck=34, sh_w=162, hem_w=130, belly=4, arm=34, sleeve=140)
    paper = rgb(236, 226, 206)
    cv = np.ones((H, W, 3), np.float32) * paper
    tooth = grain(21, 0.6)

    def fill(m, col, pressure=0.9, angle=62, seed=1, length=16):
        s = streaks(seed, angle, length)
        cover = np.clip(pressure * 1.15 - 0.42 * (1 - s) - 0.3 * tooth, 0, 1)
        put(cv, m * cover, col)

    def edge(poly, col, w=3.2, seed=5):
        pts = np.array(poly + [poly[0]], float)
        wob = noise(seed, 40)
        pts[:, 0] += (wob[np.clip(pts[:, 1].astype(int), 0, H - 1), np.clip(pts[:, 0].astype(int), 0, W - 1)] - .5) * 3
        m = line_mask([tuple(p) for p in pts], w)
        s = streaks(seed + 7, 20, 6)
        put(cv, m * np.clip(0.5 + 0.6 * s - 0.25 * tooth, 0, 1), col)

    # the dark stage: layered indigo and aubergine pencil, the spotlight left lighter and warmer
    everything = np.ones((H, W), np.float32)
    cone = mask(spot_cone(F.floor), blur=26)
    floor_pool = mask(oval(CX, F.floor, 340, 70), blur=18)
    lit = np.clip(cone * 0.75 + floor_pool * 0.9, 0, 1)
    fill(everything * (1 - lit * 0.75), rgb(40, 36, 72), 1.0, 62, 2, 18)
    fill(everything * (1 - lit), rgb(58, 34, 62), 0.5, 55, 3, 14)
    fill(lit, rgb(246, 222, 170), 0.55, 62, 4, 16)
    fill(floor_pool, rgb(214, 196, 190), 0.6, 8, 5, 24)
    # stage lip and the dark crowd below
    crowd = mask([(0, F.floor + 70), (W, F.floor + 70), (W, H), (0, H)], blur=3)
    fill(crowd, rgb(24, 20, 40), 1.0, 62, 6, 20)

    GUIT, GUIT_D = rgb(150, 92, 52), rgb(92, 54, 30)
    fill(mask(F.gneck), GUIT, 1.0, 40, 7)
    edge(F.gneck, darker(GUIT, 0.5))
    fill(mask(F.headstock), GUIT_D, 1.0, 40, 8)
    edge(F.headstock, darker(GUIT_D, 0.6))
    for p in F.pegs:
        put(cv, mask(oval(p[0], p[1], 5, 5, 12)), rgb(220, 220, 214))
    TR = rgb(46, 46, 60)
    for leg in F.legs:
        fill(mask(leg), TR, 1.0, 70, 9)
        edge(leg, darker(TR, 0.55))
    for sh in F.shoes:
        fill(mask(sh), rgb(240, 238, 232), 0.9, 10, 10)
        edge(sh, rgb(150, 148, 150))
    TEE = rgb(176, 160, 206)
    fill(mask(F.tee), TEE, 1.0, 62, 11)
    fill(mask([(CX + 20, F.sh_y + 40), (CX + F.sh_w, F.sh_y + 50), (CX + F.hem_w, F.hem_y), (CX + 40, F.hem_y)], blur=20),
         rgb(118, 100, 160), 0.6, 62, 12)
    edge(F.tee, darker(TEE, 0.5))
    put(cv, line_mask(F.strap, 8), rgb(96, 62, 44))
    SKIN = rgb(240, 196, 166)
    SKIN_E = rgb(176, 108, 88)
    for part in (F.arm_l, F.hand_l, F.neck):
        fill(mask(part), SKIN, 0.95, 62, 13)
        edge(part, SKIN_E, 2.6)
    # tattoo sleeves: small coloured pencil scribbles
    rng = np.random.default_rng(4)
    tat = [rgb(60, 110, 170), rgb(70, 140, 90), rgb(210, 110, 60), rgb(190, 60, 70), rgb(110, 80, 160)]

    def tattoos(p, q, n):
        for i in range(n):
            x, y = F.along(p, q, (i + 0.5) / n)
            fill(mask(oval(x + rng.uniform(-9, 9), y, rng.uniform(6, 11), rng.uniform(5, 8), 16,
                           rot=rng.uniform(0, 3))), tat[i % 5], 0.9, 30, 14)
    tattoos((CX - F.sh_w - 4, F.sh_y + F.sleeve + 10), F.hand_l_at, 9)
    for e in F.ears:
        fill(mask(e), SKIN, 0.95, 62, 15)
        edge(e, SKIN_E, 2.4)
    fill(mask(F.head), SKIN, 1.0, 62, 16)
    # soft pencil shading down the far side of the face, rosy cheeks
    fill(mask(oval(CX + F.rx * 0.55, F.head_cy + 10, F.rx * 0.45, F.ry * 0.9), blur=16), rgb(214, 150, 126), 0.55, 62, 17)
    for sg in (-1, 1):
        fill(mask(oval(CX + sg * F.rx * 0.52, F.head_cy + F.ry * 0.3, 18, 12), blur=6), rgb(226, 132, 120), 0.5, 62, 18)
    edge(F.head, SKIN_E, 3.0)
    put(cv, mask(oval(CX + F.rx * 0.99, F.head_cy + 6, 5, 6, 12)), rgb(30, 30, 34))  # in-ear monitor
    HAIR = rgb(206, 104, 44)
    fill(mask(F.hair), HAIR, 1.0, 70, 19, 18)
    fill(mask(F.hair), rgb(160, 70, 30), 0.45, -20, 20, 14)
    edge(F.hair, rgb(130, 56, 22), 2.8)
    # stubble: short ginger flecks round the jaw
    for i in range(140):
        a = rng.uniform(0.35, math.pi - 0.35)
        r = rng.uniform(0.62, 0.95)
        x, y = CX + F.rx * r * math.cos(a), F.head_cy + F.ry * 0.25 + F.ry * 0.7 * r * math.sin(a)
        put(cv, line_mask([(x, y), (x + 2, y + 4)], 1.4), rgb(190, 110, 70), 0.45)
    # eyes: small almonds, blue iris, heavy sincere lids; worried brows
    for (ex, ey), sg in zip(F.eyes, (-1, 1)):
        alm = curve([(ex - 16, ey), (ex, ey - 7), (ex + 16, ey), (ex, ey + 6)], 6)
        put(cv, mask(alm), rgb(246, 242, 234))
        put(cv, mask(oval(ex - 2, ey + 1, 6.5, 6.5)) * mask(alm), rgb(78, 118, 160))
        put(cv, mask(oval(ex - 2, ey + 1, 2.8, 2.8)), rgb(28, 26, 30))
        put(cv, line_mask(curve([(ex - 17, ey + 1), (ex - 4, ey - 8), (ex + 10, ey - 7), (ex + 17, ey)], 5, False), 3.4),
            rgb(90, 50, 40))
        put(cv, line_mask([(ex - 10, ey + 7), (ex + 10, ey + 6)], 1.4), rgb(170, 110, 96), 0.7)
        put(cv, line_mask([(ex - sg * 4, ey - 25), (ex + sg * 18, ey - 18)], 4.5), rgb(196, 110, 58))
    # nose, mouth open mid-word, the mic
    put(cv, line_mask(curve([(CX - 4, F.head_cy + 2), (CX - 10, F.head_cy + 30), (CX - 2, F.head_cy + 36),
                             (CX + 8, F.head_cy + 33)], 5, False), 2.6), SKIN_E)
    mx, my = F.mouth_at
    mo = curve([(mx - 18, my), (mx, my - 3), (mx + 18, my), (mx + 10, my + 14), (mx - 10, my + 14)], 5)
    fill(mask(mo), rgb(110, 40, 44), 1.0, 62, 21)
    put(cv, mask([(mx - 14, my), (mx + 14, my - 1), (mx + 12, my + 4), (mx - 12, my + 4)]), rgb(244, 240, 232))
    for part in (F.upper_r, F.fore_r):
        fill(mask(part), SKIN, 0.95, 62, 22)
        edge(part, SKIN_E, 2.6)
    tattoos(F.elbow, F.hand_r_at, 6)
    fill(mask(F.mic), rgb(40, 40, 46), 1.0, 30, 23)
    fill(mask(F.mic_head), rgb(120, 120, 128), 1.0, 30, 24)
    edge(F.mic_head, rgb(40, 40, 46), 2.4)
    fill(mask(F.hand_r), SKIN, 1.0, 62, 25)
    edge(F.hand_r, SKIN_E, 2.6)
    # a last warm glaze of the spotlight over him
    fill(cone * 0.6, rgb(250, 236, 196), 0.35, 62, 26)
    img = to_img(cv)
    caption(img)
    return img


# ================================================================ 2. two-colour risograph
def look_riso():
    """Two inks on cream paper, fluorescent pink and deep blue, printed slightly out of register with
    grainy coverage and halftone dots for the in-between tones. No outlines at all: shapes are just
    ink. A stockier, poster-like build: big square head, short legs. Eyes are heavy half-closed lids."""
    F = Figure(head_cy=600, rx=96, ry=100, jaw=1.0, crown=0.85, neck=34, sh_y=752, sh_w=178, hem_w=160, belly=16,
               hem_y=1120, leg_w=56, gap=6, arm=46, sleeve=140)
    PAPER = rgb(244, 238, 224)
    PINK = rgb(255, 72, 176)
    BLUE = rgb(40, 62, 130)
    pink = np.zeros((H, W), np.float32)
    blue = np.zeros((H, W), np.float32)

    def lay(layer, m, d):
        layer[:] = layer * (1 - m) + d * m

    cone = mask(spot_cone(F.floor, 40, 320), blur=4)
    pool = mask(oval(CX, F.floor, 330, 64), blur=2)
    lay(blue, np.ones((H, W), np.float32), 0.92)
    lay(blue, cone, 0.18)
    lay(pink, cone, 0.12)
    lay(blue, pool, 0.3)
    lay(pink, pool, 0.25)
    crowd = mask([(0, F.floor + 70), (W, F.floor + 70), (W, H), (0, H)])
    lay(blue, crowd, 1.0)
    lay(pink, crowd, 0.35)
    # figure: every part is a pair of ink densities (pink, blue)
    parts = [
        (F.gneck, .6, .6), (F.headstock, .9, 1.0),
        (F.legs[0], .0, 1.0), (F.legs[1], .0, 1.0), (F.shoes[0], .0, .0), (F.shoes[1], .0, .0),
        (F.tee, .0, .42), (F.arm_l, .38, .0), (F.hand_l, .38, .0), (F.neck, .38, .06),
        (F.ears[0], .38, .0), (F.ears[1], .38, .0), (F.head, .38, .0), (F.hair, 1.0, .0),
        (F.upper_r, .38, .0), (F.fore_r, .38, .0), (F.mic, .0, 1.0), (F.mic_head, .5, 1.0), (F.hand_r, .38, .0),
    ]
    for poly, p, b in parts:
        m = mask(poly)
        lay(pink, m, p)
        lay(blue, m, b)
        if poly is F.tee:  # the strap and a shadow down one side of the tee
            lay(blue, line_mask(F.strap, 10), 1.0)
            lay(blue, mask([(CX + 50, F.sh_y + 40), (CX + F.sh_w, F.sh_y + 50), (CX + F.hem_w + 10, F.hem_y),
                            (CX + 70, F.hem_y)]) * m, 0.7)
        if poly is F.head:  # shadow side of the face in pink halftone
            lay(pink, mask(oval(CX + F.rx * 0.7, F.head_cy + 10, F.rx * 0.4, F.ry)) * m, 0.62)
    # tattoos: solid blue flash shapes (a star, an anchor-ish bar, dots)
    rng = np.random.default_rng(9)
    for p, q, n in (((CX - F.sh_w - 4, F.sh_y + F.sleeve + 10), F.hand_l_at, 5), (F.elbow, F.hand_r_at, 4)):
        for i in range(n):
            x, y = F.along(p, q, (i + 0.5) / n)
            r = rng.uniform(7, 11)
            star = [(x + r * (1 if k % 2 == 0 else .45) * math.cos(k * math.pi / 5 + .3),
                     y + r * (1 if k % 2 == 0 else .45) * math.sin(k * math.pi / 5 + .3)) for k in range(10)]
            lay(blue, mask(star), 1.0)
    # face in blue ink: heavy half-closed lids (a flat top, a curved bottom) with the pupil tucked under
    for (ex, ey), sg in zip(F.eyes, (-1, 1)):
        ex += sg * 4
        lay(pink, mask(oval(ex, ey + 2, 20, 11)), 0.0)  # paper-white eye
        lay(blue, mask(oval(ex, ey + 4, 7, 7)) * mask(oval(ex, ey + 2, 20, 11)), 1.0)
        lid = [(ex - 23, ey - 1), (ex + 23, ey - 1), (ex + 23, ey - 12), (ex - 23, ey - 12)]
        lay(pink, mask(lid) * mask(oval(ex, ey + 2, 24, 14)), 0.9)
        lay(blue, line_mask([(ex - 23, ey), (ex + 23, ey)], 5), 1.0)
        lay(blue, mask([(ex - sg * 2, ey - 30), (ex + sg * 26, ey - 22), (ex + sg * 26, ey - 16), (ex - sg * 2, ey - 23)]), 1.0)
    lay(blue, mask([(CX - 3, F.head_cy + 8), (CX + 6, F.head_cy + 8), (CX + 14, F.head_cy + 42), (CX - 10, F.head_cy + 42)]), 0.4)
    mx, my = F.mouth_at
    lay(blue, mask([(mx - 22, my + 2), (mx + 22, my), (mx + 14, my + 20), (mx - 14, my + 20)]), 1.0)
    lay(pink, mask([(mx - 22, my + 2), (mx + 22, my), (mx + 14, my + 20), (mx - 14, my + 20)]), 1.0)
    # stubble: pink halftone band on the jaw
    jaw = mask(F.head) * (1 - mask(oval(CX, F.head_cy - 10, F.rx * 0.95, F.ry * 0.9)))
    lay(pink, jaw, 0.62)

    # print it: halftone for mid tones, grainy uneven ink for solids, pink slightly out of register
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    per = 7.0

    def screen(ang):
        a = math.radians(ang)
        u = (xx * math.cos(a) + yy * math.sin(a)) * 2 * math.pi / per
        v = (-xx * math.sin(a) + yy * math.cos(a)) * 2 * math.pi / per
        return 0.5 + 0.25 * (np.cos(u) + np.cos(v))

    def printed(d, ang, seed):
        g = grain(seed, 0.8)
        dots = np.clip((d + (g - 0.5) * 0.25 - (1 - screen(ang))) * 3.5 + 0.5, 0, 1)
        dots = np.where(d > 0.97, 1.0, dots)
        blotch = noise(seed + 1, 24)
        return dots * np.clip(0.9 + 0.12 * blotch - 0.35 * (grain(seed + 2, 0.5) > 0.93), 0, 1)

    pk = shift(printed(pink, 15, 31), 7, -5)
    bl = printed(blue, 45, 41)
    cv = np.ones((H, W, 3), np.float32) * PAPER
    ink(cv, bl, BLUE)
    ink(cv, pk, PINK, 0.95)
    img = to_img(cv)
    caption(img)
    return img


# ================================================================ 3. paper cut-out with split pins
def look_cutout():
    """Cut coloured paper on black card: every piece has slightly rough scissor edges, paper fibre, and a
    real drop shadow; joints are brass split pins; hair is torn tissue; the spotlight is a sheet of
    tracing paper. Long thin strip arms, a pear-shaped body, a wide oval head. Eyes are white paper
    with a skin-coloured lid piece lowered over half of each."""
    F = Figure(head_cy=590, rx=88, ry=84, jaw=0.0, crown=1.0, neck=24, sh_y=735, sh_w=140, hem_w=172, belly=26,
               hem_y=1110, leg_w=40, gap=12, arm=30, sleeve=120)
    cv = np.ones((H, W, 3), np.float32) * rgb(22, 20, 24)
    put(cv, (grain(51, 1.2) - 0.5) * 0.25 + 0.12, rgb(60, 56, 62))
    fib = streaks(52, 30, 14)

    def piece(poly_or_mask, col, seed, rough=0.22, shadow=1.0, tex=0.07, torn=False, lift=1.0):
        m = poly_or_mask if isinstance(poly_or_mask, np.ndarray) else mask(poly_or_mask)
        n = noise(seed, 5 if not torn else 3)
        m = np.clip((Image_blur(m, 1.2) - 0.5 + (n - 0.5) * rough) * 6 + 0.5, 0, 1)
        if torn:  # a fibrous pale rim where tissue is torn
            rim = np.clip(Image_blur(m, 3) * 1.6, 0, 1) * (1 - m)
        if shadow:
            sh = Image_blur(shift(m, int(6 * lift), int(9 * lift)), 5 * lift)
            ink(cv, sh, rgb(0, 0, 0), 0.55 * shadow)
        if torn:
            put(cv, rim * (0.4 + 0.6 * grain(seed + 3, 0.6)), rgb(250, 226, 200), 0.8)
        c = np.asarray(col, np.float32)[None, None, :] * (1 - tex + tex * 2 * (0.6 * grain(seed + 1, 0.7) + 0.4 * fib))[..., None]
        m3 = m[..., None]
        cv[:] = cv * (1 - m3) + c * m3
        return m

    def pin(x, y):
        ink(cv, mask(oval(x + 2, y + 3, 9, 9), blur=2), rgb(0, 0, 0), 0.6)
        put(cv, mask(oval(x, y, 8, 8)), rgb(196, 150, 60))
        put(cv, mask(oval(x - 2.5, y - 2.5, 3, 3), blur=1), rgb(255, 236, 170))

    # tracing-paper spotlight: pale, translucent, crinkled at the edge
    cone = mask(spot_cone(F.floor, 44, 300))
    cone = np.clip((Image_blur(cone, 1.5) - 0.5 + (noise(53, 8) - .5) * 0.2) * 6 + .5, 0, 1)
    put(cv, cone * (0.28 + 0.06 * streaks(54, 80, 40)), rgb(236, 232, 214))
    pool = piece(oval(CX, F.floor, 320, 58), rgb(90, 88, 96), 55, shadow=0.5)
    put(cv, pool * cone * 0.25, rgb(236, 232, 214))
    piece([(0, F.floor + 72), (W, F.floor + 66), (W, H), (0, H)], rgb(12, 10, 14), 56, shadow=0.8)
    # the crowd: a strip of cut black heads against the stage lip
    for i in range(16):
        x = 20 + i * 70
        piece(oval(x, F.floor + 118 + (i % 2) * 14, 30, 34), rgb(6, 6, 8), 57 + i, shadow=0)

    piece(F.gneck, rgb(170, 110, 60), 60, lift=0.6)
    piece(F.headstock, rgb(80, 48, 30), 61, lift=0.6)
    for p in F.pegs:
        pin(*p)
    for i, leg in enumerate(F.legs):
        piece(leg, rgb(34, 40, 58), 62 + i)
    for i, sh in enumerate(F.shoes):
        piece(sh, rgb(236, 234, 226), 64 + i)
    TEE = rgb(92, 140, 128)  # sage green card
    piece(F.tee, TEE, 66, lift=1.3)
    piece(limb(F.strap[0], F.strap[1], 12, 12), rgb(120, 70, 44), 67)
    SKIN = rgb(236, 188, 156)
    piece(F.arm_l, SKIN, 68)
    piece(F.hand_l, SKIN, 69)
    # tattoos: little scraps cut from magazine print (tiny halftone squares of colour)
    rng = np.random.default_rng(3)
    cols = [rgb(40, 90, 170), rgb(220, 70, 60), rgb(250, 200, 40), rgb(60, 150, 80)]
    yy, xx = np.mgrid[0:H, 0:W]
    dots = ((np.sin(xx * 1.1) + np.sin(yy * 1.1)) > 0.2).astype(np.float32)

    def scraps(p, q, n):
        for i in range(n):
            x, y = F.along(p, q, (i + 0.5) / n)
            s = rng.uniform(7, 10)
            a = rng.uniform(0, 1.5)
            sq = [(x + s * math.cos(a + k * math.pi / 2), y + s * math.sin(a + k * math.pi / 2)) for k in range(4)]
            m = piece(sq, cols[i % 4], 70 + i, rough=0.1, lift=0.25)
            put(cv, m * dots, rgb(250, 246, 236), 0.35)
    scraps((CX - F.sh_w - 4, F.sh_y + F.sleeve + 5), F.hand_l_at, 5)
    pin(CX - F.sh_w - 4, F.sh_y + F.sleeve - 10)
    piece(F.neck, SKIN, 80)
    for i, e in enumerate(F.ears):
        piece(e, SKIN, 81 + i)
    head = piece(F.head, SKIN, 83, lift=1.2)
    # a second, darker skin piece on the shadow side
    piece(mask(oval(CX + F.rx * 0.62, F.head_cy + 8, F.rx * 0.46, F.ry * 0.95)) * mask(F.head), rgb(214, 160, 130), 84,
          shadow=0, rough=0.05)
    put(cv, mask(oval(CX + F.rx * 0.98, F.head_cy + 6, 6, 7)), rgb(20, 20, 22))
    # hair: three layers of torn orange tissue
    for k, (dx, dy, col) in enumerate(((0, 0, rgb(222, 110, 40)), (-10, 6, rgb(240, 140, 60)), (12, 10, rgb(200, 90, 34)))):
        hm = mask(F.hair) * mask(oval(CX + dx, F.head_cy - F.ry * 0.5 + dy, F.rx * 1.05, F.ry * 0.62))
        piece(hm, col, 85 + k, rough=0.6, torn=True, lift=0.4, tex=0.12)
    # stubble: a piece of fine sandpaper-ish orange paper at the jaw
    jaw = mask(F.head) * (1 - mask(oval(CX, F.head_cy - 14, F.rx * 0.9, F.ry * 0.9))) * (grain(88, 0.5) > 0.55)
    put(cv, jaw, rgb(206, 120, 70), 0.7)
    # eyes: white paper ovals, black pupils, a skin-coloured lid piece lowered over the top half
    for (ex, ey), sg in zip(F.eyes, (-1, 1)):
        piece(oval(ex, ey, 17, 14), rgb(248, 246, 238), 90 + sg, rough=0.1, lift=0.3)
        piece(oval(ex - 1, ey + 3, 7, 7), rgb(16, 16, 18), 92 + sg, rough=0.05, shadow=0)
        piece([(ex - 20, ey - 17), (ex + 20, ey - 17), (ex + 20, ey), (ex - 20, ey + 1)], rgb(226, 176, 146), 94 + sg,
              rough=0.1, lift=0.35)
        piece(limb((ex - sg * 2, ey - 28), (ex + sg * 20, ey - 22), 8, 7), rgb(200, 96, 40), 96 + sg, rough=0.1, lift=0.3)
    piece(limb((CX - 2, F.head_cy + 4), (CX - 8, F.head_cy + 34), 12, 16), rgb(222, 170, 140), 98, lift=0.35)
    mx, my = F.mouth_at
    piece(oval(mx, my + 8, 20, 12), rgb(120, 30, 40), 99, rough=0.1, lift=0.3)
    piece([(mx - 14, my - 2), (mx + 14, my - 2), (mx + 12, my + 5), (mx - 12, my + 5)], rgb(246, 244, 236), 100,
          rough=0.05, shadow=0)
    piece(F.upper_r, SKIN, 101)
    pin(CX + F.sh_w + 4, F.sh_y + F.sleeve - 10)
    piece(F.fore_r, SKIN, 102, lift=1.2)
    pin(*F.elbow)
    scraps(F.elbow, F.hand_r_at, 4)
    piece(F.mic, rgb(30, 30, 34), 103, lift=1.2)
    piece(F.mic_head, rgb(150, 150, 156), 104, lift=1.2)
    put(cv, mask(F.mic_head) * (np.sin(xx * 0.9) * np.sin(yy * 0.9) > 0.3), rgb(60, 60, 66), 0.6)
    piece(F.hand_r, SKIN, 105, lift=1.3)
    pin(*F.hand_r_at)
    img = to_img(cv)
    caption(img)
    return img


def Image_blur(a, sigma):
    return gaussian_filter(a.astype(np.float32), sigma)


# ================================================================ 4. loose ink line and watercolour wash
def look_inkwash():
    """A loose brush-pen line that swells and tapers, overshoots and leaves gaps, over a watercolour
    wash printed a little off the line, on white paper. Here the stage is the paper and the dark is a
    wash around him. Caricature pushed further: big soft jowls and a small crown, tiny close-set eyes
    with bags beneath, eyebrows pushed up in earnest concern, a big hand on the mic."""
    F = Figure(head_cy=615, rx=84, ry=104, jaw=0.2, cheek=0.32, crown=0.78, neck=30, sh_y=770, sh_w=150, hem_w=146,
               belly=22, hem_y=1090, leg_w=44, gap=8, arm=36, sleeve=130)
    cv = np.ones((H, W, 3), np.float32) * rgb(250, 248, 242)
    rng = np.random.default_rng(12)

    def wash(m, col, alpha=0.6, seed=0, off=(8, -6)):
        n = noise(seed, 30)
        m = shift(m, *off)
        m = np.clip((Image_blur(m, 2.5) - 0.5 + (n - 0.5) * 0.35) * 5 + 0.5, 0, 1)
        edge = np.clip(m - Image_blur(m, 6), 0, 1) * 1.8  # pigment collects at the edge as it dries
        gran = 0.85 + 0.3 * grain(seed + 1, 1.0)
        ink(cv, np.clip(m * (0.7 + 0.3 * noise(seed + 2, 90)) * gran + edge, 0, 1), col, alpha)

    def brush(pts, w=6.0, seed=0, over=10):
        """One loose stroke: jittered, overshooting at both ends, thick in the middle, tapering."""
        p = np.array(pts, float)
        if len(p) < 2:
            return
        p += rng.normal(0, 1.2, p.shape)
        d0, d1 = p[0] - p[1], p[-1] - p[-2]
        p = np.vstack([p[0] + d0 / (np.linalg.norm(d0) + 1e-6) * over * rng.uniform(0.2, 1), p,
                       p[-1] + d1 / (np.linalg.norm(d1) + 1e-6) * over * rng.uniform(0.2, 1)])
        t = np.linspace(0, 1, len(p))
        widths = w * (0.25 + 0.95 * np.sin(np.pi * t) ** 0.7) * rng.uniform(0.8, 1.15)
        m = line_mask([tuple(q) for q in p], w, widths=widths)
        dry = np.clip(0.75 + 0.5 * streaks(seed + 300, 20, 8), 0, 1)
        put(cv, m * dry, rgb(28, 24, 30))

    def outline(poly, w=6.0, seed=0, gaps=1):
        """Draw a shape's outline as one or two open strokes, leaving a gap or two unclosed."""
        n = len(poly)
        start = rng.integers(0, n)
        cut = int(n * rng.uniform(0.06, 0.14))
        pts = [poly[(start + i) % n] for i in range(n - cut)]
        if gaps > 1 and len(pts) >= 10:
            h = len(pts) // 2
            brush(pts[:h + 2], w, seed)
            brush(pts[h + 3:], w, seed + 1)
        else:
            brush(pts, w, seed)

    # the dark around the spotlight: a violet-grey wash, the spot left as bare paper
    cone = mask(spot_cone(F.floor, 60, 330))
    everything = np.ones((H, W), np.float32)
    wash(everything * (1 - cone), rgb(92, 84, 120), 0.85, 1, (0, 0))
    wash(everything * (1 - cone) * (1 - mask(oval(CX, 700, 520, 760), blur=120)), rgb(60, 56, 90), 0.5, 2, (0, 0))
    wash(mask([(0, F.floor + 60), (W, F.floor + 60), (W, H), (0, H)]), rgb(50, 46, 70), 0.9, 3, (0, 0))
    brush([(CX - 360, F.floor + 30), (CX, F.floor + 44), (CX + 360, F.floor + 28)], 5, 4)
    # a few quick heads in the crowd
    for i in range(9):
        x = 60 + i * 115 + rng.uniform(-20, 20)
        brush(oval(x, F.floor + 150, 34, 40, 18, math.pi, 2 * math.pi), 5, 10 + i, 4)

    wash(mask(F.gneck + F.headstock), rgb(176, 110, 60), 0.8, 20)
    brush(F.gneck[:len(F.gneck) // 2 + 1], 4.5, 21, 3)
    outline(F.headstock, 4.5, 22)
    for i, leg in enumerate(F.legs):
        wash(mask(leg), rgb(70, 72, 96), 0.85, 23 + i)
        outline(leg, 6, 25 + i, 2)
    for i, s in enumerate(F.shoes):
        outline(s, 5, 27 + i)
    wash(mask(F.tee), rgb(236, 190, 96), 0.75, 29)  # a mustard tee
    wash(mask([(CX + 40, F.sh_y + 40), (CX + F.sh_w + 20, F.sh_y + 60), (CX + F.hem_w + 20, F.hem_y),
               (CX + 60, F.hem_y)]), rgb(180, 120, 60), 0.4, 30)
    outline(F.tee, 6.5, 31, 2)
    brush(F.strap, 7, 32)
    brush(F.collar, 4.5, 33)
    SKIN = rgb(246, 196, 164)
    wash(mask([F.arm_l, F.hand_l, F.neck]), SKIN, 0.85, 34)
    outline(F.arm_l, 5.5, 35, 2)
    outline(F.hand_l, 5, 36)
    brush(F.neck[:2] + [F.neck[2]], 5, 37)
    # tattoos: quick scribbled doodles in colour-less ink
    for p, q, n in (((CX - F.sh_w - 4, F.sh_y + F.sleeve + 10), F.hand_l_at, 5), (F.elbow, F.hand_r_at, 4)):
        for i in range(n):
            x, y = F.along(p, q, (i + 0.5) / n)
            brush(oval(x + rng.uniform(-6, 6), y, 8, 6, 10), 2.4, 40 + i, 0)
    wash(mask([F.head] + F.ears), SKIN, 0.85, 50)
    wash(mask(oval(CX + F.rx * 0.6, F.head_cy + 20, F.rx * 0.45, F.ry * 0.9)), rgb(220, 140, 120), 0.45, 51)
    for sg in (-1, 1):
        wash(mask(oval(CX + sg * F.rx * 0.6, F.head_cy + F.ry * 0.28, 22, 14)), rgb(236, 120, 110), 0.55, 52 + sg, (3, 2))
    wash(mask(F.hair), rgb(226, 112, 44), 0.95, 54, (6, -8))
    for e in F.ears:
        outline(e, 4.5, 55)
    outline(F.head, 6.5, 56, 2)
    # hair drawn as a few quick flicks rather than an outline
    brush(F.hair[:len(F.hair) * 2 // 3], 4.5, 59, 2)
    for k in range(6):
        a = math.pi * (1.15 + 0.7 * k / 5)
        x0, y0 = CX + F.rx * 0.8 * math.cos(a), F.head_cy + F.ry * F.crown * 0.85 * math.sin(a)
        brush([(x0, y0), (x0 + 12, y0 + 8 + rng.uniform(-2, 3))], 2.6, 60 + k, 1)
    put(cv, mask(oval(CX + F.rx * 1.0, F.head_cy + 8, 5, 6, 12)), rgb(28, 24, 30))
    # eyes: tiny close-set, a short curved stroke for each lid, a pupil tick, bags beneath; worried brows
    for (ex, ey), sg in zip(F.eyes, (-1, 1)):
        ex -= sg * 8
        brush([(ex - 13, ey + 1), (ex - 4, ey - 6), (ex + 6, ey - 6), (ex + 13, ey)], 4.2, 70 + sg, 2)
        put(cv, mask(oval(ex - 1, ey + 1, 4, 4.5)), rgb(28, 24, 30))
        brush([(ex - 10, ey + 11), (ex, ey + 15), (ex + 10, ey + 11)], 2.4, 72 + sg, 0)
        brush([(ex - sg * 6, ey - 26), (ex + sg * 8, ey - 32), (ex + sg * 22, ey - 24)], 5, 74 + sg, 2)
    # forehead creases, nose, jowl line, stubble dots
    for k in range(3):
        brush([(CX - 26, F.head_cy - 48 - 9 * k), (CX, F.head_cy - 51 - 9 * k), (CX + 24, F.head_cy - 47 - 9 * k)], 2.2, 80 + k, 0)
    brush([(CX - 2, F.head_cy + 4), (CX - 12, F.head_cy + 36), (CX - 2, F.head_cy + 44), (CX + 10, F.head_cy + 40)], 4.2, 84, 2)
    for i in range(70):
        a = rng.uniform(0.3, math.pi - 0.3)
        r = rng.uniform(0.7, 0.97)
        x, y = CX + F.rx * r * math.cos(a) * 1.1, F.head_cy + F.ry * 0.3 + F.ry * 0.62 * r * math.sin(a)
        put(cv, mask(oval(x, y, 1.4, 1.4, 8)), rgb(120, 80, 60), 0.8)
    mx, my = F.mouth_at
    mo = curve([(mx - 20, my), (mx, my - 4), (mx + 20, my + 1), (mx + 8, my + 18), (mx - 10, my + 17)], 5)
    wash(mask(mo), rgb(150, 50, 60), 0.9, 86, (2, 2))
    outline(mo, 4.2, 87)
    wash(mask([F.upper_r, F.fore_r, F.hand_r]), SKIN, 0.85, 88)
    outline(F.upper_r, 5.5, 89, 2)
    outline(F.fore_r, 5.5, 90, 2)
    wash(mask(F.mic + F.mic_head), rgb(60, 60, 70), 0.9, 91, (3, -2))
    outline(F.mic, 4.5, 92)
    outline(F.mic_head, 4.5, 93)
    big = oval(F.hand_r_at[0] - 4, F.hand_r_at[1] + 4, F.arm * 0.95, F.arm * 0.72, rot=-0.5)
    wash(mask(big), SKIN, 0.9, 94)
    outline(big, 6, 95)
    for k in range(3):
        x, y = F.hand_r_at
        brush([(x - 24 + 4 * k, y - 8 + 11 * k), (x + 10 + 4 * k, y - 18 + 11 * k)], 3.2, 96 + k, 0)
    img = to_img(cv)
    caption(img)
    return img


# ================================================================ 5. cross-stitch sampler (own idea)
STITCH = 10  # one stitch = 10 x 10 pixels, so the picture is 108 x 192 stitches


def look_stitch():
    """A cross-stitch sampler: the whole frame is 108 x 192 stitches in a small set of embroidery-thread
    colours on black Aida cloth, the unlit stage left as bare cloth. Each stitch is a real X of thread
    with a sheen along it; features are picked out in backstitch. Blocky, doll-like build: a big head,
    a square body. Eyes are 3-stitch whites with a lid row of darker thread above."""
    F = Figure(head_cy=590, rx=100, ry=104, jaw=0.7, crown=0.95, neck=30, sh_y=752, sh_w=170, hem_w=160, belly=4,
               hem_y=1110, leg_w=54, gap=8, arm=46, sleeve=140)
    # 1) a flat colour design at full size, then read one colour per stitch
    NONE = rgb(0, 0, 0) - 1  # marks cloth left bare
    flat = np.ones((H, W, 3), np.float32) * NONE
    cone = mask(spot_cone(F.floor, 40, 320))
    put(flat, cone, rgb(72, 70, 108))
    put(flat, mask(oval(CX, F.floor, 330, 62)), rgb(120, 116, 150))
    SKIN, SKIN_D = rgb(242, 196, 166), rgb(214, 156, 126)
    order = [(F.gneck, rgb(170, 100, 50)), (F.headstock, rgb(90, 52, 30)), (F.legs[0], rgb(46, 54, 84)),
             (F.legs[1], rgb(46, 54, 84)), (F.shoes[0], rgb(244, 244, 240)), (F.shoes[1], rgb(244, 244, 240)),
             (F.tee, rgb(64, 120, 176)), (F.arm_l, SKIN), (F.hand_l, SKIN), (F.neck, SKIN_D),
             (F.ears[0], SKIN), (F.ears[1], SKIN), (F.head, SKIN), (F.hair, rgb(214, 104, 38))]
    for poly, col in order:
        put(flat, mask(poly, 1), col)
    put(flat, line_mask(F.strap, 12, 1), rgb(120, 70, 44))
    put(flat, mask(oval(CX + F.rx * 0.6, F.head_cy + 12, F.rx * 0.4, F.ry * 0.85), 1) * mask(F.head, 1), SKIN_D)
    put(flat, mask([(CX + 60, F.sh_y + 40), (CX + F.sh_w, F.sh_y + 50), (CX + F.hem_w, F.hem_y), (CX + 80, F.hem_y)], 1)
        * mask(F.tee, 1), rgb(44, 90, 140))
    for sg in (-1, 1):
        put(flat, mask(oval(CX + sg * F.rx * 0.55, F.head_cy + F.ry * 0.32, 16, 10), 1), rgb(236, 140, 130))
    for poly, col in ((F.upper_r, SKIN), (F.fore_r, SKIN), (F.mic, rgb(36, 36, 40)), (F.mic_head, rgb(150, 150, 158)),
                      (F.hand_r, SKIN)):
        put(flat, mask(poly, 1), col)
    rng = np.random.default_rng(5)
    tat = [rgb(40, 90, 170), rgb(60, 150, 80), rgb(230, 120, 50), rgb(200, 50, 60)]
    for p, q, n in (((CX - F.sh_w - 4, F.sh_y + F.sleeve + 10), F.hand_l_at, 5), (F.elbow, F.hand_r_at, 3)):
        for i in range(n):
            x, y = F.along(p, q, (i + 0.5) / n)
            put(flat, mask(oval(x, y, 9, 9), 1), tat[i % 4])
    gy, gx = H // STITCH, W // STITCH
    cells = flat[STITCH // 2::STITCH, STITCH // 2::STITCH][:gy, :gx].copy()

    def cell(x, y):
        return int(x // STITCH), int(y // STITCH)

    # face placed stitch by stitch so it reads: eyes, lids, brows, mouth
    for (ex, ey), sg in zip(F.eyes, (-1, 1)):
        c, r = cell(ex, ey)
        cells[r, c - 2:c + 2] = rgb(250, 250, 246)
        cells[r, c - 1 if sg > 0 else c] = rgb(30, 50, 90)
        cells[r - 1, c - 2:c + 2] = rgb(150, 90, 70)  # the heavy lid row, half over the eye
        br = r - 3
        cells[br, c - 2:c + 2] = rgb(200, 100, 44)
        cells[br - 1, c - 1 * sg if sg > 0 else c + 1] = rgb(200, 100, 44)  # inner end raised
    mc, mr = cell(*F.mouth_at)
    cells[mr, mc - 3:mc + 3] = rgb(110, 30, 40)
    cells[mr + 1, mc - 2:mc + 2] = rgb(110, 30, 40)
    cells[mr + 2, mc - 1:mc + 1] = rgb(110, 30, 40)
    cells[mr, mc - 2:mc + 2] = rgb(246, 244, 238)
    # stubble: every other stitch round the jaw in a sandier thread
    hc, hr = cell(CX, F.head_cy)
    for r in range(mr - 1, mr + 5):
        for c in range(hc - 9, hc + 10):
            if (r + c) % 2 == 0 and np.all(np.abs(cells[r, c] - SKIN) < 0.02) and not (mr - 1 <= r <= mr + 1 and abs(c - mc) <= 2):
                cells[r, c] = rgb(222, 160, 110)
    ic, ir = cell(CX + F.rx * 0.98, F.head_cy + 6)
    cells[ir, ic] = rgb(24, 24, 28)

    # 2) the cloth: black Aida with its woven blocks and holes
    yy, xx = np.mgrid[0:H, 0:W]
    u, v = (xx % STITCH) / STITCH, (yy % STITCH) / STITCH
    weave = 0.75 + 0.25 * np.sin(u * math.pi) * np.sin(v * math.pi)
    holes = ((u < 0.14) | (u > 0.86)) & ((v < 0.14) | (v > 0.86))
    cv = np.ones((H, W, 3), np.float32) * rgb(26, 26, 30) * weave[..., None]
    cv[holes] = rgb(6, 6, 8)
    cv *= (0.9 + 0.2 * grain(71, 0.6))[..., None]
    # 3) the stitches: two crossing strands of thread in every coloured cell, with a sheen along them
    d1 = np.abs(u - v)
    d2 = np.abs(u + v - 1)
    th = 0.19
    s1 = np.clip((th - d1) / 0.05, 0, 1) * ((u > 0.08) & (u < 0.92))
    s2 = np.clip((th - d2) / 0.05, 0, 1) * ((u > 0.08) & (u < 0.92))
    sheen1 = 0.72 + 0.4 * np.cos(d1 / th * math.pi / 2) ** 2 + 0.08 * np.sin((u + v) * 40)
    sheen2 = 0.78 + 0.4 * np.cos(d2 / th * math.pi / 2) ** 2 + 0.08 * np.sin((u - v) * 40)
    ci = np.clip(yy // STITCH, 0, gy - 1)
    cj = np.clip(xx // STITCH, 0, gx - 1)
    colour = cells[ci, cj]
    stitched = colour[..., 0] >= 0
    jitter = (0.94 + 0.12 * np.random.default_rng(8).random((gy, gx)))[ci, cj]
    for s, sh in ((s1, sheen1), (s2, sheen2)):
        m = (s * stitched)[..., None]
        cv[:] = cv * (1 - m) + np.clip(colour * (sh * jitter)[..., None], 0, 1) * m
    # thin shadow of the top strand
    # 4) backstitch outline round the head and hair, in dark brown thread, along stitch edges
    face_cells = np.zeros((gy, gx), bool)
    for poly in (F.head, F.hair):
        face_cells |= mask(poly, 1)[STITCH // 2::STITCH, STITCH // 2::STITCH][:gy, :gx] > 0.5
    back = np.zeros((H, W), np.float32)
    im = Image.new('L', (W * 2, H * 2), 0)
    d = ImageDraw.Draw(im)
    for r in range(gy):
        for c in range(gx):
            if not face_cells[r, c]:
                continue
            for dr, dc, seg in ((-1, 0, ((c, r), (c + 1, r))), (1, 0, ((c, r + 1), (c + 1, r + 1))),
                                (0, -1, ((c, r), (c, r + 1))), (0, 1, ((c + 1, r), (c + 1, r + 1)))):
                rr, cc = r + dr, c + dc
                if not (0 <= rr < gy and 0 <= cc < gx) or not face_cells[rr, cc]:
                    (a, b), (e, f) = seg
                    d.line([(a * STITCH * 2, b * STITCH * 2), (e * STITCH * 2, f * STITCH * 2)], fill=255, width=5)
    back = np.asarray(im.resize((W, H), Image.BOX), np.float32) / 255
    put(cv, back, rgb(70, 36, 24))
    img = to_img(cv)
    caption(img)
    return img


LOOKS = {
    'pencil': ('1. Coloured pencil', 'House style: Dam, The Salt', look_pencil),
    'riso': ('2. Two-colour riso print', 'Pink + blue ink, halftone, off-register', look_riso),
    'cutout': ('3. Paper cut-out', 'Card, torn tissue, brass split-pin joints', look_cutout),
    'inkwash': ('4. Ink line + wash', 'Loose brush line, watercolour off the line', look_inkwash),
    'stitch': ('5. Cross-stitch sampler', '108 x 192 stitches on black Aida', look_stitch),
}


# ---------------------------------------------------------------- comparison sheet
def safe_guides(img):
    """Overlay TikTok's no-go zones, for checking (not for the film)."""
    o = img.convert('RGBA')
    lay = Image.new('RGBA', o.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rectangle([0, 0, W, 310], fill=(255, 0, 0, 70))
    d.rectangle([900, int(H * 0.45), W, H], fill=(255, 0, 0, 70))
    d.rectangle([0, 1500, W, H], fill=(255, 0, 0, 70))
    d.rectangle([60, 310, 900, 1500], outline=(0, 255, 0, 255), width=4)
    o.alpha_composite(lay)
    return o.convert('RGB')


def sheet(out, current, stills_dir, pick='pencil'):
    tw, th = 480, 853
    pad, head, lab = 36, 190, 120
    cols, rows = 3, 2
    Wd, Hd = cols * tw + (cols + 1) * pad, head + rows * (th + lab) + (rows + 1) * pad
    s = Image.new('RGB', (Wd, Hd), (24, 22, 28))
    d = ImageDraw.Draw(s)
    tf = ImageFont.truetype(TITLE_FONT, 72)
    d.text((pad, 34), 'LISTENING & LEARNING - NEW LOOKS', font=tf, fill=(178, 24, 52))
    f1 = ImageFont.truetype(FONT, 30)
    f2 = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 21)
    d.text((pad, 140), '"It is my belief" (17.5 s), 1080 x 1920, TikTok safe area, real caption',
           font=f2, fill=(200, 196, 206))
    panels = [('Current look', 'Too close to FilmCow', Image.open(current))]
    for k, (name, sub, _) in LOOKS.items():
        panels.append((name, sub, Image.open(os.path.join(stills_dir, f'{k}.png'))))
    for i, (name, sub, im) in enumerate(panels):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = head + pad + r * (th + lab + pad)
        s.paste(im.convert('RGB').resize((tw, th), Image.LANCZOS), (x, y))
        chosen = LOOKS.get(pick, ('',))[0] == name
        if chosen:
            d.rectangle([x - 6, y - 6, x + tw + 5, y + th + 5], outline=(178, 24, 52), width=6)
        d.text((x, y + th + 18), name, font=f1,
               fill=(255, 120, 140) if chosen else (240, 238, 244))
        d.text((x, y + th + 62), sub, font=f2, fill=(170, 166, 178))
        if chosen:
            d.rectangle([x, y + 14, x + 230, y + 58], fill=(178, 24, 52))
            d.text((x + 12, y + 20), 'RECOMMENDED', font=f2, fill=(255, 255, 255))
    s.save(out, quality=88)


def main():
    mode = sys.argv[1]
    if mode == 'stills':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for k in (sys.argv[3:] or list(LOOKS)):
            t0 = time.time()
            img = LOOKS[k][2]()
            img.save(os.path.join(out, f'{k}.png'), optimize=True)
            print(f'{k}: {time.time() - t0:.1f} s', flush=True)
    elif mode == 'sheet':
        sheet(sys.argv[2], sys.argv[3], sys.argv[4], *(sys.argv[5:6]))
    elif mode == 'guides':
        for p in sys.argv[2:]:
            safe_guides(Image.open(p)).save(p.replace('.png', '_guides.jpg'), quality=80)


if __name__ == '__main__':
    main()
