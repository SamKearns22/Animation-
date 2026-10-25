#!/usr/bin/env python3
"""report: every check prints a short summary and writes its full list to a file (guides/film-quality-rules.md,
rule 19). Why: Prepper Minister's checks printed hundreds of lines a run; reading them filled the chat (every line is
read again at every step) and the one fault that mattered was easy to miss.

    report.summarise('pre-flight', faults, 'OUT_DIR/film-preflight.txt')
prints:  pre-flight: 14 fault(s) -- AUDIT PASSES THROUGH 7, plan 2, caption 1 ... (full list: OUT_DIR/film-preflight.txt)
         then the first FIRST faults, one line each, cut to WIDTH characters.
"""
import os
import re

FIRST, WIDTH = 6, 150


def kind(line):
    """A fault's kind, from how it starts: 'AUDIT: PASSES THROUGH: ...' -> 'AUDIT PASSES THROUGH'; ' 12.30 s: ...' ->
    'drawing'; 'plan: ...' -> 'plan'."""
    s = line.strip()
    if re.match(r'^-?\d+(\.\d+)?\s*s\b', s):
        return 'drawing'
    m = re.match(r'^([A-Za-z][\w ()/-]{0,40}?):\s*(?:([A-Z][A-Z ]{2,30}):)?', s)
    if not m:
        return 'other'
    k = m.group(1)
    k = re.sub(r'\s*\(.*\)$', '', k)
    return f'{k} {m.group(2)}' if m.group(2) else k


def summarise(title, faults, path=None, first=FIRST, notes=()):
    """Print the short summary; write every fault (and any notes) to `path`. Returns the printed text."""
    faults = list(faults)
    if path:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'w') as f:
            f.write(f'{title}: {len(faults)} fault(s)\n')
            f.write(''.join(f'- {x}\n' for x in faults))
            if notes:
                f.write('\n' + '\n'.join(notes) + '\n')
    counts = {}
    for x in faults:
        counts[kind(x)] = counts.get(kind(x), 0) + 1
    where = f' (full list: {path})' if path else ''
    if not faults:
        out = [f'{title}: clean{where}']
    else:
        top = ', '.join(f'{k} {n}' for k, n in sorted(counts.items(), key=lambda kv: -kv[1]))
        out = [f'{title}: {len(faults)} fault(s) -- {top}{where}']
        out += [' - ' + (x if len(x) <= WIDTH else x[:WIDTH - 3] + '...') for x in faults[:first]]
        if len(faults) > first:
            out.append(f'   ... and {len(faults) - first} more in the file')
    text = '\n'.join(out)
    print(text)
    return text
