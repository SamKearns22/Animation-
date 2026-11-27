#!/usr/bin/env python3
"""planning: the paperwork asks, one list, asked once (check audit B4, Sam's Y 26 Nov).

Why: "the film has no PLAN", "no BENCHMARK", "no audits", "no acting list", "no Rehearsal clips sent line", "no MAP"
printed on every Open Wounds run (4 to 10 runs each) and were never answered. Each is a planning question, not a
drawing fault. They now become rows of the film's brief checklist ("Planning: ..."), written there the first time
they are seen; the pre-flight and quick check then print ONE line (how many are still unanswered) instead of each ask
on every run. A row is answered by writing in its "done?" cell ("done", or "none: why"); an answered ask is never
printed again. Where an ask used to stop pre-flight (rules 74 and 8 on films from the 10 Nov template), its
unanswered row still stops it, as one line.

MAP
  ASKS 30 | key_of 45 | rows 60 | route 85 | main 125

    python3 source/planning.py FILM        the film's planning rows and which are unanswered
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HEAD = re.compile(r'^## The brief as a checklist.*$', re.M)

# key: (what a check line says, the row's words in the brief checklist)
ASKS = {
    'plan': ('the film has no PLAN', 'Planning: the PLAN of the world in metres, a camera per shot (rule 1)'),
    'benchmark': ('the film has no BENCHMARK', 'Planning: the BENCHMARK, 8-10 things per place beside the references '
                  '(rule 3)'),
    'audits': ('the film has no audits', 'Planning: the general audit (each body alone; start from the template)'),
    'acting': ('no acting list in the notes', 'Planning: the acting list, one row per line (rule 74)'),
    'rehearsal': ('no "Rehearsal clips sent', 'Planning: the riskiest moves as 2-3 s clips, a "Rehearsal clips sent:" '
                  'line (rule 8)'),
    'map': ('has no MAP in its first lines', "Planning: the film's code opens with its MAP (rule 61)"),
}


def key_of(line):
    """The planning ask a check line is, or None."""
    for k, (said, _) in ASKS.items():
        if said in str(line):
            return k
    return None


def _section(text):
    m = HEAD.search(text)
    if not m:
        return None
    end = re.search(r'^## ', text[m.end():], re.M)
    return m.end(), (m.end() + end.start() if end else len(text))


def rows(text):
    """{key: answer} for every planning row in the brief checklist ('' = unanswered)."""
    sec = _section(text)
    out = {}
    if not sec:
        return out
    for ln in text[sec[0]:sec[1]].splitlines():
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if len(cells) >= 3 and cells[1].startswith('Planning: '):
            k = next((k for k, (_, words) in ASKS.items() if cells[1] == words), None)
            if k:
                out[k] = cells[-1]
    return out


def add_rows(path, keys):
    """Write the missing planning rows at the end of the brief checklist table (once)."""
    text = open(path).read()
    sec = _section(text)
    have = rows(text)
    new = [k for k in keys if k not in have]
    if not sec or not new:
        return []
    body = text[sec[0]:sec[1]]
    lines = body.rstrip('\n').split('\n')
    last = max((i for i, ln in enumerate(lines) if ln.strip().startswith('|')), default=len(lines) - 1)
    n = sum(1 for ln in lines if re.match(r'^\|\s*\d+\s*\|', ln))
    add = [f'| {n + 1 + i} | {ASKS[k][1]} |  |' for i, k in enumerate(new)]
    lines[last + 1:last + 1] = add
    rest = text[sec[1]:]
    open(path, 'w').write(text[:sec[0]] + '\n'.join(lines) + ('\n\n' if rest else '\n') + rest)
    return new


def route(lines, path, stopping=()):
    """(the lines left, the one planning line or None, the stop lines). Each planning ask in `lines` becomes a row of
    the brief checklist (written the first time) and is taken out; one line says how many rows are unanswered.
    stopping: keys whose unanswered row stops pre-flight (rules 74 and 8 on the 10 Nov template's films)."""
    keep, asks = [], []
    for x in lines:
        k = key_of(x)
        (asks if k else keep).append(k or x)
    if not asks or not path or not os.path.exists(path):
        return list(lines), None, []
    add_rows(path, asks)
    have = rows(open(path).read())
    open_ = [k for k in dict.fromkeys(asks) if not have.get(k)]
    if not open_:
        return keep, None, []
    line = (f'planning list: {len(open_)} unanswered row(s) in the notes\' brief checklist ('
            + ', '.join(open_) + '): write "done" or "none: why" in each "done?" cell; asked once, not every run')
    stops = [line] if any(k in stopping for k in open_) else []
    return keep, (None if stops else line), stops


def main():
    film = sys.argv[1].replace('_', '-')
    path = os.path.join(ROOT, 'notes', f'{film}.md')
    if not os.path.exists(path):
        sys.exit(f'no notes file {path}')
    have = rows(open(path).read())
    if not have:
        print('planning list: no planning rows yet (they are written the first time a check asks)')
    for k, a in have.items():
        print(f'{k:10s} {a or "(unanswered)"}')


if __name__ == '__main__':
    main()
