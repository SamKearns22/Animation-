#!/usr/bin/env python3
"""Prepper Minister: the things that stand in the house (in 3D, at real size) and the effects (brief, section 2:
"believable debris, sparks, flames ... bold, hard-edged shapes that last a few frames, no glows").

Things (refs in references/prepper-minister/; sizes in sizes.SIZES):
- a tin of beans (ref beans-tin, the brand dropped): turquoise, a plain cream band reading BAKED BEANS, a few beans;
- a 2-litre bottle of water (ref water-bottle-2l, the brand dropped): ribbed, a blue cap, a plain pale blue label
  with hills;
- the crossbow and the minigun with its loop of ammo, lying on the island (shot 5, 10);
- the Alexa (ref alexa: Echo Dot 5th gen): a charcoal fabric ball on a black base, the blue light ring, two buttons;
  smashed into pieces (shot 6); its battered remains walking on tiny metal rod legs holding up a kitchen knife (12);
- the crossbow bolt (black shaft, bright vanes, a steel point).
Effects, each a flat hard-edged shape: sparks (yellow, or the robots' blue), debris and glass that fly, bounce and
stay where they land, flat grey smoke, the plasma bolt (thick cobalt streak with a pale core), tracers, the blade's
sweeping arc, muzzle and impact flashes, the room flashing with the minigun.
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import prepper_set as S          # noqa: E402
from ed import INK               # noqa: E402

FLAT = S.FLAT
G = 9.8
TEAL, TEAL_D = (64, 190, 196), (40, 150, 160)
CREAM = (244, 232, 200)
BEAN = (222, 110, 50)
WATER, WATER_D = (206, 228, 242), (170, 204, 226)
CAP = (40, 90, 200)
CHARCOAL, CHARCOAL_D = (66, 68, 74), (44, 46, 52)
COBALT, COBALT_L = (48, 112, 255), (176, 214, 255)
SPARK_Y, SPARK_W = (255, 210, 70), (255, 252, 220)
SPARK_B = (120, 180, 255)
GUN, GUN_D, GUN_L = (44, 46, 52), (26, 28, 32), (84, 88, 96)
BRASS, BRASS_D = (214, 170, 76), (166, 124, 44)
STEEL = (180, 186, 192)


def _pen(img):
    return B.Pen(img, FLAT)


# ------------------------------------------------------------------------------------------------ things
def _ring(c, r, y, n=18, a0=0.0, a1=2 * math.pi, rz=None):
    rz = rz or r
    return [(c[0] + r * math.cos(a), y, c[2] + rz * math.sin(a)) for a in np.linspace(a0, a1, n)]


def _facing_arc(cam, c):
    """The angle (in the plan) from a point towards the camera: the visible half of a cylinder is centred on it."""
    return math.atan2(cam.pos[2] - c[2], cam.pos[0] - c[0])


_TEXT = {}


def _label(text, h=60, col=(30, 70, 80)):
    if text not in _TEXT:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', h)
        l, t, r, b = f.getbbox(text)
        im = Image.new('RGBA', (r - l + 8, b - t + 8), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((4 - l, 4 - t), text, font=f, fill=col + (255,))
        _TEXT[text] = im
    return _TEXT[text]


def stamp(img, cam, a, b, text):
    """Lettering laid on a short span from 3D point a to b (its middle line), scaled once (it never pulses)."""
    (xa, ya), _ = cam.project(a)
    (xb, yb), _ = cam.project(b)
    w = math.hypot(xb - xa, yb - ya) * B.SS
    if w < 18:
        return
    im = _label(text)
    k = w / im.width
    sm = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
    ang = math.degrees(math.atan2(yb - ya, xb - xa))
    sm = sm.rotate(-ang, expand=True, resample=Image.BICUBIC)
    cx, cy = (xa + xb) / 2 * B.SS, (ya + yb) / 2 * B.SS
    img.alpha_composite(sm, (int(cx - sm.width / 2), int(cy - sm.height / 2))) if cx - sm.width / 2 >= 0 and \
        cy - sm.height / 2 >= 0 else img.paste(sm, (int(cx - sm.width / 2), int(cy - sm.height / 2)), sm)


def tin(img, cam, c, dent=0.0, lid=True):
    """A tin of beans standing at base point c (x, y, z): 66 mm across, 110 mm tall."""
    p = _pen(img)
    r, h = 0.033, 0.11
    if cam.depth(c) < 0.15:
        return
    S.cylinder(c, r, h, {'side': TEAL, 'top': (196, 200, 204)}, n=18)[0].draw(img, cam, p)
    a = _facing_arc(cam, c)
    band = _ring(c, r * 1.004, c[1] + 0.035, 12, a - 1.35, a + 1.35) + _ring(c, r * 1.004, c[1] + 0.078, 12, a + 1.35, a - 1.35)
    cam.poly(p, band, CREAM, INK, 1.2)
    for k, u in enumerate((-0.5, -0.15, 0.2, 0.5)):
        q = (c[0] + r * 1.01 * math.cos(a + u), c[1] + 0.045 + 0.006 * (k % 2), c[2] + r * 1.01 * math.sin(a + u))
        (x, y), kk = cam.project(q)
        p.ell(x, y, max(1.5, 0.006 * kk), max(1.2, 0.004 * kk), BEAN, None)
    if lid:
        top = _ring(c, r, c[1] + h, 18)
        cam.poly(p, top, (196, 200, 204), INK, 1.4)
        cam.poly(p, _ring(c, r * 0.78, c[1] + h + 0.001, 14), (176, 180, 186), None)
    stamp(img, cam, (c[0] + r * 1.02 * math.cos(a + 0.7), c[1] + 0.067, c[2] + r * 1.02 * math.sin(a + 0.7)),
          (c[0] + r * 1.02 * math.cos(a - 0.7), c[1] + 0.067, c[2] + r * 1.02 * math.sin(a - 0.7)), 'BAKED BEANS')
    if dent > 0:                                               # the dent where it hit the robot
        q = (c[0] + r * math.cos(a), c[1] + 0.09, c[2] + r * math.sin(a))
        (x, y), kk = cam.project(q)
        p.poly([(x - 0.012 * kk, y), (x, y - 0.01 * kk), (x + 0.012 * kk, y + 0.002 * kk), (x, y + 0.008 * kk)],
               TEAL_D, INK, 1.0)


def bottle(img, cam, c):
    """A 2-litre water bottle at base point c: 105 mm across, 330 mm tall, ribbed, a blue cap, a plain label."""
    p = _pen(img)
    r = 0.052
    if cam.depth(c) < 0.15:
        return
    a = _facing_arc(cam, c)
    body = S.cylinder(c, r, 0.24, {'side': WATER, 'top': WATER}, n=18, top=False)[0]
    body.draw(img, cam, p)
    sh = _ring(c, r, c[1] + 0.24, 16) + _ring(c, 0.016, c[1] + 0.3, 10)
    S.blob3(img, cam, p, sh, WATER, INK, 1.6)
    S.cylinder((c[0], c[1] + 0.3, c[2]), 0.016, 0.012, {'side': WATER_D, 'top': WATER_D}, n=10)[0].draw(img, cam, p)
    S.cylinder((c[0], c[1] + 0.312, c[2]), 0.018, 0.018, {'side': CAP, 'top': CAP}, n=10)[0].draw(img, cam, p)
    for y in (0.03, 0.06, 0.2, 0.225):                         # the ribs
        cam.line(p, _ring(c, r * 1.003, c[1] + y, 10, a - 1.4, a + 1.4), WATER_D, 1.2)
    lab = _ring(c, r * 1.006, c[1] + 0.09, 12, a - 1.35, a + 1.35) + _ring(c, r * 1.006, c[1] + 0.17, 12, a + 1.35, a - 1.35)
    cam.poly(p, lab, (150, 196, 230), INK, 1.2)
    hills = [(c[0] + r * 1.01 * math.cos(a + u), c[1] + 0.1 + 0.03 * (1 - abs(u)) * (1 + 0.4 * math.sin(4 * u)),
              c[2] + r * 1.01 * math.sin(a + u)) for u in np.linspace(-1.3, 1.3, 12)]
    hills += [(c[0] + r * 1.01 * math.cos(a + u), c[1] + 0.092, c[2] + r * 1.01 * math.sin(a + u)) for u in np.linspace(1.3, -1.3, 6)]
    cam.poly(p, hills, (70, 130, 170), None)
    hl = [(c[0] + r * 1.01 * math.cos(a + 0.6), c[1] + 0.02, c[2] + r * 1.01 * math.sin(a + 0.6)),
          (c[0] + r * 1.01 * math.cos(a + 0.45), c[1] + 0.02, c[2] + r * 1.01 * math.sin(a + 0.45)),
          (c[0] + r * 1.01 * math.cos(a + 0.45), c[1] + 0.23, c[2] + r * 1.01 * math.sin(a + 0.45)),
          (c[0] + r * 1.01 * math.cos(a + 0.6), c[1] + 0.23, c[2] + r * 1.01 * math.sin(a + 0.6))]
    cam.poly(p, hl, (246, 250, 252), None)


def _local(c, yaw):
    a = math.radians(yaw)
    def L(u, y, v):                         # u along its length (forward), v across, y up
        return (c[0] + u * math.sin(a) + v * math.cos(a), c[1] + y, c[2] + u * math.cos(a) - v * math.sin(a))
    return L


def crossbow3(img, cam, c, yaw):
    """The crossbow lying on the island: the rail and stock, the grip on its side, the limbs spread across the front,
    the string, the red-dot sight, a bolt."""
    p = _pen(img)
    L = _local(c, yaw)
    def bx(u0, u1, v0, v1, y0, y1, col):
        parts = S.obox(((L((u0 + u1) / 2, y0, (v0 + v1) / 2))), (v1 - v0, y1 - y0, u1 - u0), yaw, {'all': col})
        S.draw_parts(img, cam, [parts], p)
    bx(-0.36, -0.12, -0.012, 0.012, 0.0, 0.05, GUN_D)       # stock
    bx(-0.12, 0.34, -0.022, 0.022, 0.0, 0.045, GUN)          # rail
    bx(-0.08, -0.02, 0.022, 0.09, 0.0, 0.03, GUN_D)          # grip, lying on its side
    bx(0.0, 0.07, -0.015, 0.015, 0.045, 0.08, GUN_D)         # sight
    tip = L(0.32, 0.03, 0.0)
    for sg in (-1, 1):
        a = L(0.26, 0.03, sg * 0.3)
        m = L(0.33, 0.03, sg * 0.15)
        cam.line(p, [tip, m, a], GUN_D, max(2.0, 0.02 * cam.project(tip)[1]))
        cam.line(p, [a, L(0.04, 0.05, 0.0)], (230, 230, 226), 1.4)
    cam.line(p, [L(0.02, 0.05, 0.0), L(0.4, 0.05, 0.0)], (30, 30, 30), max(1.5, 0.008 * cam.project(tip)[1]))


def minigun3(img, cam, c, yaw, belt=True):
    """The minigun lying on the island (refs minigun-1, -2) with its loop of ammo beside it."""
    p = _pen(img)
    L = _local(c, yaw)
    if belt:                                                   # the loop of ammo: brass rounds in a curling belt
        pts = [L(-0.1 + 0.18 * math.cos(u), 0.012, -0.22 + 0.13 * math.sin(u) - 0.02 * u) for u in np.linspace(0, 5.6, 26)]
        for q0, q1 in zip(pts, pts[1:]):
            (x0, y0), k0 = cam.project(q0)
            (x1, y1), k1 = cam.project(q1)
            w = 0.014 * k0
            dx, dy = x1 - x0, y1 - y0
            n = math.hypot(dx, dy) or 1.0
            nx, ny = -dy / n * w, dx / n * w
            p.poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)], BRASS, INK, 1.0)
    def bx(u0, u1, v0, v1, y0, y1, col):
        S.draw_parts(img, cam, [S.obox(L((u0 + u1) / 2, y0, (v0 + v1) / 2), (v1 - v0, y1 - y0, u1 - u0), yaw, {'all': col})], p)
    bx(-0.42, -0.4, -0.07, 0.07, 0.0, 0.12, GUN_D)           # spade grips
    bx(-0.4, -0.05, -0.065, 0.065, 0.0, 0.13, GUN)           # housing
    k = cam.project(L(0.2, 0.06, 0))[1]
    for i in range(6):                                         # six barrels round a spindle
        a = i * math.pi / 3
        v, y = 0.032 * math.cos(a), 0.062 + 0.032 * math.sin(a)
        cam.line(p, [L(-0.05, y, v), L(0.48, y, v)], INK, max(2.0, 0.026 * k))
        cam.line(p, [L(-0.05, y, v), L(0.48, y, v)], GUN_L if i % 2 else GUN, max(1.0, 0.018 * k))
    for u in (0.0, 0.25, 0.46):
        S.blob3(img, cam, p, [L(u + du, 0.062 + 0.05 * math.sin(a), 0.05 * math.cos(a)) for a in np.linspace(0, 6.28, 12)
                              for du in (0, 0.02)], GUN_D, INK, 1.4)
    cam.line(p, [L(-0.3, 0.13, 0), L(-0.26, 0.2, 0), L(-0.12, 0.2, 0), L(-0.08, 0.13, 0)], GUN_D, max(2.0, 0.02 * k))


def alexa(img, cam, c, light=True):
    """The Echo Dot (ref alexa): a charcoal fabric ball 100 mm across on a black base, the blue light ring at the
    bottom, two buttons on top, the fabric's weave as fine flecks."""
    p = _pen(img)
    r = 0.05
    ctr = (c[0], c[1] + 0.045, c[2])
    S.blob3(img, cam, p, S.sphere_pts(ctr, r, 9), CHARCOAL, INK, 1.6)
    rng = np.random.default_rng(4)
    for _ in range(40):                                        # the fabric's weave
        th, ph = rng.uniform(0, math.pi * 0.85), rng.uniform(0, 2 * math.pi)
        q = (ctr[0] + r * math.sin(th) * math.cos(ph), ctr[1] + r * math.cos(th), ctr[2] + r * math.sin(th) * math.sin(ph))
        if np.dot(np.subtract(q, ctr), np.subtract(cam.pos, q)) > 0:
            (x, y), k = cam.project(q)
            p.ell(x, y, max(0.6, 0.002 * k), max(0.6, 0.002 * k), CHARCOAL_D, None)
    base = _ring(c, r * 0.86, c[1] + 0.003, 20) + _ring(c, r * 0.86, c[1] + 0.012, 20)
    S.blob3(img, cam, p, base, (20, 20, 24), INK, 1.4)
    a = _facing_arc(cam, c)
    if light:
        ring = _ring(c, r * 0.88, c[1] + 0.012, 12, a - 1.4, a + 1.4) + _ring(c, r * 0.88, c[1] + 0.018, 12, a + 1.4, a - 1.4)
        cam.poly(p, ring, (90, 190, 255), None)
    for dx in (-0.015, 0.015):
        q = _ring((ctr[0] + dx, 0, ctr[2]), 0.005, ctr[1] + r * 0.99, 8)
        cam.poly(p, q, CHARCOAL_D, INK, 1.0)


def alexa_walker(img, cam, c, t, facing=0.0, knife=True):
    """Its battered remains up on tiny metal rod legs (shot 12): the ball cracked open (a jagged hole, a green circuit
    board and wires showing), four thin jointed rods for legs scuttling, a fifth rod holding up a kitchen knife."""
    p = _pen(img)
    r = 0.05
    L = _local(c, facing)
    lift = 0.14
    ctr = L(0, lift + 0.045, 0)
    for k, (u, v) in enumerate(((0.03, 0.04), (0.03, -0.04), (-0.03, 0.04), (-0.03, -0.04))):     # legs, far first
        ph = t * 14 + k * math.pi / 2 + (math.pi if k % 2 else 0)
        foot = L(u * 2.4 + 0.02 * math.sin(ph), 0.0 + 0.012 * max(0, math.cos(ph)), v * 2.6)
        knee = L(u * 2.0, lift + 0.03, v * 2.4)
        hip = L(u, lift + 0.02, v)
        cam.line(p, [hip, knee, foot], INK, 3.4)
        cam.line(p, [hip, knee, foot], STEEL, 1.8)
    S.blob3(img, cam, p, S.sphere_pts(ctr, r, 9), CHARCOAL, INK, 1.6)
    hole = [L(0.035 * math.cos(q) * (1.0 if i % 2 else 0.6) + 0.03, lift + 0.05 + 0.03 * math.sin(q) * (1.0 if i % 2 else 0.6), 0.04)
            for i, q in enumerate(np.linspace(0, 6.28, 12, endpoint=False))]
    if np.dot(np.subtract(L(0.03, 0, 0.05), c), np.subtract(cam.pos, c)) > -0.01:
        cam.poly(p, hole, (30, 120, 70), INK, 1.4)
        cam.line(p, [L(0.02, lift + 0.05, 0.045), L(0.05, lift + 0.07, 0.05)], (214, 60, 40), 1.6)
    if knife:                                                  # a rod arm holding the knife up
        sh = L(0.02, lift + 0.07, 0.03)
        hand = L(0.05, lift + 0.2, 0.06 + 0.01 * math.sin(t * 9))
        cam.line(p, [sh, hand], INK, 3.4)
        cam.line(p, [sh, hand], STEEL, 1.8)
        kitchen_knife(img, cam, hand, (0.25, 0.95, 0.15))


def kitchen_knife(img, cam, hand, d):
    """A sharp kitchen knife held point up: a black handle, a broad steel blade tapering to the point (20 cm)."""
    p = _pen(img)
    d = np.asarray(d, float) / np.linalg.norm(d)
    side = np.cross(d, [0, 0, 1.0])
    side = side / (np.linalg.norm(side) or 1)
    h = np.asarray(hand, float)
    def Q(u, v):
        return tuple(h + d * u + side * v)
    cam.poly(p, [Q(-0.06, -0.012), Q(0.02, -0.012), Q(0.02, 0.012), Q(-0.06, 0.012)], (24, 22, 24), INK, 1.2)
    cam.poly(p, [Q(0.02, -0.02), Q(0.12, -0.022), Q(0.2, 0.0), Q(0.02, 0.02)], STEEL, INK, 1.4)
    cam.poly(p, [Q(0.03, 0.0), Q(0.15, -0.008), Q(0.15, -0.002), Q(0.03, 0.008)], (232, 236, 240), None)


def bolt(img, cam, tip, d, length=0.42):
    """A crossbow bolt: a steel point, a black shaft, three bright vanes at the back."""
    p = _pen(img)
    d = np.asarray(d, float) / (np.linalg.norm(d) or 1)
    tip = np.asarray(tip, float)
    back = tip - d * length
    k = cam.project(tuple(tip))[1]
    cam.line(p, [tuple(back), tuple(tip - d * 0.03)], INK, max(2.0, 0.012 * k))
    cam.line(p, [tuple(back), tuple(tip - d * 0.03)], (40, 40, 44), max(1.0, 0.008 * k))
    cam.line(p, [tuple(tip - d * 0.035), tuple(tip)], (200, 204, 210), max(1.5, 0.01 * k))
    up = np.cross(d, [0, 1, 0])
    up = up / (np.linalg.norm(up) or 1)
    for sg in (-1, 1):
        cam.poly(p, [tuple(back + d * 0.08), tuple(back + up * sg * 0.025), tuple(back + up * sg * 0.025 + d * 0.03)],
                 (120, 220, 60), INK, 1.0)


# ------------------------------------------------------------------------------------------------ physics
class Piece:
    """A flying piece: launched at t0 from p0 with velocity v0, under gravity, bouncing off the floor (and the
    island's top, `tops`), the room's walls (`box`: x0, x1, z0, z1), coming to rest and staying put. 120 Hz,
    cached. Spin turns its drawing."""
    def __init__(self, p0, v0, t0, r=0.02, e=0.35, spin=8.0, box=None, tops=(), dur=6.0):
        self.t0, self.r = t0, r
        dt = 1 / 120
        self.track = []
        p, v = list(p0), list(v0)
        ang, w, rest = 0.0, spin, False
        for i in range(int(dur / dt)):
            if not rest:
                v[1] -= G * dt
                for k in range(3):
                    p[k] += v[k] * dt
                ang += w * dt
                if box:
                    x0, x1, z0, z1 = box
                    for ax, lo, hi in ((0, x0, x1), (2, z0, z1)):
                        if p[ax] < lo + r:
                            p[ax], v[ax] = lo + r, abs(v[ax]) * 0.4
                        if p[ax] > hi - r:
                            p[ax], v[ax] = hi - r, -abs(v[ax]) * 0.4
                ground = r
                for (tx0, tx1, tz0, tz1, ty) in tops:
                    if tx0 <= p[0] <= tx1 and tz0 <= p[2] <= tz1 and p[1] > ty - 0.05:
                        ground = ty + r
                if p[1] < ground:
                    p[1] = ground
                    if v[1] < 0:
                        v[1] = -v[1] * e
                    v[0] *= 0.7
                    v[2] *= 0.7
                    w *= 0.6
                    if abs(v[1]) < 0.35 and math.hypot(v[0], v[2]) < 0.2:
                        rest, v = True, [0.0, 0.0, 0.0]
            self.track.append((tuple(p), ang))

    def at(self, t):
        if t <= self.t0:
            return self.track[0]
        i = min(len(self.track) - 1, int((t - self.t0) * 120))
        return self.track[i]


def burst(t0, at, n, speed, seed, kind='chip', col=(220, 220, 214), size=0.03, up=1.5, dirn=None, box=None, tops=(),
          spread=1.0):
    """Debris thrown from a hit: n pieces, each its own size, speed and spin (never a matching set), thrown mostly
    along `dirn` (the way the hit pushes)."""
    rng = np.random.default_rng(seed)
    d0 = np.asarray(dirn if dirn is not None else (0, 0, 0), float)
    out = []
    for i in range(n):
        v = d0 * speed + rng.normal(0, speed * 0.45 * spread, 3)
        v[1] = abs(v[1]) * 0.6 + up * rng.uniform(0.4, 1.2)
        s = size * rng.uniform(0.5, 1.4)
        pc = Piece(at, tuple(v), t0, r=s * 0.4, spin=rng.uniform(-14, 14), box=box, tops=tops)
        pc.kind, pc.col, pc.size, pc.seed = kind, col, s, int(rng.integers(1 << 30))
        out.append(pc)
    return out


def draw_piece(img, cam, pc, t):
    if t < pc.t0:
        return
    (x, y, z), ang = pc.at(t)
    if cam.depth((x, y, z)) < 0.2:
        return
    (X, Y), k = cam.project((x, y, z))
    s = pc.size * k
    if s < 0.6:
        return
    p = _pen(img)
    rng = np.random.default_rng(pc.seed)
    nv = 3 if pc.kind in ('glass', 'shard') else int(rng.integers(4, 7))
    radii = rng.uniform(0.5, 1.0, nv)
    if pc.kind == 'glass':
        radii[0] = 1.6
    pts = [(X + s * r * math.cos(ang + a), Y + s * r * 0.8 * math.sin(ang + a))
           for r, a in zip(radii, np.linspace(0, 2 * math.pi, nv, endpoint=False) + rng.uniform(0, 1))]
    if pc.kind == 'glass':
        p.poly(pts, (220, 236, 246), (255, 255, 255), 1.2)
        p.line(pts[:2], INK, 1.0)
    else:
        p.poly(pts, pc.col, INK, 1.2)


# ------------------------------------------------------------------------------------------------ effects
def sparks(img, cam, t, t0, at, seed, n=14, col='yellow', speed=3.0, life=0.35, dirn=None):
    """A spray of sparks for about a third of a second: short hard streaks flying out and falling, each its own
    speed, yellow-white (or the robots' blue)."""
    if not (t0 <= t <= t0 + life + 0.2):
        return
    rng = np.random.default_rng(seed)
    p = _pen(img)
    c1, c2 = (SPARK_Y, SPARK_W) if col == 'yellow' else (SPARK_B, (230, 244, 255))
    d0 = np.asarray(dirn if dirn is not None else (0, 0, 0), float)
    for i in range(n):
        v = d0 * speed * 0.7 + rng.normal(0, speed * 0.6, 3)
        v[1] += speed * 0.3
        lf = life * rng.uniform(0.5, 1.2)
        u = t - t0
        if u > lf:
            continue
        def P(s):
            return (at[0] + v[0] * s, at[1] + v[1] * s - 0.5 * G * s * s, at[2] + v[2] * s)
        a, b = P(max(0.0, u - 0.035)), P(u)
        if cam.depth(a) < 0.2 or cam.depth(b) < 0.2:
            continue
        cam.line(p, [a, b], INK, 3.6)
        cam.line(p, [a, b], c1 if i % 3 else c2, 2.2)


def flash(img, cam, at, size, seed=0, col='yellow'):
    """A hard-edged impact or muzzle flash at a world point (a star facing us), for one or two frames."""
    if cam.depth(at) < 0.2:
        return
    (X, Y), k = cam.project(at)
    rng = np.random.default_rng(seed)
    r = size * k
    n = 10
    pts = [(X + r * (1.0 if i % 2 == 0 else rng.uniform(0.35, 0.5)) * math.cos(a),
            Y + r * (1.0 if i % 2 == 0 else rng.uniform(0.35, 0.5)) * math.sin(a))
           for i, a in enumerate(np.linspace(0, 2 * math.pi, n, endpoint=False) + rng.uniform(0, 1))]
    p = _pen(img)
    outer, mid = ((255, 160, 40), (255, 232, 110)) if col == 'yellow' else (COBALT, COBALT_L)
    p.poly(pts, outer, INK, 1.6)
    p.poly([(X + (x - X) * 0.6, Y + (y - Y) * 0.6) for x, y in pts], mid, None)
    p.poly([(X + (x - X) * 0.28, Y + (y - Y) * 0.28) for x, y in pts], (255, 255, 244), None)


def plasma(img, cam, a, b, width=0.065):
    """The plasma bolt: a thick streak from a (its tail) to b (its head), cobalt outside, a pale core, round ends."""
    if cam.depth(a) < 0.2 or cam.depth(b) < 0.2:
        return
    (xa, ya), ka = cam.project(a)
    (xb, yb), kb = cam.project(b)
    p = _pen(img)
    dx, dy = xb - xa, yb - ya
    n = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / n, dx / n
    for col, k, line in ((COBALT, 1.0, INK), (COBALT_L, 0.5, None), ((246, 250, 255), 0.22, None)):
        wa, wb = width * ka * k * 0.6, width * kb * k
        pts = [(xa + nx * wa, ya + ny * wa), (xb + nx * wb, yb + ny * wb)]
        pts += [(xb + wb * math.cos(q) * (dx / n) * 1.0 - wb * math.sin(q) * (-nx) * 0 + 0, yb) for q in ()]
        cap = [(xb + (dx / n) * wb * math.sin(q) + nx * wb * math.cos(q), yb + (dy / n) * wb * math.sin(q) + ny * wb * math.cos(q))
               for q in np.linspace(0, math.pi, 8)]
        p.poly([(xa + nx * wa, ya + ny * wa)] + cap + [(xa - nx * wa, ya - ny * wa)], col, line, 1.8)


def tracer(img, cam, a, b, u, length=1.2):
    """A bullet's streak: a short bright line part way (u, 0..1) along the path from a to b."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = np.linalg.norm(b - a) or 1.0
    d = (b - a) / L
    head = a + d * min(L, u * L)
    tail = head - d * min(length, u * L)
    if cam.depth(tuple(head)) < 0.2 or cam.depth(tuple(tail)) < 0.2:
        return
    p = _pen(img)
    cam.line(p, [tuple(tail), tuple(head)], (255, 236, 150), 2.6)
    cam.line(p, [tuple(tail + (head - tail) * 0.6), tuple(head)], (255, 255, 240), 1.6)


def blade_arc(img, cam, pts, width=0.14):
    """The blade's sweep: a crescent along the path its tip took (a few frames), cobalt with a pale edge."""
    pts = [q for q in pts if cam.depth(q) > 0.2]
    if len(pts) < 3:
        return
    p = _pen(img)
    scr = [cam.project(q) for q in pts]
    outer, inner = [], []
    n = len(scr)
    for i, ((x, y), k) in enumerate(scr):
        j = min(n - 1, i + 1)
        i0 = max(0, i - 1)
        dx, dy = scr[j][0][0] - scr[i0][0][0], scr[j][0][1] - scr[i0][0][1]
        m = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / m, dx / m
        w = width * k * math.sin(math.pi * i / (n - 1))
        outer.append((x + nx * w * 0.2, y + ny * w * 0.2))
        inner.append((x - nx * w, y - ny * w))
    p.poly(outer + inner[::-1], COBALT, INK, 1.6)
    p.poly(outer + [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(outer, inner)][::-1], COBALT_L, None)


def smoke(img, cam, t, t0, at, seed, n=4, life=1.4, size=0.12):
    """Flat grey smoke (Sam, 24 Oct): a few lumpy puffs rising, growing and thinning out."""
    if not (t0 <= t <= t0 + life):
        return
    u = (t - t0) / life
    rng = np.random.default_rng(seed)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    p = _pen(lay)
    for i in range(n):
        off = rng.normal(0, 0.06, 3)
        c = (at[0] + off[0], at[1] + 0.35 * u + abs(off[1]), at[2] + off[2])
        if cam.depth(c) < 0.2:
            continue
        (X, Y), k = cam.project(c)
        r = size * (0.6 + 1.6 * u) * k * rng.uniform(0.8, 1.2)
        a = int(170 * (1 - u))
        pts = [(X + r * rng.uniform(0.85, 1.1) * math.cos(q), Y + r * rng.uniform(0.85, 1.1) * math.sin(q))
               for q in np.linspace(0, 2 * math.pi, 9, endpoint=False)]
        p.poly(pts, (150, 150, 154, a), None)
    img.alpha_composite(lay)


def room_flash(img, amount):
    """The room flashing with the minigun's fire: the whole frame a step lighter for that frame (flat, no glow)."""
    if amount <= 0:
        return
    lay = Image.new('RGBA', img.size, (255, 244, 210, int(70 * min(1.0, amount))))
    img.alpha_composite(lay)


if __name__ == '__main__':
    print(__doc__)
