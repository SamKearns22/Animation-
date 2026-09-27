"""Turn a triangle mesh (a MakeHuman body part) into a grid of signed distances our renderer can draw.

Exact distances to the nearest triangle are computed in a narrow band round the surface; the inside/outside
sign comes from the smoothed surface normal at the nearest point; beyond the band the distance is carried on
by a distance transform. A Catmull-Clark subdivision step first smooths MakeHuman's quads so the drawn surface
has no facets.
"""
import numpy as np
from numba import njit


def catmull_clark(verts, faces):
    """One step of Catmull-Clark subdivision of a quad mesh (faces: list of 4-index lists; triangles are
    allowed). Returns new verts and quads."""
    V = np.asarray(verts, float)
    nv = len(V)
    face_pts = np.array([V[f].mean(0) for f in faces])
    edges = {}
    for fi, f in enumerate(faces):
        for k in range(len(f)):
            a, b = f[k], f[(k + 1) % len(f)]
            e = (min(a, b), max(a, b))
            edges.setdefault(e, []).append(fi)
    ekeys = list(edges)
    eidx = {e: i for i, e in enumerate(ekeys)}
    edge_pts = np.empty((len(ekeys), 3))
    for i, e in enumerate(ekeys):
        fs = edges[e]
        if len(fs) == 2:
            edge_pts[i] = (V[e[0]] + V[e[1]] + face_pts[fs[0]] + face_pts[fs[1]]) / 4
        else:  # boundary edge
            edge_pts[i] = (V[e[0]] + V[e[1]]) / 2
    # move the original vertices
    F_sum = np.zeros((nv, 3))
    n_f = np.zeros(nv)
    for fi, f in enumerate(faces):
        for a in f:
            F_sum[a] += face_pts[fi]
            n_f[a] += 1
    R_sum = np.zeros((nv, 3))
    n_e = np.zeros(nv)
    boundary = np.zeros(nv, bool)
    B_sum = np.zeros((nv, 3))
    for e, fs in edges.items():
        mid = (V[e[0]] + V[e[1]]) / 2
        for a in e:
            R_sum[a] += mid
            n_e[a] += 1
        if len(fs) == 1:
            for a in e:
                boundary[a] = True
                B_sum[a] += mid
    newV = V.copy()
    ok = (n_f > 0) & ~boundary
    n = n_f[ok][:, None]
    newV[ok] = (F_sum[ok] / n + 2 * R_sum[ok] / n_e[ok][:, None] + (n - 3) * V[ok]) / n
    nb = boundary
    newV[nb] = (V[nb] * 2 + B_sum[nb] / 2) / 3  # approx. boundary rule
    verts2 = np.concatenate([newV, edge_pts, face_pts])
    eoff, foff = nv, nv + len(ekeys)
    quads = []
    for fi, f in enumerate(faces):
        m = len(f)
        for k in range(m):
            a, prev, nxt = f[k], f[(k - 1) % m], f[(k + 1) % m]
            quads.append([a, eoff + eidx[(min(a, nxt), max(a, nxt))], foff + fi,
                          eoff + eidx[(min(a, prev), max(a, prev))]])
    return verts2, quads


def triangulate(faces):
    tris = []
    for f in faces:
        for k in range(1, len(f) - 1):
            tris.append([f[0], f[k], f[k + 1]])
    return np.array(tris, np.int64)


def vertex_normals(V, T):
    fn = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    N = np.zeros_like(V)
    for k in range(3):
        np.add.at(N, T[:, k], fn)
    return N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-12)


@njit(cache=True)
def _closest_on_tri(p, a, b, c):
    """Closest point on triangle abc to p, with barycentric weights (Ericson, Real-Time Collision Detection)."""
    ab = b - a
    ac = c - a
    ap = p - a
    d1 = ab @ ap
    d2 = ac @ ap
    if d1 <= 0 and d2 <= 0:
        return a, 1.0, 0.0, 0.0
    bp = p - b
    d3 = ab @ bp
    d4 = ac @ bp
    if d3 >= 0 and d4 <= d3:
        return b, 0.0, 1.0, 0.0
    vc = d1 * d4 - d3 * d2
    if vc <= 0 and d1 >= 0 and d3 <= 0:
        v = d1 / (d1 - d3)
        return a + v * ab, 1 - v, v, 0.0
    cp = p - c
    d5 = ab @ cp
    d6 = ac @ cp
    if d6 >= 0 and d5 <= d6:
        return c, 0.0, 0.0, 1.0
    vb = d5 * d2 - d1 * d6
    if vb <= 0 and d2 >= 0 and d6 <= 0:
        w = d2 / (d2 - d6)
        return a + w * ac, 1 - w, 0.0, w
    va = d3 * d6 - d5 * d4
    if va <= 0 and (d4 - d3) >= 0 and (d5 - d6) >= 0:
        w = (d4 - d3) / ((d4 - d3) + (d5 - d6))
        return b + w * (c - b), 0.0, 1 - w, w
    denom = 1.0 / (va + vb + vc)
    v = vb * denom
    w = vc * denom
    return a + ab * v + ac * w, 1 - v - w, v, w


@njit(cache=True)
def _band(V, N, T, lo, voxel, shape, band, dist, sgn):
    for t in range(T.shape[0]):
        a, b, c = V[T[t, 0]], V[T[t, 1]], V[T[t, 2]]
        mn = np.minimum(np.minimum(a, b), c) - band
        mx = np.maximum(np.maximum(a, b), c) + band
        i0 = max(int((mn[0] - lo[0]) / voxel), 0)
        j0 = max(int((mn[1] - lo[1]) / voxel), 0)
        k0 = max(int((mn[2] - lo[2]) / voxel), 0)
        i1 = min(int((mx[0] - lo[0]) / voxel) + 1, shape[0] - 1)
        j1 = min(int((mx[1] - lo[1]) / voxel) + 1, shape[1] - 1)
        k1 = min(int((mx[2] - lo[2]) / voxel) + 1, shape[2] - 1)
        p = np.empty(3)
        for i in range(i0, i1 + 1):
            p[0] = lo[0] + i * voxel
            for j in range(j0, j1 + 1):
                p[1] = lo[1] + j * voxel
                for k in range(k0, k1 + 1):
                    p[2] = lo[2] + k * voxel
                    q, u, v, w = _closest_on_tri(p, a, b, c)
                    d = np.sqrt(((p - q) ** 2).sum())
                    if d < dist[i, j, k]:
                        dist[i, j, k] = d
                        n = u * N[T[t, 0]] + v * N[T[t, 1]] + w * N[T[t, 2]]
                        sgn[i, j, k] = 1.0 if (p - q) @ n >= 0 else -1.0


def mesh_to_sdf(V, T, lo, hi, voxel, band_vox=4):
    """Signed distance grid (inside negative) of the mesh over the box lo..hi."""
    from scipy import ndimage
    lo = np.asarray(lo, float)
    shape = tuple(np.round((np.asarray(hi) - lo) / voxel).astype(int) + 1)
    N = vertex_normals(V, T)
    dist = np.full(shape, 1e9)
    sgn = np.ones(shape)
    _band(np.ascontiguousarray(V, float), N, np.ascontiguousarray(T), lo, float(voxel), np.array(shape),
          band_vox * voxel, dist, sgn)
    inband = dist < band_vox * voxel
    # beyond the band: sign of the nearest band voxel, distance through the band
    d_out, idx = ndimage.distance_transform_edt(~inband, return_indices=True)
    near_d = dist[idx[0], idx[1], idx[2]]
    near_s = sgn[idx[0], idx[1], idx[2]]
    far = near_s * (near_d + d_out * voxel)
    d = np.where(inband, sgn * dist, far).astype(np.float32)
    return lo, d, voxel
