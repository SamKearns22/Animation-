#!/usr/bin/env python3
"""MAP  gun3d_film: a solid pistol (slide, frame, raked grip, trigger guard, muzzle) built as real 3D blocks and
drawn through the film's own camera in the flat look, so it reads as a pistol from any side.

Why (GTA shot 4, chat 26 F2, chat 28: "the pistol reads as a stick (15.6), a blade (21.25)"): the drawn pistol was
a flat card in the barrel's plane: from above, below or behind it shrank to a line or a dark sliver. A real pistol
is about 3 cm thick; seen end-on it is a small upright block with the grip under it, from above a long narrow slab.

The pistol's own frame (as leanout.draw_gun's flat one): a along the barrel (muzzle +), b down (grip +), c across
(its right side +), in units of 0.62 * the gun's size (metres): the same outlines as the flat drawing, given depth.

  PARTS ........... (name, outline in (a, b), half thickness, colour)
  mesh(g) ......... the pistol's blocks in its own frame (points, triangles, kind per point) at size g
  draw(img, cam, hand, d, down, g, report=None)
                    onto img: hand (the grip's top middle, world), d the barrel's way, down the grip's way
  sheet(OUT) ...... the pistol from 8 directions round it and from above and below (the test before the film)

    python3 source/gun3d_film.py sheet OUT.jpg
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import hand3d_film as HF    # noqa: E402

UNIT = 0.62
GRIP = (-0.02, 0.12)   # where the middle of the fist sits on the pistol (a, b, in UNITs): round the handle, its top
#                        just under the slide, the trigger guard in front (Sam 23 Nov, chat 43: "on the handle/trigger
#                        area"; reference references/grand-theft-autism/pistol-grip-real-hand.jpg). Every pistol in a
#                        fist uses this: the grey test (bench_move.pistol_mesh), shot 4 and shots 5-8 (leanout).
COLS = ((132, 138, 152), (70, 74, 84), (44, 46, 54), (30, 30, 36), (200, 206, 218))   # slide, frame, grip, muzzle, shine
PARTS = [
    ('slide', [(-0.05, -0.012), (0.19, -0.012), (0.19, 0.045), (-0.05, 0.045)], 0.022, 0),
    ('frame', [(-0.03, 0.045), (0.14, 0.045), (0.14, 0.075), (0.04, 0.085), (-0.03, 0.075)], 0.019, 1),
    ('grip', [(-0.05, 0.045), (0.035, 0.045), (0.015, 0.20), (-0.075, 0.20)], 0.021, 2),
    ('guard_front', [(0.105, 0.075), (0.115, 0.075), (0.10, 0.12), (0.09, 0.12)], 0.009, 1),
    ('guard_bottom', [(0.055, 0.112), (0.10, 0.112), (0.10, 0.12), (0.055, 0.12)], 0.009, 1),
    ('muzzle', [(0.188, -0.004), (0.196, -0.004), (0.196, 0.037), (0.188, 0.037)], 0.016, 3),
    ('sight', [(0.165, -0.026), (0.18, -0.026), (0.18, -0.012), (0.165, -0.012)], 0.005, 1),
    ('rear_sight', [(-0.04, -0.024), (-0.02, -0.024), (-0.02, -0.012), (-0.04, -0.012)], 0.014, 1),
]


def _prism(poly, hw, kind):
    """A convex outline extruded +-hw across, with its own points for every face (sharp edges keep their lines)."""
    P = [np.array([a, b], float) for a, b in poly]
    n = len(P)
    V, T, K = [], [], []

    def face(pts):
        i0 = len(V)
        V.extend(pts)
        K.extend([kind] * len(pts))
        for j in range(1, len(pts) - 1):
            T.append((i0, i0 + j, i0 + j + 1))
    face([(p[0], p[1], hw) for p in P])
    face([(p[0], p[1], -hw) for p in reversed(P)])
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        face([(a[0], a[1], -hw), (b[0], b[1], -hw), (b[0], b[1], hw), (a[0], a[1], hw)])
    return V, T, K


def mesh(g=1.0):
    V, T, K = [], [], []
    for _, poly, hw, kind in PARTS:
        v, t, k = _prism(poly, hw, kind)
        o = len(V)
        V += v
        T += [(a + o, b + o, c + o) for a, b, c in t]
        K += k
    return np.array(V) * UNIT * g, np.array(T), np.array(K)


def draw(img, cam, hand, d, down, g=1.0, outline=None):
    """The pistol onto img. Returns its drawn box or None."""
    d = np.asarray(d, float)
    d = d / np.linalg.norm(d)
    down = np.asarray(down, float)
    down = down - d * (down @ d)
    down /= np.linalg.norm(down)
    side = np.cross(d, down)                          # its right side, when the grip is down and the muzzle ahead
    V, T, K = mesh(g)
    W = np.asarray(hand, float) + V[:, :1] * d + V[:, 1:2] * down + V[:, 2:3] * side
    got = HF.paint(img, cam, W, T, COLS[0], np.asarray(hand, float) + d * 0.05 * g, outline, 0.5,
                   colours=COLS, kind=K, shade=True)
    if got is None:
        return None
    lay, (x0, y0), _ = got
    img.alpha_composite(lay, (x0, y0))
    return (x0, y0, x0 + lay.width, y0 + lay.height)


def sheet(out):
    import sets as S
    tiles = []
    for el in (0, 50, -50):
        for deg in range(0, 360, 45):
            a, e = math.radians(deg), math.radians(el)
            pos = (math.sin(a) * math.cos(e) * 0.6, math.sin(e) * 0.6, math.cos(a) * math.cos(e) * 0.6)
            cam = S.Cam(pos, (0.0, 0.0, 0.0), focal=1000 * 0.6 / 0.3)
            im = Image.new('RGBA', (2160, 3840), (235, 230, 222, 255))
            draw(im, cam, (-0.05, 0.0, 0.0), (1, 0, 0), (0, -1, 0), 1.0)
            t = im.crop((480, 1320, 1680, 2520)).convert('RGB').resize((260, 260), Image.LANCZOS)
            ImageDraw.Draw(t).text((6, 6), f'{deg} el{el}', fill=(0, 0, 0))
            tiles.append(t)
    sh = Image.new('RGB', (260 * 8, 260 * 3), 'white')
    for i, t in enumerate(tiles):
        sh.paste(t, ((i % 8) * 260, (i // 8) * 260))
    sh.save(out, quality=88)


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
