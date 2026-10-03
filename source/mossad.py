#!/usr/bin/env python3
"""Mossad: a coffee-shop parody for TikTok (prompts/mossad.md).

A customer orders a caramel latte; the cashier, smiling, recites state talking points like a loyalty-card offer;
the order buzzer of the man waiting behind him goes off. Same look as Hope Again and The Patriots (burnham.py,
peepee.py): flat shapes, clean black outlines, almond eyes with small pupils, soft shading, deadpan staging, a
still camera and hard cuts. Made vertical (1080 x 1920); faces and text inside TikTok's safe area
(x 60-900, y 310-1500).

Everyone is invented. Coffee Queens is a made-up shop with its own made-up crown-and-cup sign. The only national
symbol is the flag printed on the cups. No real brands on anything.

One shared set: the front of house (window, patrons, the queue) is one drawing seen by camera 'front' (shots 1, 3,
5: the close shots are that camera zoomed in); the back of house (machine, cups, menu) is one drawing seen by
camera 'back' (shots 2 and 4). Seen from the staff side the croissants are on the left and the card machine on the
right; from the customer's side, mirrored. The customer always looks screen-left, the cashier screen-right.

Usage:
    python3 mossad.py stills OUT_DIR T1 T2 ...    frames at those times (seconds), full size
    python3 mossad.py sheet OUT.jpg               the storyboard sheet (one still per shot, cups and buzzer close-ups)
    python3 mossad.py animatic OUT.mp4            half size, quick, to check timing
    python3 mossad.py final OUT.mp4               full size
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import burnham as B
import peepee as PP          # lips, lashes, Rot, ctext; the series' caption
import mossad_audio as MA
from burnham_film import onepole_lp, normal
from ed import INK, curve, oval, smooth, soft

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 12
SR = 48000
TITLE = 'MOSSAD'

# palette
WOOD = (224, 198, 160)
WOOD_D = (196, 164, 122)
WHITE = (246, 245, 241)
WALL = (238, 236, 230)
TILE = (244, 244, 240)
PLANT = (78, 138, 86)
PLANT_D = (50, 100, 62)
FLAG_BLUE = (0, 56, 184)
CHROME = (196, 202, 210)
CHROME_D = (120, 128, 138)
APRON = (44, 92, 168)
BLUE_HAIR = (64, 120, 214)
NAVY_LIGHT = (66, 86, 132)
COAT = (196, 182, 154)
SUIT = (62, 64, 72)
BUZZ = (30, 30, 34)

# ------------------------------------------------------------------------------------------- timeline
# Each line: (who, film time the clip starts, recording, from, to in the recording, caption pieces).
# Caption pieces are (film time, text); a piece stays until the next piece or the end of the line.
# Words follow Sam's recordings, not the script.
LINES = [
    ('cust', 0.22, 'mossad-customer-1', 0.70, 3.62,
     [(0.30, 'Hi, can I please order a latte with caramel syrup?')]),
    ('cash', 3.27, 'mossad-cashier-1', 0.28, 5.20,
     [(3.35, 'Of course you can, and just so you know,'), (5.98, 'Israel has the right to defend itself.')]),
    ('cust', 8.47, 'mossad-customer-2', 0.50, 2.95,
     [(8.55, 'Errm...'), (10.15, 'Errm... excuse me?')]),
    ('cash', 11.02, 'mossad-cashier-2', 0.42, 2.12,
     [(11.10, 'Nothing to worry about, sir.')]),
    ('cash', 12.68, 'mossad-cashier-2', 2.28, 5.58,
     [(12.86, 'Coffee Queens is actually doing a promotion'), (14.80, 'at the moment with Mossad.')]),
    ('cash', 16.03, 'mossad-cashier-3', 0.12, 5.00,
     [(16.10, 'Did you know that October 7th'), (17.95, 'was, like, eleven 9/11s?')]),
    ('cash', 21.02, 'mossad-cashier-4', 0.00, 6.20,
     [(21.04, "And it's just my opinion,"), (22.95, 'but if you start a war,'),
      (25.15, "you shouldn't complain when you can't finish it.")]),
    ('cust2', 27.62, 'mossad-customer2-1', 0.38, 2.20,
     [(27.70, 'Hey, my drink is ready!')]),
]
SHOTS = [('front', 0.0, 3.15), ('back', 3.15, 8.35), ('cust', 8.35, 10.95), ('back2', 10.95, 27.28),
         ('cust', 27.28, 99)]
FLASH = 27.40          # the buzzer's light starts flashing
RATTLE = 29.20         # flashing faster, rattling in his palm
BANG = 29.42           # the explosion
BLACK_AT = 29.74       # hard cut to black, about three-quarters of the way through the blast
DUR = 30.10
SIP = 29.05            # patron 2 calmly sips his espresso in the last moment before the bang


def _clip_level():
    """Loudness envelopes (100 a second) of each placed clip, from the cleaned recordings."""
    out = []
    for who, at, name, s0, s1, _ in LINES:
        a = MA.line(name)[int(s0 * SR):int(s1 * SR)]
        hop = SR // 100
        lv = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
        out.append(np.clip(lv / (np.percentile(lv, 95) + 1e-9), 0, 1))
    return out


_LV = None


def level(who, t):
    """How loud this person's voice is at film time t (0-1); the mouth opens a frame ahead of the sound."""
    global _LV
    if _LV is None:
        _LV = _clip_level()
    t += 1.0 / FPS
    for (w, at, _, s0, s1, _), lv in zip(LINES, _LV):
        if w == who and at <= t < at + (s1 - s0):
            return float(lv[min(int((t - at) * 100), len(lv) - 1)])
    return 0.0


def talk_mouth(lv, t, smile=False):
    if smile:
        return 'sm_rest' if lv < 0.1 else 'sm_small' if lv < 0.32 else ['sm_mid', 'sm_open'][int(t * 12) % 2]
    return 'line' if lv < 0.1 else 'small' if lv < 0.32 else ['mid', 'open'][int(t * 12) % 2]


def blinking(t, times, d=0.12):
    return any(b <= t < b + d for b in times)


# ------------------------------------------------------------------------------------- drawing extras
_face, _mouth, _beard, _hair_back, _hair_front, _torso = B.face, B.mouth, B.beard, B.hair_back, B.hair_front, B.torso


def face(img, p, sp, t, hx, hy, hw, hh):
    br = sp.get('brows')
    mine = br in ('alarm', 'confused', 'outrage', 'weary')
    q = dict(sp, brows=None, brow_c=sp['skin']) if mine else sp
    fx = _face(img, p, q, t, hx, hy, hw, hh)
    bc = sp.get('brow_c', (60, 44, 34))
    bw = sp.get('brow_w', 3.2)
    skin_d = B.dk(sp['skin'], 0.86)
    if mine:
        for sgn in (-1, 1):
            ex, ey = fx - 4 + sgn * 30, hy - 8
            if br == 'weary':        # level, a little heavy
                p.line([(ex - sgn * 6, ey - 20), (ex + sgn * 8, ey - 22), (ex + sgn * 21, ey - 19)], bc, bw)
            elif br == 'alarm':      # inner ends pulled up and together: alarm and confusion
                p.line([(ex - sgn * 7, ey - 32), (ex + sgn * 6, ey - 31), (ex + sgn * 21, ey - 23)], bc, bw)
            elif br == 'outrage':    # both raised high, inner ends highest: offended disbelief
                p.line([(ex - sgn * 7, ey - 38), (ex + sgn * 6, ey - 37), (ex + sgn * 22, ey - 29)], bc, bw)
            elif br == 'confused':   # one brow up, the other down
                up = sgn > 0
                if up:
                    p.line([(ex - sgn * 6, ey - 26), (ex + sgn * 6, ey - 36), (ex + sgn * 21, ey - 30)], bc, bw)
                else:
                    p.line([(ex - sgn * 6, ey - 17), (ex + sgn * 8, ey - 20), (ex + sgn * 21, ey - 19)], bc, bw)
        if br in ('alarm', 'outrage'):  # creases between and above the brows
            p.line([(fx - 6, hy - 46), (fx - 4, hy - 34)], skin_d, 1.8)
            p.line([(fx - 22, hy - 54), (fx - 4, hy - 58), (fx + 14, hy - 54)], skin_d, 1.6)
            if br == 'outrage':
                p.line([(fx - 26, hy - 64), (fx - 4, hy - 68), (fx + 18, hy - 64)], skin_d, 1.6)
    if sp.get('piercing'):  # a small, neat silver ring at the nostril
        p.line(oval(fx - 15, hy + 33, 4.5, 4.5, 14, -0.6, 2.2), (196, 200, 210), 1.8)
    return fx


def mouth(p, sp, t, fx, my):
    m = sp.get('mouth', 'line')
    lip = sp.get('lip_c', (198, 96, 104))
    if m == 'agape':  # hanging a little open in offended outrage
        p.poly(curve([(fx - 13, my), (fx, my - 2), (fx + 13, my), (fx + 9, my + 17), (fx, my + 21), (fx - 9, my + 17)], 4),
               (70, 26, 30), INK, 2.2)
        return
    if m == 'pleased':
        p.line([(fx - 20, my - 3), (fx - 8, my + 6), (fx + 8, my + 6), (fx + 20, my - 3)], INK, 2.4)
        return
    if m.startswith('sm_'):  # the bright customer-service smile, talking through it
        h = {'sm_rest': 0, 'sm_small': 6, 'sm_mid': 11, 'sm_open': 16}[m]
        if h == 0:
            p.poly(curve([(fx - 24, my - 6), (fx, my + 4), (fx + 24, my - 6), (fx, my + 10)], 4), lip, INK, 2.0)
            p.line([(fx - 22, my - 5), (fx, my + 4), (fx + 22, my - 5)], INK, 2.2)
        else:
            pts = curve([(fx - 24, my - 6), (fx, my - 2), (fx + 24, my - 6), (fx + 14, my + 6 + h), (fx, my + 9 + h),
                         (fx - 14, my + 6 + h)], 4)
            p.poly(pts, (90, 30, 40), lip, 3.4)
            p.poly([(fx - 18, my - 3), (fx + 18, my - 3), (fx + 14, my + 3), (fx - 14, my + 3)], (250, 250, 246), None)
        for sgn in (-1, 1):  # dimples at the corners
            p.line([(fx + sgn * 25, my - 9), (fx + sgn * 28, my - 3)], B.dk(sp['skin'], 0.8), 1.6)
        return
    _mouth(p, sp, t, fx, my)


def beard(p, sp, hx, hy, hw, hh, fx):
    if sp.get('beard') != 'trim':
        return _beard(p, sp, hx, hy, hw, hh, fx)
    c = sp.get('beard_c', (90, 80, 74))
    cd = B.dk(c, 0.78)
    # short, neat, following the jaw; a tidy moustache; the mouth drawn on top
    pts = [(hx - hw - 1, hy - 6), (hx - hw * 0.98, hy + hh * 0.62), (hx - hw * 0.62, hy + hh * 1.08),
           (fx, hy + hh * 1.26), (hx + hw * 0.62, hy + hh * 1.08), (hx + hw * 0.98, hy + hh * 0.62),
           (hx + hw + 1, hy - 6), (hx + hw * 0.84, hy + 22), (hx + hw * 0.6, hy + 48), (fx + 26, hy + 76),
           (fx, hy + 86), (fx - 26, hy + 76), (hx - hw * 0.6, hy + 48), (hx - hw * 0.84, hy + 22)]
    p.poly(curve(pts, 5), c, INK, 2.2)
    p.poly(curve([(fx - 30, hy + 52), (fx - 6, hy + 42), (fx + 6, hy + 42), (fx + 30, hy + 52), (fx + 18, hy + 58),
                  (fx - 18, hy + 58)], 4), c, INK, 1.8)
    for k in range(7):  # a little salt and pepper texture
        x = fx - 48 + 16 * k
        p.line([(x, hy + hh * 0.86), (x + 2, hy + hh * 0.98)], cd, 1.4)
        p.line([(x + 6, hy + hh * 0.92), (x + 7, hy + hh * 1.02)], (176, 172, 168), 1.4)


def hair_back(p, sp, hx, hy, hw, hh):
    st, c = sp.get('hair'), sp.get('hair_c', (60, 44, 34))
    if st == 'wavy':  # loose waves past the shoulders
        pts = [(hx - hw - 10, hy - 50)]
        for k in range(7):
            pts.append((hx - hw - 22 - 10 * (k % 2), hy - 20 + 34 * k))
        pts += [(hx - hw + 4, hy + 240), (hx + hw - 4, hy + 240)]
        for k in range(6, -1, -1):
            pts.append((hx + hw + 22 + 10 * (k % 2), hy - 20 + 34 * k))
        pts += [(hx + hw + 10, hy - 50), (hx, hy - hh - 16)]
        p.poly(curve(pts, 4), c, INK, 2.6)
        return
    if st == 'afro':  # short natural hair, greying
        p.poly(curve(oval(hx, hy - 34, hw + 30, hh + 32, 18), 3), c, INK, 2.6)
        return
    return _hair_back(p, sp, hx, hy, hw, hh)


def hair_front(p, sp, hx, hy, hw, hh, fx):
    st = sp.get('hair')
    c = sp.get('hair_c', (60, 44, 34))
    cd = B.dk(c, 0.72)
    if st == 'wavy':
        part = fx + hw * 0.18
        hair = [(hx - hw - 10, hy + 40), (hx - hw - 14, hy - 40), (hx - hw * 0.72, hy - hh * 1.04), (part, hy - hh * 1.16),
                (hx + hw * 0.74, hy - hh * 1.04), (hx + hw + 14, hy - 40), (hx + hw + 10, hy + 40),
                (hx + hw * 0.84, hy - 6), (part + hw * 0.42, hy - hh * 0.7), (part, hy - hh * 0.9),
                (part - hw * 0.5, hy - hh * 0.66), (hx - hw * 0.84, hy - 6)]
        p.poly(curve(hair), c, INK, 2.6)
        hl = B.lt(c, 1.3)
        for sgn in (-1, 1):  # the waves
            for k in range(3):
                x0 = hx + sgn * (hw * 0.55 + 10 * k)
                p.line([(x0, hy - hh * 0.8 + 14 * k), (x0 + sgn * 10, hy - hh * 0.5 + 14 * k),
                        (x0 + sgn * 2, hy - hh * 0.2 + 14 * k)], cd, 1.8)
        p.line([(part - 30, hy - hh * 1.02), (part - 6, hy - hh * 1.1)], hl, 3.0)
        return
    if st == 'slick':  # slicked back, glossy
        hair = [(hx - hw, hy - 16), (hx - hw - 2, hy - 60), (hx - hw * 0.7, hy - hh * 1.04), (hx, hy - hh * 1.2),
                (hx + hw * 0.7, hy - hh * 1.04), (hx + hw + 2, hy - 60), (hx + hw, hy - 16), (hx + hw * 0.86, hy - 50),
                (hx + hw * 0.4, hy - hh * 0.76), (hx - hw * 0.4, hy - hh * 0.76), (hx - hw * 0.86, hy - 50)]
        p.poly(curve(hair), c, INK, 2.4)
        for k in range(4):
            x = hx - hw * 0.5 + k * hw * 0.33
            p.line([(x, hy - hh * 0.8), (x - 4, hy - hh * 1.1)], B.lt(c, 1.9), 1.6)
        p.ell(hx + hw * 0.25, hy - hh * 0.98, hw * 0.24, hh * 0.05, B.lt(c, 2.6), None, rot=0.15)
        return
    if st == 'beanie':  # a knitted beanie pulled down to the brow
        bc = sp.get('beanie_c', (204, 150, 48))
        cap = curve([(hx - hw - 6, hy - 30), (hx - hw - 4, hy - hh * 0.8), (hx - hw * 0.5, hy - hh * 1.3), (hx, hy - hh * 1.38),
                     (hx + hw * 0.5, hy - hh * 1.3), (hx + hw + 4, hy - hh * 0.8), (hx + hw + 6, hy - 30)], 4)
        p.poly(cap, bc, INK, 2.6)
        p.poly([(hx - hw - 8, hy - 62), (hx + hw + 8, hy - 62), (hx + hw + 8, hy - 28), (hx - hw - 8, hy - 28)], B.dk(bc, 0.9),
               INK, 2.4)
        for k in range(-5, 6):
            p.line([(hx + k * 13, hy - 58), (hx + k * 13, hy - 32)], B.dk(bc, 0.72), 1.4)
            p.line([(hx + k * 12, hy - hh * 1.2 + abs(k) * 4), (hx + k * 13, hy - 70)], B.dk(bc, 0.8), 1.2)
        return
    if st == 'afro':
        top = curve([(hx - hw - 8, hy - 20), (hx - hw - 10, hy - hh * 0.8), (hx - hw * 0.5, hy - hh * 1.24), (hx, hy - hh * 1.32),
                     (hx + hw * 0.5, hy - hh * 1.24), (hx + hw + 10, hy - hh * 0.8), (hx + hw + 8, hy - 20),
                     (hx + hw * 0.8, hy - hh * 0.62), (hx, hy - hh * 0.78), (hx - hw * 0.8, hy - hh * 0.62)], 4)
        p.poly(top, c, INK, 2.4)
        rng = np.random.default_rng(11)
        for _ in range(26):  # coils, some grey
            a = rng.uniform(math.pi * 1.05, math.pi * 1.95)
            r = rng.uniform(0.7, 1.15)
            x, y = hx + hw * r * math.cos(a), hy - hh * 0.4 + hh * 0.9 * r * math.sin(a)
            p.ell(x, y, 4, 4, (178, 176, 172) if rng.random() < 0.4 else B.lt(c, 1.6), None)
        return
    return _hair_front(p, sp, hx, hy, hw, hh, fx)


def torso(img, p, sp, t):
    _torso(img, p, sp, t)
    sw, bottom = sp.get('shoulders', 150), sp.get('bottom', 560)
    if sp.get('coat'):  # a light, open coat over the suit
        cc = sp['coat']
        for sgn in (-1, 1):
            p.poly([(sgn * 50, -6), (sgn * sw * 0.8, 10), (sgn * sw, 50), (sgn * (sw + 8), 200), (sgn * (sw - 2), bottom),
                    (sgn * 70, bottom), (sgn * 60, 250), (sgn * 66, 120)], cc, INK, 2.6)
            p.poly([(sgn * 52, -8), (sgn * 98, 20), (sgn * 72, 120), (sgn * 92, 150), (sgn * 64, 250), (sgn * 64, 120)],
                   B.dk(cc, 0.9), INK, 2.2)
        soft(img, p.cam, [(sw * 0.5, 30), (sw, 60), (sw, bottom), (sw * 0.6, bottom)], (0, 0, 0), 0.2, 10)
    if sp.get('apron'):  # a blue bib apron over the shirt, the shop's name small on the chest
        ac = sp['apron']
        p.poly([(-70, 70), (70, 70), (86, 230), (sw - 10, 250), (sw - 6, bottom), (-sw + 6, bottom), (-sw + 10, 250),
                (-86, 230)], ac, INK, 2.4)
        for sgn in (-1, 1):
            p.line([(sgn * 60, 72), (sgn * 40, -4)], ac, 7)
        p.poly([(-60, 300), (60, 300), (60, 380), (-60, 380)], B.dk(ac, 0.88), INK, 1.8)  # the front pocket
        if sp.get('apron_name'):
            PP.ctext(img, p.cam, 0, 132, 'COFFEE', 15, (236, 236, 240))
            PP.ctext(img, p.cam, 0, 150, 'QUEENS', 15, (236, 236, 240))
            crown_mark(p, 0, 106, 13, (236, 236, 240))
    if sp.get('tee'):  # a T-shirt: crew neck, short sleeves drawn with the arms
        p.line(oval(0, -2, 46, 20, 24, 0.2, math.pi - 0.2), INK, 2.4)


B.face, B.mouth, B.beard, B.hair_back, B.hair_front, B.torso = face, mouth, beard, hair_back, hair_front, torso


def crown_mark(p, x, y, r, colr):
    """Coffee Queens' made-up sign: a small three-point crown."""
    p.poly([(x - r, y + r * 0.5), (x - r, y - r * 0.4), (x - r * 0.5, y + r * 0.05), (x, y - r * 0.7), (x + r * 0.5, y + r * 0.05),
            (x + r, y - r * 0.4), (x + r, y + r * 0.5)], colr, None)


def flag(img, cam, x, y, w, h):
    """The national flag as printed on the cups: white, two blue stripes, the blue star in outline."""
    p = B.Pen(img, cam)
    p.poly([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)], (252, 252, 252),
           (150, 150, 160) if w * cam.s > 6 else None, 0.8)
    for sy in (-1, 1):
        y0 = y + sy * h * 0.34
        p.poly([(x - w / 2, y0 - h * 0.075), (x + w / 2, y0 - h * 0.075), (x + w / 2, y0 + h * 0.075),
                (x - w / 2, y0 + h * 0.075)], FLAG_BLUE, None)
    r = h * 0.2
    lw = max(0.5, h * 0.035 / max(0.25, cam.s) ** 0.6 / 0.75 * cam.s)
    for a0 in (-math.pi / 2, math.pi / 2):
        tri = [(x + r * math.cos(a0 + k * 2 * math.pi / 3), y + r * math.sin(a0 + k * 2 * math.pi / 3)) for k in range(3)]
        p.line(tri + tri[:1], FLAG_BLUE, lw)


def takeaway_cup(img, cam, x, y, h, lid=False):
    """A large takeaway cup (bottom centre at x, y), white, printed with the flag."""
    p = B.Pen(img, cam)
    w0, w1 = h * 0.34, h * 0.46
    p.poly([(x - w0, y), (x + w0, y), (x + w1, y - h), (x - w1, y - h)], WHITE, INK, 2.0)
    soft(img, cam, [(x + w0 * 0.4, y - 2), (x + w0, y - 2), (x + w1, y - h + 2), (x + w1 * 0.5, y - h + 2)], (0, 0, 0), 0.12, 2)
    p.poly([(x - w1 - 2, y - h), (x + w1 + 2, y - h), (x + w1 + 2, y - h - h * 0.06), (x - w1 - 2, y - h - h * 0.06)],
           (236, 236, 232), INK, 1.6)
    if lid:
        p.poly(curve([(x - w1 - 4, y - h - h * 0.05), (x + w1 + 4, y - h - h * 0.05), (x + w1 - 4, y - h - h * 0.16),
                      (x - w1 + 4, y - h - h * 0.16)], 3), (40, 40, 44), INK, 1.6)
    flag(img, cam, x, y - h * 0.5, h * 0.5, h * 0.36)


def cup_stack(img, cam, x, y, h, n, flag_on=True):
    """A stack of 12 oz takeaway cups, upside down (wide end down) and nested; the rim of each cup shows as a
    ridge. Only the top cup's print can be seen: the flag. Bottom centre at x, y; h is one cup's height."""
    p = B.Pen(img, cam)
    step = h * 0.13
    rim_top = y - (n - 1) * step          # the rim of the top cup
    base = rim_top - h                    # its upturned base
    wb, wr = h * 0.33, h * 0.45           # half-widths at base and rim
    slope = (wr - wb) / h
    p.poly([(x - wb, base), (x + wb, base), (x + wr + (n - 1) * step * slope, y), (x - wr - (n - 1) * step * slope, y)],
           WHITE, INK, 1.8)
    for k in range(n):                    # each cup's rolled rim, lowest (widest) first
        ry = y - k * step
        w = wr + (n - 1 - k) * step * slope + 3
        p.poly([(x - w, ry), (x + w, ry), (x + w, ry - h * 0.05), (x - w, ry - h * 0.05)], (236, 236, 232), INK, 1.2)
    soft(img, cam, [(x + wb * 0.4, base + 2), (x + wb, base + 2), (x + wr, y - 2), (x + wr * 0.5, y - 2)], (0, 0, 0), 0.12, 2)
    if flag_on:
        flag(img, cam, x, base + h * 0.46, h * 0.44, h * 0.32)


def espresso_cup(img, cam, x, y, h, saucer=True, flag_on=True):
    p = B.Pen(img, cam)
    if saucer:
        p.ell(x, y, h * 0.85, h * 0.16, WHITE, INK, 1.6)
    p.poly(curve([(x - h * 0.5, y - h), (x + h * 0.5, y - h), (x + h * 0.42, y - h * 0.25), (x, y - h * 0.08),
                  (x - h * 0.42, y - h * 0.25)], 3), WHITE, INK, 1.8)
    p.line(oval(x + h * 0.56, y - h * 0.62, h * 0.18, h * 0.2, 12, -1.6, 1.6), INK, 1.6)
    if flag_on:
        flag(img, cam, x, y - h * 0.56, h * 0.42, h * 0.3)


def croissant(p, x, y, s):
    c, cd = (214, 150, 70), (170, 104, 44)
    p.poly(curve([(x - 30 * s, y + 4 * s), (x - 18 * s, y - 12 * s), (x, y - 16 * s), (x + 18 * s, y - 12 * s),
                  (x + 30 * s, y + 4 * s), (x + 10 * s, y + 2 * s), (x - 10 * s, y + 2 * s)], 4), c, INK, 1.6)
    for k in (-1, 0, 1):
        p.line([(x + k * 11 * s - 3 * s, y - 13 * s), (x + k * 11 * s + 3 * s, y + 2 * s)], cd, 1.4)


def croissant_stand(img, cam, x, y, s=1.0):
    """A two-tier stand of croissants under a glass dome; bottom centre at x, y."""
    p = B.Pen(img, cam)
    p.poly([(x - 8 * s, y), (x + 8 * s, y), (x + 6 * s, y - 120 * s), (x - 6 * s, y - 120 * s)], (210, 210, 214), INK, 1.6)
    for ty, r in ((-12, 90), (-92, 64)):
        p.ell(x, y + ty * s, r * s, 12 * s, WHITE, INK, 1.8)
        for k in range(-2 if r > 70 else -1, 3 if r > 70 else 2):
            croissant(p, x + k * 34 * s, y + (ty - 8) * s, s * 0.9)
    dome = oval(x, y - 6 * s, 104 * s, 150 * s, 30, math.pi, 2 * math.pi)
    soft(img, cam, dome + [(x + 104 * s, y - 6 * s)], (220, 236, 246), 0.18, 2)
    p.line(dome, (170, 180, 190), 1.6)
    p.line([(x - 60 * s, y - 120 * s), (x - 40 * s, y - 136 * s)], (255, 255, 255), 3)


def card_machine(img, cam, x, y, s=1.0, facing=True):
    """A generic card machine on its little dock (no maker's name); bottom centre at x, y."""
    p = B.Pen(img, cam)
    p.poly([(x - 34 * s, y), (x + 34 * s, y), (x + 30 * s, y - 16 * s), (x - 30 * s, y - 16 * s)], (60, 62, 68), INK, 1.6)
    body = curve([(x - 30 * s, y - 12 * s), (x + 30 * s, y - 12 * s), (x + 32 * s, y - 108 * s), (x - 32 * s, y - 108 * s)], 3)
    p.poly(body, (44, 46, 52), INK, 1.8)
    if facing:
        p.poly([(x - 22 * s, y - 100 * s), (x + 22 * s, y - 100 * s), (x + 22 * s, y - 70 * s), (x - 22 * s, y - 70 * s)],
               (120, 196, 170), INK, 1.2)
        for r in range(4):
            for c in range(3):
                p.ell(x + (c - 1) * 14 * s, y - (60 - r * 12) * s, 4.5 * s, 3.5 * s, (200, 200, 206), None)
    else:
        p.ell(x, y - 64 * s, 12 * s, 12 * s, (62, 64, 72), None)


def biscuits(img, cam, x, y, s=1.0):
    """A small stand of neatly packaged, upmarket biscuits (plain made-up packs)."""
    p = B.Pen(img, cam)
    p.poly([(x - 70 * s, y), (x + 70 * s, y), (x + 70 * s, y - 8 * s), (x - 70 * s, y - 8 * s)], WOOD_D, INK, 1.6)
    cols = [(226, 206, 222), (196, 222, 214), (238, 222, 186)]
    for row in range(2):
        for k in range(3):
            bx = x - 44 * s + 44 * k * s
            by = y - 8 * s - row * 52 * s
            p.poly([(bx - 19 * s, by), (bx + 19 * s, by), (bx + 19 * s, by - 48 * s), (bx - 19 * s, by - 48 * s)],
                   cols[(k + row) % 3], INK, 1.4)
            p.poly([(bx - 19 * s, by - 34 * s), (bx + 19 * s, by - 34 * s), (bx + 19 * s, by - 40 * s),
                    (bx - 19 * s, by - 40 * s)], (186, 150, 80), None)
            p.ell(bx, by - 18 * s, 9 * s, 9 * s, (250, 244, 230), None)


def tablet(img, cam, x, y, s=1.0, screen=True, t=0.0):
    """The ordering tablet on its stand; bottom centre at x, y."""
    p = B.Pen(img, cam)
    p.poly([(x - 30 * s, y), (x + 30 * s, y), (x + 22 * s, y - 10 * s), (x - 22 * s, y - 10 * s)], (180, 182, 188), INK, 1.6)
    p.poly([(x - 6 * s, y - 10 * s), (x + 6 * s, y - 10 * s), (x + 6 * s, y - 70 * s), (x - 6 * s, y - 70 * s)],
           (180, 182, 188), INK, 1.4)
    p.poly([(x - 76 * s, y - 60 * s), (x + 76 * s, y - 60 * s), (x + 80 * s, y - 170 * s), (x - 80 * s, y - 170 * s)],
           (36, 36, 40), INK, 2.0)
    if screen:
        p.poly([(x - 68 * s, y - 68 * s), (x + 68 * s, y - 68 * s), (x + 71 * s, y - 162 * s), (x - 71 * s, y - 162 * s)],
               (238, 240, 244), None)
        for r in range(2):
            for c in range(3):
                bx, by = x - 46 * s + c * 46 * s, y - 140 * s + r * 34 * s
                lit = (r, c) == (1, 2) and t > 2.0
                p.poly([(bx - 18 * s, by - 12 * s), (bx + 18 * s, by - 12 * s), (bx + 18 * s, by + 12 * s), (bx - 18 * s, by + 12 * s)],
                       (226, 160, 70) if lit else (196, 208, 226), None)


def plant(img, cam, x, y, s=1.0, seed=1, tall=False):
    """A potted plant, base centre at x, y."""
    p = B.Pen(img, cam)
    rng = np.random.default_rng(seed)
    h = 300 if tall else 170
    for _ in range(16 if tall else 11):
        a = rng.uniform(-2.5, -0.65)
        ln = rng.uniform(0.5, 1.0) * h
        bx, by = x + rng.uniform(-14, 14) * s, y - 60 * s
        tx, ty = bx + math.cos(a) * ln * s, by + math.sin(a) * ln * s
        nx, ny = -math.sin(a), math.cos(a)
        w = 26 * s
        mx, my = (bx + tx) / 2, (by + ty) / 2
        col = PLANT if rng.random() < 0.6 else PLANT_D
        p.poly(curve([(bx, by), (mx + nx * w, my + ny * w), (tx, ty), (mx - nx * w, my - ny * w)], 4), col, INK, 1.6)
        p.line([(bx, by), (tx, ty)], B.dk(col, 0.75), 1.2)
    p.poly([(x - 52 * s, y - 70 * s), (x + 52 * s, y - 70 * s), (x + 40 * s, y), (x - 40 * s, y)], WHITE, INK, 2.0)


def pendant(img, cam, x, y, s=1.0):
    p = B.Pen(img, cam)
    p.line([(x, -50), (x, y - 30 * s)], (60, 60, 64), 1.6)
    p.poly(curve([(x - 52 * s, y + 18 * s), (x - 16 * s, y - 30 * s), (x + 16 * s, y - 30 * s), (x + 52 * s, y + 18 * s)], 3),
           (232, 226, 214), INK, 2.0)
    p.ell(x, y + 18 * s, 16 * s, 6 * s, (255, 236, 180), None)


# ------------------------------------------------------------------------------------------- the people
CUSTOMER = dict(full=True, trousers=(58, 60, 68), skin=B.PINK, hw=70, hh=92, jaw='square', hair='side', hair_c=(78, 66, 58), grey=(170, 166, 162),
                brow_c=(84, 72, 64), brow_w=3.4, beard='trim', beard_c=(104, 96, 90), glasses=True,
                glasses_c=(96, 70, 52), outfit='suit', jacket=COAT, shirt=(232, 236, 244), tie=(70, 86, 110), coat=COAT,
                shoulders=150, bottom=600, age=True, pose='side', lid=3)
CUST2 = dict(skin=B.PALE, hw=66, hh=86, jaw='round', hair='crop', hair_c=(110, 78, 50), outfit='jumper',
             jacket=(118, 140, 120), tee=True, shoulders=138, bottom=560, pose='none', full=True, trousers=(70, 84, 112))
CASHIER = dict(full=True, trousers=(36, 38, 46), skin=B.PALE, hw=62, hh=86, jaw='soft', hair='wavy', hair_c=BLUE_HAIR, brow_c=(70, 70, 92), brow_w=2.8,
               outfit='jumper', jacket=WHITE, apron=APRON, apron_name=True, shoulders=122, bottom=600, pose='custom',
               lashes=True, blush=True, piercing=True, brows='joy', lip_c=(206, 110, 120))
BARISTA = dict(full=True, trousers=(40, 40, 46), skin=B.DEEP, hw=68, hh=88, jaw='round', hair='afro', hair_c=(44, 36, 34), outfit='jumper',
               jacket=(150, 70, 60), apron=(60, 60, 66), shoulders=140, bottom=600, pose='custom', age=True,
               brow_c=(40, 32, 30))
STUDENT = dict(skin=B.DEEP, hw=64, hh=84, jaw='round', hair='beanie', beanie_c=(214, 156, 52), hair_c=(30, 24, 22),
               outfit='jumper', jacket=(150, 46, 52), shoulders=136, bottom=520, pose='custom', brow_c=(30, 24, 22),
               brows='fierce', lid=2)
PATRON2 = dict(skin=B.PALE, hw=68, hh=90, jaw='square', hair='slick', hair_c=(22, 20, 24), outfit='suit', jacket=NAVY_LIGHT,
               shirt=(240, 242, 246), shoulders=146, bottom=520, pose='custom', lid=4, brow_c=(26, 24, 28))


def arm_t(p, sh, el, wr, sleeve, skin, w=30):
    """An arm in a T-shirt: a short sleeve, then bare arm to the wrist."""
    B.arm(p, sh, el, wr, skin, w=w - 4)
    mid = (sh[0] + (el[0] - sh[0]) * 0.55, sh[1] + (el[1] - sh[1]) * 0.55)
    B.arm(p, sh, (sh[0] + (mid[0] - sh[0]) * 0.5, sh[1] + (mid[1] - sh[1]) * 0.5), mid, sleeve, w=w + 6)


def buzzer(img, L, x, y, t, light, shake=0.0):
    """A café's handheld order pager, held upright: a black rounded block the size of a chunky phone, a row of
    small lights along its top edge (red when it goes off) and a numbered sticker. Centre at (x, y)."""
    p = B.Pen(img, L)
    x += shake
    w, h = 36, 56
    p.poly(curve([(x - w, y - h), (x + w, y - h), (x + w, y + h), (x - w, y + h)], 4), BUZZ, INK, 2.2)
    p.poly(curve([(x - w + 7, y - h + 22), (x + w - 7, y - h + 22), (x + w - 7, y + h - 8), (x - w + 7, y + h - 8)], 4),
           (48, 48, 54), None)
    p.poly([(x - 17, y - 4), (x + 17, y - 4), (x + 17, y + 24), (x - 17, y + 24)], (246, 246, 240), INK, 1.2)
    PP.ctext(img, L, x, y + 10, '17', 17, (20, 20, 22))
    on = light > 0
    for k in range(5):
        lx = x - 24 + 12 * k
        p.ell(lx, y - h + 11, 4.2, 3.2, (255, 64, 60) if on else (88, 40, 44), None)
    if on:  # the glow from the lights
        X, Y = L.P(x, y - h + 11)
        R = L.S(64)
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse([X - R, Y - R * 0.55, X + R, Y + R * 0.55], fill=(255, 40, 40, int(140 * light)))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(R * 0.4)))
        for k in range(5):
            p.ell(x - 24 + 12 * k, y - h + 11, 2.2, 1.6, (255, 226, 220), None)


def customer2(img, cam, x, y, s, t, view):
    """The man waiting behind him: T-shirt, buzzer on his palm. Neutral; glances about; pleased at the end."""
    lv = level('cust2', t)
    sp = dict(CUST2)
    look = 0.0
    if t < FLASH:  # waiting: glances about the room, down at the buzzer, back
        ph = (t + 1.3) % 6.0
        look = -0.6 if ph < 1.6 else 0.5 if 3.0 < ph < 4.2 else 0.0
        down = 2.0 < (t % 7.0) < 2.9
        sp.update(look=look, mouth='line', lid=6 if down else 1, head_dy=4 if down else 0)
    else:  # the light: he looks at it, pleased
        sp.update(look=-0.2, lid=7, head_dy=5, mouth=talk_mouth(lv, t) if lv > 0.1 else 'pleased', brows='joy')
    sp['blink'] = blinking(t, (1.7, 5.2, 9.9, 13.6, 18.1, 22.4, 25.9))
    sp['turn'] = -0.15
    B.person(img, cam, x, y, s, sp, t)
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    skin = sp['skin']
    raise_ = smooth((t - FLASH - 0.3) / 0.5) * 40 if t > FLASH else 0.0
    # his left arm (our right) hangs; his right hand (our left) holds the buzzer in front of his belly
    arm_t(p, (124, 60), (148, 290), (140, 470), CUST2['jacket'], skin)
    B.hand(p, 140, 494, skin)
    bx, by = -20, 250 - raise_
    arm_t(p, (-124, 60), (-150, 290), (bx - 20, by + 74), CUST2['jacket'], skin)
    shake = 0.0
    light = 0.0
    if t >= FLASH:
        period = 0.5 if t < RATTLE else 0.17
        light = 1.0 if ((t - FLASH) % period) < period * 0.55 else 0.0
        if t >= RATTLE:
            shake = 6 * math.sin(t * 2 * math.pi * 11.5)
    buzzer(img, L, bx, by, t, light, shake)
    # his fingers round the bottom of it, his thumb up its side
    p.poly(curve([(bx - 42 + shake, by + 30), (bx + 40 + shake, by + 34), (bx + 44 + shake, by + 70), (bx - 40 + shake, by + 76)], 3),
           skin, INK, 2.2)
    for k in range(3):
        p.line([(bx - 20 + 22 * k + shake, by + 36), (bx - 22 + 22 * k + shake, by + 70)], B.dk(skin, 0.8), 1.4)
    p.poly(curve([(bx - 46 + shake, by + 34), (bx - 32 + shake, by - 6), (bx - 22 + shake, by - 4), (bx - 30 + shake, by + 40)], 3),
           skin, INK, 1.8)


def customer(img, cam, x, y, s, t, view):
    lv = level('cust', t)
    sp = dict(CUSTOMER, turn=-0.32, look=-0.85, mouth=talk_mouth(lv, t), brows='weary')
    if 8.35 <= t < 10.0:   # "Errm...": confused
        sp.update(brows='confused', lid=0, mouth=talk_mouth(lv, t) if lv > 0.1 else 'line')
    elif 10.0 <= t < 27.28:  # alarm, which grows through her speech
        sp.update(brows='alarm', lid=0)
    elif t >= 27.28:       # offended outrage, mouth hanging a little open
        sp.update(brows='outrage', lid=-2, mouth='agape', look=-0.95)
    sp['blink'] = blinking(t, (1.6, 6.9, 12.2, 19.6, 24.0))
    B.person(img, cam, x, y, s, sp, t)


def cashier(img, cam, x, y, s, t, view):
    lv = level('cash', t)
    sp = dict(CASHIER, turn=0.38, look=0.85, mouth=talk_mouth(lv, t, smile=True))
    sp['blink'] = blinking(t, (4.6, 7.7, 13.4, 18.9, 23.6, 26.6))
    # customer-service hands: tapping the tablet; presenting the offer; a raised finger; a little shrug
    if t < 10.95:
        tap = 6 * abs(math.sin(t * 7)) if 3.3 < t < 5.2 else 0
        arms = {'L': ((-120, 300), (40, 360), 'fist'), 'R': ((200, 200), (150, 150 + tap), 'point')}
    elif t < 12.8:
        arms = {'L': ((-120, 300), (20, 380), 'fist'), 'R': ((140, 300), (20, 372), 'fist')}
    elif t < 15.9:   # presenting the "promotion": open palm
        arms = {'L': ((-120, 300), (20, 380), 'fist'), 'R': ((210, 270), (330, 250), 'palm')}
    elif t < 20.9:   # "Did you know...": a raised finger
        arms = {'L': ((-120, 300), (20, 380), 'fist'), 'R': ((190, 250), (210, 110), 'point_up')}
    else:            # "just my opinion": palms up, a small shrug
        arms = {'L': ((-190, 270), (-300, 250), 'palm'), 'R': ((190, 270), (300, 250), 'palm')}
    sp['arms'] = arms
    B.person(img, cam, x, y, s, sp, t)


def barista(img, cam, x, y, s, t, frantic):
    """At the machine, half turned to it. Busy; then steaming milk frantically."""
    sp = dict(BARISTA, turn=0.75, look=1.0, mouth='set', lid=2)
    sp['blink'] = blinking(t, (5.1, 13.0, 21.3))
    if frantic:  # the jug jiggled up and down under the steam wand
        j = 16 * math.sin(t * 2 * math.pi * 6.0)
        sp['arms'] = {'L': ((-60, 270), (150, 230 + j), 'fist'), 'R': ((240, 250), (300, 200 + j), 'fist')}
        sp['brows'] = 'fierce'
    else:  # tamping, knocking out, reaching: a slow working loop
        ph = (t * 0.8) % 1.0
        sp['arms'] = {'L': ((-40, 280), (150 + 40 * math.sin(ph * 6.28), 260), 'fist'),
                      'R': ((250, 240), (310, 180 + 30 * math.sin(ph * 6.28 + 1)), 'fist')}
    B.person(img, cam, x, y, s, sp, t)
    if frantic:
        L = B.Local(cam, x, y, s)
        p = B.Pen(img, L)
        j = 16 * math.sin(t * 2 * math.pi * 6.0)
        jx, jy = 250, 170 + j
        p.poly([(jx - 40, jy - 60), (jx + 40, jy - 60), (jx + 48, jy + 50), (jx - 48, jy + 50)], CHROME, INK, 2.2)
        p.line([(jx - 40, jy - 30), (jx - 66, jy - 20), (jx - 66, jy + 20), (jx - 44, jy + 30)], INK, 3)
        soft(img, L, [(jx - 30, jy - 50), (jx - 10, jy - 50), (jx - 12, jy + 40), (jx - 34, jy + 40)], (255, 255, 255), 0.4, 3)
        p.line([(jx + 30, jy - 260), (jx + 4, jy - 20)], CHROME_D, 7)   # the steam wand, plunged into the jug
        rng = np.random.default_rng(int(t * FPS))
        for _ in range(9):  # steam billowing out of the jug
            sx, sy = jx + rng.uniform(-50, 60), jy - 70 - rng.uniform(0, 200)
            pts = oval(sx, sy, rng.uniform(30, 56), rng.uniform(24, 40), 16)
            soft(img, L, pts, (120, 124, 132), 0.25, 6)
            soft(img, L, pts, (255, 255, 255), 0.85, 5)


def student(img, cam, x, y, s, t):
    """Typing frantically, hunched over his laptop."""
    k1, k2 = math.sin(t * 2 * math.pi * 4.7), math.sin(t * 2 * math.pi * 5.3 + 1)
    sp = dict(STUDENT, turn=0.3, look=0.2, mouth='line', head_dy=10, lid=5)
    sp['arms'] = {'L': ((-150, 300), (-60, 380 + 8 * k1), 'fist'), 'R': ((150, 300), (60, 380 + 8 * k2), 'fist')}
    sp['blink'] = blinking(t, (3.3, 11.8, 20.4))
    B.person(img, cam, x, y, s, sp, t)


def patron2(img, cam, x, y, s, t):
    """Relaxing over an espresso; in the last moment before the bang, he calmly sips."""
    sp = dict(PATRON2, turn=-0.35, look=-0.4, mouth='line')
    sipping = SIP <= t < SIP + 0.9
    if sipping:
        sp['arms'] = {'L': ((-170, 310), (-40, 250), 'fist'), 'R': ((90, 300), (-30, 70), 'fist')}
        sp['lid'] = 7
    else:
        sp['arms'] = {'L': ((-170, 260), (-50, 170), 'fist'), 'R': ((170, 260), (40, 150), 'fist')}
    sp['blink'] = blinking(t, (2.6, 9.4, 17.2, 24.9))
    B.person(img, cam, x, y, s, sp, t)
    L = B.Local(cam, x, y, s)
    if sipping:
        espresso_cup(img, L, -40, 64, 40, saucer=False, flag_on=False)
        B.Pen(img, L).ell(-30, 60, 18, 16, sp['skin'], INK, 2.0)
    else:
        espresso_cup(img, L, -10, 150, 40, saucer=True, flag_on=False)


# ------------------------------------------------------------------------------------- the front of house
# Camera 'front': behind the counter, looking out over the customer to the bay window and the street.
WIN = (70, 380, 1010, 1000)   # the bay window
FLOOR_Y = 1060
COUNTER_Y = 1182              # the counter's top edge, seen from the staff side
POS = dict(cust=(560, 832, 0.66), cust2=(780, 806, 0.52), student=(270, 930, 0.34), patron2=(440, 930, 0.34),
           table=(355, 1010))


def street(img, cam, t):
    """Through the window: the building across the road, the road, the near pavement; now and then someone passes."""
    p = B.Pen(img, cam)
    x0, y0, x1, y1 = WIN
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], (200, 214, 226), None)
    # the terrace across the road: brick, sash windows, a shop front
    p.poly([(x0, y0), (x1, y0), (x1, 790), (x0, 790)], (176, 112, 92), None)
    for k in range(4):
        wx = x0 + 60 + k * 240
        for row in range(2):
            wy = 410 + row * 150
            p.poly([(wx, wy), (wx + 110, wy), (wx + 110, wy + 110), (wx, wy + 110)], (226, 226, 220), INK, 1.4)
            p.poly([(wx + 8, wy + 8), (wx + 102, wy + 8), (wx + 102, wy + 102), (wx + 8, wy + 102)], (120, 140, 160), None)
            p.line([(wx + 8, wy + 55), (wx + 102, wy + 55)], (226, 226, 220), 2)
    p.poly([(x0, 700), (x1, 700), (x1, 790), (x0, 790)], (64, 72, 70), None)
    for k in range(3):
        p.poly([(x0 + 40 + k * 330, 712), (x0 + 270 + k * 330, 712), (x0 + 270 + k * 330, 790), (x0 + 40 + k * 330, 790)],
               (150, 170, 180), None)
    p.poly([(x0, 790), (x1, 790), (x1, 805), (x0, 805)], (196, 196, 190), None)       # far pavement
    p.poly([(x0, 805), (x1, 805), (x1, 880), (x0, 880)], (96, 98, 104), None)         # road
    for k in range(6):
        p.poly([(x0 + 40 + k * 180, 840), (x0 + 120 + k * 180, 840), (x0 + 120 + k * 180, 846), (x0 + 40 + k * 180, 846)],
               (226, 226, 220), None)
    p.poly([(x0, 880), (x1, 880), (x1, y1), (x0, y1)], (190, 188, 182), None)         # near pavement
    # a car, once; a passer-by, twice (slow, small, muted: they never pull focus)
    cx = -300 + (t - 6.0) * 240
    if -260 < cx < 1300:
        p.poly(curve([(cx - 110, 870), (cx + 110, 870), (cx + 116, 836), (cx + 60, 832), (cx + 30, 806), (cx - 50, 806),
                      (cx - 80, 832), (cx - 116, 836)], 3), (120, 130, 150), INK, 1.4)
        p.poly([(cx - 40, 812), (cx + 24, 812), (cx + 44, 832), (cx - 64, 832)], (176, 196, 210), None)
        for sgn in (-1, 1):
            p.ell(cx + sgn * 70, 872, 16, 16, (30, 30, 32), None)
    for start, sp, col in ((1.0, -55, (70, 70, 86)), (14.0, 60, (120, 80, 70))):
        px = (1060 if sp < 0 else 20) + (t - start) * sp
        if 30 < px < 1050:
            bob = 3 * abs(math.sin((t - start) * 5))
            p.ell(px, 838 - bob, 15, 19, (226, 190, 170), INK, 1.2)
            p.poly([(px - 24, 858 - bob), (px + 24, 858 - bob), (px + 26, 960 - bob), (px - 26, 960 - bob)], col, INK, 1.2)
            sw = 10 * math.sin((t - start) * 5)
            p.line([(px - 8, 960 - bob), (px - 8 + sw, 1000)], (40, 40, 48), 6)
            p.line([(px + 8, 960 - bob), (px + 8 - sw, 1000)], (40, 40, 48), 6)
    # the glass: a pale tint and two soft reflections, so the street sits behind it
    soft(img, cam, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], (226, 236, 242), 0.32, 0)
    soft(img, cam, [(x0 + 120, y0), (x0 + 260, y0), (x0 + 60, y1), (x0 - 80, y1)], (255, 255, 255), 0.16, 6)
    soft(img, cam, [(x0 + 620, y0), (x0 + 700, y0), (x0 + 560, y1), (x0 + 480, y1)], (255, 255, 255), 0.12, 6)


def front_room(img, cam, t):
    p = B.Pen(img, cam)
    p.poly([(-400, -200), (1500, -200), (1500, FLOOR_Y), (-400, FLOOR_Y)], WALL, None)
    p.poly([(-400, -200), (1500, -200), (1500, 330), (-400, 330)], (246, 246, 244), None)   # ceiling
    p.line([(-400, 330), (1500, 330)], (214, 212, 206), 2)
    street(img, cam, t)
    x0, y0, x1, y1 = WIN  # the bay: a white frame, angled side panes, mullions
    p.poly([(x0 - 26, y0 - 26), (x1 + 26, y0 - 26), (x1 + 26, y0), (x0 - 26, y0)], WHITE, INK, 2.0)
    p.poly([(x0 - 26, y1), (x1 + 26, y1), (x1 + 40, y1 + 22), (x0 - 40, y1 + 22)], WHITE, INK, 2.0)  # the sill
    for x in (x0, 290, 790, x1):
        p.poly([(x - 9, y0), (x + 9, y0), (x + 9, y1), (x - 9, y1)], WHITE, INK, 1.8)
    p.poly([(x0 - 26, y0), (x0, y0), (x0, y1), (x0 - 26, y1)], WHITE, INK, 1.8)
    p.poly([(x1, y0), (x1 + 26, y0), (x1 + 26, y1), (x1, y1)], WHITE, INK, 1.8)
    p.poly([(x0, 552), (x1, 552), (x1, 566), (x0, 566)], WHITE, INK, 1.6)   # the transom
    p.poly([(-400, y1 + 22), (1500, y1 + 22), (1500, FLOOR_Y), (-400, FLOOR_Y)], (232, 228, 220), None)
    p.line([(-400, FLOOR_Y), (1500, FLOOR_Y)], (180, 160, 130), 2)
    p.poly([(-400, FLOOR_Y), (1500, FLOOR_Y), (1500, 1400), (-400, 1400)], WOOD, None)     # the floor
    for k in range(-8, 14):
        p.line([(540 + k * 120, FLOOR_Y), (540 + k * 260, 1400)], WOOD_D, 1.4)
    plant(img, cam, 940, 1072, 1.1, seed=3, tall=True)
    plant(img, cam, 175, 1072, 0.9, seed=5, tall=True)
    for x in (300, 790):
        pendant(img, cam, x, 400, 1.0)


def chair(img, cam, x, y, s, back=True, facing=1):
    """A plush white armchair; seat front centre at x, y."""
    p = B.Pen(img, cam)
    c, cd = (246, 244, 238), (222, 218, 210)
    if back:
        p.poly(curve([(x - 90 * s, y - 40 * s), (x - 84 * s, y - 230 * s), (x + 84 * s, y - 230 * s), (x + 90 * s, y - 40 * s)], 3),
               c, INK, 2.0)
        return
    p.poly(curve([(x - 104 * s, y + 70 * s), (x - 104 * s, y - 70 * s), (x + 104 * s, y - 70 * s), (x + 104 * s, y + 70 * s)], 3),
           c, INK, 2.0)
    for sgn in (-1, 1):
        p.poly(curve([(x + sgn * 112 * s, y + 70 * s), (x + sgn * 112 * s, y - 110 * s), (x + sgn * 80 * s, y - 110 * s),
                      (x + sgn * 80 * s, y + 70 * s)], 3), cd, INK, 2.0)
    p.line([(x - 80 * s, y - 20 * s), (x + 80 * s, y - 20 * s)], cd, 1.6)


def shins(img, cam, x, trousers, shoe):
    """A seated person's lower legs: knees at the seat's front edge, feet on the floor."""
    p = B.Pen(img, cam)
    for sgn in (-1, 1):
        kx = x + sgn * 22
        p.poly([(kx - 15, 1018), (kx + 15, 1018), (kx + 13 + sgn * 4, 1086), (kx - 13 + sgn * 4, 1086)], trousers, INK, 1.8)
        p.ell(kx, 1018, 17, 10, trousers, INK, 1.8)
        p.poly(curve([(kx - 15 + sgn * 4, 1082), (kx + 17 + sgn * 8, 1082), (kx + 22 + sgn * 8, 1096), (kx - 15 + sgn * 4, 1096)], 3),
               shoe, INK, 1.6)


def seating(img, cam, t):
    """The low white table before the window, two plush chairs either side; the student and the man in navy."""
    tx, ty = POS['table']
    sx, sy, ss = POS['student']
    nx, ny, ns = POS['patron2']
    # the far chairs of each pair (empty), then the near ones with people in them
    chair(img, cam, sx + 120, 1004, 0.5, back=True)
    chair(img, cam, sx + 120, 1004, 0.5, back=False)
    chair(img, cam, nx - 120, 1004, 0.5, back=True)
    chair(img, cam, nx - 120, 1004, 0.5, back=False)
    chair(img, cam, sx, 1030, 0.58, back=True)
    chair(img, cam, nx, 1030, 0.58, back=True)
    student(img, cam, sx, sy, ss, t)
    patron2(img, cam, nx, ny, ns, t)
    chair(img, cam, sx, 1030, 0.58, back=False)
    chair(img, cam, nx, 1030, 0.58, back=False)
    shins(img, cam, sx, (40, 40, 52), (226, 226, 220))
    shins(img, cam, nx, NAVY_LIGHT, (40, 30, 26))
    p = B.Pen(img, cam)
    # the table, the laptop (its back to us), the empty sandwich plate, his espresso saucer's twin
    p.poly([(tx - 120, ty), (tx + 120, ty), (tx + 126, ty + 14), (tx - 126, ty + 14)], WHITE, INK, 2.0)
    for sgn in (-1, 1):
        p.poly([(tx + sgn * 104, ty + 14), (tx + sgn * 96, ty + 14), (tx + sgn * 96, ty + 56), (tx + sgn * 104, ty + 56)],
               (210, 206, 198), INK, 1.4)
    lx = sx + 60
    p.poly([(lx - 44, ty - 2), (lx + 44, ty - 2), (lx + 40, ty - 62), (lx - 40, ty - 62)], (176, 180, 188), INK, 1.8)
    p.ell(lx, ty - 32, 6, 6, (214, 216, 222), None)
    p.ell(tx + 6, ty - 2, 34, 7, WHITE, INK, 1.4)
    for k in range(3):
        p.ell(tx - 6 + 7 * k, ty - 4 - (k % 2), 2.2, 1.4, (200, 170, 120), None)  # crumbs


def front_counter(img, cam, t):
    """The counter from the staff side: wood top, the white under-counter shelves; croissants left, card machine and
    biscuits right."""
    p = B.Pen(img, cam)
    croissant_stand(img, cam, 380, COUNTER_Y + 6, 0.9)
    p.poly([(-400, COUNTER_Y), (1500, COUNTER_Y), (1500, COUNTER_Y + 70), (-400, COUNTER_Y + 70)], WOOD, INK, 2.2)
    p.line([(-400, COUNTER_Y + 34), (1500, COUNTER_Y + 34)], WOOD_D, 1.4)
    p.poly([(-400, COUNTER_Y + 70), (1500, COUNTER_Y + 70), (1500, 2200), (-400, 2200)], WHITE, INK, 2.0)
    for y in (1420, 1640):
        p.poly([(-400, y), (1500, y), (1500, y + 16), (-400, y + 16)], WOOD, INK, 1.6)
    card_machine(img, cam, 800, COUNTER_Y + 22, 0.8, facing=False)
    biscuits(img, cam, 900, COUNTER_Y + 22, 0.9)


def cashier_back(img, cam, x, y, s, t):
    """The cashier from behind, at the very left of the establishing shot: blue waves, apron bow, white shirt."""
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    p.poly([(-130, 10), (130, 10), (150, 60), (160, 600), (-160, 600), (-150, 60)], WHITE, INK, 2.6)
    p.line([(-40, 10), (-60, 300)], APRON, 7)
    p.line([(40, 10), (60, 300)], APRON, 7)
    p.line([(-150, 380), (150, 380)], APRON, 9)
    p.poly(curve([(0, 380), (-50, 350), (-56, 404)], 3), APRON, INK, 1.6)
    p.poly(curve([(0, 380), (50, 350), (56, 404)], 3), APRON, INK, 1.6)
    p.poly([(-30, -80), (30, -80), (34, 10), (-34, 10)], CASHIER['skin'], INK, 2.4)
    pts = [(-90, -230)]
    for k in range(7):
        pts.append((-84 - 12 * (k % 2), -200 + 36 * k))
    pts += [(-60, 90), (60, 90)]
    for k in range(6, -1, -1):
        pts.append((84 + 12 * (k % 2), -200 + 36 * k))
    pts += [(90, -230), (0, -262)]
    p.poly(curve(pts, 4), BLUE_HAIR, INK, 2.6)
    for k in range(4):
        x0 = -48 + 32 * k
        p.line([(x0, -230), (x0 + 12, -150), (x0 - 4, -60), (x0 + 8, 30)], B.dk(BLUE_HAIR, 0.72), 1.8)


# -------------------------------------------------------------------------------------- the back of house
# Camera 'back': from the customer's side of the counter, looking at the cashier, the barista and the machine.
BACK_COUNTER_Y = 1210
BPOS = dict(cash=(372, 902, 0.8), barista=(690, 812, 0.5))


def back_room(img, cam, t, frantic):
    p = B.Pen(img, cam)
    p.poly([(-400, -200), (1500, -200), (1500, 1300), (-400, 1300)], TILE, None)
    p.poly([(-400, -200), (1500, -200), (1500, 330), (-400, 330)], (246, 246, 244), None)
    p.line([(-400, 330), (1500, 330)], (214, 212, 206), 2)
    for y in range(352, 1100, 34):  # metro tiles
        p.line([(-400, y), (1500, y)], (222, 222, 218), 1.2)
        off = 0 if (y // 34) % 2 else 34
        for x in range(-400 + off, 1500, 68):
            p.line([(x, y), (x, y + 34)], (222, 222, 218), 1.0)
    # the menu board: the shop's name small, a made-up crown over a cup, plain prices
    p.poly([(90, 370), (640, 370), (640, 640), (90, 640)], (36, 38, 40), (120, 96, 70), 6)
    crown_mark(p, 130, 412, 18, (236, 236, 230))
    PP.ctext(img, cam, 280, 414, 'COFFEE QUEENS', 26, (236, 236, 230))
    items = [('ESPRESSO', '2.80'), ('FLAT WHITE', '3.60'), ('LATTE', '3.70'), ('CARAMEL LATTE', '4.20'),
             ('CAPPUCCINO', '3.60'), ('MOCHA', '4.10')]
    for i, (n, pr) in enumerate(items):
        y = 462 + 28 * i
        PP.ctext(img, cam, 220, y, n, 17, (226, 226, 220))
        PP.ctext(img, cam, 540, y, pr, 17, (226, 226, 220))
    # the open shelf: stacks of large takeaway cups and of espresso cups, every one with the flag
    p.poly([(60, 812), (560, 812), (560, 830), (60, 830)], WOOD, INK, 2.0)
    cup_stack(img, cam, 130, 812, 68, 6)
    cup_stack(img, cam, 220, 812, 68, 6)
    cup_stack(img, cam, 310, 812, 68, 6)
    for col in range(2):
        for row in range(3):
            espresso_cup(img, cam, 440 + col * 62, 812 - row * 34, 34, saucer=False)
    plant(img, cam, 610, 812, 0.6, seed=8)
    # the back worktop, the syrups, the jugs, and the big machine
    p.poly([(-400, 1010), (1500, 1010), (1500, 1040), (-400, 1040)], WHITE, INK, 2.0)
    syrups = [(176, 104, 40), (230, 200, 120), (120, 60, 40), (200, 120, 150)]
    for k, c in enumerate(syrups):
        x = 470 + k * 34
        p.poly([(x - 13, 1010), (x + 13, 1010), (x + 13, 930), (x + 5, 910), (x + 5, 880), (x - 5, 880), (x - 5, 910), (x - 13, 930)],
               c, INK, 1.4)
        p.poly([(x - 9, 950), (x + 9, 950), (x + 9, 980), (x - 9, 980)], (244, 240, 230), None)
    machine(img, cam, t, frantic)


def machine(img, cam, t, frantic):
    """An industrial three-group espresso machine, cups warming on top, steam wands, milk jugs."""
    p = B.Pen(img, cam)
    x0, x1, top, bot = 640, 1080, 780, 1010
    for k in range(5):   # espresso cups on the warmer, every one flagged
        espresso_cup(img, cam, x0 + 60 + k * 72, top - 4, 30, saucer=False, flag_on=False)
    p.poly([(x0, top), (x1, top), (x1, bot), (x0, bot)], CHROME, INK, 2.6)
    p.poly([(x0, top), (x1, top), (x1, top + 40), (x0, top + 40)], (36, 36, 40), INK, 2.2)
    soft(img, cam, [(x0 + 20, top + 50), (x0 + 60, top + 50), (x0 + 50, bot - 20), (x0 + 10, bot - 20)], (255, 255, 255), 0.5, 4)
    for k in range(3):   # group heads and portafilters
        gx = x0 + 90 + k * 130
        p.poly([(gx - 30, top + 90), (gx + 30, top + 90), (gx + 24, top + 120), (gx - 24, top + 120)], CHROME_D, INK, 1.8)
        p.poly([(gx - 34, top + 120), (gx + 34, top + 120), (gx + 30, top + 138), (gx - 30, top + 138)], (60, 60, 66), INK, 1.8)
        p.line([(gx + 30, top + 130), (gx + 90, top + 146)], (30, 30, 32), 7)
        p.ell(gx, top + 64, 10, 10, (230, 90, 70) if k == 1 else (90, 200, 120), INK, 1.2)
    p.poly([(x0 + 30, bot - 30), (x1 - 30, bot - 30), (x1 - 30, bot - 8), (x0 + 30, bot - 8)], CHROME_D, INK, 1.6)
    for sx in (x0 + 18, x1 - 18):  # steam wands
        p.line([(sx, top + 100), (sx - 6, top + 210)], CHROME_D, 6)
    for k in range(2):   # milk jugs on the worktop
        jx = x0 + 120 + k * 70
        p.poly([(jx - 22, 1010), (jx + 22, 1010), (jx + 18, 950), (jx - 18, 950)], CHROME, INK, 1.6)
    if not frantic:   # a little steam curling from the warmer
        soft(img, cam, oval(x0 + 200, top - 60 - 10 * math.sin(t), 24, 40, 16), (255, 255, 255), 0.35, 10)


def back_counter(img, cam, t):
    """The counter from the customer's side: wood slat front; card machine and biscuits left, croissants right,
    the tablet (its back to us) in front of the cashier."""
    p = B.Pen(img, cam)
    card_machine(img, cam, 130, BACK_COUNTER_Y + 4, 1.05, facing=True)
    biscuits(img, cam, 250, BACK_COUNTER_Y + 4, 0.95)
    tablet(img, cam, 470, BACK_COUNTER_Y + 4, 1.0, screen=False)
    croissant_stand(img, cam, 820, BACK_COUNTER_Y + 4, 1.05)
    p.poly([(-400, BACK_COUNTER_Y), (1500, BACK_COUNTER_Y), (1500, BACK_COUNTER_Y + 40), (-400, BACK_COUNTER_Y + 40)],
           WOOD, INK, 2.2)
    p.poly([(-400, BACK_COUNTER_Y + 40), (1500, BACK_COUNTER_Y + 40), (1500, 2200), (-400, 2200)], WOOD_D, INK, 2.0)
    for x in range(-380, 1500, 46):
        p.line([(x, BACK_COUNTER_Y + 44), (x, 2200)], B.dk(WOOD_D, 0.86), 1.6)
    soft(img, cam, [(-400, BACK_COUNTER_Y + 40), (1500, BACK_COUNTER_Y + 40), (1500, BACK_COUNTER_Y + 110),
                    (-400, BACK_COUNTER_Y + 110)], (0, 0, 0), 0.18, 8)


# -------------------------------------------------------------------------------------------- the frames
CAMS = {'front': (1.4, 560, 653), 'cust': (1.62, 610, 756), 'back': (1.3, 500, 718), 'back2': (1.35, 500, 751)}


def explosion(img, cam, x, y, t):
    """The bang: a hard white flash, a ragged fireball rolling into dark smoke, black plastic flying, a jolt.
    Drawn in the film's flat style, played straight; no comic-book star."""
    u = (t - BANG) / 0.42   # 0 at the bang, 1 where the blast would end (we cut at about 0.75)
    p = B.Pen(img, cam)
    rng = np.random.default_rng(31)
    R = 130 + 340 * (1 - (1 - min(u, 1)) ** 2)

    def ragged(cx, cy, r, n, rough, ph):
        """An irregular, turbulent outline (no star points, no neat rings)."""
        a = np.linspace(0, 2 * math.pi, n, endpoint=False)
        k = 1 + rough * (0.5 * np.sin(3 * a + ph) + 0.3 * np.sin(5 * a + 2 * ph) + 0.2 * np.sin(9 * a + 3 * ph))
        k += rough * 0.35 * rng.uniform(-1, 1, n)
        return [(cx + r * kk * math.cos(aa), cy + r * kk * math.sin(aa) * 0.88 - r * 0.12) for kk, aa in zip(k, a)]
    # dark smoke billowing out and up, lumpy, uneven greys
    for k in range(18):
        a = rng.uniform(0, 2 * math.pi)
        d = R * rng.uniform(0.35, 0.8)
        r = R * rng.uniform(0.22, 0.42)
        g = int(rng.uniform(44, 84))
        sx, sy = x + d * math.cos(a), y + d * math.sin(a) * 0.8 - R * 0.15 * u
        p.poly(curve(ragged(sx, sy, r, 11, 0.25, k), 3), (g, g - 2, g - 4), INK, 2.0)
        soft(img, cam, ragged(sx - r * 0.2, sy - r * 0.25, r * 0.5, 9, 0.2, k + 1), (150, 146, 140), 0.35, 4)
    # the fireball: off-centre, torn, white-hot at the core, already breaking up into the smoke
    for scale, col, dx, dy in ((0.66, (214, 84, 30), 0.06, -0.04), (0.5, (246, 150, 44), -0.05, 0.02),
                               (0.34, (255, 214, 110), 0.03, -0.06), (0.17, (255, 250, 232), -0.02, 0.0)):
        r = R * scale * (1 - 0.35 * max(0.0, u - 0.4))
        p.poly(curve(ragged(x + R * dx, y + R * dy, r, 17, 0.32, scale * 9), 2), col, INK if scale > 0.6 else None, 2.2)
    # bits of the black plastic case flying out
    for k in range(11):
        a = rng.uniform(0, 2 * math.pi)
        d = R * (0.9 + rng.uniform(0, 0.7))
        bx, by = x + d * math.cos(a), y + d * math.sin(a)
        sz = rng.uniform(10, 22)
        rot = rng.uniform(0, 6.28) + u * 4
        pts = [(bx + sz * math.cos(rot + j * 2.1 + rng.uniform(-0.4, 0.4)), by + sz * math.sin(rot + j * 2.1)) for j in range(3)]
        p.poly(pts, (26, 26, 30), INK, 1.4)
    # the flash over everything, strongest on the first drawing
    flash = max(0.0, 0.85 - 1.6 * u)
    if flash > 0:
        B.shade(img, flash, (255, 250, 236))


def frame_image(t, captions=True, title=True):
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    view = next(v for v, a, b in SHOTS if a <= t < b)
    img = B.canvas((255, 255, 255))
    z, cx, cy = CAMS[view]
    if t >= BANG:  # the frame jolts with the blast
        k = int((t - BANG) * FPS)
        cx += (-14, 10, -6, 4)[k % 4] / z * 2
        cy += (8, -12, 6, -3)[k % 4] / z * 2
    cam = B.Cam(z, cx, cy)
    if view in ('front', 'cust'):
        front_room(img, cam, t)
        seating(img, cam, t)
        x2, y2, s2 = POS['cust2']
        customer2(img, cam, x2, y2, s2, t, view)
        x, y, s = POS['cust']
        if t < 0.5:  # shuffling up to the counter
            k = smooth(t / 0.5)
            x += 80 * (1 - k)
            y += 6 * abs(math.sin(t * 9)) * (1 - k)
        customer(img, cam, x, y, s, t, view)
        front_counter(img, cam, t)
        if t >= BANG:
            L = B.Local(cam, x2, y2, s2)
            ex, ey = L.P(-6, 300)
            explosion(img, cam, (ex / B.SS - B.W / 2) / cam.z + cam.cx, (ey / B.SS - B.H / 2) / cam.z + cam.cy, t)
    else:
        frantic = view == 'back2' and 11.3 < t < 26.9
        back_room(img, cam, t, frantic)
        bx, by, bs = BPOS['barista']
        barista(img, cam, bx, by, bs, t, frantic)
        x, y, s = BPOS['cash']
        cashier(img, cam, x, y, s, t, view)
        back_counter(img, cam, t)
    if captions:
        for w, at, name, s0, s1, pieces in LINES:
            end = at + (s1 - s0)
            for i, (pt, text) in enumerate(pieces):
                nxt = pieces[i + 1][0] if i + 1 < len(pieces) else end + 0.25
                if pt - 0.05 <= t < nxt and t < BLACK_AT:
                    later = [a for _, a, _, _, _, _ in LINES if a > at]
                    if not later or t < later[0] - 0.05 or i + 1 < len(pieces):
                        PP.caption(img, text)
    if title and t < 1.0:  # the standard title, over the window, gone by 1 s
        B.title(img, TITLE, alpha=1.0 if t < 0.75 else 1.0 - (t - 0.75) / 0.25, maxw=720)
    return img


# ----------------------------------------------------------------------------------------------- sound
rng = np.random.default_rng(23)


def place(mix, snd, at, gain=1.0):
    s = int(at * SR)
    e = min(len(mix), s + len(snd))
    if s < 0:
        snd, s = snd[-s:], 0
    if e > s:
        mix[s:e] += snd[:e - s] * gain


def band(x, lo, hi):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)


def murmur(n):
    """A café's soft murmur: a few people chatting at other tables, far off. Each voice is made like speech (a
    voiced buzz at its own pitch, shaped by changing vowel resonances into syllables and phrases), so it reads as
    distant talk, not as hiss."""
    from scipy.signal import butter, sosfilt
    vowels = [(730, 1090), (530, 1840), (270, 2290), (570, 840), (300, 870), (660, 1720), (490, 1350)]
    out = np.zeros(n)
    for v in range(5):
        f0 = rng.uniform(105, 135) if v % 2 == 0 else rng.uniform(185, 225)
        t = rng.uniform(0, 1.5)
        voice = np.zeros(n)
        while t < n / SR - 0.5:
            phrase_end = t + rng.uniform(1.0, 3.2)
            while t < phrase_end and t < n / SR - 0.4:
                d = rng.uniform(0.11, 0.24)
                m = int(d * SR)
                tt = np.arange(m) / SR
                pitch = f0 * (1 + 0.08 * math.sin(t * 1.7 + v) + 0.04 * rng.uniform(-1, 1)) * (1 - 0.05 * tt / d)
                ph = 2 * np.pi * np.cumsum(pitch) / SR
                buzz = sum(np.sin(h * ph) / h for h in range(1, int(3000 / pitch[0])))
                f1, f2 = vowels[rng.integers(len(vowels))]
                syl = sosfilt(butter(2, [f1 * 0.8, f1 * 1.2], 'band', fs=SR, output='sos'), buzz) \
                    + 0.5 * sosfilt(butter(2, [f2 * 0.85, f2 * 1.15], 'band', fs=SR, output='sos'), buzz)
                syl *= np.sin(np.pi * tt / d) ** 1.5 * rng.uniform(0.5, 1.0)
                place(voice, syl, t)
                t += d + rng.uniform(0.0, 0.05)
            t += rng.uniform(0.6, 2.4)   # a pause, the other person talking, a sip
        out += normal(voice) * rng.uniform(0.6, 1.0)
    out = onepole_lp(out, 1800)          # far off: the top end softened
    return normal(out)


def clink():
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * d) for f, d in ((2630, 22), (4120, 30), (5480, 40), (3310, 26)))
    return normal(x * (1 - np.exp(-tt * 2000)))


def keys(n):
    """The student's laptop: soft clicks in frantic bursts."""
    out = np.zeros(n)
    click = band(rng.standard_normal(int(0.012 * SR)), 1500, 6000) * np.exp(-np.arange(int(0.012 * SR)) / SR * 400)
    t = 0.2
    while t < n / SR - 0.1:
        burst = rng.uniform(1.0, 3.0)
        end = t + burst
        while t < end:
            place(out, click * rng.uniform(0.5, 1.0), t)
            t += rng.uniform(0.06, 0.13)
        t += rng.uniform(0.2, 0.7)
    return normal(out)


def machine_hiss(n):
    """The espresso machine working: a pump's hum and a soft hiss."""
    tt = np.arange(n) / SR
    hum = sum(np.sin(2 * np.pi * 50 * h * tt) / h for h in (1, 2, 3, 4)) * 0.3
    hiss = band(rng.standard_normal(n), 2500, 9000)
    return normal(onepole_lp(hum, 600) + 0.6 * hiss)


def steam(n):
    """The steam wand screaming into a jug of milk: a whistle that wavers and gurgles."""
    tt = np.arange(n) / SR
    f = 2900 + 260 * np.sin(2 * np.pi * 0.7 * tt) + 120 * np.sin(2 * np.pi * 6.0 * tt)
    whistle = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
    roar = band(rng.standard_normal(n), 1200, 8000)
    gurgle = band(rng.standard_normal(n), 120, 600) * (0.5 + 0.5 * np.sin(2 * np.pi * 6.0 * tt))
    env = np.minimum(1, tt / 0.15)
    return normal((0.35 * whistle + roar + 0.6 * gurgle) * env)


def street_hum(n):
    return normal(onepole_lp(onepole_lp(rng.standard_normal(n), 300), 300))


def car_pass(dur=4.0):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    env = np.exp(-((tt - dur / 2) / (dur / 5)) ** 2)
    return normal(onepole_lp(rng.standard_normal(n), 700) * env)


def buzz(dur):
    """The order buzzer's vibrating buzz and its rattle against his palm."""
    n = int(dur * SR)
    tt = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * 172 * tt)) * 0.6 + np.sin(2 * np.pi * 344 * tt) * 0.3
    rattle = band(rng.standard_normal(n), 600, 3000) * (np.sin(2 * np.pi * 43 * tt) > 0.6)
    k = int(0.006 * SR)
    env = np.ones(n)
    env[:k] = np.linspace(0, 1, k)
    env[-k:] = np.linspace(1, 0, k)
    return normal(onepole_lp(x + 0.5 * rattle, 3000) * env)


def boom():
    """A short, punchy, slightly muffled bang: a deep thump with a crack on top. Not a war-film bomb."""
    n = int(0.9 * SR)
    tt = np.arange(n) / SR
    f = 38 + 90 * np.exp(-tt * 14)
    thump = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 6)
    body = onepole_lp(onepole_lp(rng.standard_normal(n), 900), 900) * np.exp(-tt * 7)
    crack = band(rng.standard_normal(n), 900, 6000) * np.exp(-tt * 70)
    harm = np.sin(2 * np.pi * np.cumsum(f * 3) / SR) * np.exp(-tt * 9)   # a higher layer phones can play
    x = 1.0 * thump + 0.7 * normal(body) + 0.55 * normal(crack) + 0.35 * harm
    x[:int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))
    return normal(x)


def limiter(x, ceiling_db=-1.2):
    """Keep the peaks (measured between samples too) under the ceiling, smoothly."""
    from scipy.ndimage import maximum_filter1d, uniform_filter1d
    c = 10 ** (ceiling_db / 20)
    over = np.abs(x)
    need = np.minimum(1.0, c / np.maximum(over, 1e-9))
    w = int(0.004 * SR)
    g = maximum_filter1d(1 - need, w * 2)   # look ahead and hold
    g = uniform_filter1d(g, w)
    return x * (1 - g)


def soundtrack():
    n = int(DUR * SR)
    mix = np.zeros(n)
    end = int(BLACK_AT * SR)
    mix[:end] += 0.035 * murmur(end)
    mix[:end] += 0.05 * keys(end)
    for at in (1.4, 6.3, 9.8, 15.2, 19.7, 24.1, 28.4):
        place(mix, clink(), at, 0.05)
    place(mix, car_pass(), 5.5, 0.04)
    a, b = int(3.15 * SR), int(8.35 * SR)
    seg = machine_hiss(b - a)
    k = int(0.03 * SR)
    seg[:k] *= np.linspace(0, 1, k)
    seg[-k:] *= np.linspace(1, 0, k)
    mix[a:b] += 0.06 * seg
    a, b = int(11.3 * SR), int(26.9 * SR)
    seg = steam(b - a)
    k = int(0.3 * SR)
    seg[-k:] *= np.linspace(1, 0, k)
    mix[a:b] += 0.075 * seg
    # the buzzer: a buzz with each flash of its light, faster as it rattles
    t = FLASH
    while t < BANG:
        period = 0.5 if t < RATTLE else 0.17
        place(mix, buzz(period * 0.55), t, 0.12 if t < RATTLE else 0.16)
        t += period
    place(mix, boom(), BANG, 0.95)
    for who, at, name, s0, s1, _ in LINES:  # the voices: cleaned, levelled, otherwise exactly as recorded
        seg = MA.line(name)[int(s0 * SR):int(s1 * SR)].copy()
        k = int(0.02 * SR)
        seg[:k] *= np.linspace(0, 1, k)
        seg[-k:] *= np.linspace(1, 0, k)
        place(mix, seg, at, 1.0)
    k = int(0.005 * SR)
    mix[end - k:end] *= np.linspace(1, 0, k)   # hard cut to black: a few-millisecond fade, then nothing
    mix[end:] = 0
    # master: about -14 LUFS, peaks no higher than -1 dBTP
    for _ in range(3):
        mix *= 10 ** ((-14.0 - MA.lufs(mix[:end])) / 20)
        mix = limiter(mix, -1.5)
    return mix


def render_frame(args):
    i, size, ss = args
    B.SS = ss
    return np.asarray(frame_image(i / FPS).convert('RGB').resize(size, Image.LANCZOS)).tobytes()


def render(out, size, crf, ss):
    import imageio_ffmpeg
    from multiprocessing import Pool
    wav = out + '.wav'
    mix = soundtrack()
    print(f'sound: {MA.lufs(mix):.1f} LUFS, peak {MA.true_peak_db(mix):.1f} dBTP', flush=True)
    MA.write_wav(wav, mix)
    n = int(round(DUR * FPS))
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{size[0]}x{size[1]}', '-r', str(FPS), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for f, fr in enumerate(pool.imap(render_frame, [(i, size, ss) for i in range(n)], chunksize=2)):
            p.stdin.write(fr)
            if f % 48 == 0:
                print(f'frame {f}/{n}', flush=True)
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print(f'done: {out} ({os.path.getsize(out) / 1e6:.1f} MB)', flush=True)


# ------------------------------------------------------------------------------------- storyboard sheet
BOARD = [(1, 'Over the counter', 0.6), (2, 'The cashier', 6.6), (3, 'The customer', 10.5), (4, 'The cashier again', 13.6),
         (5, 'Customer; buzzer goes', 28.6)]


def closeup(t, cam_z, cx, cy, view):
    """A close look at one part of the set (the cups, the buzzer), for the storyboard."""
    global CAMS
    keep = CAMS
    CAMS = dict(CAMS, **{view: (cam_z, cx, cy)})
    try:
        return frame_image(t, captions=False, title=False)
    finally:
        CAMS = keep


def sheet(dst):
    cw, ch, lab = 360, 640, 70
    stills = [(f'{n}. {name}', frame_image(t)) for n, name, t in BOARD]
    stills.append(('Cups close-up', closeup(13.6, 2.9, 240, 770, 'back2')))
    stills.append(('Buzzer close-up', closeup(28.6, 3.4, 772, 905, 'cust')))
    stills.append(('Bang (cut 3/4 through)', frame_image(BANG + 0.25, captions=False)))
    cols = 4
    rows = (len(stills) + cols - 1) // cols
    sh = Image.new('RGB', (cols * (cw + 16) + 16, rows * (ch + lab + 12) + 16), (245, 242, 236))
    d = ImageDraw.Draw(sh)
    f = ImageFont.truetype(B.SANS, 22)
    for i, (name, im) in enumerate(stills):
        x, y = 16 + (i % cols) * (cw + 16), 16 + (i // cols) * (ch + lab + 12)
        sh.paste(im.convert('RGB').resize((cw, ch), Image.LANCZOS), (x, y))
        d.text((x + 2, y + ch + 10), name, font=f, fill=(20, 20, 20))
    sh.save(dst, quality=88)


def main():
    mode = sys.argv[1]
    if mode == 'resound':  # put a fresh soundtrack on an existing render (pictures unchanged)
        import imageio_ffmpeg
        src, out = sys.argv[2], sys.argv[3]
        mix = soundtrack()
        print(f'sound: {MA.lufs(mix):.1f} LUFS, peak {MA.true_peak_db(mix):.1f} dBTP', flush=True)
        MA.write_wav(out + '.wav', mix)
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', src, '-i', out + '.wav', '-map', '0:v',
                        '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out],
                       check=True)
        os.remove(out + '.wav')
        return
    if mode == 'stills':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for s in sys.argv[3:]:
            frame_image(float(s)).convert('RGB').resize((B.W, B.H), Image.LANCZOS).save(os.path.join(out, f't{s}.png'))
    elif mode == 'sheet':
        sheet(sys.argv[2])
    elif mode == 'animatic':
        render(sys.argv[2], (540, 960), 26, 1)
    elif mode == 'final':
        render(sys.argv[2], (1080, 1920), 20, 2)


if __name__ == '__main__':
    main()
