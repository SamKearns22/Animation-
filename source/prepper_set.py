#!/usr/bin/env python3
"""Prepper Minister: the house, built once in 3D from `prepper_plan.py` and seen through cameras (guides/satire.md,
'One set, one plan'; guides/film-quality-rules.md rules 1-4).

Plan view as in the plan file: x east, z north, y up, metres. Every shot is a camera on this one house: the living
room (forest green carpet, cream panelled walls, the sofa facing the TV, the drinks cabinet and the Lake District
watercolour either side of the hallway door, the plush armchair by the grand window), the kitchen through the wide
opening (the slate-topped island under brass pendants, shaker units, marble splashback, the fridge, the window over
the sink run that the robots climb through) and the well-lit hallway behind both (stairs, coats, the front door).

How a frame is drawn (painter's order, the camera's own room last):
1. outside (sky, lawn, fence, the neighbours' backs), seen only through the windows;
2. every other room, far to near, with its furniture and whoever stands in it;
3. the camera's room: floor, ceiling, walls with their openings (drawn over everything beyond, so a doorway shows
   the real room behind it: rule 2), marks left on the walls, then its furniture and people, sorted so whatever
   stands between the camera and something else is drawn after it (a plan-view test, not just distance).

    python3 source/prepper_set.py test OUT.jpg      the set from the film's main cameras on one sheet (working picture)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import prepper_plan as PL        # noqa: E402
from ed import INK               # noqa: E402

FLAT = B.Cam(1.0, 540, 960)
CEIL = PL.CEIL
WT = PL.WALL_T

# ------------------------------------------------------------------------------------------------ colours
CARPET, CARPET_D, CARPET_L = (54, 92, 62), (42, 74, 50), (66, 108, 74)          # forest green
WALL_L, WALL_LD, WALL_LP = (236, 228, 212), (218, 208, 190), (226, 217, 200)     # living room: warm cream, panelled
WALL_K, WALL_KD = (238, 238, 234), (214, 214, 210)                               # kitchen: soft white
WALL_H = (240, 232, 216)                                                          # hallway
CEILING, CEILING_D = (246, 244, 238), (226, 222, 214)
SKIRT = (250, 248, 242)
TILE, TILE_D, TILE_L = (150, 150, 146), (118, 118, 114), (166, 166, 162)         # grey stone floor tiles
OAK, OAK_D = (196, 156, 108), (164, 124, 80)
SLATE, SLATE_D, SLATE_L = (58, 62, 68), (42, 46, 52), (84, 90, 98)               # slate-effect worktops
UNIT, UNIT_D = (226, 228, 224), (196, 198, 194)                                   # pale shaker units
ISLAND, ISLAND_D = (84, 98, 104), (64, 76, 82)                                    # the island: deep grey-blue
BRASS, BRASS_D = (204, 160, 72), (156, 118, 44)
STEEL, STEEL_D, STEEL_L = (186, 190, 196), (146, 150, 158), (222, 226, 230)
MARBLE, MARBLE_V = (244, 242, 238), (186, 186, 190)
SOFA, SOFA_D = (232, 224, 208), (204, 194, 176)
VELVET, VELVET_D, VELVET_L = (118, 34, 42), (88, 22, 30), (146, 52, 60)          # the plush armchair
WALNUT, WALNUT_D = (110, 70, 42), (82, 50, 28)
DOOR, DOOR_D = (248, 246, 240), (222, 218, 208)
GLASS = (196, 222, 236)
SKY, SKY_L = (172, 200, 226), (206, 222, 238)
LAWN, LAWN_D = (104, 150, 72), (84, 128, 58)
BRICK, BRICK_D = (164, 96, 72), (130, 72, 54)
HEDGE, HEDGE_D = (62, 104, 56), (46, 84, 42)
BLACK = (30, 30, 34)


# ------------------------------------------------------------------------------------------------ the camera
def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _mul(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _norm(a):
    n = math.sqrt(_dot(a, a)) or 1.0
    return (a[0] / n, a[1] / n, a[2] / n)


class Cam:
    """A perspective camera in the house (the plan's handedness: looking north, east is screen right). project()
    gives the frame point (1080 x 1920 pixels) and pixels per metre there; poly() clips at the near plane, so walls
    beside and behind the camera draw correctly. `roll` tips the picture (radians); `shake` nudges it (pixels)."""
    NEAR = 0.12

    def __init__(self, pos, at, focal=1000.0, shake=(0.0, 0.0), roll=0.0):
        self.pos, self.at, self.focal, self.shake, self.roll = tuple(pos), tuple(at), focal, shake, roll
        self.f = _norm(_sub(at, pos))
        self.r = _norm(_cross((0.0, 1.0, 0.0), self.f))
        self.u = _cross(self.f, self.r)

    def depth(self, p):
        return _dot(_sub(p, self.pos), self.f)

    def project(self, p):
        d = _sub(p, self.pos)
        z = max(self.NEAR, _dot(d, self.f))
        k = self.focal / z
        x, y = _dot(d, self.r) * k, -_dot(d, self.u) * k
        if self.roll:
            c, s = math.cos(self.roll), math.sin(self.roll)
            x, y = x * c - y * s, x * s + y * c
        return (540 + x + self.shake[0], 960 + y + self.shake[1]), k

    def P(self, p):
        return self.project(p)[0]

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
        q = self.clip([jit(p) for p in pts])
        if len(q) >= 3:
            pen.poly(q, fill, line, lw)

    def line(self, pen, pts, col, lw):
        for a, b in zip(pts, pts[1:]):
            q = self.clip([a, b, b])
            if len(q) >= 2:
                pen.line(q[:2], col, lw)

    def yaw_of(self, p, facing):
        """The drawn view for someone at p facing `facing` (dx, dz): 0 facing us, +90 facing screen right."""
        fx, fz = facing
        n = math.hypot(fx, fz) or 1.0
        fx, fz = fx / n, fz / n
        tc = (self.pos[0] - p[0], self.pos[2] - p[2])
        m = math.hypot(*tc) or 1.0
        tc = (tc[0] / m, tc[1] / m)
        right = (self.r[0], self.r[2])
        m = math.hypot(*right) or 1.0
        right = (right[0] / m, right[1] / m)
        return math.degrees(math.atan2(fx * right[0] + fz * right[1], fx * tc[0] + fz * tc[1]))

    def visible(self, p, margin=200):
        if self.depth(p) < self.NEAR:
            return False
        (x, y), _ = self.project(p)
        return -margin <= x <= 1080 + margin and -margin <= y <= 1920 + margin


def jit(p, amount=0.006):
    """Hand-cut, never ruler-straight (guides/satire.md, 'The look'): every corner nudged a few millimetres, the same
    nudge every frame and for every face that shares the corner (so nothing cracks or shimmers)."""
    h = hash((round(p[0], 3), round(p[1], 3), round(p[2], 3))) & 0xffffff
    a = ((h & 0xff) / 255 - 0.5) * 2 * amount
    b = (((h >> 8) & 0xff) / 255 - 0.5) * 2 * amount
    c = (((h >> 16) & 0xff) / 255 - 0.5) * 2 * amount
    return (p[0] + a, p[1] + b, p[2] + c)


def pen(img):
    return B.Pen(img, FLAT)


def dk(c, k=0.8):
    return tuple(int(v * k) for v in c[:3])


def lt(c, k=1.15):
    return tuple(min(255, int(v * k)) for v in c[:3])


# ------------------------------------------------------------------------------------------------ shapes
class Face:
    """A flat polygon with its outward normal (None: always drawn), colour and outline; `extra` draws details laid
    on it (panel lines, handles) right after it, only when it is seen."""
    def __init__(self, pts, n, fill, line=INK, lw=2.0, extra=None):
        self.pts, self.n, self.fill, self.line, self.lw, self.extra = pts, n, fill, line, lw, extra

    def seen(self, cam):
        if self.n is None:
            return True
        c = tuple(sum(q[i] for q in self.pts) / len(self.pts) for i in range(3))
        return _dot(self.n, _sub(cam.pos, c)) > 1e-4

    def draw(self, img, cam, p):
        cam.poly(p, self.pts, self.fill, self.line, self.lw)
        if self.extra:
            self.extra(img, cam, p)


def rot_y(v, yaw):
    """A local point (x right, y up, z forward) turned to face `yaw` degrees (0 = north, 90 = east)."""
    a = math.radians(yaw)
    x, y, z = v
    return (x * math.cos(a) + z * math.sin(a), y, -x * math.sin(a) + z * math.cos(a))


def obox(c, size, yaw=0.0, cols=None, lw=2.0, extras=None):
    """An oriented box: centre of its base c (x, y, z), size (width x, height y, depth z) in its own frame, turned to
    `yaw`. cols: dict face -> colour ('top', 'front', 'back', 'left', 'right', 'bottom'); front faces +z of its
    frame (the way it faces). Returns its faces (a part)."""
    w, h, d = size
    cols = cols or {}
    extras = extras or {}
    base = cols.get('all', (200, 200, 200))
    def P(x, y, z):
        q = rot_y((x, y, z), yaw)
        return (c[0] + q[0], c[1] + q[1], c[2] + q[2])
    x0, x1, y0, y1, z0, z1 = -w / 2, w / 2, 0.0, h, -d / 2, d / 2
    spec = {
        'top': ([P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)], (0, 1, 0)),
        'bottom': ([P(x0, y0, z0), P(x1, y0, z0), P(x1, y0, z1), P(x0, y0, z1)], (0, -1, 0)),
        'front': ([P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)], rot_y((0, 0, 1), yaw)),
        'back': ([P(x0, y0, z0), P(x1, y0, z0), P(x1, y1, z0), P(x0, y1, z0)], rot_y((0, 0, -1), yaw)),
        'left': ([P(x0, y0, z0), P(x0, y0, z1), P(x0, y1, z1), P(x0, y1, z0)], rot_y((-1, 0, 0), yaw)),
        'right': ([P(x1, y0, z0), P(x1, y0, z1), P(x1, y1, z1), P(x1, y1, z0)], rot_y((1, 0, 0), yaw)),
    }
    default = {'top': lt(base, 1.06), 'bottom': dk(base, 0.7), 'front': base, 'back': dk(base, 0.86),
               'left': dk(base, 0.9), 'right': dk(base, 0.82)}
    return [Face(pts, n, cols.get(k, default[k]), INK, lw, extras.get(k)) for k, (pts, n) in spec.items()]


def cylinder(c, r, h, cols, n=20, lw=2.0, top=True, rz=None):
    """An upright cylinder (or an oval one, rz): the side as one silhouette band (flat, the shadow side darker) and
    its top."""
    rz = rz or r
    ring0 = [(c[0] + r * math.cos(a), c[1], c[2] + rz * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    ring1 = [(x, c[1] + h, z) for x, _, z in ring0]
    def side(img, cam, p):
        q0 = [cam.project(v)[0] for v in ring0]
        q1 = [cam.project(v)[0] for v in ring1]
        pts = q0 + q1
        hull = _hull(pts)
        if len(hull) >= 3:
            p.poly(hull, cols['side'], INK, lw)
    faces = [Face([ring0[0], ring0[n // 3], ring0[2 * n // 3]], None, None, None, 0, None)]
    faces[0].draw = lambda img, cam, p: side(img, cam, p)
    if top:
        faces.append(Face(ring1, (0, 1, 0), cols['top'], INK, lw))
    return faces


def _hull(pts):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))
    if len(pts) < 3:
        return pts
    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for q in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], q) <= 0:
            hi.pop()
        hi.append(q)
    return lo[:-1] + hi[:-1]


def sphere_pts(c, r, n=10, sy=1.0, sz=1.0):
    out = []
    for a in np.linspace(0, math.pi, n):
        for b in np.linspace(0, 2 * math.pi, 2 * n, endpoint=False):
            out.append((c[0] + r * math.sin(a) * math.cos(b), c[1] + r * sy * math.cos(a), c[2] + r * sz * math.sin(a) * math.sin(b)))
    return out


def blob3(img, cam, p, pts, fill, line=INK, lw=2.0):
    """The silhouette (convex outline) of a 3D point cloud: a round thing seen from anywhere."""
    if any(cam.depth(q) < cam.NEAR for q in pts):
        return
    hull = _hull([cam.project(q)[0] for q in pts])
    if len(hull) >= 3:
        p.poly(hull, fill, line, lw)


def draw_parts(img, cam, parts, p=None):
    """Parts (lists of faces), far to near; within a part its seen faces."""
    p = p or pen(img)
    def dist(part):
        pts = [q for f in part for q in f.pts]
        c = tuple(sum(q[i] for q in pts) / len(pts) for i in range(3))
        return math.dist(c, cam.pos)
    for part in sorted(parts, key=lambda pt: -dist(pt)):
        for f in sorted(part, key=lambda f: -math.dist(tuple(sum(q[i] for q in f.pts) / len(f.pts) for i in range(3)), cam.pos)):
            if f.seen(cam):
                f.draw(img, cam, p)


# ------------------------------------------------------------------------------------------------ rooms and walls
def room_of(x, z):
    for name, (x0, z0, x1, z1) in PL.ROOMS.items():
        if x0 <= x <= x1 and z0 <= z <= z1:
            return name
    return 'outside'


ROOM_WALL = {'living room': (WALL_L, WALL_LD), 'kitchen': (WALL_K, WALL_KD), 'hallway': (WALL_H, dk(WALL_H, 0.9))}


def _walls(room):
    """The room's four walls as (key, a0, a1, fixed, axis, inward normal): axis 'z' = a wall along x at z = fixed."""
    x0, z0, x1, z1 = PL.ROOMS[room]
    return [(('z', z0), x0, x1, 'z', (0, 0, 1)), (('z', z1), x0, x1, 'z', (0, 0, -1)),
            (('x', x0), z0, z1, 'x', (1, 0, 0)), (('x', x1), z0, z1, 'x', (-1, 0, 0))]


def wpt(wall, a, y, off=0.0):
    """A point on a wall: a along it, y up it, `off` towards the room (with the wall's inward normal sign)."""
    (axis, v), n = wall
    if axis == 'z':
        return (a, y, v + n[2] * off)
    return (v + n[0] * off, y, a)


def _openings_on(key, a0, a1):
    out = []
    for name, o in PL.OPENINGS.items():
        if o['wall'] == key:
            s0, s1 = max(o['span'][0], a0), min(o['span'][1], a1)
            if s1 > s0:
                out.append((name, s0, s1, o['sill'], o['head']))
    return sorted(out, key=lambda q: q[1])


def wall_pieces(room):
    """The wall rectangles round every opening: (a0, a1, y0, y1)."""
    out = []
    for key, a0, a1, axis, n in _walls(room):
        ops = _openings_on(key, a0, a1)
        pos = a0
        pieces = []
        for name, s0, s1, sill, head in ops:
            if s0 > pos:
                pieces.append((pos, s0, 0.0, CEIL))
            pieces.append((s0, s1, head, CEIL))
            if sill > 0:
                pieces.append((s0, s1, 0.0, sill))
            pos = s1
        if a1 > pos:
            pieces.append((pos, a1, 0.0, CEIL))
        out.append(((key, n), pieces, ops))
    return out


def floor(img, cam, p, room):
    x0, z0, x1, z1 = PL.ROOMS[room]
    if room == 'living room':
        cam.poly(p, [(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)], CARPET, None)
        rng = np.random.default_rng(3)                      # the carpet's pile: small flat tufts, two tones
        for _ in range(420):
            x, z = rng.uniform(x0 + 0.05, x1 - 0.05), rng.uniform(z0 + 0.05, z1 - 0.05)
            if math.dist((x, 0, z), cam.pos) > 9:
                continue
            a, l = rng.uniform(0, math.pi), rng.uniform(0.03, 0.07)
            col = CARPET_D if rng.random() < 0.6 else CARPET_L
            cam.line(p, [(x, 0.002, z), (x + l * math.cos(a), 0.002, z + l * math.sin(a))], col, 2.0)
    elif room == 'kitchen':                                 # large grey stone tiles (60 x 60), each its own shade
        cam.poly(p, [(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)], TILE, None)
        rng = np.random.default_rng(5)
        for i, x in enumerate(np.arange(x0, x1, 0.6)):
            for k, z in enumerate(np.arange(z0, z1, 0.6)):
                v = rng.uniform(-10, 10)
                col = tuple(int(c + v) for c in TILE)
                cam.poly(p, [(x, 0.001, z), (min(x + 0.6, x1), 0.001, z), (min(x + 0.6, x1), 0.001, min(z + 0.6, z1)),
                             (x, 0.001, min(z + 0.6, z1))], col, TILE_D, 1.2)
    else:                                                    # oak boards
        cam.poly(p, [(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)], OAK, None)
        for z in np.arange(z0 + 0.14, z1, 0.14):
            cam.line(p, [(x0, 0.001, z), (x1, 0.001, z)], OAK_D, 1.2)


def ceiling(img, cam, p, room):
    x0, z0, x1, z1 = PL.ROOMS[room]
    if cam.pos[1] > CEIL:
        return
    cam.poly(p, [(x0, CEIL, z0), (x0, CEIL, z1), (x1, CEIL, z1), (x1, CEIL, z0)], CEILING, INK, 2.0)
    m = 0.35                                                 # a coffer / tray line round the room
    cam.poly(p, [(x0 + m, CEIL - 0.001, z0 + m), (x0 + m, CEIL - 0.001, z1 - m), (x1 - m, CEIL - 0.001, z1 - m),
                 (x1 - m, CEIL - 0.001, z0 + m)], CEILING, CEILING_D, 2.0)
    nx, nz = max(1, int((x1 - x0) / 1.6)), max(1, int((z1 - z0) / 1.6))
    for i in range(nx):                                     # recessed downlights
        for k in range(nz):
            x = x0 + (i + 0.5) * (x1 - x0) / nx
            z = z0 + (k + 0.5) * (z1 - z0) / nz
            ring = [(x + 0.05 * math.cos(a), CEIL - 0.002, z + 0.05 * math.sin(a)) for a in np.linspace(0, 6.28, 10, endpoint=False)]
            cam.poly(p, ring, (255, 252, 236), CEILING_D, 1.4)


def walls(img, cam, room, marks=(), glass=None, t=0.0):
    """The room's walls seen from inside it, with every opening left open (what is beyond is already drawn), the
    reveals (the wall's thickness) in each opening, skirting, cornice and the panelling; windows get frames and
    glass; then the wall decor (the watercolour, switches) and any marks (bullet holes, scorches)."""
    p = pen(img)
    col, col_d = ROOM_WALL[room]
    for (key, n), pieces, ops in wall_pieces(room):
        wall = (key, n)
        c = wpt(wall, (pieces[0][0] + pieces[-1][1]) / 2 if pieces else 0, 1.4)
        if _dot(n, _sub(cam.pos, c)) <= 0:
            continue
        for a0, a1, y0, y1 in pieces:
            cam.poly(p, [wpt(wall, a0, y0), wpt(wall, a1, y0), wpt(wall, a1, y1), wpt(wall, a0, y1)], col, None)
        a_lo, a_hi = min(q[0] for q in pieces), max(q[1] for q in pieces)
        # skirting and cornice, broken at the floor-level openings
        for a0, a1, y0, y1 in pieces:
            if y0 == 0.0:
                cam.poly(p, [wpt(wall, a0, 0, 0.004), wpt(wall, a1, 0, 0.004), wpt(wall, a1, 0.12, 0.004),
                             wpt(wall, a0, 0.12, 0.004)], SKIRT, INK, 1.6)
            if y1 >= CEIL - 0.01:
                cam.poly(p, [wpt(wall, a0, CEIL - 0.1, 0.004), wpt(wall, a1, CEIL - 0.1, 0.004), wpt(wall, a1, CEIL, 0.004),
                             wpt(wall, a0, CEIL, 0.004)], SKIRT, INK, 1.6)
        if room == 'living room':                           # panel mouldings below and above a dado rail
            for a0, a1, y0, y1 in pieces:
                if y0 > 0 or y1 < CEIL - 0.01 or a1 - a0 < 0.5:
                    continue
                cam.line(p, [wpt(wall, a0, 0.95, 0.004), wpt(wall, a1, 0.95, 0.004)], col_d, 2.4)
                nb = max(1, int((a1 - a0) / 1.0))
                w = (a1 - a0) / nb
                for i in range(nb):
                    b0, b1 = a0 + i * w + 0.12, a0 + (i + 1) * w - 0.12
                    for (ya, yb) in ((0.24, 0.8), (1.1, CEIL - 0.3)):
                        cam.poly(p, [wpt(wall, b0, ya, 0.003), wpt(wall, b1, ya, 0.003), wpt(wall, b1, yb, 0.003),
                                     wpt(wall, b0, yb, 0.003)], WALL_LP, col_d, 1.8)
        # the openings: reveals (the wall's thickness) and, for windows, frames and glass
        for name, s0, s1, sill, head in ops:
            back = -WT
            for a in (s0, s1):
                cam.poly(p, [wpt(wall, a, sill, 0), wpt(wall, a, sill, back), wpt(wall, a, head, back), wpt(wall, a, head, 0)],
                         col_d, INK, 1.6)
            cam.poly(p, [wpt(wall, s0, head, 0), wpt(wall, s1, head, 0), wpt(wall, s1, head, back), wpt(wall, s0, head, back)],
                     dk(col_d, 0.92), INK, 1.6)
            if sill > 0:
                cam.poly(p, [wpt(wall, s0, sill, 0.03), wpt(wall, s1, sill, 0.03), wpt(wall, s1, sill, back),
                             wpt(wall, s0, sill, back)], SKIRT, INK, 1.6)
            if 'window' in name:
                window(img, cam, p, wall, name, s0, s1, sill, head, glass)
            elif 'door' in name:                              # a white architrave round the doorway
                for a, sg in ((s0, -1), (s1, 1)):
                    cam.poly(p, [wpt(wall, a, 0, 0.01), wpt(wall, a + sg * 0.07, 0, 0.01),
                                 wpt(wall, a + sg * 0.07, head + 0.07, 0.01), wpt(wall, a, head + 0.07, 0.01)],
                             SKIRT, INK, 1.6)
                cam.poly(p, [wpt(wall, s0 - 0.07, head, 0.01), wpt(wall, s1 + 0.07, head, 0.01),
                             wpt(wall, s1 + 0.07, head + 0.07, 0.01), wpt(wall, s0 - 0.07, head + 0.07, 0.01)], SKIRT, INK, 1.6)
        # the outline of the wall itself (its outer edges, never across an opening)
        for a0, a1, y0, y1 in pieces:
            cam.line(p, [wpt(wall, a0, y0), wpt(wall, a0, y1)], INK, 2.0) if a0 == a_lo else None
            cam.line(p, [wpt(wall, a1, y0), wpt(wall, a1, y1)], INK, 2.0) if a1 == a_hi else None
        cam.line(p, [wpt(wall, a_lo, 0), wpt(wall, a_hi, 0)], INK, 2.0)
        cam.line(p, [wpt(wall, a_lo, CEIL), wpt(wall, a_hi, CEIL)], INK, 2.0)
        decor(img, cam, p, room, wall)
    for m in marks:
        if room_of(m['at'][0], m['at'][2]) == room or m.get('room') == room:
            if t >= m['t']:
                mark(img, cam, p, m, t)


def window(img, cam, p, wall, name, s0, s1, sill, head, glass):
    """A grand window: white frame, mullions and a transom; the glass a faint pale sheen with a few flat streaks (the
    garden shows through); a broken pane leaves a jagged hole with shards round its edge."""
    glass = glass or {}
    n_panes = max(2, int(round((s1 - s0) / 0.8)))
    w = (s1 - s0) / n_panes
    tr = head - 0.45
    gone = name in glass.get('_frames_gone', ())                       # shot out (Sam, 24 Oct): mullions and transom gone, one
    panes = []                                                # open hole with shards round the surround
    for i in range(n_panes):
        a0, a1 = s0 + i * w, s0 + (i + 1) * w
        panes += [(f'{name} {i} low', a0, a1, sill, tr), (f'{name} {i} top', a0, a1, tr, head)]
    if gone:
        panes = [(f'{name} hole', s0, s1, sill, head)]
        glass = {f'{name} hole': {'seed': 11}}
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    lp = pen(lay)
    for key, a0, a1, y0, y1 in panes:
        g = glass.get(key)
        off = -WT * 0.5
        quad = [wpt(wall, a0, y0, off), wpt(wall, a1, y0, off), wpt(wall, a1, y1, off), wpt(wall, a0, y1, off)]
        if g is None:                                         # whole: a faint sheen and two diagonal streaks
            cam.poly(lp, quad, GLASS + (46,), None)
            for k, u in enumerate((0.25, 0.42)):
                q = [wpt(wall, a0 + (a1 - a0) * u, y0 + 0.1, off), wpt(wall, a0 + (a1 - a0) * (u + 0.1), y0 + 0.1, off),
                     wpt(wall, a0 + (a1 - a0) * (u + 0.42), y1 - 0.1, off), wpt(wall, a0 + (a1 - a0) * (u + 0.32), y1 - 0.1, off)]
                cam.poly(lp, q, (255, 255, 255, 70 - 25 * k), None)
        else:                                                 # broken: shards left round the frame
            rng = np.random.default_rng(g.get('seed', 1))
            cx, cy = (a0 + a1) / 2 + rng.uniform(-0.1, 0.1), (y0 + y1) / 2 + rng.uniform(-0.1, 0.1)
            edge = [(a0, y0), (a1, y0), (a1, y1), (a0, y1)]
            for e in range(4):
                (ea, ey), (fa, fy) = edge[e], edge[(e + 1) % 4]
                for k in range(3):
                    u0, u1 = k / 3, (k + 1) / 3
                    pa = (ea + (fa - ea) * u0, ey + (fy - ey) * u0)
                    pb = (ea + (fa - ea) * u1, ey + (fy - ey) * u1)
                    tip = rng.uniform(0.15, 0.55)
                    mid = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)
                    pt = (mid[0] + (cx - mid[0]) * tip, mid[1] + (cy - mid[1]) * tip)
                    tri = [wpt(wall, pa[0], pa[1], off), wpt(wall, pb[0], pb[1], off), wpt(wall, pt[0], pt[1], off)]
                    cam.poly(lp, tri, GLASS + (90,), (255, 255, 255, 200), 1.2)
    img.alpha_composite(lay)
    fw = 0.05
    for a in ([s0, s1] if gone else [s0 + i * w for i in range(n_panes + 1)]):        # mullions
        cam.poly(p, [wpt(wall, a - fw, sill, -0.02), wpt(wall, a + fw, sill, -0.02), wpt(wall, a + fw, head, -0.02),
                     wpt(wall, a - fw, head, -0.02)], SKIRT, INK, 1.6)
    for y in ((sill, head) if gone else (sill, tr, head)):   # transom, sill and head rails
        cam.poly(p, [wpt(wall, s0, y - fw, -0.02), wpt(wall, s1, y - fw, -0.02), wpt(wall, s1, y + fw, -0.02),
                     wpt(wall, s0, y + fw, -0.02)], SKIRT, INK, 1.6)
    if name == 'living window':                              # long linen curtains drawn back either side
        for a, sg in ((s0, -1), (s1, 1)):
            for k in range(3):
                b0 = a + sg * (0.04 + 0.1 * k)
                b1 = b0 + sg * 0.12
                cam.poly(p, [wpt(wall, b0, 0.02, 0.08 + 0.02 * (k % 2)), wpt(wall, b1, 0.02, 0.08 + 0.02 * (k % 2)),
                             wpt(wall, b1, CEIL - 0.12, 0.06), wpt(wall, b0, CEIL - 0.12, 0.06)],
                         (196, 178, 140) if k % 2 else (214, 196, 160), INK, 1.4)


def decor(img, cam, p, room, wall):
    """What hangs on the walls (the plan's watercolour; switches by the doors; the kitchen's splashback and wall
    cupboards are furniture)."""
    (axis, v), n = wall
    if room == 'living room' and axis == 'z' and v == 5.4:
        th = PL.THINGS['watercolour']
        cx, w, h, y = th['at'][0], th['size'][0], th['size'][2], th['y']
        watercolour(img, cam, p, wall, cx - w / 2, cx + w / 2, y, y + h)
        switch(cam, p, wall, 3.12, 1.2)
    if room == 'living room' and axis == 'x' and v == 0.0:
        switch(cam, p, wall, 0.95, 1.2)
    if room == 'kitchen' and axis == 'z' and v == 5.4:
        switch(cam, p, wall, -0.6, 1.2)
    if room == 'hallway' and axis == 'z' and v == 7.0:       # the wall seen through the living room door: a mirror over
        mirror(cam, p, wall, 2.55, 1.15)                     # a console table, coats on hooks further along
        for k, cx in enumerate((3.6, 3.85, 4.1)):
            col = [(70, 64, 90), (150, 110, 70), (60, 70, 60)][k]
            cam.poly(p, [wpt(wall, cx - 0.14, 1.75, 0.06), wpt(wall, cx + 0.14, 1.75, 0.06), wpt(wall, cx + 0.2, 0.95, 0.12),
                         wpt(wall, cx - 0.2, 0.95, 0.12)], col, INK, 1.6)
            cam.poly(p, [wpt(wall, cx - 0.04, 1.75, 0.02), wpt(wall, cx + 0.04, 1.75, 0.02), wpt(wall, cx + 0.04, 1.82, 0.02),
                         wpt(wall, cx - 0.04, 1.82, 0.02)], BRASS, INK, 1.2)


def switch(cam, p, wall, a, y):
    cam.poly(p, [wpt(wall, a - 0.043, y - 0.043, 0.006), wpt(wall, a + 0.043, y - 0.043, 0.006),
                 wpt(wall, a + 0.043, y + 0.043, 0.006), wpt(wall, a - 0.043, y + 0.043, 0.006)], BRASS, INK, 1.2)


def mirror(cam, p, wall, a, y):
    cam.poly(p, [wpt(wall, a - 0.4, y, 0.02), wpt(wall, a + 0.4, y, 0.02), wpt(wall, a + 0.4, y + 0.8, 0.02),
                 wpt(wall, a - 0.4, y + 0.8, 0.02)], BRASS, INK, 1.6)
    cam.poly(p, [wpt(wall, a - 0.34, y + 0.06, 0.025), wpt(wall, a + 0.34, y + 0.06, 0.025), wpt(wall, a + 0.34, y + 0.74, 0.025),
                 wpt(wall, a - 0.34, y + 0.74, 0.025)], (200, 214, 222), INK, 1.4)
    cam.poly(p, [wpt(wall, a - 0.2, y + 0.1, 0.03), wpt(wall, a - 0.1, y + 0.1, 0.03), wpt(wall, a + 0.1, y + 0.7, 0.03),
                 wpt(wall, a, y + 0.7, 0.03)], (226, 236, 240), None)


def watercolour(img, cam, p, wall, a0, a1, y0, y1):
    """The Lake District watercolour (brief: right of the hallway door): a pale gilt frame and white mount; a soft
    sky, three ranges of fells fading blue-grey into the distance, a lake catching the light, a green near shore."""
    def W(u, v, off=0.02):          # u across 0..1, v up 0..1, laid on the wall
        return wpt(wall, a0 + (a1 - a0) * u, y0 + (y1 - y0) * v, off)
    cam.poly(p, [W(0, 0), W(1, 0), W(1, 1), W(0, 1)], (190, 156, 90), INK, 2.0)            # frame
    cam.poly(p, [W(0.06, 0.08, 0.022), W(0.94, 0.08, 0.022), W(0.94, 0.92, 0.022), W(0.06, 0.92, 0.022)],
             (246, 244, 236), INK, 1.4)                                                        # mount
    m = (0.14, 0.17, 0.86, 0.83)
    def I(u, v):
        return W(m[0] + (m[2] - m[0]) * u, m[1] + (m[3] - m[1]) * v, 0.024)
    cam.poly(p, [I(0, 0), I(1, 0), I(1, 1), I(0, 1)], (214, 226, 234), INK, 1.2)              # sky
    cam.poly(p, [I(0.0, 0.55), I(0.25, 0.8), I(0.45, 0.64), I(0.7, 0.86), I(1.0, 0.6), I(1, 0.4), I(0, 0.4)],
             (150, 166, 190), None)                                                              # far fells
    cam.poly(p, [I(0.0, 0.45), I(0.18, 0.62), I(0.36, 0.5), I(0.6, 0.68), I(0.82, 0.5), I(1.0, 0.56), I(1, 0.32), I(0, 0.32)],
             (112, 136, 140), None)                                                              # middle fells
    cam.poly(p, [I(0, 0.34), I(1, 0.34), I(1, 0.22), I(0, 0.22)], (180, 204, 214), None)       # the lake
    cam.poly(p, [I(0.3, 0.3), I(0.55, 0.3), I(0.55, 0.28), I(0.3, 0.28)], (236, 242, 244), None)
    cam.poly(p, [I(0, 0.24), I(0.3, 0.18), I(0.6, 0.24), I(1.0, 0.16), I(1, 0), I(0, 0)], (96, 130, 80), None)   # near shore


def mark(img, cam, p, m, t):
    """Something that stays changed (guides/satire.md: anything that changes stays changed): a bullet hole (a dark
    hole in a pale ring of chipped plaster), a scorch (a flat dark star), a chip off the tiles."""
    at, nrm, kind, s = m['at'], m['n'], m['kind'], m.get('size', 0.04)
    # two axes on the surface
    a = _norm(_cross(nrm, (0, 1, 0))) if abs(nrm[1]) < 0.9 else (1, 0, 0)
    b = _cross(nrm, a)
    def S(u, v, off=0.006):
        return (at[0] + a[0] * u + b[0] * v + nrm[0] * off, at[1] + a[1] * u + b[1] * v + nrm[1] * off,
                at[2] + a[2] * u + b[2] * v + nrm[2] * off)
    rng = np.random.default_rng(m.get('seed', 1))
    if kind == 'scorch':
        pts = [S(s * r * math.cos(q), s * r * math.sin(q)) for q, r in
               zip(np.linspace(0, 6.28, 14, endpoint=False), rng.uniform(0.5, 1.4, 14))]
        cam.poly(p, pts, (60, 56, 54), None)
        cam.poly(p, [S(s * 0.3 * math.cos(q), s * 0.3 * math.sin(q), 0.007) for q in np.linspace(0, 6.28, 8, endpoint=False)],
                 (30, 28, 28), None)
        return
    ring = [S(s * r * math.cos(q), s * r * math.sin(q)) for q, r in
            zip(np.linspace(0, 6.28, 9, endpoint=False), rng.uniform(0.7, 1.2, 9))]
    cam.poly(p, ring, m.get('chip', (250, 248, 244)), INK, 1.0)
    cam.poly(p, [S(s * 0.35 * math.cos(q), s * 0.35 * math.sin(q), 0.007) for q in np.linspace(0, 6.28, 7, endpoint=False)],
             (36, 32, 32), None)


# ------------------------------------------------------------------------------------------------ outside
def outside(img, cam, t):
    """The back gardens, seen only through the windows: sky, a lawn, a timber fence, hedges, a tree, and the backs
    of the neighbours' brick houses with their windows (never a blank wall)."""
    p = pen(img)
    img.paste(SKY + (255,), (0, 0) + img.size)
    for side in (-1, 1):                                      # east garden (living window), west garden (kitchen)
        xw = 6.0 if side > 0 else -5.6
        far = xw + side * 14.0
        cam.poly(p, [(xw, -0.01, -6), (far, -0.01, -6), (far, -0.01, 14), (xw, -0.01, 14)], LAWN, None)
        for k in range(10):                                   # mown stripes
            x = xw + side * (0.6 + 1.2 * k)
            cam.poly(p, [(x, 0, -6), (x + side * 0.6, 0, -6), (x + side * 0.6, 0, 14), (x, 0, 14)], LAWN_D, None)
        fx = xw + side * 9.0                                   # the fence, then the houses behind
        hx = xw + side * 16.0
        for z0 in np.arange(-8, 16, 5.6):
            cam.poly(p, [(hx, 0, z0), (hx, 0, z0 + 5.4), (hx, 6.5, z0 + 5.4), (hx, 6.5, z0)], BRICK, INK, 2.0)
            cam.poly(p, [(hx, 6.5, z0 - 0.1), (hx, 6.5, z0 + 5.5), (hx + side * 2.2, 8.4, z0 + 5.5), (hx + side * 2.2, 8.4, z0 - 0.1)],
                     (86, 80, 84), INK, 2.0)
            for wz in (z0 + 0.8, z0 + 3.4):
                for wy in (1.0, 3.8):
                    cam.poly(p, [(hx - side * 0.01, wy, wz), (hx - side * 0.01, wy, wz + 1.1), (hx - side * 0.01, wy + 1.4, wz + 1.1),
                                 (hx - side * 0.01, wy + 1.4, wz)], (230, 234, 236), INK, 1.6)
                    cam.poly(p, [(hx - side * 0.02, wy + 0.08, wz + 0.08), (hx - side * 0.02, wy + 0.08, wz + 1.02),
                                 (hx - side * 0.02, wy + 1.32, wz + 1.02), (hx - side * 0.02, wy + 1.32, wz + 0.08)],
                             (96, 120, 140), None)
        cam.poly(p, [(fx, 0, -8), (fx, 0, 16), (fx, 1.8, 16), (fx, 1.8, -8)], (150, 112, 76), INK, 2.0)
        for z in np.arange(-8, 16, 0.15):
            cam.line(p, [(fx - side * 0.01, 0, z), (fx - side * 0.01, 1.8, z)], (126, 92, 60), 1.2)
        for z in np.arange(-6, 14, 1.3):                     # a hedge along the fence
            blob3(img, cam, p, sphere_pts((fx - side * 0.5, 1.0, z), 0.75, 6, sy=1.2), HEDGE if int(z) % 2 else HEDGE_D, INK, 1.8)
        tz = 1.5 if side > 0 else 4.0                         # a tree
        cam.poly(p, [(fx - side * 2.0 - 0.12, 0, tz), (fx - side * 2.0 + 0.12, 0, tz), (fx - side * 2.0 + 0.1, 3.0, tz),
                     (fx - side * 2.0 - 0.1, 3.0, tz)], (100, 74, 52), INK, 1.8)
        for dx, dy, dz, r in ((0, 3.6, 0, 1.4), (0.6, 4.2, 0.5, 1.1), (-0.5, 4.3, -0.4, 1.0)):
            blob3(img, cam, p, sphere_pts((fx - side * 2.0 + dx, dy, tz + dz), r, 6), (88, 140, 70), INK, 1.8)


# ------------------------------------------------------------------------------------------------ furniture
def _thing(name):
    th = PL.THINGS[name]
    (x, z), (sx, sz, sy) = th['at'], th['size']
    return x, z, sx, sz, sy, th.get('facing', 0), th.get('y', 0.0)


def _yaw_of_facing(f):
    """The plan's facing (0 = north, 90 = east) as obox's yaw: its front faces +z turned by yaw."""
    return f


def sofa_parts():
    """A cream modern sofa (refs living-1, -2): a long low seat, a back, square arms, three seat cushions and two
    scatter cushions (forest green and rust)."""
    x, z, w, d, h, f, _ = _thing('sofa')
    yaw = 180                                                 # it faces south (the TV)
    def P(u, v):                                              # u across (its right = west when facing south), v forward
        q = rot_y((u, 0, v), yaw)
        return (x + q[0], 0.0, z + q[2])
    parts = [obox(P(0, 0.05), (w, 0.2, d - 0.1), yaw, {'all': dk(SOFA, 0.9)}),
             obox(P(0, -d / 2 + 0.14), (w, h, 0.28), yaw, {'all': SOFA}),
             obox(P(-w / 2 + 0.1, 0.02), (0.2, 0.62, d - 0.04), yaw, {'all': SOFA}),
             obox(P(w / 2 - 0.1, 0.02), (0.2, 0.62, d - 0.04), yaw, {'all': SOFA})]
    for k in range(3):
        cw = (w - 0.4) / 3
        parts.append(obox((P(-w / 2 + 0.2 + cw * (k + 0.5), 0.12)[0], 0.2, P(0, 0.12)[2]), (cw - 0.02, 0.25, d - 0.36), yaw,
                          {'all': SOFA, 'top': lt(SOFA, 1.03)}))
        parts.append(obox((P(-w / 2 + 0.2 + cw * (k + 0.5), -d / 2 + 0.36)[0], 0.45, P(0, -d / 2 + 0.36)[2]),
                          (cw - 0.04, 0.38, 0.16), yaw, {'all': lt(SOFA, 1.02)}))
    for u, col in ((-0.75, (66, 104, 74)), (0.78, (176, 96, 60))):
        parts.append(obox((P(u, -d / 2 + 0.5)[0], 0.45, P(u, -d / 2 + 0.5)[2]), (0.42, 0.4, 0.14), yaw + (8 if u < 0 else -10),
                          {'all': col}))
    return parts


def armchair_parts():
    """The plush old-world armchair (brief): burgundy velvet wingback, buttoned back, rolled arms, turned walnut feet."""
    x, z, w, d, h, f, _ = _thing('armchair')
    yaw = f
    def P(u, y, v):
        q = rot_y((u, y, v), yaw)
        return (x + q[0], y, z + q[2])
    def buttons(img, cam, p):
        for i in range(3):
            for k in range(2):
                c = P(-0.18 + 0.18 * i, 0.62 + 0.18 * k, -d / 2 + 0.2 + 0.001)
                c = (c[0] + rot_y((0, 0, 1), yaw)[0] * 0.001, c[1], c[2] + rot_y((0, 0, 1), yaw)[2] * 0.001)
                ring = [(c[0] + 0.012 * math.cos(a) * math.cos(math.radians(yaw)), c[1] + 0.012 * math.sin(a), c[2])
                        for a in np.linspace(0, 6.28, 6, endpoint=False)]
                cam.poly(p, ring, VELVET_D, None)
    parts = []
    for u in (-w / 2 + 0.08, w / 2 - 0.08):
        for v in (-d / 2 + 0.08, d / 2 - 0.1):
            parts.append(obox(P(u, 0, v), (0.06, 0.12, 0.06), yaw, {'all': WALNUT}))
    parts += [obox(P(0, 0.12, 0.02), (w, 0.3, d - 0.08), yaw, {'all': VELVET}),
              obox(P(0, 0.42, 0.06), (w - 0.3, 0.12, d - 0.32), yaw, {'all': VELVET, 'top': VELVET_L}),
              obox(P(0, 0.12, -d / 2 + 0.1), (w - 0.04, h - 0.12, 0.2), yaw, {'all': VELVET}, extras={'front': buttons}),
              obox(P(-w / 2 + 0.09, 0.42, 0.04), (0.18, 0.26, d - 0.12), yaw, {'all': VELVET, 'top': VELVET_L}),
              obox(P(w / 2 - 0.09, 0.42, 0.04), (0.18, 0.26, d - 0.12), yaw, {'all': VELVET, 'top': VELVET_L}),
              obox(P(-w / 2 + 0.05, 0.68, -d / 2 + 0.22), (0.1, 0.27, 0.3), yaw, {'all': VELVET}),     # the wings
              obox(P(w / 2 - 0.05, 0.68, -d / 2 + 0.22), (0.1, 0.27, 0.3), yaw, {'all': VELVET})]
    return parts


def coffee_table_parts():
    x, z, w, d, h, f, _ = _thing('coffee table')
    parts = [cylinder((x, h - 0.05, z), w / 2, 0.05, {'side': WALNUT_D, 'top': WALNUT}, n=28, rz=d / 2),
             cylinder((x, 0.0, z), w * 0.32, h - 0.05, {'side': WALNUT_D, 'top': WALNUT_D}, n=20, rz=d * 0.3)]
    parts.append(obox((x - 0.2, h, z + 0.05), (0.3, 0.05, 0.22), 12, {'all': (40, 60, 90)}))      # books
    parts.append(obox((x - 0.2, h + 0.05, z + 0.05), (0.26, 0.04, 0.2), 6, {'all': (226, 220, 206)}))
    # (Sam's note 31, 25 Oct: the dark bowl here read as an unknown black object; gone, his coffee stands here now)
    return parts


def media_parts():
    x, z, w, d, h, f, _ = _thing('media unit')
    tx, tz, tw, td, th, _, ty = _thing('tv')
    def tv_front(img, cam, p):
        pass
    return [obox((x, 0.12, z), (w, h - 0.12, d), 0, {'all': WALNUT, 'top': lt(WALNUT, 1.1)}),
            obox((x - w / 2 + 0.1, 0, z), (0.06, 0.12, d - 0.06), 0, {'all': BLACK}),
            obox((x + w / 2 - 0.1, 0, z), (0.06, 0.12, d - 0.06), 0, {'all': BLACK}),
            obox((tx, ty, tz), (tw, th, td), 0, {'all': (20, 20, 24), 'back': (16, 16, 20)}, extras={'back': tv_front})]


def cabinet_parts():
    """The drinks cabinet (left of the hallway door): walnut, two glazed doors with bottles and glasses showing
    through, brass handles, on tapered legs."""
    x, z, w, d, h, f, _ = _thing('drinks cabinet')
    yaw = f
    def front(img, cam, p):
        fz = z - d / 2 - 0.002
        for k, (u0, u1) in enumerate(((-w / 2 + 0.05, -0.01), (0.01, w / 2 - 0.05))):
            cam.poly(p, [(x + u0, 0.3, fz), (x + u1, 0.3, fz), (x + u1, h - 0.06, fz), (x + u0, h - 0.06, fz)],
                     (70, 44, 30), INK, 1.4)
            for j, (bu, bh, bc) in enumerate(((0.08, 0.32, (90, 40, 30)), (0.2, 0.28, (60, 110, 70)), (0.3, 0.34, (190, 150, 70)))):
                bx = x + u0 + bu
                for shelf in (0.34, 0.86):
                    cam.poly(p, [(bx - 0.03, shelf, fz - 0.001), (bx + 0.03, shelf, fz - 0.001), (bx + 0.03, shelf + bh * 0.7, fz - 0.001),
                                 (bx + 0.012, shelf + bh, fz - 0.001), (bx - 0.012, shelf + bh, fz - 0.001),
                                 (bx - 0.03, shelf + bh * 0.7, fz - 0.001)], bc, INK, 1.0)
            cam.poly(p, [(x + u0 + 0.02, 0.32, fz - 0.003), (x + u0 + 0.08, 0.32, fz - 0.003), (x + u1 - 0.05, h - 0.08, fz - 0.003),
                         (x + u1 - 0.1, h - 0.08, fz - 0.003)], (255, 255, 255), None)          # a sheen on the glass
            hx = x + (u1 - 0.03 if k == 0 else u0 + 0.03)
            cam.poly(p, [(hx - 0.008, 0.8, fz - 0.004), (hx + 0.008, 0.8, fz - 0.004), (hx + 0.008, 1.0, fz - 0.004),
                         (hx - 0.008, 1.0, fz - 0.004)], BRASS, INK, 1.0)
    parts = [obox((x, 0.18, z), (w, h - 0.18, d), 0, {'all': WALNUT, 'top': lt(WALNUT, 1.1)}, extras={'back': front})]
    for u in (-w / 2 + 0.06, w / 2 - 0.06):
        parts.append(obox((x + u, 0, z - d / 2 + 0.06), (0.04, 0.18, 0.04), 0, {'all': WALNUT_D}))
    parts.append(obox((x - 0.15, h, z), (0.1, 0.24, 0.1), 0, {'all': (170, 120, 50)}))           # a decanter and a lamp on top
    parts.append(cylinder((x + 0.22, h, z), 0.05, 0.3, {'side': BRASS_D, 'top': BRASS}, n=12))
    parts.append(cylinder((x + 0.22, h + 0.3, z), 0.13, 0.16, {'side': (240, 232, 214), 'top': (250, 244, 230)}, n=16))
    return parts


def side_table_parts():
    x, z, w, d, h, f, _ = _thing('side table')
    return [cylinder((x, h - 0.04, z), w / 2, 0.04, {'side': WALNUT_D, 'top': WALNUT}, n=18),
            cylinder((x, 0, z), 0.04, h - 0.04, {'side': WALNUT_D, 'top': WALNUT_D}, n=8),
            cylinder((x, h, z), 0.07, 0.22, {'side': (60, 104, 120), 'top': (80, 124, 140)}, n=12)]


def lamp_parts():
    x, z, w, d, h, f, _ = _thing('floor lamp')
    return [cylinder((x, 0, z), 0.16, 0.03, {'side': BLACK, 'top': BLACK}, n=14),
            cylinder((x, 0.03, z), 0.015, h - 0.3, {'side': BRASS_D, 'top': BRASS}, n=6),
            cylinder((x, h - 0.32, z), 0.2, 0.3, {'side': (244, 236, 216), 'top': (252, 248, 236)}, n=18)]


def plant_parts():
    x, z, w, d, h, f, _ = _thing('plant')
    parts = [cylinder((x, 0, z), 0.2, 0.36, {'side': (226, 222, 214), 'top': (90, 70, 50)}, n=16)]
    def leaves(img, cam, p):
        rng = np.random.default_rng(9)
        for k in range(14):                                   # a fiddle-leaf fig: big flat leaves up a stem
            y = 0.5 + 0.06 * k
            a = rng.uniform(0, 6.28)
            c = (x + 0.18 * math.cos(a), y, z + 0.18 * math.sin(a))
            blob3(img, cam, p, sphere_pts(c, 0.12, 5, sy=0.7, sz=0.6), (70, 120, 60) if k % 3 else (90, 140, 70), INK, 1.4)
    stem = Face([(x, 0.36, z), (x, 1.3, z), (x + 0.01, 1.3, z)], None, None)
    stem.draw = lambda img, cam, p: (cam.line(p, [(x, 0.36, z), (x, h, z)], (90, 70, 50), 3.0), leaves(img, cam, p))
    parts.append([stem])
    return parts


def stool_parts(name):
    """A bar stool (ref kitchen-1): a grey upholstered seat with a low back, four thin black legs, a footrest ring."""
    x, z, w, d, h, f, _ = _thing(name)
    parts = []
    for u in (-0.15, 0.15):
        for v in (-0.15, 0.15):
            parts.append(obox((x + u, 0, z + v), (0.025, h - 0.08, 0.025), 0, {'all': BLACK}))
    parts.append(obox((x, 0.3, z), (0.34, 0.02, 0.34), 0, {'all': BLACK}))
    parts.append(obox((x, h - 0.08, z), (0.42, 0.08, 0.42), 0, {'all': (120, 132, 146), 'top': (138, 150, 164)}))
    parts.append(obox((x, h, z - 0.18), (0.4, 0.2, 0.06), 0, {'all': (120, 132, 146)}))
    return parts


def shaker(cam, p, pts4, col, handle=True, vertical=True):
    """A shaker door or drawer front: a recessed centre panel and a brass bar handle."""
    a, b, c, d = pts4
    def L(u, v):
        return tuple(a[i] + (b[i] - a[i]) * u + (d[i] - a[i]) * v for i in range(3))
    cam.poly(p, [L(0.12, 0.1), L(0.88, 0.1), L(0.88, 0.9), L(0.12, 0.9)], dk(col, 0.94), INK, 1.0)
    if handle:
        if vertical:
            cam.poly(p, [L(0.84, 0.55), L(0.88, 0.55), L(0.88, 0.8), L(0.84, 0.8)], BRASS, INK, 1.0)
        else:
            cam.poly(p, [L(0.35, 0.78), L(0.65, 0.78), L(0.65, 0.84), L(0.35, 0.84)], BRASS, INK, 1.0)


def run_parts(x0, x1, z0, z1, front_n, h=0.92, top=SLATE, top_d=SLATE_D, body=UNIT, sink=None, hob=None, island=False):
    """A run of base units with a slate-effect worktop (veined), shaker doors and drawers along its front."""
    front_axis = 'z' if front_n[0] == 0 else 'x'
    def fronts(img, cam, p):
        if front_axis == 'z':
            fz = z1 + 0.003 if front_n[2] > 0 else z0 - 0.003
            n = max(1, int(round((x1 - x0) / 0.6)))
            w = (x1 - x0) / n
            for i in range(n):
                a, b = x0 + i * w + 0.01, x0 + (i + 1) * w - 0.01
                shaker(cam, p, [(a, 0.12, fz), (b, 0.12, fz), (b, 0.62, fz), (a, 0.62, fz)], body)
                shaker(cam, p, [(a, 0.66, fz), (b, 0.66, fz), (b, h - 0.06, fz), (a, h - 0.06, fz)], body, vertical=False)
        else:
            fx = x1 + 0.003 if front_n[0] > 0 else x0 - 0.003
            n = max(1, int(round((z1 - z0) / 0.6)))
            w = (z1 - z0) / n
            for i in range(n):
                a, b = z0 + i * w + 0.01, z0 + (i + 1) * w - 0.01
                shaker(cam, p, [(fx, 0.12, a), (fx, 0.12, b), (fx, 0.62, b), (fx, 0.62, a)], body)
                shaker(cam, p, [(fx, 0.66, a), (fx, 0.66, b), (fx, h - 0.06, b), (fx, h - 0.06, a)], body, vertical=False)
    def veins(img, cam, p):
        rng = np.random.default_rng(int(abs(x0 * 10 + z0 * 7)))
        for _ in range(int((x1 - x0) * (z1 - z0) * 6) + 2):
            sx, sz = rng.uniform(x0, x1), rng.uniform(z0, z1)
            cam.line(p, [(sx, h + 0.001, sz), (min(x1, sx + rng.uniform(0.1, 0.4)), h + 0.001, min(z1, max(z0, sz + rng.uniform(-0.1, 0.1))))],
                     SLATE_L, 1.2)
        if sink:
            sx, sz, sw, sd = sink
            cam.poly(p, [(sx - sw / 2, h + 0.002, sz - sd / 2), (sx + sw / 2, h + 0.002, sz - sd / 2),
                         (sx + sw / 2, h + 0.002, sz + sd / 2), (sx - sw / 2, h + 0.002, sz + sd / 2)], STEEL_D, INK, 1.4)
            cam.poly(p, [(sx - sw / 2 + 0.03, h + 0.003, sz - sd / 2 + 0.03), (sx + sw / 2 - 0.03, h + 0.003, sz - sd / 2 + 0.03),
                         (sx + sw / 2 - 0.03, h + 0.003, sz + sd / 2 - 0.03), (sx - sw / 2 + 0.03, h + 0.003, sz + sd / 2 - 0.03)],
                     dk(STEEL_D, 0.8), INK, 1.2)
        if hob:
            hx, hz = hob
            cam.poly(p, [(hx - 0.3, h + 0.002, hz - 0.25), (hx + 0.3, h + 0.002, hz - 0.25), (hx + 0.3, h + 0.002, hz + 0.25),
                         (hx - 0.3, h + 0.002, hz + 0.25)], (24, 24, 28), INK, 1.4)
            for ox, oz, r in ((-0.15, -0.1, 0.09), (0.15, -0.1, 0.07), (-0.15, 0.12, 0.07), (0.15, 0.12, 0.09)):
                cam.poly(p, [(hx + ox + r * math.cos(a), h + 0.003, hz + oz + r * math.sin(a)) for a in np.linspace(0, 6.28, 14, endpoint=False)],
                         None, (90, 90, 96), 1.2)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    face_key = {(0, 0, 1): 'front', (0, 0, -1): 'back', (1, 0, 0): 'right', (-1, 0, 0): 'left'}[tuple(front_n)]
    parts = [obox((cx, 0.0, cz), (x1 - x0 - 0.08 * abs(front_n[0]), 0.1, z1 - z0 - 0.08 * abs(front_n[2])), 0, {'all': (40, 40, 44)}),
             obox((cx, 0.1, cz), (x1 - x0, h - 0.14, z1 - z0), 0, {'all': body, 'top': body}, extras={face_key: fronts}),
             obox((cx, h - 0.04, cz), (x1 - x0 + 0.04, 0.04, z1 - z0 + 0.04), 0, {'all': top_d, 'top': top}, extras={'top': veins})]
    if island:                                                # the island's overhang on the stool side and its tap
        pass
    return parts


def island_parts(props=None):
    """The island (refs kitchen-1, -2): deep grey-blue shaker cupboards, a thick slate-effect top overhanging on the
    stool (south) side; whatever stands on it (`props`: the film's beans, water, guns) drawn with it."""
    x, z, w, d, h, f, _ = _thing('island')
    parts = run_parts(x - w / 2, x + w / 2, z - d / 2 + 0.25, z + d / 2, (0, 0, 1), h, body=ISLAND)
    parts.append(obox((x, h - 0.05, z), (w + 0.08, 0.05, d + 0.04), 0, {'all': SLATE_D, 'top': SLATE}))
    if props:
        parts.append(props)
    return parts


def north_units_parts():
    """The north wall's run (left of the hall door, as seen from the island): base units, the worktop with the hob
    and the Alexa's spot, a marble splashback, an extractor hood and wall cupboards."""
    x, z, w, d, h, f, _ = _thing('north units')
    parts = run_parts(x - w / 2, x + w / 2, z - d / 2, z + d / 2, (0, 0, -1), h, hob=(x + 0.4, z))
    def splash(img, cam, p):
        zz = 5.4 - 0.004
        rng = np.random.default_rng(11)
        for _ in range(9):
            sx = rng.uniform(x - w / 2, x + w / 2)
            cam.line(p, [(sx, h + 0.05, zz), (sx + rng.uniform(-0.3, 0.3), h + 0.25, zz), (sx + rng.uniform(-0.4, 0.4), 1.5, zz)],
                     MARBLE_V, 1.4)
    parts.append(obox((x, h, 5.4 - 0.01), (w, 1.5 - h, 0.02), 0, {'all': MARBLE}, extras={'back': splash}))
    parts.append(obox((x + 0.4, 1.7, 5.4 - 0.25), (0.7, 0.35, 0.5), 0, {'all': STEEL, 'bottom': STEEL_D}))
    parts.append(obox((x + 0.4, 2.05, 5.4 - 0.12), (0.26, CEIL - 2.05, 0.24), 0, {'all': STEEL}))
    for x0, x1 in ((x - w / 2, x + 0.4 - 0.4), (x + 0.4 + 0.4, x + w / 2)):
        def doors(img, cam, p, x0=x0, x1=x1):
            n = max(1, int(round((x1 - x0) / 0.5)))
            ww = (x1 - x0) / n
            for i in range(n):
                a, b = x0 + i * ww + 0.01, x0 + (i + 1) * ww - 0.01
                shaker(cam, p, [(a, 1.6, 5.4 - 0.35 - 0.003), (b, 1.6, 5.4 - 0.35 - 0.003), (b, 2.5, 5.4 - 0.35 - 0.003),
                                (a, 2.5, 5.4 - 0.35 - 0.003)], UNIT)
        parts.append(obox(((x0 + x1) / 2, 1.58, 5.4 - 0.18), (x1 - x0, 0.95, 0.35), 0, {'all': UNIT, 'bottom': UNIT_D},
                          extras={'back': doors}))
    # a few things on the worktop (lived in): a knife block, a coffee machine
    parts.append(obox((x - 1.3, h, z), (0.12, 0.24, 0.14), 0, {'all': WALNUT}))
    # (Sam, 24 Oct: the bowl of lemons stood where the Alexa sits and popped into view as a yellow slab when the
    # Alexa went; it is gone from the set, so no shot shows it)
    parts.append(obox((x + 1.4, h, z + 0.05), (0.25, 0.36, 0.34), 0, {'all': (50, 50, 56), 'back': (70, 70, 76)}))
    return parts


def sink_run_parts():
    x, z, w, d, h, f, _ = _thing('sink run')
    return run_parts(x - w / 2, x + w / 2, z - d / 2, z + d / 2, (1, 0, 0), h, sink=(x, 2.7, 0.45, 0.8)) + [
        tap_parts(x - 0.24, 2.7, h)]


def tap_parts(x, z, h):
    f = Face([(x, h, z), (x, h + 0.3, z), (x + 0.2, h + 0.3, z)], None, None)
    f.draw = lambda img, cam, p: cam.line(p, [(x, h, z), (x, h + 0.32, z), (x + 0.18, h + 0.32, z), (x + 0.2, h + 0.22, z)],
                                          BRASS_D, 5.0)
    return [f]


def tall_units_parts():
    """The south wall's tall run: an American fridge-freezer in steel, two built-in ovens one over the other, larder
    cupboards (ref kitchen-2)."""
    x, z, w, d, h, f, _ = _thing('tall units')
    x0, x1, zf = x - w / 2, x + w / 2, z + d / 2
    def fronts(img, cam, p):
        fz = zf + 0.003
        fr0, fr1 = x0 + 0.05, x0 + 0.95                       # the fridge: two tall steel doors, a water dispenser
        cam.poly(p, [(fr0, 0.05, fz), (fr1, 0.05, fz), (fr1, 1.85, fz), (fr0, 1.85, fz)], STEEL, INK, 1.6)
        cam.line(p, [((fr0 + fr1) / 2, 0.05, fz + 0.001), ((fr0 + fr1) / 2, 1.85, fz + 0.001)], INK, 1.6)
        cam.poly(p, [(fr0 + 0.08, 1.05, fz + 0.002), (fr0 + 0.3, 1.05, fz + 0.002), (fr0 + 0.3, 1.35, fz + 0.002),
                     (fr0 + 0.08, 1.35, fz + 0.002)], (60, 64, 70), INK, 1.2)
        for hx in ((fr0 + fr1) / 2 - 0.05, (fr0 + fr1) / 2 + 0.05):
            cam.poly(p, [(hx - 0.01, 0.9, fz + 0.01), (hx + 0.01, 0.9, fz + 0.01), (hx + 0.01, 1.6, fz + 0.01),
                         (hx - 0.01, 1.6, fz + 0.01)], STEEL_D, INK, 1.0)
        cam.poly(p, [(fr0 + 0.5, 0.3, fz + 0.002), (fr0 + 0.6, 0.3, fz + 0.002), (fr0 + 0.85, 1.7, fz + 0.002),
                     (fr0 + 0.75, 1.7, fz + 0.002)], STEEL_L, None)
        ov0, ov1 = x0 + 1.05, x0 + 1.65                       # two ovens
        for y0 in (0.75, 1.38):
            cam.poly(p, [(ov0, y0, fz), (ov1, y0, fz), (ov1, y0 + 0.58, fz), (ov0, y0 + 0.58, fz)], (30, 30, 34), INK, 1.4)
            cam.poly(p, [(ov0 + 0.06, y0 + 0.08, fz + 0.002), (ov1 - 0.06, y0 + 0.08, fz + 0.002), (ov1 - 0.06, y0 + 0.42, fz + 0.002),
                         (ov0 + 0.06, y0 + 0.42, fz + 0.002)], (58, 60, 66), INK, 1.0)
            cam.poly(p, [(ov0 + 0.06, y0 + 0.48, fz + 0.01), (ov1 - 0.06, y0 + 0.48, fz + 0.01), (ov1 - 0.06, y0 + 0.51, fz + 0.01),
                         (ov0 + 0.06, y0 + 0.51, fz + 0.01)], STEEL, INK, 1.0)
        for (a, b) in ((ov0, ov1),):
            shaker(cam, p, [(a, 0.1, fz), (b, 0.1, fz), (b, 0.7, fz), (a, 0.7, fz)], UNIT)
            shaker(cam, p, [(a, 2.0, fz), (b, 2.0, fz), (b, h - 0.05, fz), (a, h - 0.05, fz)], UNIT)
        n = 3                                                  # the larder: tall shaker doors
        w2 = (x1 - (x0 + 1.7)) / n
        for i in range(n):
            a, b = x0 + 1.7 + i * w2 + 0.01, x0 + 1.7 + (i + 1) * w2 - 0.01
            shaker(cam, p, [(a, 0.1, fz), (b, 0.1, fz), (b, 1.4, fz), (a, 1.4, fz)], UNIT)
            shaker(cam, p, [(a, 1.44, fz), (b, 1.44, fz), (b, h - 0.05, fz), (a, h - 0.05, fz)], UNIT)
        cam.poly(p, [(x0 + 0.95, 1.85, fz), (x0 + 1.0, 1.85, fz), (x0 + 1.0, h, fz), (x0 + 0.95, h, fz)], UNIT, INK, 1.0)
        shaker(cam, p, [(fr0, 1.9, fz), (fr1, 1.9, fz), (fr1, h - 0.05, fz), (fr0, h - 0.05, fz)], UNIT)
    return [obox((x, 0, z), (w, h, d), 0, {'all': UNIT, 'front': UNIT_D}, extras={'front': fronts})]


def stairs_parts():
    """The hallway stairs along its north wall, rising east to west: oak treads, white risers, a white balustrade
    with an oak handrail (seen through the kitchen door)."""
    x, z, w, d, h, f, _ = _thing('stairs')
    parts = []
    n = 13
    for i in range(n):
        tx = x + w / 2 - (i + 0.5) * w / n
        parts.append(obox((tx, 0, z), (w / n, (i + 1) * h / (n + 1), d), 0, {'all': SKIRT, 'top': OAK, 'front': SKIRT}))
    for i in range(0, n, 2):
        bx = x + w / 2 - (i + 0.5) * w / n
        parts.append(obox((bx, (i + 1) * h / (n + 1), z - d / 2 + 0.04), (0.03, 0.9, 0.03), 0, {'all': SKIRT}))
    rail = Face([(x + w / 2, 0.9, z - d / 2 + 0.04), (x - w / 2, h - 0.1, z - d / 2 + 0.04), (x, 1, z)], None, None)
    rail.draw = lambda img, cam, p: cam.line(p, [(x + w / 2, 0.9 + h / (n + 1), z - d / 2 + 0.04),
                                                 (x - w / 2, 0.9 + h, z - d / 2 + 0.04)], OAK_D, 7.0)
    parts.append([rail])
    return parts


def console_parts():
    return [obox((2.55, 0.0, 6.83), (0.9, 0.8, 0.3), 0, {'all': WALNUT, 'top': lt(WALNUT, 1.1)}),
            cylinder((2.25, 0.8, 6.83), 0.08, 0.22, {'side': (196, 196, 190), 'top': (60, 120, 70)}, n=12),
            obox((2.8, 0.8, 6.83), (0.2, 0.03, 0.14), 10, {'all': (40, 40, 44)})]


def pendant_parts(x, z, drop=1.0, r=0.14, broken=False):
    """A brass globe pendant on a black cord (ref kitchen-2). Broken (shot 12, Sam 24 Oct): the globe blown away, a
    jagged brass cap and the bare bulb holder left swinging on the cord."""
    y = CEIL - drop
    if broken:
        cord = Face([(x, CEIL, z), (x, y, z), (x + 0.01, y, z)], None, None)
        cord.draw = lambda img, cam, p: cam.line(p, [(x, CEIL, z), (x, y + r * 1.2, z)], BLACK, 2.0)
        cap = Face([(x, y, z), (x, y + r, z), (x + r, y, z)], None, None)
        def gb(img, cam, p):
            rim = [(x + r * 0.55 * math.cos(a), y + r * (1.05 - 0.25 * ((k * 5) % 3) / 2), z + r * 0.55 * math.sin(a))
                   for k, a in enumerate(np.linspace(0, 6.28, 10, endpoint=False))]
            blob3(img, cam, p, sphere_pts((x, y + r * 1.15, z), r * 0.45, 6, sy=0.6) + rim, BRASS, INK, 1.8)
            cam.poly(p, [(x - 0.02, y + r * 0.95, z), (x + 0.02, y + r * 0.95, z), (x + 0.02, y + r * 0.7, z),
                         (x - 0.02, y + r * 0.7, z)], (60, 58, 56), INK, 1.2)
        cap.draw = gb
        return [[cord], [cap]]
    cord = Face([(x, CEIL, z), (x, y, z), (x + 0.01, y, z)], None, None)
    cord.draw = lambda img, cam, p: cam.line(p, [(x, CEIL, z), (x, y + r, z)], BLACK, 2.0)
    globe = Face([(x, y, z), (x, y + r, z), (x + r, y, z)], None, None)
    def g(img, cam, p):
        blob3(img, cam, p, sphere_pts((x, y + r * 0.6, z), r, 8, sy=0.85), BRASS, INK, 1.8)
        blob3(img, cam, p, sphere_pts((x - r * 0.3, y + r * 0.9, z - r * 0.3), r * 0.25, 5), lt(BRASS, 1.25), None, 0)
        cam.poly(p, [(x + r * 0.7 * math.cos(a), y + r * 0.08, z + r * 0.7 * math.sin(a)) for a in np.linspace(0, 6.28, 12, endpoint=False)],
                 (255, 244, 200), INK, 1.2)
    globe.draw = g
    return [[cord], [globe]]


def door_leaf(name, angle):
    """A white four-panel door leaf in its doorway, opened `angle` degrees into its room (0 = shut). Returns its
    parts and its plan footprint (for sorting)."""
    o = PL.OPENINGS[name]
    h = o['hinge']
    other = o['span'][1] if abs(h - o['span'][0]) < 1e-6 else o['span'][0]
    leaf = abs(other - h)
    sg = 1 if other > h else -1                         # the leaf runs from the hinge towards +x (sg 1) or -x
    zw = o['wall'][1]
    into = -1 if o['swings'] in ('living room', 'kitchen') else 1          # both open south, into their room
    a = math.radians(angle)
    tip = (h + sg * leaf * math.cos(a), zw + into * leaf * math.sin(a))
    th = 0.04
    nx, nz = -(tip[1] - zw), (tip[0] - h)
    m = math.hypot(nx, nz) or 1
    nx, nz = nx / m * th / 2, nz / m * th / 2
    H = o['head'] - 0.01
    def panels(img, cam, p, side):
        for (u0, u1, v0, v1) in ((0.12, 0.88, 0.08, 0.45), (0.12, 0.88, 0.52, 0.92)):
            pts = []
            for u, v in ((u0, v0), (u1, v0), (u1, v1), (u0, v1)):
                bx, bz = h + (tip[0] - h) * u, zw + (tip[1] - zw) * u
                pts.append((bx + side * nx * 1.05, H * v, bz + side * nz * 1.05))
            cam.poly(p, pts, DOOR_D, INK, 1.2)
        u = 0.9
        bx, bz = h + (tip[0] - h) * u, zw + (tip[1] - zw) * u
        cam.poly(p, [(bx + side * nx * 2.5, 0.98, bz + side * nz * 2.5), (bx + side * nx * 2.5, 1.02, bz + side * nz * 2.5),
                     (bx + side * nx * 2.5 - (tip[0] - h) * 0.12, 1.02, bz + side * nz * 2.5 - (tip[1] - zw) * 0.12),
                     (bx + side * nx * 2.5 - (tip[0] - h) * 0.12, 0.98, bz + side * nz * 2.5 - (tip[1] - zw) * 0.12)], BRASS, INK, 1.0)
    faces = []
    for side in (1, -1):
        pts = [(h + side * nx, 0.01, zw + side * nz), (tip[0] + side * nx, 0.01, tip[1] + side * nz),
               (tip[0] + side * nx, H, tip[1] + side * nz), (h + side * nx, H, zw + side * nz)]
        faces.append(Face(pts, (side * nx, 0, side * nz), DOOR, INK, 1.8, extra=lambda img, cam, p, s=side: panels(img, cam, p, s)))
    faces.append(Face([(tip[0] + nx, 0.01, tip[1] + nz), (tip[0] - nx, 0.01, tip[1] - nz), (tip[0] - nx, H, tip[1] - nz),
                       (tip[0] + nx, H, tip[1] + nz)], (tip[0] - h, 0, tip[1] - zw), DOOR_D, INK, 1.6))
    foot = [(h, zw), (tip[0], tip[1])]
    return [faces], foot


# ------------------------------------------------------------------------------------------------ the house plan
def furniture():
    """Every fixed piece as (name, room, plan footprint (polygon), parts-maker)."""
    def rect(name, pad=0.0):
        x, z, w, d, h, f, _ = _thing(name)
        if f % 180 == 90:
            w, d = d, w
        if f % 90:
            a = math.radians(f)
            hw, hd = w / 2 + pad, d / 2 + pad
            pts = [(-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd)]
            return [(x + u * math.cos(a) + v * math.sin(a), z - u * math.sin(a) + v * math.cos(a)) for u, v in pts]
        return [(x - w / 2 - pad, z - d / 2 - pad), (x + w / 2 + pad, z - d / 2 - pad), (x + w / 2 + pad, z + d / 2 + pad),
                (x - w / 2 - pad, z + d / 2 + pad)]
    out = [('sofa', 'living room', rect('sofa'), sofa_parts),
           ('armchair', 'living room', rect('armchair'), armchair_parts),
           ('coffee table', 'living room', rect('coffee table'), coffee_table_parts),
           ('media unit', 'living room', rect('media unit'), media_parts),
           ('drinks cabinet', 'living room', rect('drinks cabinet'), cabinet_parts),
           ('side table', 'living room', rect('side table'), side_table_parts),
           ('floor lamp', 'living room', rect('floor lamp'), lamp_parts),
           ('plant', 'living room', rect('plant'), plant_parts),
           ('north units', 'kitchen', rect('north units'), north_units_parts),
           ('sink run', 'kitchen', rect('sink run'), sink_run_parts),
           ('tall units', 'kitchen', rect('tall units'), tall_units_parts),
           ('stool 1', 'kitchen', rect('stool 1'), lambda: stool_parts('stool 1')),
           ('stool 2', 'kitchen', rect('stool 2'), lambda: stool_parts('stool 2')),
           ('stairs', 'hallway', rect('stairs'), stairs_parts),
           ('console', 'hallway', [(2.1, 6.68), (3.0, 6.68), (3.0, 6.98), (2.1, 6.98)], console_parts)]
    ix, iz = PL.THINGS['island']['at']
    for k, dx in enumerate((-0.7, 0.0, 0.7)):
        out.append((f'pendant {k}', 'kitchen', [(ix + dx - 0.1, iz - 0.1), (ix + dx + 0.1, iz - 0.1), (ix + dx + 0.1, iz + 0.1),
                                                 (ix + dx - 0.1, iz + 0.1)],
                    lambda dx=dx, broken=False: pendant_parts(ix + dx, iz, 0.7, broken=broken)))
    out.append(('living pendant', 'living room', [(2.9, 2.6), (3.1, 2.6), (3.1, 2.8), (2.9, 2.8)],
                lambda: pendant_parts(3.0, 2.7, 0.6, 0.2)))
    return out


FURNITURE = furniture()
_PART_CACHE = {}


def _parts(name, maker):
    if name not in _PART_CACHE:
        _PART_CACHE[name] = maker()
    return _PART_CACHE[name]


# ------------------------------------------------------------------------------------------------ sorting
def _seg_hits_poly(a, b, poly):
    """Does the plan segment a-b cross (or end inside) the polygon?"""
    def inside(pt):
        c = False
        n = len(poly)
        for i in range(n):
            (x1, z1), (x2, z2) = poly[i], poly[(i + 1) % n]
            if (z1 > pt[1]) != (z2 > pt[1]) and pt[0] < (x2 - x1) * (pt[1] - z1) / ((z2 - z1) or 1e-9) + x1:
                c = not c
        return c
    if len(poly) >= 3 and inside(b):
        return False                                     # the target stands inside it: no help from this test
    def cross(p1, p2, p3, p4):
        def o(a_, b_, c_):
            return (b_[0] - a_[0]) * (c_[1] - a_[1]) - (b_[1] - a_[1]) * (c_[0] - a_[0])
        return (o(p1, p2, p3) * o(p1, p2, p4) < 0) and (o(p3, p4, p1) * o(p3, p4, p2) < 0)
    n = len(poly)
    edges = [(poly[i], poly[(i + 1) % n]) for i in range(n)] if n > 2 else [(poly[0], poly[1])]
    return any(cross(a, b, e0, e1) for e0, e1 in edges)


def _centre(poly):
    return (sum(q[0] for q in poly) / len(poly), sum(q[1] for q in poly) / len(poly))


def order(items, cam):
    """Items are dicts with 'foot' (plan polygon, or a segment for a door leaf, or a point list for a person's
    footprint) and 'draw'. Sorted so that anything standing between the camera and another is drawn after it."""
    c = (cam.pos[0], cam.pos[2])
    n = len(items)
    dist = [math.dist(c, _centre(it['foot'])) for it in items]
    before = [set() for _ in range(n)]                   # before[j]: items that must be drawn before j
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            # i occludes j: the line from the camera to j's centre crosses i's footprint, and not the other way
            if _seg_hits_poly(c, _centre(items[j]['foot']), items[i]['foot']) and \
                    not _seg_hits_poly(c, _centre(items[i]['foot']), items[j]['foot']):
                before[i].add(j)
    done, out = set(), []
    while len(out) < n:
        ready = [k for k in range(n) if k not in done and before[k] <= done]
        if not ready:                                    # a cycle: fall back to distance
            ready = [k for k in range(n) if k not in done]
        k = max(ready, key=lambda q: dist[q])
        done.add(k)
        out.append(items[k])
    return out


# ------------------------------------------------------------------------------------------------ the frame
def house(img, cam, t, actors=(), state=None):
    """Draw the house through `cam` at time t. `actors`: dicts with 'at' (x, z), 'r' (plan radius), 'draw' (img ->
    None), optional 'room' (forced) and 'foot'. `state`: doors {'living door': deg, 'kitchen door': deg}, 'glass'
    (broken panes), 'marks' (bullet holes and scorches, each with its time), 'island' (a draw for what stands on the
    island: one part with it), 'on' ({furniture name: a draw for what stands on it}), 'gone' (furniture names not
    drawn)."""
    state = state or {}
    here = room_of(cam.pos[0], cam.pos[2])
    if here == 'outside':
        here = 'living room'
    outside(img, cam, t)
    groups = {r: [] for r in list(PL.ROOMS) + ['outside']}
    for name, room, foot, maker in FURNITURE:
        if name in state.get('gone', ()):
            continue
        if name in state.get('broken', ()):                 # shot to pieces (a pendant)
            parts = _parts(name + ' broken', lambda maker=maker: maker(broken=True))
        else:
            parts = _parts(name, maker)
        on = state.get('on', {}).get(name)                  # what stands on it (the dish rack on the sink run)
        groups[room].append(dict(foot=foot, draw=lambda im, parts=parts, on=on: (draw_parts(im, cam, parts),
                                                                               on and on(im, cam))))
    if state.get('island'):
        ix, iz, w, d, h, f, _ = _thing('island')
        isl = island_parts()
        groups['kitchen'].append(dict(foot=[(ix - w / 2, iz - d / 2), (ix + w / 2, iz - d / 2), (ix + w / 2, iz + d / 2),
                                            (ix - w / 2, iz + d / 2)],
                                      draw=lambda im: (draw_parts(im, cam, isl), state['island'](im, cam))))
    else:
        ix, iz, w, d, h, f, _ = _thing('island')
        isl = _parts('island', island_parts)
        groups['kitchen'].append(dict(foot=[(ix - w / 2, iz - d / 2), (ix + w / 2, iz - d / 2), (ix + w / 2, iz + d / 2),
                                            (ix - w / 2, iz + d / 2)], draw=lambda im: draw_parts(im, cam, isl)))
    for dname, room in (('living door', 'living room'), ('kitchen door', 'kitchen')):
        ang = state.get('doors', {}).get(dname, 0.0)
        parts, foot = door_leaf(dname, ang)
        # a shut door sits in its wall: drawn with the room it faces when the camera is there, else the hallway
        groups[room].append(dict(foot=foot, draw=lambda im, parts=parts: draw_parts(im, cam, parts), door=True))
    for a in actors:
        r = a.get('room') or room_of(*a['at'])
        x, z = a['at']
        rr = a.get('r', 0.2)
        foot = a.get('foot') or [(x - rr, z - rr), (x + rr, z - rr), (x + rr, z + rr), (x - rr, z + rr)]
        # someone in a doorway or opening of the camera's room is drawn with it (after its walls)
        if r != here and _near_opening(x, z, here):
            r = here
        groups.setdefault(r, []).append(dict(foot=foot, draw=a['draw']))
    p = pen(img)
    for it in order(groups['outside'], cam):
        it['draw'](img)
    others = [r for r in PL.ROOMS if r != here]
    others.sort(key=lambda r: -math.dist((cam.pos[0], cam.pos[2]), _room_centre(r)))
    for r in others:
        floor(img, cam, p, r)
        ceiling(img, cam, p, r)
        walls(img, cam, r, state.get('marks', ()), state.get('glass'), t)
        for it in order(groups[r], cam):
            it['draw'](img)
    floor(img, cam, p, here)
    for m in state.get('floor_marks', ()):
        if t >= m['t']:
            m['draw'](img, cam, p, t)
    ceiling(img, cam, p, here)
    walls(img, cam, here, state.get('marks', ()), state.get('glass'), t)
    for it in order(groups[here], cam):
        it['draw'](img)


def _room_centre(r):
    x0, z0, x1, z1 = PL.ROOMS[r]
    return ((x0 + x1) / 2, (z0 + z1) / 2)


def _near_opening(x, z, room):
    x0, z0, x1, z1 = PL.ROOMS[room]
    for name, o in PL.OPENINGS.items():
        if o['sill'] > 0.5:
            continue
        axis, v = o['wall']
        s0, s1 = o['span']
        if axis == 'z' and s0 - 0.1 <= x <= s1 + 0.1 and abs(z - v) < 0.35 and x0 <= x <= x1 and (z0 - 0.4 <= z <= z1 + 0.4):
            return True
        if axis == 'x' and s0 - 0.1 <= z <= s1 + 0.1 and abs(x - v) < 0.35 and z0 <= z <= z1 and (x0 - 0.4 <= x <= x1 + 0.4):
            return True
    return False


def cam_of(shot, t=0.0):
    """The plan's camera for a shot (moving shots at time t from 0 to 1 along their path; the loop at t seconds)."""
    c = PL.CAMS[shot]
    if 'pos' in c:
        return Cam(c['pos'], c['look'])
    if 'orbit' in c:
        o = c['orbit']
        pos = PL.orbit_pos(t, o)
        return Cam(pos, (o['centre'][0], c['look_y'], o['centre'][1]))
    pts = PL.smooth(c['path'])
    i = min(len(pts) - 1, int(t * (len(pts) - 1)))
    return Cam(pts[i], c['look'])


def test(out):
    B.SS = 1
    shots = [(1, 0), (5, 0), (6, 0), (6, 1), (8, 1), (9, 0), (10, 0), (11, 1), (12, 0.0), (12, 1.75), (12, 3.5), (12, 5.25)]
    tiles = []
    for s, u in shots:
        img = B.canvas((255, 255, 255))
        cam = cam_of(s, u)
        if s == 9:
            cam.focal = 760
        house(img, cam, 0.0, state={'doors': {'living door': 0, 'kitchen door': 0}})
        im = img.convert('RGB').resize((270, 480))
        ImageDraw.Draw(im).text((8, 8), f'shot {s} {u}', fill=(255, 0, 0))
        tiles.append(im)
    sheet = Image.new('RGB', (270 * 6, 480 * 2), 'white')
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
    sheet.save(out, quality=86)
    print('saved', out)


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'test':
        test(sys.argv[2])
    else:
        print(__doc__)
