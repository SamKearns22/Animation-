#!/usr/bin/env python3
"""MAP  The people kit's measured famous faces (ranking item 4; overnight chat 4c, 14 Nov). A real person's head is
their likeness card's measures (likeness.py) pushed and tuned, drawn the Brand way: a full beard in three colours,
long loose curls (or pulled into a topknot), deep-set eyes, the house moods. LIFTED unchanged in look from
blessed_cast.py (Brand, Blessed chats 1-11); every colour, the card, the push, the tune and the moods come from the
person's description lines (people.py builds sp['kit_famous']), nothing is keyed by name. Front on here; every turned
view through turnhead (a Person registered per face, 'kit:WHO'). Torso extras: open shirt, crucifix, scarf, zip.

Map: the house moods 26 | beard 51 | hair 108 | extras on the face 240 | turned hair 318 |
     the head 389 | turned head 460 | torsos 488 | install 524
"""
import json
import math
import os

import numpy as np

import people_parts as PP
from people_parts import AV, P4, TH, dk, INK, curve, oval  # noqa: F401
from midterminal_cast import blend

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHADES = (28, 30, 36)
SCARF = (244, 242, 236)

# ---------------------------------------------------------------------------------------------- the house moods
# Lifted from Brand's (Blessed, Sam's answers 8-9, notes 22, 36, 41); a description's `mood NAME:` line adds or changes
# one. brow: up (+); frown (+) pulls the inner ends down, (-) lifts them (worry); lid: upper lid down; mouth: lips
# (with smile) or an open shape (grin, gasp, cry); gaze_dy: -1 up .. 1 down; tears.
MOODS = {'neutral': dict(brow=0.0, frown=0.0, lid=0.16, squint=0.0, mouth='lips', smile=0.2),
         'showman': dict(brow=0.03, frown=-0.01, lid=0.14, squint=0.45, mouth='grin'),
         'sincere': dict(brow=0.02, frown=-0.03, lid=0.12, squint=0.1, mouth='lips', smile=0.5),
         'oath': dict(brow=0.04, frown=0.0, lid=0.0, squint=0.0, mouth='lips', smile=0.0, gaze_dy=-0.6),
         'hollow': dict(brow=0.006, frown=-0.04, lid=0.34, squint=0.0, mouth='lips', smile=-0.6, gaze_dy=0.6),
         'numb': dict(brow=0.0, frown=-0.01, lid=0.3, squint=0.0, mouth='lips', smile=-0.3),
         'weeping': dict(brow=0.01, frown=-0.07, lid=0.3, squint=0.5, mouth='cry', tears=True),
         'dejected': dict(brow=0.004, frown=-0.05, lid=0.28, squint=0.15, mouth='lips', smile=-0.8, tears=True),
         'deadeyed': dict(brow=0.0, frown=0.0, lid=0.4, squint=0.0, mouth='lips', smile=-0.15),
         'phone': dict(brow=0.004, frown=-0.05, lid=0.04, squint=0.0, mouth='lips', smile=-0.8),
         'stern': dict(brow=-0.02, frown=0.05, lid=0.22, squint=0.1, mouth='lips', smile=-0.4),
         'sceptic': dict(brow=0.035, frown=0.05, lid=0.26, squint=0.15, mouth='lips', smile=-0.5),
         'amazed': dict(brow=0.06, frown=0.0, lid=0.0, squint=0.0, mouth='gasp'),
         'overjoyed': dict(brow=0.05, frown=-0.01, lid=0.1, squint=0.5, mouth='grin')}


def look_of(sp):
    moods = dict(MOODS, **sp['kit_famous'].get('moods', {}))
    return moods.get(sp.get('mood', 'neutral'), moods['neutral'])


# ---------------------------------------------------------------------------------------------- the beard
def full_beard(p, f, L, skin, c, seed=91):
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
    p.poly(body, c['mid'], None)
    # grey-white over the chin and the jaw: everything below a tufted line from the jaw corner under the mouth
    low_top = AV.tufts([(fw * 0.5 + 0.01, 0.66), (jw * 0.42, 0.8), (mw * 0.5, l17 + 0.08), (0.0, l17 + 0.1),
                        (-mw * 0.5, l17 + 0.08), (-jw * 0.42, 0.8), (-fw * 0.5 - 0.01, 0.66)], 0.016 * ta, 0.016,
                       out=1.0, seed=seed + 2)
    n = len(edge)
    p.poly(f.pts(edge[n // 5: n - n // 5] + low_top), c['low'], None)
    # the dark moustache: from under the nose, over the lip, down past the corners (a horseshoe) to the chin patch
    mt = max(ny + 0.03, l0 - 0.06)                       # a band over the lip (b10), not the whole philtrum
    top = AV.tufts([(-mw * 0.7, l13 + 0.02), (-mw * 0.6, mt + 0.01), (-nw * 0.5, mt), (0.0, mt + 0.006),
                    (nw * 0.5, mt), (mw * 0.6, mt + 0.01), (mw * 0.7, l13 + 0.02)], 0.008, 0.013, out=1.0,
                   seed=seed + 3)
    down = [(mw * 0.62, l13 + 0.012), (mw * 0.12, l17 - 0.004), (mw * 0.08, l17 + 0.03), (0.0, l17 + 0.045),
            (-mw * 0.08, l17 + 0.03), (-mw * 0.12, l17 - 0.004), (-mw * 0.62, l13 + 0.012)]   # the drooping ends, a soul patch
    must = f.pts(top + AV.tufts(down, 0.008, 0.014, out=-1.0, seed=seed + 4))
    p.poly(must, c['moust'], None)
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
            p.line([q, q2], c['grain'] if light else blend(c['mid'], c['grain'], 0.45), 1.6)
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


def curls_hair(L, knot=False, seed=3):
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


def _texture(p, f, c, poly_uv, n, seed, length=0.2):
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
        p.line(curve(f.pts(pts), 3), c['grey'] if rng.uniform() < 0.35 else c['light'], 1.8)


def _top_strokes(p, f, L, knot, col):
    c = L['fhw'] * 0.5
    if knot:                                          # pulled back: a few lines sweeping back to the bun, low
        for a, b in (((-0.14, -0.2), (-0.06, -0.38)), ((0.14, -0.2), (0.06, -0.38))):
            p.line(curve(f.pts([a, ((a[0] + b[0]) / 2 * 1.2, (a[1] + b[1]) / 2), b]), 3), col['light'], 1.6)
        return
    strokes = (((-0.08, -0.21), (-0.2, -0.4)), ((0.08, -0.21), (0.2, -0.4)), ((-0.22, -0.17), (-c - 0.04, -0.3)),
               ((0.22, -0.17), (c + 0.04, -0.3)), ((0.0, -0.22), (0.0, -0.44)))
    for i, (a, b) in enumerate(strokes):
        if i == 2 and f.tq > 0.4:                     # the far side narrows: its outer stroke would leave the hair
            continue
        mid = ((a[0] + b[0]) / 2 + (0.03 if i % 2 else -0.03), (a[1] + b[1]) / 2)
        p.line(curve(f.pts([a, mid, b]), 3), col['grey'] if i == 1 else col['light'], 1.8)


def bun(p, f, c, back=False):
    """The topknot on the crown (sketch b08): a round knot of curls, a band, a few ends."""
    x, y = f(0.0, -0.47)
    p.poly(curve(oval(x, y, 28, 24, 18), 2), c['hair'], INK, 2.4)
    for k in range(3):
        p.line(curve([(x - 22 + 14 * k, y - 18), (x - 14 + 14 * k, y - 4), (x - 20 + 14 * k, y + 12)], 3),
               c['grey'] if k == 1 else c['light'], 1.8)
    p.line([(x - 14, y + 26), (x + 14, y + 26)], (30, 26, 24), 4.0)



# ---------------------------------------------------------------------------------------------- extras on the face
def shades(p, f, L, lowered=False):
    """Aviator sunglasses (ref 02, b06, b07, b09): two big black teardrop lenses in a heavy black frame, a straight
    brow bar (hunt 1, 12 Nov: the thin gold rims read as a bar at phone size). Lowered (Sam's answer 8): slid down
    the nose, the eyes showing over the rims."""
    dv = 0.13 if lowered else 0.0
    for sgn in (-1, 1):
        cx, ey = sgn * L['ecx'], L['eye_y'] + 0.02 + dv
        w = L['ew'] * 1.12
        lens = [(cx - sgn * w * 0.7, ey - 0.075), (cx + sgn * w * 0.95, ey - 0.08), (cx + sgn * w * 1.08, ey - 0.03),
                (cx + sgn * w * 0.85, ey + 0.1), (cx + sgn * w * 0.05, ey + 0.125), (cx - sgn * w * 0.62, ey + 0.08),
                (cx - sgn * w * 0.76, ey - 0.01)]   # two lenses, a gap at the bridge (hunt 2: one band)
        q = curve(f.pts(lens), 3)
        p.poly(q, SHADES, INK, 4.2)
        p.line(curve(f.pts([(cx - sgn * w * 0.45, ey - 0.04), (cx + sgn * w * 0.25, ey - 0.05)]), 2), (96, 102, 116), 2.4)
        p.line(f.pts([(cx + sgn * w * 1.05, ey - 0.06), (sgn * L['fw'] * 0.5, ey - 0.065)]), INK, 3.4)
    y = L['eye_y'] - 0.06 + dv
    p.line(f.pts([(-L['ecx'] + L['ew'] * 0.8, y), (L['ecx'] - L['ew'] * 0.8, y)]), INK, 3.0)


def tears(p, f, L, u=None):
    """u None: the old streak and drop. u given (Blessed note 41: streaks read as snot): only a drop, squeezed out
    by a blink, running down the cheek over u = 0..1 (the left one a beat behind); nothing when u is out of range."""
    if u is not None:
        for sgn, k in ((-1, 0.25), (1, 0.0)):
            v = u - k
            if not 0.0 <= v <= 1.0:
                continue
            x, y = f(sgn * (L['ecx'] - L['ew'] * 0.1), L['eye_y'] + 0.05)
            y += 70 * v * (2 - v)
            p.poly(oval(x, y, 6 + 1.5 * v, 9 + 2 * v, 10), (170, 210, 236), INK, 1.4)
        return
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


def open_mouth(p, f, L, kind):
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


# ---------------------------------------------------------------------------------------------- turned hair
def _look_clamp(look, s):
    """N11: a look past 1 (eyes to the corners) is kept; an ordinary one is clamped as before."""
    return look if abs(look) > 1.0 else min(1.0, look + 0.55 * s)


def _scr(f, psi, v):
    x, z = f.ring(psi, v)
    X, _ = f.view(x, z)
    return f.cx + float(X) * TH.H, f.top + v * TH.H


def _turned_long(p, f, colour, length=1.85):
    """His curls from the side and behind: hanging from the back of the skull, over the ear and the nape, down past
    the shoulders (v 1.9); from three-quarter front a strip also shows past the far cheek."""
    H = TH.H
    yaw = round(math.degrees(f.th))
    sil = TH.silhouette(f, 0.1)
    near = {round(v, 2): x for x, y, v, part in sil if part == 'near'}
    far = {round(v, 2): x for x, y, v, part in sil if part == 'far'}
    vs = sorted(near)
    top_v = vs[0]
    wv = lambda pts, sd: waves(pts, 11, 80, out=-1.0, seed=sd, step=5)
    # a full mass of curls, not a narrow band (hunt 1, 12 Nov: from the side it read as a plait)
    back = [(near[v] - H * (0.06 + 0.3 * max(0.0, v - top_v)), f.top + v * H) for v in vs if v <= 0.75]
    bx = back[-1][0]
    back += [(bx - H * 0.12, f.top + 1.3 * length / 1.85 * H), (bx - H * 0.04, f.top + length * H)]
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
        poly = wv(back, 31) + [(bx + H * 0.12, f.top + (length + 0.07) * H)] + inner
    p.poly(curve(poly, 2), colour, INK, 2.4)




def _turned_hair(img, p, f, L, sp):
    fm = sp['kit_famous']
    c, knot = fm['c'], fm['hair'] == 'knot'
    cap, mass, locks = curls_hair(L, knot)
    if not knot:
        _turned_long(p, f, c['hair'])
    polys = [f.pts(TH.dense(curve(cap, 2)))]
    mask = TH.hair(img, p, f, polys, c['hair'], TH.TEMPLATE)
    TH.clipped(img, p, mask, lambda pen: _top_strokes(pen, f, L, knot, c))
    if knot:
        bun(p, f, c)
    if sp.get('shades') and math.degrees(f.th) < 100:
        shades(p, f, L, lowered=sp['shades'] == 'lowered')


def hair_back(p, sp, hx, hy, hw, hh):
    """Behind the head: the big curly mass down past the shoulders (loose), or nothing (the topknot)."""
    fm = sp.get('kit_famous')
    if not fm:
        return _old_hair_back(p, sp, hx, hy, hw, hh)
    if fm['hair'] == 'knot':
        return
    pts = curls([(hx - hw - 30, hy - 40), (hx - hw - 70, hy + 120), (hx - hw - 66, hy + 300), (hx + hw + 66, hy + 300),
                 (hx + hw + 70, hy + 120), (hx + hw + 30, hy - 40), (hx, hy - hh - 30), (hx - hw - 30, hy - 40)],
                18, 46, out=1.0, seed=5)
    p.poly(pts, dk(fm['c']['hair'], 0.85), INK, 2.6)


# ---------------------------------------------------------------------------------------------- the head
def _card(fm):
    """The likeness card's measures, pushed and tuned, registered once under the face's own key."""
    k = fm['key']
    if k not in P4.MEASURED:
        card = json.load(open(os.path.join(ROOT, fm['card'])))
        m, a = card['measures'], card['average']
        P4.MEASURED[k] = {q: P4.AVG[q] + m[q] - a[q] for q in P4.AVG}
        P4.PUSH[k] = fm['push']
        P4.TUNE[k] = dict(fm['tune'])
    return k


def layout(sp):
    return P4.layout(P4.target(_card(sp['kit_famous']), sp.get('average', False)))


def famous_head(img, p, sp, t, hx, hy):
    with PP._Big():
        return _famous_head(img, p, sp, t, hx, PP._lift(hy))


def _famous_head(img, p, sp, t, hx, hy):
    fm = sp['kit_famous']
    c = fm['c']
    L = layout(sp)
    f = P4.Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin, look = sp['skin'], look_of(sp)
    knot = fm['hair'] == 'knot'
    cap, mass, locks = curls_hair(L, knot)
    if mass:                                             # the curls behind the face, past the shoulders
        p.poly(curve(f.pts(mass), 2), c['hair'], INK, 2.4)
        _texture(p, f, c, mass, 46, 7)
    AV._ears(p, f, L, skin)
    p.poly(curve(f.pts(PP._outline(L)), 4), skin, INK, 2.6)
    if fm.get('beard'):
        full_beard(p, f, L, skin, fm['beard'])
    if sp.get('empty'):
        P4.nose(p, f, L, skin)
        P4.lips(p, f, L, dict(sp, smile=0.2), fm['lip'], f(0.0, L['lip13']))
        return f(0.0, L['lip13'])[0]
    if fm.get('deep_set'):
        deep_set(p, f, L, skin)
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', look['lid']), squint=sp.get('squint', look['squint']),
                          gaze_dy=PP.gaze(L, sp.get('gaze_dy', look.get('gaze_dy', 0.0)))), fm['iris'], dk(skin, 0.8),
            liner=2.8)
    P4.brows(p, f, L, sp['brow_c'], fm['brow_thick'], look['brow'] + sp.get('brow_up', 0.0),
             look['frown'] + sp.get('frown', 0.0))
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, L['lip13'])
    if str(sp.get('mouth', 'rest')).startswith('v:') or look['mouth'] == 'lips':
        P4.lips(p, f, L, dict(sp, smile=look.get('smile', 0.0)), fm['lip'], (fx, my - 6))
    else:
        open_mouth(p, f, L, look['mouth'])
    if look.get('tears') or sp.get('tears'):
        tears(p, f, L, sp.get('tear_u'))
    if knot:
        bun(p, f, c)
    for sgn, lock in locks:                              # the curls over the cheeks' edges, covering the ears
        if sgn < 0 and f.tq > 0.6:
            continue
        p.poly(curve(f.pts(lock), 2), c['hair'], None)
        p.line(curve(f.pts(lock[:-3]), 2), INK, 2.4)              # inked on the face side only
        _texture(p, f, c, lock, 5, 11 + sgn, 0.14)
    p.poly(curve(f.pts(cap), 2), c['hair'], INK, 2.4)
    _top_strokes(p, f, L, knot, c)
    if sp.get('shades'):
        shades(p, f, L, lowered=sp['shades'] == 'lowered')
    return fx


# ---------------------------------------------------------------------------------------------- turned head
def _mood(sp, f):
    look = look_of(sp)
    st = dict(lid=sp.get('lid4', look['lid']), look=_look_clamp(sp.get('look', 0.0), f.s),
              squint=sp.get('squint', look['squint']), closed=sp.get('blink', False),
              gaze_dy=PP.gaze(f.L if hasattr(f, 'L') else None, sp.get('gaze_dy', look.get('gaze_dy', 0.0))))
    return st, look['brow'] + sp.get('brow_up', 0.0), look['frown'] + sp.get('frown', 0.0)


def _rest(p, f, L, sp, fx, my):
    look = look_of(sp)
    if str(sp.get('mouth', 'rest')).startswith('v:') or look['mouth'] == 'lips':
        P4.lips(p, f, L, dict(sp, smile=look.get('smile', 0.0), mouth='rest'), sp['kit_famous']['lip'], (fx, my - 6))
    else:
        open_mouth(p, f, L, look['mouth'])


def register(sp):
    """This face's turned head (turnhead), once per face key; its colours from the description."""
    fm = sp['kit_famous']
    if fm['key'] in TH.PEOPLE:
        return
    beard = fm.get('beard')
    TH.register(TH.Person(fm['key'], layout, -0.42, 0.4, lambda L: TH.TEMPLATE, sp['skin'], fm['iris'], sp['brow_c'],
                          fm['lip'], _mood, _rest, _turned_hair,
                          face=(lambda pen, f, L, sp2: full_beard(pen, f, L, sp2['skin'], beard)) if beard else None))


# ---------------------------------------------------------------------------------------------- torsos
def open_shirt(img, p, sp, t):
    """The open white shirt's deep V and chest hair."""
    p.poly([(-22, 40), (22, 40), (0, 120)], sp['skin'], None)
    p.line([(-22, 40), (0, 120), (22, 40)], INK, 2.0)
    for k in range(5):
        x = -10 + 5 * k
        p.line([(x, 56 + 6 * (k % 2)), (x + 3, 70 + 6 * (k % 2))], dk(sp['hair_c'], 1.4), 1.4)


def crucifix(img, p, sp, t):
    p.line(curve([(-18, 4), (-8, 60), (0, 84), (8, 60), (18, 4)], 3), (190, 190, 196), 1.4)    # the chain
    p.poly([(-3, 82), (3, 82), (3, 112), (-3, 112)], (200, 200, 206), INK, 1.0)                # the cross
    p.poly([(-10, 90), (10, 90), (10, 96), (-10, 96)], (200, 200, 206), INK, 1.0)


def scarf(img, p, sp, t):
    """A long white scarf hanging both sides, fringed (front on; turned: the film's body prop for now)."""
    for sgn in (-1, 1):
        pts = [(sgn * 30, -6), (sgn * 56, 4), (sgn * 52, 200), (sgn * 58, 420), (sgn * 30, 430), (sgn * 26, 210),
               (sgn * 18, 40)]
        p.poly(curve(pts, 3), SCARF, INK, 2.2)
        p.line(curve([(sgn * 40, 30), (sgn * 38, 220), (sgn * 44, 410)], 3), dk(SCARF, 0.86), 1.6)
        for k in range(5):
            x = sgn * (30 + 6 * k)
            p.line([(x, 428), (x + sgn * 1, 446)], dk(SCARF, 0.8), 1.6)


def zip_top(img, p, sp, t):
    """A tracksuit top: the collar round the neck and the zip down to the hem."""
    top = sp['jacket']
    p.poly([(-42, -6), (42, -6), (46, 26), (-46, 26)], top, INK, 2.2)
    p.line([(0, 22), (0, sp.get('bottom', 505) - 4)], dk(top, 0.7), 2.4)
    p.poly([(-5, 30), (5, 30), (5, 50), (-5, 50)], (180, 180, 184), INK, 1.2)


# ---------------------------------------------------------------------------------------------- install
_old_hair_back = None


def install():
    """Once: the hair behind famous heads, and their turned views through their own turnhead Person (drawn at the
    house's bigger head size, lifted, under the key 'kit:WHO' so no film's own Person is used)."""
    global _old_hair_back
    B, V = PP.B, PP.AV.MC.V
    if _old_hair_back is None:
        _old_hair_back = B.hair_back
        B.hair_back = hair_back
    V.LONG_HAIR['kit_curls'] = 230
    if getattr(V.head_view, 'kit_famous', False):
        return
    old = V.head_view

    def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
        fm = sp.get('kit_famous')
        if fm and view in TH.YAW:
            register(sp)
            with PP._Big():
                return TH.draw(img, p, dict(sp, who=fm['key']), t, view, hx, PP._lift(hy))
        return old(img, p, sp, t, view, hx, hy)
    head_view.kit_famous = head_view.turnhead = True
    V.head_view = head_view
