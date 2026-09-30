#!/usr/bin/env python3
"""Hope Again: a party conference that slowly, absurdly turns into a northern hall acclaiming its king.

Same deadpan look as Listening & Learning (ed.py): flat shapes, clean black outlines, almond eyes with
small pupils, soft painted shading, a still camera and hard cuts. Made vertical from the start
(1080 x 1920) and kept inside TikTok's safe area (x 60-900, y 310-1500).

Caricatures of real politicians for satire: drawn from a few key features (hair, glasses, face shape),
never traced. Costumes evoke a northern medieval hall; the only emblem is Manchester's worker bee.

Usage:
    python3 burnham.py stills OUT_DIR          one still per shot, for the storyboard
    python3 burnham.py sheet OUT_DIR SHEET.jpg  put those stills on one storyboard sheet
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ed import INK, curve, glow, oval, smooth, soft

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, SS = 1080, 1920, 2
SANS = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
ANTON = os.path.join(HERE, 'fonts', 'Anton-Regular.ttf')
CRANBERRY = (178, 24, 52)
OFFWHITE = (238, 234, 238)

# skin tones and colours
PALE = (246, 208, 188)
PINK = (240, 196, 178)
OLIVE = (226, 184, 150)
BROWN = (176, 120, 86)
DEEP = (120, 78, 56)
NAVY = (34, 40, 62)
CHARCOAL = (46, 46, 54)
FUR = (122, 104, 86)
FUR_D = (84, 70, 58)
FUR_L = (170, 150, 126)
STEEL = (120, 128, 140)
STEEL_D = (80, 86, 98)
LEATHER = (74, 52, 38)
CLOAK = (26, 24, 28)
GOLD = (222, 176, 60)


# ----------------------------------------------------------------------------------------------- camera

class Cam:
    """World units are output pixels (1080 x 1920) at zoom 1; (cx, cy) is the world point at frame centre."""
    def __init__(self, z=1.0, cx=W / 2, cy=H / 2):
        self.z, self.cx, self.cy, self.s = z, cx, cy, z

    def P(self, x, y):
        return ((x - self.cx) * self.z + W / 2) * SS, ((y - self.cy) * self.z + H / 2) * SS

    def S(self, v):
        return v * self.z * SS


class Local:
    """A person's own coordinates (neck base at 0, 0; head width about 150) placed into the world."""
    def __init__(self, cam, ox, oy, s, flip=1):
        self.cam, self.ox, self.oy, self.k, self.flip = cam, ox, oy, s, flip
        self.s = cam.s * s

    def P(self, x, y):
        return self.cam.P(self.ox + self.k * x * self.flip, self.oy + self.k * y)

    def S(self, v):
        return self.cam.S(v * self.k)


class Pen:
    """Flat fills with clean black outlines. Line widths grow more slowly than the drawing, so small
    people in a crowd keep readable outlines and close-ups do not get cartoon-heavy ones."""
    def __init__(self, img, cam):
        self.img, self.cam = img, cam
        self.d = ImageDraw.Draw(img)

    def w(self, lw):
        return max(1, int(round(lw * SS * 0.75 * max(0.25, self.cam.s) ** 0.6)))

    def poly(self, pts, fill, line=INK, lw=4):
        q = [self.cam.P(*p) for p in pts]
        if fill is not None:
            self.d.polygon(q, fill=fill)
        if line:
            self.d.line(q + [q[0]], fill=line, width=self.w(lw), joint='curve')

    def ell(self, cx, cy, rx, ry, fill, line=INK, lw=4, rot=0, n=40):
        pts = [(cx + rx * math.cos(a) * math.cos(rot) - ry * math.sin(a) * math.sin(rot),
                cy + rx * math.cos(a) * math.sin(rot) + ry * math.sin(a) * math.cos(rot))
               for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]
        self.poly(pts, fill, line, lw)

    def line(self, pts, colr=INK, lw=4):
        self.d.line([self.cam.P(*p) for p in pts], fill=colr, width=self.w(lw), joint='curve')


def canvas(colr=(0, 0, 0)):
    return Image.new('RGBA', (W * SS, H * SS), colr + (255,))


def gradient(img, cam, box, c_mid, c_edge, centre, radius, squash=1.0, dim=1.0):
    """A radial wash (the conference backdrop's magenta glow into deep red), filling a world box."""
    x0, y0 = cam.P(box[0], box[1])
    x1, y1 = cam.P(box[2], box[3])
    x0, y0, x1, y1 = [int(round(v)) for v in (x0, y0, x1, y1)]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(img.width, x1), min(img.height, y1)
    if x1 <= x0 or y1 <= y0:
        return
    X, Y = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1))
    CX, CY = cam.P(*centre)
    R = cam.S(radius)
    d = np.sqrt(((X - CX) / R) ** 2 + ((Y - CY) / (R * squash)) ** 2)
    k = np.clip(d, 0, 1)[..., None] ** 1.3
    a = (np.array(c_mid) * (1 - k) + np.array(c_edge) * k) * dim
    tile = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    img.alpha_composite(tile, (x0, y0))


def shade(img, alpha, colr=(0, 0, 0)):
    img.alpha_composite(Image.new('RGBA', img.size, colr + (int(255 * alpha),)))


def text(img, cam, x, y, s, size, fill, font=ANTON, anchor='la', widen=1.0, stroke=0, stroke_fill=INK):
    """Lettering in world units (backdrop slogans, banners)."""
    f = ImageFont.truetype(font, max(4, int(cam.S(size))))
    sw = int(cam.S(stroke))
    l, t, r, b = f.getbbox(s, stroke_width=sw)
    lay = Image.new('RGBA', (r - l + 4, b - t + 4), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((2 - l, 2 - t), s, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke_fill)
    if widen != 1.0:
        lay = lay.resize((int(lay.width * widen), lay.height), Image.LANCZOS)
    X, Y = cam.P(x, y)
    if anchor == 'ma':
        X -= lay.width / 2
    img.alpha_composite(lay, (int(X), int(Y)))
    return lay.width / (cam.z * SS), lay.height / (cam.z * SS)


# ---------------------------------------------------------------------------------------------- people

def bee(p, x, y, r):
    """Manchester's worker bee, as a brooch: a gold disc with a striped bee on it."""
    p.ell(x, y, r, r, GOLD, INK, 2.2)
    p.ell(x - r * 0.28, y - r * 0.18, r * 0.34, r * 0.22, (250, 250, 250), INK, 1.4, rot=-0.5)
    p.ell(x + r * 0.28, y - r * 0.18, r * 0.34, r * 0.22, (250, 250, 250), INK, 1.4, rot=0.5)
    p.ell(x, y + r * 0.12, r * 0.24, r * 0.46, (244, 196, 40), INK, 1.6)
    for k in (-1, 1):
        p.line([(x - r * 0.22, y + r * (0.12 + 0.2 * k)), (x + r * 0.22, y + r * (0.12 + 0.2 * k))], INK, 2.0)
    p.ell(x, y - r * 0.4, r * 0.14, r * 0.12, INK, None)


def dk(c, k=0.66):
    return tuple(int(v * k) for v in c)


def lt(c, k=1.25):
    return tuple(min(255, int(v * k)) for v in c)


def armour(**kw):
    """One knight's kit. Pieces: helmet (bascinet, sallet or kettle hat, visor raised so the face shows),
    gorget, breastplate, plackart, faulds, pauldrons or spaulders, rerebraces, couters, vambraces, gauntlets,
    and optionally a fur mantle over it all."""
    d = dict(steel=STEEL, helmet=None, gorget=True, pauldron='big', plackart=False, faulds=False,
             steel_arms=True, fans=True, gauntlets=True, mantle=False)
    d.update(kw)
    return d


def helmet(p, sp, hx, hy, hw, hh):
    a = sp['arm']
    kind, c = a['helmet'], a['steel']
    if kind in ('bascinet', 'sallet'):
        if kind == 'bascinet':  # a pointed skull, its cheeks down past the ears
            outer = [(hx - hw - 12, hy + 50), (hx - hw - 16, hy - 30), (hx - hw * 0.8, hy - hh * 1.05),
                     (hx, hy - hh * 1.55), (hx + hw * 0.8, hy - hh * 1.05), (hx + hw + 16, hy - 30), (hx + hw + 12, hy + 50)]
        else:  # a rounded sallet, its tail flaring out at the back of the neck
            outer = [(hx - hw - 36, hy + 58), (hx - hw - 14, hy + 10), (hx - hw - 10, hy - 40),
                     (hx - hw * 0.75, hy - hh * 1.08), (hx, hy - hh * 1.3), (hx + hw * 0.75, hy - hh * 1.08),
                     (hx + hw + 10, hy - 40), (hx + hw + 14, hy + 10), (hx + hw + 36, hy + 58)]
        inner = [(hx + hw - 4, hy + 44), (hx + hw - 2, hy - 24), (hx + hw * 0.55, hy - hh * 0.52), (hx, hy - hh * 0.58),
                 (hx - hw * 0.55, hy - hh * 0.52), (hx - hw + 2, hy - 24), (hx - hw + 4, hy + 44)]
        p.poly(curve(outer + inner, 4), c, INK, 2.8)
        soft(p.img, p.cam, [(hx - hw * 0.6, hy - hh * 1.0), (hx - hw * 0.2, hy - hh * 1.2), (hx - hw * 0.3, hy - hh * 0.7),
                            (hx - hw * 0.7, hy - hh * 0.6)], (255, 255, 255), 0.3, 6)
        # the visor, hinged up out of the way: a band over the brow with a sight slit and breaths
        top = oval(hx, hy - 34, hw + 10, hh * 0.98, 24, math.pi, 2 * math.pi)
        low = oval(hx, hy - 34, hw - 2, hh * 0.72, 24, 2 * math.pi, math.pi)
        p.poly(top + low, dk(c, 0.82), INK, 2.6)
        p.line(oval(hx, hy - 34, hw + 3, hh * 0.84, 20, math.pi * 1.15, math.pi * 1.85), INK, 3.0)
        for k in range(5):
            u = math.pi * (1.3 + 0.1 * k)
            p.ell(hx + (hw + 4) * 0.93 * math.cos(u), hy - 34 + hh * 0.93 * math.sin(u), 3, 3, INK, None)
        for sgn in (-1, 1):
            p.ell(hx + sgn * (hw + 6), hy - 32, 7, 7, lt(c), INK, 2.0)
    elif kind == 'kettle':  # a brimmed kettle hat
        p.poly(oval(hx, hy - hh * 0.62, hw * 0.98, hh * 0.64, 24, math.pi, 2 * math.pi), c, INK, 2.8)
        p.ell(hx, hy - hh * 0.6, hw * 1.55, hh * 0.17, lt(c, 1.1), INK, 2.8)
        p.line([(hx, hy - hh * 1.24), (hx, hy - hh * 0.72)], dk(c), 2.2)


def crown(p, hx, hy, hw, hh):
    """Our own crown: a bronze-gold circlet with upright points and a garnet at the front."""
    g, gd = (214, 166, 70), (150, 108, 40)
    top, bot = hy - hh * 0.86, hy - hh * 0.6
    w = hw * 1.06
    band = oval(hx, top, w, 12, 20, 0, math.pi) + oval(hx, bot, w, 14, 20, math.pi, 0)[::-1][::-1]
    pts = [(hx - w, bot), (hx - w, top)]
    n = 7
    for i in range(n):
        x0 = hx - w + 2 * w * i / n
        x1 = hx - w + 2 * w * (i + 1) / n
        h = 34 if i == n // 2 else 24
        pts += [(x0 + (x1 - x0) * 0.2, top - 2), ((x0 + x1) / 2, top - h), (x0 + (x1 - x0) * 0.8, top - 2)]
    pts += [(hx + w, top), (hx + w, bot)]
    pts += [(hx + w * 0.5, bot + 8), (hx, bot + 10), (hx - w * 0.5, bot + 8)]
    p.poly(pts, g, INK, 2.6)
    p.line([(hx - w, (top + bot) / 2), (hx - w * 0.5, (top + bot) / 2 + 6), (hx, (top + bot) / 2 + 7),
            (hx + w * 0.5, (top + bot) / 2 + 6), (hx + w, (top + bot) / 2)], gd, 2.0)
    for i in range(n):
        x = hx - w + 2 * w * (i + 0.5) / n
        p.ell(x, top - 6, 3, 3, (250, 230, 160), None)
    p.ell(hx, (top + bot) / 2 + 2, 9, 11, (150, 20, 40), INK, 2.0)


def gorget(p, c):
    """A steel collar of three overlapping lames round the neck."""
    for k in range(3):
        y, w = 34 - 26 * k, 80 - 11 * k
        p.poly([(-w, y), (w, y), (w - 9, y - 30), (-w + 9, y - 30)], c if k % 2 == 0 else lt(c, 1.12), INK, 2.4)


def pauldrons(p, a, sw):
    """Curved plates capping each shoulder: one dome with its lames scored across it (big pauldrons reach
    further down the arm and in over the chest; spaulders are small)."""
    c = a['steel']
    big = a['pauldron'] == 'big'
    rx, ry = (80, 70) if big else (58, 50)
    for sgn in (-1, 1):
        cx, cy = sgn * (sw - 10), 58 if big else 50
        dome = oval(cx, cy, rx, ry, 28, math.pi, 2 * math.pi)
        edge = [(cx + rx, cy), (cx + rx * 0.9, cy + 26), (cx + rx * 0.3, cy + 34), (cx - rx * 0.3, cy + 30),
                (cx - rx * 0.9, cy + 18), (cx - rx, cy)]
        p.poly(dome + edge[1:-1], c, INK, 2.6)
        for k in range(1, 3 if big else 2):  # the overlapping lames
            p.line(oval(cx, cy + 4, rx * (1 - 0.0 * k), ry * (1 - 0.34 * k), 20, math.pi * 1.02, math.pi * 1.98), INK, 2.0)
        p.poly(oval(cx - sgn * rx * 0.25, cy - ry * 0.7, rx * 0.28, ry * 0.12, 12), lt(c, 1.35), None)
        p.ell(cx, cy - ry + 12, 5, 5, lt(c, 1.3), INK, 1.6)


def steel_arm(p, sh, el, wr, c, w=32, fan=True):
    """A plate arm: rerebrace, a couter at the elbow (with a fan-shaped wing), a vambrace."""
    if fan:
        sx = 1 if el[0] >= sh[0] else -1
        p.poly([(el[0], el[1] - w * 0.6), (el[0] + sx * w * 1.7, el[1] - w * 0.3), (el[0] + sx * w * 1.5, el[1] + w * 0.8),
                (el[0], el[1] + w * 0.6)], dk(c, 0.85), INK, 2.2)
    arm(p, sh, el, wr, c, w)
    for (a, b, u) in ((sh, el, 0.5), (el, wr, 0.45), (el, wr, 0.8)):
        mx, my = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n * w * 0.85, dx / n * w * 0.85
        p.line([(mx + nx, my + ny), (mx - nx, my - ny)], INK, 2.0)
    p.ell(el[0], el[1], w * 1.0, w * 0.95, lt(c, 1.12), INK, 2.4)


def head_outline(hx, hy, hw, hh, jaw):
    top = oval(hx, hy - 6, hw, hh, 40, math.pi, 2 * math.pi)
    j = {'square': (0.95, 0.62, 1.02), 'round': (0.98, 0.72, 0.96), 'long': (0.9, 0.5, 1.12),
         'soft': (0.9, 0.56, 1.0)}[jaw]
    return top + [(hx + hw, hy + 10), (hx + hw * j[0], hy + hh * 0.66), (hx + hw * j[1], hy + hh * 1.02 * j[2]),
                  (hx, hy + hh * 1.14 * j[2]), (hx - hw * j[1], hy + hh * 1.02 * j[2]),
                  (hx - hw * j[0], hy + hh * 0.66), (hx - hw, hy + 10)]


def hair_back(p, sp, hx, hy, hw, hh):
    st, c = sp.get('hair'), sp.get('hair_c', (60, 44, 34))
    if st == 'long':  # straight, past the shoulders, behind the head
        p.poly(curve([(hx - hw - 14, hy - 40), (hx - hw - 20, hy + 100), (hx - hw - 18, hy + 160),
                      (hx + hw + 18, hy + 160), (hx + hw + 20, hy + 100), (hx + hw + 14, hy - 40),
                      (hx, hy - hh - 10)], 5), c, INK, 2.6)
    elif st == 'bob':  # to the jaw, flicking out
        p.poly(curve([(hx - hw - 18, hy - 30), (hx - hw - 26, hy + 70), (hx - hw - 10, hy + 118),
                      (hx + hw + 10, hy + 118), (hx + hw + 26, hy + 70), (hx + hw + 18, hy - 30),
                      (hx, hy - hh - 14)], 5), c, INK, 2.6)
    elif st == 'blonde':  # long, loose, over one shoulder
        p.poly(curve([(hx - hw - 12, hy - 40), (hx - hw - 20, hy + 150), (hx - hw - 6, hy + 270),
                      (hx + hw + 36, hy + 270), (hx + hw + 26, hy + 120), (hx + hw + 14, hy - 40),
                      (hx, hy - hh - 10)], 5), c, INK, 2.6)


def hair_front(p, sp, hx, hy, hw, hh, fx):
    st = sp.get('hair')
    c = sp.get('hair_c', (60, 44, 34))
    cd = tuple(int(v * 0.72) for v in c)
    if st in ('side', 'swept'):
        vol = 1.0 if st == 'side' else 1.12
        hair = [(hx - hw, hy - 12), (hx - hw - 2, hy - 54), (hx - hw * 0.76, hy - hh * 0.98 * vol),
                (hx - 10, hy - hh * 1.16 * vol), (hx + hw * 0.55, hy - hh * 1.12 * vol),
                (hx + hw, hy - hh * 0.8), (hx + hw + 2, hy - 16), (hx + hw * 0.86, hy - 44),
                (hx + hw * 0.5, hy - hh * 0.72), (fx - hw * 0.35, hy - hh * 0.8), (hx - hw * 0.72, hy - hh * 0.52),
                (hx - hw * 0.9, hy - 30)]
        p.poly(curve(hair), c, INK, 2.6)
        # the side parting and a few combed strands
        p.line([(fx - hw * 0.34, hy - hh * 0.82), (fx - hw * 0.22, hy - hh * 1.1 * vol)], cd, 2.2)
        for k in range(4):
            a = fx - hw * 0.1 + 22 * k
            p.line([(a, hy - hh * 1.06 * vol + 4 * k), (a + 20, hy - hh * 0.84 + 3 * k)], cd, 1.8)
        if sp.get('grey'):  # grey at the temples
            for sgn in (-1, 1):
                p.line([(hx + sgn * (hw - 3), hy - 14), (hx + sgn * (hw - 2), hy - 48)], sp['grey'], 3.0)
    elif st == 'crop':  # very short, close to the head
        hair = [(hx - hw, hy - 18), (hx - hw * 0.94, hy - hh * 0.7), (hx - hw * 0.5, hy - hh * 1.0),
                (hx + hw * 0.5, hy - hh * 1.0), (hx + hw * 0.94, hy - hh * 0.7), (hx + hw, hy - 18),
                (hx + hw * 0.9, hy - 36), (hx + hw * 0.6, hy - hh * 0.72), (hx, hy - hh * 0.8),
                (hx - hw * 0.6, hy - hh * 0.72), (hx - hw * 0.9, hy - 36)]
        p.poly(curve(hair), c, INK, 2.4)
    elif st == 'bald':  # a band round the back and sides, a shiny crown
        for sgn in (-1, 1):
            p.poly(curve([(hx + sgn * hw, hy + 14), (hx + sgn * (hw + 4), hy - 40), (hx + sgn * hw * 0.8, hy - hh * 0.7),
                          (hx + sgn * hw * 0.7, hy - hh * 0.6), (hx + sgn * (hw - 12), hy - 30),
                          (hx + sgn * (hw - 10), hy + 10)], 4), c, INK, 2.2)
        p.ell(hx + hw * 0.25, hy - hh * 0.72, hw * 0.22, hh * 0.08, (255, 240, 230), None, rot=0.2)
    elif st == 'wisps':  # an old man's thin white hair round a bald crown
        for sgn in (-1, 1):
            p.poly(curve([(hx + sgn * (hw + 2), hy + 10), (hx + sgn * (hw + 16), hy - 36),
                          (hx + sgn * (hw + 4), hy - hh * 0.72), (hx + sgn * (hw - 10), hy - 40),
                          (hx + sgn * (hw - 6), hy + 4)], 4), c, INK, 2.0)
        p.line([(hx - 20, hy - hh * 1.02), (hx - 6, hy - hh * 1.2), (hx + 8, hy - hh * 1.04)], INK, 1.6)
        p.ell(hx + hw * 0.2, hy - hh * 0.74, hw * 0.24, hh * 0.08, (255, 238, 228), None, rot=0.2)
    elif st in ('long', 'bob', 'blonde'):  # the fringe and top of longer hair
        part = fx - hw * 0.1 if st != 'blonde' else fx + hw * 0.25
        hair = [(hx - hw - 6, hy + 30), (hx - hw - 8, hy - 50), (hx - hw * 0.7, hy - hh * 1.02),
                (part, hy - hh * 1.16), (hx + hw * 0.7, hy - hh * 1.02), (hx + hw + 8, hy - 50),
                (hx + hw + 6, hy + 30), (hx + hw * 0.86, hy - 20), (part + hw * 0.5, hy - hh * 0.66),
                (part, hy - hh * 0.86), (part - hw * 0.62, hy - hh * 0.5), (hx - hw * 0.86, hy - 20)]
        if st == 'bob':  # a swept fringe
            hair[9] = (part - hw * 0.1, hy - hh * 0.62)
            hair[10] = (part - hw * 0.62, hy - hh * 0.36)
        p.poly(curve(hair), c, INK, 2.6)
        p.line([(part, hy - hh * 1.14), (part + 4, hy - hh * 0.9)], cd, 2.0)
        for k in range(3):
            p.line([(hx - hw * 0.6 + 18 * k, hy - hh * 0.8), (hx - hw * 0.8 + 10 * k, hy - 10)], cd, 1.6)
            p.line([(hx + hw * 0.6 - 18 * k, hy - hh * 0.8), (hx + hw * 0.8 - 10 * k, hy - 10)], cd, 1.6)
    elif st == 'turban':
        tc = sp.get('turban_c', (38, 48, 92))
        td = tuple(int(v * 0.7) for v in tc)
        tb = [(hx - hw - 10, hy - 22), (hx - hw - 14, hy - 80), (hx - hw * 0.72, hy - hh * 1.28),
              (hx, hy - hh * 1.5), (hx + hw * 0.72, hy - hh * 1.3), (hx + hw + 14, hy - 80), (hx + hw + 10, hy - 22),
              (hx + hw * 0.5, hy - 44), (hx, hy - 60), (hx - hw * 0.5, hy - 44)]
        p.poly(curve(tb, 5), tc, INK, 2.6)
        for k in range(3):  # the folds crossing in a V at the front
            p.line([(hx - hw - 6 + 8 * k, hy - 40 - 30 * k), (fx, hy - 70 - 26 * k),
                    (hx + hw + 6 - 8 * k, hy - 40 - 30 * k)], td, 2.2)


def beard(p, sp, hx, hy, hw, hh, fx):
    st = sp.get('beard')
    if not st:
        return
    c = sp.get('beard_c', sp.get('hair_c', (60, 44, 34)))
    if st in ('full', 'white'):
        long = 1.5 if st == 'white' else 1.3
        pts = [(hx - hw - 1, hy - 4), (hx - hw * 0.96, hy + hh * 0.7), (hx - hw * 0.6, hy + hh * 1.2 * long),
               (fx, hy + hh * 1.38 * long), (hx + hw * 0.6, hy + hh * 1.2 * long), (hx + hw * 0.96, hy + hh * 0.7),
               (hx + hw + 1, hy - 4), (hx + hw * 0.7, hy + 30), (fx + 30, hy + 36), (fx, hy + 30),
               (fx - 30, hy + 36), (hx - hw * 0.7, hy + 30)]
        p.poly(curve(pts, 5), c, INK, 2.6)
        cd = tuple(int(v * 0.8) for v in c)
        for k in range(5):
            x = fx - 40 + 20 * k
            p.line([(x, hy + hh * 0.9), (x + 3, hy + hh * 1.15 * long)], cd, 1.6)
        if sp.get('beard_grey'):
            for k in range(4):
                x = fx - 34 + 22 * k
                p.line([(x, hy + hh * 0.95), (x - 2, hy + hh * 1.2 * long)], sp['beard_grey'], 2.0)
    elif st == 'stubble':
        rng = np.random.default_rng(5)
        for _ in range(70):
            a = rng.uniform(0.3, math.pi - 0.3)
            r = rng.uniform(0.6, 0.95)
            sx, sy = fx + hw * 0.86 * r * math.cos(a), hy + 30 + hh * 0.72 * r * math.sin(a)
            p.ell(sx, sy, 0.9, 0.9, sp.get('beard_c', (90, 70, 60)), None)


def mouth_by_level(base, lv, i=0):
    """Pick a mouth shape from how loud the voice is right now: shut, then opening, then the full shout."""
    if lv < 0.1:
        return 'line'
    if lv < 0.3:
        return 'small'
    if lv < 0.6:
        return ['mid', 'open'][i % 2]
    return base


def mouth(p, sp, t, fx, my):
    m = sp.get('mouth', 'line')
    if m == 'talk':
        m = ['mid', 'small', 'open', 'small', 'mid', 'line'][int(t * 11) % 6]
    if m == 'line':
        p.line([(fx - 16, my + 2), (fx, my), (fx + 16, my + 3)], INK, 2.4)
    elif m == 'set':  # stoic: flat, the corners down a touch
        p.line([(fx - 20, my + 5), (fx - 8, my), (fx + 8, my), (fx + 20, my + 5)], INK, 2.6)
    elif m == 'smile':
        p.line([(fx - 20, my - 4), (fx - 8, my + 5), (fx + 8, my + 5), (fx + 20, my - 4)], INK, 2.4)
    elif m == 'grin':
        p.poly([(fx - 24, my - 4), (fx + 24, my - 4), (fx + 14, my + 12), (fx - 14, my + 12)], (250, 250, 246), INK, 2.2)
    elif m in ('small', 'mid', 'open'):
        h = {'small': 7, 'mid': 13, 'open': 18}[m]
        w = {'small': 15, 'mid': 17, 'open': 14}[m]
        p.poly([(fx - w, my - 2), (fx + w, my - 3), (fx + w * 0.7, my + h), (fx - w * 0.7, my + h)], (70, 26, 30), INK, 2.2)
        if m != 'small':
            p.poly([(fx - w * 0.8, my - 1), (fx + w * 0.8, my - 2), (fx + w * 0.7, my + 3), (fx - w * 0.7, my + 3)],
                   (245, 245, 240), None)
    elif m == 'cheer':  # a delighted roar: wide, corners up
        pts = curve([(fx - 36, my - 12), (fx, my - 6), (fx + 36, my - 12), (fx + 26, my + 22), (fx, my + 36),
                     (fx - 26, my + 22)], 4)
        p.poly(pts, (80, 24, 30), INK, 2.6)
        p.poly([(fx - 28, my - 9), (fx + 28, my - 9), (fx + 22, my), (fx - 22, my)], (248, 248, 242), None)
        p.ell(fx, my + 26, 14, 7, (196, 90, 96), None)
    elif m == 'shout':  # a bellow: wide open, top teeth, tongue
        pts = curve([(fx - 30, my - 8), (fx, my - 12), (fx + 30, my - 8), (fx + 24, my + 26), (fx, my + 40),
                     (fx - 24, my + 26)], 4)
        p.poly(pts, (80, 24, 30), INK, 2.6)
        p.poly([(fx - 24, my - 6), (fx + 24, my - 6), (fx + 20, my + 2), (fx - 20, my + 2)], (248, 248, 242), None)
        p.ell(fx, my + 30, 14, 7, (196, 90, 96), None)


def face(img, p, sp, t, hx, hy, hw, hh):
    turn = sp.get('turn', 0.0)  # -1 turned to our left, +1 to our right
    fx = hx + turn * hw * 0.22
    look = sp.get('look', turn)
    skin = sp['skin']
    skin_d = tuple(int(v * 0.88) for v in skin)
    if sp.get('age'):  # lines under the eyes and round the mouth
        for sgn in (-1, 1):
            ex = fx - 8 + sgn * 30
            p.line([(ex - 12, hy + 8), (ex, hy + 12), (ex + 12, hy + 8)], skin_d, 1.8)
            p.line([(fx + sgn * 26, hy + 34), (fx + sgn * 36, hy + 62)], skin_d, 1.8)
    for k in range(sp.get('creases', 0)):
        p.line([(fx - 30, hy - 44 + 9 * k), (fx - 6, hy - 48 + 9 * k), (fx + 24, hy - 45 + 9 * k)], skin_d, 1.8)
    blink = sp.get('blink', False)
    lid = sp.get('lid', 0)
    bc = sp.get('brow_c', tuple(int(v * 0.8) for v in sp.get('hair_c', (60, 44, 34))))
    for sgn in (-1, 1):
        ex, ey = fx - 4 + sgn * 30, hy - 8
        if blink:
            p.line([(ex - 16, ey), (ex, ey + 3), (ex + 16, ey)], INK, 2.4)
        else:
            almond = [(ex - 17, ey), (ex - 8, ey - 8), (ex + 8, ey - 8), (ex + 17, ey), (ex + 8, ey + 7), (ex - 8, ey + 7)]
            p.poly(almond, (250, 250, 248), INK, 2.0)
            p.ell(ex + look * 7, ey + 1, 4.5, 4.5, INK, None)
            p.line([(ex - 17, ey - 1 + lid), (ex - 8, ey - 9 + lid), (ex + 8, ey - 9 + lid), (ex + 17, ey - 1 + lid)],
                   INK, 2.6)
        raise_ = sp.get('brow_raise', 0)
        bw = sp.get('brow_w', 3.2)
        br = sp.get('brows')
        if br == 'fierce':  # inner ends pulled down: a serious, fierce bellow
            p.line([(ex - sgn * 6, ey - 12), (ex + sgn * 8, ey - 20), (ex + sgn * 22, ey - 26)], bc, bw * 1.2)
        elif br == 'joy':  # high and arched, the eyes creased with delight
            p.line([(ex - sgn * 8, ey - 26), (ex + sgn * 6, ey - 34), (ex + sgn * 20, ey - 28)], bc, bw)
            if not blink:
                p.line([(ex - 15, ey + 7), (ex, ey + 3), (ex + 15, ey + 7)], INK, 2.0)
        else:
            p.line([(ex - sgn * 4 - sgn * 2, ey - 22 - raise_), (ex + sgn * 20, ey - 20 - raise_ * 0.3)], bc, bw)
    if sp.get('glasses'):  # dark rectangular frames
        gc = sp.get('glasses_c', (30, 28, 34))
        for sgn in (-1, 1):
            ex = fx - 4 + sgn * 30
            p.poly([(ex - 25, hy - 24), (ex + 25, hy - 24), (ex + 23, hy + 8), (ex - 23, hy + 8)], None, gc, 4.2)
        p.line([(fx - 9, hy - 18), (fx - 4, hy - 21), (fx + 1, hy - 18)], gc, 3.6)
        for sgn in (-1, 1):
            p.line([(fx - 4 + sgn * 55, hy - 20), (hx + sgn * (hw + 2), hy - 16)], gc, 3.0)
    nose = sp.get('nose', 'line')
    if nose == 'long':
        p.line([(fx - 2, hy - 8), (fx - 14, hy + 34), (fx - 6, hy + 42), (fx + 8, hy + 38)], INK, 2.0)
        p.line([(fx - 18, hy + 38), (fx - 13, hy + 42)], INK, 1.6)
    else:
        p.line([(fx - 2, hy - 4), (fx - 10, hy + 26), (fx - 4, hy + 32), (fx + 7, hy + 30)], INK, 2.0)
        p.line([(fx - 14, hy + 30), (fx - 10, hy + 33)], INK, 1.6)
    if sp.get('blush'):
        for sgn in (-1, 1):
            p.ell(fx + sgn * 40, hy + 30, 14, 8, (236, 150, 140), None)
    return fx


def head(img, p, sp, t, hx, hy):
    hw, hh = sp.get('hw', 72), sp.get('hh', 88)
    skin = sp['skin']
    turn = sp.get('turn', 0.0)
    for sgn in (-1, 1):  # ears, pushed round by a turn
        p.poly(oval(hx + sgn * (hw + 2) - turn * 6, hy + 6, 12, 22), skin, INK, 2.4)
    p.poly(head_outline(hx, hy, hw, hh, sp.get('jaw', 'square')), skin, INK, 2.6)
    soft(img, p.cam, [(hx + hw * 0.4, hy - hh * 0.7), (hx + hw, hy - 10), (hx + hw * 0.9, hy + hh * 0.66),
                      (hx + hw * 0.5, hy + hh), (hx + hw * 0.4, hy + 30)], (160, 100, 90), 0.22, 8)
    fx = face(img, p, sp, t, hx, hy, hw, hh)
    beard(p, sp, hx, hy, hw, hh, fx)
    mouth(p, sp, t, fx, hy + sp.get('mouth_y', 60))
    hair_front(p, sp, hx, hy, hw, hh, fx)
    if sp.get('arm', {}).get('helmet'):
        helmet(p, sp, hx, hy, hw, hh)
    if sp.get('crown'):
        crown(p, hx, hy, hw, hh)
    if sp.get('earring'):
        p.ell(hx - hw - 2, hy + 30, 4, 4, GOLD, INK, 1.2)


def hand(p, x, y, skin, r=19, rot=0.0):
    p.ell(x, y, r, r * 0.86, skin, INK, 2.4, rot=rot)


def arm(p, sh, el, wr, sleeve, w=30):
    """A sleeve from shoulder to elbow to wrist, drawn as two tapered pieces and a round elbow."""
    def piece(a, b, wa, wb):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        return [(a[0] + nx * wa, a[1] + ny * wa), (b[0] + nx * wb, b[1] + ny * wb),
                (b[0] - nx * wb, b[1] - ny * wb), (a[0] - nx * wa, a[1] - ny * wa)]
    p.poly(piece(sh, el, w, w * 0.9), sleeve, INK, 2.6)
    p.ell(el[0], el[1], w * 0.9, w * 0.9, sleeve, INK, 2.6)
    p.poly(piece(el, wr, w * 0.9, w * 0.72), sleeve, None)
    p.line(piece(el, wr, w * 0.9, w * 0.72)[:2], INK, 2.6)
    p.line(piece(el, wr, w * 0.9, w * 0.72)[2:], INK, 2.6)
    p.line([piece(el, wr, w * 0.9, w * 0.72)[1], piece(el, wr, w * 0.9, w * 0.72)[2]], INK, 2.6)


def sword(p, hx, hy, ang=-1.5, length=520):
    """A plain longsword held upright: steel blade, dark cross-guard, leather grip."""
    ca, sa = math.cos(ang), math.sin(ang)
    tip = (hx + ca * length, hy + sa * length)
    nx, ny = -sa, ca
    base = (hx + ca * 30, hy + sa * 30)
    p.poly([(base[0] + nx * 11, base[1] + ny * 11), (tip[0] + nx * 3, tip[1] + ny * 3), (tip[0] + ca * 16, tip[1] + sa * 16),
            (tip[0] - nx * 3, tip[1] - ny * 3), (base[0] - nx * 11, base[1] - ny * 11)], (206, 212, 222), INK, 2.4)
    p.line([(base[0], base[1]), (tip[0], tip[1])], (150, 158, 170), 1.8)
    p.poly([(base[0] + nx * 40, base[1] + ny * 40), (base[0] + nx * 40 + ca * 10, base[1] + ny * 40 + sa * 10),
            (base[0] - nx * 40 + ca * 10, base[1] - ny * 40 + sa * 10), (base[0] - nx * 40, base[1] - ny * 40)],
           (60, 54, 50), INK, 2.2)
    p.ell(hx - ca * 36, hy - sa * 36, 9, 9, (60, 54, 50), INK, 2.0)


def fur_mantle(p, cx, top, half, depth, c=FUR, cd=FUR_D, cl=FUR_L, seed=1):
    """A heavy fur collar over the shoulders, its lower edge in soft tufts."""
    rng = np.random.default_rng(seed)
    pts = [(cx - half * 0.42, top - 40), (cx - half * 0.2, top - 58), (cx + half * 0.2, top - 58), (cx + half * 0.42, top - 40)]
    n = 14
    rim = []
    for i in range(n + 1):
        u = i / n
        x = cx + half * (1 - 2 * u)
        y = top + depth * (0.55 + 0.45 * math.sin(math.pi * u)) + rng.uniform(-8, 8)
        rim.append((x, y))
        if i < n:
            rim.append((x - half / n, y + 18 + rng.uniform(-4, 6)))
    edge = [(cx + half + 14, top + 30)] + rim + [(cx - half - 14, top + 30)]
    p.poly(pts + [(cx + half * 0.9, top - 10)] + edge[::-1][::-1] + [(cx - half * 0.9, top - 10)], c, INK, 2.6)
    for i in range(18):
        x = cx + rng.uniform(-half * 0.9, half * 0.9)
        y = top + rng.uniform(-30, depth * 0.6)
        p.line([(x, y), (x + rng.uniform(-8, 8), y + rng.uniform(12, 22))], cd if i % 2 else cl, 2.0)


def torso(img, p, sp, t):
    out = sp.get('outfit', 'suit')
    skin = sp['skin']
    bottom = sp.get('bottom', 560)
    sw = sp.get('shoulders', 150)
    if out in ('armour', 'king'):  # a dark cloak falling behind the shoulders
        p.poly([(-sw - 20, 20), (sw + 20, 20), (sw + 60, bottom + 40), (-sw - 60, bottom + 40)], CLOAK, INK, 2.6)
    # neck
    p.poly([(-32, -80), (32, -80), (36, 10), (-36, 10)], skin, INK, 2.6)
    soft(img, p.cam, [(-32, -76), (32, -76), (30, -40), (-30, -40)], (150, 90, 80), 0.35, 4)
    body = [(-40, -4), (-sw * 0.8, 12), (-sw, 50), (-sw - 6, 200), (-sw + 6, bottom), (sw - 6, bottom),
            (sw + 6, 200), (sw, 50), (sw * 0.8, 12), (40, -4)]
    if out == 'suit':
        jc = sp.get('jacket', NAVY)
        sc = sp.get('shirt', (236, 238, 244))
        p.poly(body, jc, INK, 2.6)
        p.poly([(-40, -4), (40, -4), (22, 150), (0, 230), (-22, 150)], sc, INK, 2.2)
        if sp.get('tie'):
            p.poly([(-11, 16), (11, 16), (15, 180), (0, 210), (-15, 180)], sp['tie'], INK, 2.0)
            p.poly([(-12, -2), (12, -2), (9, 18), (-9, 18)], sp['tie'], INK, 2.0)
        else:  # open collar
            p.poly([(-40, -4), (-8, 40), (-20, 54), (-46, 6)], sc, INK, 2.0)
            p.poly([(40, -4), (8, 40), (20, 54), (46, 6)], sc, INK, 2.0)
            p.poly([(-8, 40), (8, 40), (0, 64)], skin, None)
        jd = tuple(int(v * 0.72) for v in jc)
        for sgn in (-1, 1):  # lapels
            p.poly([(sgn * 44, -2), (sgn * 70, 30), (sgn * 46, 110), (sgn * 62, 150), (sgn * 4, 250), (sgn * 22, 150)],
                   jc, INK, 2.2)
        p.line([(0, 250), (0, bottom)], jd, 2.2)
        p.ell(6, 300, 5, 5, jd, None)
        soft(img, p.cam, [(sw * 0.4, 30), (sw, 60), (sw, bottom), (sw * 0.5, bottom)], (0, 0, 0), 0.25, 10)
    elif out == 'dress':
        dc = sp.get('dress', (190, 30, 44))
        p.poly(body, dc, INK, 2.6)
        p.poly([(-46, -4), (46, -4), (30, 50), (0, 70), (-30, 50)], skin, INK, 2.2)
        soft(img, p.cam, [(sw * 0.4, 30), (sw, 60), (sw, bottom), (sw * 0.5, bottom)], (0, 0, 0), 0.22, 10)
    elif out == 'blouse':  # a dark jacket over a pale top
        jc = sp.get('jacket', CHARCOAL)
        p.poly(body, jc, INK, 2.6)
        p.poly([(-50, -4), (50, -4), (34, 180), (-34, 180)], sp.get('shirt', (236, 232, 228)), INK, 2.0)
        soft(img, p.cam, [(sw * 0.4, 30), (sw, 60), (sw, bottom), (sw * 0.5, bottom)], (0, 0, 0), 0.25, 10)
    elif out == 'jumper':
        jc = sp.get('jacket', (90, 110, 140))
        p.poly(body, jc, INK, 2.6)
        p.line(oval(0, -2, 46, 22, 24, 0.2, math.pi - 0.2), INK, 2.4)
        soft(img, p.cam, [(sw * 0.4, 30), (sw, 60), (sw, bottom), (sw * 0.5, bottom)], (0, 0, 0), 0.22, 10)
    elif out in ('armour', 'king'):
        a = sp.get('arm') or armour()
        c = a['steel']
        if out == 'armour':  # a leather jerkin under the plate
            p.poly(body, LEATHER, INK, 2.6)
            pb = min(bottom - 20, 430)
            if a['faulds']:  # overlapping bands flaring out below the breastplate
                for k in range(3):
                    y0, w = pb + 6 + 34 * k, sw * 0.62 + 12 * k
                    p.poly([(-w, y0), (w, y0), (w + 12, y0 + 36), (-w - 12, y0 + 36)], c if k % 2 == 0 else lt(c, 1.1),
                           INK, 2.4)
            plate = curve([(-sw * 0.72, 70), (0, 50), (sw * 0.72, 70), (sw * 0.8, 260), (sw * 0.56, pb),
                           (-sw * 0.56, pb), (-sw * 0.8, 260)], 5)
            p.poly(plate, c, INK, 2.6)
            p.line([(0, 60), (0, pb - 12)], dk(c), 2.2)
            soft(img, p.cam, [(-sw * 0.5, 90), (-sw * 0.2, 80), (-sw * 0.3, 300), (-sw * 0.6, 260)], (255, 255, 255), 0.25, 8)
            for sgn in (-1, 1):
                for k in range(3):
                    p.ell(sgn * sw * 0.66, 120 + 70 * k, 4, 4, lt(c, 1.4), INK, 1.2)
            if a['plackart']:  # a second plate over the lower breastplate
                p.poly(curve([(-sw * 0.6, pb - 16), (-sw * 0.64, 320), (0, 236), (sw * 0.64, 320), (sw * 0.6, pb - 16)], 3),
                       lt(c, 1.08), INK, 2.4)
                p.line([(0, 250), (0, pb - 20)], dk(c), 2.0)
            p.poly([(-sw * 0.84, pb - 20), (sw * 0.84, pb - 20), (sw * 0.84, pb + 12), (-sw * 0.84, pb + 12)], LEATHER, INK, 2.2)
            p.ell(0, pb - 4, 16, 14, (190, 160, 90), INK, 2)
        else:  # the king: black leather studded in silver under a dark steel breastplate edged in gold
            p.poly(body, (26, 24, 28), INK, 2.6)
            plate = curve([(-sw * 0.74, 90), (0, 70), (sw * 0.74, 90), (sw * 0.8, 300), (sw * 0.56, 470),
                           (-sw * 0.56, 470), (-sw * 0.8, 300)], 5)
            p.poly(plate, (60, 62, 74), GOLD, 3.4)
            p.line([(0, 90), (0, 460)], (40, 42, 52), 2.4)
            soft(img, p.cam, [(-sw * 0.5, 110), (-sw * 0.2, 100), (-sw * 0.3, 320), (-sw * 0.6, 280)], (255, 255, 255), 0.18, 8)
            for sgn in (-1, 1):
                for k in range(6):
                    p.ell(sgn * sw * 0.9, 130 + 60 * k, 4, 4, (200, 204, 212), INK, 1.2)
        if out == 'king':  # a great dark fur over both shoulders, a gold chain and the bee medallion
            fur_mantle(p, 0, 16, sw + 50, 176, c=(66, 58, 54), cd=(34, 30, 30), cl=(150, 138, 124), seed=7)
            links = [(sw * 0.66 * math.cos(u), 60 + 150 * math.sin(u)) for u in np.linspace(0.15, math.pi - 0.15, 22)]
            for (x, y) in links:
                p.ell(x, y, 9, 6, GOLD, INK, 1.4)
            bee(p, 0, 226, 32)
        elif a['mantle']:
            if a['gorget'] and out == 'armour':
                gorget(p, c)
            fur_mantle(p, 0, 24, sw + 24, 120, seed=sp.get('seed', 1))
            bee(p, 0, 80, 20)
        else:
            if a['gorget']:
                gorget(p, c)
            bee(p, -sw * 0.36, 130, 20)
    if sp.get('lanyard'):  # the conference pass, still round the neck
        lc = sp.get('lanyard_c', (196, 26, 52))
        p.line([(-34, 0), (-16, 200)], lc, 6)
        p.line([(34, 0), (16, 200)], lc, 6)
        p.poly([(-34, 196), (34, 196), (34, 280), (-34, 280)], (248, 248, 248), INK, 2.0)
        p.poly([(-34, 196), (34, 196), (34, 214), (-34, 214)], lc, None)
        for k in range(2):
            p.line([(-24, 236 + 16 * k), (24 - 16 * k, 236 + 16 * k)], (160, 160, 170), 2.4)


def arms(img, p, sp, t, front):
    """Arm poses. front=False draws what sits behind the body, front=True what sits in front."""
    pose = sp.get('pose', 'side')
    out = sp.get('outfit', 'suit')
    a = sp.get('arm') or armour()
    plate = out == 'armour' and a['steel_arms']
    skin = a['steel'] if out == 'armour' and a['gauntlets'] else sp['skin']

    def arm(p_, sh, el, wr, sleeve_):  # plate or cloth
        if plate:
            steel_arm(p_, sh, el, wr, a['steel'], fan=a['fans'])
        else:
            globals()['arm'](p_, sh, el, wr, sleeve_)
    sleeve = {'suit': sp.get('jacket', NAVY), 'dress': sp.get('dress', (190, 30, 44)), 'blouse': sp.get('jacket', CHARCOAL),
              'jumper': sp.get('jacket', (90, 110, 140)), 'armour': LEATHER, 'king': (40, 32, 30)}[out]
    sw = sp.get('shoulders', 150)
    if pose == 'none':
        return
    if front:
        pose_arms(img, p, sp, t, pose, skin, sleeve, sw, arm)
        if out == 'armour' and a['pauldron'] and not a['mantle']:
            pauldrons(p, a, sw)
        return
    if pose == 'side':
        for sgn in (-1, 1):
            arm(p, (sgn * (sw - 14), 60), (sgn * (sw + 4), 290), (sgn * (sw - 2), 500), sleeve)
            hand(p, sgn * (sw - 4), 526, skin)


def finger(p, a, d, length, skin, w=9):
    """One finger from point a in direction d."""
    nx, ny = -d[1], d[0]
    b = (a[0] + d[0] * length, a[1] + d[1] * length)
    p.poly([(a[0] + nx * w, a[1] + ny * w), (b[0] + nx * w, b[1] + ny * w), (b[0] - nx * w, b[1] - ny * w),
            (a[0] - nx * w, a[1] - ny * w)], skin, INK, 2.2)
    p.ell(b[0], b[1], w, w, skin, None)
    p.line(oval(b[0], b[1], w, w, 12, math.atan2(d[1], d[0]) - 1.6, math.atan2(d[1], d[0]) + 1.6), INK, 2.2)


def gesture_hand(p, el, wr, shape, skin, extra=None, t=0.0):
    """Hands that talk: a fist, an open palm, an accusing finger, a raised finger, air quotes, or a sword."""
    dx, dy = wr[0] - el[0], wr[1] - el[1]
    n = math.hypot(dx, dy) or 1
    d = (dx / n, dy / n)
    c = (wr[0] + d[0] * 14, wr[1] + d[1] * 14)
    shade_ = dk(skin, 0.8)
    if shape == 'palm':  # open, fingers together, the palm turned up
        nx, ny = -d[1], d[0]
        if ny > 0:
            nx, ny = -nx, -ny
        pts = [(c[0] - nx * 4 - d[0] * 14, c[1] - ny * 4 - d[1] * 14), (c[0] + d[0] * 40 - nx * 6, c[1] + d[1] * 40 - ny * 6),
               (c[0] + d[0] * 52 + nx * 6, c[1] + d[1] * 52 + ny * 6), (c[0] + d[0] * 36 + nx * 22, c[1] + d[1] * 36 + ny * 22),
               (c[0] + nx * 22, c[1] + ny * 22)]
        p.poly(curve(pts, 4), skin, INK, 2.4)
        p.line([(c[0] + d[0] * 6 + nx * 8, c[1] + d[1] * 6 + ny * 8), (c[0] + d[0] * 36 + nx * 8, c[1] + d[1] * 36 + ny * 8)],
               shade_, 1.6)
        return
    if shape == 'sword':
        sword(p, c[0], c[1] - 10, ang=extra if extra is not None else -1.57)
    if shape == 'point':
        finger(p, (c[0] + d[0] * 8, c[1] + d[1] * 8), d, 44, skin)
    if shape == 'point_up':
        finger(p, (c[0], c[1] - 10), (0.12, -1), 44, skin)
    if shape == 'quote':  # two fingers up, bending on the beat
        bend = 0.5 + 0.5 * math.sin(t * 12)
        for k in (-1, 1):
            base = (c[0] + k * 9, c[1] - 12)
            finger(p, base, (0, -1), 22, skin, 7)
            finger(p, (base[0], base[1] - 22), (0.8 * bend * (1 if wr[0] > 0 else -1), -1 + 0.6 * bend), 16, skin, 7)
    p.ell(c[0], c[1], 25, 23, skin, INK, 2.6)
    for k in range(3):
        p.line([(c[0] - 14, c[1] - 8 + 8 * k), (c[0] + 10, c[1] - 10 + 8 * k)], shade_, 1.8)


def pose_arms(img, p, sp, t, pose, skin, sleeve, sw, arm):
    if pose == 'custom':  # arm positions given by the film, frame by frame
        for side, sgn in (('L', -1), ('R', 1)):
            g = sp['arms'].get(side)
            if g:
                el, wr, shape = g[0], g[1], g[2]
                arm(p, (sgn * (sw - 14), 60), el, wr, sleeve)
                gesture_hand(p, el, wr, shape, skin, g[3] if len(g) > 3 else None, t)
        return
    if pose == 'side':  # drawn behind the body, in arms()
        return
    elif pose == 'out':  # both arms open, palms up (the conference-stage gesture)
        for sgn in (-1, 1):
            arm(p, (sgn * (sw - 14), 60), (sgn * (sw + 70), 250), (sgn * (sw + 190), 300), sleeve)
            p.poly(curve([(sgn * (sw + 190), 280), (sgn * (sw + 262), 262), (sgn * (sw + 280), 284), (sgn * (sw + 248), 312),
                          (sgn * (sw + 192), 322)], 4), skin, INK, 2.4)
            p.line([(sgn * (sw + 214), 296), (sgn * (sw + 252), 288)], tuple(int(v * 0.85) for v in skin), 1.6)
    elif pose == 'clap':
        ph = sp.get('clap', 0.0)
        gap = 18 + 22 * (0.5 + 0.5 * math.cos(ph))
        hy = sp.get('clap_y', 220)
        for sgn in (-1, 1):
            arm(p, (sgn * (sw - 14), 60), (sgn * (sw - 10), 300), (sgn * (gap + 22), hy + 10), sleeve)
        for sgn in (-1, 1):
            p.ell(sgn * gap, hy - 6, 17, 30, skin, INK, 2.4, rot=sgn * 0.25)
    elif pose in ('fist', 'sword'):
        # left arm at the side, right arm raised high
        arm(p, (-(sw - 14), 60), (-(sw + 4), 290), (-(sw - 2), 500), sleeve)
        hand(p, -(sw - 4), 526, skin)
        hx, hy = sw + sp.get('reach', 50), -300
        arm(p, (sw - 14, 50), (hx + 20, -110), (hx, hy + 20), sleeve)
        if pose == 'sword':
            sword(p, hx, hy - 10, ang=-1.62 + 0.1 * math.sin(t * 2.4 + sp.get('seed', 0)))
        p.ell(hx, hy, 26, 24, skin, INK, 2.6)
        for k in range(3):
            p.line([(hx - 16, hy - 8 + 9 * k), (hx + 8, hy - 10 + 9 * k)], dk(skin, 0.7), 1.8)
    elif pose == 'swordboth':  # two-handed, straight up
        for sgn in (-1, 1):  # elbows wide so the face stays clear, hands together above the head
            arm(p, (sgn * (sw - 14), 50), (sgn * (sw + 5), -150), (sgn * 26, -380), sleeve)
        sword(p, 0, -400, ang=-1.57 + 0.08 * math.sin(t * 2.2 + sp.get('seed', 0)))
        p.ell(0, -382, 32, 28, skin, INK, 2.6)


def legs(img, p, sp):
    tc = sp.get('trousers', sp.get('jacket', NAVY))
    o = sp.get('stance', 0)
    for sgn in (-1, 1):
        leg = [(sgn * 6, 440), (sgn * 104, 440), (sgn * (100 + o * 0.6), 700), (sgn * (90 + o), 900), (sgn * (30 + o), 902),
               (sgn * (18 + o * 0.6), 700)]
        p.poly(leg, tc, INK, 2.6)
        soft(img, p.cam, [(sgn * 70, 450), (sgn * 100, 450), (sgn * (88 + o), 896), (sgn * (66 + o), 896)], (0, 0, 0), 0.3, 6)
        p.poly(curve([(sgn * (24 + o), 896), (sgn * (94 + o), 894), (sgn * (128 + o), 910), (sgn * (124 + o), 928),
                      (sgn * (20 + o), 928)], 4),
               (22, 20, 22), INK, 2.4)


def person(img, cam, x, y, s, sp, t=0.0, flip=1):
    """Draw one person with the neck base at world (x, y) and scale s."""
    L = Local(cam, x, y + sp.get('sit', 0.0) * 230 * s, s, flip)
    p = Pen(img, L)
    hair_back(p, sp, sp.get('head_dx', 0) * 1.0, -150 + sp.get('head_dy', 0), sp.get('hw', 72), sp.get('hh', 88))
    if sp.get('full'):
        legs(img, p, sp)
    arms(img, p, sp, t, front=False)
    torso(img, p, sp, t)
    arms(img, p, sp, t, front=True)
    head(img, p, sp, t, sp.get('head_dx', 0) * 1.0, -150 + sp.get('head_dy', 0))


# The cast. Caricatures from a few features only.
BURNHAM = dict(skin=PALE, hw=68, hh=96, jaw='long', hair='side', hair_c=(64, 48, 40), grey=(150, 140, 136),
               brow_c=(50, 38, 32), brow_w=4.4, glasses=True, jacket=NAVY, shirt=(212, 224, 238), creases=1,
               outfit='suit')
MINISTERS = [  # left to right as they stand in the front row
    dict(name='Streeting', skin=PALE, hw=70, hh=86, jaw='round', hair='crop', hair_c=(58, 44, 36), jacket=NAVY,
         tie=(150, 30, 50), mouth='grin', brow_c=(58, 44, 36)),
    dict(name='Rayner', skin=PINK, hw=66, hh=84, jaw='soft', hair='bob', hair_c=(206, 128, 72), outfit='dress',
         dress=(196, 26, 46), mouth='smile', earring=True, brow_c=(150, 96, 60), brow_w=2.6),
    dict(name='Miliband', skin=OLIVE, hw=70, hh=92, jaw='long', hair='swept', hair_c=(64, 58, 56),
         grey=(160, 156, 154), nose='long', brow_w=4.6, brow_c=(40, 34, 30), jacket=CHARCOAL, tie=(40, 60, 110),
         mouth='line', brow_raise=3),
    dict(name='Mahmood', skin=BROWN, hw=64, hh=86, jaw='soft', hair='long', hair_c=(44, 32, 28), outfit='blouse',
         jacket=(104, 44, 76), shirt=(230, 222, 214), mouth='smile', brow_c=(30, 22, 22), brow_w=3.0),
    dict(name='Healey', skin=PINK, hw=76, hh=86, jaw='round', hair='bald', hair_c=(168, 162, 158), jacket=NAVY,
         tie=(170, 40, 50), glasses=True, glasses_c=(80, 70, 70), mouth='smile', brow_c=(150, 140, 134), age=True),
]
KNIGHTS = [  # each in different plate; serious or jubilant
    dict(name='elder', skin=PINK, hw=72, hh=90, jaw='round', hair='wisps', hair_c=(236, 236, 232), beard='white',
         beard_c=(238, 238, 234), brow_c=(220, 220, 216), brow_w=4.4, age=True, creases=3, outfit='armour',
         lanyard=True, pose='fist', mouth='shout', mouth_y=66, seed=2, brows='fierce', lid=3,
         arm=armour(steel=(150, 156, 168), mantle=True, fans=False)),
    dict(name='sikh', skin=BROWN, hw=72, hh=88, jaw='square', hair='turban', turban_c=(36, 46, 96), beard='full',
         beard_c=(34, 30, 30), beard_grey=(150, 146, 144), brow_c=(28, 24, 24), brow_w=4.2, outfit='armour',
         lanyard=True, pose='fist', mouth='cheer', mouth_y=64, seed=5, brows='joy',
         arm=armour(steel=(92, 94, 106), pauldron='big', plackart=True, faulds=True)),
    dict(name='young', skin=PALE, hw=64, hh=84, jaw='soft', hair='blonde', hair_c=(236, 204, 128), brow_c=(176, 140, 90),
         brow_w=2.6, outfit='armour', lanyard=True, pose='fist', mouth='cheer', seed=9, brows='joy',
         arm=armour(steel=(178, 180, 188), helmet='sallet', pauldron='small', faulds=True)),
]
MINISTER_ARMOUR = {  # the front row in plate, for the swords shot and Miliband's moment
    'Streeting': dict(arm=armour(steel=(160, 164, 176), helmet='kettle', pauldron='small'), brows='joy', mouth='cheer'),
    'Rayner': dict(arm=armour(steel=(170, 160, 150), mantle=True, fans=False), brows='joy', mouth='cheer'),
    'Miliband': dict(arm=armour(steel=(126, 132, 146), helmet='bascinet', pauldron='big', plackart=True, faulds=True),
                     brows='fierce', lid=3, mouth='shout'),
    'Mahmood': dict(arm=armour(steel=(100, 104, 118), pauldron='small', plackart=True), brows='fierce', mouth='shout'),
    'Healey': dict(arm=armour(steel=(146, 150, 160), helmet='sallet', pauldron='big', faulds=True), mouth='shout'),
}


def armoured(i, **kw):
    m = MINISTERS[i]
    d = dict(m, outfit='armour', lanyard=True, seed=i + 3)
    d.update(MINISTER_ARMOUR[m['name']])
    d.update(kw)
    return d


KING = dict(BURNHAM, outfit='king', mouth='set', shoulders=160, crown=True)


def attendee(rng, furs=False):
    """A random conference-goer, suited or casual (or, later, in furs)."""
    skin = [PALE, PINK, OLIVE, BROWN, DEEP][rng.integers(5)]
    hair = ['side', 'crop', 'bald', 'bob', 'long', 'side'][rng.integers(6)]
    hc = [(58, 44, 36), (30, 24, 22), (150, 110, 70), (200, 170, 110), (170, 166, 162), (110, 70, 46)][rng.integers(6)]
    jacket = [NAVY, CHARCOAL, (110, 40, 50), (70, 90, 120), (90, 96, 80), (150, 60, 70)][rng.integers(6)]
    out = ['suit', 'blouse', 'jumper', 'dress'][rng.integers(4)]
    sp = dict(skin=skin, hair=hair, hair_c=hc, jacket=jacket, dress=jacket, outfit=out, pose='clap',
              clap=rng.uniform(0, 6.28), mouth=['smile', 'line', 'grin'][rng.integers(3)],
              glasses=rng.random() < 0.3, lanyard=True, hw=rng.uniform(62, 76), hh=rng.uniform(82, 94),
              jaw=['square', 'round', 'soft'][rng.integers(3)])
    if furs:
        sp.update(outfit='armour', pose=['sword', 'sword', 'swordboth'][rng.integers(3)],
                  mouth=['shout', 'cheer'][rng.integers(2)], brows=['fierce', 'joy'][rng.integers(2)],
                  seed=int(rng.integers(100)),
                  arm=armour(steel=[STEEL, (90, 92, 104), (160, 164, 172)][rng.integers(3)],
                             helmet=[None, None, 'kettle', 'bascinet', 'sallet'][rng.integers(5)],
                             mantle=rng.random() < 0.4, pauldron=['big', 'small'][rng.integers(2)]))
    return sp


# -------------------------------------------------------------------------------------------- the hall

def backdrop(img, cam, dim=1.0, big=True):
    """The stage wall: a magenta glow into deep red, HOPE AGAIN in big off-white capitals."""
    gradient(img, cam, (-400, -200, 1480, 1340), (236, 52, 150), (140, 10, 40), (620, 1180), 900, 0.9, dim)
    if big:
        c = tuple(int(v * dim) for v in OFFWHITE)
        text(img, cam, 70, 560, 'HOPE', 170, c, widen=0.95)
        text(img, cam, 70, 750, 'AGAIN', 170, c, widen=0.95)


def lectern(img, cam, x, y):
    p = Pen(img, cam)
    p.poly([(x - 48, y - 250), (x + 48, y - 250), (x + 44, y), (x - 44, y)], (206, 204, 210), INK, 3)
    p.poly([(x - 56, y - 262), (x + 56, y - 262), (x + 48, y - 248), (x - 48, y - 248)], (180, 178, 186), INK, 3)
    for k in (-1, 1):
        p.poly([(x + k * 26 - 8, y - 300), (x + k * 26 + 8, y - 300), (x + k * 26 + 6, y - 262), (x + k * 26 - 6, y - 262)],
               (220, 236, 246), INK, 2)
    soft(img, cam, [(x + 10, y - 248), (x + 44, y - 248), (x + 42, y), (x + 10, y)], (0, 0, 0), 0.2, 4)


def rise(t, t0):
    """0 while seated, 1 once on their feet (half a second to get up)."""
    return smooth((t - t0) / 0.5)


def heads_from_behind(img, cam, rows, seed, furs=False, hands_up=0.35, t=0.0, dim=1.0, waves=None):
    """The audience seen from behind: rows of heads and shoulders, some hands up clapping (or swords).
    waves = (first, few, all): one person stands first, then a few, then everyone."""
    rng = np.random.default_rng(seed)
    for ri, (y, s, n, x0, x1) in enumerate(rows):
        xs = np.linspace(x0, x1, n) + rng.uniform(-14, 14, n) * s
        for xi, x in enumerate(xs):
            few = rng.random() < 0.2
            st = 1.0
            if waves:
                t0 = waves[0] if (ri == 3 and xi == n // 2) else waves[1] if few else waves[2]
                st = rise(t, t0)
            p = Pen(img, Local(cam, x, y + rng.uniform(-10, 10) * s + (1 - st) * 120 * s, s))
            hc = [(58, 44, 36), (30, 24, 22), (150, 110, 70), (200, 170, 110), (170, 166, 162), (110, 70, 46),
                  (220, 200, 180)][rng.integers(7)]
            skin = [PALE, PINK, OLIVE, BROWN, DEEP][rng.integers(5)]
            jc = [NAVY, CHARCOAL, (110, 40, 50), (70, 90, 120), (90, 96, 80), (60, 60, 70)][rng.integers(6)]
            if furs:
                jc = FUR
            jc = tuple(int(v * dim) for v in jc)
            hc = tuple(int(v * dim) for v in hc)
            skin = tuple(int(v * dim) for v in skin)
            up = rng.random() < hands_up
            up = up and st > 0.85
            ph_off, side, bald = rng.uniform(0, 6), rng.random() < 0.5, rng.random() < 0.2
            if up and not furs:  # both hands up, clapping over their heads
                ph = t * 19 + ph_off
                g = 16 + 14 * (0.5 + 0.5 * math.cos(ph))
                for sgn in (-1, 1):
                    p.poly([(sgn * 90, 40), (sgn * 120, 30), (sgn * (g + 30), -250), (sgn * (g + 4), -250)], jc, INK, 3)
                    p.ell(sgn * g, -272, 18, 30, skin, INK, 3)
            if furs and up:  # a sword held up
                sgn = 1 if side else -1
                ang = -1.57 + sgn * 0.25 + 0.08 * math.sin(t * 2.3 + x)
                hx, hy = sgn * 70, -300
                p.poly([(sgn * 90, 40), (sgn * 124, 30), (hx + 18, hy), (hx - 10, hy)], jc, INK, 3)
                sword(p, hx, hy - 10, ang=ang, length=420)
                p.ell(hx, hy, 22, 20, skin, INK, 3)
            p.poly(curve([(-140, 160), (-130, 40), (-60, 0), (60, 0), (130, 40), (140, 160)], 4), jc, INK, 3)
            if furs:
                rng2 = np.random.default_rng(abs(int(x * 7)) + 1)
                pts = [(-150, 60 + rng2.uniform(-8, 8)) if k == 0 else
                       (-150 + 300 * k / 10, 20 + (k % 2) * 26 + rng2.uniform(-6, 6)) for k in range(11)]
                p.poly([(-150, -10)] + pts + [(150, -10)], tuple(int(v * dim) for v in FUR_L), INK, 3)
            for sgn in (-1, 1):
                p.ell(sgn * 70, -60, 12, 20, skin, INK, 3)
            p.ell(0, -80, 70, 84, hc, INK, 3)
            if bald and not furs:
                p.ell(0, -40, 60, 50, skin, None)  # a bald crown
                p.ell(0, -80, 70, 84, None, INK, 3)


def clip(img, lay, cam, box):
    """Paste a layer onto the picture, but only inside a world box (a screen, a window)."""
    x0, y0 = cam.P(box[0], box[1])
    x1, y1 = cam.P(box[2], box[3])
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).rectangle([x0, y0, x1, y1], fill=255)
    a = lay.getchannel('A')
    lay.putalpha(Image.fromarray(np.minimum(np.asarray(a), np.asarray(m))))
    img.alpha_composite(lay)


def hall(img, cam, t, furs=False, waves=None):
    """The conference arena from the back: roof rigging, the big screen, banners, the far stage."""
    dim = 0.55 if furs else 1.0
    img.paste((10, 8, 16, 255), (0, 0, img.width, img.height))
    p = Pen(img, cam)
    for y in (330, 372):  # lighting trusses
        p.line([(-60, y), (1140, y + 20)], (70, 70, 80), 5)
    for k in range(12):
        x = 30 + k * 95
        p.line([(x, 330), (x + 40, 392)], (60, 60, 70), 3)
        glow(img, cam, x, 400, 30, (255, 240, 220) if not furs else (160, 190, 255), 0.5 * dim)
        p.ell(x, 398, 9, 7, (250, 245, 235), INK, 2)
    # the big screen: red frame, two pictures of him either side of the slogan
    p.poly([(20, 460), (1060, 460), (1060, 700), (20, 700)], tuple(int(v * dim) for v in (200, 20, 50)), INK, 3)
    for x0 in (60, 700):
        p.poly([(x0, 486), (x0 + 320, 486), (x0 + 320, 674), (x0, 674)], None, INK, 2)
        gradient(img, cam, (x0, 486, x0 + 320, 674), (220, 60, 150), (150, 20, 60), (x0 + 160, 640), 260, 0.8, dim)
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        person(lay, cam, x0 + 160, 640, 0.42, dict(KING if furs else BURNHAM, mouth='set' if furs else 'smile',
                                                     pose='none', bottom=200), t)
        clip(img, lay, cam, (x0, 486, x0 + 320, 674))
    text(img, cam, 540, 540, 'HOPE', 58, tuple(int(v * dim) for v in OFFWHITE), anchor='ma')
    text(img, cam, 540, 604, 'AGAIN', 58, tuple(int(v * dim) for v in OFFWHITE), anchor='ma')
    # tall banners either side
    for x0 in (60, 880):
        p.poly([(x0, 760), (x0 + 140, 760), (x0 + 140, 1090), (x0, 1090)], tuple(int(v * dim) for v in (206, 22, 52)), INK, 3)
        text(img, cam, x0 + 70, 800, 'HOPE', 52, tuple(int(v * dim) for v in OFFWHITE), anchor='ma')
        text(img, cam, x0 + 70, 860, 'AGAIN', 52, tuple(int(v * dim) for v in OFFWHITE), anchor='ma')
        if furs:  # a bee pennant hung beside each banner
            q = [(x0 + 20, 1110), (x0 + 120, 1110), (x0 + 120, 1230), (x0 + 70, 1270), (x0 + 20, 1230)]
            p.poly(q, (70, 30, 30), INK, 3)
            bee(p, x0 + 70, 1180, 34)
    # the far stage and the tiny speaker
    gradient(img, cam, (300, 780, 780, 1060), (236, 52, 150), (150, 10, 44), (540, 1040), 300, 0.8, dim)
    p.poly([(300, 780), (780, 780), (780, 1060), (300, 1060)], None, INK, 3)
    text(img, cam, 320, 800, 'HOPE', 44, tuple(int(v * dim) for v in OFFWHITE))
    text(img, cam, 320, 850, 'AGAIN', 44, tuple(int(v * dim) for v in OFFWHITE))
    p.poly([(260, 1060), (820, 1060), (840, 1090), (240, 1090)], (40, 16, 34), INK, 3)
    person(img, cam, 560, 950, 0.12, dict(KING if furs else BURNHAM, full=True, pose='side', bottom=470), t)
    lectern(img, cam, 720, 1060)
    if furs:
        shade(img, 0.25, (20, 40, 80))
        for (x, y) in ((200, 1180), (860, 1220), (480, 1150)):  # torches held aloft in the crowd
            glow(img, cam, x, y - 30, 160, (255, 160, 60), 0.35)
    rows = [(1180, 0.22, 16, 30, 1050), (1270, 0.3, 12, 20, 1060), (1390, 0.4, 9, 0, 1080),
            (1560, 0.55, 7, -20, 1100), (1780, 0.75, 5, -40, 1120)]
    front = Image.new('RGBA', img.size, (0, 0, 0, 0))
    heads_from_behind(front, cam, rows, 11, furs=furs, hands_up=0.45 if not furs else 0.6, t=t,
                      dim=0.85 if not furs else 0.6, waves=waves)
    if furs:
        p2 = Pen(front, cam)
        for (x, y) in ((200, 1180), (860, 1220), (480, 1150)):
            p2.line([(x, y + 120), (x, y - 10)], LEATHER, 10)
            flame = [(x - 22, y - 10), (x, y - 90 - 10 * math.sin(t * 19 + x)), (x + 22, y - 10), (x, y + 6)]
            p2.poly(curve(flame, 4), (255, 170, 60), INK, 3)
            p2.poly(curve([(x - 10, y - 12), (x, y - 50), (x + 10, y - 12)], 3), (255, 236, 150), None)
    img.alpha_composite(front)


# --------------------------------------------------------------------------------------------- captions

def wrap(s, font, maxw):
    rows, cur = [], ''
    for w in s.split():
        trial = (cur + ' ' + w).strip()
        if cur and font.getbbox(trial)[2] > maxw:
            rows.append(cur)
            cur = w
        else:
            cur = trial
    rows.append(cur)
    return rows


def caption(img, s, bottom=1480):
    """Speech: bold white letters with a black outline, wrapped to 800 px, centred on x = 480."""
    f = ImageFont.truetype(SANS, 50 * SS)
    rows = wrap(s, f, 800 * SS)
    d = ImageDraw.Draw(img)
    for i, row in enumerate(rows):
        y = (bottom - 34 - 64 * (len(rows) - 1 - i)) * SS
        d.text((480 * SS, y), row, font=f, fill=(255, 255, 255), anchor='mm', stroke_width=5 * SS, stroke_fill=(0, 0, 0))


def shout(img, s, bottom=1470):
    """A shout: big Anton capitals, white, heavy outline, inside the safe area."""
    size = 120
    while True:
        f = ImageFont.truetype(ANTON, size * SS)
        rows = wrap(s, f, 800 * SS)
        if len(rows) <= 2 and max(f.getbbox(r)[2] for r in rows) <= 800 * SS:
            break
        size -= 4
    d = ImageDraw.Draw(img)
    top = bottom - len(rows) * size * 1.08 - size * 0.12
    for i, row in enumerate(rows):
        d.text((480 * SS, (top + i * size * 1.08) * SS), row, font=f, fill=(255, 255, 255), anchor='ma',
               stroke_width=int(size * 0.07) * SS, stroke_fill=(0, 0, 0))


def title(img, s='HOPE AGAIN', alpha=1.0):
    """The cranberry-red title card, drawn fresh at full size, top edge at 330 px, within 840 px."""
    size = 200
    while True:
        f = ImageFont.truetype(ANTON, size * SS)
        out = max(3, int(size * 0.075)) * SS
        l, t, r, b = f.getbbox(s, stroke_width=out)
        if (r - l) * 1.2 <= 840 * SS:
            break
        size -= 4
    lay = Image.new('RGBA', (r - l + 2 * out, b - t + 2 * out), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((out - l, out - t), s, font=f, fill=(0, 0, 0), stroke_width=out, stroke_fill=(0, 0, 0))
    d.text((out - l, out - t), s, font=f, fill=CRANBERRY, stroke_width=max(1, int(f.size * 0.012)), stroke_fill=CRANBERRY)
    lay = lay.resize((int(lay.width * 1.2), lay.height), Image.LANCZOS)
    if alpha < 1:
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * alpha)))
    img.alpha_composite(lay, (int(540 * SS - lay.width / 2), 330 * SS))


# ------------------------------------------------------------------------------------------------ shots

LINE = ("The British Right talk about 'taking back control'. Never let them forget, they are the ones that "
        "gave it away in the first place.")


def shot_stage(t, with_title=True, cap=None, mouth='talk', push=None, blink=False, arms=None, look=0.0):
    img = canvas()
    k = smooth(push) if push is not None else 0.0  # a very slow push-in over the whole speech
    cam = Cam(1 + 0.15 * k, 540 + 60 * k, 960 - 140 * k)
    backdrop(img, cam)
    p = Pen(img, cam)
    p.poly([(-20, 1340), (1100, 1340), (1100, 1420), (-20, 1420)], (44, 16, 36), INK, 3)
    glow(img, cam, 560, 1344, 260, (255, 150, 210), 0.35)
    lectern(img, cam, 930, 1340)
    person(img, cam, 600, 1340 - 918 * 0.7, 0.7, dict(BURNHAM, full=True, pose='custom' if arms else 'out', arms=arms,
                                                     mouth=mouth, bottom=470, blink=blink, stance=26, head_dy=-4,
                                                     look=look, turn=look * 0.3), t)
    front = Image.new('RGBA', img.size, (0, 0, 0, 0))
    rng = np.random.default_rng(4)
    fp = Pen(front, cam)
    for i in range(14):  # the audience's heads in the dark, right at the front
        x = -40 + i * 86 + rng.uniform(-20, 20)
        y = 1500 + rng.uniform(-40, 60)
        fp.ell(x, y, 58, 70, (22, 12, 22), None)
        fp.poly([(x - 110, y + 60), (x + 110, y + 60), (x + 130, y + 400), (x - 130, y + 400)], (22, 12, 22), None)
    img.alpha_composite(front.filter(ImageFilter.GaussianBlur(cam.S(6))))
    if cap:
        caption(img, cap)
    if with_title:
        title(img)
    return img


WAVES_HALL = (0.3, 1.1, 1.9)   # shot 2: one person stands, then a few, then everyone
STAND_ROW = {'Streeting': 0.2, 'Rayner': 0.8, 'Healey': 0.8, 'Mahmood': 1.4}  # shot 3; Miliband stays seated


def shot_hall(t, furs=False, chant=True):
    img = canvas()
    hall(img, Cam(), t, furs, waves=None if furs else WAVES_HALL)
    if furs and chant:
        shout(img, 'KING OF THE NORTH!')
    return img


def shot_front_row(t):
    img = canvas((14, 10, 18))
    cam = Cam()
    gradient(img, cam, (0, 0, 1080, 1100), (90, 20, 50), (14, 10, 18), (540, 200), 900, 0.8)
    # the rest of the hall behind them, getting to its feet, softly out of focus
    back = Image.new('RGBA', img.size, (0, 0, 0, 0))
    rng = np.random.default_rng(21)
    for row, (y, s) in enumerate(((700, 0.36), (800, 0.46))):
        for i in range(8 - row):
            sp = attendee(rng)
            up = rise(t, 0.8 if rng.random() < 0.3 else 1.4)
            sp.update(clap=t * 19 + i, sit=1 - up, pose='clap' if up > 0.8 else 'side')
            person(back, cam, 60 + i * (140 + 20 * row) + rng.uniform(-20, 20), y, s, sp, t)
    img.alpha_composite(back.filter(ImageFilter.GaussianBlur(cam.S(4))))
    shade(img, 0.15)
    order = [0, 4, 1, 3, 2]
    for i in order:
        up = rise(t, STAND_ROW.get(MINISTERS[i]['name'], 99))
        sp = dict(MINISTERS[i], pose='clap' if up > 0.8 else 'side', clap=t * 19 + i * 1.3, clap_y=170,
                  lanyard=False, sit=1 - up)
        if MINISTERS[i]['name'] == 'Miliband':
            sp['mouth'] = 'line'
        person(img, cam, 110 + i * 185, 1010, 0.76, sp, t)
    p = Pen(img, cam)  # the lip of the stage across the bottom, with a monitor speaker
    p.poly([(-20, 1440), (1100, 1440), (1100, 1940), (-20, 1940)], (24, 12, 22), INK, 4)
    glow(img, cam, 540, 1440, 700, (255, 120, 190), 0.12)
    p.poly([(360, 1470), (720, 1470), (760, 1580), (320, 1580)], (36, 34, 40), INK, 3)
    p.poly([(400, 1484), (680, 1484), (706, 1566), (374, 1566)], (20, 20, 24), None)
    return img


def front_row_bg(img, cam, t, furs=False, level=None):
    """The hall behind the front row, softly out of focus: suits clapping, or later furs and swords."""
    back = Image.new('RGBA', img.size, (0, 0, 0, 0))
    rng = np.random.default_rng(21)
    for row, (y, s) in enumerate(((700, 0.36), (800, 0.46))):
        for i in range(8 - row):
            sp = attendee(rng, furs=furs)
            sp['clap'] = t * 19 + i
            if furs and level is not None:
                sp['mouth'] = mouth_by_level(sp['mouth'], level, i + int(t * 12))
            person(back, cam, 60 + i * (140 + 20 * row) + rng.uniform(-20, 20), y, s, sp, t)
    img.alpha_composite(back.filter(ImageFilter.GaussianBlur(cam.S(4))))


def stage_lip(img, cam, y=1440):
    p = Pen(img, cam)
    p.poly([(-20, y), (1100, y), (1100, 1940), (-20, 1940)], (24, 12, 22), INK, 4)
    glow(img, cam, 540, y, 700, (255, 120, 190), 0.12)
    p.poly([(360, y + 30), (720, y + 30), (760, y + 140), (320, y + 140)], (36, 34, 40), INK, 3)
    p.poly([(400, y + 44), (680, y + 44), (706, y + 126), (374, y + 126)], (20, 20, 24), None)


def shot_miliband(t, window=(0.85, 99), arms=None, level=None):
    """The front row again: Miliband, in plate, gets to his feet and bellows. His neighbours clap on in suits."""
    img = canvas((14, 10, 18))
    cam = Cam()
    gradient(img, cam, (0, 0, 1080, 1100), (90, 20, 50), (14, 10, 18), (540, 200), 900, 0.8)
    front_row_bg(img, cam, t)
    shade(img, 0.15)
    for i, x in ((1, 100), (3, 870)):  # Rayner and Mahmood either side, still in suits, still clapping
        person(img, cam, x, 960, 0.95, dict(MINISTERS[i], pose='clap', clap=t * 19 + i, clap_y=170), t)
    up = rise(t, 0.35)
    shouting = window[0] <= t <= window[1]
    sp = armoured(2, sit=1 - up, pose='fist' if shouting else 'side', mouth='shout' if shouting else 'line',
                  brows='fierce' if shouting else None)
    if arms:
        sp.update(pose='custom', arms=arms)
    if shouting and level is not None:
        sp['mouth'] = mouth_by_level('shout', level, int(t * 12))
    person(img, cam, 480, 930, 1.08, sp, t)
    stage_lip(img, cam, 1450)
    if shouting:
        shout(img, 'KING OF THE NORTH!')
    return img


def shot_front_swords(t, chant=True, level=None):
    """From the stage: the whole hall in furs and plate, swords up, the front row in their own armour."""
    img = canvas((10, 12, 22))
    cam = Cam()
    gradient(img, cam, (0, 0, 1080, 1100), (40, 44, 80), (8, 10, 20), (540, 260), 900, 0.8)
    for (x, y) in ((150, 620), (930, 640), (540, 560)):  # torches at the back
        glow(img, cam, x, y, 180, (255, 160, 60), 0.3)
    front_row_bg(img, cam, t, furs=True, level=level)
    shade(img, 0.12, (10, 20, 50))
    poses = ['sword', 'swordboth', 'sword', 'swordboth', 'sword']
    for i in [0, 4, 1, 3, 2]:
        sp = armoured(i, pose=poses[i], reach=-30)
        if level is not None:
            sp['mouth'] = mouth_by_level(sp['mouth'], level, i + int(t * 12))
        person(img, cam, 110 + i * 185, 1010, 0.76, sp, t, flip=-1 if i == 0 else 1)
    stage_lip(img, cam, 1440)
    shade(img, 0.1, (10, 20, 60))
    if chant:
        shout(img, 'KING OF THE NORTH!')
    return img


def shot_knight(t, k, window=None, arms=None, level=None):
    img = canvas((14, 10, 18))
    cam = Cam()
    gradient(img, cam, (0, 0, 1080, 1920), (110, 24, 58), (14, 10, 18), (540, 500), 1000, 0.9)
    back = Image.new('RGBA', img.size, (0, 0, 0, 0))
    rng = np.random.default_rng(40 + k)
    for i, (x, y, s) in enumerate(((40, 660, 0.46), (300, 650, 0.46), (700, 655, 0.46), (1000, 660, 0.46),
                                   (130, 900, 0.78), (880, 905, 0.8))):
        sp = attendee(rng)
        sp['clap'] = t * 19 + i * 2
        person(back, cam, x, y, s, sp, t)
    img.alpha_composite(back.filter(ImageFilter.GaussianBlur(cam.S(5))))
    shade(img, 0.18)
    on = window is None or window[0] <= t <= window[1]
    sp = dict(KNIGHTS[k], bottom=700)
    if arms:
        sp.update(pose='custom', arms=arms)
    if not on:
        sp.update(mouth='line', brows=None, lid=0)
    elif level is not None:
        sp['mouth'] = mouth_by_level(KNIGHTS[k]['mouth'], level, int(t * 12))
    person(img, cam, 470, 900, 1.2, sp, t)
    if on:
        shout(img, 'KING OF THE NORTH!')
    return img


def shot_king(t, zoom=0.0, blink=False):
    """Burnham in furs on the stage, lit from one side; zoom 0 = chest up, 1 = the final close-up."""
    k = smooth(zoom)
    z = 1.0 + 1.0 * k
    cam = Cam(z, 480, 960 - 110 * k)
    img = canvas()
    backdrop(img, cam, dim=0.42, big=True)
    shade(img, 0.35, (10, 20, 50))
    img = img.filter(ImageFilter.GaussianBlur(SS * (3 + 8 * k)))
    turn = sp_turn(t) if zoom == 0 else 0.0
    person(img, cam, 480, 1010, 1.7, dict(KING, turn=turn, look=turn, bottom=800, blink=blink), t)
    # a hard side light from our right: the other half of his face and body falls into shadow
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    hx = 480 + turn * 1.7 * 72 * 0.22
    ImageDraw.Draw(lay).polygon([cam.P(-200, 300), cam.P(hx - 30, 300), cam.P(hx - 30, 2400), cam.P(-200, 2400)],
                                fill=(6, 8, 24, 140))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(cam.S(44))))
    return img


def sp_turn(t):
    """A slow look to his left, a hold, then a slow look to his right."""
    if t < 1.6:
        return -0.9 * smooth(t / 1.2)
    return -0.9 + 1.8 * smooth((t - 2.0) / 1.6)


# The storyboard: shot number, name, time on screen, what the still shows.
BOARD = [
    ('1', 'The stage', '0-14.2 s', lambda: shot_stage(1.2, cap="The British Right talk about 'taking back control'.")),
    ('2', 'Ovation: one, a few, all', '14.2-17.2 s', lambda: shot_hall(1.8)),
    ('3', 'Front row, waves', '17.2-19.7 s', lambda: shot_front_row(1.25)),
    ('4', 'Knight one (serious)', '19.7-22 s', lambda: shot_knight(0.3, 0)),
    ('5', 'Knight two (jubilant)', '22-24.6 s', lambda: shot_knight(0.3, 1)),
    ('6', 'Knight three (jubilant)', '24.6-26.5 s', lambda: shot_knight(0.3, 2)),
    ('7', 'Miliband stands, bellows', '26.5-29.7 s', lambda: shot_miliband(1.5)),
    ('8', 'King looks left, right', '29.7-33.7 s', lambda: shot_king(1.4)),
    ('9', 'Swords (behind)', '33.7-36.2 s', lambda: shot_hall(0.4, furs=True)),
    ('10', 'Swords (front)', '36.2-39.2 s', lambda: shot_front_swords(0.4)),
    ('11', 'Slow push in on his face', '39.2-43.2 s', lambda: shot_king(0, zoom=1.0)),
]


def finish(img):
    return img.convert('RGB').resize((W, H), Image.LANCZOS)


def main():
    mode = sys.argv[1]
    if mode == 'stills':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        only = sys.argv[3:] or [b[0] for b in BOARD]
        for n, name, _, fn in BOARD:
            if n in only:
                finish(fn()).save(os.path.join(out, f'shot{n}.png'))
                print('shot', n, flush=True)
    elif mode == 'sheet':
        out, dst = sys.argv[2], sys.argv[3]
        cw, ch, lab = 540, 960, 120
        rows = (len(BOARD) + 2) // 3
        sheet = Image.new('RGB', (cw * 3 + 80, (ch + lab + 10) * rows + 30), (245, 242, 236))
        d = ImageDraw.Draw(sheet)
        f1 = ImageFont.truetype(SANS, 34)
        f2 = ImageFont.truetype(SANS, 26)
        for i, (n, name, when, _) in enumerate(BOARD):
            im = Image.open(os.path.join(out, f'shot{n}.png')).resize((cw, ch), Image.LANCZOS)
            x, y = 20 + (i % 3) * (cw + 20), 20 + (i // 3) * (ch + lab + 10)
            sheet.paste(im, (x, y))
            d.text((x + 4, y + ch + 12), f'{n}. {name}', font=f1, fill=(20, 20, 20))
            d.text((x + 4, y + ch + 58), when, font=f2, fill=(90, 90, 90))
        sheet.save(dst, quality=88)


if __name__ == '__main__':
    main()
