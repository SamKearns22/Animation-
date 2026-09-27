"""Hair for any character, from a style: locks combed over the scalp from the parting, then let fall under
gravity over the head, shoulders and clothes, with soft waves; stray strands (flyaways) where a style has
them - real hair never ends in a clean outline, and hair that does reads as a game model's "hair cards".

A style is a dict (see MOTHER in mother.py, GIRL in daughter.py):
    scalp_c, scalp_r    the scalp's egg shape in head coordinates (origin between the eyes; x to her left, y up,
                        z out of the face)
    part                the parting, radians round from the front of the head (negative: to her right)
    hairline            height at the middle, drop to 5 cm out, height and drop at the temple (head coords)
    top                 locks either side of the parting, (her right, her left)
    under               locks in the under layer round the back and sides
    length_top, length_under    (shortest, longest) fall in metres
    r_top, r_under      (radius on the scalp, radius falling) in metres
    wave                (period m, sideways, forwards) of the soft waves
    fullness            how far the hair stands out from the head below the ears
    forward             which locks fall forward over the shoulder: 'right', 'left', 'both' or 'none'
    crown_lift          lift at the crown, metres
    flyaways            number of stray strands, their radius, and how wild (0..1)
    base                (thickness at the front, at the crown) of the hair lying on the head
    box                 (lo, hi) of the hair's grid round the head position
    voxel               grid spacing
    seed
"""
import numpy as np

import rig
from rig import unit


def grid_sampler(grid):
    """Distance and outward direction at a point, read from a distance grid (lo, d, voxel, ...)."""
    lo, d, vox = grid[0], grid[1], grid[2]

    def at(p):
        g = (p - lo) / vox
        i = np.floor(g).astype(int)
        if np.any(i < 1) or np.any(i >= np.array(d.shape) - 2):
            return 1.0, np.zeros(3)
        f = g - i

        def tri(o):
            c = d[i[0] + o[0]:i[0] + o[0] + 2, i[1] + o[1]:i[1] + o[1] + 2, i[2] + o[2]:i[2] + o[2] + 2]
            c = c[0] * (1 - f[0]) + c[1] * f[0]
            c = c[0] * (1 - f[1]) + c[1] * f[1]
            return c[0] * (1 - f[2]) + c[1] * f[2]
        n = np.array([tri((1, 0, 0)) - tri((-1, 0, 0)), tri((0, 1, 0)) - tri((0, -1, 0)),
                      tri((0, 0, 1)) - tri((0, 0, -1))])
        return float(tri((0, 0, 0))), n / max(np.linalg.norm(n), 1e-9)
    return at


def _push_out_ellipsoid(p, c, r, margin):
    q = (p - c) / (r + margin)
    k = np.linalg.norm(q)
    if k < 1.0:
        return c + (p - c) / max(k, 1e-6)
    return p


def scalp_point(style, theta, elev, layer=0.0):
    """Point on the scalp (head coordinates): theta round from the front (+ towards her left), elev up from the
    widest line of the head."""
    q = np.array([np.cos(elev) * np.sin(theta), np.sin(elev), np.cos(elev) * np.cos(theta)])
    return np.asarray(style['scalp_c']) + q * (np.asarray(style['scalp_r']) + layer)


def locks(style, H, Rh, head, bodies=(), hides=None):
    """Paths of the locks (world coordinates) with their radii. head: the head's distance grid (head coords);
    bodies: distance grids the falling hair rests on - world grids (clothes), or (grid, origin, rotation) for
    one fixed to the head (a hat); hides(p): True where a point of hair (world) is hidden (under a hat) and
    needs no collision there."""
    rng = np.random.default_rng(style.get('seed', 2))
    out = []
    head_at = grid_sampler(head)
    def framed(g):
        """A grid given in a moving frame (grid, origin, rotation) - a hat on the head - as a world sampler."""
        at = grid_sampler(g[0])
        o, R = g[1], g[2]

        def f(p):
            dv, n = at(R.T @ (p - o))
            return dv, R @ n
        return f
    body_at = [framed(g) if len(g) == 3 and isinstance(g[0], tuple) else grid_sampler(g) for g in bodies]
    sc, sr = np.asarray(style['scalp_c']), np.asarray(style['scalp_r'])

    def off_skin(p, margin):
        pl = Rh.T @ (p - H)
        for _ in range(3):
            dv, n = head_at(pl)
            if dv >= margin:
                break
            pl = pl + n * (margin - dv)
        return H + Rh @ pl

    def collide(p, layer):
        pl = Rh.T @ (p - H)
        pl = _push_out_ellipsoid(pl, sc, sr, layer)
        p = off_skin(H + Rh @ pl, 0.004 + layer)
        for at in body_at:
            for _ in range(3):
                dv, n = at(p)
                if dv >= 0.003 + layer:
                    break
                p = p + n * (0.003 + layer - dv)
        return p

    wper, wside, wfwd = style['wave']
    fullness = style['fullness']
    shoulder_y = H[1] - style.get('shoulder_drop', 0.10)

    def lock(th0, e0, thf, side, forward, length, r_flat, r_fall, layer, lift=0.0, wild=0.0):
        pts = []
        for t in np.linspace(0, 1, 9):            # 1. over the scalp, from the root to where it starts to fall
            th = th0 + (thf - th0) * np.sqrt(t)
            el = e0 + (np.radians(4) - e0) * t * t
            q = H + Rh @ scalp_point(style, th, el, layer + lift * (1 - (1 - t) ** 2))
            pts.append(off_skin(q, r_flat + 0.0035 + layer))
        on_scalp = len(pts)
        p = pts[-1]                                # 2. falling
        d = pts[-1] - pts[-2]
        d /= np.linalg.norm(d)
        travelled, step = 0.0, 0.008
        wob = rng.uniform(0, 6.28)
        phase = rng.uniform(-0.5, 0.5)
        stray = rng.normal(size=3) * wild
        while travelled < length:
            force = np.array([0, -1.0, 0])
            pl = Rh.T @ (p - H)
            force += Rh @ np.array([np.sign(pl[0]) * fullness, 0, 0]) * (pl[1] > -0.12)
            # soft waves, in step from lock to lock (by height) so they read across the whole fall of hair
            wv = np.sin(2 * np.pi * p[1] / wper + phase) * min(1.0, travelled / 0.06)
            force += Rh @ np.array([np.sign(pl[0]) * wside * wv, 0, wfwd * wv])
            if p[1] < shoulder_y:
                fwd = Rh @ np.array([0, 0, 1.0])
                fwd[1] = 0
                fwd = unit(fwd)
                sidev = np.cross([0, 1.0, 0], fwd)
                force += (side * -0.10 * sidev + (0.55 if forward else -0.40) * fwd) * \
                    min(1, (shoulder_y - p[1]) / 0.08)
            force += 0.03 * np.array([np.sin(travelled * 8 + wob), 0, np.cos(travelled * 6 + wob)])
            force += stray * min(1.0, travelled / 0.05)  # a stray strand wanders off the fall
            d = d * 0.75 + 0.25 * force
            d /= np.linalg.norm(d)
            q = p + d * step
            p = q if (hides is not None and hides(q)) else collide(q, layer)
            travelled += step
            pts.append(p.copy())
        pts = np.array(pts)
        keep = list(range(on_scalp)) + list(range(on_scalp + 2, len(pts), 2))
        pts = pts[keep]
        t = np.linspace(0, 1, len(pts))
        grow = np.clip((np.arange(len(pts)) - on_scalp + 3) / 6.0, 0, 1)
        radii = (r_flat + (r_fall - r_flat) * grow) * np.clip((1 - t) / 0.35, 0.10, 1) ** 0.8
        out.append((pts, radii))

    def falls_forward(side, front):
        f = style['forward']
        return front and (f == 'both' or (f == 'right' and side < 0) or (f == 'left' and side > 0))

    part = style['part']
    lt, lu = style['length_top'], style['length_under']
    rt, ru = style['r_top'], style['r_under']
    # the top layer, combed out from the parting to both sides
    for side, n in zip((-1, 1), style['top']):
        for i in range(n):
            s = (i + rng.uniform(-0.3, 0.3)) / (n - 1)
            s = min(max(s, 0), 1)
            if s < 0.6:  # front half of the parting: forehead up to the top of the head
                th0, e0 = part, np.radians(38 + (90 - 38) * s / 0.6)
            else:  # back half: over the top to the crown
                th0, e0 = np.pi * side, np.radians(90 - 35 * (s - 0.6) / 0.4)
            thf = side * np.radians(72 + 95 * s)  # front locks fall in front of the ear, back ones behind
            lift = style['crown_lift'] * np.clip(s / 0.35, 0, 1) ** 2 * (1 - 0.5 * np.clip((s - 0.7) / 0.3, 0, 1))
            lock(th0 + side * 0.03, e0, thf, side, falls_forward(side, s < 0.55), rng.uniform(*lt), rt[0], rt[1],
                 0.0020 + 0.0030 * rng.random(), lift)
    # an under layer round the back and sides
    nu = style['under']
    for k in range(nu):
        side = -1 if k % 2 == 0 else 1
        th = side * np.radians(68 + 110 * (k // 2) / max(nu // 2 - 1, 1)) + rng.uniform(-0.03, 0.03)
        e0 = np.radians(rng.uniform(8, 30))
        lock(th, e0, th, side, falls_forward(side, abs(np.degrees(th)) < 110), rng.uniform(*lu), ru[0], ru[1],
             0.0010 + 0.0015 * rng.random())
    # stray strands: fine, a little apart from the rest, some catching the light round the face
    nf, rf, wild = style.get('flyaways', (0, 0.0, 0.0))
    for k in range(nf):
        side = -1 if rng.random() < 0.5 else 1
        s = rng.random()
        th0 = part if s < 0.6 else np.pi * side
        e0 = np.radians(rng.uniform(40, 85))
        thf = side * np.radians(70 + 100 * s)
        lock(th0 + side * 0.03, e0, thf, side, falls_forward(side, s < 0.5), rng.uniform(*lt) * rng.uniform(0.5, 1.0),
             rf, rf, 0.004 + 0.010 * rng.random(), 0.0, wild)
    return out


def np_cone(X, Y, Z, a, b, r1, r2):
    """Rounded cone from a (radius r1) to b (radius r2), on a grid."""
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
    return np.where(np.sign(z) * a2 * z2 > k, np.sqrt(xx + z2) * il2 - r2,
                    np.where(np.sign(y) * a2 * y2 < k, np.sqrt(xx + y2) * il2 - r1,
                             (np.sqrt(xx * a2 * il2) + y * rr) * il2 - r1))


def grid(style, H, Rh, head, bodies=(), hides=None):
    """The hair as a grid of distances in world coordinates, plus the direction the hair runs in each cell.
    Each lock is a chain of tapered tubes; neighbouring locks are blended, then small gaps closed up so the
    hair falls as a continuous sheet with the locks still showing in it."""
    from scipy import ndimage
    voxel = style.get('voxel', 0.0018)
    lks = locks(style, H, Rh, head, bodies, hides)
    lo, hi = H + np.asarray(style['box'][0]), H + np.asarray(style['box'][1])
    nn = np.round((hi - lo) / voxel).astype(int) + 1
    d = np.full(nn, 0.05, np.float32)
    flow = np.zeros(tuple(nn) + (3,), np.float32)
    k = 0.008
    for pts, radii in lks:
        kk = k if radii.max() > 0.002 else 0.002        # stray strands stay apart from the mass
        m = radii.max() + kk + 0.01
        L0 = np.maximum(np.floor((pts.min(0) - m - lo) / voxel).astype(int), 0)
        L1 = np.minimum(np.ceil((pts.max(0) + m - lo) / voxel).astype(int) + 1, nn)
        if np.any(L1 <= L0):
            continue
        tmp = np.full(tuple(L1 - L0), 0.05, np.float32)
        ftmp = np.zeros(tuple(L1 - L0) + (3,), np.float32)
        for a, b_, ra, rb in zip(pts[:-1], pts[1:], radii[:-1], radii[1:]):
            mm = max(ra, rb) + kk + 0.008
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
        d[gs] = rig.smin(g, tmp, kk)
    # the hair lying on the head: the head's own surface lifted a little, everywhere above the hairline -
    # a soft curve above the brows, dipping at the temples and in front of the ears
    hlo, hd, hvox = head
    hhi = hlo + (np.array(hd.shape) - 1) * hvox
    HL = style['hairline']
    b_front, b_crown = style.get('base', (0.0065, 0.013))
    part = style['part']
    sc = np.asarray(style['scalp_c'])
    xs = (lo[0] + np.arange(nn[0]) * voxel).astype(np.float32)
    ys = (lo[1] + np.arange(nn[1]) * voxel).astype(np.float32)
    zs = (lo[2] + np.arange(nn[2]) * voxel).astype(np.float32)
    base = np.full(nn, 0.05, np.float32)
    for i in range(nn[0]):  # a slab at a time, to keep memory modest
        X, Y, Z = np.meshgrid(xs[i:i + 1] - H[0], ys - H[1], zs - H[2], indexing='ij')
        lx = Rh[0, 0] * X + Rh[1, 0] * Y + Rh[2, 0] * Z
        ly = Rh[0, 1] * X + Rh[1, 1] * Y + Rh[2, 1] * Z
        lz = Rh[0, 2] * X + Rh[1, 2] * Y + Rh[2, 2] * Z
        coords = np.stack([(lx - hlo[0]) / hvox, (ly - hlo[1]) / hvox, (lz - hlo[2]) / hvox])
        hv = ndimage.map_coordinates(hd, coords.reshape(3, -1), order=1, mode='nearest').reshape(lx.shape)
        out = sum(np.maximum(np.maximum(hlo[q] - l, l - hhi[q]), 0) ** 2 for q, l in enumerate((lx, ly, lz)))
        hv = hv + np.sqrt(out)  # outside the head's box: keep counting the distance
        ax = np.abs(lx)
        y_hair = np.where(ax < 0.05, HL[0] - HL[1] * (ax / 0.05) ** 2,
                          HL[2] - HL[3] * np.clip((ax - 0.05) / 0.025, 0, 1))  # the hairline
        front = np.clip((lz + 0.035) / 0.02, 0, 1)
        edge = np.clip((ly - y_hair) / 0.014, 0, 1)
        edge = edge * edge * (3 - 2 * edge)
        thick = (b_front + (b_crown - b_front) * np.clip((ly - 0.03) / 0.08, 0, 1)) * (1 - front * 0.42 * (1 - edge))
        bb = hv - thick
        # edges rounded off (a sharp edge would ripple when stored on the grid)
        bb = -rig.smin(-bb, -(y_hair - ly) * front, 0.003)           # not over the face
        bb = -rig.smin(-bb, -(-(ly + 0.03)), 0.004)                  # not down the neck
        # the parting: a fine line along the meridian at `part`, from the hairline to the top of the head
        across = np.abs(lx * np.cos(part) - (lz - sc[2]) * np.sin(part))
        pp = np.where((ly > 0.04) & (lz > sc[2]), 0.0022 - across, -0.02)
        bb = -rig.smin(-bb, -pp, 0.0025)
        base[i:i + 1] = np.where(np.isfinite(bb), bb, 0.05)
    d = rig.smin(d, base.astype(np.float32), 0.004)
    # close small gaps between locks: grow a little, re-measure, shrink back (not so much that stray strands
    # are swallowed)
    grow = style.get('close', 0.0035)
    d = rig.robust_distance((d - grow).astype(np.float32), voxel) + grow
    d = rig.robust_distance(d.astype(np.float32), voxel)
    return lo, d, voxel, flow


DEPS = [grid_sampler, _push_out_ellipsoid, scalp_point, locks, np_cone, grid]
