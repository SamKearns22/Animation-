#!/usr/bin/env python3
"""Poker Mon (TikTok satire): the people, the Dragonite, the cards and the chips (references/poker-mon/).

People are made up (Sam, 19 Oct: rich, classy and collected; not the Bond characters), built on the satire package
(views.person); only their bow ties, the dealer's waistcoat, the playing-card shirt and the guards' earpieces are
drawn here. The Dragonite, the Poker Mon cards (Queens with the yellow card border and HP, the blue swirl backs) and
the Poke Ball chips are new.

    python3 source/poker_mon_cast.py test OUT.jpg     everyone on one quick sheet (working picture)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import mossad                    # noqa: E402,F401  (brows, mouths, hair; patched into burnham on import)
import mouths                    # noqa: E402
import views as V                # noqa: E402
import moves                     # noqa: E402
from ed import INK, curve, open_curve, oval  # noqa: E402
from satire_style import rough, install_circle_hands   # noqa: E402

mouths.install(B)
install_circle_hands(B)

TUX = (24, 24, 30)
SHIRT = (244, 244, 240)

# ------------------------------------------------------------------------------------------------ the people
# Player one (lays the four Queens): silver-haired, tanned, groomed, a neat grey beard; smug and sure of himself.
P1 = dict(name='P1', skin=B.OLIVE, hw=70, hh=92, jaw='square', hair='side', hair_c=(196, 196, 200), beard='trim',
          beard_c=(190, 188, 186), brow_c=(150, 148, 146), brow_w=4.0, outfit='suit', jacket=TUX, shirt=SHIRT,
          trousers=TUX, shoulders=156, bow=(20, 20, 26), creases=2, mouth='line', seed=11)
# Player two (Dragonite's trainer): younger, slick dark hair, clean-shaven, perfectly still; deadpan.
P2 = dict(name='P2', skin=B.PALE, hw=66, hh=90, jaw='square', hair='slick', hair_c=(30, 26, 28), brow_c=(30, 26, 28),
          brow_w=3.2, outfit='suit', jacket=TUX, shirt=SHIRT, trousers=TUX, shoulders=150, bow=(20, 20, 26),
          mouth='line', seed=12)
# The woman in the red evening dress (the one who goes flying, as in The Salt).
LADY = dict(name='LADY', skin=B.PINK, hw=62, hh=86, jaw='soft', hair='blonde', hair_c=(232, 196, 110), lashes=True,
            outfit='dress', dress=(176, 22, 40), jacket=(176, 22, 40), trousers=(150, 18, 34), lip_c=(186, 30, 44),
            earring=True, shoulders=128, mouth='line', seed=13)   # the gown to the floor: legs in its colour
# The man in the playing-card shirt (casino-royale-4): black shirt printed with cards, open collar, longish hair.
CARDS = dict(name='CARDS', skin=B.OLIVE, hw=64, hh=92, jaw='round', hair='long', hair_c=(70, 52, 40), beard='stubble',
             brow_c=(60, 44, 34), outfit='suit', jacket=(28, 28, 32), shirt=(30, 30, 34), trousers=TUX, shoulders=146,
             card_shirt=True, mouth='line', seed=14)
# The old money: bald, white beard, round glasses.
OLD = dict(name='OLD', skin=B.PALE, hw=72, hh=88, jaw='round', hair='wisps', hair_c=(220, 220, 224), beard='full',
           beard_c=(236, 236, 234), brow_c=(220, 220, 216), glasses=True, glasses_c=(170, 140, 60), age=True,
           creases=3, outfit='suit', jacket=TUX, shirt=SHIRT, trousers=TUX, shoulders=150, bow=(110, 20, 34), seed=15)
# The dealer: white shirt, burgundy waistcoat, black bow tie, neat crop.
DEALER = dict(name='DEALER', skin=B.BROWN, hw=64, hh=86, jaw='soft', hair='crop', hair_c=(36, 28, 24),
              brow_c=(36, 28, 24), outfit='suit', jacket=SHIRT, shirt=SHIRT, trousers=TUX, shoulders=140,
              waistcoat=(110, 24, 36), bow=(20, 20, 26), seed=16)
# Two guards: black suits, black ties, earpieces.
SECURITY = (40, 40, 46)
GUARD1 = dict(name='GUARD1', skin=B.DEEP, hw=74, hh=92, jaw='square', hair='bald', outfit='suit', jacket=SECURITY,
              shirt=SHIRT, tie=(18, 18, 22), trousers=SECURITY, shoulders=172, earpiece=True, seed=17)
GUARD2 = dict(name='GUARD2', skin=B.PALE, hw=70, hh=94, jaw='square', hair='crop', hair_c=(120, 92, 60),
              outfit='suit', jacket=SECURITY, shirt=SHIRT, tie=(18, 18, 22), trousers=SECURITY, shoulders=166,
              earpiece=True, seed=18)
# Onlookers and hangers-on (Sam, 19 Oct): wives and husbands, an attractive escort.
# The escort: player one's companion, long dark waves, a black sequinned gown, red lips; her hand on his shoulder.
ESCORT = dict(name='ESCORT', skin=B.OLIVE, hw=60, hh=86, jaw='soft', hair='wavy', hair_c=(40, 28, 26), lashes=True,
              outfit='dress', dress=(26, 24, 30), jacket=(26, 24, 30), trousers=(26, 24, 30), lip_c=(196, 30, 46),
              earring=True, shoulders=124, sequins=True, mouth='line', seed=19)
# The old man's wife: silver bob, emerald gown, pearls.
WIFE = dict(name='WIFE', skin=B.PALE, hw=62, hh=86, jaw='soft', hair='bob', hair_c=(214, 214, 218), lashes=True,
            outfit='dress', dress=(26, 110, 74), jacket=(26, 110, 74), trousers=(22, 96, 64), lip_c=(176, 70, 80),
            age=True, pearls=True, shoulders=126, mouth='line', seed=20)
# The woman in red's husband: a silver fox in a midnight-blue dinner jacket.
HUSBAND = dict(name='HUSBAND', skin=B.PINK, hw=68, hh=90, jaw='square', hair='crop', hair_c=(150, 146, 144),
               brow_c=(110, 104, 100), outfit='suit', jacket=(30, 36, 70), shirt=SHIRT, trousers=(24, 28, 54),
               shoulders=152, bow=(20, 20, 26), creases=1, mouth='line', seed=21)
# A young hanger-on: white dinner jacket, champagne in hand.
BEAU = dict(name='BEAU', skin=B.BROWN, hw=64, hh=88, jaw='square', hair='crop', hair_c=(30, 24, 22),
            brow_c=(30, 24, 22), outfit='suit', jacket=(240, 236, 226), shirt=SHIRT, trousers=TUX, shoulders=148,
            bow=(20, 20, 26), mouth='line', seed=22)
PEOPLE = {'P1': P1, 'P2': P2, 'LADY': LADY, 'CARDS': CARDS, 'OLD': OLD, 'DEALER': DEALER, 'GUARD1': GUARD1,
          'GUARD2': GUARD2, 'ESCORT': ESCORT, 'WIFE': WIFE, 'HUSBAND': HUSBAND, 'BEAU': BEAU}
HEIGHTS = {'P1': 1.83, 'P2': 1.85, 'LADY': 1.70, 'CARDS': 1.80, 'OLD': 1.74, 'DEALER': 1.78, 'GUARD1': 1.93,
           'GUARD2': 1.90, 'ESCORT': 1.72, 'WIFE': 1.66, 'HUSBAND': 1.84, 'BEAU': 1.82}


def bow_tie(p, x, y, c, k=1.0):
    """A bow tie at the collar: two hand-cut wings and a knot."""
    for sg in (-1, 1):
        p.poly(curve([(x, y), (x + sg * 30 * k, y - 15 * k), (x + sg * 36 * k, y + 1), (x + sg * 30 * k, y + 16 * k)], 2),
               c, INK, 2.0)
    p.poly(curve([(x - 9 * k, y - 8 * k), (x + 9 * k, y - 8 * k), (x + 8 * k, y + 9 * k), (x - 8 * k, y + 9 * k)], 2),
           B.lt(c, 1.25) if hasattr(B, 'lt') else c, INK, 1.8)


def card_print(p, x0, y0, x1, y1, seed=0):
    """The playing-card shirt: small white cards with red and black pips scattered over black (casino-royale-4)."""
    rng = np.random.default_rng(seed)
    for gy in np.arange(y0 + 20, y1 - 10, 58):
        for gx in np.arange(x0 + 18 + (gy // 58 % 2) * 26, x1 - 14, 52):
            a = rng.uniform(-0.5, 0.5)
            w, h = 15, 21
            pts = [(gx + dx * math.cos(a) - dy * math.sin(a), gy + dx * math.sin(a) + dy * math.cos(a))
                   for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
            p.poly(pts, (240, 236, 226), INK, 1.2)
            p.ell(gx, gy, 3.2, 3.2, (196, 30, 40) if rng.random() < 0.5 else INK, None)


def dress_up(sp):
    """The film's outfit details, drawn over the satire package's suit (front view) through j['props']."""
    def draw(p, j2):
        if sp.get('card_shirt'):
            card_print(p, -40, 20, 40, 240, seed=sp.get('seed', 0))
        if sp.get('waistcoat'):
            wc = sp['waistcoat']
            p.poly(rough([(-sp['shoulders'] * 0.72, 40), (-30, 30), (0, 140), (30, 30), (sp['shoulders'] * 0.72, 40),
                          (sp['shoulders'] * 0.74, 470), (0, 500), (-sp['shoulders'] * 0.74, 470)], 3, 4), wc, INK, 2.4)
            for k in range(4):
                p.ell(0, 190 + 70 * k, 5, 5, (220, 190, 110), INK, 1.2)
        if sp.get('sequins'):                          # a scatter of sequin glints over the gown
            rng = np.random.default_rng(sp.get('seed', 0))
            for _ in range(26):
                x, y = rng.uniform(-sp['shoulders'] * 0.8, sp['shoulders'] * 0.8), rng.uniform(70, 480)
                p.ell(x, y, 3.2, 3.2, (200, 200, 214), None)
        if sp.get('pearls'):                           # a single strand of pearls at the neckline
            for a in np.linspace(0.2, math.pi - 0.2, 15):
                p.ell(44 * math.cos(a), 6 + 30 * math.sin(a), 5, 5, (246, 244, 236), INK, 1.0)
        if sp.get('bow'):
            bow_tie(p, 0, 4, sp['bow'])
        if sp.get('earpiece'):                         # the coiled wire, inked like everything else
            wire = open_curve([(sp['hw'] - 4, -150), (sp['hw'] + 12, -110), (sp['hw'] + 4, -40), (sp['hw'] - 14, 10)], 3)
            p.line(wire, INK, 4.0)
            p.line(wire, (200, 200, 206), 2.0)
    return draw


def pose_standing(sp):
    j = V.standing(sp)
    j['props'] = [dress_up(sp)]
    return j


def person(img, cam, x, y, s, sp, t=0.0, yaw=0, j=None):
    j = j or pose_standing(sp)
    if dress_up not in [getattr(f, '__wrapped__', None) for f in j.get('props', [])] and not j.get('_dressed'):
        j.setdefault('props', []).insert(0, dress_up(sp))
        j['_dressed'] = True
    return V.person(img, cam, x, y, s, dict(sp, full=True, pose='custom'), t, yaw, j)


# ------------------------------------------------------------------------------------------------ the Dragonite
# Refs dragonite-1..3 (dragonite-3, the cartoon, leads), dragonite-side-1..3, dragonite-above: pear-shaped, a small
# head on a wide round belly, short stubby legs; orange skin, a cream belly in horizontal bands, teal wing skin, white
# claws; a rounded snout, big friendly dark eyes, a gentle smile; two thin antennae curling back from the forehead, a
# small horn between; small bat wings on the shoulders; a long tail, thick at the base, tapering. Circle hands (house
# style); the claws are kept on the feet. 2.2 m tall: its units are the people's (views.M_PER_UNIT), feet at y 0.
ORANGE = (240, 160, 60)
ORANGE_D = (206, 124, 44)
CREAM = (246, 226, 176)
CREAM_D = (214, 190, 140)
TEAL = (84, 178, 172)
TEAL_D = (56, 140, 138)
CLAW = (250, 250, 246)
MOUTH = (120, 30, 40)
TONGUE = (226, 110, 120)
DRAGONITE_H = 2.2


def _rot(pts, piv, deg):
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    return [(piv[0] + (x - piv[0]) * c - (y - piv[1]) * s_, piv[1] + (x - piv[0]) * s_ + (y - piv[1]) * c)
            for x, y in pts]


def _ovl(cx, cy, rx, ry, n=36):
    return [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]


def tube(p, pts, w0, w1, col, lw=2.6):
    """A limb as one outlined shape tapering from w0 to w1 along pts (never a thick line with square ends)."""
    pts = open_curve(pts, 3) if len(pts) > 2 else pts
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        a_ = pts[max(0, i - 1)]
        b_ = pts[min(n - 1, i + 1)]
        dx, dy = b_[0] - a_[0], b_[1] - a_[1]
        d = math.hypot(dx, dy) or 1.0
        w = (w0 + (w1 - w0) * i / max(1, n - 1)) / 2
        left.append((x - dy / d * w, y + dx / d * w))
        right.append((x + dy / d * w, y - dx / d * w))
    p.poly(left + right[::-1], col, INK, lw)
    p.ell(pts[-1][0], pts[-1][1], w1 / 2, w1 / 2, col, None)


def wing(p, sx, sy, sg, k=1.0, spread=0.0):
    """One small bat wing from the shoulder blade: an orange frame along the top edge, solid teal below it, scalloped
    between the fingers (Sam, 19 Oct: orange at the top, solid blue for the rest, no gaps, no line across the middle). spread 0 (folded up behind) .. 1 (wide open)."""
    tip = (sx + sg * (230 + 170 * spread) * k, sy - (300 - 150 * spread) * k)
    elbow = (sx + sg * (110 + 60 * spread) * k, sy - (230 - 60 * spread) * k)
    f1 = (sx + sg * (230 + 150 * spread) * k, sy - (70 - 60 * spread) * k)
    f2 = (sx + sg * (110 + 70 * spread) * k, sy + (10 + 30 * spread) * k)
    skin = [(sx, sy), elbow, tip, (tip[0] - sg * 10 * k, tip[1] + 60 * k),
            ((tip[0] + f1[0]) / 2 - sg * 40 * k, (tip[1] + f1[1]) / 2 - 10 * k), f1,
            ((f1[0] + f2[0]) / 2 - sg * 40 * k, (f1[1] + f2[1]) / 2 - 20 * k), f2, (sx, sy + 30 * k)]
    p.poly(skin, TEAL, INK, 2.6)                       # solid blue below, no lines across it (Sam, 19 Oct)
    tube(p, [(sx, sy), elbow, tip], 30 * k, 12 * k, ORANGE)   # the orange frame along the top, overlapping the blue:
                                                               # no gap between them


IRIS = (34, 40, 70)


def dragonite_head(p, piv, deg, turn, mouth_open, eyes, mouth_shape='jaw'):
    """The head on its neck pivot, rotated by deg (negative: tipped back). Drawn to Sam's cute reference
    (dragonite-cute-face.jpg, 19 Oct): a round crown and a long rounded muzzle pushed toward the side it faces, tall
    oval eyes with big highlights, two small nostrils at the muzzle's tip, a small smile curling up to the cheek,
    pale cream antennae sweeping out from the brow, a small horn. turn 0 front .. 1 three-quarter to the right.
    mouth: the gentle smile ('jaw' closed) or a small round O ('o'), nothing else (Sam). Returns the mouth point."""
    R = lambda pts: _rot(pts, piv, deg)
    hx, hy = piv[0] + 25 * turn, piv[1] - 235          # the crown's centre
    sx, sy = hx + 75 * turn, hy + 105                  # the muzzle's centre: lower, toward the side it faces
    for sg in (-1, 1):                                 # antennae: from the brow, out and a little down, tips up
        k = 1.0 if sg > 0 else 1.0 - 0.3 * turn
        bx, by = hx + sg * 42 * k - 15 * turn, hy - 108
        ant = [(bx, by + 30), (bx + sg * 14 * k, by - 40), (bx + sg * 80 * k, by - 62), (bx + sg * 160 * k, by - 54),
               (bx + sg * 205 * k, by - 30)]                       # rooted inside the crown; tips droop (Sam's ref)
        tube(p, R(ant), 13, 7, CREAM, 2.0)
    p.poly(R([(hx - 18 - 10 * turn, hy - 120), (hx + 18 - 10 * turn, hy - 120), (hx - 6 * turn, hy - 172)]), ORANGE,
           INK, 2.2)                                                                    # the small horn
    p.poly(R(_ovl(hx - 8 * turn, hy, 138, 128)), ORANGE, INK, 2.8)                     # the crown
    mw, mh = 128 + 30 * turn, 92
    p.poly(R(_ovl(sx, sy, mw, mh)), ORANGE, INK, 2.8)                                  # the long rounded muzzle
    p.poly(R(_ovl((hx + sx) / 2, (hy + sy) / 2 - 8, 118, 70)), ORANGE, None)           # one shape: no seam between
    for sg in (-1, 1):                                                                 # the nostrils, at the tip
        p.line(R([(sx + sg * 26 + 40 * turn - 6, sy - 28), (sx + sg * 26 + 40 * turn + 6, sy - 31)]), INK, 3.0)
    mouth_at = (sx + 15 * turn, sy + 44)
    if mouth_shape == 'o' and mouth_open > 0.02:       # a round O, opening wide as it beams (Sam), darker lips round it
        ox, oy = mouth_at
        r_ = 18 + 34 * mouth_open
        p.poly(R(_ovl(ox, oy, r_ + 10, (r_ + 10) * 0.92)), ORANGE_D, INK, 2.4)
        p.poly(R(_ovl(ox, oy, r_, r_ * 0.92)), (92, 34, 32), INK, 2.0)
    # closed: no mouth line at all, the plain muzzle of Sam's photo (19 Oct: "there isn't [a smile] in the photo")
    eye_block(p, R, hx, hy, turn, eyes)
    return R([mouth_at])[0]


EYE_STYLES = ['narrow', 'soft', 'focus', 'aim', 'arc', 'puppy']   # for Sam's pick of the firing eyes (19 Oct)


def eye_block(p, R, hx, hy, turn, eyes):
    """The big friendly eyes. Firing styles (Sam: friendly concentration, "he's a good boy"): 'narrow' (lids cut
    straight across: determined), 'soft' (round, a level upper lid, cheeks pushed up: a smiling squint), 'focus'
    (round, a soft lowered lid and a little crease between the eyes), 'aim' (one eye soft, the other screwed up as
    if aiming), 'arc' (happy closed arcs), 'puppy' (big shining eyes, two highlights, cheeks up)."""
    for sg in (-1, 1):
        k = 1.0 if sg > 0 else 1.0 - 0.3 * turn
        ex, ey = hx + sg * 58 * k + 40 * turn, hy - 18
        style = eyes
        if eyes == 'aim':
            style = 'soft' if sg > 0 else 'squint'
        if style == 'closed':
            p.line(R([(ex - 24, ey + 2), (ex, ey + 12), (ex + 24, ey + 2)]), INK, 3.6)
        elif style == 'arc':                                       # happy, closed, curving up
            p.line(R(open_curve([(ex - 24, ey + 8), (ex, ey - 8), (ex + 24, ey + 8)], 3)), INK, 4.2)
        elif style == 'squint':                                    # screwed up, a curved slit
            p.line(R(open_curve([(ex - 24, ey + 2), (ex, ey - 4), (ex + 24, ey + 4)], 3)), INK, 4.6)
            p.line(R([(ex - 20, ey + 12), (ex + 18, ey + 14)]), ORANGE_D, 2.4)
        elif style == 'narrow':                                    # determined: the top of the eye cut by a lid
            p.poly(R([(ex - 24 * k, ey - 4 - sg * 6), (ex + 24 * k, ey - 4 + sg * 6), (ex + 22 * k, ey + 18),
                      (ex - 22 * k, ey + 18)]), INK, INK, 2.0)
            p.ell(*R([(ex + 8, ey + 4)])[0], 6, 5, (250, 250, 250), None)
        elif style in ('soft', 'focus', 'puppy'):
            r = 1.22 if style == 'puppy' else 1.0
            ew, eh = 25 * k * r, 40 * r
            p.poly(R(_ovl(ex, ey, ew, eh)), (250, 250, 250), INK, 2.2)
            p.poly(R(_ovl(ex + 4 * turn, ey + 3, ew - 4, eh - 5)), IRIS, None)
            p.ell(*R([(ex + 7 * r, ey - 14 * r)])[0], 8 * r, 12 * r, (250, 250, 250), None)
            if style == 'puppy':
                p.ell(*R([(ex - 9, ey + 12)])[0], 4.5, 4.5, (250, 250, 250), None)
            if style in ('soft', 'puppy', 'focus'):                # cheeks pushed up: the lower lid a smile
                lo = {'soft': 0.0, 'puppy': 0.45, 'focus': 0.3}[style]
                p.poly(R(curve([(ex - ew - 6, ey + eh * (0.5 + lo * 0.5)), (ex, ey + eh * lo * 0.4 - eh * 0.1 * (1 - lo)),
                                (ex + ew + 6, ey + eh * (0.5 + lo * 0.5)), (ex + ew + 6, ey + eh + 8), (ex - ew - 6, ey + eh + 8)], 3)),
                       ORANGE, None)
                p.line(R(open_curve([(ex - ew - 2, ey + eh * (0.5 + lo * 0.5)), (ex, ey + eh * lo * 0.4 - eh * 0.1 * (1 - lo)),
                                (ex + ew + 2, ey + eh * (0.5 + lo * 0.5))], 3)), INK, 2.4)
            if style == 'focus':                                   # a kind lid: lowered, sloping down to the outside
                inner = -sg                                        # the inner corner is toward the face's middle
                yi, yo = ey - eh * 0.42, ey - eh * 0.3
                pts = [(ex + inner * (ew + 6), yi), (ex - inner * (ew + 6), yo)]
                p.poly(R([pts[0], pts[1], (pts[1][0], ey - eh - 8), (pts[0][0], ey - eh - 8)]), ORANGE, None)
                p.line(R(pts), INK, 2.8)
        else:                                          # the cute eye: a tall oval, navy, two highlights
            r = 1.2 if eyes == 'wide' else 1.0
            p.poly(R(_ovl(ex, ey, 25 * k * r, 40 * r)), (250, 250, 250), INK, 2.2)
            p.poly(R(_ovl(ex + 4 * turn, ey + 3, 21 * k * r, 35 * r)), IRIS, None)
            p.ell(*R([(ex + 7, ey - 14)])[0], 8 * r, 12 * r, (250, 250, 250), None)
            p.ell(*R([(ex - 7, ey + 18)])[0], 3.5, 3.5, (200, 210, 230), None)
    if eyes == 'focus':                                            # a small crease of effort between the eyes
        p.line(R([(hx + 34 * turn - 4, hy - 74), (hx + 34 * turn - 2, hy - 58)]), ORANGE_D, 2.6)
        p.line(R([(hx + 34 * turn + 8, hy - 72), (hx + 34 * turn + 6, hy - 58)]), ORANGE_D, 2.6)


def dragonite(img, cam, x, y, s, t=0.0, turn=0.5, flip=1, head=0.0, mouth_open=0.0, eyes='open', wings=0.15,
              arms=0.0, lean=0.0, bow=True, mouth_shape='jaw'):
    """The Dragonite standing, feet at world (x, y), scale s (the people's scale), turned `turn` (0 facing us .. 1
    three-quarter) toward the right of frame (flip=-1: toward the left). head: degrees (negative thrown back);
    arms 0 at its sides .. 1 out wide (bracing); lean: degrees forward (+). Returns the mouth point (world)."""
    L = B.Local(cam, x, y, s, flip)
    p = B.Pen(img, L)
    T = lambda pts: _rot(pts, (0, -380), lean)
    tail = curve([(-80, -260), (-320, -230), (-520, -120), (-640, -10), (-720, 50), (-600, 40), (-450, -20),
                  (-280, -90), (-90, -120)], 4)                                         # the tail, behind
    p.poly(T(tail), ORANGE, INK, 2.8)
    p.line(T(open_curve([(-560, 0), (-400, -90), (-230, -150)], 3)), CREAM_D, 3)
    for sg in (-1, 1):                                                                  # both wings, behind
        k = 0.85 if sg < 0 else 1.0
        wing(p, *T([(sg * 140 * k + 30 * turn, -860)])[0], sg, k * 1.15, wings)
    for sg in (-1, 1):                                                                  # stubby legs, clawed feet
        lx = sg * 200 + 30 * turn
        p.poly(_ovl(lx, -150, 120, 150), ORANGE, INK, 2.8)
        p.poly(_ovl(lx + 30 * turn, -30, 130, 44), ORANGE, INK, 2.6)
        for c in (-1, 0, 1):
            cx = lx + 30 * turn + c * 56
            p.poly([(cx - 15, -8), (cx + 15, -8), (cx + 4 * c, 26)], CLAW, INK, 1.8)
    # body and neck are one shape with one outline, the shoulders curving up into the neck, which turns with the head
    # (Sam, 19 Oct: never a neck glued on). Its ends run up inside the head, which covers them.
    piv = T([(0, -1000)])[0]
    hr = lambda pts: _rot([(piv[0] + x_, piv[1] + y_) for x_, y_ in pts], piv, head + lean)
    nl, nr = hr([(-100 + 20 * turn, -200), (100 + 20 * turn, -200)])
    body = [nl] + T([(-125, -1030), (-200, -920), (-290, -720), (-380, -440), (-390, -260), (-300, -110), (0, -60),
                     (300, -110), (390, -260), (380, -440), (290, -720), (200, -920), (125, -1030)]) + [nr]
    edge = open_curve(body, 5)                         # fill and outline on one path (a closed curve's fill
    p.poly(edge, ORANGE, None)                         # bulged past the open outline at the neck)
    p.line(edge, INK, 3.0)
    bx = 50 * turn
    cl, cr = hr([(bx - 58, -160), (bx + 58, -160)])
    belly = [cl] + T([(bx - 88, -1000), (bx - 160, -880), (bx - 230, -680), (bx - 300, -430), (bx - 290, -250),
                      (bx - 200, -120), (bx, -90), (bx + 200, -120), (bx + 290, -250), (bx + 300, -430),
                      (bx + 230, -680), (bx + 160, -880), (bx + 88, -1000)]) + [cr]
    edge = open_curve(belly, 5)
    p.poly(edge, CREAM, None)                          # the cream runs up the throat
    p.line(edge, INK, 2.6)
    for k in range(1, 9):                                                               # the bands across the belly
        yb = -990 + k * 102
        f = (yb + 990) / 900
        w_ = 90 + 210 * math.sin(math.pi * min(1.0, f * 0.62 + 0.08)) ** 0.8
        p.line(T(open_curve([(bx - w_ * 0.96, yb - 6), (bx, yb + 14), (bx + w_ * 0.96, yb - 6)], 3)), CREAM_D, 2.6)
    for sg in (-1, 1):                                                                  # short arms, circle hands
        sh = (sg * 190 + 40 * turn, -840)
        hand = (sh[0] + sg * (90 + 200 * arms), sh[1] + 170 - 120 * arms)
        el = (sh[0] + sg * (70 + 90 * arms), sh[1] + 100 - 30 * arms)
        tube(p, T([sh, el, hand]), 84, 64, ORANGE)
        p.poly(T(_ovl(*hand, 46, 46)), ORANGE, INK, 2.6)
    if bow:
        bp = T([(40 * turn, -1000)])[0]
        bow_tie(p, bp[0], bp[1], (22, 22, 28), 2.4)
    m = dragonite_head(p, piv, head + lean, turn, mouth_open, eyes, mouth_shape)
    return L.ox + L.k * m[0] * L.flip, L.oy + L.k * m[1]


def glow(img, cam, pts_r, colour=(255, 236, 160), core=(255, 255, 250), strength=1.0):
    """The show's Hyper Beam light (Sam, 19 Oct: a real glow, this film only): bright cores with a soft halo added
    over the picture. pts_r: [(x, y, r)] world circles; a line of them makes a beam."""
    W_, H_ = img.size
    sm = 4
    lay = Image.new('L', (W_ // sm, H_ // sm), 0)
    d = ImageDraw.Draw(lay)
    for x, y, r in pts_r:
        X, Y = cam.P(x, y)
        R = cam.S(r)
        d.ellipse([(X - R) / sm, (Y - R) / sm, (X + R) / sm, (Y + R) / sm], fill=255)
    halo = lay.filter(ImageFilter.GaussianBlur(max(2, int(cam.S(90) / sm))))
    a = np.asarray(halo, np.float32) / 255.0 * strength
    big = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).resize((W_, H_), Image.BILINEAR)
    A = np.asarray(big, np.float32)[..., None] / 255.0
    base = np.asarray(img, np.float32)
    base[..., :3] = base[..., :3] + (np.array(colour, np.float32) - base[..., :3] * 0.2) * np.clip(A * 1.4, 0, 1) * 0.85
    coreL = lay.filter(ImageFilter.GaussianBlur(1)).resize((W_, H_), Image.BILINEAR)
    C = np.asarray(coreL, np.float32)[..., None] / 255.0 * min(1.0, strength * 1.5)
    base[..., :3] = base[..., :3] * (1 - C) + np.array(core, np.float32) * C
    img.paste(Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), img.mode))


# ------------------------------------------------------------------------------------------------ the cards
# Poker Mon cards (Sam, 19 Oct): the playing card's face (white, rounded corners, a thin blue frame, the index in two
# corners, the mirrored double-ended Queen in red, royal blue, mustard and black: refs queens-1..3) inside the
# trading card's yellow border, with an HP number top right; backs are the trading card's (refs card-back-1..2): deep
# blue with a lighter swirl, the Poke Ball, POKER MON in chunky yellow with a blue outline, again upside down.
# Drawn once at 500 x 700 px and laid into each shot by perspective (place_card); never the word Pokemon.
CW, CH = 500, 700
YELLOW = (250, 210, 40)
YELLOW_D = (214, 170, 20)
LOGO_BLUE = (40, 84, 170)
BACK_BLUE = (30, 70, 150)
BACK_BLUE_D = (18, 40, 100)
SWIRL = (110, 160, 220)
RED = (200, 30, 40)
ROYAL = (36, 60, 150)
MUSTARD = (226, 170, 40)
SUITS = {'S': ('\u2660', INK), 'C': ('\u2663', INK), 'H': ('\u2665', RED), 'D': ('\u2666', RED)}
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
LOGO_FONT = os.path.join(HERE, 'fonts', 'Anton-Regular.ttf')
_CARDS = {}


def _font(path, size):
    return ImageFont.truetype(path, int(size))


def _rounded(d, box, r, fill, outline=None, width=0):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)


def _suit_shape(d, cx, cy, size, suit):
    ch, col = SUITS[suit]
    f = _font(FONT, size)
    d.text((cx, cy), ch, font=f, fill=col, anchor='mm')


def _queen_half(d, cx, top, w, h, suit, flip):
    """One half of the double-ended Queen: crown, face in three-quarter, veil, patterned robe; flat bold colours."""
    def P(x, y):
        return (cx + x * w, top + (h - y * h) if flip else top + y * h)
    def el(cx_, cy_, rx, ry, fill):
        X, Y = P(cx_, cy_)
        d.ellipse([X - rx * w, Y - ry * h, X + rx * w, Y + ry * h], fill=fill)

    def poly(pts, fill):
        d.polygon([P(*q) for q in pts], fill=fill, outline=INK)
        d.line([P(*q) for q in pts] + [P(*pts[0])], fill=INK, width=3)
    trim = RED if suit in 'HD' else ROYAL
    other = ROYAL if suit in 'HD' else RED
    poly([(-0.46, 1.0), (-0.42, 0.62), (-0.2, 0.5), (0.2, 0.5), (0.42, 0.62), (0.46, 1.0)], trim)      # the robe
    poly([(-0.3, 1.0), (-0.24, 0.66), (0.0, 0.58), (0.24, 0.66), (0.3, 1.0)], MUSTARD)
    for k in range(4):                                                                               # its pattern
        y = 0.7 + k * 0.075
        d.line([P(-0.24 + 0.01 * k, y), P(0.24 - 0.01 * k, y)], fill=other, width=6)
    poly([(-0.36, 0.62), (-0.34, 0.22), (-0.16, 0.12), (0.16, 0.12), (0.34, 0.22), (0.36, 0.62)], other)   # the veil
    poly([(-0.17, 0.5), (-0.19, 0.3), (-0.1, 0.2), (0.1, 0.2), (0.17, 0.28), (0.16, 0.5)], (248, 222, 196))  # face
    el(-0.075, 0.32, 0.025, 0.012, INK)
    el(0.065, 0.32, 0.025, 0.012, INK)
    d.line([P(-0.05, 0.43), P(0.05, 0.43)], fill=RED, width=4)
    poly([(-0.2, 0.2), (-0.2, 0.06), (-0.1, 0.12), (0.0, 0.02), (0.1, 0.12), (0.2, 0.06), (0.2, 0.2)], MUSTARD)  # crown
    for x in (-0.1, 0.0, 0.1):                                                     # the crown's jewels: tiny balls
        X, Y = P(x, 0.15)
        rr = 0.024 * w
        d.ellipse([X - rr, Y - rr, X + rr, Y + rr], fill=(250, 250, 248), outline=INK, width=1)
        d.pieslice([X - rr, Y - rr, X + rr, Y + rr], 180 if not flip else 0, 360 if not flip else 180, fill=RED)
        d.line([(X - rr, Y), (X + rr, Y)], fill=INK, width=2)
    def ball(cx_, cy_, r):                                                                            # a Poke Ball
        X, Y = P(cx_, cy_)
        rr = r * w
        d.ellipse([X - rr, Y - rr, X + rr, Y + rr], fill=(250, 250, 248), outline=INK, width=2)
        top = (Y - rr, Y) if not flip else (Y, Y + rr)
        d.pieslice([X - rr, Y - rr, X + rr, Y + rr], 180 if not flip else 0, 360 if not flip else 180, fill=RED,
                   outline=INK, width=2)
        d.line([(X - rr, Y), (X + rr, Y)], fill=INK, width=max(2, int(rr * 0.22)))
        d.ellipse([X - rr * 0.32, Y - rr * 0.32, X + rr * 0.32, Y + rr * 0.32], fill=(250, 250, 248), outline=INK,
                  width=2)
    fx = 0.3                                                                       # she holds a Poke Ball, not a rose
    d.line([P(fx - 0.02, 0.92), P(fx, 0.68)], fill=INK, width=4)
    ball(fx, 0.6, 0.075)
    for x in (-0.13, 0.13):                                                        # Poke Ball roundels on the robe
        ball(x, 0.86, 0.045)


def card_face(rank, suit, hp=120):
    """A Poker Mon card face (500 x 700, RGBA, transparent corners)."""
    key = ('F', rank, suit, hp)
    if key in _CARDS:
        return _CARDS[key]
    im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    _rounded(d, (0, 0, CW - 1, CH - 1), 34, YELLOW, INK, 4)                       # the trading card's border
    _rounded(d, (22, 22, CW - 23, CH - 23), 20, YELLOW_D)
    _rounded(d, (26, 26, CW - 27, CH - 27), 18, (252, 252, 248), INK, 3)         # the playing card's face
    ch, col = SUITS[suit]
    d.text((CW - 46, 52), f'HP {hp}', font=_font(FONT, 34), fill=RED, anchor='rm')          # the HP, top right
    d.text((62, 50), rank, font=_font(FONT, 64), fill=col, anchor='mt')                      # the index
    _suit_shape(d, 62, 150, 54, suit)
    pic = (104, 100, CW - 104, CH - 100)
    if rank == 'Q':
        d.rectangle(pic, outline=ROYAL, width=5)                                             # the thin blue frame
        cx, w, h2 = CW / 2, pic[2] - pic[0], (pic[3] - pic[1]) / 2
        _queen_half(d, cx, pic[1] + 4, w, h2 - 4, suit, False)
        _queen_half(d, cx, pic[1] + h2, w, h2 - 4, suit, True)
        d.line([(pic[0], CH / 2), (pic[2], CH / 2)], fill=INK, width=3)
        _suit_shape(d, pic[0] + 44, pic[1] + 46, 58, suit)                                   # the big pip
        _suit_shape(d, pic[2] - 44, pic[3] - 46, 58, suit)
    else:
        n = {'A': 1, 'J': 1, 'K': 1}.get(rank) or int(rank)
        grid = {1: [(0, 0)], 2: [(0, -1), (0, 1)], 3: [(0, -1), (0, 0), (0, 1)],
                4: [(-1, -1), (1, -1), (-1, 1), (1, 1)], 5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)],
                6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)],
                7: [(-1, -1), (1, -1), (0, -0.5), (-1, 0), (1, 0), (-1, 1), (1, 1)],
                8: [(-1, -1), (1, -1), (0, -0.5), (-1, 0), (1, 0), (0, 0.5), (-1, 1), (1, 1)],
                9: [(-1, -1), (1, -1), (-1, -0.33), (1, -0.33), (0, 0), (-1, 0.33), (1, 0.33), (-1, 1), (1, 1)],
                10: [(-1, -1), (1, -1), (0, -0.66), (-1, -0.33), (1, -0.33), (-1, 0.33), (1, 0.33), (0, 0.66),
                     (-1, 1), (1, 1)]}[n]
        cx, cy = CW / 2, CH / 2
        for gx, gy in grid:
            _suit_shape(d, cx + gx * 90, cy + gy * 190, 110 if n == 1 else 84, suit)
    tmp = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))                                   # the index, upside down
    dt = ImageDraw.Draw(tmp)
    dt.text((62, 50), rank, font=_font(FONT, 64), fill=col, anchor='mt')
    _suit_shape(dt, 62, 150, 54, suit)
    corner = tmp.crop((20, 30, 110, 190)).rotate(180)
    im.alpha_composite(corner, (CW - 110, CH - 190))
    _CARDS[key] = im
    return im


def logo(text='POKER MON', width=420, height=110):
    """The chunky yellow logo with its blue outline, letters stepping up to the middle (refs card-back-1..2)."""
    im = Image.new('RGBA', (width, height + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    n = len(text)
    x = 10
    sizes = [height * (0.72 + 0.28 * math.sin(math.pi * (i + 0.5) / n)) for i in range(n)]
    widths = [_font(LOGO_FONT, sz).getlength(ch) * 1.05 if ch != ' ' else sz * 0.18 for ch, sz in zip(text, sizes)]
    k = (width - 20) / sum(widths)
    for ch, sz, w in zip(text, sizes, widths):
        if ch != ' ':
            f = _font(LOGO_FONT, sz * k)
            y = height + 30 - sz * k * 0.08
            d.text((x, y), ch, font=f, fill=YELLOW, anchor='ls', stroke_width=max(3, int(sz * k * 0.09)),
                   stroke_fill=LOGO_BLUE)
        x += w * k
    return im


def card_back():
    """The Poker Mon card back (500 x 700, RGBA)."""
    if 'B' in _CARDS:
        return _CARDS['B']
    im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    _rounded(d, (0, 0, CW - 1, CH - 1), 34, BACK_BLUE_D, INK, 4)
    _rounded(d, (24, 24, CW - 25, CH - 25), 20, BACK_BLUE)
    cx, cy = CW * 0.55, CH * 0.5
    for k in range(7):                                                            # the swirl spinning out
        pts = [(cx + (16 + 34 * k + 22 * a) * math.cos(a + k * 0.9), cy + (16 + 34 * k + 22 * a) * math.sin(a + k * 0.9))
               for a in np.linspace(0, 4.2, 40)]
        d.line(pts, fill=SWIRL if k % 2 == 0 else (70, 120, 196), width=14 - k)
    mask = Image.new('L', (CW, CH), 0)
    ImageDraw.Draw(mask).rounded_rectangle((24, 24, CW - 25, CH - 25), 20, fill=255)
    inner = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    inner.paste(im, (0, 0), mask)
    im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    _rounded(d, (0, 0, CW - 1, CH - 1), 34, BACK_BLUE_D, INK, 4)
    im.alpha_composite(inner)
    ball = poke_ball(150)
    im.alpha_composite(ball.rotate(-18, resample=Image.BICUBIC), (int(cx - 75), int(cy - 75)))
    lg = logo()
    im.alpha_composite(lg, (40, 30))
    im.alpha_composite(lg.rotate(180), (40, CH - 30 - lg.height))
    _CARDS['B'] = im
    return im


def poke_ball(size, top=RED, band=INK, bottom=(250, 250, 248), stripes=None):
    """A Poke Ball from the front: the top half `top`, the bottom white, the black band and the white button."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = size / 2 - 3
    c = size / 2
    d.ellipse([c - r, c - r, c + r, c + r], fill=bottom, outline=INK, width=max(2, size // 40))
    d.pieslice([c - r, c - r, c + r, c + r], 180, 360, fill=top, outline=INK, width=max(2, size // 40))
    if stripes:
        for sx in (-0.45, 0.45):
            d.ellipse([c + sx * r - r * 0.16, c - r * 0.86, c + sx * r + r * 0.16, c - r * 0.2], fill=stripes)
    d.rectangle([c - r, c - size * 0.05, c + r, c + size * 0.05], fill=band)
    d.ellipse([c - size * 0.15, c - size * 0.15, c + size * 0.15, c + size * 0.15], fill=band)
    d.ellipse([c - size * 0.1, c - size * 0.1, c + size * 0.1, c + size * 0.1], fill=(250, 250, 248), outline=INK,
              width=max(1, size // 60))
    return im


# Chips are Poke Balls with a poker chip's rim (refs casino-royale: red, blue, white, a few green): the denominations
# are the ball kinds: Poke Ball (red), Great Ball (blue with red flashes), Ultra Ball (black with yellow), and the rare
# Master Ball (purple) on top of the big stacks.
CHIPS = {'poke': (RED, None), 'great': ((40, 110, 200), (220, 40, 50)), 'ultra': ((30, 30, 34), (250, 200, 40)),
         'master': ((120, 50, 150), (220, 90, 170))}


def chip_face(kind, size=160):
    key = ('C', kind, size)
    if key in _CARDS:
        return _CARDS[key]
    top, stripes = CHIPS[kind]
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c, r = size / 2, size / 2 - 2
    d.ellipse([c - r, c - r, c + r, c + r], fill=top, outline=INK, width=3)
    for a in range(8):                                                             # the chip's rim marks
        aa = a * math.pi / 4
        x, y = c + r * 0.86 * math.cos(aa), c + r * 0.86 * math.sin(aa)
        d.ellipse([x - r * 0.1, y - r * 0.1, x + r * 0.1, y + r * 0.1], fill=(250, 250, 248))
    ball = poke_ball(int(size * 0.66), top=top, stripes=stripes)
    im.alpha_composite(ball, (int(c - ball.width / 2), int(c - ball.height / 2)))
    _CARDS[key] = im
    return im


def place_image(img, cam, src, quad, shade=1.0):
    """Lay a flat picture (card, chip) into the frame: its corners TL, TR, BR, BL go to the world points `quad`."""
    q = [cam.P(*pt) for pt in quad]
    xs, ys = [x for x, _ in q], [y for _, y in q]
    x0, y0, x1, y1 = int(min(xs)) - 2, int(min(ys)) - 2, int(max(xs)) + 3, int(max(ys)) + 3
    if x1 <= 0 or y1 <= 0 or x0 >= img.width or y0 >= img.height or x1 - x0 < 2 or y1 - y0 < 2:
        return
    w, h = src.size
    import numpy.linalg as la
    A, b_ = [], []
    for (X, Y), (u, v) in zip([(x - x0, y - y0) for x, y in q], [(0, 0), (w, 0), (w, h), (0, h)]):
        A.append([X, Y, 1, 0, 0, 0, -u * X, -u * Y]); b_.append(u)
        A.append([0, 0, 0, X, Y, 1, -v * X, -v * Y]); b_.append(v)
    try:
        coef = la.solve(np.array(A, float), np.array(b_, float))
    except la.LinAlgError:
        return
    out = src.transform((x1 - x0, y1 - y0), Image.PERSPECTIVE, tuple(coef), Image.BICUBIC)
    if shade != 1.0:
        a = np.asarray(out, np.float32)
        a[..., :3] *= shade
        out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
    img.alpha_composite(out, (x0, y0)) if x0 >= 0 and y0 >= 0 else img.paste(out, (x0, y0), out)


def card_quad(cx, cy, w, ang=0.0, squash=1.0):
    """A card's four corners on the table: centre, width (world), turn (degrees), squash (the table's perspective)."""
    h = w * CH / CW
    a = math.radians(ang)
    out = []
    for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        x = dx * math.cos(a) - dy * math.sin(a)
        y = dx * math.sin(a) + dy * math.cos(a)
        out.append((cx + x, cy + y * squash))
    return out


def chip_stack(img, cam, cx, cy, r, n, kind, squash=0.45, seed=0):
    """A stack of n chips standing on the table at (cx, cy): the edges, then the top face laid flat."""
    rng = np.random.default_rng(seed)
    p = B.Pen(img, cam)
    top, stripes = CHIPS[kind]
    th = r * 0.22
    for i in range(n):
        ox = rng.uniform(-r * 0.06, r * 0.06)
        y = cy - i * th
        p.poly([(cx + ox - r, y - th / 2)] + [(cx + ox + r * math.cos(a), y + r * squash * math.sin(a))
                                               for a in np.linspace(0, math.pi, 16)] + [(cx + ox + r, y - th / 2)],
               top, INK, 1.6)
        for a in np.linspace(0.3, math.pi - 0.3, 4):
            x = cx + ox + r * math.cos(a)
            p.line([(x, y - th * 0.4 + r * squash * math.sin(a)), (x, y + r * squash * math.sin(a))],
                   (250, 250, 248), 2.0)
    yt = cy - n * th
    place_image(img, cam, chip_face(kind), [(cx - r, yt - r * squash), (cx + r, yt - r * squash),
                                             (cx + r, yt + r * squash), (cx - r, yt + r * squash)])


# ------------------------------------------------------------------------------------------------ fire and light
FLAME_O = (240, 112, 30)
FLAME_Y = (255, 214, 80)
FLAME_W = (255, 246, 200)


def flame(p, x, y, h, t, seed=0, lean=0.0):
    """A cartoon flame standing on (x, y), h tall: a lumpy orange tongue round a yellow heart, both licking and
    flickering (their shape changes every frame), one outline; flat colour (the glow round it is added as light)."""
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 6.28)
    k = 1.0 + 0.16 * math.sin(t * 17 + ph) + 0.1 * math.sin(t * 29 + ph * 2)
    hh = h * k
    w = h * 0.36
    sway = (math.sin(t * 9 + ph) * 0.18 + lean) * hh

    def tongue(scale, col, line):
        pts = []
        for i, a in enumerate(np.linspace(0, math.pi, 9)):
            r = 1.0 + 0.12 * math.sin(i * 2.3 + t * 21 + ph)
            pts.append((x + math.cos(a) * w * scale * r, y - math.sin(a) * w * 0.7 * scale * r))
        tip = (x + sway * scale, y - hh * scale)
        mid_l = (x - w * 0.5 * scale + sway * 0.4 * scale, y - hh * 0.55 * scale)
        mid_r = (x + w * 0.45 * scale + sway * 0.5 * scale, y - hh * 0.6 * scale)
        poly = [pts[0]] + [mid_r, (tip[0] + w * 0.12 * scale, tip[1] + hh * 0.18 * scale), tip, mid_l] + [pts[-1]]
        poly += [(x + math.cos(a) * w * scale, y + math.sin(a) * w * 0.35 * scale) for a in np.linspace(math.pi, 2 * math.pi, 7)]
        p.poly(curve(poly, 2), col, line, 1.6)
    tongue(1.0, FLAME_O, INK)
    tongue(0.55, FLAME_Y, None)
    tongue(0.25, FLAME_W, None)


BRASS = (206, 160, 70)
BRASS_D = (150, 108, 40)
BRASS_L = (240, 206, 120)
WAX = (246, 238, 214)
WAX_D = (222, 210, 182)


def candle(p, x, y, h, t, seed=0, lit=True, w=None):
    """A candle in a brass candlestick standing on (x, y), h tall overall: a stepped round foot, a turned stem with
    a knop, a drip pan, then the candle (wax drips down its side), its wick and flame. Flat colour, one outline."""
    w = w or h * 0.08                                  # the candle's half-width
    hold = h * 0.42                                    # the candlestick's height; the candle is the rest
    fw = w * 3.2
    p.poly([(x - fw, y), (x + fw, y), (x + fw * 0.8, y - hold * 0.08), (x - fw * 0.8, y - hold * 0.08)], BRASS, INK, 1.4)
    p.poly([(x - fw * 0.6, y - hold * 0.08), (x + fw * 0.6, y - hold * 0.08), (x + fw * 0.3, y - hold * 0.18),
            (x - fw * 0.3, y - hold * 0.18)], BRASS_D, INK, 1.2)
    p.poly([(x - w * 0.55, y - hold * 0.18), (x + w * 0.55, y - hold * 0.18), (x + w * 0.4, y - hold * 0.88),
            (x - w * 0.4, y - hold * 0.88)], BRASS, INK, 1.2)                          # the stem
    p.ell(x, y - hold * 0.5, w * 1.1, hold * 0.06, BRASS_L, INK, 1.0)                    # its knop
    p.poly([(x - w * 2.0, y - hold * 0.9), (x + w * 2.0, y - hold * 0.9), (x + w * 1.5, y - hold), (x - w * 1.5, y - hold)],
           BRASS, INK, 1.2)                                                           # the drip pan
    top = y - h
    p.poly([(x - w, y - hold), (x + w, y - hold), (x + w, top), (x - w, top)], WAX, INK, 1.4)
    rng = np.random.default_rng(seed)
    for k in range(2):                                                               # wax drips
        dx = rng.uniform(-0.7, 0.7) * w
        dl = rng.uniform(0.15, 0.45) * (h - hold)
        p.poly([(x + dx - w * 0.22, top + 2), (x + dx + w * 0.22, top + 2), (x + dx + w * 0.16, top + dl),
                (x + dx - w * 0.16, top + dl)], WAX_D, None)
    p.line([(x, top), (x, top - w * 0.7)], INK, 1.4)
    if lit:
        flame(p, x, top - w * 0.3, w * 3.2 * flicker(t, seed), t, seed)


def candelabra2(p, x, y, h, t, seed=0, lit=True):
    """A three-branched brass candelabra standing on (x, y), h tall: a round foot, a turned stem, two scrolled arms,
    three drip pans and candles."""
    w = h * 0.035
    p.poly([(x - h * 0.16, y), (x + h * 0.16, y), (x + h * 0.11, y - h * 0.05), (x - h * 0.11, y - h * 0.05)], BRASS, INK, 1.4)
    p.poly([(x - w * 0.7, y - h * 0.05), (x + w * 0.7, y - h * 0.05), (x + w * 0.5, y - h * 0.5), (x - w * 0.5, y - h * 0.5)],
           BRASS, INK, 1.2)
    p.ell(x, y - h * 0.26, w * 1.5, h * 0.03, BRASS_L, INK, 1.0)
    for sg in (-1, 1):
        arm = open_curve([(x, y - h * 0.46), (x + sg * h * 0.12, y - h * 0.4), (x + sg * h * 0.2, y - h * 0.48),
                     (x + sg * h * 0.2, y - h * 0.55)], 4)
        p.line(arm, INK, max(3, w * 1.4))
        p.line(arm, BRASS, max(2, w * 0.9))
    for dx, base in ((-0.2, 0.55), (0.0, 0.62), (0.2, 0.55)):
        cx, cy = x + dx * h, y - base * h
        p.poly([(cx - w * 1.8, cy), (cx + w * 1.8, cy), (cx + w * 1.3, cy - h * 0.025), (cx - w * 1.3, cy - h * 0.025)],
               BRASS, INK, 1.0)
        top = cy - h * 0.33
        p.poly([(cx - w * 0.75, cy - h * 0.025), (cx + w * 0.75, cy - h * 0.025), (cx + w * 0.75, top), (cx - w * 0.75, top)],
               WAX, INK, 1.2)
        p.line([(cx, top), (cx, top - w * 0.6)], INK, 1.2)
        if lit:
            flame(p, cx, top - w * 0.3, w * 2.6 * flicker(t, seed + int(dx * 10)), t, seed + int(dx * 10))


def sconce(p, x, y, k, t, seed=0):
    """A brass wall sconce at (x, y) on the wall, k px a metre: a shaped backplate, a scrolled arm, a drip pan, a
    candle under a little pleated shade."""
    p.poly(rough([(x - 0.05 * k, y - 0.02 * k), (x + 0.05 * k, y - 0.02 * k), (x + 0.04 * k, y + 0.16 * k),
                  (x, y + 0.2 * k), (x - 0.04 * k, y + 0.16 * k)], 1, seed), BRASS, INK, 1.4)
    arm = open_curve([(x, y + 0.1 * k), (x + 0.06 * k, y + 0.12 * k), (x + 0.1 * k, y + 0.06 * k), (x + 0.1 * k, y)], 3)
    p.line(arm, INK, max(3, 0.018 * k))
    p.line(arm, BRASS, max(2, 0.011 * k))
    candle(p, x + 0.1 * k, y, 0.2 * k, t, seed, w=0.012 * k)


def flicker(t, seed=0):
    """A candle's brightness: steady with small wavers and, now and then, a sudden gutter or flare."""
    rng = np.random.default_rng(seed + 900)
    ph = rng.uniform(0, 100)
    v = 1.0 + 0.06 * math.sin(t * 13 + ph) + 0.05 * math.sin(t * 23.7 + ph * 1.3)
    gust = math.sin(t * 0.9 + ph) * math.sin(t * 2.3 + ph * 0.7)
    if gust > 0.82:                                  # the occasional flicker
        v *= 0.65 + 0.7 * abs(math.sin(t * 40 + ph))
    return v


def glass(p, x, y, h, kind='tumbler', drink=(196, 120, 40)):
    """Drinks on the table, standing on (x, y), h tall: a cut-crystal whisky tumbler (a heavy base, a lattice of
    cuts, whisky with its surface, two ice cubes), a champagne flute (bubbles rising, a slim stem and foot) or a
    martini glass (gin, an olive on a pick)."""
    gl = (214, 228, 234)
    gl_l = (244, 250, 252)
    if kind == 'tumbler':
        w = h * 0.46
        rim = h * 0.12
        p.poly([(x - w, y - h), (x + w, y - h), (x + w * 0.9, y), (x - w * 0.9, y)], gl, INK, 1.6)
        lv = y - h * 0.55                                                              # the whisky's surface
        p.poly([(x - w * 0.95, lv), (x + w * 0.95, lv), (x + w * 0.88, y - h * 0.16), (x - w * 0.88, y - h * 0.16)], drink, None)
        p.ell(x, lv, w * 0.95, rim * 0.5, B.lt(drink, 1.2) if hasattr(B, 'lt') else drink, INK, 1.0)
        for dx, dy, sz in ((-0.35, -0.08, 0.36), (0.25, -0.02, 0.3)):                 # ice
            cx, cy = x + dx * w, lv + dy * h
            p.poly([(cx - sz * w, cy - sz * w * 0.6), (cx + sz * w * 0.8, cy - sz * w * 0.8), (cx + sz * w, cy + sz * w * 0.4),
                    (cx - sz * w * 0.7, cy + sz * w * 0.6)], (236, 244, 248), INK, 1.0)
            p.line([(cx - sz * w * 0.6, cy - sz * w * 0.3), (cx - sz * w * 0.1, cy - sz * w * 0.5)], gl_l, 1.4)
        p.poly([(x - w * 0.9, y - h * 0.16), (x + w * 0.9, y - h * 0.16), (x + w * 0.9, y), (x - w * 0.9, y)],
               (196, 212, 220), INK, 1.2)                                               # the heavy base
        for i in range(-3, 4):                                                          # the cut lattice
            p.line([(x + i * w * 0.28 - w * 0.14, y - h * 0.17), (x + i * w * 0.28 + w * 0.14, y - h * 0.5)], gl_l, 1.0)
            p.line([(x + i * w * 0.28 + w * 0.14, y - h * 0.17), (x + i * w * 0.28 - w * 0.14, y - h * 0.5)], gl_l, 1.0)
        p.ell(x, y - h, w, rim * 0.5, None, INK, 1.4)                                  # the rim
        p.line([(x - w * 0.75, y - h * 0.9), (x - w * 0.7, y - h * 0.25)], gl_l, 2.0)   # a highlight
    elif kind == 'flute':
        w = h * 0.13
        p.ell(x, y, w * 1.9, w * 0.45, gl, INK, 1.2)                                   # the foot
        p.line([(x, y - h * 0.4), (x, y)], INK, 3.2)
        p.line([(x, y - h * 0.4), (x, y)], gl_l, 1.6)
        bowl = curve([(x - w, y - h), (x - w * 0.95, y - h * 0.6), (x, y - h * 0.4), (x + w * 0.95, y - h * 0.6),
                      (x + w, y - h)], 3)
        p.poly(bowl, (244, 226, 150), INK, 1.4)
        p.poly([(x - w, y - h), (x + w, y - h), (x + w * 0.98, y - h * 0.88), (x - w * 0.98, y - h * 0.88)], gl, None)
        rng = np.random.default_rng(int(abs(x) + abs(y)))
        for _ in range(5):                                                              # bubbles
            p.ell(x + rng.uniform(-0.5, 0.5) * w, y - h * rng.uniform(0.5, 0.85), max(1, w * 0.12), max(1, w * 0.12),
                  gl_l, None)
        p.ell(x, y - h, w, w * 0.3, None, INK, 1.2)
    else:                                                                               # martini
        w = h * 0.45
        p.ell(x, y, w * 0.55, w * 0.14, gl, INK, 1.2)
        p.line([(x, y - h * 0.5), (x, y)], INK, 3.2)
        p.line([(x, y - h * 0.5), (x, y)], gl_l, 1.6)
        p.poly([(x - w, y - h), (x + w, y - h), (x, y - h * 0.5)], gl, INK, 1.4)
        p.poly([(x - w * 0.8, y - h * 0.92), (x + w * 0.8, y - h * 0.92), (x, y - h * 0.52)], (232, 238, 214), None)
        p.line([(x + w * 0.5, y - h * 1.15), (x + w * 0.05, y - h * 0.7)], (120, 80, 50), 1.6)    # the pick
        p.ell(x + w * 0.22, y - h * 0.82, h * 0.07, h * 0.06, (110, 140, 50), INK, 1.0)          # the olive
        p.ell(x + w * 0.26, y - h * 0.83, h * 0.02, h * 0.02, (200, 60, 50), None)               # its pimento
        p.ell(x, y - h, w, w * 0.12, None, INK, 1.2)


def decanter(p, x, y, h):
    """A cut-glass decanter of brandy on (x, y), h tall: a round body, a neck, a ball stopper."""
    w = h * 0.36
    gl, gl_l = (214, 228, 234), (244, 250, 252)
    body = curve([(x - w * 0.7, y), (x - w, y - h * 0.3), (x - w * 0.8, y - h * 0.58), (x - w * 0.22, y - h * 0.7),
                  (x + w * 0.22, y - h * 0.7), (x + w * 0.8, y - h * 0.58), (x + w, y - h * 0.3), (x + w * 0.7, y)], 3)
    p.poly(body, gl, INK, 1.6)
    p.poly(curve([(x - w * 0.72, y - h * 0.04), (x - w * 0.95, y - h * 0.3), (x - w * 0.86, y - h * 0.45),
                  (x + w * 0.86, y - h * 0.45), (x + w * 0.95, y - h * 0.3), (x + w * 0.72, y - h * 0.04)], 3),
           (156, 74, 30), None)
    for i in range(-2, 3):
        p.line([(x + i * w * 0.32, y - h * 0.05), (x + i * w * 0.32 + w * 0.12, y - h * 0.55)], gl_l, 1.0)
    p.poly([(x - w * 0.2, y - h * 0.7), (x + w * 0.2, y - h * 0.7), (x + w * 0.16, y - h * 0.88), (x - w * 0.16, y - h * 0.88)],
           gl, INK, 1.4)
    p.ell(x, y - h * 0.94, w * 0.26, h * 0.08, gl_l, INK, 1.4)                        # the stopper


class ImgCam:
    """Draw with a Pen straight into a small picture (px), for paintings and the bust laid into the scene later."""
    def __init__(self, scale=1.0):
        self.z = self.s = scale

    def P(self, x, y):
        return x * self.s, y * self.s

    def S(self, v):
        return v * self.s


_PICS = {}


def portrait_image():
    """An old-master portrait (360 x 460 px): a gentleman three-quarter left, black hat, dark coat, white pleated
    ruff, a grey moustache and beard, a dark ground with a hint of drapery; in an ornate gilt frame."""
    if 'portrait' in _PICS:
        return _PICS['portrait']
    W_, H_ = 360, 460
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0))
    p = B.Pen(im, ImgCam())
    ink = INK
    p.poly([(0, 0), (W_, 0), (W_, H_), (0, H_)], (176, 130, 50), ink, 3)                      # the frame
    p.poly([(14, 14), (W_ - 14, 14), (W_ - 14, H_ - 14), (14, H_ - 14)], (214, 170, 80), ink, 2)
    p.poly([(28, 28), (W_ - 28, 28), (W_ - 28, H_ - 28), (28, H_ - 28)], (140, 100, 36), ink, 2)
    for cx, cy in ((21, 21), (W_ - 21, 21), (21, H_ - 21), (W_ - 21, H_ - 21)):                # corner rosettes
        p.ell(cx, cy, 11, 11, (236, 200, 110), ink, 1.6)
        p.ell(cx, cy, 4, 4, (150, 108, 40), None)
    for i in range(1, 9):                                                                     # egg-and-dart moulding
        p.ell(14 + i * (W_ - 28) / 9, 21, 7, 4, (236, 200, 110), None)
        p.ell(14 + i * (W_ - 28) / 9, H_ - 21, 7, 4, (236, 200, 110), None)
    x0, y0, x1, y1 = 36, 36, W_ - 36, H_ - 36
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], (46, 36, 30), ink, 2)                     # the dark ground
    p.poly([(x1 - 90, y0), (x1, y0), (x1, y0 + 200), (x1 - 40, y0 + 120)], (92, 30, 34), None)   # a red drape
    cx = 170
    p.poly(curve([(x0, y1), (x0 + 20, 330), (cx - 70, 290), (cx + 70, 290), (x1 - 30, 330), (x1, y1)], 4),
           (24, 22, 26), ink, 2)                                                              # the coat
    p.line([(cx + 10, 300), (cx + 20, y1)], (60, 56, 62), 2)
    for i in range(14):                                                                       # the pleated ruff
        a = math.pi * (0.95 + i * 1.1 / 13)
        rx, ry = cx + 78 * math.cos(a) * 0.95, 285 + 26 * math.sin(a) * 0.6
        p.ell(rx + 78 * 0.0, ry + 26, 12, 14, (244, 240, 230), ink, 1.2)
    p.ell(cx, 300, 76, 20, (244, 240, 230), ink, 1.6)
    face = curve([(cx - 46, 170), (cx - 50, 215), (cx - 38, 258), (cx - 8, 280), (cx + 22, 276), (cx + 44, 248),
                  (cx + 50, 205), (cx + 44, 160), (cx, 140)], 4)
    p.poly(face, (226, 188, 150), ink, 2)
    p.poly(curve([(cx - 46, 175), (cx - 50, 215), (cx - 38, 256), (cx - 14, 272), (cx - 24, 230)], 3), (196, 156, 120), None)
    p.poly(curve([(cx - 30, 246), (cx - 10, 238), (cx + 10, 238), (cx + 32, 246), (cx + 20, 282), (cx - 4, 288),
                  (cx - 24, 278)], 3), (150, 146, 140), ink, 1.4)                             # the beard
    p.poly(curve([(cx - 26, 240), (cx - 4, 233), (cx + 4, 233), (cx + 28, 240), (cx + 6, 244), (cx - 6, 244)], 3),
           (120, 116, 112), ink, 1.2)                                                         # the moustache
    p.line([(cx - 4, 252), (cx + 10, 252)], (120, 60, 56), 2)                                # the mouth
    p.line(open_curve([(cx + 6, 196), (cx + 2, 222), (cx - 6, 230), (cx + 6, 232)], 3), ink, 1.6)  # the nose
    for ex in (cx - 22, cx + 22):                                                             # the eyes, the brows
        p.poly([(ex - 11, 200), (ex, 194), (ex + 11, 200), (ex, 204)], (240, 232, 220), ink, 1.2)
        p.ell(ex + 2, 199, 3.4, 3.4, (40, 30, 26), None)
        p.line([(ex - 13, 188), (ex, 184), (ex + 13, 189)], (90, 80, 76), 2.4)
    p.poly(curve([(cx - 70, 172), (cx - 60, 130), (cx, 112), (cx + 62, 126), (cx + 74, 168), (cx + 40, 158),
                  (cx - 30, 158)], 4), (20, 18, 22), ink, 2)                                  # the black hat
    p.line([(cx - 50, 170), (cx - 48, 200)], (120, 116, 112), 3)                              # grey hair at the temple
    _PICS['portrait'] = im
    return im


def landscape_image():
    """A pastoral landscape (520 x 340 px): a pale sky with clouds, blue-grey hills, a lake, dark trees, a ruined
    tower; in a gilt frame."""
    if 'land' in _PICS:
        return _PICS['land']
    W_, H_ = 520, 340
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0))
    p = B.Pen(im, ImgCam())
    p.poly([(0, 0), (W_, 0), (W_, H_), (0, H_)], (176, 130, 50), INK, 3)
    p.poly([(14, 14), (W_ - 14, 14), (W_ - 14, H_ - 14), (14, H_ - 14)], (214, 170, 80), INK, 2)
    x0, y0, x1, y1 = 28, 28, W_ - 28, H_ - 28
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], (196, 214, 226), INK, 2)                 # the sky
    for cx, cy, r in ((120, 80, 30), (160, 70, 36), (200, 84, 28), (360, 64, 26), (392, 72, 30)):
        p.ell(cx, cy, r, r * 0.6, (240, 240, 236), None)
    p.poly(curve([(x0, 190), (110, 150), (210, 176), (320, 138), (420, 168), (x1, 150), (x1, 230), (x0, 230)], 4),
           (130, 150, 170), None)                                                              # far hills
    p.poly(curve([(x0, 214), (150, 186), (280, 206), (400, 190), (x1, 210), (x1, 250), (x0, 250)], 4), (96, 122, 86), None)
    p.poly([(x0, 240), (x1, 240), (x1, y1), (x0, y1)], (76, 104, 64), None)                    # the meadow
    p.poly(curve([(200, 252), (300, 244), (390, 254), (300, 266)], 4), (150, 182, 206), None)  # the lake
    p.poly([(400, 150), (420, 150), (420, 210), (400, 210)], (150, 140, 126), INK, 1.2)        # a ruined tower
    p.poly([(400, 150), (404, 142), (410, 150), (416, 140), (420, 150)], (150, 140, 126), INK, 1.0)
    for tx, ty, r in ((80, 232, 26), (110, 226, 20), (460, 236, 24), (436, 230, 16)):           # trees
        p.line([(tx, ty), (tx, ty + 24)], (60, 40, 30), 4)
        p.ell(tx, ty - r * 0.6, r, r, (44, 70, 40), INK, 1.2)
    _PICS['land'] = im
    return im


def bust_image():
    """A white marble bust (220 x 300 px): a classical head in profile right, curls, a draped chest."""
    if 'bust' in _PICS:
        return _PICS['bust']
    im = Image.new('RGBA', (220, 300), (0, 0, 0, 0))
    p = B.Pen(im, ImgCam())
    m, md = (238, 234, 226), (206, 200, 190)
    p.poly(curve([(20, 296), (30, 230), (70, 196), (150, 196), (196, 232), (204, 296)], 4), m, INK, 2.2)   # chest
    p.line(open_curve([(60, 210), (100, 250), (150, 236), (190, 260)], 3), md, 3)                          # drapery folds
    p.line(open_curve([(40, 250), (90, 280), (140, 270)], 3), md, 3)
    p.poly([(92, 150), (132, 150), (138, 206), (88, 206)], m, INK, 2)                                    # the neck
    head = curve([(70, 110), (76, 52), (118, 26), (162, 40), (176, 80), (184, 104), (174, 112), (178, 126),
                  (168, 132), (166, 150), (140, 160), (100, 156), (78, 140)], 4)
    p.poly(head, m, INK, 2.2)
    for cx, cy in ((90, 50), (110, 38), (132, 34), (80, 70), (78, 92), (96, 64)):                        # the curls
        p.ell(cx, cy, 13, 11, md, INK, 1.2)
    p.line([(150, 82), (160, 80)], INK, 2)                                                              # a blank eye
    p.line(open_curve([(170, 92), (182, 106), (172, 112)], 3), INK, 1.6)                                     # the nose
    p.line([(160, 128), (172, 126)], INK, 1.6)
    p.ell(98, 98, 10, 14, md, INK, 1.4)                                                                 # the ear
    _PICS['bust'] = im
    return im


def test(out):
    B.SS = 1
    img = B.canvas((214, 196, 150))
    cam = B.Cam(1.0, 540, 960)
    names = list(PEOPLE)
    for i, n in enumerate(names):
        sp = PEOPLE[n]
        x = 140 + (i % 4) * 270
        y = 260 + (i // 4) * 900
        person(img, cam, x, y, 0.62, sp, 0.0, 0, V.standing(sp))
    img.convert('RGB').save(out, quality=88)


def test_dragon(out):
    B.SS = 1
    img = B.canvas((214, 196, 150))
    cam = B.Cam(1.0, 540, 960)
    dragonite(img, cam, 300, 900, 0.5, turn=0.0)
    m = dragonite(img, cam, 800, 900, 0.5, turn=0.6, flip=-1, head=-28, mouth_open=0.8, eyes='narrow', wings=0.4)
    glow(img, cam, [(m[0], m[1], 26)])
    m2 = dragonite(img, cam, 300, 1800, 0.5, turn=0.6, flip=1, head=14, mouth_open=1.0, eyes='narrow', wings=1.0,
                   arms=1.0, lean=12)
    glow(img, cam, [(m2[0] + 30 * i, m2[1] + 12 * i, 40) for i in range(30)])
    sp = P2
    person(img, cam, 800, 1800 - 928 * 0.5, 0.5, sp, 0.0, 0, V.standing(sp))
    img.convert('RGB').save(out, quality=88)


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        test(sys.argv[2])
    elif sys.argv[1] == 'cards':
        B.SS = 1
        im = Image.new('RGBA', (2100, 1500), (40, 110, 70, 255))
        for i, sut in enumerate('SCDH'):
            im.alpha_composite(card_face('Q', sut), (20 + 520 * i, 20))
        im.alpha_composite(card_back(), (20, 760))
        for i, (r_, s_) in enumerate((('7', 'C'), ('2', 'D'))):
            im.alpha_composite(card_face(r_, s_, 60), (540 + 520 * i, 760))
        for i, k in enumerate(CHIPS):
            im.alpha_composite(chip_face(k, 220), (1580 + (i % 2) * 250, 780 + (i // 2) * 250))
        im.convert('RGB').save(sys.argv[2], quality=88)
    elif sys.argv[1] == 'eyes':                       # Sam's pick: the Dragonite's eyes while it fires
        B.SS = 1
        sheet = Image.new('RGB', (3 * 520, 2 * 600), (40, 34, 30))
        for i, e in enumerate(EYE_STYLES):
            im = B.canvas((214, 196, 150))
            cam = B.Cam(1.0, 540, 960)
            m = dragonite(im, cam, 540, 2200, 1.45, turn=0.3, head=16, lean=10, mouth_open=1.0, eyes=e, wings=1.0,
                          arms=1.0, mouth_shape='o')
            glow(im, cam, [(m[0] + 30 * k, m[1] + 22 * k, 40 + 4 * k) for k in range(14)])
            crop = im.crop((330, 0, 1080, 865)).resize((520, 600)).convert('RGB')
            sheet.paste(crop, ((i % 3) * 520, (i // 3) * 600))
            d = ImageDraw.Draw(sheet)
            d.text(((i % 3) * 520 + 16, (i // 3) * 600 + 12), f'{i + 1}. {e}', font=_font(FONT, 34), fill=(250, 250, 250),
                   stroke_width=3, stroke_fill=(20, 20, 20))
        sheet.save(sys.argv[2], quality=90)
    elif sys.argv[1] == 'dragon':
        test_dragon(sys.argv[2])
