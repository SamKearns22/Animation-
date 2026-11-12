#!/usr/bin/env python3
"""report: every check prints a short summary; the full list goes to a file only when it is longer than the summary
(guides/film-quality-rules.md, rule 19). Why: Prepper Minister's checks printed hundreds of lines a run; reading them filled the chat (every line is
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
    for start, k in (('caption "', 'caption'), ('shot ', 'shot length')):
        if s.startswith(start):
            return k
    m = re.match(r'^([A-Za-z][\w ()/-]{0,40}?):\s*(?:([A-Z][A-Z ]{2,30}):)?', s)
    if not m:
        return 'other'
    k = m.group(1)
    k = re.sub(r'\s*\(.*\)$', '', k)
    return f'{k} {m.group(2)}' if m.group(2) else k


def summarise(title, faults, path=None, first=FIRST, notes=(), off=()):
    """Print the short summary. A file is written only when there are more faults than the summary shows (Sam, 2 Nov:
    he never reads it; the one line is enough). Returns the printed text. off: checks that did not run with Sam's yes
    (preflight's CHECKS_OFF): printed first, every time, and while there are any the summary never says 'clean'
    (system audit, 12 Nov)."""
    faults = list(faults)
    off = list(off)
    try:  # the film ledger keeps every round's full result, clean ones too (Job F, Sam 9 Nov)
        import ledger
        ledger.record(title, faults, notes)
    except ImportError:
        pass
    if path and len(faults) <= first and not off:
        path = None
    if path:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'w') as f:
            f.write(f'{title}: {len(faults)} fault(s)\n')
            f.write(''.join(f'- {x}\n' for x in off + faults))
            if notes:
                f.write('\n' + '\n'.join(notes) + '\n')
    counts = {}
    for x in faults:
        counts[kind(x)] = counts.get(kind(x), 0) + 1
    where = f' (full list: {path})' if path else ''
    if not faults and off:
        out = [f'{title}: no faults found, but {len(off)} check(s) did not run (Sam\'s yes):']
    elif not faults:
        out = [f'{title}: clean']
    else:
        top = ', '.join(f'{k} {n}' for k, n in sorted(counts.items(), key=lambda kv: -kv[1]))
        out = [f'{title}: {len(faults)} fault(s) -- {top}{where}']
        out += [' - ' + (x if len(x) <= WIDTH else x[:WIDTH - 3] + '...') for x in faults[:first]]
        if len(faults) > first:
            out.append(f'   ... and {len(faults) - first} more in the file named in the line above')
    if off:
        out[1:1] = [' - ' + (x if len(x) <= WIDTH else x[:WIDTH - 3] + '...') for x in off]
    text = '\n'.join(out)
    print(text)
    return text
