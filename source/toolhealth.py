#!/usr/bin/env python3
"""toolhealth: is every essential tool still reaching all it should? (R14; Sam, 26 Nov, chat R12: "In light of
learning that this essential tool was only slightly working (just like the communication tool), how can I know if all
essential tools are working?", then "Y" to building it.)

Why: the code finder and the plain-words checker both passed their own tests on frozen old examples while the project
grew round them (code moved into shared files; new kinds of messages), so each did only part of its job. The watcher
checks a tool is switched on and ran; this checks it still COVERS everything, two ways per tool:
  reach ... computed from the project as it is now (the files a film imports, the hooks in the settings, the ways
            text reaches Sam), never a frozen example, so it moves when the project moves;
  use ..... the last week's real records (Sam's saved messages, the code finder's log, the cost records, the git
            history, the plain-words log) scored against what actually happened.
Each gives ('ok' | 'partly' | 'broken' | 'missing', plain words on what it misses). The report is one plain line
per tool for Sam: working / partly (what it misses) / broken / not built.

MAP
  Rec ............. the records, read once and lazily (git last 7 days, ledger rows, Sam's messages, show logs, plain-
                    words log, settings hooks); a kittest passes its own saved example in place of any part
  TOOLS ........... id, Sam's name, promise (one plain sentence), reach(R), use(R); R13 listed as not built
  check(R) ........ [(tool, reach, use, line)]; line() the one plain line for Sam
  at_start(film) .. kitfilm.at_start / begin: the report with the kit tests at a film's start, saved to
                    notes/logs/toolhealth.txt (and printed by handover start)

    python3 source/toolhealth.py            (the report, one line per tool)
    python3 source/toolhealth.py --why      (and each part's own finding)
"""
import glob, json, os, re, subprocess, sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, '.claude', 'hooks'))
MAIN = 'claude/create-claude-md-oe8z4g'
DAYS = 7
OUT = os.path.join(ROOT, 'notes', 'logs', 'toolhealth.txt')
RED_K = 370                                   # the cost watch's red line (thousand words of history)
CHAIN_RE = re.compile(r'First check you can (?:save|push) to GitHub|^\s*(?:Animation project|Open Wounds|Brexit Is Done)'
                      r'[^\n]{0,80}\bchat \w+\b.*\b(?:Opus|Sonnet)\b', re.I | re.S)
NOT_SAM_RE = re.compile(r'^\s*(?:<task-notification>|\[SYSTEM NOTIFICATION|<system-reminder>)'
                        r'|The following was sent by another Claude Code session')


def _git(*a):
    try:
        return subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True, timeout=60).stdout
    except (OSError, subprocess.TimeoutExpired):
        return ''


class Rec:
    """The real records, read on first use. Any attribute may be set beforehand (a kittest's saved example)."""
    def __init__(self, now=None, **given):
        self.now = now or datetime.now(timezone.utc)
        self.since = self.now - timedelta(days=DAYS)
        self.__dict__.update(given)

    def __getattr__(self, k):
        if k.startswith('_'):
            raise AttributeError(k)
        v = getattr(self, '_load_' + k)()
        setattr(self, k, v)
        return v

    def _load_commits(self):
        """[(hash, iso time, session tail (8), [files])] on every known branch, last 7 days."""
        out, cur = [], None
        for ln in _git('log', '--remotes', '--all', f'--since={self.since.isoformat()}', '--format=@@%H\t%cI\t%B%x00',
                       '--name-only').splitlines():
            if ln.startswith('@@'):
                h, t, body = (ln[2:].split('\t', 2) + ['', ''])[:3]
                cur = [h, t, '', []]
                out.append(cur)
                m = re.search(r'session_(\w+)', body)
                cur[2] = m.group(1)[-8:] if m else ''
            elif cur is not None:
                m = re.search(r'session_(\w+)', ln)
                if m and not cur[2]:
                    cur[2] = m.group(1)[-8:]
                elif ln.strip() and '\x00' not in ln and '/' in ln and not ln.startswith(' ') and os.sep != ln[0]:
                    if re.match(r'^[\w.-]+(/[\w.-]+)+$', ln.strip()):
                        cur[3].append(ln.strip())
        return out

    def _load_on_main(self):
        ref = 'origin/' + MAIN if _git('rev-parse', '--verify', '-q', 'origin/' + MAIN).strip() else 'HEAD'
        return set(_git('log', ref, f'--since={self.since.isoformat()}', '--format=%H').split())

    def _load_rows(self):
        """Every chat row in the cost records (all films) dated in the last 7 days, with its record's name."""
        out = []
        for f in glob.glob(os.path.join(ROOT, 'notes', 'ledger', '*.json')):
            try:
                d = json.load(open(f))
            except (OSError, ValueError):
                continue
            for r in d.get('chats', []) if isinstance(d, dict) else []:
                if isinstance(r, dict) and r.get('date', '') >= self.since.date().isoformat():
                    out.append(dict(r, record=os.path.basename(f)[:-5]))
        return out

    def _load_sam(self):
        """[(iso time, text, file)] of every saved message of Sam's in the last 7 days."""
        out = []
        for f in glob.glob(os.path.join(ROOT, 'notes', 'ledger', 'sam', '*.md')):
            for part in re.split(r'^### ', open(f, encoding='utf-8').read(), flags=re.M)[1:]:
                t, _, body = part.partition('\n')
                body = re.sub(r'^\(handover log:[^\n]*\)\s*$', '', body, flags=re.M).strip()
                if t.strip() >= self.since.isoformat()[:19]:
                    out.append((t.strip(), body, os.path.basename(f)))
        return sorted(out)

    def _load_shows(self):
        """{session tail: [(iso time, film, [files pointed to])]} from the code finder's logs, last 7 days."""
        out = {}
        for lg in glob.glob(os.path.join(ROOT, 'notes', 'logs', '*-show.log')):
            film = os.path.basename(lg)[:-len('-show.log')]
            for ln in open(lg, encoding='utf-8'):
                p = ln.rstrip('\n').split('\t')
                if len(p) >= 6 and p[0] >= self.since.isoformat()[:19]:
                    pts = [p[3].split(':')[0]] + (p[6].split(',') if len(p) > 6 and p[6] else [])
                    out.setdefault(p[5][-8:].lower(), []).append((p[0], film, pts, p[4] if p[4] != '-' else ''))
        return out

    def _load_plainlog(self):
        out = []
        try:
            for ln in open(os.path.join(ROOT, 'notes', 'logs', 'plainwords.log'), encoding='utf-8'):
                try:
                    out.append(json.loads(ln))
                except ValueError:
                    pass
        except OSError:
            pass
        return out

    def _load_hooks(self):
        """[(event, matcher, command)] from .claude/settings.json."""
        try:
            h = json.load(open(os.path.join(ROOT, '.claude', 'settings.json')))['hooks']
        except (OSError, ValueError, KeyError):
            return []
        return [(ev, g.get('matcher', ''), x.get('command', '')) for ev, gs in h.items() for g in gs
                for x in g.get('hooks', [])]

    def _load_notes_lines(self):
        out = []
        for f in glob.glob(os.path.join(ROOT, 'notes', '*.md')) + glob.glob(os.path.join(ROOT, 'notes', 'archive', '*.md')):
            out += [x for x in open(f, encoding='utf-8').read().splitlines() if len(x) > 20]
        return out

    def _load_routine_cmds(self):
        return routine_commands()

    def _load_edits_by_film(self):
        """{film: [(iso time, file)]}: drawing files changed by the chats whose cost row is that film's."""
        by = {}
        for r in self.rows:
            s = (r.get('sid') or '')[-8:].lower()
            if s:
                by.setdefault(s, r['record'])
        out = {}
        for s, eds in _edits_by_session(self).items():
            if s in by:
                out.setdefault(by[s], []).extend(eds)
        return out

    def _load_films(self):
        """The films worked on in the last 7 days that have their own code (source/NAME.py)."""
        names = {r['record'] for r in self.rows}
        return sorted(n for n in names if os.path.exists(os.path.join(HERE, n.replace('-', '_') + '.py')))

    def _load_page_files(self):
        import page
        return {f: [os.path.basename(x) for x in page.files(f)] for f in self.films}

    def _load_learned(self):
        try:
            w = json.load(open(os.path.join(ROOT, 'notes', 'learn', 'plain-words', 'words.json')))
        except (OSError, ValueError):
            return [], []
        ex = sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, 'notes', 'learn', 'plain-words', 'bad-*')))
        return w.get('learned', []), ex


def _plural(n, one, many=None):
    return f'{n} {one if n == 1 else (many or one + "s")}'


def _real_sam(R):
    """Sam's own typed messages: not a chat's opening prompt written by the chain, not a system notice."""
    return [(t, x, f) for t, x, f in R.sam if not NOT_SAM_RE.search(x) and not CHAIN_RE.search(x)]


# ------------------------------------------------------------------------------------------------ the tools
def handover_reach(R):
    if not any(ev == 'UserPromptSubmit' and 'handover.py log' in c for ev, _, c in R.hooks):
        return 'broken', 'the message saver is not switched on'
    chain = [t for t, x, _ in R.sam if CHAIN_RE.search(x) or NOT_SAM_RE.search(x)]
    if chain:
        return 'partly', (f'it saves {_plural(len(chain), "message")} written by a chat (a chat\'s opening '
                          f'instructions, or a system notice) as if Sam typed them, so the start check asks for them '
                          f'to be carried as his words')
    return 'ok', 'every saved message is Sam\'s own'


def handover_use(R):
    """What actually happened: a request of Sam's that no notes line carried, which he then had to make again later
    (most of his words again, in a later hour). The share carried is the handover's own measure, shown beside it."""
    import handover, functools
    lines = R.notes_lines
    asks = [(t, a, n) for t, x, _ in _real_sam(R) for n, a in handover.asks(re.sub(r'@"[^"]*"', ' ', x))]
    if not asks:
        return 'ok', 'no requests from Sam this week'
    plain = handover.words
    handover.words = functools.lru_cache(maxsize=None)(plain)      # each notes line read once, not once per ask
    try:
        lost = [(t, a) for t, a, n in asks if not handover.carried(a, lines, n)]
        W = lambda a: set(handover.words(a)[0])
        again = []
        for t, a in lost:
            A = W(a)
            if len(A) >= 4:
                for t2, b, _ in asks:
                    quoted = a.strip(' ."')[:60] in b                 # a chat quoting him is not Sam asking again
                    if t2[:13] > t[:13] and not quoted and len(A & W(b)) / len(A) >= 0.6:
                        again.append((t, a, t2))
                        break
    finally:
        handover.words = plain
    if again:
        return 'partly', (f'{_plural(len(again), "request")} of Sam\'s this week were never written in the notes and he '
                          f'had to make them again (e.g. "{again[0][1][:60]}", {again[0][0][:10]}, again '
                          f'{again[0][2][:10]})')
    return 'ok', (f'no request of Sam\'s this week had to be made twice ({len(asks) - len(lost)} of {len(asks)} '
                  f'sentences are carried word for word; the rest are replies and remarks)')


def costwatch_reach(R):
    if not any(ev == 'PostToolUse' and 'costwatch.py' in c and m in ('*', '') for ev, m, c in R.hooks):
        return 'broken', 'it is not run after every step'
    bare = [r for r in R.rows if r.get('sid') and not r.get('steps')]
    if bare:
        return 'partly', f'{_plural(len(bare), "chat")} this week have no step count'
    return 'ok', 'every step is priced'


def costwatch_use(R):
    over = [r for r in R.rows if (r.get('hist_k') or 0) > RED_K]
    if over:
        return 'partly', (f'{_plural(len(over), "chat")} this week went past the red line without handing over '
                          f'(e.g. chat {over[0].get("chat")}, {over[0].get("hist_k")} thousand)')
    return 'ok', f'no chat went past the red line ({len(R.rows)} chats this week)'


def routine_commands(texts=None):
    """The commands the guides and notes tell a chat to run for a whole-film render or the finishing step, as written
    now (so a new way of starting routine work is tested as soon as a guide names it). [(command, routine?)]: a
    command with --span is a short clip, which the guard must let through."""
    if texts is None:
        texts = [open(f, encoding='utf-8').read() for f in glob.glob(os.path.join(ROOT, 'guides', '*.md'))
                 + glob.glob(os.path.join(ROOT, 'notes', '*.md')) + [os.path.join(ROOT, 'CLAUDE.md')]]
    out = set()
    for t in texts:
        for c in re.findall(r'`((?:time\s+)?(?:cd \S+ && )?python3?\s[^`]*?(?:finish\.py|\.py (?:final|animatic))[^`]*)`', t):
            c = ' '.join(c.replace('NAME', 'brexit_is_done').replace('FILM', 'brexit_is_done').split())
            out.add((c, '--span' not in c))
    return sorted(out)


def modelguard_reach(R):
    import modelguard
    cmds = R.routine_cmds
    wrong = [c for c, want in cmds if bool(modelguard.routine(c)) != want]
    if wrong:
        return 'partly', (f'it misreads {_plural(len(wrong), "command")} the guides give for routine work, e.g. '
                          f'"{wrong[0][:70]}"')
    return 'ok', f'it reads all {len(cmds)} routine commands the guides give'


def modelguard_use(R):
    """An Opus chat whose record counts a routine step: caught if the guard's log refused it in that chat; slipped if
    not (only since the guard went in)."""
    try:
        log = open(os.path.join(ROOT, 'notes', 'logs', 'modelguard.log'), encoding='utf-8').read().lower()
    except OSError:
        log = ''
    began = _git('log', '--format=%cI', '--diff-filter=A', '--', 'notes/logs/modelguard.log').split()[-1:] or ['']
    tried = [r for r in R.rows if r.get('model') in ('opus', 'fable') and (r.get('calls') or {}).get('routine')
             and r.get('date', '') > began[0][:10]]                  # the log began on that day: later days only
    slipped = [r for r in tried if (r.get('sid') or r.get('chat', ''))[-8:].lower() not in log]
    if slipped:
        return 'partly', (f'{_plural(len(slipped), "Opus chat")} ran routine work this week with no refusal logged '
                          f'(e.g. chat {slipped[0]["chat"]}, {slipped[0]["date"]})')
    return 'ok', f'it stopped every routine step tried on Opus this week ({len(tried)})'


def _dyn_imports(path):
    """source/ modules a file loads by name (__import__('x'), importlib.import_module('x')): the plain import scan
    does not see these."""
    try:
        src = open(path, encoding='utf-8').read()
    except OSError:
        return set()
    got = set(re.findall(r"""(?:__import__|import_module)\(\s*['"](\w+)['"]""", src))
    return {m for m in got if os.path.exists(os.path.join(HERE, m + '.py'))}


def _tools():
    """The project's own tools (the watcher's list of systems, the hooks): a note on a film never lands in these, so
    the finder need not point to them."""
    import watcher
    return {k.split()[0] for k in watcher.PROMISES} | {os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '.claude', 'hooks', '*.py'))} | {'kittests.py', 'hookran.py'}


def closure(film):
    """Every source file the film's code loads, worked out here on its own (not with the finder's list): its own
    files, then each import, at the top, inside a def, or by name (__import__), followed through; other films' code
    left out. R12's blind spot (the finder searched only the film's own files) is the gap between the two."""
    import ast, page
    others = page._film_mods()
    mine = [os.path.basename(f)[:-3] for f in page.own_files(film)]
    seen, todo = set(mine), list(mine)
    while todo:
        path = os.path.join(HERE, todo.pop() + '.py')
        try:
            tree = ast.parse(open(path, encoding='utf-8').read())
        except (OSError, SyntaxError):
            continue
        got = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                got |= {a.name.split('.')[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom) and n.module and not n.level:
                got.add(n.module.split('.')[0])
        got |= _dyn_imports(path)
        for m in got:
            if m not in seen and (m not in others or m in mine) and os.path.exists(os.path.join(HERE, m + '.py')):
                seen.add(m); todo.append(m)
    return {m + '.py' for m in seen}


def finder_reach(R):
    gaps, tools = [], _tools()
    for film, fs in R.page_files.items():
        have = set(fs)
        for f in sorted((R.closures.get(film) if 'closures' in R.__dict__ else closure(film)) - have - tools):
            gaps.append(f'{f} (the {film} drawing code uses it)')
    if gaps:
        return 'partly', f'it does not search {gaps[0]}' + (f' and {len(gaps) - 1} more' if len(gaps) > 1 else '')
    return 'ok', ('it searches every file the films load, by import or by name ('
                  + ', '.join(f'{k}: {len(v)} files' for k, v in R.page_files.items()) + ')')


def _edits_by_session(R):
    """{session tail: [(iso time, file)]}: code files each chat changed this week (source/*.py)."""
    out = {}
    for h, t, s, fs in R.commits:
        for f in fs:
            if s and re.match(r'source/[\w]+\.py$', f):
                out.setdefault(s.lower(), []).append((t, os.path.basename(f)))
    return out


REPLAY_MAX = 12


def finder_use(R, show_fn=None):
    """Last week's real notes, asked again of the finder as it is NOW: does it point to a drawing file that chat then
    changed? (A chat that changed only tools, or nothing, is not counted.)"""
    import page
    show_fn = show_fn or (lambda film, note: [h.split()[0].split(':')[0] for h, _ in page.show(film, note, 40)
                                              if not h.startswith('also')])
    edits, tools, cases = _edits_by_session(R), _tools(), []
    for sid, calls in R.shows.items():
        for t, film, pts, note in calls:
            ed = {f for te, f in edits.get(sid, []) if te[:19] >= t[:19] and f not in tools}
            if ed and note and film in R.page_files:
                cases.append((t, film, note, ed))
    cases = sorted(cases)[-REPLAY_MAX:]
    if not cases:
        return 'ok', 'no note this week was followed by a drawing fix to replay'
    missed = []
    for t, film, note, ed in cases:
        if not ed & set(show_fn(film, note)):
            missed.append((note, sorted(ed)))
    if len(missed) > len(cases) // 3:
        return 'partly', (f'asked again now, {len(cases) - len(missed)} of {len(cases)} of last week\'s notes lead to '
                          f'the code that was fixed (e.g. "{missed[0][0][:50]}" was fixed in {missed[0][1][0]})')
    return 'ok', f'asked again now, {len(cases) - len(missed)} of {len(cases)} of last week\'s notes lead to the code that was fixed'


def finderwarn_reach(R):
    import finderwarn
    pat = finderwarn.film_re()
    shared = sorted({f for fs in R.page_files.values() for f in fs if not pat.search('source/' + f)})
    if shared:
        return 'partly', (f'it reminds a chat only when it hand-searches a film\'s own code, not the shared drawing '
                          f'code the finder now covers ({_plural(len(shared), "file")}, e.g. {shared[0]})')
    return 'ok', 'it watches every file the finder covers'


def finderwarn_use(R):
    rounds = [r for r in R.rows if r.get('notes')]              # a round of Sam's notes: the finder's own job
    hand = [r for r in rounds if (r.get('calls') or {}).get('film-file search') and not (r.get('calls') or {}).get('page.py')]
    if len(hand) > max(1, len(rounds) // 5):
        return 'partly', (f'in {len(hand)} of {len(rounds)} rounds of Sam\'s notes this week the chat searched film code '
                          f'by hand and never used the finder (the reminder warns, it does not stop)')
    return 'ok', f'{len(rounds) - len(hand)} of {len(rounds)} rounds of Sam\'s notes this week used the finder'


def page_reach(R):
    import page
    old = [f for f in R.films if page.stale(f)]
    if old and len(old) == len(R.films):
        return 'partly', f'the page is older than the code for {", ".join(old)} (it is rebuilt on the next finder call)'
    return 'ok', 'each film\'s page is current'


def page_use(R):
    rounds = [r for r in R.rows if r.get('notes')]
    whole = [r for r in rounds if (r.get('calls') or {}).get('whole-file .py read')]
    if len(whole) > max(1, len(rounds) // 5):
        return 'partly', (f'in {len(whole)} of {len(rounds)} rounds of Sam\'s notes this week the chat read whole code '
                          f'files instead of the page')
    return 'ok', f'{len(rounds) - len(whole)} of {len(rounds)} rounds of Sam\'s notes this week read the page, not whole files'


def packs_reach(R):
    txt = open(os.path.join(ROOT, 'guides', 'job-packs.md'), encoding='utf-8').read()
    refs = set(re.findall(r'(?<![\w/])((?:source|guides|notes|story|\.claude/hooks)/[\w./-]+\.(?:py|md|sh|txt|json|tsv))', txt))
    dead = sorted(r for r in refs if 'NAME' not in r and 'FILM' not in r and not os.path.exists(os.path.join(ROOT, r)))
    if dead:
        return 'partly', f'it names {_plural(len(dead), "file")} that no longer exist (e.g. {dead[0]})'
    return 'ok', f'all {len(refs)} files the packs name exist'


def packs_use(R):
    txt = open(os.path.join(ROOT, 'guides', 'job-packs.md'), encoding='utf-8').read()
    heads = {h.strip().lower() for h in re.findall(r'^##+\s*([^(\n]+)', txt, re.M)}
    bad, n = [], 0
    for f in glob.glob(os.path.join(ROOT, 'notes', '*.md')):
        for m in re.finditer(r'^Read:[^\n]*?job-packs\.md\s*"([^"]+)"', open(f, encoding='utf-8').read(), re.M):
            n += 1
            if not any(m.group(1).strip().lower() in h or h in m.group(1).strip().lower() for h in heads):
                bad.append((os.path.basename(f), m.group(1)))
    if bad:
        return 'partly', f'{_plural(len(bad), "handover")} name a pack section that does not exist (e.g. "{bad[0][1]}")'
    return 'ok', f'all {n} handovers name a pack that exists'


def kittests_reach(R):
    tests = set(re.findall(r'^@test\ndef (\w+)', open(os.path.join(HERE, 'kittests.py'), encoding='utf-8').read(), re.M))
    try:
        stamped = {ln.split('\t')[0] for ln in open(os.path.join(ROOT, 'notes', 'kittest-stamps.tsv'), encoding='utf-8')
                   if not ln.startswith('#')}
    except OSError:
        stamped = set()
    never = sorted(tests - stamped)
    if len(never) > len(tests) // 10:
        return 'partly', (f'{_plural(len(never), "test")} of {len(tests)} have never passed with a record of the '
                          f'files they read, so they run again every time (e.g. {never[0]})')
    return 'ok', (f'{len(tests) - len(never)} of {len(tests)} tests know which files they read, so only changed ones '
                  f're-run')


def kittests_use(R):
    import kitfilm
    rows = [r for r in kitfilm.rows() if len(r) > 3 and r[2] >= R.since.isoformat()[:16] and not r[3].startswith('seed')]
    starts = [r for r in rows if r[1] == 'start']
    runs = 0
    try:
        runs = sum(1 for ln in open(os.path.join(ROOT, 'notes', 'kittest-stamps.tsv'), encoding='utf-8')
                   if not ln.startswith('#') and ln.split('\t')[3:4] and ln.split('\t')[3] >= R.since.isoformat()[:16])
    except OSError:
        pass
    return 'ok', (f'{_plural(len(starts), "film start")} this week ran the tests; {runs} test passes were recorded so '
                  f'unchanged tests were not run again')


def ledger_reach(R):
    if not any(ev == 'Stop' and 'ledger.py auto' in c for ev, _, c in R.hooks):
        return 'broken', 'the automatic cost row is not switched on'
    bare = [r for r in R.rows if not r.get('sid')]
    rowed = {(r.get('sid') or '')[-8:].lower() for r in R.rows}
    worked = {s.lower() for _, _, s, fs in R.commits if s and any(not f.startswith('notes/ledger/') for f in fs)}
    none = sorted(worked - rowed)
    if bare and len(none) > max(1, len(worked) // 10):
        return 'partly', (f'{len(bare)} of {len(R.rows)} cost rows this week do not say which chat they belong to, so '
                          f'{len(none)} of {len(worked)} chats that saved work cannot be matched to a cost')
    if len(none) > max(1, len(worked) // 10):
        return 'partly', f'{len(none)} of {len(worked)} chats that saved work this week have no cost row'
    return 'ok', f'{len(worked) - len(none)} of {len(worked)} chats that saved work this week have a cost row'


def ledger_use(R):
    priced = [r for r in R.rows if r.get('cost')]
    blank = len(R.rows) - len(priced)
    if blank > max(1, len(R.rows) // 10):
        return 'partly', f'{blank} of {len(R.rows)} cost rows this week have no cost'
    return 'ok', f'{len(priced)} of {len(R.rows)} chats this week are priced'


CHANNELS = [('Stop', '', 'replies'), ('PreToolUse', 'SendUserFile', 'the captions on files sent to Sam'),
            ('PreToolUse', 'PushNotification', 'push notifications'),
            ('PreToolUse', 'AskUserQuestion', 'question boxes')]


def plain_reach(R):
    def covered(ev, m):
        return any(e == ev and 'plainwords' in c and (not m or re.search(mm or '.', m)) for e, mm, c in R.hooks)
    miss = [what for ev, m, what in CHANNELS if not covered(ev, m)]
    if 'replies' in miss:
        return 'broken', 'the replies to Sam are not read'
    if miss:
        return 'partly', f'it reads the replies but not {", ".join(miss[:-1]) + " or " + miss[-1] if len(miss) > 1 else miss[0]}'
    return 'ok', 'it reads every way text reaches Sam'


def plain_use(R):
    import plainwords
    log = R.plainlog
    if not log:
        return 'broken', 'it has never logged a reply'
    t0 = min(x.get('t', '9') for x in log)
    confused = [(t, x) for t, x, _ in _real_sam(R) if t.replace('T', ' ')[:16] >= t0 and plainwords.CONFUSED_RE.search(x)]
    learned, ex = R.learned
    lets = [x for x in log if x.get('event') == 'let-through']
    if confused:
        return 'partly', (f'since it went in Sam asked for something to be explained {_plural(len(confused), "time")} '
                          f'(e.g. "{confused[0][1][:50]}"), and {len(learned)} new words were learned from that'
                          + (f'; {_plural(len(lets), "reply", "replies")} went through still unclear' if lets else ''))
    if lets:
        return 'partly', f'{_plural(len(lets), "reply", "replies")} went to Sam still holding words it flagged'
    return 'ok', f'{sum(1 for x in log if x.get("event") == "block")} replies were sent back and rewritten; none reached Sam unclear'


def save_reach(R):
    import branches
    try:
        bs = R.branches if 'branches' in R.__dict__ else branches.scan(ROOT, days=DAYS, now=R.now.timestamp())
    except Exception as e:                                    # a scan that cannot run is itself the finding
        return 'broken', f'the branch scan could not run ({type(e).__name__})'
    notes = ' '.join(open(f, encoding='utf-8').read() for f in glob.glob(os.path.join(ROOT, 'notes', '*.md')))
    left = [b[0] for b in bs if b[0] not in notes]
    if left:
        return 'partly', (f'{_plural(len(left), "branch", "branches")} (separate copies a chat saved to) hold work '
                          f'that is neither on the main copy nor named in the notes (e.g. {left[0]})')
    return 'ok', f'every branch with work is on the main line or named in the notes ({len(bs)} named)'


def save_use(R):
    worked = {}
    for h, t, s, fs in R.commits:
        if s:
            worked.setdefault(s.lower(), []).append(h)
    off = sorted(s for s, hs in worked.items() if not any(h in R.on_main for h in hs))
    notes = ' '.join(open(f, encoding='utf-8').read() for f in glob.glob(os.path.join(ROOT, 'notes', '*.md')))
    named = [s for s in off if any(b.split('/', 1)[-1] in notes for b in
                                   _git('branch', '-r', '--contains', worked[s][0]).split())]
    off = [s for s in off if s not in named]
    if off:
        return 'partly', f'{len(off)} of {len(worked)} chats this week have no work on the main line (e.g. chat {off[0]})'
    return 'ok', (f'every chat that saved work this week ({len(worked)}) reached the main copy'
                  + (f', or a separate copy named in the notes ({len(named)})' if named else ''))


def body_reach(R):
    import humancheck
    if not any(ev == 'PreToolUse' and 'humancheck.py sendgate' in c for ev, _, c in R.hooks):
        return 'broken', 'the send check is not switched on'
    notes = ' '.join(open(f, encoding='utf-8').read() for f in glob.glob(os.path.join(ROOT, 'notes', '*.md'))
                     + glob.glob(os.path.join(ROOT, 'notes', 'archive', '*.md')))
    finals = [f for f in glob.glob(os.path.join(ROOT, 'animations', '*-vertical.mp4'))
              + glob.glob(os.path.join(ROOT, 'animations', '*-story.mp4')) if os.path.basename(f) in notes]
    blind = [os.path.basename(f) for f in finals if not humancheck.is_final(f)]
    if blind:
        return 'partly', f'it does not know {blind[0]} is a finished film'
    return 'ok', f'it knows all {len(finals)} finished films'


def body_use(R):
    import humancheck
    new = sorted({f for _, t, _, fs in R.commits for f in fs if re.match(r'animations/[^/]+\.mp4$', f)})
    bare = [f for f in new if os.path.exists(os.path.join(ROOT, f)) and humancheck.load(os.path.join(ROOT, f)) is None]
    if bare:
        return 'partly', f'{_plural(len(bare), "finished film")} saved this week have no body check record'
    return 'ok', (f'{_plural(len(new), "finished film")} this week, each with its record' if new
                  else 'no finished film this week (clips and animatics go as made, Sam 26 Nov)')


def cast_reach(R):
    import people
    gaps = []
    for film in R.films:
        p = os.path.join(ROOT, 'story', f'{film}-people.txt')
        if film in getattr(people, 'BEFORE_SEX', ()) or not os.path.exists(p):
            continue
        txt = open(p, encoding='utf-8').read()
        for who, blk in re.findall(r'^#\s*(\w+):[^\n]*\n(.*?)(?=^#\s*\w+:|\Z)', txt, re.M | re.S):
            if re.search(r'^crowd:', blk, re.M):
                continue                                      # the crowd pack's people, each drawn from its own list
            body = re.search(r'^body:([^\n]*)', blk, re.M)
            if not body or not re.search(r'\b(?:woman|man|girl|boy)\b', body.group(1), re.I):
                gaps.append(f'{who} ({film})')
    if gaps:
        return 'partly', f'it is not told whether {gaps[0]} is a man or a woman'
    return 'ok', 'it knows who is a woman in every cast'


def cast_use(R):
    body = [(t, x) for t, x, _ in _real_sam(R) if re.search(r"\b(?:female bod|woman'?s bod|man'?s bod|looks? like a man)", x, re.I)]
    try:
        stops = sum(1 for ln in open(os.path.join(ROOT, 'notes', 'logs', 'handover-end.log'), encoding='utf-8')
                    if 'CAST SHEET' in ln and ln[:10] >= R.since.date().isoformat())
    except OSError:
        stops = 0
    late = [x for x in body if x[0] >= '2026-11-25']           # the women's builds check went in on 25 Nov (rule S12)
    if late:
        return 'partly', f'Sam still had to say a woman looked like a man ({late[0][0][:10]})'
    return 'ok', f'it stopped {_plural(stops, "handover")} this week on a body that did not read right'


def missing(why):
    return lambda R: ('missing', why)


TOOLS = [
    ('handover', 'The handover', 'nothing Sam says or decides is lost between one chat and the next', handover_reach, handover_use),
    ('costwatch', 'The cost watch', 'every step is priced and a chat hands over in time at amber and red', costwatch_reach, costwatch_use),
    ('modelguard', 'The model guard', 'routine work (finishing, whole-film renders) never runs on the expensive model', modelguard_reach, modelguard_use),
    ('finder', 'The code finder', 'a note finds the code it touches in one step, wherever that code lives', finder_reach, finder_use),
    ('finderwarn', 'The finder reminder', 'a chat that searches code by hand before asking the finder is told at once', finderwarn_reach, finderwarn_use),
    ('page', 'The film page', 'each film has a short page of its code, so a chat reads the page, not whole files', page_reach, page_use),
    ('packs', 'The job packs', 'each stage reads only its own short reading list, and everything it names exists', packs_reach, packs_use),
    ('kittests', 'Kit tests only when needed', 'the checks on the drawing tools run at a film\'s start and end, and only the ones whose files changed', kittests_reach, kittests_use),
    ('ledger', 'The cost records', 'every chat\'s cost is written down so each film\'s cost is known', ledger_reach, ledger_use),
    ('plainwords', 'The plain-words checker', 'nothing reaches Sam in words he would need explained', plain_reach, plain_use),
    ('save', 'Saving to GitHub', 'every chat\'s work reaches the main copy of the project', save_reach, save_use),
    ('body', 'The body check on finished films', 'no finished film reaches Sam without its body check and fresh critique', body_reach, body_use),
    ('cast', 'The cast check', 'every woman in a cast is drawn and read as a woman, every man as a man', cast_reach, cast_use),
    ('limits', 'Printout and picture limits', 'long printouts are cut to the faults and pictures go on one sheet',
     missing('not built yet (a reserve job Sam has listed)'), missing('not built yet')),
]
RANK = {'ok': 0, 'partly': 1, 'broken': 2, 'missing': 3}


def _run(fn, R):
    try:
        return fn(R)
    except Exception as e:                                   # a part that cannot run is broken, never quiet
        return 'broken', f'its test could not run ({type(e).__name__}: {str(e)[:80]})'


def check(R=None, only=None):
    R = R or Rec()
    out = []
    for tid, name, promise, reach, use in TOOLS:
        if only and tid not in only:
            continue
        r, u = _run(reach, R), _run(use, R)
        out.append((tid, name, promise, r, u, line(name, r, u)))
    return out


def line(name, r, u):
    worst = max((r, u), key=lambda x: RANK[x[0]])
    if worst[0] == 'ok':
        return f'{name}: working.'
    if worst[0] == 'missing':
        return f'{name}: not built yet.'
    misses = '; '.join(x[1] for x in (r, u) if x[0] != 'ok')
    return f'{name}: {"partly working" if worst[0] == "partly" else "broken"} – {misses}.'


def report(rows, why=False):
    head = (f'Tool health ({datetime.now(timezone.utc):%d %b %H:%M}): '
            f'{sum(1 for x in rows if x[-1].endswith("working."))} of {len(rows)} working')
    body = [x[-1] for x in rows]
    if why:
        body = [f'{x[-1]}\n    promise: {x[2]}\n    reach: {x[3][0]}: {x[3][1]}\n    use: {x[4][0]}: {x[4][1]}' for x in rows]
    return '\n'.join([head] + body)


def at_start(film=None, out=OUT):
    """A film's start (kitfilm.at_start / begin): the report beside the kit tests, saved for handover start."""
    text = report(check())
    try:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(text + '\n')
    except OSError:
        pass
    return text


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['start']:
        print(at_start(a[1] if len(a) > 1 else None))
    else:
        print(report(check(only=[x for x in a if not x.startswith('-')] or None), why='--why' in a))
