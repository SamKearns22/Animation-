#!/usr/bin/env python3
"""Beaver vs Asteroid: a 45 second coloured-pencil animation.

Usage:
    python3 beaver_asteroid.py stills OUT_DIR T1 T2 ...   # save single frames at given seconds
    python3 beaver_asteroid.py render OUT.mp4 [CRF]       # render the full video with sound
"""
import math
import os
import sys

import numpy as np
from PIL import Image

from pencil import *  # noqa: F401,F403  (canvas, colours, helpers)
from pencil import FIRE, Canvas, Track, blob, clamp01, col, ell, flame, lerp, noise, render_video, smoke_wisp, \
    sstep, stars, sweep, tt, decay, W, H, FPS

DUR = 45.0

# Story timeline (seconds)
T_THREAT = 3.0     # light and rumble start to build
T_LAUNCH = 16.0    # beaver rockets upwards
T_MID = 16.8       # mid-range: shooting up through ordinary clouds
T_CLOUDS = 18.8    # wide shot: bursting through the high cloud layer
T_SPACE = 22.5     # silent majesty of the Earth
T_REVEAL = 25.0    # camera pulls back to reveal the asteroid
T_FACE = 28.5      # the unbothered face
T_IMPACT = 30.5    # streak hits the asteroid
T_INSIDE = 31.4    # smashing through the rock
T_BURST = 32.4     # out the other side
T_EXPLODE = 33.1   # asteroid explodes
T_WHITE = 33.5     # white light fills the screen
T_HOME = 34.4      # back to the forest
T_DROP = 35.1      # beaver drops from the sky
T_LAND = 35.4      # thud
T_CHEW = 37.0      # starts eating

# Little signs of life: nose twitches and blinks (start times, seconds)
TWITCHES = [0.8, 2.4, 4.6, 6.9, 9.3, 10.8, 13.8, 36.2, 38.9, 41.8, 44.2]
BLINKS = [1.6, 5.4, 8.2, 10.3, 13.3, 14.4, 36.7, 40.3, 43.1]
FACE_BLINK = 29.4
# glances straight up at the sky: a long one, then a quick one just before launch
LOOKS = [(T_LAUNCH - 4.0, T_LAUNCH - 3.1), (T_LAUNCH - 1.0, T_LAUNCH - 0.7)]

# ---------------------------------------------------------------------------
# Colours for this film
# ---------------------------------------------------------------------------
FUR = [col(0.19, 0.11, 0.07), col(0.33, 0.19, 0.10), col(0.47, 0.28, 0.15), col(0.60, 0.37, 0.19),
       col(0.74, 0.50, 0.28), col(0.62, 0.53, 0.44)]  # dark .. light, then grey-tan muzzle
FUR_BASE = col(0.42, 0.25, 0.13)
SKIN = col(0.22, 0.19, 0.18)
CLAW = col(0.80, 0.76, 0.68)
INCISOR = col(0.93, 0.47, 0.13)
INCISOR_D = col(0.58, 0.24, 0.08)
NOSE_C = col(0.14, 0.12, 0.12)
TAIL_C = col(0.24, 0.22, 0.23)
TAIL_SCALE = col(0.44, 0.42, 0.42)
TWIG = col(0.45, 0.32, 0.20)
LEAF = col(0.42, 0.60, 0.26)
LEAF_D = col(0.22, 0.40, 0.16)
AURA = (col(0.62, 0.78, 1.0), col(0.86, 0.93, 1.0), col(1.0, 1.0, 1.0))
STREAK = (col(0.93, 0.55, 0.22), col(1.0, 0.86, 0.60), col(1.0, 1.0, 0.97))
NIGHT = col(0.08, 0.12, 0.22)
DEEP = col(0.03, 0.04, 0.08)


# ---------------------------------------------------------------------------
# The beaver: a realistic, field-guide style drawing built from fur strokes
# ---------------------------------------------------------------------------
BODY_ELL = [(0.0, -0.92, 1.08, 0.95), (0.0, -1.72, 0.90, 0.74), (0.0, -2.42, 0.82, 0.56),
            (-0.42, -2.22, 0.44, 0.36), (0.42, -2.22, 0.44, 0.36)]
LIGHT_DIR = np.array([-0.5, -0.65, 0.6]) / np.linalg.norm([-0.5, -0.65, 0.6])
MUZZLE = (0.0, -2.19, 0.40, 0.30)


def _body_depth(px, py):
    best = np.full(px.shape, 9.0)
    nx = np.zeros(px.shape)
    ny = np.zeros(px.shape)
    for cx, cy, rx, ry in BODY_ELL:
        dx, dy = (px - cx) / rx, (py - cy) / ry
        d = dx * dx + dy * dy
        m = d < best
        best, nx, ny = np.where(m, d, best), np.where(m, dx, nx), np.where(m, dy, ny)
    return best, nx, ny


def _make_fur(n, seed, lmin, lmax, ymax=0.2, edge=True):
    r = np.random.default_rng(seed)
    px = r.uniform(-1.15, 1.15, n * 4)
    py = r.uniform(-3.05, ymax, n * 4)
    d, nx, ny = _body_depth(px, py)
    keep = d < 1.0
    px, py, d, nx, ny = px[keep][:n], py[keep][:n], d[keep][:n], nx[keep][:n], ny[keep][:n]
    head = (py < -1.98)
    vx, vy = px - 0.0, py + 2.22
    vl = np.hypot(vx, vy) + 1e-6
    hx, hy = vx / vl, vy / vl + 0.35
    bx, by = 0.28 * px, np.ones_like(px)
    dx, dy = np.where(head, hx, bx), np.where(head, hy, by)
    ang = np.arctan2(dy, dx) + r.normal(0, 0.22, len(px))
    dx, dy = np.cos(ang), np.sin(ang)
    L = r.uniform(lmin, lmax, len(px)) * np.where(head, 0.7, 1.0)
    curve = r.uniform(-0.35, 0.35, len(px)) * L
    pxn, pyn = -dy, dx
    s0 = np.stack([px - dx * L * 0.35, py - dy * L * 0.35], 1)
    s1 = np.stack([px + dx * L * 0.15 + pxn * curve * 0.5, py + dy * L * 0.15 + pyn * curve * 0.5], 1)
    s2 = np.stack([px + dx * L * 0.65, py + dy * L * 0.65], 1)
    strokes = np.stack([s0, s1, s2], 1)
    nz = np.sqrt(np.clip(1 - d, 0, 1))
    nrm = np.stack([nx, ny, nz * 1.2], 1)
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True)
    lam = nrm @ LIGHT_DIR
    tone = np.clip((lam + 0.25) / 1.15, 0, 1) * 4.99 + r.normal(0, 0.7, len(px))
    tone = np.where(d > 0.8, tone - 1.2, tone)
    tone = np.clip(tone, 0, 4).astype(int)
    mcx, mcy, mrx, mry = MUZZLE
    in_muzzle = ((px - mcx) / mrx) ** 2 + ((py - mcy) / mry) ** 2 < 1
    tone = np.where(in_muzzle & (r.random(len(px)) < 0.75), 5, tone)
    out = {k: strokes[tone == k] for k in range(6)}
    if edge:
        m = int(n * 0.25)
        th = r.uniform(0, 2 * np.pi, m * 3)
        part = r.integers(0, len(BODY_ELL), m * 3)
        ex = []
        for th_, pi in zip(th, part):
            cx, cy, rx, ry = BODY_ELL[pi]
            x, y = cx + rx * math.cos(th_) * 0.97, cy + ry * math.sin(th_) * 0.97
            others = min(((x - c2x) / r2x) ** 2 + ((y - c2y) / r2y) ** 2
                         for j, (c2x, c2y, r2x, r2y) in enumerate(BODY_ELL) if j != pi)
            if others > 0.98 and y < ymax:
                ex.append((x, y, math.cos(th_), math.sin(th_)))
            if len(ex) >= m:
                break
        e = np.array(ex)
        ddx, ddy = e[:, 2], e[:, 3] + 0.9
        dl = np.hypot(ddx, ddy) + 1e-6
        ddx, ddy = ddx / dl, ddy / dl
        L = r.uniform(lmin, lmax * 1.3, len(e))
        s0 = np.stack([e[:, 0] - ddx * L * 0.4, e[:, 1] - ddy * L * 0.4], 1)
        s1 = np.stack([e[:, 0] + ddx * L * 0.2, e[:, 1] + ddy * L * 0.2], 1)
        s2 = np.stack([e[:, 0] + ddx * L * 0.6 + 0.02, e[:, 1] + ddy * L * 0.6], 1)
        es = np.stack([s0, s1, s2], 1)
        lit = e[:, 2] * LIGHT_DIR[0] + e[:, 3] * LIGHT_DIR[1] > 0.1
        out['edge_lit'] = es[lit]
        out['edge_dark'] = es[~lit]
    return out


FUR_MAIN = _make_fur(2600, 1, 0.10, 0.2)
FUR_FINE = _make_fur(11000, 2, 0.05, 0.11, ymax=-0.9, edge=False)


def _make_clumps(n, seed):
    """Wet-looking clumps: a few strokes meeting at a point, with a lit edge."""
    r = np.random.default_rng(seed)
    px = r.uniform(-1.1, 1.1, n * 4)
    py = r.uniform(-2.95, 0.0, n * 4)
    d, nx, ny = _body_depth(px, py)
    keep = (d < 0.92) & ~(((px / 0.45) ** 2 + ((py + 2.3) / 0.35) ** 2) < 1)
    px, py, nx, ny = px[keep][:n], py[keep][:n], nx[keep][:n], ny[keep][:n]
    dark, lit = [], []
    for x, y, a, b in zip(px, py, nx, ny):
        if y < -1.98:
            vx, vy = x, y + 2.22
            l = math.hypot(vx, vy) + 1e-6
            dx, dy = vx / l, vy / l + 0.35
        else:
            dx, dy = 0.28 * x, 1.0
        l = math.hypot(dx, dy)
        dx, dy = dx / l, dy / l
        L = r.uniform(0.12, 0.22) * (0.65 if y < -1.98 else 1.0)
        tipx, tipy = x + dx * L, y + dy * L
        wdt = L * 0.35
        for k in (-1, 0, 1):
            bx, by = x - dy * wdt * k, y + dx * wdt * k
            dark.append([(bx, by), ((bx + tipx) / 2, (by + tipy) / 2), (tipx, tipy)])
        bx, by = x + dy * wdt, y - dx * wdt
        lit.append([(bx, by), ((bx + tipx) / 2 + dy * 0.01, (by + tipy) / 2), (tipx, tipy)])
    return np.array(dark), np.array(lit)


CLUMP_DARK, CLUMP_LIT = _make_clumps(520, 3)


def _outline():
    pts = []
    for i, (cx, cy, rx, ry) in enumerate(BODY_ELL):
        for th in np.linspace(0, 2 * np.pi, 48, endpoint=False):
            x, y = cx + rx * math.cos(th), cy + ry * math.sin(th)
            others = min(((x - c2x) / r2x) ** 2 + ((y - c2y) / r2y) ** 2
                         for j, (c2x, c2y, r2x, r2y) in enumerate(BODY_ELL) if j != i)
            if others > 1.0:
                pts.append((x, y, math.cos(th), math.sin(th)))
    return pts


OUTLINE = _outline()

LEAF_ATTACH = [(0.18, -0.03, -62), (0.40, -0.05, -32), (0.60, -0.06, -76)]


class Pose:
    def __init__(self, x, y, s, lean=0.0, sx=1.0, sy=1.0):
        a = math.radians(lean)
        self.x, self.y, self.s, self.sx, self.sy = x, y, s, sx, sy
        self.ca, self.sa = math.cos(a), math.sin(a)

    def T(self, p):
        p = np.asarray(p, np.float64)
        shp = p.shape
        q = p.reshape(-1, 2)
        u, v = q[:, 0] * self.sx, q[:, 1] * self.sy
        out = np.stack([self.x + (u * self.ca - v * self.sa) * self.s, self.y + (u * self.sa + v * self.ca) * self.s], 1)
        return out.reshape(shp)

    def pt(self, u, v):
        return tuple(self.T([(u, v)])[0])


def aura(c, P, t, strength=1.0):
    """White fire burning around the beaver."""
    cx, cy = P.pt(0, -1.6)
    c.glow(cx, cy, 2.8 * P.s, AURA[1], 0.9 * strength, power=1.4)
    c.glow(cx, cy - 0.3 * P.s, 1.8 * P.s, WHITE, 0.6 * strength, power=1.2)
    for i, (x, y, nx, ny) in enumerate(OUTLINE[::2]):
        dx, dy = nx * 0.7, ny * 0.7 - 1.0
        fl = 0.35 + 0.3 * (0.5 + 0.5 * math.sin(t * 11 + i * 2.3)) + 0.15 * ((i * 7) % 3)
        bx, by = P.pt(x - nx * 0.05, y - ny * 0.05)
        ex, ey = P.pt(x + dx, y + dy)
        flame(c, bx, by, ex - bx, ey - by, fl * P.s, 0.17 * P.s, t, seed=i, palette=AURA, line=False,
              opacity=0.9 * strength, pressure=1.3)


def beaver(c, P, lift=0.0, tx=0.0, eaten=0.0, chew=0.0, singe=0.0, t=0.0, fine=None, twig=True, twitch=0.0,
           blink=0.0, look=0.0):
    s = P.s
    T = P.T
    if fine is None:
        fine = s * P.sy > 260
    # tail lying behind on the ground
    draw_tail(c, T, s)
    # hind feet come out from under the body, so they are drawn first and the fur falls over them
    for sgn in (-1, 1):
        draw_foot(c, T, s, sgn)
    # ears
    for sgn in (-1, 1):
        c.poly(T(ell(sgn * 0.64, -2.8, 0.1, 0.085, sgn * 25, 20)), fill=FUR[1], pressure=1.0)
        c.poly(T(ell(sgn * 0.64, -2.79, 0.05, 0.04, sgn * 25, 12)), fill=FUR[0], pressure=1.0, opacity=0.8)
    # body silhouette and shading
    for cx, cy, rx, ry in BODY_ELL:
        c.poly(T(ell(cx, cy, rx, ry, 0, 48)), fill=FUR_BASE, pressure=1.1, jit=1.0)
    parts = [T(ell(cx, cy, rx, ry, 0, 48)) for cx, cy, rx, ry in BODY_ELL]
    for (cx, cy, rx, ry) in BODY_ELL[:3]:
        c.poly(T(ell(cx - 0.22 * rx, cy - 0.22 * ry, 0.62 * rx, 0.6 * ry, 0, 36)), fill=FUR[3], pressure=0.7,
               opacity=0.55, jit=2)
        hl = np.array([[(cx + rx * (0.1 + 0.08 * i) - 0.4 * rx, cy - ry), (cx + rx * (0.1 + 0.08 * i), cy),
                        (cx + rx * (0.1 + 0.08 * i) + 0.4 * rx, cy + ry)] for i in range(12)])
        c.strokes(T(hl), FUR[0], 0.05, pressure=0.7, opacity=0.35, clip=parts)
    c.poly(T(ell(0, -1.98, 0.62, 0.12, 0, 30)), fill=FUR[0], pressure=0.7, opacity=0.35, jit=1)
    # fur strokes
    wmain = 0.024
    for k in range(6):
        c.strokes(T(FUR_MAIN[k]), FUR[k], wmain, pressure=0.95, boil=0.4)
    c.strokes(T(FUR_MAIN['edge_dark']), FUR[0], wmain, pressure=0.95, boil=0.4)
    c.strokes(T(FUR_MAIN['edge_lit']), FUR[3], wmain, pressure=0.95, boil=0.4)
    c.strokes(T(CLUMP_DARK), FUR[0], wmain * 0.8, pressure=0.9, boil=0.4, opacity=0.8)
    c.strokes(T(CLUMP_LIT), FUR[4], wmain * 0.7, pressure=0.9, boil=0.4, opacity=0.8)
    if fine:
        for k in range(6):
            c.strokes(T(FUR_FINE[k]), FUR[k], 0.009, pressure=0.95, boil=0.4)
    if singe > 0:
        sel = FUR_MAIN[0]
        for k in (1, 2, 3):
            a = FUR_MAIN[k]
            mid = a[:, 1, :]
            patch = ((mid[:, 1] < -2.62) | ((mid[:, 0] - 0.55) ** 2 + (mid[:, 1] + 1.45) ** 2 < 0.12)
                     | ((mid[:, 0] + 0.6) ** 2 + (mid[:, 1] + 0.7) ** 2 < 0.08))
            sel = np.concatenate([sel, a[patch]])
        c.strokes(T(sel), col(0.10, 0.08, 0.08), wmain * 1.2, pressure=0.9, opacity=0.8 * singe)
        rr = np.random.default_rng(55)
        curls = []
        for i in range(26):
            th = rr.uniform(-2.7, -0.45)
            x0, y0 = 0.78 * math.cos(th), -2.42 + 0.62 * math.sin(th)
            pts = [(x0 + 0.04 * j * math.cos(j * 1.9), y0 - 0.035 * j + 0.03 * math.sin(j * 1.9)) for j in range(5)]
            curls.append(pts)
        c.strokes(T(np.array(curls)), col(0.12, 0.09, 0.08), 0.014, pressure=0.9, opacity=singe)
    # face: muzzle, nose, mouth, teeth, eyes, whiskers
    nose = [(0.17 * math.cos(q) * (1 - 0.25 * max(0.0, math.sin(q))), -2.39 + 0.1 * math.sin(q) + 0.02 * math.cos(2 * q)) for q in np.linspace(0, 2 * np.pi, 28, endpoint=False)]

    def N(pts):  # a nose twitch lifts and widens the nose a little
        p = np.asarray(pts, np.float64)
        return T(np.stack([p[:, 0] * (1 + 0.1 * twitch), p[:, 1] - 0.035 * twitch], 1))
    c.poly(N(nose), fill=NOSE_C, line=col(0.07, 0.06, 0.06), lw=0.012 * s, pressure=1.1, jit=0.6)
    c.poly(N(ell(-0.05, -2.44, 0.07, 0.025, -8, 12)), fill=col(0.46, 0.45, 0.47), pressure=0.6, jit=0.4)
    for sgn in (-1, 1):
        c.line(N([(sgn * 0.03, -2.335), (sgn * 0.08, -2.355), (sgn * 0.12, -2.335), (sgn * 0.13, -2.31)]),
               col(0.02, 0.02, 0.02), lw=0.02 * s, jit=0.3)
    c.line(T([(0, -2.29), (0, -2.19)]), FUR[0], lw=0.012 * s, jit=0.3)
    c.line(T([(-0.13, -2.15), (-0.05, -2.18), (0, -2.19), (0.05, -2.18), (0.13, -2.15)]), FUR[0], lw=0.012 * s,
           jit=0.3)
    ch = 0.045 * chew
    c.poly(T(ell(0, -2.03 + ch, 0.08, 0.03 + ch * 0.5, 0, 14)), fill=col(0.12, 0.07, 0.06), pressure=1.1, jit=0.3)
    for x0, x1 in ((-0.058, -0.004), (0.004, 0.058)):
        tooth = [(x0, -2.18), (x1, -2.18), (x1, -2.07), (x1 - 0.012, -2.05), (x0 + 0.012, -2.05), (x0, -2.07)]
        c.poly(T(tooth), fill=INCISOR, line=INCISOR_D, lw=0.006 * s, pressure=1.1, jit=0.2)
        c.line(T([(x0 + 0.015, -2.17), (x0 + 0.015, -2.08)]), col(1.0, 0.72, 0.45), lw=0.01 * s, jit=0.1,
               opacity=0.7)
    c.strokes(T(np.array([[(-0.1 + 0.02 * i, -2.0), (-0.1 + 0.02 * i, -1.96), (-0.1 + 0.022 * i, -1.92)]
                          for i in range(11)])), FUR[5], 0.012, pressure=0.9, opacity=0.8)
    for sgn in (-1, 1):
        ex, ey = sgn * 0.40, -2.66
        c.poly(T(ell(ex, ey, 0.085, 0.07, 0, 16)), fill=FUR[0], pressure=1.0, opacity=0.8, jit=0.4)
        gy = -0.022 * look
        if look > 0.02:
            c.poly(T(ell(ex, ey + 0.022, 0.045, 0.03, 0, 16)), fill=col(0.72, 0.64, 0.56), pressure=1.1, jit=0.2)
        c.poly(T(ell(ex, ey + gy, 0.056, 0.05, 0, 16)), fill=col(0.03, 0.03, 0.03), pressure=1.2, jit=0.3)
        c.poly(T(ell(ex - 0.018, ey - 0.02 + gy, 0.013, 0.011, 0, 8)), fill=WHITE, pressure=1.2, jit=0.1)
        if blink > 0.02:
            r_ = 0.075
            cut = ey - r_ + 2 * r_ * blink
            th = np.linspace(np.pi, 2 * np.pi, 16)
            lid = [(ex + r_ * 1.15 * math.cos(q), ey + r_ * math.sin(q)) for q in th]
            lid += [(ex + r_ * 1.15, cut), (ex - r_ * 1.15, cut)]
            c.poly(T(lid), fill=FUR[2], pressure=1.2, jit=0.2)
            c.line(T([(ex - r_ * 1.05, cut), (ex, cut + 0.01 * blink), (ex + r_ * 1.05, cut)]), FUR[0],
                   lw=0.012 * s, jit=0.2)
        lift_w = 0.03 * twitch
        for k in range(5):
            y1 = -2.36 + k * 0.07 - lift_w
            c.line(T([(sgn * 0.18, -2.25 + k * 0.02), (sgn * 0.55, (y1 - 2.25) / 2 - 0.02),
                      (sgn * (0.92 + 0.04 * k), y1)]), col(0.10, 0.09, 0.09), lw=max(1.0, 0.007 * s),
                   pressure=0.8, jit=0.3, opacity=0.75)
    # arms, the twig with leaves, and the front paws holding it
    hx, hy = tx, -1.46 + lift
    arm_pts = []
    for sgn in (-1, 1):
        sxp, syp = sgn * 0.72, -1.86
        ex_, ey_ = hx + sgn * 0.17, hy + 0.02
        dx, dy = ex_ - sxp, ey_ - syp
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        arm = ell((sxp + ex_) / 2, (syp + ey_) / 2, L / 2 + 0.1, 0.19, math.degrees(math.atan2(dy, dx)), 30)
        c.poly(T(arm), fill=FUR_BASE, pressure=1.1, jit=1.0)
        arm_pts.append((sxp, syp, dx, dy, nx, ny, L, sgn))
    rr = np.random.default_rng(9)
    for (sxp, syp, dx, dy, nx, ny, L, sgn) in arm_pts:
        nst = 700 if fine else 260
        u = rr.uniform(-0.1, 1.05, nst)
        v = rr.uniform(-1, 1, nst) * np.sqrt(np.clip(1 - (2 * u - 1) ** 2 * 0.6, 0.05, 1))
        px, py = sxp + dx * u + nx * v * 0.17, syp + dy * u + ny * v * 0.17
        ang = math.atan2(dy, dx) * 0.5 + math.pi / 4 + rr.normal(0, 0.35, nst)
        ln = rr.uniform(0.05, 0.12, nst) * (0.6 if fine else 1.0)
        ux, uy = np.cos(ang) * ln, np.sin(ang) * ln
        st = np.stack([np.stack([px - ux * 0.4, py - uy * 0.4], 1), np.stack([px + ux * 0.1, py + uy * 0.1], 1),
                       np.stack([px + ux * 0.6, py + uy * 0.6], 1)], 1)
        tone = np.clip(((-v * sgn) + 1) * 2.0 + rr.normal(0, 0.8, len(v)), 0, 4).astype(int)
        for k in range(5):
            c.strokes(T(st[tone == k]), FUR[k], 0.012 if fine else wmain, pressure=0.95, boil=0.4)
    if twig:
        c.line(T([(hx - 0.45, hy + 0.03), (hx + 0.1, hy - 0.01), (hx + 0.72, hy - 0.07)]), TWIG, lw=0.035 * s,
               pressure=1.0, jit=0.5)
        for i, (ax, ay, ang) in enumerate(LEAF_ATTACH):
            frac = clamp01(i + 1 - eaten)
            if frac <= 0.02:
                continue
            a = math.radians(ang)
            ln, wd = 0.32 * frac, 0.11 * (0.4 + 0.6 * frac)
            bx, by = hx + ax, hy + ay
            ux, uy = math.cos(a), math.sin(a)
            nx, ny = -uy, ux
            left, right = [], []
            for q in np.linspace(0, 1, 10):
                w = wd * math.sin(math.pi * q) ** 0.8
                px, py = bx + ux * ln * q, by + uy * ln * q
                left.append((px + nx * w, py + ny * w))
                right.append((px - nx * w, py - ny * w))
            c.poly(T(left + right[::-1]), fill=LEAF, line=LEAF_D, lw=0.006 * s, pressure=1.0, jit=0.5)
            c.line(T([(bx, by), (bx + ux * ln * 0.9, by + uy * ln * 0.9)]), LEAF_D, lw=0.008 * s, jit=0.3)
    for sgn in (-1, 1):
        px, py = hx + sgn * 0.17, hy
        c.poly(T(ell(px, py + 0.01, 0.12, 0.09, 0, 16)), fill=SKIN, line=col(0.1, 0.09, 0.09), lw=0.01 * s,
               pressure=1.1, jit=0.4)
        for k in range(4):
            fx = px + sgn * (-0.08 + k * 0.05)
            c.poly(T(ell(fx, py - 0.005, 0.024, 0.055, 0, 12)), fill=SKIN, line=col(0.1, 0.09, 0.09),
                   lw=0.005 * s, pressure=1.1, jit=0.3)
            c.line(T([(fx, py + 0.04), (fx + 0.004, py + 0.075), (fx - 0.006, py + 0.095)]), CLAW, lw=0.011 * s,
                   jit=0.2)


# tail: a flat, scaly paddle (local units, lying behind the beaver to its right)
def _tail_geom():
    us = np.linspace(0, 1, 24)
    cx = 0.55 + 1.2 * us
    cy = -0.03 + 0.05 * us
    w = 0.12 + 0.16 * np.sin(np.pi * np.clip(us * 1.12, 0, 1)) ** 0.65
    top = np.stack([cx, cy - w * 0.55], 1)
    bot = np.stack([cx, cy + w * 0.45], 1)
    outline = np.concatenate([top, bot[::-1]])
    rr = np.random.default_rng(71)
    scales, ticks = [], []
    for row, u in enumerate(np.arange(0.12, 0.97, 0.055)):
        wu = 0.12 + 0.16 * math.sin(math.pi * min(1.0, u * 1.12)) ** 0.65
        x0, y0 = 0.55 + 1.2 * u, -0.03 + 0.05 * u
        n = max(2, int(wu * 2 / 0.05))
        for j in range(n):
            v = -1 + (j + 0.5 + 0.5 * (row % 2)) * 2 / n
            if abs(v) > 0.92:
                continue
            x = x0 + rr.uniform(-0.004, 0.004)
            y = y0 + v * wu * (0.55 if v < 0 else 0.45)
            hw, hh = 0.028, 0.02
            scales.append([(x - hw, y), (x, y - hh), (x + hw, y), (x, y + hh), (x - hw, y)])
            ticks.append([(x - hw * 0.6, y - hh * 0.35), (x - hw * 0.1, y - hh * 0.8), (x + hw * 0.3, y - hh * 0.55)])
    return outline, np.array(scales), np.array(ticks)


TAIL_OUTLINE, TAIL_SCALES, TAIL_TICKS = _tail_geom()


def draw_tail(c, T, s):
    out = T(TAIL_OUTLINE)
    c.poly(out, fill=TAIL_C, line=col(0.09, 0.08, 0.08), lw=0.018 * s, pressure=1.15, jit=0.6)
    c.poly(T(ell(1.2, -0.05, 0.42, 0.06, 2, 24)), fill=col(0.36, 0.34, 0.35), pressure=0.75, opacity=0.8, jit=0.5)
    c.poly(T(np.concatenate([TAIL_OUTLINE[24:], TAIL_OUTLINE[:1]])), None, col(0.12, 0.11, 0.11), lw=0.03 * s,
           opacity=0.6, closed=False)
    c.strokes(T(TAIL_SCALES), col(0.12, 0.11, 0.11), 0.007, pressure=1.0, boil=0.2, clip=[out])
    c.strokes(T(TAIL_TICKS), col(0.52, 0.5, 0.5), 0.006, pressure=0.9, boil=0.2, clip=[out], opacity=0.8)
    rr = np.random.default_rng(72)
    n = 120
    px, py = rr.uniform(0.5, 0.78, n), rr.uniform(-0.16, 0.06, n)
    ang = rr.normal(0.25, 0.3, n)
    ln = rr.uniform(0.06, 0.12, n)
    fur = np.stack([np.stack([px, py], 1), np.stack([px + np.cos(ang) * ln * 0.5, py + np.sin(ang) * ln * 0.5], 1),
                    np.stack([px + np.cos(ang) * ln, py + np.sin(ang) * ln], 1)], 1)
    tone = rr.integers(0, 3, n)
    for k in range(3):
        c.strokes(T(fur[tone == k]), FUR[k], 0.022, pressure=0.95, boil=0.3)


# hind feet: big, dark, webbed, with jointed toes and curved claws
FOOT_SKIN, FOOT_LIGHT, WEB = col(0.20, 0.17, 0.16), col(0.40, 0.36, 0.34), col(0.30, 0.26, 0.25)


def _foot_geom(sgn):
    heel = (sgn * 0.5, -0.1)
    toes = []
    for k in range(5):
        a = math.radians(90 + sgn * 14 - (k - 2) * 13)
        ln = [0.28, 0.34, 0.37, 0.35, 0.29][k]
        bx, by = heel[0] + (k - 2) * 0.065, heel[1] + 0.06 - abs(k - 2) * 0.012
        ux, uy = math.cos(a), math.sin(a) * 0.72  # foreshortened: the feet lie flat, pointing at us
        toes.append((bx, by, ux, uy, ln))
    return heel, toes


def draw_foot(c, T, s, sgn):
    heel, toes = _foot_geom(sgn)
    tips = [(bx + ux * ln, by + uy * ln) for bx, by, ux, uy, ln in toes]
    # webbing between the toes, with a scalloped edge
    web = [(heel[0] - 0.13, heel[1] + 0.05)]
    for i, (tx_, ty_) in enumerate(tips):
        bx, by, ux, uy, ln = toes[i]
        web.append((bx + ux * ln * 0.93, by + uy * ln * 0.93))
        if i < 4:
            nx_, ny_ = tips[i + 1]
            web.append(((tx_ + nx_) / 2, (ty_ + ny_) / 2 - 0.03))
    web.append((heel[0] + 0.13, heel[1] + 0.05))
    c.poly(T(web), fill=WEB, line=col(0.1, 0.09, 0.09), lw=0.008 * s, pressure=1.1, jit=0.4)
    c.strokes(T(np.array([[heel, ((heel[0] + t_[0]) / 2, (heel[1] + t_[1]) / 2 + 0.01), t_] for t_ in tips])),
              col(0.36, 0.32, 0.31), 0.006, pressure=0.8, opacity=0.5, boil=0.2)
    # the sole under the toes
    c.poly(T(ell(heel[0], heel[1] + 0.06, 0.24, 0.11, 0, 20)), fill=FOOT_SKIN, pressure=1.1, jit=0.4)
    for bx, by, ux, uy, ln in toes:
        nx_, ny_ = -uy, ux
        wd = 0.045
        pts = []
        for q in np.linspace(0, 1, 8):
            w = wd * (1 - 0.35 * q)
            pts.append((bx + ux * ln * q + nx_ * w, by + uy * ln * q + ny_ * w))
        for q in np.linspace(1, 0, 8):
            w = wd * (1 - 0.35 * q)
            pts.append((bx + ux * ln * q - nx_ * w, by + uy * ln * q - ny_ * w))
        c.poly(T(pts), fill=FOOT_SKIN, line=col(0.08, 0.07, 0.07), lw=0.006 * s, pressure=1.15, jit=0.3)
        # knuckle creases and a soft highlight
        for q in (0.35, 0.65):
            cx_, cy_ = bx + ux * ln * q, by + uy * ln * q
            c.line(T([(cx_ + nx_ * wd * 0.8, cy_ + ny_ * wd * 0.8), (cx_ + ux * 0.012, cy_ + uy * 0.012),
                      (cx_ - nx_ * wd * 0.8, cy_ - ny_ * wd * 0.8)]), col(0.07, 0.06, 0.06), lw=0.005 * s,
                   jit=0.2, opacity=0.8)
        c.line(T([(bx + ux * ln * 0.1 - nx_ * wd * 0.35, by + uy * ln * 0.1 - ny_ * wd * 0.35),
                  (bx + ux * ln * 0.85 - nx_ * wd * 0.3, by + uy * ln * 0.85 - ny_ * wd * 0.3)]), FOOT_LIGHT,
               lw=0.008 * s, jit=0.2, opacity=0.7)
        # curved claw
        tx_, ty_ = bx + ux * ln, by + uy * ln
        c.line(T([(tx_ - ux * 0.01, ty_ - uy * 0.01), (tx_ + ux * 0.035, ty_ + uy * 0.035 + 0.006),
                  (tx_ + ux * 0.05 - nx_ * 0.01, ty_ + uy * 0.05 + 0.02)]), CLAW, lw=0.012 * s, jit=0.2)
        c.line(T([(tx_ - ux * 0.008, ty_ - uy * 0.008), (tx_ + ux * 0.012, ty_ + uy * 0.012)]),
               col(0.35, 0.32, 0.3), lw=0.012 * s, jit=0.1)
    # fur spilling over the ankle
    rr = np.random.default_rng(80 + sgn)
    n = 90
    px = heel[0] + rr.uniform(-0.2, 0.2, n)
    py = heel[1] + rr.uniform(-0.08, 0.02, n)
    ang = math.pi / 2 + rr.normal(sgn * 0.3, 0.3, n)
    ln = rr.uniform(0.05, 0.1, n)
    fur = np.stack([np.stack([px, py], 1), np.stack([px + np.cos(ang) * ln * 0.5, py + np.sin(ang) * ln * 0.5], 1),
                    np.stack([px + np.cos(ang) * ln, py + np.sin(ang) * ln], 1)], 1)
    tone = rr.integers(0, 4, n)
    for k in range(4):
        c.strokes(T(fur[tone == k]), FUR[k], 0.02, pressure=0.95, boil=0.3)


def life(t):
    """Nose twitch (a quick double twitch) and blink amount at time t."""
    twitch = 0.0
    for t0 in TWITCHES:
        u = t - t0
        if 0 <= u < 0.34:
            twitch = [1.0, 0.2, 1.0, 0.3][min(3, int(u * FPS + 1e-6))]
    blink = 0.0
    for t0 in BLINKS:
        u = t - t0
        if 0 <= u < 0.25:
            blink = [0.6, 1.0, 0.45][min(2, int(u * FPS + 1e-6))]
    return twitch, blink


# ---------------------------------------------------------------------------
# Forest
# ---------------------------------------------------------------------------
_rf = np.random.default_rng(42)
FAR_TREES = [(x, _rf.uniform(170, 280)) for x in np.arange(-20, 1120, 78)]
RIPPLES = [(_rf.uniform(-40, 1040), _rf.uniform(1290, 1900), _rf.uniform(60, 180)) for _ in range(26)]
RIPPLES = [rp for rp in RIPPLES if not (1310 < rp[1] < 1500)]


def dam_top(x):
    return 1402 - 50 * math.sin(math.pi * clamp01((x - 40) / 1000))


DAM_STICKS = []
for _ in range(64):
    x = _rf.uniform(90, 990)
    y = _rf.uniform(dam_top(x) + 6, 1478)
    DAM_STICKS.append((x, y, _rf.uniform(60, 160), _rf.uniform(-22, 22), int(_rf.integers(0, 3)),
                       _rf.uniform(7, 11)))
FALL_STICKS = [(7.5, 250, 1392, 130, 12, 215, 1585), (10.0, 800, 1385, 120, -10, 845, 1600),
               (12.2, 390, 1372, 110, 6, 370, 1655), (14.0, 690, 1376, 100, 8, 715, 1700),
               (15.2, 150, 1398, 95, -6, 120, 1760)]
ROUND_TREES = [(165, 1235, 820, 185), (925, 1235, 850, 165)]
PINES = [(40, 1245, 760), (1050, 1245, 700), (330, 1230, 430), (745, 1230, 400)]

LEAVES = []
for i in range(70):
    tx, _, cy, cr = ROUND_TREES[i % 2]
    ang = _rf.uniform(0, 6.28)
    rr_ = cr * math.sqrt(_rf.uniform(0, 0.8))
    t0 = 4.2 + 11.6 * _rf.uniform(0, 1) ** 0.6
    LEAVES.append(dict(t0=t0, x=tx + rr_ * math.cos(ang), y=cy + rr_ * math.sin(ang), vy=_rf.uniform(160, 300),
                       sway=_rf.uniform(20, 45), ph=_rf.uniform(0, 6.3), land=_rf.uniform(1265, 1880),
                       c=[GREEN1, GREEN_L, GREEN2][i % 3]))
SPLASHES = sorted([(5.8 + 10.1 * _rf.uniform(0, 1) ** 0.55, _rf.uniform(60, 1020),
                    float(_rf.choice([_rf.uniform(1520, 1860), _rf.uniform(1265, 1320)])), i) for i in range(30)])
EMBERS = []
for i in range(46):
    t0 = 35.6 + i * 0.19 + _rf.uniform(0, 0.12)
    x1 = _rf.uniform(30, 1050)
    if 330 < x1 < 750:
        x1 += 420 if x1 > 540 else -300
    EMBERS.append(dict(t0=t0, x0=x1 + _rf.uniform(120, 260), x1=x1, y1=_rf.uniform(1150, 1880),
                       sp=_rf.uniform(1100, 1500), r=_rf.uniform(6, 11), seed=i))

BEAVER_X, BEAVER_Y, BEAVER_S = 540, 1384, 122


def pine(c, x, base, h, colr, pressure=0.85, lined=True):
    w = h * 0.42
    c.poly([(x - 9, base), (x + 9, base), (x + 7, base - h * 0.3), (x - 7, base - h * 0.3)], fill=TRUNK,
           line=BROWN_D if lined else None, lw=4)
    for k in range(4):
        top = base - h + k * h * 0.17
        bot = top + h * 0.36
        ww = w * (0.42 + 0.2 * k)
        pts = [(x, top)]
        for j in range(1, 6):
            f = j / 5
            pts.append((x + ww * f + (8 if j % 2 else -4), top + (bot - top) * f - (0 if j % 2 else 10)))
        for j in range(6):
            pts.append((x + ww - 2 * ww * j / 5, bot + (6 if j % 2 else -4)))
        for j in range(4, 0, -1):
            f = j / 5
            pts.append((x - ww * f - (8 if j % 2 else -4), top + (bot - top) * f - (0 if j % 2 else 10)))
        c.poly(pts, fill=colr, line=GREEN2 if lined else None, lw=4, pressure=pressure)


def round_tree(c, x, base, cy, r):
    c.poly([(x - 16, base), (x + 16, base), (x + 11, cy), (x - 11, cy)], fill=TRUNK, line=BROWN_D, lw=5)
    parts = [(0, 0, 1.0), (-0.55, 0.25, 0.65), (0.55, 0.3, 0.62)]
    for px, py, pr in parts:
        c.poly(blob(x + px * r, cy + py * r, pr * r, int(x + px * 100), 48, 0.3), None, GREEN2, lw=7)
    for px, py, pr in parts:
        c.poly(blob(x + px * r, cy + py * r, pr * r, int(x + px * 100), 48, 0.3), fill=GREEN1, pressure=0.95)
    c.hatch(blob(x + 0.3 * r, cy + 0.2 * r, 0.6 * r, 3), GREEN2, spacing=15, angle=55, lw=3, opacity=0.6)


def stick(c, x, y, ln, ang, ci, lw=9, opacity=1.0):
    a = math.radians(ang)
    dx, dy = math.cos(a) * ln / 2, math.sin(a) * ln / 2
    c.line([(x - dx, y - dy), (x + dx, y + dy)], BROWN_D, lw=lw + 4, jit=1, opacity=opacity)
    c.line([(x - dx, y - dy), (x + dx, y + dy)], STICKS[ci], lw=lw, jit=1, opacity=opacity)


def draw_leaf(c, x, y, ang, colr, sc=1.0):
    c.poly(ell(x, y, 16 * sc, 8 * sc, ang, 14), fill=colr, line=GREEN2, lw=3, jit=0.8)


def splash(c, x, y, age, big=1.0, seed=0):
    if age < 0 or age > 0.9:
        return
    r = np.random.default_rng(seed)
    fade = 1 - age / 0.9
    c.poly(ell(x, y, (40 + 260 * age) * big, (10 + 60 * age) * big, 0, 30), None, WATER_D, lw=5, opacity=fade)
    for i in range(8):
        vx, vy = r.uniform(-260, 260) * big, -r.uniform(300, 650) * big
        px, py = x + vx * age, y + vy * age + 0.5 * 1800 * age * age
        if py > y + 5:
            continue
        rr = r.uniform(7, 14) * big
        c.poly(ell(px, py, rr * 0.8, rr, 0, 12), fill=WATER, line=WATER_D, lw=3, jit=0.8, opacity=fade)


def puff(c, x, y, r, opacity=1.0, colr=PUFF, line=SMOKE, shaded=False):
    c.poly(ell(x, y, r, r * 0.9, 0, 28), fill=colr, line=line, lw=5, pressure=0.95, jit=r * 0.06, opacity=opacity)
    if shaded:
        c.poly(ell(x + r * 0.25, y + r * 0.3, r * 0.7, r * 0.5, 0, 20), fill=col(0.78, 0.77, 0.8), pressure=0.8,
               opacity=0.6 * opacity, jit=r * 0.05)
        c.poly(ell(x - r * 0.3, y - r * 0.3, r * 0.4, r * 0.3, 0, 16), fill=WHITE, pressure=1.0, opacity=opacity,
               jit=r * 0.04)


def forest(c, t, shake=0.0):
    r = np.random.default_rng(c.d * 13 + 1)
    c.cam = (1.0, float(r.normal() * shake), float(r.normal() * shake))
    c.fill_screen(SKY, 0.36)
    for x, h in FAR_TREES:
        pine(c, x, 1190, h, GREEN_F, pressure=0.55, lined=False)
    c.poly([(-60, 1135), (W + 60, 1135), (W + 60, 1300), (-60, 1300)], fill=GREEN_G, pressure=0.8)
    for x, base, h in PINES[2:]:
        pine(c, x, base, h, GREEN2)
    for tr in ROUND_TREES:
        round_tree(c, *tr)
    for x, base, h in PINES[:2]:
        pine(c, x, base, h, GREEN2)
    c.poly([(-60, 1250), (W + 60, 1250), (W + 60, H + 60), (-60, H + 60)], fill=WATER, pressure=0.62)
    c.line([(-60, 1252), (W + 60, 1252)], WATER_D, lw=5)
    for x, y, ln in RIPPLES:
        c.line([(x, y), (x + ln, y + 3)], WATER_D, lw=4, pressure=0.7)
    for i, (tf, x, y, ln, ang, lx, ly) in enumerate(FALL_STICKS):
        if t >= tf:
            u = clamp01((t - tf) / 0.4)
            if u < 1:
                stick(c, lerp(x, lx, u), lerp(y, ly, u * u), ln, ang + 180 * u, i % 3)
            else:
                drift = (t - tf - 0.4) * 12
                stick(c, lx + drift, ly + 5 * math.sin(t * 3 + i), ln, ang + 180, i % 3)
                c.poly(ell(lx + drift, ly + 12, ln * 0.6, 10, 0, 20), None, WATER_D, lw=3, opacity=0.6)
    xs = np.linspace(40, 1040, 26)
    top = [(x, dam_top(x) + 8 * math.sin(x * 0.05)) for x in xs]
    bot = [(x, 1482 + 6 * math.sin(x * 0.09)) for x in xs[::-1]]
    c.poly(top + bot, fill=MUD, line=BROWN_D, lw=6, pressure=0.9)
    for (x, y, ln, ang, ci, lw) in DAM_STICKS:
        stick(c, x, y, ln, ang, ci, lw)
    for (tf, x, y, ln, ang, lx, ly) in FALL_STICKS:
        if t < tf:
            wob = math.sin(t * 40) * 3 * clamp01((t - tf + 1.2) / 1.2) if t > tf - 1.2 else 0
            stick(c, x + wob, y, ln, ang + wob, 0)
    c.line(top, BROWN_D, lw=5)
    for i, ft in enumerate(FALL_STICKS):
        splash(c, ft[5], ft[6], t - ft[0] - 0.4, 0.8, seed=50 + i)


def light_overlay(c, p):
    if p <= 0:
        return
    cam = c.cam
    c.cam = (1.0, 0.0, 0.0)
    for k, (x, sw) in enumerate(((150, 1), (420, -1), (700, 1), (960, -1))):
        wob = 30 * math.sin(c.d * 0.1 + k)
        top = [(x - 70 + wob, -20), (x + 70 + wob, -20)]
        bot = [(x + 230 * sw + 180, H + 20), (x + 230 * sw - 180, H + 20)]
        c.poly(top + bot, fill=LIGHT, pressure=0.6, opacity=0.35 * p, jit=6)
    c.vgrad(LIGHT, 0.8 * p, 0.14 * p, 0, H)
    c.cam = cam


DAM_LINE = 1400  # things further back than this are behind the dam and the beaver


def falling_leaves(c, t, behind=None):
    for lf in LEAVES:
        if behind is not None and (lf['land'] < DAM_LINE) != behind:
            continue
        if t < lf['t0']:
            continue
        dt = t - lf['t0']
        y = min(lf['y'] + lf['vy'] * dt, lf['land'])
        x = lf['x'] + lf['sway'] * math.sin(lf['ph'] + 3 * min(dt, (lf['land'] - lf['y']) / lf['vy']))
        draw_leaf(c, x, y, 40 * math.sin(lf['ph'] + 4 * dt), lf['c'])


def ember(c, x, y, dx, dy, r, t, seed):
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    c.line([(x - ux * r * 3, y - uy * r * 3), (x - ux * r * 16, y - uy * r * 16)], col(0.55, 0.53, 0.52), lw=r * 1.2,
           pressure=0.6, opacity=0.5)
    c.glow(x, y, r * 4, FIRE_O, 0.35)
    flame(c, x - ux * r * 0.3, y - uy * r * 0.3, -ux, -uy, r * 6.5, r * 1.25, t, seed=seed, opacity=0.95)
    c.poly(blob(x, y, r * 1.15, seed, 12, 0.3), fill=col(0.25, 0.12, 0.09), line=FIRE_O, lw=4)


# ---------------------------------------------------------------------------
# Sky, clouds, Earth, asteroid
# ---------------------------------------------------------------------------
_rc = np.random.default_rng(12)
HORIZON = 1130
CLOUD_SEA = []
for row in range(13):
    f = row / 12
    y = HORIZON + 20 + f ** 1.7 * 860
    rad = 22 + f ** 1.5 * 190
    x = -rad * 1.5 + _rc.uniform(0, rad)
    while x < W + rad * 2:
        CLOUD_SEA.append((x, y + _rc.uniform(-rad * 0.12, rad * 0.12), rad * _rc.uniform(0.8, 1.2), len(CLOUD_SEA)))
        x += rad * _rc.uniform(2.2, 3.2)
WISPS = [(_rc.uniform(-100, W), _rc.uniform(250, HORIZON - 120), _rc.uniform(60, 220)) for _ in range(45)]
C_SHADOW, C_MID, C_LIT, C_HI = col(0.55, 0.47, 0.58), col(0.86, 0.66, 0.58), col(1.0, 0.84, 0.62), col(1.0, 0.95, 0.84)
SUN = (905, HORIZON + 5)


def bank(x, y, rx, ry, seed, n=40):
    """A cloud shape: lumpy on top, flatter underneath."""
    rr = np.random.default_rng(seed)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    lump = np.zeros(n)
    for k in range(3, 9):
        lump += rr.uniform(0.05, 0.16) / (k / 3) * np.abs(np.sin(k * th / 2 + rr.uniform(0, 6.3)))
    top = np.sin(th) < 0
    rad = 1 + np.where(top, lump, 0.02 * lump)
    return np.stack([x + rx * rad * np.cos(th), y + ry * rad * np.sin(th) * np.where(top, 1.0, 0.45)], 1)


def cloud_puff(c, x, y, r, seed, opacity=1.0):
    rx, ry = r * 1.9, r * 0.75
    c.poly(bank(x, y, rx, ry, seed), fill=C_SHADOW, pressure=1.1, jit=r * 0.02, opacity=opacity)
    c.poly(bank(x + 0.1 * rx, y - 0.25 * ry, rx * 0.85, ry * 0.75, seed + 1), fill=C_MID, pressure=1.05,
           jit=r * 0.02, opacity=opacity)
    c.poly(bank(x + 0.2 * rx, y - 0.5 * ry, rx * 0.55, ry * 0.45, seed + 2), fill=C_LIT, pressure=1.0,
           jit=r * 0.02, opacity=opacity)
    c.poly(bank(x + 0.28 * rx, y - 0.62 * ry, rx * 0.25, ry * 0.22, seed + 3), fill=C_HI, pressure=1.0,
           jit=r * 0.015, opacity=opacity)


def scene_clouds(c, t):
    u = t - T_CLOUDS
    c.fill_screen(col(0.12, 0.17, 0.33), 1.5)
    c.vgrad(col(0.36, 0.45, 0.62), 0.0, 0.9, 150, HORIZON - 250)
    c.vgrad(col(0.99, 0.80, 0.56), 0.0, 0.95, HORIZON - 380, HORIZON + 10)
    for x, y, ln in WISPS:
        f = (y - 250) / (HORIZON - 250)
        colr = col(0.95, 0.72, 0.62) * f + col(0.62, 0.62, 0.78) * (1 - f)
        c.line([(x, y), (x + ln, y + 2)], colr, lw=3 + 5 * f, pressure=0.8, opacity=0.6)
    c.glow(SUN[0], SUN[1], 700, col(1.0, 0.82, 0.5), 0.7, power=1.6)
    c.glow(SUN[0], SUN[1], 170, WHITE, 1.0, power=1.3)
    c.poly(ell(SUN[0], SUN[1], 420, 7, 0, 30), fill=WHITE, pressure=1.0, opacity=0.6, jit=1)
    # the rocket: a brown spot on a pillar of flame
    rx = 430
    ry = HORIZON + 140 - 1000 * clamp01(u / 3.7) ** 0.85
    emerge = T_CLOUDS + 0.25
    for (x, y, rad, seed) in CLOUD_SEA[:len(CLOUD_SEA) // 3]:
        cloud_puff(c, x, y, rad, seed)
    if u > 0.1:
        ys = np.linspace(HORIZON + 60, ry + 14, 40)
        tp = T_CLOUDS + 3.7 * np.clip((HORIZON + 140 - ys) / 1000, 0, 1) ** (1 / 0.85)
        age = np.clip(t - tp, 0, None)
        wd = 6 + 30 * age ** 0.6
        xc = rx + 22 * age + 4 * np.sin(ys * 0.03)
        lump = 1 + 0.12 * np.sin(ys * 0.11 + 1.3) + 0.08 * np.sin(ys * 0.27)
        left = np.stack([xc - wd * lump, ys], 1)
        right = np.stack([xc + wd * lump, ys], 1)
        c.poly(np.concatenate([left, right[::-1]]), fill=C_SHADOW, pressure=1.1, jit=1.5)
        c.poly(np.concatenate([np.stack([xc - wd * 0.1, ys], 1), right[::-1]]), fill=C_MID, pressure=1.05, jit=1.5)
        c.poly(np.concatenate([np.stack([xc + wd * 0.45, ys], 1), np.stack([xc + wd * 0.9 * lump, ys], 1)[::-1]]),
               fill=C_LIT, pressure=1.0, jit=1)
    for (x, y, rad, seed) in CLOUD_SEA[len(CLOUD_SEA) // 3:]:
        cloud_puff(c, x, y, rad, seed)
    if u < 0.1:
        c.glow(rx, HORIZON + 120, 180, col(1.0, 0.9, 0.7), 0.5 * (u / 0.1))
    if t >= emerge:
        g = min(1.0, (t - emerge) * 4)
        for j in range(4):
            a = (j + 0.5) / 4 * math.pi
            cloud_puff(c, rx + math.cos(a) * 70 * g, HORIZON + 75 - math.sin(a) * 20 * g, 22 + 26 * g, 900 + j)
        c.glow(rx, ry + 30, 110, col(1.0, 0.92, 0.72), 0.9)
        flame(c, rx, ry + 6, 0, 1, 70, 11, t, palette=(col(1.0, 0.72, 0.35), col(1.0, 0.9, 0.65), WHITE), line=False)
        c.poly(ell(rx, ry, 7, 10, 0, 12), fill=col(0.36, 0.22, 0.12), line=col(0.18, 0.11, 0.07), lw=2, pressure=1.1,
               jit=0.4)


CUMULUS = [(150, 250, 150, 1), (930, -300, 190, 2), (60, -900, 170, 4), (1010, -1300, 160, 6),
           (220, -1900, 200, 7), (900, -2300, 150, 8)]
BIG_CLOUD = (540, 10, 360, 11)   # the one the beaver punches through
CU_SHADOW, CU_MID, CU_LIT = col(0.66, 0.72, 0.84), col(0.88, 0.91, 0.96), col(1.0, 1.0, 1.0)


def _bumps(seed):
    rr = np.random.default_rng(seed)
    out = [(0.0, -0.35, 0.62)]
    for k in range(7):
        a = math.pi * (0.1 + 0.8 * k / 6)
        out.append((0.95 * math.cos(a) * -1, -0.1 - 0.55 * math.sin(a) + rr.uniform(-0.08, 0.08),
                    rr.uniform(0.36, 0.52)))
    out += [(-0.9, 0.12, 0.38), (0.9, 0.14, 0.4), (-0.35, 0.2, 0.45), (0.4, 0.22, 0.45)]
    return out


def cumulus(c, x, y, r, seed, opacity=1.0):
    """A puffy fair-weather cloud: a dome of bumps, flat underneath, lit from the upper left."""
    b = _bumps(seed)
    base = [(x - 1.25 * r, y + 0.3 * r), (x + 1.25 * r, y + 0.3 * r), (x + 1.1 * r, y + 0.45 * r),
            (x - 1.1 * r, y + 0.45 * r)]
    for bx, by, br in b:
        c.poly(ell(x + bx * r, y + by * r, br * r, br * r, 0, 26), None, col(0.58, 0.64, 0.78), lw=6, jit=2,
               opacity=opacity)
    c.poly(base, fill=CU_SHADOW, pressure=1.1, jit=2, opacity=opacity)
    for bx, by, br in b:
        c.poly(ell(x + bx * r, y + by * r, br * r, br * r, 0, 26), fill=CU_SHADOW, pressure=1.1, jit=2,
               opacity=opacity)
    for bx, by, br in b:
        c.poly(ell(x + (bx - 0.08) * r, y + (by - 0.1) * r, br * r * 0.8, br * r * 0.75, 0, 22), fill=CU_MID,
               pressure=1.1, jit=2, opacity=opacity)
    for bx, by, br in b:
        if by < 0.05:
            c.poly(ell(x + (bx - 0.14) * r, y + (by - 0.18) * r, br * r * 0.45, br * r * 0.4, 0, 18), fill=CU_LIT,
                   pressure=1.1, jit=1.5, opacity=opacity)


def scene_mid(c, t):
    """Middle distance: the beaver punches up through ordinary white clouds."""
    u = t - T_MID
    c.fill_screen(col(0.40, 0.60, 0.88), 1.4)
    c.vgrad(col(0.74, 0.85, 0.97), 0.0, 0.85, 0, H)
    speed = 1400
    by = lerp(1450, 1050, u / 2.0)
    P = Pose(540, by, 46)
    for (x, y0, r, seed) in CUMULUS:
        cumulus(c, x, y0 + speed * u, r, seed)
    bx0, by0, br, bseed = BIG_CLOUD
    cy = by0 + speed * u
    ys = np.linspace(by + 20, H + 60, 30)
    wd = 10 + (ys - by) * 0.045
    xc = 540 + 5 * np.sin(ys * 0.03)
    left, right = np.stack([xc - wd, ys], 1), np.stack([xc + wd, ys], 1)
    c.poly(np.concatenate([left, right[::-1]]), fill=col(0.95, 0.96, 0.98), line=col(0.72, 0.76, 0.85), lw=4,
           pressure=1.1, jit=1.5)
    c.glow(540, by + 25, 90, col(1.0, 0.9, 0.7), 0.8)
    flame(c, 540, by + 3, 0, 1, 110, 18, t, palette=(FIRE_O, FIRE_Y, WHITE))
    beaver(c, P, lift=-0.22, t=t)
    cumulus(c, bx0, cy, br, bseed)
    top = cy - 0.95 * br
    if by < top + 40 and top < H - 150:
        # torn vapour where the beaver burst out of the top, dragged upwards behind it
        g = clamp01((top - by) / 300)
        for j in range(4):
            f = j / 4
            cumulus(c, 540 + 14 * math.sin(j * 2.1), top + 30 - (top - by - 60) * f * g, (70 - 12 * j) * (0.6 + 0.4 * g),
                    50 + j)


EARTH = (540.0, 2150.0, 1000.0)
LIMB_TOP = 1150.0
SUNRISE = (330.0, 1168.0)


def space_cam(t):
    k = sstep(T_REVEAL, T_FACE - 0.4, t)
    z = 0.34 ** k
    qy = lerp(LIMB_TOP, 1400.0, k)
    return z, 540 - 540 * z, qy - LIMB_TOP * z


def earth_limb(c):
    cx, cy, R = EARTH
    c.poly(ell(cx, cy, R, R, 0, 220), fill=NIGHT, pressure=1.4, jit=1.5)
    rr = np.random.default_rng(31)
    for i in range(10):
        a, rho = rr.uniform(0, 6.28), rr.uniform(0.1, 0.75)
        c.poly(blob(cx + R * rho * math.cos(a), cy + R * rho * math.sin(a), R * rr.uniform(0.12, 0.25), 60 + i, 30,
                    0.3), fill=col(0.12, 0.17, 0.26), pressure=0.9, opacity=0.8, jit=2)
    for i in range(30):
        a, rho = rr.uniform(0, 6.28), rr.uniform(0.2, 0.95)
        pts = [(cx + R * rho * math.cos(q), cy + R * rho * math.sin(q)) for q in np.linspace(a, a + 0.25, 10)]
        c.line(pts, col(0.3, 0.36, 0.48), lw=rr.uniform(6, 18), pressure=0.6, opacity=0.4)
    for i in range(22):
        a = rr.uniform(-2.35, -0.8)
        rho = rr.uniform(0.8, 0.985)
        x, y = cx + R * rho * math.cos(a), cy + R * rho * math.sin(a)
        near = max(0.0, 1 - math.hypot(x - SUNRISE[0], y - SUNRISE[1]) / 700)
        colr = col(0.55, 0.62, 0.72) * (0.35 + 0.65 * near)
        pts = [(cx + R * rho * math.cos(q), cy + R * rho * math.sin(q)) for q in np.linspace(a, a + 0.12, 8)]
        c.line(pts, colr, lw=rr.uniform(6, 16) * (1 - (1 - rho) * 3), pressure=0.7, opacity=0.5)
    c.glow(SUNRISE[0], SUNRISE[1] + 120, 600, col(0.45, 0.32, 0.18), 0.55, power=1.4)
    for w, a, colr in ((60, 0.18, col(0.25, 0.55, 1.0)), (26, 0.45, col(0.35, 0.7, 1.0)),
                       (9, 0.95, col(0.55, 0.85, 1.0)), (3, 0.9, col(0.9, 0.97, 1.0))):
        c.poly(ell(cx, cy, R + w * 0.25, R + w * 0.25, 0, 220), None, colr, lw=w, lp=0.95, opacity=a, jit=0.8)


def sunrise(c, t):
    x, y = SUNRISE
    c.glow(x, y, 900, col(1.0, 0.62, 0.22), 0.55, power=1.8)
    c.glow(x, y, 300, col(1.0, 0.85, 0.55), 0.9, power=1.5)
    c.glow(x, y, 90, WHITE, 1.0, power=1.2)
    for k in range(14):
        a = -math.pi + k / 13 * math.pi + 0.05 * math.sin(k * 3.1)
        ln = 380 + 220 * ((k * 5) % 3)
        w = 7 + 4 * (k % 2)
        c.poly([(x + math.cos(a + 0.5 * math.pi) * w, y + math.sin(a + 0.5 * math.pi) * w),
                (x + math.cos(a) * ln, y + math.sin(a) * ln),
                (x - math.cos(a + 0.5 * math.pi) * w, y - math.sin(a + 0.5 * math.pi) * w)],
               fill=col(1.0, 0.8, 0.45), pressure=0.8, opacity=0.35, jit=1)
    c.poly(ell(x + 60, y - 4, 520, 9, -3, 30), fill=WHITE, pressure=1.0, opacity=0.55, jit=1)


def light_streak(c, hx, hy, length, width, t, dx=0.0, dy=1.0, opacity=1.0):
    """The beaver as seen from far away: a white-hot point with a burning trail."""
    flame(c, hx, hy, dx, dy, length, width, t, palette=STREAK, line=False, opacity=0.9 * opacity, wobble=0.3)
    rr = np.random.default_rng(c.d // 2)
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    for i in range(7):
        off = rr.uniform(-1, 1) * width * 0.9
        ln = length * rr.uniform(0.3, 0.9)
        c.line([(hx - uy * off, hy + ux * off), (hx - uy * off * 1.6 + ux * ln, hy + ux * off * 1.6 + uy * ln)],
               STREAK[1], lw=max(1.5, width * 0.12), pressure=0.9, opacity=0.6 * opacity)
    c.glow(hx, hy, width * 7, col(0.85, 0.92, 1.0), 0.9 * opacity)
    c.glow(hx, hy, width * 2.5, WHITE, 1.0 * opacity)
    c.line([(hx - width * 5, hy), (hx + width * 5, hy)], WHITE, lw=max(1.5, width * 0.2), opacity=0.8 * opacity)
    c.line([(hx, hy - width * 5), (hx, hy + width * 3)], WHITE, lw=max(1.5, width * 0.2), opacity=0.8 * opacity)


# asteroid (unit coordinates, scaled when drawn)
_ra = np.random.default_rng(77)
AST_H = [(k, _ra.uniform(-0.28, 0.28) / k ** 0.9, _ra.uniform(0, 6.3)) for k in range(2, 11)]


def ast_rad(th):
    r = np.ones_like(th)
    for k, a, ph in AST_H:
        r = r + a * np.cos(k * th + ph)
    return r


def ast_outline(n=96):
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    rr = ast_rad(th)
    return np.stack([rr * np.cos(th), rr * np.sin(th)], 1)


def _ast_strokes(n, seed):
    r = np.random.default_rng(seed)
    th = r.uniform(0, 2 * np.pi, n)
    rho = np.sqrt(r.uniform(0, 1, n)) * ast_rad(th) * 0.98
    x, y = rho * np.cos(th), rho * np.sin(th)
    ang = th + np.pi / 2 + r.normal(0, 0.5, n)
    L = r.uniform(0.04, 0.1, n)
    dx, dy = np.cos(ang) * L, np.sin(ang) * L
    st = np.stack([np.stack([x - dx, y - dy], 1), np.stack([x, y + 0.004], 1), np.stack([x + dx, y + dy], 1)], 1)
    rel = rho / ast_rad(th)
    hot = np.clip((y - 0.3) / 0.7, 0, 1) * rel ** 2
    lit = np.clip(-(x * 0.6 + y * 0.2), -1, 1)
    tone = np.where(hot > 0.62, 5, np.where(hot > 0.38, 4, np.where(lit > 0.25, 2, np.where(lit > -0.2, 1, 0))))
    tone = np.where((r.random(n) < 0.15) & (tone < 3), 3, tone)
    return {k: st[tone == k] for k in range(6)}


AST_TONES = [col(0.13, 0.11, 0.11), col(0.27, 0.24, 0.23), col(0.42, 0.38, 0.35), col(0.34, 0.24, 0.20),
             col(0.62, 0.26, 0.10), col(0.95, 0.52, 0.16)]
AST_STROKES = _ast_strokes(3200, 5)
CRATERS = [(_ra.uniform(-0.6, 0.6), _ra.uniform(-0.6, 0.35), _ra.uniform(0.06, 0.16)) for _ in range(9)]
CRACKS = []
for i in range(11):
    a0 = i * 0.57 + _ra.uniform(-0.2, 0.2)
    pts, rr_, a = [(0.0, 0.0)], 0.0, a0
    while rr_ < 1.05:
        rr_ += _ra.uniform(0.08, 0.16)
        a += _ra.uniform(-0.35, 0.35)
        pts.append((rr_ * math.cos(a), rr_ * math.sin(a)))
    CRACKS.append(pts)
FRAGS = []
for i in range(420):
    ang = _ra.uniform(0, 6.28)
    rho = math.sqrt(_ra.uniform(0, 1))
    FRAGS.append(dict(a=ang, rho=rho, sp=_ra.uniform(600, 2600), sz=_ra.uniform(4, 40) * (1.3 - rho * 0.5),
                      hot=_ra.random() < 0.35, seed=i))


def asteroid(c, cx, cy, r, t, cracks=0.0, hole=0.0, flames=True):
    c.glow(cx, cy - 0.3 * r, r * 2.6, col(0.95, 0.45, 0.12), 0.5)
    if flames:
        for k in range(15):
            th = math.radians(-178 + k * 12.5)
            rim = ast_rad(np.array([th]))[0]
            bx, by = cx + 0.85 * r * rim * math.cos(th), cy + 0.85 * r * rim * math.sin(th)
            dx, dy = 0.5 * math.cos(th), -1.0
            ln = r * (1.2 + 0.9 * ((k * 7) % 5) / 4) * (1 + 0.1 * math.sin(t * 13 + k))
            flame(c, bx, by, dx, dy, ln, r * 0.26, t, seed=k)
        for k in range(8):
            yk = cy - r * (1.3 + k * 0.35) - (t * 300 % (r * 0.35))
            c.poly(blob(cx + r * 0.5 * math.sin(k * 1.7), yk, r * (0.25 + 0.04 * k), 400 + k, 16, 0.25),
                   fill=col(0.25, 0.2, 0.2), pressure=0.7, opacity=0.35, jit=2)
    out = ast_outline() * r + np.array([cx, cy])
    c.poly(out, fill=AST_TONES[1], line=col(0.08, 0.07, 0.07), lw=max(3, r * 0.012), pressure=1.15)
    sc = np.array([r, r])
    off = np.array([cx, cy])
    for k in range(6):
        c.strokes(AST_STROKES[k] * sc + off, AST_TONES[k], 0.012 * r, pressure=0.95, boil=0.3)
    for (x, y, sz) in CRATERS:
        px, py = cx + x * r, cy + y * r
        c.poly(ell(px, py, sz * r, sz * r * 0.8, 0, 22), fill=AST_TONES[0], pressure=0.9, opacity=0.85, jit=1)
        arc = [(px + sz * r * math.cos(q), py + sz * r * 0.8 * math.sin(q)) for q in np.linspace(0.2, 2.6, 10)]
        c.line(arc, AST_TONES[2], lw=max(2, sz * r * 0.18), opacity=0.8)
    lower = out[out[:, 1] > cy + 0.1 * r]
    lower = lower[np.argsort(lower[:, 0])]
    if len(lower) > 2:
        c.line(lower, FIRE_R, lw=max(10, r * 0.07), opacity=0.8)
        c.line(lower, FIRE_O, lw=max(6, r * 0.04), opacity=0.9)
        c.line(lower, col(1.0, 0.95, 0.75), lw=max(3, r * 0.015), opacity=0.9)
        c.glow(cx, cy + 0.9 * r, r * 1.1, col(1.0, 0.6, 0.2), 0.45)
    if hole > 0:
        c.glow(cx, cy + r * 0.92, r * 0.5 * hole, WHITE, 0.95)
    if cracks > 0:
        for pts_c in CRACKS:
            n = max(2, int(len(pts_c) * cracks + 0.5))
            seg = [(cx + x * r * 0.95, cy + y * r * 0.95) for x, y in pts_c[:n]]
            c.line(seg, FIRE_O, lw=max(6, r * 0.028), opacity=1.0)
            c.line(seg, col(1.0, 0.97, 0.85), lw=max(3, r * 0.01), opacity=1.0)
        c.glow(cx, cy, r * 1.3, col(1.0, 0.85, 0.55), 0.5 * cracks)


# ---------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------
def scene_threat(c, t):
    p = clamp01((t - T_THREAT) / (T_LAUNCH - T_THREAT))
    forest(c, t, shake=26 * p ** 2.2)
    light_overlay(c, p ** 1.6)
    lift = -0.22 * sstep(0.6, 2.6, t)
    tw, bl = life(t)
    look = max(sstep(a, a + 0.1, t) * (1 - sstep(b, b + 0.12, t)) for a, b in LOOKS)
    falling_leaves(c, t, behind=True)
    for (ts, x, y, i) in SPLASHES:
        if y < DAM_LINE:
            splash(c, x, y, t - ts, 0.9, seed=i)
    beaver(c, Pose(BEAVER_X, BEAVER_Y, BEAVER_S), lift=lift, t=t, twitch=tw, blink=bl, look=look)
    falling_leaves(c, t, behind=False)
    for (ts, x, y, i) in SPLASHES:
        if y >= DAM_LINE:
            splash(c, x, y, t - ts, 0.9, seed=i)
    c.wash(LIGHT, 0.16 * p ** 1.6, textured=True)


def scene_launch(c, t):
    u = t - T_LAUNCH
    forest(c, t, shake=30 * max(0.0, 1 - u / 0.7))
    light_overlay(c, 1.0)
    by = BEAVER_Y - 250 - 9000 * u
    ytop = max(by + 40, -300)
    ys = np.linspace(1340, ytop, 40)
    age = np.clip(t - (T_LAUNCH + np.clip(BEAVER_Y - 250 - ys, 0, None) / 9000), 0, None)
    wd = 34 + 170 * age ** 0.8
    lump = 1 + 0.1 * np.sin(ys * 0.035 + 0.7) + 0.06 * np.sin(ys * 0.09)
    xc = 540 + 6 * np.sin(ys * 0.02)
    left, right = np.stack([xc - wd * lump, ys], 1), np.stack([xc + wd * lump, ys], 1)
    c.poly(np.concatenate([left, right[::-1]]), fill=col(0.82, 0.81, 0.84), line=col(0.66, 0.65, 0.7), lw=5,
           pressure=1.05, jit=2)
    c.poly(np.concatenate([left + [wd[:, None].mean() * 0.15, 0], np.stack([xc + wd * 0.2, ys], 1)[::-1]]),
           fill=PUFF, pressure=1.0, jit=2)
    for k in range(6):
        sgn = -1 if k % 2 else 1
        dist = (80 + 440 * min(1.0, u * 2.2)) * (0.5 + 0.25 * (k // 2))
        puff(c, 540 + sgn * dist, 1352 - 20 * (k // 2), 60 + 130 * u, shaded=True, line=col(0.7, 0.69, 0.72))
    splash(c, 330, 1520, u, 1.8, seed=91)
    splash(c, 760, 1530, u, 1.8, seed=92)
    if by > -500:
        c.glow(540, by + 40, 220, col(1.0, 0.95, 0.8), 0.9)
        flame(c, 540, by + 5, 0, 1, 300, 60, t, palette=(FIRE_O, FIRE_Y, WHITE))
        for g in (2, 1):
            c.line([(540 + (g - 1.5) * 90, by - 380 + 120 * g), (540 + (g - 1.5) * 90, by + 250 * g)],
                   col(0.95, 0.9, 0.8), lw=10, pressure=0.8, opacity=0.5)
        beaver(c, Pose(540, by, BEAVER_S), lift=-0.22, t=t)
    for lf in LEAVES:
        dt = t - lf['t0']
        y = min(lf['y'] + lf['vy'] * max(0.0, dt), lf['land']) if dt > 0 else lf['y']
        x = lf['x'] + (lf['x'] - 540) * u * 1.5
        draw_leaf(c, x, y - 200 * u, 200 * u + lf['ph'] * 30, lf['c'])
    c.wash(LIGHT, 0.16, textured=True)


def scene_space(c, t):
    c.fill_screen(DEEP, 1.3)
    stars(c, 160, seed=5, dim=0.8)
    z, ox, oy = space_cam(t)
    c.cam = (z, ox, oy)
    ay = lerp(-1950, -1700, clamp01((t - T_REVEAL) / (T_FACE - T_REVEAL)))
    asteroid(c, 540, ay, 860, t)
    earth_limb(c)
    sunrise(c, t)
    k = clamp01((t - T_SPACE - 0.3) / (T_FACE - T_SPACE - 0.3))
    hy = LIMB_TOP - 40 - 620 * k ** 0.8
    if t > T_SPACE + 0.3:
        tail = (LIMB_TOP - 20) - hy
        light_streak(c, 548, hy, max(30.0, tail), 9, t)
    c.cam = (1.0, 0.0, 0.0)
    c.vgrad(col(0.7, 0.25, 0.08), 0.28 * sstep(T_REVEAL + 1.0, T_FACE, t), 0.0, 0, H * 0.45)


def scene_face(c, t):
    c.fill_screen(DEEP, 1.3)
    stars(c, 45, seed=8, streak=0.6, dim=0.6)
    c.vgrad(col(0.55, 0.18, 0.06), 0.3, 0.0, 0, H * 0.3)
    P = Pose(540, 2330, 560)
    aura(c, P, t)
    u = t - FACE_BLINK
    blink = [0.5, 1.0, 1.0, 0.5][min(3, int(u * FPS + 1e-6))] if 0 <= u < 4 / FPS else 0.0
    beaver(c, P, lift=-0.22, t=t, blink=blink)
    c.glow(540, 1150, 900, AURA[1], 0.12)


AST_C, AST_R = (540.0, 760.0), 610.0


def scene_impact(c, t):
    c.fill_screen(DEEP, 1.3)
    stars(c, 110, seed=6)
    hit = T_IMPACT + 0.6
    asteroid(c, AST_C[0], AST_C[1], AST_R, t, hole=sstep(hit, hit + 0.12, t))
    entry = AST_C[1] + AST_R * 0.93
    if t < hit:
        u = (t - T_IMPACT) / 0.6
        hy = lerp(2150, entry, u ** 1.5)
        light_streak(c, 540, hy, 700, 14, t)
    else:
        u = clamp01((t - hit) / 0.3)
        c.glow(540, entry, 150 + 350 * u, WHITE, 1.0)
        r = np.random.default_rng(5)
        for i in range(26):
            q = r.uniform(0.15, math.pi - 0.15)
            d = (60 + 560 * u) * r.uniform(0.4, 1.2)
            c.poly(blob(540 + d * math.cos(q), entry + d * math.sin(q), r.uniform(8, 28), i, 9, 0.35),
                   fill=AST_TONES[int(r.integers(0, 3))], line=FIRE_O if i % 3 == 0 else col(0.08, 0.07, 0.07), lw=3)


def scene_inside(c, t):
    u = t - T_INSIDE
    c.fill_screen(col(0.17, 0.14, 0.13), 1.2)
    r = np.random.default_rng(3)
    lines = []
    for i in range(420):
        x = r.uniform(-50, W + 50)
        y = (r.uniform(0, H + 400) + 5200 * u) % (H + 400) - 200
        ln = r.uniform(60, 260)
        lines.append([(x, y), (x + r.uniform(-8, 8), y + ln * 0.5), (x, y + ln)])
    lines = np.array(lines)
    tone = r.integers(0, 4, len(lines))
    for k in range(3):
        c.strokes(lines[tone == k], AST_TONES[k], 7, pressure=0.95, boil=0.5)
    c.strokes(lines[tone == 3], AST_TONES[4], 5, pressure=0.95, boil=0.5, opacity=0.7)
    P = Pose(540, 1500, 170)
    cx, cy = P.pt(0, -1.6)
    for k in range(10):
        q = k / 10 * 2 * math.pi + 0.2
        c.line([(cx + 260 * math.cos(q), cy + 260 * math.sin(q)),
                (cx + 1000 * math.cos(q + 0.12), cy + 1000 * math.sin(q + 0.12))], FIRE_O, lw=10, opacity=0.8)
    aura(c, P, t)
    beaver(c, P, lift=-0.22, t=t)
    for i in range(30):
        q = r.uniform(0, 2 * math.pi)
        t0 = r.uniform(0, 0.8)
        f = ((u - t0) % 0.8) / 0.8
        d = 220 + 1300 * f
        x, y = cx + d * math.cos(q), cy + d * math.sin(q) + 700 * f
        c.poly(blob(x, y, r.uniform(20, 80) * (0.5 + f), i, 10, 0.35), fill=AST_TONES[i % 3],
               line=FIRE_O if i % 4 == 0 else col(0.06, 0.05, 0.05), lw=5)


def scene_burst(c, t):
    c.fill_screen(DEEP, 1.3)
    stars(c, 110, seed=6)
    cx, cy = AST_C
    if t < T_EXPLODE:
        asteroid(c, cx, cy, AST_R, t, cracks=sstep(T_BURST, T_EXPLODE - 0.05, t), hole=1.0)
        out_t = T_BURST + 0.35
        if t >= out_t:
            u = clamp01((t - out_t) / 0.2)
            top = cy - AST_R * 0.9
            c.glow(cx, top, 260, WHITE, 1.0)
            light_streak(c, cx, top - 1300 * u, 1300 * u + 10, 16, t)
            r = np.random.default_rng(4)
            for i in range(16):
                q = r.uniform(-math.pi * 0.9, -math.pi * 0.1)
                d = 40 + 420 * u * r.uniform(0.4, 1.0)
                c.poly(blob(cx + d * math.cos(q), top + d * math.sin(q), r.uniform(6, 22), i, 8, 0.3),
                       fill=AST_TONES[i % 3], line=FIRE_O, lw=3)
    else:
        u = t - T_EXPLODE
        for f in FRAGS:
            d = f['rho'] * AST_R + f['sp'] * u
            x, y = cx + d * math.cos(f['a']), cy + d * math.sin(f['a'])
            if -60 < x < W + 60 and -60 < y < H + 60:
                c.poly(blob(x, y, f['sz'], f['seed'], 7, 0.35),
                       fill=AST_TONES[5 if f['hot'] else f['seed'] % 3],
                       line=FIRE_O if f['hot'] else (col(0.06, 0.05, 0.05) if f['sz'] > 16 else None), lw=3, jit=1)
        c.glow(cx, cy, 250 + 5200 * u ** 1.2, WHITE, 1.4, power=1.2)
        c.wash(WHITE, sstep(T_WHITE - 0.2, T_WHITE, t))


BITES = [37.8, 38.6, 39.6, 40.4, 41.4, 42.2]


def scene_home(c, t):
    la = t - T_LAND
    shake = 12 * max(0.0, 1 - la / 0.25) if la >= 0 else 0.0
    forest(c, t, shake=shake)
    for lf in LEAVES:
        x = lf['x'] + lf['sway'] * math.sin(lf['ph'] + 3 * (lf['land'] - lf['y']) / lf['vy'])
        draw_leaf(c, x, lf['land'], 40 * math.sin(lf['ph']), lf['c'])
    for e in EMBERS:
        dur = (e['y1'] + 80) / e['sp']
        u = (t - e['t0']) / dur
        if u < 0:
            continue
        if u < 1:
            x, y = lerp(e['x0'], e['x1'], u), lerp(-80, e['y1'], u)
            ember(c, x, y, e['x1'] - e['x0'], e['y1'] + 80, e['r'], t, e['seed'])
        else:
            age = t - e['t0'] - dur
            c.glow(e['x1'], e['y1'], e['r'] * 3, FIRE_O, 0.3)
            c.poly(blob(e['x1'], e['y1'], e['r'] * 0.8, e['seed'], 10, 0.3), fill=col(0.25, 0.1, 0.08),
                   line=FIRE_O, lw=3)
            if age < 0.35:
                puff(c, e['x1'], e['y1'] - 10, 14 + 60 * age, opacity=1 - age / 0.35)
            smoke_wisp(c, e['x1'], e['y1'] - 12, t, e['seed'], length=6, opacity=0.45, lw=4)
    y = BEAVER_Y
    lift, tx, eaten, chew = 0.0, 0.0, 0.0, 0.0
    if t < T_LAND:
        u = clamp01((t - T_DROP) / (T_LAND - T_DROP))
        y = lerp(-600, BEAVER_Y, u * u)
    if 0 <= la < 0.45:
        splash(c, 330, 1520, la, 1.2, seed=93)
        splash(c, 760, 1530, la, 1.2, seed=94)
        for k in range(4):
            sgn = -1 if k % 2 else 1
            puff(c, 540 + sgn * (110 + 380 * la) * (1 + k // 2 * 0.3), 1388, 40 + 50 * la, opacity=1 - la / 0.45,
                 colr=col(0.85, 0.8, 0.72))
    if t >= T_CHEW:
        k = sstep(T_CHEW, T_CHEW + 0.5, t)
        eaten = 0.5 * sum(1 for b in BITES if t >= b)
        cur = min(2, int(eaten))
        target_tx = -(LEAF_ATTACH[cur][0] + 0.06)
        prev_tx = -(LEAF_ATTACH[max(0, cur - 1)][0] + 0.06)
        swap = BITES[cur * 2 - 1] if cur > 0 else T_CHEW
        tx = lerp(prev_tx, target_tx, sstep(swap, swap + 0.3, t)) * k
        lift = -0.49 * k
        if t > T_CHEW + 0.5:
            chew = max(0.0, math.sin(2 * math.pi * 3.0 * (t - T_CHEW - 0.5)))
    if t >= T_DROP:
        P = Pose(BEAVER_X, y, BEAVER_S)
        tw, bl = life(t) if t >= T_LAND else (0.0, 0.0)
        beaver(c, P, lift=lift, tx=tx, eaten=eaten, chew=chew, singe=1.0, t=t, twitch=tw, blink=bl)
        if la >= 0:
            for k, (u_, v_) in enumerate(((-0.45, -2.95), (0.35, -3.0), (0.85, -1.9), (-0.9, -1.2))):
                px, py = P.pt(u_, v_)
                smoke_wisp(c, px, py, t, k * 2.1, length=12, opacity=0.7)
    hx, hy = Pose(BEAVER_X, BEAVER_Y, BEAVER_S).pt(0.15, -3.0)
    t_fall, t_hit = 42.5, 42.95
    if t_fall <= t < t_hit:
        u = (t - t_fall) / (t_hit - t_fall)
        ember(c, lerp(760, hx, u), lerp(-80, hy - 8, u), hx - 760, hy + 80, 11, t, 99)
    elif t >= t_hit:
        c.glow(hx, hy - 8, 40, FIRE_O, 0.6)
        c.poly(blob(hx, hy - 8, 11, 99, 10, 0.3), fill=col(0.3, 0.12, 0.09), line=FIRE_O, lw=4)
        smoke_wisp(c, hx, hy - 20, t, 7.0, length=10, opacity=0.7, lw=5)
    c.wash(WHITE, 1 - sstep(T_HOME, T_HOME + 0.5, t))


def render(d):
    t = d / FPS
    c = Canvas(d)
    if t < T_LAUNCH:
        scene_threat(c, t)
    elif t < T_MID:
        scene_launch(c, t)
    elif t < T_CLOUDS:
        scene_mid(c, t)
    elif t < T_SPACE:
        scene_clouds(c, t)
    elif t < T_FACE:
        scene_space(c, t)
    elif t < T_IMPACT:
        scene_face(c, t)
    elif t < T_INSIDE:
        scene_impact(c, t)
    elif t < T_BURST:
        scene_inside(c, t)
    elif t < T_WHITE:
        scene_burst(c, t)
    elif t < T_HOME:
        c.wash(WHITE, 1.0)
    else:
        scene_home(c, t)
    return c.result()


# ---------------------------------------------------------------------------
# Sound: kept realistic and understated
# ---------------------------------------------------------------------------
def make_audio(path):
    tr = Track(DUR)
    add = tr.add
    # forest air, and birds that fall silent as the rumble grows
    for a, b in ((0.0, T_LAUNCH), (T_HOME, DUR)):
        add(a, 0.02 * noise(b - a, 400, 3000, int(a)) * np.clip(tt(b - a) / 0.4, 0, 1))
    for tb in (0.4, 0.62, 1.5, 2.3, 2.5, 3.6, 43.6, 43.8):
        add(tb, 0.06 * sweep(0.07, 3000, 4300) * np.hanning(int(0.07 * 44100)))
    # the rumble: something enormous is coming. Deep bass for big speakers, a growl phones can play,
    # distant thunder-like cracks and groaning wood, all pushed into gentle overdrive at the peak.
    d = T_LAUNCH - T_THREAT
    x = tt(d)
    env = (x / d) ** 2.0
    throb = 0.75 + 0.25 * np.sin(2 * np.pi * 0.6 * x) * np.sin(2 * np.pi * 2.7 * x)
    drone = sum(np.sin(2 * np.pi * f * x + ph) for f, ph in ((33, 0), (41, 1.1), (49.5, 2.3), (66, 0.4)))
    rumble = (0.9 * noise(d, 18, 90, 1) + 0.6 * noise(d, 70, 260, 2) * throb + 0.18 * drone
              + 0.25 * sweep(d, 40, 62) + 0.2 * noise(d, 250, 700, 21) * throb)
    rg = np.random.default_rng(3)
    for tc in np.sort(rg.uniform(3.0, d, 26)):
        if rg.random() < tc / d:
            i = int(tc * 44100)
            crack = 1.2 * noise(1.2, 60, 900, int(tc * 77)) * decay(1.2, 0.35)
            rumble[i:i + len(crack)] += crack[:len(rumble) - i]
    for tg in (3.5, 5.8, 7.4, 8.8, 10.4, 11.6):
        i = int(tg * 44100)
        groan = 0.5 * noise(1.5, 140, 420, int(tg * 31)) * np.sin(np.pi * tt(1.5) / 1.5) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt(1.5)))
        rumble[i:i + len(groan)] += groan[:len(rumble) - i]
    rumble = rumble * env
    add(T_THREAT, 0.95 * np.tanh(1.8 * rumble) / np.tanh(1.8))
    for ts, _, _, i in SPLASHES:
        add(ts, 0.08 * noise(0.2, 300, 2000, 100 + i) * decay(0.2, 0.06))
    for ft in FALL_STICKS:
        add(ft[0] + 0.4, 0.2 * noise(0.3, 200, 2500, int(ft[0] * 10)) * decay(0.3, 0.08))
    # launch: a blast and a roar that carries into the wide shot
    add(T_LAUNCH, 0.9 * noise(1.5, 25, 3000, 4) * decay(1.5, 0.4) + 0.6 * np.sin(2 * np.pi * 50 * tt(1.5)) * decay(1.5, 0.6))
    d = T_SPACE - T_LAUNCH
    x = tt(d)
    env = np.clip(x / 0.1, 0, 1) * np.clip((d - x) / 1.5, 0, 1) * np.where(x < 0.8, 1.0, 0.45)
    add(T_LAUNCH, (0.35 * noise(d, 60, 400, 5) + 0.15 * noise(d, 400, 2000, 6)) * env)
    add(T_MID + 0.8, 0.3 * noise(0.9, 400, 5000, 25) * np.hanning(int(0.9 * 44100)))
    # space: near silence, then a deep threat as the asteroid appears
    d = T_FACE - T_SPACE
    add(T_SPACE, 0.03 * np.sin(2 * np.pi * 45 * tt(d)) * np.clip(tt(d) / 1.0, 0, 1))
    d = T_FACE - T_REVEAL
    x = tt(d)
    add(T_REVEAL, (0.6 * noise(d, 18, 90, 8) + 0.12 * sweep(d, 70, 55) + 0.35 * noise(d, 80, 320, 26) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.8 * x))) * (x / d) ** 1.6)
    tr.silence(T_FACE, T_IMPACT)
    # impact and shattering rock
    hit = T_IMPACT + 0.6
    add(hit, 1.0 * noise(1.2, 30, 3500, 10) * decay(1.2, 0.35) + 0.5 * np.sin(2 * np.pi * 42 * tt(1.2)) * decay(1.2, 0.5))
    r = np.random.default_rng(11)
    tk = T_INSIDE
    while tk < T_BURST + 0.4:
        add(tk, r.uniform(0.25, 0.55) * noise(0.12, 60, 2000, int(tk * 1000)) * decay(0.12, 0.04))
        tk += r.uniform(0.03, 0.08)
    add(T_INSIDE, 0.4 * noise(T_BURST - T_INSIDE + 0.5, 25, 160, 12))
    # the explosion: a split second of silence, a sharp crack, then a huge overdriven boom that
    # drops in pitch, a hail of debris and a long rolling rumble that carries through the white
    tr.silence(T_EXPLODE - 0.12, T_EXPLODE)
    d = 5.0
    x = tt(d)
    boom = (1.4 * noise(d, 18, 240, 14) * decay(d, 1.4)
            + 1.0 * sweep(d, 95, 26) * decay(d, 1.1)
            + 1.0 * noise(d, 240, 2500, 15) * decay(d, 0.5)
            + 0.9 * noise(d, 120, 600, 27) * decay(d, 0.9)
            + 0.9 * noise(d, 60, 180, 22) * decay(d, 2.2) * (0.7 + 0.3 * np.sin(2 * np.pi * 1.3 * x)))
    boom[:int(0.08 * 44100)] += 1.6 * noise(0.08, 300, 9000, 23) * decay(0.08, 0.02)
    rg = np.random.default_rng(24)
    for tk in rg.uniform(0.15, 3.5, 70):
        i = int(tk * 44100)
        bit = rg.uniform(0.15, 0.5) * np.exp(-tk / 1.5) * noise(0.06, 400, 6000, int(tk * 1000)) * decay(0.06, 0.02)
        boom[i:i + len(bit)] += bit
    add(T_EXPLODE, 1.3 * np.tanh(3.0 * boom) / np.tanh(3.0))
    # home: a single dull thud, then small sounds
    add(T_LAND, 0.9 * np.sin(2 * np.pi * np.cumsum(np.linspace(75, 45, int(0.35 * 44100))) / 44100) * decay(0.35, 0.12))
    add(T_LAND, 0.4 * noise(0.3, 40, 500, 16) * decay(0.3, 0.08))
    add(T_LAND, 0.12 * noise(0.5, 500, 4000, 17) * decay(0.5, 0.2))
    add(T_LAND, 0.035 * noise(DUR - T_LAND, 3000, 9000, 18) * np.exp(-tt(DUR - T_LAND) / 4.0))
    for e in EMBERS:
        tl = e['t0'] + (e['y1'] + 80) / e['sp']
        add(tl, 0.05 * noise(0.3, 1500, 7000, e['seed'] + 200) * decay(0.3, 0.12))
    for b in BITES:
        add(b, 0.3 * noise(0.07, 1200, 6000, int(b * 100)) * decay(0.07, 0.02))
    tk = T_CHEW + 0.5 + 0.25 / 3
    while tk < DUR:
        if all(abs(tk - b) > 0.12 for b in BITES):
            add(tk, 0.1 * noise(0.05, 1000, 5000, int(tk * 100)) * decay(0.05, 0.015))
        tk += 1 / 3
    add(42.95, 0.18 * noise(0.1, 100, 900, 19) * decay(0.1, 0.03))
    add(42.95, 0.05 * noise(1.0, 3000, 9000, 20) * decay(1.0, 0.4))
    tr.save(path)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for ts in sys.argv[3:]:
            Image.fromarray(render(int(round(float(ts) * FPS)))).save(os.path.join(out, f'still_{float(ts):05.2f}s.png'))
            print('saved', ts)
    elif mode == 'render':
        render_video(sys.argv[2], render, int(DUR * FPS), make_audio, crf=int(sys.argv[3]) if len(sys.argv) > 3 else 27)
