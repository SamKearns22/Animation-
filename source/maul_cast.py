#!/usr/bin/env python3
"""Darth Maul, satire parody in the house style (Sam, 26 Oct), from Sam's six photos (references/maul/maul-1-hooded-
desert, -2-full-costume, -3-attack, -4-hooded-staff, -5-hood-face, -6-face). Drawn fresh in our flat cartoon look,
never traced from the photos (like Andrew the Hutt: evoked, not copied).

What the photos show, and how he is built (guides/satire.md, 'Likeness method'):
  head      bald, a ring of short pale horns round the crown (two small ones at the front, longer ones at the
            sides); pointed ears; a long face, high cheekbones, a narrow chin
  paint     red skin, black markings: a black mask round both eyes sweeping up to the temples, a black stripe
            down the middle of the forehead, flame stripes up the forehead, black cheek stripes, a black nose tip,
            black lips, a black chin with two red stripes down it
  eyes      yellow, an orange-red ring round the pupil, red rims; no eyebrows (the paint makes the glare)
  clothes   all black: a heavy hooded cloak (hood up or down), a wrap-over tunic, a wide black sash belt with a
            strap, pleated robe skirts to the shins, black gloves and boots
  weapon    the double-bladed red lightsaber (a 'saberstaff'): a long silver-black hilt held in the middle, a red
            blade from each end; either blade can be off (ref 1: one lit)
Exaggerated (caricature): the glare, the horns, the bared teeth when he snarls.

House style: the blades are flat (red edge, white core, inked), no glow (satire.md: 'no glows'); the Poker Mon soft
glow is Sam's exception and is not used unless he asks.

Moods (sp['mood']): 'neutral' (the cold glare), 'snarl' (teeth bared, ref 3), 'talk' via sp['mouth'] = 'v:SHAPE'.
sp['hood']: True for the hood up. Poses: pose(name) returns the joints with the saberstaff in hand.

    python3 source/maul_cast.py sheet OUT.jpg       every view hood down and up, the action poses, the faces
    python3 source/maul_cast.py face OUT.png        his face straight on, for compare.py beside maul-6-face.jpg
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import shocking_cast as SC       # noqa: E402  (shared mouths)
import views as V                # noqa: E402
from traitors_cast import clip_convex, ears   # noqa: E402
from ed import INK, curve, open_curve, oval   # noqa: E402

M_SKIN = (200, 44, 38)
M_PAINT = (26, 18, 20)                 # the black markings (a touch warmer than the ink)
M_EYE = (246, 196, 52)                 # yellow eyes
M_IRIS = (232, 108, 26)                # the orange-red ring
M_RIM = (150, 24, 24)
M_HORN = (222, 204, 158)
M_HORN_D = (150, 120, 84)
M_TEETH = (226, 214, 180)
CLOAK = (34, 32, 37)
CLOAK_D = (18, 16, 20)
TUNIC = (46, 44, 50)
SASH = (56, 52, 58)
BLADE = (232, 30, 44)
CORE = (255, 236, 236)
HILT = (64, 64, 72)
SILVER = (196, 198, 206)

HILT_M, BLADE_M = 0.56, 0.65           # the saberstaff: hilt length, each blade (sizes.py 'saberstaff')
U = V.M_PER_UNIT


def _stripe(p, pts, w, c=M_PAINT):
    p.line(open_curve(pts, 5), c, w)


def _horns(p, base_pts):
    """Short pale horns: each (x, y, angle in radians pointing out from the skull, length)."""
    for x, y, a, ln in base_pts:
        dx, dy = math.cos(a), math.sin(a)
        nx, ny = -dy, dx
        w = 4 + ln * 0.24
        tip = (x + dx * ln, y + dy * ln)
        p.poly(curve([(x + nx * w, y + ny * w), (x + dx * ln * 0.55 + nx * w * 0.5, y + dy * ln * 0.55 + ny * w * 0.5),
                      tip, (x + dx * ln * 0.55 - nx * w * 0.5, y + dy * ln * 0.55 - ny * w * 0.5),
                      (x - nx * w, y - ny * w), (x - dx * 3, y - dy * 3)], 3), M_HORN, INK, 2.0)
        p.line([(x + nx * w * 0.9, y + ny * w * 0.9), (x - nx * w * 0.9, y - ny * w * 0.9)], M_HORN_D, 2.2)   # the root


def _eye(p, ex, ey, sgn, w, h, lid, glare, look=0.0, gaze_dy=0.0, closed=False):
    """His yellow eye: the inner end of the upper lid pulled down by `glare` (no brows: the lid makes the scowl).
    look (-1 .. 1 across, screen right +) and gaze_dy (down +) move the iris; closed draws the shut lid (a blink)."""
    us = np.linspace(-1, 1, 15)
    if closed:
        p.line([(ex + w * u, ey + 1 + h * 0.4 * (1 - u * u) + glare * h * 0.3 * (1 - sgn * u) / 2) for u in us], INK, 2.8)
        return
    up = [(ex + w * u, ey - h * (1 - u * u) * (1 - lid) + glare * h * 0.55 * (1 - sgn * u) / 2) for u in us]
    lo = [(ex + w * u, ey + h * 0.75 * (1 - u * u)) for u in us]
    opening = up + lo[::-1][1:-1]
    p.poly(opening, M_EYE, None)
    cx, cy = ex + look * w * 0.4, ey + 1 + gaze_dy
    circ = lambda r: [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 22, endpoint=False)]
    ring = clip_convex(opening[::-1], circ(h * 0.72))
    if len(ring) >= 3:
        p.poly(ring, M_IRIS, None)
    pu = clip_convex(opening[::-1], circ(h * 0.3))
    if len(pu) >= 3:
        p.poly(pu, INK, None)
    p.line(lo, M_RIM, 2.0)
    p.line(up, INK, 2.8)


def _outline(hx, hy, hw, hh):
    return curve([(hx - hw, hy - 12), (hx - hw * 0.92, hy - hh * 0.7), (hx - hw * 0.5, hy - hh * 1.04),
                  (hx + hw * 0.5, hy - hh * 1.04), (hx + hw * 0.92, hy - hh * 0.7), (hx + hw, hy - 12),
                  (hx + hw * 0.98, hy + hh * 0.3), (hx + hw * 0.78, hy + hh * 0.78), (hx + hw * 0.36, hy + hh * 1.12),
                  (hx, hy + hh * 1.18), (hx - hw * 0.36, hy + hh * 1.12), (hx - hw * 0.78, hy + hh * 0.78),
                  (hx - hw * 0.98, hy + hh * 0.3)], 4)          # long, high cheekbones, a narrow chin


def _pointed_ears(p, hx, hy, hw, skin, sides=(-1, 1), at=None):
    for sgn in sides:
        x = at if at is not None else hx + sgn * (hw + 2)
        p.poly(curve([(x - sgn * 4, hy - 14), (x + sgn * 10, hy - 30), (x + sgn * 14, hy - 4), (x + sgn * 10, hy + 22),
                      (x - sgn * 2, hy + 30)], 3), skin, INK, 2.4)                       # a point at the top
        p.line([(x + sgn * 3, hy - 12), (x + sgn * 8, hy + 2), (x + sgn * 3, hy + 16)], B.dk(skin, 0.72), 1.6)


def maul_head(img, p, sp, t, hx, hy):
    hw, hh, skin = sp.get('hw', 68), sp.get('hh', 96), sp['skin']
    fx = hx + sp.get('turn', 0.0) * hw * 0.2
    fy = hy + 10 * sp.get('down', 0.0)
    mood = sp.get('mood', 'neutral')
    _pointed_ears(p, hx, hy + 8, hw, skin)
    outline = _outline(hx, hy, hw, hh)
    p.poly(outline, skin, INK, 2.6)
    # the markings (black on red), drawn before the eyes, nose and mouth
    top = hy - hh * 1.02
    p.poly([(fx - 9, top + 4), (fx + 9, top + 4), (fx + 6, fy - 24), (fx - 6, fy - 24)], M_PAINT, None)   # forehead stripe
    for sgn in (-1, 1):
        mask = curve([(fx + sgn * 6, fy - 22), (fx + sgn * 22, fy - 30), (fx + sgn * 40, fy - 46),
                      (fx + sgn * 50, fy - 62), (fx + sgn * 60, fy - 40), (fx + sgn * 62, fy - 12),
                      (fx + sgn * 52, fy + 14), (fx + sgn * 30, fy + 20), (fx + sgn * 12, fy + 12)], 3)
        p.poly(mask, M_PAINT, None)                                                      # the eye mask to the temple
        _stripe(p, [(fx + sgn * 16, fy - 40), (fx + sgn * 22, fy - 66), (fx + sgn * 16, hy - hh * 0.9)], 9)   # flames
        _stripe(p, [(fx + sgn * 34, fy - 58), (fx + sgn * 44, hy - hh * 0.78), (fx + sgn * 40, top + 14)], 8)
        _stripe(p, [(fx + sgn * 38, fy + 22), (fx + sgn * 50, fy + 46), (fx + sgn * 54, fy + 70),
                    (fx + sgn * 44, fy + 86)], 10)                                       # cheek stripes
        _stripe(p, [(fx + sgn * 14, fy + 44), (fx + sgn * 26, fy + 60), (fx + sgn * 28, fy + 84)], 7)   # round the mouth
        _stripe(p, [(hx + sgn * hw * 0.98, hy - 4), (hx + sgn * hw * 0.96, hy + hh * 0.3)], 8)     # by the ear
    chin = curve([(fx - 30, fy + 84), (fx, fy + 80), (fx + 30, fy + 84), (hx + hw * 0.36, hy + hh * 1.1),
                  (hx, hy + hh * 1.16), (hx - hw * 0.36, hy + hh * 1.1)], 3)
    p.poly(chin, M_PAINT, None)                                                          # the black chin
    for sgn in (-1, 1):
        p.poly([(fx + sgn * 6, fy + 90), (fx + sgn * 14, fy + 90), (fx + sgn * 12, hy + hh * 1.08),
                (fx + sgn * 6, hy + hh * 1.08)], skin, None)                             # its two red stripes
    # eyes: no brows, the lids glare
    lid = 0.3 if mood != 'snarl' else 0.38
    glare = 0.55 if mood in ('neutral', 'snarl') else 0.3
    for sgn in (-1, 1):
        _eye(p, fx + sgn * 27, fy - 10, sgn, 15, 8.5, lid, glare, sp.get('look', 0.0), sp.get('gaze_dy', 0.0),
             sp.get('blink', False))
    # nose: a red bridge, the black tip and nostrils
    p.line([(fx - 4, fy - 8), (fx - 7, fy + 28)], INK, 1.8)
    p.poly(curve([(fx - 14, fy + 32), (fx - 6, fy + 26), (fx + 6, fy + 26), (fx + 14, fy + 32), (fx + 8, fy + 42),
                  (fx - 8, fy + 42)], 3), M_PAINT, INK, 1.8)
    my = fy + 62
    if mood == 'snarl' and not SC.talking(sp):                       # ref 3: teeth bared, lips pulled back
        shape = curve([(fx - 30, my - 2), (fx - 10, my - 8), (fx + 10, my - 8), (fx + 30, my - 2), (fx + 18, my + 14),
                       (fx, my + 18), (fx - 18, my + 14)], 3)
        p.poly(shape, SC.MOUTH_IN, M_PAINT, 4.0)
        p.poly(curve([(fx - 24, my - 2), (fx, my - 6), (fx + 24, my - 2), (fx, my + 4)], 3), M_TEETH, None)
        p.poly(curve([(fx - 16, my + 11), (fx, my + 7), (fx + 16, my + 11), (fx, my + 15)], 3), M_TEETH, None)
        for k in (-12, -4, 4, 12):
            p.line([(fx + k, my - 4), (fx + k, my + 2)], B.dk(M_TEETH, 0.7), 1.2)
        p.line(shape, INK, 2.0)
    elif SC.talking(sp):
        SC.mouth_or_talk(p, sp, fx, my, M_PAINT, width=26, lips=True)
    else:                                                            # black lips, pressed thin
        p.poly(curve([(fx - 24, my + 1), (fx, my - 5), (fx + 24, my + 1), (fx, my + 9)], 3), M_PAINT, None)
        p.line(open_curve([(fx - 26, my + 2), (fx - 8, my), (fx + 8, my), (fx + 26, my + 2)], 4), INK, 2.2)
    p.poly(outline, None, INK, 2.6)
    if not sp.get('hood'):
        horns = []                                                   # out of the skull's edge, never on the brow
        for u, v, a, ln in ((0.26, 1.03, 0.15, 24), (0.66, 0.92, 0.7, 28), (0.94, 0.62, 1.15, 22)):
            for sgn in (-1, 1):
                horns.append((hx + sgn * hw * u, hy - hh * v, -math.pi / 2 + sgn * a, ln))
        _horns(p, horns)
    return fx


# ------------------------------------------------------------------------------------------------ the hood
def hood_back(p, view, hx, hy, hw, hh):
    """The hood's back and inside, behind the head (drawn first)."""
    if view in ('back', 'three_back'):
        return
    if view == 'front':
        p.poly(curve([(hx - hw - 46, hy + 150), (hx - hw - 40, hy - 40), (hx - hw * 0.7, hy - hh - 40), (hx, hy - hh - 52),
                      (hx + hw * 0.7, hy - hh - 40), (hx + hw + 40, hy - 40), (hx + hw + 46, hy + 150)], 4), CLOAK_D, INK, 2.6)
    else:
        sh = 0.0 if view == 'side' else 18
        p.poly(curve([(hx - hw - 30, hy + 150), (hx - hw - 44, hy - 30), (hx - 20, hy - hh - 50), (hx + 50 + sh, hy - hh - 30),
                      (hx + 76 + sh, hy - 10), (hx + 60 + sh, hy + 150)], 4), CLOAK_D, INK, 2.6)


def hood_front(p, view, hx, hy, hw, hh):
    """The hood over the head: an arch round the face (its opening frames the face), its sides down to the
    shoulders. From behind it covers the whole head."""
    if view == 'front':
        shape = [(hx - hw - 52, hy + 156), (hx - hw - 44, hy - 30), (hx - hw * 0.72, hy - hh - 36), (hx, hy - hh - 48),
                 (hx + hw * 0.72, hy - hh - 36), (hx + hw + 44, hy - 30), (hx + hw + 52, hy + 156), (hx + hw + 4, hy + 150),
                 (hx + hw * 0.9, hy + hh * 0.5), (hx + hw * 0.96, hy - 20), (hx + hw * 0.66, hy - hh * 0.62),
                 (hx, hy - hh * 0.72), (hx - hw * 0.66, hy - hh * 0.62), (hx - hw * 0.96, hy - 20),
                 (hx - hw * 0.9, hy + hh * 0.5), (hx - hw - 4, hy + 150)]
        p.poly(curve(shape, 3), CLOAK, INK, 2.6)
        p.line(open_curve([(hx - hw * 0.9, hy - hh * 0.62), (hx, hy - hh * 0.86), (hx + hw * 0.9, hy - hh * 0.62)], 4),
               CLOAK_D, 2.0)                                                  # a fold over the brow
        for sgn in (-1, 1):
            p.line(open_curve([(hx + sgn * (hw + 30), hy - 10), (hx + sgn * (hw + 26), hy + 80), (hx + sgn * (hw + 36), hy + 140)], 4),
                   CLOAK_D, 2.0)
    elif view in ('three', 'side'):
        sh = 0.0 if view == 'side' else 18
        fr = hx + (34 if view == 'side' else 20)
        shape = [(hx - hw - 34, hy + 156), (hx - hw - 48, hy - 30), (hx - 22, hy - hh - 54), (hx + 46 + sh, hy - hh - 34),
                 (hx + 70 + sh, hy - hh * 0.5), (fr + 22, hy - hh * 0.62), (fr - 4, hy - hh * 0.5), (fr - 22, hy - 10),
                 (fr - 34, hy + 70), (fr - 26, hy + 150)]
        p.poly(curve(shape, 3), CLOAK, INK, 2.6)
        p.line(open_curve([(hx - hw - 20, hy - 40), (hx - 30, hy - hh - 20), (hx + 40 + sh, hy - hh - 10)], 4), CLOAK_D, 2.0)
        p.line(open_curve([(hx - hw - 20, hy + 20), (hx - 40, hy + 100), (hx - 40, hy + 150)], 4), CLOAK_D, 2.0)
    else:
        p.poly(curve([(hx - hw - 52, hy + 156), (hx - hw - 44, hy - 30), (hx - hw * 0.72, hy - hh - 36), (hx, hy - hh - 50),
                      (hx + hw * 0.72, hy - hh - 36), (hx + hw + 44, hy - 30), (hx + hw + 52, hy + 156)], 4), CLOAK, INK, 2.6)
        p.line(open_curve([(hx, hy - hh - 40), (hx + 6, hy - 10), (hx, hy + 140)], 4), CLOAK_D, 2.4)       # the seam
        for sgn in (-1, 1):
            p.line(open_curve([(hx + sgn * 50, hy - hh), (hx + sgn * 70, hy), (hx + sgn * 76, hy + 140)], 4), CLOAK_D, 2.0)


# ------------------------------------------------------------------------------------------------ other views
def maul_head_view(img, p, sp, t, view, hx, hy):
    """Three-quarter, side and back: his own heads (bald and painted; horns round the crown)."""
    hw, hh, skin = sp.get('hw', 68), sp.get('hh', 96), sp['skin']
    hood = sp.get('hood')
    if view in ('three', 'side'):
        if view == 'three':
            fx = hx + 0.4 * hw
            outline = curve([(hx - hw, hy - 10), (hx - hw * 0.88, hy - hh * 0.72), (hx - hw * 0.3, hy - hh * 1.04),
                             (hx + hw * 0.45, hy - hh * 1.0), (hx + hw * 0.92, hy - hh * 0.62), (hx + hw * 1.0, hy - 6),
                             (hx + hw * 0.94, hy + hh * 0.4), (hx + hw * 0.66, hy + hh * 0.86), (hx + hw * 0.3, hy + hh * 1.16),
                             (hx - hw * 0.2, hy + hh * 1.06), (hx - hw * 0.72, hy + hh * 0.66), (hx - hw * 0.96, hy + hh * 0.3)], 4)
            ear_x = hx - 0.5 * hw
            eyes = ((fx - 24, 1.0), (fx + 26, 0.62))
            ey = hy - 10
            nose = [(fx + 2, hy - 8), (fx + 24, hy + 30), (fx + 12, hy + 38)]
            mx, my = fx + 4, hy + 62
        else:
            outline = curve([(hx - 62, hy - 70), (hx - 40, hy - hh - 4), (hx + 20, hy - hh - 2), (hx + 58, hy - 56),
                             (hx + 64, hy - 22), (hx + 62, hy - 4), (hx + 84, hy + 30), (hx + 64, hy + 38), (hx + 66, hy + 52),
                             (hx + 60, hy + 62), (hx + 62, hy + 78), (hx + 46, hy + 108), (hx + 14, hy + 112),
                             (hx - 22, hy + 88), (hx - 60, hy + 40)], 3)
            ear_x = hx - 18
            eyes = ((hx + 44, 0.62),)
            ey = hy - 10
            nose = None
            fx, mx, my = hx + 40, hx + 52, hy + 60
        p.poly(outline, skin, INK, 2.6)
        _pointed_ears(p, hx, hy + 8, hw, skin, sides=(-1,), at=ear_x + 8)
        # markings: the mask round the eyes, forehead stripes, cheek stripe, the chin
        edge = hx + hw * 0.86 if view == 'three' else hx + 60
        for ex, w in eyes:
            pts = [(ex - 22 * w, ey + 2), (ex - 14 * w, ey - 22), (ex + 4 * w, ey - 30), (ex + 24 * w, ey - 50),
                   (ex + 30 * w, ey - 20), (ex + 22 * w, ey + 14), (ex - 10 * w, ey + 18)]
            p.poly(curve([(min(x, edge), y) for x, y in pts], 3), M_PAINT, None)   # kept inside the face's edge
        if view == 'three':
            p.poly([(fx - 9, hy - hh * 0.98), (fx + 7, hy - hh * 0.98), (fx + 4, ey - 22), (fx - 6, ey - 22)], M_PAINT, None)
            for sx in (-1, 1):
                _stripe(p, [(fx + sx * 18 - 2, ey - 38), (fx + sx * 22, hy - hh * 0.62), (fx + sx * 18, hy - hh * 0.92)], 8)
            for ex, w in eyes:
                _stripe(p, [(ex - 8 * w, ey + 30), (ex - 2 * w, ey + 56), (ex - 10 * w, ey + 84)], 9 * w + 1)
        else:
            _stripe(p, [(hx + 30, hy - 40), (hx + 26, hy - 70), (hx + 18, hy - hh + 4)], 8)
            _stripe(p, [(hx + 30, hy + 20), (hx + 36, hy + 50), (hx + 28, hy + 80)], 9)
            _stripe(p, [(hx - 46, hy - 40), (hx - 52, hy - 70)], 8)
        chin_pts = ([(fx - 24, hy + 84), (fx + 12, hy + 80), (hx + hw * 0.36, hy + hh * 1.06), (hx + hw * 0.1, hy + hh * 1.12),
                     (hx - hw * 0.16, hy + hh * 1.0)]
                    if view == 'three' else [(hx + 34, hy + 76), (hx + 62, hy + 76), (hx + 46, hy + 106), (hx + 16, hy + 108)])
        p.poly(curve(chin_pts, 3), M_PAINT, None)
        for ex, w in eyes:
            us = np.linspace(-1, 1, 11)
            up = [(ex + 14 * w * u, ey - 7 * (1 - u * u) + 3.5 * (1 + u)) for u in us]
            lo = [(ex + 14 * w * u, ey + 6 * (1 - u * u)) for u in us]
            p.poly(up + lo[::-1][1:-1], M_EYE, None)
            p.ell(ex + 4 * w, ey + 1, 4.5 * w, 4.5, M_IRIS, None)
            p.ell(ex + 4 * w, ey + 1, 2.0 * w, 2.0, INK, None)
            p.line(lo, M_RIM, 1.8)
            p.line(up, INK, 2.4)
        if nose:
            p.line(nose, INK, 2.0)
            p.ell(fx + 14, hy + 34, 9, 6, M_PAINT, None)
        else:
            p.poly([(hx + 76, hy + 26), (hx + 86, hy + 30), (hx + 66, hy + 38)], M_PAINT, None)
        mood = sp.get('mood', 'neutral')
        if mood == 'snarl' and not SC.talking(sp):
            p.poly(curve([(mx - 16, my - 3), (mx, my - 7), (mx + 14, my - 4), (mx + 8, my + 9), (mx - 10, my + 8)], 3),
                   M_TEETH, M_PAINT, 4.0)
            p.line([(mx - 14, my + 2), (mx + 12, my + 1)], B.dk(M_TEETH, 0.6), 1.4)
        elif SC.talking(sp) and sp['mouth'][2:] not in ('rest', 'MBP'):
            p.poly([(mx - 10, my - 6), (mx + 12, my - 6), (mx + 10, my + 10), (mx - 8, my + 10)], SC.MOUTH_IN, M_PAINT, 4.0)
        else:
            p.line([(mx - 14, my), (mx + 12, my - 1)], M_PAINT, 6)
        p.poly(outline, None, INK, 2.6)
        if not hood:                                     # horns round the crown, seen from the side
            top = [(hx - 0.86 * hw, hy - hh * 0.72, 3.6, 30), (hx - 0.5 * hw, hy - hh * 0.98, 4.2, 28),
                   (hx - 0.08 * hw, hy - hh * 1.06, 4.55, 22), (hx + 0.3 * hw, hy - hh * 1.04, 4.85, 16),
                   (hx + 0.62 * hw, hy - hh * 0.86, 5.2, 12)] if view == 'three' else \
                  [(hx - 54, hy - 70, 3.7, 30), (hx - 34, hy - hh - 2, 4.3, 26), (hx - 4, hy - hh - 4, 4.6, 22),
                   (hx + 24, hy - hh - 2, 4.9, 16)]
            _horns(p, top)
    else:                                                # from behind: the painted back of the skull, a ring of horns
        bt = 0.6 if view == 'three_back' else 0.0
        if not hood:
            for side in (-1, 1):
                if not (side > 0 and bt > 0):
                    _pointed_ears(p, hx, hy + 8, hw, skin, sides=(side,))
            outline = curve([(hx - hw, hy - 10), (hx - hw * 0.86, hy - hh * 0.72), (hx, hy - hh * 1.06), (hx + hw * 0.86, hy - hh * 0.72),
                             (hx + hw, hy - 10), (hx + hw * 0.92, hy + hh * 0.42), (hx + hw * 0.66, hy + hh * 0.72), (hx, hy + hh * 0.8),
                             (hx - hw * 0.66, hy + hh * 0.72), (hx - hw * 0.92, hy + hh * 0.42)], 4)
            p.poly(outline, skin, INK, 2.6)
            nw = 32.0
            p.poly([(hx - nw, hy + hh * 0.55), (hx + nw, hy + hh * 0.55), (hx + nw, hy + 132), (hx - nw, hy + 132)], skin, None)
            for sg in (-1, 1):
                p.line([(hx + sg * nw, hy + hh * 0.66), (hx + sg * nw, hy + 132)], INK, 2.6)
            for sg in (-1, 1):                           # the paint's stripes over the scalp
                _stripe(p, [(hx + sg * 14, hy - hh * 0.96), (hx + sg * 30, hy - hh * 0.4), (hx + sg * 22, hy + hh * 0.3)], 9)
                _stripe(p, [(hx + sg * hw * 0.6, hy - hh * 0.76), (hx + sg * hw * 0.8, hy - 6), (hx + sg * hw * 0.62, hy + hh * 0.5)], 8)
            p.poly(outline, None, INK, 2.6)
            if bt > 0:
                _pointed_ears(p, hx, hy + 8, hw, skin, sides=(1,), at=hx + hw * (1 - 0.42 * bt))
            hn = []
            for k, u in enumerate(np.linspace(-0.9, 0.9, 7)):
                a = -math.pi / 2 + u * 1.2
                hn.append((hx + hw * 0.86 * math.sin(u * 1.2), hy - hh * (0.2 + 0.84 * math.cos(u * 1.1)), a, 18 + 10 * abs(u)))
            _horns(p, hn)
    if hood:
        hood_front(p, view, hx, hy, hw, hh)


# --------------------------------------------------------------------------------------------- the robes
def robe_front(img, p, sp):
    sw, bottom = sp.get('shoulders', 150), sp.get('bottom', 860)
    flare = sw * 1.18
    p.poly(curve([(-sw - 14, 20), (-sw - 30, 300), (-flare - 20, bottom + 10), (flare + 20, bottom + 10), (sw + 30, 300),
                  (sw + 14, 20)], 3), CLOAK_D, INK, 2.6)                       # the cloak's back, seen past him
    p.poly([(-32, -80), (32, -80), (36, 10), (-36, 10)], sp['skin'], INK, 2.6)  # the neck
    body = [(-40, -4), (-sw * 0.8, 12), (-sw, 50), (-sw - 6, 200), (-sw * B.HEM, 300), (-flare, bottom), (flare, bottom),
            (sw * B.HEM, 300), (sw + 6, 200), (sw, 50), (sw * 0.8, 12), (40, -4)]
    p.poly(body, TUNIC, INK, 2.6)
    p.poly([(-46, -6), (8, 120), (-6, 136), (-62, 4)], B.dk(TUNIC, 0.7), INK, 2.0)   # the wrap-over collar
    p.poly([(46, -6), (-20, 150), (-30, 140), (30, -8)], B.dk(TUNIC, 0.82), INK, 2.0)
    p.poly(curve([(-42, -30), (42, -30), (48, 6), (0, 16), (-48, 6)], 3), B.dk(TUNIC, 0.7), INK, 2.2)   # a high collar (ref 6)
    for k, x in enumerate(np.linspace(-flare * 0.8, flare * 0.8, 7)):        # the skirt's pleats
        p.line([(x * 0.55, 340), (x, bottom - 10)], B.dk(TUNIC, 0.66), 2.0)
    p.poly([(-sw * 0.38, 330), (sw * 0.38, 330), (sw * 0.42, 700), (-sw * 0.42, 700)], B.dk(TUNIC, 0.86), INK, 2.0)  # the tabard
    for sgn in (-1, 1):                                                       # the cloak's front edges over the shoulders
        p.poly(curve([(sgn * 50, -6), (sgn * (sw * 0.8), 10), (sgn * (sw + 18), 60), (sgn * (sw + 24), 300),
                      (sgn * (flare + 22), bottom + 10), (sgn * (flare - 30), bottom + 10), (sgn * (sw * 0.78), 320),
                      (sgn * (sw * 0.7), 120), (sgn * 70, 20)], 3), CLOAK, INK, 2.4)
        p.line(open_curve([(sgn * (sw * 0.86), 200), (sgn * (sw * 0.96), 500), (sgn * flare, bottom - 20)], 4), CLOAK_D, 2.0)
    sash = [(-sw - 2, 244), (sw + 2, 244), (sw * B.HEM + 6, 330), (-sw * B.HEM - 6, 330)]
    p.poly(sash, SASH, INK, 2.4)
    for y in (266, 290, 312):
        p.line([(-sw * 0.92, y), (sw * 0.92, y + 2)], B.dk(SASH, 0.7), 1.6)
    p.poly([(-sw - 2, 278), (sw + 2, 278), (sw + 2, 292), (-sw - 2, 292)], CLOAK_D, INK, 1.6)     # the strap over it


def robe_view(img, p, sp, view):
    """The sash, the cloak's edges and pleats over the plain long torso of the other views."""
    sw, bottom = sp.get('shoulders', 150), sp.get('bottom', 860)
    if view == 'three':
        x0, x1 = -sw * 0.97, sw * 0.84
    elif view == 'side':
        x0, x1 = -0.6 * sw * 1.0, 0.6 * sw * 1.1
    else:
        k = 0.9 if view == 'three_back' else 1.0
        x0, x1 = -(sw + 6) * k, (sw + 6) * k
    cx0, cx1 = {'three': (-34, 50), 'side': (-32, 36)}.get(view, (-42, 42))
    p.poly(curve([(cx0, -34), (cx1, -34), (cx1 + 6, 6), (cx0 - 6, 6)], 3), B.dk(TUNIC, 0.7), INK, 2.2)   # the high collar
    p.poly([(x0, 244), (x1, 244), (x1 * 0.9, 330), (x0 * 0.9, 330)], SASH, INK, 2.4)
    p.poly([(x0, 278), (x1, 278), (x1, 292), (x0, 292)], CLOAK_D, INK, 1.6)
    for x in np.linspace(x0 * 0.8, x1 * 0.8, 6):
        p.line([(x * 0.9, 350), (x * 1.08, bottom - 10)], B.dk(sp.get('jacket', CLOAK), 0.6), 2.0)
    if view in ('three', 'side'):                         # the cloak's front edge down his side
        e = x1 * (0.5 if view == 'three' else 0.8)
        p.line(open_curve([(e, 20), (e * 1.05, 300), (e * 1.15, bottom - 6)], 4), CLOAK_D, 2.4)
    if view in ('back', 'three_back') and not sp.get('hood'):
        p.poly(curve([(-sw * 0.8, -6), (sw * 0.8, -6), (sw * 0.7, 60), (0, 90), (-sw * 0.7, 60)], 3), CLOAK, INK, 2.2)  # hood down


# --------------------------------------------------------------------------------------------- the hooks
_head, _torso, _head_view, _torso_view = B.head, B.torso, V.head_view, V.torso_view


def head(img, p, sp, t, hx, hy):
    if sp.get('who') == 'maul':
        return maul_head(img, p, sp, t, hx, hy)
    return _head(img, p, sp, t, hx, hy)


def torso(img, p, sp, t):
    if sp.get('who') == 'maul':
        return robe_front(img, p, sp)
    _torso(img, p, sp, t)


def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
    if sp.get('who') != 'maul':
        return _head_view(img, p, sp, t, view, hx, hy)
    hw, hh = sp.get('hw', 68), sp.get('hh', 96)
    if sp.get('hood'):
        hood_back(p, view, hx, hy, hw, hh)
    if view == 'front':
        maul_head(img, p, sp, t, hx, hy)
        if sp.get('hood'):
            hood_front(p, view, hx, hy, hw, hh)
        return
    maul_head_view(img, p, sp, t, view, hx, hy)


def torso_view(img, p, sp, view, seated=False):
    _torso_view(img, p, sp, view, seated)
    if sp.get('who') == 'maul':
        robe_view(img, p, sp, view)


B.head, B.torso, V.head_view, V.torso_view = head, torso, head_view, torso_view

MAUL = dict(who='maul', name='Maul', skin=M_SKIN, hw=68, hh=96, head_dy=8, hair='bald', hair_c=M_SKIN, outfit='robe',
            jacket=CLOAK, sleeve=CLOAK, glove=(30, 28, 32), trousers=CLOAK_D, shoe=(16, 14, 16), shoulders=150,
            bottom=860, full=True, pose='custom', height=1.75)             # Ray Park, who played him: 1.75 m
MAUL_HOOD = dict(MAUL, hood=True)
CAST = {'maul': MAUL}


# --------------------------------------------------------------------------------------------- the saberstaff
def saberstaff(side='R', aim3=(0.0, -1.0, 0.0), lit=(True, True)):
    """The double-bladed lightsaber held in the middle by one hand. `aim3`: where the first blade points in his own
    3D frame (x across, y down, z forward), so it turns and shortens with him. lit: (first blade, second blade)."""
    import prepper_cast as PC

    def draw(p, j2):
        c, d, _ = PC._one_hand(j2, side)
        d, keep = PC._screen_dir(j2, aim3)
        keep = max(keep, 0.25)
        nx, ny = -d[1], d[0]

        def P(u, v):
            return (c[0] + d[0] * u * keep + nx * v, c[1] + d[1] * u * keep + ny * v)
        h, bl = HILT_M / 2 / U, BLADE_M / U
        for sgn, on in ((1, lit[0]), (-1, lit[1])):
            if not on:
                continue
            u0, u1 = sgn * h, sgn * (h + bl)
            p.poly(curve([P(u0, -19), P(u1 - sgn * 14, -19), P(u1, 0), P(u1 - sgn * 14, 19), P(u0, 19)], 2), BLADE, INK, 2.2)
            p.poly(curve([P(u0, -8), P(u1 - sgn * 22, -8), P(u1 - sgn * 12, 0), P(u1 - sgn * 22, 8), P(u0, 8)], 2), CORE, None)
        p.poly([P(-h, -11), P(h, -11), P(h, 11), P(-h, 11)], HILT, INK, 2.2)
        for sgn in (-1, 1):
            p.poly([P(sgn * h, -14), P(sgn * (h - 22), -14), P(sgn * (h - 22), 14), P(sgn * h, 14)], SILVER, INK, 2.0)  # emitters
            for k in range(3):                                                                              # ridges
                u = sgn * (h - 44 - 20 * k)
                p.line([P(u, -11), P(u, 11)], SILVER, 3)
            p.poly([P(sgn * 16, -12), P(sgn * 60, -12), P(sgn * 60, 12), P(sgn * 16, 12)], (24, 24, 28), INK, 1.6)  # grips
        p.ell(*P(0, 0), 7, 7, SILVER, INK, 1.4)                                                             # the join
    draw.held = True
    draw.rear_under = True                                # from behind: drawn before his back (views)
    return draw


def pose(name, sp=MAUL):
    """His poses, saberstaff in hand. 'stand': relaxed, one blade lit, pointing at the ground by his side (ref 1);
    'present': the staff upright at his side, both lit (ref 2); 'attack': a low lunge, the staff level (ref 3);
    'strike': the staff raised high and back for a downward cut."""
    sw = sp.get('shoulders', 150)
    j = V.standing(sp)
    if name == 'stand':
        V.arm_to(j, 'R', (sw + 40, 400.0, 110.0), 'back', 'fist')
        j['props'] = [saberstaff('R', (0.5, 1.0, 0.45), (True, False))]
    elif name == 'present':
        V.arm_to(j, 'L', (-(sw + 30), 300.0, 90.0), 'back', 'fist')
        j['props'] = [saberstaff('L', (0.0, -1.0, 0.0))]
    elif name == 'attack':
        drop = 70.0
        j['bob'] = drop
        j['footR'] = (110.0, V.ANKLE_Y - drop, 170.0)
        j['footL'] = (-120.0, V.ANKLE_Y - drop, -150.0)
        j['toeL'] = 18
        j['lean'] = 16                                    # the robe's hem rises as he leans in (house rule)
        V.arm_to(j, 'R', (90.0, 150.0, 300.0), 'out', 'fist')
        V.arm_to(j, 'L', (-(sw + 120), 120.0, -80.0), 'down', 'palm')
        j['props'] = [saberstaff('R', (0.95, 0.05, -0.3))]
    elif name == 'strike':
        j['footR'] = (90.0, V.ANKLE_Y, 90.0)
        j['footL'] = (-90.0, V.ANKLE_Y, -60.0)
        j['lean'] = -6
        V.arm_to(j, 'R', (60.0, -300.0, -30.0), 'up', 'fist')
        V.arm_to(j, 'L', (-(sw + 60), 300.0, 80.0), 'back', 'fist')
        j['props'] = [saberstaff('R', (0.7, -0.6, -0.35))]
    else:
        raise ValueError(name)
    j['grip'] = {'R'} if name != 'present' else {'L'}
    return j


# --------------------------------------------------------------------------------------------- the sheet
def sheet(out):
    """Every view hood down and hood up, the four action poses, his faces large, and a 1.75 m person for scale."""
    import landmarks
    import sizes
    B.SS = 1
    W, H = 2560, 2860
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 40)
    small = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 26)
    cam = B.Cam(1.0, 540, 960)

    def tile(draw, box, at):
        lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        draw(lay)
        img.alpha_composite(lay.crop(box), at)

    d.text((40, 24), 'MAUL (satire parody, from Sam\'s six photos): every view, hood down and up', font=big,
           fill=(30, 30, 30))
    names = ('front', 'three-quarter', 'side', '3/4 back', 'back')
    s = 0.6
    for row, sp in enumerate((MAUL, MAUL_HOOD)):
        y0 = 90 + 860 * row
        for i, yaw in enumerate((0, 45, 90, 135, 180)):
            tile(lambda im, yaw=yaw, sp=sp: V.person(im, cam, 540, 330, s, dict(sp), 0.0, yaw), (320, 120, 760, 950),
                 (20 + 420 * i, y0))
            d.text((240 + 420 * i, y0 + 830), names[i] + (' (hood up)' if row else ''), font=small, fill=(40, 40, 40),
                   anchor='mm')
    lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    landmarks.draw(ld, 540, 330, s, 1000)
    sizes.scale_ref(ld, 640, 330 + 928 * s, s / U)
    img.alpha_composite(lay.crop((450, 120, 870, 950)), (2120, 90))
    d.text((2330, 920), '1.75 m person', font=small, fill=(40, 40, 40), anchor='mm')
    y0 = 1820
    acts = (('stand', MAUL_HOOD, 0, 'standing, one blade lit (ref 1)'), ('present', MAUL, 0, 'staff upright (ref 2)'),
            ('attack', MAUL, 45, 'attack: lunge (ref 3)'), ('strike', MAUL, 90, 'strike: raised to cut'))
    s2 = 0.42
    for i, (nm, sp, yaw, label) in enumerate(acts):
        tile(lambda im, nm=nm, sp=sp, yaw=yaw: V.person(im, cam, 540, 700, s2, dict(sp), 0.0, yaw, pose(nm, sp)),
             (240, 330, 860, 1180), (10 + 640 * i, y0 - 10))
        d.text((320 + 640 * i, y0 + 845), label, font=small, fill=(40, 40, 40), anchor='mm')
    img.convert('RGB').save(out, quality=90)
    return out


def faces(out):
    """His faces large: the glare, the snarl, talking, the glare under the hood, and three-quarter."""
    B.SS = 1
    W, H = 2560, 900
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    small = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 26)
    cam = B.Cam(1.0, 540, 960)
    rows = ((MAUL, 'neutral', 'rest', 0, 'the glare'), (MAUL, 'snarl', 'rest', 0, 'snarl (ref 3)'),
            (MAUL, 'neutral', 'v:AI', 0, 'talking'), (MAUL_HOOD, 'neutral', 'rest', 0, 'hood up (ref 5)'),
            (MAUL, 'snarl', 'rest', 45, 'three-quarter, snarl'))
    for i, (base, mood, mouth, yaw, label) in enumerate(rows):
        sp = dict(base, mood=mood, mouth=mouth)
        lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        V.person(lay, cam, 540, 900, 1.5, sp, 0.0, yaw)
        img.alpha_composite(lay.crop((300, 400, 780, 1220)).resize((420, 718)), (40 + 505 * i, 40))
        d.text((250 + 505 * i, 820), label, font=small, fill=(40, 40, 40), anchor='mm')
    img.convert('RGB').save(out, quality=90)
    return out


def face_png(out, sp=None):
    """His head and shoulders alone, straight on, for compare.py beside the face photo."""
    B.SS = 1
    im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    V.person(im, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(sp or MAUL), 0.0, 0)
    im.crop((240, 380, 840, 1200)).save(out)
    return out


cast_sheet = sheet


def LINE_SUBJECTS():
    return [('maul', lambda im: V.person(im, B.Cam(1.0, 540, 960), 540, 420, 1.45, dict(MAUL), 0.0, 0))]


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    elif sys.argv[1] == 'faces':
        print(faces(sys.argv[2]))
    elif sys.argv[1] == 'face':
        print(face_png(sys.argv[2]))
