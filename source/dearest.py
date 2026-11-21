#!/usr/bin/env python3
"""dearest: the five most expensive THINGS a film (or a week) spent on, each opened as a proposal (cost audit, Sam
21 Nov: "audit every last thing done in order to find the most expensive things and run it through the proposal
route to discover how it can be made more compliant with statement one").

MAP
  named_of() ..... one ledger row -> {thing: % of a week}. Rows from 21 Nov on carry stepcost's exact 'named' split
                   (thinking, writing code, writing notes, reading notes, critique helpers, start-up reading ...).
                   Older rows only have the coarse split; their parts keep the old names, marked "(older record)",
                   so nothing is guessed. Rows with no split at all: "not split (record too old)"
  rank() ......... a film's rows (or every film's rows since a date) added up and sorted, dearest first
  report() ....... the plain-words table: thing, % of a week, share of the film, how many chats it touched
  open_top() ..... --open: each of the top five NAMED things (never "not split", a gap in the record) becomes notes/proposals/dearest-FILM-N.md with Problem / Facts /
                   Record filled from the figures (no solution: the route's helpers find that); one that is already
                   open is left alone. Statement 1 is written into each Problem so the helpers weigh it
  due() .......... the weekly reminder: handover.py end flags DEAREST when the last weekly ranking is over 7 days old
  test ........... `python3 source/dearest.py test`: GTA and Milburn rank, every row is counted once, the parts add up

    python3 source/dearest.py FILM [--open]          (film end: also printed by `propose.py review FILM`)
    python3 source/dearest.py week [--open]          (every film's rows in the last 7 days)
    python3 source/dearest.py test
"""
import datetime
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ledger  # noqa: E402

PROPS = os.path.join(ROOT, 'notes', 'proposals')
WEEKLY = os.path.join(PROPS, 'dearest-week.md')
OLD = {"Claude's words": "Claude's own writing: thinking, code, notes, messages (older record: not split)",
       'start-up floor': 'start-up reading (rules, tools, first files)',
       'cache re-write': 'memory lapses (re-paying for the whole chat)',
       'messages and reminders': 'messages and reminders',
       "Claude's edits": 'writing code and notes with the edit tool (older record)',
       'result: tool search': 'searching and reading code and notes (older record)',
       'result: film-file search': 'reading film code (older record)',
       'result: whole-file .py read': 'reading kit code (older record)',
       'result: pictures': 'looking at pictures', 'result: renders': 'renders', 'helpers': 'helpers',
       'result: page.py': 'start-up and handover tools', 'result: routine': 'routine work on Opus (older record)',
       'result: other': 'other tool results (older record)', 'unexplained': 'unexplained'}
STATEMENT_1 = ('Statement 1 (Sam, 13 Nov): every choice takes the way that gives higher quality first, then fewer notes '
               'and faults, then a film nearer 15% of a week; never one that trims the joke or reuses old content.')


def named_of(row):
    """One row -> {thing: % of a week}; the parts add up to the row's cost."""
    c = row.get('cost') or 0
    sp = row.get('split') or {}
    parts = sp.get('named') or _old_parts(row, sp.get('origins') or {})
    tot = sum(parts.values())
    if not tot:
        return {'not split (record too old)': c}
    return {k: c * v / tot for k, v in parts.items()}


def _search_thing(entry, film):
    """An older row's search entry [step, film/other, where, files, pattern, ...] -> a named thing."""
    where, files = entry[2], entry[3] or ''
    initials = ''.join(w[0] for w in film.split('-')) if film.count('-') >= 2 else film.replace('-', '_')
    if entry[1] == 'film' or where.startswith('shared:' + initials) or where.startswith('shared:' + film.replace('-', '_')):
        return 'reading film code'
    if where.startswith('shared:'):
        return 'reading start-up and handover tools' if where[7:] in ('handover.py', 'page.py', 'ledger.py', 'branches.py',
                                                                      'propose.py') else 'reading kit code'
    return {'film notes': 'reading notes', 'guides': 'reading guides'}.get(where, 'other searches')


def _old_parts(row, origins, film=''):
    """An older row (before 21 Nov) has only the coarse split. Its search results are shared out over the searches it
    listed (by count, so marked 'by count'); everything else keeps its old name, marked 'older record'."""
    parts = {}
    srch = sum(v for k, v in origins.items() if k in ('result: tool search', 'result: film-file search'))
    lst = (row.get('search') or {}).get('list') or []
    film = film or row.get('_film', '')
    for k, v in origins.items():
        if k in ('result: tool search', 'result: film-file search') and lst:
            continue
        t = OLD.get(k, k + ' (older record)')
        parts[t] = parts.get(t, 0) + v
    if srch and lst:
        for e in lst:
            t = _search_thing(e, film) + ' (older record, shared by count)'
            parts[t] = parts.get(t, 0) + srch / len(lst)
    return parts


def rows_for(film=None, since=None):
    if film:
        return [(film, dict(r, _film=film)) for r in ledger.load(film).get('chats', [])]
    out = []
    for f in sorted(glob.glob(os.path.join(ledger.DIR, '*.json'))):
        name = os.path.basename(f)[:-5]
        try:
            d = json.load(open(f))
        except Exception:
            continue
        out += [(name, dict(r, _film=name)) for r in d.get('chats', []) if isinstance(r, dict) and (r.get('date') or '') >= (since or '')]
    return out


def rank(film=None, since=None):
    """[(thing, % of a week, chats touched)], dearest first, and the total."""
    acc, n = {}, {}
    rows = rows_for(film, since)
    for _, r in rows:
        for k, v in named_of(r).items():
            acc[k] = acc.get(k, 0.0) + v
            n[k] = n.get(k, 0) + (1 if v > 0.005 else 0)
    total = sum(acc.values())
    return [(k, round(v, 2), n[k]) for k, v in sorted(acc.items(), key=lambda kv: -kv[1])], round(total, 2), len(rows)


def report(film=None, since=None, top=5):
    ranked, total, nrows = rank(film, since)
    what = film or f'every film since {since}'
    lines = [f'Dearest things: {what} ({nrows} chats, {total:g}% of a week in all)']
    for i, (k, v, n) in enumerate(ranked[:top], 1):
        lines.append(f'  {i}. {k}: {v:g}% of a week ({100 * v / total if total else 0:.0f}% of it), in {n} chats')
    if not film:                                    # the week: which films and jobs it went on
        by = {}
        for name, r in rows_for(None, since):
            by[name] = by.get(name, 0.0) + (r.get('cost') or 0)
        lines.append('  By film or job: ' + ', '.join(f'{k} {v:.1f}%' for k, v in sorted(by.items(), key=lambda kv: -kv[1])[:6]))
    old = sum(v for k, v, _ in ranked if 'older record' in k or 'too old' in k)
    if total and old:
        lines.append(f'  ({100 * old / total:.0f}% of this is on older records that could not name the parts; rows from '
                     '21 Nov on are named in full)')
    return '\n'.join(lines), ranked, total


def open_top(film=None, since=None, top=5):
    """Each of the top five opens as a proposal (step 1 of the route: problem and facts only)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import propose
    _, ranked, total = report(film, since, top)
    tag = film or 'week-' + (since or '')
    made = []
    named = [x for x in ranked if 'not split' not in x[0]][:top]     # a gap in the record is not a thing to cheapen
    for i, (k, v, n) in enumerate(named, 1):
        name = f'dearest-{tag}-{i}'
        f = os.path.join(PROPS, name + '.md')
        if os.path.exists(f) or _open_already(k):
            made.append((name, 'already open'))
            continue
        propose.new(name, f'cost: {k} ({v:g}% of a week on {film or "the week"})')
        body = open(f).read()
        body = body.replace('(what is wrong, in plain words; NO solution: the chat\'s own idea goes in '
                            f'{name}/chat.md)',
                            f'"{k}" cost {v:g}% of a week on {film or "the week"} ({100 * v / total if total else 0:.0f}% of '
                            f'all it spent), in {n} chats: number {i} of the dearest things. ' + STATEMENT_1 +
                            ' The question: how can this thing cost less with no loss of quality, or buy more '
                            'quality or fewer notes for what it costs?')
        body = body.replace('(the raw facts, each with its source: file, ledger, chat record; numbers as counted, '
                            '"unchecked" where not)',
                            f'- ledger rows: notes/ledger/{film or "*"}.json, each chat\'s split (named from 21 Nov on; '
                            'older rows only coarse), added up by source/dearest.py\n'
                            f'- the whole ranking: python3 source/dearest.py {film or "week"}\n'
                            '- the films\' costs and notes per round: notes/ledger/FILM.md')
        body = body.replace('(paths the helpers may search, one per line, e.g. notes/ledger/FILM.md)',
                            f'notes/ledger/{film}.md\nnotes/ledger/{film}.json\nsource/stepcost.py\nsource/dearest.py'
                            if film else 'notes/ledger/\nsource/stepcost.py\nsource/dearest.py')
        open(f, 'w').write(body)
        made.append((name, 'opened'))
    return made


def _open_already(thing):
    """A dearest proposal on the same thing still open (the week's ranking never doubles the film-end one)."""
    for f in glob.glob(os.path.join(PROPS, 'dearest-*.md')):
        t = open(f).read(2000)
        if f'cost: {thing} (' in t and 'Status: open' in t:
            return True
    return False


def due(today=None):
    """DEAREST fault for handover.py end: the weekly ranking is over 7 days old (or never run)."""
    today = today or datetime.date.today()
    try:
        last = datetime.date.fromisoformat(open(WEEKLY).readline().split()[-1])
    except Exception:
        return ['DEAREST: the weekly ranking of the dearest things has never run: python3 source/dearest.py week --open']
    if (today - last).days > 7:
        return [f'DEAREST: the weekly ranking of the dearest things last ran {last}: python3 source/dearest.py week --open']
    return []


def test():
    ok = True

    def check(c, msg):
        nonlocal ok
        print(('PASS ' if c else 'FAIL ') + msg)
        ok = ok and c
    for film in ('grand-theft-autism', 'milburn'):
        d = ledger.load(film)
        spent = round(sum(r.get('cost') or 0 for r in d['chats']), 2)
        ranked, total, nrows = rank(film)
        check(abs(total - spent) < 0.05, f'{film}: every row counted once ({total} vs {spent})')
        check(nrows == len(d['chats']) and len(ranked) >= 1, f'{film}: ranked {len(ranked)} things over {nrows} chats')
    row = {'cost': 2.0, 'split': {'named': {'thinking': 30, 'writing code': 50, 'reading notes': 20}}}
    check(abs(sum(named_of(row).values()) - 2.0) < 1e-9 and round(named_of(row)['writing code'], 2) == 1.0,
          'a named row\'s parts add up to its cost')
    old = {'cost': 1.0, 'split': {'origins': {"Claude's words": 60, 'start-up floor': 40}}}
    check(any('older record' in k for k in named_of(old)), 'an older row is marked as older, never guessed')
    check(named_of({'cost': 1.0}) == {'not split (record too old)': 1.0}, 'a row with no split says so')
    check(due(datetime.date(2099, 1, 1)) != [], 'the weekly ranking is flagged when overdue')
    import tempfile
    import propose
    keep = (PROPS, propose.PROPS)
    with tempfile.TemporaryDirectory() as tmp:
        globals()['PROPS'] = propose.PROPS = tmp
        try:
            made = open_top('grand-theft-autism')
            again = open_top('grand-theft-autism')
            files = sorted(glob.glob(os.path.join(tmp, 'dearest-*.md')))
            body = open(files[0]).read() if files else ''
            faults = propose.pack_faults(os.path.basename(files[0])[:-3]) if files else ['none']
        finally:
            globals()['PROPS'], propose.PROPS = keep
    check(len(files) == 5 and all(h == 'opened' for _, h in made), 'GTA: the top five open as proposals')
    check(all(h == 'already open' for _, h in again), 'GTA: a second run opens nothing twice')
    check('Statement 1' in body and '% of a week' in body, 'each proposal states the cost and Statement 1')
    check(not [x for x in faults if 'empty' in x or 'solution' in x],
          'the opened proposal passes the route\'s own problem check (no empty section, no solution in it): '
          + '; '.join(x for x in faults if 'empty' in x or 'solution' in x))
    print('ALL PASS' if ok else 'SOME FAILED')
    return ok


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return
    if argv[0] == 'test':
        sys.exit(0 if test() else 1)
    since = None
    film = argv[0]
    if film == 'week':
        film, since = None, (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    text, _, _ = report(film, since)
    print(text)
    if '--open' in argv:
        for name, how in open_top(film, since):
            print(f'  {how}: notes/proposals/{name}.md')
        if not film:
            os.makedirs(PROPS, exist_ok=True)
            open(WEEKLY, 'w').write(f'# Weekly dearest things, last run {datetime.date.today()}\n\n{text}\n')


if __name__ == '__main__':
    main(sys.argv[1:])
