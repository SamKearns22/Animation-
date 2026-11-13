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


_TIME = re.compile(r'(?<![\w.])(-?\d+(?:\.\d+)?)(?:-(\d+(?:\.\d+)?))? ?s\b')   # '4.83 s', '3.1-3.5 s'


def group(faults, shots=()):
    """Rule 19 (Sam, 13 Nov: 137 faults and 356 repeat lines -> about 20): one line per fault, grouped by check, shot
    and who. Lines that differ only in their times, numbers or an extra's number (press0, press12; Journalist 4) are
    one fault: the first is kept, with its shot, time span and count. shots: the film's SHOTS, to name the shot."""
    groups = {}
    for x in faults:
        times = [float(v) for m in _TIME.findall(x) for v in m if v]
        t = times[0] if times else None
        shot = next((s[0] for s in shots if t is not None and s[1] <= t < s[2]), '')
        key = _TIME.sub('#s', x)
        key = re.sub(r'\b([A-Za-z_]+?)( ?)\d+\b', r'\1\2*', key)   # an extra's number, and any other number
        key = re.sub(r'\d+(\.\d+)?', '#', key)
        g = groups.setdefault((kind(x), shot, key), [x, [], 0])
        g[2] += 1
        g[1].extend(times)
    out = []
    for (_, shot, _), (first, ts, n) in sorted(groups.items(), key=lambda kv: (kv[0][0], min(kv[1][1] or [0]))):
        if n == 1:
            out.append(first)
            continue
        span = (f'{min(ts):.2f}-{max(ts):.2f} s' if ts and max(ts) > min(ts) else f'{ts[0]:.2f} s' if ts else '')
        where = ', '.join(v for v in ((f'shot {shot}' if shot else ''), span) if v)
        out.append(f'{first}  [{n} like it' + (f': {where}' if where else '') + ']')
    return out


def summarise(title, faults, path=None, first=FIRST, notes=()):
    """Print the short summary. A file is written only when there are more faults than the summary shows (Sam, 2 Nov:
    he never reads it; the one line is enough). Returns the printed text."""
    faults = list(faults)
    try:  # the film ledger keeps every round's full result, clean ones too (Job F, Sam 9 Nov)
        import ledger
        ledger.record(title, faults, notes)
    except ImportError:
        pass
    if path and len(faults) <= first:
        path = None
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
        out = [f'{title}: clean']
    else:
        top = ', '.join(f'{k} {n}' for k, n in sorted(counts.items(), key=lambda kv: -kv[1]))
        cnt = sum('COULD NOT TEST' in x.upper() for x in faults)   # rule 19 (Sam, 13 Nov): stops like a fault
        out = [f'{title}: {len(faults)} fault(s)' + (f', {cnt} of them COULD NOT TEST (stops the animatic like a '
               'fault)' if cnt else '') + f' -- {top}{where}']
        faults = sorted(faults, key=lambda x: 'COULD NOT TEST' not in x.upper())   # shown first
        out += [' - ' + (x if len(x) <= WIDTH else x[:WIDTH - 3] + '...') for x in faults[:first]]
        if len(faults) > first:
            out.append(f'   ... and {len(faults) - first} more in the file named in the line above')
    text = '\n'.join(out)
    print(text)
    return text
