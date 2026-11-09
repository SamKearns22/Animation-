#!/usr/bin/env python3
"""elder_swindon_extras (kept from a duplicate build, 8 Nov; port the people and vehicles onto elder_swindon.py): the Magic Roundabout, Swindon, from above in flat house style, drawn through the film's camera
(so the zoom-out and the held shot use one set; rule 1). Benchmark: Sam's two photos (notes, 'The world').

MAP
- 30: layout in metres (screen-metres: sx right, sy down; island centre at 0, 0), the world link `W`
- 70: the view: `View` (a sets.Cam straight down) -> px, pixels per metre, how much to enlarge people
- 95: ground: verges, paths, tarmac, pavements, islands, markings, minis, central island, lamp post
- 215: surroundings: houses (left, bottom), flat-roofed block (right), car park, trees, the stadium's corner (top left)
- 270: routes: cars round the minis (clockwise) and the inner ring (anticlockwise); a bus, the delivery moped
- 340: e-bikes (two hooded teens, wrong way, weaving), walkers, the fight (two groups), the burnt-out car
- 470: draw(pil, cam, t) and the still: python3 source/elder_swindon_aerial.py still OUT.jpg T [WIDTH]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B                    # noqa: E402
import sets as S                       # noqa: E402
from ed import INK                     # noqa: E402

SS = B.SS
# ------------------------------------------------------------------------------------------------ layout (metres)
# The island centre sits at world (X0, Z0); the man lies on the soil patch at world (0, 0). Through a straight-down
# camera (topcam) screen right is world -x and screen down is world +z, so screen-metres (sx, sy) = (X0 - x, z - Z0).
X0, Z0 = 5.2, 1.2                       # the lamp post 5 m from his head: out of shot 4, its shadow crosses it
R_ISLAND, R_RING, R_MINI, R_EDGE = 10.5, 15.5, 36.0, 47.0
MINIS = [211, 282, 339, 45, 148]        # bearings of the five minis and their roads (screen degrees, 270 = up)
ARM_W = 13.0                            # carriageway width of each road
WHITE, TARMAC, PAVE, VERGE = (244, 244, 240), (176, 176, 172), (206, 204, 198), (112, 158, 80)
DARK_PAVE = (104, 100, 96)
SHADOW = (0, 0, 0, 70)
SUN = (0.55, -0.55)                     # shadows fall up-right (the lamp post's long shadow in Sam's photos)


def W(sx, sy, y=0.0):
    return (X0 - sx, y, Z0 + sy)


def pol(r, ang):
    a = math.radians(ang)
    return (r * math.cos(a), r * math.sin(a))


def udir(ang):
    a = math.radians(ang)
    return (math.cos(a), math.sin(a))


def angdist(a, b):
    return abs((a - b + 180) % 360 - 180)


# ------------------------------------------------------------------------------------------------ the view
class View:
    def __init__(self, pil, cam):
        self.pil, self.cam = pil, cam
        self.d = ImageDraw.Draw(pil, 'RGBA')
        (ax, ay), k = cam.project(W(0, 0))
        self.k = k * SS                                  # pixels per metre on the canvas (at ground level)
        self.enl = float(np.clip(1080 / k / 30.0, 1.0, 4.0))   # people and bikes enlarged when far (Q11)
        self.lw = max(1, int(2.2 * SS))

    def P(self, sx, sy, y=0.0):
        (x, yy), _ = self.cam.project(W(sx, sy, y))
        return (x * SS, yy * SS)

    def poly(self, pts, fill, outline=INK, lw=None, y=0.0):
        P = [self.P(x, z, y) for x, z in pts]
        self.d.polygon(P, fill=fill)
        if outline is not None:
            self.d.line(P + [P[0]], fill=outline, width=lw or self.lw, joint='curve')

    def circle(self, cx, cy, r, fill, outline=INK, lw=None, n=None, y=0.0):
        n = n or int(np.clip(r * self.k / 3, 10, 90))
        pts = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]
        self.poly(pts, fill, outline, lw, y)

    def line(self, pts, fill, w_m=None, w_px=None, y=0.0):
        P = [self.P(x, z, y) for x, z in pts]
        w = int(max(1, w_px * SS if w_px else w_m * self.k))
        self.d.line(P, fill=fill, width=w, joint='curve')

    def visible(self, sx, sy, r):
        x, y = self.P(sx, sy)
        rr = r * self.k
        w, h = self.pil.size
        return -rr < x < w + rr and -rr < y < h + rr


def rrect(cx, cy, L, Wd, ang, rad=None, n=6):
    """A rounded rectangle (length L along ang, width Wd) as points."""
    rad = min(rad if rad is not None else Wd / 2, Wd / 2, L / 2)
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = []
    for (ux, uy, a0) in ((L / 2 - rad, Wd / 2 - rad, 0), (-(L / 2 - rad), Wd / 2 - rad, 90),
                         (-(L / 2 - rad), -(Wd / 2 - rad), 180), (L / 2 - rad, -(Wd / 2 - rad), 270)):
        for a in np.linspace(a0, a0 + 90, n):
            u, v = ux + rad * math.cos(math.radians(a)), uy + rad * math.sin(math.radians(a))
            pts.append((cx + u * ca - v * sa, cy + u * sa + v * ca))
    return pts


# ------------------------------------------------------------------------------------------------ ground
def ground(v, t):
    w, h = v.pil.size
    v.d.rectangle([0, 0, w, h], fill=VERGE)
    # footpaths across the verges (pale), incl. the top path where the fight is
    for pts in (FIGHT_PATH,
                [pol(58, 175), pol(80, 182), pol(110, 186)]):
        v.line(pts, (196, 190, 176), w_m=2.4)
    # the roads: pavement band, then carriageway with a centre line
    for m in MINIS:
        a, b = pol(R_MINI, m), pol(260, m)
        v.line([a, b], PAVE, w_m=ARM_W + 6)
    v.circle(0, 0, R_EDGE + 3, PAVE, None)
    for m in MINIS:
        a, b = pol(R_MINI, m), pol(260, m)
        v.line([a, b], TARMAC, w_m=ARM_W)
    v.circle(0, 0, R_EDGE, TARMAC, None)
    v.circle(0, 0, R_EDGE + 3, None, INK, n=120) if False else None
    for m in MINIS:                                      # dashed centre lines and the zebra crossing on each road
        ux, uy = udir(m)
        for j in range(14):
            r0 = R_EDGE + 12 + j * 7
            v.line([(ux * r0, uy * r0), (ux * (r0 + 3), uy * (r0 + 3))], WHITE, w_m=0.25)
        nx, ny = -uy, ux
        rz = R_EDGE + 6
        for j in range(-6, 7):
            c = (ux * rz + nx * j * 0.95, uy * rz + ny * j * 0.95)
            v.poly(rrect(c[0], c[1], 3.0, 0.5, m, 0.05, 2), WHITE, None)
        for side in (-1, 1):                             # give-way dashes across the entry
            for j in range(5):
                p = (ux * (R_EDGE - 1.5) + nx * side * (1.2 + j * 1.1), uy * (R_EDGE - 1.5) + ny * side * (1.2 + j * 1.1))
                v.poly(rrect(p[0], p[1], 0.5, 0.7, m, 0.05, 2), WHITE, None)
    # raised kerbed islands between the minis, with hatching round them
    for i in range(5):
        a1, a2 = MINIS[i], MINIS[(i + 1) % 5]
        mid = (a1 + ((a2 - a1) % 360) / 2) % 360
        cx, cy = pol(R_MINI - 3, mid)
        for j in range(-5, 6):                           # hatched area
            p = (cx + udir(mid + 90)[0] * j * 1.6, cy + udir(mid + 90)[1] * j * 1.6)
            v.line([(p[0] - udir(mid + 45)[0] * 2.6, p[1] - udir(mid + 45)[1] * 2.6),
                    (p[0] + udir(mid + 45)[0] * 2.6, p[1] + udir(mid + 45)[1] * 2.6)], WHITE, w_m=0.3)
        v.poly(rrect(cx, cy, 14.0, 4.6, mid + 90, 2.0), WHITE, INK)
        v.poly(rrect(cx, cy, 13.0, 3.6, mid + 90, 1.6), DARK_PAVE, None)
    # the inner ring: dashed outer edge, arrows anticlockwise
    for a in range(0, 360, 10):
        v.line([pol(R_RING + 3, a), pol(R_RING + 3, a + 5)], WHITE, w_m=0.3)
    for a in range(20, 380, 72):                         # arrows pointing anticlockwise
        p, q = pol(R_RING, a), pol(R_RING, a - 6)
        v.line([p, q], WHITE, w_m=0.35)
        tip = q
        for s in (-1, 1):
            back = pol(R_RING + s * 0.9, a - 4.2)
            v.line([back, tip], WHITE, w_m=0.35)
    # the minis: dashed give-way ring, white dome
    for m in MINIS:
        cx, cy = pol(R_MINI, m)
        for a in range(0, 360, 24):
            v.line([(cx + 8.2 * math.cos(math.radians(a)), cy + 8.2 * math.sin(math.radians(a))),
                    (cx + 8.2 * math.cos(math.radians(a + 12)), cy + 8.2 * math.sin(math.radians(a + 12)))],
                   WHITE, w_m=0.35)
        v.circle(cx, cy, 2.2, WHITE, INK)
        v.circle(cx - 0.4, cy - 0.4, 1.1, (252, 252, 250), None)
    # the central island: white kerb, dark paving, the soil-and-grass patch (Q2), the lamp post and its long shadow
    v.circle(0, 0, R_ISLAND + 0.5, WHITE, INK)
    v.circle(0, 0, R_ISLAND, DARK_PAVE, None)
    for r in (3.5, 6.5, 9.0):                            # paving rings
        v.circle(0, 0, r, None, (92, 88, 84), lw=max(1, int(0.12 * v.k)))
    patch_draw(v)
    v.line([(0, 0), (SUN[0] * 32, SUN[1] * 32)], (40, 40, 44, 120), w_m=0.45)   # the lamp post's shadow
    v.line([(SUN[0] * 32 - 1.2, SUN[1] * 32 - 0.2), (SUN[0] * 32 + 0.5, SUN[1] * 32 + 1.4)], (40, 40, 44, 120),
           w_m=0.9)


PATCH = [(5.2 + 3.9 * math.cos(a) * (1 + 0.12 * math.sin(3 * a + 1)), -1.2 + 3.1 * math.sin(a) * (1 + 0.1 * math.cos(5 * a)))
         for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)]   # round the man (at screen-metres 5.2, -1.2)


def patch_draw(v):
    v.poly(PATCH, (122, 92, 64), None)
    rng = np.random.default_rng(9)
    for _ in range(26):                                  # tufts of grass
        a, r = rng.uniform(0, 2 * math.pi), rng.uniform(0, 1)
        cx, cy = 5.2 + 3.2 * r * math.cos(a), -1.2 + 2.5 * r * math.sin(a)
        v.circle(cx, cy, rng.uniform(0.25, 0.6), (126, 146, 72), None, n=10)


def lamp(v):
    """The lamp post: a tall pole drawn through the camera (it leans away from the middle as the camera climbs)."""
    if v.cam.pos[1] < 16.0:                              # the camera is still below its head: out of shot
        return
    v.circle(0, 0, 0.35, (70, 70, 74), INK)
    v.line([(0, 0), (0, 0)], (70, 70, 74), w_m=0.3)
    base, top = v.P(0, 0, 0.0), v.P(0, 0, 10.0)
    v.d.line([base, top], fill=INK, width=int(max(2, 0.34 * v.k)))
    v.d.line([base, top], fill=(96, 98, 104), width=int(max(1, 0.22 * v.k)))
    hx, hy = top
    r = 0.55 * v.k * (v.P(0, 0.55, 10.0)[1] - hy) / max(0.55 * v.k, 1e-6) if v.k else 0
    r = abs(v.P(0, 0.6, 10.0)[1] - hy)
    v.d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=WHITE, outline=INK, width=v.lw)


# ------------------------------------------------------------------------------------------------ surroundings
def surroundings(v):
    rng = np.random.default_rng(4)
    # houses with brown roofs (bottom left and left), in rows along the verges
    for i in range(80):
        ang, r = rng.choice([rng.uniform(150, 205), rng.uniform(345, 385), rng.uniform(62, 128)]), rng.uniform(60, 120)
        if min(angdist(ang, m) for m in MINIS) < (ARM_W / 2 + 9) / r * 57.3:
            continue
        x, y = pol(r, ang)
        roof = tuple(int(c) for c in rng.choice([(150, 96, 70), (128, 84, 64), (140, 104, 82)]))
        pts = rrect(x, y, 9.0, 7.0, ang + 90, 0.2, 2)
        v.poly([(px + SUN[0] * 1.5, py + SUN[1] * 1.5) for px, py in pts], (0, 0, 0, 60), None)
        v.poly(pts, roof, INK)
        a = ang + 90
        v.line([(x - 4.5 * math.cos(math.radians(a)), y - 4.5 * math.sin(math.radians(a))),
                (x + 4.5 * math.cos(math.radians(a)), y + 4.5 * math.sin(math.radians(a)))], tuple(int(c * 0.78) for c in roof), w_m=0.4)
    # the flat-roofed block (right) and its car park
    v.poly(rrect(70, -52, 44, 18, 82, 0.3, 2), (196, 192, 186), INK)
    v.poly(rrect(70, -52, 40, 14, 82, 0.3, 2), (180, 176, 170), None)
    for i in range(8):
        v.poly(rrect(62 + i * 0.4, -66 + i * 3.0, 4.4, 1.9, 172, 0.5, 3), tuple(int(c) for c in rng.choice(CAR_COLS)), INK)
    # trees on the verges
    for i in range(60):
        ang, r = rng.uniform(0, 360), rng.uniform(56, 130)
        if min(angdist(ang, m) for m in MINIS) < (ARM_W / 2 + 6) / r * 57.3:
            continue
        x, y = pol(r, ang)
        if math.hypot(x - BURNT_AT[0], y - BURNT_AT[1]) < 9 or math.hypot(x - STADIUM[0], y - STADIUM[1]) < 30:
            continue                                     # keep trees off the burnt-out car and the stadium
        if (150 < ang < 205 or ang > 345 or ang < 25 or 62 < ang < 128) and r > 58:
            continue
        rr = rng.uniform(2.5, 4.5)
        v.circle(x + SUN[0] * 2, y + SUN[1] * 2, rr, (0, 0, 0, 60), None)
        v.circle(x, y, rr, (66, 110, 56), INK)
        v.circle(x - rr * 0.3, y - rr * 0.3, rr * 0.5, (86, 132, 66), None)
    # the stadium's corner (the County Ground), top left, as in the first layout (Sam, 8 Nov: "never wanted the angle
    # to change, just move it")
    sx, sy = STADIUM
    v.poly(rrect(sx - 20, sy - 30, 110, 70, 30, 6, 4), (90, 150, 70), INK)            # the pitch beyond
    for j in range(5):
        v.poly(rrect(sx - 20 + j * 8 * math.cos(math.radians(30)), sy - 30 + j * 8 * math.sin(math.radians(30)),
                     6, 70, 30, 0.1, 2), (104, 166, 82), None)
    v.poly(rrect(sx, sy, 80, 16, 30, 1, 3), (206, 210, 214), INK, y=6.0)               # the stand's roof
    for j in range(-9, 10):
        a = math.radians(30)
        p = (sx + j * 4 * math.cos(a), sy + j * 4 * math.sin(a))
        v.line([(p[0] + 8 * math.sin(a), p[1] - 8 * math.cos(a)), (p[0] - 8 * math.sin(a), p[1] + 8 * math.cos(a))],
               (170, 176, 184), w_m=0.4, y=6.0)
    v.circle(sx + 34, sy + 30, 1.4, (120, 120, 126), INK)                               # floodlight pylon foot


STADIUM = (-62, -118)


# ------------------------------------------------------------------------------------------------ routes
CAR_COLS = [(240, 240, 238), (32, 32, 36), (172, 174, 180), (178, 32, 38), (44, 76, 156), (240, 240, 238),
            (172, 174, 180), (32, 32, 36)]


def _arc(c, r, a0, a1, step=8):
    n = max(2, int(abs(a1 - a0) / step) + 1)
    return [(c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a))) for a in np.linspace(a0, a1, n)]


def _smooth(pts, it=3):
    p = np.array(pts, float)
    for _ in range(it):
        q = [p[0]]
        for a, b in zip(p[:-1], p[1:]):
            q += [0.75 * a + 0.25 * b, 0.25 * a + 0.75 * b]
        q.append(p[-1])
        p = np.array(q)
    return p


def route(i, j, lane=2.4, far=130):
    """In along road i (keeping left), clockwise round mini i, anticlockwise round the inner ring, clockwise round
    mini j, out along road j (keeping left)."""
    mi, mj = MINIS[i], MINIS[j]
    ui, uj = udir(mi), udir(mj)
    li = udir(mi + 90)                                   # the left of a driver coming in
    lj = udir(mj - 90)                                   # the left of a driver going out
    ci, cj = pol(R_MINI, mi), pol(R_MINI, mj)
    pts = [(ui[0] * far + li[0] * lane, ui[1] * far + li[1] * lane),
           (ui[0] * (R_EDGE + 4) + li[0] * lane, ui[1] * (R_EDGE + 4) + li[1] * lane)]
    pts += _arc(ci, 7.0, mi + 20, mi + 160)
    a_in, a_out = mi, mj
    while a_out > a_in:                                  # anticlockwise: angle decreasing
        a_out -= 360
    pts += _arc((0, 0), R_RING, a_in - 8, a_out + 8)
    pts += _arc(cj, 7.0, mj + 200, mj + 340)
    pts += [(uj[0] * (R_EDGE + 4) + lj[0] * lane, uj[1] * (R_EDGE + 4) + lj[1] * lane),
            (uj[0] * far + lj[0] * lane, uj[1] * far + lj[1] * lane)]
    p = _smooth(pts)
    seg = np.hypot(*(p[1:] - p[:-1]).T)
    return p, np.concatenate([[0], np.cumsum(seg)])


def at(rt, s):
    p, cum = rt
    s = s % cum[-1]
    k = int(np.searchsorted(cum, s) - 1)
    k = max(0, min(k, len(p) - 2))
    u = (s - cum[k]) / max(cum[k + 1] - cum[k], 1e-6)
    a, b = p[k], p[k + 1]
    pos = a + (b - a) * u
    return pos[0], pos[1], math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


# (from road, to road, speed m/s, offset m, kind, colour index)
TRAFFIC = [(0, 2, 6.5, 0, 'car', 0), (0, 3, 6.5, 70, 'car', 1), (1, 4, 6.0, 20, 'car', 2), (1, 3, 6.0, 120, 'car', 3),
           (2, 0, 6.5, 40, 'car', 4), (2, 4, 6.5, 150, 'car', 5), (3, 1, 6.0, 10, 'car', 6), (3, 0, 6.0, 95, 'car', 7),
           (4, 2, 6.5, 60, 'car', 2), (4, 1, 6.5, 180, 'car', 0), (0, 4, 6.0, 210, 'car', 3), (2, 1, 6.0, 230, 'car', 1),
           (3, 2, 5.5, 140, 'bus', 0), (1, 0, 7.0, 75, 'moped', 0), (4, 3, 6.0, 110, 'car', 4), (1, 2, 6.5, 260, 'car', 5)]
_ROUTES = {}
OFFS = {}                               # per-car nudges found by `untangle` (no car passes through another)


_SIM = {}
SIM_T0, SIM_DT = 8.0, 1 / 24


def _simulate():
    """Traffic that gives way: every vehicle moves along its route at its own speed but waits while another is just
    ahead of it (within 6 m, in front); a car held 2.5 s creeps on. Run once from 8 s, cached per step."""
    cars = []
    for n, (i, j, sp, off, kind, c) in enumerate(TRAFFIC):
        rt = _ROUTES.setdefault((i, j), route(i, j))
        reps = 1 if kind != 'car' else 3
        for r in range(reps):
            cars.append(dict(rt=rt, sp=sp, s=off + r * rt[1][-1] / reps + sp * (SIM_T0 + 40), kind=kind,
                             col=CAR_COLS[(c + 3 * r) % len(CAR_COLS)], held=0.0,
                             L={'car': 4.4, 'bus': 11.5, 'moped': 1.9}[kind]))
    steps = int((31.7 - SIM_T0) / SIM_DT) + 2
    frames = []
    for _ in range(steps):
        pos = [at(c['rt'], c['s']) for c in cars]
        frames.append([(p[0], p[1], p[2], c['kind'], c['col']) for p, c in zip(pos, cars)])
        for a, c in enumerate(cars):
            x, y, h = pos[a]
            fx, fy = math.cos(math.radians(h)), math.sin(math.radians(h))
            block = False
            for b, (x2, y2, h2) in enumerate(pos):
                if a == b:
                    continue
                dx, dy = x2 - x, y2 - y
                ahead = dx * fx + dy * fy
                side = abs(-dx * fy + dy * fx)
                if 0 < ahead < (c['L'] + cars[b]['L']) / 2 + 2.6 and side < 2.6:
                    block = True
                    break
            if block and c['held'] < 2.5:
                c['held'] += SIM_DT
            else:
                c['held'] = 0.0
                c['s'] += c['sp'] * SIM_DT
    return frames


def vehicles(t):
    """Every vehicle: (sx, sy, heading, kind, colour)."""
    if 'f' not in _SIM:
        _SIM['f'] = _simulate()
    f = _SIM['f']
    k = int(round((t - SIM_T0) / SIM_DT))
    return f[max(0, min(k, len(f) - 1))]


def car(v, x, y, h, kind, col):
    Lm, Wm = {'car': (4.4, 1.85), 'bus': (11.5, 2.55), 'moped': (1.9, 0.7)}[kind]
    if kind == 'moped':
        return moped(v, x, y, h)
    if kind == 'bus':
        col = (236, 236, 232)
    v.poly(rrect(x + SUN[0] * 0.8, y + SUN[1] * 0.8, Lm, Wm, h, 0.5, 3), (0, 0, 0, 70), None)
    v.poly(rrect(x, y, Lm, Wm, h, 0.5, 3), col, INK)
    ca, sa = math.cos(math.radians(h)), math.sin(math.radians(h))

    def L(u, w):
        return (x + u * ca - w * sa, y + u * sa + w * ca)
    if kind == 'bus':
        v.poly([L(Lm * 0.5 - 0.3, -Wm * 0.42), L(Lm * 0.5 - 0.3, Wm * 0.42), L(Lm * 0.5 - 1.0, Wm * 0.42),
                L(Lm * 0.5 - 1.0, -Wm * 0.42)], (40, 46, 56), None)
        v.line([L(-Lm * 0.45, 0), L(Lm * 0.35, 0)], (40, 80, 160), w_m=0.5)
        return
    v.poly([L(0.25, -Wm * 0.42), L(1.05, -Wm * 0.38), L(1.05, Wm * 0.38), L(0.25, Wm * 0.42)], (40, 46, 56), None)
    v.poly([L(-1.0, -Wm * 0.38), L(-1.5, -Wm * 0.34), L(-1.5, Wm * 0.34), L(-1.0, Wm * 0.38)], (40, 46, 56), None)


# ------------------------------------------------------------------------------------------------ people and bikes
def person(v, x, y, h, top, hair, t, walk=1.0, punch=0.0, hood=None, arms=None, lean=0.0):
    """A person from above, house style: shoulders, arms, head (hair or hood), enlarged by v.enl."""
    e = v.enl
    ca, sa = math.cos(math.radians(h)), math.sin(math.radians(h))

    def L(u, w):
        return (x + (u * ca - w * sa) * e, y + (u * sa + w * ca) * e)
    ph = math.sin(t * 9.0) * walk
    v.circle(*[c + s * 0.12 * e for c, s in zip((x, y), SUN)], 0.28 * e, (0, 0, 0, 38), None)
    for side in (-1, 1):                                 # feet stepping
        f = L(0.16 * ph * side, side * 0.1)
        v.circle(f[0], f[1], 0.07 * e, (30, 30, 30), None)
    for side, sw in ((-1, ph), (1, -ph)):                # arms: swinging, or a punch thrown forward
        sh = L(0.0, side * 0.2)
        reach = (punch if side == 1 else 0.0) if arms is None else arms[0 if side == -1 else 1]
        hand = L(0.12 * sw + 0.55 * reach, side * (0.26 - 0.14 * reach))
        v.line([sh, hand], INK, w_m=0.17 * e)
        v.line([sh, hand], top, w_m=0.11 * e)
        v.circle(hand[0], hand[1], 0.065 * e, (232, 190, 160), INK)
    c0 = L(0, 0)
    v.poly(rrect(c0[0], c0[1], 0.3 * e, 0.6 * e, h, 0.12 * e, 3), top, INK)
    hc = L(0.02 + lean, 0)
    if hood:
        v.circle(hc[0], hc[1], 0.15 * e, hood, INK)
        f = L(0.12 + lean, 0)
        v.circle(f[0], f[1], 0.06 * e, (40, 34, 30), None)       # the hood's dark opening
    else:
        v.circle(hc[0], hc[1], 0.12 * e, (232, 190, 160), INK)       # the head from above: skin, a short crop
        b = L(-0.02, 0)
        v.circle(b[0], b[1], 0.095 * e, hair, None)


def ebike(v, x, y, h, hood, top, t):
    e = v.enl
    ca, sa = math.cos(math.radians(h)), math.sin(math.radians(h))

    def L(u, w):
        return (x + (u * ca - w * sa) * e, y + (u * sa + w * ca) * e)
    for k in range(3):                                   # speed lines behind (shorter, finer: Sam, 9 Nov)
        a, b = L(-0.95 - k * 0.1, (k - 1) * 0.2), L(-1.55 - k * 0.2, (k - 1) * 0.2)
        v.line([a, b], (255, 255, 255, 140), w_m=0.045 * e)
    v.line([L(-0.85, 0), L(0.85, 0)], INK, w_m=0.16 * e)        # wheels and frame
    v.line([L(0.55, -0.32), L(0.55, 0.32)], INK, w_m=0.08 * e)  # handlebars
    person(v, *L(-0.05, 0), h, top, None, t, walk=0.0, hood=hood, arms=(0.55, 0.55), lean=0.15)


def moped(v, x, y, h):
    e = v.enl
    ca, sa = math.cos(math.radians(h)), math.sin(math.radians(h))

    def L(u, w):
        return (x + (u * ca - w * sa) * e, y + (u * sa + w * ca) * e)
    v.poly(rrect(*L(0, 0), 1.9 * e, 0.6 * e, h, 0.25 * e, 3), (200, 40, 40), INK)
    v.line([L(0.7, -0.35), L(0.7, 0.35)], INK, w_m=0.08 * e)
    person(v, *L(0.05, 0), h, (40, 40, 44), None, 0, walk=0.0, hood=(236, 236, 232), arms=(0.5, 0.5))
    v.poly(rrect(*L(-0.6, 0), 0.6 * e, 0.6 * e, h, 0.05, 2), (214, 52, 40), INK)    # the food box (no logo)
    v.line([L(-0.85, -0.2), L(-0.35, -0.2)], (250, 210, 200), w_m=0.05 * e)


def ebike_pos(n, t):
    """The two teens: clockwise round the inner ring (the wrong way), inside the traffic, weaving, then out across the
    hatching and back in: far too fast (12 m/s; the cars do 6)."""
    a = 120 + (t * 12.0 / 12.7) * 57.3 + n * 38   # clockwise = angle increasing
    r = 12.7 + 0.5 * math.sin(t * 3.1 + n * 1.7)
    x, y = pol(r, a)
    h = a + 90 + math.degrees(math.atan(0.5 * 3.1 * math.cos(t * 3.1 + n * 1.7) / (12.0)))
    return x, y, h


WALKERS = [  # (path points, speed m/s, offset, top colour, hair colour)
    ([pol(52, 205), pol(140, 205)], 1.3, 0, (236, 236, 232), (60, 44, 30)),
    ([pol(140, 216), pol(52, 216)], 1.2, 30, (200, 60, 60), (30, 26, 24)),
    ([pol(52, 276), pol(150, 276)], 1.4, 10, (90, 120, 60), (180, 150, 90)),
    ([pol(150, 288), pol(52, 288)], 1.1, 60, (236, 236, 232), (80, 60, 40)),
    ([pol(52, 333), pol(150, 333)], 1.3, 40, (232, 120, 160), (40, 30, 24)),
    ([pol(52, 39), pol(150, 39)], 1.2, 5, (150, 152, 158), (90, 66, 44)),
    ([pol(150, 52), pol(52, 52)], 1.3, 70, (70, 90, 150), (30, 26, 24)),
    ([pol(52, 142), pol(82, 142)], 1.1, 20, (220, 180, 60), (120, 80, 50)),
    ([pol(82, 155), pol(52, 155)], 1.4, 45, (150, 152, 158), (200, 170, 110)),
    ([pol(58, 175), pol(80, 182), pol(110, 186)], 1.2, 15, (150, 200, 230), (40, 30, 24)),
]


def walkers(v, t):
    for pts, sp, off, top, hair in WALKERS:
        p = np.array(pts, float)
        seg = np.hypot(*(p[1:] - p[:-1]).T)
        cum = np.concatenate([[0], np.cumsum(seg)])
        s = (off + sp * (t + 20)) % cum[-1]
        k = max(0, min(int(np.searchsorted(cum, s) - 1), len(p) - 2))
        u = (s - cum[k]) / seg[k]
        x, y = p[k] + (p[k + 1] - p[k]) * u
        h = math.degrees(math.atan2(*(p[k + 1] - p[k])[::-1]))
        if v.visible(x, y, 3):
            person(v, x, y, h, top, hair, t + off)


FIGHT_AT, FIGHT_DIR = (40.0, -68.0), 22.6
FIGHT_PATH = [(FIGHT_AT[0] - 18 * math.cos(math.radians(FIGHT_DIR)), FIGHT_AT[1] - 18 * math.sin(math.radians(FIGHT_DIR))),
              (FIGHT_AT[0] + 40 * math.cos(math.radians(FIGHT_DIR)), FIGHT_AT[1] + 40 * math.sin(math.radians(FIGHT_DIR)))]
FIGHT = [  # (side, along-path offset m, across m, top, hair): two groups facing each other along the path
    (-1, -0.45, 0.1, (236, 236, 232), (60, 44, 30)), (-1, -0.95, 0.55, (210, 56, 56), (30, 26, 24)),
    (-1, -1.0, -0.5, (150, 200, 230), (180, 150, 90)), (-1, -1.5, 0.05, (232, 210, 70), (40, 30, 24)),
    (1, 0.45, -0.1, (150, 152, 158), (90, 66, 44)), (1, 0.95, 0.5, (70, 110, 190), (40, 30, 24)),
    (1, 1.0, -0.55, (236, 236, 232), (200, 170, 110)), (1, 1.5, 0.0, (120, 170, 90), (60, 44, 30)),
]


def fight(v, t):
    """Two groups of lads scrapping on the path: the front pairs swinging punches, the rest surging and shoving,
    the whole scrum lurching one way then the other."""
    fx, fy = FIGHT_AT
    if not v.visible(fx, fy, 12):
        return
    ax = udir(FIGHT_DIR)                                  # along the path
    ac = udir(FIGHT_DIR + 90)                                       # across it
    surge = 0.35 * math.sin(t * 1.3)
    for n, (side, al, cr, top, hair) in enumerate(FIGHT):
        jit = 0.25 * math.sin(t * 7 + n * 1.9)
        lunge = max(0.0, math.sin(t * 5.5 + n * 2.3))
        a = al + surge - side * 0.12 * lunge + jit * 0.1
        c = cr + 0.08 * math.sin(t * 2.2 + n)
        x, y = fx + ax[0] * a * v.enl + ac[0] * c * v.enl, fy + ax[1] * a * v.enl + ac[1] * c * v.enl
        h = FIGHT_DIR + (180 if side == 1 else 0) + 25 * math.sin(t * 3 + n)
        person(v, x, y, h, top, hair, t + n, walk=0.6, punch=lunge if abs(al) < 0.7 else 0.0,
               arms=None if abs(al) < 0.7 else (0.4 + 0.3 * lunge, 0.4 + 0.3 * lunge))


BURNT_AT = (-52, -84, 18)


def burnt_car(v):
    x, y, h = BURNT_AT
    if not v.visible(x, y, 10):
        return
    v.circle(x, y, 4.6, (84, 92, 52, 220), None)                     # scorched grass
    v.circle(x + 0.6, y - 0.3, 3.4, (52, 50, 40, 220), None)
    v.poly(rrect(x, y, 4.4, 1.85, h, 0.4, 3), (120, 104, 92), INK)     # the shell: rust and soot, no glass
    ca, sa = math.cos(math.radians(h)), math.sin(math.radians(h))

    def L(u, w):
        return (x + u * ca - w * sa, y + u * sa + w * ca)
    v.poly([L(0.25, -0.75), L(1.05, -0.7), L(1.05, 0.7), L(0.25, 0.75)], (24, 22, 20), None)
    v.poly([L(-1.0, -0.7), L(-1.5, -0.62), L(-1.5, 0.62), L(-1.0, 0.7)], (24, 22, 20), None)
    v.poly([L(-0.9, -0.85), L(0.2, -0.85), L(0.2, 0.85), L(-0.9, 0.85)], (34, 30, 28), None)   # roof burnt through
    for u, w, r in ((-1.6, 0.3, 0.3), (1.6, -0.4, 0.25), (0.6, 0.8, 0.22)):
        v.circle(*L(u, w), r, (150, 84, 44), None)                   # rust


# ------------------------------------------------------------------------------------------------ the frame
def draw(pil, cam, t, man_layer=None):
    """The whole roundabout through `cam` at film time t. `man_layer(pil)` draws the man, scroll and dog on the patch
    (before the traffic and the lamp post)."""
    v = View(pil, cam)
    ground(v, t)
    surroundings(v)
    burnt_car(v)
    if man_layer:
        man_layer(pil)
    for n in range(2):                                   # the two teens on e-bikes
        x, y, h = ebike_pos(n, t)
        ebike(v, x, y, h, [(30, 30, 34), (236, 236, 232)][n], [(30, 30, 34), (236, 236, 232)][n], t)
    for x, y, h, kind, col in vehicles(t):
        if v.visible(x, y, 8):
            car(v, x, y, h, kind, col)
    walkers(v, t)
    fight(v, t)
    lamp(v)
    return v


def untangle(seed=1, tries=400):
    """Nudge cars along their routes until none passes through another in the held shot."""
    rng = np.random.default_rng(seed)
    best = len(vehicle_faults(fps=4))
    for _ in range(tries):
        if best == 0:
            break
        key = (int(rng.integers(len(TRAFFIC))), int(rng.integers(3)))
        old = OFFS.get(key, 0)
        OFFS[key] = old + rng.uniform(-25, 25)
        n = len(vehicle_faults(fps=4))
        if n <= best:
            best = n
        else:
            OFFS[key] = old
    return best


def vehicle_faults(t0=17.45, t1=30.04, fps=12, gap=2.6):
    """Vehicles (and the e-bikes) passing through each other in the held shot."""
    out = []
    for f in range(int(t0 * fps), int(t1 * fps)):
        t = f / fps
        ps = [(x, y, kind) for x, y, h, kind, c in vehicles(t)] + [(*ebike_pos(n, t)[:2], 'ebike') for n in range(2)]
        for a in range(len(ps)):
            for b in range(a + 1, len(ps)):
                g = 2.1 if 'ebike' in (ps[a][2], ps[b][2]) else gap
                if math.hypot(ps[a][0] - ps[b][0], ps[a][1] - ps[b][1]) < g and \
                        math.hypot(*ps[a][:2]) < 120:
                    out.append((round(t, 2), a, b))
    return out


VIEW_SY = -32.0                         # the held view's centre, north-south (screen-metres; Sam's notes 8 Nov)


def held_cam(t):
    """The held view from above (shot 6): the roundabout low in the frame (Sam, 8 Nov), a slice of the stadium top
    left, drifting slowly."""
    u = max(0.0, t - 17.45)
    width = 118.0 + 0.6 * u
    sx, sy = -2.0 - 0.15 * u, VIEW_SY - 0.25 * u        # the frame centre in screen-metres: roundabout low
    d = width * 3.0 / 2.6                                # the climb's own height for this width: no jump
    x, _, z = W(sx, sy)
    return S.Cam((x, d, z + d * math.cos(math.radians(89.6))), (x, 0.0, z), focal=1080 * d / width)


if __name__ == '__main__':
    if len(sys.argv) >= 4 and sys.argv[1] == 'still':
        t = float(sys.argv[3])
        im = Image.new('RGBA', (1080 * SS, 1920 * SS))
        draw(im, held_cam(t), t)
        im.convert('RGB').resize((1080, 1920), Image.LANCZOS).save(sys.argv[2], quality=90)
        print('still:', sys.argv[2])
    elif len(sys.argv) >= 2 and sys.argv[1] == 'check':
        f = vehicle_faults()
        print(len(f), 'vehicle overlaps', f[:20])
    elif len(sys.argv) >= 2 and sys.argv[1] == 'untangle':
        print('left:', untangle(), {k: round(v, 1) for k, v in OFFS.items()})
    else:
        print(__doc__)
