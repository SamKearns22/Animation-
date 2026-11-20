#!/usr/bin/env python3
"""checkreplay: today's checks re-run on a past film, chat by chat (check-catches Learn, Sam's Y on 19 Nov).

Sam's rule: remove a step only if it caught nothing in three films. Nothing recorded what each check caught, so this
re-runs today's pre-flight on each chat branch of a past film (the film's own files as that chat left them, today's
shared tools, as the 16 Nov late-faults replay did) and writes one table, one row per check.

MAP
  branches() .... a film's chat branches on GitHub, oldest first (by their last commit)
  overlay() ..... a throwaway copy of the main line (git worktree) with the film's own files from one branch
  run() ......... pre-flight (`preflight.py FILM OUT --text`) in that copy, timed; each fault line kept under its check
                  (the words before the first ':'); saved to notes/proposals/check-catches/replay/FILM.json
  table() ....... per check: runs, faults listed, gone by the next run (caught), still there at the last run (let
                  through, unless named in the notes' Exceptions), could not test, run time. Two columns are left
                  for the chat to fill by judgment: false alarms, and Sam's notes it should have caught (from the
                  film's notes table). Bar to beat: a sourced answer for 80% of check-film pairs
  test .......... `python3 source/checkreplay.py test`: the parser and the table on made-up runs

    python3 source/checkreplay.py branches FILM
    python3 source/checkreplay.py run FILM [--only BRANCH,BRANCH] [--max N]     (~20 s to 2 min a branch)
    python3 source/checkreplay.py table FILM                                    (writes replay/FILM.md)
    python3 source/checkreplay.py table FILM --record    (the live record: notes/ledger/FILM/check-table.md)
    python3 source/checkreplay.py test
"""
import json, os, re, shutil, subprocess, sys, tempfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'notes', 'proposals', 'check-catches', 'replay')
PREFIX = {'milburn': ['milburn'], 'protest-tiers': ['protest-tiers', 'protest'], 'blessed': ['blessed']}
SKIP = re.compile(r'(posted|review|usage|handover|screening|plan$|wip$)')   # not chat work on the film's code
LINE = re.compile(r'^\s*-\s+(.+)$')
NUM = re.compile(r'\d+(?:\.\d+)?')


def git(*a, cwd=ROOT):
    return subprocess.run(['git', *a], cwd=cwd, capture_output=True, text=True)


def branches(film):
    heads = [l.split()[1][len('refs/heads/'):] for l in git('ls-remote', '--heads', 'origin').stdout.splitlines()]
    want = [h for h in heads if any(h.startswith('claude/' + p) for p in PREFIX.get(film, [film]))
            and not SKIP.search(h)]
    dated = []
    for h in want:
        git('fetch', '-q', 'origin', h)
        t = git('log', '-1', '--format=%ct', 'FETCH_HEAD').stdout.strip()
        dated.append((int(t or 0), h))
    return [h for _, h in sorted(dated)]


def _film_files(film, ref):
    code = film.replace('-', '_')
    names = git('ls-tree', '-r', '--name-only', ref).stdout.splitlines()
    pat = re.compile(r'^(?:source/(?:data/)?%s[\w.-]*|story/(?:%s|%s)[\w./-]*|notes/%s\.md)$' % (
        re.escape(code), re.escape(film), re.escape(code), re.escape(film)))
    return [n for n in names if pat.match(n)]


def overlay(film, branch):
    """A throwaway copy of the main line with the film's files as BRANCH left them. Returns its folder."""
    git('fetch', '-q', 'origin', branch)
    ref = git('rev-parse', 'FETCH_HEAD').stdout.strip()
    d = tempfile.mkdtemp(prefix='replay-')
    git('worktree', 'add', '-q', '--detach', d, 'origin/claude/create-claude-md-oe8z4g')
    files = _film_files(film, ref)
    for f in _film_files(film, 'HEAD'):           # the film as it is now, minus what the branch did not have yet
        if f not in files and os.path.exists(os.path.join(d, f)):
            os.remove(os.path.join(d, f))
    if files:
        git('checkout', ref, '--', *files, cwd=d)
    return d, ref[:8], len(files)


TIMED = re.compile(r'^\d+(?:\.\d+)?\s*s$')     # "7.17 s: runner6.footR jumps": the audit's time-stamped lines


def head(body):
    """The check a fault line belongs to: the words before the first ':' (a quoted bit and a bracket dropped, counts
    as '#'). check-catches change 3 (Sam's Y, 20 Nov): a time-stamped line ("7.17 s: ...") is the audit's, so all of
    them are ONE check, not one row per time; "the brief checklist has 8 blank" and "...has 4 blank" are one check."""
    h = body.split(':', 1)[0].strip()
    if TIMED.match(h):
        return 'AUDIT'
    cut = re.split(r'\s*["“(]', h)[0].strip()
    if len(cut) <= 3:                              # 'no "Rehearsal clips sent' would be 'no': keep the quoted words
        cut = re.split(r'\s*\(', re.sub(r'["“”]', '', h))[0].strip()
    return NUM.sub('#', re.sub(r'\s+', ' ', cut or 'other'))[:40]


def parse(text):
    """Fault lines -> {check: [fault, ...]}."""
    out = {}
    for ln in text.splitlines():
        m = LINE.match(ln)
        if m:
            out.setdefault(head(m.group(1)), []).append(m.group(1)[:200])
    return out


def regroup(faults):
    """Old records were grouped before change 3; group their lines again by today's head()."""
    out = {}
    for f in (x for v in faults.values() for x in v):
        out.setdefault(head(f), []).append(f)
    return out


def broken(r):
    """change 3: a run is broken only when it listed no fault at all and crashed or timed out. Before, any run whose
    output held the word "refuse" (pre-flight's gates say it in ordinary output) was dropped, so Protest Tiers and
    Blessed scored nothing."""
    return not any(r.get('faults', {}).values()) and (r.get('refused') or r.get('exit', 0) not in (0, 1, 2))


def _key(f):
    return NUM.sub('#', f)                         # the same fault with moved times or counts is the same fault


def run(film, only=None, mx=None):
    os.makedirs(OUT, exist_ok=True)
    jf = os.path.join(OUT, film + '.json')
    rec = json.load(open(jf)) if os.path.exists(jf) else {'film': film, 'runs': []}
    done = {r['branch'] for r in rec['runs']}
    todo = [b for b in (only or branches(film)) if b not in done][:mx]
    for b in todo:
        d, ref, n = overlay(film, b)
        o = tempfile.mkdtemp()
        t0 = time.time()
        try:
            p = subprocess.run([sys.executable, 'preflight.py', film, o, '--text'], cwd=os.path.join(d, 'source'),
                               capture_output=True, text=True, timeout=900)
            txt, code = p.stdout + p.stderr, p.returncode
        except subprocess.TimeoutExpired:
            txt, code = 'TIMED OUT', -1
        secs = round(time.time() - t0)
        faults = parse(txt)
        refused = not faults and ('Traceback' in txt or code not in (0, 1, 2))
        rec['runs'].append({'branch': b, 'ref': ref, 'files': n, 'secs': secs, 'exit': code, 'refused': refused,
                            'faults': faults, 'tail': txt[-600:] if refused or code not in (0, 1) else ''})
        json.dump(rec, open(jf, 'w'), indent=1)
        git('worktree', 'remove', '--force', d)
        shutil.rmtree(o, ignore_errors=True)
        print(f'checkreplay: {b} ({ref}, {n} film files): {sum(len(v) for v in faults.values())} faults in '
              f'{len(faults)} checks, {secs} s' + (' REFUSED or broken: see its tail' if refused else ''))
    return rec


def table(film, rec=None, exceptions='', tags=None):
    rec = rec or json.load(open(os.path.join(OUT, film + '.json')))
    runs = [dict(r, faults=regroup(r['faults'])) for r in rec['runs'] if not broken(r)]
    for r in runs:                                  # stopped at a gate (exit 2): the checks after it never ran, so
        if 'ran' not in r and r.get('exit') == 2:   # only the ones it listed are compared
            r['ran'] = list(r['faults'])
    checks = sorted({c for r in runs for c in r['faults']})
    rows = []
    for c in checks:
        owners = {c} | {r.get('of', {}).get(c, c) for r in runs}   # a check inside pre-flight ran when pre-flight did
        seen = [{_key(f) for f in r['faults'].get(c, [])} for r in runs if 'ran' not in r or owners & set(r['ran'])]
        last = seen[-1] if seen else set()
        caught = len(set().union(*[a - b for a, b in zip(seen, seen[1:])]) - last)   # each fault once
        named = sum(1 for k in last if k[:30] in exceptions)
        rows.append({'check': c, 'runs': sum(1 for s in seen if s), 'faults': len(set().union(*seen)),
                     'caught': caught, 'let_through': len(last) - named, 'named': named,
                     'could_not_test': sum(1 for r in runs for f in r['faults'].get(c, []) if 'COULD NOT TEST' in f),
                     'missed': [n for n, t in (tags or {}).items() if t and t.strip().lower() == c.lower()]})
    for t in sorted({t for t in (tags or {}).values() if t and t.strip().lower() != 'none'} - {r['check'].lower() for r in rows},
                    key=str.lower):                 # a check Sam's notes name that listed nothing at all
        rows.append({'check': t.strip(), 'runs': 0, 'faults': 0, 'caught': 0, 'let_through': 0, 'named': 0,
                     'could_not_test': 0, 'missed': [n for n, x in tags.items() if x and x.strip().lower() == t.lower()]})
    secs = sum(r['secs'] for r in runs)
    out = [f'# Check replay: {film} (today\'s checks on each chat branch; check-catches Learn)', '',
           f'{len(rec["runs"])} branches, {len(runs)} ran ({len(rec["runs"]) - len(runs)} refused or broken); '
           f'pre-flight time {secs} s in all, {secs // max(1, len(runs))} s a run. "Caught" = a fault gone by the '
           f'next chat; "let through" = still there at the last chat and not named in the notes\' Exceptions.',
           'False alarms and "Sam\'s notes it should have caught" are filled by the replay chat from the film\'s '
           'notes table; "?" = could not tell (the bar: a sourced answer for 80% of check-film pairs).', '',
           '| check | runs | faults | caught | let through | named | could not test | false alarms | Sam\'s notes missed |',
           '|---|---|---|---|---|---|---|---|---|']
    out += [f"| {r['check']} | {r['runs']} | {r['faults']} | {r['caught']} | {r['let_through']} | {r['named']} | "
            f"{r['could_not_test']} | ? | " + (', '.join(r['missed']) or '0' if tags else '?') + " |" for r in rows]
    if tags:
        out.insert(next(i for i, x in enumerate(out) if x.startswith('| check |')), f"Sam's notes: {len(tags)}, each tagged by the check that should have caught it "
                   f"({sum(1 for t in tags.values() if t and t.strip().lower() == 'none')} 'none'; "
                   f"{sum(1 for t in tags.values() if not t)} untagged).\n")
    bad = [r for r in rec['runs'] if broken(r)]
    if bad:
        out += ['', '## Refused or broken (today\'s pre-flight would not run on this chat\'s files)']
        for r in bad:
            t = r['tail'].strip()
            where = re.findall(r'source/(\w+\.py)", line \d+', t)
            out.append(f"- {r['branch']} ({r['ref']}): {t.splitlines()[-1][:160] if t else '?'}"
                       + (f' (crashed in {where[-1]})' if where else ''))
    return '\n'.join(out) + '\n', rows


def test():
    ok = True

    def check(name, cond):
        nonlocal ok
        ok &= bool(cond)
        print(('PASS ' if cond else 'FAIL ') + name)
    txt = ('header\n - caption "a Maze Runner,": 0.61 s on screen\n - plan: goth has no facing\n'
           ' - clipcheck: COULD NOT TEST: no solids\n - plan: camera 2b looks at nothing\n')
    p = parse(txt)
    check('fault lines are kept under their check', p == {'caption': [p['caption'][0]], 'plan': p['plan'],
                                                        'clipcheck': p['clipcheck']} and len(p['plan']) == 2)
    rec = {'film': 'x', 'runs': [
        {'branch': 'a', 'secs': 10, 'faults': {'plan': ['plan: goth has no facing', 'plan: camera 2b at 3.1 s']}},
        {'branch': 'b', 'secs': 12, 'faults': {'plan': ['plan: camera 2b at 4.5 s'], 'clipcheck': ['clipcheck: COULD NOT TEST']}},
        {'branch': 'c', 'ref': 'cccc', 'secs': 0, 'refused': True, 'tail': 'File "/tmp/r/source/plan.py", line 98, in footprint\\nKeyError: size', 'faults': {}}]}
    md, rows = table('x', rec, exceptions='clipcheck: COULD NOT TEST')
    r = {x['check']: x for x in rows}
    check('a fault gone by the next chat is caught; a moved time is the same fault',
          r['plan']['caught'] == 1 and r['plan']['let_through'] == 1 and r['plan']['faults'] == 2)
    check('a fault named in the Exceptions is named, not let through',
          r['clipcheck']['named'] == 1 and r['clipcheck']['let_through'] == 0 and r['clipcheck']['could_not_test'] == 1)
    check('a refused run is listed apart, not scored, with the check it crashed in', 'Refused or broken' in md and '2 ran' in md
          and 'crashed in plan.py' in md)
    check('the branch list skips posted and review branches', SKIP.search('claude/milburn-posted')
          and not SKIP.search('claude/milburn-chat12'))
    # change 3 (Sam's Y, 20 Nov)
    t = (' - 7.17 s: runner6.footR jumps 74 cm in one frame\n - 4.25 s: runner3 and swinger swap front and back\n'
         ' - AUDIT: PASSES THROUGH: 4.28 s\n - the brief checklist has 8 blank "done?" row(s): 34\n'
         ' - no "Rehearsal clips sent: DATE, FILE" line in the notes\n')
    p2 = parse(t)
    check('time-stamped audit lines are one check, not one row per time', len(p2['AUDIT']) == 3)
    check('a count in the check\'s name does not split it', 'the brief checklist has # blank' in p2)
    check('a two-letter head keeps its quoted words', any(k.startswith('no Rehearsal clips sent') for k in p2))
    gated = {'film': 'y', 'runs': [{'branch': 'a', 'secs': 5, 'exit': 2, 'refused': True,
                                    'tail': 'preflight refuses: the brief is not done', 'faults': {'7.17 s': ['7.17 s: a jumps']}},
                                   {'branch': 'b', 'secs': 5, 'exit': 1, 'faults': {}}]}
    md2, rows2 = table('y', gated)
    check('a run that says "refuses" but lists faults is scored, and its old groups are regrouped',
          '2 ran' in md2 and [r['check'] for r in rows2] == ['AUDIT'] and rows2[0]['caught'] == 1)
    check('a crash with no fault lines is still broken', broken({'faults': {}, 'exit': 1, 'refused': True})
          and not broken({'faults': {}, 'exit': 0}))
    # change 1 (Sam's Y, 20 Nov): in a fresh copy with no marker file, a check saves under the film it names
    d = tempfile.mkdtemp(prefix='record-test-')
    os.makedirs(os.path.join(d, 'source'))
    os.makedirs(os.path.join(d, 'notes'))
    for f in ('ledger.py', 'report.py', 'checkreplay.py'):
        shutil.copy(os.path.join(ROOT, 'source', f), os.path.join(d, 'source', f))
    open(os.path.join(d, 'notes', 'filmx.md'), 'w').write('# notes\n')
    code = ('import report; report.summarise("plan", ["plan: goth has no facing"]); '
            'report.summarise("caption", [])')
    env = dict(os.environ, CHECK_RUN='r1')
    env.pop('CHECK_FILM', None)
    a = subprocess.run([sys.executable, '-c', code, 'filmx'], cwd=os.path.join(d, 'source'), env=env,
                       capture_output=True, text=True)
    b = subprocess.run([sys.executable, '-c', code.replace('goth', 'camera'), 'filmx'], env=dict(env, CHECK_RUN='r2'),
                       cwd=os.path.join(d, 'source'), capture_output=True, text=True)
    n = subprocess.run([sys.executable, '-c', code], cwd=os.path.join(d, 'source'), env=env, capture_output=True, text=True)
    jl = os.path.join(d, 'notes', 'ledger', 'filmx', 'checks.jsonl')
    rows_ = [json.loads(x) for x in open(jl)] if os.path.exists(jl) else []
    check('no marker file: every check run is saved under the film in its command, clean ones too',
          not os.path.exists(os.path.join(d, 'notes', 'ledger', '.current')) and len(rows_) == 4
          and {x['run'] for x in rows_} == {'r1', 'r2'} and not a.stderr.strip() and not b.stderr.strip())
    check('no film named: it says so in one line, once', n.stdout.count('check record: not saved') == 1)
    sys.path.insert(0, os.path.join(d, 'source'))
    import importlib
    lg = importlib.import_module('ledger')
    importlib.reload(lg)
    md3, rows3 = table('filmx', lg.checkruns('filmx'))
    r3 = {x['check']: x for x in rows3}
    check('each fault\'s fate from comparing runs (gone = caught, still there = let through)',
          r3['plan']['caught'] == 1 and r3['plan']['let_through'] == 1 and 'caption' not in r3)
    sys.path.remove(os.path.join(d, 'source'))
    shutil.rmtree(d, ignore_errors=True)
    # change 2 (Sam's Y, 20 Nov): notes tagged by the check that should have caught them
    md4, rows4 = table('x', rec, tags={'1': 'plan', '2': 'none', '3': 'HEAD LIFE', '4': None})
    r4 = {x['check']: x for x in rows4}
    check('a tagged note is counted against its check, even one that listed nothing',
          r4['plan']['missed'] == ['1'] and r4['HEAD LIFE']['missed'] == ['3'] and "Sam's notes: 4" in md4
          and '1 untagged' in md4 and md4.index("Sam's notes: 4") < md4.index('| check |'))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import handover
    nf = os.path.join(tempfile.mkdtemp(), 'n.md')
    open(nf, 'w').write('## Notes\n| # | shot | time | note | line | should have caught | status |\n|---|---|---|---|---|---|---|\n'
                        '| 1 | 2 | 3 s | arm through body | x | AUDIT | fixed |\n| 2 | 3 | | too fast | | | open |\n'
                        '| 3 | | | | | | open |\n## Other\n| 9 | a | b | c |\n')
    check('the handover reads each note\'s tag; a blank one is untagged; an empty row is not a note',
          handover.note_tags(nf) == {'1': 'AUDIT', '2': ''})
    open(nf, 'w').write('## Notes\n| # | shot | time | note | line | status |\n|---|---|---|---|---|---|\n| 1 | 2 | 3 s | arm | x | open |\n')
    check('a notes table with no tag column leaves every note untagged', handover.note_tags(nf) == {'1': None})
    print('ALL PASS' if ok else 'SOME FAILED')
    return ok


if __name__ == '__main__':
    a = sys.argv[1:]
    opt = lambda k: a[a.index(k) + 1] if k in a else None
    if not a:
        print(__doc__)
        sys.exit(1)
    if a[0] == 'test':
        sys.exit(0 if test() else 1)
    if a[0] == 'branches':
        print('\n'.join(branches(a[1])))
    elif a[0] == 'run':
        run(a[1], opt('--only').split(',') if opt('--only') else None, int(opt('--max')) if opt('--max') else None)
    elif a[0] == 'table':
        nf = os.path.join(ROOT, 'notes', a[1] + '.md')
        exc = open(nf).read() if os.path.exists(nf) else ''
        exc = exc.split('## Exceptions', 1)[1][:20000] if '## Exceptions' in exc else ''
        if '--record' in a:                         # change 1: the live record (every run kept), not the replay
            import ledger
            md, _ = table(a[1], ledger.checkruns(a[1]), exc, ledger.load(a[1]).get('notes_tags'))
            md = md.replace("today's checks on each chat branch", 'every check run this film, from its record')
            dest = os.path.join(ledger._paths(a[1])[2], 'check-table.md')
        else:
            md, _ = table(a[1], exceptions=exc)
            dest = os.path.join(OUT, a[1] + '.md')
        open(dest, 'w').write(md)
        print(md[:3000])
