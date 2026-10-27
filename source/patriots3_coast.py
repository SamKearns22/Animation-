#!/usr/bin/env python3
"""Patriots 3, shot 1: the coast from high above, the hook. One painted shot in moving layers (film-quality rule 39:
one camera, so 2D, drawn through the plan's camera). Refs: air-1..5 (D-Day from the air: grey sea, white wakes, smoke
along the shore, the 1944 beach), landers-3, -4 (packed craft, a ragged line), lander-pov-* (the bluffs from the sea),
bunker-1..4 (the casemates), blast-1 (a shell burst: a dark churning cloud).

Sam's note 7 (27 Oct): concrete redoubts on the cliffs the fire comes from; more texture; bullets skipping in the water;
the boats on slightly different headings; craters and scorch marks where shells land; more beach defences; ripples in
the wakes; explosions of different kinds, less cartoony; anything else from D-Day. So, back to front:
  sky with low cloud and smoke from inland; fields and hedgerows; the cliff-top casemates and MG pits; the black cliff
  (strata, gullies, ledges with grass); shingle at the foot; sand with ripples, pools, old and new craters and scorch;
  wire, mined stakes, hedgehogs, steel gates in the shallows; the sea with swell, chop and surf; bullets walking across
  the water; shell bursts of three kinds (sand thrown up then drifting dust; a tall white water column collapsing into
  a foam ring; naval shells raising black smoke off the cliff top); six craft on their own headings with rippling
  wakes; warships with barrage balloons; a rocket salvo; two fighter-bombers with invasion stripes; the casemates'
  muzzle flashes and tracers last, so the fire always reads.
Smoke and dust are soft clusters of overlapping round billows, see-through, no outline (flat, never a glow); flashes
are lumpy with an outline (house style, never a star).

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

SKY, SKY_L, SKY_D, HAZE = (200, 202, 200), (214, 216, 214), (178, 182, 182), (178, 182, 180)
SEA, SEA_D, SEA_L, SURF = (92, 108, 114), (74, 88, 96), (118, 132, 136), (230, 232, 226)
SAND, SAND_L, WET, SAND_D, POOL = (192, 180, 152), (206, 196, 170), (150, 140, 122), (168, 156, 130), (128, 142, 144)
SHINGLE, SHINGLE_D = (138, 134, 126), (104, 100, 94)
CLIFF, CLIFF_D, CLIFF_L, CLIFF_M = (40, 40, 44), (24, 24, 28), (70, 70, 72), (54, 54, 58)
GRASS, GRASS_D = (98, 112, 70), (72, 86, 52)
CONC, CONC_D, SLIT = (150, 148, 138), (112, 110, 102), (20, 20, 22)
HULL, HULL_D, HULL_L = (104, 112, 114), (72, 78, 82), (132, 138, 140)
HELMET, HELMET_D = (92, 100, 72), (68, 74, 54)
IRON, WOOD = (44, 40, 38), (96, 78, 56)
FLASH, FLASH_C = (255, 196, 80), (255, 244, 200)
DUST, DUST_D = (176, 162, 136), (132, 120, 100)
SMOKE, SMOKE_D, BLACK = (176, 174, 170), (130, 128, 126), (52, 50, 50)
SCORCH = (62, 54, 46)
T0, T1 = 0.0, 3.6
CLIFF_Z, CLIFF_H = 0.0, 34.0                        # the cliff foot along z = 0, the tops 34 m up (Pointe du Hoc ~30 m)
# the six craft: x, z at t = 0, bob phase, heading (degrees off straight in: not all on one line, Sam)
CRAFT = [(-48, 130, 0.0, 5.0), (-34, 152, 0.6, -4.0), (-20, 120, 1.1, 1.5), (-6, 158, 0.3, 7.0),
         (8, 134, 0.8, -6.0), (22, 162, 1.4, 2.5)]
SPEED = 4.2                                         # metres a second, about 8 knots
# casemates on the cliff (x, how far down the face their slit is): the fire comes from these (Sam)
REDOUBTS = [(-104, 3.0), (-62, 6.5), (-18, 2.5), (26, 5.0), (70, 3.5)]
MG_PITS = [(-84, 6.0), (6, 7.0), (48, 5.0)]         # open sandbagged MG pits just behind the edge (x, back from it)
# shell bursts: (start, x, z, kind, size); kinds: 'sand' (beach), 'spray' (water), 'smoke' (naval shells on the cliff
# top). Some start before the shot so it opens mid-battle.
BURSTS = [(-2.2, -96, -6, 'smoke', 1.2), (-1.4, 40, -8, 'smoke', 1.0), (-0.9, -60, 40, 'sand', 1.0),
          (-0.4, 70, 88, 'spray', 0.9), (0.2, -120, 46, 'sand', 1.3), (0.45, 0, 104, 'spray', 1.1),
          (0.7, 30, 22, 'sand', 0.8), (0.95, 110, 52, 'sand', 1.0), (1.15, -90, 92, 'spray', 1.3),
          (1.3, -10, -5, 'smoke', 0.9), (1.5, -30, 98, 'spray', 0.8), (1.75, 60, 40, 'sand', 1.2),
          (2.05, -140, 84, 'spray', 1.0), (2.3, 10, 50, 'sand', 0.9), (2.6, -60, 112, 'spray', 1.2),
          (2.85, 90, 110, 'spray', 0.8), (3.1, -80, 30, 'sand', 1.4), (3.35, 76, -7, 'smoke', 1.1)]
OLD_CRATERS = [(-140, 28, 1.2), (-110, 52, 0.9), (-75, 18, 1.1), (-38, 44, 0.8), (-5, 30, 1.3), (18, 58, 1.0),
               (52, 26, 0.9), (84, 48, 1.2), (120, 34, 1.0), (-160, 60, 0.8), (140, 20, 1.1)]
# machine-gun fire walking across the water: (redoubt, start, end, from (x, z), to (x, z))
MG_STREAMS = [(1, -0.2, 1.1, (-70, 120), (-30, 138)), (3, 0.4, 1.6, (30, 150), (-4, 128)),
              (0, 1.0, 2.3, (-60, 96), (-40, 140)), (4, 1.6, 2.9, (50, 112), (14, 150)),
              (2, 2.2, 3.6, (-30, 148), (10, 120)), (3, 2.9, 3.6, (40, 100), (20, 140))]
ROCKETS = [(1.25 + 0.04 * i, -110 + 19 * i + (i % 3) * 6, 18 + (i * 7) % 30) for i in range(12)]   # (launch, x, z)
PLANES = [(1.0, 22.0, 150.0), (1.3, 18.0, 168.0)]  # (time over the middle, height, z): P-47s low over the craft


def cam(t):
    c = PL.CAMS['s1']
    k = (t - T0) / (T1 - T0)
    pos = (c['pos'][0] + 6 * k, c['pos'][1], c['pos'][2] - 4 * k)
    return S.Cam(pos, (c['look'][0] + 5 * k, c['look'][1], c['look'][2] - 3 * k), focal=c['focal'])


def _rng(*seed):
    return np.random.default_rng(abs(hash(tuple(int(v * 100) for v in seed))) % (1 << 31))


def _blob(cx, cy, r, seed, n=11, sq=0.85):
    rng = np.random.default_rng(abs(int(seed)))
    return [(cx + r * rng.uniform(0.75, 1.15) * math.cos(a), cy + r * sq * rng.uniform(0.75, 1.15) * math.sin(a))
            for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]


def billow(p, X, Y, r, col, a, seed, n=7, sq=0.9, rise=0.0):
    """A soft cluster of round billows (smoke, dust, spray): overlapping circles of different sizes making a
    cauliflower outline, see-through, no outline; a lighter cluster up and to the left for the lit side."""
    if r < 1.0 or a <= 3:
        return
    rng = np.random.default_rng(abs(int(seed)))
    dark = tuple(int(v * 0.82) for v in col)
    pts = []
    for i in range(n):
        ang = rng.uniform(0, 2 * math.pi)
        d = r * rng.uniform(0.0, 0.62)
        rr = r * rng.uniform(0.42, 0.7)
        pts.append((X + d * math.cos(ang), Y + d * sq * math.sin(ang) - rise * r * (i / n), rr))
    for x, y, rr in pts:
        p.ell(x, y, rr, rr * sq, dark + (a,), None)
    for x, y, rr in pts[: max(2, n // 2)]:
        p.ell(x - rr * 0.18, y - rr * 0.22, rr * 0.72, rr * 0.72 * sq, col + (a,), None)


def _flash(p, X, Y, r, seed):
    p.poly(_blob(X, Y, r, seed, 11), FLASH, INK, 1.2)
    p.poly(_blob(X, Y, r * 0.5, seed + 5, 11), FLASH_C, None)


# ------------------------------------------------------------------------------------------------ back layers
def sky(img, cm, p, t):
    hz = cm.project((cm.pos[0], 0, -60000))[0][1]
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    q = S.pen(lay)
    rng = np.random.default_rng(2)
    for i in range(7):                                 # low cloud streaks, drifting
        y = hz - rng.uniform(20, 260)
        x = rng.uniform(-300, 900) + 8 * t
        w, h = rng.uniform(300, 700), rng.uniform(10, 26)
        q.poly(rough([(x, y), (x + w * 0.5, y - h), (x + w, y), (x + w * 0.5, y + h * 0.6)], 6, i),
               (SKY_L if i % 2 else SKY_D) + (120,), None)
    img.alpha_composite(lay)


def land(img, cm, p, t):
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
                         2, abs(int(x)) + r * 97), col, (62, 76, 46), 1.6)
            if r < 4 and rng.uniform() < 0.5:          # a hedgerow of dark trees along the field's edge
                for k in range(6):
                    c = P(x + w * k / 6, CLIFF_H + 2, z0)
                    p.ell(c[0], c[1], 5 - r, 3.5 - r * 0.6, (58, 72, 44), None)
            x += w + 4
    for r in range(3):                                 # shell holes on the cliff top behind the edge
        for k in range(5):
            c, kk = cm.project((rng.uniform(-150, 120), CLIFF_H, -rng.uniform(8, 60)))
            p.poly(_blob(c[0], c[1], 2.4 * kk, r * 10 + k, 9, 0.45), (88, 80, 60), None)
    hz = cm.project((cm.pos[0], 0, -60000))[0][1]       # the haze over the far fields
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    q = S.pen(lay)
    for i in range(4):
        y0 = hz + i * 26
        q.poly([(-20, -20), (1100, -20), (1100, y0), (-20, y0)], HAZE + (70,), None)
    for i, (x, z) in enumerate([(-260, -900), (60, -1400), (220, -700)]):   # smoke rising from inland fighting
        for k in range(5):
            (X, Y), kk = cm.project((x + 6 * k + 3 * t, CLIFF_H + 12 + k * 14, z))
            billow(q, X, Y, (8 + 3 * k) * kk, SMOKE_D, 90 - 12 * k, i * 20 + k, 6)
    img.alpha_composite(lay)


def redoubts(img, cm, p, t):
    """Concrete casemates in the cliff top (refs bunker-1..4): a grey box set into the edge under an earth cover, a
    dark firing slit facing the sea; open MG pits ringed with sandbags behind the edge."""
    P = lambda x, y, z: cm.project((x, y, z))[0]
    for i, (x, d) in enumerate(REDOUBTS):
        top = CLIFF_H + 1.5
        y0 = CLIFF_H - d - 5.0
        w = 6.5
        p.poly(rough([P(x - w - 3, top + 1.5, -2), P(x + w + 3, top + 1.5, -2), P(x + w + 5, CLIFF_H, 1),
                      P(x - w - 5, CLIFF_H, 1)], 3, i), GRASS_D, INK, 1.4)          # the earth cover
        p.poly([P(x - w, top, 0.6), P(x + w, top, 0.6), P(x + w, y0, 0.6), P(x - w, y0, 0.6)], CONC, INK, 1.8)
        p.poly([P(x - w, top, 0.6), P(x + w, top, 0.6), P(x + w, top, -3), P(x - w, top, -3)], CONC_D, INK, 1.4)
        sy = y0 + 2.2
        p.poly([P(x - 3.6, sy + 1.3, 0.7), P(x + 3.6, sy + 1.3, 0.7), P(x + 3.0, sy, 0.7), P(x - 3.0, sy, 0.7)],
               SLIT, None)
        for k in (-1, 1):                              # board marks, a chipped corner
            p.line([P(x - w, y0 + 1.2 + k * 0.8, 0.62), P(x + w, y0 + 1.2 + k * 0.8, 0.62)], CONC_D, 1.0)
    for i, (x, back) in enumerate(MG_PITS):
        c, k = cm.project((x, CLIFF_H, -back))
        for a in np.linspace(0, 2 * math.pi, 10, endpoint=False):
            q = (c[0] + 2.2 * k * math.cos(a), c[1] + 1.0 * k * math.sin(a))
            p.ell(q[0], q[1], 0.7 * k, 0.4 * k, (168, 152, 112), INK, 1.0)
        p.ell(c[0], c[1], 1.2 * k, 0.5 * k, (40, 38, 34), None)


def slit_of(i):
    x, d = REDOUBTS[i]
    return (x, CLIFF_H - d - 5.0 + 2.8, 1.0)


def cliffs(img, cm, p, t):
    P = lambda x, y, z: cm.project((x, y, z))[0]
    xs = np.arange(-700, 701, 20)
    edge = lambda x: CLIFF_H + 4 * math.sin(x * 0.021) + 2.4 * math.sin(x * 0.07 + 1)
    top = [P(x, edge(x), CLIFF_Z) for x in xs]
    p.poly([P(-700, 0, CLIFF_Z + 8)] + top + [P(700, 0, CLIFF_Z + 8)], CLIFF, INK, 2.0)
    rng = np.random.default_rng(11)
    for i in range(70):                                # rock faces: lighter and darker facets, hand cut
        x = rng.uniform(-260, 260)
        y = rng.uniform(4, CLIFF_H - 6)
        w, h = rng.uniform(4, 12), rng.uniform(3, 9)
        (X, Y), k = cm.project((x, y, CLIFF_Z + 1.5))
        p.poly(_blob(X, Y, w * 0.5 * k, 400 + i, 9, h / w), ((46, 46, 50), (36, 36, 40), (52, 50, 52))[i % 3], None)
    for k in range(6):                                 # strata: broken horizontal bands
        y = 6 + k * 4.6
        seg = []
        for x in xs:
            if rng.uniform() < 0.12:
                if len(seg) > 1:
                    p.line(seg, CLIFF_L, 1.4)
                seg = []
            else:
                seg.append(P(x, y + 0.8 * math.sin(x * 0.05 + k), CLIFF_Z + 0.5))
        if len(seg) > 1:
            p.line(seg, CLIFF_L, 1.4)
    for x in xs[::2]:                                  # gullies
        p.line([P(x + 4, edge(x) - 4, CLIFF_Z + 1), P(x - 3, 2, CLIFF_Z + 6)], CLIFF_D, 2.0)
    fringe = []                                        # the grass lip over the edge, ragged
    for x in xs:
        fringe.append(P(x, edge(x) + 0.3, CLIFF_Z - 0.5))
    for x in xs[::-1]:
        fringe.append(P(x, edge(x) - 1.2 - 0.8 * abs(math.sin(x * 0.3)), CLIFF_Z + 0.4))
    p.poly(fringe, GRASS, INK, 1.4)
    for i in range(30):                                # tufts on the ledges
        x, y = rng.uniform(-240, 240), rng.uniform(8, CLIFF_H - 8)
        c, k = cm.project((x, y, CLIFF_Z + 2))
        p.ell(c[0], c[1], 1.2 * k, 0.5 * k, GRASS_D, None)
    scree = [P(x, 3 + 2 * abs(math.sin(x * 0.11)), CLIFF_Z + 3) for x in xs] + \
            [P(x, 0, CLIFF_Z + 10 + 2 * math.sin(x * 0.07)) for x in xs[::-1]]      # rock fall at the foot
    p.poly(scree, (78, 76, 74), INK, 1.4)
    for i in range(60):
        c, k = cm.project((rng.uniform(-300, 300), 0.5, rng.uniform(CLIFF_Z + 4, CLIFF_Z + 9)))
        p.ell(c[0], c[1], rng.uniform(0.5, 1.2) * k, 0.4 * k, (96, 92, 88), INK, 0.8)


# ------------------------------------------------------------------------------------------------ the beach
def beach(img, cm, p, t):
    P = lambda x, y, z: cm.project((x, y, z))[0]
    xs = np.arange(-900, 901, 40)
    p.poly([P(x, 0, CLIFF_Z + 9 + 2 * math.sin(x * 0.05)) for x in xs] +
           [P(x, 0, 62 + 4 * math.sin(x * 0.03)) for x in xs[::-1]], SAND, INK, 2.0)
    p.poly([P(x, 0, CLIFF_Z + 9 + 2 * math.sin(x * 0.05)) for x in xs] +
           [P(x, 0, CLIFF_Z + 15 + 1.5 * math.sin(x * 0.09)) for x in xs[::-1]], SHINGLE, None)   # the shingle bank
    rng = np.random.default_rng(8)
    for i in range(140):
        c, k = cm.project((rng.uniform(-300, 300), 0, rng.uniform(CLIFF_Z + 9, CLIFF_Z + 15)))
        p.ell(c[0], c[1], 0.35 * k, 0.25 * k, SHINGLE_D, None)
    p.poly([P(x, 0, 52 + 4 * math.sin(x * 0.03)) for x in xs] +
           [P(x, 0, 78 + 5 * math.sin(x * 0.02 + 1)) for x in xs[::-1]], WET, None)
    for k in range(22):                                # ripples left by the tide in the sand
        z = 20 + k * 2.6
        seg = [P(x, 0, z + 0.6 * math.sin(x * 0.4 + k)) for x in np.arange(-300, 300, 8)]
        p.line(seg, SAND_L if z < 52 else (162, 152, 132), 1.0)
    for i in range(9):                                 # tide pools on the wet sand
        x, z = rng.uniform(-200, 200), rng.uniform(56, 74)
        c, k = cm.project((x, 0, z))
        p.poly(_blob(c[0], c[1], rng.uniform(3, 7) * k, 200 + i, 11, 0.35), POOL, (110, 120, 120), 1.0)
    for x, z, s in OLD_CRATERS:                       # the morning's shelling, already there
        crater(p, cm, x, z, s, 300 + int(x))
    for b in BURSTS:                                   # each new hit leaves its crater and scorch (Sam)
        t0, x, z, kind, size = b
        if kind == 'sand' and t >= t0 + 0.15:
            crater(p, cm, x, z, size, int(x * 3 + z))


def crater(p, cm, x, z, size, seed):
    """A shell crater: a blackened scorch round it, the dark hole, a lighter rim of thrown sand."""
    (X, Y), k = cm.project((x, 0, z))
    rng = np.random.default_rng(abs(int(seed)))
    sc = [(X + 4.5 * size * k * rng.uniform(0.45, 1.25) * math.cos(a), Y + 2.0 * size * k * rng.uniform(0.45, 1.25)
           * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 17, endpoint=False)]
    p.poly(sc, (128, 114, 92), None)                   # the blackened, splashed sand: ragged
    p.poly([(X + (x - X) * 0.6, Y + (y - Y) * 0.6) for x, y in sc], SCORCH, None)
    for i in range(7):                                 # clods of thrown sand round it
        a = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(4.5, 6.5) * size * k
        p.ell(X + d * math.cos(a), Y + d * 0.45 * math.sin(a), 0.35 * k, 0.25 * k, SAND_D, None)
    p.ell(X, Y, 1.3 * size * k, 0.6 * size * k, (54, 48, 42), None)   # the hole


def defences(img, cm, p, t):
    """Rommel's beach defences: coiled wire along the top, mined stakes leaning to sea, hedgehogs, and steel gates
    (Element C) in the shallows."""
    P = lambda x, y, z: cm.project((x, y, z))[0]
    rng = np.random.default_rng(5)
    for row, z in ((0, 16.5), (1, 19)):                # barbed wire: chains of loops
        for x in np.arange(-260, 260, 1.6):
            c, k = cm.project((x + row * 0.8, 0.6, z))
            p.ell(c[0], c[1], 0.8 * k, 0.6 * k, None, (60, 56, 52), 1.0)
    for i in range(46):                                # stakes with a Teller mine on top, leaning to sea
        x, z = rng.uniform(-260, 220), rng.uniform(34, 56)
        a, b = P(x, 0, z), P(x, 2.6, z + 1.4)
        p.line([a, b], WOOD, 2.6)
        c, k = cm.project((x, 2.7, z + 1.5))
        p.ell(c[0], c[1], 0.45 * k, 0.3 * k, IRON, INK, 0.8)
    for i in range(60):                                # Czech hedgehogs: three crossed steel beams
        x, z = rng.uniform(-280, 240), rng.uniform(56, 84)
        c = np.array((x, 0.9, z))
        for k, (dx, dy, dz) in enumerate(((1, 0.8, 0.3), (-1, 0.8, 0.3), (0.2, 0.8, -1))):
            d = np.array((dx, dy, dz)) / np.linalg.norm((dx, dy, dz)) * 1.1
            p.line([P(*(c - d)), P(*(c + d))], IRON, 2.2)
    for i in range(10):                                # Element C steel gates, standing in the shallows
        x, z = rng.uniform(-220, 180), rng.uniform(78, 92)
        w, h = 3.0, 2.6
        q = [P(x - w / 2, 0, z), P(x + w / 2, 0, z), P(x + w / 2, h, z), P(x - w / 2, h, z)]
        p.poly(q, None, IRON, 1.8)
        p.line([q[0], q[2]], IRON, 1.4)
        p.line([q[1], q[3]], IRON, 1.4)


# ------------------------------------------------------------------------------------------------ the sea
def sea(img, cm, p, t):
    P = lambda x, y, z: cm.project((x, y, z))[0]
    p.poly([P(-3000, 0, 70), P(3000, 0, 70), P(3000, 0, 2000), P(-3000, 0, 2000)], SEA, None)
    for k in range(12):                                # swell: long faint bands, rolling in
        z = 90 + k * 14 - (t * 2.0) % 14
        band = [P(x, 0, z + 2 * math.sin(x * 0.02 + k)) for x in np.arange(-500, 501, 40)] + \
               [P(x, 0, z + 5 + 2 * math.sin(x * 0.02 + k)) for x in np.arange(500, -501, -40)]
        p.poly(band, SEA_D if k % 2 else (100, 116, 120), None)
    for i in range(4):                                 # surf lines rolling in
        z = 78 + i * 9 + ((t * 3.0) % 9)
        pts = [P(x, 0, z + 2 * math.sin(x * 0.04 + i)) for x in np.arange(-900, 901, 40)]
        p.line(pts, SURF if i < 2 else SEA_L, 3.0 if i < 2 else 2.0)
    rng = np.random.default_rng(4)
    for i in range(90):                                # chop
        x, z = rng.uniform(-300, 300), rng.uniform(95, 260)
        a, b = P(x, 0, z), P(x + rng.uniform(3, 8), 0, z + rng.uniform(-0.5, 0.5))
        p.line([a, b], SEA_L if i % 3 == 0 else SEA_D, 1.4)


def mg_fire(img, cm, p, t, tracers_only=False):
    """Machine-gun fire from the casemates: bullets walking across the water (each a little white tuft thrown up,
    then a ring), the tracer streaks from the slit to where they land."""
    for ri, a, b, s0, s1 in MG_STREAMS:
        if not (a <= t <= b + 0.4):
            continue
        rate = 9.0
        n0 = max(0, int((t - a - 0.35) * rate))
        for n in range(n0, int((min(t, b) - a) * rate) + 1):
            hit_t = a + n / rate
            u = t - hit_t
            if u < 0 or u > 0.35:
                continue
            f = (hit_t - a) / max(0.01, b - a)
            rng = np.random.default_rng(ri * 1000 + n)
            x = s0[0] + (s1[0] - s0[0]) * f + rng.normal(0, 1.5)
            z = s0[1] + (s1[1] - s0[1]) * f + rng.normal(0, 1.5)
            (X, Y), k = cm.project((x, 0, z))
            if tracers_only:
                if u < 0.09 and n % 2 == 0:            # every other round a tracer
                    q0 = cm.project(slit_of(ri))[0]
                    w = rng.uniform(0.55, 0.85)
                    tail = (q0[0] + (X - q0[0]) * w, q0[1] + (Y - q0[1]) * w)
                    p.line([tail, (X, Y)], (255, 236, 150), 2.2)
                continue
            if u < 0.18:                               # the tuft of spray, rising and falling
                h = 1.6 * math.sin(math.pi * u / 0.18) * k
                p.poly([(X - 0.4 * k, Y), (X - 0.15 * k, Y - h), (X + 0.2 * k, Y - h * 0.8), (X + 0.4 * k, Y)],
                       SURF, None)
            r = (0.5 + 4 * u) * k                      # the ring spreading on the water
            p.ell(X, Y, r, r * 0.35, None, SURF + (int(255 * (1 - u / 0.35)),), 1.2)


def craft(img, cm, p, t, x0, z0, ph, head):
    """An LCVP (11 m x 3.2 m) from above on its own heading: the grey box hull, the ramp at the bow, the coxswain's
    stern, packed shoulder to shoulder with helmets (landers-3); its wake two rippling arms of foam with churned water
    between, the ripples running back as it goes (Sam)."""
    h = math.radians(head)
    fx, fz = math.sin(h), -math.cos(h)                 # forward (towards the beach)
    rx, rz = math.cos(h), math.sin(h)                  # its right
    x = x0 + fx * SPEED * t
    z = z0 + fz * SPEED * t
    bob = 0.15 * math.sin(t * 3 + ph)

    def W(lx, ly, lz):                                 # lz: metres back from the bow
        return (x + rx * lx - fx * lz, ly, z + rz * lx - fz * lz)
    P = lambda lx, ly, lz: cm.project(W(lx, ly, lz))[0]
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    q = S.pen(lay)
    q.poly(rough([P(-1.4, 0, 10.5), P(1.4, 0, 10.5), P(2.6, 0, 26), P(0.2, 0, 20), P(-2.6, 0, 26)], 3,
                 abs(int(x0))), SEA_L + (150,), None)  # churned water behind, fading
    for sg in (-1, 1):                                 # the two arms of the wake, wavy, thinning out
        pts = [P(sg * (1.5 + 0.1 * d) + 0.2 * math.sin(d * 0.9 - t * 7 + ph), 0, 10.5 + d) for d in np.arange(0, 18, 1.0)]
        q.line(pts, SURF + (220,), 2.2)
    for k in range(4):                                 # ripples running back across the wake
        d = 12 + ((k * 3.6 + t * SPEED) % 13)
        w = 1.2 + 0.1 * (d - 10)
        pts = [P(w * 0.8 * (j / 4), 0, d + 0.3 * math.sin(j * 1.5 + k)) for j in range(-4, 5)]
        q.line(pts, (200, 210, 210, int(200 * (1 - (d - 12) / 14))), 1.2)
    img.alpha_composite(lay)
    p.poly(rough([P(-2.1, 0, -0.5), P(2.1, 0, -0.5), P(2.5, 0, 0.8), P(-2.5, 0, 0.8)], 2, abs(int(z0))), SURF, None)
    p.poly([P(-1.6, 1.4 + bob, 0), P(1.6, 1.4 + bob, 0), P(1.6, 1.4 + bob, 11), P(-1.6, 1.4 + bob, 11)], HULL, INK, 2.0)
    p.poly([P(-1.3, 1.4 + bob, 1.2), P(1.3, 1.4 + bob, 1.2), P(1.3, 1.4 + bob, 9.0), P(-1.3, 1.4 + bob, 9.0)],
           HULL_D, INK, 1.4)
    p.poly([P(-1.6, 1.4 + bob, 0), P(1.6, 1.4 + bob, 0), P(1.6, 1.4 + bob, 1.2), P(-1.6, 1.4 + bob, 1.2)], HULL_L, INK, 1.6)
    p.poly([P(-0.9, 1.6 + bob, 9.2), P(0.9, 1.6 + bob, 9.2), P(0.9, 1.6 + bob, 10.6), P(-0.9, 1.6 + bob, 10.6)],
           HULL_D, INK, 1.4)
    (_, k) = cm.project(W(0, 1.5, 5))
    rng = np.random.default_rng(abs(int(x0 * 7 + z0)))
    for r in range(9):                                 # 36 men: four across, nine deep, never in a perfect grid
        for c in range(4):
            q = P(-0.95 + c * 0.63 + rng.uniform(-0.12, 0.12), 1.5 + bob, 1.55 + r * 0.85 + rng.uniform(-0.15, 0.15))
            rr = max(1.6, 0.3 * k)
            p.ell(q[0], q[1], rr, rr * 0.9, HELMET if (r + c) % 3 else HELMET_D, INK, 1.0)


def ships(img, cm, p, t):
    """Two warships at the bottom corners on their way past, each flying a barrage balloon on its cable."""
    for x0, z0, d in ((-120, 300, 1), (110, 320, -1)):
        x = x0 + d * 2.0 * t
        P = lambda dx, dz, y=2.0: cm.project((x + dx, y, z0 + dz))[0]
        p.poly(rough([P(-6 * d, 0), P(-30 * d, -6), P(-60 * d, -2), P(-30 * d, 6)], 3, abs(x0)), SURF, None)
        p.poly([P(-6 * d, 0), P(60 * d, -4), P(68 * d, 0), P(60 * d, 4), P(-6 * d, 0)], (96, 102, 106), INK, 2.0)
        p.poly([P(14 * d, -2), P(34 * d, -2), P(34 * d, 2), P(14 * d, 2)], (72, 76, 80), INK, 1.6)
        p.line([P(24 * d, 0, 6), P(24 * d, 0, 14)], (60, 62, 66), 3.0)                  # the funnel's mast
        bx, by, bz = x + 30 * d + 2 * math.sin(t), 40.0, z0 - 14                        # the balloon
        p.line([P(40 * d, 0, 4), cm.project((bx, by - 2, bz))[0]], (70, 72, 74), 1.0)
        (X, Y), k = cm.project((bx, by, bz))
        p.poly(_blob(X, Y, 4.5 * k, abs(x0), 14, 0.42), (170, 172, 170), INK, 1.6)
        for sg in (-1, 1):
            p.poly([(X + d * 3.6 * k, Y), (X + d * 5.6 * k, Y + sg * 1.6 * k), (X + d * 4.8 * k, Y)], (150, 152, 150),
                   INK, 1.2)


def rockets(img, cm, p, t):
    """A rocket salvo from the landing craft behind us: short bright heads with grey trails arcing down onto the beach,
    each bursting where it lands."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    q = S.pen(lay)
    for i, (t0, x, z) in enumerate(ROCKETS):
        u = (t - t0) / 0.7
        if not (0 <= u <= 1.0):
            continue
        a = np.array((x - 20, 20.0, 300.0))
        b = np.array((x, 0.0, z))
        def at(w):
            m = a + (b - a) * w
            m[1] += 28 * math.sin(math.pi * w)
            return m
        trail = [cm.project(tuple(at(max(0.0, u - 0.3 * (1 - j / 6)))))[0] for j in range(7)]
        q.line(trail, (210, 210, 206, 150), 2.6)
        head = cm.project(tuple(at(u)))[0]
        q.ell(head[0], head[1], 2.4, 2.4, (255, 226, 140, 255), None)
    img.alpha_composite(lay)


def planes(img, cm, p, t):
    """Two P-47 Thunderbolts crossing low, east to west: olive drab, black and white invasion stripes on the wings and
    fuselage (as every Allied plane wore on D-Day), their shadows on the water."""
    for t0, y, z in PLANES:
        x = -100 * (t - t0) - 14                       # 100 m/s, east (screen left) to west
        if not -120 < x < 100:
            continue
        def W(lx, lz, yy=y):                           # nose towards -x (west)
            return (x - lz, yy, z + lx)
        for yy, col, ink in ((0.2, (60, 72, 78, 110), None), (y, (88, 92, 66, 255), INK)):
            P = lambda lx, lz: cm.project(W(lx, lz, yy))[0]
            lay = Image.new('RGBA', img.size, (0, 0, 0, 0)) if ink is None else None
            pen = S.pen(lay) if lay is not None else p
            sx = 4 if ink is None else 0
            body = [P(-0.7, 5.5), P(0.7, 5.5), P(0.6, -5.0), P(0, -5.6), P(-0.6, -5.0)]
            wing = [P(-6.2, 1.6), P(6.2, 1.6), P(6.0, -0.4), P(-6.0, -0.4)]
            tail = [P(-2.4, -4.2), P(2.4, -4.2), P(2.2, -5.2), P(-2.2, -5.2)]
            for shape in (wing, tail, body):
                pen.poly([(a + sx, b + sx) for a, b in shape], col[:3] + ((col[3],) if lay is not None else ()), ink, 1.4)
            if ink is not None:                        # the invasion stripes: white, black, white, black, white
                for k in range(5):
                    for sg in (-1, 1):
                        a0, a1 = sg * (2.0 + k * 0.45), sg * (2.0 + (k + 1) * 0.45)
                        stripe = [P(a0, 1.6), P(a1, 1.6), P(a1, -0.4), P(a0, -0.4)]
                        pen.poly(stripe, (240, 240, 236) if k % 2 == 0 else (24, 24, 26), None)
                pen.ell(*P(0, 5.6), 2.6, 2.6, (180, 186, 190), None)             # the spinning prop
            if lay is not None:
                img.alpha_composite(lay)


# ------------------------------------------------------------------------------------------------ the bursts
def burst(img, cm, p, t, t0, x, z, kind, size=1.0):
    """A shell burst, three kinds (Sam: varied, less cartoony):
    'sand'  - a flash, a dark core of sand and smoke thrown up, pale dust billowing round it, clods falling back,
              then the dust drifting off on the wind and thinning out over ~3 s (the crater stays: beach()).
    'spray' - a tall white column of water thrown straight up, its top falling back as spray, a ring of foam spreading.
    'smoke' - a naval shell on the cliff top: a flash, then black smoke boiling up and leaning with the wind."""
    u = t - t0
    if u < 0:
        return
    (X, Y), k = cm.project((x, 0 if kind != 'smoke' else CLIFF_H, z))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    q = S.pen(lay)
    wind = 3.0 * u
    seed = abs(int(x * 7 + z * 3))
    if kind == 'sand':
        if u > 3.2:
            return
        h = 14 * size * min(1.0, u / 0.45) ** 0.5
        for i in range(5):                             # the drifting, thinning dust
            f = i / 4
            (cx, cy), _ = cm.project((x + wind * (0.4 + f), h * (0.25 + 0.6 * f) + 2 * u * f, z))
            r = (3 + 4 * f + 3.5 * u) * size * k
            billow(q, cx, cy, r, DUST, int(200 * max(0.0, 1 - u / 3.2)), seed + i, 8, 0.85)
        if u < 0.6:                                    # the dark core thrown up
            (cx, cy), _ = cm.project((x, h * 0.45, z))
            billow(q, cx, cy, (2.5 + 3 * u) * size * k, (88, 74, 58), int(230 * (1 - u / 0.6)), seed + 9, 6, 1.3)
        rng = np.random.default_rng(seed)
        for i in range(10):                            # clods arcing out and falling back
            vx, vy, vz = rng.normal(0, 5), rng.uniform(8, 15) * size, rng.normal(0, 3)
            if u > 2 * vy / 9.8:
                continue
            (cx, cy), _ = cm.project((x + vx * u, vy * u - 4.9 * u * u, z + vz * u))
            q.ell(cx, cy, 0.4 * k, 0.4 * k, (70, 60, 48, 255), None)
        img.alpha_composite(lay)
        if u < 0.09:
            _flash(p, X, Y - 1.5 * k, 3.4 * size * k, seed)
    elif kind == 'spray':
        if u > 2.2:
            return
        top = 24 * size * (math.sin(math.pi * min(1.0, u / 1.4)) if u < 1.4 else 0.0)
        a = int(235 * max(0.0, 1 - max(0.0, u - 1.0) / 1.2))
        for i in range(6):                             # the column: billows stacked, narrow, the top widening
            f = i / 5
            (cx, cy), _ = cm.project((x + wind * 0.15 * f, top * f, z))
            billow(q, cx, cy, (1.6 + 2.6 * f) * size * k * (1 + 0.5 * u), SURF, a, seed + i, 6, 1.1)
        r = (1.5 + 4 * u) * size * k                   # the foam ring
        q.ell(X, Y, r, r * 0.38, (236, 240, 238, int(200 * max(0.0, 1 - u / 2.2))), None)
        q.ell(X, Y, r * 0.75, r * 0.28, SEA_L + (int(220 * max(0.0, 1 - u / 2.2)),), None)
        img.alpha_composite(lay)
        if u < 0.06:
            _flash(p, X, Y - 1 * k, 2.4 * size * k, seed)
    else:
        for i in range(7):                             # black smoke boiling up and leaning on the wind
            f = i / 6
            (cx, cy), _ = cm.project((x + wind * f * 1.6, (6 + 34 * f) * min(1.0, u / 1.5 + 0.2) * size, z - 2))
            r = (4 + 6 * f + 1.5 * u) * size * k
            billow(q, cx, cy, r, BLACK if i % 3 else (84, 82, 80), 215, seed + i, 8, 0.8)
        img.alpha_composite(lay)
        if u < 0.1:
            _flash(p, X, Y - 3 * k, 4 * size * k, seed)


def drift(img, cm, t):
    """Smoke lying along the beach and drifting east to west with the wind (refs air-3, -4): long, low, see-through."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    q = S.pen(lay)
    rng = np.random.default_rng(6)
    for i in range(16):
        x = rng.uniform(-260, 220) + 5 * t
        z = rng.uniform(10, 66)
        (X, Y), k = cm.project((x, rng.uniform(3, 10), z))
        for j in range(4):                             # a long low bank: billows strung out along the wind
            billow(q, X + j * 7 * k, Y + rng.uniform(-1, 1) * k, rng.uniform(4, 7) * k,
                   SMOKE if i % 3 else SMOKE_D, int(rng.uniform(60, 110)), i * 10 + j, 7, 0.55)
    img.alpha_composite(lay)


def gunfire(img, cm, p, t):
    """The casemates firing: the slit lit by a lumpy muzzle flash on most frames while its stream is firing, and the
    other casemates and pits flickering too; tracers drawn last so the fire always reads."""
    f = int(t * 12)
    firing = {ri for ri, a, b, *_ in MG_STREAMS if a <= t <= b}
    for i in range(len(REDOUBTS)):
        if i in firing and f % 3 != 2 or i not in firing and (f + i * 5) % 7 == 0:
            (X, Y), k = cm.project(slit_of(i))
            _flash(p, X, Y, max(5.0, 1.8 * k), f * 31 + i)
    for i, (x, back) in enumerate(MG_PITS):
        if (f + i * 3) % 4 == 0:
            (X, Y), k = cm.project((x, CLIFF_H + 0.8, -back))
            _flash(p, X, Y, max(4.0, 1.2 * k), f * 17 + i)
    mg_fire(img, cm, p, t, tracers_only=True)


def picture(t):
    cm = cam(t)
    img = B.canvas(SKY)
    p = S.pen(img)
    sky(img, cm, p, t)
    land(img, cm, p, t)
    sea(img, cm, p, t)
    beach(img, cm, p, t)
    cliffs(img, cm, p, t)
    redoubts(img, cm, p, t)                            # set into the cliff's face, in front of it
    redoubts_face = [b for b in BURSTS if b[3] == 'smoke']
    defences(img, cm, p, t)
    for b in BURSTS:
        if b[3] == 'sand':
            burst(img, cm, p, t, *b)
    drift(img, cm, t)
    mg_fire(img, cm, p, t)
    for b in BURSTS:
        if b[3] == 'spray':
            burst(img, cm, p, t, *b)
    for x0, z0, ph, head in sorted(CRAFT, key=lambda c: c[1]):
        craft(img, cm, p, t, x0, z0, ph, head)
    for b in redoubts_face:
        burst(img, cm, p, t, *b)
    ships(img, cm, p, t)
    rockets(img, cm, p, t)
    for t0, x, z in ROCKETS:                          # each rocket bursts where it lands
        burst(img, cm, p, t, t0 + 0.7, x, z, 'sand', 0.55)
    planes(img, cm, p, t)
    gunfire(img, cm, p, t)
    return img


if __name__ == '__main__':
    B.SS = 1
    picture(float(sys.argv[2]) if len(sys.argv) > 2 else 1.8).convert('RGB').save(sys.argv[1], quality=88)
