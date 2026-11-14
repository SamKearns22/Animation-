#!/usr/bin/env python3
"""MAP  Places from a description (ranking item 5; overnight chat 5, 14 Nov). A place is a block of plain lines in
the film's places file, `story/FILM-places.txt`: its colours, then one block per view (a level camera on it, in
metres) listing every piece in it, back to front, each from the library (places_parts.py: walls, rails, doors,
windows, benches, desks, chairs, beds, booths, signs, notices, TVs, trees, lamp posts, facades), each placed in metres
(x across, depth from the lens, z up). The kit draws each view's back, middle and front layers (which layer comes
from the piece's depth against the view's people), and hands every piece's box to the checks (rule 83: SET_BOXES;
two boxes overlap as meant when one stands in front of the other), and its list of things to rule 3's benchmark.
No film imports this until Sam approves the kit (overnight run, answer 2).

THE LANGUAGE (one piece per line; params split by ', '; colours are 'R G B', a word from the place's colours,
'WORD * 0.88' (darker), or 'WORD / OTHER 0.4' (mixed 0.4 of the way to OTHER))
    # place: courtroom                 starts a place; its views follow
    colours: wall 226 214 194 | oak 204 166 116 | oak dark 170 130 86
    ## view: court_box                 a camera on the place (the film's view name)
    camera: up 1.6, horizon 850, lens 1500       a level camera (verticals stay vertical): height in metres, the
                                                 horizon's screen row, the lens in pixels (centre 540 unless given)
    people: judge 3.571, brand 2.5     where the view's people stand (metres from the lens): pieces nearer than all of
                                       them draw over them, between: the middle layer, the rest behind
    KIND: x -3.36 to 3.36, z 0 to 6.6, depth 6, step 0.48, seed 3 (the panelled wall)
          x, z: the front face's left to right and bottom to top (metres); depth: metres from the lens;
          at X Z: a point piece; look NAME: one of the kind's house looks (its trim); detail K: the trim at K of its
          usual size; any other param is the kind's own (places_parts.KINDS lists them); (NAME) names it for the checks

    python3 source/places.py replicate FILM OUT_DIR   every view's finished painting beside the kit's, and the film's
                                                      frames with the kit's places swapped in (0.05% is the bar)
    python3 source/places.py describe FILM            the film's places, as the page shows them

Map: parse 60 | colours 140 | the camera and layers 170 | draw 200 | boxes for the checks 250 | replicate 300 |
     lines for the page 390 | main 400
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)


class DescriptionError(ValueError):
    pass


# ---------------------------------------------------------------------------------------------- parse
NUM = r'-?\d+(?:\.\d+)?'


def _nums(s):
    if not re.fullmatch(rf'\s*{NUM}(\s+{NUM})*\s*', s):
        return None
    return tuple(float(v) for v in s.split())


def parse(text):
    """{'places': {name: {colours, views}}, 'views': {view: {place, camera, people, items}}}"""
    import places_parts as PP
    places, views = {}, {}
    place = view = None
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.split('  #')[0].rstrip()
        if not line.strip():
            continue
        m = re.match(r'#\s*place:\s*(\S+)', line)
        if m:
            place = places.setdefault(m.group(1), {'colours': {}, 'views': []})
            view = None
            continue
        m = re.match(r'##\s*view:\s*(\S+)', line)
        if m:
            if place is None:
                raise DescriptionError(f'line {n}: a view before any place')
            view = views[m.group(1)] = {'place': place, 'camera': None, 'people': {}, 'items': [], 'name': m.group(1),
                                        'refs': []}
            place['views'].append(m.group(1))
            continue
        if line.lstrip().startswith('#'):
            continue
        m = re.match(r'\s*([a-z][a-z ]*?):\s*(.*)$', line)
        if not m:
            raise DescriptionError(f'line {n}: not "kind: params": {line.strip()}')
        key, val = m.group(1), m.group(2).strip()
        if place is None:
            raise DescriptionError(f'line {n}: "{key}" before any place')
        if key == 'colours':
            for part in val.split('|'):
                w = part.split()
                nums = [x for x in w if re.fullmatch(r'\d+', x)]
                if len(nums) != 3:
                    raise DescriptionError(f'line {n}: a colour needs a name and three numbers: {part.strip()}')
                place['colours'][' '.join(x for x in w if x not in nums)] = tuple(int(x) for x in nums)
            continue
        if view is None:
            raise DescriptionError(f'line {n}: "{key}" before any view')
        if key == 'camera':
            cam = {}
            for part in val.split(','):
                k, _, v = part.strip().partition(' ')
                if k not in ('up', 'horizon', 'lens', 'centre') or _nums(v) is None:
                    raise DescriptionError(f'line {n}: camera takes up, horizon, lens, centre: {part.strip()}')
                cam[k] = float(v)
            if not {'up', 'horizon', 'lens'} <= set(cam):
                raise DescriptionError(f'line {n}: a camera needs up, horizon and lens')
            view['camera'] = cam
            continue
        if key == 'people':
            for part in val.split(','):
                w = part.split()
                if len(w) != 2 or _nums(w[1]) is None:
                    raise DescriptionError(f'line {n}: people are "who depth": {part.strip()}')
                view['people'][w[0]] = float(w[1])
            continue
        if key == 'refs':
            view['refs'] = [r.strip() for r in val.split(',')]
            continue
        if key not in PP.KINDS:
            raise DescriptionError(f'line {n}: no piece called "{key}" in the library (places_parts.KINDS)')
        name = key
        mn = re.search(r'\(([^)]*)\)\s*$', val)
        if mn:
            name, val = mn.group(1).strip(), val[:mn.start()].strip()
        it = {'kind': key, 'name': name, 'line': n, 'raw': {}}
        for part in [q.strip() for q in val.split(',') if q.strip()]:
            k, _, v = part.partition(' ')
            if k in it['raw']:
                raise DescriptionError(f'line {n}: {k} given twice')
            it['raw'][k] = v.strip()
        _check(it, PP.KINDS[key], n)
        view['items'].append(it)
    for v, d in views.items():
        if d['camera'] is None:
            raise DescriptionError(f'view {v}: no camera line')
    return {'places': places, 'views': views}


def _check(it, kind, n):
    allowed = {'x', 'z', 'depth', 'at', 'detail', 'seed', 'look', 'layer'} | set(kind['params'])
    for k in it['raw']:
        if k not in allowed:
            raise DescriptionError(f'line {n}: {it["kind"]} takes no "{k}" (it takes: {", ".join(sorted(allowed))})')
    if 'look' in it['raw'] and it['raw']['look'] not in kind.get('looks', {}):
        raise DescriptionError(f'line {n}: {it["kind"]} has no look "{it["raw"]["look"]}" '
                               f'(it has: {", ".join(kind.get("looks", {})) or "none"})')
    if 'depth' not in it['raw'] and not kind.get('overall'):
        raise DescriptionError(f'line {n}: {it["kind"]} needs a depth (metres from the lens)')


def places_file(film):
    return os.path.join(ROOT, 'story', f'{film}-places.txt')


def load(film):
    with open(places_file(film), encoding='utf-8') as f:
        return parse(f.read())


# ---------------------------------------------------------------------------------------------- colours
def colour(s, words):
    from remakes_sets import dk, mix
    s = s.strip()
    v = _nums(s)
    if v is not None:
        if len(v) != 3:
            raise DescriptionError(f'a colour is three numbers: {s}')
        return tuple(int(x) for x in v)
    m = re.fullmatch(r'(.+?)\s*\*\s*(' + NUM + ')', s)
    if m:
        return dk(colour(m.group(1), words), float(m.group(2)))
    m = re.fullmatch(r'(.+?)\s*/\s*(.+?)\s+(' + NUM + ')', s)
    if m:
        return mix(colour(m.group(1), words), colour(m.group(2), words), float(m.group(3)))
    if s in words:
        return words[s]
    import people
    if s in people.COLOURS:
        return people.COLOURS[s]
    raise DescriptionError(f'no colour called "{s}"')


# ---------------------------------------------------------------------------------------------- camera and layers
def level(view):
    from remakes_sets import Level

    class Snapped(Level):
        """Points snapped to a millionth of a pixel: metres written to four places land exactly on the pixel
        the painter meant (float noise put an edge at 120.0000001 and moved a whole row)."""
        def p(self, x, d, z=0.0):
            X, Y = Level.p(self, x, d, z)
            return round(X, 6), round(Y, 6)
    c = view['camera']
    return Snapped(c['up'], c['horizon'], c['lens'], c.get('centre', 540.0))


def depth_of(it):
    d = it['raw'].get('depth')
    if d is None:
        return None
    r = _range(d)
    return r[0]


def layer_of(view, it):
    """back (behind everyone), mid (between the view's people), front (nearer than all of them); overall pieces
    (a light over the whole picture) and a piece's own `layer` line go where they say."""
    if 'layer' in it['raw']:
        return it['raw']['layer']
    d = depth_of(it)
    if d is None:
        return 'front'
    ds = list(view['people'].values())
    if not ds or d >= max(ds):
        return 'back'
    if d < min(ds):
        return 'front'
    return 'mid'


def _range(s):
    m = re.fullmatch(rf'\s*({NUM})\s+to\s+({NUM})\s*', s)
    if m:
        return float(m.group(1)), float(m.group(2))
    v = _nums(s)
    if v is None or len(v) != 1:
        raise DescriptionError(f'not a number or "A to B": {s}')
    return v[0], v[0]


# ---------------------------------------------------------------------------------------------- draw
class Piece:
    """One placed piece: its kind's look, its metres turned into the kind's own drawing units (local px at the kind's
    REF pixels per metre) through the view's camera."""

    def __init__(self, view, it, words):
        import places_parts as PP
        self.view, self.it, self.words = view, it, words
        self.kind = PP.KINDS[it['kind']]
        raw = it['raw']
        self.L = level(view)
        self.d0, self.d1 = _range(raw['depth']) if 'depth' in raw else (None, None)
        self.detail = float(raw.get('detail', 1.0))
        look = self.kind['looks'].get(raw.get('look'), {})
        self.ref = look.get('ref', self.kind['ref'])
        self.k = 1.0                                  # a piece with no trim (ref None) keeps the house's lines
        if self.d0 is not None and self.ref:
            self.k = self.L.ppm(self.d0) * self.detail / self.ref
            if abs(self.k - 1.0) < 1e-3:
                self.k = 1.0                          # within 0.1% of its drawn size: as drawn (no visible change)
        if 'at' in raw:
            ax, az = _nums(raw['at'])
            self.x0 = self.x1 = ax
            self.z0 = self.z1 = az
        else:
            self.x0, self.x1 = _range(raw['x']) if 'x' in raw else (0.0, 0.0)
            self.z0, self.z1 = _range(raw['z']) if 'z' in raw else (0.0, 0.0)
        if self.d0 is not None:
            self.ox, self.oy = self.L.p(self.x0, self.d0, self.z1)
        else:
            self.ox, self.oy = 0.0, 0.0
        self.args = self._args()

    def P(self, x, z, d=None):
        """A point in metres, in the piece's own drawing units (from its anchor, at its scale)."""
        X, Y = self.L.p(x, self.d0 if d is None else d, z)
        return (round((X - self.ox) / self.k, 6), round((Y - self.oy) / self.k, 6))

    def M(self, m):
        """A length in metres at the piece's depth, in its own units."""
        return round(m * self.L.ppm(self.d0) / self.k, 6)

    def _args(self):
        kind, raw = self.kind, self.it['raw']
        a = dict(kind.get('defaults', {}))
        if 'look' in raw:
            a.update({k: v for k, v in kind['looks'][raw['look']].items() if k != 'ref'})
        for k, typ in kind['params'].items():
            if k not in raw:
                continue
            v = raw[k]
            try:
                if typ == 'c':
                    a[k] = colour(v, self.words)
                elif typ == 'm':
                    a[k] = self.M(float(v))
                elif typ == 'n':
                    a[k] = float(v)
                elif typ == 'pt':
                    xz = _nums(v)
                    a[k] = self.P(xz[0], xz[1], xz[2] if len(xz) > 2 else None)
                elif typ == 'pts':
                    a[k] = [self.P(*_nums(q)) for q in v.split(';')]
                elif typ == 'nums':
                    a[k] = _nums(v)
                elif typ == 's':
                    a[k] = v.strip('"')
                elif typ == 'r':
                    lo, hi = _range(v)
                    a[k] = (self.M(lo), self.M(hi))
                else:
                    raise DescriptionError(f'{k}: unknown param type {typ}')
            except (TypeError, ValueError) as e:
                raise DescriptionError(f'line {self.it["line"]}: {k} {v}: {e}')
        for k, v in list(a.items()):                  # colours named in the looks come from the place's colours
            if isinstance(v, str) and kind['params'].get(k) == 'c':
                a[k] = colour(v, self.words)
        a['seed'] = int(raw['seed']) if 'seed' in raw else a.get('seed', 0)
        a['w'] = round((self.x1 - self.x0) * self.L.ppm(self.d0) / self.k, 6) if self.d0 is not None else 0.0
        a['h'] = round((self.z1 - self.z0) * self.L.ppm(self.d0) / self.k, 6) if self.d0 is not None else 0.0
        a['piece'] = self
        return a

    def draw(self, img, cam, t):
        import burnham as B
        lc = B.Local(cam, self.ox, self.oy, self.k)
        self.kind['fn'](B.Pen(img, lc), img, lc, self.args, t)

    def screen_box(self):
        """The front face's box on the screen (world px at zoom 1), for the checks."""
        if self.d0 is None:
            return None
        if 'box' in self.kind:                       # a kind that knows its own drawn extent (local units)
            bx0, by0, bx1, by1 = self.kind['box'](self.args)
            return (self.ox + bx0 * self.k, self.oy + by0 * self.k, self.ox + bx1 * self.k, self.oy + by1 * self.k)
        a, b = self.L.p(self.x0, self.d0, self.z1), self.L.p(self.x1, self.d0, self.z0)
        return (a[0], a[1], b[0], b[1])


def pieces(desc, view):
    v = desc['views'][view]
    return [Piece(v, it, v['place']['colours']) for it in v['items']]


def painter(desc, view, layer):
    v = desc['views'][view]
    chosen = [p for p in pieces(desc, view) if layer_of(v, p.it) == layer]
    if not chosen:
        return None

    def paint(img, cam, t=0.0, *rest):
        for p in chosen:
            p.draw(img, cam, t)
    return paint


def install(desc, film_sets):
    """The film's BACK, MID and FRONT tables (the painters it calls) filled from the description."""
    for view in desc['views']:
        for layer, table in (('back', film_sets.BACK), ('mid', film_sets.MID), ('front', film_sets.FRONT)):
            fn = painter(desc, view, layer)
            if fn is not None:
                table[view] = fn
            else:
                table.pop(view, None)


# ---------------------------------------------------------------------------------------------- boxes for the checks
WIDE = 0.8          # a piece wider than this share of the picture is a band (a wall, a rail, a floor): not a thing


def set_boxes(desc, offsets=None):
    """Rule 83's boxes from the pieces themselves (no hand-made list): (VIEW NAME, screen box), each view laid
    `offsets[view]` px to the right so views never overlap; and the meant overlaps (one stands in front of the other
    by 0.2 m or more, or one hangs on the other: the same depth and named in `on`)."""
    boxes, depth = [], {}
    for i, view in enumerate(desc['views']):
        off = (offsets or {}).get(view, 4000 * (i + 1))
        for p in pieces(desc, view):
            b = p.screen_box()
            if b is None or p.kind.get('band') or (b[2] - b[0]) > WIDE * 1080:
                continue
            nm = f'{view} {p.it["name"]}'
            boxes.append((nm, (b[0] + off, b[1], b[2] + off, b[3])))
            depth[nm] = p.d0
    meant = []
    for i, (a, ba) in enumerate(boxes):
        for b, bb in boxes[i + 1:]:
            if a.split()[0] == b.split()[0] and abs(depth[a] - depth[b]) >= 0.2:
                meant.append((a, b, f'{a} stands {abs(depth[a] - depth[b]):.1f} m from {b} (their depths)'))
    return boxes, meant


# ---------------------------------------------------------------------------------------------- replicate
def _differ(a, b):
    import numpy as np
    A, Bm = np.asarray(a.convert('RGB'), np.int16), np.asarray(b.convert('RGB'), np.int16)
    return float((np.abs(A - Bm).max(axis=2) > 24).mean() * 100)


FRAMES = {'blessed': [(2.0, 'arrive'), (5.6, 'oath'), (8.6, 'jury'), (16.0, 'dock'), (20.5, 'van'), (24.0, 'escort'),
                      (28.6, 'cot'), (33.0, 'phone'), (38.0, 'tvroom'), (41.0, 'tv'), (50.0, 'gates'),
                      (60.5, 'gates2')]}


def _film_sets(film):
    if film == 'blessed':
        import blessed_sets as ST
        return ST
    raise SystemExit(f'replicate: no sets module for {film}')


def replicate(film, out_dir, views=None, frames=True):
    """Each described view's finished painting (bare, no cast) beside the kit's, then the film's frames with the kit's
    places swapped in. One labelled sheet; a score per picture (share of pixels that differ by more than 24 levels)."""
    from PIL import Image, ImageDraw, ImageFont
    ST = _film_sets(film)
    desc = load(film)
    views = views or [v for v in ST.VIEWS if v in desc['views'] or ST.view_cam(v)[0] in desc['views']]
    os.makedirs(out_dir, exist_ok=True)
    keep = {n: dict(getattr(ST, n)) for n in ('BACK', 'MID', 'FRONT')}
    old = {v: ST.painting(v) for v in views}
    olds = []
    if frames:
        import blessed as BL
        fr = [(t, lab) for t, lab in FRAMES[film] if ST.view_cam(BL.VIEW[BL.shot_of(t)])[0] in desc['views']]
        olds = [BL.frame_image(t) for t, _ in fr]
    install(desc, ST)
    try:
        new = {v: ST.painting(v) for v in views}
        news = [BL.frame_image(t) for t, _ in fr] if frames else []
    finally:
        for n, d in keep.items():
            tab = getattr(ST, n)
            tab.clear()
            tab.update(d)
    pairs = [(f'{v} (painting)', old[v], new[v]) for v in views] + \
            ([(f'{lab} {t:.1f}s (frame)', a, b) for (t, lab), a, b in zip(fr, olds, news)] if frames else [])
    font = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 22)
    tw, th = 270, 480
    cols = 3
    rows = (len(pairs) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (2 * tw + 20) + 10, rows * (th + 40) + 10), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    scores = []
    for i, (label, a, b) in enumerate(pairs):
        s = _differ(a, b)
        scores.append((label, s))
        x, y = 10 + (i % cols) * (2 * tw + 20), 10 + (i // cols) * (th + 40)
        for k, im in enumerate((a, b)):
            sheet.paste(im.convert('RGB').resize((tw, th)), (x + k * tw, y + 34))
        d.text((x + 4, y + 6), f'{label}: finished | kit {s:.2f}%', font=font, fill=(30, 30, 30))
    out = os.path.join(out_dir, f'{film}-places-replicate.jpg')
    sheet.save(out, quality=86)
    return out, scores


# ---------------------------------------------------------------------------------------------- lines for the page
def lines(film):
    """The places file's lines, for the page (a note changes a line here, not the set's code)."""
    with open(places_file(film), encoding='utf-8') as f:
        return [ln.rstrip() for ln in f if ln.strip()]


def main(argv):
    cmd = argv[0]
    if cmd == 'replicate':
        out, scores = replicate(argv[1], argv[2], frames='--no-frames' not in argv)
        for label, s in scores:
            print(f'{label:34s} {s:6.3f}%{"   FAIL" if s > 0.05 else ""}')
        print(out)
    elif cmd == 'describe':
        print('\n'.join(lines(argv[1])))
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
