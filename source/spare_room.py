"""The spare room, for the 'Merry Chr' shot (story/horror-merry-chr.md): a guest bedroom up under the roof of
the family's early 18th century house, with the old timbers kept and everything else new.

A pitched, vaulted ceiling in white plaster with its hand-hewn oak tie beams and ridge beam exposed; panelled
walls to dado height, a cornice where the walls meet the slope; varnished oak floorboards and an old Persian
rug; a mahogany bed with a tall panelled headboard against the left wall; a chest of drawers with a mirror over
it, a window with shutters and a writing desk on the right; and at the back right an open doorway to a
contemporary en-suite (white tiles, glass, bright light). The back wall is bare.

World coordinates: metres, y up, the floor at y = 0. We look in from the doorway (z = 0) towards the back
wall (z = BACK_Z); x runs to the right.
"""
import numpy as np

import sdf3d as S
from kitchen import shaker_panel
from materials import *  # noqa: F401,F403
from sdf3d import rot, UNION, SUNION, SSUB, SUB

HALF_W = 2.4                 # the side walls at x = -2.4 and 2.4
BACK_Z = -5.2
EAVES, RIDGE = 2.45, 3.90    # the walls rise to the eaves; the ceiling slopes up to the ridge
DADO = 0.86
BED = dict(x0=-2.36, x1=-0.30, z0=-3.65, z1=-2.05, top=0.66)      # the mattress
ENSUITE = (1.25, 2.15)       # the doorway to the en-suite, in the back wall (x from, to)
WINDOW = dict(z=-3.55, w=1.00, y0=0.80, y1=2.20)                  # in the right-hand wall
DRESSER_Z = -2.25          # the chest of drawers, on the right wall nearer the door than the window
RUG_AREA = dict(cx=0.30, cz=-2.75, hx=1.35, hz=0.95)


def wainscot(b, axis, fixed, a0, a1, face, skip=()):
    """Panelled walls to dado height along a wall: skirting, raised panels, a dado rail.
    axis: 'x' (a wall running along x at z = fixed) or 'z' (along z at x = fixed); face: +1/-1, which way the
    wall faces into the room. skip: (from, to) spans with no panelling (doorways)."""
    def box(c_along, y, along_half, hy, depth, mat=PAINT, r=0.002):
        if axis == 'x':
            b.box((c_along, y, fixed + face * depth), (along_half, hy, abs(depth) + 0.004), mat, op=UNION, r=r)
        else:
            b.box((fixed + face * depth, y, c_along), (abs(depth) + 0.004, hy, along_half), mat, op=UNION, r=r)
    spans = [(a0, a1)]
    for s0, s1 in skip:
        spans = [p for q in spans for p in ((q[0], min(q[1], s0)), (max(q[0], s1), q[1])) if p[1] - p[0] > 0.05]
    for p0, p1 in spans:
        c, h = (p0 + p1) / 2, (p1 - p0) / 2
        box(c, 0.09, h, 0.09, 0.012)                                   # skirting
        box(c, 0.185, h, 0.008, 0.018, r=0.004)                         # its moulded top
        box(c, DADO, h, 0.022, 0.020, r=0.006)                          # dado rail
        n = max(1, int(round((p1 - p0) / 0.62)))
        pw = (p1 - p0) / n
        for i in range(n):                                              # raised panels between them
            cc = p0 + (i + 0.5) * pw
            box(cc, 0.52, pw / 2 - 0.07, 0.24, 0.010, r=0.006)


def build_environment(b, SP):
    b.set_frame((0, 0, 0), None)
    W = HALF_W
    # --- floor, walls, the sloping ceiling
    b.group('floor', margin=0.03)
    b.box((0, -0.05, -2.4), (W + 0.3, 0.05, 3.4), BOARDS, op=UNION)
    b.group('walls', margin=0.05)
    zc, zh = (BACK_Z + 0.15) / 2, (0.15 - BACK_Z) / 2
    for sx in (-1, 1):
        b.box((sx * (W + 0.06), 1.6, zc), (0.06, 1.6, zh), WALL, op=UNION)
    b.box((0, 2.0, BACK_Z - 0.06), (W + 0.12, 2.0, 0.06), WALL, op=UNION)       # the gable end, bare
    b.box((0, 2.0, 0.08), (W + 0.12, 2.0, 0.08), WALL, op=UNION)                # the front, with the doorway
    b.box((0, 1.07, 0.08), (0.52, 1.07, 0.2), WALL, op=SUB)
    b.box((sum(ENSUITE) / 2, 1.07, BACK_Z - 0.06), ((ENSUITE[1] - ENSUITE[0]) / 2, 1.07, 0.2), WALL, op=SUB)
    b.box((W + 0.06, (WINDOW['y0'] + WINDOW['y1']) / 2, WINDOW['z']),
          (0.3, (WINDOW['y1'] - WINDOW['y0']) / 2, WINDOW['w'] / 2), WALL, op=SUB)
    b.group('ceiling', margin=0.05)
    ang = np.degrees(np.arctan2(RIDGE - EAVES, W))
    L = np.hypot(W, RIDGE - EAVES)
    for sx in (-1, 1):
        c = np.array([sx * W / 2, (EAVES + RIDGE) / 2, zc])
        n = np.array([sx * np.sin(np.radians(ang)), np.cos(np.radians(ang)), 0])
        b.box(c + n * 0.06, (L / 2 + 0.1, 0.06, zh + 0.1), CEILING, op=UNION, R=rot(0, 0, -sx * ang))
    # the old timbers: a ridge beam, two tie beams across the room with struts up to the slopes
    b.group('beams', margin=0.03)
    b.box((0, RIDGE - 0.08, zc), (0.11, 0.12, zh), BEAM, op=UNION, r=0.01)
    for z in (-1.55, -3.75):
        b.box((0, EAVES + 0.02, z), (W, 0.12, 0.11), BEAM, op=UNION, r=0.012)
        for sx in (-1, 1):
            a, c = np.array([sx * 0.25, EAVES + 0.12, z]), np.array([sx * 1.05, EAVES + 0.64, z])
            b.capsule(a, c, 0.075, BEAM, op=SUNION, k=0.02)
        b.box((0, (EAVES + RIDGE) / 2 + 0.02, z), (0.09, (RIDGE - EAVES) / 2, 0.09), BEAM, op=UNION, r=0.01)
    # a cornice where the walls meet the slope
    b.group('cornice', margin=0.03)
    for sx in (-1, 1):
        b.box((sx * (W - 0.05), EAVES - 0.05, zc), (0.06, 0.07, zh), PAINT, op=UNION, r=0.02)
    b.box((0, EAVES - 0.05, BACK_Z + 0.05), (W, 0.07, 0.06), PAINT, op=UNION, r=0.02)
    # panelled walls to dado height
    b.group('wainscot', margin=0.03)
    wainscot(b, 'x', BACK_Z, -W, W, 1, skip=(ENSUITE,))
    wainscot(b, 'z', -W, BACK_Z, 0.0, 1)
    wainscot(b, 'z', W, BACK_Z, 0.0, -1, skip=((WINDOW['z'] - WINDOW['w'] / 2 - 0.05, WINDOW['z'] + WINDOW['w'] / 2 + 0.05),))
    # door casings: the en-suite
    e0, e1 = ENSUITE
    for x in (e0 - 0.04, e1 + 0.04):
        b.box((x, 1.08, BACK_Z + 0.01), (0.045, 1.08, 0.025), PAINT, op=UNION, r=0.004)
    b.box(((e0 + e1) / 2, 2.19, BACK_Z + 0.01), ((e1 - e0) / 2 + 0.09, 0.045, 0.025), PAINT, op=UNION, r=0.004)
    window(b)
    ensuite(b)
    bed(b)
    dresser(b)
    desk(b)
    b.group('rug', margin=0.02)
    b.box((RUG_AREA['cx'], 0.006, RUG_AREA['cz']), (RUG_AREA['hx'], 0.006, RUG_AREA['hz']), RUG, op=UNION, r=0.004)
    SP[140:144] = (RUG_AREA['cx'], RUG_AREA['cz'], RUG_AREA['hx'], RUG_AREA['hz'])
    # the lantern hanging from the ridge beam, lit
    b.group('lantern', margin=0.03)
    lc = np.array([0.0, 2.55, -2.65])
    b.capsule(lc + [0, 0.18, 0], (0, RIDGE - 0.2, -2.65), 0.005, BLACKMETAL, op=UNION)
    for dx, dz in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        b.capsule(lc + [0.11 * dx, -0.16, 0.11 * dz], lc + [0.11 * dx, 0.14, 0.11 * dz], 0.008, BLACKMETAL,
                  op=UNION)
    b.cone(lc + [0, 0.14, 0], lc + [0, 0.22, 0], 0.17, 0.03, BLACKMETAL, op=UNION)
    b.box(lc + [0, -0.17, 0], (0.13, 0.012, 0.13), BLACKMETAL, op=UNION)
    b.sphere(lc, 0.04, BULB, op=UNION)
    return [lc]



def window(b):
    """A tall sash window in a deep panelled reveal, twelve panes over twelve, a sill, folded shutters; the
    snowy garden beyond; a wreath hung on it."""
    x = HALF_W
    z0, z1 = WINDOW['z'] - WINDOW['w'] / 2, WINDOW['z'] + WINDOW['w'] / 2
    y0, y1 = WINDOW['y0'], WINDOW['y1']
    b.group('outside', margin=0.05)
    b.box((x + 1.2, 1.6, WINDOW['z']), (0.02, 1.8, 1.6), SKY, op=UNION)
    b.group('window_frame', margin=0.02)
    xf = x + 0.09
    for z in np.linspace(z0, z1, 4):
        b.box((xf, (y0 + y1) / 2, z), (0.02, (y1 - y0) / 2, 0.014 if z0 < z < z1 else 0.03), PAINT, op=UNION)
    for y in np.linspace(y0, y1, 9):
        th = 0.03 if y in (y0, y1) or abs(y - (y0 + y1) / 2) < 1e-6 else 0.012
        b.box((xf, y, WINDOW['z']), (0.02, th, WINDOW['w'] / 2), PAINT, op=UNION)
    # the sill and the reveal's lining
    b.box((x - 0.03, y0 - 0.02, WINDOW['z']), (0.12, 0.022, WINDOW['w'] / 2 + 0.08), PAINT, op=UNION, r=0.006)
    for z in (z0 - 0.01, z1 + 0.01):
        b.box((x + 0.04, (y0 + y1) / 2, z), (0.05, (y1 - y0) / 2, 0.01), PAINT, op=UNION)
    # folded shutters against the reveal
    for z, sg in ((z0 - 0.03, -1), (z1 + 0.03, 1)):
        b.box((x - 0.035, (y0 + y1) / 2, z + sg * 0.02), (0.012, (y1 - y0) / 2, 0.10), PAINT, op=UNION, r=0.003)
    # a Christmas wreath on the window: fir, red berries, a red velvet bow
    b.group('wreath', disp=S.D_TREE, dparams=[0.010, 20.0, NEEDLES, x - 0.02, 1.62, WINDOW['z']], margin=0.03)
    wc = np.array([x - 0.05, 1.62, WINDOW['z']])
    b.torus(wc, 0.17, 0.05, NEEDLES, op=UNION, R=rot(0, 0, 90))
    rng = np.random.default_rng(3)
    for a in rng.uniform(0, 2 * np.pi, 14):
        b.sphere(wc + [-0.04, 0.17 * np.sin(a) + rng.normal(0, 0.02), 0.17 * np.cos(a) + rng.normal(0, 0.02)],
                 0.012, BAUBLE_RED, op=UNION)
    b.group('wreath_bow', margin=0.02)
    bw = wc + [-0.05, -0.17, 0]
    for sg in (-1, 1):
        b.ellipsoid(bw + [0, 0.02, sg * 0.05], (0.02, 0.035, 0.05), FELT, op=SUNION, k=0.01)
        b.capsule(bw, bw + [0, -0.16, sg * 0.05], 0.012, FELT, op=SUNION, k=0.01)


def ensuite(b):
    """Through the doorway at the back right: a bright, contemporary en-suite - white tiles, a frameless glass
    shower screen, a heated towel rail with a white towel, a pale stone floor."""
    e0, e1 = ENSUITE
    z0, z1 = BACK_Z - 0.12, BACK_Z - 2.2
    b.group('ensuite', margin=0.05)
    b.box(((e0 + e1) / 2 + 0.2, -0.05, (z0 + z1) / 2), (1.3, 0.05, 1.2), MARBLE, op=UNION)
    b.box(((e0 + e1) / 2 + 0.2, 1.3, z1 - 0.05), (1.3, 1.3, 0.05), TILE_W, op=UNION)
    b.box((e0 - 0.5, 1.3, (z0 + z1) / 2), (0.05, 1.3, 1.2), TILE_W, op=UNION)
    b.box((e1 + 0.9, 1.3, (z0 + z1) / 2), (0.05, 1.3, 1.2), TILE_W, op=UNION)
    b.box(((e0 + e1) / 2 + 0.2, 2.62, (z0 + z1) / 2), (1.3, 0.05, 1.2), CEILING, op=UNION)
    # heated towel rail on the left wall with a towel over it
    xr = e0 - 0.43
    for y in np.arange(0.45, 1.3, 0.09):
        b.capsule((xr, y, z1 + 0.35), (xr, y, z1 + 1.0), 0.010, STEEL, op=UNION)
    b.box((xr + 0.02, 1.02, z1 + 0.68), (0.018, 0.28, 0.24), LINEN, op=UNION, r=0.015)
    # the shower's glass screen (just its polished edge and fixing) and a rain head
    b.box((e1 + 0.2, 1.05, z1 + 0.9), (0.006, 1.0, 0.004), STEEL, op=UNION)
    b.cylinder((e1 + 0.5, 2.2, z1 + 0.35), 0.006, 0.12, STEEL, op=UNION)


def bed(b):
    """A mahogany bed: a tall panelled headboard with a shaped top against the left wall, turned posts, a low
    footboard; mattress and sheets (made up, before)."""
    B = BED
    zc, zh = (B['z0'] + B['z1']) / 2, (B['z1'] - B['z0']) / 2
    b.group('bed_frame', margin=0.03)
    # the rails
    b.box(((B['x0'] + B['x1']) / 2, 0.36, zc), ((B['x1'] - B['x0']) / 2, 0.12, zh + 0.03), DARKWOOD, op=UNION, r=0.01)
    # the headboard: a panelled board with a shaped (arched) top
    hx = -HALF_W + 0.05
    b.box((hx, 0.85, zc), (0.035, 0.55, zh + 0.07), DARKWOOD, op=UNION, r=0.01)
    b.cylinder((hx, 1.12, zc), 0.035, zh * 0.95, DARKWOOD, op=SUNION, k=0.02, R=rot(0, 0, 90))
    for dz in (-0.45, 0.0, 0.45):
        b.box((hx + 0.04, 1.02, zc + dz), (0.008, 0.28, 0.17), DARKWOOD, op=SUNION, k=0.004, r=0.01)
    # turned posts with finials, and the footboard between the foot posts
    for x, top in ((hx, 1.55), (B['x1'] + 0.02, 1.0)):
        for z in (B['z0'] - 0.04, B['z1'] + 0.04):
            b.cylinder((x, top / 2, z), top / 2, 0.035, DARKWOOD, op=UNION, rr=0.005)
            for y in np.arange(0.25, top - 0.1, 0.2):
                b.torus((x, y, z), 0.036, 0.012, DARKWOOD, op=SUNION, k=0.01)
            b.sphere((x, top + 0.03, z), 0.05, DARKWOOD, op=SUNION, k=0.02)
            b.cylinder((x, 0.03, z), 0.03, 0.05, DARKWOOD, op=SUNION, k=0.01)
    b.box((B['x1'] + 0.02, 0.55, zc), (0.03, 0.22, zh), DARKWOOD, op=UNION, r=0.008)
    b.box((B['x1'] + 0.03, 0.78, zc), (0.045, 0.02, zh + 0.02), DARKWOOD, op=UNION, r=0.01)


def dresser(b):
    """A mahogany chest of drawers on the right wall, a gilt mirror over it (smashed: the frame hangs empty
    but for a few shards)."""
    x = HALF_W - 0.26
    z = DRESSER_Z
    b.group('dresser', margin=0.03)
    b.box((x, 0.47, z), (0.25, 0.40, 0.55), DARKWOOD, op=UNION, r=0.01)
    b.box((x - 0.01, 0.885, z), (0.27, 0.018, 0.58), DARKWOOD, op=UNION, r=0.008)
    for i, y in enumerate((0.22, 0.47, 0.72)):
        if i == 1:                    # the bottom and top drawers are gone: dark empty holes
            b.box((x - 0.25, y, z), (0.012, 0.10, 0.50), DARKWOOD, op=SUNION, k=0.004, r=0.006)
            for dz in (-0.28, 0.28):
                b.sphere((x - 0.27, y, z + dz), 0.016, BRASS, op=UNION)
        else:
            b.box((x - 0.2, y, z), (0.1, 0.095, 0.48), DARKWOOD, op=SUB)
    for dz in (-0.5, 0.5):
        b.box((x - 0.2, 0.04, z + dz), (0.05, 0.04, 0.05), DARKWOOD, op=UNION, r=0.01)
    b.group('mirror', margin=0.02)
    mx, my = HALF_W - 0.03, 1.55
    b.box((mx, my, z), (0.02, 0.45, 0.36), GOLD, op=UNION, r=0.01)
    b.box((mx - 0.02, my, z), (0.03, 0.39, 0.30), GOLD, op=SUB)
    b.box((mx + 0.005, my, z), (0.004, 0.39, 0.30), WALL, op=UNION)
    # what is left of the glass: jagged pieces still held in the corners of the frame
    for cy, cz, s in ((0.30, -0.24, 1), (-0.31, 0.22, -1), (0.28, 0.20, 1)):
        c = np.array([mx - 0.005, my + cy, z + cz])
        b.box(c, (0.003, 0.09, 0.07), GLASS, op=UNION)
        b.halfspace(c, rot(0, 0, 0) @ rot(0, 38 * s, 0), GLASS, op=SUB)


def desk(b):
    """A small writing desk under the window's far side, its chair knocked over."""
    z = WINDOW['z']
    x = HALF_W - 0.33
    b.group('desk', margin=0.03)
    b.box((x, 0.755, z), (0.30, 0.02, 0.55), DARKWOOD, op=UNION, r=0.006)
    b.box((x + 0.02, 0.68, z), (0.26, 0.06, 0.50), DARKWOOD, op=UNION, r=0.006)
    for dx in (-0.26, 0.26):
        for dz in (-0.5, 0.5):
            b.cone((x + dx, 0.0, z + dz), (x + dx, 0.62, z + dz), 0.018, 0.028, DARKWOOD, op=UNION)
    b.group('chair', margin=0.03)
    # the chair on its back on the floor, legs towards the room
    c = np.array([x - 0.75, 0.0, z + 0.05])
    b.box(c + [0, 0.03, 0], (0.22, 0.03, 0.21), DARKWOOD, op=UNION, r=0.01)            # its back, flat
    b.box(c + [0.26, 0.23, 0], (0.03, 0.22, 0.21), DARKWOOD, op=UNION, r=0.01)          # the seat, on edge
    for dz in (-0.18, 0.18):
        b.capsule(c + [0.28, 0.44, dz], c + [0.72, 0.44, dz], 0.017, DARKWOOD, op=UNION)
        b.capsule(c + [0.28, 0.03, dz], c + [0.72, 0.05, dz], 0.017, DARKWOOD, op=UNION)


KEY = np.array([0.80, 0.52, 0.10]) / np.linalg.norm([0.80, 0.52, 0.10])    # grey daylight through the window
FILL = np.array([-0.25, 0.35, -0.90]) / np.linalg.norm([-0.25, 0.35, -0.90])  # from the bright en-suite


def shadow_maps(focus=(-0.4, 0.9, -3.2)):
    return [(KEY, tuple(focus), 3.2, 2600, np.tan(np.radians(6)), 0.0006),
            (KEY, (0.0, 1.6, -2.6), 9.0, 2800, np.tan(np.radians(6)), 0.002),
            (FILL, tuple(focus), 3.2, 1600, np.tan(np.radians(12)), 0.0006),
            (FILL, (0.0, 1.6, -2.6), 9.0, 1800, np.tan(np.radians(12)), 0.002)]


def light_rows(lamps):
    rows = [[0, *KEY, 1.10, 1.12, 1.18, 2, 0, 0, 0, 2],
            [0, *FILL, 0.25, 0.26, 0.28, 2, 0, 0, 2, 2]]
    for p in lamps:
        rows.append([1, *p, 0.55, 0.45, 0.32, 0, 0, 4.0, 0, 0])
    e = sum(ENSUITE) / 2
    rows.append([1, e, 2.0, BACK_Z - 1.0, 0.9, 0.9, 0.92, 0, 0, 3.0, 0, 0])
    return np.array(rows, dtype=np.float64)
