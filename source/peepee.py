#!/usr/bin/env python3
"""The Patriots ("Pee Pee"): a TV street interview at a border blockade outside Dover.

Same look as Hope Again (burnham.py): flat shapes, clean black outlines, almond eyes with small pupils,
soft shading, deadpan staging, a still camera and hard cuts. Made vertical (1080 x 1920), faces and text
inside TikTok's safe area (x 60-900, y 310-1500).

Everyone is invented: the masked protester and the reporter are not based on anyone real. The only
emblems are his own two arm badges ("PP", and his felt-tip doodle of the other PP) and St George flags.

Usage:
    python3 peepee.py stills OUT_DIR T1 T2 ...   frames at those times (seconds), full size
    python3 peepee.py animatic OUT.mp4           half size, quick, to check timing
    python3 peepee.py final OUT.mp4              full size
"""
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import burnham as B
from burnham_film import keyed, load, onepole_lp, bandnoise, reverb, normal
from ed import INK, curve, oval, soft, smooth

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 12
SR = 48000

BALA = (30, 30, 34)          # balaclava
JACKET = (38, 38, 44)
SLEEVE = (62, 62, 72)
COMBAT = (82, 86, 64)
EYE_SKIN = (236, 198, 178)
CAMEL = (188, 144, 98)
SCARF = (44, 54, 88)
AUBURN = (150, 64, 40)
HIVIS = (218, 236, 52)
RED = (196, 30, 44)

# ------------------------------------------------------------------------------------------- timeline
# (who, start, end, caption, italic, recording) - placeholders until Sam's recordings arrive:
# recording is (file, from, to) in that file, or None for a silent placeholder.
LINES = [
    ('pro', 0.05, 2.75, "We're here to stop an invasion on our borders, love!", False, None),
    ('rep', 3.25, 6.15, "And you're doing that by blocking citizens from accessing the UK side of the border",
     False, None),
    ('rep', 6.15, 9.05, "and preventing UK immigration officers from doing their jobs?", False, None),
    ('pro', 9.55, 13.2, "Oooooh, I'm a reporter, I think through what I do and say.", True, None),
    ('pro', 13.45, 14.7, "You're a traitor, love!", False, None),
]
SHOTS = [('two', 0.0, 3.0), ('rep', 3.0, 9.4), ('two', 9.4, 15.9)]
BLACK_AT = 15.9
DUR = 16.4
TITLE = 'THE PATRIOTS'


def level(who, t):
    """How loud this person's voice is now (0-1). Placeholder: a steady syllable rhythm."""
    for w, a, b, _, _, rec in LINES:
        if w == who and a <= t < b:
            u = t - a
            v = abs(math.sin(math.pi * 4.6 * u)) * (1.0 if math.sin(2 * math.pi * 0.85 * u + 1) > -0.7 else 0.15)
            return min(1.0, v * min(1.0, u / 0.08) * min(1.0, (b - t) / 0.08))
    return 0.0


# ---------------------------------------------------------------------------------------- the acting
# Arm keys in the protester's own units (+x is our right; his right arm is our 'L').
REST = {'L': ((-205, 280), (-195, 480), 'fist'), 'R': ((205, 280), (195, 480), 'fist')}
HIP_L = ((-300, 230), (-180, 390), 'fist')
HIP_R = ((300, 230), (180, 390), 'fist')
THUMB = ((300, 180), (280, -10), 'thumb', -0.55)
JERK = ((320, 140), (345, -50), 'thumb', -0.45)
MIC = ((-250, 190), (-95, 10), 'fist')            # pretending to hold a microphone
FLAP = ((250, 150), (300, 30), 'flap')
TEMPLE = ((240, 40), (118, -118), 'point_up')     # "I think": tapping his temple
JAB = ((-330, 60), (-520, 15), 'point')
PRO_ARMS = [
    (0.0, {'L': HIP_L, 'R': THUMB}), (0.55, {'L': HIP_L, 'R': JERK}), (0.78, {'L': HIP_L, 'R': THUMB}),
    (1.55, {'L': HIP_L, 'R': JERK}), (1.78, {'L': HIP_L, 'R': THUMB}),
    (2.2, {'L': HIP_L, 'R': ((260, 230), (380, 250), 'palm')}),
    (9.4, REST), (9.6, {'L': MIC, 'R': FLAP}), (11.5, {'L': MIC, 'R': TEMPLE}), (12.25, {'L': MIC, 'R': FLAP}),
    (13.35, {'L': JAB, 'R': HIP_R}),
]
JABS = [13.45, 13.78, 14.12, 14.45]


def pro_state(t):
    arms = keyed(PRO_ARMS, t, 0.18)
    lv = level('pro', t)
    st = dict(arms=arms, turn=-0.3, look=-0.7, lid=3, brows='flat', puff=0.0, shrug=0.0, tilt=0.0,
              head_dx=0.0, head_dy=-5 * lv, lv=lv)
    if t < 3.0:                                    # boorish, puffing up, chin out
        st.update(puff=smooth(t / 0.6), head_dy=-8 * smooth(t / 0.6) - 6 * lv, brows='flat', lid=4)
        if t > 2.15:                               # "love!": head jutting at her
            k = smooth((t - 2.15) / 0.2)
            st.update(head_dx=-14 * k, tilt=0.07 * k, look=-1.0)
    elif t < 13.3:                                 # the mimicry: wobbling head, prissy little flaps
        k = smooth((t - 9.5) / 0.25)
        w = math.sin(2 * math.pi * 2.3 * t)
        st.update(tilt=0.13 * w * k, head_dx=10 * w * k, shrug=(0.25 + 0.2 * math.sin(2 * math.pi * 2.3 * t + 1)) * k,
                  brows='raised', lid=5, look=0.4, puff=0.0)
        if 11.5 <= t < 12.25:  # tap, tap
            a = st['arms']
            el, wr, sh = a['R'][:3]
            st['arms'] = dict(a, R=(el, (wr[0] + 6 * abs(math.sin(math.pi * 5 * (t - 11.5))), wr[1]), sh))
    else:                                          # "You're a traitor, love!" and the hold
        st.update(brows='cross', lid=0, look=-1.0, puff=1.0, head_dx=-16, head_dy=-4 * lv)
        a = st['arms']
        el, wr, sh = a['L'][:3]
        jab = sum(math.exp(-((t - j) / 0.07) ** 2) for j in JABS)
        st['arms'] = dict(a, L=((el[0] - 25 * jab, el[1]), (wr[0] - 45 * jab, wr[1] + 6 * jab), sh))
    if st['arms']['R'][2] == 'flap':
        st['flap'] = 0.5 * math.sin(2 * math.pi * 3.1 * t)
    st['blink'] = any(b <= t < b + 0.12 for b in (1.2, 10.3, 12.9))
    return st


def rep_state(t, view):
    lv = level('rep', t)
    m = 'line' if lv < 0.12 else 'small' if lv < 0.35 else ['mid', 'open'][int(t * 12) % 2]
    blink = any(b <= t < b + 0.14 for b in (1.9, 5.6, 8.2, 11.7)) or 15.05 <= t < 15.35  # one slow blink in the hold
    if view == 'two':
        arms = {'L': ((-140, 290), (-128, 480), 'fist'), 'R': ((270, 150), (390, 90), 'fist')}
        return dict(REPORTER, arms=arms, mouth=m, blink=blink, turn=0.55, look=0.9), (520, -10)
    arms = {'L': ((-140, 290), (-128, 480), 'fist'), 'R': ((190, 250), (92, 80), 'fist')}
    look = 0.85 if t > 3.6 else 0.6
    return dict(REPORTER, arms=arms, mouth=m, blink=blink, turn=0.45, look=look), (36, -40)


REPORTER = dict(skin=B.PINK, hw=64, hh=88, jaw='soft', hair='bob', hair_c=AUBURN, brow_c=(118, 50, 32), brow_w=2.8,
                outfit='blouse', jacket=CAMEL, shirt=SCARF, trousers=(46, 46, 54), full=True, shoulders=128,
                bottom=620, age=True, earring=True, pose='custom', stance=8)


# ------------------------------------------------------------------------------------------ drawing

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


def ctext(img, cam, x, y, s, size, fill, font=B.SANS, angle=0.0):
    """Lettering centred on (x, y), in the given frame's units, optionally turned."""
    f = ImageFont.truetype(font, max(4, int(cam.S(size))))
    l, t_, r, b = f.getbbox(s)
    lay = Image.new('RGBA', (r - l + 6, b - t_ + 6), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((3 - l, 3 - t_), s, font=f, fill=fill)
    if angle:
        lay = lay.rotate(-math.degrees(angle), Image.BICUBIC, expand=True)
    X, Y = cam.P(x, y)
    img.alpha_composite(lay, (int(X - lay.width / 2), int(Y - lay.height / 2)))


def patch(img, p, sh, el, kind):
    """A round sew-on badge on the upper arm."""
    mx, my = sh[0] + 0.42 * (el[0] - sh[0]), sh[1] + 0.42 * (el[1] - sh[1])
    r = 33
    if kind == 'PP':
        p.ell(mx, my, r, r, (26, 26, 30), INK, 2.0)
        p.ell(mx, my, r * 0.8, r * 0.8, (246, 244, 238), None)
        ctext(img, p.cam, mx, my + 1, 'PP', 25, RED)
        return
    # his own felt-tip doodle on a blank patch: crude, wobbly, a child's drawing
    p.ell(mx, my, r, r, (232, 228, 212), (110, 106, 96), 1.6)
    q = lambda pts: [(mx + x * r / 30, my + y * r / 30) for x, y in pts]
    felt = (24, 24, 30)
    p.line(q([(-9, 2), (0, -9), (5, -15), (9, -16), (12, -13), (11, -9), (3, -2), (-3, 6)]), felt, 1.5)
    p.line(q([(-15, 8), (-17, 13), (-13, 18), (-8, 17), (-6, 12), (-9, 6), (-13, 5), (-15, 8)]), felt, 1.5)
    p.line(q([(-6, 12), (-3, 18), (2, 19), (5, 14), (2, 8), (-3, 6)]), felt, 1.5)
    p.line(q([(9, -15), (11, -13)]), felt, 1.2)
    for k in range(5):  # the stream, in yellow felt tip
        a, b = k / 5, (k + 0.6) / 5
        p.line(q([(13 + 14 * a, -15 + 30 * a * a), (13 + 14 * b, -15 + 30 * b * b)]), (232, 192, 30), 2.0)


def hand(img, p, el, wr, shape, skin, extra=None, t=0.0, flap=0.0):
    dx, dy = wr[0] - el[0], wr[1] - el[1]
    n = math.hypot(dx, dy) or 1
    d = (dx / n, dy / n)
    c = (wr[0] + d[0] * 14, wr[1] + d[1] * 14)
    if shape == 'thumb':  # a fist with the thumb jerked out
        a = extra if extra is not None else -0.5
        B.finger(p, (c[0] + 8 * math.cos(a), c[1] + 8 * math.sin(a)), (math.cos(a), math.sin(a)), 30, skin, 9)
        p.ell(c[0], c[1], 25, 23, skin, INK, 2.6)
        for k in range(3):
            p.line([(c[0] - 14, c[1] - 8 + 8 * k), (c[0] + 10, c[1] - 10 + 8 * k)], B.dk(skin, 0.8), 1.8)
        return
    if shape == 'flap':  # a limp wrist, the hand dangling and flapping
        a = math.pi / 2 + 0.35 + flap
        u = (math.cos(a), math.sin(a))
        nx, ny = -u[1], u[0]
        pts = [(wr[0] + nx * 18, wr[1] + ny * 18), (wr[0] + u[0] * 44 + nx * 20, wr[1] + u[1] * 44 + ny * 20),
               (wr[0] + u[0] * 62, wr[1] + u[1] * 62), (wr[0] + u[0] * 44 - nx * 18, wr[1] + u[1] * 44 - ny * 18),
               (wr[0] - nx * 18, wr[1] - ny * 18)]
        p.poly(curve(pts, 4), skin, INK, 2.4)
        for k in (-1, 1):
            p.line([(wr[0] + u[0] * 30 + nx * 7 * k, wr[1] + u[1] * 30 + ny * 7 * k),
                    (wr[0] + u[0] * 52 + nx * 6 * k, wr[1] + u[1] * 52 + ny * 6 * k)], B.dk(skin, 0.8), 1.6)
        return
    B.gesture_hand(p, el, wr, shape, skin, extra, t)


def flag(p, x0, y0, t, phase, w=300, h=190):
    """A St George flag streaming in the wind from a pole top at (x0, y0)."""
    def at(u, v):
        wave_ = math.sin(6.0 * u - t * 9 + phase) * 16 * u
        return (x0 + w * u * (1 - 0.06 * v), y0 + h * v + wave_ + 10 * u)

    def quad(u0, u1, v0, v1, colr, line=None):
        us = np.linspace(u0, u1, 10)
        pts = [at(u, v0) for u in us] + [at(u, v1) for u in us[::-1]]
        p.poly(pts, colr, line, 2.2)
    quad(0, 1, 0, 1, (246, 246, 242), INK)
    quad(0, 1, 0.41, 0.59, RED)
    quad(0.43, 0.57, 0, 1, RED)


def protester(img, cam, x, y, s, st, t=0.0, doodle=True, pole=None):
    """The masked protester (or one of his mates). Neck base at world (x, y)."""
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    puff, shr = st.get('puff', 0.0), -26 * st.get('shrug', 0.0)
    sw = 172 * (1 + 0.05 * puff)
    B.legs(img, p, dict(trousers=COMBAT, stance=36))
    for sgn in (-1, 1):  # cargo pockets
        p.poly([(sgn * 36, 600), (sgn * 100, 600), (sgn * 98, 700), (sgn * 40, 700)], B.dk(COMBAT, 0.86), INK, 2.0)
        p.line([(sgn * 34, 618), (sgn * 102, 618)], INK, 1.8)
    # the balaclava's neck, the collar, a thick-set body with a belly
    p.poly([(-40, -92), (40, -92), (44, 4), (-44, 4)], BALA, INK, 2.4)
    body = [(-52, -8), (-sw * 0.8, 10 + shr), (-sw, 52 + shr), (-sw - 6, 200), (-sw - 16, 340), (-sw - 8, 440),
            (-sw + 18, 482), (sw - 18, 482), (sw + 8, 440), (sw + 16, 340), (sw + 6, 200), (sw, 52 + shr),
            (sw * 0.8, 10 + shr), (52, -8)]
    p.poly(body, JACKET, INK, 2.6)
    soft(img, L, [(-110, 260), (110, 260), (130, 430), (-130, 430)], (120, 120, 132), 0.22, 16)
    p.line(oval(0, 300, 128, 150, 22, 0.45, math.pi - 0.45), (18, 18, 22), 2.0)
    p.poly([(-sw + 16, 456), (sw - 16, 456), (sw - 18, 482), (-sw + 18, 482)], B.dk(JACKET, 0.8), INK, 2.0)
    p.line([(0, 28), (6, 200), (12, 340), (6, 470)], (96, 96, 104), 2.2)
    soft(img, L, [(sw * 0.4, 40), (sw, 70), (sw + 10, 440), (sw * 0.5, 450)], (0, 0, 0), 0.3, 10)
    soft(img, L, [(-sw * 0.8, 40), (-sw * 0.3, 40), (-sw * 0.4, 200), (-sw * 0.9, 200)], (150, 150, 165), 0.16 + 0.1 * puff, 12)
    p.poly([(-64, -24), (64, -24), (76, 30), (-76, 30)], B.lt(JACKET, 1.35), INK, 2.4)
    # the head, tilting from the neck
    hx, hy = st.get('head_dx', 0.0), -150 + st.get('head_dy', 0.0)
    R = Rot(L, st.get('tilt', 0.0))
    ph = B.Pen(img, R)
    hw, hh, turn = 76, 92, st.get('turn', 0.0)
    for sgn in (-1, 1):
        ph.poly(oval(hx + sgn * (hw + 2) - turn * 6, hy + 6, 12, 22), BALA, INK, 2.4)
    ph.poly(B.head_outline(hx, hy, hw, hh, 'round'), BALA, INK, 2.6)
    for k in range(-4, 5):  # the knit's ribs
        ph.line([(hx + k * 15, hy - hh * 0.92 + abs(k) * 7), (hx + k * 16.5, hy + hh * 1.0 - abs(k) * 4)], (50, 50, 57), 1.4)
    soft(img, R, [(hx - hw * 0.7, hy - hh * 0.7), (hx - hw * 0.2, hy - hh * 0.9), (hx - hw * 0.4, hy + 20),
                  (hx - hw * 0.8, hy)], (160, 160, 175), 0.18, 10)
    fx = hx + turn * hw * 0.22
    lv = st.get('lv', 0.0)
    if lv > 0.05:  # the knit moving over his mouth as he talks
        soft(img, R, oval(fx - 2, hy + 56, 22, 8 + 8 * lv, 16), (95, 95, 105), 0.35 * lv, 4)
    ph.poly(curve([(fx - 62, hy - 46), (fx + 58, hy - 46), (fx + 60, hy + 10), (fx - 64, hy + 10)], 5), EYE_SKIN, INK, 2.4)
    look, lid = st.get('look', 0.0), st.get('lid', 0)
    for sgn in (-1, 1):
        ex, ey = fx - 2 + sgn * 30, hy - 14
        if st.get('blink'):
            ph.line([(ex - 16, ey), (ex, ey + 3), (ex + 16, ey)], INK, 2.4)
        else:
            ph.poly([(ex - 17, ey), (ex - 8, ey - 8), (ex + 8, ey - 8), (ex + 17, ey), (ex + 8, ey + 7), (ex - 8, ey + 7)],
                    (250, 250, 248), INK, 2.0)
            ph.ell(ex + look * 7, ey + 1, 4.5, 4.5, INK, None)
            if lid > 0:
                ph.poly([(ex - 18, ey - 2), (ex - 8, ey - 10), (ex + 8, ey - 10), (ex + 18, ey - 2), (ex + 17, ey - 1 + lid),
                         (ex + 8, ey - 9 + lid), (ex - 8, ey - 9 + lid), (ex - 17, ey - 1 + lid)], B.dk(EYE_SKIN, 0.84), None)
            ph.line([(ex - 17, ey - 1 + lid), (ex - 8, ey - 9 + lid), (ex + 8, ey - 9 + lid), (ex + 17, ey - 1 + lid)], INK, 2.6)
        bc, br = (104, 74, 54), st.get('brows', 'flat')
        if br == 'cross':
            ph.line([(ex - sgn * 4, ey - 13), (ex + sgn * 8, ey - 19), (ex + sgn * 21, ey - 25)], bc, 4.4)
        elif br == 'raised':
            ph.line([(ex - sgn * 13, ey - 23), (ex, ey - 29), (ex + sgn * 15, ey - 25)], bc, 3.8)
        else:
            ph.line([(ex - sgn * 15, ey - 19), (ex + sgn * 17, ey - 18)], bc, 4.4)
    # a mate's flagpole, gripped in his right fist
    arms = st['arms']
    if pole is not None:
        el, wr = arms['R'][0], arms['R'][1]
        top = (wr[0] + 14, wr[1] - 640)
        p.line([(wr[0] + 4, wr[1] + 90), top], (120, 96, 70), 7)
        flag(p, top[0], top[1], t, pole)
    for side, sgn in (('L', -1), ('R', 1)):
        g = arms[side]
        sh = (sgn * (sw - 16), 60 + shr)
        B.arm(p, sh, g[0], g[1], SLEEVE, w=36)
        patch(img, p, sh, g[0], 'doodle' if (side == 'L' and doodle) else 'PP')
        hand(img, p, g[0], g[1], g[2], EYE_SKIN, g[3] if len(g) > 3 else None, t, st.get('flap', 0.0))


def mic(img, L, wr, el, target):
    """The reporter's microphone in her fist, pointing at target (her own units), with its BBQ flag."""
    p = B.Pen(img, L)
    dx, dy = wr[0] - el[0], wr[1] - el[1]
    n = math.hypot(dx, dy) or 1
    c = (wr[0] + dx / n * 14, wr[1] + dy / n * 14)
    ux, uy = target[0] - c[0], target[1] - c[1]
    m = math.hypot(ux, uy) or 1
    ux, uy = ux / m, uy / m
    nx, ny = -uy, ux
    a, b = (c[0] - ux * 50, c[1] - uy * 50), (c[0] + ux * 96, c[1] + uy * 96)
    p.poly([(a[0] + nx * 9, a[1] + ny * 9), (b[0] + nx * 11, b[1] + ny * 11), (b[0] - nx * 11, b[1] - ny * 11),
            (a[0] - nx * 9, a[1] - ny * 9)], (26, 26, 30), INK, 2.2)
    hx, hy = c[0] + ux * 112, c[1] + uy * 112
    p.ell(hx, hy, 24, 24, (120, 124, 130), INK, 2.4)
    for k in (-1, 0, 1):
        p.line([(hx - 20, hy + 9 * k), (hx + 20, hy + 9 * k)], (80, 84, 90), 1.4)
        p.line([(hx + 9 * k, hy - 20), (hx + 9 * k, hy + 20)], (80, 84, 90), 1.4)
    # the flag: a white cube with three black blocks lettered B B Q
    fx, fy = c[0] + ux * 58, c[1] + uy * 58
    ang = math.atan2(uy, ux) + math.pi / 2
    sz = 52
    px = max(12, int(L.S(sz)))
    lay = Image.new('RGBA', (px, px), (248, 248, 246, 255))
    d = ImageDraw.Draw(lay)
    d.rectangle([0, 0, px - 1, px - 1], outline=(0, 0, 0), width=max(1, px // 26))
    f = ImageFont.truetype(B.SANS, max(5, int(px * 0.24)))
    bw = px * 0.27
    for i, ch in enumerate('BBQ'):
        x0 = px * 0.065 + i * (bw + px * 0.04)
        d.rectangle([x0, px * 0.36, x0 + bw, px * 0.36 + bw], fill=(14, 14, 16))
        d.text((x0 + bw / 2, px * 0.36 + bw / 2), ch, font=f, fill=(255, 255, 255), anchor='mm')
    lay = lay.rotate(-math.degrees(ang), Image.BICUBIC, expand=True)
    X, Y = L.P(fx, fy)
    img.alpha_composite(lay, (int(X - lay.width / 2), int(Y - lay.height / 2)))
    skin = B.PINK  # her fist round the handle
    p.ell(c[0], c[1], 25, 23, skin, INK, 2.6)
    for k in range(3):
        p.line([(c[0] - 14, c[1] - 8 + 8 * k), (c[0] + 10, c[1] - 10 + 8 * k)], B.dk(skin, 0.8), 1.8)


def reporter(img, cam, x, y, s, sp, target, t):
    B.person(img, cam, x, y, s, sp, t)
    el, wr = sp['arms']['R'][0], sp['arms']['R'][1]
    mic(img, B.Local(cam, x, y, s), wr, el, target)


# --------------------------------------------------------------------------------------- the location

VIEWS = {'two': dict(VX=450, VY=760, Hg=840, S0=0.8), 'rep': dict(VX=560, VY=700, Hg=1220, S0=1.1)}


class Ground:
    def __init__(self, v):
        self.__dict__.update(v)

    def P(self, X, z, Y=0.0):
        return (self.VX + X * self.S0 / z, self.VY + (self.Hg - Y * self.S0) / z)

    def feet(self, X, z):
        return self.P(X, z), self.S0 / z


def sky(img, v):
    S = B.SS
    h = img.height
    y = np.arange(h)[:, None] / S
    top, hor, grd = np.array((150, 160, 170.0)), np.array((208, 211, 211.0)), np.array((150, 150, 146.0))
    k = np.clip(y / v['VY'], 0, 1) ** 1.4
    col = np.where(y < v['VY'], top * (1 - k) + hor * k, grd)
    a = np.broadcast_to(col[:, None, :], (h, img.width, 3)).astype(np.uint8)
    img.paste(Image.fromarray(np.ascontiguousarray(a), 'RGB'))


def car(p, g, X, z, colr, lorry=False):
    k = g.S0 / z
    lw = max(0.6, min(2.4, 14 * k))
    P = lambda dx, Y: g.P(X + dx, z, Y)
    if lorry:
        p.poly([P(-900, 1000), P(900, 1000), P(900, 2800), P(-900, 2800)], (226, 228, 230), INK, lw)
        p.poly([P(-820, 220), P(820, 220), P(820, 2050), P(-820, 2050)], colr, INK, lw)
        p.poly([P(-700, 1250), P(700, 1250), P(680, 1850), P(-680, 1850)], (150, 166, 178), INK, lw * 0.8)
        p.poly([P(-500, 400), P(500, 400), P(500, 800), P(-500, 800)], B.dk(colr, 0.6), None)
        for sgn in (-1, 1):
            p.poly([P(sgn * 760, 0), P(sgn * 500, 0), P(sgn * 500, 300), P(sgn * 760, 300)], (24, 24, 26), None)
            p.ell(*P(sgn * 640, 600), 90 * k, 70 * k, (250, 246, 220), None)
        return
    p.poly([P(-600, 120), P(600, 120), P(620, 760), P(-620, 760)], colr, INK, lw)
    p.poly([P(-470, 760), P(470, 760), P(380, 1120), P(-380, 1120)], B.dk(colr, 0.9), INK, lw)
    p.poly([P(-420, 790), P(420, 790), P(350, 1080), P(-350, 1080)], (160, 176, 188), None)
    p.poly([P(-160, 230), P(160, 230), P(160, 330), P(-160, 330)], (246, 246, 240), None)
    for sgn in (-1, 1):
        p.poly([P(sgn * 560, 0), P(sgn * 380, 0), P(sgn * 380, 160), P(sgn * 560, 160)], (24, 24, 26), None)
        p.ell(*P(sgn * 430, 560), 80 * k, 50 * k, (250, 246, 220), None)


def background(img, view, t):
    v = VIEWS[view]
    g = Ground(v)
    cam = B.Cam()
    p = B.Pen(img, cam)
    sky(img, v)
    VY = v['VY']
    for i, (cx, cy, rx, ry) in enumerate([(160, 420, 300, 70), (700, 520, 380, 60), (420, 640, 420, 40), (950, 380, 260, 60)]):
        soft(img, cam, oval(cx + t * (6 + 2 * i), cy, rx, ry, 30), (228, 230, 232), 0.45, 30)
    # the sea, and the white cliffs faint in the haze
    p.poly([(-20, VY - 14), (1100, VY - 14), (1100, VY + 2), (-20, VY + 2)], (132, 146, 150), None)
    p.poly(curve([(680, VY), (720, VY - 40), (820, VY - 58), (960, VY - 66), (1120, VY - 74), (1120, VY + 2)], 4),
           (224, 226, 218), None)
    p.line([(712, VY - 38), (820, VY - 60), (960, VY - 68), (1120, VY - 76)], (156, 168, 146), 3)
    for k in range(8):
        x = 740 + 45 * k
        p.line([(x, VY - 46 - k * 2.5), (x - 6, VY - 6)], (204, 206, 198), 1.5)
    # the road, its lanes, the crash barriers
    p.poly([g.P(-4700, 300), g.P(4700, 300), g.P(4700, 0.5), g.P(-4700, 0.5)], (110, 112, 114), None)
    for X in (-2350, 0, 2350):
        for k in range(22):
            z0 = 1.05 * 1.28 ** k
            p.poly([g.P(X - 70, z0), g.P(X + 70, z0), g.P(X + 70, z0 * 1.1), g.P(X - 70, z0 * 1.1)], (214, 214, 208), None)
    for X in (-5300, 5300):
        zs = np.geomspace(0.6, 150, 40)
        p.poly([g.P(X, z, 520) for z in zs] + [g.P(X, z, 300) for z in zs[::-1]], (172, 176, 180), INK, 1.6)
        for z in np.geomspace(0.6, 60, 18):
            p.line([g.P(X, z, 0), g.P(X, z, 520)], (90, 94, 98), max(1, 10 / z))
    # the border control booths and canopy far off, and the sign on its gantry
    for X in range(-4000, 4001, 1600):
        p.poly([g.P(X - 450, 70), g.P(X + 450, 70), g.P(X + 450, 70, 1900), g.P(X - 450, 70, 1900)], (96, 106, 116), INK, 0.8)
        p.poly([g.P(X - 300, 70, 900), g.P(X + 300, 70, 900), g.P(X + 300, 70, 1600), g.P(X - 300, 70, 1600)],
               (170, 184, 192), None)
    p.poly([g.P(-5600, 70, 3200), g.P(5600, 70, 3200), g.P(5600, 70, 3800), g.P(-5600, 70, 3800)], (214, 216, 218), INK, 0.9)
    for X in (-5200, 5200):
        p.line([g.P(X, 28), g.P(X, 28, 3950)], (120, 124, 128), 2.4)
    p.poly([g.P(-5200, 28, 3800), g.P(5200, 28, 3800), g.P(5200, 28, 3950), g.P(-5200, 28, 3950)], (120, 124, 128), None)
    p.poly([g.P(-3000, 28, 2650), g.P(3000, 28, 2650), g.P(3000, 28, 3820), g.P(-3000, 28, 3820)], (30, 56, 120),
           (240, 240, 240), 1.6)
    sx, sy = g.P(0, 28, 3235)
    ctext(img, cam, sx, sy, 'BORDER CONTROL', 600 * v['S0'] / 28 * 0.85, (255, 255, 255))
    # the queue, stopped behind the protest, far to near
    rng = np.random.default_rng(3)
    cols = [(150, 40, 46), (60, 70, 90), (196, 196, 200), (40, 42, 48), (90, 110, 130), (200, 200, 190), (110, 60, 40)]
    jobs = []
    for li, X in enumerate((-3525, -1175, 1175, 3525)):
        z = 9.0 + 0.6 * li
        n = 0
        while z < 48:
            lorry = li in (0, 3) and n % 3 == 1
            jobs.append((z, X + rng.uniform(-150, 150), cols[rng.integers(len(cols))], lorry))
            z += (2.6 if lorry else 1.6) * (1 + 0.05 * n)
            n += 1
    for z, X, c, lorry in sorted(jobs, reverse=True):
        car(p, g, X, z, c, lorry)
    return g


def stuck(img, g, t, where):
    """The Border Force officer and a family with suitcases, stuck behind the blockade."""
    cam = B.Cam()
    p = B.Pen(img, cam)
    for X, z, sp, kid in where['family']:
        (fx, fy), s = g.feet(X, z)
        if kid:
            s *= 0.62
        B.person(img, cam, fx, fy - 928 * s, s, sp, t)
    for X, z, colr in where['cases']:
        k = g.S0 / z
        P = lambda dx, Y: g.P(X + dx, z, Y)
        p.poly([P(-190, 30), P(190, 30), P(190, 600), P(-190, 600)], colr, INK, max(0.8, 8 * k))
        p.line([P(-100, 600), P(-100, 900), P(100, 900), P(100, 600)], (40, 40, 44), max(1, 14 * k))
        for sgn in (-1, 1):
            p.ell(*P(sgn * 130, 20), 30 * k, 30 * k, (20, 20, 22), None)
    X, z = where['officer']
    (ox, oy), s = g.feet(X, z)
    sp = dict(skin=B.OLIVE, hw=70, hh=88, jaw='square', hair='crop', hair_c=(40, 32, 28), outfit='jumper', jacket=HIVIS,
              trousers=(30, 32, 40), full=True, pose='custom', mouth='set', look=-0.4,
              arms={'L': ((-210, 260), (-250, 400), 'palm'), 'R': ((210, 260), (250, 400), 'palm')})
    B.person(img, cam, ox, oy - 928 * s, s, sp, t)
    L = B.Local(cam, ox, oy - 928 * s, s)
    q = B.Pen(img, L)
    for yb in (300, 370):
        q.poly([(-150, yb), (150, yb), (150, yb + 26), (-150, yb + 26)], (196, 200, 206), None)
    ctext(img, L, -60, 130, 'BORDER', 30, (20, 20, 24))
    ctext(img, L, -60, 168, 'FORCE', 30, (20, 20, 24))


FAMILY_SP = [
    dict(skin=B.PALE, hw=70, hh=88, jaw='round', hair='side', hair_c=(90, 64, 44), outfit='jumper', jacket=(70, 110, 90),
         trousers=(60, 70, 96), full=True, pose='side', mouth='line', look=0.3),
    dict(skin=B.PALE, hw=64, hh=86, jaw='soft', hair='long', hair_c=(170, 130, 80), outfit='blouse', jacket=(120, 60, 80),
         trousers=(40, 44, 60), full=True, pose='side', mouth='line', look=0.3),
    dict(skin=B.PALE, hw=66, hh=82, jaw='soft', hair='crop', hair_c=(150, 110, 70), outfit='jumper', jacket=(200, 80, 60),
         trousers=(50, 60, 90), full=True, pose='side', mouth='line', look=0.5),
    dict(skin=B.PALE, hw=66, hh=82, jaw='soft', hair='bob', hair_c=(170, 130, 80), outfit='jumper', jacket=(90, 120, 190),
         trousers=(50, 50, 60), full=True, pose='side', mouth='line', look=-0.5),
]
MATE = dict(arms={'L': ((-205, 280), (-195, 480), 'fist'), 'R': ((240, 150), (205, -20), 'fist')}, turn=0.1,
            look=-0.3, lid=3, brows='flat')


def mates(img, g, t, where):
    cam = B.Cam()
    for i, (X, z, look) in enumerate(where):
        (fx, fy), s = g.feet(X, z)
        st = dict(MATE, look=look, blink=(t + i * 1.3) % 4.1 < 0.12)
        protester(img, cam, fx, fy - 928 * s, s, st, t, doodle=False, pole=1.7 * i)


def gulls(img, t):
    cam = B.Cam()
    p = B.Pen(img, cam)
    for i, (x0, y0, sp, ph) in enumerate([(120, 470, 22, 0.0), (760, 400, 16, 2.0), (980, 560, 30, 4.0)]):
        x = (x0 + sp * t) % 1200 - 60
        y = y0 + 12 * math.sin(t * 0.8 + ph)
        f = math.sin(t * 7 + ph)
        w = 22
        p.line([(x - w, y - 6 * f), (x - w * 0.45, y - 8 - 4 * f), (x, y)], (60, 60, 64), 2.6)
        p.line([(x, y), (x + w * 0.45, y - 8 - 4 * f), (x + w, y - 6 * f)], (60, 60, 64), 2.6)


# ------------------------------------------------------------------------------------------- the shots

WHERE_TWO = dict(family=[(250, 4.4, FAMILY_SP[0], False), (520, 4.4, FAMILY_SP[1], False), (380, 4.2, FAMILY_SP[2], True)],
                 cases=[(700, 4.3, (60, 90, 150)), (-60, 4.3, (180, 60, 60))], officer=(-200, 3.8))
MATES_TWO = [(-1150, 2.4, 0.4), (1250, 2.5, -0.6), (1900, 2.7, -0.2)]
WHERE_REP = dict(family=[(-980, 2.7, FAMILY_SP[0], False), (-660, 2.7, FAMILY_SP[1], False),
                         (-830, 2.5, FAMILY_SP[2], True), (-1150, 2.5, FAMILY_SP[3], True)],
                 cases=[(-560, 2.6, (60, 90, 150)), (-1350, 2.6, (180, 60, 60))], officer=(470, 2.4))
MATES_REP = [(1150, 3.3, -0.5)]


def caption(img, s, italic=False, bottom=1480):
    S = B.SS
    f = ImageFont.truetype(B.SANS, 50 * S)
    rows = B.wrap(s, f, 780 * S)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i, row in enumerate(rows):
        y = (bottom - 34 - 64 * (len(rows) - 1 - i)) * S
        d.text((480 * S, y), row, font=f, fill=(255, 255, 255), anchor='mm', stroke_width=5 * S, stroke_fill=(0, 0, 0))
    if italic:  # lean the letters: simple italics
        k, yc = 0.2, (bottom - 34) * S
        lay = lay.transform(lay.size, Image.AFFINE, (1, k, -k * yc, 0, 1, 0), Image.BICUBIC)
    img.alpha_composite(lay)


def frame_image(t):
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    view = next(v for v, a, b in SHOTS if a <= t < b)
    img = B.canvas()
    g = background(img, view, t)
    gulls(img, t)
    cam = B.Cam()
    if view == 'two':
        stuck(img, g, t, WHERE_TWO)
        mates(img, g, t, MATES_TWO)
        (_, fy), s = g.feet(0, 1.0)
        sp, target = rep_state(t, view)
        B.person(img, cam, 220, fy - 928 * s, s, sp, t)
        protester(img, cam, 670, fy - 928 * s, s, pro_state(t), t)
        mic(img, B.Local(cam, 220, fy - 928 * s, s), sp['arms']['R'][1], sp['arms']['R'][0], target)
    else:
        stuck(img, g, t, WHERE_REP)
        mates(img, g, t, MATES_REP)
        (_, fy), s = g.feet(0, 1.0)
        sp, target = rep_state(t, view)
        reporter(img, cam, 430, fy - 928 * s, s, sp, target, t)
    for w, a, b, text, italic, _ in LINES:
        if a - 0.05 <= t < b + 0.25 and not any(a2 - 0.05 <= t for _, a2, _, _, _, _ in LINES if a2 > a):
            caption(img, text, italic)
    if t < 2.0:  # small and high over the action, gone by 2 s (the full-size title is on the cover)
        B.title(img, TITLE, alpha=1.0 if t < 1.6 else 1.0 - (t - 1.6) / 0.4, maxw=430)
    return img


# ----------------------------------------------------------------------------------------------- sound

rng = np.random.default_rng(7)


def place(mix, snd, at, gain=1.0):
    s = int(at * SR)
    e = min(len(mix), s + len(snd))
    if e > s:
        mix[s:e] += snd[:e - s] * gain


def gull_call():
    out = []
    for dur in (0.32, 0.3, 0.16, 0.16):
        n = int(dur * SR)
        tt = np.arange(n) / SR
        f = 1550 - 650 * (tt / dur) ** 0.7
        ph = 2 * np.pi * np.cumsum(f) / SR
        tone = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)
        tone *= (0.65 + 0.35 * np.sin(2 * np.pi * 58 * tt)) * np.sin(np.pi * tt / dur) ** 0.6
        out += [tone, np.zeros(int(0.1 * SR))]
    return onepole_lp(np.concatenate(out), 3500)


def engines(n):
    tt = np.arange(n) / SR
    out = np.zeros(n)
    for f0, g in ((24.0, 1.0), (27.5, 0.7), (31.0, 0.5), (42.0, 0.35)):
        wob = 1 + 0.01 * np.sin(2 * np.pi * rng.uniform(0.2, 0.6) * tt)
        ph = 2 * np.pi * np.cumsum(f0 * wob) / SR
        x = sum(np.sin(h * ph + rng.uniform(0, 6.3)) / h ** 0.7 for h in range(2, 14))
        out += g * x
    out = onepole_lp(out, 380) + 0.15 * onepole_lp(rng.standard_normal(n), 300)
    from scipy.signal import butter, sosfilt
    return normal(sosfilt(butter(2, 70, 'high', fs=SR, output='sos'), out))


def wind(n):
    tt = np.arange(n) / SR
    gust = 0.55 + 0.25 * np.sin(2 * np.pi * 0.13 * tt + 1) + 0.2 * np.sin(2 * np.pi * 0.31 * tt + 2)
    low = normal(onepole_lp(onepole_lp(rng.standard_normal(n), 500), 500))
    hi = bandnoise(n, 700, 1800)
    return normal(low * gust + 0.25 * hi * gust ** 3)


def horn():
    n = int(0.9 * SR)
    tt = np.arange(n) / SR
    x = sum(sum(np.sin(2 * np.pi * f * h * tt) / h for h in range(1, 9)) for f in (311.0, 370.0))
    env = np.minimum(1, tt / 0.04) * np.minimum(1, (0.9 - tt) / 0.1)
    return normal(reverb(onepole_lp(x * env, 1400), 1.2, 0.4))


def soundtrack():
    n = int(DUR * SR)
    mix = np.zeros(n)
    end = int(BLACK_AT * SR)
    amb = 0.32 * wind(end) + 0.22 * engines(end)
    mix[:end] += amb
    call = gull_call()
    for at, g in ((0.6, 0.10), (4.9, 0.07), (10.8, 0.08), (14.9, 0.05)):
        place(mix, call, at, g)
    place(mix, horn(), 15.0, 0.12)   # a lorry in the queue, far off, during the hold
    for w, a, b, _, _, rec in LINES:  # the voices, exactly as recorded (volume only)
        if rec:
            f, s0, s1 = rec
            seg = load(os.path.join(HERE, 'audio', f))[int(s0 * SR):int(s1 * SR)]
            place(mix, seg / (np.abs(seg).max() + 1e-9), a, 0.85)
    k = int(0.01 * SR)
    mix[end - k:end] *= np.linspace(1, 0, k)   # hard cut to black: silence
    mix[end:] = 0
    return mix / max(1.0, np.abs(mix).max() / 0.95)


def write_wav(path, x):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def render_frame(args):
    i, size, ss = args
    B.SS = ss
    return np.asarray(frame_image(i / FPS).convert('RGB').resize(size, Image.LANCZOS)).tobytes()


def render(out, size, crf, ss):
    import imageio_ffmpeg
    from multiprocessing import Pool
    wav = out + '.wav'
    write_wav(wav, soundtrack())
    n = int(round(DUR * FPS))
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{size[0]}x{size[1]}', '-r', str(FPS), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '128k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for f, fr in enumerate(pool.imap(render_frame, [(i, size, ss) for i in range(n)], chunksize=2)):
            p.stdin.write(fr)
            if f % 48 == 0:
                print(f'frame {f}/{n}', flush=True)
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print(f'done: {out} ({os.path.getsize(out) / 1e6:.1f} MB)', flush=True)


def main():
    mode = sys.argv[1]
    if mode == 'stills':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for s in sys.argv[3:]:
            frame_image(float(s)).convert('RGB').resize((B.W, B.H), Image.LANCZOS).save(os.path.join(out, f't{s}.png'))
    elif mode == 'animatic':
        render(sys.argv[2], (540, 960), 26, 1)
    elif mode == 'final':
        render(sys.argv[2], (1080, 1920), 20, 2)


if __name__ == '__main__':
    main()
