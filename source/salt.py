#!/usr/bin/env python3
"""The Salt: a short comedy animation in pencil.

A stately couple dine at an absurdly long table. She asks for the salt.
He obliges, from the top of the half-pipe his end of the table curls into.

Usage:
    python3 salt.py stills OUT_DIR T1 T2 ...   # save single frames at given seconds
    python3 salt.py render OUT.mp4 [CRF]       # render the full video with sound
"""
import math
import os
import sys

import numpy as np
from PIL import Image

from pencil import Canvas, Track, blob, clamp01, col, ell, lerp, noise, render_video, sstep, tt, decay, \
    W, H, FPS, SR

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Palette: Bleak House greys, with colour only in the food, the wine, the flames and the salt
# ---------------------------------------------------------------------------
INK = col(0.14, 0.14, 0.15)
WALL = col(0.56, 0.57, 0.52)
WALL_D = col(0.47, 0.48, 0.44)
CEILING = col(0.44, 0.44, 0.41)
WAINSCOT = col(0.36, 0.33, 0.30)
FLOOR = col(0.33, 0.30, 0.27)
RUG = col(0.42, 0.28, 0.28)
WOOD = col(0.30, 0.25, 0.21)
WOOD_L = col(0.45, 0.39, 0.33)
PLY = col(0.62, 0.56, 0.46)
STONE = col(0.62, 0.60, 0.55)
STONE_D = col(0.48, 0.46, 0.42)
CLOTH = col(0.86, 0.85, 0.80)
CLOTH_S = col(0.70, 0.70, 0.66)
FRAME = col(0.50, 0.44, 0.33)
CANVAS_D = col(0.30, 0.31, 0.29)
DRAPE = col(0.40, 0.27, 0.29)
NIGHT_GLASS = col(0.36, 0.42, 0.50)
SKIN = col(0.86, 0.79, 0.72)
SKIN_S = col(0.74, 0.66, 0.60)
ROUGE = col(0.80, 0.60, 0.58)
GOWN = col(0.43, 0.37, 0.43)
GOWN_L = col(0.55, 0.49, 0.54)
GLOVE = col(0.84, 0.82, 0.78)
GLOVE_S = col(0.70, 0.68, 0.65)
HAIR_W = col(0.47, 0.42, 0.40)
HAIR_H = col(0.72, 0.72, 0.72)
COAT = col(0.25, 0.26, 0.28)
COAT_L = col(0.35, 0.36, 0.38)
SHIRT = col(0.92, 0.91, 0.88)
PEARL = col(0.93, 0.92, 0.88)
SILVER = col(0.72, 0.73, 0.75)
FLAME = col(1.0, 0.86, 0.45)
GLOW = col(1.0, 0.84, 0.55)
WINE = col(0.55, 0.06, 0.10)
GLASS = col(0.85, 0.88, 0.90)
PLATE = col(0.97, 0.97, 0.96)
CHICKEN = col(0.80, 0.55, 0.30)
POTATO = col(0.93, 0.80, 0.45)
PEA = col(0.40, 0.66, 0.30)
CARROT = col(0.95, 0.52, 0.18)
GRAVY = col(0.50, 0.33, 0.18)
SALT = col(0.99, 0.99, 1.0)
SALT_S = col(0.80, 0.84, 0.90)
WHITE = col(1.0, 1.0, 1.0)


class SharpCanvas(Canvas):
    """Pencil with firm pressure and steady lines: crisp shapes, only a hint of paper grain."""
    def poly(self, pts, fill=None, line=None, lw=5, pressure=0.85, lp=0.95, jit=2.2, **kw):
        super().poly(pts, fill, line, lw=lw, pressure=max(pressure, 1.2), lp=max(lp, 1.25), jit=jit * 0.35, **kw)

    def fill_screen(self, color, pressure=0.9, opacity=1.0):
        super().fill_screen(color, max(pressure, 1.2), opacity)


# ---------------------------------------------------------------------------
# Timeline (seconds)
# ---------------------------------------------------------------------------
T_SPEAK_W = 3.2      # "Darling, would you pass the salt?"
T_CUT_H = 7.6        # cut to the husband
T_SPEAK_H = 8.0      # "Of course!"
T_WHIP = 11.9        # camera jerks back and away
T_WHIP_END = 12.35
T_TURN = 12.9        # he sets down his cutlery and turns to the salt
T_PAT1 = 13.55       # pat
T_PAT2 = 13.95       # pat
T_WIND = 14.25       # wind-up
T_SLAP = 14.75       # SLAP
ROLL_DECK, ROLL_CURVE, ROLL_FLAT = 0.45, 0.5, 1.15
T_HIT = T_SLAP + ROLL_DECK + ROLL_CURVE + ROLL_FLAT   # the salt arrives
DUR = round(T_HIT + 0.6, 2)                          # and we end sharply on the crash

# ---------------------------------------------------------------------------
# The room, in metres. x runs along the table (wife at 0), y is up, z is across.
# ---------------------------------------------------------------------------
TABLE_Y = 0.75
FLAT_END = 11.0          # the ordinary part of the table
RAMP_R = 3.2             # the half-pipe curve
LIP_X = FLAT_END + RAMP_R
LIP_Y = TABLE_Y + RAMP_R
DECK_END = 16.5          # the flat top where he dines, with a hole he sits in
HALF_W = 0.7
WALL_Z = 3.6
END_WALL_W = -3.2
END_WALL_H = 18.2
CEIL = 5.6

WIFE_SEAT = (-0.25, 0.48, 0.0)
HUSB_SEAT = (15.65, LIP_Y - 0.25, 0.0)
HOLE = (15.65, 0.36, 0.3)          # centre x, radius along x, radius across
HIS_PLATE = (15.12, LIP_Y, 0.0)
SHELF = (15.15, 16.15, HALF_W, 1.58)   # x0, x1, z0, z1: the little shelf the salt waits on
BOULDER_R = 0.42
BOULDER_START = (15.65, LIP_Y + BOULDER_R, 1.12)
TABLE_CANDLES = [(x, 0.0) for x in np.arange(2.2, FLAT_END - 0.5, 2.2)]


def ramp_point(a):
    """Point on the curved table surface, a = 0 (bottom) .. pi/2 (top)."""
    return FLAT_END + RAMP_R * math.sin(a), TABLE_Y + RAMP_R - RAMP_R * math.cos(a)


# ---------------------------------------------------------------------------
# Camera and 3D drawing helpers
# ---------------------------------------------------------------------------
class Cam:
    def __init__(self, pos, target, fov=50.0):
        self.pos = np.array(pos, float)
        f = np.array(target, float) - self.pos
        self.f = f / np.linalg.norm(f)
        r = np.cross(self.f, [0.0, 1.0, 0.0])
        self.r = r / np.linalg.norm(r)
        self.u = np.cross(self.r, self.f)
        self.focal = (H / 2) / math.tan(math.radians(fov) / 2)

    def depth(self, p):
        return float(np.dot(np.asarray(p, float) - self.pos, self.f))

    def proj(self, pts):
        p = np.asarray(pts, float).reshape(-1, 3) - self.pos
        xc, yc, zc = p @ self.r, p @ self.u, p @ self.f
        zc = np.maximum(zc, 1e-3)
        return np.stack([W / 2 + self.focal * xc / zc, H / 2 - self.focal * yc / zc], 1), zc

    def scale(self, p):
        return self.focal / max(0.05, self.depth(p))

    def pt(self, p):
        s, _ = self.proj([p])
        return float(s[0, 0]), float(s[0, 1])

    def to_cam(self, pts):
        p = np.asarray(pts, float).reshape(-1, 3) - self.pos
        return np.stack([p @ self.r, p @ self.u, p @ self.f], 1)

    def screen(self, pc):
        return np.stack([W / 2 + self.focal * pc[:, 0] / pc[:, 2], H / 2 - self.focal * pc[:, 1] / pc[:, 2]], 1)


def _clip_near(pc, near, closed=True):
    """Cut a polygon (or polyline) at the camera's near plane so nothing behind the lens is drawn."""
    out = []
    n = len(pc)
    rng = range(n) if closed else range(n - 1)
    if not closed and n and pc[0, 2] >= near:
        out.append(pc[0])
    for i in rng:
        a, b = pc[i], pc[(i + 1) % n]
        ain, bin_ = a[2] >= near, b[2] >= near
        if ain and bin_:
            out.append(b)
        elif ain and not bin_:
            out.append(a + (b - a) * (near - a[2]) / (b[2] - a[2]))
        elif not ain and bin_:
            out.append(a + (b - a) * (near - a[2]) / (b[2] - a[2]))
            out.append(b)
    return np.array(out)


def poly3(c, cam, pts, fill=None, line=None, near=0.15, **kw):
    pc = _clip_near(cam.to_cam(pts), near)
    if len(pc) < 3:
        return
    c.poly(cam.screen(pc), fill=fill, line=line, **kw)


def line3(c, cam, pts, colr, lw=3, near=0.15, **kw):
    pc = _clip_near(cam.to_cam(pts), near, closed=False)
    if len(pc) < 2:
        return
    c.line(cam.screen(pc), colr, lw=lw, **kw)


def circle3(center, radius, n=28, axis='y', rz=None):
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    cx, cy, cz = center
    r2 = radius if rz is None else rz
    if axis == 'y':
        return np.stack([cx + radius * np.cos(th), np.full(n, cy), cz + r2 * np.sin(th)], 1)
    if axis == 'z':
        return np.stack([cx + radius * np.cos(th), cy + r2 * np.sin(th), np.full(n, cz)], 1)
    return np.stack([np.full(n, cx), cy + r2 * np.sin(th), cz + radius * np.cos(th)], 1)


def wall_x(xw, pts):
    """Points drawn on an end wall (x = xw), given as (z, y)."""
    return [(xw, y, z) for z, y in pts]


def smooth_closed(pts, n=6):
    """A smooth closed curve through the given points (Catmull-Rom)."""
    p = np.asarray(pts, float)
    out = []
    m = len(p)
    for i in range(m):
        p0, p1, p2, p3 = p[i - 1], p[i], p[(i + 1) % m], p[(i + 2) % m]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    return out


def capsule(a, b, ra, rb, n=8):
    (ax, ay), (bx, by) = a, b
    ang = math.atan2(by - ay, bx - ax)
    pts = [(bx + rb * math.cos(ang + q), by + rb * math.sin(ang + q)) for q in np.linspace(-math.pi / 2, math.pi / 2, n)]
    pts += [(ax + ra * math.cos(ang + q), ay + ra * math.sin(ang + q)) for q in np.linspace(math.pi / 2, 3 * math.pi / 2, n)]
    return pts


# ---------------------------------------------------------------------------
# The room
# ---------------------------------------------------------------------------
_rr = np.random.default_rng(3)
PAINTINGS = [(x, _rr.uniform(2.3, 2.9), _rr.uniform(1.0, 1.4), _rr.uniform(1.2, 1.6), i)
             for i, x in enumerate([-1.5, 2.2, 5.6, 9.0, 12.4, 15.8])]


def room(c, cam, t):
    c.fill_screen(WALL, 1.2)
    # floor, boards running the length of the hall, and a long rug under the table
    for x0 in np.arange(-4, 19, 1.0):
        poly3(c, cam, [(x0, 0, -8), (x0 + 1, 0, -8), (x0 + 1, 0, WALL_Z), (x0, 0, WALL_Z)], fill=FLOOR, jit=0.3)
    for z0 in np.arange(-8, WALL_Z, 0.25):
        for x0 in np.arange(-4, 19, 3.0):
            line3(c, cam, [(x0, 0.001, z0), (x0 + 3, 0.001, z0)], col(0.26, 0.23, 0.21), lw=2, opacity=0.5)
    for x0 in np.arange(-2.5, 17.5, 1.0):
        poly3(c, cam, [(x0, 0.002, -1.3), (x0 + 1, 0.002, -1.3), (x0 + 1, 0.002, 1.3), (x0, 0.002, 1.3)],
              fill=RUG, jit=0.3)
    for zz in (-1.15, 1.15):
        line3(c, cam, [(-2.5, 0.003, zz), (17.5, 0.003, zz)], col(0.62, 0.52, 0.40), lw=3)
    # ceiling with beams
    if cam.pos[1] < CEIL:
        for x0 in np.arange(-4, 19, 1.0):
            poly3(c, cam, [(x0, CEIL, -8), (x0 + 1, CEIL, -8), (x0 + 1, CEIL, WALL_Z), (x0, CEIL, WALL_Z)],
                  fill=CEILING, jit=0.3)
        for x0 in np.arange(-3, 18.2, 2.0):
            poly3(c, cam, [(x0, CEIL - 0.001, -8), (x0 + 0.25, CEIL - 0.001, -8), (x0 + 0.25, CEIL - 0.001, WALL_Z),
                           (x0, CEIL - 0.001, WALL_Z)], fill=WOOD, line=INK, lw=2)
    # the long side wall: striped paper, wainscot, cornice
    poly3(c, cam, [(END_WALL_W, 0, WALL_Z), (END_WALL_H, 0, WALL_Z), (END_WALL_H, CEIL, WALL_Z),
                   (END_WALL_W, CEIL, WALL_Z)], fill=WALL, jit=0.5)
    for x0 in np.arange(END_WALL_W, END_WALL_H, 0.5):
        line3(c, cam, [(x0, 1.1, WALL_Z - 0.001), (x0, CEIL, WALL_Z - 0.001)], WALL_D, lw=4, opacity=0.5)
    poly3(c, cam, [(END_WALL_W, 0, WALL_Z - 0.01), (END_WALL_H, 0, WALL_Z - 0.01), (END_WALL_H, 1.1, WALL_Z - 0.01),
                   (END_WALL_W, 1.1, WALL_Z - 0.01)], fill=WAINSCOT, jit=0.5)
    line3(c, cam, [(END_WALL_W, 1.1, WALL_Z - 0.02), (END_WALL_H, 1.1, WALL_Z - 0.02)], WOOD, lw=5)
    line3(c, cam, [(END_WALL_W, CEIL - 0.15, WALL_Z - 0.02), (END_WALL_H, CEIL - 0.15, WALL_Z - 0.02)], WOOD_L, lw=6)
    for x0 in np.arange(END_WALL_W + 0.3, END_WALL_H, 1.2):
        poly3(c, cam, [(x0, 0.2, WALL_Z - 0.02), (x0 + 0.9, 0.2, WALL_Z - 0.02), (x0 + 0.9, 0.9, WALL_Z - 0.02),
                       (x0, 0.9, WALL_Z - 0.02)], None, WOOD, lw=2, opacity=0.8)
    # end walls (only the ones the camera faces)
    for xw in (END_WALL_W, END_WALL_H):
        if (xw == END_WALL_W and cam.pos[0] < xw) or (xw == END_WALL_H and cam.pos[0] > xw):
            continue
        poly3(c, cam, [(xw, 0, -8), (xw, 0, WALL_Z), (xw, CEIL, WALL_Z), (xw, CEIL, -8)], fill=WALL_D, jit=0.5)
        poly3(c, cam, [(xw, 0, -8), (xw, 0, WALL_Z), (xw, 1.1, WALL_Z), (xw, 1.1, -8)], fill=WAINSCOT, jit=0.5)
        line3(c, cam, [(xw, CEIL - 0.15, -8), (xw, CEIL - 0.15, WALL_Z)], WOOD_L, lw=6)
    line3(c, cam, [(END_WALL_W, 0, WALL_Z), (END_WALL_W, CEIL, WALL_Z)], INK, lw=3, opacity=0.6)
    line3(c, cam, [(END_WALL_H, 0, WALL_Z), (END_WALL_H, CEIL, WALL_Z)], INK, lw=3, opacity=0.6)
    # noble ancestors, and stag heads between them
    for (x, y, w, h, i) in PAINTINGS:
        z = WALL_Z - 0.03
        poly3(c, cam, [(x - w / 2 - 0.1, y - h / 2 - 0.1, z), (x + w / 2 + 0.1, y - h / 2 - 0.1, z),
                       (x + w / 2 + 0.1, y + h / 2 + 0.1, z), (x - w / 2 - 0.1, y + h / 2 + 0.1, z)], fill=FRAME,
              line=INK, lw=3)
        poly3(c, cam, [(x - w / 2, y - h / 2, z - 0.01), (x + w / 2, y - h / 2, z - 0.01),
                       (x + w / 2, y + h / 2, z - 0.01), (x - w / 2, y + h / 2, z - 0.01)], fill=CANVAS_D)
        poly3(c, cam, [(x - w * 0.35, y - h / 2, z - 0.02), (x - w * 0.25, y - h * 0.05, z - 0.02),
                       (x + w * 0.25, y - h * 0.05, z - 0.02), (x + w * 0.35, y - h / 2, z - 0.02)],
              fill=col(0.22, 0.22, 0.22))
        poly3(c, cam, circle3((x, y + h * 0.13, z - 0.02), w * 0.16, 16, 'z'), fill=col(0.62, 0.57, 0.52))
        tx = x + (w / 2 + 0.95)
        if tx < END_WALL_H - 0.6:
            poly3(c, cam, circle3((tx, y + 0.1, z), 0.16, 12, 'z'), fill=WOOD, line=INK, lw=2)
            for sgn in (-1, 1):
                pts = [(tx + sgn * 0.08, y + 0.2, z), (tx + sgn * 0.3, y + 0.55, z), (tx + sgn * 0.42, y + 0.85, z)]
                line3(c, cam, pts, col(0.66, 0.60, 0.50), lw=4)
                for k in range(3):
                    b = pts[1] if k < 2 else pts[2]
                    line3(c, cam, [(b[0] - sgn * 0.02 * k, b[1] - 0.05 * k, z),
                                   (b[0] + sgn * (0.02 + 0.08 * k), b[1] + 0.2, z)], col(0.66, 0.60, 0.50), lw=3)
    if cam.pos[0] < END_WALL_H:
        grand_window(c, cam, t)
        crest(c, cam)
    if cam.pos[0] > END_WALL_W:
        fireplace(c, cam, t)


def grand_window(c, cam, t):
    xw = END_WALL_H - 0.02
    zc, zw, y0, y1 = -2.4, 0.9, 1.1, 3.9
    arch = [(zc + zw * math.cos(q), y1 + zw * math.sin(q)) for q in np.linspace(0, math.pi, 16)]
    outline = [(zc + zw, y0)] + arch + [(zc - zw, y0)]
    frame = [(zc + zw + 0.12, y0 - 0.12)] + \
            [(zc + (zw + 0.12) * math.cos(q), y1 + (zw + 0.12) * math.sin(q)) for q in np.linspace(0, math.pi, 16)] + \
            [(zc - zw - 0.12, y0 - 0.12)]
    poly3(c, cam, wall_x(xw, frame), fill=STONE, line=INK, lw=3)
    poly3(c, cam, wall_x(xw - 0.01, outline), fill=NIGHT_GLASS, line=INK, lw=3)
    # a pale moon through the glass
    mz, my = zc + 0.35, y1 + 0.2
    poly3(c, cam, wall_x(xw - 0.015, [(mz + 0.16 * math.cos(q), my + 0.16 * math.sin(q))
                                     for q in np.linspace(0, 2 * math.pi, 16, endpoint=False)]),
          fill=col(0.86, 0.87, 0.84))
    for z in (zc - zw / 3, zc + zw / 3):
        line3(c, cam, wall_x(xw - 0.02, [(z, y0), (z, y1 + math.sqrt(max(0.0, zw ** 2 - (z - zc) ** 2)))]), INK, lw=4)
    for y in np.arange(y0 + 0.55, y1 + 0.8, 0.55):
        half = zw if y <= y1 else math.sqrt(max(0.0, zw ** 2 - (y - y1) ** 2))
        line3(c, cam, wall_x(xw - 0.02, [(zc - half, y), (zc + half, y)]), INK, lw=3)
    # heavy drapes and a swag
    for sgn in (-1, 1):
        zin, zout = zc + sgn * (zw - 0.15), zc + sgn * (zw + 0.55)
        pts = [(zout, 0.1), (zout, CEIL - 0.3), (zin, CEIL - 0.3), (zin + sgn * 0.05, y1 + 0.3),
               (zin + sgn * 0.25, 2.2), (zin + sgn * 0.15, 0.1)]
        poly3(c, cam, wall_x(xw - 0.04, pts), fill=DRAPE, line=INK, lw=3)
        for k in range(3):
            zz = zout - sgn * (0.12 + 0.13 * k)
            line3(c, cam, wall_x(xw - 0.045, [(zz, 0.15), (zz, CEIL - 0.35)]), col(0.3, 0.2, 0.22), lw=2, opacity=0.7)
    swag = [(zc - zw - 0.55, CEIL - 0.3), (zc + zw + 0.55, CEIL - 0.3)] + \
           [(zc + (zw + 0.55) * math.cos(q), CEIL - 0.3 - 0.35 * math.sin(q)) for q in np.linspace(0, math.pi, 14)]
    poly3(c, cam, wall_x(xw - 0.05, swag), fill=DRAPE, line=INK, lw=3)


def crest(c, cam):
    """The family arms: crossed pickaxes over a block of salt, for a fortune made in salt mines."""
    xw = END_WALL_H - 0.03
    zc, yc, sw, sh = 0.0, 5.2, 0.38, 0.4
    for sgn in (-1, 1):
        for k in range(3):
            pts = [(zc + sgn * (0.26 + 0.13 * k) + 0.1 * math.cos(q), yc + 0.15 - 0.18 * k + 0.09 * math.sin(q))
                   for q in np.linspace(0, 2 * math.pi, 10, endpoint=False)]
            poly3(c, cam, wall_x(xw, pts), fill=col(0.55, 0.55, 0.52), line=INK, lw=2)
    shield = [(zc - sw, yc + sh * 0.6), (zc + sw, yc + sh * 0.6)] + \
             [(zc + sw * math.cos(q), yc + sh * 0.6 - sh * 1.1 * math.sin(q) ** 1.3) for q in np.linspace(0, math.pi, 16)]
    poly3(c, cam, wall_x(xw - 0.01, shield), fill=col(0.42, 0.45, 0.52), line=INK, lw=3)
    poly3(c, cam, wall_x(xw - 0.012, [(zc - sw, yc + sh * 0.6), (zc + sw, yc + sh * 0.6), (zc + sw, yc + sh * 0.3),
                                      (zc - sw, yc + sh * 0.3)]), fill=col(0.62, 0.55, 0.36), line=INK, lw=2)
    # crossed pickaxes
    for sgn in (-1, 1):
        line3(c, cam, wall_x(xw - 0.02, [(zc - sgn * 0.28, yc - 0.26), (zc + sgn * 0.28, yc + 0.2)]), WOOD_L, lw=5)
        hz, hy = zc + sgn * 0.28, yc + 0.2
        line3(c, cam, wall_x(xw - 0.025, [(hz - 0.1, hy + 0.05), (hz, hy), (hz + 0.07, hy - 0.09)]), SILVER, lw=5)
    # the block of salt, gleaming
    poly3(c, cam, wall_x(xw - 0.03, [(zc - 0.1, yc - 0.09), (zc + 0.1, yc - 0.09), (zc + 0.1, yc + 0.09),
                                     (zc - 0.1, yc + 0.09)]), fill=SALT, line=INK, lw=2)
    poly3(c, cam, wall_x(xw - 0.031, [(zc - 0.1, yc + 0.09), (zc - 0.04, yc + 0.14), (zc + 0.15, yc + 0.14),
                                      (zc + 0.1, yc + 0.09)]), fill=SALT_S, line=INK, lw=2)
    # coronet and a motto scroll
    cor = [(zc - 0.2, yc + sh * 0.62), (zc + 0.2, yc + sh * 0.62), (zc + 0.22, yc + sh * 0.85), (zc + 0.11, yc + sh * 0.75),
           (zc, yc + sh * 0.9), (zc - 0.11, yc + sh * 0.75), (zc - 0.22, yc + sh * 0.85)]
    poly3(c, cam, wall_x(xw - 0.01, cor), fill=col(0.62, 0.55, 0.36), line=INK, lw=2)
    scroll = [(zc - 0.42, yc - 0.28), (zc + 0.42, yc - 0.28), (zc + 0.48, yc - 0.39), (zc + 0.38, yc - 0.36),
              (zc + 0.34, yc - 0.42), (zc - 0.34, yc - 0.42), (zc - 0.38, yc - 0.36), (zc - 0.48, yc - 0.39)]
    poly3(c, cam, wall_x(xw - 0.01, scroll), fill=col(0.84, 0.82, 0.76), line=INK, lw=2)
    for k in range(6):
        z0 = zc - 0.3 + k * 0.1
        line3(c, cam, wall_x(xw - 0.015, [(z0, yc - 0.36), (z0 + 0.04, yc - 0.34), (z0 + 0.07, yc - 0.37)]), INK, lw=2)


def fireplace(c, cam, t):
    """A stone fireplace behind the wife, with a clock and candlesticks on the mantel."""
    xw = END_WALL_W + 0.02
    poly3(c, cam, [(xw, y, z) for z, y in [(-1.1, 0), (1.1, 0), (1.1, 1.2), (-1.1, 1.2)]], fill=STONE, line=INK, lw=3)
    opening = [(-0.55, 0), (0.55, 0), (0.55, 0.62)] + \
              [(0.55 * math.cos(q), 0.62 + 0.2 * math.sin(q)) for q in np.linspace(0, math.pi, 10)] + [(-0.55, 0.62)]
    poly3(c, cam, [(xw + 0.01, y, z) for z, y in opening], fill=col(0.12, 0.11, 0.11), line=INK, lw=3)
    for k in range(6):
        p = (xw + 0.12, 0.08 + 0.03 * (k % 2), -0.35 + 0.14 * k)
        if cam.depth(p) > 0.3:
            sx, sy = cam.pt(p)
            s = cam.scale(p)
            c.glow(sx, sy, 0.25 * s, col(1.0, 0.5, 0.2), 0.25 + 0.1 * math.sin(t * 5 + k))
            c.poly(ell(sx, sy, 0.06 * s, 0.03 * s, 0, 10), fill=col(0.55, 0.22, 0.12), line=INK, lw=2)
    for z in (-0.95, 0.95):
        poly3(c, cam, [(xw + 0.015, 0.05, z - 0.12), (xw + 0.015, 0.05, z + 0.12), (xw + 0.015, 1.15, z + 0.12),
                       (xw + 0.015, 1.15, z - 0.12)], fill=STONE_D, line=INK, lw=2)
    poly3(c, cam, [(xw, 1.2, -1.3), (xw, 1.2, 1.3), (xw + 0.28, 1.2, 1.3), (xw + 0.28, 1.2, -1.3)], fill=STONE,
          line=INK, lw=3)
    poly3(c, cam, [(xw + 0.28, 1.2, -1.3), (xw + 0.28, 1.2, 1.3), (xw + 0.28, 1.1, 1.3), (xw + 0.28, 1.1, -1.3)],
          fill=STONE_D, line=INK, lw=2)
    ck = [(xw + 0.12, y, z) for z, y in [(-0.2, 1.2), (0.2, 1.2), (0.2, 1.45)] +
          [(0.2 * math.cos(q), 1.45 + 0.15 * math.sin(q)) for q in np.linspace(0, math.pi, 10)] + [(-0.2, 1.45)]]
    poly3(c, cam, ck, fill=WOOD, line=INK, lw=2)
    poly3(c, cam, circle3((xw + 0.2, 1.47, 0.0), 0.1, 16, 'x'), fill=col(0.9, 0.88, 0.82), line=INK, lw=2)
    for z in (-0.8, 0.8):
        candle(c, cam, (xw + 0.14, 1.2, z), t, 90 + int(z * 10), h=0.3)


def chandelier(c, cam, t, pos=(6.5, 4.3, 0.0)):
    x, y, z = pos
    line3(c, cam, [(x, CEIL, z), (x, y + 0.5, z)], INK, lw=2)
    for k in range(3):
        s, zc = cam.proj(circle3((x, y - 0.15 * k, z), 0.9 - 0.25 * k, 24))
        if (zc > 0.2).all():
            c.poly(s, None, col(0.55, 0.52, 0.46), lw=3)
    for k in range(8):
        a = k / 8 * 2 * math.pi
        bx, bz = x + 0.9 * math.cos(a), z + 0.9 * math.sin(a)
        line3(c, cam, [(bx, y, bz), (bx, y + 0.18, bz)], PLATE, lw=5)
        flame_at(c, cam, (bx, y + 0.24, bz), t, k, size=0.05)
    if cam.depth((x, y, z)) > 0.3:
        gx, gy = cam.pt((x, y, z))
        c.glow(gx, gy, cam.scale((x, y, z)) * 2.5, GLOW, 0.22)


def flame_at(c, cam, p, t, seed, size=0.03):
    if cam.depth(p) < 0.2:
        return
    sx, sy = cam.pt(p)
    s = cam.scale(p) * size
    flick = 1 + 0.18 * math.sin(t * 13 + seed * 1.7) + 0.08 * math.sin(t * 31 + seed)
    c.glow(sx, sy, s * 6, GLOW, 0.35)
    pts = [(sx + s * 0.6 * math.sin(q), sy - s * flick * (1.6 - 1.6 * math.cos(q)) * 0.6 + s * 0.3)
           for q in np.linspace(0, 2 * math.pi, 14)]
    c.poly(pts, fill=FLAME, jit=0.3)
    c.poly([(sx, sy - s * 1.4 * flick), (sx + s * 0.25, sy), (sx - s * 0.25, sy)], fill=WHITE, jit=0.2)


# ---------------------------------------------------------------------------
# The table, the half-pipe it becomes, and the deck he dines on
# ---------------------------------------------------------------------------
def table(c, cam, t):
    near_z = -HALF_W
    for x in np.arange(0.4, FLAT_END, 1.8):
        for z in (-HALF_W + 0.1, HALF_W - 0.1):
            poly3(c, cam, [(x - 0.05, 0, z), (x + 0.05, 0, z), (x + 0.05, TABLE_Y, z), (x - 0.05, TABLE_Y, z)],
                  fill=WOOD, line=INK, lw=2)
    # the deck's posts, the tall chair and ladder beneath it
    for x in (LIP_X + 0.1, DECK_END - 0.08):
        for z in (-HALF_W + 0.08, HALF_W - 0.08):
            poly3(c, cam, [(x - 0.06, 0, z), (x + 0.06, 0, z), (x + 0.06, LIP_Y, z), (x - 0.06, LIP_Y, z)],
                  fill=WOOD, line=INK, lw=2)
    tall_chair(c, cam, HUSB_SEAT)
    # the half-pipe's panelled side under the curve
    angs = np.linspace(0, math.pi / 2, 24)
    curve = [ramp_point(a) for a in angs]
    for zside in (HALF_W, near_z):
        side = [(FLAT_END - 0.4, 0, zside)] + [(x, y, zside) for x, y in curve] + [(LIP_X, 0, zside)]
        poly3(c, cam, side, fill=WOOD, line=INK, lw=3, jit=0.5)
        for xk in np.arange(FLAT_END + 0.4, LIP_X, 0.7):
            ytop = TABLE_Y + RAMP_R - math.sqrt(max(0.0, RAMP_R ** 2 - (xk - FLAT_END) ** 2))
            line3(c, cam, [(xk, 0.05, zside), (xk, ytop - 0.05, zside)], WOOD_L, lw=2, opacity=0.7)
        line3(c, cam, [(x, y - 0.04, zside) for x, y in curve], PLY, lw=6)
    # tablecloth: flat part, then curling up the ramp
    poly3(c, cam, [(0.25, TABLE_Y, -HALF_W), (FLAT_END, TABLE_Y, -HALF_W), (FLAT_END, TABLE_Y, HALF_W),
                   (0.25, TABLE_Y, HALF_W)], fill=CLOTH, line=INK, lw=3, jit=0.5)
    for i in range(len(angs) - 1):
        (x0, y0), (x1, y1) = curve[i], curve[i + 1]
        shade = CLOTH * (1 - 0.18 * i / len(angs)) + CLOTH_S * (0.18 * i / len(angs))
        poly3(c, cam, [(x0, y0, -HALF_W), (x1, y1, -HALF_W), (x1, y1, HALF_W), (x0, y0, HALF_W)], fill=shade, jit=0.3)
    line3(c, cam, [(x, y, -HALF_W) for x, y in curve], INK, lw=3)
    line3(c, cam, [(x, y, HALF_W) for x, y in curve], INK, lw=3)
    # tablecloth hanging off the wife's end, and along the near side
    end = [(0.25, TABLE_Y, -HALF_W), (0.25, TABLE_Y, HALF_W)] + \
          [(0.26, TABLE_Y - 0.3 - 0.03 * math.sin(z * 9), z) for z in np.linspace(HALF_W, -HALF_W, 16)]
    poly3(c, cam, end, fill=CLOTH_S, line=INK, lw=2, jit=0.5)
    drape = [(x, TABLE_Y, near_z) for x in np.linspace(0.25, FLAT_END, 12)]
    hem = [(x, TABLE_Y - 0.28 - 0.03 * math.sin(x * 3), near_z - 0.01) for x in np.linspace(FLAT_END, 0.25, 30)]
    poly3(c, cam, drape + hem, fill=CLOTH_S, line=INK, lw=2, jit=0.5)
    for x in np.arange(0.6, FLAT_END, 0.6):
        line3(c, cam, [(x, TABLE_Y, near_z - 0.01), (x + 0.05, TABLE_Y - 0.26, near_z - 0.01)], col(0.6, 0.6, 0.57),
              lw=2, opacity=0.6)
    # the deck: a thick slab on top of the half-pipe, with a hole for him and a shelf for the salt
    for zside in (near_z, HALF_W):
        poly3(c, cam, [(LIP_X, LIP_Y, zside), (DECK_END, LIP_Y, zside), (DECK_END, LIP_Y - 0.12, zside),
                       (LIP_X, LIP_Y - 0.12, zside)], fill=WOOD, line=INK, lw=2)
    poly3(c, cam, [(DECK_END, LIP_Y, -HALF_W), (DECK_END, LIP_Y, HALF_W), (DECK_END, LIP_Y - 0.12, HALF_W),
                   (DECK_END, LIP_Y - 0.12, -HALF_W)], fill=WOOD, line=INK, lw=2)
    poly3(c, cam, [(LIP_X, LIP_Y, -HALF_W), (DECK_END, LIP_Y, -HALF_W), (DECK_END, LIP_Y, HALF_W),
                   (LIP_X, LIP_Y, HALF_W)], fill=CLOTH, line=INK, lw=3)
    x0, x1, z0, z1 = SHELF
    poly3(c, cam, [(x0, LIP_Y, z0), (x1, LIP_Y, z0), (x1, LIP_Y, z1), (x0, LIP_Y, z1)], fill=CLOTH, line=INK, lw=3)
    poly3(c, cam, [(x0, LIP_Y, z1), (x1, LIP_Y, z1), (x1, LIP_Y - 0.12, z1), (x0, LIP_Y - 0.12, z1)], fill=WOOD,
          line=INK, lw=2)
    hx, hrx, hrz = HOLE
    poly3(c, cam, circle3((hx, LIP_Y + 0.002, 0.0), hrx, 30, rz=hrz), fill=col(0.1, 0.09, 0.09), line=INK, lw=3)
    line3(c, cam, [(LIP_X, LIP_Y + 0.01, -HALF_W), (LIP_X, LIP_Y + 0.01, HALF_W)], SILVER, lw=5)
    # candlesticks down the table (they get knocked flying)
    for i, (x, z) in enumerate(TABLE_CANDLES):
        table_candle(c, cam, i, x, z, t)


def deck_front(c, cam):
    """The part of the deck in front of the hole, drawn over his lower half so he sits *in* it."""
    hx, hrx, hrz = HOLE
    arc = [(hx + hrx * math.cos(q), LIP_Y + 0.003, hrz * math.sin(q)) for q in np.linspace(1.5 * math.pi, 0.5 * math.pi, 16)]
    pts = [(LIP_X, LIP_Y + 0.003, -HALF_W), (hx, LIP_Y + 0.003, -HALF_W)] + arc + \
          [(hx, LIP_Y + 0.003, HALF_W), (LIP_X, LIP_Y + 0.003, HALF_W)]
    poly3(c, cam, pts, fill=CLOTH, jit=0.3)
    line3(c, cam, arc, INK, lw=3)
    line3(c, cam, [(LIP_X, LIP_Y + 0.01, -HALF_W), (LIP_X, LIP_Y + 0.01, HALF_W)], SILVER, lw=5)
    line3(c, cam, [(LIP_X, LIP_Y + 0.004, -HALF_W), (hx, LIP_Y + 0.004, -HALF_W)], INK, lw=3)


def candle(c, cam, base, t, seed, h=0.22, angle=0.0, lit=True):
    x, y, z = base
    if cam.depth(base) < 0.2:
        return
    sc = cam.scale(base)
    bx, by = cam.pt(base)
    w = max(2.0, 0.018 * sc)
    ca, sa = math.cos(angle), math.sin(angle)

    def R(u, v):
        return bx + u * ca - v * sa, by + u * sa + v * ca
    if angle == 0.0:
        poly3(c, cam, circle3((x, y + 0.005, z), 0.05, 14), fill=SILVER, line=INK, lw=2)
    c.poly([R(-w, 0), R(w, 0), R(w * 0.8, -0.1 * sc), R(-w * 0.8, -0.1 * sc)], fill=SILVER, line=INK, lw=2, jit=0.3)
    c.poly([R(-w * 0.7, -0.1 * sc), R(w * 0.7, -0.1 * sc), R(w * 0.7, -h * sc), R(-w * 0.7, -h * sc)],
           fill=col(0.93, 0.91, 0.85), line=INK, lw=2, jit=0.3)
    if lit:
        tx, ty = R(0, -(h + 0.03) * sc)
        s = sc * 0.03
        flick = 1 + 0.18 * math.sin(t * 13 + seed * 1.7)
        c.glow(tx, ty, s * 6, GLOW, 0.35)
        pts = [(tx + s * 0.6 * math.sin(q), ty - s * flick * (1.6 - 1.6 * math.cos(q)) * 0.6 + s * 0.3)
               for q in np.linspace(0, 2 * math.pi, 14)]
        c.poly(pts, fill=FLAME, jit=0.3)


def _candle_hits():
    """When each table candle gets hit by the salt, and which way it flies."""
    hits = []
    r = np.random.default_rng(21)
    for (cx, cz) in TABLE_CANDLES:
        th = None
        for k in range(2000):
            tt_ = T_SLAP + k * 0.002
            p, _ = boulder_path(tt_)
            if p[1] < TABLE_Y + BOULDER_R + 0.01 and p[0] <= cx + BOULDER_R:
                th = tt_
                break
        side = 1 if r.random() < 0.5 else -1
        hits.append(dict(t=th, v=(-4.0 - 3 * r.random(), 2.5 + 2.5 * r.random(), side * (2 + 3 * r.random())),
                         spin=side * r.uniform(9, 16)))
    return hits


def table_candle(c, cam, i, x, z, t):
    hit = CANDLE_HITS[i]
    if hit['t'] is None or t < hit['t']:
        candle(c, cam, (x, TABLE_Y, z), t, 20 + i)
        return
    u = t - hit['t']
    vx, vy, vz = hit['v']
    y = TABLE_Y + vy * u - 4.9 * u * u
    if y < 0:
        u_land = (vy + math.sqrt(vy * vy + 4 * 4.9 * TABLE_Y)) / 9.8
        candle(c, cam, (x + vx * u_land, 0.0, z + vz * u_land), t, 20 + i, angle=math.pi / 2, lit=False)
        return
    candle(c, cam, (x + vx * u, y, z + vz * u), t, 20 + i, angle=hit['spin'] * u, lit=True)


def glass_at(c, cam, base, wine=1.0):
    if cam.depth(base) < 0.2:
        return
    sx, sy = cam.pt(base)
    sc = cam.scale(base)
    stem = 0.09 * sc
    bw, bh = 0.045 * sc, 0.08 * sc
    c.poly(ell(sx, sy, bw * 0.9, bw * 0.25, 0, 14), fill=GLASS, line=INK, lw=2, opacity=0.9)
    c.line([(sx, sy), (sx, sy - stem)], INK, lw=max(2, 0.006 * sc))
    bowl = [(sx - bw, sy - stem - bh), (sx + bw, sy - stem - bh)] + \
           [(sx + bw * math.cos(q), sy - stem - bh + bh * math.sin(q)) for q in np.linspace(0, math.pi, 12)]
    if wine > 0:
        lvl = sy - stem - bh * (0.45 + 0.1 * wine)
        wn = [(sx - bw * 0.97, lvl), (sx + bw * 0.97, lvl)] + \
             [(sx + bw * 0.97 * math.cos(q), sy - stem - bh + bh * 0.97 * math.sin(q)) for q in np.linspace(0, math.pi, 12)]
        c.poly(wn, fill=WINE, jit=0.2)
    c.poly(bowl, None, INK, lw=2, jit=0.3)
    c.line([(sx - bw * 0.6, sy - stem - bh * 0.9), (sx - bw * 0.5, sy - stem - bh * 0.3)], WHITE, lw=max(2, 0.006 * sc),
           opacity=0.8)


def mound(c, cam, p, r, h, colr, dark):
    """A small rounded lump of food sitting on the plate, with shadow and highlight."""
    base, zc = cam.proj(circle3(p, r, 16))
    if (zc < 0.2).any():
        return
    cx, cy = base[:, 0].mean(), base[:, 1].mean()
    rx = (base[:, 0].max() - base[:, 0].min()) / 2
    ry = (base[:, 1].max() - base[:, 1].min()) / 2
    hs = h * cam.scale(p)
    c.poly(ell(cx + rx * 0.1, cy + ry * 0.2, rx * 1.05, ry, 0, 18), fill=dark, jit=0.2)
    c.poly(ell(cx, cy - hs * 0.45, rx, ry + hs * 0.5, 0, 20), fill=colr, line=INK, lw=max(1.5, rx * 0.08), jit=0.2)
    c.poly(ell(cx - rx * 0.35, cy - hs * 0.75, rx * 0.3, (ry + hs * 0.5) * 0.25, -20, 10),
           fill=WHITE * 0.35 + colr * 0.65, jit=0.1)


def place_setting(c, cam, center, facing, t, seed, wine=1.0):
    """A roast dinner, a glass of red, a candle and a napkin. facing = +1 if the diner sits at lower x."""
    x, y, z = center
    poly3(c, cam, circle3((x, y + 0.004, z), 0.17, 30), fill=PLATE, line=INK, lw=2)
    poly3(c, cam, circle3((x, y + 0.006, z), 0.125, 30), None, col(0.8, 0.8, 0.8), lw=2, opacity=0.8)
    poly3(c, cam, circle3((x + 0.04 * facing, y + 0.007, z - 0.06), 0.045, 14), fill=GRAVY, jit=0.2)
    for dx, dz, a in ((0.06, 0.03, 0.3), (0.08, -0.01, -0.2), (0.05, 0.07, 0.8)):
        px, pz = x + dx * facing, z + dz
        e1 = (px - 0.035 * math.cos(a), y + 0.015, pz - 0.035 * math.sin(a))
        e2 = (px + 0.035 * math.cos(a), y + 0.015, pz + 0.035 * math.sin(a))
        s1, zz = cam.proj([e1, e2])
        if (zz > 0.2).all():
            w = 0.011 * cam.scale(e1)
            c.poly(capsule(tuple(s1[0]), tuple(s1[1]), w, w * 0.8), fill=CARROT, line=INK, lw=1.5, jit=0.1)
            c.line([tuple(s1[0] - [0, w * 0.4]), tuple(s1[1] - [0, w * 0.4])], col(1, 0.75, 0.5), lw=max(1, w * 0.4))
    for dx, dz, r in ((-0.05, 0.05, 0.034), (0.0, 0.075, 0.03), (-0.08, 0.0, 0.028)):
        mound(c, cam, (x + dx * facing, y + 0.006, z + dz), r, 0.035, POTATO, col(0.7, 0.55, 0.3))
    mound(c, cam, (x + 0.02 * facing, y + 0.006, z - 0.03), 0.05, 0.045, CHICKEN, col(0.55, 0.35, 0.2))
    b0, b1 = (x + 0.05 * facing, y + 0.03, z - 0.06), (x + 0.1 * facing, y + 0.035, z - 0.09)
    s1, zz = cam.proj([b0, b1])
    if (zz > 0.2).all():
        w = 0.008 * cam.scale(b0)
        c.line([tuple(s1[0]), tuple(s1[1])], col(0.95, 0.93, 0.86), lw=max(2, w * 1.6))
        c.poly(ell(s1[1][0], s1[1][1], w * 1.4, w * 1.1, 0, 10), fill=col(0.95, 0.93, 0.86), line=INK, lw=1.5)
    rr = np.random.default_rng(seed)
    for k in range(10):
        pp = (x + rr.uniform(-0.1, -0.03) * facing, y + 0.012, z + rr.uniform(-0.09, 0.0))
        if cam.depth(pp) > 0.2:
            sx, sy = cam.pt(pp)
            pr = max(1.5, 0.011 * cam.scale(pp))
            c.poly(ell(sx, sy, pr, pr, 0, 10), fill=PEA, line=INK, lw=1, jit=0.05)
            c.poly(ell(sx - pr * 0.35, sy - pr * 0.35, pr * 0.3, pr * 0.3, 0, 6), fill=col(0.7, 0.9, 0.6), jit=0.02)
    nz = z + 0.26
    poly3(c, cam, [(x - 0.08, y + 0.004, nz - 0.06), (x + 0.08, y + 0.004, nz - 0.06), (x + 0.08, y + 0.004, nz + 0.06),
                   (x - 0.08, y + 0.004, nz + 0.06)], fill=col(0.93, 0.92, 0.89), line=INK, lw=2)
    glass_at(c, cam, (x + 0.18 * facing, y, z - 0.22), wine)
    candle(c, cam, (x + 0.3 * facing, y, z + 0.18), t, seed + 5, h=0.14)


# ---------------------------------------------------------------------------
# Characters (drawn flat, in screen space, at the size the camera sees them)
# ---------------------------------------------------------------------------
def closed_eye(c, x, y, w, lw, lashes=True, flip=1):
    """A contented closed eye: a gentle arch, with a few lashes."""
    pts = [(x + w * math.cos(q), y - w * 0.5 * math.sin(q)) for q in np.linspace(0.1, math.pi - 0.1, 12)]
    c.line(pts, INK, lw=lw, jit=0.2)
    if lashes:
        for q in (0.35, 0.75, 1.15):
            px, py = x + w * math.cos(q) * flip, y - w * 0.5 * math.sin(q)
            c.line([(px, py), (px + w * 0.28 * flip, py + w * 0.12)], INK, lw=lw * 0.7, jit=0.1)


class Figure:
    """Draw a character in its own units (metres), mirrored or tilted if needed."""
    def __init__(self, c, x, y, s, flip=1, lean=0.0, pivot=(0.0, 0.0), vs=1.0):
        self.c, self.x, self.y, self.s, self.flip, self.vs = c, x, y, s, flip, vs
        self.ca, self.sa = math.cos(math.radians(lean)), math.sin(math.radians(lean))
        self.pv = pivot
        self.lw = max(1.2, s * 0.011)

    def P(self, u, v):
        u, v = u - self.pv[0], v - self.pv[1]
        u, v = u * self.ca - v * self.sa, u * self.sa + v * self.ca
        u, v = u + self.pv[0], v + self.pv[1]
        return self.x + u * self.flip * self.s, self.y - v * self.s * self.vs

    def pts(self, lst):
        return [self.P(u, v) for u, v in lst]

    def ell(self, u, v, rx, ry, rot=0.0, n=28):
        r = math.radians(rot)
        return [self.P(u + rx * math.cos(q) * math.cos(r) - ry * math.sin(q) * math.sin(r),
                       v + rx * math.cos(q) * math.sin(r) + ry * math.sin(q) * math.cos(r))
                for q in np.linspace(0, 2 * math.pi, n, endpoint=False)]

    def smooth(self, lst, **kw):
        self.c.poly(smooth_closed(self.pts(lst)), **kw)

    def limb(self, a, b, ra, rb, **kw):
        self.c.poly(capsule(self.P(*a), self.P(*b), ra * self.s, rb * self.s), **kw)


def gloved_hand(f, hx, hy, ang, lw):
    """A gloved hand around a piece of cutlery: palm, curled fingers, thumb on top."""
    c = f.c
    ca, sa = math.cos(ang), math.sin(ang)
    c.poly(f.ell(hx, hy, 0.042, 0.032, math.degrees(ang)), fill=GLOVE, line=INK, lw=lw * 0.8)
    for k in range(3):
        u = -0.012 + 0.014 * k
        c.poly(f.ell(hx + u * ca - 0.028 * sa, hy + u * sa + 0.028 * ca, 0.013, 0.012), fill=GLOVE, line=INK,
               lw=lw * 0.6)
    c.poly(f.ell(hx + 0.025 * ca, hy + 0.025 * sa, 0.018, 0.011, math.degrees(ang) + 30), fill=GLOVE_S, line=INK,
           lw=lw * 0.6)


def lady_arm(f, sh, el, wr, lw, glove_from=0.5):
    """A bare upper arm and a long opera glove from just above the elbow to the wrist."""
    c = f.c
    (sx, sy), (ex, ey), (wx, wy) = sh, el, wr
    f.limb(sh, el, 0.043, 0.037, fill=SKIN, line=INK, lw=lw * 0.8)
    gx, gy = sx + (ex - sx) * glove_from, sy + (ey - sy) * glove_from
    f.limb((gx, gy), el, 0.041, 0.038, fill=GLOVE, line=INK, lw=lw * 0.8)
    f.limb(el, wr, 0.038, 0.027, fill=GLOVE, line=INK, lw=lw * 0.8)
    f.limb((gx, gy), el, 0.036, 0.034, fill=GLOVE)  # hide the seam at the elbow
    f.limb(el, ((ex + wx) / 2, (ey + wy) / 2), 0.034, 0.03, fill=GLOVE)
    # the glove's top edge, and soft wrinkles at the wrist
    ang = math.atan2(ey - sy, ex - sx)
    nx, ny = -math.sin(ang), math.cos(ang)
    c.line(f.pts([(gx + nx * 0.041, gy + ny * 0.041), (gx + 0.006 * math.cos(ang), gy + 0.006 * math.sin(ang)),
                  (gx - nx * 0.041, gy - ny * 0.041)]), INK, lw=lw * 0.7)
    a2 = math.atan2(wy - ey, wx - ex)
    for k in (0.72, 0.84):
        px, py = ex + (wx - ex) * k, ey + (wy - ey) * k
        nx2, ny2 = -math.sin(a2), math.cos(a2)
        c.line(f.pts([(px + nx2 * 0.022, py + ny2 * 0.022), (px + 0.01 * math.cos(a2), py + 0.01 * math.sin(a2)),
                      (px - nx2 * 0.018, py - ny2 * 0.018)]), GLOVE_S, lw=lw * 0.6)


CHAIR_X = WIFE_SEAT[0]


def chair_local():
    """Her dining chair in its own coordinates (metres): x forward (towards the table), y up, z across."""
    seat_y, hw = 0.46, 0.23
    parts = {'front': [], 'back': []}
    # front legs and the seat
    for z in (-0.19, 0.19):
        parts['front'].append(('leg', [(0.19, 0.0, z), (0.19, seat_y - 0.03, z)]))
    parts['front'].append(('poly', [(-0.22, seat_y - 0.05, -hw), (0.23, seat_y - 0.05, -hw), (0.23, seat_y, -hw),
                                    (-0.22, seat_y, -hw)], WOOD))
    parts['front'].append(('poly', [(0.23, seat_y - 0.05, -hw), (0.23, seat_y - 0.05, hw), (0.23, seat_y, hw),
                                    (0.23, seat_y, -hw)], WOOD))
    parts['front'].append(('poly', [(-0.22, seat_y, -hw), (0.23, seat_y, -hw), (0.23, seat_y, hw), (-0.22, seat_y, hw)],
                           col(0.38, 0.31, 0.36)))
    # back legs, back posts, the upholstered back and a carved top rail
    for z in (-0.19, 0.19):
        parts['back'].append(('leg', [(-0.2, 0.0, z), (-0.2, seat_y - 0.03, z)]))
    parts['back'].append(('poly', [(-0.21, 0.6, -0.17), (-0.21, 0.6, 0.17), (-0.23, 1.0, 0.17), (-0.23, 1.0, -0.17)],
                          col(0.38, 0.31, 0.36)))
    for z in (-0.2, 0.2):
        parts['back'].append(('leg', [(-0.2, seat_y - 0.03, z), (-0.24, 1.12, z)]))
    rail = [(-0.235, 1.0, -0.21), (-0.235, 1.0, 0.21), (-0.245, 1.1, 0.21)] + \
           [(-0.245, 1.1 + 0.07 * math.sin(math.pi * k / 8), 0.21 - 0.42 * k / 8) for k in range(9)]
    parts['back'].append(('poly', rail, WOOD))
    parts['back'].append(('poly', [(-0.205, seat_y + 0.02, -0.2), (-0.205, seat_y + 0.02, 0.2), (-0.21, 0.6, 0.2),
                                   (-0.21, 0.6, -0.2)], WOOD))
    return parts


CHAIR = chair_local()


def chair_xf(t):
    """Where her chair (and she) are: sitting still, or bowled over backwards by the salt."""
    def still(p):
        return (CHAIR_X + p[0], p[1], p[2])
    if t < T_HIT:
        return still, 0.0
    u = t - T_HIT
    phi = u * 7.5                       # tipping over backwards, legs in the air
    px = -0.2                           # pivot on the back legs
    vx, vy, vz = -3.2, 3.6, -0.6

    def moved(p):
        x, y, z = p
        xr = px + (x - px) * math.cos(phi) - y * math.sin(phi)
        yr = (x - px) * math.sin(phi) + y * math.cos(phi)
        return (CHAIR_X + xr + vx * u, yr + vy * u - 4.9 * u * u + 0.3 * u, z + vz * u)
    return moved, phi


def chair3d(c, cam, xf, part):
    for item in CHAIR[part]:
        pts = [xf(p) for p in item[1]]
        if item[0] == 'leg':
            mid = np.mean(pts, axis=0)
            if cam.depth(mid) > 0.2:
                line3(c, cam, pts, INK, lw=max(3, cam.scale(mid) * 0.05))
                line3(c, cam, pts, WOOD, lw=max(2, cam.scale(mid) * 0.035))
        else:
            poly3(c, cam, pts, fill=item[2], line=INK, lw=3)


def wife(c, x, y, s, t, mouth=0.0, arm=0.0, chew=0.0, swallow=0.0, view='front', lean=0.0, flip=-1, chair=False,
         vs=1.0):
    """The wife, seated. 'front' is a three-quarter view (drawn facing left; flip=-1 faces right).
    'back' shows her from behind, sitting in her chair."""
    f = Figure(c, x, y, s, flip, lean, (0.0, 0.5))
    lw = f.lw

    def chair_back():
        c.poly(f.pts([(-0.2, 0.0), (0.2, 0.0), (0.2, 0.62), (-0.2, 0.62)]), fill=WOOD, line=INK, lw=lw)
        c.poly(f.pts([(-0.15, 0.06), (0.15, 0.06), (0.15, 0.56), (-0.15, 0.56)]), fill=col(0.38, 0.31, 0.36),
               line=INK, lw=lw * 0.6)
        f.smooth([(-0.2, 0.6), (0.0, 0.7), (0.2, 0.6), (0.0, 0.64)], fill=WOOD, line=INK, lw=lw * 0.8)
        for sgn in (-1, 1):
            c.poly(f.ell(sgn * 0.2, 0.66, 0.03, 0.035, 0, 12), fill=WOOD_L, line=INK, lw=lw * 0.7)

    if view == 'back':
        # seen from behind and to her right, turned up the table towards him (her face just peeks out, left)
        f2 = Figure(c, x, y, s, 1, lean, (0.0, 0.5), vs)
        # her skirt spills over both sides of the seat
        f2.smooth([(-0.31, -0.04), (-0.3, 0.12), (-0.18, 0.2), (0.2, 0.2), (0.33, 0.12), (0.34, -0.04), (0.0, -0.08)],
                  fill=GOWN, line=INK, lw=lw)
        c.line(f2.pts([(-0.24, 0.0), (-0.22, 0.14)]), INK, lw=lw * 0.5, opacity=0.5)
        c.line(f2.pts([(0.27, 0.0), (0.25, 0.14)]), INK, lw=lw * 0.5, opacity=0.5)
        lady_arm(f2, (0.24, 0.46), (0.3, 0.27), (0.14, 0.22), lw)  # her near arm, reaching forward to the table
        f2.smooth([(-0.18, 0.12), (-0.21, 0.36), (-0.16, 0.5), (0.0, 0.55), (0.2, 0.53), (0.27, 0.4), (0.25, 0.12)],
                  fill=GOWN, line=INK, lw=lw)
        c.line(f2.pts([(0.03, 0.14), (0.05, 0.52)]), INK, lw=lw * 0.5, opacity=0.6)  # back seam of the bodice
        for i in range(4):  # lacing
            c.line(f2.pts([(0.02, 0.2 + 0.07 * i), (0.07, 0.23 + 0.07 * i)]), INK, lw=lw * 0.4, opacity=0.6)
        f2.limb((0.24, 0.46), (0.3, 0.27), 0.043, 0.037, fill=SKIN, line=INK, lw=lw * 0.8)
        for (px, py) in ((-0.15, 0.48), (0.23, 0.47)):
            f2.smooth([(px - 0.055, py - 0.03), (px - 0.045, py + 0.025), (px, py + 0.04), (px + 0.05, py + 0.02),
                       (px + 0.055, py - 0.03), (px, py - 0.045)], fill=GOWN, line=INK, lw=lw * 0.8)
        # nape, pearls, and the back of that magnificent hair
        c.poly(f2.pts([(-0.04, 0.53), (0.07, 0.53), (0.06, 0.64), (-0.04, 0.64)]), fill=SKIN, line=INK, lw=lw * 0.7)
        for i in range(5):
            c.poly(f2.ell(-0.03 + 0.024 * i, 0.61, 0.012, 0.012, 0, 8), fill=PEARL, line=INK, lw=lw * 0.3)
        # her fork arm, raised mid-conversation on the far side
        lady_arm(f2, (-0.16, 0.47), (-0.27, 0.31), (-0.23, 0.5), lw)
        c.line(f2.pts([(-0.23, 0.49), (-0.21, 0.66)]), SILVER, lw=lw * 1.2)
        for d in (-0.012, 0.0, 0.012):
            c.line(f2.pts([(-0.21 + d, 0.65), (-0.205 + d, 0.7)]), SILVER, lw=lw * 0.6)
        gloved_hand(f2, -0.23, 0.5, math.radians(80), lw)
        # her face in lost profile, turned up the table towards him: cheek, nose, a closed eye
        c.poly(f2.pts([(-0.06, 0.95), (-0.13, 0.9), (-0.16, 0.84), (-0.21, 0.8), (-0.165, 0.775), (-0.16, 0.74),
                       (-0.14, 0.7), (-0.08, 0.67), (-0.04, 0.8)]), fill=SKIN, line=INK, lw=lw * 0.8)
        c.line(f2.pts([(-0.15, 0.87), (-0.12, 0.855), (-0.095, 0.865)]), INK, lw=lw * 0.8)
        c.poly(f2.ell(-0.1, 0.78, 0.03, 0.02), fill=ROUGE, opacity=0.6)
        c.poly(f2.ell(0.1, 0.78, 0.028, 0.04), fill=SKIN, line=INK, lw=lw * 0.7)  # her ear
        c.poly(f2.ell(0.105, 0.72, 0.014, 0.02), fill=PEARL, line=INK, lw=lw * 0.4)
        f2.smooth([(-0.05, 0.72), (-0.08, 0.88), (-0.03, 0.97), (0.08, 0.96), (0.14, 0.84), (0.1, 0.7), (0.03, 0.66),
                   (-0.03, 0.67)], fill=HAIR_W, line=INK, lw=lw)
        for i in range(5):
            c.line(f2.pts([(-0.08 + 0.04 * i, 0.69), (-0.07 + 0.035 * i, 0.9)]), INK, lw=lw * 0.5, opacity=0.5)
        c.poly(f2.ell(-0.01, 1.0, 0.11, 0.085), fill=HAIR_W, line=INK, lw=lw)
        c.poly(f2.ell(0.0, 1.11, 0.065, 0.055), fill=HAIR_W, line=INK, lw=lw)
        for q in range(3):
            c.poly(f2.ell(-0.06 + 0.055 * q, 0.95, 0.028, 0.024), None, INK, lw=lw * 0.5)
        f2.smooth([(0.04, 1.13), (0.1, 1.21), (0.16, 1.33), (0.11, 1.27), (0.06, 1.19)], fill=col(0.66, 0.64, 0.62),
                  line=INK, lw=lw * 0.6)
        return

    if chair:
        chair_back()
    # skirt spilling over the seat
    f.smooth([(-0.34, -0.02), (-0.2, 0.12), (0.2, 0.12), (0.3, -0.02), (0.36, -0.46), (-0.4, -0.46)], fill=GOWN,
             line=INK, lw=lw)
    # a portly bodice: bosom to the front (left), straight back
    f.smooth([(-0.19, 0.08), (-0.26, 0.28), (-0.22, 0.44), (-0.12, 0.53), (0.12, 0.54), (0.2, 0.45), (0.2, 0.25),
              (0.17, 0.08)], fill=GOWN, line=INK, lw=lw)
    f.smooth([(-0.19, 0.44), (-0.11, 0.51), (0.11, 0.52), (0.18, 0.44), (0.09, 0.41), (-0.11, 0.41)], fill=GOWN_L)
    c.line(f.pts([(-0.24, 0.3), (-0.1, 0.27), (0.18, 0.3)]), INK, lw=lw * 0.6, opacity=0.5)
    # the far arm: held up at her side, knife aloft, as a lady should
    lady_arm(f, (0.16, 0.46), (0.26, 0.255), (0.31, 0.46), lw)
    c.line(f.pts([(0.31, 0.44), (0.32, 0.62)]), SILVER, lw=lw * 1.3)
    c.poly(f.pts([(0.313, 0.6), (0.33, 0.6), (0.322, 0.68)]), fill=SILVER, line=INK, lw=lw * 0.4)
    gloved_hand(f, 0.31, 0.46, math.radians(80), lw)
    # neck and pearls
    c.poly(f.pts([(-0.06, 0.5), (0.06, 0.5), (0.055, 0.66), (-0.065, 0.66)]), fill=SKIN, line=INK, lw=lw * 0.8)
    for i in range(9):
        a = math.pi * (0.12 + 0.76 * i / 8)
        c.poly(f.ell(0.1 * math.cos(a) - 0.01, 0.56 - 0.05 * math.sin(a), 0.017, 0.017, 0, 10), fill=PEARL, line=INK,
               lw=lw * 0.4)
    # the near arm: a conductor's flourish with her fork. Short puffed sleeve, bare upper arm, long glove.
    sx_, sy_ = -0.15, 0.46
    a1 = math.radians(235 - 45 * arm + 12 * arm * math.sin(t * 3.1))
    ex_, ey_ = sx_ + 0.21 * math.cos(a1), sy_ + 0.21 * math.sin(a1)
    a2 = math.radians(150 - 70 * arm + 35 * arm * math.sin(t * 3.1 + 0.8))
    hx_, hy_ = ex_ + 0.19 * math.cos(a2), ey_ + 0.19 * math.sin(a2)
    lady_arm(f, (sx_, sy_), (ex_, ey_), (hx_, hy_), lw)
    fa = a2 + math.radians(35)
    fx, fy = hx_ + 0.15 * math.cos(fa), hy_ + 0.15 * math.sin(fa)
    c.line(f.pts([(hx_, hy_), (fx, fy)]), SILVER, lw=lw * 1.2)
    for d in (-0.012, 0.0, 0.012):
        c.line(f.pts([(fx, fy), (fx + 0.04 * math.cos(fa) - d * math.sin(fa), fy + 0.04 * math.sin(fa) + d * math.cos(fa))]),
               SILVER, lw=lw * 0.6)
    gloved_hand(f, hx_, hy_, a2, lw)
    for (px, py) in ((-0.15, 0.47), (0.16, 0.465)):
        f.smooth([(px - 0.058, py - 0.03), (px - 0.045, py + 0.025), (px + 0.0, py + 0.04), (px + 0.05, py + 0.02),
                  (px + 0.055, py - 0.03), (px + 0.0, py - 0.045)], fill=GOWN, line=INK, lw=lw * 0.8)
        c.line(f.pts([(px - 0.02, py + 0.03), (px - 0.01, py - 0.03)]), INK, lw=lw * 0.4, opacity=0.6)
        c.line(f.pts([(px + 0.02, py + 0.03), (px + 0.025, py - 0.03)]), INK, lw=lw * 0.4, opacity=0.6)
    # head: a proud egg, chin up
    hy = 0.8 - 0.012 * swallow
    f.smooth([(-0.12, 0.0 + hy), (-0.1, 0.1 + hy), (0.0, 0.16 + hy), (0.11, 0.1 + hy), (0.12, -0.02 + hy),
              (0.06, -0.13 + hy), (-0.05, -0.15 + hy)], fill=SKIN, line=INK, lw=lw)
    # grand updo with curls and a little plume
    f.smooth([(-0.13, 0.05 + hy), (-0.1, 0.2 + hy), (0.0, 0.27 + hy), (0.13, 0.22 + hy), (0.16, 0.05 + hy),
              (0.08, 0.1 + hy), (-0.05, 0.12 + hy)], fill=HAIR_W, line=INK, lw=lw)
    c.poly(f.ell(0.03, hy + 0.34, 0.1, 0.08), fill=HAIR_W, line=INK, lw=lw)
    for q in range(3):
        c.poly(f.ell(-0.05 + 0.08 * q, hy + 0.25 + 0.02 * (q % 2), 0.035, 0.03), None, INK, lw=lw * 0.5)
    f.smooth([(0.08, hy + 0.38), (0.14, hy + 0.44), (0.2, hy + 0.56), (0.15, hy + 0.5), (0.1, hy + 0.43)],
             fill=col(0.66, 0.64, 0.62), line=INK, lw=lw * 0.6)
    c.poly(f.ell(0.12, hy + 0.02, 0.045, 0.07), fill=HAIR_W, line=INK, lw=lw * 0.8)
    c.poly(f.ell(0.1, hy - 0.08, 0.015, 0.02), fill=PEARL, line=INK, lw=lw * 0.4)
    # a neater nose: only its outer edge is drawn
    nose = [(-0.1, hy + 0.045), (-0.165, hy - 0.022), (-0.15, hy - 0.042), (-0.105, hy - 0.04)]
    c.poly(f.pts(nose + [(-0.09, hy)]), fill=SKIN, jit=0.2)
    c.line(f.pts(nose), INK, lw=lw * 0.9, jit=0.2)
    for ex, ew in ((-0.07, 0.027), (0.025, 0.033)):
        closed_eye(c, *f.P(ex, hy + 0.05), ew * s, lw * 0.9, flip=-flip)
        c.line(f.pts([(ex - ew, hy + 0.1), (ex, hy + 0.125), (ex + ew, hy + 0.105)]), INK, lw=lw * 0.7)
    c.poly(f.ell(0.03, hy - 0.035, 0.035, 0.022), fill=ROUGE, pressure=0.9, opacity=0.6, jit=0.3)
    mh = 0.004 + 0.034 * mouth + 0.012 * chew
    if mh > 0.01:
        c.poly(f.ell(-0.07, hy - 0.09, 0.028, mh), fill=col(0.35, 0.12, 0.14), line=col(0.55, 0.3, 0.3), lw=lw * 0.8)
    else:
        c.line(f.pts([(-0.09, hy - 0.083), (-0.07, hy - 0.09), (-0.05, hy - 0.083)]), col(0.5, 0.25, 0.25), lw=lw)


def husband(c, x, y, s, t, mouth=0.0, flourish=0.0, eat=0.0, turn=0.0, arm_r=None, grin=0.0):
    """The husband, seated in his hole in the deck, facing the camera.
    arm_r = (upper, fore) angles in degrees for his left arm (screen right) when he reaches for the salt."""
    f = Figure(c, x, y, s)
    lw = f.lw
    c.poly(f.pts([(-0.27, 0.1), (0.27, 0.1), (0.27, 0.7), (-0.27, 0.7)]), fill=WOOD, line=INK, lw=lw)
    c.poly(f.pts([(-0.22, 0.14), (0.22, 0.14), (0.22, 0.64), (-0.22, 0.64)]), fill=col(0.42, 0.26, 0.28))
    for sgn in (-1, 1):
        c.poly(f.pts([(sgn * 0.27 - 0.025, 0.1), (sgn * 0.27 + 0.025, 0.1), (sgn * 0.27 + 0.025, 0.74),
                      (sgn * 0.27 - 0.025, 0.74)]), fill=WOOD, line=INK, lw=lw * 0.8)
        c.poly(f.ell(sgn * 0.27, 0.78, 0.035, 0.04, 0, 12), fill=WOOD_L, line=INK, lw=lw * 0.8)
    f.smooth([(-0.26, 0.0), (-0.31, 0.22), (-0.28, 0.46), (-0.18, 0.56), (0.18, 0.56), (0.28, 0.46), (0.31, 0.22),
              (0.26, 0.0)], fill=COAT, line=INK, lw=lw)
    f.smooth([(-0.15, 0.02), (-0.2, 0.22), (-0.12, 0.48), (0.12, 0.48), (0.2, 0.22), (0.15, 0.02)],
             fill=col(0.5, 0.5, 0.48), line=INK, lw=lw * 0.8)
    for v in (0.1, 0.19, 0.28):
        c.poly(f.ell(0.0, v, 0.013, 0.013, 0, 8), fill=SILVER, line=INK, lw=lw * 0.3)
    c.line(f.pts([(-0.1, 0.15), (-0.03, 0.12), (0.02, 0.16)]), SILVER, lw=lw * 0.7)
    c.poly(f.pts([(-0.07, 0.32), (0.07, 0.32), (0.09, 0.53), (-0.09, 0.53)]), fill=SHIRT, line=INK, lw=lw * 0.6)
    for sgn in (-1, 1):
        c.poly(f.pts([(sgn * 0.09, 0.53), (sgn * 0.17, 0.53), (sgn * 0.13, 0.25)]), fill=COAT_L, line=INK, lw=lw * 0.6)
    c.poly(f.pts([(-0.07, 0.51), (0.0, 0.535), (0.07, 0.51), (0.07, 0.575), (0.0, 0.55), (-0.07, 0.575)]), fill=INK)
    hx0, hy0 = 0.03 * turn, 0.8
    f.smooth([(hx0 - 0.13, hy0 + 0.02), (hx0 - 0.1, hy0 + 0.16), (hx0, hy0 + 0.21), (hx0 + 0.1, hy0 + 0.16),
              (hx0 + 0.13, hy0 + 0.02), (hx0 + 0.12, hy0 - 0.12), (hx0 + 0.05, hy0 - 0.2), (hx0 - 0.05, hy0 - 0.2),
              (hx0 - 0.12, hy0 - 0.12)], fill=SKIN, line=INK, lw=lw)
    c.poly(f.ell(hx0 - 0.05, hy0 + 0.15, 0.04, 0.02, 20), fill=WHITE, opacity=0.7)
    for sgn in (-1, 1):
        c.poly(f.ell(hx0 + sgn * 0.14, hy0 - 0.01, 0.025, 0.04), fill=SKIN_S, line=INK, lw=lw * 0.7)
        for (du, dv, r) in ((0.15, 0.08, 0.05), (0.18, 0.02, 0.055), (0.16, -0.05, 0.05), (0.2, 0.09, 0.04)):
            c.poly(f.ell(hx0 + sgn * du, hy0 + dv, r, r * 0.85, 0, 14), fill=HAIR_H, line=INK, lw=lw * 0.7)
    for sgn in (-1, 1):
        closed_eye(c, *f.P(hx0 + sgn * 0.05, hy0 + 0.05), 0.032 * s, lw * 0.9, lashes=False)
        c.poly(f.pts([(hx0 + sgn * 0.015, hy0 + 0.095), (hx0 + sgn * 0.09, hy0 + 0.125), (hx0 + sgn * 0.095, hy0 + 0.095)]),
               fill=HAIR_H, line=INK, lw=lw * 0.6)
    # a more modest nose
    c.poly(f.pts([(hx0 - 0.01, hy0 + 0.045), (hx0 + 0.02 + 0.02 * turn, hy0 - 0.035), (hx0, hy0 - 0.048),
                  (hx0 - 0.024, hy0 - 0.036)]), fill=SKIN_S, line=INK, lw=lw * 0.9)
    open_ = max(mouth, grin * 0.5)
    if open_ > 0.05:
        c.poly(f.ell(hx0, hy0 - 0.13, 0.065, 0.012 + 0.04 * open_), fill=col(0.3, 0.1, 0.1), line=INK, lw=lw * 0.8)
        c.poly(f.pts([(hx0 - 0.055, hy0 - 0.113), (hx0 + 0.055, hy0 - 0.113), (hx0 + 0.05, hy0 - 0.135),
                      (hx0 - 0.05, hy0 - 0.135)]), fill=WHITE, line=INK, lw=lw * 0.4)
        for k in range(-2, 3):
            c.line(f.pts([(hx0 + k * 0.02, hy0 - 0.113), (hx0 + k * 0.02, hy0 - 0.135)]), INK, lw=lw * 0.3)
    else:
        c.line(f.pts([(hx0 - 0.05, hy0 - 0.125), (hx0, hy0 - 0.135), (hx0 + 0.05, hy0 - 0.125)]), INK, lw=lw)
    for sgn in (-1, 1):
        pts = [(hx0, hy0 - 0.07)]
        for q in np.linspace(0, 1, 9):
            pts.append((hx0 + sgn * (0.02 + 0.17 * q), hy0 - 0.08 - 0.025 * math.sin(q * math.pi) + 0.08 * q ** 3))
        curl = [(hx0 + sgn * (0.19 + 0.03 * math.cos(q)), hy0 + 0.02 + 0.03 * math.sin(q))
                for q in np.linspace(-0.5 * math.pi, 1.4 * math.pi, 9)]
        c.line(f.pts(pts + curl), HAIR_H, lw=0.04 * s, jit=0.2)
        c.line(f.pts(pts + curl), INK, lw=lw * 0.5, jit=0.2, opacity=0.85)
    for sgn in (-1, 1):
        sxp, syp = sgn * 0.25, 0.47
        tool = True
        if sgn > 0 and arm_r is not None:
            a1, a2 = math.radians(arm_r[0]), math.radians(arm_r[1])
            ex_, ey_ = sxp + 0.24 * math.cos(a1), syp + 0.24 * math.sin(a1)
            hx_, hy_ = ex_ + 0.22 * math.cos(a2), ey_ + 0.22 * math.sin(a2)
            tool = False
        else:
            spread = flourish * (0.6 + 0.4 * math.sin(t * 4.0 + (0 if sgn > 0 else 1.2)))
            a1 = math.radians(-90 + sgn * (25 + 55 * spread))
            ex_, ey_ = sxp + 0.21 * math.cos(a1), syp + 0.21 * math.sin(a1)
            a2 = math.radians(90 - sgn * (60 - 50 * spread)) + 0.15 * math.sin(t * 7) * eat
            hx_, hy_ = ex_ + 0.19 * math.cos(a2), ey_ + 0.19 * math.sin(a2)
            if turn > 0.5:
                a1 = math.radians(-90 + sgn * 20)
                ex_, ey_ = sxp + 0.21 * math.cos(a1), syp + 0.21 * math.sin(a1)
                hx_, hy_ = ex_ - sgn * 0.12, ey_ + 0.02
                tool = False
        f.limb((sxp, syp), (ex_, ey_), 0.06, 0.05, fill=COAT, line=INK, lw=lw * 0.8)
        f.limb((ex_, ey_), (hx_, hy_), 0.05, 0.042, fill=COAT, line=INK, lw=lw * 0.8)
        c.poly(f.ell(hx_, hy_, 0.04, 0.03, 0, 12), fill=SHIRT, line=INK, lw=lw * 0.6)
        c.poly(f.ell(hx_ + 0.005 * sgn, hy_ + 0.035, 0.035, 0.035, 0, 12), fill=SKIN, line=INK, lw=lw * 0.8)
        if tool:
            c.line(f.pts([(hx_, hy_ + 0.03), (hx_, hy_ + 0.17)]), SILVER, lw=lw * 1.2)
            if sgn < 0:
                for d in (-0.012, 0.0, 0.012):
                    c.line(f.pts([(hx_ + d, hy_ + 0.17), (hx_ + d, hy_ + 0.21)]), SILVER, lw=lw * 0.6)
            else:
                c.poly(f.pts([(hx_ - 0.012, hy_ + 0.17), (hx_ + 0.014, hy_ + 0.17), (hx_, hy_ + 0.25)]), fill=SILVER,
                       line=INK, lw=lw * 0.4)


def tall_chair(c, cam, seat):
    """His absurd chair: spindly legs from the floor, and a ladder up to the deck."""
    x, y, z = seat
    for (lx, lz) in ((x - 0.22, z - 0.22), (x + 0.22, z - 0.22), (x - 0.22, z + 0.22), (x + 0.22, z + 0.22)):
        line3(c, cam, [(lx, 0, lz), (lx, y, lz)], WOOD, lw=max(3, cam.scale((lx, y / 2, lz)) * 0.04))
    for yy in np.arange(0.6, y, 0.9):
        line3(c, cam, [(x - 0.22, yy, z - 0.22), (x + 0.22, yy, z - 0.22)], WOOD, lw=3)
        line3(c, cam, [(x - 0.22, yy, z + 0.22), (x + 0.22, yy, z + 0.22)], WOOD, lw=3)
    lz = -HALF_W - 0.1
    for dx in (-0.15, 0.15):
        line3(c, cam, [(x + dx, 0, lz - 0.3), (x + dx, LIP_Y, lz)], WOOD_L, lw=4)
    for yy in np.arange(0.3, LIP_Y, 0.3):
        f = yy / LIP_Y
        line3(c, cam, [(x - 0.15, yy, lz - 0.3 * (1 - f)), (x + 0.15, yy, lz - 0.3 * (1 - f))], WOOD_L, lw=3)


# ---------------------------------------------------------------------------
# The salt
# ---------------------------------------------------------------------------
_rs = np.random.default_rng(8)
SALT_FACETS = [(_rs.uniform(0, 2 * np.pi), _rs.uniform(0.25, 0.8), _rs.uniform(0.14, 0.26)) for _ in range(8)]


def boulder_path(t):
    """Where the salt is at time t, and how far it has rolled."""
    x0, y0, z0 = BOULDER_START
    if t < T_SLAP:
        return (x0, y0, z0), 0.0
    u = t - T_SLAP
    deck = x0 - LIP_X
    arc = RAMP_R * math.pi / 2
    flat = FLAT_END - 0.1
    if u < ROLL_DECK:
        e = (u / ROLL_DECK) ** 2
        return (x0 - deck * e, y0, lerp(z0, 0.45, min(1.0, e * 1.6))), deck * e
    u -= ROLL_DECK
    if u < ROLL_CURVE:
        f = (u / ROLL_CURVE) ** 1.6
        a = math.pi / 2 * (1 - f)
        px, py = ramp_point(a)
        return (px - math.sin(a) * BOULDER_R, py + math.cos(a) * BOULDER_R, lerp(0.45, 0.2, f)), deck + arc * f
    u -= ROLL_CURVE
    if u <= ROLL_FLAT:
        f = u / ROLL_FLAT
        s = flat * (0.8 * f + 0.2 * f * f)
        return (FLAT_END - s, TABLE_Y + BOULDER_R, lerp(0.2, 0.0, f)), deck + arc + s
    # straight on through, like a bowling ball: no slowing down, falling once it leaves the table
    v = flat * 1.2 / ROLL_FLAT
    k = u - ROLL_FLAT
    x = 0.1 - v * k
    y = TABLE_Y + BOULDER_R - (4.9 * (k - 0.03) ** 2 if k > 0.03 else 0.0)
    return (x, y, -0.4 * k), deck + arc + flat + v * k


def visual_spin(t):
    """How far the salt appears to have turned. The true spin is too fast for 12 drawings a second
    (it would seem to turn backwards), so each drawing turns it by at most ~50 degrees."""
    if t <= T_SLAP:
        return 0.0
    ang, prev, k = 0.0, 0.0, T_SLAP
    while k < t:
        k2 = min(t, k + 1 / FPS)
        _, r2 = boulder_path(k2)
        ang += min((r2 - prev) / BOULDER_R, 0.85)
        prev, k = r2, k2
    return ang


def salt_boulder(c, cam, t):
    p, rolled = boulder_path(t)
    if cam.depth(p) < 0.3:
        return
    sx, sy = cam.pt(p)
    r = cam.scale(p) * BOULDER_R
    spin = visual_spin(t)
    if t > T_SLAP + ROLL_DECK * 0.6:
        pp, _ = boulder_path(t - 0.08)
        if cam.depth(pp) > 0.3:
            px, py = cam.pt(pp)
            dx, dy = sx - px, sy - py
            dl = math.hypot(dx, dy)
            if r * 0.3 < dl < r * 3 and r < 400:
                nx, ny = -dy / dl, dx / dl
                for k in (-0.7, -0.25, 0.25, 0.7):
                    c.line([(sx - dx / dl * r * 0.8 + nx * r * k, sy - dy / dl * r * 0.8 + ny * r * k),
                            (px - dx * 0.4 + nx * r * k, py - dy * 0.4 + ny * r * k)], col(0.9, 0.9, 0.92),
                           lw=max(2, r * 0.06), opacity=0.7)
    c.glow(sx, sy, r * 2.2, WHITE, 0.35)
    c.poly(blob(sx, sy, r, 44, 26, 0.12), fill=SALT, line=col(0.45, 0.5, 0.58), lw=max(2, r * 0.03))
    for a, rho, sz in SALT_FACETS:
        aa = a - spin
        fx, fy = sx + rho * r * math.cos(aa) * 0.8, sy + rho * r * math.sin(aa) * 0.8
        c.poly(blob(fx, fy, sz * r, int(a * 10), 6, 0.3), fill=SALT_S, opacity=0.7, jit=0.3)
    for k in range(3):
        aa = -spin + k * 2.1
        c.line([(sx + r * 0.85 * math.cos(aa), sy + r * 0.85 * math.sin(aa)),
                (sx + r * 0.2 * math.cos(aa + 0.4), sy + r * 0.2 * math.sin(aa + 0.4)),
                (sx - r * 0.7 * math.cos(aa - 0.3), sy - r * 0.7 * math.sin(aa - 0.3))], col(0.55, 0.6, 0.7),
               lw=max(1.5, r * 0.03), opacity=0.8)
    c.poly(ell(sx - r * 0.35, sy - r * 0.4, r * 0.2, r * 0.1, -30, 12), fill=WHITE)
    for q in (0.3, 1.9, 3.8):
        gx, gy = sx + r * 1.05 * math.cos(q), sy + r * 1.05 * math.sin(q)
        c.line([(gx - r * 0.12, gy), (gx + r * 0.12, gy)], WHITE, lw=2, opacity=0.9)
        c.line([(gx, gy - r * 0.12), (gx, gy + r * 0.12)], WHITE, lw=2, opacity=0.9)


CANDLE_HITS = _candle_hits()


# ---------------------------------------------------------------------------
# Speech: mouth movement follows the loudness of the recordings
# ---------------------------------------------------------------------------
def _load_voice(name):
    import subprocess
    import imageio_ffmpeg
    src = os.path.join(HERE, 'audio', name)
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-i', src, '-ac', '1', '-ar',
                          str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float64) / 32767
    n = SR // FPS
    env = np.array([np.sqrt((x[i:i + n] ** 2).mean()) for i in range(0, len(x) - n, n)])
    env = np.clip((env - env.max() * 0.08) / (env.max() * 0.6), 0, 1)
    return x, env


VOICE_W, MOUTH_W = _load_voice('darling.m4a')
VOICE_H, MOUTH_H = _load_voice('of-course.m4a')


def mouth_at(env, t0, t):
    i = int(round((t - t0) * FPS))
    return float(env[i]) if 0 <= i < len(env) else 0.0


def speaking(env, t0, t):
    i = int(round((t - t0) * FPS))
    if not 0 <= i < len(env):
        return 0.0
    return float(env[max(0, i - 6):i + 6].max())


# ---------------------------------------------------------------------------
# Shots
# ---------------------------------------------------------------------------
CAM_A = ((2.6, 1.35, 1.45), (0.02, 0.92, 0.02), 45)                                     # her one o'clock
CAM_B = ((HUSB_SEAT[0] - 2.7, LIP_Y + 0.75, 0.0), (HUSB_SEAT[0], LIP_Y + 0.45, 0.0), 42)  # his twelve
CAM_C = ((-3.05, 5.3, -1.6), (6.5, 0.2, 0.4), 74)                                       # the whole arrangement


def camera(t):
    if t < T_CUT_H:
        (p, g, f) = CAM_A
        k = 0.03 * t / T_CUT_H
        return Cam(tuple(np.array(p) + (np.array(g) - np.array(p)) * k), g, f)
    if t < T_WHIP:
        return Cam(*CAM_B)
    u = clamp01((t - T_WHIP) / (T_WHIP_END - T_WHIP))
    e = 1 - (1 - u) ** 3
    p = np.array(CAM_B[0]) * (1 - e) + np.array(CAM_C[0]) * e
    g = np.array(CAM_B[1]) * (1 - e) + np.array(CAM_C[1]) * e
    f = CAM_B[2] * (1 - e) + CAM_C[2] * e
    if t > T_HIT:
        sh = 0.12 * max(0.0, 1 - (t - T_HIT) / 0.5)
        p = p + np.random.default_rng(int(t * FPS)).normal(0, sh, 3)
    return Cam(tuple(p), tuple(g), f)


def his_arm(t):
    """Angles for his left arm as he pats, pats, winds up and slaps the salt (None = normal)."""
    if t < T_TURN + 0.3:
        return None
    reach = (-15.0, 5.0)
    if t < T_PAT1:
        k = sstep(T_TURN + 0.3, T_PAT1 - 0.1, t)
        return (lerp(-60, reach[0], k), lerp(60, reach[1], k))
    for tp in (T_PAT1, T_PAT2):
        if tp <= t < tp + 0.3:
            d = math.sin(math.pi * clamp01((t - tp) / 0.2))
            return (reach[0] - 8 * d, reach[1] - 35 * d)
    if t < T_WIND:
        return reach
    if t < T_SLAP:
        k = sstep(T_WIND, T_SLAP - 0.08, t)
        return (lerp(reach[0], 55, k), lerp(reach[1], 110, k))
    k = sstep(T_SLAP - 0.08, T_SLAP + 0.02, t)
    rec = sstep(T_SLAP + 0.4, T_SLAP + 1.0, t)
    return (lerp(lerp(55, -35, k), -20, rec), lerp(lerp(110, -40, k), 0, rec))


def draw_world(c, cam, t):
    room(c, cam, t)
    chandelier(c, cam, t)
    wife_behind_table = cam.pos[0] > WIFE_SEAT[0] + 0.5 and t < T_HIT and cam.depth(WIFE_SEAT) > 0.5
    if wife_behind_table:
        wife_figure(c, cam, t)
    table(c, cam, t)
    if wife_behind_table:
        place_setting(c, cam, (0.5, TABLE_Y, 0.0), 1, t, 3)
    if cam.depth(HUSB_SEAT) > 0.5:
        sx, sy = cam.pt(HUSB_SEAT)
        s = cam.scale(HUSB_SEAT)
        speak = mouth_at(MOUTH_H, T_SPEAK_H, t)
        flourish = speaking(MOUTH_H, T_SPEAK_H, t) * sstep(T_SPEAK_H + 0.8, T_SPEAK_H + 1.1, t)
        eat = 1.0 if T_CUT_H < t < T_SPEAK_H + 0.9 else 0.0
        turn = sstep(T_TURN, T_TURN + 0.5, t)
        grin = sstep(T_SLAP, T_SLAP + 0.2, t)
        husband(c, sx, sy, s, t, mouth=speak, flourish=flourish, eat=eat, turn=turn, arm_r=his_arm(t), grin=grin)
        deck_front(c, cam)
        place_setting(c, cam, HIS_PLATE, -1, t, 7)
    if t < T_HIT:
        salt_boulder(c, cam, t)
    if not wife_behind_table:
        if t < T_HIT:
            if cam.depth(WIFE_SEAT) > 0.5:
                place_setting(c, cam, (0.5, TABLE_Y, 0.0), 1, t, 3)
                wife_figure(c, cam, t)
        else:
            wife_flies(c, cam, t)


def vertical_squash(cam, p):
    """How much a metre of height shrinks on screen, seen from this camera (1 = seen straight on)."""
    a, b = cam.pt(p), cam.pt((p[0], p[1] + 0.5, p[2]))
    return min(1.0, math.hypot(b[0] - a[0], b[1] - a[1]) / (0.5 * cam.scale(p)))


def wife_figure(c, cam, t):
    xf, _ = chair_xf(t)
    seat = xf((-0.04, 0.46, 0.0))
    sx, sy = cam.pt(seat)
    s = cam.scale(seat)
    chew = max(0.0, math.sin(t * 9)) if t < 1.3 else 0.0
    swallow = math.sin(math.pi * clamp01((t - 2.1) / 0.4))
    kw = dict(mouth=mouth_at(MOUTH_W, T_SPEAK_W, t), arm=speaking(MOUTH_W, T_SPEAK_W, t), chew=chew, swallow=swallow)
    if cam.pos[0] > CHAIR_X:
        # seen from the front: the chair is behind her
        chair3d(c, cam, xf, 'back')
        chair3d(c, cam, xf, 'front')
        wife(c, sx, sy, s, t, view='front', **kw)
    else:
        # seen from behind: seat and front legs, then her, then the back legs and chair back nearest to us
        chair3d(c, cam, xf, 'front')
        wife(c, sx, sy, s, t, view='back', vs=vertical_squash(cam, seat), **kw)
        chair3d(c, cam, xf, 'back')


def wife_flies(c, cam, t):
    """The salt bowls straight through: she and her chair go over backwards together, dinner everywhere."""
    u = t - T_HIT
    xf, phi = chair_xf(t)
    seat, up = xf((0.0, 0.46, 0.0)), xf((0.0, 1.46, 0.0))
    if cam.depth(seat) > 0.3 and cam.depth(up) > 0.3:
        (sx, sy), (ux, uy) = cam.pt(seat), cam.pt(up)
        lean = math.degrees(math.atan2(ux - sx, -(uy - sy)))
        chair3d(c, cam, xf, 'front')
        wife(c, sx, sy, cam.scale(seat), t, view='back', lean=lean, mouth=0.8,
             vs=max(0.6, vertical_squash(cam, seat)))
        chair3d(c, cam, xf, 'back')
    # plate, glass and candle go with her
    for (vx, vy, vz, spin, kind) in [(-7, 4.5, 1.5, -300, 'plate'), (-6, 5.5, 2.5, 500, 'glass'),
                                     (-8, 3.5, -2.5, 200, 'candle')]:
        p = (0.4 + vx * u, TABLE_Y + 0.05 + vy * u - 4.9 * u * u, vz * u)
        if cam.depth(p) < 0.3:
            continue
        sx, sy = cam.pt(p)
        s = cam.scale(p)
        if kind == 'plate':
            c.poly(ell(sx, sy, 0.17 * s, 0.06 * s, spin * u, 20), fill=PLATE, line=INK, lw=3)
        elif kind == 'glass':
            c.poly(ell(sx, sy, 0.05 * s, 0.1 * s, spin * u, 12), fill=GLASS, line=INK, lw=2)
            c.poly(ell(sx + 0.08 * s, sy + 0.05 * s, 0.07 * s, 0.03 * s, spin * u * 0.3, 12), fill=WINE, jit=0.3)
        else:
            candle(c, cam, p, t, 3, angle=math.radians(spin * u))
    r = np.random.default_rng(12)
    for i in range(80):
        v = r.normal(0, 1, 3) * [2.5, 2.5, 2.5] + [-6, 3, 0]
        p = (0.4 + v[0] * u, TABLE_Y + 0.2 + v[1] * u - 4.9 * u * u, v[2] * u)
        if p[1] < 0 or cam.depth(p) < 0.3:
            continue
        sx, sy = cam.pt(p)
        colr = [PLATE, GLASS, PEA, CARROT, POTATO, WINE, SALT, SILVER][i % 8]
        c.poly(blob(sx, sy, max(3, 0.03 * cam.scale(p)), i, 6, 0.4), fill=colr, line=INK, lw=1.5)
    # and the salt carries straight on, undeterred
    salt_boulder(c, cam, t)


def render(d):
    t = d / FPS
    c = SharpCanvas(d)
    draw_world(c, camera(t), t)
    return c.result()


# ---------------------------------------------------------------------------
# Sound
# ---------------------------------------------------------------------------
def hall(x, wet=0.22, length=1.3, seed=5):
    """A touch of big-room echo."""
    n = int(length * SR)
    ir = np.random.default_rng(seed).normal(size=n) * np.exp(-np.arange(n) / (0.32 * SR))
    ir = np.convolve(ir, np.ones(8) / 8, mode='same')
    y = np.convolve(x, ir)
    out = np.zeros(len(y))
    out[:len(x)] += x
    return out + wet * y / (np.abs(y).max() + 1e-9) * np.abs(x).max()


def make_audio(path):
    tr = Track(DUR)
    add = tr.add
    rg = np.random.default_rng(2)
    add(0.0, 0.012 * noise(DUR, 150, 1500, 1))
    for tc in rg.uniform(0, DUR, 40):
        add(tc, 0.02 * noise(0.03, 1000, 5000, int(tc * 100)) * decay(0.03, 0.006))
    add(T_SPEAK_W, 0.85 * hall(VOICE_W / (np.abs(VOICE_W).max() + 1e-9)))
    add(T_SPEAK_H, 0.85 * hall(VOICE_H / (np.abs(VOICE_H).max() + 1e-9)))
    add(T_WHIP, 0.25 * noise(0.45, 400, 5000, 3) * np.hanning(int(0.45 * SR)))
    for tp in (T_PAT1, T_PAT2):
        add(tp + 0.1, 0.35 * noise(0.08, 200, 1800, int(tp * 10)) * decay(0.08, 0.02))
        add(tp + 0.1, 0.25 * np.sin(2 * np.pi * 260 * tt(0.08)) * decay(0.08, 0.025))
    add(T_SLAP, 0.9 * noise(0.12, 600, 7000, 4) * decay(0.12, 0.018))
    add(T_SLAP, 0.4 * np.sin(2 * np.pi * np.cumsum(np.linspace(320, 520, int(0.12 * SR))) / SR) * decay(0.12, 0.05))
    d = T_HIT - T_SLAP
    x = tt(d)
    speed = np.clip(x / d, 0, 1) ** 1.2
    thumps = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * np.cumsum(2 + 14 * speed) / SR))
    roll = (0.5 * noise(d, 50, 300, 5) * (0.3 + 0.7 * speed) + 0.25 * noise(d, 300, 1200, 6) * speed) * \
           (0.7 + 0.3 * thumps) * np.clip(x / 0.1, 0, 1)
    add(T_SLAP + 0.02, roll)
    for h in CANDLE_HITS:
        if h['t'] is not None:
            add(h['t'], 0.3 * np.sin(2 * np.pi * 1850 * tt(0.25)) * decay(0.25, 0.06))
            add(h['t'], 0.2 * noise(0.05, 2000, 8000, int(h['t'] * 100)) * decay(0.05, 0.01))
    add(T_HIT, 1.0 * np.sin(2 * np.pi * np.cumsum(np.linspace(90, 40, int(0.4 * SR))) / SR) * decay(0.4, 0.15))
    add(T_HIT, 0.7 * noise(0.5, 40, 600, 7) * decay(0.5, 0.15))
    for k in range(45):
        add(T_HIT + rg.uniform(0, 0.55) ** 1.5,
            rg.uniform(0.2, 0.55) * noise(0.12, 2500, 11000, 100 + k) * decay(0.12, rg.uniform(0.02, 0.06)))
    for k in range(25):
        add(T_HIT + rg.uniform(0, 0.5), rg.uniform(0.2, 0.45) * noise(0.1, 700, 4000, 200 + k) * decay(0.1, 0.03))
    for k in range(14):
        add(T_HIT + rg.uniform(0.05, 0.55),
            rg.uniform(0.1, 0.25) * np.sin(2 * np.pi * rg.uniform(2500, 5500) * tt(0.3)) * decay(0.3, 0.08))
    tr.save(path)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for ts in sys.argv[3:]:
            Image.fromarray(render(int(round(float(ts) * FPS)))).save(os.path.join(out, f'salt_{float(ts):05.2f}s.png'))
            print('saved', ts)
    elif mode == 'render':
        render_video(sys.argv[2], render, int(DUR * FPS), make_audio, crf=int(sys.argv[3]) if len(sys.argv) > 3 else 27)
