#!/usr/bin/env python3
"""Beaver vs Asteroid: a 20 second coloured-pencil animation.

Usage:
    python3 beaver_asteroid.py stills OUT_DIR T1 T2 ...   # save single frames at given seconds
    python3 beaver_asteroid.py render OUT.mp4             # render the full video with sound
"""
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
FPS = 12
DUR = 20.0
M = 120  # margin so the pencil grain can be shifted each drawing
NG = 3   # number of pencil grain directions


# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
def col(r, g, b):
    return np.array([r, g, b], np.float32)


PAPER = col(0.97, 0.95, 0.90)
WHITE = col(1.0, 1.0, 1.0)
BROWN = col(0.58, 0.37, 0.21)
BROWN_D = col(0.33, 0.19, 0.10)
TAN = col(0.88, 0.72, 0.52)
TEETH = col(0.99, 0.84, 0.50)
NOSE = col(0.18, 0.11, 0.10)
INK = col(0.12, 0.10, 0.10)
PINK = col(0.96, 0.58, 0.60)
MOUTH = col(0.40, 0.12, 0.14)
SKY = col(0.78, 0.89, 0.97)
GREEN_F = col(0.50, 0.66, 0.55)
GREEN_G = col(0.55, 0.72, 0.38)
GREEN1 = col(0.42, 0.66, 0.32)
GREEN2 = col(0.24, 0.47, 0.26)
GREEN_L = col(0.62, 0.80, 0.34)
TRUNK = col(0.50, 0.33, 0.20)
WATER = col(0.48, 0.70, 0.88)
WATER_D = col(0.25, 0.47, 0.74)
MUD = col(0.47, 0.31, 0.18)
STICKS = [col(0.55, 0.38, 0.22), col(0.40, 0.25, 0.14), col(0.66, 0.48, 0.30)]
FIRE_Y = col(1.0, 0.88, 0.30)
FIRE_O = col(0.99, 0.56, 0.14)
FIRE_R = col(0.86, 0.22, 0.10)
SPACE = col(0.09, 0.11, 0.24)
ROCK = col(0.50, 0.44, 0.41)
ROCK_D = col(0.29, 0.25, 0.25)
ROCK_B = col(0.45, 0.32, 0.26)
SMOKE = col(0.62, 0.62, 0.64)
PUFF = col(0.96, 0.96, 0.97)
SOOT = col(0.16, 0.14, 0.14)
OCEAN = col(0.26, 0.47, 0.80)
OCEAN_D = col(0.14, 0.28, 0.58)
ATMOS = col(0.62, 0.82, 1.0)
DESERT = col(0.80, 0.68, 0.42)
LIGHT = col(1.0, 0.95, 0.72)


# ---------------------------------------------------------------------------
# Paper and pencil grain (made once)
# ---------------------------------------------------------------------------
def _uniform(a, rng):
    s = rng.choice(a.ravel(), 200000)
    q = np.quantile(s, np.linspace(0, 1, 257))
    return np.interp(a, q, np.linspace(0, 1, 257)).astype(np.float32)


def _make_grain(angle, seed):
    r = np.random.default_rng(seed)
    gh, gw = H + 2 * M, W + 2 * M
    big = int(math.hypot(gw, gh)) + 8
    small = r.random((big // 3, big // 12)).astype(np.float32)
    im = Image.fromarray((small * 255).astype(np.uint8)).resize((big, big), Image.BILINEAR)
    im = im.rotate(angle, resample=Image.BILINEAR)
    a = np.asarray(im, np.float32) / 255
    y0, x0 = (big - gh) // 2, (big - gw) // 2
    a = a[y0:y0 + gh, x0:x0 + gw]
    return _uniform(a, r)


_r0 = np.random.default_rng(7)
GRAIN = [_make_grain(a, 11 + i) for i, a in enumerate((32, -38, 78))]
_tooth = Image.fromarray((_r0.random((H, W)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.8))
TOOTH = _uniform(np.asarray(_tooth, np.float32), _r0)
_mottle = np.asarray(Image.fromarray((_r0.random((H // 80, W // 80)) * 255).astype(np.uint8))
                     .resize((W, H), Image.BICUBIC), np.float32) / 255
PAPER_IMG = (PAPER[None, None, :] * (1 - 0.05 * (TOOTH - 0.5) - 0.035 * (_mottle - 0.5))[..., None]).astype(np.float32)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def clamp01(x):
    return max(0.0, min(1.0, x))


def sstep(a, b, x):
    t = clamp01((x - a) / (b - a))
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def ell(cx, cy, rx, ry, rot=0.0, n=40):
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x, y = rx * np.cos(th), ry * np.sin(th)
    if rot:
        a = math.radians(rot)
        ca, sa = math.cos(a), math.sin(a)
        x, y = x * ca - y * sa, x * sa + y * ca
    return np.stack([cx + x, cy + y], 1)


def blob(cx, cy, r, seed, n=36, amt=0.18):
    rr = np.random.default_rng(seed)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    rad = np.ones(n)
    for k in range(2, 6):
        rad += rr.uniform(-amt, amt) / k * 2 * np.cos(k * th + rr.uniform(0, 6.3))
    return np.stack([cx + r * rad * np.cos(th), cy + r * rad * np.sin(th)], 1)


# ---------------------------------------------------------------------------
# Canvas: draws shapes that look like coloured pencil
# ---------------------------------------------------------------------------
class Canvas:
    def __init__(self, d):
        self.d = d
        self.n = 0
        self.img = PAPER_IMG.copy()
        self.cam = (1.0, 0.0, 0.0)
        r = np.random.default_rng(1000 + d // 4)  # pencil texture shifts 3 times a second
        self.goff = [(int(r.integers(0, 2 * M)), int(r.integers(0, 2 * M))) for _ in range(NG)]

    def rng(self):
        self.n += 1
        return np.random.default_rng(((self.d // 2) * 7919 + self.n * 104729) % (2 ** 32))  # lines wobble 6 times a second

    def scr(self, pts):
        s, ox, oy = self.cam
        return np.asarray(pts, np.float64) * s + np.array([ox, oy])

    @staticmethod
    def jitter(p, amp, r):
        n = len(p)
        if n < 2 or amp <= 0:
            return p
        k = max(4, n // 5)
        ctrl = r.normal(0, amp, (k, 2))
        idx = np.linspace(0, k, n, endpoint=False)
        i0 = np.floor(idx).astype(int) % k
        i1 = (i0 + 1) % k
        f = (idx - np.floor(idx))[:, None]
        f = f * f * (3 - 2 * f)
        return p + ctrl[i0] * (1 - f) + ctrl[i1] * f

    def _box(self, p, pad):
        x0 = int(max(0, math.floor(p[:, 0].min()) - pad))
        x1 = int(min(W, math.ceil(p[:, 0].max()) + pad))
        y0 = int(max(0, math.floor(p[:, 1].min()) - pad))
        y1 = int(min(H, math.ceil(p[:, 1].max()) + pad))
        if x1 - x0 < 1 or y1 - y0 < 1:
            return None
        return x0, y0, x1, y1

    def _mask(self, p, width=0, closed=True):
        b = self._box(p, width + 3)
        if b is None:
            return None
        x0, y0, x1, y1 = b
        im = Image.new('L', (x1 - x0, y1 - y0), 0)
        dr = ImageDraw.Draw(im)
        q = [(float(x - x0), float(y - y0)) for x, y in p]
        if width == 0:
            if len(q) >= 3:
                dr.polygon(q, fill=255)
        else:
            if closed:
                q = q + [q[0]]
            dr.line(q, fill=255, width=int(width), joint='curve')
            r = width / 2
            for (x, y) in (q[0], q[-1]):
                dr.ellipse((x - r, y - r, x + r, y + r), fill=255)
        return np.asarray(im, np.float32) / 255, x0, y0

    def _apply(self, m, x0, y0, color, pressure, opacity, gi):
        h, w = m.shape
        ox, oy = self.goff[gi]
        g = GRAIN[gi][oy + y0:oy + y0 + h, ox + x0:ox + x0 + w]
        t = TOOTH[y0:y0 + h, x0:x0 + w]
        cov = np.clip((0.78 * g + 0.22 * t - (1 - pressure)) * 3.2, 0, 1)
        a = (m * cov * opacity)[..., None]
        reg = self.img[y0:y0 + h, x0:x0 + w]
        reg += (color - reg) * a

    def poly(self, pts, fill=None, line=None, lw=5, pressure=0.85, lp=0.95,
             jit=2.2, opacity=1.0, closed=True, grain=None):
        if opacity <= 0.003:
            return
        r = self.rng()
        p = self.jitter(self.scr(pts), jit, r)
        gi = int(r.integers(0, NG)) if grain is None else grain
        if fill is not None and closed:
            res = self._mask(p)
            if res is not None:
                self._apply(*res, fill, pressure, opacity, gi)
        if line is not None:
            w = max(1.5, lw * self.cam[0])
            res = self._mask(p, width=int(round(w)), closed=closed)
            if res is not None:
                self._apply(*res, line, lp, opacity, (gi + 1) % NG)

    def line(self, pts, color, lw=5, pressure=0.9, jit=1.5, opacity=1.0):
        self.poly(pts, None, color, lw=lw, lp=pressure, jit=jit, opacity=opacity, closed=False)

    def hatch(self, pts, color, spacing=16, angle=45, lw=3, pressure=0.8, opacity=1.0):
        r = self.rng()
        p = self.jitter(self.scr(pts), 2.0, r)
        res = self._mask(p)
        if res is None:
            return
        m, x0, y0 = res
        h, w = m.shape
        im = Image.new('L', (w, h), 0)
        dr = ImageDraw.Draw(im)
        a = math.radians(angle)
        dx, dy = math.cos(a), math.sin(a)
        nx, ny = -dy, dx
        L = w + h
        sp = max(5.0, spacing * self.cam[0])
        cx, cy = w / 2, h / 2
        for off in np.arange(-L, L, sp):
            o = off + r.normal(0, sp * 0.12)
            px, py = cx + nx * o, cy + ny * o
            dr.line([(px - dx * L, py - dy * L), (px + dx * L, py + dy * L)], fill=255,
                    width=max(1, int(round(lw * max(0.5, self.cam[0])))))
        lm = np.asarray(im, np.float32) / 255
        self._apply(m * lm, x0, y0, color, pressure, opacity, int(r.integers(0, NG)))

    def fill_screen(self, color, pressure=0.9, opacity=1.0):
        gi = int(self.rng().integers(0, NG))
        self._apply(np.ones((H, W), np.float32), 0, 0, color, pressure, opacity, gi)

    def _blend(self, a, x0, y0, color, textured=True):
        h, w = a.shape
        if textured:
            ox, oy = self.goff[0]
            a = a * (0.7 + 0.3 * GRAIN[0][oy + y0:oy + y0 + h, ox + x0:ox + x0 + w])
        reg = self.img[y0:y0 + h, x0:x0 + w]
        reg += (color - reg) * a[..., None]

    def glow(self, cx, cy, rad, color, strength, power=2.0):
        s, ox, oy = self.cam
        X, Y, R = cx * s + ox, cy * s + oy, rad * s
        b = self._box(np.array([[X - R, Y - R], [X + R, Y + R]]), 0)
        if b is None or strength <= 0:
            return
        x0, y0, x1, y1 = b
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        dd = np.sqrt((xx - X) ** 2 + (yy - Y) ** 2) / R
        a = np.clip(1 - dd, 0, 1) ** power * strength
        self._blend(np.clip(a, 0, 1).astype(np.float32), x0, y0, color)

    def vgrad(self, color, a_top, a_bot, y_top=0, y_bot=H):
        y = np.arange(H, dtype=np.float32)
        f = np.clip((y - y_top) / max(1, (y_bot - y_top)), 0, 1)
        a = (a_top + (a_bot - a_top) * f)[:, None] * np.ones((1, W), np.float32)
        self._blend(np.clip(a, 0, 1).astype(np.float32), 0, 0, color)

    def wash(self, color, alpha, textured=False):
        if alpha <= 0:
            return
        self._blend(np.full((H, W), min(1.0, alpha), np.float32), 0, 0, color, textured)

    def result(self):
        return (np.clip(self.img, 0, 1) * 255 + 0.5).astype(np.uint8)


# ---------------------------------------------------------------------------
# The beaver
# ---------------------------------------------------------------------------
def beaver_point(x, y, s, lean, sx, sy, u, v):
    a = math.radians(lean)
    u, v = u * sx, v * sy
    return (x + (u * math.cos(a) - v * math.sin(a)) * s,
            y + (u * math.sin(a) + v * math.cos(a)) * s)


def beaver(c, x, y, s, lean=0.0, sx=1.0, sy=1.0, mouth=0.0, singe=0.0, tufts=0.0, t=0.0):
    a = math.radians(lean)
    ca, sa = math.cos(a), math.sin(a)

    def T(p):
        p = np.asarray(p, np.float64)
        u, v = p[:, 0] * sx, p[:, 1] * sy
        return np.stack([x + (u * ca - v * sa) * s, y + (u * sa + v * ca) * s], 1)

    def E(cx, cy, rx, ry, rot=0.0, n=40):
        return T(ell(cx, cy, rx, ry, rot, n))

    L = 0.045 * s
    fur = dict(fill=BROWN, line=BROWN_D, lw=L, pressure=1.0)

    # fur tufts blown about (drawn behind so they poke out)
    if tufts > 0:
        spots = [(0, -2.15, 0.98, 0.86, th) for th in (-165, -140, -115, -65, -40, -15, 10, 170)] + \
                [(0, -1.05, 1.05, 1.02, th) for th in (-20, 5, 30, 150, 175, 200)]
        for k, (ecx, ecy, erx, ery, th) in enumerate(spots):
            tr = math.radians(th)
            bx, by = ecx + erx * math.cos(tr), ecy + ery * math.sin(tr)
            nx, ny = math.cos(tr), math.sin(tr)
            ln = (0.30 + 0.18 * ((k * 37) % 5) / 4) * tufts
            wig = 0.18 * math.sin(t * 23 + k * 1.7) * tufts
            tipx = bx + nx * 0.15 + wig
            tipy = by + ln + 0.1
            base = [(bx - ny * 0.14, by + nx * 0.14), (bx + ny * 0.14, by - nx * 0.14)]
            c.poly(T([base[0], (tipx, tipy), base[1]]), **fur)
        # loose bits of fur flying off below
        for i in range(7):
            ph = (i * 0.37 + t * 2.6) % 1.0
            fx = ((i * 53) % 13 - 6) / 6 * 1.2 + 0.2 * math.sin(t * 9 + i)
            fy = 0.3 + ph * 3.2
            c.poly(T(ell(fx, fy, 0.07 * tufts, 0.12 * tufts, 30 * i, 10)), fill=BROWN, line=BROWN_D,
                   lw=L * 0.6, opacity=1 - ph)

    # tail
    tail = E(1.15, -0.28, 0.85, 0.33, -25)
    c.poly(tail, fill=BROWN_D, line=INK, lw=L, pressure=0.9)
    c.hatch(tail, col(0.22, 0.12, 0.07), spacing=0.14 * s, angle=40, lw=2.5)
    c.hatch(tail, col(0.22, 0.12, 0.07), spacing=0.14 * s, angle=-40, lw=2.5)
    # ears
    for sgn in (-1, 1):
        c.poly(E(sgn * 0.7, -2.78, 0.19, 0.19), **fur)
        c.poly(E(sgn * 0.7, -2.78, 0.09, 0.09), fill=PINK, pressure=0.7, jit=1)
    # body, belly, feet, arms
    c.poly(E(0, -1.05, 1.05, 1.02), **fur)
    c.poly(E(0, -0.9, 0.68, 0.72), fill=TAN, pressure=0.7, jit=1.5)
    c.hatch(E(0.55, -1.0, 0.45, 0.85), BROWN_D, spacing=0.11 * s, angle=60, lw=2, opacity=0.35)
    for sgn in (-1, 1):
        c.poly(E(sgn * 0.55, -0.06, 0.36, 0.16), fill=BROWN_D, line=INK, lw=L)
        c.poly(E(sgn * 0.8, -1.25, 0.22, 0.38, -sgn * 20), **fur)
    # head
    c.poly(E(0, -2.15, 0.98, 0.86), **fur)
    c.hatch(E(0.55, -2.25, 0.4, 0.7), BROWN_D, spacing=0.11 * s, angle=60, lw=2, opacity=0.35)
    bulge = 0.06 * mouth
    for sgn in (-1, 1):
        c.poly(E(sgn * 0.3, -1.86, 0.40 + bulge, 0.30 + bulge * 0.5), fill=TAN, line=BROWN, lw=L * 0.6,
               pressure=0.85)
        c.poly(E(sgn * 0.64, -2.02, 0.16, 0.09), fill=PINK, pressure=0.6, opacity=0.7, jit=1)
    # mouth and teeth
    if mouth > 0.02:
        c.poly(E(0, -1.44 + 0.08 * mouth, 0.2, 0.06 + 0.16 * mouth), fill=MOUTH, line=INK, lw=L * 0.6)
    ty = -1.66 - 0.05 * mouth
    for x0, x1 in ((-0.17, -0.005), (0.005, 0.17)):
        c.poly(T([(x0, ty), (x1, ty), (x1, ty + 0.3), (x0, ty + 0.32)]), fill=TEETH, line=BROWN_D,
               lw=L * 0.6, jit=1)
    c.line(T([(-0.3, -1.68), (-0.12, -1.63), (0, -1.68), (0.12, -1.63), (0.3, -1.68)]), BROWN_D, lw=L * 0.7)
    c.poly(E(0, -2.02, 0.2, 0.13), fill=NOSE, line=INK, lw=L * 0.5)
    c.poly(E(-0.06, -2.06, 0.06, 0.03), fill=WHITE, pressure=0.7, jit=0.5)
    for sgn in (-1, 1):
        for dy in (-0.12, 0.0, 0.12):
            c.line(T([(sgn * 0.5, -1.9 + dy * 0.5), (sgn * 1.05, -1.95 + dy)]), INK, lw=L * 0.35,
                   pressure=0.7)
    # silly, sleepy, mismatched eyes
    for (ex, ey, er, px, py, pr) in ((-0.38, -2.45, 0.19, 0.06, 0.07, 0.075),
                                     (0.37, -2.48, 0.25, -0.08, 0.09, 0.095)):
        c.poly(E(ex, ey, er, er), fill=WHITE, line=INK, lw=L * 0.6, pressure=1.0)
        c.poly(E(ex + px, ey + py, pr, pr), fill=INK, pressure=1.0, jit=0.8)
        th = np.linspace(np.pi, 2 * np.pi, 14)
        lid = [(ex + er * 1.08 * math.cos(q), ey + er * 1.08 * math.sin(q)) for q in th]
        lid += [(ex + er * 1.08, ey + 0.03), (ex - er * 1.08, ey + 0.03)]
        c.poly(T(lid), fill=BROWN, pressure=1.0, jit=1)
        c.line(T([(ex - er * 1.1, ey + 0.04), (ex, ey + 0.055), (ex + er * 1.1, ey + 0.04)]), INK, lw=L * 0.8)
    # singed fur
    if singe > 0:
        for (sx_, sy_, rx, ry) in ((-0.35, -2.72, 0.38, 0.16), (0.55, -1.35, 0.3, 0.26),
                                   (-0.6, -0.8, 0.26, 0.2), (0.62, -2.0, 0.18, 0.14)):
            c.poly(E(sx_, sy_, rx, ry), fill=SOOT, pressure=0.6, opacity=0.6 * singe, jit=2)
        for k in range(9):
            bx = -0.7 + k * 0.175
            by = -2.95 + 0.18 * (bx * bx)
            zz = [(bx, by)]
            for j in range(1, 4):
                zz.append((bx + (0.06 if j % 2 else -0.06), by - 0.09 * j))
            c.line(T(zz), SOOT, lw=L * 0.6, opacity=singe)


# ---------------------------------------------------------------------------
# Effects
# ---------------------------------------------------------------------------
def flame(c, bx, by, dx, dy, length, width, t, seed=0, layers=3, opacity=1.0):
    n = math.hypot(dx, dy)
    dx, dy = dx / n, dy / n
    nx, ny = -dy, dx
    specs = [(FIRE_R, 1.0, 1.0), (FIRE_O, 0.75, 0.68), (FIRE_Y, 0.5, 0.38)][:layers]
    for li, (colr, lf, wf) in enumerate(specs):
        Lh, Wd = length * lf, width * wf
        us = np.linspace(0, 1, 16)
        left, right = [], []
        for u in us:
            w = Wd * (1 - u) ** 0.75
            wob = math.sin(u * 9 + t * 22 + seed + li) * Wd * 0.22 * u
            px, py = bx + dx * u * Lh, by + dy * u * Lh
            left.append((px + nx * (w + wob), py + ny * (w + wob)))
            right.append((px - nx * (w - wob), py - ny * (w - wob)))
        cap = [(bx - dx * Wd * 0.6 * math.sin(q) + nx * Wd * math.cos(q),
                by - dy * Wd * 0.6 * math.sin(q) + ny * Wd * math.cos(q)) for q in np.linspace(0, np.pi, 9)]
        pts = left + right[::-1] + cap[::-1][1:-1]
        c.poly(pts, fill=colr, line=FIRE_R if li == 0 else None, lw=5, pressure=0.95, jit=3, opacity=opacity)


def puff(c, x, y, r, opacity=1.0, colr=PUFF):
    c.poly(ell(x, y, r, r * 0.9, 0, 28), fill=colr, line=SMOKE, lw=5, pressure=0.95, jit=r * 0.06,
           opacity=opacity)


def cloud(c, cx, cy, sc, opacity=1.0):
    parts = [(0, 0, 1.0), (-0.95, 0.22, 0.68), (0.95, 0.25, 0.74), (-0.45, -0.45, 0.7), (0.5, -0.4, 0.62)]
    shapes = [ell(cx + px * sc, cy + py * sc, pr * sc, pr * sc * 0.85, 0, 30) for px, py, pr in parts]
    for sh in shapes:
        c.poly(sh, None, col(0.72, 0.76, 0.84), lw=9, lp=0.9, jit=3, opacity=opacity)
    for sh in shapes:
        c.poly(sh, fill=WHITE, pressure=1.0, jit=3, opacity=opacity)


def splash(c, x, y, age, big=1.0, seed=0):
    if age < 0 or age > 0.9:
        return
    r = np.random.default_rng(seed)
    fade = 1 - age / 0.9
    c.poly(ell(x, y, (40 + 260 * age) * big, (10 + 60 * age) * big, 0, 30), None, WATER_D, lw=5,
           opacity=fade)
    for i in range(8):
        vx = r.uniform(-260, 260) * big
        vy = -r.uniform(300, 650) * big
        px, py = x + vx * age, y + vy * age + 0.5 * 1800 * age * age
        if py > y + 5:
            continue
        rr = r.uniform(7, 14) * big
        c.poly(ell(px, py, rr * 0.8, rr, 0, 12), fill=WATER, line=WATER_D, lw=3, jit=0.8, opacity=fade)


def smoke_wisp(c, x, y, t, seed, length=10, opacity=0.8, lw=7):
    pts = []
    for k in range(length):
        yy = y - k * 20
        xx = x + (6 + k * 2.2) * math.sin(k * 0.65 - t * 5 + seed)
        pts.append((xx, yy))
    c.line(pts, SMOKE, lw=lw, pressure=0.7, opacity=opacity)


def stars(c, n=70, seed=5):
    r = np.random.default_rng(seed)
    cam = c.cam
    c.cam = (1.0, 0.0, 0.0)
    for i in range(n):
        x, y = r.uniform(0, W), r.uniform(0, H)
        s = r.uniform(2, 5)
        if s > 4.2:
            c.line([(x - 9, y), (x + 9, y)], col(1, 0.97, 0.8), lw=3, jit=0.3)
            c.line([(x, y - 9), (x, y + 9)], col(1, 0.97, 0.8), lw=3, jit=0.3)
        c.poly(ell(x, y, s, s, 0, 8), fill=col(1, 0.98, 0.88), pressure=1.0, jit=0.4)
    c.cam = cam


# ---------------------------------------------------------------------------
# Forest scene data (fixed so it looks the same every drawing)
# ---------------------------------------------------------------------------
_rf = np.random.default_rng(42)
FAR_TREES = [(x, _rf.uniform(170, 280)) for x in np.arange(-20, 1120, 78)]
RIPPLES = [(_rf.uniform(-40, 1040), _rf.uniform(1290, 1900), _rf.uniform(60, 180)) for _ in range(26)]
RIPPLES = [rp for rp in RIPPLES if not (1310 < rp[1] < 1500)]


def dam_top(x):
    return 1402 - 50 * math.sin(math.pi * clamp01((x - 40) / 1000))


DAM_STICKS = []
for _ in range(58):
    x = _rf.uniform(90, 990)
    y = _rf.uniform(dam_top(x) + 6, 1478)
    DAM_STICKS.append((x, y, _rf.uniform(60, 160), _rf.uniform(-22, 22), int(_rf.integers(0, 3)),
                       _rf.uniform(7, 11)))
# sticks that fall into the water in beat 2: (fall time, x, y, length, angle, land x, land y)
FALL_STICKS = [(3.0, 250, 1392, 130, 12, 215, 1585), (3.6, 790, 1385, 120, -10, 845, 1600),
               (4.1, 395, 1370, 110, 6, 370, 1655)]

ROUND_TREES = [(165, 1235, 820, 185), (925, 1235, 850, 165)]
PINES = [(40, 1245, 760), (1050, 1245, 700), (330, 1230, 430), (745, 1230, 400)]

LEAVES = []
for i in range(46):
    tx, _, cy, cr = ROUND_TREES[i % 2]
    ang = _rf.uniform(0, 6.28)
    rr = cr * math.sqrt(_rf.uniform(0, 0.8))
    t0 = 1.9 + 2.5 * math.sqrt(_rf.uniform(0, 1))
    LEAVES.append(dict(t0=t0, x=tx + rr * math.cos(ang), y=cy + rr * math.sin(ang),
                       vy=_rf.uniform(180, 330), sway=_rf.uniform(20, 45), ph=_rf.uniform(0, 6.3),
                       land=_rf.uniform(1265, 1880), c=[GREEN1, GREEN_L, GREEN2][i % 3]))

SPLASHES = sorted([(2.2 + 2.2 * math.sqrt(_rf.uniform(0, 1)), _rf.uniform(60, 1020),
                    _rf.choice([_rf.uniform(1520, 1860), _rf.uniform(1265, 1320)]), i) for i in range(15)])

EMBERS = []
for i in range(26):
    t0 = 15.1 + i * 0.17 + _rf.uniform(0, 0.12)
    x1 = _rf.uniform(30, 1050)
    if 360 < x1 < 720:
        x1 += 380 if x1 > 540 else -330
    y1 = _rf.uniform(1150, 1880)
    EMBERS.append(dict(t0=t0, x0=x1 + _rf.uniform(120, 260), x1=x1, y1=y1, sp=_rf.uniform(1100, 1500),
                       r=_rf.uniform(7, 13), seed=i))

BEAVER_X, BEAVER_Y, BEAVER_S = 540, 1380, 130
LEAF_BASE_BUSH = (850, 1325)


def pine(c, x, base, h, colr, pressure=0.85, lined=True):
    w = h * 0.42
    c.poly([(x - 9, base), (x + 9, base), (x + 7, base - h * 0.3), (x - 7, base - h * 0.3)], fill=TRUNK,
           line=BROWN_D if lined else None, lw=4)
    for k in range(3):
        top = base - h + k * h * 0.22
        bot = top + h * 0.45
        ww = w * (0.55 + 0.25 * k)
        c.poly([(x, top), (x + ww, bot), (x - ww, bot)], fill=colr, line=GREEN2 if lined else None, lw=5,
               pressure=pressure)


def round_tree(c, x, base, cy, r):
    c.poly([(x - 16, base), (x + 16, base), (x + 11, cy), (x - 11, cy)], fill=TRUNK, line=BROWN_D, lw=5)
    parts = [(0, 0, 1.0), (-0.55, 0.25, 0.65), (0.55, 0.3, 0.62)]
    for px, py, pr in parts:
        c.poly(blob(x + px * r, cy + py * r, pr * r, int(x + px * 100)), None, GREEN2, lw=7)
    for px, py, pr in parts:
        sh = blob(x + px * r, cy + py * r, pr * r, int(x + px * 100))
        c.poly(sh, fill=GREEN1, pressure=0.95)
    c.hatch(blob(x + 0.3 * r, cy + 0.2 * r, 0.6 * r, 3), GREEN2, spacing=15, angle=55, lw=3, opacity=0.6)


def stick(c, x, y, ln, ang, ci, lw=9, opacity=1.0):
    a = math.radians(ang)
    dx, dy = math.cos(a) * ln / 2, math.sin(a) * ln / 2
    c.line([(x - dx, y - dy), (x + dx, y + dy)], BROWN_D, lw=lw + 4, jit=1, opacity=opacity)
    c.line([(x - dx, y - dy), (x + dx, y + dy)], STICKS[ci], lw=lw, jit=1, opacity=opacity)


def leaf_shape(tipx, tipy, bx, by, frac):
    dx, dy = bx - tipx, by - tipy
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    ln = 115 * frac
    wd = 36 * max(0.35, frac) ** 0.6
    pts_l, pts_r = [], []
    for u in np.linspace(0, 1, 12):
        w = wd * math.sin(math.pi * u) ** 0.8
        px, py = tipx + ux * ln * u, tipy + uy * ln * u
        pts_l.append((px + nx * w, py + ny * w))
        pts_r.append((px - nx * w, py - ny * w))
    base = (tipx + ux * ln, tipy + uy * ln)
    return pts_l + pts_r[::-1], base


def bush(c):
    for (px, py, pr) in ((870, 1335, 58), (818, 1355, 44), (920, 1360, 46)):
        c.poly(blob(px, py, pr, px), fill=GREEN1, line=GREEN2, lw=5)


def sapling(c, tip, frac):
    tipx, tipy = tip
    if frac > 0.01:
        leaf, base = leaf_shape(tipx, tipy, 780, 1200, frac)
    else:
        base = (tipx + 25, tipy)
    # curved twig from bush to leaf base
    ctrl = (820, 1150)
    pts = []
    for u in np.linspace(0, 1, 14):
        pts.append(((1 - u) ** 2 * 845 + 2 * u * (1 - u) * ctrl[0] + u * u * base[0],
                    (1 - u) ** 2 * 1310 + 2 * u * (1 - u) * ctrl[1] + u * u * base[1]))
    c.line(pts, BROWN_D, lw=7)
    if frac > 0.01:
        c.poly(leaf, fill=GREEN_L, line=GREEN2, lw=5, pressure=0.95)
        c.line([(tipx, tipy), base], GREEN2, lw=3)


def draw_leaf(c, x, y, ang, colr, sc=1.0):
    pts = ell(x, y, 16 * sc, 8 * sc, ang, 14)
    c.poly(pts, fill=colr, line=GREEN2, lw=3, jit=0.8)


def ember(c, x, y, dx, dy, r, t, seed):
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    c.glow(x, y, r * 4, FIRE_O, 0.35)
    flame(c, x - ux * r * 0.3, y - uy * r * 0.3, -ux, -uy, r * 6.5, r * 1.25, t, seed=seed, opacity=0.95)
    c.poly(blob(x, y, r * 1.15, seed, 12, 0.3), fill=col(0.30, 0.13, 0.10), line=FIRE_O, lw=4)


def forest(c, t, light=0.0, shake=0.0, after=False, beaver_on=True, bv=None):
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
    # sticks that fell off the dam, then float
    for i, (tf, x, y, ln, ang, lx, ly) in enumerate(FALL_STICKS):
        if t >= tf:
            u = clamp01((t - tf) / 0.4)
            if u < 1:
                px, py = lerp(x, lx, u), lerp(y, ly, u * u)
                stick(c, px, py, ln, ang + 180 * u, i % 3)
            else:
                drift = (t - tf - 0.4) * 12
                stick(c, lx + drift, ly + 5 * math.sin(t * 3 + i), ln, ang + 180, i % 3)
                c.poly(ell(lx + drift, ly + 12, ln * 0.6, 10, 0, 20), None, WATER_D, lw=3, opacity=0.6)
    # the dam
    xs = np.linspace(40, 1040, 26)
    top = [(x, dam_top(x) + r.normal(0, 0) + 8 * math.sin(x * 0.05)) for x in xs]
    bot = [(x, 1482 + 6 * math.sin(x * 0.09)) for x in xs[::-1]]
    c.poly(top + bot, fill=MUD, line=BROWN_D, lw=6, pressure=0.9)
    for (x, y, ln, ang, ci, lw) in DAM_STICKS:
        stick(c, x, y, ln, ang, ci, lw)
    for (tf, x, y, ln, ang, lx, ly) in FALL_STICKS:
        if t < tf:
            wob = math.sin(t * 40) * 3 * clamp01((t - tf + 0.8) / 0.8) if t > tf - 0.8 else 0
            stick(c, x + wob, y, ln, ang + wob, 0)
    c.line([(x, y) for x, y in top], BROWN_D, lw=5)
    for i, tf in enumerate(ft[0] for ft in FALL_STICKS):
        splash(c, FALL_STICKS[i][5], FALL_STICKS[i][6], t - tf - 0.4, 0.8, seed=50 + i)
    return r


def light_overlay(c, p):
    if p <= 0:
        return
    cam = c.cam
    c.cam = (1.0, 0.0, 0.0)
    for k, (x, sw) in enumerate(((150, 1), (420, -1), (700, 1), (960, -1))):
        wob = 30 * math.sin(c.d * 0.3 + k)
        top = [(x - 70 + wob, -20), (x + 70 + wob, -20)]
        bot = [(x + 230 * sw + 180, H + 20), (x + 230 * sw - 180, H + 20)]
        c.poly(top + bot, fill=LIGHT, pressure=0.6, opacity=0.35 * p, jit=6)
    c.vgrad(LIGHT, 0.75 * p, 0.12 * p, 0, H)
    c.cam = cam


# ---------------------------------------------------------------------------
# Space scene data
# ---------------------------------------------------------------------------
EARTH_C, EARTH_R = (540.0, 2900.0), 1300.0
_re = np.random.default_rng(9)
LANDS = []
for i in range(9):
    ph = _re.uniform(-2.6, -0.5)
    rho = _re.uniform(0.35, 0.8)
    LANDS.append((ph, rho, _re.uniform(0.08, 0.16), i))
AST_SEED = 77
_ra = np.random.default_rng(AST_SEED)
CRATERS = [(_ra.uniform(0, 6.28), _ra.uniform(0.1, 0.7), _ra.uniform(0.08, 0.17)) for _ in range(7)]
CRACKS = []
for i in range(10):
    a0 = i * 0.63 + _ra.uniform(-0.2, 0.2)
    pts = [(0.0, 0.0)]
    rr, a = 0.0, a0
    while rr < 1.05:
        rr += _ra.uniform(0.1, 0.2)
        a += _ra.uniform(-0.3, 0.3)
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    CRACKS.append(pts)
FRAGS = []
for i in range(380):
    ang = _ra.uniform(0, 6.28)
    rho = math.sqrt(_ra.uniform(0, 1))
    FRAGS.append(dict(a=ang, rho=rho, sp=_ra.uniform(700, 2600), sz=_ra.uniform(5, 42) * (1.3 - rho * 0.5),
                      rot=_ra.uniform(0, 360), spin=_ra.uniform(-400, 400),
                      c=[ROCK, ROCK_D, FIRE_O, FIRE_Y, FIRE_R, ROCK_B][i % 6], seed=i))


def earth(c):
    cx, cy = EARTH_C
    R = EARTH_R
    c.poly(ell(cx, cy, R * 1.035, R * 1.035, 0, 140), fill=ATMOS, pressure=0.55, opacity=0.7, jit=3)
    c.poly(ell(cx, cy, R, R, 0, 140), fill=OCEAN, line=OCEAN_D, lw=10, pressure=0.95, jit=3)
    for ph, rho, sz, i in LANDS:
        x, y = cx + rho * R * math.cos(ph), cy + rho * R * math.sin(ph)
        c.poly(blob(x, y, sz * R, 300 + i, 30, 0.3), fill=GREEN1 if i % 3 else DESERT, line=GREEN2, lw=7)
    for k in range(6):
        ph = -2.5 + k * 0.35
        rho = 0.88 - 0.05 * (k % 3)
        a0, a1 = ph, ph + 0.18
        pts = [(cx + rho * R * math.cos(q), cy + rho * R * math.sin(q)) for q in np.linspace(a0, a1, 8)]
        c.line(pts, WHITE, lw=16, pressure=0.8, opacity=0.8)
    c.hatch(ell(cx + R * 0.35, cy + R * 0.1, R * 0.75, R * 1.0, 0, 60), OCEAN_D, spacing=26, angle=60, lw=4,
            opacity=0.35)


def asteroid_pts(cx, cy, r):
    return blob(cx, cy, r, AST_SEED, 64, 0.22)


def asteroid(c, cx, cy, r, t, cracks=0.0, hole=0.0, flames=True):
    c.glow(cx, cy - 0.2 * r, r * 2.3, FIRE_O, 0.45)
    if flames:
        for k in range(10):
            th = math.radians(-170 + k * 17.7)
            bx, by = cx + 0.8 * r * math.cos(th), cy + 0.8 * r * math.sin(th)
            dx, dy = 0.45 * math.cos(th), -1.0
            ln = r * (1.0 + 0.45 * ((k * 7) % 5) / 4) * (1 + 0.08 * math.sin(t * 17 + k))
            flame(c, bx, by, dx, dy, ln, r * 0.32, t, seed=k)
    pts = asteroid_pts(cx, cy, r)
    c.poly(pts, fill=ROCK, line=ROCK_D, lw=12, pressure=0.95)
    c.hatch(blob(cx + r * 0.3, cy + r * 0.25, r * 0.7, 4), ROCK_D, spacing=18, angle=50, lw=4, opacity=0.6)
    for a, rho, sz in CRATERS:
        x, y = cx + rho * r * math.cos(a), cy + rho * r * math.sin(a)
        c.poly(ell(x, y, sz * r, sz * r * 0.75, 0, 24), fill=ROCK_D, line=col(0.2, 0.17, 0.17), lw=6,
               pressure=0.8)
        c.line([(x - sz * r * 0.8, y + sz * r * 0.35), (x + sz * r * 0.6, y + sz * r * 0.55)], ROCK, lw=5)
    lower = [p for p in pts if p[1] > cy + 0.2 * r]
    if len(lower) > 2:
        lower = sorted(lower, key=lambda p: p[0])
        c.line(lower, FIRE_R, lw=max(16, r * 0.05), opacity=0.9)
        c.line(lower, FIRE_O, lw=max(10, r * 0.03), opacity=0.9)
        c.line(lower, FIRE_Y, lw=max(5, r * 0.012), opacity=0.9)
    if hole > 0:
        c.glow(cx, cy + r * 0.95, r * 0.6 * hole, FIRE_Y, 0.9)
        c.poly(ell(cx, cy + r * 0.93, r * 0.16 * hole, r * 0.08 * hole, 0, 20), fill=WHITE, line=FIRE_O, lw=6)
    if cracks > 0:
        for pts_c in CRACKS:
            n = max(2, int(len(pts_c) * cracks + 0.5))
            seg = [(cx + x * r * 0.95, cy + y * r * 0.95) for x, y in pts_c[:n]]
            c.line(seg, FIRE_O, lw=16, opacity=1.0)
            c.line(seg, FIRE_Y, lw=7, opacity=1.0)
        c.glow(cx, cy, r * 1.2, FIRE_Y, 0.45 * cracks)


# ---------------------------------------------------------------------------
# The film: one function that draws any moment in time
# ---------------------------------------------------------------------------
BITES = [16.45, 17.05, 17.65, 18.25, 18.85]


def scene_forest_start(c, t):
    p = clamp01((t - 1.5) / 3.0)
    forest(c, t, shake=24 * p * p)
    lean = 7 * sstep(0.2, 1.2, t)
    mouth = 0.6 * sstep(0.6, 1.3, t)
    bush(c)
    light_overlay(c, p ** 1.3)
    beaver(c, BEAVER_X, BEAVER_Y, BEAVER_S, lean=lean, mouth=mouth)
    sapling(c, (608, 1178), 1.0)
    # falling leaves
    for lf in LEAVES:
        if t < lf['t0']:
            continue
        dt = t - lf['t0']
        y = min(lf['y'] + lf['vy'] * dt, lf['land'])
        x = lf['x'] + lf['sway'] * math.sin(lf['ph'] + 3 * dt)
        draw_leaf(c, x, y, 40 * math.sin(lf['ph'] + 4 * dt), lf['c'])
    for (ts, x, y, i) in SPLASHES:
        splash(c, x, y, t - ts, 0.9, seed=i)
    c.wash(LIGHT, 0.18 * p ** 1.3, textured=True)


def scene_launch(c, t):
    u = t - 4.5
    forest(c, t, shake=30 * max(0.0, 1 - u / 0.6))
    bush(c)
    sapling(c, (608 + 25 * math.sin(u * 30) * max(0, 1 - u * 2), 1178), 1.0)
    light_overlay(c, 1.0)
    by = BEAVER_Y - 7000 * u
    # smoke column
    ytop = max(by, -300)
    for k, yk in enumerate(np.arange(1330, ytop - 1, -85)):
        tp = 4.5 + (BEAVER_Y - yk) / 7000
        age = t - tp
        rad = 42 + 190 * age
        puff(c, 540 + 22 * math.sin(k * 1.9), yk, rad, opacity=1.0)
    for k in range(6):
        sgn = -1 if k % 2 else 1
        dist = (80 + 420 * min(1.0, u * 2.2)) * (0.5 + 0.5 * (k // 2) / 2)
        puff(c, 540 + sgn * dist, 1350 - 20 * (k // 2), 60 + 120 * u)
    splash(c, 330, 1520, u, 1.8, seed=91)
    splash(c, 760, 1530, u, 1.8, seed=92)
    if by > -600:
        flame(c, 540, by - 10, 0, 1, 260, 55, t)
        beaver(c, 540, by, BEAVER_S, sx=0.72, sy=1.7, tufts=1.0, t=t)
    for lf in LEAVES:
        dt = t - lf['t0']
        y = min(lf['y'] + lf['vy'] * max(0.0, dt), lf['land']) if dt > 0 else lf['y']
        x = lf['x'] + (lf['x'] - 540) * u * 1.5
        draw_leaf(c, x, y - 200 * u, 200 * u + lf['ph'] * 30, lf['c'])
    c.wash(LIGHT, 0.18, textured=True)


def scene_flight(c, t):
    u = t - 5.0
    k1 = sstep(5.0, 6.0, t)
    k2 = sstep(6.0, 6.5, t)
    sky = SKY * (1 - k1) + col(0.40, 0.58, 0.88) * k1
    sky = sky * (1 - k2) + SPACE * k2
    c.fill_screen(sky, 0.55 + 0.4 * k1)
    if k2 > 0.3:
        stars(c, 40)
    speed = 2600
    back = [(180, -250, 1.1), (880, -700, 1.3), (300, -2400, 1.2), (820, -2900, 1.0), (140, -3400, 0.9)]
    front = [(540, -1310, 2.3), (130, -1260, 1.8), (960, -1360, 1.9), (330, -1150, 1.4), (760, -1170, 1.5)]
    for x, y0, sc in back:
        cloud(c, x, y0 + speed * u, 150 * sc)
    # speed lines
    r = np.random.default_rng(c.d * 3)
    for i in range(int(16 * (1 - k2))):
        x = r.uniform(20, W - 20)
        y = r.uniform(-200, H)
        c.line([(x, y), (x, y + r.uniform(160, 420))], WHITE, lw=4, pressure=0.8, opacity=0.7)
    bx, by = 540, 1120
    blaze = sstep(5.2, 5.8, t)
    c.glow(bx, by - 250, 520, FIRE_O, 0.35 * blaze)
    # trail: smoke puffs scrolling away, fire in the middle
    for k in range(9):
        yk = by + 60 + ((k * 120 + speed * u * 0.5) % 1000)
        age = (yk - by) / 1000
        puff(c, bx + (1 if k % 2 else -1) * (40 + 60 * age), yk, 50 + 110 * age, opacity=1 - 0.5 * blaze)
    flame(c, bx, by - 20, 0, 1, 420 + 520 * blaze, 60 + 30 * blaze, t)
    beaver(c, bx, by, 150, sx=0.76, sy=1.38, tufts=1.0, t=t)
    for x, y0, sc in front:
        cloud(c, x, y0 + speed * u, 150 * sc)


def space_cam(t):
    z = 0.3 ** sstep(8.0, 9.7, t)
    return z, 540 * (1 - z), 630 * (1 - z) / 0.7


def scene_space(c, t):
    c.fill_screen(SPACE, 1.25)
    stars(c)
    z, ox, oy = space_cam(t)
    c.cam = (z, ox, oy)
    earth(c)
    ay = lerp(-1500, -650, clamp01((t - 8.0) / 2.0))
    asteroid(c, 540, ay, 767, t)
    if t < 8.0:
        by = lerp(1760, 950, 1 - (1 - clamp01((t - 6.5) / 1.5)) ** 2)
    else:
        by = lerp(950, 760, clamp01((t - 8.0) / 2.0))
    c.line([(540, 1600), (540, by + 80)], PUFF, lw=14, pressure=0.7, opacity=0.6)
    c.glow(540, by - 120, 260, FIRE_O, 0.4)
    flame(c, 540, by - 10, 0, 1, 300, 32, t)
    beaver(c, 540, by, 95, sx=0.8, sy=1.3, tufts=1.0, t=t)
    c.cam = (1.0, 0.0, 0.0)
    c.vgrad(FIRE_R, 0.22 * sstep(8.3, 10.0, t), 0.0, 0, H * 0.55)


def scene_face(c, t):
    c.fill_screen(SPACE, 1.25)
    stars(c, 50, seed=8)
    c.vgrad(FIRE_R, 0.2, 0.0, 0, H * 0.3)
    asteroid(c, 540, -930, 1150, t, flames=False)
    beaver(c, 540, 1905, 420, tufts=0.55, t=t)
    c.vgrad(FIRE_O, 0.10, 0.0, 0, H * 0.6)


AST_C, AST_R = (540.0, 900.0), 560.0


def scene_impact(c, t):
    c.fill_screen(SPACE, 1.25)
    stars(c)
    asteroid(c, AST_C[0], AST_C[1], AST_R, t, hole=sstep(11.45, 11.6, t))
    entry = AST_C[1] + AST_R * 0.95
    if t < 11.45:
        u = (t - 11.0) / 0.45
        by = lerp(2050, entry + 60, u * u)
        flame(c, 540, by - 5, 0, 1, 320, 20, t)
        beaver(c, 540, by, 42, sx=0.75, sy=1.45, tufts=1.0, t=t)
    else:
        u = clamp01((t - 11.45) / 0.15)
        rr = 60 + 260 * u
        star = []
        for k in range(24):
            q = k / 24 * 2 * math.pi
            rad = rr * (1.0 if k % 2 else 0.45)
            star.append((540 + rad * math.cos(q), entry + rad * math.sin(q)))
        c.glow(540, entry, rr * 2, FIRE_Y, 0.8)
        c.poly(star, fill=WHITE, line=FIRE_Y, lw=8, pressure=1.0, jit=4)
        r = np.random.default_rng(5)
        for i in range(16):
            q = r.uniform(0.2, math.pi - 0.2)
            d = (120 + 500 * u) * r.uniform(0.5, 1.2)
            c.poly(blob(540 + d * math.cos(q), entry + d * math.sin(q), r.uniform(10, 26), i, 8, 0.3),
                   fill=ROCK_D, line=INK, lw=3)


def scene_inside(c, t):
    u = t - 11.6
    c.fill_screen(ROCK_D, 1.2)
    for k in range(11):
        y = ((k * 250 + 4200 * u) % 2750) - 450
        colr = [ROCK, ROCK_B, col(0.36, 0.30, 0.30)][k % 3]
        topl = [(x, y + 25 * math.sin(x * 0.02 + k)) for x in np.linspace(-40, W + 40, 16)]
        botl = [(x, y + 120 + 25 * math.sin(x * 0.017 + k * 2)) for x in np.linspace(W + 40, -40, 16)]
        c.poly(topl + botl, fill=colr, line=col(0.2, 0.17, 0.17), lw=6, pressure=0.95)
    bx, by = 540, 1180
    c.glow(bx, by - 250, 640, FIRE_Y, 0.75)
    for k in range(8):
        q = k / 8 * 2 * math.pi + 0.3
        c.line([(bx + 200 * math.cos(q), by - 250 + 200 * math.sin(q)),
                (bx + 900 * math.cos(q + 0.1), by - 250 + 900 * math.sin(q + 0.1))], FIRE_O, lw=9, opacity=0.8)
    flame(c, bx, by - 20, 0, 1, 900, 70, t)
    beaver(c, bx, by, 125, sx=0.78, sy=1.35, tufts=1.0, t=t)
    r = np.random.default_rng(3)
    for i in range(28):
        q = r.uniform(0, 2 * math.pi)
        t0 = r.uniform(-0.4, 0.9)
        d = 150 + 1700 * ((u - t0) % 0.9)
        x, y = bx + d * math.cos(q), by - 250 + d * math.sin(q) + 900 * ((u - t0) % 0.9)
        c.poly(blob(x, y, r.uniform(18, 70), i, 9, 0.35), fill=[ROCK, ROCK_B, ROCK_D][i % 3], line=INK, lw=5)


def scene_burst(c, t):
    c.fill_screen(SPACE, 1.25)
    stars(c)
    cx, cy = AST_C
    if t < 13.1:
        asteroid(c, cx, cy, AST_R, t, cracks=sstep(12.5, 13.05, t), hole=1.0)
        if t >= 12.72:
            u = clamp01((t - 12.72) / 0.2)
            top = cy - AST_R * 0.95
            fade = 1 - clamp01((t - 12.92) / 0.2)
            c.glow(cx, top, 300, WHITE, 0.9 * fade)
            beam = [(cx - 12, top), (cx + 12, top), (cx + 45, top - 1300 * u), (cx - 45, top - 1300 * u)]
            c.poly(beam, fill=FIRE_Y, line=FIRE_O, lw=10, pressure=1.0, opacity=fade)
            c.poly([(cx - 5, top), (cx + 5, top), (cx + 16, top - 1300 * u), (cx - 16, top - 1300 * u)],
                   fill=WHITE, pressure=1.0, opacity=fade)
            r = np.random.default_rng(4)
            for i in range(14):
                q = r.uniform(-math.pi * 0.9, -math.pi * 0.1)
                d = 50 + 380 * u * r.uniform(0.5, 1.0)
                c.poly(blob(cx + d * math.cos(q), top + d * math.sin(q), r.uniform(8, 20), i, 8, 0.3),
                       fill=FIRE_O, line=FIRE_R, lw=3, opacity=fade)
    else:
        u = t - 13.1
        for f in FRAGS:
            d = f['rho'] * AST_R + f['sp'] * u
            x, y = cx + d * math.cos(f['a']), cy + d * math.sin(f['a'])
            if -60 < x < W + 60 and -60 < y < H + 60:
                c.poly(blob(x, y, f['sz'], f['seed'], 7, 0.35), fill=f['c'], line=INK if f['sz'] > 18 else None,
                       lw=3, jit=1)
        c.glow(cx, cy, 200 + 5200 * u ** 1.2, WHITE, 1.4, power=1.2)
        c.wash(WHITE, sstep(13.28, 13.45, t))


def scene_home(c, t):
    forest(c, t)
    # tiny burning rocks from the sky
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
            c.poly(blob(e['x1'], e['y1'], e['r'] * 0.8, e['seed'], 10, 0.3), fill=col(0.3, 0.12, 0.1),
                   line=FIRE_O, lw=3)
            if age < 0.35:
                puff(c, e['x1'], e['y1'] - 10, 14 + 60 * age, opacity=1 - age / 0.35)
            smoke_wisp(c, e['x1'], e['y1'] - 12, t, e['seed'], length=6, opacity=0.5, lw=4)
    # the beaver comes home
    lean, mouth, frac, sx, sy = 0.0, 0.0, 1.0, 1.0, 1.0
    y = BEAVER_Y
    if t < 14.75:
        u = clamp01((t - 14.4) / 0.35)
        y = lerp(-700, BEAVER_Y, u * u)
        sx, sy = 0.8, 1.35
    else:
        la = t - 14.75
        if la < 0.34:
            sq = [(1.3, 0.68), (1.12, 0.88), (0.95, 1.06), (1.0, 1.0)][min(3, int(la * 12))]
            sx, sy = sq
        splash(c, 330, 1520, la, 1.3, seed=93)
        splash(c, 760, 1530, la, 1.3, seed=94)
        if la < 0.45:
            for k in range(4):
                sgn = -1 if k % 2 else 1
                puff(c, 540 + sgn * (110 + 380 * la) * (1 + k // 2 * 0.3), 1385, 40 + 50 * la,
                     opacity=1 - la / 0.45, colr=col(0.85, 0.8, 0.72))
    if t >= 16.0:
        lean = 8 * sstep(16.0, 16.35, t)
        eaten = sum(1 for b in BITES if t >= b)
        frac = 1.0 - 0.2 * eaten
        chew = max(0.0, math.sin(2 * math.pi * 3.0 * (t - 16.35)))
        mouth = 0.55 * sstep(16.1, 16.35, t) if t < 16.35 else 0.12 + 0.4 * chew
    mx, my = beaver_point(BEAVER_X, BEAVER_Y, BEAVER_S, lean, 1, 1, 0.0, -1.5)
    tip = (lerp(608, mx + 12, sstep(16.1, 16.4, t)), lerp(1178, my - 2, sstep(16.1, 16.4, t)))
    bush(c)
    if t >= 14.4:
        beaver(c, BEAVER_X, y, BEAVER_S, lean=lean, sx=sx, sy=sy, mouth=mouth, singe=1.0)
        if t >= 14.75:
            for k, (u_, v_) in enumerate(((-0.45, -3.0), (0.4, -3.05), (0.9, -1.9))):
                px, py = beaver_point(BEAVER_X, y, BEAVER_S, lean, sx, sy, u_, v_)
                smoke_wisp(c, px, py, t, k * 2.1, length=11, opacity=0.75)
    sapling(c, tip, frac)
    # a last burning pebble lands on its head
    hx, hy = beaver_point(BEAVER_X, BEAVER_Y, BEAVER_S, lean, 1, 1, 0.12, -3.02)
    if 18.75 <= t < 19.2:
        u = (t - 18.75) / 0.45
        x, y2 = lerp(760, hx, u), lerp(-80, hy - 8, u)
        ember(c, x, y2, hx - 760, hy + 80, 13, t, 99)
    elif t >= 19.2:
        bounce = -26 if 19.2 <= t < 19.34 else 0
        c.glow(hx, hy - 8 + bounce, 45, FIRE_O, 0.6)
        c.poly(blob(hx, hy - 8 + bounce, 13, 99, 10, 0.3), fill=col(0.35, 0.14, 0.1), line=FIRE_O, lw=4)
        smoke_wisp(c, hx, hy - 20 + bounce, t, 7.0, length=9, opacity=0.7, lw=5)
    c.wash(WHITE, 1 - sstep(14.0, 14.45, t))


def render(d):
    t = d / FPS
    c = Canvas(d)
    if t < 4.5:
        scene_forest_start(c, t)
    elif t < 5.0:
        scene_launch(c, t)
    elif t < 6.5:
        scene_flight(c, t)
    elif t < 10.0:
        scene_space(c, t)
    elif t < 11.0:
        scene_face(c, t)
    elif t < 11.6:
        scene_impact(c, t)
    elif t < 12.5:
        scene_inside(c, t)
    elif t < 13.45:
        scene_burst(c, t)
    elif t < 14.0:
        c.wash(WHITE, 1.0)
    else:
        scene_home(c, t)
    return c.result()


# ---------------------------------------------------------------------------
# Sound effects (all made from scratch)
# ---------------------------------------------------------------------------
SR = 44100


def _band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.clip((f - lo * 0.8) / (lo * 0.4 + 1e-9), 0, 1) * np.clip((hi * 1.2 - f) / (hi * 0.4), 0, 1)
    return np.fft.irfft(X * m, len(x))


def _noise(dur, lo, hi, seed):
    x = _band(np.random.default_rng(seed).normal(size=int(dur * SR)), lo, hi)
    return x / (np.abs(x).max() + 1e-9)


def _tt(dur):
    return np.arange(int(dur * SR)) / SR


def _sweep(dur, f0, f1):
    tt = _tt(dur)
    f = f0 + (f1 - f0) * tt / dur
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def make_audio(path):
    out = np.zeros(int(DUR * SR))

    def add(t0, sig):
        i = int(t0 * SR)
        j = min(len(out), i + len(sig))
        if j > i:
            out[i:j] += sig[:j - i]

    def dec(dur, tau):
        return np.exp(-_tt(dur) / tau)

    # forest air and birds
    for a, b in ((0.0, 4.5), (14.4, 20.0)):
        n = _noise(b - a, 400, 3000, int(a))
        env = np.clip(_tt(b - a) / 0.3, 0, 1)
        add(a, 0.02 * n * env)
    for tb in (0.3, 0.52, 1.05, 17.4, 17.6):
        add(tb, 0.07 * _sweep(0.07, 3000, 4300) * np.hanning(int(0.07 * SR)))
    # the rumble builds
    d = 3.0
    tt = _tt(d)
    env = (tt / d) ** 2
    add(1.5, (0.75 * _noise(d, 25, 140, 1) + 0.25 * np.sin(2 * np.pi * 42 * tt) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * tt))
              + 0.18 * _noise(d, 150, 600, 2) * (np.random.default_rng(3).random(len(tt)) > 0.6)) * env)
    # launch blast and flight roar
    add(4.5, 0.9 * _noise(1.2, 30, 4000, 4) * dec(1.2, 0.35) + 0.6 * np.sin(2 * np.pi * 55 * _tt(1.2)) * dec(1.2, 0.5))
    d = 2.1
    tt = _tt(d)
    env = np.clip(tt / 0.15, 0, 1) * np.clip((d - tt) / 0.4, 0, 1)
    add(4.5, (0.35 * _noise(d, 150, 2500, 5) + 0.3 * _noise(d, 60, 300, 6)) * env * (0.85 + 0.15 * np.sin(tt * 60)))
    add(5.6, 0.35 * _noise(0.5, 500, 5000, 7) * np.hanning(int(0.5 * SR)))
    # space, then the looming asteroid
    d = 3.4
    tt = _tt(d)
    add(6.6, 0.05 * np.sin(2 * np.pi * 50 * tt) * np.clip(tt / 0.5, 0, 1))
    d = 2.0
    tt = _tt(d)
    env = (tt / d) ** 1.5
    add(8.0, (0.55 * _noise(d, 20, 90, 8) + 0.15 * _sweep(d, 110, 80)) * env)
    out[int(10.0 * SR):int(11.0 * SR)] = 0.0  # total silence on the face
    # into the asteroid
    d = 0.45
    add(11.0, 0.5 * _noise(d, 300, 3000, 9) * (_tt(d) / d))
    add(11.45, 0.9 * _noise(0.6, 80, 5000, 10) * dec(0.6, 0.25) + 0.5 * np.sin(2 * np.pi * 70 * _tt(0.6)) * dec(0.6, 0.3))
    r = np.random.default_rng(11)
    for tk in np.arange(11.6, 12.5, 0.055):
        add(tk, r.uniform(0.3, 0.6) * _noise(0.05, 150, 3000, int(tk * 1000)) * dec(0.05, 0.015))
    add(11.6, 0.35 * _noise(0.9, 30, 150, 12))
    # out the other side, then the boom
    add(12.72, 0.35 * _sweep(0.25, 400, 2400) * dec(0.25, 0.12) + 0.2 * _noise(0.25, 3000, 9000, 13) * dec(0.25, 0.1))
    add(13.1, 1.0 * _noise(1.8, 20, 200, 14) * dec(1.8, 0.9) + 0.6 * _noise(1.8, 200, 6000, 15) * dec(1.8, 0.3)
        + 0.5 * np.sin(2 * np.pi * 45 * _tt(1.8)) * dec(1.8, 1.2))
    add(13.45, 0.04 * np.sin(2 * np.pi * 3200 * _tt(0.8)) * dec(0.8, 0.3))
    # falling home, thud, sizzle
    add(14.4, 0.18 * _sweep(0.35, 2000, 700))
    add(14.75, 0.8 * np.sin(2 * np.pi * np.cumsum(np.linspace(90, 50, int(0.3 * SR))) / SR) * dec(0.3, 0.15)
        + 0.5 * _noise(0.3, 60, 800, 16) * dec(0.3, 0.12))
    add(14.75, 0.25 * _noise(0.6, 800, 6000, 17) * dec(0.6, 0.3))
    add(14.75, 0.06 * _noise(2.5, 3000, 9000, 18) * dec(2.5, 1.2))
    # chewing
    for b in BITES:
        add(b, 0.45 * _noise(0.08, 1500, 6000, int(b * 100)) * dec(0.08, 0.03)
            + 0.3 * _noise(0.08, 300, 1200, int(b * 100) + 1) * dec(0.08, 0.03))
    tk = 16.35 + 0.25 / 3
    while tk < 20:
        if all(abs(tk - b) > 0.12 for b in BITES):
            add(tk, 0.15 * _noise(0.05, 1200, 5000, int(tk * 100)) * dec(0.05, 0.02))
        tk += 1 / 3
    # tiny rocks landing
    for e in EMBERS:
        tl = e['t0'] + (e['y1'] + 80) / e['sp']
        add(tl, 0.07 * _noise(0.25, 2000, 8000, e['seed'] + 200) * dec(0.25, 0.12))
    # bonk
    add(19.2, 0.35 * _sweep(0.14, 900, 350) * dec(0.14, 0.06))
    add(19.2, 0.3 * _noise(0.04, 200, 1500, 19) * dec(0.04, 0.01))
    add(19.2, 0.05 * _noise(0.8, 3000, 9000, 20) * dec(0.8, 0.4))
    out[-int(0.05 * SR):] *= np.linspace(1, 0, int(0.05 * SR))
    out = out / (np.abs(out).max() + 1e-9) * 0.89
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes((out * 32767).astype(np.int16).tobytes())


def render_video(path, crf=27):
    import imageio.v2 as imageio
    import imageio_ffmpeg
    from multiprocessing import Pool
    tmp_v, tmp_a = path + '.video.mp4', path + '.audio.wav'
    wr = imageio.get_writer(tmp_v, fps=FPS, codec='libx264', quality=None, pixelformat='yuv420p',
                            macro_block_size=8, ffmpeg_params=['-vf', 'scale=720:1280:flags=lanczos', '-crf', str(crf),
                                                               '-preset', 'slow'])
    n = int(DUR * FPS)
    with Pool(os.cpu_count()) as pool:
        for i, frame in enumerate(pool.imap(render, range(n), chunksize=2)):
            wr.append_data(frame)
            if i % 24 == 0:
                print(f'frame {i}/{n}', flush=True)
    wr.close()
    make_audio(tmp_a)
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', tmp_v, '-i', tmp_a,
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-shortest', path],
                   check=True)
    os.remove(tmp_v)
    os.remove(tmp_a)
    print(f'done: {path} ({os.path.getsize(path) / 1e6:.1f} MB)')


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for ts in sys.argv[3:]:
            d = int(round(float(ts) * FPS))
            Image.fromarray(render(d)).save(os.path.join(out, f'still_{float(ts):05.2f}s.png'))
            print('saved', ts)
    elif mode == 'render':
        render_video(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 27)
