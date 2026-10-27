#!/usr/bin/env python3
"""Patriots 3 (Sam, 27 Oct): the people, the MG42 and the bunker slit (refs in references/patriots-3/).

Everyone is built on the satire package (views.person: any angle, posed on the hidden skeleton; circle hands; hips
15% narrower than the shoulders; real heights), so the Patriot of The Patriots and The Patriots 2 (peepee.protester,
a front-only drawing) is rebuilt here to the current rules and can now be seen from every side.

- The Patriot: the same man. Thick-set with a belly; black knitted balaclava (ribbed, an eye slot showing his own
  eyes and brows, the knit moving over his mouth when he talks); black jacket with grey sleeves, a ribbed hem and a
  zip; olive combat trousers with cargo pockets; black boots; the round "PP" badge on one upper arm and his felt-tip
  doodle badge (the other PP, coloured in with a Union Jack) on the other.
- Two German soldiers of a static coastal division, June 1944 (refs german-1..6, mg42-1..6, bunker-1..4):
  the Gunner (MG-Schutze 1, about 30, lean long face, stubble, narrowed eyes; M40 helmet with a camouflage net;
  older tunic with the dark collar and collar tabs; Y-straps; pistol holster and MG tool pouch on the belt;
  jackboots) and the Loader (MG-Schutze 2, about 18, round young face, fair hair; plain M40 helmet; the later M43
  tunic; Y-straps, two triple rifle-ammo pouches, a stick grenade in his belt, the gas-mask canister and bread bag
  at his back; ankle boots and canvas gaiters). The breast eagle is drawn as a plain bird (no emblem in it).
- The MG42 at its real size (1.22 m), drawn as a 3D solid that turns with the gunner's body (rule 20): bakelite
  stock and pistol grip, the receiver and feed cover, the vented barrel jacket, the muzzle booster, the bipod; the
  ammo belt from its feed on the left, to an ammo box or the Loader's hands. Firing: a lumpy flash, the gun kicking
  back on the shoulder, spent cases falling under it, the belt drawn in.
- The bunker slit: the concrete embrasure (sill at 1.15 m), from inside behind the crew, from the beach, and in
  section from the side.

    python3 source/patriots3_cast.py sheet OUT.jpg     the three people in every view, faces, beside a 1.75 m person
    python3 source/patriots3_bunker.py sheet OUT.jpg   the MG42 and the crew firing through the slit (three cameras)
    python3 source/patriots3_bunker.py clip OUT.mp4    a few seconds of the crew firing (inside, then from the beach)
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
import figure as F               # noqa: E402
import limbs                     # noqa: E402
import prepper_cast as PC        # noqa: E402  (muzzle_flash; its arm hook passes everyone else straight through)
import peepee as PP              # noqa: E402  (the PP badges, as on the old protester)
from ed import INK, curve, oval  # noqa: E402
from satire_style import install_circle_hands, rough   # noqa: E402

mouths.install(B)
install_circle_hands(B)
F.guard(B)
limbs.install(B)

M = V.M_PER_UNIT                       # metres per person unit
U = 1.0 / M                            # person units per metre

# ------------------------------------------------------------------------------------------------ colours
BALA, BALA_RIB = (30, 30, 34), (50, 50, 57)
JACKET, SLEEVE = (38, 38, 44), (62, 62, 72)
COMBAT = (82, 86, 64)
P_SKIN = (236, 198, 178)

HELM, HELM_D = (84, 92, 84), (62, 68, 62)
NET = (58, 56, 44)
LEATHER, LEATHER_D = (34, 30, 28), (22, 20, 20)
STEEL_BTN = (150, 150, 140)
TUNIC_G, COLLAR_G, TROUSER_G = (98, 104, 86), (64, 74, 62), (92, 94, 86)
TUNIC_L, TROUSER_L = (106, 112, 94), (98, 100, 90)
TAB_SILVER = (196, 196, 184)
CANVAS = (122, 120, 100)
CANISTER = (92, 104, 88)
BREAD = (120, 112, 86)
FELT = (112, 86, 60)

# ------------------------------------------------------------------------------------------------ the people
PATRIOT = dict(name='Patriot', who='patriot', skin=P_SKIN, hw=76, hh=92, jaw='round', hair='bald', hair_c=BALA,
               brow_c=(104, 74, 54), brow_w=4.4, outfit='jumper', jacket=JACKET, sleeve=SLEEVE, trousers=COMBAT,
               shoe=(22, 20, 22), shoulders=168, bottom=500, balaclava=True, patches=True, belly=True, cargo=True,
               mouth='rest', seed=31)
GUNNER = dict(name='Gunner', who='gunner', skin=(226, 190, 164), hw=66, hh=96, jaw='long', hair='crop',
              hair_c=(120, 92, 64), brow_c=(92, 70, 52), brow_w=4.6, beard='stubble',
              beard_c=(110, 90, 72), nose='long', lid=2, creases=1, mouth='set', outfit='jumper', jacket=TUNIC_G,
              sleeve=TUNIC_G, collar_c=COLLAR_G, trousers=TROUSER_G, shoe=(24, 22, 22), shoulders=156, bottom=515,
              helmet=True, net=True, boots=True, kit='gunner', seed=32)
LOADER = dict(name='Loader', who='loader', skin=(240, 206, 186), hw=66, hh=86, jaw='round', hair='crop',
              hair_c=(196, 160, 100), brow_c=(170, 134, 84), brow_w=3.4, mouth='line', outfit='jumper', jacket=TUNIC_L,
              sleeve=TUNIC_L, collar_c=TUNIC_L, trousers=TROUSER_L, shoe=(64, 46, 34), shoulders=142, bottom=515,
              helmet=True, gaiters=True, kit='loader', seed=33)
CAST = {'patriot': PATRIOT, 'gunner': GUNNER, 'loader': LOADER}
HEIGHTS = {'Patriot': 1.78, 'Gunner': 1.80, 'Loader': 1.70}
OUTFIT = {'Patriot': {'jacket hem': 500}, 'Gunner': {'jacket hem': 515}, 'Loader': {'jacket hem': 515}}


def scale_for(sp, s):
    """A person's drawing scale for their real height (the skeleton is a 1.75 m person)."""
    return s * HEIGHTS.get(sp.get('name'), 1.75) / 1.75


# ------------------------------------------------------------------------------------------------ worn on the head
def _helmet_outline(view, hx, hy, hw, hh):
    """The M40 helmet's silhouette and its inner lines for one view (facing right): the dome, the short visor just over
    the brows, the skirt flaring out over the ears and the nape."""
    if view == 'front':
        out = [(hx - hw * 1.24, hy + 14), (hx - hw * 1.17, hy - hh * 0.3), (hx - hw * 1.1, hy - hh * 0.76),
               (hx - hw * 0.72, hy - hh * 1.13), (hx, hy - hh * 1.25), (hx + hw * 0.72, hy - hh * 1.13),
               (hx + hw * 1.1, hy - hh * 0.76), (hx + hw * 1.17, hy - hh * 0.3), (hx + hw * 1.24, hy + 14),
               (hx + hw * 1.07, hy + 10), (hx + hw * 0.97, hy - hh * 0.22), (hx + hw * 0.6, hy - hh * 0.35),
               (hx, hy - hh * 0.39), (hx - hw * 0.6, hy - hh * 0.35), (hx - hw * 0.97, hy - hh * 0.22),
               (hx - hw * 1.07, hy + 10)]
        dome = (out[1:8], 'front')
        lines = [[(hx - hw * 1.08, hy - hh * 0.5), (hx - hw * 0.99, hy - hh * 0.24)],
                 [(hx + hw * 1.08, hy - hh * 0.5), (hx + hw * 0.99, hy - hh * 0.24)]]
        lugs = [(hx - hw * 0.93, hy - hh * 0.64), (hx + hw * 0.93, hy - hh * 0.64)]
        shade = [(hx + hw * 0.5, hy - hh * 1.16), (hx + hw * 1.1, hy - hh * 0.76), (hx + hw * 1.17, hy - hh * 0.3),
                 (hx + hw * 1.24, hy + 14), (hx + hw * 1.07, hy + 10), (hx + hw * 0.97, hy - hh * 0.22),
                 (hx + hw * 0.8, hy - hh * 0.6)]
        strap = [[(hx - hw * 1.0, hy + 8), (hx - hw * 0.86, hy + hh * 0.62), (hx - hw * 0.4, hy + hh * 1.08)],
                 [(hx + hw * 1.0, hy + 8), (hx + hw * 0.86, hy + hh * 0.62), (hx + hw * 0.4, hy + hh * 1.08)]]
    elif view == 'three':
        out = [(hx + hw * 1.14, hy - 30), (hx + hw * 1.04, hy - hh * 0.76), (hx + hw * 0.56, hy - hh * 1.15),
               (hx - hw * 0.12, hy - hh * 1.25), (hx - hw * 0.78, hy - hh * 1.08), (hx - hw * 1.14, hy - hh * 0.62),
               (hx - hw * 1.24, hy - 4), (hx - hw * 1.3, hy + 26), (hx - hw * 1.04, hy + 20), (hx - hw * 0.62, hy + 4),
               (hx - hw * 0.3, hy - hh * 0.24), (hx + hw * 0.2, hy - hh * 0.38), (hx + hw * 0.78, hy - hh * 0.41)]
        dome = (out[1:6], 'three')
        lines = [[(hx - hw * 1.1, hy - hh * 0.46), (hx - hw * 0.62, hy - hh * 0.4), (hx - hw * 0.3, hy - hh * 0.36),
                  (hx + hw * 0.2, hy - hh * 0.5)]]
        lugs = [(hx - hw * 0.68, hy - hh * 0.66)]
        shade = [(hx - hw * 0.4, hy - hh * 1.2), (hx - hw * 0.78, hy - hh * 1.08), (hx - hw * 1.14, hy - hh * 0.62),
                 (hx - hw * 1.24, hy - 4), (hx - hw * 1.3, hy + 26), (hx - hw * 1.04, hy + 20), (hx - hw * 0.62, hy + 4),
                 (hx - hw * 0.9, hy - hh * 0.6)]
        strap = [[(hx - hw * 0.62, hy + 6), (hx - hw * 0.2, hy + hh * 0.66), (hx + hw * 0.3, hy + hh * 1.12)]]
    elif view == 'side':
        out = [(hx + 78, hy - 30), (hx + 64, hy - hh * 0.8), (hx + 30, hy - hh * 1.15), (hx - 20, hy - hh * 1.26),
               (hx - 66, hy - hh * 1.06), (hx - 90, hy - hh * 0.62), (hx - 98, hy - 8), (hx - 108, hy + 28),
               (hx - 86, hy + 24), (hx - 44, hy + 10), (hx - 12, hy - 2), (hx + 16, hy - 18), (hx + 48, hy - 28)]
        dome = (out[1:7], 'side')
        lines = [[(hx + 66, hy - 44), (hx + 16, hy - 32), (hx - 30, hy - 14), (hx - 74, hy - 12), (hx - 94, hy - 34)]]
        lugs = [(hx - 12, hy - hh * 0.66)]
        shade = [(hx - 66, hy - hh * 1.06), (hx - 90, hy - hh * 0.62), (hx - 98, hy - 8), (hx - 108, hy + 28),
                 (hx - 86, hy + 24), (hx - 44, hy + 10), (hx - 60, hy - hh * 0.5)]
        strap = [[(hx - 8, hy + 2), (hx + 8, hy + 60), (hx + 22, hy + 104)]]
    else:                                         # from behind: the dome and the skirt flaring down over the nape
        o = -0.16 * hw if view == 'three_back' else 0.0
        out = [(hx - hw * 1.3, hy + 26), (hx - hw * 1.2, hy - hh * 0.3), (hx - hw * 1.1 + o, hy - hh * 0.78),
               (hx - hw * 0.7 + o, hy - hh * 1.13), (hx + o, hy - hh * 1.25), (hx + hw * 0.7 + o, hy - hh * 1.13),
               (hx + hw * 1.1 + o, hy - hh * 0.78), (hx + hw * 1.2, hy - hh * 0.3), (hx + hw * 1.3, hy + 26),
               (hx + hw * 0.8, hy + 36), (hx, hy + 40), (hx - hw * 0.8, hy + 36)]
        dome = (out[1:8], 'back')
        lines = [[(hx - hw * 1.12, hy - 14), (hx, hy - 4), (hx + hw * 1.12, hy - 14)]]
        lugs = [(hx - hw * 0.94, hy - hh * 0.6)] if view == 'three_back' else \
            [(hx - hw * 0.94, hy - hh * 0.6), (hx + hw * 0.94, hy - hh * 0.6)]
        shade = [(hx + hw * 0.4 + o, hy - hh * 1.18), (hx + hw * 1.1 + o, hy - hh * 0.78), (hx + hw * 1.2, hy - hh * 0.3),
                 (hx + hw * 1.3, hy + 26), (hx + hw * 0.8, hy + 36), (hx + hw * 0.5, hy - hh * 0.4)]
        strap = []
    return out, dome, lines, lugs, shade, strap


def _net(p, dome, seed):
    """A camouflage net over the dome: chords between points on its (convex) outline, crossing as a loose diamond
    lattice, with a few knots. Chords of a convex shape stay inside it."""
    pts = curve(dome, 6)[:-6]
    n = len(pts)
    if n < 8:
        return
    rng = np.random.default_rng(seed)
    step = max(2, n // 9)
    for i in range(0, n, step):
        for di in (n // 3, -n // 3):
            j = i + di
            if 0 <= j < n:
                a, b = pts[i], pts[j]
                p.line([a, b], NET, 1.8)
    for _ in range(6):
        i, j = rng.integers(0, n, 2)
        u = rng.uniform(0.3, 0.7)
        x = pts[i][0] + (pts[j][0] - pts[i][0]) * u
        y = pts[i][1] + (pts[j][1] - pts[i][1]) * u
        p.ell(x, y, 2.6, 2.6, NET, None)


def stahlhelm(p, view, sp, hx, hy):
    """The M40 steel helmet (refs german-1, -2, -6; mg42-1): field grey, matt; a camouflage net on the Gunner's."""
    hw, hh = sp.get('hw', 70), sp.get('hh', 90)
    out, dome, lines, lugs, shade, strap = _helmet_outline(view, hx, hy, hw, hh)
    for s in (strap if view == 'side' else ()):    # the chinstrap (seen clearly only from the side)
        p.line(s, LEATHER, 3.2)
    shape = curve(out, 3)
    p.poly(shape, HELM, None)
    p.poly(curve(shade, 3), HELM_D, None)          # a flat shadow side
    p.poly(shape, None, INK, 2.6)
    for ln in lines:
        p.line(curve(ln, 3)[:-3] if len(ln) > 2 else ln, HELM_D, 2.0)
    for (x, y) in lugs:                            # the vent lugs
        p.ell(x, y, 4.2, 4.2, HELM_D, INK, 1.4)
    if sp.get('net'):
        _net(p, dome[0], sp.get('seed', 1))
        p.poly(shape, None, INK, 2.6)


def _talking(sp):
    m = sp.get('mouth', 'rest')
    if isinstance(m, str) and m.startswith('v:'):
        return {'rest': 0.0, 'MBP': 0.0, 'etc': 0.45, 'E': 0.6, 'AI': 1.0, 'O': 0.8, 'U': 0.5, 'WQ': 0.4,
                'FV': 0.3, 'L': 0.6}.get(m[2:], 0.5)
    return {'talk': 0.6, 'shout': 1.0, 'open': 0.8, 'mid': 0.5, 'small': 0.3}.get(m, 0.0)


def _span(poly, x):
    """Where a vertical line at x enters and leaves a closed shape: (top, bottom), or None if it misses."""
    ys = []
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (x0 - x) * (x1 - x) <= 0 and x0 != x1:
            ys.append(y0 + (y1 - y0) * (x - x0) / (x1 - x0))
    return (min(ys), max(ys)) if len(ys) >= 2 else None


def _grow(pts, cx, cy, k):
    return [(cx + (x - cx) * k, cy + (y - cy) * k) for x, y in pts]


def _ribs(p, shape, xs, holes=()):
    """The knit's ribs: vertical lines inside the shape, broken where a hole (the eye slot) crosses them."""
    for x in xs:
        sp_ = _span(shape, x)
        if not sp_:
            continue
        top, bot = sp_[0] + 5, sp_[1] - 5
        cuts = [h for h in (_span(hh, x) for hh in holes) if h]
        segs, y = [], top
        for a, b in sorted(cuts):
            if a - 4 > y:
                segs.append((y, a - 4))
            y = max(y, b + 4)
        if bot > y:
            segs.append((y, bot))
        for a, b in segs:
            p.line([(x, a), (x, b)], BALA_RIB, 1.4)


def balaclava(p, view, sp, hx, hy):
    """The Patriot's black knitted balaclava (as in The Patriots): ribbed, over the whole head and the ears, an eye slot
    that shows his own eyes and brows (the face is drawn underneath), the knit moving over his mouth as he talks. Its
    neck runs down into his collar (drawn with the jacket, under the head)."""
    hw, hh = sp.get('hw', 76), sp.get('hh', 92)
    lv = _talking(sp)
    if view in ('back', 'three_back'):
        bt = view == 'three_back'
        for sg in ((-1,) if bt else (-1, 1)):
            p.ell(hx + sg * (hw + 2), hy + 6, 14, 24, BALA, INK, 2.4)
        if bt:
            p.ell(hx + hw * 0.58, hy + 6, 13, 23, BALA, INK, 2.4)
        head = [(hx - hw, hy - 10), (hx - hw * 0.86, hy - hh * 0.72), (hx, hy - hh * 1.06), (hx + hw * 0.86, hy - hh * 0.72),
                (hx + hw, hy - 10), (hx + hw * 0.92, hy + hh * 0.42), (hx + 42, hy + hh * 0.7), (hx + 42, hy + 152),
                (hx - 42, hy + 152), (hx - 42, hy + hh * 0.7), (hx - hw * 0.92, hy + hh * 0.42)]
        shape = curve(_grow(head, hx, hy, 1.03), 3)
        p.poly(shape, BALA, INK, 2.6)
        _ribs(p, shape, [hx + 15 * k for k in range(-5, 6)])
        p.poly(shape, None, INK, 2.6)
        return
    if view == 'side':
        p.ell(hx - 18, hy + 8, 14, 24, BALA, INK, 2.2)               # the knit-covered ear (drawn again on top)
        face = [(hx - 70, hy - 36), (hx - 64, hy - 76), (hx - 40, hy - hh - 8), (hx + 22, hy - hh - 8), (hx + 62, hy - 58), (hx + 68, hy - 36),
                (hx + 26, hy - 36), (hx + 24, hy + 4), (hx + 74, hy + 4), (hx + 88, hy + 28), (hx + 68, hy + 38),
                (hx + 72, hy + 54 + 6 * lv), (hx + 66, hy + 62), (hx + 70, hy + 76), (hx + 58, hy + 104),
                (hx + 30, hy + 114), (hx + 30, hy + 152), (hx - 34, hy + 152), (hx - 40, hy + 80), (hx - 64, hy + 40)]
        shape = curve(face, 2)
        p.poly(shape, BALA, INK, 2.6)
        _ribs(p, shape, [hx - 52 + 16 * k for k in range(8)], [curve([(hx + 26, hy - 36), (hx + 80, hy - 36),
                                                                        (hx + 80, hy + 4), (hx + 24, hy + 4)], 1)])
        p.poly(shape, None, INK, 2.6)
        p.ell(hx - 18, hy + 8, 14, 24, BALA, INK, 2.2)
        return
    # front and three-quarter: the head and ears in knit, with the eye slot cut out (the eyes and brows show through)
    three = view == 'three'
    fx = hx + (0.4 * hw if three else sp.get('turn', 0.0) * hw * 0.22)
    if three:
        p.ell(hx - 0.5 * hw, hy + 6, 14, 24, BALA, INK, 2.4)
        head = [(hx - hw, hy - 10), (hx - hw * 0.86, hy - hh * 0.72), (hx - hw * 0.3, hy - hh * 1.04),
                (hx + hw * 0.45, hy - hh * 0.98), (hx + hw * 0.92, hy - hh * 0.6), (hx + hw * 1.0, hy - 6),
                (hx + hw * 0.92, hy + hh * 0.55), (hx + hw * 0.62, hy + hh * 1.0), (hx + hw * 0.3, hy + hh * 1.14),
                (hx - hw * 0.22, hy + hh * 1.04), (hx - hw * 0.72, hy + hh * 0.66), (hx - hw * 0.96, hy + hh * 0.3)]
        slot = [(fx - 52, hy - 40), (fx + 36, hy - 42), (fx + 44, hy - 30), (fx + 44, hy + 8), (fx - 54, hy + 10)]
    else:
        for sg in (-1, 1):
            p.ell(hx + sg * (hw + 2), hy + 6, 14, 24, BALA, INK, 2.4)
        head = B.head_outline(hx, hy, hw, hh, 'round')
        slot = [(fx - 60, hy - 42), (fx + 56, hy - 42), (fx + 58, hy + 10), (fx - 62, hy + 10)]
    oc = curve(_grow(head, hx, hy, 1.03), 3) if three else _grow(head, hx, hy, 1.03)
    sc = curve(rough(slot, 2, 9), 3)
    # one shape with a hole: the outline, a cut in to the slot, round the slot, and back out the same way
    k = int(np.argmin([(x - sc[0][0]) ** 2 + (y - sc[0][1]) ** 2 for x, y in oc]))
    p.poly(oc[:k + 1] + sc + [sc[0]] + oc[k:], BALA, None)
    _ribs(p, oc, [fx + 15 * i for i in range(-6, 7)], [sc])
    if lv > 0.05:                                       # the knit pulled in and out over his mouth as he talks
        p.poly(oval(fx - 2, hy + 60, 20, 3 + 8 * lv, 18), (56, 56, 64), None)
        p.line(oval(fx - 2, hy + 60, 20, 3 + 8 * lv, 18, 0.25, math.pi - 0.25), (16, 16, 20), 1.6)
    p.poly(oc, None, INK, 2.6)
    p.poly(sc, None, INK, 2.2)


# ------------------------------------------------------------------------------------------------ worn on the body
def _box(view, sp, y):
    """(left, right) edges of the torso at height y in each view's own drawing (views.torso_view / burnham.torso)."""
    sw = sp.get('shoulders', 150)
    bottom = sp.get('bottom', V.JACKET)
    if view == 'side':
        d = 0.6 * sw
        return -d * 1.0, d * 1.06
    l, r = {'front': (-sw - 6, sw + 6), 'three': (-sw * 0.97, sw * 0.84),
            'three_back': (-(sw + 6) * 0.9, (sw + 6) * 0.9), 'back': (-sw - 6, sw + 6)}[view]
    if y > 200:
        u = min(1.0, (y - 200) / max(1.0, bottom - 200))
        k = 1 - (1 - B.HEM) * u
        l, r = l * k, r * k
    return l, r


def patriot_jacket(p, view, sp):
    """His black jacket (The Patriots): a stand collar, the zip, a ribbed hem; the belly under it (front: a curve and
    a slight swell at the sides; three-quarter and side: pushing the front out)."""
    sw, bottom = sp.get('shoulders', 168), sp.get('bottom', 500)
    jd = B.dk(JACKET, 0.7)
    if view in ('front', 'three', 'side'):
        o = {'front': 0.0, 'three': sp.get('v_at', 0.32 * sw), 'side': 0.62 * sw}[view]
        if view != 'front':                            # the belly pushes the front of the jacket out
            if view == 'three':
                pts = [(sw * 0.84, 200), (sw * 0.98, 300), (sw * 0.96, 400), (sw * 0.78 * B.HEM, bottom), (sw * 0.6, bottom),
                       (sw * 0.6, 200)]
            else:
                d = 0.6 * sw
                pts = [(d * 1.08, 170), (d * 1.42, 300), (d * 1.4, 420), (d * 1.12, bottom), (d * 0.6, bottom), (d * 0.6, 170)]
            p.poly(curve(pts, 4), JACKET, None)
            p.line(curve(pts, 4)[:30], INK, 2.6)
        else:
            for sg in (-1, 1):                          # a slight swell at the sides
                pts = [(sg * (sw + 6), 210), (sg * (sw + 14), 330), (sg * (sw * B.HEM + 6), 470), (sg * sw * 0.7, 470),
                       (sg * sw * 0.7, 210)]
                p.poly(curve(pts, 4), JACKET, None)
                p.line(curve(pts, 4)[:20], INK, 2.6)
            p.line(oval(0, 300, 128, 150, 22, 0.45, math.pi - 0.45), (18, 18, 22), 2.0)
        # the balaclava's neck in his collar, then the stand collar (lighter) and the zip
        nk = 40 if view == 'front' else 34
        p.poly([(o * 0.3 - nk, -92), (o * 0.3 + nk, -92), (o * 0.3 + nk + 4, 6), (o * 0.3 - nk - 4, 6)], BALA, INK, 2.4)
        if view == 'side':
            p.poly([(-30, -26), (o - 2, -24), (o + 4, 30), (-34, 26)], B.lt(JACKET, 1.35), INK, 2.4)
        else:
            w = 64 if view == 'front' else 56
            p.poly([(o - w, -24), (o + w * (1 if view == 'front' else 0.8), -24), (o + w * (1.18 if view == 'front' else 0.9), 30),
                    (o - w * 1.18, 30)], B.lt(JACKET, 1.35), INK, 2.4)
        p.line([(o, 30), (o + 6, 200), (o + 12, 340), (o + 6, bottom - 26)], (96, 96, 104), 2.2)
    else:                                               # from behind: the collar and the back seam
        o = -0.22 * sw if view == 'three_back' else 0.0
        p.poly([(-44, -92), (44, -92), (48, 6), (-48, 6)], BALA, INK, 2.4)
        p.poly([(-70, -20), (70, -20), (78, 26), (-78, 26)], B.lt(JACKET, 1.35), INK, 2.4)
        p.line([(o, 30), (o, bottom - 26)], jd, 2.0)
    l, r = _box(view, sp, bottom - 13)
    p.poly([(l + 2, bottom - 26), (r - 2, bottom - 26), (r, bottom), (l, bottom)], B.dk(JACKET, 0.8), INK, 2.0)
    for x in np.linspace(l + 14, r - 14, 12):          # the ribbed hem
        p.line([(x, bottom - 22), (x, bottom - 4)], (24, 24, 28), 1.2)


def _eagle(p, x, y, k=1.0):
    """The breast eagle as a plain bird: spread wings over a small blank roundel (drawn without any emblem)."""
    c = (178, 176, 160)
    wing = [(x - 34 * k, y - 4 * k), (x - 20 * k, y - 12 * k), (x - 6 * k, y - 6 * k), (x, y - 12 * k), (x + 6 * k, y - 6 * k),
            (x + 20 * k, y - 12 * k), (x + 34 * k, y - 4 * k), (x + 18 * k, y + 2 * k), (x + 6 * k, y + 4 * k),
            (x, y + 8 * k), (x - 6 * k, y + 4 * k), (x - 18 * k, y + 2 * k)]
    p.poly(wing, c, INK, 1.4)
    for sg in (-1, 1):
        p.line([(x + sg * 8 * k, y - 4 * k), (x + sg * 28 * k, y - 4 * k)], B.dk(c, 0.7), 1.0)
    p.ell(x, y + 14 * k, 7 * k, 7 * k, None, c, 2.0)


def _pocket(p, cx, y0, y1, w, col, button=True):
    """A pleated patch pocket with a scalloped flap."""
    p.poly([(cx - w, y0 + 18), (cx + w, y0 + 18), (cx + w + 2, y1), (cx - w - 2, y1)], col, INK, 1.8)
    p.line([(cx, y0 + 24), (cx, y1 - 2)], B.dk(col, 0.75), 1.6)
    p.poly([(cx - w - 2, y0), (cx + w + 2, y0), (cx + w + 2, y0 + 20), (cx + 10, y0 + 24), (cx, y0 + 32), (cx - 10, y0 + 24),
            (cx - w - 2, y0 + 20)], col, INK, 1.8)
    if button:
        p.ell(cx, y0 + 20, 5, 5, STEEL_BTN, INK, 1.2)


def tunic(p, view, sp):
    """The field-grey tunic over the plain torso: collar (dark, with the collar tabs, on the older tunic), buttons,
    the four pleated pockets, the shoulder straps, the breast eagle; then the belt and the kit on it (kit())."""
    sw, bottom = sp.get('shoulders', 150), sp.get('bottom', 515)
    tc, cc = sp.get('jacket', TUNIC_G), sp.get('collar_c', TUNIC_G)
    td = B.dk(tc, 0.72)
    if view == 'front':
        for sg in (-1, 1):                             # the shoulder straps, piped in white
            p.poly([(sg * 46, -2), (sg * (sw - 34), 16), (sg * (sw - 30), 42), (sg * 44, 22)], tc, INK, 1.8)
            p.line([(sg * 50, 2), (sg * (sw - 34), 20)], (206, 206, 196), 1.2)
            p.ell(sg * 56, 12, 4.5, 4.5, STEEL_BTN, INK, 1.0)
        for sg in (-1, 1):                             # the collar: two points down at the throat
            p.poly([(sg * 40, -14), (sg * 76, 6), (sg * 54, 50), (sg * 6, 34), (sg * 4, 8)], cc, INK, 2.0)
            tab = [(sg * 30, 18), (sg * 56, 24), (sg * 50, 40), (sg * 24, 34)]
            p.poly(tab, B.dk(cc, 0.8), None)
            p.line([(sg * 28, 24), (sg * 52, 30)], TAB_SILVER, 1.6)
            p.line([(sg * 26, 30), (sg * 50, 36)], TAB_SILVER, 1.6)
        p.line([(0, 36), (2, bottom)], td, 2.0)       # the button placket
        for y in (70, 140, 210, 280, 450):
            p.ell(4, y, 6, 6, STEEL_BTN, INK, 1.2)
        for sg in (-1, 1):
            _pocket(p, sg * 74, 104, 198, 34, tc)
            _pocket(p, sg * 84, 420, bottom - 8, 40, tc)
        _eagle(p, -74, 86, 0.9)                        # worn on the right breast: our left as he faces us
    elif view == 'three':
        o = sp.get('v_at', 0.32 * sw)
        p.poly([(-24, -14), (o + 26, -14), (o + 40, 6), (o + 12, 48), (-30, 40)], cc, INK, 2.0)   # the collar
        p.line([(o + 4, 36), (o + 8, bottom)], td, 2.0)
        for y in (70, 140, 210, 280, 450):
            p.ell(o + 10, y, 5.5, 5.5, STEEL_BTN, INK, 1.2)
        _pocket(p, o - 74, 104, 198, 32, tc)
        _pocket(p, o + 52, 104, 198, 20, tc)
        _pocket(p, o - 82, 420, bottom - 8, 36, tc)
        _eagle(p, o - 74, 86, 0.8)
        p.poly([(-sw * 0.62, 2), (-sw * 0.92, 30), (-sw * 0.88, 50), (-sw * 0.6, 26)], tc, INK, 1.8)   # near shoulder strap
    elif view == 'side':
        d = 0.6 * sw
        p.poly([(-30, -14), (d * 0.5, -10), (d * 0.66, 20), (d * 0.2, 40), (-34, 30)], cc, INK, 2.0)
        p.line([(d * 0.95, 60), (d * 1.04, bottom)], td, 1.8)
        _pocket(p, d * 0.62, 104, 198, 16, tc, button=False)
        _pocket(p, d * 0.6, 420, bottom - 8, 20, tc, button=False)
        p.poly([(-d * 0.6, -4), (d * 0.4, -4), (d * 0.38, 18), (-d * 0.62, 18)], tc, INK, 1.8)       # the shoulder strap
    else:
        k = 0.9 if view == 'three_back' else 1.0
        o = -0.22 * sw if view == 'three_back' else 0.0
        p.poly([(-56 * k, -16), (56 * k, -16), (60 * k, 14), (-60 * k, 14)], cc, INK, 2.0)          # the collar's back
        p.line([(o, 20), (o, bottom)], td, 2.0)                                                    # the back seam
        for sg in (-1, 1):
            p.poly([(sg * 50 * k, 0), (sg * (sw - 34) * k, 18), (sg * (sw - 30) * k, 40), (sg * 48 * k, 22)], tc, INK, 1.8)
    kit(p, view, sp)


def _ystraps(p, view, sp, belt_y):
    sw = sp.get('shoulders', 150)
    lw = 13
    if view == 'front':
        for sg in (-1, 1):
            p.poly([(sg * 62, -6), (sg * 76, -6), (sg * 74, belt_y), (sg * 60, belt_y)], LEATHER, INK, 1.6)
            p.ell(sg * 67, 176, 7, 7, None, STEEL_BTN, 2.2)                                         # the D-rings
    elif view == 'three':
        o = sp.get('v_at', 0.32 * sw)
        p.poly([(o - 76, -4), (o - 62, -4), (o - 64, belt_y), (o - 78, belt_y)], LEATHER, INK, 1.6)
        p.poly([(o + 34, -4), (o + 46, -4), (o + 44, belt_y), (o + 32, belt_y)], LEATHER, INK, 1.6)
    elif view == 'side':
        d = 0.6 * sw
        p.poly([(d * 0.1, -8), (d * 0.3, -8), (d * 0.8, belt_y), (d * 0.62, belt_y)], LEATHER, INK, 1.6)
        p.poly([(-d * 0.1, -8), (d * 0.08, -8), (-d * 0.62, belt_y), (-d * 0.8, belt_y)], LEATHER, INK, 1.6)
    else:                                               # the Y: two straps meeting between the shoulder blades
        k = 0.9 if view == 'three_back' else 1.0
        o = -0.22 * sw if view == 'three_back' else 0.0
        for sg in (-1, 1):
            p.poly([(sg * 64 * k, -6), (sg * 78 * k, -6), (o + sg * 8, 170), (o - sg * 6, 170)], LEATHER, INK, 1.6)
        p.poly([(o - lw / 2, 160), (o + lw / 2, 160), (o + lw / 2, belt_y), (o - lw / 2, belt_y)], LEATHER, INK, 1.6)
        p.ell(o, 166, 9, 9, None, STEEL_BTN, 2.4)


def _triple_pouch(p, cx, y, w=60):
    """A triple rifle-ammo pouch on the belt: three rounded leather boxes side by side."""
    for k in range(3):
        x0 = cx - w / 2 + k * w / 3
        p.poly(curve([(x0 + 1, y - 26), (x0 + w / 3 - 1, y - 26), (x0 + w / 3 - 1, y + 20), (x0 + w / 6, y + 26),
                      (x0 + 1, y + 20)], 3), LEATHER, INK, 1.6)
        p.line([(x0 + 3, y - 12), (x0 + w / 3 - 3, y - 12)], LEATHER_D, 1.4)


def kit(p, view, sp):
    """The belt (black leather, the steel buckle) and what hangs from it, per soldier."""
    sw, bottom = sp.get('shoulders', 150), sp.get('bottom', 515)
    belt_y = 386
    l, r = _box(view, sp, belt_y + 12)
    _ystraps(p, view, sp, belt_y)
    p.poly([(l, belt_y), (r, belt_y), (r + 1, belt_y + 26), (l - 1, belt_y + 26)], LEATHER, INK, 2.0)
    who = sp.get('kit')
    if view == 'front':
        p.poly([(-18, belt_y - 3), (18, belt_y - 3), (18, belt_y + 29), (-18, belt_y + 29)], (140, 142, 134), INK, 1.8)
        p.ell(0, belt_y + 13, 8, 8, None, (110, 112, 104), 1.6)
        if who == 'loader':
            for sg in (-1, 1):
                _triple_pouch(p, sg * 70, belt_y + 4)
            # the stick grenade tucked in his belt: the wooden handle, the steel head on its end
            p.poly([(34, belt_y - 112), (46, belt_y - 112), (50, belt_y + 44), (38, belt_y + 44)], (150, 112, 70), INK, 1.6)
            p.poly(curve([(23, belt_y - 168), (55, belt_y - 170), (57, belt_y - 112), (25, belt_y - 110)], 2),
                   (80, 88, 76), INK, 1.8)
            p.line([(25, belt_y - 120), (56, belt_y - 121)], B.dk((80, 88, 76), 0.7), 1.4)
        else:
            p.poly(curve([(84, belt_y + 4), (136, belt_y + 2), (140, belt_y + 70), (112, belt_y + 92), (86, belt_y + 70)], 3),
                   (52, 40, 32), INK, 1.8)                     # the pistol holster
            p.line([(86, belt_y + 30), (138, belt_y + 30)], B.dk((52, 40, 32), 0.7), 1.4)
            p.poly([(-128, belt_y - 6), (-80, belt_y - 6), (-82, belt_y + 46), (-126, belt_y + 46)], LEATHER, INK, 1.8)
            p.line([(-126, belt_y + 10), (-82, belt_y + 10)], LEATHER_D, 1.4)   # the MG tool pouch
    elif view == 'three':
        o = sp.get('v_at', 0.32 * sw)
        p.poly([(o - 6, belt_y - 3), (o + 24, belt_y - 3), (o + 24, belt_y + 29), (o - 6, belt_y + 29)], (140, 142, 134), INK, 1.8)
        if who == 'loader':
            _triple_pouch(p, o - 76, belt_y + 4, 54)
            _triple_pouch(p, o + 52, belt_y + 4, 34)
        else:
            p.poly([(o - 120, belt_y - 6), (o - 78, belt_y - 6), (o - 80, belt_y + 46), (o - 118, belt_y + 46)], LEATHER, INK, 1.8)
        _canister(p, -sw * 0.86, belt_y + 20, 0.8)
    elif view == 'side':
        d = 0.6 * sw
        if who == 'loader':
            _triple_pouch(p, d * 0.78, belt_y + 4, 30)
        else:
            p.poly(curve([(d * 0.3, belt_y + 4), (d * 0.7, belt_y + 2), (d * 0.72, belt_y + 70), (d * 0.5, belt_y + 92),
                          (d * 0.3, belt_y + 70)], 3), (52, 40, 32), INK, 1.8)
        _canister(p, -d * 0.7, belt_y + 30, 1.0)
    else:
        k = 0.9 if view == 'three_back' else 1.0
        _bread_bag(p, -sw * 0.56 * k, belt_y + 26)
        _canister(p, sw * 0.6 * k, belt_y + 26, 1.0)


def _canister(p, cx, y, k=1.0):
    """The gas-mask canister: a ribbed field-grey cylinder hanging at the back of the hip."""
    w, h = 34 * k, 120
    p.poly(curve([(cx - w, y), (cx + w, y), (cx + w, y + h), (cx, y + h + 8), (cx - w, y + h)], 3), CANISTER, INK, 1.8)
    for yy in (y + 26, y + 52, y + 78, y + 104):
        p.line([(cx - w + 2, yy), (cx + w - 2, yy)], B.dk(CANISTER, 0.72), 1.6)
    p.poly([(cx - w - 2, y - 10), (cx + w + 2, y - 10), (cx + w + 2, y + 6), (cx - w - 2, y + 6)], B.dk(CANISTER, 0.85), INK, 1.6)


def _bread_bag(p, cx, y):
    """The bread bag with the felt-covered canteen strapped to it."""
    p.poly(curve([(cx - 50, y), (cx + 46, y), (cx + 48, y + 96), (cx - 52, y + 96)], 3), BREAD, INK, 1.8)
    p.line([(cx - 50, y + 30), (cx + 46, y + 30)], B.dk(BREAD, 0.75), 1.4)
    p.poly(curve([(cx - 20, y + 20), (cx + 20, y + 20), (cx + 26, y + 90), (cx, y + 104), (cx - 26, y + 90)], 3), FELT, INK, 1.8)
    p.poly([(cx - 14, y + 6), (cx + 14, y + 6), (cx + 14, y + 26), (cx - 14, y + 26)], (30, 30, 32), INK, 1.4)


# ------------------------------------------------------------------------------------------------ arms and legs
_ARM, _LEG = V.arm, V.leg


def _arm(p, j2, side, sp, shape=None):
    _ARM(p, j2, side, sp, shape)
    if sp.get('patches'):                              # his badges on the upper arms, as in The Patriots
        sh, el = j2['sh' + side], j2['el' + side]
        if math.hypot(el[0] - sh[0], el[1] - sh[1]) > 90:      # only when the upper arm is seen side on
            flip = getattr(p.cam, 'flip', 1)
            kind = 'doodle' if (side == 'L') == (flip > 0) else 'PP'
            PP.patch(p.img, p, sh, el, kind)


def _leg(p, j, side, yaw, sp):
    _LEG(p, j, side, yaw, sp)
    hip3, foot3 = j['hip' + side], j['foot' + side]
    knee3 = V.knee_of(j, side)
    hip, knee, foot = (V.project(q, yaw)[0] for q in (hip3, knee3, foot3))

    def at(a, b, u):
        return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
    if sp.get('boots'):                               # jackboots: the black shaft up to just under the knee
        V.tube(p, [at(knee, foot, 0.2), foot], [38 * 0.8 + 38 * 0.2 * 0.7 + 3, 30], sp.get('shoe', (24, 22, 22)))
        top = at(knee, foot, 0.2)
        p.line([(top[0] - 34, top[1]), (top[0] + 34, top[1])], INK, 2.0)
    if sp.get('gaiters'):                             # canvas gaiters over the ankle, two straps
        V.tube(p, [at(knee, foot, 0.74), foot], [31, 29], CANVAS)
        for u in (0.82, 0.92):
            c = at(knee, foot, u)
            p.line([(c[0] - 28, c[1]), (c[0] + 28, c[1])], B.dk(CANVAS, 0.6), 2.4)
    if sp.get('cargo'):                               # combat trousers: a cargo pocket on the outside of the thigh
        dx, dy = knee[0] - hip[0], knee[1] - hip[1]
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        nx, ny = -uy, ux
        sg = -1 if side == 'L' else 1
        if yaw in (0, 180):
            sh = sg * (1 if yaw == 0 else -1) * 10
        else:
            sh = 0
        c0 = (hip[0] + dx * 0.52 + nx * sh, hip[1] + dy * 0.52 + ny * sh)
        c1 = (hip[0] + dx * 0.86 + nx * sh, hip[1] + dy * 0.86 + ny * sh)
        w = 26
        q = [(c0[0] + nx * w, c0[1] + ny * w), (c1[0] + nx * w, c1[1] + ny * w), (c1[0] - nx * w, c1[1] - ny * w),
             (c0[0] - nx * w, c0[1] - ny * w)]
        p.poly(q, B.dk(COMBAT, 0.86), INK, 2.0)
        f = (c0[0] + ux * 16, c0[1] + uy * 16)
        p.line([(f[0] + nx * w, f[1] + ny * w), (f[0] - nx * w, f[1] - ny * w)], INK, 1.6)


V.arm, V.leg = _arm, _leg


def dress(sp):
    body, head = [], []
    if sp.get('balaclava'):
        body.append(patriot_jacket)
        head.append(balaclava)
    if sp.get('kit'):
        body.append(tunic)
    if sp.get('helmet'):
        head.append(stahlhelm)
    return body, head


def outfit(j, sp):
    body, head = dress(sp)
    j['body_props'] = body + j.get('body_props', [])
    j['head_props'] = head + j.get('head_props', [])
    return j


def person(img, cam, x, y, s, sp, t=0.0, yaw=0, j=None, head_yaw=None):
    """Draw one of the cast (scale s is for a 1.75 m person: their own height is applied here)."""
    j = j or V.standing(sp)
    if not j.get('_dressed'):
        outfit(j, sp)
        j['_dressed'] = True
    return V.person(img, cam, x, y, scale_for(sp, s), dict(sp, full=True, pose='custom'), t, yaw, j, head_yaw)


# ------------------------------------------------------------------------------------------------ the cast sheet
FACES = {   # the faces each one needs (sheet labels)
    'patriot': [('rest', dict()), ('talking', dict(mouth='v:AI')), ('cross', dict(brows='fierce', lid=3)),
                ('scared', dict(brows='alarm'))],
    'gunner': [('set', dict()), ('firing', dict(brows='fierce', lid=4, mouth='v:etc')), ('shouting', dict(mouth='v:AI', brows='fierce'))],
    'loader': [('neutral', dict()), ('alarmed', dict(brows='alarm', mouth='v:O')), ('shouting', dict(mouth='v:AI', brows='alarm'))],
}


def sheet(out):
    """The Patriot, the Gunner and the Loader: every view (front, three-quarter, side, three-quarter back, back) on one
    floor line at their real heights with the body landmarks behind the front view, a 1.75 m person and a 1 m ruler;
    and each one's faces large."""
    import landmarks
    import sizes
    B.SS = 1
    W, H = 2900, 2560
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 40)
    small = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 24)
    d.text((30, 16), 'PATRIOTS 3: the Patriot (rebuilt to the current rules), the Gunner and the Loader', font=big, fill=(30, 30, 30))
    cam = B.Cam(1.0, 540, 960)
    cam.P = lambda x, y: (x, y)
    cam.S = lambda v: v
    s = 0.6
    names = ('front', 'three-quarter', 'side', '3/4 back', 'back')
    for r, key in enumerate(('patriot', 'gunner', 'loader')):
        sp = CAST[key]
        y0 = 80 + r * 820
        floor = 770
        for i, yaw in enumerate((0, 45, 90, 135, 180)):
            lay = Image.new('RGBA', (360, 800), (0, 0, 0, 0))
            s2 = scale_for(sp, s)
            if i == 0:
                landmarks.draw(ImageDraw.Draw(lay), 180, floor - 928 * s2, s2, 340)
            person(lay, cam, 180, floor - 928 * s2, s, dict(sp), 0.0, yaw)
            img.alpha_composite(lay, (20 + 362 * i, y0))
            d.text((200 + 362 * i, y0 + 790), names[i], font=small, fill=(40, 40, 40), anchor='mm')
        lay = Image.new('RGBA', (200, 800), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        sizes.scale_ref(ld, 100, floor, s / V.M_PER_UNIT)
        img.alpha_composite(lay, (1830, y0))
        d.text((1930, y0 + 790), f"{sp['name']} {HEIGHTS[sp['name']]:.2f} m", font=small, fill=(40, 40, 40), anchor='mm')
        faces = FACES[key]
        fw = 820 // len(faces)
        for i, (label, extra) in enumerate(faces):
            lay = Image.new('RGBA', (fw, 420), (0, 0, 0, 0))
            q = dict(sp, **extra)
            person(lay, cam, fw / 2, 330, 1.2, q, 0.0, 0)
            img.alpha_composite(lay, (2050 + fw * i, y0 + 160))
            d.text((2050 + fw * i + fw / 2, y0 + 600), label, font=small, fill=(40, 40, 40), anchor='mm')
    img.convert('RGB').save(out, quality=90)
    return out


cast_sheet = sheet                                       # the kit catalogue's name for it


def LINE_SUBJECTS():
    """Each of the cast alone, large, for the line-work check (linecheck.py)."""
    def one(sp):
        def draw(im):
            person(im, B.Cam(1.0, 540, 960), 540, 420, 1.3, dict(sp), 0.0, 0)
        return draw
    return [(k, one(sp)) for k, sp in CAST.items()]


# ------------------------------------------------------------------------------------------------ the world
# The crew stand in one small world in metres: X across (right +), Y up from the floor, Z forward (out of the slit,
# towards the beach). Everyone faces +Z. A body point (person units, y down from the neck base) maps to it through
# that person's own size (k metres per unit: a 1.75 m person is views.M_PER_UNIT).
class Spot:
    """Where a person stands: X, Z in metres; their height sets their unit size."""
    def __init__(self, sp, X, Z):
        self.sp, self.X, self.Z = sp, X, Z
        self.k = M * HEIGHTS.get(sp.get('name'), 1.75) / 1.75

    def to_body(self, P):
        X, Y, Z = P
        return ((X - self.X) / self.k, 928.0 - Y / self.k, (Z - self.Z) / self.k)

    def to_world(self, b):
        return (self.X + b[0] * self.k, (928.0 - b[1]) * self.k, self.Z + b[2] * self.k)

    def unlean(self, P, lean):
        """A world point as a hand target for arm_to (the body frame before the pose's lean)."""
        return V.leaned(self.to_body(P), -lean)


def _v(*a):
    return np.asarray(a, float)


def _unit(v):
    v = np.asarray(v, float)
    return v / (np.linalg.norm(v) or 1.0)


class Gun:
    """The MG42 placed in the world: `butt` (the butt plate's centre on the bore line), `aim` (unit, world).
    gun(u, v, s): a point u metres along from the butt, v up, s to its right, in world metres."""
    LENGTH = 1.22

    def __init__(self, butt, aim, recoil=0.0):
        self.a = _unit(aim)
        up = _v(0, 1, 0)
        self.w = _unit(up - self.a * float(self.a @ up))
        self.r = np.cross(self.w, self.a)
        self.o = _v(*butt) - self.a * recoil

    def __call__(self, u, v=0.0, s=0.0):
        return tuple(self.o + self.a * u + self.w * v + self.r * s)


GUN_C, GUN_D, GUN_L = (58, 60, 64), (34, 36, 40), (92, 96, 104)
BAKELITE, GRIP_C = (66, 46, 38), (122, 62, 44)
BRASS, BRASS_D, COPPER = (214, 170, 76), (166, 124, 44), (176, 104, 66)
BOX_C = (88, 92, 72)

# The MG42's parts (refs mg42-5, -6): (name, (u0, v0), (u1, v1), half width, half height at each end, kind, colour).
# u along the bore from the butt plate, v up from the bore line, metres (real: 1.22 m long, the jacket 6 cm across).
MG42_PARTS = [
    ('stock', (0.0, -0.018), (0.29, 0.0), 0.021, (0.068, 0.036), 'box', BAKELITE),
    ('grip', (0.405, -0.05), (0.355, -0.165), 0.017, (0.022, 0.02), 'box', GRIP_C),
    ('receiver', (0.29, 0.0), (0.64, 0.0), 0.03, (0.047, 0.047), 'box', GUN_C),
    ('cover', (0.34, 0.052), (0.6, 0.052), 0.027, (0.016, 0.016), 'box', GUN_D),
    ('jacket', (0.64, 0.0), (1.12, 0.0), 0.029, (0.029, 0.029), 'cyl', GUN_C),
    ('booster', (1.12, 0.0), (1.22, 0.0), 0.022, (0.022, 0.018), 'cyl', GUN_D),
    ('front sight', (1.09, 0.03), (1.09, 0.072), 0.004, (0.01, 0.006), 'box', GUN_D),
    ('rear sight', (0.52, 0.068), (0.52, 0.086), 0.012, (0.012, 0.008), 'box', GUN_D),
    ('guard', (0.43, -0.05), (0.43, -0.09), 0.01, (0.03, 0.03), 'box', GUN_D),
]


def _section(g, c, d, hw, hh, kind):
    """The outline of a part's cross-section at centre c (world), the part running along d (a world direction in
    the gun's u-v plane)."""
    n = _unit(np.cross(d, g.r))                     # in the u-v plane, at right angles to the part
    if (n @ g.w) < 0:
        n = -n
    if kind == 'cyl':
        return [tuple(c + n * hh * math.cos(q) + g.r * hw * math.sin(q)) for q in np.linspace(0, 2 * math.pi, 14, endpoint=False)]
    return [tuple(c + n * hh * a + g.r * hw * b) for a, b in ((1, 1), (1, -1), (-1, -1), (-1, 1))]


def _hull2(pts):
    return V._hull(pts)


def mg42_solids(g):
    """Each part as (name, colour, two section outlines in world metres, centre)."""
    out = []
    for name, (u0, v0), (u1, v1), hw, (h0, h1), kind, col in MG42_PARTS:
        c0, c1 = _v(*g(u0, v0)), _v(*g(u1, v1))
        d = _unit(c1 - c0)
        out.append((name, col, _section(g, c0, d, hw, h0, kind) + _section(g, c1, d, hw, h1, kind), (c0 + c1) / 2, kind))
    return out


def _bipod(g, spread=0.13):
    """The bipod: hinged under the jacket near the muzzle, its two legs splayed down to the sill."""
    hinge = _v(*g(1.0, -0.03))
    feet = []
    for sg in (-1, 1):
        foot = hinge + g.w * -0.27 + g.a * 0.05 + g.r * sg * spread
        feet.append((hinge, foot))
    return feet


def draw_mg42(p, to_body, yaw, g, flash=0.0, seed=0, rec=None):
    """The MG42 drawn through a person's frame (to_body: world -> their body units; yaw: the view's degrees): each part
    a solid (the hull of its two cross-sections), far parts first; the vents on the side we see; the bipod."""
    def P(w):
        return V.project(to_body(w), yaw)
    parts = []
    for name, col, ring, centre, kind in mg42_solids(g):
        pts, deps = zip(*(P(q) for q in ring))
        parts.append((sum(deps) / len(deps), name, col, list(pts), centre, kind))
    for hinge, foot in _bipod(g):                   # the legs as thin solids
        ring = _section(g, hinge, _unit(foot - hinge), 0.008, 0.008, 'cyl') + _section(g, foot, _unit(foot - hinge), 0.008, 0.008, 'cyl')
        pts, deps = zip(*(P(q) for q in ring))
        parts.append((sum(deps) / len(deps), 'bipod', GUN_D, list(pts), (hinge + foot) / 2, 'cyl'))
    parts.sort(key=lambda q: q[0])
    for dep, name, col, pts, centre, kind in parts:
        hull = _hull2(pts)
        if len(hull) < 3:
            continue
        p.poly(hull, col, INK, 2.0)
        if name == 'jacket':
            _vents(p, P, g)
    tip = P(g(1.225))[0]
    base = P(g(0.9))[0]
    if rec is not None:
        rec['muzzle'] = tip
    if flash > 0:
        dx, dy = tip[0] - base[0], tip[1] - base[1]
        n = math.hypot(dx, dy)
        end_on = n < 0.4 * 0.325 / M          # the last 32 cm of the gun under 40% of its length: pointing at us
        d = (dx / n, dy / n) if n > 1e-6 else (0.0, -1.0)
        PC.muzzle_flash(p, tip, d, 0.2 / M * flash, end_on, seed)


def _vents(p, P, g):
    """The oval cooling slots along the jacket, on the side facing the camera (dark: the barrel shows through)."""
    # find the side of the jacket nearest the camera: the depth of points round it
    best, best_dep = None, -1e9
    for q in np.linspace(0, 2 * math.pi, 12, endpoint=False):
        dirn = g.w * math.cos(q) + g.r * math.sin(q)
        dep = P(tuple(_v(*g(0.9)) + dirn * 0.029))[1]
        if dep > best_dep:
            best, best_dep = dirn, dep
    axis_len = abs(P(g(1.12))[0][0] - P(g(0.64))[0][0]) + abs(P(g(1.12))[0][1] - P(g(0.64))[0][1])
    if axis_len < 60:                               # nearly end on: the slots are not seen
        return
    other = np.cross(best, g.a)
    for k in range(7):
        u = 0.68 + k * 0.062
        pts = []
        for q in np.linspace(0, 2 * math.pi, 10, endpoint=False):
            pt = _v(*g(u)) + best * 0.0295 + g.a * 0.022 * math.cos(q) + other * 0.011 * math.sin(q)
            pts.append(P(tuple(pt))[0])
        p.poly(pts, (22, 22, 24), None)


def belt_path(points, n=40):
    """A smooth sagging path through world points (a Catmull-Rom curve, open)."""
    P = [np.asarray(q, float) for q in points]
    if len(P) == 2:
        P = [P[0], P[0] + (P[1] - P[0]) * 0.5 + _v(0, -0.05, 0), P[1]]
    out = []
    for i in range(len(P) - 1):
        p0, p1, p2, p3 = P[max(0, i - 1)], P[i], P[i + 1], P[min(len(P) - 1, i + 2)]
        for u in np.linspace(0, 1, n // (len(P) - 1), endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3))
    out.append(P[-1])
    return out


def draw_belt(p, to_body, yaw, path, along, phase=0.0, step=0.032):
    """The ammo belt: black links along the path, a brass round at each link (bullet forward along `along`, the gun's
    bore), drawn far rounds first. `phase` (metres) runs the rounds along towards the gun as it fires."""
    def P(w):
        return V.project(to_body(w), yaw)
    pts = [P(tuple(q))[0] for q in path]
    p.line(pts, (30, 30, 32), 3.0)
    seg = [np.linalg.norm(path[i + 1] - path[i]) for i in range(len(path) - 1)]
    total = sum(seg)
    rounds = []
    dist = (phase % step)
    while dist < total:
        acc, i = 0.0, 0
        while i < len(seg) - 1 and acc + seg[i] < dist:
            acc += seg[i]
            i += 1
        u = (dist - acc) / (seg[i] or 1)
        c = path[i] + (path[i + 1] - path[i]) * u
        a = _unit(along)
        back, tip, nose = c - a * 0.034, c + a * 0.024, c + a * 0.046
        (b2, db), (t2, dt), (n2, dn) = P(tuple(back)), P(tuple(tip)), P(tuple(nose))
        rounds.append(((db + dn) / 2, b2, t2, n2))
        dist += step
    rounds.sort(key=lambda r: r[0])
    for _, b2, t2, n2 in rounds:
        dx, dy = t2[0] - b2[0], t2[1] - b2[1]
        n = math.hypot(dx, dy)
        if n < 4:                                    # end on: a brass disc
            p.ell(b2[0], b2[1], 6, 6, BRASS, INK, 1.0)
            continue
        nx, ny = -dy / n * 6, dx / n * 6
        p.poly([(b2[0] + nx, b2[1] + ny), (t2[0] + nx, t2[1] + ny), (t2[0] - nx, t2[1] - ny), (b2[0] - nx, b2[1] - ny)],
               BRASS, INK, 1.0)
        p.poly([(t2[0] + nx * 0.8, t2[1] + ny * 0.8), (n2[0], n2[1]), (t2[0] - nx * 0.8, t2[1] - ny * 0.8)], COPPER, INK, 1.0)


def draw_box(p, to_body, yaw, c, facing=0.0, lid=True):
    """The steel ammo box (Patronenkasten 34, olive, 27 x 10 x 19 cm), its centre-bottom at world c."""
    def P(w):
        return V.project(to_body(w), yaw)
    L, Wd, Hh = 0.27, 0.10, 0.19
    ca, sa = math.cos(facing), math.sin(facing)
    def at(x, y, z):
        return (c[0] + x * ca + z * sa, c[1] + y, c[2] - x * sa + z * ca)
    corners = [at(x, y, z) for x in (-L / 2, L / 2) for y in (0, Hh) for z in (-Wd / 2, Wd / 2)]
    pts = [P(q)[0] for q in corners]
    p.poly(curve(V._hull(pts), 1), BOX_C, INK, 2.0)
    top = [P(at(x, Hh, z))[0] for x, z in ((-L / 2, -Wd / 2), (L / 2, -Wd / 2), (L / 2, Wd / 2), (-L / 2, Wd / 2))]
    p.poly(top, B.lt(BOX_C, 1.15), INK, 1.6)
    h0, h1 = P(at(-0.06, Hh + 0.025, 0))[0], P(at(0.06, Hh + 0.025, 0))[0]
    p.line([P(at(-0.06, Hh, 0))[0], h0, h1, P(at(0.06, Hh, 0))[0]], B.dk(BOX_C, 0.6), 2.6)


def cases(p, to_body, yaw, g, t, rate=20.0, life=0.4):
    """Spent cases falling from under the receiver while it fires: one every 1/rate s, each falling under gravity
    with its own small kick to the right and a tumble (`t`: seconds since the burst began)."""
    def P(w):
        return V.project(to_body(w), yaw)
    port = _v(*g(0.47, -0.05))
    k0 = max(0, int((t - life) * rate))
    for k in range(k0, int(t * rate) + 1):
        dt = t - k / rate
        if dt < 0 or dt > life:
            continue
        rng = np.random.default_rng(1000 + k)
        vel = g.r * rng.uniform(0.3, 0.7) + g.a * rng.uniform(-0.2, 0.1) + _v(0, rng.uniform(-0.3, 0.2), 0)
        c = port + vel * dt + _v(0, -4.9 * dt * dt, 0)
        ang = rng.uniform(0, math.pi) + dt * 30
        d = _unit(g.a * math.cos(ang) + _v(0, 1, 0) * math.sin(ang))
        a2, b2 = P(tuple(c - d * 0.028))[0], P(tuple(c + d * 0.028))[0]
        p.line([a2, b2], BRASS_D, 9.0)
        p.line([a2, b2], BRASS, 6.0)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    else:
        print(__doc__)
