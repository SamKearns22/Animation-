#!/usr/bin/env python3
"""MAP  castsheet (Brexit Is Done chat 2, 23 Nov; Sam's notes on cast v1). The cast sheet Sam sees, built by a tool
(chat 1 cut crops of the people sheet by hand and cut the three-quarter figures in half: n1 "these side images
appear cut off?"), and the FRONT | THREE-QUARTER MATCH check (n2 Blair "not the same person and haircut as presented
in the straight on view"; n3 Kemi "the orange is gone from her clothes").

    sheet   each person a row: their reference photo, the head front and three-quarter at ONE scale, the full figure
            front and three-quarter at one scale. Every figure is drawn on a big tile and its own box found; a box
            touching the tile's edge is REFUSED (EdgeFault), never cropped (note n1).
    match   front and three-quarter drawn at one scale; each colour the front shows (quantised: hair, skin, jacket,
            sleeves, hat...) measured in both: its height (top to bottom over the figure's height) and its share of
            the figure. A colour whose height changes past 15%, or which loses past half its share (or is gone),
            is a fault: one person must read as the same person, haircut and clothes in every view.
            Tested on Sam's saved notes (`selftest`: the cast v1 pictures he marked must fail, and why).
            NOT SEEN (a gap, chat 3): LAYERING. match counts colours, never which piece lies on top, so a piece worn
            over the clothes drawn across the collar passes (Sam on cast v2, n6: "Kemi's orange detailing travels
            over her white collar"; notes/sam-notes/brexit-cast-v2/n6-*.jpg). To see it, the check would need each
            piece's own pixels (drawn once alone) to test that an over-piece never covers the collar or lapels.
            Nor does it know a build (n5: both women on the man's body): it compares a person with herself.

    python3 source/castsheet.py sheet FILM OUT.jpg [WHO ...]    the sheet (refuses on a figure touching an edge)
    python3 source/castsheet.py match FILM [WHO ...]            front | 3/4 faults, one line each
    python3 source/castsheet.py build FILM [WHO ...]            woman or man in every view; each woman on HER build;
                                                                 no line up from the crotch (note 8)
    python3 source/castsheet.py selftest                         the checks on Sam's saved notes (n2, n3, n5, n7)
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
BG = (255, 255, 255)
LIMIT = 0.15


class EdgeFault(Exception):
    pass


# ---------------------------------------------------------------------------------------------- drawing
def _setup(film, who):
    import people
    import people_parts as PP
    from satire_style import install_circle_hands
    B = PP.B
    install_circle_hands(B)
    cast = people.load(film)
    if who:
        cast = {k: v for k, v in cast.items() if k in who}
    cast = people.install(dict(cast))
    B.SS = 1
    return cast, PP


def draw(sp, yaw, PP, scale=1.0):
    """One person at `yaw`, full figure, on a big white tile; returns (RGB array, box (x0, y0, x1, y1))."""
    from PIL import Image
    B, V = PP.B, PP.V
    tile = Image.new('RGBA', (1080, 1920), BG + (255,))
    s = 0.5 * sp['height'] / 1.75                 # the people sheet's own placing (feet near y 880 at zoom 1)
    cam = B.Cam(2.0 * scale, 540, 470)            # zoomed in on the figure: twice the people sheet's size
    V.person(tile, cam, 540, 840 - 928 * s, s, dict(sp), 0.0, yaw)
    a = np.asarray(tile.convert('RGB'))
    return a, box(a)


def box(a, bg=BG, tol=12):
    m = (np.abs(a.astype(int) - bg).sum(2) > tol)
    ys, xs = np.nonzero(m)
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def touches(b, shape, pad=2):
    x0, y0, x1, y1 = b
    return x0 <= pad or y0 <= pad or x1 >= shape[1] - pad or y1 >= shape[0] - pad


def pair(sp, PP, scale=1.0):
    """Front and three-quarter at one scale: [(array, box)], refused if either touches its tile's edge."""
    out = []
    for yaw in (0, 45):
        a, b = draw(sp, yaw, PP, scale)
        if b is None or touches(b, a.shape):
            raise EdgeFault(f"{sp['name']} at {yaw}: the figure touches the tile's edge {b}")
        out.append((a, b))
    return out


# ---------------------------------------------------------------------------------------------- the match
def palette(a, b, k=7, bg=BG):
    """The front's main colours inside its box (k-means on its non-white pixels), ink left out."""
    import cv2
    x0, y0, x1, y1 = b
    px = a[y0:y1, x0:x1].reshape(-1, 3).astype(np.float32)
    keep = (np.abs(px - bg).sum(1) > 30) & (px.max(1) > 45)          # not the paper, not the ink
    px = px[keep]
    if len(px) > 60000:
        px = px[np.random.default_rng(1).choice(len(px), 60000, replace=False)]
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1.0)
    _, lab, cen = cv2.kmeans(px, k, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    share = np.bincount(lab.ravel(), minlength=k) / len(lab)
    return [c for c, s in zip(cen, share) if s > 0.015]


def measures(a, b, cols, href, near=38.0):
    """For each colour: its top and bottom as heights over the box's FOOT (the feet, or the head crop's cut line:
    the same place in both views; the top is no anchor, it is where the hair itself may have gone wrong), over the
    front's height `href` (one scale), and its share of the figure's coloured pixels."""
    x0, y0, x1, y1 = b
    crop = a[y0:y1, x0:x1].astype(np.float32)
    h = y1 - y0
    d = np.stack([np.abs(crop - c).sum(2) for c in cols])
    idx, best = d.argmin(0), d.min(0)
    coloured = (np.abs(crop - BG).sum(2) > 30) & (crop.max(2) > 45)
    total = max(1, int(coloured.sum()))
    out = []
    for i in range(len(cols)):
        m = (idx == i) & (best < near) & coloured
        n = int(m.sum())
        if n < 40:
            out.append(None)
            continue
        ys = np.nonzero(m)[0]                     # the colour's own body: 2nd to 90th percentile of its rows
        top, bot = np.percentile(ys, 2), np.percentile(ys, 90)   # (stray ink-edge greys and a far-off speck
        rows = np.array([top, bot])                              #  never stretch it)
        out.append(dict(top=(h - rows[0]) / href, bottom=(h - rows[1]) / href, share=n / total))
    return out


def compare(front, three, name='', limit=LIMIT):
    """Faults between a front (array, box) and a three-quarter (array, box) of the same person at one scale."""
    cols = palette(*front)
    hf = front[1][3] - front[1][1]
    ht = three[1][3] - three[1][1]
    mf, mt = measures(*front, cols, hf), measures(*three, cols, hf)
    faults = []
    if abs(ht - hf) / hf > limit:
        faults.append(f'{name}: the whole figure is {ht / hf:.2f} times as tall turned')
    for c, f, t in zip(cols, mf, mt):
        if f is None or f['share'] < 0.03:
            continue
        rgb = tuple(int(v) for v in c)
        if t is None or t['share'] < f['share'] * 0.5:
            faults.append(f"{name}: colour {rgb} ({f['share']:.0%} of the front) is "
                          f"{'gone' if t is None else format(t['share'], '.0%')} turned")
            continue
        span_f, span_t = f['top'] - f['bottom'], t['top'] - t['bottom']
        if span_f < 0.05:
            continue
        if abs(t['top'] - f['top']) > limit * span_f:
            faults.append(f"{name}: colour {rgb}: its top is {f['top']:.2f} up from the front, {t['top']:.2f} turned "
                          f"({abs(t['top'] - f['top']) / span_f:.0%} of its height)")
        elif (span_f - span_t) / span_f > limit:   # shorter or flatter turned (longer is the side seen: hair over
                                                    # the ear, a sleeve's length)
            faults.append(f'{name}: colour {rgb} runs {span_f:.2f} of the height from the front, {span_t:.2f} '
                          f'turned ({abs(span_t - span_f) / span_f:.0%} off)')
    return faults


def match(film, who=None, scale=1.0):
    cast, PP = _setup(film, who)
    out = []
    for w, sp in cast.items():
        try:
            (af, bf), (at, bt) = pair(sp, PP, scale)
        except EdgeFault as e:
            out.append(str(e))
            continue
        head_f, head_t = _head(af, bf, sp), _head(at, bt, sp)
        out += compare(head_f, head_t, f'{w} head')
        out += compare((af, bf), (at, bt), f'{w} figure')
    return out


def _head(a, b, sp):
    """The head and shoulders: the figure's top down to 0.3 of its height (the hat, hair and collar)."""
    x0, y0, x1, y1 = b
    cut = y0 + int(0.3 * (y1 - y0))
    sub = a[:cut].copy()
    bb = box(sub[y0:cut])
    if bb is None:
        return a, b
    return a, (bb[0], y0 + bb[1], bb[2], y0 + bb[3])


# ---------------------------------------------------------------------------------------------- the sheet
def sheet(film, out, who=None, scale=1.0):
    from PIL import Image, ImageDraw, ImageFont
    cast, PP = _setup(film, who)
    font = lambda n: ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)   # noqa: E731
    refs = _refs(film)
    HT, FT, GAP = 420, 760, 14                    # head tile height, figure tile height
    rows = []
    BOXES.clear()
    for w, sp in cast.items():
        (af, bf), (at, bt) = pair(sp, PP, scale)  # raises EdgeFault: never a cut figure
        hf, ht_ = _head(af, bf, sp), _head(at, bt, sp)
        hk = HT * 0.86 / max(hf[1][3] - hf[1][1], ht_[1][3] - ht_[1][1])
        fk = FT * 0.92 / max(bf[3] - bf[1], bt[3] - bt[1])
        tiles = []
        ref = refs.get(w)
        if ref:
            im = Image.open(ref).convert('RGB')
            im.thumbnail((int(HT * 1.1), HT))
            tiles.append(('photo', im, HT))
        for lab, (a, b), k, th in (('front', hf, hk, HT), ('three-quarter', ht_, hk, HT),
                                   ('front', (af, bf), fk, FT), ('three-quarter', (at, bt), fk, FT)):
            x0, y0, x1, y1 = b
            pad = int(0.04 * (y1 - y0))
            im = Image.fromarray(a[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad])
            im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
            tiles.append((lab, im, th))
        rows.append((sp['name'].split(' (')[0].replace(' on site', ''), tiles))   # the name only: no working words
    width = 40 + max(sum(t[1].width + GAP for t in tiles) for _, tiles in rows)
    height = 70 + sum(60 + max(t[2] for t in tiles) + 40 for _, tiles in rows)
    img = Image.new('RGB', (width, height), (236, 232, 226))
    d = ImageDraw.Draw(img)
    d.text((20, 16), 'The cast: front and three-quarter at one scale', font=font(30), fill=(30, 30, 30))
    y = 70
    for name, tiles in rows:
        d.text((20, y), name, font=font(26), fill=(30, 30, 30))
        x, top = 20, y + 40
        rh = max(t[2] for t in tiles)
        for lab, im, th in tiles:
            BOXES.append(dict(name=f'{name}: {lab}', box=[x, top, x + im.width, top + th]))
            d.rectangle([x - 4, top - 4, x + im.width + 4, top + th + 4], fill=(255, 255, 255))
            img.paste(im, (x, top + (th - im.height) // 2 if lab == 'photo' else top + th - im.height))
            d.text((x, top + th + 6), lab, font=font(18), fill=(90, 90, 90))
            x += im.width + GAP + 8
        y = top + rh + 40
    img.save(out, quality=88)
    import json
    json.dump([b for b in BOXES if not b['name'].endswith('photo')], open(os.path.splitext(out)[0] + '-boxes.json', 'w'))
    return out


BOXES = []   # each tile's box on the last sheet (for the critique's close-ups: OUT-boxes.json beside the sheet)


def _refs(film):
    """A reference photo per person: the people file's comment names it (`references/FILM/NAME*.jpg`)."""
    import glob
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'references', film, '*.jpg'))):
        base = os.path.basename(f)
        for w, keys in (('may', ('may-interview-1',)), ('kemi', ('badenoch',)), ('blair', ('blair',))):
            if any(base.startswith(k) for k in keys) and w not in out:
                out[w] = f
    return out


# ---------------------------------------------------------------------------------------------- Sam's notes
SELFTEST = os.path.join(ROOT, 'notes', 'sam-notes', 'brexit-cast-v1')
CASES = [   # Sam's marked pictures: (file, front box, three-quarter box, must fail?, his words)
    ('n2-blair-threequarter-not-same.jpg', (2, 58, 482, 562), (510, 58, 1015, 562), True,
     'not the same person and haircut as presented in the straight on view'),
    ('n3-kemi-orange-gone-threequarter.jpg', (135, 100, 635, 505), (668, 100, 1124, 505), True,
     'the orange is gone from her clothes'),
]


def selftest():
    from PIL import Image
    ok = True
    for f, fb, tb, bad, words in CASES:
        a = np.asarray(Image.open(os.path.join(SELFTEST, f)).convert('RGB'))
        fa, ta = a[fb[1]:fb[3], fb[0]:fb[2]], a[tb[1]:tb[3], tb[0]:tb[2]]
        bg = tuple(int(v) for v in np.median(np.concatenate([fa[:6].reshape(-1, 3), ta[:6].reshape(-1, 3)]), 0))
        fbx, tbx = box(fa, bg, 40), box(ta, bg, 40)
        global BG
        old, BG = BG, bg
        try:
            faults = compare((fa, fbx), (ta, tbx), f)
        finally:
            BG = old
        print(('CAUGHT' if faults else 'MISSED') if bad else ('PASS' if not faults else 'FALSE'), f, f'("{words}")')
        for x in faults:
            print('   ', x)
        ok &= bool(faults) == bad
    # n1: the sheet cut the three-quarter figures in half: a figure box on the tile's edge is refused
    a = np.asarray(Image.open(os.path.join(SELFTEST, 'n1-sheet-cut-off.jpg')).convert('RGB'))
    print('n1-sheet-cut-off.jpg: the edge test is in pair() (a box on the tile edge raises EdgeFault);',
          'tested on a figure drawn too big:', end=' ')
    cast, PP = _setup('brexit-is-done', ['kemi'])
    try:
        draw_ok = pair(next(iter(cast.values())), PP, scale=4.0)
        print('MISSED')
        ok = False
    except EdgeFault:
        print('CAUGHT')
    return ok


# ---------------------------------------------------------------------------------------------- the build check
# Open Wounds chat 6 (24 Nov). Sam's note 5 on cast v2 ("I'm not sure we have female bodies? Kemi's body seems much
# more like a man's"; notes/sam-notes/brexit-cast-v2/n5-*.jpg: both women on the man's box) and note 7 on the first
# woman's build ("Kemi Badenoch just does not have that body. Looks good for May though!": one hourglass for every
# woman). Two questions, every person, every turned view, read from the drawing's own torso outline (views.
# torso_outline: exact, no guessing from pixels; a reading of saved pictures was tried and found unreliable: heads
# and hands move its landmarks):
#   SHAPE     does the body read as a woman's or a man's? Hip over waist at least WOMAN_HIP_WAIST. Measured on
#             every build at four turns (chat 6): women 1.08 (Kemi's own build, three-quarter: the weakest) to 1.34,
#             men 0.94 (the house box) to 1.05 (Jason's 'man'). Hip over chest was tried and dropped: it failed Lucia
#             three-quarter (0.89), a woman Sam approved.
#   LIKENESS  is it HER body? Each woman's front widths (bust, waist, hip over the outer shoulder) against the ones
#             measured from her own photos (references/FILM/WHO-build.json, written by the measuring step), within
#             LIKE_TOL; or Sam's own words approving that exact build. A woman with neither is a fault: never guessed.
WOMAN_HIP_WAIST, LIKE_TOL = 1.07, 0.05
SHAPE_VIEWS = ('front', 'three', 'three_back', 'back')
BANDS = dict(chest=(160, 220, max), waist=(220, 320, min), hip=(380, None, max))


def _width_at(poly, y):
    xs = []
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 - y) * (y1 - y) <= 0 and y0 != y1:
            xs.append(x0 + (x1 - x0) * (y - y0) / (y1 - y0))
    return (max(xs) - min(xs)) if len(xs) >= 2 else 0.0


def torso_shape(sp, view):
    """Chest, waist and hip widths of the person's torso in a view (body units), as the drawing makes it."""
    import views as V
    bottom = sp.get('bottom', V.JACKET)
    poly = [tuple(map(float, q)) for q in V.torso_outline(sp, view, bottom)]
    out = {}
    for k, (a, b, f) in BANDS.items():
        out[k] = f(_width_at(poly, y) for y in range(a, int(b or bottom - 6), 4))
    return out


def reads_as(m):
    return 'woman' if m['hip'] >= WOMAN_HIP_WAIST * m['waist'] else 'man'


def front_widths(sp):
    """Bust, waist, hip over the outer shoulder (the arm tops: 2 (sw + 20.5)), at the measuring step's heights."""
    import body as B
    sw = sp.get('shoulders', 150)
    W = 2 * (sw + 20.5)
    return {n: round(2 * B.fig_half(sp.get('figure'), y, sw, sp.get('bottom', 505)) / W, 2)
            for n, y in (('bust', 200), ('waist', 275), ('hip', 470))}


def _measured(film, w):
    import json
    p = os.path.join(ROOT, 'references', film, f'{w}-build.json')
    return json.load(open(p)) if os.path.exists(p) else None


def build_faults(film, who=None, cast=None, measured=None):
    """One line per fault: a woman drawn on a man's shape (any view), a man drawn on a woman's, a woman whose build
    is not hers (or was never measured from her photos)."""
    if cast is None:
        cast, _ = _setup(film, who)
    out = []
    for w, sp in cast.items():
        sex = sp.get('sex')
        if sex not in ('woman', 'man'):
            continue
        for view in SHAPE_VIEWS:
            m = torso_shape(sp, view)
            if reads_as(m) != sex:
                out.append(f"BUILD {w} ({sex}) reads as a {reads_as(m)} {view}: hip {m['hip'] / m['waist']:.2f} of "
                           f"the waist (a woman's: at least {WOMAN_HIP_WAIST}; Sam's note 5)")
        if sex != 'woman':
            continue
        ref = (measured or {}).get(w, 'look') if measured is not None else _measured(film, w)
        if ref == 'look':
            ref = _measured(film, w)
        if not ref:
            out.append(f'BUILD {w}: her build was never measured from her own photos (references/{film}/{w}-build.json; '
                       f"notes/learn/kemi-build/measure.py shows how): one woman's body for every woman is note 7's fault")
            continue
        if ref.get('approved'):
            if ref.get('figure') != sp.get('figure'):
                out.append(f"BUILD {w}: Sam approved build {ref.get('figure')!r} ({ref['approved']}), she is drawn on "
                           f"{sp.get('figure')!r}")
            continue
        got = front_widths(sp)
        off = {k: (got[k], v) for k, v in ref['widths'].items() if abs(got[k] - v) > LIKE_TOL}
        if off:
            out.append(f'BUILD {w}: not her body (her photos, references/{film}/{w}-build.json): ' + ', '.join(
                f'{k} drawn {a:.2f}, photos {b:.2f}' for k, (a, b) in off.items()) + " (Sam's note 7)")
    return out


# Where the legs part (Open Wounds chat 7, Sam's note 8 on the women's new legs: "This is a bit...camel toe";
# notes/sam-notes/brexit-cast-v3/n8-camel-toe.jpg: the full thighs overlapped down the middle and the near thigh's
# inner line ran up from where the legs part, deep into the trousers). From the gap between the feet, up the middle
# to the crotch, then any outline line carrying on up through the trousers' own colour is measured, over the legs'
# width there. A crotch is a small round point (the legs part, the line turns aside); a seam line up into the cloth
# is the fault. Read from the drawing (front and back, every woman and man), so any build and any trousers are seen.
CROTCH_MAX = 0.12


def crotch_line(a):
    """An RGB picture of a standing figure's legs on white (feet at the bottom): the ink line running up from the
    crotch through the trousers, over the legs' width there (0: none). None when the legs never part."""
    g = a.astype(int).sum(2) / 3.0
    bg = g > 200
    H, W = g.shape
    y = H - max(3, H // 12)
    xs = np.nonzero(~bg[y])[0]
    if len(xs) < 2:
        return None
    runs = [x for x in range(xs.min(), xs.max()) if bg[y, x]]
    if not runs:
        return None
    x = int(np.median(runs))
    while y > 0 and bg[y - 1, max(0, x - 1):x + 2].any():
        y -= 1
    yc = y
    cloth = np.median(a[H - H // 6:][~bg[H - H // 6:]].astype(int), 0)
    near = lambda yy, xx: (0 <= xx < W) and np.abs(a[yy, xx].astype(int) - cloth).sum() < 60   # noqa: E731
    run, miss, yy = 0, 0, yc - 4                 # the gap's own top edge (soft in a saved picture): up to 16 rows
    while yy > 0 and (miss <= 4 or (run == 0 and yy > yc - 20)):   # before a line starts
        wide = g[yy, max(0, x - 30):x + 31]
        if (wide < cloth.mean() - 10).mean() > 0.8:   # a hem line across: the trousers end (a jacket above)
            break
        seg = g[yy, max(0, x - 4):x + 5]
        ink = seg.min() < cloth.mean() - 8 if near(yy, x - 12) and near(yy, x + 12) else False
        if ink:
            run, miss = run + 1 + miss, 0
        else:
            miss += 1
        yy -= 1
    row = np.nonzero(~bg[min(H - 1, yc + 4)])[0]
    width = (row.max() - row.min()) if len(row) else 1
    return run / max(1.0, float(width))


def crotch_faults(film, who=None, cast=None):
    """Every standing person front and back: the line up from the crotch (crotch_line) under CROTCH_MAX."""
    from PIL import Image
    import views as V
    import body as B
    if cast is None:
        cast, _ = _setup(film, who)
    out = []
    for w, sp in cast.items():
        for yaw, name in ((0, 'front'), (180, 'back')):
            tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
            s = 0.5 * sp['height'] / 1.75
            y0 = 840 - 928 * s
            V.person(tile, B.Cam(2.0, 540, 470), 540, y0, s, dict(sp), 0.0, yaw, None)
            top = int((y0 + 400 * s - 470) * 2.0 + 960)
            knee = int((y0 + 760 * s - 470) * 2.0 + 960)
            got = crotch_line(np.asarray(tile.convert('RGB'))[top:knee])
            if got is not None and got > CROTCH_MAX:
                out.append(f"CROTCH {w} {name}: a line runs up from where the legs part, {got:.2f} of the legs' width "
                           f"(at most {CROTCH_MAX}; Sam's note 8, \"camel toe\")")
    return out


# The blind judge (Change 1: "a fresh helper that hasn't seen the cast list says man or woman at phone size"). Chat
# 6 found the shape test alone too weak: it passed Kemi three-quarter (hip 1.08 of the waist, just over the line)
# while the judge called her a man there and seated ("boxy straight torso, no waist"): her arms and the straight
# jacket hide the shape. So a woman (or a man) must also be read right by the judge in every view, with confidence
# JUDGE_MIN or more, on outlines drawn from the CURRENT drawing: the record (notes/judge/FILM-cast.json) is stale once
# the cast file or the drawing code changes after it (git: a newer commit on those files, or unsaved edits).
JUDGE_MIN = 3
JUDGES = 3        # Open Wounds chat 7: three fresh judges a round, the middle verdict kept (notes/judge/FILM-cast.json
#                   'judges' holds each one's lines): a single judge's score moved by a point on figures that had not
#                   changed (Kemi front 3, then 2), so one judge could pass or fail a view by luck
JUDGE_FILES = ('story/{film}-people.txt', 'source/body.py', 'source/views.py', 'source/people.py',
               'source/people_parts.py', 'source/sitting.py')


def judge_faults(film, who=None):
    import json
    import subprocess
    p = os.path.join(ROOT, 'notes', 'judge', f'{film}-cast.json')
    if not os.path.exists(p):
        return [f'JUDGE: no blind judge has read this cast (notes/judge/{film}-cast.json; notes/learn/kemi-build/judge.py '
                'makes the outlines)']
    rec = json.load(open(p))
    files = [f.format(film=film) for f in JUDGE_FILES]
    git = lambda *a: subprocess.run(['git', '-C', ROOT] + list(a), capture_output=True, text=True).stdout.strip()
    t_rec = git('log', '-1', '--format=%ct', '--', os.path.relpath(p, ROOT))
    t_draw = git('log', '-1', '--format=%ct', '--', *files)
    dirty = git('status', '--porcelain', '--', *files)
    out = []
    if dirty or (t_rec and t_draw and int(t_draw) > int(t_rec)) or not t_rec:
        out.append(f'JUDGE: the judge\'s record is older than the drawing (or not committed after it): draw the outlines '
                   'again and ask a fresh judge')
    if len(rec.get('judges') or {}) < JUDGES:
        out.append(f'JUDGE: the record holds {len(rec.get("judges") or {})} judge(s); a round needs {JUDGES} fresh ones, each '
                   'verdict the middle of theirs (chat 7: one judge moved a point on unchanged figures)')
    cast, _ = _setup(film, who)
    for v in rec['verdicts']:
        sex = cast.get(v['who'], {}).get('sex')
        if sex and (v['said'] != sex or v['conf'] < JUDGE_MIN):
            out.append(f"JUDGE: {v['who']} ({sex}) {v['view']}: the blind judge said {v['said']} ({v['conf']} of 5): "
                       f"\"{v['why']}\"")
    return out


def _n5_picture(f, box_):
    """The saved n5 picture's own front figure: hip over waist of its silhouette (the head and feet left out by the
    tile's box: arms included, as Sam saw it), so the selftest proves its redraw is the picture's state."""
    from PIL import Image
    a = np.asarray(Image.open(os.path.join(ROOT, 'notes', 'sam-notes', 'brexit-cast-v2', f)).convert('RGB'))
    t = a[box_[1]:box_[3], box_[0]:box_[2]].astype(int)
    m = np.abs(t - np.median(t[:5].reshape(-1, 3), 0)).sum(2) > 40
    wid = np.array([(np.ptp(np.nonzero(r)[0]) if r.any() else 0) for r in m], float)
    ys = np.nonzero(wid)[0]
    H = ys.max() - ys.min()
    mid = wid[ys.min() + int(0.40 * H)]
    sh = int(np.argmax(wid > 0.92 * mid))
    L = int(0.30 * H)                             # the jacket: about 30% of the figure below the shoulders
    return wid[sh + int(0.70 * L):sh + int(0.84 * L)].max() / wid[sh + int(0.35 * L):sh + int(0.65 * L)].min()


def build_selftest():
    """Trusted only when it catches Sam's notes 5 and 7 and passes Lucia (a woman) and Blair (a man)."""
    ok = True
    cast, _ = _setup('brexit-is-done', None)
    n5 = {w: dict(cast[w], figure=None) for w in ('may', 'kemi')}       # cast v2: both on the house (man's) body
    for w, f in (('may', 'n5-may-body.jpg'), ('kemi', 'n5-kemi-body-like-a-mans.jpg')):
        pic = _n5_picture(f, (1190, 30, 1455, 790))
        got = build_faults('brexit-is-done', cast={w: n5[w]}, measured={})
        hit = any('reads as a man' in g for g in got)
        print(('CAUGHT' if hit else 'MISSED'), f'n5 {w} (the saved picture\'s hips {pic:.2f} of its waist: a box; '
              f'"Kemi\'s body seems much more like a man\'s")', '|', (got or ['-'])[0][:110])
        ok &= hit and pic < WOMAN_HIP_WAIST
    v1 = {'kemi': dict(cast['kemi'], figure='female')}                  # note 7: May's hourglass on Kemi
    got = build_faults('brexit-is-done', cast=v1)
    hit = any('not her body' in g for g in got)
    print('CAUGHT' if hit else 'MISSED', 'n7 kemi on the hourglass ("Kemi Badenoch just does not have that body")',
          '|', (got or ['-'])[0][:120])
    ok &= hit
    from PIL import Image
    pic = crotch_line(np.asarray(Image.open(os.path.join(ROOT, 'notes', 'sam-notes', 'brexit-cast-v3',
                                                         'n8-camel-toe.jpg')).convert('RGB')))
    hit = pic is not None and pic > CROTCH_MAX
    print('CAUGHT' if hit else 'MISSED', f'n8 camel toe (the saved picture: a line {pic or 0:.2f} of the legs\' '
          'width up from the crotch)', '|', '-')
    ok &= hit
    got = crotch_faults('brexit-is-done', cast={w: cast[w] for w in ('kemi', 'may', 'blair')})
    print('PASS' if not got else 'FAIL', 'the cast now: no line up from the crotch', '|', (got or ['-'])[0][:110])
    ok &= not got
    gta, _ = _setup('grand-theft-autism', ['lucia'])
    lu = dict(gta['lucia'], sex='woman')
    got = [g for g in build_faults('grand-theft-autism', cast={'lucia': lu}, measured={'lucia': {'approved': 'GTA, '
           '20 Nov: measured from the game\'s art', 'figure': 'woman'}})]
    print('PASS' if not got else 'FALSE', 'Lucia reads as a woman in every view', '|', (got or ['-'])[0][:100])
    ok &= not got
    got = build_faults('brexit-is-done', cast={'blair': cast['blair']})
    print('PASS' if not got else 'FALSE', 'Blair reads as a man in every view', '|', (got or ['-'])[0][:100])
    ok &= not got
    return ok


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['sheet']:
        print(sheet(a[1], a[2], a[3:] or None))
    elif a[:1] == ['match']:
        fs = match(a[1], a[2:] or None)
        print('\n'.join(fs) or 'match: front and three-quarter agree')
        sys.exit(1 if fs else 0)
    elif a[:1] == ['selftest']:
        sys.exit(0 if (selftest() & build_selftest()) else 1)
    elif a[:1] == ['build']:
        fs = build_faults(a[1], a[2:] or None) + crotch_faults(a[1], a[2:] or None) + judge_faults(a[1], a[2:] or None)
        print('\n'.join(fs) or 'build: every woman reads as a woman, every man as a man, each woman on her own build')
        sys.exit(1 if fs else 0)
    else:
        print(__doc__)
