#!/usr/bin/env python3
"""MAP  Blessed, note 25 (Sam, 12 Nov): David Walliams led by two officers into the prison door Brand just left, at the
end of the gates shot. Front-on only (Sam: "everyone front-on, South Park movement"), scared and alarmed. His head is
a measured likeness (likeness.py card on w01-w03, references/blessed/likeness/) on the patriots4 face layout, drawn
at Brand's size (blessed_cast HEAD_K), the Brand way.

    WALLIAMS  card (12 Nov): a short nose (98th centile), a narrow forehead (97th), narrow hooded eyes (92nd), a wide
              mouth (91st), a wide nose (87th), a thin upper lip (85th). By eye: short brown hair swept up and back off
              a clear, high forehead, grey at the sides; a short salt-and-pepper beard, grey-white on the chin and jaw,
              darker grey-brown at the moustache; light skin. Very tall (1.96 m). Prison: Brand's grey tracksuit.

    python3 source/blessed_walliams.py head OUT.png [--average] [--mood M]   his head straight on (likeness.py check)
    python3 source/blessed_walliams.py faces OUT.jpg                          his face in each mood, his photos beside

Map: measures 35 | moods 45 | beard 55 | hair 95 | mouth 140 | head 165 | the person 205 | sheets 225
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import blessed_cast as BC          # noqa: E402  (P4, TC, the house head size, the tracksuit)
from blessed_cast import P4, TC, AV, B, V, dk, blend, INK, curve, oval  # noqa: E402

# ---------------------------------------------------------------------------------------------- measures (12 Nov)
_card = json.load(open(os.path.join(HERE, '..', 'references', 'blessed', 'likeness', 'walliams-card.json')))
_WM, _WA = _card['measures'], _card['average']
P4.MEASURED['walliams'] = {k: P4.AVG[k] + _WM[k] - _WA[k] for k in P4.AVG}
P4.PUSH['walliams'] = 1.6
# Note 29 (Sam, 12 Nov: not recognisable): a new card from Sam's straight-on photos w06, w07 with w01, w02. Its top
# measures: a broad, square jaw (99th), a long chin (98th), a narrow forehead, a long gap nose to lip, small wide-set
# eyes. Its 'short nose' (82nd, the photos disagree) is the long chin taking the face's height: by eye the nose is
# long and straight, so it is pushed the other way (TUNE -1.5), as the first try's tiny button nose taught.

# ---------------------------------------------------------------------------------------------- moods
# brow: up (+); frown (-) lifts the inner ends (worry); lid: upper lid down; wide: the stare (P4.eyes)
MOODS = {'neutral': dict(brow=0.0, frown=0.0, lid=0.25, wide=0.0, mouth='lips', smile=1.0, squint=0.55, cock=0.015),   # the smirk
         # scared and alarmed (note 25): brows high and pinched up in the middle, eyes wide, mouth pulled into a
         # wide grimace, the teeth showing
         'scared': dict(brow=0.03, frown=-0.07, lid=0.0, wide=1.0, mouth='lips', smile=-0.8),   # chat 3: the grimace read as a grin,
         'alarmed': dict(brow=0.06, frown=-0.02, lid=0.0, wide=1.0, mouth='gasp'),
         # note 32: pleading with the press: brows up and pinched, soft wide eyes, the mouth turned down
         'pleading': dict(brow=0.03, frown=-0.1, lid=0.06, wide=0.55, mouth='lips', smile=-0.9)}


# ---------------------------------------------------------------------------------------------- the face (job, 12 Nov)
# The Walliams' face job (Sam, 12 Nov: "not nearly as recognisable as RB"). The blind name test (nametest.py) named
# the old head "nobody in particular" and ranked Walliams 7th of 8 look-alikes; the Brand head was named at once.
# What Brand has and he lacked: features pushed hard (Brand's TUNE runs to x25; his ran to x2.2) and big two-tone
# shapes that read at phone size. His own cues, by eye on w02, w06, w07, w09: a BIG, broad, fleshy face, round full
# cheeks and a wide jaw nearly as wide as the cheekbones; the knowing closed-lip SMIRK (thin lips, corners up, deep
# lines from the nose round the mouth); SMALL crinkled eyes that half-smile; thick dark straight brows sitting low;
# a broad nose with a round tip; thick dark hair swept up and back in a high rounded dome, short and grey at the
# sides, the temples receding; a short beard, dark grey round the mouth, white on the long round chin.
# Chat 4 (13 Nov): the pear (temples narrowed to 0.69 of the cheeks) and the tall narrow quiff read as nobody; by eye
# on w02, w06, w09 his head is a BIG BOX: the hair makes the top as wide as the cheeks, the jaw square and wide.
# likeness.py check on w06 (13 Nov, measured on the clean face: the stubble's edge fooled the jaw and lip measures):
# 77%, none the wrong way, first in the line-up. The cocked brow above 0.015 made it read his eye corners as lifting.
P4.TUNE['walliams'] = dict(nose_long=0.0, chin_long=1.0, jaw_wide=8.0, face_wide=2.0, forehead_wide=5.0,
                           eyes_apart=6.0, eye_size=3.0, eye_open=1.0, eye_tilt=-3.0, mouth_wide=-2.0, lip_top=1.5,
                           lip_low=1.5, brow_high=3.0, brow_slope=-0.6)


def _lay(L):
    """By eye on w02, w06, w07 (the measures put the mouth just under the nose to make the long chin): the nose base
    at 0.6 of the face, the lips at 0.71-0.75, a long round chin below; the brows low over small eyes."""
    L = dict(L)
    L['nose_y'] = 0.61
    L['lip0'], L['lip13'], L['lip17'] = 0.765, 0.782, 0.808      # chat 4: the long gap nose to lip (his card)
    L['nw'] = max(L['nw'], 0.25)
    L['brow_y'] = L['eye_y'] - 0.048
    L['mw'] = min(L['mw'], 2 * L['ecx'] * 0.98)          # the mouth about as wide as the eye centres are apart
    return L


SHAVE = 'stubble'                 # 'stubble' or 'clean' (chat 4's blind tests)
LOW = 1.15                        # the lower face (below the cheekbones) stretched: his chin is his 98th-centile measure


def outline(L):
    """His big face: temples a little in, full round cheeks, a wide heavy jaw, a long, broad, rounded chin."""
    fw, jw, fh = L['fw'] * 0.5, L['jw'] * 0.5, L['fhw'] * 0.5
    jw = min(jw, fw * 0.98)                               # chat 4: a box, the jaw nearly as wide as the cheeks
    fh = max(fh, fw * 0.9)                                # the temples nearly as wide too (the hair squares it off)
    right = [(fh * 0.98, -0.02), (fh + 0.01, 0.14), (fw * 0.99, 0.36), (fw + 0.006, 0.52), (fw + 0.004, 0.66),
             (jw * 0.99, 0.8), (jw * 0.93, 0.92), (jw * 0.72, 1.0), (0.17, 1.05), (0.0, 1.058)]
    top = [(-fh * 0.75, -0.34), (0.0, -0.4), (fh * 0.75, -0.34)]
    right = [(u, v if v < 0.62 else 0.62 + (v - 0.62) * LOW) for u, v in right]   # chat 4: his long, heavy lower face
    left = [(-u, v) for u, v in right[::-1][1:]]
    return top + right + left


SKIN = (242, 190, 168)            # light and pink, a warm flush (w06: 249, 186, 169)
HAIR = (66, 54, 46)               # dark brown on top (w06, w09)
HAIR_L = (104, 86, 72)
HAIR_GREY = (92, 82, 74)       # the short sides, greying (w02, w07)
BROW = (56, 44, 38)
IRIS = (86, 66, 48)
LIP = (200, 130, 118)
# Blind test 2 (12 Nov): with a full white-chinned beard he was named as other bearded men; his famous face (w06,
# w09, his TV years) is near clean-shaven. So the beard is light stubble: a grey shade the skin shows through,
# a touch lighter on the chin, a touch darker round the mouth; the jaw, chin and smirk read through it.
BD_MID = blend(SKIN, (150, 142, 140), 0.22)       # stubble over the jaw and cheeks
BD_LIGHT = blend(SKIN, (200, 196, 194), 0.3)      # greyer-white on the chin
BD_MOUST = blend(SKIN, (120, 108, 100), 0.32)     # darker round the mouth
BD_GRAIN = blend(SKIN, (230, 228, 226), 0.5)
STUBBLE = BD_MID


# ---------------------------------------------------------------------------------------------- the beard
def beard(p, f, L, seed=61):
    """Short and two-tone (w02, w07, w10), Brand's way: a grey band along the jaw that turns white over the chin,
    a darker grey-brown moustache joining a goatee round the mouth; tufted edges on the cheeks; the cheeks above the
    jaw stay skin, so the round cheeks show."""
    fw, jw, ny, l0, l13, l17, mw, nw = L['fw'], L['jw'], L['nose_y'], L['lip0'], L['lip13'], L['lip17'], L['mw'], L['nw']
    jw = min(jw, fw * 0.98)                               # as outline() clamps it: no tufts outside the face
    o = outline(L)
    n = len(o)
    i0 = next(i for i, q in enumerate(o) if q[0] > 0 and q[1] > 0.6)           # down the right side ...
    i1 = next(i for i in range(n - 1, -1, -1) if o[i][0] < 0 and o[i][1] > 0.6)  # ... round the chin, up the left
    low = o[i0:i1 + 1]
    cheek = [(-jw * 0.5 - 0.01, 0.6), (-jw * 0.42, 0.68), (-mw * 0.8, l13 + 0.0), (-mw * 0.62, ny + 0.04),
             (0.0, ny + 0.035), (mw * 0.62, ny + 0.04), (mw * 0.8, l13 + 0.0), (jw * 0.42, 0.68), (jw * 0.5 + 0.01, 0.6)]
    top = AV.tufts(cheek, 0.01, 0.014, out=1.0, seed=seed)
    body = f.pts(low + top)
    p.poly(body, BD_MID, None)
    chin = AV.tufts([(jw * 0.46, 0.8), (mw * 0.55, l17 + 0.06), (0.0, l17 + 0.075), (-mw * 0.55, l17 + 0.06),
                     (-jw * 0.46, 0.8)], 0.012, 0.016, out=-1.0, seed=seed + 1)
    p.poly(f.pts([q for q in low if abs(q[0]) < jw * 0.47 and q[1] > 0.78] + chin[::-1]), BD_LIGHT, None)
    mt = l0 - 0.03                                       # a thin band over the lip (w02, w07), not the philtrum
    must = AV.tufts([(-mw * 0.6, l13 + 0.004), (-mw * 0.52, mt + 0.008), (-nw * 0.3, mt), (0.0, mt + 0.004),
                     (nw * 0.3, mt), (mw * 0.52, mt + 0.008), (mw * 0.6, l13 + 0.004)], 0.006, 0.012,
                    out=1.0, seed=seed + 2)
    goat = [(mw * 0.6, l13 + 0.01), (mw * 0.3, l17 + 0.012), (mw * 0.14, l17 + 0.045), (0.0, l17 + 0.05),
            (-mw * 0.14, l17 + 0.045), (-mw * 0.3, l17 + 0.012), (-mw * 0.6, l13 + 0.01)]
    p.poly(f.pts(must + AV.tufts(goat, 0.007, 0.012, out=-1.0, seed=seed + 3)), BD_MOUST, None)
    rng = np.random.default_rng(seed)
    for gv in np.arange(0.66, 1.0, 0.035):                # the grain: short light strokes on the grey
        for gu in np.arange(-fw * 0.5, fw * 0.5, 0.035):
            u, v = gu + rng.uniform(-0.012, 0.012), gv + rng.uniform(-0.012, 0.012)
            q = f(u, v)
            if not AV._inside(body, q[0], q[1]) or (abs(u) < mw * 0.62 and v < l17 + 0.055):
                continue
            q2 = f(u - u * 0.012, v + 0.02)
            p.line([q, q2], BD_GRAIN, 1.4)
    p.poly(curve(f.pts([(-mw * 0.5, l13), (mw * 0.5, l13), (mw * 0.4, l17 + 0.006), (0.0, l17 + 0.012),
                        (-mw * 0.4, l17 + 0.006)]), 3), SKIN, None)       # the lips' skin
    oo = curve(f.pts(o), 4)
    p.line(oo + oo[:1], INK, 2.6)                         # the face's ink back over the beard's edge


# ---------------------------------------------------------------------------------------------- the hair
def hair(p, f, L):
    """Chat 4 (13 Nov), by eye on w02, w06, w09: short, thick and dark, brushed UP at the front into a low, wide
    quiff and back over a flat-topped crown, as wide as the head (the box); the sides clipped close and greying,
    hugging the head down to the ears; the temples receding a little, so the high forehead shows."""
    e, c = L['fw'] * 0.5, L['fw'] * 0.5                 # the cap as wide as the cheeks: the box Sam liked
    hl = -0.1                                              # the hairline in the middle
    t = max(L['fhw'], L['fw'] * 0.9) * 0.5                    # the skin's temple (outline())
    side = [(-c - 0.03, -0.24), (-c - 0.03, -0.12), (-e - 0.02, 0.06), (-e - 0.014, 0.27), (-e + 0.01, 0.3),
            (-t + 0.0, 0.12), (-t + 0.03, -0.02), (-t + 0.06, -0.1), (-t + 0.08, -0.24)]   # Sam 13 Nov: run up
    # under the cap, so no gap is left at the temples between the skull and the hair          # the clipped grey sides fill out to the cap's width
    for sgn in (-1, 1):
        p.poly(curve(f.pts([(sgn * -u, v) for u, v in side] if sgn > 0 else side), 2), HAIR_GREY, INK, 2.2)
    top = [(-c - 0.035, -0.06), (-c - 0.04, -0.2), (-c + 0.0, -0.33), (-c * 0.55, -0.43), (-c * 0.15, -0.48),
           (c * 0.25, -0.47), (c * 0.62, -0.41), (c + 0.0, -0.32), (c + 0.04, -0.2), (c + 0.035, -0.06)]
    front = [(c - 0.01, -0.05), (c - 0.06, -0.16), (c * 0.62, -0.17), (c * 0.4, hl - 0.02), (c * 0.15, hl + 0.01),
             (-c * 0.15, hl + 0.012), (-c * 0.4, hl - 0.015), (-c * 0.62, -0.17), (-c + 0.06, -0.16),
             (-c + 0.01, -0.05)]                            # chat 4: the temples receding to an M (w02, w06)
    p.poly(curve(f.pts(AV.tufts(top, 0.008, 0.022, out=1.0, seed=52) + front), 2), HAIR, INK, 2.4)
    for k, (u, ln) in enumerate(((-0.24, 0.24), (-0.13, 0.3), (-0.03, 0.27), (0.08, 0.31), (0.18, 0.25),
                                 (0.27, 0.2))):           # brushed up and over to our right, uneven
        u *= c / 0.4
        p.line(curve(f.pts([(u, hl - 0.03), (u + 0.03, hl - 0.03 - ln * 0.6), (u + 0.08, hl - 0.03 - ln)]), 3),
               HAIR_L if k % 2 else dk(HAIR, 0.7), 1.6)
    p.poly(curve(f.pts([(-c * 0.3, hl - 0.04), (-c * 0.22, -0.3), (-c * 0.02, -0.41), (-c * 0.1, -0.29),
                        (-c * 0.14, hl - 0.04)]), 3), blend(HAIR, HAIR_L, 0.5), None)   # the light on the quiff


def long_nose(p, f, L, skin):
    """A broad nose, straight bridge and a round tip (w02, w06): the tip's ball and the wings, P4's nostrils."""
    nw, y = L['nw'], L['nose_y']
    sd = dk(skin, 0.76)
    p.line(curve(f.pts([(-0.03, L['eye_y'] + 0.02), (-0.04, (L['eye_y'] + y) / 2), (-nw * 0.24, y - 0.065)]), 3), sd, 1.7)
    p.line(curve(f.pts([(-nw * 0.26, y - 0.03), (-nw * 0.2, y - 0.075), (0.0, y - 0.088), (nw * 0.2, y - 0.075),
                        (nw * 0.26, y - 0.03)]), 4), dk(skin, 0.84), 1.5)
    P4.nose(p, f, L, skin)


def smirk_lines(p, f, L, skin, smile):
    """The deep lines from the nose wings round the mouth corners, and the round cheeks over them (w02, w06, w09);
    with smile > 0 they curl up into his knowing smirk."""
    nw, ny, mw, l13 = L['nw'], L['nose_y'], L['mw'], L['lip13']
    sd = dk(skin, 0.74)
    for sgn in (-1, 1):
        p.line(curve(f.pts([(sgn * nw * 0.56, ny - 0.03), (sgn * (mw * 0.62 + 0.02), ny + 0.05),
                            (sgn * (mw * 0.62 + 0.012), l13 + 0.04)]), 3), sd, 2.0)
        if smile > 0.2:                                   # the corner tucked in: a short curl (the dimple)
            p.line(curve(f.pts([(sgn * mw * 0.5, l13 - 0.012), (sgn * (mw * 0.56), l13 - 0.02),
                                (sgn * mw * 0.57, l13 + 0.008)]), 3), dk(skin, 0.7), 1.6)
        p.line(curve(f.pts([(sgn * L['fw'] * 0.36, 0.5), (sgn * L['fw'] * 0.3, 0.535), (sgn * nw * 0.7, 0.535)]), 3),
               dk(skin, 0.88), 1.4)                       # the top of the round cheek


def smirk(p, f, L, smile):
    """His closed-lip smirk (w02, w06, w09): the line a broad U, both corners lifted and tucked into the cheeks; a
    thin upper lip, a fuller lower one following the curve; smile 0..1 lifts the corners."""
    hw, l13 = L['mw'] / 2 * 1.2, L['lip13']
    up = 0.058 * smile
    us = np.linspace(-1, 1, 17)
    lop = lambda u: 1.0 + 0.6 * u                       # chat 4: lopsided, our right corner higher (w06, w09)
    yl = lambda u: l13 + 0.004 - up * u ** 4 * lop(u) - 0.008 * smile * u * u
    line = [(hw * u, yl(u)) for u in us]
    top = [(hw * u, yl(u) - 0.013 * (1 - u * u) ** 0.7) for u in us]
    bot = [(hw * u, yl(u) + 0.024 * (1 - u * u) ** 0.8) for u in us]
    p.poly(f.pts(top + line[::-1]), dk(LIP, 0.84), None)
    p.poly(f.pts(bot + line[::-1]), LIP, None)
    p.line(f.pts(bot[2:-2]), dk(LIP, 0.7), 1.2)
    p.line(f.pts(line), INK, 2.4)
    for sgn in (-1, 1):                                   # the corners tucked into the cheeks
        x0, y0 = sgn * hw, yl(sgn)
        p.line(curve(f.pts([(x0 - sgn * 0.004, y0 - 0.014), (x0 + sgn * 0.008, y0 - 0.002),
                            (x0 + sgn * 0.002, y0 + 0.012)]), 3), INK, 1.8)


def crinkles(p, f, L, skin, smile):
    """Small eyes that half-smile: bags under each eye and crow's feet at the outer corners."""
    sh = dk(skin, 0.8)
    for sgn in (-1, 1):
        cx, ey, w = sgn * L['ecx'], L['eye_y'], L['ew'] * 0.6
        k = max(smile, 0.0)                              # chat 4: the round cheeks push up under the eyes
        p.line(curve(f.pts([(cx - sgn * w * 0.8, ey + 0.03 - 0.01 * k), (cx, ey + 0.05 - 0.012 * k),
                            (cx + sgn * w * 1.0, ey + 0.05 - 0.012 * k)]), 3), sh, 1.8)   # outer end lower: the droop
        p.line(curve(f.pts([(cx - sgn * w, ey - 0.032), (cx, ey - 0.042), (cx + sgn * w * 1.15, ey + 0.004)]), 3),
               dk(skin, 0.86), 1.5)                       # the hood
        p.line(curve(f.pts([(cx - sgn * w * 0.5, ey + 0.075 - 0.01 * k), (cx + sgn * w * 0.2, ey + 0.085 - 0.012 * k),
                            (cx + sgn * w * 0.9, ey + 0.065 - 0.012 * k)]), 3), dk(skin, 0.86), 1.4)   # the bag
        if smile > 0.0:                                   # crow's feet, fanned (his twinkle)
            ox = cx + sgn * w * 1.2
            for dy in (-0.016, 0.004, 0.024):
                p.line(curve(f.pts([(ox, ey + dy * 0.3), (ox + sgn * 0.026, ey + dy * 1.2),
                                    (ox + sgn * 0.045, ey + dy * 2.0)]), 3), sh, 1.4)


# ---------------------------------------------------------------------------------------------- the mouth
def mouth(p, f, L, kind):
    """'grimace' (scared: wide and flat, the corners pulled out and down, both rows of teeth), 'gasp' (an open O)."""
    hw, l0, l13, l17 = L['mw'] / 2, L['lip0'], L['lip13'], L['lip17']
    if kind == 'gasp':
        x, y = f(0.0, (l13 + l17) / 2 + 0.01)
        rx, ry = hw * P4.H * 0.6, (l17 - l0) * P4.H * 0.9
        p.poly(oval(x, y, rx, ry, 24), (70, 26, 30), INK, 2.4)
        p.poly(oval(x, y + ry * 0.25, rx * 0.6, ry * 0.5, 20), (40, 14, 18), None)
        p.poly(oval(x, y - ry * 0.74, rx * 0.66, ry * 0.16, 14), (250, 248, 240), None)
        return
    hw *= 1.1
    pts = [(-hw, l13 + 0.02), (-hw * 0.5, l13 - 0.012), (0.0, l13 - 0.016), (hw * 0.5, l13 - 0.012), (hw, l13 + 0.02),
           (hw * 0.6, l17 + 0.022), (0.0, l17 + 0.028), (-hw * 0.6, l17 + 0.022)]
    p.poly(curve(f.pts(pts), 3), (70, 26, 30), INK, 2.4)
    p.poly(curve(f.pts([(-hw * 0.85, l13 + 0.012), (0.0, l13 - 0.01), (hw * 0.85, l13 + 0.012), (hw * 0.6, l13 + 0.03),
                        (0.0, l13 + 0.026), (-hw * 0.6, l13 + 0.03)]), 3), (250, 248, 240), None)    # top teeth
    p.poly(curve(f.pts([(-hw * 0.55, l17 + 0.006), (0.0, l17 + 0.0), (hw * 0.55, l17 + 0.006), (hw * 0.45, l17 + 0.02),
                        (0.0, l17 + 0.024), (-hw * 0.45, l17 + 0.02)]), 3), (240, 238, 230), None)   # bottom teeth
    p.line(curve(f.pts([(-hw * 0.7, l13 + 0.03), (0.0, l13 + 0.035), (hw * 0.7, l13 + 0.03)]), 3), (200, 196, 190), 1.2)


# ---------------------------------------------------------------------------------------------- his head
def walliams_head(img, p, sp, t, hx, hy):
    with BC._Big():
        return _head(img, p, sp, t, hx, BC._lift(hy))


def _head(img, p, sp, t, hx, hy):
    L = _lay(P4.layout(P4.target('walliams', sp.get('average', False))))
    f = P4.Face(hx, hy, 0.0, sp.get('turn', 0.0), sp.get('down', 0.0))
    look = MOODS.get(sp.get('mood', 'neutral'), MOODS['neutral'])
    smile = look.get('smile', 0.0) if look['mouth'] == 'lips' else -0.5
    AV._ears(p, f, L, SKIN)
    p.poly(curve(f.pts(outline(L)), 4), SKIN, INK, 2.6)
    if sp.get('shave', SHAVE) == 'stubble':
        beard(p, f, L)
    if sp.get('empty'):                                  # the likeness check's bare face
        long_nose(p, f, L, SKIN)
        P4.lips(p, f, L, dict(sp, smile=0.1), LIP, f(0.0, L['lip13']))
        hair(p, f, L)
        return f(0.0, L['lip13'])[0]
    smirk_lines(p, f, L, SKIN, smile)
    crinkles(p, f, L, SKIN, smile)
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', look['lid']), look=sp.get('look', 0.0),
                          squint=sp.get('squint', look.get('squint', 0.0)),
                          gaze_dy=BC.gaze(L, sp.get('gaze_dy', 0.0))), IRIS, dk(SKIN, 0.8), liner=3.0,
            wide=look['wide'])
    r = look['brow'] + sp.get('brow_up', 0.0)
    P4.brows(p, f, L, BROW, 0.052, (r + look.get('cock', 0.0), r), look['frown'] + sp.get('frown', 0.0))
    long_nose(p, f, L, SKIN)
    fx, my = f(0.0, L['lip13'])
    talking = str(sp.get('mouth', 'rest')).startswith('v:')
    if not talking and look['mouth'] == 'lips' and smile > 0.3:
        smirk(p, f, L, smile)
    elif talking or look['mouth'] == 'lips':
        P4.lips(p, f, L, dict(sp, smile=smile), LIP, (fx, my - 6))
    else:
        mouth(p, f, L, look['mouth'])
    hair(p, f, L)
    return fx


# ---------------------------------------------------------------------------------------------- the person
WALLIAMS = dict(who='walliams', name='David Walliams', neck_w=1.3, neck_shade=True, skin=SKIN, hw=66, hh=96, head_dy=10, hair='crop',
                hair_c=HAIR, brow_c=BROW, brow_w=4.6, outfit='jumper', jacket=BC.TRACK, sleeve=BC.TRACK,
                trousers=BC.TRACK, shirt=BC.TRACK, tie=None, shoe=(236, 236, 236), shoulders=158, full=True,
                pose='custom', height=1.96, seed=95, look_='prison', mood='scared')
TC.HEADS['walliams'] = walliams_head
TC.TORSOS['walliams'] = BC.brand_torso           # look_='prison': the tracksuit's collar and zip
BC.FACE_HEADS.add(walliams_head)                 # he has a mouth at rest (blessed_cast.mouth_faults)
BC.CAST['walliams'] = WALLIAMS


# ---------------------------------------------------------------------------------------------- sheets
def head_png(out, average=False, mood='neutral', bare=False):
    """His head straight on, as likeness.py check wants it (the bare face; --average: the average face, the bias).
    --bare: the head only, cut at the chin (nametest.py: the tracksuit's zip collar made the blind helper say
    Zelensky)."""
    B.SS = 1
    im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    V.person(im, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(WALLIAMS, average=average, mood=mood), 0.0, 0)
    bot = 1250
    if bare:                                             # cut just under the chin: the first ink below the mouth
        a = np.asarray(im.convert('RGB')).astype(int).sum(2)[:, 540]
        bot = next(y for y in range(800, 1250) if a[y] < 200 and a[y - 12] > 300) + 3
    im.crop((180, 300, 900, bot)).convert('RGB').save(out)
    return out


def faces_sheet(out):
    """His face large in each mood, two photos beside (rule 76)."""
    B.SS = 1
    tw, th = 420, 520
    img = Image.new('RGB', (tw * 6, th + 50), (232, 228, 222))
    d = ImageDraw.Draw(img)
    refs = os.path.join(HERE, '..', 'references', 'blessed', 'likeness')
    for i, name in enumerate(('w06-front-hedge-sam.jpg', 'w02-front-bbc2024.jpg')):
        ph = Image.open(os.path.join(refs, name)).convert('RGB')
        ph.thumbnail((tw - 10, th - 10))
        img.paste(ph, (i * tw + 5, 45))
        d.text((i * tw + 8, 10), name[:3] + ' (photo)', font=BC._font(26), fill=(30, 30, 30))
    for j, mood in enumerate(('neutral', 'scared', 'alarmed', 'pleading')):
        im = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
        V.person(im, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(WALLIAMS, mood=mood), 0.0, 0)
        tile = im.crop((180, 280, 900, 1170)).convert('RGB')
        tile.thumbnail((tw - 10, th - 10))
        x = (j + 2) * tw
        img.paste(tile, (x + 5, 45))
        d.text((x + 8, 10), mood, font=BC._font(26), fill=(30, 30, 30))
    img.save(out, quality=88)
    return out


if __name__ == '__main__':
    if '--clean' in sys.argv:
        SHAVE = 'clean'
    if sys.argv[1] == 'head':
        mood = sys.argv[sys.argv.index('--mood') + 1] if '--mood' in sys.argv else 'neutral'
        print(head_png(sys.argv[2], '--average' in sys.argv, mood, '--bare' in sys.argv))
    elif sys.argv[1] == 'faces':
        print(faces_sheet(sys.argv[2]))
