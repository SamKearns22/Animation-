#!/usr/bin/env python3
"""Halo No-No's cast (notes/halo-no-no.md): Elon Musk in Master Chief's armour (front on, seated at the Roadster's
yoke, his face clearly through a see-through gold visor) and anime Cortana (a small flat hologram, see-through blue
with scan lines and a slight glow: Sam's exception, 29 Oct).

Person units as in the rest of the series: neck base at (0, 0), y down, a head about 190 tall. Arms are solved by
the rig (figure.Rig), hands are plain circles.

    python3 source/halo_cast.py sheet OUT.jpg     the cast sheet (every view and pose the film uses)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B                    # noqa: E402  Cam, Local, Pen: flat fills, black outlines
from burnham import INK, dk, lt        # noqa: E402
import figure as F                     # noqa: E402  arms solved and guarded
import mouths                          # noqa: E402  lip-sync shapes
from ed import curve, open_curve       # noqa: E402  smooth outlines and lines
from satire_style import rough         # noqa: E402
from press_secretary import _clip_convex   # noqa: E402

SANS = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')

# ================================================ MUSKER CHIEF =====================================================
G = (92, 124, 70)            # the armour's olive green (refs 10-12)
G_D = (64, 90, 50)           # its flat shadow side
G_L = (128, 160, 100)        # the lit bevel
GREY = (104, 106, 112)       # the undersuit's grey hardware
SUIT = (48, 50, 56)          # the dark undersuit
LAMP = (190, 214, 255)       # the small blue lights
VISOR = (214, 158, 60)       # gold, see-through (Sam: no light streak, it might hide him)
INSIDE = (22, 24, 30)        # the helmet's dark inside round his face (never brown: it read as long hair)
SKIN = (236, 196, 170)
HAIR = (66, 48, 36)          # dark brown, short at the sides, swept up and back (refs 07-09, 20-21)
IRIS = (112, 146, 168)       # blue-grey

CHIEF_SW = 214               # shoulders: the armour is broad (shoulder joints at +-200)
YOKE = (0, 270)              # the yoke's middle, in his units (in front of his lower chest)
YOKE_HALF = 150              # centre to each grip


def chief_rig():
    return F.Rig(dict(shoulders=CHIEF_SW, name='Musk'))


def yoke_grips(turn):
    """Where each hand holds the yoke, turned `turn` degrees (positive: clockwise as he sees it, our anticlockwise)."""
    a = math.radians(turn)
    return {s: (YOKE[0] + sg * YOKE_HALF * math.cos(a), YOKE[1] - sg * YOKE_HALF * math.sin(a))
            for s, sg in (('L', -1), ('R', 1))}


def chief_arms(turn=0.0):
    rig, g = chief_rig(), yoke_grips(turn)
    return {s: rig.arm(s, g[s], 'grip', 'out', depth=0.2) for s in 'LR'}


def chief(img, cam, x, y, s, st=None, t=0.0):
    """Musk in the armour, front on, seated: from the helmet down to the belt (the dash hides the rest). st: mouth
    (a mouths shape), look (-1 his right .. 1 his left, i.e. our left is -1), blink, turn (the yoke, degrees),
    yoke (draw it), lean (degrees), brows ('set', 'up')."""
    st = dict(dict(mouth='rest', look=0.0, blink=False, turn=0.0, yoke=True, lean=0.0, brows='set'), **(st or {}))
    L = Lean(cam, x, y, s, st['lean'])
    p = B.Pen(img, L)
    R = lambda pts, sd, a=3: rough(pts, a, sd)
    # the dark undersuit body behind the plates
    p.poly(R([(-190, 20), (190, 20), (170, 470), (-170, 470)], 1), SUIT, INK, 4)
    # abdomen: dark grey segments under the chest plate
    for i, yy in enumerate((330, 372, 414)):
        p.poly(R([(-118 + i * 6, yy), (118 - i * 6, yy), (112 - i * 6, yy + 40), (-112 + i * 6, yy + 40)], 2 + i, 2),
               (72, 74, 80), INK, 3)
    # the chest plate: one big angular green plate, a ridge down the middle, a lip at the bottom
    chest = [(-176, 34), (-70, 20), (70, 20), (176, 34), (184, 150), (150, 290), (60, 336), (-60, 336), (-150, 290),
             (-184, 150)]
    p.poly(R(chest, 6, 2), G, INK, 4.4)
    p.poly(R([(-184, 150), (-150, 290), (-60, 336), (-58, 300), (-136, 262), (-160, 150)], 7, 2), G_D, None)
    p.poly(R([(-70, 20), (70, 20), (60, 52), (-60, 52)], 8, 1.5), G_L, INK, 3)                 # the collar bevel
    for sg in (-1, 1):
        p.line([(sg * 18, 60), (sg * 24, 300)], dk(G, 0.8), 3)                               # the central ridge
        p.poly(R([(sg * 62, 120), (sg * 132, 112), (sg * 140, 210), (sg * 70, 226)], 9 + sg, 2), dk(G, 0.92), INK, 2.6)
    p.poly(R([(-10, 230), (10, 230), (10, 256), (-10, 256)], 11, 1), LAMP, INK, 2)            # the small blue light
    # the upper arms (undersuit, a green plate on each), solved to the yoke grips
    arms = chief_arms(st['turn'])
    for side, sg in (('L', -1), ('R', 1)):
        el, wr, _ = arms[side]
        sh = (sg * (CHIEF_SW - 14), 60)
        _limb(p, sh, el, 84, SUIT)
        _plate(p, sh, el, 0.15, 0.85, 78, G, 12 + sg)
    # the neck seal and the helmet
    p.poly(R([(-96, -46), (96, -46), (110, 34), (-110, 34)], 13, 2), GREY, INK, 4)
    for yy in (-24, -2, 18):
        p.line([(-98, yy), (98, yy)], dk(GREY, 0.72), 2.4)
    _helmet(img, p, L, st, t)
    # the big shoulder plates over the tops of the arms
    for sg in (-1, 1):
        pts = [(sg * 120, -6), (sg * 214, -24), (sg * 272, 30), (sg * 262, 168), (sg * 196, 186), (sg * 150, 120)]
        p.poly(R(pts, 14 + sg, 3), G, INK, 4.4)
        p.poly(R([(sg * 262, 168), (sg * 196, 186), (sg * 182, 150), (sg * 246, 136)], 15 + sg, 2), G_D, None)
        p.line([(sg * 214, -24), (sg * 206, 120)], dk(G, 0.8), 2.6)                          # its fold
        p.poly(R([(sg * 236, 20), (sg * 254, 22), (sg * 252, 46), (sg * 234, 44)], 16 + sg, 1), LAMP, INK, 2)
    # the yoke in front of him (nearly upright, satire.md), then the forearms and gloved hands over it
    if st['yoke']:
        yoke(p, st['turn'])
    for side, sg in (('L', -1), ('R', 1)):
        el, wr, _ = arms[side]
        _limb(p, el, wr, 74, SUIT)
        _plate(p, el, wr, 0.0, 0.9, 80, G, 18 + sg)
        d = _unit(np.subtract(wr, el))
        p.ell(wr[0] + d[0] * 26, wr[1] + d[1] * 26, 34, 34, (58, 60, 66), INK, 3.6)          # the glove: a circle


def yoke(p, turn):
    """The Roadster's yoke (ref 04): a black U with two handles, on a column; turned `turn` degrees."""
    a = math.radians(turn)
    cx, cy = YOKE
    rot = lambda pts: [(cx + u * math.cos(a) + v * math.sin(a), cy - u * math.sin(a) + v * math.cos(a)) for u, v in pts]
    p.poly(rough([(cx - 30, cy + 60), (cx + 30, cy + 60), (cx + 40, cy + 240), (cx - 40, cy + 240)], 2, 31),
           (30, 30, 34), INK, 4)                                                                    # the column
    rim = [(-170, -40), (-130, -46), (-110, 20), (-60, 40), (60, 40), (110, 20), (130, -46), (170, -40), (166, 30),
           (120, 70), (60, 84), (-60, 84), (-120, 70), (-166, 30)]
    p.poly(rot(curve(rim, 3)), (26, 26, 30), INK, 4)
    p.poly(rot([(-44, 44), (44, 44), (40, 78), (-40, 78)]), (52, 52, 58), INK, 2.6)             # the hub


def _helmet(img, p, L, st, t):
    """Mark V helmet (refs 10-12): an angular dome with a ridge, a brow over a big visor, side pieces with two blue
    lights, a vented chin guard. The visor is made tall enough to show his whole face (a cheat on the real helmet, so
    it is clearly Musk and his mouth can talk: Sam's brief)."""
    hx, hy = 0, -196                     # the face's centre
    R = lambda pts, sd, a=3: rough(pts, a, sd)
    shell = [(-128, -150), (-120, -270), (-80, -328), (0, -344), (80, -328), (120, -270), (128, -150), (124, -70),
             (92, -34), (-92, -34), (-124, -70)]
    p.poly(R(shell, 40, 2), G, INK, 4.4)
    p.poly(R([(-128, -150), (-120, -270), (-80, -328), (-60, -300), (-100, -250), (-106, -150)], 41, 2), G_D, None)
    p.poly(R([(-20, -344), (20, -344), (24, -306), (-24, -306)], 42, 1), G_L, INK, 2.6)        # the ridge
    # the side pieces with their two blue lights
    for sg in (-1, 1):
        p.poly(R([(sg * 118, -230), (sg * 150, -226), (sg * 154, -132), (sg * 122, -120)], 43 + sg, 2), G, INK, 4)
        for ly in (-200, -164):
            p.ell(sg * 137, ly, 10, 10, LAMP, INK, 2)
    # the visor opening: the helmet's dark inside, his face, then the gold glass over it (see-through)
    vis = [(-100, -282), (-60, -306), (60, -306), (100, -282), (108, -170), (88, -102), (40, -84), (-40, -84),
           (-88, -102), (-108, -170)]
    p.poly(vis, INSIDE, INK, 4)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))                # his face, clipped to the visor's opening
    musk_face(lay, B.Pen(lay, L), st, hx, hy)
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).polygon([L.P(*q) for q in curve(vis, 3)], fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.array(lay.split()[3]), np.array(m))))
    img.alpha_composite(lay)
    tint = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(tint).polygon([L.P(*q) for q in curve(vis, 3)], fill=VISOR + (62,))
    img.alpha_composite(tint)
    p.poly(curve(vis, 3), None, dk(VISOR, 0.6), 7)                                              # the gold frame
    p.poly(curve(vis, 3), None, INK, 3)
    # the brow over the visor and the vented chin guard below it
    p.poly(R([(-112, -290), (-62, -318), (62, -318), (112, -290), (106, -276), (60, -300), (-60, -300), (-106, -276)],
             45, 1.5), G_L, INK, 3)
    chin = [(-92, -100), (-40, -80), (40, -80), (92, -100), (90, -46), (54, -28), (-54, -28), (-90, -46)]
    p.poly(R(chin, 46, 2), G, INK, 4)
    for sg in (-1, 1):
        for i in range(3):
            yy = -78 + i * 13
            p.line([(sg * 30, yy), (sg * 74, yy - 6)], dk(G, 0.6), 4)


def musk_face(img, p, st, hx, hy):
    """Elon Musk, front on, measured on ref 08 (hairline to chin 1.0): brows 0.29, eyes 0.37, nose base 0.60, mouth
    0.75; width at the cheeks 0.72 of the height; eye centres 0.31 of the face width either side of the middle. Long
    face, full soft cheeks, a narrow chin; receding temples, the hair short at the sides and swept up and back; dark,
    fairly straight brows; small, hooded blue-grey eyes with heavy lower lids; a long straight nose; a thin upper lip
    over a fuller lower lip; light stubble round the mouth and a goatee shadow on the chin. Sam: no exaggeration."""
    top, chin = hy - 80, hy + 84                     # hairline .. chin: 164
    H = chin - top
    at = lambda f: top + f * H
    cw = 0.36 * H                                    # half the width at the cheeks
    look = st.get('look', 0.0)
    # the hair behind (the crown and the swept-back top, short at the sides)
    back = [(hx - cw - 2, at(0.04)), (hx - cw + 2, at(-0.06)), (hx - cw * 0.66, at(-0.24)), (hx, at(-0.30)),
            (hx + cw * 0.66, at(-0.24)), (hx + cw - 2, at(-0.06)), (hx + cw + 2, at(0.04))]
    p.poly(rough(curve(back, 3), 1.2, 60), HAIR, INK, 2.6)
    # ears (only their front edges inside the helmet)
    for sg in (-1, 1):
        p.poly(curve([(hx + sg * cw * 0.96, at(0.33)), (hx + sg * (cw + 12), at(0.36)), (hx + sg * (cw + 10), at(0.52)),
                      (hx + sg * cw * 0.94, at(0.58))], 3), SKIN, INK, 2.4)
    # the face: long, full in the cheeks, tapering to a narrow chin
    face = [(hx - cw * 0.92, at(0.0)), (hx - cw, at(0.30)), (hx - cw * 0.98, at(0.52)), (hx - cw * 0.9, at(0.74)),
            (hx - cw * 0.62, at(0.92)), (hx - cw * 0.26, at(1.0)), (hx + cw * 0.26, at(1.0)), (hx + cw * 0.62, at(0.92)),
            (hx + cw * 0.9, at(0.74)), (hx + cw * 0.98, at(0.52)), (hx + cw, at(0.30)), (hx + cw * 0.92, at(0.0))]
    p.poly(curve(face, 3), SKIN, INK, 2.8)
    # stubble round the mouth and the goatee shadow on the chin
    stub = dk(SKIN, 0.95)
    p.poly(curve([(hx - cw * 0.44, at(0.70)), (hx, at(0.67)), (hx + cw * 0.44, at(0.70)), (hx + cw * 0.40, at(0.86)),
                  (hx + cw * 0.2, at(0.99)), (hx - cw * 0.2, at(0.99)), (hx - cw * 0.40, at(0.86))], 3), stub, None)
    p.poly(curve([(hx - cw * 0.5, at(0.84)), (hx - cw * 0.2, at(0.86)), (hx + cw * 0.2, at(0.86)), (hx + cw * 0.5, at(0.84)),
                  (hx + cw * 0.3, at(0.97)), (hx, at(1.0)), (hx - cw * 0.3, at(0.97))], 3), (196, 156, 132), None)   # goatee
    # short dark sides (sideburns) and the hair: receding deep at the temples, a short peak in the middle, the top
    # swept up and back into a low quiff (refs 08, 20)
    for sg in (-1, 1):
        p.poly(curve([(hx + sg * cw * 1.03, at(0.24)), (hx + sg * cw * 0.95, at(0.22)), (hx + sg * cw * 0.92, at(0.08)),
                      (hx + sg * cw * 1.02, at(0.04))], 3), HAIR, INK, 2.0)
    front = [(hx - cw * 0.98, at(0.06)), (hx - cw * 0.88, at(0.07)), (hx - cw * 0.74, at(-0.03)),
             (hx - cw * 0.52, at(-0.06)), (hx - cw * 0.26, at(-0.02)), (hx, at(0.0)), (hx + cw * 0.26, at(-0.02)),
             (hx + cw * 0.52, at(-0.06)), (hx + cw * 0.74, at(-0.03)), (hx + cw * 0.88, at(0.07)), (hx + cw * 0.98, at(0.06)),
             (hx + cw * 0.98, at(-0.14)), (hx + cw * 0.7, at(-0.30)), (hx + cw * 0.1, at(-0.38)),
             (hx - cw * 0.5, at(-0.34)), (hx - cw * 0.98, at(-0.16))]
    p.poly(rough(curve(front, 3), 1.0, 61), HAIR, INK, 2.6)
    for i in range(3):                                                                   # swept back, a few strokes
        x0 = hx - cw * 0.34 + i * cw * 0.3
        p.line(open_curve([(x0, at(-0.06)), (x0 + 4, at(-0.18)), (x0 + 14, at(-0.28))], 3), lt(HAIR, 1.5), 1.8)
    # eyes: small, a little hooded, heavy lower lids; brows dark and fairly straight
    ey = at(0.37)
    blink = st.get('blink')
    for sg in (-1, 1):
        ex = hx + sg * 0.31 * 2 * cw
        if blink:
            p.line([(ex - 12, ey + 1), (ex, ey + 3), (ex + 12, ey + 1)], INK, 2.6)
        else:
            _musk_eye(p, ex, ey, look)
        p.line([(ex - 13, ey + 9), (ex, ey + 12), (ex + 12, ey + 9)], dk(SKIN, 0.82), 1.6)        # the heavy lower lid
        p.line([(ex - 13, ey - 8), (ex + 2, ey - 11), (ex + 13, ey - 7)], dk(SKIN, 0.8), 1.6)     # the hood crease
        by = at(0.27) - (5 if st.get('brows') == 'up' else 0)
        inner, outer = ex - sg * 16, ex + sg * 21
        p.poly([(inner, by + 3), (ex + sg * 4, by - 2), (outer, by + 3), (outer, by + 5), (ex + sg * 4, by + 2),
                (inner, by + 7)], dk(HAIR, 0.85), None)                                              # thin, a soft arch
    # the long straight nose and its base
    nb = at(0.58)
    p.line([(hx - 4, ey + 2), (hx - 6, nb - 8)], dk(SKIN, 0.72), 1.8)
    p.poly(curve([(hx - 16, nb - 4), (hx - 5, nb + 3), (hx + 5, nb + 3), (hx + 16, nb - 4), (hx + 4, nb), (hx - 4, nb)], 3),
           dk(SKIN, 0.86), None)
    for sg in (-1, 1):
        p.line([(hx + sg * 11, nb), (hx + sg * 5, nb + 3)], INK, 1.8)
        p.line([(hx + sg * 18, nb + 2), (hx + sg * 25, at(0.76))], dk(SKIN, 0.86), 1.6)          # faint smile folds
    # the mouth: a thin upper lip over a fuller lower one; talking shapes from the lip-sync set
    my = at(0.75)
    shape = st.get('mouth', 'rest')
    if shape == 'rest':                                                              # pink lips, the lower one fuller
        p.poly(curve([(hx - 22, my + 1), (hx - 8, my - 5), (hx, my - 3), (hx + 8, my - 5), (hx + 22, my + 1), (hx + 10, my + 9),
                      (hx - 10, my + 9)], 3), (214, 140, 136), None)
        p.line([(hx - 22, my + 1), (hx - 8, my - 1), (hx + 8, my - 1), (hx + 22, my + 1)], INK, 2.4)
    else:
        mouths.draw(p, {}, hx, my, shape)


def _musk_eye(p, ex, ey, look):
    """One opening between two lids, the iris cut to it (no line ever crosses the white)."""
    w = 12
    us = np.linspace(-1, 1, 15)
    upper = [(ex + w * u, ey - 5.5 * (1 - u * u) - 0.6 * u) for u in us]
    lower = [(ex + w * u, ey + 4.5 * (1 - u * u)) for u in us]
    opening = upper + lower[::-1][1:-1]
    p.poly(opening, (250, 250, 246), None)
    cx, cy = ex + 6 * look, ey
    circ = lambda r: [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24, endpoint=False)]
    iris = _clip_convex(opening[::-1], circ(6.2))
    if len(iris) >= 3:
        p.poly(iris, IRIS, None)
    pupil = _clip_convex(opening[::-1], circ(2.8))
    if len(pupil) >= 3:
        p.poly(pupil, INK, None)
    p.line(lower, INK, 1.4)
    p.line(upper, INK, 2.8)


class Lean(B.Local):
    """A person's own coordinates with the upper body leaning (degrees) about the hips (y 440)."""
    def __init__(self, cam, ox, oy, s, lean=0.0, flip=1):
        super().__init__(cam, ox, oy, s, flip)
        self.c, self.sn = math.cos(math.radians(lean)), math.sin(math.radians(lean))

    def P(self, x, y):
        dy = y - 440
        return super().P(x * self.c - dy * self.sn, 440 + x * self.sn + dy * self.c)


def _unit(v):
    v = np.asarray(v, float)
    return v / (np.linalg.norm(v) + 1e-9)


def _limb(p, a, b, w, col):
    d = _unit(np.subtract(b, a))
    n = np.array([-d[1], d[0]]) * w / 2
    a, b = np.array(a, float), np.array(b, float)
    p.poly([tuple(a + n), tuple(b + n * 0.92), tuple(b - n * 0.92), tuple(a - n)], col, INK, 4)
    p.ell(a[0], a[1], w / 2, w / 2, col, None)


def _plate(p, a, b, u0, u1, w, col, seed):
    """An armour plate along a limb from u0 to u1 of its length: angular, a little wider in the middle."""
    a, b = np.array(a, float), np.array(b, float)
    d = b - a
    n = _unit((-d[1], d[0])) * w / 2
    q0, q1, qm = a + d * u0, a + d * u1, a + d * (u0 + u1) / 2
    pts = [tuple(q0 + n * 0.8), tuple(qm + n * 1.05), tuple(q1 + n * 0.85), tuple(q1 - n * 0.85), tuple(qm - n * 1.05),
           tuple(q0 - n * 0.8)]
    p.poly(rough(pts, 2, seed), col, INK, 3.6)
    p.line([tuple(qm - n * 0.4 + (q0 - qm) * 0.6), tuple(qm - n * 0.4 + (q1 - qm) * 0.6)], dk(col, 0.78), 2.4)


# ================================================== CORTANA ========================================================
# Anime Cortana (refs 17-19): a grown woman, anime proportions (about 6.5 heads), big glossy eyes, a navy bob with a
# long fringe lock, the high-collared bodysuit of ref 18 (dark blue, pale panel lines, long gloves), an hourglass
# figure. Drawn front on, and once turned away looking back over her shoulder (rule 38 exception: the brief).
# Fan-service played as a cringe joke, never explicit (Sam, 29 Oct). Her own units: neck base (0, 0), y down, the
# head's middle at (0, -150), toes at 948 (pointed: she floats).
C_SKIN = (150, 206, 252)
C_SKIN_D = (112, 170, 236)
C_SUIT = (40, 72, 156)
C_SUIT_D = (30, 54, 124)
C_SUIT_L = (66, 106, 196)
C_LINE = (196, 236, 255)     # the suit's pale panel lines
C_HAIR = (26, 44, 112)
C_HAIR_L = (74, 116, 204)
C_IRIS = (40, 76, 178)
C_GLOW = (110, 180, 255)
C_SW = 98                    # her shoulders (joints at +-84)

POSES = ('appear', 'point', 'kawaii', 'turn', 'stand')


def cortana_rig():
    return F.Rig(dict(shoulders=C_SW, name='Cortana'))


def cortana_arms(pose):
    """Arms per pose, solved by the rig (hand contact points in her units). Musk is to her left (our right)."""
    rig = cortana_rig()
    if pose == 'appear':        # flung up and out, a burst of arrival
        return {'L': rig.arm('L', (-250, -200), 'fist', 'out'), 'R': rig.arm('R', (250, -200), 'fist', 'out')}
    if pose == 'point':         # one arm thrust at Musk, the other fist on her popped hip
        return {'L': rig.arm('L', (-128, 380), 'fist', 'out'), 'R': rig.arm('R', (400, 20), 'point', 'down')}
    if pose == 'kawaii':        # fists squeezed up by her cheeks, elbows tucked in: the chest pushed forward
        return {'L': rig.arm('L', (-74, -96), 'fist', 'down', depth=0.45), 'R': rig.arm('R', (74, -96), 'fist', 'down', depth=0.45)}
    if pose == 'turn':          # seen from behind: a fist on the hip, the other hand waving up by her head
        return {'L': rig.arm('L', (-128, 380), 'fist', 'out'), 'R': rig.arm('R', (230, -170), 'fist', 'out')}
    return {'L': rig.arm('L', (-120, 430), 'fist', 'depth'), 'R': rig.arm('R', (120, 430), 'fist', 'depth')}


def cortana(img, cam, x, y, s, st=None, t=0.0):
    """Cortana as a hologram at world (x, y) (her neck base), s the scale. st: pose (POSES), mouth ('rest', 'smile' or
    a mouths shape), look (-1..1, her pupils; 1 = towards our right), blink, wink, appear (0..1: she forms out of
    the discharge; 1 = whole), flicker (0..1), lean (degrees), hip (the hip pop, -1..1), chest (0..1 pushed out)."""
    st = dict(dict(pose='stand', mouth='rest', look=1.0, blink=False, wink=False, appear=1.0, flicker=0.0, lean=0.0,
                   hip=0.0, chest=0.0), **(st or {}))
    if st['appear'] <= 0:
        return
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    L = Lean(cam, x, y, s, st['lean'])
    p = B.Pen(lay, L)
    if st['pose'] == 'turn':
        _cortana_back(p, st)
    else:
        _cortana_front(p, st)
    hologram(img, lay, cam, st['appear'], st['flicker'], t)


def hologram(img, lay, cam, appear=1.0, flicker=0.0, t=0.0):
    """Lay a figure drawn on its own layer into the frame as a flat hologram: a slight soft glow round it (Sam's
    exception), see-through, scan lines across it. appear 0..1 builds it up in horizontal bands (the digital forming)."""
    a = lay.split()[3]
    if appear < 1:
        w, h = lay.size
        r = np.random.default_rng(int(t * 24) + 5)
        mask = np.zeros((h, w), np.uint8)
        band = max(4, int(cam.S(9)))
        for y0 in range(0, h, band):
            if r.random() < appear:
                mask[y0:y0 + band] = 255
        a = Image.fromarray(np.minimum(np.array(a), mask))
    glow = Image.new('RGBA', lay.size, C_GLOW + (0,))
    glow.putalpha(a.filter(ImageFilter.GaussianBlur(cam.S(10))).point(lambda v: int(v * 0.55)))
    img.alpha_composite(glow)
    k = (0.85 - 0.25 * flicker) * min(1.0, appear * 1.4)
    arr = np.array(lay)
    al = np.array(a).astype(float) * k
    rows = (np.arange(arr.shape[0]) // max(2, int(cam.S(3)))) % 2 == 0                      # scan lines
    arr[rows, :, :3] = np.minimum(255, arr[rows, :, :3].astype(int) + 24).astype(np.uint8)
    arr[..., 3] = al.astype(np.uint8)
    img.alpha_composite(Image.fromarray(arr))


def _legs(p, hip):
    """Two long legs tapering to pointed toes; their tops tuck under the hips."""
    for sg in (-1, 1):
        o = hip * (1.0 if sg > 0 else 0.6)
        leg = [(sg * 116 + o, 420), (sg * 112 + o, 500), (sg * 66 + o * 0.5, 700), (sg * 50 + o * 0.3, 880),
               (sg * 40 + o * 0.2, 950), (sg * 28 + o * 0.2, 940), (sg * 22 + o * 0.3, 880), (sg * 22 + o * 0.5, 700),
               (sg * 6 + o, 486), (sg * 4 + o, 440)]
        p.poly(curve(leg, 4), C_SUIT, INK, 3.2)
        kx = sg * 44 + o * 0.5
        p.line(open_curve([(kx - 22, 680), (kx, 688), (kx + 22, 680)], 3), C_LINE, 3)              # knee panel
        p.line(open_curve([(kx - 20, 728), (kx, 734), (kx + 20, 728)], 3), C_LINE, 3)
        p.line([(sg * 24 + o * 0.3, 862), (sg * 50 + o * 0.3, 860)], C_LINE, 3)                   # boot cuff


def _body_outline(chest, hip, back=False):
    c = 1.0 + 0.16 * chest
    pts = [(-26, -12), (26, -12), (78, 18), (96, 62), (88, 110), (100 * c, 160), (84, 214), (56, 290),
           (82 + hip, 350), (118 + hip, 420), (108 + hip, 478), (0 + hip, 470), (-108 + hip, 478), (-118 + hip, 420),
           (-82 + hip, 350), (-56, 290), (-84, 214), (-100 * c, 160), (-88, 110), (-96, 62), (-78, 18)]
    return pts


def _cortana_front(p, st):
    hip = st['hip'] * 20
    c = 1.0 + 0.16 * st['chest']
    _legs(p, hip)
    p.poly(curve(_body_outline(st['chest'], hip), 4), C_SUIT, INK, 3.4)
    # the bust: two round forms, inked underneath, a flat lighter top (an hourglass, never explicit)
    for sg in (-1, 1):
        bx, by, rx, ry = sg * 44 * c, 156, 50 * c, 44 * c
        p.ell(bx, by, rx, ry, C_SUIT, None)
        p.ell(bx - sg * 6, by - 14, rx * 0.6, ry * 0.42, C_SUIT_L, None)
        p.line([(bx + rx * math.cos(a), by + ry * math.sin(a)) for a in np.linspace(0.15 * math.pi, 0.9 * math.pi, 14)]
               if sg < 0 else [(bx + rx * math.cos(a), by + ry * math.sin(a)) for a in np.linspace(0.1 * math.pi, 0.85 * math.pi, 14)],
               INK, 2.8)
    # the collar and panel lines (ref 18)
    p.poly(curve([(-30, -14), (30, -14), (34, 22), (-34, 22)], 3), C_SUIT_D, INK, 3)
    p.line([(-30, 14), (30, 14)], C_LINE, 3)
    p.line(open_curve([(-86, 70), (-40, 92), (0, 100), (40, 92), (86, 70)], 3), C_LINE, 3)       # shoulder panel
    p.line([(0, 200), (0, 270)], C_LINE, 2.4)
    p.poly(curve([(-58, 270), (0, 280), (58, 270), (60, 296), (0, 306), (-60, 296)], 3), C_LINE, INK, 2.4)   # belt
    for xx in (-30, 0, 30):
        p.line([(xx, 276 + abs(xx) * 0.1), (xx, 300 - abs(xx) * 0.1)], C_SUIT_D, 2.4)
    for sg in (-1, 1):                                                                          # the high-cut panels
        p.line(open_curve([(sg * 60 + hip, 304), (sg * 50 + hip, 380), (sg * 14 + hip, 466)], 3), C_LINE, 3)
    _c_arms(p, st, cortana_arms(st['pose']), front=st['pose'] != 'kawaii')
    _cortana_head(p, st, 0, -150)
    if st['pose'] == 'kawaii':                    # the fists up by her cheeks, drawn over the hair
        _c_arms(p, st, cortana_arms('kawaii'), front=True, only_fore=True)


def _c_arms(p, st, arms, front=True, only_fore=False):
    for side, sg in (('L', -1), ('R', 1)):
        el, wr, shape = arms[side]
        sh = (sg * (C_SW - 14), 60)
        if not only_fore:
            _limb(p, sh, el, 46, C_SKIN)
            mid = tuple(np.array(sh) + (np.array(el) - np.array(sh)) * 0.45)
            _limb(p, mid, el, 48, C_SUIT)                                                     # the long glove
            p.ell(sh[0], sh[1], 26, 26, C_SUIT_D, INK, 3)                                     # the shoulder panel
            if not front:
                continue
        _limb(p, el, wr, 42, C_SUIT)
        d = _unit(np.subtract(wr, el))
        off = F.HAND.get(shape, 14) if shape != 'point' else 24
        p.ell(wr[0] + d[0] * off, wr[1] + d[1] * off, 25, 25, C_SKIN, INK, 3)                  # circle hand


def _cortana_head(p, st, hx, hy, turned=0.0):
    """The anime head: a soft face narrowing to a small pointed chin, big glossy eyes set low, a tick of a nose, a small
    mouth; a navy bob to the jaw with locks in front of the ears and a long fringe lock. turned 0..1: looking back over
    her shoulder (the face slides to our right, the hair covers its far side)."""
    sh = 40 * turned
    back = [(hx - 100, hy + 90), (hx - 108, hy - 20), (hx - 86, hy - 92), (hx - 40, hy - 118), (hx + 20, hy - 120),
            (hx + 80, hy - 98), (hx + 106, hy - 30), (hx + 100, hy + 90), (hx + 70, hy + 104), (hx + 40, hy + 84),
            (hx, hy + 100), (hx - 40, hy + 86), (hx - 72, hy + 104)]
    p.poly(rough(curve(back, 4), 1.5, 70), C_HAIR, INK, 3)
    p.poly([(hx - 18 + sh * 0.3, hy + 70), (hx + 18 + sh * 0.3, hy + 70), (hx + 22, hy + 160), (hx - 22, hy + 160)],
           C_SKIN_D, INK, 2.6)                                                                  # neck
    hx = hx + sh
    face = [(hx - 70, hy - 50), (hx - 68, hy + 10), (hx - 46, hy + 66), (hx - 12, hy + 98), (hx, hy + 102),
            (hx + 12, hy + 98), (hx + 46, hy + 66), (hx + 68, hy + 10), (hx + 70, hy - 50), (hx + 40, hy - 92),
            (hx - 40, hy - 92)]
    p.poly(curve(face, 4), C_SKIN, INK, 3)
    p.ell(hx - 46, hy + 40, 12, 6, C_SKIN_D, None)                                           # a flat blush
    p.ell(hx + 46, hy + 40, 12, 6, C_SKIN_D, None)
    look = st['look']
    for sg in (-1, 1):
        ex, ey = hx + sg * 32, hy + 10
        if turned and sg < 0:
            continue                                                                            # behind her hair
        if st['blink'] or (st['wink'] and sg == 1):
            p.line(open_curve([(ex - 20, ey + 4), (ex, ey - 6), (ex + 20, ey + 4)], 3), INK, 4)
            continue
        opening = [(ex - 22, ey - 6), (ex - 12, ey - 24), (ex + 8, ey - 27), (ex + 22, ey - 14), (ex + 20, ey + 16),
                   (ex + 6, ey + 26), (ex - 12, ey + 24), (ex - 22, ey + 8)]
        p.poly(opening, (250, 252, 255), None)
        cx = ex + 6 * look
        iris = _clip_convex(opening[::-1], [(cx + 15 * math.cos(a), ey + 3 + 21 * math.sin(a))
                                            for a in np.linspace(0, 2 * math.pi, 24, endpoint=False)])
        if len(iris) >= 3:
            p.poly(iris, C_IRIS, None)
        p.ell(cx, ey + 6, 7, 10, (10, 20, 64), None)
        p.ell(cx - 5, ey - 5, 5, 6, (255, 255, 255), None)                                     # the gloss
        p.ell(cx + 5, ey + 12, 2.4, 2.4, (255, 255, 255), None)
        lash = [(ex - 23, ey - 6), (ex - 12, ey - 25), (ex + 8, ey - 28), (ex + 24, ey - 14)]
        p.line(lash, INK, 5)
        p.line([(ex + sg * 22 if sg > 0 else ex - 23, ey - 14 if sg > 0 else ey - 6),
                (ex + sg * 30, ey - 22)], INK, 3.4)                                              # the outer flick
        p.line([(ex - 12, ey + 25), (ex + 8, ey + 25)], INK, 1.8)
        p.line([(ex - 18, ey - 44), (ex + 16, ey - 48)], C_HAIR, 3)                              # a thin brow
    p.line([(hx + 3, hy + 40), (hx - 1, hy + 48)], C_SKIN_D, 2.4)                              # the nose: a tick
    m, my = st['mouth'], hy + 70
    if m == 'rest':
        p.line([(hx - 8, my), (hx + 8, my)], INK, 2.4)
    elif m == 'smile':
        p.line(open_curve([(hx - 14, my - 3), (hx, my + 6), (hx + 14, my - 3)], 3), INK, 2.6)
    else:
        mouths.draw(p, {}, hx, my - 2, m)
    # locks in front of the ears, then the fringe: cut straight with one long lock swept across
    for sg in (-1, 1):
        if turned and sg < 0:
            continue
        lock = [(hx + sg * 62, hy - 70), (hx + sg * 80, hy - 20), (hx + sg * 74, hy + 60), (hx + sg * 62, hy + 96),
                (hx + sg * 56, hy + 50), (hx + sg * 58, hy - 20)]
        p.poly(curve(lock, 3), C_HAIR, INK, 3)
    fringe = [(hx - 76, hy - 40), (hx - 70, hy - 96), (hx - 20, hy - 124), (hx + 40, hy - 118), (hx + 78, hy - 84),
              (hx + 76, hy - 36), (hx + 56, hy - 58), (hx + 40, hy - 30), (hx + 24, hy - 56), (hx + 4, hy - 34),
              (hx - 14, hy - 4), (hx - 22, hy - 50), (hx - 44, hy - 40), (hx - 58, hy - 58)]
    p.poly(curve(fringe, 3), C_HAIR, INK, 3)
    p.line(open_curve([(hx - 34, hy - 100), (hx - 6, hy - 92), (hx + 20, hy - 100)], 3), C_HAIR_L, 3.4)   # shine
    if turned:                                    # her far side hidden under the back of her bob
        p.poly(rough(curve([(hx - sh - 104, hy + 90), (hx - sh - 108, hy - 30), (hx - sh - 60, hy - 112),
                            (hx - 20, hy - 108), (hx - 30, hy - 30), (hx - 44, hy + 60), (hx - 40, hy + 100),
                            (hx - sh - 60, hy + 104)], 4), 1.5, 71), C_HAIR, INK, 3)


def _cortana_back(p, st):
    """Turned away, the hip popped, looking back over her right shoulder at Musk (our right)."""
    hip = (st['hip'] or 0.8) * 20
    _legs(p, hip)
    p.poly(curve(_body_outline(0.0, hip), 4), C_SUIT, INK, 3.4)
    # the seat: two round forms, inked underneath and down the middle (a cringe pose, never explicit)
    for sg in (-1, 1):
        bx, by, rx, ry = sg * 54 + hip, 430, 64, 54
        p.ell(bx, by, rx, ry, C_SUIT, None)
        p.ell(bx - sg * 4, by - 18, rx * 0.56, ry * 0.4, C_SUIT_L, None)
        p.line([(bx + rx * math.cos(a), by + ry * math.sin(a)) for a in np.linspace(0.05 * math.pi, 0.95 * math.pi, 14)],
               INK, 2.8)
    p.line(open_curve([(hip, 380), (hip, 430), (hip, 470)], 3), INK, 2.4)
    p.line([(0, 20), (0, 270)], C_LINE, 3)                                                      # the back seam
    p.line(open_curve([(-46, 80), (-20, 120), (-30, 170)], 3), C_SUIT_D, 2.4)                   # shoulder blades
    p.line(open_curve([(46, 80), (20, 120), (30, 170)], 3), C_SUIT_D, 2.4)
    p.poly(curve([(-58, 270), (0, 280), (58, 270), (60, 296), (0, 306), (-60, 296)], 3), C_LINE, INK, 2.4)
    p.poly(curve([(-30, -14), (30, -14), (34, 22), (-34, 22)], 3), C_SUIT_D, INK, 3)
    _c_arms(p, st, cortana_arms('turn'))
    _cortana_head(p, dict(st, look=1.0), 6, -150, turned=1.0)


# ================================================== THE SHEET ======================================================
def _label(img, x, y, s, size=34, fill=(255, 255, 255)):
    f = ImageFont.truetype(SANS, size * B.SS)
    ImageDraw.Draw(img).text((x * B.SS, y * B.SS), s, font=f, fill=fill)


def sheet(out):
    """The cast sheet: Musk at the two-shot's size and close up (faces: serious, talking, glancing at Cortana, the
    yoke turned); Cortana in every pose, and beside him to scale."""
    tiles = []
    # 1. Musk two-shot size, yoke straight; 2. yoke turned
    for turn, lab in ((0, 'Musk, yoke straight'), (-22, 'yoke turned (back and forth)')):
        img = B.canvas((24, 24, 30))
        chief(img, B.Cam(1.0, 540, 960), 540, 900, 1.05, dict(turn=turn, mouth='rest' if turn == 0 else 'E'))
        tiles.append((lab, img))
    # 3-5. close-ups of the face: serious, talking, glancing at Cortana (our left)
    for st, lab in ((dict(), 'close-up: serious'), (dict(mouth='AI'), 'talking'), (dict(look=-1.0, mouth='E'), 'glance at Cortana')):
        img = B.canvas((24, 24, 30))
        chief(img, B.Cam(1.0, 540, 960), 540, 1180, 2.9, dict(st, yoke=False))
        tiles.append((lab, img))
    # 6-9. Cortana's poses
    for pose, lab, extra in (('appear', 'Cortana appears', dict(mouth='O')), ('point', '"Oh, Musker Chief"', dict(mouth='O', hip=-0.8)),
                             ('kawaii', '"Le Epic Chungus" (chest out)', dict(mouth='E', wink=True, lean=-4, chest=1.0)),
                             ('turn', '"Kawaiii!!" (turned away)', dict(mouth='AI'))):
        img = B.canvas((14, 16, 30))
        cortana(img, B.Cam(1.0, 540, 960), 540, 620, 0.95, dict(extra, pose=pose), t=1.0)
        tiles.append((lab, img))
    # 10. beside him to scale (about a third of his height, standing in mid-air over the passenger seat)
    img = B.canvas((24, 24, 30))
    chief(img, B.Cam(1.0, 540, 960), 700, 900, 0.8, dict(look=-1.0))
    cortana(img, B.Cam(1.0, 540, 960), 230, 760, 0.42, dict(pose='point', hip=-0.8), t=1.0)
    tiles.append(('to scale (Cortana about 0.6 m)', img))
    W, H, band = 432, 768, 50
    cols = 5
    S = Image.new('RGB', (cols * (W + 8) + 8, 2 * (H + band) + 8), (36, 36, 36))
    d = ImageDraw.Draw(S)
    f = ImageFont.truetype(SANS, 20)
    for i, (lab, im) in enumerate(tiles):
        cx, cy = 8 + (i % cols) * (W + 8), (i // cols) * (H + band)
        S.paste(im.convert('RGB').resize((W, H), Image.LANCZOS), (cx, cy + band))
        d.text((cx + 4, cy + 14), f'{i + 1}. {lab}', font=f, fill=(255, 255, 255))
    S.save(out, quality=90)
    print('wrote', out)


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
    else:
        print(__doc__)
