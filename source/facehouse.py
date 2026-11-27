#!/usr/bin/env python3
"""MAP  facehouse (face tool chat 6, 14 Nov; Sam: "rebuild the face tool on the house head"). The face tool's heads
drawn the HOUSE way (Ad-vanced Notice, Blessed: the hand-made Walliams and Brand are the models), not traced off the
photo: the house outline, ears, eyes, brows, nose and lips (patriots4) at the house's bigger head size, on the
people kit's body and clothes; the hair a drawn house piece (shapes with an ink edge and a few strokes), the glasses,
age lines and braids from the face tool's measures, redrawn in house weights. What the face tool measured and Sam
picked (references/faces/NAME/pick/NAME-pick.json: the tuned measures of his pick, the colours, glasses, age lines,
eyes) is read as it is; nothing here is keyed by name except the hair piece the person's lines name.

PARTS: one module in 3 files (cost-spike fix 5c; parts.py runs them inside facehouse, so setters reach all):
  facehouse_b.py (the brows checked); facehouse_c.py (hair: braids). Import facehouse, never a part; touch.py NAME
  gives the file and line.

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

    long     B2 (27 Nov, replay test 2: Ocasio-Cortez came out in May's bob): long straight hair, middle parting, past
             the shoulders: the braids' measured shape as one smooth mass, a few long strands, a sheen, a straight cut;
             turned through the braids' code (plaited False); facepick's hair_fit names it for long hair
BEARD (B1, 27 Nov): a pick's beard with style 'short' (facepick: beardkit coverage SHORT_BEARD 0.4 up, in the hair's
    colour; or `beard: short C` in the people file) is a solid short full beard (short_beard: sideburns to the clipped
    sides, wrapped round the turned head); every other beard the house stubble, exactly as before (beard()).

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
    """The closed curve, through each point once: ink.curve drops repeats itself now (R8 A4, 27 Nov)."""
    return _curve(pts, n)
from faces import blend               # noqa: E402
from ink import open_curve                        # noqa: E402
import turnhead as TH  # noqa: E402
import focus as FO                               # noqa: E402  (C2: where a front-on head looks)
import parts as _PARTS        # noqa  (cost-spike fix 5c: this module is kept in parts; parts.py)

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


_PARTS.include(globals(), 'facehouse_b', 'facehouse_c', 'facehouse_d')
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
