#!/usr/bin/env python3
"""MAP (startup fixes change 4, Sam's Y, 16 Nov): no CLAUDE.md sentence is ever lost.

Text may leave CLAUDE.md only word for word: to the rulebook (guides/film-quality-rules.md) or a pack
(guides/job-packs.md). A dated tag such as "(Sam, 13 Nov)" may leave its sentence only if the rulebook's
"Dates moved from CLAUDE.md" table holds a row: the sentence's first words | the tag, word for word.

  split(text) ........ CLAUDE.md -> sentences (bullets, headers, '. ' ends; whitespace and ** ignored)
  lost(old, files) ... the old sentences found in none of the new files (after moved tags are taken out)
  tag_rows(text) ..... the rulebook's moved-tag rows: [(first words, tag)]
  faults() ........... every CLAUDE.md change since this check began (each commit, then the working copy)

  python3 source/sentences.py check            the faults; exit 1 if any (handover.py end runs it too)
  python3 source/sentences.py lost OLD.md      one old CLAUDE.md against today's files

A later rewording (only with Sam's Y on its own proposal) must add its own allowance here; none exists yet.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ['CLAUDE.md', 'guides/film-quality-rules.md', 'guides/job-packs.md']
TAGS_HEADER = 'Dates moved from CLAUDE.md'


def norm(s):
    s = s.replace('**', '')
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s+([.,;:)])', r'\1', s)
    s = re.sub(r'[;,]\s*\)', ')', s)
    s = re.sub(r'\(\s*\)', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def _blocks(text):
    out, cur = [], []
    for ln in text.splitlines():
        start = re.match(r'\s*(#+\s|-\s|\|)', ln) or not ln.strip()
        if start and cur:
            out.append(' '.join(cur)); cur = []
        head = re.match(r'\s*#+\s', ln)
        ln = re.sub(r'^\s*(#+|-)\s+', '', ln)
        if ln.strip():
            cur.append(ln.strip())
        if head and cur:                    # a header is a block of its own
            out.append(' '.join(cur)); cur = []
    if cur:
        out.append(' '.join(cur))
    return out


def split(text):
    out = []
    for b in _blocks(text):
        for s in re.sub(r'([.!?](?:\*\*)?)\s+', r'\1\n', b).split('\n'):
            s = norm(s)
            if len(s) > 2:
                out.append(s)
    return out


def corpus(text):
    return ' ' + ' '.join(norm(b) for b in _blocks(text)) + ' '


def tag_rows(rulebook):
    rows, on = [], False
    for ln in rulebook.splitlines():
        if ln.startswith('#'):
            on = TAGS_HEADER in ln
        elif on and ln.startswith('|') and not ln.startswith('|---'):
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if len(cells) >= 2 and cells[1] and not cells[0].startswith('CLAUDE.md rule'):
                rows.append((norm(cells[0]), norm(cells[1])))
    return rows


SAM_REWORDED = {   # sentences Sam himself rewrote (his words now stand in their place): never "lost"
    'Every stage aims at three things (Sam, 13 Nov)': 'Statement One (Sam, 22 Nov), top of CLAUDE.md, and "Every stage '
                                                     'aims at Statement One" in "Rules are permanent"',
    'Every stage aims at three things: high quality': 'the same, reworded again by Sam\'s 22 Nov Statement One',
    'Be honest about what I can do (Sam, 21 Nov)': 'Statement Two (Sam, 21 Nov), top of CLAUDE.md',
    'Choose views the drawing can carry.': 'Seeing like Sam 4, now bold-split by Sam\'s 21 Nov wording',
}


def lost(old, files):
    """old: the old CLAUDE.md text; files: {path: new text}. Returns the old sentences not found word for word
    (a sentence Sam himself rewrote, SAM_REWORDED, is not lost: his new words stand in its place)."""
    body = ''.join(corpus(t) for t in files.values())
    rows = tag_rows(files.get('guides/film-quality-rules.md', ''))
    miss = []
    for s in split(old):
        if s in body or any(s.startswith(k) for k in SAM_REWORDED):
            continue
        t = s
        for words, tag in rows:
            if words in t and tag in t:
                t = norm(t.replace(tag, ''))
        if t == s or t not in body:
            miss.append(s)
    return miss


def _git(*a):
    r = subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def _at(rev):
    return {f: _git('show', f'{rev}:{f}') or '' for f in FILES}


def faults():
    out = []
    since = (_git('log', '--format=%H', '--diff-filter=A', '-1', '--', 'source/sentences.py') or '').strip()
    revs = (_git('log', '--format=%H', f'{since}..HEAD', '--', 'CLAUDE.md') or '').split() if since else []
    for c in reversed(revs):
        old = _git('show', f'{c}^:CLAUDE.md')
        if old is None:           # shallow copy: the parent is not here; GitHub's copy was checked when it was made
            continue
        out += [f'SENTENCE lost from CLAUDE.md in {c[:8]}: "{s[:110]}"' for s in lost(old, _at(c))]
    head = _git('show', 'HEAD:CLAUDE.md')
    if head is not None:
        now = {f: open(os.path.join(ROOT, f), encoding='utf-8').read() for f in FILES}
        out += [f'SENTENCE lost from CLAUDE.md (not yet saved): "{s[:110]}"' for s in lost(head, now)]
    return [f + ' -> put it back, or move it word for word to the rulebook or a pack' for f in out]


def main(argv):
    if argv[:1] == ['check']:
        f = faults()
        for x in f:
            print(x)
        print('Checks: sentence check: ' + (f'{len(f)} CLAUDE.md sentences lost' if f else 'no CLAUDE.md sentence lost'))
        return 1 if f else 0
    if argv[:1] == ['lost'] and len(argv) > 1:
        now = {f: open(os.path.join(ROOT, f), encoding='utf-8').read() for f in FILES}
        m = lost(open(argv[1], encoding='utf-8').read(), now)
        for s in m:
            print('LOST:', s)
        print(f'{len(m)} lost')
        return 1 if m else 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
