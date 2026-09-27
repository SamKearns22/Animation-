"""The kitchen set, shared by every shot in it: white shaker cabinets, a marble island, a window on to the
snowy garden, pendant lamps, a little tree with candles, and through a doorway the lit Christmas tree in the
next room. It never moves, so a shot renders it once and reuses it (see shot.py).

World coordinates: metres, y up, the floor at y = 0; the island runs along x; the back wall is at z = BACK_Z.
"""
import numpy as np

import sdf3d as S
from materials import *  # noqa: F401,F403 - the set uses most of them
from sdf3d import rot, UNION, SUNION, SSUB, SUB


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# The kitchen: white shaker cabinets with black handles, a marble island, a window on to the snowy garden,
# clear glass pendant lamps, a little tree in a weathered wooden tray with pillar candles, and through a
# doorway the lit Christmas tree in the next room.
# ---------------------------------------------------------------------------
ISLAND = dict(x0=-1.25, x1=1.25, z0=-0.62, z1=0.38, top=0.92)
BACK_Z = -2.25
PENDANTS = [(-0.62, -0.12), (0.64, -0.12)]
TRAY_C = np.array([1.00, 0.92, -0.30])


def shaker_panel(b, c, half, R, depth_axis=2, handle=None):
    """A painted shaker door/drawer front: flat frame with a recessed centre panel and a black pull."""
    c = np.asarray(c, float)
    b.box(c, half, PAINT, op=SUNION, k=0.001, r=0.002, R=R)
    inner = np.array(half, float)
    inner[0] -= 0.055
    inner[1] -= 0.055
    n = (R if R is not None else np.eye(3))[:, depth_axis]
    if inner[0] > 0.01 and inner[1] > 0.01:
        inner[depth_axis] = 0.006
        b.box(c + n * half[depth_axis], inner, PAINT, op=SSUB, k=0.003, r=0.002, R=R)
    if handle == 'bar':
        ax = (R if R is not None else np.eye(3))[:, 0]
        p = c + n * (half[depth_axis] + 0.022)
        b.capsule(p - ax * 0.07, p + ax * 0.07, 0.0055, BLACKMETAL, op=UNION)
        for sgn in (-1, 1):
            b.capsule(p + ax * 0.065 * sgn, p + ax * 0.065 * sgn - n * 0.022, 0.0045, BLACKMETAL, op=UNION)
    elif handle == 'knob':
        up = (R if R is not None else np.eye(3))[:, 1]
        p = c + n * (half[depth_axis] + 0.012) - up * (half[1] - 0.09)
        b.sphere(p, 0.013, BLACKMETAL, op=UNION)


FRONT_Z = 1.55                      # the wall on the daughter's side of the island (a 'wild wall': only built for
RADIATOR_X = (-0.40, 0.20)          # shots that face it, as on a film set - shot 1's camera stands beyond it)


def front_wall(b):
    """The wall behind the daughter: plain paint over a skirting board, and a slim modern column radiator
    (the hot-water kind a contemporary remodel would fit), white, standing on short legs."""
    b.group('front_wall', margin=0.05)
    b.box((0, 1.35, FRONT_Z + 0.05), (4.0, 1.40, 0.05), WALL, op=UNION)
    b.box((0, 0.06, FRONT_Z - 0.008), (4.0, 0.06, 0.010), PAINT, op=UNION, r=0.003)     # skirting board
    b.group('radiator', margin=0.02)
    x0, x1 = RADIATOR_X
    zc = FRONT_Z - 0.075
    ylo, yhi = 0.16, 0.70
    n = int((x1 - x0) / 0.046)
    for i in range(n + 1):
        x = x0 + i * (x1 - x0) / n
        for dz in (-0.018, 0.018):          # two columns deep, like a classic column radiator
            b.capsule((x, ylo, zc + dz), (x, yhi, zc + dz), 0.0115, RADIATOR, op=SUNION, k=0.006)
    for y in (ylo, yhi):                    # the manifolds joining the columns top and bottom
        b.box(((x0 + x1) / 2, y, zc), ((x1 - x0) / 2 + 0.012, 0.014, 0.030), RADIATOR, op=SUNION, k=0.008, r=0.010)
    for x in (x0 + 0.02, x1 - 0.02):        # legs
        b.box((x, ylo / 2, zc), (0.012, ylo / 2, 0.022), RADIATOR, op=UNION, r=0.004)
    b.capsule((x1 + 0.02, ylo, zc), (x1 + 0.06, ylo, zc), 0.009, STEEL, op=UNION)      # valve and pipe
    b.cylinder((x1 + 0.075, ylo + 0.004, zc), 0.018, 0.012, STEEL, op=UNION, rr=0.003)
    b.capsule((x1 + 0.075, ylo, zc), (x1 + 0.075, 0.0, zc), 0.0075, STEEL, op=UNION)


def build_environment(b, SP, front=False):
    """The set. front: also build the wall behind the daughter (for shots looking her way)."""
    b.set_frame((0, 0, 0), None)
    I = ISLAND
    if front:
        front_wall(b)
    # --- floor (patterned cement tiles), walls, ceiling
    b.group('room', margin=0.05)
    b.box((0, -0.05, -1.0), (4.0, 0.05, 4.5), TILE, op=UNION)
    b.box((0, 2.75, -1.0), (4.0, 0.05, 4.5), CEILING, op=UNION)
    b.box((0, 1.35, BACK_Z - 0.05), (4.0, 1.40, 0.05), WALL, op=UNION)
    b.box((-2.9, 1.35, -1.0), (0.05, 1.40, 4.5), WALL, op=UNION)
    b.box((2.9, 1.35, -1.0), (0.05, 1.40, 4.5), WALL, op=UNION)
    # the window opening and the doorway through the back wall
    b.box((-1.15, 1.63, BACK_Z - 0.05), (0.62, 0.62, 0.20), WALL, op=SUB)
    b.box((1.55, 1.05, BACK_Z - 0.05), (0.40, 1.05, 0.20), WALL, op=SUB)
    for x in (-1.3, 0.0, 1.3):
        b.cylinder((x, 2.705, -0.9), 0.006, 0.045, DOWNLIGHT, op=UNION)
        b.cylinder((x, 2.705, 0.6), 0.006, 0.045, DOWNLIGHT, op=UNION)
    # --- the snowy garden beyond the window
    b.group('outside', margin=0.05)
    b.box((-1.15, 1.6, BACK_Z - 0.75), (1.4, 1.6, 0.02), OUTSIDE, op=UNION)
    b.group('window_frame', margin=0.02)
    wx0, wx1, wy0, wy1 = -1.77, -0.53, 1.01, 2.25
    zf = BACK_Z - 0.02
    for x in (wx0, (wx0 + wx1) / 2, wx1):
        b.box((x, (wy0 + wy1) / 2, zf), (0.022 if x != (wx0 + wx1) / 2 else 0.016, (wy1 - wy0) / 2, 0.03),
              BLACKMETAL, op=UNION)
    for y in (wy0, (wy0 + wy1) / 2, wy1):
        b.box(((wx0 + wx1) / 2, y, zf), ((wx1 - wx0) / 2, 0.022 if y != (wy0 + wy1) / 2 else 0.016, 0.03),
              BLACKMETAL, op=UNION)
    b.box(((wx0 + wx1) / 2, wy0 - 0.03, BACK_Z + 0.02), ((wx1 - wx0) / 2 + 0.06, 0.018, 0.07), PAINT, op=UNION)
    # --- the next room: warm walls, a big tree full of lights
    b.group('next_room', margin=0.05)
    b.box((1.4, -0.05, BACK_Z - 1.5), (1.0, 0.05, 1.5), FLOOR, op=UNION)
    b.box((1.4, 1.35, BACK_Z - 2.6), (1.2, 1.40, 0.05), WARMWALL, op=UNION)
    b.box((0.7, 1.35, BACK_Z - 1.5), (0.05, 1.40, 1.5), WARMWALL, op=UNION)
    tc = np.array([1.85, 0.0, BACK_Z - 1.7])
    b.group('big_tree', disp=S.D_TREE, dparams=[0.05, 4.0, NEEDLES, *tc], margin=0.08)
    for i, (y0, y1, r0) in enumerate(((0.25, 0.95, 0.48), (0.75, 1.40, 0.37), (1.20, 1.80, 0.25), (1.60, 2.05, 0.13))):
        b.cone(tc + [0, y0, 0], tc + [0, y1, 0], r0, 0.02, NEEDLES, op=SUNION if i else UNION, k=0.06)
    b.cylinder(tc + [0, 0.12, 0], 0.12, 0.05, TRAY, op=SUNION, k=0.02)
    rng = np.random.default_rng(11)
    for _ in range(55):
        y = rng.uniform(0.35, 1.95)
        rr = 0.48 * (1 - (y - 0.25) / 1.9) + 0.02
        a = rng.uniform(0, 2 * np.pi)
        p = tc + [rr * np.sin(a), y, rr * np.cos(a)]
        b.sphere(p, 0.014, FAIRY, op=UNION)
    # --- back run of cabinets and worktop, upper cabinets, a few things on the counter
    b.group('back_run', margin=0.03)
    b.box((-0.2, 0.46, BACK_Z + 0.31), (2.6, 0.44, 0.30), PAINT, op=UNION)
    b.box((-0.2, 0.915, BACK_Z + 0.32), (2.65, 0.02, 0.32), MARBLE, op=UNION, r=0.004)
    for i, x in enumerate(np.arange(-2.4, 0.9, 0.55)):
        shaker_panel(b, (x + 0.275, 0.62, BACK_Z + 0.615), (0.265, 0.20, 0.012), None, handle='bar')
        shaker_panel(b, (x + 0.275, 0.24, BACK_Z + 0.615), (0.265, 0.17, 0.012), None, handle='bar')
    b.group('uppers', margin=0.03)
    for x0, x1 in ((-2.85, -1.85), (-0.40, 0.95)):
        b.box(((x0 + x1) / 2, 1.95, BACK_Z + 0.18), ((x1 - x0) / 2, 0.45, 0.18), PAINT, op=UNION)
        for x in np.arange(x0, x1 - 0.01, 0.45):
            shaker_panel(b, (x + 0.225, 1.95, BACK_Z + 0.37), (0.215, 0.43, 0.012), None, handle='knob')
    b.box((-0.2, 2.47, BACK_Z + 0.22), (2.7, 0.06, 0.22), PAINT, op=UNION)  # crown moulding
    b.group('counter_things', margin=0.02)
    # a stand of clementines in a white bowl, a stoneware jar of utensils, a kettle
    bowl = np.array([0.35, 0.935, BACK_Z + 0.33])
    b.sphere(bowl + [0, 0.07, 0], 0.13, CERAMIC, op=UNION)
    b.box(bowl + [0, 0.20, 0], (0.2, 0.08, 0.2), CERAMIC, op=SSUB, k=0.01)
    b.sphere(bowl + [0, 0.11, 0], 0.115, CERAMIC, op=SSUB, k=0.005)
    for dx, dy, dz in ((-0.05, 0.10, 0.02), (0.05, 0.10, -0.03), (0.0, 0.10, 0.06), (0.02, 0.15, 0.0),
                       (-0.06, 0.13, -0.05), (0.07, 0.12, 0.05)):
        b.sphere(bowl + [dx, dy, dz], 0.034, CLEMENTINE, op=UNION)
    jar = np.array([-0.35, 0.93, BACK_Z + 0.28])
    b.cylinder(jar + [0, 0.09, 0], 0.09, 0.06, CERAMIC, op=UNION, rr=0.01)
    for a in (-0.2, 0.0, 0.25):
        b.capsule(jar + [0.02 * np.sin(a * 9), 0.15, 0.01], jar + [np.sin(a) * 0.08, 0.36, 0.02], 0.007, HANDLE,
                  op=UNION)
    kettle = np.array([-0.05, 0.93, BACK_Z + 0.30])
    b.ellipsoid(kettle + [0, 0.10, 0], (0.10, 0.10, 0.09), BLACKMETAL, op=UNION)
    b.capsule(kettle + [0.07, 0.10, 0], kettle + [0.15, 0.17, 0], 0.012, BLACKMETAL, k=0.01)
    b.torus(kettle + [0, 0.21, 0], 0.05, 0.008, BLACKMETAL, k=0.004, R=rot(roll=90))
    # --- the island: marble slab over painted shaker drawers with black bar pulls
    b.group('island', margin=0.03)
    cx, cz = (I['x0'] + I['x1']) / 2, (I['z0'] + I['z1']) / 2
    hx, hz = (I['x1'] - I['x0']) / 2, (I['z1'] - I['z0']) / 2
    b.box((cx, I['top'] - 0.015, cz), (hx, 0.015, hz), MARBLE, op=UNION, r=0.004)
    b.box((cx, 0.49, cz), (hx - 0.03, 0.40, hz - 0.03), PAINT, op=UNION)
    b.box((cx, 0.05, cz), (hx - 0.08, 0.05, hz - 0.08), PAINT, op=UNION)
    fz = I['z1'] - 0.03
    for x in np.arange(I['x0'] + 0.03, I['x1'] - 0.05, 0.62):
        shaker_panel(b, (x + 0.305, 0.72, fz + 0.012), (0.295, 0.13, 0.012), None, handle='bar')
        shaker_panel(b, (x + 0.305, 0.36, fz + 0.012), (0.295, 0.21, 0.012), None, handle='bar')
    # --- the little tree in a weathered tray with white pillar candles
    b.group('tray', margin=0.03)
    T0 = TRAY_C
    b.box(T0 + [0, 0.028, 0], (0.25, 0.028, 0.16), TRAY, op=UNION, r=0.004)
    b.box(T0 + [0, 0.040, 0], (0.232, 0.03, 0.142), TRAY, op=SUB)
    b.box(T0 + [0, 0.012, 0], (0.232, 0.004, 0.142), TRAY, op=UNION)
    tree = T0 + np.array([-0.08, 0.02, -0.04])
    b.group('little_tree', disp=S.D_TREE, dparams=[0.012, 18.0, NEEDLES, *tree], margin=0.03)
    b.cylinder(tree + [0, 0.045, 0], 0.045, 0.055, CERAMIC, op=UNION, rr=0.008)
    for i, (y0, y1, r0) in enumerate(((0.08, 0.22, 0.10), (0.17, 0.31, 0.080), (0.26, 0.40, 0.055))):
        b.cone(tree + [0, y0, 0], tree + [0, y1, 0], r0, 0.005, NEEDLES, op=SUNION, k=0.025)
    rng = np.random.default_rng(5)
    for _ in range(22):
        y = rng.uniform(0.10, 0.37)
        rr = 0.10 * (1 - (y - 0.08) / 0.36) + 0.010
        a = rng.uniform(-1.6, 1.6)
        p = tree + [rr * np.sin(a), y, rr * np.cos(a)]
        b.sphere(p, 0.006, FAIRY, op=UNION)
    for i, (a, y) in enumerate(((0.3, 0.14), (-0.8, 0.19), (1.1, 0.25), (-0.2, 0.30), (-1.2, 0.12),
                                 (0.9, 0.17), (-0.5, 0.24), (0.5, 0.34))):
        rr = 0.10 * (1 - (y - 0.08) / 0.36) + 0.004
        b.sphere(tree + [rr * np.sin(a), y, rr * np.cos(a)], 0.012 + 0.002 * (i % 2), (GOLD, BAUBLE_RED)[i % 2],
                 op=UNION)
    b.sphere(tree + [0, 0.415, 0], 0.011, GOLD, op=UNION)
    candles = [((0.10, 0.06), 0.045, 0.21), ((0.16, -0.05), 0.040, 0.14), ((0.03, 0.08), 0.036, 0.10),
               ((-0.15, 0.08), 0.034, 0.08), ((0.19, 0.07), 0.034, 0.07)]
    flames = []
    for (dx, dz), r, h in candles:
        c = T0 + np.array([dx, 0.016 + h / 2, dz])
        b.cylinder(c, h / 2, r, WAX, op=UNION, rr=0.006)
        b.cylinder(c + [0, h / 2 + 0.004, 0], 0.012, r - 0.006, WAX, op=SSUB, k=0.004)
        top = c + [0, h / 2 - 0.004, 0]
        b.capsule(top, top + [0, 0.012, 0], 0.0012, HANDLE, op=UNION)
        b.ellipsoid(top + [0, 0.026, 0], (0.0055, 0.014, 0.0055), FLAME, op=UNION)
        flames.append(top + [0, 0.026, 0])
    # --- the pendant lamps: clear glass drawn as an overlay, black caps, bulbs, flex to the ceiling
    b.group('pendants', margin=0.03)
    for (x, z) in PENDANTS:
        b.cylinder((x, 2.075, z), 0.022, 0.100, BLACKMETAL, op=UNION, rr=0.008)
        b.capsule((x, 2.09, z), (x, 2.70, z), 0.004, BLACKMETAL, op=UNION)
        b.sphere((x, 1.925, z), 0.036, BULB, op=UNION)
        b.capsule((x, 1.96, z), (x, 2.06, z), 0.012, BLACKMETAL, op=UNION)
    SP[80] = len(PENDANTS)
    for k2, (x, z) in enumerate(PENDANTS):
        SP[81 + 5 * k2:86 + 5 * k2] = (x, z, 1.78, 2.06, 0.098)
    return flames


KEY = np.array([0.70, 0.58, 0.42]) / np.linalg.norm([0.70, 0.58, 0.42])   # low winter sun through the window
RIM = np.array([-0.40, 0.30, -0.86]) / np.linalg.norm([-0.40, 0.30, -0.86])  # cool light from the back


def shadow_maps(focus=(0.0, 1.25, -0.55)):
    """The shadow maps the kitchen's light needs: a fine one round the action (`focus`) and a coarse one for
    the whole room, for the sun and for the back light. (light, centre, extent, resolution, softness, bias)"""
    return [(KEY, tuple(focus), 1.5, 2400, np.tan(np.radians(7)), 0.0004),
            (KEY, (0.0, 1.2, -0.8), 6.5, 2600, np.tan(np.radians(7)), 0.002),
            (RIM, tuple(focus), 1.5, 1800, np.tan(np.radians(10)), 0.0004),
            (RIM, (0.0, 1.2, -0.8), 6.5, 2000, np.tan(np.radians(10)), 0.002)]


def light_rows(flames):
    """The lights: sun (shadow maps 0-1), back light (maps 2-3), the pendant lamps, candle flames, and the warm
    glow from the next room."""
    rows = [[0, *KEY, 1.30, 1.26, 1.20, 2, 0, 0, 0, 2],
            [0, *RIM, 0.50, 0.54, 0.60, 2, 0, 0, 2, 2]]
    for (x, z) in PENDANTS:
        rows.append([1, x, 1.925, z, 0.30, 0.25, 0.17, 0, 0, 1.3, 0, 0])
    for f in flames:
        rows.append([1, *f, 0.06, 0.042, 0.022, 0, 0, 0.35, 0, 0])
    rows.append([1, 1.5, 1.7, BACK_Z - 1.0, 0.30, 0.22, 0.12, 0, 0, 2.0, 0, 0])
    return np.array(rows, dtype=np.float64)
