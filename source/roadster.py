#!/usr/bin/env python3
"""Roadster: the Tesla Roadster 'flying car' demo that keeps flipping, out through the hangar roof, into space and
all the way to Mars, where it lands on Matt Damon ("Fatality Avoided"). Satire style for the car, Damon and the
sets; Dam's coloured pencil (pencil_cartoon) for every space shot. Notes and decisions: notes/roadster.md.

    python3 source/roadster.py cast OUT.jpg     the car from every angle, flipping, jets, the wreck; Damon wide and
                                                his eyes-widening strength sheet (1-6)
    python3 source/roadster.py sets OUT.jpg     the hangar and ramp (with the dials), the Mars set, the two pencil
                                                space shots with the car in them
    python3 source/roadster.py stills OUT.jpg   one still per key moment of every shot, on one sheet
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402  Cam, Local, Pen: flat fills, black outlines
from burnham import INK, dk      # noqa: E402
from satire_style import rough   # noqa: E402
from press_secretary import _clip_convex   # noqa: E402

NAME = 'roadster'
SANS = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')


# ============================================== THE CAR (one 3D model) ==============================================
# Units: centimetres, car-local axes x forward, y to the car's left, z up; origin on the ground under the car's middle.
# The body is a faceted wedge (the real car is all flat angled panels), built from cross-sections front to back.
# Each section: x, then (half-width, height) at the sill bottom, the widest line, the shoulder and the top.
SECTIONS = [
    (232, (70, 24), (80, 34), (74, 42), (46, 44)),     # nose: a blunt wedge
    (204, (92, 18), (100, 36), (96, 56), (62, 60)),
    (122, (96, 16), (102, 40), (98, 68), (70, 72)),    # bonnet
    (58, (96, 16), (102, 42), (98, 74), (66, 82)),     # foot of the windscreen
    (-12, (96, 16), (102, 44), (94, 76), (50, 112)),   # front of the roof
    (-92, (96, 16), (102, 44), (96, 78), (52, 108)),   # back of the roof
    (-172, (96, 18), (102, 46), (98, 80), (70, 84)),   # rear deck
    (-230, (90, 24), (96, 46), (92, 76), (70, 80)),    # tail
]
WHEELS = [(136, 1), (136, -1), (-142, 1), (-142, -1)]   # (x, side); centre height = radius
WHEEL_R, WHEEL_Y, WHEEL_W = 36, 100, 26
BODY = (236, 236, 232)                                 # white paint: lit, mid and shadow tones come from the light
GLASS = (40, 44, 54)
SILL = (34, 34, 38)
TYRE = (26, 26, 28)
RIM = (58, 60, 66)
RED_BAR = (226, 46, 52)
LAMP = (250, 250, 244)
LIGHT = np.array([-0.45, -0.55, 0.70])                 # world: from the upper left, in front of the car
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def _ring(sec):
    x, *pts = sec
    left = [(x, w, z) for w, z in pts]                 # sill, widest, shoulder, top on the left (+y) ...
    right = [(x, -w, z) for w, z in pts]               # ... then from the sill back up the right
    return left[::-1] + right                           # top-left, shoulder-left, ... ; 8 points round the section


def _build():
    """Vertices and faces (with a material) of the body."""
    V, Fc = [], []
    rings = []
    for s in SECTIONS:
        r = _ring(s)
        rings.append(list(range(len(V), len(V) + len(r))))
        V += r
    # ring order: 0 top-L, 1 shoulder-L, 2 widest-L, 3 sill-L, 4 sill-R, 5 widest-R, 6 shoulder-R, 7 top-R
    band_mat = {0: 'upper', 1: 'side', 2: 'sill', 3: 'bottom', 4: 'sill', 5: 'side', 6: 'upper', 7: 'top'}
    for i in range(len(rings) - 1):
        a, b = rings[i], rings[i + 1]
        x0 = SECTIONS[i][0]
        for k in range(8):
            k2 = (k + 1) % 8
            band = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}[k]
            m = band_mat[band]
            if m == 'upper' and 58 >= x0 > -172:        # the greenhouse sides: dark glass
                m = 'glass'
            if m == 'top' and 58 >= x0 > -172:          # windscreen, glass roof, rear glass
                m = 'glass'
            if m in ('upper', 'top'):
                m = 'body'
            if m == 'side':
                m = 'body'
            Fc.append(([a[k], b[k], b[k2], a[k2]], m))
    Fc.append((rings[0][::-1], 'nose'))
    Fc.append((rings[-1], 'tail'))
    return np.array(V, float), Fc


VERTS, FACES = _build()
CENTRE = np.array([0.0, 0.0, 55.0])


def rot(axis, a):
    c, s = math.cos(a), math.sin(a)
    if axis == 'x':
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == 'y':
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


class View:
    """Car-local points to the screen. yaw turns the car on the ground (0 = nose to screen right, we see its right
    side; 90 = nose towards us), elev lifts the camera (degrees above the horizon), flip is the car's own
    nose-over-tail rotation and roll its barrel roll (degrees); the car turns about its middle. Mild perspective."""
    def __init__(self, yaw=0.0, elev=12.0, flip=0.0, roll=0.0, focal=2600.0):
        Rc = rot('x', math.radians(roll)) @ rot('y', math.radians(flip))
        Rw = rot('x', math.radians(elev)) @ rot('z', math.radians(-yaw))
        self.R = Rw @ Rc
        self.Rc = Rc
        self.focal = focal

    def world(self, p):
        """Car-local -> world (x right, y away from the camera, z up), about the car's middle."""
        return (np.asarray(p, float) - CENTRE) @ self.R.T

    def screen(self, q):
        q = np.atleast_2d(q)
        k = self.focal / (self.focal + q[:, 1])
        return np.stack([q[:, 0] * k, -q[:, 2] * k], 1), q[:, 1]


def crumple(V, k, seed=7):
    """The wreck: roof caved in, front and back folded towards the middle, everything buckled; k 0..1."""
    if k <= 0:
        return V
    r = np.random.default_rng(seed)
    V = V.copy()
    x, z = V[:, 0], V[:, 2]
    V[:, 0] = x - np.sign(x) * k * np.clip(np.abs(x) - 50, 0, None) * 0.34          # folded towards the middle
    top = np.clip((z - 24) / 80, 0, 1)
    V[:, 2] = z - k * top * (z - 24) * 0.62                                           # flattened from above
    V[:, 2] += k * 26 * np.clip(np.abs(x) / 230, 0, 1) ** 2 * top                     # ends kicked up: a V fold
    V[:, 1] *= 1 + k * 0.32 * top                                                     # bulging out as it squashes
    V += r.normal(0, 1, V.shape) * k * np.array([16, 14, 9])                          # buckled panels
    return V


def car(img, cam, x, y, s, view, jets=0.0, crush=0.0, headlight=False, t=0.0, smoke=True):
    """Draw the Roadster with its middle at world (x, y), s world pixels per cm. jets 0..1: the four underside
    cold-gas jets (the 'hydraulics'); crush 0..1: the wreck; headlight: one corner lamp lit on the wreck."""
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    V = crumple(VERTS, crush)
    Wv = view.world(V)
    P2, D = view.screen(Wv)
    cam_pos = np.array([0.0, -view.focal, 0.0])

    def wpt(pt):
        return view.screen(view.world(np.array(pt, float)))[0][0]

    # the jets go first: the body covers their nozzles
    if jets > 0:
        down = view.Rc @ np.array([0, 0, -1.0])
        for jx, jy in ((70, 52), (70, -52), (-80, 52), (-80, -52)):
            _jet(p, view, (jx, jy, 14), down, jets, t, seed=jx + jy)

    # wheels: far ones before the body, near ones after
    wheel_draws = []
    for wx, side in WHEELS:
        c3 = np.array([wx, side * WHEEL_Y, WHEEL_R], float)
        if crush > 0:
            c3 += np.array([-np.sign(wx) * 40 * crush, side * 30 * crush, -14 * crush])
        depth = view.world(c3)[1]
        wheel_draws.append((depth, wx, side, c3))
    centre_depth = view.world(CENTRE)[1]
    def near(side):                                  # a wheel on the side of the car facing us
        return (view.world(CENTRE + np.array([0, side, 0.0])) - view.world(CENTRE))[1] < 0
    for depth, wx, side, c3 in sorted(wheel_draws, key=lambda w: -w[0]):
        if not near(side):
            _wheel(p, view, c3, side, crush)

    # the body: faces facing us, far to near; fills, then the edges that are creases, silhouettes or colour changes
    vis = []
    for idx, (fi, m) in enumerate(FACES):
        q = Wv[fi]
        n = np.cross(q[1] - q[0], q[2] - q[0])
        if np.linalg.norm(n) < 1e-6:
            n = np.cross(q[2] - q[0], q[3 % len(q)] - q[0])
        n = n / (np.linalg.norm(n) + 1e-9)
        cen = q.mean(0)
        out = cen - view.world(CENTRE + np.array([0, 0, 0]))
        if np.dot(n, out) < 0:
            n = -n
        facing = np.dot(n, cen - cam_pos) < 0 or crush > 0      # a wreck is not a closed shape: draw every panel
        vis.append((idx, facing, n, cen[1]))
    order = sorted([v for v in vis if v[1]], key=lambda v: -v[3])
    for idx, _, n, _ in order:
        fi, m = FACES[idx]
        p.poly([tuple(P2[i]) for i in fi], _tone(m, n), None)
    facing = {v[0]: v[1] for v in vis}
    normal = {v[0]: v[2] for v in vis}
    edges = {}
    for idx, (fi, m) in enumerate(FACES):
        for a, b in zip(fi, fi[1:] + fi[:1]):
            edges.setdefault((min(a, b), max(a, b)), []).append(idx)
    for (a, b), fs in edges.items():
        shown = [f for f in fs if facing[f]]
        if not shown:
            continue
        draw = len(fs) == 1 or len(shown) == 1
        if not draw and len(fs) == 2:
            f0, f1 = fs
            crease = np.dot(normal[f0], normal[f1]) < math.cos(math.radians(14))
            draw = crease or FACES[f0][1] != FACES[f1][1]
        if draw:
            p.line([tuple(P2[a]), tuple(P2[b])], INK, 3.2)

    # details laid on the body (only when the face they sit on is towards us)
    nose_face = len(FACES) - 2
    tail_face = len(FACES) - 1
    if facing[nose_face]:
        bar = [tuple(wpt(_crushed((233, w, 33), crush))) for w in (-44, 44)]
        p.line(bar, INK, 6.0)
        p.line(bar, LAMP if not crush else (120, 120, 120), 3.0)
    lit_side = 1 if (view.world(CENTRE + np.array([0, 1.0, 0])) - view.world(CENTRE))[1] < 0 else -1
    for side in (1, -1):                             # the triangular corner headlamps on the nose
        if facing[nose_face]:
            tri = [(234, side * 48, 42), (234, side * 74, 41), (234, side * 70, 34)]
            lit = (not crush) or (headlight and side == lit_side)
            p.poly([tuple(wpt(_crushed(q, crush))) for q in tri], LAMP if lit else (90, 92, 96), INK, 2.0)
            if headlight and side == lit_side and crush:
                cx, cy = wpt(_crushed((234, side * 64, 39), crush))
                for k in range(7):                    # short rays: a lit lamp, drawn flat
                    a = k * 0.9
                    p.line([(cx + 12 * math.cos(a), cy + 12 * math.sin(a)),
                            (cx + 34 * math.cos(a), cy + 34 * math.sin(a))], INK, 5.0)
                    p.line([(cx + 12 * math.cos(a), cy + 12 * math.sin(a)),
                            (cx + 34 * math.cos(a), cy + 34 * math.sin(a))], (255, 246, 170), 2.6)
    if crush > 0.5:                                  # the glass smashed: cracks across every pane we see
        rr = np.random.default_rng(9)
        for idx, _, n, _ in order:
            fi, m = FACES[idx]
            if m == 'glass':
                q = np.array([P2[i] for i in fi])
                c0 = q.mean(0) + rr.normal(0, 4, 2)
                for _ in range(4):
                    tgt = q[rr.integers(len(q))] * 0.7 + c0 * 0.3
                    mid = (c0 + tgt) / 2 + rr.normal(0, 3, 2)
                    p.line([tuple(c0), tuple(mid), tuple(tgt)], (190, 198, 210), 1.8)
    if facing[tail_face]:
        bar = [wpt(_crushed((-231, w, 66), crush)) for w in (-88, 88)]
        p.line(bar, RED_BAR, 5.0)
        plate = [(-231, -18, 50), (-231, 18, 50), (-231, 18, 38), (-231, -18, 38)]
        p.poly([tuple(wpt(_crushed(q, crush))) for q in plate], (240, 240, 236), INK, 1.6)
        for ex in (-54, -30, 30, 54):
            cx, cy = wpt(_crushed((-231, ex, 32), crush))
            p.ell(cx, cy, 4.5, 4.5, (180, 150, 90), INK, 1.4)
    _wing(p, view, crush, wpt)

    for depth, wx, side, c3 in sorted(wheel_draws, key=lambda w: -w[0]):
        if near(side):
            _wheel(p, view, c3, side, crush)


def _crushed(q, k):
    return tuple(crumple(np.array([q], float), k, seed=7)[0]) if k else q


def _face_index(section, band):
    return section * 8 + band


def _tone(m, n):
    lit = float(np.dot(n, LIGHT))
    base = {'body': BODY, 'nose': BODY, 'tail': BODY, 'glass': GLASS, 'sill': SILL, 'bottom': (92, 94, 102)}[m]
    k = 1.0 if lit > 0.35 else (0.86 if lit > -0.1 else 0.7)       # three flat tones: lit, side, shadow
    if m == 'glass':
        k = 1.0 if lit > 0.2 else 0.8
    return tuple(int(v * k) for v in base)


def _wing(p, view, crush, wpt):
    """The tall rear wing: a flat plate on two struts."""
    tilt = crush * 0.5
    plate = [(-196, 96, 120), (-196, -96, 120), (-250, -96, 126 + 30 * tilt), (-250, 96, 126 + 30 * tilt)]
    for sy in (40, -40):
        p.line([tuple(wpt(_crushed((-210, sy, 82), crush))), tuple(wpt(_crushed((-214, sy, 120), crush)))], INK, 5.0)
        p.line([tuple(wpt(_crushed((-210, sy, 82), crush))), tuple(wpt(_crushed((-214, sy, 120), crush)))],
               (70, 72, 78), 2.6)
    q = [tuple(wpt(_crushed(c, crush))) for c in plate]
    n = view.world(np.array([0, 0, 1.0]) + CENTRE) - view.world(CENTRE)
    p.poly(q, (224, 224, 220) if n[1] < 0 else (150, 152, 158), INK, 3.0)


def _wheel(p, view, c3, side, crush):
    """A tyre with a dark six-spoke rim, seen at any angle (a 3D disc projected)."""
    camber = math.radians(25 * crush) * side
    ax = np.array([0, side * math.cos(camber), math.sin(camber)])           # the axle, out of the car's side
    u = np.array([1.0, 0, 0])
    v = np.cross(ax, u)
    ring = lambda r, off: [c3 + ax * off + r * (math.cos(a) * u + math.sin(a) * v)
                           for a in np.linspace(0, 2 * math.pi, 28, endpoint=False)]
    outer, inner = ring(WHEEL_R, WHEEL_W / 2), ring(WHEEL_R, -WHEEL_W / 2)
    P = lambda pts: [tuple(view.screen(view.world(np.array(pts, float)))[0][i]) for i in range(len(pts))]
    po, pi = P(outer), P(inner)
    hull = _hull(po + pi)
    p.poly(hull, TYRE, INK, 3.0)                                             # the tread, all round
    cam_side = view.world(c3 + ax) - view.world(c3)
    if cam_side[1] < 0:                                                      # the outer face is towards us
        p.poly(po, TYRE, INK, 2.4)
        p.poly(P(ring(WHEEL_R * 0.7, WHEEL_W / 2 + 0.5)), RIM, INK, 2.0)
        hub = P([c3 + ax * (WHEEL_W / 2 + 1)])[0]
        for k in range(6):
            a = k * math.pi / 3 + 0.3
            tip = P([c3 + ax * (WHEEL_W / 2 + 1) + WHEEL_R * 0.66 * (math.cos(a) * u + math.sin(a) * v)])[0]
            p.line([hub, tip], (150, 154, 162), 3.2)
        p.ell(hub[0], hub[1], 4, 4, (150, 154, 162), INK, 1.2)


def _hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], q) <= 0:
            hi.pop()
        hi.append(q)
    return lo[:-1] + hi[:-1]


def _jet(p, view, nozzle, down, k, t, seed=0):
    """One cold-gas jet: a white plume blasting out of the underside, flat and lumpy, with a pale blue core."""
    r = np.random.default_rng(abs(seed) * 31 + int(t * 12))
    base = view.world(np.array(nozzle, float))
    d = view.R @ np.array([0, 0, -1.0])
    length = 280 * k
    pts_l, pts_r = [], []
    for i in range(11):
        f = i / 10
        c = base + d * length * f
        w = 7 + 52 * f ** 1.3 + r.uniform(-5, 5) * f + 6 * math.sin(f * 9 + t * 20 + seed) * f
        sx, _ = view.screen(c)
        off = np.cross(d, np.array([0, 1.0, 0]))
        if np.linalg.norm(off) < 0.2:
            off = np.array([1.0, 0, 0])
        off = off / np.linalg.norm(off)
        a, _ = view.screen(c + off * w)
        b, _ = view.screen(c - off * w)
        pts_l.append(tuple(a[0]))
        pts_r.append(tuple(b[0]))
    end = base + d * length
    e2, _ = view.screen(end)
    p.poly(pts_l + pts_r[::-1], (246, 248, 252), INK, 2.4)
    for j in range(3):                                         # the plume ends in a lumpy puff
        o = np.array([r.uniform(-1, 1), 0, r.uniform(-1, 1)]) * 30 * k
        q, _ = view.screen(end + o)
        p.ell(q[0][0], q[0][1], 30 * k + 8 * j, 22 * k + 6 * j, (246, 248, 252), INK, 2.0)
    core_l = [((a[0] * 2 + b[0]) / 3, (a[1] * 2 + b[1]) / 3) for a, b in zip(pts_l[:7], pts_r[:7])]
    core_r = [((a[0] + b[0] * 2) / 3, (a[1] + b[1] * 2) / 3) for a, b in zip(pts_l[:7], pts_r[:7])]
    p.poly(core_l + core_r[::-1], (170, 206, 240), None)


def debris(img, cam, x, y, s, seed=11, spread=1.0):
    """What flew off at the crush, lying where it landed (each piece its own size): glass shards, white panel
    pieces, a bent bit of trim, a hubcap. Ground level is y; s world pixels per cm."""
    r = np.random.default_rng(seed)
    p = B.Pen(img, cam)
    for i in range(26):
        dx = r.normal(0, 1) * 170 * spread * s
        dy = r.uniform(0.05, 0.5) * 60 * s
        k = r.uniform(9, 24) * s
        a = r.uniform(0, 6.28)
        pts = [(x + dx + k * math.cos(a + j * 2.1 + r.uniform(-0.4, 0.4)),
                y + dy + 0.45 * k * math.sin(a + j * 2.1)) for j in range(3)]
        kind = i % 4
        colr = (200, 212, 226) if kind < 2 else (BODY if kind == 2 else (60, 62, 68))
        p.poly(pts, colr, INK, 1.6)
    hx = x + 250 * spread * s
    p.ell(hx, y + 10 * s, 26 * s, 9 * s, RIM, INK, 2.0)
    p.ell(hx, y + 10 * s, 8 * s, 3 * s, (150, 154, 162), None)


def smoke_cloud(img, cam, x, y, w, h, seed, fill=(232, 234, 238), shade=(196, 200, 208)):
    """Ground smoke from the jets: lumpy flat puffs with one outline round the whole cloud and a flat shadow side."""
    r = np.random.default_rng(seed)
    p = B.Pen(img, cam)
    lumps = [(x + r.uniform(-w, w) * 0.5, y - abs(r.normal(0, h * 0.25)), r.uniform(0.18, 0.32) * w,
              r.uniform(0.5, 0.8) * h) for _ in range(9)]
    for lx, ly, rx, ry in lumps:
        p.ell(lx, ly, rx + 4, ry + 4, INK, None)
    for lx, ly, rx, ry in lumps:
        p.ell(lx, ly, rx, ry, shade, None)
    for lx, ly, rx, ry in lumps:
        p.ell(lx - rx * 0.12, ly - ry * 0.14, rx * 0.86, ry * 0.8, fill, None)


# ================================================ DAMON (Mark Watney) ===============================================
# Person units as in the rest of the series: neck base at (0, 0), y down, soles at 928, head about 190 tall.
SUIT_OR = (206, 92, 46)       # the orange-red panels
SUIT_OR_D = (160, 64, 34)
SUIT_GR = (182, 176, 166)     # silver-grey
SUIT_GR_D = (138, 132, 124)
SUIT_WH = (234, 232, 226)
GLOVE = (72, 72, 78)
VISOR = (214, 160, 58)
VISOR_D = (168, 116, 38)
SKIN = (238, 192, 162)
HAIR = (112, 80, 52)


def damon(img, cam, x, y, s, st=None, t=0.0):
    """Watney in his suit, front view. st: look_up 0..1, wide 1..6 (the eyes-widening strength), visor_car
    (0..1, the car's reflection growing in the gold visor)."""
    st = dict(dict(look_up=0.6, wide=1, visor_car=0.0), **(st or {}))
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    R = lambda pts, sd, a=4: rough(pts, a, sd)
    # backpack showing past the shoulders
    p.poly(R([(-170, -10), (170, -10), (176, 260), (-176, 260)], 1), SUIT_WH, INK, 4)
    # legs and boots
    for sgn in (-1, 1):
        lx = sgn * 50
        p.poly(R([(lx - 46, 420), (lx + 46, 420), (lx + 42, 860), (lx - 40, 860)], 10 + sgn), SUIT_GR, INK, 4)
        p.poly(R([(lx + sgn * 30 - 10, 440), (lx + sgn * 30 + 10, 440), (lx + sgn * 30 + 9, 840),
                  (lx + sgn * 30 - 9, 840)], 12 + sgn, 2), SUIT_OR, INK, 3)
        p.poly(R([(lx - 34, 670), (lx + 34, 670), (lx + 32, 740), (lx - 32, 740)], 14 + sgn), (120, 120, 124), INK, 3.4)
        p.poly(R([(lx - 50, 850), (lx + 52, 850), (lx + 58, 928), (lx - 54, 928)], 16 + sgn), (160, 160, 164), INK, 4)
        p.line([(lx - 52, 902), (lx + 56, 902)], INK, 2.4)
    # torso: grey, orange panels over the shoulders and chest, a belt
    p.poly(R([(-150, 30), (150, 30), (124, 450), (-124, 450)], 20), SUIT_GR, INK, 4.4)
    for sgn in (-1, 1):
        p.poly(R([(sgn * 150, 30), (sgn * 70, 26), (sgn * 64, 180), (sgn * 138, 210)], 22 + sgn), SUIT_OR, INK, 3.4)
    p.poly(R([(-124, 380), (124, 380), (122, 418), (-122, 418)], 24, 2), (90, 88, 86), INK, 3)
    p.poly(R([(-18, 384), (18, 384), (18, 414), (-18, 414)], 25, 1), (196, 170, 90), INK, 2)
    # the chest control box and the ARES III strap
    p.poly(R([(-58, 110), (58, 110), (56, 232), (-56, 232)], 26, 3), SUIT_WH, INK, 3.4)
    for i, c in enumerate([(70, 140, 200), (210, 60, 50), (240, 200, 70), (60, 60, 64)]):
        p.ell(-34 + i * 22, 140, 7, 7, c, INK, 1.6)
    p.poly(R([(-40, 168), (40, 168), (40, 214), (-40, 214)], 27, 2), (80, 84, 92), INK, 2.4)
    p.poly(R([(66, 40), (96, 40), (92, 330), (62, 330)], 28, 2), SUIT_OR_D, INK, 3)
    _text(img, L, 80, 120, 'ARES III', 16, (240, 236, 228), vertical=True)
    # shoulder patches: the flag and the red 2
    _flag(p, -118, 70, 0.55)
    _text(img, L, 112, 64, '2', 30, (200, 40, 40))
    # arms hanging a little out from the bulk of the suit, dark gloves (plain circles)
    for sgn in (-1, 1):
        sh, el, wr = (sgn * 140, 60), (sgn * 172, 260), (sgn * 166, 420)
        _sleeve(p, sh, el, 72, SUIT_OR)
        _sleeve(p, el, wr, 64, SUIT_GR)
        p.ell(wr[0], wr[1] + 30, 34, 34, GLOVE, INK, 3.4)
        p.line([(wr[0] - 18, wr[1] + 20), (wr[0] + 18, wr[1] + 20)], (170, 172, 178), 3)
    _helmet(img, p, L, st, t)


def _sleeve(p, a, b, w, col):
    d = np.array(b, float) - np.array(a, float)
    n = np.array([-d[1], d[0]]) / (np.linalg.norm(d) + 1e-9) * w / 2
    pts = [tuple(np.array(a) + n), tuple(np.array(b) + n * 0.94), tuple(np.array(b) - n * 0.94), tuple(np.array(a) - n)]
    p.poly(pts, col, INK, 4)
    p.ell(a[0], a[1], w / 2, w / 2, col, None)


def _flag(p, x, y, k):
    w, h = 60 * k, 36 * k
    p.poly([(x - w, y - h), (x + w, y - h), (x + w, y + h), (x - w, y + h)], (236, 236, 236), INK, 1.6)
    for i in range(4):
        yy = y - h + (i * 2 + 0.5) * h / 3.6
        p.poly([(x - w, yy), (x + w, yy), (x + w, yy + h / 7), (x - w, yy + h / 7)], (200, 40, 48), None)
    p.poly([(x - w, y - h), (x - w * 0.15, y - h), (x - w * 0.15, y), (x - w, y)], (40, 54, 120), None)
    p.poly([(x - w, y - h), (x + w, y - h), (x + w, y + h), (x - w, y + h)], None, INK, 1.6)


def _text(img, L, x, y, s, size, fill, vertical=False):
    px = max(6, int(L.S(size)))
    f = ImageFont.truetype(SANS, px)
    if vertical:
        tw = int(f.getlength(s)) + 4
        lay = Image.new('RGBA', (tw, px + 6), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((2, 0), s, font=f, fill=fill)
        lay = lay.rotate(90, expand=True)
        cx, cy = L.P(x, y)
        img.alpha_composite(lay, (int(cx - lay.width / 2), int(cy)))
    else:
        cx, cy = L.P(x, y)
        ImageDraw.Draw(img).text((cx, cy), s, font=f, fill=fill, anchor='mm')


def _helmet(img, p, L, st, t):
    """The bubble helmet: the face inside, the gold visor over the top half, the orange-and-white shell round it."""
    hx, hy, R = 0, -150, 142
    # the shell behind the bubble (white, orange at the collar), lamps on both sides
    p.poly(rough([(hx + R * 1.08 * math.cos(a), hy + R * 1.06 * math.sin(a))
                  for a in np.linspace(math.pi * 0.95, math.pi * 2.05, 30)] +
                 [(hx + 100, hy + 150), (hx - 100, hy + 150)], 2, 40), SUIT_WH, INK, 4)
    for sgn in (-1, 1):
        p.poly(rough([(sgn * 132, -270), (sgn * 166, -270), (sgn * 166, -222), (sgn * 132, -222)], 2, 41 + sgn),
               (200, 200, 204), INK, 3)
        p.ell(sgn * 149, -246, 10, 10, (250, 248, 230), INK, 2)
    p.poly([(hx + R * math.cos(a), hy + R * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 48, endpoint=False)],
           (226, 230, 230), None)                          # what's seen through the glass behind his head
    _face(img, p, st, hx, hy + 4)
    # the visor: gold, over the top half, its edge just above the brows
    vy = hy - 46 - 10 * st['look_up']
    top = [(hx + R * math.cos(a), hy + R * math.sin(a)) for a in np.linspace(math.pi * 1.06, math.pi * 1.94, 30)]
    edge = [(hx + R * 0.92 * u, vy + 18 * (1 - u * u)) for u in np.linspace(0.995, -0.995, 20)]
    p.poly(top + edge, VISOR, None)
    p.poly([(hx - R * 0.55, hy - R * 0.86), (hx - R * 0.15, hy - R * 0.98), (hx - R * 0.42, vy + 8),
            (hx - R * 0.78, vy + 2)], VISOR_D, None)
    if st['visor_car'] > 0:                                # the car's reflection, growing as it falls on him
        k = st['visor_car']
        cx, cy = hx + 20, hy - R * 0.6
        w = 16 + 60 * k
        p.poly([(cx - w, cy + w * 0.2), (cx - w * 0.3, cy - w * 0.25), (cx + w * 0.6, cy - w * 0.2),
                (cx + w, cy + w * 0.15), (cx - w * 0.9, cy + w * 0.3)], (250, 244, 220), INK, 1.6)
    p.line(edge, INK, 3.2)
    p.line([(hx + R * 0.36, hy - R * 0.8), (hx + R * 0.62, hy - R * 0.6)], (250, 226, 160), 3)   # a glint line
    p.poly([(hx + R * math.cos(a), hy + R * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 48, endpoint=False)],
           None, INK, 4.4)
    # the collar ring
    p.poly(rough([(-104, -12), (104, -12), (112, 22), (-112, 22)], 3, 44), SUIT_OR, INK, 4)


def _face(img, p, st, hx, hy):
    """Damon's face (from Sam's refs 19-24): a broad, square head and jaw, a dimpled chin, strong straight brows over
    smallish deep-set blue eyes, a rounded nose, thin wide lips, short brown hair with the fringe pushed up, light
    stubble, no moustache; a thick neck going down into the dark inside of the suit. wide 1..6 opens the eyes from a
    hopeful look to a huge frozen stare, the brows rising with it."""
    k = (st['wide'] - 1) / 5.0
    up = st['look_up']
    R = 142
    # the dark inside of the suit, seen through the bottom of the bubble, and the neck rising out of it
    p.poly(rough([(hx - 46, hy + 60), (hx + 46, hy + 60), (hx + 56, -10), (hx - 56, -10)], 1.5, 49), SKIN, INK, 2.6)
    a0 = math.asin(0.8)                                           # the suit's dark inside: the bubble below one flat
    inner = [(hx + R * math.cos(a), -150 + R * math.sin(a)) for a in np.linspace(a0, math.pi - a0, 30)]
    p.poly(inner, (58, 58, 64), None)                             # line straight across, over the neck (Sam, 16 Oct)
    for sgn in (-1, 1):                                           # ears, standing out a little
        p.poly(rough([(hx + sgn * 74 + sgn * 11 * math.cos(a), hy + 4 + 21 * math.sin(a))
                      for a in np.linspace(0, 2 * math.pi, 16, endpoint=False)], 1.2, 50 + sgn), SKIN, INK, 2.6)
    head = [(hx - 26, hy + 84), (hx - 60, hy + 54), (hx - 72, hy + 10), (hx - 72, hy - 40), (hx - 60, hy - 76),
            (hx - 30, hy - 94), (hx + 30, hy - 94), (hx + 60, hy - 76), (hx + 72, hy - 40), (hx + 72, hy + 10),
            (hx + 60, hy + 54), (hx + 26, hy + 84), (hx, hy + 90)]
    p.poly(rough(head, 1.5, 52), SKIN, INK, 2.8)
    p.poly([(hx - 26, hy + 76), (hx - 52, hy + 52), (hx - 62, hy + 30), (hx - 50, hy + 44), (hx - 22, hy + 66), (hx, hy + 70),
            (hx + 22, hy + 66), (hx + 50, hy + 44), (hx + 62, hy + 30), (hx + 52, hy + 52), (hx + 26, hy + 76),
            (hx, hy + 82)], dk(SKIN, 0.93), None)                                                   # light stubble
    p.line([(hx, hy + 76), (hx + 1, hy + 85)], dk(SKIN, 0.72), 2.2)                                # the chin dimple
    hair = [(hx - 72, hy - 30), (hx - 70, hy - 70), (hx - 44, hy - 96), (hx - 6, hy - 104), (hx + 30, hy - 108),
            (hx + 58, hy - 92), (hx + 74, hy - 62), (hx + 72, hy - 30), (hx + 64, hy - 56), (hx + 40, hy - 70),
            (hx + 18, hy - 78), (hx - 6, hy - 70), (hx - 30, hy - 66), (hx - 56, hy - 54)]
    p.poly(rough(hair, 1.5, 54), HAIR, INK, 2.6)
    p.line([(hx + 10, hy - 98), (hx + 24, hy - 84)], dk(HAIR, 0.8), 2.0)                          # the fringe pushed up
    p.line([(hx - 20, hy - 94), (hx - 10, hy - 80)], dk(HAIR, 0.8), 2.0)
    for sgn in (-1, 1):
        ex, ey = hx + sgn * 30, hy - 8
        p.line([(ex - 14, ey - 13), (ex + 14, ey - 13)], dk(SKIN, 0.82), 2.0)                     # deep-set: lid crease
        _eye(p, ex, ey, sgn, k, up)
        br = ey - 21 - 3 * up - 15 * k
        inner_x, outer_x = ex - sgn * 18, ex + sgn * 19
        p.poly([(inner_x, br + 1), (ex, br - 2), (outer_x, br + 2), (outer_x, br + 7), (ex, br + 4), (inner_x, br + 7)],
               dk(HAIR, 0.78), None)                                                                 # strong straight brows
    p.line([(hx - 3, hy - 6), (hx - 7, hy + 22)], dk(SKIN, 0.7), 2.0)                            # nose: bridge, round tip
    p.poly(rough([(hx - 14, hy + 24), (hx - 6, hy + 32), (hx + 6, hy + 33), (hx + 14, hy + 25), (hx + 6, hy + 28),
                  (hx - 6, hy + 28)], 0.8, 56), dk(SKIN, 0.86), None)
    for sgn in (-1, 1):
        p.line([(hx + sgn * 12, hy + 30), (hx + sgn * 6, hy + 32)], INK, 1.8)
        p.line([(hx + sgn * 26, hy + 30), (hx + sgn * 30, hy + 52)], dk(SKIN, 0.82), 1.8)          # smile lines
    if k > 0.55:                                                   # lips part at the biggest strengths
        o = 3 + 9 * (k - 0.55) / 0.45
        p.poly([(hx - 14, hy + 54), (hx + 14, hy + 54), (hx + 11, hy + 54 + o), (hx - 11, hy + 54 + o)], (110, 50, 46),
               INK, 2.0)
    else:                                                          # thin, wide, a hopeful lift at the corners
        p.line([(hx - 20, hy + 52), (hx - 8, hy + 55), (hx + 8, hy + 55), (hx + 20, hy + 52 - 2 * (1 - k))], INK, 2.4)


def _eye(p, ex, ey, sgn, k, up):
    """One opening between two lids, the iris cut to it (no line ever crosses the white)."""
    w, h = 15 + 3 * k, 5 + 10 * k
    us = np.linspace(-1, 1, 15)
    upper = [(ex + w * u, ey - h * (1 - u * u)) for u in us]
    lower = [(ex + w * u, ey + (4 + 6 * k) * (1 - u * u)) for u in us]
    opening = upper + lower[::-1][1:-1]
    p.poly(opening, (252, 252, 250), None)
    cx, cy = ex, ey - 3 * up - 2 * k
    r_iris = 8.5 - 2.2 * k
    circ = lambda r: [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24, endpoint=False)]
    iris = _clip_convex(opening[::-1], circ(r_iris))
    if len(iris) >= 3:
        p.poly(iris, (86, 132, 178), None)
    pupil = _clip_convex(opening[::-1], circ(r_iris * 0.48))
    if len(pupil) >= 3:
        p.poly(pupil, INK, None)
    p.line(lower, INK, 1.6)
    p.line(upper, INK, 3.0)


# ================================================ THE SETS =========================================================
def hangar(img, cam, t=0.0):
    """The dark hangar: the ramp (grey concrete, red neon edges, a white centre line) curving up from a floor plate
    to nearly vertical, a steel scaffold tower behind its right side, roof beams and lights high up, a lit board."""
    p = B.Pen(img, cam)
    p.poly([(-200, -200), (1280, -200), (1280, 2200), (-200, 2200)], (14, 14, 18), None)
    for i in range(7):                                         # roof trusses, faint in the dark
        y = 120 + i * 34
        p.line([(-100, y), (1180, y - 20)], (34, 34, 42), 3)
    for i in range(14):
        x = 30 + i * 80
        p.line([(x, 110), (x + 40, 330)], (30, 30, 38), 2)
        p.ell(x + 10, 150 + 6 * (i % 3), 4, 4, (220, 220, 200), None)
    # the back wall: tall panels and a green exit sign, no new jokes (Sam, 16 Oct: only what the script has)
    for i in range(9):
        x = 20 + i * 130
        p.line([(x, 360), (x, 1290)], (26, 26, 32), 2)
    p.poly(rough([(80, 1150), (190, 1150), (190, 1196), (80, 1196)], 2, 60), (40, 150, 80), INK, 2)
    _text(img, cam, 135, 1173, 'EXIT', 20, (230, 250, 230))
    # floor
    p.poly([(-200, 1300), (1280, 1300), (1280, 2200), (-200, 2200)], (36, 36, 42), None)
    p.line([(-200, 1300), (1280, 1300)], (60, 60, 68), 2)
    for i in range(6):
        p.line([(-200 + i * 260, 2200), (300 + i * 110, 1300)], (46, 46, 54), 2)
    # the ramp's centre line: a curve from the floor plate (bottom) up to near-vertical (top)
    base, top = (640, 1300), (520, 380)
    def spine(u):                                              # u 0 at the foot .. 1 at the top
        x = base[0] + (top[0] - base[0]) * u ** 2.2 + 70 * math.sin(u * math.pi) * 0.6
        y = base[1] - (base[1] - top[1]) * (1 - (1 - u) ** 1.6)
        return x, y
    # the scaffold tower behind the right edge
    for u in np.linspace(0.05, 0.95, 12):
        x, y = spine(u)
        x2, y2 = spine(min(1.0, u + 0.075))
        p.line([(x + 110, y), (x2 + 110, y2)], (76, 78, 86), 3)
        p.line([(x + 170, y), (x2 + 170, y2)], (76, 78, 86), 3)
        p.line([(x + 110, y), (x2 + 170, y2)], (60, 62, 70), 2)
        p.line([(x + 170, y), (x2 + 110, y2)], (60, 62, 70), 2)
    us = np.linspace(0, 1, 30)
    half = lambda u: 120 - 55 * u                              # narrower with height (further away)
    left = [(spine(u)[0] - half(u), spine(u)[1]) for u in us]
    right = [(spine(u)[0] + half(u), spine(u)[1]) for u in us]
    p.poly(left + right[::-1], (196, 196, 194), INK, 3)
    p.poly([(spine(u)[0] - half(u) * 0.2, spine(u)[1]) for u in us[:20]] +
           [(spine(u)[0] - half(u) * 0.9, spine(u)[1]) for u in us[:20]][::-1], (176, 176, 176), None)   # a flat shadow side
    p.line(left, (240, 70, 64), 9)
    p.line(right, (240, 70, 64), 9)
    p.line([spine(u) for u in us], (246, 246, 240), 3)
    p.poly(rough([(470, 1290), (820, 1290), (850, 1330), (440, 1330)], 2, 61), (150, 150, 152), INK, 3)  # floor plate
    return spine


def dials(img, cam, g=1.0, alt=0.0, pitch=0.0):
    """The demo's two dials, kept as they are, with whatever numbers the story needs (G-FORCE left, ALTITUDE right)."""
    p = B.Pen(img, cam)
    for x, label, val, unit in ((150, 'G-FORCE', g, 'G'), (830, 'ALTITUDE', alt, 'FT')):
        p.ell(x, 1400, 62, 62, (14, 14, 18), (220, 220, 220), 2.4)
        p.line([(x + 62 * math.cos(a), 1400 + 62 * math.sin(a)) for a in np.linspace(2.2, 2.2 + 4.3 * min(1, abs(val) / 70 + 0.15), 20)],
               (250, 250, 250), 4)
        _text(img, cam, x, 1376, label, 10, (210, 210, 210))
        if abs(val) < 1e5:
            _text(img, cam, x, 1404, _num(val), 22 if abs(val) < 1e4 else 17, (250, 250, 250))
        else:                                                 # too long for the dial: on a dark plate under it
            txt = _num(val)
            wd = 9 * len(txt) + 16
            cx = min(1040 - wd / 2, max(40 + wd / 2, x))
            p.poly([(cx - wd / 2, 1474), (cx + wd / 2, 1474), (cx + wd / 2, 1504), (cx - wd / 2, 1504)], (14, 14, 18),
                   (220, 220, 220), 2)
            _text(img, cam, cx, 1489, txt, 16, (250, 250, 250))
            _text(img, cam, x, 1404, '...', 22, (250, 250, 250))
        _text(img, cam, x, 1432, unit, 10, (210, 210, 210))
    v = View(yaw=0, elev=0, flip=pitch)                         # the little side-on car icon turns with the car
    car(img, cam, 270, 1400, 0.16, v)
    car(img, cam, 712, 1400, 0.16, View(yaw=90, elev=89))       # the top-down icon


def _num(v):
    if abs(v) < 100:
        return f'{v:.1f}'
    return f'{v:,.0f}'


def mars(img, cam, t=0.0):
    """The Martian's set, upright: layered sandstone cliffs high up, hazy orange-brown sky, the Hab (white panels,
    round airlock, the flag), solar boards, NASA crates and numbered flags, rocks in front. Damon stands by the boards."""
    p = B.Pen(img, cam)
    p.poly([(-200, -200), (1280, -200), (1280, 1100), (-200, 1100)], (214, 164, 118), None)
    p.poly([(-200, -200), (1280, -200), (1280, 260), (-200, 260)], (196, 146, 104), None)
    # cliffs: three layers, each lumpy, with strata lines and a flat shadow side
    def cliff(xs, top, base, colr, sd):
        r = np.random.default_rng(sd)
        pts = [(xs[0], base)]
        for x in np.linspace(xs[0], xs[1], 16):
            pts.append((x + r.uniform(-14, 14), top + r.uniform(-90, 90) + 120 * math.sin((x - xs[0]) / 180)))
        pts.append((xs[1], base))
        p.poly(pts, colr, INK, 3)
        for k in range(6):                                     # strata
            y = top + 120 + k * (base - top - 120) / 6
            x0 = xs[0] + r.uniform(0, 120)
            p.line([(x0, y), (x0 + r.uniform(160, 380), y + r.uniform(-8, 8))], dk(colr, 0.82), 2.4)
        for k in range(3):                                     # shadowed clefts
            x = r.uniform(xs[0] + 60, xs[1] - 60)
            p.poly([(x, top + 100), (x + 30, top + 140), (x + 20, base - 20), (x - 14, base - 20)], dk(colr, 0.74), None)
    cliff((-200, 560), 260, 1020, (198, 128, 84), 70)
    cliff((480, 1280), 420, 1030, (178, 108, 70), 71)
    cliff((-200, 1280), 820, 1060, (206, 140, 92), 72)
    # ground
    p.poly([(-200, 1040), (1280, 1040), (1280, 2200), (-200, 2200)], (204, 120, 74), None)
    p.line([(-200, 1040), (1280, 1040)], INK, 3)
    r = np.random.default_rng(73)
    for _ in range(26):
        x, y = r.uniform(-60, 1140), r.uniform(1080, 1900)
        p.poly(rough([(x - 60, y), (x + 70, y - 6), (x + 50, y + 14), (x - 50, y + 16)], 6, int(abs(x))), (190, 108, 66), None)
    # the Hab, behind on the right
    hx0, hy0 = 560, 1060
    p.poly(rough([(hx0, hy0 - 150), (hx0 + 470, hy0 - 160), (hx0 + 480, hy0), (hx0, hy0)], 3, 74), (236, 232, 222), INK, 3)
    p.poly(rough([(hx0 + 10, hy0 - 150), (hx0 + 240, hy0 - 196), (hx0 + 470, hy0 - 160)], 3, 75), (214, 210, 200), INK, 3)
    for i in range(1, 9):
        x = hx0 + i * 54
        p.line([(x, hy0 - 156 + 2 * i), (x, hy0 - 4)], (170, 168, 160), 2)
    _flag(p, hx0 + 340, hy0 - 90, 0.8)
    p.poly(rough([(hx0 - 66, hy0 - 128), (hx0 + 6, hy0 - 132), (hx0 + 6, hy0 - 6), (hx0 - 66, hy0 - 10)], 2, 76),
           (228, 224, 214), INK, 3)                                                       # the airlock's drum, joined on
    for x in (hx0 - 44, hx0 - 22):
        p.line([(x, hy0 - 128), (x, hy0 - 10)], (176, 172, 164), 2)
    p.poly([(hx0 - 66 + 38 * math.cos(a), hy0 - 69 + 60 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 30)],
           (240, 238, 230), INK, 3)                                                       # its round end, with the door
    p.poly(rough([(hx0 - 84, hy0 - 104), (hx0 - 50, hy0 - 104), (hx0 - 50, hy0 - 32), (hx0 - 84, hy0 - 32)], 1.5, 77),
           (212, 208, 198), INK, 2)
    _text(img, cam, hx0 - 66, hy0 - 116, 'CAUTION', 7, (200, 60, 40))
    # solar boards on the left, crates and numbered flags in front
    for i in range(3):
        x = 10 + i * 140
        p.poly(rough([(x, 940), (x + 130, 936), (x + 132, 1040), (x + 2, 1044)], 3, 77 + i), (220, 222, 226), INK, 3)
        for gx in range(4):
            for gy in range(4):
                if (gx + gy) % 2 == 0:
                    p.poly([(x + 8 + gx * 30, 948 + gy * 23), (x + 34 + gx * 30, 948 + gy * 23),
                            (x + 34 + gx * 30, 966 + gy * 23), (x + 8 + gx * 30, 966 + gy * 23)], (120, 130, 150), None)
        p.line([(x + 66, 1044), (x + 66, 1070)], INK, 4)
    for i, (x, y) in enumerate([(120, 1230), (230, 1250), (840, 1180)]):
        p.poly(rough([(x - 60, y - 60), (x + 60, y - 60), (x + 62, y + 20), (x - 62, y + 20)], 3, 80 + i), (232, 230, 224),
               INK, 3)
        p.poly(rough([(x - 62, y - 70), (x + 62, y - 70), (x + 60, y - 52), (x - 60, y - 52)], 2, 83 + i), (210, 208, 200),
               INK, 2.4)
        _text(img, cam, x, y - 20, 'NASA', 12, (190, 50, 40))
    for i, (x, y, n) in enumerate([(700, 1320, '37'), (940, 1400, '38'), (1010, 1210, '39'), (380, 1440, '36')]):
        p.line([(x, y), (x + 4, y - 150)], INK, 4)
        p.poly(rough([(x + 4, y - 150), (x + 64, y - 140), (x + 60, y - 100), (x + 4, y - 108)], 2, 90 + i),
               (240, 240, 236), INK, 2.4)
        _text(img, cam, x + 32, y - 124, n, 14, INK)
    for i, (x, y, w) in enumerate([(160, 1700, 180), (820, 1760, 220), (520, 1880, 160)]):
        p.poly(rough([(x - w, y + 40), (x - w * 0.6, y - w * 0.5), (x + w * 0.4, y - w * 0.6), (x + w, y + 40)], 10, 95 + i),
               (170, 98, 60), INK, 3)
        p.poly([(x + w * 0.1, y - w * 0.55), (x + w * 0.4, y - w * 0.6), (x + w, y + 40), (x + w * 0.2, y + 40)],
               (146, 82, 50), None)


MARS_NECK, MARS_S = 960, 0.85        # Damon in the Mars shot: big enough to read his eyes, the set behind him


# ============================================== SPACE (Dam's pencil) ================================================
def space_stars(t, car_view=None, comet=True):
    """Shot 6: deep blue-black with soft blue-violet nebula wisps, a faint Milky Way band, dense small stars, a few
    four-point ones, the green comet far off. Returns the drawing as an RGBA image (car added on top)."""
    import pencil_cartoon as PC
    c = PC.Canvas(int(t * PC.FPS))
    c.fill_screen(PC.col(0.03, 0.04, 0.09), 1.3)
    r = np.random.default_rng(12)
    for i in range(7):                                         # nebula wisps
        x, y = r.uniform(0, 1080), r.uniform(0, 1920)
        c.glow(x, y, r.uniform(260, 520), PC.col(0.22, 0.24, 0.62) if i % 2 else PC.col(0.42, 0.24, 0.58), 0.45)
    for i in range(14):                                        # the Milky Way, a soft diagonal haze
        u = i / 13
        x, y = 160 + 800 * u + r.normal(0, 40), 1950 - 2000 * u + r.normal(0, 40)
        c.glow(x, y, r.uniform(140, 220), PC.col(0.40, 0.42, 0.60), 0.35)
    PC.stars(c, 340, seed=21, dim=0.85)
    if comet:
        hx, hy = 830, 520
        for k in range(12):                                    # the tail: soft glows fading out behind
            f = k / 11
            c.glow(hx + 300 * f, hy - 380 * f, 30 + 50 * f, PC.col(0.55, 0.85, 0.85), 0.5 * (1 - f) + 0.1)
        c.glow(hx, hy, 70, PC.col(0.35, 0.95, 0.75), 0.9)
        c.glow(hx, hy, 18, PC.WHITE, 1.0)
    res = c.result()
    m = PC.M if res.shape[0] > 1920 else 0
    return Image.fromarray(res[m:m + 1920, m:m + 1080])


def space_mars(t, grow=0.0):
    """Shot 7: Mars, small and lit from one side, swelling towards us (grow 0..1) until it fills the upright frame
    half off the edge: craters, the dark Valles Marineris scar, a white polar cap."""
    import pencil_cartoon as PC
    c = PC.Canvas(int(t * PC.FPS))
    c.fill_screen(PC.col(0.02, 0.02, 0.05), 1.3)
    PC.stars(c, 160, seed=31, dim=0.8)
    R = 90 + 1000 * grow ** 1.6
    cx, cy = 700 + 260 * grow, 760 + 300 * grow
    c.poly(PC.ell(cx, cy, R, R, 0, 120), fill=PC.col(0.78, 0.38, 0.20), pressure=1.2, jit=1.0)
    r = np.random.default_rng(32)
    for i in range(14):                                       # darker regions
        a, rho = r.uniform(0, 6.28), r.uniform(0.1, 0.8)
        c.poly(PC.blob(cx + R * rho * math.cos(a), cy + R * rho * math.sin(a), R * r.uniform(0.08, 0.2), 40 + i, 30, 0.35),
               fill=PC.col(0.52, 0.22, 0.12), pressure=0.9, opacity=0.7, jit=1)
    c.line([(cx - R * 0.7, cy + R * 0.05), (cx - R * 0.2, cy + R * 0.12), (cx + R * 0.4, cy + R * 0.02)],
           PC.col(0.34, 0.14, 0.10), lw=max(4, R * 0.06), pressure=0.9, opacity=0.8)       # Valles Marineris
    for i in range(18):                                       # craters
        a, rho = r.uniform(0, 6.28), r.uniform(0.0, 0.85)
        x, y = cx + R * rho * math.cos(a), cy + R * rho * math.sin(a)
        rr = R * r.uniform(0.02, 0.06)
        c.poly(PC.ell(x, y, rr, rr, 0, 16), None, PC.col(0.50, 0.22, 0.12), lw=max(1.5, rr * 0.25), opacity=0.7)
    c.poly(PC.ell(cx - R * 0.1, cy - R * 0.9, R * 0.3, R * 0.09, 0, 30), fill=PC.col(0.96, 0.94, 0.92), pressure=1.0,
           opacity=0.9)
    c.poly(PC.ell(cx + R * 0.42, cy + R * 0.1, R * 0.88, R * 1.02, 0, 80), fill=PC.col(0.05, 0.03, 0.04), pressure=1.0,
           opacity=0.55)                                       # the night side, lit from the left
    res = c.result()
    m = PC.M if res.shape[0] > 1920 else 0
    return Image.fromarray(res[m:m + 1920, m:m + 1080])


# ============================================== THE FILM: TIMELINE ==================================================
FPS = 12
SHOTS = [   # (name, start, end): hard cuts
    ('hangar', 0.0, 10.6),    # 1: the original demo, shot for shot to 6 s; then it keeps flipping and goes up
    ('roof', 10.6, 12.0),     # 2: out through the hangar roof (outside, night)
    ('clouds', 12.0, 13.6),   # 3: up through ordinary clouds (pencil)
    ('sea', 13.6, 15.4),      # 4: wide, bursting through the high cloud layer (pencil)
    ('earth', 15.4, 17.6),    # 5: the Earth from space, silent (pencil)
    ('stars', 17.6, 19.6),    # 6: flipping through the stars, the comet far off (pencil)
    ('towards', 19.6, 21.8),  # 7: flipping towards Mars as it swells (pencil)
    ('mars', 21.8, 29.0),     # 8: Damon hopeful, eyes 2 -> 5, the car drops upside down, crushes him; the line
]
DUR = 29.0
T_LAND1 = 6.0          # lands in the smoke (as the original)
T_UP = 9.6             # the jets go full and it shoots up
T_SEEN = 22.9          # a speck in the Mars sky
T_IMPACT = 24.2
T_LINE = 25.0          # roadster-1.m4a starts here (its speech starts 1.02 s in: "Fatality avoided" at ~26.0)
T_LAMP = 26.0
MARS_DIST_FT = 738188976378
FLIP_PERIOD = {'hangar': 1.4, 'roof': 1.1, 'clouds': 0.9, 'sea': 0.75, 'earth': 0.6, 'stars': 0.45, 'towards': 0.3}


def shot_of(t):
    return next((s for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1])


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def flip_angle(t):
    """The car's own nose-over-tail angle (degrees, negative = nose up and over backwards), faster each scene."""
    if t < 4.0:
        return -_ramp_pitch(_climb_u(t))
    if t < T_LAND1:
        return -80 - 280 * ease((t - 4.0) / (T_LAND1 - 4.0))
    acc, prev = -360.0, T_LAND1
    for name, a, b in SHOTS:
        if b <= T_LAND1 or name == 'mars':
            continue
        a = max(a, T_LAND1)
        span = min(t, b) - a
        if span > 0:
            acc -= 360 * span / FLIP_PERIOD[name]
        if t < b:
            break
    return acc


def _climb_u(t):
    return 0.22 + 0.78 * (t / 4.0) ** 1.6


def _ramp_pitch(u):
    return 80 * u ** 1.5


def altitude(t):
    """The ALTITUDE dial (ft): the original's climb to 67.8, back to 0 at the landing, the hops, then the journey to
    Mars (the Earth-Mars distance in feet on arrival)."""
    if t < 4.5:
        return 7.4 + 60.4 * (t / 4.5) ** 1.3
    if t < T_LAND1:
        return 67.8 * (1 - ease((t - 4.5) / 1.5))
    if t < T_UP:
        ph = (t - T_LAND1) % 1.2
        return 38 * math.sin(math.pi * ph / 1.2)
    if t < 21.8:
        k = (t - T_UP) / (21.8 - T_UP)
        return 20 * (MARS_DIST_FT / 20) ** k                        # roughly exponential: feet, miles, millions...
    return float(MARS_DIST_FT)


def gforce(t):
    if t < T_LAND1:
        return [1.4, 1.1, 0.9, 0.9, 0.9, 0.9, 0.8, 1.1, 1.1, 0.2, 0.4, 0.3][min(11, int(t * 2))]
    if t < T_UP:
        return 3.3 + 1.5 * math.sin(t * 5)
    if t < 21.8:
        return 1274210.0 * ease((t - T_UP) / 1.2)
    return 1274210.0


# ---------------------------------------------------------------------------- shot 1: the hangar
HANGAR_SPINE = None


def hangar_car(t):
    """Where the car is in shot 1: (x, y, scale, View, jets)."""
    global HANGAR_SPINE
    if HANGAR_SPINE is None:
        HANGAR_SPINE = hangar(B.canvas((0, 0, 0)), B.Cam(1.0, 540, 960))
    sp = HANGAR_SPINE
    if t < 4.0:                                                     # climbing the ramp, seen from behind
        u = _climb_u(t)
        x, y = sp(u)
        k = (120 - 55 * u) / 120
        return x, y - 40 * k, 0.75 * k, View(yaw=-90, elev=10, flip=flip_angle(t)), 0.0
    tx, ty = sp(1.0)
    if t < T_LAND1:                                                 # off the top, over backwards, down into the smoke
        f = (t - 4.0) / (T_LAND1 - 4.0)
        x = tx + (360 - tx) * f
        y = ty - 180 * math.sin(math.pi * min(1, f * 1.2)) + (1240 - ty) * f ** 2.2
        return x, y, 0.55 + 0.2 * f, View(yaw=-120, elev=12, flip=flip_angle(t)), 0.0
    if t < T_UP:                                                    # hops on its jets, flipping, each one higher
        ph = (t - T_LAND1) / 1.2
        h = [260, 420, 600][min(2, int(ph))]
        y = 1240 - h * math.sin(math.pi * (ph % 1))
        return 380 + 30 * math.sin(t), y, 0.75, View(yaw=-120, elev=12, flip=flip_angle(t)), 1.0
    f = (t - T_UP) / (10.6 - T_UP)                                  # full jets: straight up, out of the top
    return 380, 1240 - 1500 * f ** 1.6, 0.75, View(yaw=-120, elev=12, flip=flip_angle(t)), 1.0


def picture_hangar(t):
    cam = B.Cam(1.0 + 0.04 * ease(t / 10.0), 540, 960)              # the original's slight push-in
    img = B.canvas((0, 0, 0))
    hangar(img, cam, t)
    x, y, s, v, jets = hangar_car(t)
    if t >= T_LAND1 - 0.05:                                         # the smoke from the landing and the jets
        grow = ease((t - T_LAND1 + 0.05) / 1.0)
        smoke_cloud(img, cam, 400, 1300, 420 * grow + 120, 150 * grow + 40, 5)
    car(img, cam, x, y, s, v, jets=jets, t=t)
    if t >= T_LAND1 - 0.05:
        smoke_cloud(img, cam, 520, 1340, 360 * ease((t - T_LAND1) / 1.4) + 60, 90, 6)
    dials(img, B.Cam(1.0, 540, 960), gforce(t), altitude(t), flip_angle(t))
    return img


# ---------------------------------------------------------------------------- shot 2: out through the roof
def picture_roof(t):
    u = t - 10.6
    cam = B.Cam(1.0, 540, 960)
    img = B.canvas((22, 28, 56))
    p = B.Pen(img, cam)
    r = np.random.default_rng(3)
    for _ in range(60):
        p.ell(r.uniform(0, 1080), r.uniform(0, 1100), 2.2, 2.2, (230, 230, 210), None)
    # the hangar roof from just above its edge: corrugated, skylights, vents
    roof = [(-100, 1150), (1180, 1080), (1180, 2100), (-100, 2100)]
    p.poly(roof, (70, 74, 84), INK, 4)
    for i in range(30):
        x = -100 + i * 46
        p.line([(x, 1150 - i * 2.4), (x - 120, 2100)], (56, 60, 70), 2)
    for i in range(3):
        y = 1350 + i * 200
        p.poly(rough([(80, y), (300, y - 8), (310, y + 60), (84, y + 66)], 3, 10 + i), (40, 46, 62), INK, 3)
        p.poly(rough([(760, y - 20), (980, y - 28), (990, y + 40), (764, y + 46)], 3, 20 + i), (40, 46, 62), INK, 3)
    p.poly(rough([(900, 1180), (980, 1176), (980, 1100), (900, 1104)], 2, 30), (110, 114, 124), INK, 3)   # a vent
    # the hole it tore, the panels thrown up (each its own size and speed, under gravity)
    hole = [(540 + 130 * math.cos(a) * (1 + 0.25 * math.sin(a * 5)), 1500 + 50 * math.sin(a) * (1 + 0.3 * math.cos(a * 7)))
            for a in np.linspace(0, 2 * math.pi, 24, endpoint=False)]
    p.poly(hole, (16, 14, 18), INK, 4)
    p.poly([(540 + 90 * math.cos(a), 1500 + 30 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 20)],
           (250, 210, 140), None)                                                         # light from inside
    for i in range(9):
        vx, vy = r.uniform(-260, 260), r.uniform(-1500, -800)
        x = 540 + vx * u
        y = 1500 + vy * u + 900 * u * u
        a, w = r.uniform(0, 6) + u * r.uniform(-6, 6), r.uniform(26, 60)
        pts = [(x + w * math.cos(a + q), y + 0.5 * w * math.sin(a + q)) for q in (0, 1.9, 3.3, 4.8)]
        p.poly(pts, (88, 92, 102), INK, 2.4)
    y = 1500 - 1700 * (u / 1.4) ** 1.2
    car(img, cam, 540, y, 0.9, View(yaw=-60, elev=12, flip=flip_angle(t)), jets=1.0, t=t)
    dials(img, cam, gforce(t), altitude(t), flip_angle(t))
    return img


# ---------------------------------------------------------------------------- shots 3-7: Dam's pencil
def _pencil(t):
    import pencil_cartoon as PC
    return PC, PC.Canvas(int(round(t * PC.FPS)))


def _paste(c, layer):
    """Lay a flat Satire-style layer (RGBA) into a pencil canvas."""
    a = np.asarray(layer, np.float32) / 255.0
    al = a[..., 3:4]
    c.img = c.img * (1 - al) + a[..., :3] * al


def _car_layer(x, y, s, view, jets, t):
    lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    car(lay, B.Cam(1.0, 540, 960), x, y, s, view, jets=jets, t=t)
    return lay


def _finish_pencil(c, t):
    lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    dials(lay, B.Cam(1.0, 540, 960), gforce(t), altitude(t), flip_angle(t))
    _paste(c, lay)
    return Image.fromarray(c.result()).convert('RGBA')


def picture_clouds(t):
    import beaver_asteroid as DAM
    PC, c = _pencil(t)
    u = t - 12.0
    c.fill_screen(PC.col(0.40, 0.60, 0.88), 1.4)
    c.vgrad(PC.col(0.74, 0.85, 0.97), 0.0, 0.85, 0, 1920)
    for (x, y0, r, seed) in DAM.CUMULUS:
        DAM.cumulus(c, x, y0 + 1400 * u, r, seed)
    _paste(c, _car_layer(540, 1500 - 437 * u, 0.7, View(yaw=-40, elev=8, flip=flip_angle(t)), 1.0, t))
    bx, by, br, bseed = DAM.BIG_CLOUD
    DAM.cumulus(c, bx, -600 + 1400 * u, br, bseed)                  # the cloud it punches up through, in front
    return _finish_pencil(c, t)


def picture_sea(t):
    import beaver_asteroid as DAM
    PC, c = _pencil(t)
    u = t - 13.6
    c.fill_screen(PC.col(0.12, 0.17, 0.33), 1.5)
    c.vgrad(PC.col(0.36, 0.45, 0.62), 0.0, 0.9, 150, DAM.HORIZON - 250)
    c.vgrad(PC.col(0.99, 0.80, 0.56), 0.0, 0.95, DAM.HORIZON - 380, DAM.HORIZON + 10)
    for x, y, ln in DAM.WISPS:
        c.line([(x, y), (x + ln, y + 2)], PC.col(0.80, 0.68, 0.70), lw=5, pressure=0.8, opacity=0.5)
    c.glow(DAM.SUN[0], DAM.SUN[1], 700, PC.col(1.0, 0.82, 0.5), 0.7, power=1.6)
    c.glow(DAM.SUN[0], DAM.SUN[1], 170, PC.WHITE, 1.0, power=1.3)
    ry = DAM.HORIZON + 120 - 900 * min(1.0, u / 1.8) ** 0.85
    for (x, y, rad, seed) in DAM.CLOUD_SEA:
        DAM.cloud_puff(c, x, y, rad, seed)
    if u > 0.15:                                                    # its white jet trail out of the cloud sea
        ys = np.linspace(DAM.HORIZON + 60, ry + 20, 30)
        wd = 5 + 0.03 * (ys - ry)
        xc = 430 + 6 * np.sin(ys * 0.03)
        c.poly(np.concatenate([np.stack([xc - wd, ys], 1), np.stack([xc + wd, ys], 1)[::-1]]),
               fill=PC.col(0.97, 0.97, 0.99), pressure=1.0, jit=1.5)
        _paste(c, _car_layer(430, ry, 0.13, View(yaw=-30, elev=10, flip=flip_angle(t)), 1.0, t))
    return _finish_pencil(c, t)


def picture_earth(t):
    import beaver_asteroid as DAM
    PC, c = _pencil(t)
    u = t - 15.4
    c.fill_screen(DAM.DEEP, 1.3)
    PC.stars(c, 160, seed=5, dim=0.8)
    DAM.earth_limb(c)
    DAM.sunrise(c, t)
    _paste(c, _car_layer(560, 1000 - 420 * u / 2.2, 0.16, View(yaw=-30, elev=12, flip=flip_angle(t)), 1.0, t))
    return _finish_pencil(c, t)


def picture_stars(t):
    u = t - 17.6
    bg = space_stars(t)
    PC, c = _pencil(t)
    c.img = np.asarray(bg.convert('RGB'), np.float32) / 255.0
    _paste(c, _car_layer(260 + 520 * u / 2.0, 1500 - 900 * u / 2.0, 0.6, View(yaw=-20, elev=18, flip=flip_angle(t)), 1.0, t))
    return _finish_pencil(c, t)


def picture_towards(t):
    u = (t - 19.6) / 2.2
    bg = space_mars(t, 0.08 + 0.92 * u)
    PC, c = _pencil(t)
    c.img = np.asarray(bg.convert('RGB'), np.float32) / 255.0
    _paste(c, _car_layer(380 + 200 * u, 1450 - 500 * u, 0.7 * (1 - 0.75 * u), View(yaw=-150, elev=20, flip=flip_angle(t)),
                         1.0, t))
    return _finish_pencil(c, t)


# ---------------------------------------------------------------------------- shot 8: Mars
def damon_eyes(t):
    """Strength 2 (hopeful) while he waits; widening to 5 as the car falls into view (eyes snap, feelings ease)."""
    return 2 + 3 * ease((t - T_SEEN) / (T_IMPACT - 0.25 - T_SEEN))


def picture_mars(t):
    shake = 0.0
    if T_IMPACT <= t < T_IMPACT + 0.45:
        k = 1 - (t - T_IMPACT) / 0.45
        shake = 26 * k * math.sin((t - T_IMPACT) * 90)
    cam = B.Cam(1.0, 540 + shake, 960 + shake * 0.6)
    img = B.canvas((0, 0, 0))
    mars(img, cam, t)
    ground = MARS_NECK + 928 * MARS_S - 40
    if t < T_IMPACT:
        damon(img, cam, 540, MARS_NECK, MARS_S, dict(look_up=1.0, wide=damon_eyes(t), visor_car=max(0, (t - T_SEEN) / 1.3)))
        if t >= T_SEEN:                                             # dropping: no jets, upside down, still turning
            f = (t - T_SEEN) / (T_IMPACT - T_SEEN)
            y = -150 + (ground - 120 + 150) * f ** 2
            s = 0.1 + 0.9 * f ** 2
            car(img, cam, 540, y, s, View(yaw=-30, elev=10, flip=180 + 140 * (1 - f)), jets=0.0, t=t)
    else:
        debris(img, cam, 540, ground + 20, 1.3)
        car(img, cam, 540, ground - 40, 1.3, View(yaw=-30, elev=10, flip=180), crush=1.0, headlight=t >= T_LAMP and
            not (T_LAMP + 0.12 < t < T_LAMP + 0.24))                # the lamp flickers on with the line
        d = t - T_IMPACT
        if d < 1.4:                                                 # the dust burst: thrown out, then settling
            g = 0.55 + 0.45 * ease(d / 0.3)
            fade = 1 - ease((d - 0.45) / 0.95)
            if fade > 0.02:
                smoke_cloud(img, cam, 540, ground - 60 * fade, 1100 * g, 520 * fade + 40, 8, fill=(222, 156, 112),
                            shade=(190, 120, 82))
    if t < T_IMPACT:
        dials(img, B.Cam(1.0, 540, 960), gforce(t), altitude(t), flip_angle(min(t, 21.79)))
    return img


PICTURES = {'hangar': picture_hangar, 'roof': picture_roof, 'clouds': picture_clouds, 'sea': picture_sea,
            'earth': picture_earth, 'stars': picture_stars, 'towards': picture_towards, 'mars': picture_mars}


def picture(t):
    """The frame WITHOUT captions (they go on last, so wording notes never re-render a picture)."""
    return PICTURES[shot_of(t)[0]](t)


def caption_at(t):
    return 'Fatality avoided.' if T_LAMP - 0.1 <= t < T_LAMP + 2.2 else None


def overlay(img, t):
    c = caption_at(t)
    if c:
        import peepee as PP
        PP.caption(img, c)
    return img


def frame_image(t):
    return overlay(picture(t), t)


STILLS = [(2.0, '1 climbing the ramp'), (4.9, '1 off the top'), (8.0, '1 hopping, flipping'), (10.2, '1 jets full'),
          (11.2, '2 out through the roof'), (12.8, '3 up through clouds'), (14.6, '4 through the cloud sea'),
          (16.6, '5 the Earth'), (18.6, '6 the stars'), (21.0, '7 towards Mars'), (23.6, '8 Damon, the car falls'),
          (24.3, '8 the crash'), (26.6, '8 "Fatality avoided"')]


def stills_sheet(out):
    B.SS = 1
    cols, w, h = 5, 400, 711
    rows = (len(STILLS) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w + (cols + 1) * 10, rows * (h + 50) + 10), (232, 228, 222))
    for i, (t, lab) in enumerate(STILLS):
        im = frame_image(t).convert('RGB').resize((w, h))
        x, y = 10 + (i % cols) * (w + 10), 10 + (i // cols) * (h + 50)
        sheet.paste(im, (x, y + 40))
        _label(sheet, x, y + 6, f'{t:.1f}s  {lab}', 22)
    sheet.save(out, quality=86)


# ============================================== SHEETS ==============================================================
def _panel(w, h, bg=(232, 228, 222)):
    return Image.new('RGBA', (w, h), bg + (255,))


def _label(img, x, y, s, size=26, fill=(30, 30, 30)):
    ImageDraw.Draw(img).text((x, y), s, font=ImageFont.truetype(SANS, size), fill=fill)


def cast_sheet(out):
    B.SS = 1
    W, H = 2160, 2720
    sheet = _panel(W, H)
    cell = lambda: Image.new('RGBA', (1080, 1920), (226, 222, 216, 255))

    def place(lay, x, y, w, h, label):
        im = lay.crop((540 - w, 960 - h, 540 + w, 960 + h)).resize((w, h))
        sheet.alpha_composite(im, (x, y))
        _label(sheet, x + 10, y + 8, label)

    cam = B.Cam(1.0, 540, 960)
    views = [('side', View(yaw=0, elev=6)), ('front', View(yaw=90, elev=6)), ('back', View(yaw=-90, elev=6)),
             ('from above', View(yaw=0, elev=88)), ('three-quarter front', View(yaw=40, elev=14)),
             ('three-quarter back', View(yaw=-140, elev=14))]
    for i, (lab, v) in enumerate(views):
        lay = cell()
        car(lay, cam, 540, 960, 1.6, v)
        place(lay, 20 + (i % 3) * 710, 60 + (i // 3) * 420, 700, 400, lab)
    _label(sheet, 20, 12, 'THE ROADSTER: every angle', 34)
    # the flip, eight steps, jets firing
    _label(sheet, 20, 905, 'The flip, nose over tail, jets firing (each scene faster)', 34)
    for i in range(8):
        lay = cell()
        car(lay, cam, 540, 900, 1.0, View(yaw=8, elev=10, flip=-i * 45), jets=1.0, t=i / 12)
        place(lay, 20 + i * 265, 960, 260, 380, f'{i * 45} deg')
    # upside down with jets; the landing: dropped upside down, no jets, crushed flat; its lamp lit
    _label(sheet, 20, 1360, 'Upside down, jets / it lands upside down, no jets, crushed flat / lamp lit on the line', 34)
    lay = cell()
    car(lay, cam, 540, 900, 1.4, View(yaw=30, elev=12, flip=180), jets=1.0)
    place(lay, 20, 1410, 700, 420, 'upside down, jets')
    for i, lit in enumerate((False, True)):
        lay = cell()
        debris(lay, cam, 540, 1010, 1.6)
        car(lay, cam, 540, 960, 1.6, View(yaw=-30, elev=10, flip=180), crush=1.0, headlight=lit)
        place(lay, 730 + i * 710, 1410, 700, 420, 'lamp lit' if lit else 'crashed, upside down')
    # Damon in the Mars shot (no close-up): framed big enough to read his eyes; they widen from 2 to 5
    _label(sheet, 20, 1860, 'MATT DAMON in the Mars shot (no close-up): his eyes widen from 2 to 5 as the car falls', 34)
    for i, w in enumerate((2, 3, 4, 5)):
        lay = B.canvas((0, 0, 0))
        mars(lay, cam)
        damon(lay, cam, 540, MARS_NECK, MARS_S, dict(look_up=1.0, wide=w, visor_car=(w - 2) / 3))
        sheet.alpha_composite(lay.crop((140, 520, 940, 1700)).resize((520, 767)), (20 + i * 535, 1910))
        _label(sheet, 30 + i * 535, 1918, str(w), 34, (250, 250, 250))
    sheet.convert('RGB').save(out, quality=88)


def sets_sheet(out):
    B.SS = 1
    W, H = 2160, 1060
    sheet = _panel(W, H)
    small = (520, 924)
    cam = B.Cam(1.0, 540, 960)
    lay = B.canvas((0, 0, 0))
    spine = hangar(lay, cam)
    sx, sy = spine(0.0)
    car(lay, cam, sx, sy - 70, 1.0, View(yaw=-90, elev=10))
    dials(lay, cam, 1.0, 0.0)
    panels = [('Hangar, ramp, dials', lay)]
    lay = B.canvas((0, 0, 0))
    mars(lay, cam)
    damon(lay, cam, 540, MARS_NECK, MARS_S, dict(look_up=0.9, wide=2))
    panels.append(('The Martian set', lay))
    st = space_stars(20.0).convert('RGBA')
    car(st, cam, 420, 1100, 1.0, View(yaw=20, elev=20, flip=-60), jets=1.0)
    panels.append(('Stars (pencil)', st))
    ms = space_mars(22.0, 0.35).convert('RGBA')
    car(ms, cam, 380, 1300, 0.8, View(yaw=-30, elev=25, flip=-120), jets=1.0)
    panels.append(('Towards Mars (pencil)', ms))
    for i, (lab, im) in enumerate(panels):
        sheet.alpha_composite(im.resize(small), (20 + i * 535, 90))
        _label(sheet, 24 + i * 535, 40, lab, 30)
    sheet.convert('RGB').save(out, quality=88)


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        cast_sheet(a[1])
    elif a[0] == 'sets':
        sets_sheet(a[1])
    elif a[0] == 'stills':
        stills_sheet(a[1])


if __name__ == '__main__':
    main()
