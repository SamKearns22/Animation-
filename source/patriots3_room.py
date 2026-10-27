#!/usr/bin/env python3
"""Patriots 3: the casemate's inside, drawn once from the plan (patriots3_plan) and seen through every shot's camera.

Refs (references/patriots-3/): room-1 (raw concrete walls with the formwork's vertical joints, a ribbed ceiling, the
bright slit), room-2 (a bunker room: concrete, cables along the walls, a caged lamp, a steel door frame onto a lit
passage), bunker-1..4 (the casemate, the embrasure). The painter is handed to sets.house, which draws the passage and
the beach through their openings (rule 2) and the room over them. Lighting is flat (house style): the walls facing
the slit are lit, the slit wall itself is in shadow, the ceiling darkest.

    python3 source/patriots3_room.py sheet OUT.jpg      the room from four of the film's cameras, empty
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
import patriots3_bunker as K     # noqa: E402
from ed import INK               # noqa: E402

LIT = (150, 146, 134)            # the back (south) wall, facing the slit
SIDE = (122, 118, 108)           # the east and west walls
SHADE = (92, 90, 84)             # the slit wall's inner face (backlit)
CEIL_C, BEAM, BEAM_D = (98, 96, 90), (82, 80, 76), (64, 62, 60)
FLOOR, FLOOR_D = (104, 100, 92), (96, 92, 85)
JOINT = (0, 0, 0, 0)
PASS_WALL, PASS_FLOOR, PASS_CEIL = (164, 160, 148), (128, 124, 114), (118, 114, 106)
STEEL, STEEL_D = (70, 72, 74), (48, 50, 52)
WOOD, WOOD_D = (126, 104, 70), (96, 78, 52)
OLIVE = (88, 92, 70)
BRASS = (204, 162, 76)
WALL_T = PL.Z_OUT - PL.Z_IN      # the slit wall is 0.7 m thick
DOOR_T = 0.4


def _ink(c, k):
    return tuple(int(v * k) for v in c[:3])


def wall_colour(n):
    if n[2] < 0:
        return SHADE              # faces south: the slit wall (inner face)
    if n[2] > 0:
        return LIT
    return SIDE


def _wall_details(img, cam, p, key, n, a0, a1, col, seed):
    """Formwork: the vertical joints between the shutter panels (room-1: dark seams about every 0.6 m), faint board
    lines across, and a few damp stains: so no wall is ever a blank flat colour."""
    rng = np.random.default_rng(seed)
    pieces = S.wall_pieces(PLAN, key, a0, a1)

    def on_wall(a, y):
        return any(b0 <= a <= b1 and y0 <= y <= y1 for b0, b1, y0, y1, _ in pieces)
    a = a0 + rng.uniform(0.45, 0.6)
    while a < a1 - 0.1:                                 # the panel joints, broken where an opening cuts the wall
        ys = [y for y in np.linspace(0.0, PL_CEIL, 25) if on_wall(a, y)]
        if ys:
            runs, cur = [], [ys[0]]
            for y in ys[1:]:
                if y - cur[-1] < 0.11:
                    cur.append(y)
                else:
                    runs.append(cur)
                    cur = [y]
            runs.append(cur)
            for r in runs:
                cam.line(p, [S.wpt(key, n, a, r[0], 0.003), S.wpt(key, n, a, r[-1], 0.003)], _ink(col, 0.62), 2.6)
        a += rng.uniform(0.55, 0.7)
    y = 0.3
    while y < PL_CEIL - 0.1:                            # board lines: faint, broken
        b = a0 + rng.uniform(0.0, 0.3)
        while b < a1 - 0.2:
            L = rng.uniform(0.4, 1.1)
            e = min(a1 - 0.05, b + L)
            if on_wall(b, y) and on_wall(e, y):
                cam.line(p, [S.wpt(key, n, b, y, 0.003), S.wpt(key, n, e, y + rng.uniform(-0.01, 0.01), 0.003)],
                         _ink(col, 0.86), 1.2)
            b = e + rng.uniform(0.2, 0.6)
        y += rng.uniform(0.25, 0.4)
    for k in range(3):                                  # damp stains, hand-cut
        ca, cy = rng.uniform(a0 + 0.3, a1 - 0.3), rng.uniform(0.2, 1.6)
        if not on_wall(ca, cy):
            continue
        r = rng.uniform(0.08, 0.2)
        pts = [S.wpt(key, n, ca + r * rng.uniform(0.7, 1.2) * math.cos(u), cy + r * 1.4 * rng.uniform(0.7, 1.2) * math.sin(u), 0.003)
               for u in np.linspace(0, 2 * math.pi, 9, endpoint=False)]
        cam.poly(p, pts, _ink(col, 0.9), None)


def _beams(img, cam, p, x0, z0, x1, z1):
    """The ribbed ceiling (room-1): steel beams across the room, about every 0.5 m, each a dark flange seen from below
    and its web's side."""
    parts = []
    z = z0 + 0.2
    while z < z1 - 0.1:
        parts.append(S.obox(((x0 + x1) / 2, PL_CEIL - 0.11, z), (x1 - x0, 0.11, 0.09), 0.0,
                            cols={'bottom': BEAM, 'front': BEAM_D, 'back': BEAM_D, 'left': BEAM_D, 'right': BEAM_D,
                                  'top': BEAM}, lw=1.6))
        z += 0.5
    S.draw_parts(img, cam, parts, p)


def _reveal(cam, p, name, depth, col):
    """An opening's reveal: the wall's real thickness round it (sides, sill, head), seen from inside the room."""
    o = PLAN.openings[name]
    axis, v = o['wall']
    s0, s1, sill, head = o['span'][0], o['span'][1], o.get('sill', 0.0), o['head']
    out = 1 if v > 0 else -1                            # which way is out (north wall: +z)
    if axis != 'z':
        return
    Q = lambda a, y, d: (a, y, v + out * d)
    for a in (s0, s1):
        cam.poly(p, [Q(a, sill, 0), Q(a, sill, depth), Q(a, head, depth), Q(a, head, 0)], _ink(col, 0.82), INK, 2.0)
    if sill > 0:
        cam.poly(p, [Q(s0, sill, 0), Q(s1, sill, 0), Q(s1, sill, depth), Q(s0, sill, depth)], _ink(LIT, 1.0), INK, 2.0)
    cam.poly(p, [Q(s0, head, 0), Q(s1, head, 0), Q(s1, head, depth), Q(s0, head, depth)], _ink(col, 0.6), INK, 2.0)


def _door_frame(cam, p):
    """The steel door frame (room-2): an angle-iron frame round the door, rivet heads, a sill plate."""
    o = PLAN.openings['door']
    s0, s1, head = o['span'][0], o['span'][1], o['head']
    z = o['wall'][1] + 0.004
    w = 0.07
    for a, b, y0, y1 in ((s0 - w, s0, 0.0, head + w), (s1, s1 + w, 0.0, head + w), (s0 - w, s1 + w, head, head + w)):
        cam.poly(p, [(a, y0, z), (b, y0, z), (b, y1, z), (a, y1, z)], STEEL, INK, 2.0)
    for a in (s0 - w / 2, s1 + w / 2):
        for y in np.arange(0.25, head, 0.42):
            (X, Y), k = cam.project((a, y, z))
            if cam.depth((a, y, z)) > 0.2:
                p.ell(X, Y, 0.011 * k, 0.011 * k, STEEL_D, None)
    cam.poly(p, [(s0, 0.004, z), (s1, 0.004, z), (s1, 0.004, z - 0.1), (s0, 0.004, z - 0.1)], STEEL, INK, 1.6)
    for a in (s0, s1):                                  # the door's own reveal through the back wall
        cam.poly(p, [(a, 0.0, z), (a, 0.0, z - DOOR_T), (a, head, z - DOOR_T), (a, head, z)], _ink(SIDE, 0.9), INK, 1.8)
    cam.poly(p, [(s0, head, z), (s1, head, z), (s1, head, z - DOOR_T), (s0, head, z - DOOR_T)], _ink(SIDE, 0.6), INK, 1.8)


def _cable(cam, p):
    """A cable run along the back and east walls just under the ceiling (room-2), on little clips."""
    y = PL_CEIL - 0.24
    x0, z0, x1, z1 = PLAN.rooms['casemate']
    pts = [(x0 + 0.05, y, z0 + 0.03), (x1 - 0.03, y, z0 + 0.03), (x1 - 0.03, y, z1 - 0.3)]
    cam.line(p, pts, (30, 30, 32), 4.0)
    cam.line(p, [(x1 - 0.03, y, z0 + 0.03), (x1 - 0.03, y + 0.2, z0 + 0.03)], (30, 30, 32), 4.0)


def lamp(cam, p, lit=1.0):
    """A caged bulkhead lamp over the door (room-2), a dim bulb behind a steel cage."""
    c = (0.65, 2.18, -2.4 + 0.07)
    if cam.depth(c) < 0.2:
        return
    (X, Y), k = cam.project(c)
    p.ell(X, Y, 0.09 * k, 0.07 * k, STEEL_D, INK, 1.6)
    p.ell(X, Y, 0.065 * k, 0.05 * k, (236, 214, 150) if lit else (150, 146, 130), INK, 1.2)
    for dx in (-0.03, 0.0, 0.03):
        p.line([(X + dx * k, Y - 0.05 * k), (X + dx * k, Y + 0.05 * k)], STEEL_D, 1.4)
    p.line([(X - 0.065 * k, Y), (X + 0.065 * k, Y)], STEEL_D, 1.4)


def _crates(img, cam, p):
    """Two wooden ammo crates stacked (front right, by the slit): plank lines, rope handles, steel corners."""
    th = PLAN.things['ammo crates']
    (cx, cz), (sx, sz, sy) = th['at'], th['size']
    parts = []
    for k, (dx, dz, h) in enumerate(((0.0, 0.0, 0.0), (0.03, -0.02, sy / 2))):
        cols = {'top': (140, 116, 78), 'front': WOOD, 'back': WOOD_D, 'left': WOOD_D, 'right': WOOD, 'bottom': WOOD_D}
        parts.append(S.obox((cx + dx, h, cz + dz), (sx * (1 - 0.06 * k), sy / 2 - 0.01, sz * (1 - 0.05 * k)),
                            4.0 * k, cols=cols))
    S.draw_parts(img, cam, parts, p)
    for h in (0.0, sy / 2):                             # plank lines and the rope handles on the faces we see
        for face_z, sgn in ((cz - sz / 2, -1), (cz + sz / 2, 1)):
            mid = ((cx, h + sy / 4, face_z))
            if cam.depth(mid) < 0.2 or (cam.pos[2] - face_z) * sgn < 0:
                continue
            for f in (0.33, 0.66):
                cam.line(p, [(cx - sx / 2 + 0.01, h + sy / 2 * f, face_z + sgn * 0.003),
                             (cx + sx / 2 - 0.01, h + sy / 2 * f, face_z + sgn * 0.003)], WOOD_D, 1.4)
        for face_x, sgn in ((cx - sx / 2, -1), (cx + sx / 2, 1)):
            if (cam.pos[0] - face_x) * sgn < 0:
                continue
            q = (face_x + sgn * 0.004, h + sy / 4 + 0.02, cz)
            if cam.depth(q) < 0.2:
                continue
            (X, Y), k = cam.project(q)
            p.ell(X, Y, 0.04 * k, 0.018 * k, None, (90, 74, 50), 2.0)


def _shelf(img, cam, p):
    """A plank shelf on two brackets on the east wall, the field telephone on it (bakelite case, handset on top)."""
    sh = PLAN.things['shelf']
    (sx_, sz_), y = sh['at'], sh['y']
    x = PLAN.rooms['casemate'][2]
    parts = [S.obox((x - 0.11, y, sz_), (0.22, 0.035, 1.0), 0.0, cols={'all': WOOD})]
    ph = PLAN.things['field telephone']
    pz = ph['at'][1]
    parts.append(S.obox((x - 0.12, y + 0.035, pz), (0.16, 0.12, 0.24), 0.0, cols={'all': (52, 44, 36)}))
    parts.append(S.obox((x - 0.12, y + 0.155, pz), (0.06, 0.035, 0.22), 0.0, cols={'all': (34, 30, 28)}))
    S.draw_parts(img, cam, parts, p)
    for dz in (-0.38, 0.38):                            # the brackets
        cam.line(p, [(x - 0.003, y - 0.18, sz_ + dz), (x - 0.18, y - 0.003, sz_ + dz)], STEEL_D, 3.0)


def _range_card(cam, p):
    """The range card pinned above the slit (ref bunker-1): a pale card, the coast sketched on it, range lines."""
    rc = PLAN.things['range card']
    (cx, cz), (w, _, h), y = rc['at'], rc['size'], rc['y']
    z = PL.Z_IN - 0.004
    cam.poly(p, [(cx - w / 2, y, z), (cx + w / 2, y, z), (cx + w / 2, y + h, z), (cx - w / 2, y + h, z)],
             (214, 206, 180), INK, 1.8)
    pts = [(cx - w / 2 + 0.03 + i * (w - 0.06) / 8, y + h * (0.55 + 0.12 * math.sin(i * 1.3)), z - 0.001) for i in range(9)]
    cam.line(p, pts, (70, 66, 60), 1.4)
    for i in range(1, 4):
        a = cx - w / 2 + i * w / 4
        cam.line(p, [(a, y + 0.03, z - 0.001), (a, y + h * 0.5, z - 0.001)], (150, 60, 50), 1.2)


def _floor_marks(cam, p):
    """Old spent cases swept against the slit wall under the gun, and a dark oil stain: the gun has fired all day."""
    rng = np.random.default_rng(31)
    x0, z0, x1, z1 = PLAN.rooms['casemate']
    for k in range(5):
        cx, cz = rng.uniform(x0 + 0.4, x1 - 0.4), rng.uniform(z0 + 0.4, z1 - 0.5)
        r = rng.uniform(0.08, 0.2)
        pts = [(cx + r * rng.uniform(0.7, 1.2) * math.cos(u), 0.002, cz + r * 0.8 * rng.uniform(0.7, 1.2) * math.sin(u))
               for u in np.linspace(0, 2 * math.pi, 10, endpoint=False)]
        cam.poly(p, pts, FLOOR_D, None)
    for k in range(46):                                 # brass cases (each 8 cm long), never two on top of each other
        x = rng.uniform(-0.25, 0.75)
        z = PL.Z_IN - abs(rng.normal(0.0, 0.32))
        a = rng.uniform(0, math.pi)
        d = (0.04 * math.cos(a), 0.0, 0.04 * math.sin(a))
        q0, q1 = (x - d[0], 0.006, z - d[2]), (x + d[0], 0.006, z + d[2])
        if cam.depth(q0) < 0.2 or cam.depth(q1) < 0.2:
            continue
        cam.line(p, [q0, q1], INK, 6.0)
        cam.line(p, [q0, q1], BRASS, 3.6)


def _trench(img, cam):
    """Daylight at the passage's east end: the open trench, sandbags, the grass bank, a grey sky."""
    w, h = img.size
    p = S.pen(img)
    img.paste((196, 198, 196, 255), (0, 0, w, h))
    gy = cam.project((cam.pos[0] + 30 * cam.f[0], 1.2, cam.pos[2] + 30 * cam.f[2]))[0][1]
    p.poly([(-50, gy), (1130, gy - 10), (1130, 2000), (-50, 2000)], (104, 124, 72), None)
    p.poly([(-50, gy + 60), (1130, gy + 40), (1130, 2000), (-50, 2000)], (112, 96, 72), None)
    rng = np.random.default_rng(5)
    for r in range(3):
        for c in range(14):
            x = -40 + c * 84 + (r % 2) * 42 + rng.uniform(-6, 6)
            y = gy + 40 + r * 34
            p.poly([(x, y), (x + 80, y - 4), (x + 84, y + 30), (x + 2, y + 32)], (176, 160, 120), INK, 1.6)


_BEACH = {}


def _beach(img, cam):
    """The beach seen through the slit (patriots3_bunker.beach_layer), laid out between this camera's horizon and the
    slit's outer sill edge (the bunker sits up on the bluff: the sand runs down to the foot of the sill), cached."""
    horizon = cam.project((cam.pos[0] + 2000.0 * cam.f[0], cam.pos[1], cam.pos[2] + 2000.0 * cam.f[2]))[0][1]
    o = PLAN.openings['slit']
    sill = max(cam.project((a, o['sill'], PL.Z_OUT))[0][1] for a in o['span'])
    h = int(max(horizon + 80, sill + 30))
    hz = int(max(10, horizon))
    key = (img.size, h, hz)
    if key not in _BEACH:
        _BEACH.clear()
        w = img.size[0] // B.SS
        lay = Image.new('RGBA', (w, 1920), K.SAND + (255,))
        lay.alpha_composite(K.beach_layer((w, min(1920, h)), hz), (0, 0))
        _BEACH[key] = lay.resize(img.size, Image.LANCZOS) if B.SS != 1 else lay
    img.alpha_composite(_BEACH[key])


def painter(t=0.0, flash=0.0):
    """paint(img, cam, space) for sets.house: the casemate, the passage, and outside (the beach, or the trench)."""
    def paint(img, cam, space):
        if space == 'outside':
            if cam.f[2] < 0:                            # looking south: out of the passage's east end
                _trench(img, cam)
            else:
                _beach(img, cam)
            return
        p = S.pen(img)
        x0, z0, x1, z1 = PLAN.rooms[space]
        if space == 'passage':
            cam.poly(p, [(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)], PASS_FLOOR, INK, 2.0)
            cam.poly(p, [(x0, PL_CEIL, z0), (x0, PL_CEIL, z1), (x1, PL_CEIL, z1), (x1, PL_CEIL, z0)], PASS_CEIL, INK, 2.0)
            for key, a0, a1, n in S.walls_of(PLAN, space):
                c = S.wpt(key, n, (a0 + a1) / 2, 1.2)
                if S._dot(n, S._sub(cam.pos, c)) <= 0:
                    continue
                for b0, b1, y0, y1, _ in S.wall_pieces(PLAN, key, a0, a1):
                    cam.poly(p, [S.wpt(key, n, b0, y0), S.wpt(key, n, b1, y0), S.wpt(key, n, b1, y1),
                                 S.wpt(key, n, b0, y1)], PASS_WALL if key[0] == 'z' else _ink(PASS_WALL, 0.9), INK, 2.0)
                _wall_details(img, cam, p, key, n, a0, a1, PASS_WALL, 70 + int(key[1] * 10))
            for x in (0.0, 1.6, 3.0):                   # passage lamps, the far end daylight
                lampc = (x, 2.1, -3.55)
                if cam.depth(lampc) > 0.2:
                    (X, Y), k = cam.project(lampc)
                    p.ell(X, Y, 0.06 * k, 0.045 * k, (236, 214, 150), INK, 1.4)
            return
        cam.poly(p, [(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)], FLOOR, INK, 2.0)
        _floor_marks(cam, p)
        if cam.pos[1] < PL_CEIL:
            cam.poly(p, [(x0, PL_CEIL, z0), (x0, PL_CEIL, z1), (x1, PL_CEIL, z1), (x1, PL_CEIL, z0)], CEIL_C, INK, 2.0)
        for key, a0, a1, n in S.walls_of(PLAN, space):
            c = S.wpt(key, n, (a0 + a1) / 2, 1.4)
            if S._dot(n, S._sub(cam.pos, c)) <= 0:
                continue
            col = wall_colour(n)
            for b0, b1, y0, y1, _ in S.wall_pieces(PLAN, key, a0, a1):
                cam.poly(p, [S.wpt(key, n, b0, y0), S.wpt(key, n, b1, y0), S.wpt(key, n, b1, y1), S.wpt(key, n, b0, y1)],
                         col, INK, 2.0)
            _wall_details(img, cam, p, key, n, a0, a1, col, 11 + int(abs(key[1]) * 10) + (0 if key[0] == 'x' else 50))
        if cam.pos[2] < PL.Z_IN:
            _reveal(cam, p, 'slit', WALL_T, SHADE)
        if cam.pos[2] > -2.4:
            _door_frame(cam, p)
        _beams(img, cam, p, x0, z0, x1, z1)
        _cable(cam, p)
        lamp(cam, p)
        _range_card(cam, p)
        _shelf(img, cam, p)
        _crates(img, cam, p)
    return paint


import plan as _PLN               # noqa: E402
PLAN = _PLN.Plan(PL)
PL_CEIL = PL.CEIL


def draw(img, cam, t=0.0):
    """The set through `cam` (the room, the passage and the beach through their openings)."""
    S.house(img, cam, PLAN, t, paint=painter(t), here='casemate')


def foreground(img, cam):
    """For a camera inside the slit itself (shot 9): the slit's own reveal round the lens (sill, head, sides)."""
    if cam.pos[2] <= PL.Z_IN:
        return
    p = S.pen(img)
    o = PLAN.openings['slit']
    s0, s1, sill, head = o['span'][0], o['span'][1], o['sill'], o['head']
    z0, z1 = PL.Z_IN, cam.pos[2] + 0.4
    cam.poly(p, [(s0 - 2, sill, z0), (s1 + 2, sill, z0), (s1 + 2, sill, z1), (s0 - 2, sill, z1)], (132, 128, 118), INK, 2.4)
    cam.poly(p, [(s0 - 2, sill, z0), (s1 + 2, sill, z0), (s1 + 2, sill - 1.5, z0), (s0 - 2, sill - 1.5, z0)], SHADE, INK, 2.4)
    cam.poly(p, [(s0 - 2, head, z0), (s1 + 2, head, z0), (s1 + 2, head, z1), (s0 - 2, head, z1)], (60, 58, 54), INK, 2.4)
    cam.poly(p, [(s0 - 2, head, z0), (s1 + 2, head, z0), (s1 + 2, head + 1.5, z0), (s0 - 2, head + 1.5, z0)], SHADE, INK, 2.4)
    for a, out in ((s0, -1), (s1, 1)):
        cam.poly(p, [(a, sill - 1, z0), (a, head + 1, z0), (a, head + 1, z1), (a, sill - 1, z1)], (78, 76, 70), INK, 2.4)
        cam.poly(p, [(a, sill - 1.5, z0), (a + out * 3, sill - 1.5, z0), (a + out * 3, head + 1.5, z0), (a, head + 1.5, z0)],
                 SHADE, INK, 2.4)


def sheet(out):
    from PIL import ImageDraw
    B.SS = 1
    tiles = []
    for name in ('s2', 's3', 's5', 's8', 's9 start'):
        c = PL.CAMS[name]
        cam = S.Cam(c['pos'], c['look'], focal=c['focal'])
        img = B.canvas((255, 255, 255))
        draw(img, cam)
        foreground(img, cam)
        tiles.append(img.convert('RGB').resize((432, 768)))
    W = Image.new('RGB', (432 * len(tiles) + 10 * (len(tiles) + 1), 788), (235, 232, 226))
    for i, t in enumerate(tiles):
        W.paste(t, (10 + i * 442, 10))
    W.save(out, quality=86)
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
