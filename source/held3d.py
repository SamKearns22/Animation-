#!/usr/bin/env python3
"""held3d: a 3D prop held by a flat person, through the real camera (kit lesson, Patriots 3, 27 Oct: the MG42 was drawn
through the person's own flat frame, so in shot 9 it lay sideways and below the Patriot; drawn through the real camera,
with the hands put on the grip points where the camera sees them, it sat in true perspective in every shot).

- `through(cam)`: while drawing the prop, views.project is the real camera (world metres in, screen pixels out), so a
  prop built from 3D points (a gun, a shovel, a steering wheel) is drawn in true perspective from any camera.
- `body_point(cam, x, z, yaw, j, place, height)`: a function turning a world point into the hand target in that
  person's own frame (views' torso frame, before the lean) that lands on the very screen point the camera sees.
- `hold(j, cam, x, z, yaw, place, grips, draw, ...)`: both hands (or one) onto the grips, nearest shoulder to nearest
  grip; the prop drawn with them (`draw(p, j2)`, its hands over it); when the prop is nearer the lens than the
  shoulders, the arms go behind it and only the hands over (views' 'wrap', Patriots 3 note 12).

`place` is lying.place(cam, x, z, ground, height): (Xf, Yf, s, e, c), the same numbers views.person is drawn with.
Use it with lying.stand (same camera, same place) or a film's own call of views.person(..., tilt=(e, c)).
"""
import contextlib
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import views as V            # noqa: E402

M = V.M_PER_UNIT


@contextlib.contextmanager
def through(cam):
    """views.project swapped for the real camera while a 3D prop draws (its points are world metres)."""
    real = V.project
    V.project = lambda p3, yaw: (cam.project(p3)[0], -cam.depth(p3))
    try:
        yield lambda w: V.project(w, 0)
    finally:
        V.project = real


def body_point(cam, x, z, yaw, j, place, height=1.75):
    """world point -> the hand target in this person's frame that the camera sees on the same screen point."""
    Xf, Yf, s, e, c = place
    deg, mirror = V.snap(yaw)
    flip = -1 if mirror else 1
    ang = math.radians(deg)
    Yn = Yf - 928 * s + j.get('bob', 0.0) * s
    unit = M * height / 1.75
    tc = np.array((cam.pos[0] - x, cam.pos[2] - z))
    tc /= np.linalg.norm(tc) or 1.0

    def target(W):
        (X, Y), _ = cam.project(W)
        d = float(np.dot((W[0] - x, W[2] - z), tc)) / unit          # how much nearer the lens than the body
        px = (X - Xf) / (s * flip)
        py = 928.0 + ((Y - Yn) / s - 928.0) / c
        bx, bz, by = px * math.cos(ang) - d * math.sin(ang), px * math.sin(ang) + d * math.cos(ang), py - e * d
        return V.leaned((bx, by, bz), -j.get('lean', 0.0))
    return target


def hold(j, cam, x, z, yaw, place, grips, draw, height=1.75, one_hand=False, reach=1.0, centre=None,
         shoulders=1.35, pole='down', shape='fist'):
    """Hands on a 3D prop's grips (world points) where the camera sees them; the prop drawn with the hands over it.
    one_hand: only the hand nearest the last grip (resting on it); reach (0-1): part way there from where the hand was;
    centre: a world point in the prop's middle (default the grips' mean), tested against the shoulders' distance from
    the lens (`shoulders` metres up) for 'wrap'. Returns [(side, target)]."""
    target = body_point(cam, x, z, yaw, j, place, height)
    pts = [target(g) for g in grips]
    near = lambda side, q: math.dist(j['sh' + side], q)
    if len(pts) >= 2:
        sides = ('R', 'L') if near('R', pts[0]) + near('L', pts[1]) <= near('L', pts[0]) + near('R', pts[1]) \
            else ('L', 'R')
        pairs = list(zip(sides, pts))
    else:
        pairs = [(min('LR', key=lambda sd: near(sd, pts[0])), pts[0])]
    if one_hand:
        side = min('LR', key=lambda sd: near(sd, pts[-1]))
        pairs = [(side, pts[-1])]
    for side, q in pairs:
        if reach < 1.0:
            q = tuple(a + (b - a) * reach for a, b in zip(j['wr' + side], q))
        V.arm_to(j, side, q, pole, shape)
    draw.held = True
    j['props'] = [draw]
    j['grip'] = {sd for sd, _ in pairs}
    W = centre if centre is not None else tuple(np.mean(np.asarray(grips, float), 0))
    if math.dist(cam.pos, W) < math.dist(cam.pos, (x, shoulders, z)) - 0.15:
        j['wrap'] = set(j['grip'])
    return pairs
