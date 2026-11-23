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

    python3 source/castsheet.py sheet FILM OUT.jpg [WHO ...]    the sheet (refuses on a figure touching an edge)
    python3 source/castsheet.py match FILM [WHO ...]            front | 3/4 faults, one line each
    python3 source/castsheet.py selftest                         the check on Sam's saved notes
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


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['sheet']:
        print(sheet(a[1], a[2], a[3:] or None))
    elif a[:1] == ['match']:
        fs = match(a[1], a[2:] or None)
        print('\n'.join(fs) or 'match: front and three-quarter agree')
        sys.exit(1 if fs else 0)
    elif a[:1] == ['selftest']:
        sys.exit(0 if selftest() else 1)
    else:
        print(__doc__)
