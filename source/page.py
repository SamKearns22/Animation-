#!/usr/bin/env python3
"""page: a notes round reads a page, not a film (ranking item 6, overnight chat 3, 14 Nov).

MAP
  build() .... story/FILM-page.md: each of the film's files (source/FILM*.py) with its size and its codemap (every
               def with its line and first docstring line); about a tenth of the code's words (Blessed: 6.7k tokens
               against ~60k). A round chat reads this page, then only the lines a note points to (rule 61).
  find() ..... a note's words against the page: the defs whose name or docstring hold most of them, best first, as
               FILE:LINE, so the chat opens 40 lines, not a file. Words of 3+ letters; plurals folded.
  tokens() ... rough size (characters / 4), printed so the saving is seen.

    python3 source/page.py FILM                  (writes story/FILM-page.md; prints its size against the code's)
    python3 source/page.py FILM find "the officer's arms clip the van" [-n 5]

Waits for items 4, 5, 7 (people, places, moves kits): then a person, place or move is a description line, and the page
carries those lines too, so most notes are answered by changing a line on the page itself.
"""
import glob, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def files(film):
    return sorted(f for f in glob.glob(os.path.join(HERE, f'{film}*.py')) if re.match(rf'{film}(_\w+)?\.py$', os.path.basename(f)))


def tokens(text):
    return len(text) // 4


def build(film):
    parts, code = [f'# {film}: the page a notes round reads (python3 source/page.py {film}; regenerate after any edit)\n',
                   'Read this, then only the lines a note points to (`page.py FILM find "note words"`).\n'], ''
    for f in files(film):
        src = open(f, encoding='utf-8').read()
        code += src
        m = subprocess.run([sys.executable, os.path.join(HERE, 'codemap.py'), f], capture_output=True, text=True).stdout
        parts.append(f'\n## {os.path.basename(f)} ({src.count(chr(10))} lines)\n' + '\n'.join(m.splitlines()[2:]))
    page = '\n'.join(parts) + '\n'
    out = os.path.join(ROOT, 'story', f'{film}-page.md')
    open(out, 'w', encoding='utf-8').write(page)
    return out, tokens(page), tokens(code)


def _words(s):
    return {w[:-1] if w.endswith('s') and len(w) > 4 else w for w in re.findall(r'[a-z]{3,}', s.lower())} - STOP


STOP = set('the and with for not but his her its are was one two too from that this what who into onto off out now '
           'just still more less very then than when where should could would can has have had all any him she they'.split())


def find(film, note, n=5):
    p = os.path.join(ROOT, 'story', f'{film}-page.md')
    if not os.path.exists(p):
        build(film)
    want, cur, hits = _words(note), '', []
    for ln in open(p, encoding='utf-8'):
        if ln.startswith('## '):
            cur = ln[3:].split()[0]
        m = re.match(r'- (\d+): (.*)', ln)
        if m and want:
            score = len(want & _words(m.group(2).replace('_', ' ')))
            if score:
                hits.append((score, f'{cur}:{m.group(1)}', m.group(2)[:100]))
    return sorted(hits, key=lambda h: -h[0])[:n]


def main(a):
    if not a or a[0] in ('-h', '--help'):
        print(__doc__); return 0
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
