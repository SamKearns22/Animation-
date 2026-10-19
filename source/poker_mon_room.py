#!/usr/bin/env python3
"""Poker Mon, shot 6 (Sam, 19 Oct): the parlour in perspective, the beam swept round the table, everything thrown.

The room is laid out in metres (y up). The table sits in the middle of a panelled parlour: player two and the
Dragonite at its -x end, player one at the +x end with his back to the portrait wall, the woman in red and the man
in the card shirt on the far (+z) side, the old man and the dealer on the near side, onlookers standing behind them.
A camera high in the near corner sweeps along the near wall as the beam fires (Sam: a dynamic upper-diagonal,
sweeping view). The Dragonite hits player one, sweeps its beam down the near side and back up across the far side
(never at its trainer). Whatever the beam passes is thrown away from it: people fly on real arcs, slap into the far
walls, slide down and collapse in a heap; chairs tumble; chips, cards, drinks and the rest fly, bounce off walls and
floor and stay where they land; paper and cloth catch fire. Low parlour light: lamp, sconces and flickering candles.
After a pause, player two pulls in the pot, his hands on it.
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import views as V                # noqa: E402
import figure as F               # noqa: E402
import poker_mon_cast as C       # noqa: E402
from ed import INK, curve        # noqa: E402
from satire_style import rough   # noqa: E402

M_UNIT = V.M_PER_UNIT
RX, RZ, CEIL = 4.4, 4.0, 3.3              # the room: walls at x = +-RX, z = +-RZ
TABLE_H = 0.76
TABLE_A = (1.6, 0.95)                     # the oval's half-length (x) and half-width (z)
NECK_SEATED = (928 - V.SEAT_DROP) * M_UNIT
NECK_STANDING = 928 * M_UNIT
SEAT_Y = 0.40
G = 9.8
WALL = (196, 170, 124)
WALL_D = (168, 140, 98)
GOLD = (196, 150, 60)
GOLD_D = (140, 102, 38)
CARPET = (110, 28, 38)
CARPET_D = (84, 20, 30)
WOOD = (92, 52, 30)
WOOD_D = (62, 34, 20)
FELT = (34, 112, 72)
RAIL = (64, 38, 28)
LINE_Y = (226, 196, 70)
ARMCHAIR = (232, 216, 180)
ARMCHAIR_D = (196, 178, 140)
DRAPE = (120, 22, 40)
DRAPE_D = (88, 14, 30)

# Who sits or stands where: (x, z, facing (dx, dz)). Seated people sit in armchairs (3D, below).
SEATED = {
    'P2': (-1.82, 0.0, (1.0, -0.15)),
    'P1': (1.95, 0.0, (-1.0, 0.0)),
    'LADY': (-0.8, 1.4, (0.0, -1.0)),
    'CARDS': (0.8, 1.4, (0.0, -1.0)),
    'OLD': (-0.55, -1.4, (0.0, 1.0)),
}
STANDING = {
    'DEALER': (0.0, 1.55, (0.0, -1.0)),
    'HUSBAND': (-1.0, 2.2, (0.2, -1.0)),
    'BEAU': (1.55, 2.15, (-0.5, -1.0)),
    'WIFE': (-1.15, -1.75, (0.4, 1.0)),
    'ESCORT': (2.55, -0.6, (-1.0, 0.35)),
    'GUARD1': (3.7, 3.1, (-1.0, -1.0)),
    'GUARD2': (3.7, -3.0, (-1.0, 1.0)),
}
DRAGON = (-2.15, 1.0, (1.0, -0.3))
POT = (-1.2, 0.05)                        # the pot, in front of player two
DRAPES = [('x', 1.2, 2.6), ('z', 0.6, 2.0)]   # cloth: on the +x wall from z 1.2 to 2.6, on the +z wall from x 0.6
PAINTING = ('z', -1.35, 0.05, 1.45, 2.5)      # the landscape on the far wall: canvas, it burns too
FIRE_KINDS = {'card', 'napkin', 'pad'}


# ------------------------------------------------------------------------------------------------ the camera
def _norm(v):
    n = math.sqrt(sum(c * c for c in v)) or 1.0
    return tuple(c / n for c in v)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def _mul(a, k):
    return tuple(x * k for x in a)


class Cam3:
    """A perspective camera inside the room; project() gives the frame point (px) and pixels per metre there;
    poly() draws a 3D polygon clipped at the near plane (so walls beside the camera draw correctly)."""
    NEAR = 0.15

    def __init__(self, pos, at, focal=1650.0, shake=(0.0, 0.0)):
        self.pos, self.focal, self.shake = pos, focal, shake
        self.f = _norm(_sub(at, pos))
        self.r = _norm(_cross(self.f, (0.0, 1.0, 0.0)))
        self.u = _cross(self.r, self.f)

    def depth(self, p):
        return _dot(_sub(p, self.pos), self.f)

    def project(self, p):
        d = _sub(p, self.pos)
        z = max(self.NEAR, _dot(d, self.f))
        k = self.focal / z
        return (540 + _dot(d, self.r) * k + self.shake[0], 960 - _dot(d, self.u) * k + self.shake[1]), k

    def clip(self, pts):
        out = []
        n = len(pts)
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]
            da, db = self.depth(a) - self.NEAR, self.depth(b) - self.NEAR
            if da >= 0:
                out.append(a)
            if (da >= 0) != (db >= 0):
                u = da / (da - db)
                out.append(_add(a, _mul(_sub(b, a), u)))
        return [self.project(q)[0] for q in out]

    def poly(self, pen, pts, fill, line=INK, lw=2.4):
        q = self.clip(pts)
        if len(q) >= 3:
            pen.poly(q, fill, line, lw)

    def line(self, pen, pts, col, lw):
        for a, b in zip(pts, pts[1:]):
            q = self.clip([a, b, b])
            if len(q) >= 2:
                pen.line(q[:2], col, lw)

    def yaw_of(self, p, facing):
        """The drawn view for someone at p facing `facing` (dx, dz): 0 facing us, +90 facing right of frame."""
        fx, fz = _norm((facing[0], facing[1]))
        to_cam = _norm((self.pos[0] - p[0], self.pos[2] - p[2]))
        right = _norm((self.r[0], self.r[2]))
        return math.degrees(math.atan2(fx * right[0] + fz * right[1], fx * to_cam[0] + fz * to_cam[1]))


FLAT = B.Cam(1.0, 540, 960)


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


# ------------------------------------------------------------------------------------------------ the film's clock
class Clock:
    """The film's times, handed in by poker_mon (FIRE, IMPACT, BEAM_END, PULL...)."""
    FIRE = 12.7
    IMPACT = 12.78
    BEAM_END = (14.35, 14.6)
    PAUSE = (14.9, 16.2)          # everything settles; nobody moves for a beat (Sam: a pause before the chips)
    REACH = (16.2, 16.65)         # player two's hands go out to the pot
    PULL = (16.65, 17.6)          # he draws it in, his hands on it
    RELEASE = (17.6, 18.0)
    CHARGE0 = 8.9


def sweep_cam(t):
    """High in the near-right corner (behind player one's shoulder, the Dragonite and player two facing us across
    the room), sweeping along the near wall to its middle as the beam fires; a slow drift while things fly; then an
    eased push in on player two and the pot."""
    a = ease((t - 12.45) / 1.5)
    pos = (3.3 - 3.1 * a, 3.0 - 0.05 * a, -3.55 - 0.2 * a)
    look = (-0.15 - 0.75 * a, 1.2, 0.3 + 0.25 * a)
    b = ease((t - 15.2) / 1.2)
    pos = tuple(p0 + (p1 - p0) * b for p0, p1 in zip(pos, (0.1, 2.45, -1.95)))
    look = tuple(l0 + (l1 - l0) * b for l0, l1 in zip(look, (-1.45, 1.05, 0.15)))
    k = max(0.0, 1 - (t - Clock.IMPACT) / 0.45) if t >= Clock.IMPACT else 0.0
    return Cam3(pos, look, shake=(14 * k * math.sin(t * 90), 10 * k * math.cos(t * 77)))


# ------------------------------------------------------------------------------------------------ the beam
def mouth_world(dstate):
    """The Dragonite's mouth: its head height, a little forward (higher while it rears back)."""
    x, z, f = DRAGON
    f = _norm(f)
    back = max(0.0, -dstate['head']) / 34.0
    return (x + f[0] * 0.3 * (1 - back), 1.74 + 0.22 * back, z + f[1] * 0.3 * (1 - back))


# The sweep: degrees from the Dragonite's mouth (0 = +x, + toward +z). It fires at player one, sweeps down the near
# side, then back up across the far side; never round to player two (about -96).
SWEEP = [(12.70, -15.0), (12.86, -15.0), (13.4, -70.0), (13.5, -70.0), (14.3, 60.0), (14.6, 60.0)]


def beam_angle(t):
    if t <= SWEEP[0][0]:
        return SWEEP[0][1]
    for (t0, a0), (t1, a1) in zip(SWEEP, SWEEP[1:]):
        if t < t1:
            u = (t - t0) / (t1 - t0)
            return a0 + (a1 - a0) * (u * u * (3 - 2 * u))
    return SWEEP[-1][1]


def beam_ray(t, dstate_fire):
    """(start, unit direction) of the beam at t: aimed down so it crosses player one's chest at his distance."""
    m = mouth_world(dstate_fire)
    a = math.radians(beam_angle(t))
    drop = (m[1] - 1.0) / 3.95
    d = _norm((math.cos(a), -drop, math.sin(a)))
    return m, d


def beam_end(m, d):
    """Where the beam meets a wall or the floor."""
    best = 30.0
    for axis, lim in ((0, RX), (0, -RX), (2, RZ), (2, -RZ)):
        if abs(d[axis]) > 1e-6:
            s = (lim - m[axis]) / d[axis]
            if s > 0:
                best = min(best, s)
    if d[1] < 0:
        best = min(best, m[1] / -d[1])
    return _add(m, _mul(d, best)), best


def dist_to_ray(p, m, d, length):
    v = _sub(p, m)
    s = max(0.0, min(length, _dot(v, d)))
    return math.sqrt(_dot(_sub(v, _mul(d, s)), _sub(v, _mul(d, s)))), s


# ------------------------------------------------------------------------------------------------ the physics
class Body:
    """Something thrown: launched at t0 from p0 with velocity v0; bounces off the walls, ceiling and floor
    (restitution e, friction on the floor), comes to rest and stays. Steps at 240 Hz, cached."""
    def __init__(self, p0, v0, t0, r=0.05, e=0.35, wall_e=None, spin=0.0, grip=0.6):
        self.t0, self.r, self.e, self.wall_e = t0, r, e, (e if wall_e is None else wall_e)
        self.grip = grip                                 # how much speed along the wall survives a hit
        self.spin = spin
        self.track = []                                  # (t, pos, angle, event)
        self.wall_t = self.floor_t = self.wall = None
        self._run(p0, v0)

    def _run(self, p, v):
        dt = 1 / 240
        t, ang, w = self.t0, 0.0, self.spin
        p, v = list(p), list(v)
        rest = False
        for _ in range(int(6.5 / dt)):
            if not rest:
                v[1] -= G * dt
                for i in range(3):
                    p[i] += v[i] * dt
                ang += w * dt
                for axis, lim in ((0, RX), (2, RZ)):
                    for sg in (-1, 1):
                        if sg * p[axis] > lim - self.r:
                            p[axis] = sg * (lim - self.r)
                            if sg * v[axis] > 0:
                                v[axis] = -v[axis] * self.wall_e
                                v[2 - axis] *= self.grip
                                v[1] *= 0.5
                                w *= 0.4
                                if self.wall_t is None:
                                    self.wall_t, self.wall = t, (axis, sg)
                if p[1] > CEIL - self.r and v[1] > 0:
                    p[1], v[1] = CEIL - self.r, -v[1] * 0.3
                if p[1] < self.r:
                    p[1] = self.r
                    if self.floor_t is None:
                        self.floor_t = t
                    if v[1] < 0:
                        v[1] = -v[1] * self.e
                    v[0] *= 0.82
                    v[2] *= 0.82
                    w *= 0.7
                    if abs(v[1]) < 0.4 and math.hypot(v[0], v[2]) < 0.25:
                        rest = True
                        v = [0.0, 0.0, 0.0]
            self.track.append((t, tuple(p), ang))
            t += dt

    def at(self, t):
        if t <= self.t0:
            return self.track[0][1], 0.0
        i = min(len(self.track) - 1, int((t - self.t0) * 240))
        return self.track[i][1], self.track[i][2]


# ------------------------------------------------------------------------------------------------ the room
def floor_and_walls(img, cam, t):
    p = B.Pen(img, FLAT)
    cam.poly(p, [(-RX, 0, -RZ), (RX, 0, -RZ), (RX, 0, RZ), (-RX, 0, RZ)], CARPET, None)
    for k in np.arange(-RZ - 4, RZ, 0.6):                       # the carpet's pattern: a lattice of fine lines
        cam.line(p, [(-RX, 0.001, k), (RX, 0.001, k + 3.2)], CARPET_D, 2.6)
        cam.line(p, [(-RX, 0.001, k + 3.2), (RX, 0.001, k)], CARPET_D, 2.6)
    for wall in ('+x', '+z', '-x', '-z'):
        wall_face(img, cam, p, wall)


def _wall_pts(wall, a0, a1, y0, y1, inset=0.0):
    """A rectangle on a wall: a runs along it, y up it."""
    if wall == '+x':
        return [(RX - inset, y0, a0), (RX - inset, y0, a1), (RX - inset, y1, a1), (RX - inset, y1, a0)]
    if wall == '-x':
        return [(-RX + inset, y0, a0), (-RX + inset, y0, a1), (-RX + inset, y1, a1), (-RX + inset, y1, a0)]
    if wall == '+z':
        return [(a0, y0, RZ - inset), (a1, y0, RZ - inset), (a1, y1, RZ - inset), (a0, y1, RZ - inset)]
    return [(a0, y0, -RZ + inset), (a1, y0, -RZ + inset), (a1, y1, -RZ + inset), (a0, y1, -RZ + inset)]


def wall_face(img, cam, p, wall):
    """A panelled parlour wall: a dark wood dado below a gilt rail, framed silk panels above, a moulded cornice."""
    span = RZ if wall in ('+x', '-x') else RX
    cam.poly(p, _wall_pts(wall, -span, span, 0, CEIL), WALL, INK, 2.6)
    cam.poly(p, _wall_pts(wall, -span, span, 0, 0.95, 0.002), WOOD, INK, 2.2)          # the dado
    cam.poly(p, _wall_pts(wall, -span, span, 0.92, 1.0, 0.004), GOLD, INK, 1.8)        # the rail
    cam.poly(p, _wall_pts(wall, -span, span, CEIL - 0.22, CEIL, 0.004), WALL_D, GOLD, 2.0)   # the cornice
    n = int(span * 2 / 1.1)
    w = span * 2 / n
    for i in range(n):
        a0 = -span + i * w
        cam.poly(p, _wall_pts(wall, a0 + 0.1, a0 + w - 0.1, 1.12, CEIL - 0.36, 0.003), WALL_D, GOLD, 2.2)
        cam.poly(p, _wall_pts(wall, a0 + 0.12, a0 + w - 0.12, 0.12, 0.8, 0.004), WOOD_D, GOLD_D, 1.6)


def decor(img, cam, t, ign):
    """Minimal old-world pieces: a gilt-framed portrait and a landscape, velvet drapes at a tall window, a
    sideboard with a decanter and a candelabra, a marble bust on a plinth, brass sconces with candles."""
    p = B.Pen(img, FLAT)
    # the portrait over player one (+x wall) and a landscape on the far wall (+z)
    for wall, a0, a1, y0, y1, kind in (('+x', -2.2, -0.8, 1.3, 2.75, 'portrait'), ('+z',) + PAINTING[1:] + ('land',)):
        cam.poly(p, _wall_pts(wall, a0 - 0.08, a1 + 0.08, y0 - 0.08, y1 + 0.08, 0.01), GOLD, INK, 2.4)
        cam.poly(p, _wall_pts(wall, a0, a1, y0, y1, 0.012), (60, 44, 34) if kind == 'portrait' else (120, 150, 160),
                 INK, 1.8)
        if kind == 'portrait':                                  # a dark old master: a figure in a ruff
            mid = (a0 + a1) / 2
            cam.poly(p, _wall_pts(wall, mid - 0.32, mid + 0.32, y0, y0 + 0.55, 0.014), (30, 26, 28), None)
            cam.poly(p, _wall_pts(wall, mid - 0.2, mid + 0.2, y0 + 0.5, y0 + 0.64, 0.015), (226, 220, 206), INK, 1.2)
            cam.poly(p, _wall_pts(wall, mid - 0.15, mid + 0.15, y0 + 0.62, y0 + 1.05, 0.015), (206, 168, 140), INK, 1.4)
        else:                                                   # hills, a lake, a pale sky
            cam.poly(p, _wall_pts(wall, a0, a1, y0, y0 + 0.45, 0.014), (70, 110, 70), None)
            cam.poly(p, _wall_pts(wall, a0 + 0.3, a1 - 0.2, y0 + 0.2, y0 + 0.35, 0.015), (90, 130, 170), None)
    # the tall window with velvet drapes (cloth: they catch fire when the beam reaches them)
    for wall, a0, a1 in (('+' + w, a0_, a1_) for w, a0_, a1_ in DRAPES):
        cam.poly(p, _wall_pts(wall, a0 + 0.25, a1 - 0.25, 0.4, 2.85, 0.01), (30, 34, 56), INK, 2.2)   # night outside
        cam.poly(p, _wall_pts(wall, (a0 + a1) / 2 - 0.02, (a0 + a1) / 2 + 0.02, 0.4, 2.85, 0.012), WOOD, None)
        for d0, d1 in ((a0, a0 + 0.42), (a1 - 0.42, a1)):
            cam.poly(p, _wall_pts(wall, d0, d1, 0.0, 3.0, 0.02), DRAPE, INK, 2.2)
            for k in range(3):
                x = d0 + (d1 - d0) * (k + 1) / 4
                cam.line(p, [_wall_pts(wall, x, x, 0.05, 2.9, 0.025)[0], _wall_pts(wall, x, x, 0.05, 2.9, 0.025)[3]],
                         DRAPE_D, 2.4)
        cam.poly(p, _wall_pts(wall, a0 - 0.1, a1 + 0.1, 2.92, 3.08, 0.03), GOLD, INK, 2.0)          # the pelmet
    # the sideboard on the -x wall, behind player two: dark wood, a decanter, a candelabra
    sx0, sx1 = -RX, -RX + 0.5
    box(img, cam, p, (sx0, 0.0, -0.4), (sx1, 0.9, 1.4), WOOD, WOOD_D)
    # the bust on its plinth in the far corner
    box(img, cam, p, (RX - 0.75, 0.0, RZ - 0.75), (RX - 0.25, 1.05, RZ - 0.25), (220, 214, 204), (190, 184, 176))
    (X, Y), k = cam.project((RX - 0.5, 1.05, RZ - 0.5))
    p.poly(rough([(X - 0.16 * k, Y), (X + 0.16 * k, Y), (X + 0.12 * k, Y - 0.16 * k), (X - 0.12 * k, Y - 0.16 * k)], 2, 3),
           (236, 232, 224), INK, 2.0)
    p.ell(X, Y - 0.27 * k, 0.1 * k, 0.12 * k, (236, 232, 224), INK, 2.0)


def sideboard_props(img, cam, t):
    """The decanter and the candelabra on the sideboard (drawn after the light, the flames self-lit)."""
    p = B.Pen(img, FLAT)
    (X, Y), k = cam.project((-RX + 0.25, 0.9, 0.0))
    p.poly(rough([(X - 0.06 * k, Y), (X + 0.06 * k, Y), (X + 0.07 * k, Y - 0.14 * k), (X + 0.02 * k, Y - 0.2 * k),
                  (X + 0.02 * k, Y - 0.27 * k), (X - 0.02 * k, Y - 0.27 * k), (X - 0.02 * k, Y - 0.2 * k),
                  (X - 0.07 * k, Y - 0.14 * k)], 1, 2), (150, 70, 36), INK, 1.6)
    candelabra(p, cam, (-RX + 0.25, 0.9, 0.9), t, 31)


def candelabra(p, cam, base, t, seed, lit=True, ang=0.0, flying=False):
    (X, Y), k = cam.project(base)
    h = 0.34 * k
    p.line([(X, Y), (X, Y - h * 0.7)], GOLD, max(2, 0.025 * k))
    p.poly([(X - 0.06 * k, Y), (X + 0.06 * k, Y), (X + 0.03 * k, Y - 0.03 * k), (X - 0.03 * k, Y - 0.03 * k)], GOLD, INK, 1.4)
    p.line(curve([(X - 0.13 * k, Y - h * 0.62), (X, Y - h * 0.72), (X + 0.13 * k, Y - h * 0.62)], 3), GOLD,
           max(2, 0.02 * k))
    for i, dx in enumerate((-0.13, 0.0, 0.13)):
        C.candle(p, X + dx * k, Y - h * (0.62 if dx else 0.74), 0.14 * k, t, seed + i, lit, w=0.012 * k)


def box(img, cam, p, a, b, col, col_d):
    """An axis-aligned box from corner a to corner b: its three faces toward the camera."""
    x0, y0, z0 = a
    x1, y1, z1 = b
    faces = [([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], (0, 1, 0), col),
             ([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], (0, 0, -1), col_d),
             ([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], (0, 0, 1), col_d),
             ([(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], (-1, 0, 0), col_d),
             ([(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], (1, 0, 0), col_d)]
    for pts, n, c in faces:
        ctr = tuple(sum(q[i] for q in pts) / 4 for i in range(3))
        if _dot(n, _sub(cam.pos, ctr)) > 0:
            cam.poly(p, pts, c, INK, 2.0)


# ------------------------------------------------------------------------------------------------ the table
def oval(y, r=1.0, n=96):
    return [(TABLE_A[0] * r * math.cos(a), y, TABLE_A[1] * r * math.sin(a)) for a in
            np.linspace(0, 2 * math.pi, n, endpoint=False)]


def table(img, cam):
    p = B.Pen(img, FLAT)
    top, low = oval(TABLE_H), oval(TABLE_H - 0.12)
    tp = [cam.project(q)[0] for q in top]
    lp = [cam.project(q)[0] for q in low]
    (bx, by), bk = cam.project((0, 0, 0))
    p.poly([cam.project(q)[0] for q in oval(0.0, 0.35)], WOOD_D, INK, 2.0)                # the pedestal's foot
    p.poly([cam.project((-0.18, 0, 0))[0], cam.project((0.18, 0, 0))[0], cam.project((0.18, TABLE_H - 0.1, 0))[0],
            cam.project((-0.18, TABLE_H - 0.1, 0))[0]], WOOD, INK, 2.0)
    for i in range(len(tp)):
        j = (i + 1) % len(tp)
        p.poly([tp[i], tp[j], lp[j], lp[i]], RAIL, None)
    p.poly(lp, None, INK, 2.2)
    p.poly(tp, RAIL, INK, 2.6)
    p.poly([cam.project(q)[0] for q in oval(TABLE_H + 0.005, 0.86)], FELT, INK, 2.2)
    ring = [cam.project(q)[0] for q in oval(TABLE_H + 0.006, 0.64)]
    p.line(ring + [ring[0]], LINE_Y, 3)


# ------------------------------------------------------------------------------------------------ armchairs
def chair_faces(pos, facing, rot=None):
    """A padded armchair (cream, wooden legs) at pos (x, 0, z) facing `facing`, optionally tumbled by rot (axis,
    angle, pivot): its faces as (points, normal, colour)."""
    fx, fz = _norm(facing)
    rx, rz = fz, -fx                                     # the chair's own sideways axis

    def W(lx, ly, lz):                                   # chair coords (x across, y up, z forward) to world
        return (pos[0] + lx * rx + lz * fx, ly, pos[2] + lx * rz + lz * fz)
    boxes = [((-0.3, 0.28, -0.27), (0.3, SEAT_Y, 0.27), ARMCHAIR),
             ((-0.3, SEAT_Y, -0.29), (0.3, 1.0, -0.17), ARMCHAIR),
             ((-0.36, SEAT_Y, -0.27), (-0.28, 0.6, 0.25), ARMCHAIR_D),
             ((0.28, SEAT_Y, -0.27), (0.36, 0.6, 0.25), ARMCHAIR_D)]
    for lx in (-0.25, 0.22):
        for lz in (-0.22, 0.19):
            boxes.append(((lx, 0.0, lz), (lx + 0.04, 0.28, lz + 0.04), WOOD))
    out = []
    for (x0, y0, z0), (x1, y1, z1), col in boxes:
        corners = {}
        for i, x in enumerate((x0, x1)):
            for j, y in enumerate((y0, y1)):
                for k, z in enumerate((z0, z1)):
                    corners[(i, j, k)] = W(x, y, z)
        quads = [((0, 1, 0), [(0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)]), ((0, -1, 0), [(0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0)]),
                 ((-1, 0, 0), [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)]), ((1, 0, 0), [(1, 0, 0), (1, 0, 1), (1, 1, 1), (1, 1, 0)]),
                 ((0, 0, -1), [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]), ((0, 0, 1), [(0, 0, 1), (0, 1, 1), (1, 1, 1), (1, 0, 1)])]
        for n, idx in quads:
            pts = [corners[c] for c in idx]
            if rot:
                pts = [rotate(q, *rot) for q in pts]
            out.append((pts, col))
    return out


def rotate(p, axis, ang, pivot):
    """Rodrigues: p turned by ang (radians) about the axis through pivot."""
    k = _norm(axis)
    v = _sub(p, pivot)
    c, s = math.cos(ang), math.sin(ang)
    r = _add(_add(_mul(v, c), _mul(_cross(k, v), s)), _mul(k, _dot(k, v) * (1 - c)))
    return _add(r, pivot)


def draw_faces(img, cam, faces, near_than=None, far_than=None):
    """A chair's faces, far to near (painter's order); split at a depth so a person sits between them."""
    p = B.Pen(img, FLAT)
    vis = []
    for pts, col in faces:
        ctr = tuple(sum(q[i] for q in pts) / len(pts) for i in range(3))
        dep = cam.depth(ctr)
        if near_than is not None and dep >= near_than:
            continue
        if far_than is not None and dep < far_than:
            continue
        vis.append((dep, pts, col))
    for dep, pts, col in sorted(vis, key=lambda v: -v[0]):
        cam.poly(p, pts, col, INK, 1.8)


# ------------------------------------------------------------------------------------------------ table things
def _things():
    """Everything on the table before the blast: (kind, (x, z), extra). Each player's chips, cards and drink; the
    old man's ashtray and cigar and his score pad; the dealer's shoe and button; napkins; the candelabra; the pot."""
    T = []
    rng = np.random.default_rng(5)

    def chips(x, z, n, kind):
        for i in range(n):
            T.append(('chip', (x + rng.uniform(-0.006, 0.006), z + rng.uniform(-0.006, 0.006)), dict(kind=kind, level=i)))
    for i, suit in enumerate('SCDH'):                                   # player one's four Queens, face up
        T.append(('card', (1.32, -0.17 + i * 0.11), dict(face=('Q', suit), ang=80 + (i - 1.5) * 6)))
    chips(1.25, 0.5, 7, 'ultra'), chips(1.3, 0.62, 5, 'poke')
    T.append(('tumbler', (1.42, -0.55), dict(drink=(196, 120, 40))))
    T.append(('napkin', (1.2, -0.42), {}))
    for who, (x, z), drink in (('LADY', (-0.8, 0.95), 'flute'), ('CARDS', (0.8, 0.95), 'martini'),
                               ('OLD', (-0.55, -0.95), 'tumbler')):
        sg = 1 if z > 0 else -1
        for k in range(2):
            T.append(('card', (x - 0.05 + k * 0.06, z), dict(face=None, ang=rng.uniform(-14, 14))))
        chips(x - 0.3, z - sg * 0.06, 6, 'great'), chips(x - 0.38, z + sg * 0.02, 4, 'poke')
        T.append((drink, (x + 0.3, z - sg * 0.1), {}))
        T.append(('napkin', (x + 0.18, z + sg * 0.08), {}))
    T.append(('ashtray', (-0.2, -0.92), {}))
    T.append(('pad', (-0.92, -0.62), {}))
    T.append(('shoe', (0.0, 0.78), {}))
    T.append(('button', (0.35, 0.62), {}))
    T.append(('candelabra', (0.25, 0.0), {}))
    for k in range(3):                                                  # player two's own hand, face down
        T.append(('card', (-1.33, -0.32 + k * 0.05), dict(face=None, ang=90 + k * 8)))
    T.append(('tumbler', (-1.3, -0.5), dict(drink=(150, 70, 30))))
    return T


THINGS = _things()
POT_STACKS = [(dx, dz, n, kind) for dx, dz, n, kind in
              ((-0.08, 0.0, 9, 'ultra'), (0.0, 0.05, 12, 'poke'), (0.08, 0.0, 7, 'great'), (-0.04, -0.08, 5, 'master'),
               (0.05, -0.08, 10, 'poke'), (0.12, 0.08, 8, 'ultra'), (-0.12, 0.08, 6, 'great'), (0.0, 0.14, 11, 'poke'),
               (0.13, -0.05, 9, 'poke'), (-0.11, -0.03, 7, 'great'), (0.03, -0.15, 6, 'ultra'), (-0.06, 0.15, 4, 'master'))]
_CACHE = {}


def blast_hits(dfire):
    """When the sweeping beam's blast reaches each thing and each person (the first moment it passes close), with the
    sweep's direction then. Cached."""
    if 'hits' in _CACHE:
        return _CACHE['hits']
    pts = {}
    for i, (kind, (x, z), ex) in enumerate(THINGS):
        pts[('T', i)] = ((x, TABLE_H + 0.03, z), 0.75)
    for who, (x, z, f) in SEATED.items():
        if who != 'P2':
            pts[('P', who)] = ((x, 0.95, z), 0.7)
    for who, (x, z, f) in STANDING.items():
        pts[('P', who)] = ((x, 1.25, z), 0.7)
    out = {}
    t = Clock.FIRE
    while t < Clock.BEAM_END[0]:
        m, d = beam_ray(t, dfire)
        end, length = beam_end(m, d)
        sweep = beam_angle(t + 0.01) - beam_angle(t)
        for key, (p, r) in pts.items():
            if key not in out and t >= Clock.IMPACT - 0.02:
                dd, s = dist_to_ray(p, m, d, length)
                if dd < r and s > 0.3:
                    out[key] = (t, m, 1 if sweep >= 0 else -1)
        t += 1 / 240
    _CACHE['hits'] = out
    return out


def launch(key, p0, hit, speed, up, spin, r, e, wall_e=None, seed=0, grip=0.6):
    """A body thrown from p0: away from the beam's mouth, dragged a little along the sweep, up, spinning."""
    t, m, sg = hit
    rng = np.random.default_rng(seed)
    along = _norm((p0[0] - m[0], 0.0, p0[2] - m[2]))
    radial = _norm((p0[0] / TABLE_A[0], 0.0, p0[2] / TABLE_A[1]))      # the blast spreads out from the table
    away = _norm(_add(_mul(along, 0.55), _mul(radial, 0.8)))
    side = (-away[2] * sg, 0.0, away[0] * sg)
    v = _add(_add(_mul(away, speed), _mul(side, speed * 0.25 * rng.uniform(0.5, 1.2))), (0.0, up, 0.0))
    return Body(p0, v, t, r=r, e=e, wall_e=wall_e, spin=spin, grip=grip)


def thing_body(i, dfire):
    key = ('T', i)
    if key in _CACHE:
        return _CACHE[key]
    kind, (x, z), ex = THINGS[i]
    hit = blast_hits(dfire).get(key)
    b = None
    if hit:
        rng = np.random.default_rng(100 + i)
        y = TABLE_H + 0.01 + 0.004 * ex.get('level', 0)
        heavy = kind in ('shoe', 'candelabra', 'ashtray', 'tumbler')
        b = launch(key, (x, y, z), hit, rng.uniform(2.5, 5.0) if heavy else rng.uniform(3.5, 7.5),
                   rng.uniform(1.5, 4.5), rng.uniform(-900, 900), 0.03, 0.35 if not heavy else 0.2, seed=i)
    _CACHE[key] = b
    return b


def person_body(who, dfire):
    key = ('P', who)
    if key in _CACHE:
        return _CACHE[key]
    hit = blast_hits(dfire).get(key)
    b = None
    if hit:
        x, z, f = (SEATED.get(who) or STANDING[who])
        y = NECK_SEATED if who in SEATED else NECK_STANDING
        rng = np.random.default_rng(sum(map(ord, who)))
        b = launch(key, (x, y, z), hit, rng.uniform(6.0, 7.5), rng.uniform(2.6, 3.6),
                   rng.choice([-1, 1]) * rng.uniform(420, 820), 0.3, 0.05, wall_e=0.06, seed=sum(map(ord, who)),
                   grip=0.08)
    _CACHE[key] = b
    return b


def chair_body(who, dfire):
    key = ('C', who)
    if key in _CACHE:
        return _CACHE[key]
    hit = blast_hits(dfire).get(('P', who))
    b = None
    if hit:
        x, z, f = SEATED[who]
        rng = np.random.default_rng(7 + sum(map(ord, who)))
        b = launch(key, (x, 0.5, z), (hit[0] + 0.03, hit[1], hit[2]), rng.uniform(3.5, 5.0), rng.uniform(1.8, 2.8),
                   rng.uniform(300, 600), 0.35, 0.25, wall_e=0.3, seed=7 + sum(map(ord, who)))
        b.axis = _norm((rng.uniform(-1, 1), rng.uniform(-0.3, 0.3), rng.uniform(-1, 1)))
    _CACHE[key] = b
    return b


def drape_fire_times(dfire):
    """When the beam's end first sweeps across each drape (cloth: it catches fire)."""
    if 'drapes' in _CACHE:
        return _CACHE['drapes']
    out = {}
    t = Clock.FIRE
    while t < Clock.BEAM_END[0]:
        m, d = beam_ray(t, dfire)
        end, _ = beam_end(m, d)
        for i, (wall, a0, a1) in enumerate(DRAPES):
            if i in out:
                continue
            if wall == 'x' and abs(end[0] - RX) < 0.05 and a0 <= end[2] <= a1:
                out[i] = (t, end)
            if wall == 'z' and abs(end[2] - RZ) < 0.05 and a0 <= end[0] <= a1:
                out[i] = (t, end)
        t += 1 / 240
        w, a0, a1, y0, y1 = PAINTING
        if 'paint' not in out and abs(end[2] - RZ) < 0.05 and a0 <= end[0] <= a1:
            out['paint'] = (t, end)
    _CACHE['drapes'] = out
    return out


def scorch(img, cam, t, dfire):
    """The beam's burnt track along the walls where its end has passed: stays once made."""
    p = B.Pen(img, FLAT)
    pts = []
    tt = Clock.FIRE + 0.05
    while tt < min(t, Clock.BEAM_END[0]):
        m, d = beam_ray(tt, dfire)
        end, _ = beam_end(m, d)
        pts.append(end)
        tt += 1 / 60
    if len(pts) < 2:
        return
    for (a, b) in zip(pts, pts[1:]):
        if (abs(a[0]) > RX - 0.06 and abs(b[0]) > RX - 0.06) or (abs(a[2]) > RZ - 0.06 and abs(b[2]) > RZ - 0.06):
            (A, ka), (Bp, kb) = cam.project(a), cam.project(b)
            p.line([A, Bp], (176, 84, 34), max(3, 0.16 * (ka + kb) / 2))
            p.line([A, Bp], (24, 18, 16), max(2, 0.1 * (ka + kb) / 2))


# ------------------------------------------------------------------------------------------------ drawing things
def draw_thing(img, cam, kind, ex, pos, ang, t, burning, seed, flying):
    """One thing at pos (world), turned by ang (degrees) about the vertical while flat, tumbling while it flies."""
    p = B.Pen(img, FLAT)
    (X, Y), k = cam.project(pos)
    tilt = max(0.3, min(0.95, _dot(cam.f, (0, -1, 0)) + 0.15))
    if kind == 'chip':
        w = 0.039 * k
        sq = tilt if not flying else 0.3 + 0.7 * abs(math.cos(math.radians(ang * 0.7)))
        C.place_image(img, FLAT, C.chip_face(ex['kind']), C.card_quad(X, Y, w, ang, sq * C.CW / C.CH))
    elif kind == 'card':
        src = C.card_face(*ex['face']) if ex.get('face') else C.card_back()
        sq = tilt if not flying else 0.25 + 0.75 * abs(math.cos(math.radians(ang * 0.6)))
        C.place_image(img, FLAT, src, C.card_quad(X, Y, 0.063 * k, ex.get('ang', 0) + ang, sq))
    elif kind in ('tumbler', 'flute', 'martini'):
        h = {'tumbler': 0.09, 'flute': 0.22, 'martini': 0.17}[kind] * k
        if flying:
            lay = Image.new('RGBA', (int(h * 3 * B.SS) + 4, int(h * 3 * B.SS) + 4), (0, 0, 0, 0))
            q = B.Pen(lay, B.Cam(1.0, 540 - lay.width / B.SS / 2, 960 - lay.height / B.SS / 2))
            C.glass(q, lay.width / B.SS / 2, lay.height / B.SS / 2 + h / 2, h, kind, ex.get('drink', (196, 120, 40)))
            lay = lay.rotate(ang, Image.BILINEAR)
            img.alpha_composite(lay, (max(0, int(X * B.SS - lay.width / 2)), max(0, int(Y * B.SS - lay.height / 2)))) \
                if X * B.SS - lay.width / 2 >= 0 and Y * B.SS - lay.height / 2 >= 0 else None
        else:
            C.glass(p, X, Y, h, kind, ex.get('drink', (196, 120, 40)))
    elif kind == 'napkin':
        w = 0.14 * k
        p.poly(rough(C.card_quad(X, Y, w, ang + 30, tilt * 0.8), 2, seed), (248, 246, 240), INK, 1.4)
    elif kind == 'pad':
        q = C.card_quad(X, Y, 0.1 * k, ang, tilt * 1.3)
        p.poly(q, (250, 248, 232), INK, 1.4)
        for i in range(4):
            u = 0.25 + 0.15 * i
            p.line([(q[0][0] + (q[3][0] - q[0][0]) * u + 4, q[0][1] + (q[3][1] - q[0][1]) * u),
                    (q[1][0] + (q[2][0] - q[1][0]) * u - 4, q[1][1] + (q[2][1] - q[1][1]) * u)], (120, 140, 190), 1.2)
    elif kind == 'ashtray':
        p.ell(X, Y, 0.06 * k, 0.06 * k * tilt, (170, 176, 182), INK, 1.4)
        p.line([(X - 0.02 * k, Y), (X + 0.08 * k, Y - 0.01 * k)], (120, 80, 50), max(2, 0.018 * k))     # the cigar
        p.ell(X + 0.08 * k, Y - 0.01 * k, 0.008 * k, 0.008 * k, (250, 120, 40), None)
    elif kind == 'shoe':
        q = C.card_quad(X, Y - 0.05 * k, 0.12 * k, ang, 1.3)
        p.poly(q, (40, 30, 26), INK, 1.6)
        p.poly(C.card_quad(X, Y - 0.08 * k, 0.07 * k, ang, 0.9), C.YELLOW, INK, 1.0)
    elif kind == 'button':
        p.ell(X, Y, 0.03 * k, 0.03 * k * tilt, (250, 250, 246), INK, 1.4)
    elif kind == 'candelabra':
        if flying:
            lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            candelabra(B.Pen(lay, FLAT), cam, pos, t, seed, lit=True)
            bb = lay.getbbox()
            if bb:
                piece = lay.crop(bb).rotate(ang, Image.BILINEAR, expand=True)
                img.alpha_composite(piece, (max(0, int((bb[0] + bb[2]) / 2 - piece.width / 2)),
                                            max(0, int((bb[1] + bb[3]) / 2 - piece.height / 2))))
        else:
            candelabra(p, cam, pos, t, seed)
    if burning:
        FIRES.append((X, Y - 0.02 * k, 0.09 * k, seed))


FIRES = []           # flames this frame (drawn after the light, self-lit): (X, Y, height, seed)
LIGHTS = []          # lights this frame: (X, Y, radius px, strength, colour)


def things(img, cam, t, dfire, on_table):
    """Everything that sat on the table: still there (on_table) or thrown (in the room, sorted with the rest)."""
    out = []
    for i, (kind, (x, z), ex) in enumerate(THINGS):
        b = thing_body(i, dfire)
        y = TABLE_H + 0.01 + 0.004 * ex.get('level', 0)
        if b is None or t < b.t0:
            if on_table:
                out.append((cam.depth((x, y, z)), i, (x, y, z), 0.0, False, False))
            continue
        if on_table:
            continue
        pos, ang = b.at(t)
        flying = b.floor_t is None or t < b.floor_t + 0.3
        burning = kind in FIRE_KINDS and (i % 2 == 0 or kind != 'card')
        out.append((cam.depth(pos), i, pos, ang, flying, burning))
    return out


def draw_things(img, cam, t, lst):
    for dep, i, pos, ang, flying, burning in lst:
        kind, _, ex = THINGS[i]
        if kind == 'chip' and not flying and pos[1] > TABLE_H - 0.01:
            pass
        draw_thing(img, cam, kind, ex, pos, ang, t, burning, i, flying)
        if kind == 'candelabra':
            (X, Y), k = cam.project(pos)
            LIGHTS.append((X, Y - 0.4 * k, 0.9 * k, 0.55 * C.flicker(t, 40), (255, 190, 110)))


def pot(img, cam, t, film):
    """The pot in front of player two: still through the blast; after the pause, his hands draw it in."""
    u = ease((t - Clock.PULL[0]) / (Clock.PULL[1] - Clock.PULL[0])) if t >= Clock.PULL[0] else 0.0
    px = POT[0] + (-1.4 - POT[0]) * u
    pz = POT[1] + (0.0 - POT[1]) * u
    for dx, dz, n, kind in POT_STACKS:
        (X, Y), k = cam.project((px + dx, TABLE_H, pz + dz))
        C.chip_stack(img, FLAT, X, Y, 0.0195 * k, n, kind, squash=max(0.35, min(0.8, _dot(cam.f, (0, -1, 0)) + 0.2)),
                     seed=n)
    return (px, pz)


# ------------------------------------------------------------------------------------------------ people
def screen_hand_target(j, side, yaw, mirror, X, Yneck, s, target, zb):
    """The body-frame point (torso units) whose drawing lands on the frame point `target`, `zb` in front: so a hand
    really touches what it holds on screen (views.project inverted for this view)."""
    a = math.radians(V.snap(yaw)[0])
    flip = -1 if mirror else 1
    px = (target[0] - X) / (s * flip)
    py = (target[1] - Yneck) / s
    ca, sa = math.cos(a), math.sin(a)
    if abs(ca) > 0.3:
        x, z = (px - zb * sa) / ca, zb
    else:
        x = j['sh' + side][0]
        z = (px - x * ca) / sa
    y = py - V.ELEV * (-x * sa + z * ca)
    tgt = (x, y, z)
    sh = j['sh' + side]
    d = math.sqrt(sum((u - v) ** 2 for u, v in zip(tgt, sh)))
    lim = (F.UPPER + F.FORE) * 0.97 + F.HAND['palm']
    if d > lim:                                          # out of reach: as far as the arm goes, never stretched
        tgt = tuple(v + (u - v) * lim / d for u, v in zip(tgt, sh))
    return tgt


def heap_pose(sp, u=1.0):
    """Collapsed in a heap at the foot of the wall: sitting on the floor, slumped back, legs out, arms limp, head
    dropped. u 0..1 eases from kneeling (just down the wall) to the heap."""
    j = V.standing(sp)
    j['props'] = [C.dress_up(sp)]
    j['bob'] = 300 + 138 * u
    floor = 928 - j['bob']
    for s, sg in (('L', -1), ('R', 1)):
        j['foot' + s] = (sg * (80 + 50 * u), floor - 30, 150 + 260 * u)
        j['knee_pole' + s] = (0.3 * sg, -1.0, 0.4)
        V.arm_to(j, s, (sg * (170 + 40 * u), min(floor - 50, 470.0), 40.0), 'out', 'palm')
    j['lean'] = 14 * u                                   # folded forward over the legs
    j['head_dy'] = 44 * u
    return j


def people_pose(film, who, t, sp):
    """The pose and face for someone at the table or standing round it before the blast."""
    if who == 'P2':
        sp.update(film.p2_face(t))
        return None
    if who == 'P1':
        sp.update(film.p1_face(film.SHOTS[4][2] - 0.01))
    else:                                                # everyone stares at the Dragonite as it charges
        sp.update(brows='alarm', mouth='agape', look=-0.6, lid=0)
    return None


def seated_joints(film, sp, kind='rest'):
    j = film.seated(sp, kind)
    j['seated'] = False                                  # our own armchair is drawn (3D), not the kit's office chair
    j['bob'] = V.SEAT_DROP
    for sd, sg in (('L', -1), ('R', 1)):
        j['foot' + sd] = (sg * 64, 928 - V.SEAT_DROP - 38, V.THIGH * 0.98)
        j['knee_pole' + sd] = (0.1 * sg, -1.0, 0.7)
    return j


DRAWN = {}           # this frame: who -> (X, Yneck, s, yaw, mirror, j, j2)


def draw_person(img, cam, film, who, t, t_pose=None, hand_on=None):
    """Someone in place (seated in their armchair, or standing), the view from their facing. Returns (X, Y, s)."""
    tp = t if t_pose is None else t_pose
    sp = dict(C.PEOPLE[who], blink=F.blinking(tp, film.BLINKS.get(who, [])), mouth='line', look=0.0)
    if who in SEATED:
        x, z, f = SEATED[who]
        (X, Y), k = cam.project((x, NECK_SEATED, z))
        people_pose(film, who, tp, sp)
        j = seated_joints(film, sp)
        bob = V.SEAT_DROP
    else:
        x, z, f = STANDING[who]
        (X, Y), k = cam.project((x, NECK_STANDING, z))
        people_pose(film, who, tp, sp)
        j = C.pose_standing(sp)
        bob = 0.0
        if who == 'BEAU':                                # a champagne flute in his hand
            V.arm_to(j, 'R', (60.0, 230.0, 160.0), 'down', 'fist')
            j['props'].append(lambda p, j2: C.glass(p, j2['wrR'][0] + 4, j2['wrR'][1] + 6, 120, 'flute'))
    s = k * M_UNIT
    yaw = cam.yaw_of((x, 0, z), f)
    mirror = V.snap(yaw)[1]
    if who == 'P2':
        j = p2_pull_pose(img, cam, film, sp, t, X, Y, s, yaw, mirror)
    if hand_on and who == 'ESCORT' and 'P1' in DRAWN:     # her hand on player one's shoulder: real contact
        X1, Y1, s1, yaw1, m1, j1, j21 = DRAWN['P1']
        sh = j21['shL'] if not m1 else j21['shR']
        tgt = (X1 + s1 * sh[0] * (-1 if m1 else 1), Y1 + s1 * sh[1])
        V.arm_to(j, 'R', screen_hand_target(j, 'R', yaw, mirror, X, Y, s, tgt, 180.0), 'down', 'palm')
    j2 = C.person(img, FLAT, X, Y - bob * s, s, sp, tp, yaw, j)
    DRAWN[who] = (X, Y, s, yaw, mirror, j, j2)
    return X, Y, s


def p2_pull_pose(img, cam, film, sp, t, X, Y, s, yaw, mirror):
    """Player two: still through the blast and the pause; then his hands go out to the pot, rest on its far side and
    draw it in (the pot moves with them), then come back to rest."""
    j = seated_joints(film, sp)
    c = Clock
    if t < c.REACH[0]:
        return j
    if t < c.PULL[0]:
        u = ease((t - c.REACH[0]) / (c.REACH[1] - c.REACH[0]))
        pot_at = POT
    elif t < c.PULL[1]:
        u = 1.0
        w = ease((t - c.PULL[0]) / (c.PULL[1] - c.PULL[0]))
        pot_at = (POT[0] + (-1.4 - POT[0]) * w, POT[1] * (1 - w))
    else:
        u = 1 - ease((t - c.RELEASE[0]) / (c.RELEASE[1] - c.RELEASE[0]))
        pot_at = (-1.4, 0.0)
    rest = {sd: j['wr' + sd] for sd in 'LR'}
    for sd, dz in (('L', -0.14), ('R', 0.14)):
        far = (pot_at[0] + 0.15, TABLE_H + 0.05, pot_at[1] + dz)          # the far side of the pot
        tgt_screen = cam.project(far)[0]
        zb = max(120.0, (far[0] - SEATED['P2'][0]) / M_UNIT * 0.9)
        tgt = screen_hand_target(j, sd, yaw, mirror, X, Y, s, tgt_screen, zb)
        cur = tuple(r + (g - r) * u for r, g in zip(rest[sd], tgt))
        V.arm_to(j, sd, cur, 'down', 'palm')
    return j


def thrown_person(img, cam, film, who, t, dfire):
    """Before the blast: in place. Thrown: the drawing as they were, flying on its arc, spinning; slapped against a
    wall it turns upright and slides down; on the floor, a heap that stays. Out of the room past the camera: gone."""
    b = person_body(who, dfire)
    if b is None or t < b.t0:
        return draw_person(img, cam, film, who, t, hand_on=(who == 'ESCORT'))
    if b.floor_t is not None and t >= b.floor_t:
        pos, _ = b.at(t)
        if cam.depth(pos) < 0.6:
            return None
        if b.wall is not None:
            axis, sg = b.wall
            facing = (-sg, 0.0) if axis == 0 else (0.0, -sg)
        else:
            facing = _norm((cam.pos[0] - pos[0], cam.pos[2] - pos[2]))
        u = ease((t - b.floor_t) / 0.3)
        sp = dict(C.PEOPLE[who], blink=True, mouth='agape', brows='weary')
        j = heap_pose(sp, u)
        neck_h = 0.06 + (928 - j['bob'] - 478) * M_UNIT + 0.67
        (X, Y), k = cam.project((pos[0], neck_h, pos[2]))
        s = k * M_UNIT
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))             # slumped over to one side, against the wall
        C.person(lay, FLAT, X, Y - j['bob'] * s, s, sp, t, cam.yaw_of(pos, facing), j)
        hip = (X * B.SS, (Y + 450 * s) * B.SS)
        tilt = (1 if sum(map(ord, who)) % 2 else -1) * 28 * u
        lay = lay.rotate(tilt, Image.BILINEAR, center=hip)
        img.alpha_composite(lay)
        return X, Y, s
    pos, ang = b.at(t)
    if cam.depth(pos) < 0.7:
        return None
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    X0, Y0, s0 = draw_person(lay, cam, film, who, b.t0)
    bbox = lay.getbbox()
    if not bbox:
        return None
    if b.wall_t is not None and t >= b.wall_t:                          # flat against the wall, sliding down
        ang = ang * (1 - ease((t - b.wall_t) / 0.12))
    (X, Y), k = cam.project(pos)
    sc = k * M_UNIT / s0
    reach = max(bbox[2] - bbox[0], bbox[3] - bbox[1]) / B.SS * sc
    if sc > 5 or not (-reach < X < 1080 + reach and -reach < Y < 1920 + reach):
        return None
    S = B.SS
    piece = lay.crop(bbox)
    ax, ay = X0 * S - bbox[0], Y0 * S - bbox[1]
    big = piece.resize((max(1, int(piece.width * sc)), max(1, int(piece.height * sc))), Image.BILINEAR)
    pad = int(max(big.size)) + 2
    canvas = Image.new('RGBA', (big.width + 2 * pad, big.height + 2 * pad), (0, 0, 0, 0))
    canvas.paste(big, (pad, pad))
    cx, cy = pad + ax * sc, pad + ay * sc
    rot = canvas.rotate(ang, Image.BILINEAR, center=(cx, cy))
    img.paste(rot, (int(X * S - cx), int(Y * S - cy)), rot)
    return X, Y, k * M_UNIT


def chair(img, cam, who, t, dfire, near_than=None, far_than=None):
    x, z, f = SEATED[who]
    b = chair_body(who, dfire)
    if b is None or t < b.t0:
        faces = chair_faces((x, 0.0, z - 0.0), f)
    else:
        pos, ang = b.at(t)
        if cam.depth(pos) < 0.6:
            return
        faces = chair_faces((pos[0], 0.0, pos[2]), f, rot=(b.axis, math.radians(ang), (pos[0], 0.5, pos[2])))
        faces = [([(q[0], q[1] + pos[1] - 0.5, q[2]) for q in pts], col) for pts, col in faces]
        low = min(q[1] for pts, _ in faces for q in pts)
        if low < 0:
            faces = [([(q[0], q[1] - low, q[2]) for q in pts], col) for pts, col in faces]
    draw_faces(img, cam, faces, near_than, far_than)


# ------------------------------------------------------------------------------------------------ light
def parlour(img, lights, ambient=0.48, warm=(1.0, 0.86, 0.66)):
    """Low parlour light: the picture darkened to the room's glow, with warm pools round each lamp, sconce, candle
    and fire (each (X, Y, radius px, strength, colour))."""
    W_, H_ = img.size
    sm = 6
    w, h = W_ // sm, H_ // sm
    Ys, Xs = np.mgrid[0:h, 0:w]
    Lr = np.full((h, w), ambient, np.float32)
    Lg, Lb = Lr.copy() * warm[1], Lr.copy() * warm[2]
    Lr = Lr * warm[0]
    S = B.SS
    for X, Y, R, k, col in lights:
        R_ = max(4.0, R * S / sm)
        g = np.exp(-(((Xs - X * S / sm) ** 2 + (Ys - Y * S / sm) ** 2) / (R_ * R_))) * k
        Lr += g * col[0] / 255
        Lg += g * col[1] / 255
        Lb += g * col[2] / 255
    L = np.stack([Lr, Lg, Lb], -1)
    L = np.clip(L, 0, 1.35)
    Lim = Image.fromarray((L / 1.35 * 255).astype(np.uint8)).resize((W_, H_), Image.BILINEAR)
    a = np.asarray(img, np.float32)
    a[..., :3] *= np.asarray(Lim, np.float32) * (1.35 / 255)
    img.paste(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), img.mode))


# ------------------------------------------------------------------------------------------------ the shot
def lamp_point(t):
    """The low lamp over the table; the blast sets it swinging."""
    sw = 0.0
    if t > Clock.IMPACT:
        dt = t - Clock.IMPACT
        sw = 0.42 * math.exp(-dt / 2.2) * math.sin(dt * 2.6)
    return (0.1 + 1.3 * math.sin(sw), 2.25 - 1.3 * (1 - math.cos(sw)), 0.0), sw


def draw_lamp(img, cam, t):
    p = B.Pen(img, FLAT)
    (lx, ly, lz), sw = lamp_point(t)
    top = cam.project((0.1, CEIL, 0.0))[0]
    (X, Y), k = cam.project((lx, ly, lz))
    p.line([top, (X, Y)], GOLD_D, max(2, 0.012 * k))
    w = 0.42 * k
    p.poly(rough([(X - w * 0.5, Y), (X + w * 0.5, Y), (X + w * 0.95, Y + w * 0.5), (X - w * 0.95, Y + w * 0.5)], 2, 9),
           (40, 92, 64), INK, 2.2)                                                      # a green parlour shade
    for i in range(14):                                                                 # its gold fringe
        x = X - w * 0.95 + i * w * 1.9 / 13
        p.line([(x, Y + w * 0.5), (x, Y + w * 0.62)], GOLD, 2)
    return (X, Y + w * 0.55, k)


def shot(img, t, film):
    """Shot 6: the parlour from above, the beam swept round the table."""
    global FIRES, LIGHTS
    FIRES, LIGHTS = [], []
    DRAWN.clear()
    cam = sweep_cam(t)
    dfire = film.dragon_state(Clock.FIRE + 0.05)
    floor_and_walls(img, cam, t)
    decor(img, cam, t, None)
    scorch(img, cam, t, dfire)
    items = []
    tdep = cam.depth((0.0, TABLE_H, 0.0))
    items.append((tdep, 'table', None))
    for who in SEATED:
        x, z, f = SEATED[who]
        items.append((cam.depth((x, NECK_SEATED, z)), 'person', who))
        items.append((cam.depth((x, 0.5, z)) + 0.001, 'chair_far', who))
        items.append((cam.depth((x, 0.5, z)) - 0.001, 'chair_near', who))
    for who in STANDING:
        b = person_body(who, dfire)
        pos = b.at(t)[0] if b is not None and t >= b.t0 else (STANDING[who][0], 1.0, STANDING[who][1])
        items.append((cam.depth(pos), 'person', who))
    for who in SEATED:                                  # the seated thrown sort where they now are
        b = person_body(who, dfire)
        if b is not None and t >= b.t0:
            pos = b.at(t)[0]
            items = [it for it in items if not (it[1] == 'person' and it[2] == who)]
            items.append((cam.depth(pos), 'person', who))
    items.append((cam.depth((DRAGON[0], 1.0, DRAGON[1])), 'dragon', None))
    items.append((cam.depth(lamp_point(t)[0]) - 0.5, 'lamp', None))
    for dep, i, pos, ang, flying, burning in things(img, cam, t, dfire, on_table=False):
        items.append((dep, 'thing', (i, pos, ang, flying, burning)))
    mouth = None
    lamp_px = None
    for dep, kind, who in sorted(items, key=lambda it: -it[0]):
        if kind == 'table':
            table(img, cam)
            on = things(img, cam, t, dfire, on_table=True)
            draw_things(img, cam, t, sorted(on, key=lambda v: -v[0]))
            pot(img, cam, t, film)
            p2_arms(img)
        elif kind == 'person':
            if who == 'P2':
                draw_person(img, cam, film, who, t)
            else:
                thrown_person(img, cam, film, who, t, dfire)
        elif kind in ('chair_far', 'chair_near'):
            pd = cam.depth((SEATED[who][0], NECK_SEATED, SEATED[who][1]))
            if kind == 'chair_far':
                chair(img, cam, who, t, dfire, far_than=pd)
            else:
                chair(img, cam, who, t, dfire, near_than=pd)
        elif kind == 'dragon':
            st = film.dragon_state(t)
            x, z, f = DRAGON
            (X, Y), k = cam.project((x, 0.0, z))
            yaw = cam.yaw_of((x, 0, z), f)
            mouth = C.dragonite(img, FLAT, X, Y, k * M_UNIT, t, turn=min(1.0, abs(yaw) / 55.0),
                                flip=1 if yaw >= 0 else -1, head=st['head'], mouth_open=st['mouth_open'],
                                eyes=st['eyes'], wings=st['wings'], arms=st['arms'], lean=st['lean'])
        elif kind == 'lamp':
            lamp_px = draw_lamp(img, cam, t)
        elif kind == 'thing':
            i, pos, ang, flying, burning = who
            draw_things(img, cam, t, [(dep, i, pos, ang, flying, burning)])
    # drapes on fire (cloth): flames climbing them from where the beam crossed
    for i, (tf, end) in drape_fire_times(dfire).items():
        if t < tf:
            continue
        if i == 'paint':                                   # the canvas burns from where the beam crossed it
            w, a0, a1, y0, y1 = PAINTING
            grow = ease((t - tf) / 1.0)
            for kk, (fa, fy) in enumerate(((0.5, 0.0), (0.3, 0.2), (0.7, 0.25), (0.45, 0.5), (0.15, 0.55), (0.8, 0.6))):
                if fy > grow:
                    continue
                pnt = (a0 + (a1 - a0) * fa, y0 + (y1 - y0) * fy, RZ - 0.05)
                (X, Y), k = cam.project(pnt)
                FIRES.append((X, Y, 0.3 * k, 90 + kk))
            continue
        wall, a0, a1 = DRAPES[i]
        grow = ease((t - tf) / 1.2)
        for kk, (da, hy) in enumerate(((0.1, 0.1), (0.3, 0.6), (0.16, 1.2), (0.36, 1.7), (0.06, 2.2), (1.24, 0.3),
                                        (1.36, 0.9), (1.18, 1.5))):
            if hy > 0.3 + 2.4 * grow:
                continue
            a = a0 + da if da < 1 else a1 - (da - 1)
            pnt = (RX - 0.05, hy, a) if wall == 'x' else (a, hy, RZ - 0.05)
            (X, Y), k = cam.project(pnt)
            FIRES.append((X, Y, 0.35 * k, 60 + i * 10 + kk))
    # the light: lamp pool, sconces and candles (flickering), fires, the beam
    if lamp_px:
        LIGHTS.append((lamp_px[0], lamp_px[1] + 0.6 * lamp_px[2], 1.4 * lamp_px[2], 0.75, (255, 214, 150)))
    for wall, a, y in (('+x', 0.05, 1.95), ('+z', -2.3, 1.95), ('-x', -1.5, 1.95), ('-x', 2.4, 1.95), ('+z', 3.7, 1.95)):
        pt = (RX - 0.1, y, a) if wall == '+x' else (-RX + 0.1, y, a) if wall == '-x' else (a, y, RZ - 0.1)
        (X, Y), k = cam.project(pt)
        if cam.depth(pt) > 0.5:
            LIGHTS.append((X, Y, 0.8 * k, 0.5 * C.flicker(t, int(a * 10 + 50)), (255, 196, 120)))
    (X, Y), k = cam.project((-RX + 0.25, 1.2, 0.9))
    LIGHTS.append((X, Y, 0.7 * k, 0.45 * C.flicker(t, 31), (255, 190, 110)))
    for X, Y, h, sd in FIRES:
        LIGHTS.append((X, Y - h * 0.5, h * 2.6, 0.7 * C.flicker(t * 1.7, sd), (255, 150, 60)))
    beam_pts = None
    if Clock.FIRE <= t < Clock.BEAM_END[1] and mouth is not None:
        m, d = beam_ray(t, dfire)
        end, length = beam_end(m, d)
        (X1, Y1), k1 = cam.project(end)
        reach = min(1.0, (t - Clock.FIRE) / 0.08)
        x0, y0 = mouth
        x1, y1 = x0 + (X1 - x0) * reach, y0 + (Y1 - y0) * reach
        fade = 1 - ease((t - Clock.BEAM_END[0]) / (Clock.BEAM_END[1] - Clock.BEAM_END[0]))
        w0 = 0.1 * cam.project(m)[1] * ease((t - Clock.FIRE) / 0.08) * fade + 5
        beam_pts = [(x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, w0 * (0.85 + 0.4 * u)) for u in
                    np.linspace(0, 1, int(max(40, math.hypot(x1 - x0, y1 - y0) / max(4.0, w0 * 0.35))))]
        for u in np.linspace(0, 1, 6):
            LIGHTS.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, 380, 0.9 * fade, (255, 236, 170)))
        if reach >= 1:
            LIGHTS.append((X1, Y1, 300, 1.2 * fade, (255, 220, 150)))
    elif Clock.CHARGE0 < t < Clock.FIRE and mouth is not None:
        st = film.dragon_state(t)
        LIGHTS.append((mouth[0], mouth[1], 300 + 500 * st['ball'], 0.3 + 0.7 * st['ball'], (255, 236, 170)))
    parlour(img, LIGHTS)
    p = B.Pen(img, FLAT)                                 # self-lit: flames, candles, the beam
    sideboard_props(img, cam, t)
    for X, Y, h, sd in FIRES:
        C.flame(p, X, Y, h, t, sd)
    if beam_pts:
        C.glow(img, FLAT, beam_pts, strength=1.0)
        if beam_pts[-1]:
            C.glow(img, FLAT, [(beam_pts[-1][0], beam_pts[-1][1], beam_pts[-1][2] * 2.2)], strength=0.8)
    elif Clock.CHARGE0 < t < Clock.FIRE and mouth is not None:
        st = film.dragon_state(t)
        C.glow(img, FLAT, [(mouth[0], mouth[1], 8 + 26 * st['ball'])], strength=0.5 + 0.5 * st['ball'])


def p2_arms(img):
    """Player two's forearms lie over the table's edge: drawn again after the table and the pot."""
    if 'P2' not in DRAWN:
        return
    X, Y, s, yaw, mirror, j, j2 = DRAWN['P2']
    L = B.Local(FLAT, X, Y, s, -1 if mirror else 1)
    p = B.Pen(img, L)
    for sd in 'LR':
        if j2.get('hand', {}).get(sd) in ('fist', 'palm') and j['wr' + sd][1] > 260:
            V.arm(p, j2, sd, C.PEOPLE['P2'])
