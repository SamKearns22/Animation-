#!/usr/bin/env python3
"""MAP  The people kit's drawing parts (ranking item 4, overnight chat 4, 14 Nov), LIFTED out of blessed_cast.py
unchanged in look: every invented face is the average face (patriots4) pushed its own way, at the house's bigger
head size, with lips, brows, a nose, ears, eye bags, shaped hair, stubble or a beard, glasses, freckles. A person's
face card rides in their own spec (sp['kit_face']), so nothing is keyed by name. people.py reads the descriptions
and hangs these parts on the engine; no film imports this file until Sam approves the kit.

Map: gaze 23 | head size 31 | outline 49 | hair cap 62 | torsos (robe, officer) 70 | wig 100 | the front face 129 |
     hair mass 241 | hair front 279 | glasses 313
"""
import math

import numpy as np

import ad_vanced_notice_cast as AV     # noqa: E402  (installs midterminal's hooks, turnhead, the Vance helpers)
from midterminal_cast import B, P4, dk   # noqa: E402
from ed import INK, curve, oval  # noqa: E402
import turnhead as TH  # noqa: E402

LONG_STYLES = ('bob', 'long', 'curly', 'bun')   # hair that has a mass behind the head, drawn before it


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
    if fc['hair'] not in ('bob', 'long', 'curly'):
        AV._ears(p, f, L, skin)
    p.poly(curve(f.pts(_outline(L)), 4), skin, INK, 2.6)
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
        o = curve(f.pts(_outline(L)), 4)                      # the face's ink back over the stubble's edge (line-work
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
    if fc.get('glasses'):
        _glasses(p, f, L, fc['glasses'])
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
    return fx


def _hair_mass(p, f, L, fc, hc):
    """The hair seen round and below the head from the front (drawn before the face): a bob to the jaw, long hair
    over the shoulders, a mass of curls, a bun on the crown (the press pack's haircuts, seen from the front)."""
    e, st = L['fw'] * 0.5, fc['hair']
    if st == 'bob':
        pts = [(-e - 0.05, 0.92), (-e - 0.1, 0.5), (-e - 0.08, 0.05), (-e + 0.02, -0.33), (0.0, -0.5), (e - 0.02, -0.33),
               (e + 0.08, 0.05), (e + 0.1, 0.5), (e + 0.05, 0.92), (e - 0.06, 0.88), (-e + 0.06, 0.88)]
    elif st == 'long':                                        # note 14: two curtains, the neck showing between them
        pts = [(-e - 0.1, 1.5), (-e - 0.13, 0.9), (-e - 0.09, 0.2), (-e + 0.02, -0.34), (0.0, -0.5), (e - 0.02, -0.34),
               (e + 0.09, 0.2), (e + 0.13, 0.9), (e + 0.1, 1.5), (e - 0.1, 1.42), (e * 0.62, 0.92), (e * 0.4, 0.6),
               (-e * 0.4, 0.6), (-e * 0.62, 0.92), (-e + 0.1, 1.42)]
    elif st == 'curly':
        n, pts = 22, []
        for k in range(n + 1):
            a = math.pi * (0.92 + 1.16 * k / n)
            r = 1.0 + 0.06 * math.sin(k * 2.7)
            pts.append(((e + 0.17) * r * math.cos(a), 0.22 + 0.62 * r * math.sin(a)))
        pts += [(e + 0.1, 0.62), (-e - 0.1, 0.62)]
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
    if st == 'curly':
        for _ in range(26):
            a = rng.uniform(math.pi * 0.95, math.pi * 2.05)
            r = rng.uniform(0.75, 0.95)
            x, y = f((e + 0.17) * r * math.cos(a), 0.22 + 0.62 * r * math.sin(a))
            p.line(oval(x, y, 7, 6, 10, 0.3, math.pi * 1.6), dk(hc, 0.66), 1.3)


def _hair_front(p, f, L, fc, hc, skin):
    """The hair over the forehead (after the face): a fringe for the bob and long hair, curls for the curly mass,
    hair drawn back to the bun or a ponytail, a grey horseshoe round a bald crown (receding)."""
    e, c, st = L['fw'] * 0.5, L['fhw'] * 0.5, fc['hair']
    if st == 'receding':
        for sgn in (-1, 1):
            side = [(sgn * (e + 0.02), 0.44), (sgn * (e + 0.03), 0.08), (sgn * (c + 0.02), -0.16),
                    (sgn * (c - 0.06), -0.12), (sgn * (e - 0.03), 0.12), (sgn * (e - 0.02), 0.42)]
            p.poly(curve(f.pts(side), 3), hc, INK, 1.6)
        p.line(curve(f.pts([(-0.12, -0.3), (0.0, -0.33), (0.12, -0.3)]), 3), dk(skin, 0.86), 1.4)
        return
    hl = {'bob': -0.02, 'long': -0.08, 'curly': -0.1, 'bun': -0.1, 'pony': -0.1}[st]
    cap = _press_cap(L, hl)
    if st == 'bob':                                           # a straight fringe to the brows
        cap = [(-e - 0.02, 0.36), (-e - 0.03, 0.02), (-e + 0.04, -0.24), (-0.24, -0.4), (0.0, -0.45), (0.24, -0.4),
               (e - 0.04, -0.24), (e + 0.03, 0.02), (e + 0.02, 0.36), (e - 0.03, 0.34), (c - 0.02, 0.1),
               (c * 0.6, L['brow_y'] - 0.07), (-c * 0.6, L['brow_y'] - 0.07), (-c + 0.02, 0.1), (-e + 0.03, 0.34)]
    p.poly(curve(f.pts(cap), 2), hc, INK, 2.4)
    rng = np.random.default_rng(len(fc['m']) + 3)
    if st == 'curly':
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


def _glasses(p, f, L, col):
    """Thin-framed glasses round both eyes, a bridge across the nose."""
    w, h = L['ew'] * 0.78, L['eh'] * 1.15
    for sgn in (-1, 1):
        cx, cy = sgn * L['ecx'], L['eye_y'] + 0.004
        x0, y0 = f(cx - w, cy - h)
        x1, y1 = f(cx + w, cy + h)
        p.poly(oval((x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2, 18), None, col, 2.6)
    p.line(curve(f.pts([(-L['ecx'] + w, L['eye_y'] - 0.01), (0.0, L['eye_y'] - 0.03), (L['ecx'] - w, L['eye_y'] - 0.01)]),
                 3), col, 2.4)

