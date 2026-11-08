#!/usr/bin/env python3
"""MAP  Ad-Vanced Notice (8 Nov): the sets. Flat paintings, one per camera (rule 39), in the house style (flat colour,
one ink outline, hand-cut edges), every piece at its real size in metres through that shot's camera.

    python3 source/ad_vanced_notice_sets.py sheet OUT.jpg     the four shots with the cast in place + the props sheet
    python3 source/ad_vanced_notice_sets.py reel OUT.mp4      a few seconds of each moving set (fire, sea, tanker)
    python3 source/benchmark.py ad_vanced_notice_sets OUT.jpg the place lists ticked against the photos (rule 3)

Map: helpers 45 | study 132 (study_pose 469) | strait (cliff + close-up) 511 | tanker 618 |
     strait() 871 | gas station 909 | pickup 1056 | the cast in place 1192 | BENCHMARK, PROP_SIZES 1318 | sheets 1392

Use in the film (each returns a 1080 x 1920 RGBA):
    study_back(t), study_front()            people go between (Vance at STUDY_VANCE: x, neck_y, s)
    strait('wide' | 'close', t, near=('sail' | 'wreck', x_m[, brk]), fx=fn)   fx(img, cam) draws the showstopper's effects
                                            between the sea and the cliff top; Vance goes on top (place_cliff)
    gas_back(), gas_front()                 people go between (place_gas); HOSE_FROM, FILLER, BOARD_BOX for the cast
                                            stage and KEEP_CLEAR
    tanker(pen, cam, x, y, ...), pickup(pen, x_front, ground_y, ppm)   the props, any camera / any scale
"""
import functools
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import flying_whales_sea as FS      # noqa: E402  (the sea painting re-lit: bands, rays, ground, project)
import sitting                      # noqa: E402
import views as V                   # noqa: E402
import whale as WH                  # noqa: E402  (the pinhole camera)
from ed import INK                  # noqa: E402

NAME = 'ad-vanced-notice'
W, H = 1080, 1920
SS = 2                              # drawn at twice the size, then shrunk (smooth edges)
LW = 3.0                            # the set's ink line at 1080 wide (the people keep their own)
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')


# ---------------------------------------------------------------------------------------------- helpers
def mix(a, b, k):
    return tuple(int(round(a[i] + (b[i] - a[i]) * k)) for i in range(3))


def layer():
    return Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))


def shrink(im):
    return im.resize((W, H), Image.LANCZOS)


class Pen:
    """Draws in 1080 x 1920 coordinates onto an SS-sized image: flat fills, one ink line."""
    def __init__(self, im, ss=SS):
        self.d, self.ss, self.im = ImageDraw.Draw(im, 'RGBA'), ss, im

    def _p(self, pts):
        return [(x * self.ss, y * self.ss) for x, y in pts]

    def poly(self, pts, fill, w=LW, ink=INK):
        P = self._p(pts)
        if len(P) < 3:
            return
        if fill is not None:
            self.d.polygon(P, fill=fill)
        if w:
            self.d.line(P + [P[0]], fill=ink, width=max(1, int(round(w * self.ss))), joint='curve')

    def line(self, pts, col=INK, w=LW):
        self.d.line(self._p(pts), fill=col, width=max(1, int(round(w * self.ss))), joint='curve')

    def ell(self, cx, cy, rx, ry, fill, w=LW, ink=INK):
        s = self.ss
        self.d.ellipse([(cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s], fill=fill,
                       outline=ink if w else None, width=max(1, int(round(w * s))) if w else 0)

    def text(self, xy, s, size, fill, anchor='la'):
        f = ImageFont.truetype(FONT, int(size * self.ss))
        self.d.text((xy[0] * self.ss, xy[1] * self.ss), s, font=f, fill=fill, anchor=anchor)


def cut(pts, amt, seed):
    """Hand-cut: every corner nudged a little (the same every frame)."""
    r = random.Random(seed)
    return [(x + r.uniform(-amt, amt), y + r.uniform(-amt, amt)) for x, y in pts]


def box(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def wobbly(pts, amt, seed, step=40.0):
    """Long edges broken into short runs, each point nudged: a hand-drawn edge rather than a ruled one."""
    r = random.Random(seed)
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        for i in range(n):
            u = i / n
            out.append((x0 + (x1 - x0) * u + r.uniform(-amt, amt), y0 + (y1 - y0) * u + r.uniform(-amt, amt)))
    return out


def star(cx, cy, r, squash=1.0):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.40
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * squash))
    return pts


class Level:
    """A level camera with its horizon moved off the middle (a shift lens): verticals stay vertical, as a flat painting
    wants. World: x right, d away from the lens, z up (metres)."""
    def __init__(self, h, hz, f, cx=540.0):
        self.h, self.hz, self.f, self.cx = h, hz, f, cx

    def p(self, x, d, z):
        return self.cx + self.f * x / d, self.hz - self.f * (z - self.h) / d

    def ppm(self, d):
        return self.f / d


# ---------------------------------------------------------------------------------------------- shot 1: the study
# A level camera 1.45 m up, horizon y 760, focal 1600. Vance's hips 2.6 m away; the desk measured from the sitting
# kit's desk at his size (its top 500 person units up, so his forearms land on it: rule 78); the back wall 5.0 m away
# (far enough that the fire shows over the desk: at the composition's 3.6 m the desk hid it).
STUDY = Level(1.45, 760.0, 1600.0)
V_UNIT = V.M_PER_UNIT * 1.88 / 1.75                  # Vance's person unit in metres
_DK = sitting.Desk()
D_V = 2.6                                            # his hips
DESK_Z = _DK.h * V_UNIT                              # the top, 0.82 m
D_NEAR = D_V - _DK.front * V_UNIT                    # the edge at his side
D_FAR = D_V - (_DK.front + _DK.depth) * V_UNIT       # the edge nearest us
D_HANDS = D_V - (_DK.front + 125.0) * V_UNIT         # where spec_hands_folded puts his hands
DESK_HALF = 0.9                                      # a 1.8 m pedestal desk
D_WALL = 5.0
WALL_PPM = STUDY.ppm(D_WALL)
_S_V = V_UNIT * STUDY.ppm(D_V)
STUDY_VANCE = dict(x=540.0, s=_S_V,
                   neck_y=STUDY.p(0, D_HANDS, DESK_Z)[1] - (sitting.FLOOR - _DK.h) * _S_V)

OAK, OAK_D, OAK_DD, OAK_L, OAK_HI = (128, 78, 40), (94, 56, 28), (50, 30, 16), (158, 102, 56), (196, 144, 90)
BOOKS = [(112, 62, 34), (86, 48, 26), (142, 86, 44), (122, 30, 30), (96, 24, 28), (38, 72, 48), (28, 56, 40),
         (176, 132, 80), (38, 46, 76), (70, 40, 26)]
GOLD, GOLD_D = (214, 172, 76), (150, 112, 40)
STONE, STONE_D = (204, 190, 164), (170, 154, 128)
FIREBOX, IRON = (26, 20, 18), (50, 48, 50)
LEATHER = (46, 82, 58)
CHAIR, CHAIR_D = (108, 36, 30), (70, 20, 18)


def _wall(x, z):
    return STUDY.p(x, D_WALL, z)


def _wall_box(x0, z0, x1, z1):
    (a, b), (c, d) = _wall(x0, z1), _wall(x1, z0)
    return box(a, b, c, d)


def _books(pen, x0, x1, z0, z1, seed):
    """One shelf of leather books between x0 and x1 (wall metres), standing on z0, under the shelf above at z1."""
    r = random.Random(seed)
    x = x0 + 0.01
    while x < x1 - 0.03:
        kind = r.random()
        if kind < 0.07 and x < x1 - 0.3:                  # a short stack lying flat
            hgt = 0.0
            for k in range(r.randint(2, 4)):
                th = r.uniform(0.035, 0.06)
                wd = r.uniform(0.18, 0.26)
                pen.poly(cut(_wall_box(x, z0 + hgt, x + wd, z0 + hgt + th), 1.0, seed + k), r.choice(BOOKS), 2)
                hgt += th
            x += 0.28
            continue
        bw = r.uniform(0.025, 0.065)
        bh = min(z1 - z0 - 0.02, r.uniform(0.2, 0.31))
        col = r.choice(BOOKS)
        if kind > 0.97:                                   # a gap: one leaning book
            x += 0.05
            (ax, ay), (bx, by) = _wall(x, z0), _wall(x + bw, z0)
            lean = bh * WALL_PPM * 0.35
            pen.poly([(ax, ay), (bx, by), (bx + lean, by - bh * WALL_PPM * 0.94), (ax + lean, ay - bh * WALL_PPM * 0.94)],
                     col, 2)
            x += bw + 0.06
            continue
        pts = cut(_wall_box(x, z0, x + bw, z0 + bh), 1.2, int(x * 1000) + seed)
        pen.poly(pts, col, 2)
        (sx0, _), (sx1, _) = _wall(x, 0), _wall(x + bw, 0)
        for zz in (z0 + 0.03, z0 + bh - 0.035):          # gold bands on the spine
            yy = _wall(0, zz)[1]
            pen.line([(sx0 + 2, yy), (sx1 - 2, yy)], GOLD, 2.2)
        if r.random() < 0.45:                             # a title label
            ya, yb = _wall(0, z0 + bh * 0.72)[1], _wall(0, z0 + bh * 0.6)[1]
            pen.poly(box(sx0 + 3, ya, sx1 - 3, yb), mix(col, (20, 12, 8), 0.4), 0)
        x += bw + r.uniform(0.0, 0.006)


def _bookcases(pen):
    ups = [-1.8, -0.98, -0.16, 0.26]                      # flat oak uprights; the chimney breast from 0.3
    shelves = [0.8 + 0.36 * k for k in range(8)]          # 0.8 .. 3.32
    for a, b in zip(ups, ups[1:]):
        pen.poly(_wall_box(a, 0.0, b, 3.32), OAK_DD, 0)
        for k, (z0, z1) in enumerate(zip(shelves, shelves[1:])):
            _books(pen, a + 0.04, b - 0.04, z0 + 0.03, z1, int(a * 100) + 31 * k)
            pen.poly(cut(_wall_box(a, z0, b, z0 + 0.035), 0.8, k), OAK_L, 2)
        pen.poly(cut(_wall_box(a, 0.0, b, 0.8), 1.0, 7), OAK, 2)              # the cupboard plinth
        for dx in (0.0, (b - a) / 2):
            pen.poly(cut(_wall_box(a + dx + 0.07, 0.1, a + dx + (b - a) / 2 - 0.03, 0.72), 1.0, 9), OAK_D, 2)
    for k, a in enumerate(ups):
        pen.poly(cut(_wall_box(a - 0.04, 0.0, a + 0.04, 3.32), 1.0, 40 + k), OAK, LW)
        (x0, y0), (x1, y1) = _wall(a - 0.015, 3.2), _wall(a, 1.0)                # lacquer shine
        pen.poly([(x0, y0), (x0 + 4, y0), (x1 + 2, y1), (x1 - 1, y1)], OAK_HI, 0)


def _cornice(pen):
    steps = [(3.32, 3.38, OAK_L), (3.38, 3.47, OAK), (3.47, 3.52, OAK_HI), (3.52, 3.6, OAK_D)]
    for z0, z1, c in steps:
        pen.poly(wobbly(_wall_box(-1.9, z0, 1.9, z1), 0.8, int(z0 * 100), 90), c, 2)
    a, b = _wall(-1.9, 3.6)
    pen.poly(box(-10, -10, W + 10, b), (228, 214, 188), LW)                    # the plaster ceiling


def _fireplace(pen):
    pen.poly(cut(_wall_box(0.3, 0.0, 1.95, 3.32), 1.0, 51), OAK, LW)             # the chimney breast
    for x0, x1 in ((0.38, 0.62), (1.48, 1.86)):                                  # raised panels beside the portrait
        pen.poly(cut(_wall_box(x0, 1.52, x1, 3.2), 1.0, int(x0 * 50)), OAK_D, 2)
        pen.poly(cut(_wall_box(x0 + 0.04, 1.56, x1 - 0.04, 3.16), 1.0, int(x0 * 70)), OAK, 2)
    pen.poly(cut(_wall_box(0.4, 0.0, 1.7, 1.3), 1.2, 52), STONE, LW)            # the stone surround
    pen.poly(cut(_wall_box(0.5, 0.0, 0.6, 1.2), 1.0, 53), STONE_D, 2)
    pen.poly(cut(_wall_box(1.5, 0.0, 1.6, 1.2), 1.0, 54), STONE_D, 2)
    pen.poly(cut(_wall_box(0.32, 1.3, 1.78, 1.39), 1.0, 55), OAK_L, LW)         # the mantel shelf
    pen.poly(cut(_wall_box(0.36, 1.24, 1.74, 1.3), 1.0, 56), STONE_D, 2)
    # the firebox: a black opening with a shallow arched head, an iron fireback
    xs = np.linspace(0.68, 1.42, 15)
    arch = [_wall(x, 0.72 + 0.06 * math.sin(math.pi * (x - 0.68) / 0.74)) for x in xs]
    pen.poly([_wall(0.68, 0.0)] + arch + [_wall(1.42, 0.0)], FIREBOX, LW)
    pen.poly(cut(_wall_box(0.84, 0.12, 1.26, 0.6), 1.0, 57), (40, 34, 32), 2)
    # mantel dressing: a bracket clock and two brass candlesticks
    cx, top = 1.05, 1.39
    pen.poly(cut(_wall_box(cx - 0.12, top, cx + 0.12, top + 0.24), 1.0, 58), (74, 42, 24), LW)
    xs = np.linspace(cx - 0.12, cx + 0.12, 9)
    pen.poly([_wall(x, top + 0.24 + 0.07 * math.sin(math.pi * (x - cx + 0.12) / 0.24)) for x in xs], (74, 42, 24), LW)
    (dx, dy) = _wall(cx, top + 0.13)
    r = 0.07 * WALL_PPM
    pen.ell(dx, dy, r, r, (240, 234, 216), 2)
    pen.line([(dx, dy), (dx, dy - r * 0.7)], INK, 2)
    pen.line([(dx, dy), (dx + r * 0.5, dy + r * 0.2)], INK, 2)
    for x in (0.55, 1.55):
        pen.poly(cut(_wall_box(x - 0.045, top, x + 0.045, top + 0.025), 0.5, 59), (196, 160, 70), 2)
        pen.poly(_wall_box(x - 0.014, top + 0.025, x + 0.014, top + 0.22), (196, 160, 70), 2)
        pen.poly(_wall_box(x - 0.03, top + 0.2, x + 0.03, top + 0.23), (196, 160, 70), 2)
        pen.poly(_wall_box(x - 0.012, top + 0.23, x + 0.012, top + 0.38), (244, 240, 226), 2)
    # a portrait in a gilt frame over it (an anonymous gentleman: nobody real), its foot clear above the clock's top
    # (1.70 m: Sam, 8 Nov, it clipped into the clock), painted in some detail (Sam: "add some detail")
    f0, f1 = 1.80, 2.86
    pen.poly(cut(_wall_box(0.72, f0, 1.38, f1), 1.2, 60), GOLD, LW)
    pen.poly(cut(_wall_box(0.77, f0 + 0.05, 1.33, f1 - 0.05), 1.0, 61), GOLD_D, 2)
    pen.poly(cut(_wall_box(0.8, f0 + 0.08, 1.30, f1 - 0.08), 1.0, 62), (58, 46, 36), 2)
    k = WALL_PPM
    pen.poly([_wall(0.8, f0 + 0.08), _wall(0.8, f1 - 0.08), _wall(0.98, f1 - 0.08), _wall(0.86, f0 + 0.5),
              _wall(0.9, f0 + 0.08)], (120, 34, 34), 2)                                  # a red drape behind him
    for gx, gy in ((0.84, f1 - 0.12), (1.26, f1 - 0.12), (0.84, f0 + 0.12), (1.26, f0 + 0.12)):   # the frame's corners
        cx_, cy_ = _wall(gx, gy)
        pen.ell(cx_, cy_, 0.018 * k, 0.018 * k, (232, 196, 96), 1.2)
    sx, sy = _wall(1.05, f0 + 0.08)
    P = lambda x, y: (sx + x * k, sy - y * k)
    pen.poly([P(-0.22, 0), P(-0.19, 0.32), P(-0.08, 0.42), P(0.08, 0.42), P(0.19, 0.32), P(0.22, 0)], (40, 32, 44), 2)  # coat
    pen.poly([P(-0.08, 0.42), P(-0.03, 0.42), P(-0.06, 0.0), P(-0.12, 0.0)], (60, 50, 66), 1.4)        # its lapels
    pen.poly([P(0.08, 0.42), P(0.03, 0.42), P(0.06, 0.0), P(0.12, 0.0)], (60, 50, 66), 1.4)
    for by in (0.08, 0.16, 0.24):                                                         # gilt buttons
        bx_, by_ = P(-0.075, by)
        pen.ell(bx_, by_, 0.012 * k, 0.012 * k, (220, 180, 80), 1.0)
    pen.poly([P(-0.06, 0.43), P(0.06, 0.43), P(0.04, 0.3), P(0.0, 0.26), P(-0.04, 0.3)], (240, 236, 222), 1.6)  # cravat
    for side in (-1, 1):                                                                   # the wig's side curls
        for j in range(3):
            cx_, cy_ = P(side * 0.105, 0.5 - j * 0.045)
            pen.ell(cx_, cy_, 0.035 * k, 0.026 * k, (228, 222, 210), 1.4)
    hx_, hy_ = P(0, 0.58)
    pen.ell(hx_, hy_ - 0.04 * k, 0.095 * k, 0.07 * k, (232, 226, 214), 1.8)                   # the wig's crown
    pen.ell(hx_, hy_, 0.065 * k, 0.088 * k, (222, 182, 150), 1.8)                            # the face
    for ex in (-0.025, 0.025):
        e = P(ex, 0.6)
        pen.ell(e[0], e[1], 0.008 * k, 0.006 * k, (40, 34, 30), 0)                             # eyes
        pen.line([P(ex - 0.016, 0.618), P(ex + 0.016, 0.62)], (110, 90, 80), 1.4)               # brows
    pen.line([P(0.0, 0.595), P(0.006, 0.56), P(-0.004, 0.555)], (150, 100, 80), 1.4)            # nose
    pen.line([P(-0.018, 0.535), P(0.0, 0.53), P(0.018, 0.535)], (150, 70, 70), 1.6)             # a thin, stern mouth
    c1, c2 = P(-0.035, 0.555), P(0.035, 0.555)
    pen.ell(c1[0], c1[1], 0.012 * k, 0.008 * k, (226, 160, 140), 0)                           # rosy cheeks
    pen.ell(c2[0], c2[1], 0.012 * k, 0.008 * k, (226, 160, 140), 0)


# Rule 83: every painted object on the fireplace wall, its box in wall metres (x along the wall, z up), and the
# overlaps that are meant (setcheck.py; the film's checks() runs it)
SET_BOXES = [('chimney breast', (0.3, 0.0, 1.95, 3.32)), ('stone surround', (0.4, 0.0, 1.7, 1.3)),
             ('mantel shelf', (0.32, 1.24, 1.78, 1.39)), ('clock', (0.93, 1.39, 1.17, 1.70)),
             ('candlestick L', (0.505, 1.39, 0.595, 1.77)), ('candlestick R', (1.505, 1.39, 1.595, 1.77)),
             ('portrait', (0.72, 1.80, 1.38, 2.86)), ('panel L', (0.38, 1.52, 0.62, 3.2)),
             ('panel R', (1.48, 1.52, 1.86, 3.2))]
SET_MEANT = [('chimney breast', b, 'it stands on the chimney breast') for b in
             ('stone surround', 'mantel shelf', 'clock', 'candlestick L', 'candlestick R', 'portrait', 'panel L', 'panel R')]
SET_MEANT += [('stone surround', 'mantel shelf', 'the shelf sits on the surround'),
              ('panel L', 'candlestick L', 'the candlestick stands in front of the panel'),
              ('panel R', 'candlestick R', 'the candlestick stands in front of the panel')]


def _chair(pen):
    """His high-backed oxblood leather chair, buttoned, behind him (the film draws him over it, no kit chair)."""
    v = STUDY_VANCE
    s, x, ny = v['s'], v['x'], v['neck_y']
    top, bot = ny + 30 * s, ny + 470 * s
    hw = 235 * s
    pts = [(x - hw, bot), (x - hw - 8 * s, top + 60 * s), (x - hw + 30 * s, top), (x - 60 * s, top - 22 * s),
           (x + 60 * s, top - 22 * s), (x + hw - 30 * s, top), (x + hw + 8 * s, top + 60 * s), (x + hw, bot)]
    pen.poly(cut(pts, 3, 70), CHAIR, LW)
    pen.poly(cut([(x - hw + 26 * s, bot), (x - hw + 20 * s, top + 40 * s), (x + hw - 20 * s, top + 40 * s),
                  (x + hw - 26 * s, bot)], 2, 71), mix(CHAIR, (150, 60, 50), 0.25), 2)
    for row in range(5):
        for c in range(-3, 4):
            if (row + c) % 2:
                continue
            pen.ell(x + c * 58 * s, top + 70 * s + row * 70 * s, 5 * s, 5 * s, CHAIR_D, 0)


@functools.lru_cache(maxsize=1)
def _study_still():
    im = layer()
    pen = Pen(im)
    pen.poly(box(-10, -10, W + 10, H + 10), OAK, 0)
    _bookcases(pen)
    _fireplace(pen)
    _cornice(pen)
    return shrink(im)


@functools.lru_cache(maxsize=1)
def _chair_layer():
    im = layer()
    _chair(Pen(im))
    return shrink(im)


FIRE_LOOP = 2.0                                      # the fire repeats every 2 s


def _fire(pen, t):
    """Logs on an iron grate and a low fire: tongues in three colours that flicker on a 2 s loop."""
    w = 2 * math.pi / FIRE_LOOP
    base_z = 0.24
    # the glow on the stone jambs and the hearth: two flat warm steps that breathe with the fire
    g = 0.5 + 0.5 * math.sin(w * 2 * t)
    for x0, x1 in ((0.6, 0.68), (1.42, 1.5)):
        pen.poly(_wall_box(x0, 0.0, x1, 0.55 + 0.05 * g), (222, 184, 140), 0)
    for k, (dx, hh, ph, fr) in enumerate(((-0.24, 0.26, 0.0, 3), (-0.12, 0.36, 1.3, 2), (0.0, 0.42, 2.1, 4),
                                           (0.13, 0.33, 3.7, 3), (0.24, 0.24, 5.0, 2))):
        x = 1.05 + dx
        hgt = hh * (0.78 + 0.22 * math.sin(fr * w / 2 * t + ph))
        sway = 0.03 * math.sin(fr * w / 2 * t * 1.0 + ph * 2)
        for sc, col, lw in ((1.0, (236, 104, 34), 2.5), (0.66, (250, 164, 50), 0), (0.34, (255, 228, 124), 0)):
            half = 0.075 * sc + 0.02
            pts = [_wall(x - half, base_z), _wall(x - half * 0.5 + sway * 0.4, base_z + hgt * sc * 0.55),
                   _wall(x + sway, base_z + hgt * sc), _wall(x + half * 0.55 + sway * 0.5, base_z + hgt * sc * 0.5),
                   _wall(x + half, base_z)]
            pen.poly(pts, col, lw)
    # logs and the grate in front of the flames
    for x0, x1, z0, z1 in ((0.76, 1.24, 0.16, 0.25), (0.88, 1.36, 0.2, 0.29)):
        pen.poly(cut(_wall_box(x0, z0, x1, z1), 1.5, int(x0 * 100)), (94, 58, 34), 2.5)
        ex, ey = _wall(x1, (z0 + z1) / 2)
        r = (z1 - z0) / 2 * WALL_PPM
        pen.ell(ex, ey, r * 0.6, r, (200, 164, 112), 2)
    for x in np.linspace(0.78, 1.32, 7):
        pen.poly(_wall_box(x - 0.009, 0.08, x + 0.009, 0.26), IRON, 1.5)
    pen.poly(_wall_box(0.74, 0.08, 1.36, 0.11), IRON, 2)
    # sparks: three that rise and go out on the loop
    for k in range(3):
        u = ((t / FIRE_LOOP) + k / 3) % 1.0
        sx, sy = _wall(1.0 + 0.1 * math.sin(k * 2.1 + u * 4), 0.4 + u * 0.35)
        if u < 0.7:
            pen.ell(sx, sy, 2.5, 2.5, (255, 214, 120), 0)


def study_back(t, chair=True):
    """The study behind Vance at time t: the still painting plus the moving fire; chair=False leaves the painted
    armchair out (the film seats him in the kit's swivel chair, note 27)."""
    im = _study_still().copy()
    x0, y0 = _wall(0.55, 0.85)
    x1, y1 = _wall(1.55, 0.0)
    crop = (int(x0), int(y0), int(x1) + 1, min(H, int(y1) + 1))
    fl = Image.new('RGBA', ((crop[2] - crop[0]) * SS, (crop[3] - crop[1]) * SS), (0, 0, 0, 0))
    pen = Pen(fl)
    pen.d = ImageDraw.Draw(fl)
    off = (-crop[0], -crop[1])
    pen._p = lambda pts: [((x + off[0]) * SS, (y + off[1]) * SS) for x, y in pts]
    _fire(pen, t)
    im.alpha_composite(fl.resize((crop[2] - crop[0], crop[3] - crop[1]), Image.LANCZOS), (crop[0], crop[1]))
    if chair:
        im.alpha_composite(_chair_layer())            # the chair in front of the fire (Sam, 8 Nov: the glow cut it)
    return im


def _desk_pt(x, d, z):
    return STUDY.p(x, d, z)


def _flag(pen):
    """A 2 x 3 ft US flag draped over the desk's left side: its top edge lying 7 cm back on the desk top, the rest
    hanging down the front with soft folds; 13 stripes, the union of 50 stars at the top left."""
    hoist, fly = 0.61, 0.915
    stripe = hoist / 13
    on_top = 0.07
    x_hoist, x_end = -0.62, -0.05                    # the hoist at the left; the fly end folded back at x_end
    uw, uh = 0.4 * fly, 7 * stripe
    RED, WHITE, BLUE = (186, 32, 44), (246, 244, 238), (34, 44, 104)
    ppm = STUDY.ppm(D_FAR)
    yF = _desk_pt(0, D_FAR, DESK_Z)[1]

    def front(x, v):                                 # v metres down the flag from its top edge (v >= on_top)
        down = v - on_top
        fold = 0.012 * math.sin((x - x_hoist) / 0.09 * math.pi) * min(1.0, down / 0.3)
        return _desk_pt(x, D_FAR - fold, DESK_Z - down)

    def top(x, v):                                   # v <= on_top: lying on the desk top
        return _desk_pt(x, D_FAR + (on_top - v), DESK_Z)

    xs = np.linspace(x_hoist, x_end, 28)
    hem = [hoist - 0.012 - 0.025 * (1 + math.sin(i * 0.9)) * (0.5 + 0.5 * math.cos(i * 0.31)) for i in range(len(xs))]
    # the hanging part, stripe by stripe
    for k in range(13):
        v0, v1 = max(on_top, k * stripe), (k + 1) * stripe
        if v1 <= on_top:
            continue
        upper = [front(x, v0) for x in xs]
        lower = [front(x, min(v1, hem[i])) for i, x in enumerate(xs)]
        pen.poly(upper + lower[::-1], RED if k % 2 == 0 else WHITE, 0)
    # the part on the desk top
    for k in range(2):
        v0, v1 = k * stripe, min(on_top, (k + 1) * stripe)
        pen.poly([top(x, v0) for x in xs] + [top(x, v1) for x in xs[::-1]], RED if k % 2 == 0 else WHITE, 0)
    # the union, on top and hanging
    ux = [x for x in xs if x <= x_hoist + uw + 1e-6] + [x_hoist + uw]
    pen.poly([top(x, 0) for x in ux] + [top(x, on_top) for x in ux[::-1]], BLUE, 0)
    pen.poly([front(x, on_top) for x in ux] + [front(x, uh) for x in ux[::-1]], BLUE, 0)
    hs, vs = uw / 12, uh / 10
    for r in range(1, 10):
        for c in (range(1, 12, 2) if r % 2 else range(2, 11, 2)):
            x, v = x_hoist + c * hs, r * vs
            if v < on_top:
                sx, sy = top(x, v)
                pen.poly(star(sx, sy, 0.019 * ppm, 0.33), WHITE, 0)
            else:
                sx, sy = front(x, v)
                pen.poly(star(sx, sy, 0.019 * ppm), WHITE, 0)
    # fold shadows: flat darker wedges in the valleys, widening to the hem
    shade = Image.new('RGBA', pen.im.size, (0, 0, 0, 0))   # (Sam, 8 Nov: drawn straight onto the flag, the see-
    sp = Pen(shade, pen.ss)                                  # through shadows cut holes in it: the desk showed
    for x in (-0.52, -0.34, -0.17):                          # through. Now laid OVER the cloth, one whole flag)
        a, b = front(x, 0.2), front(x, hoist - 0.03)
        sp.poly([(a[0] - 3, a[1]), (a[0] + 3, a[1]), (b[0] + 26, b[1]), (b[0] - 26, b[1])], (40, 0, 20, 255), 0)
    sh = np.asarray(shade).copy()
    sh[..., 3] = (sh[..., 3].astype(np.uint16) * 40 // 255).astype(np.uint8)
    pen.im.alpha_composite(Image.fromarray(sh, 'RGBA'))
    # one outline round the whole drape
    outline = [top(x, 0) for x in xs] + [front(x_end, on_top)] + \
              [front(x, hem[i]) for i, x in list(enumerate(xs))[::-1]] + [front(x_hoist, on_top)]
    pen.poly(outline, None, LW)
    pen.line([front(x, on_top) for x in xs], INK, 2)             # the fold over the desk edge
    return yF


def _glass(pen):
    """A cut-crystal tumbler of water on his left (our right), on the leather, 8.5 cm across, 10 cm tall."""
    x, d = 0.42, 2.05
    ppm = STUDY.ppm(d)
    bx, by = _desk_pt(x, d, DESK_Z)
    w0, w1, hgt = 0.075 * ppm / 2, 0.085 * ppm / 2, 0.1 * ppm
    body = [(bx - w0, by), (bx - w1, by - hgt), (bx + w1, by - hgt), (bx + w0, by)]
    pen.poly(body, (214, 232, 238, 200), 0)
    wl = by - hgt * 0.68
    pen.poly([(bx - w0 - (w1 - w0) * 0.68, wl), (bx + w0 + (w1 - w0) * 0.68, wl), (bx + w0, by), (bx - w0, by)],
             (176, 214, 228, 220), 0)
    for k in range(-3, 4):                                       # the cut facets
        fx0 = bx + k * w0 / 3.6
        pen.line([(fx0, by - 6), (fx0 * 0.92 + bx * 0.08 + k * 1.5, by - hgt * 0.55)], (150, 190, 206), 1.6)
    pen.poly(box(bx - w0, by - hgt * 0.14, bx + w0, by), (196, 222, 232, 230), 0)   # the thick base
    pen.line([(bx - w1 * 0.55, by - hgt * 0.92), (bx - w0 * 0.6, by - hgt * 0.2)], (255, 255, 255), 2.5)
    pen.ell(bx, by - hgt, w1, w1 * 0.18, (226, 240, 244), 2)
    pen.poly(body, None, LW)


@functools.lru_cache(maxsize=1)
def study_desktop():
    """The desk's top (oak, green leather, gold tooling): drawn over his body but under his forearms (study_pose)."""
    im = layer()
    pen = Pen(im)
    a, b = _desk_pt(-DESK_HALF, D_NEAR, DESK_Z), _desk_pt(DESK_HALF, D_NEAR, DESK_Z)
    c, d = _desk_pt(DESK_HALF, D_FAR, DESK_Z), _desk_pt(-DESK_HALF, D_FAR, DESK_Z)
    pen.poly([a, b, c, d], OAK_L, LW)                                            # the top
    ins = [_desk_pt(-DESK_HALF + 0.08, D_NEAR + 0.0, DESK_Z), _desk_pt(DESK_HALF - 0.08, D_NEAR, DESK_Z),
           _desk_pt(DESK_HALF - 0.08, D_FAR + 0.07, DESK_Z), _desk_pt(-DESK_HALF + 0.08, D_FAR + 0.07, DESK_Z)]
    pen.poly(ins, LEATHER, 2)                                                    # the leather inset
    ins2 = [_desk_pt(-DESK_HALF + 0.1, D_NEAR + 0.0, DESK_Z), _desk_pt(DESK_HALF - 0.1, D_NEAR, DESK_Z),
            _desk_pt(DESK_HALF - 0.1, D_FAR + 0.09, DESK_Z), _desk_pt(-DESK_HALF + 0.1, D_FAR + 0.09, DESK_Z)]
    pen.poly(ins2, None, 1.6, GOLD)                                              # its tooled gold line
    return shrink(im)


def study_pose(j):
    """Seat Vance at the painted desk: no kit chair or kit desk (the set paints its own), the desk top laid between
    his body and his arms, so his forearms rest on it (rule 78)."""
    j['chair_draw'] = lambda *a, **k: None
    j['pre'] = []
    j['mid'] = [lambda p, j2, view: p.img.alpha_composite(study_desktop())]
    return j


@functools.lru_cache(maxsize=1)
def study_front():
    """The desk's front, the flag and the glass: everything in front of Vance in the study (still)."""
    im = layer()
    pen = Pen(im)
    pf = STUDY.ppm(D_FAR)
    yF = _desk_pt(0, D_FAR, DESK_Z)[1]
    fy = lambda z: STUDY.p(0, D_FAR, z)[1]
    fx = lambda x: STUDY.p(x, D_FAR, 0)[0]
    pen.poly(cut(box(fx(-DESK_HALF), yF, fx(DESK_HALF), H + 20), 2, 80), OAK, LW)   # the front face
    pen.poly(cut(box(fx(-DESK_HALF), yF, fx(DESK_HALF), fy(DESK_Z - 0.045)), 1.5, 81), OAK_L, LW)  # the top's edge
    pen.poly([(fx(-0.6), yF + 6), (fx(0.5), yF + 6), (fx(0.48), yF + 10), (fx(-0.62), yF + 10)], OAK_HI, 0)
    for x0, x1 in ((-0.88, -0.44), (-0.4, 0.4), (0.44, 0.88)):                  # the frieze drawers
        pen.poly(cut(box(fx(x0), fy(0.76), fx(x1), fy(0.655)), 1.5, int(x0 * 90)), OAK_D, 2)
        pen.poly(cut(box(fx(x0) + 6, fy(0.75), fx(x1) - 6, fy(0.665)), 1.5, int(x1 * 90)), OAK, 2)
    pen.poly(cut(box(fx(-0.4), fy(0.64), fx(0.4), H + 20), 1.5, 84), OAK_D, LW)  # the kneehole's back panel
    for x0, x1 in ((-0.88, -0.44), (0.44, 0.88)):                               # pedestal drawers
        for z0, z1 in ((0.64, 0.44), (0.42, 0.22)):
            pen.poly(cut(box(fx(x0), fy(z0), fx(x1), fy(z1)), 1.5, int(z0 * 100 + x0 * 10)), OAK, 2)
            pen.poly([(fx(x0) + 10, fy(z0) + 8), (fx(x0) + 16, fy(z0) + 8), (fx(x0) + 40, fy(z1) - 10),
                      (fx(x0) + 34, fy(z1) - 10)], OAK_HI, 0)
    for x0, x1, z in ((-0.88, -0.44, 0.708), (-0.4, 0.4, 0.708), (0.44, 0.88, 0.708), (-0.88, -0.44, 0.54),
                      (0.44, 0.88, 0.54), (-0.88, -0.44, 0.32), (0.44, 0.88, 0.32)):   # brass swan-neck handles
        cx, cy = fx((x0 + x1) / 2), fy(z)
        r = 0.04 * pf
        pen.line([(cx - r, cy), (cx - r * 0.7, cy + r * 0.45), (cx + r * 0.7, cy + r * 0.45), (cx + r, cy)], GOLD, 4)
        pen.ell(cx - r, cy, 4, 4, GOLD, 1.5)
        pen.ell(cx + r, cy, 4, 4, GOLD, 1.5)
    _flag(pen)
    _glass(pen)
    return shrink(im)


# ---------------------------------------------------------------------------------------------- shot 2: the strait
# The world: x right, y out to sea, z up (metres), the sea at z 0; the cliff-top plateau at z 60, its edge about 12 m
# out. The wide camera stands on the plateau 1.6 m up (61.6 m above the sea), horizon y 763, focal 1890 (35% closer
# than the composition, Sam 8 Nov); no headland or tree, only sea and the far shore behind (the eye goes to the ships). The close-up camera stands 1.1 m in front of Vance's mark, at his eye height, turned 4 degrees left so
# the burning wreck sits over his left shoulder (screen right, Sam 7 Nov), horizon y 1010.
PLATEAU = 60.0
CLIFF_F = 1890.0                                    # Sam, 8 Nov: 35% closer than the composition's 1400
CLIFF = WH.Cam(pos=(0.0, 0.0, PLATEAU + 1.6), yaw=0.0, pitch=-math.degrees(math.atan(197.0 / CLIFF_F)),
               focal=CLIFF_F, size=(W, H))            # the horizon stays at y 763
VANCE_MARK = (-0.30, 3.0)                           # where he stops: screen x 360, 35% bigger than in the composition
NEAR_Y, NEAR_L, NEAR_V = 1200.0, 330.0, 6.0        # the moving tanker: 1.2 km out, 330 m long, 6 m/s (12 knots)

HAZE = (226, 230, 228)
SKY_DAY = [(0.5, (226, 230, 228)), (1.4, (214, 224, 230)), (3.2, (200, 216, 230)), (6.5, (186, 208, 230)),
           (11.0, (172, 200, 228)), (17.0, (160, 192, 226)), (25.0, (148, 184, 222)), (36.0, (138, 176, 218)),
           (90.0, (128, 168, 214))]
SEA_DAY = [(190, 206, 208), (152, 186, 194), (116, 166, 178), (84, 146, 162), (62, 128, 146), (48, 112, 132),
           (40, 100, 122), (34, 90, 112), (30, 82, 104)]
ROCK, ROCK_D, ROCK_SH = (172, 148, 118), (128, 106, 84), (150, 128, 98)
SAND, SAND_L, SAND_D = (212, 194, 158), (226, 212, 178), (194, 174, 138)


def near_x(t, t_hit):
    """The moving tanker's middle (world x) at time t, when the missile lands at t_hit."""
    return X_HIT - NEAR_V * (t_hit - t)


def proj(cam, P):
    """Screen (x, y) and depth of world points (N x 3)."""
    s, d = cam.screen(np.asarray(P, float))
    return s, d


def _x_at(cam, sx, y):
    """The world x on the sea at distance y that the camera sees at screen x."""
    a, b = -2000.0, 2000.0
    for _ in range(50):
        m = (a + b) / 2
        if proj(cam, [(m, y, 0.0)])[0][0][0] < sx:
            a = m
        else:
            b = m
    return (a + b) / 2


X_HIT = _x_at(CLIFF, 790.0, NEAR_Y)                 # its middle when the missile lands: screen x 790, y 861
_CU_POS = (VANCE_MARK[0], VANCE_MARK[1] - 1.1, PLATEAU + 1.75)
CLOSE = WH.Cam(pos=_CU_POS, yaw=math.degrees(math.atan2(X_HIT - _CU_POS[0], NEAR_Y - _CU_POS[1]) - math.atan(300 / 1500.0))
               * -1.0, pitch=-1.91, focal=1500.0, size=(W, H))
CAMS = {'wide': CLIFF, 'close': CLOSE}



def sdir(cam, az_deg, el_deg):
    """Screen point of a far direction (azimuth right of +y, elevation up), for the shore and the clouds."""
    a, e = math.radians(az_deg), math.radians(el_deg)
    v = np.array([math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)])
    s, _ = proj(cam, cam.pos + v * 1e6)
    return float(s[0]), float(s[1])


def _haze_k(dist):
    return 1.0 - math.exp(-dist / 5200.0)


def _bands(cam):
    """Sky and sea in flat bands with hand-cut edges: the Flying Whales painting re-lit for hazy daylight (no sunset
    dome, the sun high and out of frame)."""
    saved = {k: getattr(FS, k) for k in ('SKY', 'SEA', 'DOME', 'SUN_AZ')}
    FS.SKY, FS.SEA, FS.DOME, FS.SUN_AZ = SKY_DAY, SEA_DAY, 0.0, 2.6
    try:
        elev, az = FS._rays(cam, 2)
        sky = FS._bands(elev, az, False)
        sea = FS._bands(elev, az, True)
    finally:
        for k, v in saved.items():
            setattr(FS, k, v)
    arr = np.where((elev >= 0)[..., None], sky, sea)
    return Image.fromarray(arr, 'RGB').convert('RGBA').resize((W, H), Image.LANCZOS)


def _wisps(pen, cam):
    """A few thin high wisps: long low lumpy streaks, pale, with a pale outline (haze softens the ink up there)."""
    for az, el, ln, th, sd in ((-13, 13.0, 340, 16, 1), (8, 19.0, 460, 18, 2), (16, 8.0, 240, 12, 3)):
        x, y = sdir(cam, az, el)
        r = random.Random(sd)
        n = 9
        top = []
        for i in range(n + 1):
            u = i / n
            bump = math.sin(math.pi * u) ** 0.7 * th * r.uniform(0.6, 1.2)
            top.append((x - ln / 2 + ln * u, y - bump + ln * 0.03 * (u - 0.5)))
        bot = [(px, y + th * 0.25 + ln * 0.03 * ((px - x + ln / 2) / ln - 0.5)) for px, _ in top[::-1]]
        pen.poly(top + bot, (238, 242, 246), 1.6, (170, 184, 198))


def _shore(pen, cam):
    """The Iranian shore 40-55 km off: two flat grey hill bands just over the horizon, the farther paler."""
    for col, ink, top, seed in (((206, 210, 216), (186, 190, 198), 1.15, 5), ((186, 192, 200), (170, 176, 186), 0.6, 6)):
        r = random.Random(seed)
        pts = []
        for az in np.linspace(-40, 40, 33):
            pts.append(sdir(cam, az, max(0.06, top * (0.45 + 0.55 * abs(math.sin(az * 0.09 + seed))) * r.uniform(0.7, 1.0))))
        pts += [sdir(cam, 40, 0.0), sdir(cam, -40, 0.0)]
        pen.poly(pts, col, 1.6, ink)


# ---------------------------------------------------------------------------------------------- the tanker
TANKER_COLS = [  # hull, band (above the waterline), funnel, funnel band
    ((44, 48, 54), (150, 40, 34), (232, 228, 220), (30, 70, 140)),
    ((70, 40, 36), (150, 40, 34), (40, 40, 44), (220, 170, 40)),
    ((40, 56, 72), (160, 44, 38), (210, 90, 40), (240, 240, 236)),
    ((92, 32, 30), (60, 30, 26), (232, 228, 220), (180, 30, 30)),
    ((56, 64, 60), (150, 40, 34), (30, 90, 70), (236, 236, 230)),
]


WRECK_FULL = (6.5, 44.0, 0.8)      # the broken tanker settled: each half tilted 6.5 degrees (torn ends down), 44 m apart, 0.8 m lower


def clip_up(pts, f):
    """The polygon (or 2-point line) pts cut to where f(p) >= 0 (Sutherland-Hodgman)."""
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        fa, fb_ = f(a), f(b)
        if fa >= 0:
            out.append(a)
        if (fa >= 0) != (fb_ >= 0):
            k = fa / (fa - fb_)
            out.append(tuple(a[j] + (b[j] - a[j]) * k for j in range(len(a))))
    return out


def wreck_xform(u, z, L, brk=WRECK_FULL):
    """Where a point of the broken tanker (u along the hull from its middle, z up, before the break) ends up: each
    half turns about its own middle so the torn ends dip and the bow and stern lift (a broken back), drifts apart and
    settles a little."""
    ang, gap, sink = brk
    s = -1.0 if u < 0 else 1.0
    a = math.radians(s * ang)
    pu = s * L / 4
    du, dz = u - pu, z
    return (pu + du * math.cos(a) - dz * math.sin(a) + s * gap / 2,
            du * math.sin(a) + dz * math.cos(a) - sink)


def _torn(s, fb, seed):
    """A torn end (s = -1 the stern half's, +1 the bow half's): ragged from the deck down to the keel, with a strip of
    deck plating peeled up and back at the top."""
    r = random.Random(seed)
    u0 = s * 4.0
    pts = [(u0 + s * 9, fb + 0.2), (u0 + s * 4.5, fb + 5.5 + r.uniform(0, 1.5)), (u0 + s * 2.5, fb + 1.2)]
    for i, z in enumerate(np.linspace(fb, -16, 8)):
        pts.append((u0 + s * r.uniform(-2.5, 3.5) * (1 if i % 2 else -0.6), float(z)))
    return pts


def tanker(pen, cam, x, y, L=330.0, cols=TANKER_COLS[0], state='whole', bow=1, haze=None, brk=None):
    """A crude carrier side on at sea (its middle at world x, y), bow to the right (bow=1) or left (-1): long and low
    (9 m freeboard laden), a red band at the waterline, the white bridge block aft with its funnel, a pipe run and
    catwalk down the deck, cranes amidships, a raised bow and mast. 'wreck': stopped, blackened and torn in two
    amidships (Sam, 8 Nov): the halves part, their torn ends dip and the bow and stern lift (brk = (tilt degrees,
    gap m, sink m), WRECK_FULL settled), the red bottom showing; everything cut at the sea. Far ones fade into the haze."""
    hull, band, fun, fband = cols
    _, dep = proj(cam, [(x, y, 0.0)])
    dist = float(dep[0])
    k = _haze_k(dist) if haze is None else haze
    hz = lambda c: mix(c, HAZE, k)
    ink = mix(INK, HAZE, k)
    lw = max(1.0, min(2.2, 2.2 * 1200 / dist))
    wreck = state == 'wreck'
    brk = brk or WRECK_FULL
    fb = 9.0

    def S(pts):
        if not wreck:
            return [tuple(p) for p in proj(cam, [(x + bow * u, y, z) for u, z in pts])[0]]
        side = -1 if np.mean([u for u, _ in pts]) < 0 else 1           # each shape belongs to one half
        w = [wreck_xform(u if u * side > 0 else side * 0.01, z, L, brk) for u, z in pts]
        w = clip_up(w, lambda p: p[1] + 0.05) if len(w) > 1 else w     # nothing below the sea
        if len(w) < 2:
            return []
        return [tuple(p) for p in proj(cam, [(x + bow * u, y, z) for u, z in w])[0]]

    if wreck:
        hull = mix(hull, (24, 20, 20), 0.6)
        for s in (-1, 1):
            torn = _torn(s, fb, 4 if s < 0 else 9)
            if s < 0:
                hp = [(-L / 2 + 3, -16), (-L / 2 + 3, 0), (-L / 2, fb + 0.5)] + torn
            else:
                hp = [(L / 2 - 26, fb), (L / 2 - 24, fb + 3), (L / 2 + 1, fb + 3.2), (L / 2 - 5, 0),
                      (L / 2 - 9, -16)] + torn[::-1]
            pen.poly(S(hp), hz(hull), lw, ink)
            red = clip_up(hp, lambda p: 1.3 - p[1])                        # the red bottom, up to the old waterline
            if len(red) > 2:
                pen.poly(S(red), hz(band), 0)
            face = torn[2:] + [(u + s * 7, z) for u, z in torn[2:][::-1]]  # the open tank inside the torn end
            pen.poly(S(face), (26, 16, 14), 0)
            pen.poly(S(hp), None, lw, ink)
    else:
        # hull: raked stem, raised forecastle, near-vertical transom
        hp = [(-L / 2 + 3, 0), (-L / 2, fb + 0.5), (L / 2 - 26, fb), (L / 2 - 24, fb + 3), (L / 2 + 1, fb + 3.2),
              (L / 2 - 5, 0)]
        pen.poly(S(hp), hz(hull), lw, ink)
        pen.poly(S([(-L / 2 + 3, 0), (L / 2 - 5, 0), (L / 2 - 4.6, 1.3), (-L / 2 + 2.8, 1.3)]), hz(band), 0)
        pen.poly(S(hp), None, lw, ink)
    # deck: pipe run on a catwalk, posts
    runs = [((-L / 2 + 38, fb + 1.6), (-12, fb + 1.6)), ((12, fb + 1.6), (L / 2 - 30, fb + 1.6))] if wreck else \
        [((-L / 2 + 38, fb + 1.6), (L / 2 - 30, fb + 1.6))]
    for pr in runs:
        pts = S(list(pr))
        if len(pts) > 1:
            pen.line(pts, hz((196, 190, 176)), max(1.0, lw * 0.9))
    for u in np.linspace(-L / 2 + 40, L / 2 - 32, 14):
        if wreck and abs(u) < 16:
            continue
        pts = S([(u, fb), (u, fb + 1.6)])
        if len(pts) > 1:
            pen.line(pts, hz((120, 116, 108)), 1.0)
    if state == 'whole':                             # cranes and the manifold amidships
        for u, sgn in ((-6, 1), (8, -1)):
            pen.line(S([(u, fb), (u, fb + 14)]), hz((226, 222, 210)), max(1.0, lw * 0.9))
            pen.line(S([(u, fb + 12), (u + sgn * 16, fb + 4)]), hz((226, 222, 210)), max(1.0, lw * 0.8))
        pen.poly(S([(-3, fb), (5, fb), (5, fb + 3), (-3, fb + 3)]), hz((150, 150, 146)), 1.0, ink)
    # the bridge block aft: six storeys, wider wings at the top, a dark band of windows
    b0, b1 = -L / 2 + 8, -L / 2 + 36
    pen.poly(S([(b0, fb), (b1, fb), (b1, fb + 16), (b1 + 3, fb + 16), (b1 + 3, fb + 18), (b0 - 2, fb + 18),
                (b0 - 2, fb + 16), (b0, fb + 16)]), hz((238, 236, 228)), lw, ink)
    pen.poly(S([(b0, fb + 16.2), (b1 + 2.5, fb + 16.2), (b1 + 2.5, fb + 17.3), (b0, fb + 17.3)]), hz((50, 60, 70)), 0)
    for z in (fb + 3.0, fb + 6.0, fb + 9.0, fb + 12.0):
        pen.line(S([(b0 + 2, z), (b1 - 2, z)]), hz((120, 130, 140)), 1.0)
    # the funnel behind it with its coloured band, a mast on the bridge and one at the bow
    f0, f1 = -L / 2 + 3, -L / 2 + 13
    if wreck:                                        # the funnel top was blown off (FUNNEL_TOP flies): a torn stub
        pen.poly(S([(f0, fb + 14), (f1, fb + 14), (f1 + 0.75, fb + 21.6), (f1 - 2.5, fb + 20.6), (f0 + 5, fb + 21.8),
                    (f0 + 2.5, fb + 20.8), (f0 + 1.4, fb + 21.4)]), hz(mix(fun, (40, 34, 32), 0.55)), lw, ink)
        pen.poly(S([(f0 + 0.6, fb + 20), (f1 + 0.6, fb + 20), (f1 + 0.7, fb + 20.9), (f0 + 1.3, fb + 20.9)]),
                 hz(mix(fband, (40, 34, 32), 0.55)), 0)
    else:
        pen.poly(S([(f0, fb + 14), (f1, fb + 14), (f1 + 1, fb + 27), (f0 + 2, fb + 27)]), hz(fun), lw, ink)
        pen.poly(S([(f0 + 0.6, fb + 20), (f1 + 0.6, fb + 20), (f1 + 0.8, fb + 23), (f0 + 1.3, fb + 23)]), hz(fband), 0)
        pen.poly(S([(f0 + 2, fb + 25.5), (f1 + 1, fb + 25.5), (f1 + 1, fb + 27), (f0 + 2, fb + 27)]), hz((30, 30, 32)), 0)
    pen.line(S([(b0 + 14, fb + 18), (b0 + 14, fb + 26)]), hz((60, 60, 64)), 1.0)
    pen.line(S([(L / 2 - 14, fb + 3), (L / 2 - 14, fb + 14)]), hz((60, 60, 64)), 1.0)
    return dist


def _wake(pen, cam, x, y, L, t):
    """The moving tanker's wake on the sea: a white bow wave, churned water behind the stern, and the spreading V
    (two arms at 19.5 degrees) made of short broken white ripples that fade with age; they shimmer a little."""
    bow, stern = x + L / 2, x - L / 2
    tan = math.tan(math.radians(19.5))
    for sgn in (-1, 1):                                          # the V's two arms, from the bow backwards
        for i in range(70):
            s0 = 18 + i * 11.0
            s1 = s0 + 7.0 + 2.0 * math.sin(t * 2.3 + i)
            age = s0 / 790.0
            col = mix((246, 250, 250), SEA_DAY[3], min(0.95, age * 1.15))
            P, _ = proj(cam, [(bow - s0, y + sgn * s0 * tan, 0), (bow - s1, y + sgn * s1 * tan, 0)])
            pen.line([tuple(p) for p in P], col, 2.0 if sgn < 0 else 1.6)
            if i % 3 == 0 and age < 0.7:                         # transverse ripples between the arms
                m0 = (bow - s0 - 4, y + sgn * s0 * tan * 0.55, 0)
                m1 = (bow - s0 - 10, y + sgn * s0 * tan * 0.25, 0)
                P, _ = proj(cam, [m0, m1])
                pen.line([tuple(p) for p in P], col, 1.4)
    for i in range(16):                                          # churned water behind the stern
        s0 = i * 9.0
        wd = 8 + s0 * 0.12
        col = mix((246, 250, 250), SEA_DAY[3], min(0.9, s0 / 170.0))
        P, _ = proj(cam, [(stern - s0, y - wd, 0), (stern - s0 - 7, y - wd * 1.05, 0), (stern - s0 - 7, y + wd * 1.05, 0),
                          (stern - s0, y + wd, 0)])
        pen.poly([tuple(p) for p in P], col, 0)
    P, _ = proj(cam, [(bow - 2, y - 4, 0), (bow + 1.5, y, 2.2), (bow - 2, y + 4, 0), (bow - 30, y - 6, 0)])
    pen.poly([tuple(p) for p in P], (246, 250, 250), 0)            # the bow wave


# the flotilla at anchor: (x, y, length, colours, haze) world metres; all bows the same way (right)
_SPREAD = [(40, 4200, 300, 0), (170, 7600, 320, 1), (330, 6000, 300, 2), (560, 9000, 330, 4), (650, 5600, 290, 3),
           (880, 7000, 310, 2), (1000, 4300, 270, 1)]   # (screen x, metres out): spread clear of Vance and the near one
ANCHORED = [(_x_at(CLIFF, sx, d), d, L, c) for sx, d, L, c in _SPREAD]


@functools.lru_cache(maxsize=4)
def _strait_still(which):
    """The still part of a strait shot: sky, wisps, far shore, sea bands (no headland: Sam, 8 Nov, the eye goes to the
    tankers)."""
    cam = CAMS[which]
    im = _bands(cam)
    lay = layer()
    pen = Pen(lay)
    _wisps(pen, cam)
    _shore(pen, cam)
    im.alpha_composite(shrink(lay))
    return im


@functools.lru_cache(maxsize=4)
def _flotilla(which):
    cam = CAMS[which]
    lay = layer()
    pen = Pen(lay)
    for x, y, L, c in sorted(ANCHORED, key=lambda a: -a[1]):
        tanker(pen, cam, x, y, L, TANKER_COLS[c])
    return shrink(lay)


@functools.lru_cache(maxsize=4)
def _ripples(which, n=1100):
    """Ripple strokes fixed on the sea (world points), as the Flying Whales sea lays them, for this camera."""
    cam = CAMS[which]
    rnd = np.random.default_rng(7)
    hy = sdir(cam, 0, 0)[1]
    v = rnd.random(n) ** 1.5
    sy = hy + 2 + v * (min(H, hy + 420) - hy - 2)
    sx = rnd.uniform(-60, W + 60, n)
    P = FS._ground(cam, sx, sy)
    ln = rnd.uniform(5, 20, n)
    kind = rnd.random(n) < 0.55
    phase = rnd.uniform(0, 6.3, n)
    return P, ln, kind, phase


def _sea_strokes(pen, cam, which, t):
    P, ln, kind, phase = _ripples(which)
    Q = P.copy()
    Q[:, 0] += 0.25 * t
    breathe = 0.75 + 0.25 * np.sin(1.1 * t + phase)
    A = Q.copy()
    B = Q.copy()
    A[:, 0] -= ln * breathe / 2
    B[:, 0] += ln * breathe / 2
    sa, da = proj(cam, A)
    sb, _ = proj(cam, B)
    hy = sdir(cam, 0, 0)[1]
    for i in np.argsort(-da):
        y = sa[i, 1]
        if y < hy + 1 or da[i] < 30:
            continue
        frac = min(1.0, (y - hy) / 260.0)
        base = SEA_DAY[min(8, int(frac * 6))]
        col = mix(base, (236, 244, 246), 0.35) if kind[i] else mix(base, (22, 70, 92), 0.3)
        pen.line([tuple(sa[i]), tuple(sb[i])], col, 1.0 + 1.4 * frac)


def _track_x(y):
    return VANCE_MARK[0] + 0.09 * (y - VANCE_MARK[1]) + 0.22 * math.sin((y - VANCE_MARK[1]) / 2.4)


def _edge_y(x):
    return 12.0 + 1.4 * math.sin(x / 3.1) + 0.7 * math.sin(x / 1.3 + 1.0)


def _rock(pen, cam, x, y, r, seed, col=None):
    """A stone on the plateau: a lumpy dome with its short hard shadow (high sun, behind us and to the left)."""
    s, d = proj(cam, [(x, y, PLATEAU)])
    if d[0] < 0.6:
        return
    cx, cy = float(s[0][0]), float(s[0][1])
    ppm = cam.focal / float(d[0])
    rx = r * ppm
    flat = min(1.0, (cam.pos[2] - PLATEAU) / float(d[0]) + 0.08)
    rr = random.Random(seed)
    pen.ell(cx + rx * 0.25, cy - rx * flat * 0.5, rx * 0.9, rx * flat * 0.8, ROCK_SH, 0)
    pts = []
    for i in range(12):
        a = math.pi + math.pi * i / 11
        k = rr.uniform(0.8, 1.1)
        pts.append((cx + rx * math.cos(a) * k, cy + rx * 0.75 * math.sin(a) * k))
    pts += [(cx + rx, cy + rx * flat * 0.35), (cx - rx, cy + rx * flat * 0.35)]
    pen.poly(pts, col or rr.choice([ROCK_D, (146, 122, 98), (110, 94, 80), (160, 140, 116)]), max(1.2, min(LW, rx / 6)))


@functools.lru_cache(maxsize=4)
def _cliff_top(which):
    """The plateau in front: pale sand, darker patches, the dirt track Vance walks, scattered stones, the rim, the odd
    thorn tree. Drawn over the sea; everything beyond the rim is sea far below."""
    cam = CAMS[which]
    lay = layer()
    pen = Pen(lay)
    y_cam = float(cam.pos[1])
    xs = np.linspace(-40, 40, 161)
    edge = [(float(x), _edge_y(float(x)), PLATEAU) for x in xs]
    s, d = proj(cam, edge)
    pts = [tuple(p) for p, dd in zip(s, d) if dd > 0.5]
    pen.poly(pts + [(W + 400, H + 400), (-400, H + 400)], SAND, LW)
    lip = [(x, y - 0.25, z - 0.0) for x, y, z in edge]
    s2, _ = proj(cam, lip)
    pen.poly([tuple(p) for p in s] + [tuple(p) for p in s2[::-1]], ROCK, 0)
    pen.line(pts, INK, LW)
    r = random.Random(12)
    for i in range(14):                                        # darker stony patches
        px, py = r.uniform(-7, 7), r.uniform(y_cam + 2.5, 11.5)
        if abs(px - _track_x(py)) < 2.2:
            continue
        rad = r.uniform(0.6, 1.6)
        ring = [(px + rad * math.cos(a) * r.uniform(0.7, 1.1), py + rad * 0.7 * math.sin(a) * r.uniform(0.7, 1.1), PLATEAU)
                for a in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
        sp, dp = proj(cam, ring)
        if (dp > 0.5).all():
            pen.poly([tuple(p) for p in sp], SAND_D, 0)
    def run(off):                                              # one line along the track, out to the cliff edge
        ys = list(np.linspace(y_cam + 0.7, 16.0, 200))
        pts = []
        for y in ys:
            x = _track_x(y) + off
            if y >= _edge_y(x):
                pts.append((x, _edge_y(x), PLATEAU))
                break
            pts.append((x, y, PLATEAU))
        return pts
    left, right = run(-1.3), run(1.3)                         # the dirt track runs right up to the edge (Sam, 8 Nov)
    rim = [(x, _edge_y(x), PLATEAU) for x in np.linspace(left[-1][0], right[-1][0], 12)]
    sp, _ = proj(cam, left + rim + right[::-1])
    pen.poly([tuple(p) for p in sp], SAND_L, LW)
    for off in (-0.75, 0.75):
        sp, _ = proj(cam, run(off))
        pen.line([tuple(p) for p in sp], (200, 182, 146), 3.0)
    pen.line(pts, INK, LW)                                     # the rim's ink over the track's end
    rocks = []
    for i in range(260):
        py = y_cam + 1.0 + (11.6 - y_cam - 1.0) * r.random() ** 1.3
        px = r.uniform(-0.6, 0.6) * (py - y_cam) * 1.3
        if abs(px - _track_x(py)) < 1.45:
            continue
        rocks.append((px, py, r.uniform(0.03, 0.22) * (0.6 if r.random() < 0.65 else 1.5), i))
    for i in range(120):                                       # grit on the track itself
        py = y_cam + 1.0 + (11.6 - y_cam - 1.0) * r.random() ** 1.3
        rocks.append((_track_x(py) + r.uniform(-1.2, 1.2), py, r.uniform(0.015, 0.05), 900 + i))
    for x in (-6.5, -2.0, 2.5, 5.5, 8.0):                                    # boulders on the rim
        rocks.append((x, _edge_y(x) - 0.4, 0.45, 200 + int(x)))
    for x, y, rad, sd in sorted(rocks, key=lambda q: -q[1]):
        _rock(pen, cam, x, y, rad, sd)
    return shrink(lay)


def strait(which, t, near=None, fx=None, ground=True):
    """One frame of a strait shot ('wide' or 'close') at time t. near: ('sail', x) the moving tanker under way with its
    wake, ('wreck', x[, brk]) stopped and torn in two, or None. fx(img, cam): the showstopper's effects, drawn after the ships
    and before the cliff top."""
    cam = CAMS[which]
    im = _strait_still(which).copy()
    lay = layer()
    pen = Pen(lay)
    _sea_strokes(pen, cam, which, t)
    im.alpha_composite(shrink(lay))
    im.alpha_composite(_flotilla(which))
    if near:
        lay = layer()
        pen = Pen(lay)
        if near[0] == 'sail':
            _wake(pen, cam, near[1], NEAR_Y, NEAR_L, t)
        tanker(pen, cam, near[1], NEAR_Y, NEAR_L, TANKER_COLS[0], 'whole' if near[0] == 'sail' else 'wreck',
               brk=near[2] if len(near) > 2 else None)
        im.alpha_composite(shrink(lay))
    if fx:
        fx(im, cam)
    if ground:
        im.alpha_composite(_cliff_top(which))
    return im


def place_cliff(x, y, which='wide'):
    """Screen x, soles y and px per metre for someone standing on the plateau at world (x, y)."""
    cam = CAMS[which]
    s, d = proj(cam, [(x, y, PLATEAU)])
    return float(s[0][0]), float(s[0][1]), cam.focal / float(d[0])


def cliff_shadow(img, x, y, ppm):
    """Vance's short hard shadow at his feet (high sun): a flat dark patch just behind his soles."""
    d = ImageDraw.Draw(img, 'RGBA')
    d.ellipse([x - 0.24 * ppm, y - 0.09 * ppm, x + 0.3 * ppm, y + 0.02 * ppm], fill=ROCK_SH + (255,))


# ---------------------------------------------------------------------------------------------- shot 4: gas station
# A level camera 1.6 m up, horizon y 900, focal 2160 (a long lens: the men 4.5 m away at 480 px/m). We look over the
# pump island (in front, its curb hides their feet) at the man and his pickup (side on, driver side, 6 m away), the
# canopy overhead to 8.5 m, the price board on its pylon 20 m away by the road, flat land beyond.
GAS = Level(1.6, 900.0, 2160.0)
D_MEN, D_TRUCK, D_ISLAND = 4.5, 6.0, (3.7, 4.3)
MAN_X, VANCE_X = -0.2, 0.35                           # where they stand (world x at 4.5 m)
TRUCK_FRONT = -4.64                                   # the pickup's front bumper (world x); its filler at x -0.58
BOARD = dict(x=-1.02, d=20.0, top=8.0, half=1.3)
SKY_GAS = [(150, 198, 238), (166, 208, 240), (184, 218, 242), (204, 228, 244)]
CONC, CONC_D = (184, 182, 176), (160, 158, 152)
CANOPY_RED = (196, 40, 40)


def _gp(x, d, z):
    return GAS.p(x, d, z)


def _gbox(x0, x1, d, z0, z1):
    (a, b), (c, e) = _gp(x0, d, z1), _gp(x1, d, z0)
    return box(a, b, c, e)


def _ground_quad(x0, x1, d0, d1):
    return [_gp(x0, d0, 0), _gp(x1, d0, 0), _gp(x1, d1, 0), _gp(x0, d1, 0)]


def _board(pen):
    b = BOARD
    ppm = GAS.ppm(b['d'])
    pen.poly(cut(_gbox(b['x'] - 0.2, b['x'] + 0.2, b['d'], 0, b['top'] - 2.4), 1.5, 90), (96, 96, 102), LW)  # pylon
    y_top = _gp(0, b['d'], b['top'])[1]
    x0, x1 = _gp(b['x'] - b['half'], b['d'], 0)[0], _gp(b['x'] + b['half'], b['d'], 0)[0]
    rows = [('DIESEL', '6.15'), ('REGULAR', '4.39'), ('PREMIUM', '5.25')]     # peak war prices (Sam, 7 Nov)
    blank, rh = 0.72 * ppm, 0.6 * ppm
    y_bot = y_top + blank + len(rows) * rh + 0.12 * ppm
    pen.poly(cut(box(x0, y_top, x1, y_bot), 1.5, 91), (238, 238, 234), LW)
    pen.poly(cut(box(x0 + 6, y_top + 6, x1 - 6, y_top + blank - 4), 1.5, 92), CANOPY_RED, 2)   # the blank top panel
    pen.poly(box(x0 + 20, y_top + blank * 0.4, x1 - 20, y_top + blank * 0.6), (236, 230, 220), 0)
    for i, (name, price) in enumerate(rows):
        y = y_top + blank + i * rh + 0.06 * ppm
        pen.poly(cut(box(x0 + 6, y, x1 - 6, y + rh - 6), 1.0, 93 + i), (22, 22, 24), 2)
        pen.text((x0 + 16, y + rh * 0.5), name, rh * 0.26, (240, 240, 236), 'lm')
        pen.text((x1 - 44, y + rh * 0.52), price, rh * 0.62, (255, 82, 48) if i == 0 else (255, 196, 60), 'rm')
        pen.text((x1 - 40, y + rh * 0.2), '9', rh * 0.26, (255, 82, 48) if i == 0 else (255, 196, 60), 'lt')
    return (x0, y_top, x1, y_bot)


BOARD_BOX = None                                      # set when the station is painted


def _sky_land(pen):
    hz = GAS.hz
    for k, c in enumerate(SKY_GAS):
        y0 = -20 + k * (hz + 20) / 4
        pen.poly(wobbly(box(-20, y0, W + 20, hz + 2), 3, 300 + k, 120), c, 0)
    for cx, cy, ln, sd in ((700, 300, 260, 1), (980, 220, 180, 2), (200, 360, 160, 3)):      # flat cumulus
        r = random.Random(sd)
        lumps = [(cx - ln / 2 + ln * i / 5, cy - r.uniform(14, 40)) for i in range(6)]
        pts = []
        for i, (x, y) in enumerate(lumps):
            for a in np.linspace(math.pi, 2 * math.pi, 6):
                pts.append((x + ln / 10 * math.cos(a) * 1.2, y + 26 * math.sin(a)))
        pts += [(cx + ln / 2 + 20, cy + 10), (cx - ln / 2 - 20, cy + 10)]
        pen.poly(pts, (248, 250, 252), 2, (150, 170, 190))
        pen.poly([(cx - ln / 2 - 14, cy + 2), (cx + ln / 2 + 14, cy + 2), (cx + ln / 2 + 20, cy + 10),
                  (cx - ln / 2 - 20, cy + 10)], (220, 228, 236), 0)
    # flat fields to the horizon in strips, a dark road, a verge, the forecourt's edge
    fields = [(2000, 1e5, (178, 168, 112)), (700, 2000, (150, 156, 92)), (300, 700, (190, 172, 108)),
              (120, 300, (156, 160, 96)), (60, 120, (196, 178, 112)), (44, 60, (128, 150, 84)),
              (34, 44, (78, 78, 82)), (22, 34, (120, 146, 80))]
    for d0, d1, col in fields:
        pen.poly(wobbly(_ground_quad(-1e4, 1e4, d0, d1), 0.6, int(d0), 60), col, 0)
    for k in range(-30, 30):                                               # yellow centre dashes
        x0 = k * 6.0
        pen.poly(_ground_quad(x0, x0 + 3, 38.9, 39.1), (236, 200, 60), 0)
    # far off: a grain elevator, a farmstead's trees
    gx, gd = 163.0, 1500.0                                                 # right of Vance's head
    sky = (204, 228, 244)
    hz_ = lambda c: mix(c, sky, 0.3)
    ink = mix(INK, sky, 0.35)
    ppm = GAS.ppm(gd)
    # a farm grain site, not a monument (Sam, 8 Nov: pillars with a bar across read as Stonehenge): three round
    # steel bins with cone roofs, ribbed, touching; a tall thin elevator leg beside them; spouts down to each bin
    for k, (dx, wd, hgt) in enumerate(((0, 13, 16), (13.5, 13, 16), (27, 10, 12))):
        x0, x1 = gx + dx, gx + dx + wd
        pen.poly(_gbox(x0, x1, gd, 0, hgt), hz_((196, 198, 200)), 1.4, ink)
        for z in np.arange(2.0, hgt, 2.5):
            pen.line([_gp(x0, gd, z), _gp(x1, gd, z)], hz_((168, 170, 174)), 1.0)
        pen.poly([_gp(x0 - 0.4, gd, hgt), _gp(x1 + 0.4, gd, hgt), _gp((x0 + x1) / 2, gd, hgt + wd * 0.42)],
                 hz_((176, 178, 182)), 1.4, ink)
    lx = gx + 38.0
    pen.poly(_gbox(lx, lx + 3.2, gd, 0, 38), hz_((214, 210, 200)), 1.4, ink)
    pen.poly([_gp(lx - 0.8, gd, 38), _gp(lx + 4.0, gd, 38), _gp(lx + 1.6, gd, 41)], hz_((170, 60, 50)), 1.2, ink)
    for dx, wd, hgt in ((0, 13, 16), (13.5, 13, 16), (27, 10, 12)):
        pen.line([_gp(lx, gd, 35), _gp(gx + dx + wd / 2, gd, hgt + wd * 0.42)], ink, 1.0)
    for x in (180.0, 210.0, 240.0):
        cx, cy = _gp(x, 1200, 0)
        pen.ell(cx, cy - 9, 14, 10, mix((86, 110, 60), (204, 228, 244), 0.3), 1.4, mix(INK, (204, 228, 244), 0.4))


def _poles(pen):
    """Power poles along the far side of the road, wires sagging between them."""
    tops = []
    for x in (-3.5, 9.8, -17.0):
        d = 46.0
        ppm = GAS.ppm(d)
        pen.poly(_gbox(x - 0.15, x + 0.15, d, 0, 11.0), (110, 86, 62), 2)
        pen.poly(_gbox(x - 1.1, x + 1.1, d, 10.2, 10.45), (110, 86, 62), 2)
        tops.append((x, d))
    for (xa, da), (xb, db) in ((tops[2], tops[0]), (tops[0], tops[1])):
        for off in (-0.9, 0.0, 0.9):
            pts = []
            for u in np.linspace(0, 1, 24):
                x = xa + (xb - xa) * u
                z = 10.45 - 1.6 * 4 * u * (1 - u)
                pts.append(_gp(x + off, da, z))
            pen.line(pts, (40, 40, 44), 1.4)


def _shop(pen):
    """A low shop with a glass front on the right, set back by the road (no name on it)."""
    d = 21.0
    pen.poly(cut(_gbox(3.0, 12.0, d, 0, 4.2), 1.5, 120), (226, 220, 206), LW)
    pen.poly(cut(_gbox(3.0, 12.0, d, 3.4, 4.2), 1.5, 121), CANOPY_RED, LW)
    pen.poly(cut(_gbox(3.3, 11.7, d, 0.3, 3.1), 1.5, 122), (70, 92, 112), LW)
    for x in np.arange(3.3, 11.7, 1.4):
        pen.poly(_gbox(x, x + 0.08, d, 0.3, 3.1), (210, 212, 214), 1.2)
    pen.poly(_gbox(3.6, 4.4, d, 1.2, 2.2), (240, 214, 90), 1.4)          # a poster (blank)
    pen.poly(_gbox(5.2, 6.4, d, 0.3, 2.5), (40, 54, 66), 1.6)            # the door


def _canopy(pen):
    """Overhead: the canopy's lit underside to its edge 8.5 m away, the coloured band round its edge, a column."""
    edge = 8.5
    y_e = _gp(0, edge, 4.9)[1]
    pen.poly(box(-20, -20, W + 20, y_e), (232, 232, 228), 0)
    for d in (8.0,):
        for x in (-2.0, 0.0, 2.0):
            pts = [_gp(x - 0.5, d - 0.25, 4.9), _gp(x + 0.5, d - 0.25, 4.9), _gp(x + 0.5, d + 0.25, 4.9), _gp(x - 0.5, d + 0.25, 4.9)]
            pen.poly(pts, (255, 252, 226), 2)
    pen.poly(cut(box(-20, y_e - 4, W + 20, y_e + 0.32 * GAS.ppm(edge)), 2, 130), CANOPY_RED, LW)
    pen.poly(box(-20, y_e + 0.32 * GAS.ppm(edge) - 10, W + 20, y_e + 0.32 * GAS.ppm(edge) - 4), (240, 240, 236), 0)
    pen.poly(cut(_gbox(-2.3, -1.85, edge, 0, 4.7), 1.5, 131), (210, 210, 206), LW)   # a square column (left)


def _forecourt(pen):
    pen.poly(_ground_quad(-1e3, 1e3, 1.0, 22.0), CONC, 0)
    pen.line([(-20, _gp(0, 22.0, 0)[1]), (W + 20, _gp(0, 22.0, 0)[1])], INK, 2)
    for d in (5.5, 9.0, 13.0, 17.0):                                      # expansion joints
        y = _gp(0, d, 0)[1]
        pen.line([(-20, y), (W + 20, y)], CONC_D, 2)
    for x in (-6.0, -2.0, 2.0, 6.0):
        pen.line([_gp(x, 3.0, 0), _gp(x, 22.0, 0)], CONC_D, 2)
    r = random.Random(5)
    for x, d, rad in ((-0.4, 7.2, 0.5), (1.2, 9.5, 0.7), (-2.4, 12.0, 0.9), (0.6, 15.0, 0.6), (2.4, 6.6, 0.4)):
        ring = [(x + rad * math.cos(a) * r.uniform(0.6, 1.1), d + rad * 0.8 * math.sin(a) * r.uniform(0.6, 1.1))
                for a in np.linspace(0, 2 * math.pi, 11, endpoint=False)]
        pen.poly([_gp(px, pd, 0) for px, pd in ring], (148, 144, 138), 0)


# ---------------------------------------------------------------------------------------------- the pickup
PICKUP_WHITE, PICKUP_TRIM, GLASS_TINT = (238, 238, 234), (40, 40, 44), (54, 62, 74)


def pickup(pen, x_front, ground_y, ppm, body=PICKUP_WHITE, facing=-1):
    """A full-size 4x4 crew-cab pickup side on (5.9 m long, 1.95 m tall), facing left (driver side to us): square
    grille and high flat bonnet, crew cab with four doors and tinted glass, big mirrors, an open bed and tailgate,
    big wheels high off the ground in flared arches, a running board, the fuel flap ahead of the rear wheel.
    x_front: the front bumper's screen x; returns the fuel flap's middle (screen)."""
    P = lambda u, z: (x_front - facing * u * ppm, ground_y - z * ppm)
    Q = lambda pts: [P(u, z) for u, z in pts]
    ax_f, ax_r, tr, rr = 0.95, 4.63, 0.42, 0.25
    arch = lambda ax: [(ax + 0.53 * math.cos(a), 0.42 + 0.53 * math.sin(a)) for a in np.linspace(0, math.pi, 13)]
    body_pts = [(0.05, 0.42), (0.02, 1.25), (0.25, 1.32), (1.72, 1.36), (2.45, 1.93), (2.6, 1.96), (3.95, 1.96),
                (4.05, 1.9), (4.08, 1.32), (5.86, 1.32), (5.9, 0.55)] + arch(ax_r) + [(4.0, 0.5), (1.6, 0.5)] + arch(ax_f)
    pen.poly(Q(body_pts), body, LW)
    pen.poly(Q([(5.86, 1.32), (5.9, 1.32), (5.9, 0.6), (5.86, 0.6)]), mix(body, (0, 0, 0), 0.08), 2)
    for ax in (ax_f, ax_r):                                                   # flared arches (black)
        outer = [(ax + 0.6 * math.cos(a), 0.42 + 0.6 * math.sin(a)) for a in np.linspace(-0.12, math.pi + 0.12, 15)]
        inner = [(ax + 0.52 * math.cos(a), 0.42 + 0.52 * math.sin(a)) for a in np.linspace(math.pi + 0.12, -0.12, 15)]
        pen.poly(Q(outer + inner), PICKUP_TRIM, 2)
    pen.poly(Q([(1.68, 0.44), (4.0, 0.44), (4.0, 0.53), (1.68, 0.53)]), PICKUP_TRIM, 2)   # running board
    pen.poly(Q([(-0.04, 0.38), (0.25, 0.38), (0.25, 0.78), (-0.04, 0.78)]), (150, 150, 156), 2)   # front bumper
    pen.poly(Q([(0.0, 0.8), (0.12, 0.8), (0.1, 1.26), (0.0, 1.24)]), (70, 70, 76), 2)          # the grille's edge
    pen.poly(Q([(0.05, 1.08), (0.32, 1.1), (0.3, 1.24), (0.05, 1.22)]), (240, 238, 220), 1.5)   # headlamp
    pen.poly(Q([(5.72, 0.36), (5.98, 0.36), (5.98, 0.66), (5.72, 0.66)]), (150, 150, 156), 2)  # rear bumper
    pen.poly(Q([(5.8, 0.95), (5.9, 0.95), (5.9, 1.3), (5.8, 1.3)]), (196, 34, 34), 1.5)        # tail lamp
    pen.poly(Q([(4.08, 1.3), (5.86, 1.3), (5.86, 1.36), (4.08, 1.36)]), PICKUP_TRIM, 1.5)      # bed rail cap
    # glass: windscreen edge, front and rear door windows, the B pillar
    pen.poly(Q([(1.95, 1.42), (2.45, 1.86), (3.0, 1.86), (3.0, 1.42)]), GLASS_TINT, 2)
    pen.poly(Q([(3.08, 1.42), (3.08, 1.86), (3.9, 1.86), (3.96, 1.42)]), GLASS_TINT, 2)
    pen.line(Q([(2.15, 1.82), (2.5, 1.5)]), (120, 130, 144), 2)
    # door seams and handles, the body crease
    for u0, u1 in ((1.82, 3.04), (3.04, 4.04)):
        pen.line(Q([(u0, 1.4), (u0, 0.55)]), INK, 2)
    pen.line(Q([(4.04, 1.4), (4.04, 0.55)]), INK, 2)
    pen.line(Q([(0.3, 1.0), (5.86, 1.0)]), mix(body, INK, 0.35), 1.5)
    for u in (2.8, 3.82):
        pen.poly(Q([(u, 1.18), (u + 0.18, 1.18), (u + 0.18, 1.23), (u, 1.23)]), PICKUP_TRIM, 1.2)
    # the big tow mirror on the A pillar
    pen.poly(Q([(1.78, 1.38), (2.02, 1.38), (2.04, 1.7), (1.8, 1.72)]), PICKUP_TRIM, 2)
    pen.poly(Q([(1.82, 1.42), (2.0, 1.42), (2.0, 1.66), (1.83, 1.67)]), (150, 166, 186), 1.2)
    # the fuel flap: on the bed side, over the front of the rear arch
    fx, fz = 4.2, 1.12
    pen.poly(Q([(fx - 0.09, fz - 0.09), (fx + 0.09, fz - 0.09), (fx + 0.09, fz + 0.09), (fx - 0.09, fz + 0.09)]),
             mix(body, INK, 0.1), 1.8)
    # wheels: big tyres, silver six-lug rims
    for ax in (ax_f, ax_r):
        cx, cy = P(ax, tr)
        pen.ell(cx, cy, tr * ppm, tr * ppm, (34, 34, 36), LW)
        pen.ell(cx, cy, rr * ppm, rr * ppm, (176, 178, 184), 2)
        for k in range(6):
            a = k * math.pi / 3
            pen.line([(cx + 0.06 * ppm * math.cos(a), cy + 0.06 * ppm * math.sin(a)),
                      (cx + 0.22 * ppm * math.cos(a), cy + 0.22 * ppm * math.sin(a))], (120, 122, 128), 0.035 * ppm)
        pen.ell(cx, cy, 0.06 * ppm, 0.06 * ppm, (150, 152, 158), 1.5)
    return P(fx, fz)


def _island(pen):
    """The pump island in front of the men: a raised concrete curb across the frame, its end post, the pump on it at
    the left (its long face to us: header, screen, grade buttons, the holster he took the nozzle from, a hose)."""
    d0, d1 = D_ISLAND
    zt = 0.18
    top = [_gp(-4.0, d1, zt), _gp(1.05, d1, zt), _gp(1.3, (d0 + d1) / 2, zt), _gp(1.05, d0, zt), _gp(-4.0, d0, zt)]
    pen.poly(top, (206, 204, 198), LW)
    pen.poly([_gp(-4.0, d0, zt), _gp(1.05, d0, zt), _gp(1.05, d0, 0), _gp(-4.0, d0, 0)], (176, 174, 168), LW)
    pen.poly([_gp(-4.0, d0, zt), _gp(1.05, d0, zt), _gp(1.05, d0, zt - 0.05), _gp(-4.0, d0, zt - 0.05)], (236, 200, 50), 0)
    # the end post (yellow, black bands)
    bx, bd = 1.0, (d0 + d1) / 2
    pen.poly(_gbox(bx - 0.08, bx + 0.08, bd, zt, 1.1), (236, 196, 40), LW)
    for z in (0.5, 0.8):
        pen.poly(_gbox(bx - 0.08, bx + 0.08, bd, z, z + 0.08), (30, 30, 32), 0)
    # the pump
    pd = 4.0
    x0, x1 = -1.95, -0.78                         # mostly off the left edge: its right end shows
    pen.poly(cut(_gbox(x0, x1, pd, zt, zt + 0.25), 1.5, 140), (120, 124, 130), LW)        # plinth
    pen.poly(cut(_gbox(x0, x1, pd, zt + 0.25, zt + 1.85), 1.5, 141), (236, 236, 232), LW)  # body
    pen.poly(cut(_gbox(x0 - 0.03, x1 + 0.03, pd, zt + 1.85, zt + 2.2), 1.5, 142), (40, 80, 150), LW)  # lit header
    pen.poly(_gbox(x0 + 0.1, x1 - 0.1, pd, zt + 1.95, zt + 2.1), (236, 240, 250), 0)
    pen.poly(cut(_gbox(x1 - 0.52, x1 - 0.1, pd, zt + 1.3, zt + 1.7), 1.0, 143), (28, 34, 30), 2)   # screen
    for k, z in enumerate((zt + 1.6, zt + 1.48, zt + 1.36)):
        (a, b), (c, e) = _gp(x1 - 0.46, pd, z), _gp(x1 - 0.18, pd, z - 0.05)
        pen.poly(box(a, b, c, e), (90, 200, 120), 0)
    for k, col in enumerate(((60, 140, 60), (230, 180, 40), (200, 50, 40))):          # grade buttons
        (a, b), (c, e) = _gp(x1 - 0.5 + k * 0.14, pd, zt + 1.18), _gp(x1 - 0.41 + k * 0.14, pd, zt + 1.08)
        pen.poly(box(a, b, c, e), col, 1.5)
    # holsters: the left one with its nozzle, the right one empty (he holds that nozzle)
    for hx, full in ((x1 - 0.55, True), (x1 - 0.2, False)):
        pen.poly(_gbox(hx - 0.06, hx + 0.1, pd, zt + 0.75, zt + 1.0), (60, 60, 64), 2)
        if full:
            pen.poly(_gbox(hx - 0.04, hx + 0.08, pd, zt + 0.6, zt + 0.98), (30, 30, 32), 2)
            pts = [_gp(hx, pd, zt + 0.62), _gp(hx - 0.05, pd, zt + 0.3), _gp(hx + 0.12, pd, zt + 0.32),
                   _gp(hx + 0.25, pd, zt + 1.85)]
            pen.line(pts, (24, 24, 26), 0.035 * GAS.ppm(pd))
    return _gp(x1 - 0.12, pd, zt + 1.85)


@functools.lru_cache(maxsize=1)
def _gas_layers():
    global BOARD_BOX
    back = layer()
    pen = Pen(back)
    _sky_land(pen)
    _poles(pen)
    BOARD_BOX = _board(pen)
    _shop(pen)
    _forecourt(pen)
    _canopy(pen)
    ppm = GAS.ppm(D_TRUCK)
    filler = pickup(pen, _gp(TRUCK_FRONT, D_TRUCK, 0)[0], _gp(0, D_TRUCK, 0)[1], ppm)
    front = layer()
    hose = _island(Pen(front))
    return shrink(back), shrink(front), filler, hose


def gas_back():
    return _gas_layers()[0].copy()


def gas_front():
    return _gas_layers()[1]


def gas_points():
    """FILLER (the truck's fuel flap) and HOSE_FROM (the empty holster's hose exit), screen points."""
    _, _, filler, hose = _gas_layers()
    return dict(filler=filler, hose_from=hose, board=BOARD_BOX)


def place_gas(x, d=D_MEN):
    """Screen x, soles y and px per metre for someone standing on the forecourt at world (x, d)."""
    sx, sy = GAS.p(x, d, 0)
    return sx, sy, GAS.ppm(d)


# ---------------------------------------------------------------------------------------------- the cast in place
def _cast():
    import ad_vanced_notice_comp as CP
    CP.setup()
    return CP


def study_frame(t=1.0):
    CP = _cast()
    import ad_vanced_notice_cast as AC
    im = study_back(t)
    j = study_pose(sitting.pose(AC.VANCE, 'hands folded'))
    v = STUDY_VANCE
    V.person(im, AC.B.Cam(1.0, 540, 960), v['x'], v['neck_y'], v['s'], dict(AC.VANCE, mood='smile', mouth='rest'),
             t, 0.0, j)
    im.alpha_composite(study_front())
    return im


def cliff_frame(t=2.0, at=VANCE_MARK, near=('sail', X_HIT - 30)):
    CP = _cast()
    import ad_vanced_notice_cast as AC
    im = strait('wide', t, near)
    x, y, ppm = place_cliff(*at)
    cliff_shadow(im, x, y, ppm)
    CP.person(im, AC.VANCE, x, y, ppm, 0, mood='sincere')
    return im


def close_frame(t=3.5):
    CP = _cast()
    import ad_vanced_notice_cast as AC
    im = strait('close', t, ('wreck', X_HIT))
    CP.person(im, AC.VANCE, 430, 1920 + 1500, 1500, 0, mood='sincere', mouth='rest')
    return im


def gas_frame(t=4.0):
    CP = _cast()
    import ad_vanced_notice_cast as AC
    im = gas_back()
    mx, feet, ppm = place_gas(MAN_X)
    vx, _, _ = place_gas(VANCE_X)
    j = V.standing(AC.VANCE)
    V.arm_to(j, 'L', (-360, 40, 40), 'out', 'palm')
    CP.person(im, AC.VANCE, vx, feet + 10, ppm * 1.01, 0, j, mood='smile', mouth='rest')
    jm = V.standing(AC.MAN)
    V.arm_to(jm, 'L', (-250, 330, 60), 'down', 'fist')
    CP.person(im, AC.MAN, mx, feet, ppm, 0, jm, head_yaw=-8, anger=4, gaze_dy=-1.0)
    im.alpha_composite(gas_front())
    return im


class Ortho:
    """A flat side-on view for the props sheet: x right, z up, k px per metre, no perspective."""
    def __init__(self, cx, cy, k):
        self.cx, self.cy, self.focal = cx, cy, k * 1000.0
        self.k = k

    def screen(self, P):
        P = np.asarray(P, float)
        return np.stack([self.cx + P[..., 0] * self.k, self.cy - P[..., 2] * self.k], -1), np.full(P.shape[:-1], 1000.0)


def props_frame(t=5.0):
    """The new props at real size beside a 1.75 m person and a 1 m ruler (sizes.scale_ref), and the tanker beside
    a 100 m bar."""
    import sizes
    im = Image.new('RGBA', (W, H), (236, 232, 224, 255))
    lay = layer()
    pen = Pen(lay)
    ppm = 160.0
    pickup(pen, 60, 760, ppm)
    pen.text((40, 40), 'PICKUP  5.9 x 1.95 m, side on, driver side', 30, (30, 30, 34))
    k = 3.0
    pen.text((40, 900), 'TANKER  330 m, side on (whole)', 30, (30, 30, 34))
    tanker(pen, Ortho(540, 1060, k), 0, 0, 330, TANKER_COLS[0], haze=0.0)
    pen.line([(60, 1100), (60 + 100 * k, 1100)], (200, 40, 40), 4)
    pen.text((60 + 100 * k + 12, 1086), '100 m', 26, (200, 40, 40))
    pen.text((40, 1150), 'TANKER  wreck: stopped, torn open amidships', 30, (30, 30, 34))
    tanker(pen, Ortho(540, 1300, k), 0, 0, 330, TANKER_COLS[0], 'wreck', haze=0.0)
    pen.text((40, 1380), 'the flotilla: five colourings', 30, (30, 30, 34))
    for i, c in enumerate(TANKER_COLS):
        tanker(pen, Ortho(270 + 540 * (i % 2), 1500 + 90 * (i // 2), 1.5), 0, 0, 290 + 10 * i, c, haze=0.0)
    im.alpha_composite(shrink(lay))
    d = ImageDraw.Draw(im)
    sizes.scale_ref(d, 1000, 760, ppm)
    return im


def picture(t):
    """For benchmark.py and sheet.py: each place at its 'time'."""
    if t < 1.5:
        return study_frame(t)
    if t < 2.4:
        return cliff_frame(t)
    if t < 2.8:
        return cliff_frame(t, (0.25, 9.5), ('sail', X_HIT - 50))
    if t < 3.25:
        return _flotilla_zoom(t)
    if t < 3.9:
        return close_frame(t)
    if t < 4.5:
        return gas_frame(t)
    return props_frame(t)


def frame_image(t):
    return picture(t)


def _flotilla_zoom(t):
    im = cliff_frame(2.0)
    crop = im.crop((380, 760, 1020, 880)).resize((1080, 202), Image.LANCZOS)
    out = Image.new('RGBA', (W, H), (236, 232, 224, 255))
    out.alpha_composite(im.resize((540, 960)), (270, 860))
    out.alpha_composite(crop, (0, 520))
    ImageDraw.Draw(out).rectangle([0, 520, 1079, 722], outline=(200, 40, 40), width=4)
    return out


SHOTS = [('study', 0.0, 1.5), ('cliff: at his mark', 1.5, 2.4), ('cliff: walking on', 2.4, 2.8),
         ('tankers, zoomed', 2.8, 3.25), ('close-up', 3.25, 3.9), ('gas station', 3.9, 4.5), ('props at real size', 4.5, 9)]
FPS = 24


# ---------------------------------------------------------------------------------------------- rule 3 and sizes
BENCHMARK = [
    dict(place='The study', refs=['study-abbotsford.jpg', 'study-canons-ashby.jpg', 'study-oak-fireplace.jpg'], at=1.0,
         items=[('floor-to-ceiling dark oak bookcases, packed with old books', 'done: 3 bays to a 3.6 m cornice, 7 shelves'),
                ('books in leather browns, dark reds and greens, gold spine bands', 'done: 10 leathers, 2 gold bands each'),
                ('shelves in tall bays between flat oak uprights; a cornice on top', 'done: uprights, stepped cornice'),
                ('oak with a lacquer shine: pale highlight streaks on the wood', 'done: streaks on uprights, desk'),
                ('the fireplace set into the book wall (right): stone surround', 'done: chimney breast, stone surround'),
                ('a black firebox, iron grate, logs, a low fire', 'done: fire loops every 2 s, sparks'),
                ('a mantel shelf with a clock and two candlesticks', 'done: bracket clock, brass candlesticks'),
                ('a portrait in a gilt frame over the mantel', 'done: an anonymous gentleman (nobody real)'),
                ('a big pedestal desk: drawers in front, leather top', 'done: 1.8 m, brass handles, green leather'),
                ('warm, low light; the fire glows on the nearby wood', 'done: warm oak; flat glow on the jambs')]),
    dict(place='The cliff and the strait', refs=['cliff-musandam-plateau.jpg', 'cliff-musandam-road.jpg',
                                                  'cliff-musandam-fjord.jpg'], at=2.0,
         items=[('bare limestone mountains, grey-brown, in level layers', 'left out: Sam, 8 Nov: the eye goes to the tankers'),
                ('a stony plateau: pale sand, scattered dark rocks, a dirt track', 'done: track to the cliff edge, ruts, stones'),
                ('sheer cliff faces dropping straight into the sea', 'done: the track runs to a sheer edge; the sea far below'),
                ('calm deep blue-teal sea, fine ripples, no waves', 'done: Flying Whales sea re-lit, ripples drift'),
                ('haze: the farther, the paler and bluer', 'done: ships and hills fade by distance'),
                ('the far shore: flat grey hill shapes on the horizon', 'done: two grey hill bands'),
                ('a pale washed-out blue sky, a few thin wisps', 'done: pale bands, three wisps'),
                ('no plants but the odd thorn tree', 'left out: none in shot; nothing to pull the eye from the tankers'),
                ('high sun: short, hard shadows', 'done: stone shadows; cliff_shadow for Vance')]),
    dict(place='The tankers', refs=['tanker-side-wake.jpg', 'tanker-side-dark.jpg', 'tankers-at-anchor-haze.jpg'], at=3.0,
         items=[('very long and low: 330 m long, about 10 m above the water', 'done: 330 m, 9 m freeboard'),
                ('hull dark above, a red band below; laden ships sit low', 'done: thin red band at the waterline'),
                ('a white bridge block at the stern, 5-6 storeys', 'done: 6 storeys, window band, wings'),
                ('a funnel on the bridge block with a coloured band', 'done: 5 colourings'),
                ('a flat deck: a pipe run and catwalk down the middle', 'done: pipe run on posts'),
                ('cranes and a manifold amidships; a raised bow and mast', 'done'),
                ('no names or logos (decision: no brands)', 'done: none'),
                ('at anchor: still, all pointing the same way', 'done: 7 at anchor + the near one, all bows right'),
                ('under way: a white bow wave and a spreading V wake', 'done: V arms, churn, ripples'),
                ('far ones: grey shapes in the haze, the bridge the tallest bump', 'done: haze by distance')]),
    dict(place='The gas station', refs=['gas-iowa-canopy.jpg', 'gas-price-pylon.jpg', 'gas-price-board.jpg'], at=4.0,
         items=[('a flat canopy on square columns, lit underneath, a coloured band', 'done: lit panels, red band, a column (left)'),
                ('pumps on raised concrete islands, a post at each end', 'done: island in front, yellow post'),
                ('pumps: tall boxes with a screen, black hoses and nozzles', 'done: one holster empty (his nozzle)'),
                ('a pylon price board by the road: a tall pole, a blank top panel', 'done: blank red top panel'),
                ('prices in lit numbers, each ending in a small 9 (9/10 of a cent)', 'done'),
                ('rows: DIESEL 6.15, REGULAR 4.39, PREMIUM 5.25 (peak war prices)', 'done'),
                ('a pale concrete forecourt with oil stains', 'done: joints and stains'),
                ('flat land to the horizon under a huge sky; power poles', 'done: field strips, poles, wires'),
                ('a grain elevator in the distance', 'done: steel bins and a leg tower, right of Vance'),
                ('a low shop with a glass front behind', 'done: on the right, no name')]),
    dict(place='The pickup', refs=['pickup-side.jpg', 'pickup-rear.jpg', 'gas-nozzle-filler.jpg'], at=5.0,
         items=[('a full-size 4x4 crew cab: 4 doors, 5.9 m long, 1.9 m tall', 'done: 5.9 x 1.96 m'),
                ('a big square grille and a high, flat bonnet', 'done (out of the gas shot: rear half in frame)'),
                ('an open bed behind the cab with a tailgate', 'done'),
                ('big wheels, chunky tyres, high off the ground', 'done: 0.84 m tyres, six-lug rims'),
                ('flared wheel arches; a running board under the doors', 'done'),
                ('big side mirrors; dark tinted glass', 'done'),
                ('the fuel flap on the driver side, ahead of the rear wheel', 'done: over the rear arch\'s front'),
                ('seen side on facing left: the driver side, as in the photo', 'done'),
                ('plain white paint (my pick: both men stand out against it)', 'done')]),
]

PROP_SIZES = [  # (name, sizes kind, width, height, px per metre: None = metres)
    ('pedestal desk', 'pedestal desk', 2 * DESK_HALF, DESK_Z, None),
    ('crystal tumbler', 'tumbler', 0.085, 0.10, None),
    ('desk flag (2 x 3 ft)', 'desk flag', 0.915, 0.61, None),
    ('fireplace surround', 'fireplace', 1.3, 1.3, None),
    ('bookcase (floor to cornice)', 'bookcase', 0.82, 3.32, None),
    ('oil tanker (near)', 'oil tanker', NEAR_L, 9.0 + 27.0, None),
    ('pickup', 'pickup truck', 5.9, 1.96, None),
    ('fuel pump', 'fuel pump', 1.17, 2.2, None),
    ('price board', 'price sign', 2 * BOARD['half'], 0.72 + 3 * 0.6 + 0.12, None),
    ('canopy clearance', 'gas canopy', 8.5, 4.9, None),
    ('thorn tree', 'thorn tree', 2.5, 2.4, None),
]
KEEP_CLEAR_BOXES = {'price board': lambda: gas_points()['board']}


# ---------------------------------------------------------------------------------------------- sheets
def _label(im, text, size=30):
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, size)
    d.rectangle([0, 0, im.width, size + 16], fill=(20, 20, 24))
    d.text((10, 6), text, font=f, fill=(255, 255, 255))


def sheet(out):
    """The four shots with the cast in place (TikTok safe area marked) and the props sheet, 1080 px wide."""
    tiles = [('1 Study', study_frame(1.0)), ('2 Cliff: walking on', picture(2.5)), ('2 Cliff: at his mark', cliff_frame(2.0)),
             ('3 Close-up (wreck, fire later)', close_frame(3.5)), ('4 Gas station', gas_frame(4.0)),
             ('Props at real size', props_frame())]
    tw, th, pad = 352, 626, 8
    cols = 3
    rows = (len(tiles) + cols - 1) // cols
    sh = Image.new('RGB', (cols * tw + (cols + 1) * pad, rows * (th + 40) + (rows + 1) * pad), (226, 222, 214))
    for i, (lab, im) in enumerate(tiles):
        im = im.convert('RGB')
        ImageDraw.Draw(im).rectangle([60, 310, 900, 1500], outline=(255, 255, 255), width=4)
        t = Image.new('RGB', (tw, th + 40), (20, 20, 24))
        t.paste(im.resize((tw, th), Image.LANCZOS), (0, 40))
        ImageDraw.Draw(t).text((8, 8), lab, font=ImageFont.truetype(FONT, 20), fill=(255, 255, 255))
        sh.paste(t, (pad + (i % cols) * (tw + pad), pad + (i // cols) * (th + 40 + pad)))
    sh.save(out, quality=88)
    return out


def reel(out, secs=3.0):
    """A few seconds of each moving set, small: the fire, then the sea with the tanker sailing (rule: movement clips)."""
    import subprocess
    import tempfile
    tmp = tempfile.mkdtemp()
    n = 0
    fps = 12
    for k in range(int(secs * fps)):
        t = k / fps
        im = study_back(t)
        im.alpha_composite(study_desktop())
        im.alpha_composite(study_front())
        im.convert('RGB').resize((540, 960)).save(f'{tmp}/f{n:04d}.png')
        n += 1
    for k in range(int(secs * fps)):
        t = k / fps
        strait('wide', t, ('sail', near_x(t, 30.0))).convert('RGB').resize((540, 960)).save(f'{tmp}/f{n:04d}.png')
        n += 1
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', f'{tmp}/f%04d.png',
                    '-vf', 'fps=24', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '28', out], check=True)
    return out


if __name__ == '__main__':
    print({'sheet': sheet, 'reel': reel}[sys.argv[1]](sys.argv[2]))
