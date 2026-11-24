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
    eye_scale, iris_r/pupil_r/iris_c (the iris's colour), lid (a heavier upper lid: calm, not wide), brow_up/brow_arch/brow_taper, mouth (the house mouths, FA.house_mouth: soft, grin,
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
    python3 source/facehouse.py measure NAME [OUT.jpg]             the head's whole shape off the photos (chat 16)
    python3 source/facehouse.py compare OUT.jpg NAME [FILM:WHO] [--turns]   photos, a known head, before, measured,
                                                                   pushed (--turns: the pushed head turned, under)

WHOLE HEAD (chat 16, Sam: "draw the face shape from the reference a lot more intelligently"): measure_head() reads
    each front photo's face skin row by row (ears cut at the mesh's face edge), the hair and skin together (the head's
    silhouette), the crown, the hairline and the side hair's foot into the pick ('head'); with `head` in the lines
    (the default; CAST's finished pair say head=False) the face outline, the swept hair's cap and sides and the eyes'
    size (HEAD_EYES) follow it. Kittest facehouse_head_from_photos.
    DOME (rule 49, Milburn note 4, Pat "alien carrot man" at 62% likeness): dome_faults() measures a bald head's drawn
    skull: widest at or above the eyes, no taller over its widest row than its half width (a near half-circle, as the
    photos' skulls measure); draw() prints HEAD SHAPE lines, facepick's sheet shows them red. Kittest dome_not_a_carrot.
    PROPORTIONS (chat 17, rule 30: pushing each row from the average face left Walliams a light bulb; his rows differ
    from it by hundredths): shape_push (SHAPE_PUSH 3) pushes the head's proportions from real faces' middle by the
    pick's card (z-scores): the face's width (face_wide), the jaw against the cheeks (jaw_wide) and with it the chin's
    squareness (SQUARE); feature_scale() scales every feature together so the eye centres sit against the drawn
    cheeks as the photos' do, pushed alike; the layout's fw/jw/fhw are the drawn face's (ears, age lines, stubble);
    the turned views go round on the drawn outline (_turn_widths). The beard is face skin to the segmenter already
    (it counts as jaw). Kittest facehouse_head_proportions. shape_push 1 draws the photos' shape as measured.

FOCUS (front-on focus C2, 19 Nov): sp['focus'] -1 .. +1 moves the front head's pieces toward where they look
    (focus.py); 0 draws exactly as before.

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
from people_parts import FA, dk, INK, oval  # noqa: E402
from people_parts import curve as _curve          # noqa: E402


def curve(pts, n=6):
    """The closed curve, through each point once (Open Wounds chat 9: a closed curve through one point twice in a row
    loops out into a spike, Sam's note 11 on Blair's grin; the hair and hat shapes here did it too: the turned hard
    hat's two sides met at its top point twice, a nub on Kemi's hat, 6% of its width). Repeats dropped, wrap included."""
    q = []
    for x, y in pts:
        if not q or abs(x - q[-1][0]) > 1e-6 or abs(y - q[-1][1]) > 1e-6:
            q.append((x, y))
    while len(q) > 3 and abs(q[0][0] - q[-1][0]) < 1e-6 and abs(q[0][1] - q[-1][1]) < 1e-6:
        q.pop()
    return _curve(q, n)
from faces import blend               # noqa: E402
from ink import open_curve                        # noqa: E402
import turnhead as TH  # noqa: E402
import focus as FO                               # noqa: E402  (C2: where a front-on head looks)

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
                brow=d.get('brow'), src=src, beard=d.get('beard') or None, head_m=d.get('head'), card=d.get('card') or {})


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
    L = FA.layout(load(name)['meas'])
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


# ---------------------------------------------------------------------------------------------- the whole head
# Face tool chat 16 (Sam on the Walliams sheet, 14 Nov: "Very different head shape ... it just needs to be able to
# draw the face shape from the reference a lot more intelligently"). The house outline was built from three widths
# (forehead, cheeks, jaw) and the hair from the house's own cap: his broad box (the hair as wide as the cheeks, a
# low flat crown, a jaw nearly as wide) came out a narrow, tall egg. Now the head's whole shape is read off the front
# photos: the face skin row by row with the ears cut away (the mesh's face edge marks where the cheek ends and the
# ear begins), the hair and skin together (the head's silhouette: temples, the hair's width, the crown), where the
# hair starts over the forehead and how far down the sides it comes. The middle value of the photos per row.
HV = tuple(round(v, 2) for v in np.arange(-0.6, 1.06, 0.05))      # the rows measured (face heights)
OVAL = (10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149,
        150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109)               # the mesh's face edge


def _poly_halfw(u, v, rows):
    """A closed outline's half width at each row (nan where it does not reach)."""
    out = []
    for r in rows:
        xs = []
        for i in range(len(u)):
            j = (i + 1) % len(u)
            if (v[i] - r) * (v[j] - r) < 0:
                xs.append(u[i] + (r - v[i]) / (v[j] - v[i]) * (u[j] - u[i]))
        out.append((max(xs) - min(xs)) / 2 if len(xs) >= 2 else float('nan'))
    return out


def _head_rows(path):
    """One front photo's head, in the house's face units (0 the mesh's forehead point, 1 its chin, upright): per HV
    row the face skin's half width (ears cut: past the mesh's face edge by EAR, the ear has begun), the hair and skin
    together, the mesh edge; the crown (the hair's top over the middle), the chin's foot, the hairline (the first
    face skin under the hair at 0, 0.1, 0.2, 0.3 across) and how low the hair comes down the sides."""
    import likeness as LK
    from scipy import ndimage
    im, fc = LK.pick_face(path)
    crop, mask, (x0, y0, x1, y1) = LK.segment(im, fc)
    P = (fc['P'][:, :2] - [x0, y0]) * [512 / (x1 - x0), 512 / (y1 - y0)]
    a, b = P[10], P[152]
    hh, ang = np.hypot(*(b - a)), math.atan2(b[0] - a[0], b[1] - a[1])
    ca, sa = math.cos(ang), math.sin(ang)
    uv = lambda xs, ys: (((xs - a[0]) * ca - (ys - a[1]) * sa) / hh, ((xs - a[0]) * sa + (ys - a[1]) * ca) / hh)  # noqa: E731
    seed = (int(P[1][1]), int(P[1][0]))
    lab, _ = ndimage.label(mask == 3)
    su, sv = uv(*np.nonzero(lab == lab[seed])[::-1])
    hm = ndimage.binary_opening(mask == 1, iterations=1)
    lab2, _ = ndimage.label(hm | (mask == 3))
    hu, hv = uv(*np.nonzero(lab2 == lab2[seed])[::-1])
    ou, ov = uv(P[list(OVAL), 0], P[list(OVAL), 1])
    oval = _poly_halfw(ou, ov, HV)
    mid_u = float(np.mean(ou))
    skin, both = [], []
    for v, o in zip(HV, oval):
        s, h = np.abs(sv - v) < 0.008, np.abs(hv - v) < 0.008
        sw = float((su[s].max() - su[s].min()) / 2) if s.sum() > 3 else float('nan')
        hw = float((hu[h].max() - hu[h].min()) / 2) if h.sum() > 3 else float('nan')
        if o == o and 0.15 <= v <= 0.75:                  # the ears: cut back to the face's edge (the hair beside
            sw = min(sw, o + EAR) if sw == sw else sw     # the temples, above the ears, kept)
            if v >= 0.3:
                hw = min(hw, max(o + EAR, sw)) if hw == hw else hw
        skin.append(sw)
        both.append(hw)
    top = hv[np.abs(hu - mid_u) < 0.05]
    hl = []
    for du in (0.0, 0.1, 0.2, 0.3):                       # the hairline: the first face skin from the top
        vals = [sv[(np.abs(su - mid_u - sg * du) < 0.012) & (sv < 0.35)] for sg in (-1, 1)]
        vals = [x.min() for x in vals if len(x)]
        if vals:
            hl.append((du, float(np.mean(vals))))
    low = float('nan')                                    # the side hair's foot: hair beside the face
    hs = (mask == 1)[lab2 == lab2[seed]]
    hu2, hv2 = hu[hs], hv[hs]
    side = hv2[np.abs(hu2 - mid_u) > 0.3]
    if len(side):
        low = float(np.percentile(side, 97))
    return dict(skin=skin, both=both, oval=oval, crown=float(top.min()) if len(top) else float('nan'),
                foot=float(sv.max()), hairline=hl, side_low=low, path=path, P=fc['P'], ang=ang, mid=mid_u)


EAR = 0.01           # skin this far past the mesh's face edge (face heights) is ear


def _canon_oval():
    """The average face's edge (MediaPipe's canonical face), half width per HV row in the same face units."""
    import likeness as LK
    C = LK.canonical()
    a, b = C[10, :2] * [1, -1], C[152, :2] * [1, -1]
    hh = float(np.hypot(*(b - a)))
    return _poly_halfw(list((C[list(OVAL), 0] - a[0]) / hh), list((-C[list(OVAL), 1] - a[1]) / hh), HV)


def measure_head(name, out=None, src=None):
    """The head's whole shape off the person's front photos (chat 16), saved into the pick as 'head': per row the
    face skin (ears cut), the head's silhouette (hair and skin), the mesh's face edge and the average face's; the
    crown, the chin's foot, the hairline, the side hair's foot. The person's lines draw it with `head` (every face
    but the finished pair, Andy and Kemi). OUT: the drawn head's outline and hair edge laid over each photo."""
    f = pick_file(name, src)
    d = json.load(open(f))
    got = [_head_rows(os.path.join(ROOT, p)) for p in d['fronts']]
    med = lambda k: [None if np.isnan(x) else round(float(x), 4)                      # noqa: E731
                     for x in np.nanmedian(np.array([g[k] for g in got], float), 0)]
    hl = {}
    for g in got:
        for du, v in g['hairline']:
            hl.setdefault(du, []).append(v)
    hd = dict(v=list(HV), skin=med('skin'), both=med('both'), oval=med('oval'),
              avg=[None if np.isnan(x) else round(float(x), 4) for x in _canon_oval()],
              crown=round(float(np.nanmedian([g['crown'] for g in got])), 4),
              foot=round(float(np.median([g['foot'] for g in got])), 4),
              hairline=[[du, round(float(np.median(vs)), 4)] for du, vs in sorted(hl.items())],
              side_low=round(float(np.nanmedian([g['side_low'] for g in got])), 4), photos=d['fronts'])
    d['head'] = hd
    json.dump(d, open(f, 'w'), indent=1)
    if out:
        head_overlay(name, got, out, src)
    return hd


def head_overlay(name, got, out, src=None, T=420):
    """Each front photo with the drawn head laid over: the face outline (yellow) and the hair's edge (cyan)."""
    from PIL import Image, ImageDraw
    sp = person(name, 'detail', **dict(CAST.get(name, {}), head=True, src=src))
    kh = sp['kit_house']
    L = face_layout(kh)
    face = face_outline(L, -0.3)
    sh = _swept_shapes(L, kh, (0, 0, 0)) if kh['hair'] == 'swept' else None
    tiles = []
    for g in got:
        im = Image.open(g['path']).convert('RGB')
        P = g['P'][:, :2]
        a, b = P[10], P[152]
        hh, ca, sa = np.hypot(*(b - a)), math.cos(g['ang']), math.sin(g['ang'])
        to = lambda uv: [(a[0] + hh * ((u + g['mid']) * ca + v * sa), a[1] + hh * (-(u + g['mid']) * sa + v * ca))  # noqa: E731
                         for u, v in uv]
        k = max(2, int(hh / 120))
        dr = ImageDraw.Draw(im)
        n = to(curve(face, 4))
        dr.line(n + n[:1], fill=(255, 220, 0), width=2 * k)
        if sh:
            for piece in sh['sides'] + [sh['cap']]:
                q = to(curve(piece, 2))
                dr.line(q + q[:1], fill=(0, 230, 255), width=k)
        c = (a + b) / 2
        tiles.append(im.crop((int(c[0] - hh), int(c[1] - 1.15 * hh), int(c[0] + hh), int(c[1] + 0.85 * hh))).resize((T, T)))
    sheet = Image.new('RGB', (len(tiles) * (T + 10) - 10, T), (255, 255, 255))
    for i, t in enumerate(tiles):
        sheet.paste(t, (i * (T + 10), 0))
    sheet.save(out, quality=90)
    return out


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
    br = curve(FA.brow_uv(L, kh.get('brow_thick', 0.05), 0.0, 0.0, kh.get('brow_arch', 0.0), kh.get('brow_taper', 0.0),
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
LID0 = 0.12          # the house's resting upper lid (FA.eyes' lid4) that the measured brow height was laid out against


def face_layout(kh):
    """The layout the head is drawn on: the pick's measures, the brows kept their measured height above the lid AS
    DRAWN (chat 10: a heavier lid, `lid`, lowers the lid line; the brows used to stay put, so the gap grew)."""
    meas = dict(kh['meas'])
    lo = EYE_OPEN_HEAD if kh.get('head') and kh.get('head_m') else EYE_OPEN_MIN
    meas['eye_open'] = max(meas.get('eye_open', lo), lo)
    hd = None
    if kh.get('head') and kh.get('head_m'):                # chat 16: the whole head as measured (measure_head())
        hd = drawn_head(kh['head_m'], kh.get('shape_push', SHAPE_PUSH), kh.get('card'))
        meas['face_wide'] *= feature_scale(kh, hd, meas, kh.get('shape_push', SHAPE_PUSH))
    L = FA.layout(meas)
    if hd:                                                 # chat 17: the widths every part reads (ears, age lines,
        L['head'] = hd                                     # stubble, the turned views) are the drawn face's own
        r = [(q[0], q[1]) for q in hd['rows'] if q[1] is not None]
        w = lambda v: 2 * float(np.interp(v, *zip(*r)))   # noqa: E731
        L.update(fw=2 * _cheek(r), jw=w(PROP_ROWS[1]), fhw=w(0.1))
    L['brow_y'] += L['eh'] / 1.8 * (kh.get('lid', LID0) - LID0)
    if (kh.get('brow') or {}).get('high'):                 # browcheck() measured the photos: the brows sit as hers
        L['brow_y'] += (_brow_gap(L, kh) - kh['brow']['high']) * L['ew']
    return L


def _cheek(rows):
    """The face's widest half width from the temples to the jaw (the cheeks), from (v, half width) rows."""
    return max(w for v, w in rows if w is not None and 0.3 <= v <= PROP_ROWS[0] + 0.1)


def feature_scale(kh, hd, meas, push=3.0):
    """Chat 17: the face's width against its features. The features are laid out on the pick's face_wide; the drawn
    face is the measured one, pushed. Every feature (eyes, their spacing, nose, mouth) is scaled together so the eye
    centres sit against the drawn cheeks as the photos' do against theirs, that proportion pushed from real faces'
    middle (the average face's skin cheek over its eye centres) like the head's other proportions. Without it the
    pick's tiny eyes (eye_size pushed small) pulled the eye centres in by a sixth: pinched features on a big face."""
    a = json.load(open(os.path.join(HERE, 'likeness_average.json')))['neutral']
    card = kh.get('card') or {}
    raw = {k: a['med'][k] + card.get(k, 0.0) * a['spread'][k] for k in ('face_wide', 'eye_size', 'eyes_apart')}
    ecx = lambda m: m['eye_size'] * m['face_wide'] * (m['eyes_apart'] + 1) / 2         # noqa: E731
    hm = kh['head_m']
    photo = _cheek(list(zip(hm['v'], hm['skin']))) / ecx(raw)
    avg = _cheek([(v, None if x is None else x + float(np.interp(v, *zip(*SKIN_BIAS))))
                  for v, x in zip(hm['v'], hm['avg'])]) / ecx(a['med'])
    want = _cheek([(q[0], q[1]) for q in hd['rows']]) / (avg + push * (photo - avg))
    return want / ecx(meas)


SHAPE_PUSH = 3.0     # chat 17: the head's PROPORTIONS pushed from real faces' middle by this (the card's z-scores,
                     # likeness_average's spread): the face's width against its height, the jaw against the cheeks and
                     # the chin's squareness. Chat 16 pushed each row from the average face (x1.3, x3): his rows differ
                     # from it by a few hundredths, so nothing moved and the narrow chin read as a light bulb.
PROP_ROWS = (0.5, 0.8)   # the cheeks' row and the jaw's (face heights): the jaw push grows from one to the other
SQUARE = 2.5             # how much a pushed jaw squares the chin (a broad, square jaw: the card's words for one)


def proportions(card, push=SHAPE_PUSH):
    """The drawn head's proportion factors from the person's card (z-scores against real faces, likeness.py): the
    face's width (face_wide) and the jaw against the cheeks (jaw_wide), each as the pushed measure over the
    photos' own: (middle + push z spread) / (middle + z spread), held to 0.85-1.2; the chin's squareness from the
    jaw's (a jaw pushed wider squares the chin, SQUARE)."""
    a = json.load(open(os.path.join(HERE, 'likeness_average.json')))['neutral']

    def fac(k):
        z, m, sd = (card or {}).get(k, 0.0), a['med'][k], a['spread'][k]
        return min(1.2, max(0.85, (m + push * z * sd) / (m + z * sd)))
    w, j = fac('face_wide'), fac('jaw_wide')
    return dict(wide=w, jaw=j, square=max(0.5, min(1.5, 1.0 - SQUARE * (j - 1.0))))


def _smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def drawn_head(hd, push=SHAPE_PUSH, card=None):
    """The measured head (measure_head()) as the drawing uses it: rows (v, face half width, silhouette half width),
    the face's proportions pushed (proportions()): every row widened by the face's width factor, the rows from the
    cheeks to the jaw widened by the jaw's (growing smoothly), and under the jaw the chin's taper eased by the
    squareness (the foot kept: the chin's bottom flattens); the hair standing off the head by as much as measured."""
    pr = proportions(card, push)
    c0, j0 = PROP_ROWS
    known = [(v, s) for v, s in zip(hd['v'], hd['skin']) if s is not None]
    sj = float(np.interp(j0, *zip(*known)))
    top = max(s for v, s in known if v <= c0) * pr['wide']     # the jaw never wider than the cheeks (a box, not a pear)
    rows = []
    for v, s, b in zip(hd['v'], hd['skin'], hd['both']):
        if s is None:
            rows.append((v, s, None if b is None else b * pr['wide']))
            continue
        g = 1.0 + (pr['jaw'] - 1.0) * _smooth((v - c0) / (j0 - c0))
        if v > j0:                                         # under the jaw: the taper eased (square < 1: squarer)
            s = sj * (1.0 - (1.0 - s / sj) * pr['square'])
        s1 = s * g * pr['wide']
        if v > c0:
            s1 = min(s1, top)
        b1 = None if b is None else s1 + max(0.0, b - s) * min(1.0, pr['wide'])
        rows.append((v, s1, b1))
    return dict(rows=rows, crown=hd['crown'], foot=hd['foot'], hairline=[tuple(q) for q in hd['hairline']],
                side_low=hd['side_low'], prop=pr)


SKIN_BIAS = ((0.05, 0.072), (0.1, 0.023), (0.15, -0.005), (0.2, -0.018), (0.25, -0.015), (0.3, -0.014),
             (0.35, -0.01), (0.4, -0.007), (0.45, -0.003), (0.5, 0.0), (0.55, 0.003), (0.6, 0.008), (0.65, 0.012),
             (0.7, 0.015), (0.75, 0.016), (0.8, 0.023), (0.85, 0.026), (0.9, 0.04), (0.95, 0.054))
# the photos' skin edge against the average face's mesh edge, the middle of the faces measured so far (Walliams,
# Burnham, Badenoch, chat 16): the mesh's chin is narrower than any real chin's skin, its temples sit under the
# hair. The push is from the average face plus this, so only what is this face's own grows.
HEAD_EYES = dict(eye_scale=1.2, liner=3.0)   # Sam (14 Nov): bigger, livelier eyes, as the Blessed head's
EYE_OPEN_HEAD = 0.26                          # and never shut to a line (EYE_OPEN_MIN for the finished pair)


def _sil(L, v):
    """The head's measured silhouette (hair and skin) half width at row v."""
    r = [(q[0], q[2]) for q in L['head']['rows'] if q[2] is not None]
    return float(np.interp(v, [q[0] for q in r], [q[1] for q in r]))


def _brow_gap(L, kh):
    """The drawn brow's middle line over the eye's middle, above the drawn upper lid, in eye widths."""
    br = curve(FA.brow_uv(L, kh.get('brow_thick', 0.05), 0.0, 0.0, kh.get('brow_arch', 0.0), kh.get('brow_taper', 0.0),
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
    if kh['hair'] == 'bald':
        L['round_top'] = True
        L['dome'] = kh.get('dome', -0.44)                 # Milburn note 4: the crown's height and the skull's
        L['dome_wide'] = kh.get('dome_wide')              # half width over the temples (face units), the photos'
    if kh.get('shape') and kh.get('outline'):               # the outline traced off the front photos (trace())
        L['trace'] = kh['outline']
    FF = FO.Focus(FA.Face(hx, hy), sp, L, _focus_room(L, kh))   # C2 (19 Nov): where they look; off at focus 0
    f = FF.whole
    skin = sp['skin']
    hc = sp['hair_c']
    piece = kh['hair']
    if piece == 'braids':
        braids_behind(p, f, L, hc, kh, sp)
    if piece != 'braids':                                 # her plaits cover the ears
        ears(p, FF.ears, _ear_L(L), skin, kh.get('ear_k', 1.0))
    o = curve(f.pts(face_outline(L, -0.42 if piece != 'braids' else _hair(L, kh)['crown'] + 0.06)), 4)
    p.poly(o, skin, INK, 2.6)
    if lk['sockets'] and kh['eyes'].get('shade', 0) >= 0.1:
        sockets(p, FF.eyes, L, skin, kh['eyes']['shade'])
    ey = kh['eyes']
    FA.eyes(p, FF.eyes, L, dict(sp, lid4=sp.get('lid4', kh.get('lid', 0.12)), look=FO.look(sp)), tuple(kh.get('iris_c') or ey.get('iris') or (66, 46, 34)), dk(skin, 0.8),
            liner=_eye(kh, 'liner', 2.8) + 1.6 * kh.get('lashes', 0.0), iris_r=kh.get('iris_r', min(1.15, ey.get('iris_r', 0.95))),
            pupil_r=kh.get('pupil_r', min(0.5, ey.get('pupil_r', 0.42))), scale=_eye(kh, 'eye_scale', 1.0))
    if kh.get('lashes'):
        lashes(p, FF.eyes, L, sp, kh['lashes'], _eye(kh, 'eye_scale', 1.0))
    FA.brows(p, FF.brows, L, sp['brow_c'], kh.get('brow_thick', 0.05), sp.get('brow_up', 0.0), sp.get('frown', 0.0),
             kh.get('brow_arch', 0.0), kh.get('brow_taper', 0.0), _peak(kh))
    FA.nose(p, FF.nose, L, skin)
    age_lines(p, FF.lines, L, skin, kh['age'], lk)
    if kh.get('beard'):
        stubble(p, f, L, skin, kh['beard'])
    fx, my = FF.mouth(0.0, L['lip13'])
    m = kh.get('mouth')
    if m:                                                 # the person's own resting mouth (chat 8: the likeness push)
        FA.talk_or(p, dict(sp, lips=True, lip_c=kh['lip']), 0.0, fx, my - 6, lambda: FA.house_mouth(
            p, FF.mouth, L, m['kind'], kh['lip'], skin, m.get('wide', 1.12), m.get('gap', 0.0), m.get('creases', 1.0), m.get('drop')))
    else:
        FA.lips(p, FF.mouth, L, dict(sp, smile=sp.get('smile', 0.0), lopsided=None), kh['lip'], (fx, my - 6))
    if piece == 'swept':
        swept(p, f, L, hc, kh, lk)
    elif piece == 'bald':
        bald(p, f, L, hc, kh, skin)
    elif piece == 'bob':
        bob(p, f, L, hc, kh, lk)
    elif piece == 'back':
        back(p, f, L, hc, kh, lk)
    elif piece == 'braids':
        braids(p, f, L, hc, lk, kh)
        if kh.get('ears'):                                # over the plaits, as the pick drew them (K1: her width)
            FA.ears(p, FF.ears, _ear_L(L), skin)
    if kh.get('pearls'):
        earrings(p, f, L, dict(kh, _skin=skin))
    if kh.get('hat'):
        cr = _hair(L, kh)['crown'] if piece == 'braids' else -0.46
        hard_hat(p, f, L, kh, cr, max(_face_u(L, 0.0) + 0.1, L['fw'] * 0.5 + 0.08))
    if kh.get('glasses'):
        glasses(p, FF.lens, L, kh['glasses'])
    return fx


def _focus_room(L, kh):
    """How far the far eye, brow and lens may slide under focus: the outline's half width at the eye line less the
    outermost of the eye's corner and the glasses' outer rim (glasses()' own sums), less a hair."""
    if not kh.get('focus_room', True):
        return None
    ew = L['ew']
    outer = L['ecx'] + ew * 0.5 * _eye(kh, 'eye_scale', 1.0)
    g = kh.get('glasses')
    if g:
        outer = max(outer, min(L['ecx'] + g['cx'] * ew + g['w'] * ew * g.get('w_k', 1.0) / 2, L['fw'] * 0.5))
    return _face_u(L, L['eye_y']) - outer - 0.012


def ears(p, f, L, skin, k=1.0):
    """The house ears (FA.ears); `ear_k` in the person's lines (Milburn chat 5, McFadden's): bigger, standing out
    from the head by as much again."""
    if k == 1.0:
        return FA.ears(p, f, L, skin)
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.5:
            continue
        ex, ey = f(sgn * (L['fw'] * 0.5 + 0.01 + 0.03 * (k - 1)), 0.42)
        p.poly(oval(ex, ey, 11 * k * 1.15, 24 * k, 20), skin, INK, 2.4)
        p.line([(ex - sgn * 2 * k, ey - 10 * k), (ex + sgn * 3 * k, ey), (ex - sgn * 1 * k, ey + 10 * k)], dk(skin, 0.7), 1.4)


def _ear_L(L):
    """The ears sit on the face's edge: the measured head's own (chat 17: on the house width they hid behind the
    measured face, which is wider), else the house's."""
    return dict(L, fw=2 * _face_u(L, 0.42)) if L.get('head') else L


def _eye(kh, k, default):
    """The person's own eye line (eye_scale, liner), else the measured head's (HEAD_EYES), else the house's."""
    if k in kh:
        return kh[k]
    return HEAD_EYES[k] if kh.get('head') and kh.get('head_m') else default


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
    p.poly(f.pts(low + FA.tufts(cheek, 0.01, 0.014, out=1.0, seed=seed)), mid, None)
    chin = FA.tufts([(jw * 0.46, 0.8), (mw * 0.55, l17 + 0.06), (0.0, l17 + 0.075), (-mw * 0.55, l17 + 0.06),
                     (-jw * 0.46, 0.8)], 0.012, 0.016, out=-1.0, seed=seed + 1)
    p.poly(f.pts([q for q in low if abs(q[0]) < jw * 0.47 and q[1] > 0.78] + chin[::-1]), light, None)
    mt = l0 - 0.03
    mo = FA.tufts([(-mw * 0.6, l13 + 0.004), (-mw * 0.52, mt + 0.008), (-nw * 0.3, mt), (0.0, mt + 0.004),
                   (nw * 0.3, mt), (mw * 0.52, mt + 0.008), (mw * 0.6, l13 + 0.004)], 0.006, 0.012, out=1.0, seed=seed + 2)
    goat = [(mw * 0.6, l13 + 0.01), (mw * 0.3, l17 + 0.012), (mw * 0.14, l17 + 0.045), (0.0, l17 + 0.05),
            (-mw * 0.14, l17 + 0.045), (-mw * 0.3, l17 + 0.012), (-mw * 0.6, l13 + 0.01)]
    p.poly(f.pts(mo + FA.tufts(goat, 0.007, 0.012, out=-1.0, seed=seed + 3)), must, None)
    if ink:                                               # turned (turnhead's TurnFace): its own outline inks
        p.poly(curve(f.pts(face_outline(L)), 4), None, INK, 2.6)   # the jaw's ink line back over the shade


def lashes(p, f, L, sp, k, scale=1.0):
    """Long dark lashes along each upper lid, longest at the outer corner (chat 8: Burnham's, the cartoonists' cue);
    k (0..1) their length and count. The lid's curve is FA.eyes' own."""
    w = L['ew'] * FA.H / 2 * scale
    h = L['eh'] * FA.H / 1.8 * scale
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
    if L.get('head'):
        return _swept_measured(L, kh, hc)
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
    cap = FA.tufts(top, 0.005, 0.03, out=1.0, seed=31) + front
    return dict(c=c, hl=hl, lift=lift, grey=grey, sides=sides, cap=cap)


def _swept_measured(L, kh, hc):
    """Chat 16: the swept hair on the head's measured shape: the cap's outer edge the photos' silhouette from the
    crown down the temples (as wide as it is: his box), the fringe's edge on the measured hairline, the clipped sides
    from under the cap down to where the side hair ends, their inner edge laid on the face's own edge. The house's
    look kept: the tufted top, the sweep rising higher on our right, the strokes and the light (scaled to the hair's
    own depth, crown to hairline)."""
    hd = L['head']
    hm = dict(hd['hairline'])
    hl = kh.get('hairline_m', hm.get(0.0, -0.1))
    crown = hd['crown']
    lift = kh.get('quiff', 0.02)                         # the photos hold his quiff already: a touch more only
    grey = kh.get('grey') or blend(hc, (150, 146, 142), 0.35)
    c = _sil(L, hl)
    cb = min(hl + 0.1, 0.0)                               # the dark cap's foot at the side; the grey below
    low = min(max(hd['side_low'], cb + 0.12), 0.34)
    k = (hl - crown) / 0.42                              # the hair's own depth against the house cap's
    vs = [v for v in np.arange(round(cb, 2), crown + 0.04, -0.03)]
    up = lambda u: lift * 0.8 * max(0.0, min(1.0, (u + 0.1 * c) / (0.7 * c))) * (1 - max(0.0, u / c - 0.75) * 2)  # noqa: E731
    rt = [(_sil(L, v) + 0.006, v) for v in vs]
    top_mid = [(c * x, crown + 0.02 * x * x - up(c * x)) for x in (0.55, 0.3, 0.0, -0.3, -0.55)]
    rt = [(u, v - (up(u) if v < hl else 0.0)) for u, v in rt]
    lt = [(-(_sil(L, v) + 0.006), v) for v in vs]       # our left, from its foot up
    top = lt + sorted(top_mid, key=lambda q: q[0]) + rt[::-1]   # over the crown, down to our right foot
    h = lambda u: float(np.interp(abs(u), sorted(hm), [hm[x] for x in sorted(hm)]))   # noqa: E731
    fe = _face_u(L, cb)
    front = [(c - 0.01, cb), (fe - 0.02, cb - 0.02), (0.3, h(0.3)), (0.2, h(0.2) + 0.005), (0.1, h(0.1) + 0.012),
             (0.0, h(0.0) + 0.016), (-0.1, h(0.1) + 0.012), (-0.2, h(0.2) + 0.002), (-0.3, h(0.3) - 0.004),
             (-fe + 0.02, cb - 0.02), (-c + 0.01, cb)]
    front = [q for q in front if abs(q[0]) <= c]
    cap = FA.tufts(top, 0.005, 0.03 * max(0.5, min(1.0, k)), out=1.0, seed=31) + front
    sides = []
    for sgn in (1, -1):
        sv = np.linspace(cb - 0.08, low, 7)
        outer = [(_sil(L, v) + 0.006, v) for v in sv]
        inner = [(min(_face_u(L, v) - 0.012, _sil(L, v) - 0.02), v) for v in sv[::-1]]
        pts = outer + [(_face_u(L, low) - 0.02, low + 0.02)] + inner
        sides.append([(-sgn * u, v) for u, v in pts])
    roof = sorted([q for q in top if q[1] < hl], key=lambda q: q[0])
    return dict(c=c, hl=hl, lift=lift, grey=grey, sides=sides, cap=cap, k=k, crown=crown, roof=roof)


class _Squeeze:
    """A face frame whose rows above `v0` are squeezed by k towards it (the house hair's strokes on a shallower or
    deeper head of hair)."""

    def __init__(self, f, v0, k, roof=None):
        self.f, self.v0, self.k = f, v0, k
        self.roof = roof                                  # the cap's top: nothing drawn above it (less a margin)

    def __call__(self, u, v):
        v = self.v0 + (v - self.v0) * self.k if v < self.v0 else v
        if self.roof:
            ru, rv = zip(*self.roof)
            v = max(v, float(np.interp(u, ru, rv)) + 0.035)
        return self.f(u, v)

    def pts(self, uvs):
        return [self(u, v) for u, v in uvs]


def _swept_strokes(p, f, hc, sh, lk):
    """The strokes brushed up and over, the light on the quiff, the grey flecks (the look 'detail')."""
    c, hl, lift, grey = sh['c'], sh['hl'], sh['lift'], sh['grey']
    light = blend(hc, (150, 140, 136), 0.38)
    if 'k' in sh:                                        # chat 16: the measured head: the house's strokes squeezed
        kk, f0 = sh['k'], f                              # to the hair's own depth (crown to hairline)
        f = _Squeeze(f0, hl, kk, sh.get('roof'))
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


# ---------------------------------------------------------------------------------------------- hair: bald
def bald_shapes(L, kh, hc):
    """Milburn chat 5 (McFadden): a bald crown, the hair a short clipped fringe at each side from the temple
    (`side_top`, face units) down to the ear's top (`side_low`), laid on the face's own edge and standing a little
    proud of it; its colour `grey` (the person's lines), else the hair colour greyed."""
    grey = tuple(kh.get('grey') or blend(hc, (150, 146, 142), 0.35))
    v0, v1 = kh.get('side_top', 0.0), kh.get('side_low', 0.3)
    vs = np.linspace(v0, v1, 12)
    proud = kh.get('side_proud', 0.026)
    out = [(_face_u(L, v) + proud * math.sin(math.pi * (v - v0) / (v1 - v0)) ** 0.7, v) for v in vs]
    inn = [(_face_u(L, v) - 0.006 - 0.012 * math.sin(math.pi * (v - v0) / (v1 - v0)), v) for v in vs[::-1]]
    right = out + inn
    return dict(grey=grey, sides=[right, [(-u, v) for u, v in right]])


def bald(p, f, L, hc, kh, skin):
    """The bald piece: the side fringes (bald_shapes) and a soft shine high on the dome, to our left."""
    sh = bald_shapes(L, kh, hc)
    for sd in sh['sides']:
        p.poly(curve(f.pts(sd), 2), sh['grey'], INK, 1.8)
    top = face_outline(L)[0][1]
    w = _face_u(L, top + 0.12)
    cx, cy = -w * 0.42, top + 0.1
    shine = [(cx + w * 0.26 * math.cos(a), cy + 0.045 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24)]
    p.poly(f.pts(shine), blend(skin, (255, 250, 244), 0.32), None)


# ---------------------------------------------------------------------------------------------- hair: bob, back
def bob_shapes(L, kh, hc):
    """Brexit Is Done (23 Nov, May): a short layered bob. The mass from a full crown down both sides over the tops of
    the ears to just under the lobe (`bob_low`, face units), the tips flicked out; a side-swept fringe from a parting
    on our left (`part`) across the forehead, its edge falling to the brow on our right. Lighter streaks (`light`)."""
    e = L['fw'] * 0.5
    c = e + kh.get('bob_wide', 0.09)                     # the hair stands proud of the face at the sides
    low = kh.get('bob_low', 0.5)
    pu = kh.get('part', -0.12)
    crown = kh.get('bob_crown', -0.5)
    fe = lambda v: _face_u(L, v)                          # noqa: E731
    outer_r = [(c * 0.55, crown + 0.02), (c * 0.85, crown + 0.1), (c, -0.22), (c + 0.01, 0.0), (c - 0.005, 0.2),
               (c - 0.02, 0.36), (c + 0.02, low - 0.03), (c + 0.05, low + 0.01)]        # the flick out at the tip
    inner_r = [(fe(low - 0.02) + 0.02, low - 0.02), (fe(0.36) - 0.005, 0.36), (fe(0.2) - 0.015, 0.2),
               (fe(0.08) - 0.025, 0.08)]
    # the fringe: from the parting it sweeps down and across to our right, ending on the brow at the temple
    fringe = [(fe(0.08) - 0.03, 0.06), (e * 0.72, 0.1), (e * 0.45, 0.04), (e * 0.15, -0.04), (pu + 0.06, -0.1),
              (pu, -0.13)]
    left_hl = [(pu - 0.08, -0.1), (-e * 0.6, -0.08), (-(fe(0.0) - 0.03), -0.02), (-(fe(0.12) - 0.02), 0.12),
               (-(fe(0.36) - 0.005), 0.36), (-(fe(low - 0.02) + 0.02), low - 0.02)]
    outer_l = [(-u, v) for u, v in outer_r[::-1]]
    top = [(-c * 0.55, crown + 0.02), (-c * 0.2, crown - 0.005), (c * 0.15, crown - 0.01)]
    cap = (top + outer_r + inner_r + fringe + left_hl + outer_l)
    cap = FA.tufts(cap[:len(top) + len(outer_r)], 0.004, 0.035, out=1.0, seed=41) + cap[len(top) + len(outer_r):]
    light = tuple(kh.get('light') or blend(hc, (250, 248, 242), 0.6))
    return dict(c=c, low=low, pu=pu, crown=crown, cap=cap, light=light, e=e)


def _bob_strokes(p, f, hc, sh):
    """The layers: strokes from the parting sweeping across the fringe and down each side, alternating light and dark."""
    c, pu, crown, low, light = sh['c'], sh['pu'], sh['crown'], sh['low'], sh['light']
    dark = dk(hc, 0.6)
    for k, x in enumerate((0.05, 0.2, 0.35, 0.5, 0.65)):            # across the fringe to our right
        u0 = pu + 0.02
        p.line(open_curve(f.pts([(u0, crown + 0.2 + 0.03 * k), (pu + x * 0.5, -0.14 + 0.02 * k),
                                 (min(pu + x * 0.95, sh['e'] * 0.8), -0.06 + 0.03 * k + 0.08 * x)]), 3),
               light if k % 2 else dark, 2.6)
    for sgn in (-1, 1):                                             # down each side to the flick
        for k, x in enumerate((0.25, 0.55, 0.8)):
            u = sgn * (sh['e'] + (c - sh['e']) * x)
            p.line(open_curve(f.pts([(u * 0.9, -0.2 + 0.04 * k), (u, 0.15), (u + sgn * 0.02, low - 0.06)]), 3),
                   dark if k % 2 else light, 2.4)
        for k in range(3):                                          # the layered ends: notches up from the tips
            u = sgn * (sh['e'] + (c - sh['e']) * (0.3 + 0.3 * k))
            p.line(open_curve(f.pts([(u, low - 0.01 - 0.02 * k), (u - sgn * 0.01, low - 0.09 - 0.02 * k)]), 2),
                   INK, 1.6)
    p.poly(curve(f.pts([(pu - 0.02, crown + 0.14), (pu + 0.12, crown + 0.12), (pu + 0.28, -0.3), (pu + 0.18, -0.24),
                        (pu + 0.04, -0.3)]), 3), blend(hc, light, 0.6), None)   # the light on the crown


def bob(p, f, L, hc, kh, lk):
    sh = bob_shapes(L, kh, hc)
    p.poly(curve(f.pts(sh['cap']), 2), hc, INK, 2.4)
    _bob_strokes(p, f, hc, sh)


def earrings(p, f, L, kh, near=None):
    """Pearl studs at the lobes (`pearls` in the person's lines), drawn over the hair; turned, only the `near` side's
    (-1: our left)."""
    for sgn in (-1, 1):
        if near is not None and sgn != near:
            continue
        lx, ly = f(sgn * (_face_u(L, 0.5) + 0.006), 0.515)            # the lobe under the hair's edge
        p.poly(oval(lx, ly, 6, 8, 14), kh.get('_skin', (222, 182, 158)), INK, 1.6)
        x, y = f(sgn * (_face_u(L, 0.5) + 0.008), 0.535)
        p.poly(oval(x, y, 7, 7, 14), (250, 248, 240), INK, 1.8)


def hard_hat(p, f, L, kh, crown, hw):
    """Brexit Is Done (23 Nov, Kemi on site): a white safety helmet sat on the hair, its brim at the forehead
    (`hat_v`, face units) and a peak over the eyes, a ridge front to back. Front view in face units (`hw`: the hair's
    half width); turned views as a solid on the head's own rings (turned_hat)."""
    col = tuple(kh.get('hat_c', (244, 244, 240)))
    vb = kh.get('hat_v', 0.04)
    top = crown - 0.16
    W = hw + 0.07
    dome = [(W * math.cos(a), vb + (top - vb) * math.sin(a)) for a in np.linspace(0, math.pi, 30)]
    p.poly(curve(f.pts(dome), 2), col, INK, 2.6)
    p.line(open_curve(f.pts([(0.0, vb - 0.005), (0.0, top + 0.01)]), 3), dk(col, 0.78), 3.0)   # the ridge
    for sgn in (-1, 1):
        p.line(open_curve(f.pts([(sgn * W * 0.55, vb - 0.01), (sgn * W * 0.5, (vb + top) / 2), (sgn * W * 0.3, top + 0.03)]), 3),
               dk(col, 0.86), 1.6)
    brim = [(-W - 0.04, vb - 0.012), (W + 0.04, vb - 0.012), (W + 0.05, vb + 0.02), (W * 0.5, vb + 0.03),
            (0.0, vb + 0.07), (-W * 0.5, vb + 0.03), (-W - 0.05, vb + 0.02)]
    p.poly(curve(f.pts(brim), 2), dk(col, 0.92), INK, 2.2)


def turned_hat(p, f, kh, crown):
    """The helmet from any turned view: a shell over the head's rings (each ring 1.18 times out, an ellipsoid from
    the brim's ring up to above the crown), its outline the shell's silhouette; the brim a band round the ring, the
    peak at the face (psi 0) reaching further; the ridge the face's centre meridian."""
    H = TH.H
    col = tuple(kh.get('hat_c', (244, 244, 240)))
    vb = kh.get('hat_v', 0.04)
    top = crown - 0.16
    ps = np.linspace(-180, 180, 145)
    bx, bz = f.ring(ps, vb)
    k = kh.get('hat_k', 1.3)
    def at(h):                                       # the shell's ring at height h (0 brim .. 1 top)
        s = math.sqrt(max(0.0, 1 - h * h)) * k
        X, Z = f.view(bx * s, bz * s)
        return X, Z, vb + (top - vb) * h
    left, right = [], []
    for h in np.linspace(0, 1, 16):
        X, Z, v = at(h)
        left.append((f.cx + float(X.min()) * H, f.top + v * H))
        right.append((f.cx + float(X.max()) * H, f.top + v * H))
    p.poly(curve(left + right[::-1], 2), col, INK, 2.6)
    fr = np.clip(np.cos(np.radians(ps)), 0, 1) ** 2         # 1 at the face's centre, 0 at the sides and back
    pk = 1.0 + 0.14 * fr                                     # the peak over the face reaching a little further
    #   (0.32 stuck out past the hat as a thin spike from three-quarter: chat 2)
    X, Z = f.view(bx * k * 1.08 * pk, bz * k * 1.08 * pk)
    # the brim as the front draws it (Sam on cast v1: the turned hat "sat flat and wide"): a band 0.032 deep, its
    # lower edge dipping to the peak over the face (front: vb + 0.07), the dip carried round with the face
    seen = Z >= -1e-6
    order = np.argsort(X[seen])
    xs = (f.cx + X[seen] * H)[order]
    low = (f.top + (vb + 0.024 + 0.05 * fr[seen]) * H)[order]
    if len(xs) > 2:
        topl = [(float(xs[0]) - 2, f.top + (vb - 0.012) * H), (float(xs[-1]) + 2, f.top + (vb - 0.012) * H)]
        bot = [(float(x), float(y)) for x, y in zip(xs, low)][::-1]
        p.poly(curve(topl + bot, 2), dk(col, 0.92), INK, 2.2)
    rid = []
    for h in np.linspace(0, 0.9, 10):                  # the ridge: the meridian at the face's centre, if we see it
        s = math.sqrt(max(0.0, 1 - h * h)) * k
        x, z = f.ring(0.0, vb)
        Xr, Zr = f.view(x * s, z * s)
        if float(Zr) > -0.05:
            rid.append((f.cx + float(Xr) * H, f.top + (vb + (top - vb) * h) * H))
    if len(rid) > 1:
        p.line(open_curve(rid, 3), dk(col, 0.78), 3.0)
    for psi in (-38.0, 38.0):                          # the two side lines the front draws (castsheet match, chat 2)
        x, z = f.ring(psi, vb)
        seg = []
        for h in np.linspace(0.04, 0.94, 10):
            s_ = math.sqrt(max(0.0, 1 - h * h)) * k
            Xr, Zr = f.view(float(x) * s_, float(z) * s_)
            if float(Zr) > 0.02:
                seg.append((f.cx + float(Xr) * H, f.top + (vb + (top - vb) * h) * H))
        if len(seg) > 2:
            p.line(open_curve(seg, 3), dk(col, 0.86), 1.6)


def back_shapes(L, kh, hc):
    """Brexit Is Done (23 Nov, Blair): grey hair brushed straight back off a high forehead, the temples receded
    (`recede`), a little lift over the front (`lift`); the sides short and lying back over the ears' tops."""
    e = L['fw'] * 0.5
    c = max(L['fhw'] * 0.5 + 0.03, e + 0.02)
    hl = kh.get('hairline', -0.17)
    rc = kh.get('recede', 0.07)
    lift = kh.get('lift', 0.05)
    crown = kh.get('back_crown', -0.5)
    fe = lambda v: _face_u(L, v)                          # noqa: E731
    front = [(c - 0.02, 0.2), (fe(0.2) - 0.02, 0.24), (fe(0.1) - 0.02, 0.08), (fe(-0.05) - 0.04, -0.06),
             (e * 0.6, hl - rc * 0.4), (e * 0.48, hl - rc), (e * 0.3, hl - rc * 0.5), (e * 0.12, hl + 0.005),
             (0.0, hl + 0.01)]
    front = front + [(-u, v) for u, v in front[::-1][1:]]
    top = [(-c + 0.01, 0.2), (-c - 0.01, 0.0), (-c + 0.01, -0.22), (-c * 0.8, crown + 0.1), (-c * 0.45, crown - lift * 0.5),
           (0.0, crown - lift), (c * 0.45, crown - lift * 0.5), (c * 0.8, crown + 0.1), (c - 0.01, -0.22),
           (c + 0.01, 0.0), (c - 0.02, 0.2)]
    cap = FA.tufts(top, 0.004, 0.03, out=1.0, seed=53) + front
    light = tuple(kh.get('light') or blend(hc, (244, 242, 238), 0.5))
    return dict(c=c, hl=hl, rc=rc, crown=crown, lift=lift, cap=cap, light=light, e=e)


def _round_strokes(p, f, prof, hc, sh, kind):
    """The hair's strokes on the side and back of a turned head, drawn on the hair's own surface (turnhead.hair_point,
    so they follow the shell): 'back' combed straight back, rows running from the temple round to the back of the
    head and falling to the nape; 'bob' the layers falling from the crown to the ends. Only where the surface faces
    us (Brexit chat 2, Sam on cast v1: Blair's side and back were a plain grey cap)."""
    import turnhead as TH
    light, dark = sh['light'], dk(hc, 0.7 if kind == 'back' else 0.6)
    vref = prof.get('shell_ref', -0.25)
    top = prof['shell'][0][0] + 0.04
    nape = prof.get('nape', 0.6) - 0.06

    def seen(psi, v):
        lo, hi = f.visible(max(v, vref))
        return any(lo + 4 <= q <= hi - 4 for q in (psi, psi - 360, psi + 360))

    def run(pts, col, w):
        seg = []
        for psi, v in pts:
            if seen(psi, v):
                seg.append(TH.hair_point(f, prof, psi, v))
            elif len(seg) > 2:
                p.line(open_curve(seg, 2), col, w)
                seg = []
            else:
                seg = []
        if len(seg) > 2:
            p.line(open_curve(seg, 2), col, w)

    for sgn in (-1, 1):
        if kind == 'back':                       # combed back: from the hairline over the temple back round the
            for k, v0 in enumerate(np.linspace(top + 0.02, 0.1, 6)):   # head, sweeping down to the nape behind
                end = 168 - 9 * k
                pts = [(sgn * a, v0 + (nape - 0.02 - v0) * max(0.0, (a - 95) / (end - 95)) ** 2.2)
                       for a in np.arange(65, end + 0.1, 3)]
                run(pts, light if k % 2 else dark, 1.9)
        else:                                    # the bob: layers falling from the crown, curling out at the ends
            for k, a in enumerate(np.arange(65, 181, 23)):
                pts = [(sgn * (a + 6 * (v - top)), v) for v in np.arange(top, nape + 0.06, 0.02)]
                run(pts, light if k % 2 else dark, 2.0)


def _back_strokes(p, f, hc, sh):
    """Combed straight back: strokes from the hairline up over the crown, fanning to the sides."""
    c, hl, crown = sh['c'], sh['hl'], sh['crown']
    dark = dk(hc, 0.7)
    for k, u in enumerate((-0.28, -0.18, -0.08, 0.02, 0.12, 0.22, 0.3)):
        u *= c / 0.42
        p.line(open_curve(f.pts([(u * 0.8, hl - 0.03), (u * 0.95, (hl + crown) / 2), (u * 1.1, crown + 0.15)]), 3),
               sh['light'] if k % 2 else dark, 2.2)
    for sgn in (-1, 1):
        p.line(open_curve(f.pts([(sgn * (sh['e'] - 0.005), 0.15), (sgn * (c - 0.01), -0.05), (sgn * c * 0.85, -0.3)]), 3),
               dark, 1.3)


def back(p, f, L, hc, kh, lk):
    sh = back_shapes(L, kh, hc)
    p.poly(curve(f.pts(sh['cap']), 2), hc, INK, 2.4)
    _back_strokes(p, f, hc, sh)


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
    hd = L.get('head')
    if hd:                                                # chat 16: the measured head; under the hair, just inside
        top = hd['crown'] + 0.035                         # the hair's edge (no white between hair and face)
        bare = L.get('round_top')                         # bald (McFadden): the photos' dome reads as hair, so
        if bare:                                          # the skull is the silhouette's own top and edge
            top = max(min(v for v, s, b in hd['rows'] if b is not None) + 0.01, L.get('dome', -0.44))
        right = []
        for v, s, b in hd['rows']:
            if v <= (-0.05 if bare else top + 0.02) or v > hd['foot'] - 0.01:   # bald: the dome is an arc
                continue                                                         # (its rows read hair: noisy)
            u = s if s is not None else (b - 0.06 if b is not None else None)
            if u:
                right.append((round(u, 4), v))
        if L.get('round_top'):                            # a bald crown (McFadden): a round dome, not a peak
            wd = L.get('dome_wide')
            if wd:                                        # Milburn note 4 ("alien carrot man"): the photos' skull
                right = [q for q in right if q[1] >= 0.1]  # (a01 measured): widest at the temples, 1.1x the
                u1, v1 = right[0]                         # cheeks, then a near half-circle over the top whose
                vc = v1 - 0.12                            # height is its half width; no egg, no waist
                up = [(wd * max(0.0, 1 - ((vc - v) / (vc - top)) ** 2.2) ** (1 / 2.2), v)
                      for v in np.linspace(top + 0.003, vc, 14)]
                up += [(wd + (u1 - wd) * (0.5 - 0.5 * math.cos(math.pi * (v - vc) / (v1 - vc))), v)
                       for v in np.linspace(vc, v1, 5)[1:-1]]
                right = up + right + [(0.0, hd['foot'])]
            else:
                u1, v1 = right[0]
                right = [(u1 * math.sin(a), v1 - (v1 - top) * math.cos(a)) for a in np.linspace(0.12, 1.5, 9)] + \
                    [q for q in right if q[1] >= v1] + [(0.0, hd['foot'])]
        else:
            right = [(right[0][0] * 0.55, top + 0.005)] + right + [(0.0, hd['foot'])]
        return [(0.0, top)] + right + [(-u, v) for u, v in right[::-1][1:]]
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
    vc = (yc - f.top) / FA.H
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
    lw = min(g['rim_w'], 0.17) * ew * FA.H
    y0 = max(L['eye_y'] + g['top'] * ew, L['brow_y'] - 0.02)
    y1 = L['eye_y'] + min(g['bot'], 1.0) * ew
    xi = max(half + g['cx'] * ew - g['w'] * ew / 2, 0.035)
    for sgn in (-1, 1):
        c, w = half + g['cx'] * ew, g['w'] * ew * g.get('w_k', 1.0)
        x0, x1 = sorted((sgn * max(c - w / 2, 0.035), sgn * min(c + w / 2, L['fw'] * 0.5)))
        r = g.get('round', 0.16)                             # 0.16 a rounded box; ~0.45 round lenses
        box = [(x0, y0 + (y1 - y0) * r), (x0 + (x1 - x0) * r, y0), (x1 - (x1 - x0) * r, y0), (x1, y0 + (y1 - y0) * r),
               (x1, y1 - (y1 - y0) * r * 1.2), (x1 - (x1 - x0) * r * 1.4, y1), (x0 + (x1 - x0) * r * 1.4, y1),
               (x0, y1 - (y1 - y0) * r * 1.2)]
        if g.get('round'):                                 # round lenses (McFadden's): a soft superellipse,
            n = 2.0 + 3.0 * (0.5 - min(0.5, g['round']))    # 2 a true oval, towards 3.5 a rounded square
            mx, my, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
            sg = lambda a: math.copysign(abs(a) ** (2 / n), a)   # noqa: E731
            pts = f.pts([(mx + rx * sg(math.cos(a)), my + ry * sg(math.sin(a))) for a in np.linspace(0, 2 * math.pi, 40)[:-1]])
        else:
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
    bo = age.get('boost', 1.0)                           # Brexit chat 2 (Sam on cast v1: May's age lines
    st = {k: min(1.0, v * lk['age_k'] * bo) for k, v in (age.get('strength') or {}).items()   # stronger): the
          if v * bo >= lk['age_min']}                    # person's lines (`age_boost`) deeper, wider, longer
    dark = sum(skin) < 360                               # a darker skin needs a deeper shade to show
    pen = lambda s: (dk(skin, (0.74 if dark else 0.8) - 0.06 * s - 0.1 * (bo - 1)), (1.5 + 0.7 * s) * bo ** 0.5)   # noqa: E731
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
HAIR = ('swept', 'braids', 'bald', 'bob', 'back')
TURN_PROF = {'swept': dict(hair_low=0.36, nape=0.62, volume=0.015),         # clipped short at the back
             'braids': dict(hair_low=0.5, nape=0.78, volume=0.05),
             'bald': dict(hair_low=0.3, nape=0.6, volume=0.0),
             'bob': dict(hair_low=0.5, nape=0.66, volume=0.06),       # May: full, to the lobe, the nape covered
             'back': dict(hair_low=0.3, nape=0.6, volume=0.03)}       # Blair: short at the back and sides               # bald: the skull is the head's own          # the plaits' bulk over the skull


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
        FA.house_mouth(p, f, L, m['kind'], kh['lip'], sp['skin'], m.get('wide', 1.12), m.get('gap', 0.0),
                          m.get('creases', 1.0), m.get('drop'))
    else:
        FA.lips(p, f, L, dict(sp, smile=sp.get('smile', 0.0), mouth='rest', lopsided=None), kh['lip'], (fx, my - 6))


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
    _turn_hair0(img, p, f, L, sp)
    kh = sp['kit_house']
    if kh.get('hat'):
        turned_hat(p, f, kh, _hair(L, kh)['crown'] if kh['hair'] == 'braids' else -0.46)


def hair_shell(cap, step=0.02, upto=0.1):
    """The front hair piece's outline as half widths row by row [(v, half width)], crown down to `upto`: the turned
    hair's mass is built to it (turnhead.hair 'shell'), so the hair keeps the front's height and width in every view
    (Brexit chat 2, Sam's n2: Blair's turned hair was a flatter, smaller shape than the front's)."""
    vs_ = [v for _, v in cap]
    top = min(vs_)
    out = [(top, 0.0)]
    n = len(cap)
    for v in np.arange(top + step / 2, upto + 1e-9, step):
        xs = []
        for i in range(n):
            (u0, v0), (u1, v1) = cap[i], cap[(i + 1) % n]
            if (v0 - v) * (v1 - v) <= 0 and v0 != v1:
                xs.append(abs(u0 + (u1 - u0) * (v - v0) / (v1 - v0)))
        if xs:
            out.append((float(v), max(xs)))
    return out


def _turn_hair0(img, p, f, L, sp):
    import turnhead as TH
    kh, hc = sp['kit_house'], sp['hair_c']
    lk = LOOKS[kh['look']]
    yaw = round(math.degrees(f.th))
    if kh['hair'] == 'bald':                                     # Milburn chat 5: the bare skull; a clipped band
        TH.hair(img, p, f, [], tuple(kh.get('grey') or hc), dict(f.prof, hair_low=0.3, nape=0.6, volume=0.0,
                                                                  hair_top=0.0, hair_top_back=0.12, hair_ragged=0.006))
        return
    if kh['hair'] in ('bob', 'back'):                            # Brexit Is Done: one mass, front carried round
        sh = (bob_shapes if kh['hair'] == 'bob' else back_shapes)(L, kh, hc)
        prof = dict(f.prof, **TURN_PROF[kh['hair']], shell=hair_shell(sh['cap']))   # one shape in every view
        cap = [(u, max(v, -0.44)) for u, v in curve(sh['cap'], 2)]          # the crown's points held to the skull
        fronts = [f.pts(TH.dense(cap))] if yaw <= 60 else []   # past 60 the front's crown point
        mask = TH.hair(img, p, f, fronts, hc, prof)                         # stood up off the skull (a spike)
        if yaw <= 60:
            TH.clipped(img, p, mask, lambda pen: (_bob_strokes if kh['hair'] == 'bob' else _back_strokes)(pen, f, hc, sh))
        if yaw >= 30:                                    # Sam (cast v1): the side and back not a plain cap
            TH.clipped(img, p, mask, lambda pen: _round_strokes(pen, f, prof, hc, sh, kh['hair']))
        if kh.get('pearls') and yaw <= 135:
            earrings(p, f, L, dict(kh, _skin=sp['skin']), near=-1 if f.th > 0 else 1)
        return
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
        if yaw <= 60:                                            # the far curtain past the far cheek (the front
            fv = [v for v in vs if v in far]                     # shows two; Sam's n3 picture had one: chat 2)
            if len(fv) > 3:
                fo = [(far[v] + H * (0.012 + 0.22 * max(0.0, v - 0.06)), f.top + v * H) for v in fv]
                fi = [(far[v] - H * 0.06, f.top + v * H) for v in fv]
                curt.append((fo + [(fo[-1][0] + H * 0.03, foot)], fi + [(fi[-1][0] - H * 0.02, foot)]))
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
    import body as B
    base = p.pen if hasattr(p, 'pen') else p
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw(B.Pen(layer, base.cam))
    m = Image.new('L', img.size, 255)
    ImageDraw.Draw(m).polygon([base.cam.P(*q) for q in poly], fill=0)
    a = np.asarray(layer)[:, :, 3].astype(np.uint16) * np.asarray(m) // 255
    layer.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(layer)


def _turn_widths(L):
    """The face's half widths the turned views go round on: the measured head's drawn outline (chat 17: the turned
    views carried the house outline's widths, so the head changed shape as it turned), else the house outline's."""
    import turnhead as TH
    return TH.half_widths(face_outline(L) if L.get('head') else FA.outline_uv(L, 0.4, crown=-0.42))


def _turn_person(sp):
    import turnhead as TH
    kh = sp['kit_house']
    key = _turn_key(kh)
    if key not in TH.PEOPLE:
        L = face_layout(kh)
        prof = TH.fitted(L, -0.42, 1.06, **TURN_PROF[kh['hair']])
        w = _turn_widths(L)                                         # the house outline's rows are few: between the
        wv = lambda v: float(np.interp(v, [q[0] for q in w], [q[1] for q in w]))   # crown's end and the temples
        c0 = prof['crown'][-1][1]                                   # the skull stepped in (a notch, spikes in the
        prof['crown'] = prof['crown'] + [(v, max(c0, wv(v))) for v in (0.15, 0.3, 0.43)]   # hair); held round here
        TH.register(TH.Person(key, lambda sp2, _kh=kh: face_layout(_kh), -0.42, 0.4, lambda L, _p=prof: _p,
                              sp['skin'], tuple(kh.get('iris_c') or kh['eyes'].get('iris') or (66, 46, 34)),
                              sp['brow_c'], kh['lip'], _turn_mood, _turn_mouth, _turn_hair, face=_turn_face,
                              over=_turn_over, brow_thick=kh.get('brow_thick', 0.05), widths=_turn_widths))
    return key


def install_turned():
    """Once: a house head's turned views (three-quarter, side, three-quarter behind, behind) through its own turnhead
    Person: its measured face carried round the head, its colours, age lines and glasses, its hair piece turned;
    drawn at the house's bigger head size, lifted as the front is. Ears hidden under braids."""
    import turnhead as TH
    V = PP.V
    if 'kit_house' in V.TURNED_HEADS:
        return

    def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
        kh = sp.get('kit_house')
        if kh and view in TH.YAW:
            key = _turn_person(sp)
            with PP._Big():
                return TH.draw(img, p, dict(sp, who=key, ears_hidden=kh['hair'] == 'braids' and not kh.get('ears')),
                               t, view, hx, PP._lift(hy))
        return V.NOT_MINE
    V.TURNED_HEADS['kit_house'] = head_view     # one list of turned heads in views.py, newest tried first


# ---------------------------------------------------------------------------------------------- the person
def caricature(meas, push=1.0, tune=None):
    """The caricaturist's push (chat 8, Sam: "we are allowed to play with face shapes in the house style"): each
    measure moved further from real faces' middle (FA.AVG), by push, times tune[measure] where a person's lines name
    one; push 1 and no tune is the pick as measured. What makes this face THIS face grows; nothing new is invented."""
    tune = tune or {}
    return {k: (FA.AVG[k] + push * tune.get(k, 1.0) * (v - FA.AVG[k])) if k in FA.AVG else v for k, v in meas.items()}


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
    if 'brow_c' in kw:                                      # (and her brows, lighter and finer than the photo's)
        d['brows'] = tuple(kw.pop('brow_c'))
    if 'hair_c' in kw:                                      # Brexit Is Done: the hair's colour set by eye where the
        d['hair_c'] = tuple(kw.pop('hair_c'))               # photos' lighting tints it (May's silver read brown)
    if 'neck_w' in kw:                                      # the person's lines: a wider neck (Kemi's, K1)
        d['neck_w'] = kw.pop('neck_w')
    if d['tie'] is not None:
        d['tie'] = tuple(d['tie'])
    sp = people.person(d)
    if 'brow_up' in kw:                                     # the person's resting brows (a pair: one raised)
        sp['brow_up'] = tuple(kw.pop('brow_up')) if isinstance(kw['brow_up'], list) else kw.pop('brow_up')
    sp['hair'] = 'bald'                                    # the engine's own hair: none (the head part draws it all)
    if kw.pop('specs', None):                               # Brexit Is Done: glasses the pick's photos lacked (Kemi
        kw['glasses'] = dict(cx=0.3, w=2.5, top=-0.42, bot=1.05, rim_w=0.1, colr=(44, 32, 30), round=0.3)  # on site)
    kw.setdefault('head', True)                             # chat 16: every face's whole head measured (but the
    kh = dict(pk, look=look, hair=hair, lip=d['lips'], **kw)  # finished pair's: CAST says head=False)
    kh['meas'] = caricature(pk['meas'], kh.pop('push', 1.0), kh.pop('tune', {}))
    if kh['age'] and lk['age_k']:
        kh['age'] = dict(kh['age'], boost=kh.get('age_boost', 1.0))
    sp.update(kit_head='house', kit_house=kh, neck_shade=True)
    if hair == 'braids':                                    # the plaits behind the neck repaint it and lay the
        sp['neck_redrawn'] = True                           # collar again: the front torso leaves the collar to them
    return sp


CAST = {   # the test pair (Sam, 14 Nov): the lines a people file would hold. Chat 9, Sam's sheet notes: Andy is
           # finished at chat 7's head (no push, grin, lashes or tie); Kemi back to that head but for the bigger plaits,
           # her ears hidden (Sam: "her hair hides her ears"), her thin arched brows (her photos; Sam: "try the eyebrows"), the small pupils in her own big dark iris under a heavier, calm upper lid (chat 8's were wide and
           # startled), and her face's outline traced off her three front photos (shape)
    'burnham': dict(hair='swept', outfit=('suit', (31, 34, 58)), shirt=(246, 246, 246), tie=None, quiff=0.05,
                    hairline=-0.07, brow_thick=0.058, head=False),
    'badenoch': dict(hair='braids', outfit=('suit', (30, 32, 58)), shirt=(246, 246, 246), height=1.7, collar='open',
                     brow_thick=0.032, brow_arch=0.03, brow_taper=0.6, neck_w=1.2, plait_k=1.2, iris_r=0.98, pupil_r=0.28, iris_c=(56, 36, 26),
                     lid=0.24, shape=True, head=False),
    'walliams': dict(hair='swept', outfit=('suit', (31, 34, 58)), shirt=(246, 246, 246), tie=None,   # chat 13: his
                     mouth=dict(kind='smirk'), brow_up=[0.0, 0.025], push=1.1),   # smirk and cocked brow
                                                                         # (Blessed's hand-made, Sam: "That's him")
    'mcfadden': dict(hair='bald', outfit=('suit', (40, 42, 56)), shirt=(246, 246, 246), tie=(70, 96, 140),   # Milburn
                     grey=(184, 170, 156), ear_k=1.3, side_proud=0.034, dome=-0.33, dome_wide=0.405),   # chat 5: bald, grey-ginger sides, his ears
    'may': dict(hair='bob', outfit=('suit', (118, 38, 92)), shirt=(246, 246, 246), height=1.73, collar='open',   # Brexit
                pearls=True, hair_c=(208, 202, 192), brow_c=(150, 124, 108), brow_thick=0.034, age_boost=1.5,
                brow_arch=0.03, brow_taper=0.5, head=False),                                                                     # Is Done, 23 Nov: first try
    'blair': dict(hair='back', ear_k=1.35, lift=0.08, hair_c=(208, 204, 198), back_crown=-0.54, outfit=('suit', (28, 30, 40)), shirt=(246, 246, 246), tie=(150, 30, 40), height=1.83,
                  mouth=dict(kind='grin'), head=False),                                          # (Brexit Is Done)
}


def install():
    import people
    PP.B.HEADS  # noqa: B018  (the hooks are installed on import)
    people.install({})
    TC = PP.B                                    # the engine holds each look's head and torso (HEADS, TORSOS)
    return TC


def dome_faults(name, lines=None, src=None, variant=None):
    """Rule 49's head-shape step (Milburn note 4, 17 Nov: Pat McFadden's bald dome passed the likeness test at 62% and
    Sam saw "an alien carrot man": the skull drawn 1.9x as tall over its widest row as its half width, widest down at
    the cheeks). A bald head's drawn skull must be widest at or above the eyes (v <= 0.05 face heights) and no taller
    over that row than 1.1x its half width (real skulls, measured off Pat's photos: a near half-circle, 0.76)."""
    c = dict(lines if lines is not None else CAST.get(name, {}))
    if c.get('hair') != 'bald':
        return []
    kh = person(name, 'detail', src=src, variant=variant, **c)['kit_house']
    L = face_layout(kh)
    L['round_top'], L['dome'], L['dome_wide'] = True, kh.get('dome', -0.44), kh.get('dome_wide')
    fo = face_outline(L)
    def half(v):
        r = [abs(u0 + (v - v0) / (v1 - v0) * (u1 - u0)) for (u0, v0), (u1, v1) in zip(fo, fo[1:] + fo[:1])
             if (v0 - v) * (v1 - v) < 0]
        return max(r) if r else 0.0
    top = min(v for _, v in fo)
    vs = np.linspace(top + 0.005, 0.3, 60)
    ws = [half(v) for v in vs]
    k = int(np.argmax(ws))
    tall = (vs[k] - top) / max(ws[k], 1e-6)
    out = []
    if vs[k] > 0.05:
        out.append(f'HEAD SHAPE: {name}: the bald skull is widest at the cheeks ({vs[k]:.2f} face heights down), not '
                   'the temples: a narrow dome (Milburn note 4, "alien carrot man")')
    if tall > 1.1:
        out.append(f'HEAD SHAPE: {name}: the bald dome is {tall:.1f}x as tall as its half width (a real skull is a near '
                   'half-circle, under 1.1x): "alien carrot man" (Milburn note 4)')
    return out


def draw(name, look, out, size=900, lines=None, src=None, variant=None):
    """One head and shoulders, front on, on white: the people kit's person with the house head. `lines`: the
    person's house lines (CAST's for that face otherwise); `src`/`variant`: one of facepick's heads (load())."""
    from PIL import Image
    from satire_style import install_circle_hands
    B, V = PP.B, PP.V
    install_circle_hands(B)
    TC = install()
    sp = person(name, look, src=src, variant=variant, **(lines if lines is not None else CAST[name]))
    for f in dome_faults(name, lines, src, variant):       # rule 49: the head's shape, before anyone sees it
        print(f)
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
    B, V = PP.B, PP.V
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




def compare(out, name, beside=None, T=440, title=None, turned=False):
    """The whole-head sheet (chat 16): two front photos, a head Sam knows (`beside`: a people-file entry such as
    Blessed's 'walliams', drawn by the people kit), the head before (the house outline: head=False) and the head
    from the measured shape; a phone-size row under them."""
    from PIL import Image, ImageDraw, ImageFont
    import people
    import facepick as FP
    from satire_style import install_circle_hands
    B, V = PP.B, PP.V
    install_circle_hands(B)
    TC = install()
    tmp = os.path.join(os.path.dirname(os.path.abspath(out)), '_facehouse')
    os.makedirs(tmp, exist_ok=True)
    font = lambda n: ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)   # noqa: E731
    pk = json.load(open(pick_file(name)))
    tiles, heads = [], []
    for ph in pk['fronts'][:2]:
        im, _ = FP._face_tile(os.path.join(ROOT, ph), None, T)
        sq = Image.new('RGB', (T, T), (255, 255, 255))
        im = im.convert('RGB')
        im.thumbnail((T, T))
        sq.paste(im, ((T - im.width) // 2, (T - im.height) // 2))
        tiles.append(sq)
        heads.append('photo')
    if beside:
        film, who = beside
        d = people.parse(open(people.people_file(film)).read())[who]
        sp = people.person(d)
        people.install({who: sp})
        B.SS = 1
        tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
        V.person(tile, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(sp), 0.0, 0)
        tiles.append(_fit(tile.crop((150, 280, 930, 1180)), T))
        heads.append('Blessed: "that\'s him"')
    for lab, hd, sp_ in (('before', False, None), ('true to the photos', True, 1.0),
                         ('NEW: proportions pushed', True, SHAPE_PUSH)):
        png = os.path.join(tmp, f'{name}-{hd}-{sp_}.png')
        ln = dict(CAST.get(name, {}), head=hd)
        if sp_:
            ln['shape_push'] = sp_
        draw(name, 'detail', png, lines=ln)
        tiles.append(_fit(Image.open(png), T))
        heads.append(lab)
    img = Image.new('RGB', (20 + len(tiles) * (T + 16), 120 + T + T // 3 + 40), (236, 232, 226))
    d = ImageDraw.Draw(img)
    d.text((20, 20), title or f'{name.title()}: the head\'s whole shape read off the photos', font=font(32), fill=(30, 30, 30))
    for k, (tl, h) in enumerate(zip(tiles, heads)):
        x = 20 + k * (T + 16)
        img.paste(tl, (x, 100))
        d.text((x + 4, 70), h, font=font(22), fill=(30, 30, 30))
        sm = tl.resize((T // 3, T // 3))
        img.paste(sm, (x, 100 + T + 20))
    if turned:                                            # the new head turned, front to behind, under the row
        tj = turns(os.path.join(tmp, f'{name}-turns.jpg'), [name])
        tv = Image.open(tj)
        tv = tv.resize((img.width - 40, int(tv.height * (img.width - 40) / tv.width)))
        full = Image.new('RGB', (img.width, img.height + tv.height + 10), (236, 232, 226))
        full.paste(img, (0, 0))
        full.paste(tv, (20, img.height))
        img = full
    img.save(out, quality=90)
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
    elif a and a[0] == 'measure':
        print(measure_head(a[1], a[2] if len(a) > 2 else None))
    elif a and a[0] == 'compare':
        b = [x for x in a[3:] if ':' in x]
        print(compare(a[1], a[2], tuple(b[0].split(':')) if b else None, turned='--turns' in a))
    elif a and a[0] == 'head':
        print(draw(a[1], a[2], a[3]))
    else:
        print(__doc__)
