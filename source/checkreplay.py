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


def parse(text):
    """Fault lines -> {check: [fault, ...]}. A check is the words before the first ':' (quotes dropped)."""
    out = {}
    for ln in text.splitlines():
        m = LINE.match(ln)
        if not m:
            continue
        body = m.group(1)
        head = re.split(r'\s*["“(]', body.split(':', 1)[0])[0].strip() or 'other'
        head = re.sub(r'\s+', ' ', head)[:40]
        out.setdefault(head, []).append(body[:200])
    return out


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
        refused = 'REFUSE' in txt.upper()[:3000] or ('Traceback' in txt and not LINE.search(txt))
        faults = parse(txt)
        rec['runs'].append({'branch': b, 'ref': ref, 'files': n, 'secs': secs, 'exit': code, 'refused': refused,
                            'faults': faults, 'tail': txt[-600:] if refused or code not in (0, 1) else ''})
        json.dump(rec, open(jf, 'w'), indent=1)
        git('worktree', 'remove', '--force', d)
        shutil.rmtree(o, ignore_errors=True)
        print(f'checkreplay: {b} ({ref}, {n} film files): {sum(len(v) for v in faults.values())} faults in '
              f'{len(faults)} checks, {secs} s' + (' REFUSED or broken: see its tail' if refused else ''))
    return rec


def table(film, rec=None, exceptions=''):
    rec = rec or json.load(open(os.path.join(OUT, film + '.json')))
    runs = [r for r in rec['runs'] if not r.get('refused')]
    checks = sorted({c for r in runs for c in r['faults']})
    rows = []
    for c in checks:
        seen = [{_key(f) for f in r['faults'].get(c, [])} for r in runs]
        caught = sum(len(a - b) for a, b in zip(seen, seen[1:]))
        last = seen[-1] if seen else set()
        named = sum(1 for k in last if k[:30] in exceptions)
        rows.append({'check': c, 'runs': sum(1 for s in seen if s), 'faults': len(set().union(*seen)),
                     'caught': caught, 'let_through': len(last) - named, 'named': named,
                     'could_not_test': sum(1 for r in runs for f in r['faults'].get(c, []) if 'COULD NOT TEST' in f)})
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
            f"{r['could_not_test']} | ? | ? |" for r in rows]
    bad = [r for r in rec['runs'] if r.get('refused')]
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
        md, _ = table(a[1], exceptions=exc)
        open(os.path.join(OUT, a[1] + '.md'), 'w').write(md)
        print(md[:3000])
