#!/usr/bin/env python3
"""Power Crime Action (TikTok satire): the people, their uniforms and the props (notes/power-crime-action.md).

Everyone is built on the satire package (views.person: any angle, posed on the hidden skeleton). Drawn here: the
old lady's curls and striped glasses (Cry Minister's design), the Met's uniforms (hi-vis, the senior officer's white
shirt and peaked cap, the armed officers' armour, caps and carbines, Jenkins's stab vest), the senior officer's
mirrored aviators, the protesters' keffiyehs, flags and placards, and her placard.

Her placard reads I OPPOSE / GENOCIDE / I SUPPORT. Its lower part is never lettered at all (Sam, 20 Oct: the rest
is only implied), so nothing can ever show, whatever the camera or the throw does.

    python3 source/power_crime_cast.py test OUT.jpg     everyone on one quick sheet (working picture)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import mossad                    # noqa: E402,F401  (brows, mouths, hair; patched into burnham on import)
import mouths                    # noqa: E402
import views as V                # noqa: E402
from ed import INK, curve, oval  # noqa: E402
from satire_style import rough, install_circle_hands   # noqa: E402

import figure as F               # noqa: E402
import limbs                     # noqa: E402

mouths.install(B)
install_circle_hands(B)
F.guard(B)                       # every arm measured against the rig
limbs.install(B)                 # the smooth, shaped arms of the house style (Sam, 20 Oct: no blocky arms)

_circle_hand = B.gesture_hand


def _gesture_hand(p, el, wr, shape, skin, extra=None, t=0.0):
    """A 'point' hand (Sam, 20 Oct: "give him a little finger pointing out for prodding Jenkins"): the circle with
    one short round-ended finger sticking out the way the forearm points (drawn first, so the circle covers its root)."""
    if shape == 'point':
        dx, dy = wr[0] - el[0], wr[1] - el[1]
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        cx, cy = wr[0] + ux * 12, wr[1] + uy * 12
        tip = (cx + ux * 50, cy + uy * 50)
        w = 8.5
        p.poly([(cx - uy * w, cy + ux * w), (tip[0] - uy * w, tip[1] + ux * w), (tip[0] + uy * w, tip[1] - ux * w),
                (cx + uy * w, cy - ux * w)], skin, INK, 2.2)
        p.ell(tip[0], tip[1], w, w, skin, INK, 2.2)
        p.poly([(tip[0] - ux * 6 - uy * (w - 1.5), tip[1] - uy * 6 + ux * (w - 1.5)),
                (tip[0] - ux * 6 + uy * (w - 1.5), tip[1] - uy * 6 - ux * (w - 1.5)),
                (cx + uy * (w - 1.5), cy - ux * (w - 1.5)), (cx - uy * (w - 1.5), cy + ux * (w - 1.5))], skin, None)
    return _circle_hand(p, el, wr, shape, skin, extra, t)


B.gesture_hand = _gesture_hand

# ------------------------------------------------------------------------------------------------ colours
HIVIS, HIVIS_D = (212, 226, 40), (170, 182, 30)
SILVER = (206, 210, 216)
UNIFORM = (30, 32, 40)            # the Met's black wicking tops and trousers
ARV_TOP = (36, 40, 56)            # armed officers: dark navy
ARMOUR, ARMOUR_D = (26, 27, 31), (16, 16, 19)
WHITE_SHIRT = (244, 244, 240)
CAP, CAP_D = (22, 22, 28), (12, 12, 16)
POLICE_BLUE = (30, 60, 140)
GUN, GUN_D = (72, 74, 80), (48, 50, 56)     # a shade lighter than the armour, so it reads
CARD, CARD_D = (196, 160, 112), (168, 134, 90)          # brown corrugated cardboard
MARKER = (24, 22, 26)
FONT = os.path.join(HERE, 'fonts', 'Caveat-Latin-Bold.woff')
BLOCK = os.path.join(HERE, 'fonts', 'Anton-Regular.ttf')
PAL_FLAG = ((20, 20, 22), (246, 246, 242), (20, 122, 62), (206, 32, 42))   # black, white, green; red triangle

# ------------------------------------------------------------------------------------------------ the people
# The old lady (Cry Minister's, Sam: "use model from Wolves"): little and petite, a pink frock trimmed in black,
# curly white hair, big white-and-pink striped glasses. Her stick and handbag are left out: both hands hold the sign.
GRAN = dict(name='GRAN', skin=(244, 214, 200), hw=62, hh=80, jaw='soft', hair='crop', hair_c=(246, 244, 240),
            brow_c=(214, 208, 204), outfit='dress', dress=(238, 150, 184), jacket=(238, 150, 184),
            trousers=(244, 240, 236), shoulders=120, bottom=600, age=True, mouth='line', curls=True,
            striped_glasses=True, trim=True, seed=31)
# The senior officer (Sam, 20 Oct: tough stubble; refs senior-1..5 for the uniform only, his face is made up): a
# Chief Superintendent, middle-aged, square-jawed; white shirt, black tie, black shoulder boards with a silver crown
# and pip, name badge; the senior peaked cap (three-row chequer, silver oak leaves on the peak); mirrored aviators.
SUPER = dict(name='SUPER', skin=B.PINK, hw=74, hh=92, jaw='square', hair='crop', hair_c=(70, 62, 58),
             brow_c=(60, 52, 48), brow_w=4.4, beard='stubble', beard_c=(64, 56, 52), heavy_stubble=True,
             outfit='jumper', jacket=WHITE_SHIRT, sleeve=WHITE_SHIRT, trousers=UNIFORM, shoulders=160, creases=2,
             mouth='set', cap='peaked', braid=True, cap_lift=0.12, aviators=True, white_shirt=True, seed=32)
# Jenkins: a young constable, lanky, eager, ginger; black top, black stab vest with POLICE, radio on the chest.
JENKINS = dict(name='JENKINS', skin=B.PALE, hw=64, hh=90, jaw='soft', hair='side', hair_c=(196, 112, 60),
               brow_c=(176, 96, 52), outfit='jumper', jacket=UNIFORM, trousers=UNIFORM, shoulders=138,
               stab_vest=True, mouth='line', seed=33)


def _officer(i, skin, hair, hair_c, jaw='square', hw=70, hh=90, sw=152, mouth='set', brows=None, **kw):
    return dict(name=f'PC{i}', skin=skin, hw=hw, hh=hh, jaw=jaw, hair=hair, hair_c=hair_c,
                brow_c=B.dk(hair_c, 0.85) if hair != 'bald' else (90, 70, 60), outfit='jumper', jacket=HIVIS,
                trousers=UNIFORM, shoulders=sw, hivis=True, cap='peaked', mouth=mouth, brows=brows, seed=40 + i, **kw)


# The police line by a lion (refs police-1..4, police-group-lion): full hi-vis jackets (a cold April day), the flat
# chequered cap on everyone; a mix of faces, men and women.
PCS = [_officer(1, B.PALE, 'crop', (110, 80, 54)),
       _officer(2, B.BROWN, 'bob', (30, 24, 22), jaw='soft', hw=64, hh=86, sw=134, lashes=True),
       _officer(3, B.DEEP, 'bald', (40, 32, 30), hw=74, sw=160, beard='trim', beard_c=(40, 32, 30)),
       _officer(4, B.PINK, 'side', (196, 168, 110), hw=68, hh=88, sw=146),
       _officer(5, B.OLIVE, 'crop', (40, 34, 30), hw=72, sw=156, beard='stubble')]


def _arv(i, skin, hair_c, cap, jaw='square', hw=70, hh=90, sw=162, **kw):
    sp = dict(name=f'ARV{i}', skin=skin, hw=hw, hh=hh, jaw=jaw, hair='crop', hair_c=hair_c,
              brow_c=B.dk(hair_c, 0.85), outfit='jumper', jacket=ARV_TOP, trousers=ARMOUR, shoulders=sw,
              arv=True, cap=cap, mouth='set', brows='serious', holster=True, seed=60 + i, **kw)
    if cap == 'ct':                                   # counter-terror: balaclava and black gloves (ref armed-4)
        sp.update(balaclava=True, glove=(24, 24, 28), jacket=ARMOUR, sleeve=ARMOUR)
    return sp


# The armed officers (refs armed-1..4): black armour with pouches, the black POLICE patch, a yellow Taser at the
# front, a pistol low on the right thigh, SIG MCX carbines. Eight (Sam, 20 Oct): three in the flat chequered cap,
# three in the navy POLICE baseball cap, and the two who come down the ropes in black caps, balaclavas and gloves.
ARVS = [_arv(1, B.PALE, (90, 66, 44), 'peaked'), _arv(2, B.BROWN, (28, 22, 20), 'peaked', beard='trim', beard_c=(28, 22, 20)),
        _arv(3, B.PINK, (150, 110, 70), 'peaked', hw=66, sw=150, beard='full', beard_c=(170, 96, 50)),
        _arv(4, B.DEEP, (24, 20, 18), 'ball', hw=74, sw=170), _arv(5, B.OLIVE, (40, 32, 28), 'ball', beard='stubble'),
        _arv(6, B.PALE, (196, 150, 90), 'ball', hw=68, sw=156),
        _arv(7, B.PALE, (60, 46, 36), 'ct', hw=72), _arv(8, B.BROWN, (30, 24, 22), 'ct', jaw='soft', hw=66, sw=148)]
# Sam, 20 Oct: a real wall of police (four more in hi-vis) and more armed officers sweeping in from left and right
# to escort her (six more: flat caps and navy caps).
PCS += [_officer(6, B.PINK, 'crop', (60, 46, 36), hw=70, sw=154, beard='stubble'),
        _officer(7, B.PALE, 'bob', (150, 110, 70), jaw='soft', hw=64, hh=86, sw=136, lashes=True),
        _officer(8, B.BROWN, 'bald', (40, 32, 30), hw=72, sw=158),
        _officer(9, B.OLIVE, 'side', (40, 34, 30), hw=68, sw=150)]
ARVS += [_arv(9, B.PINK, (120, 90, 60), 'peaked', hw=70), _arv(10, B.DEEP, (24, 20, 18), 'ball', beard='trim',
                                                                beard_c=(24, 20, 18)),
         _arv(11, B.PALE, (196, 160, 110), 'ball', hw=66, sw=152), _arv(12, B.OLIVE, (40, 32, 28), 'peaked', beard='full',
                                                                       beard_c=(40, 32, 28)),
         _arv(13, B.BROWN, (28, 22, 20), 'ball', hw=72, sw=166), _arv(14, B.PALE, (90, 70, 50), 'peaked', beard='stubble')]
PEOPLE = {'GRAN': GRAN, 'SUPER': SUPER, 'JENKINS': JENKINS}
PEOPLE.update({p['name']: p for p in PCS + ARVS})
HEIGHTS = {'GRAN': 1.55, 'SUPER': 1.85, 'JENKINS': 1.86}
HEIGHTS.update({p['name']: h for p, h in zip(PCS, (1.80, 1.68, 1.88, 1.78, 1.83, 1.81, 1.70, 1.86, 1.79))})
HEIGHTS.update({p['name']: h for p, h in zip(ARVS, (1.84, 1.82, 1.78, 1.90, 1.80, 1.79, 1.85, 1.76, 1.83, 1.88, 1.77,
                                                    1.81, 1.89, 1.80))})

# ------------------------------------------------------------------------------------------------ the protesters
# Mostly elderly and middle-aged (Sam's brief): grey, white and thinning hair, sensible coats, fleeces and cardigans,
# a few keffiyehs; flags and FREE PALESTINE / CEASEFIRE NOW boards (Sam, 20 Oct: only she has the placard).
COATS = [(88, 96, 70), (120, 60, 50), (60, 70, 96), (150, 120, 86), (70, 64, 60), (96, 40, 56), (40, 74, 80),
         (176, 150, 110), (110, 100, 120), (54, 60, 50), (150, 70, 40), (84, 84, 92), (196, 180, 150), (36, 44, 66)]
HAIRS = [('wisps', (226, 226, 228)), ('bob', (210, 210, 214)), ('crop', (180, 178, 176)), ('bald', (200, 196, 192)),
         ('short', (150, 146, 144)), ('bob', (120, 90, 70)), ('side', (200, 200, 204)), ('crop', (60, 48, 40)),
         ('long', (196, 196, 200)), ('side', (90, 70, 56)), ('bald', (60, 50, 44)), ('bob', (236, 236, 236))]
SKINS = [B.PALE, B.PINK, B.OLIVE, B.BROWN, B.DEEP, B.PALE, B.PINK]


def protester(i):
    """Protester number i: their own build, face, hair, coat and what they carry (never a copy of the next one)."""
    rng = np.random.default_rng(1000 + i)
    hair, hc = HAIRS[rng.integers(len(HAIRS))]
    old = rng.random() < 0.65
    sp = dict(name=f'P{i}', skin=SKINS[rng.integers(len(SKINS))], hw=int(rng.integers(60, 76)),
              hh=int(rng.integers(80, 94)), jaw=['soft', 'round', 'square'][rng.integers(3)], hair=hair, hair_c=hc,
              brow_c=B.dk(hc, 0.8), outfit=['jumper', 'blouse', 'suit', 'dress'][rng.integers(4)],
              jacket=COATS[rng.integers(len(COATS))], shirt=[(236, 232, 226), (200, 210, 220), (226, 214, 190)][rng.integers(3)],
              trousers=[(50, 52, 60), (70, 60, 50), (40, 44, 56), (96, 90, 84)][rng.integers(4)],
              shoulders=int(rng.integers(124, 166)), age=old, mouth='line', seed=2000 + i)
    if sp['outfit'] == 'dress':
        sp['dress'] = sp['jacket']
    if rng.random() < 0.3:
        sp['keffiyeh'] = True
    if old and rng.random() < 0.35:
        sp['glasses'] = True
        sp['glasses_c'] = [(60, 50, 44), (150, 130, 80), (30, 28, 34)][rng.integers(3)]
    if not old and rng.random() < 0.3:
        sp['beard'] = ['trim', 'stubble', 'full'][rng.integers(3)]
        sp['beard_c'] = hc
    r = rng.random()
    sp['carry'] = 'flag' if r < 0.3 else ('board' if r < 0.5 else None)
    sp['board'] = ['FREE PALESTINE', 'CEASEFIRE NOW', 'FREE PALESTINE', 'STOP THE BOMBING'][rng.integers(4)]
    sp['height'] = float(rng.uniform(1.58, 1.86))
    return sp


# ------------------------------------------------------------------------------------------------ worn on the head
def chequer(p, x0, x1, y0, y1, rows=2, n=None):
    """The Sillitoe tartan band: black and white squares."""
    n = n or max(4, int(abs(x1 - x0) / max(1.0, (y1 - y0) / rows)))
    w, h = (x1 - x0) / n, (y1 - y0) / rows
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], (246, 246, 242), INK, 1.8)
    for r in range(rows):
        for c in range(n):
            if (r + c) % 2 == 0:
                p.poly([(x0 + c * w, y0 + r * h), (x0 + (c + 1) * w, y0 + r * h), (x0 + (c + 1) * w, y0 + (r + 1) * h),
                        (x0 + c * w, y0 + (r + 1) * h)], (24, 24, 28), None)
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], None, INK, 1.8)


def cap_badge(p, cx, cy, r, senior=False):
    """The cap badge: a silver crown over a round wreath (the senior cap's is larger)."""
    p.ell(cx, cy + r * 0.25, r * 0.62, r * 0.62, SILVER, INK, 1.4)
    p.ell(cx, cy + r * 0.25, r * 0.3, r * 0.3, (60, 70, 120) if not senior else (150, 30, 40), INK, 1.0)
    p.poly([(cx - r * 0.5, cy - r * 0.3), (cx - r * 0.55, cy - r * 0.95), (cx - r * 0.2, cy - r * 0.6), (cx, cy - r * 1.05),
            (cx + r * 0.2, cy - r * 0.6), (cx + r * 0.55, cy - r * 0.95), (cx + r * 0.5, cy - r * 0.3)], SILVER, INK, 1.4)


def peaked_cap(p, view, sp, hx, hy):
    """The Met's flat peaked cap (refs police-1..4, senior-3..5): a wide flat black top overhanging the band, the
    black-and-white chequered band (three rows on a senior's), a glossy black peak, the silver crowned badge; a
    senior's peak edged with a thick band of silver oak leaves."""
    hw, hh = sp.get('hw', 72), sp.get('hh', 90)
    senior = sp.get('braid')
    rows = 3 if senior else 2
    lift = hh * sp.get('cap_lift', 0.0)                 # worn a little higher (the senior officer: his brows must read)
    top, b0, b1 = hy - hh * 1.22 - lift, hy - hh * (0.86 if senior else 0.80) - lift, hy - hh * 0.58 - lift
    if view in ('front', 'three'):
        o = 0.0 if view == 'front' else 0.18 * hw
        crown = curve([(hx - hw * 0.98, b0 + 4), (hx - hw * 1.2, top + 18), (hx - hw * 0.7, top), (hx + o, top - 6),
                       (hx + hw * 0.7, top), (hx + hw * 1.2, top + 18), (hx + hw * 0.98, b0 + 4)], 3)
        p.poly(crown, CAP, INK, 2.4)
        p.line([(hx - hw * 0.98, top + 22), (hx + o, top + 14), (hx + hw * 0.98, top + 22)], CAP_D, 2.0)
        chequer(p, hx - hw * 0.99, hx + hw * 0.99, b0, b1, rows=rows, n=14)
        pk = [(hx - hw * 0.92 + o, b1 - 2), (hx + o, b1 + hh * 0.06), (hx + hw * 0.92 + o, b1 - 2),
              (hx + hw * 0.7 + o, b1 + hh * 0.2), (hx + o, b1 + hh * 0.27), (hx - hw * 0.7 + o, b1 + hh * 0.2)]
        p.poly(curve(pk, 3), CAP_D, INK, 2.2)
        p.line([(hx - hw * 0.5 + o, b1 + hh * 0.17), (hx + o, b1 + hh * 0.21)], (90, 90, 100), 2.0)   # the gloss
        if senior:                                          # the silver oak leaves along the peak
            for k in range(11):
                u = (k - 5) / 5.5
                x = hx + o + u * hw * 0.84
                y = b1 + hh * 0.04 + hh * 0.06 * (1 - u * u)
                p.ell(x, y, hw * 0.085, hh * 0.05, SILVER, INK, 1.0, rot=0.5 * (1 if k % 2 else -1))
        cap_badge(p, hx + o, (top + b0) / 2 + 6, hw * (0.3 if senior else 0.24), senior)
    elif view == 'side':
        crown = curve([(hx - hw * 1.02, b1), (hx - hw * 1.16, top + 12), (hx - hw * 0.4, top - 2), (hx + hw * 0.7, top + 2),
                       (hx + hw * 1.22, top + 16), (hx + hw * 0.98, b1)], 3)
        p.poly(crown, CAP, INK, 2.4)
        chequer(p, hx - hw * 1.0, hx + hw * 0.98, b0, b1, rows=rows, n=12)
        p.poly(curve([(hx + hw * 0.7, b1 - 4), (hx + hw * 1.5, b1 + hh * 0.12), (hx + hw * 1.46, b1 + hh * 0.2),
                      (hx + hw * 0.8, b1 + hh * 0.1)], 3), CAP_D, INK, 2.2)
        if senior:
            p.line([(hx + hw * 0.86, b1 + hh * 0.04), (hx + hw * 1.44, b1 + hh * 0.13)], SILVER, 5.0)
        cap_badge(p, hx + hw * 0.82, (top + b0) / 2 + 6, hw * 0.2, senior)
    else:
        crown = curve([(hx - hw * 0.98, b0 + 4), (hx - hw * 1.18, top + 18), (hx, top - 4), (hx + hw * 1.18, top + 18),
                       (hx + hw * 0.98, b0 + 4)], 3)
        p.poly(crown, CAP, INK, 2.4)
        chequer(p, hx - hw * 0.99, hx + hw * 0.99, b0, b1, rows=rows, n=14)


def ball_cap(p, view, sp, hx, hy):
    """An armed officer's baseball cap (refs armed-3..4): navy with the chequered band and POLICE across the front;
    the counter-terror team's ('ct') is black with the chequer on the side only."""
    hw, hh = sp.get('hw', 72), sp.get('hh', 90)
    ct = sp.get('cap') == 'ct'
    col, col_d = ((22, 22, 26), (12, 12, 14)) if ct else ((34, 44, 80), (22, 28, 54))
    top, b0, b1 = hy - hh * 1.12, hy - hh * 0.72, hy - hh * 0.56
    if view == 'side':
        p.poly(curve([(hx - hw * 1.02, b1), (hx - hw * 0.96, hy - hh * 0.95), (hx - hw * 0.2, top), (hx + hw * 0.7, hy - hh * 0.98),
                      (hx + hw * 1.0, b1)], 3), col, INK, 2.4)
        chequer(p, hx - hw * 0.7, hx + hw * 0.2, b0 - hh * 0.1, b1 - hh * 0.04, n=7) if ct else \
            chequer(p, hx - hw * 1.0, hx + hw * 0.98, b0, b1, n=12)
        p.poly(curve([(hx + hw * 0.8, b1 - 4), (hx + hw * 1.62, b1 + 6), (hx + hw * 1.56, b1 + 14),
                      (hx + hw * 0.86, b1 + 8)], 3), col_d, INK, 2.2)
        return
    o = 0.0 if view in ('front', 'back') else (0.2 * hw if view == 'three' else -0.2 * hw)
    p.poly(curve([(hx - hw * 1.0, b1), (hx - hw * 0.94, hy - hh * 0.9), (hx - hw * 0.5 + o, top + 6), (hx + o, top),
                  (hx + hw * 0.5 + o, top + 6), (hx + hw * 0.94, hy - hh * 0.9), (hx + hw * 1.0, b1)], 3), col, INK, 2.4)
    p.line([(hx + o, top + 4), (hx + o * 1.4, b0 - 2)], col_d, 1.8)
    if ct:
        if view != 'front':
            sg = -1 if view == 'three' else 1
            chequer(p, hx + sg * hw * 0.92, hx + sg * hw * 0.5, b0 - hh * 0.12, b1 - hh * 0.04, n=4)
    else:
        chequer(p, hx - hw * 1.0, hx + hw * 1.0, b0, b1, n=14)
        if view in ('front', 'three'):
            _text(p, hx + o, (top + b0) / 2 + 8, hw * 1.1, hh * 0.2, 'POLICE', (246, 246, 242))
    if view in ('front', 'three'):
        p.poly(curve([(hx - hw * 0.8 + o, b1 - 2), (hx + o * 1.5, b1 + 4), (hx + hw * 0.8 + o * 2, b1 - 2),
                      (hx + hw * 0.66 + o * 2, b1 + hh * 0.18), (hx + o * 1.5, b1 + hh * 0.24),
                      (hx - hw * 0.66 + o, b1 + hh * 0.18)], 3), col_d, INK, 2.2)


def balaclava(p, view, sp, hx, hy):
    """The counter-terror balaclava (ref armed-4): black over the whole head and neck, the eyes left clear."""
    hw, hh = sp.get('hw', 72), sp.get('hh', 90)
    col = (22, 22, 26)
    if view in ('back', 'three_back'):
        p.poly(curve([(hx - hw * 1.02, hy - hh * 0.5), (hx, hy - hh * 1.04), (hx + hw * 1.02, hy - hh * 0.5),
                      (hx + hw * 0.9, hy + hh * 0.9), (hx + 40, 0), (hx - 40, 0), (hx - hw * 0.9, hy + hh * 0.9)], 3), col, INK, 2.4)
        return
    if view == 'side':
        ex, ey = hx + 42, hy - 10
        p.poly(curve([(hx - hw * 0.98, hy - hh * 0.5), (hx, hy - hh * 1.02), (hx + hw * 0.9, hy - hh * 0.6),
                      (ex + 24, ey - 16), (ex - 14, ey - 16), (ex - 16, ey + 12), (ex + 30, ey + 14), (hx + hw * 1.04, hy + 20),
                      (hx + hw * 0.9, hy + hh * 0.9), (40, 0), (-40, 0), (hx - hw * 0.9, hy + hh * 0.6)], 3), col, INK, 2.4)
        return
    fx = hx + (0.4 * hw if view == 'three' else 0.0)
    out = [(hx - hw * 1.02, hy + 6), (hx - hw * 1.0, hy - hh * 0.5), (hx, hy - hh * 1.04), (hx + hw * 1.0, hy - hh * 0.5),
           (hx + hw * 1.02, hy + 6), (hx + hw * 0.92, hy + hh * 0.8), (hx + 46, 4), (hx - 46, 4),
           (hx - hw * 0.92, hy + hh * 0.8)]
    p.poly(curve(out, 3), col, INK, 2.4)
    # the eye slot: skin, with the eyes drawn back in (open, looking where the face looks)
    slot = [(fx - 58, hy - 26), (fx + 54, hy - 26), (fx + 56, hy + 10), (fx - 60, hy + 10)]
    p.poly(rough(slot, 3, 9), sp['skin'], INK, 2.0)
    look = sp.get('look', 0.0)
    for ex, w in (((fx - 34, 1.0), (fx + 26, 1.0)) if view == 'front' else ((fx - 26, 1.0), (fx + 24, 0.62))):
        ey = hy - 8
        p.poly([(ex - 17 * w, ey), (ex - 8 * w, ey - 8), (ex + 8 * w, ey - 8), (ex + 17 * w, ey), (ex + 8 * w, ey + 7),
                (ex - 8 * w, ey + 7)], (250, 250, 248), INK, 2.0)
        p.ell(ex + look * 7 * w, ey, 5 * w, 5, INK, None)
        p.line([(ex - 16 * w, ey - 16), (ex + 18 * w, ey - 19)], sp.get('brow_c', (40, 30, 26)), 4.0)


def curls(p, view, sp, hx, hy):
    """Her curly white hair (Cry Minister): a cloud of small curls round the crown, one shape with one outline (each
    curl inked first, then every fill laid over, so only the outer edge keeps its line)."""
    hw, hh = sp.get('hw', 62), sp.get('hh', 80)
    rng = np.random.default_rng(4)
    a0, a1, cx = {'front': (0.95, 2.05, 0.0), 'three': (0.9, 2.02, -0.12), 'side': (0.7, 2.0, -0.2),
                  'three_back': (0.6, 2.4, 0.0), 'back': (0.55, 2.45, 0.0)}[view]
    blobs = []
    for _ in range(40 if view in ('back', 'three_back') else 34):
        a = rng.uniform(math.pi * a0, math.pi * a1)
        r = rng.uniform(0.9, 1.18)
        blobs.append((hx + hw * cx + hw * 1.02 * r * math.cos(a), hy - hh * 0.25 + hh * 0.95 * r * math.sin(a)))
    if view in ('back', 'three_back'):                         # from behind the curls cover the whole back of the head
        for _ in range(26):
            blobs.append((hx + rng.uniform(-0.75, 0.75) * hw, hy + rng.uniform(-0.9, 0.35) * hh))
    for x, y in blobs:
        p.ell(x, y, 15, 13, (246, 244, 240), INK, 2.2)
    for x, y in blobs:
        p.ell(x, y, 13.6, 11.6, (246, 244, 240), None)
    for x, y in blobs[::3]:                                    # a few inner swirls
        p.line(oval(x, y, 6, 5, 8, 0.4, 3.6), (206, 204, 210), 1.4)


def striped_glasses(p, view, sp, hx, hy):
    """Her big white-and-pink striped glasses (Cry Minister)."""
    if view in ('back', 'three_back'):
        return
    if view == 'side':
        ex, ey = hx + 42, hy - 10
        p.ell(ex + 4, ey, 16, 22, None, (250, 250, 250), 7)
        p.ell(ex + 4, ey, 19, 25, None, INK, 1.6)
        p.line([(ex - 12, ey - 8), (hx - 18, hy - 6)], (236, 120, 170), 4)
        return
    fx = hx + (0.4 * sp.get('hw', 62) if view == 'three' else 0.0)
    lenses = ((fx - 34, 1.0), (fx + 26, 1.0)) if view == 'front' else ((fx - 26, 1.0), (fx + 24, 0.62))
    for ex, w in lenses:
        ey = hy - 6
        p.ell(ex, ey, 30 * w, 26, None, (250, 250, 250), 9)
        for j in range(8):
            a = j * math.pi / 4
            p.line([(ex + 30 * w * math.cos(a), ey + 26 * math.sin(a)),
                    (ex + 30 * w * math.cos(a + 0.35), ey + 26 * math.sin(a + 0.35))], (236, 120, 170), 9)
        p.ell(ex, ey, 34 * w, 30, None, INK, 1.6)
    p.line([(lenses[0][0] + 26, hy - 10), ((lenses[0][0] + lenses[1][0]) / 2, hy - 14),
            (lenses[1][0] - 26 * lenses[1][1], hy - 10)], (236, 120, 170), 5)


LENS, LENS_L, FRAME = (70, 104, 140), (176, 206, 228), (200, 186, 120)


def _lens(p, ex, ey, w, sgn):
    """One aviator lens, teardrop, the outer corner dropping lower; a flat mirror sheen across it."""
    pts = curve([(ex - sgn * 16 * w, ey - 10), (ex + sgn * 19 * w, ey - 11), (ex + sgn * 21 * w, ey + 4),
                 (ex + sgn * 10 * w, ey + 15), (ex - sgn * 6 * w, ey + 13), (ex - sgn * 17 * w, ey + 2)], 3)
    p.poly(pts, LENS, INK, 2.2)
    p.poly([(ex - sgn * 9 * w, ey - 6), (ex - sgn * 2 * w, ey - 7), (ex + sgn * 10 * w, ey + 9), (ex + sgn * 3 * w, ey + 10)],
           LENS_L, None)


def aviators(p, view, sp, hx, hy):
    """The senior officer's mirrored aviators: gold wire frame, blue mirrored teardrop lenses; the brows stay clear."""
    if view in ('back', 'three_back'):
        return
    hw = sp.get('hw', 72)
    if view == 'side':
        ex, ey = hx + 42, hy - 10
        _lens(p, ex + 6, ey + 2, 0.7, 1)
        p.line([(ex - 8, ey - 8), (hx - 12, hy - 6)], FRAME, 3.0)
        return
    if view == 'front':
        fx = hx + sp.get('turn', 0.0) * hw * 0.22
        ls = ((fx - 34, 1.0, -1), (fx + 26, 1.0, 1))
    else:
        fx = hx + 0.4 * hw
        ls = ((fx - 26, 1.0, -1), (fx + 24, 0.62, 1))
    for ex, w, sgn in ls:
        _lens(p, ex, hy - 6, w, sgn)
    p.line([(ls[0][0] + 16, hy - 15), ((ls[0][0] + ls[1][0]) / 2, hy - 17), (ls[1][0] - 16 * ls[1][1], hy - 15)], FRAME, 3.0)
    if view == 'front':
        for ex, w, sgn in ls:
            p.line([(ex + sgn * 20, hy - 13), (hx + sgn * (hw - 2), hy - 12)], FRAME, 2.6)
    else:
        p.line([(ls[0][0] - 18, hy - 13), (hx - hw * 0.62, hy - 10)], FRAME, 2.6)


HATS = {'peaked': peaked_cap, 'ball': ball_cap, 'ct': ball_cap}


# ------------------------------------------------------------------------------------------------ worn on the body
def _torso_box(view, sp, y=150.0):
    """(left, right) edges of the torso at height y for a view, facing right: full width down to the waist (200),
    then narrowing to the hem (burnham.HEM: Sam, 20 Oct, hips 15% narrower)."""
    sw = sp.get('shoulders', 150)
    l, r = {'front': (-sw, sw), 'three': (-sw * 0.95, sw * 0.82), 'side': (-0.6 * sw, 0.66 * sw),
            'three_back': (-sw * 0.9, sw * 0.9), 'back': (-sw, sw)}[view]
    if view != 'side' and y > 200:
        bottom = sp.get('bottom', V.JACKET)
        u = min(1.0, (y - 200) / max(1.0, bottom - 200))
        k = 1 - (1 - B.HEM) * u
        l, r = l * k, r * k
    return l, r


_GLYPH = {}


def _text(p, cx, cy, w, h, text, col, font=BLOCK):
    """Block lettering fitted to a box (w x h, person units), drawn once large and scaled, so it never pulses; it
    always reads forwards, even on a mirrored person."""
    key = (text, col, font)
    if key not in _GLYPH:
        f = ImageFont.truetype(font, 160)
        l, t_, r, b = f.getbbox(text)
        im = Image.new('RGBA', (r - l + 12, b - t_ + 12), col + (0,))
        ImageDraw.Draw(im).text((6 - l, 6 - t_), text, font=f, fill=col + (255,))
        _GLYPH[key] = im
    im = _GLYPH[key]
    k = min(w / im.width, h / im.height)
    ww, hh = im.width * k, im.height * k
    a = p.cam.P(cx - ww / 2, cy - hh / 2)
    b = p.cam.P(cx + ww / 2, cy + hh / 2)
    x0, x1 = sorted((a[0], b[0]))
    y0, y1 = sorted((a[1], b[1]))
    if x1 - x0 < 2 or y1 - y0 < 2:
        return
    small = im.resize((max(1, int(round(x1 - x0))), max(1, int(round(y1 - y0)))), Image.LANCZOS)
    p.img.alpha_composite(small, (int(round(x0)), int(round(y0)))) if x0 >= 0 and y0 >= 0 else \
        p.img.paste(small, (int(x0), int(y0)), small)


def _patch(p, cx, cy, w, h, text, fill, ink):
    p.poly([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)],
           fill, INK, 1.6)
    _text(p, cx, cy, w * 0.84, h * 0.66, text, ink)


def body_cam(p, cx, cy):
    """A body-worn camera clipped to the chest: a small black box with a round lens."""
    p.poly([(cx - 18, cy - 24), (cx + 18, cy - 24), (cx + 18, cy + 24), (cx - 18, cy + 24)], (30, 30, 34), INK, 1.6)
    p.ell(cx, cy - 6, 8, 8, (70, 80, 100), INK, 1.2)


def hivis(p, view, sp):
    """The hi-vis jacket (refs police-1..4): yellow; silver bands over the shoulders like braces and round the body;
    the blue-and-white chequered band near the hem; white POLICE on a blue chest patch; black collar; body camera
    centre chest; radio high on the shoulder."""
    bottom = sp.get('bottom', V.JACKET)
    y0 = bottom - 70                                            # the chequered band near the hem
    l, r = _torso_box(view, sp, y0 + 44)
    n = 12
    w = (r - l - 8) / n
    for k in range(n):
        p.poly([(l + 4 + k * w, y0), (l + 4 + (k + 1) * w, y0), (l + 4 + (k + 1) * w, y0 + 22), (l + 4 + k * w, y0 + 22)],
               POLICE_BLUE if k % 2 == 0 else (246, 246, 242), None)
        p.poly([(l + 4 + k * w, y0 + 22), (l + 4 + (k + 1) * w, y0 + 22), (l + 4 + (k + 1) * w, y0 + 44),
                (l + 4 + k * w, y0 + 44)], (246, 246, 242) if k % 2 == 0 else POLICE_BLUE, None)
    p.poly([(l + 4, y0), (r - 4, y0), (r - 4, y0 + 44), (l + 4, y0 + 44)], None, INK, 1.6)
    bl, br_ = _torso_box(view, sp, 326)
    p.poly([(bl + 4, 300), (br_ - 4, 300), (br_ - 6, 326), (bl + 6, 326)], SILVER, INK, 1.6)   # the band round the body
    l, r = _torso_box(view, sp)
    if view in ('front', 'three', 'back', 'three_back'):
        for x in ((l + r) / 2 - (r - l) * 0.24, (l + r) / 2 + (r - l) * 0.24):              # the braces over the shoulders
            p.poly([(x - 13, 0), (x + 13, 0), (x + 13, 300), (x - 13, 300)], SILVER, INK, 1.6)
    if view in ('front', 'three'):
        o = 0 if view == 'front' else 0.32 * sp.get('shoulders', 150)
        p.poly([(o - 40, -6), (o + 40, -6), (o + 30, 24), (o - 30, 24)], (24, 24, 28), INK, 1.8)   # black collar
        p.line([(o, 24), (o + 2, bottom)], HIVIS_D, 2.2)                                       # the zip
        _patch(p, o + (r - l) * 0.26, 170, 84, 30, 'POLICE', POLICE_BLUE, (246, 246, 242))
        body_cam(p, o - 2, 200)
        p.poly([(l + 30, 20), (l + 56, 20), (l + 56, 76), (l + 30, 76)], (50, 50, 56), INK, 1.4)  # radio on the shoulder
    elif view in ('back', 'three_back'):
        _patch(p, (l + r) / 2, 180, (r - l) * 0.6, 60, 'POLICE', POLICE_BLUE, (246, 246, 242))


def steward_vest(p, view, sp):
    """A protest steward's orange hi-vis vest (refs crowd-low-1..3): orange, two silver bands."""
    l, r = _torso_box(view, sp)
    l2, r2 = _torso_box(view, sp, 440)
    p.poly([(l + 16, 10), (r - 16, 10), (r - 6, 200), (r2 - 6, 440), (l2 + 6, 440), (l + 6, 200)], (244, 124, 34), INK, 1.8)
    for y in (270, 360):
        a, b = _torso_box(view, sp, y + 20)
        p.poly([(a + 8, y), (b - 8, y), (b - 8, y + 22), (a + 8, y + 22)], SILVER, INK, 1.2)


def armour(p, view, sp):
    """The armed officer's black plate carrier (refs armed-1..4): pouches, the black POLICE patch with white letters,
    radio, body camera, a small Union flag patch, the yellow Taser in its holster at the front."""
    l, r = _torso_box(view, sp)
    l2, r2 = _torso_box(view, sp, 470)
    p.poly(rough([(l + 14, 36), (r - 14, 36), (r - 4, 120), (r - 4, 200), (r2 - 6, 470), (l2 + 6, 470), (l + 4, 200),
                  (l + 4, 120)], 3, 5), ARMOUR, INK, 2.4)
    if view in ('front', 'three'):
        o = 0 if view == 'front' else 0.3 * sp.get('shoulders', 150)
        p.poly([(l + 30, -2), (l + 80, -2), (l + 70, 60), (l + 30, 60)], ARMOUR, INK, 2.0)        # shoulder straps
        p.poly([(r - 80, -2), (r - 30, -2), (r - 30, 60), (r - 70, 60)], ARMOUR, INK, 2.0)
        for k in range(3):                                                                     # magazine pouches
            x = l + 34 + k * (r - l - 68) / 3
            p.poly([(x, 330), (x + (r - l - 90) / 3, 330), (x + (r - l - 90) / 3, 440), (x, 440)], ARMOUR_D, INK, 1.6)
        _patch(p, o, 120, (r - l) * 0.42, 40, 'POLICE', ARMOUR_D, (246, 246, 242))
        body_cam(p, o - (r - l) * 0.2, 210)
        p.poly([(r - 74, 74), (r - 44, 74), (r - 44, 150), (r - 74, 150)], (50, 50, 56), INK, 1.4)   # radio
        p.poly([(l + 40, 176), (l + 80, 176), (l + 80, 202), (l + 40, 202)], (40, 60, 130), INK, 1.2)   # the flag patch
        p.line([(l + 40, 189), (l + 80, 189)], (200, 40, 50), 2.6)
        p.line([(l + 60, 176), (l + 60, 202)], (200, 40, 50), 2.6)
        p.poly([(o + 26, 236), (o + 70, 236), (o + 70, 300), (o + 26, 300)], ARMOUR_D, INK, 1.6)       # the Taser
        p.poly([(o + 32, 230), (o + 64, 230), (o + 64, 262), (o + 40, 262), (o + 40, 290), (o + 32, 290)],
               (238, 200, 30), INK, 1.4)
    elif view in ('back', 'three_back'):
        _patch(p, (l + r) / 2, 170, (r - l) * 0.62, 56, 'POLICE', ARMOUR_D, (246, 246, 242))
    else:
        p.poly([(r - 50, 330), (r + 6, 330), (r + 6, 440), (r - 50, 440)], ARMOUR_D, INK, 1.6)


def stab_vest(p, view, sp):
    """Jenkins's black stab vest over his black top: POLICE patch, a radio clipped high on the chest."""
    l, r = _torso_box(view, sp)
    l2, r2 = _torso_box(view, sp, 450)
    p.poly(rough([(l + 20, 30), (r - 20, 30), (r - 8, 110), (r - 8, 200), (r2 - 10, 450), (l2 + 10, 450), (l + 8, 200),
                  (l + 8, 110)], 3, 7), (20, 21, 26), INK, 2.2)
    if view in ('front', 'three'):
        _patch(p, (l + r) / 2, 220, (r - l) * 0.46, 36, 'POLICE', (246, 246, 242), INK)
        p.poly([(l + 40, 80), (l + 74, 80), (l + 74, 150), (l + 40, 150)], (56, 56, 62), INK, 1.4)
        p.line([(l + 50, 80), (l + 50, 50)], INK, 3.0)
        body_cam(p, (l + r) / 2 + 30, 140)
    elif view in ('back', 'three_back'):
        _patch(p, 0, 200, (r - l) * 0.6, 50, 'POLICE', (246, 246, 242), INK)


def shoulder_board(p, x0, x1, y0, y1, sg):
    """A senior officer's black shoulder board, pointed at the collar end: a silver crown and a pip (Chief Supt)."""
    p.poly([(x0, y0 + 6), (x1, y0), (x1, y1), (x0, y1 - 4), (x0 - sg * 18, (y0 + y1) / 2)], (22, 22, 26), INK, 1.6)
    cx = x0 + (x1 - x0) * 0.62
    cy = (y0 + y1) / 2
    cap_badge(p, cx, cy, 12, True)
    p.poly([(x0 + (x1 - x0) * 0.28 - 7, cy), (x0 + (x1 - x0) * 0.28, cy - 8), (x0 + (x1 - x0) * 0.28 + 7, cy),
            (x0 + (x1 - x0) * 0.28, cy + 8)], SILVER, INK, 1.0)


def white_shirt(p, view, sp):
    """The senior officer's white shirt (refs senior-1..5): pointed collar, plain black tie, two chest pockets with
    buttoned flaps, black shoulder boards (crown and pip), a small black name badge over the right pocket."""
    l, r = _torso_box(view, sp)
    if view == 'front':
        p.poly([(-11, 16), (11, 16), (15, 210), (0, 236), (-15, 210)], (24, 24, 28), INK, 2.0)
        p.poly([(-12, -2), (12, -2), (9, 18), (-9, 18)], (24, 24, 28), INK, 2.0)
        for sg in (-1, 1):
            p.poly([(sg * 10, -8), (sg * 50, -8), (sg * 30, 34)], WHITE_SHIRT, INK, 1.8)            # collar points
            p.poly([(sg * 54, 128), (sg * 118, 128), (sg * 116, 206), (sg * 56, 206)], WHITE_SHIRT, INK, 1.6)
            p.poly([(sg * 52, 124), (sg * 120, 124), (sg * 120, 150), (sg * 86, 158), (sg * 52, 150)], WHITE_SHIRT, INK, 1.6)
            p.ell(sg * 86, 148, 4, 4, (220, 220, 216), INK, 1.0)
            shoulder_board(p, sg * 50, sg * (r - 6), 8, 46, sg)
        p.poly([(-118, 96), (-58, 96), (-58, 116), (-118, 116)], (22, 22, 26), INK, 1.2)            # name badge
        _text(p, -88, 106, 54, 12, 'CHIEF SUPERINTENDENT', (246, 246, 242))
        p.line([(0, 236), (0, 500)], (214, 214, 210), 1.6)
    elif view == 'three':
        o = 0.32 * sp.get('shoulders', 150)
        p.poly([(o - 8, 16), (o + 10, 16), (o + 13, 206), (o + 2, 230), (o - 10, 206)], (24, 24, 28), INK, 2.0)
        p.poly([(o - 28, -8), (o + 4, -8), (o - 10, 30)], WHITE_SHIRT, INK, 1.8)
        p.poly([(o - 30, 128), (o - 84, 128), (o - 84, 200), (o - 30, 200)], WHITE_SHIRT, INK, 1.6)
        p.poly([(o + 30, 128), (o + 70, 128), (o + 70, 196), (o + 30, 196)], WHITE_SHIRT, INK, 1.6)
        shoulder_board(p, o + 40, r - 4, 8, 44, 1)
        shoulder_board(p, o - 40, l + 10, 8, 44, -1)
    elif view == 'side':
        d = 0.6 * sp.get('shoulders', 150)
        p.poly([(30, 10), (42, 12), (d * 0.9, 206), (d * 0.8, 202)], (24, 24, 28), INK, 1.8)
        shoulder_board(p, -30, 34, 0, 30, 1)
    else:
        for sg in (-1, 1):
            shoulder_board(p, sg * 46, sg * (r - 8), 8, 46, sg)


def keffiyeh(p, view, sp):
    """A black-and-white keffiyeh round the neck: a fringed scarf with the fishnet pattern."""
    if view in ('back', 'three_back'):
        p.poly(curve([(-56, -10), (56, -10), (60, 40), (-60, 40)], 2), (240, 240, 236), INK, 2.0)
        return
    o = 0.0 if view == 'front' else (0.32 * sp.get('shoulders', 150) if view == 'three' else 30.0)
    p.poly(curve([(o - 62, -10), (o + 62, -10), (o + 54, 40), (o, 64), (o - 54, 40)], 3), (240, 240, 236), INK, 2.0)
    p.poly([(o - 34, 40), (o - 4, 40), (o - 8, 190), (o - 36, 190)], (240, 240, 236), INK, 1.8)
    for k in range(6):
        y = 50 + k * 22
        p.line([(o - 34, y), (o - 6, y + 10)], INK, 1.4)
        p.line([(o - 34, y + 10), (o - 6, y)], INK, 1.4)
    for k in range(5):
        p.line([(o - 34 + k * 7, 190), (o - 34 + k * 7, 204)], INK, 1.4)


def trim(p, view, sp):
    """Her frock's black trim at the neckline and the hem (Cry Minister)."""
    bottom = sp.get('bottom', 600)
    if view == 'front':
        p.line([(-46, -4), (0, 70), (46, -4)], INK, 7)
    l, r = _torso_box(view, sp, bottom - 6)
    p.line([(l + 4, bottom - 6), (r - 4, bottom - 6)], INK, 9)


def holster(p, j2):
    """The pistol in its drop-leg holster, strapped low on the right thigh (ref armed-2): front and back views only
    (from the side the leg nearest us is the left)."""
    if j2.get('yaw') not in (0, 180):
        return
    h, f = j2['hipR'], j2['footR']
    a = (h[0] + (f[0] - h[0]) * 0.18, h[1] + (f[1] - h[1]) * 0.18)
    b = (h[0] + (f[0] - h[0]) * 0.42, h[1] + (f[1] - h[1]) * 0.42)
    sg = 1 if j2.get('yaw') == 0 else -1
    x = sg * 46
    p.poly([(a[0] + x - 22, a[1]), (a[0] + x + 22, a[1]), (b[0] + x + 20, b[1]), (b[0] + x - 18, b[1])], ARMOUR, INK, 1.8)
    for u in (0.4, 0.8):
        y = a[1] + (b[1] - a[1]) * u
        p.line([(a[0] - 40, y), (a[0] + x + 24, y)], ARMOUR_D, 4.0)


def dress(sp):
    """The film's clothing and headwear for one person, as views' body_props and head_props."""
    body, head = [], []
    for k, fn in (('hivis', hivis), ('arv', armour), ('stab_vest', stab_vest), ('white_shirt', white_shirt),
                  ('keffiyeh', keffiyeh), ('trim', trim), ('steward', steward_vest)):
        if sp.get(k):
            body.append(fn)
    for k, fn in (('curls', curls), ('striped_glasses', striped_glasses), ('aviators', aviators),
                  ('balaclava', balaclava)):
        if sp.get(k):
            head.append(fn)
    if sp.get('cap'):
        head.append(HATS[sp['cap']])
    return body, head


def outfit(j, sp):
    j['body_props'], j['head_props'] = dress(sp)
    if sp.get('holster'):
        j.setdefault('props', []).insert(0, holster)
    return j


def pose_standing(sp):
    return outfit(V.standing(sp), sp)


def person(img, cam, x, y, s, sp, t=0.0, yaw=0, j=None, head_yaw=None):
    j = j or pose_standing(sp)
    if 'body_props' not in j:
        outfit(j, sp)
    return V.person(img, cam, x, y, s, dict(sp, full=True, pose='custom'), t, yaw, j, head_yaw)


# ------------------------------------------------------------------------------------------------ the placard
PLACARD_W, PLACARD_H = 0.45, 0.6     # metres (sizes: 'protest placard'; refs placard-1..2)
LETTERED = 0.58                      # the top 58% is lettered; below it, plain card that is always hidden


def placard_image(px=450, lettered=True):
    """Her placard (refs placard-1..2): white card, black marker capitals in uneven hand lettering, I OPPOSE /
    GENOCIDE / I SUPPORT filling the top three-fifths. The rest is plain card, never lettered (Sam, 20 Oct)."""
    w, h = px, int(px * PLACARD_H / PLACARD_W)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(7)
    edge = [(4 + rng.uniform(-2, 2), 4 + rng.uniform(-2, 2)), (w - 4 + rng.uniform(-2, 2), 3 + rng.uniform(-2, 2)),
            (w - 3 + rng.uniform(-2, 2), h - 4 + rng.uniform(-2, 2)), (4 + rng.uniform(-2, 2), h - 3 + rng.uniform(-2, 2))]
    d.polygon(edge, fill=(248, 247, 242, 255))
    if lettered:
        f = ImageFont.truetype(FONT, int(h * 0.15))
        for txt, y in (('I OPPOSE', 0.035), ('GENOCIDE', 0.215), ('I SUPPORT', 0.395)):
            l, t_, r, b = d.textbbox((0, 0), txt, font=f)
            k = min(1.0, w * 0.92 / (r - l))                  # each line fills the width, as on the real ones
            line = Image.new('RGBA', (r - l + 8, b - t_ + 8), (0, 0, 0, 0))
            ImageDraw.Draw(line).text((4 - l, 4 - t_), txt, font=f, fill=MARKER + (255,))
            line = line.resize((int(line.width * k * 1.0), int(line.height)), Image.LANCZOS)
            line = line.rotate(rng.uniform(-2.5, 2.5), resample=Image.BICUBIC, expand=True)
            im.alpha_composite(line, (int((w - line.width) / 2 + rng.uniform(-6, 6)), int(h * y)))
    d.line(edge + [edge[0]], fill=(60, 56, 52, 255), width=max(2, px // 150))
    return im


_PLACARD = {}
HIDDEN_TEST = [False]   # the check paints the never-seen part magenta, renders the frame and counts what shows


def _placard_im():
    key = 'test' if HIDDEN_TEST[0] else 'im'
    if key not in _PLACARD:
        im = placard_image()
        if HIDDEN_TEST[0]:
            d = ImageDraw.Draw(im)
            d.rectangle([0, int(im.height * LETTERED), im.width, im.height], fill=(255, 0, 255, 255))
        _PLACARD[key] = im
    return _PLACARD[key]


def placard_prop(quad, skin=None):
    """Her placard: `quad` = its corners TL, TR, BR, BL in her own units; laid into the frame through her own drawing
    frame (so it turns and moves with her), reading forwards even when she faces left. The card is in front of her
    arms (Sam, 20 Oct: its top corners cut into her shoulders when the arms were drawn over it): only her hands show,
    gripping its edges, drawn over it here."""
    def hands(p, j2):
        if skin is None or j2.get('yaw', 0) > 90:
            return
        for sd in 'LR':
            el, wr = j2['el' + sd], j2['wr' + sd]
            B.gesture_hand(p, el, wr, 'fist', skin)

    def draw(p, j2):
        import poker_mon_cast as PC
        yaw = j2.get('yaw', 0)
        c = math.cos(math.radians(yaw))
        q = [(x * max(0.12, abs(c)), y) for x, y in quad]          # it faces the way she faces
        if c < 0.05:                                                 # from behind: the plain back of the card, seen
            if max(y for _, y in q) < -150:                          # only when it is up over her head (lower, her
                p.poly(q, (236, 234, 226), INK, 2.0)                 # body hides it)
            return
        q = q if getattr(p.cam, 'flip', 1) == 1 else [q[1], q[0], q[3], q[2]]
        PC.place_image(p.img, p.cam, _placard_im(), q)
        hands(p, j2)
    return draw


def placard_pose(sp, t=0.0, raise_u=1.0, tremble=1.0, seed=0):
    """Her placard in both hands at its bottom corners (refs placard-1..2), raised from her chest (raise_u 0) to above
    her head (1), trembling (the script says so: a quick small judder, never a slow sway). Returns the pose and the
    placard's corners in her own units."""
    j = pose_standing(sp)
    jy = 5 * (math.sin(t * 41 + seed) + 0.6 * math.sin(t * 67 + 1.3 + seed)) * tremble
    jx = 3 * math.sin(t * 53 + 0.7 + seed) * tremble
    W_, H_ = PLACARD_W / V.M_PER_UNIT, PLACARD_H / V.M_PER_UNIT
    bottom = 330 + (-265 - 330) * raise_u + jy                  # the card's bottom edge: at her waist, or over her head
    z = 110 - 40 * raise_u
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, (sg * (W_ / 2 - 26) + jx, bottom - 26, z), 'out', 'fist')
    quad = [(-W_ / 2 + jx, bottom - H_), (W_ / 2 + jx, bottom - H_ + 2), (W_ / 2 + jx, bottom), (-W_ / 2 + jx, bottom)]
    j['props'] = j.get('props', []) + [placard_prop(quad, sp['skin'])]
    return j, quad


def board_image(text, px=420, seed=0):
    """A protester's board: white card, hand-lettered in red, black or green."""
    rng = np.random.default_rng(seed)
    w, h = px, int(px * 0.62)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(4, 4), (w - 4, 6), (w - 6, h - 4), (6, h - 6)], fill=(246, 244, 236, 255))
    f = ImageFont.truetype(FONT, int(h * 0.36))
    col = [(196, 30, 40), (24, 22, 26), (20, 110, 60)][int(rng.integers(3))]
    words = text.split()
    lines = [' '.join(words[:len(words) // 2 or 1]), ' '.join(words[len(words) // 2 or 1:])] if len(words) > 1 else words
    for k, ln in enumerate(lines):
        l, t_, r, b = d.textbbox((0, 0), ln, font=f)
        line = Image.new('RGBA', (r - l + 8, b - t_ + 8), (0, 0, 0, 0))
        ImageDraw.Draw(line).text((4 - l, 4 - t_), ln, font=f, fill=col + (255,))
        kx = min(1.0, w * 0.9 / line.width)
        line = line.resize((max(1, int(line.width * kx)), line.height), Image.LANCZOS)
        im.alpha_composite(line, (int((w - line.width) / 2), int(h * (0.06 + 0.44 * k))))
    d.line([(4, 4), (w - 4, 6), (w - 6, h - 4), (6, h - 6), (4, 4)], fill=(40, 30, 24, 255), width=3)
    return im


def flag_image(px=360):
    """The Palestinian flag: black, white, green bands; a red triangle at the hoist."""
    w, h = px, int(px * 2 / 3)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k, c in enumerate(PAL_FLAG[:3]):
        d.rectangle([0, k * h / 3, w, (k + 1) * h / 3], fill=c + (255,))
    d.polygon([(0, 0), (w * 0.4, h / 2), (0, h)], fill=PAL_FLAG[3] + (255,))
    d.rectangle([0, 0, w - 1, h - 1], outline=(24, 22, 26, 255), width=3)
    return im


_IMAGES = {}


def flag_prop(t=0.0, seed=0, wave=1.0):
    """A hand flag on a pole, held up in the right hand and waved: the cloth ripples (four bands, each its own small
    lag) and swings with the pole."""
    def draw(p, j2):
        if 'flag' not in _IMAGES:
            _IMAGES['flag'] = flag_image()
        import poker_mon_cast as PC
        hx, hy = j2['wrR']
        ang = math.radians(-8 + 14 * math.sin(t * 5.2 + seed) * wave)
        pole = 1.2 / V.M_PER_UNIT
        top = (hx + math.sin(ang) * pole * 0.72, hy - math.cos(ang) * pole * 0.72)
        bot = (hx - math.sin(ang) * pole * 0.28, hy + math.cos(ang) * pole * 0.28)
        p.line([bot, top], (110, 84, 56), 7)
        fw, fh = 0.9 / V.M_PER_UNIT, 0.6 / V.M_PER_UNIT
        sg = 1 if getattr(p.cam, 'flip', 1) == 1 else -1
        ripple = lambda u: 18 * math.sin(t * 7 + seed + u * 4) * u * wave
        tl = top
        tr = (top[0] + sg * fw, top[1] + ripple(1.0) + 14)
        br = (top[0] + sg * fw + ripple(0.8), top[1] + fh + ripple(1.0) + 20)
        bl = (top[0] - math.sin(ang) * fh, top[1] + math.cos(ang) * fh)
        q = [tl, tr, br, bl] if sg == 1 else [tr, tl, bl, br]
        PC.place_image(p.img, p.cam, _IMAGES['flag'], q)
        p.line([bot, top], (110, 84, 56), 7)
    draw.held = True
    return draw


BOARD_W = 0.6 / V.M_PER_UNIT


def board_prop(text, seed=0, t=0.0, skin=None):
    """A protester's board held up in both hands at chest-to-head height, bobbing a little with the chant. With
    `skin` (Sam, 20 Oct: "hands coming through signs"): held like her placard, the card in front of the arms and only
    the hands over it, gripping its bottom corners; from behind, the body hides it. Without (the board man in front
    of the low camera, whose board is laid on a sight line): the hands under its middle, as before."""
    def draw(p, j2):
        key = ('board', text, seed)
        if key not in _IMAGES:
            _IMAGES[key] = board_image(text, seed=seed)
        import poker_mon_cast as PC
        (lx, ly), (rx, ry) = j2['wrL'], j2['wrR']
        w = BOARD_W
        h = w * 0.62
        if skin is not None:
            c = math.cos(math.radians(j2.get('yaw', 0)))
            if c < 0.05:
                return
            w *= max(0.12, c)
            cx, cy = (lx + rx) / 2, (ly + ry) / 2 + 26 - h / 2
        else:
            cx, cy = (lx + rx) / 2, (ly + ry) / 2 - h * 0.42
        q = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
        if getattr(p.cam, 'flip', 1) != 1:
            q = [q[1], q[0], q[3], q[2]]
        PC.place_image(p.img, p.cam, _IMAGES[key], q)
        if skin is not None:
            for sd in 'LR':
                B.gesture_hand(p, j2['el' + sd], j2['wr' + sd], 'fist', skin)
    draw.held = skin is None
    return draw


# ------------------------------------------------------------------------------------------------ the carbine
CARBINE = 0.85 / V.M_PER_UNIT        # its length in person units (sizes: 'carbine' 0.75 m, a touch longer to read)
GUN_V = 2.1                          # its depth (receiver, magazine, grip) x 2.1 (Sam, 20 Oct: "very tiny rifles")
GRIP_U, GUARD_U = 0.33, 0.66         # where the right hand (pistol grip) and the left (foregrip) hold it, butt = 0


def carbine():
    """The SIG MCX (refs armed-1..4): all black, short stock, the receiver, a slightly curved magazine, the pistol
    grip, a long slotted handguard with a small foregrip, a small sight on top, the sling. Laid along the line through
    both hands, so it is always really held; foreshortened when it points at or away from us."""
    def draw(p, j2):
        (gx, gy), (fx_, fy) = j2['wrR'], j2['wrL']
        dx, dy = fx_ - gx, fy - gy
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        L = max(n / (GUARD_U - GRIP_U), 0.55 * CARBINE)  # screen length (foreshortened, but never to a stub)
        sx, sy = -uy, ux                                # the gun's "up" on screen: the side away from the floor
        if sy > 0:
            sx, sy = -sx, -sy
        g = GUN_V * (1.0 if L > 0.7 * CARBINE else 0.75)   # nearly end-on: the profile parts shrink a little

        def P(u, v):
            return (gx + ux * (u - GRIP_U) * L + sx * v * g, gy + uy * (u - GRIP_U) * L + sy * v * g)
        p.line([P(0.04, 10), P(0.5, -40), P(0.9, 4)], (30, 30, 34), 3.0)                                       # sling
        p.poly([P(0.0, -20), P(0.0, 22), P(0.06, 24), P(0.2, 14), P(0.2, -8), P(0.08, -12)], GUN_D, INK, 2.0)  # stock
        p.poly([P(0.2, -16), P(0.2, 22), P(0.52, 22), P(0.52, -14)], GUN, INK, 2.2)                           # receiver
        p.poly([P(0.42, -14), P(0.5, -14), P(0.55, -66), P(0.47, -70)], GUN_D, INK, 2.0)                      # magazine
        p.poly([P(0.29, -14), P(0.35, -14), P(0.31, -54), P(0.25, -52)], GUN_D, INK, 1.8)                     # grip
        p.poly([P(0.52, -12), P(0.52, 18), P(0.9, 16), P(0.9, -10)], GUN_D, INK, 2.0)                         # handguard
        for u in np.linspace(0.57, 0.85, 6):                                                                    # its slots
            p.line([P(u, 2), P(u + 0.025, 2)], (70, 72, 78), 2.0)
        p.poly([P(GUARD_U - 0.02, -10), P(GUARD_U + 0.02, -10), P(GUARD_U + 0.015, -34), P(GUARD_U - 0.015, -34)],
               GUN_D, INK, 1.6)                                                                                 # foregrip
        p.poly([P(0.9, -4), P(0.9, 6), P(1.0, 6), P(1.0, -4)], GUN, INK, 1.8)                                 # barrel
        p.poly([P(0.32, 22), P(0.32, 40), P(0.44, 40), P(0.44, 22)], GUN_D, INK, 1.8)                         # sight
    draw.held = True
    return draw


def _hands_on_gun(j, grip, aim_dir):
    """Right hand on the grip at `grip`, left hand on the foregrip along `aim_dir` (torso frame); the gun's own
    length fixes how far apart they are."""
    n = math.sqrt(sum(c * c for c in aim_dir)) or 1.0
    d = (GUARD_U - GRIP_U) * CARBINE
    fore = tuple(g + c / n * d for g, c in zip(grip, aim_dir))
    V.arm_to(j, 'R', grip, 'down', 'fist')
    V.arm_to(j, 'L', fore, 'down', 'fist')
    j['props'] = j.get('props', []) + [carbine()]
    j['grip'] = {'L', 'R'}
    return j


def aim_pose(sp, at=(0.0, 0.0), lean=5.0):
    """Carbine shouldered and aimed: stock in the right shoulder, right hand on the grip under the cheek, left hand
    on the foregrip, elbows down; `at` swings the aim (degrees: right of straight ahead, below level)."""
    j = pose_standing(sp)
    sw = sp.get('shoulders', 150)
    ax, ay = math.radians(at[0]), math.radians(at[1])
    aim = (math.sin(ax), math.sin(ay), math.cos(ax) * math.cos(ay))
    butt = (sw * 0.42, 30.0, 10.0)
    grip = tuple(b + c * GRIP_U * CARBINE for b, c in zip(butt, aim))
    j = _hands_on_gun(j, grip, aim)
    j['lean'] = lean
    return j


def low_ready(j, sp):
    """Carbine held low ready, muzzle down and forward, a little across the body (ref armed-1): for running in. Mostly
    forward, so it reads side on (Sam, 20 Oct: across the body it went end-on and vanished)."""
    sw = sp.get('shoulders', 150)
    return _hands_on_gun(j, (sw * 0.5, 280.0, 120.0), (-0.3, 0.45, 0.84))


def clasped_pose(sp):
    """Hands clasped in front at the belt (ref police-3: the police line's patient stance; Sam, 20 Oct: hands behind
    the back hid both arms from three-quarter)."""
    j = pose_standing(sp)
    V.arm_to(j, 'L', (-16.0, 440.0, 120.0), 'down', 'fist')
    V.arm_to(j, 'R', (16.0, 452.0, 128.0), 'down', 'fist')
    return j


def rope_prop(top=-2400.0, bottom=2400.0):
    """The rope (refs rope-1..2): from above, through the gloved hand, down to the harness at the hip, then on down
    below him; drawn behind the hand that grips it."""
    def draw(p, j2):
        hx, hy = j2['wrR']
        hip = ((j2['hipL'][0] + j2['hipR'][0]) / 2 + 30, (j2['hipL'][1] + j2['hipR'][1]) / 2 - 20)
        for a, b in (((hx, top), (hx, hy)), ((hx, hy), hip), (hip, (hip[0] + 10, bottom))):
            p.line([a, b], INK, 9.0)
            p.line([a, b], (176, 150, 104), 6.0)
        p.ell(hip[0], hip[1], 16, 12, (60, 60, 66), INK, 1.6)          # the descender on the harness
    draw.held = True
    return draw


def carried_pose(sp, kick=0.0, t=0.0):
    """Lifted by both arms (ref arrest: an officer's arm hooked under each armpit, a hand on her forearm): her arms
    held up and out, her feet off the ground, knees bent, legs dangling; `kick` 0..1 swings them a little."""
    j = pose_standing(sp)
    sw = sp.get('shoulders', 120)
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, (sg * (sw + 150), 120.0, 60.0), 'down', 'fist')
    sw_ = 30 * math.sin(t * 6.0) * kick
    for sd, sg, ph in (('L', -1, 0.0), ('R', 1, 1.6)):
        j['foot' + sd] = (sg * 50, V.ANKLE_Y - 90, 60 + 40 * math.sin(t * 6.0 + ph) * kick + sw_)
    j['bob'] = 0.0
    return j


# ------------------------------------------------------------------------------------------------ the key reaction
HORROR = {1: (12, 8, 0, 'raise4'), 2: (14, 16, 0, 'raise9'), 3: (16, 28, 0, 'alarm'), 4: (19, 42, 6, 'alarm'),
          5: (21, 56, 16, 'wow'), 6: (24, 72, 30, 'wow')}       # level: mouth half-width, height, jaw drop, brows


def horror(sp, level):
    """The senior officer's mouth dropping in horror (Sam's brief), strength 1 (lips parted) to 6 (the jaw falls
    right open, South Park style): the library mouth off, our own drawn (one mouth only), the brows up over the
    aviators. Front and three-quarter views."""
    import satire_style
    w, h, drop, br = HORROR[level]
    sp['mouth'] = 'hidden'
    satire_style.own_mouth(sp)
    bc = sp.get('brow_c', (60, 44, 34))
    sp['brows'], sp['brow_c'] = None, sp['skin']        # the library's brows off: ours sit between lenses and peak
    up = {'raise4': (3, 1), 'raise9': (6, 2), 'alarm': (10, 2), 'wow': (12, 4)}[br]

    def draw(p, view, sp_, hx, hy):
        if view not in ('front', 'three'):
            return
        hw, hh = sp_.get('hw', 72), sp_.get('hh', 90)
        fx = hx + (0.4 * hw if view == 'three' else 0.0)
        k = 1.0 if view == 'front' else 0.8
        if drop:                                       # the jaw falls: the chin drawn lower over the collar
            skin = sp_['skin']
            tone = tuple(int(a + (b - a) * 0.3) for a, b in zip(skin, sp_.get('beard_c', skin)))
            jaw = curve([(hx - hw * 0.98, hy + hh * 0.3), (hx - hw * 0.9, hy + hh * 0.7 + drop * 0.5),
                         (hx - hw * 0.5, hy + hh * 1.0 + drop), (fx, hy + hh * 1.06 + drop), (hx + hw * 0.5, hy + hh * 1.0 + drop),
                         (hx + hw * 0.9, hy + hh * 0.7 + drop * 0.5), (hx + hw * 0.98, hy + hh * 0.3)], 4)
            p.poly(jaw, skin, None)
            p.line(jaw[1:-1], INK, 2.6)                      # the jaw's edge only (no line across the cheeks)
            stub = curve([(hx - hw * 0.96, hy + 20), (hx - hw * 0.9, hy + hh * 0.66 + drop * 0.5),
                          (hx - hw * 0.5, hy + hh * 0.98 + drop), (fx, hy + hh * 1.04 + drop), (hx + hw * 0.5, hy + hh * 0.98 + drop),
                          (hx + hw * 0.9, hy + hh * 0.66 + drop * 0.5), (hx + hw * 0.96, hy + 20), (fx + 34, hy + 44),
                          (fx - 34, hy + 44)], 4)
            p.poly(stub, tone, None)
            rng = np.random.default_rng(5)
            for _ in range(160):
                a = rng.uniform(0.2, math.pi - 0.2)
                r = rng.uniform(0.55, 0.96)
                p.ell(fx + hw * 0.88 * r * math.cos(a), hy + 30 + (hh * 0.74 + drop) * r * math.sin(a), 0.9, 0.9,
                      sp_.get('beard_c', (90, 70, 60)), None)
        for sgn in (-1, 1):                            # the brows: inner ends up, both lifted (alarm, then more)
            ex, ey = fx - 4 + sgn * 30 * k, hy - 8
            p.poly(curve([(ex - sgn * 8 * k, ey - 22 - up[0]), (ex + sgn * 8 * k, ey - 23 - up[0] + up[1]),
                          (ex + sgn * 24 * k, ey - 17 - up[1]), (ex + sgn * 23 * k, ey - 13 - up[1]),
                          (ex + sgn * 8 * k, ey - 17 - up[0] + up[1]), (ex - sgn * 8 * k, ey - 16 - up[0])], 3), bc, None)
        my = hy + 52
        pts = curve([(fx - w * k, my), (fx, my - 3), (fx + w * k, my), (fx + w * 0.9 * k, my + h * 0.7),
                     (fx, my + h), (fx - w * 0.9 * k, my + h * 0.7)], 4)
        p.poly(pts, (70, 26, 30), INK, 2.4)
        if h >= 16:                                    # the top teeth
            p.poly([(fx - w * 0.8 * k, my), (fx + w * 0.8 * k, my), (fx + w * 0.7 * k, my + 6), (fx - w * 0.7 * k, my + 6)],
                   (246, 246, 240), None)
        if h >= 40:                                    # the tongue down in the jaw
            p.ell(fx, my + h * 0.8, w * 0.55 * k, h * 0.12, (196, 90, 96), None)
    return draw


# ------------------------------------------------------------------------------------------------ the cast sheet
def _height_s(name, s, sp=None):
    h = HEIGHTS.get(name, (sp or {}).get('height', 1.75))
    return s * h / 1.75


def cast_sheet(out):
    """Everyone the film needs, on one sheet (guides/satire.md, step 3): the line-up at their real heights with the
    body landmarks and a scale person; every other view each appears in (her sign raised, carried, from behind,
    seated; the senior officer from every side and seated; Jenkins side-on; an armed officer aiming, one coming down
    a rope; the police line's poses); the props at real size beside the scale person; and the numbered strength sheet
    for the key reaction (the senior officer's mouth dropping in horror, 1 = slight, 6 = huge)."""
    import landmarks
    import moves
    import sizes
    import poker_mon_cast as PC
    B.SS = 1
    Wd, Ht = 3150, 2760
    img = Image.new('RGBA', (Wd, Ht), (232, 228, 222, 255))
    cam = B.Cam(1.0, 540, 960)
    d = ImageDraw.Draw(img)
    lab = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 20)
    big = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 30)

    def label(x, y, txt, f=lab):
        d.text((x, y), txt, fill=(40, 40, 46), font=f, anchor='mm')

    S0 = 0.46
    ppm = S0 / V.M_PER_UNIT                               # pixels per metre on rows 1 and 2
    # ---- row 1: the line-up
    d.text((30, 20), 'POWER CRIME ACTION - cast sheet (row 1 at real heights; red lines: neck, waist, hips, knee)',
           fill=(40, 40, 46), font=big)
    floor = 900
    line = [('GRAN', GRAN, 'the old lady'), ('SUPER', SUPER, 'Chief Supt'), ('JENKINS', JENKINS, 'Jenkins'),
            ('PC1', PCS[0], 'PC (hi-vis)'), ('PC2', PCS[1], 'PC'), ('PC3', PCS[2], 'PC'),
            ('ARV1', ARVS[0], 'armed: flat cap'), ('ARV4', ARVS[3], 'armed: navy cap'), ('ARV7', ARVS[6], 'armed: rope team')]
    x = 130
    for name, sp, txt in line:
        s = _height_s(name, S0)
        j = pose_standing(sp)
        if name.startswith('ARV'):
            j = low_ready(j, sp)
        person(img, cam, x, floor - V.ANKLE_Y * s - 38 * s, s, sp, 0.0, 0, j)
        label(x, floor + 24, txt)
        x += 215
    for k, i in enumerate((3, 11)):                       # two protesters: a flag, a board
        sp = protester(i)
        sp['carry'] = ('flag', 'board')[k]
        s = _height_s(sp['name'], S0, sp)
        j = pose_standing(sp)
        if k == 0:
            V.arm_to(j, 'R', (sp['shoulders'] * 0.7, -120.0, 60.0), 'out', 'fist')
            j['props'].append(flag_prop(0.4, seed=i))
            j['grip'] = {'R'}
        else:
            for sd, sg in (('L', -1), ('R', 1)):
                V.arm_to(j, sd, (sg * 150.0, 250.0, 150.0), 'down', 'fist')
            j['props'].append(board_prop('FREE PALESTINE', seed=i))
            j['grip'] = {'L', 'R'}
        outfit(j, sp)
        person(img, cam, x, floor - V.ANKLE_Y * s - 38 * s, s, sp, 0.0, 0, j)
        label(x, floor + 24, ('protester: flag', 'protester: board')[k])
        x += 215
    ny = floor - V.ANKLE_Y * S0 - 38 * S0
    landmarks.draw(d, 1060, ny, S0, 2050)
    # ---- the props at real size beside a scale person
    px0 = x + 30
    sizes.scale_ref(d, px0, floor, ppm)
    label(px0, floor + 24, '1.75 m')
    pw, ph = PLACARD_W * ppm, PLACARD_H * ppm
    pim = placard_image().resize((int(pw), int(ph)), Image.LANCZOS)
    img.alpha_composite(pim, (int(px0 + 70), int(floor - 1.6 * ppm)))
    label(px0 + 70 + pw / 2, floor - 1.6 * ppm - 18, 'placard 45x60 cm')
    d.rectangle([px0 + 70, floor - 1.6 * ppm + ph * LETTERED, px0 + 70 + pw, floor - 1.6 * ppm + ph], outline=(200, 40, 40), width=2)
    label(px0 + 70 + pw / 2, floor - 1.6 * ppm + ph + 18, 'red: never lettered,')
    label(px0 + 70 + pw / 2, floor - 1.6 * ppm + ph + 40, 'always hidden')
    # ---- row 2: her other views
    floor2 = 1760
    d.text((30, 950), 'Every other view: her sign (chest -> overhead, trembling), carried by the arms, from behind, seated; '
           'the senior officer from every side and seated; Jenkins; an armed officer aiming and on the rope; the police line',
           fill=(40, 40, 46), font=lab)
    x = 130
    s = _height_s('GRAN', S0)
    ng = floor2 - V.ANKLE_Y * s - 38 * s
    for raise_u, yaw, txt in ((0.0, 0, 'sign at her chest'), (1.0, 45, 'sign raised (3/4)')):
        j, _ = placard_pose(GRAN, 0.3, raise_u)
        person(img, cam, x, ng, s, GRAN, 0.3, yaw, j)
        label(x, floor2 + 24, txt)
        x += 200
    j = carried_pose(GRAN, kick=0.6, t=0.4)
    person(img, cam, x, ng - 110 * s, s, GRAN, 0.0, 90, j)
    label(x, floor2 + 24, 'carried (feet off)')
    x += 200
    person(img, cam, x, ng, s, GRAN, 0.0, 180)
    label(x, floor2 + 24, 'from behind')
    x += 190
    j = outfit(moves.seated(GRAN), GRAN)
    person(img, cam, x, ng, s, GRAN, 0.0, 45, j)
    label(x, floor2 + 24, 'seated (3/4)')
    x += 220
    s = _height_s('SUPER', S0)
    ns = floor2 - V.ANKLE_Y * s - 38 * s
    for yaw, txt in ((45, 'Chief Supt 3/4'), (90, 'side'), (180, 'back')):
        person(img, cam, x, ns, s, SUPER, 0.0, yaw)
        label(x, floor2 + 24, txt)
        x += 200
    j = outfit(moves.seated(SUPER), SUPER)
    person(img, cam, x, ns, s, SUPER, 0.0, -45, j)
    label(x, floor2 + 24, 'seated (3/4)')
    x += 210
    s = _height_s('JENKINS', S0)
    person(img, cam, x, floor2 - V.ANKLE_Y * s - 38 * s, s, JENKINS, 0.0, -90)
    label(x, floor2 + 24, 'Jenkins side')
    x += 200
    s = _height_s('ARV2', S0)
    j = aim_pose(ARVS[1], (0, 4))
    person(img, cam, x, floor2 - V.ANKLE_Y * s - 38 * s, s, ARVS[1], 0.0, 90, j)
    label(x, floor2 + 24, 'aiming (side)')
    x += 240
    j = aim_pose(ARVS[4], (0, 4))
    person(img, cam, x, floor2 - V.ANKLE_Y * s - 38 * s, s, ARVS[4], 0.0, 45, j)
    label(x, floor2 + 24, 'aiming (3/4)')
    x += 230
    s = _height_s('ARV8', S0)                              # on the rope (refs rope-1..2): one hand high on the rope
    sp = ARVS[7]
    j = pose_standing(sp)
    V.arm_to(j, 'R', (30.0, -300.0, 60.0), 'up', 'fist')
    V.arm_to(j, 'L', (sp['shoulders'] + 40.0, 150.0, 160.0), 'down', 'fist')
    j['footL'] = (-90.0, V.ANKLE_Y - 120, 120.0)
    j['footR'] = (70.0, V.ANKLE_Y - 40, -40.0)
    j['lean'] = -8
    j['props'].append(rope_prop(top=-900.0, bottom=1500.0))
    j['grip'] = {'R'}
    ny8 = floor2 - V.ANKLE_Y * s - 38 * s - 120
    person(img, cam, x, ny8, s, sp, 0.0, 90, j)
    label(x, floor2 + 24, 'rope (CT team)')
    x += 210
    s = _height_s('PC4', S0)
    for sp_, pose_, txt in ((PCS[3], 'arms_folded', 'arms folded'), (PCS[4], 'clasped', 'hands clasped at belt')):
        j = outfit(moves.pose(sp_, pose_) if pose_ != 'clasped' else clasped_pose(sp_), sp_)
        person(img, cam, x, floor2 - V.ANKLE_Y * s - 38 * s, s, sp_, 0.0, 0 if pose_ == 'arms_folded' else 45, j)
        label(x, floor2 + 24, txt)
        x += 190
    # ---- row 3: the key reaction, 1-6
    d.text((30, 1840), "Key reaction: the senior officer's mouth drops in horror (pick a number; 'Shit. A code red.')",
           fill=(40, 40, 46), font=big)
    for lv in range(1, 7):
        sp = dict(SUPER)
        hp = horror(sp, lv)
        j = pose_standing(sp)
        j['head_props'] = [hp] + j['head_props']
        cx = 230 + (lv - 1) * 400
        person(img, cam, cx, 2470, 1.25, sp, 0.0, 0, j)
        label(cx, 1935, str(lv), big)
    img.convert('RGB').save(out, quality=90)


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        cast_sheet(sys.argv[2])
