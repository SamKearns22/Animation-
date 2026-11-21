"""hookran: each automatic step leaves a 'seen running' mark when it runs (Sam, 21 Nov: "Why are tools built then not
enabled? Keeps happening."). The watcher reads the marks: a step that is switched on but never seen running is flagged,
so a tool is ticked done only after it has really run in a chat, not when its file and test exist.

    import hookran; hookran.ran('modelguard.py')       first thing in the step's main(); never raises

The marks live on this machine (~/.claude/watcher/ran/NAME: the last time it ran), one file per step, named as
watcher.systems() names it ('handover.py log', 'modelguard.py').
"""
import os
import time

DIR = os.path.expanduser('~/.claude/watcher/ran')


def ran(name):
    try:
        if not os.path.isdir(DIR):
            os.makedirs(DIR, exist_ok=True)
        if not os.path.exists(os.path.join(DIR, '_since')):          # when marks began on this machine
            open(os.path.join(DIR, '_since'), 'w').write(f'{time.time():.0f}\n')
        with open(os.path.join(DIR, name.replace('/', '_')), 'w') as f:
            f.write(f'{time.time():.0f}\n')
    except Exception:
        pass


def since():
    """When this machine began keeping marks (a chat older than that cannot be judged on its start-up steps)."""
    return last('_since')


def last(name):
    """When the step last ran on this machine (seconds since 1970), or None."""
    try:
        return float(open(os.path.join(DIR, name.replace('/', '_'))).read().strip())
    except (OSError, ValueError):
        return None
