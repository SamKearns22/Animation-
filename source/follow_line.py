#!/usr/bin/env python3
"""The follow line on the sign-off (rule 52, Sam 12 Nov): one line per film, taken in order from
story/follow-lines.md and ticked off with the film's name; the same film keeps its line on every later finish.

    python3 follow_line.py            what is left, and which film had which line
    follow_line.line_for(NAME)        the film's line (claims the next one the first time); SystemExit when used up
"""
import datetime
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIST = os.path.join(os.path.dirname(HERE), 'story', 'follow-lines.md')
ROW = re.compile(r'^- \[( |x)\] (.+?)(?: — (\S+) \(([^)]*)\))?$')


def path():
    return os.environ.get('FOLLOW_LINES', LIST)       # the kit tests use a copy, so they never use up a real line


def rows():
    """[(line number, ticked, text, film)] for every line in the list."""
    out = []
    with open(path(), encoding='utf-8') as f:
        for i, ln in enumerate(f.read().splitlines()):
            m = ROW.match(ln)
            if m:
                out.append((i, m.group(1) == 'x', m.group(2), m.group(3)))
    return out


def line_for(film):
    rs = rows()
    for _, ticked, text, who in rs:
        if ticked and who == film:
            return text
    free = [r for r in rs if not r[1]]
    if not free:
        sys.exit('finish REFUSED (rule 52): the follow lines in story/follow-lines.md are used up. Ask Sam for a new '
                 'batch (research/follow-cta-plan.md has the tricks and the ones already tried).')
    i, _, text, _ = free[0]
    with open(path(), encoding='utf-8') as f:
        lines = f.read().split('\n')
    lines[i] = f'- [x] {text} — {film} ({datetime.date.today():%d %b})'
    with open(path(), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    left = len(free) - 1
    print(f'follow line for {film}: "{text}" ({left} left)')
    if left <= 2:
        print(f'FOLLOW LINES: only {left} left: ask Sam for a new batch in this message')
    return text


if __name__ == '__main__':
    for _, ticked, text, who in rows():
        print(('x ' if ticked else '  ') + text + (f'  ({who})' if who else ''))
