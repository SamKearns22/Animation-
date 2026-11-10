#!/usr/bin/env python3
"""Remakes (the Ocarina of Time remake satire, Sam 10 Nov): the creatures, drawn fresh in our flat look from Sam's
references (references/remakes/01, 02, 05, 06, 11, 12), never traced. The children and the gunman are in
remakes_cast.py.

MAP (rule 61)
  units ................ person units (V.M_PER_UNIT metres each); s is the scale for a 1.75 m adult, as remakes_cast
  colours .............. top of file
  ribbons .............. _ribbon (a tapering band along a curve), _notched (a feathery edge)
  Kaepora Gaebora ...... KG_MOODS; _kg_wing (a wing used as an arm: shoulder, elbow, hand; the primaries are its
                         fingers, rule 41); WING_POSES; _kg_front, _kg_side (head, crests, body, bib, legs, tail, beak,
                         brows); bandana; kg() places him and returns where his wing hands are
  Navi ................. navi(): the glowing ball (style exception, Decision 4), four dragonfly wings, heat 0-1 blue to red
  the Goron ............ goron(): one egg of a body, stubby limbs, rocky back, frilly pink dress, vacant face, drool
  sheets ............... alone(WHO, OUT) one creature beside its references, its poses and faces

    python3 source/remakes_creatures.py alone kg|navi|goron OUT.jpg
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import views as V                # noqa: E402
from ed import INK, curve, open_curve, oval   # noqa: E402

REF = os.path.join(os.path.dirname(HERE), 'references', 'remakes')
SHINE = (255, 255, 255)


def dk(c, k=0.7):
    return B.dk(c, k)


def mix(a, b, u):
    return tuple(int(round(x + (y - x) * u)) for x, y in zip(a, b))


# ------------------------------------------------------------------------------------------------ colours
KG_BROWN, KG_BROWN_D = (118, 72, 44), (84, 50, 30)          # back, head, wings
KG_RUST = (156, 78, 42)                                     # the chest
KG_OCHRE, KG_OCHRE_L = (206, 150, 64), (226, 182, 96)       # the belly
KG_CREST, KG_CREST_D = (198, 152, 82), (150, 108, 54)       # the horn crests, the legs
KG_FACE, KG_FACE_RIM = (242, 238, 226), (196, 160, 112)     # the face disc
KG_IRIS = (116, 146, 172)
KG_BROW = (58, 40, 30)
KG_BEAK = (226, 176, 62)
KG_FOOT, KG_TALON = (234, 196, 74), (52, 42, 34)
KG_TAIL, KG_TAIL_TIP = (112, 90, 72), (190, 176, 156)
KG_WING_EDGE = (168, 128, 92)
MOUTH_IN, TONGUE = (110, 34, 40), (214, 104, 110)
BANDANA, BANDANA_D = (192, 38, 40), (140, 24, 28)

GORON, GORON_D, GORON_L = (246, 190, 64), (214, 150, 40), (252, 214, 110)
ROCK, ROCK_D = (150, 140, 128), (110, 102, 94)
DRESS, DRESS_D, DRESS_L = (244, 160, 196), (214, 120, 162), (252, 206, 226)
G_EYE = (70, 34, 96)


# ------------------------------------------------------------------------------------------------ ribbons
def _ribbon(centre, w0, w1, notch=0.0, seed=1):
    """A band of width w0 tapering to w1 along the points of `centre`; notch > 0 roughens both edges (feathers)."""
    c = np.asarray(centre, float)
    n = len(c)
    left, right = [], []
    for i in range(n):
        a, b = c[max(0, i - 1)], c[min(n - 1, i + 1)]
        d = b - a
        L = math.hypot(*d) or 1.0
        nx, ny = -d[1] / L, d[0] / L
        u = i / (n - 1)
        w = (w0 + (w1 - w0) * u) / 2
        jl = jr = 1.0
        if notch:
            jl = 1.0 + notch * (((i * 7 + seed) % 3) - 1) * 0.5
            jr = 1.0 + notch * (((i * 5 + seed * 3) % 3) - 1) * 0.5
        left.append((c[i][0] + nx * w * jl, c[i][1] + ny * w * jl))
        right.append((c[i][0] - nx * w * jr, c[i][1] - ny * w * jr))
    return left + right[::-1]


def _feather(base, ang, length, width):
    """One long feather: a pointed leaf from `base` along angle `ang`."""
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux
    bx, by = base
    return curve([(bx + nx * width * 0.4, by + ny * width * 0.4), (bx + ux * length * 0.5 + nx * width * 0.5,
                   by + uy * length * 0.5 + ny * width * 0.5), (bx + ux * length, by + uy * length),
                  (bx + ux * length * 0.5 - nx * width * 0.5, by + uy * length * 0.5 - ny * width * 0.5),
                  (bx - nx * width * 0.4, by - ny * width * 0.4)], 3)


# ================================================================================================ Kaepora Gaebora
# Faces: brows (tilt: + is the inner end down, an angry V; lift: both up), eyes, beak (Q3: a big hype grin)
KG_MOODS = {
    'kindly': dict(eyes='smile', brows=(-0.25, 10), beak='smile'),        # line 3: eyes closed in a smile
    'hype': dict(eyes='open', pupil=1.2, shine2=True, brows=(-0.4, 24), beak='grin'),   # line 1: the big hype grin,
                                                                          # eyes wide and sparkling
    'glee': dict(eyes='open', pupil=0.32, low=0.42, brows=(0.6, 0), beak='grin'),   # the execution: hostile glee, a
                                                                          # crazed squint from below, pinprick pupils
    'war': dict(eyes='narrow', brows=(0.7, -4), beak='roar'),             # the camp: war face
    'show': dict(eyes='smile', brows=(-0.5, 26), beak='grin'),            # line 11: the game-show grin, eyes
                                                                          # squeezed shut in it (pass 2: faces alike)
    'fury': dict(eyes='narrow', pupil=0.5, brows=(0.85, -8), beak='roar', spit=True),   # line 13: hissing, spitting
}

# Each wing as an arm (rule 41): (elbow, hand, hand shape) in his own units, for his left (screen right, front view)
# wing; the right wing mirrors it. Shapes: 'fold' (feathers together), 'spread' (fingers fanned), 'grip' (curled
# round something), 'point' (one long feather out, the rest tucked).
WING_POSES = {
    'fold': ((192, -30), (172, 90), 'fold'),           # hugging his sides, the tips no lower than his belly
    'wide': ((300, -150), (470, -260), 'spread'),          # line 1: flung wide
    'teach': ((250, -170), (290, -380), 'point'),          # line 3: one wing raised like a teacher
    'gesture': ((300, -40), (500, -60), 'spread'),         # line 11: the sweep along the line-up
    'gun': ((210, -10), (90, 20), 'grip'),                 # the MG42 furled in his wings, up at his chest (pass 3:
                                                           # held low it sat on his talons)
    'grab': ((230, -40), (110, -120), 'grip'),             # the lapels (front)
    'up': ((300, -260), (520, -420), 'spread'),            # a flap, up
    'down': ((300, 40), (480, 200), 'spread'),             # a flap, down
}


def _curl(base, ang, ln, bend, w0, w1):
    """A finger feather bent like a hooked finger: out along `ang`, then curling by `bend` radians."""
    pts, x, y, a = [base], base[0], base[1], ang
    for k in range(4):
        x, y = x + math.cos(a) * ln / 4, y + math.sin(a) * ln / 4
        pts.append((x, y))
        a += bend / 3
    return _ribbon(open_curve(pts, 4), w0, w1)


def _kg_wing(p, sh, el, hd, shape, side, colour=KG_BROWN, taper=False):
    """A wing used as an arm (rule 41): a broad feathered limb shoulder to elbow to wrist, a row of secondary
    feathers hanging off its trailing edge (so it reads as a wing, not a stick), the pale leading edge, and the
    primaries at the end as its fingers: 'fold' together, 'spread' fanned, 'grip' bent round what it holds like
    hooked fingers, 'point' one long feather out. side +1 or -1 picks which way the feathers lie."""
    path = open_curve([sh, el, hd], 8)
    n = len(path)
    dx, dy = hd[0] - el[0], hd[1] - el[1]
    ang = math.atan2(dy, dx)
    fold = shape == 'fold'
    sec = []                                                            # the secondaries along the trailing edge
    for i in range(1, n - 1):
        a, b = path[i - 1], path[min(n - 1, i + 1)]
        L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
        nx, ny = -(b[1] - a[1]) / L, (b[0] - a[0]) / L
        if ny + side * nx * 0.6 < 0:                                    # the trailing side: down, or outward
            nx, ny = -nx, -ny
        u = i / (n - 1)
        if fold:                                                        # folded: they lie back along the body
            fa = math.atan2(b[1] - a[1], b[0] - a[0]) + side * 0.2
            sec.append((path[i], fa, 60 + 40 * u, 60))
        else:                                                           # they hang: the normal, pulled toward the ground
            gx, gy = nx * 0.55, ny * 0.55 + 0.45
            fa = math.atan2(gy, gx)
            sec.append((path[i], fa, 70 + 60 * (1 - abs(u - 0.6)) * max(0.3, gy), 72))
    for base, fa, ln, wd in sec:
        p.poly(_feather(base, fa, ln, wd), dk(colour, 0.82), INK, 2.0)
    if taper:                                       # side on (pass 2: an even tube with a pale stripe read as a coat
        p.poly(_ribbon(path, 170, 46, notch=0.2, seed=3), colour, INK, 2.8)    # sleeve): broad at the shoulder,
        for k in range(5):                          # narrowing to the wrist, rows of scalloped coverts, no stripe
            u = 0.12 + k * 0.16
            i0 = int(u * (n - 1))
            q, q2 = path[i0], path[min(n - 1, i0 + 2)]
            L = math.hypot(q2[0] - q[0], q2[1] - q[1]) or 1.0
            tx, ty = (q2[0] - q[0]) / L, (q2[1] - q[1]) / L
            hw = 70 * (1 - u * 0.7)
            for v in (-0.5, 0.0, 0.5):
                c = (q[0] - ty * hw * v, q[1] + tx * hw * v)
                p.line(open_curve([(c[0] - ty * 16 - tx * 4, c[1] + tx * 16 - ty * 4), (c[0] + tx * 12, c[1] + ty * 12),
                                   (c[0] + ty * 16 - tx * 4, c[1] - tx * 16 - ty * 4)], 4), dk(colour, 0.68), 1.8)
    else:
        p.poly(_ribbon(path, 120, 70, notch=0.12, seed=3), colour, INK, 2.8)
        p.line(open_curve([(sh[0] + side * 8, sh[1] + 30), (el[0], el[1] + 18), (hd[0], hd[1] + 14)], 6),
               KG_WING_EDGE, 4.0)                                       # the pale leading edge
        for k in range(3):                                              # the covert rows: a few strokes only
            u = 0.3 + k * 0.2
            q = path[int(u * (n - 1))]
            p.line(open_curve([(q[0] - 26, q[1] - 10), (q[0], q[1] + 8), (q[0] + 26, q[1] - 10)], 4), dk(colour, 0.7), 1.6)
    if shape == 'grip':                                                 # hooked fingers, bent round the thing held
        for k in range(4):
            u = k / 3 - 0.5
            p.poly(_curl(hd, ang + u * 0.7 * side - side * 0.2, 130 - 20 * abs(u), side * 2.0, 34, 14),
                   dk(colour, 0.88 + 0.05 * (k % 2)), INK, 2.2)
        p.ell(hd[0], hd[1], 40, 36, colour, INK, 2.4)                   # the wrist, a knuckle of feathers
        return
    n_f, spread, length = {'fold': (5, 0.18, 120), 'spread': (5, 1.0, 180), 'point': (4, 0.35, 120)}[shape]
    for k in range(n_f):
        u = (k / (n_f - 1) - 0.5)
        a = ang + u * spread * side
        ln = length * (1.0 - 0.15 * abs(u))
        if shape == 'point' and k == 0:
            a, ln = ang - 0.05 * side, 220
        f = _feather(hd, a, ln, 40)
        p.poly(f, dk(colour, 0.86 + 0.04 * (k % 2)), INK, 2.2)
        p.line([hd, (hd[0] + math.cos(a) * ln * 0.8, hd[1] + math.sin(a) * ln * 0.8)], dk(colour, 0.66), 1.4)
    p.ell(hd[0], hd[1], 36, 32, colour, None)                           # the wrist covers the feather roots


def _kg_eye(p, ex, ey, r, mood, sgn, look=0.0):
    """A big round owl eye: a white ring, the blue-grey iris, a dark pupil, one shine."""
    eyes = mood['eyes']
    p.ell(ex, ey, r * 1.28, r * 1.28, KG_FACE, KG_FACE_RIM, 2.0)
    if eyes == 'smile':                                                 # closed in a smile: a thick arch
        p.line([(ex + r * math.cos(a), ey + r * 0.3 - r * 0.7 * math.sin(a)) for a in np.linspace(0.15, math.pi - 0.15, 14)],
               INK, 6.0)
        return
    top = -0.42 if eyes == 'narrow' else -1.0
    pts = oval(ex, ey, r, r, 40)
    lid = ey + r * top
    pts = [(x, max(y, lid)) for x, y in pts]
    p.poly(pts, KG_IRIS, None)
    pr = r * 0.5 * mood.get('pupil', 1.0)
    cx = ex + look * r * 0.3
    p.poly([(x, max(y, lid)) for x, y in oval(cx, ey + 2, pr, pr, 28)], INK, None)
    if eyes != 'narrow':
        p.ell(cx - r * 0.3, ey - r * 0.32, r * 0.16, r * 0.16, SHINE, None)
        if mood.get('shine2'):
            p.ell(cx + r * 0.28, ey + r * 0.26, r * 0.09, r * 0.09, SHINE, None)
    p.poly(pts, None, INK, 3.0)
    if mood.get('low'):                                                 # the lower lid pushed up: a squint
        lo = ey + r * (1.0 - 2 * mood['low'])
        p.poly([(x, max(y, lo)) for x, y in oval(ex, ey, r * 1.02, r * 1.02, 40)], KG_FACE, None)
        p.line(open_curve([(ex - r * 1.02, lo + r * 0.2), (ex, lo - r * 0.06), (ex + r * 1.02, lo + r * 0.2)], 4), INK, 4.0)
    if eyes == 'narrow':
        p.line([(ex - r * 1.05, lid), (ex + r * 1.05, lid)], INK, 5.0)


def _kg_brow(p, ex, ey, r, sgn, tilt, lift):
    """A heavy dark brow wedge over the eye; tilt > 0 drops the inner end (an angry V), < 0 lifts it (kindly)."""
    inner = (ex - sgn * r * 1.3, ey - r * 1.35 + tilt * r * 0.9 - lift)
    outer = (ex + sgn * r * 1.35, ey - r * 1.55 - tilt * r * 0.5 - lift)
    mid = ((inner[0] + outer[0]) / 2, min(inner[1], outer[1]) - r * 0.22)
    path = open_curve([inner, mid, outer], 8)
    p.poly(_ribbon(path, r * 0.5, r * 0.22), KG_BROW, INK, 2.0)


def _kg_beak(p, bx, by, w, kind, spit=False, side=False):
    """The small gold hooked beak; 'grin' opens it wide into a smile, 'roar' wide and square, 'smile' a closed curl."""
    if kind in ('grin', 'roar'):                                       # Q3: a BIG grin, corners high, wide open
        drop = w * (2.3 if kind == 'roar' else 2.0)
        if kind == 'grin':
            mouth = curve([(bx - w * 3.1, by - w * 0.5), (bx - w * 1.4, by + w * 0.4), (bx, by + w * 0.6),
                           (bx + w * 1.4, by + w * 0.4), (bx + w * 3.1, by - w * 0.5), (bx + w * 2.0, by + drop * 0.8),
                           (bx, by + drop + w * 0.3), (bx - w * 2.0, by + drop * 0.8)], 4)
        else:
            mouth = curve([(bx - w * 2.2, by + w * 0.1), (bx, by + w * 0.5), (bx + w * 2.2, by + w * 0.1),
                           (bx + w * 1.7, by + drop), (bx, by + drop + w * 0.4), (bx - w * 1.7, by + drop)], 4)
        p.poly(mouth, MOUTH_IN, INK, 2.8)
        p.ell(bx, by + drop * 0.8, w * 1.2, w * 0.45, TONGUE, None)
        p.poly(curve([(bx - w * 1.1, by + drop - 6), (bx, by + drop + w * 0.45), (bx + w * 1.1, by + drop - 6),
                      (bx, by + drop + w * 0.1)], 3), KG_BEAK, INK, 2.2)   # the lower beak, dropped
        p.poly(mouth, None, INK, 2.8)
        if kind == 'grin':                                              # the cheeks pushed up at the corners
            for sgn in (-1, 1):
                p.line(open_curve([(bx + sgn * w * 3.0, by - w * 0.1), (bx + sgn * w * 3.5, by - w * 0.7),
                                   (bx + sgn * w * 3.4, by - w * 1.3)], 4), KG_FACE_RIM, 2.4)
        if spit:                                                        # flecks of spit flying off (no hiss sound)
            for k, (dx, dy, r) in enumerate(((-2.4, 0.6, 5), (2.6, 0.2, 6), (-3.2, -0.2, 4), (3.4, 1.0, 4), (0.4, 2.6, 5))):
                p.ell(bx + w * dx * 1.2, by + w * dy, r * 2.2, r * 2.8, (236, 244, 250), INK, 1.6)
    up = curve([(bx - w * 0.6, by - w * 1.0), (bx + w * 0.6, by - w * 1.0), (bx + w * 0.5, by + w * 0.2),
                (bx, by + w * 0.9), (bx - w * 0.5, by + w * 0.2)], 4)
    p.poly(up, KG_BEAK, INK, 2.4)                                       # the upper beak, hooking down
    p.line([(bx - w * 0.2, by - w * 0.6), (bx - w * 0.1, by + w * 0.2)], dk(KG_BEAK, 0.75), 1.6)
    if kind == 'smile':
        for sgn in (-1, 1):
            p.line(open_curve([(bx + sgn * w * 0.5, by + w * 0.2), (bx + sgn * w * 1.1, by + w * 0.3),
                               (bx + sgn * w * 1.4, by - w * 0.1)], 4), INK, 2.6)


def _crest_plume(p, root, pts, w0=72, seed=1, out=1):
    """One of the two big swept horn crests (refs 01, 02): a NARROW plume of gold-tan feathers arching up and out from
    the head and drooping at the end, like a curled moustache (pass 2: the broad fans read as wheat sheaves or
    antlers). A tapering core with a ragged feathery edge, short feather tips off its outer side, a dark shaft."""
    path = open_curve([root] + pts, 8)
    n = len(path)
    tips = []
    for i in range(3, n - 2, 5):                                        # short feather tips off the outer edge
        a, b = np.asarray(path[i], float), np.asarray(path[min(n - 1, i + 2)], float)
        ang = math.atan2(*(b - a)[::-1])
        u = i / (n - 1)
        wide = w0 * (1.0 - 0.7 * u)
        tips.append((path[i], ang + out * (0.5 + 0.1 * ((i + seed) % 2)), 24 + wide * 0.7, 10 + wide * 0.22))
    for base, ang, ln, wd in tips:                                      # behind the core: a darker underlayer
        p.poly(_feather(base, ang, ln, wd), KG_CREST_D, INK, 1.8)
    p.poly(_ribbon(path, w0, 10, notch=0.3, seed=seed), KG_CREST, INK, 2.6)
    p.line(path[1:-4], KG_CREST_D, 2.2)                                 # the shaft
    for i in range(4, n - 6, 4):                                        # a few barbs across it, angled to the tip
        a, b = np.asarray(path[i], float), np.asarray(path[i + 2], float)
        ang = math.atan2(*(b - a)[::-1])
        wd = w0 * (1.0 - 0.7 * i / (n - 1)) * 0.42
        for sg in (-1, 1):
            p.line([path[i], (path[i][0] + math.cos(ang + sg * 2.2) * -wd, path[i][1] + math.sin(ang + sg * 2.2) * -wd)],
                   KG_CREST_D, 1.4)


def _crest_fan(p, root, pts, w0=150, seed=1, out=1):
    """One of the two big swept horn crests (refs 01, 02): a broad fan of long gold-tan feathers sweeping up and out
    from the head and curling over at the tip. A broad tapering core, then single feathers splaying off its outer
    (convex) side, each a pointed leaf with a dark shaft; `out` (+1 or -1) is the side they splay to."""
    path = open_curve([root] + pts, 8)
    n = len(path)
    feathers = []
    for i in range(2, n - 2, 4):                                        # feathers along the spine, splaying outward
        a, b = np.asarray(path[i], float), np.asarray(path[min(n - 1, i + 2)], float)
        ang = math.atan2(*(b - a)[::-1])
        u = i / (n - 1)
        wide = w0 * (1.0 - 0.75 * u)
        feathers.append((path[i], ang + out * (0.6 + 0.12 * ((i + seed) % 2)), 80 + wide * 1.0, 30 + wide * 0.34))
        feathers.append((path[i], ang - out * 0.35, 40 + wide * 0.5, 16 + wide * 0.2))
    for base, ang, ln, wd in feathers:                                  # behind the core
        p.poly(_feather(base, ang, ln, wd), KG_CREST_D, INK, 2.0)
    p.poly(_ribbon(path, w0, 14, notch=0.22, seed=seed), KG_CREST, INK, 2.6)
    for base, ang, ln, wd in feathers[::2]:                             # the long outer ones, over the core's edge
        f = _feather(base, ang, ln * 0.92, wd * 0.9)
        p.poly(f, mix(KG_CREST, KG_OCHRE_L, 0.25), INK, 2.0)
        p.line([base, (base[0] + math.cos(ang) * ln * 0.8, base[1] + math.sin(ang) * ln * 0.8)], KG_CREST_D, 1.6)
    p.line(path[:-3], KG_CREST_D, 2.2)                                  # the core's shaft


def _crest_layered(p, root, pts, w0=72, seed=1, out=1):
    """Option C: a plume of overlapping long feathers, each pointing along to the tip (a flame of feathers), thick at
    the root; the path is cut short so it arches out without drooping to the shoulders."""
    path = open_curve([root] + pts[:-1], 8)
    n = len(path)
    W = w0 * 1.5
    p.poly(_ribbon(path, W * 0.8, 10, notch=0.2, seed=seed), KG_CREST_D, INK, 2.2)
    for i in range(n - 3, 0, -3):                                      # from the tip back, so root feathers lie on top
        a, b = np.asarray(path[i], float), np.asarray(path[min(n - 1, i + 3)], float)
        ang = math.atan2(*(b - a)[::-1])
        u = i / (n - 1)
        wide = W * (1.0 - 0.7 * u)
        for sg, k in ((out, 0.22), (-out, 0.12)):
            f = _feather(path[i], ang + sg * k, 60 + wide * 0.9, 12 + wide * 0.3)
            p.poly(f, mix(KG_CREST, KG_OCHRE_L, 0.2 if sg == out else 0.0), INK, 1.8)
            p.line([path[i], (path[i][0] + math.cos(ang + sg * k) * (50 + wide * 0.7),
                              path[i][1] + math.sin(ang + sg * k) * (50 + wide * 0.7))], KG_CREST_D, 1.4)


CREST = 'layered'        # the look Sam picks (Claude's pick: layered, pending Sam) from the options sheet (fan: pass 1, plume: pass 2, layered)


def _crest(p, root, pts, w0=72, seed=1, out=1):
    if CREST == 'fan':
        return _crest_fan(p, root, pts, int(w0 * 150 / 72), seed, out)
    return (_crest_layered if CREST == 'layered' else _crest_plume)(p, root, pts, w0, seed, out)


def bandana(p, hx, hy, hw, t, view='front'):
    """The Rambo bandana (line 12): a red band across his brow, knotted at his right, two ties streaming and
    fluttering behind."""
    if view == 'front':
        band = [(hx - hw * 1.0, hy - 30), (hx, hy - 44), (hx + hw * 1.0, hy - 30), (hx + hw * 1.0, hy + 8), (hx, hy - 6),
                (hx - hw * 1.0, hy + 8)]
        kx, ky = hx - hw * 1.02, hy - 12
    else:                                                               # pass 3: a straight bar overhanging his face
        # read as a blindfold; now it wraps the skull, bowed like the head, ending inside the head's front edge
        top = [(hx - hw * 0.88, hy - 10), (hx - hw * 0.2, hy - 34), (hx + hw * 0.5, hy - 26), (hx + hw * 0.74, hy - 6)]
        bot = [(hx + hw * 0.8, hy + 26), (hx + hw * 0.5, hy + 12), (hx - hw * 0.2, hy + 6), (hx - hw * 0.9, hy + 30)]
        band = open_curve(top, 5) + open_curve(bot, 5)
        kx, ky = hx - hw * 0.92, hy + 10
    for k in (0, 1):                                                    # the ties, behind the knot
        ph = t * 9.0 + k * 1.7
        pts = [(kx - 40 * i, ky + (14 + k * 26) * i * 0.5 + 12 * math.sin(ph - i * 1.3) * i * 0.6) for i in range(5)]
        p.poly(_ribbon(open_curve(pts, 5), 30, 18), BANDANA if k else BANDANA_D, INK, 2.2)
    p.poly(band, BANDANA, INK, 2.4)
    p.ell(kx, ky, 22, 18, BANDANA_D, INK, 2.2)                         # the knot


def _kg_feet(p, x, y, sgn, perched):
    """Shaggy gold-feathered legs (ref 02: feathered trousers, a ragged hem) over long yellow toes: perched, three
    toes reach forward and curl down over the branch and one grips behind; dangling, they hang open. Dark hooked
    talons on each."""
    toes = []
    for k, dx in enumerate((-34, 0, 34)):
        if perched:                                                     # forward and curling down over the branch
            toes.append([(x + dx * 0.3, y - 6), (x + dx * 0.9, y + 18), (x + dx * 1.15, y + 46), (x + dx * 1.0, y + 66)])
        else:                                                           # dangling, spread open
            toes.append([(x + dx * 0.3, y - 6), (x + dx * 1.0, y + 34), (x + dx * 1.5, y + 62), (x + dx * 1.7, y + 88)])
    for toe in toes:
        p.poly(_ribbon(open_curve(toe, 5), 22, 12), KG_FOOT, INK, 2.0)
        for q in toe[1:3]:                                              # the scales: two knuckle creases
            p.line([(q[0] - 8, q[1] - 2), (q[0] + 8, q[1] + 2)], dk(KG_FOOT, 0.75), 1.4)
        (ax, ay), (tx, ty) = toe[-2], toe[-1]
        ang = math.atan2(ty - ay, tx - ax)
        p.poly(curve([(tx + math.cos(ang + 1.6) * 7, ty + math.sin(ang + 1.6) * 7),
                      (tx + math.cos(ang) * 22 + math.cos(ang + 1.6) * 4, ty + math.sin(ang) * 22 + 6),
                      (tx + math.cos(ang) * 26, ty + math.sin(ang) * 26 + 14),
                      (tx + math.cos(ang - 1.6) * 7, ty + math.sin(ang - 1.6) * 7)], 2), KG_TALON, INK, 1.6)
    # the leg: a shaggy feathered shape, wider at its foot, with a ragged notched hem over the toes
    hem = []
    for i in range(9):
        u = i / 8
        hem.append((x + 44 - 88 * u, y + (14 if i % 2 else 0) + 4))
    p.poly([(x - 30, y - 80), (x + 30, y - 80), (x + 42, y - 30)] + hem + [(x - 42, y - 30)], KG_CREST, INK, 2.4)
    for k in (-1, 0, 1):                                                # the feather strokes on it
        p.line(open_curve([(x + k * 18, y - 50), (x + k * 22, y - 20), (x + k * 26, y + 6)], 4), KG_CREST_D, 1.6)


def _kg_tail(p, root, ang0, n, step, length):
    """The long tail (refs 01, 02): broad overlapping feathers fanned from one root, grey-brown, each with dark
    bars across it and a pale rounded tip, the outer ones a little shorter, so it reads as one fanned tail."""
    order = sorted(range(n), key=lambda k: -abs(k - (n - 1) / 2))      # the outer ones first, the middle on top
    for k in order:
        off = k - (n - 1) / 2
        a = ang0 + off * step
        ln = length - abs(off) * 26
        ux, uy, nx, ny = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        bx, by = root
        w = 58
        pts = [(bx + nx * w * 0.35, by + ny * w * 0.35), (bx + ux * ln * 0.55 + nx * w * 0.55, by + uy * ln * 0.55 + ny * w * 0.55),
               (bx + ux * ln * 0.92 + nx * w * 0.42, by + uy * ln * 0.92 + ny * w * 0.42), (bx + ux * ln, by + uy * ln),
               (bx + ux * ln * 0.92 - nx * w * 0.42, by + uy * ln * 0.92 - ny * w * 0.42),
               (bx + ux * ln * 0.55 - nx * w * 0.55, by + uy * ln * 0.55 - ny * w * 0.55),
               (bx - nx * w * 0.35, by - ny * w * 0.35)]
        col = KG_TAIL if k % 2 else dk(KG_TAIL, 0.9)
        f = curve(pts, 3)
        p.poly(f, col, INK, 2.2)
        for v in (0.45, 0.62, 0.79):                                    # the dark bars across
            c = (bx + ux * ln * v, by + uy * ln * v)
            hw = w * (0.52 if v < 0.7 else 0.46)
            p.line([(c[0] + nx * hw, c[1] + ny * hw), (c[0] + ux * 10, c[1] + uy * 10), (c[0] - nx * hw, c[1] - ny * hw)],
                   dk(KG_TAIL, 0.62), 5.0)
        p.line([(bx + ux * ln * 0.3, by + uy * ln * 0.3), (bx + ux * ln * 0.95, by + uy * ln * 0.95)], dk(KG_TAIL, 0.7), 1.4)
        p.ell(bx + ux * ln * 0.95, by + uy * ln * 0.95, w * 0.26, w * 0.2, KG_TAIL_TIP, None, rot=a)
        p.poly(f, None, INK, 2.2)


def _kg_front(p, mood, wings, perched, band, t, look=0.0, tail=1.0):
    """Facing us (S1, S3, S5, S10): tail behind, the far halves of the wings, the body (rust chest, ochre belly, the
    white bib with its two gold eye-spots), feet, the head with its face disc, eyes, brows, beak, the two crests."""
    m = KG_MOODS[mood]
    _kg_tail(p, (0, 90), math.pi / 2, 9, 0.17, 430 * tail)                  # the long fanned tail hanging below
    hx, hy, hw = 0.0, -250.0, 168.0
    _crest(p, (hx - 50, hy - 110), [(-120, hy - 250), (-200, hy - 350), (-290, hy - 380), (-360, hy - 320),
                                    (-380, hy - 210), (-360, hy - 120)], seed=1, out=1)   # arching up, out, drooping
    _crest(p, (hx + 50, hy - 110), [(130, hy - 240), (210, hy - 340), (300, hy - 365), (365, hy - 295),
                                    (380, hy - 190), (395, hy - 140)], seed=2, out=-1)
    body = curve([(0, -230), (150, -190), (196, -40), (186, 110), (110, 210), (0, 236), (-110, 210), (-186, 110),
                  (-196, -40), (-150, -190)], 5)
    p.poly(body, KG_BROWN, INK, 2.8)
    p.poly(curve([(0, -170), (130, -130), (162, 0), (150, 120), (80, 196), (0, 214), (-80, 196), (-150, 120),
                  (-162, 0), (-130, -130)], 5), KG_RUST, None)          # the chest
    p.poly(curve([(0, 30), (120, 50), (136, 130), (80, 196), (0, 212), (-80, 196), (-136, 130), (-120, 50)], 5),
           KG_OCHRE, None)                                              # the belly
    for row in range(4):                                                # the chest feathers: scallop strokes only
        y = 60 + row * 36
        for k in range(-3, 4):
            x = k * 34 + (row % 2) * 17
            if abs(x) < 120 - row * 10:
                p.line(oval(x, y, 16, 10, 8, 0.2, math.pi - 0.2), KG_OCHRE_L if row else dk(KG_RUST, 0.8), 1.8)
    p.poly(body, None, INK, 2.8)
    for sd, sgn in (('R', -1), ('L', 1)):                               # the feet (perched: over the branch at y 240)
        _kg_feet(p, sgn * 64, 236, sgn, perched)
    bib = curve([(-120, -150), (0, -180), (120, -150), (110, -40), (60, 10), (0, 30), (-60, 10), (-110, -40)], 5)
    p.poly(bib, KG_FACE, INK, 2.4)                                      # the white bib, scalloped at its foot
    for k in range(-2, 3):
        p.line(oval(k * 40, -10 + abs(k) * -14, 20, 12, 8, 0.2, math.pi - 0.2), KG_FACE_RIM, 1.6)
    for x, y, r in ((-74, -40, 30), (0, -40, 30), (74, -40, 30)):        # its eye-spots (ref 01): pale rings in a row
        p.ell(x, y, r, r, KG_FACE_RIM, INK, 1.8)                         # along the bib's foot, never two filled dots
        p.ell(x, y, r * 0.62, r * 0.62, KG_FACE, None)                    # (pass 2: those read as breasts)
        p.ell(x, y, r * 0.26, r * 0.26, KG_CREST, None)
    for sd, sgn in (('R', -1), ('L', 1)):                               # the wings, as arms, over the body's sides
        el, hd, shape = wings[sd]
        _kg_wing(p, (sgn * 150, -150), el, hd, shape, sgn)
    head = curve([(hx - hw, hy + 10), (hx - hw * 0.94, hy - 80), (hx - hw * 0.56, hy - 136), (hx, hy - 146),
                  (hx + hw * 0.56, hy - 136), (hx + hw * 0.94, hy - 80), (hx + hw, hy + 10), (hx + hw * 0.8, hy + 90),
                  (hx, hy + 110), (hx - hw * 0.8, hy + 90)], 5)
    p.poly(head, KG_BROWN, INK, 2.8)
    for sgn in (-1, 1):                                                 # the face disc: two round lobes
        p.ell(hx + sgn * 66, hy + 4, 86, 92, KG_FACE, None)
    p.ell(hx, hy + 60, 84, 56, KG_FACE, None)
    for sgn in (-1, 1):
        p.line(oval(hx + sgn * 66, hy + 4, 88, 94, 30, math.pi * (0.75 if sgn < 0 else -0.25) - 0.6,
                    math.pi * (1.75 if sgn < 0 else 0.75) - 0.6 + 0.0), KG_FACE_RIM, 2.6)
    if band:
        bandana(p, hx, hy - 80, hw * 0.9, t)
    for sgn in (-1, 1):
        _kg_eye(p, hx + sgn * 64, hy + 2, 38, m, sgn, look)
        _kg_brow(p, hx + sgn * 64, hy + 2, 38, sgn, *m['brows'])
    _kg_beak(p, hx, hy + 56, 28, m['beak'], m.get('spit', False))
    return (hx, hy)


def _kg_side(p, mood, wings, perched, band, t, lean=0.0):
    """Side on facing right (S5 the swoop, S7 the burst, S12 the wall): tail back, the far wing, the body leaning
    `lean` degrees forward, the near wing in front, the head in profile with its half face disc, one eye, the beak
    forward, the crests sweeping back."""
    m = KG_MOODS[mood]
    r = math.radians(lean)
    rot = lambda x, y: (x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r))
    R = lambda pts: [rot(*q) for q in pts]
    el, hd, shape = wings['R']                                          # the far wing, darker, behind
    _kg_wing(p, rot(-10, -150), el, hd, shape, 1, dk(KG_BROWN, 0.8), taper=True)
    _kg_tail(p, rot(-140, 70), math.radians(146) + r, 5, 0.07, 480)    # the tail back and down: long, narrow,
                                                                        # pointed (ref 02; pass 2: a stub)
    if not perched:
        _kg_feet(p, *rot(30, 220), 1, False)
    body = R(curve([(-20, -230), (120, -190), (180, -40), (150, 120), (60, 220), (-80, 220), (-170, 120), (-190, -20),
                    (-140, -170)], 5))
    p.poly(body, KG_BROWN, INK, 2.8)
    p.poly(R(curve([(60, -190), (150, -90), (166, 40), (130, 160), (60, 200), (40, 60), (30, -80)], 5)), KG_RUST, None)
    p.poly(R(curve([(70, 40), (150, 70), (130, 160), (60, 200), (30, 120)], 4)), KG_OCHRE, None)
    p.poly(R(curve([(40, -170), (120, -150), (150, -60), (100, -20), (50, -60)], 4)), KG_FACE, INK, 2.2)   # the bib
    for bx, by in ((86, -40), (124, -70)):                               # the eye-spot rings, side on
        c = rot(bx, by)
        p.ell(*c, 16, 20, KG_FACE_RIM, INK, 1.6)
        p.ell(*c, 9, 12, KG_FACE, None)
    p.poly(body, None, INK, 2.8)
    if perched:
        _kg_feet(p, *rot(20, 230), 1, True)
    hx, hy, hw = (*rot(40, -250), 150.0)
    _crest(p, (hx - 70, hy - 90), [(hx - 200, hy - 170), (hx - 320, hy - 250), (hx - 400, hy - 220),
                                    (hx - 420, hy - 130)], 56, seed=2, out=1)     # the far one, lower, behind
    _crest(p, (hx - 30, hy - 110), [(hx - 120, hy - 250), (hx - 210, hy - 350), (hx - 310, hy - 380),
                                    (hx - 380, hy - 320), (hx - 400, hy - 220)], 70, seed=1, out=1)
    head = curve([(hx - hw, hy), (hx - hw * 0.8, hy - 110), (hx, hy - 146), (hx + hw * 0.7, hy - 110), (hx + hw, hy - 10),
                  (hx + hw * 0.86, hy + 80), (hx, hy + 112), (hx - hw * 0.8, hy + 84)], 5)
    p.poly(head, KG_BROWN, INK, 2.8)
    p.poly(curve([(hx + 20, hy - 100), (hx + hw * 0.84, hy - 80), (hx + hw * 1.0, hy + 10), (hx + hw * 0.8, hy + 90),
                  (hx + 30, hy + 96), (hx - 10, hy)], 4), KG_FACE, None)  # the half face disc
    p.line(open_curve([(hx + 20, hy - 100), (hx - 12, hy), (hx + 30, hy + 96)], 6), KG_FACE_RIM, 2.6)
    if band:
        bandana(p, hx, hy - 80, hw * 0.95, t, 'side')
    ex, ey = hx + 82, hy - 6
    _kg_eye(p, ex, ey, 34, m, 1, 0.6)
    _kg_brow(p, ex, ey, 34, 1, *m['brows'])
    bx, by = hx + hw * 0.98, hy + 46
    if m['beak'] in ('grin', 'roar'):                                   # open: the lower beak dropped
        drop = 64 if m['beak'] == 'roar' else 54                        # Q3: big; the grin runs back into his cheek
        p.poly(curve([(bx - 96, by - 30), (bx - 40, by - 4), (bx + 30, by + 4), (bx + 4, by + drop),
                      (bx - 50, by + drop - 6), (bx - 86, by - 8)], 3), MOUTH_IN, INK, 2.6)
        p.ell(bx - 30, by + drop - 16, 30, 12, TONGUE, None)
        p.poly(curve([(bx - 40, by + drop - 10), (bx + 6, by + drop), (bx - 24, by + drop + 12)], 2), KG_BEAK, INK, 2.0)
        if m['beak'] == 'grin':
            p.line(open_curve([(bx - 92, by - 26), (bx - 104, by - 48), (bx - 100, by - 66)], 4), KG_FACE_RIM, 2.4)
        if m.get('spit'):
            for dx, dy, rr in ((60, 0, 6), (90, 24, 5), (70, 44, 4), (110, -8, 4)):
                p.ell(bx + dx, by + dy, rr * 2.2, rr * 2.8, (236, 244, 250), INK, 1.6)
    p.poly(curve([(bx - 34, by - 40), (bx + 10, by - 34), (bx + 40, by + 6), (bx + 18, by + 14), (bx - 30, by + 8)], 3),
           KG_BEAK, INK, 2.4)                                           # the hooked upper beak
    el, hd, shape = wings['L']                                          # the near wing, in front
    _kg_wing(p, rot(10, -140), el, hd, shape, 1, taper=True)
    return (hx, hy)


SIDE_WINGS = {                                                          # side on: (far, near) wing poses
    'fold': (((-10, -10), (-70, 100), 'fold'), ((20, 0), (-40, 110), 'fold')),
    'up': (((-40, -360), (-120, -560), 'spread'), ((60, -340), (40, -560), 'spread')),
    'down': (((-60, 0), (-200, 160), 'spread'), ((40, 20), (-60, 240), 'spread')),
    'swoop': (((-200, -200), (-420, -260), 'spread'), ((-120, -180), (-360, -300), 'spread')),   # swept back
                                                         # in the dive, body tipped near level (pass 2: upright)
    'grab': (((180, -120), (300, -180), 'grip'), ((200, -80), (330, -140), 'grip')),     # the lapels (S12)
    'gun': (((150, -20), (260, -10), 'grip'), ((170, 40), (290, 60), 'grip')),           # the MG42 (S7)
    'snap': (((170, -220), (290, -200), 'grip'), ((190, -170), (320, -150), 'grip')),    # round the head (S5)
}


GUN_C, GUN_D = (40, 40, 44), (24, 24, 28)


def kg_gun(p, hands, view):
    """A belt-fed machine gun furled in his wings (S7; pass 2: the war pose had no gun), drawn in his own units
    through the two wing hands, pointing to screen right: a wooden-free black stock, the receiver with its ammo belt
    hanging, a perforated barrel jacket, a bipod folded under it, a flash hider."""
    (ax, ay), (bx, by) = sorted(hands, key=lambda q: q[0])
    y = (ay + by) / 2 - 10
    x0 = ax - 220
    x1 = bx + (330 if view == 'front' else 300)
    p.poly([(x0, y - 22), (ax - 40, y - 34), (ax - 40, y + 26), (x0 + 30, y + 70), (x0 - 6, y + 62)], GUN_C, INK, 2.6)
    p.poly([(ax - 50, y - 40), (bx + 30, y - 40), (bx + 30, y + 22), (ax - 50, y + 22)], GUN_C, INK, 2.6)   # receiver
    p.poly([(ax - 10, y - 52), (ax + 70, y - 52), (ax + 70, y - 40), (ax - 10, y - 40)], GUN_D, INK, 2.0)   # top cover
    p.poly([(bx + 30, y - 30), (x1 - 40, y - 30), (x1 - 40, y + 8), (bx + 30, y + 8)], GUN_C, INK, 2.4)    # jacket
    for k in range(int((x1 - 70 - bx) / 34)):
        p.ell(bx + 56 + k * 34, y - 11, 8, 8, GUN_D, None)                  # the cooling holes
    p.poly([(x1 - 40, y - 20), (x1 + 10, y - 20), (x1 + 10, y - 2), (x1 - 40, y - 2)], GUN_D, INK, 2.0)    # flash hider
    p.line([(x1 - 80, y + 8), (x1 - 170, y + 30)], GUN_D, 6.0)               # the bipod, folded
    p.line([(x1 - 90, y + 8), (x1 - 186, y + 22)], GUN_D, 6.0)
    belt = open_curve([(ax + 20, y + 22), (ax - 10, y + 80), (ax - 70, y + 120), (ax - 140, y + 130)], 8)  # trails to his side
    p.poly(_ribbon(belt, 34, 30), (150, 120, 60), INK, 2.0)                  # the ammo belt hanging
    for q in belt[1::2]:
        p.ell(q[0], q[1], 10, 6, (206, 170, 80), INK, 1.2)


def kg(img, cam, x, y, s, view='front', mood='kindly', wings='fold', perched=True, band=False, t=0.0, flip=1,
       lean=0.0, look=0.0, tail=1.0):
    """Kaepora Gaebora at world (x, y) (his body's middle), scale s (as for a 1.75 m adult). wings: a WING_POSES name
    (front) or SIDE_WINGS name (side), or a dict {'L': (elbow, hand, shape), 'R': ...} in his own units (front:
    the L wing on screen right). tail < 1 shortens the tail (front: lying back along the ground when he stands).
    Returns his wing hands in world coordinates, for what he holds."""
    loc = B.Local(cam, x, y, s, flip)
    p = B.Pen(img, loc)
    wings_name = wings if isinstance(wings, str) else None
    if view == 'front':
        if isinstance(wings, str):
            name_ = wings
            el, hd, sh_ = WING_POSES[wings]
            wings = {'L': (el, hd, sh_), 'R': ((-el[0], el[1]), (-hd[0], hd[1]), sh_)}
            if name_ == 'teach':                                       # ONE wing raised, like a teacher
                fe, fh, fs = WING_POSES['fold']
                wings['R'] = ((-fe[0], fe[1]), (-fh[0], fh[1]), fs)
        _kg_front(p, mood, wings, perched, band, t, look, tail)
        if wings_name == 'gun':
            _gun_over(p, wings, 'front')
        hands = {sd: loc.P(*wings[sd][1]) for sd in 'LR'}
    else:
        if isinstance(wings, str):
            far, near = SIDE_WINGS[wings]
            wings = {'R': far, 'L': near}
        _kg_side(p, mood, wings, perched, band, t, lean)
        if wings_name == 'gun':
            _gun_over(p, wings, 'side')
        hands = {sd: loc.P(*wings[sd][1]) for sd in 'LR'}
    return hands


def _gun_over(p, wings, view):
    """The gun, then the wing wrists over it (the curled feathers hold it from behind)."""
    kg_gun(p, [wings['L'][1], wings['R'][1]], view)
    for sd in 'LR':
        hx, hy = wings[sd][1]
        p.ell(hx, hy, 40, 36, KG_BROWN, INK, 2.4)
        for k in (-1, 0, 1):
            p.line(open_curve([(hx - 30, hy + k * 14 - 6), (hx, hy + k * 14 + 4), (hx + 30, hy + k * 14 - 6)], 4),
                   KG_BROWN_D, 1.8)


KG_HEIGHT_U = 1050       # crest tips to tail tip, in person units (about 1.6 m: he towers over Link, S1)


# ================================================================================================ Navi
def navi(img, cam, x, y, s, t=0.0, heat=0.0, flip=1):
    """Navi at world (x, y), scale s: a white-hot ball in a soft glow (Decision 4: a style exception, like Cortana),
    four dragonfly wings (the top pair long and upright, the lower pair small) fluttering fast. heat 0 is her calm
    pale blue; 1 is danger red (line 9, grenade mode)."""
    loc = B.Local(cam, x, y, s, flip)
    p = B.Pen(img, loc)
    glow_c = mix((150, 200, 255), (255, 60, 36), heat)
    core = mix((250, 252, 255), (255, 214, 190), heat)
    R = 40.0                                                            # pass 2: the ball read small
    X, Y = loc.P(0, 0)
    rad = abs(loc.S(R))
    lay = Image.new('RGBA', img.size, glow_c + (0,))                 # the glow: two soft pools
    d = ImageDraw.Draw(lay)
    for k, a in ((4.2, 0.35), (2.4, 0.6)):
        d.ellipse([X - rad * k, Y - rad * k, X + rad * k, Y + rad * k], fill=glow_c + (int(255 * a),))
    lay = lay.filter(ImageFilter.GaussianBlur(rad * 1.1))
    img.alpha_composite(lay)
    flap = math.sin(t * 2 * math.pi * 7.0)                              # a fast flutter (7 beats a second)
    # refs 05, 06: the top pair long and slender, upright in a V and apart; the lower pair small, rounder, out to
    # the sides and down, clear of the ball. Drawn behind the ball, their roots hidden in it.
    for sgn in (-1, 1):
        for big in (True, False):
            if big:
                ang = -math.pi / 2 + sgn * (0.8 + 0.7 * flap)         # pass 3: the down beat was still up; now
                # the top pair sweeps from upright (0.1 rad off) to out and about level (1.5 rad)
                ln, wd, root = 130, 44, (sgn * 20, -20)
            else:
                ang = math.pi / 2 - sgn * (0.7 - 0.3 * flap)           # the small pair tucks in as the top swings down
                ln, wd, root = 58, 46, (sgn * 18, 20)
            wing = _feather(root, ang, ln, wd)
            p.poly(wing, mix((236, 236, 250), glow_c, 0.15), dk(glow_c, 0.7), 1.4)
            ux, uy = math.cos(ang), math.sin(ang)
            for k in range(1, 4):                                       # the vein cells
                c = (root[0] + ux * ln * (0.3 + k * 0.17), root[1] + uy * ln * (0.3 + k * 0.17))
                p.ell(c[0], c[1], wd * 0.2, wd * 0.13, mix((226, 200, 236), (200, 236, 214), k / 3.0), None,
                      rot=ang)
            p.line([root, (root[0] + ux * ln * 0.9, root[1] + uy * ln * 0.9)], dk(glow_c, 0.8), 1.4)
            vx, vy = -uy, ux                                            # the veins: side ribs off the spine (refs 05, 06)
            for k in range(1, 6 if big else 3):
                u = k / (6.0 if big else 3.0)
                b0 = (root[0] + ux * ln * u * 0.9, root[1] + uy * ln * u * 0.9)
                w = wd * 0.42 * math.sin(math.pi * min(0.95, u + 0.1))
                for sg in (-1, 1):
                    p.line([b0, (b0[0] + (vx * sg * w + ux * w * 0.6), b0[1] + (vy * sg * w + uy * w * 0.6))],
                           mix(dk(glow_c, 0.8), (226, 160, 210), 0.4), 1.1)
    # the ball: white-hot at the middle, shading smoothly to her tint at a soft edge (no hard ring)
    rim = mix(core, glow_c, 0.55)
    lay = Image.new('RGBA', img.size, rim + (0,))                     # clear in her own colour: no dark fringe
    d = ImageDraw.Draw(lay)
    for k in range(12):
        u = k / 11
        rr = rad * (1.08 - 0.75 * u)
        d.ellipse([X - rr, Y - rr, X + rr, Y + rr], fill=mix(rim, (255, 255, 255), u ** 0.7) + (255,))
    lay = lay.filter(ImageFilter.GaussianBlur(max(1, rad * 0.12)))
    img.alpha_composite(lay)


# ================================================================================================ the Goron
GORON_HEIGHT_U = 1280    # about Link x 1.6 (ref 11)


def _ruffle(p, y0, w0, y1, w1, col, n=11, seed=0, sag=0.0):
    """One gathered ruffle tier: flaring from half-width w0 at y0 to w1 at y1, its hem a row of deep round
    scallops, a fold line down from each gather to the hem, the inside of each fold a shade darker. sag drops the
    hem's middle, so the tiers wrap round the belly instead of hanging flat."""
    hem = []
    Y = lambda xx: y1 + sag * (1 - (xx / w1) ** 2)
    for i in range(n):                                                  # the scalloped hem, one bulge per gather
        xa, xb = -w1 + 2 * w1 * i / n, -w1 + 2 * w1 * (i + 1) / n
        for a in np.linspace(math.pi, 0, 7):
            hx = (xa + xb) / 2 + (xb - xa) / 2 * math.cos(a)
            hem.append((hx, Y(hx) + (xb - xa) * 0.42 * math.sin(a)))
    pts = [(-w0, y0), (w0, y0)] + hem[::-1]
    p.poly(pts, col, INK, 2.4)
    for i in range(1, n):                                               # the folds, from the gathers to the hem
        xb = -w1 + 2 * w1 * i / n
        xt = xb * w0 / w1
        p.poly([(xt - 3, y0 + 6), (xt + 3, y0 + 6), (xb + 10, Y(xb) + 4), (xb - 10, Y(xb) + 4)], dk(col, 0.86), None)
        p.line([(xt, y0 + 6), (xb, Y(xb) + 6)], DRESS_D, 1.6)
    p.line(open_curve([(-w0, y0 + 2), (0, y0 + 10), (w0, y0 + 2)], 6), DRESS_D, 2.0)   # the gathered top seam
    p.poly(pts, None, INK, 2.4)


def goron(img, cam, x, y, s, mood='vacant', t=0.0, flip=1, drool=True):
    """The Goron at world (x, y) (between his feet), scale s (refs 11, 12): one smooth yellow-orange body, a smaller
    dome of a head flowing into a BIG round belly (a pear, not a bell), the face on the upper third, stubby thick
    arms and legs, grey rocks on his back peeking past his shoulders, a pale tuft on top; in a frilly pink dress
    with gathered ruffles (line 11: happily absent, a vacant smile, drooling)."""
    loc = B.Local(cam, x, y, s, flip)
    p = B.Pen(img, loc)
    for sgn, (cx, cy, rx, ry) in ((-1, (-330, -900, 72, 56)), (-1, (-280, -990, 60, 46)), (1, (335, -880, 76, 58)),
                                  (1, (285, -985, 58, 44)), (1, (130, -1255, 66, 44))):   # pass 2: two big ones read as ears
        rock = [(cx + rx * math.cos(a) * (0.82 + 0.18 * ((k * 3) % 2)), cy + ry * math.sin(a) * (0.86 + 0.14 * (k % 2)))
                for k, a in enumerate(np.linspace(0, 2 * math.pi, 9, endpoint=False))]   # lumpy grey boulders
        p.poly(rock, ROCK, INK, 2.6)                                    # on his back, peeking over his shoulders
        p.line([(cx - rx * 0.3, cy - ry * 0.4), (cx, cy), (cx + rx * 0.1, cy + ry * 0.5)], ROCK_D, 2.4)   # a crack
        p.poly([(cx - rx * 0.5, cy - ry * 0.6), (cx - rx * 0.1, cy - ry * 0.8), (cx - rx * 0.2, cy - ry * 0.4)],
               mix(ROCK, (255, 255, 255), 0.3), None)
    for sgn in (-1, 1):                                                 # stubby legs, flat round feet
        p.poly(curve([(sgn * 60, -280), (sgn * 210, -280), (sgn * 215, -60), (sgn * 70, -60)], 3), GORON, INK, 2.6)
        p.poly(curve([(sgn * 40, -70), (sgn * 250, -70), (sgn * 260, 0), (sgn * 30, 0)], 3), GORON_D, INK, 2.6)
        for k in range(3):                                              # three blunt toes
            p.line([(sgn * (80 + k * 60), -4), (sgn * (80 + k * 60), -30)], dk(GORON_D, 0.8), 2.0)
    # the body: a narrower dome on top, sloping shoulders, then the belly swelling out wide and round
    egg = curve([(0, -1300), (150, -1270), (230, -1170), (260, -1030), (300, -900), (390, -720), (440, -540),
                 (420, -380), (320, -270), (160, -230), (0, -222), (-160, -230), (-320, -270), (-420, -380),
                 (-440, -540), (-390, -720), (-300, -900), (-260, -1030), (-230, -1170), (-150, -1270)], 6)
    p.poly(egg, GORON, INK, 3.0)
    p.ell(-100, -1180, 60, 30, GORON_L, None, rot=-0.5)                 # a shine on the dome
    p.poly(curve([(-60, -1286), (-20, -1350), (20, -1360), (60, -1290)], 3), (226, 238, 246), INK, 2.0)   # the pale tuft
    # the dress (it follows the belly): a bodice from under the arms, then three gathered ruffle tiers over the
    # belly, each lower one wider, drawn bottom first so each tier's top tucks under the one above
    for k, (y0, w0, y1, w1, sg) in enumerate(((-470, 430, -330, 420, 70), (-620, 420, -470, 470, 60),
                                              (-770, 380, -620, 455, 50))):
        _ruffle(p, y0, w0, y1, w1, DRESS if k % 2 == 0 else DRESS_L, n=11 - k, seed=k, sag=sg)
    neck = open_curve([(-310, -900), (-220, -830), (0, -770), (220, -830), (310, -900)], 10)   # a deep round scoop
    p.poly(neck + [(360, -800), (390, -750), (0, -730), (-390, -750), (-360, -800)], DRESS, INK, 2.6)   # (Sam: a curved
    p.line([(x, y + 12) for x, y in neck], DRESS_D, 2.0)                # neckline, clear of the goatee's point)
    for q in neck[::max(1, len(neck) // 12)]:                           # the lace along it
        p.ell(q[0], q[1] + 2, 14, 10, DRESS_L, INK, 1.4)
    # (no bow at the neckline: pass 2, it and the goatee read as one frilly jabot)
    for sgn in (-1, 1):                                                 # stubby thick arms, puffed sleeves, round fists
        arm = curve([(sgn * 310, -910), (sgn * 450, -820), (sgn * 520, -660), (sgn * 450, -620), (sgn * 380, -760)], 3)
        p.poly(arm, GORON, INK, 3.0)                                     # out from his side, a gap under it
        p.line(open_curve([(sgn * 360, -860), (sgn * 430, -760), (sgn * 470, -660)], 4), GORON_D, 3.0)   # its shade
        p.ell(sgn * 500, -620, 64, 58, GORON_D, INK, 2.8)
        p.line([(sgn * 476, -652), (sgn * 520, -632)], dk(GORON_D, 0.8), 1.8)
        p.ell(sgn * 300, -880, 96, 70, DRESS_L, INK, 2.4)
        for k in (-1, 0, 1):                                            # the sleeve's puff folds
            p.line(open_curve([(sgn * 300 + k * 40, -940), (sgn * 296 + k * 46, -880), (sgn * 300 + k * 40, -820)], 4),
                   DRESS_D, 1.4)
    # the face, on the upper third (ref 12): round dark purple eyes wide apart, small black brows, a little nose,
    # the wide vacant smile, the white goatee point
    vac = mood == 'vacant'
    for sgn in (-1, 1):
        ex, ey = sgn * 120, -1080
        p.ell(ex, ey, 40, 46, G_EYE, INK, 2.6)
        px = ex + (10 if vac else 0)
        p.ell(px - 10, ey + (6 if vac else -16), 11, 11, SHINE, None)
        if vac:                                                         # heavy half-shut lids: absent, not happy (pass 2)
            lid = [(ex + 43 * math.cos(a), ey + 49 * math.sin(a)) for a in np.linspace(math.pi * 1.06, math.pi * 1.94, 14)]
            p.poly(lid, GORON, INK, 2.6)
        if vac:                                                         # raised, flat, blank brows (an arch read sly)
            p.line([(ex - 30, ey - 100), (ex + 30, ey - 102)], INK, 6.0)
        else:
            p.line(open_curve([(ex - 34, ey - 72), (ex, ey - 82), (ex + 34, ey - 72)], 4), INK, 6.0)
    p.ell(0, -1010, 18, 13, GORON_D, None)                             # the nose
    p.ell(-8, -1004, 4, 3, dk(GORON_D, 0.7), None)
    p.ell(8, -1004, 4, 3, dk(GORON_D, 0.7), None)
    sm = [(-190, -990), (-110, -952), (0, -940), (110, -952), (190, -990)]
    if vac:                                                             # slack: a softer smile, the jaw just hanging open
        sm = [(-170, -972), (-100, -954), (0, -948), (100, -954), (170, -972)]
        p.poly(curve([(-46, -950), (46, -950), (26, -922), (-26, -922)], 3), (120, 50, 60), INK, 2.4)
    p.line(open_curve(sm, 6), INK, 4.6)                                 # the wide smile line
    for sgn in (-1, 1):
        p.line([(sgn * (166 if vac else 186), -978 if vac else -996), (sgn * (180 if vac else 200), -962 if vac else -980)],
               INK, 3.0)                                                # its dimpled corners
    beard = (226, 236, 244)                                             # the goatee: a pale tuft of strands on his chin
    p.poly([(-30, -916), (30, -916), (6, -868), (0, -852), (-6, -868)], beard, INK, 2.0)   # one small point, high
    for k in (-12, 0, 12):                                              # on the chin, hair strands down it
        p.line([(k, -912), (k * 0.3, -866)], (170, 188, 204), 1.6)      # (pass 2: the frilly one read as a jabot)
    if drool:                                                           # a fat string from the corner, swelling and stretching
        u = (t * 0.6) % 1.0
        ln = 60 + 120 * u
        dx0, dy0 = 150, -968
        wet = (176, 218, 246)
        drop = [(dx0 - 9, dy0), (dx0 + 9, dy0), (dx0 + 5, dy0 + ln * 0.8), (dx0 + 14, dy0 + ln + 6),
                (dx0, dy0 + ln + 26), (dx0 - 14, dy0 + ln + 6), (dx0 - 5, dy0 + ln * 0.8)]
        p.poly(curve(drop, 2), wet, INK, 2.0)                           # a thin string to a small drop (pass 2: the
        p.line([(dx0 - 1, dy0 + 8), (dx0 - 1, dy0 + ln * 0.8)], (240, 250, 255), 2.0)   # wide end read as a spoon)


# ================================================================================================ the sheets
REFS = {'kg': ['01-kg.jpg', '02-kg.jpg'], 'navi': ['05-navi.jpg', '06-navi.jpg'], 'goron': ['11-goron.jpg', '12-goron.jpg']}
NAMES = {'kg': 'Kaepora Gaebora', 'navi': 'Navi', 'goron': 'The Goron'}


def _font(n):
    from PIL import ImageFont
    return ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)


def _crop(lay, bg=(236, 232, 224), m=30):
    a = np.abs(np.asarray(lay.convert('RGB')).astype(int) - np.array(bg)).sum(2) > 12
    ys, xs = np.where(a)
    return lay.crop((max(0, xs.min() - m), max(0, ys.min() - m), min(lay.width, xs.max() + m), min(lay.height, ys.max() + m)))


def tile(fn, w=1400, h=1700, bg=(236, 232, 224), at=None, **kw):
    """One drawing on a full 1080 x 1920 frame (the camera's own size), the world point `at` in its middle, cropped."""
    lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), bg + (255,))
    cam = B.Cam(1.0, *(at or (w / 2, h / 2)))
    fn(lay, cam, **kw)
    return _crop(lay, bg)


def tiles(who):
    """Every pose and view the shots use (rule 38), named."""
    out = []
    if who == 'kg':
        k = dict(s=0.9)
        for name, kw in (('perched, folded (S1 settle)', dict(mood='kindly')),
                         ('wings flung wide, hype (line 1)', dict(mood='hype', wings='wide')),
                         ('teacher wing, kindly (line 3)', dict(mood='kindly', wings='teach')),
                         ('gesture at the line-up (line 11)', dict(mood='show', wings='gesture', perched=False)),
                         ('bandana, gun grip, war (S7)', dict(mood='war', wings='gun', band=True, perched=False))):
            out.append((name, tile(lambda img, cam, **a: kg(img, cam, 700, 950, **a), at=(700, 800), **k, **kw)))
        for name, kw in (('side: swoop (S5)', dict(mood='glee', wings='swoop', perched=False, lean=58)),
                         ('side: neck snap grip (S5)', dict(mood='glee', wings='snap', perched=False)),
                         ('side: lapel grab, fury (S12)', dict(mood='fury', wings='grab', perched=False, band=True)),
                         ('side: flap up', dict(mood='hype', wings='up', perched=False)),
                         ('side: flap down', dict(mood='hype', wings='down', perched=False))):
            out.append((name, tile(lambda img, cam, **a: kg(img, cam, 700, 950, view='side', **a), at=(700, 800), **k, **kw)))
    elif who == 'navi':
        for name, kw in (('calm, wings up', dict(heat=0.0, t=0.107)), ('calm, wings down', dict(heat=0.0, t=0.036)),
                         ('reddening', dict(heat=0.5, t=0.1)), ('grenade red', dict(heat=1.0, t=0.112))):
            out.append((name, tile(lambda img, cam, **a: navi(img, cam, 300, 300, 2.2, **a), at=(300, 300),
                                   bg=(60, 70, 64), **kw)))
    elif who == 'goron':
        for name, kw in (('front, vacant, drooling', dict(t=1.2)),):
            out.append((name, tile(lambda img, cam, **a: goron(img, cam, 700, 1600, 0.85, **a), at=(700, 1060), **kw)))
    return out


def faces(who):
    if who != 'kg':
        return []
    out = []
    for m in ('kindly', 'hype', 'glee', 'war', 'show', 'fury'):
        lay = Image.new('RGBA', (B.W, B.H), (236, 232, 224, 255))
        kg(lay, B.Cam(1.0, 540, 960), 540, 1210, 1.0, mood=m)        # the head's middle lands at (540, 960)
        out.append((m, lay.crop((330, 740, 750, 1244)).resize((380, 456))))
    return out


def alone(who, out):
    """One creature alone beside its references (rule 89): each pose and view the shots use, its faces."""
    B.SS = 1
    ts = tiles(who)
    th = 760
    ts = [(n, t.resize((max(1, int(t.width * th / t.height)), th))) for n, t in ts]
    refs = [Image.open(os.path.join(REF, f)).convert('RGB') for f in REFS[who]]
    fs = faces(who)
    rows, row, w = [], [], 0
    for n, t in ts:                                                     # wrap the tiles into rows of 3000 px
        if w + t.width > 3000 and row:
            rows.append(row)
            row, w = [], 0
        row.append((n, t))
        w += t.width + 30
    rows.append(row)
    W = max(3060, sum(int(r.width * 600 / r.height) + 30 for r in refs) + 60)
    H = 80 + len(rows) * (th + 60) + 660 + (520 if fs else 0)
    img = Image.new('RGB', (W, H), (250, 248, 244))
    d = ImageDraw.Draw(img)
    d.text((30, 20), f'{NAMES[who]} (Remakes): drawn alone beside the references', font=_font(40), fill=(30, 30, 30))
    y = 80
    for row in rows:
        x = 30
        for n, t in row:
            img.paste(t.convert('RGB'), (x, y))
            d.text((x + t.width // 2, y + th + 24), n, font=_font(26), fill=(40, 40, 40), anchor='mm')
            x += t.width + 30
        y += th + 60
    x = 30
    for f, r in zip(REFS[who], refs):
        r = r.resize((int(r.width * 600 / r.height), 600))
        img.paste(r, (x, y))
        d.text((x + 6, y + 606), 'ref ' + f, font=_font(24), fill=(40, 40, 40))
        x += r.width + 30
    y += 660
    for i, (m, t) in enumerate(fs):
        img.paste(t.convert('RGB'), (30 + 420 * i, y))
        d.text((30 + 420 * i + 190, y + 480), m, font=_font(28), fill=(40, 40, 40), anchor='mm')
    img.save(out, quality=88)
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'alone':
        print(alone(sys.argv[2], sys.argv[3]))
