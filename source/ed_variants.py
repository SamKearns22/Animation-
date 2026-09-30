#!/usr/bin/env python3
"""Listening & Learning: subtle character redesigns inside the ORIGINAL look.

Same flat cartoon, same dark stadium, same spotlight, same pose and camera (ed.py's stage and camera are
reused unchanged). Only the way the character is designed changes, one or two FilmCow tell-tales at a
time, so the film stays recognisably ours but stops reading as a copy.

Options (combined per variant in VARIANTS):
    line    'black' (as now) or 'colour': outlines in a darker shade of each shape's own colour
    eyes    'almond' (as now) or 'lids': white eyes half-covered by heavy skin-coloured lids, coloured iris
    build   'box' (as now) or 'round': pear-shaped head with fuller cheeks, shorter thicker neck, sloping
            shoulders, tapered curved arms and proper hands with a thumb
    shade   'soft' (as now, airbrushed) or 'cel': one hard-edged shadow tone
    grain   False or True: a faint print grain over the fills
    rim     False or True: a cranberry rim light down his shadow side (a CranbriJoos signature)

Usage:
    python3 ed_variants.py stills OUT_DIR [T]
    python3 ed_variants.py sheet OUT.jpg CURRENT.png STILLS_DIR PICK
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import ed
from ed import INK, SKIN, SKIN_D, GINGER, GINGER_D, LILAC, LILAC_D, TROUSER, TATS, W, H, SS, Cam, curve, oval, \
    speaking, mouth_shape

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
TITLE_FONT = os.path.join(HERE, 'fonts', 'Anton-Regular.ttf')
CRANBERRY = (178, 24, 52)

VARIANTS = {
    'A': dict(name='A. Coloured outlines', note='Darker shade of each colour, not black',
              line='colour'),
    'B': dict(name='B. Heavy lids', note='Half-lidded eyes; hard-edged shadow',
              eyes='lids', shade='cel'),
    'C': dict(name='C. Rounder build', note='Pear head, tapered arms, real hands',
              build='round'),
    'D': dict(name='D. Grain + rim light', note='Print grain, cranberry rim light',
              grain=True, rim=True),
    'E': dict(name='E. All of A-D together', note='Our house character',
              line='colour', eyes='lids', build='round', shade='cel', grain=True, rim=True),
}
DEFAULTS = dict(line='black', eyes='almond', build='box', shade='soft', grain=False, rim=False)


class StylePen(ed.Pen):
    """ed.py's pen, with the option of outlines in a darker shade of the fill instead of black."""

    def __init__(self, img, cam, o):
        super().__init__(img, cam)
        self.o = o

    def poly(self, pts, fill, line=INK, lw=4):
        if self.o['line'] == 'colour' and line == INK and fill is not None:
            line = tuple(int(c * 0.5) for c in fill[:3])
            lw *= 0.85
        super().poly(pts, fill, line, lw)


def shadow(img, cam, pts, colr, alpha, blur, o):
    if o['shade'] == 'cel':
        ed.soft(img, cam, pts, colr, alpha * 0.6, 0)
    else:
        ed.soft(img, cam, pts, colr, alpha, blur)


def figure(img, pen, cam, t, o):
    """ed.ed(), redrawn with the design options."""
    LW = 2.6
    rnd = o['build'] == 'round'
    x = 640 + 2.0 * math.sin(t * 0.7)
    sp = speaking(t)
    look_down = (int(t / 2.7) % 3 == 1) and sp is not None
    # guitar on his back (unchanged)
    pen.poly([(x - 70, 300), (x - 58, 296), (x - 120, 150), (x - 132, 155)], (128, 78, 44), INK, LW)
    pen.poly([(x - 140, 108), (x - 118, 104), (x - 114, 156), (x - 136, 158)], (72, 44, 28), INK, LW)
    for k in range(3):
        pen.ell(x - 143, 116 + k * 14, 3.5, 3, (215, 215, 215), INK, 1.5)
        pen.ell(x - 111, 114 + k * 14, 3.5, 3, (215, 215, 215), INK, 1.5)
    # legs and trainers (unchanged)
    for sgn in (-1, 1):
        leg = [(x + sgn * 6, 630), (x + sgn * 98, 630), (x + sgn * 96, 700), (x + sgn * 88, 780), (x + sgn * 82, 872),
               (x + sgn * 30, 874), (x + sgn * 24, 780), (x + sgn * 14, 690)]
        pen.poly(curve(leg, 5), TROUSER, INK, LW)
        shadow(img, cam, [(x + sgn * 70, 640), (x + sgn * 96, 640), (x + sgn * 84, 868), (x + sgn * 66, 868)],
               (0, 0, 0), 0.35, 6, o)
        shoe = [(x + sgn * 22, 872), (x + sgn * 84, 870), (x + sgn * 108, 880), (x + sgn * 118, 894),
                (x + sgn * 112, 904), (x + sgn * 20, 906), (x + sgn * 16, 890)]
        pen.poly(curve(shoe, 4), (244, 244, 242), INK, LW)
        pen.line([(x + sgn * 18, 900), (x + sgn * 114, 899)], (170, 170, 176), 3)
    # body: the tee. Round build: sloping shoulders, sleeves that taper, a softer hem.
    if rnd:
        tee = [(x - 56, 272), (x - 120, 300), (x - 168, 348), (x - 190, 424), (x - 148, 440), (x - 140, 410),
               (x - 144, 520), (x - 140, 640), (x + 140, 640), (x + 144, 520), (x + 140, 410), (x + 148, 440),
               (x + 190, 424), (x + 168, 348), (x + 120, 300), (x + 56, 272)]
        tee = curve(tee, 5)
    else:
        tee = [(x - 60, 268), (x - 128, 292), (x - 176, 330), (x - 196, 420), (x - 150, 436), (x - 140, 400),
               (x - 136, 640), (x + 136, 640), (x + 140, 400), (x + 150, 436), (x + 196, 420), (x + 176, 330),
               (x + 128, 292), (x + 60, 268)]
    pen.poly(tee, LILAC, INK, LW)
    shadow(img, cam, [(x + 60, 290), (x + 170, 330), (x + 190, 420), (x + 136, 640), (x + 70, 640), (x + 90, 400)],
           (120, 100, 170), 0.28, 10, o)
    pen.line([(x - 100, 300), (x + 110, 560)], (78, 54, 40), 6)
    # neck: round build is shorter and thicker, tapering into the shoulders
    if rnd:
        neck = [(x - 40, 238), (x + 40, 238), (x + 50, 282), (x - 50, 282)]
    else:
        neck = [(x - 34, 230), (x + 34, 230), (x + 38, 286), (x - 38, 286)]
    pen.poly(neck, SKIN, INK, LW)
    shadow(img, cam, [(neck[0][0], 240), (neck[1][0], 240), (neck[1][0] - 4, 262), (neck[0][0] + 4, 262)],
           (170, 110, 90), 0.35, 4, o)
    pen.line(oval(x, 266 if rnd else 262, 60, 22, 30, 0.15, math.pi - 0.15), INK, LW)
    # left arm hanging
    rng = np.random.default_rng(11)
    if rnd:  # a tapered, slightly bent arm and a mitten hand with a thumb
        arm = curve([(x - 188, 430), (x - 150, 440), (x - 152, 500), (x - 160, 572), (x - 186, 572), (x - 190, 500)], 5)
        pen.poly(arm, SKIN, INK, LW)
        for i in range(9):
            cx, cy = x - 172 + rng.uniform(-8, 8), 450 + i * 12
            pen.ell(cx, cy, rng.uniform(5, 9), rng.uniform(4, 6), TATS[i % 5], None, rot=rng.uniform(0, 3))
        hand = curve([(x - 188, 566), (x - 156, 566), (x - 150, 596), (x - 162, 616), (x - 182, 614), (x - 192, 592)], 5)
        pen.poly(hand, SKIN, INK, LW)
        pen.poly(curve([(x - 158, 578), (x - 146, 584), (x - 148, 600), (x - 158, 598)], 4), SKIN, INK, LW * 0.8)
    else:
        pen.poly([(x - 196, 420), (x - 150, 436), (x - 158, 560), (x - 190, 558)], SKIN, INK, LW)
        for i in range(9):
            cx, cy = x - 174 + rng.uniform(-10, 10), 446 + i * 12
            pen.ell(cx, cy, rng.uniform(6, 11), rng.uniform(4, 7), TATS[i % 5], None, rot=rng.uniform(0, 3))
        pen.poly([(x - 192, 556), (x - 156, 556), (x - 154, 592), (x - 170, 604), (x - 190, 592)], SKIN, INK, LW)
    # head
    hx, hy = x + 4, 150 + 1.2 * math.sin(t * 1.1)
    if rnd:  # pear-shaped: narrower crown, fuller cheeks and jowl
        head = curve([(hx - 62, hy - 70), (hx - 20, hy - 96), (hx + 24, hy - 96), (hx + 64, hy - 70), (hx + 76, hy - 10),
                      (hx + 82, hy + 40), (hx + 64, hy + 86), (hx, hy + 104), (hx - 64, hy + 86), (hx - 82, hy + 40),
                      (hx - 76, hy - 10)], 6)
        ears = [oval(hx + sgn * 78, hy + 4, 12, 22) for sgn in (-1, 1)]
    else:
        head = oval(hx, hy - 6, 74, 88, 40, math.pi, 2 * math.pi) + [
            (hx + 74, hy + 10), (hx + 66, hy + 58), (hx + 40, hy + 92), (hx, hy + 102), (hx - 40, hy + 92),
            (hx - 66, hy + 58), (hx - 74, hy + 10)]
        ears = [oval(hx + sgn * 76, hy + 6, 13, 24) for sgn in (-1, 1)]
    for e in ears:
        pen.poly(e, SKIN, INK, LW)
    pen.ell(hx + 78, hy + 6, 5, 6, INK, None)
    pen.line([(hx + 80, hy + 12), (hx + 86, hy + 80), (hx + 90, 260)], INK, 1.6)
    pen.poly(head, SKIN, INK, LW)
    shadow(img, cam, [(hx + 30, hy - 60), (hx + 74, hy - 10), (hx + 70, hy + 58), (hx + 40, hy + 92), (hx + 30, hy + 30)],
           (190, 120, 100), 0.32, 8, o)
    if rnd:
        hair = [(hx - 70, hy - 20), (hx - 70, hy - 58), (hx - 46, hy - 90), (hx - 6, hy - 106), (hx + 40, hy - 100),
                (hx + 68, hy - 70), (hx + 74, hy - 22), (hx + 60, hy - 44), (hx + 30, hy - 62), (hx - 14, hy - 66),
                (hx - 48, hy - 56), (hx - 62, hy - 38)]
    else:
        hair = [(hx - 74, hy - 8), (hx - 76, hy - 50), (hx - 56, hy - 86), (hx - 10, hy - 102), (hx + 40, hy - 98),
                (hx + 72, hy - 70), (hx + 76, hy - 14), (hx + 64, hy - 40), (hx + 34, hy - 62), (hx - 10, hy - 68),
                (hx - 50, hy - 58), (hx - 66, hy - 34)]
    pen.poly(curve(hair), GINGER, INK, LW)
    for k in range(4):
        pen.line([(hx - 40 + 26 * k, hy - 92 + 4 * k), (hx - 30 + 26 * k, hy - 70 + 3 * k)], GINGER_D, 2)
    for k in range(2):
        pen.line([(hx - 30, hy - 44 + 9 * k), (hx - 6, hy - 48 + 9 * k), (hx + 24, hy - 45 + 9 * k)], SKIN_D, 1.8)
    # eyes
    blink = (t % 3.9) < 0.12
    for sgn in (-1, 1):
        ex, ey = hx - 8 + sgn * 30, hy - 8
        if blink:
            pen.line([(ex - 16, ey), (ex, ey + 3), (ex + 16, ey)], INK, 2.4)
            continue
        if o['eyes'] == 'lids':
            # a rounder eye, a blue iris, and a heavy skin-coloured lid over the top half: sincere, tired
            pen.ell(ex, ey + 1, 16, 10, (250, 250, 248), INK, 1.8)
            pen.ell(ex - 2, ey + 3, 6.5, 6.5, (80, 124, 170), None)
            pen.ell(ex - 2, ey + 3, 3, 3, INK, None)
            lid = [(ex - 18, ey + 1), (ex - 16, ey - 8), (ex, ey - 12), (ex + 16, ey - 8), (ex + 18, ey + 1),
                   (ex + 8, ey - 1), (ex - 8, ey - 1)]
            pen.poly(curve(lid, 4), SKIN_D, INK, 1.8)
            pen.line([(ex - 10, ey + 14), (ex, ey + 16), (ex + 10, ey + 14)], SKIN_D, 1.5)  # a tired crease below
            pen.line([(ex - sgn * 2, ey - 26), (ex + sgn * 20, ey - 19)], GINGER_D, 4.4)
        else:
            almond = [(ex - 17, ey), (ex - 8, ey - 8), (ex + 8, ey - 8), (ex + 17, ey), (ex + 8, ey + 7), (ex - 8, ey + 7)]
            pen.poly(almond, (250, 250, 248), INK, 2.0)
            py = ey + (3 if look_down else -1)
            pen.ell(ex - 3, py, 4.5, 4.5, INK, None)
            lid = 3 if look_down else 0
            pen.line([(ex - 17, ey - 1 + lid), (ex - 8, ey - 9 + lid), (ex + 8, ey - 9 + lid), (ex + 17, ey - 1 + lid)],
                     INK, 2.6)
            pen.line([(ex - sgn * 4, ey - 24), (ex + sgn * 20, ey - 18)], GINGER_D, 3.2)
    nose_col = tuple(int(c * 0.6) for c in SKIN) if o['line'] == 'colour' else INK
    pen.line([(hx - 4, hy - 4), (hx - 12, hy + 26), (hx - 6, hy + 32), (hx + 6, hy + 30)], nose_col, 2.0)
    pen.line([(hx - 16, hy + 30), (hx - 12, hy + 33)], nose_col, 1.6)
    rng = np.random.default_rng(5)
    for i in range(55):
        a = rng.uniform(0.3, math.pi - 0.3)
        r = rng.uniform(0.6, 0.95)
        sx, sy = hx + 64 * r * math.cos(a), hy + 30 + 66 * r * math.sin(a)
        if abs(sx - hx + 4) < 24 and hy + 48 < sy < hy + 84:
            continue
        pen.ell(sx, sy, 0.9, 0.9, (196, 128, 92), None)
    m = mouth_shape(t)
    mx, my = hx - 4, hy + 60
    if m == 0:
        pen.line([(mx - 16, my + 2), (mx, my), (mx + 16, my + 3)], INK, 2.4)
    else:
        h = {1: 7, 2: 13, 3: 18}[m]
        w = {1: 15, 2: 17, 3: 14}[m]
        pen.poly([(mx - w, my - 2), (mx + w, my - 3), (mx + w * 0.7, my + h), (mx - w * 0.7, my + h)], (70, 26, 30), INK, 2.2)
        if m >= 2:
            pen.poly([(mx - w * 0.8, my - 1), (mx + w * 0.8, my - 2), (mx + w * 0.7, my + 3), (mx - w * 0.7, my + 3)],
                     (245, 245, 240), None)
    ed.glow(img, cam, hx, hy + 90, 80, (170, 190, 240), 0.14)
    if o['rim']:  # cranberry rim light down his shadow side (head and tee), under the raised arm
        rim = Image.new('RGBA', img.size, (0, 0, 0, 0))
        rp = ed.Pen(rim, cam)
        for q in ([p for p in head if p[0] > hx + 34], [p for p in tee if p[0] > x + 60 and p[1] < 600]):
            if len(q) > 2:
                rp.line(q, (236, 70, 100), 3.6)
        img.alpha_composite(rim.filter(ImageFilter.GaussianBlur(cam.S(4))))
        img.alpha_composite(rim)
    # right arm up to the mic
    ex2, ey2 = x + 236, 478
    hx2, hy2 = hx + 78, hy + 112
    if rnd:
        upper = curve([(x + 150, 436), (x + 192, 420), (ex2 + 16, ey2 - 6), (ex2 + 6, ey2 + 18), (ex2 - 16, ey2 + 10)], 5)
        fore = curve([(ex2 - 16, ey2 + 12), (ex2 + 18, ey2 - 4), (hx2 + 16, hy2 - 2), (hx2 - 10, hy2 + 14)], 5)
        pen.poly(upper, SKIN, INK, LW)
        pen.poly(fore, SKIN, INK, LW)
    else:
        pen.poly([(x + 152, 432), (x + 196, 418), (ex2 + 18, ey2 - 4), (ex2 - 14, ey2 + 12)], SKIN, INK, LW)
        pen.ell(ex2 + 2, ey2 + 4, 19, 17, SKIN, INK, LW)
        pen.poly([(ex2 - 14, ey2 + 12), (ex2 + 18, ey2 - 6), (hx2 + 18, hy2 - 6), (hx2 - 12, hy2 + 14)], SKIN, INK, LW)
    for i in range(6):
        q = (i + 0.5) / 6
        pen.ell(ex2 + (hx2 - ex2) * q + 2, ey2 + (hy2 - ey2) * q, 8, 5, TATS[(i + 2) % 5], None, rot=-0.9)
    mx2, my2 = hx + 22, hy + 70
    pen.poly([(hx2 - 6, hy2 + 16), (hx2 + 8, hy2 + 10), (mx2 + 8, my2 + 4), (mx2 - 6, my2 + 10)], (28, 28, 32), INK, 2)
    pen.ell(mx2, my2 + 4, 11, 10, (70, 70, 76), INK, 2)
    if rnd:  # fingers wrapped round the mic, a thumb on top
        fist = curve([(hx2 - 18, hy2 - 6), (hx2 + 12, hy2 - 16), (hx2 + 24, hy2 + 4), (hx2 + 12, hy2 + 24),
                      (hx2 - 14, hy2 + 22)], 5)
        pen.poly(fist, SKIN, INK, LW)
        pen.poly(curve([(hx2 - 16, hy2 - 4), (hx2 - 6, hy2 - 20), (hx2 + 4, hy2 - 16), (hx2 - 4, hy2 - 2)], 4), SKIN, INK,
                 LW * 0.8)
        for k in range(2):
            pen.line([(hx2 + 2, hy2 + 2 + 8 * k), (hx2 + 20, hy2 - 2 + 8 * k)], SKIN_D, 1.4)
    else:
        pen.poly([(hx2 - 18, hy2 - 8), (hx2 + 16, hy2 - 14), (hx2 + 22, hy2 + 12), (hx2 - 12, hy2 + 22)], SKIN, INK, LW)
        for k in range(3):
            pen.line([(hx2 - 14, hy2 - 2 + 7 * k), (hx2 + 16, hy2 - 7 + 7 * k)], SKIN_D, 1.4)


def frame(t, o):
    """One widescreen frame exactly as ed.py builds it, with the redesigned figure and no caption."""
    cam = Cam(t)
    img = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 255))
    ed.stage(img, ed.Pen(img, cam), cam, t)
    img = img.filter(ImageFilter.GaussianBlur(cam.S(5)))
    ed.spotlight(img, cam)
    fig = Image.new('RGBA', img.size, (0, 0, 0, 0))
    figure(fig, StylePen(fig, cam, o), cam, t, o)
    if o['grain']:  # faint print grain on the figure only
        a = np.asarray(fig).astype(np.float32)
        rng = np.random.default_rng(3)
        g = rng.normal(0, 1, a.shape[:2]).astype(np.float32)
        g = np.asarray(Image.fromarray(((g * 0.5 + 2) * 60).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)),
                       np.float32) / 60 - 2
        a[..., :3] *= (1 + 0.07 * g)[..., None]
        fig = Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')
    img.alpha_composite(fig)
    front = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ed.audience(front, ed.Pen(front, cam), cam, t)
    img.alpha_composite(front.filter(ImageFilter.GaussianBlur(cam.S(4))))
    return img.convert('RGB').resize((W, H), Image.LANCZOS)


def vertical(wide, text):
    """The TikTok conversion from tiktok-design.md: picture a third larger than fitting the width, centred and
    untouched; above and below, a heavy blur of its own top and bottom edges fading to the background;
    the caption drawn fresh, wrapped to 800 px, centred on x = 480, just below the picture."""
    VW, VH = 1080, 1920
    s = VW / W * 1.333
    pw, ph = int(W * s), int(H * s)
    pic = wide.resize((pw, ph), Image.LANCZOS).crop(((pw - VW) // 2, 0, (pw - VW) // 2 + VW, ph))
    top = (VH - ph) // 2
    out = Image.new('RGB', (VW, VH), (8, 8, 12))
    for edge, y0, flip in ((pic.crop((0, 0, VW, 40)), 0, True), (pic.crop((0, ph - 40, VW, ph)), top + ph, False)):
        band = edge.resize((VW, top)).filter(ImageFilter.GaussianBlur(40))
        a = np.asarray(band, np.float32)
        ramp = np.linspace(0, 1, top, dtype=np.float32)[:, None, None]
        if flip:
            ramp = ramp[::-1]
        fade = (1 - ramp) ** 1.5
        a = a * (1 - (1 - fade)) + np.array([8, 8, 12], np.float32) * (1 - fade)
        out.paste(Image.fromarray(a.clip(0, 255).astype(np.uint8)), (0, y0))
    out.paste(pic, (0, top))
    d = ImageDraw.Draw(out)
    font = ImageFont.truetype(FONT, 60)
    d.text((480, top + ph + 60), text, font=font, fill=(255, 255, 255), anchor='mm', stroke_width=6,
           stroke_fill=(0, 0, 0))
    return out, top


def sheet(out, current, stills_dir, pick):
    tw, th = 420, 747
    fc = 420  # face close-up size
    pad, head, lab = 36, 190, 110
    cols = 3
    Wd = cols * tw + (cols + 1) * pad
    rowh = th + 12 + fc + lab
    Hd = head + 2 * rowh + 3 * pad
    s = Image.new('RGB', (Wd, Hd), (24, 22, 28))
    d = ImageDraw.Draw(s)
    d.text((pad, 34), 'LISTENING & LEARNING - SUBTLE REDESIGNS', font=ImageFont.truetype(TITLE_FONT, 60), fill=CRANBERRY)
    f1, f2 = ImageFont.truetype(FONT, 28), ImageFont.truetype(FONT, 20)
    d.text((pad, 120), 'Same look, stage, pose and camera. Only the character design changes.', font=f2,
           fill=(200, 196, 206))
    d.text((pad, 148), '"It is my belief" (17.5 s), 1080 x 1920 TikTok frame, with a close-up of the face below each.',
           font=f2, fill=(160, 156, 170))
    panels = [('Current', 'As posted', Image.open(current).convert('RGB'))]
    for k, v in VARIANTS.items():
        panels.append((v['name'], v['note'], Image.open(os.path.join(stills_dir, f'variant_{k}.png')).convert('RGB')))
    for i, (name, note, im) in enumerate(panels):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = head + pad + r * (rowh + pad)
        s.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
        face = im.crop((340, 560, 740, 960)).resize((fc, fc), Image.LANCZOS)
        s.paste(face, (x, y + th + 12))
        chosen = name.startswith(pick + '.')
        if chosen:
            d.rectangle([x - 6, y - 6, x + tw + 5, y + th + 12 + fc + 5], outline=CRANBERRY, width=6)
            d.rectangle([x, y + 14, x + 230, y + 58], fill=CRANBERRY)
            d.text((x + 12, y + 20), 'RECOMMENDED', font=f2, fill=(255, 255, 255))
        d.text((x, y + th + fc + 26), name, font=f1, fill=(255, 120, 140) if chosen else (240, 238, 244))
        d.text((x, y + th + fc + 66), note, font=f2, fill=(170, 166, 178))
    s.save(out, quality=88)


def main():
    mode = sys.argv[1]
    if mode == 'stills':
        outd = sys.argv[2]
        t = float(sys.argv[3]) if len(sys.argv) > 3 else 17.5
        os.makedirs(outd, exist_ok=True)
        for k, v in VARIANTS.items():
            o = dict(DEFAULTS, **{kk: vv for kk, vv in v.items() if kk in DEFAULTS})
            img, _ = vertical(frame(t, o), 'It is my belief')
            img.save(os.path.join(outd, f'variant_{k}.png'), optimize=True)
            print('done', k, flush=True)
    elif mode == 'sheet':
        sheet(*sys.argv[2:6])


if __name__ == '__main__':
    main()
