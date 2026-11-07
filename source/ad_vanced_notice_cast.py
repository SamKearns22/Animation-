#!/usr/bin/env python3
"""MAP  Ad-Vanced Notice (7 Nov): the cast. Vance is a measured likeness head (likeness.py card on the three official
portraits, references/ad-vanced-notice/) on the patriots4 face layout, drawn the Islamocommunism way.

    VANCE  JD Vance (card, 7 Nov): brows low and heavy (97th centile), long chin (95th), wide nose (93rd), brows rising
           to the outside, narrow hooded eyes, wide mouth, thin upper lip. Medium-dark brown hair swept up and over from
           a parting on his right (our left), receding at the temples into an M, short at the sides, a little grey
           over the ears. A short, full, brown beard with a ginger cast, joined to the moustache, up the cheeks to a
           line from mid-ear to past the mouth corners; blue eyes. Navy suit, white shirt, red tie, flag pin (Sam,
           7 Nov: the same in every shot). 1.88 m.
    MAN    The gas-station driver (invented, from the brief): 17 stone (108 kg), 1.80 m, a belly over his belt; a blue
           and red checked shirt, blue jeans, brown boots; a black goatee, balding pate with dark sides.

    python3 source/ad_vanced_notice_cast.py sheet OUT.jpg     front, side, back of both, a 1.75 m person
    python3 source/ad_vanced_notice_cast.py faces OUT.jpg     the faces large in every mood
    python3 source/ad_vanced_notice_cast.py head WHO OUT.png  one head straight on (for likeness.py check)

Map: colours 35 | measures 50 | Vance head 70 | man head 140 | torsos 175 | people 215 | sheets 235
"""
import json
import math
import os
import sys

import numpy as np

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import midterminal_cast as MC   # noqa: E402  (installs the hooks chain and the sheet helpers)
from midterminal_cast import B, TC, P4, V, dk, blend, FONT  # noqa: E402
from ed import INK, curve, oval, open_curve  # noqa: E402

# ---------------------------------------------------------------------------------------------- colours
V_SKIN = (232, 178, 152)          # fair, pink (card: 232, 172, 148)
V_HAIR = (82, 60, 44)             # medium-dark brown
V_HAIR_L = (120, 92, 70)
V_BEARD = (136, 100, 72)          # brown with a ginger cast, a touch of grey
V_IRIS = (92, 140, 186)           # blue
V_LIP = (204, 134, 120)
NAVY = (30, 38, 62)
RED_TIE = (150, 26, 38)
M_SKIN = (226, 170, 140)
M_HAIR = (26, 22, 22)
M_SHIRT = (178, 30, 36)           # (Sam, 7 Nov: "thicker colours, black and red"): a red and black buffalo check
M_CHECK = (26, 20, 22)
M_JEANS = (58, 84, 128)
M_BOOT = (96, 64, 40)

# ---------------------------------------------------------------------------------------------- measures (7 Nov)
_card = json.load(open(os.path.join(HERE, '..', 'references', 'ad-vanced-notice', 'vance-card.json')))
_VM, _VA = _card['measures'], _card['average']
P4.MEASURED['vance'] = {k: P4.AVG[k] + _VM[k] - _VA[k] for k in P4.AVG}   # differences from likeness.py's average
P4.PUSH['vance'] = 1.6
P4.TUNE['vance'] = dict(brow_high=1.3, chin_long=2.0, nose_wide=3.2, brow_slope=1.6, eyes_apart=5.0, mouth_wide=3.0, eye_tilt=5.5, eye_open=0.5)   # 7 Nov, likeness check rounds
P4.MEASURED['man'] = dict(P4.AVG, face_wide=P4.AVG['face_wide'] + 0.06, jaw_wide=P4.AVG['jaw_wide'] + 0.08,
                          eye_size=P4.AVG['eye_size'] - 0.02, brow_high=P4.AVG['brow_high'] - 0.06)
P4.PUSH['man'] = 1.0
P4.TUNE['man'] = {}

# Vance's moods (Sam, 7 Nov: "the four emotions show an identical picture"): each moves the brows, the lids and the
# mouth by a clear amount. brow: up (+) or (our left, our right); frown (+) pulls the inner ends down, (-) lifts them
MOODS = {'neutral': dict(brow=0.0, frown=0.0, lid=0.13, squint=0.0, smile=0.6, mouth='lips'),
         'sincere': dict(brow=0.02, frown=-0.035, lid=0.1, squint=0.0, smile=0.0, mouth='soft'),
         'smile': dict(brow=0.025, frown=0.0, lid=0.18, squint=0.45, smile=0.0, mouth='grin'),
         'teasing': dict(brow=(0.032, -0.01), frown=0.0, lid=0.16, squint=0.15, smile=0.0, mouth='smirk'),
         'proud': dict(brow=0.04, frown=0.0, lid=0.2, squint=0.4, smile=0.0, mouth='grin')}
SMILE = {'neutral': 0.6, 'sincere': 0.35, 'smile': 1.4, 'proud': 1.2, 'angry': -0.6, 'glare': -0.4}


def _ears(p, f, L, skin):
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.5:
            continue
        ex, ey = f(sgn * (L['fw'] * 0.5 + 0.01), 0.42)
        p.poly(oval(ex, ey, 11, 24, 20), skin, INK, 2.4)
        p.line([(ex - sgn * 2, ey - 10), (ex + sgn * 3, ey), (ex - sgn * 1, ey + 10)], dk(skin, 0.7), 1.4)


# ---------------------------------------------------------------------------------------------- Vance's beard
# (Sam, 7 Nov, close-up ref vance-beard-sam.jpg: "try to get this beard really correct"). Measured on that photo
# against its own cheek skin (201,164,150), then scaled to ours: a salt-and-pepper short beard. Darkest in a band
# along the underside of the jaw and chin, where it spills a little below the jawline (0.33 of the skin); mid on the
# cheeks and sides (0.67); lighter on the chin's front (0.83); a sparse, lighter moustache the skin shows through
# (0.75), joining the beard at the mouth corners; a dark soul patch under the lower lip's middle (0.63) with lighter
# patches either side (0.84); the upper edge on the cheeks soft and ragged, never a hard line; grey-blond and dark
# flecks all over (its 90th and 10th centiles).
B_MID = (124, 100, 86)            # ash brown (Sam, 7 Nov: "dark/medium brown/silver"; his close-up's cheek beard)
B_DARK = (90, 72, 62)             # the jaw's underside, the close-up's darkest band
B_MOUST = (130, 102, 86)          # the moustache: grey-brown, a touch warmer, blending into the cheeks
B_GRAIN = (170, 156, 146)         # the silver-ash grain
B_CHIN = (190, 152, 132)
B_MOUST = (178, 136, 116)
B_SOUL = (140, 104, 88)
B_FLECK_L = (204, 190, 176)
B_FLECK_D = (58, 44, 36)


def _ragged(rng, pts, amp):
    """A hand-cut edge: every other point nudged in or out a little (hairs, not a ruled line)."""
    out = []
    for i, (u, v) in enumerate(pts):
        out.append((u + rng.uniform(-amp, amp) * 0.5, v + (amp if i % 2 else -amp) * rng.uniform(0.3, 1.0)))
    return out


def tufts(pts, amp, step, out=1.0, seed=0):
    """A hair edge: the polyline resampled every `step` and every other point pushed `amp` to one side (out=+1 to the
    left of the travel direction, -1 to the right), so the edge is a row of small pointed tufts, not a ruled line."""
    import random
    rng = random.Random(seed)
    res = []
    for (u0, v0), (u1, v1) in zip(pts, pts[1:]):
        d = math.hypot(u1 - u0, v1 - v0)
        n = max(1, int(d / step))
        nu, nv = -(v1 - v0) / (d + 1e-9), (u1 - u0) / (d + 1e-9)
        for k in range(n):
            t = k / n
            u, v = u0 + (u1 - u0) * t, v0 + (v1 - v0) * t
            if k % 2:
                a = amp * out * rng.uniform(0.6, 1.0)
                u, v = u + nu * a, v + nv * a
            res.append((u, v))
    res.append(pts[-1])
    return res


def scrub_beard(p, f, L, skin, seed=81):
    """Vance's beard as Sam described it (7 Nov): a medium moustache from under the nose to the upper lip and out to
    the mouth corners; a beard covering the cheeks from the mouth corners out to the face's edge, round the jaw and
    halfway up the chin; a small patch under the lower lip; bare skin between that patch and the beard.
    Texture and colour (Sam, 7 Nov: "now get the texture and colour right"; measured on his close-up): an ash-brown
    body, a darker band along the jaw's underside, the moustache a touch warmer and lighter; every edge facing skin
    is a row of small hair tufts; an even grain of short strokes in one soft ash colour following the hair's fall.
    Flat shapes only: no random flecks (Sam, note 6)."""
    import random
    rng = random.Random(seed)
    fw, jw, ny, l0, l13, l17, mw, nw = L['fw'], L['jw'], L['nose_y'], L['lip0'], L['lip13'], L['lip17'], L['mw'], L['nw']
    half = (l17 + 1.0) / 2                                  # halfway up the chin
    bottom = [(-fw * 0.5 - 0.004, 0.46), (-fw * 0.5 - 0.004, 0.62), (-jw * 0.5 - 0.016, 0.83), (-jw * 0.38, 0.97),
              (-0.18, 1.035), (0.0, 1.05), (0.18, 1.035), (jw * 0.38, 0.97), (jw * 0.5 + 0.016, 0.83),
              (fw * 0.5 + 0.004, 0.62), (fw * 0.5 + 0.004, 0.46)]
    cheek = [(fw * 0.5 - 0.02, 0.46), (fw * 0.42, ny - 0.02), (fw * 0.32, ny + 0.01), (mw * 0.68, l0 - 0.012)]
    corner = [(mw * 0.62, l13 + 0.01), (mw * 0.56, l17 + 0.02), (mw * 0.42, half - 0.01)]
    right = cheek + corner + [(0.0, half)]
    left = [(-u, v) for u, v in right[::-1]]
    inner = tufts(right + left[1:], 0.012, 0.014, out=1.0, seed=seed)        # tufts reaching up into the skin
    edge = tufts(bottom, 0.007, 0.016, out=1.0, seed=seed + 1)                  # small tufts below the jaw
    body = f.pts(edge + inner)                    # straight joins: the tufts stay sharp
    p.poly(body, B_MID, None)
    # the darker underside: a band along the jaw's bottom, its upper edge tufted
    band_top = tufts([(fw * 0.5 - 0.03, 0.6), (jw * 0.5 - 0.05, 0.8), (jw * 0.28, 0.92), (0.0, 0.965),
                      (-jw * 0.28, 0.92), (-jw * 0.5 + 0.05, 0.8), (-fw * 0.5 + 0.03, 0.6)], 0.012, 0.014, out=1.0,
                     seed=seed + 2)
    n = len(edge)
    p.poly(f.pts(edge[n // 7: n - n // 7] + band_top), B_DARK, None)
    # the moustache: warmer and lighter, its lower edge tufts hanging just over the lip line
    top = tufts([(-mw * 0.66, l13 + 0.006), (-mw * 0.62, ny + 0.03), (-nw * 0.5, ny + 0.026), (0.0, ny + 0.032),
                 (nw * 0.5, ny + 0.026), (mw * 0.62, ny + 0.03), (mw * 0.66, l13 + 0.006)], 0.008, 0.014, out=1.0,
                seed=seed + 3)
    low = tufts([(mw * 0.66, l13 + 0.006), (mw * 0.4, l0 + 0.006), (0.0, l0 + 0.01), (-mw * 0.4, l0 + 0.006),
                 (-mw * 0.66, l13 + 0.006)], 0.006, 0.014, out=-1.0, seed=seed + 4)
    must = f.pts(top + low[1:-1])
    p.poly(must, B_MOUST, None)
    soul = tufts([(-mw * 0.13, l17 + 0.012), (-mw * 0.08, l17 + 0.05), (0.0, l17 + 0.072), (mw * 0.08, l17 + 0.05),
                  (mw * 0.13, l17 + 0.012)], 0.008, 0.014, out=-1.0, seed=seed + 5)
    p.poly(f.pts(soul), B_MID, None)
    # the grain: short strokes, staggered rows, a soft ash just lighter than the hair, falling down and in towards
    # the chin (along the jaw on the sides); none in the moustache (kept clean)
    grain = blend(B_MID, B_GRAIN, 0.78)
    for r, gv in enumerate(np.arange(0.5, 1.04, 0.042)):
        for gu in np.arange(-fw * 0.5 + (0.021 if r % 2 else 0.0), fw * 0.5, 0.042):
            u, v = gu + rng.uniform(-0.015, 0.015), gv + rng.uniform(-0.015, 0.015)
            q = f(u, v)
            if not _inside(body, q[0], q[1]) or (abs(u) < mw * 0.7 and l0 - 0.03 < v < half + 0.02):
                continue
            du, dv = -u * 0.5, 1.0
            n = math.hypot(du, dv)
            ln = rng.uniform(0.016, 0.024)
            q2 = f(u + du / n * ln, v + dv / n * ln)
            on_dark = v > 0.86 or abs(u) > jw * 0.5 - 0.04
            p.line([q, q2], blend(grain, B_DARK, 0.3) if on_dark else grain, 1.6)
    p.line(f.pts(edge), INK, 2.2)                               # the ink round the outer edge only


def beard_test(out, mood='neutral'):
    """The beard alone on an empty face (no eyes, brows or hair), large, beside Sam's close-up, both cropped to the
    same nose-to-neck framing and height."""
    B.SS = 1
    im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    V.person(im, B.Cam(1.0, 540, 960), 540, 1500, 2.8, dict(VANCE, empty=True, mood=mood), 0.0, 0)
    g = np.asarray(im.convert('RGB')).astype(int)
    skin = np.all(np.abs(g - np.array(V_SKIN)) < 6, axis=2)
    ys, xs = np.where(skin)
    top, bot = ys.min(), ys.max()                          # the face (and neck) in skin colour
    nose_y = top + int((bot - top) * 0.40)
    cols = np.where((g[nose_y:bot] < 250).any(axis=2).any(axis=0))[0]
    ours = im.convert('RGB').crop((cols.min() - 20, nose_y, cols.max() + 20, int(top + (bot - top) * 0.97)))
    ref = Image.open(os.path.join(HERE, '..', 'references', 'ad-vanced-notice', 'vance-beard-sam.jpg')).convert('RGB')
    H = 600
    ours = ours.resize((ours.width * H // ours.height, H))
    ref = ref.resize((ref.width * H // ref.height, H))
    sheet = Image.new('RGB', (ref.width + ours.width + 30, H + 50), (232, 228, 222))
    sheet.paste(ref, (0, 50))
    sheet.paste(ours, (ref.width + 30, 50))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(FONT, 30)
    d.text((10, 8), "Sam's reference", font=font, fill=(30, 30, 30))
    d.text((ref.width + 40, 8), 'ours (empty face)', font=font, fill=(30, 30, 30))
    sheet.save(out, quality=90)
    return out


# ---------------------------------------------------------------------------------------------- Vance's head
def vance_head(img, p, sp, t, hx, hy):
    L = P4.layout(P4.target('vance', sp.get('average', False)))
    f = P4.Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin, mood = V_SKIN, sp.get('mood', 'neutral')
    _ears(p, f, L, skin)
    out = curve(f.pts(P4.outline_uv(L, 0.4, crown=-0.42)), 4)
    p.poly(out, skin, INK, 2.6)
    fw, jw, ny, l0, l13, l17 = L['fw'], L['jw'], L['nose_y'], L['lip0'], L['lip13'], L['lip17']
    mw = L['mw']
    # the beard: one shape, short and full, from mid-ear down the jaw and round a long chin, up the cheeks to a line
    # sloping from the sideburn to just outside the mouth corners, the moustache joined to it; the lips clear
    scrub_beard(p, f, L, skin)
    if sp.get('empty'):                                    # the beard test: no eyes, brows or hair
        P4.nose(p, f, L, skin)
        P4.lips(p, f, L, dict(sp, smile=0.4), V_LIP, f(0.0, l13))
        return f(0.0, l13)[0]
    # the lips sit in a clear patch inside the beard (a soft gap round the lower lip, as in all three portraits)
    look = MOODS.get(mood, MOODS['neutral'])
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', look['lid']), squint=sp.get('squint', look['squint'])), V_IRIS,
            dk(skin, 0.82), liner=2.6)
    # the hooded outer corners (card: eyes drooping at the outside): a fold of lid over each eye's outer top corner,
    # its edge sloping down and out, so the opening droops at the outside as in all three portraits
    if not sp.get('blink'):
        w, h = L['ew'] * P4.H / 2, L['eh'] * P4.H / 1.8
        for sgn in (-1, 1):
            ex, ey = f(sgn * L['ecx'], L['eye_y'])
            ww = w * (1 - 0.3 * f.tq if sgn < 0 else 1.0)
            hood = [(ex + sgn * ww * 0.05, ey - h * 1.25), (ex + sgn * ww * 1.2, ey - h * 1.0),
                    (ex + sgn * ww * 1.12, ey + h * 0.15), (ex + sgn * ww * 0.6, ey - h * 0.55),
                    (ex + sgn * ww * 0.05, ey - h * 0.92)]
            p.poly(hood, skin, None)
            p.line(curve([(ex + sgn * ww * 0.05, ey - h * 0.92), (ex + sgn * ww * 0.6, ey - h * 0.55),
                          (ex + sgn * ww * 1.12, ey + h * 0.15)], 3), INK, 2.4)
    up = look['brow']
    raise_ = tuple(b + sp.get('brow_up', 0.0) for b in up) if isinstance(up, tuple) else up + sp.get('brow_up', 0.0)
    P4.brows(p, f, L, dk(V_HAIR, 0.85), 0.05, raise_, look['frown'] + sp.get('frown', 0.0))
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, l13)
    if str(sp.get('mouth', 'rest')).startswith('v:') or look['mouth'] == 'lips':
        P4.lips(p, f, L, dict(sp, smile=look['smile']), V_LIP, (fx, my - 6))
    else:
        vance_mouth(p, f, L, look['mouth'])
    # the hair: swept up and over to our right from a parting on our left, volume on top, receding temples (an M)
    fhw = L['fhw']
    c = fhw * 0.5
    hl = -0.05                                                  # a high hairline: a broad forehead below it
    hair = [(-fw * 0.5 + 0.004, 0.36), (-fw * 0.5 - 0.02, 0.18), (-c - 0.04, -0.04), (-c * 0.85, -0.24),
            (-0.2, -0.36), (-0.04, -0.42), (0.12, -0.43), (0.26, -0.38), (c * 0.9, -0.28), (c + 0.06, -0.1),
            (fw * 0.5 + 0.022, 0.16), (fw * 0.5 - 0.004, 0.36), (fw * 0.5 - 0.03, 0.22),       # sideburn, cropped
            (fw * 0.5 - 0.05, 0.06), (c * 0.86, -0.1), (c * 0.62, -0.14),                     # the temple, receding (M)
            (0.18, hl - 0.02), (0.06, hl + 0.0), (-0.06, hl - 0.01), (-0.16, hl - 0.03),      # the forelock, swept
            (-c * 0.62, -0.13), (-c * 0.86, -0.09), (-fw * 0.5 + 0.05, 0.07), (-fw * 0.5 + 0.03, 0.22)]
    p.poly(curve(f.pts([(-c * 0.8, 0.16), (-c * 0.76, -0.18), (c * 0.76, -0.18), (c * 0.8, 0.16)]), 3), skin, None)
    p.poly(curve(f.pts(hair), 4), V_HAIR, INK, 2.4)
    for a, b in (((-0.2, -0.06), (0.06, -0.38)), ((-0.06, -0.08), (0.2, -0.36)), ((0.08, -0.08), (0.3, -0.28)),
                 ((-0.3, 0.0), (-0.16, -0.3))):
        p.line(curve(f.pts([a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 0.03), b]), 3), V_HAIR_L, 1.6)
    p.line(curve(f.pts([(-c * 0.62, hl + 0.04), (-c * 0.64, -0.2), (-c * 0.54, -0.32)]), 3), dk(V_HAIR, 0.7), 1.8)  # parting
    for sgn in (-1, 1):                                                                # a little grey over the ears
        if sgn < 0 and f.tq > 0.5:
            continue
        p.line(curve(f.pts([(sgn * (fw * 0.5 + 0.004), 0.24), (sgn * (fw * 0.5 + 0.012), 0.32)]), 2),
               (150, 142, 136), 2.2)
    return fx


def MC_inside(poly, q):
    return _inside(poly, q[0], q[1])


def vance_mouth(p, f, L, kind):
    """His mouths for the moods: 'soft' (closed, corners up a little, earnest), 'grin' (open, top teeth, corners
    high), 'smirk' (closed, one corner up: our right)."""
    hw, l0, l13, l17 = L['mw'] / 2, L['lip0'], L['lip13'], L['lip17']
    if kind == 'grin':
        hw *= 1.12
        top = [(-hw, l13 - 0.03), (-hw * 0.5, l13 - 0.012), (0.0, l13 - 0.008), (hw * 0.5, l13 - 0.012), (hw, l13 - 0.03)]
        bot = [(hw, l13 - 0.03), (hw * 0.55, l17 + 0.012), (0.0, l17 + 0.03), (-hw * 0.55, l17 + 0.012)]
        p.poly(curve(f.pts(top + bot), 3), (70, 26, 30), INK, 2.2)
        teeth = [(-hw * 0.82, l13 - 0.022), (0.0, l13 - 0.006), (hw * 0.82, l13 - 0.022), (hw * 0.6, l13 + 0.012),
                 (0.0, l13 + 0.02), (-hw * 0.6, l13 + 0.012)]
        p.poly(curve(f.pts(teeth), 3), (250, 248, 240), None)
        p.line(curve(f.pts([(-hw, l13 - 0.03), (-hw * 0.5, l0 + 0.004), (0.0, l0 + 0.008), (hw * 0.5, l0 + 0.004),
                            (hw, l13 - 0.03)]), 3), dk(V_LIP, 0.8), 3.0)                   # the thin top lip
        for sgn in (-1, 1):                                                                # smile creases
            p.line(curve(f.pts([(sgn * (hw + 0.03), l13 - 0.07), (sgn * (hw + 0.05), l13 - 0.02),
                                (sgn * (hw + 0.035), l13 + 0.03)]), 3), dk(V_SKIN, 0.75), 1.6)
        return
    if kind == 'soft':
        ends = (0.014, 0.014)
    else:                                                                                  # smirk
        ends = (-0.002, 0.04)
    a, b = ends
    line = [(-hw, l13 - a), (-hw * 0.4, l13 + 0.004 - a * 0.3), (0.0, l13 + 0.004), (hw * 0.4, l13 + 0.004 - b * 0.3),
            (hw, l13 - b)]
    top = curve(f.pts([(-hw, l13 - a), (-hw * 0.4, l0 + 0.006), (0.0, l0 + 0.01), (hw * 0.4, l0 + 0.006),
                       (hw, l13 - b)] + line[::-1][1:-1]), 3)
    bot = curve(f.pts(line + [(hw * 0.5, l17 - 0.012 - b * 0.3), (0.0, l17 - 0.004), (-hw * 0.5, l17 - 0.012 - a * 0.3)]), 3)
    p.poly(top, dk(V_LIP, 0.86), INK, 1.5)
    p.poly(bot, V_LIP, INK, 1.5)
    p.line(curve(f.pts(line), 3), INK, 2.4)
    for sgn, e in ((-1, a), (1, b)):                                                       # a dimple at a raised corner
        if e > 0.01:
            p.line(curve(f.pts([(sgn * (hw + 0.012), l13 - e - 0.02), (sgn * (hw + 0.022), l13 - e + 0.004)]), 2),
                   dk(V_SKIN, 0.75), 1.6)


# ---------------------------------------------------------------------------------------------- the man's head
def man_head(img, p, sp, t, hx, hy):
    L = P4.layout(P4.target('man'))
    f = P4.Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin, mood = M_SKIN, sp.get('mood', 'glare')
    _ears(p, f, L, skin)
    fw, fhw, ny, l0, l13, l17 = L['fw'], L['fhw'], L['nose_y'], L['lip0'], L['lip13'], L['lip17']
    # balding: dark hair only round the sides and back, the pate bare and shiny (drawn under the skin outline)
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.5:
            continue
        side = [(sgn * (fw * 0.5 - 0.01), 0.4), (sgn * (fw * 0.5 + 0.03), 0.22), (sgn * (fw * 0.5 + 0.02), 0.1),
                (sgn * (fw * 0.5 - 0.03), 0.12), (sgn * (fw * 0.5 - 0.035), 0.38)]
        p.poly(curve(f.pts(side), 3), M_HAIR, INK, 2.2)
    out = curve(f.pts(P4.outline_uv(L, 0.46, crown=-0.2)), 4)
    p.poly(out, skin, INK, 2.6)
    for sgn in (-1, 1):                                         # the side hair over the outline at the temples
        if sgn < 0 and f.tq > 0.5:
            continue
        side = [(sgn * (fw * 0.5 + 0.008), 0.4), (sgn * (fw * 0.5 + 0.02), 0.22), (sgn * (fw * 0.5 + 0.004), 0.12),
                (sgn * (fw * 0.5 - 0.035), 0.16), (sgn * (fw * 0.5 - 0.035), 0.38)]
        p.poly(curve(f.pts(side), 3), M_HAIR, INK, 2.0)
    p.line(curve(f.pts([(-0.12, -0.14), (-0.04, -0.17), (0.04, -0.16)]), 3), (246, 214, 196), 3.0)   # pate shine
    # the black goatee: moustache joined round the mouth to a short block on the chin
    mw = L['mw']
    goatee = [(-mw * 0.62, l13 + 0.02), (-mw * 0.58, l0 - 0.01), (-L['nw'] * 0.45, ny + 0.014), (0.0, ny + 0.02),
              (L['nw'] * 0.45, ny + 0.014), (mw * 0.58, l0 - 0.01), (mw * 0.56, l13 + 0.02), (mw * 0.34, l17 + 0.07),
              (0.08, 0.98), (0.0, 0.99), (-0.08, 0.98), (-mw * 0.34, l17 + 0.07)]
    p.poly(curve(f.pts(goatee), 4), M_HAIR, None)
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', 0.22) + 0.035 * ((sp.get('anger') or -5) + 5), gaze_dy=sp.get('gaze_dy', -0.5)), (82, 60, 42),
            dk(skin, 0.82), liner=2.6)
    # the strength scale, 1 to 6 (Sam, 7 Nov: "6 is the first face that registers as anger"): the new 1 is the old 6
    ang = sp.get('anger')
    ang = ang + 5 if ang else ang
    frown = (min(0.012 * ang, 0.13) if ang else {'angry': 0.05, 'glare': 0.045}.get(mood, 0.0)) + sp.get('frown', 0.0)
    P4.brows(p, f, L, M_HAIR, 0.05, sp.get('brow_up', 0.0), frown)
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, l13)
    smile = -0.3 * ang if ang else SMILE.get(mood, -0.4)
    P4.lips(p, f, L, dict(sp, smile=smile), (176, 110, 100), (fx, my - 6))
    return fx


# ---------------------------------------------------------------------------------------------- torsos
def vance_torso(img, p, sp, t):
    """The flag pin on his left lapel (our right)."""
    sw = sp.get('shoulders', 158)
    x, y = sw * 0.46, 92
    p.poly([(x - 9, y - 6), (x + 9, y - 6), (x + 9, y + 6), (x - 9, y + 6)], (246, 246, 246), INK, 1.2)
    p.poly([(x - 9, y - 6), (x - 1, y - 6), (x - 1, y), (x - 9, y)], (40, 60, 140), None)
    for k in (-3, 1, 5):
        p.line([(x - 1, y + k), (x + 9, y + k)], (196, 36, 48), 1.4)


def man_torso(img, p, sp, t):
    """The checked shirt over a belly: red check lines on blue, a button placket, a collar, a belt under the belly."""
    sw = sp.get('shoulders', 186)
    bottom = int(sp.get('bottom', 560))
    belly = [(-sw * 0.92, 250), (-sw * 1.06, 380), (-sw * 0.98, bottom - 20), (sw * 0.98, bottom - 20),
             (sw * 1.06, 380), (sw * 0.92, 250)]
    p.poly(curve(belly, 4), M_SHIRT, INK, 2.6)
    body = [(-40, -4), (-sw * 0.8, 12), (-sw, 50), (-sw - 6, 200)] + belly + [(sw + 6, 200), (sw, 50), (sw * 0.8, 12), (40, -4)]
    check_lines(p, body, -sw * 1.1, sw * 1.1, 0, bottom)
    p.line([(0, 0), (0, bottom - 22)], dk(M_SHIRT, 0.7), 2.2)
    for y in range(60, bottom - 40, 70):
        p.ell(0, y, 5, 5, (236, 232, 222), INK, 1.0)
    for sgn in (-1, 1):
        p.poly([(sgn * 36, -6), (sgn * 64, 16), (sgn * 22, 40), (0, 10)], M_SHIRT, INK, 2.0)
    p.poly([(-sw * 0.98, bottom - 24), (sw * 0.98, bottom - 24), (sw * 0.96, bottom), (-sw * 0.96, bottom)],
           (60, 40, 28), INK, 2.0)                                                     # the belt
    p.poly([(-16, bottom - 22), (16, bottom - 22), (16, bottom - 2), (-16, bottom - 2)], (196, 176, 120), INK, 1.4)


_torso_view = V.torso_view


def _inside(poly, x, y):
    """Point in polygon (ray casting)."""
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
            c = not c
    return c


def check_lines(p, poly, x0, x1, y0, y1, step=48, col=M_CHECK, inset=2, width=22):
    """The shirt's check, cut to the shirt's outline (never past its edge)."""
    def runs(a, b):
        across = (0, inset + width / 2) if a[1] == b[1] else (inset + width / 2, 0)    # the band's thickness
        along = (inset, 0) if a[1] == b[1] else (0, inset)
        offs = (along, (-along[0], -along[1]), across, (-across[0], -across[1]))
        pts = [(a[0] + (b[0] - a[0]) * k / 60, a[1] + (b[1] - a[1]) * k / 60) for k in range(61)]
        seg = []
        for q in pts:
            ok = all(_inside(poly, q[0] + dx, q[1] + dy) for dx, dy in offs)
            if ok:
                seg.append(q)
            elif seg:
                if len(seg) > 1:
                    p.line(seg, col, width)
                seg = []
        if len(seg) > 1:
            p.line(seg, col, width)
    for x in range(int(x0) // step * step, int(x1), step):
        runs((x, y0), (x, y1))
    for y in range(int(y0) // step * step, int(y1), step):
        runs((x0, y), (x1, y))


def torso_view(img, p, sp, view, seated=False):
    """The man's side and back: a belly pushing his shirt out in front (side), and the check all round, cut to the
    shirt's outline."""
    _torso_view(img, p, sp, view, seated)
    if sp.get('who') != 'man':
        return
    sw = sp.get('shoulders', 186)
    bottom = int(min(sp.get('bottom', V.JACKET), 470) if seated else sp.get('bottom', V.JACKET))
    if view == 'side':
        d = 0.6 * sw
        body = curve([(-34, -8), (-d * 0.92, 22), (-d * 1.02, 130), (-d * 0.96, 320), (-d * 0.92, bottom),
                      (d * 1.24, bottom), (d * 1.42, 400), (d * 1.32, 300), (d * 0.9, 150), (d * 0.86, 30),
                      (30, -6)], 3)
        p.poly(body, M_SHIRT, INK, 2.6)
        check_lines(p, body, -d * 1.1, d * 1.5, 0, bottom)
        p.poly([(-d * 0.92, bottom - 20), (d * 1.24, bottom - 20), (d * 1.22, bottom), (-d * 0.92, bottom)],
               (60, 40, 28), INK, 2.0)
    elif view == 'back':
        body = [(-40, -4), (-sw * 0.8, 12), (-sw, 50), (-(sw + 6), 200), (-sw * B.HEM, bottom),
                (sw * B.HEM, bottom), (sw + 6, 200), (sw, 50), (sw * 0.8, 12), (40, -4)]
        check_lines(p, body, -sw - 10, sw + 10, 0, bottom)


V.torso_view = torso_view
_arm = V.arm


def arm(p, j2, side, sp, shape=None):
    """The driver's sleeves in the same check (Sam, 7 Nov: "checkered shirts tend to be 100% in pattern"): black
    bands across and along each sleeve piece, in the arm's own direction, kept inside its outline."""
    if sp.get('who') != 'man' or V.PROBE:
        return _arm(p, j2, side, sp, shape)
    sh, el, wr = j2['sh' + side], j2['el' + side], j2['wr' + side]
    with V.F.allow('a skeleton arm, checked in 3D (check_arm3); on screen it may be foreshortened'):
        B.arm(p, sh, el, wr, sp.get('sleeve'))
    w = 30
    for a, b, wa, wb in ((sh, el, w, w * 0.9), (el, wr, w * 0.9, w * 0.72)):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1
        tx, ty, nx, ny = dx / n, dy / n, -dy / n, dx / n
        for t in np.arange(14, n - 8, 48):                          # bands across the sleeve
            wt = (wa + (wb - wa) * t / n) - 5
            c = (a[0] + tx * t, a[1] + ty * t)
            p.line([(c[0] + nx * wt, c[1] + ny * wt), (c[0] - nx * wt, c[1] - ny * wt)], M_CHECK, 16)
        for off in (-0.4, 0.4):                                     # bands along it
            p.line([(a[0] + nx * wa * off + tx * 10, a[1] + ny * wa * off + ty * 10),
                    (b[0] + nx * wb * off - tx * 6, b[1] + ny * wb * off - ty * 6)], M_CHECK, 14)
    shape = shape or j2.get('hand', {}).get(side, 'fist')
    if shape != 'none':
        V.hand(p, j2, side, sp, shape)


V.arm = arm
TC.HEADS.update(vance=vance_head, man=man_head)
TC.TORSOS.update(vance=vance_torso, man=man_torso)

# ---------------------------------------------------------------------------------------------- the people
VANCE = dict(who='vance', name='JD Vance', skin=V_SKIN, hw=72, hh=94, head_dy=10, hair='slick', hair_c=V_HAIR,
             brow_c=V_HAIR, brow_w=4.4, beard='stubble', beard_c=V_BEARD, outfit='suit', jacket=NAVY, sleeve=NAVY,
             trousers=NAVY, shirt=(246, 246, 248), tie=RED_TIE, shoe=(20, 16, 14), shoulders=158, full=True,
             pose='custom', height=1.88, seed=81)
MAN = dict(who='man', name='The driver', skin=M_SKIN, hw=80, hh=92, head_dy=12, hair='bald', hair_c=M_HAIR,
           brow_c=M_HAIR, brow_w=4.6, beard='goatee', beard_c=M_HAIR, outfit='jumper', jacket=M_SHIRT, sleeve=M_SHIRT,
           trousers=M_JEANS, shirt=M_SHIRT, tie=None, shoe=M_BOOT, shoulders=186, leg_k=1.35, anger=4,   # Sam, 7 Nov: anger 4
           full=True, pose='custom',
           height=1.80, seed=82)
CAST = {'vance': VANCE, 'man': MAN}


# ---------------------------------------------------------------------------------------------- the sheets
def sheet(out):
    import landmarks
    import sizes
    MC.CAST.clear()
    MC.CAST.update(CAST)
    B.SS = 1
    W, H = 1900, 1880
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(FONT, 40)
    small = ImageFont.truetype(FONT, 26)
    cam = B.Cam(1.0, 540, 960)
    d.text((40, 24), 'AD-VANCED NOTICE: the cast (front, side, back)', font=big, fill=(30, 30, 30))
    for r, key in enumerate(('vance', 'man')):
        sp = CAST[key]
        s = 0.5 * sp['height'] / 1.75
        y0 = 100 + r * 900
        d.text((40, y0 - 4), f"{sp['name']} ({sp['height']:.2f} m)", font=big, fill=(30, 30, 30))
        for i, yaw in enumerate((0, 90, 180)):
            MC._tile(img, lambda im, yaw=yaw, sp=sp, s=s: V.person(im, cam, 540, 840 - 928 * s, s, dict(sp), 0.0, yaw),
                     (190, 60, 890, 880), (20 + 440 * i, y0 + 40))
            d.text((370 + 440 * i, y0 + 860), ('front', 'side', 'back')[i], font=small, fill=(40, 40, 40), anchor='mm')
    lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    landmarks.draw(ld, 540, 840 - 928 * 0.5, 0.5, 1000)
    sizes.scale_ref(ld, 640, 840, 0.5 / V.M_PER_UNIT)
    img.alpha_composite(lay.crop((390, 60, 890, 880)), (1360, 140))
    d.text((1610, 960), '1.75 m person', font=small, fill=(40, 40, 40), anchor='mm')
    img.convert('RGB').save(out, quality=88)
    return out


def faces_sheet(out):
    """The faces large, each mood; the references beside Vance's (rule 76)."""
    B.SS = 1
    rows = {'vance': [('neutral', 'rest', 'rest'), ('sincere', 'rest', 'sincere'), ('smile', 'rest', 'big smile'),
                      ('teasing', 'rest', 'teasing'), ('proud', 'rest', 'proud ("This guy")'), ('neutral', 'v:AI', 'talking')],
            'man': [(k, 'rest', f'anger {k}') for k in range(1, 7)]}
    W, H = 6 * 400 + 40, 3 * 560 + 40
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    small = ImageFont.truetype(FONT, 26)
    cam = B.Cam(1.0, 540, 960)
    for r, key in enumerate(('vance', 'man')):
        for i, (mood, mouth, label) in enumerate(rows[key]):
            sp = dict(CAST[key], mouth=mouth)
            sp.update(anger=mood, gaze_dy=-0.8) if isinstance(mood, int) else sp.update(mood=mood)
            MC._tile(img, lambda im, sp=sp: V.person(im, cam, 540, 900, 1.3, sp, 0.0, 0), (340, 470, 740, 980),
                     (20 + 400 * i, 20 + r * 560))
            d.text((220 + 400 * i, 550 + r * 560), label, font=small, fill=(40, 40, 40), anchor='mm')
    ref = os.path.join(HERE, '..', 'references', 'ad-vanced-notice')
    for i, n in enumerate(('vance-front-2023', 'vance-front-2025', 'vance-front-2026', 'vance-caricature-2022')):
        im = Image.open(os.path.join(ref, n + '.jpg')).convert('RGBA')
        im.thumbnail((380, 500))
        img.alpha_composite(im, (20 + 400 * i + (380 - im.width) // 2, 20 + 2 * 560 + (500 - im.height) // 2))
    d.text((W - 220, 2 * 560 + 260), 'references', font=small, fill=(40, 40, 40), anchor='mm')
    img.convert('RGB').save(out, quality=88)
    return out


def head_png(who, out, average=False):
    B.SS = 1
    im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    V.person(im, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(CAST[who], average=average), 0.0, 0)
    im.crop((240, 380, 840, 1200)).convert('RGB').save(out)
    return out


cast_sheet = sheet

if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    elif sys.argv[1] == 'faces':
        print(faces_sheet(sys.argv[2]))
    elif sys.argv[1] == 'beard':
        print(beard_test(sys.argv[2]))
    elif sys.argv[1] == 'head':
        print(head_png(sys.argv[2], sys.argv[3], '--average' in sys.argv))
