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
  film names . `protest-tiers` and `protest_tiers` both work (code files use _, story files use -).

    python3 source/page.py FILM show "note words" [-n 40]   (a round's one look per note: the code it touches)
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
           'just still more less very then than when where should could would can has have had all any him she they'.split())


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


def _defs(path):
    """{start line: (end line, name)} for the file's top-level defs and classes (and methods inside classes)."""
    import ast
    out = {}
    for n in ast.walk(ast.parse(open(path, encoding='utf-8').read())):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            out[n.lineno] = (n.end_lineno, n.name)
    return out


def show(film, note, budget=40):
    """A note's words -> the code to read: [(header, [(line number, text)])], at most ~budget code lines in all.
    The best hit gets the lion's share: the whole def if it fits, else its first lines plus every line holding the
    note's words (one line either side). Runners-up get their first lines; the rest are listed as FILE:LINE."""
    want = _words(note)
    hits = find(film, note, 12)
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
        rescored.append((score * 2 + body, where, what, path, ln))
    rescored.sort(key=lambda h: -h[0])
    out, left = [], budget
    for i, (score, where, what, path, ln) in enumerate(rescored):
        if left <= 2:
            out.append((f'also {where}  {what}', []))
            continue
        lines = open(path, encoding='utf-8').read().splitlines()
        if not path.endswith('.py'):
            take = list(range(max(1, ln), min(len(lines), ln + 2) + 1))
        else:
            end = _defs(path).get(ln, (ln + 10, ''))[0]
            span = list(range(ln, end + 1))
            room = left - 6 if i == 0 else min(8, left)
            if len(span) <= room:
                take = span
            else:
                keep = set(span[:min(6, room)])
                for k in span:
                    if want & _words(lines[k - 1].replace('_', ' ')):
                        keep |= {k - 1, k, k + 1}
                take = sorted(k for k in keep if ln <= k <= end)[:room]
        out.append((f'{where}  {what}', [(k, lines[k - 1]) for k in take]))
        left -= len(take)
    return out


def main(a):
    if not a or a[0] in ('-h', '--help'):
        print(__doc__); return 0
    if len(a) > 2 and a[1] == 'show':
        b = int(a[a.index('-n') + 1]) if '-n' in a else 40
        res = show(a[0], a[2], b)
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
