#!/usr/bin/env python3
"""MAP  kitfilm: the kit tests at each film's start and end, not in every chat (rule 90; Sam, 25 Nov: "Make the kit check
happen at the beginning and the end of every film. If something major changes in the kits, then you can manually
suggest making one to me. Currently, it is wasting usage and time to do this with every chat."; proposal
notes/proposals/kit-tests-per-film.md, the judged pick V2).

  FILMS ............. notes/kittest-films.tsv (committed; merge=union): one row per kit run point of a film:
                      film, kind (start | final), when, chat. A film with no 'start' row has not had its first chat.
  started_here() .... handover end: this chat wrote a start row (it is a film's first chat)
  first_chat() ...... True when this chat is the film's first (no start row yet, or the start row is this chat's)
  at_start() ........ handover.py start --film NAME: in the film's first chat, writes the start row and starts the
                      stale kit tests in the background (watcher.py kittests-bg); in every chat, saves which tests are
                      stale now (local file), so the end can tell what THIS chat's changes made stale. Tool jobs (no
                      --film) start no run.
  never_green() ..... tests with no stamp at all: a new tool's own kit test, run once at the handover in any chat
  major_line() ...... handover end: when this chat's own changes made more than MAJOR tests stale, one plain line to
                      put to Sam (a full kit check, run only on his Y). Never a stop.
  setup_faults() .... the check: the start-up hook (setup.sh) starts no kit run
  final_row() ....... finish.py: a final (not an animatic) that passed the kit gate leaves the film's 'final' row

The setup hook no longer starts any kit run (setup.sh); finish.py's gate before an animatic or final is unchanged
(Change 2, keeping it before animatics: Sam's Y, 25 Nov; ANIMATIC_GATE).

    python3 source/kitfilm.py status [FILM]      the films' start / final rows
"""
import os
import subprocess
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FILMS = os.path.join(ROOT, 'notes', 'kittest-films.tsv')
START_STALE = os.path.join(ROOT, 'notes', 'logs', 'kittest-stale-start.txt')   # local to the machine (.gitignore)
MAJOR = 20                  # tests made stale by one chat's own changes before a full check is suggested to Sam
ANIMATIC_GATE = False       # Sam, 26 Nov: "the kit tests we had agreed only happen at the beginning and the end of a major film"
#                             (was True: Change 2, 25 Nov, the kit gate before every animatic)


def sid_now():
    return os.environ.get('CLAUDE_CODE_REMOTE_SESSION_ID', '').split('_')[-1] or 'local'


def rows(path=None):
    p = path or FILMS
    if not os.path.exists(p):
        return []
    return [ln.rstrip('\n').split('\t') for ln in open(p, encoding='utf-8') if ln.count('\t') >= 3]


def _add(film, kind, sid, path=None):
    p = path or FILMS
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'a', encoding='utf-8') as f:
        f.write(f'{film}\t{kind}\t{datetime.now(timezone.utc).isoformat(timespec="minutes")}\t{sid}\n')


def _norm(film):
    return (film or '').replace('_', '-').strip().lower()


def first_chat(film, sid=None, path=None):
    """The film's first chat: no start row yet, or the start row is this chat's own. No film (a tool job): False."""
    if not film:
        return False
    sid = sid or sid_now()
    starts = [r for r in rows(path) if _norm(r[0]) == _norm(film) and r[1] == 'start']
    return not starts or any(r[3] == sid for r in starts)


def started_here(sid=None, path=None):
    """handover end: this chat wrote a film's start row at its start (so it is that film's first chat). Needs no film
    name, so an end without --film, or a tool job whose files suggest a film, is never taken for a first chat."""
    sid = sid or sid_now()
    return any(r[1] == 'start' and r[3] == sid for r in rows(path))


def _stale_names():
    sys.path.insert(0, HERE)
    import kitstamps
    st, _ = kitstamps.stale(kitstamps.test_names())
    return st


def at_start(film, sid=None, path=None, start_path=None, stale_fn=None, launch_fn=None):
    """handover.py start. Returns the lines to print. In the film's first chat: the start row and the background run."""
    sid = sid or sid_now()
    out = []
    try:
        st = (stale_fn or _stale_names)()
    except Exception as e:
        st = None
        out.append(f'kit tests: could not list the stale ones ({e})')
    if st is not None:
        sp = start_path or START_STALE
        os.makedirs(os.path.dirname(sp), exist_ok=True)
        with open(sp, 'w', encoding='utf-8') as f:
            f.write(f'{sid}\t{",".join(st)}\n')
    if film and practice(film):
        out.append(f'kit tests: {film} is a practice job: no kit tests (Sam, 26 Nov: only at the start and end of a major film)')
    elif film and first_chat(film, sid, path):
        if not any(_norm(r[0]) == _norm(film) and r[1] == 'start' and r[3] == sid for r in rows(path)):
            _add(_norm(film), 'start', sid, path)
        (launch_fn or _launch)()
        out.append(f'kit tests: {film}\'s first chat: the start-of-film kit check runs in the background '
                   f'({len(st or [])} tests to run); `handover.py end` waits for it (rule 90)')
    elif film:
        out.append('kit tests: not this chat (rule 90: only a film\'s first chat and its final run them)')
    return out


def practice(film, notes_dir=None):
    """A practice job (a test clip, a learn job): its notes file has a line 'Kind: practice' (Sam, 26 Nov). No kit
    tests at its start or end; a never-passed test of a tool it builds still runs once (always test what is built)."""
    p = os.path.join(notes_dir or os.path.join(ROOT, 'notes'), f'{_norm(film)}.md')
    try:
        return any(ln.strip().lower() == 'kind: practice' for ln in open(p, encoding='utf-8'))
    except OSError:
        return False


def _launch():
    subprocess.Popen([sys.executable, os.path.join(HERE, 'watcher.py'), 'kittests-bg'], cwd=ROOT,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)


def never_green(names=None, record=None):
    """Tests with no stamp line at all: a new tool's own kit test (run once at its chat's handover)."""
    sys.path.insert(0, HERE)
    import kitstamps
    names = names if names is not None else kitstamps.test_names()
    seen = {r['name'] for r in kitstamps._rows(record or kitstamps.RECORD)}
    return [n for n in names if n not in seen]


def made_stale(sid=None, stale_now=None, start_path=None):
    """The tests stale now that were not stale at this chat's start (None when the start list is not this chat's)."""
    sid = sid or sid_now()
    sp = start_path or START_STALE
    if not os.path.exists(sp):
        return None
    got = open(sp, encoding='utf-8').read().rstrip('\n').split('\t')
    if len(got) < 2 or got[0] != sid:
        return None
    before = set(filter(None, got[1].split(',')))
    now = stale_now if stale_now is not None else _stale_names()
    return [n for n in now if n not in before]


def major_line(sid=None, stale_now=None, start_path=None, secs=None):
    """handover end: '' or one plain line suggesting a full kit check to Sam (his Y runs it)."""
    made = made_stale(sid, stale_now, start_path)
    if made is None or len(made) <= MAJOR:
        return ''
    mins = ''
    if secs:
        mins = f', about {max(1, round(sum(secs.get(n, 60.0) for n in made) / 60))} min'
    return (f'KIT CHANGE (not a stop; rule 90): this chat changed shared tools that {len(made)} kit checks rely on. '
            f'Ask Sam in plain words, numbered with the other questions: "N. Run the full kit check now (it re-checks '
            f'that the faults you caught stay fixed{mins})? Y or N". Run `python3 source/kittests.py --stale` only on '
            'his Y; on N the film\'s final runs them.')


def setup_faults(text=None):
    """Rule 90's check on the start-up hook: no kit run when a machine starts (the old fault: every chat ran them)."""
    text = text if text is not None else open(os.path.join(ROOT, '.claude', 'hooks', 'setup.sh'), encoding='utf-8').read()
    live = [ln for ln in text.splitlines() if not ln.lstrip().startswith('#')]
    return [f'the start-up hook runs the kit tests in every chat: {ln.strip()[:100]}' for ln in live
            if 'kittests' in ln]


def final_row(film, path=None):
    if film:
        _add(_norm(film), 'final', sid_now(), path)


def main(argv):
    if argv[:1] == ['status']:
        film = argv[1] if len(argv) > 1 else None
        for r in rows():
            if not film or _norm(r[0]) == _norm(film):
                print('\t'.join(r))
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
