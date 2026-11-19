"""The quiet cost line (Sam, 19 Nov; job 2).

At every handover the film's cost so far and forecast are RECORDED (in the film's ledger and its notes), always, and
SHOWN to Sam only when something is wrong, once per problem, with a way to save cost that keeps the quality.

  python3 source/costline.py FILM [--notes PATH]     record the line; print a message only on a problem

What counts as a problem: a planned stage that finished at more than 1.5x its planned share, or a forecast more than
25% over the film's own estimate because the stages ran dearer than planned. A forecast over 15% of a week is NOT a
problem by itself (Sam adds things that take a film past 15%; that is allowed and never nagged about).
Nothing here ever suggests cutting a joke or doing less.
"""
import datetime
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(DIR)
sys.path.insert(0, DIR)
MARK = 'Cost line (recorded every handover; shown to Sam only on a problem):'
SAVE = ('Cheapest way on that keeps the quality: build from kit pieces that already exist before making new ones, '
        'give routine steps (checks, animatic, sending) to Sonnet, and hand over before a chat grows long so '
        'its history is not paid for again.')


def line(d):
    """'film so far X% of 15%; forecast Y%' (the forecast is None before the stages are planned)."""
    import ledger
    spent = ledger.totals(d)[0]
    f = ledger.forecast(d)
    fc = f'{f[2]:g}%' if f else 'not yet planned'
    return f'film so far {spent:g}% of 15%; forecast {fc}', spent, (f[2] if f else None)


def problems(d):
    """The new problems only (each named once in the ledger under cost_flagged)."""
    import ledger
    seen, out = d.setdefault('cost_flagged', []), []
    for s in d.get('stages') or []:
        if s.get('done') and s['pct'] > 0 and not s.get('unplanned'):
            prior = [x for x in d['stages'] if x.get('done') and x is not s]
            before = max([x['done']['spent'] for x in prior if x['done']['spent'] <= s['done']['spent']], default=0.0)
            used = s['done']['spent'] - before
            if used > 1.5 * s['pct'] and s['name'] not in seen:
                seen.append(s['name'])
                out.append(f"{s['name']} cost about {used:.1f}% of a week against {s['pct']:g}% planned")
    f, est = ledger.forecast(d), d.get('estimate')
    if f and est and f[2] > est * 1.25 and 'forecast' not in seen and out:
        seen.append('forecast')
        out.append(f'the forecast is {f[2]:g}% against the film\'s own {est:g}%')
    return out


def record(film, notes=None):
    """Record the line (ledger + notes). Returns the message for Sam, or None when nothing is wrong."""
    import ledger
    d = ledger.load(film)
    if not d.get('estimate'):
        return None
    text, spent, fc = line(d)
    new = problems(d)
    d.setdefault('cost_log', []).append({'date': str(datetime.date.today()), 'spent': spent, 'forecast': fc})
    ledger.store(d)
    p = notes or os.path.join(ROOT, 'notes', f'{film}.md')
    if os.path.exists(p):
        body = open(p, encoding='utf-8').read()
        entry = f'{MARK} {text} ({datetime.date.today()})'
        body = re.sub(r'(?m)^' + re.escape(MARK) + r'.*\n?', '', body).rstrip('\n') + '\n\n' + entry + '\n'
        open(p, 'w', encoding='utf-8').write(body)
    return ('Cost: ' + '; '.join(new) + '. ' + SAVE) if new else None


def faults(film, notes=None):
    """For handover.py end: the line is recorded here, so the only fault is a film that cannot record it."""
    import ledger
    d = ledger.load(film)
    if not d.get('estimate'):
        return [f'COST: {film} has no estimate in the ledger, so the cost line cannot be recorded '
                f'(python3 source/ledger.py estimate {film} PERCENT)']
    msg = record(film, notes)
    return [msg] if msg else []


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    m = record(a[0], a[a.index('--notes') + 1] if '--notes' in a else None)
    print(m or 'cost line recorded; nothing to show Sam')
