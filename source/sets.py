#!/usr/bin/env python3
"""sets: the shared 3D set, built from the film's plan (plan.py): the camera and shapes every set uses, the portal
(rule 2) and the set's solids for the collision audit (rule 12).

Why: each film built its rooms on its own (power_crime_set, poker_mon_room, prepper_set), so a doorway could show a
flat colour (Power Crime), and the collision audit only knew what a film remembered to hand it (Prepper note 47: Wes
backed through a door frame the audit had never heard of). Built once here, from the plan, every film gets both.

  Cam(pos, at, focal)             a perspective camera (plan handedness: looking north, east is screen right); poly()
                                  clips at the near plane; project() gives the frame point and pixels per metre
  Face, obox, cylinder, blob3, draw_parts, jit, dk, lt     the house style's shapes (flat fills, one outline, hand-cut)
  house(img, cam, plan, t, paint) the portal: the camera's room, and through every doorway and window in sight the
                                  real next room (its floor, walls, colours and whatever the film paints in it), clipped
                                  to the opening, room behind room; an opening onto the outside shows the film's
                                  outside (paint(img, cam, 'outside', clip)). paint(img, cam, room) draws a room's
                                  contents; plain_room() is the default (LOOKS colours, every THING as a box: enough
                                  for the rough composition sheet, rule 11)
  solids(film)                    every wall (cut round its openings), door frame, door leaf (at film.door_angles(t))
                                  and THING as audit Things: audit.py adds them to every frame by itself (rule 12);
                                  a film lists only what to leave out: SET_EXCLUDE = [(name pattern, why)]
  portal_faults(film)             each opening on screen in each shot must show something, never one flat colour

    python3 source/sets.py FILM sketch OUT.jpg [SHOT ...]   each shot's camera on the plain set (portals working)
"""
import fnmatch
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
from ed import INK               # noqa: E402

FLAT = B.Cam(1.0, 540, 960)
WALL_LOOK = dict(floor=(196, 186, 168), wall=(232, 226, 214), ceiling=(246, 244, 238), thing=(170, 140, 110))
OUTSIDE_LOOK = dict(sky=(172, 200, 226), ground=(104, 150, 72))


# ------------------------------------------------------------------------------------------------ the camera

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



# ------------------------------------------------------------------------------------------------ the plan's rooms
def _plan(film_or_plan):
    import plan as PLN
    return film_or_plan if isinstance(film_or_plan, PLN.Plan) else PLN.of(film_or_plan)


def walls_of(P, room):
    """The room's four walls as ((axis, value), a0, a1, inward normal): axis 'z' = a wall along x at z = value."""
    x0, z0, x1, z1 = P.rooms[room]
    return [(('z', z0), x0, x1, (0, 0, 1)), (('z', z1), x0, x1, (0, 0, -1)),
            (('x', x0), z0, z1, (1, 0, 0)), (('x', x1), z0, z1, (-1, 0, 0))]


def wpt(key, n, a, y, off=0.0):
    """A point on a wall: a along it, y up it, `off` into the room."""
    axis, v = key
    return (a, y, v + n[2] * off) if axis == 'z' else (v + n[0] * off, y, a)


def wall_pieces(P, key, a0, a1):
    """The solid rectangles of one wall round its openings: [(a0, a1, y0, y1, label)]; a piece beside, above or below
    an opening is labelled as that opening's frame."""
    ops = sorted(((n, max(o['span'][0], a0), min(o['span'][1], a1), o.get('sill', 0.0), o.get('head', 2.0))
                  for n, o in P.openings.items() if tuple(o['wall']) == tuple(key)
                  and min(o['span'][1], a1) > max(o['span'][0], a0)), key=lambda q: q[1])
    wall = f'wall {key[0]}={key[1]:g}'
    out, pos, prev = [], a0, None
    for n, s0, s1, sill, head in ops:
        if s0 > pos:
            out.append((pos, s0, 0.0, P.ceil, f'{n} frame' if s0 - pos < 0.5 or prev else wall))
        out.append((s0, s1, head, P.ceil, f'{n} frame'))
        if sill > 0:
            out.append((s0, s1, 0.0, sill, f'{n} frame'))
        pos, prev = s1, n
    if a1 > pos:
        out.append((pos, a1, 0.0, P.ceil, f'{prev} frame' if prev and a1 - pos < 0.5 else wall))
    return out


def thing_box(th):
    """A THING as obox wants it: base centre, (width, height, depth) in its own frame, yaw (its tilt off the axes)."""
    import plan as PLN
    (cx, cz), (sx, sz, sy) = th['at'], th['size']
    return (cx, th.get('y', 0.0), cz), (sx, sy, sz), -PLN.tilt(th)


def plain_room(film_or_plan, looks=None):
    """The default painter: a room's floor, ceiling and walls (openings cut, their reveals drawn) in the plan's LOOKS
    colours, and every THING in it as a plain box; 'outside' is sky and ground. paint(img, cam, space)."""
    P = _plan(film_or_plan)
    looks = looks or P.looks

    def paint(img, cam, space):
        p = pen(img)
        if space == 'outside':
            lk = dict(OUTSIDE_LOOK, **looks.get('outside', {}))
            img.paste(tuple(lk['sky']) + (255,), (0, 0) + img.size)
            far = 60.0
            cx, cz = cam.pos[0], cam.pos[2]
            cam.poly(p, [(cx - far, 0, cz - far), (cx + far, 0, cz - far), (cx + far, 0, cz + far), (cx - far, 0, cz + far)],
                     tuple(lk['ground']), None)
            return
        lk = dict(WALL_LOOK, **looks.get(space, {}))
        x0, z0, x1, z1 = P.rooms[space]
        cam.poly(p, [(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)], tuple(lk['floor']), INK, 2.0)
        if cam.pos[1] < P.ceil:
            cam.poly(p, [(x0, P.ceil, z0), (x0, P.ceil, z1), (x1, P.ceil, z1), (x1, P.ceil, z0)], tuple(lk['ceiling']), INK, 2.0)
        for key, a0, a1, n in walls_of(P, space):
            c = wpt(key, n, (a0 + a1) / 2, 1.4)
            if _dot(n, _sub(cam.pos, c)) <= 0:
                continue
            for b0, b1, y0, y1, _ in wall_pieces(P, key, a0, a1):
                cam.poly(p, [wpt(key, n, b0, y0), wpt(key, n, b1, y0), wpt(key, n, b1, y1), wpt(key, n, b0, y1)],
                         tuple(lk['wall']), INK, 2.0)
            for name, o in P.openings.items():                # the reveals: the wall's thickness in each opening
                if tuple(o['wall']) != tuple(key):
                    continue
                s0, s1, sill, head = o['span'][0], o['span'][1], o.get('sill', 0.0), o.get('head', 2.0)
                for a in (s0, s1):
                    cam.poly(p, [wpt(key, n, a, sill), wpt(key, n, a, sill, -P.wall_t), wpt(key, n, a, head, -P.wall_t),
                                 wpt(key, n, a, head)], dk(tuple(lk['wall']), 0.88), INK, 1.6)
        parts = []
        for name, th in P.things.items():
            if P.room_of(*th['at']) == space:
                c, size, yaw = thing_box(th)
                parts.append(obox(c, size, yaw, {'all': tuple(lk.get('things', {}).get(name, lk['thing']))}))
        draw_parts(img, cam, parts, p)
    return paint


# ------------------------------------------------------------------------------------------------ the portal (rule 2)
def opening_quad(P, name):
    """An opening's four corners in the world (on its wall's plane)."""
    o = P.openings[name]
    axis, v = o['wall']
    s0, s1, sill, head = o['span'][0], o['span'][1], o.get('sill', 0.0), o.get('head', 2.0)
    if axis == 'z':
        return [(s0, sill, v), (s1, sill, v), (s1, head, v), (s0, head, v)]
    return [(v, sill, s0), (v, sill, s1), (v, head, s1), (v, head, s0)]


def _clip_poly(subject, clip):
    """Sutherland-Hodgman: the part of polygon `subject` inside the convex polygon `clip` (screen points)."""
    def inside(p, a, b, s):
        return s * ((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])) >= 0
    def meet(p, q, a, b):
        x1, y1, x2, y2, x3, y3, x4, y4 = p[0], p[1], q[0], q[1], a[0], a[1], b[0], b[1]
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(den) < 1e-12:
            return q
        u = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + u * (x2 - x1), y1 + u * (y2 - y1))
    area = sum(clip[i][0] * clip[(i + 1) % len(clip)][1] - clip[(i + 1) % len(clip)][0] * clip[i][1]
               for i in range(len(clip)))
    s = 1 if area > 0 else -1
    out = list(subject)
    for i in range(len(clip)):
        a, b = clip[i], clip[(i + 1) % len(clip)]
        inp, out = out, []
        for k in range(len(inp)):
            p, q = inp[k], inp[(k + 1) % len(inp)]
            if inside(q, a, b, s):
                if not inside(p, a, b, s):
                    out.append(meet(p, q, a, b))
                out.append(q)
            elif inside(p, a, b, s):
                out.append(meet(p, q, a, b))
        if not out:
            return []
    return out


def _area(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                   for i in range(len(poly)))) / 2


SCREEN = [(0, 0), (1080, 0), (1080, 1920), (0, 1920)]


def portals(cam, film_or_plan, here=None, depth=3):
    """What the camera sees through openings: [(space, opening, screen polygon, depth)], room behind room (up to
    `depth` openings deep). space is a room or 'outside'."""
    P = _plan(film_or_plan)
    here = here or P.room_of(cam.pos[0], cam.pos[2], 0.05)
    out = []

    def walk(room, clip, d, path):
        if d >= depth:
            return
        for name, o in P.openings.items():
            lo, hi = P.sides(name)
            if room not in (lo, hi):
                continue
            other = hi if lo == room else lo
            if other is None:
                other = 'outside'
            if other in path:
                continue
            quad = cam.clip(opening_quad(P, name))
            if len(quad) < 3:
                continue
            poly = _clip_poly(quad, clip)
            if len(poly) < 3 or _area(poly) < 4:
                continue
            out.append((other, name, poly, d + 1))
            if other != 'outside':
                walk(other, poly, d + 1, path | {other})
    if here is not None:
        walk(here, SCREEN, 0, {here})
    return out


def house(img, cam, film_or_plan, t=0.0, paint=None, here=None):
    """Draw the set through `cam`: every space seen through an opening first (deepest first), each clipped to its
    opening, then the camera's own room over them. paint(img, cam, space) draws a space (default plain_room)."""
    from PIL import ImageChops
    P = _plan(film_or_plan)
    paint = paint or plain_room(P)
    here = here or P.room_of(cam.pos[0], cam.pos[2], 0.05)
    for space, name, poly, d in sorted(portals(cam, P, here), key=lambda q: -q[3]):
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        paint(layer, cam, space)
        mask = Image.new('L', img.size, 0)
        ImageDraw.Draw(mask).polygon([(x * B.SS, y * B.SS) for x, y in poly], fill=255)
        layer.putalpha(ImageChops.multiply(layer.getchannel('A'), mask))
        img.alpha_composite(layer)
    if here is not None:
        paint(img, cam, here)


def portal_faults(film, per_shot=2):
    """Rule 2's check on the real picture: in each shot (at `per_shot` moments), every opening on screen shows
    something (more than one flat colour inside it), never a flat fill. Needs PLAN and cam_for(t) with a Cam."""
    P = _plan(film)
    if P is None or not P.openings:
        return []
    B.SS = 1
    out, seen = [], set()
    draw = getattr(film, 'picture', None) or film.frame_image
    for shot, s0, s1 in getattr(film, 'SHOTS', []):
        for k in range(per_shot):
            t = s0 + (s1 - s0) * (k + 0.5) / per_shot
            cam = film.cam_for(t)
            if not hasattr(cam, 'clip'):
                return [f'portal (rule 2): not checked: cam_for(t) is not a sets.Cam']
            im = None
            for space, name, poly, d in portals(cam, P):     # only what is really seen through each opening
                q = np.array(poly, float)
                c = q.mean(0)
                q = c + (q - c) * 0.7                          # inset: the frame and reveals are not the view
                x0, y0 = np.maximum(q.min(0), 0).astype(int)
                x1, y1 = np.minimum(q.max(0), (1080, 1920)).astype(int)
                if x1 - x0 < 12 or y1 - y0 < 12:
                    continue
                if im is None:
                    im = np.asarray(draw(t).convert('RGB').resize((1080, 1920))).astype(int)
                mask = Image.new('L', (1080, 1920), 0)
                ImageDraw.Draw(mask).polygon([tuple(p) for p in q.tolist()], fill=255)
                m = np.asarray(mask)[y0:y1, x0:x1] > 0
                px = im[y0:y1, x0:x1][m]
                if len(px) < 100:
                    continue
                med = np.median(px, 0)
                spread = np.abs(px - med).sum(1)
                lk = dict(OUTSIDE_LOOK if space == 'outside' else {}, **P.looks.get(space, {}))
                own = any(np.abs(med - np.asarray(c)).sum() <= 24 for k, c in lk.items()   # its own wall or sky seen
                          if k in ('wall', 'floor', 'sky', 'ground'))                       # square on is fine
                if (spread > 24).mean() < 0.02 and not own and (shot, name) not in seen:
                    seen.add((shot, name))
                    out.append(f'portal (rule 2): {t:.2f} s ({shot}): the {name} shows one flat colour '
                               f'{tuple(int(v) for v in np.median(px, 0))}: draw the {space} beyond it (sets.house)')
    return out


# ------------------------------------------------------------------------------------------------ solids (rule 12)
_STATIC = {}


def _excluded(film, name):
    return any(fnmatch.fnmatchcase(name.lower(), pat.lower()) for pat, *_ in getattr(film, 'SET_EXCLUDE', ()))


def _thing_solid(CC, name, th):
    """A THING as one solid: an axis box, or (turned off the axes) a rounded box laid as a thick card."""
    import plan as PLN
    (cx, cz), (sx, sz, sy) = th['at'], th['size']
    y0 = th.get('y', 0.0)
    a = math.radians(-PLN.tilt(th))
    if abs(a) < 1e-3:
        return CC.box(name, 'box', (cx - sx / 2, y0, cz - sz / 2), (cx + sx / 2, y0 + sy, cz + sz / 2))
    long_x = sx >= sz
    w, d = (sx, sz) if long_x else (sz, sx)
    r = d / 2
    ux = np.array((math.cos(a), 0.0, -math.sin(a))) if long_x else np.array((math.sin(a), 0.0, math.cos(a)))
    up = np.array((0.0, 1.0, 0.0))
    u = ux * max(0.0, w - 2 * r)
    v = up * max(0.0, sy - 2 * r)
    corner = np.array((cx, y0 + r, cz)) - u / 2
    return CC.card(name, 'box', corner, u, v, r)


def _door_leaf_solid(CC, P, name, angle):
    o = P.openings[name]
    axis, v = o['wall']
    h = o['hinge']
    other = o['span'][1] if abs(h - o['span'][0]) < 1e-6 else o['span'][0]
    leaf, sg = abs(other - h), (1 if other > h else -1)
    room = o.get('swings')
    into = 1
    if room in P.rooms:
        x0, z0, x1, z1 = P.rooms[room]
        into = 1 if ((z0 + z1) / 2 if axis == 'z' else (x0 + x1) / 2) > v else -1
    a = math.radians(angle)
    along, out = sg * leaf * math.cos(a), into * leaf * math.sin(a)
    if axis == 'z':
        base, u = np.array((h, 0.02, v)), np.array((along, 0.0, out))
    else:
        base, u = np.array((v, 0.02, h)), np.array((out, 0.0, along))
    return CC.card('DOOR ' + name.upper(), 'leaf', base, u, np.array((0.0, o.get('head', 2.0) - 0.04, 0.0)), 0.02)


def solids(film, t=0.0):
    """Rule 12: the set's solids at time t as audit Things (kind 'set'): every wall cut round its openings (pieces by
    an opening named as its frame), every THING, every door leaf at film.door_angles(t) ({name: degrees}, 0 = shut).
    Leaves out what SET_EXCLUDE names (each with its reason) and anything solid=False in the plan."""
    import audit as A
    import clipcheck as CC
    P = _plan(film)
    if P is None:
        return []
    key = id(film)
    if key not in _STATIC:
        walls, done = [], set()
        for room in P.rooms:
            for wkey, a0, a1, n in walls_of(P, room):
                for b0, b1, y0, y1, lab in wall_pieces(P, wkey, a0, a1):
                    k = (wkey, round(b0, 3), round(b1, 3), round(y0, 3), round(y1, 3))
                    if k in done:
                        continue
                    done.add(k)
                    tw = P.wall_t / 2
                    if wkey[0] == 'z':
                        lo, hi = (b0, y0, wkey[1] - tw), (b1, y1, wkey[1] + tw)
                    else:
                        lo, hi = (wkey[1] - tw, y0, b0), (wkey[1] + tw, y1, b1)
                    walls.append(CC.box('WALL', lab, lo, hi))
        things = [] if _excluded(film, 'WALL') else [A.Thing('WALL', walls, 'set')]
        for name, th in P.things.items():
            nm = name.upper()
            if th.get('solid', True) and not _excluded(film, nm):
                things.append(A.Thing(nm, [_thing_solid(CC, nm, th)], 'set'))
        _STATIC[key] = things
    out = list(_STATIC[key])
    angles = film.door_angles(t) if hasattr(film, 'door_angles') else {}
    for name, ang in angles.items():
        if name in P.openings and 'hinge' in P.openings[name] and not _excluded(film, 'DOOR ' + name.upper()):
            out.append(A.Thing('DOOR ' + name.upper(), [_door_leaf_solid(CC, P, name, ang)], 'set'))
    return out


def solids_faults(film):
    """What rule 12 needs and a film lacks, said out loud (never skipped in silence)."""
    P = _plan(film)
    if P is None:
        return []
    out = []
    if any('hinge' in o for o in P.openings.values()) and not hasattr(film, 'door_angles'):
        out.append('collision audit (rule 12): the plan has hinged doors but the film has no door_angles(t) '
                   '({door: degrees open}); their leaves are not tested')
    for pat, *why in getattr(film, 'SET_EXCLUDE', ()):
        if not why or not str(why[0]).strip():
            out.append(f'collision audit (rule 12): SET_EXCLUDE {pat} gives no reason')
    return out


def sketch(film, out, shots=None):
    """Each shot's camera on the plain set (plain_room), the portals at work, on one sheet."""
    P = _plan(film)
    B.SS = 1
    shots = shots or [s[0] for s in film.SHOTS]
    tiles = []
    for s in shots:
        t0, t1 = next(((a, b) for n, a, b in film.SHOTS if str(n) == str(s)), (0.0, 0.0))
        cam = film.cam_for((t0 + t1) / 2)
        img = B.canvas((255, 255, 255))
        house(img, cam, P)
        im = img.convert('RGB').resize((270, 480))
        ImageDraw.Draw(im).text((8, 8), f'shot {s}', fill=(255, 0, 0))
        tiles.append(im)
    cols = min(6, len(tiles))
    sheet = Image.new('RGB', (270 * cols, 480 * ((len(tiles) + cols - 1) // cols)), 'white')
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * 270, (i // cols) * 480))
    sheet.save(out, quality=86)
    return out


if __name__ == '__main__':
    import importlib
    a = sys.argv[1:]
    if len(a) >= 3 and a[1] == 'sketch':
        print('sheet:', sketch(importlib.import_module(a[0]), a[2], a[3:] or None))
    else:
        print(__doc__)
