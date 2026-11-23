#!/usr/bin/env python3
"""MAP  bench_draw: the test bench's ONE-PASS drawing (learn step L2, proposal solid-body-moves, chat 33). Jason's
solid body (bench_pose), the car's window parts and the pistol are drawn into ONE picture through the film's own
camera (sets.Cam): every dot keeps the depth and the part of the nearest thing there, so what hides what is decided
by depth alone (no hand-made hiding map, no pieces joined by fades). The look is the house's: flat house colours,
house ink outlines on every silhouette and wherever two parts meet (vest/skin, body/car), the house head drawing
(views, as lying_flat draws it, laid at the head's depth) and the house circle hands (solid balls: a circle from
every side, hidden by depth like everything else).

  scene(k, sp) ..... triangles (camera-ready points, part id per triangle, object id) for body, car, gun, hands
  raster(cam, ..) .. the depth / part / object buffers (perspective-correct depth per dot)
  ink(..) .......... house outlines from the buffers (object or part changes; depth jumps inside the body)
  crossings(..) .... body points inside the car's solids or the pistol inside the body (the bar: 0)
  still(OUT, ..) ... the whole still; prints seconds per frame

    python3 source/bench_draw.py still OUT.png
"""
import math
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bench_pose as BP   # noqa: E402

INK = (24, 20, 22)
W, H = 1080, 1920
CAM4_0 = ((0.00, 1.62, 4.40), (0.00, 1.02, -0.60), 2000)      # shot 4's locked camera at its start (= shot 3's frame)


def colours(sp):
    import gta_cars as G
    return {'skin': tuple(sp['skin']), 'vest': tuple(sp.get('vest_c', (236, 230, 212))),
            'trousers': tuple(sp['trousers']), 'shoes': tuple(sp['shoe']), 'hair': tuple(sp['hair_c']),
            'door': G.TULIP_RED, 'body': G.TULIP_RED, 'dash': G.VINYL, 'seat': (120, 84, 62),
            'pillar': G.STRIPE, 'gun': (44, 44, 48), 'hand': tuple(sp['skin'])}


def _box(lo, hi):
    x0, y0, z0 = lo
    x1, y1, z1 = hi
    P = np.array([(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)], float)
    F = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    return P, np.array([t for a, b, c, d in F for t in ((a, b, c), (a, c, d))])


def _rod(a, b, r, n=8):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    u = np.cross(d, [0, 1, 0] if abs(d[1]) < 0.9 else [1, 0, 0])
    u /= np.linalg.norm(u)
    v = np.cross(d, u)
    ring = [u * math.cos(2 * math.pi * i / n) * r + v * math.sin(2 * math.pi * i / n) * r for i in range(n)]
    P = np.array([a + q for q in ring] + [b + q for q in ring])
    T = []
    for i in range(n):
        j = (i + 1) % n
        T += [(i, j, n + j), (i, n + j, n + i)]
    return P, np.array(T)


def _ball(c, r, n=14):
    P, T = [], []
    for i in range(n + 1):
        th = math.pi * i / n
        for j in range(2 * n):
            ph = 2 * math.pi * j / (2 * n)
            P.append(c + r * np.array([math.sin(th) * math.cos(ph), math.cos(th), math.sin(th) * math.sin(ph)]))
    for i in range(n):
        for j in range(2 * n):
            a, b = i * 2 * n + j, i * 2 * n + (j + 1) % (2 * n)
            T += [(a, b, b + 2 * n), (a, b + 2 * n, a + 2 * n)]
    return np.array(P), np.array(T)


def hand_balls(k, cam):
    """The house circle hand (satire_style: centre 12 units past the wrist along the forearm, radius 26 units,
    units of lying.M metres) as a ball: from every side a circle of the house size."""
    import lying as L
    out = []
    for sd in 'LR':
        el, wr = np.asarray(k['el' + sd]), np.asarray(k['wr' + sd])
        d = (wr - el) / np.linalg.norm(wr - el)
        out.append((wr + d * 12 * L.M, 26 * L.M))
    return out


def gun_mesh(k):
    """The pistol (gun3d_film's blocks) with its grip in the gun hand, laid flat on his chest along k.aim."""
    import gun3d_film as GF
    V, T, K = GF.mesh(1.0)
    d = np.asarray(k.aim, float) / np.linalg.norm(k.aim) if hasattr(k, 'aim') else np.array([1.0, 0, 0])
    fwd = np.asarray(k['fwd'], float)
    down = np.cross(fwd, d)
    if down[1] > 0:
        down = -down
    down /= np.linalg.norm(down)
    side = np.cross(d, down)
    el, wr = np.asarray(k['elR']), np.asarray(k['wrR'])
    hand = wr + (wr - el) / np.linalg.norm(wr - el) * 12 * 0.00152 - fwd * 0.012  # held between fist and chest
    Wp = hand + V[:, :1] * d + V[:, 1:2] * down + V[:, 2:3] * side
    return Wp, T


def scene(k, sp, cam):
    """[(points (N,3) car frame, tris (M,3), part name per tri, object name)]"""
    out = []
    P, T, part, bone, keep = BP.posed(k)
    # the 3D head and hand are not drawn: the house head drawing and the circle hands stand in (Sam's look)
    hide = np.array([str(b).startswith(('head', 'jaw', 'eye', 'oculi', 'tongue', 'levator', 'oris', 'orbicularis',
                                       'risorius', 'temporalis', 'special', 'mandible', 'wrist', 'finger',
                                       'metacarpal', 'thumb')) for b in bone])
    ok = keep & ~hide
    Tk = T[ok[T].all(1)]
    tp = np.array([BP.PARTS[int(np.bincount(part[t]).argmax())] for t in Tk])
    out.append((P, Tk, tp, 'jason'))
    for nm, pt, lo, hi in BP.car_window():
        Pb, Tb = _box(lo, hi)
        out.append((Pb, Tb, np.array([pt] * len(Tb)), nm))
    for nm, a, b, r in BP.windscreen_frame():
        Pr, Tr = _rod(a, b, r)
        out.append((Pr, Tr, np.array(['pillar'] * len(Tr)), nm))
    for i, (c, r) in enumerate(hand_balls(k, cam)):
        Pb, Tb = _ball(c, r)
        out.append((Pb, Tb, np.array(['hand'] * len(Tb)), 'hand' + 'LR'[i]))
    Pg, Tg = gun_mesh(k)
    out.append((Pg, Tg, np.array(['gun'] * len(Tg)), 'gun'))
    return out


def _proj(cam, P):
    c = np.asarray(cam.pos)
    d = P - c
    z = d @ np.asarray(cam.f)
    x = d @ np.asarray(cam.r)
    y = -(d @ np.asarray(cam.u))
    zc = np.maximum(z, cam.NEAR)
    return np.stack([540 + x * cam.focal / zc + cam.shake[0], 960 + y * cam.focal / zc + cam.shake[1]], 1), z


@njit(cache=True)
def _fill(xy, z, T, tpi, zb, pb, ob, oi, near, ab, attrs, use_ab):
    """One object's triangles into the buffers, in order (speed-up step 5, chat 40): the same sums, in the same
    order, as the numpy loop it replaced (kept as _raster_py, the referee), so every dot comes out the same."""
    h, w = zb.shape
    for ti in range(len(T)):
        a, b, c = T[ti, 0], T[ti, 1], T[ti, 2]
        if min(z[a], z[b], z[c]) <= near:
            continue
        pa0, pa1, pb0, pb1, pc0, pc1 = xy[a, 0], xy[a, 1], xy[b, 0], xy[b, 1], xy[c, 0], xy[c, 1]
        x0 = int(max(0.0, math.floor(min(pa0, pb0, pc0))))
        x1 = int(min(w - 1.0, math.ceil(max(pa0, pb0, pc0))))
        y0 = int(max(0.0, math.floor(min(pa1, pb1, pc1))))
        y1 = int(min(h - 1.0, math.ceil(max(pa1, pb1, pc1))))
        if x1 < x0 or y1 < y0:
            continue
        den = (pb1 - pc1) * (pa0 - pc0) + (pc0 - pb0) * (pa1 - pc1)
        if abs(den) < 1e-9:
            continue
        for yy in range(y0, y1 + 1):
            Y = yy + 0.5
            for xx in range(x0, x1 + 1):
                X = xx + 0.5
                l1 = ((pb1 - pc1) * (X - pc0) + (pc0 - pb0) * (Y - pc1)) / den
                l2 = ((pc1 - pa1) * (X - pc0) + (pa0 - pc0) * (Y - pc1)) / den
                l3 = 1 - l1 - l2
                if l1 < -1e-6 or l2 < -1e-6 or l3 < -1e-6:
                    continue
                iz = l1 / z[a] + l2 / z[b] + l3 / z[c]
                zz = 1.0 / iz
                if not zz < zb[yy, xx]:
                    continue
                zb[yy, xx] = zz
                pb[yy, xx] = tpi[ti]
                ob[yy, xx] = oi
                if use_ab:
                    wa = l1 / z[a] * zz
                    wb_ = l2 / z[b] * zz
                    wc = l3 / z[c] * zz
                    for k in range(attrs.shape[1]):
                        ab[yy, xx, k] = wa * attrs[a, k] + wb_ * attrs[b, k] + wc * attrs[c, k]


def raster(cam, objs, scale=1, attrs=None):
    """Depth (metres along the lens), part index and object index per dot (scale: supersampling). attrs: per-point
    values of object 0 (Jason) interpolated per dot (his rest-body point and bone group), returned as ab."""
    if os.environ.get('BENCH_OLD_FILL'):
        return _raster_py(cam, objs, scale, attrs)
    w, h = W * scale, H * scale
    ab = np.zeros((h, w, attrs.shape[1])) if attrs is not None else None
    zb = np.full((h, w), np.inf)
    pb = np.full((h, w), -1, np.int64)
    ob = np.full((h, w), -1, np.int64)
    names = []
    for oi, (P, T, tp, nm) in enumerate(objs):
        xy, z = _proj(cam, P)
        xy = np.ascontiguousarray(xy * scale, float)
        tpi = np.array([PART_IX[x] for x in tp], np.int64)
        use = oi == 0 and ab is not None
        _fill(xy, np.ascontiguousarray(z, float), np.ascontiguousarray(T, np.int64), tpi, zb, pb, ob, oi,
              float(cam.NEAR), ab if use else np.zeros((1, 1, 1)),
              np.ascontiguousarray(attrs, float) if use else np.zeros((1, 1)), use)
        names.append(nm)
    if ab is not None:
        m = ob == 0
        if m.any():
            pb[m] = BP.part_at(ab[m][:, :3], ab[m][:, 3:])
    return zb, pb, ob, names


def _raster_py(cam, objs, scale=1, attrs=None):
    """Depth (metres along the lens), part index and object index per dot (scale: supersampling). attrs: per-point
    values of object 0 (Jason) interpolated per dot (his rest-body point and bone group), returned as ab."""
    w, h = W * scale, H * scale
    ab = np.zeros((h, w, attrs.shape[1])) if attrs is not None else None
    zb = np.full((h, w), np.inf)
    pb = np.full((h, w), -1, int)
    ob = np.full((h, w), -1, int)
    names = []
    for oi, (P, T, tp, nm) in enumerate(objs):
        xy, z = _proj(cam, P)
        xy = xy * scale
        for ti, (a, b, c) in enumerate(T):
            if min(z[a], z[b], z[c]) <= cam.NEAR:
                continue
            pa, pbb, pc = xy[a], xy[b], xy[c]
            x0, x1 = int(max(0, math.floor(min(pa[0], pbb[0], pc[0])))), int(min(w - 1, math.ceil(max(pa[0], pbb[0], pc[0]))))
            y0, y1 = int(max(0, math.floor(min(pa[1], pbb[1], pc[1])))), int(min(h - 1, math.ceil(max(pa[1], pbb[1], pc[1]))))
            if x1 < x0 or y1 < y0:
                continue
            den = (pbb[1] - pc[1]) * (pa[0] - pc[0]) + (pc[0] - pbb[0]) * (pa[1] - pc[1])
            if abs(den) < 1e-9:
                continue
            X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            l1 = ((pbb[1] - pc[1]) * (X - pc[0]) + (pc[0] - pbb[0]) * (Y - pc[1])) / den
            l2 = ((pc[1] - pa[1]) * (X - pc[0]) + (pa[0] - pc[0]) * (Y - pc[1])) / den
            l3 = 1 - l1 - l2
            m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
            if not m.any():
                continue
            iz = l1 / z[a] + l2 / z[b] + l3 / z[c]                  # 1/depth is straight in the picture
            zz = 1.0 / iz
            sub = zb[y0:y1 + 1, x0:x1 + 1]
            m &= zz < sub
            sub[m] = zz[m]
            pb[y0:y1 + 1, x0:x1 + 1][m] = PART_IX[tp[ti]]
            ob[y0:y1 + 1, x0:x1 + 1][m] = oi
            if oi == 0 and ab is not None:
                wa, wb_, wc = l1[m] / z[a] * zz[m], l2[m] / z[b] * zz[m], l3[m] / z[c] * zz[m]
                ab[y0:y1 + 1, x0:x1 + 1][m] = wa[:, None] * attrs[a] + wb_[:, None] * attrs[b] + wc[:, None] * attrs[c]
        names.append(nm)
    if ab is not None:
        m = ob == 0
        if m.any():
            pb[m] = BP.part_at(ab[m][:, :3], ab[m][:, 3:])
    return zb, pb, ob, names


PART_NAMES = ['skin', 'vest', 'trousers', 'shoes', 'hair', 'door', 'body', 'dash', 'seat', 'pillar', 'gun', 'hand']
PART_IX = {n: i for i, n in enumerate(PART_NAMES)}


def ink(zb, pb, ob, width):
    """House outlines: a dot is ink where its neighbour (within `width`) is another object or part, or where the
    depth jumps (a fold of the same body: an arm over the chest). The line sits on the nearer side."""
    h, w = zb.shape
    edge = np.zeros((h, w), bool)
    zf = np.where(np.isfinite(zb), zb, 1e3)
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        a = (slice(max(0, -dy), h - max(0, dy)), slice(max(0, -dx), w - max(0, dx)))
        b = (slice(max(0, dy), h - max(0, -dy) if dy < 0 else h), slice(max(0, dx), w if dx >= 0 else w + dx))
        b = (slice(a[0].start + dy, a[0].stop + dy), slice(a[1].start + dx, a[1].stop + dx))
        diff = (ob[a] != ob[b]) | (pb[a] != pb[b]) | (np.abs(zf[a] - zf[b]) > 0.03 + 0.02 * np.minimum(zf[a], zf[b]) / 4)
        near_a = zf[a] <= zf[b]
        ea = diff & near_a & (ob[a] >= 0)
        eb = diff & ~near_a & (ob[b] >= 0)
        edge[a] |= ea
        edge[b] |= eb
    if width > 1:
        from scipy import ndimage
        edge = ndimage.binary_dilation(edge, iterations=int(width // 2))
    return edge


def crossings(objs, k):
    """Body points inside the car's solid boxes (the window's opening and the cabin's air are free), and the
    pistol's points inside the body's trunk (a rough inside test: nearer the trunk's middle line than its skin)."""
    P, T, tp, _ = objs[0]
    used = np.unique(T)
    Q = P[used]
    hits = {}
    for nm, pt, lo, hi in BP.car_window():
        lo_, hi_ = np.asarray(lo), np.asarray(hi)
        m = np.all((Q > lo_) & (Q < hi_), 1)
        if m.any():
            dep = np.minimum(Q[m] - lo_, hi_ - Q[m]).min(1)          # how far inside, metres
            hits[nm] = (int(m.sum()), round(float(dep.max()) * 100, 1))   # (points, deepest cm)
    for nm, a, b, r in BP.windscreen_frame():
        a, b = np.asarray(a), np.asarray(b)
        d = b - a
        u = np.clip(((Q - a) @ d) / (d @ d), 0, 1)
        m = np.linalg.norm(Q - (a + u[:, None] * d), axis=1) < r - 0.003
        if m.any():
            hits[nm] = (int(m.sum()), None)
    # the pistol against the body: a pistol point is inside when it lies behind the skin's outward side at the
    # nearest skin point (the grip inside the fist ball is the grip, not a crossing: the hands are not the body mesh)
    from scipy.spatial import cKDTree
    import mesh_sdf as MS
    Tb = T
    N = MS.vertex_normals(P, Tb)
    tree = cKDTree(Q)
    for Qg, Tg, _, nm in objs:
        if nm != 'gun':
            continue
        dist, ix = tree.query(Qg)
        v = used[ix]
        side = np.einsum('ij,ij->i', Qg - P[v], N[v])
        sgn = np.sign(np.median(np.einsum('ij,ij->i', P[used] - P[used].mean(0), N[used])))   # the normals' way out
        m = side * sgn < -0.002
        if m.any():
            hits['pistol in body'] = (int(m.sum()), round(float(dist[m].max()) * 100, 1))
    return hits


def compose(zb, pb, ob, names, edge, cols, scale=1):
    img = np.zeros(zb.shape + (4,), np.uint8)
    for i, n in enumerate(PART_NAMES):
        m = pb == i
        img[m, :3] = cols[n]
        img[m, 3] = 255
    img[edge, :3] = INK
    img[edge, 3] = 255
    im = Image.fromarray(img, 'RGBA')
    if scale > 1:
        im = im.resize((W, H), Image.LANCZOS)
    return im


def house_head(cam, k, sp, neck=True):
    """The house head (views.head_view as lying_flat draws seated Jason), alone on a clear layer: the full drawing
    minus the same drawing with the head left out."""
    import lying_flat as LF
    import views as V
    def layer(nohead):
        img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        old, oldn, olda, oldl = V.head_view, LF._neck, LF._arm, LF._leg
        if nohead:                                    # the head and the house neck under it (its chin sits on it)
            V.head_view = lambda *a, **kw: None
        if nohead or not neck:                        # neck=False: the head alone (a solid neck stands under it;
            LF._neck = lambda *a, **kw: None          # the flat neck's outline drew a stray line down it, chat 38)
        # the flat arms and legs are not drawn: only the head is kept from this drawing (the solid body has its
        # own limbs), a flat arm crossing the head left a hole in it, and the flat arm's own check refused poses
        # the solid arm reaches (an elbow across the chest: the dressed clip stopped there, chat 44)
        LF._arm = LF._leg = lambda *a, **kw: None
        try:
            LF.draw(img, cam, k, sp)
        finally:
            V.head_view, LF._neck, LF._arm, LF._leg = old, oldn, olda, oldl
        return img
    full, nh = layer(False), layer(True)
    a, b = np.asarray(full).astype(int), np.asarray(nh).astype(int)
    m = np.abs(a - b).sum(2) > 0
    out = np.zeros_like(np.asarray(full))
    out[m] = np.asarray(full)[m]
    return Image.fromarray(out, 'RGBA'), full


def lay_head(img, head, zb_full, depth, scale=1):
    """The house head layer over img where nothing nearer than the head's depth is drawn (the roof rail in front
    of his crown hides it, as in the film)."""
    zb = zb_full[::scale, ::scale] if scale > 1 else zb_full
    a = np.asarray(head).copy()
    a[zb < depth - 0.05, 3] = 0
    img.alpha_composite(Image.fromarray(a, 'RGBA'))
    return img


def still(out, scale=2):
    import gta_cast as GC
    import leanout as LO
    import sets as S
    sp = dict(GC.cast()['jason'], mood='stern', squint=0.35, frown=0.07)
    k = LO.seated(sp)
    cam = S.Cam(*CAM4_0)
    t0 = time.time()
    objs = scene(k, sp, cam)
    rv, rg = BP.rest_attrs()
    zb, pb, ob, names = raster(cam, objs, scale, np.concatenate([rv, rg], 1))
    edge = ink(zb, pb, ob, 3 * scale)
    img = compose(zb, pb, ob, names, edge, colours(sp), scale)
    head, house = house_head(cam, k, sp)
    lay_head(img, head, zb, cam.depth(tuple(k['head'])), scale)
    secs = time.time() - t0
    img.save(out)
    house.save(out.replace('.png', '-house.png'))
    np.save(out.replace('.png', '-z.npy'), zb[::scale, ::scale])
    hits = crossings(objs, k)
    print('seconds per frame', round(secs, 1), 'crossings', hits or 0)
    return img, hits, secs




def _subdiv(P, T, A):
    """Each triangle into four (midpoints); points P and per-point values A follow."""
    e = {}
    P, A = list(P), list(A)
    def mid(i, j):
        key = (min(i, j), max(i, j))
        if key not in e:
            e[key] = len(P)
            P.append((np.asarray(P[i]) + P[j]) / 2)
            A.append((np.asarray(A[i]) + A[j]) / 2)
        return e[key]
    out = []
    for a, b, c in T:
        ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
        out += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]
    return np.array(P), np.array(out), np.array(A)


def export_blender(out_dir):
    """The same scene for Blender, in Blender's axes (car x, z, y): one OBJ per object kind with a material per
    house part. Jason's clothes are decided by the same rule as the one pass (bench_pose.part_at) on a body cut
    twice finer (Blender colours whole faces)."""
    import gta_cast as GC
    import leanout as LO
    import sets as S
    import json
    sp = dict(GC.cast()['jason'], mood='stern', squint=0.35, frown=0.07)
    k = LO.seated(sp)
    cam = S.Cam(*CAM4_0)
    objs = scene(k, sp, cam)
    rv, rg = BP.rest_attrs()
    P, T, _, _ = objs[0]
    used = np.unique(T)
    remap = -np.ones(len(P), int)
    remap[used] = np.arange(len(used))
    P2, T2, A2 = P[used], remap[T], np.concatenate([rv, rg], 1)[used]
    for _ in range(2):
        P2, T2, A2 = _subdiv(P2, T2, A2)
    cent = A2[T2].mean(1)
    parts = BP.part_at(cent[:, :3], cent[:, 3:])
    sw = lambda Q: np.asarray(Q)[:, [0, 2, 1]]
    def write(path, items):
        with open(path, 'w') as f:
            o = 0
            for Q, Ts, names in items:
                for q in sw(Q):
                    f.write('v %.5f %.5f %.5f\n' % tuple(q))
                for nm in sorted(set(names)):
                    f.write('usemtl %s\n' % nm)
                    for t, n in zip(Ts, names):
                        if n == nm:
                            f.write('f %d %d %d\n' % tuple(np.asarray(t)[::-1] + 1 + o))
                o += len(Q)
    write(os.path.join(out_dir, 'jason.obj'), [(P2, T2, [PART_NAMES[i] for i in parts])])
    write(os.path.join(out_dir, 'car.obj'), [(Q, Ts, list(tp)) for Q, Ts, tp, nm in objs[1:] if nm != 'gun'
                                             and not nm.startswith('hand')])
    write(os.path.join(out_dir, 'gun.obj'), [(Q, Ts, list(tp)) for Q, Ts, tp, nm in objs if nm == 'gun'])
    write(os.path.join(out_dir, 'hands.obj'), [(Q, Ts, list(tp)) for Q, Ts, tp, nm in objs if nm.startswith('hand')])
    head, _ = house_head(cam, k, sp)
    head.save(os.path.join(out_dir, 'head.png'))
    json.dump(dict(cam=CAM4_0, head_depth=cam.depth(tuple(k['head'])), cols={n: list(c) for n, c in colours(sp).items()},
                   ink=INK), open(os.path.join(out_dir, 'scene.json'), 'w'))
    print('exported', len(T2), 'body triangles')


if __name__ == '__main__':
    if sys.argv[1] == 'still':
        still(sys.argv[2])
    if sys.argv[1] == 'blender':
        export_blender(sys.argv[2])
