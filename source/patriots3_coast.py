#!/usr/bin/env python3
"""Patriots 3, shot 1: the coast from high above, one painted shot in moving layers (film-quality rule 39: one
camera, so 2D). Refs: air-1..5 (D-Day from the air: grey sea, white wakes, smoke along the shore), landers-3 (packed
craft from above), landers-4 (craft in a ragged line), lander-pov-* (the bluffs from the sea).

Back to front: the grey sky and haze; Normandy fields and hedgerows; the black cliffs, flashing with machine-gun fire
(lumpy one-frame flashes, short tracer streaks down at the beach); the beach (dry sand, wet sand, hedgehogs at the
waterline) with artillery bursts throwing up sand and spray; drifting smoke; the sea with surf lines; six landing craft
packed with helmets creeping in, their white wakes behind; two warships at the bottom corners.
The camera drifts a little to the right as the craft come in (life, rule 4).

    python3 source/patriots3_coast.py OUT.jpg [T]
"""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import sets as S                 # noqa: E402
import patriots3_plan as PL      # noqa: E402
from ed import INK               # noqa: E402
from satire_style import rough   # noqa: E402

SKY, HAZE = (200, 202, 200), (178, 182, 180)
SEA, SEA_D, SEA_L, SURF = (92, 108, 114), (74, 88, 96), (118, 132, 136), (230, 232, 226)
SAND, WET, SAND_D = (192, 180, 152), (150, 140, 122), (168, 156, 130)
CLIFF, CLIFF_D, CLIFF_L = (40, 40, 44), (26, 26, 30), (64, 64, 66)
GRASS = (98, 112, 70)
HULL, HULL_D, HULL_L = (104, 112, 114), (72, 78, 82), (132, 138, 140)
HELMET, HELMET_D = (92, 100, 72), (68, 74, 54)
FLASH, FLASH_C = (255, 196, 80), (255, 244, 200)
SMOKE, SMOKE_D = (172, 170, 166), (128, 126, 124)
T0, T1 = 0.0, 3.6
CLIFF_Z, CLIFF_H = 0.0, 34.0                        # the cliff foot along z = 0, the tops 34 m up (Pointe du Hoc ~30 m)
CRAFT = [(-48, 130, 0.0), (-34, 152, 0.6), (-20, 120, 1.1), (-6, 158, 0.3), (8, 134, 0.8), (22, 162, 1.4)]
BURSTS = [(-0.6, -60, 40, 'sand'), (-0.3, 70, 88, 'spray'), (0.15, -120, 46, 'sand'), (0.4, 0, 104, 'spray'),
          (0.55, 40, 70, 'spray'), (0.9, 110, 52, 'sand'), (1.1, -90, 92, 'spray'), (1.35, -30, 98, 'spray'),
          (1.7, 60, 40, 'sand'), (1.95, -10, 34, 'sand'), (2.15, -140, 84, 'spray'), (2.5, 10, 50, 'sand'),
          (2.75, -60, 112, 'spray'), (2.95, 90, 110, 'spray'), (3.25, -80, 60, 'sand')]


def cam(t):
    c = PL.CAMS['s1']
    k = (t - T0) / (T1 - T0)
    pos = (c['pos'][0] + 6 * k, c['pos'][1], c['pos'][2] - 4 * k)
    return S.Cam(pos, (c['look'][0] + 5 * k, c['look'][1], c['look'][2] - 3 * k), focal=c['focal'])


def _blob(cx, cy, r, seed, n=11, sq=0.85):
    rng = np.random.default_rng(abs(int(seed)))
    return [(cx + r * rng.uniform(0.75, 1.15) * math.cos(a), cy + r * sq * rng.uniform(0.75, 1.15) * math.sin(a))
            for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]


def land(img, cm, p):
    P = lambda x, y, z: cm.project((x, y, z))[0]
    p.poly([P(-4000, CLIFF_H, CLIFF_Z), P(4000, CLIFF_H, CLIFF_Z), P(4000, CLIFF_H, -9000), P(-4000, CLIFF_H, -9000)],
           GRASS, None)
    rng = np.random.default_rng(3)
    for r in range(9):                                 # fields and hedgerows to the haze
        z0 = CLIFF_Z - 30 - r * (90 + r * 40)
        z1 = z0 - (80 + r * 40)
        x = -900 - rng.uniform(0, 200)
        while x < 900:
            w = rng.uniform(140, 260) * (1 + r * 0.3)
            col = ((112, 128, 78), (132, 140, 86), (90, 108, 66), (150, 146, 96), (120, 118, 80))[int(rng.integers(5))]
            p.poly(rough([P(x, CLIFF_H, z0), P(x + w, CLIFF_H, z0), P(x + w - 6, CLIFF_H, z1), P(x - 4, CLIFF_H, z1)],
                         2, int(x) + r * 97), col, (62, 76, 46), 1.6)
            x += w + 4
    hz = cm.project((cm.pos[0], 0, -60000))[0][1]       # the haze over the far fields
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    q = S.pen(lay)
    for i in range(4):
        y0 = hz + i * 26
        q.poly([(-20, -20), (1100, -20), (1100, y0), (-20, y0)], HAZE + (70,), None)
    img.alpha_composite(lay)


def cliffs(img, cm, p, t):
    P = lambda x, y, z: cm.project((x, y, z))[0]
    xs = np.arange(-700, 701, 25)
    top = [P(x, CLIFF_H + 5 * math.sin(x * 0.021) + 3 * math.sin(x * 0.07), CLIFF_Z) for x in xs]
    p.poly([P(-700, 0, CLIFF_Z + 6)] + top + [P(700, 0, CLIFF_Z + 6)], CLIFF, INK, 2.0)
    for x in xs[::2]:                                  # the rock's dark gullies (a black cliff, never a flat band)
        a = P(x + 4, CLIFF_H - 4, CLIFF_Z + 1)
        b = P(x - 3, 2, CLIFF_Z + 5)
        p.line([a, b], CLIFF_D, 2.0)
    for x in xs[1::3]:
        a = P(x, CLIFF_H - 2, CLIFF_Z + 0.5)
        p.line([a, P(x + 6, CLIFF_H * 0.6, CLIFF_Z + 2)], CLIFF_L, 1.4)
    f = int(t * 12)                                    # gunfire: lumpy one-frame flashes along the cliff face
    rng = np.random.default_rng(1000 + f)
    for i in range(9):
        x = rng.uniform(-420, 420)
        y = rng.uniform(CLIFF_H * 0.35, CLIFF_H * 0.85)
        (X, Y), k = cm.project((x, y, CLIFF_Z + 3))
        r = max(6.0, 2.4 * k)
        p.poly(_blob(X, Y, r, f * 31 + i, 9), FLASH, INK, 1.0)
        p.poly(_blob(X, Y, r * 0.5, f * 31 + i + 5, 9), FLASH_C, None)
        if i % 2 == 0:                                 # the tracer streak down at the beach and the water
            tx, tz = x + rng.uniform(-40, 40), rng.uniform(30, 160)
            u = rng.uniform(0.2, 0.8)
            a = (x + (tx - x) * u, y * (1 - u), CLIFF_Z + 3 + (tz - 3) * u)
            b = (x + (tx - x) * (u + 0.12), y * (1 - u - 0.12), CLIFF_Z + 3 + (tz - 3) * (u + 0.12))
            q0, q1 = cm.project(a)[0], cm.project(b)[0]
            p.line([q0, q1], (255, 236, 150), 2.4)


def beach(img, cm, p, t):
    P = lambda x, y, z: cm.project((x, y, z))[0]
    xs = np.arange(-900, 901, 60)
    p.poly([P(x, 0, CLIFF_Z + 6 + 3 * math.sin(x * 0.05)) for x in xs] +
           [P(x, 0, 62 + 4 * math.sin(x * 0.03)) for x in xs[::-1]], SAND, INK, 2.0)
    p.poly([P(x, 0, 52 + 4 * math.sin(x * 0.03)) for x in xs] +
           [P(x, 0, 78 + 5 * math.sin(x * 0.02 + 1)) for x in xs[::-1]], WET, None)
    rng = np.random.default_rng(8)
    for i in range(30):                                # shell craters pocking the sand
        x, z = rng.uniform(-500, 500), rng.uniform(14, 56)
        (X, Y), k = cm.project((x, 0, z))
        p.poly(_blob(X, Y, 2.6 * k, i, 9, 0.5), SAND_D, None)
    for i in range(40):                                # hedgehogs at the waterline: little dark crosses
        x, z = rng.uniform(-520, 520), rng.uniform(62, 86)
        (X, Y), k = cm.project((x, 0, z))
        r = max(2.0, 1.2 * k)
        p.line([(X - r, Y - r), (X + r, Y + r * 0.4)], (40, 36, 34), 1.6)
        p.line([(X + r, Y - r), (X - r, Y + r * 0.4)], (40, 36, 34), 1.6)


def sea(img, cm, p, t):
    P = lambda x, y, z: cm.project((x, y, z))[0]
    p.poly([P(-3000, 0, 70), P(3000, 0, 70), P(3000, 0, 2000), P(-3000, 0, 2000)], SEA, None)
    for i in range(4):                                 # surf lines rolling in
        z = 78 + i * 9 + ((t * 3.0) % 9)
        pts = [P(x, 0, z + 2 * math.sin(x * 0.04 + i)) for x in np.arange(-900, 901, 50)]
        p.line(pts, SURF if i < 2 else SEA_L, 3.0 if i < 2 else 2.0)
    rng = np.random.default_rng(4)
    for i in range(36):                                # chop on the water
        x, z = rng.uniform(-600, 600), rng.uniform(110, 420)
        a, b = P(x, 0, z), P(x + rng.uniform(6, 16), 0, z)
        p.line([a, b], SEA_D, 1.6)


def burst(img, cm, p, t, t0, x, z, kind):
    """An artillery burst: one frame of flash, then a lumpy column of sand (or white spray on the water) thrown up and
    falling back over about a second; a darker stain stays on the sand."""
    u = t - t0
    if u < 0:
        return
    (X, Y), k = cm.project((x, 0, z))
    if kind == 'sand':
        p.poly(_blob(X, Y, 3.2 * k, int(x), 9, 0.5), SAND_D, None)
    if u > 1.3:
        return
    if u < 0.09:
        p.poly(_blob(X, Y - 2 * k, 4 * k, int(x) + 2, 11), FLASH, INK, 1.4)
        p.poly(_blob(X, Y - 2 * k, 2 * k, int(x) + 3, 11), FLASH_C, None)
    h = 26 * math.sin(math.pi * min(1.0, u / 1.3)) ** 0.6
    col, dark = ((214, 202, 172), (156, 144, 120)) if kind == 'sand' else ((236, 240, 238), (170, 184, 188))
    rng = np.random.default_rng(abs(int(x * 13 + z)))
    grow = min(1.0, u * 2.5)
    for i in range(4):                                 # a lumpy plume (ref blast-1): blobs stacked up the column,
        f = i / 3                                      # the top ones biggest, each its own size and lean
        c = cm.project((x + rng.uniform(-2, 2) * f, h * f * 0.85, z))[0]
        r = (4.5 + 6.5 * f) * grow * k * rng.uniform(0.85, 1.15)
        if r < 1:
            continue
        pts = _blob(c[0], c[1], r, int(rng.integers(1 << 20)), 11, 0.8)
        p.poly(pts, dark, INK, 1.4)
        p.poly([(c[0] + (px - c[0]) * 0.72 - r * 0.12, c[1] + (py - c[1]) * 0.72 - r * 0.15) for px, py in pts], col, None)


def craft(img, cm, p, t, x0, z0, ph):
    """An LCVP (11 m x 3.2 m) from above: the grey box hull, the ramp at the bow (towards the beach), the coxswain's
    stern, and inside it packed shoulder to shoulder with helmets (landers-3); the white wake behind."""
    z = z0 - 4.2 * t                                   # creeping in at about 8 knots
    bob = 0.15 * math.sin(t * 3 + ph)
    P = lambda dx, dy, dz: cm.project((x0 + dx, dy, z + dz))[0]
    wake = [P(-1.7, 0, 10.5), P(1.7, 0, 10.5), P(3.6 + ph, 0, 30), P(0.4, 0, 22), P(-3.6 - ph, 0, 30)]
    p.poly(rough(wake, 3, abs(int(x0))), SEA_L, None)                # the wake: churned paler water, a V of foam
    for sg in (-1, 1):
        p.line([P(sg * 1.7, 0, 10.6), P(sg * (2.6 + ph * 0.5), 0, 20), P(sg * (3.6 + ph), 0, 30)], SURF, 2.4)
    p.poly([P(-0.9, 0, 11), P(0.9, 0, 11), P(1.3, 0, 17), P(-1.3, 0, 17)], SURF, None)
    p.poly([P(-2.0, 0, -0.6), P(2.0, 0, -0.6), P(2.4, 0, 0.6), P(-2.4, 0, 0.6)], SURF, None)   # the bow wave
    hull = [P(-1.6, 1.4 + bob, 0), P(1.6, 1.4 + bob, 0), P(1.6, 1.4 + bob, 11), P(-1.6, 1.4 + bob, 11)]
    p.poly(hull, HULL, INK, 2.0)
    inner = [P(-1.3, 1.4 + bob, 1.2), P(1.3, 1.4 + bob, 1.2), P(1.3, 1.4 + bob, 9.0), P(-1.3, 1.4 + bob, 9.0)]
    p.poly(inner, HULL_D, INK, 1.4)
    p.poly([P(-1.6, 1.4 + bob, 0), P(1.6, 1.4 + bob, 0), P(1.6, 1.4 + bob, 1.2), P(-1.6, 1.4 + bob, 1.2)], HULL_L, INK, 1.6)
    p.poly([P(-0.9, 1.6 + bob, 9.2), P(0.9, 1.6 + bob, 9.2), P(0.9, 1.6 + bob, 10.6), P(-0.9, 1.6 + bob, 10.6)],
           HULL_D, INK, 1.4)
    rng = np.random.default_rng(abs(int(x0 * 7 + z0)))
    for r in range(9):                                 # 36 men: four across, nine deep, never in a perfect grid
        for c in range(4):
            q = P(-0.95 + c * 0.63 + rng.uniform(-0.12, 0.12), 1.5 + bob, 1.55 + r * 0.85 + rng.uniform(-0.15, 0.15))
            (_, k) = cm.project((x0, 1.5, z + 5))
            rr = max(1.6, 0.3 * k)
            p.ell(q[0], q[1], rr, rr * 0.9, HELMET if (r + c) % 3 else HELMET_D, INK, 1.0)


def ships(img, cm, p, t):
    """Two warships at the bottom corners, on their way past (life; refs air-1, -2)."""
    for x0, z0, d in ((-120, 300, 1), (110, 320, -1)):
        x = x0 + d * 2.0 * t
        P = lambda dx, dz: cm.project((x + dx, 2.0, z0 + dz))[0]
        p.poly([P(-6 * d, 0), P(60 * d, -4), P(68 * d, 0), P(60 * d, 4), P(-6 * d, 0)], (96, 102, 106), INK, 2.0)
        p.poly([P(14 * d, -2), P(34 * d, -2), P(34 * d, 2), P(14 * d, 2)], (72, 76, 80), INK, 1.6)
        p.poly(rough([P(-6 * d, 0), P(-30 * d, -6), P(-60 * d, -2), P(-30 * d, 6)], 3, x0), SURF, None)


def smoke(img, cm, t):
    """Flat grey smoke drifting along the shore and up off the bursts (refs air-3, -4)."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    p = S.pen(lay)
    rng = np.random.default_rng(6)
    for i in range(14):
        x = rng.uniform(-400, 400) + 6 * t
        z = rng.uniform(8, 60)
        y = rng.uniform(4, 28)
        (X, Y), k = cm.project((x, y, z))
        r = rng.uniform(8, 16) * k
        a = int(rng.uniform(80, 130))
        p.poly(_blob(X, Y, r, i, 13, 0.4), SMOKE_D + (a,), None)
        p.poly(_blob(X - r * 0.1, Y - r * 0.08, r * 0.75, i + 40, 13, 0.4), SMOKE + (a,), None)
    img.alpha_composite(lay)


def picture(t):
    cm = cam(t)
    img = B.canvas(SKY)
    p = S.pen(img)
    land(img, cm, p)
    sea(img, cm, p, t)
    beach(img, cm, p, t)
    cliffs(img, cm, p, t)
    for b in BURSTS:
        if b[3] == 'sand':
            burst(img, cm, p, t, *b)
    smoke(img, cm, t)
    for b in BURSTS:
        if b[3] == 'spray':
            burst(img, cm, p, t, *b)
    for x0, z0, ph in sorted(CRAFT, key=lambda c: c[1]):
        craft(img, cm, p, t, x0, z0, ph)
    ships(img, cm, p, t)
    return img


if __name__ == '__main__':
    B.SS = 1
    picture(float(sys.argv[2]) if len(sys.argv) > 2 else 1.8).convert('RGB').save(sys.argv[1], quality=88)
