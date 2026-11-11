#!/usr/bin/env python3
"""eyekit: rule S5 for every cast (tool job, 11 Nov): the iris, pupil and shine are cut to the eye's outline, so they
never spill out at any size or glance. Every new cast's eye drawing uses `inside` (or `iris_and_pupil`); preflight's
house-style check names a cast file that draws a pupil without it.

MAP
  circle ........... the points of a circle or oval (a convex shape to cut)
  inside ........... the part of a convex shape (iris, pupil, shine) that lies inside the eye's outline
  iris_and_pupil ... draws iris, pupil and shine, each cut to the outline (the outline's own line is the caller's)
  spill ............ how much of a shape lies outside the outline (0 = none): what the kittest and checks measure

    import eyekit
    eyekit.iris_and_pupil(p, outline, cx, cy, iris_r, IRIS, pupil_r, shine=(-0.3, -0.32, 0.16))
"""
import math

from traitors_cast import clip_convex

INK = (28, 24, 26)
SHINE = (255, 255, 255)


def circle(cx, cy, rx, ry=None, n=28):
    ry = rx if ry is None else ry
    return [(cx + rx * math.cos(a), cy + ry * math.sin(a))          # as ed.oval draws it (the last point repeats
            for a in (2 * math.pi * i / (n - 1) for i in range(n))]   # the first), so a shape that fits is unchanged


def _area(pts):
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))) / 2 if len(pts) >= 3 else 0.0


def _ccw(pts):
    s = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))
    return pts if s > 0 else pts[::-1]


def inside(outline, shape):
    """The part of `shape` (convex: a circle, an oval) inside `outline` (the eye's opening, any simple shape).
    Returns the points to fill; fewer than 3 means nothing shows."""
    return clip_convex(_ccw(list(outline)), _ccw(list(shape)))


def spill(outline, shape):
    """The share of `shape` that lies outside `outline`: 0 when it is all inside."""
    a = _area(list(shape))
    return 0.0 if a <= 0 else max(0.0, 1.0 - _area(inside(outline, shape)) / a)


def iris_and_pupil(p, outline, cx, cy, iris_r, iris, pupil_r, pupil=INK, shine=(-0.3, -0.32, 0.16), shine_col=SHINE,
                   squash=1.0):
    """Iris, pupil and one shine, each cut to the outline. shine = (dx, dy, r) as shares of iris_r, or None.
    squash > 1 makes them taller than wide (an oval eye)."""
    for r, col in ((iris_r, iris), (pupil_r, pupil)):
        if r and col is not None:
            shape = circle(cx, cy, r, r * squash)
            part = shape if spill(outline, shape) < 1e-4 else inside(outline, shape)   # untouched when it fits
            if len(part) >= 3:
                p.poly(part, col, None)
    if shine:
        dx, dy, sr = shine
        sx, sy, rr = cx + dx * iris_r, cy + dy * iris_r, sr * iris_r
        if spill(outline, circle(sx, sy, rr, rr, 40)) < 1e-4:
            p.ell(sx, sy, rr, rr, shine_col, None)
        else:
            part = inside(outline, circle(sx, sy, rr, rr, 40))
            if len(part) >= 3:
                p.poly(part, shine_col, None)
