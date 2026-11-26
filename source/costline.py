"""The quiet cost line (Sam, 19 Nov; job 2).

At every handover the film's cost so far is RECORDED (in the film's ledger and its notes), quietly, and never shown
to Sam: the forecast and the cost warnings were deleted on Sam's word (R8 check audit, 26 Nov, his answer 2: the
paused budget alarms go; the quiet tracking stays).

  python3 source/costline.py FILM [--notes PATH]     record the line (prints nothing)
"""
import datetime
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(DIR)
sys.path.insert(0, DIR)
MARK = 'Cost line (recorded every handover; shown to Sam only on a problem):'

def line(d):
    """'film so far X% of a week'."""
    import ledger
    spent = ledger.totals(d)[0]
    return f'film so far {spent:g}% of a week', spent


def record(film, notes=None):
    """Record the line (ledger + notes), quietly. Returns None (nothing is ever shown)."""
    import ledger
    d = ledger.load(film)
    if not d.get('chats'):
        return None
    text, spent = line(d)
    d.setdefault('cost_log', []).append({'date': str(datetime.date.today()), 'spent': spent})
    ledger.store(d)
    p = notes or os.path.join(ROOT, 'notes', f'{film}.md')
    if os.path.exists(p):
        body = open(p, encoding='utf-8').read()
        entry = f'{MARK} {text} ({datetime.date.today()})'
        body = re.sub(r'(?m)^' + re.escape(MARK) + r'.*\n?', '', body).rstrip('\n') + '\n\n' + entry + '\n'
        open(p, 'w', encoding='utf-8').write(body)
    return None


def faults(film, notes=None):
    """For handover.py end: the line is recorded here, so the only fault is a film that cannot record it."""
    record(film, notes)
    return []


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    record(a[0], a[a.index('--notes') + 1] if '--notes' in a else None)
    print('cost line recorded (quietly)')
