"""NEW STORY CHAPTER: BAYEUX: ENDLESS CONQUEST. Three new scenes stitched in the tapestry's style.

Each scene is composed as a wool map: the tapestry's borders, our stitched figures cut out of Sam's reference
scenes (already carrying their new weapons and skins), and new stitched buildings, fire, beds, the book, villagers
and animals; then a Latin caption stitched above, and the whole stitched like everything else.

    python3 bayeux_story.py build        stitch the three scenes into the cache (data/bayeux/ch1..ch3)
    python3 bayeux_story.py check DIR    flat wool maps for checking
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import bayeux_stitch as BS
import bayeux_weapons as BW

S = BW.S
H_REF = 330                        # every chapter scene is as tall as the Ice Claw reference (borders included)
I = BS.IDX
LIN = I['linen']
FONT = os.path.join(BS.HERE, 'fonts', 'Cinzel-Variable.ttf')

# --------------------------------------------------------------------------------------- figures to reuse
# (reference scene, polygon round the figure in that reference's pixels, after its swap?)
CUTS = {
    'archer':  ('rifle', [(255, 40), (612, 40), (612, 140), (470, 190), (480, 300), (535, 330), (545, 412), (470, 412),
                          (430, 330), (372, 300), (322, 405), (248, 412), (262, 170)], True),
    'ghostrider': ('ghost', [(180, 30), (525, 30), (525, 110), (470, 140), (470, 285), (300, 290), (252, 180),
                             (170, 120)], True),
    'clawrider': ('claw', [(205, 85), (345, 85), (360, 140), (345, 282), (225, 282), (210, 200)], True),
    'collector': ('stapler', [(100, 70), (330, 70), (330, 200), (300, 200), (305, 345), (100, 345)], True),
    'william': ('william', [(176, 40), (212, 6), (312, 6), (314, 58), (390, 58), (460, 100), (460, 170), (420, 180),
                            (410, 450), (70, 450), (60, 200), (118, 70)], True),
    'messenger': ('stapler', [(375, 80), (488, 80), (500, 345), (375, 345)], True),
}
_SCENE_CACHE = {}


def cut(key):
    name, poly, after = CUTS[key]
    if (name, after) not in _SCENE_CACHE:
        _SCENE_CACHE[(name, after)] = BW.scene_labels(name, after=after)
    lab, forced = _SCENE_CACHE[(name, after)]
    if forced is None:
        forced = np.full(lab.shape, np.nan, np.float32)
    m = Image.new('L', (lab.shape[1], lab.shape[0]), 0)
    ImageDraw.Draw(m).polygon([(x * S, y * S) for x, y in poly], fill=255)
    mask = (np.asarray(m) > 0) & (lab != LIN)
    ys, xs = np.nonzero(mask)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return lab[y0:y1, x0:x1], forced[y0:y1, x0:x1], mask[y0:y1, x0:x1], (x0 / S, y0 / S)


class Scene:
    def __init__(self, w_ref):
        self.w = int(w_ref * S)
        self.h = int(H_REF * S)
        self.lab = np.full((self.h, self.w), LIN, np.int16)
        self.forced = np.full((self.h, self.w), np.nan, np.float32)
        self.borders()

    def borders(self):
        """The tapestry's own upper and lower borders, taken from the Ice Claw scene and repeated along."""
        src = BS.trace('claw', S)
        top, bot = src[:int(72 * S)], src[int(283 * S):int(H_REF * S)]
        for band, y in ((top, 0), (bot, int(283 * S))):
            bw = band.shape[1]
            for x in range(0, self.w, bw):
                k = min(bw, self.w - x)
                self.lab[y:y + band.shape[0], x:x + k] = band[:, :k]

    @staticmethod
    def scaled(key, k, flip=False):
        lab, forced, mask, (ox, oy) = cut(key)
        h, w = lab.shape
        nh, nw = max(1, int(h * k)), max(1, int(w * k))
        L = np.asarray(Image.fromarray(lab.astype(np.int32)).resize((nw, nh), Image.NEAREST)).astype(np.int16)
        M = np.asarray(Image.fromarray(mask.astype(np.uint8) * 255).resize((nw, nh), Image.NEAREST)) > 0
        F = np.asarray(Image.fromarray(forced).resize((nw, nh), Image.NEAREST))
        if flip:
            L, M, F = L[:, ::-1], M[:, ::-1], np.pi - F[:, ::-1]
        return L, M, F, ox, oy, nw, nh

    def sprite(self, scene, tag, key, x, y, k, extra=None):
        """A figure that moves in the film (William dancing, a collector's recoil): stitched on its own with a
        see-through background, not into the scene. Its place is recorded in ANCHORS."""
        L, M, F, ox, oy, nw, nh = self.scaled(key, k)
        pad = int(14 * S)
        lab = np.full((nh + 2 * pad, nw + 2 * pad), LIN, np.int16)
        frc = np.full(lab.shape, np.nan, np.float32)
        lab[pad:pad + nh, pad:pad + nw][M] = L[M]
        frc[pad:pad + nh, pad:pad + nw][M] = F[M]
        msk = np.zeros(lab.shape, bool)
        msk[pad:pad + nh, pad:pad + nw] = M
        x0, y0 = x - pad / S, y - pad / S

        def to_scene(px, py):
            return x + (px - ox) * k, y + (py - oy) * k
        if extra:
            Ly = BW.Layer(lab.shape[1], lab.shape[0])
            extra(Ly, lambda px, py: (px - x0, py - y0), to_scene)
            wl, wa = Ly.arrays()
            on = wl != BW.NONE
            lab[on], frc[on], msk[on] = wl[on], wa[on], True
        rgb = BS.stitch(lab, 3.0, frc, seed=33)
        from scipy import ndimage as ndi
        al = ndi.gaussian_filter(ndi.binary_dilation(msk, iterations=1).astype(np.float32), 0.8)
        Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)])).save(
            os.path.join(BW.CACHE, f'{scene}-{tag}.png'))
        ANCHORS.setdefault(scene, {}).setdefault('sprites', []).append(
            dict(tag=tag, x=x0, y=y0, w=lab.shape[1] / S, h=lab.shape[0] / S))
        return to_scene

    def put(self, key, x, y, k, flip=False):
        """A cut-out figure, scaled by k, its top-left at (x, y) in this scene's reference pixels. Returns a function
        mapping the figure's own reference pixels to this scene's (to place extra details on it)."""
        L, M, F, ox, oy, nw, nh = self.scaled(key, k, flip)
        X, Y = int(x * S), int(y * S)
        ya, yb, xa, xb = max(0, Y), min(self.h, Y + nh), max(0, X), min(self.w, X + nw)
        sub = M[ya - Y:yb - Y, xa - X:xb - X]
        self.lab[ya:yb, xa:xb][sub] = L[ya - Y:yb - Y, xa - X:xb - X][sub]
        self.forced[ya:yb, xa:xb][sub] = F[ya - Y:yb - Y, xa - X:xb - X][sub]

        def to_scene(px, py):
            u, v = (px - ox) * k, (py - oy) * k
            if flip:
                u = nw / S - u
            return x + u, y + v
        return to_scene

    def draw(self, fn):
        """Draw new wool areas with a BW.Layer (reference-pixel coordinates), on top of what is there."""
        L = BW.Layer(self.w, self.h)
        fn(L)
        wl, wa = L.arrays()
        on = wl != BW.NONE
        self.lab[on] = wl[on]
        self.forced[on] = wa[on]

    def caption(self, text, x, y, size=20):
        """Latin capitals stitched in dark blue-green above the scene, like the tapestry's captions."""
        f = ImageFont.truetype(FONT, int(size * S))
        f.set_variation_by_axes([700])
        m = Image.new('L', (self.w, self.h), 0)
        ImageDraw.Draw(m).text((x * S, y * S), text, font=f, fill=255)
        on = np.asarray(m) > 110
        self.lab[on] = I['navy']
        self.forced[on] = np.nan


# -------------------------------------------------------------------------------------- new stitched things
V = math.pi / 2


def person(L, x, y, h, tunic='terracotta', legs='bluegreen', helmet=None, facing=1, pose='stand', arms='down'):
    """A small tapestry figure in profile: feet at (x, y), height h, in the tapestry's flat way."""
    f = facing

    def P(u, v):
        return (x + u * h * f, y - v * h)
    if pose == 'run':
        L.line([P(0, 0.46), P(0.22, 0.24), P(0.32, 0.02)], legs, h * 0.07)
        L.line([P(0, 0.46), P(-0.14, 0.22), P(-0.30, 0.10)], legs, h * 0.07)
    else:
        L.line([P(0.02, 0.46), P(0.06, 0.02)], legs, h * 0.07)
        L.line([P(-0.04, 0.46), P(-0.08, 0.02)], legs, h * 0.07)
    L.poly([P(-0.13, 0.82), P(0.12, 0.82), P(0.20, 0.40), P(-0.20, 0.40)], tunic, V, 'madder', 1.1)
    if arms == 'up':
        L.line([P(0.08, 0.78), P(0.20, 0.96)], tunic, h * 0.06)
        L.line([P(-0.08, 0.78), P(-0.02, 0.98)], tunic, h * 0.06)
    elif arms == 'forward':
        L.line([P(0.08, 0.78), P(0.34, 0.70)], tunic, h * 0.06)
    else:
        L.line([P(0.06, 0.78), P(0.16, 0.56)], tunic, h * 0.06)
    hx, hy = P(0.02, 0.91)
    L.ellipse(hx, hy, h * 0.075, h * 0.085, 'buff', 0.0, 'madder', 1.0)
    if helmet:
        L.poly([P(-0.08, 0.93), P(0.09, 0.93), P(0.0, 1.06)], helmet, V, 'black', 1.0)


def flames(L, x, y, w, h, seed=0):
    """Stitched flames: tongues of terracotta with ochre and buff hearts."""
    rng = np.random.default_rng(seed)
    n = max(3, int(w / 9))
    for i in range(n):
        cx = x + (i + 0.5) * w / n + rng.uniform(-2, 2)
        hh = h * rng.uniform(0.6, 1.0)
        ww = w / n * 0.8
        for wool, s in (('terracotta', 1.0), ('ochre', 0.62), ('buff', 0.3)):
            L.poly([(cx - ww * s, y), (cx - ww * 0.3 * s, y - hh * 0.55 * s), (cx + ww * 0.2 * s, y - hh * s),
                    (cx + ww * 0.45 * s, y - hh * 0.45 * s), (cx + ww * s, y)], wool, V,
                   'madder' if s == 1.0 else None, 1.0)


def house(L, x, y, w, h, roof='terracotta', wall='ochre', fire=True, seed=0):
    """A Saxon house: walls with a door, a steep thatched roof with stitched rows."""
    L.poly([(x, y), (x + w, y), (x + w, y - h * 0.55), (x, y - h * 0.55)], wall, V, 'madder', 1.2)
    L.poly([(x + w * 0.4, y), (x + w * 0.6, y), (x + w * 0.6, y - h * 0.32), (x + w * 0.4, y - h * 0.32)], 'navy', V)
    L.poly([(x - w * 0.12, y - h * 0.55), (x + w * 1.12, y - h * 0.55), (x + w * 0.5, y - h)], roof, 0.0, 'madder', 1.4)
    for k in (0.68, 0.8):
        L.line([(x + w * 0.5 - w * 0.62 * (1 - k) / 0.45 * 0.45, y - h * k),
                (x + w * 0.5 + w * 0.62 * (1 - k) / 0.45 * 0.45, y - h * k)], 'madder', 0.9)
    if fire:
        flames(L, x - w * 0.05, y - h * 0.62, w * 1.1, h * 0.75, seed)


def abbey(L, x, y, w, h):
    """The abbey: a long nave with round arches, a central tower, a cross; the tapestry's way of drawing churches."""
    L.poly([(x, y), (x + w, y), (x + w, y - h * 0.5), (x, y - h * 0.5)], 'buff', V, 'madder', 1.4)
    for i in range(5):
        ax = x + w * (0.08 + i * 0.18)
        L.poly([(ax, y), (ax + w * 0.1, y), (ax + w * 0.1, y - h * 0.3), (ax + w * 0.05, y - h * 0.38),
                (ax, y - h * 0.3)], 'bluegreen' if i % 2 else 'terracotta', V, 'madder', 1.0)
    L.poly([(x - w * 0.04, y - h * 0.5), (x + w * 1.04, y - h * 0.5), (x + w * 0.96, y - h * 0.62),
            (x + w * 0.04, y - h * 0.62)], 'terracotta', 0.0, 'madder', 1.2)
    for i in range(14):                                                                       # roof tiles
        L.line([(x + w * (0.05 + i * 0.065), y - h * 0.52), (x + w * (0.05 + i * 0.065), y - h * 0.60)], 'madder', 0.8)
    tx = x + w * 0.42
    L.poly([(tx, y - h * 0.62), (tx + w * 0.16, y - h * 0.62), (tx + w * 0.16, y - h * 0.9), (tx, y - h * 0.9)],
           'ochre', V, 'madder', 1.2)
    L.poly([(tx - w * 0.02, y - h * 0.9), (tx + w * 0.18, y - h * 0.9), (tx + w * 0.08, y - h * 1.0)], 'bluegreen', 0.0,
           'madder', 1.0)
    cx = tx + w * 0.08
    L.line([(cx, y - h * 1.0), (cx, y - h * 1.12)], 'black', 1.6)
    L.line([(cx - w * 0.025, y - h * 1.08), (cx + w * 0.025, y - h * 1.08)], 'black', 1.6)
    for i in (0, 1):                                                                         # end turrets
        ex = x + (w * 0.02 if i == 0 else w * 0.9)
        L.poly([(ex, y - h * 0.5), (ex + w * 0.08, y - h * 0.5), (ex + w * 0.08, y - h * 0.74), (ex, y - h * 0.74)],
               'sage', V, 'madder', 1.0)
        L.poly([(ex - w * 0.01, y - h * 0.74), (ex + w * 0.09, y - h * 0.74), (ex + w * 0.04, y - h * 0.84)],
               'terracotta', 0.0, 'madder', 1.0)


def palace(L, x, y, w, h):
    """The bishop's palace at Durham: two storeys of arches, towers, beds with sleepers inside, burning."""
    L.poly([(x, y), (x + w, y), (x + w, y - h * 0.72), (x, y - h * 0.72)], 'sage', V, 'madder', 1.5)
    for row, (r0, r1) in enumerate(((0.0, 0.36), (0.40, 0.68))):
        n = 3 if row == 0 else 4
        for i in range(n):
            bw = w / n
            ax0, ax1 = x + i * bw + bw * 0.08, x + (i + 1) * bw - bw * 0.08
            ya, yb = y - h * r0 - (2 if row == 0 else 0), y - h * r1
            L.poly([(ax0, ya), (ax1, ya), (ax1, yb + h * 0.06), ((ax0 + ax1) / 2, yb), (ax0, yb + h * 0.06)], 'linen', V,
                   'madder', 1.1)
            if row == 0:                                                                    # a bed with a sleeper
                bx0, bx1 = ax0 + bw * 0.06, ax1 - bw * 0.06
                L.poly([(bx0, ya - h * 0.02), (bx1, ya - h * 0.02), (bx1, ya - h * 0.09), (bx0, ya - h * 0.09)],
                       'ochre', 0.0, 'madder', 1.0)
                L.line([(bx0, ya - h * 0.02), (bx0, ya - h * 0.15)], 'ochre', 1.6)
                L.poly([(bx0 + bw * 0.16, ya - h * 0.09), (bx1, ya - h * 0.09), (bx1 - bw * 0.04, ya - h * 0.16),
                        (bx0 + bw * 0.2, ya - h * 0.17)], ['bluegreen', 'terracotta', 'navy'][i], 0.0, 'madder', 1.0)
                L.ellipse(bx0 + bw * 0.1, ya - h * 0.14, h * 0.035, h * 0.03, 'buff', 0.0, 'madder', 1.0)
                L.line([(bx0 + bw * 0.13, ya - h * 0.15), (bx0 + bw * 0.115, ya - h * 0.145)], 'black', 0.8)
            else:
                flames(L, ax0 + bw * 0.05, yb + h * 0.22, ax1 - ax0 - bw * 0.1, h * 0.2, seed=i + 10)
    L.poly([(x - w * 0.04, y - h * 0.72), (x + w * 1.04, y - h * 0.72), (x + w * 0.5, y - h * 0.86)], 'terracotta', 0.0,
           'madder', 1.4)
    for ex in (x - w * 0.1, x + w * 1.0):
        L.poly([(ex, y), (ex + w * 0.1, y), (ex + w * 0.1, y - h * 0.9), (ex, y - h * 0.9)], 'ochre', V, 'madder', 1.2)
        L.poly([(ex - w * 0.02, y - h * 0.9), (ex + w * 0.12, y - h * 0.9), (ex + w * 0.05, y - h * 1.0)], 'bluegreen',
               0.0, 'madder', 1.0)
    flames(L, x - w * 0.02, y - h * 0.8, w * 1.04, h * 0.32, seed=4)


def gate(L, x, y, w, h):
    """Durham's town gate, broken open."""
    L.poly([(x, y), (x + w, y), (x + w, y - h), (x, y - h)], 'buff', V, 'madder', 1.4)
    L.poly([(x + w * 0.22, y), (x + w * 0.78, y), (x + w * 0.78, y - h * 0.55), (x + w * 0.5, y - h * 0.7),
            (x + w * 0.22, y - h * 0.55)], 'linen', V, 'madder', 1.2)
    L.poly([(x + w * 0.78, y), (x + w * 1.1, y - h * 0.08), (x + w * 1.1, y - h * 0.6), (x + w * 0.78, y - h * 0.55)],
           'madder', 0.3, 'black', 1.0)                                                        # the door, smashed open
    for i in range(4):
        L.poly([(x + i * w * 0.27, y - h), (x + i * w * 0.27 + w * 0.17, y - h),
                (x + i * w * 0.27 + w * 0.17, y - h * 1.12), (x + i * w * 0.27, y - h * 1.12)], 'buff', V, 'madder', 1.0)


def book(L, x, y, s):
    """The Domesday Book, open on a lectern."""
    L.poly([(x - s * 0.08, y), (x + s * 0.08, y), (x + s * 0.05, y - s * 0.7), (x - s * 0.05, y - s * 0.7)], 'ochre', V,
           'madder', 1.2)
    L.poly([(x - s * 0.55, y - s * 0.7), (x + s * 0.55, y - s * 0.7), (x + s * 0.6, y - s * 0.95),
            (x - s * 0.6, y - s * 0.95)], 'madder', 0.0, 'black', 1.2)
    L.poly([(x - s * 0.5, y - s * 0.74), (x - s * 0.02, y - s * 0.78), (x - s * 0.02, y - s * 1.25),
            (x - s * 0.52, y - s * 1.2)], 'linen', V, 'madder', 1.2)
    L.poly([(x + s * 0.5, y - s * 0.74), (x + s * 0.02, y - s * 0.78), (x + s * 0.02, y - s * 1.25),
            (x + s * 0.52, y - s * 1.2)], 'linen', V, 'madder', 1.2)
    for i in range(6):
        yy = y - s * (0.86 + i * 0.06)
        L.line([(x - s * 0.44, yy), (x - s * 0.08, yy - s * 0.02)], 'navy', 0.8)
        L.line([(x + s * 0.08, yy - s * 0.02), (x + s * 0.44, yy)], 'navy', 0.8)


def sheep(L, x, y, s):
    for i in range(7):
        L.ellipse(x + s * (0.12 * (i % 4) - 0.18), y - s * (0.42 + 0.12 * (i // 4)), s * 0.14, s * 0.12, 'linen', 0.0,
                  'madder', 1.0)
    L.ellipse(x, y - s * 0.45, s * 0.34, s * 0.18, 'linen', 0.0, 'madder', 1.0)
    L.ellipse(x + s * 0.38, y - s * 0.52, s * 0.1, s * 0.08, 'black', 0.0)
    for dx in (-0.2, -0.08, 0.12, 0.24):
        L.line([(x + s * dx, y - s * 0.3), (x + s * dx, y)], 'black', 1.2)


def ox(L, x, y, s):
    L.poly([(x - s * 0.5, y - s * 0.35), (x + s * 0.35, y - s * 0.4), (x + s * 0.45, y - s * 0.75),
            (x - s * 0.45, y - s * 0.78)], 'terracotta', 0.0, 'madder', 1.2)
    L.poly([(x + s * 0.4, y - s * 0.72), (x + s * 0.62, y - s * 0.66), (x + s * 0.64, y - s * 0.52),
            (x + s * 0.45, y - s * 0.5)], 'terracotta', 0.3, 'madder', 1.2)
    L.line([(x + s * 0.48, y - s * 0.72), (x + s * 0.44, y - s * 0.86)], 'buff', 1.3)
    L.line([(x + s * 0.56, y - s * 0.7), (x + s * 0.6, y - s * 0.84)], 'buff', 1.3)
    for dx in (-0.42, -0.3, 0.22, 0.34):
        L.line([(x + s * dx, y - s * 0.4), (x + s * dx, y)], 'madder', 2.0)
    L.line([(x - s * 0.48, y - s * 0.7), (x - s * 0.6, y - s * 0.4)], 'madder', 1.0)


def staple(L, x, y, s=7, ang=0.0):
    """A staple, stitched: a squared bracket in grey."""
    c, si = math.cos(ang), math.sin(ang)

    def R(u, v):
        return (x + u * c - v * si, y + u * si + v * c)
    L.line([R(0, -s * 0.5), R(-s * 0.5, -s * 0.5), R(-s * 0.5, s * 0.5), R(0, s * 0.5)], 'steel', 1.4)


def crown(L, x, y, w):
    L.poly([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y - w * 0.5), (x + w * 0.25, y - w * 0.25), (x, y - w * 0.55),
            (x - w * 0.25, y - w * 0.25), (x - w / 2, y - w * 0.5)], 'ochre', 0.0, 'madder', 1.2)
    for dx in (-0.25, 0.0, 0.25):
        L.ellipse(x + dx * w, y - w * 0.12, w * 0.06, w * 0.06, 'terracotta')


# -------------------------------------------------------------------------------------------- the scenes
W_REF = {'ch1': 1060, 'ch2': 920, 'ch3': 1090}
ANCHORS = {}            # per scene: moving sprites, gun muzzles, stapler mouths, fire (saved with the build)
FIRE_POINTS = {}        # where the trailer adds live flame over the stitched fire (reference pixels of each scene)
STAPLE_MOUTHS = []      # where the tax collectors' staplers point (ch3), for the flying staples


def ch1():
    """1066: William crowned at the abbey on Christmas Day; his guards set the Saxon houses alight."""
    sc = Scene(W_REF['ch1'])
    sc.draw(lambda L: abbey(L, 30, 280, 270, 180))
    def crowned(L, sh, to_scene):
        hx, hy = sh(*to_scene(258, 14))
        crown(L, hx, hy + 2, 22)
    sc.sprite('ch1', 'william', 'william', 262, 96, 0.40, crowned)
    a = sc.put('archer', 418, 102, 0.40)
    g = sc.put('ghostrider', 560, 112, 0.62)
    ANCHORS['ch1'].update(rifle=[a(577, 68)], pistol=[g(254, 43)])
    sc.draw(lambda L: [house(L, 812, 280, 70, 112, seed=1), house(L, 902, 280, 60, 96, roof='bluegreen', seed=2),
                       house(L, 980, 280, 62, 116, wall='buff', seed=3)])
    sc.draw(lambda L: [person(L, 1046, 281, 62, 'bluegreen', 'terracotta', arms='up'),
                       person(L, 790, 281, 56, 'terracotta', 'navy', facing=-1, arms='up')])
    sc.caption('HIC WILLELM REX CORONATVS EST: ET DOMVS ARDENT', 300, 74, 19)
    FIRE_POINTS['ch1'] = ANCHORS['ch1']['fire'] = [(847, 208), (932, 206), (1011, 196)]
    return sc


def ch2():
    """1069: rebels storm Durham; the bishop's palace burns with the Normans asleep in their beds; two escape."""
    sc = Scene(W_REF['ch2'])
    sc.put('clawrider', 20, 96, 1.0)
    sc.draw(lambda L: gate(L, 190, 280, 80, 150))
    g = sc.put('ghostrider', 250, 118, 0.58)
    ANCHORS['ch2'] = dict(pistol=[g(254, 43)], rifle=[])
    sc.draw(lambda L: palace(L, 470, 280, 280, 162))
    sc.draw(lambda L: [person(L, 830, 281, 46, 'navy', 'ochre', helmet='navy', pose='run'),
                       person(L, 890, 281, 46, 'terracotta', 'bluegreen', helmet='navy', pose='run')])
    sc.caption('VBI DVNELMVM ARDET: DVO SOLI EVASERVNT', 150, 74, 19)
    FIRE_POINTS['ch2'] = ANCHORS['ch2']['fire'] = [(520, 196), (590, 196), (660, 196), (730, 196), (610, 145)]
    return sc


def ch3():
    """1086: the Domesday survey. William points; the tax collectors fire staple after staple at everyone."""
    sc = Scene(W_REF['ch3'])
    sc.sprite('ch3', 'william', 'william', 10, 96, 0.40)
    sc.draw(lambda L: book(L, 245, 280, 70))
    mouths = []
    for i, xx in enumerate((300, 410, 520)):
        f = sc.sprite('ch3', f'collector{i}', 'collector', xx, 98 + (i % 2) * 6, 0.66)
        mouths.append(f(318, 158))
    sc.put('messenger', 712, 98, 0.66)
    sc.draw(lambda L: [person(L, 850, 281, 72, 'bluegreen', 'terracotta', facing=-1, arms='up'),
                       person(L, 1060, 281, 66, 'ochre', 'navy', facing=-1, arms='up'),
                       sheep(L, 920, 281, 60), ox(L, 990, 281, 74)])
    rng = np.random.default_rng(12)

    def staples(L):
        for _ in range(46):                                    # staples everywhere: in the air, stuck in everything
            staple(L, rng.uniform(640, 1080), rng.uniform(100, 270), rng.uniform(5, 8), rng.uniform(-0.3, 0.3))
    sc.draw(staples)
    sc.caption('HIC REX TOTAM ANGLIAM DESCRIBIT', 300, 74, 19)
    STAPLE_MOUTHS[:] = mouths
    ANCHORS['ch3'].update(mouths=mouths, rifle=[], pistol=[], fire=[])
    return sc


BUILDERS = {'ch1': ch1, 'ch2': ch2, 'ch3': ch3}


def build(names=None):
    os.makedirs(BW.CACHE, exist_ok=True)
    for name in names or BUILDERS:
        sc = BUILDERS[name]()
        img = Image.fromarray(BS.stitch(sc.lab, 3.0, sc.forced, seed=21))
        img.save(os.path.join(BW.CACHE, f'{name}-before.png'))
        img.save(os.path.join(BW.CACHE, f'{name}-after.png'))
        print('built', name, sc.lab.shape, flush=True)
    path = os.path.join(BW.CACHE, 'story-anchors.json')
    old = json.load(open(path)) if os.path.exists(path) else {}
    old.update({k: v for k, v in ANCHORS.items() if k in (names or BUILDERS)})
    json.dump(old, open(path, 'w'), indent=1)


if __name__ == '__main__':
    if sys.argv[1] == 'build':
        build(sys.argv[2:] or None)
    elif sys.argv[1] == 'check':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for name, fn in BUILDERS.items():
            sc = fn()
            Image.fromarray(BS.RGB[sc.lab].astype(np.uint8)).save(os.path.join(out, f'{name}-flat.png'))
