#!/usr/bin/env python3
"""MAP  facehouse (face tool chat 6, 14 Nov; Sam: "rebuild the face tool on the house head"). The face tool's heads
drawn the HOUSE way (Ad-vanced Notice, Blessed: the hand-made Walliams and Brand are the models), not traced off the
photo: the house outline, ears, eyes, brows, nose and lips (patriots4) at the house's bigger head size, on the
people kit's body and clothes; the hair a drawn house piece (shapes with an ink edge and a few strokes), the glasses,
age lines and braids from the face tool's measures, redrawn in house weights. What the face tool measured and Sam
picked (references/faces/NAME/pick/NAME-pick.json: the tuned measures of his pick, the colours, glasses, age lines,
eyes) is read as it is; nothing here is keyed by name except the hair piece the person's lines name.

Why: chat 5's Walliams replay ("not identifiable as him at all") and Sam's worry that the traced heads drift from
the house style. Sam on the tests: "a lot of great detail ... try to retain" (Kemi's plaits, Andy's eyes and
glasses, the age lines: "important for some characters"), "blend it into our existing style".

TWO LOOKS (the taste call, chat 6's sheet):
    house    the house's own plainness: skin moved most of the way to the house's tones, the house eye, only the
             strong age lines (strength 0.5 up), soft and short; the hair a clean shape with a few strokes
    detail   the house head carrying more of the test's detail: skin nearer the photo, the socket shade round the
             eyes, every measured age line (0.15 up), denser plaits and grey flecks
    Both: the measured face (the pick's tuned measures), the house ink and outline, the glasses at their measured
    size in house ink, the people kit's body (suit or blouse, neck, shoulders).

HAIR PIECES (named in the person's lines, `head: house NAME, hair PIECE`):
    swept    short and thick, brushed up and over to one side into a low quiff, the sides clipped and greying
             (Walliams' hand-made hair made general: its height, sweep and grey from the lines)
    braids   long box braids (chat 7, Sam's K1/K2): plaits from the middle parting over the whole crown, down the
             temples into two curtains past the shoulders, each plait one rope with chevrons from parting to tip; the
             hair's outline and hairline MEASURED off the pick's picture (pick_hair), not guessed (the guessed cap
             was a head too tall and narrow: the face itself was the pick's, the head read long); dark behind the
             neck, the neck redrawn at the person's neck_w; `ears` in the lines draws the ears over the plaits

    python3 source/facehouse.py sheet OUT.jpg NAME [NAME ...]   the design sheet: photo, the pick, both house looks
    python3 source/facehouse.py head NAME LOOK OUT.png             one head-and-shoulders (for the name test)

Map: reading the pick 52 | colours 65 | the head 88 | hair: swept 142, braids 178 (measured hair 179, crown 255,
     curtains 268, plaits 279, behind the neck 310, the piece 329) | glasses 357 | age lines 387 | the person 437 |
     sheet 494 | main 569
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
import people_parts as PP                        # noqa: E402  (the house head size, outline; installs the hooks)
from people_parts import AV, P4, dk, INK, curve, oval  # noqa: E402
from midterminal_cast import blend               # noqa: E402
from ed import open_curve                        # noqa: E402

# ---------------------------------------------------------------------------------------------- reading the pick
def pick_file(name):
    return os.path.join(ROOT, 'references', 'faces', name, 'pick', f'{name}-pick.json')


def load(name):
    """Sam's pick: its tuned measures, colours, glasses, age-line strengths and eyes."""
    d = json.load(open(pick_file(name)))
    h = d['heads'][d.get('picked', 'C')]
    return dict(name=name, meas=dict(h['measures']), col=d['colours'], glasses=d.get('glasses'),
                age=d.get('age') or {}, eyes=d.get('eyes') or {}, picked=d.get('picked', 'C'))


# ---------------------------------------------------------------------------------------------- colours
HOUSE_SKIN = [(246, 208, 188), (240, 196, 178), (226, 184, 150), (176, 120, 86), (120, 78, 56)]   # people.COLOURS


def house_tone(rgb, k):
    """The photo's colour moved k of the way to the nearest house skin tone at the same lightness (the house is
    warmer and cleaner than a photo's grey-pink)."""
    rgb = np.array(rgb, float)
    lum = lambda c: 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]          # noqa: E731
    tones = sorted(HOUSE_SKIN, key=lum)
    l0 = lum(rgb)
    for a, b in zip(tones, tones[1:]):
        if lum(a) <= l0 <= lum(b) or (l0 < lum(tones[0]) and a == tones[0]) or b == tones[-1]:
            t = float(np.clip((l0 - lum(a)) / max(1e-6, lum(b) - lum(a)), 0, 1))
            near = np.array(a, float) * (1 - t) + np.array(b, float) * t
            break
    return tuple(int(v) for v in rgb * (1 - k) + near * k)


LOOKS = {'house': dict(skin_k=0.65, age_min=0.5, age_k=0.6, sockets=False, flecks=False, plait_step=0.05),
         'detail': dict(skin_k=0.1, age_min=0.15, age_k=1.3, sockets=True, flecks=True, plait_step=0.034)}


# ---------------------------------------------------------------------------------------------- the head
def house_head(img, p, sp, t, hx, hy):
    """The people kit's head part 'house': sp['kit_house'] holds the pick (load()), the look and the hair piece."""
    with PP._Big():
        return _head(img, p, sp, t, hx, PP._lift(hy))


def _head(img, p, sp, t, hx, hy):
    kh = sp['kit_house']
    lk = LOOKS[kh['look']]
    L = P4.layout(kh['meas'])
    f = P4.Face(hx, hy)
    skin = sp['skin']
    hc = sp['hair_c']
    piece = kh['hair']
    if piece == 'braids':
        braids_behind(p, f, L, hc, kh, sp)
    if piece != 'braids':                                 # her plaits cover the ears
        AV._ears(p, f, L, skin)
    o = curve(f.pts(PP._outline(L, -0.42 if piece != 'braids' else _hair(L, kh)['crown'] + 0.06)), 4)
    p.poly(o, skin, INK, 2.6)
    if lk['sockets'] and kh['eyes'].get('shade', 0) >= 0.1:
        sockets(p, f, L, skin, kh['eyes']['shade'])
    ey = kh['eyes']
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', 0.12)), tuple(ey.get('iris') or (66, 46, 34)), dk(skin, 0.8),
            liner=2.8, iris_r=min(1.15, ey.get('iris_r', 0.95)), pupil_r=min(0.5, ey.get('pupil_r', 0.42)))
    P4.brows(p, f, L, sp['brow_c'], kh.get('brow_thick', 0.05), sp.get('brow_up', 0.0), sp.get('frown', 0.0))
    P4.nose(p, f, L, skin)
    age_lines(p, f, L, skin, kh['age'], lk)
    fx, my = f(0.0, L['lip13'])
    P4.lips(p, f, L, dict(sp, smile=sp.get('smile', 0.0)), sp['kit_house']['lip'], (fx, my - 6))
    if piece == 'swept':
        swept(p, f, L, hc, kh, lk)
    elif piece == 'braids':
        braids(p, f, L, hc, lk, kh)
        if kh.get('ears'):                                # over the plaits, as the pick drew them (K1: her width)
            AV._ears(p, f, L, skin)
    if kh.get('glasses'):
        glasses(p, f, L, kh['glasses'])
    return fx


def sockets(p, f, L, skin, shade):
    """The socket shade (the test's, kept for the 'detail' look): one flat crescent of darker skin under the brow,
    no ink, softer than the test's."""
    c = dk(skin, 1 - 0.16 * shade)
    for sgn in (-1, 1):
        ecx, ew, ey, by = L['ecx'], L['ew'], L['eye_y'], L['brow_y']
        top = by + 0.014
        pts = [(ecx - 0.6 * ew, ey), (ecx - 0.5 * ew, top + 0.45 * (ey - top)), (ecx - 0.15 * ew, top + 0.05 * (ey - top)),
               (ecx + 0.45 * ew, top + 0.1 * (ey - top)), (ecx + 0.8 * ew, top + 0.6 * (ey - top)), (ecx + 0.6 * ew, ey)]
        p.poly(curve(f.pts([(sgn * u, v) for u, v in pts]), 4), c, None)


# ---------------------------------------------------------------------------------------------- hair: swept
def swept(p, f, L, hc, kh, lk):
    """Short, thick hair brushed up and over to our right into a low quiff (Walliams' hand-made hair, made general):
    the cap as wide as the cheeks, rising higher on the sweep's side; the sides clipped close and greying."""
    e = L['fw'] * 0.5
    c = max(L['fhw'] * 0.5 + 0.02, e)
    hl = kh.get('hairline', -0.08)
    lift = kh.get('quiff', 0.06)                           # how much higher the sweep's side rises
    grey = kh.get('grey') or blend(hc, (150, 146, 142), 0.35)
    t = max(L['fhw'], L['fw'] * 0.9) * 0.5
    side = [(-c - 0.025, -0.22), (-c - 0.025, -0.1), (-e - 0.018, 0.06), (-e - 0.012, 0.26), (-e + 0.012, 0.29),
            (-t + 0.005, 0.12), (-t + 0.03, -0.02), (-t + 0.06, -0.12), (-t + 0.08, -0.22)]
    for sgn in (-1, 1):
        p.poly(curve(f.pts([(-u, v) for u, v in side] if sgn > 0 else side), 2), grey, INK, 2.2)
    top = [(-c - 0.03, -0.04), (-c - 0.04, -0.17), (-c + 0.0, -0.3), (-c * 0.6, -0.4), (-c * 0.15, -0.45 - lift * 0.3),
           (c * 0.3, -0.46 - lift * 0.8), (c * 0.68, -0.41 - lift), (c + 0.01, -0.3 - lift * 0.6), (c + 0.045, -0.16),
           (c + 0.035, -0.04)]
    front = [(c - 0.005, -0.04), (c - 0.05, -0.14), (c * 0.66, -0.16 + 0.02), (c * 0.42, hl - 0.01), (c * 0.12, hl + 0.015),
             (-c * 0.2, hl + 0.02), (-c * 0.48, hl + 0.005), (-c * 0.7, -0.13), (-c + 0.05, -0.14), (-c + 0.01, -0.04)]
    p.poly(curve(f.pts(AV.tufts(top, 0.005, 0.03, out=1.0, seed=31) + front), 2), hc, INK, 2.4)
    light = blend(hc, (150, 140, 136), 0.38)
    for k, (u, ln) in enumerate(((-0.3, 0.2), (-0.2, 0.27), (-0.09, 0.3), (0.02, 0.32), (0.13, 0.3), (0.24, 0.26),
                                 (0.33, 0.18))):         # brushed up and over to our right
        u *= c / 0.42
        p.line(open_curve(f.pts([(u, hl - 0.03), (u + 0.04, hl - 0.03 - ln * 0.6), (u + 0.1, hl - 0.03 - ln - lift * 0.5)]),
                          3), light if k % 2 else dk(hc, 0.6), 1.6)
    p.poly(curve(f.pts([(-c * 0.05, hl - 0.04), (c * 0.05, -0.3), (c * 0.3, -0.42 - lift * 0.6), (c * 0.18, -0.3),
                        (c * 0.08, hl - 0.04)]), 3), blend(hc, light, 0.5), None)   # the light on the quiff
    if lk['flecks']:                                     # grey flecks through the dark (his salt in the pepper)
        rng = np.random.default_rng(17)
        for _ in range(26):
            u, v = rng.uniform(-c * 0.85, c * 0.85), rng.uniform(-0.4, hl - 0.05)
            if v > -0.42 + 0.25 * (abs(u) / c) ** 2:
                p.line(f.pts([(u, v), (u + 0.012, v - 0.02)]), blend(grey, (210, 206, 202), 0.4), 1.2)


# ---------------------------------------------------------------------------------------------- hair: braids
def pick_hair(name, picked='C'):
    """The hair Sam picked, measured off the pick's picture (facepick traced it from the photos; chat 7, K1: the
    house cap was guessed, a head taller and narrower than the pick, and the head read long): its outer edge (half
    width at each row, both sides averaged) and the hairline over the forehead, in face units (facepick's canvas:
    Face(HX, HY), H face height, SC pixels per unit). None when there is no pick picture."""
    from PIL import Image
    from scipy import ndimage
    import facepick as FP
    png = os.path.join(ROOT, 'references', 'faces', name, 'pick', f'{name}-{picked}.png')
    if not os.path.exists(png):
        return None
    col = json.load(open(pick_file(name)))['colours']
    a = np.asarray(Image.open(png).convert('RGB')).astype(float)
    hair = (np.abs(a - col['hair']).sum(2) < np.abs(a - col['cloth']).sum(2)) & (a.max(2) < 80)
    hair = ndimage.binary_closing(hair, iterations=6) | hair
    skin = np.abs(a - col['skin']).sum(2) < 60
    H, cx, top = 172.0 * FP.SC, FP.HX * FP.SC, (FP.HY - 72) * FP.SC
    rows = {}
    for v in np.arange(-0.6, 1.1, 0.05):
        y = int(top + v * H)
        xs = np.nonzero(hair[y])[0] if 0 <= y < a.shape[0] else []
        if len(xs):
            rows[round(float(v), 2)] = ((cx - xs.min()) + (xs.max() - cx)) / 2 / H
    ys = np.nonzero(hair[:, int(cx) - 6:int(cx) + 6].any(1))[0]
    crown = (ys.min() - top) / H if len(ys) else -0.4
    hl = []
    for u in (0.0, 0.1, 0.2, 0.3):                          # the first skin under the hair, middle to temple
        x = int(cx + u * H)
        ys = np.nonzero(skin[:int(top + 0.3 * H), x])[0]
        if len(ys):
            hl.append((u, (ys.min() - top) / H))
    return dict(crown=float(crown), rows=rows, hairline=hl)


def _face_u(L, v):
    """The face outline's half width at row v (our right side)."""
    r = [q for q in PP._outline(L) if q[0] >= 0]
    r = sorted({round(q[1], 4): q for q in r}.values(), key=lambda q: q[1])
    return float(np.interp(v, [q[1] for q in r], [q[0] for q in r]))


VJ = 0.3                                     # where the crown's plaits become the curtains (about the eye line)
VS = np.linspace(VJ, 1.95, 40)               # the curtain's rows, top to bottom (fractions of the face height)


def _hair(L, kh):
    """The braids' shape: the measured hair (pick_hair) or, without one, a round cap; kept per head."""
    m = kh.get('_hair')
    if m is None:
        m = kh['_hair'] = pick_hair(kh['name'], kh.get('picked', 'C')) or {}
    e = L['fw'] * 0.5
    rows = m.get('rows') or {}
    vs = sorted(v for v in rows if v >= -0.36)
    crown = m.get('crown', -0.4)
    if vs:
        out_v = [crown] + vs + [1.95]
        last = rows[vs[-1]]
        out_u = [0.0] + [max(rows[v], _face_u(L, v) + 0.06) if v >= 0 else rows[v] for v in vs] + [last + 0.04]
    else:
        out_v, out_u = [crown, -0.25, 0.0, 0.5, 1.95], [0.0, e * 0.85, e + 0.12, e + 0.18, e + 0.22]
    hl = m.get('hairline') or [(0.0, -0.18), (0.2, -0.09), (0.3, -0.02)]
    return dict(crown=crown, out_v=np.array(out_v), out_u=np.array(out_u), hairline=hl)


def _out(hs, v):
    return np.interp(v, hs['out_v'], hs['out_u'])


def _resample(pts, n=60):
    """A path resampled to n points evenly along its length."""
    pts = np.array(pts, float)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    t = np.linspace(0, d[-1], n)
    return np.c_[np.interp(t, d, pts[:, 0]), np.interp(t, d, pts[:, 1])]


def _crown_paths(L, hs):
    """The crown's two edges (our right side), each from the parting to the curtain's top at VJ, resampled to the
    same count so a plait is the band between them at a share a: inner (a = 0) along the hairline over the forehead
    and down the temple just inside the face's edge; outer (a = 1) over the top of the head along the measured edge."""
    hl = sorted(hs['hairline'])
    (u0, v0), (ut, vt) = hl[0], hl[-1]                    # a rounded arch: level at the parting, as in the photos
    inner = [(u, v0 + (vt - v0) * (u / ut) ** 1.6) for u in np.linspace(u0, ut, 8)]
    for v in np.linspace(max(hl[-1][1], -0.05) + 0.06, VJ, 6):
        inner.append((_face_u(L, v) - 0.006, v))
    outer = [(0.0, hs["crown"])] + [(_out(hs, v), v) for v in np.linspace(hs["crown"] + 0.01, VJ, 30)]
    return _resample(inner), _resample(outer)


def _edges(L, hs):
    """A curtain's inner and outer edge (our right side) at each row VS: the inner edge on the cheek and jaw's ink
    line (the plaits meet the face with no gap, the face's width kept), then leaving the neck clear under the chin;
    the outer edge the measured hair's (the curtain as wide as the pick's)."""
    e, j = L['fw'] * 0.5, L['jw'] * 0.5
    face = np.array([_face_u(L, min(v, 1.0)) - 0.006 for v in VS])
    under = np.interp(VS, [0.82, 1.0, 1.2, 1.95], [j * 0.95, e * 0.76, e * 0.74, e * 0.8])   # the pick's neck gap
    inner = np.where(VS < 0.82, face, np.maximum(under, face))
    return inner, _out(hs, VS)


def _band(p, f, sgn, P, light, sep, n, step, w):
    """Plaits as bands across a strip whose edges are P(0) and P(1) (P(a) a path from top to bottom): a dark line
    between plaits, chevrons stacked down each, pointing the way the plait runs."""
    def at(arr, k):
        i = np.arange(len(arr))
        return np.interp(k, i, arr[:, 0]), np.interp(k, i, arr[:, 1])
    body = blend(sep, light, 0.22)                         # each plait a rope a shade lighter than the gaps
    for i in range(n):
        a0, a1 = i / n, (i + 1) / n
        g = 0.1 / n
        p.poly(f.pts([(sgn * u, v) for u, v in P(a0 + g)] + [(sgn * u, v) for u, v in P(a1 - g)[::-1]]), body, None)
        if i:
            p.line(f.pts([(sgn * u, v) for u, v in P(a0)]), sep, 1.5)
        mid = P((a0 + a1) / 2)
        lo, hi = P(a0 + 0.12 / n), P(a1 - 0.12 / n)
        d = np.r_[0, np.cumsum(np.hypot(*np.diff(mid, axis=0).T))]
        s = step * 0.5 if i % 2 else 0.0
        while s < d[-1] - step * 0.7:
            k0 = np.interp(s, d, np.arange(len(d)))
            k1 = np.interp(s + step * 0.7, d, np.arange(len(d)))
            (xl, yl), (xm, ym), (xr, yr) = at(lo, k0), at(mid, k1), at(hi, k0)
            p.line(f.pts([(sgn * xl, yl), (sgn * xm, ym), (sgn * xr, yr)]), light, w)
            s += step


def _looks(hc, lk):
    house = lk['plait_step'] > 0.04
    return (blend(hc, (160, 156, 160), 0.6 if house else 0.5), blend(hc, (0, 0, 0), 0.6), 7 if house else 10,
            lk['plait_step'], 1.7 if house else 1.3)


def braids_behind(p, f, L, hc, kh, sp):
    """Behind the face: the plaits that fall behind the neck (the photos: dark between the curtains, never the
    background), then the neck again over them, down to the collar (the person's neck_w: Kemi's is the pick's,
    wider than the house's)."""
    hs = _hair(L, kh)
    inner, _ = _edges(L, hs)
    yc = -11.0                                              # the collar's top in the body's units (views.torso)
    vc = (yc - f.top) / P4.H
    rows = VS[VS <= vc]
    right = [(u + 0.01, v) for u, v in zip(inner[:len(rows)], rows)] + [(inner[len(rows) - 1] + 0.01, vc)]
    p.poly(f.pts(right + [(-u, v) for u, v in right[::-1]]), dk(hc, 0.8), None)
    nw = sp.get('neck_w', 1.0)
    skin = sp['skin']
    p.poly([(f.cx - 32 * nw, -90), (f.cx + 32 * nw, -90), (f.cx + 35 * nw, yc), (f.cx - 35 * nw, yc)], skin, INK, 2.6)
    p.poly([(f.cx - 32 * nw, -90), (f.cx + 32 * nw, -90), (f.cx + 30 * nw, -46), (f.cx, -34), (f.cx - 30 * nw, -46)],
           dk(skin, 0.82), None)                            # the jaw's shadow on it (views' neck_shade)
    p.line([(f.cx - 35 * nw, yc), (f.cx + 35 * nw, yc)], skin, 2.0)   # no ink line along the collar's top


def braids(p, f, L, hc, lk, kh):
    """Box braids, all one piece over the face (K2, Sam 14 Nov: "her plaits go all the way to the top ... always the
    way she keeps her hair"): plaits from the middle parting over the whole crown, down the temples and on into two
    curtains past the shoulders, each plait one band from the parting to its own tip. The crown is the band between
    the hairline and the hair's measured edge; the curtains the band between the face's edge and the measured edge."""
    hs = _hair(L, kh)
    ci, co = _crown_paths(L, hs)
    ti, to = _edges(L, hs)
    inner = np.r_[ci, np.c_[ti, VS][1:]]
    outer = np.r_[co, np.c_[to, VS][1:]]
    light, sep, n, step, w = _looks(hc, lk)
    tips = []
    for i in range(n):
        xl = inner[-1][0] * (1 - i / n) + outer[-1][0] * i / n
        xr = inner[-1][0] * (1 - (i + 1) / n) + outer[-1][0] * (i + 1) / n
        tips.append([(xl, 1.94), ((xl + xr) / 2, 1.995), (xr, 1.94)])
    for sgn in (-1, 1):                                    # the tips first: the curtain's edge closes over them
        for t in tips:
            p.poly(f.pts([(sgn * u, v) for u, v in t]), hc, INK, 1.8)
    right = [tuple(q) for q in outer] + [tuple(q) for q in inner[::-1]]
    whole = right + [(-u, v) for u, v in right[::-1]]
    p.poly(curve(f.pts(whole), 2), hc, INK, 2.4)
    for sgn in (-1, 1):
        _band(p, f, sgn, lambda a: inner * (1 - a) + outer * a, light, sep, n, step, w)
    p.line(f.pts([(0.0, hs['crown'] + 0.02), (0.0, inner[0][1] - 0.005)]),
           blend(hc, (200, 170, 150), 0.45), 1.8)                   # the parting


# ---------------------------------------------------------------------------------------------- glasses
def glasses(p, f, L, g):
    """The measured frames (face tool: each lens's centre, width, top and bottom in eye widths) in house ink: a
    rounded box round each eye, an ink edge either side of the frame's colour, the bridge, the arms to the ears."""
    colr = tuple(g.get('colr', (30, 28, 30)))
    half, ew = L['ecx'], L['ew']
    lw = min(g['rim_w'], 0.17) * ew * P4.H
    y0 = max(L['eye_y'] + g['top'] * ew, L['brow_y'] - 0.02)
    y1 = L['eye_y'] + min(g['bot'], 1.0) * ew
    xi = max(half + g['cx'] * ew - g['w'] * ew / 2, 0.035)
    for sgn in (-1, 1):
        c, w = half + g['cx'] * ew, g['w'] * ew
        x0, x1 = sorted((sgn * max(c - w / 2, 0.035), sgn * min(c + w / 2, L['fw'] * 0.5)))
        r = 0.16
        box = [(x0, y0 + (y1 - y0) * r), (x0 + (x1 - x0) * r, y0), (x1 - (x1 - x0) * r, y0), (x1, y0 + (y1 - y0) * r),
               (x1, y1 - (y1 - y0) * r * 1.2), (x1 - (x1 - x0) * r * 1.4, y1), (x0 + (x1 - x0) * r * 1.4, y1),
               (x0, y1 - (y1 - y0) * r * 1.2)]
        pts = curve(f.pts(box), 3)
        p.line(pts + pts[:1], INK, lw + 2.4)
        p.line(pts + pts[:1], colr, lw)
        xo = x1 if sgn > 0 else x0
        ya = y0 + (y1 - y0) * 0.28
        p.line(f.pts([(xo, ya), (sgn * (L['fw'] * 0.5 + 0.012), ya + 0.01)]), INK, lw * 0.7 + 2.0)
        p.line(f.pts([(xo, ya), (sgn * (L['fw'] * 0.5 + 0.012), ya + 0.01)]), colr, lw * 0.7)
    yb = y0 + (y1 - y0) * 0.3
    br = open_curve(f.pts([(-xi, yb), (0.0, yb - 0.012), (xi, yb)]), 3)
    p.line(br, INK, lw * 0.8 + 2.0)
    p.line(br, colr, lw * 0.8)


# ---------------------------------------------------------------------------------------------- age lines
def age_lines(p, f, L, skin, age, lk):
    """The measured age lines (agelines' strengths) drawn the house way, the hand-made Walliams' smile folds and
    crinkles: soft open curves one or two shades darker than the skin, never ink; longer and darker the stronger the
    line. Only those at the look's strength or more."""
    st = {k: min(1.0, v * lk['age_k']) for k, v in (age.get('strength') or {}).items() if v >= lk['age_min']}
    dark = sum(skin) < 360                               # a darker skin needs a deeper shade to show
    pen = lambda s: (dk(skin, (0.74 if dark else 0.8) - 0.06 * s), 1.5 + 0.7 * s)   # noqa: E731
    nw, ny, mw, l13, ecx, ew, ey = L['nw'], L['nose_y'], L['mw'], L['lip13'], L['ecx'], L['ew'], L['eye_y']
    s = st.get('nasolabial', 0)
    if s:                                                # from the nose wing round to beside the mouth corner
        c, w = pen(s)
        for sg in (-1, 1):
            p.line(open_curve(f.pts([(sg * nw * 0.56, ny - 0.035), (sg * (mw * 0.6 + 0.022), ny + 0.04),
                                     (sg * (mw * 0.6 + 0.01), l13 + 0.015 + 0.03 * s)]), 3), c, w)
    s = st.get('marionette', 0)
    if s:                                                # short lines down from the mouth corners
        c, w = pen(s)
        for sg in (-1, 1):
            x0 = sg * (mw * 0.5 + 0.008)
            p.line(open_curve(f.pts([(x0, l13 + 0.012), (x0 + sg * 0.006, l13 + 0.035 + 0.03 * s)]), 3), c, w * 0.85)
    s = st.get('eye_bags', 0)
    if s:                                                # a shallow arc under each eye (the hand-made bag)
        c, w = pen(s)
        for sg in (-1, 1):
            cx = sg * ecx
            p.line(open_curve(f.pts([(cx - sg * ew * 0.3, ey + 0.058), (cx + sg * ew * 0.12, ey + 0.07 + 0.008 * s),
                                     (cx + sg * ew * 0.55, ey + 0.055)]), 3), c, w * 0.8)
    s = st.get('crows_feet', 0)
    if s:                                                # two or three short curves fanned out from the outer corner
        c, w = pen(s)
        for sg in (-1, 1):
            ox = sg * (ecx + ew * 0.66)
            for dy in ((-0.014, 0.012) if s < 0.6 else (-0.018, 0.002, 0.022)):
                p.line(open_curve(f.pts([(ox, ey + dy * 0.3), (ox + sg * 0.02, ey + dy * 1.1),
                                         (ox + sg * (0.03 + 0.012 * s), ey + dy * 1.9)]), 3), c, w * 0.75)
    s = st.get('forehead', 0)
    if s:                                                # one to three gentle lines across the forehead
        c, w = pen(s)
        for i in range(1 + int(s * 2.2)):
            y, hw = L['brow_y'] - 0.06 - 0.035 * i, L['fhw'] * (0.2 - 0.03 * i)
            p.line(open_curve(f.pts([(-hw, y + 0.006), (0.0, y - 0.006), (hw, y + 0.006)]), 3), c, w * 0.8)
    s = st.get('cheek_hollow', 0)
    if s:                                                # a soft stroke under the cheekbone
        c, w = pen(s * 0.8)
        for sg in (-1, 1):
            x0 = sg * (L['fw'] * 0.5 - 0.06)
            p.line(open_curve(f.pts([(x0, ey + 0.15), (x0 - sg * 0.025, ey + 0.22)]), 3), c, w * 0.8)


# ---------------------------------------------------------------------------------------------- the person
def person(name, look, hair, outfit=('suit', (31, 34, 58)), shirt=(246, 246, 246), tie=None, height=1.75, **kw):
    """The engine's person (views.person) for one picked face in one look, on the people kit's body."""
    import people
    pk = load(name)
    lk = LOOKS[look]
    col = pk['col']
    skin = house_tone(col['skin'], lk['skin_k'])
    d = dict(who=name, name=name.title(), skin=skin, hair_style='none', hair_c=tuple(col['hair']), height=height,
             brows=tuple(col['brow']), lips=house_tone(col['lip'], lk['skin_k'] * 0.5), outfit=outfit[0],
             jacket=tuple(outfit[1]), sleeve=tuple(outfit[1]), shirt=shirt, tie=tie)
    if 'neck_w' in kw:                                      # the person's lines: a wider neck (Kemi's, K1)
        d['neck_w'] = kw.pop('neck_w')
    sp = people.person(d)
    sp['hair'] = 'bald'                                    # the engine's own hair: none (the head part draws it all)
    kh = dict(pk, look=look, hair=hair, lip=d['lips'], **kw)
    if kh['age'] and lk['age_k']:
        kh['age'] = dict(kh['age'])
    sp.update(kit_head='house', kit_house=kh, neck_shade=True)
    return sp


CAST = {   # the test pair (Sam, 14 Nov): the lines a people file would hold
    'burnham': dict(hair='swept', outfit=('suit', (31, 34, 58)), shirt=(246, 246, 246), tie=None, quiff=0.05,
                    hairline=-0.07, brow_thick=0.058),
    'badenoch': dict(hair='braids', outfit=('suit', (30, 32, 58)), shirt=(246, 246, 246), height=1.7,
                     brow_thick=0.052, neck_w=1.2, ears=True),
}


def install():
    import people
    PP.AV.MC.TC.HEADS  # noqa: B018  (the hooks are installed on import)
    people.install({})
    TC = PP.AV.MC.TC
    return TC


def draw(name, look, out, size=900):
    """One head and shoulders, front on, on white: the people kit's person with the house head."""
    from PIL import Image
    from satire_style import install_circle_hands
    B, V = PP.B, PP.AV.MC.V
    install_circle_hands(B)
    TC = install()
    sp = person(name, look, **CAST[name])
    TC.HEADS[sp['who']] = house_head
    TC.TORSOS[sp['who']] = lambda *a: None
    B.SS = 1
    tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    V.person(tile, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(sp), 0.0, 0)
    crop = tile.crop((150, 280, 930, 1180)).convert('RGB')
    crop = crop.resize((size, int(size * 900 / 780)))
    crop.save(out)
    return out


# ---------------------------------------------------------------------------------------------- sheet
def sheet(out, names, looks=('house', 'detail')):
    """The design sheet: each person's front photo, the face tool's pick as Sam chose it, then each house look; the
    kept details named under each; a phone-size row (how big a face is in a film) below."""
    from PIL import Image, ImageDraw, ImageFont
    import facepick as FP
    tmp = os.path.join(os.path.dirname(os.path.abspath(out)), '_facehouse')
    os.makedirs(tmp, exist_ok=True)
    font = lambda n: ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)   # noqa: E731
    fontr = lambda n: ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans.ttf'), n)        # noqa: E731
    T = 460
    cols = 2 + len(looks)
    rowh = T + 250
    img = Image.new('RGB', (cols * (T + 20) + 20, 90 + len(names) * rowh), (236, 232, 226))
    d = ImageDraw.Draw(img)
    d.text((20, 22), 'Face tool on the house head: the test as picked, then two house looks', font=font(34),
           fill=(30, 30, 30))
    heads = ['photo', 'test (your pick)'] + [f'{i + 1}: house' if lk == 'house' else f'{i + 1}: house + detail'
                                             for i, lk in enumerate(looks)]
    for i, name in enumerate(names):
        y = 80 + i * rowh
        pk = json.load(open(pick_file(name)))
        photo, _ = FP._face_tile(os.path.join(ROOT, pk['fronts'][0]), None, T)
        sq = Image.new('RGB', (T, T), (255, 255, 255))
        photo = photo.convert('RGB')
        photo.thumbnail((T, T))
        sq.paste(photo, ((T - photo.width) // 2, (T - photo.height) // 2))
        pick = Image.open(os.path.join(ROOT, 'references', 'faces', name, 'pick', f"{name}-{pk['picked']}.png"))
        tiles = [sq, _fit(pick, T)]
        for lk in looks:
            png = os.path.join(tmp, f'{name}-{lk}.png')
            draw(name, lk, png)
            tiles.append(_fit(Image.open(png), T))
        for k, tl in enumerate(tiles):
            x = 20 + k * (T + 20)
            img.paste(tl, (x, y + 36))
            d.text((x, y + 4), f'{name.title()}: {heads[k]}', font=font(24), fill=(30, 30, 30))
        for k, line in enumerate(KEPT.get(name, ())):
            d.text((20 + 2 * (T + 20), y + T + 50 + 30 * k), line, font=fontr(22), fill=(40, 40, 40))
        for k, tl in enumerate(tiles):                     # phone size: a face about 70 px tall, as in a film shot
            sm = tl.resize((T // 4, T // 4))
            img.paste(sm, (20 + k * (T // 4 + 10), y + T + 50))
        d.text((20, y + T + 50 + T // 4 + 6), 'at phone size', font=fontr(20), fill=(60, 60, 60))
    img.save(out, quality=90)
    return out


KEPT = {'burnham': ('Kept from your pick: the thick dark rectangular glasses (measured),',
                    'his eyes (iris size and colour), the long chin and wide jaw, the hair',
                    'swept up to one side with grey sides, the smile folds and crow\'s feet.',
                    'Look 2 also keeps the shade round the eyes and grey flecks.'),
        'badenoch': ('Kept from your pick: the plaits (middle parting, crown lines, the chevrons),',
                     'the high strong brows, the big eyes, the wide full lips and nose,',
                     'the smile folds and eye bags (her strongest age lines).',
                     'Look 2 keeps more plaits, her skin nearer the photo, every age line.')}


def _fit(im, T):
    from PIL import Image
    im = im.convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    im = bg.convert('RGB')
    a = np.asarray(im.convert('L'))
    ys, xs = np.nonzero(a < 245)
    if len(xs):
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        side = max(x1 - x0, y1 - y0) + 40
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        sq = Image.new('RGB', (side, side), (255, 255, 255))      # past the picture's edge: white, not black
        sq.paste(im, (side // 2 - cx, side // 2 - cy))
        im = sq
    return im.resize((T, T))


# ---------------------------------------------------------------------------------------------- main
if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        print(sheet(a[1], a[2:] or ['burnham', 'badenoch']))
    elif a and a[0] == 'head':
        print(draw(a[1], a[2], a[3]))
    else:
        print(__doc__)
