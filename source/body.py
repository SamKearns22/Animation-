#!/usr/bin/env python3
"""MAP  body: the people engine (one-route-kit Change 2, 20 Nov). One file owns each drawing step of a person: the
camera and pen, the body and its outfits, arm poses, the plain head (tools' test people only: a film's people come
from the people kit, people.py, which hangs each look's head and torso on HEADS and TORSOS), the head's tilt, the
house limbs (limbs.py) and circle hands (satire_style.py). Lifted out of Hope Again's film file (burnham.py) and the
hooks that six later films' files laid over it (The Traitors' head and torso hooks, Mossad's tilt, MidTerminal's
short sleeves in views.py), so no kit file loads a finished film and no step is overwritten by another file. Hope
Again's knights (armour, swords, crowns, its hall) stay with that film at its bookmark.

Map: constants | Cam, Local, Pen | canvas, gradient, shade, text, dk, lt, wrap, title_lines | the plain head
(head_outline, hair, beard, mouth, face) | head (HEADS, tilt: Rot) | torso (TORSOS) | arms, finger, pose_arms |
person | the house limbs and circle hands (_house)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ink import INK, curve, oval, soft



HERE = os.path.dirname(os.path.abspath(__file__))
W, H, SS = 1080, 1920, 2
HEM = 0.85    # the torso's hem width over the shoulders' (Sam, 20 Oct: hips about 15% narrower, less blocky)
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


GOLD = (222, 176, 60)


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


def dk(c, k=0.66):
    return tuple(int(v * k) for v in c)


def lt(c, k=1.25):
    return tuple(min(255, int(v * k)) for v in c)


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


def title_lines(img, lines=('HOPE', 'AGAIN'), cap=148, top=330, alpha=1.0):
    """The title at the account's standard size: each line's capitals `cap` px tall (Listening & Learning's
    size), Anton widened 20%, cranberry red, thick black outline, centred on the frame, top edge at `top`."""
    probe = ImageFont.truetype(ANTON, 1000)
    l, t, r, b = probe.getbbox('H')
    size = int(round(cap * 1000 / (b - t)))
    f = ImageFont.truetype(ANTON, size * SS)
    out = max(3, int(size * 0.075)) * SS
    y = top * SS
    for s in lines:
        l, t, r, b = f.getbbox(s, stroke_width=out)
        lay = Image.new('RGBA', (r - l + 2 * out, b - t + 2 * out), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.text((out - l, out - t), s, font=f, fill=(0, 0, 0), stroke_width=out, stroke_fill=(0, 0, 0))
        d.text((out - l, out - t), s, font=f, fill=CRANBERRY, stroke_width=max(1, int(f.size * 0.012)),
               stroke_fill=CRANBERRY)
        lay = lay.resize((int(lay.width * 1.2), lay.height), Image.LANCZOS)
        if alpha < 1:
            lay.putalpha(lay.getchannel('A').point(lambda v: int(v * alpha)))
        img.alpha_composite(lay, (int(540 * SS - lay.width / 2), int(y)))
        y += lay.height - 2 * out + out * 0.6


def head_outline(hx, hy, hw, hh, jaw):
    top = oval(hx, hy - 6, hw, hh, 40, math.pi, 2 * math.pi)
    j = {'square': (0.95, 0.62, 1.02), 'round': (0.98, 0.72, 0.96), 'long': (0.9, 0.5, 1.12),
         'soft': (0.9, 0.56, 1.0)}[jaw]
    return top + [(hx + hw, hy + 10), (hx + hw * j[0], hy + hh * 0.66), (hx + hw * j[1], hy + hh * 1.02 * j[2]),
                  (hx, hy + hh * 1.14 * j[2]), (hx - hw * j[1], hy + hh * 1.02 * j[2]),
                  (hx - hw * j[0], hy + hh * 0.66), (hx - hw, hy + 10)]


def plain_hair_back(p, sp, hx, hy, hw, hh):
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
        if not sp.get('no_shine'):                    # none lying (it read as a balloon, Sam 10 Nov)
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
        if sp.get('heavy_stubble'):  # tough stubble: a flat shadow over the jaw, cheeks and lip, then the dots
            tone = tuple(int(a + (b - a) * 0.3) for a, b in zip(sp['skin'], sp.get('beard_c', (90, 70, 60))))
            p.poly(curve([(hx - hw * 0.96, hy + 20), (hx - hw * 0.9, hy + hh * 0.66), (hx - hw * 0.5, hy + hh * 1.0),
                          (fx, hy + hh * 1.08), (hx + hw * 0.5, hy + hh * 1.0), (hx + hw * 0.9, hy + hh * 0.66),
                          (hx + hw * 0.96, hy + 20), (fx + 34, hy + 44), (fx + 14, hy + 40), (fx - 14, hy + 40),
                          (fx - 34, hy + 44)], 4), tone, None)
        rng = np.random.default_rng(5)
        for _ in range(140 if sp.get('heavy_stubble') else 70):
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
    if isinstance(m, str) and m.startswith('v:'):         # a spoken shape (mouths.py: sp['mouth'] = 'v:AI')
        import mouths
        shape = m[2:]
        if sp.get('smile', 0.0) <= -0.6 and shape in ('etc', 'E', 'AI'):   # an angry face talks angrily (Milburn
            shape += '!'                                                      # critique r2: rage read as a laugh)
        return mouths.draw(p, sp, fx, my, shape)
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
    lid = sp.get('lid', 0) + 3 * sp.get('harrow', 0.0)
    bc = sp.get('brow_c', tuple(int(v * 0.8) for v in sp.get('hair_c', (60, 44, 34))))
    for sgn in (-1, 1):
        ex, ey = fx - 4 + sgn * 30, hy - 8
        if blink:
            p.line([(ex - 16, ey), (ex, ey + 3), (ex + 16, ey)], INK, 2.4)
        else:
            almond = [(ex - 17, ey), (ex - 8, ey - 8), (ex + 8, ey - 8), (ex + 17, ey), (ex + 8, ey + 7), (ex - 8, ey + 7)]
            p.poly(almond, (250, 250, 248), INK, 2.0)
            lv = sp.get('look_v', 0.0)                                   # +1 down, -1 up
            px_, py_ = ex + look * 7, ey + 1 + lv * 5
            # the pupil stays inside the eye: any part past the eye's edge is under the lid (Sam, 19 Oct), so it is
            # drawn already cut to the eye's outline (each point held between its top and bottom edges)
            def _edge(x, pts):
                for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                    if x0 <= x <= x1:
                        return y0 + (y1 - y0) * (x - x0) / max(1e-6, x1 - x0)
                return ey
            bot = [(ex - 17, ey), (ex - 8, ey + 7), (ex + 8, ey + 7), (ex + 17, ey)]
            top = [(ex - 17, ey), (ex - 8, ey - 8), (ex + 8, ey - 8), (ex + 17, ey)]
            circ = [(px_ + 4.5 * math.cos(a_), py_ + 4.5 * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 24, endpoint=False)]
            circ = [(x, min(max(y, _edge(x, top) + 1), _edge(x, bot) - 1)) for x, y in circ]
            p.poly(circ, INK, None)
            if lid > 0:  # a heavy lid drooping over the top of the eye
                p.poly([(ex - 18, ey - 2), (ex - 8, ey - 10), (ex + 8, ey - 10), (ex + 18, ey - 2), (ex + 17, ey - 1 + lid),
                        (ex + 8, ey - 9 + lid), (ex - 8, ey - 9 + lid), (ex - 17, ey - 1 + lid)], dk(skin, 0.84), None)
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
    h = sp.get('harrow', 0.0)
    if h > 0:  # the weight of the world: dark rings under the eyes, bags, heavier lids
        for sgn in (-1, 1):
            ex, ey = fx - 4 + sgn * 30, hy - 8
            soft(img, p.cam, [(ex - 20, ey + 5), (ex - 8, ey + 16), (ex + 8, ey + 16), (ex + 20, ey + 5), (ex + 8, ey + 10),
                              (ex - 8, ey + 10)], (96, 52, 84), 0.5 * h, 3)
            if h > 0.2:
                p.line([(ex - 16, ey + 9), (ex - 6, ey + 14), (ex + 6, ey + 14), (ex + 16, ey + 9)], dk(skin, 0.72), 2.0)
            if h > 0.55:
                p.line([(ex - 12, ey + 20), (ex, ey + 24), (ex + 12, ey + 20)], dk(skin, 0.78), 1.8)
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


def plain_head(img, p, sp, t, hx, hy):
    """The engine's plain head: tools' test people (a film's people come from the people kit: HEADS)."""
    hw, hh = sp.get('hw', 72), sp.get('hh', 88)
    skin = sp['skin']
    turn = sp.get('turn', 0.0)
    for sgn in (-1, 1):  # ears, pushed round by a turn
        p.poly(oval(hx + sgn * (hw + 2) - turn * 6, hy + 6, 12, 22), skin, INK, 2.4)
    p.poly(head_outline(hx, hy, hw, hh, sp.get('jaw', 'square')), skin, INK, 2.6)
    # no darker shadow side on the face or clothes (Sam, 14 Nov): the house look gives the depth
    fx = face(img, p, sp, t, hx, hy, hw, hh)
    beard(p, sp, hx, hy, hw, hh, fx)
    mouth(p, sp, t, fx, hy + sp.get('mouth_y', 60))
    hair_front(p, sp, hx, hy, hw, hh, fx)
    if sp.get('earring'):
        p.ell(hx - hw - 2, hy + 30, 4, 4, GOLD, INK, 1.2)


class Rot:
    """A person's local frame, turned about a pivot (to tilt the head)."""
    def __init__(self, L, a, pivot=(0, -60)):
        self.L, self.c, self.s_, self.pv = L, math.cos(a), math.sin(a), pivot
        self.s, self.cam = L.s, L.cam

    def P(self, x, y):
        dx, dy = x - self.pv[0], y - self.pv[1]
        return self.L.P(self.pv[0] + dx * self.c - dy * self.s_, self.pv[1] + dx * self.s_ + dy * self.c)

    def S(self, v):
        return self.L.S(v)


def tilted(fn):
    """Draw a head part turned about the neck by sp['tilt'] (radians), so heads can tilt and sway (from Mossad)."""
    def draw(*args):
        sp = next(a for a in args if isinstance(a, dict))
        if not sp.get('tilt'):
            return fn(*args)
        args = list(args)
        k = next(i for i, a in enumerate(args) if isinstance(a, Pen))
        args[k] = Pen(args[k].img, Rot(args[k].cam, sp['tilt'], pivot=(0, -60)))
        return fn(*args)
    return draw


HEADS, TORSOS = {}, {}      # each look's own head and torso, by who (the people kit fills them: people.install)
HAIR_BEHIND = {}            # a look's own hair behind the head, by who (people.install: a famous look's curls)


def head(img, p, sp, t, hx, hy):
    """A look's own head (HEADS), else the plain head, turned by sp['tilt']."""
    f = HEADS.get(sp.get('who'))
    return f(img, p, sp, t, hx, hy) if f else tilted(plain_head)(img, p, sp, t, hx, hy)


def hair_back(p, sp, hx, hy, hw, hh):
    """The plain head's hair behind the head; a look with its own head draws its own (HEADS)."""
    if sp.get('who') in HEADS:
        f = HAIR_BEHIND.get(sp.get('who'))
        return f(p, sp, hx, hy, hw, hh) if f else None
    return tilted(plain_hair_back)(p, sp, hx, hy, hw, hh)


def hand(p, x, y, skin, r=19, rot=0.0):
    p.ell(x, y, r, r * 0.86, skin, INK, 2.4, rot=rot)


def plain_torso(img, p, sp, t):
    out = sp.get('outfit', 'suit')
    skin = sp['skin']
    bottom = sp.get('bottom', 560)
    sw = sp.get('shoulders', 150)
    # neck
    nx, ny = (sp.get('head_dx', 0.0), sp.get('head_dy', 0.0)) if sp.get('neck_lean') else (0.0, 0.0)
    if not sp.get('neck_off'):                   # lying_flat draws the neck with the head (Job I)
        p.poly([(-32 + nx, -80 + ny), (32 + nx, -80 + ny), (36, 10), (-36, 10)], skin, INK, 2.6)   # neck_lean: its top
        soft(img, p.cam, [(-32 + nx, -76 + ny), (32 + nx, -76 + ny), (30 + nx * 0.5, -40), (-30 + nx * 0.5, -40)],
             (150, 90, 80), 0.35, 4)                # follows a shifted head, one neck (Ad-Vanced Notice, 8 Nov)
    body = [(-40, -4), (-sw * 0.8, 12), (-sw, 50), (-sw - 6, 200), (-sw * HEM, bottom), (sw * HEM, bottom),
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
    elif out == 'dress':
        dc = sp.get('dress', (190, 30, 44))
        p.poly(body, dc, INK, 2.6)
        p.poly([(-46, -4), (46, -4), (30, 50), (0, 70), (-30, 50)], skin, INK, 2.2)
    elif out == 'blouse':  # a dark jacket over a pale top
        jc = sp.get('jacket', CHARCOAL)
        p.poly(body, jc, INK, 2.6)
        p.poly([(-50, -4), (50, -4), (34, 180), (-34, 180)], sp.get('shirt', (236, 232, 228)), INK, 2.0)
    elif out == 'jumper':
        jc = sp.get('jacket', (90, 110, 140))
        p.poly(body, jc, INK, 2.6)
        p.line(oval(0, -2, 46, 22, 24, 0.2, math.pi - 0.2), INK, 2.4)
    if sp.get('lanyard'):  # the conference pass, still round the neck
        lc = sp.get('lanyard_c', (196, 26, 52))
        p.line([(-34, 0), (-16, 200)], lc, 6)
        p.line([(34, 0), (16, 200)], lc, 6)
        p.poly([(-34, 196), (34, 196), (34, 280), (-34, 280)], (248, 248, 248), INK, 2.0)
        p.poly([(-34, 196), (34, 196), (34, 214), (-34, 214)], lc, None)
        for k in range(2):
            p.line([(-24, 236 + 16 * k), (24 - 16 * k, 236 + 16 * k)], (160, 160, 170), 2.4)


def torso(img, p, sp, t):
    """The body in its outfit, then the look's own torso pieces (TORSOS)."""
    plain_torso(img, p, sp, t)
    f = TORSOS.get(sp.get('who'))
    if f:
        f(img, p, sp, t)


def arms(img, p, sp, t, front):
    """Arm poses. front=False draws what sits behind the body, front=True what sits in front."""
    pose = sp.get('pose', 'side')
    out = sp.get('outfit', 'suit')
    skin = sp['skin']

    def arm(p_, sh, el, wr, sleeve_):  # the house limb (installed by _house)
        globals()['arm'](p_, sh, el, wr, sleeve_)
    sleeve = {'suit': sp.get('jacket', NAVY), 'dress': sp.get('dress', (190, 30, 44)), 'blouse': sp.get('jacket', CHARCOAL),
              'jumper': sp.get('jacket', (90, 110, 140))}[out]
    sw = sp.get('shoulders', 150)
    if pose == 'none':
        return
    if front:
        pose_arms(img, p, sp, t, pose, skin, sleeve, sw, arm)
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
    elif pose == 'fist':
        # left arm at the side, right arm raised high
        arm(p, (-(sw - 14), 60), (-(sw + 4), 290), (-(sw - 2), 500), sleeve)
        hand(p, -(sw - 4), 526, skin)
        hx, hy = sw + sp.get('reach', 50), -300
        arm(p, (sw - 14, 50), (hx + 20, -110), (hx, hy + 20), sleeve)
        p.ell(hx, hy, 26, 24, skin, INK, 2.6)
        for k in range(3):
            p.line([(hx - 16, hy - 8 + 9 * k), (hx + 8, hy - 10 + 9 * k)], dk(skin, 0.7), 1.8)


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


arm = legs = gesture_hand = None   # each filled once by _house() below: the house limbs and circle hands


def _house():
    """The house limbs (limbs.py: one tube from shoulder to wrist, joined to the body's outline; legs curved through
    the knee) and circle hands (satire_style.py), each the one definition of its step; every arm is measured by the
    arm check (figure.py)."""
    import figure
    import limbs
    import satire_style
    me = sys.modules[__name__]
    figure._GUARDED.setdefault('arm', None)     # limbs' arm runs figure.audit_arm on every arm
    limbs.install(me)
    satire_style.install_circle_hands(me)


_house()
