#!/usr/bin/env python3
"""round: one note's fix, checked, clipped, pictured and saved in ONE command with ONE short printout
(rule 19, Job C 3, Sam 13 Nov: each step is one command with a short summary; a third fewer actions a chat).

    python3 source/round.py FILM T0 T1 -m "8: the whale knocks the helideck away" [--times 12.5 13 ...]
                            [--no-check] [--no-clip] [--no-sheet] [--no-save]

Make the fix (edit the film's code) first, then run this. In order, each step one line:
  check   the film's own checks (`FILM.py check`); a fault stops the run before anything is rendered
  clip    `FILM.py final source/data/FILM-clip-T0-T1.mp4 --small --span T0 T1` (needs no Sam yes; send it to him)
  sheet   `sheet.py FILM` at T0, the middle and T1 (or --times), for looking once (rule 48)
  save    commit the changed tracked files (drafts in source/data stay off) with the -m words, push the chat's branch
Every step's whole output goes to source/data/FILM-round.log; the printout keeps only the outcome and the faults.
A failed step stops the run and says which; rerun with the done steps switched off (--no-...).
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(HERE, 'data')


def _run(cmd, log, timeout=None):
    t = time.time()
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    out = (p.stdout or '') + (p.stderr or '')
    with open(log, 'a') as fh:
        fh.write(f'\n$ {" ".join(cmd)}\n{out}')
    return p.returncode, out, time.time() - t


def _faults(out, n=3):
    """The lines that name a fault (rule 19: only the faults are read)."""
    keys = ('fault', 'FAULT', 'Error', 'error', 'REFUSED', 'check:', 'Checks:', 'Traceback')
    hits = [x.strip() for x in out.splitlines() if any(k in x for k in keys)]
    return hits[-n:] or [x.strip() for x in out.strip().splitlines()[-n:]]


def plan(film, t0, t1, times=None, skip=()):
    """The commands, in order, as (step, command); a step in skip is left out."""
    clip = os.path.join('source', 'data', f'{film}-clip-{t0:g}-{t1:g}.mp4')
    times = times or [t0, round((t0 + t1) / 2, 2), t1]
    steps = [('check', ['python3', f'source/{film}.py', 'check']),
             ('clip', ['python3', f'source/{film}.py', 'final', clip, '--small', '--span', f'{t0:g}', f'{t1:g}']),
             ('sheet', ['python3', 'source/sheet.py', film] + [f'{x:g}' for x in times]
              + ['--out', os.path.join('source', 'data', f'{film}-round-sheet.jpg')]),
             ('save', None)]
    return [(s, c) for s, c in steps if s not in skip], clip


def save(msg, log):
    """Commit the tracked changes (never new files in source/data: drafts stay off GitHub) and push this branch."""
    _run(['git', 'add', '-u'], log)
    code, out, _ = _run(['git', 'commit', '-q', '-m', msg], log)
    if code and 'nothing to commit' in out:
        return 0, 'nothing changed to save'
    if code:
        return code, _faults(out)[0]
    br = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=ROOT, capture_output=True,
                        text=True).stdout.strip()
    for wait in (0, 2, 4, 8, 16):
        time.sleep(wait)
        code, out, _ = _run(['git', 'push', '-q', '-u', 'origin', br], log)
        if not code:
            return 0, f'saved and pushed to {br}'
    return code, 'push failed: ' + _faults(out)[0]


def main(a):
    if len(a) < 3 or '-m' not in a:
        sys.exit(__doc__)
    film, t0, t1 = a[0], float(a[1]), float(a[2])
    msg = a[a.index('-m') + 1]
    times = None
    if '--times' in a:
        times = []
        for x in a[a.index('--times') + 1:]:
            if x.startswith('-'):
                break
            times.append(float(x))
    skip = {x[5:] for x in a if x.startswith('--no-')}
    os.makedirs(DATA, exist_ok=True)
    log = os.path.join(DATA, f'{film}-round.log')
    open(log, 'w').close()
    steps, clip = plan(film, t0, t1, times, skip)
    lines, start = [], time.time()
    for step, cmd in steps:
        if step == 'save':
            code, what = save(msg, log)
        else:
            code, out, took = _run(cmd, log)
            if code:
                what = '; '.join(_faults(out))
            elif step == 'clip':
                what = f'{clip} ({os.path.getsize(os.path.join(ROOT, clip)) / 1e6:.1f} MB, {took:.0f} s)'
            elif step == 'sheet':
                what = os.path.join('source', 'data', f'{film}-round-sheet.jpg')
            else:
                what = _faults(out, 1)[0] if out.strip() else 'clean'
        lines.append(f'{step:6s} {"ok  " if not code else "FAIL"} {what[:220]}')
        if code:
            lines.append(f'round stopped at {step}; full output: {log}')
            break
    print(f'round ({film}, {t0:g}-{t1:g} s, {time.time() - start:.0f} s):')
    print('\n'.join(lines))
    return 1 if any(' FAIL ' in x for x in lines) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
