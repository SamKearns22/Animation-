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

import ad_vanced_notice_cast as AV     # noqa: E402  (installs midterminal's hooks, turnhead, the Vance helpers)
from midterminal_cast import B, P4, dk   # noqa: E402
from ed import INK, curve, oval  # noqa: E402
import turnhead as TH  # noqa: E402

LONG_STYLES = ('bob', 'long', 'curly', 'bun', 'shag')   # hair that has a mass behind the head, drawn before it


def gaze(L, g):
    """This film's gaze_dy is a share of the eye's half-height (-1 up .. 1 down); traitors_cast.eye takes drawing units
    (found 11 Nov, cast chat 8: -0.7 moved the pupils under a pixel, so no planned eye move showed)."""
    eh = (L['eh'] if L else 0.0508) * P4.H / 1.8
    return g * eh * 0.85



HEAD_K = 1.15        # Sam, 11 Nov (cast sheet): "a small-looking head": his face drawn 15% bigger, grown up from the chin


class _Big:
    """While drawing his head, the face height (patriots4's and turnhead's H) is HEAD_K times the house size."""
    def __enter__(self):
        self.old = (P4.H, TH.H)
        P4.H = TH.H = 172.0 * HEAD_K

    def __exit__(self, *a):
        P4.H, TH.H = self.old


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
    """P4.outline_uv without its fold: that list runs out to the upper-left temple and back and repeats the left
    temple point, so the smoothing folds the left forehead into a notch (Sam, 11 Nov: "strange ridges on the left
    side"). Here: once round, crown first, both temples alike."""
    pts = P4.outline_uv(L, 0.4, crown=crown)[2:]               # from the crown: right side, chin, left side
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
    m = dict(P4.AVG)
    for k, v in fc["m"].items():
        m[k] = m[k] + v
    return P4.layout(m)


def front_head(img, p, sp, t, hx, hy):
    """An invented face, front on (blessed_cast's inmate head, lifted): the face card is sp['kit_face']."""
    k = sp['kit_face'].get('k', 1.0)          # note 14: a face may be drawn smaller than the house's bigger size
    with _Big():
        P4.H, TH.H = P4.H * k, TH.H * k
        return _front_head(img, p, sp, t, hx, hy - (HEAD_K * k - 1) * 172.0 * 0.85)


def _front_head(img, p, sp, t, hx, hy):
    who = sp['who']
    fc = sp['kit_face']
    L = face_layout(fc)
    up = max(0.0, -sp.get('gaze_dy', 0.0))                 # looking up at the TV: the face tips up a little
    f = P4.Face(hx, hy, down=-0.8 * up)
    skin, hc = sp['skin'], sp.get('hair_c', (40, 32, 28))
    fw, fhw = L['fw'], L['fhw']
    e, c = fw * 0.5, fhw * 0.5
    if fc['hair'] in LONG_STYLES:
        _hair_mass(p, f, L, fc, hc)
    if fc['hair'] not in ('bob', 'long', 'curly', 'shag'):
        AV._ears(p, f, L, skin)
    outl = _dome_outline(L) if bare_skull(fc) else _outline(L)
    p.poly(curve(f.pts(outl), 4), skin, INK, 2.6)
    jaw = [(-e, 0.5), (-L['jw'] * 0.5, 0.82), (-0.08, 0.98), (0.0, 1.0), (0.08, 0.98), (L['jw'] * 0.5, 0.82), (e, 0.5),
           (e * 0.7, 0.62), (L['mw'] * 0.75, L['lip17'] + 0.04), (0.0, L['lip17'] + 0.03),
           (-L['mw'] * 0.75, L['lip17'] + 0.04), (-e * 0.7, 0.62)]
    if fc.get('stub'):                                        # stubble: a shade over the jaw and the upper lip
        p.poly(curve(f.pts(jaw), 3), dk(skin, fc['stub']), None)
        p.poly(curve(f.pts([(-L['mw'] * 0.6, L['lip0'] - 0.005), (0.0, L['nose_y'] + 0.01),
                            (L['mw'] * 0.6, L['lip0'] - 0.005), (0.0, L['lip0'] + 0.01)]), 3), dk(skin, fc['stub']), None)
        rng = np.random.default_rng(len(who))
        for _ in range(60):
            u, v = rng.uniform(-e * 0.8, e * 0.8), rng.uniform(0.7, 0.96)
            if abs(u) < L['jw'] * 0.5 * (1.0 - (v - 0.82) * 2.2):
                p.poly(oval(*f(u, v), 1.6, 1.6, 6), dk(skin, fc['stub'] - 0.12), None)
        o = curve(f.pts(outl), 4)                             # the face's ink back over the stubble's edge (line-work
        p.line(o + o[:1], INK, 2.6)                           # check, chat 3: the jaw lost its outline)
    if fc.get('beard'):                                       # a short boxed beard and a moustache
        b = fc['beard']
        p.poly(curve(f.pts(jaw), 3), b, INK, 1.6)
        p.poly(curve(f.pts([(-L['mw'] * 0.72, L['lip13'] + 0.02), (-L['mw'] * 0.6, L['lip0'] - 0.01),
                            (0.0, L['nose_y'] + 0.012), (L['mw'] * 0.6, L['lip0'] - 0.01),
                            (L['mw'] * 0.72, L['lip13'] + 0.02), (L['mw'] * 0.5, L['lip0'] + 0.006),
                            (0.0, L['lip0'] - 0.002), (-L['mw'] * 0.5, L['lip0'] + 0.006)]), 3), b, INK, 1.4)
        rng = np.random.default_rng(7)
        for _ in range(40):
            u, v = rng.uniform(-e * 0.8, e * 0.8), rng.uniform(0.72, 0.95)
            if abs(u) < L['jw'] * 0.5 * (1.0 - (v - 0.82) * 2.2) and abs(u) > L['mw'] * 0.6:
                p.line([f(u, v), f(u + 0.004, v + 0.02)], (120, 116, 112), 1.4)       # flecks of grey
    sh = dk(skin, 0.84)                                       # detail: eye bags, the smile folds, a chin dimple
    for sgn in (-1, 1):
        cx, ey, w = sgn * L['ecx'], L['eye_y'], L['ew'] * 0.6
        p.line(curve(f.pts([(cx - w * 0.6, ey + 0.05), (cx, ey + 0.064), (cx + w * 0.7, ey + 0.046)]), 3), sh, 1.5)
        p.line(curve(f.pts([(sgn * L['nw'] * 0.62, L['nose_y'] - 0.03), (sgn * L['mw'] * 0.7, L['lip0'] + 0.01),
                            (sgn * L['mw'] * 0.76, L['lip13'] + 0.03)]), 3), dk(skin, 0.78), 1.6)
    if not fc.get('beard'):
        p.line(curve(f.pts([(-0.025, 0.93), (0.0, 0.94), (0.025, 0.93)]), 3), dk(skin, 0.8), 1.4)
    if fc.get('freckles'):
        rng = np.random.default_rng(31)
        for _ in range(22):
            sgn = 1 if rng.random() < 0.5 else -1
            u, v = sgn * rng.uniform(L['nw'] * 0.4, L['ecx'] + 0.04), rng.uniform(L['eye_y'] + 0.08, L['nose_y'])
            p.poly(oval(*f(u, v), 2.0, 2.0, 6), dk(skin, 0.74), None)
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', 0.22 - 0.2 * up), gaze_dy=gaze(L, -up)), fc['iris'], dk(skin, 0.8),
            liner=2.6)
    if fc.get('pencil'):                                      # a pencil moustache: one thin line above the lip
        y = (L['lip0'] + L['nose_y']) * 0.5 + 0.008
        p.poly(curve(f.pts([(-L['mw'] * 0.62, y + 0.01), (0.0, y - 0.004), (L['mw'] * 0.62, y + 0.01),
                            (0.0, y + 0.008)]), 3), fc['pencil'], None)
    if fc.get('glasses'):
        _glasses(p, f, L, fc['glasses'], fc.get('glasses_thick'))
    P4.brows(p, f, L, fc['brow'], fc.get('brow_thick', 0.05 if fc['hair'] != 'side' else 0.04),
             sp.get('brow_up', 0.012 * up), sp.get('frown', 0.0))
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, L['lip13'])
    P4.lips(p, f, L, dict(sp, smile=sp.get('smile', -0.4)), fc['lip'], (fx, my - 6))
    hl = -0.06
    if fc['hair'] in LONG_STYLES + ('receding', 'pony'):
        _hair_front(p, f, L, fc, hc, skin)
    elif fc['hair'] == 'crop':                                  # a short crop: a low straight hairline, the skull's shape
        cap = [(-e - 0.01, 0.3), (-e - 0.02, 0.04), (-e + 0.04, -0.22), (-0.24, -0.38), (0.0, -0.43), (0.24, -0.38),
               (e - 0.04, -0.22), (e + 0.02, 0.04), (e + 0.01, 0.3), (e - 0.02, 0.3), (c + 0.01, 0.12), (c - 0.03, 0.02),
               (c * 0.7, hl), (0.0, hl - 0.012), (-c * 0.7, hl), (-c + 0.03, 0.02), (-c - 0.01, 0.12), (-e + 0.02, 0.3)]
        p.poly(curve(f.pts(cap), 2), hc, INK, 2.4)
        rng = np.random.default_rng(5)
        for _ in range(36):                                   # the crop's texture: short strokes
            u, v = rng.uniform(-c, c), rng.uniform(-0.36, hl - 0.03)
            if abs(u) < c * (1.0 - max(0.0, -v - 0.25) * 2.0):
                p.line([f(u, v), f(u + 0.008, v + 0.025)], B.lt(hc, 1.7), 1.4)
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
        piercings(p, f, L, fc, sp.get('brow_up', 0.012 * up), sp.get('frown', 0.0))
    return fx


SILVER = (214, 218, 226)


def _bead(p, xy, r):
    """One silver ball: ink rim, a white glint up-left (reads as metal at phone size)."""
    p.poly(oval(*xy, r, r, 10), SILVER, INK, 1.0)
    p.poly(oval(xy[0] - r * 0.35, xy[1] - r * 0.35, r * 0.4, r * 0.4, 6), (255, 255, 255), None)


def piercings(p, f, L, fc, raise_=0.0, frown=0.0):
    """`piercings: brow, lip, nose` (any of them; bare `piercings` = all three), silver, front head (Milburn note 2):
    a bar through the outer end of her left brow (our right) with a ball each side, a hoop through the lower lip off
    centre (our left), a stud on the nostril wing (our right)."""
    which = fc['piercings']
    thick = fc.get('brow_thick', 0.05)
    k = max(1.0, abs(f(1.0, 0.0)[0] - f(0.0, 0.0)[0]) / 100.0)   # sizes grow with the face (phone size, 2a's close)
    if 'brow' in which:
        up = raise_[1] if isinstance(raise_, (tuple, list)) else raise_
        uv = P4.brow_uv(L, thick, up, frown)
        (xm, ym), (xo, yo) = uv[1], uv[2]
        u = xm + (xo - xm) * 0.62
        v = ym + (yo - ym) * 0.62
        a, b = f(u - 0.008, v - thick * 0.75), f(u + 0.008, v + thick * 1.05)
        p.line([a, b], INK, 2.6 * k)
        p.line([a, b], SILVER, 1.4 * k)
        _bead(p, a, 2.8 * k)
        _bead(p, b, 2.8 * k)
    if 'lip' in which:
        r = 4.2 * k
        cx, cy = f(-L['mw'] * 0.26, L['lip17'])
        cy -= r * 0.25                               # the ring's top runs into the lower lip, the rest hangs below
        ring = [(cx + r * math.sin(a), cy + r * math.cos(a)) for a in np.linspace(-2.5, 2.5, 20)]
        p.line(ring, INK, 3.2 * k)
        p.line(ring, SILVER, 1.8 * k)
        p.poly(oval(cx - r * 0.5, cy + r * 0.6, 0.8 * k, 0.8 * k, 6), (255, 255, 255), None)
    if 'nose' in which:
        _bead(p, f(L['nw'] * 0.46, L['nose_y'] - 0.04), 2.6 * k)


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
    cap = _press_cap(L, hl)
    if st == 'bob':                                           # a straight fringe to the brows
        cap = [(-e - 0.02, 0.36), (-e - 0.03, 0.02), (-e + 0.04, -0.24), (-0.24, -0.4), (0.0, -0.45), (0.24, -0.4),
               (e - 0.04, -0.24), (e + 0.03, 0.02), (e + 0.02, 0.36), (e - 0.03, 0.34), (c - 0.02, 0.1),
               (c * 0.6, L['brow_y'] - 0.07), (-c * 0.6, L['brow_y'] - 0.07), (-c + 0.02, 0.1), (-e + 0.03, 0.34)]
    p.poly(curve(f.pts(cap), 2), hc, INK, 2.4)
    rng = np.random.default_rng(len(fc['m']) + 3)
    if st == 'curly' and fc.get('hair_streak'):
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
