#!/usr/bin/env python3
"""page: a notes round reads a page, not a film (ranking item 6, overnight chat 3, 14 Nov).

MAP
  build() .... story/FILM-page.md: each of the film's files (source/FILM*.py) with its size and its codemap (every
               def with its line and first docstring line); about a tenth of the code's words (Blessed: 6.7k tokens
               against ~60k). A round chat reads this page, then only the lines a note points to (rule 61).
  find() ..... a note's words against the page: the defs whose name or docstring hold most of them, best first, as
               FILE:LINE, so the chat opens 40 lines, not a file. Words of 3+ letters; plurals folded.
  tokens() ... rough size (characters / 4), printed so the saving is seen.
  show() ..... THE ONE STEP A ROUND TAKES PER NOTE (Sam's Y, 15 Nov; chats 29/31 spent a third of their steps on
               greps and sed ranges): the note's words -> the code itself, ~40 numbered lines: the best def whole
               (or its head plus every line holding the note's words), then the runners-up' heads, then FILE:LINE
               for the rest. Rebuilds a stale page first. Words also count inside a def's comments and names.
  shots() .... the film's shots and times (its SHOTS list), saved to story/FILM-shots.json beside the page (importing
               a big film takes ~20 s, so once per code change); shot names are also read from `shot ==`/`in` lines.
  --shot/--at  code-finder change 1 (Sam's 1, 16 Nov; notes/proposals/code-finder.md): the notes table's shot and time
               go in apart from the note's words. Defs named for the shot and lines naming it in quotes score as a
               second count, so a shot the code does not know ("cast sheet") cannot push out a word hit; an unknown
               shot falls to the shot playing at --at, else the nearest name, said so.
  change 2 ... (Sam's yes, 16 Nov) module-level tables and constants are found like defs; any def or table whose one
               line holds 2+ of the note's words joins; tables whose keys name the note's thing are lifted (chin ->
               chin_long); the best line is shown before the head. --who (the notes table's who column) lifts a def or
               table named for them. Files are parsed once and kept until they change (the replay: 52 s -> 0.5 s).
  log ........ every show call writes one line to notes/logs/FILM-show.log; handover.py end flags a chat that changed
               the film's code today with no show call.
  film names . `protest-tiers` and `protest_tiers` both work (code files use _, story files use -).

    python3 source/page.py FILM show "note words" --shot SHOT --at SECONDS --who WHO [-n 40]   (one look per note;
                                                  shot, time and who from the notes table; any may be left out)
    python3 source/page.py FILM                  (writes story/FILM-page.md; prints its size against the code's)
    python3 source/page.py FILM find "the officer's arms clip the van" [-n 5]

People (item 4, 14 Nov): the page carries each person's description from story/FILM-people.txt (people.lines), so
`find` points a note on a person at their block. Places (item 5, chat 5d): one line per piece from
story/FILM-places.txt (its line number, view, kind and name), so a note on a place finds its line. Moves (item 7, chat 7): one line per move from story/FILM-moves.txt
(shot, who, the line), so a note on a move finds its line.
"""
import glob, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def names(film):
    """(code name, story name): code files are protest_tiers*.py, story files protest-tiers-*.txt; either works."""
    return film.replace('-', '_'), film.replace('_', '-')


def files(film):
    film = names(film)[0]
    return sorted(f for f in glob.glob(os.path.join(HERE, f'{film}*.py')) if re.match(rf'{film}(_\w+)?\.py$', os.path.basename(f)))


def tokens(text):
    return len(text) // 4


def build(film):
    film = names(film)[1]
    parts, code = [f'# {film}: the page a notes round reads (python3 source/page.py {film}; regenerate after any edit)\n',
                   'Read this, then only the lines a note points to (`page.py FILM find "note words"`).\n'], ''
    for f in files(film):
        src = open(f, encoding='utf-8').read()
        code += src
        m = subprocess.run([sys.executable, os.path.join(HERE, 'codemap.py'), f], capture_output=True, text=True).stdout
        parts.append(f'\n## {os.path.basename(f)} ({src.count(chr(10))} lines)\n' + '\n'.join(m.splitlines()[2:]))
    import people                                 # item 4: each person's description lines (story/FILM-people.txt)
    ppl = people.lines(film)
    if ppl:
        parts.append(f'\n## {film}-people.txt ({len(ppl)} people; a note on a person changes their lines)\n' +
                     '\n'.join(f'- {n}: {_bare(txt)}' for n, txt in ppl))
    import places                                 # item 5: each place's pieces (story/FILM-places.txt), by line
    pcs = places.lines(film)
    if pcs:
        parts.append(f'\n## {film}-places.txt ({len(pcs)} pieces; a note on a place changes its line: open that line)\n' +
                     '\n'.join(_group(pcs, lambda t: tuple(t.split(': ', 1)) if ': ' in t else (t, ''))))
    import acting                                 # item 7: each shot's moves (story/FILM-moves.txt), by line
    mvs = acting.lines(film)
    if mvs:
        parts.append(f'\n## {film}-moves.txt ({len(mvs)} lines; a note on a move changes its line: open that line)\n' +
                     '\n'.join(_group([(n, acting.gist(t)) for n, t in mvs], lambda t: tuple(re.split(r' ?: ', t, maxsplit=1)) if re.search(r' ?: ', t) else (t, ''))))
    page = '\n'.join(parts) + '\n'
    out = os.path.join(ROOT, 'story', f'{film}-page.md')
    open(out, 'w', encoding='utf-8').write(page)
    return out, tokens(page), tokens(code)


def _group(rows, split):
    """Rows (line, text) as '### head' once, then '- line: rest' under it: the shared start of neighbouring lines is
    said once (find counts the head's words too). split(text) -> (head, rest)."""
    out, cur = [], None
    for n, txt in rows:
        h, r = split(txt)
        if h != cur:
            out.append(f'### {h}'); cur = h
        out.append(f'- {n}: {r}')
    return out


def _bare(txt):
    """A person's line without its numbers (sizes, colours, seeds): the words a note would name stay."""
    return re.sub(r'\s+', ' ', re.sub(r'[-+]?\d+\.?\d*(\s*m\b)?|\bseed:?|[|]', ' ', txt)).strip()


def _words(s):
    return {w[:-1] if w.endswith('s') and len(w) > 4 else w for w in re.findall(r'[a-z]{3,}', s.lower())} - STOP


STOP = set('the and with for not but his her its are was one two too from that this what who into onto off out now '
           'just still more less very then than when where should could would can has have had all any him she they '
           # bookkeeping words: the code's comments are full of "Sam, 13 Nov, note 18, chat 5", which never name a thing
           'sam oct nov dec jan note animatic chat brief round warning again'.split())


def page_path(film):
    return os.path.join(ROOT, 'story', f'{names(film)[1]}-page.md')


def stale(film):
    """True when the page is missing or older than any film file or story list it is made from."""
    p = page_path(film)
    if not os.path.exists(p):
        return True
    src = files(film) + glob.glob(os.path.join(ROOT, 'story', f'{names(film)[1]}-*.txt'))
    return any(os.path.getmtime(f) > os.path.getmtime(p) for f in src)


def find(film, note, n=5):
    p = page_path(film)
    if stale(film):
        build(film)
    want, cur, grp, hits = _words(note), '', '', []
    for ln in open(p, encoding='utf-8'):
        if ln.startswith('## '):
            cur, grp = ln[3:].split()[0], ''
        if ln.startswith('### '):
            grp = ln[4:]
        m = re.match(r'- (\d+): (.*)', ln)
        if m and want:
            score = len(want & _words((grp + ' ' + m.group(2)).replace('_', ' ')))
            if score:
                hits.append((score, f'{cur}:{m.group(1)}', (grp + ': ' + m.group(2))[:100]))
    return sorted(hits, key=lambda h: -h[0])[:n]


_CACHE = {}


def _parsed(path):
    """(lines, defs, blocks, line words) for a file, kept until it changes. blocks: the module-level statements outside
    any def (tables, constants, X['k'] = ...): {start: (end, name)} (code-finder change 2)."""
    import ast
    key = (path, os.path.getmtime(path))
    if key not in _CACHE:
        src = open(path, encoding='utf-8').read()
        tree, defs, blocks = ast.parse(src), {}, {}
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                defs[n.lineno] = (n.end_lineno, n.name)
        for n in tree.body:
            if isinstance(n, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                tg = n.targets[0] if isinstance(n, ast.Assign) else n.target
                blocks[n.lineno] = (n.end_lineno, ast.unparse(tg)[:40])
        lines = src.splitlines()
        _CACHE[key] = (lines, defs, blocks, [_words(x.replace('_', ' ')) for x in lines])
    return _CACHE[key]


def _defs(path):
    """{start line: (end line, name)} for the file's top-level defs and classes (and methods inside classes); with
    show.deep (change 2) the module-level tables and constants too."""
    _, defs, blocks, _ = _parsed(path)
    return {**blocks, **defs} if show.deep else defs


# a note asking for more or less of a thing ("chin still big") wants a number: the thing's setting in a table
SIZE = set('big bigger small smaller long longer short shorter wide wider narrow high higher low lower tall thin fat '
           'fast faster slow slower loud quiet dark darker light lighter bright close far large tiny huge'.split())


def _deep(film, want, seen):
    """Change 2: every def and table, scored by its best single line (the note's words met on one line: a comment
    naming the fix, a key like chin_long). A def or table joins the hits when one line holds 2+ of the note's words,
    or, when the note asks for more or less of something, a table's key holds one of its words. -> [(0, where, name)]."""
    size, things = (want & SIZE) or not show.gate, want - SIZE
    out = []
    for f in files(film):
        lines, defs, blocks, lw = _parsed(f)
        for ln, (end, name) in {**blocks, **defs}.items():
            where = f'{os.path.basename(f)}:{ln}'
            if where in seen:
                continue
            best = max((len(want & lw[k - 1]) for k in range(ln, min(end, len(lw)) + 1)), default=0)
            keyed = ln in blocks and size and any(things & _words(' '.join(re.findall(r'(\w+)\s*=', lines[k - 1])).replace('_', ' '))
                                                  for k in range(ln, end + 1))
            if best >= 2 or keyed:
                out.append((0, where, name))
    return out


def _line_score(path, ln, end, want):
    """The best single line's count of the note's words (change 2), and its line number."""
    lw = _parsed(path)[3]
    return max(((len(want & lw[k - 1]), k) for k in range(ln, min(end, len(lw)) + 1)), default=(0, ln))


def shots(film):
    """[(name, start, end)] from the film's SHOTS list, cached in story/FILM-shots.json until a code file is newer."""
    import json
    code, story = names(film)
    cache = os.path.join(ROOT, 'story', f'{story}-shots.json')
    fs = files(film)
    if os.path.exists(cache) and all(os.path.getmtime(f) <= os.path.getmtime(cache) for f in fs):
        return [tuple(x) for x in json.load(open(cache))]
    got = []
    try:
        r = subprocess.run([sys.executable, '-c', f'import json,{code} as m;print(json.dumps([[str(x[0]),float(x[1]),'
                            f'float(x[2])] for x in m.SHOTS]))'], cwd=HERE, capture_output=True, text=True, timeout=180)
        got = [tuple(x) for x in json.loads(r.stdout.strip().splitlines()[-1])]
    except Exception:
        pass
    names_ = {n for n, _, _ in got}
    for f in fs:                                  # shots only branched on (`shot in ('tvroom', 'push')`)
        for ln in open(f, encoding='utf-8'):
            m = re.search(r'\b(?:shot|s|shot_of\([^)]*\))\s*(?:==|in)\s*\(?([^:\n]*)', ln)
            if m:
                for n in re.findall(r"'([a-z][a-z0-9_]*)'", m.group(1)):
                    if n not in names_:
                        names_.add(n); got.append((n, -1.0, -1.0))
    if fs:
        json.dump(got, open(cache, 'w'))
    return got


def _shot_of(film, shot, at):
    """The code's shot names the notes table's shot text means: ([names], message or '')."""
    import difflib
    table = shots(film)
    known = [n for n, _, _ in table]
    named = [w for w in re.findall(r'[a-z][a-z0-9_]*', (shot or '').lower()) if w in known]
    if named:
        return list(dict.fromkeys(named)), ''
    if at is not None:
        playing = [n for n, a, b in table if a <= at < b]
        if playing:
            return playing, f'shot "{shot}" is not a name in the code; at {at:g} s the code plays {playing[0]}' if shot else ''
    near = difflib.get_close_matches((shot or '').lower().split(',')[0].strip(), known, 1, 0.5) if shot else []
    if near:
        return near, f'shot "{shot}" is not a name in the code; nearest name: {near[0]}'
    return [], (f'shot "{shot}" is not in the code (a new shot? add it beside the nearest like one)' if shot else '')


def _at(txt):
    """The notes table's time column ('49.45-53.6', '36.8', 'all', '-') -> one second or None."""
    nums = [float(x) for x in re.findall(r'\d+(?:\.\d+)?', txt or '')]
    return sum(nums[:2]) / len(nums[:2]) if nums else None


def _log(film, note, shot, at, res):
    from datetime import datetime
    d = os.path.join(ROOT, 'notes', 'logs')
    os.makedirs(d, exist_ok=True)
    top = res[0][0].split()[0] if res else '-'
    with open(os.path.join(d, f'{names(film)[1]}-show.log'), 'a', encoding='utf-8') as f:
        f.write(f'{datetime.now().isoformat(timespec="seconds")}\t{shot or "-"}\t{at if at is not None else "-"}\t'
                f'{top}\t{" ".join(note.split())[:100]}\t'
                f'{os.environ.get("CLAUDE_CODE_REMOTE_SESSION_ID", "local").split("_")[-1][-8:]}\n')   # finder-use: the chat


def show(film, note, budget=40, shot=None, at=None, who=None):
    """A note's words -> the code to read: [(header, [(line number, text)])], at most ~budget code lines in all.
    The best hit gets the lion's share: the whole def if it fits, else its first lines plus every line holding the
    note's words (one line either side). Runners-up get their first lines; the rest are listed as FILE:LINE.
    shot/at (the notes table's columns) add a second count: defs named for the shot, lines naming it in quotes."""
    want = _words(note)
    hits = find(film, note, 12)
    sh, msg = _shot_of(film, shot, at) if (shot or at is not None) else ([], '')
    show.msg = msg
    quoted = re.compile('|'.join(rf"""['"]{re.escape(n)}['"]""" for n in sh)) if sh else None
    if sh:                                        # the shot's own defs and the defs that branch on it join the hits
        seen = {w for _, w, _ in hits}
        for f in files(film):
            lines = open(f, encoding='utf-8').read().splitlines()
            for ln, (end, name) in _defs(f).items():
                own = any(name == n or name.startswith(n + '_') or name.endswith('_' + n) for n in sh)
                if (own or any(quoted.search(x) for x in lines[ln - 1:end])) and f'{os.path.basename(f)}:{ln}' not in seen:
                    hits.append((0, f'{os.path.basename(f)}:{ln}', name))
    if show.deep:                                 # change 2: tables, and defs whose one line names the note's thing
        hits += _deep(film, want, {w for _, w, _ in hits})
    # words inside a def's body (comments, names) break ties and lift a def whose docstring missed the note
    rescored = []
    for score, where, what in hits:
        f, ln = where.rsplit(':', 1)
        path, ln = os.path.join(HERE, f) if f.endswith('.py') else os.path.join(ROOT, 'story', f), int(ln)
        body = 0
        if f.endswith('.py'):
            end = _defs(path).get(ln, (ln, ''))[0]
            src = open(path, encoding='utf-8').read().splitlines()[ln - 1:end]
            body = len(want & _words(' '.join(src).replace('_', ' ')))
            if sh:                                # the shot's count: its own def 3, each line naming it 1 (at most 3)
                name = _defs(path).get(ln, (0, ''))[1]
                own = any(name == n or name.startswith(n + '_') or name.endswith('_' + n) for n in sh)
                body += 3 * own + min(3, sum(1 for x in src if quoted.search(x)))
            if show.deep and who:                 # the notes table's who column: a def or table named for them
                name = _defs(path).get(ln, (0, ''))[1].lower()
                body += 2 * len(_words(who) & _words(name.replace('_', ' ').replace("'", ' ')))
            if show.deep:                         # one line holding several of the note's words is the fix's line
                best = _line_score(path, ln, end, want)[0]
                body += 2 * best if best >= 2 else 0
                if ln in _parsed(path)[2] and (want & SIZE or not show.gate):       # a settings table a more-or-less note may want
                    keys = ' '.join(re.findall(r'(\w+)\s*=', ' '.join(src))).replace('_', ' ')
                    body += 3 * len((want - SIZE) & _words(keys))
        if score or body:
            rescored.append((score * 2 + body, where, what, path, ln))
    rescored.sort(key=lambda h: -h[0])
    out, left = [], budget
    for i, (score, where, what, path, ln) in enumerate(rescored):
        if left <= 2:                             # each def's header is a line too; at most 3 more as FILE:LINE
            if sum(1 for _, r in out if not r) < 3:
                out.append((f'also {where}  {what}', []))
            continue
        lines = open(path, encoding='utf-8').read().splitlines()
        if not path.endswith('.py'):
            take = list(range(max(1, ln), min(len(lines), ln + 2) + 1))
        else:
            end = _defs(path).get(ln, (ln + 10, ''))[0]
            span = list(range(ln, end + 1))
            room = min(show.first, left - 6) if i == 0 else min(show.rest, left)
            if len(span) <= room:
                take = span
            else:
                keep = set(span[:min(show.head, room)])
                for k in span:
                    if want & _words(lines[k - 1].replace('_', ' ')) or (quoted and quoted.search(lines[k - 1])):
                        keep |= {k - 1, k, k + 1}
                first = [k for k in span if quoted and quoted.search(lines[k - 1])][:max(1, room // 2)]
                must = {ln} | {k for k in first} | {k + 1 for k in first}     # the shot's own lines before the head
                if show.deep:                     # change 2: the def's best line (and its neighbours) before the head
                    b, k = _line_score(path, ln, end, want)
                    if b:
                        must |= {k - 1, k, k + 1} if b >= 2 or room > 5 else {k}
                rest = sorted(k for k in keep - must if ln <= k <= end)
                take = sorted((sorted(k for k in must if ln <= k <= end) + rest)[:room])
        out.append((f'{where}  {what}', [(k, lines[k - 1]) for k in take]))
        left -= len(take) + 1
    return out


show.first, show.rest, show.head = 16, 5, 3     # lines for the best def, each runner-up, a def's head
show.gate = False                                # True: tables lifted only for a more-or-less note (SIZE words);
                                                 # off since 16 Nov: same replay score without the hand list
show.deep = os.environ.get('FINDER_DEEP', '1') == '1'  # code-finder change 2 (Sam's yes, 16 Nov); FINDER_DEEP=0 turns it off


def main(a):
    if not a or a[0] in ('-h', '--help'):
        print(__doc__); return 0
    if len(a) > 2 and a[1] == 'show':
        b = int(a[a.index('-n') + 1]) if '-n' in a else 40
        shot = a[a.index('--shot') + 1] if '--shot' in a else None
        at = _at(a[a.index('--at') + 1]) if '--at' in a else None
        who = a[a.index('--who') + 1] if '--who' in a else None
        res = show(a[0], a[2], b, shot, at, who)
        _log(a[0], a[2], shot, at, res)
        if getattr(show, 'msg', ''):
            print('note: ' + show.msg)
        if not res:
            print('no code matches those words: try the thing on screen (who, what object), or `page.py FILM` and read the page')
        for head, rows in res:
            print(f'== {head}' if rows else f'   {head}')
            last = None
            for k, t in rows:
                if last is not None and k != last + 1:
                    print('      ...')
                print(f'{k:6}  {t}')
                last = k
        return 0
    if len(a) > 2 and a[1] == 'find':
        n = int(a[a.index('-n') + 1]) if '-n' in a else 5
        for s, where, what in find(a[0], a[2], n):
            print(f'{where}  ({s}) {what}')
        return 0
    out, pg, code = build(a[0])
    print(f'page: {os.path.relpath(out, ROOT)} ~{pg:,} tokens (the code ~{code:,}; {pg * 100 // max(code, 1)}%)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
