#!/usr/bin/env python3
"""Terfwarts: the cast (Harry, Ron, McGonagall, Myrtle) and the Sorting Hat, and the cast sheet.
MAP: colours: top; hair, glasses, lips: head props; uniform, Myrtle's skirt, the tartan coat: body props; the Hat:
hat(); people: CAST, HEIGHTS, person(); Myrtle see-through: ghost(); the sheet: sheet() (rows: turnarounds x2, key
views, Harry's annoyance 1-6, faces).

    python3 source/terfwarts_cast.py OUT.jpg          (also: python3 source/terfwarts.py cast OUT.jpg)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import mossad                    # noqa: E402,F401  (mouth shapes, brows)
import mouths                    # noqa: E402
import views as V                # noqa: E402
import moves as MV               # noqa: E402
from ed import INK, curve        # noqa: E402
from satire_style import install_circle_hands, rough   # noqa: E402

mouths.install(B)
install_circle_hands(B)
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
M = V.M_PER_UNIT

ROBE = (34, 28, 36)              # plum-black robes (refs trio-hbo-cloister)
MAROON, GOLD = (122, 30, 40), (206, 164, 62)
TARTAN = (104, 118, 134)         # McGonagall's blue-grey tartan coat (ref mcgonagall-hbo)
HAT, HAT_DK, PATCH = (124, 88, 56), (84, 58, 38), (146, 108, 72)


# ------------------------------------------------------------------------------------------------ worn on the head
def _cap(p, view, hx, hy, hw, hh, c, fringe, seed, lumps=9, vol=1.12, curly=False):
    """A full head of hair as one lumpy shape over the base crop: a jagged top and a fringe edge for each view."""
    r = np.random.default_rng(seed)
    top = []
    for i in range(lumps + 1):
        a = math.pi * (1 - i / lumps)
        k = vol * (1 + r.uniform(-0.05, 0.07))
        top.append((hx + math.cos(a) * hw * 1.08 * (1.06 if curly else 1.0), hy - 12 - math.sin(a) * hh * k))
    if view == 'front':
        edge = [(hx + hw * 1.02, hy - 14), (hx - hw * 1.02, hy - 14)]
        fr_from, fr_to = hx + hw * 0.8, hx - hw * 0.8
    elif view == 'three':
        edge = [(hx + hw * 1.0, hy - 20), (hx - hw * 0.95, hy + 20)]
        fr_from, fr_to = hx + hw * 0.95, hx - hw * 0.15
    elif view == 'side':
        edge = [(hx + hw * 0.72, hy - 26), (hx - hw * 1.0, hy + hh * 0.45)]
        fr_from, fr_to = hx + hw * 0.72, hx + hw * 0.1
    else:                                         # from behind: the hair comes down to the nape
        edge = [(hx + hw * 1.04, hy + 10), (hx - hw * 1.04, hy + 10)]
        fr_from = fr_to = None
    pts = top + [edge[0]]
    if fr_from is not None:                       # the fringe: points hanging over the brow
        n = 6
        for i in range(n + 1):
            x = fr_from + (fr_to - fr_from) * i / n
            y = hy - fringe + (r.uniform(4, 14) if i % 2 == 0 else -r.uniform(10, 22))
            pts.append((x, y))
    else:
        for i in range(7):
            x = edge[0][0] + (edge[1][0] - edge[0][0]) * i / 6
            pts.append((x, hy + hh * 0.5 + (10 if i % 2 else -6)))
    pts.append(edge[1])
    p.poly(curve(pts, 3), c, INK, 2.6)
    cd = B.dk(c, 0.72)
    for i in range(4):                            # a few strands
        x = hx - hw * 0.5 + i * hw * 0.32
        p.line([(x, hy - hh * 0.95), (x + 10, hy - hh * 0.62)], cd, 1.8)


def _face_x(view, hx, hw, sp):
    return hx + sp.get('turn', 0.0) * hw * 0.22 if view == 'front' else hx + 0.4 * hw


def round_glasses(p, view, sp, hx, hy):
    """Thin round wire frames (Harry: black; Myrtle: round too)."""
    gc, hw = sp.get('rg_c', (26, 24, 28)), sp.get('hw', 72)
    fx = _face_x(view, hx, hw, sp)
    if view == 'front':
        for sgn in (-1, 1):
            p.ell(fx - 4 + sgn * 30, hy - 8, 22, 21, None, gc, 3.0)
        p.line([(fx - 12, hy - 12), (fx - 4, hy - 16), (fx + 4, hy - 12)], gc, 2.6)
        for sgn in (-1, 1):
            p.line([(fx - 4 + sgn * 52, hy - 12), (hx + sgn * (hw + 2), hy - 16)], gc, 2.4)
    elif view == 'three':
        for ex, w in ((fx - 26, 1.0), (fx + 24, 0.62)):
            p.ell(ex, hy - 8, 21 * w, 20, None, gc, 3.0)
        p.line([(fx - 5, hy - 12), (fx + 9, hy - 12)], gc, 2.6)
        p.line([(fx - 47, hy - 12), (hx - 0.5 * hw + 6, hy - 6)], gc, 2.4)
    elif view == 'side':
        p.ell(hx + 46, hy - 10, 6, 19, None, gc, 3.0)
        p.line([(hx + 40, hy - 12), (hx - 16, hy - 4)], gc, 2.4)


def harry_hair(p, view, sp, hx, hy):
    _cap(p, view, hx, hy, sp['hw'], sp['hh'], sp['hair_c'], sp['hh'] * 0.46, 11, lumps=11, vol=1.16)


def ron_hair(p, view, sp, hx, hy):
    _cap(p, view, hx, hy, sp['hw'], sp['hh'], sp['hair_c'], sp['hh'] * 0.5, 23, lumps=8, vol=1.2, curly=True)


def freckles(p, view, sp, hx, hy):
    if view in ('front', 'three'):
        fx = _face_x(view, hx, sp['hw'], sp)
        r = np.random.default_rng(4)
        for _ in range(14):
            sgn = 1 if r.random() < 0.5 else -1
            p.ell(fx - 4 + sgn * r.uniform(12, 40), hy + r.uniform(12, 34), 2.2, 2.2, (196, 128, 92), None)


def myrtle_hair(p, view, sp, hx, hy):
    """Dark bunches at the sides with a straight-ish fringe (refs myrtle-1/2/3)."""
    hw, hh, c = sp['hw'], sp['hh'], sp['hair_c']
    if view != 'side':
        sides = (-1, 1) if view in ('front', 'back') else (-1,)
        for sgn in sides:
            bx = hx + sgn * (hw + 26)
            p.poly(curve(rough([(bx - 22, hy - 10), (bx + 20, hy - 14), (bx + 30, hy + 40), (bx + 10, hy + 92),
                                (bx - 18, hy + 70), (bx - 30, hy + 24)], 4, 7 + sgn), 3), c, INK, 2.6)
            p.ell(bx - sgn * 8, hy - 6, 8, 8, (70, 110, 150), INK, 2.0)     # the band
    _cap(p, view, hx, hy, hw, hh, c, hh * 0.4, 31, lumps=7, vol=1.06)


def mcg_hair(p, view, sp, hx, hy):
    """Dark grey hair swept up, a side wave, a low bun at the back (ref mcgonagall-hbo)."""
    hw, hh, c = sp['hw'], sp['hh'], sp['hair_c']
    if view in ('side', 'three_back', 'back', 'three'):
        bx = hx - (hw * 0.95 if view in ('side', 'three') else 0)
        p.poly(curve(rough([(bx - 34, hy - 30), (bx + 30, hy - 34), (bx + 40, hy + 10), (bx + 10, hy + 34),
                            (bx - 34, hy + 22)], 4, 3), 3), c, INK, 2.6)
    pts = [(hx - hw * 1.02, hy - 10), (hx - hw * 1.0, hy - hh * 0.7), (hx - hw * 0.5, hy - hh * 1.12),
           (hx + hw * 0.4, hy - hh * 1.14), (hx + hw * 1.0, hy - hh * 0.72), (hx + hw * 1.02, hy - 10),
           (hx + hw * 0.86, hy - 40), (hx + hw * 0.2, hy - hh * 0.62), (hx - hw * 0.5, hy - hh * 0.9),
           (hx - hw * 0.86, hy - 44)]
    if view == 'back':
        pts = pts[:6] + [(hx + hw, hy + 20), (hx - hw, hy + 20)]
    p.poly(curve(pts, 3), c, INK, 2.6)
    cd = B.lt(c, 1.25)
    p.line([(hx - hw * 0.6, hy - hh * 0.98), (hx, hy - hh * 1.06), (hx + hw * 0.7, hy - hh * 0.8)], cd, 2.0)


def red_lips(p, view, sp, hx, hy):
    if view in ('front', 'three') and sp.get('mouth', 'set') in ('set', 'line'):
        fx = _face_x(view, hx, sp['hw'], sp) + (0 if view == 'front' else 4)
        my = hy + sp.get('mouth_y', 62)
        p.poly(curve([(fx - 20, my), (fx - 6, my - 5), (fx, my - 3), (fx + 6, my - 5), (fx + 20, my), (fx + 6, my + 6),
                      (fx - 6, my + 6)], 3), (150, 30, 44), INK, 1.6)


def hat(p, cx, by, k=1.0, mood='rest', open_=1.0):
    """The Sorting Hat (refs sorting-hat-face, sorting-hat-scene): patched brown suede, a slumped point, a wide floppy
    brim; folds make a brow, two eye creases and a wide mouth near the base. mood: 'rest', 'yell'."""
    P = lambda pts: [(cx + x * k, by + y * k) for x, y in pts]        # noqa: E731
    p.poly(curve(P(rough([(-205, 4), (-150, -26), (-60, -38), (60, -38), (150, -26), (210, 6), (150, 30), (0, 40),
                          (-150, 28)], 5, 1)), 3), HAT_DK, INK, 2.8)
    p.poly(curve(P(rough([(-108, -16), (-116, -110), (-94, -204), (-54, -282), (8, -330), (82, -366), (140, -350),
                          (108, -322), (66, -280), (76, -200), (100, -108), (108, -16)], 5, 2)), 3), HAT, INK, 2.8)
    p.poly(P([(-100, -168), (-58, -176), (-52, -112), (-96, -104)]), PATCH, INK, 2.0)        # the torn patch
    for a, b in (((-98, -160), (-62, -168)), ((-56, -170), (-54, -118)), ((-94, -110), (-58, -116))):
        p.line(P([a, b]), B.dk(PATCH, 0.6), 1.2)
    p.line(P([(-30, -250), (10, -232), (50, -262)]), HAT_DK, 2.2)                           # crown creases
    p.line(P([(-60, -26), (-40, -12), (-10, -20)]), HAT_DK, 2.0)
    p.poly(curve(P([(-78, -184), (-30, -204), (20, -196), (78, -206), (60, -186), (10, -178), (-40, -170)]), 3),
           HAT_DK, INK, 2.0)                                                                      # the brow fold
    if mood == 'yell':
        for sgn in (-1, 1):
            p.poly(P([(sgn * 20, -168), (sgn * 60, -158), (sgn * 52, -146), (sgn * 18, -154)]), (40, 24, 16), None)
        o = 0.25 + 0.75 * max(0.0, min(1.0, open_))    # how wide (Sam's note 13.1: a syllable at a time)
        Q = lambda pts: P([(x, -118 + (y + 118) * o) for x, y in pts])   # noqa: E731  the lower jaw drops from the top lip
        p.poly(curve(Q([(-80, -110), (-36, -126), (36, -126), (84, -108), (62, -48), (0, -30), (-60, -48)]), 3),
               (44, 22, 16), INK, 2.6)
        if o > 0.45:
            p.poly(curve(Q([(-58, -60), (0, -46), (58, -60), (40, -40), (0, -34), (-40, -40)]), 3), (120, 40, 40), None)
    else:
        for sgn in (-1, 1):
            p.line(P([(sgn * 18, -152), (sgn * 40, -146), (sgn * 62, -152)]), (40, 24, 16), 3.0)
        p.line(P([(-70, -82), (-30, -72), (0, -76), (34, -70), (70, -84)]), (40, 24, 16), 3.2)
        p.line(P([(-60, -64), (0, -58), (56, -66)]), HAT_DK, 1.8)


def worn_hat(mood):
    def draw(p, view, sp, hx, hy):
        if view == 'front':
            hat(p, hx, hy - 84, sp['hw'] / 120, mood)
    return draw


# ------------------------------------------------------------------------------------------------ worn on the body
def _o(view, sp):
    return 0.0 if view == 'front' else 0.32 * sp.get('shoulders', 150)


def _x(view, sp, x):
    return _o(view, sp) + x * (1.0 if view == 'front' else 0.75)


def uniform(p, view, sp):
    """Maroon V-neck jumper with gold trim over the shirt, the striped tie in the V (ref harry-hbo-clapper)."""
    if view not in ('front', 'three'):
        return
    X = lambda pts: [(_x(view, sp, x), y) for x, y in pts]            # noqa: E731
    jc = sp.get('jumper', MAROON)
    p.poly(X([(-36, 40), (0, 122), (36, 40), (22, 150), (0, 232), (-22, 150)]), jc, INK, 2.0)
    p.line(X([(-36, 42), (0, 124), (36, 42)]), GOLD, 3.2)
    tc, sc = sp.get('tie', MAROON), sp.get('stripe', GOLD)
    p.poly(X([(-11, 16), (11, 16), (10, 95), (0, 108), (-10, 95)]), tc, INK, 1.8)
    p.poly(X([(-12, -2), (12, -2), (9, 18), (-9, 18)]), tc, INK, 1.8)
    for y in (32, 56, 80):
        p.line(X([(-10, y + 6), (10, y - 6)]), sc, 3.0)


def satchel(p, view, sp):
    if view in ('front', 'three'):
        p.line([(_x(view, sp, -60), 10), (_x(view, sp, 70), 330)], (92, 64, 40), 7.0)


def myrtle_clothes(p, view, sp):
    """Grey cardigan, the striped tie (blue and bronze), buttons, a pleated grey skirt (refs myrtle-1/2/3)."""
    sw = sp.get('shoulders', 150)
    lo, hi = (-sw * 0.95, sw * 0.95) if view in ('front', 'back') else (-sw * 0.8, sw * 0.75)
    p.poly(curve([(lo + 6, 430), (hi - 6, 430), (hi + 30, 660), (lo - 30, 660)], 2), (96, 98, 104), INK, 2.4)
    for i in range(1, 6):
        x = lo - 30 + (hi - lo + 60) * i / 6
        p.line([(lo + 6 + (hi - lo - 12) * i / 6, 450), (x, 652)], B.dk((96, 98, 104), 0.7), 1.6)
    if view in ('front', 'three'):
        X = lambda pts: [(_x(view, sp, x), y) for x, y in pts]        # noqa: E731
        for y in (40, 80, 120, 160):
            p.line(X([(-12, y + 6), (12, y - 6)]), (176, 136, 70), 3.0)
        for y in (270, 330, 390):
            p.ell(_x(view, sp, 6), y, 5, 5, (60, 60, 64), None)


def tartan_coat(p, view, sp):
    """The long tartan coat buttoned to a high black collar (ref mcgonagall-hbo)."""
    sw, bottom, c = sp.get('shoulders', 150), sp.get('bottom', 505), sp['jacket']
    if view == 'front':
        p.poly([(-40, -4), (40, -4), (22, 150), (0, 240), (-22, 150)], c, None)
    span = {'front': (-1, 1), 'back': (-1, 1), 'side': (-0.55, 0.6)}.get(view, (-0.88, 0.78))
    for y in range(70, int(bottom) - 10, 64):
        w = sw * (0.94 - 0.12 * (y - 50) / bottom)
        p.line([(span[0] * w, y), (span[1] * w, y)], B.dk(c, 0.78), 3.0)
        p.line([(span[0] * w, y + 9), (span[1] * w, y + 9)], B.lt(c, 1.18), 1.4)
    for f in (-0.62, -0.25, 0.12, 0.5):
        x = f * sw * (1 if view in ('front', 'back') else 0.85)
        if span[0] * sw * 0.8 < x < span[1] * sw * 0.8:
            p.line([(x, 40), (x * 0.9, bottom - 8)], B.dk(c, 0.78), 3.0)
            p.line([(x + 9, 40), (x * 0.9 + 9, bottom - 8)], B.lt(c, 1.18), 1.4)
    o = _o(view, sp) if view in ('front', 'three') else (0.45 * sw if view == 'side' else None)
    if o is not None:
        p.poly([(o - 40, -44), (o + 40, -44), (o + 46, 14), (o - 46, 14)], (24, 22, 26), INK, 2.2)
    elif view in ('back', 'three_back'):
        p.poly([(-46, -40), (46, -40), (50, 14), (-50, 14)], (24, 22, 26), INK, 2.2)


# ------------------------------------------------------------------------------------------------ the cast
UNI = dict(outfit='suit', jacket=ROBE, sleeve=ROBE, trousers=(40, 40, 44), shoe=(22, 20, 20), shirt=(240, 240, 236),
           tie=MAROON, bottom=780)
CAST = {
    'harry': dict(name='Harry', skin=(242, 216, 198), hw=80, hh=96, jaw='soft', hair='crop', hair_c=(46, 34, 28),
                  shoulders=120, brow_c=(46, 34, 28), seed=51, props=[harry_hair, round_glasses], **UNI),
    'ron': dict(name='Ron', skin=(246, 218, 200), hw=84, hh=94, jaw='round', hair='crop', hair_c=(200, 96, 42),
                shoulders=124, brow_c=(176, 90, 46), seed=52, props=[ron_hair, freckles], **UNI),
    'mcg': dict(name='McGonagall', skin=(234, 208, 192), hw=66, hh=96, jaw='long', hair='crop', hair_c=(92, 88, 92),
                glasses=True, glasses_c=(30, 28, 32), shoulders=130, brow_c=(70, 66, 70), lashes=True, outfit='suit',
                jacket=TARTAN, sleeve=TARTAN, trousers=(40, 40, 46), shoe=(20, 20, 22), bottom=840, age=True,
                seed=53, props=[mcg_hair, red_lips], body=[tartan_coat]),
    'myrtle': dict(name='Myrtle', skin=(240, 220, 210), hw=76, hh=92, jaw='soft', hair='crop', hair_c=(40, 34, 32),
                   shoulders=118, brow_c=(40, 34, 32), lashes=True, outfit='suit', jacket=(128, 130, 136),
                   sleeve=(128, 130, 136), trousers=(232, 228, 222), shoe=(40, 40, 44), shirt=(240, 240, 236),
                   tie=(44, 64, 120), bottom=470, seed=54, props=[myrtle_hair, round_glasses], body=[myrtle_clothes]),
}
HEIGHTS = {'harry': 1.42, 'ron': 1.47, 'mcg': 1.75, 'myrtle': 1.50}
ORDER = ('harry', 'ron', 'mcg', 'myrtle')
for _w in ('harry', 'ron'):                       # the uniform goes on under everything else worn on the body
    CAST[_w]['body'] = [uniform] + CAST[_w].get('body', [])


def person(img, cam, x, floor, s, who, yaw=0, j=None, extra=None, lift=0.0, t=0.0, head_props=()):
    """Draw one of the cast standing on `floor` (pixels) at scale s for a 1.75 m person. Returns the neck point."""
    sp = dict(CAST[who], **(extra or {}))
    s2 = s * HEIGHTS[who] / 1.75
    j = j or V.standing(sp)
    j['body_props'] = list(sp.get('body', [])) + j.get('body_props', [])
    j['head_props'] = list(sp.get('props', [])) + list(head_props) + j.get('head_props', [])
    ny = floor - (928 - j.get('bob', 0.0)) * s2 - lift
    if who == 'myrtle':
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        V.person(lay, cam, x, ny, s2, dict(sp, full=True, pose='custom'), t, yaw, j)
        ghost(img, lay)
    else:
        V.person(img, cam, x, ny, s2, dict(sp, full=True, pose='custom'), t, yaw, j)
    return x, ny, s2


def ghost(img, lay):
    """See-through pale blue, no glow (refs myrtle-1/2/3): the drawing turned to blue greys, 68% solid."""
    r, g, b, a = lay.split()
    grey = Image.merge('RGB', (r, g, b)).convert('L')
    tint = Image.merge('RGB', (grey.point(lambda v: int(v * 0.5 + 48)), grey.point(lambda v: int(v * 0.66 + 62)),
                               grey.point(lambda v: int(v * 0.5 + 118))))
    tint.putalpha(a.point(lambda v: int(v * 0.68)))
    img.alpha_composite(tint)


# ------------------------------------------------------------------------------------------------ the sheet
def _flat():
    cam = B.Cam(1.0, 540, 960)
    cam.P = lambda x, y: (x, y)
    cam.S = lambda v: v
    return cam


def sheet(out):
    import landmarks
    import sizes
    B.SS = 1
    W, H = 1080, 2340
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    big, small = ImageFont.truetype(FONT, 30), ImageFont.truetype(FONT, 19)
    cam = _flat()
    d.text((20, 12), 'TERFWARTS: the cast at real heights', font=big, fill=(30, 30, 30))
    views = ((0, 'front'), (45, '3/4'), (90, 'side'), (180, 'back'))
    s = 0.36
    for r, pair in enumerate((('harry', 'ron'), ('mcg', 'myrtle'))):
        floor = 70 + 470 * (r + 1)
        for i, who in enumerate(pair):
            for k, (yaw, lab) in enumerate(views):
                x = 70 + (i * 4 + k) * 118
                if k == 0:
                    s2 = s * HEIGHTS[who] / 1.75
                    landmarks.draw(d, x, floor - 928 * s2, s2, 100)
                person(img, cam, x, floor, s, who, yaw)
                d.text((x, floor + 6), lab, font=small, fill=(60, 60, 60), anchor='mt')
            d.text((70 + i * 4 * 118 - 40, floor - 440), CAST[who]['name'] + f' {HEIGHTS[who]:.2f} m', font=small,
                   fill=(30, 30, 30))
        d.line([(30, floor), (1050, floor)], fill=(150, 146, 140), width=2)
    sizes.scale_ref(d, 1000, 1010, s / M)

    # key views: the close-up (McGonagall places the Hat), the run at the lens, Myrtle blocks the door
    y0 = 1040
    d.text((20, y0), 'Key views', font=big, fill=(30, 30, 30))
    tile = Image.new('RGBA', (400, 520), (214, 198, 170, 255))
    tc = _flat()
    hx, hfloor, hs = 150, 510, 0.42                    # Harry seated; McGonagall behind his shoulder, a little back
    sit = MV.seated(CAST['harry'])
    s2h = hs * HEIGHTS['harry'] / 1.75
    neck_y = hfloor - (928 - sit['bob']) * s2h
    hk = CAST['harry']['hw'] / 120 * s2h
    brim = (hx, neck_y - 150 * s2h - CAST['harry']['hh'] * s2h - 4)   # held just above his hair
    mx, mfloor, ms = 222, 500, 0.42
    s2m = ms * HEIGHTS['mcg'] / 1.75
    mny = mfloor - 928 * s2m
    jm = V.standing(CAST['mcg'])
    hands = [(brim[0] - 200 * hk, brim[1]), (brim[0] + 200 * hk, brim[1])]
    for side, (tx, ty) in zip(('L', 'R'), hands):
        V.arm_to(jm, side, ((mx - tx) / s2m, (ty - mny) / s2m, 90.0), 'down', 'fist')
    person(tile, tc, mx, mfloor, ms, 'mcg', -45, jm)
    hip = neck_y + 450 * s2h
    ImageDraw.Draw(tile).rectangle((hx - 90 * s2h * 1.4, hip, hx + 90 * s2h * 1.4, hfloor), fill=(96, 64, 40), outline=(20, 16, 14), width=2)
    person(tile, tc, hx, hfloor, hs, 'harry', 0, sit, dict(brows='fierce', mouth='line', look=0.3))
    tp = B.Pen(tile, tc)
    hat(tp, brim[0], brim[1], hk, 'rest')
    for tx, ty in hands:
        tp.ell(tx, ty, 26 * s2m, 26 * s2m, CAST['mcg']['skin'], INK, 2.6)
    img.alpha_composite(tile, (20, y0 + 44))
    d.text((24, y0 + 570), 'Shot 1: McGonagall lowers the Hat\nonto Harry (the shot itself is close)', font=small,
           fill=(30, 30, 30))
    run = Image.new('RGBA', (300, 520), (0, 0, 0, 0))
    for who, x, t in (('ron', 215, 0.18), ('harry', 85, 0.0)):
        person(run, tc, x, 500, 0.58, who, 0, MV.gait(dict(CAST[who]), t, 'run'))
    img.alpha_composite(run, (430, y0 + 44))
    d.text((440, y0 + 570), 'Shot 2: Harry and Ron\nrun at the lens', font=small, fill=(30, 30, 30))
    jy = V.standing(CAST['myrtle'])
    for side, tgt in {'L': (-330.0, 40.0, 60.0), 'R': (330.0, 40.0, 60.0)}.items():
        V.arm_to(jy, side, tgt, 'down', 'fist')
    my = Image.new('RGBA', (330, 520), (196, 172, 128, 255))
    ImageDraw.Draw(my).rectangle((60, 120, 270, 520), fill=(112, 78, 50))        # a stand-in door behind her
    person(my, tc, 165, 470, 0.42, 'myrtle', 0, jy, dict(mouth='v:AI', brows='fierce'), lift=40)
    img.alpha_composite(my, (735, y0 + 44))
    d.text((740, y0 + 570), 'Shots 3-5: Myrtle floats,\nsee-through; arms spread\nacross the doorway', font=small,
           fill=(30, 30, 30))

    # Harry's annoyance, 1-6, with the Hat on
    y1 = y0 + 650
    d.text((20, y1), "Harry's annoyance under the Hat: pick 1-6", font=big, fill=(30, 30, 30))
    faces = [dict(brow_raise=-3, mouth='set'), dict(brows='fierce', mouth='set'), dict(brows='fierce', lid=2, mouth='line'),
             dict(brows='fierce', lid=3, mouth='v:etc', look=0.4), dict(brows='fierce', lid=4, mouth='v:FV', look=0.5),
             dict(brows='fierce', lid=5, mouth='shout', look=0.5)]
    for i, f in enumerate(faces):
        t = Image.new('RGBA', (172, 250), (244, 240, 234, 255))
        person(t, tc, 86, 846, 0.75, 'harry', 0, None, f, head_props=[worn_hat('yell')])
        img.alpha_composite(t, (20 + i * 176, y1 + 44))
        d.text((106 + i * 176, y1 + 300), str(i + 1), font=big, fill=(30, 30, 30), anchor='mt')

    # the other faces
    y2 = y1 + 350
    d.text((20, y2), 'Faces', font=big, fill=(30, 30, 30))
    heads = [('Hat: rest', None, 'rest'), ('Hat: yelling', None, 'yell'),
             ('Ron: vacant', 'ron', dict(mouth='agape', brow_raise=6)), ('Ron: talking', 'ron', dict(mouth='v:O', brow_raise=8)),
             ('Myrtle: lecturing', 'myrtle', dict(mouth='v:AI', brows='fierce')), ('McGonagall', 'mcg', dict(mouth='set'))]
    for i, (lab, who, f) in enumerate(heads):
        t = Image.new('RGBA', (172, 200), (244, 240, 234, 255))
        if who is None:
            hat(B.Pen(t, tc), 86, 180, 0.4, f)
        else:
            k = 0.9
            person(t, tc, 86, 120 + 928 * k * HEIGHTS[who] / 1.75 + 150 * k * HEIGHTS[who] / 1.75, k, who, 0, None, f)
        img.alpha_composite(t, (20 + i * 176, y2 + 44))
        d.multiline_text((24 + i * 176, y2 + 250), lab.replace(': ', ':\n'), font=small, fill=(30, 30, 30))
    img.convert('RGB').save(out, quality=90)


if __name__ == '__main__':
    sheet(sys.argv[1])
