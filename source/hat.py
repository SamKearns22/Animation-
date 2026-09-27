"""A droopy felt Santa hat, made to fit a particular head (in head coordinates: origin between the eyes, x to
the wearer's left, y up, z out of the face).

A soft white fur band sits round the head above the brows and lower at the back; the red felt crown follows
the head and rises a little above it, then the long tip flops over to one side and hangs down beside the
head, ending in a fluffy pompom. The felt has a few soft creases where it folds.

    make(head_grid, side=+1) -> dict(felt=(lo, d, voxel), fur=(lo, d, voxel), under=(lo, d, voxel), ...)
    hidden(hat) -> a test: is a point (head coordinates) under the hat?
"""
import numpy as np

import rig


def _fbm(X, Y, Z, freq, seed, octaves=3):
    """Smooth value noise on a grid (for fur and felt), -0.5..0.5."""
    from scipy import ndimage
    rng = np.random.default_rng(seed)
    out = np.zeros(np.broadcast_shapes(X.shape, Y.shape, Z.shape), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        f = freq * 2 ** o
        n = rng.random((32, 32, 32)).astype(np.float32)
        coords = [((np.broadcast_to(A, out.shape) * f) % 32) for A in (X, Y, Z)]
        out += amp * ndimage.map_coordinates(n, coords, order=1, mode='wrap')
        tot += amp
        amp *= 0.5
    return out / tot - 0.5


def _capsule_chain(lo, n, voxel, pts, radii, far=0.05):
    """Distance to a chain of tapered tubes through pts with radii, on the grid (each tube only computed
    near itself)."""
    import hair
    d = np.full(tuple(n), far, np.float32)
    for a, b, ra, rb in zip(pts[:-1], pts[1:], radii[:-1], radii[1:]):
        m = max(ra, rb) + far
        i0 = np.maximum(np.floor((np.minimum(a, b) - m - lo) / voxel).astype(int), 0)
        i1 = np.minimum(np.ceil((np.maximum(a, b) + m - lo) / voxel).astype(int) + 1, n)
        if np.any(i1 <= i0):
            continue
        xs = [(lo[q] + np.arange(i0[q], i1[q]) * voxel) for q in range(3)]
        sl = tuple(slice(i0[q], i1[q]) for q in range(3))
        dc = hair.np_cone(xs[0][:, None, None], xs[1][None, :, None], xs[2][None, None, :], a, b, ra, rb)
        d[sl] = np.minimum(d[sl], dc.astype(np.float32))
    return d


def bezier(ctrl, n):
    ctrl = np.asarray(ctrl, float)
    t = np.linspace(0, 1, n)[:, None]
    k = len(ctrl) - 1
    from math import comb
    return sum(comb(k, i) * (1 - t) ** (k - i) * t ** i * ctrl[i] for i in range(k + 1))


def make(head, side=1.0, band_front=0.050, band_back=-0.005, clearance=0.009, voxel=0.0015, seed=7):
    """head: the head's distance grid (lo, d, voxel) in head coordinates. band_front/back: heights of the
    band above the eyes at the front and the back; clearance: room for the hair under the hat."""
    from scipy import ndimage
    hlo, hd, hvox = head
    hhi = hlo + (np.array(hd.shape) - 1) * hvox

    def head_d(P):
        P = np.asarray(P, float)
        idx = np.stack([((P[..., q] - hlo[q]) / hvox).reshape(-1) for q in range(3)])
        return ndimage.map_coordinates(hd, idx, order=1, mode='nearest').reshape(P.shape[:-1])

    # the band: round the head at a height falling from the front to the back, just outside the hair
    cz = (hlo[2] + hhi[2]) / 2 - 0.01
    ring = []
    for th in np.linspace(0, 2 * np.pi, 73)[:-1]:
        y = band_front + (band_back - band_front) * (1 - np.cos(th)) / 2
        dirv = np.array([np.sin(th), 0, np.cos(th)])
        r = 0.02
        while r < 0.2 and head_d(np.array([0, y, cz]) + dirv * r) < 0:
            r += 0.001
        ring.append(np.array([0, y, cz]) + dirv * (r + clearance))
    ring = np.array(ring + [ring[0]])
    top = hlo[1] + (np.array(hd.shape)[1] - 1) * hvox
    # the head's top: highest skin point
    ys = np.arange(hhi[1], 0, -0.002)
    for yy in ys:
        if head_d(np.array([0, yy, cz])) < 0:
            top = yy
            break
    # the grid: round the head's top, with room for the droop on one side
    lo = np.array([-0.16, band_back - 0.03, hlo[2] - 0.06])
    hi = np.array([0.16, top + 0.10, hhi[2] + 0.02])
    if side > 0:
        hi[0] += 0.06
    else:
        lo[0] -= 0.06
    lo[1] = min(lo[1], top - 0.28)
    n = np.round((hi - lo) / voxel).astype(int) + 1
    X, Y, Z = np.meshgrid(*[lo[q] + np.arange(n[q]) * voxel for q in range(3)], indexing='ij')
    P = np.stack([X, Y, Z], -1)
    hd_here = head_d(P).astype(np.float32)
    # the crown: the head swollen by the hair and the felt, cut off below the band
    th = np.arctan2(X, Z - cz)
    band_y = band_front + (band_back - band_front) * (1 - np.cos(th)) / 2
    crown = hd_here - (clearance + 0.004)
    crown = rig.smax(crown, band_y + 0.005 - Y, 0.004)     # (its edge tucked inside the fur)
    # the tip: rising a little above the crown, then flopping over to one side and hanging down beside the
    # head (a curve through control points), tapering to the pompom
    s = float(side)
    ctrl = [(0.0, top - 0.035, cz - 0.01), (0.0, top + 0.045, cz - 0.02), (s * 0.06, top + 0.06, cz - 0.03),
            (s * 0.125, top - 0.02, cz - 0.03), (s * 0.14, top - 0.14, cz - 0.01), (s * 0.13, top - 0.22, cz)]
    spine = bezier(ctrl, 48)
    tt = np.linspace(0, 1, 48)
    radii = 0.052 * (1 - tt) ** 1.2 + 0.008
    tip = _capsule_chain(lo, n, voxel, spine, radii)
    felt = rig.smin(crown, tip, 0.03)
    # soft creases where the felt folds over, and a little unevenness everywhere
    felt = felt + 0.0015 * _fbm(X, Y, Z, 25.0, seed) + 0.0025 * np.clip((Y - top) / 0.06, 0, 1) * \
        np.sin(np.arctan2(X - s * 0.05, Y - top) * 7.0)
    # the fur: the band, and the pompom on the tip
    fur = _capsule_chain(lo, n, voxel, ring, np.full(len(ring), 0.012))
    pom = spine[-1] + np.array([s * 0.005, -0.012, 0])
    fur = np.minimum(fur, np.sqrt(((P - pom) ** 2).sum(-1)) - 0.024)
    fur = fur - 0.004 * (_fbm(X, Y, Z, 180.0, seed + 1) + 0.5)
    felt = rig.smax(felt, -fur, 0.002)                              # the fur sits over the felt
    felt = rig.robust_distance(felt.astype(np.float32), voxel)
    fur = rig.robust_distance(fur.astype(np.float32), voxel)

    # where hair is hidden under the hat: inside it, or between it and the head above the band
    under = np.minimum(np.minimum(felt, fur), np.where((hd_here < clearance + 0.004) & (Y > band_y), -0.001, 0.01))
    return dict(felt=(lo, felt, voxel), fur=(lo, fur, voxel), under=(lo, under.astype(np.float32), voxel),
                spine=spine, top=top)


def hidden(hat):
    """A test for points in head coordinates: is this point under the hat (hidden by it)?"""
    lo, u, voxel = hat['under']
    n = np.array(u.shape)

    def inside(p_head):
        i = np.round((np.asarray(p_head) - lo) / voxel).astype(int)
        if np.any(i < 0) or np.any(i >= n):
            return False
        return bool(u[tuple(i)] < 0)
    return inside
