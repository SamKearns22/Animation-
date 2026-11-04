#!/usr/bin/env python3
"""Patriots 4 (The Celebrity Traitors winners): the cast. Built 1 Nov from Sam's references (references/patriots-4/).

Reused (kit-catalogue, rule 28): Claudia's head and hair from `traitors_cast` (new outfit here: black jacket, cream
high-neck blouse with a gold chain, ref 03 and 11); the Patriot whole from `patriots3_cast` (balaclava, black jacket).
New: Romesh Ranganathan and Sebastian "Bash" Croft, as likeness heads (film-quality rules 49-51).

The two new heads are drawn from MEASUREMENTS (likeness.py card on photos 14 and 16, 18 and 19), not by eye: each face
is laid out on MediaPipe's average face and moved by how far this person differs from real faces, pushed further
(`PUSH`). The same drawing with the average measurements is the head's twin (`--average`), so likeness.py check can
take away what the drawing style itself does.

    Romesh  rust-orange double-breasted suit, teal top; big squarish CLEAR glasses; short tight dark curls, greying a
            little; a SHORT salt-and-pepper beard (greyest at the chin) under a dark moustache (Sam, 1 Nov: ref 13); brows set high; a wide nose; a long narrow face (refs 03,
            09, 13-16)
    Bash    dark navy tartan suit, white shirt open at the collar; swept wavy brown hair falling over the brow; close-set
            big eyes under low heavy brows; a narrow tapering jaw; a long nose; light stubble; two silver rings
            (refs 04-08, 13, 17-20)

    python3 source/patriots4_cast.py head WHO OUT.png [--average]   one head, large, front on (for likeness.py check)
    python3 source/patriots4_cast.py likeness OUT_DIR                 every head checked against its photos
    python3 source/patriots4_cast.py sheet OUT.jpg                    the cast sheet
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import traitors_cast as TC       # noqa: E402  (Claudia's head; installs the head hooks into burnham)
import patriots3_cast as P3      # noqa: E402  (the Patriot)
import views as V                # noqa: E402
import mouths                    # noqa: E402
from ed import INK, curve, oval  # noqa: E402

dk, blend = TC.dk, TC.blend
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
REFS = os.path.join(HERE, '..', 'references', 'patriots-4')

# ---------------------------------------------------------------------------------------------- the measurements
# Real faces' middle (likeness_average.json, 'neutral') and each person's measured face (likeness.py card, 1 Nov).
AVG = dict(face_wide=0.872, jaw_wide=0.82, forehead_wide=0.942, eyes_apart=1.325, eye_size=0.186, eye_open=0.313,
           eye_tilt=2.474, brow_high=0.586, brow_slope=-9.371, nose_long=0.417, nose_wide=0.641, mouth_wide=0.802,
           lip_top=0.121, lip_low=0.183, philtrum=0.133, chin_long=0.295)
MEASURED = {
    'romesh': dict(face_wide=0.789, jaw_wide=0.837, forehead_wide=0.951, eyes_apart=1.286, eye_size=0.2,
                   eye_open=0.303, eye_tilt=1.718, brow_high=0.752, brow_slope=-11.316, nose_long=0.413,
                   nose_wide=0.72, mouth_wide=0.877, lip_top=0.117, lip_low=0.206, philtrum=0.146, chin_long=0.293),
    'bash': dict(face_wide=0.819, jaw_wide=0.781, forehead_wide=0.955, eyes_apart=1.058, eye_size=0.206,
                 eye_open=0.363, eye_tilt=3.49, brow_high=0.478, brow_slope=-10.587, nose_long=0.458,
                 nose_wide=0.677, mouth_wide=0.874, lip_top=0.125, lip_low=0.171, philtrum=0.117, chin_long=0.294),
}
MEASURED['claudia'] = dict(face_wide=0.791, jaw_wide=0.827, forehead_wide=0.956, eyes_apart=1.241, eye_size=0.209,
                           eye_open=0.345, eye_tilt=2.185, brow_high=0.592, brow_slope=-12.039, nose_long=0.422,
                           nose_wide=0.62, mouth_wide=0.76, lip_top=0.135, lip_low=0.169, philtrum=0.142,
                           chin_long=0.33)   # her photos smile: mouth, nose width, philtrum and chin set from the card's
                                             # words against smiling faces (a small mouth, a long gap, a long chin)
PUSH = {'romesh': 1.6, 'bash': 1.6, 'claudia': 1.6}
TUNE = {   # per measure, an extra push where the first check found the drawing under the photo (rule 49)
    'romesh': dict(jaw_wide=1.0, nose_wide=2.0, eye_size=2.0, forehead_wide=1.0, lip_low=3.0, philtrum=2.0,
                   brow_slope=1.8, eyes_apart=4.5, brow_high=0.0, nose_long=1.5),   # searched, 1 Nov (series look)
    'bash': dict(jaw_wide=3.0, philtrum=2.0, brow_slope=1.5, eye_size=1.4, nose_wide=2.0, eye_open=1.4, brow_high=1.3),
    'claudia': dict(face_wide=2.4, jaw_wide=-3.0),   # Sam, 1 Nov: she is thin-faced (the jaw x15 pushed for the
                                                     # face finder's score made her round)
}


def target(who, average=False):
    """The measures to draw: the person's, pushed further from the middle (or the middle itself, for the twin)."""
    if average:
        return dict(AVG)
    m, k = MEASURED[who], PUSH[who]
    return {key: AVG[key] + k * TUNE[who].get(key, 1.0) * (m[key] - AVG[key]) for key in AVG}


def layout(m):
    """Where everything goes, as fractions of the face height H (forehead top 0 .. chin 1; x from the middle),
    laid out on MediaPipe's average face (likeness.canonical) and moved to give the measures m."""
    fw = m['face_wide']
    ew = m['eye_size'] * fw
    gap = m['eyes_apart'] * ew
    ecx = gap / 2 + ew / 2
    ipd = 2 * ecx
    eye_y = 0.32
    eh = m['eye_open'] * ew                            # the opening's height (upper lid to lower lid)
    lid_top = eye_y - eh / 2
    brow_y = lid_top - m['brow_high'] * ew             # the brow's lower edge over the pupil (landmark 52)
    slope = math.tan(math.radians(m['brow_slope']))   # + rises to the outside
    nose_y = 0.283 + m['nose_long'] * 0.717
    lip0 = nose_y + m['philtrum'] * 0.717
    mw = m['mouth_wide'] * ipd
    lip13 = lip0 + m['lip_top'] * mw
    lip17 = lip13 + 0.006 + m['lip_low'] * mw
    want17 = 1.0 - m['chin_long'] * 0.717                # the chin's length: meet it halfway by moving the mouth
    k = 1.0 + 0.5 * ((want17 - nose_y) / (lip17 - nose_y) - 1.0)
    lip0, lip13, lip17 = (nose_y + (v - nose_y) * k for v in (lip0, lip13, lip17))
    return dict(fw=fw, jw=m['jaw_wide'] * fw, fhw=m['forehead_wide'] * fw, ew=ew, ecx=ecx, eye_y=eye_y, eh=eh,
                lid_top=lid_top, brow_y=brow_y, slope=slope, nose_y=nose_y, nw=m['nose_wide'] * ipd, lip0=lip0,
                lip13=lip13, lip17=lip17, mw=mw, tilt=math.tan(math.radians(m['eye_tilt'])))


H = 172.0          # the face height in the person's own units (the library's heads are about 190 from crown to chin)


class Face:
    """Turns the layout's fractions into the person's units: x across from the face's middle, y down from the top of
    the forehead. `tq` (0..1) turns it towards a three-quarter view facing our right (features slide to the near
    side, the far half narrows), so the likeness survives the turn (newsdesk_cast's way)."""

    def __init__(self, hx, hy, tq=0.0, turn=0.0, down=0.0):
        self.cx, self.top = hx + turn * 12, hy - 72 + 10 * down
        self.hx, self.tq = hx, tq

    def x(self, u):
        k = 1.0 - 0.38 * self.tq if u < 0 else 1.0 - 0.1 * self.tq     # the far side (our left) narrows
        return self.cx + 0.2 * self.tq * H + u * H * k

    def __call__(self, u, v):
        return (self.x(u), self.top + v * H)

    def pts(self, uvs):
        return [self(u, v) for u, v in uvs]


def outline_uv(L, chin_w=0.36, crown=-0.17):
    """The head's outline (fractions), round from the left temple over the crown and down to the chin."""
    fw, jw, fhw = L['fw'], L['jw'], L['fhw']
    right = [(fhw * 0.5 * 0.93, 0.0), (fhw * 0.5, 0.16), (fw * 0.5, 0.43), (fw * 0.5 * 0.97, 0.6),
             (jw * 0.5, 0.82), (jw * 0.5 * chin_w + 0.04, 0.965), (0.0, 1.0)]
    top = [(fhw * 0.5 * 0.7, crown * 0.6), (0.0, crown)]
    left = [(-u, v) for u, v in right[::-1][1:]]
    return [(-u, v) for u, v in top[::-1]] + top[1:] + right + left + [(-fhw * 0.5 * 0.93, 0.0), (-fhw * 0.5 * 0.7, crown * 0.6)]


def eyes(p, f, L, sp, iris, lid_c, liner=2.6, wide=0.0):
    """Both eyes (traitors_cast.eye: one opening between two lids, the iris cut to it). wide (0..1): the stare."""
    w = L['ew'] * H / 2
    h = L['eh'] * H / 1.8 * (1 + 0.55 * wide)
    st = dict(lid=sp.get('lid4', 0.08) * (1 - wide), look=sp.get('look', 0.0), squint=sp.get('squint', 0.0),
              closed=sp.get('blink', False), gaze_dy=sp.get('gaze_dy', 0.0))
    for sgn in (-1, 1):
        ex, ey = f(sgn * L['ecx'], L['eye_y'])
        ww = w * (1 - 0.3 * f.tq if sgn < 0 else 1.0)
        TC.eye(p, ex, ey, sgn, ww, h, iris, st, lid_c, liner=liner)


def brows(p, f, L, c, thick=0.034, raise_=0.0, frown=0.0):
    """Filled brows from inner to outer end at the measured height and slope. raise_ lifts them (surprise);
    frown pulls the inner ends down (narrowed, accusing). raise_ may be a pair (our left, our right): one brow up."""
    for sgn in (-1, 1):
        ecx, ew = L['ecx'], L['ew']
        xi, xo, xm = ecx - 0.69 * ew, ecx + 0.98 * ew, ecx + 0.21 * ew
        up = raise_[0 if sgn < 0 else 1] if isinstance(raise_, (tuple, list)) else raise_
        y_m = L['brow_y'] - thick * 0.35 - up
        yi = y_m + L['slope'] * (xm - xi) * 1.0 + frown
        yo = y_m - L['slope'] * (xo - xm)
        ym = y_m - 0.008
        th = thick
        uv = [(xi, yi - th * 0.45), (xm, ym - th * 0.6), (xo, yo - th * 0.2), (xo + 0.01, yo + th * 0.15),
              (xm, ym + th * 0.45), (xi, yi + th * 0.55)]
        p.poly(curve(f.pts([(sgn * u, v) for u, v in uv]), 3), c, None)


def nose(p, f, L, skin):
    """The bridge as one line down one side, the tip and the nostril wings at the measured width."""
    nw, y = L['nw'], L['nose_y']
    sd = dk(skin, 0.72)
    p.line(f.pts([(-0.025, L['eye_y'] + 0.02), (-0.04, y - 0.07)]), sd, 1.8)
    for sgn in (-1, 1):                                # the wings: a curve round each side of the nose's base
        p.line(curve(f.pts([(sgn * nw * 0.32, y - 0.075), (sgn * nw * 0.5, y - 0.045), (sgn * nw * 0.46, y - 0.012),
                            (sgn * nw * 0.26, y - 0.002)]), 3), INK, 1.8)
    p.line(curve(f.pts([(-nw * 0.2, y - 0.002), (-0.03, y + 0.005), (0.0, y - 0.004), (0.03, y + 0.005),
                        (nw * 0.2, y - 0.002)]), 3), INK, 1.6)
    for sgn in (-1, 1):
        p.poly(oval(*f(sgn * nw * 0.2, y - 0.016), 5, 3, 10), dk(skin, 0.5), None)


def lips(p, f, L, sp, lip_c, fx_my):
    """Closed lips at the measured width and fullness; talking shapes from mouths.draw (the series' lip sync)."""
    fx, my = fx_my
    mw, l0, l13, l17 = L['mw'], L['lip0'], L['lip13'], L['lip17']
    smile = sp.get('smile', 0.0)

    def rest():
        hw = mw / 2
        top = curve(f.pts([(-hw, l13 - 0.004 * smile), (-hw * 0.4, l0 + 0.006), (0.0, l0 + 0.012), (hw * 0.4, l0 + 0.006),
                           (hw, l13 - 0.004 * smile), (0.0, l13 + 0.004)]), 3)
        bot = curve(f.pts([(-hw, l13 - 0.004 * smile), (0.0, l13 + 0.004), (hw, l13 - 0.004 * smile), (hw * 0.5, l17 - 0.01),
                           (0.0, l17), (-hw * 0.5, l17 - 0.01)]), 3)
        p.poly(top, dk(lip_c, 0.86), INK, 1.5)
        p.poly(bot, lip_c, INK, 1.5)
        p.line(curve(f.pts([(-hw, l13 - 0.006 * smile), (-hw * 0.3, l13 + 0.004), (hw * 0.3, l13 + 0.004),
                            (hw, l13 - 0.006 * smile)]), 3), INK, 2.2)
    TC.talk_or(p, dict(sp, lips=True, lip_c=lip_c), 0.0, fx, my, rest)


# ---------------------------------------------------------------------------------------------- Romesh
R_SKIN = (182, 124, 90)
R_HAIR = (34, 30, 32)
R_HAIR_SIDE = (58, 54, 56)
R_BEARD = (78, 72, 72)
R_MOUST = (34, 30, 32)
R_GREY = (176, 172, 168)
R_FRAME = (214, 212, 206)
RIM = [5.8, 2.8]                 # clear frames: (outline, frame) widths (thicker ink: they shimmered as he talked)
R_LIP = (150, 92, 84)
R_RUST = (190, 88, 42)
R_TEAL = (36, 96, 104)


def romesh_head(img, p, sp, t, hx, hy):
    L = layout(target('romesh', sp.get('average', False)))
    f = Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin = R_SKIN
    for sgn in (-1, 1):                                # ears (only the near one in a three-quarter turn)
        if sgn < 0 and f.tq > 0.5:
            continue
        ex, ey = f(sgn * (L['fw'] * 0.5 + 0.01), 0.42)
        p.poly(oval(ex, ey, 11, 23, 20), skin, INK, 2.4)
        p.line([(ex - sgn * 2, ey - 10), (ex + sgn * 3, ey), (ex - sgn * 1, ey + 10)], dk(skin, 0.7), 1.4)
    out = curve(f.pts(outline_uv(L, 0.42)), 4)
    p.poly(out, skin, INK, 2.6)
    # the series look (Sam, 1 Nov: ref 13, taken two days before, with refs 04-05): a SHORT, close-trimmed beard,
    # salt-and-pepper and greyest at the chin, under a darker moustache; it hugs the jaw, from the sideburns down
    fw, jw = L['fw'], L['jw']
    ny, l0, l17 = L['nose_y'], L['lip0'], L['lip17']
    right = [(fw * 0.5 + 0.004, 0.3), (fw * 0.5 - 0.04, 0.5), (L['nw'] * 0.85, ny + 0.0), (L['nw'] * 0.45, ny + 0.015),
             (L['mw'] * 0.36, l0 - 0.008)]
    rim = [(fw * 0.5 + 0.006, 0.6), (jw * 0.5 + 0.03, 0.84), (jw * 0.36, 1.0), (jw * 0.14, 1.04), (0.0, 1.045)]
    shape = ([(u, v) for u, v in right] + [(-u, v) for u, v in right[::-1]]
             + [(-u, v) for u, v in rim] + [(u, v) for u, v in rim[::-1]])
    shape = shape[:len(right) * 2] + [(-fw * 0.5 - 0.004, 0.3)] + shape[len(right) * 2:]
    beard_pts = curve(f.pts([(u, v) for u, v in shape[len(right):]] + [(u, v) for u, v in shape[:len(right)]]), 4)
    p.poly(beard_pts, R_BEARD, INK, 2.0)
    rng = np.random.default_rng(14)
    for _ in range(150):                               # salt and pepper: grey flecks, thickest at the chin
        u, v = rng.uniform(-fw * 0.5, fw * 0.5), rng.uniform(0.5, 1.03)
        inside = abs(u) < (fw * 0.5 if v < 0.6 else jw * 0.5 * (1.0 - 1.4 * max(0.0, v - 0.84)))
        if inside and (v > l17 or abs(u) > L['mw'] * 0.62) and rng.random() < 0.35 + 0.8 * max(0.0, v - 0.7):
            x, y = f(u, v)
            p.line([(x, y), (x + rng.uniform(-1.5, 1.5), y + 3.5)], R_GREY, 1.3)
    eyes(p, f, L, sp, (48, 30, 22), dk(skin, 0.82), wide=sp.get('wide', 0.0))
    brows(p, f, L, (28, 24, 24), 0.036, sp.get('brow_up', 0.0), sp.get('frown', 0.0))
    nose(p, f, L, skin)
    fx, my = f(0.0, (L['lip13']))
    lips(p, f, L, sp, R_LIP, (fx, my - 6))
    # the moustache, darker than the beard, over the top of the upper lip
    mw2, l13 = L['mw'] * 0.5, L['lip13']                # a band from under the nose, drooping past the lip corners
    p.poly(curve(f.pts([(-mw2 * 1.2, l13 + 0.04), (-mw2 * 1.05, l0 + 0.0), (-L['nw'] * 0.45, ny + 0.014), (0.0, ny + 0.022),
                        (L['nw'] * 0.45, ny + 0.014), (mw2 * 1.05, l0 + 0.0), (mw2 * 1.2, l13 + 0.04), (mw2 * 1.06, l13 + 0.03),
                        (mw2 * 0.6, l0 + 0.012), (0.0, l0 + 0.016), (-mw2 * 0.6, l0 + 0.012), (-mw2 * 1.06, l13 + 0.03)]), 3),
           R_MOUST, INK, 1.6)
    # big squarish CLEAR frames (refs 04, 05, 13: pale see-through plastic, not black)
    ew, ecx, ey = L['ew'], L['ecx'], L['eye_y']
    for sgn in (-1, 1):
        cx = sgn * ecx
        w2, h1, h2 = ew * 0.85, 0.085, 0.075
        fr = [(cx - w2, ey - h1), (cx + w2, ey - h1), (cx + w2, ey + h2 * 0.8), (cx + w2 * 0.8, ey + h2),
              (cx - w2 * 0.8, ey + h2), (cx - w2, ey + h2 * 0.8)]
        pts = curve(f.pts(fr), 2)
        p.poly(pts + pts[:1], None, INK, RIM[0])
        p.poly(pts + pts[:1], None, R_FRAME, RIM[1])
        p.line(f.pts([(cx + w2 * 0.2, ey - h1 * 0.6), (cx + w2 * 0.6, ey - h1 * 0.15)]), (246, 246, 244), 1.6)  # a glint
        tip = (sgn * (L['fw'] * 0.5 + 0.01), ey - 0.05)
        p.line(f.pts([(cx + sgn * w2, ey - h1 + 0.02), tip]), INK, 6.4)
        p.line(f.pts([(cx + sgn * w2, ey - h1 + 0.02), tip]), R_FRAME, 4.0)
    for v in (ey - 0.05, ey - h1):                     # the double bridge
        p.line(f.pts([(-ecx + ew * 0.85, v), (0.0, v - 0.008), (ecx - ew * 0.85, v)]), INK, 5.6)
        p.line(f.pts([(-ecx + ew * 0.85, v), (0.0, v - 0.008), (ecx - ew * 0.85, v)]), R_FRAME, 3.4)
    # the hair: short tight curls close to the head, greying a little (ref 13)
    fhw = L['fhw']
    side = [(fhw * 0.5 + 0.015, 0.31), (fhw * 0.5 + 0.03, 0.12), (fhw * 0.5 * 0.86, 0.0), (fhw * 0.5 * 0.86, 0.08),
            (fhw * 0.5 * 0.97, 0.29)]
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.5:
            continue
        p.poly(curve(f.pts([(sgn * u, v) for u, v in side]), 3), R_HAIR_SIDE, INK, 2.0)
    top = [(-fhw * 0.5 * 0.92, 0.03), (-fhw * 0.5 - 0.035, -0.07), (-fhw * 0.5 * 0.92, -0.2), (-0.24, -0.3),
           (-0.1, -0.34), (0.04, -0.35), (0.18, -0.33), (0.28, -0.28), (fhw * 0.5 * 0.94, -0.2), (fhw * 0.5 + 0.035, -0.07),
           (fhw * 0.5 * 0.92, 0.03), (0.22, 0.05), (0.08, 0.035), (-0.06, 0.045), (-0.22, 0.035)]
    hp = curve(f.pts(top), 6)
    cx0 = sum(q[0] for q in hp) / len(hp)
    cy0 = f.top - 0.12 * H
    bumpy = []                                         # messy curls: uneven clumps all round the top and sides
    for i, q in enumerate(hp):
        if q[1] < f.top + 0.02 * H:
            a = 7.0 * abs(math.sin(i * 0.9)) ** 0.6 * (0.6 + 0.4 * math.sin(i * 2.3) ** 2)
            dx, dy = q[0] - cx0, q[1] - cy0
            n = math.hypot(dx, dy) or 1.0
            bumpy.append((q[0] + dx / n * a, q[1] + dy / n * a))
        else:
            bumpy.append(q)
    p.poly(bumpy, R_HAIR, INK, 2.4)
    for k in range(22):                                # curl marks inside (darker, a few grey hairs)
        x, y = f(rng.uniform(-0.3, 0.3), rng.uniform(-0.3, -0.01))
        c = (104, 100, 100) if k % 5 == 0 else (14, 12, 14)
        r = rng.uniform(3.5, 6)
        p.line([(x + r * math.cos(a), y + r * 0.8 * math.sin(a)) for a in np.linspace(0.4, 4.6, 8)], c, 1.4)
    return fx


def romesh_torso(img, p, sp, t):
    """Rust-orange double-breasted suit over a teal crew-neck top (refs 03, 09, 13)."""
    p.poly([(-34, -36), (34, -36), (40, 10), (0, 40), (-40, 10)], R_TEAL, INK, 2.0)          # the top's neck
    p.line([(-30, -26), (0, -18), (30, -26)], dk(R_TEAL, 0.75), 1.6)
    for sgn in (-1, 1):                                # wide peaked lapels
        p.poly([(sgn * 40, -4), (sgn * 74, 24), (sgn * 64, 60), (sgn * 82, 84), (sgn * 14, 236), (sgn * 26, 120)],
               R_RUST, INK, 2.2)
        p.line([(sgn * 70, 62), (sgn * 30, 168)], dk(R_RUST, 0.8), 1.2)
    p.poly([(-40, 10), (0, 40), (40, 10), (24, 140), (0, 200), (-24, 140)], R_TEAL, INK, 2.0)
    for bx in (-34, 34):                                # the double-breasted buttons
        for by in (270, 340):
            p.ell(bx, by, 7, 7, dk(R_RUST, 0.7), INK, 1.4)


# ---------------------------------------------------------------------------------------------- Bash
S_SKIN = (238, 204, 182)
S_HAIR = (88, 60, 42)
S_HAIR_L = (126, 90, 62)
S_STUB = (222, 190, 172)
S_LIP = (204, 140, 128)
S_NAVY = (34, 40, 62)
S_CHECK = (66, 76, 104)


def bash_hair_back(p, sp, hx, hy):
    L = layout(target('bash', sp.get('average', False)))
    f = Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    fw = L['fw']
    p.poly(curve(f.pts([(-fw * 0.5 - 0.07, 0.0), (-fw * 0.5 - 0.09, 0.4), (-fw * 0.5 - 0.04, 0.66), (-fw * 0.3, 0.6),
                        (fw * 0.3, 0.6), (fw * 0.5 + 0.04, 0.66), (fw * 0.5 + 0.09, 0.4), (fw * 0.5 + 0.07, 0.0),
                        (0.0, -0.3)]), 4), S_HAIR, INK, 2.4)


def bash_head(img, p, sp, t, hx, hy):
    L = layout(target('bash', sp.get('average', False)))
    f = Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin = S_SKIN
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.5:
            continue
        ex, ey = f(sgn * (L['fw'] * 0.5 + 0.01), 0.43)
        p.poly(oval(ex, ey, 10, 21, 20), skin, INK, 2.4)
    out = curve(f.pts(outline_uv(L, 0.3)), 4)
    p.poly(out, skin, INK, 2.6)
    # light stubble (refs 18-20): a faint tint on the jaw, chin and over the lip, no outline of its own
    fw, jw, ny, l0 = L['fw'], L['jw'], L['nose_y'], L['lip0']
    stub = [(fw * 0.5 - 0.004, 0.5), (jw * 0.5 - 0.004, 0.82), (jw * 0.15, 0.985), (0.0, 0.995), (-jw * 0.15, 0.985),
            (-jw * 0.5 + 0.004, 0.82), (-fw * 0.5 + 0.004, 0.5), (-fw * 0.36, 0.62), (-L['mw'] * 0.62, L['lip13'] + 0.03),
            (-L['mw'] * 0.55, l0 - 0.01), (-L['nw'] * 0.45, ny + 0.01), (L['nw'] * 0.45, ny + 0.01), (L['mw'] * 0.55, l0 - 0.01),
            (L['mw'] * 0.62, L['lip13'] + 0.03), (fw * 0.36, 0.62)]
    p.poly(curve(f.pts(stub), 4), S_STUB, None)
    p.poly(out, None, INK, 2.6)
    eyes(p, f, L, sp, (92, 68, 44), dk(skin, 0.84), wide=sp.get('wide', 0.0))
    brows(p, f, L, (62, 42, 30), 0.042, sp.get('brow_up', 0.0), sp.get('frown', 0.0))
    nose(p, f, L, skin)
    fx, my = f(0.0, L['lip13'])
    lips(p, f, L, sp, S_LIP, (fx, my - 6))
    # the hair: swept across from his right (our left) with long wavy locks falling over the brow to the eyebrows on
    # our left, full and wide past the ears (refs 06, 18, 19)
    fhw = L['fhw']
    hair = [(-fw * 0.5 - 0.06, 0.5), (-fw * 0.5 - 0.11, 0.44), (-fw * 0.5 - 0.08, 0.36),   # a flicked end by the ear
            (-fw * 0.5 - 0.12, 0.2), (-fhw * 0.5 - 0.1, -0.04), (-fhw * 0.5 - 0.04, -0.2), (-0.3, -0.34),
            (-0.18, -0.42), (-0.04, -0.44), (0.06, -0.4), (0.16, -0.45), (0.3, -0.38), (fhw * 0.5 + 0.06, -0.24),
            (fhw * 0.5 + 0.11, -0.06), (fw * 0.5 + 0.12, 0.18), (fw * 0.5 + 0.08, 0.34), (fw * 0.5 + 0.12, 0.44),
            (fw * 0.5 + 0.05, 0.5), (fw * 0.5 + 0.005, 0.36), (fhw * 0.5 - 0.01, 0.12),
            (0.26, 0.02), (0.16, 0.06), (0.1, 0.0), (0.03, 0.09),             # the sweep's lower edge, dipping to our left
            (-0.04, 0.2), (-0.08, 0.12), (-0.13, 0.22), (-0.18, 0.13),        # locks falling over the brow
            (-0.24, 0.2), (-0.28, 0.1), (-fhw * 0.5 + 0.01, 0.12), (-fw * 0.5 - 0.005, 0.36)]
    p.poly(curve(f.pts(hair), 4), S_HAIR, INK, 2.4)
    for a, b in (((-0.2, -0.34), (-0.06, 0.14)), ((-0.04, -0.38), (0.06, 0.02)), ((0.14, -0.38), (0.24, -0.02)),
                 ((-0.34, -0.16), (-0.22, 0.14)), ((0.28, -0.28), (0.38, 0.14)), ((-0.4, 0.1), (-0.46, 0.4)),
                 ((0.42, 0.1), (0.48, 0.4))):
        p.line(curve(f.pts([a, ((a[0] + b[0]) / 2 + 0.03, (a[1] + b[1]) / 2), b]), 3), S_HAIR_L, 1.8)
    return fx


def bash_torso(img, p, sp, t):
    """Dark navy tartan suit, white shirt open at the collar (refs 04, 06, 13)."""
    p.poly([(-30, -40), (30, -40), (44, 8), (12, 120), (0, 150), (-12, 120), (-44, 8)], (248, 248, 246), INK, 2.0)
    p.poly([(-12, -6), (12, -6), (0, 60)], S_SKIN, INK, 1.6)                                   # the open neck
    for sgn in (-1, 1):
        p.poly([(sgn * 30, -40), (sgn * 52, -6), (sgn * 12, -6)], (248, 248, 246), INK, 1.8)  # the collar points
        p.poly([(sgn * 44, -2), (sgn * 70, 26), (sgn * 54, 104), (sgn * 66, 140), (sgn * 8, 280), (sgn * 18, 140)],
               sp.get('jacket', S_NAVY), INK, 2.2)
    p.ell(0, 300, 6, 6, (20, 24, 38), INK, 1.4)


def tartan(p, j2, view, sp, x0, x1, y0, y1):
    """A quiet navy check over the jacket: a few lighter lines each way (ref 04)."""
    for k in range(int(x0) // 46 * 46, int(x1), 46):
        p.line([(k, y0), (k, y1)], S_CHECK, 1.4)
    for k in range(int(y0) // 46 * 46, int(y1), 46):
        p.line([(x0, k), (x1, k)], S_CHECK, 1.4)


# ---------------------------------------------------------------------------------------------- Claudia (new look)
CREAM = (240, 230, 208)
GOLD = (214, 172, 78)


CL_TAPER = 0.62     # the hair curtains' inner edge at the jaw, as a share of the face's width (thin face: Sam)
CL_CHIN = 0.26


def claudia_head(img, p, sp, t, hx, hy):
    """Claudia's face from her measurements (the Traitors film's head failed the likeness check: 35%, 3rd in the
    line-up), keeping that head's look: the heavy blunt fringe to just above the eyes, long straight black curtains past
    the jaw, smoky eyes with lashes, nude lips with the knowing half smile (refs 01, 03, 11, 21-23)."""
    L = layout(target('claudia', sp.get('average', False)))
    f = Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin = TC.C_SKIN
    out = curve(f.pts(outline_uv(L, CL_CHIN)), 4)
    p.poly(out, skin, INK, 2.6)
    w = L['ew'] * H / 2
    h = L['eh'] * H / 1.8 * (1 + 0.55 * sp.get('wide', 0.0))
    st = dict(lid=sp.get('lid4', 0.16), look=sp.get('look', 0.0), squint=sp.get('squint', 0.0),
              closed=sp.get('blink', False), gaze_dy=sp.get('gaze_dy', 0.0))
    for sgn in (-1, 1):
        ex, ey = f(sgn * L['ecx'], L['eye_y'])
        TC.eye(p, ex, ey, sgn, w * (1 - 0.3 * f.tq if sgn < 0 else 1.0), h, (52, 40, 38), st, (150, 120, 124),
               liner=3.4, lower=2.2, lashes=True, smoky=(176, 146, 136))
    nose(p, f, L, skin)
    for sgn in (-1, 1):                                # cheekbones
        p.line(f.pts([(sgn * L['fw'] * 0.36, 0.47), (sgn * L['fw'] * 0.32, 0.6)]), dk(skin, 0.9), 1.4)
    fx, my = f(0.0, L['lip13'])
    lips(p, f, L, dict(sp, smile=sp.get('smile', 0.6)), TC.C_LIP, (fx, my - 6))
    fw, fhw, fr = L['fw'], L['fhw'], L['lid_top'] - 0.035
    hair = [(-0.16, 1.85), (-fw * 0.5 - 0.24, 1.85), (-fw * 0.5 - 0.19, 1.0), (-fw * 0.5 - 0.13, 0.25),
            (-fhw * 0.5 - 0.09, -0.1), (-fhw * 0.5 * 0.7, -0.27), (0.0, -0.31), (fhw * 0.5 * 0.7, -0.27),
            (fhw * 0.5 + 0.09, -0.1), (fw * 0.5 + 0.13, 0.25), (fw * 0.5 + 0.19, 1.0), (fw * 0.5 + 0.24, 1.85),
            (0.16, 1.85), (fw * 0.5 * CL_TAPER, 0.9), (fw * 0.5 + 0.005, 0.5), (fw * 0.5 - 0.01, fr + 0.05),
            (fw * 0.3, fr), (0.0, fr + 0.008), (-fw * 0.3, fr), (-fw * 0.5 + 0.01, fr + 0.05),
            (-fw * 0.5 - 0.005, 0.5), (-fw * 0.5 * CL_TAPER, 0.9)]
    p.poly(f.pts(hair), TC.C_HAIR, INK, 2.6)
    for k in range(9):                                 # the fringe's blunt ends and a sheen across the crown
        u = -fw * 0.42 + k * fw * 0.105
        p.line(f.pts([(u, fr - 0.2), (u + 0.01, fr - 0.01)]), (50, 50, 60), 1.2)
    p.line(curve(f.pts([(-0.26, -0.2), (0.0, -0.25), (0.26, -0.2)]), 3), TC.C_SHEEN, 2.4)
    for sgn in (-1, 1):
        p.line(f.pts([(sgn * (fw * 0.5 + 0.08), 0.2), (sgn * (fw * 0.5 + 0.15), 1.4)]), TC.C_SHEEN, 1.8)
    return fx


def claudia4_torso(img, p, sp, t):
    """Black tailored jacket over a cream high-neck tie blouse with a fine gold chain (refs 03, 11)."""
    p.poly([(-34, -50), (34, -50), (42, 6), (24, 160), (0, 210), (-24, 160), (-42, 6)], CREAM, INK, 2.0)
    p.line([(-32, -34), (32, -34)], dk(CREAM, 0.86), 1.4)
    for sgn in (-1, 1):                                # the tie: two soft loops and two short tails at the throat
        p.poly(curve([(0, -6), (sgn * 22, -16), (sgn * 28, -2), (sgn * 18, 4)], 3), CREAM, INK, 1.6)
        p.poly([(sgn * 2, -2), (sgn * 14, 40), (sgn * 6, 44), (sgn * 0, 4)], dk(CREAM, 0.95), INK, 1.4)
    p.ell(0, -4, 7, 6, dk(CREAM, 0.92), INK, 1.4)
    p.line(curve([(-30, -20), (-20, 30), (0, 52), (20, 30), (30, -20)], 4), GOLD, 2.4)     # the gold chain
    for sgn in (-1, 1):
        p.poly([(sgn * 42, -2), (sgn * 66, 30), (sgn * 46, 110), (sgn * 62, 150), (sgn * 6, 250), (sgn * 24, 150)],
               sp.get('jacket', (30, 28, 32)), INK, 2.2)


# ---------------------------------------------------------------------------------------------- the Patriot's eyes
def patriot_eyes(p, view, sp, hx, hy):
    """The Patriot's wide-eyed stare, drawn in the library's own eye style (Sam, 1 Nov: "I prefer the first style, the
    original"): burnham's almond eye with its ink outline, lid line and round pupil, and the library's straight brows,
    only bigger and raised as the stare grows. sp['stare'] 1..4 = its strength; sp['look'] -1..1 where the pupils point.
    The library has already drawn its own eyes and (hidden: brow_c set to the skin by the film) brows underneath; these
    cover them. The narrowed eyes of "Traitors." are the library's own (brows 'fierce', lid 3)."""
    k = sp.get('stare')
    if view != 'front' or k is None:
        return
    k = float(k)
    hw = sp.get('hw', 76)
    fx = hx + sp.get('turn', 0.0) * hw * 0.22
    look = sp.get('look', 0.0)
    bc, bw = sp.get('brow_c_real', (104, 74, 54)), sp.get('brow_w', 3.2)
    sx, sy = 1.0 + 0.06 * k, 1.0 + 0.2 * k                  # wider a little, taller a lot: the eyes widen
    for sgn in (-1, 1):
        ex, ey = fx - 4 + sgn * 30, hy - 8
        if sp.get('blink'):
            p.line([(ex - 16, ey), (ex, ey + 3), (ex + 16, ey)], INK, 2.4)
        else:
            top = [(ex - 17 * sx, ey), (ex - 8 * sx, ey - 8 * sy), (ex + 8 * sx, ey - 8 * sy), (ex + 17 * sx, ey)]
            bot = [(ex - 17 * sx, ey), (ex - 8 * sx, ey + 7 * sy), (ex + 8 * sx, ey + 7 * sy), (ex + 17 * sx, ey)]
            almond = top + bot[::-1][1:-1]
            p.poly(almond, (250, 250, 248), INK, 2.0)
            cx, cy = ex + look * 7 * sx, ey + 1
            circ = [(cx + 4.5 * math.cos(a), cy + 4.5 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24, endpoint=False)]
            ir = TC.clip_convex(almond[::-1], circ)
            if len(ir) >= 3:
                p.poly(ir, INK, None)
            p.line(top, INK, 2.6)
        lift = 1.6 * k                                        # the library's straight brow, raised with the stare
        p.line([(ex - sgn * 6, ey - 22 - lift), (ex + sgn * 20, ey - 20 - lift * 0.3)], bc, bw)


# ---------------------------------------------------------------------------------------------- the hooks
TC.HEADS.update(romesh=romesh_head, bash=bash_head,
                claudia4=TC.claudia_head)   # Sam, 1 Nov: The Traitors film's Claudia face (thin), this film's outfit
TC.TORSOS.update(romesh=romesh_torso, bash=bash_torso, claudia4=claudia4_torso)
_hair_back = B.hair_back


def hair_back(p, sp, hx, hy, hw, hh):
    w = sp.get('who')
    if w == 'claudia4':
        return TC.claudia_hair_back(p, sp, hx, hy, hw, hh)
    if w == 'bash':
        return bash_hair_back(p, sp, hx, hy)
    return _hair_back(p, sp, hx, hy, hw, hh)


B.hair_back = hair_back

ROMESH = dict(who='romesh', name='Romesh', skin=R_SKIN, hw=70, hh=92, head_dy=10, outfit='suit', jacket=R_RUST,
              sleeve=R_RUST, trousers=R_RUST, shirt=R_TEAL, shoe=(236, 234, 228), shoulders=156, full=True,
              pose='custom', seed=41)
BASH = dict(who='bash', name='Bash', skin=S_SKIN, hw=70, hh=92, head_dy=10, outfit='suit', jacket=S_NAVY,
            sleeve=S_NAVY, trousers=S_NAVY, shirt=(248, 248, 246), shoe=(30, 26, 22), shoulders=146, full=True,
            pose='custom', seed=42)
CLAUDIA = dict(TC.CLAUDIA, who='claudia4', jacket=(30, 28, 32), sleeve=(30, 28, 32), trousers=(30, 28, 32),
               shirt=CREAM, shoe=(20, 20, 20), seed=43)
PATRIOT = P3.PATRIOT
CAST = {'claudia': CLAUDIA, 'patriot': PATRIOT, 'romesh': ROMESH, 'bash': BASH}
HEIGHTS = {'Romesh': 1.78, 'Bash': 1.78, 'Patriot': 1.78, 'Claudia': 1.70}
P3.HEIGHTS.update(HEIGHTS)                             # patriots3_cast.person applies the real height by name


def person(img, cam, x, y, s, sp, t=0.0, yaw=0, j=None, head_yaw=None):
    if sp.get('who') == 'patriot':
        j = j or V.standing(sp)
        if patriot_eyes not in j.get('head_props', []):
            j['head_props'] = j.get('head_props', []) + [patriot_eyes]   # after the balaclava (P3 puts it first)
    return P3.person(img, cam, x, y, s, sp, t, yaw, j, head_yaw)


# ---------------------------------------------------------------------------------------------- the cast sheet
SCORES = {   # likeness.py check (rule 49), 1 Nov: `python3 source/patriots4_cast.py likeness OUT_DIR` re-measures
    'romesh': 'photo 14: 74%, 1st of 6, in the series look (ref 13). Photo 16 disagrees (the tool matches his own two photos 17%)',
    'bash': 'photo 18: 88%, 1st of 6; photo 19: 91%, 1st of 6',
    'claudia': 'photo 21: 80%, 1st of 6; photo 22: 68%, 1st of 6 (rebuilt: the Traitors head scored 35%, 3rd)',
}
FACES = {   # the faces each one needs in the film (labels for the sheet)
    'claudia': [('asking', dict(mouth='v:AI')), ('staring', dict(look=0.9, smile=0.0)), ('blink', dict(blink=True, smile=0.0)),
                ('knowing smile', dict())],
    'bash': [('talking', dict(mouth='v:E')), ('moved, eyes shut', dict(blink=True, frown=-0.03, brow_up=0.01)),
             ('staring', dict(look=0.9, wide=0.3)), ('eyes slide', dict(look=-0.9))],
    'romesh': [('talking', dict(mouth='v:etc')), ('sincere', dict(frown=-0.015)), ('eyes slide', dict(look=0.9)),
               ('still', dict())],
}


def _flat():
    cam = B.Cam(1.0, 540, 960)
    cam.P = lambda x, y: (x, y)
    cam.S = lambda v: v
    return cam


def sheet(out):
    """The cast sheet: everyone in the pose and view the film shows them in, at their real heights on one floor, with
    the body landmarks and a 1.75 m person and a 1 m ruler; the faces large with the likeness scores beside the photos;
    and the Patriot's stare as a numbered strength sheet (1 = slight, 6 = huge) for Sam to pick from."""
    import landmarks
    import posegallery as PG
    import sizes
    B.SS = 1
    W, Hh = 3000, 3420
    img = Image.new('RGBA', (W, Hh), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    big, mid, small = (ImageFont.truetype(FONT, n) for n in (44, 30, 24))
    d.text((30, 18), 'PATRIOTS 4: the cast (likeness heads measured; real heights; poses from the gallery)', font=big,
           fill=(30, 30, 30))
    cam = _flat()
    s = 0.62
    floor = 900
    row = [('claudia', 0, PG.hands_on_table, 'Claudia, front\n(hands on the table, ref 03)'),
           ('bash', 0, PG.palms_together, 'Bash, front\n(hands together, shot 2)'),
           ('romesh', 0, PG.hands_on_table, 'Romesh, front\n(hands on the table, shot 3)'),
           ('patriot', 0, PG.point_both, 'The Patriot, front\n("Traitors.", shot 12)'),
           ('patriot', 0, None, 'The Patriot, front\n(the stare, shots 5-11)'),
           ('patriot', 180, None, 'The Patriot from behind\n(his shoulder, shot 9)')]
    for i, (who, yaw, build, label) in enumerate(row):
        sp = dict(CAST[who], mouth='rest')
        if who == 'patriot' and build is not None:
            sp['brows'], sp['lid'] = 'fierce', 3
        elif who == 'patriot' and yaw == 0:
            sp['stare'] = 3
            sp['brow_c_real'], sp['brow_c'] = sp.get('brow_c', (104, 74, 54)), sp['skin']
        lay = Image.new('RGBA', (740, 980), (0, 0, 0, 0))     # wide: the pointing hands reach far out
        s2 = P3.scale_for(sp, s)
        if i == 0:
            landmarks.draw(ImageDraw.Draw(lay), 370, floor - 928 * s2, s2, 400)
        person(lay, cam, 370, floor - 928 * s2, s, sp, 0.0, yaw, build(sp) if build else None)
        img.alpha_composite(lay, (30 + 450 * i - 150 + (60 if i >= 3 else 0) + (90 if i >= 4 else 0), 80))
        for k, line in enumerate(label.split('\n')):
            d.text((250 + 450 * i + (60 if i >= 3 else 0) + (90 if i >= 4 else 0), 1000 + 30 * k), line, font=small, fill=(40, 40, 40), anchor='mm')
    lay = Image.new('RGBA', (200, 980), (0, 0, 0, 0))
    sizes.scale_ref(ImageDraw.Draw(lay), 100, floor, s / V.M_PER_UNIT)
    img.alpha_composite(lay, (2790, 80))
    d.text((2860, 1060), '1.75 m, 1 m', font=small, fill=(40, 40, 40), anchor='mm')
    d.text((1500, 64), 'heights: Romesh, Bash, the Patriot 1.78 m; Claudia 1.70 m', font=small, fill=(40, 40, 40))
    # the faces, each beside its photo, with the likeness score
    y0 = 1080
    for r, who in enumerate(('claudia', 'bash', 'romesh')):
        y = y0 + r * 560
        ph = Image.open(os.path.join(REFS, PHOTOS[who][0])).convert('RGB')
        ph.thumbnail((380, 470))
        img.paste(ph, (30, y + 40))
        d.text((30, y), f"{CAST[who]['name']}: likeness {SCORES[who]}", font=mid, fill=(30, 30, 30))
        for c, (label, extra) in enumerate(FACES[who]):
            lay = Image.new('RGBA', (600, 520), (0, 0, 0, 0))
            q = dict(dict(CAST[who], mouth='rest'), **extra)
            person(lay, cam, 300, 440, 1.5, q, 0.0, 0)
            img.alpha_composite(lay.crop((40, 0, 560, 480)).resize((476, 440)), (440 + 630 * c, y + 50))
            d.text((678 + 630 * c, y + 510), label, font=small, fill=(40, 40, 40), anchor='mm')
    # the Patriot's stare: the numbered strength sheet, then the looks the film needs
    y = y0 + 3 * 560 + 10
    d.text((30, y), "The Patriot's wide-eyed stare (shots 5-11): Sam chose: from 1 slowly up to 4.  Then: eyes sliding "
           'to Romesh (shot 8), and narrowed for "Traitors." (shot 12)', font=mid, fill=(30, 30, 30))
    faces = [(str(k), dict(stare=k)) for k in range(1, 7)] + [('to Romesh', dict(stare=3, look=-0.9)),
                                                                ('"Traitors."', dict(narrow=True, mouth='v:etc'))]
    for c, (label, extra) in enumerate(faces):
        lay = Image.new('RGBA', (600, 520), (0, 0, 0, 0))
        person(lay, cam, 300, 440, 1.5, dict(dict(PATRIOT, mouth='rest'), **extra), 0.0, 0)
        img.alpha_composite(lay.crop((60, 0, 540, 480)).resize((350, 350)), (30 + 370 * c, y + 60))
        d.text((205 + 370 * c, y + 430), label, font=mid if len(label) < 3 else small, fill=(20, 20, 20), anchor='mm')
    img.convert('RGB').save(out, quality=88)
    return out


def LINE_SUBJECTS():
    """Each of the cast alone, large, for the line-work check (linecheck.py)."""
    def one(sp):
        def draw(im):
            person(im, B.Cam(1.0, 540, 960), 540, 420, 1.3, dict(sp), 0.0, 0)
        return draw
    return [(k, one(sp)) for k, sp in CAST.items()]


# ---------------------------------------------------------------------------------------------- the likeness check
PHOTOS = {
    'romesh': ['14-romesh-straight-1.jpg', '16-romesh-straight-2.jpg'],
    'bash': ['18-bash-straight-1.jpg', '19-bash-straight-2-hand.jpg'],
    'claudia': ['21-claudia-straight-1.jpg', '22-claudia-straight-2.jpg'],
}
OTHERS = {   # the line-up: our drawing must sit nearer its own person than any of these famous faces
    'romesh': ['patriots-4/18-bash-straight-1.jpg', 'patriots-4/21-claudia-straight-1.jpg',
               'newsdesk/netanyahu-1-front.jpg', 'shocking/farage-5-front.jpg', 'traitors/25-putin-front-close.jpg'],
    'bash': ['patriots-4/14-romesh-straight-1.jpg', 'patriots-4/21-claudia-straight-1.jpg',
             'newsdesk/netanyahu-1-front.jpg', 'shocking/farage-5-front.jpg', 'traitors/25-putin-front-close.jpg'],
    'claudia': ['patriots-4/14-romesh-straight-1.jpg', 'patriots-4/18-bash-straight-1.jpg',
                'newsdesk/netanyahu-1-front.jpg', 'shocking/farage-5-front.jpg', 'traitors/25-putin-front-close.jpg'],
}


def head_png(who, out, average=False):
    """One head, large, front on, on a plain light ground (what likeness.py check measures)."""
    B.SS = 1
    img = Image.new('RGBA', (700, 820), (236, 234, 230, 255))
    sp = dict(CAST[who], average=average, mouth='rest')
    cam = B.Cam(1.0, 540, 960)
    cam.P = lambda x, y: (x, y)
    cam.S = lambda v: v
    person(img, cam, 350, 640, 2.0, sp, 0.0, 0)
    img.convert('RGB').save(out)
    return out


def likeness(out_dir):
    import subprocess
    os.makedirs(out_dir, exist_ok=True)
    for who in ('romesh', 'bash', 'claudia'):
        ours = head_png(who, os.path.join(out_dir, f'{who}.png'))
        head_png(who, os.path.join(out_dir, f'{who}-average.png'), average=True)
        refs = os.path.join(HERE, '..', 'references')
        for ph in PHOTOS[who]:
            cmd = [sys.executable, os.path.join(HERE, 'likeness.py'), 'check', os.path.join(REFS, ph), ours,
                   os.path.join(out_dir, f'{who}-check-{ph[:2]}.jpg'), '--others'] + [os.path.join(refs, o) for o in OTHERS[who]]
            r = subprocess.run(cmd, capture_output=True, text=True)
            print(f'--- {who} vs {ph}')
            print('\n'.join(x for x in (r.stdout + r.stderr).splitlines()
                            if not any(w in x for w in ('WARN', 'W0000', 'INFO', 'Logging', 'I0000'))))


def main():
    a = sys.argv[1:]
    if a[0] == 'head':
        print(head_png(a[1], a[2], '--average' in a))
    elif a[0] == 'likeness':
        likeness(a[1])
    elif a[0] == 'sheet':
        print(sheet(a[1]))


if __name__ == '__main__':
    main()
