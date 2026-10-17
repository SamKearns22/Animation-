#!/usr/bin/env python3
"""The Traitors (TikTok satire): the four people, drawn from Sam's reference photos (references/traitors/).

Each likeness is its own head (face shape, hair, eyes, brows, nose, resting mouth); talking mouths come from the
series' lip-sync shapes (mouths.draw). Bodies are the satire package's (views.person, front view): only the head and
the outfit details are drawn here. Hooked into burnham by `who` in the person's dict, so everyone else is untouched.

    Trump    navy suit, white shirt, long red tie, flag pin; swept blond hair, tan with pale rings round the eyes,
             squint, heavy jowls, the pout (refs 16-21)
    Putin    dark suit, white shirt, navy dotted tie; thin receding light hair, wide cheekbones, hooded narrow eyes,
             thin flat mouth (refs 22, 25-27); blood spattered over him (`blood`), believable, never cartoon splats
    Zelensky all black: military-style jacket with a stand collar and chest pockets, black shirt; short dark crop,
             close dark beard, heavy brows, tired eyes (refs 16-24)
    Claudia  black tailored jacket, white blouse, black rose at the throat, frilled cuffs; heavy blunt fringe to the
             eyes, long straight black hair, smoky eyes, nude lips (refs 3, 11-15)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import mouths                    # noqa: E402
from ed import INK, curve, oval  # noqa: E402

mouths.install(B)


def blend(a, b, k):
    return tuple(int(round(x + (y - x) * k)) for x, y in zip(a, b))


def dk(c, k=0.8):
    return tuple(int(v * k) for v in c)


def clip_convex(subject, window):
    """The part of a shape inside a convex window (Sutherland-Hodgman): an iris kept inside its eye."""
    def inside(q, a, b):
        return (b[0] - a[0]) * (q[1] - a[1]) - (b[1] - a[1]) * (q[0] - a[0]) >= 0

    def cross(p1, p2, a, b):
        x1, y1, x2, y2, x3, y3, x4, y4 = *p1, *p2, *a, *b
        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(d) < 1e-9:
            return p2
        u = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
        return (x1 + u * (x2 - x1), y1 + u * (y2 - y1))
    out = list(subject)
    for i in range(len(window)):
        a, b = window[i], window[(i + 1) % len(window)]
        inp, out = out, []
        if not inp:
            break
        s = inp[-1]
        for e in inp:
            if inside(e, a, b):
                if not inside(s, a, b):
                    out.append(cross(s, e, a, b))
                out.append(e)
            elif inside(s, a, b):
                out.append(cross(s, e, a, b))
            s = e
    return out


def eye(p, ex, ey, sgn, w, h, iris, st, lid_c, liner=2.6, lower=1.4, lashes=False, smoky=None):
    """One opening between two lids, the iris cut to it (no line ever crosses the white). st: lid (0 open .. 1 shut),
    look (-1 .. 1 across), gaze_dy (down +), squint (lower lid up), closed."""
    us = np.linspace(-1, 1, 15)
    if smoky:                                          # made-up eyes: a flat dark shadow round the opening
        p.poly(curve([(ex - w - 4, ey + 1), (ex - w * 0.4, ey - h - 7), (ex + w * 0.5, ey - h - 8), (ex + w + 7, ey - 3),
                      (ex + w * 0.6, ey + h + 3), (ex - w * 0.5, ey + h + 3)], 4), smoky, None)
    if st.get('closed'):
        p.line([(ex + w * u, ey + 1 + h * 0.45 * (1 - u * u)) for u in us], INK, liner)
        return
    lid, squint = st.get('lid', 0.0), st.get('squint', 0.0)
    up_open = [(ex + w * u, ey - h * (1 - u * u)) for u in us]
    up = [(ex + w * u, ey - h * (1 - u * u) * (1 - lid)) for u in us]
    lo = [(ex + w * u, ey + h * 0.8 * (1 - squint) * (1 - u * u)) for u in us]
    opening = up + lo[::-1][1:-1]
    p.poly(opening, (250, 250, 247), None)
    cx, cy = ex + st.get('look', 0.0) * w * 0.38, ey + st.get('gaze_dy', 0.0)
    circ = lambda r: [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 22, endpoint=False)]
    ir = clip_convex(opening[::-1], circ(h * 0.95))
    if len(ir) >= 3:
        p.poly(ir, iris, None)
    pu = clip_convex(opening[::-1], circ(h * 0.42))
    if len(pu) >= 3:
        p.poly(pu, INK, None)
    if lid > 0.02:
        p.poly(up_open + up[::-1], lid_c, None)
    p.line(lo, INK if smoky else dk(lid_c, 0.7), lower)
    p.line(up, INK, liner)
    if lashes:
        tip = up[-1] if sgn > 0 else up[0]
        p.line([tip, (tip[0] + sgn * 7, tip[1] - 5)], INK, liner * 0.8)


def brow(p, ex, ey, sgn, c, w, inner_dy, outer_dy, length=24, thick=None):
    """A brow as a filled tapered shape (inner end towards the nose)."""
    th = thick or w
    a = (ex - sgn * length * 0.55, ey + inner_dy)
    m = (ex + sgn * length * 0.05, ey - 3 + (inner_dy + outer_dy) * 0.4)
    b = (ex + sgn * length * 0.6, ey + outer_dy)
    p.poly(curve([(a[0], a[1] - th * 0.5), (m[0], m[1] - th * 0.55), (b[0], b[1] - th * 0.2), (b[0], b[1] + th * 0.15),
                  (m[0], m[1] + th * 0.5), (a[0], a[1] + th * 0.5)], 3), c, None)


def ears(p, hx, hy, hw, skin, dy=6, rx=12, ry=22):
    for sgn in (-1, 1):
        p.poly(oval(hx + sgn * (hw + 2), hy + dy, rx, ry, 24), skin, INK, 2.4)
        p.line([(hx + sgn * (hw + 4), hy + dy - 10), (hx + sgn * (hw + 8), hy + dy), (hx + sgn * (hw + 4), hy + dy + 10)],
               dk(skin, 0.75), 1.4)


def talk_or(p, sp, t, fx, my, rest):
    m = sp.get('mouth', 'rest')
    if isinstance(m, str) and m.startswith('v:') and m != 'v:rest':
        mouths.draw(p, sp, fx, my, m[2:])
    else:
        rest()


# --------------------------------------------------------------------------------------------- Trump
T_SKIN = (232, 160, 112)
T_RING = (240, 190, 148)          # the paler skin round the eyes
T_HAIR = (236, 202, 134)
T_HAIR_L = (248, 224, 170)
T_HAIR_D = (196, 156, 92)


def trump_head(img, p, sp, t, hx, hy):
    hw, hh, skin = 80, 92, T_SKIN
    turn = sp.get('turn', 0.0)
    fx = hx + turn * hw * 0.2
    fy = hy + 10 * sp.get('down', 0.0)
    ears(p, hx - turn * 6, hy, hw, skin)
    outline = curve([(hx - hw, hy - 10), (hx - hw * 0.86, hy - hh * 0.72), (hx - hw * 0.4, hy - hh * 1.04),
                     (hx + hw * 0.4, hy - hh * 1.04), (hx + hw * 0.86, hy - hh * 0.72), (hx + hw, hy - 10),
                     (hx + hw * 1.04, hy + hh * 0.48), (hx + hw * 0.96, hy + hh * 0.88), (hx + hw * 0.66, hy + hh * 1.1),
                     (hx + hw * 0.28, hy + hh * 1.2), (hx, hy + hh * 1.22), (hx - hw * 0.28, hy + hh * 1.2),
                     (hx - hw * 0.66, hy + hh * 1.1), (hx - hw * 0.96, hy + hh * 0.88), (hx - hw * 1.04, hy + hh * 0.48)], 4)
    p.poly(outline, skin, INK, 2.6)
    sd = dk(skin, 0.86)
    for sgn in (-1, 1):                                # the pale rings round the eyes (goggle tan)
        p.poly(curve(oval(fx + sgn * 32, fy - 5, 25, 15, 12)), blend(skin, T_RING, 0.6), None)
    for sgn in (-1, 1):                                # jowls: from the nose wings down past the mouth to the jaw
        p.line([(fx + sgn * 26, fy + 36), (fx + sgn * 40, fy + 66), (fx + sgn * 50, fy + 92)], sd, 2.0)
        p.line([(hx + sgn * hw * 0.92, hy + hh * 0.78), (hx + sgn * hw * 0.72, hy + hh * 1.0)], sd, 1.8)
    p.line([(fx - 22, hy + hh * 1.08), (fx, hy + hh * 1.12), (fx + 22, hy + hh * 1.08)], sd, 1.8)      # the double chin
    for k in range(2):                                 # forehead creases
        p.line([(fx - 30, fy - 46 + 8 * k), (fx, fy - 49 + 8 * k), (fx + 30, fy - 46 + 8 * k)], sd, 1.6)
    st = dict(lid=sp.get('lid', 0.42), look=sp.get('look', 0.0), squint=sp.get('squint', 0.3),
              closed=sp.get('blink', False), gaze_dy=sp.get('gaze_dy', 0.0))
    frown = sp.get('frown', 1.0)
    for sgn in (-1, 1):
        ex, ey = fx + sgn * 32, fy - 6
        eye(p, ex, ey, sgn, 15, 7, (104, 136, 168), st, blend(T_RING, skin, 0.6), liner=2.4)
        p.line([(ex - 12, ey + 9), (ex, ey + 12), (ex + 12, ey + 9)], blend(T_RING, skin, 0.6), 1.4)   # bags
        brow(p, ex, ey - 19, sgn, (186, 140, 86), 6, 4 * frown, -3 + sp.get('brow_raise', 0) * -1, 30)
    p.line([(fx - 3, fy - 4), (fx - 9, fy + 26)], dk(skin, 0.7), 1.8)                                # a broad nose
    p.line(curve([(fx - 20, fy + 30), (fx - 12, fy + 38), (fx, fy + 40), (fx + 12, fy + 38), (fx + 20, fy + 30),
                  (fx, fy + 30)], 3)[:15], INK, 1.8)
    for sgn in (-1, 1):
        p.line([(fx + sgn * 20, fy + 30), (fx + sgn * 16, fy + 22)], INK, 1.6)
    my = fy + 62

    def rest():                                        # the pout: lips pushed forward into a small rosebud
        if sp.get('sneer'):
            p.poly(curve([(fx - 18, my + 3), (fx, my - 3), (fx + 20, my - 6), (fx + 14, my + 7), (fx, my + 9),
                          (fx - 14, my + 7)], 3), (196, 116, 98), INK, 1.8)
            p.line([(fx - 18, my + 3), (fx, my + 2), (fx + 20, my - 6)], INK, 2.0)
            return
        p.poly(curve(oval(fx, my + 2, 16, 10, 12)), (196, 116, 98), INK, 1.8)
        p.line([(fx - 9, my + 2), (fx, my + 4), (fx + 9, my + 2)], INK, 2.0)
        for sgn in (-1, 1):
            p.line([(fx + sgn * 18, my), (fx + sgn * 24, my + 6)], sd, 1.5)
    talk_or(p, sp, t, fx, my, rest)
    hair = [(hx - hw - 2, hy + 6), (hx - hw - 18, hy - 38), (hx - hw - 16, hy - hh * 0.78),
            (hx - hw * 1.1, hy - hh * 1.08), (hx - hw * 0.8, hy - hh * 1.34), (hx - hw * 0.1, hy - hh * 1.44),
            (hx + hw * 0.56, hy - hh * 1.36), (hx + hw * 1.0, hy - hh * 1.08), (hx + hw + 18, hy - hh * 0.56),
            (hx + hw + 10, hy - 12), (hx + hw + 2, hy + 6), (hx + hw - 8, hy - 22), (hx + hw * 0.84, hy - hh * 0.62),
            (hx + hw * 0.4, hy - hh * 0.76), (hx - hw * 0.1, hy - hh * 0.78), (hx - hw * 0.5, hy - hh * 0.82),
            (hx - hw * 0.8, hy - hh * 0.8), (hx - hw * 0.9, hy - hh * 0.64), (hx - hw + 6, hy - 30), (hx - hw + 8, hy + 2)]
    p.poly(curve(hair, 4), T_HAIR, INK, 2.6)
    for k in range(7):                                 # swept from the back of the crown, forward and over to our left
        x0 = hx + hw * (0.95 - 0.12 * k)
        p.line(curve([(x0, hy - hh * 0.62), (x0 - hw * 0.25, hy - hh * 1.12), (x0 - hw * 0.75, hy - hh * 1.3),
                      (x0 - hw * 1.1, hy - hh * 1.1)], 4)[:14], T_HAIR_D if k % 2 else T_HAIR_L, 1.6)
    fl = curve([(hx + hw * 0.2, hy - hh * 0.8), (hx - hw * 0.3, hy - hh * 1.02), (hx - hw * 0.9, hy - hh * 1.04),
                (hx - hw * 1.08, hy - hh * 0.9), (hx - hw * 0.94, hy - hh * 0.74), (hx - hw * 0.6, hy - hh * 0.8),
                (hx - hw * 0.2, hy - hh * 0.76)], 4)
    p.poly(fl, T_HAIR_L, INK, 2.0)                     # the forelock, swept over and curling down at the front
    p.line(curve([(hx - hw * 0.1, hy - hh * 0.86), (hx - hw * 0.6, hy - hh * 0.96), (hx - hw * 0.95, hy - hh * 0.86)], 4)[:10],
           T_HAIR_D, 1.4)
    return fx


def trump_torso(img, p, sp, t):
    tie = sp.get('tie', (196, 28, 40))
    p.poly([(-13, 16), (13, 16), (19, 250), (0, 290), (-19, 250)], tie, INK, 2.0)       # the tie, long, past the belt
    p.poly([(-13, -2), (13, -2), (10, 18), (-10, 18)], tie, INK, 2.0)
    p.line([(-4, 40), (4, 120)], dk(tie, 0.8), 1.4)
    jc = sp.get('jacket', B.NAVY)
    for sgn in (-1, 1):                                # the lapels again, over the long tie
        p.poly([(sgn * 44, -2), (sgn * 70, 30), (sgn * 46, 110), (sgn * 62, 150), (sgn * 24, 250), (sgn * 22, 150)],
               jc, INK, 2.2)
    x, y = -86, 104                                    # the flag pin on his left lapel (our right when mirrored: keep)
    p.poly([(x - 9, y - 6), (x + 9, y - 6), (x + 9, y + 6), (x - 9, y + 6)], (240, 240, 240), INK, 1.2)
    for k in range(3):
        p.line([(x - 9, y - 4 + 4 * k), (x + 9, y - 4 + 4 * k)], (196, 30, 44), 1.4)
    p.poly([(x - 9, y - 6), (x - 1, y - 6), (x - 1, y + 1), (x - 9, y + 1)], (40, 56, 120), None)


# --------------------------------------------------------------------------------------------- Putin
P_SKIN = (240, 210, 192)
P_HAIR = (200, 182, 160)


def putin_head(img, p, sp, t, hx, hy):
    hw, hh, skin = 70, 88, P_SKIN
    turn = sp.get('turn', 0.0)
    fx = hx + turn * hw * 0.2
    fy = hy + 10 * sp.get('down', 0.0)
    ears(p, hx - turn * 6, hy, hw, skin, dy=4)
    outline = curve([(hx - hw, hy - 10), (hx - hw * 0.9, hy - hh * 0.7), (hx - hw * 0.45, hy - hh * 1.06),
                     (hx + hw * 0.45, hy - hh * 1.06), (hx + hw * 0.9, hy - hh * 0.7), (hx + hw, hy - 10),
                     (hx + hw * 1.04, hy + hh * 0.3), (hx + hw * 0.9, hy + hh * 0.74), (hx + hw * 0.5, hy + hh * 1.04),
                     (hx, hy + hh * 1.13), (hx - hw * 0.5, hy + hh * 1.04), (hx - hw * 0.9, hy + hh * 0.74),
                     (hx - hw * 1.04, hy + hh * 0.3)], 4)
    p.poly(outline, skin, INK, 2.6)
    sd = dk(skin, 0.86)
    side = blend(skin, P_HAIR, 0.55)
    for sgn in (-1, 1):                                # thin hair at the sides, cut short
        p.poly(curve([(hx + sgn * (hw + 1), hy + 2), (hx + sgn * (hw + 5), hy - 40), (hx + sgn * hw * 0.92, hy - hh * 0.66),
                      (hx + sgn * hw * 0.78, hy - hh * 0.62), (hx + sgn * (hw - 9), hy - 36), (hx + sgn * (hw - 5), hy + 2)], 4),
               side, None)
    p.poly(curve([(hx - hw * 0.62, hy - hh * 0.86), (hx - hw * 0.3, hy - hh * 1.03), (hx + hw * 0.34, hy - hh * 1.02),
                  (hx + hw * 0.62, hy - hh * 0.86), (hx + hw * 0.22, hy - hh * 0.9), (hx - hw * 0.3, hy - hh * 0.9)], 4),
           blend(skin, P_HAIR, 0.4), None)             # the thin combed top, scalp showing through
    for k in range(6):
        x = hx - hw * 0.5 + k * hw * 0.2
        p.line([(x, hy - hh * 0.92), (x + 10, hy - hh * 1.0)], blend(skin, P_HAIR, 0.7), 1.1)
    p.poly(outline, None, INK, 2.6)
    for sgn in (-1, 1):                                # the high cheekbones, the softer cheeks under them
        p.line([(fx + sgn * 44, fy + 18), (fx + sgn * 34, fy + 40), (fx + sgn * 30, fy + 64)], sd, 1.8)
    p.line([(fx - 26, fy - 50), (fx, fy - 53), (fx + 26, fy - 50)], sd, 1.4)
    st = dict(lid=sp.get('lid', 0.36), look=sp.get('look', 0.0), squint=sp.get('squint', 0.25),
              closed=sp.get('blink', False), gaze_dy=sp.get('gaze_dy', 0.0))
    for sgn in (-1, 1):
        ex, ey = fx + sgn * 29, fy - 8
        eye(p, ex, ey, sgn, 15, 7.5, (112, 136, 156), st, dk(skin, 0.9), liner=2.4)
        p.line([(ex - 13, ey + 9), (ex - 2, ey + 13), (ex + 12, ey + 10)], sd, 1.5)     # puffy under the eyes
        p.line([(ex - 9, ey + 16), (ex + 7, ey + 17)], blend(skin, sd, 0.6), 1.2)
        brow(p, ex, ey - 18, sgn, (178, 150, 128), 4, 2, 2, 26)
    p.line([(fx - 2, fy - 6), (fx - 6, fy + 28), (fx - 2, fy + 34), (fx + 8, fy + 32)], INK, 1.8)   # straight nose
    p.line([(fx - 12, fy + 31), (fx - 7, fy + 34)], INK, 1.4)
    my = fy + 58

    def rest():                                        # thin flat lips; smug: the left corner (our right) up a touch
        s = sp.get('smirk', 0.0)
        p.line([(fx - 20, my + 3), (fx - 6, my + 1), (fx + 8, my + 1 - 2 * s), (fx + 20, my - 5 * s)], INK, 2.4)
        p.line([(fx - 8, my + 7), (fx + 8, my + 7 - s)], blend(skin, (180, 110, 110), 0.4), 1.6)
        if s > 0.3:
            p.line([(fx + 21, my - 6 * s), (fx + 25, my - 2 * s)], sd, 1.4)
    talk_or(p, sp, t, fx, my, rest)
    return fx


def putin_torso(img, p, sp, t):
    tie = sp.get('tie', (34, 40, 74))
    for k in range(18):                                # small white dots on the dark navy tie
        x, y = -8 + 8 * (k % 3) + (4 if (k // 3) % 2 else 0), 30 + 26 * (k // 3)
        if y < 196:
            p.ell(x, y, 1.6, 1.6, (220, 222, 232), None)


# --------------------------------------------------------------------------------------------- Zelensky
Z_SKIN = (228, 184, 156)
Z_HAIR = (58, 46, 40)
Z_BEARD = (66, 54, 48)
Z_BLACK = (34, 34, 38)
Z_SEAM = (78, 78, 86)


def zelensky_head(img, p, sp, t, hx, hy):
    hw, hh, skin = 70, 88, Z_SKIN
    turn = sp.get('turn', 0.0)
    down = sp.get('down', 0.0)
    fx = hx + turn * hw * 0.2
    fy = hy + 28 * down                                # head bowed: the features drop, more crown shows
    ears(p, hx - turn * 6, hy, hw, skin, dy=4)
    outline = curve([(hx - hw, hy - 10), (hx - hw * 0.9, hy - hh * 0.7), (hx - hw * 0.45, hy - hh * 1.06),
                     (hx + hw * 0.45, hy - hh * 1.06), (hx + hw * 0.9, hy - hh * 0.7), (hx + hw, hy - 10),
                     (hx + hw * 0.98, hy + hh * 0.6), (hx + hw * 0.66, hy + hh * 1.02), (hx, hy + hh * 1.14),
                     (hx - hw * 0.66, hy + hh * 1.02), (hx - hw * 0.98, hy + hh * 0.6)], 4)
    p.poly(outline, skin, INK, 2.6)
    sd = dk(skin, 0.84)
    bfill = blend(skin, Z_BEARD, 0.72)
    beard = [(hx - hw - 1, hy + 14), (hx - hw * 0.98, hy + hh * 0.6), (hx - hw * 0.66, hy + hh * 1.02), (hx, hy + hh * 1.16),
             (hx + hw * 0.66, hy + hh * 1.02), (hx + hw * 0.98, hy + hh * 0.6), (hx + hw + 1, hy + 14),
             (hx + hw * 0.84, hy + 24 + 26 * down), (fx + 48, fy + 30), (fx + 30, fy + 46), (fx, fy + 44),
             (fx - 30, fy + 46), (fx - 48, fy + 30), (hx - hw * 0.84, hy + 24 + 26 * down)]
    p.poly(curve(beard, 4), bfill, dk(bfill, 0.8), 1.6)
    p.poly(curve([(fx - 30, fy + 52), (fx - 10, fy + 44), (fx + 10, fy + 44), (fx + 30, fy + 52), (fx + 16, fy + 54),
                  (fx - 16, fy + 54)], 3), bfill, dk(bfill, 0.8), 1.2)                  # the moustache
    rng = np.random.default_rng(31)
    for _ in range(40):                                # a few grey hairs in it
        a, r = rng.uniform(0.25, math.pi - 0.25), rng.uniform(0.7, 0.95)
        x, y = fx + hw * 0.9 * r * math.cos(a), fy + 46 + hh * 0.6 * r * math.sin(a)
        if abs(x - fx) > 26 or y > fy + 74 or y < fy + 52:
            p.line([(x, y), (x + 1, y + 4)], (150, 140, 134) if rng.random() < 0.4 else dk(bfill, 0.8), 1.0)
    p.poly(outline, None, INK, 2.6)
    st = dict(lid=sp.get('lid', 0.3), look=sp.get('look', 0.0), squint=0.1, closed=sp.get('blink', False),
              gaze_dy=sp.get('gaze_dy', 0.0))
    for sgn in (-1, 1):
        ex, ey = fx + sgn * 29, fy - 8
        eye(p, ex, ey, sgn, 15, 8, (76, 54, 40), st, dk(skin, 0.86), liner=2.6)
        p.poly(curve([(ex - 14, ey + 7), (ex, ey + 11), (ex + 14, ey + 7), (ex + 10, ey + 15), (ex - 10, ey + 15)], 3),
               blend(skin, (150, 110, 110), 0.3), None)                                   # the tired dark bags
        p.line([(ex - 12, ey + 10), (ex, ey + 15), (ex + 12, ey + 10)], sd, 1.4)
        brow(p, ex, ey - 17, sgn, (46, 36, 32), 7, -3 * sp.get('worry', 1.0), 3, 30)
    p.line([(fx - 3, fy - 6), (fx - 8, fy + 26)], dk(skin, 0.7), 1.8)
    p.poly(curve([(fx - 16, fy + 30), (fx - 8, fy + 24), (fx + 8, fy + 24), (fx + 16, fy + 30), (fx + 6, fy + 36),
                  (fx - 6, fy + 36)], 3), skin, INK, 1.6)
    my = fy + 62

    def rest():                                        # the lower lip showing under the moustache
        p.poly(curve([(fx - 15, my + 2), (fx, my + 1), (fx + 15, my + 3), (fx + 8, my + 10), (fx - 8, my + 10)], 3),
               (176, 112, 104), None)
        p.line([(fx - 16, my + 3), (fx, my + 1), (fx + 16, my + 4)], INK, 2.4)
    talk_or(p, sp, t, fx, my, rest)
    hair = [(hx - hw - 1, hy - 18), (hx - hw - 4, hy - hh * 0.6), (hx - hw * 0.72, hy - hh * 1.08), (hx, hy - hh * 1.18),
            (hx + hw * 0.72, hy - hh * 1.08), (hx + hw + 4, hy - hh * 0.6), (hx + hw + 1, hy - 18), (hx + hw - 7, hy - 24),
            (hx + hw * 0.78, hy - hh * 0.64), (hx + hw * 0.4, hy - hh * 0.74 + 26 * down), (hx + hw * 0.1, hy - hh * 0.68 + 26 * down),
            (hx - hw * 0.2, hy - hh * 0.76 + 26 * down), (hx - hw * 0.5, hy - hh * 0.7 + 26 * down),
            (hx - hw * 0.78, hy - hh * 0.64), (hx - hw + 7, hy - 24)]
    p.poly(curve(hair, 4), Z_HAIR, INK, 2.4)
    for k in range(9):                                 # short, textured, pushed forward
        x = hx - hw * 0.7 + k * hw * 0.17
        p.line([(x, hy - hh * 1.04), (x + 5, hy - hh * 0.86)], dk(Z_HAIR, 0.7), 1.3)
    return fx


def zelensky_torso(img, p, sp, t):
    """The sombre black military-style jacket over a black shirt: stand collar, chest pockets with flaps, buttons."""
    p.poly([(-44, -14), (44, -14), (48, 14), (-48, 14)], (40, 40, 44), INK, 2.2)          # the stand collar
    p.line([(-46, 0), (46, 0)], Z_SEAM, 1.2)
    p.line([(4, 14), (4, 470)], Z_SEAM, 1.6)                                             # the front opening
    for k in range(5):
        p.ell(14, 40 + 80 * k, 4, 4, (20, 20, 22), Z_SEAM, 1.0)
    for sgn in (-1, 1):
        x0, x1 = sgn * 30, sgn * 106
        p.poly([(x0, 92), (x1, 92), (x1, 182), (x0, 182)], Z_BLACK, Z_SEAM, 1.4)         # chest pockets
        p.poly([(x0 - sgn * 2, 82), (x1 + sgn * 2, 82), (x1 + sgn * 2, 108), (x0 - sgn * 2, 108)], (40, 40, 44), Z_SEAM, 1.4)
        p.line([(sgn * 70, 50), (sgn * 128, 40)], Z_SEAM, 1.2)                           # yoke seam


# --------------------------------------------------------------------------------------------- Claudia
C_SKIN = (242, 214, 198)
C_HAIR = (26, 24, 30)
C_SHEEN = (74, 76, 92)
C_LIP = (206, 146, 138)


def claudia_hair_back(p, sp, hx, hy, hw, hh):
    p.poly(curve([(hx - hw - 20, hy - 50), (hx - hw - 30, hy + 120), (hx - hw - 26, hy + 250), (hx + hw + 26, hy + 250),
                  (hx + hw + 30, hy + 120), (hx + hw + 20, hy - 50), (hx, hy - hh - 18)], 5), C_HAIR, INK, 2.6)


def claudia_head(img, p, sp, t, hx, hy):
    hw, hh, skin = 62, 88, C_SKIN
    turn = sp.get('turn', 0.0)
    fx = hx + turn * hw * 0.2
    fy = hy + 10 * sp.get('down', 0.0)
    outline = curve([(hx - hw, hy - 10), (hx - hw * 0.9, hy - hh * 0.7), (hx - hw * 0.45, hy - hh * 1.04),
                     (hx + hw * 0.45, hy - hh * 1.04), (hx + hw * 0.9, hy - hh * 0.7), (hx + hw, hy - 10),
                     (hx + hw * 0.96, hy + hh * 0.46), (hx + hw * 0.66, hy + hh * 0.92), (hx + hw * 0.24, hy + hh * 1.1),
                     (hx, hy + hh * 1.13), (hx - hw * 0.24, hy + hh * 1.1), (hx - hw * 0.66, hy + hh * 0.92),
                     (hx - hw * 0.96, hy + hh * 0.46)], 4)
    p.poly(outline, skin, INK, 2.6)
    st = dict(lid=sp.get('lid', 0.18), look=sp.get('look', 0.0), squint=0.0, closed=sp.get('blink', False),
              gaze_dy=sp.get('gaze_dy', 0.0))
    for sgn in (-1, 1):
        eye(p, fx + sgn * 27, fy - 4, sgn, 17, 9, (52, 40, 38), st, (150, 120, 124), liner=3.4, lower=2.2,
            lashes=True, smoky=(172, 142, 132))
    p.line([(fx - 2, fy), (fx - 5, fy + 26), (fx - 1, fy + 32), (fx + 6, fy + 30)], INK, 1.7)     # slim nose
    p.line([(fx - 10, fy + 29), (fx - 6, fy + 32)], INK, 1.3)
    for sgn in (-1, 1):
        p.line([(fx + sgn * 38, fy + 12), (fx + sgn * 34, fy + 34)], dk(skin, 0.9), 1.4)      # cheekbones
    my = fy + 55
    sp2 = dict(sp, lips=True, lip_c=C_LIP)

    def rest():                                        # nude lips, closed, the knowing half smile (one corner up)
        k = sp.get('smile', 0.6)
        top = curve([(fx - 21, my + 2), (fx - 8, my - 5), (fx, my - 3), (fx + 8, my - 5), (fx + 21, my + 2 - 4 * k),
                     (fx, my + 2)], 3)
        bot = curve([(fx - 21, my + 2), (fx, my + 2), (fx + 21, my + 2 - 4 * k), (fx + 10, my + 11), (fx, my + 12),
                     (fx - 10, my + 11)], 3)
        p.poly(top, dk(C_LIP, 0.9), INK, 1.6)
        p.poly(bot, C_LIP, INK, 1.6)
        p.line([(fx - 21, my + 2), (fx, my + 3), (fx + 21, my + 2 - 4 * k)], INK, 2.0)
    talk_or(p, sp2, t, fx, my, rest)
    # the heavy blunt fringe to just above the eyes (it hides her brows), the crown, and the long straight curtains
    # falling past her jaw and over the front of her shoulders (refs 3, 11)
    top = hy - hh - 20
    fr = fy - 22
    hair = [(hx - 46, hy + 300), (hx - hw - 44, hy + 300), (hx - hw - 34, hy + 160), (hx - hw - 24, hy + 30),
            (hx - hw - 18, hy - 50), (hx - hw - 12, top + 52), (hx - hw * 0.66, top + 8), (hx, top - 2),
            (hx + hw * 0.66, top + 8), (hx + hw + 12, top + 52), (hx + hw + 18, hy - 50), (hx + hw + 24, hy + 30), (hx + hw + 34, hy + 160),
            (hx + hw + 44, hy + 300), (hx + 46, hy + 300), (hx + hw * 0.62, hy + 150), (hx + hw * 0.9, hy + 70),
            (hx + hw * 0.95, fr + 8), (hx + hw * 0.6, fr), (hx + hw * 0.2, fr + 2), (hx - hw * 0.2, fr + 1),
            (hx - hw * 0.6, fr + 2), (hx - hw * 0.95, fr + 8), (hx - hw * 0.9, hy + 70), (hx - hw * 0.62, hy + 150)]
    p.poly(hair, C_HAIR, INK, 2.6)
    for k in range(8):                                 # the fringe's blunt ends, a few strands, a sheen across the crown
        x = hx - hw * 0.84 + k * hw * 0.24
        p.line([(x, fr - 34), (x + 2, fr - 2)], (50, 50, 60), 1.2)
    p.line(curve([(hx - hw * 0.7, top + 30), (hx, top + 20), (hx + hw * 0.7, top + 30), (hx, top + 24)], 4)[:12], C_SHEEN, 2.4)
    for sgn in (-1, 1):
        p.line([(hx + sgn * (hw + 10), hy - 30), (hx + sgn * (hw + 22), hy + 200)], C_SHEEN, 1.8)
        p.line([(hx + sgn * (hw - 2), hy + 90), (hx + sgn * (hw + 6), hy + 260)], (50, 50, 60), 1.2)
    return fx


def claudia_torso(img, p, sp, t):
    """White blouse buttoned to the throat, a black rose at the collar."""
    p.poly([(-30, -46), (30, -46), (40, 6), (24, 150), (0, 200), (-24, 150), (-40, 6)], (248, 248, 246), INK, 2.0)
    p.line([(-30, -30), (30, -30)], (210, 210, 210), 1.2)
    for sgn in (-1, 1):                                # the jacket's lapels over the blouse
        p.poly([(sgn * 40, -2), (sgn * 66, 30), (sgn * 46, 110), (sgn * 62, 150), (sgn * 6, 250), (sgn * 24, 150)],
               sp.get('jacket', (30, 28, 32)), INK, 2.2)
    x, y = 0, -24                                      # the rose: a dark spiral of petals
    p.ell(x, y, 22, 18, (22, 20, 24), INK, 2.0)
    for r, a in ((15, 0.3), (10, 2.1), (6, 4.0)):
        p.line(curve(oval(x, y, r, r * 0.8, 10), 3)[2:20], (74, 70, 80), 1.4)
    for sgn in (-1, 1):
        p.poly([(x + sgn * 12, y + 12), (x + sgn * 30, y + 34), (x + sgn * 8, y + 22)], (22, 20, 24), INK, 1.4)


def frill(p, j2, side):
    """A frilled white cuff where the sleeve ends, round the wrist."""
    el, wr = j2['el' + side], j2['wr' + side]
    d = (wr[0] - el[0], wr[1] - el[1])
    n = math.hypot(*d) or 1.0
    ux, uy = d[0] / n, d[1] / n
    for k in range(3):
        cx, cy = wr[0] - ux * (14 - 8 * k), wr[1] - uy * (14 - 8 * k)
        p.ell(cx, cy, 30 - 3 * k, 13, (250, 250, 248), INK, 1.4, rot=math.atan2(uy, ux) + math.pi / 2)
        p.line([(cx - uy * 20, cy + ux * 20), (cx - uy * 8, cy + ux * 6)], (214, 214, 214), 1.0)


# --------------------------------------------------------------------------------------------- the hooks
HEADS = {'trump': trump_head, 'putin': putin_head, 'zelensky': zelensky_head, 'claudia': claudia_head}
TORSOS = {'trump': trump_torso, 'putin': putin_torso, 'zelensky': zelensky_torso, 'claudia': claudia_torso}
_head, _torso, _hair_back = B.head, B.torso, B.hair_back


def head(img, p, sp, t, hx, hy):
    f = HEADS.get(sp.get('who'))
    return f(img, p, sp, t, hx, hy) if f else _head(img, p, sp, t, hx, hy)


def torso(img, p, sp, t):
    _torso(img, p, sp, t)
    f = TORSOS.get(sp.get('who'))
    if f:
        f(img, p, sp, t)


def hair_back(p, sp, hx, hy, hw, hh):
    if sp.get('who') == 'claudia':
        return claudia_hair_back(p, sp, hx, hy, hw, hh)
    if sp.get('who') in HEADS:
        return
    return _hair_back(p, sp, hx, hy, hw, hh)


B.head, B.torso, B.hair_back = head, torso, hair_back

TRUMP = dict(who='trump', name='Trump', skin=T_SKIN, hw=80, hh=92, head_dy=16, outfit='suit', jacket=(32, 40, 70),
             shirt=(246, 246, 244), tie=(196, 28, 40), shoulders=172, full=True, pose='custom')
PUTIN = dict(who='putin', name='Putin', skin=P_SKIN, hw=70, hh=88, head_dy=10, outfit='suit', jacket=(42, 46, 58),
             shirt=(246, 246, 244), tie=(34, 40, 74), shoulders=150, full=True, pose='custom')
ZELENSKY = dict(who='zelensky', name='Zelensky', skin=Z_SKIN, hw=70, hh=88, head_dy=10, outfit='jumper', jacket=Z_BLACK,
                shoulders=154, full=True, pose='custom')
CLAUDIA = dict(who='claudia', name='Claudia', skin=C_SKIN, hw=62, hh=88, head_dy=10, outfit='suit', jacket=(30, 28, 32),
               shirt=(248, 248, 246), shoulders=132, full=True, pose='custom')


# --------------------------------------------------------------------------------------------- the slate
LATIN = os.path.join(HERE, 'fonts', 'Caveat-Latin-Bold.woff')
CYRIL = os.path.join(HERE, 'fonts', 'Caveat-Cyrillic-Bold.woff')
_SLATES = {}


def slate_face(name, cyrillic=False, seed=0):
    """The chalk side of a slate, drawn once at high resolution (600 x 400): black board, the name in white chalk,
    a little uneven (each letter its own small tilt and drop), chalk dust in the strokes."""
    key = (name, cyrillic, seed)
    if key in _SLATES:
        return _SLATES[key]
    W_, H_ = 600, 400
    img = Image.new('RGBA', (W_, H_), (34, 36, 38, 255))
    d = ImageDraw.Draw(img)
    rng = np.random.default_rng(seed + 5)
    for _ in range(10):                                # faint old chalk smudges
        x, y = rng.uniform(0, W_), rng.uniform(0, H_)
        d.ellipse([x - 60, y - 10, x + 60, y + 10], fill=(40, 42, 44, 255))
    size = 170
    while True:                                        # the biggest writing that fits with a margin
        font = ImageFont.truetype(CYRIL if cyrillic else LATIN, size)
        adv = [font.getlength(c) for c in name]
        if sum(adv) <= W_ * 0.86 or size < 40:
            break
        size -= 6
    x = (W_ - sum(adv)) / 2
    for c, w in zip(name, adv):
        g = Image.new('L', (int(w) + 80, size + 120), 0)
        ImageDraw.Draw(g).text((40, 40), c, font=font, fill=255)
        g = g.rotate(rng.uniform(-6, 6), resample=Image.BICUBIC)
        dust = Image.fromarray((rng.random((g.height, g.width)) > 0.2).astype(np.uint8) * 255)
        g = ImageChops.multiply(g, dust)
        img.paste((236, 236, 230, 255), (int(x) - 40, int(H_ / 2 - size * 0.62 - 40 + rng.uniform(-8, 8))), g)
        x += w
    _SLATES[key] = img
    return img


def draw_slate(img, p, cx, cy, w, name, cyrillic=False, seed=0, stand=True, face_up=True):
    """A slate in its wooden stand, standing upright at (cx, cy) = the middle of its bottom edge, in p's units."""
    h = w * 2 / 3
    if stand:
        p.poly([(cx - w * 0.36, cy - 8), (cx + w * 0.36, cy - 8), (cx + w * 0.38, cy + 22), (cx - w * 0.38, cy + 22)],
               (196, 156, 104), INK, 2.0)
    if not face_up:                                    # lying flat, face down, on the table in front of them
        p.poly([(cx - w / 2 + 14, cy - 16), (cx + w / 2 - 14, cy - 16), (cx + w / 2, cy + 6), (cx - w / 2, cy + 6)],
               (34, 36, 38), INK, 2.0)
        p.poly([(cx - w / 2, cy + 6), (cx + w / 2, cy + 6), (cx + w / 2, cy + 12), (cx - w / 2, cy + 12)], (24, 24, 26), INK, 1.6)
        return
    q = [(cx - w / 2, cy - h), (cx + w / 2, cy - h), (cx + w / 2, cy), (cx - w / 2, cy)]
    if face_up:
        face = slate_face(name, cyrillic, seed)
        a, b = p.cam.P(*q[0]), p.cam.P(*q[2])
        sz = (max(1, int(b[0] - a[0])), max(1, int(b[1] - a[1])))
        img.alpha_composite(face.resize(sz, Image.LANCZOS), (int(a[0]), int(a[1])))
    else:
        p.poly(q, (34, 36, 38), None)
    p.poly(q, None, INK, 2.2)
    if stand:
        p.poly([(cx - w * 0.36, cy - 2), (cx + w * 0.36, cy - 2), (cx + w * 0.38, cy + 22), (cx - w * 0.38, cy + 22)],
               (196, 156, 104), INK, 2.0)
        f = ImageFont.truetype(B.ANTON, max(4, int(p.cam.S(13))))
        X, Y = p.cam.P(cx, cy + 3)
        ImageDraw.Draw(img).text((X, Y), 'THE TRAITORS', font=f, fill=(70, 46, 30), anchor='ma')


# --------------------------------------------------------------------------------------------- the blood
def spatter(seed=4, source=(-1.0, -0.35)):
    """Putin's blood as a list of shapes in his own units: a spray from one side (his left, our right), so drops
    are elongated along their flight with the tails behind them, the mist finer further from the side it came
    from, a few larger splashes with satellites, runs dripping down from the biggest under gravity, and his hands
    smeared. No pools, no wounds. Returns [(kind, points or circle, colour)]."""
    rng = np.random.default_rng(seed)
    fresh, dark = (150, 14, 20), (112, 10, 16)
    out = []
    dx, dy = source
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n                          # the direction the drops were travelling
    regions = [((-60, 80), (-230, -60), 1.0),        # the face and head (his left side, our right, more)
               ((-150, 150), (-40, 260), 1.4),       # shirt, tie, lapels, shoulders
               ((-170, 170), (-80, 60), 0.6)]        # collar and shoulders
    for (x0, x1), (y0, y1), dens in regions:
        for _ in range(int(420 * dens)):
            x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
            side = (x - x0) / (x1 - x0)            # 0 his right (our left) .. 1 his left (our right): denser there
            if rng.random() > 0.35 + 0.65 * side:
                continue
            r = rng.choice([0.8, 1.2, 1.7, 2.4, 3.4, 4.6], p=[0.36, 0.26, 0.18, 0.11, 0.06, 0.03])
            if y < -60:                                # the face: a lighter, finer spray (half the dots)
                if r < 1.5 and rng.random() < 0.5:
                    continue
                r = min(r, 2.4)
                if abs(y + 148) < 14 and (abs(x - 29) < 22 or abs(x + 29) < 22):
                    continue                           # keep the eyes clear
            c = fresh if rng.random() < 0.6 else dark
            if r < 2.0:
                out.append(('dot', (x, y, r), c))
                continue
            L = r * rng.uniform(2.2, 3.6)          # a teardrop: round head, tapering tail behind it
            pts = []
            for a in np.linspace(-math.pi / 2, math.pi / 2, 9):
                pts.append((x + ux * r * math.cos(a) - uy * r * math.sin(a) * -1, y + uy * r * math.cos(a) + ux * r * math.sin(a) * -1))
            pts.append((x - ux * L, y - uy * L))
            out.append(('poly', pts, c))
    for cx, cy, big in [(52, -112, 6), (40, -196, 5), (-20, -92, 4), (62, -170, 4), (50, 120, 12), (-40, 60, 9),
                        (90, 30, 10), (120, 180, 9), (-100, 140, 8), (20, 220, 10), (70, -60, 6)]:
        blob = [(cx + big * (0.8 + 0.4 * rng.random()) * math.cos(a), cy + big * (0.8 + 0.4 * rng.random()) * math.sin(a))
                for a in np.linspace(0, 2 * math.pi, 14, endpoint=False)]
        out.append(('poly', blob, fresh))
        for _ in range(8):                         # satellites thrown out round the splash
            a = rng.uniform(0, 2 * math.pi)
            d = big * rng.uniform(1.5, 2.8)
            out.append(('dot', (cx + d * math.cos(a), cy + d * math.sin(a), rng.uniform(1.0, 2.6)), fresh))
        if big >= 6:                               # a run, dripping straight down
            L = big * rng.uniform(3.0, 5.5)
            w = big * 0.32
            out.append(('poly', [(cx - w, cy), (cx + w, cy), (cx + w * 0.7, cy + L), (cx, cy + L + w * 1.6),
                                 (cx - w * 0.7, cy + L)], dark))
    return out


def hand_smears(wrists, seed=9):
    """Blood on his hands: irregular smears over most of each hand and up the cuff."""
    rng = np.random.default_rng(seed)
    out = []
    for (x, y) in wrists:
        for _ in range(4):
            cx, cy = x + rng.uniform(-14, 14), y + rng.uniform(-10, 18)
            r = rng.uniform(8, 16)
            out.append(('poly', [(cx + r * (0.6 + 0.6 * rng.random()) * math.cos(a), cy + r * (0.6 + 0.6 * rng.random()) * math.sin(a))
                                 for a in np.linspace(0, 2 * math.pi, 12, endpoint=False)], (128, 12, 18)))
    return out


def bloody(img, cam, x, y, s, draw_person, shapes):
    """Draw a person, then lay the blood over them only (multiplied, so it reads wet and dark on the navy suit and
    bright on the shirt and skin; it never spills off their outline)."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw_person(lay)
    bl = Image.new('RGBA', img.size, (255, 255, 255, 0))
    p = B.Pen(bl, B.Local(cam, x, y, s))
    for kind, g, c in shapes:
        if kind == 'dot':
            p.ell(g[0], g[1], g[2], g[2], c, None, n=10)
        else:
            p.poly(g, c, None)
    a = np.asarray(bl.split()[3], np.float32) / 255 * (np.asarray(lay.split()[3], np.float32) / 255)
    base = np.asarray(lay, np.float32)
    col = np.asarray(bl, np.float32)[..., :3]
    mult = base[..., :3] * col / 255
    base[..., :3] = base[..., :3] * (1 - a[..., None]) + mult * a[..., None]
    img.alpha_composite(Image.fromarray(base.astype(np.uint8), 'RGBA'))


# --------------------------------------------------------------------------------------------- the table
WOOD = (176, 100, 52)
WOOD_D = (128, 70, 36)
BORDER = (36, 64, 68)
STAR_GOLD = (204, 166, 82)
RING = (250, 244, 226)


def table_far(img, p, x0, x1, y_edge, seed=0):
    """The Round Table seen across its top towards a player's place (refs 5, 9, 34): from the player's edge
    (y_edge) towards us, the gilded rim, the blue-green border with gold stars, the lit ring with its white plate,
    then the polished wood. Flat colour, one outline."""
    p.poly([(x0, y_edge - 4), (x1, y_edge - 4), (x1, y_edge + 6), (x0, y_edge + 6)], STAR_GOLD, INK, 2.0)
    p.poly([(x0, y_edge + 6), (x1, y_edge + 6), (x1, y_edge + 70), (x0, y_edge + 70)], BORDER, INK, 2.0)
    rng = np.random.default_rng(seed)
    x = x0 + 30 + rng.uniform(0, 40)
    while x < x1 - 20:                                 # gold stars in the border, eight points
        cy = y_edge + 38
        pts = []
        for k in range(16):
            r = 13 if k % 2 == 0 else 5
            a = k * math.pi / 8
            pts.append((x + r * math.cos(a), cy + r * 0.55 * math.sin(a)))
        p.poly(pts, STAR_GOLD, None)
        x += 110
    p.poly([(x0, y_edge + 70), (x1, y_edge + 70), (x1, y_edge + 82), (x0, y_edge + 82)], RING, INK, 1.6)
    p.poly([(x0, y_edge + 82), (x1, y_edge + 82), (x1, y_edge + 400), (x0, y_edge + 400)], WOOD, INK, 2.0)
    for k in range(4):                                 # the grain, long and faint
        y = y_edge + 120 + 60 * k
        p.line([(x0, y), (x1, y + 6)], blend(WOOD, WOOD_D, 0.4), 1.4)


def plate(p, x, y, r=34):
    """One of the lit white plates set into the ring (refs 1, 4): a white disc in a dark rim."""
    p.ell(x, y, r + 6, (r + 6) * 0.42, (60, 50, 44), INK, 1.8)
    p.ell(x, y, r, r * 0.4, RING, None)


def goblet(p, x, y, h=150):
    """A cut-crystal goblet standing at (x, y) = its foot: patterned bowl, short stem, round foot (refs 28-34)."""
    gl, gd = (222, 228, 230), (178, 190, 196)
    p.ell(x, y, h * 0.24, h * 0.06, gl, INK, 1.6)                                    # the foot
    p.poly([(x - h * 0.05, y - 2), (x + h * 0.05, y - 2), (x + h * 0.06, y - h * 0.32), (x - h * 0.06, y - h * 0.32)],
           gl, INK, 1.6)                                                              # the stem
    p.ell(x, y - h * 0.3, h * 0.1, h * 0.04, gd, INK, 1.4)
    bowl = curve([(x - h * 0.27, y - h), (x + h * 0.27, y - h), (x + h * 0.25, y - h * 0.62), (x + h * 0.12, y - h * 0.36),
                  (x - h * 0.12, y - h * 0.36), (x - h * 0.25, y - h * 0.62)], 3)
    p.poly(bowl, gl, INK, 1.8)
    p.poly(curve([(x - h * 0.25, y - h * 0.8), (x + h * 0.25, y - h * 0.8), (x + h * 0.22, y - h * 0.6),
                  (x + h * 0.1, y - h * 0.4), (x - h * 0.1, y - h * 0.4), (x - h * 0.22, y - h * 0.6)], 3), (206, 220, 226), None)
    for k in range(5):                                 # the cut pattern: crossing diagonals
        u = -0.2 + 0.1 * k
        p.line([(x + h * u, y - h * 0.94), (x + h * (u + 0.1), y - h * 0.48)], gd, 1.1)
        p.line([(x + h * (u + 0.1), y - h * 0.94), (x + h * u, y - h * 0.48)], gd, 1.1)
    p.ell(x, y - h, h * 0.27, h * 0.06, (236, 240, 242), INK, 1.6)
