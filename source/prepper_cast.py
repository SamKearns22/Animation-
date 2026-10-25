#!/usr/bin/env python3
"""Prepper Minister: the people and what they hold (notes/prepper-minister.md; refs in references/prepper-minister/).

Everyone is built on the satire package (views.person: any angle, posed on the hidden skeleton; circle hands).
- Andy Burnham: the Hope Again Andy (burnham.BURNHAM: long face, dark rectangular glasses, grey-flecked side-parted
  hair; ref andy-white-top), in Sam's outfit (24 Oct): white shirt, top button undone, sleeves rolled, navy chinos, a
  tan belt with the Glock tucked behind it at the back, brown shoes. His fear in six strengths (FEAR, 1 = calm,
  6 = hysterical): brows, eyes widening, the grin going to a rictus, rings and stress lines, pallor, small flat sweat
  beads (never cartoon drops).
- Wes Streeting (refs wes-1..5; likeness: a round face with full cheeks, a high forehead, short dark hair with a side
  parting and faded sides, small eyes, a stocky build; no glasses): the full dark navy suit, white shirt, burgundy
  tie, ripped and torn as though he has just escaped danger (Sam: torn and dirty, no blood).
- What they hold, at real size (sizes.SIZES), laid through the hands that hold it (so it is always really held):
  the pistol crossbow (ref crossbow, the DEMON lettering dropped), the Glock 17 (ref pistols, bottom), the oiled
  machete (ref machete), the minigun with its ammo belt (refs minigun-1, -2; the belt round Wes's forehead like a
  bandana, its loose end to the gun), a tin of beans.

    python3 source/prepper_cast.py test OUT.jpg       everyone and everything held, on one quick sheet (working picture)
"""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import mossad                    # noqa: E402,F401  (brows, mouths, hair; patched into burnham on import)
import mouths                    # noqa: E402
import views as V                # noqa: E402
import figure as F               # noqa: E402
import limbs                     # noqa: E402
from ed import INK, curve        # noqa: E402
from satire_style import install_circle_hands   # noqa: E402

mouths.install(B)
install_circle_hands(B)
F.guard(B)
limbs.install(B)

M = V.M_PER_UNIT                       # metres per person unit
WHITE = (246, 246, 242)
WHITE_D = (214, 214, 210)
CHINOS = (44, 54, 84)
TAN, TAN_D = (176, 120, 66), (138, 88, 44)
SUIT, SUIT_D = (34, 42, 66), (24, 30, 48)
TIE = (128, 26, 40)
GUN, GUN_D, GUN_L = (44, 46, 52), (26, 28, 32), (84, 88, 96)
BRASS, BRASS_D = (214, 170, 76), (166, 124, 44)
SWEAT = (214, 234, 244)

# ------------------------------------------------------------------------------------------------ the people
ANDY = dict(B.BURNHAM, name='Andy', outfit='jumper', jacket=WHITE, sleeve=WHITE, trousers=CHINOS, bottom=468,
            shoulders=150, creases=1, rolled=True, shirt_open=True, belt=TAN, seed=71)
WES = dict(name='Wes', skin=B.PINK, hw=76, hh=86, jaw='round', hair='crop', hair_c=(52, 40, 32), brow_c=(46, 34, 28),
           brow_w=4.0, outfit='suit', jacket=SUIT, sleeve=SUIT, trousers=SUIT, tie=TIE, shirt=(236, 238, 244),
           shoulders=160, torn=True, fade=True, cheeks=True, seed=72)
HEIGHTS = {'Andy': 1.75, 'Wes': 1.78}
PEOPLE = {'Andy': ANDY, 'Wes': WES}

# Andy's fear, 1 (calm) to 6 (hysterical). Sam picks the numbers per shot; the plan is in the notes file.
FEAR = [
    dict(name='1 Calm', brows=None, mouth='smile', harrow=0.0, lid=0, pale=0.0, sweat=0, lines=0),
    dict(name='2 Breezy', brows='sincere', mouth='smile', harrow=0.1, lid=0, pale=0.0, sweat=0, lines=0),
    dict(name='3 Rictus', brows='sincere', mouth='grin', harrow=0.45, lid=-1, pale=0.08, sweat=1, lines=2),
    dict(name='4 Rigid', brows='alarm', mouth='set', harrow=0.6, lid=-1.5, pale=0.15, sweat=3, lines=2),
    dict(name='5 Pained', brows='alarm', mouth='set', harrow=0.8, lid=-2, pale=0.25, sweat=6, lines=3),
    dict(name='6 Terror', brows='wow', mouth='open', harrow=1.0, lid=-3, pale=0.4, sweat=8, lines=3),
]


def fear(sp, level, talking=False):
    """Andy at fear level 1-6 (fractions blend the numbers): brows, lids, mouth (unless he is talking: the lip sync
    keeps it), rings, pallor and sweat."""
    lv = FEAR[max(0, min(5, int(round(level)) - 1))]
    sp = dict(sp)
    sp['brows'] = lv['brows']
    sp['lid'] = lv['lid']
    sp['harrow'] = lv['harrow']
    if not talking:
        sp['mouth'] = lv['mouth']
    k = lv['pale']
    sp['skin'] = tuple(int(c + (g - c) * k) for c, g in zip(sp['skin'], (236, 232, 222)))
    sp['sweat'] = lv['sweat']
    sp['stress_lines'] = lv['lines']
    return sp


# ------------------------------------------------------------------------------------------------ clothes
def _box(view, sp, y=150.0):
    sw = sp.get('shoulders', 150)
    l, r = {'front': (-sw, sw), 'three': (-sw * 0.95, sw * 0.82), 'side': (-0.6 * sw, 0.66 * sw),
            'three_back': (-sw * 0.9, sw * 0.9), 'back': (-sw, sw)}[view]
    return l, r


def andy_shirt(p, view, sp):
    """The white shirt (Sam, 24 Oct): the top button undone (a V of skin under a pointed collar), a button placket,
    tucked into navy chinos with a tan belt; from behind, the Glock's grip above the belt in the small of his back
    (until he whips it out)."""
    bottom = sp.get('bottom', 468)
    skin = sp['skin']
    belt = sp.get('belt', TAN)
    l, r = _box(view, sp, bottom)
    if view == 'front':
        # Sam, 25 Oct: the V's top edge was inked across his neck like a necklace: only its two sides are inked
        p.poly([(-30, -4), (30, -4), (0, 58)], skin, None)
        p.line([(-30, -4), (0, 58), (30, -4)], INK, 2.0)
        for sg in (-1, 1):
            p.poly([(sg * 6, 56), (sg * 34, -8), (sg * 54, -4), (sg * 40, 30)], WHITE, INK, 2.0)       # collar points
        p.line([(0, 58), (0, bottom - 30)], WHITE_D, 2.0)
        for k in range(4):
            p.ell(5, 110 + 85 * k, 4, 4, WHITE_D, INK, 1.0)
        for sg in (-1, 1):                                    # a soft fold or two where it tucks in
            p.line([(sg * 60, bottom - 60), (sg * 46, bottom - 26)], WHITE_D, 1.8)
    elif view == 'three':
        o = 0.32 * sp.get('shoulders', 150)
        p.poly([(o - 26, -4), (o + 22, -4), (o - 2, 50)], skin, None)
        p.line([(o - 26, -4), (o - 2, 50), (o + 22, -4)], INK, 2.0)
        p.poly([(o - 4, 48), (o - 28, -8), (o - 46, -4), (o - 34, 26)], WHITE, INK, 2.0)
        p.poly([(o + 2, 48), (o + 20, -8), (o + 34, -4), (o + 26, 24)], WHITE, INK, 2.0)
        p.line([(o - 2, 50), (o + 2, bottom - 30)], WHITE_D, 2.0)
        for k in range(4):
            p.ell(o + 4, 110 + 85 * k, 4, 4, WHITE_D, INK, 1.0)
    elif view == 'side':
        p.poly([(10, -8), (40, -2), (34, 30)], WHITE, INK, 2.0)
    else:
        p.poly([(-40, -12), (40, -12), (44, 8), (-44, 8)], WHITE, INK, 2.0)
        p.line([(0, 20), (0, bottom - 20)], WHITE_D, 1.6)
    # the belt round the waist, the buckle in front
    yb = bottom - 16
    p.poly([(l * 0.88, yb), (r * 0.88, yb), (r * 0.88, bottom + 4), (l * 0.88, bottom + 4)], belt, INK, 2.0)
    if view in ('front', 'three'):
        bx = 0 if view == 'front' else 0.32 * sp.get('shoulders', 150)
        p.poly([(bx - 14, yb - 3), (bx + 14, yb - 3), (bx + 14, bottom + 7), (bx - 14, bottom + 7)], (210, 196, 150), INK, 1.8)
    if view in ('back', 'three_back') and sp.get('glock_tucked', False):
        bx = 0 if view == 'back' else -0.15 * sp.get('shoulders', 150)
        p.poly([(bx - 16, yb - 66), (bx + 18, yb - 70), (bx + 22, yb + 8), (bx - 14, yb + 8)], GUN, INK, 2.0)
        for k in range(4):
            p.line([(bx - 8, yb - 56 + 12 * k), (bx + 12, yb - 58 + 12 * k)], GUN_D, 1.4)


def wes_rips(p, view, sp):
    """Wes's suit after a narrow escape (Sam: torn and dirty, no blood): jagged rips through the jacket with the
    white shirt showing, a lapel torn half off, a ripped pocket flap, smears of dust and grime."""
    rng = np.random.default_rng(sp.get('seed', 72))
    shirt = sp.get('shirt', (236, 238, 244))
    dirt = (112, 100, 86)
    def rip(cx, cy, w, h, seed, ang=0.5):
        """A slash through the cloth: a long, jagged gap showing the shirt, a flap of jacket hanging off its edge."""
        r = np.random.default_rng(seed)
        ca, sa = math.cos(ang), math.sin(ang)
        R = lambda u, v: (cx + u * ca - v * sa, cy + u * sa + v * ca)
        top = [R(u, -h * r.uniform(0.3, 1.0) * (1 - abs(u) / w) ** 0.5) for u in np.linspace(-w, w, 7)]
        bot = [R(u, h * r.uniform(0.2, 0.7) * (1 - abs(u) / w) ** 0.5) for u in np.linspace(w, -w, 7)]
        p.poly(top + bot, shirt, INK, 1.8)
        flap = [R(-w * 0.2, h * 0.3), R(w * 0.5, h * 0.4), R(w * 0.25, h * 1.9)]
        p.poly(flap, SUIT, INK, 1.6)
        for k in range(3):                                   # loose threads at its ends
            a0 = R(w * (1 if k % 2 else -1), 0)
            p.line([a0, (a0[0] + 7 * math.cos(ang + k), a0[1] + 7 * math.sin(ang + k))], (230, 230, 230), 1.2)
    def smear(cx, cy, w, h, seed):
        r = np.random.default_rng(seed)
        pts = [(cx + w * r.uniform(0.6, 1.0) * math.cos(a), cy + h * r.uniform(0.6, 1.0) * math.sin(a))
               for a in np.linspace(0, 2 * math.pi, 9, endpoint=False)]
        p.poly(pts, (66, 64, 70), None)
    if view == 'front':
        rip(-84, 170, 60, 15, 1, 1.1)
        rip(92, 340, 55, 13, 2, -0.4)
        p.poly([(44, -2), (86, 40), (78, 70), (60, 150), (30, 112)], SUIT, INK, 2.0)          # the torn lapel hanging
        p.line([(46, 116), (62, 150)], INK, 1.4)
        smear(-40, 380, 30, 16, 3)
        smear(70, 70, 22, 12, 4)
    elif view == 'three':
        rip(-60, 170, 40, 11, 1, 1.1)
        rip(70, 330, 38, 10, 2, -0.4)
        smear(-10, 380, 28, 14, 3)
    elif view == 'side':
        rip(20, 210, 40, 10, 5, 1.2)
        smear(-30, 330, 24, 14, 6)
    else:
        rip(-70, 150, 50, 12, 7, 0.9)
        rip(60, 300, 40, 10, 8, -0.3)
        smear(10, 220, 34, 18, 9)


def wes_head(p, view, sp, hx, hy):
    """His likeness (refs wes-1..5): a side parting high on the left, the sides faded short (a paler band over the
    ears), full cheeks."""
    hw, hh = sp.get('hw', 76), sp.get('hh', 86)
    if view in ('front', 'three'):
        fx = hx + (12 if view == 'three' else 0)
        hc = B.dk(sp.get('hair_c', (52, 40, 32)), 0.6)
        p.line([(fx + hw * 0.3, hy - hh * 0.98), (fx + hw * 0.42, hy - hh * 0.72)], hc, 2.4)     # the side parting
        for k in range(3):                                    # combed over from it
            p.line([(fx + hw * 0.22 - 18 * k, hy - hh * 0.95), (fx - 10 - 22 * k, hy - hh * 0.76)], hc, 1.6)
        for sg in (-1, 1):                                    # full cheeks
            p.line([(fx + sg * (hw - 22), hy + 22), (fx + sg * (hw - 14), hy + 42)], B.dk(sp['skin'], 0.86), 1.6)


def sweat(p, view, sp, hx, hy):
    """Andy's sweat (brief: small flat beads, not cartoony): a few small round beads on the forehead and temples,
    each with a pale highlight; more at higher fear."""
    n = sp.get('sweat', 0)
    if not n or view in ('back', 'three_back'):
        return
    hw, hh = sp.get('hw', 68), sp.get('hh', 96)
    spots = [(-0.55, -0.62), (0.5, -0.66), (0.86, -0.25), (-0.88, -0.2), (0.1, -0.74), (-0.3, -0.7), (0.78, 0.1),
             (-0.8, 0.12)]
    for (u, v) in spots[:n]:
        if view == 'side' and u < 0:
            continue
        x, y = hx + u * hw * (0.6 if view == 'side' else 1.0), hy + v * hh
        p.ell(x, y, 4.2, 5.2, SWEAT, INK, 1.2)
        p.ell(x - 1.2, y - 1.6, 1.3, 1.3, (255, 255, 255), None)
    if sp.get('stress_lines') and view in ('front', 'three'):
        for sgn in (-1, 1):                                   # stress lines under the eyes
            ex = hx - 4 + sgn * 30
            for k in range(sp['stress_lines']):
                p.line([(ex - 14, hy + 14 + 6 * k), (ex, hy + 18 + 6 * k), (ex + 12, hy + 14 + 6 * k)], B.dk(sp['skin'], 0.74), 1.4)


def bandana(p, view, sp, hx, hy):
    """The minigun's ammo belt worn round Wes's forehead like a bandana (Sam, 24 Oct): brass rounds in black links,
    tied off at the side."""
    if not sp.get('bandana'):
        return
    hw, hh = sp.get('hw', 76), sp.get('hh', 86)
    y = hy - hh * 0.62
    if view == 'front':
        xs = np.linspace(-hw - 2, hw + 2, 11)
        p.poly([(xs[0], y - 10), (xs[-1], y - 10), (xs[-1], y + 12), (xs[0], y + 12)], (40, 40, 44), INK, 1.8)
        for x in xs[1:-1]:
            p.poly([(x - 5, y - 16), (x + 5, y - 16), (x + 5, y + 6), (x - 5, y + 6)], BRASS, INK, 1.2)
            p.ell(x, y - 18, 4, 3, BRASS_D, INK, 1.0)
    elif view in ('three', 'side'):
        x0, x1 = (hx - hw * 0.8, hx + hw + 4) if view == 'three' else (hx - hw * 0.7, hx + hw * 0.9)
        xs = np.linspace(x0, x1, 8)
        p.poly([(x0, y - 8), (x1, y - 12), (x1, y + 10), (x0, y + 12)], (40, 40, 44), INK, 1.8)
        for x in xs[1:-1]:
            p.poly([(x - 5, y - 16), (x + 5, y - 16), (x + 5, y + 6), (x - 5, y + 6)], BRASS, INK, 1.2)
    else:
        p.poly([(hx - hw - 2, y - 8), (hx + hw + 2, y - 8), (hx + hw + 2, y + 10), (hx - hw - 2, y + 10)], (40, 40, 44), INK, 1.8)
        p.poly([(hx - 10, y), (hx + 10, y), (hx + 22, y + 60), (hx + 4, y + 64)], (40, 40, 44), INK, 1.6)   # the knot's tail


def dress(sp):
    body, head = [], []
    if sp.get('shirt_open'):
        body.append(andy_shirt)
    if sp.get('torn'):
        body.append(wes_rips)
    if sp.get('fade'):
        head.append(wes_head)
    head.append(sweat)
    head.append(bandana)
    return body, head


# rolled sleeves (Andy) and a torn sleeve (Wes): drawn over each arm as it is drawn
_ARM = V.arm


def _arm(p, j2, side, sp, shape=None):
    sh, el, wr = j2['sh' + side], j2['el' + side], j2['wr' + side]
    if sp.get('rolled'):
        # Sam's note 26 (25 Oct): the wrists looked sunk in the sleeves (the sleeve ran on under a narrow strip of skin
        # to the wrist). Now the bare forearm is its own limb from the elbow, the sleeve stops at the elbow, and a fat
        # rolled cuff sits over the join; the hand comes out of the skin, never out of cloth, even foreshortened.
        with F.allow('a skeleton arm, checked in 3D (check_arm3); on screen it may be foreshortened'):
            B.arm(p, sh, el, wr, sp['skin'], w=24)
            # Sam's note 38 (25 Oct): the cuff looked detached (the sleeve tapered to about 19 at the elbow, under a
            # 27-wide cuff over a 22-wide forearm). A wider sleeve ends about 24 wide, so the cuff sits flush on it
            mid = ((sh[0] + el[0]) / 2, (sh[1] + el[1]) / 2)
            B.arm(p, sh, mid, el, sp.get('sleeve', WHITE), w=34)
        fx, fy = wr[0] - el[0], wr[1] - el[1]
        fl = math.hypot(fx, fy)
        if fl < 18:                                          # pointing at us: the band lies across the upper arm's line
            fx, fy = el[0] - sh[0], el[1] - sh[1]
            fl = math.hypot(fx, fy) or 1.0
        dx, dy = fx / fl, fy / fl
        nx, ny = -dy, dx
        c0 = (el[0] - dx * 4, el[1] - dy * 4)
        c1 = (el[0] + dx * 16, el[1] + dy * 16)
        hw0, hw1 = 27.0, 26.0
        band = [(c0[0] + nx * hw0, c0[1] + ny * hw0), (c1[0] + nx * hw1, c1[1] + ny * hw1),
                (c1[0] + dx * 3, c1[1] + dy * 3), (c1[0] - nx * hw1, c1[1] - ny * hw1),
                (c0[0] - nx * hw0, c0[1] - ny * hw0), (c0[0] - dx * 2, c0[1] - dy * 2)]
        p.poly(band, WHITE, INK, 2.2)
        m = (el[0] + dx * 6, el[1] + dy * 6)                 # the roll's fold
        p.line([(m[0] + nx * 22, m[1] + ny * 22), (m[0] - nx * 22, m[1] - ny * 22)], WHITE_D, 1.6)
        shape = shape or j2.get('hand', {}).get(side, 'fist')
        if shape != 'none':
            B.gesture_hand(p, el, wr, shape, sp['skin'])
    else:
        _ARM(p, j2, side, sp, shape)
    if sp.get('torn') and side == 'L':                       # his left sleeve torn at the elbow
        m = (el[0] + (sh[0] - el[0]) * 0.15, el[1] + (sh[1] - el[1]) * 0.15)
        pts = [(m[0] + 16 * math.cos(a) * (0.6 if k % 2 else 1.0), m[1] + 10 * math.sin(a) * (0.6 if k % 2 else 1.0))
               for k, a in enumerate(np.linspace(0, 2 * math.pi, 10, endpoint=False))]
        p.poly(pts, sp.get('shirt', WHITE), INK, 1.6)


V.arm = _arm


def outfit(j, sp):
    body, head = dress(sp)
    j['body_props'] = body + j.get('body_props', [])
    j['head_props'] = head + j.get('head_props', [])
    return j


def person(img, cam, x, y, s, sp, t=0.0, yaw=0, j=None, head_yaw=None):
    j = j or V.standing(sp)
    if not j.get('_dressed'):
        outfit(j, sp)
        j['_dressed'] = True
    return V.person(img, cam, x, y, s, dict(sp, full=True, pose='custom'), t, yaw, j, head_yaw)


# ------------------------------------------------------------------------------------------------ held things
def _frame(j2, a, b, u_a, u_b, full, min_k=0.55):
    """A long thing held by two hands: hand `a` at u_a along it, hand `b` at u_b (0 = its back end, 1 = its front).
    Returns P(u, v) in person units (v up, away from the floor), its screen length and how end-on it is (0..1)."""
    (ax, ay), (bx, by) = j2[a], j2[b]
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy) or 1.0
    ux, uy = dx / n, dy / n
    L = max(n / max(1e-6, u_b - u_a), min_k * full)
    sx, sy = -uy, ux
    if sy > 0:
        sx, sy = -sx, -sy
    end_on = max(0.0, min(1.0, 1.0 - L / full))
    def P(u, v):
        return (ax + ux * (u - u_a) * L + sx * v, ay + uy * (u - u_a) * L + sy * v)
    return P, L, end_on, (ux, uy), (sx, sy)


def _fists(p, j2, skin, sides=('R', 'L')):
    """The holding hands drawn over a long gun (the sleeves stay under it): a fist at each wrist."""
    for sd in sides:
        B.gesture_hand(p, j2['el' + sd], j2['wr' + sd], 'fist', skin)


def _screen_dir(j2, aim3, k=100.0):
    """A direction in the body's own 3D frame (x across, y down, z forward) as drawn in this view: the unit screen
    direction and how much of it survives (1 side on, 0 straight at us)."""
    (x0, y0), _ = V.project((0.0, 0.0, 0.0), j2['yaw'])
    (x1, y1), _ = V.project(tuple(c * k for c in aim3), j2['yaw'])
    dx, dy = x1 - x0, y1 - y0
    n = math.hypot(dx, dy)
    return ((dx / n, dy / n) if n > 1e-6 else (0.0, -1.0)), min(1.0, n / k)


def _one_hand(j2, side):
    (ex, ey), (wx, wy) = j2['el' + side], j2['wr' + side]
    dx, dy = wx - ex, wy - ey
    n = math.hypot(dx, dy) or 1.0
    return (wx + dx / n * 14, wy + dy / n * 14), (dx / n, dy / n), n


CROSSBOW = 0.72 / M                    # its length (stock folded out), person units
CB_GRIP, CB_FORE = 0.36, 0.62


def crossbow(loaded=True, skin=None, aim3=(0.0, 0.0, 1.0), min_k=0.55):
    """The pistol crossbow (ref crossbow): grey-black skeletal stock folded out, a pistol grip with its trigger, the
    long rail with a red-dot sight on top, short recurved limbs at the front with the string drawn back to the latch,
    a bolt on the rail with bright vanes. Right hand on the grip, left under the front. The limbs spread wide when it
    points at us, and close to a stub side on."""
    def draw(p, j2):
        P, L, eo, u, s = _frame(j2, 'wrR', 'wrL', CB_GRIP, CB_FORE, CROSSBOW, min_k)
        g = 1.0
        p.poly([P(0.0, -26), P(0.0, 18), P(0.05, 22), P(0.2, 10), P(0.2, -4), P(0.06, -18)], GUN_D, INK, 2.0)    # stock
        p.poly([P(0.04, -10), P(0.04, 8), P(0.17, 4), P(0.17, -2)], (236, 232, 222), None)                       # its gap
        p.poly([P(0.2, -10), P(0.2, 14), P(0.92, 10), P(0.92, -6)], GUN, INK, 2.2)                              # rail
        for k in range(5):
            p.line([P(0.45 + 0.08 * k, 2), P(0.48 + 0.08 * k, 2)], GUN_L, 2.0)
        p.poly([P(0.33, -8), P(0.39, -8), P(0.36, -58), P(0.29, -56)], GUN_D, INK, 1.8)                          # grip
        p.line([P(0.4, -10), P(0.42, -26), P(0.37, -30)], INK, 2.0)                                                # trigger guard
        p.poly([P(0.46, 14), P(0.46, 34), P(0.58, 34), P(0.58, 14)], GUN_D, INK, 1.8)                            # red-dot sight
        p.ell(*P(0.58, 24), 3, 3, (220, 40, 40), None)
        if loaded:
            p.line([P(0.55, 14), P(1.02, 14)], (30, 30, 30), 3.0)                                                 # the bolt
            p.poly([P(0.55, 14), P(0.62, 14), P(0.6, 24), P(0.55, 24)], (120, 220, 60), INK, 1.0)
        across = (aim3[2], 0.0, -aim3[0])                     # the limbs lie level, across the shooter
        ld, keep = _screen_dir(j2, across)
        span = 0.3 / M * max(keep, 0.12)
        tip = P(0.9, 0)
        for sg in (-1, 1):
            a = (tip[0] + ld[0] * sg * span - u[0] * 30, tip[1] + ld[1] * sg * span - u[1] * 30)
            mid = (tip[0] + ld[0] * sg * span * 0.55 - u[0] * 8, tip[1] + ld[1] * sg * span * 0.55 - u[1] * 8)
            p.line([tip, mid, a], GUN_D, 7.0)
            p.line([a, P(0.58 if loaded else 0.88, 4)], (230, 230, 226), 1.6)                                    # string
        p.ell(*tip, 9, 9, GUN, INK, 1.6)
        if skin:
            _fists(p, j2, skin)
    draw.held = skin is None
    draw.own_fists = skin is not None          # it draws the fists: seen from behind, hidden by his back (Sam, 25 Oct:
    draw.along = ('wrR', 'wrL', CROSSBOW, CB_GRIP)   # a fist and the crossbow showed over Andy's back as he aimed)
    return draw


GLOCK_L = 0.186 / M


def glock(side='R', flash=0.0, aim3=None, rec=None):
    """The Glock 17 (ref pistols, bottom): a black slide and frame, the angled textured grip in the fist, the trigger
    guard; seen end on (pointing at us) a square slide face with the muzzle. `flash` > 0: a hard muzzle flash."""
    def draw(p, j2):
        c, d, n = _one_hand(j2, side)
        keep = n / F.FORE
        if aim3 is not None:
            d, keep = _screen_dir(j2, aim3)
        nx, ny = -d[1], d[0]
        if ny > 0:
            nx, ny = -nx, -ny                                 # "up" on the gun: away from the floor
        def P(u, v):
            return (c[0] + d[0] * u * max(keep, 0.35) + nx * v, c[1] + d[1] * u * max(keep, 0.35) + ny * v)
        end_on = keep < 0.4
        if end_on:
            p.poly([P(-6, 30), P(6, 30), P(6, 52), P(-6, 52)], GUN, INK, 2.0)
            p.poly([(c[0] - 16, c[1] - 30), (c[0] + 16, c[1] - 30), (c[0] + 16, c[1] - 8), (c[0] - 16, c[1] - 8)], GUN, INK, 2.0)
            p.ell(c[0], c[1] - 20, 5, 5, (10, 10, 12), None)
            mz = (c[0], c[1] - 20)
        else:
            L = GLOCK_L
            p.poly([P(-30, 14), P(L - 30, 14), P(L - 30, 44), P(-30, 44)], GUN, INK, 2.0)                       # slide
            for k in range(5):
                p.line([P(-24 + 5 * k, 18), P(-24 + 5 * k, 40)], GUN_D, 1.4)
            p.poly([P(-26, 14), P(L - 40, 14), P(L - 40, 2), P(-10, 0)], GUN_D, INK, 1.8)                     # frame
            p.poly([P(-30, 10), P(4, 10), P(-6, -50), P(-36, -46)], GUN_D, INK, 1.8)                          # grip
            p.line([P(8, 4), P(20, -14), P(36, -14), P(40, 4)], INK, 2.0)                                     # guard
            mz = P(L - 26, 30)
        if rec is not None:                                   # where the muzzle is drawn (for the film's tracers)
            rec['muzzle'] = tuple(v / B.SS for v in p.cam.P(*mz))
        if flash > 0:
            muzzle_flash(p, mz, d if not end_on else (0, -1), 50 * flash, end_on)
    draw.held = True
    return draw


def muzzle_flash(p, at, d, size, end_on=False, seed=0):
    """A muzzle flash in the flat house style: a lumpy, uneven burst (never a star: Sam, 24 Oct, 'too cartoony'),
    white core in yellow and orange, for a frame or two (no glow)."""
    rng = np.random.default_rng(seed)
    if end_on:
        rad = rng.uniform(0.74, 1.0, 11)
        pts = [(at[0] + size * rad[k] * math.cos(a), at[1] + size * rad[k] * math.sin(a))
               for k, a in enumerate(np.linspace(0, 2 * math.pi, 11, endpoint=False) + rng.uniform(0, 0.5))]
    else:
        nx, ny = -d[1], d[0]
        pts = []
        for k, a in enumerate(np.linspace(-1.2, 1.2, 9)):
            r = size * rng.uniform(0.7, 1.0) * (1.25 if abs(a) < 0.2 else 1.0)
            pts.append((at[0] + (d[0] * math.cos(a) + nx * math.sin(a)) * r, at[1] + (d[1] * math.cos(a) + ny * math.sin(a)) * r))
        pts = [at] + pts
    p.poly(pts, (255, 170, 40), INK, 1.6)
    cx = sum(q[0] for q in pts) / len(pts)
    cy = sum(q[1] for q in pts) / len(pts)
    p.poly([(cx + (x - cx) * 0.6, cy + (y - cy) * 0.6) for x, y in pts], (255, 236, 120), None)
    p.poly([(cx + (x - cx) * 0.3, cy + (y - cy) * 0.3) for x, y in pts], (255, 255, 240), None)


MACHETE = 0.6 / M


def machete(side='R', aim3=None):
    """The oiled machete (ref machete): a long steel blade hooked at the tip, smeared dark with oil and a hard
    highlight, a black handle with brass rivets in the fist. `aim3`: where the blade points in the body's own 3D frame
    (x across, y down, z forward), so it turns with him and shortens when it points at us or away (Sam's note 45,
    25 Oct: it was a fixed angle on the screen, so when Wes turned it lay across his back). None: along the forearm."""
    def draw(p, j2):
        c, d, n = _one_hand(j2, side)
        keep = 1.0
        if aim3 is not None:
            d, keep = _screen_dir(j2, aim3)
        keep = max(keep, 0.3)
        nx, ny = -d[1], d[0]
        if ny > 0:
            nx, ny = -nx, -ny
        def P(u, v):
            return (c[0] + d[0] * u * keep + nx * v, c[1] + d[1] * u * keep + ny * v)
        L = MACHETE
        p.poly([P(-50, -14), P(30, -16), P(30, 16), P(-50, 14), P(-58, 0)], (24, 22, 24), INK, 2.0)       # handle
        for u in (-34, 0):
            p.ell(*P(u, 0), 4, 4, BRASS, INK, 1.0)
        blade = [P(30, -16), P(L * 0.75, -20), P(L * 0.95, -18), P(L + 6, -4), P(L - 6, 26), P(L * 0.8, 20), P(30, 18)]
        p.poly(blade, (176, 182, 188), INK, 2.2)
        p.poly([P(60, 6), P(L * 0.7, 2), P(L * 0.72, 10), P(60, 12)], (226, 232, 236), None)               # highlight
        for k, (u0, u1) in enumerate(((80, 200), (180, 300), (260, 360))):                                    # the oil
            p.poly([P(u0, -12 + 6 * k), P(u1, -14 + 5 * k), P(u1 - 20, -4 + 5 * k), P(u0 + 10, -2 + 6 * k)], (60, 66, 52), None)
    draw.held = True
    return draw


MINIGUN = 0.9 / M
MG_GRIP, MG_FORE = 0.04, 0.32


def minigun(spin=0.0, flash=0.0, belt_to=None, seed=0, skin=None, rec=None):
    """The minigun (refs minigun-1, -2): six barrels round a spindle with a clamp ring and a muzzle ring, the motor
    housing, a carry handle on top, spade grips at the back; the ammo belt runs from its feed (under the left side) up
    to Wes's forehead (`belt_to`: the point in his units, or None for a loop hanging down). `spin` turns the barrels
    (they blur into each other when firing); `flash` a muzzle flash at the front."""
    def draw(p, j2):
        if j2['yaw'] == 180:                                  # from behind: the gun and belt are in front of him
            return
        P, L, eo, u, s = _frame(j2, 'wrR', 'wrL', MG_GRIP, MG_FORE, MINIGUN, min_k=0.5)
        # the belt first (behind the gun): brass rounds in black links, in a sagging curve (hidden by his back when
        # we see him from behind)
        feed = P(0.36, -26)
        end = belt_to if belt_to is not None else (feed[0] + 40, feed[1] + 160)
        mid = ((feed[0] + end[0]) / 2 + 30, max(feed[1], end[1]) + 90)
        pts = []
        for k in np.linspace(0, 1, 14):
            x = (1 - k) ** 2 * feed[0] + 2 * (1 - k) * k * mid[0] + k * k * end[0]
            y = (1 - k) ** 2 * feed[1] + 2 * (1 - k) * k * mid[1] + k * k * end[1]
            pts.append((x, y))
        if j2['yaw'] == 135:
            pts = []
        if pts:
            p.line(pts, (40, 40, 44), 14.0)
        for (x, y), (x2, y2) in zip(pts, pts[1:]):
            dx, dy = x2 - x, y2 - y
            n = math.hypot(dx, dy) or 1.0
            ax, ay = -dy / n, dx / n
            p.poly([(x + ax * 12, y + ay * 12), (x + ax * 12 + dx * 0.5, y + ay * 12 + dy * 0.5),
                    (x - ax * 6 + dx * 0.5, y - ay * 6 + dy * 0.5), (x - ax * 6, y - ay * 6)], BRASS, INK, 1.0)
        # spade grips at the back
        p.poly([P(0.0, -30), P(0.06, -30), P(0.06, 30), P(0.0, 30)], GUN_D, INK, 2.0)
        p.poly([P(0.02, -50), P(0.05, -50), P(0.05, 50), P(0.02, 50)], GUN_D, INK, 1.8)
        # the motor housing and receiver
        p.poly([P(0.05, -34), P(0.05, 32), P(0.46, 34), P(0.46, -36)], GUN, INK, 2.4)
        p.poly([P(0.1, -20), P(0.4, -20), P(0.4, 4), P(0.1, 4)], GUN_D, INK, 1.4)
        p.poly([P(0.36, -36), P(0.44, -36), P(0.44, -52), P(0.36, -52)], GUN_D, INK, 1.6)          # the feed chute
        # the carry handle
        p.line([P(0.16, 34), P(0.2, 70), P(0.4, 70), P(0.42, 34)], GUN_D, 9.0)
        # the barrels: three seen, turning
        w = 28 * (1.0 - 0.4 * eo)
        for k in range(3):
            v = (-w + w * k + (spin * 40) % w) if spin else (-w + w * k)
            p.poly([P(0.46, v - 8), P(1.0, v - 7), P(1.0, v + 7), P(0.46, v + 8)], GUN_L if k == 1 else GUN, INK, 1.6)
        for uu, ww in ((0.47, 1.25), (0.72, 1.2), (0.98, 1.2)):                                   # clamp and muzzle rings
            p.poly([P(uu - 0.015, -w * ww - 8), P(uu + 0.015, -w * ww - 8), P(uu + 0.015, w * ww + 8),
                    P(uu - 0.015, w * ww + 8)], GUN_D, INK, 1.8)
        if eo > 0.3:                                                                                # end on: the barrel ring
            c = P(1.0, 0)
            p.ell(c[0], c[1], w * 1.4, w * 1.4, GUN_D, INK, 2.0)
            for k in range(6):
                a = spin * 3 + k * math.pi / 3
                p.ell(c[0] + w * 0.8 * math.cos(a), c[1] + w * 0.8 * math.sin(a), 6, 6, (10, 10, 12), None)
        if rec is not None:
            rec['muzzle'] = tuple(v / B.SS for v in p.cam.P(*P(1.02, 0)))
        if flash > 0:
            muzzle_flash(p, P(1.02, 0), u, 90 * flash, eo > 0.5, seed)
        if skin:
            _fists(p, j2, skin)
    draw.held = skin is None
    draw.along = ('wrR', 'wrL', MINIGUN, MG_GRIP)
    draw.own_fists = True                  # it draws his fists on its grips (views.py: held, so hidden by his back)
    return draw


def tin_held(side='R'):
    """A tin of beans in the fist (ref beans-tin, the brand dropped): turquoise, a plain cream band, BAKED BEANS."""
    def draw(p, j2):
        c, d, n = _one_hand(j2, side)
        w, h = 0.066 / M / 2, 0.11 / M / 2
        p.poly([(c[0] - w, c[1] - h), (c[0] + w, c[1] - h), (c[0] + w, c[1] + h), (c[0] - w, c[1] + h)], (64, 190, 196), INK, 2.0)
        p.ell(c[0], c[1] - h, w, w * 0.3, (196, 200, 204), INK, 1.6)
        p.poly([(c[0] - w, c[1] - h * 0.3), (c[0] + w, c[1] - h * 0.3), (c[0] + w, c[1] + h * 0.35), (c[0] - w, c[1] + h * 0.35)],
               (244, 232, 200), INK, 1.4)
        for k in range(4):
            p.ell(c[0] - w * 0.5 + w * 0.33 * k, c[1] + h * 0.15, 4, 3, (222, 110, 50), None)
    draw.held = True
    return draw


# ------------------------------------------------------------------------------------------------ poses
def aim_two_hands(sp, grip_u, fore_u, full, at=(0.0, 0.0), butt=None, lean=4.0, j=None):
    """A long gun shouldered (crossbow) or at the hip (minigun): right hand on the grip, left along it; `at` swings
    the aim (degrees right of straight ahead, below level)."""
    j = j or V.standing(sp)
    sw = sp.get('shoulders', 150)
    ax, ay = math.radians(at[0]), math.radians(at[1])
    aim = (math.sin(ax) * math.cos(ay), math.sin(ay), math.cos(ax) * math.cos(ay))
    butt = butt or (sw * 0.42, 40.0, 10.0)
    grip = tuple(b + c * grip_u * full for b, c in zip(butt, aim))
    fore = tuple(b + c * fore_u * full for b, c in zip(butt, aim))
    V.arm_to(j, 'R', grip, 'down', 'fist')
    V.arm_to(j, 'L', fore, 'down', 'fist')
    j['hand'] = {'R': 'none', 'L': 'none'}             # the fists are drawn over the gun by the gun itself
    j['lean'] = lean
    return j


def crossbow_aim(sp, at=(0.0, 0.0), j=None, loaded=True, min_k=0.55):
    """`min_k`: the shortest it may be drawn. Seen from behind, pointing away, it is nearly end on (Sam's note 48,
    25 Oct: a floor of 0.55 drew a stub across his shoulder): pass a small one, and only the limbs show at his sides."""
    j = aim_two_hands(sp, CB_GRIP, CB_FORE, CROSSBOW, at, j=j)
    ax, ay = math.radians(at[0]), math.radians(at[1])
    aim = (math.sin(ax) * math.cos(ay), math.sin(ay), math.cos(ax) * math.cos(ay))
    j['props'] = j.get('props', []) + [crossbow(loaded, sp['skin'], aim, min_k)]
    return j


def minigun_hip(sp, at=(0.0, 0.0), spin=0.0, flash=0.0, belt_to=(64.0, -196.0), j=None, seed=0, rec=None):
    """Wes with the minigun at his hip, braced (feet apart, leaning in): right hand on the spade grip at his hip,
    left on the carry handle, the muzzle swinging to `at`."""
    j = j or V.standing(sp)
    sw = sp.get('shoulders', 150)
    j['footL'] = (-90, V.ANKLE_Y, 30.0)
    j['footR'] = (90, V.ANKLE_Y, -20.0)
    j = aim_two_hands(sp, MG_GRIP, MG_FORE, MINIGUN, at, butt=(sw * 0.55, 330.0, -40.0), lean=6.0, j=j)
    j['props'] = j.get('props', []) + [minigun(spin, flash, belt_to, seed, sp['skin'], rec)]
    return j


def glock_aim(sp, at=(0.0, 0.0), flash=0.0, j=None, two_hands=True, rec=None):
    """The Glock held out at arm's length, both hands (the left cupping the right), aimed at `at`."""
    j = j or V.standing(sp)
    sw = sp.get('shoulders', 150)
    ax, ay = math.radians(at[0]), math.radians(at[1])
    aim = (math.sin(ax) * math.cos(ay), math.sin(ay), math.cos(ax) * math.cos(ay))
    reach = 330.0
    hand = (sw * 0.15 + aim[0] * reach, 70.0 + aim[1] * reach, aim[2] * reach)
    V.arm_to(j, 'R', hand, 'out', 'fist')
    if two_hands:
        V.arm_to(j, 'L', (hand[0] - 18, hand[1] + 16, hand[2] - 10), 'out', 'fist')
    j['props'] = j.get('props', []) + [glock('R', flash, aim, rec)]
    j['grip'] = {'R'} | ({'L'} if two_hands else set())
    return j


def test(out):
    B.SS = 1
    img = B.canvas((232, 228, 220))
    cam = B.Cam(1.0, 540, 960)
    s = 0.42
    y0 = 300
    for i, lv in enumerate(range(1, 7)):
        sp = fear(ANDY, lv)
        person(img, cam, 110 + 170 * i, y0, s, sp, 0.0, 0)
    sp = fear(ANDY, 4)
    person(img, cam, 110, 1000, s, sp, 0.0, 45, crossbow_aim(sp, (20, 0)))
    person(img, cam, 300, 1000, s, sp, 0.0, 90, glock_aim(sp, (0, 0), flash=1.0))
    person(img, cam, 470, 1000, s, dict(sp, glock_tucked=True), 0.0, 180)
    wsp = dict(WES, bandana=True)
    person(img, cam, 640, 1000, s, wsp, 0.0, 0, minigun_hip(wsp, (-30, 0), spin=0.3, flash=1.0))
    person(img, cam, 820, 1000, s, wsp, 0.0, 45, minigun_hip(wsp, (0, 0)))
    j = V.standing(WES)
    V.arm_to(j, 'R', (180, 300, 120), 'down', 'fist')
    j['props'] = [machete('R')]
    j['grip'] = {'R'}
    person(img, cam, 980, 1000, s, WES, 0.0, 0, j)
    img.convert('RGB').save(out, quality=88)
    print('saved', out)


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'test':
        test(sys.argv[2])
    else:
        print(__doc__)
