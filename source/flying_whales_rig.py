#!/usr/bin/env python3
"""Flying Whales: the oil rig (Jackdaw-style, refs rig-jackdaw-*, rig-night-*, rig-sunset-pipes, rig-legs-walkway-dusk),
in 31 breakable pieces, painted flat in the house style through the rig scene's one locked camera (flying_whales_sea.CAM).

How it is drawn (rule 39: one locked camera, so a flat painting in layers): every piece is laid out in metres at its
real size and painted through the camera once (flat lit and shadow tones, one ink outline round every face, details
on top: lit windows, yellow framing, railings, pipes, the JACKDAW board). A piece knocked loose is simply painted again
at its new place and angle each frame (`xf`), so it keeps its perspective as it falls; anything below the sea surface
(z = 0) is cut off, so a sinking piece disappears behind the waterline by itself.

The layout (world: whale.py's axes, x right, y away from the camera, z up; the camera 120 m from the near corner):
- the rig's own frame: `a` along the long side (0 at the near right corner, 50 m to the far left), `b` along the short
  side (0 at the front, 35 m to the back), z up from the sea; the long side turned 25 degrees off square, so we see the
  long front face and the right end (Sam: "from a diagonal direction");
- the jacket: four yellow legs (1.8 m across, leaning in as they rise) with X bracing, sea to 25 m;
- three deck storeys, each split into a right and a left half (so one half can be smashed while the other stands):
  the open cellar deck (25-33 m: dark inside, yellow beams, pipes, three orange lifeboats on the front), the
  mezzanine (33-41 m: clad, yellow framing, the JACKDAW board), the top deck (41-49 m: clad modules, lit windows);
- on the roof: two modules, the crane (pedestal and cab; its lattice boom up to the left), the drilling derrick, two
  exhaust stacks; on the left end a yellow stair tower, the helideck on its truss with the orange escape chute, and a
  stub of the walkway bridge; on the right end the flare boom, 45 m out and up, with its flame.

    python3 source/flying_whales_rig.py sheet OUT.jpg     the rig on the dusk sea, the pieces numbered, a break test
    python3 source/flying_whales_rig.py check            the line check on the rig alone

Use in the film:
    import flying_whales_rig as R
    frame = R.draw(base_rgb, t, xf={'deck_top_r': (Rm, T)}, gone={'lifeboat_2'})   # Rm 3x3 about the piece's pivot
    R.PARTS['leg_fr'].pivot, R.PARENT['crane_boom'], R.FLARE_TIP, R.part_box(name)  # for the choreography and hits
"""
import functools
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import whale as W                                     # noqa: E402
import flying_whales_sea as SEA                       # noqa: E402

INK = W.INK
CAM = SEA.CAM
OL = 5
SS = 2

# the rig's frame in the world
ORIGIN = np.array([14.0, 0.0, 0.0])                   # the near right corner of the cellar deck, at sea level
YAW = math.radians(25.0)
EU = np.array([-math.cos(YAW), math.sin(YAW), 0.0])   # a: along the long side, to the far left
EV = np.array([math.sin(YAW), math.cos(YAW), 0.0])    # b: along the short side, away from us
EZ = np.array([0.0, 0.0, 1.0])
DECK_L, DECK_D = 50.0, 35.0
LEVELS = (25.0, 33.0, 41.0, 49.0)                     # cellar floor, mezzanine, top deck, roof
LIGHT = np.array([-0.6, -0.25, 0.75])                 # sky light from above and the sunset side (left)
LIGHT = LIGHT / np.linalg.norm(LIGHT)
TINT = SEA.DUSK_TINT

# (lit, shadow); all kept above the line check's ink darkness (luma 85)
COL = {
    'yellow': ((236, 190, 52), (192, 148, 44)),
    'clad': ((210, 210, 216), (162, 164, 180)),
    'grey': ((156, 158, 166), (120, 122, 136)),
    'dark': ((116, 116, 128), (96, 98, 110)),
    'blue': ((76, 126, 186), (60, 100, 156)),
    'red': ((206, 74, 58), (172, 62, 52)),
    'orange': ((248, 132, 44), (210, 104, 36)),
    'white': ((238, 238, 238), (198, 200, 208)),
    'deck': ((132, 140, 134), (104, 110, 108)),
}
LAMP = [(255, 218, 140), (255, 190, 100), (255, 236, 190)]
PIPE = (150, 150, 158)


def P(a, b, z):
    """A point in the rig's frame (a, b, z in m) in the world."""
    return ORIGIN + a * EU + b * EV + z * EZ


# ------------------------------------------------- building blocks --------------------------------------------------
def _face(pts, col, centre):
    pts = np.array(pts, float)
    n = np.cross(pts[1] - pts[0], pts[2] - pts[0])
    n = n / (np.linalg.norm(n) + 1e-12)
    if np.dot(n, pts.mean(0) - centre) < 0:
        n = -n
    return dict(kind='poly', pts=pts, n=n, col=col)


def box(a0, b0, z0, a1, b1, z1, col, cols=None):
    """Six faces of a box in the rig frame. cols: per-face colour overrides {'front','back','left','right','top','bot'}."""
    c = P((a0 + a1) / 2, (b0 + b1) / 2, (z0 + z1) / 2)
    cols = cols or {}
    q = lambda *abz: [P(*v) for v in abz]
    return [
        _face(q((a0, b0, z0), (a1, b0, z0), (a1, b0, z1), (a0, b0, z1)), cols.get('front', col), c),
        _face(q((a0, b1, z0), (a1, b1, z0), (a1, b1, z1), (a0, b1, z1)), cols.get('back', col), c),
        _face(q((a0, b0, z0), (a0, b1, z0), (a0, b1, z1), (a0, b0, z1)), cols.get('right', col), c),
        _face(q((a1, b0, z0), (a1, b1, z0), (a1, b1, z1), (a1, b0, z1)), cols.get('left', col), c),
        _face(q((a0, b0, z1), (a1, b0, z1), (a1, b1, z1), (a0, b1, z1)), cols.get('top', col), c),
        _face(q((a0, b0, z0), (a1, b0, z0), (a1, b1, z0), (a0, b1, z0)), cols.get('bot', col), c),
    ]


def prism(outline_az, b0, b1, col):
    """A prism: a closed outline in the (a, z) plane, extruded from b0 to b1 (the lifeboats)."""
    c = np.mean([P(a, (b0 + b1) / 2, z) for a, z in outline_az], 0)
    fr = [P(a, b0, z) for a, z in outline_az]
    bk = [P(a, b1, z) for a, z in outline_az]
    faces = [_face(fr, col, c), _face(bk, col, c)]
    n = len(outline_az)
    for i in range(n):
        j = (i + 1) % n
        faces.append(_face([fr[i], fr[j], bk[j], bk[i]], col, c))
    return faces


def tube(p0, p1, r, col):
    return dict(kind='tube', p0=np.asarray(p0, float), p1=np.asarray(p1, float), r=r, col=col)


def line(p0, p1, col=INK, w=0.35):
    """A thin member or pipe: drawn after the ink, w metres across (at least 2 px)."""
    return dict(kind='line', p0=np.asarray(p0, float), p1=np.asarray(p1, float), col=col, w=w)


def lights(face_q, rows, per, seed, dens=0.7, n=None):
    """Rows of lit windows laid on a face quad (four world corners: bottom-left, bottom-right, top-right, top-left)."""
    r = np.random.default_rng(seed)
    q = np.array(face_q, float)
    out = []
    for i in range(rows):
        v = (i + 0.5) / rows
        for j in range(per):
            if r.random() > dens:
                continue
            u = (j + 0.5 + r.uniform(-0.2, 0.2)) / per
            du, dv = 0.28 / per, 0.18 / rows
            pts = []
            for uu, vv in ((u - du, v - dv), (u + du, v - dv), (u + du, v + dv), (u - du, v + dv)):
                bot = q[0] + (q[1] - q[0]) * uu
                top = q[3] + (q[2] - q[3]) * uu
                pts.append(bot + (top - bot) * vv)
            out.append(dict(kind='spot', pts=np.array(pts), col=LAMP[int(r.integers(0, 3))], n=n))
    return out


def stripe(quad, col, n_hint):
    """A flat painted band on a face (yellow framing), no ink of its own."""
    return dict(kind='spot', pts=np.array(quad, float), col=COL[col][0], n=n_hint)


def rail(p0, p1, h=1.2, post=2.5):
    """A handrail h m above the edge p0-p1, with posts."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    out = [line(p0 + EZ * h, p1 + EZ * h, INK, 0.12)]
    n = max(1, int(np.linalg.norm(p1 - p0) / post))
    for k in range(n + 1):
        p = p0 + (p1 - p0) * k / n
        out.append(line(p, p + EZ * h, INK, 0.1))
    return out


class Part:
    def __init__(self, name, label, items, pivot):
        self.name, self.label, self.items, self.pivot = name, label, items, np.asarray(pivot, float)


# ------------------------------------------------- the rig ----------------------------------------------------------
LEGS = {'leg_fr': (9.0, 7.0), 'leg_fl': (41.0, 7.0), 'leg_br': (9.0, 28.0), 'leg_bl': (41.0, 28.0)}
BATTER = 1.6                                          # m each leg leans in from the sea to the deck
LEG_R = 0.9
FLARE_DIR = np.array([-0.45, 0.68, 0.62])            # in the rig frame (a, b, z): out to the right and up
FLARE_DIR = FLARE_DIR / np.linalg.norm(FLARE_DIR)
FLARE_ROOT = (0.0, 26.0, 45.0)
FLARE_LEN = 42.0


def _leg_pt(name, z):
    a, b = LEGS[name]
    k = (1 - z / LEVELS[0]) * BATTER
    sa = -1 if a < 25 else 1
    sb = -1 if b < 17.5 else 1
    return P(a + sa * k, b + sb * k, z)


def _brace_face(n0, n1, z0, z1, r=0.6):
    """An X between legs n0 and n1 from z0 to z1, with the horizontal at z1. The front face's tubes are yellow and
    filled; the sides and back are thinner (ink members), so the front X reads first through the jacket."""
    return [tube(_leg_pt(n0, z0), _leg_pt(n1, z1), r, 'yellow'), tube(_leg_pt(n1, z0), _leg_pt(n0, z1), r, 'yellow'),
            tube(_leg_pt(n0, z1), _leg_pt(n1, z1), r * 1.04, 'yellow')]


def _storey(level, a0, a1, inset, seed, kind):
    z0, z1 = LEVELS[level], LEVELS[level + 1]
    b0, b1 = inset, DECK_D - inset
    if kind == 'cellar':
        items = box(a0, b0, z0, a1, b1, z1, 'dark', cols={'bot': 'grey', 'top': 'grey'})
    else:
        items = box(a0, b0, z0, a1, b1, z1, 'clad', cols={'bot': 'grey'})
    fn = items[0]['n']
    rn = items[2]['n']
    # yellow framing: a beam along the bottom and top of the front, columns every 8 m (6 m on the cellar)
    step = 6.0 if kind == 'cellar' else 8.0
    for zz0, zz1 in ((z0, z0 + 1.0), (z1 - 0.9, z1)):
        items.append(stripe([P(a0, b0 - 0.02, zz0), P(a1, b0 - 0.02, zz0), P(a1, b0 - 0.02, zz1), P(a0, b0 - 0.02, zz1)],
                            'yellow', fn))
    a = a0 + (step - (a0 % step))
    while a < a1 - 0.5:
        items.append(stripe([P(a - 0.45, b0 - 0.03, z0), P(a + 0.45, b0 - 0.03, z0), P(a + 0.45, b0 - 0.03, z1),
                             P(a - 0.45, b0 - 0.03, z1)], 'yellow', fn))
        a += step
    if a0 < 0.5:                                      # the right end of the right half: framing and lights there too
        for zz0, zz1 in ((z0, z0 + 1.0), (z1 - 0.9, z1)):
            items.append(stripe([P(a0 - 0.02, b0, zz0), P(a0 - 0.02, b1, zz0), P(a0 - 0.02, b1, zz1),
                                 P(a0 - 0.02, b0, zz1)], 'yellow', rn))
        for bb in np.arange(b0 + 7.0, b1, 7.0):
            items.append(stripe([P(a0 - 0.03, bb - 0.45, z0), P(a0 - 0.03, bb + 0.45, z0), P(a0 - 0.03, bb + 0.45, z1),
                                 P(a0 - 0.03, bb - 0.45, z1)], 'yellow', rn))
        items += lights([P(a0 - 0.05, b0 + 1, z0 + 1.2), P(a0 - 0.05, b1 - 1, z0 + 1.2), P(a0 - 0.05, b1 - 1, z1 - 1.1),
                         P(a0 - 0.05, b0 + 1, z1 - 1.1)], 2, 12, seed + 7, 0.55 if kind != 'cellar' else 0.3, rn)
    if kind == 'cellar':
        # the open cellar: pipes along the front and a few lamps deep inside
        for zz in (z0 + 2.6, z0 + 4.2, z0 + 5.4):
            items.append(line(P(a0 + 0.3, b0 - 0.05, zz), P(a1 - 0.3, b0 - 0.05, zz), PIPE, 0.55))
        items += lights([P(a0 + 1, b0 - 0.06, z0 + 1.5), P(a1 - 1, b0 - 0.06, z0 + 1.5), P(a1 - 1, b0 - 0.06, z1 - 1.5),
                         P(a0 + 1, b0 - 0.06, z1 - 1.5)], 2, int((a1 - a0) / 2.2), seed, 0.35, fn)
    else:
        rows = 2
        items += lights([P(a0 + 1, b0 - 0.05, z0 + 1.4), P(a1 - 1, b0 - 0.05, z0 + 1.4), P(a1 - 1, b0 - 0.05, z1 - 1.3),
                         P(a0 + 1, b0 - 0.05, z1 - 1.3)], rows, int((a1 - a0) / 1.6), seed, 0.6, fn)
    if kind == 'top':                                 # blue panels on the top deck's modules
        for k, aa in enumerate(np.arange(a0 + 3.0, a1 - 3.0, 9.0)):
            if (k + seed) % 2 == 0:
                items.append(stripe([P(aa, b0 - 0.04, z0 + 1.2), P(aa + 4.5, b0 - 0.04, z0 + 1.2),
                                     P(aa + 4.5, b0 - 0.04, z1 - 1.2), P(aa, b0 - 0.04, z1 - 1.2)], 'blue', fn))
    # the railing round the top of this storey's front and right end (on the lip in front of the storey above)
    items += rail(P(a0, b0 - 0.3, z1), P(a1, b0 - 0.3, z1))
    if a0 < 0.5:
        items += rail(P(a0 - 0.3, b0, z1), P(a0 - 0.3, b1, z1))
    return items


def _lattice(p0, p1, w0, w1, up, col, r, bays):
    """A lattice boom or tower from p0 to p1: two chords (tubes, w0 -> w1 apart) and the zigzag between (ink lines)."""
    d = p1 - p0
    side = np.cross(d, up)
    side = side / (np.linalg.norm(side) + 1e-9)
    a0, a1 = p0 - side * w0 / 2, p1 - side * w1 / 2
    b0, b1 = p0 + side * w0 / 2, p1 + side * w1 / 2
    items = [tube(a0, a1, r, col), tube(b0, b1, r, col)]
    pts_a = [a0 + (a1 - a0) * k / bays for k in range(bays + 1)]
    pts_b = [b0 + (b1 - b0) * k / bays for k in range(bays + 1)]
    for k in range(bays):
        items.append(line(pts_a[k], pts_b[k + 1], INK, 0.22))
        items.append(line(pts_b[k + 1], pts_a[k + 1], INK, 0.22))
    return items


@functools.lru_cache(None)
def build():
    parts = []

    def add(name, label, items, pivot):
        parts.append(Part(name, label, items, pivot))

    # the jacket
    for n in LEGS:
        add(n, 'leg ' + n[-2:].upper(), [tube(_leg_pt(n, -6.0), _leg_pt(n, LEVELS[0]), LEG_R, 'yellow')],
            _leg_pt(n, 12.0))
    add('brace_front_low', 'front bracing, low', _brace_face('leg_fr', 'leg_fl', 0.5, 12.5), P(25, 6, 6))
    add('brace_front_high', 'front bracing, high', _brace_face('leg_fr', 'leg_fl', 12.5, 24.5), P(25, 6, 18))
    add('brace_right', 'right-end bracing', _brace_face('leg_fr', 'leg_br', 0.5, 12.5, 0.36) +
        _brace_face('leg_fr', 'leg_br', 12.5, 24.5, 0.36), P(8, 17.5, 12))
    add('brace_left', 'left-end bracing', _brace_face('leg_fl', 'leg_bl', 0.5, 12.5, 0.36) +
        _brace_face('leg_fl', 'leg_bl', 12.5, 24.5, 0.36), P(42, 17.5, 12))
    add('brace_back', 'back bracing', _brace_face('leg_br', 'leg_bl', 0.5, 12.5, 0.36) +
        _brace_face('leg_br', 'leg_bl', 12.5, 24.5, 0.36), P(25, 29, 12))
    # the decks, each in two halves
    for lv, (nm, kind, inset) in enumerate((('cellar', 'cellar', 0.0), ('mezz', 'mezz', 1.2), ('top', 'top', 2.4))):
        for half, (a0, a1) in (('r', (inset, 25.0)), ('l', (25.0, DECK_L - inset))):
            z0, z1 = LEVELS[lv], LEVELS[lv + 1]
            add(f'deck_{nm}_{half}', f'{nm} deck, {"right" if half == "r" else "left"} half',
                _storey(lv, a0, a1, inset, 11 * lv + (0 if half == 'r' else 5), kind),
                P((a0 + a1) / 2, DECK_D / 2, (z0 + z1) / 2))
    roof = LEVELS[3]
    add('module_a', 'blue module', box(15.0, 4.0, roof, 22.0, 7.5, roof + 3.2, 'blue') +
        rail(P(15, 3.7, roof + 3.2), P(22, 3.7, roof + 3.2), 1.0), P(18.5, 5.7, roof + 1.6))
    add('module_b', 'grey module', box(30.0, 22.0, roof, 38.0, 29.0, roof + 4.0, 'grey'), P(34, 25.5, roof + 2))
    # the crane: pedestal and cab, then its boom up to the left
    cr = (29.0, 7.0)
    cab = box(cr[0] - 2.6, cr[1] - 2.2, roof + 8.0, cr[0] + 2.6, cr[1] + 2.2, roof + 12.0, 'yellow',
              cols={'front': 'white'})
    cab += lights([P(cr[0] - 2, cr[1] - 2.25, roof + 9.4), P(cr[0] + 0.5, cr[1] - 2.25, roof + 9.4),
                   P(cr[0] + 0.5, cr[1] - 2.25, roof + 11.2), P(cr[0] - 2, cr[1] - 2.25, roof + 11.2)], 1, 2, 5, 1.0, cab[0]['n'])
    add('crane_house', 'crane pedestal and cab', [tube(P(cr[0], cr[1], roof), P(cr[0], cr[1], roof + 8.2), 1.5, 'yellow')]
        + cab, P(cr[0], cr[1], roof + 6))
    bdir = np.array([math.cos(math.radians(58)), -0.12, math.sin(math.radians(58))])
    b0 = np.array([cr[0] + 1.5, cr[1], roof + 10.0])
    b1 = b0 + bdir * 35.0
    boom = _lattice(P(*b0), P(*b1), 3.0, 0.8, EV, 'yellow', 0.55, 10)
    boom.append(line(P(*b1), P(b1[0], b1[1], b1[2] - 14.0), INK, 0.12))          # the hook rope
    boom += box(b1[0] - 0.5, b1[1] - 0.5, b1[2] - 15.2, b1[0] + 0.5, b1[1] + 0.5, b1[2] - 14.0, 'red')
    add('crane_boom', 'crane boom', boom, P(*(b0 + bdir * 12)))
    # the derrick: a tapered red lattice tower
    dc, dz0, dz1 = (12.0, 22.0), roof, roof + 24.0
    der = []
    corners0 = [(-4, -4), (4, -4), (4, 4), (-4, 4)]
    corners1 = [(-1.1, -1.1), (1.1, -1.1), (1.1, 1.1), (-1.1, 1.1)]
    c0 = [P(dc[0] + x, dc[1] + y, dz0) for x, y in corners0]
    c1 = [P(dc[0] + x, dc[1] + y, dz1) for x, y in corners1]
    for k in range(4):
        der.append(tube(c0[k], c1[k], 0.5, 'red'))
    for lvl in range(1, 6):
        f0, f1 = (lvl - 1) / 5, lvl / 5
        q0 = [c0[k] + (c1[k] - c0[k]) * f0 for k in range(4)]
        q1 = [c0[k] + (c1[k] - c0[k]) * f1 for k in range(4)]
        for k in range(4):
            der.append(line(q1[k], q1[(k + 1) % 4], INK, 0.25))
            der.append(line(q0[k], q1[(k + 1) % 4], INK, 0.2))
    der += box(dc[0] - 1.6, dc[1] - 1.6, dz1, dc[0] + 1.6, dc[1] + 1.6, dz1 + 2.2, 'white')
    add('derrick', 'derrick', der, P(dc[0], dc[1], roof + 10))
    # the exhaust stacks, grey with sooty tops
    for k, (sa, sb, h) in enumerate(((40.0, 24.0, 19.0), (43.6, 24.5, 16.5))):
        add(f'stack_{k + 1}', f'exhaust stack {k + 1}',
            [tube(P(sa, sb, roof), P(sa, sb, roof + h), 1.0, 'grey'),
             tube(P(sa, sb, roof + h - 1.6), P(sa, sb, roof + h), 1.04, 'dark')], P(sa, sb, roof + h / 2))
    # the yellow stair tower on the left end
    st = box(50.0, 3.0, LEVELS[0], 53.6, 7.0, roof + 5.0, 'yellow')
    for z in np.arange(LEVELS[0] + 1.5, roof + 4.0, 3.0):
        st.append(line(P(50.2, 2.95, z), P(53.4, 2.95, z + 1.5), INK, 0.18))
        st.append(line(P(53.4, 2.95, z + 1.5), P(50.2, 2.95, z + 3.0), INK, 0.18))
    add('stair_tower', 'stair tower', st, P(51.8, 5, 37))
    # the helideck: an octagon on a truss off the left end, the orange escape chute beneath
    hc, hz, hr = (64.0, 13.0), roof + 3.0, 11.0
    oct_ = [(hc[0] + hr * math.cos(math.pi / 8 + k * math.pi / 4), hc[1] + hr * math.sin(math.pi / 8 + k * math.pi / 4))
            for k in range(8)]
    top = [P(a, b, hz + 1.2) for a, b in oct_]
    bot = [P(a, b, hz) for a, b in oct_]
    cen = P(hc[0], hc[1], hz + 0.6)
    hd = [_face(top, 'deck', cen), _face(bot, 'grey', cen)]
    for k in range(8):
        j = (k + 1) % 8
        hd.append(_face([bot[k], bot[j], top[j], top[k]], 'white', cen))
    for k in range(8):                                  # the safety net round the edge: an orange line
        j = (k + 1) % 8
        hd.append(line(top[k] + EZ * 0.5, top[j] + EZ * 0.5, COL['orange'][0], 0.35))
    add('helideck', 'helideck', hd, P(hc[0], hc[1], hz))
    tr = [tube(P(53.6, 4.0, LEVELS[2]), P(58.0, 6.0, hz - 0.1), 0.45, 'grey'),
          tube(P(53.6, 6.5, LEVELS[1]), P(60.0, 9.0, hz - 0.1), 0.45, 'grey'),
          tube(P(DECK_L, 20.0, LEVELS[2]), P(58.0, 20.0, hz - 0.1), 0.45, 'grey'),
          tube(P(DECK_L, 27.0, LEVELS[1]), P(61.0, 19.0, hz - 0.1), 0.45, 'grey')]
    tr += prism([(56.0, hz - 0.3), (58.4, hz - 0.3), (54.6, LEVELS[0] + 1.0), (52.2, LEVELS[0] + 1.0)], 6.0, 8.6,
                'orange')
    add('helideck_truss', 'helideck truss and chute', tr, P(57, 12, LEVELS[1] + 6))
    # the walkway bridge stub, off the left end towards the back
    wk = []
    w0, w1 = (DECK_L, 26.0), (DECK_L + 17.0, 31.0)
    for db in (-1.6, 1.6):
        for zz in (LEVELS[0] + 3.0, LEVELS[0] + 6.4):
            wk.append(tube(P(w0[0], w0[1] + db, zz), P(w1[0], w1[1] + db, zz), 0.35, 'yellow'))
    for k in range(6):
        f0, f1 = k / 6, (k + 1) / 6
        pa = lambda f, db, zz: P(w0[0] + (w1[0] - w0[0]) * f, w0[1] + (w1[1] - w0[1]) * f + db, zz)
        wk.append(line(pa(f0, -1.6, LEVELS[0] + 3.0), pa(f1, -1.6, LEVELS[0] + 6.4), INK, 0.2))
    wk.append(line(P(w1[0], w1[1] - 1.6, LEVELS[0] + 3.0), P(w1[0] + 0.8, w1[1] - 1.0, LEVELS[0] + 7.2), INK, 0.2))
    add('walkway', 'walkway bridge stub', wk, P((w0[0] + w1[0]) / 2, (w0[1] + w1[1]) / 2, LEVELS[0] + 4.7))
    # the flare boom off the right end, with its tip
    fr = np.array(FLARE_ROOT)
    tip = fr + FLARE_DIR * FLARE_LEN
    fb = _lattice(P(*fr), P(*tip), 3.4, 1.2, EZ, 'grey', 0.5, 12)
    fb += _lattice(P(*fr) + EZ * 0.01, P(*tip) + EZ * 0.01, 3.4, 1.2, np.cross(FLARE_DIR @ np.stack([EU, EV, EZ]), EZ),
                   'grey', 0.4, 12)[2:]
    fb.append(tube(P(*tip), P(*tip) + EZ * 3.0, 0.6, 'dark'))
    add('flare_boom', 'flare boom', fb, P(*(fr + FLARE_DIR * 18)))
    # three orange lifeboats on the cellar deck's front, and the name board on the mezzanine
    for k, la in enumerate((5.5, 17.0, 43.5)):
        z0 = LEVELS[0] + 1.2
        out = []
        for i in range(14):                               # a capsule outline in (a, z): 8.5 m long, 3 m tall
            th = 2 * math.pi * i / 14
            out.append((la + 4.25 * math.copysign(abs(math.cos(th)) ** 0.45, math.cos(th)),
                        z0 + 1.5 + 1.5 * math.copysign(abs(math.sin(th)) ** 0.6, math.sin(th))))
        lb = prism(out, -3.2, -0.2, 'orange')
        lb += [stripe([P(la - 3.0, -3.25, z0 + 1.9), P(la + 3.0, -3.25, z0 + 1.9), P(la + 3.0, -3.25, z0 + 2.4),
                       P(la - 3.0, -3.25, z0 + 2.4)], 'white', lb[0]['n'])]
        lb.append(line(P(la - 2.5, -1.7, z0 + 3.0), P(la - 2.5, -1.7, LEVELS[1]), INK, 0.12))   # davit falls
        lb.append(line(P(la + 2.5, -1.7, z0 + 3.0), P(la + 2.5, -1.7, LEVELS[1]), INK, 0.12))
        add(f'lifeboat_{k + 1}', f'lifeboat {k + 1}', lb, P(la, -1.7, z0 + 1.5))
    nb = box(22.0, 0.75, LEVELS[1] + 1.4, 36.0, 1.2, LEVELS[1] + 5.2, 'yellow')
    add('name_board', 'JACKDAW board', nb + [dict(kind='text', text='JACKDAW',
        quad=np.array([P(35.4, 0.7, LEVELS[1] + 1.8), P(22.6, 0.7, LEVELS[1] + 1.8), P(22.6, 0.7, LEVELS[1] + 4.8),
                       P(35.4, 0.7, LEVELS[1] + 4.8)]), n=nb[0]['n'])], P(29, 1, LEVELS[1] + 3.3))
    return {p.name: p for p in parts}


PARTS = build()
FLARE_TIP = P(*(np.array(FLARE_ROOT) + FLARE_DIR * FLARE_LEN)) + EZ * 3.0
# what each piece hangs on (it falls with its parent unless knocked off itself)
PARENT = {
    'deck_cellar_r': 'leg_fr', 'deck_cellar_l': 'leg_fl',
    'deck_mezz_r': 'deck_cellar_r', 'deck_mezz_l': 'deck_cellar_l',
    'deck_top_r': 'deck_mezz_r', 'deck_top_l': 'deck_mezz_l',
    'module_a': 'deck_top_r', 'crane_house': 'deck_top_l', 'crane_boom': 'crane_house', 'module_b': 'deck_top_l',
    'derrick': 'deck_top_r', 'stack_1': 'deck_top_l', 'stack_2': 'deck_top_l',
    'stair_tower': 'deck_cellar_l', 'helideck': 'deck_top_l', 'helideck_truss': 'deck_top_l', 'walkway': 'deck_cellar_l',
    'flare_boom': 'deck_mezz_r', 'lifeboat_1': 'deck_cellar_r', 'lifeboat_2': 'deck_cellar_r',
    'lifeboat_3': 'deck_cellar_l', 'name_board': 'deck_mezz_l',
    'brace_front_low': 'leg_fr', 'brace_front_high': 'leg_fr', 'brace_right': 'leg_fr', 'brace_left': 'leg_fl',
    'brace_back': 'leg_br',
}


def part_box(name):
    """World bounding box (min, max) of a piece at rest: for the whales' hit tests."""
    pts = []
    for it in PARTS[name].items:
        if it['kind'] in ('poly', 'spot'):
            pts += list(it['pts'])
        elif it['kind'] in ('tube', 'line'):
            pts += [it['p0'], it['p1']]
    pts = np.array(pts)
    return pts.min(0), pts.max(0)


# ------------------------------------------------- painting a piece -------------------------------------------------
def _clip_z(pts, z=0.0):
    """Keep the part of a polygon above the sea (z >= 0)."""
    out = []
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        ia, ib = a[2] >= z, b[2] >= z
        if ia:
            out.append(a)
        if ia != ib:
            out.append(a + (b - a) * (z - a[2]) / (b[2] - a[2]))
    return out


def _clip_seg(p0, p1, z=0.0):
    if p0[2] < z and p1[2] < z:
        return None
    if p0[2] < z:
        p0 = p0 + (p1 - p0) * (z - p0[2]) / (p1[2] - p0[2])
    elif p1[2] < z:
        p1 = p1 + (p0 - p1) * (z - p1[2]) / (p0[2] - p1[2])
    return p0, p1


def _shade(n, col):
    return COL[col][0 if np.dot(n, LIGHT) > -0.05 else 1]


def _tint(c, k=1.0):
    tr, tg, tb, tk = TINT
    tk *= k
    return tuple(int(c[i] * (1 - tk) + (tr, tg, tb)[i] * tk) for i in range(3))


def _font(px):
    return ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), max(6, int(px)))


def _perspective(src_quad, dst_quad):
    """PIL PERSPECTIVE coefficients mapping dst pixels back to src."""
    A, B = [], []
    for (x, y), (u, v) in zip(dst_quad, src_quad):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def render(part, cam=CAM, xf=None, ss=SS):
    """Paint one piece. xf: (Rm 3x3, T 3) moves it rigidly about its pivot. Returns a whale.Sprite (or None)."""
    piv = part.pivot
    if xf is None:
        Rm, T = np.eye(3), np.zeros(3)
    else:
        Rm, T = np.asarray(xf[0], float), np.asarray(xf[1], float)
    mv = lambda p: (np.asarray(p, float) - piv) @ Rm.T + piv + T
    W_, H_ = cam.size
    polys, late, spots, texts = [], [], [], []
    depth_all = []
    for it in part.items:
        k = it['kind']
        if k == 'poly':
            pts = mv(it['pts'])
            n = it['n'] @ Rm.T
            c = pts.mean(0)
            if np.dot(n, c - cam.pos) >= 0:
                continue                                        # facing away
            q = _clip_z(list(pts))
            if len(q) < 3:
                continue
            S_, d = cam.screen(np.array(q))
            if (d < 1).any():
                continue
            polys.append((float(np.linalg.norm(c - cam.pos)), S_, _tint(_shade(n, it['col']))))
            depth_all.append(polys[-1][0])
        elif k == 'tube':
            seg = _clip_seg(mv(it['p0']), mv(it['p1']))
            if seg is None:
                continue
            (s0, s1), d = cam.screen(np.array(seg))
            if (d < 1).any():
                continue
            r0, r1 = it['r'] * cam.focal / d[0], it['r'] * cam.focal / d[1]
            v = s1 - s0
            L = np.linalg.norm(v) + 1e-9
            perp = np.array([-v[1], v[0]]) / L
            c3 = (seg[0] + seg[1]) / 2
            dist = float(np.linalg.norm(c3 - cam.pos))
            if max(r0, r1) * 2 < 2.0 * OL:                       # too thin to fill: an ink member
                late.append((s0, s1, INK, max(2.0, r0 + r1)))
            else:
                n_side = np.cross(seg[1] - seg[0], np.cross(cam.pos - c3, seg[1] - seg[0]))
                lit = np.dot(n_side / (np.linalg.norm(n_side) + 1e-9), LIGHT) > -0.3
                col = _tint(COL[it['col']][0 if lit else 1])
                quad = np.array([s0 + perp * r0, s1 + perp * r1, s1 - perp * r1, s0 - perp * r0])
                polys.append((dist, quad, col))
            depth_all.append(dist)
        elif k == 'line':
            seg = _clip_seg(mv(it['p0']), mv(it['p1']))
            if seg is None:
                continue
            (s0, s1), d = cam.screen(np.array(seg))
            if (d < 1).any():
                continue
            wpx = max(2.0, it['w'] * cam.focal / float(d.mean()))
            col = it['col'] if it['col'] == INK else _tint(it['col'])
            late.append((s0, s1, col, wpx))
        elif k == 'spot':
            pts = mv(it['pts'])
            n = it['n'] @ Rm.T
            if np.dot(n, pts.mean(0) - cam.pos) >= 0:
                continue
            q = _clip_z(list(pts))
            if len(q) < 3:
                continue
            S_, d = cam.screen(np.array(q))
            if (d < 1).any():
                continue
            spots.append((S_, it['col'] if it['col'] in LAMP else _tint(it['col'])))
        elif k == 'text':
            pts = mv(it['quad'])
            n = it['n'] @ Rm.T
            if np.dot(n, pts.mean(0) - cam.pos) >= 0 or (pts[:, 2] < 0).any():
                continue
            S_, d = cam.screen(pts)
            texts.append((S_, it['text']))
    if not polys and not late:
        return None
    allp = np.concatenate([p[1] for p in polys] + [np.array([l[0], l[1]]) for l in late])
    pad = 4 * OL + 8
    x0, y0 = np.floor(allp.min(0)) - pad
    x1, y1 = np.ceil(allp.max(0)) + pad
    x0, y0 = max(x0, -W_), max(y0, -H_)
    x1, y1 = min(x1, 2 * W_), min(y1, 2 * H_)
    bw, bh = int(x1 - x0), int(y1 - y0)
    if bw < 2 or bh < 2:
        return None
    S = ss
    col = Image.new('RGB', (bw * S, bh * S), (0, 0, 0))
    ids = Image.new('I', (bw * S, bh * S), 0)
    dc, di = ImageDraw.Draw(col), ImageDraw.Draw(ids)
    tr = lambda pts: [((x - x0) * S, (y - y0) * S) for x, y in pts]
    for i, (dist, pts, c) in enumerate(sorted(polys, key=lambda p: -p[0])):
        Q = tr(pts)
        dc.polygon(Q, fill=c, outline=c)
        di.polygon(Q, fill=i + 1, outline=i + 1)
    I = np.asarray(ids)
    for pts, c in spots:                                         # framing, lit windows: painted on, no ink
        mask = Image.new('L', col.size, 0)
        ImageDraw.Draw(mask).polygon(tr(pts), fill=255)
        col.paste(c, mask=Image.fromarray(np.where(I > 0, np.asarray(mask), 0).astype(np.uint8)))
    for pts, text in texts:                                      # the board's lettering, laid on in perspective
        Q = tr(pts)
        tw, th = 640, 150
        src = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
        f = _font(118)
        sd = ImageDraw.Draw(src)
        w = sd.textlength(text, font=f)
        sd.text(((tw - w) / 2, 8), text, font=f, fill=INK + (255,))
        # Q runs bottom-left, bottom-right, top-right, top-left
        coeffs = _perspective([(0, th), (tw, th), (tw, 0), (0, 0)], Q)
        warped = src.transform(col.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
        col.paste(warped.convert('RGB'), mask=warped.split()[3])
    # the ink: every change of face, and the outside
    edge = np.zeros(I.shape, bool)
    for dy, dx in ((0, 1), (1, 0)):
        a1 = I[:I.shape[0] - dy, :I.shape[1] - dx]
        a2 = I[dy:, dx:]
        edge[:I.shape[0] - dy, :I.shape[1] - dx] |= a1 != a2
    k = max(3, int(round(OL * S)))
    k = k if k % 2 else k + 1
    ink = np.asarray(Image.fromarray((edge * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(k))) > 0
    alpha = (I > 0) | ink
    out = np.asarray(col).copy()
    out[ink] = INK
    rgba = Image.fromarray(np.dstack([out, (alpha * 255).astype(np.uint8)]), 'RGBA')
    dl = ImageDraw.Draw(rgba)
    for s0, s1, c, wpx in late:                                  # thin members, railings, pipes, ropes
        dl.line(tr([s0, s1]), fill=tuple(c) + (255,), width=max(2, int(round(min(wpx, OL) * S))))
    if S != 1:
        rgba = rgba.resize((bw, bh), Image.LANCZOS)
    bb = rgba.getbbox()
    if not bb:
        return None
    depth = float(np.linalg.norm(mv(piv) - cam.pos))
    return W.Sprite(rgba, (x0, y0), None, (bb[0] + x0, bb[1] + y0, bb[2] + x0, bb[3] + y0), depth, None)


@functools.lru_cache(None)
def _rest(name):
    return render(PARTS[name])


# draw order at rest (far to near), fixed so the jacket and decks layer the same every frame; a moved piece is sorted
# in by its pivot's distance
def _order_key(name, xf):
    p = PARTS[name]
    base = float(np.linalg.norm(p.pivot - CAM.pos))
    if name.startswith('deck_'):
        base += 0.5                                              # decks under what sits on or hangs from them
    if xf is not None:
        base = float(np.linalg.norm(p.pivot + np.asarray(xf[1]) - CAM.pos))
    return -base


def flame(img, t, tip=None, scale=1.0, cam=CAM):
    """The flare's flame: a lumpy tongue licking up and to the right off the tip, yellow inside orange, one ink line;
    flickering (a new shape every 3 frames)."""
    tip = FLARE_TIP if tip is None else tip
    (sx, sy), d = cam.screen(tip)
    k = cam.focal / d * scale
    r = np.random.default_rng(int(t * 8))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(lay)
    for pass_, (col, shrink) in enumerate(((INK, -0.25), ((246, 126, 40), 0.0), ((255, 212, 90), 0.42))):
        pts = []
        n = 11
        for i in range(n):
            f = i / (n - 1)
            h = 6.5 * (1 - shrink * 0.6)                             # m tall
            wd = 2.0 * math.sin(math.pi * min(1, f * 1.15)) * (1 - shrink) + 0.4
            lean = 1.8 * f ** 1.4
            x = (lean + wd * (1 + 0.25 * r.uniform(-1, 1))) * k
            y = -h * f * k
            pts.append((sx + x, sy + y))
        for i in range(n - 1, -1, -1):
            f = i / (n - 1)
            h = 6.5 * (1 - shrink * 0.6)
            wd = 2.0 * math.sin(math.pi * min(1, f * 1.15)) * (1 - shrink) + 0.4
            lean = 1.8 * f ** 1.4
            pts.append((sx + (lean - wd * (1 + 0.25 * r.uniform(-1, 1))) * k, sy - h * f * k))
        if pass_ == 0:
            dr.polygon(pts, fill=INK + (255,), outline=INK + (255,), width=OL * 2)
        else:
            dr.polygon(pts, fill=col + (255,))
    img.alpha_composite(lay)


def foam(img, t, gone=(), cam=CAM):
    """White foam slapping round each standing leg at the waterline, rising and falling with the swell."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(lay)
    for n in LEGS:
        if n in gone:
            continue
        p = _leg_pt(n, 0.0)
        z = float(SEA.sea_z(p[0], p[1], t))
        (sx, sy), d = cam.screen(p + EZ * z)
        k = cam.focal / d
        w = (LEG_R + 2.2) * k
        h = 0.9 * k
        r = np.random.default_rng(int(t * 6) + int(abs(p[0]) * 10) + 1000)
        pts = [(sx - w + 2 * w * i / 10, sy - h * (0.6 + 0.6 * r.random()) * math.sin(math.pi * i / 10)) for i in range(11)]
        pts += [(sx + w * 0.8, sy + h * 0.5), (sx - w * 0.8, sy + h * 0.5)]
        dr.polygon(pts, fill=(240, 236, 238, 255), outline=INK + (255,), width=3)
    img.alpha_composite(lay)


def draw(base, t, xf=None, gone=(), with_flame=True, cam=CAM, extra=()):
    """The rig over a sea painting (RGB or RGBA), pieces in xf moved, pieces in gone left out. extra: other sprites
    (the whales) as [(distance from the camera in m, sprite)], sorted in among the pieces far to near. Returns RGBA."""
    xf = xf or {}
    img = base.convert('RGBA') if base.mode != 'RGBA' else base.copy()
    names = [n for n in PARTS if n not in gone]
    order = [(_order_key(n, xf.get(n)), 0, n) for n in names] + [(-d, 1, k) for k, (d, _) in enumerate(extra)]
    for _, kind, n in sorted(order, key=lambda o: o[0]):
        if kind == 1:
            extra[n][1].paste(img)
            continue
        spr = _rest(n) if n not in xf and cam is CAM else render(PARTS[n], cam, xf.get(n))
        if spr:
            spr.paste(img)
        if n == 'flare_boom' and with_flame and 'flare_boom' not in xf:
            flame(img, t)
    foam(img, t, gone=set(gone) | set(xf), cam=cam)
    return img


def rot(axis, deg):
    """A rotation matrix about a world axis (x, y or z, or a vector) by deg degrees."""
    ax = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}[axis] if isinstance(axis, str) else axis
    ax = np.asarray(ax, float)
    ax = ax / np.linalg.norm(ax)
    a = math.radians(deg)
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K


# ------------------------------------------------- sheet and check --------------------------------------------------
def _label(img, text, size=34):
    SEA._label(img, text, size)


def sheet(out):
    import time
    t0 = time.time()
    sea = SEA.paint(1.0)
    a = draw(sea, 1.0)
    # the pieces numbered: each nudged out from the rig's middle, with its number
    mid = P(25, 17.5, 30)
    b = sea.convert('RGBA')
    xf = {}
    for n, p in PARTS.items():
        off = p.pivot - mid
        off[1] *= 0.3
        xf[n] = (np.eye(3), off * 0.28)
    b = draw(sea, 1.0, xf=xf, with_flame=False)
    db = ImageDraw.Draw(b)
    f = W._font(26)
    for i, (n, p) in enumerate(PARTS.items()):
        (sx, sy), _ = CAM.screen(p.pivot + xf[n][1])
        tx = str(i + 1)
        tw = db.textlength(tx, font=f)
        db.ellipse([sx - 19, sy - 19, sx + 19, sy + 19], fill=(250, 248, 242, 255), outline=INK + (255,), width=3)
        db.text((sx - tw / 2, sy - 15), tx, font=f, fill=INK + (255,))
    # a break test: the right halves of the decks dropped and tipped into the sea, a leg kicked out, the crane over
    hinge = P(25, 17.5, 0)
    tip_r = rot(EV, -24)
    xf2 = {}
    for n in ('deck_cellar_r', 'deck_mezz_r', 'deck_top_r', 'module_a', 'derrick', 'lifeboat_1', 'lifeboat_2',
              'flare_boom'):
        p = PARTS[n].pivot
        new = (p - hinge) @ tip_r.T + hinge + np.array([0, 0, -22.0])
        xf2[n] = (tip_r, new - p)
    xf2['leg_fr'] = (rot(EV, 30), np.array([6.0, -3.0, -8.0]))
    xf2['brace_front_high'] = (rot(EV, 18), np.array([3.0, -2.0, -10.0]))
    xf2['crane_boom'] = (rot(EV, -70), np.array([-6.0, 0.0, -10.0]))
    c = draw(SEA.paint(3.0), 3.0, xf=xf2, gone={'brace_right'})
    # readability: the board and the right end at full size
    d = a.crop((180, 560, 720, 1520)).resize((1080, 1920), Image.LANCZOS)
    panels = [(a, '1  the rig at dusk, whole (flare lit, foam at the legs)'),
              (b, '2  the 31 breakable pieces (numbers: see list)'),
              (c, '3  break test: right half tipped and sinking'),
              (d, '4  close: the JACKDAW board, lit windows, lifeboats')]
    tw, th = 540, 960
    names = list(PARTS)
    listing = Image.new('RGB', (520, th), (250, 248, 242))
    dl = ImageDraw.Draw(listing)
    fs = W._font(17)
    for i, n in enumerate(names):
        dl.text((12, 14 + i * 29), f'{i + 1:2d}  {PARTS[n].label}', font=fs, fill=(30, 30, 34))
    img = Image.new('RGB', (4 * (tw + 10) + 530, th + 10), (250, 248, 242))
    for i, (im, lab) in enumerate(panels):
        im = im.convert('RGB')
        _label(im, lab, 30)
        img.paste(im.resize((tw, th), Image.LANCZOS), (5 + i * (tw + 10), 5))
    img.paste(listing, (5 + 4 * (tw + 10), 5))
    img.save(out, quality=88)
    print(f'{out} ({time.time() - t0:.0f} s)')
    return out


def check():
    import linecheck
    lay = Image.new('RGBA', CAM.size, (0, 0, 0, 0))
    for n in PARTS:
        spr = _rest(n)
        if spr:
            spr.paste(lay)
    found, _ = linecheck.analyse(lay)
    bad = [f'{kd} at ({x}, {y}): {det}' for kd, x, y, det in found]
    print('\n'.join(bad[:30]) if bad else 'rig line work: every shape outlined, one weight')
    return bad


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == 'check':
        check()
    else:
        print(__doc__)
