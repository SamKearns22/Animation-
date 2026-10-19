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
from ed import INK, curve, oval  # noqa: E402
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
PEOPLE = {'P1': P1, 'P2': P2, 'LADY': LADY, 'CARDS': CARDS, 'OLD': OLD, 'DEALER': DEALER, 'GUARD1': GUARD1,
          'GUARD2': GUARD2}
HEIGHTS = {'P1': 1.83, 'P2': 1.85, 'LADY': 1.70, 'CARDS': 1.80, 'OLD': 1.74, 'DEALER': 1.78, 'GUARD1': 1.93,
           'GUARD2': 1.90}


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
        if sp.get('bow'):
            bow_tie(p, 0, 4, sp['bow'])
        if sp.get('earpiece'):                         # the coiled wire, inked like everything else
            wire = curve([(sp['hw'] - 4, -150), (sp['hw'] + 12, -110), (sp['hw'] + 4, -40), (sp['hw'] - 14, 10)], 3)
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
    pts = curve(pts, 3) if len(pts) > 2 else pts
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
    """One small bat wing from the shoulder blade: an orange arm along the top edge, teal skin scalloped between the
    fingers. spread 0 (folded up behind) .. 1 (wide open)."""
    tip = (sx + sg * (230 + 170 * spread) * k, sy - (300 - 150 * spread) * k)
    elbow = (sx + sg * (110 + 60 * spread) * k, sy - (230 - 60 * spread) * k)
    f1 = (sx + sg * (230 + 150 * spread) * k, sy - (70 - 60 * spread) * k)
    f2 = (sx + sg * (110 + 70 * spread) * k, sy + (10 + 30 * spread) * k)
    skin = [(sx, sy), elbow, tip, (tip[0] - sg * 10 * k, tip[1] + 60 * k),
            ((tip[0] + f1[0]) / 2 - sg * 40 * k, (tip[1] + f1[1]) / 2 - 10 * k), f1,
            ((f1[0] + f2[0]) / 2 - sg * 40 * k, (f1[1] + f2[1]) / 2 - 20 * k), f2, (sx, sy + 30 * k)]
    p.poly(skin, TEAL, INK, 2.6)
    for f in (f1, f2):
        p.line([elbow, f], TEAL_D, 2.4)
    tube(p, [(sx, sy), elbow, tip], 44 * k, 14 * k, ORANGE)


def dragonite_head(p, piv, deg, turn, mouth_open, eyes):
    """The head on its neck pivot, rotated by deg (negative: thrown back, chin up). turn 0 front .. 1 three-quarter
    to the right. mouth_open 0..1; eyes 'open', 'narrow', 'closed', 'wide'. Returns the mouth centre."""
    R = lambda pts: _rot(pts, piv, deg)
    hx, hy = piv[0] + 30 * turn, piv[1] - 200                      # the skull's centre
    sx, sy = hx + 70 * turn, hy + 70                               # the snout's centre, toward the side it faces
    for sg in (-1, 1):                                             # antennae, behind: thin, curling back and out
        k = 1.0 if sg > 0 else 1.0 - 0.3 * turn
        bx = hx + sg * 40 * k - 20 * turn
        by = hy - 128
        ant = [(bx, by), (bx + sg * 24 * k, by - 90), (bx + sg * 80 * k, by - 150), (bx + sg * 150 * k, by - 160),
               (bx + sg * 186 * k, by - 128)]
        tube(p, R(ant), 18, 9, ORANGE, 2.0)
    p.poly(R(_ovl(hx - 10 * turn, hy, 160, 150)), ORANGE, INK, 2.8)                   # the skull
    p.poly(R([(hx - 18 - 14 * turn, hy - 138), (hx + 18 - 14 * turn, hy - 138), (hx - 16 * turn, hy - 196)]),
           ORANGE, INK, 2.2)                                                            # the small horn
    jaw = 80 * mouth_open
    if mouth_open > 0.02:                                          # open: the dark mouth between snout and jaw
        p.poly(R(_ovl(sx + 6 * turn, sy + 40 + jaw * 0.45, 110, 34 + jaw * 0.55)), MOUTH, INK, 2.6)
        p.poly(R(_ovl(sx + 6 * turn, sy + 62 + jaw * 0.6, 60, 14 + jaw * 0.2)), TONGUE, None)
        p.poly(R(_ovl(sx, sy + 70 + jaw, 118 + 10 * turn, 44)), ORANGE, INK, 2.6)       # the lower jaw
        p.poly(R(_ovl(sx, sy - 6, 150 + 10 * turn, 74)), ORANGE, INK, 2.8)              # the upper snout
    else:
        p.poly(R(_ovl(sx, sy, 150 + 10 * turn, 100)), ORANGE, INK, 2.8)                 # the snout
        p.line(R(curve([(sx - 70, sy + 40), (sx - 30, sy + 64), (sx + 30, sy + 64), (sx + 74, sy + 38)], 3)), INK, 3.2)
    p.poly(R(_ovl(hx - 6 * turn, hy + 10, 140, 64)), ORANGE, None)                     # one shape: no seam line
    for sg in (-1, 1):
        p.ell(*R([(sx + sg * 32 + 12 * turn, sy - 30)])[0], 7, 5, INK, None)           # nostrils
    for sg in (-1, 1):                                                                  # the big friendly eyes
        k = 1.0 if sg > 0 else 1.0 - 0.3 * turn
        ex, ey = hx + sg * 66 * k + 34 * turn, hy - 30
        if eyes == 'closed':
            p.line(R([(ex - 24, ey + 2), (ex, ey + 12), (ex + 24, ey + 2)]), INK, 3.6)
        elif eyes == 'narrow':                                     # determined: the top of the eye cut by a lid
            p.poly(R([(ex - 24 * k, ey - 4 - sg * 6), (ex + 24 * k, ey - 4 + sg * 6), (ex + 22 * k, ey + 18),
                      (ex - 22 * k, ey + 18)]), INK, INK, 2.0)
            p.ell(*R([(ex + 8, ey + 4)])[0], 6, 5, (250, 250, 250), None)
        else:
            r = 1.2 if eyes == 'wide' else 1.0
            p.poly(R(_ovl(ex, ey, 26 * k * r, 36 * r)), INK, INK, 2.0)
            p.ell(*R([(ex + 9, ey - 13)])[0], 9, 10, (250, 250, 250), None)
    return R([(sx + 6 * turn, sy + 40 + jaw * 0.45)])[0]


def dragonite(img, cam, x, y, s, t=0.0, turn=0.5, flip=1, head=0.0, mouth_open=0.0, eyes='open', wings=0.15,
              arms=0.0, lean=0.0, bow=True):
    """The Dragonite standing, feet at world (x, y), scale s (the people's scale), turned `turn` (0 facing us .. 1
    three-quarter) toward the right of frame (flip=-1: toward the left). head: degrees (negative thrown back);
    arms 0 at its sides .. 1 out wide (bracing); lean: degrees forward (+). Returns the mouth point (world)."""
    L = B.Local(cam, x, y, s, flip)
    p = B.Pen(img, L)
    T = lambda pts: _rot(pts, (0, -380), lean)
    tail = curve([(-80, -260), (-320, -230), (-520, -120), (-640, -10), (-720, 50), (-600, 40), (-450, -20),
                  (-280, -90), (-90, -120)], 4)                                         # the tail, behind
    p.poly(T(tail), ORANGE, INK, 2.8)
    p.line(T(curve([(-560, 0), (-400, -90), (-230, -150)], 3)), CREAM_D, 3)
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
    body = curve([(-120, -1010), (-200, -920), (-290, -720), (-380, -440), (-390, -260), (-300, -110), (0, -60),
                  (300, -110), (390, -260), (380, -440), (290, -720), (200, -920), (120, -1010)], 5)
    p.poly(T(body), ORANGE, INK, 3.0)
    bx = 50 * turn
    belly = curve([(bx - 90, -990), (bx - 160, -880), (bx - 230, -680), (bx - 300, -430), (bx - 290, -250),
                   (bx - 200, -120), (bx, -90), (bx + 200, -120), (bx + 290, -250), (bx + 300, -430),
                   (bx + 230, -680), (bx + 160, -880), (bx + 90, -990)], 5)
    p.poly(T(belly), CREAM, INK, 2.6)
    for k in range(1, 9):                                                               # the bands across the belly
        yb = -990 + k * 102
        f = (yb + 990) / 900
        w_ = 90 + 210 * math.sin(math.pi * min(1.0, f * 0.62 + 0.08)) ** 0.8
        p.line(T(curve([(bx - w_ * 0.96, yb - 6), (bx, yb + 14), (bx + w_ * 0.96, yb - 6)], 3)), CREAM_D, 2.6)
    for sg in (-1, 1):                                                                  # short arms, circle hands
        sh = (sg * 190 + 40 * turn, -840)
        hand = (sh[0] + sg * (90 + 200 * arms), sh[1] + 170 - 120 * arms)
        el = (sh[0] + sg * (70 + 90 * arms), sh[1] + 100 - 30 * arms)
        tube(p, T([sh, el, hand]), 84, 64, ORANGE)
        p.poly(T(_ovl(*hand, 46, 46)), ORANGE, INK, 2.6)
    if bow:
        bp = T([(40 * turn, -1000)])[0]
        bow_tie(p, bp[0], bp[1], (22, 22, 28), 2.4)
    piv = T([(0, -1000)])[0]
    m = dragonite_head(p, piv, head + lean, turn, mouth_open, eyes)
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
    for x in (-0.1, 0.0, 0.1):
        el(x, 0.15, 0.02, 0.02, RED)
    fx = 0.3                                                                                          # the flower
    d.line([P(fx, 0.9), P(fx, 0.62)], fill=(40, 120, 60), width=5)
    for a in range(5):
        aa = a * 2 * math.pi / 5
        q = P(fx + 0.05 * math.cos(aa), 0.6 + 0.035 * math.sin(aa))
        d.ellipse([q[0] - 9, q[1] - 9, q[0] + 9, q[1] + 9], fill=RED, outline=INK)
    q = P(fx, 0.6)
    d.ellipse([q[0] - 6, q[1] - 6, q[0] + 6, q[1] + 6], fill=MUSTARD, outline=INK)


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
    elif sys.argv[1] == 'dragon':
        test_dragon(sys.argv[2])
