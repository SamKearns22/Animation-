#!/usr/bin/env python3
"""critbench: the critic test bench (ranking item 3, overnight run 13-14 Nov). Replays a finished film's old pictures
to a critic helper with Sam's real notes on them as the answer key, so critics (Opus, Sonnet) and checklist lines are
scored on the same packs instead of on trust. Every key note a critic misses names its checklist line to improve.

MAP
  CASES ............ source/bench/CASE.json (committed): film, commit (the code as Sam saw it), panels, key
  frames ........... renders each panel's time from a git worktree at that commit (cached, source/data/critbench/)
  make ............. one pack per critic, the same pictures and step files critique.py writes (cold look, then check)
  prompt ........... the one-line Agent call for that critic (kind `critic`, model named)
  match ............ a key item is CAUGHT by a FAULT on one of its panels that names one of its lines or its words
  score ............ caught / key, misses (with the line to improve), extras (faults not in the key: Claude rules
                     each real or false in the case file's "extras_ruled"), can't-tells; one row in notes/critic-bench.tsv
  table ............ the scores so far, critic by critic

    python3 source/critbench.py make CASE [MODEL ...]      (default models: opus sonnet)
    python3 source/critbench.py prompt CASE MODEL
    python3 source/critbench.py score CASE MODEL [--cost PCT]
    python3 source/critbench.py table

CASE file: {"film": "blessed", "commit": "5c95b9e", "what": "...", "panels": [{"t": 2.46, "is": "...", "parts": "PS"}],
"key": [{"id": "k13", "note": 13, "panels": [2, 4], "lines": ["P12"], "words": "mouth", "said": "Sam's words"}]}.
Only notes a fresh eye could spot on a still go in the key (a fault, not a wish or a taste; motion notes need strips).
Switch rule (ranking item 3): the critic moves to Sonnet only if Sonnet catches at least as many key items as Opus on
the same cases, with no more false extras.
"""
import json
import os
import re
import subprocess
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
CASES = os.path.join(HERE, 'bench')
DATA = os.path.join(HERE, 'data', 'critbench')
TABLE = os.path.join(ROOT, 'notes', 'critic-bench.tsv')
HEAD = 'date\tcase\tcritic\tcaught\tkey\tmissed\textras\tcant_tell\tcost_pct\n'


def case(name):
    c = json.load(open(os.path.join(CASES, name + '.json')))
    c['name'] = name
    return c


def frames(c):
    """Each panel's picture as Sam saw it: rendered from a worktree at the case's commit (cached by time)."""
    out = os.path.join(DATA, c['name'], 'frames')
    os.makedirs(out, exist_ok=True)
    paths = [os.path.join(out, f"{p['t']:06.2f}.jpg") for p in c['panels']]
    need = [p['t'] for p, f in zip(c['panels'], paths) if not os.path.exists(f)]
    if need:
        wt = os.path.join(DATA, c['name'], 'tree')
        if not os.path.exists(wt):
            subprocess.run(['git', '-C', ROOT, 'worktree', 'add', '-f', '--detach', wt, c['commit']], check=True,
                           capture_output=True)
        code = (f"import {c['film']} as F\n"
                f"for t in {need!r}:\n"
                f"    im = (F.picture(t) if hasattr(F, 'picture') else F.frame_image(t)).convert('RGB')\n"
                f"    im.resize((1080, 1920)).save({out!r} + '/%06.2f.jpg' % t, quality=90)\n")
        subprocess.run([sys.executable, '-c', code], cwd=os.path.join(wt, 'source'), check=True)
    return paths


class _Shots:
    def __init__(self, shots):
        self.SHOTS = shots


def make(c, models=('opus', 'sonnet')):
    import critique as C
    from PIL import Image
    paths = frames(c)
    specs = [dict(p, img=f) for p, f in zip(c['panels'], paths)]
    pics = [Image.open(f).convert('RGB') for f in paths]
    pics = [im.crop(tuple(p['crop'])) if p.get('crop') else im for im, p in zip(pics, specs)]   # a detail panel
    parts = ''.join(sorted(set(''.join(p.get('parts', '') for p in specs)), key=C.PARTS.index))
    film = _Shots(c.get('shots', []))
    made = []
    for m in models:
        out = os.path.join(DATA, c['name'], m)
        if os.path.exists(os.path.join(out, 'result.md')):
            sys.exit(f'critbench: {out} already has an answer; score it, or delete the folder to run again')
        os.makedirs(out, exist_ok=True)
        looks = C.look_sheets(pics, specs, out)
        checks = C.check_sheet(pics, specs, out)
        open(os.path.join(out, 'checklist.md'), 'w').write(C.checklist_for(parts))
        open(os.path.join(out, 'brief.md'), 'w').write(C.brief_md(film, specs, []))
        names = lambda ps: ' and '.join(os.path.basename(p) for p in ps)
        open(os.path.join(out, 'step1.md'), 'w').write(C.STEP1.format(opening=C.OPENING, looks=names(looks),
                                                                      n=len(specs)))
        open(os.path.join(out, 'step2.md'), 'w').write(C.STEP2.format(opening=C.OPENING, checks=names(checks),
                                                                      n=len(specs), extra='', notes_part=''))
        json.dump({'round': 0, 'stage': 'bench', 'panels': specs}, open(out + '.spec.json', 'w'), indent=1)
        made.append(out)
    return made


def prompt(c, model):
    out = os.path.join(DATA, c['name'], model)
    return (f'Agent (critic, model {model}, a NEW one): "Read {out}/step1.md and follow it exactly; '
            f'write only into {out}."')


def match(key, faults):
    """{key id: the fault that caught it}. A fault catches an item on one of its panels when it names one of the
    item's lines or its words (a regex) appear in the fault's words."""
    got = {}
    for k in key:
        for f in faults:
            if f['kind'] != 'FAULT' or not set(f['panels']) & set(k['panels']):
                continue
            if set(f['lids']) & set(k['lines']) or re.search(k['words'], f['words'], re.I):
                got[k['id']] = f
                break
    return got


def score(c, model, cost=None, write=True):
    import critique as C
    out = os.path.join(DATA, c['name'], model)
    why, r = C.check_answer(out)
    if r is None:
        sys.exit('critbench: ' + '; '.join(why))
    faults = [f for f in r['faults'] if f['kind'] == 'FAULT']
    cant = [f for f in r['faults'] if f['kind'] != 'FAULT']
    got = match(c['key'], faults)
    used = {id(f) for f in got.values()}
    extras = [f for f in faults if id(f) not in used]
    miss = [k for k in c['key'] if k['id'] not in got]
    lines = C.lines()
    rep = [f"critbench {c['name']} / {model}: caught {len(got)} of {len(c['key'])}; {len(extras)} extra fault(s); "
           f"{len(cant)} can't tell" + (f"; answer not whole: {'; '.join(why)}" if why else '')]
    for k in miss:
        lid = k['lines'][0]
        rep.append(f"  MISS {k['id']} (note {k['note']}, panel {C._span(k['panels'])}, line {lid}): \"{k['said']}\" "
                   f"-> improve {lid}: {lines.get(lid, ('', '?'))[1][:110]}")
    for f in extras:
        rep.append(f"  EXTRA panel {C._span(f['panels'])} {' '.join(f['lids'])}: {f['words'][:120]}")
    if write:
        new = not os.path.exists(TABLE)
        with open(TABLE, 'a') as t:
            if new:
                t.write(HEAD)
            t.write(f"{date.today()}\t{c['name']}\t{model}\t{len(got)}\t{len(c['key'])}\t"
                    f"{' '.join(k['id'] for k in miss) or '-'}\t{len(extras)}\t{len(cant)}\t"
                    f"{cost if cost is not None else '?'}\n")
    return got, miss, extras, cant, '\n'.join(rep)


def table():
    if not os.path.exists(TABLE):
        return 'critbench: no scores yet'
    rows = [ln.split('\t') for ln in open(TABLE).read().splitlines()[1:] if ln.strip()]
    out = []
    for crit in sorted({r[2] for r in rows}):
        mine = [r for r in rows if r[2] == crit]
        cg, ky = sum(int(r[3]) for r in mine), sum(int(r[4]) for r in mine)
        out.append(f'{crit}: caught {cg} of {ky} key items over {len(mine)} case(s), '
                   f'{sum(int(r[6]) for r in mine)} extras')
    return '\n'.join(out)


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == 'make':
        for out in make(case(a[1]), a[2:] or ('opus', 'sonnet')):
            print(out)
            print(prompt(case(a[1]), os.path.basename(out)))
    elif a[0] == 'prompt':
        print(prompt(case(a[1]), a[2]))
    elif a[0] == 'score':
        cost = a[a.index('--cost') + 1] if '--cost' in a else None
        print(score(case(a[1]), a[2], cost)[-1])
    elif a[0] == 'table':
        print(table())
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
