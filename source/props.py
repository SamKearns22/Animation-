"""Props that the characters handle: the chopping board, the glazed Christmas ham and the cleaver.

Each is an object with a position (and for the cleaver an orientation) so a shot can move it frame by frame,
build it into the scene, and measure against it (for the automatic checks and for placing hands).
World coordinates: metres, y up.
"""
import numpy as np

from materials import (WOOD, MEAT, HAMPINK, PINEAPPLE, CHERRY, PAPER, BONE, STEEL, HANDLE)
from sdf3d import rot, UNION, SUNION, SSUB, SUB


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


class Board:
    def __init__(self, centre, half):
        self.c, self.half = np.asarray(centre, float), np.asarray(half, float)

    @property
    def top(self):
        return self.c[1] + self.half[1]

    def build(self, b):
        b.set_frame((0, 0, 0), None)
        b.group('board', margin=0.01)
        b.box(self.c, self.half, WOOD, op=UNION, r=0.006)


class Ham:
    """A glazed ham on the bone lying on the board: scored in diamonds and studded with cloves, pineapple rings
    pinned on with glace cherries, the shank bone dressed in a paper frill. It is cut from one end; `cut` is
    where the cut face is, measured along the ham from its middle (negative: towards the cut end)."""

    R = np.array([0.100, 0.064, 0.074])                      # half length, height, width

    def __init__(self, centre, angle, cut, slices=()):
        self.c = np.asarray(centre, float)
        self.angle = angle
        self.a = np.array([np.cos(np.radians(angle)), 0.0, np.sin(np.radians(angle))])  # along the ham
        self.across = np.cross(self.a, [0, 1.0, 0])          # its side facing us
        self.cut = cut
        self.slices = list(slices)                          # (centre, rotation) of slices lying about
        self.base_y = self.c[1] - 0.058                      # its flat underside, on the board

    def frame(self):
        return np.stack([self.a, [0, 1.0, 0], self.across], 1)

    def top_at(self, along):
        """Height of the top of the ham at a distance along it from the middle."""
        return self.c[1] + self.R[1] * np.sqrt(max(0.0, 1 - (along / self.R[0]) ** 2))

    def distance(self, p):
        """Approximate distance from points to the ham's surface (negative inside)."""
        q = (np.atleast_2d(p) - self.c) @ self.frame()
        k0 = np.linalg.norm(q / self.R, axis=1)
        k1 = np.linalg.norm(q / self.R ** 2, axis=1)
        d = k0 * (k0 - 1) / np.maximum(k1, 1e-9)
        d = np.maximum(d, self.base_y + 0.002 - np.atleast_2d(p)[:, 1])
        return np.maximum(d, self.cut - q[:, 0])

    def build(self, b, press=None):
        """press: (grid, origin, rotation) of a hand pressing into the meat - the meat is dented round it."""
        b.set_frame((0, 0, 0), None)
        b.group('ham', margin=0.02)
        Rh = self.frame()
        b.ellipsoid(self.c, self.R, MEAT, op=UNION, R=Rh)
        b.halfspace(np.array([self.c[0], self.base_y + 0.002, self.c[2]]), np.eye(3), MEAT, op=SUB)
        b.halfspace(self.c + self.cut * self.a, np.stack([np.cross([0, 1.0, 0], self.a), self.a, [0, 1.0, 0]], 1),
                    MEAT, op=SUB)
        if press is not None:
            grid, o, R = press
            b.set_frame(o, R)
            b.grid(grid[0], grid[1], grid[2], MEAT, op=SSUB, k=0.004)
            b.set_frame((0, 0, 0), None)
        shank_a = self.c + self.a * (self.R[0] - 0.02) + np.array([0, 0.004, 0])
        shank_b = shank_a + self.a * 0.042 + np.array([0, 0.010, 0])
        b.capsule(shank_a, shank_b, 0.0095, BONE, op=SUNION, k=0.010)
        fr = shank_a + (shank_b - shank_a) * 0.62
        sd = unit(shank_b - shank_a)
        b.group('frill', margin=0.01)
        Rf = np.stack([self.across, sd, np.cross(self.across, sd)], 1)
        b.cone(fr, fr + sd * 0.020, 0.0125, 0.017, PAPER, op=UNION)
        b.cylinder(fr + sd * 0.011, 0.011, 0.0100, PAPER, op=SUB, R=Rf)
        b.group('garnish', margin=0.01)
        for s_, phi in ((-0.42, 0.95), (0.05, 1.00), (0.50, 0.90)):
            if s_ * self.R[0] - 0.021 < self.cut:
                continue                                     # this ring went with the slices already cut
            rr = np.sqrt(1 - s_ ** 2)
            loc = np.array([s_ * self.R[0], self.R[1] * rr * np.cos(phi), self.R[2] * rr * np.sin(phi)])
            n_ = unit(Rh @ unit(loc / self.R ** 2))
            p = self.c + Rh @ loc
            x_ = unit(np.cross(n_, [0, 0, 1.0]))
            Rn = np.stack([x_, n_, np.cross(x_, n_)], 1)
            b.cylinder(p - n_ * 0.001, 0.0042, 0.021, PINEAPPLE, op=UNION, R=Rn, rr=0.002)
            b.cylinder(p, 0.010, 0.0075, PINEAPPLE, op=SUB, R=Rn)
            b.sphere(p + n_ * 0.003, 0.0072, CHERRY, op=UNION)
        for i, (sc, Rs) in enumerate(self.slices):
            b.group('slice%d' % i, margin=0.01)
            b.cylinder(sc, 0.0034, 0.058, MEAT, op=UNION, R=Rs, rr=0.002)
            b.cylinder(sc + Rs @ np.array([0, 0.0006, 0]), 0.0034, 0.051, HAMPINK, op=UNION, R=Rs, rr=0.002)

    def fill_params(self, SP):
        """The meat's surface pattern needs the ham's frame, and where its pink cut face is."""
        SP[115:118], SP[118:121], SP[121:124] = self.c, self.a, self.across
        SP[124] = self.cut


class Cleaver:
    """A heavy square blade on a dark wooden handle with steel rivets. Placed by `o`, the middle of its edge,
    and R, whose columns are: along the blade towards its tip, up from the edge to the spine, and the blade's
    face normal."""

    HANDLE_R = 0.0125

    def __init__(self, o, R):
        self.o, self.R = np.asarray(o, float), np.asarray(R, float)

    @property
    def x(self):
        return self.R[:, 0]

    @property
    def heel(self):
        """Back top corner of the blade, where the handle starts."""
        return self.o + self.R @ np.array([-0.07, 0.075, 0])

    @property
    def butt(self):
        return self.heel - 0.12 * self.x

    def blade_points(self, n=(41, 21)):
        u, v, w = np.meshgrid(np.linspace(-1, 1, n[0]), np.linspace(-1, 1, n[1]), (-1, 1), indexing='ij')
        centre = self.o + self.R @ np.array([0.030, 0.049, 0])
        return centre + np.stack([u.ravel() * 0.100, v.ravel() * 0.049, w.ravel() * 0.0016], 1) @ self.R.T

    def edge_points(self, n=41):
        t = np.linspace(-0.07, 0.13, n)
        return self.o + np.outer(t, self.x)

    def build(self, b):
        R, o, x = self.R, self.o, self.x
        b.set_frame((0, 0, 0), None)
        b.group('cleaver', margin=0.01)
        centre = o + R @ np.array([0.030, 0.049, 0])
        b.box(centre, (0.100, 0.049, 0.0016), STEEL, op=UNION, r=0.0012, R=R)
        b.box(centre + R @ np.array([0, 0.042, 0]), (0.100, 0.009, 0.0026), STEEL, k=0.002, r=0.0015, R=R)
        b.cylinder(o + R @ np.array([0.110, 0.070, 0]), 0.01, 0.0085, STEEL, op=SUB,
                   R=np.stack([R[:, 0], R[:, 2], R[:, 1]], 1))
        heel = self.heel
        b.box(heel + R @ np.array([0.004, -0.004, 0]), (0.006, 0.010, 0.0060), STEEL, k=0.002, r=0.002, R=R)
        b.capsule(heel - x * 0.006, self.butt, self.HANDLE_R, HANDLE, k=0.003)
        for t in (0.030, 0.065, 0.100):
            for sgn in (1, -1):
                b.sphere(heel - x * t + sgn * R[:, 2] * 0.0118, 0.0032, STEEL, k=0.001)


def slice_lying(centre, yaw):
    """A slice lying flat on the board."""
    return np.asarray(centre, float), rot(yaw=yaw)
