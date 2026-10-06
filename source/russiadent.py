#!/usr/bin/env python3
"""Russiadent Evil: the Kremlin's spokesman calmly says all is well while a zombie outbreak tears through his own
press conference behind the camera (prompts/russiadent-evil.md).

Same look as the rest of the TikTok parody series (burnham.py, mossad.py, patriots2.py): flat shapes, clean black
outlines, almond eyes with small pupils, soft shading, deadpan staging, hard cuts. Made vertical (1080 x 1920);
faces and text inside TikTok's safe area (x 60-900, y 310-1500).

Peskov is a caricature from a few features (grey hair brushed up and back, thin grey moustache, heavy-lidded sad
eyes, charcoal suit, dotted burgundy tie). Everyone else is invented. Russia is suggested only by colour (a plain
white-blue-red flag, a blue backdrop with a pale gold frame line); no emblems, no real outlets, no ministry logo.
The zombies evoke the genre, never Resident Evil itself (no Umbrella, no logos, no font, no music, no characters).
The researcher who died is never shown, named or joked about.

ONE PLAN for the press room (best-practice 1.3): every camera is a perspective camera placed in that plan, so the
180-degree reverse in shot 2 is the same room seen from the podium. Units: metres. X across the room (+X is screen
right when looking at the podium), Y up from the floor, Z from the podium (0) towards the back doors (+).

Usage:
    python3 russiadent.py stills OUT_DIR T1 T2 ...   frames at those times (seconds), full size
    python3 russiadent.py sheet OUT.jpg              the approval sheet (cast, both angles, the phone)
"""
import functools
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import burnham as B
import peepee as PP          # Rot, ctext, the series' caption
import mossad as M           # brows, mouths, tilted heads, hair styles (patched into burnham on import)
import figure as F
import kit
from ed import INK, curve, oval, soft

kit.install(B)

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 12
SR = 48000
TITLE = ('RUSSIADENT', 'EVIL')
UPM = 680.0                 # a person's own units per metre (burnham adult: about 1193 units, 1.75 m)

# ------------------------------------------------------------------------------------------- palette
WALL = (222, 214, 196)
WALL_D = (196, 186, 166)
PANEL = (120, 84, 58)          # the wooden dado round the room
PANEL_D = (92, 62, 42)
PARQUET = (164, 116, 74)
PARQUET_D = (136, 94, 58)
CEIL = (232, 228, 218)
BACKDROP = (28, 70, 168)
BACKDROP_L = (60, 112, 214)
FRAME_GOLD = (232, 204, 150)
PODIUM = (98, 64, 44)
PODIUM_L = (128, 88, 60)
STAGE = (70, 52, 44)
CHAIR = (46, 62, 120)          # dark blue folding chairs
CHAIR_FRAME = (150, 154, 160)
GLASS = (196, 222, 236)
NET = (240, 238, 232)
BLOOD = (196, 18, 30)
BLOOD_D = (128, 8, 18)
ZSKIN = (156, 172, 138)        # grey-green
ZSKIN_D = (118, 134, 104)
FLAG_W, FLAG_B, FLAG_R = (246, 246, 244), (28, 64, 168), (206, 30, 40)

# ------------------------------------------------------------------------------------------- the plan
ROOM = dict(x0=-5.4, x1=5.4, z0=-1.2, z1=8.8, h=3.9)
STAGE_BOX = dict(x0=-3.6, x1=3.6, z0=-1.2, z1=1.1, h=0.25)
PODIUM_BOX = dict(x=0.0, z0=0.22, z1=0.62, w=0.84, h=0.9)          # stands on the stage: top at 1.15 m
PESKOV_AT = (0.0, 0.0)                                               # behind the podium, on the stage
BACKDROP_BOX = dict(x0=-3.3, x1=3.3, y0=0.25, y1=3.7)
FLAG_AT = (0.56, -0.45)                                              # pole on the stage, beside the podium
ROWS_Z = [2.6, 3.6, 4.6, 5.6, 6.6]
SEATS_X = [-3.1, -2.4, -1.7, -1.0, 1.0, 1.7, 2.4, 3.1]               # centre aisle between -1.0 and 1.0
WINDOWS_Z = [3.0, 4.6, 6.2]                                          # down the left wall (X = -6), each 1.4 wide
SIDE_DOORS = dict(L=(7.3, 8.5), R=(6.8, 8.0))                       # Z extent of the door in each side wall
BACK_DOORS = (-0.95, 0.95)                                           # double doors in the back wall
RISERS = [(-4.0, -1.4), (1.4, 4.0)]                                  # camera platforms at the back, Z 7.6-8.6
TRIPODS = [(-3.3, 8.0), (-2.0, 8.0), (2.4, 8.0), (3.4, 8.1)]
CLOCK = (0.0, 3.3)                                                   # on the back wall above the doors (X, Y)
PLANT_AT = (4.9, 8.4)                                               # beside the right-hand door
CRATE_AT = (-5.3, 1.6)                                               # an empty water-bottle crate by the front wall


def check_plan():
    """Set pieces that must stay apart (best-practice 1.3): seats, podium, flag, tripods, plant, crate."""
    items = {'podium': (-PODIUM_BOX['w'] / 2, PODIUM_BOX['z0'], PODIUM_BOX['w'] / 2, PODIUM_BOX['z1']),
             'flag': (FLAG_AT[0] - 0.15, FLAG_AT[1] - 0.15, FLAG_AT[0] + 0.15, FLAG_AT[1] + 0.15),
             'plant': (PLANT_AT[0] - 0.25, PLANT_AT[1] - 0.25, PLANT_AT[0] + 0.25, PLANT_AT[1] + 0.25),
             'crate': (CRATE_AT[0] - 0.25, CRATE_AT[1] - 0.2, CRATE_AT[0] + 0.25, CRATE_AT[1] + 0.2)}
    for zi, z in enumerate(ROWS_Z):
        for xi, x in enumerate(SEATS_X):
            items[f'seat {zi}.{xi}'] = (x - 0.24, z - 0.22, x + 0.24, z + 0.22)
    for i, (x, z) in enumerate(TRIPODS):
        items[f'tripod {i}'] = (x - 0.3, z - 0.3, x + 0.3, z + 0.3)
    F.check_apart('the press room', {k: tuple(v * 100 for v in b) for k, b in items.items()})


check_plan()


class PCam:
    """A perspective camera in the plan: at (x, y, z), heading along +Z (dirz=1) or -Z (dirz=-1), turned by yaw
    (radians, + turns towards screen right), focal length f in pixels, (ox, oy) the screen point the optical axis
    passes through. Projects to world pixels (1080 x 1920 at zoom 1); a burnham Cam on top does the slow zoom."""
    def __init__(self, x, y, z, dirz, f, ox=540.0, oy=960.0, yaw=0.0):
        self.x, self.y, self.z, self.dirz, self.f, self.ox, self.oy = x, y, z, dirz, f, ox, oy
        h = (0.0 if dirz > 0 else math.pi) - yaw * dirz
        self.fw = (math.sin(h), math.cos(h))      # forward, in (X, Z)
        self.rt = (-math.cos(h), math.sin(h))     # screen right, in (X, Z)

    def depth(self, Z, X=None):
        X = self.x if X is None else X
        return (X - self.x) * self.fw[0] + (Z - self.z) * self.fw[1]

    def P(self, X, Y, Z):
        d = max(1e-3, self.depth(Z, X))
        r = (X - self.x) * self.rt[0] + (Z - self.z) * self.rt[1]
        return (self.ox + self.f * r / d, self.oy - self.f * (Y - self.y) / d)

    def scale(self, Z, X=None):
        """A person's scale (burnham units -> world pixels) at plan point (X, Z)."""
        return self.f / max(1e-3, self.depth(Z, X)) / UPM


NEAR = 0.25


def clipz(pc, pts3):
    """Clip a polygon (list of (X, Y, Z)) against the camera's near plane; returns screen points."""
    out = []
    n = len(pts3)
    for i in range(n):
        a, b = pts3[i], pts3[(i + 1) % n]
        da, db = pc.depth(a[2], a[0]) - NEAR, pc.depth(b[2], b[0]) - NEAR
        if da >= 0:
            out.append(a)
        if (da >= 0) != (db >= 0):
            u = da / (da - db)
            out.append(tuple(a[k] + (b[k] - a[k]) * u for k in range(3)))
    return [pc.P(*q) for q in out]


def quad(p, pc, pts3, fill, line=INK, lw=2.4):
    q = clipz(pc, pts3)
    if len(q) >= 3:
        p.poly(q, fill, line, lw)


def seg(p, pc, a, b, colr=INK, lw=2.4):
    q = clipz(pc, [a, b])
    if len(q) >= 2:
        p.line(q[:2], colr, lw)


# ------------------------------------------------------------------------------------------- the people
_face, _torso, _hair_back, _hair_front, _beard = B.face, B.torso, B.hair_back, B.hair_front, B.beard


def face(img, p, sp, t, hx, hy, hw, hh):
    br = sp.get('brows')
    mine = br in ('droop', 'terror')
    q = dict(sp, brows=None, brow_c=sp['skin']) if mine else sp
    fx = _face(img, p, q, t, hx, hy, hw, hh)
    bc, bw = sp.get('brow_c', (60, 44, 34)), sp.get('brow_w', 3.2)
    for sgn in (-1, 1):
        ex, ey = fx - 4 + sgn * 30, hy - 8
        if br == 'droop':   # Peskov: inner ends a touch up, outer ends sloping down: weary, unbothered
            p.line([(ex - sgn * 8, ey - 25), (ex + sgn * 6, ey - 24), (ex + sgn * 22, ey - 15)], bc, bw * 1.25)
        elif br == 'terror':  # true fear: wrenched up and together, the inner ends highest
            p.line([(ex - sgn * 10, ey - 44), (ex + sgn * 4, ey - 38), (ex + sgn * 22, ey - 26)], bc, bw * 1.15)
        if sp.get('hooded'):  # heavy upper lids folding over the outer corners, the eyes drooping outwards
            p.line([(ex + sgn * 4, ey - 12), (ex + sgn * 16, ey - 10), (ex + sgn * 24, ey - 1)], B.dk(sp['skin'], 0.8), 2.0)
            p.line([(ex - 12, ey + 13), (ex, ey + 17), (ex + 12, ey + 13)], B.dk(sp['skin'], 0.8), 1.8)
        if sp.get('milky') and not sp.get('blink'):  # a zombie: milky white eyes, a pale clouded pupil, red rims
            almond = [(ex - 18, ey), (ex - 8, ey - 9), (ex + 8, ey - 9), (ex + 18, ey), (ex + 8, ey + 8), (ex - 8, ey + 8)]
            p.poly(almond, (234, 236, 226), (150, 40, 44), 2.4)
            p.ell(ex, ey + 1, 6, 6, (206, 210, 200), None)
            p.line([(ex - 17, ey - 1), (ex - 8, ey - 9), (ex + 8, ey - 9), (ex + 17, ey - 1)], INK, 2.4)
        if sp.get('wide') and not sp.get('blink'):  # terror: stretched wide, white all round, a pinprick pupil
            eye = curve([(ex - 20, ey + 1), (ex - 10, ey - 16), (ex + 10, ey - 16), (ex + 20, ey + 1), (ex + 10, ey + 14),
                         (ex - 10, ey + 14)], 3)
            p.poly(eye, (253, 253, 252), INK, 2.4)
            jx, jy = 1.2 * math.sin(t * 31 + sgn), 1.2 * math.cos(t * 27)
            p.ell(ex + sp.get('look', 0) * 7 + jx, ey - 1 + jy, 2.6, 2.6, INK, None)
    if br == 'terror':  # the forehead creased hard, a crease between the brows, sweat at the temples
        sd = B.dk(sp['skin'], 0.8)
        for k in range(3):
            p.line([(fx - 30 + 4 * k, hy - 62 - 9 * k), (fx - 10, hy - 58 - 9 * k), (fx + 10, hy - 58 - 9 * k),
                    (fx + 30 - 4 * k, hy - 62 - 9 * k)], sd, 1.6)
        p.line([(fx - 6, hy - 50), (fx - 4, hy - 36)], sd, 1.6)
        p.line([(fx + 4, hy - 50), (fx + 2, hy - 36)], sd, 1.6)
        for sgn in (-1, 1):  # cheeks pulled down by the scream
            p.line([(fx + sgn * 30, hy + 34), (fx + sgn * 34, hy + 70)], sd, 1.6)
        for (dx, dy) in ((hw * 0.86, -40), (-hw * 0.9, -20)):
            dy += 6 * ((t * 3) % 1.0)
            p.poly(curve([(hx + dx, hy + dy - 12), (hx + dx + 6, hy + dy + 2), (hx + dx, hy + dy + 8), (hx + dx - 6, hy + dy + 2)], 3),
                   (200, 228, 246), INK, 1.4)
    if sp.get('jowls'):  # lines from the nose to past the mouth corners, and the soft jowls at the jaw
        sd = B.dk(sp['skin'], 0.78)
        for sgn in (-1, 1):
            p.line([(fx + sgn * 22, hy + 30), (fx + sgn * 36, hy + 56), (fx + sgn * 40, hy + 80)], sd, 2.0)
            p.line([(hx + sgn * hw * 0.78, hy + hh * 0.6), (hx + sgn * hw * 0.62, hy + hh * 0.86)], sd, 1.8)
    return fx


def hair_back(p, sp, hx, hy, hw, hh):
    st, c = sp.get('hair'), sp.get('hair_c', (60, 44, 34))
    if st == 'ponytail':  # a high ponytail swinging out behind the head
        sw = sp.get('tail_swing', 0.0)
        tip = (hx + hw + 40 + sw, hy + 150)
        p.poly(curve([(hx + hw * 0.2, hy - hh * 1.05), (hx + hw * 0.7, hy - hh * 1.1), (hx + hw + 30 + sw * 0.5, hy - 30),
                      tip, (hx + hw + 10 + sw * 0.6, hy + 40), (hx + hw * 0.5, hy - hh * 0.6)], 5), c, INK, 2.4)
        p.line([(hx + hw * 0.7, hy - hh * 0.9), (hx + hw + 22 + sw * 0.5, hy - 10), (tip[0] - 14, tip[1] - 30)],
               B.dk(c, 0.8), 1.6)
        return
    if st in ('peskov', 'zombie'):
        return
    return _hair_back(p, sp, hx, hy, hw, hh)


def hair_front(p, sp, hx, hy, hw, hh, fx):
    st = sp.get('hair')
    c = sp.get('hair_c', (60, 44, 34))
    cd, cl = B.dk(c, 0.74), B.lt(c, 1.12)
    if st == 'peskov':  # thick grey hair brushed up and straight back from a high forehead, full at the sides
        hair = [(hx - hw - 4, hy - 2), (hx - hw - 14, hy - 56), (hx - hw * 0.98, hy - hh * 0.98), (hx - hw * 0.55, hy - hh * 1.42),
                (hx + hw * 0.1, hy - hh * 1.56), (hx + hw * 0.72, hy - hh * 1.36), (hx + hw + 14, hy - hh * 0.86),
                (hx + hw + 6, hy - 2), (hx + hw * 0.9, hy - 46), (hx + hw * 0.62, hy - hh * 0.78), (fx + hw * 0.15, hy - hh * 0.86),
                (fx - hw * 0.35, hy - hh * 0.84), (hx - hw * 0.66, hy - hh * 0.76), (hx - hw * 0.9, hy - 46)]
        p.poly(curve(hair, 5), c, INK, 2.6)
        for k in range(6):  # combed strands sweeping up and back from the hairline
            x0 = hx - hw * 0.6 + k * hw * 0.24
            p.line([(x0, hy - hh * 0.84), (x0 + 4, hy - hh * 1.12), (x0 + 18, hy - hh * 1.38 + abs(k - 2.5) * 4)], cd, 1.8)
        p.line([(hx - hw * 0.4, hy - hh * 1.3), (hx + hw * 0.1, hy - hh * 1.46), (hx + hw * 0.5, hy - hh * 1.34)], cl, 3.4)
        for sgn in (-1, 1):  # the sides brushed back over the ears
            p.line([(hx + sgn * (hw - 4), hy - 10), (hx + sgn * (hw + 8), hy - 50), (hx + sgn * hw * 0.86, hy - hh * 0.9)], cd, 1.6)
        return
    if st == 'ponytail':  # pulled tight back from the face, no fringe, a few loose strands (shaken loose)
        hair = [(hx - hw - 4, hy - 6), (hx - hw - 6, hy - 52), (hx - hw * 0.72, hy - hh * 1.04), (hx, hy - hh * 1.18),
                (hx + hw * 0.72, hy - hh * 1.04), (hx + hw + 6, hy - 52), (hx + hw + 4, hy - 6), (hx + hw * 0.9, hy - 44),
                (hx + hw * 0.5, hy - hh * 0.8), (fx, hy - hh * 0.86), (hx - hw * 0.5, hy - hh * 0.8), (hx - hw * 0.9, hy - 44)]
        p.poly(curve(hair, 5), c, INK, 2.4)
        for k in range(4):
            x0 = hx - hw * 0.5 + k * hw * 0.33
            p.line([(x0, hy - hh * 0.84), (x0 * 0.6 + hx * 0.4 + hw * 0.3, hy - hh * 1.12)], cd, 1.5)
        if sp.get('loose'):
            p.line([(fx - 22, hy - hh * 0.86), (fx - 34, hy - hh * 0.4), (fx - 28, hy - 6)], c, 2.6)
            p.line([(fx + 30, hy - hh * 0.84), (fx + 44, hy - hh * 0.5)], c, 2.4)
        return
    if st == 'zombie':  # thin, matted, patchy hair
        for k in range(7):
            x0 = hx - hw * 0.8 + k * hw * 0.27
            p.line([(x0, hy - hh * 0.9 + abs(k - 3) * 6), (x0 + 6 * math.sin(k * 2.1), hy - hh * 0.5 + 10 * (k % 3))],
                   c, 4.0)
        return
    return _hair_front(p, sp, hx, hy, hw, hh, fx)


def beard(p, sp, hx, hy, hw, hh, fx):
    if sp.get('beard') != 'moustache':
        return _beard(p, sp, hx, hy, hw, hh, fx)
    c = sp.get('beard_c', (168, 162, 156))
    my = hy + sp.get('mouth_y', 60)
    # Peskov's: a thin, bristly grey moustache over the whole upper lip, the ends dipping a little at the corners
    pts = [(fx - 36, my - 2), (fx - 30, my - 12), (fx - 10, my - 19), (fx, my - 16), (fx + 10, my - 19), (fx + 30, my - 12),
           (fx + 36, my - 2), (fx + 26, my - 5), (fx, my - 7), (fx - 26, my - 5)]
    p.poly(curve(pts, 4), c, INK, 1.8)
    for k in range(9):
        x = fx - 28 + 7 * k
        p.line([(x, my - 14 + abs(k - 4) * 0.8), (x + 1, my - 7)], B.dk(c, 0.8), 1.2)


def torso(img, p, sp, t):
    _torso(img, p, sp, t)
    sw, bottom = sp.get('shoulders', 150), sp.get('bottom', 560)
    if sp.get('tie_dots'):  # small pale dots on the tie
        for k, (x, y) in enumerate([(-6, 40), (6, 66), (-7, 96), (6, 124), (-5, 152), (5, 178)]):
            p.ell(x, y, 2.6, 2.6, B.lt(sp['tie'], 1.7), None)
    if sp.get('torn'):  # ripped clothes: dark tears, a ragged hem
        rng = np.random.default_rng(sp.get('seed', 3))
        for _ in range(4):
            x, y = rng.uniform(-sw * 0.8, sw * 0.8), rng.uniform(150, bottom - 60)
            r = rng.uniform(18, 34)
            pts = [(x + r * math.cos(a) * rng.uniform(0.4, 1.0), y + r * 1.3 * math.sin(a) * rng.uniform(0.4, 1.0))
                   for a in np.linspace(0, 2 * math.pi, 9, endpoint=False)]
            p.poly(pts, sp.get('tear_c', ZSKIN_D), INK, 1.8)
        hem = [(-sw + 6, bottom - 4)]
        for k in range(10):
            hem.append((-sw + 6 + (2 * sw - 12) * (k + 0.5) / 10, bottom + (26 if k % 2 else -4)))
        hem.append((sw - 6, bottom - 4))
        p.poly(hem + [(sw - 6, bottom - 20), (-sw + 6, bottom - 20)], sp.get('jacket', B.NAVY), INK, 1.8)
    if sp.get('press'):  # a generic press lanyard: plain strap, a white card with a coloured band and a grey photo
        lc = sp.get('lanyard_c', (40, 120, 200))
        sx = sp.get('lanyard_swing', 0.0)
        p.line([(-30, 0), (-14 + sx, 196)], lc, 6)
        p.line([(30, 0), (14 + sx, 196)], lc, 6)
        p.poly([(-32 + sx, 194), (32 + sx, 194), (32 + sx, 276), (-32 + sx, 276)], (248, 248, 246), INK, 2.0)
        p.poly([(-32 + sx, 194), (32 + sx, 194), (32 + sx, 210), (-32 + sx, 210)], lc, None)
        p.poly([(-24 + sx, 218), (-4 + sx, 218), (-4 + sx, 244), (-24 + sx, 244)], (190, 190, 196), None)
        p.line([(2 + sx, 224), (24 + sx, 224)], (150, 150, 160), 2.4)
        p.line([(2 + sx, 236), (18 + sx, 236)], (150, 150, 160), 2.4)
        p.ell(sx, 264, 6, 6, (80, 80, 90), None)
    for (x, y, r, seed) in sp.get('splats', ()):  # blood on the clothes
        splat(p, x, y, r, seed)


_mouth = B.mouth


def mouth(p, sp, t, fx, my):
    m = sp.get('mouth', 'line')
    if m == 'scream':  # terror: stretched wide and tall, corners dragged down, both rows of teeth, the tongue
        k = 1.0 + 0.08 * math.sin(t * 23 + sp.get('seed', 0))
        pts = curve([(fx - 28, my + 4), (fx - 14, my - 8), (fx + 14, my - 8), (fx + 28, my + 4), (fx + 30, my + 30 * k),
                     (fx + 18, my + 46 * k), (fx - 18, my + 46 * k), (fx - 30, my + 30 * k)], 4)
        p.poly(pts, (62, 16, 24), INK, 2.6)
        p.poly([(fx - 16, my - 6), (fx + 16, my - 6), (fx + 18, my + 2), (fx - 18, my + 2)], (246, 244, 238), None)
        p.poly([(fx - 15, my + 40 * k), (fx + 15, my + 40 * k), (fx + 14, my + 45 * k), (fx - 14, my + 45 * k)], (236, 232, 222), None)
        p.ell(fx, my + 34 * k, 11, 6, (184, 80, 88), None)
        return
    if m == 'gasp':  # a frozen, open gasp
        p.poly(curve([(fx - 14, my), (fx, my - 6), (fx + 14, my), (fx + 12, my + 26), (fx, my + 32), (fx - 12, my + 26)], 4),
               (62, 16, 24), INK, 2.4)
        p.poly([(fx - 10, my - 2), (fx + 10, my - 2), (fx + 9, my + 3), (fx - 9, my + 3)], (246, 244, 238), None)
        return
    if m == 'snarl':  # a zombie: wide, square, both rows of teeth bared
        p.poly([(fx - 30, my - 6), (fx + 30, my - 8), (fx + 26, my + 22), (fx - 26, my + 24)], (60, 18, 24), INK, 2.6)
        p.poly([(fx - 26, my - 4), (fx + 26, my - 6), (fx + 24, my + 3), (fx - 24, my + 5)], (226, 222, 196), None)
        p.poly([(fx - 22, my + 16), (fx + 22, my + 14), (fx + 22, my + 21), (fx - 22, my + 23)], (226, 222, 196), None)
        for k in range(-2, 3):
            p.line([(fx + k * 10, my - 6), (fx + k * 10, my + 3)], (150, 140, 110), 1.2)
        return
    _mouth(p, sp, t, fx, my)


B.face, B.hair_front, B.beard, B.torso = face, hair_front, beard, torso
B.mouth = mouth
B.hair_back = M.tilted(hair_back)


def splat(p, x, y, r, seed=0, colr=BLOOD, drops=5):
    """Flat cartoon blood: an irregular blob and a few round drops flung out. No anatomy, no realism."""
    rng = np.random.default_rng(seed)
    n = 14
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        rr = r * (rng.uniform(0.62, 1.0) if k % 2 else rng.uniform(1.0, 1.45))
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    p.poly(curve(pts, 3), colr, B.dk(colr, 0.6), 1.4)
    for _ in range(drops):
        a, d = rng.uniform(0, 2 * math.pi), rng.uniform(1.5, 2.6) * r
        rd = rng.uniform(0.12, 0.28) * r
        p.ell(x + d * math.cos(a), y + d * math.sin(a), rd, rd, colr, None)


def legs_draw(img, p, sp, kind, phase=0.0):
    """Everyone has legs and feet (figure-rig.md). kind: stand, run, kneel, lunge."""
    tc = sp.get('trousers', sp.get('jacket', B.NAVY))
    shoe = sp.get('shoe', (22, 20, 22))
    if sp.get('skirt'):
        tc = sp['tights']
    if kind == 'stand':
        o = sp.get('stance', 0)
        for sgn in (-1, 1):
            p.poly([(sgn * 6, 440), (sgn * 104, 440), (sgn * (100 + o * 0.6), 700), (sgn * (90 + o), 900), (sgn * (30 + o), 902),
                    (sgn * (18 + o * 0.6), 700)], tc, INK, 2.6)
            p.poly(curve([(sgn * (24 + o), 896), (sgn * (94 + o), 894), (sgn * (128 + o), 910), (sgn * (124 + o), 928),
                          (sgn * (20 + o), 928)], 4), shoe, INK, 2.4)
    elif kind in ('run', 'lunge'):
        stride = 70 if kind == 'run' else 40
        for k, sgn in enumerate((-1, 1)):
            sw = stride * math.sin(phase + k * math.pi)
            lift = max(0.0, 40 * math.sin(phase + k * math.pi + 1.2)) if kind == 'run' else 0.0
            knee = (sgn * 60 + sw * 0.7, 690 - lift * 0.6)
            foot = (sgn * 60 + sw, 900 - lift)
            p.poly([(sgn * 8, 440), (sgn * 104, 440), (knee[0] + sgn * 42, knee[1]), (foot[0] + 30, foot[1]),
                    (foot[0] - 30, foot[1]), (knee[0] - sgn * 42, knee[1])], tc, INK, 2.6)
            p.poly(curve([(foot[0] - 36, foot[1] - 4), (foot[0] + 34, foot[1] - 6), (foot[0] + 64, foot[1] + 10),
                          (foot[0] + 60, foot[1] + 28), (foot[0] - 38, foot[1] + 28)], 4), shoe, INK, 2.4)
    elif kind == 'kneel':  # knees on the floor (y 720), shins going back, the toes showing behind
        for sgn in (-1, 1):
            p.poly(curve([(sgn * 120, 690), (sgn * 150, 720), (sgn * 120, 740), (sgn * 60, 740)], 3), shoe, INK, 2.2)
            p.poly([(sgn * 8, 440), (sgn * 108, 440), (sgn * 118, 700), (sgn * 30, 712)], tc, INK, 2.6)
            p.ell(sgn * 74, 708, 46, 26, tc, INK, 2.4)
    if sp.get('skirt'):
        p.poly([(-sp.get('shoulders', 140) + 4, 380), (sp.get('shoulders', 140) - 4, 380), (124, 600 if kind != 'kneel' else 640),
                (-124, 600 if kind != 'kneel' else 640)], sp['skirt'], INK, 2.6)


def zombie_reach(rig):
    """The classic zombie reach, straight at the camera: seen end-on the arms are very short, so this is a named
    break of the arm guard (figure-rig.md, 'Breaking a rule on purpose')."""
    with F.allow('zombie arms reaching straight at the camera, seen end-on'):
        return {'L': rig.arm('L', (-150, 20), 'palm', 'depth', depth=0.6),
                'R': rig.arm('R', (156, 6), 'palm', 'depth', depth=0.6)}


def person(img, cam, x, y, s, sp, t=0.0, legs='stand', phase=0.0, tilt=0.0, flip=1):
    """Draw one person, neck base at world (x, y), scale s, leaning by tilt (radians, about the hips)."""
    if sp.get('reach_cam'):
        with F.allow('zombie arms reaching straight at the camera, seen end-on'):
            return _person(img, cam, x, y, s, dict(sp, reach_cam=False), t, legs, phase, tilt, flip)
    return _person(img, cam, x, y, s, sp, t, legs, phase, tilt, flip)


def _person(img, cam, x, y, s, sp, t=0.0, legs='stand', phase=0.0, tilt=0.0, flip=1):
    L = B.Local(cam, x, y, s, flip)
    R = PP.Rot(L, tilt, pivot=(0, 440)) if tilt else L
    p = B.Pen(img, R)
    hx, hy = sp.get('head_dx', 0.0), -150 + sp.get('head_dy', 0.0)
    B.hair_back(p, sp, hx, hy, sp.get('hw', 72), sp.get('hh', 88))
    legs_draw(img, p, sp, legs, phase)
    B.arms(img, p, sp, t, front=False)
    B.torso(img, p, sp, t)
    B.arms(img, p, sp, t, front=True)
    B.head(img, p, sp, t, hx, hy)
    for (sx, sy, r, seed) in sp.get('face_splats', ()):
        splat(p, sx, sy, r, seed, drops=2)
    return p


def person_back(img, cam, x, y, s, sp, t=0.0, legs='stand', phase=0.0, tilt=0.0):
    """The same person seen from behind (running away, pulling at a door): no face, the hair covering the head."""
    L = B.Local(cam, x, y, s)
    R = PP.Rot(L, tilt, pivot=(0, 440)) if tilt else L
    p = B.Pen(img, R)
    sw, bottom = sp.get('shoulders', 150), sp.get('bottom', 560)
    legs_draw(img, p, dict(sp, skirt=None) if sp.get('skirt') else sp, legs, phase)
    jc = sp.get('jacket', B.NAVY)
    p.poly([(-32, -80), (32, -80), (36, 10), (-36, 10)], sp['skin'], INK, 2.6)
    body = [(-40, -4), (-sw * 0.8, 12), (-sw, 50), (-sw - 6, 200), (-sw + 6, bottom), (sw - 6, bottom), (sw + 6, 200),
            (sw, 50), (sw * 0.8, 12), (40, -4)]
    p.poly(body, jc, INK, 2.6)
    if sp.get('outfit') == 'suit':
        p.poly([(-40, -6), (40, -6), (34, 14), (-34, 14)], sp.get('shirt', (236, 238, 244)), INK, 2.0)
        p.line([(0, 200), (0, bottom)], B.dk(jc, 0.75), 2.0)
    if sp.get('skirt'):
        p.poly([(-sw + 4, 380), (sw - 4, 380), (124, 600), (-124, 600)], sp['skirt'], INK, 2.6)
    if sp.get('press'):
        p.line([(-30, 0), (-34, -40)], sp.get('lanyard_c', (40, 120, 200)), 6)
        p.line([(30, 0), (34, -40)], sp.get('lanyard_c', (40, 120, 200)), 6)
    B.arms(img, p, sp, t, front=True)
    hx, hy, hw, hh = 0.0, -150.0, sp.get('hw', 72), sp.get('hh', 88)
    for sgn in (-1, 1):
        p.poly(oval(hx + sgn * (hw + 2), hy + 6, 12, 22), sp['skin'], INK, 2.4)
    p.poly(B.head_outline(hx, hy, hw, hh, sp.get('jaw', 'square')), sp['skin'], INK, 2.6)
    c = sp.get('hair_c', (60, 44, 34))
    st = sp.get('hair')
    if st == 'bald':
        p.poly(curve([(hx - hw, hy + 20), (hx - hw - 4, hy - 40), (hx, hy - 30), (hx + hw + 4, hy - 40), (hx + hw, hy + 20),
                      (hx, hy + 40)], 4), c, INK, 2.2)
    else:
        low = {'long': 200, 'wavy': 220, 'bob': 110, 'blonde': 240}.get(st, 46)
        p.poly(curve([(hx - hw - 6, hy + low), (hx - hw - 10, hy - 40), (hx - hw * 0.7, hy - hh * 1.08), (hx, hy - hh * 1.18),
                      (hx + hw * 0.7, hy - hh * 1.08), (hx + hw + 10, hy - 40), (hx + hw + 6, hy + low), (hx, hy + low + 12)], 5),
               c, INK, 2.6)
        for k in range(4):
            p.line([(hx - 30 + 20 * k, hy - hh * 0.9), (hx - 34 + 22 * k, hy + low * 0.6)], B.dk(c, 0.8), 1.6)
    return p


# The cast. Caricature from a few features only.
PESKOV = dict(name='Peskov', skin=(236, 190, 170), hw=78, hh=98, jaw='soft', hair='peskov', hair_c=(184, 180, 176),
              beard='moustache', beard_c=(170, 164, 158), brows='droop', brow_c=(150, 144, 140), brow_w=3.4, lid=6, hooded=True, jowls=True,
              age=True, nose='long', mouth='set', outfit='suit', jacket=(64, 66, 74), shirt=(244, 244, 246),
              tie=(122, 30, 54), tie_dots=True, trousers=(58, 60, 68), shoulders=162, bottom=600, full=True, pose='custom')
REPORTER = dict(name='the reporter', skin=(242, 226, 220), hw=64, hh=86, jaw='soft', hair='ponytail', hair_c=(236, 204, 124),
                brow_c=(176, 146, 92), brow_w=2.8, lashes=True, outfit='jumper', jacket=(240, 230, 206), skirt=(96, 98, 108),
                tights=(214, 196, 186), shoe=(40, 36, 40), shoulders=132, bottom=430, full=True, pose='custom', press=True,
                lanyard_c=(46, 150, 120), loose=True)
ZOMBIE = dict(name='a zombie', skin=ZSKIN, hw=70, hh=90, jaw='square', hair='zombie', hair_c=(70, 66, 60), milky=True,
              brows='fierce', brow_c=(80, 84, 70), harrow=0.9, mouth='snarl', outfit='suit', jacket=(80, 84, 96),
              shirt=(206, 204, 190), tie=(70, 74, 110), trousers=(60, 62, 72), torn=True, seed=4, shoulders=150,
              full=True, pose='custom', press=True, lanyard_c=(206, 120, 40),
              splats=[(-40, 90, 16, 1), (60, 160, 22, 2), (-90, 330, 14, 3)], face_splats=[(30, -95, 7, 4)])


def mic(p, base, top, flag_c, flag_t=None):
    """A gooseneck microphone on a stand with a plain coloured cube flag (no outlet's name)."""
    p.line([base, ((base[0] + top[0]) / 2 + 8, (base[1] + top[1]) / 2), top], (40, 40, 44), 5)
    p.ell(top[0], top[1] - 10, 13, 18, (36, 36, 40), INK, 1.8)
    fx, fy = top[0], top[1] + 34
    p.poly([(fx - 22, fy - 18), (fx + 22, fy - 18), (fx + 22, fy + 18), (fx - 22, fy + 18)], flag_c, INK, 2.0)
    p.poly([(fx + 22, fy - 18), (fx + 30, fy - 24), (fx + 30, fy + 12), (fx + 22, fy + 18)], B.dk(flag_c, 0.75), INK, 1.8)
    if flag_t:  # a plain white stripe or ring
        p.line([(fx - 22, fy), (fx + 22, fy)], flag_t, 5)


# ------------------------------------------------------------------------------------------- the room
def room(img, cam, pc, t=0.0, chaos=False):
    """The press room from any camera in the plan: walls, windows, doors, floor, stage, backdrop, chairs, tripods."""
    p = B.Pen(img, cam)
    W3 = lambda X, Y, Z: pc.P(X, Y, Z)
    x0, x1, z0, z1, h = ROOM['x0'], ROOM['x1'], ROOM['z0'], ROOM['z1'], ROOM['h']
    # floor, ceiling, walls (far to near is automatic: they don't overlap)
    quad(p, pc, [(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)], PARQUET, None)
    for k in range(-12, 13):  # floorboards running towards the stage
        seg(p, pc, (k * 0.5, 0, z0), (k * 0.5, 0, z1), PARQUET_D, 1.4)
    quad(p, pc, [(x0, h, z0), (x1, h, z0), (x1, h, z1), (x0, h, z1)], CEIL, None)
    for z in (1.0, 4.0, 7.0, 10.0):  # ceiling lights
        for x in (-3.0, 0.0, 3.0):
            quad(p, pc, [(x - 0.5, h - 0.01, z - 0.3), (x + 0.5, h - 0.01, z - 0.3), (x + 0.5, h - 0.01, z + 0.3),
                         (x - 0.5, h - 0.01, z + 0.3)], (252, 250, 236), (200, 196, 186), 1.4)
    if pc.dirz > 0:   # looking at the back wall
        quad(p, pc, [(x0, 0, z1), (x1, 0, z1), (x1, h, z1), (x0, h, z1)], WALL, None)
        quad(p, pc, [(x0, 0, z1), (x1, 0, z1), (x1, 1.0, z1), (x0, 1.0, z1)], PANEL, INK, 2.0)
        bx0, bx1 = BACK_DOORS
        quad(p, pc, [(bx0 - 0.12, 0, z1), (bx1 + 0.12, 0, z1), (bx1 + 0.12, 2.52, z1), (bx0 - 0.12, 2.52, z1)], PANEL_D, INK, 2.4)
        if chaos:   # burst open: the leaves swung back against the wall, the corridor beyond full of them
            gap = [(bx0, 0, z1), (bx1, 0, z1), (bx1, 2.4, z1), (bx0, 2.4, z1)]
            quad(p, pc, gap, (34, 30, 34), INK, 2.2)
            outside(img, cam, pc, gap, [(-0.7 + 0.45 * (j % 4), z1 + 0.5 + 0.55 * (j // 4) + 0.15 * (j % 2), 50 + j)
                                        for j in range(12)], t)
            for a, sgn in ((bx0, -1), (bx1, 1)):
                quad(p, pc, [(a, 0, z1), (a + sgn * 0.12, 0, z1 - 0.9), (a + sgn * 0.12, 2.4, z1 - 0.9), (a, 2.4, z1)], PODIUM_L, INK, 2.2)
        else:
            for a, b in ((bx0, 0.0), (0.0, bx1)):
                quad(p, pc, [(a + 0.03, 0, z1), (b - 0.03, 0, z1), (b - 0.03, 2.4, z1), (a + 0.03, 2.4, z1)], PODIUM_L, INK, 2.2)
                quad(p, pc, [(a + 0.18, 1.3, z1), (b - 0.18, 1.3, z1), (b - 0.18, 2.2, z1), (a + 0.18, 2.2, z1)], GLASS, INK, 1.6)
        cx, cy = W3(CLOCK[0], CLOCK[1], z1)
        r = pc.f * 0.25 / pc.depth(z1, CLOCK[0])
        p.ell(cx, cy, r, r, (250, 250, 246), INK, 2.4)
        p.line([(cx, cy), (cx, cy - r * 0.7)], INK, 2.2)
        p.line([(cx, cy), (cx + r * 0.5, cy + r * 0.2)], INK, 2.2)
    else:             # looking at the front wall: the backdrop
        quad(p, pc, [(x0, 0, z0), (x1, 0, z0), (x1, h, z0), (x0, h, z0)], WALL, None)
        quad(p, pc, [(x0, 0, z0), (x1, 0, z0), (x1, 1.0, z0), (x0, 1.0, z0)], PANEL, INK, 2.0)
        bd = BACKDROP_BOX
        q = clipz(pc, [(bd['x0'], bd['y0'], z0 + 0.02), (bd['x1'], bd['y0'], z0 + 0.02), (bd['x1'], bd['y1'], z0 + 0.02),
                       (bd['x0'], bd['y1'], z0 + 0.02)])
        p.poly(q, BACKDROP, INK, 2.4)
        X0, Y0 = cam.P(*q[0])
        X1, Y1 = cam.P(*q[2])
        cxy = W3(0.0, 1.9, z0)
        B.gradient(img, cam, (min(q[0][0], q[2][0]), min(q[0][1], q[2][1]), max(q[0][0], q[2][0]), max(q[0][1], q[2][1])),
                   BACKDROP_L, BACKDROP, cxy, pc.f * 2.4 / pc.depth(z0), squash=0.8)
        for (fx0, fx1, fy0, fy1) in ((-0.62, 0.62, 1.2, 2.75), (-3.0, -1.0, 0.9, 3.4), (1.0, 3.0, 0.9, 3.4)):
            r = [(fx0, fy0, z0 + 0.02), (fx1, fy0, z0 + 0.02), (fx1, fy1, z0 + 0.02), (fx0, fy1, z0 + 0.02)]
            qq = clipz(pc, r)
            p.line(qq + [qq[0]], FRAME_GOLD, 12)
            # soft diagonal light bands, as on a broadcast backdrop
        for k in (-1, 1):
            a, b = W3(k * 0.4, 3.7, z0), W3(k * 2.4, 0.25, z0)
            p.line([a, b], B.lt(BACKDROP, 1.18), 3)
    for side, X in (('L', x0), ('R', x1)):  # the side walls
        quad(p, pc, [(X, 0, z0), (X, 0, z1), (X, h, z1), (X, h, z0)], WALL_D if pc.dirz > 0 else WALL_D, INK, 2.0)
        quad(p, pc, [(X, 0, z0), (X, 0, z1), (X, 1.0, z1), (X, 1.0, z0)], PANEL, INK, 2.0)
        za, zb = SIDE_DOORS[side]
        quad(p, pc, [(X, 0, za - 0.1), (X, 0, zb + 0.1), (X, 2.5, zb + 0.1), (X, 2.5, za - 0.1)], PANEL_D, INK, 2.2)
        if chaos and side == 'L':   # burst open: the corridor beyond packed with them
            gap = [(X, 0, za), (X, 0, zb), (X, 2.4, zb), (X, 2.4, za)]
            quad(p, pc, gap, (34, 30, 34), INK, 2.2)
            outside(img, cam, pc, gap, through(pc, X, (za + zb) / 2, zb - za, 90), t)
        else:
            quad(p, pc, [(X, 0, za), (X, 0, zb), (X, 2.4, zb), (X, 2.4, za)], PODIUM_L, INK, 2.2)
            quad(p, pc, [(X, 1.45, za + 0.25), (X, 1.45, zb - 0.25), (X, 2.1, zb - 0.25), (X, 2.1, za + 0.25)], GLASS, INK, 1.6)
            if chaos:   # zombie faces pressed to the door's little window
                outside(img, cam, pc, [(X, 1.45, za + 0.25), (X, 1.45, zb - 0.25), (X, 2.1, zb - 0.25), (X, 2.1, za + 0.25)],
                        [(X + (-0.4 if X < 0 else 0.4), (za + zb) / 2 + d, 30 + j) for j, d in enumerate((-0.2, 0.2))], t)
        if side == 'L':
            for i, zw in enumerate(WINDOWS_Z):
                pane = [(X, 0.55, zw - 0.7), (X, 0.55, zw + 0.7), (X, 3.1, zw + 0.7), (X, 3.1, zw - 0.7)]
                quad(p, pc, pane, (206, 226, 236), INK, 2.4)
                if chaos:   # the tide outside, several deep, pressed against the glass
                    outside(img, cam, pc, pane, through(pc, X, zw, 1.4, 40 + 9 * i), t)
                    glass_hands(img, cam, pc, X, zw, 60 + i, t)
                quad(p, pc, [(X, 2.7, zw - 0.7), (X, 2.7, zw + 0.7), (X, 3.1, zw + 0.7), (X, 3.1, zw - 0.7)], NET, INK, 1.6)
                for k in range(1, 6):  # net-curtain folds
                    seg(p, pc, (X, 2.7, zw - 0.7 + k * 0.233), (X, 3.1, zw - 0.7 + k * 0.233), (214, 212, 204), 1.6)
                quad(p, pc, pane, None, INK, 2.4)
                seg(p, pc, (X, 3.1, zw), (X, 0.55, zw), INK, 2.0)
                seg(p, pc, (X, 2.2, zw - 0.7), (X, 2.2, zw + 0.7), INK, 2.0)
    # the stage (a low platform at the front)
    st = STAGE_BOX
    quad(p, pc, [(st['x0'], st['h'], st['z0']), (st['x1'], st['h'], st['z0']), (st['x1'], st['h'], st['z1']),
                 (st['x0'], st['h'], st['z1'])], STAGE, INK, 2.0)
    quad(p, pc, [(st['x0'], 0, st['z1']), (st['x1'], 0, st['z1']), (st['x1'], st['h'], st['z1']), (st['x0'], st['h'], st['z1'])],
         B.dk(STAGE, 0.8), INK, 2.0)


def outside(img, cam, pc, opening, crowd, t):
    """Zombies beyond an opening (a window, a doorway), seen only through it: drawn on their own layer and masked
    by the opening. crowd: [(X, Z, seed)] in the plan, beyond the wall."""
    q = clipz(pc, opening)
    if len(q) < 3:
        return
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    for X, Z, seed in sorted(crowd, key=lambda c: -pc.depth(c[1], c[0])):
        sp = zombie_base(seed, press=(seed % 2 == 0))
        rig = F.Rig(sp)
        sway = 20 * math.sin(t * 5 + seed)
        sp['arms'] = {'L': rig.arm('L', (-190, -170 + sway), 'palm', 'out', strict=False),
                      'R': rig.arm('R', (200, -150 - sway), 'palm', 'out', strict=False)}
        sc = pc.scale(Z, X)
        nx, ny = pc.P(X, F.SOLE_Y / UPM, Z)
        person(lay, cam, nx, ny, sc, sp, t, tilt=0.05 * math.sin(t * 3 + seed))
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).polygon([cam.P(*pt) for pt in q], fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay.getchannel('A')), np.asarray(mask))))
    img.alpha_composite(lay)


def through(pc, X, zc, width, seed, n=9):
    """Places beyond a side-wall opening (centred at zc, `width` wide) that the camera actually sees through it: each
    one on the line of sight through a point of the opening, 0.3-1.4 m beyond the wall, in rows."""
    out = []
    for j in range(n):
        u = (j % 3 - 1) * width * 0.3 + 0.08 * (j // 3)      # across the opening
        dx = 0.3 + 0.45 * (j // 3)                            # how far beyond the wall
        zo = zc + u
        k = (zo - pc.z) / (X - pc.x)                          # the line of sight's slope in the plan
        Xb = X - dx if X < 0 else X + dx
        out.append((Xb, zo + k * (Xb - X), seed + j))
    return out


def glass_hands(img, cam, pc, X, zw, seed, t):
    """Grey-green hands pressed flat on a window pane (palms and spread fingers), smearing it."""
    rng = np.random.default_rng(seed)
    p = B.Pen(img, cam)
    for _ in range(7):
        Z, Y = zw + rng.uniform(-0.6, 0.6), rng.uniform(0.9, 2.1) + 0.02 * math.sin(t * 6 + seed)
        cx, cy = pc.P(X + 0.01, Y, Z)
        k = pc.f / pc.depth(Z, X) * 0.05
        sq = 0.55     # seen at an angle on the side wall
        colr = [ZSKIN, (148, 166, 140), (162, 172, 132)][rng.integers(3)]
        for j in range(4):
            a = -2.2 + 0.35 * j
            p.line([(cx, cy), (cx + math.cos(a) * 1.6 * k * sq, cy + math.sin(a) * 1.6 * k)], INK, 7.0)
            p.line([(cx, cy), (cx + math.cos(a) * 1.6 * k * sq, cy + math.sin(a) * 1.6 * k)], colr, 4.6)
        p.ell(cx, cy, k * sq, k * 0.9, colr, INK, 1.6)
        if rng.random() < 0.5:
            p.line([(cx, cy + k), (cx + rng.uniform(-2, 2), cy + 2.4 * k)], B.dk(BLOOD, 0.9), 2.2)


def floor_splat(img, cam, pc, X, Z, r, seed):
    """A flat red pool on the floor, squashed by the camera's view of the floor."""
    sx, sy = pc.P(X, 0.0, Z)
    k = pc.f / max(0.3, pc.depth(Z, X))
    squash = max(0.12, min(0.45, 0.8 * abs(pc.y) / max(0.3, pc.depth(Z, X))))
    lay = PP.Rot(cam, 0.0) if False else cam

    class Squash:
        def __init__(self, c):
            self.c, self.s = c, c.s

        def P(self, x, y):
            return self.c.P(sx + (x - sx), sy + (y - sy) * squash)

        def S(self, v):
            return self.c.S(v)
    splat(B.Pen(img, Squash(cam)), sx, sy, r * k, seed, drops=4)


def chair(img, cam, pc, X, Z, over=0.0, facing=-1):
    """A folding chair at plan (X, Z), facing the podium (-Z). over: knocked over sideways (0-1)."""
    p = B.Pen(img, cam)
    s = pc.f / max(0.3, pc.depth(Z, X))
    sx, sy = pc.P(X, 0, Z)
    kit.contact_shadow(img, cam, sx, sy, 0.5 * s, alpha=0.22)
    ang = over * 1.45 * (1 if X > 0 else -1)
    ca, sa = math.cos(ang), math.sin(ang)

    def P(u, v):  # chair-local: u across (m), v up (m), rotated about the foot on the floor
        return (sx + (u * ca - v * sa) * s, sy - (u * sa + v * ca) * s)
    back_far = (pc.dirz < 0) == (facing < 0)   # seen from behind (front cam) or from the front (reverse cam)
    seat = [P(-0.22, 0.44), P(0.22, 0.44), P(0.22, 0.48), P(-0.22, 0.48)]
    for u in (-0.2, 0.2):
        p.line([P(u, 0.0), P(u * 0.9, 0.46)], CHAIR_FRAME, 2.6)
    backrest = [P(-0.21, 0.62), P(0.21, 0.62), P(0.2, 0.9), P(-0.2, 0.9)]
    if back_far:
        p.poly(backrest, CHAIR, INK, 2.0)
        p.poly(seat, B.lt(CHAIR, 1.2), INK, 2.0)
    else:
        p.poly(seat, B.lt(CHAIR, 1.2), INK, 2.0)
        p.poly(backrest, CHAIR, INK, 2.0)
    for u in (-0.2, 0.2):
        p.line([P(u, 0.46), P(u, 0.9)], CHAIR_FRAME, 2.4)


def tripod(img, cam, pc, X, Z, y0=0.3):
    p = B.Pen(img, cam)
    top = pc.P(X, y0 + 1.45, Z)
    for dx in (-0.35, 0.0, 0.35):
        a = pc.P(X + dx, y0, Z + (0.25 if dx == 0 else -0.15))
        p.line([top, a], (40, 40, 44), 3.0)
    s = pc.f / pc.depth(Z, X)
    cx, cy = top
    p.poly([(cx - 0.18 * s, cy - 0.28 * s), (cx + 0.18 * s, cy - 0.28 * s), (cx + 0.18 * s, cy), (cx - 0.18 * s, cy)],
           (34, 34, 38), INK, 2.0)
    p.ell(cx, cy - 0.14 * s, 0.07 * s, 0.07 * s, (90, 110, 140), INK, 1.6)
    p.poly([(cx + 0.18 * s, cy - 0.24 * s), (cx + 0.28 * s, cy - 0.2 * s), (cx + 0.28 * s, cy - 0.04 * s), (cx + 0.18 * s, cy)],
           (50, 50, 56), INK, 1.6)


def risers(img, cam, pc):
    p = B.Pen(img, cam)
    for a, b in RISERS:
        quad(p, pc, [(a, 0.3, 7.6), (b, 0.3, 7.6), (b, 0.3, 8.6), (a, 0.3, 8.6)], (60, 60, 66), INK, 2.0)
        quad(p, pc, [(a, 0, 7.6), (b, 0, 7.6), (b, 0.3, 7.6), (a, 0.3, 7.6)], (44, 44, 50), INK, 2.0)


def flag(img, cam, pc, t=0.0):
    """A plain white-blue-red flag on a pole, folds hanging, a gold tip. No emblem."""
    p = B.Pen(img, cam)
    X, Z = FLAG_AT
    s = pc.f / pc.depth(Z)
    base, top = pc.P(X, STAGE_BOX['h'], Z), pc.P(X, 2.75, Z)
    kit.contact_shadow(img, cam, base[0], base[1], 0.35 * s, alpha=0.3)
    p.poly([(base[0] - 0.16 * s, base[1]), (base[0] + 0.16 * s, base[1]), (base[0] + 0.06 * s, base[1] - 0.06 * s),
            (base[0] - 0.06 * s, base[1] - 0.06 * s)], (60, 52, 40), INK, 1.8)
    p.line([base, top], (176, 140, 70), 5)
    p.ell(top[0], top[1] - 0.04 * s, 0.035 * s, 0.05 * s, (232, 196, 90), INK, 1.4)
    fx, fy = top[0], top[1] + 0.06 * s
    w, hh = 0.26 * s, 1.35 * s          # hanging: the stripes run down the drape
    sway = math.sin(t * 0.9) * 0.02 * s
    for k, c in enumerate((FLAG_W, FLAG_B, FLAG_R)):
        a, b = hh * k / 3, hh * (k + 1) / 3
        pts = [(fx + 0.01 * s, fy + a), (fx + w + sway * (a / hh), fy + a + 0.02 * s), (fx + w * 0.9 + sway * (b / hh), fy + b),
               (fx + 0.01 * s, fy + b)]
        p.poly(pts, c, None)
    p.poly([(fx, fy), (fx + w, fy + 0.02 * s), (fx + w * 0.9 + sway, fy + hh), (fx, fy + hh)], None, INK, 2.2)
    for k in range(1, 4):  # folds
        p.line([(fx + w * k / 4, fy + 0.02 * s), (fx + w * k / 4 * 0.92 + sway * 0.8, fy + hh)], (0, 0, 0, 0) if False else
               B.dk(FLAG_W, 0.85), 1.4)


def podium(img, cam, pc, hands=None, glass=True):
    """The podium: plain dark wood, no emblem. Top 1.25 m above the floor (on the stage). Two microphones with plain
    coloured cube flags, a water glass and a carafe, a few papers."""
    p = B.Pen(img, cam)
    b = PODIUM_BOX
    y0, y1 = STAGE_BOX['h'], STAGE_BOX['h'] + b['h']
    hw = b['w'] / 2
    quad(p, pc, [(-hw, y1, b['z0']), (hw, y1, b['z0']), (hw, y1, b['z1']), (-hw, y1, b['z1'])], PODIUM_L, INK, 2.4)
    front = b['z1'] if pc.dirz < 0 else b['z0']
    quad(p, pc, [(-hw, y0, front), (hw, y0, front), (hw, y1, front), (-hw, y1, front)], PODIUM, INK, 2.6)
    quad(p, pc, [(-hw + 0.06, y0 + 0.08, front), (hw - 0.06, y0 + 0.08, front), (hw - 0.06, y1 - 0.12, front),
                 (-hw + 0.06, y1 - 0.12, front)], B.dk(PODIUM, 0.86), INK, 1.8)
    quad(p, pc, [(-hw - 0.02, y1 - 0.06, front), (hw + 0.02, y1 - 0.06, front), (hw + 0.02, y1, front), (-hw - 0.02, y1, front)],
         PODIUM_L, INK, 2.0)
    s = pc.f / pc.depth(0.42)
    if glass:   # papers, a glass of water and a carafe on the top
        papers = [pc.P(-0.18, y1 + 0.003, 0.32), pc.P(0.14, y1 + 0.003, 0.32), pc.P(0.14, y1 + 0.003, 0.5),
                  pc.P(-0.18, y1 + 0.003, 0.5)]
        p.poly(papers, (248, 248, 244), INK, 1.4)
        gx, gy = pc.P(-0.32, y1, 0.42)
        p.poly([(gx - 0.03 * s, gy - 0.11 * s), (gx + 0.03 * s, gy - 0.11 * s), (gx + 0.025 * s, gy), (gx - 0.025 * s, gy)],
               GLASS, INK, 1.4)
        p.poly([(gx - 0.028 * s, gy - 0.07 * s), (gx + 0.028 * s, gy - 0.07 * s), (gx + 0.025 * s, gy), (gx - 0.025 * s, gy)],
               (170, 206, 230), None)
        cx, cy = pc.P(0.33, y1, 0.42)
        p.poly(curve([(cx - 0.02 * s, cy - 0.2 * s), (cx + 0.02 * s, cy - 0.2 * s), (cx + 0.025 * s, cy - 0.14 * s),
                      (cx + 0.05 * s, cy - 0.06 * s), (cx + 0.04 * s, cy), (cx - 0.04 * s, cy), (cx - 0.05 * s, cy - 0.06 * s),
                      (cx - 0.025 * s, cy - 0.14 * s)], 3), GLASS, INK, 1.4)
        p.poly([(cx - 0.045 * s, cy - 0.07 * s), (cx + 0.045 * s, cy - 0.07 * s), (cx + 0.04 * s, cy), (cx - 0.04 * s, cy)],
               (170, 206, 230), None)
    return y1


def podium_mics(img, cam, pc):
    """The two microphones, in front of his chest, clear of his face."""
    p = B.Pen(img, cam)
    y1 = STAGE_BOX['h'] + PODIUM_BOX['h']
    for X, c, stripe in ((-0.17, (200, 40, 50), (250, 250, 250)), (0.19, (40, 90, 170), None)):
        base = pc.P(X, y1, 0.36)
        top = pc.P(X * 0.7, y1 + 0.32, 0.18)
        mic(p, base, top, c, stripe)


# ------------------------------------------------------------------------------------------- the shots
def cam_front(t, zoom=None):
    """Shot 1 and 5: from the camera platform at the back, along the aisle, a long lens on the podium. Slow zoom in."""
    pc = PCam(0.0, 2.0, 9.6, -1, 7000.0, oy=800.0)
    z = 1.0 + 0.32 * min(1.0, t / 7.0) if zoom is None else zoom
    return pc, B.Cam(z, 540, 905 + 25 * (z - 1))


def peskov_spec(t, mouth='set', blink=False, look=0.0, breath=0.0):
    sp = dict(PESKOV, mouth=mouth, blink=blink, look=look, head_dy=breath)
    # resting on the podium: the upper arms hang by his sides, the forearms come forward (towards us, so drawn
    # shorter) to the hands flat on the podium's top (figure-rig 5b: how people hold things in front)
    sw = sp['shoulders']
    sp['arms'] = {'L': ((-(sw - 4), 258), (-108, 334), 'flat'), 'R': ((sw - 4, 262), (106, 338), 'flat')}
    return sp


def draw_peskov(img, cam, pc, t, **kw):
    X, Z = PESKOV_AT
    s = pc.scale(Z)
    nx, ny = pc.P(X, STAGE_BOX['h'] + F.SOLE_Y / UPM, Z)
    sp = peskov_spec(t, **kw)
    person(img, cam, nx, ny, s, sp, t)
    return nx, ny, s, sp


def shot_front(t, zoom=None, behind=None, front=None, **kw):
    pc, cam = cam_front(t, zoom)
    img = B.canvas(WALL)
    room(img, cam, pc, t)
    flag(img, cam, pc, t)
    if behind:
        behind(img, cam, pc)
    nx, ny, s, sp = draw_peskov(img, cam, pc, t, **kw)
    podium(img, cam, pc)
    if front:
        front(img, cam, pc)
    p = B.Pen(img, B.Local(cam, nx, ny, s))
    for side in 'LR':   # his hands rest on the podium's top, in front of its back edge
        el, wr, shape = sp['arms'][side][:3]
        B.gesture_hand(p, el, wr, shape, sp['skin'])
    podium_mics(img, cam, pc)
    return img


def cam_reverse():
    """Shot 2: the 180. From just beside the podium, at his eye height, looking down the hall to the back doors."""
    return PCam(0.3, 1.55, -0.15, 1, 1050.0, oy=640.0, yaw=0.42), B.Cam(1.0, 540, 960)


def chaos_items(pc, chaos=True, people=True, zmin=-99.0):
    items = []
    for zi, z in enumerate(ROWS_Z):
        for xi, x in enumerate(SEATS_X):
            if chaos and (zi, xi) == HIDE_SEAT:
                continue
            items.append((z, x, 'chair', (x, z, CHAOS_CHAIRS.get((zi, xi), 0.0) if chaos else 0.0)))
    for i, (x, z) in enumerate(TRIPODS):
        if not (chaos and i == TRIPOD_TAKEN):
            items.append((z, x, 'tripod', (x, z)))
    if people:
        for who in CROWD:
            items.append((who['z'] - 0.05, who['x'], 'person', who))
    items = [i for i in items if i[0] >= zmin and pc.depth(i[0], i[1]) > 0.5]
    return sorted(items, key=lambda i: -pc.depth(i[0], i[1]))


def draw_items(img, cam, pc, items, t):
    for z, x, kind, a in items:
        if kind == 'chair':
            chair(img, cam, pc, a[0], a[1], over=a[2])
        elif kind == 'tripod':
            tripod(img, cam, pc, a[0], a[1], y0=0.3)
        else:
            crowd_person(img, cam, pc, a, t)


def shot_reverse(t, people=True):
    pc, cam = cam_reverse()
    img = B.canvas(WALL)
    room(img, cam, pc, t, chaos=True)
    risers(img, cam, pc)
    for X, Z, r, seed in FLOOR_SPLATS:
        floor_splat(img, cam, pc, X, Z, r, seed)
    draw_items(img, cam, pc, chaos_items(pc), t)
    p = B.Pen(img, cam)
    for X, Y, Z, r, seed in AIR_DROPS:   # blood flying from the tackle (thrown out, falling)
        u = (t * 1.3 + seed * 0.37) % 1.0
        X, Y = X + (X - 0.4) * 1.5 * u, Y + 1.2 * u - 3.0 * u * u
        x, y = pc.P(X, Y, Z)
        splat(p, x, y, r * pc.f / pc.depth(Z, X), seed, drops=1)
    return img


# Shot 2's chaos, in the plan. Chairs knocked over (row, seat) -> how far over.
CHAOS_CHAIRS = {(0, 3): 1.0, (0, 5): 0.6, (1, 4): 1.0, (2, 6): 1.0, (3, 1): 0.7, (1, 0): 1.0, (4, 4): 1.0, (2, 2): 0.8}


def crowd_spec(i, base, **kw):
    sp = dict(base)
    sp.update(kw)
    return sp


rng0 = np.random.default_rng(7)
SKINS = [B.PALE, B.PINK, (232, 196, 170), (214, 172, 140), B.OLIVE]
PRESS_C = [(46, 150, 120), (40, 120, 200), (206, 120, 40), (150, 60, 160), (196, 40, 60)]


def reporter_base(k, **kw):
    hair = [('side', (70, 52, 40)), ('bob', (40, 34, 32)), ('crop', (120, 100, 80)), ('long', (90, 60, 40)),
            ('slick', (34, 30, 30)), ('bald', (110, 96, 90)), ('wavy', (150, 110, 70))][k % 7]
    women = hair[0] in ('bob', 'long', 'wavy')
    pale = tuple(int(0.55 * c + 0.45 * w) for c, w in zip(SKINS[k % len(SKINS)], (232, 230, 228)))   # drained of colour
    sp = dict(name=f'reporter {k}', skin=pale, hw=66 if women else 70, hh=86 if women else 90,
              jaw='soft' if women else ['square', 'round'][k % 2], hair=hair[0], hair_c=hair[1],
              outfit=['suit', 'jumper', 'blouse', 'suit', 'jumper'][k % 5],
              jacket=[(60, 64, 80), (120, 60, 60), (70, 90, 70), (90, 80, 110), (150, 120, 90)][k % 5],
              shirt=(236, 236, 240), tie=(90, 40, 50) if k % 3 == 0 else None, trousers=(56, 58, 66),
              shoulders=136 if women else 150, full=True, pose='custom', press=True, lanyard_c=PRESS_C[k % 5],
              wide=True, brows='terror', mouth='scream', lashes=women, seed=k)
    if women:
        sp.update(skirt=(70, 72, 84) if k % 2 else None, tights=(200, 180, 170))
        if not sp['skirt']:
            sp.pop('skirt')
    sp.update(kw)
    return sp


def zombie_base(k, **kw):
    sp = dict(ZOMBIE, name=f'zombie {k}', seed=k + 10, hw=70 - 3 * (k % 3), jacket=[(80, 84, 96), (110, 96, 80), (70, 80, 70),
              (96, 70, 70)][k % 4], press=(k % 3 != 2), lanyard_c=PRESS_C[(k + 2) % 5],
              skin=[ZSKIN, (148, 166, 140), (162, 172, 132)][k % 3])
    sp.update(kw)
    return sp


# who is where in shot 2, and what each is doing (every background person has one clear action). Plan units.
CROWD = [
    dict(kind='zombie', k=0, x=-0.45, z=8.5, act='door'),        # zombies jammed in the back doorway
    dict(kind='zombie', k=1, x=0.5, z=8.55, act='door'),
    dict(kind='zombie', k=9, x=-0.2, z=7.95, act='lunge'),        # already through the back doors
    dict(kind='zombie', k=10, x=0.75, z=8.1, act='lunge_l'),
    dict(kind='zombie', k=11, x=-5.0, z=7.7, act='lunge_l', v=(0.5, -0.2)),      # pouring in through the side door
    dict(kind='zombie', k=12, x=-4.7, z=8.3, act='lunge_l', v=(0.4, -0.3)),
    dict(kind='zombie', k=15, x=-4.3, z=7.7, act='lunge'),
    dict(kind='person', k=8, x=-4.2, z=7.05, act='door_pull'),    # trying to shove the side door shut (too late)
    dict(kind='person', k=1, x=-2.0, z=7.9, act='tripod'),        # beating a zombie off with a tripod, on the riser
    dict(kind='zombie', k=4, x=-1.55, z=7.75, act='lunge_r'),
    dict(kind='zombie', k=14, x=3.0, z=7.2, act='lunge_r'),
    dict(kind='person', k=0, x=0.7, z=6.4, act='run_away', v=(0.0, 0.8)),       # running for the back doors (straight into them)
    dict(kind='zombie', k=13, x=-3.0, z=6.3, act='lunge'),
    dict(kind='zombie', k=8, x=-3.6, z=5.2, act='lunge_l'),
    dict(kind='person', k=3, x=-2.5, z=4.9, act='phone'),         # filming it all on a phone
    dict(kind='zombie', k=16, x=-1.3, z=6.0, act='lunge_r'),
    dict(kind='person', k=2, x=2.1, z=5.3, act='chair'),          # swinging a chair at a zombie
    dict(kind='zombie', k=5, x=2.75, z=5.6, act='lunge_r'),
    dict(kind='zombie', k=7, x=0.35, z=5.0, act='lunge', v=(0.05, -0.7)),         # lurching down the aisle after...
    dict(kind='person', k=5, x=0.05, z=4.2, act='run', v=(0.1, -1.0)),           # ...a reporter fleeing towards us
    dict(kind='zombie', k=17, x=-3.9, z=3.4, act='lunge'),
    dict(kind='person', k=6, x=-1.7, z=3.45, act='hide'),         # hiding under a chair (seat 1.2)
    dict(kind='heroine', k=0, x=-0.72, z=3.15, act='crawl', v=(0.12, 0.0)),      # our reporter, crawling (shot 3 follows her)
    dict(kind='person', k=7, x=-1.75, z=2.6, act='run', v=(-0.4, -0.3)),          # fleeing past the front row
    dict(kind='person', k=4, x=0.5, z=2.0, act='tackled'),        # grabbed, in the foreground
    dict(kind='zombie', k=6, x=0.12, z=2.2, act='tackle'),
]
HIDE_SEAT = (1, 2)              # the chair the hider is under (drawn with her)
TRIPOD_TAKEN = 1                # the tripod in the fighter's hands
FLOOR_SPLATS = [(0.3, 1.75, 0.1, 61), (-0.6, 3.9, 0.12, 62), (0.3, 6.2, 0.14, 63), (-2.8, 6.0, 0.12, 64), (1.6, 3.3, 0.1, 65)]
AIR_DROPS = [(0.45, 1.75, 1.95, 0.026, 71), (0.25, 1.95, 2.0, 0.02, 72), (0.7, 1.55, 1.9, 0.018, 73), (0.15, 1.6, 1.9, 0.016, 74)]


def crowd_person(img, cam, pc, who, t):
    k, act, X, z = who['k'], who['act'], who['x'], who['z']
    vx, vz = who.get('v', (0.0, 0.0))        # some are on the move through the shot
    X, z = X + vx * t, z + vz * t             # t: seconds since the 180 (the same clock in shots 2 and 3)
    if pc.depth(z, X) < 0.6:
        return
    y0 = 0.3 if 7.6 <= z <= 8.6 and any(a <= X <= b for a, b in RISERS) else 0.0
    s = pc.scale(z, X)
    nx, ny = pc.P(X, y0 + F.SOLE_Y / UPM, z)
    fy = pc.P(X, y0, z)[1]
    ph = t * 9 + k
    if who['kind'] == 'heroine':
        x, y = pc.P(X, 0.0, z)
        reporter_crawl(img, cam, x, y, s, t, step=t * 7, grab=GRAB[0])
        return
    if who['kind'] == 'zombie':
        sp = zombie_base(k)
        rig = F.Rig(sp)
        kit.contact_shadow(img, cam, nx, fy, 300 * s)
        if act == 'door':
            sp['arms'] = {'L': rig.arm('L', (-260, -40 + 20 * math.sin(ph)), 'palm', 'out', strict=False),
                          'R': rig.arm('R', (250, -10 + 20 * math.cos(ph)), 'palm', 'out', strict=False)}
            person(img, cam, nx, ny, s, sp, t, tilt=0.06 * math.sin(ph * 0.5))
        elif act in ('lunge_r', 'lunge_l', 'lunge'):
            d = 1 if act == 'lunge_r' else -1 if act == 'lunge_l' else (1 if k % 2 else -1)   # always sideways: reads best
            if d:
                near, far = ('L', 'R') if d > 0 else ('R', 'L')   # the arm on the far side crosses the body
                sp['arms'] = {far: rig.arm(far, (d * 380, -10), 'palm', 'out', strict=False),
                              near: rig.arm(near, (d * 150, 30), 'palm', 'down')}
            else:
                sp['arms'], sp['reach_cam'] = zombie_reach(rig), True
            person(img, cam, nx, ny, s, sp, t, legs='lunge', phase=ph, tilt=0.22 * d)
        elif act == 'tackle':   # grabbing the reporter from behind and biting at his shoulder
            sp['arms'] = {'L': rig.arm('L', (-300, 80), 'palm', 'out', strict=False),
                          'R': rig.arm('R', (-120, 200), 'palm', 'down')}
            sp['face_splats'] = [(10, 70, 12, 81), (-30, 40, 8, 82)]
            person(img, cam, nx, ny, s, sp, t, legs='lunge', phase=1.0, tilt=0.32)
        return
    sp = reporter_base(k)
    rig = F.Rig(sp)
    if act not in ('tackled', 'hide', 'climb'):
        kit.contact_shadow(img, cam, nx, fy, 300 * s)
    if act == 'run':
        sp['arms'] = {'L': rig.arm('L', (-200, -120 + 60 * math.sin(ph)), 'palm', 'out', strict=False),
                      'R': rig.arm('R', (210, -100 - 60 * math.sin(ph)), 'palm', 'out', strict=False)}
        sp['splats'] = [(30, 120, 18, k)]
        person(img, cam, nx, ny, s, sp, t, legs='run', phase=ph, tilt=0.08 * math.sin(ph))
    elif act == 'run_away':
        sp['arms'] = {'L': rig.arm('L', (-230, -150), 'palm', 'out', strict=False),
                      'R': rig.arm('R', (220, -170), 'palm', 'out', strict=False)}
        person_back(img, cam, nx, ny, s, sp, t, legs='run', phase=ph)
    elif act == 'door_pull':  # both hands on the handle, leaning back
        sp['arms'] = {'L': rig.arm('L', (-50, 250), 'grip', 'out'), 'R': rig.arm('R', (50, 240), 'grip', 'out')}
        person_back(img, cam, nx, ny, s, sp, t, legs='lunge', phase=0.4, tilt=-0.12)
    elif act == 'tripod':
        sp['arms'] = {'L': rig.arm('L', (40, -230), 'grip', 'out'), 'R': rig.arm('R', (170, -190), 'grip', 'out')}
        p = person(img, cam, nx, ny, s, sp, t, legs='lunge', phase=0.5, tilt=-0.1)
        for end in ((-420, -360), (-400, -280), (-440, -320)):   # the tripod's legs, swung over his head
            p.line([(40, -240), end], (40, 40, 44), 9)
        p.poly([(40, -270), (130, -270), (130, -200), (40, -200)], (34, 34, 38), INK, 2.0)
    elif act == 'chair':
        sp['arms'] = {'L': rig.arm('L', (-130, -260), 'grip', 'out'), 'R': rig.arm('R', (40, -280), 'grip', 'out')}
        p = person(img, cam, nx, ny, s, sp, t, legs='lunge', phase=2.0, tilt=0.15)
        p.poly([(-250, -440), (110, -450), (100, -300), (-240, -290)], CHAIR, INK, 2.4)   # the chair raised overhead
        p.line([(-240, -290), (-280, -120)], CHAIR_FRAME, 6)
        p.line([(100, -300), (130, -130)], CHAIR_FRAME, 6)
    elif act == 'phone':
        sp['arms'] = rig.pose('hold', side='R', shape='phone', lift=1.0)
        sp['arms']['L'] = rig.pose('sides')['L']
        sp['mouth'] = 'scream'
        person(img, cam, nx, ny, s, sp, t)
    elif act == 'tackled':   # knocked sideways, arms flung up
        sp['arms'] = {'L': rig.arm('L', (-200, -260), 'palm', 'out', strict=False),
                      'R': rig.arm('R', (230, -240), 'palm', 'out', strict=False)}
        sp['splats'] = [(-20, 140, 26, 9), (60, 60, 14, 10)]
        sp['face_splats'] = [(30, -120, 9, 11)]
        person(img, cam, nx, ny, s, sp, t, legs='run', phase=0.6, tilt=0.3)
    elif act == 'hide':  # crouched on the floor, arms over the head, under the chair
        sp['arms'] = {'L': rig.arm('L', (30, -280), 'palm', 'out'), 'R': rig.arm('R', (-20, -270), 'palm', 'out')}
        sp['mouth'] = 'line'
        kit.contact_shadow(img, cam, nx, fy, 340 * s * 0.72)
        person(img, cam, nx, fy - 740 * s * 0.72, s * 0.72, sp, t, legs='kneel', tilt=0.25)
        zi, xi = HIDE_SEAT
        chair(img, cam, pc, SEATS_X[xi], ROWS_Z[zi])
    elif act == 'climb':   # one foot up on the seat, a hand on the chair back
        sp['arms'] = {'L': rig.arm('L', (-240, 300), 'flat', 'out'), 'R': rig.arm('R', (250, 120), 'palm', 'out', strict=False)}
        sp['splats'] = [(-60, 200, 20, 33)]
        kit.contact_shadow(img, cam, nx, fy, 300 * s)
        person(img, cam, nx, ny - 0.3 * pc.f / pc.depth(z, X), s, sp, t, legs='run', phase=0.3, tilt=-0.2)


# ------------------------------------------------------------------------------------------- shot 3 and 4 (stills)
def phone_screen(img, box, t=0.0, typed=1.0, scale=1.0):
    """The ministry's page on her phone: a generic blue bar with a plain Russian header (no emblem), the report."""
    x0, y0, x1, y1 = [v * B.SS for v in box]
    I = lambda v: int(round(v))
    d = ImageDraw.Draw(img)
    S = B.SS * scale
    d.rectangle([x0, y0, x1, y1], fill=(250, 250, 250))
    d.rectangle([x0, y0, x1, y0 + 120 * S], fill=(236, 238, 242))     # the address bar
    d.rounded_rectangle([x0 + 30 * S, y0 + 40 * S, x1 - 30 * S, y0 + 96 * S], I(26 * S), fill=(255, 255, 255),
                        outline=(200, 202, 210), width=I(2 * S))
    f = ImageFont.truetype(B.SANS, I(24 * S))
    d.text((x0 + 60 * S, y0 + 68 * S), 'health.gov.ru', font=f, fill=(110, 110, 120), anchor='lm')
    d.rectangle([x0, y0 + 120 * S, x1, y0 + 290 * S], fill=(22, 62, 150))
    fh = ImageFont.truetype(B.SANS, I(36 * S))
    d.text(((x0 + x1) / 2, y0 + 180 * S), 'МИНИСТЕРСТВО', font=fh, fill=(255, 255, 255), anchor='mm')
    d.text(((x0 + x1) / 2, y0 + 232 * S), 'ЗДРАВООХРАНЕНИЯ', font=fh, fill=(255, 255, 255), anchor='mm')
    fs = ImageFont.truetype(B.SANS, I(26 * S))
    d.text((x0 + 50 * S, y0 + 350 * S), 'ОФИЦИАЛЬНОЕ СООБЩЕНИЕ', font=fs, fill=(196, 30, 44), anchor='lm')
    d.text((x0 + 50 * S, y0 + 392 * S), '06.10.2026', font=fs, fill=(130, 130, 140), anchor='lm')
    fb = ImageFont.truetype(B.SANS, I(66 * S))
    rows = ['Everything', 'fine.', 'Stop asking', 'questions.']
    for i, r in enumerate(rows):
        d.text((x0 + 50 * S, y0 + (480 + 84 * i) * S), r, font=fb, fill=(20, 20, 26), anchor='lm')
    for k in range(4):  # greyed body text below
        d.rectangle([x0 + 50 * S, y0 + (850 + 34 * k) * S, x1 - (60 + 90 * (k % 2)) * S, y0 + (866 + 34 * k) * S],
                    fill=(214, 214, 220))


class Turned:
    """A local frame turned by `ang` (radians, clockwise on screen) about (cx, cy) in world pixels: the phone's own
    frame, so the phone and the hands holding it tilt together."""
    def __init__(self, cam, cx, cy, ang):
        self.cam, self.cx, self.cy, self.c, self.sn, self.s = cam, cx, cy, math.cos(ang), math.sin(ang), cam.s

    def P(self, u, v):
        return self.cam.P(self.cx + u * self.c - v * self.sn, self.cy + u * self.sn + v * self.c)

    def S(self, v):
        return self.cam.S(v)


def limb(p, cl, ws, colr, tip_round=True, lw=2.6):
    """A tapering finger or thumb along a centre line `cl` with widths `ws` (half-widths), rounded at the tip.
    Returns the tip point and direction (for the nail)."""
    L, R = [], []
    for i, (x, y) in enumerate(cl):
        a = cl[max(0, i - 1)]
        b = cl[min(len(cl) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        L.append((x + nx * ws[i], y + ny * ws[i]))
        R.append((x - nx * ws[i], y - ny * ws[i]))
    (x1, y1), (x0, y0) = cl[-1], cl[-2]
    d = math.atan2(y1 - y0, x1 - x0)
    w = ws[-1]
    cap = [(x1 + w * math.cos(d + a), y1 + w * math.sin(d + a)) for a in np.linspace(math.pi / 2, -math.pi / 2, 7)]
    p.poly(curve(L + cap[1:-1] + R[::-1], 3), colr, INK, lw)
    return (x1, y1), d


def thumb(p, base, knuckle, tip, skin, w=(46, 38, 30)):
    """A thumb seen from above: broad where it leaves the palm, a bend at the knuckle, a flat nail at the tip."""
    mid = ((base[0] + knuckle[0]) / 2, (base[1] + knuckle[1]) / 2)
    end, d = limb(p, [base, mid, knuckle, tip], [w[0], w[0] * 0.92, w[1], w[2]], skin)
    sd = B.dk(skin, 0.8)
    nx, ny = -math.sin(d), math.cos(d)
    p.line([(knuckle[0] + nx * w[1] * 0.7, knuckle[1] + ny * w[1] * 0.7), (knuckle[0] - nx * w[1] * 0.2, knuckle[1] - ny * w[1] * 0.2)],
           sd, 2.0)                                                        # the crease at the knuckle
    nc = (end[0] - math.cos(d) * w[2] * 0.45, end[1] - math.sin(d) * w[2] * 0.45)
    p.ell(nc[0], nc[1], w[2] * 0.8, w[2] * 0.62, B.lt(skin, 1.06), B.dk(skin, 0.72), 1.8, rot=d)   # the nail
    p.ell(nc[0] + math.cos(d) * w[2] * 0.42, nc[1] + math.sin(d) * w[2] * 0.42, w[2] * 0.3, w[2] * 0.5,
          (252, 246, 244), None, rot=d)


def finger(p, pts, w, skin, nail=True):
    """A curled finger (back of the finger towards us): knuckle creases and a nail at the tip."""
    end, d = limb(p, pts, [w, w * 0.96, w * 0.9, w * 0.82][:len(pts)], skin, lw=2.4)
    sd = B.dk(skin, 0.78)
    for k in range(1, len(pts) - 1):   # creases over the joints
        x, y = pts[k]
        a, b = pts[k - 1], pts[k + 1]
        dd = math.atan2(b[1] - a[1], b[0] - a[0])
        nx, ny = -math.sin(dd), math.cos(dd)
        p.line([(x + nx * w * 0.5, y + ny * w * 0.5), (x - nx * w * 0.5, y - ny * w * 0.5)], sd, 1.6)
    if nail:
        nc = (end[0] - math.cos(d) * w * 0.35, end[1] - math.sin(d) * w * 0.35)
        p.ell(nc[0], nc[1], w * 0.62, w * 0.5, B.lt(skin, 1.06), B.dk(skin, 0.72), 1.6, rot=d)


PHONE_W, PHONE_H, SCREEN_W, SCREEN_H = 560, 1150, 516, 1106
PHONE_AT, PHONE_ANG = (540, 790), -0.06


@functools.lru_cache(maxsize=4)
def phone_hands_layer(tap_key):
    """Both hands on the phone, rendered once per thumb position, matched to the drawn phone (same size and tilt)."""
    import hands3d
    k = (PHONE_W / 2) / hands3d.PHONE[0]                 # world pixels per metre
    cam = B.Cam(1.0, 540, 960)
    T = Turned(cam, PHONE_AT[0], PHONE_AT[1], PHONE_ANG)
    return hands3d.phone_hands((B.W * B.SS, B.H * B.SS), lambda X, Y: T.P(X * k, -Y * k), tap_key,
                               skin=(240, 228, 220), sleeve=REPORTER['jacket'], outline=6.0)


def shot_phone(t=0.0, tap=None):
    """Shot 4: a straight insert of her phone's screen filling the frame, the room just visible round it, out of focus."""
    from PIL import ImageFilter
    img = B.canvas((96, 70, 50))
    cam = B.Cam(1.0, 540, 960)
    # the room behind, out of focus: floor, chair legs, a fallen chair, blood
    bg = B.canvas((126, 90, 60))
    q = B.Pen(bg, cam)
    q.poly([(-100, -100), (1200, -100), (1200, 520), (-100, 620)], (196, 186, 166), None)
    for x in (60, 300, 760, 1000):
        q.poly([(x, 380), (x + 150, 380), (x + 150, 560), (x, 560)], CHAIR, None)
        q.line([(x + 10, 560), (x + 4, 900)], CHAIR_FRAME, 10)
        q.line([(x + 140, 560), (x + 146, 900)], CHAIR_FRAME, 10)
    q.poly([(820, 1500), (1100, 1380), (1150, 1600), (880, 1720)], CHAIR, None)
    splat(q, 220, 1700, 90, 44)
    bg = bg.filter(ImageFilter.GaussianBlur(26 * B.SS))
    img.alpha_composite(bg)
    B.shade(img, 0.18)
    T = Turned(cam, PHONE_AT[0], PHONE_AT[1], PHONE_ANG)
    p = B.Pen(img, T)
    skin, sd = (240, 228, 220), (214, 194, 186)
    hw, hh = PHONE_W / 2, PHONE_H / 2

    def rrect(w2, h2, r):
        pts = []
        for cx, cy, a0 in ((w2 - r, -h2 + r, -90), (w2 - r, h2 - r, 0), (-w2 + r, h2 - r, 90), (-w2 + r, -h2 + r, 180)):
            pts += [(cx + r * math.cos(math.radians(a0 + k * 15)), cy + r * math.sin(math.radians(a0 + k * 15))) for k in range(7)]
        return pts
    p.poly(rrect(hw, hh, 70), (22, 22, 26), INK, 3.0)
    p.poly(rrect(hw - 4, hh - 4, 66), (44, 44, 52), None)
    # the screen, drawn flat and turned with the phone
    S = B.SS
    scr = Image.new('RGBA', (SCREEN_W * S, SCREEN_H * S), (0, 0, 0, 0))
    phone_screen(scr, (0, 0, SCREEN_W, SCREEN_H), t, scale=SCREEN_W / 720)
    mask = Image.new('L', scr.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, scr.width - 1, scr.height - 1], 52 * S, fill=255)
    scr.putalpha(mask)
    scr = scr.rotate(-math.degrees(PHONE_ANG), Image.BICUBIC, expand=True)
    cx, cy = cam.P(*PHONE_AT)
    img.alpha_composite(scr, (int(cx - scr.width / 2), int(cy - scr.height / 2)))
    p.ell(0, -hh + 34, 46, 12, (14, 14, 16), None)            # the camera notch
    # her hands: MakeHuman's real hands posed round the phone and drawn flat (hands3d.py); the right thumb types
    img.alpha_composite(phone_hands_layer(0 if tap is None else int(tap) % 2))
    for (u, v, r, seed) in ((-hw - 70, hh + 230, 20, 41), (hw + 120, hh + 120, 14, 42), (-hw + 150, hh + 40, 9, 43)):
        splat(p, u, v, r, seed, drops=3)
    for (u, v, r, seed) in ((hw - 70, -250, 10, 45), (hw - 110, 160, 8, 46)):   # drops on the glass
        splat(p, u, v, r, seed, drops=2)
        p.ell(u - r * 0.3, v - r * 0.35, r * 0.25, r * 0.18, (255, 210, 210), None)
    return img


def reporter_crawl(img, cam, x, y, s, t, grab=0.0, step=0.0, flip=1):
    """Shots 2 and 3: crawling on hands and knees across the floor, seen from the side (heading to our left when
    flip=1), her face turned to us in terror (the cartoon convention: body in profile, head to camera). (x, y) is the
    point on the floor under her middle. step: the crawl cycle (radians); grab (0-1): her front hand reaching for
    the phone."""
    L = B.Local(cam, x, y, s, flip)
    p = B.Pen(img, L)
    sp = dict(REPORTER, wide=True, brows='terror', mouth='gasp', skin=(240, 234, 232),
              face_splats=[(-38, -110, 8, 7), (44, -60, 6, 8)], tail_swing=40 + 20 * math.sin(step))
    jc, skin, tights = sp['jacket'], sp['skin'], sp['tights']
    kit.contact_shadow(img, cam, x, y, 640 * s, alpha=0.25)
    a, b = math.sin(step), math.sin(step + math.pi)        # the two diagonal pairs move in turn
    lift = lambda v: max(0.0, v) * 18

    def limb_arm(dx, colr, ph, reach=0.0):
        sh = (-150 + dx, -300)
        hand = (-210 + dx + 30 * ph - 90 * reach, -6 - lift(ph) - 10 * reach)
        el = ((sh[0] + hand[0]) / 2 - 18, (sh[1] + hand[1]) / 2)
        B.arm(p, sh, el, (hand[0], hand[1] - 18), colr, w=26)
        p.poly(curve([(hand[0] + 26, hand[1] - 22), (hand[0] - 30, hand[1] - 16), (hand[0] - 52, hand[1] - 4),
                      (hand[0] - 40, hand[1] + 4), (hand[0] + 24, hand[1] + 2)], 3), B.dk(skin, 0.95) if dx else skin, INK, 2.2)

    def limb_leg(dx, colr, ph):
        hip, knee = (120 + dx, -300), (150 + dx + 26 * ph, -28 - lift(ph))
        foot = (360 + dx + 26 * ph, -14 - lift(ph) * 0.5)
        p.poly(curve([(hip[0] - 40, hip[1] - 20), (hip[0] + 44, hip[1] - 10), (knee[0] + 30, knee[1] - 6),
                      (knee[0] - 28, knee[1] + 2)], 2), colr, INK, 2.4)
        p.poly([(knee[0] - 6, knee[1] + 26), (knee[0] + 10, knee[1] - 24), (foot[0], foot[1] - 16), (foot[0], foot[1] + 6)],
               colr, INK, 2.4)
        p.ell(knee[0], knee[1], 30, 26, colr, INK, 2.4)
        p.poly(curve([(foot[0] - 16, foot[1] - 18), (foot[0] + 36, foot[1] - 14), (foot[0] + 44, foot[1] + 4),
                      (foot[0] - 16, foot[1] + 8)], 3), sp['shoe'], INK, 2.2)
    # the far side first, a shade darker
    limb_leg(-30, B.dk(tights, 0.86), b)
    limb_arm(30, B.dk(jc, 0.86), b)
    # the body: blouse over the back, the skirt over the hips
    p.poly(curve([(-205, -310), (-150, -372), (-20, -396), (110, -392), (190, -352), (196, -282), (110, -250), (-20, -256),
                  (-160, -262)], 5), jc, INK, 2.6)
    p.poly(curve([(60, -392), (150, -384), (200, -340), (196, -262), (120, -232), (60, -244)], 4), sp['skirt'], INK, 2.4)
    soft(img, L, [(-150, -370), (40, -385), (190, -360), (40, -345)], (255, 255, 255), 0.2, 6)
    splat(p, -60, -340, 18, 5)
    splat(p, 30, -280, 12, 6, drops=2)
    limb_leg(0, tights, a)
    kit.dangle(p, (-205, -300), 150, 0.2 * math.sin(step * 2), sp['lanyard_c'], 6, tag=(46, 58, (248, 248, 246)))
    limb_arm(0, jc, a, reach=grab)
    # the neck, and her head turned to us
    p.poly([(-222, -350), (-180, -372), (-160, -320), (-206, -300)], skin, INK, 2.4)
    hx, hy = -250, -470
    B.hair_back(p, sp, hx, hy, sp['hw'], sp['hh'])
    B.head(img, p, sp, t, hx, hy)
    for (fx, fy, r, seed) in sp['face_splats']:
        splat(p, hx + fx, hy + 150 + fy, r, seed, drops=2)


GRAB = [0.0]                    # how far her hand has reached for the phone (shot 3)
HEROINE_S3 = (-0.45, 3.25)      # where she has crawled to by shot 3 (down the aisle, towards the podium)
PHONE_S3 = (-0.2, 2.95)         # her phone, dropped on the floor ahead of her


def floor_phone(img, cam, pc, X, Z, lit=True):
    """A phone lying face up on the floor (about 15 x 7 cm), its screen lit."""
    p = B.Pen(img, cam)
    pts = [(X - 0.04, 0.005, Z - 0.08), (X + 0.04, 0.005, Z - 0.08), (X + 0.04, 0.005, Z + 0.08), (X - 0.04, 0.005, Z + 0.08)]
    quad(p, pc, pts, (26, 26, 30), INK, 2.0)
    scr = [(X - 0.032, 0.006, Z - 0.07), (X + 0.032, 0.006, Z - 0.07), (X + 0.032, 0.006, Z + 0.07), (X - 0.032, 0.006, Z + 0.07)]
    quad(p, pc, scr, (190, 214, 240) if lit else (40, 40, 46), None)


def shot_crawl(t=0.0, grab=0.0):
    """Shot 3 (still): low in the aisle, looking towards the back doors, she crawls towards us."""
    pc = PCam(-0.45, 0.42, 1.85, 1, 950.0, oy=880.0)
    cam = B.Cam(1.0, 540, 960)
    img = B.canvas(WALL)
    room(img, cam, pc, t, chaos=True)
    risers(img, cam, pc)
    for X, Z, r, seed in FLOOR_SPLATS:
        floor_splat(img, cam, pc, X, Z, r, seed)
    GRAB[0] = grab
    if grab < 0.6:
        floor_phone(img, cam, pc, *PHONE_S3)
    items = [(HEROINE_S3[1] - 0.05, HEROINE_S3[0], k, dict(a, x=HEROINE_S3[0], z=HEROINE_S3[1], v=(0.0, 0.0)))
             if k == 'person' and a['kind'] == 'heroine' else (z, x, k, a) for z, x, k, a in chaos_items(pc)]
    def keep(i):
        if i[2] != 'person':
            return pc.depth(i[0], i[1]) > 1.1
        w = i[3]
        if w['kind'] == 'heroine':
            return True
        vx, vz = w.get('v', (0.0, 0.0))
        X, z = w['x'] + vx * t, w['z'] + vz * t          # where they are now
        if pc.depth(z, X) < 1.1 or w['z'] < 2.7:
            return False
        return -60 < pc.P(X, 1.4, z)[0] < 1140            # nobody cut off by the frame's edge
    items = sorted([i for i in items if keep(i)], key=lambda i: -pc.depth(i[0], i[1]))
    draw_items(img, cam, pc, items, t)
    return img


# ------------------------------------------------------------------------------------------- the approval sheet
def turnaround(sp_fn, legs='stand', bg=(236, 232, 224), h=1180, shadow=True, tilt=0.0):
    img = B.canvas(bg)
    cam = B.Cam(1.0, 540, 960)
    s = 1.1
    nx, ny = 540, 960 - 300 * s + 120
    sp = sp_fn()
    if shadow:
        kit.feet_shadow(img, cam, nx, ny, s)
    person(img, cam, nx - 400 * tilt, ny, s, sp, 0.0, legs=legs, tilt=tilt)
    return img


def closeup(sp, bg=(236, 232, 224), z=2.6):
    img = B.canvas(bg)
    cam = B.Cam(z, 540, 960 - 150)
    person(img, cam, 540, 960, 1.0, sp, 0.0)
    return img


def sheet(dst):
    def pes():
        sp = dict(PESKOV)
        rig = F.Rig(sp)
        sp['arms'] = rig.pose('sides')
        return sp

    def rep():
        sp = dict(REPORTER, splats=[(-50, 140, 18, 5), (70, 300, 12, 6)], face_splats=[(-38, -110, 8, 7)], wide=True,
                  brows='terror', mouth='scream', skin=(240, 234, 232))
        rig = F.Rig(sp)
        sp['arms'] = rig.pose('hold', side='R', shape='phone', lift=1.0)
        sp['arms']['L'] = rig.pose('sides')['L']
        return sp

    def zom():
        sp = dict(ZOMBIE)
        rig = F.Rig(sp)
        sp['arms'] = {'R': rig.arm('R', (380, -10), 'palm', 'out', strict=False), 'L': rig.arm('L', (150, 30), 'palm', 'down')}
        return sp
    pesk = pes()
    stills = [('Peskov', turnaround(pes)), ('Peskov, face', closeup(pesk)),
              ('The reporter', turnaround(rep)), ('A zombie (ex-reporter)', turnaround(zom, legs='lunge', tilt=0.2)),
              ('1. Peskov (title)', title_frame(shot_front(0.3), 0.3)), ('1. End of the slow zoom', shot_front(6.8)),
              ('2. The 180: the hall', shot_reverse(0.0)), ('3. She crawls', shot_crawl(0.0)), ('4. Her phone', shot_phone())]
    cw, ch, lab = 405, 720, 64
    cols = 5
    rows = (len(stills) + cols - 1) // cols
    sh = Image.new('RGB', (cols * (cw + 16) + 16, rows * (ch + lab + 12) + 16), (245, 242, 236))
    d = ImageDraw.Draw(sh)
    f = ImageFont.truetype(B.SANS, 24)
    for i, (name, im) in enumerate(stills):
        x, y = 16 + (i % cols) * (cw + 16), 16 + (i // cols) * (ch + lab + 12)
        sh.paste(im.convert('RGB').resize((cw, ch), Image.LANCZOS), (x, y))
        d.text((x + 2, y + ch + 12), name, font=f, fill=(20, 20, 20))
    sh.save(dst, quality=90)
    return stills


def title_frame(img, t):
    B.title_lines(img, TITLE, alpha=1.0 if t < 0.75 else max(0.0, 1.0 - (t - 0.75) / 0.25))
    return img


# ============================================================================================ the film
import mouths
import mossad_audio as MA
from burnham_film import onepole_lp, normal

mouths.install(B)

# Placeholder timing from Sam's usual pace (3.0-3.6 words a second) until his recordings arrive; then REC replaces
# it (cleaned and levelled by mossad_audio.line; pauses may be shortened, never the words).
LINE1 = ['The researcher in question', 'died from a common pneumonia.', 'All is well.', 'We ask anyone concerned',
         'to pay attention to bulletins', 'from the Ministry of Health.']
LINE2 = ['Any more questions?']
WPS = 3.4


def syl(w):
    return max(1, len(re.findall(r'[aeiouy]+', w.lower().strip('.,?'))))


def word_times(start, pieces, wps=WPS):
    """[(piece index, start, end)] for each word, at the pace, with short pauses at commas and full stops."""
    out, t = [], start
    for i, piece in enumerate(pieces):
        for w in piece.split():
            d = (0.55 + 0.45 * min(2.0, syl(w) / 1.6)) / wps
            out.append((i, t, t + d, w))
            t += d
            if w[-1] in '.?':
                t += 0.32
    return out


import re   # noqa: E402

T = {}
W1 = word_times(0.30, LINE1)
T['line1_end'] = W1[-1][2]
T['s2'] = T['line1_end'] + 0.35                 # the 180: hard cut into the outbreak
T['slap'] = 5.2                                 # shot 1: a hand slaps onto the podium's edge (no reaction)
T['s3'] = T['s2'] + 3.0                         # she crawls
T['grab'] = T['s3'] + 1.05                      # she dives for her phone
T['s3b'] = T['s3'] + 1.5                        # her face as she types
T['s4'] = T['s3'] + 3.0                         # her phone
T['roar'] = T['s4'] + 1.3                       # a zombie roars right behind her
T['crunch'] = T['s4'] + 2.05                    # a crunch, and blood bursts across the screen
T['s5'] = T['s4'] + 3.0                         # back to Peskov
T['arm_throw'] = T['s5'] + 0.2                  # a severed arm (still holding a microphone) flies up...
T['arm_hit'] = T['s5'] + 0.55                   # ...and slaps the backdrop behind him
W2 = word_times(T['s5'] + 1.25, LINE2)
T['line2_end'] = W2[-1][2]
T['black'] = T['line2_end'] + 0.6               # a short silent beat (the screams go on), then hard cut to black
T['dur'] = T['black'] + 0.35
SHOTS = [('front', 0.0, T['s2']), ('reverse', T['s2'], T['s3']), ('crawl', T['s3'], T['s3b']),
         ('face', T['s3b'], T['s4']), ('phone', T['s4'], T['s5']), ('front_end', T['s5'], T['black'])]
BLINKS = [1.9, 4.6, 7.4, T['s5'] + 0.95]        # his slow blinks: he never looks round, never flinches


def track_of(words):
    """Mouth shapes for a placeholder line: the words placed at their times."""
    out = []
    for i, a, b, w in words:
        shapes = mouths._letters_to_shapes(w)
        step = (b - a) / len(shapes)
        out += [(a + n * step - 1 / 12, a + (n + 1) * step - 1 / 12, sh) for n, sh in enumerate(shapes)]
    return out


TRACK = track_of(W1) + track_of(W2)


def caption_at(t):
    for words, end in ((W1, T['line1_end']), (W2, T['line2_end'])):
        if words[0][1] - 0.05 <= t < end + 0.3:
            pieces = LINE1 if words is W1 else LINE2
            cur = [i for i, a, b, w in words if a - 0.05 <= t]
            return pieces[max(cur) if cur else 0]
    return None


def shot_at(t):
    for v, a, b in SHOTS:
        if a <= t < b:
            return v, t - a
    return 'black', 0.0


def peskov_kw(t):
    blink = any(b <= t < b + 0.18 for b in BLINKS)       # a slow, heavy blink (about two drawings)
    m = mouths.at(TRACK, t)
    return dict(mouth='set' if m == 'rest' else 'v:' + m, blink=blink, breath=1.5 * math.sin(2 * math.pi * t / 4.2))


@functools.lru_cache(maxsize=2)
def podium_hand():
    import hands3d
    pc, cam = cam_front(0.0, 1.0)
    k = pc.f / pc.depth(PODIUM_BOX['z1']) * B.SS                 # canvas pixels a metre at the podium's front
    n = int(0.5 * k)
    return hands3d.edge_grab((n, n), k, skin=(236, 226, 220), sleeve=(70, 90, 70), outline=2.5 * B.SS)


@functools.lru_cache(maxsize=2)
def mic_arm():
    import hands3d
    pc, cam = cam_front(0.0, 1.0)
    k = pc.f / pc.depth(-1.18) * B.SS
    n = int(0.6 * k)
    return hands3d.mic_fist((n, n), k, skin=(232, 222, 214), sleeve=(80, 84, 96), outline=2.5 * B.SS)


def paste_sprite(img, lay, at, origin, scale, angle=0.0):
    """Paste a hands3d layer so its `origin` pixel lands on canvas point `at`, scaled and turned (degrees)."""
    w, h = lay.size
    lay = lay.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.BICUBIC)
    ox, oy = origin[0] * scale, origin[1] * scale
    if angle:
        cx, cy = lay.width / 2, lay.height / 2
        lay2 = lay.rotate(angle, Image.BICUBIC, expand=True)
        a = math.radians(angle)
        dx, dy = ox - cx, oy - cy
        ox = lay2.width / 2 + dx * math.cos(a) + dy * math.sin(a)
        oy = lay2.height / 2 - dx * math.sin(a) + dy * math.cos(a)
        lay = lay2
    img.alpha_composite(lay, (int(at[0] - ox), int(at[1] - oy)))


def film_front(t):
    """Shot 1: the slow zoom while he speaks. At T['slap'] a bloodied hand slaps onto the podium's front edge from
    below, clings, and slides off leaving a smear. He does not react."""
    def front(img, cam, pc):
        u = t - T['slap']
        if u < 0:
            return
        X = -0.22
        top = cam.P(*pc.P(X, STAGE_BOX['h'] + PODIUM_BOX['h'], PODIUM_BOX['z1']))
        k = pc.f / pc.depth(PODIUM_BOX['z1']) * cam.z * B.SS
        drop = 0.0 if u < 0.3 else min(1.2, (u - 0.3) ** 1.6 * 1.4)      # clings, then slides down and away
        d = ImageDraw.Draw(img)
        if drop > 0:   # the smear it leaves down the podium's front
            sm = 0.05 * k
            d.polygon([(top[0] - sm, top[1] + 0.03 * k), (top[0] + sm, top[1] + 0.03 * k),
                       (top[0] + sm * 0.8, top[1] + drop * k), (top[0] - sm * 0.9, top[1] + drop * k)], fill=BLOOD_D + (255,))
        if drop < 1.0:
            lay, origin = podium_hand()
            paste_sprite(img, lay, (top[0], top[1] + drop * k), origin, cam.z)
    return shot_front(t, front=front, **peskov_kw(t))


ARM_FROM, ARM_AT = (-0.95, 1.2), (-0.34, 2.3)          # (X, Y) on the backdrop's plane: thrown in, hits here


def film_front_end(t_local):
    """Shot 5: back on him, the camera where the zoom ended. The arm flies in behind him and slaps the backdrop,
    leaving a red splat; it drops away behind his shoulder. "Any more questions?" """
    t = T['s5'] + t_local
    zb = ROOM['z0'] + 0.03

    def behind(img, cam, pc):
        u = t - T['arm_throw']
        hit = T['arm_hit'] - T['arm_throw']
        p = B.Pen(img, cam)
        if t >= T['arm_hit']:   # the splat stays on the backdrop, a drip running down
            cx, cy = pc.P(ARM_AT[0], ARM_AT[1], zb)
            r = pc.f / pc.depth(zb) * 0.11
            run = min(1.0, (t - T['arm_hit']) / 1.2)
            p.poly([(cx - r * 0.12, cy), (cx + r * 0.12, cy), (cx + r * 0.06, cy + r * 2.4 * run), (cx - r * 0.08, cy + r * 2.4 * run)],
                   BLOOD, None)
            splat(p, cx, cy, r, 77, drops=6)
        if u < 0:
            return
        lay, head, cut, fdir = mic_arm()
        if u < hit:            # in flight: an arc in from the left, tumbling
            w = u / hit
            X = ARM_FROM[0] + (ARM_AT[0] - ARM_FROM[0]) * w
            Y = ARM_FROM[1] + (ARM_AT[1] - ARM_FROM[1]) * w + 0.5 * w * (1 - w)
            ang = 200 - 560 * w
        else:                  # after the slap: drops away behind his shoulder
            w = (u - hit) / 0.5
            if w > 1:
                return
            X, Y, ang = ARM_AT[0] + 0.2 * w, ARM_AT[1] - 1.1 * w * w, -360 + 25 * w
        at = cam.P(*pc.P(X, Y, zb))
        cx, cy = lay.size[0] / 2, lay.size[1] / 2
        paste_sprite(img, lay, at, (cx, cy), cam.z, ang)
        # the cut end: a flat red cap with a pale bone in it (cartoon, no anatomy)
    return shot_front(t, zoom=1.32, behind=behind, **peskov_kw(t))


def film_face(t_local):
    """Shot 3, second half: in close on her face as she types frantically (the phone just below the frame, its cold
    light on her face), the hall a blur behind her."""
    from PIL import ImageFilter
    pc = PCam(-0.45, 0.95, 1.2, 1, 900.0, oy=900.0)
    cam = B.Cam(1.0, 540, 960)
    bg = B.canvas(WALL)
    since = T['s3b'] - T['s2'] + t_local
    room(bg, cam, pc, since, chaos=True)
    draw_items(bg, cam, pc, [i for i in chaos_items(pc) if not (i[2] == 'person' and i[3]['kind'] == 'heroine')], since)
    img = bg.filter(ImageFilter.GaussianBlur(14 * B.SS))
    z = 2.9 + 0.6 * F.ease(min(1.0, t_local / 1.5))               # zoom in on her face
    zc = B.Cam(z, 540, 790)
    sp = dict(REPORTER, wide=True, brows='terror', mouth='gasp' if int(t_local * 6) % 3 else 'scream',
              skin=(240, 234, 232), face_splats=[(-38, -110, 8, 7), (44, -60, 6, 8)],
              splats=[(-50, 140, 18, 5)], look=0.5 * math.sin(t_local * 11), seed=3)
    rig = F.Rig(sp)
    sp['arms'] = {sd: rig.pose('hold', side=sd, shape='phone', lift=0.6)[sd] for sd in 'LR'}
    jig = 4 * math.sin(t_local * 40)                            # her shoulders jitter with the typing
    person(img, zc, 540 + jig * 0.3, 960, 1.0, sp, t_local, legs='kneel')
    soft(img, zc, [(380, 800), (700, 800), (720, 1000), (360, 1000)], (150, 200, 255), 0.18, 30)   # the phone's glow
    return img


def film_crawl(t_local):
    """Shot 3, first half: low in the aisle; she crawls to her phone and grabs it."""
    global HEROINE_S3
    keep = HEROINE_S3
    x = keep[0] - 0.35 + 0.3 * min(1.0, t_local / 1.05)
    HEROINE_S3 = (x, keep[1])
    try:
        img = shot_crawl(T['s3'] - T['s2'] + t_local, grab=max(0.0, min(1.0, (t_local - 1.05) / 0.2)))
    finally:
        HEROINE_S3 = keep
    return img


def film_phone(t_local):
    """Shot 4: her phone. She types (the thumb lifting and pressing); a roar right behind her (a shadow falls
    over the phone, her hands shake); a crunch - and blood bursts across the glass."""
    t = T['s4'] + t_local
    tap = int(t_local * 9) % 2 if t < T['crunch'] else 0
    img = shot_phone(t_local, tap=tap)
    if t >= T['roar']:
        u = min(1.0, (t - T['roar']) / 0.5)
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        g = np.linspace(0.55 * u, 0.0, img.size[1])[:, None] * np.ones((1, img.size[0]))
        a = np.clip(g * 255, 0, 255).astype(np.uint8)
        lay.putalpha(Image.fromarray(a))
        img.alpha_composite(lay)
        sh = 6 * B.SS * u * math.sin(t * 70)                       # her hands shaking
        img = img.transform(img.size, Image.AFFINE, (1, 0, sh, 0, 1, sh * 0.5), Image.BICUBIC)
    if t >= T['crunch']:   # the blood hits the glass: big splats growing over three drawings, then running
        u = min(1.0, (t - T['crunch']) / 0.25)
        p = B.Pen(img, B.Cam(1.0, 540, 960))
        for (x, y, r, seed) in ((420, 700, 260, 91), (760, 1020, 200, 92), (300, 1250, 170, 93), (640, 420, 150, 94),
                                (880, 600, 110, 95), (180, 900, 130, 96)):
            splat(p, x, y, r * u, seed, drops=6)
            run = max(0.0, t - T['crunch'] - 0.25) * 260
            if run:
                p.poly([(x - r * 0.1, y), (x + r * 0.1, y), (x + r * 0.07, y + r * 0.6 + run), (x - r * 0.06, y + r * 0.6 + run)],
                       BLOOD, None)
    return img


SHOT_FN = {'front': film_front, 'reverse': lambda tl: shot_reverse(tl), 'crawl': film_crawl, 'face': film_face,
           'phone': film_phone, 'front_end': film_front_end}


def frame_image(t, captions=True, title=True):
    if t >= T['black']:
        return B.canvas((0, 0, 0))
    view, local = shot_at(t)
    img = film_front(t) if view == 'front' else SHOT_FN[view](local)
    if captions:
        c = caption_at(t)
        if c:
            PP.caption(img, c)
    if title and t < 1.0:   # the standard title over the backdrop, gone by 1 s
        title_frame(img, t)
    return img


# ----------------------------------------------------------------------------------------------- sound
rng = np.random.default_rng(66)
place, band = M.place, M.band


def scream(dur, f0, vowel, seed):
    """A human scream: a strained voice gliding up, wavering, rough, through vowel resonances."""
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    tt = np.arange(n) / SR
    wob = np.cumsum(r.standard_normal(n)) / SR * 3
    f = f0 * (1 + 0.3 * np.minimum(1, tt / 0.18)) * (1 + 0.025 * np.sin(2 * np.pi * r.uniform(5, 7) * tt)) * (1 + 0.02 * wob)
    ph = 2 * np.pi * np.cumsum(f) / SR
    src = sum(np.sin(h * ph + r.uniform(0, 6)) / h ** 0.8 for h in range(1, 18))
    src += 0.35 * r.standard_normal(n) * (0.7 + 0.3 * np.sin(ph))
    F = {'a': ((850, 1.0), (1300, 0.7), (2800, 0.4)), 'e': ((550, 1.0), (2000, 0.6), (2800, 0.4)),
         'i': ((380, 0.8), (2500, 0.8), (3300, 0.5))}[vowel]
    y = sum(g * band(src, fc * 0.82, min(fc * 1.2, SR / 2 - 100)) for fc, g in F)
    env = np.minimum(1, tt / 0.05) * np.minimum(1, (dur - tt) / 0.2) * (0.8 + 0.2 * np.sin(2 * np.pi * r.uniform(2, 4) * tt))
    return normal(y * env)


def roar(dur, seed, low=1.0):
    """A zombie's roar: a low, rasping, gurgling voice."""
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = (95 * low) * (1 + 0.15 * np.sin(np.pi * tt / dur)) * (1 + 0.05 * r.standard_normal(n).cumsum() / np.sqrt(np.arange(1, n + 1)))
    ph = 2 * np.pi * np.cumsum(f) / SR
    src = sum(np.sin(h * ph) / h ** 0.6 for h in range(1, 40)) + 0.5 * np.sin(0.5 * ph)
    src *= 0.55 + 0.45 * np.sin(2 * np.pi * 27 * tt)                       # the rattle in the throat
    src += 0.8 * r.standard_normal(n)
    y = band(src, 300, 900) + 0.7 * band(src, 900, 1600) + 0.3 * band(src, 2000, 3500) + 0.4 * onepole_lp(src, 250)
    env = np.minimum(1, tt / 0.08) * np.minimum(1, (dur - tt) / 0.25)
    return normal(y * env)


def thud(f0=70, dur=0.5, crack=0.4):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = f0 + 80 * np.exp(-tt * 20)
    body_ = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
    cr = band(rng.standard_normal(n), 600, 5000) * np.exp(-tt * 40)
    return normal(body_ + crack * normal(cr))


def crash():
    """Chairs going over: a thud and metal legs clattering."""
    out = np.zeros(int(0.9 * SR))
    place(out, thud(90, 0.4, 0.8), 0.0)
    for k in range(5):
        at = 0.06 + 0.07 * k + 0.02 * k * k
        place(out, M.clink() * 0.4, at, 0.6 * 0.7 ** k)
        place(out, thud(260, 0.08, 1.0) * 0.5, at, 0.6 * 0.7 ** k)
    return normal(out)


def splat_snd(size=1.0):
    """A wet splat: a soft, low burst of noise with a few droplets."""
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    x = onepole_lp(rng.standard_normal(n), 1400 * size ** -0.5) * np.exp(-tt * 18) * np.minimum(1, tt / 0.004)
    for k in range(4):
        place(x, band(rng.standard_normal(int(0.02 * SR)), 1500, 5000) * 0.3, 0.04 + 0.05 * k + rng.uniform(0, 0.03))
    return normal(x)


def crunch():
    """Bone breaking: a quick run of sharp cracks over a dull thud."""
    out = np.zeros(int(0.5 * SR))
    place(out, thud(60, 0.4, 0.3), 0.0, 0.8)
    for k in range(7):
        n = int(0.012 * SR)
        c = band(rng.standard_normal(n), 1200, 7000) * np.exp(-np.arange(n) / SR * 400)
        place(out, normal(c), 0.01 + 0.018 * k + rng.uniform(0, 0.008), 0.9 * 0.85 ** k)
    return normal(out)


def slap():
    n = int(0.25 * SR)
    tt = np.arange(n) / SR
    x = band(rng.standard_normal(n), 700, 6000) * np.exp(-tt * 60) + 0.6 * thud(140, 0.25, 0.0)[:n]
    return normal(x)


def shutter():
    out = np.zeros(int(0.12 * SR))
    for at in (0.0, 0.06):
        n = int(0.01 * SR)
        place(out, band(rng.standard_normal(n), 2000, 8000) * np.exp(-np.arange(n) / SR * 600), at)
    return normal(out)


def tap_snd():
    n = int(0.03 * SR)
    tt = np.arange(n) / SR
    return normal(band(rng.standard_normal(n), 1500, 5000) * np.exp(-tt * 300))


def chaos_bed(t0, t1, seed=5):
    """The outbreak heard: screams overlapping (men and women), roars, chairs going over, splats, banging on the
    glass. A dense wall from the first frame of the 180."""
    r = np.random.default_rng(seed)
    n = int((t1 - t0) * SR)
    out = np.zeros(n)
    t = 0.0
    k = 0
    while t < t1 - t0:
        f0 = r.choice([r.uniform(650, 1100), r.uniform(330, 560)])
        place(out, scream(r.uniform(0.6, 1.6), f0, r.choice(['a', 'e', 'i']), seed * 100 + k), t, r.uniform(0.35, 0.8))
        t += r.uniform(0.08, 0.28)
        k += 1
    for a in np.arange(0.3, t1 - t0, 0.7):
        place(out, roar(r.uniform(0.7, 1.3), seed * 200 + int(a * 10), r.uniform(0.8, 1.2)), a + r.uniform(0, 0.3), r.uniform(0.3, 0.55))
    for a in np.arange(0.1, t1 - t0, 0.9):
        place(out, crash(), a + r.uniform(0, 0.4), r.uniform(0.25, 0.45))
    for a in np.arange(0.2, t1 - t0, 0.55):
        place(out, splat_snd(r.uniform(0.7, 1.4)), a + r.uniform(0, 0.3), r.uniform(0.3, 0.5))
    for a in np.arange(0.4, t1 - t0, 0.8):   # fists on the windows
        place(out, thud(110, 0.2, 0.6), a + r.uniform(0, 0.3), 0.18)
    for k in range(3):                        # the wall hits at once on the cut
        place(out, scream(1.4, 700 + 180 * k, 'a', 999 + k), 0.0, 0.8)
    return out


def soundtrack():
    n = int(T['dur'] * SR)
    mix = np.zeros(n)
    # shot 1: the quiet press room: only the photographers' shutters, now and then; the hand's wet slap
    for at in (0.9, 2.6, 2.75, 4.1, 6.3, 7.0):
        place(mix, shutter(), at, 0.06)
    place(mix, slap(), T['slap'], 0.35)
    # from the 180: the outbreak, shot by shot
    bed = chaos_bed(T['s2'], T['black'])
    tt = np.arange(len(bed)) / SR + T['s2']
    g = np.ones(len(bed))
    g[(tt >= T['s3'])] = 0.75                                    # behind her, a touch quieter
    g[(tt >= T['s5'])] = 0.7                                     # under his line
    muff = (tt >= T['s4']) & (tt < T['s5'])
    lp = onepole_lp(onepole_lp(bed, 700), 700)
    bed = np.where(muff, lp * 1.6 * 0.7, bed)                     # muffled while we look at the phone
    k = int(0.01 * SR)
    for edge in (T['s4'], T['s5']):
        i = int((edge - T['s2']) * SR)
        bed[i - k:i + k] *= np.linspace(1, 1, 2 * k)
    place(mix, bed * g, T['s2'])
    # shot 3b and 4: frantic taps on the phone
    for a in np.arange(T['s3b'] + 0.1, T['crunch'], 0.11):
        place(mix, tap_snd(), a + rng.uniform(-0.02, 0.02), 0.12 if a < T['s4'] else 0.2)
    place(mix, roar(1.1, 4242, 0.85), T['roar'], 1.0)            # right behind her, not muffled
    place(mix, crunch(), T['crunch'], 1.0)
    place(mix, splat_snd(1.6), T['crunch'] + 0.03, 0.9)
    # shot 5: the arm slaps the wall
    place(mix, slap(), T['arm_hit'], 0.8)
    place(mix, splat_snd(1.0), T['arm_hit'] + 0.01, 0.5)
    end = int(T['black'] * SR)
    k = int(0.005 * SR)
    # master: about -14 LUFS, peaks no higher than -1 dBTP (measured on the film up to the cut)
    for _ in range(3):
        mix *= 10 ** ((-14.0 - MA.lufs(mix[:end])) / 20)
        mix = M.limiter(mix, -2.6)
    mix[end - k:end] *= np.linspace(1, 0, k)                     # hard cut to black: picture and sound together
    mix[end:] = 0
    return mix


# ------------------------------------------------------------------------------------------- render
def render_frame(args):
    i, size, ss = args
    B.SS = ss
    return np.asarray(frame_image(i / FPS).convert('RGB').resize(size, Image.LANCZOS)).tobytes()


def render(out, size, crf, ss):
    import subprocess
    import imageio_ffmpeg
    from multiprocessing import Pool
    wav = out + '.wav'
    mix = soundtrack()
    print(f'sound: {MA.lufs(mix):.1f} LUFS, peak {MA.true_peak_db(mix):.1f} dBTP', flush=True)
    MA.write_wav(wav, mix)
    n = int(round(T['dur'] * FPS))
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{size[0]}x{size[1]}', '-r', str(FPS), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for k, fr in enumerate(pool.imap(render_frame, [(i, size, ss) for i in range(n)], chunksize=2)):
            p.stdin.write(fr)
            if k % 24 == 0:
                print(f'frame {k}/{n}', flush=True)
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print(f'done: {out} ({os.path.getsize(out) / 1e6:.1f} MB)', flush=True)


def main():
    mode = sys.argv[1]
    if mode == 'sheet':
        stills = sheet(sys.argv[2])
        if len(sys.argv) > 3:
            os.makedirs(sys.argv[3], exist_ok=True)
            for name, im in stills:
                fn = ''.join(c if c.isalnum() else '-' for c in name.lower()).strip('-')
                im.convert('RGB').resize((B.W, B.H), Image.LANCZOS).save(os.path.join(sys.argv[3], fn + '.jpg'), quality=90)
    elif mode == 'part':
        fn = {'front': lambda: title_frame(shot_front(0.3), 0.3), 'front_end': lambda: shot_front(6.8),
              'reverse': lambda: shot_reverse(0.0), 'crawl': lambda: shot_crawl(0.0), 'phone': shot_phone}[sys.argv[2]]
        fn().convert('RGB').resize((B.W // 2, B.H // 2), Image.LANCZOS).save(sys.argv[3])
    elif mode == 'times':
        for k, v in T.items():
            print(f'{k:10s} {v:.2f}')
    elif mode == 'stills':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        B.SS = 1
        for a in sys.argv[3:]:
            frame_image(float(a)).convert('RGB').save(os.path.join(out, f't{a}.jpg'), quality=88)
    elif mode == 'animatic':
        render(sys.argv[2], (540, 960), 26, 1)
    elif mode == 'final':
        render(sys.argv[2], (1080, 1920), 20, 2)


F.guard(B)   # every arm drawn is measured against the rig; a wrong one stops the render (guides/figure-rig.md)

if __name__ == '__main__':
    main()
