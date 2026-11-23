#!/usr/bin/env python3
"""MAP  The rough command (ranking item 1; overnight chat 10, 14 Nov). Rule 11: a quick rough of every new person, place
and move on ONE sheet before it is built, each sent once. Closest before it: the hand-made roughs (protest_tiers_roughs:
pencil, by hand, per film), people.py sheet, places.py picture, acting.py replicate. What is new: one command reads the
film's three description files (story/FILM-people.txt, -places.txt, -moves.txt) and draws only what Sam has NOT yet seen
on a rough (new, or changed since), with the three kits themselves, so the rough is the thing that will be built, not a
sketch of it; a record (story/FILM-roughs.txt) keeps what was sent, so nothing is sent twice, and the pre-flight warns
about anything built that never went on a rough.

  People: front, side, back at true heights (people.py). Crowds: their first 6 members.
  Places: each view painted by the places kit through its own camera, blue 1.75 m outlines at its people's depths.
  Moves: each block's person alone at its key moments (the start, each hand key, the word it lands on, the end), with
    the time and the word under each; a block left as code says so. With no film code yet (a new film), the moves are
    drawn on a draft clock: each word or beat the block names gets its own second, in the order written (the poses are
    the real ones; only the timing waits for the voice). A film with code (acting.FILMS) gets its true times.

    python3 source/rough.py sheet FILM OUT.jpg [--all] [--draft]   the sheet (--all: everything, sent or not;
                                                                    --draft: the draft clock even with film code)
    python3 source/rough.py sent FILM [OUT.jpg] --delivered                  after sending: records everything on the sheet
    python3 source/rough.py check FILM                             what is built but never sent on a rough (rule 11)
    python3 source/rough.py board FILM OUT.jpg [--root DIR]        the shot board (craft-step2): every shot in the
                                 film's SHOTS through its own picture(t): start, key beat, end, and the next shot's
                                 first frame; app-safe box and frame thirds drawn over; under each shot its row
                                 (story/FILM-board.txt: camera, lead, focus, next focus, match, choices; a field
                                 missing is printed red "not planned"). --root: a checkout of an older commit (the
                                 learn step draws from a film's first plan). Leaves OUT.jpg.json beside it.
                                 --shots A,B: only those shots (a re-staged shot drawn as built, before it moves:
                                 lesson staging-stills, source/staging.py)
    python3 source/rough.py sent FILM OUT.jpg --delivered --board   after sending the board: records each shot and
                                 its frames' digest (story/FILM-board-sent.txt) and ends the ledger's "board" stage;
                                 the pre-flight refuses without it (board_gate: a shot on no board, a shot with nobody
                                 in it, a board after the first move)

Map: items 40 | the record 85 | people 110 | places 135 | moves (draft clock 170, key times 210, tiles 240) |
     the sheet 310 | the board 420 | the board's record and gate 558 | main 712
"""
import datetime
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
BG = (232, 228, 222)


# ---------------------------------------------------------------------------------------------- items
def _path(film, kind):
    return os.path.join(ROOT, 'story', f'{film.replace("_", "-")}-{kind}.txt')   # story files use - (either spelling in)


def _blocks(text, head):
    """[(name, block text)] for every block that starts with a line matching `head` (its group 1 is the name)."""
    out, cur, buf = [], None, []
    for line in text.splitlines():
        m = re.match(head, line)
        if m:
            if cur:
                out.append((cur, '\n'.join(buf).strip()))
            cur, buf = m.group(1), [line]
        elif cur:
            buf.append(line)
    if cur:
        out.append((cur, '\n'.join(buf).strip()))
    return out


def _digest(s):
    s = '\n'.join(ln.split('  #')[0].rstrip() for ln in s.splitlines() if ln.strip() and not ln.startswith('# ---'))
    return hashlib.sha1(s.encode()).hexdigest()[:10]


def items(film):
    """{(kind, name): digest} for every person, place view and moves block the film describes."""
    out = {}
    p = _path(film, 'people')
    if os.path.exists(p):
        for name, b in _blocks(open(p).read(), r'#\s*([a-z][a-z_0-9]*):\s'):
            out[('person', name)] = _digest(b)
    p = _path(film, 'places')
    if os.path.exists(p):
        text = open(p).read()
        for place, pb in _blocks(text, r'#\s*place:\s*(.+?)\s*$'):
            colours = pb.split('## view')[0]                 # a place's colours change every view of it
            for name, b in _blocks(pb, r'##\s*view:\s*(\S+)'):
                out[('place', name)] = _digest(colours + b)
    p = _path(film, 'moves')
    if os.path.exists(p):
        text = open(p).read()
        lib = text.split('\n## ')[0]                          # the film's own gaits, places, body moves
        import acting
        keys = list(acting.load(film)['shots'])               # the kit's own keys, in the file's order
        for key, (head, b) in zip(keys, _blocks(text, r'##\s*([a-z0-9_]+:\s*[a-z0-9_]+)')):
            used = [ln for ln in lib.splitlines() if re.match(r'(gait|place|body) (\S+?):', ln)
                    and re.match(r'(gait|place|body) (\S+?):', ln).group(2) in b]
            out[('move', key)] = _digest('\n'.join(used) + b)
    return out


# ---------------------------------------------------------------------------------------------- the record
def record_path(film):
    return _path(film, 'roughs')


def record(film):
    """{(kind, name): (digest, date)} of everything already sent on a rough."""
    out = {}
    if os.path.exists(record_path(film)):
        for ln in open(record_path(film)):
            f = ln.split()
            if len(f) >= 4 and not ln.startswith('#'):
                out[(f[0], f[1])] = (f[2], f[3])
    return out


def new_items(film, every=False):
    """[(kind, name, why)] for what goes on the sheet: never sent ('new'), or changed since ('changed since DATE')."""
    sent = record(film)
    out = []
    for k, dg in items(film).items():
        if every or k not in sent:
            out.append((k[0], k[1], 'new' if k not in sent else 'sent ' + sent[k][1]))
        elif sent[k][0] != dg:
            out.append((k[0], k[1], f'changed since the rough of {sent[k][1]}'))
    return out


def mark_sent(film, sheet=''):
    have = items(film)
    rec = record(film)
    day = datetime.date.today().isoformat()
    for k, dg in have.items():
        if rec.get(k, (None,))[0] != dg:
            rec[k] = (dg, day)
    with open(record_path(film), 'w') as f:
        f.write(f'# What Sam has seen on a rough (rule 11; source/rough.py). kind name digest date. Last: {sheet}\n')
        for (kind, name), (dg, d) in sorted(rec.items()):
            f.write(f'{kind} {name} {dg} {d}\n')
    return len(have)


def gate_faults(film):
    """The pre-flight's rule 11 line: built things (in the description files) never sent on a rough."""
    if not any(os.path.exists(_path(film, k)) for k in ('people', 'places', 'moves')):
        return []
    left = [f'{k} {n}' for k, n, why in new_items(film)]
    if not left:
        return []
    return [f'{len(left)} new or changed thing(s) never on a rough (rule 11): {", ".join(left[:8])}'
            f'{" ..." if len(left) > 8 else ""}: python3 source/rough.py sheet {film} OUT.jpg, send it, then `sent`']


# ---------------------------------------------------------------------------------------------- people
def people_tile(film, names, crowd=6):
    """The people kit's own sheet for just these people (and these crowds' first members)."""
    import people as P
    import tempfile
    from PIL import Image
    cast = {w: sp for w, sp in P.load(film).items() if w in names}
    crowds = [w for w in P.crowds(film) if w in names]
    if not cast and not crowds:
        return None
    if crowds:
        for w in crowds:
            for i in range(crowd):
                cast[f'{w}{i}'] = P.crowd_person(P.crowds(film)[w], i)
    out = os.path.join(tempfile.mkdtemp(), 'people.jpg')
    P.sheet(film, out, cast=cast, yaws=(0, 90, 180), crowd=0)
    return Image.open(out).convert('RGB')


# ---------------------------------------------------------------------------------------------- places
def place_tile(film, view, w=300):
    """One view painted by the places kit alone through its camera; blue outlines (1.75 m) at its people's depths."""
    import places as PL
    from PIL import Image, ImageDraw
    import people_parts as PP
    B = PP.B
    B.SS = 1
    desc = PL.load(film)
    v = desc['views'][view]
    lv, cam = PL.level(v), B.Cam(1.0)               # metres through the view's level camera; the painter's 2D cam
    img = B.canvas(BG)
    ppl = sorted(v['people'].items(), key=lambda kv: -kv[1])
    for layer in ('back', 'mid', 'front'):
        if layer in ('mid', 'front'):
            _standins(img, lv, ppl, layer, v)
        paint = PL.painter(desc, view, layer)
        if paint:
            paint(img, cam, 0.0)
    tile = img.convert('RGB')
    tile.thumbnail((w, int(w * 16 / 9)))
    return tile


def _standins(img, cam, ppl, layer, v):
    """1.75 m outlines where the view's people stand, spread across the frame (the composition, not the cast)."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    n = len(ppl)
    ds = sorted(v['people'].values())
    for i, (who, dist) in enumerate(ppl):
        if (layer == 'mid') != (dist >= ds[-1]):       # the farthest under the middle layer, the rest over it
            continue
        x = (i + 1) / (n + 1) * 2.4 - 1.2
        X, Y = cam.p(x, dist, 0.0)
        _, Yh = cam.p(x, dist, 1.75)
        h = Y - Yh
        wd = h * 0.24
        lw = max(4, int(h / 90))                       # outlines: the painting stays readable through them
        d.rounded_rectangle((X - wd / 2, Yh + h * 0.13, X + wd / 2, Y), radius=wd / 2.5, outline=(60, 60, 200), width=lw)
        d.ellipse((X - h * 0.065, Yh, X + h * 0.065, Yh + h * 0.14), outline=(60, 60, 200), width=lw)


# ---------------------------------------------------------------------------------------------- moves: draft clock
def draft_side(film, desc):
    """A film side for a film with no code yet: every shot 0..8 s, each word or beat a block names gets its own second
    in the order written; people from the people file (no props, a plain seat)."""
    import people as P
    cast = P.install(P.load(film))
    slots = {}

    def slot(key):
        return slots.setdefault(key, 1.0 + len(slots) * 1.0)
    T = _Beats(slot)
    seat = lambda: __import__('sitting').Seat('plastic', width=150)                       # noqa: E731

    def sp(shot, who, t, mood, shades):
        base = cast.get(who) or cast.get(f'{who}_{shot}') or next(iter(cast.values()))
        return dict(base)
    return dict(module=None, T=T, word_at=lambda n, w: slot((n, w)), line_end=lambda n: slot((n, 'end')),
                line_start=lambda n: 0.0, span=lambda shot: (0.0, 8.0),
                ground=lambda on, x, d: (540.0, 1800.0, 300.0), props=_Skip(), extras=_Skip(), seats=_Seats(seat),
                sp=sp, mark=lambda shot, who: (540.0, 1800.0, 300.0), draft=True)


class _Beats(dict):
    def __init__(self, slot):
        super().__init__()
        self.slot = slot

    def __getitem__(self, k):
        return self.slot(('beat', k))


class _Skip(dict):
    def __getitem__(self, k):
        return lambda *a: None


class _Seats(dict):
    def __init__(self, seat):
        super().__init__()
        self.seat = seat

    def __getitem__(self, k):
        return self.seat


# ---------------------------------------------------------------------------------------------- moves: key times
def key_times(desc, film, key, most=5):
    """[(t, label)]: the block's start, the word it lands on and the shot's end always; then the moments most apart
    from those among its hand keys, body moves, timed channels and the walk (mid-walk, landed)."""
    import acting as A
    b = A.block_for(desc, key)
    landed = film['span'](b['shot'])[0] + A.walk_time(b['walk']) if b['walk'] else None
    clock = A.Clock(film, b, b['shot'], landed)
    start, cut = film['span'](b['shot'])
    found = []

    def add(text, label):
        try:
            found.append((clock(text) if isinstance(text, str) else float(text), label))
        except Exception:
            pass
    for side, keys in b['hands']:
        for k in keys:
            add(k[2] if k[0] == 'at' else k[3], f'{k[1]}')
    for m in b['body']:
        add(m['a'], m['move'])
    for line in b['keys']:
        for v, when in line['keys']:
            add(when, f"{line['ch']} {v:g}")
    add((start + cut) / 2, 'mid-shot')
    if landed is not None:
        add((start + landed) / 2, 'walking')
        add(landed, 'landed')
    fixed = [(start + 0.05, 'start'), (cut - 0.1, 'end')]
    if b['lands']:
        try:
            t = clock(b['lands'])
            if start <= t <= cut:
                fixed.append((t + (0.3 if film.get('draft') else 0.0), 'lands on ' + b['lands']))
        except Exception:
            pass
    pool = [(t, lab) for t, lab in found if start + 0.3 < t < cut - 0.3]
    picks = sorted(fixed)
    while pool and len(picks) < most:
        t, lab = max(pool, key=lambda c: min(abs(c[0] - p[0]) for p in picks))
        if min(abs(t - p[0]) for p in picks) < 0.35:
            break
        picks.append((t, lab))
        pool.remove((t, lab))
    return sorted(picks)


# ---------------------------------------------------------------------------------------------- moves: tiles
def move_tiles(film_name, keys, draft=False, tw=160, th=285):
    """{key: [(image, caption)]} each block's person alone at its key times; a block left as code gets one caption."""
    import acting as A
    from PIL import Image
    desc = A.load(film_name)
    A.install_gaits(desc)
    real = film_name in A.FILMS and not draft
    film = A.film_side(film_name) if real else draft_side(film_name, desc)
    import people_parts as PP
    from satire_style import install_circle_hands
    B, V = PP.B, PP.V
    install_circle_hands(B)
    keep = A.install(desc, film) if real else None
    out = {}
    try:
        for key in keys:
            b = A.block_for(desc, key)
            if b.get('code') and not (b['hands'] or b['body'] or b['walk'] or b['keys'] or b['stance']):
                out[key] = [(None, f'left as code: {b["code"]}')]
                continue
            tiles = []
            for t, lab in key_times(desc, film, key):
                try:
                    sp, mark, yaw, j, hy = A.person(desc, film, key, t)
                    s = 0.5 * sp.get('height', 1.75) / 1.75
                    img = Image.new('RGBA', (1080, 1920), BG + (255,))
                    V.person(img, B.Cam(1.0, 540, 960), 540, 840 - 928 * s, s, sp, t, yaw, j, head_yaw=hy)
                    img = img.crop((240, 40, 840, 1100)).convert('RGB')
                    img.thumbnail((tw, th))
                    tiles.append((img, f'{t:.1f}s {lab}'))
                except Exception as e:                                  # named on the sheet, never dropped quietly
                    tiles.append((None, f'{t:.1f}s {lab}: not drawn ({type(e).__name__}: {str(e)[:40]})'))
            errs = {c.split(': ', 1)[1] for im, c in tiles if im is None}
            if len(errs) == 1 and all(im is None for im, _ in tiles):
                tiles = [(None, f'not drawn ({errs.pop().split("(", 1)[-1].rstrip(")")}): the person is the film\'s '
                                f'own code; this block moves only {", ".join(k["ch"] for k in b["keys"]) or "a part"}')]
            out[key] = tiles
    finally:
        if keep is not None:
            A.uninstall(film, keep)
    return out


# ---------------------------------------------------------------------------------------------- the sheet
def sheet(film, out, every=False, draft=False):
    """One labelled sheet of everything new or changed; returns (path, [(kind, name, why)])."""
    from PIL import Image, ImageDraw, ImageFont
    todo = new_items(film, every)
    font = lambda n: ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)      # noqa: E731
    W = 1800
    parts = []

    def heading(text):
        im = Image.new('RGB', (W, 60), BG)
        ImageDraw.Draw(im).text((20, 14), text, font=font(30), fill=(30, 30, 30))
        parts.append(im)
    why = {(k, n): w for k, n, w in todo}
    ppl = [n for k, n, _ in todo if k == 'person']
    if ppl:
        heading(f'People ({len(ppl)}): front, side, back; ' + ', '.join(f'{n} ({why["person", n]})' for n in ppl)[:110])
        im = people_tile(film, set(ppl))
        if im:
            im.thumbnail((W, 100000))
            parts.append(im)
    views = [n for k, n, _ in todo if k == 'place']
    if views:
        heading(f'Places ({len(views)} views): the kit\'s painting, blue outlines (1.75 m) where its people stand')
        tw, cols = 290, 6
        th = int(tw * 16 / 9) + 40
        rows = (len(views) + cols - 1) // cols
        im = Image.new('RGB', (W, rows * th + 10), BG)
        d = ImageDraw.Draw(im)
        for i, v in enumerate(views):
            x, y = 10 + (i % cols) * (tw + 8), (i // cols) * th
            try:
                im.paste(place_tile(film, v, tw), (x, y + 34))
                lab = v
            except Exception as e:
                lab = f'{v}: not drawn ({type(e).__name__})'
            d.text((x + 2, y + 6), f'{lab} ({why["place", v]})'[:34], font=font(17), fill=(30, 30, 30))
        parts.append(im)
    mv = [n for k, n, _ in todo if k == 'move']
    if mv:
        heading(f'Moves ({len(mv)} blocks): each person alone at the key moments'
                + (' (draft clock: timing waits for the voice)' if draft or film not in _films() else ''))
        tiles = move_tiles(film, mv, draft)
        tw, th, per_row = 160, 285, 2
        bw = 5 * (tw + 8)
        rows = (len(mv) + per_row - 1) // per_row
        im = Image.new('RGB', (W, rows * (th + 70) + 10), BG)
        d = ImageDraw.Draw(im)
        for i, k in enumerate(mv):
            x, y = 10 + (i % per_row) * (bw + 60), (i // per_row) * (th + 70)
            d.text((x, y + 4), f'{k} ({why["move", k]})', font=font(19), fill=(30, 30, 30))
            for c, (tile, cap) in enumerate(tiles.get(k, [])):
                if tile is not None:
                    im.paste(tile, (x + c * (tw + 8), y + 30))
                    d.text((x + c * (tw + 8), y + 32 + th), cap[:22], font=font(13), fill=(60, 60, 60))
                else:
                    d.text((x, y + 60 + 22 * c), cap[:80], font=font(15), fill=(150, 30, 30))
        parts.append(im)
    if not parts:
        heading(f'{film}: nothing new since the last rough')
    top = Image.new('RGB', (W, 70), BG)
    ImageDraw.Draw(top).text((20, 16), f'{film}: the rough of every new thing (rule 11), {datetime.date.today()}',
                             font=font(36), fill=(20, 20, 20))
    parts.insert(0, top)
    sheet_im = Image.new('RGB', (W, sum(p.height for p in parts)), BG)
    y = 0
    for p in parts:
        sheet_im.paste(p, (0, y))
        y += p.height
    sheet_im.save(out, quality=84)
    return out, todo


# ---------------------------------------------------------------------------------------------- the board
BOARD_FIELDS = ('camera', 'lead', 'focus', 'next focus', 'match', 'choices')
SAFE = (60, 310, 900, 1500)                       # the app's safe area at 1080 x 1920 (preflight.SAFE)
_GRAB = r"""
import json, os, sys
root, mod, out = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.join(root, 'source')); os.chdir(root)
import importlib; F = importlib.import_module(mod)
shots = [(n, float(a), float(b)) for n, a, b in F.SHOTS if float(b) > float(a)]
only = [x for x in os.environ.get('BOARD_ONLY', '').split(',') if x]   # --shots: a re-staged shot's own board
beats = {k: float(v) for k, v in vars(F).items() if k.isupper() and isinstance(v, (int, float))
         and not isinstance(v, bool) and k not in ('FPS', 'SR', 'W', 'H', 'DUR', 'BLACK_AT')}
beats.update({k: float(v) for k, v in (getattr(F, 'T', None) or {}).items() if isinstance(v, (int, float))})
starts = {round(a, 3) for _, a, _ in shots}
want = {}
for i, (n, a, b) in enumerate(shots):
    if only and n not in only:
        continue
    mid = (a + b) / 2
    inside = [(abs(t - mid), k, t) for k, t in beats.items() if a + 0.3 < t < b - 0.3 and round(t, 3) not in starts]
    key = min(inside)[1:] if inside else ('middle', mid)
    want[n] = [('start', a + 0.04), (key[0], key[1]), ('end', b - 0.06)]
    if i + 1 < len(shots):
        want[n].append(('next: ' + shots[i + 1][0], shots[i + 1][1] + 0.04))
done, cache = {}, {}
for n, moments in want.items():
    done[n] = []
    for lab, t in moments:
        f = os.path.join(out, f'{t:.3f}.jpg')
        if f not in cache:
            try:
                im = F.picture(t).convert('RGB'); im.thumbnail((360, 640)); im.save(f, quality=86); cache[f] = ''
            except Exception as e:
                cache[f] = f'{type(e).__name__}: {str(e)[:50]}'
        done[n].append((lab, round(t, 2), f, cache[f]))
cast = getattr(F, 'SHOT_CAST', {})
shots = [s for s in shots if not only or s[0] in only]
print('BOARD' + json.dumps(dict(shots=shots, frames=done, cast={n: cast.get(n) for n, _, _ in shots})))
"""


def _commit(root):
    import subprocess
    r = subprocess.run(['git', '-C', root, 'log', '-1', '--format=commit %h, %ad', '--date=format:%d %b %H:%M'],
                       capture_output=True, text=True)
    return r.stdout.strip() or 'the film now'


def board_rows(film, root=ROOT):
    """{shot: {field: text}} from story/FILM-board.txt: a block per shot ('shot NAME'), one 'field: text' line each."""
    p = os.path.join(root, 'story', f'{film.replace("_", "-")}-board.txt')
    rows = {}
    if os.path.exists(p):
        for name, text in _blocks(open(p).read(), r'^shot\s+(\S+)'):
            rows[name] = {k.strip().lower(): v.strip() for k, v in
                          (ln.split(':', 1) for ln in text.splitlines()[1:] if ':' in ln)}
    return rows


def board_frames(film, root=ROOT, tmp=None, only=()):
    """Runs the film's own code (at ROOT, or an older checkout) in its own process: its shots, cast and frames.
    only: just these shots (a re-staged shot drawn as built, lesson staging-stills)."""
    import json
    import subprocess
    import tempfile
    tmp = tmp or tempfile.mkdtemp(prefix='board-')
    r = subprocess.run([sys.executable, '-c', _GRAB, os.path.abspath(root), film.replace('-', '_'), tmp],
                       capture_output=True, text=True, timeout=3600,
                       env=dict(os.environ, BOARD_ONLY=','.join(only)))
    line = next((ln for ln in r.stdout.splitlines() if ln.startswith('BOARD')), None)
    if not line:
        raise RuntimeError(f'the film did not draw: {(r.stderr or r.stdout).strip().splitlines()[-1:]}')
    return json.loads(line[5:])


def board(film, out, root=ROOT, only=()):
    """The shot board: one row per shot, four frames (start, key beat, end, next shot's first) and its plan row.
    only: just these shots (a re-staged shot, before it moves: staging.py)."""
    from PIL import Image, ImageDraw, ImageFont
    font = lambda n: ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)      # noqa: E731
    got = board_frames(film, root, only=only)
    rows = board_rows(film, root)
    tw, th, gap = 216, 384, 10
    W = 40 + 4 * (tw + gap) + 30 + 640
    sx, sy = tw / 1080, th / 1920
    parts, missing = [], {}
    for n, a, b in got['shots']:
        im = Image.new('RGB', (W, th + 70), BG)
        d = ImageDraw.Draw(im)
        cast = got['cast'].get(n)
        d.text((20, 8), f'{n}  {a:.1f}-{b:.1f}s ({b - a:.1f}s)  cast: {", ".join(cast) if cast else "NOBODY"}',
               font=font(22), fill=(150, 30, 30) if not cast else (20, 20, 20))
        for i, (lab, t, f, err) in enumerate(got['frames'][n]):
            x, y = 20 + i * (tw + gap) + (30 if i == 3 else 0), 44
            if err or not os.path.exists(f):
                d.text((x, y + 40), f'not drawn: {err}'[:30], font=font(13), fill=(150, 30, 30))
                continue
            fr = Image.open(f).convert('RGB').resize((tw, th))
            fd = ImageDraw.Draw(fr)
            for k in (1, 2):                                            # thirds of the tall frame
                fd.line([(0, th * k / 3), (tw, th * k / 3)], fill=(255, 255, 255), width=1)
            x0, y0, x1, y1 = SAFE                                       # the app's safe area, dashed
            box = [(x0 * sx, y0 * sy), (x1 * sx, y0 * sy), (x1 * sx, y1 * sy), (x0 * sx, y1 * sy), (x0 * sx, y0 * sy)]
            for (p0, q0), (p1, q1) in zip(box, box[1:]):
                L = max(abs(p1 - p0), abs(q1 - q0))
                for s0 in range(0, int(L), 8):
                    e0 = min(L, s0 + 4)
                    fd.line([(p0 + (p1 - p0) * s0 / L, q0 + (q1 - q0) * s0 / L),
                             (p0 + (p1 - p0) * e0 / L, q0 + (q1 - q0) * e0 / L)], fill=(255, 40, 40), width=1)
            im.paste(fr, (x, y))
            d.text((x, y + th + 2), f'{lab} {t:.1f}s'[:30], font=font(13), fill=(60, 60, 60))
        if True:
            x = 20 + 4 * (tw + gap) + 50
            plan = rows.get(n, {})
            yy = 50
            for k in BOARD_FIELDS:
                v = plan.get(k)
                if not v:
                    missing.setdefault(n, []).append(k)
                txt = f'{k}: {v or "not planned"}'
                for ln in [txt[i:i + 46] for i in range(0, len(txt), 46)][:3]:
                    d.text((x, yy), ln, font=font(17), fill=(20, 20, 20) if v else (170, 40, 40))
                    yy += 22
                yy += 6
        parts.append(im)
    top = Image.new('RGB', (W, 80), BG)
    ImageDraw.Draw(top).text((20, 10), f'{film}: the shot board, {len(got["shots"])} shots: start, key beat, end, '
                             f'next shot (red dashes: the app-safe area; white: thirds)', font=font(24), fill=(20, 20, 20))
    ImageDraw.Draw(top).text((20, 44), f'drawn from {_commit(root)}, '
                             f'{datetime.date.today()}', font=font(18), fill=(80, 80, 80))
    parts.insert(0, top)
    sheet_im = Image.new('RGB', (W, sum(p.height for p in parts)), BG)
    y = 0
    for p in parts:
        sheet_im.paste(p, (0, y))
        y += p.height
    sheet_im.save(out, quality=82)
    _board_note(film, out, got, root)
    return out, got, missing


# ---------------------------------------------------------------------------------------------- the board's record
# Rule 11's gate (craft chat 8, 18 Nov). `board` leaves a note beside the picture (OUT.jpg.json: each shot, its cast,
# a digest of its four frames, the commit drawn from, how many move blocks the film had then); `sent FILM OUT.jpg
# --delivered --board` copies it into story/FILM-board-sent.txt with the time it reached Sam; the pre-flight's
# board_gate refuses a film whose shot is on no delivered board, whose shot has nobody in it, or whose first board
# reached Sam after its first move was written (the earliest commit adding a block to story/FILM-moves.txt, or a
# board drawn while the film already had blocks). Films begun before the rule keep the old "Composition sheet sent:"
# line. Not covered: moves written only in a film's code (not in its moves file).
RULE_COMMIT = 'fbfe83b9'                            # rule 11 rewritten (Sam's Y, 18 Nov): films older than it keep the old line
MOVE_BLOCK = r'^## *[a-z0-9_]+: *[a-z0-9_]+'


def _git(root, *args):
    import subprocess
    r = subprocess.run(['git', '-C', root, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def _story(film, kind, root=ROOT):
    return os.path.join(root, 'story', f'{film.replace("_", "-")}-{kind}')


def move_blocks(film, root=ROOT):
    p = _story(film, 'moves.txt', root)
    return len(re.findall(MOVE_BLOCK, open(p).read(), re.M)) if os.path.exists(p) else 0


def first_move(film, root=ROOT):
    """(epoch, where) of the film's first move: the earliest commit adding a block to its moves file; blocks not yet
    committed count from the file's last change. None: no moves yet."""
    p = _story(film, 'moves.txt', root)
    rel = os.path.relpath(p, root)
    got = _git(root, 'log', '--reverse', '--format=%at %h', '-G', MOVE_BLOCK, '--', rel)
    if got:
        t, h = got.splitlines()[0].split()
        return int(t), f'commit {h}'
    if move_blocks(film, root):
        return int(os.path.getmtime(p)), 'the moves file (not yet committed)'
    return None


def _board_note(film, out, got, root):
    """The note beside the picture, so `sent --board` records exactly what was drawn (never a redraw)."""
    import json
    import time
    digests = {}
    for n, _, _ in got['shots']:
        h = hashlib.sha1()
        for _lab, _t, f, err in got['frames'][n]:
            h.update(open(f, 'rb').read() if not err and os.path.exists(f) else err.encode())
        digests[n] = h.hexdigest()[:10]
    json.dump(dict(film=film, drawn=int(time.time()), commit=_git(root, 'rev-parse', '--short', 'HEAD') or 'none',
                   moves=move_blocks(film, root), shots=got['shots'], cast=got['cast'], digests=digests),
              open(out + '.json', 'w'))


def board_record_path(film, root=ROOT):
    return _story(film, 'board-sent.txt', root)


def board_record(film, root=ROOT):
    """[{delivered, drawn, commit, moves, file, shots: {name: (digest, cast)}}] for every board delivered, oldest first."""
    out = []
    p = board_record_path(film, root)
    if os.path.exists(p):
        for ln in open(p):
            f = ln.split()
            if ln.startswith('board '):
                kv = dict(x.split('=', 1) for x in f[2:] if '=' in x)
                out.append(dict(file=f[1], delivered=int(kv['delivered']), drawn=int(kv['drawn']),
                                commit=kv.get('commit'), moves=int(kv.get('moves', 0)), shots={}))
            elif ln.startswith('shot ') and out and len(f) >= 3:
                out[-1]['shots'][f[1]] = (f[2], [c for c in (f[3] if len(f) > 3 else '').split(',') if c])
    return out


def mark_board_sent(film, out, root=ROOT):
    """Records the board drawn into OUT as delivered now (its note must exist: draw it with `board` first)."""
    import json
    import time
    note = out + '.json'
    if not os.path.exists(note):
        raise SystemExit(f'NOT recorded: {out} has no board note ({note}); draw it with rough.py board {film} {out}')
    b = json.load(open(note))
    if b['film'].replace('_', '-') != film.replace('_', '-'):
        raise SystemExit(f'NOT recorded: {out} is the board of {b["film"]}, not {film}')
    now = int(time.time())
    p = board_record_path(film, root)
    new = not os.path.exists(p)
    with open(p, 'a') as f:
        if new:
            f.write('# The shot boards that reached Sam (rule 11; source/rough.py sent FILM OUT.jpg --delivered --board).\n'
                    '# board FILE delivered=EPOCH drawn=EPOCH commit=C moves=N (move blocks when drawn); '
                    'then one line per shot: shot NAME FRAMES-DIGEST CAST\n')
        f.write(f'board {os.path.basename(out)} delivered={now} drawn={b["drawn"]} commit={b["commit"]} '
                f'moves={b["moves"]} ({datetime.datetime.fromtimestamp(now):%d %b %H:%M})\n')
        for n, _a, _b in b['shots']:
            f.write(f'shot {n} {b["digests"][n]} {",".join(b["cast"].get(n) or []) or "-"}\n')
    return b


def _before_rule(film_mod, name, root):
    """A film begun before rule 11's board (its code already there at RULE_COMMIT, or its notes archived)."""
    src = getattr(film_mod, '__file__', '') or ''
    if src and os.path.abspath(src).startswith(os.path.abspath(root) + os.sep):
        if _git(root, 'cat-file', '-e', f'{RULE_COMMIT}:{os.path.relpath(src, root)}') is not None:
            return True
    return os.path.exists(os.path.join(root, 'notes', 'archive', f'{name}.md'))


def board_gate(film_mod, name, notes_text='', root=ROOT):
    """Rule 11's refusals for the pre-flight (empty: go)."""
    send = (f'python3 source/rough.py board {name} OUT.jpg, send it with SendUserFile, then '
            f'python3 source/rough.py sent {name} OUT.jpg --delivered --board')
    boards = board_record(name, root)
    if not boards:
        if _before_rule(film_mod, name, root):              # begun before the board: the old line still counts
            if re.search(r'^\s*[-*]?\s*\**Composition sheet sent\**:\**[ \t]*[^\s(*]', notes_text, re.M | re.I):
                return []
            return ['no record of the composition sheet being sent (rule 11, a film begun before the shot board): '
                    'add "Composition sheet sent: DATE, FILE" to the notes, or ' + send]
        return [f'no shot board has reached Sam (rule 11): {send}']
    out = []
    shots = [n for n, a, b in film_mod.SHOTS if float(b) > float(a)]
    seen = set().union(*(b['shots'] for b in boards))
    gone = [n for n in shots if n not in seen]
    if gone:
        out.append(f'{len(gone)} shot(s) on no delivered board (rule 11): {", ".join(gone[:8])}'
                   f'{" ..." if len(gone) > 8 else ""}: draw the board again, send it, then `sent --board`')
    cast = getattr(film_mod, 'SHOT_CAST', None)
    if cast is None:
        out.append('the film has no SHOT_CAST (rule 11): the board must show who is in every shot')
    else:
        empty = [n for n in shots if not cast.get(n)]
        if empty:
            out.append(f'{len(empty)} shot(s) with nobody in SHOT_CAST (rule 11): {", ".join(empty[:8])}')
    first = boards[0]
    when = datetime.datetime.fromtimestamp(first['delivered']).strftime('%d %b %H:%M')
    if first['moves']:
        out.append(f'the first board ({first["file"]}, {when}) was drawn after {first["moves"]} move block(s) were '
                   'written (rule 11: every shot on the board before any movement is built)')
    else:
        fm = first_move(name, root)
        if fm and fm[0] < first['delivered']:
            out.append(f'the first move ({fm[1]}, {datetime.datetime.fromtimestamp(fm[0]):%d %b %H:%M}) came before '
                       f'the first board reached Sam ({when}) (rule 11: the board before any movement)')
    if not _before_rule(film_mod, name, root):          # lesson staging-stills: a held framing, or a framing note
        import staging
        out += [f for f in staging.gate(name, shots, shots, root, notes_text=notes_text or (None if root == ROOT else ''))
                if ' has never been on ' not in f]          # (those are counted above)
    return out


def _films():
    import acting
    return acting.FILMS


def main(argv):
    if len(argv) < 2 or argv[0] not in ('sheet', 'sent', 'check', 'board'):
        print(__doc__.split('Map:')[0])
        return 2
    film = argv[1]
    if argv[0] == 'board':
        root = argv[argv.index('--root') + 1] if '--root' in argv else ROOT
        only = tuple(argv[argv.index('--shots') + 1].split(',')) if '--shots' in argv else ()
        out, got, missing = board(film, argv[2], root, only)
        print(f'{out}: {len(got["shots"])} shots; plan rows missing fields on {len(missing)} shot(s)'
              + ''.join(f'\n  {n}: {", ".join(m)}' for n, m in list(missing.items())[:3])
              + (f'\n  ... and {len(missing) - 3} more' if len(missing) > 3 else '')
              + (f'\n  nobody in: {", ".join(n for n, _, _ in got["shots"] if not got["cast"].get(n))}'
                 if any(not got['cast'].get(n) for n, _, _ in got['shots']) else '')
              + (f'\nafter SendUserFile has delivered it: python3 source/rough.py sent {film} {out} --delivered --board'
                 if root == ROOT else ''))
        return 0
    if argv[0] == 'check':
        f = gate_faults(film)
        print('\n'.join(f) if f else f'{film}: everything built has been on a rough')
        return 1 if f else 0
    if argv[0] == 'sent':
        if '--delivered' not in argv:
            print('NOT recorded: add --delivered once SendUserFile has delivered the sheet (a sheet is "sent" only when it arrived).')
            return 1
        rest = [a for a in argv[2:] if not a.startswith('--')]
        if '--board' in argv:
            if not rest:
                print('NOT recorded: name the board picture: rough.py sent FILM OUT.jpg --delivered --board')
                return 1
            b = mark_board_sent(film, rest[0])
            print(f'{film}: the board of {len(b["shots"])} shots recorded as seen '
                  f'({os.path.relpath(board_record_path(film), ROOT)})')
            import subprocess
            import ledger
            if ledger.load(film).get('stages'):            # the plan's "board" stage ends here (rule 24)
                r = subprocess.run([sys.executable, os.path.join(HERE, 'ledger.py'), 'stage', film, 'board'],
                                   capture_output=True, text=True)
                print((r.stdout + r.stderr).strip())
            return 0
        n = mark_sent(film, rest[0] if rest else '')
        print(f'{film}: {n} things recorded as seen on a rough ({os.path.relpath(record_path(film), ROOT)})')
        return 0
    out, todo = sheet(film, argv[2], '--all' in argv, '--draft' in argv)
    print(f'{out}: {len(todo)} thing(s) ({sum(k == "person" for k, _, _ in todo)} people, '
          f'{sum(k == "place" for k, _, _ in todo)} places, {sum(k == "move" for k, _, _ in todo)} moves)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
