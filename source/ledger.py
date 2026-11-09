#!/usr/bin/env python3
"""Film ledger (Job F, Sam 9 Nov): what each film cost and what went wrong, kept on GitHub, not in the chat.

MAP
  files ............ notes/ledger/FILM.json (the record), FILM.md (written from it), FILM/round-N.txt (evidence)
  round ............ start a round: later check results are saved into that round's file automatically
  record() ......... called by report.summarise: every check's full result (clean ones too) goes into the round file
  save / note ...... the check sheet's text, false alarms, "could not test", into the round file
  log .............. at every handover: this chat's cost (from the cost watch), model, stage, notes, repeated notes
  estimate ......... the film's estimate (% of a week), for estimate versus actual
  audit ............ the 10-line end-of-film audit, also written into FILM.md

    python3 source/ledger.py estimate FILM 10
    python3 source/ledger.py round FILM 2
    python3 source/ledger.py save FILM SHEET.txt          (or: save FILM - "text", a line straight in)
    python3 source/ledger.py note FILM "false alarm: handcheck 12.3 s, the hand is behind the mug on purpose"
    python3 source/ledger.py log FILM --stage "round 2 notes" --notes 9 --repeat "arm join at 4 s | shoulder test"
    python3 source/ledger.py audit FILM

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
           '| date | chat | model | stage | round | cost % | notes | repeated |', '|---|---|---|---|---|---|---|---|']
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


def main():
    a = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    s = a.add_subparsers(dest='cmd', required=True)
    p = s.add_parser('estimate'); p.add_argument('film'); p.add_argument('pct', type=float)
    p = s.add_parser('round'); p.add_argument('film'); p.add_argument('n', type=int)
    p = s.add_parser('save'); p.add_argument('film'); p.add_argument('path'); p.add_argument('text', nargs='?')
    p = s.add_parser('note'); p.add_argument('film'); p.add_argument('text')
    p = s.add_parser('log'); p.add_argument('film'); p.add_argument('--stage', default='')
    p.add_argument('--notes', type=int, default=0)
    p.add_argument('--repeat', action='append', default=[], help='"the note | what would have caught it"')
    p = s.add_parser('audit'); p.add_argument('film')
    o = a.parse_args()
    d = load(o.film)
    film, rnd = current()
    rnd = rnd if film == o.film else None
    if o.cmd == 'estimate':
        d['estimate'] = o.pct
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
    elif o.cmd == 'audit':
        d['audit'] = audit(d)
        print('\n'.join(d['audit']))
    store(d)


if __name__ == '__main__':
    main()
