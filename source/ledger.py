#!/usr/bin/env python3
"""Film ledger (Job F, Sam 9 Nov): what each film cost and what went wrong, kept on GitHub, not in the chat.

MAP
  files ............ notes/ledger/FILM.json (the record), FILM.md (written from it), FILM/round-N.txt (evidence)
  round ............ start a round: later check results are saved into that round's file automatically
  record() ......... called by report.summarise: every check's full result (clean ones too) goes into the round file
  save / note ...... the check sheet's text, false alarms, "could not test", into the round file
  log .............. at every handover: this chat's cost (from the cost watch), model, stage, notes, repeated notes
  appcost .......... cost-spike fix 7 (Sam's Y, 27 Nov): at each chat's end the app's own figure (get_session) goes
                     into app-costs.tsv and notes/ledger/app-check.tsv beside the estimate (main chat, helpers and
                     other records apart); an estimate more than 25% under it is flagged (chat 36: $4.71 vs $12.50).
                     handover.py end flags a cloud chat with no app figure. Test: appcost_test (kittest app_cost_gap)
  app .............. the REAL record (cost job, 13 Nov): notes/ledger/app-costs.tsv holds each chat's cost from the
                     app (get_session usage.cost_usd, list $); `app` turns it into each film's rows, replacing the
                     estimates for the same chats (and, from a film's first app row on, its estimate rows without a
                     session id, except rows marked keep). Chats that hit the usage limit or never pushed are caught
                     here, since the app keeps the figure after the chat ends
  auto ............. the Stop hook (Sam, 11 Nov: "automate this"): after every turn, this chat's running cost goes
                     into the ledger of the film or job it worked on (found from the files it touched); committed and
                     pushed when it has moved by 0.25% of a week, so the record survives the chat
  estimate ......... the film's estimate (% of a week), for estimate versus actual; --stages gives the plan's stages
                     and shares (Job M, rule 24): "cast 2, sets 2.5, board 0.5, moves 3, animatic1 1, round 1.5, final 0.5"
  stage ............ marks a stage done at its end (the first open one of that name; one not in the plan is added
                     with no share): kept quietly for later study. The forecast, the budget stop and the stage stop
                     were deleted on Sam's word (R8 check audit, 26 Nov, his answer 2: "tracked quietly")
  push_row() ....... startup-fixes 1 (Sam, 16 Nov): every row goes onto the main line as its own commit holding only
                     the ledger files (mainline.to_main: fetch, commit, push, 3 tries); the chat's HEAD is never pushed
  union() .......... two copies of a ledger as one, each chat once (sid, then transcript id; an app row beats an
                     estimate); used by gather, the merge driver (mergefile, .gitattributes) and push_row
  gather ........... one-off: every row stranded on any branch onto the main line; `audit` lists rows still missing
  audit ............ after the film (rule 24, Sam 13 Nov; replaced the 10-line audit): one line, its real cost
                     against the last three films' (ledgers with an estimate); over 1.5x their average, the next chat
                     finds why before any film work
  stepcost ......... (history-and-search Learn, 16 Nov) auto also writes each chat's steps, history at the end
                     and cost by kind of step (source/stepcost.py) onto its row, kept when the app row replaces it
  kept() ........... rule 37 (Job L): sounds and references not yet on GitHub, at every log (handover) and `kept`

    python3 source/ledger.py estimate FILM 10 --stages "cast 3, sets 2, board 0.5, moves 2, animatic1 1, round 1.5, final 0.5"
    python3 source/ledger.py stage FILM cast          (at the end of each stage; "board" ends itself: rough.py sent --board)
    python3 source/ledger.py round FILM 2
    python3 source/ledger.py save FILM SHEET.txt          (or: save FILM - "text", a line straight in)
    python3 source/ledger.py note FILM "false alarm: handcheck 12.3 s, the hand is behind the mug on purpose"
    python3 source/ledger.py log FILM --stage "round 2 notes" --notes 9 --repeat "arm join at 4 s | shoulder test"
    python3 source/ledger.py audit FILM                 (also: rows missing from the main line; no FILM: all films)
    python3 source/ledger.py gather
    python3 source/ledger.py kept                       (also run by every log)

A chat is tagged by its transcript; logging the same chat again replaces its row, so nothing is counted twice.
"""
import argparse, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datetime import date, datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'notes', 'ledger')
CURRENT = os.path.join(DIR, '.current')      # "FILM ROUND": where check results go


def _paths(film):
    # chat 17 (protest-tiers): pre-flight passes the code name (protest_tiers) and the ledger is filed under the film's
    # name (protest-tiers), so the critique read "none recorded"; the hyphen file is used when only it exists
    if '_' in film and not os.path.exists(os.path.join(DIR, film + '.json')) \
            and os.path.exists(os.path.join(DIR, film.replace('_', '-') + '.json')):
        film = film.replace('_', '-')
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


RUN = os.environ.get('CHECK_RUN') or f'{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%S}-{os.getpid()}'
_WARNED = []
WHOLE = ('pre-flight', 'quick check')     # titles whose one list holds many checks' faults


def check_film():
    """check-catches change 1 (Sam's Y, 20 Nov): the film a check is saved under, with NO marker file needed: the film
    named in the command (pre-flight puts it in CHECK_FILM for itself and every check it starts; a check run on its
    own names the film among its arguments), else the old marker (notes/ledger/.current). Before, with no marker file
    every check quietly saved nothing: 0 rows in all 27 ledgers against Milburn's 14 pre-flight runs."""
    env = os.environ.get('CHECK_FILM', '')
    if re.match(r'^[\w-]+$', env):
        return env.replace('_', '-') if os.path.exists(os.path.join(ROOT, 'notes', env.replace('_', '-') + '.md')) else env
    for a in [os.path.splitext(os.path.basename(a))[0] for a in sys.argv[1:]]:
        for n in (a, a.replace('_', '-')):
            if n and re.match(r'^[\w-]+$', n) and n not in SKIP and os.path.exists(os.path.join(ROOT, 'notes', n + '.md')):
                return n
    return current()[0]


def record(title, faults, notes=()):
    """Called by report.summarise for every check. Saves the full list into the round file and counts each check's
    faults by kind, so the audit can say which checks caught things and which never fired. change 1: also one line
    per check run in notes/ledger/FILM/checks.jsonl (time, run, check, its faults, clean ones too), so each fault's
    fate comes from comparing one run with the next (checkreplay.py table FILM --record). Never breaks a check; says
    so in one line when it cannot save."""
    try:
        film = check_film()
        if not film:
            if not _WARNED:
                _WARNED.append(1)
                print('(check record: not saved: no film named in the command; run it as `CHECK_FILM=NAME ...` '
                      'or with the film as an argument)')
            return
        cf, crnd = current()
        rnd = crnd if cf and cf.replace('_', '-') == film.replace('_', '-') else 0
        import report
        faults = list(faults)
        body = f'== {title} ({date.today()}): ' + (f'{len(faults)} fault(s)' if faults else 'clean') + '\n'
        body += ''.join(f'- {x}\n' for x in faults) + ''.join(f'  {n}\n' for n in notes)
        name = re.sub(r'\s*\(.*\)$', '', title)
        os.makedirs(_paths(film)[2], exist_ok=True)   # the run lines first: they need nothing else to work
        t, run = datetime.now(timezone.utc).isoformat(timespec='seconds'), os.environ.get('CHECK_RUN') or RUN
        parts = {name: faults}
        if name in WHOLE:                             # pre-flight's one list: each check under its own name
            import checkreplay
            parts = {name: []}
            for x in faults:
                parts.setdefault(checkreplay.head(str(x)), []).append(x)
        with open(os.path.join(_paths(film)[2], 'checks.jsonl'), 'a', encoding='utf-8') as f:
            for k, v in parts.items():
                f.write(json.dumps({'t': t, 'run': run, 'check': k, 'of': name,
                                    'faults': [str(x)[:200] for x in v]}) + '\n')
        append(film, rnd, body)
        d = load(film)
        c = d.setdefault('checks', {}).setdefault(name, {'runs': 0, 'faults': 0, 'kinds': {}})
        c['runs'] += 1
        c['faults'] += len(faults)
        for x in faults:
            k = report.kind(x)
            c['kinds'][k] = c['kinds'].get(k, 0) + 1
        store(d)
    except Exception as e:
        print(f'(check record: not saved: {e})')


def checkruns(film):
    """The record as runs, oldest first, in checkreplay's shape: {'runs': [{'branch': RUN, 'ran': [checks],
    'faults': {check: [...]}}]}."""
    p = os.path.join(_paths(film)[2], 'checks.jsonl')
    runs = {}
    for ln in (open(p, encoding='utf-8') if os.path.exists(p) else []):
        try:
            x = json.loads(ln)
        except ValueError:
            continue
        r = runs.setdefault(x['run'], {'branch': x['run'], 't': x['t'], 'secs': 0, 'ran': [], 'of': {}, 'faults': {}})
        r['ran'] += [x['check'], x.get('of', x['check'])]
        r['of'][x['check']] = x.get('of', x['check'])
        if x['faults']:
            r['faults'].setdefault(x['check'], []).extend(x['faults'])
    return {'film': film, 'runs': sorted(runs.values(), key=lambda r: r['t'])}


def record_since(film, since):
    """Lines saved for FILM at or after SINCE (an ISO time, UTC)."""
    return [r for r in checkruns(film)['runs'] if r['t'][:19] >= since[:19]]


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


PROCESS = 'proposal-route'      # tool, kit and process upgrades (notes/proposals/...): never a film's cost (Sam, 16 Nov)
NAMED = r'(?:notes|source)/(proposals/|[A-Za-z0-9_-]+\.(?:md|py))'


def _jobs(text, names, count=None):
    """{job: times named} in text: notes/NAME.md or source/NAME*.py with a notes file; notes/proposals/... = PROCESS."""
    count = {} if count is None else count
    for m in re.finditer(NAMED, text):
        n = m.group(1)
        if n == 'proposals/':
            n = PROCESS
        else:
            n = os.path.splitext(n)[0]
            n = n if n in names else n.split('_')[0]
        if n in names:
            count[n] = count.get(n, 0) + 1
    return count


def _task(transcript):
    """The chat's task: its first typed message (the seed from the last chat's handover, or Sam's own)."""
    for raw in open(transcript, encoding='utf-8', errors='replace'):
        if '"user"' not in raw:
            continue
        try:
            r = json.loads(raw)
        except ValueError:
            continue
        c = (r.get('message') or {}).get('content') if r.get('type') == 'user' else None
        if isinstance(c, list):
            c = '' if any(x.get('type') == 'tool_result' for x in c) else ' '.join(x.get('text', '') for x in c)
        if c and c.strip():
            return c
    return ''


def film_of(transcript):
    """The film or job this chat worked on, in this order: (0) the film its task names with --film NAME; (1) a task (its first message) under notes/proposals/ is
    process work (named more than any film), billed to the proposal-route ledger (Sam, 16 Nov: chat 7406486e built a startup fix
    but was billed to a film on hiatus, because it tested on that film's notes 14 times); (2) any chat that names
    notes/morning-report.md is overnight work, recorded there (Sam, 14 Nov); (3) the film its task names most; (4) the
    notes/NAME.md (or source/NAME*.py with a notes file) its own tool calls named most."""
    names = {os.path.splitext(f)[0] for f in os.listdir(os.path.join(ROOT, 'notes')) if f.endswith('.md')} - SKIP
    names.add(PROCESS)
    told = re.search(r'--film[ =]([A-Za-z0-9_-]+)', _task(transcript))   # (0) the film the chat is told it works on
    if told and told.group(1) in names:           # wins (pose-kit-format C1, Sam 26 Nov: R7 chats 1-5 were billed to
        return told.group(1)                      # brexit-is-done and proposal-route, 13.3% hidden from R7)
    task = _jobs(_task(transcript), names)
    films = [v for k, v in task.items() if k != PROCESS]
    if task.get(PROCESS, 0) > max(films, default=0):   # a film's task that also cites a proposal stays the film's
        return PROCESS
    count = {}
    for raw in open(transcript, encoding='utf-8', errors='replace'):
        if '"tool_use"' in raw:
            _jobs(raw, names, count)
    if count.get('morning-report') or task.get('morning-report'):   # overnight builds and tests are recorded
        return 'morning-report'                   # apart from the films they test on (a Remakes bench was billed to Remakes)
    if task:
        return max(task, key=task.get)
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
    sid = this_sid()
    drop_elsewhere(film, sid, chat)
    d = load(film)
    try:                                          # history-and-search Learn (Sam's 1, 16 Nov): steps, history at
        import stepcost                           # the end, and cost by kind of step, on every chat's row
        meas = stepcost.measure(transcript, film)
    except Exception:
        meas = None
    real = next((c for c in d['chats'] if sid and c.get('sid') == sid and c.get('src') == 'app'), None)
    if real:                                      # the real figure is in already; an estimate never replaces it,
        if meas and meas['steps'] - real.get('steps', 0) >= 20:   # but its measure still grows
            _put_measure(real, meas)
            store(d)
            push_row(film, real)
        return
    old = next((c for c in d['chats'] if c['chat'] == chat), None)
    if old and abs(old['cost'] - cost) < 0.25:
        return
    row = dict(old or {'date': str(date.today()), 'chat': chat, 'stage': 'auto', 'round': None, 'notes': 0,
                       'repeats': []}, model=model, cost=cost, src='estimate', sid=sid)
    if meas:
        _put_measure(row, meas)
    try:                                          # cost audit (Sam, 21 Nov: "fix ... the notes problem"): counted, not typed
        n, maybe = count_notes(transcript, film)
        row['notes_auto'], row['notes'] = n, max(n, row.get('notes') or 0)
        if maybe:
            row['repeats_maybe'] = maybe
    except Exception:
        pass
    if old:
        d['chats'][d['chats'].index(old)] = row
    else:
        d['chats'].append(row)
    store(d)                                      # tracked quietly: no alarm (Sam, 26 Nov: the budget alarms deleted)
    push_row(film, row)                           # startup-fixes 1 (Sam, 16 Nov): straight onto the main line


def drop_elsewhere(film, sid, chat):
    """One chat, one ledger (Sam, 16 Nov): this chat's estimate rows under any other film are taken out, here and on
    the main line, so a chat whose billing moved is never counted twice. The app's real figures are left alone."""
    import glob
    import subprocess
    import mainline
    me = {'sid': sid, 'chat': chat}
    mine = lambda c: same_row(c, me) and c.get('src') != 'app'
    for f in sorted(glob.glob(os.path.join(DIR, '*.json'))):
        other = os.path.splitext(os.path.basename(f))[0]
        if other == film:
            continue
        try:
            d = json.load(open(f))
        except (ValueError, OSError):
            continue
        if not isinstance(d, dict) or not any(mine(c) for c in d.get('chats', [])):
            continue

        def cut(x):
            n = len(x.get('chats', []))
            x['chats'] = [c for c in x.get('chats', []) if not mine(c)]
            return len(x['chats']) != n
        cut(d)
        store(d)
        up, _ = _ledger_updates(other, cut)
        mainline.to_main(up, root=ROOT, msg=f'Ledger: {other}, chat {chat} moved to {film} (automatic)')
        j, md, _ = _paths(other)
        subprocess.run(['git', '-C', ROOT, 'add', j, md], capture_output=True)
        subprocess.run(['git', '-C', ROOT, 'commit', '-q', '-m', f'Ledger: {other}, chat {chat} moved to {film}',
                        '--', j, md], capture_output=True)
        print(f'ledger auto: chat {chat} was also under {other}; taken out there (billed to {film})', file=sys.stderr)


def same_row(a, b):
    """One chat's row twice: the same app session id, or the same transcript id."""
    return bool(a.get('sid') and a.get('sid') == b.get('sid')) or a.get('chat') == b.get('chat')


def better(a, b):
    """Of two rows for one chat: the app's real figure, else the larger running cost; measures kept from either."""
    if (a.get('src') == 'app') != (b.get('src') == 'app'):
        win, lose = (a, b) if a.get('src') == 'app' else (b, a)
    elif a.get('src') == 'app' and 'usd' in a and 'usd' in b:   # two reads of the app: the later (larger) dollar
        win, lose = (a, b) if a['usd'] >= b['usd'] else (b, a)   # figure, its % at today's week price (the old
        win = dict(win, cost=_pct(win['usd']))                   # branches priced a week lower: 0.27 vs 0.19)
    else:
        win, lose = (a, b) if a.get('cost', 0) >= b.get('cost', 0) else (b, a)
    win = dict(win)
    if lose.get('steps', 0) > win.get('steps', 0):
        win.update({k: lose[k] for k in ('steps', 'hist_k', 'kinds', 'calls', 'split', 'start') if k in lose})
    return win


def _pct(usd):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.claude', 'hooks'))
    import costwatch
    return round(usd / costwatch.WEEK_USD * 100, 2)


def merge_row(d, row):
    """Puts one row into a ledger: replaces the same chat's row (never an app row by an estimate), or adds it.
    An estimate row with no app session id is left out once the film has app rows from that date (app_import drops
    those as the same chats under the transcript's id; F3: no chat counted twice). True if the ledger changed."""
    old = next((c for c in d['chats'] if same_row(c, row)), None)
    if old is None:
        if not row.get('sid') and row.get('src') != 'app' and not row.get('keep') and any(
                c.get('src') == 'app' and c['date'] <= row['date'] for c in d['chats']):
            return False
        d['chats'].append(row)
        d['chats'].sort(key=lambda c: c['date'])
        return True
    new = better(old, row)
    if new == old:
        return False
    d['chats'][d['chats'].index(old)] = new
    return True


def union(a, b):
    """Two copies of one film's ledger as one: every chat's row once (merge_row); everything else is a's (never
    brought back from b: a key a later chat removed, like Blessed's alarms_off, stays removed)."""
    out = json.loads(json.dumps(a))
    out.setdefault('chats', [])
    for row in b.get('chats', []):
        merge_row(out, row)
    return out


def _ledger_updates(film, change):
    """to_main updates for one film: its .json changed by change(d) on the main line's copy, its .md written from it."""
    j, md, _ = _paths(film)
    rj, rmd = os.path.relpath(j, ROOT), os.path.relpath(md, ROOT)
    box = {}

    def fj(old):
        d = json.loads(old) if old else {'film': film, 'estimate': None, 'chats': [], 'checks': {}}
        if not change(d):
            return None
        box['d'] = d
        return json.dumps(d, indent=1)
    return {rj: fj, rmd: lambda old: render(box['d']) if 'd' in box else None}, box


def push_row(film, row):
    """This chat's row onto the main line as its own commit (mainline.to_main); the chat's HEAD is never pushed.
    The main line's merged copy is then written here too and committed alone (only these two files), so the chat's
    branch stays clean and later merges go row by row (the ledger merge driver)."""
    import subprocess
    import mainline
    up, box = _ledger_updates(film, lambda d: merge_row(d, row))
    res = mainline.to_main(up, root=ROOT,
                           msg=f'Ledger: {film}, chat {row["chat"]} at {row["cost"]}% of a week (automatic)')
    if res is None:
        print(f'ledger auto: the row for {film} could not reach the main line (3 tries); it is kept here',
              file=sys.stderr)
    mainline.config(ROOT)
    if any(os.path.exists(os.path.join(ROOT, '.git', x)) for x in ('MERGE_HEAD', 'rebase-merge', 'rebase-apply')):
        return res                                # mid-merge: the chat's own next commit carries it
    if 'd' in box:
        store(union(box['d'], load(film)))
    j, md, _ = _paths(film)
    git = lambda *a: subprocess.run(['git', '-C', ROOT] + list(a), capture_output=True, text=True, timeout=60)
    git('add', j, md)
    git('commit', '-q', '-m', f'Ledger: {film}, chat {row["chat"]} (automatic, also on the main line)', '--', j, md)
    return res


def _branch_ledgers(root=None, remote='origin'):
    """Every ledger file on every branch tip: {path: [text, ...]}, each distinct copy once."""
    import subprocess
    root = root or ROOT
    git = lambda *a: subprocess.run(['git', '-C', root] + list(a), capture_output=True, text=True, timeout=60)
    tips = git('for-each-ref', '--format=%(objectname)', f'refs/remotes/{remote}/').stdout.split()
    blobs = {}
    for t in set(tips):
        for ln in git('ls-tree', t, 'notes/ledger/').stdout.splitlines():
            meta, path = ln.split('\t', 1)
            if path.endswith('.json') or path == 'notes/ledger/app-costs.tsv':
                blobs.setdefault(path, set()).add(meta.split()[2])
    return {p: [git('cat-file', 'blob', b).stdout for b in sorted(bs)] for p, bs in blobs.items()}


def _tsv_union(a, b):
    """app-costs.tsv: a's lines, then b's rows for sessions a lacks."""
    have = {ln.split('\t')[1] for ln in a.splitlines() if ln.strip() and not ln.startswith('#') and '\t' in ln}
    add = [ln for ln in b.splitlines() if ln.strip() and not ln.startswith('#') and '\t' in ln
           and ln.split('\t')[1] not in have]
    return a if not add else a.rstrip('\n') + '\n' + '\n'.join(add) + '\n'


def _main_ids(root, remote):
    """{sid or transcript id: ledger path} for every row on the main line, any film (a chat filed under another
    film there, e.g. a Blessed chat moved to cost-diagnosis, is not brought back under the first; F3)."""
    import subprocess
    import mainline
    ref = f'refs/remotes/{remote}/{mainline.MAIN}'
    git = lambda *a: subprocess.run(['git', '-C', root] + list(a), capture_output=True, text=True, timeout=60)
    ids = {}
    for ln in git('ls-tree', '--name-only', ref, 'notes/ledger/').stdout.split():
        if ln.endswith('.json'):
            try:
                for c in json.loads(git('show', f'{ref}:{ln}').stdout).get('chats', []):
                    for k in (c.get('sid'), c.get('chat')):
                        if k:
                            ids.setdefault(k, ln)
            except (ValueError, AttributeError):
                pass
    return ids


def _claim(ids, found):
    """Chats on no main-line ledger but under two films on the branches go to the copy with the larger running cost
    (the later write: 1f73e167 was re-filed from blessed to cost-diagnosis); added to ids."""
    best = {}
    for path, texts in found.items():
        for t in texts if path.endswith('.json') else ():
            try:
                rows = json.loads(t).get('chats', [])
            except ValueError:
                continue
            for c in rows:
                k = c.get('sid') or c.get('chat')
                if k and k not in ids and c.get('cost', 0) >= best.get(k, ('', -1))[1]:
                    best[k] = (path, c.get('cost', 0))
    for k, (path, _) in best.items():
        ids[k] = path
    return ids


def _elsewhere(ids, path):
    """A filter for rows held on the main line under another film's ledger."""
    return lambda c: any(ids.get(k) not in (None, path) for k in (c.get('sid'), c.get('chat')) if k)


def missing(root=None, remote='origin'):
    """Rows held on some branch but not on the main line: {path: [chat, ...]} (`audit`; 0 is the aim at film end)."""
    import subprocess
    import mainline
    root = root or ROOT
    out = {}
    found = _branch_ledgers(root, remote)
    ids = _claim(_main_ids(root, remote), found)
    for path, texts in found.items():
        away = _elsewhere(ids, path)
        r = subprocess.run(['git', '-C', root, 'show', f'refs/remotes/{remote}/{mainline.MAIN}:{path}'],
                           capture_output=True, text=True)
        main = r.stdout if r.returncode == 0 else ''
        for t in texts:
            if path.endswith('.tsv'):
                extra = _tsv_union('' if not main else main, t)[len(main):]
                lost = [ln.split('\t')[1][-8:] for ln in extra.splitlines() if ln.strip()]
            else:
                try:
                    d, m = json.loads(t), json.loads(main) if main else {'chats': []}
                except ValueError:
                    continue
                lost = [c['chat'] for c in d.get('chats', []) if not away(c) and merge_row(m, dict(c))]
            for x in lost:
                if x not in out.setdefault(path, []):
                    out[path].append(x)
    return {p: v for p, v in out.items() if v}


def gather(root=None, remote='origin'):
    """One-off (startup-fixes 1): every row stranded on a branch onto the main line, each chat once (matched on the
    app session id first, across all branches; F3). Returns {path: rows added}."""
    import mainline
    root = root or ROOT
    found = _branch_ledgers(root, remote)
    ids = _claim(_main_ids(root, remote), found)
    added = {}

    def fn_for(path, texts):
        def fn(old):
            if path.endswith('.tsv'):
                new = old or ''
                for t in texts:
                    new = _tsv_union(new, t)
                added[path] = len(new.splitlines()) - len((old or '').splitlines())
                return new if added[path] else None
            d = json.loads(old) if old else None
            n0 = len(d['chats']) if d else 0
            for t in texts:
                try:
                    b = json.loads(t)
                except ValueError:
                    continue
                away = _elsewhere(ids, path)
                b['chats'] = [c for c in b.get('chats', []) if not away(c)]
                d = union(d, b) if d else b
            new = box[path] = json.dumps(d, indent=1)
            added[path] = len(d['chats']) - n0 or (new != old and 'updated')
            return new if new != old else None
        return fn
    ups = {p: fn_for(p, ts) for p, ts in found.items()}
    for p in [p for p in ups if p.endswith('.json')]:          # each film's .md written from its gathered .json
        def md(old, p=p):
            new = render(json.loads(box[p])) if p in box else None
            return new if new != old else None
        ups[p[:-5] + '.md'] = md
    box = {}
    res = mainline.to_main(ups, 'Ledger: stranded cost rows from every branch, each chat once (startup-fixes 1)',
                           root=root, remote=remote)
    return res, {p: n for p, n in added.items() if n}


def mergefile(o, a, b, path):
    """git's merge driver for the ledger (.gitattributes): rows from both sides, each chat once; .md written from
    ours (the next row pushed rewrites it from the
    .json); app-costs.tsv by session. Exit 0 (never a clash)."""
    ta, tb = open(a, encoding='utf-8').read(), open(b, encoding='utf-8').read()
    if path.endswith('.json'):
        try:
            out = json.dumps(union(json.loads(ta), json.loads(tb)), indent=1)
        except ValueError:
            return 1
    elif path.endswith('.tsv'):
        out = _tsv_union(ta, tb)
    else:
        out = ta
    open(a, 'w', encoding='utf-8').write(out)
    return 0


NOT_A_NOTE = re.compile(r'^\W*(y|n|yes|no|go|ok|okay|override|thanks?|thank you|hold|just go|\d{1,2}\s*[yn]?)\W*$', re.I)
STOP = set('the a an to of and is it in on that this for be with as at not but are was i you he she they them his her '
           'its my me do does so if or from have has can will would should there what when then than now just also '
           'one all any more very too please make made keep still again'.split())


def _words(t):
    return {w for w in re.findall(r"[a-z']{3,}", t.lower()) if w not in STOP}


def count_notes(transcript, film):
    """Sam's notes in this chat, counted from his own typed messages (the chat record): each numbered item is one
    note; a message with none is one note, unless it is only a yes/no/go/number answer or a question. Possible
    repeats: a note sharing at least 60% of its words (and 4 or more) with a line of the film's notes written before
    this chat. Returns (count, [possible repeats, short])."""
    import handover
    msgs = [t for _, t in handover.sam_messages(transcript)]
    notes = []
    for m in msgs:
        m = m.strip()
        if not m or NOT_A_NOTE.match(m) or (m.endswith('?') and '\n' not in m):
            continue
        items = re.split(r'(?m)^\s*\d{1,2}\s*[.):-]\s+', m)
        items = [x.strip() for x in items if len(x.strip()) > 3]
        notes += items if len(items) > 1 else [m]
    past = []
    for f in (os.path.join(ROOT, 'notes', film + '.md'), os.path.join(ROOT, 'notes', 'archive', film + '-handovers.md'),
              os.path.join(ROOT, 'notes', 'archive', film + '-notes.md')):    # ticked notes move here (GTA chat 27)
        try:
            past += [ln for ln in open(f, encoding='utf-8') if len(ln) > 30]
        except OSError:
            pass
    pw = [(ln, _words(ln)) for ln in past]
    maybe = []
    for n in notes:
        w = _words(n)
        if len(w) < 4:
            continue
        best = max((len(w & q) / len(w) for _, q in pw), default=0)
        if best >= 0.6 and not any(n[:40] in ln for ln, _ in pw):     # the note copied in this chat is not a repeat
            maybe.append(n[:90])
    return len(notes), maybe


def _put_measure(row, m):
    """stepcost's figures onto a ledger row: steps, history at the end (k tokens), each kind's share of the chat (%)."""
    row.update(steps=m['steps'], hist_k=m['hist'] // 1000, kinds=m['kinds'], calls=m['calls'])
    if m.get('split'):                            # cost-other change 1 (Sam's Y, 19 Nov): the exact split
        row['split'] = m['split']
    if m.get('start'):                            # cold-start change (Sam's Y, 19 Nov): four start figures
        row['start'] = m['start']
    if m.get('search'):                           # finder-use Learn (Sam's 1, 17 Nov): the chat's search record
        row['search'] = m['search']


def this_sid():
    """This chat's id in the app ('session_...'), from the cloud session's environment; None elsewhere."""
    r = os.environ.get('CLAUDE_CODE_REMOTE_SESSION_ID', '')
    return 'session_' + r.split('_', 1)[1] if '_' in r else None


APP = os.path.join(DIR, 'app-costs.tsv')


def app_import(path=APP):
    """The real record: app-costs.tsv rows (film, session, created, title, cost_usd, ...) become each film's rows
    (src 'app', cost in % of a week at costwatch.WEEK_USD). Replaced: the film's rows for the same session, and its
    estimate rows dated on or after its first app row (they are the same chats, under the transcript's id), except
    rows marked keep (chats the app cannot show, e.g. from Sam's earlier account). Returns {film: (rows, % total)}."""
    sys.path.insert(0, os.path.join(ROOT, '.claude', 'hooks'))
    import costwatch
    rows = {}
    for ln in open(path, encoding='utf-8'):
        if not ln.strip() or ln.startswith('#'):
            continue
        f = ln.rstrip('\n').split('\t')
        rows.setdefault(f[0], []).append(f)
    out = {}
    for film, rs in rows.items():
        d = load(film)
        first = min(r[2][:10] for r in rs)
        sids = {'session_' + r[1] for r in rs}
        meas = {c['sid']: c for c in d['chats'] if c.get('sid') in sids and c.get('steps')}  # kept onto the app row
        d['chats'] = [c for c in d['chats'] if c.get('keep') or (c.get('sid') not in sids and
                      (c.get('src') == 'app' or c['date'] < first))]
        have = {c.get('sid'): c for c in d['chats']}
        for r in rs:
            sid = 'session_' + r[1]
            row = have.get(sid) or {'notes': 0, 'repeats': [], 'round': None}
            row.update(date=r[2][:10], chat=r[1][-8:], sid=sid, src='app', stage=r[3][:60],
                       model=r[9], cost=round(float(r[4]) / costwatch.WEEK_USD * 100, 2), usd=float(r[4]))
            if sid in meas and not row.get('steps'):
                row.update({k: meas[sid][k] for k in ('steps', 'hist_k', 'kinds', 'calls', 'search', 'split', 'start') if k in meas[sid]})
            if sid not in have:
                d['chats'].append(row)
        d['chats'].sort(key=lambda c: c['date'])
        store(d)
        out[film] = (len(rs), totals(d)[0])
    return out


CHECK = os.path.join(DIR, 'app-check.tsv')
GAP = 0.25


def estimate_parts(transcript):
    """This chat's own estimate in dollars, split: the main chat, its helpers (critique and other agents), and other
    records in this machine's chat folder (a restart that began a new record)."""
    sys.path.insert(0, os.path.join(ROOT, '.claude', 'hooks'))
    import costwatch
    st, _ = costwatch.read_usage(transcript)
    others = 0.0
    for p in glob.glob(os.path.join(os.path.dirname(transcript), '*.jsonl')):
        if os.path.abspath(p) != os.path.abspath(transcript):
            try:
                others += costwatch.read_usage(p)[0]['usd']
            except Exception:
                pass
    return {'main': round(st['usd'], 3), 'helpers': round(st.get('helpers_usd', 0.0), 3), 'restarts': round(others, 3),
            'model': costwatch.fam(st.get('model'))}


def appcost(film, usd, transcript=None, sid=None, restarts=0, usage=None, check=CHECK, app=APP, today=None, est=None):
    """Cost-spike fix 7 (Sam's Y, 27 Nov; chat 36: estimated $4.71, the app said $12.50): at a chat's end the app's
    own figure (get_session: external_metadata.usage.cost_usd) goes into app-costs.tsv beside the estimate, and the
    chat is flagged when the estimate is more than 25% under it. Helpers and restarts are counted apart, so the gap
    says where the missing money went. Returns the line to print."""
    sid = (sid or this_sid() or '').replace('session_', '')
    est = est or estimate_parts(transcript)
    total = est['main'] + est['helpers'] + est['restarts']
    gap = (usd - total) / usd if usd > 0 else 0.0
    flag = gap > GAP
    day = today or str(date.today())
    u = usage or {}
    row = [film, sid, day + 'T' + datetime.now().strftime('%H:%M'), 'chat end (appcost)', f'{usd:.3f}',
           f"{u.get('cache_read_tokens', 0) / 1e6:.3f}", f"{u.get('cache_write_tokens', 0) / 1e6:.3f}",
           f"{u.get('output_tokens', 0) / 1e3:.1f}", '', est['model']]
    lines = open(app, encoding='utf-8').read().splitlines() if os.path.exists(app) else []
    lines = [ln for ln in lines if ln.startswith('#') or ln.split('\t')[1:2] != [sid]]
    lines.append('\t'.join(row))
    with open(app, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    head = '# date\tsession\tfilm\tapp_usd\testimate_usd\tmain\thelpers\trestart_records\trestarts_app\tgap\tflag\n'
    old = open(check, encoding='utf-8').read().splitlines()[1:] if os.path.exists(check) else []
    old = [ln for ln in old if ln.split('\t')[1:2] != [sid]]
    old.append('\t'.join([day, sid, film, f'{usd:.2f}', f'{total:.2f}', f"{est['main']:.2f}", f"{est['helpers']:.2f}",
                          f"{est['restarts']:.2f}", str(restarts), f'{gap:.0%}', 'UNDER' if flag else 'ok']))
    with open(check, 'w', encoding='utf-8') as f:
        f.write(head + '\n'.join(old) + '\n')
    split = f"main ${est['main']:.2f}, helpers ${est['helpers']:.2f}, other records ${est['restarts']:.2f}" + \
        (f', {restarts} restart(s) by the app' if restarts else '')
    if flag:
        return (f'COST GAP: the estimate (${total:.2f}: {split}) is {gap:.0%} under the app\'s own figure '
                f'(${usd:.2f}). The missing part is what no record here shows (restarts on another machine, a model '
                'switch, helpers the app bills apart); the app figure is the one that counts.')
    return f'ledger appcost: app ${usd:.2f}, estimate ${total:.2f} ({split}); within {GAP:.0%}'


def appcost_faults(sid=None, check=CHECK):
    """handover.py end: a cloud chat with no app figure recorded (ledger.py appcost) is a fault."""
    sid = (sid or this_sid() or '').replace('session_', '')
    if not sid:
        return []
    rows = open(check, encoding='utf-8').read().splitlines() if os.path.exists(check) else []
    if any(r.split('\t')[1:2] == [sid] for r in rows):
        return []
    return ['COST: this chat has no app cost figure on record (cost-spike fix 7): call get_session (no id), then '
            'python3 source/ledger.py appcost FILM COST_USD --restarts N (cost_usd from external_metadata.usage, N = '
            'worker_epoch - 1)']


def appcost_test():
    """The fault, saved as an example: chat 36 (Brexit, 26 Nov) was estimated at $4.71 and the app said $12.50."""
    import tempfile
    d = tempfile.mkdtemp()
    chk, app = os.path.join(d, 'check.tsv'), os.path.join(d, 'app.tsv')
    open(app, 'w').write('# film\tsession\tcreated\ttitle\tcost_usd\tcache_read_M\tcache_write_M\toutput_k\thistory_k\tmodel\n')
    est = {'main': 4.21, 'helpers': 0.5, 'restarts': 0.0, 'model': 'opus'}
    bad = []
    if appcost_faults('session_x36', chk) == []:
        bad.append('a chat with no app figure was not flagged')
    a = appcost('brexit-is-done', 12.50, sid='session_x36', restarts=5, check=chk, app=app, est=est)
    if not a.startswith('COST GAP') or '62%' not in a or '5 restart' not in a:
        bad.append('chat 36 not flagged: ' + a)
    b = appcost('brexit-is-done', 4.90, sid='session_x37', check=chk, app=app, est=est)
    if 'within' not in b:
        bad.append('a close estimate was flagged: ' + b)
    appcost('brexit-is-done', 13.0, sid='session_x36', restarts=5, check=chk, app=app, est=est)  # a later read
    rows = [r for r in open(chk).read().splitlines() if not r.startswith('#')]
    apps = [r for r in open(app).read().splitlines() if not r.startswith('#')]
    if len(rows) != 2 or len(apps) != 2 or not any('13.000' in r for r in apps) or appcost_faults('x36', chk):
        bad.append(f'rows {rows} / {apps}')
    return not bad, '; '.join(bad) or 'chat 36 flagged (62% under, 5 restarts named); a close one passes; one row a chat'


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
    with no share."""
    spent = totals(d)[0]
    st = d.setdefault('stages', [])
    s = next((x for x in st if x['name'] == name and x['done'] is None), None)
    if s is None:
        s = {'name': name, 'pct': 0.0, 'done': None, 'unplanned': True}
        last = max([i for i, x in enumerate(st) if x['done'] is not None], default=-1)
        st.insert(last + 1, s)
    s['done'] = {'date': str(date.today()), 'spent': spent}
    return s


def compare_line(d):
    """Rule 24 (Sam, 13 Nov): after the film, one line: its real cost against the last three films' (ledgers with an
    estimate, by their last chat before this film's). Returns (line, over 1.5x their average)."""
    spent = totals(d)[0]
    last = max((c['date'] for c in d['chats']), default='')
    past = []
    for f in glob.glob(os.path.join(DIR, '*.json')):
        o = json.load(open(f))
        if o.get('film') == d['film'] or o.get('estimate') is None or not o['chats']:
            continue
        end = max(c['date'] for c in o['chats'])
        if end < last:                            # ended before this film's last chat (not one still running)
            past.append((end, o['film'], totals(o)[0]))
    past = sorted(past)[-3:]
    if not past:
        return f"{d['film']}: {spent}% of a week; no earlier film to compare.", False
    avg = sum(x[2] for x in past) / len(past)
    over = spent > 1.5 * avg
    return (f"{d['film']}: {spent}% of a week, against the last {len(past)} films' average {avg:.1f}% ("
            + ', '.join(f'{n} {v}' for _, n, v in past) + f"): {spent / avg:.1f}x"
            + ('. OVER 1.5x: the next chat finds why before any film work.' if over else '.')), over


def totals(d):
    spent = round(sum(c['cost'] for c in d['chats']), 2)
    rounds = max([c['round'] for c in d['chats'] if c['round']] + [current()[1] or 0 if current()[0] == d['film'] else 0])
    notes = sum(c['notes'] for c in d['chats'])
    reps = [r for c in d['chats'] for r in c['repeats']]
    return spent, rounds, notes, reps


def coldstart(d):
    """cold-start change (Sam's Y, 19 Nov): the film-end line. Each chat's start (its cost up to the first real work)
    plus its re-learning (re-reading files the film's previous chat also read before ITS first real work), as % of
    the film. Checked against the app: a chat with the app's figure has its measured dollars set beside it."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.claude', 'hooks'))
    import costwatch                  # the real hooks folder (a kit test's copied ROOT has none: it passed only when
                                      # an earlier test had loaded costwatch; kit-tests-per-film run, 25 Nov)
    rows = [c for c in d['chats'] if c.get('start')]
    if not rows:
        return None
    spent = sum(c['cost'] for c in d['chats']) or 1
    st = rl = 0.0
    prev = set()
    for c in rows:
        s_ = c['start']
        st += s_.get('work_pct') or 0
        mine = {f: u for f, _, u in s_.get('reads', [])}
        rl += 100 * sum(u for f, u in mine.items() if f in prev) / costwatch.WEEK_USD
        prev = set(mine)
    app = [c for c in rows if c.get('src') == 'app' and (c.get('split') or {}).get('total')]
    chk = ''
    if app:
        meas = sum(100 * c['split']['total'] / costwatch.WEEK_USD for c in app)
        real = sum(c['cost'] for c in app)
        chk = (f"; checked against the app on {len(app)} chats: measured {meas:.2f}% vs app {real:.2f}% "
               f"({100 * (meas - real) / real:+.0f}%)" if real else '')
    per = (st + rl) / len(rows)
    base = sum(c['start'].get('base_pct', 0) for c in rows) / len(rows)
    flag = (' Over 0.5% a chat: a warm handover goes to Sam through the proposal route.' if per > 0.5 else '')
    return (f"A new chat's start and re-learning cost {100 * (st + rl) / spent:.0f}% of the film "
            f"({st + rl:.2f}% of a week over {len(rows)} chats: start {st:.2f}, re-learning {rl:.2f}; "
            f"{per:.2f}% a chat; step-1 context re-read is {base:.0f}% of a chat on average){chk}.{flag}")


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
        out += ['**Stages (tracked quietly):**', '', '| stage | planned % | done | spent at its end |',
                '|---|---|---|---|']
        out += [f"| {x['name']}{' (unplanned)' if x.get('unplanned') else ''} | {x['pct']:g} | "
                f"{x['done']['date'] if x['done'] else ''} | {x['done']['spent'] if x['done'] else ''} |"
                for x in d['stages']]
        out += ['']
    out += ["Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate "
            '(chats the app cannot show, or not yet imported with `ledger.py app`).', '']
    out += ['| date | chat | source | model | stage | round | cost % | $ | notes | repeated |',
            '|---|---|---|---|---|---|---|---|---|---|']
    out += [f"| {c['date']} | {c['chat']} | {'app' if c.get('src') == 'app' else 'est'} | {c['model']} | "
            f"{c['stage']} | {c['round'] or ''} | {c['cost']} | {c.get('usd', '')} | {c['notes']} | "
            f"{len(c['repeats'])} |" for c in d['chats']]
    meas = [c for c in d['chats'] if c.get('steps')]
    if meas:                                      # history-and-search Learn (16 Nov): where each chat's cost went
        out += ['', '## Cost by kind of step (share of each chat; measured from its transcript)']
        out += [f"- {c['date']} {c['chat']} ({c['stage']}): {c['steps']} steps, history {c['hist_k']}k at the end; "
                + ', '.join(f'{k} {v:g}%' for k, v in sorted(c['kinds'].items(), key=lambda kv: -kv[1]))
                for c in meas]
    sps = [c for c in d['chats'] if c.get('split')]
    if sps:                                       # cost-other change 1 (19 Nov): exact split, leftover under 5%
        import stepcost
        out += ['', '## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)']
        out += [f"- {c['date']} {c['chat']} ({c['stage']}): " + stepcost.split_line(c['split']) for c in sps]
    cs = coldstart(d)
    if cs:                                        # cold-start change (19 Nov): the film-end line
        out += ['', '## Starting each chat', cs]
        out += [f"- {c['date']} {c['chat']}: step-1 context {c['start']['floor_k']}k; first real work at step "
                f"{c['start']['work_step']} ({c['start']['work_pct']}% of a week); read before it: "
                + ', '.join(f'{f} {k:g}k' for f, k, _ in c['start'].get('reads', [])[:6])
                for c in d['chats'] if c.get('start')]
    if reps:
        out += ['', '## Repeated notes (what would have caught them)']
        out += [f'- {r}' for r in reps]
    if d['checks']:
        out += ['', '## Checks (runs, faults, by kind)']
        for n, c in sorted(d['checks'].items()):
            kinds = ', '.join(f'{k} {v}' for k, v in sorted(c['kinds'].items(), key=lambda kv: -kv[1]))
            out.append(f"- {n}: {c['runs']} runs, {c['faults']} faults" + (f' ({kinds})' if kinds else ''))
    if d.get('compare'):
        out += ['', '## After the film', d['compare']]
    return '\n'.join(out) + '\n'


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

SESS = re.compile(r'session_[A-Za-z0-9]{24}')


def film_sessions(film):
    """The chats a film's own handovers name as its chats: every "where things stand (chat N, ..., session_X)" line in
    notes/FILM.md and notes/archive/FILM-handovers.md."""
    out = []
    for f in (os.path.join(ROOT, 'notes', film + '.md'), os.path.join(ROOT, 'notes', 'archive', film + '-handovers.md')):
        if not os.path.exists(f):
            continue
        for line in open(f, encoding='utf-8', errors='replace'):
            if 'where things stand' in line.lower():
                out += [m for m in SESS.findall(line) if m not in out]
    return out


def misfiled(film, ledgers=None):
    """[(other ledger, row)] for the film's own chats (film_sessions) whose estimate row sits under another ledger
    (pose-kit-format C1). ledgers: {name: dict} to test on a saved copy; default the files in notes/ledger/."""
    import glob
    mine = set(film_sessions(film))
    if ledgers is None:
        ledgers = {}
        for f in sorted(glob.glob(os.path.join(DIR, '*.json'))):
            try:
                ledgers[os.path.splitext(os.path.basename(f))[0]] = json.load(open(f))
            except (ValueError, OSError):
                pass
    out = []
    for name, d in ledgers.items():
        if name == film or not isinstance(d, dict):
            continue
        out += [(name, c) for c in d.get('chats', []) if c.get('sid') in mine and c.get('src') != 'app']
    return out


def rebook(film):
    """Move every misfiled row to the film's own ledger (taken out of the other, on the main line too); a row already
    in the film's ledger for the same chat is kept (the double-booked one is only taken out elsewhere)."""
    import subprocess
    import mainline
    moved = misfiled(film)
    for other, row in moved:
        drop = lambda x, row=row: _cut(x, row)
        d = load(other)
        drop(d)
        store(d)
        up, _ = _ledger_updates(other, drop)
        mainline.to_main(up, root=ROOT, msg=f'Ledger: {other}, chat {row["chat"]} rebooked to {film}')
        j, md, _ = _paths(other)
        subprocess.run(['git', '-C', ROOT, 'add', j, md], capture_output=True)
        subprocess.run(['git', '-C', ROOT, 'commit', '-q', '-m', f'Ledger: {other}, chat {row["chat"]} rebooked to {film}',
                        '--', j, md], capture_output=True)
        here = load(film)
        if not any(same_row(c, row) for c in here['chats']):
            push_row(film, row)
    return moved


def _cut(x, row):
    n = len(x.get('chats', []))
    x['chats'] = [c for c in x.get('chats', []) if not same_row(c, row)]
    return len(x['chats']) != n


def main():
    a = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    s = a.add_subparsers(dest='cmd', required=True)
    p = s.add_parser('estimate'); p.add_argument('film'); p.add_argument('pct', type=float)
    p.add_argument('--stages', help='"cast 2, sets 2.5, board 0.5, moves 3, animatic1 1, round 1.5, final 0.5"')
    p = s.add_parser('stage'); p.add_argument('film'); p.add_argument('name')
    p = s.add_parser('round'); p.add_argument('film'); p.add_argument('n', type=int)
    p = s.add_parser('save'); p.add_argument('film'); p.add_argument('path'); p.add_argument('text', nargs='?')
    p = s.add_parser('note'); p.add_argument('film'); p.add_argument('text')
    p = s.add_parser('log'); p.add_argument('film'); p.add_argument('--stage', default='')
    p.add_argument('--notes', type=int, default=0)
    p.add_argument('--repeat', action='append', default=[], help='"the note | what would have caught it"')
    p = s.add_parser('audit'); p.add_argument('film', nargs='?')
    s.add_parser('gather', help='one-off: rows stranded on branches onto the main line, each chat once')
    p = s.add_parser('mergefile'); [p.add_argument(x) for x in ('o', 'a', 'b', 'path')]
    s.add_parser('kept')
    s.add_parser('auto')
    p = s.add_parser('coldstart', help='the film-end line: what starting new chats cost the film')
    p.add_argument('film')
    p = s.add_parser('rebook', help='move the film\'s own chats (named in its handovers) from other ledgers to it')
    p.add_argument('film'); p.add_argument('--dry', action='store_true')
    s.add_parser('app', help='rebuild film rows from notes/ledger/app-costs.tsv (the app\'s real per-chat costs)')
    p = s.add_parser('appcost', help='at a chat\'s end: the app\'s own figure beside the estimate (cost-spike fix 7)')
    p.add_argument('film'); p.add_argument('usd', type=float); p.add_argument('--restarts', type=int, default=0)
    p.add_argument('--read', type=float, default=0); p.add_argument('--write', type=float, default=0)
    p.add_argument('--out', type=float, default=0)
    o = a.parse_args()
    if o.cmd == 'coldstart':
        print(coldstart(load(o.film)) or f'ledger coldstart: {o.film} has no start figures yet (recorded from 19 Nov)')
        return
    if o.cmd == 'rebook':
        rows = misfiled(o.film) if o.dry else rebook(o.film)
        for other, r in rows:
            print(f'ledger rebook: {o.film} chat {r["chat"]} ({r.get("cost")}%) {"is under" if o.dry else "moved from"} {other}')
        tot = sum(c.get('cost') or 0 for c in load(o.film)['chats'])
        print(f'ledger rebook: {len(rows)} rows; {o.film} now {round(tot, 2)}% of a week on its own record')
        return
    if o.cmd == 'appcost':
        import handover
        print(appcost(o.film, o.usd, handover.this_record(), restarts=o.restarts,
                      usage={'cache_read_tokens': o.read, 'cache_write_tokens': o.write, 'output_tokens': o.out}))
        return
    if o.cmd == 'app':
        for film, (n, pct) in app_import().items():
            print(f'ledger: {film}: {n} chats from the app; film total now {pct}% of a week')
        return
    if o.cmd == 'mergefile':
        sys.exit(mergefile(o.o, o.a, o.b, o.path))
    if o.cmd == 'gather':
        res, added = gather()
        for p_, n in added.items():
            print(f'ledger gather: {p_}: {n} rows' + ('' if n == 'updated' else ' added'))
        print(f'ledger gather: {res or "could not push"}')
        return
    if o.cmd == 'audit':                          # startup-fixes 1: rows a branch holds and the main line lacks
        lost = missing()
        if o.film:
            lost = {p_: v for p_, v in lost.items() if os.path.basename(p_).split('.')[0] in (o.film, 'app-costs')}
        n = sum(len(v) for v in lost.values())
        print(f'ledger audit: {n} rows missing from the main line' + ''.join(
            f'\n  {p_}: {", ".join(v)}' for p_, v in lost.items()) + (' (fix: ledger.py gather)' if n else ''))
        if not o.film:
            return
    if o.cmd == 'kept':
        print('\n'.join(kept_lines()))
        return
    if o.cmd == 'auto':                           # the Stop hook: its JSON (with the transcript's path) on stdin
        __import__('hookran').ran('ledger.py auto')
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
                  + (f' (scaled to {o.pct}%)' if abs(plan - o.pct) > 0.05 else ''))
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
        d['compare'], over = compare_line(d)
        d.pop('audit', None)
        print(d['compare'])
    store(d)


if __name__ == '__main__':
    main()
