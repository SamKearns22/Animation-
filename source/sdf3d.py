"""A small 3D renderer for building scenes out of smooth shapes ("signed distance fields").

Every object is made of simple solids - spheres, ellipsoids, capsules, rounded boxes, cones - blended
smoothly together, the way a sculptor adds and carves clay. Rays are fired from a camera into the scene;
where one hits a surface we light it: a soft key light with soft shadows, sky fill with ambient occlusion,
lamps, glowing flames, reflections in marble and steel.

Besides the picture, the renderer saves everything a draughtsman needs to redraw the frame by hand:
depth, surface direction, which material each pixel is, and where it sits in the world.

The scene is a table of primitives (see Builder), grouped into objects with bounding spheres so that
each ray only does real work near the objects it passes.
"""
import math

import numpy as np
from numba import njit, prange

# primitive types
SPHERE, ELLIPSOID, RBOX, CAPSULE, RCONE, CYL, TORUS, HALFSPACE, CAP, GRID, LENS = range(11)
# how a primitive combines with the object built so far
UNION, SUNION, SSUB, SINTER, SUB = range(5)
NC = 24  # columns per primitive: type, op, k, material, origin(3), rotation(9), params(8)


# ---------------------------------------------------------------------------
# Building scenes
# ---------------------------------------------------------------------------
def rot(yaw=0.0, pitch=0.0, roll=0.0):
    """Rotation matrix (local -> world): yaw about y, then pitch about x, then roll about z (degrees)."""
    y, p, r = np.radians([yaw, pitch, roll])
    Ry = np.array([[np.cos(y), 0, np.sin(y)], [0, 1, 0], [-np.sin(y), 0, np.cos(y)]])
    Rx = np.array([[1, 0, 0], [0, np.cos(p), -np.sin(p)], [0, np.sin(p), np.cos(p)]])
    Rz = np.array([[np.cos(r), -np.sin(r), 0], [np.sin(r), np.cos(r), 0], [0, 0, 1]])
    return Ry @ Rx @ Rz


def frame_from_axis(a, b):
    """A rotation whose local +y runs from a to b (for capsules and cones). Returns local->world."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    yv = b - a
    yv = yv / np.linalg.norm(yv)
    helper = np.array([0, 0, 1.0]) if abs(yv[2]) < 0.9 else np.array([1.0, 0, 0])
    xv = np.cross(yv, helper)
    xv /= np.linalg.norm(xv)
    zv = np.cross(xv, yv)
    return np.stack([xv, yv, zv], 1)


class Builder:
    """Collects primitives into groups. Positions can be given in a local frame (e.g. the head)."""

    def __init__(self):
        self.rows = []
        self.groups = []
        self.frame_o = np.zeros(3)
        self.frame_R = np.eye(3)

    def set_frame(self, origin=(0, 0, 0), R=None):
        self.frame_o = np.asarray(origin, float)
        self.frame_R = np.eye(3) if R is None else np.asarray(R, float)

    def group(self, name, disp=0, dparams=(), margin=0.01):
        self.groups.append(dict(name=name, start=len(self.rows), disp=disp,
                                dparams=list(dparams) + [0.0] * (33 - len(dparams)), margin=margin, bounds=[]))

    def _add(self, typ, op, k, mat, origin, Rl, params, bound_r, bound_c=None):
        """origin, Rl (local->frame) in the current frame. Stores world->prim transform."""
        o_w = self.frame_o + self.frame_R @ np.asarray(origin, float)
        R_lw = self.frame_R @ (np.eye(3) if Rl is None else np.asarray(Rl, float))  # prim-local -> world
        row = np.zeros(NC)
        row[0], row[1], row[2], row[3] = typ, op, max(k, 1e-6), mat
        row[4:7] = o_w
        row[7:16] = R_lw.T.reshape(-1)  # world -> prim-local
        row[16:16 + len(params)] = params
        self.rows.append(row)
        if op in (UNION, SUNION):
            c = o_w if bound_c is None else self.frame_o + self.frame_R @ np.asarray(bound_c, float)
            self.groups[-1]['bounds'].append((c, bound_r + k))

    # shapes -----------------------------------------------------------------
    def sphere(self, c, r, mat, op=SUNION, k=0.0):
        self._add(SPHERE, op, k, mat, c, None, [r], r)

    def ellipsoid(self, c, radii, mat, op=SUNION, k=0.0, R=None):
        self._add(ELLIPSOID, op, k, mat, c, R, list(radii), max(radii))

    def box(self, c, half, mat, op=SUNION, k=0.0, r=0.0, R=None):
        self._add(RBOX, op, k, mat, c, R, list(half) + [r], float(np.linalg.norm(half)))

    def capsule(self, a, b, r, mat, op=SUNION, k=0.0):
        a, b = np.asarray(a, float), np.asarray(b, float)
        h = float(np.linalg.norm(b - a))
        self._add(CAPSULE, op, k, mat, a, frame_from_axis(a, b), [h, r], h / 2 + r, (a + b) / 2)

    def cone(self, a, b, r1, r2, mat, op=SUNION, k=0.0):
        a, b = np.asarray(a, float), np.asarray(b, float)
        h = float(np.linalg.norm(b - a))
        self._add(RCONE, op, k, mat, a, frame_from_axis(a, b), [h, r1, r2], h / 2 + max(r1, r2), (a + b) / 2)

    def cylinder(self, c, h, r, mat, op=SUNION, k=0.0, rr=0.0, R=None):
        """Vertical (local y) cylinder, half-height h, radius r, edge rounding rr."""
        self._add(CYL, op, k, mat, c, R, [h, r, rr], float(np.hypot(h, r)))

    def torus(self, c, R0, r, mat, op=SUNION, k=0.0, R=None):
        self._add(TORUS, op, k, mat, c, R, [R0, r], R0 + r)

    def cap(self, c, radius, offset, R, mat, op=SUNION, k=0.0):
        """Part of a sphere (centre c) beyond a plane: local +y (from R) is the plane normal."""
        self._add(CAP, op, k, mat, c, R, [radius, offset], radius)

    def grid(self, corner, sdf, voxel, mat, op=UNION, k=0.0, R=None):
        """A shape given as a numpy array of distances (x, y, z order), its minimum corner at `corner`."""
        if not hasattr(self, 'grids'):
            self.grids = []
            self.grid_len = 0
        off = self.grid_len
        self.grids.append(np.ascontiguousarray(sdf, dtype=np.float32).reshape(-1))
        self.grid_len += sdf.size
        nx, ny, nz = sdf.shape
        half = np.array([nx - 1, ny - 1, nz - 1]) * voxel / 2
        self._add(GRID, op, k, mat, corner, R, [off, nx, ny, nz, voxel], float(np.linalg.norm(half)),
                  np.asarray(corner, float) + (R if R is not None else np.eye(3)) @ half)

    def grid_buffer(self):
        if not hasattr(self, 'grids'):
            return np.zeros(8, np.float32)
        return np.concatenate(self.grids)

    def lens(self, c, cu, ru, cl, rl, zlo, zhi, mat, op=SSUB, k=0.0, R=None):
        self._add(LENS, op, k, mat, c, R, [cu[0], cu[1], ru, cl[0], cl[1], rl, zlo, zhi], 0.03)

    def halfspace(self, c, R, mat=0, op=SSUB, k=0.0):
        """Solid below the local y=0 plane through c (use with SSUB / SINTER to cut)."""
        self._add(HALFSPACE, op, k, mat, c, R, [], 0)

    def build(self):
        P = np.array(self.rows, dtype=np.float64)
        G = np.zeros((len(self.groups), 40))
        for gi, g in enumerate(self.groups):
            end = self.groups[gi + 1]['start'] if gi + 1 < len(self.groups) else len(self.rows)
            cs = np.array([b[0] for b in g['bounds']])
            rs = np.array([b[1] for b in g['bounds']])
            lo = (cs - rs[:, None]).min(0)
            hi = (cs + rs[:, None]).max(0)
            c = (lo + hi) / 2
            r = float(np.max(np.linalg.norm(cs - c, axis=1) + rs)) + g['margin']
            G[gi, 0:3] = c
            G[gi, 3] = r
            G[gi, 4], G[gi, 5], G[gi, 6] = g['start'], end, g['disp']
            G[gi, 7:40] = g['dparams']
        return P, G


# ---------------------------------------------------------------------------
# Distance functions
# ---------------------------------------------------------------------------
@njit(fastmath=True, cache=True)
def cr_weights(f):
    """Catmull-Rom weights for the four samples around a point: smooth (C1) interpolation."""
    f2 = f * f
    f3 = f2 * f
    return (-0.5 * f3 + f2 - 0.5 * f, 1.5 * f3 - 2.5 * f2 + 1.0, -1.5 * f3 + 2.0 * f2 + 0.5 * f, 0.5 * f3 - 0.5 * f2)


@njit(fastmath=True, cache=True)
def grid_sdf(x, y, z, P, i, GB):
    """A shape stored as a 3D table of distances (sculpted in numpy), read with smooth cubic blending."""
    off = int(P[i, 16])
    nx, ny, nz = int(P[i, 17]), int(P[i, 18]), int(P[i, 19])
    vs = P[i, 20]
    gx, gy, gz = x / vs, y / vs, z / vs
    ex = max(-gx, gx - (nx - 1), 0.0)
    ey = max(-gy, gy - (ny - 1), 0.0)
    ez = max(-gz, gz - (nz - 1), 0.0)
    if ex > 0.0 or ey > 0.0 or ez > 0.0:
        return math.sqrt(ex * ex + ey * ey + ez * ez) * vs + 0.004
    ix = min(int(gx), nx - 2)
    iy = min(int(gy), ny - 2)
    iz = min(int(gz), nz - 2)
    fx, fy, fz = gx - ix, gy - iy, gz - iz
    wx0, wx1, wx2, wx3 = cr_weights(fx)
    wy0, wy1, wy2, wy3 = cr_weights(fy)
    wz0, wz1, wz2, wz3 = cr_weights(fz)
    total = 0.0
    for a in range(4):
        xi = min(max(ix - 1 + a, 0), nx - 1)
        wa = wx0 if a == 0 else (wx1 if a == 1 else (wx2 if a == 2 else wx3))
        acc_y = 0.0
        for bb in range(4):
            yi = min(max(iy - 1 + bb, 0), ny - 1)
            wb = wy0 if bb == 0 else (wy1 if bb == 1 else (wy2 if bb == 2 else wy3))
            base = off + (xi * ny + yi) * nz
            z0 = min(max(iz - 1, 0), nz - 1)
            z1 = iz
            z2 = min(iz + 1, nz - 1)
            z3 = min(iz + 2, nz - 1)
            acc_y += wb * (wz0 * GB[base + z0] + wz1 * GB[base + z1] + wz2 * GB[base + z2] + wz3 * GB[base + z3])
        total += wa * acc_y
    return total


@njit(fastmath=True, cache=True)
def prim_sdf(t, x, y, z, P, i, GB):
    if t == 0:
        return math.sqrt(x * x + y * y + z * z) - P[i, 16]
    elif t == 1:
        rx, ry, rz = P[i, 16], P[i, 17], P[i, 18]
        ax, ay, az = x / rx, y / ry, z / rz
        k0 = math.sqrt(ax * ax + ay * ay + az * az)
        bx, by, bz = ax / rx, ay / ry, az / rz
        k1 = math.sqrt(bx * bx + by * by + bz * bz)
        if k1 < 1e-9:
            return -min(rx, min(ry, rz))
        return k0 * (k0 - 1.0) / k1
    elif t == 2:
        r = P[i, 19]
        qx = abs(x) - P[i, 16] + r
        qy = abs(y) - P[i, 17] + r
        qz = abs(z) - P[i, 18] + r
        ox, oy, oz = max(qx, 0.0), max(qy, 0.0), max(qz, 0.0)
        return math.sqrt(ox * ox + oy * oy + oz * oz) + min(max(qx, max(qy, qz)), 0.0) - r
    elif t == 3:
        h = P[i, 16]
        yy = y - min(max(y, 0.0), h)
        return math.sqrt(x * x + yy * yy + z * z) - P[i, 17]
    elif t == 4:
        h, r1, r2 = P[i, 16], P[i, 17], P[i, 18]
        b = (r1 - r2) / h
        a = math.sqrt(max(1.0 - b * b, 0.0))
        qx = math.sqrt(x * x + z * z)
        k = -b * qx + a * y
        if k < 0.0:
            return math.sqrt(qx * qx + y * y) - r1
        if k > a * h:
            return math.sqrt(qx * qx + (y - h) * (y - h)) - r2
        return a * qx + b * y - r1
    elif t == 5:
        rr = P[i, 18]
        dx = math.sqrt(x * x + z * z) - P[i, 17] + rr
        dy = abs(y) - P[i, 16] + rr
        mx, my = max(dx, 0.0), max(dy, 0.0)
        return min(max(dx, dy), 0.0) + math.sqrt(mx * mx + my * my) - rr
    elif t == 6:
        qx = math.sqrt(x * x + z * z) - P[i, 16]
        return math.sqrt(qx * qx + y * y) - P[i, 17]
    elif t == 7:
        return y
    elif t == 8:
        # a spherical cap: the part of a sphere on the +y side of a plane (eyelids)
        return max(math.sqrt(x * x + y * y + z * z) - P[i, 16], P[i, 17] - y)
    elif t == 9:
        return grid_sdf(x, y, z, P, i, GB)
    elif t == 10:
        # an almond-shaped opening (the space between the eyelids): inside two circles, over a depth range
        dxu, dyu = x - P[i, 16], y - P[i, 17]
        du = math.sqrt(dxu * dxu + dyu * dyu) - P[i, 18]
        dxl, dyl = x - P[i, 19], y - P[i, 20]
        dl = math.sqrt(dxl * dxl + dyl * dyl) - P[i, 21]
        return max(max(du, dl), max(P[i, 22] - z, z - P[i, 23]))
    return 1e9


@njit(fastmath=True, cache=True)
def hash1(n):
    s = math.sin(n * 127.1) * 43758.5453
    return s - math.floor(s)


@njit(fastmath=True, cache=True)
def vnoise1(x):
    i = math.floor(x)
    f = x - i
    u = f * f * (3.0 - 2.0 * f)
    return hash1(i) * (1.0 - u) + hash1(i + 1.0) * u


@njit(fastmath=True, cache=True)
def hash3(x, y, z):
    s = math.sin(x * 127.1 + y * 311.7 + z * 74.7) * 43758.5453
    return s - math.floor(s)


@njit(fastmath=True, cache=True)
def vnoise3(x, y, z):
    ix, iy, iz = math.floor(x), math.floor(y), math.floor(z)
    fx, fy, fz = x - ix, y - iy, z - iz
    ux, uy, uz = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy), fz * fz * (3 - 2 * fz)
    a = hash3(ix, iy, iz)
    b = hash3(ix + 1, iy, iz)
    c = hash3(ix, iy + 1, iz)
    d = hash3(ix + 1, iy + 1, iz)
    e = hash3(ix, iy, iz + 1)
    f = hash3(ix + 1, iy, iz + 1)
    g = hash3(ix, iy + 1, iz + 1)
    h = hash3(ix + 1, iy + 1, iz + 1)
    k0 = a + (b - a) * ux
    k1 = c + (d - c) * ux
    k2 = e + (f - e) * ux
    k3 = g + (h - g) * ux
    l0 = k0 + (k1 - k0) * uy
    l1 = k2 + (k3 - k2) * uy
    return l0 + (l1 - l0) * uz


@njit(fastmath=True, cache=True)
def fbm3(x, y, z, octaves):
    s = 0.0
    a = 0.5
    for _ in range(octaves):
        s += a * vnoise3(x, y, z)
        x, y, z = x * 2.03 + 1.7, y * 2.01 + 9.2, z * 1.97 + 3.1
        a *= 0.5
    return s


# displacement types
D_NONE, D_KNIT, D_HAIR, D_SLEEVE, D_BODY, D_TREE = 0, 1, 2, 3, 4, 5


@njit(fastmath=True, cache=True)
def seg_closest(px, py, pz, ax, ay, az, bx, by, bz):
    vx, vy, vz = bx - ax, by - ay, bz - az
    L2 = vx * vx + vy * vy + vz * vz
    h = ((px - ax) * vx + (py - ay) * vy + (pz - az) * vz) / L2
    h = min(max(h, 0.0), 1.0)
    cx, cy, cz = ax + vx * h, ay + vy * h, az + vz * h
    return math.sqrt((px - cx) ** 2 + (py - cy) ** 2 + (pz - cz) ** 2), h


@njit(fastmath=True, cache=True)
def around_axis(px, py, pz, ax, ay, az, bx, by, bz):
    """Angle of p round the axis a->b (0 at the side facing up)."""
    vx, vy, vz = bx - ax, by - ay, bz - az
    L = math.sqrt(vx * vx + vy * vy + vz * vz)
    vx, vy, vz = vx / L, vy / L, vz / L
    wx, wy, wz = px - ax, py - ay, pz - az
    s = wx * vx + wy * vy + wz * vz
    rx, ry, rz = wx - s * vx, wy - s * vy, wz - s * vz
    ux, uy, uz = 0.0, 1.0, 0.0
    d0 = uy * vy
    ux, uy, uz = ux - d0 * vx, uy - d0 * vy, uz - d0 * vz
    ul = math.sqrt(ux * ux + uy * uy + uz * uz) + 1e-9
    ux, uy, uz = ux / ul, uy / ul, uz / ul
    tx, ty, tz = vy * uz - vz * uy, vz * ux - vx * uz, vx * uy - vy * ux
    return math.atan2(rx * tx + ry * ty + rz * tz, rx * ux + ry * uy + rz * uz), s


@njit(fastmath=True, cache=True)
def displace(dt, px, py, pz, mat, G, g, P, GB):
    if dt == 1:  # knitted ribs running up the body: across-coordinate = angle round the body's axis
        cx, cz, R0, period, depth = G[g, 7], G[g, 8], G[g, 9], G[g, 10], G[g, 11]
        th = math.atan2(px - cx, pz - cz)
        u = th * R0 / period
        rib = 0.5 + 0.5 * math.cos(6.2831853 * u)
        stitch = 0.5 + 0.5 * math.cos(6.2831853 * (py / (period * 0.9) + 0.5 * math.floor(u)))
        return -depth * (rib * 0.8 + 0.2 * rib * stitch)
    if dt == 3:  # sleeve ribs running along an arm: axis a->b in dparams
        ax, ay, az = G[g, 7], G[g, 8], G[g, 9]
        bx, by, bz = G[g, 10], G[g, 11], G[g, 12]
        period, depth = G[g, 13], G[g, 14]
        vx, vy, vz = bx - ax, by - ay, bz - az
        L = math.sqrt(vx * vx + vy * vy + vz * vz)
        vx, vy, vz = vx / L, vy / L, vz / L
        wx, wy, wz = px - ax, py - ay, pz - az
        s = wx * vx + wy * vy + wz * vz
        rx, ry, rz = wx - s * vx, wy - s * vy, wz - s * vz
        # a fixed reference direction perpendicular to the axis
        ux, uy, uz = 0.0, 1.0, 0.0
        d0 = ux * vx + uy * vy + uz * vz
        ux, uy, uz = ux - d0 * vx, uy - d0 * vy, uz - d0 * vz
        ul = math.sqrt(ux * ux + uy * uy + uz * uz) + 1e-9
        ux, uy, uz = ux / ul, uy / ul, uz / ul
        tx, ty, tz = vy * uz - vz * uy, vz * ux - vx * uz, vx * uy - vy * ux
        th = math.atan2(rx * tx + ry * ty + rz * tz, rx * ux + ry * uy + rz * uz)
        u = th * 0.045 / period
        rib = 0.5 + 0.5 * math.cos(6.2831853 * u)
        return -depth * rib
    if dt == 4:  # the jumper: chunky ribs up the body and along the sleeves, soft folds
        cx, cz, R0, period, depth = G[g, 7], G[g, 8], G[g, 9], G[g, 10], G[g, 11]
        best = 1e9
        th = 0.0
        along = 0.0
        # which part of the jumper is this: 0 body, 1 right sleeve, 2 left sleeve (a grid baked with the sculpt)
        part = -1
        if G[g, 32] > 0:
            s0 = int(G[g, 4])
            ox, oy, oz = px - P[s0, 4], py - P[s0, 5], pz - P[s0, 6]
            lx = P[s0, 7] * ox + P[s0, 8] * oy + P[s0, 9] * oz
            ly = P[s0, 10] * ox + P[s0, 11] * oy + P[s0, 12] * oz
            lz = P[s0, 13] * ox + P[s0, 14] * oy + P[s0, 15] * oz
            nx_, ny_, nz_ = int(P[s0, 17]), int(P[s0, 18]), int(P[s0, 19])
            vs = P[s0, 20]
            ix = min(max(int(lx / vs + 0.5), 0), nx_ - 1)
            iy = min(max(int(ly / vs + 0.5), 0), ny_ - 1)
            iz = min(max(int(lz / vs + 0.5), 0), nz_ - 1)
            part = int(GB[int(G[g, 32]) + (ix * ny_ + iy) * nz_ + iz] + 0.5)
        cuff = 1.0
        for arm in range(2):
            if part == 0 or (part > 0 and part != arm + 1):
                continue
            base = 12 + 9 * arm
            for sgi in range(2):
                o = base + 3 * sgi
                dd, hh = seg_closest(px, py, pz, G[g, o], G[g, o + 1], G[g, o + 2], G[g, o + 3], G[g, o + 4],
                                     G[g, o + 5])
                if dd < best:
                    best = dd
                    th, along = around_axis(px, py, pz, G[g, o], G[g, o + 1], G[g, o + 2], G[g, o + 3],
                                            G[g, o + 4], G[g, o + 5])
                    cuff = 1.0
                    if sgi == 1:  # no ribs across the end of the cuff, where the hand comes out
                        L = math.sqrt((G[g, o + 3] - G[g, o]) ** 2 + (G[g, o + 4] - G[g, o + 1]) ** 2 +
                                      (G[g, o + 5] - G[g, o + 2]) ** 2)
                        cuff = min(max((L + 0.002 - along) / 0.012, 0.0), 1.0)
        if (part > 0 and best < 1e8) or (part < 0 and best < G[g, 30] and py < G[g, 31]):
            u = th * 0.045 / period
        else:
            u = math.atan2(px - cx, pz - cz) * R0 / period
        rib = 0.5 + 0.5 * math.cos(6.2831853 * u)
        folds = fbm3(px * 9.0, py * 5.0, pz * 9.0, 3) - 0.5
        return -depth * rib * cuff + 0.0018 * folds
    if dt == 5:  # fir branches: a ragged, layered outline instead of a smooth cone
        amp, freq = G[g, 7], G[g, 8]
        if mat < 0 or mat != G[g, 9]:
            return 0.0
        n = fbm3(px * freq, py * freq * 1.3, pz * freq, 4) - 0.5
        tiers = abs(math.sin(py * freq * 2.2)) - 0.5
        return amp * (n * 1.4 + 0.35 * tiers)
    if dt == 2:  # hair: fine strands - grooves across the direction the hair falls
        hx, hy, hz, R0 = G[g, 7], G[g, 8], G[g, 9], G[g, 10]
        th = math.atan2(px - hx, pz - hz)
        top = min(max((py - hy - G[g, 11]) / 0.05, 0.0), 1.0)
        u = th * R0 * (1.0 - top) + (pz - hz) * top
        n = vnoise1(u / 0.0022) * 0.6 + vnoise1(u / 0.0061 + 7.3) * 0.4
        return -G[g, 12] * n
    return 0.0


@njit(fastmath=True, cache=True)
def scene_map(px, py, pz, P, G, GB):
    dbest = 1e9
    mbest = -1.0
    for g in range(G.shape[0]):
        cx, cy, cz, br = G[g, 0], G[g, 1], G[g, 2], G[g, 3]
        dx, dy, dz = px - cx, py - cy, pz - cz
        db = math.sqrt(dx * dx + dy * dy + dz * dz) - br
        if db > dbest:
            continue
        if db > 0.02:
            dbest = db
            mbest = -1.0
            continue
        s, e = int(G[g, 4]), int(G[g, 5])
        dg = 1e9
        mg = -1.0
        for i in range(s, e):
            ox, oy, oz = px - P[i, 4], py - P[i, 5], pz - P[i, 6]
            lx = P[i, 7] * ox + P[i, 8] * oy + P[i, 9] * oz
            ly = P[i, 10] * ox + P[i, 11] * oy + P[i, 12] * oz
            lz = P[i, 13] * ox + P[i, 14] * oy + P[i, 15] * oz
            di = prim_sdf(int(P[i, 0]), lx, ly, lz, P, i, GB)
            op = int(P[i, 1])
            k = P[i, 2]
            if op == 0:
                if di < dg:
                    dg = di
                    mg = P[i, 3]
            elif op == 1:
                h = 0.5 + 0.5 * (dg - di) / k
                h = min(max(h, 0.0), 1.0)
                if di < dg:
                    mg = P[i, 3]
                dg = dg * (1.0 - h) + di * h - k * h * (1.0 - h)
            elif op == 2:
                h = 0.5 - 0.5 * (dg + di) / k
                h = min(max(h, 0.0), 1.0)
                dg = dg * (1.0 - h) - di * h + k * h * (1.0 - h)
            elif op == 3:
                h = 0.5 - 0.5 * (di - dg) / k
                h = min(max(h, 0.0), 1.0)
                dg = dg * (1.0 - h) + di * h + k * h * (1.0 - h)
            elif op == 4:
                # hard subtract, and the carved surface takes this primitive's material
                if -di > dg:
                    dg = -di
                    if P[i, 3] >= 0:
                        mg = P[i, 3]
        dt = int(G[g, 6])
        if dt != 0:
            dg += displace(dt, px, py, pz, mg, G, g, P, GB)
        if dg < dbest:
            dbest = dg
            mbest = mg
    return dbest, mbest


@njit(fastmath=True, cache=True)
def calc_normal(px, py, pz, P, G, GB, e):
    d1, _ = scene_map(px + e, py - e, pz - e, P, G, GB)
    d2, _ = scene_map(px - e, py - e, pz + e, P, G, GB)
    d3, _ = scene_map(px - e, py + e, pz - e, P, G, GB)
    d4, _ = scene_map(px + e, py + e, pz + e, P, G, GB)
    nx = d1 - d2 - d3 + d4
    ny = -d1 - d2 + d3 + d4
    nz = -d1 + d2 - d3 + d4
    L = math.sqrt(nx * nx + ny * ny + nz * nz) + 1e-12
    return nx / L, ny / L, nz / L


@njit(fastmath=True, cache=True)
def march(ox, oy, oz, dx, dy, dz, tmin, tmax, P, G, GB, maxs, eps0, eps1):
    t = tmin
    for _ in range(maxs):
        d, m = scene_map(ox + dx * t, oy + dy * t, oz + dz * t, P, G, GB)
        if d < eps0 + eps1 * t:
            return t, m
        t += d * 0.8
        if t > tmax:
            break
    return -1.0, -1.0


@njit(fastmath=True, cache=True)
def soft_shadow(px, py, pz, lx, ly, lz, tmax, k, P, G, GB):
    """Soft shadow towards a light. Starts a little way off the surface so smooth skin doesn't shadow itself."""
    res = 1.0
    t = 0.010
    for _ in range(80):
        h, _m = scene_map(px + lx * t, py + ly * t, pz + lz * t, P, G, GB)
        res = min(res, k * h / t)
        if res < 0.002:
            break
        t += min(max(h * 0.9, 0.0025), 0.2)
        if t > tmax:
            break
    res = min(max(res, 0.0), 1.0)
    return res * res * (3.0 - 2.0 * res)


@njit(fastmath=True, cache=True)
def ambient_occlusion(px, py, pz, nx, ny, nz, P, G, GB, scale):
    occ = 0.0
    sca = 1.0
    for i in range(6):
        h = scale * (0.01 + 0.04 * i)
        d, _ = scene_map(px + nx * h, py + ny * h, pz + nz * h, P, G, GB)
        occ += (h - d) * sca
        sca *= 0.75
    return min(max(1.0 - 2.2 * occ / scale, 0.0), 1.0)


# ---------------------------------------------------------------------------
# Materials and shading
# ---------------------------------------------------------------------------
# material table columns
MA_R, MA_G, MA_B, MA_SPEC, MA_SHIN, MA_REFL, MA_EMIT, MA_WRAP, MA_TEX = range(9)
# texture ids (MA_TEX) - how the surface pattern is worked out
T_NONE, T_SKIN, T_LID, T_EYE, T_HAIR, T_KNIT, T_MARBLE, T_WOODGRAIN, T_MEAT, T_STEEL, T_WINDOW, T_TRAY, \
    T_NEEDLES, T_WAX, T_BONE = range(15)


@njit(fastmath=True, cache=True)
def head_local(px, py, pz, SP):
    """World point -> head coordinates (x across, y up, z out of the face)."""
    ox, oy, oz = px - SP[0], py - SP[1], pz - SP[2]
    # SP[3:12] is the head rotation (local -> world), row-major; its transpose takes world -> local
    lx = SP[3] * ox + SP[6] * oy + SP[9] * oz
    ly = SP[4] * ox + SP[7] * oy + SP[10] * oz
    lz = SP[5] * ox + SP[8] * oy + SP[11] * oz
    return lx, ly, lz


@njit(fastmath=True, cache=True)
def smoothstep(a, b, x):
    t = min(max((x - a) / (b - a), 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


@njit(fastmath=True, cache=True)
def brow_mask(lx, ly, lz, SP):
    """Eyebrows, drawn on the skin in head coordinates: an arch over each eye, thick near the nose, tapering out."""
    ax = abs(lx)
    x0, x1 = SP[40], SP[41]  # inner and outer end (distance from the midline)
    if ax < x0 - 0.004 or ax > x1 + 0.004 or lz < -0.01 or ly < 0.004 or ly > 0.035:
        return 0.0
    u = (ax - x0) / (x1 - x0)  # 0 at the inner end, 1 at the tail
    arch = SP[42] + SP[43] * math.sin(min(max(u, 0.0), 1.0) * 2.4) - SP[44] * max(u - 0.7, 0.0)
    thick = SP[45] * (1.0 - 0.65 * u) * (0.55 + 0.45 * smoothstep(-0.10, 0.22, u))  # a rounded head, a fine tail
    d = abs(ly - arch) / max(thick, 1e-4)
    m = 1.0 - smoothstep(0.55, 1.0, d)
    m *= smoothstep(-0.12, 0.08, u) * (1.0 - smoothstep(0.95, 1.12, u))
    # hairs: fine streaks, slanted up and outwards
    streak = vnoise1((ax * 900.0 - ly * 520.0)) * 0.5 + 0.5
    return m * (0.55 + 0.45 * streak)


@njit(fastmath=True, cache=True)
def lip_curves(u, SP):
    """Heights of the lip outlines at u = |x| / half mouth width: top of the upper lip (with the cupid's
    bow), the parting between the lips, the bottom of the lower lip."""
    yc = SP[101]
    top = SP[102] + SP[103] * math.exp(-((u - 0.21) / 0.09) ** 2) + (yc - SP[102]) * u ** 1.8
    stom = SP[104] + (yc - SP[104]) * u ** 2.2
    bot = SP[105] + (yc - SP[105]) * u ** 2.0
    return top, stom, bot


@njit(fastmath=True, cache=True)
def lip_mask(lx, ly, lz, SP):
    W = SP[100]
    if W <= 0.0 or lz < 0.005 or abs(lx) > W + 0.001 or ly > SP[102] + 0.003 or ly < SP[105] - 0.004:
        return 0.0, 0.0
    u = min(abs(lx) / W, 1.0)
    top, stom, bot = lip_curves(u, SP)
    edge = 0.00025
    m = smoothstep(-edge, edge, top - ly) * smoothstep(-edge, edge, ly - bot)
    m *= 1.0 - smoothstep(0.93, 1.0, abs(lx) / W)
    part = (1.0 - smoothstep(0.0002, 0.0009, abs(ly - stom))) * (1.0 - smoothstep(0.96, 1.08, abs(lx) / W))
    return m, part


@njit(fastmath=True, cache=True)
def texture(tex, px, py, pz, nx, ny, nz, mat, M, SP):
    r, g, b = M[mat, 0], M[mat, 1], M[mat, 2]
    spec_mul = 1.0
    if tex == 1 or tex == 2:  # skin: brows, lips, lash lines, a little colour in the cheeks
        lx, ly, lz = head_local(px, py, pz, SP)
        if lx * lx + ly * ly + lz * lz > 0.03:  # not on the face: plain skin (hands)
            return r, g, b, spec_mul
        # the hairline: fine short hairs darkening the skin just below the edge of the hair (SP[110:114])
        if SP[110] > 0.0 and lz > -0.04:
            ax = abs(lx)
            if ax < 0.05:
                yh = SP[110] - SP[111] * (ax / 0.05) ** 2
            else:
                yh = SP[112] - SP[113] * min(max((ax - 0.05) / 0.025, 0.0), 1.0)
            dy = yh - ly
            if dy > -0.001 and dy < 0.007:
                fine = (1.0 - smoothstep(0.0, 0.007, dy)) * (0.45 + 0.55 * vnoise1(ax * 1500.0 + ly * 200.0))
                k = 1.0 - 0.55 * fine
                r, g, b = r * k * (1.0 - 0.10 * fine), g * k * (1.0 - 0.14 * fine), b * k * (1.0 - 0.16 * fine)
        bm = brow_mask(lx, ly, lz, SP)
        if bm > 0.0:
            k = 1.0 - 0.80 * bm
            r, g, b = r * k * 0.80, g * k * 0.72, b * k * 0.68
        cheek = math.exp(-((abs(lx) - 0.040) ** 2 + (ly + 0.030) ** 2) / (2 * 0.016 ** 2)) * (lz > 0.0)
        r, g, b = r * (1 + 0.05 * cheek), g * (1 - 0.05 * cheek), b * (1 - 0.05 * cheek)
        lm, part = lip_mask(lx, ly, lz, SP)
        if lm > 0.0:
            r = r + (SP[107] - r) * lm
            g = g + (SP[108] - g) * lm
            b = b + (SP[109] - b) * lm
            spec_mul = 1.0 + 1.2 * lm
        if part > 0.0:
            k = 1.0 - 0.8 * part
            r, g, b = r * k, g * k, b * k
        if SP[114] > 0.0:  # a modelled face (MakeHuman): its lids and lashes are geometry, not paint
            return r, g, b, spec_mul
        # eyes: the dark line of the upper lashes, softer lower lashes, the shadowed rims
        for sx in (-1.0, 1.0):
            ex = (lx - sx * SP[29]) * sx  # across the eye, positive towards the outer corner
            ey = ly
            if abs(ex) > 0.024 or abs(ey) > 0.014 or lz < 0.0:
                continue
            du = math.sqrt((ex - SP[23]) ** 2 + (ey - SP[24]) ** 2) - SP[25]
            dl = math.sqrt((ex - SP[26]) ** 2 + (ey - SP[27]) ** 2) - SP[28]
            lens = max(du, dl)
            wing = smoothstep(0.004, 0.017, ex)  # the lash line thickens towards the outer corner
            if du > -0.0002 and dl < 0.0035:
                lash = 1.0 - smoothstep(0.0006 + 0.0010 * wing, 0.0016 + 0.0016 * wing, du)
                lash *= 1.0 - smoothstep(0.015, 0.0185, abs(ex))
                k = 1.0 - 0.92 * lash
                r, g, b = r * k, g * k, b * k
            if dl > -0.0002 and du < 0.0 and dl < 0.0009:
                low = (1.0 - smoothstep(0.0002, 0.0009, dl)) * 0.45 * smoothstep(-0.012, 0.004, ex)
                k = 1.0 - low
                r, g, b = r * k, g * k, b * k
            if lens < 0.0:
                r, g, b = r * 0.55, g * 0.42, b * 0.40  # the moist rim of the lids
            # the fold of the upper lid, a soft line above the lashes
            fold = math.exp(-((du - 0.0068 + 0.0012 * (ex / 0.016) ** 2) / 0.0007) ** 2)
            fold *= smoothstep(-0.013, -0.006, ex) * (1.0 - smoothstep(0.013, 0.019, ex)) * (dl < 0.012)
            k = 1.0 - 0.30 * fold
            r, g, b = r * k, g * k * 0.98, b * k * 0.97
    elif tex == 3:  # eye: white, iris, pupil, a dark ring round the iris
        for e in range(2):
            ex, ey, ez = SP[12 + 3 * e], SP[13 + 3 * e], SP[14 + 3 * e]
            wx, wy, wz = px - ex, py - ey, pz - ez
            dist = math.sqrt(wx * wx + wy * wy + wz * wz)
            if dist < 0.02:
                c = (wx * SP[18] + wy * SP[19] + wz * SP[20]) / dist
                ang = math.acos(min(max(c, -1.0), 1.0))
                ir, pr = SP[21], SP[22]
                if ang < pr:
                    r, g, b = 0.012, 0.010, 0.010
                    spec_mul = 1.6
                elif ang < ir:
                    u = (ang - pr) / (ir - pr)
                    # radial fibres in the iris
                    fx = wx - c * dist * SP[18]
                    fy = wy - c * dist * SP[19]
                    fz = wz - c * dist * SP[20]
                    th = math.atan2(fy, fx + fz * 0.7)
                    fib = vnoise1(th * 18.0) * 0.5 + vnoise1(th * 43.0 + 3.0) * 0.5
                    base_r, base_g, base_b = 0.30, 0.20, 0.11  # warm hazel-brown
                    k = (0.55 + 0.45 * fib) * (0.75 + 0.35 * u)
                    ring = smoothstep(0.78, 1.0, u)
                    k *= 1.0 - 0.75 * ring
                    r, g, b = base_r * k, base_g * k, base_b * k
                    spec_mul = 1.4
                else:
                    # the white of the eye, a touch darker towards the corners and under the lids
                    shade = 0.82 + 0.18 * smoothstep(-0.2, 0.7, c)
                    r, g, b = r * shade, g * shade, b * shade
    elif tex == 4:  # hair: dark, with lighter and darker strands
        s = vnoise3(px * 900.0, py * 60.0, pz * 900.0)
        k = 0.75 + 0.5 * s
        r, g, b = r * k, g * k, b * k
    elif tex == 5:  # knit: slight variation in the wool
        s = vnoise3(px * 400.0, py * 400.0, pz * 400.0)
        k = 0.93 + 0.1 * s
        r, g, b = r * k, g * k, b * k
    elif tex == 6:  # marble: soft grey veins
        v = fbm3(px * 7.0, py * 7.0 + 3.0, pz * 7.0, 5)
        vein = 1.0 - smoothstep(0.0, 0.035, abs(v - 0.5))
        vein2 = 1.0 - smoothstep(0.0, 0.012, abs(fbm3(px * 21.0 + 5.0, py * 21.0, pz * 21.0, 4) - 0.5))
        k = 1.0 - 0.16 * vein - 0.08 * vein2
        r, g, b = r * k, g * k, b * k
    elif tex == 7:  # oak: grain along x (in the board's own direction, SP[46:49])
        u = px * SP[46] + py * SP[47] + pz * SP[48]
        w = px * SP[48] - pz * SP[46]
        grain = 0.5 + 0.5 * math.sin(w * 900.0 + 6.0 * fbm3(u * 6.0, py * 60.0, w * 40.0, 3))
        k = 0.86 + 0.14 * grain
        r, g, b = r * k, g * k, b * k
    elif tex == 8:  # glazed meat: sticky glaze, charred edges from the grill
        ch = fbm3(px * 60.0, py * 60.0, pz * 60.0, 4)
        char = smoothstep(0.55, 0.72, ch)
        k = 1.0 - 0.75 * char
        r, g, b = r * k, g * k, b * k
        spec_mul = 1.0 - 0.6 * char
    elif tex == 9:  # brushed steel: fine streaks along the blade
        s = vnoise1((py * 3000.0 + px * 40.0)) * 0.5 + vnoise1(py * 700.0 + 3.1) * 0.5
        k = 0.9 + 0.15 * s
        r, g, b = r * k, g * k, b * k
    elif tex == 10:  # the view out of the window: pale winter sky, snow, a far treeline and a few near firs
        u = px
        v = py
        dark = 0.0
        # distant treeline, soft and pale
        line = 1.12 + 0.10 * fbm3(u * 3.0, 0.0, 0.0, 4) + 0.05 * math.sin(u * 17.0)
        if v < line:
            dark = 0.35 * smoothstep(0.96, 1.02, v)
        for t in range(6):
            cx = -2.1 + t * 0.34 + 0.1 * math.sin(t * 5.3)
            hgt = 1.55 + 0.45 * hash1(t * 3.7)
            base = 0.98
            if v < hgt and v > base:
                h = (hgt - v) / (hgt - base)
                w = 0.02 + h * 0.16 * (0.75 + 0.5 * fbm3(v * 18.0 + t, u * 9.0, 0.0, 3))
                if abs(u - cx) < w:
                    snow = smoothstep(0.62, 0.8, fbm3(u * 40.0, v * 25.0, t, 3))
                    dark = max(dark, 0.88 * (1.0 - 0.8 * snow))
        ground = smoothstep(1.00, 0.94, v)
        sky = 1.0 - 0.10 * smoothstep(1.0, 2.3, v)
        k = sky * (1.0 - dark)
        k = k * (1.0 - 0.04 * ground)
        r, g, b = r * k, g * k, b * k
    elif tex == 11:  # weathered tray: grain along its length
        grain = 0.5 + 0.5 * math.sin(pz * 700.0 + 4.0 * fbm3(px * 12.0, py * 30.0, pz * 3.0, 3))
        k = 0.8 + 0.2 * grain
        r, g, b = r * k, g * k, b * k
    elif tex == 12:  # pine needles: lots of tiny variation
        s = vnoise3(px * 300.0, py * 300.0, pz * 300.0)
        k = 0.6 + 0.8 * s
        r, g, b = r * k, g * k, b * k
    elif tex == 13:  # wax: glows warmer near the flame
        pass
    return r, g, b, spec_mul


@njit(fastmath=True, cache=True)
def hair_tangent(px, py, pz, nx, ny, nz, SP):
    """Which way the hair runs here: sideways from the parting near the crown, then straight down."""
    lx, ly, lz = head_local(px, py, pz, SP)
    a = smoothstep(0.02, 0.11, ly) * 2.5
    sx = 1.0 if lx >= 0 else -1.0
    gx, gy, gz = sx * a, -1.0, -0.15 * (lz < 0)
    # to world
    wx = SP[3] * gx + SP[4] * gy + SP[5] * gz
    wy = SP[6] * gx + SP[7] * gy + SP[8] * gz
    wz = SP[9] * gx + SP[10] * gy + SP[11] * gz
    d = wx * nx + wy * ny + wz * nz
    wx, wy, wz = wx - d * nx, wy - d * ny, wz - d * nz
    L = math.sqrt(wx * wx + wy * wy + wz * wz) + 1e-9
    return wx / L, wy / L, wz / L


# shadow map table columns
SM_OFF, SM_NU, SM_NV, SM_O, SM_U, SM_V, SM_W, SM_EU, SM_EV, SM_TAN, SM_BIAS = 0, 1, 2, 3, 6, 9, 12, 15, 16, 17, 18


@njit(fastmath=True, cache=True)
def sm_fetch(SM, off, nu, nv, fu, fv):
    iu = int(fu)
    iv = int(fv)
    if iu < 0 or iv < 0 or iu >= nu or iv >= nv:
        return 1e9
    return SM[off + iv * nu + iu]


@njit(fastmath=True, cache=True)
def shadow_map_light(px, py, pz, ndl, SM, SMP, mi):
    """Soft shadow from a depth map rendered from the light (PCSS): the further the surface is from whatever
    blocks the light, the softer the shadow's edge. Returns -1 if the point is outside this map."""
    off, nu, nv = int(SMP[mi, 0]), int(SMP[mi, 1]), int(SMP[mi, 2])
    ox, oy, oz = px - SMP[mi, 3], py - SMP[mi, 4], pz - SMP[mi, 5]
    u = ox * SMP[mi, 6] + oy * SMP[mi, 7] + oz * SMP[mi, 8]
    v = ox * SMP[mi, 9] + oy * SMP[mi, 10] + oz * SMP[mi, 11]
    w = ox * SMP[mi, 12] + oy * SMP[mi, 13] + oz * SMP[mi, 14]
    eu, ev = SMP[mi, 15], SMP[mi, 16]
    tu = eu / nu
    fu = (u + 0.5 * eu) / tu
    fv = (v + 0.5 * ev) / tu
    if fu < 2 or fv < 2 or fu > nu - 3 or fv > nv - 3:
        return -1.0
    tanr = SMP[mi, 17]
    sn = math.sqrt(max(1.0 - ndl * ndl, 0.0))
    bias = SMP[mi, 18] + tu * 1.5 + 0.0012 * min(sn / max(ndl, 0.05), 6.0)
    # 1. look for blockers nearby and how far above the surface they are
    search = 0.12 * tanr + tu * 2.0
    step = search / 3.0 / tu
    acc, cnt = 0.0, 0
    for a in range(-3, 4):
        for b in range(-3, 4):
            d = sm_fetch(SM, off, nu, nv, fu + a * step, fv + b * step)
            if d < w - bias:
                acc += d
                cnt += 1
    if cnt == 0:
        return 1.0
    avg = acc / cnt
    pen = (w - avg) * tanr
    pen = min(max(pen, tu * 1.2), search)
    # 2. average the light getting through over the penumbra
    st = pen / 2.5 / tu
    lit, n = 0.0, 0
    for a in range(-3, 4):
        for b in range(-3, 4):
            ja = a + 0.5 * hash3(fu, fv, a * 7.0 + b) - 0.25
            jb = b + 0.5 * hash3(fv, fu, b * 5.0 + a) - 0.25
            d = sm_fetch(SM, off, nu, nv, fu + ja * st, fv + jb * st)
            if d >= w - bias:
                lit += 1.0
            n += 1
    return lit / n


@njit(fastmath=True, cache=True)
def direct_light(px, py, pz, nx, ny, nz, vx, vy, vz, r, g, b, spec, shin, wrap, is_hair, Lt, P, G, GB, SP,
                 shadows, SM, SMP):
    cr, cg, cb = 0.0, 0.0, 0.0
    tx, ty, tz = 0.0, 0.0, 0.0
    if is_hair:
        tx, ty, tz = hair_tangent(px, py, pz, nx, ny, nz, SP)
    for li in range(Lt.shape[0]):
        typ = int(Lt[li, 0])
        if typ == 0:
            lx, ly, lz = Lt[li, 1], Lt[li, 2], Lt[li, 3]
            att = 1.0
            dist = 20.0
        else:
            lx, ly, lz = Lt[li, 1] - px, Lt[li, 2] - py, Lt[li, 3] - pz
            dist = math.sqrt(lx * lx + ly * ly + lz * lz) + 1e-9
            lx, ly, lz = lx / dist, ly / dist, lz / dist
            rng = Lt[li, 9]
            att = 1.0 / (1.0 + (dist / rng) * (dist / rng))
        ndl = nx * lx + ny * ly + nz * lz
        diff = max((ndl + wrap) / (1.0 + wrap), 0.0)
        if diff <= 0.0 and spec <= 0.0:
            continue
        sh = 1.0
        if shadows and Lt[li, 7] > 0 and (ndl > -wrap) and SP[66] == 0:
            if Lt[li, 7] == 2:
                sh = -1.0
                for mk in range(int(Lt[li, 11])):
                    sh = shadow_map_light(px, py, pz, max(ndl, 0.0), SM, SMP, int(Lt[li, 10]) + mk)
                    if sh >= 0.0:
                        break
                if sh < 0.0:
                    sh = 1.0
            else:
                sh = soft_shadow(px + nx * 0.0015, py + ny * 0.0015, pz + nz * 0.0015, lx, ly, lz,
                                 min(dist, 6.0), Lt[li, 8], P, G, GB)
        hx, hy, hz = lx + vx, ly + vy, lz + vz
        hl = math.sqrt(hx * hx + hy * hy + hz * hz) + 1e-9
        hx, hy, hz = hx / hl, hy / hl, hz / hl
        if is_hair:
            th = tx * hx + ty * hy + tz * hz
            sp = spec * (math.sqrt(max(1.0 - th * th, 0.0)) ** shin) * 0.6
        else:
            sp = spec * (shin + 8.0) / 25.0 * (max(nx * hx + ny * hy + nz * hz, 0.0) ** shin) * (ndl > 0)
        k = sh * att
        cr += (r * diff + sp) * Lt[li, 4] * k
        cg += (g * diff + sp) * Lt[li, 5] * k
        cb += (b * diff + sp) * Lt[li, 6] * k
    return cr, cg, cb


@njit(fastmath=True, cache=True)
def shade_basic(px, py, pz, nx, ny, nz, vx, vy, vz, mat, P, G, GB, M, Lt, SP, shadows, SM, SMP):
    """Colour of the surface at p, seen from direction v (pointing back to the eye), without mirror bounce."""
    mi = int(mat)
    if mi < 0:
        return 0.5, 0.5, 0.5
    tex = int(M[mi, MA_TEX])
    r, g, b, spec_mul = texture(tex, px, py, pz, nx, ny, nz, mi, M, SP)
    emit = M[mi, MA_EMIT]
    if emit > 0.0:
        return r * emit, g * emit, b * emit
    spec = M[mi, MA_SPEC] * spec_mul
    shin = M[mi, MA_SHIN]
    wrap = M[mi, MA_WRAP]
    ao = ambient_occlusion(px, py, pz, nx, ny, nz, P, G, GB, SP[67] if SP[67] > 0 else 1.0) if (shadows and SP[65] == 0) else 0.85
    # room fill: brighter from above, a little bounce from below
    hemi = 0.55 + 0.45 * ny
    amb = SP[60] * ao * hemi + SP[61] * ao
    cr, cg, cb = r * amb * SP[62], g * amb * SP[63], b * amb * SP[64]
    dr, dg, db = direct_light(px, py, pz, nx, ny, nz, vx, vy, vz, r, g, b, spec, shin, wrap, tex == 4,
                              Lt, P, G, GB, SP, shadows, SM, SMP)
    return cr + dr, cg + dg, cb + db


@njit(fastmath=True, cache=True)
def shade(px, py, pz, nx, ny, nz, vx, vy, vz, mat, P, G, GB, M, Lt, SP, SM, SMP):
    cr, cg, cb = shade_basic(px, py, pz, nx, ny, nz, vx, vy, vz, mat, P, G, GB, M, Lt, SP, True, SM, SMP)
    mi = int(mat)
    if mi < 0:
        return cr, cg, cb
    refl = M[mi, MA_REFL]
    if refl > 0.0:
        # mirror bounce (marble, steel, glaze)
        d = vx * nx + vy * ny + vz * nz
        rx, ry, rz = 2.0 * d * nx - vx, 2.0 * d * ny - vy, 2.0 * d * nz - vz
        fres = refl + (1.0 - refl) * (1.0 - max(d, 0.0)) ** 5 * 0.6
        t, m2 = march(px + nx * 0.002, py + ny * 0.002, pz + nz * 0.002, rx, ry, rz, 0.002, 8.0, P, G, GB,
                      110, 0.0004, 0.001)
        if t > 0:
            qx, qy, qz = px + rx * t, py + ry * t, pz + rz * t
            n2x, n2y, n2z = calc_normal(qx, qy, qz, P, G, GB, 0.0006)
            er, eg, eb = shade_basic(qx, qy, qz, n2x, n2y, n2z, -rx, -ry, -rz, m2, P, G, GB, M, Lt, SP, False, SM, SMP)
        else:
            er, eg, eb = 0.8, 0.8, 0.8
        cr = cr * (1.0 - fres) + er * fres
        cg = cg * (1.0 - fres) + eg * fres
        cb = cb * (1.0 - fres) + eb * fres
    return cr, cg, cb


@njit(fastmath=True, cache=True)
def glass_overlay(ox, oy, oz, dx, dy, dz, thit, SP):
    """Clear glass pendant shades (open cylinders): returns how much to keep of what's behind, a reflection
    to add on top, and how strongly glass was seen here (for the drawing's outlines)."""
    keep, add, seen = 1.0, 0.0, 0.0
    n = int(SP[80])
    for k in range(n):
        base = 81 + 5 * k
        cx, cz, y0, y1, rad = SP[base], SP[base + 1], SP[base + 2], SP[base + 3], SP[base + 4]
        a = dx * dx + dz * dz
        if a < 1e-9:
            continue
        bx, bz = ox - cx, oz - cz
        bb = 2.0 * (bx * dx + bz * dz)
        cc = bx * bx + bz * bz - rad * rad
        disc = bb * bb - 4.0 * a * cc
        if disc <= 0.0:
            continue
        sq = math.sqrt(disc)
        for sgn in (-1.0, 1.0):
            t = (-bb + sgn * sq) / (2.0 * a)
            if t <= 0.0 or (thit > 0.0 and t > thit):
                continue
            yy = oy + dy * t
            if yy < y0 or yy > y1:
                continue
            hx, hz = (ox + dx * t - cx) / rad, (oz + dz * t - cz) / rad
            cosv = abs(hx * dx + hz * dz) / math.sqrt(a)
            fres = 0.04 + 0.96 * (1.0 - cosv) ** 5
            edge = (1.0 - cosv) ** 3
            keep *= 0.93 - 0.35 * edge
            add += fres * 0.9 + 0.08
            # the thick rolled rim at the bottom of the shade
            if yy - y0 < 0.006:
                keep *= 0.5
                seen = max(seen, 1.0)
            seen = max(seen, edge)
    return keep, add, seen


@njit(parallel=True, fastmath=True, cache=True)
def render(W, H, cam, P, G, GB, M, Lt, SP, SM, SMP, rgb, depth, normal, matid, pos, glass, rows0, rows1,
           cols0, cols1):
    ox, oy, oz = cam[0], cam[1], cam[2]
    fx, fy, fz = cam[3], cam[4], cam[5]
    rx, ry, rz = cam[6], cam[7], cam[8]
    ux, uy, uz = cam[9], cam[10], cam[11]
    th, aspect = cam[12], cam[13]
    for j in prange(rows0, rows1):
        for i in range(cols0, cols1):
            sx = (2.0 * (i + 0.5) / W - 1.0) * th * aspect
            sy = (1.0 - 2.0 * (j + 0.5) / H) * th
            dx = fx + sx * rx + sy * ux
            dy = fy + sx * ry + sy * uy
            dz = fz + sx * rz + sy * uz
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            dx, dy, dz = dx / L, dy / L, dz / L
            t, m = march(ox, oy, oz, dx, dy, dz, 0.05, 40.0, P, G, GB, 400, 0.00008, 0.00022)
            if t > 0:
                px, py, pz = ox + dx * t, oy + dy * t, oz + dz * t
                nx, ny, nz = calc_normal(px, py, pz, P, G, GB, max(0.0005, 0.0002 * t))
                cr, cg, cb = shade(px, py, pz, nx, ny, nz, -dx, -dy, -dz, m, P, G, GB, M, Lt, SP, SM, SMP)
                depth[j, i] = t
                normal[j, i, 0], normal[j, i, 1], normal[j, i, 2] = nx, ny, nz
                pos[j, i, 0], pos[j, i, 1], pos[j, i, 2] = px, py, pz
                matid[j, i] = int(m)
            else:
                cr, cg, cb = 0.9, 0.9, 0.9
                depth[j, i] = -1.0
                matid[j, i] = -1
            keep, add, seen = glass_overlay(ox, oy, oz, dx, dy, dz, t, SP)
            rgb[j, i, 0] = cr * keep + add * 0.9
            rgb[j, i, 1] = cg * keep + add * 0.9
            rgb[j, i, 2] = cb * keep + add * 0.88
            glass[j, i] = seen


def camera(pos, target, vfov_deg, aspect, roll=0.0):
    pos, target = np.asarray(pos, float), np.asarray(target, float)
    f = target - pos
    f /= np.linalg.norm(f)
    r = np.cross(f, [0, 1.0, 0])
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    if roll:
        c, s = np.cos(np.radians(roll)), np.sin(np.radians(roll))
        r, u = r * c + u * s, u * c - r * s
    return np.concatenate([pos, f, r, u, [np.tan(np.radians(vfov_deg) / 2), aspect]])


def render_image(W, H, cam, P, G, M, Lt, SP, GB=None, SM=None, SMP=None, bands=8, verbose=True, crop=None):
    import time
    rgb = np.zeros((H, W, 3), np.float32)
    depth = np.zeros((H, W), np.float32)
    normal = np.zeros((H, W, 3), np.float32)
    matid = np.zeros((H, W), np.int16)
    pos = np.zeros((H, W, 3), np.float32)
    glass = np.zeros((H, W), np.float32)
    if GB is None:
        GB = np.zeros(8, np.float32)
    if SM is None:
        SM = np.zeros(8, np.float32)
        SMP = np.zeros((1, 19))
    t0 = time.time()
    x0, y0, x1, y1 = crop if crop is not None else (0, 0, W, H)
    step = int(np.ceil((y1 - y0) / bands))
    for b0 in range(y0, y1, step):
        render(W, H, cam, P, G, GB, M, Lt, SP, SM, SMP, rgb, depth, normal, matid, pos, glass, b0,
               min(y1, b0 + step), x0, x1)
        if verbose:
            print(f'  rows {min(y1, b0 + step)}/{y1}  {time.time() - t0:.0f}s', flush=True)
    return dict(rgb=rgb, depth=depth, normal=normal, mat=matid, pos=pos, glass=glass)


def tonemap(rgb, exposure=1.0):
    x = np.maximum(rgb * exposure, 0)
    y = (x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14)
    return np.clip(y, 0, 1) ** (1 / 2.2)



@njit(parallel=True, fastmath=True, cache=True)
def depth_map(nu, nv, o, U, V, Wd, eu, ev, P, G, GB, out):
    tu = eu / nu
    for j in prange(nv):
        for i in range(nu):
            u = -0.5 * eu + (i + 0.5) * tu
            v = -0.5 * ev + (j + 0.5) * tu
            sx = o[0] + U[0] * u + V[0] * v
            sy = o[1] + U[1] * u + V[1] * v
            sz = o[2] + U[2] * u + V[2] * v
            t, m = march(sx, sy, sz, Wd[0], Wd[1], Wd[2], 0.0, 30.0, P, G, GB, 500, 0.00005, 0.00003)
            out[j * nu + i] = t if t > 0 else 1e9


class ShadowMaps:
    """Depth maps seen from the lights, for soft, stable shadows."""

    def __init__(self):
        self.maps = []
        self.rows = []
        self.length = 0

    def add(self, P, G, GB, light_dir, centre, extent, res, tan_light, bias=0.0004, back=6.0):
        L = np.asarray(light_dir, float)
        L = L / np.linalg.norm(L)
        Wd = -L
        helper = np.array([0, 1.0, 0]) if abs(Wd[1]) < 0.9 else np.array([1.0, 0, 0])
        U = np.cross(helper, Wd)
        U /= np.linalg.norm(U)
        V = np.cross(Wd, U)
        o = np.asarray(centre, float) + L * back
        nu = nv = int(res)
        out = np.zeros(nu * nv, np.float32)
        depth_map(nu, nv, o, U, V, Wd, extent, extent, P, G, GB, out)
        row = np.zeros(19)
        row[0], row[1], row[2] = self.length, nu, nv
        row[3:6], row[6:9], row[9:12], row[12:15] = o, U, V, Wd
        row[15], row[16], row[17], row[18] = extent, extent, tan_light, bias
        self.maps.append(out)
        self.rows.append(row)
        self.length += out.size
        return len(self.rows) - 1

    def arrays(self):
        return np.concatenate(self.maps), np.array(self.rows)
