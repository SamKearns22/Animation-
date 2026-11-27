#!/usr/bin/env python3
"""MAP  kitfilm: the kit tests at each film's start and end, not in every chat (rule 90; Sam, 25 Nov: "Make the kit check
happen at the beginning and the end of every film. If something major changes in the kits, then you can manually
suggest making one to me. Currently, it is wasting usage and time to do this with every chat."; proposal
notes/proposals/kit-tests-per-film.md, the judged pick V2).

  FILMS ............. notes/kittest-films.tsv (committed; merge=union): one row per kit run point of a film:
                      film, kind (start | final), when, chat. A film with no 'start' row has not had its first chat.
  started_here() .... handover end: this chat wrote a start row (it is a film's first chat)
  first_chat() ...... True when this chat is the film's first (no start row yet, or the start row is this chat's)
  begun(), begin(), lessons(): where a film starts and ends (Sam, 26 Nov): the screenplay and title; the lessons.
  _health() ......... R14: the tool health report (source/toolhealth.py), one plain line per tool, printed with the
                      kit tests at a film's start (at_start's first chat, begin) and end (lessons)
  at_start() ........ handover.py start --film NAME: once the film has begun (its notes say so), in its first chat, writes the start row and starts the
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

    python3 source/kitfilm.py begin FILM         Sam gave the screenplay and title: the film's start (run in that chat);
                                                 also the kit found for it (B3: lookups)
    python3 source/kitfilm.py lookups FILM       the catalogue's rows per brief line, the face tool per filed person
    python3 source/kitfilm.py lessons FILM       Sam asked for the film's lessons: the film's end (the stale tests)
    python3 source/kitfilm.py status [FILM]      the films' start / end rows
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


def _health(film):
    """R14 (Sam, 26 Nov): the tool health report runs beside the kit tests, one plain line per tool for Sam."""
    try:
        import toolhealth
        return ['TOOL HEALTH (tell Sam these lines in plain words; a "partly" goes to him as a numbered question with '
                'its fix, never fixed unasked):'] + ['  ' + x for x in toolhealth.at_start(film).splitlines()]
    except Exception as e:                      # a report that cannot run is said, never skipped
        return [f'TOOL HEALTH: could not run ({type(e).__name__}: {e})']


def at_start(film, sid=None, path=None, start_path=None, stale_fn=None, launch_fn=None, notes_dir=None, health_fn=None):
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
    if film and practice(film, notes_dir):
        out.append(f'kit tests: {film} is a practice job: no kit tests (Sam, 26 Nov: only at the start and end of a major film)')
    elif film and not begun(film, notes_dir):
        out.append(f'kit tests: not yet for {film} (rule 90: they start when Sam gives the screenplay and title; '
                   '`kitfilm.py begin FILM` in that chat)')
    elif film and first_chat(film, sid, path):
        if not any(_norm(r[0]) == _norm(film) and r[1] == 'start' and r[3] == sid for r in rows(path)):
            _add(_norm(film), 'start', sid, path)
        (launch_fn or _launch)()
        out.append(f'kit tests: {film}\'s first chat: the start-of-film kit check runs in the background '
                   f'({len(st or [])} tests to run); `handover.py end` waits for it (rule 90)')
        health = health_fn or (None if launch_fn else _health)    # a kittest passes its own launcher: no report
        out += health(film) if health else []
    elif film:
        out.append('kit tests: not this chat (rule 90: only a film\'s first chat and its final run them)')
    return out


# Where a film starts and ends (Sam, 26 Nov, crowd pool chat 1: "The beginning of the film is when I give you the
# screenplay and title. The end of the film is when I ask for any lessons on the film that need to be learned."):
#   start: the film's notes carry the line 'Screenplay and title: given DATE' (the chat Sam gives them to writes it,
#          `kitfilm.py begin FILM`); a job without it (a tool, a pool, a practice clip) never starts the run
#   end:   `kitfilm.py lessons FILM`, run when Sam asks for the film's lessons: the stale tests, and the 'end' row
#          (a final render no longer runs or waits for them)
BEGUN = 'screenplay and title: given'


def begun(film, notes_dir=None):
    """True when the film's notes say Sam gave the screenplay and title (the film's start, Sam 26 Nov)."""
    p = os.path.join(notes_dir or os.path.join(ROOT, 'notes'), f'{_norm(film)}.md')
    try:
        return any(ln.strip().lower().startswith(BEGUN) for ln in open(p, encoding='utf-8'))
    except OSError:
        return False


def begin(film, notes_dir=None, sid=None, path=None, launch_fn=None):
    """Sam gave the screenplay and title in this chat: the start line in the notes, the start row, the run."""
    p = os.path.join(notes_dir or os.path.join(ROOT, 'notes'), f'{_norm(film)}.md')
    if not begun(film, notes_dir):
        with open(p, 'a', encoding='utf-8') as f:
            f.write(f'\nScreenplay and title: given {datetime.now(timezone.utc):%d %b %Y} (the film\'s start: kit tests, rule 90)\n')
    sid = sid or sid_now()
    if not any(_norm(r[0]) == _norm(film) and r[1] == 'start' for r in rows(path)):
        _add(_norm(film), 'start', sid, path)
        (launch_fn or _launch)()
        if not launch_fn:
            print('\n'.join(_health(film)))
            print('\n'.join(lookups(film, notes_dir)))   # B3: the kit looked up for the plan chat
        return f'kit tests: {film} starts (screenplay and title given): the kit check runs in the background; `handover.py end` waits for it'
    return f'kit tests: {film} already started (its start row is on record)'


# B3 (replay test 2, Sam's Y, 27 Nov): the plan chat of Islamocommunism's replay spent 5-6 steps a real person
# finding the face tool route, and found the missing hair piece only on the cast sheet. At the film's start the kit
# is looked up for it: the catalogue's best rows for each brief line, and the face tool (background, ~2 min each)
# for each real person whose photos are filed (references/faces/NAME/NN-front-WHERE.jpg) and named in the brief;
# its hair piece (or NEW), beard and sheet are written into the film's notes when it ends. Kittest start_lookups.
KIT_FOUND = '## Kit found at the start'
FACES = os.path.join(ROOT, 'references', 'faces')


def brief_lines(film, notes_dir=None):
    """The film's brief checklist rows (its notes' section whose heading names the brief and a checklist: bullets
    '- [ ] ...' or the template's table rows '| N | words | done? |')."""
    p = os.path.join(notes_dir or os.path.join(ROOT, 'notes'), f'{_norm(film)}.md')
    try:
        text = open(p, encoding='utf-8').read().splitlines()
    except OSError:
        return []
    out, inside = [], False
    for ln in text:
        if ln.startswith('## '):
            low = ln.lower()
            inside = 'brief' in low and 'checklist' in low
            continue
        if not inside:
            continue
        if ln.startswith('- '):
            w = ln[2:].strip()
            w = w[3:].strip() if w[:3] in ('[ ]', '[x]', '[X]') else w
            out.append(w)
        elif ln.startswith('|') and not ln.startswith('| #') and not ln.startswith('|--') and not ln.startswith('| ---'):
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if len(cells) >= 2 and cells[1]:
                out.append(cells[1])
    return [w for w in out if len(w) > 3]


def people_filed(text, faces=None):
    """[(name, front photos, picked)] for each person filed under references/faces whose folder name is a word of the
    brief: their front photos (*-front-*) and whether Sam's pick is on file (known: no face tool run)."""
    import re
    faces = faces or FACES
    words = set(re.findall(r"[a-z][a-z'-]+", text.lower().replace("\u2019", "'")))
    words = {w[:-2] if w.endswith("'s") else w for w in words}          # El-Sayed's -> el-sayed
    words |= {w.replace("'", '').replace('-', '') for w in words} | {p for w in words for p in w.split('-')}
    out = []
    for name in sorted(os.listdir(faces)) if os.path.isdir(faces) else []:
        d = os.path.join(faces, name)
        if not os.path.isdir(d) or name.lower() not in words:
            continue
        fronts = sorted(os.path.join(d, f) for f in os.listdir(d) if '-front' in f.lower()
                        and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')))
        if fronts:
            out.append((name, fronts, os.path.exists(os.path.join(d, 'pick', f'{name}-pick.json'))))
    return out


def lookups(film, notes_dir=None, faces=None, launch_fn=None):
    """The kit looked up for a new film (B3): written under KIT_FOUND in its notes; the face tool started in the
    background for each new real person. Returns the lines written."""
    sys.path.insert(0, HERE)
    import catalogue
    p = os.path.join(notes_dir or os.path.join(ROOT, 'notes'), f'{_norm(film)}.md')
    brief = brief_lines(film, notes_dir)
    out = ['', KIT_FOUND, f'(kitfilm begin, {datetime.now(timezone.utc):%d %b}: the catalogue\'s best rows per brief line; '
           'the face tool per real person filed under references/faces; a row is KNOWN only once a person checks it)']
    if not brief:
        out.append(f'- no brief checklist in the notes yet: write it, then `python3 source/kitfilm.py lookups {film}`')
    for w in brief:
        rows = catalogue.find(w, 2, least=2)
        found = '; '.join(f'{what[:80]} [{where[:60]}]' for _, what, where in rows) or 'nothing in the kit fits: NEW (or a plain moment, nothing to build)'
        out.append(f'- "{w[:70]}": {found}')
    for name, fronts, picked in people_filed(' '.join(brief), faces):
        if picked:
            out.append(f'- {name}: Sam\'s pick is on file (references/faces/{name}/pick): KNOWN')
            continue
        dst = os.path.join(faces or FACES, name, 'draft')
        (launch_fn or _face_bg)(film, name, dst, fronts, p)
        out.append(f'- {name}: the face tool started in the background on {len(fronts)} front photos (about 2 min); '
                   f'its hair piece, beard and sheet are added here when it ends')
    with open(p, 'a', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
    return out


def _face_bg(film, name, dst, fronts, notes):
    subprocess.Popen([sys.executable, os.path.join(HERE, 'kitfilm.py'), 'face', film, name, dst, notes] + list(fronts),
                     cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)


def face_result(film, name, dst, notes, fronts, run_fn=None):
    """The background face tool run (B3): facepick on the person's front photos, then one line in the notes: the
    hair piece that fits (or NEW: a priced row in the estimate), the beard, the sheet to send Sam."""
    if run_fn is None:
        r = subprocess.run([sys.executable, os.path.join(HERE, 'facepick.py'), name, dst] + list(fronts),
                           cwd=ROOT, capture_output=True, text=True)
        log = (r.stdout or '') + (r.stderr or '')
    else:
        log = run_fn()
    keep = [ln.strip() for ln in log.splitlines()
            if ln.strip().startswith((f'{name}: hair piece', f'{name}: NEW', 'beard:')) or ln.strip().endswith('-sheet.jpg')]
    line = f'- {name} (face tool done): ' + ('; '.join(keep) if keep else 'FAILED, no result: run facepick.py by hand')
    with open(notes, 'a', encoding='utf-8') as f:
        f.write(line + '\n')
    return line


def lessons(film, sid=None, path=None, run_fn=None):
    """Sam asked for the film's lessons (the film's end): run the stale kit tests now and write the 'end' row."""
    sys.path.insert(0, HERE)
    st = _stale_names() if run_fn is None else []
    ok = True
    if run_fn is not None:
        ok = run_fn()
    elif st:
        ok = subprocess.run([sys.executable, os.path.join(HERE, 'kittests.py'), '--stale'], cwd=ROOT).returncode == 0
    _add(_norm(film), 'end', sid or sid_now(), path)
    if run_fn is None:
        print('\n'.join(_health(film)))          # R14: the tool report at the film's end too, with its kit tests
    return ok


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
    if argv[:1] == ['lookups'] and len(argv) > 1:
        print('\n'.join(lookups(argv[1])))
        return 0
    if argv[:1] == ['face'] and len(argv) > 5:
        print(face_result(argv[1], argv[2], argv[3], argv[4], argv[5:]))
        return 0
    if argv[:1] == ['begin'] and len(argv) > 1:
        print(begin(argv[1]))
        return 0
    if argv[:1] == ['lessons'] and len(argv) > 1:
        ok = lessons(argv[1])
        print(f'kit tests: {argv[1]}\'s end-of-film check {"passed" if ok else "FAILED: fix or name each red before the lessons"}')
        return 0 if ok else 1
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
