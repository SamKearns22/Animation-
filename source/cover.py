#!/usr/bin/env python3
"""cover: the clipping check fed by default (could-not-test, Sam's pick 1, 22 Nov). 3 of the last 4 films gave the
clipping check nothing to look at, so it printed COULD NOT TEST and Andy's, Pat's and Milburn's hands went through
their name cards unseen. Now the drawing itself is recorded: every piece the places painter paints is its own layer at
its own depth (the painter knows it), and every person drawn by the people kit (views.person) is split into body,
each arm and head, the arms at their REAL depth from the pose (shoulder, elbow, wrist), never a fixed reach guess.
Who is in front is then read from the real frame, so whatever order a film composites in, what Sam sees is judged.

MAP
  recording 60     REC: the frame being recorded; view(v) (the places view the painter is on), piece(img, p) (one
                   painted piece), person(img, who, depth) (a film's own person drawn at a known depth), the views tap
  analyse 200      faults(records, frame): a further thing drawn over a nearer one where they overlap on screen;
                   flat things (papers, folders, coasters, a table top) under anything resting on or above them allowed
  clipcheck 290    cover_faults(film, times): picture(t) recorded at each time; the faults, and what it could not see
                   (people drawn with no depth: COULD NOT TEST for that shot)
  readable 400     read_boxes(film, rec) for the render: each listed thing's box as drawn (text pieces, KEEP_CLEAR);
                   readable_faults(film, record, hook): finish.py's check, captions and Hook Text against those boxes

A film with no places views gives its people's depth with `with cover.person(img, who, depth): draw...` and its own
set pieces with `with cover.thing(img, name, near, far, flat=False, bottom=None): draw...` (satire_template does).

    python3 source/cover.py FILM T [T ...]     the faults at those times, and the layers it saw
"""
import contextlib
import importlib
import os
import sys

import numpy as np
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

LENS = 1500.0           # px: the places kit's usual lens, for depth read from drawn size when no view is painted
ORDER_TOL = 0.05        # m: depths closer than this are side by side (clipcheck's ORDER_TOL)
MIN_PX = 60             # px at 1080 x 1920: a further thing showing over a nearer one by fewer is noise (edges)
FLAT = {'papers', 'coaster', 'folder', 'table top', 'rug', 'mat', 'floor'}   # lie on a surface (plus any kind with `near`)
REST = 0.15             # m: how far below a surface a hand resting on it reaches on screen (a cartoon hand is big)
TORSO = 0.12            # m: a body's half depth
HAND = 0.045            # m: a hand's radius (clipcheck's hand sphere)
TEXT_KINDS = ('name card', 'sign board', 'notice', 'can')    # pieces with words on them (the readable check)


# ---------------------------------------------------------------------------------------------- recording
class _Rec:
    def __init__(self, mode='cover'):
        self.mode = mode              # 'cover' (everything) or 'read' (only things with words, cheap)
        self.view = None              # the places view last painted this frame (its camera and its people's depths)
        self.items = []
        self.depths = {}              # who -> depth from the lens, given by the film (person())
        self.blind = set()            # people drawn with no depth known
        self.sized = set()            # people whose depth was read from their drawn size (no places view lists them)
        self.drawn = []               # every person drawn: who, screen box, scale, yaw, depth, view (kitinputs' survey)
        self.person = None            # the person being drawn (the views tap's state)


REC = [None]


def recording():
    return REC[0] is not None


def begin(mode='cover'):
    REC[0] = _Rec(mode)
    import views
    views.TAP[0] = _tap if mode in ('cover', 'survey') else None
    if mode == 'cover' and _ORIG_ARM[0] is None:
        _ORIG_ARM[0] = views.arm
        views.arm = _arm
    return REC[0]


def end():
    r = REC[0]
    REC[0] = None
    try:
        import views
        views.TAP[0] = None
        if _ORIG_ARM[0] is not None:
            views.arm = _ORIG_ARM[0]
            _ORIG_ARM[0] = None
    except ImportError:
        pass
    return r


def view(v):
    if REC[0] is not None:
        REC[0].view = v


def _diff(before, img):
    """(box, mask, pixels) of what changed between two images of one size; None if nothing did."""
    d = ImageChops.difference(img, before)
    bbs = [b.getbbox() for b in d.split()]
    bbs = [b for b in bbs if b]
    if not bbs:
        return None
    bb = (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))
    m = np.asarray(d.crop(bb)).max(-1) > 8
    if not m.any():
        return None
    return bb, m, np.asarray(img.crop(bb).convert('RGBA')).copy()


def _add(img, rec, **kw):
    if rec is None:
        return
    bb, m, px = rec
    k = 1080.0 / img.size[0]                       # supersampled pictures: boxes kept at 1080 x 1920
    REC[0].items.append(dict(kw, box=bb, mask=m, px=px, k=k, size=img.size))


@contextlib.contextmanager
def piece(img, p):
    """One places piece painted onto img (places.painter calls this)."""
    r = REC[0]
    raw = p.it['raw']
    text = str(p.args.get('text') or '').strip()
    if r is None or p.d0 is None or (r.mode in ('read', 'survey') and not (text and p.it['kind'] in TEXT_KINDS)):
        yield
        return
    before = img.copy()
    yield
    near = float(raw['near']) if 'near' in raw else p.d0
    flat = p.it['kind'] in FLAT or 'near' in raw
    _add(img, _diff(before, img), name=p.it.get('name') or p.it['kind'], owner=p.it.get('name') or p.it['kind'],
         rng=(min(near, p.d0), max(near, p.d1)), flat=flat, surface=p.z1 if flat else None, bottom=p.z0,
         on=raw.get('on'), text=text, kind=p.it['kind'])


@contextlib.contextmanager
def thing(img, name, near, far=None, flat=False, bottom=None, surface=None, text=''):
    """A film's own set piece drawn by hand, at its depth (metres from the lens)."""
    r = REC[0]
    if r is None or (r.mode in ('read', 'survey') and not text):
        yield
        return
    before = img.copy()
    yield
    far = near if far is None else far
    _add(img, _diff(before, img), name=name, owner=name, rng=(near, far), flat=flat, surface=surface, bottom=bottom,
         on=None, text=text, kind='thing')


@contextlib.contextmanager
def person(img, who, depth, flat_person=True):
    """A film's own person at `depth` m from the lens. Drawn by the people kit (views.person), the arms are split off
    at their real depth; drawn any other way (body.person), the whole person is one layer at that depth."""
    r = REC[0]
    if r is None or r.mode != 'cover':
        if r is not None:
            r.depths[who] = depth
        yield
        return
    r.depths[who] = depth
    before = img.copy()
    n = len(r.items)
    yield
    if len(r.items) == n:                          # nothing tapped: drawn whole (not the people kit)
        _add(img, _diff(before, img), name=f'{who}', owner=who, rng=(depth - TORSO, depth + TORSO), flat=False,
             surface=None, bottom=None, on=None, text='', kind='person')


def _tap(stage, img, **kw):
    """views.person's tap: start, mid (the body drawn so far), head/head_end. Each arm is recorded by _arm (drawn
    alone on a clear layer as well), wherever views.person draws it (behind the body, in the lap, over the desk)."""
    r = REC[0]
    if r is None:
        return
    if stage == 'start':
        sp = kw['sp']
        who = sp.get('who') or sp.get('name') or 'someone'
        d = None
        if who in r.depths:
            d = r.depths[who]
        elif r.view is not None and who in r.view.get('people', {}):
            d = float(r.view['people'][who])
        mu = float(sp['height']) * 0.84 / 928.0 if sp.get('height') else None
        if mu is None:
            import views as V
            mu = V.M_PER_UNIT
        est = False
        if d is None and kw.get('s'):          # named-lines change 3: no places view lists them, so their depth is
            lens = float(r.view['camera']['lens']) if r.view is not None else LENS   # read from their drawn size (a
            d, est = lens * mu / float(kw['s']), True          # level camera: pixels per metre = lens / depth)
            r.sized.add(who)
        r.person = dict(who=who, d=d, mu=mu, depth=kw['depth'], snap=img.copy(), snap0=img.copy(), arms=[], body=None)
        r.drawn.append(dict(who=who, d=d, est=est, s=kw.get('s'), yaw=kw.get('yaw'), x=kw.get('x'), y=kw.get('y'),
                            view=r.view['name'] if r.view is not None else None, box=None, k=1080.0 / img.size[0],
                            seated=bool(sp.get('seated'))))
        if d is None:
            r.blind.add(who)
        return
    P = r.person
    if stage == 'head_end' and P is not None and r.drawn and r.drawn[-1]['who'] == P['who']:
        bb = ImageChops.difference(img.convert('RGB'), P['snap0'].convert('RGB')).getbbox()   # (RGBA: alpha only)
        k = r.drawn[-1]['k']
        r.drawn[-1]['box'] = tuple(int(v * k) for v in bb) if bb else None
    if r.mode == 'survey':
        if stage == 'head_end':
            r.person = None
        return
    if P is None or P['d'] is None:
        return
    who, d = P['who'], P['d']
    if stage == 'mid' and P['body'] is None:
        P['body'] = _diff(P['snap'], img)
    elif stage == 'head':
        P['snap'] = img.copy()
    elif stage == 'head_end':
        if P['body'] is not None:              # the body, less whatever an arm painted (an arm drawn behind it)
            bb, m, px = P['body']
            m = m.copy()
            for abb, am in P['arms']:
                x0, y0 = max(bb[0], abb[0]), max(bb[1], abb[1])
                x1, y1 = min(bb[2], abb[2]), min(bb[3], abb[3])
                if x1 > x0 and y1 > y0:
                    m[y0 - bb[1]:y1 - bb[1], x0 - bb[0]:x1 - bb[0]] &= ~am[y0 - abb[1]:y1 - abb[1], x0 - abb[0]:x1 - abb[0]]
            _add(img, (bb, m, px), name=f'{who} body', owner=who, rng=(d - TORSO, d + TORSO), flat=False,
                 surface=None, bottom=None, on=None, text='', kind='person')
        _add(img, _diff(P['snap'], img), name=f'{who} head', owner=who, rng=(d - 0.1, d + 0.1), flat=False,
             surface=None, bottom=None, on=None, text='', kind='person')
        r.person = None


_ORIG_ARM = [None]


def _arm(p, j2, side, sp, *a, **k):
    """views.arm while recording: the arm drawn alone on a clear layer too, so its own pixels are known even where
    it repaints what was there; recorded at its real depth (shoulder, elbow and wrist from the pose)."""
    r = REC[0]
    P = r.person if r is not None else None
    if P is not None and P['d'] is not None:
        lay = Image.new('RGBA', p.img.size, (0, 0, 0, 0))
        try:
            _ORIG_ARM[0](type(p)(lay, p.cam), j2, side, sp, *a, **k)
            bb = lay.getbbox()
        except Exception:
            bb = None
        if bb:
            px = np.asarray(lay.crop(bb)).copy()
            m = px[..., 3] > 0
            d, mu = P['d'], P['mu']
            ds = [d - P['depth'][q + side] * mu for q in ('sh', 'el', 'wr')]
            bottom = None
            if r.view is not None:
                c = r.view['camera']           # the arm's lowest point as a height above the floor (level camera)
                ymax = bb[1] + int(np.nonzero(m.any(1))[0].max())
                bottom = c['up'] - (ymax - c['horizon']) * ds[2] / c['lens']
            P['arms'].append((bb, m))
            _add(p.img, (bb, m, px), name=f'{P["who"]} arm{side}', owner=P['who'], rng=(min(ds) - HAND, max(ds)),
                 flat=False, surface=None, bottom=bottom, on=None, text='', kind='person')
    return _ORIG_ARM[0](p, j2, side, sp, *a, **k)


# ---------------------------------------------------------------------------------------------- analyse
def _merge(items):
    """The same thing recorded twice in a frame (a layer painted again) becomes one, its masks joined."""
    out = {}
    for it in items:
        k = it['name']
        if k not in out:
            out[k] = it
            continue
        a = out[k]
        x0, y0 = min(a['box'][0], it['box'][0]), min(a['box'][1], it['box'][1])
        x1, y1 = max(a['box'][2], it['box'][2]), max(a['box'][3], it['box'][3])
        m = np.zeros((y1 - y0, x1 - x0), bool)
        px = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
        for b in (a, it):
            bx, by = b['box'][0] - x0, b['box'][1] - y0
            sl = (slice(by, by + b['mask'].shape[0]), slice(bx, bx + b['mask'].shape[1]))
            px[sl][b['mask']] = b['px'][b['mask']]
            m[sl] |= b['mask']
        out[k] = dict(a, box=(x0, y0, x1, y1), mask=m, px=px)
    return list(out.values())


def _over(a, b, frame, others=()):
    """Pixels where b shows over a in the frame (and a over b): only pixels where their colours differ count."""
    x0, y0 = max(a['box'][0], b['box'][0]), max(a['box'][1], b['box'][1])
    x1, y1 = min(a['box'][2], b['box'][2]), min(a['box'][3], b['box'][3])
    if x1 <= x0 or y1 <= y0:
        return 0, 0

    def cut(r):
        sx, sy = x0 - r['box'][0], y0 - r['box'][1]
        return (r['mask'][sy:sy + y1 - y0, sx:sx + x1 - x0],
                r['px'][sy:sy + y1 - y0, sx:sx + x1 - x0].astype(np.int16))
    ma, pa = cut(a)
    mb, pb = cut(b)
    both = ma & mb & (pa[..., 3] > 245) & (pb[..., 3] > 245)
    if both.sum() < MIN_PX:
        return 0, 0
    f = frame[y0:y1, x0:x1, :3].astype(np.int16)
    da = np.abs(f - pa[..., :3]).max(-1)
    db = np.abs(f - pb[..., :3]).max(-1)
    differ = np.abs(pa[..., :3] - pb[..., :3]).max(-1) > 40
    b_top = both & differ & (db <= 6) & (da > 40)      # the frame shows b's own colour exactly (nothing else on top)
    a_top = both & differ & (da <= 6) & (db > 40)
    if b_top.sum() >= MIN_PX:                          # a pixel a third thing also explains (Andy's white shirt over
        for o in others:                               # the white marble) is nobody's proof
            ox0, oy0 = max(x0, o['box'][0]), max(y0, o['box'][1])
            ox1, oy1 = min(x1, o['box'][2]), min(y1, o['box'][3])
            if ox1 <= ox0 or oy1 <= oy0:
                continue
            sx, sy = ox0 - o['box'][0], oy0 - o['box'][1]
            om = o['mask'][sy:sy + oy1 - oy0, sx:sx + ox1 - ox0]
            op = o['px'][sy:sy + oy1 - oy0, sx:sx + ox1 - ox0, :3].astype(np.int16)
            same = om & (np.abs(frame[oy0:oy1, ox0:ox1, :3].astype(np.int16) - op).max(-1) <= 6)
            b_top[oy0 - y0:oy1 - y0, ox0 - x0:ox1 - x0] &= ~same
    b_top = _solid(b_top)                              # outlines and soft edges (1-2 px, the same ink on everything)
    return int(b_top.sum()), int(a_top.sum())        # prove nothing: only a patch of b's own colour counts


def _solid(m, n=2):
    """m eroded by n pixels: what is left of a mask once thin lines and edges are taken off."""
    for _ in range(n):
        e = m.copy()
        e[1:] &= m[:-1]
        e[:-1] &= m[1:]
        e[:, 1:] &= m[:, :-1]
        e[:, :-1] &= m[:, 1:]
        m = e
    return m


def _excused(near, far):
    """A flat thing lying on a surface (papers, a folder) under something resting on or above that surface: the
    camera looks down on the surface, so what sits on it covers it (Milburn's hands on his papers: no fault)."""
    if near['flat'] and far.get('bottom') is not None and near.get('surface') is not None:
        return far['bottom'] >= near['surface'] - REST   # a resting hand's lowest drawn edge dips below the top
    if near.get('on') and near['on'] == far['name'] or far.get('on') and far['on'] == near['name']:
        return True
    return False


def faults(items, frame, allowed=lambda a, b: False):
    """[(further, nearer, px)]: a further thing drawn over a nearer one where they overlap on screen."""
    if frame.shape[1] != 1080 and items:
        pass
    items = _merge(items)
    out = []
    for i, a in enumerate(items):
        for b in items[i + 1:]:
            if a['owner'] == b['owner']:
                continue
            if a['rng'][1] + ORDER_TOL < b['rng'][0]:
                near, far = a, b
            elif b['rng'][1] + ORDER_TOL < a['rng'][0]:
                near, far = b, a
            else:
                continue                            # side by side in depth
            if _excused(near, far) or allowed(near, far):
                continue
            n, _ = _over(near, far, frame, [o for o in items if o is not near and o is not far])
            if n >= MIN_PX:
                out.append((far, near, n))
    return out


# ---------------------------------------------------------------------------------------------- clipcheck
class _Part:
    def __init__(self, it):
        self.owner = it['owner']
        self.part = it['name'].split(' ', 1)[1].replace(' ', '') if it['kind'] == 'person' and ' ' in it['name'] \
            else ''

    def __repr__(self):
        return f'{self.owner}.{self.part}' if self.part else self.owner


def picture_fn(film):
    for k in ('picture', 'frame_image'):
        if hasattr(film, k):
            return getattr(film, k)
    return None


def record(film, t):
    """(records, frame as an array, blind people) for film time t."""
    pic = picture_fn(film)
    begin('cover')
    try:
        im = pic(t)
    finally:
        r = end()
    fr = np.asarray(im.convert('RGB'))
    return r.items, fr, r.blind


def survey_record(film, t):
    """kitinputs' survey: who is drawn at t (screen box, scale, yaw, depth), the places view painted, and every
    piece with words on it (its box): no layers kept, so it is cheap."""
    pic = picture_fn(film)
    begin('survey')
    try:
        im = pic(t)
    finally:
        r = end()
    v = r.view
    return dict(t=t, view=(v['name'], dict(v['camera'] or {}), dict(v.get('people') or {}), v.get('place'))
                if v is not None else None, people=[{k: x for k, x in d.items()} for d in r.drawn],
                texts=[(i['name'], i['box'], i['k']) for i in r.items if i.get('text')], size=im.size, image=im)


def _one(args):
    film_name, t = args
    film = sys.modules.get(film_name) or importlib.import_module(film_name)
    import clipcheck as C
    items, fr, blind = record(film, t)
    al = lambda a, b: C._allowed(film, _Part(a), _Part(b), t)
    return t, [(f['name'], f['rng'], n['name'], n['rng'], px) for f, n, px in faults(items, fr, al)], \
        sorted(blind), len(items)


def cover_faults(film, times, pool=True):
    """(faults, untested): the clipping check on the recorded drawing; untested names the shots where people were
    drawn with no depth (or nothing at all was recorded)."""
    import clipcheck as C
    args = [(film.__name__, t) for t in times]
    if pool and len(args) > 4:
        from multiprocessing import Pool
        with Pool(os.cpu_count()) as p:
            res = p.map(_one, args, chunksize=2)
    else:
        res = [_one(a) for a in args]
    seen, out, blind, recorded = {}, [], {}, 0
    for t, fs, bl, n in res:
        recorded += n
        shot = C._shot(film, t)
        for fn, fr_, nn, nr, px in fs:
            k = (fn, nn)
            if k not in seen:
                seen[k] = [t, shot, fr_, nr, px, 0]
            seen[k][5] += 1
            seen[k][4] = max(seen[k][4], px)
        for w in bl:
            blind.setdefault(shot, set()).add(w)
    for (fn, nn), (t, shot, fr_, nr, px, cnt) in seen.items():
        out.append(f'{t:.2f} s (shot {shot}): {fn} ({fr_[0]:.2f} m away) is drawn over {nn} ({nr[1]:.2f} m, nearer): '
                   f'passes through it on screen ({cnt} of {len(times)} frames checked, up to {px} px)')
    untested = []
    if not recorded:
        untested.append('clipcheck: COULD NOT TEST: nothing the film draws was recorded (no places views, no people '
                        'kit, no cover.person / cover.thing): give each person and set piece its depth (cover.py)')
    for shot, who in sorted(blind.items()):
        untested.append(f'clipcheck: COULD NOT TEST (shot {shot}): {", ".join(sorted(who))} drawn with no depth (no '
                        f'places view lists them): draw them inside cover.person(img, who, depth) (cover.py)')
    return out, untested


# ---------------------------------------------------------------------------------------------- readable
def read_boxes(film, r):
    """For the render (film_engine records each drawing in 'read' mode): [(name, x0, y0, x1, y1)] at 1080 x 1920,
    each text piece as it was actually drawn on this frame, then the film's KEEP_CLEAR boxes at this time."""
    out = []
    for it in _merge(r.items):
        k = it['k']
        x0, y0, x1, y1 = it['box']
        out.append((it['name'], round(x0 * k), round(y0 * k), round(x1 * k), round(y1 * k), 'text'))
    return out


def keep_clear(film, t):
    out = []
    for name, box_at in getattr(film, 'KEEP_CLEAR', ()):
        try:
            b = box_at(t)
        except Exception:
            b = None
        if b:
            out.append((name, *(int(v) for v in b)))
    return out


SIDE = '.readable.json'     # the render's record beside the clean video: each drawing's boxes (finish.py reads it)
COVERED = 0.05              # a listed thing with 5% or more of its box under a caption or the Hook Text is a fault


def readable_faults(film, data, hook=None):
    """Captions (as finish.py draws them) and the Hook Text against each listed thing's box on the frames the render
    drew (data: the render's record). One line per thing per caption: when, how much, the posted time."""
    import subtitles as SUB
    draw = getattr(film, 'draw_subtitle', None) or SUB.draw
    B = sys.modules.get('burnham')
    fps = data['fps']
    alpha = {}

    def cap(c):
        if c not in alpha:
            old = B.SS if B else None
            if B:
                B.SS = 1
            lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
            draw(lay, c)
            if B:
                B.SS = old
            alpha[c] = np.asarray(lay.split()[3]) > 100
        return alpha[c]
    hb, hook_until = None, -1.0
    if hook:
        import hookcheck
        text, opts = hook
        hb = hookcheck.hook_box(text, **opts)
        hook_until = opts.get('until', 3.6) * SUB.SPEED             # its 'until' is on the delivered (1.1x) clock
    worst = {}
    for key in sorted(data['frames'], key=int):
        t = int(key) / fps
        c = film.caption_at(t) if hasattr(film, 'caption_at') else None
        for name, x0, y0, x1, y1, *kind in data['frames'][key]:
            if kind and kind[0] == 'text':           # a thing with words: its words sit in the middle; a caption
                dx, dy = (x1 - x0) * 0.1, (y1 - y0) * 0.3   # touching its edge leaves them readable (Milburn's posted
                x0, y0, x1, y1 = int(x0 + dx), int(y0 + dy), int(x1 - dx), int(y1 - dy)   # frames, 23 Nov)
            name = name.split(';')[0].split(' (')[0]
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(1080, x1), min(1920, y1)
            area = max(1, (x1 - x0) * (y1 - y0))
            if c:
                share = cap(c)[y0:y1, x0:x1].sum() / area
                if share >= COVERED:
                    w = worst.setdefault((name, 'the caption "' + c + '"'), [t, t, 0.0, 0])
                    w[1], w[2], w[3] = t, max(w[2], share), w[3] + 1
            if hb and t < hook_until:
                ix = max(0, min(x1, hb[2]) - max(x0, hb[0])) * max(0, min(y1, hb[3]) - max(y0, hb[1]))
                if ix / area >= COVERED:
                    w = worst.setdefault((name, 'the Hook Text'), [t, t, 0.0, 0])
                    w[1], w[2], w[3] = t, max(w[2], ix / area), w[3] + 1
    return [f'{t0:.2f}-{t1:.2f} s (posted {t0 / SUB.SPEED:.2f} s): {name} is {share:.0%} under {what} at worst '
            f'({n} drawings): move the thing, or the caption (a draw_subtitle with its own base for that shot)'
            for (name, what), (t0, t1, share, n) in sorted(worst.items(), key=lambda kv: kv[1][0])]


if __name__ == '__main__':
    film = importlib.import_module(sys.argv[1])
    for _b in ('body', 'burnham'):
        if _b in sys.modules:
            sys.modules[_b].SS = 1
    import cover as _me                           # the painters import `cover`: record through that same copy
    for t in map(float, sys.argv[2:]):
        items, fr, blind = _me.record(film, t)
        print(f'{t:.2f} s: {len(items)} layers: ' + ', '.join(f'{i["name"]} {i["rng"][0]:.2f}-{i["rng"][1]:.2f}'
                                                             for i in _merge(items)))
        if blind:
            print('  no depth:', ', '.join(sorted(blind)))
        for f, n, px in _me.faults(items, fr):
            print(f'  FAULT: {f["name"]} ({f["rng"][0]:.2f} m) drawn over {n["name"]} ({n["rng"][1]:.2f} m): {px} px')
