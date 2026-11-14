#!/usr/bin/env python3
"""critbench: the critic test bench (ranking item 3, overnight run 13-14 Nov). Replays a finished film's old pictures
to a critic helper with Sam's real notes on them as the answer key, so critics (Opus, Sonnet) and checklist lines are
scored on the same packs instead of on trust. Every key note a critic misses names its checklist line to improve.

MAP
  CASES ............ source/bench/CASE.json (committed): film, commit (the code as Sam saw it), panels, key, acting
  frames ........... renders each panel's time from a git worktree at that commit (cached, source/data/critbench/);
                     a panel may name its own "commit" (a second animatic of the same film in one pack: one critic
                     run covers both) and a "strip" of times (moments side by side, cropped alike: stillness and
                     moods over a line show, Sam's "too static" notes)
  make ............. one pack per critic, the same pictures and step files critique.py writes (cold look, then check)
  prompt ........... the one-line Agent call for that critic (kind `critic`, model named)
  acting ........... Sam's face and body notes (14 Nov: "acting must be covered"), scored apart from the checklist
                     key: the same item form, caught by any FAULT on its panels with its words
  match ............ a key item is CAUGHT by a FAULT on one of its panels that names one of its lines or its words
                     ("words_only": true: its words alone, where a line is too broad, e.g. S6 or P7 on a busy panel)
  score ............ caught / key and acting caught / acting, misses (with the line to improve), extras (faults not in the key: Claude rules
                     each real or false in the case file's "extras_ruled"), can't-tells; one row in notes/critic-bench.tsv
  table ............ the scores so far, critic by critic

    python3 source/critbench.py make CASE [MODEL ...]      (default models: opus sonnet; opus-r2 sonnet-r2 ... repeats)
    python3 source/critbench.py prompt CASE MODEL
    python3 source/critbench.py score CASE MODEL [--cost PCT]
    python3 source/critbench.py table

CASE file: {"film": "blessed", "commit": "5c95b9e", "what": "...", "panels": [{"t": 2.46, "is": "...", "parts": "PS"}],
"key": [{"id": "k13", "note": 13, "panels": [2, 4], "lines": ["P12"], "words": "mouth", "said": "Sam's words"}]}.
Only notes a fresh eye could spot on a still go in the key (a fault, not a wish or a taste; motion notes need strips).
Switch rule (Sam, 14 Nov: "know definitively", not luck): three runs per critic per case; Sonnet becomes the critic only
if it matches Opus on the checklist key AND the acting key across all runs, with no more false extras; else split
(Sonnet for checklist faults, Opus for acting).
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
HEAD = 'date\tcase\tcritic\tcaught\tkey\tmissed\textras\tcant_tell\tcost_pct\tacting\tacting_key\tacting_missed\n'


def case(name):
    c = json.load(open(os.path.join(CASES, name + '.json')))
    c['name'] = name
    return c


def _frame_path(c, commit, t):
    """A rendered frame's file: the case's own commit by time alone (as before); another commit by commit and time."""
    out = os.path.join(DATA, c['name'], 'frames')
    return os.path.join(out, f"{t:06.2f}.jpg" if commit == c['commit'] else f"{commit}-{t:06.2f}.jpg")


def frames(c):
    """Each panel's picture as Sam saw it: rendered from a worktree at its commit (the panel's, else the case's;
    cached). A strip panel's entry is the list of its times' files."""
    os.makedirs(os.path.join(DATA, c['name'], 'frames'), exist_ok=True)
    need, paths = {}, []
    for p in c['panels']:
        com = p.get('commit', c['commit'])
        fs = [_frame_path(c, com, t) for t in (p['strip'] if p.get('strip') else [p['t']])]
        need.setdefault(com, []).extend(t for t, f in zip(p.get('strip') or [p['t']], fs) if not os.path.exists(f))
        paths.append(fs if p.get('strip') else fs[0])
    for com, ts in need.items():
        if not ts:
            continue
        wt = os.path.join(DATA, c['name'], 'tree' if com == c['commit'] else f'tree-{com}')
        if not os.path.exists(wt):
            subprocess.run(['git', '-C', ROOT, 'worktree', 'add', '-f', '--detach', wt, com], check=True,
                           capture_output=True)
        names = {t: _frame_path(c, com, t) for t in ts}
        code = (f"import {c['film']} as F\n"
                f"for t, f in {names!r}.items():\n"
                f"    im = (F.picture(t) if hasattr(F, 'picture') else F.frame_image(t)).convert('RGB')\n"
                f"    im.resize((1080, 1920)).save(f, quality=90)\n")
        subprocess.run([sys.executable, '-c', code], cwd=os.path.join(wt, 'source'), check=True)
    return paths


def _picture(path, p):
    """One panel's picture: a frame (cropped for a detail panel), or a strip's crops side by side, left to right."""
    from PIL import Image, ImageDraw
    if not isinstance(path, list):
        im = Image.open(path).convert('RGB')
        return im.crop(tuple(p['crop'])) if p.get('crop') else im
    ims = [Image.open(f).convert('RGB') for f in path]
    ims = [im.crop(tuple(p['crop'])) for im in ims] if p.get('crop') else ims
    w, h = ims[0].size
    out = Image.new('RGB', (len(ims) * w + 12 * (len(ims) - 1), h), (255, 255, 255))
    for k, im in enumerate(ims):
        out.paste(im, (k * (w + 12), 0))
        ImageDraw.Draw(out).text((k * (w + 12) + 6, 4), f"{p['strip'][k] - p['strip'][0]:+.1f}s", fill=(255, 255, 0))
    return out


class _Shots:
    def __init__(self, shots):
        self.SHOTS = shots


def make(c, models=('opus', 'sonnet')):
    import critique as C
    from PIL import Image
    paths = frames(c)
    specs = [dict(p, img=f if isinstance(f, str) else f[0]) for p, f in zip(c['panels'], paths)]
    pics = [_picture(f, p) for f, p in zip(paths, c['panels'])]          # a detail panel, or a strip
    parts = ''.join(sorted(set(''.join(p.get('parts', '') for p in specs)), key=C.PARTS.index))
    film = _Shots(c.get('shots', []))
    made = []
    for m in models:
        out = os.path.join(DATA, c['name'], m)
        if os.path.exists(os.path.join(out, 'result.md')):
            sys.exit(f'critbench: {out} already has an answer; score it, or delete the folder to run again')
        os.makedirs(out, exist_ok=True)
        looks = C.look_sheets(pics, specs, out)
        checks = C.check_sheet(pics, specs, out) + C.set_sheet(pics, specs, out)
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
    """model may carry a run number for the repeat test: 'sonnet-r2' is Sonnet's second run (its own folder)."""
    out = os.path.join(DATA, c['name'], model)
    return (f'Agent (critic, model {model.split("-r")[0]}, a NEW one): "Read {out}/step1.md and follow it exactly; '
            f'write only into {out}."')


def match(key, faults):
    """{key id: the fault that caught it}. A fault catches an item on one of its panels when it names one of the
    item's lines or its words (a regex) appear in the fault's words."""
    got = {}
    for k in key:
        for f in faults:
            if f['kind'] != 'FAULT' or not set(f['panels']) & set(k['panels']):
                continue
            if (not k.get('words_only') and set(f['lids']) & set(k['lines'])) or re.search(k['words'], f['words'], re.I):
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
    act = match(c.get('acting', []), faults)
    amiss = [k for k in c.get('acting', []) if k['id'] not in act]
    used = {id(f) for f in got.values()} | {id(f) for f in act.values()}
    extras = [f for f in faults if id(f) not in used]
    miss = [k for k in c['key'] if k['id'] not in got]
    lines = C.lines()
    rep = [f"critbench {c['name']} / {model}: caught {len(got)} of {len(c['key'])}; {len(extras)} extra fault(s); "
           f"{len(cant)} can't tell; acting caught {len(act)} of {len(c.get('acting', []))}" + (f"; answer not whole: {'; '.join(why)}" if why else '')]
    for k in miss:
        lid = k['lines'][0]
        rep.append(f"  MISS {k['id']} (note {k['note']}, panel {C._span(k['panels'])}, line {lid}): \"{k['said']}\" "
                   f"-> improve {lid}: {lines.get(lid, ('', '?'))[1][:110]}")
    for k in amiss:
        rep.append(f"  ACTING MISS {k['id']} (note {k['note']}, panel {C._span(k['panels'])}): \"{k['said']}\"")
    for f in extras:
        rep.append(f"  EXTRA panel {C._span(f['panels'])} {' '.join(f['lids'])}: {f['words'][:120]}")
    if write:
        new = not os.path.exists(TABLE)
        with open(TABLE, 'a') as t:
            if new:
                t.write(HEAD)
            t.write(f"{date.today()}\t{c['name']}\t{model}\t{len(got)}\t{len(c['key'])}\t"
                    f"{' '.join(k['id'] for k in miss) or '-'}\t{len(extras)}\t{len(cant)}\t"
                    f"{cost if cost is not None else '?'}\t{len(act)}\t{len(c.get('acting', []))}\t"
                    f"{' '.join(k['id'] for k in amiss) or '-'}\n")
    return got, miss, extras, cant, '\n'.join(rep)


def table():
    if not os.path.exists(TABLE):
        return 'critbench: no scores yet'
    rows = [ln.split('\t') for ln in open(TABLE).read().splitlines()[1:] if ln.strip()]
    out = []
    for crit in sorted({r[2] for r in rows}):
        mine = [r for r in rows if r[2] == crit]
        cg, ky = sum(int(r[3]) for r in mine), sum(int(r[4]) for r in mine)
        out.append(f'{crit}: caught {cg} of {ky} key items over {len(mine)} run(s), '
                   f'{sum(int(r[6]) for r in mine)} extras')
    for cs in sorted({r[1] for r in rows}):                  # the repeat test: each critic's spread on one case
        for crit in sorted({r[2] for r in rows if r[1] == cs}):
            runs = [r for r in rows if r[1] == cs and r[2] == crit]
            if len(runs) > 1:
                ck = [int(r[3]) for r in runs]
                ac = [int(r[9]) for r in runs if len(r) > 10]
                out.append(f'  {cs} / {crit}: {len(runs)} runs, checklist {min(ck)}-{max(ck)} of {runs[0][4]}'
                           + (f', acting {min(ac)}-{max(ac)} of {runs[0][10]}' if ac else ''))
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
