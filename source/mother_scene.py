#!/usr/bin/env python3
"""The mother at her kitchen island at Christmas, built in 3D (see sdf3d.py) so it can be drawn with real
light, depth and form.

Usage:
    python3 mother_scene.py render OUT_DIR [W H]    the full shot: colour render + drawing passes (.npz)
    python3 mother_scene.py face OUT_DIR            just her face, cut from the full-size (2560) frame
    python3 mother_scene.py facelab OUT.png [VOXEL [nohair]]
                                                    her head alone, quickly: as the shot sees it, from
                                                    the front, in profile, and close up
    python3 mother_scene.py headtest OUT.png        close-ups of the head from three angles

Then draw it: python3 graphite.py OUT_DIR/passes_2560.npz drawing.png

Sculpted parts (head, hair, body) take a minute or two each and are kept in a cache folder (set
SCENE_CACHE to choose where), keyed by the code and numbers they are made from.
"""
import os
import sys
import tempfile

import numpy as np

import sdf3d as S
from sdf3d import Builder, rot, UNION, SUNION, SSUB, SUB

CACHE_DIR = os.environ.get('SCENE_CACHE', os.path.join(tempfile.gettempdir(), 'mother_scene_cache'))


def cached(name, fn, deps, *args):
    """Sculpted grids take minutes; keep them on disk, keyed by the code and numbers they depend on."""
    import hashlib
    import inspect
    import pickle
    h = hashlib.sha1()
    for d in deps:
        h.update((inspect.getsource(d) if callable(d) else repr(d)).encode())
    h.update(repr(args).encode())
    path = os.path.join(CACHE_DIR, f'{name}_{h.hexdigest()[:12]}.pkl')
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    res = fn(*args)
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(res, f, protocol=4)
    return res


def _mh_deps():
    import character as C
    import mesh_sdf
    import mhuman as MH
    return [C.base_body, C._grid_of, C._hand_faces, C.head_grid, C.right_hand, C.left_hand, C.FACE, C.SMILE,
            C.SHAPE, C.HANDLE_R, MH.Skeleton, MH.skin if hasattr(MH, 'skin') else MH.bone_matrix, MH.solve_grip,
            MH.face_units, MH.blend_units, MH.macro_values, MH.apply_macros, mesh_sdf.catmull_clark,
            mesh_sdf.mesh_to_sdf, mesh_sdf._band]


def get_mh_head():
    """Her head and neck from MakeHuman, smiling, in head coordinates: ((lo, d, voxel), eyes)."""
    import character as C
    return cached('mhhead', C.head_grid, _mh_deps(), 0.001)


def get_head_grid(smile=1.0):
    return get_mh_head()[0]


def get_mh_hands():
    import character as C
    return cached('mhhands', C.hands, _mh_deps())



# ---------------------------------------------------------------------------
# Materials: colour, shine, mirror, glow, soft light wrap (skin), surface pattern
# ---------------------------------------------------------------------------
MATS = []


def material(rgb, spec=0.0, shin=10.0, refl=0.0, emit=0.0, wrap=0.0, tex=0):
    MATS.append(list(rgb) + [spec, shin, refl, emit, wrap, tex])
    return len(MATS) - 1


SKIN = material((0.80, 0.60, 0.50), spec=0.10, shin=14, wrap=0.35, tex=S.T_SKIN)
LIPS = material((0.64, 0.34, 0.32), spec=0.22, shin=26, wrap=0.3, tex=S.T_SKIN)
LID = material((0.79, 0.58, 0.49), spec=0.08, shin=14, wrap=0.35, tex=S.T_LID)
EYE = material((0.86, 0.84, 0.82), spec=0.9, shin=220, tex=S.T_EYE)
NOSTRIL = material((0.36, 0.20, 0.17), wrap=0.3)
HAIR = material((0.060, 0.043, 0.034), spec=0.15, shin=50, tex=S.T_HAIR)
KNIT = material((0.80, 0.71, 0.58), wrap=0.25, tex=S.T_KNIT)
NAIL = material((0.84, 0.66, 0.60), spec=0.35, shin=40, wrap=0.2)
WOOD = material((0.66, 0.48, 0.31), spec=0.05, shin=12, tex=S.T_WOODGRAIN)
MEAT = material((0.60, 0.29, 0.08), spec=0.65, shin=70, refl=0.05, tex=S.T_MEAT)   # honey-mustard glaze
HAMPINK = material((0.86, 0.52, 0.47), spec=0.25, shin=30, wrap=0.2)
PINEAPPLE = material((0.96, 0.78, 0.24), spec=0.45, shin=40, wrap=0.2)
CHERRY = material((0.62, 0.02, 0.06), spec=0.9, shin=120, refl=0.05)
PAPER = material((0.96, 0.95, 0.92), spec=0.02, shin=8, wrap=0.3)
BONE = material((0.80, 0.74, 0.62), spec=0.1, shin=20, wrap=0.1)
STEEL = material((0.30, 0.31, 0.33), spec=0.9, shin=90, refl=0.05, tex=S.T_STEEL)
HANDLE = material((0.10, 0.065, 0.045), spec=0.4, shin=50)
PAINT = material((0.88, 0.875, 0.855), spec=0.10, shin=30)
BLACKMETAL = material((0.035, 0.035, 0.035), spec=0.6, shin=60, refl=0.08)
MARBLE = material((0.93, 0.93, 0.915), spec=0.45, shin=110, refl=0.14, tex=S.T_MARBLE)
WALL = material((0.90, 0.885, 0.865), spec=0.02, shin=8)
FLOOR = material((0.60, 0.47, 0.34), spec=0.25, shin=40, refl=0.05, tex=S.T_WOODGRAIN)
OUTSIDE = material((1.0, 1.0, 1.0), emit=1.55, tex=S.T_WINDOW)
BULB = material((1.0, 0.86, 0.62), emit=5.0)
WAX = material((0.94, 0.915, 0.86), spec=0.12, shin=20, wrap=0.55)
FLAME = material((1.0, 0.78, 0.45), emit=6.0)
NEEDLES = material((0.06, 0.11, 0.07), spec=0.1, shin=15, tex=S.T_NEEDLES)
TRAY = material((0.55, 0.50, 0.44), spec=0.05, shin=10, tex=S.T_TRAY)
GOLD = material((0.78, 0.62, 0.30), spec=0.9, shin=80, refl=0.2)
IVORY = material((0.92, 0.90, 0.86), spec=0.5, shin=60)
BAUBLE_RED = material((0.62, 0.04, 0.06), spec=0.9, shin=90, refl=0.15)
FAIRY = material((1.0, 0.86, 0.55), emit=3.5)
CEILING = material((0.93, 0.925, 0.91), spec=0.0, shin=5)
DOWNLIGHT = material((1.0, 0.95, 0.86), emit=3.5)
CLEMENTINE = material((0.86, 0.42, 0.10), spec=0.35, shin=40, wrap=0.2)
CERAMIC = material((0.80, 0.80, 0.78), spec=0.5, shin=60, refl=0.06)
WARMWALL = material((0.80, 0.72, 0.60), spec=0.02, shin=8)


def mat_table():
    return np.array(MATS, dtype=np.float64)


# ---------------------------------------------------------------------------
# The head, in its own coordinates: x across (her left is +x), y up, z out of the face.
# Origin midway between the centres of the eyeballs. Metres.
# ---------------------------------------------------------------------------
EYE_X, EYE_R = 0.0305, 0.0168     # MakeHuman's eyeballs (centres 61 mm apart), sized to fit its lids


def lid_planes(side, open_up=0.0048, open_low=-0.0052, tilt_deg=5.0, smile=1.0):
    """Upper and lower eyelid planes for one eye (head coordinates): normal and offset from the eye centre.
    The lid covers the eyeball where n . (p - c) > offset."""
    tilt = np.radians(tilt_deg) * side  # outer corners slightly higher
    Rz = np.array([[np.cos(tilt), -np.sin(tilt), 0], [np.sin(tilt), np.cos(tilt), 0], [0, 0, 1]])
    nu = Rz @ (np.array([0, 1.0, -0.55]) / np.linalg.norm([0, 1.0, -0.55]))
    nl = Rz @ (np.array([0, -1.0, -0.33]) / np.linalg.norm([0, -1.0, -0.33]))
    front = np.array([0, 0, EYE_R - 0.0002])
    ou = float(nu @ (front + [0, open_up, 0]))
    ol = float(nl @ (front + [0, open_low + 0.0006 * smile, 0]))
    return nu, ou, nl, ol


def frame_y_to(n):
    """Rotation whose local +y is the unit vector n."""
    n = np.asarray(n, float)
    n = n / np.linalg.norm(n)
    h = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 0, 1.0])
    x = np.cross(n, h)
    x /= np.linalg.norm(x)
    z = np.cross(x, n)
    return np.stack([x, n, z], 1)


# --- numpy versions of the basic shapes, for sculpting on a grid ------------------------------------------
def np_ellipsoid(X, Y, Z, c, r, R=None):
    x, y, z = X - c[0], Y - c[1], Z - c[2]
    if R is not None:
        R = np.asarray(R)
        x, y, z = (R[0, 0] * x + R[1, 0] * y + R[2, 0] * z, R[0, 1] * x + R[1, 1] * y + R[2, 1] * z,
                   R[0, 2] * x + R[1, 2] * y + R[2, 2] * z)
    k0 = np.sqrt((x / r[0]) ** 2 + (y / r[1]) ** 2 + (z / r[2]) ** 2)
    k1 = np.sqrt((x / r[0] ** 2) ** 2 + (y / r[1] ** 2) ** 2 + (z / r[2] ** 2) ** 2)
    return k0 * (k0 - 1) / np.maximum(k1, 1e-9)


def np_capsule(X, Y, Z, a, b, r):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ba = b - a
    px, py, pz = X - a[0], Y - a[1], Z - a[2]
    h = np.clip((px * ba[0] + py * ba[1] + pz * ba[2]) / (ba @ ba), 0, 1)
    return np.sqrt((px - ba[0] * h) ** 2 + (py - ba[1] * h) ** 2 + (pz - ba[2] * h) ** 2) - r


def np_cone(X, Y, Z, a, b, r1, r2):
    """Rounded cone from a (radius r1) to b (radius r2)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ba = b - a
    l2 = ba @ ba
    rr = r1 - r2
    a2 = l2 - rr * rr
    il2 = 1.0 / l2
    pax, pay, paz = X - a[0], Y - a[1], Z - a[2]
    y = pax * ba[0] + pay * ba[1] + paz * ba[2]
    z = y - l2
    xx = (pax * l2 - ba[0] * y) ** 2 + (pay * l2 - ba[1] * y) ** 2 + (paz * l2 - ba[2] * y) ** 2
    y2 = y * y * l2
    z2 = z * z * l2
    k = np.sign(rr) * rr * rr * xx
    d = np.where(np.sign(z) * a2 * z2 > k, np.sqrt(xx + z2) * il2 - r2,
                 np.where(np.sign(y) * a2 * y2 < k, np.sqrt(xx + y2) * il2 - r1,
                          (np.sqrt(xx * a2 * il2) + y * rr) * il2 - r1))
    return d


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b + (a - b) * h - k * h * (1 - h)


def ssub(d, s, k):
    """Carve s out of d, softly."""
    h = np.clip(0.5 - 0.5 * (d + s) / k, 0, 1)
    return d + (-s - d) * h + k * h * (1 - h)


# --- the head's outline: at each height, the half-width, where the widest point sits (front-back), how far the
# head reaches forward and back from there, and how square (>2) or pointed (<2) the front and back curves are.
#                 y        w       cz      front   back    nf    nb
HEAD_PROFILE = np.array([
    [0.1180, 0.0040, -0.060, 0.0080, 0.0080, 2.0, 2.0],
    [0.1120, 0.0300, -0.060, 0.0400, 0.0500, 2.0, 2.0],
    [0.1000, 0.0470, -0.060, 0.0560, 0.0750, 2.0, 2.0],
    [0.0850, 0.0600, -0.060, 0.0720, 0.0880, 2.1, 2.0],
    [0.0650, 0.0680, -0.060, 0.0820, 0.0950, 2.2, 2.0],
    [0.0450, 0.0705, -0.060, 0.0870, 0.0970, 2.3, 2.0],
    [0.0250, 0.0700, -0.060, 0.0890, 0.0950, 2.35, 2.0],
    [0.0100, 0.0690, -0.060, 0.0860, 0.0900, 2.3, 2.0],
    [-0.0050, 0.0680, -0.060, 0.0810, 0.0850, 2.3, 2.0],
    [-0.0200, 0.0660, -0.060, 0.0840, 0.0800, 2.25, 2.0],
    [-0.0350, 0.0625, -0.058, 0.0830, 0.0740, 2.15, 2.1],
    [-0.0500, 0.0580, -0.054, 0.0775, 0.0640, 2.1, 2.2],
    [-0.0620, 0.0525, -0.049, 0.0700, 0.0520, 2.0, 2.3],
    [-0.0720, 0.0468, -0.044, 0.0640, 0.0400, 2.0, 2.5],
    [-0.0810, 0.0402, -0.036, 0.0575, 0.0300, 2.0, 2.6],
    [-0.0890, 0.0322, -0.024, 0.0490, 0.0230, 2.0, 2.6],
    [-0.0955, 0.0232, -0.012, 0.0375, 0.0200, 2.05, 2.5],
    [-0.1005, 0.0140, -0.002, 0.0245, 0.0150, 2.05, 2.4],
    [-0.1040, 0.0040, 0.004, 0.0070, 0.0050, 2.0, 2.2],
])
HEAD_BOX = (np.array([-0.080, -0.205, -0.170]), np.array([0.080, 0.125, 0.062]))


def circle3(a, b, c):
    """Centre and radius of the circle through three 2D points."""
    ax, ay = a
    bx, by = b
    cx, cy = c
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return np.array([ux, uy]), float(np.hypot(ax - ux, ay - uy))


def eye_opening(smile=1.0):
    """The almond between the lids, in eye-centred coordinates (x towards the outer corner, y up): the upper
    lid is the top arc of circle U, the lower lid the bottom arc of circle L."""
    inner, outer = (-0.0153, -0.0010), (0.0153, 0.0020)
    apex = (-0.0025, 0.0061 - 0.0003 * smile)  # the highest point of the upper lid, a little towards the nose
    low = (0.0020, -0.0052 + 0.0007 * smile)  # a smile lifts the lower lid
    cu, ru = circle3(inner, apex, outer)
    cl, rl = circle3(inner, low, outer)
    return cu, ru, cl, rl


def lip_params(smile=1.0):
    W = 0.0235
    yc = -0.0628 + 0.0024 * smile  # the corners of the mouth, lifted in a smile
    return dict(W=W, yc=yc, top=-0.0578, bow=0.0012, stom=-0.0650, bot=-0.0762)


def lip_curves_np(u, L):
    top = L['top'] + L['bow'] * np.exp(-((u - 0.21) / 0.09) ** 2) + (L['yc'] - L['top']) * u ** 1.8
    stom = L['stom'] + (L['yc'] - L['stom']) * u ** 2.2
    bot = L['bot'] + (L['yc'] - L['bot']) * u ** 2.0
    return top, stom, bot


def robust_distance(F, voxel):
    """Turn an inside/outside function F (negative inside) into distances: F over its slope close to the
    surface, and further away the straight-line distance to the nearest surface voxel plus that voxel's own
    exact distance, lightly smoothed (it steps a little from voxel to voxel, which would show wherever another
    shape is blended in softly). The two are cross-faded, so the result is smooth everywhere."""
    from scipy import ndimage
    gx, gy, gz = np.gradient(F, voxel)
    near = (F / np.maximum(np.sqrt(gx * gx + gy * gy + gz * gz), 1e-6)).astype(np.float32)
    del gx, gy, gz
    inside = F < 0
    d_out, i_out = ndimage.distance_transform_edt(~inside, return_indices=True)
    far = (d_out * voxel + near[i_out[0], i_out[1], i_out[2]]).astype(np.float32)
    del d_out, i_out
    d_in, i_in = ndimage.distance_transform_edt(inside, return_indices=True)
    far_in = (-(d_in * voxel - near[i_in[0], i_in[1], i_in[2]])).astype(np.float32)
    del d_in, i_in
    far = np.where(inside, far_in, far).astype(np.float32)
    far = ndimage.gaussian_filter(far, 1.2)
    w = np.clip((np.abs(far) - 1.8 * voxel) / (1.2 * voxel), 0, 1)
    w = np.where((np.sign(near) != np.sign(far)) & (np.abs(far) > 2 * voxel), 1.0, w)
    near = np.clip(near, -3 * voxel, 3 * voxel)
    return (near * (1 - w) + far * w).astype(np.float32)


def head_grid(voxel=0.0010, smile=1.0):
    """Sculpt the head (skull, face, jaw, neck, nose, lids, lips) as a grid of distances in head coordinates."""
    from scipy.interpolate import PchipInterpolator
    lo, hi = HEAD_BOX
    n = np.round((hi - lo) / voxel).astype(int) + 1
    xs = (lo[0] + np.arange(n[0]) * voxel).astype(np.float32)
    ys = (lo[1] + np.arange(n[1]) * voxel).astype(np.float32)
    zs = (lo[2] + np.arange(n[2]) * voxel).astype(np.float32)
    X, Y, Z = xs[:, None, None], ys[None, :, None], zs[None, None, :]
    # --- the outline of skull and face
    prof = HEAD_PROFILE[::-1]
    yc_ = np.clip(ys, prof[0, 0], prof[-1, 0])
    cols = [PchipInterpolator(prof[:, 0], prof[:, c])(yc_).astype(np.float32) for c in range(1, 7)]
    w, cz, fr, bk, nf, nb = [c[None, :, None] for c in cols]
    w = np.maximum(w, 1e-4)
    zz = Z - cz
    front = zz > 0
    D = np.where(front, np.maximum(fr, 1e-4), np.maximum(bk, 1e-4))
    N = np.where(front, nf, nb)
    F = ((np.abs(X) / w) ** N + (np.abs(zz) / D) ** N) ** (1 / N) - 1
    del D, N, zz, front
    F = np.where((Y > prof[-1, 0]) | (Y < prof[0, 0]), np.maximum(F, 0.05), F)
    d = robust_distance(F.astype(np.float32), voxel)
    del F
    # top of the skull kept perfectly round
    d = smin(d, np_ellipsoid(X, Y, Z, (0, 0.024, -0.062), (0.0690, 0.0935, 0.0915)), 0.012)
    # neck
    d = smin(d, np_capsule(X, Y, Z, (0, -0.205, -0.052), (0, -0.062, -0.072), 0.047), 0.024)
    # cheekbones, softly
    for sx in (-1, 1):
        d = smin(d, np_ellipsoid(X, Y, Z, (sx * 0.044, -0.016, -0.010), (0.018, 0.010, 0.012)), 0.02)
    # the eyes: set back under the brow, the skin of the lids wrapping the eyeballs
    for sx in (-1, 1):
        c = np.array([sx * EYE_X, 0.0, 0.0])
        d = ssub(d, np_ellipsoid(X, Y, Z, c + (-sx * 0.001, 0.0015, 0.0068), (0.0185, 0.0140, 0.0105)), 0.007)
        d = smin(d, np.sqrt((X - c[0]) ** 2 + (Y - c[1]) ** 2 + (Z - c[2]) ** 2) - (EYE_R + 0.0022), 0.0045)
    # nose: fine straight bridge, a neat lifted tip, slim wings with a crease round them
    d = smin(d, np_cone(X, Y, Z, (0, 0.001, 0.0165), (0, -0.0280, 0.0348), 0.0044, 0.0056), 0.008)
    d = smin(d, np_ellipsoid(X, Y, Z, (0, -0.0325, 0.0350), (0.0052, 0.0046, 0.0056), rot(pitch=-25)), 0.008)
    for sx in (-1, 1):
        d = smin(d, np_ellipsoid(X, Y, Z, (sx * 0.0096, -0.0383, 0.0238), (0.0038, 0.0036, 0.0052),
                                 rot(yaw=sx * 35)), 0.008)
        crease = [(sx * 0.0135, -0.0350, 0.0240), (sx * 0.0152, -0.0392, 0.0228), (sx * 0.0132, -0.0432, 0.0238)]
        for a, c in zip(crease[:-1], crease[1:]):
            d = ssub(d, np_capsule(X, Y, Z, a, c, 0.0006), 0.0014)
    d = smin(d, np_ellipsoid(X, Y, Z, (0, -0.0385, 0.0290), (0.0024, 0.0022, 0.0060), rot(pitch=35)), 0.0035)
    # the apples of the cheeks, lifted by the smile
    for sx in (-1, 1):
        d = smin(d, np_ellipsoid(X, Y, Z, (sx * 0.034, -0.028, 0.002), (0.014, 0.011, 0.008)), 0.012)
        # youthful fullness in the lower cheek, so it doesn't hollow under the cheekbone
        d = smin(d, np_ellipsoid(X, Y, Z, (sx * 0.041, -0.043, -0.006), (0.016, 0.018, 0.012)), 0.02)
    # the mouth: lips raised on the face as a relief, philtrum, the groove above the chin
    L = lip_params(smile)
    x2 = np.abs(xs)[:, None]
    y2 = ys[None, :]
    ur = x2 / L['W']
    u = np.clip(ur, 0, 1)
    top, stom, bot = lip_curves_np(u, L)
    inside_w = np.clip((1 - x2 / L['W']) / 0.08, 0, 1)
    tu = np.clip((top - y2) / np.maximum(top - stom, 1e-4), 0, 1)
    tl = np.clip((stom - y2) / np.maximum(stom - bot, 1e-4), 0, 1)
    upper = ((y2 <= top) & (y2 >= stom)) * np.clip(np.sin(np.pi * tu ** 0.8), 0, 1) ** 0.7 * 0.0034
    lower = ((y2 < stom) & (y2 >= bot)) * np.clip(np.sin(np.pi * tl ** 1.1), 0, 1) ** 0.6 * 0.0042
    taper = (1 - u ** 3) * inside_w
    relief = (upper + lower) * taper
    relief -= 0.0011 * np.exp(-((y2 - stom) / 0.0005) ** 2) * np.clip((1.04 - ur) / 0.06, 0, 1)  # lips pressed together
    relief += 0.00035 * np.exp(-((y2 - top) / 0.0006) ** 2) * np.clip((1.0 - ur) / 0.1, 0, 1)  # the soft ridge along the upper lip
    ph = np.exp(-((y2 + 0.0515) / 0.0045) ** 2)
    relief += ph * (0.0006 * np.exp(-((x2 - 0.0045) / 0.0018) ** 2) - 0.0005 * np.exp(-(x2 / 0.0022) ** 2))
    relief -= 0.0013 * np.exp(-((y2 + 0.0830) / 0.0035) ** 2 - (x2 / 0.014) ** 2)  # above the chin
    corner = np.exp(-(((x2 - L['W'] - 0.0008) / 0.0022) ** 2 + ((y2 - L['yc']) / 0.0022) ** 2))
    relief -= 0.0014 * corner  # the corners of the mouth tuck in
    front_w = np.clip((Z + 0.005) / 0.01, 0, 1)  # only the front of the face
    d = d - (relief[:, :, None] * front_w).astype(np.float32)
    d = d.astype(np.float32)
    bad = ~np.isfinite(d)
    if bad.any():
        print('warning: fixing', int(bad.sum()), 'bad grid values')
        d[bad] = 0.01
    return lo, d, voxel


# ---------------------------------------------------------------------------
# Where she stands (world coordinates, metres; y up, the camera looks along -z)
# ---------------------------------------------------------------------------
BODY_Z = -0.765                      # centre of her hips, front to back
LEAN = 0.10                          # she leans a little over the island: forward shift per metre of height
HEAD_YAW, HEAD_PITCH, HEAD_ROLL = 38.0, 10.0, -4.0  # turned towards her daughter, looking a little down
GAZE = (0.10, -0.15, 1.0)            # her eyes, in head coordinates
NECK_BASE = np.array([0.0, 1.455, BODY_Z + 0.455 * LEAN + 0.004])


def body_cz(y):
    return BODY_Z + (np.asarray(y) - 1.0) * LEAN


def head_rotation():
    return rot(HEAD_YAW, HEAD_PITCH, HEAD_ROLL)


HEAD_POS = NECK_BASE - head_rotation() @ np.array([0.0, -0.205, -0.052])

# the cleaver, the meat and the board (see build_props); the hands are placed from these
BOARD_C, BOARD_HALF = np.array([-0.03, 0.940, -0.330]), np.array([0.285, 0.020, 0.190])  # lies square on the island
RACK_ANGLE = -30.0  # the blade points forward and a little to her left, as a right-handed cook's does; this is
                    # the angle at which her arm falls naturally (elbow at her side, wrist bent ~35 degrees)
RACK_A = np.array([np.cos(np.radians(RACK_ANGLE)), 0.0, np.sin(np.radians(RACK_ANGLE))])   # along the rack
BLADE_B = np.array([-np.sin(np.radians(RACK_ANGLE)), 0.0, np.cos(np.radians(RACK_ANGLE))])  # blade, to its tip
CUT_C = np.array([-0.110, 0.985, -0.360])                                  # where the blade rests in the meat
RACK_C = CUT_C + 0.12 * RACK_A
# a glazed Christmas ham on the bone lies across the board; the blade has cut into its end, a slice already off
HAM_R = np.array([0.100, 0.064, 0.074])                                    # half length, height, width
HAM_C = CUT_C + 0.072 * RACK_A + np.array([0, 0.96 + 0.058 - CUT_C[1], 0])
HAM_ACROSS = np.cross(RACK_A, [0, 1.0, 0])                                 # the ham's side facing us
HAM_CUT = 0.015                                                            # its cut end, just past the blade
# the moment before a chop: the cleaver held up, its edge hovering a few centimetres over the meat, level with
# the fingers of her other hand
HOVER = 0.165                                                              # how far the blade is raised
BLADE_O = CUT_C + np.array([0, HOVER, 0]) - 0.008 * RACK_A  # middle of its edge, before lifting
HEEL = BLADE_O - 0.07 * BLADE_B + np.array([0, 0.075, 0])                  # back top corner of the blade
BUTT = HEEL - 0.12 * BLADE_B                                               # end of the handle

# arms: shoulder, elbow, wrist. The hands are MakeHuman's (character.py): the right one closed round the
# handle, the left one lying on the meat; each is turned about the handle (or the vertical) until its forearm
# points back to where her elbow naturally sits, and the sleeves then follow the real forearms.
R_SHOULDER = np.array([-0.160, 1.392, body_cz(1.392)])
L_SHOULDER = np.array([0.160, 1.392, body_cz(1.392)])
L_ALONG = 0.045                      # her palm, along the ham from its middle: fingertips a hair's breadth
                                     # from where the blade will fall, but clearly apart from it on screen
L_PALM = HAM_C + L_ALONG * RACK_A + np.array([0, HAM_R[1] * np.sqrt(1 - (L_ALONG / HAM_R[0]) ** 2), 0])
L_SLOPE = L_ALONG * HAM_R[1] / (HAM_R[0] ** 2 * np.sqrt(1 - (L_ALONG / HAM_R[0]) ** 2))  # the ham falls away
                                                                           # towards the blade under her fingers
ELBOW_GUIDES = (np.array([-0.265, 1.120, -0.690]), np.array([0.175, 1.105, -0.575]))
FOREARM = 0.25                       # wrist to elbow, metres
PRESS = 0.004                        # how deep her left hand presses into the meat to hold it steady


def _unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def place_hands():
    """Where the two MakeHuman hands go: [(origin, rotation, wrist, forearm direction)] right then left.
    Each hand is turned about the handle (or, the left, about the vertical), and its wrist bent within a
    natural range (flexion up to 50 degrees, sideways up to 25), so the forearm heads back towards the elbow."""
    import mhuman as MH
    parts = get_mh_hands()
    out = []
    bends = [(fl, dv) for fl in range(-50, 51, 5) for dv in range(-25, 26, 5)]

    def best_forearm(R, wr, fore, wx, wz, guide):
        w = origin + R @ wr
        want = _unit(guide - w)
        best = None
        for fl, dv in bends:
            f = R @ (MH.axis_angle(wz, dv) @ MH.axis_angle(wx, fl) @ fore)
            score = f @ want - 0.002 * (abs(fl) + abs(dv))  # the least bent wrist that does the job
            if best is None or score > best[0]:
                best = (score, w, f)
        return best

    # right: frame x along the handle towards the blade, y towards the knuckles; roll about the handle.
    # An overhand grip, as for any chopping blade: the hand comes over the top of the handle, the back of the
    # hand faces up and the fingers curl round underneath.
    (_, wr, fore, wx, wz, back) = parts[0]
    u = _unit(BLADE_B)
    origin = HEEL - u * 0.038
    k0 = _unit(np.cross([0, 1.0, 0], u))
    best = None
    for th in np.radians(np.arange(0, 360, 3)):
        k = k0 * np.cos(th) + np.cross(u, k0) * np.sin(th)
        R = np.stack([u, k, np.cross(u, k)], 1)
        sc, w, f = best_forearm(R, wr, fore, wx, wz, ELBOW_GUIDES[0])
        sc += 1.5 * ((R @ back)[1] > 0.75) + 0.5 * (R @ back)[1]
        if best is None or sc > best[0]:
            best = (sc, R, w, f)
    out.append((origin, best[1], best[2], best[3]))
    # left: palm down on the meat, fingers lying along it towards the blade (where they shouldn't be);
    # turn about the vertical
    (_, wr, fore, wx, wz) = parts[1]
    origin = L_PALM
    best = None
    n = _unit(np.array([0, 1.0, 0]) - L_SLOPE * RACK_A)  # the ham's surface under her palm
    for th in np.radians(np.arange(0, 360, 3)):
        x = _unit(np.array([np.cos(th), 0, np.sin(th)]) - n * (n @ np.array([np.cos(th), 0, np.sin(th)])))
        R = np.stack([x, n, np.cross(x, n)], 1)
        sc, w, f = best_forearm(R, wr, fore, wx, wz, ELBOW_GUIDES[1])
        sc += 0.8 * (x @ -RACK_A)
        if best is None or sc > best[0]:
            best = (sc, R, w, f)
    # let the hand settle onto the ham: tilt it a little either way, then press it down so it holds the meat
    # steady - its deepest point PRESS into the surface; the meat is dented round it (build_props)
    lgrid = parts[1][0]
    pts = _surface_points(lgrid)
    R0 = best[1]
    settled = None
    for ax in np.radians(np.arange(-15, 16, 3)):
        for az in np.radians(np.arange(-15, 16, 3)):
            R = MH.axis_angle(R0[:, 0], np.degrees(ax)) @ MH.axis_angle(R0[:, 2], np.degrees(az)) @ R0
            dmin = ham_distance(L_PALM + pts @ R.T).min()
            lift = -dmin - PRESS
            if settled is None or lift < settled[0]:
                settled = (lift, R)
    lift, R = settled
    origin = L_PALM + n * lift
    for _ in range(6):  # the distance to the ham is approximate: measure again and correct until the press is right
        dmin = ham_distance(origin + pts @ R.T).min()
        origin = origin + np.array([0, 1.0, 0]) * (-dmin - PRESS)
    sc, w, f = best_forearm(R, wr, fore, wx, wz, ELBOW_GUIDES[1])
    out.append((origin, R, w, f))  # w already includes the lift (best_forearm places it from origin)
    check_joins(out, parts)
    return out


def check_joins(placed, parts):
    """Every hand must meet its sleeve: the wrist the sleeve ends at has to be the hand's own wrist."""
    for (origin, R, w, f), part, name in zip(placed, parts, ('right', 'left')):
        gap = np.linalg.norm(origin + R @ part[1] - w)
        if gap > 0.003:
            raise RuntimeError(f'{name} hand is {gap * 1000:.0f} mm away from the end of its sleeve')


def _surface_points(grid, step=3):
    """Points on a grid shape's surface (in its own frame), thinned out."""
    lo, d, voxel = grid
    idx = np.argwhere(np.abs(d[::step, ::step, ::step]) < 0.6 * voxel * step)
    return lo + idx * voxel * step


def ham_distance(p):
    """Approximate distance from points to the ham's surface (negative inside)."""
    Rh_ = np.stack([RACK_A, [0, 1.0, 0], HAM_ACROSS], 1)
    q = (p - HAM_C) @ Rh_
    k0 = np.linalg.norm(q / HAM_R, axis=1)
    k1 = np.linalg.norm(q / HAM_R ** 2, axis=1)
    d = k0 * (k0 - 1) / np.maximum(k1, 1e-9)
    d = np.maximum(d, 0.962 - p[:, 1])
    return np.maximum(d, -((p - (CUT_C - HAM_CUT * RACK_A)) @ RACK_A))


HANDS = place_hands()
R_WRIST, L_WRIST = HANDS[0][2], HANDS[1][2]
R_ELBOW = R_WRIST + HANDS[0][3] * FOREARM
L_ELBOW = L_WRIST + HANDS[1][3] * FOREARM


def build_mh_hands(b):
    rgrid, lgrid = get_mh_hands()[0][0], get_mh_hands()[1][0]
    for name, (origin, R, _, _), grid in (('right_hand', HANDS[0], rgrid), ('left_hand', HANDS[1], lgrid)):
        b.set_frame(origin, R)
        b.group(name, margin=0.01)
        b.grid(grid[0], grid[1], grid[2], SKIN, op=UNION)
    b.set_frame((0, 0, 0), None)


def body_colliders():
    """Rough solids for the hair to fall over: neck and collar, shoulders, chest, back, upper arms."""
    nz = NECK_BASE[2]
    return [
        ('capsule', (0, 1.44, nz), (0, 1.60, nz - 0.01), 0.050),
        ('capsule', (0, 1.45, nz), (0, 1.52, nz), 0.084),                     # the roll neck
        ('capsule', (-0.05, 1.455, nz), (-0.175, 1.385, float(body_cz(1.385))), 0.045),  # sloping shoulders
        ('capsule', (0.05, 1.455, nz), (0.175, 1.385, float(body_cz(1.385))), 0.045),
        ('ellipsoid', (0, 1.28, float(body_cz(1.28)) + 0.010), (0.170, 0.200, 0.125)),   # chest
        ('capsule', R_SHOULDER, R_ELBOW, 0.052),
        ('capsule', L_SHOULDER, L_ELBOW, 0.052),
    ]


# ---------------------------------------------------------------------------
# Hair: long, dark, parted a little to her right, lifted at the crown, falling in soft waves past the
# shoulders - on her right side forward over the shoulder, on her left behind it. Built from locks combed from
# the parting and let fall under gravity.
# ---------------------------------------------------------------------------
SCALP_C, SCALP_R = np.array([0.0, 0.026, -0.064]), np.array([0.0725, 0.0970, 0.0960])
PART = np.radians(-17.0)             # the parting, round from the front of the head
HAIRLINE = (0.066, 0.019, 0.047, 0.057)  # height at the middle, drop to 5 cm out, height and drop at the temple


def _push_out_ellipsoid(p, c, r, margin):
    q = (p - c) / (r + margin)
    k = np.linalg.norm(q)
    if k < 1.0:
        return c + (p - c) / max(k, 1e-6)
    return p


def _push_out_capsule(p, a, b, r):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ba = b - a
    h = np.clip((p - a) @ ba / (ba @ ba), 0, 1)
    c = a + ba * h
    v = p - c
    L = np.linalg.norm(v)
    if L < r:
        return c + v / max(L, 1e-6) * r
    return p


def scalp_point(theta, elev, layer=0.0):
    """Point on the scalp (head coordinates): theta round from the front (+ towards her left), elev up from the
    widest line of the head."""
    q = np.array([np.cos(elev) * np.sin(theta), np.sin(elev), np.cos(elev) * np.cos(theta)])
    return SCALP_C + q * (SCALP_R + layer)


def hair_locks(seed=2):
    """Paths of the locks (world coordinates) with their radii. Each lock is combed over the scalp from its
    root to a point at the side or back of the head, then falls under gravity over the shoulders."""
    rng = np.random.default_rng(seed)
    Rh = head_rotation()
    H = HEAD_POS
    cols = body_colliders()
    locks = []
    hlo, hd, hvox = get_head_grid()

    def head_dist(pl):
        g = (pl - hlo) / hvox
        i = np.floor(g).astype(int)
        if np.any(i < 1) or np.any(i >= np.array(hd.shape) - 2):
            return 1.0, np.zeros(3)
        f = g - i

        def at(o):
            c = hd[i[0] + o[0]:i[0] + o[0] + 2, i[1] + o[1]:i[1] + o[1] + 2, i[2] + o[2]:i[2] + o[2] + 2]
            c = c[0] * (1 - f[0]) + c[1] * f[0]
            c = c[0] * (1 - f[1]) + c[1] * f[1]
            return c[0] * (1 - f[2]) + c[1] * f[2]
        dv = at((0, 0, 0))
        n = np.array([at((1, 0, 0)) - at((-1, 0, 0)), at((0, 1, 0)) - at((0, -1, 0)), at((0, 0, 1)) - at((0, 0, -1))])
        return float(dv), n / max(np.linalg.norm(n), 1e-9)

    def off_skin(p, margin):
        """Keep a point at least `margin` off her skin (the sculpted head, not just the scalp's egg shape)."""
        pl = Rh.T @ (p - H)
        for _ in range(3):
            dv, n = head_dist(pl)
            if dv >= margin:
                break
            pl = pl + n * (margin - dv)
        return H + Rh @ pl

    def collide(p, layer):
        pl = Rh.T @ (p - H)
        pl = _push_out_ellipsoid(pl, SCALP_C, SCALP_R, layer)
        p = off_skin(H + Rh @ pl, 0.004 + layer)
        pl = Rh.T @ (p - H)
        p = H + Rh @ pl
        for c in cols:
            if c[0] == 'capsule':
                p = _push_out_capsule(p, c[1], c[2], c[3] + layer)
            else:
                p = _push_out_ellipsoid(p, np.asarray(c[1]), np.asarray(c[2]), layer)
        return p

    def lock(th0, e0, thf, side, forward, length, r_flat, r_fall, layer, lift=0.0):
        # 1. over the scalp, from the root to where it starts to fall, standing off it a little on the way
        pts = []
        for t in np.linspace(0, 1, 9):
            th = th0 + (thf - th0) * np.sqrt(t)
            el = e0 + (np.radians(4) - e0) * t * t
            q = H + Rh @ scalp_point(th, el, layer + lift * (1 - (1 - t) ** 2))
            pts.append(off_skin(q, r_flat + 0.0035 + layer))
        on_scalp = len(pts)
        # 2. falling
        p = pts[-1]
        d = pts[-1] - pts[-2]
        d /= np.linalg.norm(d)
        travelled, step = 0.0, 0.008
        wob = rng.uniform(0, 6.28)
        phase = rng.uniform(-0.5, 0.5)
        while travelled < length:
            force = np.array([0, -1.0, 0])
            pl = Rh.T @ (p - H)
            force += Rh @ np.array([np.sign(pl[0]) * 0.25, 0, 0]) * (pl[1] > -0.12)  # a little fullness
            # soft waves, in step from lock to lock (by height) so they read across the whole fall of hair
            wv = np.sin(2 * np.pi * p[1] / 0.105 + phase) * min(1.0, travelled / 0.06)
            force += Rh @ np.array([np.sign(pl[0]) * 0.34 * wv, 0, 0.14 * wv])
            if p[1] < 1.56:
                force += np.array([side * 0.10, 0, 0.55 if forward else -0.40]) * min(1, (1.56 - p[1]) / 0.08)
            force += 0.03 * np.array([np.sin(travelled * 8 + wob), 0, np.cos(travelled * 6 + wob)])
            d = d * 0.75 + 0.25 * force
            d /= np.linalg.norm(d)
            pn = collide(p + d * step, layer)
            p = pn
            travelled += step
            pts.append(p.copy())
        pts = np.array(pts)
        keep = list(range(on_scalp)) + list(range(on_scalp + 2, len(pts), 2))
        pts = pts[keep]
        t = np.linspace(0, 1, len(pts))
        grow = np.clip((np.arange(len(pts)) - on_scalp + 3) / 6.0, 0, 1)
        radii = (r_flat + (r_fall - r_flat) * grow) * np.clip((1 - t) / 0.35, 0.10, 1) ** 0.8
        locks.append((pts, radii))

    # the top layer, combed out from the parting to both sides (more of it to her left, the parting being off
    # to her right)
    for side in (-1, 1):
        n = 30 if side < 0 else 40
        for i in range(n):
            s = (i + rng.uniform(-0.3, 0.3)) / (n - 1)
            s = min(max(s, 0), 1)
            if s < 0.6:  # front half of the parting: forehead up to the top of the head
                th0, e0 = PART, np.radians(38 + (90 - 38) * s / 0.6)
            else:  # back half: over the top to the crown
                th0, e0 = np.pi * side, np.radians(90 - 35 * (s - 0.6) / 0.4)
            thf = side * np.radians(72 + 95 * s)  # front locks fall in front of the ear, back ones behind
            forward = side < 0 and s < 0.55
            lift = 0.0065 * np.clip(s / 0.35, 0, 1) ** 2 * (1 - 0.5 * np.clip((s - 0.7) / 0.3, 0, 1))  # the crown
            lock(th0 + side * 0.03, e0, thf, side, forward, rng.uniform(0.26, 0.38), 0.0038, 0.0105,
                 0.0020 + 0.0030 * rng.random(), lift)
    # an under layer round the back and sides
    for k in range(44):
        side = -1 if k % 2 == 0 else 1
        th = side * np.radians(68 + 110 * (k // 2) / 21) + rng.uniform(-0.03, 0.03)  # ear, round the back
        e0 = np.radians(rng.uniform(8, 30))
        forward = side < 0 and abs(np.degrees(th)) < 110
        lock(th, e0, th, side, forward, rng.uniform(0.27, 0.32), 0.0060, 0.0110, 0.0010 + 0.0015 * rng.random())
    return locks


HAIR_BOX_W = (np.array([-0.27, 1.16, -0.96]), np.array([0.27, 1.83, -0.43]))


def hair_grid(voxel=0.0018, seed=2):
    """The hair as a grid of distances in world coordinates, plus the direction the hair runs in each cell.
    Each lock is a chain of tapered tubes; neighbouring locks are blended, then small gaps closed up so the
    hair falls as a continuous sheet with the locks still showing in it."""
    locks = hair_locks(seed)
    lo, hi = HAIR_BOX_W
    nn = np.round((hi - lo) / voxel).astype(int) + 1
    d = np.full(nn, 0.05, np.float32)
    flow = np.zeros(tuple(nn) + (3,), np.float32)
    k = 0.008
    for pts, radii in locks:
        m = radii.max() + k + 0.01
        L0 = np.maximum(np.floor((pts.min(0) - m - lo) / voxel).astype(int), 0)
        L1 = np.minimum(np.ceil((pts.max(0) + m - lo) / voxel).astype(int) + 1, nn)
        if np.any(L1 <= L0):
            continue
        tmp = np.full(tuple(L1 - L0), 0.05, np.float32)
        ftmp = np.zeros(tuple(L1 - L0) + (3,), np.float32)
        for a, b_, ra, rb in zip(pts[:-1], pts[1:], radii[:-1], radii[1:]):
            mm = max(ra, rb) + k + 0.008
            i0 = np.maximum(np.floor((np.minimum(a, b_) - mm - lo) / voxel).astype(int), L0)
            i1 = np.minimum(np.ceil((np.maximum(a, b_) + mm - lo) / voxel).astype(int) + 1, L1)
            if np.any(i1 <= i0):
                continue
            xs = (lo[0] + np.arange(i0[0], i1[0]) * voxel)[:, None, None]
            ys = (lo[1] + np.arange(i0[1], i1[1]) * voxel)[None, :, None]
            zs = (lo[2] + np.arange(i0[2], i1[2]) * voxel)[None, None, :]
            dc = np_cone(xs, ys, zs, a, b_, ra, rb).astype(np.float32)
            sl = tuple(slice(i0[q] - L0[q], i1[q] - L0[q]) for q in range(3))
            blk = tmp[sl]
            closer = dc < blk
            fb = ftmp[sl]
            fb[closer] = (b_ - a) / max(np.linalg.norm(b_ - a), 1e-9)
            tmp[sl] = np.minimum(blk, dc)
        gs = tuple(slice(L0[q], L1[q]) for q in range(3))
        g = d[gs]
        closer = tmp < g
        fl = flow[gs]
        fl[closer] = ftmp[closer]
        d[gs] = smin(g, tmp, k)
    # the hair lying on the head: the head's own surface lifted by 7-9 mm, everywhere above the hairline -
    # a soft curve 5 cm above the brows, dipping at the temples and in front of the ears
    from scipy import ndimage
    Rh = head_rotation()
    hlo, hd, hvox = get_head_grid()
    hhi = hlo + (np.array(hd.shape) - 1) * hvox
    xs = (lo[0] + np.arange(nn[0]) * voxel).astype(np.float32)
    ys = (lo[1] + np.arange(nn[1]) * voxel).astype(np.float32)
    zs = (lo[2] + np.arange(nn[2]) * voxel).astype(np.float32)
    base = np.full(nn, 0.05, np.float32)
    for i in range(nn[0]):  # a slab at a time, to keep memory modest
        X, Y, Z = np.meshgrid(xs[i:i + 1] - HEAD_POS[0], ys - HEAD_POS[1], zs - HEAD_POS[2], indexing='ij')
        lx = Rh[0, 0] * X + Rh[1, 0] * Y + Rh[2, 0] * Z
        ly = Rh[0, 1] * X + Rh[1, 1] * Y + Rh[2, 1] * Z
        lz = Rh[0, 2] * X + Rh[1, 2] * Y + Rh[2, 2] * Z
        coords = np.stack([(lx - hlo[0]) / hvox, (ly - hlo[1]) / hvox, (lz - hlo[2]) / hvox])
        hv = ndimage.map_coordinates(hd, coords.reshape(3, -1), order=1, mode='nearest').reshape(lx.shape)
        out = sum(np.maximum(np.maximum(hlo[q] - l, l - hhi[q]), 0) ** 2 for q, l in enumerate((lx, ly, lz)))
        hv = hv + np.sqrt(out)  # outside the head's box: keep counting the distance
        ax = np.abs(lx)
        y_hair = np.where(ax < 0.05, HAIRLINE[0] - HAIRLINE[1] * (ax / 0.05) ** 2,
                          HAIRLINE[2] - HAIRLINE[3] * np.clip((ax - 0.05) / 0.025, 0, 1))  # the hairline
        front = np.clip((lz + 0.035) / 0.02, 0, 1)
        edge = np.clip((ly - y_hair) / 0.014, 0, 1)
        edge = edge * edge * (3 - 2 * edge)
        thick = (0.0065 + 0.0065 * np.clip((ly - 0.03) / 0.08, 0, 1)) * (1 - front * 0.42 * (1 - edge))
        b_ = hv - thick
        # edges rounded off (a sharp edge would ripple when stored on the grid)
        b_ = -smin(-b_, -(y_hair - ly) * front, 0.003)           # not over the face
        b_ = -smin(-b_, -(-(ly + 0.03)), 0.004)                  # not down the neck
        # the parting: a fine line along the meridian at PART, from the hairline to the top of the head
        across = np.abs(lx * np.cos(PART) - (lz - SCALP_C[2]) * np.sin(PART))
        part = np.where((ly > 0.04) & (lz > SCALP_C[2]), 0.0022 - across, -0.02)
        b_ = -smin(-b_, -part, 0.0025)
        base[i:i + 1] = np.where(np.isfinite(b_), b_, 0.05)
    d = smin(d, base.astype(np.float32), 0.004)
    # close small gaps between locks: grow by 3.5 mm, re-measure, shrink back
    grow = 0.0035
    d = robust_distance((d - grow).astype(np.float32), voxel) + grow
    d = robust_distance(d.astype(np.float32), voxel)
    return lo, d, voxel, flow


def build_hair(b, grid=None):
    lo, d, voxel, flow = grid if grid is not None else hair_grid()
    Hc = HEAD_POS
    b.set_frame((0, 0, 0), None)
    b.group('hair', disp=S.D_HAIR, dparams=[Hc[0], Hc[1], Hc[2], 0.09, 0.075, 0.0004], margin=0.01)
    b.grid(lo, d, voxel, HAIR, op=UNION)


# ---------------------------------------------------------------------------
# Her body in a loose, chunky rib-knit jumper with a soft roll neck (world coordinates)
# ---------------------------------------------------------------------------
#                 y       w      front   back
BODY_PROFILE = np.array([  # shoulders sloping down from the neck, a slim chest, a soft waist
    [1.500, 0.062, 0.055, 0.055], [1.475, 0.098, 0.064, 0.062], [1.455, 0.135, 0.072, 0.068],
    [1.435, 0.162, 0.080, 0.074], [1.410, 0.180, 0.088, 0.080], [1.380, 0.186, 0.096, 0.086],
    [1.340, 0.174, 0.104, 0.092], [1.290, 0.160, 0.112, 0.097], [1.240, 0.154, 0.114, 0.096],
    [1.180, 0.148, 0.108, 0.093], [1.110, 0.140, 0.100, 0.090], [1.040, 0.146, 0.098, 0.094],
    [0.950, 0.158, 0.100, 0.100], [0.860, 0.156, 0.096, 0.098]])
BODY_BOX = (np.array([-0.33, 0.84, -0.93]), np.array([0.33, 1.56, -0.34]))


def body_grid(voxel=0.0025):
    from scipy.interpolate import PchipInterpolator
    lo, hi = BODY_BOX
    nn = np.round((hi - lo) / voxel).astype(int) + 1
    xs = (lo[0] + np.arange(nn[0]) * voxel).astype(np.float32)
    ys = (lo[1] + np.arange(nn[1]) * voxel).astype(np.float32)
    zs = (lo[2] + np.arange(nn[2]) * voxel).astype(np.float32)
    X, Y, Z = xs[:, None, None], ys[None, :, None], zs[None, None, :]
    prof = BODY_PROFILE[::-1]
    yc = np.clip(ys, prof[0, 0], prof[-1, 0])
    w, fr, bk = [PchipInterpolator(prof[:, 0], prof[:, c])(yc).astype(np.float32)[None, :, None] for c in (1, 2, 3)]
    cz = body_cz(ys).astype(np.float32)[None, :, None]
    zz = Z - cz
    front = zz > 0
    D = np.where(front, fr, bk)
    N = np.where(front, 2.3, 2.4).astype(np.float32)
    F = ((np.abs(X) / w) ** N + (np.abs(zz) / D) ** N) ** (1 / N) - 1
    gx, gy, gz = np.gradient(F, voxel)
    d = (F / np.maximum(np.sqrt(gx * gx + gy * gy + gz * gz), 1e-6)).astype(np.float32)
    del gx, gy, gz, F, D, N, zz, front
    d = np.maximum(d, np.maximum(Y - prof[-1, 0], prof[0, 0] - Y))
    # a soft bust under the knit
    for sx in (-1, 1):
        d = smin(d, np_ellipsoid(X, Y, Z, (sx * 0.066, 1.300, float(body_cz(1.300)) + 0.080),
                                 (0.062, 0.055, 0.044)), 0.05)
    # the roll neck: three soft rolls round the neck
    nz = NECK_BASE[2]
    for y, R0, r in ((1.458, 0.080, 0.021), (1.484, 0.075, 0.019), (1.505, 0.067, 0.016)):
        q = np.sqrt(X ** 2 + (Z - nz) ** 2) - R0
        d = smin(d, (np.sqrt(q ** 2 + (Y - y) ** 2) - r).astype(np.float32), 0.012)
    # the opening of the roll neck - only through the collar, not down through her whole body
    hole = np.sqrt(X ** 2 + (Z - nz) ** 2) - 0.052
    hole = np.maximum(hole, 1.43 - Y)
    d = ssub(d, hole.astype(np.float32), 0.004)
    # sleeves; remember which part is nearest everywhere, so the knit can run the right way
    torso = d.copy()
    arm_d = []
    for sh, el, wr in ((R_SHOULDER, R_ELBOW, R_WRIST), (L_SHOULDER, L_ELBOW, L_WRIST)):
        fore = (wr - el) / np.linalg.norm(wr - el)
        cuff = wr - fore * 0.050
        upper = np_cone(X, Y, Z, sh, el, 0.052, 0.045)
        lower = np_cone(X, Y, Z, el, cuff, 0.045, 0.039)
        # a ribbed cuff hugs the wrist and ends in a rounded fold just over the heel of the hand
        lower = smin(lower, np_cone(X, Y, Z, cuff, wr + fore * 0.014, 0.037, 0.027), 0.012)
        a = smin(upper, lower, 0.02)
        arm_d.append(a.astype(np.float32))
        # only the upper arm melts into the jumper (at the shoulder seam); a forearm resting across her front
        # stays a separate sleeve, never webbed to her tummy
        d = smin(d, upper, 0.035)
        d = np.minimum(d, lower)
    part = np.zeros(d.shape, np.float32)
    part[(arm_d[0] < torso) & (arm_d[0] <= arm_d[1])] = 1
    part[(arm_d[1] < torso) & (arm_d[1] < arm_d[0])] = 2
    d = robust_distance(d.astype(np.float32), voxel)
    return lo, d, voxel, part


def build_body(b, grid=None):
    lo, d, voxel, part = grid if grid is not None else body_grid()
    b.set_frame((0, 0, 0), None)
    nz = NECK_BASE[2]
    params = [0.0, nz, 0.15, 0.0085, 0.0016] + list(R_SHOULDER) + list(R_ELBOW) + list(R_WRIST) + \
        list(L_SHOULDER) + list(L_ELBOW) + list(L_WRIST) + [0.075, 1.43]
    b.group('body', disp=S.D_BODY, dparams=params, margin=0.02)
    b.grid(lo, d, voxel, KNIT, op=UNION)
    # the part map rides along in the grid buffer; its offset goes in the group's parameters
    off = b.grid_len
    b.grids.append(np.ascontiguousarray(part, dtype=np.float32).reshape(-1))
    b.grid_len += part.size
    b.groups[-1]['dparams'][25] = float(off)


# ---------------------------------------------------------------------------
# The board, the glazed rack of ribs, the cleaver
# ---------------------------------------------------------------------------
def build_props(b):
    b.set_frame((0, 0, 0), None)
    b.group('board', margin=0.01)
    b.box(BOARD_C, BOARD_HALF, WOOD, op=UNION, r=0.006)  # square to the island's edges
    # the ham: glazed, scored in diamonds and studded with cloves (see the MEAT texture), sitting a little
    # flattened on the board, the shank bone at the far end dressed in a paper frill
    b.group('ham', margin=0.02)
    Rh_ = np.stack([RACK_A, [0, 1.0, 0], HAM_ACROSS], 1)
    b.ellipsoid(HAM_C, HAM_R, MEAT, op=UNION, R=Rh_)
    b.halfspace(np.array([HAM_C[0], 0.962, HAM_C[2]]), np.eye(3), MEAT, op=SUB)  # its flat underside
    # its cut end, where the last slice came off, and the blade's cut
    b.halfspace(CUT_C - HAM_CUT * RACK_A, np.stack([np.cross([0, 1.0, 0], RACK_A), RACK_A, [0, 1.0, 0]], 1),
                MEAT, op=SUB)
    # the dent her left hand presses into it: the meat gives way round the palm and fingers
    lgrid = get_mh_hands()[1][0]
    b.set_frame(HANDS[1][0], HANDS[1][1])
    b.grid(lgrid[0], lgrid[1], lgrid[2], MEAT, op=SSUB, k=0.004)
    b.set_frame((0, 0, 0), None)
    shank_a = HAM_C + RACK_A * (HAM_R[0] - 0.02) + np.array([0, 0.004, 0])
    shank_b = shank_a + RACK_A * 0.042 + np.array([0, 0.010, 0])
    b.capsule(shank_a, shank_b, 0.0095, BONE, op=SUNION, k=0.010)
    fr = shank_a + (shank_b - shank_a) * 0.62
    b.group('frill', margin=0.01)
    Rf = np.stack([HAM_ACROSS, _unit(shank_b - shank_a), np.cross(HAM_ACROSS, _unit(shank_b - shank_a))], 1)
    b.cone(fr, fr + _unit(shank_b - shank_a) * 0.020, 0.0125, 0.017, PAPER, op=UNION)
    b.cylinder(fr + _unit(shank_b - shank_a) * 0.011, 0.011, 0.0100, PAPER, op=SUB, R=Rf)
    # pineapple rings pinned on with glace cherries, on the side and top facing us
    b.group('garnish', margin=0.01)
    for s_, phi in ((-0.42, 0.95), (0.05, 1.00), (0.50, 0.90)):
        rr = np.sqrt(1 - s_ ** 2)
        loc = np.array([s_ * HAM_R[0], HAM_R[1] * rr * np.cos(phi), HAM_R[2] * rr * np.sin(phi)])
        nrm = _unit(loc / HAM_R ** 2)
        p = HAM_C + Rh_ @ loc
        n_ = _unit(Rh_ @ nrm)
        Rn = np.stack([_unit(np.cross(n_, [0, 0, 1.0])), n_, np.cross(_unit(np.cross(n_, [0, 0, 1.0])), n_)], 1)
        b.cylinder(p - n_ * 0.001, 0.0042, 0.021, PINEAPPLE, op=UNION, R=Rn, rr=0.002)
        b.cylinder(p, 0.010, 0.0075, PINEAPPLE, op=SUB, R=Rn)
        b.sphere(p + n_ * 0.003, 0.0072, CHERRY, op=UNION)
    # a slice already cut, lying on the board towards us
    b.group('slice', margin=0.01)
    sc_ = CUT_C - 0.075 * RACK_A + HAM_ACROSS * 0.075
    sc_[1] = 0.96 + 0.0035
    Rs = rot(yaw=-RACK_ANGLE + 25)
    b.cylinder(sc_, 0.0034, 0.058, MEAT, op=UNION, R=Rs, rr=0.002)
    b.cylinder(sc_ + np.array([0, 0.0006, 0]), 0.0034, 0.051, HAMPINK, op=UNION, R=Rs, rr=0.002)
    # the cleaver: a heavy square blade, held up over the meat; dark wooden handle, steel rivets
    b.group('cleaver', margin=0.01)
    Rb = np.stack([BLADE_B, [0, 1.0, 0], RACK_A], 1)
    centre = BLADE_O + BLADE_B * 0.030 + np.array([0, 0.040, 0])
    b.box(centre, (0.100, 0.049, 0.0016), STEEL, op=UNION, r=0.0012, R=Rb)
    b.box(centre + [0, 0.042, 0], (0.100, 0.009, 0.0026), STEEL, k=0.002, r=0.0015, R=Rb)
    b.cylinder(BLADE_O + BLADE_B * 0.110 + np.array([0, 0.070, 0]), 0.01, 0.0085, STEEL, op=SUB,
               R=np.stack([BLADE_B, RACK_A, [0, 1.0, 0]], 1))
    b.box(HEEL + BLADE_B * 0.004 + np.array([0, -0.004, 0]), (0.006, 0.010, 0.0060), STEEL, k=0.002, r=0.002,
          R=Rb)
    b.capsule(HEEL - BLADE_B * 0.006, BUTT, 0.0125, HANDLE, k=0.003)
    for t in (0.030, 0.065, 0.100):
        b.sphere(HEEL - BLADE_B * t + RACK_A * 0.0118, 0.0032, STEEL, k=0.001)
        b.sphere(HEEL - BLADE_B * t - RACK_A * 0.0118, 0.0032, STEEL, k=0.001)


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


def build_environment(b, SP):
    b.set_frame((0, 0, 0), None)
    I = ISLAND
    # --- floor, walls, ceiling
    b.group('room', margin=0.05)
    b.box((0, -0.05, -1.0), (4.0, 0.05, 4.5), FLOOR, op=UNION)
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


def build_head(b, smile=1.0, grid=None):
    """The MakeHuman head (its own nostrils, lids and lips) with eyeballs set in its sockets."""
    b.group('head', margin=0.01)
    lo, d, voxel = grid if grid is not None else get_head_grid()
    b.grid(lo, d, voxel, SKIN, op=UNION)
    for c, r in get_mh_eyes():
        b.sphere(c, r, EYE, op=UNION)


def get_mh_eyes():
    return get_mh_head()[1]


def build_head_sculpted(b, smile=1.0, grid=None):
    """The earlier hand-sculpted head (kept for comparison; see guides/character-anatomy.md for why not)."""
    b.group('head', margin=0.01)
    lo, d, voxel = grid if grid is not None else head_grid(smile=smile)
    b.grid(lo, d, voxel, SKIN, op=UNION)
    for sx in (-1, 1):
        b.ellipsoid((sx * 0.0046, -0.0418, 0.0278), (0.0020, 0.0009, 0.0030), NOSTRIL, op=SUB,
                    R=rot(yaw=sx * 22, pitch=-25))
    cu, ru, cl, rl = eye_opening(smile)
    for sx in (-1, 1):
        c = np.array([sx * EYE_X, 0.0, 0.0])
        # open the lids
        b.lens(c, cu, ru, cl, rl, -0.004, 0.03, SKIN, op=SSUB, k=0.0011, R=np.diag([sx, 1.0, 1.0]))
    for sx in (-1, 1):
        b.sphere((sx * EYE_X, 0.0, 0.0), EYE_R, EYE, op=UNION)


def head_frame(Hc, yaw, pitch, roll):
    return np.asarray(Hc, float), rot(yaw, pitch, roll)


def fill_head_params(SP, Hc, Rh, gaze_local, smile=1.0):
    SP[0:3] = Hc
    SP[3:12] = Rh.reshape(-1)
    for e, sx in ((0, -1), (1, 1)):
        SP[12 + 3 * e:15 + 3 * e] = Hc + Rh @ np.array([sx * EYE_X, 0, 0])
    g = Rh @ (np.asarray(gaze_local, float) / np.linalg.norm(gaze_local))
    SP[18:21] = g
    SP[21] = np.arcsin(0.0059 / EYE_R)
    SP[22] = np.arcsin(0.0019 / EYE_R)
    cu, ru, cl, rl = eye_opening(smile)
    SP[23:29] = [cu[0], cu[1], ru, cl[0], cl[1], rl]
    SP[29] = EYE_X
    # eyebrows: inner end, outer end (from the midline), height, arch, tail drop, thickness
    SP[40:46] = [0.011, 0.056, 0.0168, 0.0050, 0.012, 0.0034]
    L = lip_params(smile)
    SP[100:106] = [L['W'], L['yc'], L['top'], L['bow'], L['stom'], L['bot']]
    SP[107:110] = (0.66, 0.38, 0.36)
    SP[110:114] = HAIRLINE


def default_lights(key_dir=(0.55, 0.45, 0.70)):
    k = np.asarray(key_dir, float)
    k /= np.linalg.norm(k)
    # type, x, y, z, r, g, b, shadow (0 none, 1 traced, 2 shadow map), softness, range, first map, maps
    return np.array([[0, *k, 1.25, 1.18, 1.08, 2, 10.0, 0, 0, 1],
                     [0, -0.6, 0.3, -0.5, 0.30, 0.30, 0.32, 0, 6.0, 0, 0, 0]], dtype=np.float64)


def new_params():
    SP = np.zeros(128)
    SP[60], SP[61] = 0.28, 0.08  # sky fill, flat fill
    SP[62:65] = (1.0, 0.98, 0.96)
    SP[46:49] = (1.0, 0.0, 0.0)
    return SP


def build_test_body(b):
    """Stand-in body (the colliders) so the hair can be judged resting on the shoulders."""
    b.set_frame((0, 0, 0), None)
    b.group('testbody', margin=0.01)
    first = True
    for c in body_colliders():
        op = UNION if first else SUNION
        if c[0] == 'capsule':
            b.capsule(c[1], c[2], c[3], KNIT, op=op, k=0.03)
        else:
            b.ellipsoid(c[1], c[2], KNIT, op=op, k=0.03)
        first = False


def headtest(out, smile=1.0, flags=(0, 0)):
    from PIL import Image
    import time
    t0 = time.time()
    grid = head_grid(smile=smile)
    hgrid = hair_grid()
    print(f'head and hair sculpted in {time.time() - t0:.0f}s', flush=True)
    Rh = head_rotation()
    b = Builder()
    b.set_frame(HEAD_POS, Rh)
    build_head(b, smile, grid)
    build_hair(b, hgrid)
    build_test_body(b)
    P, G = b.build()
    GB = b.grid_buffer()
    SP = new_params()
    fill_head_params(SP, HEAD_POS, Rh, (0.25, -0.12, 1), smile)
    SP[65], SP[66] = flags
    M = mat_table()
    Lt = default_lights((0.75, 0.45, 0.50))
    sm = S.ShadowMaps()
    sm.add(P, G, GB, Lt[0, 1:4], (0, 1.45, -0.74), 0.9, 1600, np.tan(np.radians(8)))
    SM, SMP = sm.arrays()
    face_dir = Rh @ np.array([0, 0, 1.0])
    views = [((0.45, 1.52, 1.9), (0.03, 1.55, -0.73), 13),
             (tuple(HEAD_POS + face_dir * 1.3 + [0, 0.02, 0]), tuple(HEAD_POS + [0, -0.06, 0]), 28),
             ((-1.5, 1.55, -0.60), (0.0, 1.50, -0.73), 28)]
    tiles = []
    for pos, tgt, fov in views:
        cam = S.camera(pos, tgt, fov, 1.0)
        res = S.render_image(560, 560, cam, P, G, M, Lt, SP, GB, SM, SMP, bands=2, verbose=False)
        tiles.append((S.tonemap(res['rgb'], 1.1) * 255).astype(np.uint8))
    Image.fromarray(np.concatenate(tiles, 1)).save(out)
    print('saved', out, f'{time.time() - t0:.0f}s')


def facelab(out, voxel=0.0010, gaze=None, hair=True, flags=(0, 0)):
    """Quick look at the face alone: as the shot sees it, from the front, and in profile, lit by the shot's key
    light (head, hair and a stand-in body only)."""
    from PIL import Image
    import time
    t0 = time.time()
    grid = cached('head', head_grid, [head_grid, robust_distance, eye_opening, lip_params, lip_curves_np,
                                      HEAD_PROFILE.tolist(), HEAD_BOX], voxel, 1.0)
    print(f'head sculpted in {time.time() - t0:.0f}s', flush=True)
    Rh = head_rotation()
    b = Builder()
    b.set_frame(HEAD_POS, Rh)
    build_head(b, 1.0, grid)
    if hair:
        build_hair(b, get_hair_grid())
    build_test_body(b)
    P, G = b.build()
    GB = b.grid_buffer()
    SP = new_params()
    fill_head_params(SP, HEAD_POS, Rh, GAZE if gaze is None else gaze, 1.0)
    SP[65], SP[66] = flags
    M = mat_table()
    key = np.array([0.70, 0.58, 0.42])
    key /= np.linalg.norm(key)
    Lt = np.array([[0, *key, 1.30, 1.26, 1.20, 2, 0, 0, 0, 1],
                   [0, -0.40, 0.30, -0.86, 0.50, 0.54, 0.60, 0, 0, 0, 0, 0]], dtype=np.float64)
    Lt[1, 1:4] /= np.linalg.norm(Lt[1, 1:4])
    sm = S.ShadowMaps()
    sm.add(P, G, GB, key, HEAD_POS + [0, -0.05, 0], 0.6, 1600, np.tan(np.radians(7)))
    SM, SMP = sm.arrays()
    c = HEAD_POS + Rh @ np.array([0, -0.02, 0.0])
    face_dir = Rh @ np.array([0, 0, 1.0])
    side = Rh @ np.array([1.0, 0, 0])
    shot = np.array(CAMERA['pos'])
    views = [(shot, c, 7.0), (c + face_dir * 1.2, c, 13.0), (c - side * 1.2 + face_dir * 0.05, c, 13.0),
             (shot, c + Rh @ np.array([0, -0.01, 0.02]), 3.2)]
    tiles = []
    for pos, tgt, fov in views:
        cam = S.camera(tuple(pos), tuple(tgt), fov, 1.0)
        res = S.render_image(640, 640, cam, P, G, M, Lt, SP, GB, SM, SMP, bands=2, verbose=False)
        tiles.append((S.tonemap(res['rgb'], 1.05) * 255).astype(np.uint8))
    Image.fromarray(np.concatenate([np.concatenate(tiles[:2], 1), np.concatenate(tiles[2:], 1)], 0)).save(out)
    print('saved', out, f'{time.time() - t0:.0f}s')


def _arms():
    return (R_SHOULDER.tolist(), R_ELBOW.tolist(), R_WRIST.tolist(), L_SHOULDER.tolist(), L_ELBOW.tolist(),
            L_WRIST.tolist())


def get_hair_grid():
    return cached('hair', hair_grid, [hair_grid, hair_locks, scalp_point, body_colliders, robust_distance,
                                      HEAD_POS.tolist(), HEAD_YAW, HEAD_PITCH, HEAD_ROLL, _arms(), HAIR_BOX_W, PART, HAIRLINE]
                  + _mh_deps())


def get_body_grid():
    return cached('body', body_grid, [body_grid, robust_distance, BODY_PROFILE.tolist(), _arms(),
                                      NECK_BASE.tolist(), LEAN, BODY_BOX])


def build_character(smile=1.0, cache=None):
    """Head, hair, body, hands and the cleaver, board and meat. Returns builder and scene params."""
    import time
    t0 = time.time()
    cache = {} if cache is None else cache
    if 'head' not in cache:
        cache['head'] = get_head_grid(smile)
        cache['hair'] = get_hair_grid()
        cache['body'] = get_body_grid()
        print(f'  sculpted in {time.time() - t0:.0f}s', flush=True)
    Rh = head_rotation()
    b = Builder()
    b.set_frame(HEAD_POS, Rh)
    build_head(b, smile, cache['head'])
    build_hair(b, cache['hair'])
    build_body(b, cache['body'])
    build_mh_hands(b)
    build_props(b)
    SP = new_params()
    fill_head_params(SP, HEAD_POS, Rh, GAZE, smile)
    SP[114] = 1.0  # the face's lids and lashes are real geometry now: don't paint the old ones on
    SP[115:118], SP[118:121], SP[121:124] = HAM_C, RACK_A, HAM_ACROSS
    SP[124] = (CUT_C - HAM_CUT * RACK_A - HAM_C) @ RACK_A  # where the pink cut face is, along the ham
    # lip colour, fitted to her measured mouth (corners 22 mm out, lips from 52 to 73.5 mm below the eyes)
    SP[100:106] = [0.022, -0.0590, -0.0525, 0.0010, -0.0632, -0.0735]
    board_x = np.array([1.0, 0, 0])
    SP[46:49] = board_x
    return b, SP, cache


def chartest(out):
    from PIL import Image
    import time
    t0 = time.time()
    b, SP, cache = build_character()
    P, G = b.build()
    GB = b.grid_buffer()
    M = mat_table()
    Lt = default_lights((0.75, 0.45, 0.50))
    sm = S.ShadowMaps()
    sm.add(P, G, GB, Lt[0, 1:4], (0, 1.25, -0.55), 1.3, 2048, np.tan(np.radians(8)))
    SM, SMP = sm.arrays()
    tiles = []
    for pos, tgt, fov, W, H in (((0.45, 1.52, 1.9), (0.0, 1.30, -0.55), 26, 900, 600),
                                ((0.15, 1.35, 0.3), (-0.02, 1.02, -0.33), 26, 600, 600)):
        cam = S.camera(pos, tgt, fov, W / H)
        res = S.render_image(W, H, cam, P, G, M, Lt, SP, GB, SM, SMP, bands=4, verbose=False)
        img = (S.tonemap(res['rgb'], 1.1) * 255).astype(np.uint8)
        tiles.append(img)
    canvas = np.full((600, 1500, 3), 230, np.uint8)
    canvas[:, :900] = tiles[0]
    canvas[:, 900:] = tiles[1]
    Image.fromarray(canvas).save(out)
    print('saved', out, f'{time.time() - t0:.0f}s')


CAMERA = dict(pos=(0.85, 1.60, 2.30), target=(0.36, 1.37, -0.55), vfov=19.0)


def scene_lights(P, G, GB, flames):
    key = np.array([0.70, 0.58, 0.42])
    key /= np.linalg.norm(key)
    rim = np.array([-0.40, 0.30, -0.86])
    rim /= np.linalg.norm(rim)
    sm = S.ShadowMaps()
    k0 = sm.add(P, G, GB, key, (0.0, 1.25, -0.55), 1.5, 2400, np.tan(np.radians(7)))
    sm.add(P, G, GB, key, (0.0, 1.2, -0.8), 6.5, 2600, np.tan(np.radians(7)), bias=0.002)
    r0 = sm.add(P, G, GB, rim, (0.0, 1.25, -0.55), 1.5, 1800, np.tan(np.radians(10)))
    sm.add(P, G, GB, rim, (0.0, 1.2, -0.8), 6.5, 2000, np.tan(np.radians(10)), bias=0.002)
    rows = [[0, *key, 1.30, 1.26, 1.20, 2, 0, 0, k0, 2],
            [0, *rim, 0.50, 0.54, 0.60, 2, 0, 0, r0, 2]]
    for (x, z) in PENDANTS:
        rows.append([1, x, 1.925, z, 0.30, 0.25, 0.17, 0, 0, 1.3, 0, 0])
    for f in flames:
        rows.append([1, *f, 0.06, 0.042, 0.022, 0, 0, 0.35, 0, 0])
    rows.append([1, 1.5, 1.7, BACK_Z - 1.0, 0.30, 0.22, 0.12, 0, 0, 2.0, 0, 0])
    Lt = np.array(rows, dtype=np.float64)
    SM, SMP = sm.arrays()
    return Lt, SM, SMP


def render_shot(out_dir, W=1280, H=720, crop=None):
    import time
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    import checks
    checks.run()  # stops here, with a reason, if anything is visibly wrong
    b, SP, cache = build_character()
    flames = build_environment(b, SP)
    P, G = b.build()
    GB = b.grid_buffer()
    M = mat_table()
    print(f'scene: {len(P)} shapes in {len(G)} objects', flush=True)
    Lt, SM, SMP = scene_lights(P, G, GB, flames)
    print(f'shadow maps done {time.time() - t0:.0f}s', flush=True)
    cam = S.camera(CAMERA['pos'], CAMERA['target'], CAMERA['vfov'], W / H)
    res = S.render_image(W, H, cam, P, G, M, Lt, SP, GB, SM, SMP, bands=8, crop=crop)
    tag = f'{W}' if crop is None else f'{W}_crop'
    if crop is not None:
        x0, y0, x1, y1 = crop
        res = {k: v[y0:y1, x0:x1] for k, v in res.items()}
    np.savez_compressed(os.path.join(out_dir, f'passes_{tag}.npz'), cam=cam, SP=SP, **res)
    img = (S.tonemap(res['rgb'], 1.05) * 255).astype(np.uint8)
    Image.fromarray(img).save(os.path.join(out_dir, f'render_{tag}.png'))
    print('rendered', f'{time.time() - t0:.0f}s', flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'render':
        render_shot(sys.argv[2], *(int(v) for v in sys.argv[3:5]))
    if sys.argv[1] == 'facelab':
        facelab(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.0010,
                hair=len(sys.argv) <= 4 or sys.argv[4] != 'nohair',
                flags=tuple(int(v) for v in sys.argv[5].split(',')) if len(sys.argv) > 5 else (0, 0))
    if sys.argv[1] == 'face':  # just her face, at full size
        render_shot(sys.argv[2], 2560, 1440, crop=(560, 60, 1260, 700))
    if sys.argv[1] == 'chartest':
        chartest(sys.argv[2])
    if sys.argv[1] == 'headtest':
        headtest(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1.0,
                 tuple(int(v) for v in sys.argv[4].split(',')) if len(sys.argv) > 4 else (0, 0))
