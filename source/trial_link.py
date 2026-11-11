#!/usr/bin/env python3
"""trial_link: Young Link (the 2026 remake's design) rebuilt from scratch for the budget trial (notes/trial_link.md).
A 9-year-old Lead in the flat house style on views.person: front, side and back (no three-quarter: rule 38).

MAP
  colours ............ top (skin, hair, cap, tunic, leather, boots)
  eyes, brows, mouths  _eye, _brow, _mouth (the seven faces read MOODS)
  head, front ........ head_front (cap tail, face, hair, ears, eyes, cap)
  head, side ......... head_side (profile facing right)
  head, back ......... head_back (the woven cap with its spiral, ears, hair)
  body ............... body (shirt collar, tunic panel, strap, belt, buckle, fringe; shield from behind and side),
                       shield_front (the shield's edge behind him, front on: j['pre'])
  arms, legs ......... arm (short frayed sleeves), leg (boots with folded cuffs): hooks on views
  the hooks .......... install(): B.head, V.head_view, V.arm, V.leg for who == 'link'
  poses .............. pose(name, t): standing, shrug, cheeks, scuttle, collar
  person ............. person(img, cam, x, floor, s, ...): s is the scale of a 1.75 m adult; Link is 1.33 m
  sheet .............. sheet(out): turnaround, poses, faces, beside references 03 and 04

    python3 source/trial_link.py sheet OUT.jpg
    python3 source/trial_link.py faces OUT.jpg          (the faces at full size)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import mouths                    # noqa: E402
import views as V                # noqa: E402
import moves as MV               # noqa: E402
import eyekit                    # noqa: E402
from ed import INK, curve, oval  # noqa: E402
from satire_style import install_circle_hands   # noqa: E402

mouths.install(B)
install_circle_hands(B)
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')

# ------------------------------------------------------------------------------------------------ colours
SKIN = (248, 214, 180)
BLUSH = (240, 170, 150)
HAIR = (226, 176, 72)            # golden blond (04)
HAIR_D = (176, 122, 44)
HAIR_L = (246, 208, 120)
BROW = (128, 76, 30)             # darker than the hair so the brows read over the fringe
IRIS = (64, 118, 206)            # big blue eyes
IRIS_D = (36, 70, 140)
CAP = (92, 132, 50)              # the woven green cap
CAP_D = (60, 92, 34)
CAP_L = (128, 168, 72)
BAND = (70, 100, 40)
BEAD_R, BEAD_B = (214, 52, 36), (120, 66, 34)
TUNIC = (88, 136, 52)            # the woven green tunic
TUNIC_D = (62, 100, 40)
SHIRT = (132, 176, 76)           # the lighter knit shirt and its collar (04)
LEATHER = (120, 72, 38)
LEATHER_D = (84, 50, 26)
SILVER = (198, 200, 204)
TIGHTS = (236, 222, 196)
BOOT = (104, 66, 36)
CUFF = (196, 158, 106)
WOOD, WOOD_D = (132, 84, 44), (92, 58, 30)

HEIGHT = 1.33                    # a 9-year-old
TOP = 1199.0                     # units from the cap's top to the soles (measured off the drawing)


def lerp(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


# ------------------------------------------------------------------------------------------------ faces
# per mood: brows (inner_dy, outer_dy) for screen-left and screen-right brow (negative = up), lid (0 open .. 0.7),
# eye scale, pupil share of the iris, look (-1 .. 1 across), gaze_dy, squeeze (eyes shut tight), mouth
MOODS = {
    'neutral':    dict(brows=((0, 0), (0, 0)), lid=0.08, mouth='rest'),
    'unsure':     dict(brows=((-22, -2), (-22, -2)), lid=0.0, look=-0.25, mouth='unsure'),
    'sceptical':  dict(brows=((10, 8), (-26, -32)), lid=0.18, look=1.0, mouth='side'),
    'aghast':     dict(brows=((-20, -16), (-20, -16)), lid=0.0, scale=1.12, pupil=0.3, mouth='wide'),
    'wince':      dict(brows=((10, -2), (10, -2)), squeeze=True, mouth='grit'),
    'horror':     dict(brows=((-24, -6), (-24, -6)), lid=0.0, scale=1.06, pupil=0.2, mouth='small_o'),
    'deadpan':    dict(brows=((4, 4), (4, 4)), lid=0.64, mouth='flat'),
    'terrified':  dict(brows=((-20, -4), (-20, -4)), lid=0.0, scale=1.08, pupil=0.3, mouth='wobble', tear=True),
}


def _mood(sp):
    m = dict(MOODS.get(sp.get('mood', 'neutral'), MOODS['neutral']))
    for k in ('lid', 'look', 'gaze_dy', 'mouth', 'brows'):
        if k in sp and sp[k] is not None and not (k == 'mouth' and sp[k] is None):
            m[k] = sp[k]
    return m


def _eye_outline(ex, ey, w, h, lid=0.0):
    """The eye's opening (convex): an oval, the top cut down by the lid."""
    us = np.linspace(-1, 1, 17)
    up = [(ex + w * u, ey - h * math.sqrt(max(0.0, 1 - u * u)) * (1 - lid)) for u in us]
    lo = [(ex + w * u, ey + h * 0.86 * math.sqrt(max(0.0, 1 - u * u))) for u in us]
    return up + lo[::-1][1:-1], up, lo


def _eye(p, ex, ey, w, h, m, sgn, skin, t=0.0):
    """A big round eye: white, a big blue iris with a dark rim, pupil and two shines, all cut to the opening; a thick
    upper lid line with a flick at the outer corner."""
    if m.get('squeeze'):                                  # shut tight: a sideways chevron, > <
        p.line([(ex - sgn * w * 0.9, ey - h * 0.5), (ex + sgn * w * 0.6, ey + 2), (ex - sgn * w * 0.9, ey + h * 0.45)],
               INK, 3.4)
        return
    lid = m.get('lid', 0.0)
    outline, up, lo = _eye_outline(ex, ey, w, h, lid)
    p.poly(outline, (252, 252, 250), None)
    look, gdy = m.get('look', 0.0), m.get('gaze_dy', 0.0)
    r = min(w, h) * 0.8
    cx, cy = ex + look * w * 0.48, ey + 3 + gdy * h * 0.3 + lid * h * 0.25
    eyekit.iris_and_pupil(p, outline, cx, cy, r, IRIS_D, None, shine=None)
    eyekit.iris_and_pupil(p, outline, cx, cy, r * 0.84, IRIS, r * m.get('pupil', 0.44), shine=(-0.34, -0.38, 0.3))
    eyekit.iris_and_pupil(p, outline, cx, cy, 0.0, None, None, shine=(0.36, 0.34, 0.12))
    if lid > 0.02:                                        # the lid: skin down to its edge, a crease above
        full = [(ex + w * u, ey - h * math.sqrt(max(0.0, 1 - u * u))) for u in np.linspace(-1, 1, 17)]
        p.poly(full + up[::-1], skin, None)
        p.line(full[3:-3], B.dk(skin, 0.8), 1.4)
    p.line(lo[3:-3], B.dk(skin, 0.7), 1.6)
    p.line(up, INK, 3.6)
    tip = up[-1] if sgn > 0 else up[0]
    p.line([tip, (tip[0] + sgn * 8, tip[1] - 6)], INK, 3.0)
    if m.get('tear') and sgn > 0:                         # one tear welling at the lower lid (terrified)
        p.ell(ex + w * 0.5, ey + h * 0.95 + 10, 7.5, 11, (180, 220, 250), INK, 1.8)
        p.line([(ex + w * 0.5, ey + h * 0.95 + 22), (ex + w * 0.56, ey + h * 0.95 + 40)], (150, 200, 240), 3.0)


def _brow(p, ex, ey, sgn, inner, outer, length=30, c=BROW, w=6.0):
    a = (ex - sgn * length * 0.5, ey + inner)
    b = (ex + sgn * length * 0.55, ey + outer)
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 4)
    p.poly(curve([(a[0], a[1] - w * 0.5), (m[0], m[1] - w * 0.6), (b[0], b[1] - w * 0.2), (b[0], b[1] + w * 0.2),
                  (m[0], m[1] + w * 0.5), (a[0], a[1] + w * 0.5)], 3), c, None)


DARK, TEETH, TONGUE, LIP = (92, 34, 40), (250, 248, 242), (214, 108, 112), (206, 120, 112)


def _mouth(p, sp, fx, my, m, t=0.0):
    name = m.get('mouth', 'rest') or 'rest'
    if name.startswith('v:'):                             # talking (the film's mouth shapes), a child's small mouth
        mouths.draw(p, dict(sp, lips=False), fx, my, name[2:])
        return
    if name == 'rest':
        p.line(curve([(fx - 11, my), (fx, my + 2), (fx + 11, my)], 3)[:-6], INK, 2.4)
    elif name == 'half':                                  # a crooked half smile, one corner up
        p.line([(fx - 13, my + 1), (fx - 3, my + 4), (fx + 8, my + 1), (fx + 15, my - 5)], INK, 2.6)
    elif name == 'unsure':                                # a wavering line, one corner up, one down: not a grin
        p.line(curve([(fx - 14, my + 4), (fx - 6, my + 1), (fx + 2, my + 4), (fx + 9, my + 1), (fx + 15, my - 3)], 3),
               INK, 2.6)
    elif name == 'side':                                  # pursed off to one side (sceptical)
        p.line([(fx - 4, my + 1), (fx + 8, my + 1), (fx + 17, my - 2)], INK, 2.8)
        p.line([(fx - 4, my + 1), (fx - 9, my + 4)], INK, 2.2)
    elif name == 'flat':                                  # dead flat
        p.line([(fx - 13, my + 1), (fx + 13, my + 1)], INK, 2.8)
    elif name == 'wide':                                  # aghast: a tall open oval, top teeth, tongue
        o = oval(fx, my + 10, 21, 28, 40)
        p.poly(o, DARK, INK, 2.6)
        p.poly([(x, y) for x, y in oval(fx, my + 22, 11, 8, 30, math.pi, 2 * math.pi)], TONGUE, None)
        p.poly([(fx - 12, my - 10), (fx + 12, my - 10), (fx + 10, my - 4), (fx - 10, my - 4)], TEETH, None)
        p.poly(o, None, INK, 2.6)
    elif name == 'grit':                                  # wince: teeth clenched, corners pulled down and out
        box = curve([(fx - 22, my + 2), (fx, my - 4), (fx + 22, my + 2), (fx + 18, my + 10), (fx, my + 12),
                     (fx - 18, my + 10)], 3)
        p.poly(box, TEETH, INK, 2.6)
        p.line([(fx - 20, my + 4), (fx + 20, my + 4)], (150, 140, 140), 1.6)
        for x in (-10, 0, 10):
            p.line([(fx + x, my - 2), (fx + x, my + 10)], (150, 140, 140), 1.2)
        p.line([(fx - 22, my + 2), (fx - 27, my + 8)], INK, 2.2)
        p.line([(fx + 22, my + 2), (fx + 27, my + 8)], INK, 2.2)
    elif name == 'small_o':                               # flat horror: a small, stiff, downturned opening
        box = [(fx - 20, my + 10), (fx - 10, my + 2), (fx + 10, my + 2), (fx + 20, my + 10), (fx + 12, my + 14),
               (fx - 12, my + 14)]                        # a stiff, downturned grimace, teeth showing
        p.poly(box, DARK, INK, 2.4)
        p.poly([(fx - 10, my + 3), (fx + 10, my + 3), (fx + 9, my + 7), (fx - 9, my + 7)], TEETH, None)
        p.line([(fx - 20, my + 10), (fx - 25, my + 17)], INK, 2.2)
        p.line([(fx + 20, my + 10), (fx + 25, my + 17)], INK, 2.2)
    elif name == 'wobble':                                # terrified: open, the lower lip trembling (moves with t)
        ph = t * 26.0
        top = [(fx - 18, my + 4), (fx - 8, my - 2), (fx, my - 1), (fx + 8, my - 2), (fx + 18, my + 4)]
        low = [(fx + 18 - 36 * i / 8, my + 10 + 3.2 * math.sin(i * 1.9 + ph)) for i in range(9)]
        p.poly(top + low, DARK, None)
        p.poly([(fx - 8, my - 1), (fx + 8, my - 1), (fx + 7, my + 3), (fx - 7, my + 3)], TEETH, None)
        p.line(top, INK, 2.6)
        p.line(low, INK, 2.6)
        p.line([(fx - 18, my + 4), (fx - 22, my + 10)], INK, 2.0)
        p.line([(fx + 18, my + 4), (fx + 22, my + 10)], INK, 2.0)


# ------------------------------------------------------------------------------------------------ the cap
def _weave(p, pts, c, step=16, seed=3):
    """A few short criss-cross strokes inside a shape's box: the woven look, kept sparse (flat style)."""
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    r = np.random.default_rng(seed)
    from matplotlib.path import Path
    path = Path(pts)
    for _ in range(int((max(xs) - min(xs)) * (max(ys) - min(ys)) / (step * step * 6))):
        x, y = r.uniform(min(xs), max(xs)), r.uniform(min(ys), max(ys))
        if path.contains_point((x, y)) and path.contains_point((x + 8, y + 8)):
            s = 1 if r.random() < 0.5 else -1
            p.line([(x, y), (x + 10, y + 10 * s)], c, 2.4)


def _beads(p, pts, n):
    """Beads spaced evenly by length along the band (big and red enough to read at phone size: hunt 1)."""
    a = np.array(pts, float)
    d = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(a, axis=0).T))])
    for i in range(n):
        k = (i + 0.5) / n * d[-1]
        x, y = np.interp(k, d, a[:, 0]), np.interp(k, d, a[:, 1])
        p.ell(x, y, 7.5, 7.5, BEAD_R if i % 3 != 2 else BEAD_B, INK, 1.6)


# ------------------------------------------------------------------------------------------------ head, front
def head_front(img, p, sp, t, hx, hy):
    hw, hh, skin = sp['hw'], sp['hh'], sp['skin']
    m = _mood(sp)
    fx = hx + sp.get('turn', 0.0) * hw * 0.15
    # the cap's floppy body, behind the head: up over the crown and down behind to his left (screen right)
    tail = [(hx - hw * 0.7, hy - hh * 0.9), (hx - hw * 0.2, hy - hh * 1.22), (hx + hw * 0.6, hy - hh * 1.24),
            (hx + hw * 1.2, hy - hh * 1.02), (hx + hw * 1.42, hy - hh * 0.6), (hx + hw * 1.38, hy - hh * 0.2),
            (hx + hw * 1.22, hy - hh * 0.05), (hx + hw * 1.06, hy - hh * 0.3), (hx + hw * 0.7, hy - hh * 0.7)]
    tp = curve(tail, 4)
    p.poly(tp, CAP_D, INK, 2.6)
    _weave(p, tp, B.dk(CAP_D, 0.75), seed=5)
    # the face: round and full-cheeked, a small chin
    face = curve([(hx - hw * 0.98, hy - hh * 0.1), (hx - hw * 0.9, hy - hh * 0.68), (hx - hw * 0.5, hy - hh * 0.98),
                  (hx, hy - hh * 1.04), (hx + hw * 0.5, hy - hh * 0.98), (hx + hw * 0.9, hy - hh * 0.68),
                  (hx + hw * 0.98, hy - hh * 0.1), (hx + hw * 0.98, hy + hh * 0.34), (hx + hw * 0.8, hy + hh * 0.72),
                  (hx + hw * 0.42, hy + hh * 0.96), (hx, hy + hh * 1.02), (hx - hw * 0.42, hy + hh * 0.96),
                  (hx - hw * 0.8, hy + hh * 0.72), (hx - hw * 0.98, hy + hh * 0.34)], 4)
    p.poly(face, skin, INK, 2.6)
    for sg in (-1, 1):                                   # rosy cheeks
        p.ell(fx + sg * hw * 0.6, hy + hh * 0.5, hw * 0.16, hh * 0.08, lerp(skin, BLUSH, 0.45), None)
    # hair: a blond bowl cut, the sides down to the jaw, a pointed fringe swept to his left
    top = hy - hh * 1.14
    outer = [(hx - hw * 1.02, hy + hh * 0.66), (hx - hw * 1.1, hy + hh * 0.1), (hx - hw * 1.06, hy - hh * 0.6),
             (hx - hw * 0.6, top + 10), (hx, top), (hx + hw * 0.6, top + 10), (hx + hw * 1.06, hy - hh * 0.6),
             (hx + hw * 1.1, hy + hh * 0.1), (hx + hw * 1.02, hy + hh * 0.66)]
    inner = [(hx + hw * 0.9, hy + hh * 0.5), (hx + hw * 0.84, hy - hh * 0.05), (hx + hw * 0.8, hy - hh * 0.36)]
    fringe = []
    for i in range(9):                                    # points hanging over the brow, longer to screen left
        u = i / 8
        x = hx + hw * (0.78 - 1.56 * u)
        y = hy - hh * 0.42 + (hh * (0.16 + 0.06 * u) if i % 2 == 0 else hh * 0.0)
        fringe.append((x, y))
    inner += fringe + [(hx - hw * 0.82, hy - hh * 0.3), (hx - hw * 0.84, hy + hh * 0.05), (hx - hw * 0.9, hy + hh * 0.5)]
    hair = outer + inner
    p.poly(hair, sp.get('hair_c', HAIR), INK, 2.6)
    for k in range(6):                                    # strands
        x0 = hx - hw * 0.6 + k * hw * 0.24
        p.line([(x0, hy - hh * 0.75), (x0 - 6 + 2 * k, hy - hh * 0.36)], HAIR_D, 1.6)
    for sg in (-1, 1):
        p.line([(hx + sg * hw * 0.98, hy - hh * 0.2), (hx + sg * hw * 0.96, hy + hh * 0.5)], HAIR_D, 1.6)
        p.line([(hx + sg * hw * 0.9, hy - hh * 0.5), (hx + sg * hw * 0.86, hy - hh * 0.1)], HAIR_L, 2.0)
    # ears: long and pointed, out to the sides and a little up, through the hair
    for sg in (-1, 1):
        ear = curve([(hx + sg * hw * 0.98, hy - hh * 0.02), (hx + sg * hw * 1.32, hy - hh * 0.12),
                     (hx + sg * hw * 1.66, hy - hh * 0.3), (hx + sg * hw * 1.4, hy + hh * 0.08),
                     (hx + sg * hw * 1.12, hy + hh * 0.3), (hx + sg * hw * 1.0, hy + hh * 0.3)], 3)
        p.poly(ear, skin, INK, 2.6)
        p.line([(hx + sg * hw * 1.1, hy + hh * 0.14), (hx + sg * hw * 1.36, hy - hh * 0.06),
                (hx + sg * hw * 1.52, hy - hh * 0.2)], lerp(skin, BLUSH, 0.6), 2.4)
    # eyes, brows, nose, mouth
    sc = m.get('scale', 1.0)
    ew, eh = hw * 0.25 * sc, hw * 0.29 * sc
    ey = hy + hh * 0.17
    for sg in (-1, 1):
        _eye(p, fx + sg * hw * 0.42, ey, ew, eh, m, sg, skin, t)
    (il, ol), (ir, orr) = m['brows']
    _brow(p, fx - hw * 0.42, ey - eh - 13, -1, il, ol)
    _brow(p, fx + hw * 0.42, ey - eh - 13, 1, ir, orr)
    ny = hy + hh * 0.5
    p.line([(fx - 3, ny - 7), (fx + 5, ny), (fx - 2, ny + 4)], B.dk(skin, 0.72), 2.0)
    _mouth(p, sp, fx, hy + hh * 0.72, m, t)
    # the cap over the hair: a woven band with red and brown beads, the crown rising out of it
    band_top = [(hx - hw * 1.06, hy - hh * 0.5), (hx - hw * 0.5, hy - hh * 0.8), (hx, hy - hh * 0.86),
                (hx + hw * 0.5, hy - hh * 0.8), (hx + hw * 1.06, hy - hh * 0.5)]
    band_bot = [(x, y + 16) for x, y in band_top]
    crown = curve([band_top[0], (hx - hw * 0.98, hy - hh * 1.0), (hx - hw * 0.5, hy - hh * 1.26),
                   (hx + hw * 0.2, hy - hh * 1.32), (hx + hw * 0.86, hy - hh * 1.18), (hx + hw * 1.1, hy - hh * 0.82),
                   band_top[-1], band_top[3], band_top[2], band_top[1]], 4)
    p.poly(crown, CAP, INK, 2.6)
    _weave(p, crown, B.dk(CAP, 0.62), step=12, seed=7)
    p.line([(hx + hw * 0.2, hy - hh * 1.3), (hx + hw * 0.7, hy - hh * 1.0)], CAP_D, 2.0)   # the fold
    bt = curve(band_top, 3)[:-8]
    bb = curve(band_bot, 3)[:-8]
    p.poly(bt + bb[::-1], BAND, INK, 2.4)
    for i in range(0, len(bt) - 2, 3):                    # the band's weave: little chevrons
        x, y = bt[i]
        p.line([(x - 3, y + 4), (x + 2, y + 9), (x - 3, y + 13)], B.dk(BAND, 0.7), 1.4)
    _beads(p, [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(bt, bb)], 7)
    for i in range(0, len(bb), 2):                        # frayed edge under the band
        x, y = bb[i]
        p.line([(x, y), (x + 1, y + 6)], CAP_D, 1.4)
    return fx


# ------------------------------------------------------------------------------------------------ head, side
def head_side(img, p, sp, t, hx, hy):
    """Profile facing right: the cap flops back behind the head, the long ear points back and up."""
    hw, hh, skin = sp['hw'], sp['hh'], sp['skin']
    m = _mood(sp)
    tail = curve([(hx - hw * 0.2, hy - hh * 1.2), (hx - hw * 0.9, hy - hh * 1.1), (hx - hw * 1.42, hy - hh * 0.62),
                  (hx - hw * 1.56, hy - hh * 0.1), (hx - hw * 1.42, hy + hh * 0.24), (hx - hw * 1.24, hy - hh * 0.08),
                  (hx - hw * 1.0, hy - hh * 0.5), (hx - hw * 0.5, hy - hh * 0.8)], 4)
    p.poly(tail, CAP_D, INK, 2.6)
    _weave(p, tail, B.dk(CAP_D, 0.75), seed=9)
    face = curve([(hx - hw * 0.92, hy + hh * 0.1), (hx - hw * 0.86, hy - hh * 0.6), (hx - hw * 0.3, hy - hh * 1.02),
                  (hx + hw * 0.4, hy - hh * 0.96), (hx + hw * 0.78, hy - hh * 0.5), (hx + hw * 0.84, hy - hh * 0.02),
                  (hx + hw * 0.9, hy + hh * 0.34), (hx + hw * 0.98, hy + hh * 0.46), (hx + hw * 0.9, hy + hh * 0.56),
                  (hx + hw * 0.86, hy + hh * 0.7), (hx + hw * 0.8, hy + hh * 0.86), (hx + hw * 0.5, hy + hh * 0.98),
                  (hx + hw * 0.1, hy + hh * 0.92), (hx - hw * 0.3, hy + hh * 0.74), (hx - hw * 0.7, hy + hh * 0.5)], 4)
    p.poly(face, skin, INK, 2.6)
    p.ell(hx + hw * 0.52, hy + hh * 0.5, hw * 0.16, hh * 0.08, lerp(skin, BLUSH, 0.45), None)
    # hair: the back and top, a sideburn in front of the ear down to the jaw, the fringe at the brow
    hair = curve([(hx - hw * 0.98, hy + hh * 0.66), (hx - hw * 1.04, hy - hh * 0.1), (hx - hw * 0.9, hy - hh * 0.8),
                  (hx - hw * 0.3, hy - hh * 1.14), (hx + hw * 0.5, hy - hh * 1.06), (hx + hw * 0.9, hy - hh * 0.62),
                  (hx + hw * 0.88, hy - hh * 0.3), (hx + hw * 0.7, hy - hh * 0.38), (hx + hw * 0.66, hy - hh * 0.2),
                  (hx + hw * 0.5, hy - hh * 0.36), (hx + hw * 0.24, hy - hh * 0.3), (hx + hw * 0.18, hy + hh * 0.2),
                  (hx + hw * 0.2, hy + hh * 0.66), (hx - hw * 0.1, hy + hh * 0.58), (hx - hw * 0.5, hy + hh * 0.7)], 3)
    p.poly(hair, sp.get('hair_c', HAIR), INK, 2.6)
    for k in range(4):
        x0 = hx - hw * 0.7 + k * hw * 0.24
        p.line([(x0, hy - hh * 0.6), (x0 - 8, hy + hh * 0.3)], HAIR_D, 1.6)
    # the ear: long, pointing back and up from in front of the hair's edge
    ear = curve([(hx + hw * 0.02, hy - hh * 0.02), (hx - hw * 0.4, hy - hh * 0.2), (hx - hw * 0.86, hy - hh * 0.46),
                 (hx - hw * 0.6, hy - hh * 0.08), (hx - hw * 0.3, hy + hh * 0.22), (hx + hw * 0.04, hy + hh * 0.26)], 3)
    p.poly(ear, skin, INK, 2.6)
    p.line([(hx - hw * 0.06, hy + hh * 0.1), (hx - hw * 0.38, hy - hh * 0.04), (hx - hw * 0.62, hy - hh * 0.22)],
           lerp(skin, BLUSH, 0.6), 2.4)
    # one big eye seen from the side: a narrower opening, the iris to the front
    sc = m.get('scale', 1.0)
    ex, ey = hx + hw * 0.6, hy + hh * 0.17
    _eye(p, ex, ey, hw * 0.14 * sc, hw * 0.28 * sc, dict(m, look=0.7), 1, skin, t)
    (_, _), (ir, orr) = m['brows']
    _brow(p, ex, ey - hw * 0.28 * sc - 13, 1, ir, orr, length=22)
    mo = m.get('mouth', 'rest') or 'rest'
    mx, my = hx + hw * 0.84, hy + hh * 0.72
    if mo.startswith('v:') or mo in ('wide', 'small_o', 'wobble', 'grit'):    # open: a dark wedge back from the lips
        big = 16 if mo == 'wide' else 9
        wob = 2.5 * math.sin(t * 26.0) if mo == 'wobble' else 0.0
        p.poly([(mx + 4, my - 5), (mx - 12, my), (mx + 2, my + big + wob)], DARK, INK, 2.2)
    else:
        p.line([(mx + 4, my), (mx - 10, my + (-3 if mo == 'half' else 2))], INK, 2.4)
    # the band round the head and the crown above it
    band_f, band_b = (hx + hw * 0.86, hy - hh * 0.56), (hx - hw * 0.92, hy - hh * 0.4)
    bt = curve([band_b, (hx - hw * 0.2, hy - hh * 0.74), band_f], 3)[:-8]
    bb = [(x, y + 16) for x, y in bt]
    crown = curve([band_b, (hx - hw * 0.9, hy - hh * 1.0), (hx - hw * 0.3, hy - hh * 1.3), (hx + hw * 0.4, hy - hh * 1.24),
                   (hx + hw * 0.86, hy - hh * 0.9), band_f, (hx - hw * 0.2, hy - hh * 0.74)], 4)
    p.poly(crown, CAP, INK, 2.6)
    _weave(p, crown, B.dk(CAP, 0.62), step=12, seed=11)
    p.poly(bt + bb[::-1], BAND, INK, 2.4)
    _beads(p, [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(bt, bb)], 5)
    return hx + hw * 0.6


# ------------------------------------------------------------------------------------------------ head, back
def head_back(img, p, sp, t, hx, hy):
    """From behind (reference 01): the woven cap covers the crown and hangs down the back of the head, a raised
    spiral on it; the ears stick out both sides; blond hair below the band to the nape."""
    hw, hh, skin = sp['hw'], sp['hh'], sp['skin']
    skull = curve([(hx - hw * 0.98, hy), (hx - hw * 0.9, hy - hh * 0.7), (hx, hy - hh * 1.04),
                   (hx + hw * 0.9, hy - hh * 0.7), (hx + hw * 0.98, hy), (hx + hw * 0.8, hy + hh * 0.7),
                   (hx, hy + hh * 0.9), (hx - hw * 0.8, hy + hh * 0.7)], 4)
    p.poly(skull, skin, INK, 2.6)
    hair = curve([(hx - hw * 1.06, hy + hh * 0.6), (hx - hw * 1.1, hy - hh * 0.4), (hx - hw * 0.7, hy - hh * 1.04),
                  (hx, hy - hh * 1.14), (hx + hw * 0.7, hy - hh * 1.04), (hx + hw * 1.1, hy - hh * 0.4),
                  (hx + hw * 1.06, hy + hh * 0.6), (hx + hw * 0.5, hy + hh * 0.8), (hx, hy + hh * 0.86),
                  (hx - hw * 0.5, hy + hh * 0.8)], 4)
    p.poly(hair, sp.get('hair_c', HAIR), INK, 2.6)
    for k in range(7):
        x0 = hx - hw * 0.8 + k * hw * 0.27
        p.line([(x0, hy - hh * 0.2), (x0 + 3, hy + hh * 0.72)], HAIR_D, 1.6)
    for sg in (-1, 1):                                    # the ears from behind: out and up past the hair
        ear = curve([(hx + sg * hw * 1.0, hy - hh * 0.04), (hx + sg * hw * 1.32, hy - hh * 0.14),
                     (hx + sg * hw * 1.64, hy - hh * 0.32), (hx + sg * hw * 1.4, hy + hh * 0.06),
                     (hx + sg * hw * 1.12, hy + hh * 0.28), (hx + sg * hw * 1.02, hy + hh * 0.28)], 3)
        p.poly(ear, B.dk(skin, 0.94), INK, 2.6)
    band_top = [(hx - hw * 1.08, hy - hh * 0.38), (hx, hy - hh * 0.6), (hx + hw * 1.08, hy - hh * 0.38)]
    bt = curve(band_top, 3)[:-8]
    bb = [(x, y + 16) for x, y in bt]
    # the cap: over the crown, its long floppy body hanging down the back of the head, the tip below the nape
    cap = curve([(hx - hw * 1.08, hy - hh * 0.38), (hx - hw * 1.04, hy - hh * 0.96), (hx - hw * 0.4, hy - hh * 1.3),
                 (hx + hw * 0.5, hy - hh * 1.28), (hx + hw * 1.08, hy - hh * 0.9), (hx + hw * 1.08, hy - hh * 0.38),
                 (hx + hw * 0.7, hy - hh * 0.1), (hx + hw * 0.5, hy + hh * 0.5), (hx + hw * 0.24, hy + hh * 1.16),
                 (hx, hy + hh * 1.3), (hx - hw * 0.26, hy + hh * 1.1), (hx - hw * 0.5, hy + hh * 0.4),
                 (hx - hw * 0.72, hy - hh * 0.12)], 4)
    p.poly(cap, CAP, INK, 2.6)
    _weave(p, cap, CAP_D, step=14, seed=13)
    sx, sy = hx - hw * 0.1, hy - hh * 0.52                 # the raised woven spiral (reference 01)
    spiral = [(sx + (4 + 6.5 * a) * math.cos(a), sy + (4 + 6.5 * a) * math.sin(a) * 0.9)
              for a in np.linspace(0, 4.2 * math.pi, 70)]
    p.line(spiral, INK, 9.0)
    p.line(spiral, CAP_L, 4.0)
    p.poly(bt + bb[::-1], BAND, INK, 2.4)
    _beads(p, [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(bt, bb)], 7)
    for k in range(9):                                    # a frayed tip
        x = hx - hw * 0.2 + k * hw * 0.05
        p.line([(x, hy + hh * 1.18 + (6 if k % 2 else 0)), (x + 1, hy + hh * 1.3 + (6 if k % 2 else 0))], CAP_D, 1.6)
    return hx


# ------------------------------------------------------------------------------------------------ body
def _fringe(p, x0, x1, y, c=TUNIC_D, n=None, dy=20):
    n = n or max(4, int(abs(x1 - x0) / 13))
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        p.line([(x, y - 2), (x + 2, y + dy + (5 if i % 2 else 0))], c, 3.0)


def _strap(p, a, b, w=18):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / n * w / 2, dx / n * w / 2
    p.poly([(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)],
           LEATHER, INK, 2.0)
    for k in range(1, int(n / 14)):                       # the braid: chevrons along it
        u = k * 14 / n
        cx, cy = a[0] + dx * u, a[1] + dy * u
        p.line([(cx + nx * 0.8, cy + ny * 0.8), (cx + dx / n * 6, cy + dy / n * 6), (cx - nx * 0.8, cy - ny * 0.8)],
               LEATHER_D, 1.6)


def _shield(p, cx, top, w, h, edge=False):
    if edge:                                              # seen edge on: a thin slab
        p.poly(curve([(cx - 9, top + 10), (cx, top), (cx + 9, top + 10), (cx + 9, top + h - 20), (cx, top + h),
                      (cx - 9, top + h - 20)], 2), WOOD, INK, 2.4)
        return
    sh = curve([(cx - w, top + h * 0.12), (cx, top), (cx + w, top + h * 0.12), (cx + w * 0.92, top + h * 0.6),
                (cx, top + h), (cx - w * 0.92, top + h * 0.6)], 4)
    p.poly(sh, WOOD, INK, 2.8)
    for k in (-0.5, 0.0, 0.5):                            # planks
        p.line([(cx + k * w, top + h * 0.06), (cx + k * w * 0.9, top + h * 0.92)], WOOD_D, 2.0)
    p.line(curve([(cx - w * 0.82, top + h * 0.16), (cx, top + h * 0.06), (cx + w * 0.82, top + h * 0.16)], 3)[:-6],
           WOOD_D, 3.0)


def body(p, view, sp):
    """Drawn over the torso in its own frame: the shirt collar, the darker tunic panel, the braided strap, the belt
    and buckle, the frayed hem; the shield over his back from behind, edge on from the side."""
    sw, bottom = sp.get('shoulders', 118), sp.get('bottom', 590)
    if view == 'front':
        panel = [(-sw * 0.62, 30), (-30, 30), (0, 96), (30, 30), (sw * 0.62, 30), (sw * 0.76, 360),
                 (sw * B.HEM * 0.98, bottom), (-sw * B.HEM * 0.98, bottom), (-sw * 0.76, 360)]
        p.poly(panel, TUNIC_D, INK, 2.2)
        _weave(p, panel, B.dk(TUNIC_D, 0.75), seed=21)
        p.poly([(-40, 30), (40, 30), (0, 70)], SHIRT, INK, 2.0)
        for sg in (-1, 1):                                # the knit shirt's open collar: wide flat points out to the
            p.poly([(sg * 10, -4), (sg * 66, -8), (sg * 84, 22), (sg * 30, 30)], SHIRT, INK, 2.0)   # sides (not a tie)
        _strap(p, (sw * 0.72, 2), (-sw * 0.7, 380))
        p.poly([(-sw * 0.86, 372), (sw * 0.86, 372), (sw * 0.88, 404), (-sw * 0.88, 404)], LEATHER, INK, 2.2)
        p.ell(0, 388, 22, 20, SILVER, INK, 2.4)
        p.ell(0, 388, 11, 10, LEATHER, INK, 1.6)
        p.line([(0, 380), (14, 388)], INK, 2.4)
        _fringe(p, -sw * B.HEM, sw * B.HEM, bottom)
    elif view == 'side':
        d = 0.6 * sw
        panel = curve([(d * 0.2, 20), (d * 0.86, 30), (d * 1.1, 140), (d * 1.0, 300), (d * 1.0, bottom),
                       (d * 0.1, bottom), (d * 0.2, 300)], 3)
        p.poly(panel, TUNIC_D, INK, 2.2)
        _weave(p, panel, B.dk(TUNIC_D, 0.75), seed=23)
        p.poly([(6, -12), (40, -8), (44, 26), (18, 18)], SHIRT, INK, 2.0)
        _shield(p, -d * 1.06, 6, 0, 420, edge=True)
        _strap(p, (-d * 0.5, 4), (d * 0.86, 380))
        p.poly([(-d * 1.0, 372), (d * 1.04, 372), (d * 1.04, 404), (-d * 1.0, 404)], LEATHER, INK, 2.2)
        p.ell(d * 0.96, 388, 9, 20, SILVER, INK, 2.4)
        _fringe(p, -d * 0.92, d * 1.0, bottom)
    elif view == 'back':
        p.poly([(-sw * 0.88, 372), (sw * 0.88, 372), (sw * 0.9, 404), (-sw * 0.9, 404)], LEATHER, INK, 2.2)
        _strap(p, (-sw * 0.72, 2), (sw * 0.7, 380))
        _shield(p, sw * 0.08, 30, sw * 0.62, 400)
        p.poly([(sw * 0.08 - 50, 40), (sw * 0.08 + 50, 40), (sw * 0.08 + 50, 56), (sw * 0.08 - 50, 56)], LEATHER, INK, 1.8)
        _fringe(p, -sw * B.HEM, sw * B.HEM, bottom)


def shield_front(p, j2, view):
    """Front on: the shield's edge shows past his left side (screen right), behind the body (reference 04)."""
    if view == 'front':
        _shield(p, 118 * 0.8, 70, 118 * 0.5, 340)


def collar_up(p, view, sp):
    """Held by the collar: the shirt's collar bunched up round his neck and under his chin."""
    if view in ('side', 'front'):
        # wrapped round the neck, yanked up behind (towards the grip off-panel): a point and pull folds
        p.poly(curve([(-44, 16), (-54, -40), (-46, -130), (-14, -44), (20, -30), (46, -10), (40, 16)], 3), SHIRT, INK, 2.2)
        for k in range(3):
            p.line([(-34 + 8 * k, 6), (-40 + 4 * k, -100 + 20 * k)], B.dk(SHIRT, 0.75), 1.8)


# ------------------------------------------------------------------------------------------------ the hooks
_head, _head_view, _arm, _leg = B.head, V.head_view, V.arm, V.leg
HEADS = {'front': head_front, 'side': head_side, 'back': head_back}


def head(img, p, sp, t, hx, hy):
    if sp.get('who') == 'link':
        return head_front(img, p, sp, t, hx, hy)
    return _head(img, p, sp, t, hx, hy)


def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
    if sp.get('who') == 'link':
        return HEADS.get(view, head_front)(img, p, sp, t, hx, hy)
    return _head_view(img, p, sp, t, view, hx, hy)


def arm(p, j2, side, sp, shape=None):
    """Bare arms out of short, frayed green sleeves (references 03, 04)."""
    if sp.get('who') != 'link' or V.PROBE:
        return _arm(p, j2, side, sp, shape)
    sh, el = j2['sh' + side], j2['el' + side]
    _arm(p, j2, side, dict(sp, sleeve=sp['skin'], jacket=sp['skin']), shape)
    end = (sh[0] + (el[0] - sh[0]) * 0.5, sh[1] + (el[1] - sh[1]) * 0.5)
    top = (sh[0] - (el[0] - sh[0]) * 0.22, sh[1] - (el[1] - sh[1]) * 0.22)
    dx, dy = end[0] - top[0], end[1] - top[1]
    n = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / n * 38, dx / n * 38
    p.poly([(top[0] + nx, top[1] + ny), (end[0] + nx * 1.05, end[1] + ny * 1.05), (end[0] - nx * 1.05, end[1] - ny * 1.05),
            (top[0] - nx, top[1] - ny)], TUNIC, INK, 2.4)
    for k in range(6):                                    # the frayed cuff
        u = -1 + 2 * k / 5
        x, y = end[0] + nx * u, end[1] + ny * u
        p.line([(x, y), (x + dx / n * 14, y + dy / n * 14)], TUNIC_D, 2.6)


def leg(p, j, side, yaw, sp, from_u=0.0):
    """Pale tights, then brown boots to mid-shin with a folded tan cuff."""
    _leg(p, j, side, yaw, sp, from_u)
    if sp.get('who') != 'link' or from_u:
        return
    knee = V.project(V.knee_of(j, side), yaw)[0]
    foot = V.project(j['foot' + side], yaw)[0]
    top = (foot[0] + (knee[0] - foot[0]) * 0.46, foot[1] + (knee[1] - foot[1]) * 0.46)
    cuff = (foot[0] + (knee[0] - foot[0]) * 0.6, foot[1] + (knee[1] - foot[1]) * 0.6)
    V.tube(p, [top, foot], [31, 30], BOOT)
    V.tube(p, [top, cuff], [36, 37], CUFF)
    p.line([((top[0] + cuff[0]) / 2 - 18, (top[1] + cuff[1]) / 2), ((top[0] + cuff[0]) / 2 + 18, (top[1] + cuff[1]) / 2)],
           B.dk(CUFF, 0.8), 1.6)


def install():
    B.head, V.head_view, V.arm, V.leg = head, head_view, arm, leg


install()

LINK = dict(who='link', name='Link', skin=SKIN, hw=100, hh=108, head_dy=10, hair='crop', hair_c=HAIR, brow_c=BROW,
            shoulders=118, outfit='jumper', jacket=TUNIC, sleeve=TUNIC, trousers=TIGHTS, shoe=BOOT, bottom=590,
            full=True, pose='custom', seed=31)


# ------------------------------------------------------------------------------------------------ poses
def pose(name, t=0.0):
    """Link's poses (torso frame units). Returns the joints dict."""
    sp = LINK
    hy = -150.0 + sp['head_dy']
    hw, hh = sp['hw'], sp['hh']
    if name == 'shrug':
        j = stand(sp)                                     # elbows tucked at his sides, forearms out, palms up;
        for sd, sg in (('L', -1), ('R', 1)):              # head sunk between the shoulders and tipped
            V.arm_to(j, sd, (sg * (sp['shoulders'] + 140), 200.0, 90.0), 'back', 'palm')
        j['head_dy'] = 18
        j['head_roll'] = 9
    elif name == 'cheeks':                                # hands to his cheeks, jolting back
        j = V.standing(sp)
        for sd, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, sd, (sg * hw * 0.62, hy + hh * 0.62, 190.0), (1.0, 1.0, 0.0), 'palm')
        j['on_face'] = {'L', 'R'}
        j['lean'] = -12
        j['nod'] = -1.4                                   # the jolt: chin up, head back
        j['head_dy'] = -8
    elif name == 'scuttle':                               # a crouched front-on scuttle, hands clamped over his ears
        j = MV.gait(dict(sp), t, 'front_run')
        crouch = 150.0
        j['bob'] = crouch                                 # a held still: no run bounce, soles on the floor
        for sd, sg in (('L', -1), ('R', 1)):
            fx, fy, fz = j['foot' + sd]
            j['foot' + sd] = (fx + sg * 24, fy - crouch, fz)
            j['knee_pole' + sd] = (0.35 * sg, 0.0, 0.94)
        j['lean'] = 10
        j['nod'] = 1.2                                    # head ducked
        j['head_dy'] = 16
        for sd, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, sd, (sg * hw * 1.02, hy + hh * 0.06, 16.0), (0.5, 0.4, 0.9), 'palm')
        j['on_face'] = {'L', 'R'}
    elif name == 'collar':                                # held up by the collar, side on: feet dangling, toes down
        j = V.standing(sp)
        j['footL'] = (-30, V.ANKLE_Y - 10, 18.0)          # legs hanging together, a little forward: limp
        j['footR'] = (30, V.ANKLE_Y - 16, 30.0)
        j['toeL'] = j['toeR'] = -40
        for sd, tgt in (('L', (-30.0, 380.0, 60.0)), ('R', (30.0, 370.0, 90.0))):
            V.arm_to(j, sd, tgt, 'back', 'palm')          # arms hang limp
        j['body_props'] = [collar_up]
        j['head_dy'] = 2
    else:
        j = stand(sp)
    return j


def stand(sp=None):
    """Standing relaxed: elbows a little bent and back, hands a touch in front of the hips (hunt 1: not straight tubes)."""
    sp = sp or LINK
    j = V.standing(sp)
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, (sg * (sp['shoulders'] + 8), 392.0, 60.0), 'back', 'fist')
    return j


def person(img, cam, x, floor, s, yaw=0, j=None, extra=None, lift=0.0, t=0.0):
    """Link standing on `floor` (pixels) at scale s for a 1.75 m adult; `lift` raises him (held off the ground)."""
    sp = dict(LINK, **(extra or {}))
    s2 = s * HEIGHT / (TOP * V.M_PER_UNIT)
    j = j or stand(sp)
    j['body_props'] = [body] + list(j.get('body_props', []))
    j['pre'] = [shield_front] + list(j.get('pre', []))
    ny = floor - 928 * s2 - lift                     # views.person lowers the body by j['bob'] itself
    V.person(img, cam, x, ny, s2, sp, t, yaw, j)
    return x, ny, s2


# ------------------------------------------------------------------------------------------------ the sheet
def _flat():
    cam = B.Cam(1.0, 540, 960)
    cam.P = lambda x, y: (x, y)
    cam.S = lambda v: v
    return cam


def _ref(name, h):
    im = Image.open(os.path.join(ROOT, 'references', 'remakes', name)).convert('RGBA')
    return im.resize((int(im.width * h / im.height), h))


POSES = [('standing', 0, 0.0, 'standing still'), ('shrug', 0, 0.0, 'shrug ("I think so?")'),
         ('cheeks', 0, 0.0, 'hands to cheeks,\njolt back ("god!")'), ('scuttle', 0, 0.1, 'crouched scuttle,\nhands over ears'),
         ('collar', 90, 0.0, 'held by the collar,\nfeet off the ground')]
FACES = ['unsure', 'sceptical', 'aghast', 'wince', 'horror', 'deadpan', 'terrified']


def _head_tile(mood, w, h, view=0, t=0.0):
    """A close-up of the head: Link drawn big, the head centred in the tile."""
    tile = Image.new('RGBA', (w, h), (244, 240, 232, 255))
    s = h / 470.0                                          # adult scale for which his head fills the tile
    s2 = s * HEIGHT / (TOP * V.M_PER_UNIT)
    hy_units = -150 + LINK['head_dy'] - 30                  # aim at the middle of head and cap
    floor = h / 2 - hy_units * s2 + 928 * s2
    person(tile, _flat(), w / 2, floor, s, view, None, dict(mood=mood), t=t)
    return tile


def sheet(out):
    B.SS = 1
    W, H = 1080, 1900
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    big, small = ImageFont.truetype(FONT, 28), ImageFont.truetype(FONT, 17)
    cam = _flat()
    d.text((20, 12), 'TRIAL: Young Link (remake), front / side / back, 1.33 m', font=big, fill=(30, 30, 30))
    floor, s = 640, 0.46
    for i, (yaw, lab) in enumerate(((0, 'front'), (90, 'side'), (180, 'back'))):
        x = 90 + i * 165
        person(img, cam, x, floor, s, yaw)
        d.text((x, floor + 8), lab, font=small, fill=(60, 60, 60), anchor='mt')
    d.line([(20, floor), (640, floor)], fill=(150, 146, 140), width=2)
    import sizes
    sizes.scale_ref(d, 600, floor, s / V.M_PER_UNIT)
    r3, r4 = _ref('03-link.jpg', 290), _ref('04-link.jpg', 290)
    img.alpha_composite(r3.resize((290 * r3.width // r3.height, 290)), (W - 400, 60))
    r4 = r4.resize((400, int(400 * r4.height / r4.width)))
    img.alpha_composite(r4, (W - 410, 384))
    d.text((W - 400, 44), 'ref 03', font=small, fill=(30, 30, 30))
    d.text((W - 400, 362), 'ref 04 (MAIN)', font=small, fill=(30, 30, 30))
    y0 = 700
    d.text((20, y0), 'Poses', font=big, fill=(30, 30, 30))
    for i, (name, yaw, t, lab) in enumerate(POSES):
        tile = Image.new('RGBA', (206, 520), (244, 240, 232, 255))
        lift = 60 if name == 'collar' else 0
        person(tile, cam, 103, 490, 0.4, yaw, pose(name, t), dict(mood={'shrug': 'unsure', 'cheeks': 'aghast',
               'scuttle': 'wince', 'collar': 'terrified'}.get(name, 'neutral')), lift=lift, t=t)
        ImageDraw.Draw(tile).line([(10, 490), (196, 490)], fill=(150, 146, 140), width=2)
        img.alpha_composite(tile, (14 + i * 213, y0 + 40))
        d.multiline_text((18 + i * 213, y0 + 566), lab, font=small, fill=(30, 30, 30))
    y1 = y0 + 620
    d.text((20, y1), 'Faces', font=big, fill=(30, 30, 30))
    for i, mood in enumerate(FACES):
        tile = _head_tile(mood, 148, 190)
        img.alpha_composite(tile, (14 + i * 152, y1 + 40))
        d.text((88 + i * 152, y1 + 236), mood, font=small, fill=(30, 30, 30), anchor='mt')
    d.text((20, y1 + 270), 'terrified, side on (S12)', font=small, fill=(30, 30, 30))
    img.alpha_composite(_head_tile('terrified', 148, 190, 90), (14, y1 + 292))
    img.alpha_composite(_head_tile('neutral', 148, 190, 180), (166, y1 + 292))
    d.text((170, y1 + 486), 'cap from behind (S1)', font=small, fill=(30, 30, 30))
    img.alpha_composite(_ref('01-kg.jpg', 190), (380, y1 + 292))
    d.text((384, y1 + 486), 'ref 01', font=small, fill=(30, 30, 30))
    img.convert('RGB').save(out, quality=90)
    return out


def faces(out):
    B.SS = 1
    tiles = [_head_tile(m, 360, 440) for m in FACES] + [_head_tile('terrified', 360, 440, 90),
                                                        _head_tile('neutral', 360, 440, 180)]
    W = 360 * 3
    img = Image.new('RGBA', (W, 440 * 3), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, 24)
    for i, (t, lab) in enumerate(zip(tiles, FACES + ['terrified, side on', 'cap from behind'])):
        img.alpha_composite(t, ((i % 3) * 360, (i // 3) * 440))
        d.text(((i % 3) * 360 + 14, (i // 3) * 440 + 10), f'{i + 1} {lab}', font=f, fill=(30, 30, 30))
    img.convert('RGB').save(out, quality=90)
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    elif sys.argv[1] == 'faces':
        print(faces(sys.argv[2]))
