#!/usr/bin/env python3
"""MAP  MidTerminal (Sam, 4 Nov): the cast. Satan (new, an original design), Jeffrey Epstein (new, a measured likeness
head), Donald Trump (reused from traitors_cast; his turned views fixed here: blond hair and his brows, not the library's
brown default). References: references/midterminal/.

    SATAN    humanoid, in a suit (refs satan-1, -2; Sam's picks: the black suit of ref 1 with ref 2's horns and red
             wings, kept modest so the suit reads): black two-button suit, white shirt, dark red tie, white pocket
             square, a small gold lapel pin; black hair slicked straight back to a widow's peak; pale skin; a long
             narrow face with sharp cheekbones and a hard jaw; brows angled up at the outside; red irises (flat red,
             no glow: house style); curved dark horns rising from the hairline and bending in (ref 2's lyre shape,
             smaller); dark red feathered wings behind the shoulders. 1.88 m.
    EPSTEIN  from MEASUREMENTS (likeness.py card on epstein-1, -2; ref 3 is turned 28 degrees, left out): a wide nose,
             a wide mouth, a long gap from nose to lip, a long narrow face, a long chin, close-set small eyes drooping
             at the outer corners. Big grey hair swept back and up, wide past the ears; a tanned, lined face (forehead
             lines, crow's feet, folds nose to mouth); the closed half-smile (refs 1, 2). Dark navy-black short-sleeved
             polo (ref 3, Sam's pick), three-button placket, collar. 1.83 m.
    TRUMP    traitors_cast.TRUMP (navy suit, long red tie, flag pin; the pout, the swept blond hair); 1.90 m.

Moods: Satan 'neutral' (a cold closed smile), 'smirk', 'stern', 'fury' + talking (sp['mouth'] = 'v:SHAPE').
Epstein 'neutral' (the half-smile), 'stern' + talking.

    python3 source/midterminal_cast.py sheet OUT.jpg        every view of all three, faces large, a 1.75 m person
    python3 source/midterminal_cast.py head WHO OUT.png     one head large, straight on (for likeness.py check)

Map: colours 50-75 | Satan head 78 | wings 170 | Satan torso 225 | Epstein head 245 | polo 330 | hooks 350 |
specs 395 | sheet 420 | heads 500
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import traitors_cast as TC       # noqa: E402  (Trump; installs the head hooks into burnham)
import patriots4_cast as P4      # noqa: E402  (the measured-face layout: layout, Face, eyes, brows, nose, lips)
import views as V                # noqa: E402
from ed import INK, curve, oval  # noqa: E402

dk, blend = TC.dk, TC.blend
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')

# ---------------------------------------------------------------------------------------------- colours
S_SKIN = (236, 216, 204)          # pale
S_HAIR = (22, 20, 24)
S_HAIR_L = (64, 62, 72)           # the sheen on the slicked hair
S_IRIS = (214, 28, 34)            # red eyes, flat (no glow)
S_LID = (196, 164, 160)
S_LIP = (176, 112, 108)
S_HORN = (44, 34, 34)
S_HORN_L = (92, 72, 66)
S_SUIT = (26, 26, 30)
S_TIE = (150, 20, 28)
S_WING = (150, 24, 30)
S_WING_D = (100, 14, 22)
S_WING_L = (196, 48, 46)
GOLD = (214, 172, 78)

E_SKIN = (226, 162, 122)          # tanned
E_HAIR = (196, 192, 186)
E_HAIR_D = (150, 144, 138)
E_HAIR_L = (228, 226, 222)
E_IRIS = (96, 120, 136)           # grey-blue (ref 1)
E_LIP = (190, 118, 100)
E_POLO = (30, 34, 46)             # navy-black (ref 3)

# Epstein's measured face (likeness.py card, 4 Nov, refs epstein-1 and -2), into the patriots4 tables
P4.MEASURED['epstein'] = dict(face_wide=0.784, jaw_wide=0.822, forehead_wide=0.913, eyes_apart=1.231, eye_size=0.177,
                              eye_open=0.324, eye_tilt=0.382, brow_high=0.554, brow_slope=-12.109, nose_long=0.386,
                              nose_wide=0.762, mouth_wide=0.951, lip_top=0.106, lip_low=0.151, philtrum=0.164,
                              chin_long=0.342)
P4.PUSH['epstein'] = 1.6
P4.TUNE['epstein'] = {}

# Satan is an original face, laid out on the same average face and moved by hand: long and narrow, a narrow sharp jaw,
# a long nose, narrow eyes, brows high at the outside (the classic devil's arch), thin lips, a long chin.
SATAN_FACE = dict(P4.AVG, face_wide=0.80, jaw_wide=0.70, forehead_wide=0.98, eyes_apart=1.30, eye_size=0.19,
                  eye_open=0.34, eye_tilt=7.0, brow_high=0.50, brow_slope=16.0, nose_long=0.46, nose_wide=0.56,
                  mouth_wide=0.80, lip_top=0.07, lip_low=0.11, philtrum=0.12, chin_long=0.34)


# ---------------------------------------------------------------------------------------------- Satan's head
def _horn(p, base, up, curl, length, w):
    """One horn: from its base on the head, rising (`up`, a unit direction), curling by `curl` (radians over its
    length), tapering from width w to a point. Ridged bands across it."""
    pts_l, pts_r, spine = [], [], []
    x, y = base
    a = math.atan2(up[1], up[0])
    n = 14
    for k in range(n + 1):
        u = k / n
        wk = w * (1 - u) ** 0.8
        nx, ny = -math.sin(a), math.cos(a)
        spine.append((x, y, nx, ny, wk))
        pts_l.append((x + nx * wk, y + ny * wk))
        pts_r.append((x - nx * wk, y - ny * wk))
        x += math.cos(a) * length / n
        y += math.sin(a) * length / n
        a += curl / n
    shape = pts_l + pts_r[::-1]
    p.poly(shape, S_HORN, INK, 2.2)
    for k in (3, 6, 9):                                # ridges
        x, y, nx, ny, wk = spine[k]
        p.line([(x + nx * wk * 0.9, y + ny * wk * 0.9), (x - nx * wk * 0.9, y - ny * wk * 0.9)], S_HORN_L, 1.4)
    x, y, nx, ny, wk = spine[2]                        # a pale streak up the near side
    x2, y2, _, _, _ = spine[8]
    p.line([(x + nx * wk * 0.4, y + ny * wk * 0.4), (x2, y2)], S_HORN_L, 1.6)


def satan_horns(p, f, L, behind):
    """Ref 2's lyre-shaped horns, smaller: from the top of the brow either side, rising, bowing out and curling back
    in towards each other. `behind`: only the parts behind the head (none: both sit in front of the hair)."""
    fhw = L['fhw']
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.5:
            continue
        bx, by = f(sgn * fhw * 0.36, -0.12)
        _horn(p, (bx, by), (sgn * 0.42, -1.0), -sgn * 0.95, 0.4 * P4.H, 12)


def satan_head(img, p, sp, t, hx, hy):
    L = P4.layout(SATAN_FACE)
    f = P4.Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin = S_SKIN
    mood = sp.get('mood', 'neutral')
    for sgn in (-1, 1):                                # pointed ears, set high
        if sgn < 0 and f.tq > 0.5:
            continue
        ex, ey = f(sgn * (L['fw'] * 0.5 + 0.01), 0.40)
        p.poly([(ex, ey + 22), (ex + sgn * 14, ey + 8), (ex + sgn * 22, ey - 30), (ex + sgn * 6, ey - 16), (ex, ey - 14)],
               skin, INK, 2.2)
        p.line([(ex + sgn * 4, ey + 8), (ex + sgn * 12, ey - 14)], dk(skin, 0.75), 1.4)
    out = curve(f.pts(P4.outline_uv(L, 0.26)), 4)
    p.poly(out, skin, INK, 2.6)
    sd = dk(skin, 0.84)
    for sgn in (-1, 1):                                # sharp cheekbones, hollow cheeks
        p.line(f.pts([(sgn * L['fw'] * 0.40, 0.46), (sgn * L['fw'] * 0.30, 0.62)]), sd, 2.0)
        p.line(f.pts([(sgn * L['nw'] * 0.6, L['nose_y'] + 0.01), (sgn * L['mw'] * 0.62, L['lip13'] + 0.02)]), sd, 1.6)
    p.line(f.pts([(-0.03, 0.97), (0.0, 0.985), (0.03, 0.97)]), sd, 1.4)    # the cleft chin
    frown = {'stern': 0.012, 'fury': 0.03}.get(mood, 0.0)
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', 0.22 if mood != 'fury' else 0.05)), S_IRIS, S_LID, liner=3.0,
            wide=0.25 if mood == 'fury' else 0.0)
    P4.brows(p, f, L, S_HAIR, 0.034, sp.get('brow_up', 0.0), frown + sp.get('frown', 0.0))
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, L['lip13'])
    if mood == 'fury' and not sp.get('mouth', 'rest').startswith('v:'):
        mw = L['mw'] / 2
        shape = curve(f.pts([(-mw, L['lip13'] - 0.01), (0.0, L['lip0']), (mw, L['lip13'] - 0.01), (mw * 0.7, L['lip17'] + 0.05),
                             (0.0, L['lip17'] + 0.07), (-mw * 0.7, L['lip17'] + 0.05)]), 3)
        p.poly(shape, (70, 20, 24), INK, 2.2)
        p.poly(curve(f.pts([(-mw * 0.8, L['lip13'] - 0.006), (0.0, L['lip0'] + 0.006), (mw * 0.8, L['lip13'] - 0.006),
                            (0.0, L['lip13'] + 0.02)]), 3), (244, 240, 230), None)
        for sgn in (-1, 1):                            # two pointed canines
            cx, cy = f(sgn * mw * 0.45, L['lip13'] + 0.005)
            p.poly([(cx - 5, cy - 4), (cx + 5, cy - 4), (cx, cy + 12)], (250, 248, 240), INK, 1.2)
    else:
        smile = {'neutral': 0.5, 'smirk': 1.0, 'stern': -0.3}.get(mood, 0.4)
        P4.lips(p, f, L, dict(sp, smile=smile), S_LIP, (fx, my - 6))
        if mood == 'smirk' and not sp.get('mouth', 'rest').startswith('v:'):   # one corner tucked up (his left)
            cx, cy = f(L['mw'] / 2, L['lip13'] - 0.01)
            p.line([(cx - 2, cy + 2), (cx + 8, cy - 6)], INK, 2.0)
    # the hair: black, slicked straight back from a sharp widow's peak, tight to the skull, sheen lines
    fw, fhw = L['fw'], L['fhw']
    hl = 0.02                                          # the hairline's sides
    hair = [(-fw * 0.5 - 0.012, 0.36), (-fhw * 0.5 - 0.035, 0.10), (-fhw * 0.5 * 0.78, -0.17), (-0.18, -0.27),
            (0.0, -0.29), (0.18, -0.27), (fhw * 0.5 * 0.78, -0.17), (fhw * 0.5 + 0.035, 0.10), (fw * 0.5 + 0.012, 0.36),
            (fw * 0.5 - 0.015, 0.30), (fhw * 0.5 - 0.02, 0.12), (fhw * 0.5 * 0.8, hl - 0.01), (0.2, hl - 0.03),
            (0.07, hl), (0.0, hl + 0.075), (-0.07, hl), (-0.2, hl - 0.03), (-fhw * 0.5 * 0.8, hl - 0.01),
            (-fhw * 0.5 + 0.02, 0.12), (-fw * 0.5 + 0.015, 0.30)]
    p.poly(f.pts(hair), S_HAIR, INK, 2.6)
    for k in range(-3, 4):                             # combed straight back: sheen lines up from the hairline
        u = k * 0.07
        p.line(curve(f.pts([(u * 0.9, hl + 0.0 - abs(k) * 0.005), (u, -0.12), (u * 1.05, -0.24)]), 3)[:8], S_HAIR_L, 1.4)
    satan_horns(p, f, L, False)
    return fx


def satan_head_view(img, p, sp, t, view, hx, hy):
    """Three-quarter, side and back: the library's head from his keys (black slicked hair), then his horns and red
    eyes on top."""
    _head_view(img, p, dict(sp, who='satan_lib', mood='stern' if sp.get('mood') == 'fury' else sp.get('mood')),
               t, view, hx, hy)
    hw, hh = sp.get('hw', 66), sp.get('hh', 98)
    if view in ('three', 'side', 'three_back', 'back'):
        k = {'three': 0.55, 'side': 0.15, 'three_back': -0.1, 'back': 0.0}[view]
        for sgn in ((-1, 1) if view in ('three', 'back') else (1,)):
            bx = hx + (sgn * hw * 0.42 if view in ('three', 'back') else -hw * 0.05) + k * 10
            by = hy - hh * 0.92
            curl = -sgn * 0.95 if view in ('three', 'back') else 0.5
            dirx = sgn * 0.42 if view in ('three', 'back') else -0.2
            _horn(p, (bx, by), (dirx, -1.0), curl, 0.4 * P4.H, 11)


# ---------------------------------------------------------------------------------------------- the wings
def _wing(p, sgn, spread, view):
    """One wing in the person's own units (neck base at 0, 0): from the shoulder blade, an upper arm up and out, a
    hand down and out, and long feathers hanging from it. sgn -1 = his right (our left in a front view).
    spread 0 (folded against the back) .. 1 (open, ref 2)."""
    s = 0.45 + 0.55 * spread
    root = (sgn * 60, 70)
    wrist = (sgn * (120 + 170 * s), -60 - 90 * s)
    tip = (sgn * (150 + 240 * s), 230 + 30 * (1 - s))
    elbow = (sgn * (95 + 90 * s), 0 - 45 * s)
    lead = curve([root, elbow, wrist, tip], 4)
    # the feather mass: under the leading edge down to a scalloped trailing edge
    n = 9
    trail = []
    for k in range(n + 1):
        u = k / n
        x = tip[0] + (root[0] - tip[0]) * u
        y = tip[1] + (340 - tip[1]) * math.sin(u * math.pi * 0.5) * 0.9 + 40 * u
        trail.append((x, y))
    body = lead + trail[1:]
    p.poly(body, S_WING, INK, 2.6)
    # feather rows: long primaries hanging from the wrist, coverts nearer the arm
    for k in range(1, n):
        u = k / n
        a = trail[k]
        top = (wrist[0] + (root[0] - wrist[0]) * u * 0.9, wrist[1] + (root[1] - wrist[1]) * u * 0.9 + 30)
        p.line(curve([top, ((top[0] + a[0]) / 2 + sgn * 6, (top[1] + a[1]) / 2), a], 3), S_WING_D, 2.0)
    for k in range(n):                                 # the scallops along the trailing edge
        a, b = trail[k], trail[k + 1]
        mid = ((a[0] + b[0]) / 2, max(a[1], b[1]) + 22)
        p.poly(curve([a, mid, b], 3), S_WING, INK, 2.0)
    cov = curve([(root[0] + sgn * 10, root[1] - 10), (elbow[0], elbow[1] + 40), (wrist[0] - sgn * 10, wrist[1] + 70),
                 (wrist[0] - sgn * 40, wrist[1] + 120), (elbow[0] - sgn * 20, elbow[1] + 130), (root[0], root[1] + 90)], 3)
    p.poly(cov, S_WING_L, INK, 2.0)                    # the lighter coverts along the arm
    p.line(lead, dk(S_WING_D, 0.8), 4.0)
    p.line(lead, INK, 2.2)


def wings(img, cam, x, y, s, sp, yaw, j):
    """Both wings, behind him (front and three-quarter) in his own frame; seen from behind, they are drawn after him
    (wings_over)."""
    view_deg, mirror = V.snap(yaw)
    L = B.Local(cam, x, y + j.get('bob', 0.0) * s if j else y, s, -1 if mirror else 1)
    p = B.Pen(img, L)
    spread = sp.get('spread', 0.5)
    view = V.VIEWS[view_deg]
    if view == 'side':
        _wing(p, -1, spread * 0.5, view)
        return
    if view == 'three':
        _wing(p, 1, spread * 0.6, view)
        _wing(p, -1, spread, view)
        return
    for sgn in (-1, 1):
        _wing(p, sgn, spread, view)


# ---------------------------------------------------------------------------------------------- Satan's suit
def satan_torso(img, p, sp, t):
    """Ref 1: black suit, white shirt, dark red tie, a white pocket square, a small gold pin on his left lapel."""
    tie = sp.get('tie', S_TIE)
    p.poly([(-12, 16), (12, 16), (15, 196), (0, 222), (-15, 196)], tie, INK, 2.0)
    p.poly([(-12, -2), (12, -2), (9, 18), (-9, 18)], tie, INK, 2.0)
    p.line([(3, 26), (7, 186)], dk(tie, 0.78), 1.4)
    for sgn in (-1, 1):                                # sharp peaked lapels
        p.poly([(sgn * 44, -2), (sgn * 72, 28), (sgn * 60, 70), (sgn * 84, 84), (sgn * 6, 250), (sgn * 24, 150)],
               S_SUIT, INK, 2.2)
        p.line([(sgn * 66, 72), (sgn * 30, 170)], dk(S_SUIT, 0.6), 1.2)
    p.poly([(-118, 150), (-80, 150), (-84, 166), (-114, 166)], (246, 246, 244), INK, 1.4)      # pocket square
    p.poly([(-112, 150), (-104, 138), (-96, 150)], (246, 246, 244), INK, 1.2)
    p.ell(58, 96, 6, 6, GOLD, INK, 1.2)                # the gold pin (ref 1)
    p.ell(8, 290, 5, 5, (10, 10, 12), None)


# ---------------------------------------------------------------------------------------------- Epstein's head
def epstein_head(img, p, sp, t, hx, hy):
    L = P4.layout(P4.target('epstein', sp.get('average', False)))
    f = P4.Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin = E_SKIN
    mood = sp.get('mood', 'neutral')
    sd = dk(skin, 0.82)
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.5:
            continue
        ex, ey = f(sgn * (L['fw'] * 0.5 + 0.01), 0.42)
        p.poly(oval(ex, ey, 11, 24, 20), skin, INK, 2.4)
        p.line([(ex - sgn * 2, ey - 10), (ex + sgn * 3, ey), (ex - sgn * 1, ey + 10)], dk(skin, 0.7), 1.4)
    out = curve(f.pts(P4.outline_uv(L, 0.40)), 4)
    p.poly(out, skin, INK, 2.6)
    for k in range(3):                                 # forehead lines
        v = 0.07 + 0.045 * k
        p.line(curve(f.pts([(-0.2 + 0.03 * k, v + 0.01), (0.0, v - 0.006), (0.2 - 0.03 * k, v + 0.01)]), 3), sd, 1.4)
    if not sp.get('average'):
        for sgn in (-1, 1):                            # crow's feet, bags, the deep folds nose to mouth
            cx, cy = f(sgn * (L['ecx'] + L['ew'] * 0.62), L['eye_y'])
            for k in (-1, 0, 1):
                p.line([(cx, cy + 4 * k), (cx + sgn * 12, cy + 7 * k - 2)], sd, 1.3)
            bx, by = f(sgn * L['ecx'], L['eye_y'] + L['eh'] * 0.9)
            p.line(curve([(bx - 12, by), (bx, by + 5), (bx + 12, by)], 3), sd, 1.4)
            p.line(curve(f.pts([(sgn * L['nw'] * 0.55, L['nose_y'] - 0.03), (sgn * L['mw'] * 0.58, L['lip0'] + 0.01),
                                (sgn * L['mw'] * 0.62, L['lip17'] + 0.02)]), 3), sd, 2.0)
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', 0.22)), E_IRIS, dk(skin, 0.84), liner=2.4)
    P4.brows(p, f, L, (128, 116, 106), 0.03, sp.get('brow_up', 0.0),
             {'stern': 0.012}.get(mood, 0.0) + sp.get('frown', 0.0))
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, L['lip13'])
    smile = {'neutral': 0.9, 'stern': -0.2}.get(mood, 0.6)
    P4.lips(p, f, L, dict(sp, smile=smile), E_LIP, (fx, my - 6))
    if mood == 'neutral' and not sp.get('mouth', 'rest').startswith('v:'):   # the half-smile: corners tucked in
        for sgn in (-1, 1):
            cx, cy = f(sgn * L['mw'] / 2, L['lip13'] - 0.008)
            p.line([(cx, cy + 1), (cx + sgn * 7, cy - 4)], sd, 1.6)
    # the hair: big, grey, swept back and up from a high hairline, wide past the ears, a wavy outline (refs 1-3)
    fw, fhw = L['fw'], L['fhw']
    hl = 0.035
    hair = [(-fw * 0.5 - 0.02, 0.40), (-fw * 0.5 - 0.075, 0.24), (-fhw * 0.5 - 0.09, 0.02), (-fhw * 0.5 - 0.06, -0.16),
            (-fhw * 0.5 * 0.8, -0.30), (-0.2, -0.38), (-0.05, -0.40), (0.1, -0.41), (0.24, -0.37),
            (fhw * 0.5 * 0.85, -0.29), (fhw * 0.5 + 0.06, -0.15), (fhw * 0.5 + 0.09, 0.03), (fw * 0.5 + 0.075, 0.24),
            (fw * 0.5 + 0.02, 0.40), (fw * 0.5 - 0.01, 0.34), (fhw * 0.5 - 0.005, 0.12), (fhw * 0.5 * 0.88, hl),
            (0.22, hl - 0.02), (0.08, hl - 0.005), (-0.06, hl + 0.005), (-0.2, hl - 0.015), (-fhw * 0.5 * 0.88, hl),
            (-fhw * 0.5 + 0.005, 0.12), (-fw * 0.5 + 0.01, 0.34)]
    hp = curve(f.pts(hair), 4)
    cx0, cy0 = f(0.0, -0.08)
    wavy = []                                          # a gently wavy outline over the top and sides
    for i, q in enumerate(hp):
        if q[1] < f.top + 0.03 * P4.H:
            a = 4.5 * math.sin(i * 0.75) ** 2
            dx, dy = q[0] - cx0, q[1] - cy0
            n = math.hypot(dx, dy) or 1.0
            wavy.append((q[0] + dx / n * a, q[1] + dy / n * a))
        else:
            wavy.append(q)
    p.poly(wavy, E_HAIR, INK, 2.6)
    rng = np.random.default_rng(7)
    for k in range(9):                                 # strands swept back and up, a few darker
        u = -0.26 + k * 0.065
        c = E_HAIR_D if k % 3 else E_HAIR_L
        p.line(curve(f.pts([(u, hl - 0.01), (u * 1.1 + 0.02, -0.15), (u * 1.2 + 0.05, -0.3)]), 3)[:8], c, 1.6)
    for sgn in (-1, 1):                                # waves over the sides
        if sgn < 0 and f.tq > 0.5:
            continue
        p.line(curve(f.pts([(sgn * (fhw * 0.5 + 0.02), 0.05), (sgn * (fw * 0.5 + 0.05), 0.15),
                            (sgn * (fw * 0.5 + 0.03), 0.3)]), 3), E_HAIR_D, 1.6)
    del rng
    return fx


# ---------------------------------------------------------------------------------------------- Epstein's polo
def epstein_torso(img, p, sp, t):
    """Ref 3: a dark short-sleeved polo: a soft collar either side of the neck, a three-button placket."""
    c = sp.get('jacket', E_POLO)
    cd, cl = dk(c, 0.7), blend(c, (255, 255, 255), 0.12)
    p.poly([(-12, 0), (12, 0), (12, 110), (-12, 110)], cl, INK, 1.6)            # the placket
    p.poly([(-12, 0), (12, 0), (0, 30)], sp['skin'], INK, 1.4)                   # the open neck
    for k in range(3):
        p.ell(0, 30 + 30 * k, 4, 4, (210, 210, 214), INK, 1.0)
    for sgn in (-1, 1):                                # the collar's points
        p.poly([(sgn * 12, -2), (sgn * 48, -10), (sgn * 64, 8), (sgn * 36, 44), (sgn * 14, 30)], cl, INK, 2.0)
    p.line([(-90, 230), (-40, 260)], cd, 1.4)          # soft creases
    p.line([(90, 230), (40, 262)], cd, 1.4)


# ---------------------------------------------------------------------------------------------- Trump, measured
# traitors_cast's Trump failed the likeness check (4 Nov: -28%, 6th of 7). Rebuilt from measurements (likeness.py card
# on trump-1 and -2; trump-3 turned 36 degrees, left out), keeping that head's big shapes: the swept blond hair and
# forelock, the tan with pale rings round the eyes, the pout, the jowls and double chin.
P4.MEASURED['trump'] = dict(face_wide=0.868, jaw_wide=0.811, forehead_wide=0.939, eyes_apart=1.375, eye_size=0.177,
                            eye_open=0.213, eye_tilt=1.145, brow_high=0.553, brow_slope=-8.097, nose_long=0.401,
                            nose_wide=0.618, mouth_wide=0.788, lip_top=0.114, lip_low=0.185, philtrum=0.139,
                            chin_long=0.283)    # 4 Nov, second pack: trump-6 (front), -5, -2, -1
DCHIN = True
P4.PUSH['trump'] = 1.8
P4.TUNE['trump'] = dict(eye_open=0.4, eye_size=0.8, forehead_wide=3, eye_tilt=2, lip_top=4, lip_low=4, philtrum=4,  # Sam 4 Nov: eyes a little more open
                        chin_long=5, brow_slope=3, face_wide=2)   # searched 4 Nov: 31% on trump-6, 22% on trump-2


def trump_head(img, p, sp, t, hx, hy):
    L = P4.layout(P4.target('trump', sp.get('average', False)))
    f = P4.Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin = TC.T_SKIN
    sd = dk(skin, 0.86)
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.5:
            continue
        ex, ey = f(sgn * (L['fw'] * 0.5 + 0.01), 0.42)
        p.poly(oval(ex, ey, 12, 25, 20), skin, INK, 2.4)
        p.line([(ex - sgn * 2, ey - 10), (ex + sgn * 3, ey), (ex - sgn * 1, ey + 10)], dk(skin, 0.7), 1.4)
    out = curve(f.pts(P4.outline_uv(L, 0.5)), 4)
    p.poly(out, skin, INK, 2.6)
    if not sp.get('average'):
        for sgn in (-1, 1):                            # the pale rings round the eyes (goggle tan)
            cx, cy = f(sgn * L['ecx'], L['eye_y'])
            p.poly(curve(oval(cx, cy, L['ew'] * P4.H * 0.78, L['ew'] * P4.H * 0.48, 12)), blend(skin, TC.T_RING, 0.6), None)
        for sgn in (-1, 1):                            # jowls from the nose wings past the mouth to the jaw
            p.line(curve(f.pts([(sgn * L['nw'] * 0.55, L['nose_y'] - 0.02), (sgn * L['mw'] * 0.66, L['lip13']),
                                (sgn * L['jw'] * 0.42, 0.9)]), 3), sd, 2.0)
        if DCHIN:
            p.line(curve(f.pts([(-0.12, 1.04), (0.0, 1.06), (0.12, 1.04)]), 3), sd, 1.8)      # the double chin
        for k in range(2):                             # forehead creases
            v = 0.1 + 0.05 * k
            p.line(curve(f.pts([(-0.16, v + 0.01), (0.0, v - 0.004), (0.16, v + 0.01)]), 3), sd, 1.5)
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', 0.05)), (104, 136, 168), blend(TC.T_RING, skin, 0.6), liner=2.4)
    P4.brows(p, f, L, (186, 140, 86), 0.04, sp.get('brow_up', 0.0), sp.get('frown', 0.012))
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, L['lip13'])

    def pout():                                        # lips pushed forward into a small rosebud
        mw = L['mw'] * P4.H * 0.3
        p.poly(curve(oval(fx, my - 2, mw, mw * 0.62, 12)), (196, 116, 98), INK, 1.8)
        p.line([(fx - mw * 0.55, my - 2), (fx, my), (fx + mw * 0.55, my - 2)], INK, 2.0)
    if sp.get('pout'):                                 # the rosebud pout, for a moment that wants it
        TC.talk_or(p, dict(sp, lips=True, lip_c=(196, 116, 98)), t, fx, my - 6, pout)
    else:                                              # measured: thin lips, corners pulled down (ref 2)
        P4.lips(p, f, L, dict(sp, smile=0.0 if sp.get('average') else -0.8), (196, 116, 98), (fx, my - 6))
    # the hair: high and swept from the back of the crown forward and over to our left, the forelock curling down
    fw, fhw = L['fw'], L['fhw']
    hair = [(-fw * 0.5 - 0.01, 0.42), (-fw * 0.5 - 0.09, 0.22), (-fhw * 0.5 - 0.1, -0.02), (-fhw * 0.5 - 0.06, -0.24),
            (-fhw * 0.5 * 0.7, -0.38), (-0.05, -0.43), (0.22, -0.4), (fhw * 0.5 * 0.92, -0.26), (fhw * 0.5 + 0.1, -0.06),
            (fw * 0.5 + 0.08, 0.2), (fw * 0.5 + 0.01, 0.42), (fw * 0.5 - 0.02, 0.3), (fhw * 0.5 - 0.02, 0.08),
            (0.2, 0.02), (-0.05, 0.03), (-0.3, 0.05), (-fhw * 0.5 + 0.02, 0.1), (-fw * 0.5 + 0.02, 0.3)]
    p.poly(curve(f.pts(hair), 4), TC.T_HAIR, INK, 2.6)
    for k in range(7):                                 # strands swept forward and over to our left
        u = 0.32 - 0.09 * k
        c = TC.T_HAIR_D if k % 2 else TC.T_HAIR_L
        p.line(curve(f.pts([(u + 0.04, 0.08), (u - 0.02, -0.22), (u - 0.14, -0.34), (u - 0.26, -0.3)]), 4)[:12], c, 1.6)
    fl = [(0.12, 0.02), (-0.12, -0.08), (-0.3, -0.1), (-fhw * 0.5 - 0.06, -0.04), (-fhw * 0.5 - 0.02, 0.08),
          (-0.32, 0.06), (-0.12, 0.06)]
    p.poly(curve(f.pts(fl), 4), TC.T_HAIR_L, INK, 2.0)  # the forelock
    p.line(curve(f.pts([(0.0, -0.02), (-0.2, -0.06), (-0.36, -0.02)]), 4)[:10], TC.T_HAIR_D, 1.4)
    return fx


# ---------------------------------------------------------------------------------------------- the hooks
TC.HEADS.update(satan=satan_head, epstein=epstein_head, trump=trump_head)
TC.TORSOS.update(satan=satan_torso, epstein=epstein_torso)
_head_view, _arm, _person = V.head_view, V.arm, V.person


def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
    if sp.get('who') == 'satan' and view != 'front':
        return satan_head_view(img, p, sp, t, view, hx, hy)
    if sp.get('who') == 'epstein' and view == 'three':                 # his own face, turned (patriots4's way)
        sp = dict(sp, three=0.7)
    return _head_view(img, p, sp, t, view, hx, hy)


def arm(p, j2, side, sp, shape=None):
    """A short-sleeved top (Epstein's polo): the bare arm, then the sleeve over the top third of the upper arm."""
    if not sp.get('short_sleeve') or V.PROBE:
        return _arm(p, j2, side, sp, shape)
    sh, el = j2['sh' + side], j2['el' + side]
    _arm(p, j2, side, dict(sp, sleeve=sp['skin'], jacket=sp['skin']), shape)
    end = (sh[0] + (el[0] - sh[0]) * 0.55, sh[1] + (el[1] - sh[1]) * 0.55)
    sh = (sh[0] - (el[0] - sh[0]) * 0.2, sh[1] - (el[1] - sh[1]) * 0.2)     # up over the shoulder's round top
    dx, dy = end[0] - sh[0], end[1] - sh[1]
    n = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / n * 36, dx / n * 36
    p.poly([(sh[0] + nx, sh[1] + ny), (end[0] + nx * 0.95, end[1] + ny * 0.95), (end[0] - nx * 0.95, end[1] - ny * 0.95),
            (sh[0] - nx, sh[1] - ny)], sp['jacket'], INK, 2.4)


def person(img, cam, x, y, s, sp, t, yaw, joints=None, head_yaw=None, tilt=None):
    """Satan's wings: behind him from the front and three-quarter, over his back from behind."""
    if sp.get('who') != 'satan' or not sp.get('wings', True):
        return _person(img, cam, x, y, s, sp, t, yaw, joints, head_yaw, tilt)
    view = V.VIEWS[V.snap(yaw)[0]]
    rear = view in ('back', 'three_back')
    if not rear:
        wings(img, cam, x, y, s, sp, yaw, joints or {})
    out = _person(img, cam, x, y, s, sp, t, yaw, joints, head_yaw, tilt)
    if rear:
        wings(img, cam, x, y, s, sp, yaw, joints or {})
    return out


V.head_view, V.arm, V.person = head_view, arm, person


# ---------------------------------------------------------------------------------------------- the people
SATAN = dict(who='satan', name='Satan', skin=S_SKIN, hw=66, hh=98, head_dy=8, hair='slick', hair_c=S_HAIR,
             brow_c=S_HAIR, brow_w=4.0, nose='long', outfit='suit', jacket=S_SUIT, sleeve=S_SUIT, trousers=S_SUIT,
             shirt=(248, 248, 250), tie=S_TIE, shoe=(14, 12, 14), shoulders=156, full=True, pose='custom',
             height=1.88, spread=0.5, seed=61)
EPSTEIN = dict(who='epstein', name='Epstein', skin=E_SKIN, hw=70, hh=92, head_dy=10, hair='wavy_short', hair_c=E_HAIR,
               brow_c=(128, 116, 106), outfit='jumper', jacket=E_POLO, sleeve=E_POLO, short_sleeve=True,
               trousers=(44, 46, 54), shoe=(30, 26, 22), shoulders=152, full=True, pose='custom', height=1.83,
               seed=62)
TRUMP = dict(TC.TRUMP, hair='side', hair_c=TC.T_HAIR, brow_c=(186, 140, 86), sleeve=(32, 40, 70),
             trousers=(32, 40, 70), shoe=(16, 14, 14), height=1.90, seed=63)
CAST = {'satan': SATAN, 'epstein': EPSTEIN, 'trump': TRUMP}


# ---------------------------------------------------------------------------------------------- the sheet
def _tile(img, draw, box, at):
    lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    draw(lay)
    img.alpha_composite(lay.crop(box), at)


def sheet(out):
    """Every view of all three (true heights against each other), the faces large, a 1.75 m person for scale."""
    import landmarks
    import sizes
    B.SS = 1
    W, H = 1900, 2800
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(FONT, 40)
    small = ImageFont.truetype(FONT, 26)
    cam = B.Cam(1.0, 540, 960)
    d.text((40, 24), 'MIDTERMINAL: the cast (front, side, back)', font=big, fill=(30, 30, 30))
    names = ('front', 'side', 'back')
    for r, key in enumerate(('satan', 'epstein', 'trump')):
        sp = CAST[key]
        k = sp['height'] / 1.75
        s = 0.5 * k
        y0 = 120 + r * 900
        d.text((40, y0 - 4), f"{sp['name']} ({sp['height']:.2f} m)", font=big, fill=(30, 30, 30))
        for i, yaw in enumerate((0, 90, 180)):
            _tile(img, lambda im, yaw=yaw, sp=sp, s=s: V.person(im, cam, 540, 840 - 928 * s, s, dict(sp), 0.0, yaw),
                  (190, 60, 890, 880), (20 + 440 * i, y0 + 40))
            d.text((370 + 440 * i, y0 + 860), names[i], font=small, fill=(40, 40, 40), anchor='mm')
    lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    s = 0.5
    landmarks.draw(ld, 540, 840 - 928 * s, s, 1000)
    sizes.scale_ref(ld, 640, 840, s / V.M_PER_UNIT)
    img.alpha_composite(lay.crop((390, 60, 890, 880)), (1360, 160))
    d.text((1610, 980), '1.75 m person', font=small, fill=(40, 40, 40), anchor='mm')
    img.convert('RGB').save(out, quality=88)
    return out


def faces_sheet(out):
    """The faces large: Satan (rest, smirk, fury, talking), Epstein (rest, stern, talking), Trump (rest, talking)."""
    B.SS = 1
    rows = [('satan', [('neutral', 'rest', 'rest'), ('smirk', 'rest', 'smirk'), ('fury', 'rest', 'fury'),
                       ('neutral', 'v:AI', 'talking')]),
            ('epstein', [('neutral', 'rest', 'rest (half-smile)'), ('stern', 'rest', 'stern'),
                         ('neutral', 'v:AI', 'talking')]),
            ('trump', [('neutral', 'rest', 'rest'), ('neutral', 'v:AI', 'talking')])]
    W, H = 2000, 3 * 660 + 40
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    small = ImageFont.truetype(FONT, 26)
    cam = B.Cam(1.0, 540, 960)
    for r, (key, faces) in enumerate(rows):
        for i, (mood, mouth, label) in enumerate(faces):
            sp = dict(CAST[key], mood=mood, mouth=mouth, wings=False)
            _tile(img, lambda im, sp=sp: V.person(im, cam, 540, 900, 1.3, sp, 0.0, 0), (310, 470, 770, 1080),
                  (20 + 490 * i, 20 + r * 660))
            d.text((250 + 490 * i, 650 + r * 660), f"{CAST[key]['name']}: {label}", font=small, fill=(40, 40, 40),
                   anchor='mm')
    img.convert('RGB').save(out, quality=88)
    return out


def head_png(who, out, average=False):
    """One head and shoulders, straight on, on white (for likeness.py check)."""
    B.SS = 1
    im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    V.person(im, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(CAST[who], average=average, wings=False), 0.0, 0)
    im.crop((240, 380, 840, 1200)).convert('RGB').save(out)
    return out


def LINE_SUBJECTS():
    return [(k, lambda im, sp=sp: V.person(im, B.Cam(1.0, 540, 960), 540, 420, 1.0, dict(sp), 0.0, 0))
            for k, sp in CAST.items()]


cast_sheet = sheet

if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    elif sys.argv[1] == 'faces':
        print(faces_sheet(sys.argv[2]))
    elif sys.argv[1] == 'head':
        print(head_png(sys.argv[2], sys.argv[3], '--average' in sys.argv))
