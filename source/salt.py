#!/usr/bin/env python3
"""The Salt: a 20 second comedy animation in pencil.

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

from pencil import Canvas, Track, blob, clamp01, col, ell, lerp, noise, render_video, sstep, sweep, tt, decay, \
    W, H, FPS, SR

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 20.0

# ---------------------------------------------------------------------------
# Palette: Bleak House greys, with colour only in the food, the wine and the salt
# ---------------------------------------------------------------------------
INK = col(0.14, 0.14, 0.15)
WALL = col(0.56, 0.57, 0.52)
WALL_D = col(0.45, 0.46, 0.42)
WAINSCOT = col(0.36, 0.33, 0.30)
FLOOR = col(0.33, 0.30, 0.27)
FLOOR_L = col(0.40, 0.37, 0.33)
WOOD = col(0.30, 0.25, 0.21)
WOOD_L = col(0.45, 0.39, 0.33)
PLY = col(0.62, 0.56, 0.46)
CLOTH = col(0.86, 0.85, 0.80)
CLOTH_S = col(0.70, 0.70, 0.66)
FRAME = col(0.50, 0.44, 0.33)
CANVAS_D = col(0.30, 0.31, 0.29)
SKIN = col(0.86, 0.79, 0.72)
SKIN_S = col(0.74, 0.66, 0.60)
ROUGE = col(0.80, 0.60, 0.58)
GOWN = col(0.43, 0.37, 0.43)
GOWN_L = col(0.55, 0.49, 0.54)
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
T_SPEAK_W = 3.2      # "Darling, would you pass the salt?" clip starts
T_CUT_H = 7.6        # cut to the husband
T_SPEAK_H = 8.0      # "Of course!" clip starts
T_WHIP = 11.9        # camera jerks back and away
T_WHIP_END = 12.35
T_TURN = 13.6        # he puts down his cutlery and turns to the boulder
T_WIND = 15.3        # wind-up
T_SLAP = 16.0        # slap!
T_HIT = 18.15        # the salt arrives
T_END = DUR

# ---------------------------------------------------------------------------
# The room, in metres. x runs along the table (wife at 0), y is up, z is across.
# ---------------------------------------------------------------------------
TABLE_Y = 0.75
FLAT_END = 11.0          # the ordinary part of the table
RAMP_R = 3.2             # the half-pipe curve
LIP_X = FLAT_END + RAMP_R
LIP_Y = TABLE_Y + RAMP_R
DECK_END = LIP_X + 1.1   # the flat top where he dines
HALF_W = 0.7             # half the table's width
WALL_Z = 3.6             # the long side wall
END_WALL_W = -3.2        # wall behind the wife
END_WALL_H = 18.2        # wall behind the husband
CEIL = 7.5

WIFE_SEAT = (-0.25, 0.48, 0.0)
HUSB_SEAT = (DECK_END + 0.35, LIP_Y - 0.45, 0.0)
BOULDER_R = 0.3
BOULDER_START = (DECK_END - 0.4, LIP_Y + BOULDER_R, 0.98)


def ramp_point(a):
    """Point on the curved table surface, a = 0 (bottom) .. pi/2 (top)."""
    return FLAT_END + RAMP_R * math.sin(a), TABLE_Y + RAMP_R - RAMP_R * math.cos(a)


# ---------------------------------------------------------------------------
# Camera
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
        """Pixels per metre at point p."""
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


def circle3(center, radius, n=28, axis='y'):
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    cx, cy, cz = center
    if axis == 'y':
        return np.stack([cx + radius * np.cos(th), np.full(n, cy), cz + radius * np.sin(th)], 1)
    if axis == 'z':
        return np.stack([cx + radius * np.cos(th), cy + radius * np.sin(th), np.full(n, cz)], 1)
    return np.stack([np.full(n, cx), cy + radius * np.sin(th), cz + radius * np.cos(th)], 1)


# ---------------------------------------------------------------------------
# The room
# ---------------------------------------------------------------------------
_rr = np.random.default_rng(3)
PAINTINGS = [(x, _rr.uniform(2.3, 3.2), _rr.uniform(1.0, 1.5), _rr.uniform(1.3, 1.9), i)
             for i, x in enumerate([-1.5, 2.2, 5.6, 9.0, 12.4, 15.8])]


def room(c, cam):
    # walls
    c.fill_screen(WALL, 1.1)
    for x0 in np.arange(-4, 19, 1.0):
        poly3(c, cam, [(x0, 0, -8), (x0 + 1, 0, -8), (x0 + 1, 0, WALL_Z), (x0, 0, WALL_Z)], fill=FLOOR, jit=0.3)
    for z0 in np.arange(-8, WALL_Z, 0.25):
        for x0 in np.arange(-4, 19, 3.0):
            line3(c, cam, [(x0, 0.001, z0), (x0 + 3, 0.001, z0)], col(0.26, 0.23, 0.21), lw=2, opacity=0.5)
    for x0 in np.arange(-2.5, 17.5, 1.0):
        poly3(c, cam, [(x0, 0.002, -1.3), (x0 + 1, 0.002, -1.3), (x0 + 1, 0.002, 1.3), (x0, 0.002, 1.3)],
              fill=col(0.42, 0.28, 0.28), jit=0.3)
    for zz in (-1.15, 1.15):
        line3(c, cam, [(-2.5, 0.003, zz), (17.5, 0.003, zz)], col(0.62, 0.52, 0.40), lw=3)
    # long side wall: paper, wainscot, damask hint
    poly3(c, cam, [(END_WALL_W, 0, WALL_Z), (END_WALL_H, 0, WALL_Z), (END_WALL_H, CEIL, WALL_Z),
                   (END_WALL_W, CEIL, WALL_Z)], fill=WALL, pressure=1.1, jit=0.5)
    for x0 in np.arange(END_WALL_W, END_WALL_H, 0.5):
        line3(c, cam, [(x0, 1.1, WALL_Z - 0.001), (x0, CEIL, WALL_Z - 0.001)], WALL_D, lw=4, opacity=0.5)
    poly3(c, cam, [(END_WALL_W, 0, WALL_Z - 0.01), (END_WALL_H, 0, WALL_Z - 0.01),
                   (END_WALL_H, 1.1, WALL_Z - 0.01), (END_WALL_W, 1.1, WALL_Z - 0.01)], fill=WAINSCOT, pressure=1.1,
          jit=0.5)
    line3(c, cam, [(END_WALL_W, 1.1, WALL_Z - 0.02), (END_WALL_H, 1.1, WALL_Z - 0.02)], WOOD, lw=5)
    for x0 in np.arange(END_WALL_W + 0.3, END_WALL_H, 1.2):
        poly3(c, cam, [(x0, 0.2, WALL_Z - 0.02), (x0 + 0.9, 0.2, WALL_Z - 0.02), (x0 + 0.9, 0.9, WALL_Z - 0.02),
                       (x0, 0.9, WALL_Z - 0.02)], None, WOOD, lw=2, opacity=0.8)
    # end walls (only the ones the camera faces)
    for xw, zs in ((END_WALL_W, (-8, WALL_Z)), (END_WALL_H, (-8, WALL_Z))):
        if (xw == END_WALL_W and cam.pos[0] < xw) or (xw == END_WALL_H and cam.pos[0] > xw):
            continue
        poly3(c, cam, [(xw, 0, zs[0]), (xw, 0, zs[1]), (xw, CEIL, zs[1]), (xw, CEIL, zs[0])], fill=WALL_D,
              pressure=1.1, jit=0.5)
        poly3(c, cam, [(xw, 0, zs[0]), (xw, 0, zs[1]), (xw, 1.1, zs[1]), (xw, 1.1, zs[0])], fill=WAINSCOT,
              pressure=1.1, jit=0.5)
    line3(c, cam, [(END_WALL_W, 0, WALL_Z), (END_WALL_W, CEIL, WALL_Z)], INK, lw=3, opacity=0.6)
    line3(c, cam, [(END_WALL_H, 0, WALL_Z), (END_WALL_H, CEIL, WALL_Z)], INK, lw=3, opacity=0.6)
    # paintings of noble ancestors, and hunting trophies between them
    for (x, y, w, h, i) in PAINTINGS:
        z = WALL_Z - 0.03
        poly3(c, cam, [(x - w / 2 - 0.1, y - h / 2 - 0.1, z), (x + w / 2 + 0.1, y - h / 2 - 0.1, z),
                       (x + w / 2 + 0.1, y + h / 2 + 0.1, z), (x - w / 2 - 0.1, y + h / 2 + 0.1, z)], fill=FRAME,
              line=INK, lw=3, pressure=1.1, jit=0.5)
        poly3(c, cam, [(x - w / 2, y - h / 2, z - 0.01), (x + w / 2, y - h / 2, z - 0.01), (x + w / 2, y + h / 2, z - 0.01),
                       (x - w / 2, y + h / 2, z - 0.01)], fill=CANVAS_D, pressure=1.1, jit=0.5)
        # a rough noble sitter: shoulders, head, a dash of collar
        poly3(c, cam, [(x - w * 0.35, y - h / 2, z - 0.02), (x - w * 0.25, y - h * 0.05, z - 0.02),
                       (x + w * 0.25, y - h * 0.05, z - 0.02), (x + w * 0.35, y - h / 2, z - 0.02)],
              fill=col(0.22, 0.22, 0.22), pressure=1.0, jit=0.8)
        poly3(c, cam, circle3((x, y + h * 0.13, z - 0.02), w * 0.16, 16, 'z'), fill=col(0.62, 0.57, 0.52),
              pressure=0.9, jit=0.8)
        tx = x + (w / 2 + 0.95)
        if tx < END_WALL_H - 0.6:
            # stag antlers on a shield plaque
            poly3(c, cam, circle3((tx, y + 0.1, z), 0.16, 12, 'z'), fill=WOOD, line=INK, lw=2, pressure=1.1)
            for sgn in (-1, 1):
                pts = [(tx + sgn * 0.08, y + 0.2, z), (tx + sgn * 0.3, y + 0.55, z), (tx + sgn * 0.42, y + 0.85, z)]
                line3(c, cam, pts, col(0.66, 0.60, 0.50), lw=4)
                for k in range(3):
                    b = pts[1] if k < 2 else pts[2]
                    line3(c, cam, [(b[0] - sgn * 0.02 * k, b[1] - 0.05 * k, z),
                                   (b[0] + sgn * (0.02 + 0.08 * k), b[1] + 0.2, z)], col(0.66, 0.60, 0.50), lw=3)
    # behind the wife: a crossed pair of hunting rifles over a portrait
    if cam.pos[0] < END_WALL_W:
        return
    z = END_WALL_W + 0.03
    poly3(c, cam, [(z, 2.0, -1.0), (z, 2.0, 1.0), (z, 3.6, 1.0), (z, 3.6, -1.0)], fill=FRAME, line=INK, lw=3)
    poly3(c, cam, [(z + 0.01, 2.1, -0.9), (z + 0.01, 2.1, 0.9), (z + 0.01, 3.5, 0.9), (z + 0.01, 3.5, -0.9)],
          fill=CANVAS_D)
    poly3(c, cam, circle3((z + 0.02, 3.0, 0.0), 0.28, 16, 'x'), fill=col(0.62, 0.57, 0.52), pressure=0.9)
    poly3(c, cam, [(z + 0.02, 2.1, -0.6), (z + 0.02, 2.7, -0.35), (z + 0.02, 2.7, 0.35), (z + 0.02, 2.1, 0.6)],
          fill=col(0.22, 0.22, 0.22))
    for sgn in (-1, 1):
        line3(c, cam, [(z + 0.03, 3.9, sgn * 1.3), (z + 0.03, 4.6, -sgn * 1.3)], WOOD, lw=6)
        line3(c, cam, [(z + 0.04, 4.1, sgn * 0.8), (z + 0.04, 4.55, -sgn * 1.25)], SILVER, lw=3)


def chandelier(c, cam, t, pos=(6.5, 5.6, 0.0)):
    x, y, z = pos
    line3(c, cam, [(x, CEIL, z), (x, y + 0.5, z)], INK, lw=2)
    for k in range(3):
        ring = circle3((x, y - 0.15 * k, z), 0.9 - 0.25 * k, 24)
        s, zc = cam.proj(ring)
        if (zc > 0.2).all():
            c.poly(s, None, col(0.55, 0.52, 0.46), lw=3)
    for k in range(8):
        a = k / 8 * 2 * math.pi
        bx, bz = x + 0.9 * math.cos(a), z + 0.9 * math.sin(a)
        line3(c, cam, [(bx, y, bz), (bx, y + 0.18, bz)], PLATE, lw=5)
        flame_at(c, cam, (bx, y + 0.24, bz), t, k, size=0.05)
    gx, gy = cam.pt((x, y, z))
    if cam.depth((x, y, z)) > 0.3:
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
    c.poly(pts, fill=FLAME, pressure=1.2, jit=0.3)
    c.poly([(sx, sy - s * 1.4 * flick), (sx + s * 0.25, sy), (sx - s * 0.25, sy)], fill=WHITE, pressure=1.2, jit=0.2)


# ---------------------------------------------------------------------------
# The table, and the half-pipe it becomes
# ---------------------------------------------------------------------------
def table(c, cam, t):
    near_z = -HALF_W
    # legs under the flat part
    for x in np.arange(0.4, FLAT_END, 1.8):
        for z in (-HALF_W + 0.1, HALF_W - 0.1):
            poly3(c, cam, [(x - 0.05, 0, z), (x + 0.05, 0, z), (x + 0.05, TABLE_Y, z), (x - 0.05, TABLE_Y, z)],
                  fill=WOOD, line=INK, lw=2, pressure=1.1)
    # the half-pipe's substructure: a panelled wooden side under the curve
    angs = np.linspace(0, math.pi / 2, 24)
    curve = [ramp_point(a) for a in angs]
    for zside in (HALF_W, near_z):
        side = [(FLAT_END - 0.4, 0, zside)] + [(x, y, zside) for x, y in curve] + [(DECK_END, LIP_Y, zside),
                                                                                    (DECK_END, 0, zside)]
        poly3(c, cam, side, fill=WOOD, line=INK, lw=3, pressure=1.15, jit=0.5)
        for xk in np.arange(FLAT_END + 0.4, DECK_END, 0.7):
            ytop = LIP_Y if xk >= LIP_X else TABLE_Y + RAMP_R - math.sqrt(max(0.0, RAMP_R ** 2 - (xk - FLAT_END) ** 2))
            line3(c, cam, [(xk, 0.05, zside), (xk, ytop - 0.05, zside)], WOOD_L, lw=2, opacity=0.7)
        line3(c, cam, [(x, y - 0.04, zside) for x, y in curve], PLY, lw=6)
    # the tablecloth: flat part, then curling up the ramp
    poly3(c, cam, [(0.25, TABLE_Y, -HALF_W), (FLAT_END, TABLE_Y, -HALF_W), (FLAT_END, TABLE_Y, HALF_W),
                   (0.25, TABLE_Y, HALF_W)], fill=CLOTH, line=INK, lw=3, pressure=1.15, jit=0.5)
    for i in range(len(angs) - 1):
        (x0, y0), (x1, y1) = curve[i], curve[i + 1]
        shade = CLOTH * (1 - 0.18 * i / len(angs)) + CLOTH_S * (0.18 * i / len(angs))
        poly3(c, cam, [(x0, y0, -HALF_W), (x1, y1, -HALF_W), (x1, y1, HALF_W), (x0, y0, HALF_W)], fill=shade,
              pressure=1.15, jit=0.3)
    line3(c, cam, [(x, y, -HALF_W) for x, y in curve], INK, lw=3)
    line3(c, cam, [(x, y, HALF_W) for x, y in curve], INK, lw=3)
    # the deck he dines on
    poly3(c, cam, [(LIP_X, LIP_Y, -HALF_W), (DECK_END, LIP_Y, -HALF_W), (DECK_END, LIP_Y, HALF_W),
                   (LIP_X, LIP_Y, HALF_W)], fill=CLOTH, line=INK, lw=3, pressure=1.15)
    line3(c, cam, [(LIP_X, LIP_Y + 0.01, -HALF_W), (LIP_X, LIP_Y + 0.01, HALF_W)], SILVER, lw=5)
    poly3(c, cam, [(DECK_END - 0.8, LIP_Y, HALF_W), (DECK_END, LIP_Y, HALF_W), (DECK_END, LIP_Y, 1.35),
                   (DECK_END - 0.8, LIP_Y, 1.35)], fill=CLOTH, line=INK, lw=3)
    poly3(c, cam, [(DECK_END - 0.8, LIP_Y, 1.35), (DECK_END, LIP_Y, 1.35), (DECK_END, LIP_Y - 0.25, 1.35),
                   (DECK_END - 0.8, LIP_Y - 0.25, 1.35)], fill=WOOD, line=INK, lw=3)
    # tablecloth hanging off the wife's end
    end = [(0.25, TABLE_Y, -HALF_W), (0.25, TABLE_Y, HALF_W)] + \
          [(0.26, TABLE_Y - 0.3 - 0.03 * math.sin(z * 9), z) for z in np.linspace(HALF_W, -HALF_W, 16)]
    poly3(c, cam, end, fill=CLOTH_S, line=INK, lw=2, jit=0.5)
    # tablecloth drape along the near edge
    drape = [(x, TABLE_Y, near_z) for x in np.linspace(0.25, FLAT_END, 12)]
    hem = [(x, TABLE_Y - 0.28 - 0.03 * math.sin(x * 3), near_z - 0.01) for x in np.linspace(FLAT_END, 0.25, 30)]
    poly3(c, cam, drape + hem, fill=CLOTH_S, line=INK, lw=2, pressure=1.1, jit=0.5)
    for x in np.arange(0.6, FLAT_END, 0.6):
        line3(c, cam, [(x, TABLE_Y, near_z - 0.01), (x + 0.05, TABLE_Y - 0.26, near_z - 0.01)], col(0.6, 0.6, 0.57),
              lw=2, opacity=0.6)
    # a line of candlesticks down the table
    for i, x in enumerate(np.arange(2.2, FLAT_END - 0.5, 2.2)):
        candle(c, cam, (x, TABLE_Y, 0.0), t, 20 + i)


def candle(c, cam, base, t, seed, h=0.22):
    x, y, z = base
    poly3(c, cam, circle3((x, y + 0.005, z), 0.05, 14), fill=SILVER, line=INK, lw=2)
    s1, z1 = cam.proj([(x, y, z)])
    if z1[0] < 0.2:
        return
    sc = cam.scale(base)
    bx, by = s1[0]
    wstick = max(2.0, 0.018 * sc)
    c.poly([(bx - wstick, by), (bx + wstick, by), (bx + wstick * 0.8, by - 0.1 * sc), (bx - wstick * 0.8, by - 0.1 * sc)],
           fill=SILVER, line=INK, lw=2, jit=0.3)
    c.poly([(bx - wstick * 0.7, by - 0.1 * sc), (bx + wstick * 0.7, by - 0.1 * sc), (bx + wstick * 0.7, by - h * sc),
            (bx - wstick * 0.7, by - h * sc)], fill=col(0.93, 0.91, 0.85), line=INK, lw=2, jit=0.3)
    flame_at(c, cam, (x, y + h + 0.03, z), t, seed)


def place_setting(c, cam, center, facing, t, seed, food=1.0, wine=1.0, show=True, knife_fork=False):
    """Plate of roast dinner, glass of red, candle and napkin on the table at `center`.
    `facing` is +1 if the diner sits at lower x, -1 if at higher x."""
    x, y, z = center
    poly3(c, cam, circle3((x, y + 0.004, z), 0.17, 30), fill=PLATE, line=INK, lw=2, pressure=1.2, jit=0.3)
    poly3(c, cam, circle3((x, y + 0.006, z), 0.12, 30), None, col(0.8, 0.8, 0.8), lw=2, opacity=0.8)
    rr = np.random.default_rng(seed)
    items = [(CHICKEN, 0.02, -0.03, 0.06), (POTATO, -0.05, 0.05, 0.035), (POTATO, 0.0, 0.07, 0.03),
             (CARROT, 0.06, 0.04, 0.025), (CARROT, 0.07, -0.02, 0.022)]
    for colr, dx, dz, r in items:
        if food > 0:
            poly3(c, cam, circle3((x + dx * facing, y + 0.02, z + dz), r * food, 14), fill=colr, line=INK, lw=1,
                  pressure=1.1, jit=0.3)
    for k in range(9):
        dx, dz = rr.uniform(-0.09, -0.02), rr.uniform(-0.08, 0.0)
        if food > 0:
            poly3(c, cam, circle3((x + dx * facing, y + 0.02, z + dz), 0.012, 8), fill=PEA, pressure=1.2, jit=0.1)
    poly3(c, cam, circle3((x + 0.04 * facing, y + 0.012, z - 0.06), 0.035, 12), fill=GRAVY, pressure=1.0,
          opacity=0.8, jit=0.2)
    # napkin, folded, and wine glass
    nz = z + 0.26
    poly3(c, cam, [(x - 0.08, y + 0.004, nz - 0.06), (x + 0.08, y + 0.004, nz - 0.06), (x + 0.08, y + 0.004, nz + 0.06),
                   (x - 0.08, y + 0.004, nz + 0.06)], fill=col(0.93, 0.92, 0.89), line=INK, lw=2)
    gx, gz = x + 0.18 * facing, z - 0.22
    glass_at(c, cam, (gx, y, gz), wine)
    candle(c, cam, (x + 0.3 * facing, y, z + 0.18), t, seed + 5, h=0.14)


def glass_at(c, cam, base, wine=1.0):
    x, y, z = base
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
        c.poly(wn, fill=WINE, pressure=1.2, jit=0.2)
    c.poly(bowl, None, INK, lw=2, jit=0.3)
    c.line([(sx - bw * 0.6, sy - stem - bh * 0.9), (sx - bw * 0.5, sy - stem - bh * 0.3)], WHITE, lw=max(2, 0.006 * sc),
           opacity=0.8)


# ---------------------------------------------------------------------------
# Characters (drawn flat, in screen space, at the size the camera sees them)
# s = pixels per metre, (x, y) = the seat point
# ---------------------------------------------------------------------------
def smooth_closed(pts, n=6):
    """A smooth closed curve through the given points (Catmull-Rom)."""
    p = np.asarray(pts, float)
    out = []
    m = len(p)
    for i in range(m):
        p0, p1, p2, p3 = p[i - 1], p[i], p[(i + 1) % m], p[(i + 2) % m]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    return out


def capsule(a, b, ra, rb, n=8):
    (ax, ay), (bx, by) = a, b
    ang = math.atan2(by - ay, bx - ax)
    pts = [(bx + rb * math.cos(ang + q), by + rb * math.sin(ang + q)) for q in np.linspace(-math.pi / 2, math.pi / 2, n)]
    pts += [(ax + ra * math.cos(ang + q), ay + ra * math.sin(ang + q)) for q in np.linspace(math.pi / 2, 3 * math.pi / 2, n)]
    return pts


def closed_eye(c, x, y, w, lw, lashes=True, flip=1):
    """A contented closed eye: a gentle arch, with a few lashes."""
    pts = [(x + w * math.cos(q), y - w * 0.5 * math.sin(q)) for q in np.linspace(0.1, math.pi - 0.1, 12)]
    c.line(pts, INK, lw=lw, jit=0.2)
    if lashes:
        for q in (0.35, 0.75, 1.15):
            px, py = x + w * math.cos(q) * flip, y - w * 0.5 * math.sin(q)
            c.line([(px, py), (px + w * 0.28 * flip, py + w * 0.12)], INK, lw=lw * 0.7, jit=0.1)


class Figure:
    """Helper for drawing a character in its own units (metres), mirrored if needed."""
    def __init__(self, c, x, y, s, flip=1, lean=0.0, pivot=(0.0, 0.0)):
        self.c, self.x, self.y, self.s, self.flip = c, x, y, s, flip
        self.ca, self.sa = math.cos(math.radians(lean)), math.sin(math.radians(lean))
        self.pv = pivot
        self.lw = max(2.0, s * 0.011)

    def P(self, u, v):
        u, v = u - self.pv[0], v - self.pv[1]
        u, v = u * self.ca - v * self.sa, u * self.sa + v * self.ca
        u, v = u + self.pv[0], v + self.pv[1]
        return self.x + u * self.flip * self.s, self.y - v * self.s

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


def wife(c, x, y, s, t, mouth=0.0, arm=0.0, chew=0.0, swallow=0.0, view='three_quarter', lean=0.0, flip=-1):
    """The wife, seated, in three-quarter view (drawn facing left; flip=-1 faces right), or from behind."""
    f = Figure(c, x, y, s, flip, lean, (0.0, 0.6))
    lw = f.lw
    # a high-backed dining chair
    f.smooth([(0.2, 0.0), (0.24, 0.6), (0.2, 1.12), (0.08, 1.2), (-0.06, 1.16), (-0.1, 0.6), (-0.08, 0.0)],
             fill=WOOD, line=INK, lw=lw, pressure=1.4)
    f.smooth([(0.14, 0.12), (0.17, 0.6), (0.14, 1.04), (0.06, 1.1), (-0.02, 1.06), (-0.04, 0.6), (-0.02, 0.12)],
             fill=col(0.38, 0.31, 0.36), pressure=1.4)
    if view == 'back':
        f.smooth([(-0.3, 0.0), (0.3, 0.0), (0.27, 0.4), (0.18, 0.56), (-0.18, 0.56), (-0.27, 0.4)], fill=GOWN,
                 line=INK, lw=lw, pressure=1.4)
        c.poly(f.ell(0.0, 0.8, 0.14, 0.15), fill=HAIR_W, line=INK, lw=lw, pressure=1.4)
        c.poly(f.ell(0.0, 1.0, 0.15, 0.12), fill=HAIR_W, line=INK, lw=lw, pressure=1.4)
        c.poly(f.ell(0.02, 1.14, 0.08, 0.07), fill=HAIR_W, line=INK, lw=lw, pressure=1.4)
        return
    # skirt spilling over the seat
    f.smooth([(-0.34, -0.02), (-0.2, 0.12), (0.2, 0.12), (0.3, -0.02), (0.36, -0.46), (-0.4, -0.46)], fill=GOWN,
             line=INK, lw=lw, pressure=1.4)
    # a portly bodice: bosom to the front (left), straight back
    f.smooth([(-0.19, 0.08), (-0.26, 0.28), (-0.22, 0.46), (-0.12, 0.55), (0.12, 0.56), (0.2, 0.46), (0.2, 0.25),
              (0.17, 0.08)], fill=GOWN, line=INK, lw=lw, pressure=1.4)
    f.smooth([(-0.2, 0.44), (-0.12, 0.52), (0.12, 0.53), (0.19, 0.44), (0.1, 0.4), (-0.12, 0.4)], fill=GOWN_L,
             pressure=1.3)
    c.line(f.pts([(-0.24, 0.3), (-0.1, 0.27), (0.18, 0.3)]), INK, lw=lw * 0.6, opacity=0.5)
    # puffed sleeve at the far shoulder
    c.poly(f.ell(0.17, 0.46, 0.07, 0.06), fill=GOWN_L, line=INK, lw=lw, pressure=1.4)
    # neck and pearls
    f.smooth([(-0.07, 0.5), (0.06, 0.5), (0.06, 0.65), (-0.07, 0.65)], fill=SKIN, line=INK, lw=lw * 0.8, pressure=1.4)
    for i in range(9):
        a = math.pi * (0.12 + 0.76 * i / 8)
        c.poly(f.ell(0.1 * math.cos(a) - 0.01, 0.56 - 0.05 * math.sin(a), 0.017, 0.017, 0, 10), fill=PEARL, line=INK,
               lw=lw * 0.4, pressure=1.4)
    # head: a proud egg, chin up
    hy = 0.8 - 0.012 * swallow
    f.smooth([(-0.12, 0.0 + hy), (-0.1, 0.1 + hy), (0.0, 0.16 + hy), (0.11, 0.1 + hy), (0.12, -0.02 + hy),
              (0.06, -0.13 + hy), (-0.05, -0.15 + hy)], fill=SKIN, line=INK, lw=lw, pressure=1.4)
    c.line(f.pts([(-0.07, hy - 0.16), (0.0, hy - 0.18), (0.07, hy - 0.14)]), INK, lw=lw * 0.6)  # double chin
    # grand grey-auburn updo with curls and a little feather
    f.smooth([(-0.13, 0.05 + hy), (-0.1, 0.2 + hy), (0.0, 0.27 + hy), (0.13, 0.22 + hy), (0.16, 0.05 + hy),
              (0.08, 0.1 + hy), (-0.05, 0.12 + hy)], fill=HAIR_W, line=INK, lw=lw, pressure=1.4)
    c.poly(f.ell(0.03, hy + 0.34, 0.1, 0.08), fill=HAIR_W, line=INK, lw=lw, pressure=1.4)
    for q in range(3):
        c.poly(f.ell(-0.05 + 0.08 * q, hy + 0.25 + 0.02 * (q % 2), 0.035, 0.03), None, INK, lw=lw * 0.5)
    f.smooth([(0.08, hy + 0.38), (0.14, hy + 0.44), (0.2, hy + 0.56), (0.15, hy + 0.5), (0.1, hy + 0.43)],
             fill=col(0.66, 0.64, 0.62), line=INK, lw=lw * 0.6, pressure=1.4)
    c.poly(f.ell(0.12, hy + 0.02, 0.045, 0.07), fill=HAIR_W, line=INK, lw=lw * 0.8, pressure=1.4)  # over the ear
    c.poly(f.ell(0.1, hy - 0.08, 0.015, 0.02), fill=PEARL, line=INK, lw=lw * 0.4, pressure=1.4)  # earring
    # a long, faintly upturned nose
    c.poly(f.pts([(-0.1, hy + 0.05), (-0.2, hy - 0.03), (-0.17, hy - 0.05), (-0.1, hy - 0.04)]), fill=SKIN, line=INK,
           lw=lw * 0.9, pressure=1.4)
    # closed, utterly contented eyes and high arched brows
    for ex, ew in ((-0.075, 0.028), (0.025, 0.034)):
        closed_eye(c, *f.P(ex, hy + 0.05), ew * s, lw * 0.9, flip=-flip)
        c.line(f.pts([(ex - ew, hy + 0.1), (ex, hy + 0.125), (ex + ew, hy + 0.105)]), INK, lw=lw * 0.7)
    c.poly(f.ell(0.03, hy - 0.035, 0.035, 0.022), fill=ROUGE, pressure=0.9, opacity=0.6, jit=0.3)
    # the mouth: prim when shut, round and noble when speaking
    mh = 0.004 + 0.034 * mouth + 0.012 * chew
    if mh > 0.01:
        c.poly(f.ell(-0.075, hy - 0.09, 0.03, mh), fill=col(0.35, 0.12, 0.14), line=col(0.55, 0.3, 0.3), lw=lw * 0.8,
               pressure=1.4)
    else:
        c.line(f.pts([(-0.095, hy - 0.083), (-0.075, hy - 0.09), (-0.055, hy - 0.083)]), col(0.5, 0.25, 0.25), lw=lw)
    # the fork hand: a conductor's flourish
    sx_, sy_ = -0.16, 0.46
    a1 = math.radians(235 - 45 * arm + 12 * arm * math.sin(t * 3.1))
    ex_, ey_ = sx_ + 0.22 * math.cos(a1), sy_ + 0.22 * math.sin(a1)
    a2 = math.radians(150 - 70 * arm + 35 * arm * math.sin(t * 3.1 + 0.8))
    hx_, hy_ = ex_ + 0.2 * math.cos(a2), ey_ + 0.2 * math.sin(a2)
    f.limb((sx_, sy_), (ex_, ey_), 0.05, 0.04, fill=GOWN, line=INK, lw=lw * 0.8, pressure=1.4)
    f.limb((ex_, ey_), (hx_, hy_), 0.04, 0.03, fill=col(0.82, 0.8, 0.76), line=INK, lw=lw * 0.8, pressure=1.4)
    c.poly(f.ell(sx_ + 0.02, sy_, 0.07, 0.06), fill=GOWN_L, line=INK, lw=lw, pressure=1.4)
    c.poly(f.ell(hx_, hy_, 0.035, 0.03), fill=col(0.82, 0.8, 0.76), line=INK, lw=lw * 0.8, pressure=1.4)
    fa = a2 + math.radians(35)
    fx, fy = hx_ + 0.14 * math.cos(fa), hy_ + 0.14 * math.sin(fa)
    c.line(f.pts([(hx_, hy_), (fx, fy)]), SILVER, lw=lw * 1.2)
    for d in (-0.012, 0.0, 0.012):
        c.line(f.pts([(fx, fy), (fx + 0.04 * math.cos(fa) - d * math.sin(fa), fy + 0.04 * math.sin(fa) + d * math.cos(fa))]),
               SILVER, lw=lw * 0.6)


def husband(c, x, y, s, t, mouth=0.0, flourish=0.0, eat=0.0, turn=0.0, wind=0.0, slap=0.0, grin=0.0):
    """The husband, seated, facing the camera. turn > 0 turns him towards the boulder (screen right)."""
    f = Figure(c, x, y, s)
    lw = f.lw
    # the back of his chair
    c.poly(f.pts([(-0.27, 0.1), (0.27, 0.1), (0.27, 0.7), (-0.27, 0.7)]), fill=WOOD, line=INK, lw=lw, pressure=1.4)
    c.poly(f.pts([(-0.22, 0.14), (0.22, 0.14), (0.22, 0.64), (-0.22, 0.64)]), fill=col(0.42, 0.26, 0.28), pressure=1.4)
    for sgn in (-1, 1):
        c.poly(f.pts([(sgn * 0.27 - 0.025, 0.1), (sgn * 0.27 + 0.025, 0.1), (sgn * 0.27 + 0.025, 0.74),
                      (sgn * 0.27 - 0.025, 0.74)]), fill=WOOD, line=INK, lw=lw * 0.8, pressure=1.4)
        c.poly(f.ell(sgn * 0.27, 0.78, 0.035, 0.04, 0, 12), fill=WOOD_L, line=INK, lw=lw * 0.8, pressure=1.4)
    # a portly, barrel-shaped tailcoat
    f.smooth([(-0.26, 0.0), (-0.31, 0.22), (-0.28, 0.46), (-0.18, 0.56), (0.18, 0.56), (0.28, 0.46), (0.31, 0.22),
              (0.26, 0.0)], fill=COAT, line=INK, lw=lw, pressure=1.4)
    f.smooth([(-0.15, 0.02), (-0.2, 0.22), (-0.12, 0.48), (0.12, 0.48), (0.2, 0.22), (0.15, 0.02)],
             fill=col(0.5, 0.5, 0.48), line=INK, lw=lw * 0.8, pressure=1.4)
    for v in (0.1, 0.19, 0.28):
        c.poly(f.ell(0.0, v, 0.013, 0.013, 0, 8), fill=SILVER, line=INK, lw=lw * 0.3, pressure=1.4)
    c.line(f.pts([(-0.1, 0.15), (-0.03, 0.12), (0.02, 0.16)]), SILVER, lw=lw * 0.7)  # watch chain
    c.poly(f.pts([(-0.07, 0.32), (0.07, 0.32), (0.09, 0.53), (-0.09, 0.53)]), fill=SHIRT, line=INK, lw=lw * 0.6,
           pressure=1.4)
    for sgn in (-1, 1):
        c.poly(f.pts([(sgn * 0.09, 0.53), (sgn * 0.17, 0.53), (sgn * 0.13, 0.25)]), fill=COAT_L, line=INK, lw=lw * 0.6,
               pressure=1.4)
    c.poly(f.pts([(-0.07, 0.51), (0.0, 0.535), (0.07, 0.51), (0.07, 0.575), (0.0, 0.55), (-0.07, 0.575)]), fill=INK,
           pressure=1.5)
    # head: bald dome, a general's jaw, Dickensian clouds of grey at the sides
    hx0, hy0 = 0.03 * turn, 0.8
    f.smooth([(hx0 - 0.13, hy0 + 0.02), (hx0 - 0.1, hy0 + 0.16), (hx0, hy0 + 0.21), (hx0 + 0.1, hy0 + 0.16),
              (hx0 + 0.13, hy0 + 0.02), (hx0 + 0.12, hy0 - 0.12), (hx0 + 0.05, hy0 - 0.2), (hx0 - 0.05, hy0 - 0.2),
              (hx0 - 0.12, hy0 - 0.12)], fill=SKIN, line=INK, lw=lw, pressure=1.4)
    c.poly(f.ell(hx0 - 0.05, hy0 + 0.15, 0.04, 0.02, 20), fill=WHITE, pressure=1.0, opacity=0.7)
    for sgn in (-1, 1):
        c.poly(f.ell(hx0 + sgn * 0.14, hy0 - 0.01, 0.025, 0.04), fill=SKIN_S, line=INK, lw=lw * 0.7, pressure=1.4)
        for i, (du, dv, r) in enumerate(((0.15, 0.08, 0.05), (0.18, 0.02, 0.055), (0.16, -0.05, 0.05), (0.2, 0.09, 0.04))):
            c.poly(f.ell(hx0 + sgn * du, hy0 + dv, r, r * 0.85, 0, 14), fill=HAIR_H, line=INK, lw=lw * 0.7,
                   pressure=1.4)
    # eyes closed in contentment, bushy brows
    for sgn in (-1, 1):
        closed_eye(c, *f.P(hx0 + sgn * 0.05, hy0 + 0.05), 0.032 * s, lw * 0.9, lashes=False)
        c.poly(f.pts([(hx0 + sgn * 0.015, hy0 + 0.095), (hx0 + sgn * 0.09, hy0 + 0.125), (hx0 + sgn * 0.095, hy0 + 0.095)]),
               fill=HAIR_H, line=INK, lw=lw * 0.6, pressure=1.4)
    c.poly(f.pts([(hx0 - 0.015, hy0 + 0.06), (hx0 + 0.03 + 0.03 * turn, hy0 - 0.055), (hx0, hy0 - 0.065),
                  (hx0 - 0.035, hy0 - 0.05)]), fill=SKIN_S, line=INK, lw=lw * 0.9, pressure=1.4)
    # mouth: a general's grin of teeth when he speaks or beams
    open_ = max(mouth, grin * 0.5)
    if open_ > 0.05:
        c.poly(f.ell(hx0, hy0 - 0.13, 0.065, 0.012 + 0.04 * open_), fill=col(0.3, 0.1, 0.1), line=INK, lw=lw * 0.8,
               pressure=1.4)
        c.poly(f.pts([(hx0 - 0.055, hy0 - 0.113), (hx0 + 0.055, hy0 - 0.113), (hx0 + 0.05, hy0 - 0.135),
                      (hx0 - 0.05, hy0 - 0.135)]), fill=WHITE, line=INK, lw=lw * 0.4, pressure=1.4)
        for k in range(-2, 3):
            c.line(f.pts([(hx0 + k * 0.02, hy0 - 0.113), (hx0 + k * 0.02, hy0 - 0.135)]), INK, lw=lw * 0.3)
    else:
        c.line(f.pts([(hx0 - 0.05, hy0 - 0.125), (hx0, hy0 - 0.135), (hx0 + 0.05, hy0 - 0.125)]), INK, lw=lw)
    # the glorious handlebar moustache
    for sgn in (-1, 1):
        pts = [(hx0, hy0 - 0.075)]
        for q in np.linspace(0, 1, 9):
            pts.append((hx0 + sgn * (0.02 + 0.17 * q), hy0 - 0.085 - 0.025 * math.sin(q * math.pi) + 0.08 * q ** 3))
        curl = [(hx0 + sgn * (0.19 + 0.03 * math.cos(q)), hy0 + 0.02 + 0.03 * math.sin(q))
                for q in np.linspace(-0.5 * math.pi, 1.4 * math.pi, 9)]
        body = pts + curl
        c.line(f.pts(body), HAIR_H, lw=0.04 * s, jit=0.2)
        c.line(f.pts(body), INK, lw=lw * 0.5, jit=0.2, opacity=0.85)
    # arms: knife and fork held up nobly; the flourish spreads them; the slap swings his left arm out
    for sgn in (-1, 1):
        sxp, syp = sgn * 0.25, 0.47
        tool = True
        if sgn > 0 and (wind > 0 or slap > 0):
            a1 = math.radians(-40 + 120 * wind - 120 * slap)
            ex_, ey_ = sxp + 0.24 * math.cos(a1), syp + 0.24 * math.sin(a1)
            a2 = a1 - math.radians(20 - 60 * wind)
            hx_, hy_ = ex_ + 0.22 * math.cos(a2), ey_ + 0.22 * math.sin(a2)
            tool = False
        else:
            spread = flourish * (0.6 + 0.4 * math.sin(t * 4.0 + (0 if sgn > 0 else 1.2)))
            a1 = math.radians(-90 + sgn * (25 + 55 * spread))
            ex_, ey_ = sxp + 0.21 * math.cos(a1), syp + 0.21 * math.sin(a1)
            a2 = math.radians(90 - sgn * (60 - 50 * spread)) + 0.15 * math.sin(t * 7) * eat
            hx_, hy_ = ex_ + 0.19 * math.cos(a2), ey_ + 0.19 * math.sin(a2)
            if turn > 0.5 and sgn > 0:
                tool = False
        f.limb((sxp, syp), (ex_, ey_), 0.06, 0.05, fill=COAT, line=INK, lw=lw * 0.8, pressure=1.4)
        f.limb((ex_, ey_), (hx_, hy_), 0.05, 0.042, fill=COAT, line=INK, lw=lw * 0.8, pressure=1.4)
        c.poly(f.ell(hx_, hy_, 0.04, 0.03, 0, 12), fill=SHIRT, line=INK, lw=lw * 0.6, pressure=1.4)
        c.poly(f.ell(hx_ + 0.005 * sgn, hy_ + 0.035, 0.035, 0.035, 0, 12), fill=SKIN, line=INK, lw=lw * 0.8,
               pressure=1.4)
        if tool:
            c.line(f.pts([(hx_, hy_ + 0.03), (hx_, hy_ + 0.17)]), SILVER, lw=lw * 1.2)
            if sgn < 0:
                for d in (-0.012, 0.0, 0.012):
                    c.line(f.pts([(hx_ + d, hy_ + 0.17), (hx_ + d, hy_ + 0.21)]), SILVER, lw=lw * 0.6)
            else:
                c.poly(f.pts([(hx_ - 0.012, hy_ + 0.17), (hx_ + 0.014, hy_ + 0.17), (hx_, hy_ + 0.25)]), fill=SILVER,
                       line=INK, lw=lw * 0.4)


def tall_chair(c, cam, seat):
    """His absurd chair: spindly legs from the floor, and a ladder up its side."""
    x, y, z = seat
    legs = [(x - 0.22, z - 0.22), (x + 0.22, z - 0.22), (x - 0.22, z + 0.22), (x + 0.22, z + 0.22)]
    for (lx, lz) in legs:
        line3(c, cam, [(lx, 0, lz), (lx, y, lz)], WOOD, lw=max(3, cam.scale((lx, y / 2, lz)) * 0.04))
    for yy in np.arange(0.6, y, 0.9):
        line3(c, cam, [(x - 0.22, yy, z - 0.22), (x + 0.22, yy, z - 0.22)], WOOD, lw=3)
        line3(c, cam, [(x - 0.22, yy, z + 0.22), (x + 0.22, yy, z + 0.22)], WOOD, lw=3)
        line3(c, cam, [(x - 0.22, yy + 0.4, z - 0.22), (x - 0.22, yy + 0.4, z + 0.22)], WOOD, lw=3)
    # ladder up the side
    lz = z - 0.55
    for dx in (-0.15, 0.15):
        line3(c, cam, [(x + dx, 0, lz - 0.25), (x + dx, y, lz)], WOOD_L, lw=4)
    for yy in np.arange(0.3, y, 0.3):
        f = yy / y
        line3(c, cam, [(x - 0.15, yy, lz - 0.25 * (1 - f)), (x + 0.15, yy, lz - 0.25 * (1 - f))], WOOD_L, lw=3)
    poly3(c, cam, [(x - 0.26, y, z - 0.26), (x + 0.26, y, z - 0.26), (x + 0.26, y, z + 0.26), (x - 0.26, y, z + 0.26)],
          fill=col(0.36, 0.30, 0.34), line=INK, lw=3)
    poly3(c, cam, [(x + 0.24, y, z - 0.26), (x + 0.24, y, z + 0.26), (x + 0.24, y + 1.1, z + 0.22),
                   (x + 0.24, y + 1.1, z - 0.22)], fill=WOOD, line=INK, lw=3)


# ---------------------------------------------------------------------------
# The salt
# ---------------------------------------------------------------------------
_rs = np.random.default_rng(8)
SALT_FACETS = [(_rs.uniform(0, 2 * np.pi), _rs.uniform(0.2, 0.85), _rs.uniform(0.15, 0.3)) for _ in range(9)]


def salt_boulder(c, cam, p, spin=0.0):
    if cam.depth(p) < 0.2:
        return
    sx, sy = cam.pt(p)
    r = cam.scale(p) * BOULDER_R
    c.glow(sx, sy, r * 2.2, WHITE, 0.35)
    c.poly(blob(sx, sy, r, 44, 26, 0.12), fill=SALT, line=col(0.45, 0.5, 0.58), lw=max(2, r * 0.03), pressure=1.3)
    for a, rho, sz in SALT_FACETS:
        aa = a + spin
        fx, fy = sx + rho * r * math.cos(aa) * 0.8, sy + rho * r * math.sin(aa) * 0.8
        c.poly(blob(fx, fy, sz * r, int(a * 10), 6, 0.3), fill=SALT_S, pressure=0.8, opacity=0.6, jit=0.5)
        c.line([(fx - sz * r * 0.6, fy), (fx + sz * r * 0.4, fy - sz * r * 0.5)], WHITE, lw=max(1.5, r * 0.03),
               opacity=0.9)
    c.poly(ell(sx - r * 0.35, sy - r * 0.4, r * 0.2, r * 0.1, -30, 12), fill=WHITE, pressure=1.3)
    for q in (0.3, 1.9, 3.8):
        gx, gy = sx + r * 1.05 * math.cos(q + spin * 0.2), sy + r * 1.05 * math.sin(q + spin * 0.2)
        c.line([(gx - r * 0.12, gy), (gx + r * 0.12, gy)], WHITE, lw=2, opacity=0.9)
        c.line([(gx, gy - r * 0.12), (gx, gy + r * 0.12)], WHITE, lw=2, opacity=0.9)


def boulder_path(t):
    """Where the salt is at time t, and how far it has rolled (for its spin)."""
    x0, y0, z0 = BOULDER_START
    if t < T_SLAP:
        return (x0, y0, z0), 0.0
    u = t - T_SLAP
    deck = x0 - LIP_X
    arc = RAMP_R * math.pi / 2
    flat = FLAT_END - 0.1
    if u < 0.35:
        e = (u / 0.35) ** 2
        d = deck * e
        return (x0 - d, y0, lerp(z0, 0.55, e)), d
    u -= 0.35
    if u < 0.5:
        f = (u / 0.5) ** 1.6
        a = math.pi / 2 * (1 - f)
        px, py = ramp_point(a)
        nx, ny = -math.sin(a), math.cos(a)  # surface normal points into the pipe
        zz = lerp(0.55, 0.25, f)
        return (px + nx * BOULDER_R, py + ny * BOULDER_R, zz), deck + arc * f
    u -= 0.5
    dur = T_HIT - T_SLAP - 0.85
    f = u / dur
    s = flat * (0.8 * f + 0.2 * f * f)
    return (FLAT_END - s, TABLE_Y + BOULDER_R, lerp(0.25, 0.0, min(1.0, f))), deck + arc + s


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
CAM_A = ((2.6, 1.35, 1.45), (0.02, 0.92, 0.02), 45)        # her one o'clock
CAM_B = ((HUSB_SEAT[0] - 2.7, LIP_Y + 0.6, 0.0), (HUSB_SEAT[0], LIP_Y + 0.3, 0.0), 42)  # his twelve
CAM_C = ((-2.9, 4.8, -2.0), (7.0, 1.0, 0.2), 68)        # the whole absurd arrangement


def camera(t):
    if t < T_CUT_H:
        (p, g, f) = CAM_A
        k = 0.03 * t / T_CUT_H
        p = tuple(np.array(p) + (np.array(g) - np.array(p)) * k)
        return Cam(p, g, f)
    if t < T_WHIP:
        return Cam(*CAM_B)
    u = clamp01((t - T_WHIP) / (T_WHIP_END - T_WHIP))
    e = 1 - (1 - u) ** 3
    p = np.array(CAM_B[0]) * (1 - e) + np.array(CAM_C[0]) * e
    g = np.array(CAM_B[1]) * (1 - e) + np.array(CAM_C[1]) * e
    f = CAM_B[2] * (1 - e) + CAM_C[2] * e
    if t > T_HIT:
        sh = 0.12 * max(0.0, 1 - (t - T_HIT) / 0.5)
        r = np.random.default_rng(int(t * FPS))
        p = p + r.normal(0, sh, 3)
    return Cam(tuple(p), tuple(g), f)


def draw_world(c, cam, t):
    room(c, cam)
    chandelier(c, cam, t)
    tall_chair(c, cam, HUSB_SEAT)
    wife_behind_table = cam.pos[0] > WIFE_SEAT[0] + 0.5 and t < T_HIT and cam.depth(WIFE_SEAT) > 0.5
    if wife_behind_table:
        wife_figure(c, cam, t)
    table(c, cam, t)
    if wife_behind_table:
        place_setting(c, cam, (0.5, TABLE_Y, 0.0), 1, t, 3)
    # the husband
    if cam.depth(HUSB_SEAT) < 0.5:
        bp, rolled = boulder_path(t)
        if cam.depth(bp) > 0.5:
            salt_boulder(c, cam, bp, spin=rolled / BOULDER_R)
        if (cam.depth(WIFE_SEAT) > 0.5 and not wife_behind_table) or t >= T_HIT:
            wife_scene(c, cam, t)
        return
    sx, sy = cam.pt(HUSB_SEAT)
    s = cam.scale(HUSB_SEAT)
    speak = mouth_at(MOUTH_H, T_SPEAK_H, t)
    flourish = speaking(MOUTH_H, T_SPEAK_H, t) * sstep(T_SPEAK_H + 0.8, T_SPEAK_H + 1.1, t)
    eat = 1.0 if T_CUT_H < t < T_SPEAK_H + 0.9 else 0.0
    turn = sstep(T_TURN, T_TURN + 0.6, t)
    wind = sstep(T_WIND, T_SLAP - 0.1, t) * (1 - sstep(T_SLAP - 0.1, T_SLAP, t))
    slap = sstep(T_SLAP - 0.1, T_SLAP + 0.05, t) * (1 - sstep(T_SLAP + 0.4, T_SLAP + 1.0, t))
    husband(c, sx, sy, s, t, mouth=speak, flourish=flourish, eat=eat, turn=turn, wind=wind, slap=slap)
    place_setting(c, cam, (LIP_X + 0.55, LIP_Y, 0.0), -1, t, 7)
    # the salt
    bp, rolled = boulder_path(t)
    salt_boulder(c, cam, bp, spin=rolled / BOULDER_R)
    # the wife and her dinner (unless the salt has arrived)
    if not wife_behind_table:
        wife_scene(c, cam, t)


def wife_scene(c, cam, t):
    if t < T_HIT and cam.depth(WIFE_SEAT) < 0.5:
        return
    if t < T_HIT:
        place_setting(c, cam, (0.5, TABLE_Y, 0.0), 1, t, 3)
        wife_figure(c, cam, t)
    else:
        wife_flies(c, cam, t)


def wife_figure(c, cam, t):
    if True:
        sx, sy = cam.pt(WIFE_SEAT)
        s = cam.scale(WIFE_SEAT)
        chew = max(0.0, math.sin(t * 9)) if t < 1.3 else 0.0
        swallow = math.sin(math.pi * clamp01((t - 2.1) / 0.4))
        mouth = mouth_at(MOUTH_W, T_SPEAK_W, t)
        arm = speaking(MOUTH_W, T_SPEAK_W, t)
        view = 'three_quarter' if t < T_CUT_H else 'back'
        wife(c, sx, sy, s, t, mouth=mouth, arm=arm, chew=chew, swallow=swallow, view=view)


def wife_flies(c, cam, t):
    if True:
        u = t - T_HIT
        # the wife, her chair and her dinner fly back, past the camera
        for i, (vx, vy, vz, spin, kind) in enumerate([(-9, 5, -3, 400, 'wife'), (-8, 3, -1, -300, 'plate'),
                                                     (-7, 6, 2, 500, 'glass'), (-10, 4, -2, 200, 'candle')]):
            p = (0.3 + vx * u, TABLE_Y + 0.4 + vy * u - 4.9 * u * u, vz * u)
            if cam.depth(p) < 0.3:
                continue
            sx, sy = cam.pt(p)
            s = cam.scale(p)
            if kind == 'wife':
                wife(c, sx, sy, s, t, mouth=0.8, view='three_quarter', lean=spin * u)
            elif kind == 'plate':
                c.poly(ell(sx, sy, 0.17 * s, 0.06 * s, spin * u, 20), fill=PLATE, line=INK, lw=3)
            elif kind == 'glass':
                c.poly(ell(sx, sy, 0.05 * s, 0.1 * s, spin * u, 12), fill=GLASS, line=INK, lw=2)
        r = np.random.default_rng(12)
        for i in range(60):
            v = r.normal(0, 1, 3) * [3, 3, 3] + [-6, 3, 0]
            p = (0.4 + v[0] * u, TABLE_Y + 0.3 + v[1] * u - 4.9 * u * u, v[2] * u)
            if p[1] < 0 or cam.depth(p) < 0.3:
                continue
            sx, sy = cam.pt(p)
            s = cam.scale(p)
            colr = [PLATE, GLASS, PEA, CARROT, POTATO, WINE, SALT][i % 7]
            c.poly(blob(sx, sy, max(3, 0.03 * s), i, 6, 0.4), fill=colr, line=INK, lw=1.5)


def render(d):
    t = d / FPS
    c = SharpCanvas(d)
    cam = camera(t)
    draw_world(c, cam, t)
    return c.result()


# ---------------------------------------------------------------------------
# Sound
# ---------------------------------------------------------------------------
def make_audio(path):
    tr = Track(DUR)
    add = tr.add
    add(0.0, 0.015 * noise(DUR, 300, 3000, 1) * (0.7 + 0.3 * np.random.default_rng(2).random(int(DUR * SR))))
    add(T_SPEAK_W, 0.9 * VOICE_W / (np.abs(VOICE_W).max() + 1e-9))
    add(T_SPEAK_H, 0.9 * VOICE_H / (np.abs(VOICE_H).max() + 1e-9))
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
