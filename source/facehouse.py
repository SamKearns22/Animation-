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

LIKENESS (chat 8): the person's lines may also name push/tune (caricature(): each measure moved further from real
    faces' middle; Sam: "careful, you're straying too hard into caricature territory": keep push near 1.15), lashes,
    eye_scale, iris_r/pupil_r/iris_c (the iris's colour), lid (a heavier upper lid: calm, not wide), brow_up/brow_arch/brow_taper, mouth (the house mouths, AV.vance_mouth: soft, grin,
    smirk; wide, gap, creases, drop), forehead (hairline lifted), plait_k (each plait bigger).
    shape (chat 9): the face's outline traced off the front photos, row by row (`facehouse.py trace NAME OUT.jpg`
    measures it into the pick and lays it over each photo); the house outline otherwise.
    brows (chat 10, Sam: Kemi's brows "really far from her eyes"; why: the face tool's height was honest, 52 sat on
    her sharp photo's brow, but the pick's push (0.68 -> 0.80), chat 9's arch lifting the WHOLE brow and the heavier
    lid lowering the lid line added up to about twice her gap): `facehouse.py brows NAME OUT.jpg` measures each front
    photo's brow middle and peak in the pixels (eyes under 40 px wide only when nothing sharper), saves them into the
    pick ('brow'), and lays the drawn brows over each photo; with 'brow' in the pick the brows are drawn at her
    height and peak (face_layout), and the arch bends the ends down. Run it on every new face.

IN THE PEOPLE KIT (chat 11): a people file says `head: house NAME, hair PIECE, look LOOK` and `house: brow_thick
    0.032 | lid 0.24 | shape` (CAST's lines are the defaults for that face); people.py builds it with person() here.
    TURNED (chat 11): three-quarter, side and behind through turnhead (install_turned, _turn_person): the measured
    face carried round, its age lines and glasses; swept: grey clipped back and sides, the dark top and quiff carried
    round; braids: the crown's plaits running back over the skull, curtains hanging behind the ear (arched tops: sharp
    corners inked as spikes), one curtain across the back from behind. Kittest facehouse_whole_head.

    python3 source/facehouse.py turns OUT.jpg NAME [NAME ...]   each person turned, front to behind, big
    python3 source/facehouse.py sheet OUT.jpg NAME [NAME ...]   the design sheet: photo, the pick, both house looks
    python3 source/facehouse.py head NAME LOOK OUT.png             one head-and-shoulders (for the name test)
    python3 source/facehouse.py brows NAME OUT.jpg                 the brows measured on the photos, the drawing laid over

Map: reading the pick 67 | the traced outline 81 | the brows checked 156 | colours 270 | the head 290 (layout 294) |
     hair: swept 400, braids 436 (measured hair 437, crown 528, plaits 552, behind the neck 583, collar 604, the
     piece 615) | glasses 645 | age lines 675 | the person 725 | sheet 799 | main 874
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
def pick_dir(name, src=None):
    """Where a face's pick lives: Sam's pick (references/faces/NAME/pick), or `src`, facepick's own folder while he
    has not picked yet (its sheet draws A, B and C the house way: chat 13)."""
    return src or os.path.join(ROOT, 'references', 'faces', name, 'pick')


def pick_file(name, src=None):
    return os.path.join(pick_dir(name, src), f'{name}-pick.json')


def load(name, src=None, variant=None):
    """Sam's pick: its tuned measures, colours, glasses, age-line strengths and eyes; `variant` A, B or C draws that
    head of facepick's three instead (from `src`, facepick's folder)."""
    d = json.load(open(pick_file(name, src)))
    v = variant or d.get('picked', 'C')
    h = d['heads'][v]
    return dict(name=name, meas=dict(h['measures']), col=d['colours'], glasses=d.get('glasses'),
                age=d.get('age') or {}, eyes=d.get('eyes') or {}, picked=v, outline=d.get('outline'),
                brow=d.get('brow'), src=src, beard=d.get('beard') or None)


# ---------------------------------------------------------------------------------------------- the traced outline
TV = (0.0, 0.08, 0.16, 0.25, 0.33, 0.43, 0.52, 0.6, 0.7, 0.82, 0.9, 0.965, 1.0)    # the rows traced (face heights)


def _skin_rows(path):
    """One front photo's face, row by row: the face-skin's half width at each TV row and the chin's foot, in the
    house's fractions (0 the face mesh's forehead point, 1 its chin point; the face turned upright first)."""
    import likeness as LK
    from scipy import ndimage
    im, fc = LK.pick_face(path)
    crop, mask, (x0, y0, x1, y1) = LK.segment(im, fc)
    P = (fc['P'][:, :2] - [x0, y0]) * [512 / (x1 - x0), 512 / (y1 - y0)]
    a, b = P[10], P[152]
    hh, ang = np.hypot(*(b - a)), math.atan2(b[0] - a[0], b[1] - a[1])
    lab, _ = ndimage.label(mask == 3)                    # face skin, the piece holding the nose tip
    ys, xs = np.nonzero(lab == lab[int(P[1][1]), int(P[1][0])])
    qx, qy = xs - a[0], ys - a[1]
    u = (qx * math.cos(ang) - qy * math.sin(ang)) / hh
    v = (qx * math.sin(ang) + qy * math.cos(ang)) / hh
    rows = []
    for t in TV:
        s = np.abs(v - t) < 0.006
        rows.append(float((u[s].max() - u[s].min()) / 2) if s.sum() > 3 else float('nan'))
    return dict(rows=rows, foot=float(v.max()), path=path, P=fc['P'], ang=ang)


def trace(name, out=None):
    """The face's outline traced off the person's front photos (Sam, chat 9: "looking at your face on references
    would help"): each photo's face skin (likeness.segment) measured row by row, the middle value of the photos kept
    per row (an ear showing, plaits over a temple or an open mouth in one photo is outvoted). Saved into the pick as
    'outline'; the person's lines draw it with `shape=True`. OUT: the outline laid over each front photo."""
    f = pick_file(name)
    d = json.load(open(f))
    got = [_skin_rows(os.path.join(ROOT, p)) for p in d['fronts']]
    rows = [float(np.nanmedian([g['rows'][i] for g in got])) for i in range(len(TV))]
    tr = dict(rows=[[t, round(w, 4)] for t, w in zip(TV, rows)], foot=round(float(np.median([g['foot'] for g in got])), 4),
              photos=d['fronts'])
    d['outline'] = tr
    json.dump(d, open(f, 'w'), indent=1)
    if out:
        overlay(name, got, tr, out)
    return tr


def overlay(name, got, tr, out, T=420):
    """Each front photo with the traced outline (yellow) and the house outline it replaces (thin blue) laid over."""
    from PIL import Image, ImageDraw
    L = P4.layout(load(name)['meas'])
    old = PP._outline(L, -0.3)
    new = face_outline(dict(L, trace=tr), -0.3)
    tiles = []
    for g in got:
        im = Image.open(g['path']).convert('RGB')
        P = g['P'][:, :2]
        a, b = P[10], P[152]
        hh, ca, sa = np.hypot(*(b - a)), math.cos(g['ang']), math.sin(g['ang'])
        to = lambda uv: [(a[0] + hh * (u * ca + v * sa), a[1] + hh * (-u * sa + v * ca)) for u, v in uv]  # noqa: E731
        k = max(2, int(hh / 120))
        dr = ImageDraw.Draw(im)
        o = to(old)
        dr.line(o + o[:1], fill=(70, 150, 255), width=k)
        n = to(curve(new, 4))
        dr.line(n + n[:1], fill=(255, 220, 0), width=2 * k)
        c = (a + b) / 2
        tiles.append(im.crop((int(c[0] - hh), int(c[1] - 1.15 * hh), int(c[0] + hh), int(c[1] + 0.85 * hh))).resize((T, T)))
    sheet = Image.new('RGB', (len(tiles) * (T + 10) - 10, T), (255, 255, 255))
    for i, t in enumerate(tiles):
        sheet.paste(t, (i * (T + 10), 0))
    sheet.save(out, quality=90)
    return out


HOUSE_SKIN = [(246, 208, 188), (240, 196, 178), (226, 184, 150), (176, 120, 86), (120, 78, 56)]   # people.COLOURS


# ---------------------------------------------------------------------------------------------- the brows checked
def _photo_brows(path):
    """One front photo's brows: each brow's MIDDLE LINE over the eye's middle above the upper lid (159 / 386), and
    where the brow PEAKS, found in the pixels (the darkest band in each column, searched round the mesh's brow
    points, which are a stock shape, not hers), both in eye widths; the points to lay the drawing over. In a small
    photo (an eye under SHARP pixels wide) the brow is a blur of 3 or 4 pixels: its middle is the mesh's (between 52
    and 105 / 282 and 334) and the photo counts only when no sharp one does (chat 10: Kemi's two small photos put 52
    mid-brow). The middle line, not the lower edge: the shadow between brow and lid passes for brow in the pixels."""
    from scipy import ndimage
    import likeness as LK
    im, fc = LK.pick_face(path)
    P = fc['P'][:, :2]
    g = ndimage.gaussian_filter(np.asarray(im.convert('L')).astype(float), 1.0)
    out = []
    for (low, hi), lid, (i0, i1), top_i, under_i in (((52, 105), 159, (133, 33), (107, 66, 105, 63, 70), (55, 65, 52, 53, 46)),
                                                     ((282, 334), 386, (362, 263), (336, 296, 334, 293, 300), (285, 295, 282, 283, 276))):
        ew = float(np.hypot(*(P[i0] - P[i1])))
        ec = (P[i0] + P[i1]) / 2
        out_dir = np.sign(P[i1][0] - P[i0][0])
        tx, ty = P[list(top_i)].T
        ux, uy = P[list(under_i)].T
        o = np.argsort(tx)
        o2 = np.argsort(ux)
        band = []
        for x in range(int(min(tx.min(), ux.min())), int(max(tx.max(), ux.max())) + 1):
            ya = int(np.interp(x, tx[o], ty[o]) - 0.25 * ew)
            yb = int(np.interp(x, ux[o2], uy[o2]) + 0.15 * ew)
            col = g[max(0, ya):yb, max(0, x - 1):x + 2].mean(1)
            if len(col) > 2:
                c = int(np.argmin(col))
                half = (col[c] + np.median(col)) / 2
                e = c
                while e < len(col) - 1 and col[e] < half:
                    e += 1
                band.append((x, max(0, ya) + c, max(0, ya) + e))
        xs, cs, es = np.array(band, float).T
        cs = ndimage.uniform_filter1d(cs, max(3, int(0.15 * ew)))
        k = int(np.argmin(cs))
        sharp = ew >= SHARP
        mid = np.abs(xs - ec[0]) < max(2, 0.08 * ew)
        cm = (P[low] + P[hi]) / 2
        cy = float(np.median(cs[mid])) if sharp and mid.any() else float(cm[1])
        out.append(dict(high=float((P[lid][1] - cy) / ew), peak=float(out_dir * (xs[k] - ec[0]) / ew), sharp=sharp,
                        ew=ew, ec=ec, lid=P[lid], low=(float(ec[0]) if sharp else float(cm[0]), cy),
                        top=(float(xs[k]), float(cs[k]))))
    return im, P, out


SHARP = 40           # an eye at least this many pixels wide shows the brow's own edges


def browcheck(name, out=None):
    """The drawn brows against the person's own (chat 10, Sam on Kemi: "her eyebrows are really far from her eyes";
    the arch had lifted the whole brow and a heavier lid had lowered the lid line). Prints, in eye widths, the gap
    from the upper lid to the brow's middle line on each front photo and in the drawing, and where each peaks; saves
    the photos' middle values into the pick as 'brow' (the drawing reads the peak). OUT: the drawing's brows and lids
    (yellow, blue) laid over each photo, eye on eye; red: the photo's brow middle over each eye; white: its peak."""
    from PIL import Image, ImageDraw
    f = pick_file(name)
    d = json.load(open(f))
    got = [_photo_brows(os.path.join(ROOT, p)) for p in d['fronts']]
    sides = [b for _, _, bs in got for b in bs]
    sides = [b for b in sides if b['sharp']] or sides             # the small photos only when nothing sharper
    photo = dict(high=round(float(np.median([b['high'] for b in sides])), 3),
                 peak=round(float(np.median([b['peak'] for b in sides])), 3), photos=d['fronts'])
    d['brow'] = photo
    json.dump(d, open(f, 'w'), indent=1)
    sp = person(name, 'detail', **CAST.get(name, {})) if name in CAST else None
    kh = sp['kit_house'] if sp else dict(load(name), brow=photo)
    L = face_layout(kh)
    br = curve(P4.brow_uv(L, kh.get('brow_thick', 0.05), 0.0, 0.0, kh.get('brow_arch', 0.0), kh.get('brow_taper', 0.0),
                          _peak(kh)), 3)
    lid = kh.get('lid', LID0)
    drawn = dict(high=round(_brow_gap(L, kh), 3),
                 peak=round((min(br, key=lambda q: q[1])[0] - L['ecx']) / L['ew'], 3))
    lines = [f"{os.path.basename(p)}: brows {', '.join(f'{b['high']:.2f}' for b in bs)} eye widths above the lid; "
             f"peak {', '.join(f'{b['peak']:+.2f}' for b in bs)}{'' if bs[0]['sharp'] else ' (small: eye under 40 px)'}" for (p, (_, _, bs)) in zip(d['fronts'], got)]
    lines.append(f"photos' middle: {photo['high']:.2f} above the lid, peak {photo['peak']:+.2f}; the drawing: "
                 f"{drawn['high']:.2f}, peak {drawn['peak']:+.2f} ({drawn['high'] - photo['high']:+.2f} eye widths)")
    if out:
        T = 520
        tiles = []
        for (im, P, bs) in got:
            im = im.copy()
            dr = ImageDraw.Draw(im)
            (cr, cl) = bs[0]['ec'], bs[1]['ec']                 # the photo's eye centres: person's right, left
            s = float(np.hypot(*(cl - cr))) / (2 * L['ecx'])
            ang = math.atan2(cl[1] - cr[1], cl[0] - cr[0])
            mid = (cr + cl) / 2
            ca, sa = math.cos(ang), math.sin(ang)
            to = lambda q: [(mid[0] + s * (u * ca - (v - L['eye_y']) * sa), mid[1] + s * (u * sa + (v - L['eye_y']) * ca)) for u, v in q]  # noqa: E731
            k = max(1, int(bs[0]['ew'] / 40))
            for sgn in (-1, 1):                                  # sgn -1: our left on screen = person's right
                b = to([(sgn * u, v) for u, v in br])
                dr.line(b + b[:1], fill=(255, 225, 0), width=2 * k)
                us = np.linspace(-1, 1, 15)
                ln = to([(sgn * L['ecx'] + L['ew'] / 2 * t, L['eye_y'] - L['eh'] / 1.8 * (1 - t * t) * (1 - lid)) for t in us])
                dr.line(ln, fill=(60, 170, 255), width=k)
            for b in bs:
                x, y = b['low']
                dr.ellipse((x - 2 * k, y - 2 * k, x + 2 * k, y + 2 * k), fill=(255, 40, 40))
                px, py = b['top']
                dr.ellipse((px - 2 * k, py - 2 * k, px + 2 * k, py + 2 * k), outline=(255, 255, 255), width=k)
            w = float(np.hypot(*(cl - cr)))
            tiles.append(im.crop((int(mid[0] - 1.25 * w), int(mid[1] - 0.95 * w), int(mid[0] + 1.25 * w), int(mid[1] + 0.45 * w)))
                         .resize((T, int(T * 1.4 / 2.5))))
        sheet = Image.new('RGB', (len(tiles) * (T + 8) - 8, tiles[0].height), (255, 255, 255))
        for i, t in enumerate(tiles):
            sheet.paste(t, (i * (T + 8), 0))
        sheet.save(out, quality=90)
        lines.append(out)
    return '\n'.join(lines)


# ---------------------------------------------------------------------------------------------- colours
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
EYE_OPEN_MIN = 0.2   # chat 13: Walliams' smiling photos tuned his eyes to 0.08 open: shut, at phone size a line.
                     # The house eye never opens less (real faces' middle 0.31; Andy's 0.26 untouched)
LID0 = 0.12          # the house's resting upper lid (P4.eyes' lid4) that the measured brow height was laid out against


def face_layout(kh):
    """The layout the head is drawn on: the pick's measures, the brows kept their measured height above the lid AS
    DRAWN (chat 10: a heavier lid, `lid`, lowers the lid line; the brows used to stay put, so the gap grew)."""
    meas = dict(kh['meas'])
    meas['eye_open'] = max(meas.get('eye_open', EYE_OPEN_MIN), EYE_OPEN_MIN)
    L = P4.layout(meas)
    L['brow_y'] += L['eh'] / 1.8 * (kh.get('lid', LID0) - LID0)
    if (kh.get('brow') or {}).get('high'):                 # browcheck() measured the photos: the brows sit as hers
        L['brow_y'] += (_brow_gap(L, kh) - kh['brow']['high']) * L['ew']
    return L


def _brow_gap(L, kh):
    """The drawn brow's middle line over the eye's middle, above the drawn upper lid, in eye widths."""
    br = curve(P4.brow_uv(L, kh.get('brow_thick', 0.05), 0.0, 0.0, kh.get('brow_arch', 0.0), kh.get('brow_taper', 0.0),
                          _peak(kh)), 3)
    cut = [v0 + (v1 - v0) * (L['ecx'] - u0) / (u1 - u0) for (u0, v0), (u1, v1) in zip(br, br[1:] + br[:1])
           if (u0 - L['ecx']) * (u1 - L['ecx']) < 0]
    lid_top = L['eye_y'] - L['eh'] / 1.8 * (1 - kh.get('lid', LID0))
    return (lid_top - (max(cut) + min(cut)) / 2) / L['ew']


def _peak(kh):
    """Where the brow peaks (eye widths out from the eye's middle): the photos' own (browcheck()) where measured."""
    b = kh.get('brow') or {}
    return b.get('peak', 0.21) if kh.get('brow_arch') else 0.21


def house_head(img, p, sp, t, hx, hy):
    """The people kit's head part 'house': sp['kit_house'] holds the pick (load()), the look and the hair piece."""
    with PP._Big():
        return _head(img, p, sp, t, hx, PP._lift(hy))


def _head(img, p, sp, t, hx, hy):
    kh = sp['kit_house']
    lk = LOOKS[kh['look']]
    L = face_layout(kh)
    if kh.get('shape') and kh.get('outline'):               # the outline traced off the front photos (trace())
        L['trace'] = kh['outline']
    f = P4.Face(hx, hy)
    skin = sp['skin']
    hc = sp['hair_c']
    piece = kh['hair']
    if piece == 'braids':
        braids_behind(p, f, L, hc, kh, sp)
    if piece != 'braids':                                 # her plaits cover the ears
        AV._ears(p, f, L, skin)
    o = curve(f.pts(face_outline(L, -0.42 if piece != 'braids' else _hair(L, kh)['crown'] + 0.06)), 4)
    p.poly(o, skin, INK, 2.6)
    if lk['sockets'] and kh['eyes'].get('shade', 0) >= 0.1:
        sockets(p, f, L, skin, kh['eyes']['shade'])
    ey = kh['eyes']
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', kh.get('lid', 0.12))), tuple(kh.get('iris_c') or ey.get('iris') or (66, 46, 34)), dk(skin, 0.8),
            liner=2.8 + 1.6 * kh.get('lashes', 0.0), iris_r=kh.get('iris_r', min(1.15, ey.get('iris_r', 0.95))),
            pupil_r=kh.get('pupil_r', min(0.5, ey.get('pupil_r', 0.42))), scale=kh.get('eye_scale', 1.0))
    if kh.get('lashes'):
        lashes(p, f, L, sp, kh['lashes'], kh.get('eye_scale', 1.0))
    P4.brows(p, f, L, sp['brow_c'], kh.get('brow_thick', 0.05), sp.get('brow_up', 0.0), sp.get('frown', 0.0),
             kh.get('brow_arch', 0.0), kh.get('brow_taper', 0.0), _peak(kh))
    P4.nose(p, f, L, skin)
    age_lines(p, f, L, skin, kh['age'], lk)
    if kh.get('beard'):
        stubble(p, f, L, skin, kh['beard'])
    fx, my = f(0.0, L['lip13'])
    m = kh.get('mouth')
    if m:                                                 # the person's own resting mouth (chat 8: the likeness push)
        PP.AV.MC.TC.talk_or(p, dict(sp, lips=True, lip_c=kh['lip']), 0.0, fx, my - 6, lambda: PP.AV.vance_mouth(
            p, f, L, m['kind'], kh['lip'], skin, m.get('wide', 1.12), m.get('gap', 0.0), m.get('creases', 1.0), m.get('drop')))
    else:
        P4.lips(p, f, L, dict(sp, smile=sp.get('smile', 0.0)), kh['lip'], (fx, my - 6))
    if piece == 'swept':
        swept(p, f, L, hc, kh, lk)
    elif piece == 'braids':
        braids(p, f, L, hc, lk, kh)
        if kh.get('ears'):                                # over the plaits, as the pick drew them (K1: her width)
            AV._ears(p, f, L, skin)
    if kh.get('glasses'):
        glasses(p, f, L, kh['glasses'])
    return fx


def stubble(p, f, L, skin, bd, seed=61, ink=True):
    """A measured beard as the house draws stubble (blessed_walliams.beard made general, chat 13): a shade of the
    beard's colour the skin shows through along the jaw and round the chin, lighter where the photo's is grey-white,
    a darker band over the lip and round the mouth; the cheeks above the jaw stay skin. How far it comes up and how
    strong it is follow its measured coverage (beardkit: share of the lower face)."""
    col = bd['colour']
    k = float(np.clip(bd.get('coverage', 0.3) / 0.3, 0.6, 1.4))
    mid = blend(skin, col, 0.3 * k)
    light = blend(skin, tuple(min(255, c + 50) for c in col), 0.3 * k)
    must = blend(skin, tuple(int(c * 0.8) for c in bd.get('moustache') or col), 0.42 * k)
    fw, jw, ny, l0, l13, l17, mw, nw = L['fw'], L['jw'], L['nose_y'], L['lip0'], L['lip13'], L['lip17'], L['mw'], L['nw']
    jw = min(jw, fw * 0.98)
    o = face_outline(L)
    n = len(o)
    top_v = 0.66 - 0.06 * (k - 1)                         # a fuller beard comes further up the cheek
    i0 = next(i for i, q in enumerate(o) if q[0] > 0 and q[1] > top_v)
    i1 = next(i for i in range(n - 1, -1, -1) if o[i][0] < 0 and o[i][1] > top_v)
    low = o[i0:i1 + 1]
    uj = _face_u(L, top_v)
    cheek = [(-uj + 0.01, top_v), (-uj * 0.84, top_v + 0.07), (-mw * 0.8, l13), (-mw * 0.62, ny + 0.04),
             (0.0, ny + 0.035), (mw * 0.62, ny + 0.04), (mw * 0.8, l13), (uj * 0.84, top_v + 0.07), (uj - 0.01, top_v)]
    p.poly(f.pts(low + AV.tufts(cheek, 0.01, 0.014, out=1.0, seed=seed)), mid, None)
    chin = AV.tufts([(jw * 0.46, 0.8), (mw * 0.55, l17 + 0.06), (0.0, l17 + 0.075), (-mw * 0.55, l17 + 0.06),
                     (-jw * 0.46, 0.8)], 0.012, 0.016, out=-1.0, seed=seed + 1)
    p.poly(f.pts([q for q in low if abs(q[0]) < jw * 0.47 and q[1] > 0.78] + chin[::-1]), light, None)
    mt = l0 - 0.03
    mo = AV.tufts([(-mw * 0.6, l13 + 0.004), (-mw * 0.52, mt + 0.008), (-nw * 0.3, mt), (0.0, mt + 0.004),
                   (nw * 0.3, mt), (mw * 0.52, mt + 0.008), (mw * 0.6, l13 + 0.004)], 0.006, 0.012, out=1.0, seed=seed + 2)
    goat = [(mw * 0.6, l13 + 0.01), (mw * 0.3, l17 + 0.012), (mw * 0.14, l17 + 0.045), (0.0, l17 + 0.05),
            (-mw * 0.14, l17 + 0.045), (-mw * 0.3, l17 + 0.012), (-mw * 0.6, l13 + 0.01)]
    p.poly(f.pts(mo + AV.tufts(goat, 0.007, 0.012, out=-1.0, seed=seed + 3)), must, None)
    if ink:                                               # turned (turnhead's TurnFace): its own outline inks
        p.poly(curve(f.pts(face_outline(L)), 4), None, INK, 2.6)   # the jaw's ink line back over the shade


def lashes(p, f, L, sp, k, scale=1.0):
    """Long dark lashes along each upper lid, longest at the outer corner (chat 8: Burnham's, the cartoonists' cue);
    k (0..1) their length and count. The lid's curve is P4.eyes' own."""
    w = L['ew'] * P4.H / 2 * scale
    h = L['eh'] * P4.H / 1.8 * scale
    lid = sp.get('lid4', 0.12)
    for sgn in (-1, 1):
        ex, ey = f(sgn * L['ecx'], L['eye_y'])
        for u in np.linspace(0.05, 1.0, 3 + int(4 * k)):
            x, y = ex + sgn * w * u, ey - h * (1 - u * u) * (1 - lid)
            ln = (3 + 6 * k) * (0.6 + 0.6 * u)
            a = math.radians(100 - 55 * u)                # straight up at the middle, out at the corner
            p.line([(x, y), (x + sgn * ln * math.cos(a) * 0.5, y - ln * math.sin(a) * 0.6),
                    (x + sgn * ln * math.cos(a), y - ln * math.sin(a))], INK, 1.3 + 0.8 * k)


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
def _swept_shapes(L, kh, hc):
    """The swept hair's pieces in face units: the two clipped sides, the cap (tufted top and fringe) and the light."""
    e = L['fw'] * 0.5
    c = max(L['fhw'] * 0.5 + 0.02, e)
    hl = kh.get('hairline', -0.08)
    lift = kh.get('quiff', 0.06)                           # how much higher the sweep's side rises
    grey = kh.get('grey') or blend(hc, (150, 146, 142), 0.35)
    t = max(L['fhw'], L['fw'] * 0.9) * 0.5
    # chat 13: the clipped side's inner edge never stands off the face: on Walliams' narrower temples (0.026 off at
    # the cheek top) a white sliver showed between them; laid onto the face's own edge where it stands off over
    # 0.015 (Andy's sits 0.003 off: unchanged, held pixel for pixel)
    off = (t - 0.005) - _face_u(L, 0.12) > 0.015
    fu = lambda d, v: -min(t - d, _face_u(L, v) - 0.012) if off else d - t      # noqa: E731
    side = [(-c - 0.025, -0.22), (-c - 0.025, -0.1), (-e - 0.018, 0.06), (-e - 0.012, 0.26), (-e + 0.012, 0.29),
            (fu(0.005, 0.12), 0.12), (fu(0.03, -0.02), -0.02), (fu(0.06, -0.12), -0.12), (fu(0.08, -0.22), -0.22)]
    sides = [[(-u, v) for u, v in side] if sgn > 0 else side for sgn in (-1, 1)]
    top = [(-c - 0.03, -0.04), (-c - 0.04, -0.17), (-c + 0.0, -0.3), (-c * 0.6, -0.4), (-c * 0.15, -0.45 - lift * 0.3),
           (c * 0.3, -0.46 - lift * 0.8), (c * 0.68, -0.41 - lift), (c + 0.01, -0.3 - lift * 0.6), (c + 0.045, -0.16),
           (c + 0.035, -0.04)]
    front = [(c - 0.005, -0.04), (c - 0.05, -0.14), (c * 0.66, -0.16 + 0.02), (c * 0.42, hl - 0.01), (c * 0.12, hl + 0.015),
             (-c * 0.2, hl + 0.02), (-c * 0.48, hl + 0.005), (-c * 0.7, -0.13), (-c + 0.05, -0.14), (-c + 0.01, -0.04)]
    cap = AV.tufts(top, 0.005, 0.03, out=1.0, seed=31) + front
    return dict(c=c, hl=hl, lift=lift, grey=grey, sides=sides, cap=cap)


def _swept_strokes(p, f, hc, sh, lk):
    """The strokes brushed up and over, the light on the quiff, the grey flecks (the look 'detail')."""
    c, hl, lift, grey = sh['c'], sh['hl'], sh['lift'], sh['grey']
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


def swept(p, f, L, hc, kh, lk):
    """Short, thick hair brushed up and over to our right into a low quiff (Walliams' hand-made hair, made general):
    the cap as wide as the cheeks, rising higher on the sweep's side; the sides clipped close and greying."""
    sh = _swept_shapes(L, kh, hc)
    for sd in sh['sides']:
        p.poly(curve(f.pts(sd), 2), sh['grey'], INK, 2.2)
    p.poly(curve(f.pts(sh['cap']), 2), hc, INK, 2.4)
    _swept_strokes(p, f, hc, sh, lk)


# ---------------------------------------------------------------------------------------------- hair: braids
def pick_hair(name, picked='C', src=None):
    """The hair Sam picked, measured off the pick's picture (facepick traced it from the photos; chat 7, K1: the
    house cap was guessed, a head taller and narrower than the pick, and the head read long): its outer edge (half
    width at each row, both sides averaged) and the hairline over the forehead, in face units (facepick's canvas:
    Face(HX, HY), H face height, SC pixels per unit). None when there is no pick picture."""
    from PIL import Image
    from scipy import ndimage
    import facepick as FP
    png = os.path.join(pick_dir(name, src), f'{name}-{picked}.png')
    if not os.path.exists(png):
        return None
    col = json.load(open(pick_file(name, src)))['colours']
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


def face_outline(L, crown=-0.42):
    """The face's outline (fractions, crown first, round by our right): the house's (PP._outline, from the measured
    widths) or, where the person's lines say `shape`, the one traced off their front photos (trace()): its half widths
    row by row down to the chin's foot, the crown over the top as the house draws it."""
    tr = L.get('trace')
    if not tr:
        return PP._outline(L, crown)
    rows = [(w, v) for v, w in tr['rows']]
    w0 = rows[0][0]
    right = [(w0 * 0.7, crown * 0.6)] + rows + [(0.0, tr['foot'])]
    return [(0.0, crown)] + right + [(-u, v) for u, v in right[::-1][1:]]


def _face_u(L, v):
    """The face outline's half width at row v (our right side)."""
    r = [q for q in face_outline(L) if q[0] >= 0]
    r = sorted({round(q[1], 4): q for q in r}.values(), key=lambda q: q[1])
    return float(np.interp(v, [q[1] for q in r], [q[0] for q in r]))


VJ = 0.3                                     # where the crown's plaits become the curtains (about the eye line)
VS = np.linspace(VJ, 1.95, 40)               # the curtain's rows, top to bottom (fractions of the face height)


def _hair(L, kh):
    """The braids' shape: the measured hair (pick_hair) or, without one, a round cap; kept per head."""
    m = kh.get('_hair')
    if m is None:
        m = kh['_hair'] = pick_hair(kh['name'], kh.get('picked', 'C'), kh.get('src')) or {}
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
    up = kh.get('forehead', 0.0)                 # a higher forehead (chat 8): the hairline lifted, most at the middle
    hl = [(u, v - up * max(0.0, 1 - u / 0.4)) for u, v in hl]
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
    if sp.get('collar') == 'open':                          # the outfit's neckline, laid again over the redrawn
        open_collar(p, f.cx, yc, nw, skin, sp.get('shirt', (246, 246, 246)))   # neck (the torso leaves it: neck_redrawn)


open_collar, open_collar_three = PP.open_collar, PP.open_collar_three   # the outfit's (people_parts, chat 15)


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
    k = kh.get('plait_k', 1.0)                              # each plait that much bigger (Sam, chat 8: "slightly")
    n, step = max(3, round(n / k)), step * k
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


# ---------------------------------------------------------------------------------------------- turned views
HAIR = ('swept', 'braids')
TURN_PROF = {'swept': dict(hair_low=0.36, nape=0.62, volume=0.015),         # clipped short at the back
             'braids': dict(hair_low=0.5, nape=0.78, volume=0.05)}          # the plaits' bulk over the skull


class _Screen:
    """A frame that leaves points as they are: _band() drawn on paths already on screen (a curtain seen turned)."""
    def pts(self, uvs):
        return [tuple(q) for q in uvs]


def _turn_key(kh):
    import hashlib
    keep = {k: v for k, v in kh.items() if not k.startswith('_')}
    return 'house:%s:%s' % (kh['name'], hashlib.md5(repr(sorted(keep.items(), key=lambda q: q[0])).encode()).hexdigest()[:10])


def _turn_mood(sp, f):
    kh = sp['kit_house']
    up = sp.get('brow_up', 0.0)
    st = dict(lid=sp.get('lid4', kh.get('lid', LID0)), look=min(1.0, sp.get('look', 0.0) + 0.3), squint=0.0,
              closed=sp.get('blink', False), gaze_dy=-0.2)
    return st, (sum(up) / 2 if isinstance(up, tuple) else up), sp.get('frown', 0.0)


def _turn_mouth(p, f, L, sp, fx, my):
    kh = sp['kit_house']
    m = kh.get('mouth')
    if m:
        PP.AV.vance_mouth(p, f, L, m['kind'], kh['lip'], sp['skin'], m.get('wide', 1.12), m.get('gap', 0.0),
                          m.get('creases', 1.0), m.get('drop'))
    else:
        P4.lips(p, f, L, dict(sp, smile=sp.get('smile', 0.0), mouth='rest'), kh['lip'], (fx, my - 6))


def _turn_face(pen, f, L, sp):
    kh = sp['kit_house']
    age_lines(pen, f, L, sp['skin'], kh['age'], LOOKS[kh['look']])
    if kh.get('beard'):                                   # chat 14: the stubble carried round (as Vance's goatee)
        stubble(pen, f, L, sp['skin'], kh['beard'], ink=False)


def _turn_over(img, p, f, L, sp, view):
    kh = sp['kit_house']
    if kh.get('glasses') and view in ('three', 'side'):
        glasses(p, f, L, kh['glasses'])


def _turn_hair(img, p, f, L, sp):
    import turnhead as TH
    kh, hc = sp['kit_house'], sp['hair_c']
    lk = LOOKS[kh['look']]
    yaw = round(math.degrees(f.th))
    if kh['hair'] == 'swept':
        sh = _swept_shapes(L, kh, hc)
        TH.hair(img, p, f, [], sh['grey'], f.prof, 2.2)        # the clipped back and sides, greying
        if yaw <= 90:
            for sd in sh['sides']:
                p.poly(curve(f.pts(sd), 2), sh['grey'], INK, 2.2)
        top = dict(f.prof, hair_low=-0.16, nape=0.12, volume=0.03)   # the thick dark top over the crown, down the back
        fronts = [f.pts(TH.dense(curve(sh['cap'], 2)))] if yaw <= 90 else []
        mask = TH.hair(img, p, f, fronts, hc, top)
        if yaw <= 90:
            TH.clipped(img, p, mask, lambda pen: _swept_strokes(pen, f, hc, sh, lk))
    else:
        _turned_braids(img, p, f, L, sp, kh, hc, lk, yaw)


def _turned_braids(img, p, f, L, sp, kh, hc, lk, yaw):
    """The plaits from three-quarter, the side and behind: the crown's mass (the front's crown band carried round)
    with plaits running from the parting back over the skull, then the curtains hanging to the same length as the
    front's (VS's foot), behind the near ear and, from behind, across the whole back; plaits down each curtain."""
    import turnhead as TH
    H = TH.H
    light, sep, n, step, w = _looks(hc, lk)
    k = kh.get('plait_k', 1.0)
    n, step = max(3, round(n / k)), step * k
    hs = _hair(L, kh)
    sil = TH.silhouette(f, 0.02)
    near = {round(v, 2): x for x, y, v, part in sil if part == 'near'}
    far = {round(v, 2): x for x, y, v, part in sil if part == 'far'}
    foot = f.top + 1.97 * H
    vs = [v for v in sorted(near) if 0.06 <= v <= 0.75]      # its top tucked under the crown's mass
    # the curtains first (the crown closes over their tops)
    curt = []
    if yaw >= 135:                                               # behind: one curtain the whole back's width
        sw = lambda v: H * min(0.08, 0.005 + 0.25 * max(0.0, v - 0.06))   # widening from the crown's edge
        back = [(near[v] - sw(v), f.top + v * H) for v in vs]
        fr = [(far[v] + sw(v), f.top + v * H) for v in vs]
        bx, fx_ = back[-1][0] - H * 0.06, fr[-1][0] + H * 0.06
        curt.append((back + [(bx, foot)], fr + [(fx_, foot)]))
    else:
        reach = {45: 0.03, 90: 0.12}.get(yaw, 0.1) * H          # in front of the ear: over it
        ex = f.at(f.wrap(0.42, -100), 0.42, clamp=False)[0]   # the near ear's place
        back = [(near[v] - H * (0.005 + 0.3 * max(0.0, v - 0.06)), f.top + v * H) for v in vs]
        bx = back[-1][0] - H * 0.05
        front = [(ex + reach, f.top + v * H) for v in vs]
        curt.append((back + [(bx, foot)], front + [(ex + reach + H * 0.04, foot)]))
    head = [(x, y) for x, y, v, part in sil]
    for i, (a, b) in enumerate(curt):
        mid = ((a[0][0] + b[0][0]) / 2, a[0][1] - 0.12 * H)       # an arched top under the crown: no sharp
        a = [mid] + a                                            # corners (their ink stuck out as spikes)
        b = [mid] + b
        A, B = _resample(a, 50), _resample(b, 50)

        def draw(pen, A=A, B=B):
            pen.poly(curve([tuple(q) for q in A] + [tuple(q) for q in B[::-1]], 2), hc, INK, 2.4)
            _band(pen, _Screen(), 1, lambda t: B * (1 - t) + A * t, light, sep,
                  max(3, round(n * (1.6 if yaw >= 135 else 1.0))), step * H, w)
        if i:                                                    # the far curtain: only where the head is not
            _outside(img, p, head, draw)
        else:
            draw(p)
    # the crown: the hair's mass over the skull, the front's crown carried round where it is seen
    fronts = []
    if yaw <= 90:
        ci, co = _crown_paths(L, hs)
        band = [tuple(q) for q in co] + [tuple(q) for q in ci[::-1]]
        fronts = [f.pts(TH.dense(curve(band + [(-u, v) for u, v in band[::-1]], 2)))]
    mask = TH.hair(img, p, f, fronts, hc, dict(f.prof, hair_low=0.12, nape=0.16))   # ends above the cheekbones: the curtains take over

    def plaits(pen):
        lo, hi = f.visible(0.1)
        def merid(t):
            psi = lo + (hi - lo) * t
            out = []
            for v in np.linspace(hs['crown'] - 0.02, 0.62, 40):
                x, z = f.ring(psi, v)
                X, _ = f.view(float(x) * 1.04, float(z) * 1.04)
                out.append((f.cx + X * H, f.top + v * H))
            return np.array(out)
        _band(pen, _Screen(), 1, merid, light, sep, max(4, round(n * 1.4)), step * H, w)
    TH.clipped(img, p, mask, plaits)


def _outside(img, p, poly, draw):
    """draw(pen) kept OUTSIDE the head's outline (poly, head units): what hangs behind the far cheek."""
    from PIL import Image, ImageDraw
    import burnham as B
    base = p.pen if hasattr(p, 'pen') else p
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw(B.Pen(layer, base.cam))
    m = Image.new('L', img.size, 255)
    ImageDraw.Draw(m).polygon([base.cam.P(*q) for q in poly], fill=0)
    a = np.asarray(layer)[:, :, 3].astype(np.uint16) * np.asarray(m) // 255
    layer.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(layer)


def _turn_person(sp):
    import turnhead as TH
    kh = sp['kit_house']
    key = _turn_key(kh)
    if key not in TH.PEOPLE:
        L = face_layout(kh)
        prof = TH.fitted(L, -0.42, 1.06, **TURN_PROF[kh['hair']])
        w = TH.half_widths(P4.outline_uv(L, 0.4, crown=-0.42))     # the house outline's rows are few: between the
        wv = lambda v: float(np.interp(v, [q[0] for q in w], [q[1] for q in w]))   # crown's end and the temples
        c0 = prof['crown'][-1][1]                                   # the skull stepped in (a notch, spikes in the
        prof['crown'] = prof['crown'] + [(v, max(c0, wv(v))) for v in (0.15, 0.3, 0.43)]   # hair); held round here
        TH.register(TH.Person(key, lambda sp2, _kh=kh: face_layout(_kh), -0.42, 0.4, lambda L, _p=prof: _p,
                              sp['skin'], tuple(kh.get('iris_c') or kh['eyes'].get('iris') or (66, 46, 34)),
                              sp['brow_c'], kh['lip'], _turn_mood, _turn_mouth, _turn_hair, face=_turn_face,
                              over=_turn_over, brow_thick=kh.get('brow_thick', 0.05)))
    return key


def install_turned():
    """Once: a house head's turned views (three-quarter, side, three-quarter behind, behind) through its own turnhead
    Person: its measured face carried round the head, its colours, age lines and glasses, its hair piece turned;
    drawn at the house's bigger head size, lifted as the front is. Ears hidden under braids."""
    import turnhead as TH
    V = PP.AV.MC.V
    if getattr(V.head_view, 'kit_house', False):
        return
    old = V.head_view

    def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
        kh = sp.get('kit_house')
        if kh and view in TH.YAW:
            key = _turn_person(sp)
            with PP._Big():
                return TH.draw(img, p, dict(sp, who=key, ears_hidden=kh['hair'] == 'braids' and not kh.get('ears')),
                               t, view, hx, PP._lift(hy))
        return old(img, p, sp, t, view, hx, hy)
    head_view.kit_house = head_view.turnhead = True
    V.head_view = head_view


# ---------------------------------------------------------------------------------------------- the person
def caricature(meas, push=1.0, tune=None):
    """The caricaturist's push (chat 8, Sam: "we are allowed to play with face shapes in the house style"): each
    measure moved further from real faces' middle (P4.AVG), by push, times tune[measure] where a person's lines name
    one; push 1 and no tune is the pick as measured. What makes this face THIS face grows; nothing new is invented."""
    tune = tune or {}
    return {k: (P4.AVG[k] + push * tune.get(k, 1.0) * (v - P4.AVG[k])) if k in P4.AVG else v for k, v in meas.items()}


def person(name, look, hair, outfit=('suit', (31, 34, 58)), shirt=(246, 246, 246), tie=None, height=1.75, src=None,
           variant=None, collar=None, **kw):
    """The engine's person (views.person) for one picked face in one look, on the people kit's body; `src` and
    `variant`: one of facepick's three heads before Sam picks (load())."""
    import people
    pk = load(name, src, variant)
    lk = LOOKS[look]
    col = pk['col']
    skin = house_tone(col['skin'], lk['skin_k'])
    d = dict(who=name, name=name.title(), skin=skin, hair_style='none', hair_c=tuple(col['hair']), height=height,
             brows=tuple(col['brow']), lips=house_tone(col['lip'], lk['skin_k'] * 0.5), outfit=outfit[0],
             jacket=tuple(outfit[1]), sleeve=tuple(outfit[1]), shirt=shirt, tie=tie)
    if collar:                                              # the outfit's neckline (chat 15: 'open collar')
        d['collar'] = collar
    if 'neck_w' in kw:                                      # the person's lines: a wider neck (Kemi's, K1)
        d['neck_w'] = kw.pop('neck_w')
    if d['tie'] is not None:
        d['tie'] = tuple(d['tie'])
    sp = people.person(d)
    if 'brow_up' in kw:                                     # the person's resting brows (a pair: one raised)
        sp['brow_up'] = tuple(kw.pop('brow_up')) if isinstance(kw['brow_up'], list) else kw.pop('brow_up')
    sp['hair'] = 'bald'                                    # the engine's own hair: none (the head part draws it all)
    kh = dict(pk, look=look, hair=hair, lip=d['lips'], **kw)
    kh['meas'] = caricature(pk['meas'], kh.pop('push', 1.0), kh.pop('tune', {}))
    if kh['age'] and lk['age_k']:
        kh['age'] = dict(kh['age'])
    sp.update(kit_head='house', kit_house=kh, neck_shade=True)
    if hair == 'braids':                                    # the plaits behind the neck repaint it and lay the
        sp['neck_redrawn'] = True                           # collar again: the front torso leaves the collar to them
    return sp


CAST = {   # the test pair (Sam, 14 Nov): the lines a people file would hold. Chat 9, Sam's sheet notes: Andy is
           # finished at chat 7's head (no push, grin, lashes or tie); Kemi back to that head but for the bigger plaits,
           # her ears hidden (Sam: "her hair hides her ears"), her thin arched brows (her photos; Sam: "try the eyebrows"), the small pupils in her own big dark iris under a heavier, calm upper lid (chat 8's were wide and
           # startled), and her face's outline traced off her three front photos (shape)
    'burnham': dict(hair='swept', outfit=('suit', (31, 34, 58)), shirt=(246, 246, 246), tie=None, quiff=0.05,
                    hairline=-0.07, brow_thick=0.058),
    'badenoch': dict(hair='braids', outfit=('suit', (30, 32, 58)), shirt=(246, 246, 246), height=1.7, collar='open',
                     brow_thick=0.032, brow_arch=0.03, brow_taper=0.6, neck_w=1.2, plait_k=1.2, iris_r=0.98, pupil_r=0.28, iris_c=(56, 36, 26),
                     lid=0.24, shape=True),
    'walliams': dict(hair='swept', outfit=('suit', (31, 34, 58)), shirt=(246, 246, 246), tie=None,   # chat 13: his
                     mouth=dict(kind='smirk'), brow_up=[0.0, 0.025], push=1.1),   # smirk and cocked brow
                                                                         # (Blessed's hand-made, Sam: "That's him")
}


def install():
    import people
    PP.AV.MC.TC.HEADS  # noqa: B018  (the hooks are installed on import)
    people.install({})
    TC = PP.AV.MC.TC
    return TC


def draw(name, look, out, size=900, lines=None, src=None, variant=None):
    """One head and shoulders, front on, on white: the people kit's person with the house head. `lines`: the
    person's house lines (CAST's for that face otherwise); `src`/`variant`: one of facepick's heads (load())."""
    from PIL import Image
    from satire_style import install_circle_hands
    B, V = PP.B, PP.AV.MC.V
    install_circle_hands(B)
    TC = install()
    sp = person(name, look, src=src, variant=variant, **(lines if lines is not None else CAST[name]))
    TC.HEADS[sp['who']] = house_head
    TC.TORSOS[sp['who']] = lambda *a: None
    B.SS = 1
    tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    V.person(tile, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(sp), 0.0, 0)
    crop = tile.crop((150, 280, 930, 1180)).convert('RGB')
    crop = crop.resize((size, int(size * 900 / 780)))
    crop.save(out)
    return out


def turns(out, names, look='detail', yaws=(0, 45, 90, 135, 180), T=420):
    """Each person turned (front, three-quarter, side, three-quarter behind, behind), head and shoulders, big enough
    to judge; the people kit draws them (people.py's `head: house NAME` lines, as a film would)."""
    from PIL import Image, ImageDraw, ImageFont
    import people
    from satire_style import install_circle_hands
    B, V = PP.B, PP.AV.MC.V
    install_circle_hands(B)
    cast = {}
    for n in names:
        kw = dict(CAST.get(n, {}))
        d = dict(who=n, name=n.title(), house=dict(name=n, hair=kw.get('hair'), look=look))
        cast[n] = people.person(d)
    people.install(cast)
    B.SS = 1
    font = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 26)
    img = Image.new('RGB', (20 + len(yaws) * (T + 10), 60 + len(names) * (T + 50)), (236, 232, 226))
    d = ImageDraw.Draw(img)
    d.text((20, 16), 'Turned: front, three-quarter, side, three-quarter behind, behind', font=font, fill=(30, 30, 30))
    for i, (n, sp) in enumerate(cast.items()):
        y = 60 + i * (T + 50)
        d.text((20, y), sp['name'], font=font, fill=(30, 30, 30))
        for k, yaw in enumerate(yaws):
            tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
            V.person(tile, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(sp), 0.0, yaw)
            crop = tile.crop((150, 230, 930, 1010)).convert('RGB').resize((T, T))
            img.paste(crop, (20 + k * (T + 10), y + 36))
    img.save(out, quality=88)
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
    elif a and a[0] == 'trace':
        print(trace(a[1], a[2] if len(a) > 2 else None))
    elif a and a[0] == 'brows':
        print(browcheck(a[1], a[2] if len(a) > 2 else None))
    elif a and a[0] == 'turns':
        print(turns(a[1], a[2:] or ['burnham', 'badenoch']))
    elif a and a[0] == 'head':
        print(draw(a[1], a[2], a[3]))
    else:
        print(__doc__)
