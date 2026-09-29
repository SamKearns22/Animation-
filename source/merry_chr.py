"""What happened in the spare room: the dressing of the 'Merry Chr' shot (story/horror-merry-chr.md).

- The present: a huge, badly wrapped Christmas present the length of a person on the bed - green paper with
  little gold stars, a crooked gold ribbon and a crushed bow - with shapes pushing at the paper from inside (a
  head, an elbow, a knee, a foot, in the wrong places). Dark liquid has soaked up its paper from below and
  seeps from under it into the sheets, over the side of the mattress and on to the floor.
- 'Merry Chr' written on the bare back wall in fresh blood, wildly, with a forehead: broad smeared strokes
  that thin and break as they drag, drips, and around the last r a growing mess of blood and spatter.
- The wreckage: shredded sheets, broken glass, a burst suitcase of Christmas clothes and small presents, a
  holdall, a pillow, a smashed lamp, a strand of fairy lights.

Shapes the renderer's primitives can't make (crumpled paper, soaked stains, the writing) are worked out here
as distance grids with numpy.
"""
import numpy as np
from scipy import ndimage

import sdf3d as S
import spare_room as R
from cache import cached
from materials import (BLOOD, GORE, GIFTWRAP, RIBBON, GIFT_RED, XMAS_JUMPER, LINEN, GLASS, LEATHER, SHELL,
                       BRASS, FAIRY, BLACKMETAL, PAPER, FELT, FUR, DARKWOOD, COAT, CLOTH_LIGHT, CLOTH_MID, DENIM,
                       PLASTIC, SCREEN, XMAS_GREEN_KNIT, DIRTY_LINEN, GOLD, WOOD, LIGHT_RED, LIGHT_GREEN, LIGHT_BLUE, LIGHT_YELLOW,
                       LIGHT_ORANGE, DEAD_RED, DEAD_GREEN, DEAD_BLUE, DEAD_YELLOW, DEAD_ORANGE, CARD_INK)
from rig import smin, smax, robust_distance
from numba import njit
from sdf3d import rot, UNION, SUNION, SUB

PRESENT_O = np.array([-2.07, 0.672, -2.87])      # its head end, on the sheet; it runs along +x
PRESENT_LEN = 1.62
BOW_U, BOW_W = 0.81, 0.0          # where the ribbon crosses and the bow sits: the middle of its top


# ---------------------------------------------------------------------------
# numpy shape tools
# ---------------------------------------------------------------------------
def noise3(P, scale, seed=0):
    """Smooth value noise in -1..1 at points P (..., 3), features about `scale` apart."""
    g = np.random.default_rng(seed).uniform(-1, 1, (24, 24, 24))
    q = (np.moveaxis(P, -1, 0) / scale) % 24
    return ndimage.map_coordinates(g, q.reshape(3, -1), order=3, mode='grid-wrap').reshape(P.shape[:-1])


def noise2(X, Y, scale, seed=0):
    g = np.random.default_rng(seed).uniform(-1, 1, (48, 48))
    q = np.stack([np.broadcast_to(X, np.broadcast(X, Y).shape), np.broadcast_to(Y, np.broadcast(X, Y).shape)])
    q = (q / scale) % 48
    return ndimage.map_coordinates(g, q.reshape(2, -1), order=3, mode='grid-wrap').reshape(q.shape[1:])


def noise1(x, seed=0):
    g = np.random.default_rng(seed).uniform(-1, 1, 512)
    return np.interp(np.asarray(x) % 511, np.arange(512), g)


def sd_ellipsoid(P, c, r):
    q = (P - c) / r
    k0 = np.linalg.norm(q, axis=-1)
    k1 = np.linalg.norm(q / r, axis=-1)
    return k0 * (k0 - 1) / np.maximum(k1, 1e-9)


def sd_capsule(P, a, b, r):
    a, b = np.asarray(a, float), np.asarray(b, float)
    pa, ba = P - a, b - a
    h = np.clip((pa @ ba) / (ba @ ba), 0, 1)
    return np.linalg.norm(pa - h[..., None] * ba, axis=-1) - r


def sd_box(P, c, half, r=0.0):
    q = np.abs(P - c) - (np.asarray(half) - r)
    return np.linalg.norm(np.maximum(q, 0), axis=-1) + np.minimum(q.max(-1), 0) - r


def grid_points(lo, hi, vox):
    n = np.round((np.asarray(hi) - lo) / vox).astype(int) + 1
    axes = [lo[q] + np.arange(n[q]) * vox for q in range(3)]
    return np.stack(np.meshgrid(*axes, indexing='ij'), -1).astype(np.float32), n


def sdf2(mask, px):
    """Signed distance (metres, negative inside) of a 2D mask."""
    return ((ndimage.distance_transform_edt(~mask) - ndimage.distance_transform_edt(mask)) * px).astype(np.float32)


# ---------------------------------------------------------------------------
# the present
# ---------------------------------------------------------------------------
def _inside_parts(Q):
    """What pushes at the paper from inside, in the present's frame (u along it from the head end, v up, w
    towards the room): a head, a torso, a separate hip, an arm bent up in an elbow, legs at wrong angles, a
    foot against the far end."""
    parts = [sd_ellipsoid(Q, (0.14, 0.11, 0.03), (0.11, 0.10, 0.09)),                    # head
             sd_ellipsoid(Q, (0.50, 0.12, 0.00), (0.28, 0.11, 0.18)),                    # chest
             sd_ellipsoid(Q, (0.90, 0.10, -0.04), (0.15, 0.10, 0.16)),                   # hips, turned away
             sd_capsule(Q, (0.36, 0.14, 0.14), (0.54, 0.33, 0.11), 0.045),               # an elbow sticking up
             sd_capsule(Q, (0.54, 0.33, 0.11), (0.70, 0.18, 0.13), 0.040),
             sd_capsule(Q, (0.98, 0.10, -0.10), (1.25, 0.28, -0.12), 0.065),             # a knee up
             sd_capsule(Q, (1.25, 0.28, -0.12), (1.50, 0.09, -0.07), 0.052),
             sd_capsule(Q, (1.00, 0.08, 0.13), (1.40, 0.09, 0.18), 0.050),               # a leg, the wrong way
             sd_capsule(Q, (0.78, 0.08, 0.20), (1.05, 0.10, 0.19), 0.042),               # a forearm, loose
             sd_ellipsoid(Q, (1.56, 0.13, 0.02), (0.05, 0.10, 0.05))]                    # a foot, toes up
    d = parts[0]
    for p in parts[1:]:
        d = smin(d, p, 0.03)
    return d


def present_grids(vox=0.004):
    """The wrapped present: (paper, ribbon, soaked stains), each (lo, d, voxel) in the world."""
    lo = PRESENT_O + np.array([-0.12, -0.04, -0.34])
    hi = PRESENT_O + np.array([PRESENT_LEN + 0.14, 0.50, 0.34])
    P, n = grid_points(lo, hi, vox)
    Q = P - PRESENT_O
    u, v, w = Q[..., 0], Q[..., 1], Q[..., 2]
    inner = _inside_parts(Q) - 0.012
    bag = sd_box(Q, (PRESENT_LEN / 2, 0.10, 0.0), (PRESENT_LEN / 2, 0.10, 0.21), 0.08)
    d = smin(inner, bag + 0.01, 0.10)
    # gathered and crumpled at both ends, as if the paper ran out; creased all over
    ends = np.clip(1 - np.minimum(u + 0.02, PRESENT_LEN + 0.02 - u) / 0.14, 0, 1)
    d = d + 0.005 * noise3(Q, 0.06, 1) + 0.0025 * noise3(Q, 0.022, 2) + 0.016 * ends * noise3(Q, 0.035, 3)
    d = smax(d, -(v + 0.012), 0.02)          # resting on the bed, sunk a little into it
    paper = robust_distance(d.astype(np.float32), vox)
    # the ribbon: tied round its middle, under the bow, pulled a little crooked by the shapes under the paper
    # (a second one along its length spread into wide gold wedges over the humps: left off)
    band = np.full(u.shape, 1.0, np.float32)
    for c, nrm, half in (((BOW_U, 0, 0), (1.0, 0.04, 0.10), 0.024),):
        nn = np.asarray(nrm) / np.linalg.norm(nrm)
        band = np.minimum(band, np.abs((Q - c) @ nn) - half)
    ribbon = smax(paper - 0.0025, band, 0.002)
    # the stains: soaked up from below (higher on the side that lies in it), in blotches over the head, the
    # hips and the knee, running down the side
    soak = (0.05 + 0.035 * noise3(Q, 0.07, 4) + 0.03 * np.clip(w / 0.2, 0, 1)) - v
    blot = -1.0
    # (soaked through from inside where the shapes press on the paper, low on their sides rather than capping
    # their tops; ragged, broken edges - never neat circles)
    for c, r in (((0.14, 0.07, 0.13), 0.10), ((0.90, 0.08, 0.12), 0.15), ((1.22, 0.18, 0.04), 0.06),
                 ((0.55, 0.27, 0.12), 0.045), ((0.40, 0.10, 0.20), 0.10)):
        rr = r * (1 + 0.55 * noise3(Q, 0.05, 5) + 0.22 * noise3(Q, 0.02, 8))
        blot = np.maximum(blot, rr - np.linalg.norm((Q - c) * np.array([0.8, 1.2, 1.0]), axis=-1))
    runs = (0.012 - np.abs(((u * 7.3 + 0.3 * noise3(Q, 0.1, 6)) % 1.0) - 0.5) * 0.12) * (v < 0.22) * (w > 0.05) \
        * (noise3(Q * np.array([1, 0.1, 1]), 0.08, 7) > 0.1)
    stain = np.maximum(np.maximum(soak, blot), runs - 0.0001 * (runs == 0))
    gore = smax(paper - 0.0018, -stain, 0.001)
    ribbon = smax(ribbon, stain, 0.001)          # the stain soaks the ribbon too
    return (lo, paper, vox), (lo, robust_distance(ribbon.astype(np.float32), vox), vox), \
        (lo, robust_distance(gore.astype(np.float32), vox), vox)


def side_of(grid, u, v):
    """How far the present's paper reaches towards the room (+w) at u along it, v above the sheet."""
    lo, d, vox = grid
    p = PRESENT_O + np.array([u, v, 0])
    i, j = int((p[0] - lo[0]) / vox), int((p[1] - lo[1]) / vox)
    row = d[i, j, :]
    k = np.nonzero(row < 0)[0].max()
    return lo[2] + (k + 0.5) * vox - PRESENT_O[2]


def top_of(grid, u, w):
    """Height of the top of a world grid above a point in the present's frame (for the bow)."""
    lo, d, vox = grid
    p = PRESENT_O + np.array([u, 0, w])
    i, k = int((p[0] - lo[0]) / vox), int((p[2] - lo[2]) / vox)
    col = d[i, :, k]
    j = np.nonzero(col < 0)[0].max()
    return lo[1] + (j + 0.5) * vox


# ---------------------------------------------------------------------------
# the bed: mattress and sheets, sodden under the present
# ---------------------------------------------------------------------------
# (x, where it ends) of the runs down the side of the mattress that faces the door; the lowest carry on down
# the bed's rail (rail_gore)
SIDE_RUNS = [(-1.72, 0.55), (-1.55, 0.50), (-1.40, 0.45), (-1.29, 0.45), (-1.16, 0.45), (-1.02, 0.47),
             (-0.90, 0.45), (-0.74, 0.52), (-0.60, 0.58)]


def bed_grids(vox=0.006):
    """The made-up mattress (lumpy, torn sheets) and the dark stain soaked into it, draining over the front
    edge. Returns (sheet, stain), world grids."""
    B = R.BED
    lo = np.array([B['x0'] - 0.02, 0.40, B['z0'] - 0.02])
    hi = np.array([B['x1'] + 0.03, B['top'] + 0.08, B['z1'] + 0.03])
    P, n = grid_points(lo, hi, vox)
    x, y, z = P[..., 0], P[..., 1], P[..., 2]
    c = np.array([(B['x0'] + B['x1']) / 2, (B['top'] + 0.44) / 2, (B['z0'] + B['z1']) / 2])
    half = np.array([(B['x1'] - B['x0']) / 2, (B['top'] - 0.44) / 2, (B['z1'] - B['z0']) / 2])
    d = sd_box(P, c, half, 0.045)
    # rumpled: the sheet pulled and twisted, sagging under the weight
    Q = P - PRESENT_O
    under = np.exp(-(np.maximum(np.abs(Q[..., 2]) - 0.15, 0) / 0.12) ** 2) * (Q[..., 0] > -0.05) * (Q[..., 0] < PRESENT_LEN + 0.05)
    d = d - 0.010 * noise3(P * np.array([1, 3, 1]), 0.12, 11) - 0.004 * noise3(P, 0.04, 12) + 0.014 * under * (y > B['top'] - 0.05)
    sheet = robust_distance(d.astype(np.float32), vox)
    # the stain: round and under the present, a tongue of it running to the front edge and over it in runs
    ux = x - PRESENT_O[0]
    foot = np.maximum(np.maximum(-ux, ux - PRESENT_LEN), np.abs(z - PRESENT_O[2]) - 0.2)
    top = 0.13 + 0.07 * noise2(x, z, 0.12, 13) - foot
    tongue = 0.035 + 0.02 * noise2(x, z, 0.05, 14) - np.abs(x - (-1.22 + 0.06 * np.sin(z * 9))) * \
        (1 + 0.5 * (z < -2.4)) - np.maximum(-2.5 - z, 0)
    tongue2 = 0.02 + 0.015 * noise2(x, z, 0.05, 15) - np.abs(x + 0.78) - np.maximum(-2.5 - z, 0)
    front = z > B['z1'] - 0.02
    # over the front edge it has soaked down into the side of the mattress in a ragged tide mark, and one
    # trickle has wandered on down
    edge = (B['top'] - 0.04 - 0.035 * (1 + noise2(x, y, 0.04, 16)) * (np.abs(x + 1.2) < 0.25)) - y
    edge = np.where(np.abs(x + 1.2) < 0.28 + 0.05 * noise2(x, y, 0.05, 17), -edge, -1.0)
    # runs down the side of the mattress, where it poured over the edge: many, of different lengths, some
    # right down to the rail
    runs = np.full(x.shape, -1.0)
    rng = np.random.default_rng(19)
    for xr, low in SIDE_RUNS:
        tx = xr + 0.010 * np.sin(y * 50 + xr * 7) + 0.006 * noise2(x * 0, y, 0.03, 18)
        wdt = 0.004 + 0.003 * rng.random() + 0.004 * np.clip((y - low) / 0.15, 0, 1)
        runs = np.maximum(runs, (wdt - np.abs(x - tx)) * (y > low) - 1.0 * (y <= low))
        runs = np.maximum(runs, 0.008 - np.hypot(x - xr, y - low - 0.004))          # the bead at its end
    # a wider tide mark soaked along the top of the side under the stain
    tide = np.where(np.abs(x + 1.15) < 0.42 + 0.10 * noise2(x, y, 0.05, 20),
                    y - (B['top'] - 0.05 - 0.035 * (1 + noise2(x, y * 0, 0.03, 21))), -1.0)
    runs = np.maximum(runs, tide)
    # spatter flung across the side of the mattress
    for _ in range(90):
        cx_, cy_ = rng.uniform(-1.95, -0.45), rng.uniform(0.46, B['top'] - 0.02)
        runs = np.maximum(runs, 0.002 + 0.006 * rng.random() ** 2 - np.hypot(x - cx_, y - cy_))
    stain = np.maximum(np.maximum(top, tongue), tongue2)
    stain = np.where(front & (y < B['top'] - 0.03), runs, stain)
    gore = smax(sheet - 0.0022, -stain, 0.001)
    return (lo, sheet, vox), (lo, robust_distance(gore.astype(np.float32), vox), vox)


# ---------------------------------------------------------------------------
# the writing on the wall
# ---------------------------------------------------------------------------
# each letter: strokes as points in letter units (the capital's height = 1), and its width
LETTERS = {
    'M': ([[(0.0, 0.0), (0.06, 1.0), (0.45, 0.28), (0.86, 1.06), (0.97, -0.02)]], 1.0),
    'e': ([[(0.04, 0.30), (0.60, 0.36), (0.57, 0.58), (0.30, 0.63), (0.05, 0.40), (0.12, 0.07), (0.42, -0.01),
            (0.66, 0.09)]], 0.72),
    'r': ([[(0.10, -0.02), (0.08, 0.62)], [(0.09, 0.36), (0.30, 0.58), (0.60, 0.60)]], 0.64),
    'y': ([[(0.02, 0.62), (0.34, 0.10)], [(0.68, 0.64), (0.42, 0.04), (0.22, -0.32), (-0.02, -0.38)]], 0.70),
    'C': ([[(0.88, 0.82), (0.62, 1.0), (0.30, 0.94), (0.06, 0.62), (0.08, 0.26), (0.32, 0.0), (0.66, 0.0),
            (0.90, 0.16)]], 0.92),
    'h': ([[(0.12, 1.06), (0.08, -0.02)], [(0.10, 0.40), (0.34, 0.62), (0.60, 0.54), (0.64, -0.02)]], 0.74),
    ' ': ([], 0.45),
}
TEXT = 'Merry Chr'
LAST_R_SCALE = 1.45
WALL_LO, WALL_HI, WALL_PX = (-2.40, 0.0), (1.20, 1.95), 0.003


CARD_TEXT = 'To Mum x'
# a quick hand: strokes in units of the letter height, each glyph with its width
HAND = {
    'T': ([[(0.0, 1.0), (0.62, 1.03)], [(0.30, 1.02), (0.28, 0.0)]], 0.62),
    'o': ([[(0.30, 0.58), (0.08, 0.45), (0.06, 0.12), (0.28, 0.0), (0.48, 0.14), (0.47, 0.46), (0.30, 0.58)]], 0.55),
    'M': ([[(0.0, 0.0), (0.08, 1.0), (0.40, 0.35), (0.72, 1.0), (0.80, 0.0)]], 0.85),
    'u': ([[(0.02, 0.60), (0.04, 0.12), (0.24, 0.0), (0.44, 0.15), (0.46, 0.60)], [(0.46, 0.60), (0.49, 0.0)]], 0.56),
    'm': ([[(0.0, 0.0), (0.0, 0.58)], [(0.0, 0.42), (0.16, 0.60), (0.30, 0.45), (0.30, 0.0)],
           [(0.30, 0.42), (0.46, 0.60), (0.60, 0.45), (0.60, 0.0)]], 0.68),
    'x': ([[(0.0, 0.02), (0.36, 0.56)], [(0.0, 0.56), (0.36, 0.02)]], 0.4),
    ' ': ([], 0.3),
}


def handwriting(text, height):
    """Pen strokes (lists of (x, y) in metres, from the start of the line) writing text."""
    out, x = [], 0.0
    for ch in text:
        strokes, w = HAND[ch]
        out += [[(x + a * height, b_ * height) for a, b_ in st] for st in strokes]
        x += (w + 0.12) * height
    return out


def smooth_path(pts, step):
    """A sloppy hand's curve through the points (Catmull-Rom), sampled every `step`."""
    pts = np.asarray(pts, float)
    if len(pts) == 2:
        L = np.linalg.norm(pts[1] - pts[0])
        return pts[0] + (pts[1] - pts[0]) * np.linspace(0, 1, max(2, int(L / step)))[:, None]
    P = np.vstack([2 * pts[0] - pts[1], pts, 2 * pts[-1] - pts[-2]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        L = np.linalg.norm(p2 - p1)
        for t in np.linspace(0, 1, max(2, int(L / step)), endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(pts[-1])
    return np.array(out)


def layout(r_centre):
    """Where each letter's strokes go on the wall (metres), so the last r's middle lands on r_centre (x, y):
    big and energetic at first, then smaller, lower and wilder as he weakens."""
    rng = np.random.default_rng(21)
    items = []
    x = 0.0
    for i, ch in enumerate(TEXT):
        strokes, wdt = LETTERS[ch]
        late = i >= 6
        cap = (0.44 if not late else 0.40 + 0.03 * (i == 8)) * rng.uniform(0.90, 1.12)
        if i == len(TEXT) - 1:
            cap *= LAST_R_SCALE      # the last r: big enough to read round his head from the doorway
        base = 0.06 * np.sin(i * 1.7) + rng.normal(0, 0.02) - (0.03 * (i - 5) if late else 0.0)
        tilt = np.radians(rng.normal(0, 8 if not late else 11))
        Rt = np.array([[np.cos(tilt), -np.sin(tilt)], [np.sin(tilt), np.cos(tilt)]])
        for s in strokes:
            p = np.array(s, float) * cap
            p = p + rng.normal(0, 0.016 if not late else 0.024, p.shape)
            # the forehead overshoots the end of a stroke as it is dragged off
            p = np.vstack([p, p[-1] + (p[-1] - p[-2]) * rng.uniform(0.05, 0.25)])
            p = p @ Rt.T + np.array([x, base])
            items.append((i, p, late))
            if rng.random() < 0.55 and len(p) > 2:
                # gone over again, not quite in the same place, only part of the way
                n2 = max(2, int(len(p) * rng.uniform(0.4, 0.9)))
                q = p[:n2] + rng.normal(0, 0.014, 2) + rng.normal(0, 0.006, (n2, 2))
                items.append((i, q, late))
        x += wdt * cap + (0.055 if i != 7 else 0.09)
    # the last r's middle
    last = [p for i, p, _ in items if i == len(TEXT) - 1]
    allp = np.vstack(last)
    off = np.asarray(r_centre) - (allp.min(0) + allp.max(0)) / 2
    return [(i, p + off, late) for i, p, late in items]


def wall_profile(y):
    """How far the back wall's surface stands out at height y (skirting, panels, dado rail)."""
    prof = np.zeros_like(y)
    prof = np.where(y < 0.18, 0.028, prof)
    prof = np.where((y >= 0.18) & (y < 0.195), 0.036, prof)
    prof = np.where((y >= 0.28) & (y < 0.76), 0.024, prof)
    prof = np.where((y >= R.DADO - 0.022) & (y < R.DADO + 0.022), 0.044, prof)
    return prof


def wall_blood(r_centre, contact):
    """The writing, its drips and the mess round the last r, as a world grid over the back wall.
    contact: where his forehead meets the wall (x, y)."""
    rng = np.random.default_rng(5)
    px = WALL_PX
    nx, ny = int((WALL_HI[0] - WALL_LO[0]) / px), int((WALL_HI[1] - WALL_LO[1]) / px)
    X = WALL_LO[0] + (np.arange(nx) + 0.5) * px
    Y = WALL_LO[1] + (np.arange(ny) + 0.5) * px
    mask = np.zeros((nx, ny), bool)
    thick = np.zeros((nx, ny), np.float32)

    def stamp(c, rad, t=None, keep=None, h=0.0012):
        i0, i1 = int((c[0] - rad - WALL_LO[0]) / px), int((c[0] + rad - WALL_LO[0]) / px) + 2
        j0, j1 = int((c[1] - rad - WALL_LO[1]) / px), int((c[1] + rad - WALL_LO[1]) / px) + 2
        i0, j0, i1, j1 = max(i0, 0), max(j0, 0), min(i1, nx), min(j1, ny)
        if i1 <= i0 or j1 <= j0:
            return
        dx, dy = X[i0:i1, None] - c[0], Y[None, j0:j1] - c[1]
        inside = dx * dx + dy * dy < rad * rad
        if keep is not None:
            inside &= keep(dx, dy)
        mask[i0:i1, j0:j1] |= inside
        thick[i0:i1, j0:j1] = np.maximum(thick[i0:i1, j0:j1], inside * h)

    drips = []
    items = layout(r_centre)
    for k, (i, pts, late) in enumerate(items):
        path = smooth_path(pts, 0.004)
        seg = np.diff(path, axis=0)
        s = np.concatenate([[0], np.cumsum(np.linalg.norm(seg, axis=1))])
        tang = np.vstack([seg, seg[-1:]])
        tang /= np.linalg.norm(tang, axis=1, keepdims=True) + 1e-9
        width0 = (0.066 if not late else 0.058) * (1 + 0.2 * rng.normal())
        last = i == len(TEXT) - 1
        if last:
            width0 *= 1.25           # pressed hard: the r is bold
        # where the forehead first pressed on: a blot, smeared the way it then dragged
        blot = path[0] - tang[0] * 0.01
        for q in range(4):
            stamp(blot + tang[0] * q * 0.008 + rng.normal(0, 0.005, 2), width0 * rng.uniform(0.32, 0.48), h=0.0024)
        for c, sc, t in zip(path, s, tang):
            load = np.exp(-sc / (0.7 if not late else (0.9 if last else 0.4)))   # the blood runs out along a stroke
            # uneven pressure: the head rocks as it drags, pressing wide, then skidding thin
            press = 1 + 0.40 * noise1(sc * 7 + k * 17, k) + 0.15 * noise1(sc * 30 + k * 5, 50 + k)
            wdt = width0 * (0.45 + 0.55 * load) * max(press, 0.35)
            nrm = np.array([-t[1], t[0]])
            dry = 0.55 * (1 - load) + 0.05

            def keep(dx, dy, nrm=nrm, k=k, dry=dry, sc=sc):
                o = (dx * nrm[0] + dy * nrm[1]) / wdt
                # the streaks a dragged forehead leaves (skin and hair), breaking up as it dries
                streak = noise1(o * 26 + k * 31, 100 + k) * 0.5 + 0.5
                return streak > dry * (0.7 + 0.3 * noise1(sc * 25 + k, 200 + k))
            stamp(c, wdt / 2, keep=keep, h=0.0010 + 0.0008 * load)
            if rng.random() < 0.06 * (0.3 + load) and t[0] ** 2 > 0.05:
                drips.append((c + np.array([0, -wdt * 0.35]), load))
    # smudges where his face slid across the wall between letters: pale, broad, streaky wipes
    for i in range(len(TEXT) - 1):
        own = [p for j, p, _ in items if j == i]
        if not own:
            continue
        pts_i = np.vstack(own)
        c0 = pts_i.mean(0) + rng.normal(0, 0.05, 2)
        a = rng.uniform(-0.5, 0.5)
        L = rng.uniform(0.10, 0.25)
        for q in np.linspace(0, 1, 30):
            c = c0 + np.array([np.cos(a), np.sin(a)]) * L * q
            nrm = np.array([-np.sin(a), np.cos(a)])

            def keep(dx, dy, nrm=nrm, i=i):
                o = (dx * nrm[0] + dy * nrm[1]) / 0.08
                return noise1(o * 30 + i * 9, 500 + i) > 0.35 + 0.5 * q
            if rng.random() < 0.7:
                stamp(c, 0.04, keep=keep, h=0.0008)
    # drips run down from the heavy parts
    for c, load in drips:
        L = (0.03 + 0.30 * load * rng.random()) * (1.3 if c[0] > r_centre[0] - 0.8 else 1.0)
        wdt = 0.004 + 0.004 * load * rng.random()
        y_end = max(c[1] - L, R.DADO + 0.024)
        ys = np.arange(c[1], y_end, -0.003)
        xw = c[0] + 0.004 * np.cumsum(rng.normal(0, 0.15, len(ys)))
        for x_, y_ in zip(xw, ys):
            stamp((x_, y_), wdt / 2 * (0.8 + 0.2 * rng.random()), h=0.0016)
        stamp((xw[-1] if len(xw) else c[0], y_end), wdt * 0.9, h=0.0028)       # the bead at the end
    # the mess round the last r: where his forehead keeps striking, a blotch, spattered all round, running
    sel = (np.abs(X[:, None] - contact[0]) < 0.25) & (np.abs(Y[None, :] - contact[1]) < 0.25)
    dx, dy = X[:, None] - contact[0], Y[None, :] - contact[1]
    a = np.arctan2(dy, dx / 1.1)
    rad = 0.085 * (1 + 0.35 * noise1(a * 3 + 20, 300) + 0.15 * noise1(a * 11 + 50, 301))
    inb = sel & (np.hypot(dx / 1.1, dy) < rad)
    mask |= inb
    thick[inb] = 0.0026
    # the circle of spatter his strikes have thrown out, again and again, all round the one spot: dense close
    # in, thinning outwards, each drop with a tail flying away from the middle
    for _ in range(700):
        a = rng.uniform(0, 2 * np.pi)
        dist = 0.09 + 0.36 * rng.random() ** 1.6
        c = contact + dist * np.array([np.cos(a), np.sin(a) * 0.85])
        r0 = max(0.0015, 0.009 * (1 - dist / 0.5) * rng.random() ** 0.8)
        stamp(c, r0, h=0.0014)
        if rng.random() < 0.6:
            for q in range(1, 4):
                stamp(c + q * r0 * 1.2 * np.array([np.cos(a), np.sin(a) * 0.85]), r0 * (1 - q * 0.22), h=0.001)
    for xr in contact[0] + np.array([-0.075, -0.03, 0.02, 0.06, 0.09]) + rng.normal(0, 0.01, 5):
        # heavy runs from the blotch, all the way down to the rail, and on down the panels to the floor
        ys = np.arange(contact[1] - 0.05, 0.0, -0.003)
        xw = xr + 0.003 * np.cumsum(rng.normal(0, 0.2, len(ys)))
        wd = 0.007 + 0.006 * rng.random()
        for x_, y_ in zip(xw, ys):
            stamp((x_, y_), wd / 2, h=0.0022)
    # the pool along the top of the dado rail, where the runs meet it
    for x_ in np.arange(contact[0] - 0.14, contact[0] + 0.16, 0.003):
        stamp((x_, R.DADO + 0.024), 0.005 + 0.003 * (noise1(x_ * 80, 400) + 1), h=0.003)
    # a little spatter low on the wall beside the en-suite doorway, carried in from there (dropped and flicked
    # from something dripping), a few with short runs
    for _ in range(45):
        c = np.array([rng.uniform(0.98, 1.18), 0.03 + 0.45 * rng.random() ** 1.5])
        r0 = 0.0015 + 0.004 * rng.random() ** 2
        stamp(c, r0, h=0.0012)
        if rng.random() < 0.15:
            for y_ in np.arange(c[1], max(c[1] - rng.uniform(0.02, 0.08), 0.005), -0.003):
                stamp((c[0], y_), r0 * 0.6, h=0.0012)
    thick = ndimage.gaussian_filter(thick, 1.0)
    d2 = sdf2(mask, px)
    # into 3D: a thin skin of blood standing proud of the wall's surface (which steps out at the panels, the
    # rail and the skirting)
    z0 = R.BACK_Z - 0.004
    nz = int(0.056 / px) + 1
    Z = z0 + np.arange(nz) * px
    surf = R.BACK_Z + wall_profile(Y)
    zrel = Z[None, None, :] - surf[None, :, None]
    h = np.maximum(thick, 0.0008)[:, :, None]
    d = np.maximum(np.maximum(d2[:, :, None], zrel - h), -(zrel + 0.006))
    lo = np.array([X[0], Y[0], z0])
    return lo, d.astype(np.float32), px


def floor_pools(vox=0.003):
    """Dark pools on the floorboards: under the bed's front edge, where the runs from the mattress drip."""
    dz = R.BED['z1'] + 1.65              # (laid out for the bed's front edge at z = -1.65)
    lo2, hi2 = np.array([-1.55, -1.66 + dz]), np.array([-0.60, -1.12 + dz])
    nx, nz = ((hi2 - lo2) / vox).astype(int)
    X = lo2[0] + (np.arange(nx) + 0.5) * vox
    Zc = lo2[1] + (np.arange(nz) + 0.5) * vox
    XX, ZZ = np.meshgrid(X, Zc, indexing='ij')
    ZZ = ZZ - dz
    f = 0.13 * (1 + 0.4 * noise2(XX, ZZ, 0.06, 41)) - np.hypot((XX + 1.22) / 1.4, ZZ + 1.50)
    f = np.maximum(f, 0.05 * (1 + 0.5 * noise2(XX, ZZ, 0.03, 42)) - np.hypot(XX + 0.80, (ZZ + 1.52) * 1.3))
    for cx, cz, r in ((-0.98, -1.30, 0.012), (-1.02, -1.24, 0.008), (-1.45, -1.40, 0.010), (-0.70, -1.40, 0.009)):
        f = np.maximum(f, r - np.hypot(XX - cx, ZZ - cz))
    mask = f > 0
    d2 = sdf2(mask, vox)
    ny = 6
    Yc = -0.004 + np.arange(ny) * vox
    d = np.maximum(np.maximum(d2[:, None, :], Yc[None, :, None] - 0.0025), -(Yc[None, :, None] + 0.004))
    return np.array([X[0], Yc[0], Zc[0]]), d.astype(np.float32), vox


# ---------------------------------------------------------------------------
# putting it in the scene
# ---------------------------------------------------------------------------
def deps():
    import inspect
    import sys
    return [inspect.getsource(sys.modules[__name__]), R.BED, R.BACK_Z]


def build(b, man_state=None, contact=None, r_centre=None, t=0.0):
    """Everything that happened in the room. contact: where his forehead meets the wall (world x, y);
    r_centre: the middle of the last r."""
    b.set_frame((0, 0, 0), None)
    paper, ribbon, gore = cached('present', present_grids, deps())
    b.group('present', margin=0.02)
    b.grid(*paper, GIFTWRAP, op=UNION)
    b.group('present_ribbon', margin=0.01)
    b.grid(*ribbon, RIBBON, op=UNION)
    b.group('present_gore', margin=0.01)
    b.grid(*gore, GORE, op=UNION)
    # a gold satin bow in the middle, where the ribbon crosses, spotted with what has soaked
    # through
    b.group('bow', margin=0.03)
    yt = top_of(paper, BOW_U, BOW_W)
    bc = np.array([PRESENT_O[0] + BOW_U, yt - 0.004, PRESENT_O[2] + BOW_W])
    satin_bow(b, bc, 8, RIBBON)
    for off in ((0.03, 0.02, 0.012), (-0.04, 0.012, -0.01)):
        b.ellipsoid(bc + np.array(off), (0.006, 0.004, 0.007), GORE, op=UNION)
    # a Christmas card in its envelope, propped against the present's side on the sheet
    b.group('card', margin=0.02)
    u = 0.72
    w = side_of(paper, u, 0.08)
    base = np.array([PRESENT_O[0] + u, R.BED['top'] + 0.004, PRESENT_O[2] + w + 0.035])
    Rc = rot(-8) @ rot(0, -18, 0)                        # leaning back against the paper
    # plain, white and clean - as if set down gently, afterwards
    b.box(base + Rc @ np.array([0, 0.058, 0]), (0.085, 0.058, 0.0025), PAPER, op=UNION, r=0.001, R=Rc)
    # written on it, small and faint in pen: 'To Mum x' (too far from the doorway to read)
    b.group('card_writing', margin=0.01)
    for stroke in handwriting(CARD_TEXT, 0.015):
        pts = [base + Rc @ np.array([x - 0.040, y + 0.052, 0.0026]) for x, y in stroke]
        for p, q in zip(pts[:-1], pts[1:]):
            b.capsule(p, q, 0.0007, CARD_INK, op=UNION)
    b.group('tape', margin=0.01)
    ty = top_of(paper, 1.45, 0.0)
    b.box((PRESENT_O[0] + 1.45, ty - 0.004, PRESENT_O[2]), (0.02, 0.003, 0.16), PAPER, op=UNION, R=rot(12, 0, 0))
    # the soaked bed
    sheet, sheet_gore = cached('bedsheets', bed_grids, deps())
    b.group('mattress', margin=0.02)
    b.grid(*sheet, LINEN, op=UNION)
    b.group('mattress_gore', margin=0.01)
    b.grid(*sheet_gore, GORE, op=UNION)
    # drips down the bed rail, and pools on the floor
    b.group('rail_gore', margin=0.01)
    rng = np.random.default_rng(23)
    zr = R.BED['z1'] + 0.032                     # the front face of the rail
    for xr, low in SIDE_RUNS:
        if low > 0.46:
            continue
        # carried on down the rail's face, wandering, thinning; a bead at the end or a drip to the floor
        end = rng.uniform(0.25, 0.40)
        ys = np.arange(0.48, end, -0.012)
        xs = xr + 0.004 * np.cumsum(rng.normal(0, 0.4, len(ys)))
        for (x0, y0), (x1_, y1) in zip(zip(xs[:-1], ys[:-1]), zip(xs[1:], ys[1:])):
            b.capsule((x0, y0, zr), (x1_, y1, zr), 0.0035, GORE, op=UNION)
        b.sphere((xs[-1], ys[-1], zr + 0.001), 0.0055, GORE, op=UNION)
    for _ in range(40):                          # spatter on the rail
        b.ellipsoid((rng.uniform(-1.9, -0.5), rng.uniform(0.26, 0.47), zr), np.array((0.004, 0.004, 0.0015))
                    * rng.uniform(0.5, 1.6), GORE, op=UNION)
    # blood on the en-suite's round mirror: a smear dragged down and across it, spatter round it, two runs
    b.group('mirror_blood', margin=0.01)
    ec, zm = sum(R.ENSUITE) / 2, R.BACK_Z - 2.2 + 0.0405       # the mirror's face
    rng = np.random.default_rng(31)
    for q in np.linspace(0, 1, 40):                             # the smear, thinning and breaking as it drags
        if rng.random() < 0.25 * q:
            continue
        c = np.array([ec - 0.08 + 0.13 * q, 1.66 - 0.20 * q ** 1.3]) + rng.normal(0, 0.004, 2)
        r0 = 0.022 * (1 - 0.6 * q) * rng.uniform(0.7, 1.0)
        b.ellipsoid((c[0], c[1], zm), (r0, r0 * 0.8, 0.0008), BLOOD, op=UNION)
    for _ in range(45):                                         # spatter
        a, dist = rng.uniform(0, 2 * np.pi), 0.05 + 0.20 * rng.random()
        c = np.array([ec - 0.04 + dist * np.cos(a), 1.58 + dist * np.sin(a)])
        if np.hypot(c[0] - ec, c[1] - 1.55) > 0.31:           # only on the glass
            continue
        r0 = 0.0015 + 0.004 * rng.random() ** 2
        b.ellipsoid((c[0], c[1], zm), (r0, r0, 0.0006), BLOOD, op=UNION)
    for xr, y0, L in ((ec - 0.02, 1.50, 0.16), (ec + 0.04, 1.47, 0.10)):   # runs from the smear
        b.capsule((xr, y0, zm), (xr + 0.004, y0 - L, zm), 0.0025, BLOOD, op=UNION)
        b.sphere((xr + 0.004, y0 - L, zm), 0.004, BLOOD, op=UNION)
    # a sparse trail of drops on the boards, carried in from the en-suite towards where he kneels
    b.group('floor_drops', margin=0.01)
    rng = np.random.default_rng(29)
    for q in np.linspace(0, 1, 34):
        c = np.array([1.62, -5.12]) + q * np.array([-0.60, 0.40]) + np.array([0.06 * np.sin(q * 9), 0]) \
            + rng.normal(0, 0.035, 2)
        r0 = 0.003 + 0.006 * rng.random() ** 2
        b.ellipsoid((c[0], 0.0006, c[1]), (r0, 0.0012, r0 * rng.uniform(0.7, 1.0)), BLOOD, op=UNION)
        if rng.random() < 0.3:              # a satellite drop thrown off it
            a = rng.uniform(0, 2 * np.pi)
            b.ellipsoid((c[0] + 0.02 * np.cos(a), 0.0005, c[1] + 0.02 * np.sin(a)), (0.0018, 0.001, 0.0015),
                        BLOOD, op=UNION)
    b.group('floor_gore', margin=0.01)
    b.grid(*cached('floorpools', floor_pools, deps()), GORE, op=UNION)
    # the writing on the wall
    b.group('writing', margin=0.01)
    b.grid(*cached('wallblood', wall_blood, deps(), tuple(np.round(r_centre, 4)), tuple(np.round(contact, 4))),
           BLOOD, op=UNION)
    b.group('sheet_heap', margin=0.03)
    b.grid(*cached('sheetheap', sheet_heap, deps()), DIRTY_LINEN, op=UNION)

    def fixed(sb):
        import man
        from materials import new_params
        R.build_environment(sb, new_params())
        sb.group('heap', margin=0.01)
        sb.grid(*cached('sheetheap', sheet_heap, deps()), LINEN, op=UNION)
        if man_state is not None:
            man.build(sb, man_state)
    wreckage(b, fixed)
    dresser_top(b)
    wall_lights(b, t)


def on_rug(p):
    A = R.RUG_AREA
    return abs(p[0] - A['cx']) < A['hx'] and abs(p[2] - A['cz']) < A['hz']


def floor_y(p):
    return 0.012 if on_rug(p) else 0.0


def flat_limb(b, a, e, width, thick, mat, op=SUNION, k=0.04):
    """A sleeve or trouser leg lying flat on the floor: a flattened ellipsoid from a to e."""
    a, e = np.asarray(a, float), np.asarray(e, float)
    d = e - a
    yaw = np.degrees(np.arctan2(-d[2], d[0]))
    b.ellipsoid((a + e) / 2, (np.linalg.norm(d) / 2 + width * 0.5, thick, width), mat, op=op, k=k, R=rot(yaw))


def cloth_shape(rng, x, z, kind, yaw, s):
    """The flat outline of a thrown piece of clothing, as ellipses (cx, cz, rx, rz, yaw, thickness)."""
    Rg = rot(yaw)
    out = []

    def limb(a, e, w, t):
        d = e - a
        out.append(((a[0] + e[0]) / 2, (a[2] + e[2]) / 2, np.linalg.norm(d) / 2 + w / 2, w,
                    np.degrees(np.arctan2(-d[2], d[0])), t))
    c = np.array([x, 0, z])
    if kind == 'top':
        out.append((x, z, 0.24 * s, 0.30 * s, yaw, 0.035 * s))
        for sg in (-1, 1):
            a = c + Rg @ np.array([sg * 0.20 * s, 0, -0.18 * s])
            e = a + Rg @ np.array([sg * rng.uniform(0.15, 0.32) * s, 0, rng.uniform(-0.25, 0.2) * s])
            limb(a, e, 0.07 * s, 0.028 * s)
    elif kind == 'trousers':
        for sg in (-1, 1):
            a = c + Rg @ np.array([sg * 0.07 * s, 0, -0.20 * s])
            e = a + Rg @ np.array([sg * rng.uniform(0.02, 0.15) * s, 0, rng.uniform(0.55, 0.72) * s])
            limb(a, e, 0.09 * s, 0.03 * s)
        out.append((x, z - 0.0, 0.18 * s, 0.12 * s, yaw, 0.035 * s))
    elif kind == 'ball':
        out.append((x, z, 0.16 * s, 0.13 * s, yaw, 0.09 * s))
        p = c + Rg @ np.array([0.1 * s, 0, 0.08 * s])
        out.append((p[0], p[2], 0.11 * s, 0.09 * s, yaw + 40, 0.08 * s))
    elif kind == 'pillow':
        out.append((x, z, 0.36, 0.22, 25, 0.13))
    else:
        p = c.copy()
        ang = np.radians(yaw)
        for k in range(8):
            ang += rng.normal(0, 0.45)
            q = p + np.array([np.cos(ang), 0, np.sin(ang)]) * 0.10 * s
            limb(p, q, 0.055 * s, 0.018 * s)
            p = q
    return out


def garment(b, rng, c, kind, mat, yaw=None, size=1.0):
    """A piece of clothing thrown on the floor: 'top' (body and two sleeves flung out), 'trousers', 'ball'
    (balled up), 'long' (a scarf or a belt trailing)."""
    c = np.array(c, float)
    c[1] = floor_y(c)
    yaw = rng.uniform(0, 360) if yaw is None else yaw
    Rg = rot(yaw)
    s = size
    if kind == 'top':
        b.ellipsoid(c + [0, 0.025 * s, 0], (0.24 * s, 0.03 * s, 0.30 * s), mat, op=UNION, R=Rg @ rot(0, 0, rng.normal(0, 4)))
        for sg in (-1, 1):
            a = c + Rg @ np.array([sg * 0.20 * s, 0.02 * s, -0.18 * s])
            e = a + Rg @ np.array([sg * rng.uniform(0.15, 0.35) * s, 0, rng.uniform(-0.3, 0.25) * s])
            flat_limb(b, a, e, 0.065 * s, 0.018 * s, mat)
    elif kind == 'trousers':
        for sg in (-1, 1):
            a = c + Rg @ np.array([sg * 0.07 * s, 0.03 * s, -0.20 * s])
            e = a + Rg @ np.array([sg * rng.uniform(0.02, 0.18) * s, 0, rng.uniform(0.55, 0.75) * s])
            flat_limb(b, a, e, 0.08 * s, 0.022 * s, mat, op=UNION if sg < 0 else SUNION)
        b.ellipsoid(c + Rg @ np.array([0, 0.035 * s, -0.22 * s]), (0.18 * s, 0.035 * s, 0.10 * s), mat, op=SUNION, k=0.04, R=Rg)
    elif kind == 'ball':
        b.ellipsoid(c + [0, 0.07 * s, 0], (0.16 * s, 0.07 * s, 0.13 * s), mat, op=UNION, R=Rg)
        b.ellipsoid(c + Rg @ np.array([0.1 * s, 0.05 * s, 0.08 * s]), (0.10 * s, 0.05 * s, 0.09 * s), mat, op=SUNION, k=0.04, R=Rg)
    else:
        p = c + [0, 0.012, 0]
        ang = np.radians(yaw)
        for k in range(8):
            ang += rng.normal(0, 0.5)
            q = p + np.array([np.cos(ang), 0, np.sin(ang)]) * 0.10 * s
            flat_limb(b, p, q, 0.05 * s, 0.012 * s, mat, op=UNION if k == 0 else SUNION, k=0.015)
            p = q


def suitcase(b, rng, c, yaw, state, mat=SHELL):
    """A suitcase thrown about: 'burst' (on its back, lid torn half off), 'side' (on its side, gutted),
    'upturned' (face down, crushed), 'lid' (just a torn-off lid)."""
    c = np.array(c, float)
    Rs = rot(yaw)
    if state == 'burst':
        b.box(c + Rs @ [0, 0.11, 0], (0.36, 0.11, 0.24), mat, op=UNION, r=0.03, R=Rs)
        b.box(c + Rs @ [0, 0.14, 0], (0.335, 0.11, 0.215), mat, op=SUB, r=0.02, R=Rs)
        Rl = Rs @ rot(0, -168, rng.normal(0, 6))                      # the lid wrenched right back, flat
        lc = c + Rs @ np.array([0, 0.2, -0.24]) + Rl @ np.array([0, 0, 0.24])
        b.box(lc, (0.36, 0.03, 0.24), mat, op=UNION, r=0.02, R=Rl)
    elif state == 'side':
        Rside = Rs @ rot(0, 0, 90)
        b.box(c + [0, 0.24, 0], (0.36, 0.11, 0.24), mat, op=UNION, r=0.03, R=Rside)
        b.box(c + [0, 0.24, 0] + Rside @ np.array([0, 0.04, 0]), (0.335, 0.11, 0.215), mat, op=SUB, r=0.02, R=Rside)
        b.capsule(c + Rs @ np.array([-0.1, 0.49, 0]), c + Rs @ np.array([0.1, 0.49, 0]), 0.012, BLACKMETAL, op=UNION)
    elif state == 'upturned':
        b.box(c + [0, 0.10, 0], (0.34, 0.10, 0.23), mat, op=UNION, r=0.03, R=Rs @ rot(0, 4, -3))
        for sg in (-1, 1):
            b.cylinder(c + Rs @ np.array([sg * 0.28, 0.21, 0.18]), 0.02, 0.025, BLACKMETAL, op=UNION, R=rot(0, 90, 0))
    else:
        b.box(c + [0, 0.03, 0], (0.36, 0.03, 0.24), mat, op=UNION, r=0.02, R=Rs @ rot(0, 0, 3))
        b.box(c + [0, 0.05, 0], (0.335, 0.03, 0.215), mat, op=SUB, r=0.015, R=Rs @ rot(0, 0, 3))


@njit(cache=True)
def _occupied(P, G, GB, x0, z0, cell, i0, i1, k0, k1, heights, out):
    """Mark the floor cells (i, k) in the window whose column holds anything solid at these heights."""
    for i in range(i0, i1):
        for k in range(k0, k1):
            x, z = x0 + (i + 0.5) * cell, z0 + (k + 0.5) * cell
            for y in heights:
                d, m = S.scene_map(x, y, z, P, G, GB)
                if d < 0.0:
                    out[i, k] = True
                    break


@njit(cache=True)
def _heights(P, G, GB, x0, z0, cell, i0, i1, k0, k1, ys, out):
    """The top of whatever stands in each floor cell (ys from high to low); out keeps the highest."""
    for i in range(i0, i1):
        for k in range(k0, k1):
            x, z = x0 + (i + 0.5) * cell, z0 + (k + 0.5) * cell
            for y in ys:
                if y <= out[i, k]:
                    break
                d, m = S.scene_map(x, y, z, P, G, GB)
                if d < 0.0:
                    out[i, k] = y
                    break


class Floor:
    """What already stands on the floor, as a map of 2 cm cells, so that thrown things land beside each other
    and never inside each other (or inside the furniture, the walls or the man). Each thing is tried where it
    is meant to go and, if that is taken, nudged outwards until it fits."""
    X0, Z0, CELL = -2.45, -5.25, 0.02
    NX, NZ = 245, 270
    HEIGHTS = np.array([0.02, 0.05, 0.10, 0.18, 0.28, 0.40, 0.55])

    HC = 0.01            # the height map (what cloth lies on) is finer: 1 cm cells
    HN = (490, 540)

    def __init__(self, scratch_build):
        self.occ = np.zeros((self.NX, self.NZ), bool)
        self.placed = []
        self.occ |= self.mask(scratch_build)
        self.base = self.occ.copy()
        hx = self.X0 + (np.arange(self.HN[0]) + 0.5) * self.HC
        hz = self.Z0 + (np.arange(self.HN[1]) + 0.5) * self.HC
        A = R.RUG_AREA
        self.H = np.where((np.abs(hx[:, None] - A['cx']) < A['hx']) & (np.abs(hz[None, :] - A['cz']) < A['hz']),
                          0.012, 0.0).astype(np.float64)

    def raise_heights(self, make):
        """Add a new thing's top to the height map."""
        sb = S.Builder()
        sb.group('probe', margin=0.0)
        make(sb)
        sb.groups = [g for g in sb.groups if g['bounds']]
        P, G = sb.build()
        GB = sb.grid_buffer()
        lo = (G[:, 0:3] - G[:, 3:4]).min(0)
        hi = (G[:, 0:3] + G[:, 3:4]).max(0)
        i0, i1 = max(int((lo[0] - self.X0) / self.HC), 0), min(int((hi[0] - self.X0) / self.HC) + 1, self.HN[0])
        k0, k1 = max(int((lo[2] - self.Z0) / self.HC), 0), min(int((hi[2] - self.Z0) / self.HC) + 1, self.HN[1])
        ys = np.arange(min(hi[1], 0.8), 0.0, -0.004)
        if i1 > i0 and k1 > k0:
            _heights(P, G, GB, self.X0, self.Z0, self.HC, i0, i1, k0, k1, ys, self.H)

    def height_at(self, X, Z):
        """The height map sampled (bilinear) at world points."""
        q = np.stack([(np.asarray(X) - self.X0) / self.HC - 0.5, (np.asarray(Z) - self.Z0) / self.HC - 0.5])
        return ndimage.map_coordinates(self.H, q.reshape(2, -1), order=1, mode='nearest').reshape(q.shape[1:])

    def drape(self, b, name, mat, shapes, x, z, reach=0.9, seed=0):
        """Throw a piece of cloth down near (x, z): shapes(x, z) gives its flat outline as ellipses
        (cx, cz, rx, rz, yaw, thickness). It settles over whatever is already there - floor, cases, other
        clothes - resting on the tops, slumping over edges, never passing through them."""
        tries = [(0.0, 0.0)] + [(r * np.cos(a), r * np.sin(a)) for r in np.arange(0.05, reach, 0.05)
                                for a in np.linspace(0, 2 * np.pi, int(8 + r * 40), endpoint=False)]
        vox = 0.006
        base_grown = ndimage.binary_dilation(self.base, iterations=1)
        for dx, dz in tries:
            ells = shapes(x + dx, z + dz)
            ext = max(max(e[2], e[3]) for e in ells) + 0.03
            lo2 = np.array([min(e[0] for e in ells) - ext, min(e[1] for e in ells) - ext])
            hi2 = np.array([max(e[0] for e in ells) + ext, max(e[1] for e in ells) + ext])
            nx, nz = ((hi2 - lo2) / vox).astype(int) + 1
            X = lo2[0] + np.arange(nx) * vox
            Z = lo2[1] + np.arange(nz) * vox
            XX, ZZ = np.meshgrid(X, Z, indexing='ij')
            th = np.zeros(XX.shape)
            for cx, cz, rx, rz, yaw, t in ells:
                c, s_ = np.cos(np.radians(yaw)), np.sin(np.radians(yaw))
                u = ((XX - cx) * c - (ZZ - cz) * s_) / rx
                v = ((XX - cx) * s_ + (ZZ - cz) * c) / rz
                th = np.maximum(th, t * np.sqrt(np.clip(1 - u * u - v * v, 0, 1)))
            th *= 1 + 0.15 * noise2(XX, ZZ, 0.08, seed)            # rucked and creased
            mask = th > 0.003
            # (on the coarse map: off the furniture, walls and the man)
            ci = ((XX[mask] - self.X0) / self.CELL).astype(int)
            ck = ((ZZ[mask] - self.Z0) / self.CELL).astype(int)
            if (ci < 0).any() or (ck < 0).any() or (ci >= self.NX).any() or (ck >= self.NZ).any():
                continue
            if base_grown[ci, ck].any():
                continue
            Hn = self.height_at(XX, ZZ)
            if Hn[mask].max() > 0.32:
                continue
            # cloth bridges small gaps and slumps over edges: never below what is under it
            # (spanning openings and thin walls like fabric: the highest point within 5 cm, softened)
            span = ndimage.gaussian_filter(ndimage.maximum_filter(Hn, size=17), 4.0)
            Bm = np.maximum(Hn, np.minimum(span, Hn + 0.05)) + 0.002
            T = Bm + th
            y0, y1 = Bm[mask].min() - 0.012, T[mask].max() + 0.012
            Y = y0 + np.arange(int((y1 - y0) / vox) + 1) * vox
            d2 = sdf2(mask, vox)
            d = np.maximum(np.maximum(Bm[:, None, :] - Y[None, :, None], Y[None, :, None] - T[:, None, :]),
                           d2[:, None, :])
            d = robust_distance(d.astype(np.float32), vox)
            b.grid(np.array([X[0], Y[0], Z[0]]), d, vox, mat, op=UNION)
            # what it now covers, for everything thrown after it
            hi_ = np.zeros(self.H.shape)
            ii = ((XX[mask] - self.X0) / self.HC).astype(int)
            kk = ((ZZ[mask] - self.Z0) / self.HC).astype(int)
            ok = (ii >= 0) & (kk >= 0) & (ii < self.HN[0]) & (kk < self.HN[1])
            np.maximum.at(self.H, (ii[ok], kk[ok]), T[mask][ok])
            m = np.zeros(self.occ.shape, bool)
            m[ci, ck] = True
            self.occ |= m
            self.placed.append((name + ' (cloth)', m))
            return x + dx, z + dz
        print(f'  (no room on the floor for {name} near {x:.2f}, {z:.2f}: left out)', flush=True)
        return None

    def mask(self, make):
        sb = S.Builder()
        sb.group('probe', margin=0.0)
        make(sb)
        sb.groups = [g for g in sb.groups if g['bounds']]
        P, G = sb.build()
        GB = sb.grid_buffer()
        out = np.zeros((self.NX, self.NZ), bool)
        lo = (G[:, 0:3] - G[:, 3:4]).min(0)
        hi = (G[:, 0:3] + G[:, 3:4]).max(0)
        i0, i1 = max(int((lo[0] - self.X0) / self.CELL), 0), min(int((hi[0] - self.X0) / self.CELL) + 1, self.NX)
        k0, k1 = max(int((lo[2] - self.Z0) / self.CELL), 0), min(int((hi[2] - self.Z0) / self.CELL) + 1, self.NZ)
        if i1 > i0 and k1 > k0:
            _occupied(P, G, GB, self.X0, self.Z0, self.CELL, i0, i1, k0, k1, self.HEIGHTS, out)
        return out

    def place(self, b, name, make, x, z, reach=0.9):
        """Put make(builder, x, z) down at (x, z), or as near as it fits. Returns where, or None."""
        grown = ndimage.binary_dilation(self.occ, iterations=1)       # and not touching, either
        tries = [(0.0, 0.0)] + [(r * np.cos(a), r * np.sin(a)) for r in np.arange(0.05, reach, 0.05)
                                for a in np.linspace(0, 2 * np.pi, int(8 + r * 40), endpoint=False)]
        for dx, dz in tries:
            m = self.mask(lambda sb: make(sb, x + dx, z + dz))
            if m.any() and not (m & grown).any():
                self.occ |= m
                self.placed.append((name, m))
                make(b, x + dx, z + dz)
                self.raise_heights(lambda sb: make(sb, x + dx, z + dz))
                return x + dx, z + dz
        print(f'  (no room on the floor for {name} near {x:.2f}, {z:.2f}: left out)', flush=True)
        return None

    def free(self, x, z, r=0.0):
        i, k = int((x - self.X0) / self.CELL), int((z - self.Z0) / self.CELL)
        n = int(np.ceil(r / self.CELL))
        return not self.occ[max(i - n, 0):i + n + 1, max(k - n, 0):k + n + 1].any()


PLACED = []          # (name, footprint) of everything laid on the floor in the last build, for checks.py


def wreckage(b, fixed):
    """fixed(builder): adds everything that was already standing on the floor (the room, the man)."""
    fl = Floor(fixed)
    # --- the luggage of someone coming home for Christmas: five cases thrown about and burst open
    b.group('suitcases', margin=0.03)
    for name, (x, z), yaw, state, mat, seed in (
            ('burst case', (0.20, -2.95), -18, 'burst', SHELL, 1), ('leather case', (1.55, -2.95), 64, 'side', LEATHER, 2),
            ('fabric case', (-0.05, -4.00), 25, 'upturned', CLOTH_MID, 3), ('torn lid', (1.60, -4.45), -40, 'lid', SHELL, 4),
            ('flung case', (0.95, -1.95), 8, 'upturned', SHELL, 5)):
        fl.place(b, name, lambda sb, x, z, yaw=yaw, state=state, mat=mat, seed=seed:
                 suitcase(sb, np.random.default_rng(seed), (x, 0.0, z), yaw, state, mat=mat), x, z)
    # the chest's drawers torn out and thrown down, one upside down
    b.group('drawers', margin=0.03)
    for (x, z), yaw, roll in (((1.20, -1.75), 35, 0), ((1.45, -3.40), 70, 180)):
        def drawer(sb, x, z, yaw=yaw, roll=roll):
            Rd = rot(yaw, 0, roll)
            c = np.array([x, 0.10, z])
            sb.box(c, (0.24, 0.09, 0.45), DARKWOOD, op=UNION, r=0.006, R=Rd)
            sb.box(c + Rd @ [0, 0.02, 0], (0.22, 0.09, 0.43), DARKWOOD, op=SUB, R=Rd)
        fl.place(b, 'drawer', drawer, x, z)
    # a leather holdall, a pillow flung on the floor, the smashed desk lamp
    b.group('holdall', margin=0.03)

    def holdall(sb, x, z):
        hc = np.array([x, 0.17, z])
        sb.capsule(hc + [-0.25, 0, 0.08], hc + [0.25, 0, -0.08], 0.16, LEATHER, op=UNION)
        sb.torus(hc + [0, 0.12, 0.02], 0.10, 0.012, LEATHER, op=UNION, R=rot(-17, 0, 0) @ rot(0, 90, 0))
    fl.place(b, 'holdall', holdall, 1.35, -4.10)
    b.group('lamp', margin=0.02)

    def lamp(sb, x, z):
        lc = np.array([x, 0.0, z])
        sb.cylinder(lc + [0, 0.012, 0], 0.012, 0.08, BRASS, op=UNION)
        sb.capsule(lc + [0, 0.02, 0], lc + [-0.32, 0.035, 0.12], 0.012, BRASS, op=UNION)
        sb.cone(lc + [-0.32, 0.12, 0.12], lc + [-0.50, 0.12, 0.20], 0.12, 0.08, LINEN, op=UNION)
        sb.cone(lc + [-0.32, 0.12, 0.12], lc + [-0.50, 0.12, 0.20], 0.11, 0.07, LINEN, op=SUB)
    fl.place(b, 'lamp', lamp, 2.05, -4.55)
    # small presents of every shape, some with bows
    b.group('small_presents', margin=0.02)
    gifts = [((1.20, -2.75), 'box', (0.09, 0.06, 0.07), 30, GIFT_RED, True),
             ((0.55, -3.45), 'cube', (0.075, 0.075, 0.075), -15, GIFTWRAP, True),
             ((1.95, -3.10), 'flat', (0.16, 0.025, 0.11), 55, GIFT_RED, False),
             ((-0.15, -2.60), 'tube', (0.035, 0.16), 70, GIFTWRAP, False),
             ((0.25, -1.95), 'big', (0.17, 0.12, 0.13), 12, GIFT_RED, True),
             ((1.55, -2.25), 'tall', (0.05, 0.14, 0.05), 5, GIFTWRAP, True),
             ((0.95, -3.35), 'tube', (0.05, 0.11), -35, GIFT_RED, True),
             ((0.02, -3.65), 'box', (0.11, 0.045, 0.06), 80, GIFT_RED, False, 'crushed')]
    for g in gifts:
        fl.place(b, 'present', lambda sb, x, z, g=g: small_present(sb, (x, z), *g[1:6], crushed=len(g) > 6), *g[0])
    # everything that was in the cases, flung across the room, landing on top of each other and over the
    # cases: ordinary clothes, and Christmas ones
    kinds = [((0.55, -2.15), 'top', CLOTH_LIGHT), ((0.05, -2.9), 'trousers', DENIM), ((1.15, -2.55), 'ball', CLOTH_MID),
             ((0.70, -3.20), 'top', XMAS_JUMPER), ((1.85, -2.35), 'ball', CLOTH_LIGHT), ((-0.15, -3.45), 'top', COAT),
             ((1.25, -3.55), 'trousers', CLOTH_MID), ((0.35, -3.70), 'long', XMAS_GREEN_KNIT), ((1.10, -1.85), 'top', DENIM),
             ((1.95, -3.95), 'ball', XMAS_JUMPER), ((0.30, -4.30), 'ball', CLOTH_LIGHT), ((0.60, -2.65), 'long', CLOTH_MID),
             ((-0.20, -2.25), 'ball', COAT), ((1.45, -2.10), 'long', LEATHER), ((0.95, -3.95), 'top', CLOTH_LIGHT),
             ((1.75, -3.45), 'top', CLOTH_MID), ((0.15, -3.10), 'ball', XMAS_JUMPER), ((0.85, -2.95), 'trousers', COAT),
             ((0.30, -2.95), 'top', DIRTY_LINEN), ((-0.10, -3.20), 'pillow', DIRTY_LINEN)]
    for n, ((x, z), kind, mat) in enumerate(kinds):
        rs = np.random.default_rng(100 + n)
        size, yaw = rs.uniform(0.8, 1.0), rs.uniform(0, 360)
        b.group('cloth_%d' % n, margin=0.02)
        fl.drape(b, kind, mat, lambda x, z, kind=kind, n=n, size=size, yaw=yaw:
                 cloth_shape(np.random.default_rng(200 + n), x, z, kind, yaw, size), x, z, reach=1.0, seed=300 + n)
    # a Santa hat, knocked across the floor

    def santa_hat(sb, x, z):
        hc = np.array([x, floor_y((x, 0, z)), z])
        sb.cone(hc + [0, 0.02, 0], hc + [0.18, 0.06, 0.08], 0.09, 0.015, FELT, op=UNION)
        sb.torus(hc + [0, 0.03, 0], 0.085, 0.025, FUR, op=UNION, R=rot(0, 0, 70) @ rot(90, 0, 0))
        sb.sphere(hc + [0.20, 0.04, 0.10], 0.028, FUR, op=UNION)
    fl.place(b, 'Santa hat', santa_hat, 1.30, -2.30)
    # toiletries spilled out of a wash bag
    b.group('toiletries', margin=0.02)
    rng = np.random.default_rng(7)
    for k in range(10):
        x, z = 0.4 + rng.normal(0, 0.3), -2.75 + rng.normal(0, 0.25)
        L, r, a = rng.uniform(0.06, 0.16), rng.uniform(0.012, 0.03), rng.uniform(0, 2 * np.pi)

        def bottle(sb, x, z, L=L, r=r, a=a, k=k):
            c = np.array([x, floor_y((x, 0, z)) + r, z])
            d = np.array([np.cos(a), 0, np.sin(a)]) * L / 2
            sb.capsule(c - d, c + d, r, (PLASTIC, CLOTH_MID, SHELL)[k % 3], op=UNION)
        fl.place(b, 'toiletry', bottle, x, z, reach=0.3)
    # --- shredded sheets: torn strips trailing across the floor, stopping where they meet something
    b.group('shreds', margin=0.02)
    for k in range(12):
        p = np.array([rng.uniform(-0.3, 1.7), 0.0, rng.uniform(-3.6, -1.8)])
        yaw = rng.uniform(0, 360)
        wdt = rng.uniform(0.05, 0.12)
        for s in range(int(rng.integers(4, 9))):
            yaw += rng.normal(0, 25)
            L = rng.uniform(0.07, 0.13)
            dirv = np.array([np.cos(np.radians(yaw)), 0, np.sin(np.radians(yaw))])
            c = p + dirv * L / 2
            if not fl.free(c[0], c[2], L / 2 + 0.02):
                break
            c[1] = floor_y(c) + 0.004 + 0.006 * rng.random()
            b.box(c, (L / 2 + 0.01, 0.0025, wdt / 2), DIRTY_LINEN, op=UNION, r=0.002, R=rot(-yaw, rng.normal(0, 3), rng.normal(0, 3)))
            p = p + dirv * L
    # --- broken glass: shards everywhere there is bare floor, thickest under the smashed mirror
    b.group('glass', margin=0.02)
    for k in range(260):
        if k < 110:
            c = np.array([R.HALF_W - 0.45 - 1.3 * rng.random() ** 1.5, 0.0, R.DRESSER_Z + rng.normal(0, 0.5)])
        else:
            c = np.array([rng.uniform(-0.3, 2.0), 0.0, rng.uniform(-4.2, -1.5)])
        s = 0.01 + 0.05 * rng.random() ** 2.0
        yaw = rng.uniform(0, 360)
        if not fl.free(c[0], c[2], s + 0.02):
            continue
        c[1] = 0.0025 + floor_y(c)
        Rr = rot(yaw, rng.normal(0, 3), rng.normal(0, 3))
        b.box(c, (s, 0.0015, s * rng.uniform(0.4, 1.0)), GLASS, op=UNION, R=Rr)
        b.halfspace(c, Rr @ rot(0, 0, 90) @ rot(rng.uniform(-50, 50), 0, 0), GLASS, op=SUB)
    PLACED[:] = fl.placed
    return fl


def small_present(b, xz, kind, size, yaw, mat, has_bow, crushed=False):
    x, z = xz
    c = np.array([x, floor_y((x, 0, z)), z])
    if kind == 'tube':                       # a tube lying on its side: a bottle, a poster
        r, h = size
        d = np.array([np.cos(np.radians(yaw)), 0, -np.sin(np.radians(yaw))]) * h
        c[1] += r
        b.capsule(c - d, c + d, r, mat, op=UNION)
        for t in (-0.55, 0.55):              # ribbon tied round it
            b.torus(c + d * t, r + 0.001, 0.004, RIBBON, op=UNION, R=S.frame_from_axis(c - d, c + d))
        top = c + [0, r, 0]
    else:
        half = np.array(size)
        Rg = rot(yaw, 0, 0) @ (rot(0, 8, -14) if crushed else np.eye(3))
        h2 = half * (np.array([1, 0.7, 1]) if crushed else 1)
        c[1] += h2[1] + (0.015 if crushed else 0.0)
        b.box(c, h2, mat, op=UNION, r=0.004, R=Rg)
        b.box(c, (h2[0] + 0.002, h2[1] + 0.002, 0.009), RIBBON, op=UNION, R=Rg)
        b.box(c, (0.009, h2[1] + 0.002, h2[2] + 0.002), RIBBON, op=UNION, R=Rg)
        top = c + Rg @ np.array([0, h2[1], 0])
    if has_bow:
        bow(b, top, 0.6 + 2.2 * min(size[0], 0.12), yaw + 30, RIBBON)


def draped_jumper(vox=0.003):
    """A jumper dragged half off the chest of drawers: lying crumpled on the top, the rest falling down the
    front in soft folds to a ragged hem, one sleeve hanging lower."""
    x1 = R.HALF_W - 0.26 - 0.27                 # the front edge of the top (the chest faces -x)
    top, z0 = 0.903, R.DRESSER_Z - 0.03
    lo, hi = np.array([x1 - 0.06, top - 0.50, z0 - 0.26]), np.array([x1 + 0.28, top + 0.07, z0 + 0.26])
    P, n = grid_points(lo, hi, vox)
    x, y, z = P[..., 0], P[..., 1], P[..., 2]
    chest = sd_box(P, (x1 + 0.27, top - 0.45, z0), (0.27, 0.45, 0.6), 0.012)
    fold = 0.010 * np.sin(z * 55 + 3 * noise3(P, 0.08, 61)) * (y < top - 0.02) + 0.012 * noise3(P, 0.05, 62) * (y > top - 0.02)
    bulk = 0.010 + 0.012 * (y > top - 0.01) * np.clip(1 - (x - x1) / 0.25, 0, 1)
    d = np.abs(chest - bulk - fold) - 0.006
    width = 0.20 + 0.03 * noise3(P, 0.06, 63)
    hem = top - 0.26 + 0.04 * noise3(P * np.array([0, 0, 1]), 0.05, 64)
    sleeve = np.hypot(z - (z0 + 0.14), 0) - 0.045
    region = np.maximum(np.abs(z - z0) - width, np.maximum(hem - y, x - (x1 + 0.25)))
    region = np.minimum(region, np.maximum(sleeve, np.maximum(top - 0.44 - y, x - (x1 + 0.04))))
    d = smax(d, region, 0.01)
    return lo, robust_distance(d.astype(np.float32), vox), vox


def sheet_heap(vox=0.008):
    """The top sheet, dragged off the foot of the bed: a crumpled heap on the boards, one end still over the
    mattress edge."""
    lo, hi = np.array([-1.7, 0.0, R.BED['z1'] - 0.15]), np.array([-0.05, 0.72, R.BED['z1'] + 0.75])
    P, n = grid_points(lo, hi, vox)
    z1 = R.BED['z1']
    d = sd_ellipsoid(P, (-0.9, 0.06, z1 + 0.22), (0.45, 0.065, 0.22))
    d = smin(d, sd_ellipsoid(P, (-0.55, 0.04, z1 + 0.40), (0.28, 0.04, 0.14)), 0.08)
    d = smin(d, sd_ellipsoid(P, (-1.3, 0.06, z1 + 0.15), (0.22, 0.06, 0.18)), 0.06)
    d = d + 0.018 * noise3(P, 0.07, 51) + 0.007 * noise3(P, 0.025, 52)
    d = smax(d, -P[..., 1], 0.01)
    return lo, robust_distance(d.astype(np.float32), vox), vox


def ribbon_strip(b, pts, ups, width, mat, thick=0.0012):
    """A flat satin ribbon along a path: at each point its width runs along `ups` (a direction across the
    ribbon), laid as short thin boxes. width may be a number or one per point."""
    pts = np.asarray(pts, float)
    wid = np.broadcast_to(np.asarray(width, float), (len(pts),))
    for i in range(len(pts) - 1):
        p, q = pts[i], pts[i + 1]
        t = q - p
        L = np.linalg.norm(t)
        if L < 1e-6:
            continue
        t /= L
        w = np.asarray(ups[i], float)
        w = w - t * (w @ t)
        w /= np.linalg.norm(w)
        n = np.cross(t, w)
        b.box((p + q) / 2, (L / 2 + 0.0008, thick, (wid[i] + wid[i + 1]) / 4), mat, op=UNION, r=0.0006,
              R=np.column_stack([t, n, w]))


def satin_bow(b, top, yaw, mat, size=1.0):
    """A shop-bought satin bow, as on any present (about 15 cm across): two big loops standing out to the
    sides, two smaller ones in front, each a flat ribbon curving round and pinched in at a wrapped knot, and
    two short tails lying on the paper. top: where it sits; yaw: which way its loops spread."""
    Rb = rot(yaw)
    up = np.array([0, 1.0, 0])
    width = 0.028 * size
    # (direction round the knot in degrees, how steeply it rises, length, how open the loop is, a lean)
    for az, el, L, H, lean in ((8, 30, 0.080, 0.032, 10), (172, 32, 0.076, 0.031, -12),
                               (-38, 50, 0.060, 0.026, 6), (-142, 48, 0.058, 0.026, -8)):
        a = Rb @ np.array([np.cos(np.radians(az)) * np.cos(np.radians(el)), np.sin(np.radians(el)),
                           np.sin(np.radians(az)) * np.cos(np.radians(el))])
        n = up - a * (up @ a)
        n /= np.linalg.norm(n)
        side = np.cross(a, n)
        n = n * np.cos(np.radians(lean)) + side * np.sin(np.radians(lean))
        side = np.cross(a, n)
        s = np.linspace(0, 2 * np.pi, 44)
        # a loop: out along a and back, opening to H across; fullest at its far end, pinched at the knot
        pts = [top + [0, 0.010 * size, 0] + size * (L / 2 * (1 - np.cos(u)) * a + H * np.sin(u) * n
                                                   * (0.6 + 0.4 * np.sin(u / 2))) for u in s]
        wid = width * (0.45 + 0.55 * np.sin(s / 2) ** 0.7)
        # the ribbon twists a little as it comes round, so each loop catches the light differently
        ups = [side * np.cos(0.25 * np.sin(u)) + n * np.sin(0.25 * np.sin(u)) for u in s]
        ribbon_strip(b, pts, ups, wid, mat)
    # the knot: a short length of ribbon wrapped round the middle
    b.box(top + [0, 0.013 * size, 0], (0.015 * size, 0.012 * size, 0.014 * size), mat, op=UNION,
          r=0.008 * size, R=Rb)
    # two tails from under the knot, lying on the paper, their ends cut in a V
    for sg, ang in ((1, 118), (-1, -60)):
        d = Rb @ np.array([np.cos(np.radians(ang)), 0, np.sin(np.radians(ang))])
        pts = [top + d * r_ + [0, 0.004 - 0.02 * r_ * r_, 0] for r_ in np.linspace(0.005, 0.085 * size, 12)]
        ribbon_strip(b, pts, [np.cross(d, up)] * 12, width * 0.9, mat)


def bow(b, top, size, yaw, mat, squash=0.0):
    """A ribbon bow sitting on a present: two loops, a knot and two tails. size 1 = loops 4 cm across."""
    Rb = rot(yaw)
    k = size
    for sg in (-1, 1):
        lc = top + Rb @ np.array([sg * 0.030 * k, 0.018 * k * (1 - squash), 0])
        b.torus(lc, 0.024 * k, 0.0065 * k, mat, op=UNION, R=Rb @ rot(0, 0, -sg * (55 + 20 * squash)) @ rot(0, 90, 0))
        tail = top + Rb @ np.array([sg * 0.02 * k, 0.002, 0.05 * k])
        b.box((top + tail) / 2 + [0, 0.002, 0], (0.009 * k, 0.0015, 0.03 * k), mat, op=UNION,
              R=Rb @ rot(sg * 25, 0, 0))
    b.sphere(top + [0, 0.012 * k, 0], 0.012 * k, mat, op=UNION)


def dresser_top(b):
    """On the chest of drawers: a mess - things knocked flat, a jumper dragged half over the edge, glass from
    the mirror - and a few ordinary things that somehow survived, still standing: a framed photo, a snow globe,
    a perfume bottle, a closed laptop with a phone on it."""
    rng = np.random.default_rng(17)
    top = 0.903
    x0, z0 = R.HALF_W - 0.27, R.DRESSER_Z
    b.group('dresser_things', margin=0.02)
    # survivors
    fp = np.array([x0 + 0.12, top, z0 - 0.38])                                  # a framed photo, standing
    Rf = rot(-90 + 25) @ rot(0, -12, 0)
    b.box(fp + Rf @ [0, 0.11, 0], (0.08, 0.11, 0.012), BRASS, op=UNION, r=0.004, R=Rf)
    b.box(fp + Rf @ [0, 0.11, 0.012], (0.06, 0.09, 0.003), PAPER, op=UNION, R=Rf)
    sg = np.array([x0 - 0.02, top, z0 - 0.12])                                  # a snow globe
    b.cylinder(sg + [0, 0.02, 0], 0.02, 0.05, DARKWOOD, op=UNION, rr=0.005)
    b.sphere(sg + [0, 0.085, 0], 0.052, GLASS, op=UNION)
    pb = np.array([x0 - 0.10, top, z0 + 0.12])                                  # a perfume bottle
    b.box(pb + [0, 0.045, 0], (0.028, 0.045, 0.018), GLASS, op=UNION, r=0.006)
    b.cylinder(pb + [0, 0.10, 0], 0.012, 0.012, BRASS, op=UNION)
    lp = np.array([x0 + 0.04, top, z0 + 0.34])                                  # a closed laptop, askew, a phone on it
    b.box(lp + [0, 0.009, 0], (0.16, 0.009, 0.22), SHELL, op=UNION, r=0.004, R=rot(14))
    b.box(lp + [0.02, 0.022, -0.03], (0.038, 0.004, 0.075), SCREEN, op=UNION, r=0.004, R=rot(-8))
    # knocked flat: a deodorant can, a hairbrush, a toppled bottle, a lipstick, a watch
    for c, L, r, m in (((x0 - 0.05, z0 - 0.30), 0.14, 0.024, PLASTIC), ((x0 + 0.05, z0 + 0.05), 0.20, 0.018, DARKWOOD),
                       ((x0 - 0.12, z0 - 0.02), 0.16, 0.03, GLASS), ((x0 + 0.10, z0 - 0.08), 0.06, 0.009, BRASS)):
        a = rng.uniform(0, np.pi)
        d = np.array([np.cos(a), 0, np.sin(a)]) * L / 2
        p = np.array([c[0], top + r, c[1]])
        b.capsule(p - d, p + d, r, m, op=UNION)
    # a jumper dragged half off, hanging down the front
    b.group('dresser_jumper', margin=0.02)
    b.grid(*cached('draped', draped_jumper, deps()), CLOTH_LIGHT, op=UNION)
    # glass from the mirror
    for k in range(10):
        c = np.array([x0 + rng.normal(0, 0.08), top + 0.0015, z0 + rng.normal(0, 0.3)])
        s = 0.01 + 0.03 * rng.random()
        b.box(c, (s, 0.0015, s * 0.6), GLASS, op=UNION, R=rot(rng.uniform(0, 360), 0, 0))


LIT = (LIGHT_RED, LIGHT_GREEN, LIGHT_BLUE, LIGHT_YELLOW, LIGHT_ORANGE)
DEAD = (DEAD_RED, DEAD_GREEN, DEAD_BLUE, DEAD_YELLOW, DEAD_ORANGE)


def bulb_lit(i, t):
    """Whether bulb i is lit at time t: a few dead for good; the rest flash in a broken, stuttering way, in
    runs along the string (a bad contact), each run on its own irregular beat."""
    h = lambda *a: (np.sin(np.dot(a, (12.9898, 78.233, 37.719)[:len(a)])) * 43758.5453) % 1.0
    if h(i, 1.0) < 0.14:
        return False
    run = i // 7
    beat = int(np.floor(t * (6 + 5 * h(run, 2.0))))
    return h(run, beat, 3.0) > 0.35 and h(i, beat, 4.0) > 0.12


def bulb_spots(pts, first=0, spacing=0.11):
    """Where the bulbs hang along a string: (index, point on the wire)."""
    pts = np.array(pts)
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s_all = np.concatenate([[0], np.cumsum(seg)])
    return [(i, np.array([np.interp(s, s_all, pts[:, k]) for k in range(3)]))
            for i, s in enumerate(np.arange(0.05, s_all[-1], spacing), start=first)]


def light_string(b, pts, t, first=0, spacing=0.11):
    """A string of coloured bulbs hanging from a wire along the points; returns how many bulbs."""
    pts = np.array(pts)
    for p, q in zip(pts[:-1], pts[1:]):
        b.capsule(p, q, 0.0025, BLACKMETAL, op=UNION)
    spots = bulb_spots(pts, first, spacing)
    for i, p in spots:
        col = (i * 3 + int(i * 0.37)) % 5
        b.cylinder(p + [0, -0.008, 0], 0.006, 0.005, BLACKMETAL, op=UNION)
        b.ellipsoid(p + [0, -0.026, 0], (0.0075, 0.014, 0.0075), (LIT if bulb_lit(i, t) else DEAD)[col], op=UNION)
    return len(spots)


def swags(a, b_, hooks, sag=0.12, per=12):
    """Points of a string hung in swags between hooks (fractions 0..1 of the way from a to b_)."""
    a, b_ = np.asarray(a, float), np.asarray(b_, float)
    pts = []
    for h0, h1 in zip(hooks[:-1], hooks[1:]):
        for s in np.linspace(0, 1, per, endpoint=False):
            f = h0 + (h1 - h0) * s
            pts.append(a + (b_ - a) * f - np.array([0, sag * 4 * s * (1 - s), 0]))
    pts.append(a + (b_ - a) * hooks[-1])
    return pts


def strings():
    """The two strings of lights: along the top of the back wall (the left end torn from its hook and
    hanging down), with their hooks; and along the top of the right-hand wall, with its hooks."""
    z = R.BACK_Z + 0.035
    y = R.EAVES - 0.16
    hooks = np.linspace(-2.25, 2.25, 8)
    pts = []
    a = np.array([hooks[1], y, z])                    # the torn end hangs from the second hook
    for s in np.linspace(1, 0, 14):
        pts.append(a + np.array([-0.35 * (1 - s) ** 1.5, -0.95 * (1 - s), 0.02 * (1 - s)]))
    pts = pts[::-1] + swags((-2.25, y, z), (2.25, y, z), (hooks[1:] + 2.25) / 4.5)[1:]
    back_hooks = [(h, y + 0.005, z - 0.01) for h in hooks[1:]]
    x = R.HALF_W - 0.035
    za, zb = R.BACK_Z + 0.12, -0.35
    hk = np.linspace(0, 1, 8)
    side_hooks = [(x - 0.01, y + 0.005, za + (zb - za) * f) for f in hk]
    return (pts, back_hooks), (swags((x, y, za), (x, y, zb), hk), side_hooks)


def wall_lights(b, t=0.0):
    """Coloured fairy lights strung in swags along the top of the back wall, under the cornice, and the same
    along the top of the right-hand wall, from the back corner towards the door."""
    (back, back_hooks), (side, side_hooks) = strings()
    b.group('wall_lights', margin=0.02)
    for h in back_hooks:
        b.sphere(h, 0.008, BLACKMETAL, op=UNION)
    n = light_string(b, back, t)
    b.group('side_lights', margin=0.02)
    for h in side_hooks:
        b.sphere(h, 0.008, BLACKMETAL, op=UNION)
    light_string(b, side, t, first=n)


def glow(t, back_x=(-1.4, -0.2, 1.0, 2.2, -2.0), side_z=None):
    """How strongly the lights' glow on the walls shines at time t (1 = as in the still, when about half the
    bulbs are lit): for each of the glow lights along the back wall (at x = back_x) the share of the bulbs
    near it that are lit now; then the same for the right-hand wall's (at z = side_z)."""
    (back, _), (side, _) = strings()
    b_spots = bulb_spots(back)
    s_spots = bulb_spots(side, first=len(b_spots))
    avg = 0.5

    def share(spots, where, axis):
        w = np.array([np.exp(-((p[axis] - where) / 0.6) ** 2) for _, p in spots])
        lit = np.array([bulb_lit(i, t) for i, _ in spots], float)
        return float((w * lit).sum() / (w.sum() + 1e-9)) / avg
    out = [share(b_spots, x, 0) for x in back_x]
    if side_z is not None:
        out += [share(s_spots, z, 2) for z in side_z]
    return out
