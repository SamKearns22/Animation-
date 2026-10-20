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

mouths.install(B)
install_circle_hands(B)

# ------------------------------------------------------------------------------------------------ colours
HIVIS, HIVIS_D = (212, 226, 40), (170, 182, 30)
SILVER = (206, 210, 216)
UNIFORM = (30, 32, 40)            # the Met's black wicking tops and trousers
ARV_TOP = (36, 40, 56)            # armed officers: dark navy
ARMOUR, ARMOUR_D = (26, 27, 31), (16, 16, 19)
WHITE_SHIRT = (244, 244, 240)
CAP, CAP_D = (22, 22, 28), (12, 12, 16)
POLICE_BLUE = (30, 60, 140)
GUN, GUN_D = (40, 42, 46), (24, 25, 28)
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
# The senior officer (Sam, 20 Oct: yes, with tough stubble): middle-aged, square-jawed, white shirt, black tie,
# epaulettes with a crown, peaked cap with the chequered band and silver braid, mirrored aviators.
SUPER = dict(name='SUPER', skin=B.PINK, hw=74, hh=92, jaw='square', hair='crop', hair_c=(70, 62, 58),
             brow_c=(60, 52, 48), brow_w=4.4, beard='stubble', beard_c=(64, 56, 52), outfit='jumper',
             jacket=WHITE_SHIRT, trousers=UNIFORM, shoulders=160, creases=2, mouth='set', cap='peaked', braid=True,
             aviators=True, white_shirt=True, seed=32)
# Jenkins: a young constable, lanky, eager, ginger; black top, black stab vest with POLICE, radio on the chest.
JENKINS = dict(name='JENKINS', skin=B.PALE, hw=64, hh=90, jaw='soft', hair='side', hair_c=(196, 112, 60),
               brow_c=(176, 96, 52), outfit='jumper', jacket=UNIFORM, trousers=UNIFORM, shoulders=138,
               stab_vest=True, mouth='line', seed=33)


def _officer(i, skin, hair, hair_c, hat, jaw='square', hw=70, hh=90, sw=152, mouth='set', brows=None, **kw):
    return dict(name=f'PC{i}', skin=skin, hw=hw, hh=hh, jaw=jaw, hair=hair, hair_c=hair_c,
                brow_c=B.dk(hair_c, 0.85) if hair != 'bald' else (90, 70, 60), outfit='jumper', jacket=HIVIS,
                trousers=UNIFORM, shoulders=sw, hivis=True, cap=hat, mouth=mouth, brows=brows, seed=40 + i, **kw)


# The police line at the edge of the square: hi-vis jackets; custodian helmets and peaked caps (both true to the Met).
PCS = [_officer(1, B.PALE, 'crop', (110, 80, 54), 'helmet'),
       _officer(2, B.BROWN, 'crop', (30, 24, 22), 'peaked', jaw='soft', hw=64, hh=86, sw=134, lashes=True),
       _officer(3, B.DEEP, 'bald', (40, 32, 30), 'helmet', hw=74, sw=160, beard='trim', beard_c=(40, 32, 30)),
       _officer(4, B.PINK, 'side', (196, 168, 110), 'peaked', hw=68, hh=88, sw=146),
       _officer(5, B.OLIVE, 'crop', (40, 34, 30), 'helmet', hw=72, sw=156, beard='stubble')]


def _arv(i, skin, hair_c, jaw='square', hw=70, hh=90, sw=162, **kw):
    return dict(name=f'ARV{i}', skin=skin, hw=hw, hh=hh, jaw=jaw, hair='crop', hair_c=hair_c,
                brow_c=B.dk(hair_c, 0.85), outfit='jumper', jacket=ARV_TOP, trousers=ARV_TOP, shoulders=sw,
                arv=True, cap='ball', mouth='set', brows='serious', seed=60 + i, **kw)


# The armed officers (Met ARV: navy tops, black armour marked POLICE, blue-black caps with the chequered band, SIG MCX
# carbines). Eight: three from the left, three from the right, two down ropes (Sam, 20 Oct).
ARVS = [_arv(1, B.PALE, (90, 66, 44)), _arv(2, B.BROWN, (28, 22, 20), beard='trim', beard_c=(28, 22, 20)),
        _arv(3, B.PINK, (150, 110, 70), hw=66, sw=150), _arv(4, B.DEEP, (24, 20, 18), hw=74, sw=170),
        _arv(5, B.OLIVE, (40, 32, 28), beard='stubble'), _arv(6, B.PALE, (196, 150, 90), hw=68, sw=156),
        _arv(7, B.PALE, (60, 46, 36), beard='stubble', hw=72), _arv(8, B.BROWN, (30, 24, 22), jaw='soft', hw=66, sw=148)]
PEOPLE = {'GRAN': GRAN, 'SUPER': SUPER, 'JENKINS': JENKINS}
PEOPLE.update({p['name']: p for p in PCS + ARVS})
HEIGHTS = {'GRAN': 1.55, 'SUPER': 1.85, 'JENKINS': 1.86}
HEIGHTS.update({p['name']: h for p, h in zip(PCS, (1.80, 1.68, 1.88, 1.78, 1.83))})
HEIGHTS.update({p['name']: h for p, h in zip(ARVS, (1.84, 1.82, 1.78, 1.90, 1.80, 1.79, 1.85, 1.76))})

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
def chequer(p, x0, x1, y0, y1, rows=2, n=None, flip_x=None):
    """The Sillitoe tartan band: black and white squares, two rows."""
    n = n or max(4, int(abs(x1 - x0) / max(1.0, (y1 - y0) / rows)))
    w, h = (x1 - x0) / n, (y1 - y0) / rows
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], (246, 246, 242), INK, 1.8)
    for r in range(rows):
        for c in range(n):
            if (r + c) % 2 == 0:
                p.poly([(x0 + c * w, y0 + r * h), (x0 + (c + 1) * w, y0 + r * h), (x0 + (c + 1) * w, y0 + (r + 1) * h),
                        (x0 + c * w, y0 + (r + 1) * h)], (24, 24, 28), None)
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], None, INK, 1.8)


def star(p, cx, cy, r, col=SILVER):
    """The Met's Brunswick star: an eight-pointed silver star with a small crowned centre."""
    pts = []
    for k in range(16):
        a = -math.pi / 2 + k * math.pi / 8
        rr = r if k % 2 == 0 else r * 0.62
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    p.poly(pts, col, INK, 1.6)
    p.ell(cx, cy, r * 0.36, r * 0.36, (60, 70, 120), INK, 1.2)


def peaked_cap(p, view, sp, hx, hy):
    """The Met's flat peaked cap: black crown, chequered band, glossy black peak; silver braid for senior ranks."""
    hw, hh = sp.get('hw', 72), sp.get('hh', 90)
    top, b0, b1 = hy - hh * 1.2, hy - hh * 0.80, hy - hh * 0.58
    braid = sp.get('braid')
    if view in ('front', 'three'):
        o = 0.0 if view == 'front' else 0.18 * hw
        crown = curve([(hx - hw * 0.98, b0 + 4), (hx - hw * 1.16, top + 16), (hx - hw * 0.7, top), (hx + o, top - 6),
                       (hx + hw * 0.7, top), (hx + hw * 1.16, top + 16), (hx + hw * 0.98, b0 + 4)], 3)
        p.poly(crown, CAP, INK, 2.4)
        p.line([(hx - hw * 0.96, top + 20), (hx + o, top + 12), (hx + hw * 0.96, top + 20)], CAP_D, 2.0)
        chequer(p, hx - hw * 0.99, hx + hw * 0.99, b0, b1, n=14)
        pk = [(hx - hw * 0.92 + o, b1 - 2), (hx + o, b1 + hh * 0.06), (hx + hw * 0.92 + o, b1 - 2),
              (hx + hw * 0.7 + o, b1 + hh * 0.2), (hx + o, b1 + hh * 0.27), (hx - hw * 0.7 + o, b1 + hh * 0.2)]
        p.poly(curve(pk, 3), CAP_D, INK, 2.2)
        p.line([(hx - hw * 0.5 + o, b1 + hh * 0.18), (hx + o, b1 + hh * 0.22)], (90, 90, 100), 2.0)   # the gloss
        if braid:
            for k in range(9):
                x = hx + o + (k - 4) * hw * 0.17
                p.ell(x, b1 + hh * 0.2 - abs(k - 4) * 2.4, hw * 0.07, hh * 0.04, SILVER, INK, 1.0)
        star(p, hx + o, (top + b0) / 2 + 4, hw * 0.26)
    elif view == 'side':
        crown = curve([(hx - hw * 1.02, b1), (hx - hw * 1.12, top + 12), (hx - hw * 0.4, top - 2), (hx + hw * 0.7, top + 2),
                       (hx + hw * 1.18, top + 16), (hx + hw * 0.98, b1)], 3)
        p.poly(crown, CAP, INK, 2.4)
        chequer(p, hx - hw * 1.0, hx + hw * 0.98, b0, b1, n=12)
        p.poly(curve([(hx + hw * 0.7, b1 - 4), (hx + hw * 1.5, b1 + hh * 0.12), (hx + hw * 1.46, b1 + hh * 0.2),
                      (hx + hw * 0.8, b1 + hh * 0.1)], 3), CAP_D, INK, 2.2)
        if braid:
            p.line([(hx + hw * 0.9, b1 + hh * 0.12), (hx + hw * 1.42, b1 + hh * 0.18)], SILVER, 4.0)
        star(p, hx + hw * 0.8, (top + b0) / 2 + 4, hw * 0.18)
    else:
        crown = curve([(hx - hw * 0.98, b0 + 4), (hx - hw * 1.14, top + 16), (hx, top - 4), (hx + hw * 1.14, top + 16),
                       (hx + hw * 0.98, b0 + 4)], 3)
        p.poly(crown, CAP, INK, 2.4)
        chequer(p, hx - hw * 0.99, hx + hw * 0.99, b0, b1, n=14)


def custodian(p, view, sp, hx, hy):
    """The custodian helmet: a tall black dome with a comb, the silver Brunswick star at the front, a rose boss on top."""
    hw, hh = sp.get('hw', 72), sp.get('hh', 90)
    rim, top = hy - hh * 0.62, hy - hh * 1.9
    if view == 'side':
        dome = curve([(hx - hw * 1.16, rim + 6), (hx - hw * 1.0, hy - hh * 1.3), (hx - hw * 0.3, top + 6),
                      (hx + hw * 0.5, hy - hh * 1.55), (hx + hw * 1.06, hy - hh * 1.0), (hx + hw * 1.22, rim + 2)], 3)
        p.poly(dome, CAP, INK, 2.4)
        p.poly(curve([(hx - hw * 1.3, rim + 10), (hx + hw * 1.34, rim), (hx + hw * 1.3, rim + 14),
                      (hx - hw * 1.24, rim + 22)], 2), CAP_D, INK, 2.0)
        p.line([(hx - hw * 0.9, hy - hh * 1.32), (hx - hw * 0.2, top + 14)], (60, 62, 72), 2.4)
        star(p, hx + hw * 0.62, hy - hh * 1.05, hw * 0.22)
        p.ell(hx - hw * 0.28, top + 2, hw * 0.12, hh * 0.08, SILVER, INK, 1.4)
        return
    w0 = 1.1 if view != 'three' else 1.06
    o = 0.0 if view in ('front', 'back') else (0.14 * hw if view == 'three' else -0.14 * hw)
    dome = curve([(hx - hw * w0, rim + 4), (hx - hw * 0.98, hy - hh * 1.3), (hx - hw * 0.58 + o, top + 16),
                  (hx + o, top), (hx + hw * 0.58 + o, top + 16), (hx + hw * 0.98, hy - hh * 1.3), (hx + hw * w0, rim + 4)], 3)
    p.poly(dome, CAP, INK, 2.4)
    p.poly(curve([(hx - hw * 1.18, rim), (hx + hw * 1.18, rim), (hx + hw * 1.12, rim + 14), (hx - hw * 1.12, rim + 14)], 2),
           CAP_D, INK, 2.0)
    p.line([(hx + o, top + 6), (hx + o, rim - 6)], (60, 62, 72), 2.2)            # the comb down the middle
    if view in ('front', 'three'):
        star(p, hx + o * 1.6, hy - hh * 1.08, hw * 0.3)
    p.ell(hx + o, top - 2, hw * 0.14, hh * 0.08, SILVER, INK, 1.4)               # the rose boss


def ball_cap(p, view, sp, hx, hy):
    """An armed officer's cap: blue-black, hugging the head, the chequered band, a short curved bill."""
    hw, hh = sp.get('hw', 72), sp.get('hh', 90)
    top, b0, b1 = hy - hh * 1.1, hy - hh * 0.7, hy - hh * 0.56
    if view == 'side':
        p.poly(curve([(hx - hw * 1.02, b1), (hx - hw * 0.96, hy - hh * 0.95), (hx - hw * 0.2, top), (hx + hw * 0.7, hy - hh * 0.98),
                      (hx + hw * 1.0, b1)], 3), CAP, INK, 2.4)
        chequer(p, hx - hw * 1.0, hx + hw * 0.98, b0, b1, n=12)
        p.poly(curve([(hx + hw * 0.8, b1 - 4), (hx + hw * 1.62, b1 + 6), (hx + hw * 1.56, b1 + 14),
                      (hx + hw * 0.86, b1 + 8)], 3), CAP_D, INK, 2.2)
        return
    o = 0.0 if view in ('front', 'back') else (0.2 * hw if view == 'three' else -0.2 * hw)
    p.poly(curve([(hx - hw * 1.0, b1), (hx - hw * 0.94, hy - hh * 0.9), (hx - hw * 0.5 + o, top + 6), (hx + o, top),
                  (hx + hw * 0.5 + o, top + 6), (hx + hw * 0.94, hy - hh * 0.9), (hx + hw * 1.0, b1)], 3), CAP, INK, 2.4)
    p.line([(hx + o, top + 4), (hx + o * 1.4, b0 - 2)], CAP_D, 1.8)
    chequer(p, hx - hw * 1.0, hx + hw * 1.0, b0, b1, n=14)
    if view in ('front', 'three'):
        p.poly(curve([(hx - hw * 0.8 + o, b1 - 2), (hx + o * 1.5, b1 + 4), (hx + hw * 0.8 + o * 2, b1 - 2),
                      (hx + hw * 0.66 + o * 2, b1 + hh * 0.18), (hx + o * 1.5, b1 + hh * 0.24),
                      (hx - hw * 0.66 + o, b1 + hh * 0.18)], 3), CAP_D, INK, 2.2)


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
    for k, (x, y) in enumerate(blobs[::3]):                    # a few inner swirls
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
    p.line([(lenses[0][0] + 26, hy - 10), ((lenses[0][0] + lenses[1][0]) / 2, hy - 14), (lenses[1][0] - 26 * lenses[1][1], hy - 10)],
           (236, 120, 170), 5)


LENS, LENS_L, FRAME = (70, 104, 140), (176, 206, 228), (200, 186, 120)


def _lens(p, ex, ey, w, sgn):
    """One aviator lens, teardrop, outer corner dropping lower; a flat mirror sheen across it."""
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


HATS = {'peaked': peaked_cap, 'helmet': custodian, 'ball': ball_cap}


# ------------------------------------------------------------------------------------------------ worn on the body
def _torso_box(view, sp):
    """(left, right) edges of the torso at chest height for a view, facing right."""
    sw = sp.get('shoulders', 150)
    return {'front': (-sw, sw), 'three': (-sw * 0.95, sw * 0.82), 'side': (-0.6 * sw, 0.66 * sw),
            'three_back': (-sw * 0.9, sw * 0.9), 'back': (-sw, sw)}[view]


def _label(p, cx, cy, w, text, fill=(246, 246, 242), size=1.0):
    """A small printed patch with block letters (POLICE): the letters fitted to the patch's width."""
    h = 44 * size
    p.poly([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)],
           fill, INK, 1.6)
    _text(p, cx, cy, w * 0.86, h * 0.7, text, INK if fill != ARMOUR else (246, 246, 242))


_GLYPH = {}


def _text(p, cx, cy, w, h, text, col, font=BLOCK):
    """Block lettering fitted to a box (w x h, person units), drawn as a picture laid into the frame so it never
    pulses (drawn once large, then scaled)."""
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
    if a[0] > b[0]:
        small = small.transpose(Image.FLIP_LEFT_RIGHT)       # mirrored person: keep the letters reading forwards
        small = small.transpose(Image.FLIP_LEFT_RIGHT)
    p.img.alpha_composite(small, (int(round(x0)), int(round(y0)))) if x0 >= 0 and y0 >= 0 else p.img.paste(small, (int(x0), int(y0)), small)


def hivis(p, view, sp):
    """The hi-vis jacket: yellow, two silver reflective bands round the body, POLICE on a panel (chest and back)."""
    l, r = _torso_box(view, sp)
    for y in (300, 380):
        p.poly([(l + 4, y), (r - 4, y), (r - 6, y + 26), (l + 6, y + 26)], SILVER, INK, 1.6)
    if view in ('front', 'three'):
        p.line([(0 if view == 'front' else 0.32 * sp.get('shoulders', 150), 0),
                (0 if view == 'front' else 0.32 * sp.get('shoulders', 150) + 4, 500)], HIVIS_D, 2.2)
        cx = 0 if view == 'front' else 0.32 * sp.get('shoulders', 150)
        _label(p, cx - 60 if view == 'front' else cx - 50, 170, 90, 'POLICE', (246, 246, 242), 0.8)
    elif view in ('back', 'three_back'):
        _label(p, 0, 170, (r - l) * 0.62, 'POLICE', (246, 246, 242), 1.3)


def armour(p, view, sp):
    """The armed officer's black body armour over a navy top: plate carrier with pouches, POLICE in white."""
    l, r = _torso_box(view, sp)
    p.poly(rough([(l + 14, 40), (r - 14, 40), (r - 4, 120), (r - 6, 470), (l + 6, 470), (l + 4, 120)], 3, 5),
           ARMOUR, INK, 2.4)
    if view in ('front', 'three'):
        p.poly([(l + 30, 0), (l + 80, 0), (l + 70, 60), (l + 30, 60)], ARMOUR, INK, 2.0)        # shoulder straps
        p.poly([(r - 80, 0), (r - 30, 0), (r - 30, 60), (r - 70, 60)], ARMOUR, INK, 2.0)
        for k in range(3):                                                         # magazine pouches
            x = l + 40 + k * (r - l - 80) / 3
            p.poly([(x, 330), (x + (r - l - 100) / 3, 330), (x + (r - l - 100) / 3, 430), (x, 430)], ARMOUR_D, INK, 1.6)
        _text(p, (l + r) / 2, 190, (r - l) * 0.6, 56, 'POLICE', (246, 246, 242))
        p.poly([(r - 70, 90), (r - 40, 90), (r - 40, 150), (r - 70, 150)], (50, 50, 56), INK, 1.4)   # radio
    elif view in ('back', 'three_back'):
        _text(p, (l + r) / 2, 200, (r - l) * 0.7, 80, 'POLICE', (246, 246, 242))
    else:
        p.poly([(r - 50, 330), (r + 6, 330), (r + 6, 430), (r - 50, 430)], ARMOUR_D, INK, 1.6)


def stab_vest(p, view, sp):
    """Jenkins's black stab vest over his black top: POLICE patch, a radio clipped high on the chest."""
    l, r = _torso_box(view, sp)
    p.poly(rough([(l + 20, 30), (r - 20, 30), (r - 8, 110), (r - 10, 450), (l + 10, 450), (l + 8, 110)], 3, 7),
           (20, 21, 26), INK, 2.2)
    if view in ('front', 'three'):
        _label(p, (l + r) / 2, 220, (r - l) * 0.5, 'POLICE', (246, 246, 242), 0.8)
        p.poly([(l + 40, 80), (l + 74, 80), (l + 74, 150), (l + 40, 150)], (56, 56, 62), INK, 1.4)
        p.line([(l + 50, 80), (l + 50, 50)], INK, 3.0)
    elif view in ('back', 'three_back'):
        _label(p, 0, 200, (r - l) * 0.6, 'POLICE', (246, 246, 242), 1.1)


def white_shirt(p, view, sp):
    """The senior officer's white shirt: black tie, collar, epaulettes with a silver crown, pockets."""
    l, r = _torso_box(view, sp)
    if view == 'front':
        p.poly([(-11, 16), (11, 16), (15, 200), (0, 228), (-15, 200)], (24, 24, 28), INK, 2.0)
        p.poly([(-12, -2), (12, -2), (9, 18), (-9, 18)], (24, 24, 28), INK, 2.0)
        for sg in (-1, 1):
            p.poly([(sg * 12, -6), (sg * 46, -6), (sg * 36, 26)], WHITE_SHIRT, INK, 1.8)            # collar points
            p.poly([(sg * 56, 120), (sg * 116, 120), (sg * 116, 196), (sg * 56, 196)], WHITE_SHIRT, INK, 1.6)  # pockets
            p.line([(sg * 56, 138), (sg * 116, 138)], INK, 1.4)
            p.poly([(sg * (r - 70), 6), (sg * (r - 8), 26), (sg * (r - 12), 46), (sg * (r - 74), 30)], (24, 24, 28), INK, 1.6)
            p.ell(sg * (r - 40), 26, 9, 7, SILVER, INK, 1.0)                                       # the crown
        p.line([(0, 228), (0, 500)], (214, 214, 210), 1.6)
    elif view == 'three':
        o = 0.32 * sp.get('shoulders', 150)
        p.poly([(o - 8, 16), (o + 10, 16), (o + 13, 196), (o + 2, 222), (o - 10, 196)], (24, 24, 28), INK, 2.0)
        p.poly([(o - 30, 120), (o - 80, 120), (o - 80, 190), (o - 30, 190)], WHITE_SHIRT, INK, 1.6)
        p.poly([(r - 60, 8), (r - 6, 26), (r - 10, 44), (r - 64, 30)], (24, 24, 28), INK, 1.6)
    elif view == 'side':
        p.poly([(30, 10), (42, 12), (0.6 * sp.get('shoulders', 150) * 0.9, 196), (0.6 * sp.get('shoulders', 150) * 0.8, 192)],
               (24, 24, 28), INK, 1.8)
        p.poly([(-30, 8), (30, 8), (30, 30), (-30, 30)], (24, 24, 28), INK, 1.6)
    else:
        for sg in (-1, 1):
            p.poly([(sg * (r - 70), 6), (sg * (r - 8), 26), (sg * (r - 12), 46), (sg * (r - 74), 30)], (24, 24, 28), INK, 1.6)


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
    sw, bottom = sp.get('shoulders', 120), sp.get('bottom', 600)
    if view == 'front':
        p.line([(-46, -4), (0, 70), (46, -4)], INK, 7)
    l, r = _torso_box(view, sp)
    p.line([(l + 6, bottom - 6), (r - 6, bottom - 6)], INK, 9)


def dress(sp):
    """The film's clothing and headwear for one person, as views' body_props and head_props."""
    body, head = [], []
    if sp.get('hivis'):
        body.append(hivis)
    if sp.get('arv'):
        body.append(armour)
    if sp.get('stab_vest'):
        body.append(stab_vest)
    if sp.get('white_shirt'):
        body.append(white_shirt)
    if sp.get('keffiyeh'):
        body.append(keffiyeh)
    if sp.get('trim'):
        body.append(trim)
    if sp.get('curls'):
        head.append(curls)
    if sp.get('striped_glasses'):
        head.append(striped_glasses)
    if sp.get('aviators'):
        head.append(aviators)
    if sp.get('cap'):
        head.append(HATS[sp['cap']])
    return body, head


def pose_standing(sp):
    j = V.standing(sp)
    j['body_props'], j['head_props'] = dress(sp)
    return j


def person(img, cam, x, y, s, sp, t=0.0, yaw=0, j=None, head_yaw=None):
    j = j or pose_standing(sp)
    if 'body_props' not in j:
        j['body_props'], j['head_props'] = dress(sp)
    return V.person(img, cam, x, y, s, dict(sp, full=True, pose='custom'), t, yaw, j, head_yaw)


# ------------------------------------------------------------------------------------------------ the placard
PLACARD_M = 0.5                    # 50 cm square (sizes: 'protest placard')
LETTERED = 0.58                    # the top 58% is lettered; below it, plain card that is always hidden


def placard_image(px=500, lettered=True):
    """Her placard: hand-cut brown card, black marker capitals I OPPOSE / GENOCIDE / I SUPPORT on the top part. The
    rest is plain card (never lettered: Sam, 20 Oct)."""
    im = Image.new('RGBA', (px, px), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(7)
    edge = [(6 + rng.uniform(-3, 3), 6 + rng.uniform(-3, 3)), (px - 6 + rng.uniform(-3, 3), 4 + rng.uniform(-3, 3)),
            (px - 4 + rng.uniform(-3, 3), px - 6 + rng.uniform(-3, 3)), (5 + rng.uniform(-3, 3), px - 5 + rng.uniform(-3, 3))]
    d.polygon(edge, fill=CARD + (255,))
    for k in range(9):                                        # the corrugation showing faintly through
        y = int(px * (0.08 + 0.1 * k))
        d.line([(10, y), (px - 10, y + 2)], fill=CARD_D + (90,), width=2)
    if lettered:
        f = ImageFont.truetype(FONT, int(px * 0.16))
        for k, (txt, y) in enumerate((('I OPPOSE', 0.05), ('GENOCIDE', 0.22), ('I SUPPORT', 0.40))):
            l, t_, r, b = d.textbbox((0, 0), txt, font=f)
            d.text(((px - (r - l)) / 2 - l + rng.uniform(-6, 6), px * y - t_), txt, font=f, fill=MARKER + (255,))
    d.line(edge + [edge[0]], fill=(40, 30, 24, 255), width=max(2, px // 160))
    return im


_PLACARD = {}


def placard(img, quad):
    """Lay her placard into the frame: corners TL, TR, BR, BL in frame pixels (1080 x 1920 units)."""
    if 'im' not in _PLACARD:
        _PLACARD['im'] = placard_image()
    import poker_mon_cast as PC
    PC.place_image(img, B.Cam(1.0, 540, 960), _PLACARD['im'], quad)


def board_image(text, px=420, seed=0):
    """A protester's board: white card, hand-lettered in red or black."""
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
        sc = min(1.0, (w * 0.9) / (r - l))
        d.text(((w - (r - l)) / 2 - l, h * (0.1 + 0.42 * k) - t_), ln, font=f, fill=col + (255,))
    d.line([(4, 4), (w - 4, 6), (w - 6, h - 4), (6, h - 6), (4, 4)], fill=(40, 30, 24, 255), width=3)
    return im


def flag_image(px=360):
    """The Palestinian flag: black, white, green bands; a red triangle at the hoist."""
    w, h = px, int(px * 0.5)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k, c in enumerate(PAL_FLAG[:3]):
        d.rectangle([0, k * h / 3, w, (k + 1) * h / 3], fill=c + (255,))
    d.polygon([(0, 0), (w * 0.36, h / 2), (0, h)], fill=PAL_FLAG[3] + (255,))
    d.rectangle([0, 0, w - 1, h - 1], outline=(24, 22, 26, 255), width=3)
    return im


# ------------------------------------------------------------------------------------------------ the carbine
def carbine(lean=0.0, sling=True):
    """A SIG MCX carbine held at the shoulder (a held prop): the stock at the right shoulder, right hand on the grip,
    left hand on the handguard; drawn along the line from the shoulder past both hands, side-on profile shapes
    shortened by how much the gun points at us. 0.75 m long (sizes: 'carbine')."""
    def draw(p, j2):
        view = j2['yaw']
        a = (j2['shR'][0] * 0.5 + j2['wrR'][0] * 0.5, j2['shR'][1] * 0.3 + j2['wrR'][1] * 0.7 - 10)
        b = j2['wrL']
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        full = 0.75 / V.M_PER_UNIT                       # the real length in person units
        k = max(0.18, min(1.0, n / (full * 0.62)))       # foreshortened when pointing at or away from us
        L = full * k
        sx, sy = (-uy, ux) if ux >= 0 else (uy, -ux)     # the gun's "up" on screen
        if sy > 0:
            sx, sy = -sx, -sy

        def P(u, v):                                     # u along the gun from the butt (0) to the muzzle (1); v up
            return (a[0] + ux * (u * L - 0.18 * L) + sx * v, a[1] + uy * (u * L - 0.18 * L) + sy * v)
        p.poly([P(0.0, -22), P(0.0, 26), P(0.08, 22), P(0.22, 14), P(0.22, -10), P(0.06, -14)], GUN_D, INK, 2.0)  # stock
        p.poly([P(0.22, -18), P(0.22, 24), P(0.56, 24), P(0.56, -16)], GUN, INK, 2.2)                         # receiver
        p.poly([P(0.4, -16), P(0.48, -16), P(0.52, -70), P(0.44, -72)], GUN_D, INK, 2.0)                    # magazine
        p.poly([P(0.28, -16), P(0.34, -16), P(0.3, -54), P(0.24, -52)], GUN_D, INK, 1.8)                    # grip
        p.poly([P(0.56, -14), P(0.56, 20), P(0.86, 18), P(0.86, -12)], GUN_D, INK, 2.0)                     # handguard
        p.poly([P(0.86, -5), P(0.86, 6), P(1.0, 6), P(1.0, -5)], GUN, INK, 1.8)                             # barrel
        p.poly([P(0.3, 24), P(0.3, 40), P(0.46, 40), P(0.46, 24)], GUN_D, INK, 1.8)                         # optic
        p.ell(*P(0.38, 32), 8 * k + 3, 6, (120, 30, 30), None)
    draw.held = True
    return draw


def aim_pose(sp, at=(0.0, 0.0), lean=4.0):
    """Standing, carbine shouldered and aimed: right hand on the grip under the cheek, left on the handguard, elbows
    down; `at` swings the aim (x right, y down, in degrees)."""
    j = pose_standing(sp)
    sw = sp.get('shoulders', 150)
    ax, ay = math.radians(at[0]), math.radians(at[1])
    fwd = lambda d: (sw * 0.55 + d * math.sin(ax), 40 + d * math.sin(ay), d * math.cos(ax) * math.cos(ay))
    V.arm_to(j, 'R', fwd(140), 'down', 'fist')
    V.arm_to(j, 'L', fwd(330), 'down', 'fist')
    j['lean'] = lean
    j['props'] = j.get('props', []) + [carbine(lean)]
    j['grip'] = {'L', 'R'}
    return j


def placard_pose(sp, t=0.0, raise_u=1.0, tremble=1.0, seed=0):
    """Her placard raised in both hands above her head, arms nearly straight, trembling (the script says so: a quick
    small judder, never a slow sway). Returns the pose and the placard's corners in her own units (x, y)."""
    j = pose_standing(sp)
    rng = (math.sin(t * 41 + seed) + 0.6 * math.sin(t * 67 + 1.3 + seed)) * tremble
    jy = 5 * rng
    jx = 3 * math.sin(t * 53 + 0.7 + seed) * tremble
    low = (0.0, 330.0, 90.0)
    high = (0.0, -270.0, 70.0)
    cy = low[1] + (high[1] - low[1]) * raise_u + jy
    cz = low[2] + (high[2] - low[2]) * raise_u
    half = PLACARD_M / V.M_PER_UNIT / 2
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, (sg * (half - 10) + jx, cy, cz), 'out', 'fist')
    # the card's corners: the hands grip its sides a little below the lettering's foot
    top = cy - half * 2 * (LETTERED + 0.06)
    quad = [(-half + jx, top), (half + jx, top + 2), (half + jx, top + half * 2), (-half + jx, top + half * 2)]
    j['grip'] = {'L', 'R'}
    return j, quad
