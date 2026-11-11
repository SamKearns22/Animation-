#!/usr/bin/env python3
"""MAP  Blessed (Sam, 11 Nov): the cast. Brand is a measured likeness head (likeness.py card on b01-b04,
references/blessed/likeness/) on the patriots4 face layout, built the Ad-Vanced Notice (Vance) way.

    BRAND     Russell Brand (card, 11 Nov): close-set eyes (84th centile), a long narrow face (77th), a narrow
              forehead (76th), a wide nose (73rd); the card's "short nose" is unsure and by eye his nose is long and
              straight (trust the eye). Deep-set dark eyes under heavy dark brows. A full beard: dark brown at the
              moustache and round the mouth, grey-white at the chin and along the jaw. Long dark-brown curls past the
              shoulders with grey streaks, off a high hairline. 1.83 m. Three looks (Sam's answer 7):
                trial   (arrival, gates) grey jacket, open white shirt, crucifix, long white scarf, hair loose, aviators
                stand   (the witness box, sentencing) dark suit, open white shirt; hair loose (stand) or topknot (dock)
                prison  grey tracksuit, hair in the topknot from the sentencing sketch
    JUDGE     invented (Sam's answer 4): red robe, white wig, white bands, half-moon glasses; chest up at the bench.
    OFFICER   prison officer: white shirt, black epaulettes and tie, black trousers, keys on the belt.
    NEWSREADER  the BBC-style presenter on the TV (newsdesk_cast's presenter, restyled: navy suit, red tie).

    python3 source/blessed_cast.py sheet OUT.jpg       front, side, back of the cast, a 1.75 m person
    python3 source/blessed_cast.py faces OUT.jpg       Brand's face large in every mood and look, his photos beside
    python3 source/blessed_cast.py head brand OUT.png  his head straight on (for likeness.py check)
    python3 source/blessed_cast.py turn OUT.jpg        his head all the way round, three moods

Map: colours 40 | measures 62 | moods 72 | beard 95 | hair 160 | extras 250 | head 300 | turned 370 | torsos 400 |
     people 470 | sheets 520
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ad_vanced_notice_cast as AV     # noqa: E402  (installs midterminal's hooks, turnhead, the Vance helpers)
import json  # noqa: E402
from midterminal_cast import B, TC, P4, V, dk, blend, FONT  # noqa: E402
from ed import INK, curve, oval  # noqa: E402
import turnhead as TH  # noqa: E402
MC = AV.MC

# ---------------------------------------------------------------------------------------------- colours
BR_SKIN = (232, 176, 150)         # card: light (238, 175, 149)
BR_HAIR = (80, 62, 48)            # dark brown curls (lighter after critique pass 2)
BR_HAIR_L = (112, 90, 72)         # the light on the curls
BR_GREY = (156, 146, 136)         # the grey streaks
BR_BROW = (48, 38, 32)
BR_IRIS = (86, 62, 42)            # dark brown
BR_LIP = (196, 128, 116)
BD_MOUST = (74, 58, 48)           # the beard: dark at the moustache and round the mouth
BD_MID = (140, 128, 118)          # grey-brown on the cheeks
BD_LOW = (206, 200, 192)          # grey-white at the chin and along the jaw
BD_GRAIN = (226, 222, 216)
GREY_JKT = (86, 88, 94)
DARK_SUIT = (38, 38, 46)
SCARF = (244, 242, 236)
TRACK = (134, 136, 140)
GOLD = (206, 166, 70)
SHADES = (28, 30, 36)

# ---------------------------------------------------------------------------------------------- measures (11 Nov)
_card = json.load(open(os.path.join(HERE, '..', 'references', 'blessed', 'likeness', 'brand-card.json')))
_BM, _BA = _card['measures'], _card['average']
P4.MEASURED['brand'] = {k: P4.AVG[k] + _BM[k] - _BA[k] for k in P4.AVG}
P4.PUSH['brand'] = 1.6
P4.TUNE['brand'] = dict(eyes_apart=2.0, nose_wide=2.0, brow_slope=3.0, brow_high=3.0, eye_tilt=8.0, chin_long=4.0,
                        forehead_wide=4.0, eye_open=3.0, jaw_wide=25.0, nose_long=5.0)   # 11 Nov, likeness check rounds

# ---------------------------------------------------------------------------------------------- moods
# brow: up (+); frown (+) pulls the inner ends down, (-) lifts them (worry); lid: upper lid down; mouth: his shapes
MOODS = {'neutral': dict(brow=0.0, frown=0.0, lid=0.16, squint=0.0, mouth='lips', smile=0.2),
         # the sincere showman (Sam's answer 8): believes his own performance; beaming, brows up, crinkled eyes
         'showman': dict(brow=0.03, frown=-0.01, lid=0.14, squint=0.45, mouth='grin'),
         'sincere': dict(brow=0.02, frown=-0.03, lid=0.12, squint=0.1, mouth='lips', smile=0.5),
         # the stiff showman in the box: bolt upright, eyes up on "Almighty God", too loud
         'oath': dict(brow=0.04, frown=0.0, lid=0.0, squint=0.0, mouth='lips', smile=0.0, gaze_dy=-0.6),
         # sentenced: the stillness cracks (Sam's answer 9: quiet, to himself, deadpan); hollow, eyes down
         'hollow': dict(brow=0.006, frown=-0.04, lid=0.34, squint=0.0, mouth='lips', smile=-0.6, gaze_dy=0.6),
         'numb': dict(brow=0.0, frown=-0.01, lid=0.3, squint=0.0, mouth='lips', smile=-0.3),
         'weeping': dict(brow=0.01, frown=-0.07, lid=0.3, squint=0.5, mouth='cry', tears=True),
         'dejected': dict(brow=0.004, frown=-0.05, lid=0.28, squint=0.15, mouth='lips', smile=-0.8, tears=True),
         'stern': dict(brow=-0.02, frown=0.05, lid=0.22, squint=0.1, mouth='lips', smile=-0.4),   # the judge's bang
         'amazed': dict(brow=0.06, frown=0.0, lid=0.0, squint=0.0, mouth='gasp'),
         'overjoyed': dict(brow=0.05, frown=-0.01, lid=0.1, squint=0.5, mouth='grin')}

# ---------------------------------------------------------------------------------------------- the beard
# (by eye on b01-b03, b07): full and fairly short, past the chin; dark brown at the moustache, which runs down past
# the mouth corners and joins a dark patch under the lower lip; grey-white over the chin and along the jaw; grey-brown
# on the cheeks; the cheek line high and soft. Every edge facing skin is a row of small tufts (AV.tufts).


def brand_beard(p, f, L, skin, seed=91):
    rng = np.random.default_rng(seed)
    fw, jw, ny, l0, l13, l17, mw, nw = L['fw'], L['jw'], L['nose_y'], L['lip0'], L['lip13'], L['lip17'], L['mw'], L['nw']
    wrap = getattr(f, 'wrap', None)
    nb = [(wrap(0.44, -95), 0.44), (wrap(0.62, -98), 0.62), (wrap(0.83, -96), 0.83)] if wrap else \
        [(-fw * 0.5 - 0.004, 0.44), (-fw * 0.5 - 0.004, 0.62), (-jw * 0.46, 0.84)]
    cb = 0.015 if wrap else 0.0                        # turned: past the chin outline, so no skin flecks under it
    bottom = nb + [(-jw * 0.32, 0.97 + cb), (-0.12, 1.02 + cb), (0.0, 1.035 + cb), (0.12, 1.02 + cb), (jw * 0.32, 0.97 + cb), (jw * 0.46, 0.84),
                   (fw * 0.5 + 0.004, 0.62), (fw * 0.5 + 0.004, 0.44)]
    cheek = [(fw * 0.5 - 0.015, 0.47), (fw * 0.41, ny - 0.01), (fw * 0.3, ny + 0.01), (mw * 0.7, l0 - 0.015)]
    corner = [(mw * 0.64, l13 + 0.01), (mw * 0.58, l17 + 0.02), (mw * 0.3, l17 + 0.04)]
    right = cheek + corner + [(0.0, l17 + 0.045)]
    left = [(-u, v) for u, v in right[::-1]]
    if wrap:
        left[-1] = (wrap(0.42, -90), 0.4)
    # turned (oath, phone, gates) the far half narrows and the tufts turn into stair steps (Sam, 11 Nov: "ridges on
    # the left side"): smaller tufts the more he turns
    turned = abs(getattr(f, 's', 0.0)) if hasattr(f, 'th') else (getattr(f, 'tq', 0.0) or 0.0)   # TurnFace: sin(yaw)
    ta = 1.0 - 0.6 * min(1.0, turned)
    inner = AV.tufts(right + left[1:], 0.012 * ta, 0.014, out=1.0, seed=seed)
    edge = AV.tufts(bottom, 0.012 * ta, 0.018, out=1.0, seed=seed + 1)
    body = f.pts(edge + inner)
    p.poly(body, BD_MID, None)
    # grey-white over the chin and the jaw: everything below a tufted line from the jaw corner under the mouth
    low_top = AV.tufts([(fw * 0.5 + 0.01, 0.66), (jw * 0.42, 0.8), (mw * 0.5, l17 + 0.08), (0.0, l17 + 0.1),
                        (-mw * 0.5, l17 + 0.08), (-jw * 0.42, 0.8), (-fw * 0.5 - 0.01, 0.66)], 0.016 * ta, 0.016,
                       out=1.0, seed=seed + 2)
    n = len(edge)
    p.poly(f.pts(edge[n // 5: n - n // 5] + low_top), BD_LOW, None)
    # the dark moustache: from under the nose, over the lip, down past the corners (a horseshoe) to the chin patch
    mt = max(ny + 0.03, l0 - 0.06)                       # a band over the lip (b10), not the whole philtrum
    top = AV.tufts([(-mw * 0.7, l13 + 0.02), (-mw * 0.6, mt + 0.01), (-nw * 0.5, mt), (0.0, mt + 0.006),
                    (nw * 0.5, mt), (mw * 0.6, mt + 0.01), (mw * 0.7, l13 + 0.02)], 0.008, 0.013, out=1.0,
                   seed=seed + 3)
    down = [(mw * 0.62, l13 + 0.012), (mw * 0.12, l17 - 0.004), (mw * 0.08, l17 + 0.03), (0.0, l17 + 0.045),
            (-mw * 0.08, l17 + 0.03), (-mw * 0.12, l17 - 0.004), (-mw * 0.62, l13 + 0.012)]   # the drooping ends, a soul patch
    must = f.pts(top + AV.tufts(down, 0.008, 0.014, out=-1.0, seed=seed + 4))
    p.poly(must, BD_MOUST, None)
    # the grain: short light strokes falling down and in over the grey parts (none in the dark horseshoe)
    for r, gv in enumerate(np.arange(0.5, 1.06, 0.04)):
        for gu in np.arange(-fw * 0.5 - (0.12 if wrap else 0.0) + (0.02 if r % 2 else 0.0), fw * 0.5, 0.04):
            u, v = gu + rng.uniform(-0.014, 0.014), gv + rng.uniform(-0.014, 0.014)
            q = f(u, v)
            if not AV._inside(body, q[0], q[1]) or AV._inside(must, q[0], q[1]) or (wrap and f.k(u, v) < 0.15):
                continue
            du, dv = -u * 0.5, 1.0
            nn = math.hypot(du, dv)
            ln = rng.uniform(0.018, 0.028)
            q2 = f(u + du / nn * ln, v + dv / nn * ln)
            light = v > 0.8 or abs(u) > jw * 0.5 - 0.03
            p.line([q, q2], BD_GRAIN if light else blend(BD_MID, BD_GRAIN, 0.45), 1.6)
    p.line(f.pts(edge), INK, 2.2)


# ---------------------------------------------------------------------------------------------- the hair
def curls(pts, amp, step, out=1.0, seed=0):
    """A curly edge: the polyline cut into bumps `step` long, each bulging `amp` to one side (out=+1 left of the
    travel direction): a row of round curls, not tufts."""
    rng = np.random.default_rng(seed)
    res = []
    for (u0, v0), (u1, v1) in zip(pts, pts[1:]):
        d = math.hypot(u1 - u0, v1 - v0)
        n = max(1, int(round(d / step)))
        nu, nv = -(v1 - v0) / (d + 1e-9), (u1 - u0) / (d + 1e-9)
        for k in range(n):
            a = amp * out * rng.uniform(0.6, 1.15)
            for t, h in ((0.0, 0.0), (0.2, 0.62), (0.5, 1.0), (0.8, 0.62)):
                tt = (k + t) / n
                res.append((u0 + (u1 - u0) * tt + nu * a * h, v0 + (v1 - v0) * tt + nv * a * h))
    res.append(pts[-1])
    return res


def waves(pts, amp, wl, out=1.0, seed=0, step=0.012):
    """A loose wavy edge (his curls are big waves, not ringlets): the polyline resampled every `step` and pushed
    sideways by two sines of random phase (wavelength about `wl`), the push growing along the line (the ends wavier)."""
    rng = np.random.default_rng(seed)
    ph1, ph2 = rng.uniform(0, 6.3, 2)
    dense = []
    for (u0, v0), (u1, v1) in zip(pts, pts[1:]):
        d = math.hypot(u1 - u0, v1 - v0)
        n = max(1, int(d / step))
        for k in range(n):
            dense.append((u0 + (u1 - u0) * k / n, v0 + (v1 - v0) * k / n))
    dense.append(pts[-1])
    res, s = [], 0.0
    for i, (u, v) in enumerate(dense):
        if i:
            s += math.hypot(u - dense[i - 1][0], v - dense[i - 1][1])
        j = min(i, len(dense) - 2)
        du, dv = dense[j + 1][0] - dense[j][0], dense[j + 1][1] - dense[j][1]
        dd = math.hypot(du, dv) + 1e-9
        nu, nv = -dv / dd, du / dd
        a = amp * out * (0.5 + 0.5 * i / len(dense)) * (math.sin(2 * math.pi * s / wl + ph1) +
                                                     0.45 * math.sin(2 * math.pi * s / (wl * 0.43) + ph2))
        res.append((u + nu * a, v + nv * a))
    return res


def brand_hair(L, knot=False, seed=3):
    """His hair (face fractions). Loose (b01-b07): a high hairline, swept back off the forehead, flat-ish on top, then
    big loose waves either side of the face, widest round the ears and jaw, on down past the shoulders (v 1.85), the
    ends in separate locks. Returns (cap, mass, locks): cap over the forehead; mass the whole shape behind the face;
    locks a wavy lock over each cheek's edge (hiding the ears). Topknot (b08): pulled back tight; no mass or locks."""
    fw, fhw = L['fw'], L['fhw']
    c = fhw * 0.5
    hl = -0.17                                                   # a high hairline (Sam's photo b10: a tall forehead)
    if knot:
        e = fw * 0.5                             # pulled back flat over a round skull, out to the ears
        cap = [(-e - 0.01, 0.3), (-e - 0.03, 0.02), (-e + 0.04, -0.22), (-0.24, -0.38), (0.0, -0.42), (0.24, -0.38),
               (e - 0.04, -0.22), (e + 0.03, 0.02), (e + 0.01, 0.3), (e - 0.03, 0.3), (c + 0.02, 0.1), (c - 0.02, 0.2), (c * 0.8, 0.0), (c * 0.5, hl),
               (0.0, hl - 0.02), (-c * 0.5, hl), (-c * 0.8, 0.0), (-c + 0.02, 0.2), (-c - 0.02, 0.1), (-e + 0.03, 0.3)]
        return cap, [], []
    e = fw * 0.5

    def side(sgn, sd):
        outer = [(sgn * 0.02, -0.4), (sgn * (c + 0.04), -0.36), (sgn * (e + 0.14), -0.1), (sgn * (e + 0.22), 0.3),
                 (sgn * (e + 0.26), 0.8), (sgn * (e + 0.25), 1.2), (sgn * (e + 0.2), 1.5)]
        ends = []                                                # the ends: four locks of different lengths
        for k, (du, dv) in enumerate(((0.2, 1.5), (0.16, 1.62), (0.11, 1.53), (0.07, 1.6), (0.03, 1.48))):
            u = sgn * (e + du)
            ends += [(u, dv), (u - sgn * 0.03, dv - 0.08)] if k % 2 == 0 else [(u + sgn * 0.01, dv - 0.02), (u, dv)]
        inner = [(sgn * (e + 0.01), 1.4), (sgn * (e - 0.02), 1.05), (sgn * (e - 0.05), 0.7)]
        return waves(outer, 0.03, 0.34, out=-sgn, seed=sd) + ends + waves(inner, 0.02, 0.3, out=sgn, seed=sd + 1)
    right, left = side(1, seed), side(-1, seed + 10)
    mass = left[::-1] + [(-0.05, 0.2), (0.05, 0.2)] + right
    cap = waves([(-c - 0.1, 0.06), (-c - 0.02, -0.26), (-0.22, -0.44), (0.0, -0.49), (0.22, -0.44), (c + 0.02, -0.26),
                 (c + 0.1, 0.06)], 0.012, 0.2, out=1.0, seed=seed + 4)
    cap += [(c - 0.02, 0.04), (c * 0.86, -0.12), (c * 0.5, hl), (0.12, hl - 0.03), (0.0, hl - 0.015), (-0.12, hl - 0.03),
            (-c * 0.5, hl), (-c * 0.86, -0.12), (-c + 0.02, 0.04)]
    locks = []
    for sgn in (-1, 1):                                          # a lock over the face's edge, temple to below the jaw
        inner = waves([(sgn * c, 0.04), (sgn * (e - 0.04), 0.3), (sgn * (e - 0.045), 0.62), (sgn * (e - 0.01), 0.9)],
                      0.014, 0.22, out=sgn, seed=seed + 5 + sgn)
        tip = [(sgn * (e + 0.03), 1.08)]
        outer = [(sgn * (e + 0.13), 0.8), (sgn * (e + 0.16), 0.4), (sgn * (c + 0.14), 0.0)]
        locks.append((sgn, inner + tip + outer))
    return cap, mass, locks


def _texture(p, f, poly_uv, n, seed, length=0.2):
    """Wave strands inside a hair shape: short S-curves falling down the hair, light and grey (his grey streaks)."""
    rng = np.random.default_rng(seed)
    q = f.pts(poly_uv)
    us, vs = [a for a, _ in poly_uv], [b for _, b in poly_uv]
    k = 0
    for _ in range(n * 10):
        if k >= n:
            break
        u, v = rng.uniform(min(us), max(us)), rng.uniform(min(vs), max(vs))
        ln = length * rng.uniform(0.6, 1.2)
        ends = (f(u, v), f(u, v + ln))
        if not (AV._inside(q, *ends[0]) and AV._inside(q, *ends[1])):
            continue
        k += 1
        sw = rng.choice((-1, 1)) * 0.025
        pts = [(u, v), (u + sw, v + ln * 0.33), (u - sw, v + ln * 0.66), (u + sw * 0.5, v + ln)]
        p.line(curve(f.pts(pts), 3), BR_GREY if rng.uniform() < 0.35 else BR_HAIR_L, 1.8)


def _top_strokes(p, f, L, knot):
    c = L['fhw'] * 0.5
    if knot:                                          # pulled back: a few lines sweeping back to the bun, low
        for a, b in (((-0.14, -0.2), (-0.06, -0.38)), ((0.14, -0.2), (0.06, -0.38))):
            p.line(curve(f.pts([a, ((a[0] + b[0]) / 2 * 1.2, (a[1] + b[1]) / 2), b]), 3), BR_HAIR_L, 1.6)
        return
    strokes = (((-0.08, -0.21), (-0.2, -0.4)), ((0.08, -0.21), (0.2, -0.4)), ((-0.22, -0.17), (-c - 0.04, -0.3)),
               ((0.22, -0.17), (c + 0.04, -0.3)), ((0.0, -0.22), (0.0, -0.44)))
    for i, (a, b) in enumerate(strokes):
        if i == 2 and f.tq > 0.4:                     # the far side narrows: its outer stroke would leave the hair
            continue
        mid = ((a[0] + b[0]) / 2 + (0.03 if i % 2 else -0.03), (a[1] + b[1]) / 2)
        p.line(curve(f.pts([a, mid, b]), 3), BR_GREY if i == 1 else BR_HAIR_L, 1.8)


def bun(p, f, back=False):
    """The topknot on the crown (sketch b08): a round knot of curls, a band, a few ends."""
    x, y = f(0.0, -0.47)
    p.poly(curve(oval(x, y, 28, 24, 18), 2), BR_HAIR, INK, 2.4)
    for k in range(3):
        p.line(curve([(x - 22 + 14 * k, y - 18), (x - 14 + 14 * k, y - 4), (x - 20 + 14 * k, y + 12)], 3),
               BR_GREY if k == 1 else BR_HAIR_L, 1.8)
    p.line([(x - 14, y + 26), (x + 14, y + 26)], (30, 26, 24), 4.0)


def hair_back(p, sp, hx, hy, hw, hh):
    """Behind the head: the big curly mass down past the shoulders (loose), or just the bun (topknot)."""
    if sp.get('who') != 'brand':
        return _hair_back(p, sp, hx, hy, hw, hh)
    if sp.get('hair') == 'brand_knot':
        return
    pts = curls([(hx - hw - 30, hy - 40), (hx - hw - 70, hy + 120), (hx - hw - 66, hy + 300), (hx + hw + 66, hy + 300),
                 (hx + hw + 70, hy + 120), (hx + hw + 30, hy - 40), (hx, hy - hh - 30), (hx - hw - 30, hy - 40)],
                18, 46, out=1.0, seed=5)
    p.poly(pts, dk(BR_HAIR, 0.85), INK, 2.6)


# ---------------------------------------------------------------------------------------------- extras
def shades(p, f, L, lowered=False):
    """Aviator sunglasses (b06, b07, b09): two dark teardrop lenses in thin gold rims, a double bridge. Lowered
    (Sam's answer 8, "lowers the sunglasses"): slid down the nose, the eyes showing over the rims."""
    dv = 0.13 if lowered else 0.0
    for sgn in (-1, 1):
        cx, ey = sgn * L['ecx'], L['eye_y'] + 0.01 + dv
        w = L['ew'] * 0.9
        lens = [(cx - sgn * w * 0.95, ey - 0.055), (cx + sgn * w * 0.9, ey - 0.06), (cx + sgn * w * 1.05, ey - 0.02),
                (cx + sgn * w * 0.8, ey + 0.07), (cx + sgn * w * 0.05, ey + 0.085), (cx - sgn * w * 0.85, ey + 0.05),
                (cx - sgn * w * 1.0, ey - 0.01)]
        q = curve(f.pts(lens), 3)
        p.poly(q, SHADES, GOLD, 2.4)
        p.line(curve(f.pts([(cx - sgn * w * 0.4, ey - 0.03), (cx + sgn * w * 0.3, ey - 0.04)]), 2), (90, 96, 110), 2.0)
        p.line(f.pts([(cx + sgn * w * 1.0, ey - 0.04), (sgn * L['fw'] * 0.5, ey - 0.045)]), GOLD, 2.4)
    y = L['eye_y'] - 0.045 + dv
    p.line(f.pts([(-L['ecx'] + L['ew'] * 0.85, y), (L['ecx'] - L['ew'] * 0.85, y)]), GOLD, 2.4)
    p.line(curve(f.pts([(-L['ecx'] + L['ew'] * 0.9, y + 0.03), (0.0, y + 0.015), (L['ecx'] - L['ew'] * 0.9, y + 0.03)]),
                 3), GOLD, 2.0)


def tears(p, f, L):
    for sgn in (-1, 1):
        x, y = f(sgn * (L['ecx'] - L['ew'] * 0.1), L['eye_y'] + 0.04)
        p.line(curve([(x, y), (x + sgn * 2, y + 22), (x - sgn * 1, y + 44)], 3), (150, 196, 230), 3.2)
        p.poly(oval(x - sgn * 1, y + 48, 4, 6, 10), (170, 210, 236), INK, 1.0)


def deep_set(p, f, L, skin):
    """Deep-set eyes (b01-b03): a shadow under each brow, over the eye, and a soft bag line below."""
    sh = dk(skin, 0.86)
    for sgn in (-1, 1):
        cx, ey, w = sgn * L['ecx'], L['eye_y'], L['ew'] * 0.62
        pts = [(cx - w, ey - 0.02), (cx - w * 0.6, ey - 0.06), (cx + w * 0.4, ey - 0.065), (cx + w * 1.05, ey - 0.03),
               (cx + w * 0.7, ey - 0.01), (cx - w * 0.6, ey - 0.012)]
        p.poly(curve(f.pts(pts), 3), sh, None)
        p.line(curve(f.pts([(cx - w * 0.6, ey + 0.05), (cx, ey + 0.065), (cx + w * 0.7, ey + 0.045)]), 3),
               dk(skin, 0.74), 1.6)


def brand_mouth(p, f, L, kind):
    """'grin' (the showman's beam, top teeth), 'gasp' (amazed: an open O), 'cry' (open, corners pulled down)."""
    hw, l0, l13, l17 = L['mw'] / 2, L['lip0'], L['lip13'], L['lip17']
    if kind == 'grin':
        hw *= 1.15
        top = [(-hw, l13 - 0.03), (-hw * 0.5, l13 - 0.012), (0.0, l13 - 0.008), (hw * 0.5, l13 - 0.012), (hw, l13 - 0.03)]
        bot = [(hw, l13 - 0.03), (hw * 0.55, l17 + 0.018), (0.0, l17 + 0.036), (-hw * 0.55, l17 + 0.018)]
        p.poly(curve(f.pts(top + bot), 3), (70, 26, 30), INK, 2.2)
        teeth = [(-hw * 0.85, l13 - 0.022), (0.0, l13 - 0.006), (hw * 0.85, l13 - 0.022), (hw * 0.6, l13 + 0.016),
                 (0.0, l13 + 0.024), (-hw * 0.6, l13 + 0.016)]
        p.poly(curve(f.pts(teeth), 3), (250, 248, 240), None)
        return
    if kind == 'gasp':
        # a round O inside the moustache: a long narrow one hanging below it read as a tongue (critique, 11 Nov)
        x, y = f(0.0, (l13 + l17) / 2 - 0.004)
        rx, ry = hw * P4.H * 0.72, (l17 - l0) * P4.H * 0.72
        p.poly(oval(x, y, rx, ry, 24), (70, 26, 30), INK, 2.4)
        p.poly(oval(x, y + ry * 0.25, rx * 0.62, ry * 0.55, 20), (40, 14, 18), None)          # the dark throat
        p.poly(oval(x, y - ry * 0.72, rx * 0.66, ry * 0.16, 14), (250, 248, 240), None)       # top teeth
        return
    # cry: a wide, low, square-ish opening, the corners dragged down
    pts = [(-hw * 1.05, l13 + 0.03), (-hw * 0.5, l13 - 0.006), (0.0, l13 - 0.01), (hw * 0.5, l13 - 0.006),
           (hw * 1.05, l13 + 0.03), (hw * 0.7, l17 + 0.03), (0.0, l17 + 0.02), (-hw * 0.7, l17 + 0.03)]
    p.poly(curve(f.pts(pts), 3), (70, 26, 30), INK, 2.2)
    p.poly(curve(f.pts([(-hw * 0.6, l13 - 0.002), (0.0, l13 - 0.004), (hw * 0.6, l13 - 0.002), (0.0, l13 + 0.01)]), 3),
           (250, 248, 240), None)


# ---------------------------------------------------------------------------------------------- his head
def gaze(L, g):
    """This film's gaze_dy is a share of the eye's half-height (-1 up .. 1 down); traitors_cast.eye takes drawing units
    (found 11 Nov, cast chat 8: -0.7 moved the pupils under a pixel, so no planned eye move showed)."""
    eh = (L['eh'] if L else 0.0508) * P4.H / 1.8
    return g * eh * 0.85


def look_of(sp):
    return MOODS.get(sp.get('mood', 'neutral'), MOODS['neutral'])


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


def _outline(L):
    """P4.outline_uv without its fold: that list runs out to the upper-left temple and back and repeats the left
    temple point, so the smoothing folds the left forehead into a notch (Sam, 11 Nov: "strange ridges on the left
    side"). Here: once round, crown first, both temples alike."""
    pts = P4.outline_uv(L, 0.4, crown=-0.42)[2:]               # from the crown: right side, chin, left side
    out = []
    for q in pts:
        if not out or abs(q[0] - out[-1][0]) + abs(q[1] - out[-1][1]) > 1e-6:
            out.append(q)
    return [out[0], (-pts[-1][0], pts[-1][1])] + out[1:]       # the right upper temple, as the left has


def brand_head(img, p, sp, t, hx, hy):
    with _Big():
        return _brand_head(img, p, sp, t, hx, _lift(hy))


def _brand_head(img, p, sp, t, hx, hy):
    L = P4.layout(P4.target('brand', sp.get('average', False)))
    f = P4.Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin, look = BR_SKIN, look_of(sp)
    knot = sp.get('hair') == 'brand_knot'
    cap, mass, locks = brand_hair(L, knot)
    if mass:                                             # the curls behind the face, past the shoulders
        p.poly(curve(f.pts(mass), 2), BR_HAIR, INK, 2.4)
        _texture(p, f, mass, 46, 7)
    AV._ears(p, f, L, skin)
    p.poly(curve(f.pts(_outline(L)), 4), skin, INK, 2.6)
    brand_beard(p, f, L, skin)
    if sp.get('empty'):
        P4.nose(p, f, L, skin)
        P4.lips(p, f, L, dict(sp, smile=0.2), BR_LIP, f(0.0, L['lip13']))
        return f(0.0, L['lip13'])[0]
    deep_set(p, f, L, skin)
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', look['lid']), squint=sp.get('squint', look['squint']),
                          gaze_dy=gaze(L, sp.get('gaze_dy', look.get('gaze_dy', 0.0)))), BR_IRIS, dk(skin, 0.8), liner=2.8)
    P4.brows(p, f, L, BR_BROW, 0.056, look['brow'] + sp.get('brow_up', 0.0), look['frown'] + sp.get('frown', 0.0))
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, L['lip13'])
    if str(sp.get('mouth', 'rest')).startswith('v:') or look['mouth'] == 'lips':
        P4.lips(p, f, L, dict(sp, smile=look.get('smile', 0.0)), BR_LIP, (fx, my - 6))
    else:
        brand_mouth(p, f, L, look['mouth'])
    if look.get('tears') or sp.get('tears'):
        tears(p, f, L)
    if knot:
        bun(p, f)
    for sgn, lock in locks:                              # the curls over the cheeks' edges, covering the ears
        if sgn < 0 and f.tq > 0.6:
            continue
        p.poly(curve(f.pts(lock), 2), BR_HAIR, None)
        p.line(curve(f.pts(lock[:-3]), 2), INK, 2.4)              # inked on the face side only
        _texture(p, f, lock, 5, 11 + sgn, 0.14)
    p.poly(curve(f.pts(cap), 2), BR_HAIR, INK, 2.4)
    _top_strokes(p, f, L, knot)
    if sp.get('shades'):
        shades(p, f, L, lowered=sp['shades'] == 'lowered')
    return fx


# ---------------------------------------------------------------------------------------------- Brand turned
BRAND_PROFILE = TH.TEMPLATE


def _brand_mood(sp, f):
    look = look_of(sp)
    st = dict(lid=sp.get('lid4', look['lid']), look=min(1.0, sp.get('look', 0.0) + 0.55 * f.s),
              squint=sp.get('squint', look['squint']), closed=sp.get('blink', False),
              gaze_dy=gaze(f.L if hasattr(f, 'L') else None, sp.get('gaze_dy', look.get('gaze_dy', 0.0))))
    return st, look['brow'] + sp.get('brow_up', 0.0), look['frown'] + sp.get('frown', 0.0)


def _brand_rest(p, f, L, sp, fx, my):
    look = look_of(sp)
    if str(sp.get('mouth', 'rest')).startswith('v:') or look['mouth'] == 'lips':
        P4.lips(p, f, L, dict(sp, smile=look.get('smile', 0.0), mouth='rest'), BR_LIP, (fx, my - 6))
    else:
        brand_mouth(p, f, L, look['mouth'])


def _scr(f, psi, v):
    x, z = f.ring(psi, v)
    X, _ = f.view(x, z)
    return f.cx + float(X) * TH.H, f.top + v * TH.H


def _turned_long(p, f, colour=None, length=1.85):
    """His curls from the side and behind: hanging from the back of the skull, over the ear and the nape, down past
    the shoulders (v 1.9); from three-quarter front a strip also shows past the far cheek."""
    H = TH.H
    yaw = round(math.degrees(f.th))
    sil = TH.silhouette(f, 0.1)
    near = {round(v, 2): x for x, y, v, part in sil if part == 'near'}
    far = {round(v, 2): x for x, y, v, part in sil if part == 'far'}
    vs = sorted(near)
    top_v = vs[0]
    wv = lambda pts, sd: waves(pts, 7, 70, out=-1.0, seed=sd, step=5)
    back = [(near[v] - H * (0.03 + 0.12 * max(0.0, v - top_v)), f.top + v * H) for v in vs if v <= 0.75]
    bx = back[-1][0]
    back += [(bx - H * 0.08, f.top + 1.3 * length / 1.85 * H), (bx - H * 0.02, f.top + length * H)]
    if yaw >= 180:
        front = [(far[v] + H * (0.03 + 0.12 * max(0.0, v - top_v)), f.top + v * H) for v in vs if v <= 0.75]
        fx_ = front[-1][0]
        front += [(fx_ + H * 0.08, f.top + 1.3 * length / 1.85 * H), (fx_ + H * 0.02, f.top + length * H)]
        poly = wv(back, 31) + [(bx + H * 0.1, f.top + (length + 0.07) * H), (fx_ - H * 0.1, f.top + (length + 0.05) * H)] + wv(front, 32)[::-1]
    else:
        ex, ey = _scr(f, -91, 0.42)
        reach = {45: 0.02, 90: 0.1, 135: 0.25}.get(yaw, 0.1) * H       # the hair in front of the ear (over it)
        inner = [(ex + reach + H * 0.02, f.top + length * H), (ex + reach, f.top + 1.1 * H), (ex + reach, ey),
                 (ex + reach * 0.6, f.top + 0.05 * H)]
        poly = wv(back, 31) + [(bx + H * 0.06, f.top + (length + 0.07) * H)] + inner
    p.poly(curve(poly, 2), colour or BR_HAIR, INK, 2.4)


def _brand_turned_hair(img, p, f, L, sp):
    knot = sp.get('hair') == 'brand_knot'
    cap, mass, locks = brand_hair(L, knot)
    if not knot:
        _turned_long(p, f)
    polys = [f.pts(TH.dense(curve(cap, 2)))]
    mask = TH.hair(img, p, f, polys, BR_HAIR, BRAND_PROFILE)
    TH.clipped(img, p, mask, lambda pen: _top_strokes(pen, f, L, knot))
    if knot:
        bun(p, f)
    if sp.get('shades') and math.degrees(f.th) < 100:
        shades(p, f, L, lowered=sp['shades'] == 'lowered')


_th_draw = TH.draw


def _th_draw_big(img, p, sp, t, view, hx, hy):
    if sp.get('who') != 'brand' and not str(sp.get('who', '')).startswith('press'):   # the press at his size too
        return _th_draw(img, p, sp, t, view, hx, hy)
    with _Big():                                  # (the press: no lift, or from behind the neck shows long)
        return _th_draw(img, p, sp, t, view, hx, hy if sp['who'] != 'brand' else _lift(hy))


TH.draw = _th_draw_big
TH.register(TH.Person(
    'brand', lambda sp: P4.layout(P4.target('brand', sp.get('average', False))), -0.42, 0.4,
    lambda L: BRAND_PROFILE, BR_SKIN, BR_IRIS, BR_BROW, BR_LIP, _brand_mood, _brand_rest, _brand_turned_hair,
    face=lambda pen, f, L, sp: brand_beard(pen, f, L, BR_SKIN), sheet=lambda: BRAND))


# ---------------------------------------------------------------------------------------------- the press pack
# Sam's note 4 (11 Nov): "the journalists are blob people". They were press_secretary's seated reporters (a back
# outline, no arms, no legs) stood on the pavement. Now each is a standing person (views.person: shoulders, arms, a
# collar, legs) with a turning head (turnhead, like Brand's: the skull, both ears, the neck, hair carried round the
# head) from behind (180) or three-quarter behind (135, the cheek, jaw and an eyebrow's end showing).
# style: front hair design; hl: hairline; the profile keys say how far down the back the hair reaches.
PRESS_STYLES = {
    'short': dict(hl=-0.1, prof=dict(hair_low=0.4, nape=0.66)),
    'crop': dict(hl=-0.06, prof=dict(hair_low=0.36, nape=0.62, volume=0.015)),
    'bald': dict(hl=None, prof=dict(hair_top=0.3, hair_top_back=0.34, hair_ragged=0.008, hair_low=0.66, nape=0.7)),
    'bob': dict(hl=-0.12, prof=dict(hair_low=0.9, nape=0.95, volume=0.07), long=1.1),
    'pony': dict(hl=-0.14, prof=dict(hair_low=0.44, nape=0.7, volume=0.02), pony=True),
    'curly': dict(hl=-0.08, prof=dict(hair_low=0.5, nape=0.74, volume=0.12), curls=True),
    'long': dict(hl=-0.14, prof=dict(hair_low=0.6, nape=0.8, volume=0.05), long=1.55),
    'side': dict(hl=-0.08, prof=dict(hair_low=0.44, nape=0.7, volume=0.035), parting=True),
}


def _press_layout(sp):
    m = dict(P4.AVG)
    for k, v in sp.get('face_m', {}).items():
        m[k] += v
    return P4.layout(m)


def _press_cap(L, hl):
    e, c = L['fw'] * 0.5, L['fhw'] * 0.5
    return [(-e - 0.02, 0.36), (-e - 0.03, 0.02), (-e + 0.04, -0.24), (-0.24, -0.4), (0.0, -0.45), (0.24, -0.4),
            (e - 0.04, -0.24), (e + 0.03, 0.02), (e + 0.02, 0.36), (e - 0.03, 0.34), (c + 0.01, 0.12), (c - 0.03, 0.02),
            (c * 0.7, hl), (0.0, hl - 0.012), (-c * 0.7, hl), (-c + 0.03, 0.02), (-c - 0.01, 0.12), (-e + 0.03, 0.34)]


def _press_profile(sp):
    st = PRESS_STYLES[sp['style']]
    return lambda L: TH.fitted(L, -0.42, 1.06, **st['prof'])


def _press_hair(img, p, f, L, sp):
    st, hc = PRESS_STYLES[sp['style']], sp['hair_c']
    H = TH.H
    if st.get('long'):
        _turned_long(p, f, hc, st['long'])
    fronts = [] if st['hl'] is None else [f.pts(TH.dense(curve(_press_cap(L, st['hl']), 2)))]
    prof = TH.PEOPLE[sp['who']].build(sp)[1]
    mask = TH.hair(img, p, f, fronts, hc, prof)
    rng = np.random.default_rng(sp.get('seed', 1))
    yaw = math.degrees(f.th)
    bx = f.hx + (0.0 if yaw >= 170 else -0.18 * H)            # the back of the skull on screen

    def strands(pen):                                          # the hair's fall: strokes down from the crown
        for k in range(14 if not st.get('curls') else 0):
            u = rng.uniform(-0.42, 0.42)
            x0, y0 = bx + u * H * 0.8, f.top - 0.36 * H + abs(u) * 0.2 * H
            pen.line(curve([(x0, y0), (x0 + u * 18, y0 + 0.25 * H), (x0 + u * 30, y0 + 0.55 * H)], 3), dk(hc, 0.72), 1.4)
        if st.get('curls'):                                    # curls: little loops all over
            for k in range(40):
                x, y = bx + rng.uniform(-0.5, 0.5) * H, f.top + rng.uniform(-0.45, 0.65) * H
                pen.line(oval(x, y, 9, 7, 10, 0.3, math.pi * 1.6), dk(hc, 0.66), 1.4)
        if st.get('parting'):
            pen.line(curve([(bx - 0.12 * H, f.top - 0.42 * H), (bx - 0.14 * H, f.top - 0.2 * H)], 3), dk(hc, 0.55), 1.6)
    TH.clipped(img, p, mask, strands)
    if st.get('pony'):                                         # a ponytail from the back of the head, a band round it
        x, y = bx, f.top + 0.36 * H
        tail = [(x - 16, y), (x - 26, y + 60), (x - 20, y + 130), (x - 4, y + 168), (x + 12, y + 132), (x + 20, y + 62),
                (x + 16, y)]
        p.poly(curve(tail, 3), hc, INK, 2.2)
        for k in range(3):
            p.line(curve([(x - 6 + 6 * k, y + 14), (x - 10 + 7 * k, y + 80), (x - 4 + 4 * k, y + 140)], 3), dk(hc, 0.72), 1.3)
        p.poly(oval(x, y + 6, 18, 8, 12), (40, 40, 44), INK, 1.6)


def _press_mood(sp, f):
    return dict(lid=0.1, look=0.3, squint=0.0, closed=False, gaze_dy=-0.2), 0.0, 0.0


def _press_rest(p, f, L, sp, fx, my):
    P4.lips(p, f, L, dict(sp, smile=0.0, mouth='rest'), sp.get('lip_c', (190, 120, 110)), (fx, my - 6))


def press_person(who, style, skin, hair_c, seed, face_m):
    """Register one journalist's turning head (built when first drawn) and return their cast entry's head part."""
    sp = dict(who=who, style=style, hair_c=hair_c, seed=seed, face_m=face_m,
              ears_hidden=style in ('bob', 'long', 'curly'))    # hair over the ears: none drawn on top of it
    if who not in TH.PEOPLE:
        TH.register(TH.Person(who, _press_layout, -0.42, 0.4, _press_profile(sp), skin, (80, 60, 44),
                              dk(hair_c, 0.8), (190, 120, 110), _press_mood, _press_rest,
                              lambda img, p, f, L, sp2, _sp=sp: _press_hair(img, p, f, L, dict(sp2, **_sp))))
    return sp


# ---------------------------------------------------------------------------------------------- torsos
def brand_torso(img, p, sp, t):
    """trial: the open white shirt's deep V, chest hair, crucifixes on chains, the long white scarf hanging both
    sides; stand: a small crucifix only; prison: the tracksuit's zip and collar."""
    look = sp.get('look_', 'trial')
    if look == 'prison':
        p.poly([(-34, -4), (34, -4), (40, 26), (-40, 26)], TRACK, INK, 2.2)          # the tracksuit's collar
        p.line([(0, 22), (0, 560)], dk(TRACK, 0.7), 2.4)                          # the zip
        p.poly([(-5, 30), (5, 30), (5, 50), (-5, 50)], (180, 180, 184), INK, 1.2)
        return
    p.poly([(-22, 40), (22, 40), (0, 120)], BR_SKIN, None)                       # the open shirt, deeper
    p.line([(-22, 40), (0, 120), (22, 40)], INK, 2.0)
    for k in range(5):
        x = -10 + 5 * k
        p.line([(x, 56 + 6 * (k % 2)), (x + 3, 70 + 6 * (k % 2))], dk(BR_HAIR, 1.4), 1.4)
    p.line(curve([(-18, 4), (-8, 60), (0, 84), (8, 60), (18, 4)], 3), (190, 190, 196), 1.4)    # the chain
    p.poly([(-3, 82), (3, 82), (3, 112), (-3, 112)], (200, 200, 206), INK, 1.0)                # the crucifix
    p.poly([(-10, 90), (10, 90), (10, 96), (-10, 96)], (200, 200, 206), INK, 1.0)
    if look == 'trial':
        for sgn in (-1, 1):                                                    # the long white scarf
            pts = [(sgn * 30, -6), (sgn * 56, 4), (sgn * 52, 200), (sgn * 58, 420), (sgn * 30, 430), (sgn * 26, 210),
                   (sgn * 18, 40)]
            p.poly(curve(pts, 3), SCARF, INK, 2.2)
            p.line(curve([(sgn * 40, 30), (sgn * 38, 220), (sgn * 44, 410)], 3), dk(SCARF, 0.86), 1.6)
            for k in range(5):
                x = sgn * (30 + 6 * k)
                p.line([(x, 428), (x + sgn * 1, 446)], dk(SCARF, 0.8), 1.6)


def judge_torso(img, p, sp, t):
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


def judge_head(img, p, sp, t, hx, hy):
    """The library's head (bald under the wig) with a short white bench wig: rows of rolled curls over the crown,
    a roll over each ear (the courtroom sketches 05, 07, 11)."""
    fx = TC._head(img, p, sp, t, hx, hy)
    hw, hh = sp.get('hw', 70), sp.get('hh', 90)
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


# ---------------------------------------------------------------------------------------------- the inmates
# Sam's note 5 (11 Nov): "strange heights, proportions and details next to Russell; no mouths?". The house head drew
# no mouth or brows at this size and its 'short' hair came out bald; Brand's face is the measured layout at HEAD_K.
# So the three inmates use his face system at his size (P4.layout from the average face, each pushed their own way),
# with lips, brows, a nose, ears, eye bags, shaped hair and stubble or a beard. Front view only (they never turn).
INMATE_FACES = {
    'inmate1': dict(m=dict(face_wide=0.06, jaw_wide=0.05, eye_size=-0.012, nose_wide=0.08, brow_high=-0.15,
                           mouth_wide=0.04, chin_long=0.02), iris=(70, 96, 120), lip=(186, 120, 106),
                    brow=(52, 40, 32), hair='crop', stub=0.82),
    'inmate2': dict(m=dict(face_wide=0.03, jaw_wide=0.1, nose_wide=0.2, eyes_apart=0.08, lip_low=0.03,
                           mouth_wide=0.1, brow_slope=-4.0), iris=(52, 34, 24), lip=(110, 64, 56),
                    brow=(28, 22, 20), hair='bald', beard=(46, 40, 38)),
    'inmate3': dict(m=dict(face_wide=-0.05, jaw_wide=-0.04, eye_size=0.01, nose_long=0.02, mouth_wide=-0.04,
                           chin_long=0.03, brow_slope=4.0), iris=(96, 120, 90), lip=(204, 132, 120),
                    brow=(160, 110, 64), hair='side', freckles=True),
}


def _inmate_layout(who):
    m = dict(P4.AVG)
    for k, v in INMATE_FACES[who]['m'].items():
        m[k] = m[k] + v
    return P4.layout(m)


def inmate_head(img, p, sp, t, hx, hy):
    with _Big():
        return _inmate_head(img, p, sp, t, hx, _lift(hy))


def _inmate_head(img, p, sp, t, hx, hy):
    who = sp['who']
    fc = INMATE_FACES[who]
    L = _inmate_layout(who)
    up = max(0.0, -sp.get('gaze_dy', 0.0))                 # looking up at the TV: the face tips up a little
    f = P4.Face(hx, hy, down=-0.8 * up)
    skin, hc = sp['skin'], sp.get('hair_c', (40, 32, 28))
    fw, fhw = L['fw'], L['fhw']
    e, c = fw * 0.5, fhw * 0.5
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
    P4.brows(p, f, L, fc['brow'], 0.05 if fc['hair'] != 'side' else 0.04, sp.get('brow_up', 0.012 * up),
             sp.get('frown', 0.0))
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, L['lip13'])
    P4.lips(p, f, L, dict(sp, smile=sp.get('smile', -0.4)), fc['lip'], (fx, my - 6))
    hl = -0.06
    if fc['hair'] == 'crop':                                  # a short crop: a low straight hairline, the skull's shape
        cap = [(-e - 0.01, 0.3), (-e - 0.02, 0.04), (-e + 0.04, -0.22), (-0.24, -0.38), (0.0, -0.43), (0.24, -0.38),
               (e - 0.04, -0.22), (e + 0.02, 0.04), (e + 0.01, 0.3), (e - 0.02, 0.3), (c + 0.01, 0.12), (c - 0.03, 0.02),
               (c * 0.7, hl), (0.0, hl - 0.012), (-c * 0.7, hl), (-c + 0.03, 0.02), (-c - 0.01, 0.12), (-e + 0.02, 0.3)]
        p.poly(curve(f.pts(cap), 2), hc, INK, 2.4)
        rng = np.random.default_rng(5)
        for _ in range(36):                                   # the crop's texture: short strokes
            u, v = rng.uniform(-c, c), rng.uniform(-0.36, hl - 0.03)
            if abs(u) < c * (1.0 - max(0.0, -v - 0.25) * 2.0):
                p.line([f(u, v), f(u + 0.008, v + 0.025)], B.lt(hc, 1.7), 1.4)
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


TC.HEADS.update(brand=brand_head, judge=judge_head)
TC.HEADS.update(inmate1=inmate_head, inmate2=inmate_head, inmate3=inmate_head)
TC.TORSOS.update(brand=brand_torso, judge=judge_torso, officer=officer_torso)
_hair_back = B.hair_back
B.hair_back = hair_back
V.LONG_HAIR['brand_long'] = 230          # his curls in the side and back views

# ---------------------------------------------------------------------------------------------- the people
BRAND = dict(who='brand', name='Russell Brand', skin=BR_SKIN, hw=66, hh=96, head_dy=10, hair='brand_long',
             hair_c=BR_HAIR, brow_c=BR_BROW, brow_w=4.6, beard='full', beard_c=BD_MID, outfit='suit',
             jacket=GREY_JKT, sleeve=GREY_JKT, trousers=dk(GREY_JKT, 0.7), shirt=(248, 248, 246), tie=None,
             shoe=(22, 18, 16), shoulders=150, full=True, pose='custom', height=1.83, seed=91, look_='trial')
BRAND_STAND = dict(BRAND, jacket=DARK_SUIT, sleeve=DARK_SUIT, trousers=DARK_SUIT, look_='stand')
BRAND_DOCK = dict(BRAND_STAND, hair='brand_knot', jacket=GREY_JKT, sleeve=GREY_JKT)
BRAND_PRISON = dict(BRAND, hair='brand_knot', outfit='jumper', jacket=TRACK, sleeve=TRACK, trousers=TRACK,
                    shoe=(236, 236, 236), look_='prison')
JUDGE = dict(who='judge', name='The judge (invented)', skin=(236, 190, 168), hw=70, hh=90, head_dy=10, hair='bald',
             hair_c=(240, 238, 230), brow_c=(150, 140, 132), brow_w=4.4, outfit='suit', jacket=(170, 26, 34),
             sleeve=(170, 26, 34), trousers=(170, 26, 34), shirt=(246, 246, 246), tie=None, shoe=(20, 16, 14),
             shoulders=164, full=True, pose='custom', height=1.72, seed=92, glasses=True)
OFFICER = dict(who='officer', name='Prison officer', skin=(150, 100, 70), hw=70, hh=90, head_dy=10, hair='crop',
               hair_c=(30, 26, 24), brow_c=(30, 26, 24), brow_w=4.6, outfit='jumper', jacket=(244, 244, 246),
               sleeve=(244, 244, 246), trousers=(24, 24, 28), shirt=(244, 244, 246), tie=(20, 20, 24), bottom=500,
               shoe=(16, 14, 14), shoulders=168, full=True, pose='custom', height=1.80, seed=93)
NEWSREADER = dict(who='newsreader', name='Newsreader', skin=(226, 182, 156), hw=64, hh=88, head_dy=10, hair='side',
                  hair_c=(150, 108, 66), brow_c=(110, 80, 56), brow_w=3.8, outfit='suit', jacket=(28, 34, 60),
                  sleeve=(28, 34, 60), trousers=(28, 34, 60), shirt=(246, 246, 248), tie=(170, 24, 36),
                  shoe=(18, 16, 14), shoulders=146, full=True, pose='custom', height=1.76, seed=94)
CAST = {'brand': BRAND, 'judge': JUDGE, 'officer': OFFICER, 'newsreader': NEWSREADER}
LOOKS = {'trial': BRAND, 'stand': BRAND_STAND, 'dock': BRAND_DOCK, 'prison': BRAND_PRISON}


# ---------------------------------------------------------------------------------------------- the sheets
def _font(n):
    return ImageFont.truetype(FONT, n)


def sheet(out):
    """Front, side, back of everyone at true heights (Brand in his three looks), a 1.75 m person."""
    import landmarks
    import sizes
    MC.CAST.clear()
    MC.CAST.update(CAST)
    B.SS = 1
    rows = [('Russell Brand: trial (arrival, gates)', BRAND), ('Brand: dock (sentencing)', BRAND_DOCK),
            ('Brand: prison', BRAND_PRISON), ('The judge (invented)', JUDGE), ('Prison officer', OFFICER),
            ('Newsreader', NEWSREADER)]
    tw, th = 330, 470
    W, H = 60 + tw * 6, 90 + th * 3
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    d.text((30, 20), 'BLESSED: the cast (front, side, back)', font=_font(40), fill=(30, 30, 30))
    cam = B.Cam(1.0, 540, 960)
    for r, (label, sp) in enumerate(rows):
        s = 0.5 * sp['height'] / 1.75
        col, row = (r % 2) * 3, r // 2
        x0, y0 = 30 + col * tw, 80 + row * th
        d.text((x0 + 4, y0), f"{label} ({sp['height']:.2f} m)", font=_font(24), fill=(30, 30, 30))
        for i, yaw in enumerate((0, 90, 180)):
            tile = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
            V.person(tile, cam, 540, 840 - 928 * s, s, dict(sp), 0.0, yaw)
            tile = tile.crop((290, 60, 790, 880))
            tile.thumbnail((tw, th - 40))
            img.alpha_composite(tile, (x0 + i * tw // 1 if False else x0 + i * tw, y0 + 34))
    img.convert('RGB').save(out, quality=88)
    return out


FACES = [('trial', 'showman', None, 'showman'), ('trial', 'showman', 'lowered', 'shades lowered'),
         ('trial', 'neutral', 'on', 'shades on'), ('stand', 'oath', None, 'the oath'),
         ('dock', 'hollow', None, 'sentenced'), ('prison', 'numb', None, 'numb'),
         ('prison', 'weeping', None, 'weeping'), ('prison', 'dejected', None, 'on the phone'),
         ('prison', 'amazed', None, 'amazed'), ('trial', 'overjoyed', None, 'overjoyed'),
         ('trial', 'neutral', None, 'neutral'), ('trial', 'neutral', None, 'talking')]


def faces_sheet(out):
    """His face large in every mood and look; his photos beside (rule 76)."""
    B.SS = 1
    tw, th = 360, 470
    img = Image.new('RGBA', (tw * 6 + 20, th * 3 + 20), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    cam = B.Cam(1.0, 540, 960)
    for i, (lk, mood, sh, label) in enumerate(FACES):
        sp = dict(LOOKS[lk], mood=mood, shades=sh, mouth='v:AI' if label == 'talking' else 'rest')
        tile = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
        V.person(tile, cam, 540, 900, 1.3, sp, 0.0, 0)
        tile = tile.crop((300, 400, 780, 1030))
        tile.thumbnail((tw - 10, th - 40))
        x, y = 10 + (i % 6) * tw, 10 + (i // 6) * th
        img.alpha_composite(tile, (x, y))
        d.text((x + tw // 2, y + th - 24), label, font=_font(26), fill=(40, 40, 40), anchor='mm')
    ref = os.path.join(HERE, '..', 'references', 'blessed', 'likeness')
    for i, n in enumerate(('b01-front-courthousenews', 'b03-front-bbc', 'b05-smiling-wikimedia',
                           'b07-sunglasses-front-guardian', 'b08-topknot-sketch-guardian', 'b02-front-eyesdown-guardian')):
        im = Image.open(os.path.join(ref, n + '.jpg')).convert('RGBA')
        im.thumbnail((tw - 10, th - 20))
        img.alpha_composite(im, (10 + i * tw + (tw - 10 - im.width) // 2, 10 + 2 * th + (th - 20 - im.height) // 2))
    img.convert('RGB').save(out, quality=88)
    return out


def turn_sheet(out, moods=('neutral', 'showman', 'hollow')):
    B.SS = 1
    yaws = (0, 45, 90, 135, 180)
    tw, th = 330, 420
    img = Image.new('RGB', (tw * 5, 50 + th * len(moods)), (232, 228, 222))
    d = ImageDraw.Draw(img)
    for i, lab in enumerate(('front', 'three-quarter', 'side', 'three-quarter behind', 'behind')):
        d.text((tw * i + tw // 2, 25), lab, font=_font(26), fill=(40, 40, 40), anchor='mm')
    for r, mood in enumerate(moods):
        for i, yaw in enumerate(yaws):
            im = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
            sp = dict(BRAND_DOCK if mood == 'hollow' else BRAND, mood=mood)
            V.person(im, B.Cam(1.0, 540, 960), 540, 1060, 1.25, sp, 0.0, yaw)
            img.paste(im.crop((375, 600, 705, 1020)).resize((tw, th)).convert('RGB'), (tw * i, 50 + th * r))
        d.text((8, 58 + th * r), mood, font=_font(26), fill=(40, 40, 40))
    img.save(out, quality=90)
    return out


def head_png(who, out, average=False):
    B.SS = 1
    im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    V.person(im, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(CAST[who], average=average), 0.0, 0)
    im.crop((180, 300, 900, 1250)).convert('RGB').save(out)
    return out


cast_sheet = sheet

if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    elif sys.argv[1] == 'faces':
        print(faces_sheet(sys.argv[2]))
    elif sys.argv[1] == 'turn':
        print(turn_sheet(sys.argv[2]))
    elif sys.argv[1] == 'head':
        print(head_png(sys.argv[2], sys.argv[3], '--average' in sys.argv))
