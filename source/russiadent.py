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
import filmkit
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
            p.ell(ex + sp.get('look', 0) * 7 + jx, ey - 1 + sp.get('look_y', 0) * 7 + jy, 2.6, 2.6, INK, None)
    if sp.get('socket') and not sp.get('blink'):   # one eye gone: a dark, bloody socket
        sx_ = fx - 4 + (30 if sp['socket'] == 'R' else -30)
        p.ell(sx_, hy - 8, 20, 15, (44, 10, 16), (150, 40, 44), 2.2)
        p.line([(sx_ - 4, hy + 6), (sx_ - 6, hy + 40)], BLOOD, 4)
    if sp.get('scalp'):   # a flap of scalp torn back: a flat red patch with a pale edge of skull
        p.poly(curve([(hx - hw * 0.6, hy - hh * 0.9), (hx - hw * 0.05, hy - hh * 1.12), (hx + hw * 0.3, hy - hh * 0.92),
                      (hx - hw * 0.2, hy - hh * 0.62)], 3), BLOOD, INK, 2.0)
        p.poly(curve([(hx - hw * 0.4, hy - hh * 0.92), (hx - hw * 0.1, hy - hh * 1.02), (hx + hw * 0.1, hy - hh * 0.9),
                      (hx - hw * 0.2, hy - hh * 0.8)], 3), (232, 222, 200), None)
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
    if st in ('peskov', 'zombie', 'buzz', 'combover', 'updo', 'curly'):
        return
    if st in ('matted', 'braid'):   # long hair falling behind the shoulders (a braid down one side)
        if st == 'braid':
            for kk in range(6):
                p.ell(hx + hw * 0.7 + 6 * (kk % 2), hy + 10 + 34 * kk, 18, 22, c, INK, 1.8)
            return
        p.poly(curve([(hx - hw - 16, hy - 40), (hx - hw - 24, hy + 120), (hx - hw - 4, hy + 210), (hx - hw * 0.2, hy + 170),
                      (hx + hw * 0.3, hy + 220), (hx + hw + 20, hy + 150), (hx + hw + 16, hy - 40), (hx, hy - hh - 10)], 4),
               c, INK, 2.4)
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
    if st in ('ponytail', 'braid'):  # pulled tight back from the face, no fringe, a few loose strands (shaken loose)
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
    if st == 'buzz':  # cropped to stubble: a flat cap of short hair, the scalp showing through
        hair = [(hx - hw, hy - 26), (hx - hw * 0.92, hy - hh * 0.74), (hx - hw * 0.45, hy - hh * 1.04), (hx + hw * 0.45, hy - hh * 1.04),
                (hx + hw * 0.92, hy - hh * 0.74), (hx + hw, hy - 26), (hx + hw * 0.86, hy - 44), (hx, hy - hh * 0.84),
                (hx - hw * 0.86, hy - 44)]
        p.poly(curve(hair, 4), B.lt(c, 1.25), INK, 2.2)
        rng = np.random.default_rng(sp.get('seed', 1))
        for _ in range(40):
            a, r = rng.uniform(math.pi * 1.08, math.pi * 1.92), rng.uniform(0.6, 0.98)
            p.ell(hx + hw * 0.95 * r * math.cos(a), hy - 24 + hh * 0.95 * r * math.sin(a), 1.6, 1.6, B.dk(c, 0.9), None)
        return
    if st == 'combover':  # thin hair combed across a bald crown, the sides grown thick
        for sgn in (-1, 1):
            p.poly(curve([(hx + sgn * hw, hy + 10), (hx + sgn * (hw + 8), hy - 44), (hx + sgn * hw * 0.82, hy - hh * 0.72),
                          (hx + sgn * (hw - 14), hy - 30), (hx + sgn * (hw - 10), hy + 6)], 4), c, INK, 2.2)
        for kk in range(5):   # the strands laid across
            y0 = hy - hh * (0.62 + 0.09 * kk)
            p.line([(hx - hw * 0.86, y0 + 10), (hx, y0 - 6), (hx + hw * 0.8, y0 + 4)], c, 3.0)
        return
    if st == 'updo':  # pinned up in a tight bun on top, smooth at the sides
        hair = [(hx - hw - 4, hy - 4), (hx - hw - 6, hy - 50), (hx - hw * 0.72, hy - hh * 1.04), (hx, hy - hh * 1.16),
                (hx + hw * 0.72, hy - hh * 1.04), (hx + hw + 6, hy - 50), (hx + hw + 4, hy - 4), (hx + hw * 0.88, hy - 46),
                (hx + hw * 0.4, hy - hh * 0.78), (hx - hw * 0.4, hy - hh * 0.78), (hx - hw * 0.88, hy - 46)]
        p.poly(curve(hair, 5), c, INK, 2.4)
        p.ell(hx + 6, hy - hh * 1.32, hw * 0.42, hh * 0.24, c, INK, 2.4)
        p.line([(hx - hw * 0.2, hy - hh * 1.3), (hx + hw * 0.3, hy - hh * 1.36)], cd, 1.8)
        return
    if st == 'curly':  # short tight curls, sitting on top of the head (clear of the eyes and brows)
        p.poly(curve(oval(hx, hy - hh * 0.8, hw + 8, hh * 0.42, 18), 3), c, INK, 2.4)
        rng = np.random.default_rng(sp.get('seed', 2))
        for _ in range(22):
            a, r = rng.uniform(math.pi * 1.05, math.pi * 1.95), rng.uniform(0.55, 1.0)
            p.ell(hx + (hw + 4) * r * math.cos(a), hy - hh * 0.8 + hh * 0.4 * r * math.sin(a), 6, 6, cl, cd, 1.2)
        return
    if st == 'matted':  # a zombie woman's long hair, matted into clumps
        hair = [(hx - hw - 10, hy + 30), (hx - hw - 14, hy - 40), (hx - hw * 0.7, hy - hh * 1.04), (hx, hy - hh * 1.12),
                (hx + hw * 0.7, hy - hh * 1.04), (hx + hw + 14, hy - 40), (hx + hw + 10, hy + 30), (hx + hw * 0.84, hy - 10),
                (hx + hw * 0.4, hy - hh * 0.7), (hx - hw * 0.3, hy - hh * 0.6), (hx - hw * 0.84, hy - 10)]
        p.poly(curve(hair, 4), c, INK, 2.4)
        for kk in range(5):
            x0 = hx - hw * 0.7 + kk * hw * 0.35
            p.line([(x0, hy - hh * 0.9), (x0 + 8, hy - hh * 0.5)], cd, 2.4)
        return
    if st == 'zombie':  # thin, matted, patchy hair
        for k in range(7):
            x0 = hx - hw * 0.8 + k * hw * 0.27
            p.line([(x0, hy - hh * 0.9 + abs(k - 3) * 6), (x0 + 6 * math.sin(k * 2.1), hy - hh * 0.5 + 10 * (k % 3))],
                   c, 4.0)
        return
    return _hair_front(p, sp, hx, hy, hw, hh, fx)


def beard(p, sp, hx, hy, hw, hh, fx):
    b = sp.get('beard')
    c = sp.get('beard_c', (90, 70, 56))
    my = hy + sp.get('mouth_y', 60)
    if b == 'walrus':   # a heavy moustache drooping past the corners of the mouth
        p.poly(curve([(fx - 44, my + 16), (fx - 38, my - 10), (fx - 10, my - 20), (fx + 10, my - 20), (fx + 38, my - 10),
                      (fx + 44, my + 16), (fx + 28, my + 2), (fx, my - 4), (fx - 28, my + 2)], 4), c, INK, 2.0)
        return
    if b == 'goatee':   # a short beard on the chin and a thin moustache
        p.poly(curve([(fx - 22, my + 24), (fx + 22, my + 24), (fx + 14, my + 54), (fx - 14, my + 54)], 3), c, INK, 1.8)
        p.poly(curve([(fx - 26, my - 4), (fx, my - 14), (fx + 26, my - 4), (fx, my - 8)], 3), c, INK, 1.6)
        return
    if b != 'moustache':
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
    if sp.get('belly'):  # a heavy man's belly straining the jacket's buttons
        bl = sp['belly']
        jc = sp.get('jacket', B.NAVY)
        p.poly(curve([(-sw * 0.9, 250), (0, 230), (sw * 0.9, 250), (sw * (0.95 + 0.25 * bl), 420), (0, bottom + 40 * bl),
                      (-sw * (0.95 + 0.25 * bl), 420)], 5), jc, INK, 2.4)
        if sp.get('tie'):
            p.poly([(-12, 230), (12, 230), (14, 330), (0, 350), (-14, 330)], sp['tie'], INK, 1.8)
        p.line([(0, 340), (0, bottom + 30 * bl)], B.dk(jc, 0.75), 2.0)
        for yy in (380, 440):
            p.ell(0, yy, 6, 6, B.dk(jc, 0.7), None)
    for side in sp.get('stump', ()):   # an arm torn away at the shoulder: a ragged sleeve, a flat red end
        sgn = -1 if side == 'L' else 1
        x0 = sgn * (sw - 6)
        p.poly(curve([(x0 - sgn * 10, 40), (x0 + sgn * 40, 50), (x0 + sgn * 50, 110), (x0 + sgn * 6, 120)], 3),
               sp.get('jacket', B.NAVY), INK, 2.2)
        p.ell(x0 + sgn * 34, 118, 26, 14, BLOOD, B.dk(BLOOD, 0.6), 1.6, rot=sgn * 0.4)
        p.ell(x0 + sgn * 34, 116, 9, 6, (236, 226, 210), None)
        p.line([(x0 + sgn * 30, 130), (x0 + sgn * 28, 170)], BLOOD, 5)
    if sp.get('gash'):   # a torn-open shirt, a flat red wound beneath (cartoon: no anatomy)
        gx, gy = sp['gash']
        p.poly(curve([(gx - 40, gy - 30), (gx + 30, gy - 40), (gx + 46, gy + 20), (gx - 10, gy + 44), (gx - 44, gy + 10)], 3),
               (150, 24, 34), INK, 2.0)
        p.poly(curve([(gx - 24, gy - 14), (gx + 16, gy - 20), (gx + 26, gy + 10), (gx - 6, gy + 22)], 3), BLOOD, None)
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
    if m == 'wail':  # a howl: an arch on top, corners dragged far down (never a grin), lower teeth, strain lines
        k = 1.0 + 0.06 * math.sin(t * 19 + sp.get('seed', 0))
        pts = curve([(fx - 32, my + 26), (fx - 20, my - 4), (fx, my - 10), (fx + 20, my - 4), (fx + 32, my + 26),
                     (fx + 22, my + 50 * k), (fx - 22, my + 50 * k)], 4)
        p.poly(pts, (62, 16, 24), INK, 2.6)
        p.poly(curve([(fx - 16, my - 1), (fx, my - 6), (fx + 16, my - 1), (fx + 14, my + 5), (fx - 14, my + 5)], 2),
               (246, 244, 238), None)
        p.ell(fx, my + 40 * k, 13, 7, (184, 80, 88), None)
        for sgn in (-1, 1):
            p.line([(fx + sgn * 34, my + 30), (fx + sgn * 40, my + 52)], B.dk(sp['skin'], 0.7), 2.0)
        return
    if m == 'grimace':  # clenched in horror: teeth bared and gritted, the corners dragged down hard
        p.poly([(fx - 34, my + 10), (fx - 20, my - 2), (fx + 20, my - 2), (fx + 34, my + 10), (fx + 22, my + 22), (fx - 22, my + 22)],
               (246, 244, 238), INK, 2.6)
        p.line([(fx - 30, my + 10), (fx + 30, my + 10)], INK, 2.0)
        for kk in range(-2, 3):
            p.line([(fx + kk * 11, my), (fx + kk * 11, my + 20)], (170, 166, 156), 1.4)
        for sgn in (-1, 1):
            p.line([(fx + sgn * 34, my + 10), (fx + sgn * 40, my + 30)], INK, 2.2)
        return
    if m == 'jaw':  # a zombie whose jaw hangs loose: the mouth gaping down to the chin, dark inside
        p.poly(curve([(fx - 24, my - 4), (fx + 24, my - 4), (fx + 30, my + 40), (fx + 8, my + 60), (fx - 20, my + 54)], 3),
               (52, 12, 18), INK, 2.6)
        p.poly([(fx - 20, my - 2), (fx + 20, my - 2), (fx + 18, my + 6), (fx - 18, my + 6)], (214, 208, 180), None)
        p.poly([(fx - 4, my + 50), (fx + 20, my + 52), (fx + 18, my + 58), (fx - 2, my + 56)], (214, 208, 180), None)
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


HAND_R = 26                     # every hand is a plain circle at the end of the arm (props laid over it)


def chand(p, x, y, skin, r=HAND_R):
    p.ell(x, y, r, r, skin, INK, 2.4)


def phone_prop(p, x, y, w=26, h=50, ang=0.0, lit=False):
    """A phone held in a circle hand: a dark slab standing up from (x, y), its back to us."""
    c, s_ = math.cos(ang), math.sin(ang)
    R = lambda u, v: (x + u * c - v * s_, y + u * s_ + v * c)
    p.poly([R(-w, -2 * h), R(w, -2 * h), R(w, 0), R(-w, 0)], (52, 58, 72), INK, 2.2)
    p.ell(*R(w * 0.45, -1.75 * h), w * 0.22, w * 0.22, (16, 16, 20), None)


def gesture_hand(p, el, wr, shape, skin, extra=None, t=0.0):
    d = (wr[0] - el[0], wr[1] - el[1])
    n = math.hypot(*d) or 1.0
    cx, cy = wr[0] + d[0] / n * 12, wr[1] + d[1] / n * 12
    if shape == 'phone':
        phone_prop(p, cx, cy + 10)
    chand(p, cx, cy, skin)


B.gesture_hand = gesture_hand


def no_stump_arms(sp):
    """A zombie missing an arm: that arm is simply not drawn (the torso draws the torn sleeve)."""
    if sp.get('stump') and sp.get('arms'):
        return dict(sp, arms={k: v for k, v in sp['arms'].items() if k not in sp['stump']})
    return sp


def _person(img, cam, x, y, s, sp, t=0.0, legs='stand', phase=0.0, tilt=0.0, flip=1):
    sp = no_stump_arms(sp)
    L = B.Local(cam, x, y, s, flip)
    R = PP.Rot(L, tilt, pivot=(0, 440)) if tilt else L       # a lean bends at the waist: the legs stay planted
    p = B.Pen(img, R)
    hx, hy = sp.get('head_dx', 0.0), -150 + sp.get('head_dy', 0.0)
    if not sp.get('nohead'):
        B.hair_back(p, sp, hx, hy, sp.get('hw', 72), sp.get('hh', 88))
    legs_draw(img, B.Pen(img, L), sp, legs, phase)
    B.arms(img, p, sp, t, front=False)
    B.torso(img, p, sp, t)
    B.arms(img, p, sp, t, front=True)
    if not sp.get('nohead'):
        B.head(img, p, sp, t, hx, hy)
    if not sp.get('nohead'):
        for (sx, sy, r, seed) in sp.get('face_splats', ()):
            splat(p, sx, sy, r, seed, drops=2)
    return p


def person_back(img, cam, x, y, s, sp, t=0.0, legs='stand', phase=0.0, tilt=0.0):
    """The same person seen from behind (running away, pulling at a door): no face, the hair covering the head."""
    sp = no_stump_arms(sp)
    L = B.Local(cam, x, y, s)
    R = PP.Rot(L, tilt, pivot=(0, 440)) if tilt else L       # bends at the waist: the legs stay planted
    p = B.Pen(img, R)
    sw, bottom = sp.get('shoulders', 150), sp.get('bottom', 560)
    legs_draw(img, B.Pen(img, L), dict(sp, skirt=None) if sp.get('skirt') else sp, legs, phase)
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
                burst = chaos and zw == WIN_Z
                broken = burst and t >= WIN_BURST
                if chaos:   # the tide outside, several deep, pressed against the glass (the burst window's front
                    #         row are cast members, drawn with everyone else)
                    crowd = through(pc, X, zw, 1.4, 40 + 9 * i)
                    outside(img, cam, pc, pane, crowd[3:] if burst else crowd, t, glass_x=None if burst else X)
                for (ya, yb) in ((0.55, 2.2), (2.2, 2.7)):         # a glint on each light of glass that is still there
                    if broken and ya < 2.2:
                        continue
                    for zz in (zw - 0.45, zw + 0.25):
                        soft(img, cam, [pc.P(X, ya + 0.15, zz), pc.P(X, ya + 0.15, zz + 0.12), pc.P(X, yb - 0.1, zz + 0.32),
                                        pc.P(X, yb - 0.1, zz + 0.2)], (255, 255, 255), 0.18, 3)
                if burst and not broken:      # struck from outside: the cracks spreading
                    cracks(p, pc, X, zw - 0.2, 1.45, t / WIN_BURST, 5)
                if broken:                    # the lower lights gone: jagged teeth of glass left in the frame
                    cracks(p, pc, X, zw + 0.3, 2.5, 1.0, 6, reach=0.3)
                    rng_ = np.random.default_rng(12)
                    for a_, b_ in ((zw - 0.7, zw), (zw, zw + 0.7)):
                        for q_ in range(4):
                            z_a, z_b = a_ + (b_ - a_) * q_ / 4, a_ + (b_ - a_) * (q_ + 1) / 4
                            zm = (z_a + z_b) / 2 + rng_.uniform(-0.05, 0.05)
                            quad(p, pc, [(X, 0.55, z_a), (X, 0.55, z_b), (X, 0.55 + rng_.uniform(0.05, 0.22), zm)], (226, 240, 248),
                                 INK, 1.4)
                            quad(p, pc, [(X, 2.2, z_a), (X, 2.2, z_b), (X, 2.2 - rng_.uniform(0.05, 0.3), zm)], (226, 240, 248),
                                 INK, 1.4)
                    for z_ in (zw - 0.7, zw + 0.7):
                        sg = 1 if z_ < zw else -1
                        for q_ in range(4):
                            y_a, y_b = 0.55 + 1.65 * q_ / 4, 0.55 + 1.65 * (q_ + 1) / 4
                            quad(p, pc, [(X, y_a, z_), (X, y_b, z_), (X, (y_a + y_b) / 2, z_ + sg * rng_.uniform(0.04, 0.18))],
                                 (226, 240, 248), INK, 1.4)
                quad(p, pc, [(X, 2.7, zw - 0.7), (X, 2.7, zw + 0.7), (X, 3.1, zw + 0.7), (X, 3.1, zw - 0.7)], NET, INK, 1.6)
                for k in range(1, 6):  # net-curtain folds
                    seg(p, pc, (X, 2.7, zw - 0.7 + k * 0.233), (X, 3.1, zw - 0.7 + k * 0.233), (214, 212, 204), 1.6)
                quad(p, pc, pane, None, INK, 2.4)
                seg(p, pc, (X, 3.1, zw), (X, 2.2 if broken else 0.55, zw), INK, 2.0)
                seg(p, pc, (X, 2.2, zw - 0.7), (X, 2.2, zw + 0.7), INK, 2.0)
                if broken:
                    shards(img, cam, pc, X, zw, t)
    # the stage (a low platform at the front)
    st = STAGE_BOX
    quad(p, pc, [(st['x0'], st['h'], st['z0']), (st['x1'], st['h'], st['z0']), (st['x1'], st['h'], st['z1']),
                 (st['x0'], st['h'], st['z1'])], STAGE, INK, 2.0)
    quad(p, pc, [(st['x0'], 0, st['z1']), (st['x1'], 0, st['z1']), (st['x1'], st['h'], st['z1']), (st['x0'], st['h'], st['z1'])],
         B.dk(STAGE, 0.8), INK, 2.0)


def outside(img, cam, pc, opening, crowd, t, glass_x=None, sp_for=None):
    """Zombies beyond an opening (a window, a doorway), seen only through it: drawn on their own layer and masked
    by the opening. crowd: [(X, Z, seed)] in the plan, beyond the wall. glass_x: the opening is glazed, at this X:
    the front row's hands are pressed to it and leave smeared prints exactly where they touch."""
    q = clipz(pc, opening)
    if len(q) < 3:
        return
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    hands = []
    for X, Z, seed in sorted(crowd, key=lambda c: -pc.depth(c[1], c[0])):
        sp = dict((sp_for or {}).get(seed) or zombie_base(seed, press=(seed % 2 == 0)))
        rig = F.Rig(sp)
        sway = 20 * math.sin(t * 5 + seed)
        tg = {'L': (-190, -170 + sway), 'R': (200, -150 - sway)}
        sp['arms'] = {side: rig.arm(side, tg[side], 'palm', 'out', strict=False) for side in tg}
        sc = pc.scale(Z, X)
        nx, ny = pc.P(X, F.SOLE_Y / UPM, Z)
        tilt = 0.05 * math.sin(t * 3 + seed)
        person(lay, cam, nx, ny, sc, sp, t, tilt=tilt)
        if glass_x is not None and abs(X - glass_x) < 0.45:    # the front row: palms flat on the glass
            Rr = PP.Rot(B.Local(cam, nx, ny, sc), tilt, pivot=(0, 440))
            for side, (hx, hy) in tg.items():
                if side not in sp.get('stump', ()):
                    px, py = Rr.P(hx, hy - 20)
                    hands.append((px, py, Rr.S(30), seed * 7 + len(hands)))
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).polygon([cam.P(*pt) for pt in q], fill=255)
    _masked(img, lay, mask)
    if hands:
        _masked(img, glass_prints(img, hands, t), mask)


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


CLUTTER = [('paper', -0.55, 2.05, 0.3), ('paper', -0.3, 2.3, -0.5), ('paper', 0.1, 2.15, 0.9), ('notepad', -0.75, 2.35, 0.2),
           ('mic', -0.15, 2.5, 0.6), ('shoe', 0.3, 2.45, -0.3), ('paper', -1.5, 1.75, 0.4)]


def floor_clutter(img, cam, pc):
    """What the stampede left on the floor at the front: papers, a notepad, a dropped microphone, a lost shoe, a
    smear of blood. All flat on the floor, in the plan."""
    p = B.Pen(img, cam)
    for kind, X, Z, a in CLUTTER:
        ca, sa = math.cos(a), math.sin(a)
        R = lambda u, v: pc.P(X + u * ca - v * sa, 0.002, Z + u * sa + v * ca)
        if kind == 'paper':
            p.poly([R(-0.105, -0.15), R(0.105, -0.15), R(0.105, 0.15), R(-0.105, 0.15)], (248, 248, 244), INK, 1.6)
            for k in range(4):
                p.line([R(-0.07, -0.1 + 0.05 * k), R(0.07, -0.1 + 0.05 * k)], (190, 190, 196), 1.4)
        elif kind == 'notepad':
            p.poly([R(-0.08, -0.11), R(0.08, -0.11), R(0.08, 0.11), R(-0.08, 0.11)], (238, 214, 90), INK, 1.8)
            p.line([R(-0.08, -0.09), R(0.08, -0.09)], (90, 90, 100), 2.4)
        elif kind == 'mic':
            p.line([R(-0.1, 0), R(0.08, 0)], (30, 30, 34), 9)
            p.ell(*R(0.12, 0), 12, 9, (110, 114, 120), INK, 1.6)
            p.poly([R(-0.04, -0.03), R(0.0, -0.03), R(0.0, 0.03), R(-0.04, 0.03)], (40, 120, 200), INK, 1.4)
        elif kind == 'shoe':
            p.poly(curve([R(-0.13, -0.04), R(0.12, -0.05), R(0.14, 0.03), R(-0.12, 0.05)], 3), (30, 28, 30), INK, 1.8)
        elif kind == 'smear':
            p.poly(curve([R(-0.35, -0.03), R(0.3, -0.06), R(0.32, 0.05), R(-0.3, 0.07)], 3), BLOOD_D, None)


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
    return PCam(0.3, 1.55, -0.15, 1, 1050.0, oy=760.0, yaw=0.42), B.Cam(1.0, 540, 960)


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
    # a grabbing zombie's head and arms are drawn with its victim; if the victim isn't in this shot, it lunges alone
    shown = set()
    for z, x, kind, a in items:
        if kind == 'person' and a['act'] == 'tackled':
            X, Z = where(a, t)
            if pc.depth(Z, X) >= 0.6:
                shown.add(a.get('pair'))
    items = [(z, x, kind, dict(a, act='lunge_l') if kind == 'person' and a['act'] == 'tackle' and a.get('pair') not in shown
              else a) for z, x, kind, a in items]
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
    floor_clutter(img, cam, pc)
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


# The press corps, each designed on purpose (best-practice: no two people alike): build, face, hair, clothes and
# their own kind of terror. Muted Russian office palette: greys, browns, olive, burgundy; wide ties; dyed hair.
CAST = {
    0: dict(sex='m', build=(150, 0.0), jaw='square', hair='buzz', hair_c=(90, 80, 70), jacket=(72, 74, 80), tie=(110, 40, 40),
            fear='scream', note='running for the back doors'),
    1: dict(sex='m', build=(176, 0.7), jaw='round', hair='combover', hair_c=(120, 110, 100), beard='walrus', beard_c=(110, 96, 84),
            jacket=(104, 84, 64), tie=(60, 70, 50), fear='wail', glasses=True, note='beating a zombie off with a tripod'),
    2: dict(sex='m', build=(158, 0.0), jaw='long', hair='side', hair_c=(60, 48, 40), grey=(150, 146, 140), jacket=(66, 86, 66),
            tie=(150, 120, 60), fear='grimace', note='the chair: one hard hit'),
    3: dict(sex='f', build=(132, 0.0), jaw='soft', hair='bob', hair_c=(150, 56, 40), jacket=(96, 70, 110), skirt=(60, 60, 70),
            fear='scream', note='filming it all on her phone'),
    4: dict(sex='m', build=(156, 0.0), jaw='square', hair='crop', hair_c=(40, 34, 30), beard='goatee', beard_c=(44, 36, 32),
            jacket=(132, 108, 80), tie=None, fear='scream', note='grabbed and bitten, front right'),
    5: dict(sex='m', build=(144, 0.0), jaw='long', hair='bald', hair_c=(110, 96, 90), jacket=(54, 60, 84), tie=(70, 90, 140),
            fear='wail', glasses=True, note='fleeing down the centre'),
    6: dict(sex='f', build=(134, 0.0), jaw='soft', hair='updo', hair_c=(214, 200, 150), jacket=(176, 44, 52), trousers=(196, 172, 132),
            fear='grimace', note='hiding: head under a chair'),
    8: dict(sex='m', build=(166, 0.4), jaw='round', hair='curly', hair_c=(80, 60, 44), beard='moustache', beard_c=(70, 52, 40),
            jacket=(84, 84, 90), tie=(90, 30, 60), fear='grimace', note='shoving the side door shut'),
    9: dict(sex='f', build=(136, 0.0), jaw='soft', hair='braid', hair_c=(52, 40, 34), jacket=(70, 100, 120), skirt=(90, 60, 50),
            fear='wail', note='grabbed mid-hall, the one our reporter crawls past'),
}


def reporter_base(k, **kw):
    c = CAST[k]
    women = c['sex'] == 'f'
    sk = SKINS[k % len(SKINS)]
    pale = tuple(int(0.55 * v + 0.45 * w) for v, w in zip(sk, (232, 230, 228)))   # drained of colour
    sw, belly = c['build']
    sp = dict(name=f"reporter {k} ({c['note']})", skin=pale, hw=(64 if women else 70) + 0.08 * (sw - 150),
              hh=86 if women else 90 + (4 if c['jaw'] == 'long' else 0), jaw=c['jaw'], hair=c['hair'], hair_c=c['hair_c'],
              grey=c.get('grey'), outfit='blouse' if women else 'suit', jacket=c['jacket'],
              shirt=(236, 236, 240) if not women else (230, 222, 214), tie=c.get('tie'),
              trousers=c.get('trousers', B.dk(c['jacket'], 0.8)), shoulders=sw, belly=belly, full=True, pose='custom',
              press=True, lanyard_c=PRESS_C[k % 5], wide=True, brows='terror', mouth=c['fear'], lashes=women, seed=k,
              beard=c.get('beard'), beard_c=c.get('beard_c'), glasses=c.get('glasses', False), age=k in (1, 2, 8),
              nose='long' if k in (2, 5, 8) else 'line')
    if c.get('skirt'):
        sp.update(skirt=c['skirt'], tights=(200, 180, 170))
    sp.update(kw)
    return sp


# The zombies: men and women, in different states of falling apart (flat cartoon damage only: no anatomy).
ZCAST = {
    0: dict(sex='m', hair='zombie', jacket=(80, 84, 96), dmg=dict(scalp=True)),
    1: dict(sex='f', hair='matted', hair_c=(120, 96, 60), jacket=(110, 80, 90), skirt=(70, 60, 64), dmg=dict(socket='L')),
    4: dict(sex='m', hair='zombie', jacket=(96, 86, 70), dmg=dict(stump=('L',))),
    5: dict(sex='m', hair='zombie', jacket=(96, 92, 112), dmg=dict(mouth='jaw', gash=(40, 300))),   # the chair's zombie
    6: dict(sex='m', hair='zombie', jacket=(64, 70, 84), dmg=dict(scalp=True)),                    # the front-right biter
    8: dict(sex='f', hair='matted', hair_c=(60, 50, 44), jacket=(120, 100, 80), skirt=(80, 70, 60), dmg=dict(gash=(-30, 260))),
    9: dict(sex='m', hair='zombie', jacket=(90, 90, 96), dmg=dict(mouth='jaw')),
    10: dict(sex='f', hair='matted', hair_c=(170, 140, 90), jacket=(80, 96, 110), skirt=(60, 64, 80), dmg=dict()),
    11: dict(sex='m', hair='zombie', jacket=(100, 70, 64), dmg=dict(stump=('R',))),
    12: dict(sex='f', hair='matted', hair_c=(90, 50, 40), jacket=(96, 96, 80), skirt=(70, 70, 60), dmg=dict(socket='R')),
    13: dict(sex='m', hair='zombie', jacket=(76, 66, 60), dmg=dict(gash=(20, 220))),
    14: dict(sex='m', hair='zombie', jacket=(60, 76, 70), dmg=dict(mouth='jaw')),
    15: dict(sex='f', hair='matted', hair_c=(40, 34, 30), jacket=(110, 110, 120), skirt=(50, 54, 60), dmg=dict(scalp=True)),
    16: dict(sex='m', hair='zombie', jacket=(86, 76, 90), dmg=dict(stump=('L',))),
    17: dict(sex='f', hair='matted', hair_c=(150, 120, 70), jacket=(100, 84, 70), skirt=(64, 60, 56), dmg=dict(gash=(0, 280))),
    18: dict(sex='m', hair='zombie', jacket=(70, 70, 76), dmg=dict(socket='L', scalp=True)),       # the one after her
    20: dict(sex='f', hair='matted', hair_c=(196, 170, 120), jacket=(122, 92, 60), skirt=(70, 56, 50), dmg=dict(socket='R')),
    21: dict(sex='m', hair='zombie', jacket=(56, 64, 60), dmg=dict(mouth='jaw', stump=('R',))),
    19: dict(sex='f', hair='matted', hair_c=(70, 56, 44), jacket=(90, 70, 70), skirt=(60, 56, 60), dmg=dict()),  # the mid biter
}


def zombie_base(k, **kw):
    """A zombie: from the cast list if it has a part, otherwise one of the crowd at the windows and doors (varied
    by its number: men and women, different damage)."""
    c = ZCAST.get(k)
    if c is None:
        r = np.random.default_rng(k)
        f = r.random() < 0.45
        c = dict(sex='f' if f else 'm', hair='matted' if f else 'zombie',
                 hair_c=tuple(int(v) for v in r.integers(40, 160, 3)), jacket=tuple(int(v) for v in r.integers(60, 120, 3)),
                 skirt=(70, 64, 60) if f else None,
                 dmg=[dict(), dict(scalp=True), dict(socket='L'), dict(mouth='jaw'), dict(gash=(0, 260))][k % 5])
    women = c['sex'] == 'f'
    sp = dict(ZOMBIE, name=f'zombie {k}', seed=k + 10, hw=(64 if women else 70) - 2 * (k % 3), hh=86 if women else 90,
              jaw='soft' if women else ['square', 'round', 'long'][k % 3], hair=c['hair'],
              hair_c=c.get('hair_c', (70, 66, 60)), jacket=c['jacket'], outfit='blouse' if women else 'suit',
              shoulders=136 if women else 150 + 8 * (k % 3), press=(k % 3 != 2), lanyard_c=PRESS_C[(k + 2) % 5],
              skin=[ZSKIN, (148, 166, 140), (162, 172, 132), (170, 176, 150)][k % 4], lashes=women)
    if c.get('skirt'):
        sp.update(skirt=c['skirt'], tights=(120, 130, 110))
    d = c['dmg']
    if 'mouth' in d:
        sp['mouth'] = d['mouth']
    for key in ('scalp', 'socket', 'gash'):
        if key in d:
            sp[key] = d[key]
    if 'stump' in d:
        sp['stump'] = d['stump']
    sp.update(kw)
    return sp


def check_outfits():
    """No two people in the hall look alike (best-practice 1.3): each person's look is unique."""
    seen = {}
    for w in CROWD:
        sp = reporter_base(w['k']) if w['kind'] == 'person' else zombie_base(w['k']) if w['kind'] == 'zombie' else REPORTER
        key = (w['kind'], sp.get('hair'), sp.get('hair_c'), sp.get('jacket'), sp.get('beard'), sp.get('glasses'))
        if key in seen:
            raise ValueError(f"check: {w['kind']} {w['k']} is dressed exactly like {seen[key]}")
        seen[key] = f"{w['kind']} {w['k']}"


# who is where in shot 2, and what each is doing (every background person has one clear action). Plan units.
CROWD = [
    # the back: zombies jammed in the doorways and coming through
    dict(kind='zombie', k=0, x=-0.45, z=8.5, act='door'),
    dict(kind='zombie', k=1, x=0.5, z=8.55, act='door'),
    dict(kind='zombie', k=9, x=-0.2, z=7.95, act='lunge'),
    dict(kind='zombie', k=10, x=0.75, z=8.1, act='lunge_l', v=(0.1, -0.2), pair='doors'),
    dict(kind='person', k=0, x=0.7, z=6.4, act='run_away', v=(0.0, 0.8), until=2.0, pair='doors'),   # straight into them
    # the side door (back right of the frame): pouring in; a reporter shoving the door against them
    dict(kind='zombie', k=11, x=-5.0, z=7.7, act='lunge_l', v=(0.5, -0.2), until=1.0, pair='side'),
    dict(kind='zombie', k=12, x=-4.7, z=8.3, act='lunge_l', v=(0.4, -0.3), until=1.5),
    dict(kind='zombie', k=15, x=-3.5, z=8.3, act='lunge', v=(0.0, -0.15)),
    dict(kind='person', k=8, x=-4.2, z=7.05, act='door_pull', pair='side'),
    # the riser: a reporter beating a zombie off with a tripod
    dict(kind='person', k=1, x=-2.0, z=7.9, act='tripod', pair='riser'),
    dict(kind='zombie', k=4, x=-1.55, z=7.75, act='lunge_r', v=(0.0, 0.0), pair='riser'),
    dict(kind='zombie', k=14, x=3.0, z=7.2, act='lunge_r'),
    dict(kind='zombie', k=13, x=-3.0, z=6.3, act='lunge'),
    dict(kind='zombie', k=16, x=-1.3, z=6.0, act='lunge_r', v=(-0.1, -0.25), until=3.5),
    # middle: filming it all, backing away from a zombie
    dict(kind='person', k=3, x=-2.45, z=4.85, act='phone', v=(0.0, 0.0)),
    dict(kind='zombie', k=8, x=-3.6, z=5.2, act='lunge_l'),
    dict(kind='zombie', k=17, x=-3.9, z=3.4, act='lunge'),
    # a reporter fleeing towards us down the centre, stopping short of the front row
    dict(kind='person', k=5, x=-0.1, z=6.4, act='run', v=(0.0, -1.0), until=1.6),
    # a second attack, on our reporter's path (she crawls past it in shot 3)
    dict(kind='person', k=9, x=-0.6, z=4.7, act='tackled', pair='mid'),     # seen in shots 2 and 3 and the close-up
    dict(kind='zombie', k=19, x=-0.83, z=4.93, act='tackle', pair='mid'),
    # the zombie lurching after our reporter
    dict(kind='zombie', k=18, x=-3.0, z=3.9, act='stalk', v=(0.35, 0.0), dir=-1, until=7.0, z2=None),
    # hiding: head under a chair, the rest of her very much not hidden (seat 1.2)
    dict(kind='person', k=6, x=-3.1, z=3.32, act='hide'),
    # our reporter, crawling (shot 3 follows her)
    dict(kind='heroine', k=0, x=-1.85, z=3.25, act='crawl', v=(0.35, 0.0), until=5.1),   # until: 3 + 1.5 + 0.6 s
    # the front left corner: bringing a chair down on a zombie
    # (it comes round from behind him; one hard hit at CHAIR_HIT sends it flying onto its back)
    dict(kind='person', k=2, x=0.17, z=2.1, act='chair', pair='front_l'),
    dict(kind='zombie', k=5, x=0.12, z=2.6, act='chair_z', pair='front_l',
         path=[(0.0, 0.12, 2.6), (1.0, -0.25, 2.3), (1.5, -0.25, 2.3), (1.9, -0.25, 2.75)]),
    # the window nearest the back bursts in at WIN_BURST: one topples over the sill into a heap and drags itself
    # up; another climbs in after it, a knee on the sill
    dict(kind='zombie', k=20, x=-5.0, z=5.85, act='window_fall', path=[(0.0, -5.0, 5.85), (1.8, -5.0, 5.85), (3.0, -4.8, 5.85),
                                                                      (8.0, -3.9, 5.75)]),
    dict(kind='zombie', k=21, x=-5.55, z=6.4, act='window_climb', path=[(0.0, -5.55, 6.4), (3.0, -5.3, 6.4)]),
    # the front right: a zombie has a reporter from behind, biting into his neck; he strains to escape
    dict(kind='person', k=4, x=-1.1, z=1.95, act='tackled', v=(-0.04, 0.1), until=3.0, pair='front_r'),
    dict(kind='zombie', k=6, x=-1.3, z=2.2, act='tackle', v=(-0.04, 0.1), until=3.0, pair='front_r'),
]
PEOPLE_R = 0.24                 # each person's footprint on the floor plan (metres)


def where(who, t):
    """A person's place on the plan at t seconds after the 180: a steady walk (v, until), or keyframes
    (path: [(t, X, Z), ...], eased between keys)."""
    if 'path' in who:
        ks = who['path']
        if t <= ks[0][0]:
            return ks[0][1], ks[0][2]
        for (t0, x0, z0), (t1, x1, z1) in zip(ks, ks[1:]):
            if t <= t1:
                u = F.ease((t - t0) / (t1 - t0)) if t1 > t0 else 1.0
                return x0 + (x1 - x0) * u, z0 + (z1 - z0) * u
        return ks[-1][1], ks[-1][2]
    vx, vz = who.get('v', (0.0, -0.25) if who['act'].startswith('lunge') else (0.0, 0.0))   # zombies keep coming
    tm = min(t, who.get('until', 99.0))
    return who['x'] + vx * tm, who['z'] + vz * tm


def check_crowd(t1=8.0):
    """No two people ever overlap on the floor plan as they move (except a pair meant to touch: an attacker and
    their victim). Stops the render with the names and the moment (best-practice 1.3)."""
    for i in range(int(t1 * FPS)):
        t = i / FPS
        pos = [(w, where(w, t)) for w in CROWD]
        for a in range(len(pos)):
            for b in range(a + 1, len(pos)):
                (wa, pa), (wb, pb) = pos[a], pos[b]
                if wa.get('pair') and wa.get('pair') == wb.get('pair'):
                    continue
                d = math.dist(pa, pb)
                if d < 2 * PEOPLE_R:
                    raise ValueError(f"check: at {t:.2f} s after the 180, {wa['kind']} {wa['k']} ({wa['act']}) and "
                                     f"{wb['kind']} {wb['k']} ({wb['act']}) overlap ({d:.2f} m apart)")


HIDE_SEAT = (1, 0)              # the chair the hider is under (drawn with her)
TRIPOD_TAKEN = 1                # the tripod in the fighter's hands
FLOOR_SPLATS = [(0.3, 1.75, 0.1, 61), (-0.6, 3.9, 0.12, 62), (0.3, 6.2, 0.14, 63), (-2.8, 6.0, 0.12, 64), (1.6, 3.3, 0.1, 65)]
AIR_DROPS = [(0.45, 1.75, 1.95, 0.026, 71), (0.25, 1.95, 2.0, 0.02, 72), (0.7, 1.55, 1.9, 0.018, 73), (0.15, 1.6, 1.9, 0.016, 74)]


PENDING = {}                    # a grabbing zombie's arms and head, drawn over its victim


def grab_and_draw_forearm(p, el, wr, colr, w=30):
    d = (wr[0] - el[0], wr[1] - el[1])
    n = math.hypot(*d) or 1
    nx, ny = -d[1] / n, d[0] / n
    p.poly([(el[0] + nx * w, el[1] + ny * w), (wr[0] + nx * w * 0.75, wr[1] + ny * w * 0.75),
            (wr[0] - nx * w * 0.75, wr[1] - ny * w * 0.75), (el[0] - nx * w, el[1] - ny * w)], colr, INK, 2.6)
    p.ell(el[0], el[1], w, w, colr, INK, 2.6)


def grip_and_bite(img, Rv, zsp, t, seed):
    """Drawn in the victim's own (leaning) frame, over him: the zombie's forearms wrapped round his chest from behind,
    its grey-green hands clamped on his front; its head buried in the side of his neck, biting, blood spurting."""
    p = B.Pen(img, Rv)
    jc = zsp.get('jacket', (80, 84, 96))
    # forearms come round his sides (elbows just outside his body) to hands clamped on his chest
    for el, wr, rot in (((-170, 250), (-30, 200), 0.3), ((175, 120), (60, 150), -0.4)):
        grab_and_draw_forearm(p, el, wr, jc)
        chand(p, wr[0] + (12 if el[0] < 0 else -12), wr[1], zsp['skin'], 30)
    # its head, mouth on the right side of his neck, jerking as it bites
    bite = 0.5 + 0.5 * math.sin(t * 12)
    hp = B.Pen(img, PP.Rot(Rv, 0.0, pivot=(0, 0)))
    hl = _Offset(Rv, 135 + 6 * bite, -5 + 8 * bite, -0.5)
    hpen = B.Pen(img, hl)
    zsp = dict(zsp, mouth='snarl', tilt=0.0)
    B.hair_back(hpen, zsp, 0, -150, zsp.get('hw', 70), zsp.get('hh', 90))
    B.head(img, hpen, zsp, t, 0, -150)
    # the bite: blood spurting out in arcs from where its mouth meets his neck
    for j in range(5):
        u = (t * 2.5 + j / 5) % 1.0
        a = math.radians(-120 + 25 * j)
        x = 85 + math.cos(a) * 140 * u
        y = -25 + math.sin(a) * 140 * u + 160 * u * u
        p.ell(x, y, 9 * (1 - 0.5 * u), 9 * (1 - 0.5 * u), BLOOD, None)
    splat(p, 80, 5, 22, seed + 70, drops=3)


class _Offset:
    """A frame placed inside another: origin at (ox, oy) of the parent, turned by a (the zombie's head on the neck)."""
    def __init__(self, parent, ox, oy, a):
        self.parent, self.ox, self.oy, self.c, self.sn = parent, ox, oy, math.cos(a), math.sin(a)
        self.s, self.cam = parent.s, getattr(parent, 'cam', None)

    def P(self, x, y):
        y = y + 90                              # its mouth (90 above the neck base in its own frame) on the point
        return self.parent.P(self.ox + x * self.c - y * self.sn, self.oy + x * self.sn + y * self.c)

    def S(self, v):
        return self.parent.S(v)


def hider(img, cam, x, y, s, sp, t):
    """Seen from behind: knees on the floor, bottom in the air, her shoulders, arms and head jammed under the chair's
    seat; only her ponytail and clasped hands show beneath it. Shaking all over. (x, y): the floor under her knees."""
    sh = 4 * math.sin(t * 38)
    L = B.Local(cam, x + sh * s, y, s)
    p = B.Pen(img, L)
    tc = sp.get('trousers', (56, 58, 66)) if not sp.get('skirt') else sp['tights']
    # under the seat (furthest away): her hands over her head and the end of her ponytail
    p.poly(curve([(40, -330), (110, -360), (150, -330), (120, -310)], 3), sp['hair_c'], INK, 2.0)
    for dx in (-40, 20):
        p.ell(dx, -330, 26, 20, sp['skin'], INK, 2.0)
    # her back sloping away under the seat, then the bottom up in the air, legs folded, soles towards us
    p.poly(curve([(-130, -320), (130, -320), (150, -250), (-150, -250)], 3), sp['jacket'], INK, 2.4)
    for sgn in (-1, 1):
        p.poly([(sgn * 30, -260), (sgn * 140, -260), (sgn * 130, -20), (sgn * 40, -20)], tc, INK, 2.4)
        p.poly(curve([(sgn * 50, -10), (sgn * 130, -10), (sgn * 140, 30), (sgn * 40, 30)], 3), (60, 56, 60), INK, 2.2)
        p.ell(sgn * 90, 18, 40, 14, (150, 140, 140), None)              # the soles of her shoes
    bot = sp.get('skirt') or sp.get('trousers', (56, 58, 66))
    p.poly(curve([(-160, -230), (-150, -330), (0, -350), (150, -330), (160, -230), (0, -200)], 4), bot, INK, 2.6)
    p.line([(0, -345), (0, -215)], B.dk(bot, 0.8), 2.0)


def ik2(sh, target, l1, l2, bend=1):
    """Two-bone arm from shoulder to target (lengths l1, l2): the elbow on the `bend` side. Returns (elbow, hand),
    the hand pulled back onto the arm's reach if the target is too far."""
    dx, dy = target[0] - sh[0], target[1] - sh[1]
    d = max(1e-6, math.hypot(dx, dy))
    if d > l1 + l2 - 1:
        dx, dy, d = dx * (l1 + l2 - 1) / d, dy * (l1 + l2 - 1) / d, l1 + l2 - 1
    a = math.acos(max(-1.0, min(1.0, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d))))
    base = math.atan2(dy, dx) + bend * a
    el = (sh[0] + l1 * math.cos(base), sh[1] + l1 * math.sin(base))
    return el, (sh[0] + dx, sh[1] + dy)


def swing(t, period=1.1, phase=0.0):
    """A strike, over and over: a fast blow down (the first quarter) and a slower lift back up (0 = raised, 1 = struck)."""
    u = (t / period + phase) % 1.0
    return F.ease(u / 0.25) if u < 0.25 else 1.0 - F.ease((u - 0.25) / 0.75)


def lerp2(a, b, u):
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)


def crowd_person(img, cam, pc, who, t):
    """Everyone in the outbreak, each with one clear action, and always moving (never a frozen pose)."""
    k, act, X, z = who['k'], who['act'], who['x'], who['z']
    X, z = where(who, t)                      # t: seconds since the 180 (the same clock in shots 2 and 3)
    if pc.depth(z, X) < 0.6:
        return
    y0 = 0.3 if 7.6 <= z <= 8.6 and any(a <= X <= b for a, b in RISERS) else 0.0
    s = pc.scale(z, X)
    nx, ny = pc.P(X, y0 + F.SOLE_Y / UPM, z)
    fy = pc.P(X, y0, z)[1]
    ph = t * 9 + k
    w1, w2 = math.sin(t * 7.3 + k * 1.7), math.sin(t * 11.1 + k * 2.3)     # two unrelated wobbles per person
    if who['kind'] == 'heroine':
        x, y = pc.P(X, 0.0, z)
        st = HEROINE.get('step', t * 7)
        ph = HEROINE.get('phone_plan')
        loc = None
        if ph is not None:
            wx, wy = pc.P(ph[0], 0.0, ph[1])
            loc = ((wx - x) / s, (wy - y) / s)
        reporter_crawl(img, cam, x, y, s, t, step=st, phone=loc, pick=HEROINE.get('pick', 0.0),
                       hold=HEROINE.get('hold', False), look=HEROINE.get('look', 0.0), raise_ph=HEROINE.get('raise_ph', 0.0),
                       look_y=HEROINE.get('look_y', 0.0))
        return
    if who['kind'] == 'zombie':
        sp = zombie_base(k)
        rig = F.Rig(sp)
        kit.contact_shadow(img, cam, nx, fy, 300 * s)
        if act == 'door':     # clawing forward out of the doorway
            sp['arms'] = {'L': rig.arm('L', (-330 + 40 * w1, -40 + 60 * w2), 'palm', 'out', strict=False),
                          'R': rig.arm('R', (330 - 40 * w2, -20 + 60 * w1), 'palm', 'out', strict=False)}
            person(img, cam, nx, ny, s, sp, t, tilt=0.1 * w1)
        elif act in ('lunge_r', 'lunge_l', 'lunge', 'stalk'):
            d = 1 if act == 'lunge_r' else -1 if act == 'lunge_l' else (1 if k % 2 else -1)   # always sideways: reads best
            if act == 'stalk':
                d = who.get('dir', 1)
            near, far = ('L', 'R') if d > 0 else ('R', 'L')   # the arm on the far side crosses the body
            grab_ = 0.5 + 0.5 * math.sin(t * 6 + k)            # clawing: reaching out and pulling back
            sp['arms'] = {far: rig.arm(far, (d * (300 + 90 * grab_), -10 - 50 * w2), 'palm', 'out', strict=False),
                          near: rig.arm(near, (d * (110 + 60 * grab_), 30 + 30 * w1), 'palm', 'down', strict=False)}
            person(img, cam, nx, ny, s, sp, t, legs='lunge', phase=ph, tilt=0.22 * d + 0.07 * w1)
        elif act == 'chair_z':  # comes round from behind the man with the chair; takes the hit; flies onto its back
            H = CHAIR_HIT
            if t < H:
                grab_ = 0.5 + 0.5 * math.sin(t * 6 + k)
                sp['arms'] = {'L': rig.arm('L', (-(300 + 90 * grab_), -10 - 50 * w2), 'palm', 'out', strict=False),
                              'R': rig.arm('R', (-(110 + 60 * grab_), 30 + 30 * w1), 'palm', 'down', strict=False)}
                person(img, cam, nx, ny, s, sp, t, legs='lunge', phase=ph if t < 1.0 else 1.0, tilt=-0.2 + 0.07 * w1)
            else:
                u = t - H
                x, y = pc.P(X, 0.0, z)
                if u < 0.4:            # airborne: thrown back, turning from upright to flat, head first
                    w = u / 0.4
                    ang, lift = -1.3 * (1 - F.ease(w)), 0.55 * UPM * math.sin(math.pi * w) * (1 - 0.4 * w)
                elif u < 0.55:         # hits the floor and bounces once
                    ang, lift = 0.0, 0.07 * UPM * math.sin(math.pi * (u - 0.4) / 0.15)
                else:
                    ang, lift = 0.0, 0.0
                twitch = max(0.0, math.sin((u - 0.7) * 20)) if any(a_ < u < a_ + 0.16 for a_ in (0.8, 1.6, 2.7)) else 0.0
                zombie_down(img, cam, x, y, s, sp, t, ang=ang, lift=lift, twitch=twitch, hit=u, flip=1)
        elif act == 'window_fall':
            window_fall(img, cam, pc, sp, t, X, z)
        elif act == 'window_climb':
            window_climb(img, cam, pc, sp, rig, t, X, z, w1, w2)
        elif act == 'tackle':   # it has him from behind: its body first, its arms and biting head after him
            sp.update(nohead=True, pose='none')
            person(img, cam, nx, ny, s, sp, t, legs='lunge', phase=1.0, tilt=0.12 + 0.05 * w1)
            PENDING[who['pair']] = (dict(zombie_base(k)), s)
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
        sp['arms'] = {'L': rig.arm('L', (-230, -150 + 60 * math.sin(ph)), 'palm', 'out', strict=False),
                      'R': rig.arm('R', (220, -170 - 60 * math.sin(ph)), 'palm', 'out', strict=False)}
        person_back(img, cam, nx, ny, s, sp, t, legs='run', phase=ph)
    elif act == 'door_pull':  # shoving the door shut against them: heaving again and again
        heave = abs(math.sin(t * 5 + k))
        sp['arms'] = {'L': rig.arm('L', (-50, 250 - 30 * heave), 'grip', 'out'), 'R': rig.arm('R', (50, 240 - 30 * heave), 'grip', 'out')}
        person_back(img, cam, nx, ny, s, sp, t, legs='lunge', phase=0.4, tilt=-0.08 - 0.12 * heave)
    elif act == 'tripod':      # swinging the tripod down on the zombie, lifting it, swinging again
        u = swing(t, 1.0, k * 0.13)
        th = math.radians(-70 - 125 * u)            # the hands sweep a wide arc: overhead, over to our left and down
        c_ = (20 + 330 * math.cos(th), 40 + 330 * math.sin(th))
        tg = (-math.sin(th), math.cos(th))
        L_, R_ = (c_[0] - 40 * tg[0], c_[1] - 40 * tg[1]), (c_[0] + 40 * tg[0], c_[1] + 40 * tg[1])
        sp['arms'] = {'L': rig.arm('L', L_, 'grip', 'out', strict=False), 'R': rig.arm('R', R_, 'grip', 'down', strict=False)}
        p = person(img, cam, nx, ny, s, sp, t, legs='lunge', phase=0.5, tilt=-0.1 + 0.25 * u)
        ang = math.radians(-160 + 120 * u)          # the tripod's legs point the way it is swung
        hx, hy = (L_[0] + R_[0]) / 2, (L_[1] + R_[1]) / 2
        for da in (-0.12, 0.0, 0.12):
            p.line([(hx, hy), (hx + 460 * math.cos(ang + da), hy + 460 * math.sin(ang + da))], (40, 40, 44), 9)
        p.poly([(hx - 45, hy - 35), (hx + 45, hy - 35), (hx + 45, hy + 35), (hx - 45, hy + 35)], (34, 34, 38), INK, 2.0)
    elif act == 'chair':       # guard, wind-up, ONE hard hit, then standing over it, panting (best-practice 1.3)
        H = CHAIR_HIT
        guard_L, guard_R = (-110 + 20 * w1, 220), (210, 200 + 20 * w2)    # held across his front, face clear
        up_L, up_R = (-170, -290), (10, -320)
        hit_L, hit_R = (100, 0), (290, -50)          # brought down on its head, at his side
        low_L, low_R = (60, 200), (200, 180)
        if t < H - 0.5:        # backing off, the chair held up between them, shaking
            L_, R_, deg, tl = guard_L, guard_R, 4 * w1, -0.06 + 0.03 * w2
        elif t < H - 0.1:      # the wind-up: high over his head, leaning back
            u = F.ease((t - (H - 0.5)) / 0.4)       # swung out wide and up (a straight lift folds the elbows)
            via = lambda a, m, b: lerp2(a, m, u * 2) if u < 0.5 else lerp2(m, b, u * 2 - 1)
            L_, R_ = via(guard_L, (-330, 140), up_L), via(guard_R, (320, 60), up_R)
            deg, tl = -14 * u, -0.06 - 0.12 * u
        elif t < H:            # the strike: very fast
            u = ((t - (H - 0.1)) / 0.1) ** 2
            L_, R_, deg, tl = lerp2(up_L, hit_L, u), lerp2(up_R, hit_R, u), -14 + 114 * u, -0.18 + 0.48 * u
        elif t < H + 0.25:     # follow-through
            L_, R_, deg, tl = hit_L, hit_R, 100, 0.3
        else:                  # straightening up over it, the bent chair hanging from his hands, panting
            u = F.ease(min(1.0, (t - H - 0.25) / 0.4))
            L_, R_ = lerp2(hit_L, low_L, u), lerp2(hit_R, low_R, u)
            deg, tl = 100 + 12 * u, 0.3 - 0.2 * u + 0.035 * math.sin(t * 9)
        sp['mouth'] = 'grimace' if t < H + 0.25 else 'wail'
        sp['look'] = 1.0                           # his eyes on the zombie at his side, the whole time
        mate = next((w for w in CROWD if w.get('pair') == who.get('pair') and w is not who), None)
        if mate is not None:
            X2, Z2 = where(mate, t)
            filmkit.eyeline(f'person {k} (chair)', t, cam.P(nx, ny - 150 * s), (sp['look'], 0.0), cam.P(*pc.P(X2, 1.5, Z2)))
        sp['arms'] = {'L': rig.arm('L', L_, 'grip', 'down', strict=False), 'R': rig.arm('R', R_, 'grip', 'out', strict=False)}
        p = person(img, cam, nx, ny, s, sp, t, legs='lunge', phase=2.0, tilt=tl)
        hx, hy = (L_[0] + R_[0]) / 2, (L_[1] + R_[1]) / 2
        a = math.radians(deg)                      # the chair turns as it comes down
        ca, sa = math.cos(a), math.sin(a)
        R2 = lambda x, y: (hx + x * ca - y * sa, hy + x * sa + y * ca)
        if t < H:
            p.poly([R2(-180, -170), R2(180, -180), R2(170, -30), R2(-170, -20)], CHAIR, INK, 2.4)
            p.line([R2(-170, -20), R2(-210, 150)], CHAIR_FRAME, 6)
            p.line([R2(170, -30), R2(200, 140)], CHAIR_FRAME, 6)
        else:                  # buckled by the blow: the back dented in, the legs bent out of true
            p.poly([R2(-180, -170), R2(-10, -120), R2(180, -190), R2(170, -30), R2(10, -60), R2(-170, -20)], CHAIR, INK, 2.4)
            p.line([R2(-170, -20), R2(-200, 60), R2(-130, 140)], CHAIR_FRAME, 6)
            p.line([R2(170, -30), R2(230, 50), R2(260, 110)], CHAIR_FRAME, 6)
    elif act == 'phone':       # filming it all, shaking, backing away
        sp['arms'] = rig.pose('hold', side='R', shape='phone', lift=0.9 + 0.1 * w2)
        sp['arms']['L'] = rig.arm('L', (-270 + 30 * w1, 210), 'palm', 'out', strict=False)
        sp['mouth'] = 'scream'
        person(img, cam, nx + 6 * s * w2, ny, s, sp, t, legs='lunge', phase=t * 6, tilt=0.05 * w1)
    elif act == 'tackled':     # held from behind: straining away, one arm reaching for help, the other tearing at its grip
        strain = 0.28 + 0.06 * w1 - 0.18 * min(1.0, t / 3.0)        # he strains away; it hauls him back upright
        reach = (-330 + 40 * w2, -120 + 80 * w1)          # one arm flung out for help, the other shoving its face away;
        sp['arms'] = {'L': rig.arm('L', reach, 'palm', 'out', strict=False),       # eyes on his attacker, head turned from it
                      'R': rig.arm('R', (200 + 15 * w1, -60 + 15 * w2), 'palm', 'out', strict=False)}
        sp.update(look=1.0, tilt=-0.22)     # eyes on the biter at his right shoulder, head turned away from it
        sp['splats'] = [(60, 60, 22, 9), (90, 140, 14, 10)]
        sp['face_splats'] = [(30, -120, 9, 11)]
        L = B.Local(cam, nx, ny, s)
        Rv = PP.Rot(L, strain, pivot=(0, 440))
        person(img, cam, nx, ny, s, sp, t, legs='lunge', phase=t * 10, tilt=strain)
        if who.get('pair') in PENDING:
            zsp, zs = PENDING.pop(who['pair'])
            grip_and_bite(img, Rv, zsp, t, k)
            filmkit.eyeline(f"person {k} (grabbed)", t, Rv.P(0, -150), (sp['look'], 0.0), _Offset(Rv, 135, -5, -0.5).P(0, -150))
    elif act == 'hide':        # the ostrich: head and shoulders jammed under a chair, the rest of her very much not hidden
        sp.update(jacket=(176, 44, 52), trousers=(196, 172, 132))      # bright, so she reads against the chairs
        sp.pop('skirt', None)
        zi, xi = HIDE_SEAT
        chair(img, cam, pc, SEATS_X[xi], ROWS_Z[zi])
        kit.contact_shadow(img, cam, nx, fy, 420 * s)
        hider(img, cam, nx, fy, s, sp, t)

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


@functools.lru_cache(maxsize=12)
@functools.lru_cache(maxsize=4)
def phone_hand_layer(side, tap_key=0, relax=0.0, phone=True):
    """Her hand holding the phone up (shot 4), on its own layer so it can move on its own when the phone drops: the
    sleeve coming up from below and a plain circle hand over the phone's lower corner (the same hand that lifted it
    in the close-up). One hand only: side 'R' is empty."""
    lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
    if side == 'R':
        return lay
    cam = B.Cam(1.0, 540, 960)
    p = B.Pen(lay, Turned(cam, PHONE_AT[0], PHONE_AT[1], PHONE_ANG))
    hx, hy = -PHONE_W / 2 + 40, PHONE_H / 2 - 30
    taper(p, (hx - 330, hy + 1100), (hx, hy), 150, 130, REPORTER['jacket'], lw=5.0)
    p.ell(hx, hy, 165, 165, (240, 228, 220), INK, 5.0)
    return lay


def phone_hands_layer(tap_key=0):
    return phone_hand_layer('L')


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


def taper(p, a, b, wa, wb, colr, lw=2.4):
    """A smooth limb piece from a to b, wa to wb wide, with a round joint at a."""
    d = (b[0] - a[0], b[1] - a[1])
    n = math.hypot(*d) or 1
    nx, ny = -d[1] / n, d[0] / n
    p.poly([(a[0] + nx * wa, a[1] + ny * wa), (b[0] + nx * wb, b[1] + ny * wb), (b[0] - nx * wb, b[1] - ny * wb),
            (a[0] - nx * wa, a[1] - ny * wa)], colr, None)
    p.line([(a[0] + nx * wa, a[1] + ny * wa), (b[0] + nx * wb, b[1] + ny * wb)], INK, lw)
    p.line([(a[0] - nx * wa, a[1] - ny * wa), (b[0] - nx * wb, b[1] - ny * wb)], INK, lw)
    p.ell(a[0], a[1], wa, wa, colr, None)


def crawl_hand(step, near=True):
    """Where her hand is (her own units) at this point of the crawl: planted, then lifted and moved forward."""
    ph = math.sin(step if near else step + math.pi)
    return (-210 + (0 if near else 30) + 30 * ph, -6 - max(0.0, ph) * 18)


def reporter_crawl(img, cam, x, y, s, t, step=0.0, flip=1, phone=None, pick=0.0, hold=False, look=0.0, who_sp=None, raise_ph=0.0, look_y=0.0):
    """Crawling on hands and knees across the floor, seen from the side (heading to our left when flip=1), her face
    turned to us in terror (the cartoon convention: body in profile, head to camera). (x, y): the floor under her
    middle. step: the crawl cycle (radians). The pickup, without stopping: `pick` (0-1) carries her leading hand
    onto the phone (at `phone`, her units) on its stroke; `hold`: she crawls on with it clutched in that fist."""
    L = B.Local(cam, x, y, s, flip)
    p = B.Pen(img, L)
    sp = dict(REPORTER, wide=True, brows='terror', mouth='gasp', skin=(240, 234, 232), look=look, look_y=look_y,
              face_splats=[(-38, -110, 8, 7), (44, -60, 6, 8)], tail_swing=40 + 20 * math.sin(step))
    if who_sp:     # someone else on hands and knees (a zombie dragging itself along): their own look and face
        sp.update({k_: v_ for k_, v_ in who_sp.items() if k_ not in ('arms', 'pose')})
        sp.setdefault('tights', sp.get('trousers', (60, 62, 72)))
        sp['skirt'] = sp.get('skirt') or sp.get('jacket')
    jc, skin, tights = sp['jacket'], sp['skin'], sp['tights']
    kit.contact_shadow(img, cam, x, y, 640 * s, alpha=0.25)
    lift = lambda v: max(0.0, v) * 18
    bob = 6 * math.sin(step * 2)                       # the body rocks with each stroke

    def arm(dx, colr, near, reach=0.0):
        sh = (-150 + dx, -300 + bob)
        hand = crawl_hand(step, near)
        hand = (hand[0] + dx, hand[1])
        if reach > 0 and phone is not None:
            hand = lerp2(hand, (phone[0] + 20, phone[1] - 4), F.ease(reach))
        if near and raise_ph > 0:  # stopped: the phone comes up to her eyeline, in front of her face
            hand = lerp2(hand, (-345, -430 + bob), F.ease(raise_ph))
        # raised: the elbow drops low and forward, the forearm goes straight up in front of her, clear of her head
        el, wr = ik2(sh, (hand[0] + 6, hand[1] - 22), 150, 140, bend=-1 if (near and raise_ph > 0.5) else 1)
        taper(p, sh, el, 30, 26, colr)
        taper(p, el, wr, 26, 20, colr)
        c = B.dk(skin, 0.95) if dx else skin
        d_ = (wr[0] - el[0], wr[1] - el[1])
        n_ = math.hypot(*d_) or 1.0
        hx, hy = wr[0] + d_[0] / n_ * 12, wr[1] + d_[1] / n_ * 12
        if hold and near:          # the phone laid over the circle hand: flat along the floor, then up at her eyeline
            phone_prop(p, hx, hy + 10, ang=-1.5 * (1 - F.ease(raise_ph)))
        chand(p, hx, hy, c)

    def leg(dx, colr, ph):
        hip, knee = (120 + dx, -290 + bob), (150 + dx + 26 * ph, -28 - lift(ph))
        foot = (360 + dx + 26 * ph, -14 - lift(ph) * 0.5)
        taper(p, hip, knee, 52, 34, colr)
        taper(p, knee, foot, 34, 20, colr)
        p.poly(curve([(foot[0] - 16, foot[1] - 18), (foot[0] + 36, foot[1] - 14), (foot[0] + 44, foot[1] + 4),
                      (foot[0] - 16, foot[1] + 8)], 3), sp['shoe'], INK, 2.2)
    a_, b_ = math.sin(step), math.sin(step + math.pi)
    leg(-30, B.dk(tights, 0.86), b_)                   # the far side first, a shade darker
    arm(30, B.dk(jc, 0.86), False)
    # the body: a curved back from the shoulders to the hips, the skirt over the hips
    # the neck grows out of the top of her shoulders, curving up and forward to under her chin (drawn first: the
    # jacket's collar covers its base, so it can never look stuck on)
    neck = curve([(-226, -404 + bob), (-188, -410 + bob), (-166, -378 + bob), (-140, -336 + bob), (-186, -322 + bob),
                  (-206, -360 + bob)], 3)
    p.poly(neck, B.dk(skin, 0.93), INK, 2.4)
    body = curve([(-215, -320 + bob), (-170, -378 + bob), (-30, -398 + bob), (100, -388 + bob), (175, -350 + bob),
                  (182, -290 + bob), (100, -262 + bob), (-40, -268 + bob), (-170, -282 + bob)], 6)
    check_neck(neck, body)
    p.poly(body, jc, INK, 2.6)
    p.poly(curve([(70, -390 + bob), (160, -376 + bob), (205, -330 + bob), (196, -262 + bob), (130, -236 + bob),
                  (70, -248 + bob)], 5), sp['skirt'], INK, 2.4)
    soft(img, L, [(-150, -370 + bob), (40, -388 + bob), (170, -360 + bob), (40, -350 + bob)], (255, 255, 255), 0.2, 6)
    splat(p, -60, -340 + bob, 18, 5)
    splat(p, 30, -290 + bob, 12, 6, drops=2)
    leg(0, tights, a_)
    # the lanyard hangs from her neck under her chest, swinging with each stroke
    kit.dangle(p, (-180, -330 + bob), 150, 0.25 * math.sin(step * 2), sp['lanyard_c'], 5, tag=(26, 34, (236, 236, 232)))
    arm(0, jc, True, reach=pick)
    # her head, turned to us, sitting on the top of the neck
    hx, hy = -208, -468 + bob
    B.hair_back(p, sp, hx, hy, sp['hw'], sp['hh'])
    B.head(img, p, sp, t, hx, hy)
    for (fx, fy, r, seed) in sp['face_splats']:
        splat(p, hx + fx, hy + 150 + fy, r, seed, drops=2)
    if raise_ph > 0.5:  # the screen's cold light on her face
        soft(img, L, [(hx - 75, hy - 30), (hx + 40, hy - 30), (hx + 40, hy + 80), (hx - 75, hy + 80)], (214, 232, 255),
             0.5 * (raise_ph - 0.5), 4)


def inside(pt, poly):
    """Is the point inside the polygon (even-odd rule)?"""
    x, y = pt
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def check_neck(neck, body):
    """Best-practice 1.3: a neck grows out of the body. The two base corners of the neck must lie inside the body
    outline (so no gap can ever open between them), or the render stops."""
    base = [pt for pt in neck if pt[1] > max(q[1] for q in neck) - 30]
    if not all(inside(pt, body) for pt in base):
        raise ValueError(f'check: her neck base {base[:2]} is outside her body: the head would float')


CHAIR_HIT = 1.5                 # shot 2: the chair lands, this many seconds after the 180
WIN_BURST = 0.6                 # shot 2: the window nearest the back bursts in
WIN_Z = 6.2


class _Place:
    """A frame placed inside another at (ox, oy), turned by a (a head on a neck that lies along the floor)."""
    def __init__(self, parent, ox, oy, a):
        self.parent, self.ox, self.oy, self.c, self.sn = parent, ox, oy, math.cos(a), math.sin(a)
        self.s, self.cam = parent.s, getattr(parent, 'cam', None)

    def P(self, x, y):
        return self.parent.P(self.ox + x * self.c - y * self.sn, self.oy + x * self.sn + y * self.c)

    def S(self, v):
        return self.parent.S(v)


def zombie_down(img, cam, x, y, s, sp, t, ang=0.0, lift=0.0, twitch=0.0, hit=9.0, flip=1):
    """A zombie flat on its back on the floor, seen side-on: feet at one end, the head lolling at the other (head
    towards local +x). (x, y): the floor under its hips (world px). ang turns the whole body about the hips (in
    flight: -1.3 is nearly upright); lift raises it off the floor (its own units); twitch (0-1) jerks a knee and the
    far arm; hit: seconds since the blow (blood on the floor under its head spreads from the landing)."""
    sp = dict(sp)
    L0 = B.Local(cam, x, y - lift * s, s, flip)
    L = PP.Rot(L0, ang, pivot=(0, -70)) if ang else L0
    p = B.Pen(img, L)
    jc, skin = sp.get('jacket', B.NAVY), sp['skin']
    tc = sp['tights'] if sp.get('skirt') else sp.get('trousers', (60, 62, 72))
    shoe = sp.get('shoe', (22, 20, 22))
    if ang == 0.0 and lift < 1:
        kit.contact_shadow(img, cam, x + 80 * s * flip, y, 1000 * s, alpha=0.3)
        if hit > 0.45:     # a pool spreading under its head
            r = min(1.0, (hit - 0.45) / 1.5)
            p.ell(520, -4, 60 + 110 * r, 14 + 22 * r, BLOOD_D, None)
            p.ell(520, -6, 44 + 90 * r, 10 + 16 * r, BLOOD, None)
    stump = sp.get('stump', ())
    # the far arm (behind the body): flung up when it twitches, lying behind it otherwise
    if 'R' not in stump:
        el = lerp2((250, -40), (360, -230), twitch)
        hd = lerp2((150, -30), (430, -300), twitch)
        taper(p, (300, -120), el, 30, 26, B.dk(jc, 0.85))
        taper(p, el, hd, 26, 20, B.dk(jc, 0.85))
        p.ell(hd[0], hd[1], 26, 22, B.dk(skin, 0.9), INK, 2.0)
    # the legs: the far one a shade darker; a knee jerks up on a twitch
    for dx, dy, colr, tw in ((25, -12, B.dk(tc, 0.85), twitch), (0, 0, tc, 0.0)):
        hip, knee, foot = (-50 + dx, -60 + dy), (-230 + dx, -250 + dy - 90 * tw), (-400 + dx * 0.5, -30 + dy)   # knees up
        taper(p, hip, knee, 56, 40, colr)
        taper(p, knee, foot, 40, 26, colr)
        p.poly(curve([(foot[0] + 20, foot[1] - 34), (foot[0] - 50, foot[1] - 26), (foot[0] - 70, foot[1] + 10),
                      (foot[0] + 24, foot[1] + 14)], 3), shoe, INK, 2.2)          # flat on the floor, toes out
    # the body on its back: chest up, the jacket rumpled, its shirt and lanyard
    body = curve([(-130, -8), (-140, -110), (40, -150), (300, -160), (370, -120), (380, -10), (120, 0)], 5)
    p.poly(body, jc, INK, 2.6)
    p.poly([(250, -158), (330, -150), (300, -115)], sp.get('shirt', (206, 204, 190)), INK, 1.8)
    if sp.get('skirt'):
        p.poly(curve([(-150, -10), (-160, -110), (-10, -146), (40, -140), (30, -6)], 3), sp['skirt'], INK, 2.4)
    if sp.get('gash'):
        p.poly(curve([(90, -150), (170, -158), (190, -120), (110, -112)], 3), BLOOD, INK, 1.8)
    splat(p, 200, -120, 20, 7)
    # the near arm, flopped on the floor beside it
    if 'L' not in stump:
        taper(p, (330, -100), (420, -30), 30, 26, jc)
        taper(p, (420, -30), (530, -22), 26, 20, jc)
        p.ell(552, -22, 26, 20, skin, INK, 2.0)
    else:
        p.ell(340, -100, 30, 18, BLOOD, B.dk(BLOOD, 0.6), 1.6)
    # the neck and the head, lolling back, its face to us
    taper(p, (360, -95), (430, -95), 34, 30, B.dk(skin, 0.92))
    hl = _Place(L, 420, -100, math.pi / 2 - 0.3)
    hp = B.Pen(img, hl)
    sp.update(mouth=sp.get('mouth', 'snarl') if hit > 0.1 else 'scream', tilt=0.0,
              face_splats=[(20, -110, 9, 5), (-30, -60, 7, 6)] if hit < 9 else sp.get('face_splats', []))
    B.hair_back(hp, sp, 0, -150, sp.get('hw', 70), sp.get('hh', 90))
    B.head(img, hp, sp, t, 0, -150)
    for (fx, fy, r, seed) in sp['face_splats']:
        splat(hp, fx, -150 + 150 + fy, r, seed, drops=2)
    if hit < 0.3:          # the blow: blood thrown off its head the way it is flying
        for j in range(6):
            u = hit / 0.3
            a = math.radians(-60 + 20 * j)
            hp.ell(60 * j * u + 80 * u, -150 + 40 * math.sin(a) * u * 4, 10 * (1 - 0.5 * u), 10 * (1 - 0.5 * u), BLOOD, None)
        splat(hp, 40, -150, 30, 9, drops=4)


def _wall_mask(img, cam, pc, X, z0, z1, y_top):
    """A mask that is clear everywhere except over the wall below y_top between z0 and z1 (what hides the legs of
    someone climbing in through a window)."""
    m = Image.new('L', img.size, 255)
    q = clipz(pc, [(X, 0.0, z0), (X, 0.0, z1), (X, y_top, z1), (X, y_top, z0)])
    if len(q) >= 3:
        ImageDraw.Draw(m).polygon([cam.P(*pt) for pt in q], fill=0)
    return m


def _masked(img, lay, mask):
    lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay.getchannel('A')), np.asarray(mask))))
    img.alpha_composite(lay)


def window_fall(img, cam, pc, sp, t, X, z):
    """The front one at the window: pressed to the glass; when it bursts it topples over the sill head first into a
    heap on the floor below, lies there twitching, then drags itself up onto its hands and knees and comes on."""
    W = ROOM['x0']
    if t < WIN_BURST:      # pressed to the glass, outside (seen through it)
        outside(img, cam, pc, window_pane(W, WIN_Z), [(W - 0.3, z, 20)], t, glass_x=W, sp_for={20: sp})
        return
    u = t - WIN_BURST
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    if u < 0.45:           # toppling over the sill: pivoting on its hips at the sill, then dropping inside
        w = u / 0.45
        hipX = lerp2((W - 0.15, 0.0), (X, 0.0), F.ease(w))[0]
        hipY = 0.75 * (1 - w * w)
        x, y = pc.P(hipX, hipY, z)
        s = pc.scale(z, hipX)
        zombie_down(lay, cam, x, y, s, sp, t, ang=-1.45 * (1 - F.ease(w)), hit=9.0, flip=-1)
        _masked(img, lay, _wall_mask(img, cam, pc, W - 0.001, WIN_Z - 1.2, WIN_Z + 1.2, 0.55))
        return
    if u < 1.2:            # in a heap, a bounce, twitching
        x, y = pc.P(X, 0.0, z)
        lift = 0.05 * UPM * max(0.0, math.sin(math.pi * (u - 0.45) / 0.12)) if u < 0.57 else 0.0
        zombie_down(img, cam, x, y, pc.scale(z, X), sp, t, lift=lift, twitch=max(0.0, math.sin(u * 30)) if u > 0.8 else 0.0,
                    hit=9.0, flip=-1)
        return
    x, y = pc.P(X, 0.0, z)  # dragging itself up and on, slowly, on hands and knees
    reporter_crawl(img, cam, x, y, pc.scale(z, X), t, step=(u - 1.2) * 4, flip=1, who_sp=sp)


def window_climb(img, cam, pc, sp, rig, t, X, z, w1, w2):
    """The second one: when the glass goes it steps up, a knee on the sill, and climbs in, clawing at the room."""
    W = ROOM['x0']
    if t < WIN_BURST:
        outside(img, cam, pc, window_pane(W, WIN_Z), [(X, z, 21)], t, glass_x=W, sp_for={21: sp})
        return
    u = min(1.0, (t - WIN_BURST) / 0.8)
    rise = 0.42 * F.ease(u)                                  # up onto the sill
    grab_ = 0.5 + 0.5 * math.sin(t * 6)
    sp['arms'] = {'L': rig.arm('L', (300 + 80 * grab_, -60 - 40 * w2), 'palm', 'out', strict=False),
                  'R': rig.arm('R', (160 + 60 * grab_, 10 + 30 * w1), 'palm', 'out', strict=False)}
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    s = pc.scale(z, X)
    nx, ny = pc.P(X, rise + F.SOLE_Y / UPM, z)
    person(lay, cam, nx, ny, s, sp, t, legs='kneel' if u > 0.5 else 'lunge', phase=1.0, tilt=-0.25 - 0.08 * w1, flip=-1)
    _masked(img, lay, _wall_mask(img, cam, pc, W - 0.001, WIN_Z - 1.2, WIN_Z + 1.2, 0.55))


def window_pane(X, zw):
    return [(X, 0.55, zw - 0.7), (X, 0.55, zw + 0.7), (X, 3.1, zw + 0.7), (X, 3.1, zw - 0.7)]


def cracks(p, pc, X, zc, yc, grow, seed, reach=0.75):
    """Cracks spreading through a pane from where it is struck: jagged white lines, growing (0-1)."""
    rng = np.random.default_rng(seed)
    for j in range(11):
        a = 2 * math.pi * j / 11 + rng.uniform(-0.2, 0.2)
        pts, (zz, yy) = [], (zc, yc)
        n = 5
        for kk in range(n + 1):
            if kk / n > grow:
                break
            pts.append(pc.P(X + 0.002, yy, zz))
            step = reach * rng.uniform(0.6, 1.1) / n
            a += rng.uniform(-0.35, 0.35)
            zz, yy = zz + math.cos(a) * step, yy + math.sin(a) * step
            yy = min(3.08, max(0.57, yy))
            zz = min(WIN_Z + 0.68, max(WIN_Z - 0.68, zz)) if abs(zc - WIN_Z) < 1 else zz
        if len(pts) > 1:
            p.line(pts, (90, 110, 120), 3.2)
            p.line(pts, (250, 252, 255), 1.8)
    for r in (0.06, 0.13):     # rings round the point of impact
        ring = [pc.P(X + 0.002, yc + r * math.sin(2 * math.pi * q / 10), zc + r * math.cos(2 * math.pi * q / 10)) for q in range(11)]
        if grow > r * 4:
            p.line(ring, (250, 252, 255), 1.6)


def shards(img, cam, pc, X, zw, t, seed=3):
    """The burst: glass thrown into the room, falling, then lying glinting on the floor."""
    if t < WIN_BURST:
        return
    p = B.Pen(img, cam)
    rng = np.random.default_rng(seed)
    u = t - WIN_BURST
    for j in range(16):
        z0, y0 = zw + rng.uniform(-0.6, 0.6), rng.uniform(0.7, 2.1)
        vx, vy, vz = rng.uniform(1.5, 3.5), rng.uniform(-0.2, 1.4), rng.uniform(-0.6, 0.6)
        tl = (vy + math.sqrt(vy * vy + 2 * 9.8 * y0)) / 9.8      # when it lands
        tu = min(u, tl)
        Xs, Ys, Zs = X + vx * tu, y0 + vy * tu - 4.9 * tu * tu, z0 + vz * tu
        sz = rng.uniform(0.05, 0.11) * (0.6 if u >= tl else 1.0)
        spin = rng.uniform(0, 6) + (u * 9 if u < tl else 0)
        pts = []
        for q in range(3):
            a = spin + q * 2.1 + rng.uniform(-0.3, 0.3)
            if u < tl:
                pts.append(pc.P(Xs + math.cos(a) * sz * 0.5, Ys + math.sin(a) * sz, Zs + math.cos(a) * sz))
            else:   # flat on the floor
                pts.append(pc.P(Xs + math.cos(a) * sz, 0.003, Zs + math.sin(a) * sz))
        p.poly(pts, (226, 240, 248), (110, 130, 140), 1.6)


def glass_prints(img, hands, t):
    """Where a zombie's own hand is pressed to the glass: a smeared grimy, bloody print round it, streaks dragged
    down below (best-practice 1.3: effects land on surfaces). hands: canvas points of hands on the glass."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for (hx, hy, r, seed) in hands:
        rng = np.random.default_rng(seed)
        d.ellipse([hx - r * 1.2, hy - r * 1.1, hx + r * 1.2, hy + r * 1.3], fill=(110, 30, 34, 170))
        for kk in range(4):
            x0 = hx - r * 0.8 + kk * r * 0.55
            ln = r * (1.5 + 2.5 * rng.random()) * min(1.0, 0.4 + 0.3 * t)
            d.line([(x0, hy + r), (x0 + rng.uniform(-2, 2), hy + r + ln)], fill=(130, 24, 30, 200), width=max(2, int(r * 0.32)))
    return lay


HEROINE = {}                    # her crawl in shots 3 and 3b: the phone's place, the pickup, the hold
HEROINE_S3 = (-0.45, 3.25)      # where she has crawled to by shot 3 (down the aisle, towards the podium)
PHONE_S3 = (-0.08, 3.25)        # her phone, dropped on the floor just ahead of where she stops


def floor_phone(img, cam, pc, X, Z, lit=True):
    """A phone lying face up on the floor (about 15 x 7 cm), its screen lit."""
    p = B.Pen(img, cam)
    pts = [(X - 0.04, 0.005, Z - 0.08), (X + 0.04, 0.005, Z - 0.08), (X + 0.04, 0.005, Z + 0.08), (X - 0.04, 0.005, Z + 0.08)]
    quad(p, pc, pts, (26, 26, 30), INK, 2.0)
    scr = [(X - 0.032, 0.006, Z - 0.07), (X + 0.032, 0.006, Z - 0.07), (X + 0.032, 0.006, Z + 0.07), (X - 0.032, 0.006, Z + 0.07)]
    quad(p, pc, scr, (190, 214, 240) if lit else (40, 40, 46), None)


CRAWL_Z, CRAWL_X0, CRAWL_V = 3.25, -0.8, 0.35           # her line across the hall in shots 3 and 3b (plan, m/s)


CRAWL_STOP = 2.1               # she stops crawling this long into shot 3 (0.6 s into the close-up) and sits back


def heroine_x(tl):
    """Where she is along her line, tl seconds into shot 3 (crawling until CRAWL_STOP, then still)."""
    return CRAWL_X0 + CRAWL_V * min(tl, CRAWL_STOP)


def heroine_state(tl):
    """Her crawl at tl seconds into shot 3: the crawl cycle, and the pickup on the stroke that lands on the phone."""
    tp = T['grab'] - T['s3']                                     # her hand comes down on the phone here
    step = (T['s3'] - T['s2'] + tl) * 7
    hand = crawl_hand((T['s3'] - T['s2'] + tp) * 7, True)
    phone = (heroine_x(tp) - hand[0] / UPM, CRAWL_Z)           # her hand's spot on the floor at that moment
    pick = 0.0 if tl < tp - 0.3 else min(1.0, (tl - (tp - 0.3)) / 0.3)
    hold = tl >= tp
    look = -1.0 if (tl * 3) % 2 < 1 else 0.6                    # glancing back at what's behind her, then ahead
    return dict(step=step, phone_plan=None if hold else phone, pick=0.0 if hold else pick, hold=hold, look=look), phone


def shot_crawl(t=0.0, grab=0.0, tl=None):
    """Shot 3: low among the chairs, looking towards the back of the hall; she crawls across, away from the zombie
    behind her, and snatches up her phone on the way without stopping."""
    pc = PCam(-0.45, 0.42, 1.85, 1, 1150.0, oy=1180.0)
    cam = B.Cam(1.0, 540, 960)
    img = B.canvas(WALL)
    room(img, cam, pc, t, chaos=True)
    risers(img, cam, pc)
    for X, Z, r, seed in FLOOR_SPLATS:
        floor_splat(img, cam, pc, X, Z, r, seed)
    tl = 0.0 if tl is None else tl
    st, phone = heroine_state(tl)
    HEROINE.clear()
    HEROINE.update(st)
    if not st['hold']:
        floor_phone(img, cam, pc, *phone)
    hx = heroine_x(tl)
    items = [(CRAWL_Z - 0.05, hx, k, dict(a, x=hx, z=CRAWL_Z, v=(0.0, 0.0)))
             if k == 'person' and a['kind'] == 'heroine' else (z, x, k, a) for z, x, k, a in chaos_items(pc)]

    def keep(i):
        if i[2] != 'person':
            return pc.depth(i[0], i[1]) > 1.1
        w = i[3]
        if w['kind'] == 'heroine':
            return True
        X, z = where(w, t)
        if pc.depth(z, X) < 1.1 or w['z'] < 2.7:
            return False
        return -60 < pc.P(X, 1.4, z)[0] < 1140            # nobody cut off by the frame's edge
    items = sorted([i for i in items if keep(i)], key=lambda i: -pc.depth(i[0], i[1]))
    draw_items(img, cam, pc, items, t)
    HEROINE.clear()
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
    B.title_lines(img, TITLE, alpha=1.0 if t < 1.75 else max(0.0, 1.0 - (t - 1.75) / 0.25))   # on for 2 s (Sam)
    return img


# ============================================================================================ the film
import mouths
import mossad_audio as MA
from burnham_film import onepole_lp, normal

mouths.install(B)

# Placeholder timing from Sam's usual pace (3.0-3.6 words a second) until his recordings arrive; then REC replaces
# it (cleaned and levelled by mossad_audio.line; pauses may be shortened, never the words).
LINE1 = ['The researcher in question', 'died from a common pneumonia.', 'All is well.', 'We ask anyone concerned',
         'to pay attention to the bulletins from', 'the Ministry of Health.']
LINE2 = ['Any more questions?']
REC_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio', 'russiadent-peskov.m4a')
REC_CUTS = [(4.45, 19.05), (24.18, 26.45)]       # Sam's take (recorded outdoors): line 1, line 2


@functools.lru_cache(maxsize=1)
def rec_lines():
    """Sam's two lines, cleaned (hum, rumble and hiss off; the outdoor noise taken down hard and gated out of the
    pauses), long pauses shortened to 0.3 s (never the words), each line set to the shared line loudness.
    Returns [(voice, speech stretches in seconds from the line's start)] for line 1 and line 2."""
    from scipy.signal import butter, sosfiltfilt
    from burnham_film import load
    import mossad_audio as MA_
    MA_.MAX_CUT_DB = 20.0
    x = load(REC_FILE)
    y = sosfiltfilt(butter(4, [90, 8000], 'band', fs=SR, output='sos'), MA_.dehum(x))
    y = MA_.denoise(MA_.denoise(y))
    out = []
    for a, b in REC_CUTS:
        seg = y[int(a * SR):int(b * SR)]
        ps = MA_.pauses(seg, 0.12)
        lv = [20 * np.log10(np.sqrt(np.mean(seg[int(p0 * SR):int(p1 * SR)] ** 2)) + 1e-9) for p0, p1 in ps]
        ps = [p for p, l in zip(ps, lv) if l > max(lv) - 14]       # quiet blips are noise, not words
        parts, stretches, t, prev = [], [], 0.0, None
        f_ = int(0.01 * SR)
        for p0, p1 in ps:
            if prev is not None:
                gap = max(0.0, min(0.3, p0 - prev) - 0.08)
                parts.append(np.zeros(int(gap * SR)))
                t += gap
            s_ = seg[max(0, int((p0 - 0.03) * SR)):int((p1 + 0.05) * SR)].copy()
            s_[:f_] *= np.linspace(0, 1, f_)
            s_[-f_:] *= np.linspace(1, 0, f_)
            parts.append(s_)
            stretches.append((t + 0.03, t + 0.03 + (p1 - p0)))
            t += len(s_) / SR
            prev = p1
        v = np.concatenate(parts)
        out.append((v * 10 ** ((MA_.LINE_LUFS - MA.lufs(v)) / 20), stretches))
    return out


REC_PIECES = [[0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 5], [0, 0]]   # which caption piece each speech stretch says (by ear-timing)


def rec_word_times(start, pieces, stretches, owner):
    """Each caption piece's words spread over its own speech stretches, by syllables."""
    out = []
    for i, pc in enumerate(pieces):
        mine = [st for st, o in zip(stretches, owner) if o == i]
        ws = pc.split()
        total = sum(syl(w) for w in ws)
        span = sum(b - a for a, b in mine)
        k, acc = 0, 0.0
        for w in ws:
            d = syl(w) / total * span
            # walk acc (speech seconds into this piece) onto the stretches
            def at(u):
                for a, b in mine:
                    if u <= b - a:
                        return a + u
                    u -= b - a
                return mine[-1][1]
            out.append((i, start + at(acc), start + at(acc + d), w))
            acc += d
    return out
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
W1 = rec_word_times(0.30, LINE1, rec_lines()[0][1], REC_PIECES[0])
T['line1_end'] = W1[-1][2]
T['s2'] = T['line1_end'] + 0.35                 # the 180: hard cut into the outbreak
T['slap'] = 5.2                                 # shot 1: a hand slaps onto the podium's edge (no reaction)
T['s3'] = T['s2'] + 3.0                         # she crawls
T['grab'] = T['s3'] + 0.85                      # she reaches for her phone, picks it up
T['s3b'] = T['s3'] + 1.5                        # her face as she types
T['s4'] = T['s3b'] + 2.5                        # her phone (after the tracking close-up)
T['roar'] = T['s4'] + 1.3                       # a zombie roars right behind her
T['crunch'] = T['s4'] + 2.05                    # a crunch, and blood bursts across the screen
T['s5'] = T['s4'] + 3.4                         # back to Peskov (after the phone drops out of frame)
T['arm_throw'] = T['s5'] + 0.2                  # a severed arm (still holding a microphone) flies up...
T['arm_hit'] = T['s5'] + 0.55                   # ...and slaps the backdrop behind him
W2 = rec_word_times(T['s5'] + 1.25, LINE2, rec_lines()[1][1], REC_PIECES[1])
T['line2_end'] = W2[-1][2]
T['black'] = T['line2_end'] + 0.6               # a short silent beat (the screams go on), then hard cut to black
T['dur'] = T['black'] + 0.35
BLACK_AT, DUR = T['black'], T['dur']            # for preflight.py
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


def rec_track(start, pieces, stretches, owner):
    """Mouth shapes piece by piece, each over its own speech stretches (so every phrase moves his mouth)."""
    out = []
    for i, pc in enumerate(pieces):
        mine = []
        for st in [st for st, o in zip(stretches, owner) if o == i]:   # bits split by a breath count as one
            if mine and st[0] - mine[-1][1] < 0.25:
                mine[-1] = (mine[-1][0], st[1])
            else:
                mine.append(st)
        t0 = mine[0][0]
        out += [(a + start + t0, b + start + t0, sh) for a, b, sh in mouths.track(pc, [(a - t0, b - t0) for a, b in mine])]
    return out


TRACK = (rec_track(0.30, LINE1, rec_lines()[0][1], REC_PIECES[0]) +
         rec_track(W2[0][1], LINE2, rec_lines()[1][1], REC_PIECES[1]))


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
def _sprite_pen(n, k):
    lay = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    return lay, ImageDraw.Draw(lay), max(2, int(2.5 * B.SS))


@functools.lru_cache(maxsize=2)
def podium_hand():
    """The hand slapped on the podium's front edge: a sleeve from below and a circle hand clamped over the edge.
    Returns (layer, origin) with the edge's centre at the origin pixel."""
    pc, cam = cam_front(0.0, 1.0)
    k = pc.f / pc.depth(PODIUM_BOX['z1']) * B.SS                 # canvas pixels a metre at the podium's front
    n = int(0.5 * k)
    lay, d, lw = _sprite_pen(n, k)
    ox, oy = n / 2, n * 0.3
    d.polygon([(ox - 0.04 * k, oy + 0.02 * k), (ox + 0.04 * k, oy + 0.02 * k), (ox + 0.05 * k, n), (ox - 0.05 * k, n)],
              fill=(70, 90, 70, 255), outline=(0, 0, 0, 255), width=lw)
    r = 0.05 * k
    d.ellipse([ox - r, oy - r * 0.7, ox + r, oy + r * 1.3], fill=(236, 226, 220, 255), outline=(0, 0, 0, 255), width=lw)
    return lay, (ox, oy)


@functools.lru_cache(maxsize=2)
def mic_arm():
    """The severed arm still holding its microphone: circle hand round the mic's handle, the forearm ending in a flat
    red cut with a pale bone. Returns (layer, mic head, cut end, forearm direction) in layer pixels; centre = hand."""
    pc, cam = cam_front(0.0, 1.0)
    k = pc.f / pc.depth(-1.18) * B.SS
    n = int(0.6 * k)
    lay, d, lw = _sprite_pen(n, k)
    c = n / 2
    d.polygon([(c - 0.035 * k, c), (c + 0.035 * k, c), (c + 0.04 * k, c + 0.26 * k), (c - 0.04 * k, c + 0.26 * k)],
              fill=(80, 84, 96, 255), outline=(0, 0, 0, 255), width=lw)
    d.ellipse([c - 0.042 * k, c + 0.24 * k, c + 0.042 * k, c + 0.28 * k], fill=BLOOD + (255,), outline=(90, 0, 10, 255), width=lw)
    d.ellipse([c - 0.012 * k, c + 0.25 * k, c + 0.012 * k, c + 0.27 * k], fill=(236, 226, 210, 255))
    d.rectangle([c - 0.012 * k, c - 0.17 * k, c + 0.012 * k, c + 0.02 * k], fill=(30, 30, 34, 255), outline=(0, 0, 0, 255), width=lw)
    d.ellipse([c - 0.03 * k, c - 0.23 * k, c + 0.03 * k, c - 0.16 * k], fill=(70, 70, 76, 255), outline=(0, 0, 0, 255), width=lw)
    r = 0.045 * k
    d.ellipse([c - r, c - r, c + r, c + r], fill=(232, 222, 214, 255), outline=(0, 0, 0, 255), width=lw)
    return lay, (c, c - 0.2 * k), (c, c + 0.26 * k), (0.0, 1.0)


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


def ragged(pts, rng, amt):
    """Roughen an outline: every point nudged a little (seeded, so it is the same each frame)."""
    return [(x + rng.uniform(-amt, amt), y + rng.uniform(-amt, amt)) for x, y in pts]


def hand_smear(img, cam, pc, X, drop, u):
    """What a bloody hand leaves when it clings to the podium's front edge and slides down: a palm print where it
    held, four finger streaks dragged down below it along the hand's path (thinning, breaking up as the blood runs
    out), ragged darker edges, drips running on from the print. Drawn on the podium's front face, in metres (X across,
    Y up), and kept inside it. drop: how far the hand has slid (m); u: seconds since it began to slide."""
    p = B.Pen(img, cam)
    z = PODIUM_BOX['z1']
    y1 = STAGE_BOX['h'] + PODIUM_BOX['h'] - 0.06                       # just under the top rail
    floor_ = STAGE_BOX['h'] + 0.09                                      # the bottom of the front panel
    P = lambda x, y: pc.P(x, max(floor_, y), z)
    drift = lambda d_: 0.02 * d_ + 0.008 * math.sin(d_ * 9)            # the hand drifts a little as it slides
    rng = np.random.default_rng(91)
    FING = [(-0.024, 0.008, 0.040), (-0.008, 0.0085, 0.048), (0.008, 0.008, 0.046), (0.023, 0.007, 0.036)]   # x, half-width, length

    def blot(pts, rim=0.0035, inner=0.0025):
        """A wet print: a ragged dark rim, the brighter blood inside."""
        p.poly([P(*q) for q in ragged(curve(pts, 3), rng, rim)], BLOOD_D, None)
        cx = sum(q[0] for q in pts) / len(pts)
        cy = sum(q[1] for q in pts) / len(pts)
        p.poly([P(*q) for q in ragged(curve([(cx + (x - cx) * 0.72, cy + (y - cy) * 0.72) for x, y in pts], 3), rng, inner)],
               BLOOD, None)
    # the four finger streaks, dragged from the bottom of the print down the hand's path, each its own length
    run = min(drop, y1 - floor_ - 0.12)
    top = y1 - 0.105
    for i, (fx, w0, _) in enumerate(FING):
        length = max(0.0, run * (1.0 - 0.15 * abs(i - 1.3)))
        if length < 0.01:
            continue
        cut = sorted(float(c) for c in rng.uniform(0.35, 0.95, 1 + i % 2))   # where the blood runs out for a moment
        pieces, a0 = [], 0.0
        for c_ in cut + [1.0]:
            pieces.append((a0, c_ - 0.04 if c_ < 1.0 else 1.0))
            a0 = c_ + 0.03
        for pa, pb in pieces:
            if pb <= pa:
                continue
            n = 8
            ts = [pa + (pb - pa) * j / n for j in range(n + 1)]
            ys = [top - tt * length for tt in ts]
            ws = [w0 * (1 - 0.75 * tt) for tt in ts]
            xs = [X + fx + drift(tt * length) for tt in ts]
            left = [(x - w, y) for x, w, y in zip(xs, ws, ys)]
            right = [(x + w, y) for x, w, y in zip(xs, ws, ys)][::-1]
            blot(left + right, rim=0.002, inner=0.001)
    # the palm print where it clung: the heel of the hand, the thumb to one side, the fingers up to the edge
    blot([(X - 0.032, top + 0.03), (X + 0.03, top + 0.03), (X + 0.036, top - 0.005), (X + 0.02, top - 0.03),
          (X - 0.02, top - 0.03), (X - 0.036, top - 0.005)])
    blot([(X - 0.036, top + 0.0), (X - 0.05, top + 0.02), (X - 0.054, top + 0.042), (X - 0.044, top + 0.046),
          (X - 0.032, top + 0.024)], rim=0.002, inner=0.0015)
    for fx, w, ln in FING:
        y0_ = top + 0.03
        blot([(X + fx - w, y0_), (X + fx - w * 0.9, y0_ + ln * 0.8), (X + fx, y0_ + ln), (X + fx + w * 0.9, y0_ + ln * 0.8),
              (X + fx + w, y0_)], rim=0.002, inner=0.0015)
    # drips running on down from the print, still creeping after the hand has gone
    for dx, sp_, dl in ((-0.026, 0.12, 0.0), (0.02, 0.09, 0.3), (-0.004, 0.07, 0.6)):
        ln = min(0.35, sp_ * max(0.0, u - dl))
        if ln > 0:
            xs, ys = X + dx, top - 0.02
            p.poly([P(xs - 0.004, ys), P(xs + 0.004, ys), P(xs + 0.0025, ys - ln), P(xs - 0.0025, ys - ln)], BLOOD_D, None)
            bx, by = P(xs, ys - ln)
            r = 0.0065 * pc.f / pc.depth(z)
            p.ell(bx, by, r, r * 1.3, BLOOD_D, None)


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
        if drop > 0:   # the smear it leaves down the podium's front
            hand_smear(img, cam, pc, X, drop, u - 0.3)
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
    def front(img, cam, pc):   # the smear the hand left on the podium in shot 1 is still there
        hand_smear(img, cam, pc, -0.22, 1.2, 9.0)
    return shot_front(t, zoom=1.32, behind=behind, front=front, **peskov_kw(t))


def film_face(t_local):
    """Shot 3b: a tracking close-up, the camera travelling with her at floor level as she keeps crawling, the phone
    clutched in her fist, her eyes darting back at what's behind her; the hall slides past behind her, out of focus:
    the bloody action she is crawling past. The camera is in the same plan, so what's behind her is really there."""
    from PIL import ImageFilter
    tl = (T['s3b'] - T['s3']) + t_local                          # her clock from the start of shot 3
    since = T['s3'] - T['s2'] + tl
    X = heroine_x(tl)
    pc = PCam(X + 0.12, 0.5, CRAWL_Z - 0.9, 1, 2300.0, oy=960.0)
    x, y = pc.P(X, 0.0, CRAWL_Z)
    s = pc.scale(CRAWL_Z, X)
    stop = CRAWL_STOP - (T['s3b'] - T['s3'])                   # she stops here and lifts the phone to her eyeline
    raise_ph = max(0.0, min(1.0, (t_local - stop) / 0.5))
    head = (x - 208 * s, y - 468 * s)
    cam = B.Cam(1.0, head[0] + 40 * s - 100 * s * F.ease(raise_ph), head[1] + 90 * s)   # eases over to take in the phone
    bg = B.canvas(WALL)
    room(bg, cam, pc, since, chaos=True)
    draw_items(bg, cam, pc, [i for i in chaos_items(pc) if not (i[2] == 'person' and i[3]['kind'] == 'heroine')
                             and pc.depth(*i[:2][::1]) > 0.6], since)
    img = bg.filter(ImageFilter.GaussianBlur(9 * B.SS))
    st, _ = heroine_state(min(tl, CRAWL_STOP))                 # stopped: the crawl frozen where she stopped
    st['raise_ph'] = raise_ph
    if raise_ph > 0:           # her eyes dart about, then lock on the screen (up and to her front, our left)
        u = t_local - stop
        darts = [(0.0, 0.8, 0.3), (0.1, -1.1, -0.5), (0.2, 0.4, 0.2), (0.3, -0.6, 0.4), (0.4, -1.7, -0.4)]
        st['look'], st['look_y'] = [d[1:] for d in darts if d[0] <= u][-1]
    HEROINE.clear()
    HEROINE.update(st)
    crowd_person(img, cam, pc, dict(kind='heroine', k=0, x=X, z=CRAWL_Z, act='crawl'), since)
    HEROINE.clear()
    return img


def film_crawl(t_local):
    """Shot 3: she crawls across, snatching up her phone without stopping."""
    return shot_crawl(T['s3'] - T['s2'] + t_local, tl=t_local)


def phone_parts(t_local, tap):
    """Shot 4 in three layers, so each can move and blood lands only on what it hits: the room behind (out of
    focus), the phone (with the page), her hands."""
    from PIL import ImageFilter
    cam = B.Cam(1.0, 540, 960)
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
    B.shade(bg, 0.18)
    ph = Image.new('RGBA', bg.size, (0, 0, 0, 0))
    T_ = Turned(cam, PHONE_AT[0], PHONE_AT[1], PHONE_ANG)
    p = B.Pen(ph, T_)
    hw, hh = PHONE_W / 2, PHONE_H / 2

    def rrect(w2, h2, r):
        pts = []
        for cx, cy, a0 in ((w2 - r, -h2 + r, -90), (w2 - r, h2 - r, 0), (-w2 + r, h2 - r, 90), (-w2 + r, -h2 + r, 180)):
            pts += [(cx + r * math.cos(math.radians(a0 + k * 15)), cy + r * math.sin(math.radians(a0 + k * 15))) for k in range(7)]
        return pts
    p.poly(rrect(hw, hh, 70), (22, 22, 26), INK, 3.0)
    p.poly(rrect(hw - 4, hh - 4, 66), (44, 44, 52), None)
    S = B.SS
    scr = Image.new('RGBA', (SCREEN_W * S, SCREEN_H * S), (0, 0, 0, 0))
    phone_screen(scr, (0, 0, SCREEN_W, SCREEN_H), t_local, scale=SCREEN_W / 720)
    mask = Image.new('L', scr.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, scr.width - 1, scr.height - 1], 52 * S, fill=255)
    scr.putalpha(mask)
    scr = scr.rotate(-math.degrees(PHONE_ANG), Image.BICUBIC, expand=True)
    cx, cy = cam.P(*PHONE_AT)
    ph.alpha_composite(scr, (int(cx - scr.width / 2), int(cy - scr.height / 2)))
    p.ell(0, -hh + 34, 46, 12, (14, 14, 16), None)            # the camera notch
    for (u, v, r, seed) in ((hw - 70, -250, 10, 45), (hw - 110, 160, 8, 46)):   # drops already on the glass
        splat(p, u, v, r, seed, drops=2)
    old_blood = Image.new('RGBA', bg.size, (0, 0, 0, 0))     # the blood already on her hands from the crawl
    bp = B.Pen(old_blood, T_)
    for (u, v, r, seed) in ((-hw - 70, hh + 230, 20, 41), (hw + 120, hh + 120, 14, 42), (-hw + 150, hh + 40, 9, 43)):
        splat(bp, u, v, r, seed, drops=3)
    return bg, ph, old_blood


def clip_to(lay, mask):
    """Keep only the parts of a layer inside a mask (blood stays on what it hit)."""
    a = np.minimum(np.asarray(lay.getchannel('A')), np.asarray(mask))
    out = lay.copy()
    out.putalpha(Image.fromarray(a.astype(np.uint8)))
    return out


def moved(lay, dx, dy, ang=0.0, about=None):
    """A layer moved by (dx, dy) canvas pixels and turned by ang degrees about a point."""
    if ang:
        lay = lay.rotate(ang, Image.BICUBIC, center=about)
    out = Image.new('RGBA', lay.size, (0, 0, 0, 0))
    out.paste(lay, (int(dx), int(dy)), lay)
    return out


def film_phone(t_local):
    """Shot 4: her phone, held up in her one circle hand (no typing); a roar right behind her (a shadow falls,
    her hands shake); a crunch: blood thrown from above lands on the phone and her hands (only on them: what misses
    flies past); her grip goes: the phone tips out of her hands and falls out of frame, her hands go limp and sink
    away. Each hand is its own whole drawing, so it moves as one piece with its blood."""
    t = T['s4'] + t_local
    tap = 0                            # she only holds it up: no typing
    bg, ph, blood = phone_parts(t_local, tap)
    W_, H_ = bg.size
    S = B.SS
    hand = {sd: phone_hand_layer(sd, tap) for sd in 'LR'}
    masks = {sd: np.asarray(hand[sd].getchannel('A')) for sd in 'LR'}
    air = Image.new('RGBA', bg.size, (0, 0, 0, 0))
    if t >= T['crunch'] - 0.12:        # the spray: drops in flight, then splats on the phone and the hands only
        bp, ap = B.Pen(blood, B.Cam(1.0, 540, 960)), B.Pen(air, B.Cam(1.0, 540, 960))
        hit = np.maximum(np.asarray(ph.getchannel('A')), np.maximum(masks['L'], masks['R']))
        for (x, y, r, ang, dt, seed) in SPRAY:
            ti = T['crunch'] + dt
            on = hit[min(H_ - 1, int(y * S)), min(W_ - 1, int(x * S))] > 128
            if t < ti or not on:           # still flying (or it missed, and flies on past and out of frame)
                u = (t - (ti - 0.12)) / 0.12
                if u < 0 or (not on and u > 4):
                    continue
                fx, fy = x - math.cos(ang) * 700 * (1 - u), y - math.sin(ang) * 700 * (1 - u)
                rr = r * (0.15 + 0.35 * min(u, 1.0))
                ap.poly([(fx - math.cos(ang) * rr * 4, fy - math.sin(ang) * rr * 4),
                         (fx + math.sin(ang) * rr, fy - math.cos(ang) * rr), (fx + math.cos(ang) * rr, fy + math.sin(ang) * rr),
                         (fx - math.sin(ang) * rr, fy + math.cos(ang) * rr)], BLOOD, None)
                continue
            dsplat(bp, x, y, r, ang, seed, max(0.0, t - ti - 0.15) * (240 if r > 60 else 90))
    # the blood belongs to whatever it landed on: each hand, or the phone where no hand covers it
    on_hand = {sd: clip_to(blood, Image.fromarray(masks[sd])) for sd in 'LR'}
    covered = np.maximum(masks['L'], masks['R'])
    ph.alpha_composite(clip_to(blood, Image.fromarray(np.minimum(np.asarray(ph.getchannel('A')), 255 - covered).astype(np.uint8))))
    drop = t - (T['crunch'] + 0.45)
    img = bg.copy()
    if drop <= 0:
        img.alpha_composite(ph)
        for sd in 'LR':
            img.alpha_composite(hand[sd])
            img.alpha_composite(on_hand[sd])
    else:                              # her grip opens: the hands turn out from the wrists and sink; the phone falls
        cx, cy = PHONE_AT[0] * S, PHONE_AT[1] * S
        relax = 0.5 if drop < 0.12 else 1.0
        o = F.ease(min(1.0, drop / 0.3))                          # opening outwards, fast
        sink = max(0.0, drop - 0.15)
        for sd, sgn in (('L', -1), ('R', 1)):
            limp = phone_hand_layer(sd, 0, relax, False)              # whole again: nothing hides any finger now
            mine = clip_to(on_hand[sd], limp.getchannel('A'))
            ang = -sgn * 28 * o
            dx, dy = sgn * 200 * S * o, 1600 * S * sink * sink
            about = (cx + sgn * 260 * S, cy + 700 * S)              # roughly her wrist
            img.alpha_composite(moved(limp, dx, dy, ang=ang, about=about))
            img.alpha_composite(moved(mine, dx, dy, ang=ang, about=about))
        img.alpha_composite(moved(ph, 30 * S * drop, 0.5 * 9000 * S * drop * drop, ang=-140 * drop, about=(cx, cy + 300 * S)))
    img.alpha_composite(air)
    if t >= T['roar']:
        u = min(1.0, (t - T['roar']) / 0.5)
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        g = np.linspace(0.55 * u, 0.0, img.size[1])[:, None] * np.ones((1, img.size[0]))
        lay.putalpha(Image.fromarray(np.clip(g * 255, 0, 255).astype(np.uint8)))
        img.alpha_composite(lay)
        sh = 6 * S * u * math.sin(t * 70) * (1.0 if drop <= 0 else 0.3)    # her hands shaking
        if T['crunch'] <= t < T['crunch'] + 0.2:                   # the jolt as she is bitten
            sh += 26 * S * (1 - (t - T['crunch']) / 0.2)
        k_ = 1.04                                                  # zoomed a touch, so the shake never shows an edge
        cx_, cy_ = img.size[0] / 2, img.size[1] / 2
        img = img.transform(img.size, Image.AFFINE, (1 / k_, 0, cx_ - cx_ / k_ + sh, 0, 1 / k_, cy_ - cy_ / k_ + sh * 0.5),
                            Image.BICUBIC)
    return img


# the spray from the bite: (x, y, size, direction it was flying, when it lands after the crunch, seed). It comes
# from above and behind the phone (where her head is), thrown down and towards us.
# Placed by hand: the big ones round the edges and over her thumbs, small drops across the page, so the words
# "Everything fine. Stop asking questions." stay readable through the blood (that irony is the joke).
SPRAY = sorted([
    (300, 300, 120, 75, 0.00, 11), (860, 520, 130, 100, 0.02, 12), (470, 1180, 150, 85, 0.03, 13),
    (210, 820, 95, 70, 0.05, 14), (760, 1000, 90, 95, 0.04, 15), (930, 1260, 80, 110, 0.07, 16),
    (640, 330, 55, 90, 0.01, 17), (560, 640, 18, 80, 0.06, 18), (380, 520, 14, 72, 0.08, 19), (700, 560, 16, 96, 0.03, 20),
    (300, 1450, 70, 80, 0.06, 21), (820, 1550, 60, 100, 0.09, 22), (150, 520, 40, 65, 0.05, 23), (500, 880, 30, 88, 0.07, 24),
    (640, 780, 22, 92, 0.02, 25), (980, 820, 34, 115, 0.08, 26), (420, 980, 26, 78, 0.09, 27), (760, 220, 30, 104, 0.04, 28),
], key=lambda q: q[4])
SPRAY = [(float(x), float(y), float(r), math.radians(a), dt, sd) for x, y, r, a, dt, sd in SPRAY]


def dsplat(p, x, y, r, ang, seed, run=0.0, colr=BLOOD):
    """A drop that hit the glass while flying in direction `ang`: a blob stretched along its flight, spikes and
    droplets thrown on ahead of it, a short tail behind; `run` (pixels) drips running down from it."""
    rng = np.random.default_rng(seed)
    ca, sa = math.cos(ang), math.sin(ang)
    T_ = lambda u, v: (x + u * ca - v * sa, y + u * sa + v * ca)       # u along the flight, v across it
    n = 16
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        rr = r * rng.uniform(0.82, 1.08)
        pts.append(T_(rr * 1.35 * math.cos(a), rr * 0.85 * math.sin(a)))
    p.poly(curve(pts, 3), colr, B.dk(colr, 0.62), 1.4)
    for _ in range(4 + int(r / 25)):        # spikes thrown forward, each ending in a droplet
        a = rng.uniform(-0.55, 0.55)
        L = r * rng.uniform(1.4, 2.6)
        w = r * rng.uniform(0.1, 0.2)
        base = (r * 1.1 * math.cos(a), r * 0.75 * math.sin(a))
        tip = (base[0] + L * math.cos(a), base[1] + L * math.sin(a))
        p.poly([T_(base[0], base[1] - w), T_(tip[0], tip[1]), T_(base[0], base[1] + w)], colr, None)
        p.ell(*T_(tip[0] + w * 0.6, tip[1]), w * 0.9, w * 0.9, colr, None)
    for _ in range(5 + int(r / 18)):        # loose droplets scattered ahead
        a = rng.uniform(-0.8, 0.8)
        d = r * rng.uniform(1.8, 3.4)
        rd = r * rng.uniform(0.05, 0.14)
        p.ell(*T_(d * math.cos(a), d * math.sin(a)), rd * 1.3, rd, colr, None, rot=ang)
    p.poly([T_(-r * 1.2, -r * 0.25), T_(-r * 2.0, 0), T_(-r * 1.2, r * 0.25)], colr, None)     # the short tail
    if run > 0 and r > 15:                  # drips running straight down the glass
        for k in range(1 + int(r / 50)):
            dx = rng.uniform(-0.6, 0.6) * r
            ln = run * rng.uniform(0.6, 1.0)
            w = max(3.0, r * 0.09)
            p.poly([(x + dx - w, y), (x + dx + w, y), (x + dx + w * 0.8, y + r * 0.4 + ln), (x + dx - w * 0.8, y + r * 0.4 + ln)],
                   colr, None)
            p.ell(x + dx, y + r * 0.4 + ln, w * 1.25, w * 1.4, colr, None)


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
    if title and t < 2.0:   # the standard title over the backdrop, gone by 2 s (Sam)
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


def glass_snd():
    """A window bursting in: a hard crack, a bright spray of breaking glass, then shards tinkling down."""
    out = np.zeros(int(1.4 * SR))
    n = int(0.5 * SR)
    tt = np.arange(n) / SR
    place(out, normal(band(rng.standard_normal(n), 2500, 9000) * np.exp(-tt * 9)), 0.0, 0.9)
    place(out, thud(120, 0.2, 1.0), 0.0, 0.6)
    for k in range(22):
        at = 0.05 + rng.uniform(0, 1.0) ** 1.6
        place(out, M.clink() * 0.5, at, 0.5 * (1 - at / 1.2))
    return normal(out)


def chair_hit():
    """A metal chair smashed into someone: a wet smack and the frame clanging as it buckles."""
    out = np.zeros(int(0.7 * SR))
    place(out, splat_snd(1.2), 0.0, 0.8)
    place(out, thud(110, 0.3, 0.9), 0.0, 0.9)
    for k in range(3):
        place(out, M.clink() * 0.6, 0.01 + 0.05 * k, 0.6 * 0.6 ** k)
        place(out, thud(300 + 40 * k, 0.1, 1.0), 0.01 + 0.05 * k, 0.4 * 0.6 ** k)
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


def soundtrack(stems=False):
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
    g[(tt >= W2[0][1] - 0.2)] = 0.45                             # down further under his last line
    place(mix, bed * g * 0.8, T['s2'])                         # the hall 20% down (Sam)
    vox = np.zeros(n)
    place(vox, rec_lines()[0][0], 0.30)                          # Sam as Peskov
    place(vox, rec_lines()[1][0], W2[0][1], 1.2)                  # 'Any more questions?' 20% up (Sam)
    mix += vox
    # shot 2's big moments, over the din: the window bursting in; the chair; the body hitting the floor and bouncing
    place(mix, glass_snd(), T['s2'] + WIN_BURST, 0.7)
    place(mix, thud(80, 0.4, 0.3), T['s2'] + WIN_BURST + 0.45, 0.4)
    place(mix, chair_hit(), T['s2'] + CHAIR_HIT, 1.0)
    place(mix, thud(65, 0.5, 0.5), T['s2'] + CHAIR_HIT + 0.4, 0.9)
    place(mix, thud(75, 0.25, 0.3), T['s2'] + CHAIR_HIT + 0.55, 0.45)
    place(mix, roar(1.1, 4242, 0.85), T['roar'], 1.0)            # right behind her, not muffled
    place(mix, crunch(), T['crunch'], 1.0)
    place(mix, splat_snd(1.6), T['crunch'] + 0.03, 0.9)
    # shot 5: the arm slaps the wall
    place(mix, slap(), T['arm_hit'], 0.8)
    place(mix, splat_snd(1.0), T['arm_hit'] + 0.01, 0.5)
    if stems:                                                    # for the voice-balance check
        return mix, vox, mix - vox
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
def overlays(img, t):
    """Captions and the title go on LAST, on the finished picture, so a wording or timing note never needs the
    picture re-rendered (same order and same code as frame_image)."""
    if t < T['black']:
        c = caption_at(t)
        if c:
            PP.caption(img, c)
        if t < 2.0:
            title_frame(img, t)
    return img


def render_frame(args):
    i, size, ss, cache, reuse = args
    B.SS = ss
    t = i / FPS
    path = os.path.join(cache, f'{i:04d}.png') if cache else None
    if path and reuse and os.path.exists(path):
        pic = Image.open(path)
        pic.load()
    else:
        pic = frame_image(t, captions=False, title=False)
        if path:
            pic.save(path, compress_level=1)
    return np.asarray(overlays(pic, t).convert('RGB').resize(size, Image.LANCZOS)).tobytes()


def render(out, size, crf, ss, reuse=False, redo=()):
    """Frames are cached (pictures only). reuse=True with redo=('reverse', ...) re-renders only those shots and takes
    every other frame from the cache of the last full render at this size (the cache lives in $FILM_CACHE or
    ~/.cache/filmcache and is only trusted when asked for: it cannot know what code changed)."""
    import subprocess
    import imageio_ffmpeg
    from multiprocessing import Pool
    wav = out + '.wav'
    mix = soundtrack()
    print(f'sound: {MA.lufs(mix):.1f} LUFS, peak {MA.true_peak_db(mix):.1f} dBTP', flush=True)
    MA.write_wav(wav, mix)
    n = int(round(T['dur'] * FPS))
    cache = os.path.join(os.environ.get('FILM_CACHE', os.path.expanduser('~/.cache/filmcache')),
                         f'russiadent-{size[0]}x{size[1]}-ss{ss}')
    os.makedirs(cache, exist_ok=True)
    redo_set = {i for i in range(n) if shot_at(i / FPS)[0] in redo}
    print(f'picture cache: {cache}' + (f' (re-rendering shots {sorted(redo)}, reusing the rest)' if reuse else ''), flush=True)
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{size[0]}x{size[1]}', '-r', str(FPS), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for k, fr in enumerate(pool.imap(render_frame, [(i, size, ss, cache, reuse and i not in redo_set) for i in range(n)], chunksize=2)):
            p.stdin.write(fr)
            if k % 24 == 0:
                print(f'frame {k}/{n}', flush=True)
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print(f'done: {out} ({os.path.getsize(out) / 1e6:.1f} MB)', flush=True)


def check_mouths():
    """Every stretch of speech must move his mouth (once, "Ministry of Health" got through with a still mouth)."""
    for start, (v, stretches) in ((0.30, rec_lines()[0]), (W2[0][1], rec_lines()[1])):
        for a, b in stretches:
            if b - a < 0.25:
                continue
            moving = sum(max(0.0, min(b, y1 - start) - max(a, y0 - start)) for y0, y1, sh in TRACK if sh != 'rest')
            if moving < 0.5 * (b - a):
                raise ValueError(f'check: no mouth movement for the speech at {start + a:.2f}-{start + b:.2f} s')


def print_subtitles():
    """The subtitles as plain text with their times, to proofread before a render (not after)."""
    rows, last = [], None
    for i in range(int(T['black'] * FPS) + 1):
        c = caption_at(i / FPS)
        if c != last:
            rows.append((i / FPS, c))
            last = c
    print('subtitles:')
    for (t, c), nxt in zip(rows, rows[1:] + [(T['black'], None)]):
        if c:
            print(f'  {t:6.2f}-{nxt[0]:6.2f} s  {c}')


def _in_frame(pc, cam, X, Z, pad=60):
    if pc.depth(Z, X) < 0.6:
        return False
    sx, sy = pc.P(X, 1.2, Z)
    return abs(sx - cam.cx) * cam.z < 540 + pad and abs(sy - cam.cy) * cam.z < 960 + pad


def check_closeups_seen_in_wides():
    """Anyone in the close-up's background must already have been seen in shot 2 or 3 (Sam's rule)."""
    pc2, cam2 = cam_reverse()
    pc3, cam3 = PCam(-0.45, 0.42, 1.85, 1, 1150.0, oy=1180.0), B.Cam(1.0, 540, 960)
    s2s3 = [(pc2, cam2, i / 12) for i in range(int((T['s3'] - T['s2']) * 12))] + \
           [(pc3, cam3, (T['s3'] - T['s2']) + i / 12) for i in range(int((T['s3b'] - T['s3']) * 12))]
    for w in CROWD:
        if w['kind'] == 'heroine':
            continue
        seen = any(_in_frame(pc, cam, *where(w, t)) for pc, cam, t in s2s3)
        for j in range(int((T['s4'] - T['s3b']) * 4)):
            tl = (T['s3b'] - T['s3']) + j / 4
            X = heroine_x(tl)
            pcf = PCam(X + 0.12, 0.5, CRAWL_Z - 0.9, 1, 2300.0, oy=960.0)
            x, y = pcf.P(X, 0.0, CRAWL_Z)
            sc = pcf.scale(CRAWL_Z, X)
            camf = B.Cam(1.0, x - 208 * sc + 40 * sc, y - 468 * sc + 90 * sc)
            since = (T['s3'] - T['s2']) + tl
            if w['z'] >= 2.7 and _in_frame(pcf, camf, *where(w, since)) and not seen:
                raise ValueError(f"check: {w['kind']} {w['k']} is in the close-up at {T['s3'] + tl:.1f} s but never "
                                 f"seen in shot 2 or 3")


MARKS = [dict(name='podium smear (shot 1)', box=(0, 1450, 760, 1920), colour=BLOOD_D, tol=70, min=150,
              times=[T['slap'] + 1.6, 11.0]),
         dict(name='podium smear (last shot)', box=(0, 1450, 760, 1920), colour=BLOOD_D, tol=70, min=150,
              times=[T['s5'] + 0.3, T['s5'] + 2.0])]


def checks():
    """Every check that stops a bad render before it starts (best-practice 1.3, guides/preflight.md)."""
    check_crowd()
    check_outfits()
    check_mouths()
    check_closeups_seen_in_wides()
    _, vox, rest = soundtrack(stems=True)
    sp_ = [(0.30 + a, 0.30 + b) for a, b in rec_lines()[0][1]] + [(W2[0][1] + a, W2[0][1] + b) for a, b in rec_lines()[1][1]]
    bad = filmkit.voice_balance(vox, rest, SR, sp_)
    if bad:
        raise ValueError('check: ' + '; '.join(bad))
    print_subtitles()


FAST_OK = {('zombie', 5): (1.5, 4.0, 'thrown by the chair; the blood pool under its head is a separate shape'), ('zombie', 20): (0.55, 1.35, 'topples through the window'),
           ('zombie', 21): (0.55, 1.7, 'climbs in')}


def _views():
    pc2, cam2 = cam_reverse()
    pc3, cam3 = PCam(-0.45, 0.42, 1.85, 1, 1150.0, oy=1180.0), B.Cam(1.0, 540, 960)
    return (('shot 2', pc2, cam2, (0.0, T['s3'] - T['s2'])), ('shot 3', pc3, cam3, (T['s3'] - T['s2'], T['s3b'] - T['s2'])))


def _audit_draw(vi, members, hero):
    label, pc, cam, win = _views()[vi]

    def draw(t):
        lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
        PENDING.clear()
        HEROINE.clear()
        tl = t - (T['s3'] - T['s2'])
        if hero:
            st, _ = heroine_state(tl)
            HEROINE.update(st)
        for i in members:
            w = CROWD[i]
            if hero:
                w = dict(w, x=heroine_x(tl), z=CRAWL_Z, v=(0.0, 0.0))
            crowd_person(lay, cam, pc, w, t)
        HEROINE.clear()
        return lay
    return draw


def _audit_one(spec):
    import filmkit
    name, vi, members, times, hero, allow = spec
    filmkit.EYES.clear()
    out = filmkit.silhouette_audit({name: (times, _audit_draw(vi, members, hero))}, fps=12, allow=allow)
    return out + filmkit.check_eyelines()


def audit_specs():
    """Every character (an attacker with their victim as one) alone, in every shot that shows them, as runs of
    consecutive frames. Nothing here is specific to arms, necks or legs: it tests the drawn result."""
    groups = {}
    for i, w in enumerate(CROWD):      # only a biter and its victim are one body (the biter's head is drawn by the victim)
        if w['kind'] != 'heroine':
            bite = w['act'] in ('tackle', 'tackled')
            groups.setdefault(w['pair'] if bite else f'solo{i}', []).append(i)
    for key in groups:      # a biting zombie is drawn first (its victim draws its head)
        groups[key].sort(key=lambda i: CROWD[i]['act'] != 'tackle')
    specs = []
    for vi, (label, pc, cam, (t0, t1)) in enumerate(_views()):
        frames = [t0 + j / 12 for j in range(int((t1 - t0) * 12))]
        units = [(f'{" + ".join(CROWD[i]["kind"] + " " + str(CROWD[i]["k"]) for i in m)} [{label}]', m, False)
                 for m in groups.values()]
        if vi == 1:
            units.append(('heroine [shot 3]', [next(i for i, w in enumerate(CROWD) if w['kind'] == 'heroine')], True))
        for name, m, hero in units:
            on = []
            for t in frames:
                if hero:
                    on.append(True)
                    continue
                vis = []
                for i in m:
                    X, Z = where(CROWD[i], t)
                    ok = pc.depth(Z, X) >= 1.1 and -40 < pc.P(X, 1.0, Z)[0] < 1120 and (vi == 0 or CROWD[i]['z'] >= 2.7)
                    vis.append(ok)
                on.append(any(vis))
            runs, cur = [], []
            for t, o in zip(frames, on):
                if o:
                    cur.append(t)
                elif cur:
                    runs.append(cur)
                    cur = []
            if cur:
                runs.append(cur)
            for n, run in enumerate(runs):
                if len(run) < 3:
                    continue
                allow = [(f'{name}#{n}', a, b, why) for (kind, k), (a, b, why) in FAST_OK.items()
                         if any(CROWD[i]['kind'] == kind and CROWD[i]['k'] == k for i in m)]
                specs.append((f'{name}#{n}', vi, m, run, hero, allow))
    return specs


def audits():
    """The general audit (guides/preflight.md): the body, the movement and the permanent marks, over the whole film."""
    import filmkit
    from multiprocessing import Pool
    B.SS = 1                           # quick and small: the audit looks at shapes, not finish
    faults = []
    specs = audit_specs()
    with Pool(os.cpu_count()) as pool:
        for r in pool.imap_unordered(_audit_one, specs):
            faults += r
    faults += filmkit.probe_marks(lambda t: frame_image(t, captions=False, title=False), MARKS)
    print(f'audit: {len(specs)} runs of characters checked')
    return sorted(faults)


def cast_sheet(out):
    """Every reporter and zombie on one sheet, to approve the cast BEFORE any animation (one cheap render)."""
    class C:
        s = 1.0

        def P(self, x, y):
            return (x, y)

        def S(self, v):
            return v
    img = Image.new('RGBA', (2400, 1800), (230, 226, 220, 255))
    for i, k in enumerate(sorted(CAST)):
        sp = reporter_base(k)
        sp['arms'] = F.Rig(sp).pose('sides')
        person(img, C(), 130 + i * 260, 330, 0.36, sp, 0.3)
    for i, k in enumerate(sorted(ZCAST)):
        sp = zombie_base(k)
        rig = F.Rig(sp)
        sp['arms'] = {'L': rig.arm('L', (-190, -170), 'palm', 'out', strict=False), 'R': rig.arm('R', (200, -150), 'palm', 'out', strict=False)}
        person(img, C(), 110 + (i % 10) * 230, 900 + (i // 10) * 520, 0.32, sp, 0.3)
    img.convert('RGB').save(out)


def main():
    mode = sys.argv[1]
    if mode in ('stills', 'animatic', 'final'):
        checks()
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
    elif mode in ('animatic', 'final'):
        redo = tuple(sys.argv[sys.argv.index('--redo') + 1].split(',')) if '--redo' in sys.argv else ()
        reuse = '--reuse' in sys.argv
        render(sys.argv[2], (540, 960) if mode == 'animatic' else (1080, 1920), 26 if mode == 'animatic' else 20,
               1 if mode == 'animatic' else 2, reuse, redo)
    elif mode == 'cast':
        cast_sheet(sys.argv[2])


F.guard(B)   # every arm drawn is measured against the rig; a wrong one stops the render (guides/figure-rig.md)

if __name__ == '__main__':
    main()
