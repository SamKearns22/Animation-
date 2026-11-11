#!/usr/bin/env python3
"""trial_lineup: the five of Remakes' line-up shot (S10) as Glimpses, built for budget trial 2 (notes/trial_lineup.md).
Young Zelda, Malon, Saria, Princess Ruto and a Goron in a frilly dress: ONE view (front), ONE pose each and one small
reaction on "ROMANCE" (react=1). Judged only in the line-up frame at phone size and its 2x crop.

MAP
  colours ............ top, one block per character
  faces .............. MOODS (idle, react per character), _eye (iris colour, lashes, wink), _mouth (smile, beam,
                       smirk, smug + trial_link's)
  heads .............. child_head (shared face) + hair_zelda, hair_malon, hair_saria; ruto_head; back hair and the
                       veil drawn behind the body (back_hair, a 'pre')
  bodies ............. body_zelda, body_malon, body_saria, body_ruto (body_props, the torso's own frame)
  props .............. ocarina_blue, ocarina_wood, milk_bottle (held: the hands are drawn over them)
  arms, legs ......... arm, leg: hooks on views for the four children (sleeves, fins, shorts, boots, bare feet)
  poses .............. pose(who, react)
  the Goron .......... goron(img, cam, x, floor, k, react): drawn whole in its own units (no views.person)
  person ............. person(img, cam, who, x, floor, s, react): s the scale of a 1.75 m adult; heights from HEIGHTS
  the frame .......... lineup(react, scale): 1080 x 1920 (scale 2: 2160 x 3840), the flat backdrop and ground line
  sheets ............. frame(out), crop(out), compare(out, real)

    python3 source/trial_lineup.py frame OUT.png [idle]     (phone-size frame, on "ROMANCE" unless idle)
    python3 source/trial_lineup.py crop OUT.png              (the 2x crop of the same frame)
    python3 source/trial_lineup.py spec R                    (renders both into source/data/trial_lineup/ and writes
                                                              the critique SPEC for hunt R; prints its path)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import trial_link as TL          # noqa: E402  (installs Link's hooks; ours chain onto them)
import kit                       # noqa: E402
from trial_link import B, V, INK, curve, oval, lerp   # noqa: E402

FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
dk = B.dk

# ------------------------------------------------------------------------------------------------ colours
SKIN = (248, 214, 180)
BLUSH = (240, 150, 140)
# Zelda (10 MAIN, 09)
Z_HAIR, Z_IRIS = (232, 196, 110), (70, 160, 120)
VEIL, Z_PURPLE, Z_PURPLE_D = (246, 244, 238), (128, 70, 150), (92, 46, 112)
GOLD, GOLD_D = (220, 178, 70), (160, 120, 40)
Z_BLUE, DRESS_W = (150, 178, 222), (244, 242, 236)
OCARINA_B = (60, 104, 190)
# Malon (14 right half MAIN, 13)
M_HAIR, M_HAIR_D, M_HAIR_L = (222, 104, 48), (170, 70, 32), (240, 142, 80)
M_IRIS = (60, 110, 200)
M_BLOUSE, M_SLEEVE = (176, 160, 140), (70, 104, 176)
M_SCARF, M_BROOCH = (238, 196, 60), (150, 70, 50)
M_APRON, M_APRON_L = (128, 84, 52), (168, 120, 78)
M_SKIRT, M_HEM = (138, 96, 168), (74, 104, 180)
BELT, BELT_D = (110, 70, 40), (78, 48, 26)
MILK, MILK_CAP = (250, 250, 246), (90, 140, 210)
# Saria (16 MAIN, 15)
S_HAIR, S_HAIR_D, S_HAIR_L = (164, 214, 60), (112, 160, 34), (200, 236, 110)
S_IRIS = (60, 116, 200)
S_DARK, S_TUNIC, S_TUNIC_L = (52, 92, 46), (96, 150, 64), (132, 182, 92)
PENDANT, BEAD = (220, 110, 50), (200, 60, 46)
WOOD, BOOT = (196, 150, 96), (110, 74, 44)
# Ruto (08 MAIN, 07)
R_SKIN, R_SKIN_D = (228, 234, 230), (190, 202, 198)
FIN, FIN_D, FIN_L = (70, 186, 170), (40, 130, 124), (150, 224, 210)
R_IRIS, TOES = (140, 90, 190), (240, 170, 176)
# the Goron (11, 12 MAIN face)
G_SKIN, G_SKIN_D, G_SKIN_L = (246, 178, 60), (214, 140, 40), (252, 206, 110)
G_EYE, ROCK, ROCK_D, TUFT = (78, 36, 96), (150, 140, 132), (110, 102, 96), (226, 234, 240)
FRILL, FRILL_D, FRILL_L, LACE = (244, 140, 186), (206, 96, 146), (250, 186, 214), (252, 246, 250)
DROOL = (210, 236, 250)

HEIGHTS = dict(zelda=1.36, malon=1.27, saria=1.31, ruto=1.38, goron=2.13)   # tops of everything, metres (Link 1.33)
MINE = ('zelda', 'malon', 'saria', 'ruto')


# ------------------------------------------------------------------------------------------------ faces
# brows (inner_dy, outer_dy) per side (negative = up), lid, look (-1 .. 1 across), mouth, plus: wink, blush, nod, roll
MOODS = {
    ('zelda', 0): dict(brows=((-18, -2), (-18, -2)), lid=0.0, look=-0.55, gaze_dy=0.3, mouth='unsure', blush=0.3),
    ('zelda', 1): dict(brows=((-26, -6), (-26, -6)), lid=0.0, look=0.15, mouth='unsure', blush=0.8),
    ('malon', 0): dict(brows=((-8, -4), (-8, -4)), lid=0.04, mouth='smile', blush=0.35),
    ('malon', 1): dict(brows=((-18, -12), (-18, -12)), lid=0.0, scale=1.06, mouth='beam', blush=0.6),
    ('saria', 0): dict(brows=((4, -6), (-6, -12)), lid=0.12, look=0.1, mouth='smirk', blush=0.25),
    ('saria', 1): dict(brows=((4, -6), (-8, -16)), lid=0.1, look=0.0, mouth='smirk_big', wink='R', blush=0.4),
    ('ruto', 0): dict(brows=((2, -22), (2, -22)), lid=0.3, look=0.7, mouth='smug', blush=0.3),
    ('ruto', 1): dict(brows=((0, -26), (0, -26)), lid=0.3, look=0.0, mouth='smug_big', wink='both', blush=0.5),
}


def _eye(p, ex, ey, w, h, m, sg, skin, iris, lashes=True):
    """trial_link's big eye in this character's iris colour; girls' lashes; a wink is a happy closed arc."""
    if m.get('wink') in ('both', 'R' if sg > 0 else 'L'):
        p.line(curve([(ex - w * 1.0, ey + 4), (ex, ey - h * 0.55), (ex + w * 1.0, ey + 4)], 3), INK, 4.0)
        tip = (ex + sg * w * 1.0, ey + 4)
        p.line([tip, (tip[0] + sg * 10, tip[1] - 4)], INK, 3.0)
        return
    TL.IRIS, TL.IRIS_D = iris, dk(iris, 0.6)
    TL._eye(p, ex, ey, w, h, m, sg, skin)
    if lashes:                                            # two lash flicks at the outer top corner
        lid = m.get('lid', 0.0)
        for k, (dx, dy) in enumerate(((0.78, -0.62), (0.96, -0.3))):
            x0, y0 = ex + sg * w * dx, ey - h * (-dy) * (1 - lid) * 1.0
            y0 = ey + dy * h * (1 - lid)
            p.line([(x0, y0), (x0 + sg * 11, y0 - 8 + 3 * k)], INK, 2.6)


DARK, TEETH, TONGUE = TL.DARK, TL.TEETH, TL.TONGUE


def _mouth(p, sp, fx, my, m):
    name = m.get('mouth', 'rest')
    if name == 'smile':                                   # kind: a soft closed smile, corners up
        p.line(curve([(fx - 17, my - 4), (fx - 8, my + 4), (fx, my + 6), (fx + 8, my + 4), (fx + 17, my - 4)], 3),
               INK, 2.8)
    elif name == 'beam':                                  # eager: an open D-shaped smile, top teeth, tongue
        o = curve([(fx - 22, my - 4), (fx, my - 1), (fx + 22, my - 4), (fx + 14, my + 14), (fx, my + 20),
                   (fx - 14, my + 14)], 3)
        p.poly(o, DARK, INK, 2.6)
        p.poly([(fx - 15, my - 2), (fx + 15, my - 2), (fx + 13, my + 4), (fx - 13, my + 4)], TEETH, None)
        p.poly(oval(fx, my + 16, 9, 5, 16), TONGUE, None)
        p.poly(o, None, INK, 2.6)
    elif name in ('smirk', 'smirk_big'):                  # sure of herself: one corner hooked up
        big = name == 'smirk_big'
        p.line(curve([(fx - 14, my + 2), (fx - 2, my + 5), (fx + 10, my + 1), (fx + 18, my - (10 if big else 6))], 3),
               INK, 2.8)
        p.line([(fx + 18, my - (10 if big else 6)), (fx + 21, my - (4 if big else 2))], INK, 2.0)
    elif name in ('smug', 'smug_big'):                    # pleased with herself: tight, both corners tucked up high
        k = 1.3 if name == 'smug_big' else 1.0
        p.line(curve([(fx - 16 * k, my - 6 * k), (fx - 6, my + 3), (fx + 6, my + 3), (fx + 16 * k, my - 6 * k)], 3),
               INK, 3.0)
        for sg in (-1, 1):
            p.line([(fx + sg * 16 * k, my - 6 * k), (fx + sg * 20 * k, my - 3 * k)], INK, 2.0)
    else:
        TL._mouth(p, sp, fx, my, m)


def _face(p, sp, hx, hy, skin=None, chin=1.0):
    """The child's face shape (trial_link's): round, full cheeks, a small chin."""
    hw, hh = sp['hw'], sp['hh']
    skin = skin or sp['skin']
    face = curve([(hx - hw * 0.98, hy - hh * 0.1), (hx - hw * 0.9, hy - hh * 0.68), (hx - hw * 0.5, hy - hh * 0.98),
                  (hx, hy - hh * 1.04), (hx + hw * 0.5, hy - hh * 0.98), (hx + hw * 0.9, hy - hh * 0.68),
                  (hx + hw * 0.98, hy - hh * 0.1), (hx + hw * 0.96, hy + hh * 0.34), (hx + hw * 0.76 * chin, hy + hh * 0.72),
                  (hx + hw * 0.4 * chin, hy + hh * 0.96), (hx, hy + hh * 1.02), (hx - hw * 0.4 * chin, hy + hh * 0.96),
                  (hx - hw * 0.76 * chin, hy + hh * 0.72), (hx - hw * 0.96, hy + hh * 0.34)], 4)
    p.poly(face, skin, INK, 2.6)
    return face


def _features(p, sp, hx, hy, m, iris, brow_c, skin=None, eye_k=1.0):
    hw, hh = sp['hw'], sp['hh']
    skin = skin or sp['skin']
    fx = hx
    bl = m.get('blush', 0.3)
    for sg in (-1, 1):
        p.ell(fx + sg * hw * 0.6, hy + hh * 0.52, hw * 0.17, hh * 0.08, lerp(skin, BLUSH, bl * 0.75), None)
    sc = m.get('scale', 1.0) * eye_k
    ew, eh = hw * 0.26 * sc, hw * 0.30 * sc
    ey = hy + hh * 0.16
    for sg in (-1, 1):
        _eye(p, fx + sg * hw * 0.42, ey, ew, eh, m, sg, skin, iris)
    (il, ol), (ir, orr) = m['brows']
    TL._brow(p, fx - hw * 0.42, ey - eh - 14, -1, il, ol, c=brow_c, w=5.4)
    TL._brow(p, fx + hw * 0.42, ey - eh - 14, 1, ir, orr, c=brow_c, w=5.4)
    ny = hy + hh * 0.5
    p.line([(fx - 2, ny - 5), (fx + 4, ny), (fx - 1, ny + 3)], dk(skin, 0.72), 2.0)
    _mouth(p, sp, fx, hy + hh * 0.73, m)


def _ears(p, sp, hx, hy, skin=None):
    """Long pointed Hylian ears, out to the sides and a little up."""
    hw, hh = sp['hw'], sp['hh']
    skin = skin or sp['skin']
    for sg in (-1, 1):
        ear = curve([(hx + sg * hw * 0.96, hy - hh * 0.02), (hx + sg * hw * 1.3, hy - hh * 0.12),
                     (hx + sg * hw * 1.6, hy - hh * 0.3), (hx + sg * hw * 1.38, hy + hh * 0.08),
                     (hx + sg * hw * 1.1, hy + hh * 0.3), (hx + sg * hw * 0.98, hy + hh * 0.3)], 3)
        p.poly(ear, skin, INK, 2.6)
        p.line([(hx + sg * hw * 1.1, hy + hh * 0.14), (hx + sg * hw * 1.34, hy - hh * 0.06),
                (hx + sg * hw * 1.48, hy - hh * 0.2)], lerp(skin, BLUSH, 0.6), 2.4)


# ------------------------------------------------------------------------------------------------ hair and headwear
def _strands(p, pts, c, w=1.6):
    for a, b in pts:
        p.line([a, b], c, w)


def hair_zelda(p, sp, hx, hy):
    """Blond fringe swept to one side under a white cloth veil and a purple padded headband with a gold plate (10)."""
    hw, hh = sp['hw'], sp['hh']
    # the veil's sides falling past the jaw (front parts; the back hangs behind the body: back_hair)
    for sg in (-1, 1):
        side = curve([(hx + sg * hw * 0.86, hy - hh * 0.8), (hx + sg * hw * 1.14, hy - hh * 0.5),
                      (hx + sg * hw * 1.2, hy + hh * 0.3), (hx + sg * hw * 1.28, hy + hh * 1.2),
                      (hx + sg * hw * 0.98, hy + hh * 1.26), (hx + sg * hw * 0.9, hy + hh * 0.2),
                      (hx + sg * hw * 0.84, hy - hh * 0.3)], 3)
        p.poly(side, VEIL, INK, 2.4)
        p.line([(hx + sg * hw * 1.06, hy - hh * 0.1), (hx + sg * hw * 1.12, hy + hh * 1.0)], dk(VEIL, 0.85), 1.6)
    # the fringe: soft, swept to screen right, a few points over the brow
    fr = [(hx - hw * 0.92, hy - hh * 0.3), (hx - hw * 0.9, hy - hh * 0.62), (hx - hw * 0.3, hy - hh * 0.78),
          (hx + hw * 0.5, hy - hh * 0.74), (hx + hw * 0.92, hy - hh * 0.5), (hx + hw * 0.94, hy - hh * 0.08),
          (hx + hw * 0.66, hy - hh * 0.3), (hx + hw * 0.4, hy - hh * 0.22), (hx + hw * 0.1, hy - hh * 0.42),
          (hx - hw * 0.2, hy - hh * 0.3), (hx - hw * 0.5, hy - hh * 0.44), (hx - hw * 0.76, hy - hh * 0.16)]
    p.poly(curve(fr, 3), Z_HAIR, INK, 2.4)
    _strands(p, [((hx - hw * 0.4, hy - hh * 0.66), (hx - hw * 0.5, hy - hh * 0.46)),
                 ((hx + hw * 0.2, hy - hh * 0.66), (hx + hw * 0.4, hy - hh * 0.3))], dk(Z_HAIR, 0.75))
    # the veil over the crown
    crown = curve([(hx - hw * 1.12, hy - hh * 0.5), (hx - hw * 1.0, hy - hh * 1.06), (hx - hw * 0.4, hy - hh * 1.32),
                   (hx + hw * 0.4, hy - hh * 1.32), (hx + hw * 1.0, hy - hh * 1.06), (hx + hw * 1.12, hy - hh * 0.5),
                   (hx + hw * 0.9, hy - hh * 0.66), (hx, hy - hh * 0.86), (hx - hw * 0.9, hy - hh * 0.66)], 3)
    p.poly(crown, VEIL, INK, 2.4)
    # the purple padded headband, a gold edge, the gold plate with the triangle mark
    top = [(hx - hw * 1.08, hy - hh * 0.62), (hx - hw * 0.5, hy - hh * 0.92), (hx, hy - hh * 0.98),
           (hx + hw * 0.5, hy - hh * 0.92), (hx + hw * 1.08, hy - hh * 0.62)]
    bt = curve(top, 3)[:-8]
    bb = [(x, y + 22) for x, y in bt]
    p.poly(bt + bb[::-1], Z_PURPLE, INK, 2.4)
    p.line(bb, GOLD, 2.4)
    for i in range(2, len(bt) - 2, 4):
        x, y = bt[i]
        p.line([(x, y + 3), (x, y + 19)], Z_PURPLE_D, 1.6)
    px, py = hx, hy - hh * 0.98 + 10
    p.poly([(px - 26, py - 12), (px + 26, py - 12), (px + 30, py + 14), (px - 30, py + 14)], GOLD, INK, 2.2)
    p.poly([(px, py - 8), (px + 10, py + 9), (px - 10, py + 9)], GOLD_D, None)


def hair_malon(p, sp, hx, hy):
    """Long red-orange hair, a soft side-swept fringe, locks falling down past the jaw onto the shoulders (14)."""
    hw, hh = sp['hw'], sp['hh']
    top = hy - hh * 1.16
    for sg in (-1, 1):                                    # the front locks: over the shoulders to the chest
        lock = curve([(hx + sg * hw * 0.98, hy - hh * 0.4), (hx + sg * hw * 1.18, hy + hh * 0.3),
                      (hx + sg * hw * 1.24, hy + hh * 1.3), (hx + sg * hw * 1.3, hy + hh * 2.5),
                      (hx + sg * hw * 1.0, hy + hh * 2.4), (hx + sg * hw * 0.94, hy + hh * 1.3),
                      (hx + sg * hw * 0.86, hy + hh * 0.4)], 3)
        p.poly(lock, M_HAIR, INK, 2.4)
        p.line([(hx + sg * hw * 1.06, hy + hh * 0.2), (hx + sg * hw * 1.12, hy + hh * 2.2)], M_HAIR_D, 1.8)
    cap = curve([(hx - hw * 1.04, hy - hh * 0.1), (hx - hw * 1.08, hy - hh * 0.7), (hx - hw * 0.6, top + 8), (hx, top),
                 (hx + hw * 0.6, top + 8), (hx + hw * 1.08, hy - hh * 0.7), (hx + hw * 1.04, hy - hh * 0.1),
                 (hx + hw * 0.84, hy - hh * 0.3), (hx + hw * 0.56, hy - hh * 0.36),       # the fringe, swept to
                 (hx + hw * 0.2, hy - hh * 0.5), (hx - hw * 0.2, hy - hh * 0.56),       # screen left, a part at
                 (hx - hw * 0.5, hy - hh * 0.38), (hx - hw * 0.84, hy - hh * 0.3)], 3)  # screen right
    p.poly(cap, M_HAIR, INK, 2.4)
    _strands(p, [((hx + hw * 0.36, top + 14), (hx + hw * 0.1, hy - hh * 0.56)),
                 ((hx + hw * 0.36, top + 14), (hx + hw * 0.7, hy - hh * 0.4)),
                 ((hx - hw * 0.3, top + 30), (hx - hw * 0.66, hy - hh * 0.4))], M_HAIR_D, 1.8)
    p.line([(hx - hw * 0.6, hy - hh * 0.86), (hx - hw * 0.86, hy - hh * 0.5)], M_HAIR_L, 2.4)


def hair_saria(p, sp, hx, hy):
    """A bright lime bob: a full straight-ish fringe, the ends flipped out at the jaw (16)."""
    hw, hh = sp['hw'], sp['hh']
    top = hy - hh * 1.2
    bob = curve([(hx - hw * 1.36, hy + hh * 0.66), (hx - hw * 1.06, hy + hh * 0.5), (hx - hw * 1.14, hy - hh * 0.3),
                 (hx - hw * 1.0, hy - hh * 0.86), (hx - hw * 0.5, top + 6), (hx, top), (hx + hw * 0.5, top + 6),
                 (hx + hw * 1.0, hy - hh * 0.86), (hx + hw * 1.14, hy - hh * 0.3), (hx + hw * 1.06, hy + hh * 0.5),
                 (hx + hw * 1.36, hy + hh * 0.66), (hx + hw * 1.1, hy + hh * 0.72), (hx + hw * 0.9, hy + hh * 0.5),
                 (hx + hw * 0.86, hy - hh * 0.2),
                 (hx + hw * 0.7, hy - hh * 0.3), (hx + hw * 0.5, hy - hh * 0.22), (hx + hw * 0.28, hy - hh * 0.34),
                 (hx, hy - hh * 0.24), (hx - hw * 0.28, hy - hh * 0.34), (hx - hw * 0.5, hy - hh * 0.22),
                 (hx - hw * 0.7, hy - hh * 0.3),
                 (hx - hw * 0.86, hy - hh * 0.2), (hx - hw * 0.9, hy + hh * 0.5), (hx - hw * 1.1, hy + hh * 0.72)], 2)
    p.poly(bob, S_HAIR, INK, 2.4)
    _strands(p, [((hx - hw * 0.5, top + 30), (hx - hw * 0.4, hy - hh * 0.36)),
                 ((hx + hw * 0.1, top + 20), (hx + hw * 0.16, hy - hh * 0.36)),
                 ((hx + hw * 0.62, top + 34), (hx + hw * 0.6, hy - hh * 0.34)),
                 ((hx - hw * 1.02, hy - hh * 0.3), (hx - hw * 1.04, hy + hh * 0.4)),
                 ((hx + hw * 1.02, hy - hh * 0.3), (hx + hw * 1.04, hy + hh * 0.4))], S_HAIR_D, 1.8)
    p.line([(hx - hw * 0.66, top + 26), (hx - hw * 0.9, hy - hh * 0.6)], S_HAIR_L, 2.6)


HAIR = dict(zelda=(hair_zelda, Z_IRIS, (176, 130, 60), True), malon=(hair_malon, M_IRIS, (176, 80, 40), True),
            saria=(hair_saria, S_IRIS, (96, 140, 30), True))


def back_hair(p, j2, view):
    """Behind the body: Malon's long hair to the waist; Zelda's veil to the shoulder blades."""
    sp = j2.get('_sp', {})
    who = sp.get('who')
    hw, hh = sp.get('hw', 100), sp.get('hh', 108)
    hx, hy = 0.0, -150.0 + sp.get('head_dy', 0)
    if who == 'malon':
        back = curve([(hx - hw * 1.0, hy - hh * 0.8), (hx - hw * 1.3, hy + hh * 0.6), (hx - hw * 1.5, hy + hh * 2.8),
                      (hx - hw * 1.2, hy + hh * 3.4), (hx + hw * 1.2, hy + hh * 3.4), (hx + hw * 1.5, hy + hh * 2.8),
                      (hx + hw * 1.3, hy + hh * 0.6), (hx + hw * 1.0, hy - hh * 0.8)], 3)
        p.poly(back, M_HAIR_D, INK, 2.4)
    elif who == 'zelda':
        back = curve([(hx - hw * 1.1, hy - hh * 0.6), (hx - hw * 1.4, hy + hh * 1.4), (hx - hw * 1.3, hy + hh * 2.0),
                      (hx + hw * 1.3, hy + hh * 2.0), (hx + hw * 1.4, hy + hh * 1.4), (hx + hw * 1.1, hy - hh * 0.6)], 3)
        p.poly(back, dk(VEIL, 0.9), INK, 2.4)


def child_head(img, p, sp, t, hx, hy):
    who = sp['who']
    if who == 'ruto':
        return ruto_head(img, p, sp, t, hx, hy)
    m = dict(MOODS[(who, sp.get('react', 0))])
    hair, iris, brow_c, ears = HAIR[who]
    _face(p, sp, hx, hy)
    if who != 'zelda':
        hair(p, sp, hx, hy)
        _ears(p, sp, hx, hy)
    else:
        _ears(p, sp, hx, hy)
        hair(p, sp, hx, hy)
    _features(p, sp, hx, hy, m, iris, brow_c)
    return hx


def ruto_head(img, p, sp, t, hx, hy):
    """Ruto: pale smooth skin, a big teal domed head-fin sweeping back, small side fins, purple lashed eyes (07, 08)."""
    hw, hh = sp['hw'], sp['hh']
    m = dict(MOODS[('ruto', sp.get('react', 0))])
    for sg in (-1, 1):                                    # the small side fins where ears would be
        fin = curve([(hx + sg * hw * 0.9, hy - hh * 0.1), (hx + sg * hw * 1.4, hy - hh * 0.5),
                     (hx + sg * hw * 1.32, hy - hh * 0.06), (hx + sg * hw * 1.42, hy + hh * 0.14),
                     (hx + sg * hw * 0.94, hy + hh * 0.3)], 3)
        p.poly(fin, FIN, INK, 2.4)
        p.line([(hx + sg * hw * 1.0, hy + hh * 0.06), (hx + sg * hw * 1.3, hy - hh * 0.36)], FIN_D, 1.6)
    sweep = curve([(hx + hw * 0.6, hy - hh * 1.5), (hx + hw * 1.5, hy - hh * 1.9), (hx + hw * 2.0, hy - hh * 1.84),
                   (hx + hw * 1.7, hy - hh * 1.4), (hx + hw * 1.3, hy - hh * 1.0)], 3)
    p.poly(sweep, FIN_D, INK, 2.4)                        # the fin sweeping back, seen past the dome
    _face(p, sp, hx, hy, R_SKIN, chin=0.86)
    # the dome: a wide mushroom cap over the brow, wider than the face, a pale band under its rim
    dome = curve([(hx - hw * 1.86, hy - hh * 0.56), (hx - hw * 1.8, hy - hh * 1.06), (hx - hw * 1.2, hy - hh * 1.66),
                  (hx, hy - hh * 1.86), (hx + hw * 1.2, hy - hh * 1.66), (hx + hw * 1.8, hy - hh * 1.06),
                  (hx + hw * 1.86, hy - hh * 0.56), (hx + hw * 1.1, hy - hh * 0.56), (hx + hw * 0.6, hy - hh * 0.6),
                  (hx, hy - hh * 0.64), (hx - hw * 0.6, hy - hh * 0.6), (hx - hw * 1.1, hy - hh * 0.56)], 3)
    p.poly(dome, FIN, INK, 2.6)
    p.poly(curve([(hx - hw * 1.3, hy - hh * 1.2), (hx - hw * 0.5, hy - hh * 1.66), (hx + hw * 0.4, hy - hh * 1.68),
                  (hx - hw * 0.3, hy - hh * 1.5), (hx - hw * 1.0, hy - hh * 1.1)], 3), FIN_L, None)
    p.line(curve([(hx - hw * 1.7, hy - hh * 0.66), (hx, hy - hh * 0.8), (hx + hw * 1.7, hy - hh * 0.66)], 3)[:-6],
           FIN_D, 2.0)
    p.ell(hx, hy - hh * 1.04, 9, 9, R_IRIS, INK, 1.6)    # the small mark on the dome's front (07)
    _features(p, sp, hx, hy, m, R_IRIS, (120, 140, 150), R_SKIN, eye_k=1.04)
    return hx


# ------------------------------------------------------------------------------------------------ bodies
def _torso(sw, bottom):
    return [(-40, -4), (-sw * 0.8, 12), (-sw, 50), (-sw - 6, 200), (-sw * B.HEM, bottom), (sw * B.HEM, bottom),
            (sw + 6, 200), (sw, 50), (sw * 0.8, 12), (40, -4)]


def _skirt(p, sw, top, hem, flare, c, band=None, band_h=34):
    sk = curve([(-sw * 0.86, top), (sw * 0.86, top), (sw * flare, hem - 10), (sw * flare * 0.5, hem + 4), (0, hem + 6),
                (-sw * flare * 0.5, hem + 4), (-sw * flare, hem - 10)], 2)
    p.poly(sk, c, INK, 2.4)
    for k in (-0.5, 0.0, 0.5):                            # a few soft folds
        p.line([(sw * k * 0.7, top + 60), (sw * k * flare * 0.9, hem - 20)], dk(c, 0.86), 1.8)
    if band:
        y0 = hem - band_h
        k0 = 0.86 + (flare - 0.86) * (y0 - top) / (hem - top)
        p.poly([(-sw * k0, y0), (sw * k0, y0), (sw * flare, hem - 10), (sw * flare * 0.5, hem + 4), (0, hem + 6),
                (-sw * flare * 0.5, hem + 4), (-sw * flare, hem - 10)], band, INK, 2.2)
    return sk


def body_zelda(p, view, sp):
    sw = sp['shoulders']
    p.poly(_torso(sw, 340), Z_BLUE, INK, 2.4)
    _skirt(p, sw, 300, 836, 1.3, DRESS_W, Z_PURPLE, 36)
    tab = [(-sw * 0.62, 6), (sw * 0.62, 6), (sw * 0.56, 300), (sw * 0.6, 690), (0, 730), (-sw * 0.6, 690),
           (-sw * 0.56, 300)]
    p.poly(tab, Z_PURPLE, INK, 2.4)
    inner = [(x * 0.8, 20 + (y - 6) * 0.95) for x, y in tab]
    p.line(inner + [inner[0]], GOLD, 2.0)                 # the gold border
    for y in (200, 420, 600):                             # embroidery: small gold scrolls down the panel
        p.line(curve([(-26, y), (-12, y - 16), (0, y), (12, y + 16), (26, y)], 3), GOLD, 2.0)
    p.poly([(-50, -6), (50, -6), (70, 26), (0, 56), (-70, 26)], GOLD, INK, 2.2)     # the gold collar
    p.poly([(-30, -4), (30, -4), (0, 22)], sp['skin'], None)
    p.poly([(-24, 12), (24, 12), (0, 40)], GOLD_D, None)


def body_malon(p, view, sp):
    sw = sp['shoulders']
    p.poly(_torso(sw, 330), M_BLOUSE, INK, 2.4)
    for k in range(-3, 4):                                # the knit: a few short ribs
        p.line([(k * sw * 0.24, 110), (k * sw * 0.24, 160)], dk(M_BLOUSE, 0.85), 1.6)
    _skirt(p, sw, 300, 820, 1.26, M_SKIRT, M_HEM, 44)
    for i in range(9):                                    # the hem's meander: little square hooks
        x = -sw * 1.1 + i * sw * 0.27
        y = 800
        p.line([(x, y), (x, y - 20), (x + 18, y - 20), (x + 18, y - 8), (x + 8, y - 8)], (232, 236, 246), 2.0)
    ap = [(-sw * 0.52, 300), (sw * 0.4, 300), (sw * 0.5, 760), (-sw * 0.62, 760)]   # the apron, a touch off centre
    p.poly(ap, M_APRON, INK, 2.2)
    for y in (380, 480, 580, 680):                        # its woven pattern: light bars and boxes
        p.poly([(-sw * 0.36, y), (sw * 0.24, y), (sw * 0.24, y + 22), (-sw * 0.36, y + 22)], None, M_APRON_L, 2.0)
        p.line([(-sw * 0.06, y + 4), (-sw * 0.06, y + 18)], M_APRON_L, 2.0)
    p.poly([(-sw * 0.9, 284), (sw * 0.9, 284), (sw * 0.92, 316), (-sw * 0.92, 316)], BELT, INK, 2.0)
    p.poly([(-62, -6), (62, -6), (36, 70), (0, 120), (-36, 70)], M_SCARF, INK, 2.2)   # the yellow neckerchief
    p.poly([(-34, -6), (34, -6), (0, 30)], sp['skin'], None)
    p.ell(0, 36, 14, 12, M_BROOCH, INK, 2.0)


def body_saria(p, view, sp):
    sw = sp['shoulders']
    p.poly(_torso(sw, 520), S_DARK, INK, 2.4)
    tun = [(-sw * 0.7, 30), (-30, 30), (0, 54), (30, 30), (sw * 0.7, 30), (sw * 0.86, 300), (sw * B.HEM * 1.04, 540),
           (-sw * B.HEM * 1.04, 540), (-sw * 0.86, 300)]
    p.poly(tun, S_TUNIC, INK, 2.2)
    for cx, cy in ((-40, 180), (46, 250), (-30, 470), (50, 480)):   # the swirl pattern
        pts = [(cx + 6 * a / 6 * math.cos(a), cy + 6 * a / 6 * math.sin(a)) for a in np.linspace(0.5, 11, 24)]
        p.line(pts, S_TUNIC_L, 2.2)
    for sg in (-1, 1):                                    # fringed shoulders
        for k in range(6):
            x = sg * (sw * 0.62 + k * 9)
            p.line([(x, 20 + k * 4), (x + sg * 4, 50 + k * 4)], dk(S_TUNIC, 0.7), 2.4)
    p.poly([(-38, -70), (38, -70), (44, 14), (-44, 14)], S_DARK, INK, 2.2)   # the high collar over the neck
    p.line([(-36, -40), (36, -40)], dk(S_DARK, 0.75), 1.6)
    p.line([(-26, 8), (0, 86), (26, 8)], (90, 60, 40), 1.8)        # the pendant on its cord
    p.poly([(-12, 84), (12, 84), (0, 108)], PENDANT, INK, 1.8)
    p.poly([(-sw * 0.92, 380), (sw * 0.92, 380), (sw * 0.94, 410), (-sw * 0.94, 410)], BELT, INK, 2.0)
    p.ell(-sw * 0.3, 396, 13, 13, BEAD, INK, 1.8)
    p.line([(-sw * 0.3, 408), (-sw * 0.32, 446)], BELT_D, 2.0)
    p.ell(-sw * 0.32, 452, 8, 8, WOOD, INK, 1.4)


def body_ruto(p, view, sp):
    """A child's straight, plain body (not shapely: she is a child); the teal fin 'top' across the chest; hip fins."""
    sw = sp['shoulders']
    p.poly(_torso(sw, 470), R_SKIN, INK, 2.4)
    for sg in (-1, 1):                                    # small fins at the hips, hanging down and out
        f = curve([(sg * sw * 0.8, 400), (sg * sw * 1.24, 470), (sg * sw * 1.2, 580), (sg * sw * 0.96, 520),
                   (sg * sw * 0.82, 470)], 3)
        p.poly(f, FIN, INK, 2.2)
        p.line([(sg * sw * 0.86, 430), (sg * sw * 1.12, 540)], FIN_D, 1.6)
    top = [(-sw * 0.9, 74)]
    for i in range(7):                                    # the scalloped top edge
        x = -sw * 0.9 + (i + 0.5) * sw * 1.8 / 7
        top += [(x, 60 if i % 2 else 66), (-sw * 0.9 + (i + 1) * sw * 1.8 / 7, 74)]
    band = top + [(sw * 0.94, 150), (0, 158), (-sw * 0.94, 150)]
    p.poly(band, FIN, INK, 2.2)
    p.line([(-sw * 0.7, 100), (sw * 0.7, 100)], FIN_L, 2.0)


BODIES = dict(zelda=body_zelda, malon=body_malon, saria=body_saria, ruto=body_ruto)


# ------------------------------------------------------------------------------------------------ props (held)
def _mid(j2, sides='LR'):
    pts = [j2['wr' + s] for s in sides]
    return sum(q[0] for q in pts) / len(pts), sum(q[1] for q in pts) / len(pts)


def ocarina_blue(p, j2):
    x, y = _mid(j2)
    y -= 34                                               # held up over the hands, the body clear of them
    p.poly(curve([(x - 92, y + 6), (x - 44, y - 34), (x + 40, y - 34), (x + 88, y - 4), (x + 40, y + 32),
                  (x - 44, y + 32)], 3), OCARINA_B, INK, 2.6)
    p.poly([(x + 80, y - 10), (x + 122, y - 22), (x + 124, y - 2), (x + 84, y + 8)], OCARINA_B, INK, 2.2)   # mouthpiece
    p.line([(x - 54, y - 16), (x + 14, y - 24)], (150, 190, 246), 3.6)
    for k in range(3):
        p.ell(x - 30 + k * 26, y + 4, 5, 5, dk(OCARINA_B, 0.5), None)


ocarina_blue.held = True


def ocarina_wood(p, j2):
    x, y = j2['wrL']
    x, y = x + 40, y - 30                                 # resting across the top of her hand, shown to us
    p.poly(curve([(x - 70, y + 8), (x - 34, y - 28), (x + 34, y - 26), (x + 70, y + 2), (x + 34, y + 26),
                  (x - 34, y + 26)], 3), WOOD, INK, 2.6)
    p.poly([(x - 64, y), (x - 100, y - 14), (x - 102, y + 4), (x - 66, y + 12)], WOOD, INK, 2.2)
    for k in range(4):
        p.ell(x - 30 + k * 20, y - 2, 5, 5, dk(WOOD, 0.5), None)


ocarina_wood.held = False                                 # over her hand (shown to us)


def milk_bottle(p, j2):
    x, y = _mid(j2)
    y -= 20
    bot = curve([(x - 34, y + 70), (x - 36, y - 10), (x - 22, y - 46), (x - 16, y - 70), (x + 16, y - 70),
                 (x + 22, y - 46), (x + 36, y - 10), (x + 34, y + 70)], 2)
    p.poly(bot, MILK, INK, 2.4)
    p.poly([(x - 18, y - 70), (x + 18, y - 70), (x + 18, y - 88), (x - 18, y - 88)], MILK_CAP, INK, 2.0)
    p.poly([(x - 32, y), (x + 32, y), (x + 32, y + 30), (x - 32, y + 30)], MILK_CAP, INK, 1.8)   # the label
    p.line([(x - 22, y - 30), (x - 24, y + 50)], (226, 232, 240), 3.0)


milk_bottle.held = True


# ------------------------------------------------------------------------------------------------ arms, legs (hooks)
_prev_arm, _prev_leg, _prev_head_view, _prev_head = V.arm, V.leg, V.head_view, B.head
_base_arm = TL._arm


def _along(a, b, u):
    return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u


def _band(p, a, b, u0, u1, half, c, lw=2.2):
    """A band round a limb from u0 to u1 along a->b, `half` wide either side."""
    p0, p1 = _along(a, b, u0), _along(a, b, u1)
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / n * half, dx / n * half
    p.poly([(p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny), (p1[0] - nx, p1[1] - ny), (p0[0] - nx, p0[1] - ny)],
           c, INK, lw)


def arm(p, j2, side, sp, shape=None):
    who = sp.get('who')
    if who not in MINE or V.PROBE:
        return _prev_arm(p, j2, side, sp, shape)
    sh, el, wr = j2['sh' + side], j2['el' + side], j2['wr' + side]
    sg = -1 if side == 'L' else 1
    if who == 'ruto':                                     # the big leaf fin hangs from the forearm, behind it
        a = _along(el, wr, 0.2)
        f = curve([a, (a[0] + sg * 70, a[1] + 60), (a[0] + sg * 84, a[1] + 190), (a[0] + sg * 40, a[1] + 250),
                   (a[0] + sg * 20, a[1] + 150), _along(el, wr, 0.7)], 3)
        p.poly(f, FIN, INK, 2.4)
        p.line([(a[0] + sg * 14, a[1] + 30), (a[0] + sg * 50, a[1] + 200)], FIN_D, 1.8)
        p.line([(a[0] + sg * 40, a[1] + 60), (a[0] + sg * 64, a[1] + 150)], FIN_L, 2.0)
        return _base_arm(p, j2, side, sp, shape)
    if who == 'zelda':                                    # long pale-blue sleeves, puffed at the top, gold cuffs
        _base_arm(p, j2, side, dict(sp, sleeve=Z_BLUE, jacket=Z_BLUE), shape)
        c = _along(sh, el, 0.34)
        p.ell(c[0] + sg * 6, c[1], 50, 58, Z_BLUE, INK, 2.4)
        p.line([(c[0] + sg * 6 - 20, c[1] - 30), (c[0] + sg * 6 - 14, c[1] + 30)], dk(Z_BLUE, 0.82), 1.6)
        p.line([(c[0] + sg * 6 + 18, c[1] - 30), (c[0] + sg * 6 + 22, c[1] + 30)], dk(Z_BLUE, 0.82), 1.6)
        _band(p, el, wr, 0.82, 0.98, 30, GOLD)
        return
    if who == 'malon':                                    # short blue sleeves, white embroidery at the cuff
        _base_arm(p, j2, side, dict(sp, sleeve=sp['skin'], jacket=sp['skin']), shape)
        top = (sh[0] - (el[0] - sh[0]) * 0.18, sh[1] - (el[1] - sh[1]) * 0.18)
        _band(p, top, el, 0.0, 0.62, 36, M_SLEEVE, 2.4)
        q0, q1 = _along(top, el, 0.5), _along(top, el, 0.58)
        for k in range(-2, 3):
            p.ell((q0[0] + q1[0]) / 2 + k * 11, (q0[1] + q1[1]) / 2, 3, 3, (240, 240, 250), None)
        return
    if who == 'saria':                                    # dark green sleeves, brown bracers
        _base_arm(p, j2, side, dict(sp, sleeve=S_DARK, jacket=S_DARK), shape)
        _band(p, el, wr, 0.5, 0.94, 26, BOOT, 2.2)
        q = _along(el, wr, 0.72)
        p.line([(q[0] - 14, q[1]), (q[0] + 14, q[1])], dk(BOOT, 0.7), 1.6)
        return


def leg(p, j, side, yaw, sp, from_u=0.0):
    who = sp.get('who')
    if who not in MINE or from_u:
        return _prev_leg(p, j, side, yaw, sp, from_u)
    V.leg(p, j, side, yaw, sp, from_u) if False else TL._leg(p, j, side, yaw, sp, from_u)
    hip = V.project(j['hip' + side], yaw)[0]
    knee = V.project(V.knee_of(j, side), yaw)[0]
    foot = V.project(j['foot' + side], yaw)[0]
    if who == 'saria':                                    # green shorts to mid-thigh; boots with a folded cuff
        V.tube(p, [hip, _along(hip, knee, 0.42)], [56, 52], S_TUNIC)
        top = _along(foot, knee, 0.5)
        V.tube(p, [top, foot], [31, 30], BOOT)
        V.tube(p, [top, _along(foot, knee, 0.62)], [36, 37], dk(BOOT, 1.25))
    elif who == 'ruto':                                   # bare feet: a soft foot, pink toes; a knee line
        p.poly(curve([(foot[0] - 34, foot[1] + 40), (foot[0] - 30, foot[1] + 4), (foot[0] + 30, foot[1] + 4),
                      (foot[0] + 34, foot[1] + 40)], 3), R_SKIN, INK, 2.2)
        for k in (-2, -1, 0, 1, 2):
            p.ell(foot[0] + k * 13, foot[1] + 38, 6.5, 6, TOES, INK, 1.2)
        p.line([(knee[0] - 12, knee[1] + 4), (knee[0] + 4, knee[1] + 10)], R_SKIN_D, 2.0)


def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
    if sp.get('who') in MINE:
        return child_head(img, p, sp, t, hx, hy)
    return _prev_head_view(img, p, sp, t, view, hx, hy)


def head(img, p, sp, t, hx, hy):
    if sp.get('who') in MINE:
        return child_head(img, p, sp, t, hx, hy)
    return _prev_head(img, p, sp, t, hx, hy)


def install():
    B.head, V.head_view, V.arm, V.leg = head, head_view, arm, leg


install()

BASE = dict(skin=SKIN, hw=100, hh=108, head_dy=10, shoulders=108, outfit='jumper', full=True, pose='custom', seed=41)
CAST = dict(
    zelda=dict(BASE, who='zelda', name='Zelda', jacket=Z_BLUE, sleeve=Z_BLUE, trousers=DRESS_W, shoe=(150, 110, 80),
               bottom=560),
    malon=dict(BASE, who='malon', name='Malon', hw=98, jacket=M_BLOUSE, sleeve=SKIN, trousers=(236, 222, 196),
               shoe=BOOT, bottom=560),
    saria=dict(BASE, who='saria', name='Saria', jacket=S_DARK, sleeve=S_DARK, trousers=SKIN, shoe=BOOT, bottom=540),
    ruto=dict(BASE, who='ruto', name='Ruto', skin=R_SKIN, hw=94, jacket=R_SKIN, sleeve=R_SKIN, trousers=R_SKIN,
              shoe=R_SKIN, shoulders=100, bottom=470),
)


# ------------------------------------------------------------------------------------------------ poses
def pose(who, react=0):
    sp = CAST[who]
    sw = sp['shoulders']
    hw, hy = sp['hw'], -150.0 + sp['head_dy']
    j = V.standing(sp)
    if who == 'zelda':                                    # unsure: the ocarina held close in both hands, head tipped
        lift = 30 if react else 0
        for sd, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, sd, (sg * 38, 250.0 - lift, 150.0), 'down', 'fist')
        j['props'], j['grip'] = [ocarina_blue], {'L', 'R'}
        j['head_roll'] = -5 if react else -7
    elif who == 'malon':                                  # dutiful, pick-me: the milk bottle offered; on "ROMANCE"
        lift = 80 if react else 0                         # she lifts it up to us and rises a touch
        for sd, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, sd, (sg * 40, 310.0 - lift, 170.0), 'down', 'fist')
        j['props'], j['grip'] = [milk_bottle], {'L', 'R'}
        j['head_roll'] = 4 if react else 2
        if react:
            j['bob'] = -8
    elif who == 'saria':                                  # spunky: a hand on her hip, the ocarina up by her chest
        V.arm_to(j, 'R', (sw * 0.86, 340.0, -10.0), 'out', 'fist')
        V.arm_to(j, 'L', (-40.0, 230.0, 150.0), 'down', 'fist')
        j['props'] = [ocarina_wood]
        j['head_roll'] = 7 if react else 4
    elif who == 'ruto':                                   # preening: hands on hips, chin up; on "ROMANCE" one hand
        for sd, sg in (('L', -1), ('R', 1)):              # pats her head-fin
            V.arm_to(j, sd, (sg * sw * 0.86, 360.0, 0.0), 'out', 'fist')
        if react:
            V.arm_to(j, 'R', (hw * 1.3, hy - 60, 30.0), 'out', 'palm')
        j['nod'] = -1.2 if react else -0.8
        j['head_roll'] = 6 if react else 4
    j['body_props'] = [BODIES[who]]
    j['pre'] = [back_hair]
    return j


# ------------------------------------------------------------------------------------------------ the Goron
def goron(img, cam, x, floor, k, react=0):
    """The Goron in a frilly dress, front on, in its own units: feet at (0, 0), y up is negative, about 1470 tall to
    the tuft (2.13 m: Link x 1.6). One egg for head and body, stubby limbs, a big grin, drooling (11, 12)."""
    L = B.Local(cam, x, floor, k)
    p = B.Pen(img, L)
    kit.contact_shadow(img, cam, x, floor, 700 * k)
    for sg in (-1, 1):                                    # rocky grey patches on the back, peeking past the shoulders
        p.poly(curve([(sg * 250, -1200), (sg * 360, -1150), (sg * 400, -1020), (sg * 330, -980)], 2), ROCK, INK, 2.6)
        p.line([(sg * 320, -1140), (sg * 370, -1040)], ROCK_D, 2.4)
    for sg in (-1, 1):                                    # stubby legs and wide round feet
        p.poly(curve([(sg * 90, -330), (sg * 250, -330), (sg * 260, -120), (sg * 230, -50), (sg * 110, -50),
                      (sg * 90, -140)], 3), G_SKIN, INK, 2.6)
        p.poly(curve([(sg * 70, 0), (sg * 80, -70), (sg * 180, -96), (sg * 280, -70), (sg * 300, 0)], 3), G_SKIN, INK, 2.6)
        for t in range(3):
            p.line([(sg * (140 + 50 * t), -2), (sg * (140 + 50 * t), -24)], G_SKIN_D, 2.4)
    egg = curve([(0, -1400), (240, -1356), (330, -1190), (380, -960), (410, -660), (390, -440), (300, -290),
                 (0, -240), (-300, -290), (-390, -440), (-410, -660), (-380, -960), (-330, -1190), (-240, -1356)], 4)
    p.poly(egg, G_SKIN, INK, 3.0)
    p.poly(curve([(-250, -1240), (-180, -1330), (-60, -1362), (-160, -1250), (-236, -1090)], 3), G_SKIN_L, None)
    p.poly(curve([(0, -1394), (-30, -1440), (-10, -1470), (16, -1452), (40, -1470), (44, -1420), (24, -1390)], 2),
           TUFT, INK, 2.2)                                # the pale tuft
    # the dress: a frilly pink pinafore with straps, a lace-edged bodice, two ruffled tiers and a bow
    for sg in (-1, 1):
        p.poly([(sg * 150, -930), (sg * 220, -940), (sg * 250, -760), (sg * 180, -750)], FRILL, INK, 2.2)
    p.poly([(-396, -770), (396, -770), (410, -560), (-410, -560)], FRILL, INK, 2.4)
    for i in range(11):                                   # lace along the bodice top
        p.ell(-360 + i * 72, -772, 32, 20, LACE, INK, 1.8)
    sk_top, hem = -570, -260
    p.poly([(-410, sk_top), (410, sk_top), (450, hem), (-450, hem)], FRILL, INK, 2.4)
    for tier, y in enumerate((-450, hem)):
        half = 420 + 36 * tier
        n = 9 + tier
        for i in range(n):                                # the ruffles: a row of scallops
            xx = -half + (i + 0.5) * 2 * half / n
            p.ell(xx, y + 10, half / n + 8, 40, FRILL_L, INK, 2.0)
            p.line([(xx, y - 6), (xx, y + 34)], FRILL_D, 1.6)
    for i in range(12):                                   # lace at the hem
        p.ell(-440 + (i + 0.5) * 73, hem + 52, 24, 15, LACE, INK, 1.6)
    for sg in (-1, 1):                                    # the bow at the bodice
        p.poly([(0, -712), (sg * 100, -762), (sg * 108, -660)], FRILL_D, INK, 2.2)
    p.ell(0, -712, 30, 28, FRILL_D, INK, 2.2)
    # arms: stubby, curving down in front of the tummy, the hands clasped low over the skirt (bashful); on
    # "ROMANCE" they squeeze together and lift a little
    hy = -470 - (30 if react else 0)
    for sg in (-1, 1):
        ar = curve([(sg * 330, -900), (sg * 420, -800), (sg * 410, -640), (sg * 300, hy - 30), (sg * 100, hy - 50),
                    (sg * 100, hy + 60), (sg * 270, hy + 60), (sg * 300, -620), (sg * 280, -820)], 3)
        p.poly(ar, G_SKIN, INK, 2.6)
        p.line([(sg * 340, -700), (sg * 360, -620)], G_SKIN_D, 2.2)
    p.ell(46, hy, 78, 74, G_SKIN, INK, 2.6)              # two round hands, one over the other
    p.ell(-46, hy + 6, 78, 74, G_SKIN, INK, 2.6)
    p.line([(-30, hy - 40), (-6, hy - 10)], G_SKIN_D, 2.2)
    # the face (12): round dark purple eyes, small black brows, a small nose, a wide grin, a white goatee point
    for sg in (-1, 1):
        ex, ey = sg * 130, -1140
        r = 48 if react else 44
        p.ell(ex, ey, r, r * 1.08, G_EYE, INK, 2.6)
        p.ell(ex - 14, ey - 16, r * 0.36, r * 0.36, (255, 255, 255), None)
        p.ell(ex + 14, ey + 16, r * 0.15, r * 0.15, (255, 255, 255), None)
        by = ey - 82 - (18 if react else 0)
        p.poly(curve([(ex - sg * 14, by + 12), (ex + sg * 24, by - 6), (ex + sg * 56, by + 6), (ex + sg * 24, by + 10)],
                     2), (36, 26, 24), None)
    p.poly(oval(0, -1066, 28, 20, 16), G_SKIN_D, INK, 2.0)
    for sg in (-1, 1):
        p.ell(sg * 236, -1040, 54, 26, lerp(G_SKIN, (240, 110, 90), 0.75 if react else 0.4), None)
    w = 240 if react else 220
    grin = curve([(-w, -1020), (-w * 0.5, -956), (0, -940), (w * 0.5, -956), (w, -1020),
                  (w * 0.5, -930), (0, -908), (-w * 0.5, -930)], 3)
    p.poly(grin, (120, 50, 40), INK, 3.2)                 # a wide grin, a sliver of open mouth
    p.line(curve([(-w * 0.7, -952), (0, -932), (w * 0.7, -952)], 3), (250, 248, 240), 4.0)
    for sg in (-1, 1):
        p.line([(sg * w, -1020), (sg * (w + 20), -1040)], INK, 3.4)
    p.poly([(-26, -896), (26, -896), (0, -836)], (250, 250, 250), INK, 2.0)      # the goatee point
    dl = 170 if react else 90                             # the drool from the corner of the grin
    dx0, dy0 = -w * 0.66, -948
    p.poly(curve([(dx0 - 14, dy0), (dx0 + 14, dy0), (dx0 + 10, dy0 + dl), (dx0 + 24, dy0 + dl + 30),
                  (dx0, dy0 + dl + 52), (dx0 - 24, dy0 + dl + 30), (dx0 - 10, dy0 + dl)], 2), DROOL, INK, 2.2)
    p.ell(dx0 - 6, dy0 + dl + 24, 7, 8, (255, 255, 255), None)


# ------------------------------------------------------------------------------------------------ person
_TOPS = {}


def _top(who):
    """Units from the soles to the top of the drawing (measured once, so HEIGHTS means the visible top)."""
    if who not in _TOPS:
        im = Image.new('RGBA', (900, 1000), (0, 0, 0, 0))
        s2, floor = 0.5, 900
        sp = dict(CAST[who], react=0)
        j = pose(who, 0)
        j['_sp'] = sp
        V.person(im, TL._flat(), 450, floor - 928 * s2, s2, sp, 0.0, 0, j)
        top = im.getbbox()[1]
        _TOPS[who] = (floor - top) / s2
    return _TOPS[who]


def person(img, cam, who, x, floor, s, react=0):
    """Draw one of the five standing on `floor`; s is the scale of a 1.75 m adult."""
    if who == 'goron':
        k = s * HEIGHTS['goron'] / (1470 * V.M_PER_UNIT)
        goron(img, cam, x, floor, k, react)
        return
    s2 = s * HEIGHTS[who] / (_top(who) * V.M_PER_UNIT)
    sp = dict(CAST[who], react=react)
    j = pose(who, react)
    _patch_pre(j, sp)
    kit.feet_shadow(img, cam, x, floor - 928 * s2, s2)
    V.person(img, cam, x, floor - 928 * s2, s2, sp, 0.0, 0, j)


def _patch_pre(j, sp):
    """views passes only (p, j2, view) to a 'pre': hand it the person's settings through j2."""
    def pre(p, j2, view):
        j2['_sp'] = sp
        back_hair(p, j2, view)
    j['pre'] = [pre]


# ------------------------------------------------------------------------------------------------ the frame
ORDER = [('zelda', 106), ('malon', 268), ('saria', 432), ('ruto', 610), ('goron', 870)]
FLOOR = 1520


def lineup(react=1, scale=1):
    """The line-up, framed as S10 would be: 1080 x 1920 (x scale), a plain flat backdrop and a ground line."""
    B.SS = 1
    W, H = 1080 * scale, 1920 * scale
    img = Image.new('RGBA', (W, H), (206, 222, 232, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, FLOOR * scale, W, H], fill=(196, 186, 160))
    d.line([(0, FLOOR * scale), (W, FLOOR * scale)], fill=(150, 140, 118), width=3 * scale)
    cam = TL._flat()
    s = 0.48 * scale
    for who, x in sorted(ORDER, key=lambda o: o[0] != 'goron'):    # the big Goron stands a half step back
        person(img, cam, who, x * scale, FLOOR * scale, s, react)
    return img


def frame(out, react=1):
    img = lineup(react, 2).resize((1080, 1920), Image.LANCZOS)
    img.convert('RGB').save(out)
    return out


CROP = (0, 1020, 1080, 1560)                             # heads to feet of the children, the Goron's face and tummy


def crop(out, react=1):
    img = lineup(react, 2)
    x0, y0, x1, y1 = CROP
    img.crop((x0 * 2, y0 * 2, x1 * 2, y1 * 2)).convert('RGB').save(out)
    return out


BRIEF = ("Remakes S10, a wide line-up in a town square (the square and the owl who gestures at them are NOT in this "
         "test: a plain backdrop and ground line). Left to right: Young Zelda (unsure; holds her blue ocarina close), "
         "Malon (dutiful, 'pick-me', kind; holds a milk bottle up to us), Saria (spunky, sure 'he's already picked "
         "me': a hand on her hip, a wooden ocarina; she WINKS), Princess Ruto (vain, preening, pushy: chin up, a hand "
         "patting her head-fin; she is a CHILD, nothing sexual), a big Goron in a frilly pink dress, slightly "
         "drooling. Heights: Malon a little shorter than the others, the Goron about 1.6 x the children. Flat house "
         "style, circle hands. Judged ONLY at this size: detail too small to see here is not expected.")
BEAT = 'on "FIVE ROMANCE OPTIONS": each reacts on "ROMANCE"; Saria winks at Link (the camera), already sure'
REFS = ['references/remakes/10-zelda.jpg', 'source/data/trial_lineup/14-malon-right.jpg',
        'references/remakes/16-saria.jpg', 'references/remakes/08-ruto.jpg', 'references/remakes/12-goron.jpg',
        'references/remakes/11-goron.jpg']


def spec(rnd):
    import json
    d = os.path.join(HERE, 'data', 'trial_lineup')
    os.makedirs(d, exist_ok=True)
    im = Image.open(os.path.join(ROOT, 'references', 'remakes', '14-malon.jpg'))
    im.crop((im.width // 2, 0, im.width, im.height)).save(os.path.join(d, '14-malon-right.jpg'), quality=92)
    f, c = frame(os.path.join(d, f'h{rnd}-frame.png')), crop(os.path.join(d, f'h{rnd}-crop.png'))
    refs = [os.path.join(ROOT, r) for r in REFS]
    sp = {'round': rnd, 'panels': [
        dict(img=f, crop=None, parts='P', refs=refs, beat=BEAT, views=['front'],
             **{'is': 'the whole line-up frame at phone size (1080 x 1920). ' + BRIEF}),
        dict(img=c, crop=[0, 0, 2160, 1080], parts='P', refs=refs, beat=BEAT, views=['front'],
             **{'is': 'a 2x crop of the SAME frame (all five, heads to feet; the Goron face to knees), to confirm '
                      'faces and joins. ' + BRIEF})]}
    out = os.path.join(d, f'spec{rnd}.json')
    json.dump(sp, open(out, 'w'), indent=1)
    return out


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'frame':
        print(frame(sys.argv[2], 0 if 'idle' in sys.argv[3:] else 1))
    elif cmd == 'crop':
        print(crop(sys.argv[2], 0 if 'idle' in sys.argv[3:] else 1))
    elif cmd == 'spec':
        print(spec(int(sys.argv[2])))
