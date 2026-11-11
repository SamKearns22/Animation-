#!/usr/bin/env python3
"""Film ledger (Job F, Sam 9 Nov): what each film cost and what went wrong, kept on GitHub, not in the chat.

MAP
  files ............ notes/ledger/FILM.json (the record), FILM.md (written from it), FILM/round-N.txt (evidence)
  round ............ start a round: later check results are saved into that round's file automatically
  record() ......... called by report.summarise: every check's full result (clean ones too) goes into the round file
  save / note ...... the check sheet's text, false alarms, "could not test", into the round file
  log .............. at every handover: this chat's cost (from the cost watch), model, stage, notes, repeated notes
  auto ............. the Stop hook (Sam, 11 Nov: "automate this"): after every turn, this chat's running cost goes
                     into the ledger of the film or job it worked on (found from the files it touched); committed and
                     pushed when it has moved by 0.25% of a week, so the record survives the chat
  estimate ......... the film's estimate (% of a week), for estimate versus actual; --stages gives the plan's stages
                     and shares (Job M, rule 24): "cast 2, sets 2.5, moves 3, animatic1 1, round 1.5, final 0.5"
  stage ............ marks a stage done at its end (the first open one of that name; one not in the plan is added
                     with no share) and prints the forecast line for Sam's first line
  forecast() ....... spent / (share of the plan done) x estimate; mid-stage, never less than spent so far plus the
                     stages after the open one at the rate so far. auto stops the chat once per quarter step when it
                     passes the estimate by a quarter (only when it says more than the spend alarm already has)
  stage_alarm() .... rule 24 (Sam, 11 Nov): auto stops the chat when the stage being worked on reaches its share, and
                     at each half share beyond (before: only when the whole film was a quarter over its estimate)
  audit ............ the 10-line end-of-film audit, also written into FILM.md
  kept() ........... rule 37 (Job L): sounds and references not yet on GitHub, at every log (handover) and `kept`

    python3 source/ledger.py estimate FILM 10 --stages "cast 3, sets 2, moves 2, animatic1 1, round 1.5, final 0.5"
    python3 source/ledger.py stage FILM cast          (at the end of each stage)
    python3 source/ledger.py round FILM 2
    python3 source/ledger.py save FILM SHEET.txt          (or: save FILM - "text", a line straight in)
    python3 source/ledger.py note FILM "false alarm: handcheck 12.3 s, the hand is behind the mug on purpose"
    python3 source/ledger.py log FILM --stage "round 2 notes" --notes 9 --repeat "arm join at 4 s | shoulder test"
    python3 source/ledger.py audit FILM
    python3 source/ledger.py kept                       (also run by every log)

A chat is tagged by its transcript; logging the same chat again replaces its row, so nothing is counted twice.
"""
import argparse, glob, json, os, re, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'notes', 'ledger')
CURRENT = os.path.join(DIR, '.current')      # "FILM ROUND": where check results go


def _paths(film):
    return os.path.join(DIR, film + '.json'), os.path.join(DIR, film + '.md'), os.path.join(DIR, film)


def load(film):
    j, _, _ = _paths(film)
    try:
        return json.load(open(j))
    except FileNotFoundError:
        return {'film': film, 'estimate': None, 'chats': [], 'checks': {}}


def store(d):
    j, md, _ = _paths(d['film'])
    os.makedirs(DIR, exist_ok=True)
    json.dump(d, open(j, 'w'), indent=1)
    open(md, 'w').write(render(d))


def current():
    try:
        film, rnd = open(CURRENT).read().split()
        return film, int(rnd)
    except Exception:
        return None, None


def round_file(film, rnd):
    _, _, folder = _paths(film)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f'round-{rnd}.txt')


def append(film, rnd, text):
    with open(round_file(film, rnd), 'a') as f:
        f.write(text.rstrip('\n') + '\n\n')


def record(title, faults, notes=()):
    """Called by report.summarise for every check. Saves the full list into the round file and counts each check's
    faults by kind, so the audit can say which checks caught things and which never fired. Never breaks a check."""
    try:
        film, rnd = current()
        if not film:
            return
        import report
        faults = list(faults)
        body = f'== {title} ({date.today()}): ' + (f'{len(faults)} fault(s)' if faults else 'clean') + '\n'
        body += ''.join(f'- {x}\n' for x in faults) + ''.join(f'  {n}\n' for n in notes)
        append(film, rnd, body)
        d = load(film)
        name = re.sub(r'\s*\(.*\)$', '', title)
        c = d['checks'].setdefault(name, {'runs': 0, 'faults': 0, 'kinds': {}})
        c['runs'] += 1
        c['faults'] += len(faults)
        for x in faults:
            k = report.kind(x)
            c['kinds'][k] = c['kinds'].get(k, 0) + 1
        store(d)
    except Exception as e:
        print(f'(ledger: not saved: {e})')


def chat_cost():
    """This chat's id, cost (% of a week) and model, from the cost watch."""
    sys.path.insert(0, os.path.join(ROOT, '.claude', 'hooks'))
    import costwatch
    files = glob.glob(os.path.expanduser('~/.claude/projects/**/*.jsonl'), recursive=True)
    path = max(files, key=os.path.getmtime)
    st, _ = costwatch.read_usage(path)
    _, pct = costwatch.level(st)
    return os.path.basename(path)[:8], round(pct, 2), costwatch.fam(st['model'])


SKIP = {'archive', 'next-jobs', '_template', 'sheets', 'ledger'}


def film_of(transcript):
    """The film or job this chat worked on: the notes/NAME.md (or source/NAME*.py with a notes file) its own tool
    calls named most."""
    names = {os.path.splitext(f)[0] for f in os.listdir(os.path.join(ROOT, 'notes')) if f.endswith('.md')} - SKIP
    count = {}
    for raw in open(transcript, encoding='utf-8', errors='replace'):
        if '"tool_use"' not in raw:
            continue
        for m in re.finditer(r'(?:notes|source)/([A-Za-z0-9_-]+)\.(?:md|py)', raw):
            n = m.group(1)
            n = n if n in names else n.split('_')[0]
            if n in names:
                count[n] = count.get(n, 0) + 1
    return max(count, key=count.get) if count else None


def auto(transcript):
    """Stop hook: this chat's running cost into its film's ledger (one row per chat, replaced as it grows); committed
    and pushed to the chat's branch when it moved by 0.25% of a week or the chat is new to the ledger."""
    import subprocess
    film = film_of(transcript)
    if not film:
        return
    sys.path.insert(0, os.path.join(ROOT, '.claude', 'hooks'))
    import costwatch
    st, _ = costwatch.read_usage(transcript)
    _, pct = costwatch.level(st)
    chat, cost, model = os.path.basename(transcript)[:8], round(pct, 2), costwatch.fam(st['model'])
    d = load(film)
    old = next((c for c in d['chats'] if c['chat'] == chat), None)
    if old and abs(old['cost'] - cost) < 0.25:
        return
    row = dict(old or {'date': str(date.today()), 'chat': chat, 'stage': 'auto', 'round': None, 'notes': 0,
                       'repeats': []}, model=model, cost=cost)
    if old:
        d['chats'][d['chats'].index(old)] = row
    else:
        d['chats'].append(row)
    alarm = None
    spent, est = totals(d)[0], d.get('estimate')
    if est:                                       # Sam, 11 Nov: Remakes ran to 45% on a 14.5% estimate and nothing
        step = int((spent / est - 1) / 0.25) + 1 if spent >= est else 0      # caught it: an alarm at the estimate
        if step > d.get('alarm', 0):                                        # and at every quarter over it, once each
            d['alarm'] = step
            alarm = (f'COST ALARM (ledger): {film} has spent {spent}% of a week against its estimate of {est}% '
                     f'({spent / est:.0%}). Stop this work now. Tell Sam in the first line of your reply, with what '
                     f'is left to do and your estimate for it, and ask Y/N whether to go on. Do not go on before his Y.')
    stop = stage_alarm(d)                         # each marks its own step, so none repeats on the next reply
    fore = forecast_alarm(d)
    alarm = alarm or (stop + (' ' + forecast_line(d) if fore else '') if stop else fore)
    store(d)
    if alarm:
        print(json.dumps({'decision': 'block', 'reason': alarm}))
    if any(os.path.exists(os.path.join(ROOT, '.git', x)) for x in ('MERGE_HEAD', 'rebase-merge', 'rebase-apply')):
        return                                    # mid-merge: the chat's own next commit carries it

    def git(*a):
        return subprocess.run(['git', '-C', ROOT] + list(a), capture_output=True, text=True, timeout=60)
    j, md, _ = _paths(film)
    git('add', j, md)
    if git('commit', '-q', '-m', f'Ledger: {film}, chat {chat} at {cost}% of a week (automatic)', '--', j,
           md).returncode == 0 and git('push', '-q', 'origin', 'HEAD').returncode != 0:
        br = git('rev-parse', '--abbrev-ref', 'HEAD').stdout.strip()      # another chat pushed first: merge its
        if git('pull', '-q', '--no-rebase', 'origin', br).returncode == 0:  # work (git refuses if it would touch
            git('push', '-q', 'origin', 'HEAD')                              # this chat's unsaved files)
        elif os.path.exists(os.path.join(ROOT, '.git', 'MERGE_HEAD')):
            git('merge', '--abort')                                          # a clash: leave it to the chat


def parse_stages(text):
    """'cast 2, sets 2.5, round 1.5' -> [{'name': 'cast', 'pct': 2.0, 'done': None}, ...]"""
    out = []
    for part in filter(None, (x.strip() for x in text.split(','))):
        m = re.fullmatch(r'(.+?)\s+([0-9.]+)', part)
        if not m:
            sys.exit(f'ledger: stage "{part}" needs a name and a share, e.g. "sets 2.5"')
        out.append({'name': m.group(1).strip(), 'pct': float(m.group(2)), 'done': None})
    return out


def mark_stage(d, name):
    """The first open planned stage of that name is done, at today's spend; a stage not in the plan is added, done,
    with no share (so an unplanned round pushes the forecast up, as it should)."""
    spent = totals(d)[0]
    st = d.setdefault('stages', [])
    s = next((x for x in st if x['name'] == name and x['done'] is None), None)
    if s is None:
        s = {'name': name, 'pct': 0.0, 'done': None, 'unplanned': True}
        last = max([i for i, x in enumerate(st) if x['done'] is not None], default=-1)
        st.insert(last + 1, s)
    s['done'] = {'date': str(date.today()), 'spent': spent}
    return s


def forecast(d):
    """(spent, planned so far in % of a week, forecast in % of a week), or None without an estimate and stages."""
    st, est = d.get('stages') or [], d.get('estimate')
    plan = sum(x['pct'] for x in st)
    if not est or not plan:
        return None
    spent = totals(d)[0]
    done = [x for x in st if x['done'] is not None]
    f_done = sum(x['pct'] for x in done) / plan
    at_mark = max((x['done']['spent'] for x in done), default=0.0)
    rate = at_mark / (f_done * est) if f_done else 1.0           # cost per planned % so far (1 before any stage ends)
    open_ = [x for x in st if x['done'] is None]
    after = sum(x['pct'] for x in open_[1:]) / plan * est       # the stages after the open one
    fc = max(at_mark / f_done if f_done else 0.0, spent + after * rate)
    return spent, round(f_done * est, 2), round(fc, 1)


def forecast_line(d):
    f = forecast(d)
    if not f:
        return None
    return f'Spent {f[0]:g}% of the {f[1]:g}% planned so far; at this rate the film lands at {f[2]:g}%.'


def forecast_alarm(d):
    """Rule 24: the forecast passes the estimate by a quarter: once per quarter step, and only when it says more
    than the spend alarm (at the estimate and each quarter over) already has. Returns the message or None."""
    f, est = forecast(d), d.get('estimate')
    if not f or f[2] < est * 1.25:
        return None
    step = int((f[2] / est - 1) / 0.25)
    if step <= max(d.get('forecast_alarm', 0), d.get('alarm', 0) - 1):
        return None
    d['forecast_alarm'] = step
    left = ', '.join(f"{x['name']} {x['pct']:g}" for x in d['stages'] if x['done'] is None) or 'nothing planned'
    return (f"FORECAST ALARM (ledger, rule 24): {d['film']}: {forecast_line(d)} The estimate is {est}%, and this is "
            f"{f[2] / est:.0%} of it. Stop this work now. First line to Sam: that forecast line, what is left "
            f"({left}), and a cheaper way that keeps the quality; ask Y/N. Do not go on before his Y.")


def open_stage(d):
    """(index, the stage being worked on, its share in % of a week, spent in it so far): the first planned stage not
    done after the last one done. None without an estimate and stages, or with nothing planned left."""
    st, est = d.get('stages') or [], d.get('estimate')
    plan = sum(x['pct'] for x in st)
    if not est or not plan:
        return None
    last = max((i for i, x in enumerate(st) if x['done'] is not None), default=-1)
    i = next((i for i in range(last + 1, len(st)) if st[i]['pct'] > 0), None)
    if i is None:
        return None
    at_mark = max((x['done']['spent'] for x in st if x['done'] is not None), default=0.0)
    return i, st[i], round(st[i]['pct'] / plan * est, 2), round(totals(d)[0] - at_mark, 2)


def stage_alarm(d):
    """Rule 24: the stage being worked on has reached its share: once at the share and once at each half share beyond.
    Returns the message or None."""
    o = open_stage(d)
    if not o or o[3] < o[2]:
        return None
    i, s, share, spent = o
    step = int((spent / share - 1) / 0.5) + 1
    seen = d.setdefault('stage_alarm', {})
    if step <= seen.get(f"{i}:{s['name']}", 0):
        return None
    seen[f"{i}:{s['name']}"] = step
    left = ', '.join(f"{x['name']} {x['pct']:g}" for x in d['stages'][i + 1:] if x['done'] is None) or 'nothing planned'
    return (f"STAGE STOP (ledger, rule 24): {d['film']}: the '{s['name']}' stage has spent {spent:g}% of a week against "
            f"its share of {share:g}%. If that stage is in fact finished, run `ledger.py stage {d['film']} {s['name']}` "
            f"and carry on. Otherwise stop this work now. First line to Sam: that figure, what exists, what is left "
            f"of this stage, and the cheapest way on that keeps the quality; ask Y/N. The stages after it ({left}) "
            f"keep their shares: do not spend them here. Do not go on before his Y.")


def totals(d):
    spent = round(sum(c['cost'] for c in d['chats']), 2)
    rounds = max([c['round'] for c in d['chats'] if c['round']] + [current()[1] or 0 if current()[0] == d['film'] else 0])
    notes = sum(c['notes'] for c in d['chats'])
    reps = [r for c in d['chats'] for r in c['repeats']]
    return spent, rounds, notes, reps


def render(d):
    spent, rounds, notes, reps = totals(d)
    est = d['estimate']
    out = [f"# Ledger: {d['film']}", '',
           'Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). '
           'Each round\'s check results and check sheet text are in the folder of the same name.', '',
           f"**Estimate {est if est is not None else '?'}% of a week; spent {spent}%"
           + (f' ({spent - est:+.2f})' if est is not None else '') + f"; {len(d['chats'])} chats, {rounds} rounds, "
           f"{notes} notes, {len(reps)} repeated.**", '',
           ]
    if d.get('stages'):
        out += [f'**Forecast: {forecast_line(d)}**', '', '| stage | planned % | done | spent at its end |',
                '|---|---|---|---|']
        out += [f"| {x['name']}{' (unplanned)' if x.get('unplanned') else ''} | {x['pct']:g} | "
                f"{x['done']['date'] if x['done'] else ''} | {x['done']['spent'] if x['done'] else ''} |"
                for x in d['stages']]
        out += ['']
    out += ['| date | chat | model | stage | round | cost % | notes | repeated |', '|---|---|---|---|---|---|---|---|']
    out += [f"| {c['date']} | {c['chat']} | {c['model']} | {c['stage']} | {c['round'] or ''} | {c['cost']} | "
            f"{c['notes']} | {len(c['repeats'])} |" for c in d['chats']]
    if reps:
        out += ['', '## Repeated notes (what would have caught them)']
        out += [f'- {r}' for r in reps]
    if d['checks']:
        out += ['', '## Checks (runs, faults, by kind)']
        for n, c in sorted(d['checks'].items()):
            kinds = ', '.join(f'{k} {v}' for k, v in sorted(c['kinds'].items(), key=lambda kv: -kv[1]))
            out.append(f"- {n}: {c['runs']} runs, {c['faults']} faults" + (f' ({kinds})' if kinds else ''))
    if d.get('audit'):
        out += ['', '## Audit (end of film)'] + d['audit']
    return '\n'.join(out) + '\n'


def audit(d):
    spent, rounds, notes, reps = totals(d)
    est = d['estimate']
    caught = sorted(((c['faults'], n) for n, c in d['checks'].items() if c['faults']), reverse=True)
    silent = sorted(n for n, c in d['checks'].items() if not c['faults'])
    falses = unable = 0
    for f in glob.glob(os.path.join(_paths(d['film'])[2], 'round-*.txt')):
        t = open(f).read().lower()
        falses += t.count('false alarm')
        unable += t.count('could not test')
    over = '' if est is None else (' (over: name what ran over)' if spent > est else ' (within)')
    models = {}
    for c in d['chats']:
        models[c['model']] = round(models.get(c['model'], 0) + c['cost'], 2)
    lines = [
        f"1. Cost: estimate {est if est is not None else '?'}%, spent {spent}% of a week{over}.",
        f"2. Chats {len(d['chats'])}, rounds {rounds}; by model: " + ', '.join(f'{m} {v}%' for m, v in models.items()) + '.',
        f"3. Sam's notes {notes}; repeated {len(reps)}" + (f' ({100 * len(reps) // notes}%)' if notes else '') + '.',
        '4. Repeated: ' + ('; '.join(r.split(' | ')[0] for r in reps[:4]) or 'none') + '.',
        '5. Would have caught them: ' + ('; '.join(r.split(' | ')[1] for r in reps if ' | ' in r)[:300] or 'not given') + '.',
        '6. Checks that caught things: ' + (', '.join(f'{n} {k}' for k, n in caught[:6]) or 'none') + '.',
        '7. Checks that ran and never fired: ' + (', '.join(silent) or 'none') + '.',
        f'8. False alarms {falses}; could not test {unable} (from the round files).',
        '9. By-hand rules: read the check sheet text in the round files; name any that never caught anything.',
        '10. Proposal for Sam (one line, a rule replaced or a check added): ',
    ]
    return lines



KEEP_DIRS = ('source/audio', 'music', 'references', 'refs', 'sounds')   # rule 37: these go on GitHub
BIG_MB = 10


def kept():
    """Rule 37 (Job L; was by hand): every sound and reference file goes on GitHub; one over about BIG_MB stays off
    and is named in the handover's first line. Returns (to add, too big): files git does not hold, in KEEP_DIRS."""
    import subprocess
    dirs = [d for d in KEEP_DIRS if os.path.isdir(os.path.join(ROOT, d))]
    if not dirs:
        return [], []
    out = subprocess.run(['git', 'status', '--porcelain', '--ignored', '--untracked-files=all', '--', *dirs],
                         cwd=ROOT, capture_output=True, text=True).stdout
    add, big = [], []
    for ln in out.splitlines():
        if ln[:2] not in ('??', '!!'):
            continue
        path = ln[3:].strip().strip('"')
        full = os.path.join(ROOT, path)
        if not os.path.isfile(full) or os.path.basename(path).startswith('.') or path.endswith('.pyc'):
            continue
        mb = os.path.getsize(full) / 1e6
        (big if mb > BIG_MB else add).append((path, mb))
    return add, big


def kept_lines():
    add, big = kept()
    out = [f'NOT ON GITHUB (rule 37): {p} ({mb:.1f} MB): git add it (or -f if ignored) and push' for p, mb in add]
    out += [f'STAYS OFF (rule 37, over {BIG_MB} MB): {p} ({mb:.0f} MB): name it in the handover\'s first line'
            for p, mb in big]
    return out or ['rule 37: every sound and reference file is on GitHub']

def main():
    a = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    s = a.add_subparsers(dest='cmd', required=True)
    p = s.add_parser('estimate'); p.add_argument('film'); p.add_argument('pct', type=float)
    p.add_argument('--stages', help='"cast 2, sets 2.5, moves 3, animatic1 1, round 1.5, final 0.5"')
    p = s.add_parser('stage'); p.add_argument('film'); p.add_argument('name')
    p = s.add_parser('round'); p.add_argument('film'); p.add_argument('n', type=int)
    p = s.add_parser('save'); p.add_argument('film'); p.add_argument('path'); p.add_argument('text', nargs='?')
    p = s.add_parser('note'); p.add_argument('film'); p.add_argument('text')
    p = s.add_parser('log'); p.add_argument('film'); p.add_argument('--stage', default='')
    p.add_argument('--notes', type=int, default=0)
    p.add_argument('--repeat', action='append', default=[], help='"the note | what would have caught it"')
    p = s.add_parser('audit'); p.add_argument('film')
    s.add_parser('kept')
    s.add_parser('auto')
    o = a.parse_args()
    if o.cmd == 'kept':
        print('\n'.join(kept_lines()))
        return
    if o.cmd == 'auto':                           # the Stop hook: its JSON (with the transcript's path) on stdin
        try:
            auto(json.load(sys.stdin)['transcript_path'])
        except Exception as e:                    # never hold up a chat over the ledger
            print(f'ledger auto: {e}', file=sys.stderr)
        return
    d = load(o.film)
    film, rnd = current()
    rnd = rnd if film == o.film else None
    if o.cmd == 'estimate':
        d['estimate'] = o.pct
        if o.stages:
            old = {x['name']: x for x in d.get('stages', []) if x['done']}
            d['stages'] = parse_stages(o.stages)
            plan = sum(x['pct'] for x in d['stages'])
            print(f'ledger: {o.film}: estimate {o.pct}%, {len(d["stages"])} stages adding to {plan:g}%'
                  + (f' (the forecast scales them to {o.pct}%)' if abs(plan - o.pct) > 0.05 else ''))
            if old:
                print('ledger: stages already marked done are cleared; mark them again with: ledger.py stage')
    elif o.cmd == 'stage':
        try:                                      # this chat's cost first, so the stage's end is up to date
            chat, cost, model = chat_cost()
            row = next((c for c in d['chats'] if c['chat'] == chat), None)
            if row:
                row['cost'] = max(row['cost'], cost)
        except Exception:
            pass
        if not d.get('stages'):
            sys.exit(f'ledger: {o.film} has no stages; run: ledger.py estimate {o.film} PCT --stages "..."')
        s_ = mark_stage(d, o.name)
        print(f"ledger: {o.film}: stage '{o.name}' done" + (' (not in the plan: no share)' if s_.get('unplanned') else ''))
        print(forecast_line(d))
        msg = forecast_alarm(d)
        if msg:
            print(msg)
    elif o.cmd == 'round':
        os.makedirs(DIR, exist_ok=True)
        open(CURRENT, 'w').write(f'{o.film} {o.n}\n')
        append(o.film, o.n, f'#### Round {o.n} ({date.today()})')
        print(f'ledger: {o.film} round {o.n}; check results now go to {os.path.relpath(round_file(o.film, o.n), ROOT)}')
    elif o.cmd in ('save', 'note'):
        if not rnd:
            sys.exit(f'ledger: no round open for {o.film}; run: ledger.py round {o.film} N')
        if o.cmd == 'note':
            text = '-- note: ' + o.text
        elif o.path == '-':
            text = '== check sheet:\n' + (o.text or sys.stdin.read())
        else:
            text = f'== check sheet ({os.path.basename(o.path)}):\n' + open(o.path).read()
        append(o.film, rnd, text)
        print(f'ledger: saved to {os.path.relpath(round_file(o.film, rnd), ROOT)}')
    elif o.cmd == 'log':
        chat, cost, model = chat_cost()
        row = {'date': str(date.today()), 'chat': chat, 'model': model, 'stage': o.stage, 'round': rnd,
               'cost': cost, 'notes': o.notes, 'repeats': o.repeat}
        old = next((c for c in d['chats'] if c['chat'] == chat), None)
        if old:   # the same chat logged again: its cost is a running total, so replace, keeping earlier notes
            row['notes'] = max(o.notes, old['notes'])
            row['repeats'] = old['repeats'] + [r for r in o.repeat if r not in old['repeats']]
            row['stage'] = o.stage or old['stage']
            d['chats'][d['chats'].index(old)] = row
        else:
            d['chats'].append(row)
        spent, _, _, _ = totals(d)
        est = d['estimate']
        print(f'ledger: {o.film}: this chat {cost}% ({model}); film so far {spent}%'
              + (f' of {est}% estimated' + (' -- OVER: tell Sam in the first line' if spent > est else '')
                 if est is not None else ' (no estimate set)'))
        print('\n'.join(kept_lines()))           # rule 37: sounds and references on GitHub, checked at the handover
    elif o.cmd == 'audit':
        d['audit'] = audit(d)
        print('\n'.join(d['audit']))
    store(d)


if __name__ == '__main__':
    main()
