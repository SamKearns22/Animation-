#!/usr/bin/env python3
"""stage: people on a perspective floor (one camera in metres; series.Room is the projection).

Everyone stands on the floor at (X, Z) metres: their size follows their distance, their feet meet the floor, and
the nearer person is drawn over the farther one. With the camera at eye height, every standing adult's eyes sit on
the horizon line whatever their distance (checked).

    st = Stage(Room(...)); st.draw(img, cam, [Actor(sp, X, Z, yaw, pose, t), ...])
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import figure as F           # noqa: E402
import kit                   # noqa: E402
import views as V            # noqa: E402
from ed import INK           # noqa: E402


class Actor:
    def __init__(self, sp, X, Z, yaw=0.0, pose=None, t=0.0, head_yaw=None):
        self.sp, self.X, self.Z, self.yaw, self.pose, self.t, self.head_yaw = sp, X, Z, yaw, pose, t, head_yaw


class Stage:
    def __init__(self, room):
        self.room = room

    def place(self, X, Z):
        """(x, y, s): the neck base on the screen and the scale of someone standing at (X, Z)."""
        return self.room.person(X, Z)

    def floor(self, img, cam, colr=(196, 198, 186), line=(178, 180, 168), x0=-8, x1=8, z0=0.0, z1=12.0, grid=1.0):
        p = B.Pen(img, cam)
        r = self.room
        if r.facing == 'front':
            z1 = min(z1, r.Z - 0.6)                         # never past the camera (it would project wrongly)
        p.poly(r.quad([(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)]), colr, None)
        k = x0
        while k <= x1:
            p.line(r.quad([(k, 0, z0), (k, 0, z1)]), line, 2)
            k += grid
        z = z0
        while z <= z1:
            p.line(r.quad([(x0, 0, z), (x1, 0, z)]), line, 2)
            z += grid

    def draw(self, img, cam, actors):
        """Draw everyone, the farthest first; each with a soft contact shadow under the feet."""
        for a in sorted(actors, key=lambda a: self.room.depth(a.Z), reverse=True):
            x, y, s = self.place(a.X, a.Z)
            kit.contact_shadow(img, cam, x, y + F.SOLE_Y * s + (a.pose or {}).get('bob', 0.0) * 0 , 300 * s)
            V.person(img, cam, x, y, s, a.sp, a.t, a.yaw, a.pose, a.head_yaw)

    def check_horizon(self, X, Z, eye_m=1.52, tol=6):
        """With the camera at eye height, a standing person's eyes sit on the horizon line (perspective is right)."""
        r = self.room
        if abs(r.Y - eye_m) > 0.05:
            return []
        hx, hy = r.P(0, r.Y, 1e6 if r.facing == 'front' else -1e6)
        x, y, s = self.place(X, Z)
        eyes = y - 150 * s
        return [] if abs(eyes - hy) <= tol * max(1.0, s) else [f'eyes at {eyes:.0f}, horizon at {hy:.0f}: not on one floor']
