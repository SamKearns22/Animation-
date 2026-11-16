#!/usr/bin/env python3
"""MAP  The people kit's hats (craft change 1, 16 Nov): a knitted beanie and a baseball cap, LIFTED from European
Protests, Ranked (protest_tiers_cast.py, O7) unchanged in look, so any crowd made from the kit can wear them. A crowd
member's hat is sp['kit_hat'] ('beanie' or 'cap'), its colour sp['hat_c'] = (colour, darker); people.install hangs
draw() on views.HEAD_WEAR, which draws it over the head in every view. A film that dresses its own heads
(sp['headwear'], EPR's) is left alone.

Map: head box 20 | beanie 45 | cap 66 | draw 100
"""
import numpy as np
from PIL import Image

import people_parts as PP
from ed import INK, curve

B = PP.B
V = PP.AV.MC.V
_BOX = {}
_VIEW_YAW = {'front': 0, 'three': 45, 'side': 90, 'three_back': 135, 'back': 180}
_DK = lambda c, k=.72: tuple(int(v * k) for v in c)                                   # noqa: E731


def head_box(sp, view):
    """(left, right, top) of the bare head as drawn in this view, in person units from the head centre (measured once)."""
    key = (sp.get('who'), sp.get('hw'), sp.get('hh'), sp.get('head_dy'), sp.get('kit_face', {}).get('hair'), view)
    if key not in _BOX:
        ss, B.SS = B.SS, 1
        img = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
        cam = B.Cam(1.0, 540, 960)
        bare = dict(sp, force=None, kit_hat=None)
        j = V.standing(bare)
        j['_dressed'] = True
        V.person(img, cam, 540, 700, 1.0, dict(bare, full=True, pose='custom'), 0.0, _VIEW_YAW[view], j)
        B.SS = ss
        m = (np.abs(np.asarray(img.convert('RGB')).astype(int) - 255).sum(2) > 20)
        hy = int(700 - 150 + sp.get('head_dy', 10))
        top = int(np.nonzero(m[:hy].any(1))[0].min())
        xs = np.nonzero(m[top:hy + 40].any(0))[0]
        _BOX[key] = (float(xs.min() - 540), float(xs.max() - 540), float(top - hy))
    return _BOX[key]


def beanie(p, view, sp, hx, hy):
    """A knitted beanie pulled down to the brow, a turned-up cuff; colour sp['hat_c']."""
    col, dk = sp.get('hat_c', ((24, 24, 26), (16, 16, 18)))
    l, r, t = head_box(sp, view)
    H = -t
    top, brow = hy + t - 0.07 * H, hy + t + 0.6 * H
    w = r - l
    o = 0.06 * w if view == 'three' else -0.06 * w if view == 'three_back' else 0.0
    dome = [(hx + l - 7, brow + 4), (hx + l - 9, top + 0.42 * H), (hx + l + 0.16 * w, top + 0.07 * H),
            (hx + (l + r) / 2 + o, top), (hx + r - 0.16 * w, top + 0.07 * H), (hx + r + 9, top + 0.42 * H),
            (hx + r + 7, brow + 4)]
    p.poly(curve(dome, 3), col, INK, 2.4)
    cuff = [(hx + l - 9, brow - 0.2 * H), (hx + r + 9, brow - 0.2 * H), (hx + r + 8, brow + 6), (hx + l - 8, brow + 6)]
    p.poly(cuff, dk, INK, 2.2)
    for k in range(1, 7):                           # the rib knit on the cuff
        x = hx + l - 6 + k * (w + 12) / 7
        p.line([(x, brow - 0.17 * H), (x, brow + 3)], _DK(dk, .75), 1.4)


def cap(p, view, sp, hx, hy):
    """A baseball cap in sp['hat_c']: a round crown, the peak forward (side: out over the brow; back: the strap gap)."""
    col, dk = sp.get('hat_c', ((24, 24, 26), (16, 16, 18)))
    l, r, t = head_box(sp, view)
    H, w = -t, r - l
    top, brow = hy + t - 0.05 * H, hy + t + 0.55 * H
    if view == 'side':
        crown = [(hx + l - 6, brow + 4), (hx + l - 8, top + 0.4 * H), (hx + (l + r) / 2 - 6, top),
                 (hx + r + 4, top + 0.4 * H), (hx + r + 6, brow)]
        p.poly(curve(crown, 3), col, INK, 2.4)
        p.poly([(hx + r - 10, brow - 8), (hx + r + 0.42 * w, brow + 2), (hx + r + 0.4 * w, brow + 12),
                (hx + r - 6, brow + 8)], dk, INK, 2.2)
        return
    crown = [(hx + l - 7, brow + 4), (hx + l - 9, top + 0.42 * H), (hx + l + 0.16 * w, top + 0.07 * H), (hx, top),
             (hx + r - 0.16 * w, top + 0.07 * H), (hx + r + 9, top + 0.42 * H), (hx + r + 7, brow + 4)]
    p.poly(curve(crown, 3), col, INK, 2.4)
    if view in ('back', 'three_back'):
        p.poly([(hx - 0.1 * w, brow - 0.16 * H), (hx + 0.1 * w, brow - 0.16 * H), (hx + 0.08 * w, brow + 2),
                (hx - 0.08 * w, brow + 2)], (236, 228, 214), INK, 1.4)
        return
    o = 0.12 * w if view == 'three' else 0.0
    for k in (-0.2, 0.2):                           # the crown's seams
        p.line([(hx + k * 0.3 * w + o * .3, top + 0.04 * H), (hx + k * w + o * .3, brow - 2)], dk, 1.8)
    peak = [(hx + l + 0.06 * w + o, brow), (hx + r - 0.06 * w + o, brow), (hx + r + 0.08 * w + o, brow + 0.14 * H),
            (hx + o, brow + 0.22 * H), (hx + l - 0.08 * w + o, brow + 0.14 * H)]
    p.poly(curve(peak, 2), dk, INK, 2.2)


def draw(p, view, sp, hx, hy):
    """views.HEAD_WEAR: the kit's hat on a crowd member who has one (never over a film's own headwear)."""
    hat = sp.get('kit_hat')
    if hat and not sp.get('headwear'):
        (beanie if hat == 'beanie' else cap)(p, view, sp, hx, hy)
