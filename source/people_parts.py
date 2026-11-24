#!/usr/bin/env python3
"""MAP  The people kit's drawing parts (ranking item 4, overnight chat 4, 14 Nov), LIFTED out of blessed_cast.py
unchanged in look: every invented face is the average face (patriots4) pushed its own way, at the house's bigger
head size, with lips, brows, a nose, ears, eye bags, shaped hair, stubble or a beard, glasses, freckles. A person's
face card rides in their own spec (sp['kit_face']), so nothing is keyed by name. people.py reads the descriptions
and hangs these parts on the engine; no film imports this file until Sam approves the kit.

Map: gaze 23 | head size 31 | outline 49 | hair cap 62 | torsos (robe, officer; their backs, the open collar: chat 15) 70 | wig | the front face 129 |
     hair mass 241 | hair front 279 | glasses 313
"""
import math

import numpy as np

import body as B                       # noqa: E402  the people engine
import views as V                      # noqa: E402  every view of a person
import faces as FA                     # noqa: E402  the measured face layout and its parts
from faces import dk                   # noqa: E402
from ink import INK, curve, oval, open_curve  # noqa: E402
import turnhead as TH  # noqa: E402
import focus as FO  # noqa: E402  (C2, 19 Nov: where a front-on face looks)

LONG_STYLES = ('bob', 'long', 'curly', 'bun', 'shag')   # hair that has a mass behind the head, drawn before it


def gaze(L, g):
    """This film's gaze_dy is a share of the eye's half-height (-1 up .. 1 down); traitors_cast.eye takes drawing units
    (found 11 Nov, cast chat 8: -0.7 moved the pupils under a pixel, so no planned eye move showed)."""
    eh = (L['eh'] if L else 0.0508) * FA.H / 1.8
    return g * eh * 0.85



HEAD_K = 1.15        # Sam, 11 Nov (cast sheet): "a small-looking head": his face drawn 15% bigger, grown up from the chin


class _Big:
    """While drawing his head, the face height (patriots4's and turnhead's H) is HEAD_K times the house size."""
    def __enter__(self):
        self.old = (FA.H, TH.H)
        FA.H = TH.H = 172.0 * HEAD_K

    def __exit__(self, *a):
        FA.H, TH.H = self.old


def _lift(hy):
    """The head's anchor moved up so the bigger face grows upwards: the chin drops only a little onto the neck."""
    return hy - (HEAD_K - 1) * 172.0 * 0.85


# Bald heads (Sam, 16 Nov: "their heads end up massive and strange-looking"; Blessed's jury, Protest Tiers' Germany).
# Why: a bald head showed the skull drawn for hair. Its top was the face outline's crown, a narrow point made to sit
# hidden under a haircut (a tall egg), and the whole skull was the hair's outer size (crown -0.42, where a crop's hair
# ends). Blessed patched it by shrinking the whole face 14% (note 14's 'k'). The fix: a bald or receding head's skull
# is a round dome as wide as the temples (turnhead's own dome, the shape the turned views already use) whose crown sits
# a crop's thickness lower (SKULL_CROWN); ears, jaw and face unchanged; a gentle shine. Opt-in: a film turns it on with
# TRUE_SKULL = True (Protest Tiers, chat O5); off, every film draws exactly as before.
TRUE_SKULL = False
SKULL_CROWN = -0.30          # the bare skull's crown (face heights above the top of the forehead); hair's is -0.42
BARE = ('bald', 'receding')


def bare_skull(fc):
    return TRUE_SKULL and fc.get('hair') in BARE


def _dome_outline(L, crown=SKULL_CROWN):
    """_outline with its top replaced by the skull's round dome: turnhead's crown (a near-circle to the temples),
    squeezed to this crown and widened to this face's temples, joined to the face's own sides at the forehead."""
    side = [q for q in _outline(L) if q[1] >= 0.0 and q[0] > 0]          # the right side from the temple down
    w0 = L['fhw'] * 0.5 * 0.93                                             # the temple: outline_uv's (fhw/2*.93, 0)
    T = TH.TEMPLATE['crown']
    t0, tw = T[0][0], T[-1][1]
    top = [(w0 * z / tw, v / t0 * crown) for v, z in T if v < 0.0]       # crown (u=0) to just above the temple
    right = top + side                                                     # crown, round the right, to the chin
    return right + [(0.0, 1.0)] + [(-u, v) for u, v in right[::-1] if u > 1e-6]


def _outline(L, crown=-0.42):
    """FA.outline_uv without its fold: that list runs out to the upper-left temple and back and repeats the left
    temple point, so the smoothing folds the left forehead into a notch (Sam, 11 Nov: "strange ridges on the left
    side"). Here: once round, crown first, both temples alike."""
    pts = FA.outline_uv(L, 0.4, crown=crown)[2:]               # from the crown: right side, chin, left side
    out = []
    for q in pts:
        if not out or abs(q[0] - out[-1][0]) + abs(q[1] - out[-1][1]) > 1e-6:
            out.append(q)
    return [out[0], (-pts[-1][0], pts[-1][1])] + out[1:]       # the right upper temple, as the left has



def _press_cap(L, hl):
    e, c = L['fw'] * 0.5, L['fhw'] * 0.5
    return [(-e - 0.02, 0.36), (-e - 0.03, 0.02), (-e + 0.04, -0.24), (-0.24, -0.4), (0.0, -0.45), (0.24, -0.4),
            (e - 0.04, -0.24), (e + 0.03, 0.02), (e + 0.02, 0.36), (e - 0.03, 0.34), (c + 0.01, 0.12), (c - 0.03, 0.02),
            (c * 0.7, hl), (0.0, hl - 0.012), (-c * 0.7, hl), (-c + 0.03, 0.02), (-c - 0.01, 0.12), (-e + 0.03, 0.34)]



def robe_torso(img, p, sp, t):
    """The red robe's black-trimmed front, white bands at the throat, a black sash over the shoulder."""
    sw = sp.get('shoulders', 160)
    p.poly([(-40, -4), (40, -4), (32, 40), (-32, 40)], (246, 246, 246), INK, 2.0)
    p.poly([(-12, 30), (-2, 30), (-4, 96), (-14, 96)], (250, 250, 250), INK, 1.6)              # the bands
    p.poly([(2, 30), (12, 30), (14, 96), (4, 96)], (250, 250, 250), INK, 1.6)
    for sgn in (-1, 1):                                                                       # fur-trimmed front
        p.poly([(sgn * 30, 30), (sgn * 52, 34), (sgn * 30, 560), (sgn * 12, 560)], (238, 232, 222), INK, 2.0)
    p.poly([(-sw * 0.9, 20), (-sw * 0.6, 4), (sw * 0.2, 300), (sw * 0.1, 340)], (24, 22, 24), INK, 2.0)  # the sash


def officer_torso(img, p, sp, t):
    """HMPPS officer: white shirt, black tie, black epaulettes, a black belt with a key chain."""
    sw = sp.get('shoulders', 160)
    for sgn in (-1, 1):                                                                       # the shirt collar
        p.poly([(sgn * 6, 4), (sgn * 40, -6), (sgn * 34, 26), (sgn * 12, 30)], (250, 250, 250), INK, 1.8)
    p.poly([(-10, 10), (10, 10), (14, 300), (0, 330), (-14, 300)], (20, 20, 24), INK, 1.6)      # the tie
    p.line([(0, 330), (0, 470)], (200, 200, 204), 1.6)                                          # the placket
    for sgn in (-1, 1):
        p.poly([(sgn * sw * 0.35, 10), (sgn * sw * 0.85, 26), (sgn * sw * 0.85, 46), (sgn * sw * 0.35, 30)],
               (20, 20, 24), INK, 1.6)
    p.poly([(-sw * 0.98, 466), (sw * 0.98, 466), (sw * 0.98, 496), (-sw * 0.98, 496)], (20, 20, 24), INK, 1.6)
    p.line(curve([(sw * 0.5, 500), (sw * 0.58, 560), (sw * 0.66, 520)], 3), (190, 190, 196), 2.4)
    p.ell(sw * 0.62, 566, 9, 9, None, (190, 190, 196), 2.4)
    p.poly([(-sw * 0.62, 96), (-sw * 0.32, 96), (-sw * 0.32, 130), (-sw * 0.62, 130)], (240, 240, 240), INK, 1.2)  # badge
    p.poly([(sw * 0.3, 70), (sw * 0.62, 70), (sw * 0.62, 176), (sw * 0.3, 176)], (20, 20, 24), INK, 1.6)  # note 28:
    p.line([(sw * 0.38, 70), (sw * 0.38, 20)], (20, 20, 24), 4.0)                     # a radio clipped at the chest
    p.poly([(sw * 0.35, 96), (sw * 0.57, 96), (sw * 0.57, 128), (sw * 0.35, 128)], (90, 96, 104), None)


def robe_back(img, p, sp, t):
    """The robe from behind (face tool chat 15: one outfit in every view): the black sash coming over the shoulder
    and across the back to the other hip (the back's own units: as seen from behind)."""
    sw = sp.get('shoulders', 160)
    p.poly([(sw * 0.9, 20), (sw * 0.6, 4), (-sw * 0.2, 300), (-sw * 0.1, 340)], (24, 22, 24), INK, 2.0)


def officer_back(img, p, sp, t):
    """HMPPS officer from behind (chat 15): the black belt all round, the black epaulettes on the shoulders."""
    sw = sp.get('shoulders', 160)
    p.poly([(-sw * 0.98, 466), (sw * 0.98, 466), (sw * 0.98, 496), (-sw * 0.98, 496)], (20, 20, 24), INK, 1.6)
    for sgn in (-1, 1):
        p.poly([(sgn * sw * 0.35, 10), (sgn * sw * 0.85, 26), (sgn * sw * 0.85, 46), (sgn * sw * 0.35, 30)],
               (20, 20, 24), INK, 1.6)


def open_collar(p, cx, yc, nw, skin, sc):
    """The open shirt collar at the neck's foot (face tool chat 9, Sam: "look closely at the neckline"; an outfit
    choice since chat 15, `outfit: suit .., no tie, open collar`, was in the braids code): the skin runs on down from
    the neck in a V to the top button, and the two collar flaps lie over the lapels either side, so the neck no
    longer stops at a flat shirt edge, steps in at its foot, or leaves white bars out at the sides."""
    w = 36 * nw
    p.poly([(cx - w, yc - 2), (cx + w, yc - 2), (cx + 4, 56), (cx - 4, 56)], skin, None)
    for sg in (-1, 1):
        p.poly([(cx + sg * (w + 1), yc - 3), (cx - sg * 1, 62), (cx + sg * 22, 70), (cx + sg * 60, 6),
                (cx + sg * (w + 16), yc - 4)], sc, INK, 2.0)


def open_collar_three(p, sp, nw, skin, sc, yc=-11.0):
    """The open collar from three-quarter (face tool chat 12, Sam: "Kemi's correct outfit is replaced by her
    previous one in her 3/4 pose"): the skin V from the neck's foot down to the top button on the chest's centre
    (views' three-quarter V, `v_at`), the near flap over the near lapel, the far one foreshortened."""
    sw = sp.get('shoulders', 150)
    o = sp.get('v_at', 0.24 * sw)
    nl, nr = -20.0 * nw, 44.0 * nw - 8 * (nw - 1)           # the three-quarter neck's foot, at her neck_w
    p.poly([(nl, yc - 2), (nr, yc - 2), (o + 4, 56), (o - 4, 56)], skin, None)
    for sg, tx, k in ((-1, nl, 1.0), (1, nr, 0.55)):
        p.poly([(tx + sg * 1, yc - 3), (o - sg * 1, 62), (o + sg * 22 * k, 70), (tx + sg * 24 * k, 6),
                (tx + sg * 16 * k, yc - 4)], sc, INK, 2.0)


def collar_torso(img, p, sp, t):
    """The open collar on the front torso, as an outfit piece (the neck's foot at the house's -11)."""
    open_collar(p, 0.0, -11.0, sp.get('neck_w', 1.0), sp['skin'], sp.get('shirt', (246, 246, 246)))


def collar_three(img, p, sp, t):
    open_collar_three(p, sp, sp.get('neck_w', 1.0), sp['skin'], sp.get('shirt', (246, 246, 246)))


WIG_K = (1.42, 1.0, -62)    # (width, height, shift down) of the wig on the front face


def wig_head(img, p, sp, t, hx, hy):
    """The library's head (bald under the wig) with a short white bench wig: rows of rolled curls over the crown,
    a roll over each ear (the courtroom sketches 05, 07, 11)."""
    fx = front_head(img, p, sp, t, hx, hy)             # notes 13, 15: the front face with lips (was the house head)
    hw, hh = sp.get('hw', 70) * WIG_K[0], sp.get('hh', 90) * WIG_K[1]   # the wig sized to that bigger face
    hy = hy + WIG_K[2]
    W, Wd = (240, 238, 230), (196, 192, 182)
    cap = curve([(hx - hw - 8, hy + 6), (hx - hw - 10, hy - hh * 0.5), (hx - hw * 0.5, hy - hh - 14), (hx, hy - hh - 20),
                 (hx + hw * 0.5, hy - hh - 14), (hx + hw + 10, hy - hh * 0.5), (hx + hw + 8, hy + 6),
                 (hx + hw - 4, hy - hh * 0.45), (hx, hy - hh * 0.62), (hx - hw + 4, hy - hh * 0.45)], 3)
    p.poly(cap, W, INK, 2.4)
    for r, y in enumerate((hy - hh * 0.85, hy - hh * 0.68)):        # the rows of rolled curls
        for k in range(-3, 4):
            x = hx + k * hw * 0.28 + (hw * 0.14 if r else 0)
            if abs(x - hx) < hw * 0.95:
                p.line(oval(x, y, 9, 6, 10, 0.3, math.pi * 1.7), Wd, 1.6)
    for sgn in (-1, 1):                                              # a roll over each ear
        x = hx + sgn * (hw + 6)
        for k in range(3):
            p.ell(x, hy - 4 + k * 16, 12, 9, W, INK, 1.8)
    return fx





def face_layout(fc):
    m = dict(FA.AVG)
    for k, v in fc["m"].items():
        m[k] = m[k] + v
    return FA.layout(m)


def _lop_brows(sp, r):
    """Job K 5 (Sam: Y, 11 Nov): an invented face may be a touch uneven (sp['lopsided']): our left brow higher. The
    mouth corner comes from faces.lips; a likeness head never reads it."""
    b = FA.lop(sp).get('brow', 0.0)
    return (r + b, r - 0.004) if b else r


def front_head(img, p, sp, t, hx, hy):
    """An invented face, front on (blessed_cast's inmate head, lifted): the face card is sp['kit_face']."""
    k = sp['kit_face'].get('k', 1.0)          # note 14: a face may be drawn smaller than the house's bigger size
    with _Big():
        FA.H, TH.H = FA.H * k, TH.H * k
        return _front_head(img, p, sp, t, hx, hy - (HEAD_K * k - 1) * 172.0 * 0.85)


def _front_head(img, p, sp, t, hx, hy):
    who = sp['who']
    fc = sp['kit_face']
    L = face_layout(fc)
    up = max(0.0, -sp.get('gaze_dy', 0.0))                 # looking up at the TV: the face tips up a little
    gw = (L['ew'] * (0.86 if fc.get('glasses_thick') else 0.78)) if fc.get('glasses') else L['ew'] * 0.5
    FF = FO.Focus(FA.Face(hx, hy, down=-0.8 * up), sp, L, L['fw'] * 0.5 - L['ecx'] - gw - 0.012)   # C2 (19 Nov): where
    #                                                         they look (focus.py); off at focus 0
    f = FF.whole
    skin, hc = sp['skin'], sp.get('hair_c', (40, 32, 28))
    fw, fhw = L['fw'], L['fhw']
    e, c = fw * 0.5, fhw * 0.5
    if fc['hair'] in LONG_STYLES:
        _hair_mass(p, f, L, fc, hc)
    if fc['hair'] not in ('bob', 'long', 'curly', 'shag'):
        FA.ears(p, FF.ears, L, skin)
    outl = _dome_outline(L) if bare_skull(fc) else _outline(L)
    p.poly(curve(f.pts(outl), 4), skin, INK, 2.6)
    jaw = [(-e, 0.5), (-L['jw'] * 0.5, 0.82), (-0.08, 0.98), (0.0, 1.0), (0.08, 0.98), (L['jw'] * 0.5, 0.82), (e, 0.5),
           (e * 0.7, 0.62), (L['mw'] * 0.75, L['lip17'] + 0.04), (0.0, L['lip17'] + 0.03),
           (-L['mw'] * 0.75, L['lip17'] + 0.04), (-e * 0.7, 0.62)]
    if fc.get('stub'):                                        # stubble: a shade over the jaw and the upper lip
        p.poly(curve(f.pts(jaw), 3), dk(skin, fc['stub']), None)
        p.poly(curve(FF.mouth.pts([(-L['mw'] * 0.6, L['lip0'] - 0.005), (0.0, L['nose_y'] + 0.01),
                            (L['mw'] * 0.6, L['lip0'] - 0.005), (0.0, L['lip0'] + 0.01)]), 3), dk(skin, fc['stub']), None)
        rng = np.random.default_rng(len(who))
        light = fc['stub'] >= 0.9                          # a very light fade (GTA chat 9, Jason): finer, fainter
        for _ in range(110 if light else 60):
            u, v = rng.uniform(-e * 0.8, e * 0.8), rng.uniform(0.62 if light else 0.7, 0.96)
            if abs(u) < L['jw'] * 0.5 * (1.0 - (v - 0.82) * 2.2):
                p.poly(oval(*f(u, v), *((1.0, 1.0) if light else (1.6, 1.6)), 6),
                       dk(skin, fc['stub'] - (0.06 if light else 0.12)), None)
        o = curve(f.pts(outl), 4)                             # the face's ink back over the stubble's edge (line-work
        p.line(o + o[:1], INK, 2.6)                           # check, chat 3: the jaw lost its outline)
    if fc.get('beard'):                                       # a short boxed beard and a moustache
        b = fc['beard']
        p.poly(curve(f.pts(jaw), 3), b, INK, 1.6)
        p.poly(curve(FF.mouth.pts([(-L['mw'] * 0.72, L['lip13'] + 0.02), (-L['mw'] * 0.6, L['lip0'] - 0.01),
                            (0.0, L['nose_y'] + 0.012), (L['mw'] * 0.6, L['lip0'] - 0.01),
                            (L['mw'] * 0.72, L['lip13'] + 0.02), (L['mw'] * 0.5, L['lip0'] + 0.006),
                            (0.0, L['lip0'] - 0.002), (-L['mw'] * 0.5, L['lip0'] + 0.006)]), 3), b, INK, 1.4)
        rng = np.random.default_rng(7)
        for _ in range(40):
            u, v = rng.uniform(-e * 0.8, e * 0.8), rng.uniform(0.72, 0.95)
            if abs(u) < L['jw'] * 0.5 * (1.0 - (v - 0.82) * 2.2) and abs(u) > L['mw'] * 0.6:
                p.line([f(u, v), f(u + 0.004, v + 0.02)], (120, 116, 112), 1.4)       # flecks of grey
    face_detail(p, FF.lines, L, fc, skin)
    if fc.get('freckles'):
        rng = np.random.default_rng(31)
        for _ in range(22):
            sgn = 1 if rng.random() < 0.5 else -1
            u, v = sgn * rng.uniform(L['nw'] * 0.4, L['ecx'] + 0.04), rng.uniform(L['eye_y'] + 0.08, L['nose_y'])
            p.poly(oval(*FF.lines(u, v), 2.0, 2.0, 6), dk(skin, 0.74), None)
    FA.eyes(p, FF.eyes, L, dict(sp, lid4=sp.get('lid4', 0.22 - 0.2 * up), gaze_dy=gaze(L, -up), look=FO.look(sp)), fc['iris'], dk(skin, 0.8),
            liner=2.6)
    if fc.get('lashes'):                                      # GTA (Lucia): a heavier upper lid and two flicks out
        for sgn in (-1, 1):
            cx, cy = sgn * L['ecx'], L['eye_y']
            p.line(curve(FF.eyes.pts([(cx - sgn * L['ew'] * 0.85, cy - L['eh'] * 0.35), (cx, cy - L['eh'] * 0.78),
                                      (cx + sgn * L['ew'] * 1.08, cy - L['eh'] * 0.3)]), 3), INK, 3.0)
            for k in range(2):
                a = (cx + sgn * L['ew'] * (0.75 + 0.25 * k), cy - L['eh'] * (0.75 - 0.25 * k))
                b = (a[0] + sgn * L['ew'] * 0.2, a[1] - L['eh'] * 0.3)
                p.line(FF.eyes.pts([a, b]), INK, 2.2)
    if fc.get('pencil'):                                      # a pencil moustache: one thin line above the lip
        pencil(p, FF.mouth, L, fc)
    if fc.get('glasses'):
        _glasses(p, FF.lens, L, fc['glasses'], fc.get('glasses_thick'))
    FA.brows(p, FF.brows, L, fc['brow'], fc.get('brow_thick', 0.05 if fc['hair'] != 'side' else 0.04),
             _lop_brows(sp, sp.get('brow_up', 0.012 * up)), sp.get('frown', 0.0))
    FA.nose(p, FF.nose, L, skin)
    fx, my = FF.mouth(0.0, L['lip13'])
    FA.lips(p, FF.mouth, L, dict(sp, smile=sp.get('smile', -0.4)), fc['lip'], (fx, my - 6))
    hl = -0.06
    if fc['hair'] in LONG_STYLES + ('receding', 'pony'):
        _hair_front(p, f, L, fc, hc, skin)
    elif fc['hair'] == 'crop' and fc.get('hair_buzz'):         # GTA chat 9 (Jason): a buzz cut
        buzz_front(p, f, L, hc)
    elif fc['hair'] == 'crop':                                  # a short crop: a low straight hairline, the skull's shape
        crop_front(p, f, L, hc, hl)
    elif fc['hair'] == 'none':                                # under a wig (the judge): the wig is drawn after
        pass
    elif fc['hair'] == 'bald':                                # shaved: a shine on the dome, dark short sides
        for sgn in (-1, 1):
            side = [(sgn * (e + 0.015), 0.46), (sgn * (e + 0.02), 0.1), (sgn * (c + 0.01), -0.12),
                    (sgn * (c - 0.04), -0.08), (sgn * (e - 0.03), 0.12), (sgn * (e - 0.02), 0.4)]
            p.poly(curve(f.pts(side), 3), hc, INK, 1.6)
        if bare_skull(fc):                                    # the shine where the lower dome turns over
            p.poly(oval(*f(0.1, SKULL_CROWN * 0.72), 15, 7, 16, -0.3), B.lt(skin, 1.18), None)
        else:
            p.poly(oval(*f(0.1, -0.3), 18, 9, 16, -0.3), B.lt(skin, 1.3), None)
    else:                                                     # side parting on our left, the fringe swept across
        cap = [(-e - 0.01, 0.32), (-e - 0.025, 0.02), (-e + 0.03, -0.26), (-0.22, -0.43), (0.02, -0.47), (0.26, -0.41),
               (e - 0.02, -0.22), (e + 0.025, 0.04), (e + 0.01, 0.32), (e - 0.025, 0.3), (c, 0.08), (c * 0.6, 0.0),
               (0.1, -0.03), (-0.1, -0.06), (-c * 0.7, -0.1), (-c + 0.02, 0.04), (-e + 0.01, 0.34)]
        p.poly(curve(f.pts(cap), 2), hc, INK, 2.4)
        p.line(curve(f.pts([(-0.16, -0.42), (-0.15, -0.26), (-0.14, -0.14)]), 3), dk(hc, 0.6), 1.8)   # the parting
        for k in range(6):                                    # strands swept from the parting to our right
            u0 = -0.12 + 0.07 * k
            p.line(curve(f.pts([(u0, -0.36 + 0.02 * k), (u0 + 0.08, -0.2), (u0 + 0.13, -0.04 + 0.01 * k)]), 3),
                   dk(hc, 0.72), 1.4)
    if fc.get('piercings'):                                   # Milburn note 2 (17 Nov): drawn last, over the fringe
        piercings(p, FF.marks, L, fc, sp.get('brow_up', 0.012 * up), sp.get('frown', 0.0))
    return fx


# ---- One source for every view (proposal three-quarter-people, adopted 18 Nov): the front's own part code, called
# by the front head here and by the turned head (people_turned) on its 3D head (turnhead.TurnFace has the same
# f(u, v) / f.pts as the front's Face). `seen(u, v)` (turned only) leaves out a mark on the far side of the head.
def _all_seen(u, v):
    return True


def face_detail(p, f, L, fc, skin, seen=_all_seen):
    """Eye bags, the smile folds, a chin dimple. 'soft' (GTA, 20 Nov: a young, pretty face): no eye bags, the smile
    folds short and faint."""
    sh = dk(skin, 0.84)
    soft = fc.get('soft')
    for sgn in (-1, 1):
        cx, ey, w = sgn * L['ecx'], L['eye_y'], L['ew'] * 0.6
        if soft:
            if seen(sgn * L['mw'] * 0.7, L['lip0']):
                p.line(curve(f.pts([(sgn * L['nw'] * 0.75, L['nose_y'] + 0.0), (sgn * L['mw'] * 0.72, L['lip0'])]), 3),
                       dk(skin, 0.88), 1.2)
            continue
        if seen(cx, ey + 0.06):
            p.line(curve(f.pts([(cx - w * 0.6, ey + 0.05), (cx, ey + 0.064), (cx + w * 0.7, ey + 0.046)]), 3), sh, 1.5)
        if seen(sgn * L['mw'] * 0.7, L['lip0']):
            p.line(curve(f.pts([(sgn * L['nw'] * 0.62, L['nose_y'] - 0.03), (sgn * L['mw'] * 0.7, L['lip0'] + 0.01),
                                (sgn * L['mw'] * 0.76, L['lip13'] + 0.03)]), 3), dk(skin, 0.78), 1.6)
    if not fc.get('beard') and not soft and seen(0.0, 0.93):
        p.line(curve(f.pts([(-0.025, 0.93), (0.0, 0.94), (0.025, 0.93)]), 3), dk(skin, 0.8), 1.4)


def pencil(p, f, L, fc):
    """A pencil moustache: one thin line above the lip."""
    y = (L['lip0'] + L['nose_y']) * 0.5 + 0.008
    p.poly(curve(f.pts([(-L['mw'] * 0.62, y + 0.01), (0.0, y - 0.004), (L['mw'] * 0.62, y + 0.01),
                        (0.0, y + 0.008)]), 3), fc['pencil'], None)


def crop_cap(L, hl=-0.06):
    e, c = L['fw'] * 0.5, L['fhw'] * 0.5
    return [(-e - 0.01, 0.3), (-e - 0.02, 0.04), (-e + 0.04, -0.22), (-0.24, -0.38), (0.0, -0.43), (0.24, -0.38),
            (e - 0.04, -0.22), (e + 0.02, 0.04), (e + 0.01, 0.3), (e - 0.02, 0.3), (c + 0.01, 0.12), (c - 0.03, 0.02),
            (c * 0.7, hl), (0.0, hl - 0.012), (-c * 0.7, hl), (-c + 0.03, 0.02), (-c - 0.01, 0.12), (-e + 0.02, 0.3)]


def crop_front(p, f, L, hc, hl=-0.06, fill=True):
    """A short crop: a low straight hairline, the skull's shape, its texture in short strokes."""
    c = L['fhw'] * 0.5
    if fill:
        p.poly(curve(f.pts(crop_cap(L, hl)), 2), hc, INK, 2.4)
    rng = np.random.default_rng(5)
    for _ in range(36):                                   # the crop's texture: short strokes
        u, v = rng.uniform(-c, c), rng.uniform(-0.36, hl - 0.03)
        if abs(u) < c * (1.0 - max(0.0, -v - 0.25) * 2.0):
            p.line([f(u, v), f(u + 0.008, v + 0.025)], B.lt(hc, 1.7), 1.4)


def buzz_front(p, f, L, hc, hl=-0.08):
    """A buzz cut (GTA chat 9, Jason; Sam: "his hair should be a buzz"): the crop's cap hugging the skull, the skin
    showing through (the colour is set lighter in people.py), a fine stipple instead of strokes, a soft hairline."""
    c = L['fhw'] * 0.5
    cap = crop_cap(L, hl)
    cap = [(u, v + 0.03 if v < -0.3 else v) for u, v in cap]         # no height over the skull: it hugs the dome
    p.poly(curve(f.pts(cap), 2), hc, INK, 1.8)
    rng = np.random.default_rng(7)
    for _ in range(90):                                   # the stubble of a buzz: fine dots
        u, v = rng.uniform(-c, c), rng.uniform(-0.36, hl - 0.02)
        if abs(u) < c * (1.0 - max(0.0, -v - 0.25) * 2.0):
            x, y = f(u, v)
            p.poly(oval(x, y, 1.3, 1.3, 6), dk(hc, 0.72), None)


SILVER = (214, 218, 226)


def _bead(p, xy, r):
    """One silver ball: ink rim, a white glint up-left (reads as metal at phone size)."""
    p.poly(oval(*xy, r, r, 10), SILVER, INK, 1.0)
    p.poly(oval(xy[0] - r * 0.35, xy[1] - r * 0.35, r * 0.4, r * 0.4, 6), (255, 255, 255), None)


def piercings(p, f, L, fc, raise_=0.0, frown=0.0, seen=_all_seen):
    """`piercings: brow, lip, nose` (any of them; bare `piercings` = all three), silver, front head (Milburn note 2):
    a bar through the outer end of her left brow (our right) with a ball each side, a hoop through the lower lip off
    centre (our left), a stud on the nostril wing (our right)."""
    which = fc['piercings']
    thick = fc.get('brow_thick', 0.05)
    k = max(1.0, abs(f(1.0, 0.0)[0] - f(0.0, 0.0)[0]) / 100.0)   # sizes grow with the face (phone size, 2a's close)
    if 'brow' in which:
        up = raise_[1] if isinstance(raise_, (tuple, list)) else raise_
        uv = FA.brow_uv(L, thick, up, frown)
        (xm, ym), (xo, yo) = uv[1], uv[2]
        u = xm + (xo - xm) * 0.62
        v = ym + (yo - ym) * 0.62
        if not seen(u, v):
            which = [w for w in which if w != 'brow']
    if 'brow' in which:
        a, b = f(u - 0.008, v - thick * 0.75), f(u + 0.008, v + thick * 1.05)
        p.line([a, b], INK, 2.6 * k)
        p.line([a, b], SILVER, 1.4 * k)
        _bead(p, a, 2.8 * k)
        _bead(p, b, 2.8 * k)
    if 'lip' in which and seen(-L['mw'] * 0.26, L['lip17']):
        r = 4.2 * k
        cx, cy = f(-L['mw'] * 0.26, L['lip17'])
        cy -= r * 0.25                               # the ring's top runs into the lower lip, the rest hangs below
        ring = [(cx + r * math.sin(a), cy + r * math.cos(a)) for a in np.linspace(-2.5, 2.5, 20)]
        p.line(ring, INK, 3.2 * k)
        p.line(ring, SILVER, 1.8 * k)
        p.poly(oval(cx - r * 0.5, cy + r * 0.6, 0.8 * k, 0.8 * k, 6), (255, 255, 255), None)
    if 'nose' in which and seen(L['nw'] * 0.46, L['nose_y'] - 0.04):
        _bead(p, f(L['nw'] * 0.46, L['nose_y'] - 0.04), 2.6 * k * fc.get('stud_k', 1.0))


def _hair_mass(p, f, L, fc, hc):
    """The hair seen round and below the head from the front (drawn before the face): a bob to the jaw, long hair
    over the shoulders, a mass of curls, a bun on the crown (the press pack's haircuts, seen from the front)."""
    e, st = L['fw'] * 0.5, fc['hair']
    if st == 'shag':
        return shag_mass(p, f, L, fc, hc)
    if st == 'bob':
        pts = [(-e - 0.05, 0.92), (-e - 0.1, 0.5), (-e - 0.08, 0.05), (-e + 0.02, -0.33), (0.0, -0.5), (e - 0.02, -0.33),
               (e + 0.08, 0.05), (e + 0.1, 0.5), (e + 0.05, 0.92), (e - 0.06, 0.88), (-e + 0.06, 0.88)]
    elif st == 'long':                                        # note 14: two curtains, the neck showing between them
        pts = [(-e - 0.1, 1.5), (-e - 0.13, 0.9), (-e - 0.09, 0.2), (-e + 0.02, -0.34), (0.0, -0.5), (e - 0.02, -0.34),
               (e + 0.09, 0.2), (e + 0.13, 0.9), (e + 0.1, 1.5), (e - 0.1, 1.42), (e * 0.62, 0.92), (e * 0.4, 0.6),
               (-e * 0.4, 0.6), (-e * 0.62, 0.92), (-e + 0.1, 1.42)]
    elif st == 'curly':
        n, pts, big = 22, [], fc.get('hair_big', 1.0)
        for k in range(n + 1):
            a = math.pi * (0.92 + 1.16 * k / n)
            r = 1.0 + 0.04 * math.sin(k * 2.7)
            pts.append(((e + 0.17) * big * r * math.cos(a), 0.22 + 0.62 * big * r * math.sin(a)))
        pts += [(e + 0.1 * big, 0.62 + 0.2 * (big - 1)), (-e - 0.1 * big, 0.62 + 0.2 * (big - 1))]
    elif fc.get('hair_messy'):                               # GTA chat 9 (her): a big messy curly bun, high
        return messy_bun(p, f, L, fc, hc)
    else:                                                     # bun: a knot on the crown
        p.poly(curve(f.pts([(-0.13, -0.46), (-0.12, -0.62), (0.0, -0.68), (0.12, -0.62), (0.13, -0.46)]), 3), hc, INK,
               2.2)
        p.line(curve(f.pts([(-0.08, -0.6), (0.0, -0.56), (0.08, -0.6)]), 3), dk(hc, 0.7), 1.4)
        return
    p.poly(curve(f.pts(pts), 3), hc, INK, 2.4)
    rng = np.random.default_rng(len(fc['m']) * 7 + len(st))
    for _ in range(14 if st != 'curly' else 0):              # strands falling down the mass
        u = rng.choice([-1, 1]) * rng.uniform(e + 0.01, e + 0.08)
        v0 = rng.uniform(0.1, 0.4)
        p.line(curve(f.pts([(u, v0), (u * 1.03, v0 + 0.25), (u * 0.99, v0 + (0.45 if st == 'bob' else 0.9))]), 3),
               dk(hc, 1.6) if st == 'long' else dk(hc, 0.75), 1.3)   # long: light strands (hunt 1: a black block)
    if st == 'curly' and fc.get('hair_streak'):
        _streaked_mass(p, f, e, fc, hc, rng)
    elif st == 'curly':
        for _ in range(26):
            a = rng.uniform(math.pi * 0.95, math.pi * 2.05)
            r = rng.uniform(0.75, 0.95)
            big = fc.get('hair_big', 1.0)
            x, y = f((e + 0.17) * big * r * math.cos(a), 0.22 + 0.62 * big * r * math.sin(a))
            p.line(oval(x, y, 7, 6, 10, 0.3, math.pi * 1.6), dk(hc, 0.66), 1.3)


def messy_bun(p, f, L, fc, hc):
    """A big messy bun of curls piled high on the crown (her, GTA chat 9): overlapping lumps of curls, loops of
    curl inside, a few curls springing loose off the top."""
    rng = np.random.default_rng(31)
    lumps = [(0.0, -0.64, 0.15), (-0.12, -0.58, 0.11), (0.12, -0.6, 0.11), (-0.06, -0.74, 0.1), (0.08, -0.75, 0.1),
             (0.0, -0.52, 0.12)]
    for u, v, r in lumps:                                     # ink first, then fill, so the lumps merge as one mass
        p.poly(oval(*f(u, v), *_rr(f, r * 1.04), 18), INK, None)
    for u, v, r in lumps:
        p.poly(oval(*f(u, v), *_rr(f, r * 0.98), 18), hc, None)
    for _ in range(22):                                       # curls inside the bun
        u, v = rng.uniform(-0.17, 0.17), rng.uniform(-0.82, -0.5)
        x, y = f(u, v)
        p.line(oval(x, y, 7, 6, 10, 0.3, math.pi * 1.6), dk(hc, 0.66), 1.3)
    for u, v, du in ((-0.1, -0.82, -0.06), (0.06, -0.86, 0.05), (0.17, -0.7, 0.07)):   # loose curls off the top
        x0, y0 = f(u, v)
        x1, y1 = f(u + du, v - 0.05)
        p.line(curve([(x0, y0), ((x0 + x1) / 2 - 6, (y0 + y1) / 2), (x1, y1)], 3), INK, 4.4)
        p.line(curve([(x0, y0), ((x0 + x1) / 2 - 6, (y0 + y1) / 2), (x1, y1)], 3), hc, 2.4)


def _rr(f, r):
    """A radius in face units as the picture's x and y radii."""
    return (abs(f(r, 0.0)[0] - f(0.0, 0.0)[0]), abs(f(0.0, r)[1] - f(0.0, 0.0)[1]))


def messy_front(p, f, L, fc, hc, hl):
    """Her curls swept up to the bun (GTA chat 9): curly texture over the crown, and loose ringlets falling by
    each temple to the cheek (no fringe)."""
    e, c = L['fw'] * 0.5, L['fhw'] * 0.5
    rng = np.random.default_rng(len(fc['m']) + 11)
    for _ in range(14):
        u, v = rng.uniform(-c, c), rng.uniform(-0.4, hl - 0.04)
        x, y = f(u, v)
        p.line(oval(x, y, 7, 6, 10, 0.3, math.pi * 1.6), dk(hc, 0.66), 1.3)
    for sgn in (-1, 1):                                       # ringlets at the temples: a wavy ribbon each side
        for k, (x0, y0, ln) in enumerate(((e - 0.035, 0.0, 0.58), (e + 0.01, 0.08, 0.46))):
            pts = []                                          # hanging in front of the face's edge, to the cheek
            for i in range(11):
                t = i / 10
                pts.append((sgn * (x0 + 0.03 * math.sin(t * math.pi * 3.5 + k)), y0 + t * ln))
            q = curve(f.pts(pts), 3)
            p.line(q, INK, 6.2 - k)
            p.line(q, hc, 3.8 - k)
            p.line(q, B.lt(hc, 1.25), 1.0)


def _strand(p, pts, col, w):
    """One wavy strand of hair: a thick ribbon with a dark edge and a lighter line along it."""
    p.line(pts, dk(col, 0.5), w + 3)
    p.line(pts, col, w)
    p.line(pts, B.lt(col, 1.3), max(1.2, w * 0.18))


def _streaked_mass(p, f, e, fc, hc, rng):
    """Milburn note 1 (Sam, 17 Nov: "blue and purple as different strands, not a single block"): the curly mass
    drawn as wavy strands from the crown to the edge, blue and purple in turn, so both colours read at phone size."""
    big, sc = fc.get('hair_big', 1.0), fc['hair_streak']
    w = 24 * big / 1.5
    for k in range(14):
        a0 = math.pi * (0.95 + 1.1 * (k + 0.5) / 14)
        col = sc if k % 2 == 0 else B.lt(hc, 1.12)
        pts = []
        for i in range(9):
            r = 0.45 + 0.46 * i / 8
            aa = a0 + 0.045 * math.sin(i * 0.9 + k * 1.3)
            pts.append(f((e + 0.17) * big * r * math.cos(aa), 0.22 + 0.62 * big * r * math.sin(aa)))
        _strand(p, curve(pts, 3), col, w)


def streaked_front(p, f, c, hl, fc, hc, rng):
    """The hair over the forehead as short wavy strands in both colours (the fringe of the streaked mass)."""
    sc = fc['hair_streak']
    for k in range(9):
        u = -c + 2 * c * (k + 0.5) / 9
        pts = [f(u * 0.55 + 0.01 * math.sin(i * 0.9 + k), -0.42 + (hl + 0.36) * i / 7) for i in range(8)]
        pts = [(x + (j / 7) * (f(u, 0)[0] - f(u * 0.55, 0)[0]), y) for j, (x, y) in enumerate(pts)]
        _strand(p, curve(pts, 3), sc if k % 2 == 0 else B.lt(hc, 1.12), 13)


# ---- Milburn note 3 (Sam, 17 Nov: the streaked curls "look like the crest of an alien monster"; look at real dyed
# alternative hair). Why notes 1's fix failed: its strands fanned OUT from the crown like spokes, and hair falls DOWN.
# The house shag (a wolf cut, the alt look in the photos): volume on the crown, choppy layers to the shoulders, pointed
# ends, a heavy choppy fringe to the brows, dark roots, panels of the second colour falling through (peekaboo).
def _shag_dims(L, fc):
    e, b = L['fw'] * 0.5, fc.get('hair_big', 1.0)
    return e, 1.0 + 0.35 * (b - 1.0)


def _jag(x0, x1, v_hi, v_lo, n, seed=0):
    """A choppy edge from x0 to x1: tips and notches at uneven spacing and depth (note 3 r1: even teeth read as a
    saw blade); each tip a narrow point, each notch a wider curve."""
    rng = np.random.default_rng(17 + seed)
    xs = np.cumsum(rng.uniform(0.6, 1.4, n + 1))
    xs = (xs - xs[0]) / (xs[-1] - xs[0])
    out = []
    for i, t in enumerate(xs):
        if i % 2:
            out.append((x0 + (x1 - x0) * t, v_hi + (v_lo - v_hi) * rng.uniform(0.55, 1.15)))
        else:
            out.append((x0 + (x1 - x0) * t, v_hi + (v_lo - v_hi) * rng.uniform(0.0, 0.25)))
    return out


def shag_mass(p, f, L, fc, hc):
    """The shag behind and round the head: crown, cheeks wider, two curtains to the shoulders, the neck between."""
    e, w = _shag_dims(L, fc)
    o = e + 0.15 * w
    left = [(-o + 0.02, 1.22), (-o - 0.02, 0.86), (-o + 0.03, 0.62), (-o - 0.05, 0.5), (-o + 0.01, 0.4),
            (-o + 0.0, 0.08), (-e - 0.02, -0.32), (-0.26, -0.53), (0.0, -0.59), (0.26, -0.53), (e + 0.02, -0.32),
            (o - 0.0, 0.08), (o - 0.01, 0.36), (o + 0.06, 0.47), (o - 0.02, 0.6), (o + 0.02, 0.86), (o - 0.02, 1.22)]
    # the wolf cut's layers: a short layer flicking out at the cheek on each side, the crown a touch fuller
    pts = left + _jag(o - 0.02, e * 0.5, 1.2, 1.33, 7, 1)[1:] + [(e * 0.46, 0.96), (e * 0.4, 0.64),
                                                               (-e * 0.4, 0.64), (-e * 0.46, 0.96)] + \
        _jag(-e * 0.5, -o + 0.02, 1.33, 1.2, 7, 2)[:-1]
    p.poly(curve(f.pts(pts), 2), hc, INK, 2.4)
    sc = fc.get('hair_streak')
    if sc:                                                   # peekaboo panels: one each side, falling down
        for sgn, u0 in ((1, e + 0.02), (-1, e + 0.07)):
            u1 = u0 + 0.07
            pan = [(sgn * u0, 0.18), (sgn * u1, 0.16), (sgn * (u1 + 0.02), 0.7), (sgn * (u1 + 0.01), 1.27),
                   (sgn * (u0 + 0.035), 1.17), (sgn * (u0 - 0.01), 1.29), (sgn * (u0 - 0.02), 0.7)]
            p.poly(curve(f.pts(pan), 2), sc, None)
    for k in range(12):                                      # strands falling down each curtain, dark and light
        sgn = -1 if k % 2 else 1
        u = sgn * (e + 0.015 + 0.012 * (k // 2))
        col = dk(hc, 0.62) if k % 3 else B.lt(hc, 1.35)
        p.line(curve(f.pts([(u, 0.1 + 0.03 * k), (u + sgn * 0.03, 0.6), (u + sgn * 0.01, 1.15)]), 3), col, 1.5)
    o2 = curve(f.pts(pts), 2)
    p.line(o2 + o2[:1], INK, 2.4)


def shag_front(p, f, L, fc, hc):
    """Over the forehead: dark roots on the crown, a heavy choppy fringe to the brows (a chunk of the second colour
    in it), and a layer falling past each temple to the cheek, so the hair hangs round the face."""
    e, w = _shag_dims(L, fc)
    c = L['fhw'] * 0.5
    fb = L['brow_y'] - 0.05                                  # the fringe's ends sit just above the brows
    cap = [(-e - 0.03, 0.5), (-e - 0.04, 0.05), (-e + 0.02, -0.3), (-0.24, -0.47), (0.0, -0.52), (0.24, -0.47),
           (e - 0.02, -0.3), (e + 0.04, 0.05), (e + 0.03, 0.5)]
    cap += [(e - 0.01, 0.62), (e - 0.05, 0.36), (c + 0.0, 0.06)] + _jag(c - 0.02, -c + 0.02, fb - 0.05, fb, 9, 3) + \
        [(-c, 0.06), (-e + 0.05, 0.36), (-e + 0.01, 0.62)]
    p.poly(curve(f.pts(cap), 2), hc, INK, 2.4)
    roots = [(-e + 0.02, -0.3), (-0.24, -0.47), (0.0, -0.52), (0.24, -0.47), (e - 0.02, -0.3)] + \
        _jag(e - 0.04, -e + 0.04, -0.38, -0.33, 7, 4)
    p.poly(curve(f.pts(roots), 2), dk(hc, 0.42), None)       # dark roots, growing out
    sc = fc.get('hair_streak')
    if sc:                                                   # a blue chunk in the fringe, our left of the middle
        u0, u1 = -c * 0.55, -c * 0.12
        chunk = [(u0 + 0.03, -0.36), (u1, -0.36), (u1 + 0.01, fb - 0.04), (u1 - 0.04, fb + 0.0),
                 (u0 + 0.06, fb - 0.04), (u0, fb + 0.0)]
        p.poly(curve(f.pts(chunk), 2), sc, None)
    for k in range(10):                                      # the fringe's strands: down from the crown, a slight sweep
        u = -c + 2 * c * (k + 0.5) / 10
        col = dk(hc, 0.6) if k % 2 else B.lt(hc, 1.3)
        p.line(curve(f.pts([(u * 0.6, -0.44), (u * 0.9, -0.2), (u + 0.01, fb - 0.06)]), 3), col, 1.4)
    for sgn in (-1, 1):                                      # the temple layers' strands
        p.line(curve(f.pts([(sgn * (c + 0.02), -0.05), (sgn * (e - 0.02), 0.25), (sgn * e, 0.55)]), 3),
               dk(hc, 0.6), 1.4)
    o = curve(f.pts(cap), 2)
    p.line(o + o[:1], INK, 2.4)


def _hair_front(p, f, L, fc, hc, skin):
    """The hair over the forehead (after the face): a fringe for the bob and long hair, curls for the curly mass,
    hair drawn back to the bun or a ponytail, a grey horseshoe round a bald crown (receding)."""
    e, c, st = L['fw'] * 0.5, L['fhw'] * 0.5, fc['hair']
    if st == 'receding':
        for sgn in (-1, 1):
            side = [(sgn * (e + 0.02), 0.44), (sgn * (e + 0.03), 0.08), (sgn * (c + 0.02), -0.16),
                    (sgn * (c - 0.06), -0.12), (sgn * (e - 0.03), 0.12), (sgn * (e - 0.02), 0.42)]
            p.poly(curve(f.pts(side), 3), hc, INK, 1.6)
        if bare_skull(fc):                                    # the crown's crease, moved down with the dome
            k = SKULL_CROWN / -0.42
            p.line(curve(f.pts([(-0.12, -0.3 * k), (0.0, -0.33 * k), (0.12, -0.3 * k)]), 3), dk(skin, 0.86), 1.4)
            p.poly(oval(*f(0.1, SKULL_CROWN * 0.6), 13, 6, 16, -0.3), B.lt(skin, 1.14), None)
        else:
            p.line(curve(f.pts([(-0.12, -0.3), (0.0, -0.33), (0.12, -0.3)]), 3), dk(skin, 0.86), 1.4)
        return
    if st == 'shag':
        return shag_front(p, f, L, fc, hc)
    hl = {'bob': -0.02, 'long': -0.08, 'curly': -0.1, 'bun': -0.1, 'pony': -0.1}[st]
    if st == 'bun' and fc.get('hair_messy'):                  # swept up off the face: a higher hairline (her, chat 9)
        hl = -0.2
    cap = _press_cap(L, hl)
    if st == 'bob':                                           # a straight fringe to the brows
        cap = [(-e - 0.02, 0.36), (-e - 0.03, 0.02), (-e + 0.04, -0.24), (-0.24, -0.4), (0.0, -0.45), (0.24, -0.4),
               (e - 0.04, -0.24), (e + 0.03, 0.02), (e + 0.02, 0.36), (e - 0.03, 0.34), (c - 0.02, 0.1),
               (c * 0.6, L['brow_y'] - 0.07), (-c * 0.6, L['brow_y'] - 0.07), (-c + 0.02, 0.1), (-e + 0.03, 0.34)]
    p.poly(curve(f.pts(cap), 2), hc, INK, 2.4)
    rng = np.random.default_rng(len(fc['m']) + 3)
    if st == 'bun' and fc.get('hair_messy'):
        messy_front(p, f, L, fc, hc, hl)
    elif st == 'curly' and fc.get('hair_streak'):
        streaked_front(p, f, c, hl, fc, hc, rng)
    elif st == 'curly':
        for _ in range(16):
            u, v = rng.uniform(-c, c), rng.uniform(-0.38, hl - 0.04)
            x, y = f(u, v)
            p.line(oval(x, y, 7, 6, 10, 0.3, math.pi * 1.6), dk(hc, 0.66), 1.3)
    elif st == 'bob':
        for k in range(7):
            u = -c * 0.55 + k * c * 0.18
            p.line(curve(f.pts([(u * 0.6, -0.4), (u * 0.9, -0.2), (u, L['brow_y'] - 0.08)]), 3), dk(hc, 0.72), 1.3)
    else:                                                     # drawn straight back from the hairline
        for k in range(7):
            u = -c * 0.75 + k * c * 0.25
            p.line(curve(f.pts([(u, hl - 0.02), (u * 0.7, -0.24), (u * 0.3, -0.42)]), 3), dk(hc, 0.72), 1.3)
    if st == 'pony' and fc.get('pony_high'):           # GTA (Lucia; critique r1): a high ponytail from the front:
        p.poly(curve(f.pts([(-0.1, -0.44), (0.0, -0.5), (0.1, -0.44)]), 2), hc, INK, 2.0)   # its root over the crown
        tail = [(e - 0.06, -0.24), (e + 0.14, -0.08), (e + 0.24, 0.3), (e + 0.2, 0.7), (e + 0.1, 0.92),
                (e + 0.04, 0.96), (e + 0.0, 0.7), (e + 0.02, 0.3), (e - 0.03, 0.0)]   # the tail past her cheek: full
        p.poly(curve(f.pts(tail), 3), hc, INK, 2.2)                        # (Sam's likeness note, chat 9)
        for u in (0.04, 0.09, 0.14):
            p.line(curve(f.pts([(e + u, -0.02), (e + u + 0.05, 0.35), (e + u - 0.01, 0.8)]), 3), dk(hc, 0.7), 1.2)
        for (u0, v0), (u1, v1) in (((e + 0.1, 0.9), (e + 0.16, 1.0)), ((e + 0.05, 0.93), (e + 0.02, 1.03)),
                                   ((e + 0.2, 0.62), (e + 0.27, 0.7))):    # split ends off the tail
            p.line(curve(f.pts([(u0, v0), ((u0 + u1) / 2 + 0.01, (v0 + v1) / 2), (u1, v1)]), 3), INK, 3.0)
            p.line(curve(f.pts([(u0, v0), ((u0 + u1) / 2 + 0.01, (v0 + v1) / 2), (u1, v1)]), 3), hc, 1.4)
    if fc.get('hoops'):                                       # GTA (Lucia): small gold hoops at the ear lobes
        for sgn in (-1, 1):
            x, y = f(sgn * (e + 0.01), 0.5)
            p.poly(oval(x, y + 9, 7, 9, 14), None, (222, 180, 70), 2.6)
    if fc.get('hair_loose'):                                  # GTA (Lucia): a middle parting, loose strands either
        p.line(curve(f.pts([(0.0, hl - 0.01), (0.01, -0.3), (0.0, -0.44)]), 3), dk(hc, 0.55), 1.8)  # side of the face
        for sgn in (-1, 1):
            for k, (w, dv) in enumerate(((0.07, 0.0), (0.05, 0.08))):
                x0 = sgn * (c * 0.55 - k * 0.04)
                pts = [(x0, hl - 0.04), (sgn * (e - 0.03 - k * 0.02), 0.04 + dv), (sgn * (e - 0.08 - k * 0.03), 0.3 + dv),
                       (sgn * (e - 0.01), 0.52 + dv), (sgn * (e - 0.05), 0.66 + dv)]
                out = [(x + sgn * w * (1 - i / 5), y) for i, (x, y) in enumerate(pts)]
                p.poly(curve(f.pts(pts + out[::-1]), 3), hc, INK, 1.4)


def _glasses(p, f, L, col, thick=False):
    """Thin-framed glasses round both eyes, a bridge across the nose; thick: heavy rectangular frames (Milburn)."""
    w, h = L['ew'] * 0.78, L['eh'] * 1.15
    if thick:
        w, h = L['ew'] * 0.86, L['eh'] * 1.05
        for sgn in (-1, 1):
            cx, cy = sgn * L['ecx'], L['eye_y'] + 0.004
            box = [(cx - w, cy - h), (cx + w, cy - h * 1.05), (cx + w * 0.96, cy + h * 0.8), (cx, cy + h),
                   (cx - w * 0.96, cy + h * 0.8)]
            p.poly(curve(f.pts(box), 2), None, INK, 9.0)            # critique r1: read as thin wire: heavier
            p.poly(curve(f.pts(box), 2), None, col, 6.0)
        p.line(curve(f.pts([(-L['ecx'] + w, L['eye_y'] - 0.01), (0.0, L['eye_y'] - 0.02), (L['ecx'] - w, L['eye_y'] - 0.01)]),
                     3), col, 5.0)
        return
    for sgn in (-1, 1):
        cx, cy = sgn * L['ecx'], L['eye_y'] + 0.004
        x0, y0 = f(cx - w, cy - h)
        x1, y1 = f(cx + w, cy + h)
        p.poly(oval((x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2, 18), None, col, 2.6)
    p.line(curve(f.pts([(-L['ecx'] + w, L['eye_y'] - 0.01), (0.0, L['eye_y'] - 0.03), (L['ecx'] - w, L['eye_y'] - 0.01)]),
                 3), col, 2.4)



# ------------------------------------------------------------------- Milburn (17 Nov): two tops, kit extras for any film
def flowers_torso(img, p, sp, t):
    """A woollen jumper's knitted flowers: small five-petal flowers in a loose grid down the front (or back)."""
    bot = int(sp.get('bottom', 505)) - 30
    rng = np.random.default_rng(11)
    cols = [(206, 92, 110), (232, 170, 70), (120, 150, 200), (150, 110, 170)]
    for row, y in enumerate(range(60, bot, 70)):
        for k, x in enumerate(range(-50 + (row % 2) * 25, 60, 50)):
            c = cols[(row + k) % len(cols)]
            cx, cy = x + rng.uniform(-4, 4), y + rng.uniform(-4, 4)
            for a in range(5):
                ang = a * 2 * math.pi / 5 + row
                p.poly(oval(cx + 7 * math.cos(ang), cy + 7 * math.sin(ang), 5.5, 5.5, 8), c, dk(c, 0.6), 1.0)
            p.poly(oval(cx, cy, 3.5, 3.5, 8), (246, 226, 140), None)


def crest_torso(img, p, sp, t):
    """A football shirt: white trim round the collar and a small crest on the wearer's left chest."""
    outer = curve([(-46, -4), (-24, 34), (0, 44), (24, 34), (46, -4)], 3)
    inner = curve([(34, -4), (18, 22), (0, 30), (-18, 22), (-34, -4)], 3)
    p.poly(outer + inner, (246, 246, 246), INK, 1.8)          # a white V collar band
    x, y = 36, 86
    shield = [(x - 20, y - 22), (x + 20, y - 22), (x + 20, y + 6), (x, y + 26), (x - 20, y + 6)]
    p.poly(shield, (246, 246, 246), INK, 1.6)
    p.poly(oval(x, y - 2, 9, 9, 12), sp.get('jacket', (196, 22, 36)), None)        # the robin's red breast
    p.poly(oval(x + 6, y - 10, 5, 5, 10), (90, 60, 40), None)


def skirt_torso(img, p, sp, t):
    """A full, flared ('blooming') skirt from the waist to just below the knee, with soft folds (Milburn, 17 Nov)."""
    c = sp.get('dress', sp.get('jacket', (30, 26, 34)))
    sw = sp.get('shoulders', 150) * 0.5
    top, hem = 300, int(sp.get('bottom', 505)) + 260
    pts = [(-sw * 0.95, top), (sw * 0.95, top), (sw * 1.5, top + 140), (sw * 2.3, hem - 24), (sw * 1.2, hem + 8),
           (0, hem - 4), (-sw * 1.2, hem + 8), (-sw * 2.3, hem - 24), (-sw * 1.5, top + 140)]
    p.poly(curve(pts, 3), c, INK, 2.6)
    for u in (-0.9, -0.3, 0.3, 0.9):                       # folds falling from the waist
        p.line(curve([(u * sw * 0.6, top + 30), (u * sw * 0.9, top + 160), (u * sw * 1.2, hem - 20)], 3),
               B.lt(c, 1.9), 1.6)


# ------------------------------------------------------------------- GTA (20 Nov): three tops, kit extras for any film
def _inside(sp, y, pad=0.78):
    """Half the torso's width at height y (the body tapers from the shoulders to a hem at 0.85), padded in."""
    sw = sp.get('shoulders', 150)
    bot = sp.get('bottom', 505)
    return sw * (1.0 - 0.15 * min(1.0, max(0.0, y / bot))) * pad


def palms_torso(img, p, sp, t):
    """A dark shirt's palm-leaf print (Jason, GTA): long pointed leaves with a mid-rib, two tones, in a loose
    scatter at varied angles, kept inside the shirt's outline (front, and the same seen from behind)."""
    rng = np.random.default_rng(23)
    base = sp.get('jacket', (52, 50, 40))
    tones = [(150, 118, 78), (122, 96, 64)]
    bot = int(sp.get('bottom', 480)) - 24
    for row, y in enumerate(range(44, bot, 58)):
        half = _inside(sp, y)
        xs = np.arange(-half + 18 + (row % 2) * 26, half - 10, 52)
        for k, x in enumerate(xs):
            ang = rng.uniform(-1.2, 1.2) + (0.6 if (row + k) % 2 else -0.6)
            ln, wd = rng.uniform(26, 34), rng.uniform(7, 9)
            ca, sa = math.cos(ang), math.sin(ang)
            pts = []
            for u in np.linspace(-1, 1, 9):
                pts.append((u * ln, wd * (1 - u * u) ** 0.8))
            for u in np.linspace(1, -1, 9):
                pts.append((u * ln, -wd * (1 - u * u) ** 0.8))
            c = tones[(row + k) % 2]
            q = [(x + a * ca - b * sa, y + a * sa + b * ca) for a, b in pts]
            q = [(max(-half, min(half, a)), b) for a, b in q]
            p.poly(q, c, None)
            p.line([(x - ln * 0.9 * ca, y - ln * 0.9 * sa), (x + ln * 0.9 * ca, y + ln * 0.9 * sa)], dk(base, 1.1), 1.2)


def biker_torso(img, p, sp, t):
    """A black leather biker jacket worn open (Lucia, GTA): a white vest top between wide lapels with silver
    studs, the off-centre zip running down one front, a gold chain with a small pendant on the vest."""
    jk = sp.get('jacket', (36, 34, 36))
    vest = sp.get('shirt', (240, 238, 230))
    bot = int(sp.get('bottom', 470))
    jw = sp.get('shoulders', 150)
    p.poly([(-jw * 0.9, -4), (jw * 0.9, -4), (jw * 0.86, bot - 4), (-jw * 0.86, bot - 4)], jk, None)  # the plain front
    p.poly(curve([(-44, -2), (0, 40), (44, -2), (46, 120), (34, bot - 6), (-34, bot - 6), (-46, 120)], 3),
           vest, INK, 2.0)                                                        # the vest between the fronts
    p.poly(curve([(-30, -6), (30, -6), (24, 10), (0, 30), (-24, 10)], 3), sp['skin'], None)   # bare skin above it
    p.line(curve([(-30, 4), (0, 30), (30, 4)], 3), dk(vest, 0.8), 1.6)            # the vest's scoop neck
    for k in range(4):                                                            # ribbing
        x = -18 + k * 12
        p.line([(x, 70), (x, bot - 20)], dk(vest, 0.9), 1.0)
    hi = B.lt(jk, 2.4)
    for sgn in (-1, 1):                                                           # the wide lapels
        lap = [(sgn * 40, -10), (sgn * 70, -4), (sgn * 98, 30), (sgn * 92, 96), (sgn * 66, 92), (sgn * 48, 170),
               (sgn * 46, 120)]
        p.poly(curve(lap, 1), B.lt(jk, 1.35), INK, 2.6)                          # wide notched lapels, a sheen
        p.line(curve([(sgn * 72, 4), (sgn * 90, 34), (sgn * 86, 86)], 2), B.lt(jk, 2.6), 2.0)
        p.poly(oval(sgn * 90, 88, 4.2, 4.2, 8), (214, 214, 220), INK, 0.9)         # studs at the lapel points
        p.poly(oval(sgn * 56, 158, 4.2, 4.2, 8), (214, 214, 220), INK, 0.9)
        p.line([(sgn * 46, 168), (sgn * 36, bot - 6)], INK, 2.4)                   # the jacket fronts' edges
    p.line([(-70, 190), (-60, bot - 10)], (196, 196, 202), 2.6)                   # the off-centre zip
    for y in range(200, bot - 20, 14):
        p.line([(-73, y), (-63, y + 2)], (150, 150, 156), 1.0)
    p.line([(54, 250), (90, 244)], (196, 196, 202), 2.4)                          # a pocket zip
    p.line([(-90, 300), (-120, 294)], (196, 196, 202), 2.4)
    gold = (222, 180, 70)
    p.line(curve([(-26, 2), (-14, 56), (0, 74), (14, 56), (26, 2)], 3), gold, 2.6)  # the gold chain
    p.poly([(0, 72), (9, 84), (0, 98), (-9, 84)], gold, dk(gold, 0.6), 1.2)        # the pendant


def biker_back(img, p, sp, t):
    """The biker jacket from behind: its collar round the neck and a yoke seam across the shoulders."""
    jk = sp.get('jacket', (36, 34, 36))
    p.poly([(-44, -6), (44, -6), (48, 18), (-48, 18)], jk, INK, 2.2)
    p.line(curve([(-60, 70), (0, 84), (60, 70)], 3), B.lt(jk, 2.4), 1.6)


class _Scaled:
    """A pen that scales and moves every point (a small picture drawn bigger: the unicorn)."""
    def __init__(self, p, k, x, y):
        self.p, self.k, self.x, self.y = p, k, x, y

    def _q(self, pts):
        return [(self.x + a * self.k, self.y + b * self.k) for a, b in pts]

    def poly(self, pts, fill, line=None, w=1.0):
        return self.p.poly(self._q(pts), fill, line, w * self.k ** 0.5)

    def line(self, pts, col, w=1.0):
        return self.p.line(self._q(pts), col, w * self.k ** 0.5)


def unicorn_torso(img, p, sp, t):
    """A jumper's knitted unicorn being sick rainbows (her, GTA): a white unicorn head in profile on the chest, gold
    horn, pink and purple mane, mouth open, a rainbow pouring down the jumper in six bands."""
    cx, cy = 0, 0
    white, horn = (250, 250, 250), (236, 196, 90)
    bands = [(220, 60, 60), (240, 150, 50), (244, 220, 70), (90, 180, 90), (70, 130, 210), (140, 90, 190)]
    # the rainbow and its splash stay on the jumper, above the hem (Sam, 20 Nov: "vomiting off the jumper itself")
    bot = min(200, (sp.get('bottom', 470) - 150) / 1.7 - 34)
    p = _Scaled(p, 1.7, 30, 150)
    for k, c in enumerate(bands):                         # the rainbow, from the mouth down and out to the left
        o = (k - 2.5) * 5.0
        pts = [(cx - 32, cy + 14 + o * 0.4), (cx - 52 - o * 0.3, cy + 60 + o * 0.6), (cx - 46 - o, bot - 60),
               (cx - 34 - o * 1.2, bot)]
        p.line(curve(pts, 3), c, 5.4)
    for k in range(5):                                    # the splash where it lands
        p.poly(oval(cx - 54 + k * 9, bot + 4 - (k % 2) * 4, 4.4, 3.4, 8), bands[k], None)
    mane = [(cx + 4, cy - 40), (cx + 30, cy - 34), (cx + 40, cy - 6), (cx + 34, cy + 30), (cx + 18, cy + 34)]
    p.poly(curve(mane, 3), (234, 140, 190), INK, 1.4)
    p.line(curve([(cx + 12, cy - 36), (cx + 30, cy - 10), (cx + 26, cy + 24)], 3), (160, 110, 200), 3.0)
    head = [(cx + 6, cy - 38), (cx + 20, cy - 26), (cx + 22, cy + 26), (cx + 4, cy + 30), (cx - 10, cy + 12),
            (cx - 30, cy + 10), (cx - 36, cy + 2), (cx - 30, cy - 10), (cx - 10, cy - 24)]
    p.poly(curve(head, 2), white, INK, 1.8)
    p.poly([(cx - 30, cy + 8), (cx - 36, cy + 18), (cx - 20, cy + 14)], (190, 70, 90), INK, 1.2)    # open mouth
    p.poly([(cx - 4, cy - 30), (cx + 6, cy - 34), (cx - 14, cy - 66)], horn, INK, 1.4)              # the horn
    p.line([(cx - 2, cy - 40), (cx - 8, cy - 46)], dk(horn, 0.7), 1.0)
    p.line(curve([(cx - 12, cy - 12), (cx - 6, cy - 9), (cx - 1, cy - 12)], 2), INK, 1.8)            # a shut eye
    p.poly([(cx + 4, cy - 40), (cx + 10, cy - 54), (cx + 14, cy - 36)], white, INK, 1.4)            # the ear


def scoop_torso(img, p, sp, t):
    """A fitted top with a wide scoop neck (Lucia in the game's first hours): bare skin to the scoop, a soft line
    under it, a fine gold chain with a small pendant."""
    top = sp.get('jacket', (120, 150, 200))
    p.poly(curve([(-46, -6), (46, -6), (40, 14), (0, 44), (-40, 14)], 3), sp['skin'], None)
    p.line(curve([(-46, 2), (-30, 30), (0, 46), (30, 30), (46, 2)], 3), INK, 2.0)
    p.line(curve([(-40, 8), (-26, 34), (0, 52), (26, 34), (40, 8)], 3), dk(top, 0.8), 1.4)
    gold = (222, 180, 70)
    p.line(curve([(-22, -2), (-12, 22), (0, 30), (12, 22), (22, -2)], 3), gold, 1.8)
    p.poly(oval(0, 33, 3.4, 4.2, 8), gold, dk(gold, 0.6), 0.8)


def headphones_torso(img, p, sp, t):
    """Big over-ear headphones resting round the neck (her, GTA), from the front: the 3D prop at yaw 0."""
    headphones3d(p, sp, 0.0)


def headphones_back(img, p, sp, t):
    headphones3d(p, sp, 180.0)


PHONES_YAW = {'three': 45.0, 'side': 90.0, 'three_back': 135.0, 'back': 180.0}


def headphones_view(view):
    return lambda img, p, sp, t: headphones3d(p, sp, PHONES_YAW[view])


def headphones_over_neck(p, view, sp, hx, hy):
    """views.HEAD_WEAR: seen from behind (or three-quarter behind) the band round the back of the neck is nearer
    than the neck, which the head draws after the torso's props: the band again, over it (Sam, GTA chat 10: "they
    don't go around the back of her neck")."""
    if 'headphones' in sp.get('kit_extras', ()) and view in ('back', 'three_back'):
        headphones3d(p, sp, PHONES_YAW[view], band_only=True)


def headphones3d(p, sp, yaw, band_only=False):
    """The headphones as one solid 3D prop round the neck (Sam, GTA chat 9: "drawn on in 2D ... it needs to be a 3D
    prop"; chat 10: the first prop "clip[s] through her body ... more 2D than before"). Real over-ear headphones worn
    round the neck: the band lies on the shoulders round the back of the neck; each cup hangs on the collarbone, its
    pad flat on the chest and its shell facing out. Each cup is two solid drums (the soft pad, then the hard shell),
    every rim a true circle in 3D, so it is thick and round from every side; its back rests ON the chest's surface
    (the torso's section at that height), never inside it. Sizes are real: a cup about two-thirds of the head's width.
    Body units (views.project): neck base at 0, 0, y down, z towards the face."""
    c = sp.get('phones_c', (40, 40, 46))
    pad = sp.get('phones_pad', (64, 64, 72))
    hi = sp.get('phones_hi', (150, 210, 200))
    a = math.radians(yaw)
    view_v = (-math.sin(a), 0.0, math.cos(a))          # towards the camera, in the body's frame
    behind_body = math.cos(a) < -0.2                    # seen from behind: the chest (and the cups on it) is hidden
    sw = sp.get('shoulders', 150)
    deep = 0.6 * sw * 0.86                               # the chest's depth at the collarbone (views.torso_outline side)

    def chest_z(x, y):                                   # the front of the body at (x, y): an oval section
        d = deep + 0.5 * max(0.0, y - 20)
        return d * math.sqrt(max(0.05, 1 - (x / sw) ** 2))

    def unit(v):
        n = math.sqrt(sum(q * q for q in v)) or 1.0
        return tuple(q / n for q in v)

    def add(*vs):
        return tuple(sum(q) for q in zip(*vs))

    def mul(v, k):
        return tuple(q * k for q in v)

    def dot(u, v):
        return sum(x * y for x, y in zip(u, v))

    def cross(u, v):
        return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])

    def proj(pt):
        return V.project(pt, yaw)[0]

    def hull(pts):
        pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))
        if len(pts) < 3:
            return pts

        def turn(o, a_, b_):
            return (a_[0] - o[0]) * (b_[1] - o[1]) - (a_[1] - o[1]) * (b_[0] - o[0])
        lo, up = [], []
        for q in pts:
            while len(lo) > 1 and turn(lo[-2], lo[-1], q) <= 0:
                lo.pop()
            lo.append(q)
        for q in reversed(pts):
            while len(up) > 1 and turn(up[-2], up[-1], q) <= 0:
                up.pop()
            up.append(q)
        return lo[:-1] + up[:-1]

    def ring(ctr, cup, r, k=28):
        return [add(ctr, mul(cup['up'], r * math.cos(2 * math.pi * i / k)), mul(cup['side'], r * math.sin(2 * math.pi * i / k)))
                for i in range(k)]

    R = 40.0                                             # the cup's radius (the pad); the shell a little smaller
    cups = []
    for sgn in (-1, 1):
        # worn as in the photos (references/grand-theft-autism/headphones-*): each cup turned out to the side and a
        # little forward, its pad beside the throat, its rim resting on the collarbone
        n = unit((sgn * 0.85, -0.3, 0.45))
        upr = (0.0, -1.0, -0.7)                          # its top leans back with the chest's slope
        e_up = unit(add(upr, mul(n, -dot(upr, n))))
        e_side = cross(n, e_up)
        cup = dict(sgn=sgn, back=(sgn * 30.0, 26.0, 20.0), n=n, up=e_up, side=e_side)
        dz = 0.0                                         # pushed forward until no part of it is inside her
        for q in ring(cup['back'], cup, R, 36) + ring(add(cup['back'], mul(n, 34.0)), cup, R * 0.9, 36):
            if q[1] > 2:
                dz = max(dz, chest_z(q[0], q[1]) + 1.5 - q[2])
        cup['back'] = add(cup['back'], (0.0, 0.0, dz))
        cups.append(cup)


    def drum(cup, z0, z1, r, wall, face):
        """A solid round drum along the cup's axis, from z0 to z1 out of the chest: its wall, then the end we see."""
        b0 = add(cup['back'], mul(cup['n'], z0))
        b1 = add(cup['back'], mul(cup['n'], z1))
        r0, r1 = ring(b0, cup, r), ring(b1, cup, r)
        p.poly(hull([proj(q) for q in r0 + r1]), wall, INK, 2.4)
        facing = dot(cup['n'], view_v)
        end = r1 if facing >= 0 else r0
        if abs(facing) > 0.08:
            p.poly([proj(q) for q in end], face, INK, 1.8)
        return b1, facing

    def draw_cup(cup):
        _, facing = drum(cup, 0.0, 15.0, R, dk(pad, 0.75), pad)          # the soft pad on the chest
        top, facing = drum(cup, 15.0, 34.0, R * 0.9, dk(c, 0.6), c)      # the hard shell
        if facing > 0.08:                                                 # the shell's face: a ring, a logo, a shine
            p.line([proj(q) for q in ring(top, cup, R * 0.66)] + [proj(ring(top, cup, R * 0.66)[0])], dk(c, 0.55), 2.0)
            p.poly([proj(q) for q in ring(top, cup, R * 0.2, 16)], hi, None)
            sh = [add(top, mul(cup['up'], R * 0.78 * math.cos(u)), mul(cup['side'], -R * 0.78 * math.sin(u)))
                  for u in (math.radians(d) for d in range(-10, 75, 8))]
            p.line([proj(q) for q in sh], B.lt(c, 2.6), 3.0)

    def hidden(pt):
        (sx, _), d = V.project(pt, yaw)
        return d < -4 and abs(sx) < 34                   # behind the neck

    # the band: from each shell's top, up onto the shoulder beside the neck, round the back of the neck
    def outward(cu):                                     # the cup's side away from the neck
        return cu['side'] if cu['side'][0] * cu['sgn'] > 0 else mul(cu['side'], -1)
    ends = [add(cu['back'], mul(cu['n'], 24.0), mul(cu['up'], R * 0.7), mul(outward(cu), R * 0.7)) for cu in cups]
    band = []
    for k in range(49):
        u = math.pi * k / 48                             # 0 at one side of the neck, pi at the other, round the back
        x = -68 * math.cos(u)
        z = 14 - 60 * math.sin(u)
        band.append((x, -5 - 9 * math.sin(u), z))          # rising onto the back of the neck
    lead = []
    for i, e in enumerate(ends):                         # each end climbs from the shell to the band's side
        side_pt = band[0] if i == 0 else band[-1]
        mid = add(mul(add(e, side_pt), 0.5), (0.0, 0.0, 14.0))        # the yoke bows forward a little
        lead.append([add(mul(e, (1 - f) ** 2), mul(mid, 2 * f * (1 - f)), mul(side_pt, f * f))
                     for f in (k / 10 for k in range(11))])
    path = lead[0][::-1][:-1] + band + lead[1][1:]

    def draw_band():
        run = []
        for pt in (band if (behind_body or band_only) else path) + [None]:   # from behind: no stubs of the yokes
            if pt is not None and not hidden(pt) and not (behind_body and pt[2] > 30):
                run.append(proj(pt))
                continue
            if len(run) > 1:
                pts = curve(run, 2)
                p.line(pts, INK, 15.0)
                p.line(pts, c, 10.5)
                p.line([(x, y - 2.5) for x, y in pts], B.lt(c, 2.0), 2.4)
            run = []

    if behind_body or band_only:                         # from behind only the band shows, on the shoulders
        draw_band()
        return
    order = sorted(cups, key=lambda cu: V.project(cu['back'], yaw)[1])    # the far cup first
    draw_cup(order[0])
    draw_band()
    draw_cup(order[1])


# ------------------------------------------------- GTA cast chat (20 Nov): sleeveless tops on a bare-armed body
# 'vest' (Jason in Sam's key art: wide straps, a deep scoop, deep armholes) and 'tank' (Lucia: thin straps). The body
# under them is skin (people.person sets the jacket to the skin), so the arm grows out of a bare shoulder with the
# house arm's one outline (rule 41); the top is drawn on the body, its sides on the body's own outline (any build).
VEST = {'vest': dict(xi=50, xo=88, neck=78, back=26, ya=196, dip=200),
        'tank': dict(xi=60, xo=72, neck=62, back=34, ya=150, dip=200)}
# ya: where the armhole is seen to bottom out (beside the arm); dip: where its curve meets the body's side, under
# the arm, below the house arm's fade at the shoulder (limbs: the upper arm's top 0.6), or the top shows through the
# faded arm as a smudge in the armpit (GTA cast chat).


def _vest_kind(sp):
    return 'tank' if 'tank' in sp.get('kit_extras', ()) else 'vest'


def _top_y(out, x):
    """The highest point of the outline straight above x (the shoulder's top there)."""
    ys = []
    for (x0, y0), (x1, y1) in zip(out, out[1:] + out[:1]):
        if (x0 - x) * (x1 - x) <= 0 and x0 != x1:
            ys.append(y0 + (y1 - y0) * (x - x0) / (x1 - x0))
    return min(ys) if ys else 0.0


def _bez(a, b, c, n=10):
    return [((1 - u) ** 2 * a[0] + 2 * (1 - u) * u * b[0] + u * u * c[0],
             (1 - u) ** 2 * a[1] + 2 * (1 - u) * u * b[1] + u * u * c[1]) for u in np.linspace(0, 1, n)]


def vest_outline(sp, neck=None):
    """The top's outline on the front (or back) body: the scoop, a strap over each shoulder, the armhole curving down
    to the side at ya, the body's own sides to the hem."""
    k = VEST[_vest_kind(sp)]
    sw, bot = sp.get('shoulders', 150), sp.get('bottom', 505)
    out = B.front_outline(sw, bot, 2.0, sp.get('figure'), sp.get('arm_w', 30.0), B.seat_hem(sp))
    edge = lambda y: V._span(out, y)[1] - 0.5                                     # noqa: E731
    neck = k['neck'] if neck is None else neck
    xi, xo, ya = k['xi'], k['xo'], k['ya']
    yi, yo = _top_y(out, xi) + 1.5, _top_y(out, xo) + 1.5
    yd = max(ya, k['dip'])
    xa = edge(yd)
    right = _bez((0, neck), (xi * 0.9, neck), (xi, yi), 9)[:-1] + [(xi, yi), (xo, yo)]
    right += _bez((xo, yo), (xo + 6, ya + 30), (xa, yd), 12)[1:]
    right += [(edge(y), y) for y in np.linspace(yd, bot - 0.6, 9)[1:]]
    left = [(-x, y) for x, y in right]
    return right + left[::-1]


def vest_torso(img, p, sp, t):
    """The sleeveless top on the front; Jason's vest carries its LEONIDA sunset print and his thin silver chain,
    Lucia's tank a fine gold chain with a small pendant."""
    col = sp.get('vest_c', (236, 232, 220))
    kind = _vest_kind(sp)
    # one neck and body (Sam, GTA chat 9: "the neckline which is straight is a kit problem"): the skin body's flat top
    # edge across the neck's foot is painted out, the neck's sides run on down into the shoulders' line
    p.poly([(-35, -40), (35, -40), (38.6, 5), (-38.6, 5)], sp['skin'], None)
    for sgn in (-1, 1):
        p.line(open_curve([(sgn * 33.8, -40), (sgn * 35.2, -16), (sgn * 38.5, -6), (sgn * 44, -3.6)], 3), INK, 2.6)
    p.poly(vest_outline(sp), col, INK, 2.4)
    if kind == 'vest':
        k = VEST['vest']
        p.line(open_curve([(-k['xi'] + 6, 8), (-30, k['neck'] - 6), (0, k['neck'] + 8), (30, k['neck'] - 6),
                      (k['xi'] - 6, 8)], 3), dk(col, 0.86), 1.4)              # the scoop's binding
        if sp.get('vest_print', 'leonida') == 'leonida':
            _leonida(p, 0, 236)
        silver = (196, 198, 204)
        p.line(open_curve([(-30, -2), (-20, 60), (0, 118), (20, 60), (30, -2)], 3), dk(silver, 0.7), 2.4)
        p.line(open_curve([(-30, -2), (-20, 60), (0, 118), (20, 60), (30, -2)], 3), silver, 1.4)
    else:
        gold = (222, 180, 70)                   # a bolder chain and pendant (Sam, chat 9: "a bit small")
        p.line(open_curve([(-28, -2), (-17, 30), (0, 44), (17, 30), (28, -2)], 3), dk(gold, 0.6), 4.2)
        p.line(open_curve([(-28, -2), (-17, 30), (0, 44), (17, 30), (28, -2)], 3), gold, 2.8)
        p.poly(oval(0, 51, 6.4, 8.2, 12), gold, dk(gold, 0.55), 1.2)
        p.poly(oval(-1.8, 48.5, 1.8, 2.2, 6), (252, 236, 170), None)
        for sgn in (-1, 1):                     # a soft line under the chest each side: reads as a woman at phone size
            p.line(open_curve([(sgn * 58, 122), (sgn * 40, 148), (sgn * 14, 146)], 3), dk(col, 0.7), 1.8)   # (critique, chat 9)


def _leonida(p, cx, cy, word_dx=0.0, pitch=21.0, gw=13.0, stroke=2.6):
    """The vest's print (Sam's key art): a setting sun in bands, a palm, LEONIDA in a hand-drawn line above."""
    cam = getattr(p, 'cam', None)                                     # the drawing mirrored (a turned or lying
    if cam is not None:                                               # body): the print is flipped back, so the
        a, b, c = (cam.P(*q) for q in ((cx, cy), (cx + 1, cy), (cx, cy + 1)))   # word never reads backwards
        if (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) < 0:   # (GTA chat 20, lean-out sheet)
            p = _Flip(p, cx)
    bands = [(250, 196, 70), (244, 150, 60), (226, 102, 70)]
    for i, c in enumerate(bands):                                     # the sun: a half disc cut by bands
        y0 = cy + i * 16
        r = 58
        xs = math.sqrt(max(0.0, r * r - (y0 - cy) ** 2))
        xs2 = math.sqrt(max(0.0, r * r - (y0 + 12 - cy) ** 2))
        p.poly([(cx - xs, y0), (cx + xs, y0), (cx + xs2, y0 + 12), (cx - xs2, y0 + 12)], c, None)
    p.line(oval(cx, cy, 58, 58, 24, math.pi, 2 * math.pi), (226, 102, 70), 1.6)
    teal = (40, 88, 96)
    p.line(open_curve([(cx + 34, cy + 48), (cx + 30, cy + 10), (cx + 22, cy - 34)], 3), teal, 4.0)   # the palm
    for a in (-2.6, -2.0, -1.2, -0.5, 0.1):
        tip = (cx + 22 + 34 * math.cos(a), cy - 34 + 22 * math.sin(a) + 14)
        p.line(open_curve([(cx + 22, cy - 34), ((cx + 22 + tip[0]) / 2, cy - 44), tip], 2), teal, 3.0)
    ink = (36, 40, 52)
    x = cx - 3.5 * pitch + word_dx
    for ch in 'LEONIDA':                                              # the word, slanted a little, as the print's
        for st in _GLYPH[ch]:                                         # hand lettering
            p.line([(x + gx * gw + (cy - 60 - (cy - 82 + gy * 22)) * -0.18, cy - 82 + gy * 22) for gx, gy in st],
                   ink, stroke)
        x += pitch


class _Flip:
    """A pen mirrored about x = cx (the print drawn so it reads the right way on a mirrored drawing)."""
    def __init__(self, p, cx):
        self.p, self.cx = p, cx

    def _m(self, pts):
        return [(2 * self.cx - x, y) for x, y in pts]

    def poly(self, pts, *a, **k):
        return self.p.poly(self._m(pts), *a, **k)

    def line(self, pts, *a, **k):
        return self.p.line(self._m(pts), *a, **k)


_GLYPH = {'L': [[(0, 0), (0, 1), (0.8, 1)]], 'E': [[(0.8, 0), (0, 0), (0, 1), (0.8, 1)], [(0, 0.5), (0.6, 0.5)]],
          'O': [[(0.4, 0), (0.85, 0.25), (0.85, 0.75), (0.4, 1), (0, 0.75), (0, 0.25), (0.4, 0)]],
          'N': [[(0, 1), (0, 0), (0.8, 1), (0.8, 0)]], 'I': [[(0.4, 0), (0.4, 1)]],
          'D': [[(0, 0), (0, 1), (0.5, 1), (0.85, 0.7), (0.85, 0.3), (0.5, 0), (0, 0)]],
          'A': [[(0, 1), (0.42, 0), (0.85, 1)], [(0.18, 0.62), (0.68, 0.62)]]}


def vest_back(img, p, sp, t):
    """The top seen from behind: the same straps and armholes, a shallow neck."""
    p.poly(vest_outline(sp, VEST[_vest_kind(sp)]['back']), sp.get('vest_c', (236, 232, 220)), INK, 2.4)


def vest_side(img, p, sp, t):
    """The top in profile: the side of the body below the armhole, which rises in a U to the strap at the chest's
    front and at the back (each outline point pushed down onto the armhole's curve)."""
    k = VEST[_vest_kind(sp)]
    sw, bot = sp.get('shoulders', 150), sp.get('bottom', 505)
    body = V.torso_outline(sp, 'side', bot)
    d = 0.6 * sw
    ya = k['dip'] + 16
    dense = []
    for (x0, y0), (x1, y1) in zip(body, body[1:] + body[:1]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / 6))
        dense += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n)]
    w = 0.82 * d
    U = lambda x: ya - (ya - 24) * min(1.0, max(0.0, (abs(x) - 0.45 * w) / (0.55 * w))) ** 1.5   # noqa: E731
    #   (flat under the arm, which hangs over the middle of the side: the arm's fade must find skin there)
    p.poly([(x, max(y, U(x))) for x, y in dense], sp.get('vest_c', (236, 232, 220)), INK, 2.4)


# ---------------------------------------------------------------------------------------------- workwear (hi-vis)
def workwear_torso(img, p, sp, t):
    """Brexit Is Done (23 Nov, Kemi on site; Sam's photo): a two-tone work jacket over the outfit's own (navy)
    jacket. Her photo, as Sam's note on cast v1 asked ("the orange is gone from her clothes"): ORANGE over the
    shoulders (a yoke from the collar out to the sleeves, which are the outfit's orange `sleeves`), the chest NAVY,
    an orange band round the waist with a silver reflective stripe, navy below it to the hem; a zip. Colours: `work_c` (orange), the outfit's jacket the navy. Front coordinates; the turned views wrap it
    (views.WrapPen), so it turns with her."""
    orange = tuple(sp.get('work_c', (236, 112, 30)))
    silver = (178, 186, 196)                         # (critique r1: a paler silver vanished against the orange)
    navy = tuple(sp.get('jacket', (30, 32, 58)))
    sw = sp.get('shoulders', 150)
    bottom = sp.get('bottom', V.JACKET)

    out = B.front_outline(sw, bottom, 2.0, sp.get('figure'), sp.get('arm_w', 30.0), B.seat_hem(sp))

    def edge(y):                                    # the body's own half width at y (any build: body.FIGS)
        got = V._span(out, min(max(y, 0.0), bottom - 0.5))
        return float(got[1]) - 1.0 if got else sw
    for sgn in (-1, 1):                             # the yoke: orange over each shoulder, from the collar's edge out
        # Its inner edge runs just outside the collar and lapel (the suit's lapel reaches x 70 at y 30, 62 at 150;
        # Sam on cast v2, note 6: "Kemi's orange detailing travels over her white collar"; her photo: the navy
        # collar lies on top, the orange starts at the shoulder outside it). It is drawn after the jacket, so it
        # must never reach inside x 74 above the lapel's foot.
        yoke = [(sgn * 76, 6), (sgn * edge(30) * 0.78, 18), (sgn * edge(40), 40), (sgn * edge(250), 250),
                (sgn * edge(250) * 0.8, 240), (sgn * max(edge(130) * 0.74, 96), 118), (sgn * 86, 70), (sgn * 78, 32)]
        #   (down the side under the arm, as her photo: the sleeve's shoulder joins orange, never fades to navy)
        # chat 7: the smoothed yoke kept inside the body (its curve stood out over the shoulder's top, a nub on
        # each shoulder: the blind judge's "square shoulders"): each point under the top edge and inside the side
        ins = [(x if y < 60 else sgn * min(abs(x), edge(y) - 0.5), max(y, B._top_y(out, x) + 0.8))
               for x, y in curve(yoke, 3)]
        p.poly(ins, orange, INK, 2.0)
    hem = min(bottom, sp.get('jacket_hem') or bottom)   # a short jacket (chat 7): the band sits as far over its hem
    ya, yb = hem - 150, hem - 62                    # the waist band, its silver stripe through the middle
    p.poly([(-edge(ya), ya), (edge(ya), ya), (edge(yb), yb), (-edge(yb), yb)], orange, INK, 2.0)
    sa, sb = ya + 30, ya + 56
    p.poly([(-edge(sa), sa), (edge(sa), sa), (edge(sb), sb), (-edge(sb), sb)], silver, INK, 1.6)
    p.line([(0, 60), (1, bottom)], dk(navy, 0.5), 2.4)       # the zip (no stand-up collar: hidden by the braids
    # from the front, it read as a navy scarf turned; chat 2 critique of Sam's n3 picture)


# ---------------------------------------------------------------------------------------------- patterned blouse
BLOUSE_STRIPES = ((222, 130, 50), (70, 140, 140), (112, 62, 118), (212, 172, 64), (232, 226, 210), (62, 92, 150))


def pattern_torso(img, p, sp, t):
    """Brexit Is Done chat 2 (May's interview photo; Sam on cast v1: she must read clearly as a woman at full
    height): the shirt seen in the jacket's opening becomes a patterned silk blouse, wavy vertical stripes in
    `pattern` colours (her photo's orange, teal, plum, mustard, cream, blue). Drawn on its own layer and kept only
    where the shirt's colour already shows, so it follows the lapels and collar in every view (the turned views'
    WrapPen carries the stripes round with the body)."""
    from PIL import Image
    shirt = np.array(sp.get('shirt', (246, 246, 246)), float)
    cols = sp.get('pattern') or BLOUSE_STRIPES
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    lp = B.Pen(layer, p.cam)
    if hasattr(p, 'pen'):                       # a WrapPen: the same wrap, drawing onto the layer
        old = p.pen
        p.pen = lp
        draw = p
    else:
        draw = lp
    try:
        for k, x in enumerate(np.arange(-90, 91, 7)):       # side by side, no shirt left between them
            pts = [(x + 3 * math.sin(y / 22.0 + k), y) for y in np.arange(-30, 330, 10)]
            draw.line(pts, cols[k % len(cols)], 9.0)
    finally:
        if hasattr(p, 'pen'):
            p.pen = old
    a = np.asarray(img.convert('RGB')).astype(float)
    keep = (np.abs(a - shirt).sum(2) < 24).astype(np.uint8) * 255
    al = np.asarray(layer)[:, :, 3].astype(np.uint16) * keep // 255
    layer.putalpha(Image.fromarray(al.astype(np.uint8)))
    if img.mode == 'RGBA':
        img.alpha_composite(layer)
    else:
        img.paste(layer, (0, 0), layer)
