#!/usr/bin/env python3
"""MAP  agelines (13 Nov, face tool chat 3; new: no kit piece drew a face's age). The lines that make a face read its
age, MEASURED from the photo and drawn on any measured-face head (patriots4_cast's layout), so a 56-year-old does
not come out young and round.

    MEASURE  measure(crop, mask, q, ipd) -> {line: depth} for six creases, each found where it lies in the photo:
             nasolabial folds (nose wing to past the mouth corner), crow's feet (beside the outer eye corner),
             eye bags (under the lower lid), forehead lines, marionette lines (down from the mouth corners), and
             the cheek hollow under the cheekbone. A crease is a valley: darker than the skin either side of it,
             across its own direction; its depth is how much darker, as a share of the skin's brightness. Glasses,
             hair and background are never sampled (the photo's segmentation). The nasolabial fold's own path is
             kept (how far out it sits from the nose wing and mouth corner) so the drawing follows the photo.
             Every depth is less plain skin's own reading (the same search on the smooth mid-cheeks), so lighting,
             texture and a darker skin's lower brightness do not read as lines.
    STRENGTH strength(depths) -> 0..1 per line: LO (faint) to HI (full), set from 19 front photos of 15 people; a
             person's depth is the mean of their two deepest front photos (light hides creases more than it makes
             them); times age_factor(age) when the age is given (--says age=N). rank(): where they stand among
             the line-up (every film's front photos). Drawn AFTER the likeness check (rule 49.3's reason: the face
             finder reads a cheek fold as the lips).
    DRAW     draw(p, f, L, skin, age) on the head after the nose: thin lines one shade darker than the skin, longer
             and darker the stronger they are.

    python3 source/agelines.py PHOTO.jpg [PHOTO2.jpg ...]        print each photo's depths (a look at the numbers)

Map: measure 35 | strength 159 | draw 238
"""
import json
import os

import numpy as np

LINES = ('nasolabial', 'crows_feet', 'eye_bags', 'forehead', 'marionette', 'cheek_hollow')


# ---------------------------------------------------------------------------------------------- measure
def measure(crop, mask, q, ipd):
    """Each crease's depth in one photo. crop: the segmentation crop (PIL); mask: its labels (3 face skin, 5 glasses,
    1 hair); q(i): landmark i in the crop's pixels; ipd: the eye gap in pixels."""
    from scipy import ndimage
    g = np.asarray(crop.convert('L')).astype(float)
    g = ndimage.gaussian_filter(g, max(0.8, 0.012 * ipd))
    skin = mask == 3
    bad = ndimage.binary_dilation(~skin, iterations=max(2, int(0.025 * ipd)))   # glasses, hair, edges: never sampled
    ok = ~bad
    tone = float(np.median(g[skin])) if skin.any() else 128.0

    def at(pts):
        pts = np.asarray(pts, float)
        v = ndimage.map_coordinates(g, [pts[:, 1], pts[:, 0]], order=1, mode='nearest')
        good = ndimage.map_coordinates(ok.astype(float), [pts[:, 1], pts[:, 0]], order=0, mode='constant') > 0.5
        return v, good

    def valley(c, n, lo, hi, d=0.045):
        """Deepest valley on the line c + t*n (t in lo..hi eye gaps): (depth, t) or (None, None)."""
        ts = np.linspace(lo, hi, 25)
        best = (None, None)
        for t in ts:
            p0 = c + t * ipd * n
            vals, good = at([p0 - d * ipd * n, p0, p0 + d * ipd * n])
            if not good.all():
                continue
            dep = (0.5 * (vals[0] + vals[2]) - vals[1]) / tone
            if best[0] is None or dep > best[0]:
                best = (dep, t)
        return best

    er, el = (q(33) + q(133)) / 2, (q(362) + q(263)) / 2
    ax = (el - er) / np.linalg.norm(el - er)
    ay = np.array([-ax[1], ax[0]])
    out, path = {}, {}

    def med(v):
        v = [x for x in v if x is not None]
        return (float(np.median(v)), len(v)) if len(v) >= 3 else (None, len(v))

    # nasolabial: rows from the nose wing's top to below the mouth corner; across each row, outward from the wing
    deps, offs = [], []
    for side, wing, corner in ((-1, 129, 61), (1, 358, 291)):
        W, M = q(wing), q(corner)
        out_dir = side * ax
        for k in np.linspace(0.0, 1.15, 10):
            base = W + (M - W) * k
            dep, t = valley(base, out_dir, 0.02, 0.32)
            deps.append(dep)
            if dep is not None:
                offs.append((side, round(float(k), 2), round(float(t), 3)))
    out['nasolabial'], _ = med(deps)
    path['nasolabial'] = offs
    # crow's feet: columns beside the outer eye corner, each searched up and down for a dark line
    deps = []
    for side, corner in ((-1, 33), (1, 263)):
        E = q(corner)
        for a in np.linspace(0.08, 0.3, 8):
            c = E + side * a * ipd * ax
            deps.append(valley(c, ay, -0.12, 0.16, d=0.03)[0])
    out['crows_feet'], _ = med(deps)
    # eye bags: under each lower lid, searched downward
    deps = []
    for side, lid, centre in ((-1, 145, er), (1, 374, el)):
        Lp = q(lid)
        for a in np.linspace(-0.12, 0.15, 7):
            c = Lp + side * a * ipd * ax
            deps.append(valley(c, ay, 0.10, 0.34, d=0.04)[0])   # (from 0.10: the lid margin is not a bag)
    out['eye_bags'], _ = med(deps)
    # forehead: columns across the forehead, from above the brows up to the hairline (skin only)
    deps = []
    mid_brow = (q(66) + q(296)) / 2
    for a in np.linspace(-0.45, 0.45, 9):
        c = mid_brow + a * ipd * ax
        deps.append(valley(c, -ay, 0.12, 0.6, d=0.04)[0])
    out['forehead'], _ = med(deps)
    # marionette: rows down from each mouth corner, searched outward
    deps = []
    for side, corner in ((-1, 61), (1, 291)):
        M = q(corner)
        for k in np.linspace(0.05, 0.4, 6):
            c = M + k * ipd * ay
            deps.append(valley(c, side * ax, -0.05, 0.2)[0])
    out['marionette'], _ = med(deps)
    # cheek hollow: under the cheekbone, between the fold and the face's edge, searched downward
    deps = []
    for side, bone in ((-1, 116), (1, 345)):
        B = q(bone)
        for a in np.linspace(-0.1, 0.1, 5):
            c = B + a * ipd * ax
            deps.append(valley(c, ay, 0.05, 0.45, d=0.07)[0])
    out['cheek_hollow'], _ = med(deps)
    # plain skin's own reading: the same search on the smooth mid-cheeks, both ways. Every depth is taken less this,
    # so lighting, skin texture and a dark skin's lower brightness do not read as lines (Badenoch read 1.25 without)
    ctrl = []
    for i in (50, 280, 205, 425):
        c = q(i)
        ctrl += [valley(c, ax, -0.06, 0.06)[0], valley(c, ay, -0.06, 0.06)[0]]
    base, _ = med(ctrl)
    base = base or 0.0
    for k in list(out):
        if out[k] is not None:
            out[k] = out[k] - base
    out['_plain'] = base
    out['_path'] = path
    return out


def measure_photo(path, n=None):
    """measure() on a photo file (the face the likeness check would use)."""
    import likeness as LK
    im, faces = LK.find_faces(path)
    if not faces:
        return None
    face = faces[n if n is not None else int(np.argmax([f['box'][1][0] - f['box'][0][0] for f in faces]))]
    crop, mask, box = LK.segment(im, face)
    P = face['P']
    kx, ky = 512 / (box[2] - box[0]), 512 / (box[3] - box[1])
    q = lambda i: np.array([(P[i, 0] - box[0]) * kx, (P[i, 1] - box[1]) * ky])
    ipd = float(np.linalg.norm((q(33) + q(133)) / 2 - (q(362) + q(263)) / 2))
    return measure(crop, mask, q, ipd)


# ---------------------------------------------------------------------------------------------- strength
CACHE = os.path.expanduser('~/.cache/agelines3.json')     # (3: eye bags searched from 0.10; 2: depths less plain skin's own reading)


def cached(path):
    """measure_photo with a cache by file and date (the line-up's photos are measured once)."""
    try:
        c = json.load(open(CACHE))
    except Exception:
        c = {}
    key = f'{os.path.abspath(path)}@{int(os.path.getmtime(path))}'
    if key not in c:
        try:
            m = measure_photo(path)
        except Exception:
            m = None
        c[key] = {k: v for k, v in m.items() if k != '_path'} if m else None
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        json.dump(c, open(CACHE, 'w'))
    return c[key]


# How deep each crease must be to start showing (LO) and to be drawn at full strength (HI), as a share of the skin's
# brightness, less plain skin's own reading: set on 14 Nov from 19 front photos of 15 people (Burnham, Badenoch,
# Walliams, Trump, Putin, Damon ...): LO about the 30th percentile of the sharp photos, HI about the 85th. Absolute,
# not against the line-up's median: a cartoon with no lines reads as a child, so an average adult gets faint ones.
# Blurred or small photos read shallow: give the person's sharpest front photos.
LO = dict(nasolabial=0.03, crows_feet=0.02, eye_bags=0.08, forehead=0.02, marionette=0.03, cheek_hollow=0.02)
HI = dict(nasolabial=0.12, crows_feet=0.08, eye_bags=0.25, forehead=0.12, marionette=0.11, cheek_hollow=0.07)


def age_factor(age):
    """The person's age (public record, given with --says age=N) scales every line: a photo's light can deepen a
    46-year-old's folds past a 56-year-old's (Badenoch's top light, 14 Nov). 30 -> 0.4, 46 -> 0.75, 56 -> 1.0,
    70 -> 1.2; unknown -> 1 (the photos alone)."""
    if not age:
        return 1.0
    return float(np.clip(0.4 + (float(age) - 30) * 0.6 / 26, 0.3, 1.25))


def strength(depths, others=()):
    """0..1.25 per line from the person's depths (LO -> 0, HI -> 1). others: the line-up's depths, only to say
    where the person stands (rank), never to scale."""
    s = {}
    for k in LINES:
        v = depths.get(k)
        s[k] = 0.0 if v is None else float(np.clip((v - LO[k]) / (HI[k] - LO[k]), 0.0, 1.25))
    return s


def rank(depths, others):
    """Per line: how many of the others' depths this person's beats, as 'n of m'."""
    r = {}
    for k in LINES:
        o = [x[k] for x in others if x and x.get(k) is not None]
        v = depths.get(k)
        r[k] = f'{sum(v > x for x in o)} of {len(o)}' if v is not None else '-'
    return r


def person(photos, others, age=None):
    """The age lines for one person: the median depth over their front photos, the strength against the line-up,
    and the nasolabial fold's path (how far out it sits) from the photos."""
    ms = [m for m in (measure_photo(*p) if isinstance(p, tuple) else measure_photo(p) for p in photos) if m]
    def top2(v):                                 # light hides a crease more often than it invents one: the mean of
        v = sorted(v)[-2:]                       # the two deepest photos
        return float(np.mean(v)) if v else None
    depths = {k: top2([m[k] for m in ms if m.get(k) is not None]) for k in LINES}
    offs = [t for m in ms for (_, _, t) in m['_path'].get('nasolabial', [])]
    k = age_factor(age)
    st = {key: min(1.25, v * k) for key, v in strength(depths).items()}
    return dict(depth={k: (round(v, 4) if v is not None else None) for k, v in depths.items()},
                strength={k: round(v, 2) for k, v in st.items()},
                rank=rank(depths, [cached(o) for o in others]) if others else {},
                age=age, age_factor=round(k, 2),
                fold_out=round(float(np.median(offs)), 3) if offs else 0.12)


# ---------------------------------------------------------------------------------------------- draw
def draw(p, f, L, skin, age, ink=None):
    """The age lines on a front head (patriots4_cast's Face f and layout L), after the nose and before the lips.
    age: person()'s dict (or just {'strength': {...}}). Nothing is drawn for a line of strength under 0.15."""
    from ed import open_curve as curve      # (ed.curve is closed: a line on it doubles back)
    st = age.get('strength', age)
    dk = lambda c, k: tuple(int(v * k) for v in c)
    ew, ecx, ey, eh = L['ew'], L['ecx'], L['eye_y'], L['eh']
    nw, ny, mw = L['nw'], L['nose_y'], L['mw']
    lipm = (L['lip0'] + L['lip13']) / 2

    def pen(s):
        s = min(1.0, s)
        return (ink or dk(skin, 0.70 - 0.16 * s)), 1.9 + 1.2 * s

    s = st.get('nasolabial', 0)
    if s >= 0.15:                                    # from above the nose wing, out and down round the mouth corner,
        c, w = pen(s)                                # as far out as the photo's own fold (fold_out, in eye gaps)
        fo = float(np.clip(age.get('fold_out', 0.12) * 2 * ecx, 0.03, 0.08))
        reach = lipm + 0.015 + 0.045 * min(1.0, s)
        wing = nw * 0.5
        for sg in (-1, 1):
            out = max(wing, mw / 2)                  # a bracket: out past the wing, back in under the mouth corner
            pts = [(sg * (wing + 0.008), ny - 0.075), (sg * (wing + fo * 0.7), ny - 0.025),
                   (sg * (out + fo), (ny + lipm) / 2 + 0.01), (sg * (mw / 2 + fo * 0.55), reach)]
            p.line(curve(f.pts(pts), 4), c, w)
    s = st.get('crows_feet', 0)
    if s >= 0.15:                                    # two or three short lines fanning out past the outer eye corner
        c, w = pen(s)
        n = 2 if s < 0.6 else 3
        ln = 0.035 + 0.03 * min(1.0, s)
        for sg in (-1, 1):
            x0 = sg * (ecx + ew * 0.78)
            for ang in ((-0.45, 0.05, 0.5) if n == 3 else (-0.3, 0.35)):
                a0 = (x0, ey + ang * 0.025)
                a1 = (x0 + sg * ln, ey + ang * 0.025 + ang * ln * 0.8)
                p.line(f.pts([a0, a1]), c, w * 0.8)
    s = st.get('eye_bags', 0)
    if s >= 0.15:                                    # a shallow arc under each lower lid
        c, w = pen(s)
        dy = eh / 2 + 0.022 + 0.014 * min(1.0, s)
        for sg in (-1, 1):
            cx = sg * ecx
            pts = [(cx - sg * ew * 0.28, ey + dy - 0.004), (cx + sg * ew * 0.05, ey + dy + 0.012),
                   (cx + sg * ew * 0.42, ey + dy - 0.002)]
            p.line(curve(f.pts(pts), 4), c, w * 0.85)
    s = st.get('forehead', 0)
    if s >= 0.15:                                    # one to three gentle lines across the forehead (hair covers some)
        c, w = pen(s)
        n = 1 + int(min(1.0, s) * 2.2)
        for i in range(n):
            y = L['brow_y'] - 0.06 - 0.035 * i
            hw = L['fhw'] * (0.22 - 0.03 * i)
            pts = [(-hw, y + 0.006), (-hw * 0.3, y - 0.004), (hw * 0.3, y - 0.004), (hw, y + 0.006)]
            p.line(curve(f.pts(pts), 4), c, w * 0.8)
    s = st.get('marionette', 0)
    if s >= 0.15:                                    # short lines down and out from the mouth corners
        c, w = pen(s)
        for sg in (-1, 1):
            x0 = sg * (mw / 2 + 0.012)
            p.line(f.pts([(x0, L['lip13'] + 0.01), (x0 + sg * 0.012, L['lip13'] + 0.03 + 0.04 * min(1.0, s))]), c, w * 0.85)
    s = st.get('cheek_hollow', 0)
    if s >= 0.15:                                    # a soft stroke under the cheekbone, out by the face's side
        c, w = pen(s * 0.8)
        for sg in (-1, 1):
            x0 = sg * (L['fw'] * 0.5 - 0.06)
            pts = [(x0, ey + 0.15), (x0 - sg * 0.025, ey + 0.22), (x0 - sg * 0.03, ey + 0.27)]
            p.line(curve(f.pts(pts), 4), c, w * 0.8)


if __name__ == '__main__':
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    for a in sys.argv[1:]:
        m = measure_photo(a)
        print(os.path.basename(a), {k: (round(v, 4) if v is not None else None) for k, v in (m or {}).items()
                                    if k != '_path'})
