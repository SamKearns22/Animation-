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
                       PLASTIC, SCREEN, XMAS_GREEN_KNIT, GOLD, WOOD, LIGHT_RED, LIGHT_GREEN, LIGHT_BLUE, LIGHT_YELLOW,
                       LIGHT_ORANGE, DEAD_RED, DEAD_GREEN, DEAD_BLUE, DEAD_YELLOW, DEAD_ORANGE)
from rig import smin, smax, robust_distance
from sdf3d import rot, UNION, SUNION, SUB

PRESENT_O = np.array([-2.07, 0.672, -2.87])      # its head end, on the sheet; it runs along +x
PRESENT_LEN = 1.62


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
    # the ribbon: two crooked bands round it (one slipped) and a strip of tape at the foot
    band = np.full(u.shape, 1.0, np.float32)
    for c, nrm, half in (((0.44, 0, 0), (1.0, 0.05, 0.28), 0.020), ((1.13, 0, 0), (1.0, -0.12, -0.34), 0.020)):
        nn = np.asarray(nrm) / np.linalg.norm(nrm)
        band = np.minimum(band, np.abs((Q - c) @ nn) - half)
    ribbon = smax(paper - 0.0025, band, 0.002)
    # the stains: soaked up from below (higher on the side that lies in it), in blotches over the head, the
    # hips and the knee, running down the side
    soak = (0.05 + 0.035 * noise3(Q, 0.07, 4) + 0.03 * np.clip(w / 0.2, 0, 1)) - v
    blot = -1.0
    for c, r in (((0.14, 0.12, 0.08), 0.13), ((0.90, 0.10, 0.10), 0.17), ((1.25, 0.26, -0.05), 0.10),
                 ((0.55, 0.30, 0.12), 0.07), ((0.40, 0.10, 0.20), 0.10)):
        blot = np.maximum(blot, r * (1 + 0.45 * noise3(Q, 0.04, 5)) - np.linalg.norm(Q - c, axis=-1))
    runs = (0.012 - np.abs(((u * 7.3 + 0.3 * noise3(Q, 0.1, 6)) % 1.0) - 0.5) * 0.12) * (v < 0.22) * (w > 0.05) \
        * (noise3(Q * np.array([1, 0.1, 1]), 0.08, 7) > 0.1)
    stain = np.maximum(np.maximum(soak, blot), runs - 0.0001 * (runs == 0))
    gore = smax(paper - 0.0018, -stain, 0.001)
    ribbon = smax(ribbon, stain, 0.001)          # the stain soaks the ribbon too
    return (lo, paper, vox), (lo, robust_distance(ribbon.astype(np.float32), vox), vox), \
        (lo, robust_distance(gore.astype(np.float32), vox), vox)


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
    runs = np.full(x.shape, -1.0, np.float32)
    for xr, y0, wd in ((-1.24, 0.47, 0.014), (-1.31, 0.58, 0.008)):
        runs = np.maximum(runs, (wd * (0.6 + 0.4 * np.clip((y - y0) / 0.1, 0, 1)) - np.abs(x - xr)) * (y > y0))
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
WALL_LO, WALL_HI, WALL_PX = (-2.35, 0.0), (1.20, 1.95), 0.003


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
        cap = (0.44 if not late else 0.40 + 0.03 * (i == 8)) * rng.uniform(0.88, 1.15)
        base = 0.05 * np.sin(i * 1.7) + rng.normal(0, 0.02) - (0.03 * (i - 5) if late else 0.0)
        tilt = np.radians(rng.normal(0, 8 if not late else 12))
        Rt = np.array([[np.cos(tilt), -np.sin(tilt)], [np.sin(tilt), np.cos(tilt)]])
        for s in strokes:
            p = np.array(s, float) * cap
            p = p + rng.normal(0, 0.018 if not late else 0.026, p.shape)
            # the forehead overshoots the end of a stroke as it is dragged off
            p = np.vstack([p, p[-1] + (p[-1] - p[-2]) * rng.uniform(0.03, 0.12)])
            p = p @ Rt.T + np.array([x, base])
            items.append((i, p, late))
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
        width0 = (0.062 if not late else 0.052) * (1 + 0.12 * rng.normal())
        for c, sc, t in zip(path, s, tang):
            load = np.exp(-sc / (0.8 if not late else 0.5))       # the blood runs out along a stroke
            wdt = width0 * (0.55 + 0.45 * load) * (1 + 0.22 * noise1(sc * 12 + k * 17, k))
            nrm = np.array([-t[1], t[0]])
            dry = 0.40 * (1 - load) + 0.02

            def keep(dx, dy, nrm=nrm, k=k, dry=dry, sc=sc):
                o = (dx * nrm[0] + dy * nrm[1]) / wdt
                # the streaks a dragged forehead leaves (skin and hair), breaking up as it dries
                streak = noise1(o * 26 + k * 31, 100 + k) * 0.5 + 0.5
                return streak > dry * (0.7 + 0.3 * noise1(sc * 25 + k, 200 + k))
            stamp(c, wdt / 2, keep=keep, h=0.0010 + 0.0008 * load)
            if rng.random() < 0.035 * (0.3 + load) and t[0] ** 2 > 0.1:
                drips.append((c + np.array([0, -wdt * 0.35]), load))
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
    rad = 0.062 * (1 + 0.35 * noise1(a * 3 + 20, 300) + 0.15 * noise1(a * 11 + 50, 301))
    inb = sel & (np.hypot(dx / 1.1, dy) < rad)
    mask |= inb
    thick[inb] = 0.0026
    for _ in range(260):
        a = rng.uniform(0, 2 * np.pi)
        dist = 0.10 + 0.40 * rng.random() ** 2.2
        c = contact + dist * np.array([np.cos(a), np.sin(a) * 0.8])
        r0 = max(0.0012, 0.006 * (1 - dist / 0.55) * rng.random())
        stamp(c, r0, h=0.0012)
        if rng.random() < 0.5:                                       # the tail each drop leaves, flying outward
            for q in range(1, 4):
                stamp(c + q * r0 * 1.2 * np.array([np.cos(a), np.sin(a) * 0.8]), r0 * (1 - q * 0.22), h=0.001)
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
    # a crushed, lopsided bow on top of the first band, and a strip of tape at the foot
    b.group('bow', margin=0.02)
    yt = top_of(paper, 0.44, 0.02)
    bc = np.array([PRESENT_O[0] + 0.44, yt + 0.012, PRESENT_O[2] + 0.02])
    b.torus(bc + [-0.035, 0.012, 0.01], 0.038, 0.007, RIBBON, op=UNION, R=rot(20, 70, 25))
    b.torus(bc + [0.04, 0.004, -0.02], 0.034, 0.007, RIBBON, op=UNION, R=rot(-30, 20, -15))     # squashed flat
    b.sphere(bc, 0.016, RIBBON, op=UNION)
    b.box(bc + [0.03, -0.006, 0.07], (0.012, 0.002, 0.07), RIBBON, op=UNION, R=rot(-35, 0, 8))
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
    for x, y0, y1, r in ((-1.24, 0.47, 0.25, 0.006), (-1.17, 0.47, 0.33, 0.004), (-0.78, 0.47, 0.30, 0.004)):
        b.capsule((x, y0, R.BED['z1'] + 0.035), (x + 0.003, y1, R.BED['z1'] + 0.035), r, GORE, op=UNION)
        b.sphere((x + 0.003, y1, R.BED['z1'] + 0.036), r * 1.4, GORE, op=UNION)
    b.group('floor_gore', margin=0.01)
    b.grid(*cached('floorpools', floor_pools, deps()), GORE, op=UNION)
    # the writing on the wall
    b.group('writing', margin=0.01)
    b.grid(*cached('wallblood', wall_blood, deps(), tuple(np.round(r_centre, 4)), tuple(np.round(contact, 4))),
           BLOOD, op=UNION)
    wreckage(b)
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
        b.box(c + [0, 0.10, 0], (0.34, 0.10, 0.23), mat, op=UNION, r=0.03, R=Rs @ rot(0, 4, -6))
        b.box(c + [0, 0.23, 0], (0.28, 0.06, 0.18), mat, op=SUB, r=0.03, R=Rs @ rot(0, -12, 8))   # stamped in
        for sg in (-1, 1):
            b.cylinder(c + Rs @ np.array([sg * 0.28, 0.21, 0.18]), 0.02, 0.025, BLACKMETAL, op=UNION, R=rot(0, 90, 0))
    else:
        b.box(c + [0, 0.03, 0], (0.36, 0.03, 0.24), mat, op=UNION, r=0.02, R=Rs @ rot(0, 0, 3))
        b.box(c + [0, 0.05, 0], (0.335, 0.03, 0.215), mat, op=SUB, r=0.015, R=Rs @ rot(0, 0, 3))


def wreckage(b):
    rng = np.random.default_rng(7)
    # --- shredded sheets: torn strips trailing across the floor from the bed
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
            c[1] = floor_y(c) + 0.004 + 0.012 * rng.random()
            b.box(c, (L / 2 + 0.01, 0.0025, wdt / 2), LINEN, op=UNION, r=0.002, R=rot(-yaw, rng.normal(0, 8), rng.normal(0, 6)))
            p = p + dirv * L
    # the torn top sheet dragged off the bed and heaped at its foot, crumpled
    b.group('sheet_heap', margin=0.03)
    b.grid(*cached('sheetheap', sheet_heap, deps()), LINEN, op=UNION)
    # --- broken glass: shards everywhere, thickest under the smashed mirror
    b.group('glass', margin=0.02)
    for k in range(190):
        if k < 80:
            c = np.array([R.HALF_W - 0.45 - 1.3 * rng.random() ** 1.5, 0.0, R.DRESSER_Z + rng.normal(0, 0.5)])
        else:
            c = np.array([rng.uniform(-0.3, 2.0), 0.0, rng.uniform(-4.2, -1.8)])
        s = 0.01 + 0.05 * rng.random() ** 2.0
        c[1] = 0.0025 + floor_y(c)
        Rr = rot(rng.uniform(0, 360), rng.normal(0, 6), rng.normal(0, 6))
        b.box(c, (s, 0.0015, s * rng.uniform(0.4, 1.0)), GLASS, op=UNION, R=Rr)
        b.halfspace(c, Rr @ rot(0, 0, 90) @ rot(rng.uniform(-50, 50), 0, 0), GLASS, op=SUB)
    # --- the luggage of someone coming home for Christmas: four cases thrown about and burst open
    b.group('suitcases', margin=0.03)
    suitcase(b, rng, (0.20, 0.012, -2.95), -18, 'burst')
    suitcase(b, rng, (1.55, 0.0, -2.95), 64, 'side', mat=LEATHER)
    suitcase(b, rng, (-0.05, 0.0, -4.00), 25, 'upturned', mat=CLOTH_MID)
    suitcase(b, rng, (1.60, 0.0, -4.45), -40, 'lid')
    suitcase(b, rng, (0.95, 0.0, -1.95), 8, 'upturned')
    # everything that was in them, flung across the room: ordinary clothes, and Christmas ones
    b.group('clothes', margin=0.03)
    kinds = [((0.55, -2.15), 'top', CLOTH_LIGHT), ((0.05, -2.9), 'trousers', DENIM), ((1.15, -2.55), 'ball', CLOTH_MID),
             ((0.70, -3.20), 'top', XMAS_JUMPER), ((1.85, -2.35), 'ball', CLOTH_LIGHT), ((-0.15, -3.45), 'top', COAT),
             ((1.25, -3.55), 'trousers', CLOTH_MID), ((0.35, -3.70), 'long', XMAS_GREEN_KNIT), ((1.10, -1.85), 'top', DENIM),
             ((1.95, -3.95), 'ball', XMAS_JUMPER), ((0.30, -4.30), 'ball', CLOTH_LIGHT), ((0.60, -2.65), 'long', CLOTH_MID),
             ((-0.20, -2.25), 'ball', COAT), ((1.45, -2.10), 'long', LEATHER), ((0.95, -3.95), 'top', CLOTH_LIGHT),
             ((1.75, -3.45), 'top', CLOTH_MID), ((0.15, -3.10), 'ball', XMAS_JUMPER), ((0.85, -2.95), 'trousers', COAT)]
    for (x, z), kind, mat in kinds:
        garment(b, rng, (x, 0, z), kind, mat, size=rng.uniform(0.85, 1.1))
    # a Santa hat, knocked across the floor
    hc = np.array([1.30, 0.0, -2.30])
    b.cone(hc + [0, 0.02, 0], hc + [0.18, 0.06, 0.08], 0.09, 0.015, FELT, op=UNION)
    b.torus(hc + [0, 0.03, 0], 0.085, 0.025, FUR, op=UNION, R=rot(0, 0, 70) @ rot(90, 0, 0))
    b.sphere(hc + [0.20, 0.04, 0.10], 0.028, FUR, op=UNION)
    # toiletries spilled out of a wash bag
    b.group('toiletries', margin=0.02)
    for k in range(10):
        c = np.array([0.4 + rng.normal(0, 0.3), 0, -2.75 + rng.normal(0, 0.25)])
        c[1] = floor_y(c)
        L, r = rng.uniform(0.06, 0.16), rng.uniform(0.012, 0.03)
        a = rng.uniform(0, 2 * np.pi)
        d = np.array([np.cos(a), 0, np.sin(a)]) * L / 2
        b.capsule(c + [0, r, 0] - d, c + [0, r, 0] + d, r, (PLASTIC, CLOTH_MID, SHELL)[k % 3], op=UNION)
    # small presents, one crushed, one torn open
    b.group('small_presents', margin=0.02)
    for c, half, yaw, m in (((1.20, 0, -2.75), (0.09, 0.06, 0.07), 30, GIFT_RED),
                            ((0.55, 0, -3.45), (0.07, 0.07, 0.07), -15, 'wrap'),
                            ((1.95, 0, -3.10), (0.14, 0.035, 0.10), 55, GIFT_RED),
                            ((-0.15, 0, -2.60), (0.06, 0.045, 0.11), 70, 'wrap'),
                            ((0.25, 0, -1.95), (0.10, 0.05, 0.08), 12, GIFT_RED)):
        c = np.array(c, float)
        c[1] = half[1] + floor_y(c)
        Rg = rot(yaw, 0, 0)
        mat = GIFTWRAP if m == 'wrap' else m
        b.box(c, half, mat, op=UNION, r=0.004, R=Rg)
        b.box(c, (half[0] + 0.002, half[1] + 0.002, 0.009), RIBBON, op=UNION, R=Rg)
        b.box(c, (0.009, half[1] + 0.002, half[2] + 0.002), RIBBON, op=UNION, R=Rg)
    # the chest's drawers torn out and thrown down, one upside down
    b.group('drawers', margin=0.03)
    for c, yaw, roll in (((1.20, 0.10, -1.75), 35, 0), ((0.75, 0.10, -3.65), -20, 180), ((1.45, 0.11, -3.40), 70, 12)):
        Rd = rot(yaw, 0, roll)
        c = np.array(c)
        b.box(c, (0.24, 0.09, 0.45), DARKWOOD, op=UNION, r=0.006, R=Rd)
        b.box(c + Rd @ [0, 0.02, 0], (0.22, 0.09, 0.43), DARKWOOD, op=SUB, R=Rd)
    # a leather holdall slashed open, a pillow flung on the floor
    b.group('holdall', margin=0.03)
    hc = np.array([1.35, 0.17, -4.10])
    b.capsule(hc + [-0.25, 0, 0.08], hc + [0.25, 0, -0.08], 0.16, LEATHER, op=UNION)
    b.torus(hc + [0, 0.12, 0.02], 0.10, 0.012, LEATHER, op=UNION, R=rot(-17, 0, 0) @ rot(0, 90, 0))
    b.group('pillow', margin=0.02)
    b.ellipsoid((-0.15, 0.08, -3.2), (0.36, 0.07, 0.22), LINEN, op=UNION, R=rot(25))
    b.ellipsoid((-2.18, 0.80, -3.35), (0.10, 0.20, 0.30), LINEN, op=UNION, R=rot(0, 0, -18))
    # the desk lamp, smashed on the floor
    b.group('lamp', margin=0.02)
    lc = np.array([2.05, 0.0, -4.55])
    b.cylinder(lc + [0, 0.012, 0], 0.012, 0.08, BRASS, op=UNION)
    b.capsule(lc + [0, 0.02, 0], lc + [-0.32, 0.035, 0.12], 0.012, BRASS, op=UNION)
    b.cone(lc + [-0.32, 0.12, 0.12], lc + [-0.50, 0.12, 0.20], 0.12, 0.08, LINEN, op=UNION)
    b.cone(lc + [-0.32, 0.12, 0.12], lc + [-0.50, 0.12, 0.20], 0.11, 0.07, LINEN, op=SUB)


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
    fx = R.HALF_W - 0.26 - 0.27                    # the front edge of the top
    jc = np.array([fx + 0.12, top + 0.012, z0 - 0.02])
    b.box(jc, (0.12, 0.010, 0.17), CLOTH_LIGHT, op=UNION, r=0.008, R=rot(8))
    b.box((fx - 0.012, top - 0.16, z0 - 0.05), (0.010, 0.17, 0.15), CLOTH_LIGHT, op=SUNION, k=0.03,
          R=rot(0, 0, -4) @ rot(0, 6, 0))
    b.capsule((fx - 0.01, top - 0.02, z0 + 0.12), (fx - 0.03, top - 0.42, z0 + 0.16), 0.03, CLOTH_LIGHT, op=SUNION, k=0.03)
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


def wall_lights(b, t=0.0):
    """Coloured fairy lights strung in swags along the top of the back wall, under the cornice; the left end
    torn from its hook and hanging down."""
    b.group('wall_lights', margin=0.02)
    z = R.BACK_Z + 0.035
    y = R.EAVES - 0.16
    hooks = np.linspace(-2.25, 2.25, 8)
    pts = []
    # the left end has come away from its hook: it hangs down from the second hook
    a = np.array([hooks[1], y, z])
    for s in np.linspace(1, 0, 14):
        pts.append(a + np.array([-0.35 * (1 - s) ** 1.5, -0.95 * (1 - s), 0.02 * (1 - s)]))
    pts = pts[::-1]
    for h0, h1 in zip(hooks[1:-1], hooks[2:]):
        for s in np.linspace(0, 1, 12, endpoint=False):
            pts.append(np.array([h0 + (h1 - h0) * s, y - 0.12 * 4 * s * (1 - s), z]))
    pts.append(np.array([hooks[-1], y, z]))
    pts = np.array(pts)
    for p, q in zip(pts[:-1], pts[1:]):
        b.capsule(p, q, 0.0025, BLACKMETAL, op=UNION)
    for h in hooks[1:]:
        b.sphere((h, y + 0.005, z - 0.01), 0.008, BLACKMETAL, op=UNION)
    # bulbs every 11 cm along it, hanging from the wire
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s_all = np.concatenate([[0], np.cumsum(seg)])
    for i, s in enumerate(np.arange(0.05, s_all[-1], 0.11)):
        p = np.array([np.interp(s, s_all, pts[:, k]) for k in range(3)])
        col = (i * 3 + int(i * 0.37)) % 5
        b.cylinder(p + [0, -0.008, 0], 0.006, 0.005, BLACKMETAL, op=UNION)
        b.ellipsoid(p + [0, -0.026, 0.002], (0.0075, 0.014, 0.0075), (LIT if bulb_lit(i, t) else DEAD)[col], op=UNION)
