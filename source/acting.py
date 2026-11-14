#!/usr/bin/env python3
"""MAP  Moves from the acting list (ranking item 7; overnight chat 7, 14 Nov). A film's moves are plain lines in
`story/FILM-moves.txt`, one block per shot, each block one row of the acting list (rule 74): who, the line, the word
the move lands on, the face and the body. This kit turns each block into the pose the film draws (views.person's
joints, plus mark and yaw when the person walks), timed to the voice. Closest before it: moves.py (gaits, keyed
poses), blessed.py's arm_keys/_bump (lifted here unchanged), perform.py. What is new: the moves are words, not code;
a hand place, a body move or a gait written once is in the library for every film; `check` ties each block to its
acting-list row (the word it lands on). No film imports this until Sam approves the kit (overnight run, answer 2).

THE LANGUAGE (story/FILM-moves.txt; '#' starts a comment)
    gait NAME: like walk, sps 1.8, step 0.5, swing 0.42, bend 0.25, lean -3       a gait (moves.GAITS) by its numbers
    place NAME: sw+300, 40, 150, out, palm      a hand place for the RIGHT hand (the left is mirrored): x (sw = the
                                               shoulders' half-width; 0.55sw allowed), y down, z forward; elbow pole
                                               (a word or 'pole 1 0.8 0.3'); hand shape. PLACES has the library's.
    body NAME: lean 7, roll 5                   a body move: channels per unit (lean, nod, roll, dip, bob, head_dy);
                                               'lean 2.5 shifts 81 0.8 1.4' = filmkit.shifts idle life (seed, hold)
    ## SHOT: WHO, line N, lands on "WORD"       starts a block (lands on: a quoted word or a beat name)
    row: ...                                   the acting-list row, as words (read by people, not the kit)
    like: SHOT                                 the same block as another shot (oath2 = oath)
    face: MOOD, shades on | gaze -0.6 from A to B | MOOD2 from A      the face column (the film's moods)
    walk: GAIT from X D to X D on PLACE, over S|auto, phase P, settle W | settle A to B, still from T, chest C,
          sway A [at STEPS_PER_S]      linear from A to B; mixed into the stance over the settle; the head rolls
    L: / R: / both: KEY | KEY ...               a hand through timed keys; KEY = 'PLACE at T', 'PLACE from T to T'
                                               (held), 'rest at T' (where the stance puts it); a second line for the same
                                               hand lies over the first from its first key on ('rest' = the first's)
    body: MOVE [AMOUNT] [with CH V, CH V] from A to B[, rise R, fall F]    up and back down (a bump)
    body: MOVE [AMOUNT] ... from A over D                                   eased up, then held
    body: MOVE [AMOUNT] ... except from A to B[, rise R, fall F]            held, down only between A and B
    holds L|R: PROP [between A and B, ...]      a thing in the hand (the film's PROPS: beads, bible ...)
  TIMES: "word" (the block's line says it), a beat in the film's timeline (s2, hollow, bang), end (the line's last
    word), cut / start (the shot's), landed (the walk's end), min(A, B), +/- seconds; a bare number is seconds into
    the shot.

    python3 source/acting.py check FILM             every block parses; each lands on a move within 0.3 s (rule 74)
    python3 source/acting.py replicate FILM OUT_DIR the finished film's frames beside the same frames with the kit's
                                                    moves swapped in (nothing in the film changes); one sheet, scores

MAP  library 60 | parse 120 | times 205 | hands 240 | body 300 | pose 335 | films 410 | check, replicate 460 | main 540
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

import figure as F           # noqa: E402
import views as V            # noqa: E402
import moves                 # noqa: E402

# =============================================== library ===========================================================
# Hand places for the right hand (x out from the body; the left hand mirrors x): (sw multiple, x, y, z, pole, shape).
# Each was tuned on a finished film and is named for what it means, so the acting list's words find it.
PLACES = {
    'heart': (0.0, 30.0, 135.0, 78.0, 'out', 'palm'),        # Blessed arrival: hand on the heart (chat 6: not 'in')
    'point': (1.0, 150.0, 20.0, 230.0, 'out', 'point'),      # points at the pack (note 34)
    'wide': (1.0, 300.0, 40.0, 150.0, 'out', 'palm'),        # flung open at shoulder height
    'sweep': (1.0, 300.0, 40.0, 160.0, 'out', 'palm'),       # swept open to a crowd
    'messiah': (1.0, 290.0, -110.0, 90.0, 'out', 'palm'),    # up and out, palms open
    'arms out': (1.0, 200.0, 120.0, 40.0, 'down', 'palm'),   # out to the side on the way up (figure-rig 3's waypoint)
    'hair': (0.55, 0.0, -250.0, 40.0, 'out', 'palm'),        # a hand back through the hair (note 49; 'in' folded)
    'hair back': (0.95, 0.0, -200.0, -30.0, 'out', 'palm'),
    'oath hand': (1.0, 40.0, -140.0, 100.0, (1.0, 0.8, 0.3), 'palm'),   # the raised hand of an oath, palm out
    'oath mid': (1.0, 70.0, 60.0, 90.0, (1.0, 0.8, 0.3), 'palm'),       # its way up: the elbow never folds tight
    'bible': (0.0, 6.0, 120.0, 128.0, 'down', 'fist'),       # a book held up at the shirt opening
    'clasp low': (0.0, 10.0, 420.0, 60.0, 'back', 'fist'),   # hands clasped low in front (the dock)
}
# Body moves: channels per unit of the move (the first channel is the one an AMOUNT sets; the rest scale with it).
# lean: degrees forward; nod: + down; roll: head tilt; dip: down at the knees, feet kept; bob, head_dy: drops.
BODY = {
    'lean in': dict(lean=7.0, roll=5.0),
    'bow': dict(lean=6.0, nod=1.4),
    'chin up': dict(nod=-2.5),
    'dip': dict(dip=60.0),
    'slump': dict(bob=12.0, head_dy=10.0, lean=4.0),
    'start': dict(bob=5.0),                                   # a small start (a bang heard)
    'tilt': dict(roll=4.0),
    'nod': dict(nod=0.9),
    'preen': dict(nod=-1.2),
    'bask': dict(lean=(2.5, 81, 0.8, 1.4), roll=(5.0, 82, 0.7, 1.3)),   # weight shifts, basking (filmkit.shifts)
    'lean': dict(lean=1.0), 'roll': dict(roll=1.0), 'nod by': dict(nod=1.0),
}
CHANNELS = ('lean', 'nod', 'roll', 'dip', 'bob', 'head_dy')
SWAY = 3.5                     # the swagger's head roll towards each planted foot (degrees)


def ease(u):
    return u * u * (3 - 2 * u)


def ramp(t, a, b):
    return min(1.0, max(0.0, (t - a) / max(1e-6, b - a)))


def bump(t, a, b, rise=0.2, fall=0.25):
    return ease(ramp(t, a, a + rise)) * (1 - ease(ramp(t, b - fall, b)))


# =============================================== parse =============================================================
def _num(s):
    return float(s.strip())


def _split_time(text):
    """'heart from "feeling" to "mate" -0.35' -> words before the first time word, then the time parts."""
    return text


def parse(text):
    """The moves file -> {'gaits', 'places', 'body', 'shots': {shot: block}}. A block is a dict of its lines."""
    out = dict(gaits={}, places={}, body={}, shots={})
    cur = None
    for raw in text.splitlines():
        line = raw.split(' #')[0].rstrip() if not raw.lstrip().startswith('row:') else raw.rstrip()
        if not line.strip() or line.lstrip().startswith('#') and not line.startswith('##'):
            continue
        if line.startswith('## '):
            m = re.match(r'## (\w+): (\w+)(?:, line (\d+))?(?:, lands on (.+))?', line)
            if not m:
                raise ValueError(f'moves: cannot read the block line {line!r}')
            shot, who, n, lands = m.groups()
            lands = lands.split(' (')[0].strip() if lands else None
            cur = dict(shot=shot, who=who, line=int(n) if n else None, lands=lands, hands=[], body=[], holds=[],
                       face=None, walk=None, like=None, row=None)
            out['shots'][shot] = cur
            continue
        key, _, rest = line.partition(':')
        key, rest = key.strip(), rest.strip()
        if cur is None:
            kind, _, name = key.partition(' ')
            if kind == 'gait':
                out['gaits'][name] = _gait(rest)
            elif kind == 'place':
                out['places'][name] = _place(rest)
            elif kind == 'body':
                out['body'][name] = _channels(rest)
            else:
                raise ValueError(f'moves: unknown library line {line!r}')
            continue
        if key == 'row':
            cur['row'] = rest
        elif key == 'like':
            cur['like'] = rest
        elif key == 'face':
            cur['face'] = _face(rest)
        elif key == 'walk':
            cur['walk'] = _walk(rest)
        elif key in ('L', 'R', 'both'):
            for sd in (('L', 'R') if key == 'both' else (key,)):
                cur['hands'].append((sd, [_key(k) for k in rest.split('|')]))
        elif key == 'body':
            cur['body'].append(_body(rest))
        elif key.startswith('holds'):
            cur['holds'].append(_holds(key.split()[1], rest))
        else:
            raise ValueError(f'moves: unknown line in block {cur["shot"]}: {line!r}')
    return out


def _gait(rest):
    parts = [p.strip() for p in rest.split(',')]
    base = parts[0].split()[1]
    d = dict(like=base)
    for p in parts[1:]:
        k, v = p.split()
        d[k] = float(v)
    return d


def _place(rest):
    parts = [p.strip() for p in rest.split(',')]
    m = re.match(r'^(?:([\d.]*)sw)?\s*([+-]?\s*[\d.]+)?$', parts[0].replace(' ', ''))
    a = float(m.group(1) or 1.0) if 'sw' in parts[0] else 0.0
    c = float(m.group(2)) if m.group(2) else 0.0
    pole = parts[3]
    if pole.startswith('pole'):
        pole = tuple(float(x) for x in pole.split()[1:])
    return (a, c, float(parts[1]), float(parts[2]), pole, parts[4])


def _channels(rest):
    d = {}
    for p in rest.split(','):
        w = p.split()
        if 'shifts' in w:
            d[w[0]] = (float(w[1]), int(w[3]), float(w[4]), float(w[5]))
        else:
            d[w[0]] = float(w[1])
    return d


def _face(rest):
    parts = [p.strip() for p in rest.split('|')]
    first = [x.strip() for x in parts[0].split(',')]
    f = dict(mood=first[0], shades=None, gaze=[], later=[])
    for x in first[1:]:
        if x.startswith('shades'):
            f['shades'] = x.split()[1]
    for p in parts[1:]:
        if p.startswith('gaze'):
            m = re.match(r'gaze ([-\d.]+) from (.+) to (.+)$', p)
            f['gaze'].append((float(m.group(1)), m.group(2), m.group(3)))
        else:
            mood, _, at = p.partition(' from ')
            f['later'].append((at.strip(), mood.strip()))
    return f


def _walk(rest):
    m = re.match(r'(\w+) from ([-\d.]+) ([-\d.]+) to ([-\d.]+) ([-\d.]+) on (\w+)(.*)$', rest)
    g, x0, d0, x1, d1, where, more = m.groups()
    w = dict(gait=g, a=(float(x0), float(d0)), b=(float(x1), float(d1)), on=where, over='auto', phase=0.0,
             settle=0.15, still=None, chest=0.0, sway=SWAY)
    for p in [p.strip() for p in more.split(',') if p.strip()]:
        k, _, v = p.partition(' ')
        if k == 'settle' and ' to ' in v:
            w['settle'] = tuple(float(x) for x in v.split(' to '))
        elif k in ('over',):
            w[k] = v if v == 'auto' else float(v)
        elif k == 'still':
            w['still'] = v.replace('from', '').strip()
        elif k == 'sway':
            a, _, r = v.partition(' at ')
            w['sway'], w['sway_rate'] = float(a), float(r) if r else None
        else:
            w[k] = float(v)
    return w


def _key(text):
    text = text.strip()
    m = re.match(r'(.+?) from (.+) to (.+)$', text)
    if m:
        return ('hold', m.group(1).strip(), m.group(2).strip(), m.group(3).strip())
    m = re.match(r'(.+?) at (.+)$', text)
    if not m:
        raise ValueError(f'moves: a hand key needs "at" or "from .. to": {text!r}')
    return ('at', m.group(1).strip(), m.group(2).strip())


def _body(rest):
    m = re.match(r'(.+?) (except from|from) (.+)$', rest)
    head, how, tail = m.groups()
    w = dict(curve='bump' if how == 'from' else 'except', rise=0.2, fall=0.25, over=None)
    h = re.match(r'([a-z][a-z ]*?)(?: ([-\d.]+))?(?: with (.+))?$', head.strip())
    w['move'], amt, extra = h.groups()
    w['amount'] = float(amt) if amt else None
    w['with'] = _channels(extra) if extra else {}
    parts = [p.strip() for p in tail.split(',')]
    m2 = re.match(r'(.+) over ([\d.]+)$', parts[0])
    if m2:
        w['curve'], w['a'], w['over'] = 'ramp', m2.group(1), float(m2.group(2))
    else:
        w['a'], w['b'] = parts[0].split(' to ')
    for p in parts[1:]:
        k, v = p.split()
        w[k] = float(v)
    return w


def _holds(side, rest):
    name, _, wins = rest.partition(' between ')
    spans = []
    if wins:
        for s in ('between ' + wins).split(', between '):
            a, b = s.replace('between ', '').split(' and ')
            spans.append((a.strip(), b.strip()))
    return (side, name.strip(), spans)


def lines(film):
    """The moves file for the page (page.py): (line number, 'SHOT (WHO): the line') for every line in a block, so a
    note on a move ("his dip on 'super' is too deep") finds its line and the chat opens that one line."""
    p = os.path.join(ROOT, 'story', f'{film}-moves.txt')
    if not os.path.exists(p):
        return []
    out, cur = [], None
    for n, raw in enumerate(open(p, encoding='utf-8'), 1):
        ln = raw.rstrip()
        m = re.match(r'## (\w+): (\w+)', ln)
        if m:
            cur = f'{m.group(1)} ({m.group(2)})'
            continue
        if cur and ln.strip() and not ln.startswith('#'):
            out.append((n, f'{cur}: {ln.strip()}'))
    return out


def gist(text):
    """A moves line without its times, for the page: 'gates2 (brand): R: messiah | hair | hair back | rest'."""
    if ': row:' in text:
        return text[:100]
    t = re.sub(r'"([^"]*)"', r'\1', text.replace('min(', '('))
    t = re.sub(r'[-+]?\d+\.?\d*|\b(at|from|to|over|rise|fall|between|and|except)\b|[,()]', ' ', t)
    return re.sub(r'\s+', ' ', t).replace(' |', ' |').strip()[:110]


def load(film):
    with open(os.path.join(ROOT, 'story', f'{film}-moves.txt')) as f:
        return parse(f.read())


# =============================================== times =============================================================
class Clock:
    """Resolves the language's times for one block at one shot: words through the film's word_at, beats from T."""

    def __init__(self, film, block, shot, landed=None):
        self.f, self.b, self.shot = film, block, shot
        self.start, self.cut = film['span'](shot)
        self.landed = landed
        self._memo = {}

    def __call__(self, text):
        if text in self._memo:
            return self._memo[text]
        anchored = [False]

        def word(m):
            anchored[0] = True
            return repr(self.f['word_at'](self.b['line'], m.group(1)))

        def name(m):
            n = m.group(0)
            if n == 'min' or n == 'max':
                return n
            anchored[0] = True
            if n == 'end':
                return repr(self.f['line_end'](self.b['line']))
            if n == 'cut':
                return repr(self.cut)
            if n == 'start':
                return repr(self.start)
            if n == 'landed':
                return repr(self.landed)
            return repr(self.f['T'][n])
        s = re.sub(r'"([^"]+)"', word, text)
        s = re.sub(r'(?<![\d.\'])\b[a-z_][a-z_0-9]*\b', name, s)
        v = float(eval(s, {'__builtins__': {}}, {'min': min, 'max': max}))
        if not anchored[0]:
            v += self.start
        self._memo[text] = v
        return v


# =============================================== hands (blessed.py's arm_keys, lifted unchanged) ===================
def _contact(j, side, off):
    el, wr = j['el' + side], j['wr' + side]
    return V._add(wr, V._mul(V._unit(V._sub(wr, el)), off))


def _rest_spec(sp, side, j=None):
    j = j or V.standing(sp)
    shape = j.get('hand', {}).get(side, 'fist')
    sg = -1 if side == 'L' else 1
    e = V._unit(V._sub(j['el' + side], j['sh' + side]))
    return _contact(j, side, F.HAND.get(shape, 14)), (sg * e[0], e[1], e[2]), shape


def _arm(j, side, target, pole, off, shape):
    sg = -1 if side == 'L' else 1
    px, py, pz = V.POLES[pole] if isinstance(pole, str) else pole
    el, end = V.ik3(j['sh' + side], target, F.UPPER * 0.98, F.FORE * 0.98 + off, (sg * px, py, pz))
    j['el' + side], j['wr' + side] = el, V._add(el, V._mul(V._unit(V._sub(end, el)), F.FORE * 0.98))
    j.setdefault('hand', {})[side] = shape
    return j


def arm_keys(j, sp, side, t, keys):
    """The hand on `side` through timed keys [(t, spec)]: spec = (target, pole, shape), or None for the hand where `j`
    already has it (rest). Between two keys the contact point and the pole blend, eased."""
    rest = _rest_spec(sp, side, j)

    def spec(s):
        if s is None:
            return rest
        tgt, pole, shape = s
        return tgt, V.POLES[pole] if isinstance(pole, str) else pole, shape
    if t <= keys[0][0]:
        a = b = spec(keys[0][1])
        u = 0.0
    elif t >= keys[-1][0]:
        a = b = spec(keys[-1][1])
        u = 0.0
    else:
        (t0, sa), (t1, sb) = next(((k0, k1) for k0, k1 in zip(keys, keys[1:]) if t < k1[0]))
        a, b = spec(sa), spec(sb)
        u = ease(ramp(t, t0, t1))
    if a is rest and b is rest:
        return j
    tgt = moves.lerp(a[0], b[0], u)
    pole = moves.lerp(a[1], b[1], u)
    off = F.HAND.get(a[2], 14) + (F.HAND.get(b[2], 14) - F.HAND.get(a[2], 14)) * u
    return _arm(j, side, tgt, pole, off, b[2] if u >= 0.5 else a[2])


def place(name, side, sw, places):
    """A named hand place for `side` as an arm spec. 'wide fist' = the place 'wide' with a fist."""
    shape = None
    if name not in places:
        base, _, shp = name.rpartition(' ')
        if base in places and shp in F.HAND:
            name, shape = base, shp
        else:
            raise KeyError(f'moves: no hand place {name!r} (the library: {", ".join(sorted(places))})')
    a, c, y, z, pole, shp = places[name]
    sg = -1 if side == 'L' else 1
    return (sg * (a * sw + c), y, z), pole, shape or shp


def hand_keys(keys, side, sw, clock, places):
    out = []
    for k in keys:
        spec = None if k[1] == 'rest' else place(k[1], side, sw, places)
        if k[0] == 'at':
            out.append((clock(k[2]), spec))
        else:
            out += [(clock(k[2]), spec), (clock(k[3]), spec)]
    return out


# =============================================== body ==============================================================
def body_value(m, t, clock, table):
    """{channel: value} of one body move at t."""
    if m['curve'] == 'ramp':
        a = clock(m['a'])
        u = ease(ramp(t, a, a + m['over']))
    else:
        u = bump(t, clock(m['a']), clock(m['b']), m['rise'], m['fall'])
        if m['curve'] == 'except':
            u = 1 - u
    base = dict(table[m['move']])
    first = next(iter(base))
    if m['amount'] is not None:
        f0 = base[first][0] if isinstance(base[first], tuple) else base[first]
        k = abs(m['amount'] / f0) if f0 else 1.0
        base = {c: ((v[0] * k,) + v[1:] if isinstance(v, tuple) else v * k) for c, v in base.items()}
    base.update(m['with'])
    out = {}
    for c, v in base.items():
        if isinstance(v, tuple):
            import filmkit
            out[c] = u * filmkit.shifts(t, seed=v[1], amount=v[0], hold=(v[2], v[3]))
        else:
            out[c] = v * u
    return out


def dip(j, amt, splay=0.2):
    """Down at the knees by `amt` person units, feet kept on the floor, knees opening a little (blessed._dip)."""
    if amt <= 0:
        return j
    j['bob'] = j.get('bob', 0.0) + amt
    for sd, sg in (('L', -1), ('R', 1)):
        x, y, z = j['foot' + sd]
        j['foot' + sd] = (x, y - amt, z)
        j['knee_pole' + sd] = (sg * splay, 0.0, 1.0)
    return j


# =============================================== pose ==============================================================
def install_gaits(desc):
    for name, g in desc['gaits'].items():
        d = dict(moves.GAITS[g['like']])
        d.update({k: v for k, v in g.items() if k != 'like'})
        moves.GAITS[name] = d


def block_for(desc, shot):
    b = desc['shots'][shot]
    while b.get('like'):
        b = dict(desc['shots'][b['like']], shot=shot)
    return b


def walk_time(w):
    if w['over'] != 'auto':
        return w['over']
    return math.hypot(w['b'][0] - w['a'][0], w['b'][1] - w['a'][1]) / moves.speed(w['gait'])


def pose(desc, film, shot, sp, t):
    """(mark or None, yaw, joints) for the block of `shot` at film time t."""
    b = block_for(desc, shot)
    places = dict(PLACES, **desc['places'])
    table = dict(BODY, **desc['body'])
    w = b['walk']
    start = film['span'](shot)[0]
    k = t - start
    mark, yaw = None, 0.0
    if w:
        dur = walk_time(w)
        u = min(1.0, max(0.0, k / dur))
        mark = film['ground'](w['on'], w['a'][0] + (w['b'][0] - w['a'][0]) * u, w['a'][1] + (w['b'][1] - w['a'][1]) * u)
        g = moves.gait(sp, k + w['phase'], w['gait'])
        s0, s1 = w['settle'] if isinstance(w['settle'], tuple) else (dur - w['settle'], dur + w['settle'])
        settle = ease(ramp(k, s0, s1))
        j = moves.mix_poses(g, V.standing(sp), settle)
        still = float(w['still']) if w['still'] else s1
        if k >= still:
            j['bob'] = 0.0
            j['lean'] = 0.0
        rate = w.get('sway_rate') or moves.GAITS[w['gait']]['sps']          # towards each planted foot
        j['head_roll'] = w['sway'] * math.sin(math.pi * rate * (k + w['phase'])) * (1 - settle)
        if w['chest']:
            j['lean'] = j.get('lean', 0.0) - w['chest'] * (1 - settle)
        landed = start + dur
    else:
        j = V.standing(sp)
        landed = None
    clock = Clock(film, b, shot, landed)
    sw = sp.get('shoulders', 150)
    seen = set()
    for side, keys in b['hands']:
        ks = hand_keys(keys, side, sw, clock, places)
        if side in seen and t < ks[0][0]:
            continue                                  # a later line for this hand lies over the first from its start
        seen.add(side)
        arm_keys(j, sp, side, t, ks)
    tot = {}
    for m in b['body']:
        for c, v in body_value(m, t, clock, table).items():
            tot[c] = tot.get(c, 0.0) + v
    dip(j, tot.pop('dip', 0.0))
    if 'nod' in tot:
        j['nod'] = tot.pop('nod')
    if 'roll' in tot:
        j['head_roll'] = j.get('head_roll', 0.0) + tot.pop('roll')
    for c, v in tot.items():
        j[c] = j.get(c, 0.0) + v
    for side, name, spans in b['holds']:
        if not spans or any(clock(a) < t < clock(c) for a, c in spans):
            film['props'][name](j, side, sp)
    return mark, yaw, j


def face(desc, film, shot, t):
    """(mood, shades, gaze) of the block's face line at t."""
    b = block_for(desc, shot)
    f = b['face']
    if not f:
        return None
    clock = Clock(film, b, shot)
    mood = f['mood']
    for at, m in f['later']:
        if t >= clock(at):
            mood = m
    gaze = sum(g for g, a, c in f['gaze'] if clock(a) <= t < clock(c))
    return mood, f['shades'], gaze


# =============================================== films =============================================================
def _blessed():
    """Blessed's side of the kit: its timeline, words, places and the things its people hold."""
    import blessed as BL
    import grips
    ST = BL.ST
    spans = {s: (a, b) for s, a, b in BL.SHOTS}
    return dict(
        module=BL, T=BL.T, word_at=BL.word_at, line_end=lambda n: BL.L[n]['end'],
        line_start=lambda n: BL.L[n]['start'],
        span=lambda shot: spans[shot],
        ground=lambda on, x, d: ST._mark(getattr(ST, on), x, d),
        props={'beads': lambda j, side, sp: grips.held(j, side, sp, BL._beads(sp)),
               'sleeve edge': lambda j, side, sp: grips.held(j, side, sp, BL._sleeve_edge(sp)),
               'bible': lambda j, side, sp: BL._bible(j, sp)},
        # which film functions the kit stands in for: shot -> (function name, returns mark and yaw too)
        stands_in={'arrive': ('arrive', True), 'oath': ('oath', False), 'oath2': ('oath', False),
                   'dock': ('dock', False), 'gates': ('gates_wide', True), 'gates2': ('gates_close', True)})


FILMS = {'blessed': _blessed}
FRAMES = {'blessed': [1.0, 2.3, 2.9, 3.6, 4.1, 5.0, 6.6, 12.0, 14.2, 15.6, 16.8, 49.6, 50.3,
                      51.6, 52.6, 53.5, 54.9]}


def film_side(film):
    return FILMS[film]()


def install(desc, film):
    """Swap the film's pose functions for the kit's (returns the originals, to put back)."""
    install_gaits(desc)
    BL = film['module']
    keep = {}
    for shot, (fn, walks) in film['stands_in'].items():
        if shot not in desc['shots']:
            continue
        keep.setdefault(fn, getattr(BL, fn))
    by_fn = {}
    for shot, (fn, walks) in film['stands_in'].items():
        if shot in desc['shots']:
            by_fn.setdefault(fn, []).append((shot, walks))

    def make(fn, shots):
        def stand_in(sp, t):
            shot = BL.shot_of(t)
            if shot not in [s for s, _ in shots]:
                shot = shots[0][0]
            mark, yaw, j = pose(desc, film, shot, sp, t)
            return (mark, yaw, j) if shots[0][1] else j
        return stand_in
    for fn, shots in by_fn.items():
        setattr(BL, fn, make(fn, shots))
    keep['brand_mood'] = BL.brand_mood
    keep['oath_gaze'] = BL.oath_gaze
    old_mood, old_gaze = BL.brand_mood, BL.oath_gaze

    def mood(t):
        shot = BL.shot_of(t)
        if shot in desc['shots'] and block_for(desc, shot)['face']:
            m, sh, _ = face(desc, film, shot, t)
            return m, sh
        return old_mood(t)

    def gaze(t):
        shot = BL.shot_of(t)
        if shot in desc['shots'] and block_for(desc, shot)['face']:
            return face(desc, film, shot, t)[2]
        return old_gaze(t)
    BL.brand_mood, BL.oath_gaze = mood, gaze
    return keep


def uninstall(film, keep):
    for fn, f in keep.items():
        setattr(film['module'], fn, f)


# =============================================== check, replicate ==================================================
def check(film_name):
    """Faults in plain words: a block that does not read, a time that does not resolve, a block whose acting-list
    'lands on' has no move within 0.3 s of it (rule 74: moves checked against the acting list)."""
    desc = load(film_name)
    film = film_side(film_name)
    install_gaits(desc)
    faults = []
    for shot in desc['shots']:
        b = block_for(desc, shot)
        if shot not in film['stands_in'] and shot not in [s for s, _, _ in film['module'].SHOTS]:
            faults.append(f'{shot}: no such shot in the film')
            continue
        try:
            landed = film['span'](shot)[0] + walk_time(b['walk']) if b['walk'] else None
            clock = Clock(film, b, shot, landed)
            times = []
            for side, keys in b['hands']:
                times += [k for k, _ in hand_keys(keys, side, 150, clock, dict(PLACES, **desc['places']))]
            for m in b['body']:
                times.append(clock(m['a']))
                if m.get('b'):
                    times.append(clock(m['b']))
            if b['lands']:
                at = clock(b['lands'])
                if not times or min(abs(x - at) for x in times) > 0.3:
                    faults.append(f'{shot}: nothing lands on {b["lands"]} ({at:.2f} s): the acting list says it should')
            a, c = film['span'](shot)
            if b['line']:                                               # a line can run across a cut (the oath)
                a, c = min(a, film['line_start'](b['line'])), max(c, film['line_end'](b['line']))
            for x in times:
                if x < a - 1.0 or x > c + 5.0:
                    faults.append(f'{shot}: a key at {x:.2f} s is far outside the shot ({a:.2f}-{c:.2f} s)')
        except Exception as e:                                          # noqa: BLE001  any reading fault, in words
            faults.append(f'{shot}: does not read ({e})')
    return faults


def _differ(a, b):
    import numpy as np
    x = np.asarray(a.convert('RGB'), dtype=np.int16)
    y = np.asarray(b.convert('RGB'), dtype=np.int16)
    return float((np.abs(x - y).max(axis=2) > 24).mean() * 100)


def replicate(film_name, out_dir, times=None):
    """The finished film's frames beside the same frames with the kit's moves swapped in. One labelled sheet; a score
    per frame (share of pixels that differ by more than 24 levels; 0.00% = the same picture)."""
    from PIL import Image, ImageDraw, ImageFont
    desc = load(film_name)
    film = film_side(film_name)
    BL = film['module']
    times = times or FRAMES[film_name]
    olds = [BL.frame_image(t) for t in times]
    keep = install(desc, film)
    try:
        news = [BL.frame_image(t) for t in times]
    finally:
        uninstall(film, keep)
    font = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 22)
    tw, th, cols = 270, 480, 3
    rows = (len(times) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (2 * tw + 20) + 10, rows * (th + 40) + 10), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    scores = []
    for i, (t, a, b) in enumerate(zip(times, olds, news)):
        s = _differ(a, b)
        scores.append((f'{BL.shot_of(t)} {t:.1f}s', s))
        x, y = 10 + (i % cols) * (2 * tw + 20), 10 + (i // cols) * (th + 40)
        for k, im in enumerate((a, b)):
            sheet.paste(im.convert('RGB').resize((tw, th)), (x + k * tw, y + 34))
        d.text((x + 4, y + 6), f'{BL.shot_of(t)} {t:.1f}s: finished | kit {s:.2f}%', font=font, fill=(30, 30, 30))
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f'{film_name}-moves-replicate.jpg')
    sheet.save(out, quality=86)
    return out, scores


def picture(t, film_name='blessed'):
    """One film frame with the kit's moves in (the catalogue's tile: catalogue.py)."""
    desc, film = load(film_name), film_side(film_name)
    keep = install(desc, film)
    try:
        return film['module'].frame_image(t)
    finally:
        uninstall(film, keep)


def main():
    a = sys.argv[1:]
    if not a or a[0] not in ('check', 'replicate'):
        print(__doc__.split('MAP  library')[0])
        return 2
    if a[0] == 'check':
        f = check(a[1])
        print('\n'.join(f) if f else f'{a[1]} moves: every block reads and lands on its word')
        return 1 if f else 0
    out, scores = replicate(a[1], a[2])
    for lab, s in scores:
        print(f'  {lab}: {s:.3f}%')
    print(out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
