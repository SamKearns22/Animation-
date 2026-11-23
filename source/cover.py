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
  readable 360     boxes(film, t) for the render: each listed thing's box as drawn (text pieces, KEEP_CLEAR)

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

ORDER_TOL = 0.05        # m: depths closer than this are side by side (clipcheck's ORDER_TOL)
MIN_PX = 60             # px at 1080 x 1920: a further thing showing over a nearer one by fewer is noise (edges)
FLAT = {'papers', 'coaster', 'folder', 'table top', 'rug', 'mat', 'floor'}   # lie on a surface (plus any kind with `near`)
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
        self.person = None            # the person being drawn (the views tap's state)


REC = [None]


def recording():
    return REC[0] is not None


def begin(mode='cover'):
    REC[0] = _Rec(mode)
    import views
    views.TAP[0] = _tap if mode == 'cover' else None
    return REC[0]


def end():
    r = REC[0]
    REC[0] = None
    try:
        import views
        views.TAP[0] = None
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
    if r is None or p.d0 is None or (r.mode == 'read' and not (text and p.it['kind'] in TEXT_KINDS)):
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
    if r is None or (r.mode == 'read' and not text):
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
    """views.person's tap: start, mid (body drawn), mid_end, arm/arm_end (each arm), head/head_end."""
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
        r.person = dict(who=who, d=d, mu=mu, depth=kw['depth'], snap=img.copy(), L=kw['L'], j2=kw['j2'])
        if d is None:
            r.blind.add(who)
        return
    P = r.person
    if P is None or P['d'] is None:
        return
    who, d, mu = P['who'], P['d'], P['mu']
    if stage in ('mid', 'arm_end', 'head_end'):
        what = {'mid': 'body', 'arm_end': 'arm' + kw.get('side', ''), 'head_end': 'head'}[stage]
        if what.startswith('arm'):
            sd = kw['side']
            ds = [d - P['depth'][k + sd] * mu for k in ('sh', 'el', 'wr')]
            rng = (min(ds) - HAND, max(ds))
        elif what == 'body':
            rng = (d - TORSO, d + TORSO)
        else:
            rng = (d - 0.1, d + 0.1)
        rec = _diff(P['snap'], img)
        bottom = None
        if rec is not None and what.startswith('arm') and r.view is not None:
            c = r.view['camera']                 # the arm's lowest point as a height above the floor (level camera)
            ymax = rec[0][1] + int(np.nonzero(rec[1].any(1))[0].max())
            wd = d - P['depth']['wr' + kw['side']] * mu
            bottom = c['up'] - (ymax - c['horizon']) * wd / c['lens']
        _add(img, rec, name=f'{who} {what}', owner=who, rng=rng, flat=False, surface=None, bottom=bottom, on=None,
             text='', kind='person')
    if stage in ('mid', 'mid_end', 'arm', 'arm_end', 'head', 'head_end'):
        P['snap'] = img.copy()


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


def _over(a, b, frame):
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
    b_top = both & differ & (db < 24) & (da > 40)
    a_top = both & differ & (da < 24) & (db > 40)
    return int(b_top.sum()), int(a_top.sum())


def _excused(near, far):
    """A flat thing lying on a surface (papers, a folder) under something resting on or above that surface: the
    camera looks down on the surface, so what sits on it covers it (Milburn's hands on his papers: no fault)."""
    if near['flat'] and far.get('bottom') is not None and near.get('surface') is not None:
        return far['bottom'] >= near['surface'] - 0.03
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
            n, _ = _over(near, far, frame)
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
def boxes(film, t, draw):
    """For the render: draw the frame (draw(t)) while recording things with words; returns (picture, boxes), boxes
    [(name, x0, y0, x1, y1, px)] at 1080 x 1920: each text piece's drawn pixels, then the film's KEEP_CLEAR."""
    begin('read')
    try:
        pic = draw(t)
    finally:
        r = end()
    out = []
    for it in _merge(r.items):
        k = it['k']
        x0, y0, x1, y1 = it['box']
        out.append((it['name'], round(x0 * k), round(y0 * k), round(x1 * k), round(y1 * k), int(it['mask'].sum() * k * k)))
    for name, box_at in getattr(film, 'KEEP_CLEAR', ()):
        try:
            b = box_at(t)
        except Exception:
            b = None
        if b:
            out.append((name, *(int(v) for v in b), int((b[2] - b[0]) * (b[3] - b[1]))))
    return pic, out


if __name__ == '__main__':
    import body as B
    B.SS = 1
    film = importlib.import_module(sys.argv[1])
    import cover as _me                           # the painters import `cover`: record through that same copy
    for t in map(float, sys.argv[2:]):
        items, fr, blind = _me.record(film, t)
        print(f'{t:.2f} s: {len(items)} layers: ' + ', '.join(f'{i["name"]} {i["rng"][0]:.2f}-{i["rng"][1]:.2f}'
                                                             for i in _merge(items)))
        if blind:
            print('  no depth:', ', '.join(sorted(blind)))
        for f, n, px in _me.faults(items, fr):
            print(f'  FAULT: {f["name"]} ({f["rng"][0]:.2f} m) drawn over {n["name"]} ({n["rng"][1]:.2f} m): {px} px')
