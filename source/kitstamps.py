#!/usr/bin/env python3
"""kitstamps: which files each kit test reads, and a stamp per passing test, so only the tests whose files changed run
again (Sam's pick 1, 25 Nov, notes/proposals/kit-tests-when.md: "test only what changed, every time").

How a test's reads are found (fail-shut: anything unsure counts as read):
  * every function that runs in the test (Python's own per-function start event, switched off after its first sighting
    and switched back on for the next test, so it costs almost nothing): its file;
  * every module an `import` names during the test, even one already loaded;
  * one step out: every project module or function the files above hold by name (a constant read from another module,
    or a fast compiled function whose own lines Python never sees, still counts);
  * every file opened for reading and every folder listed inside the project (a folder's stamp is its list of names);
  * a test that starts another program (Python, a project script, git on the project) counts as reading ALL of
    source/ and .claude/ (fixed old versions read with `git show COMMIT:` and ffmpeg on its own files do not);
  * the test's own lines in kittests.py (the function, not the whole file, so adding a test re-runs nothing else).
A test whose files changed WHILE it ran leaves no stamp. A test never stamped green, or stamped on another setup
(Python or library versions), is stale.

The record: notes/kittest-stamps.tsv, committed, one line per green test (name, stamp, seconds, when, setup, reads);
kept on both sides when two chains merge (.gitattributes merge=union); a test is fresh when any of its lines matches
the files as they are now.

    python3 source/kitstamps.py stale            the tests that would run now, and the estimated time
    python3 source/kitstamps.py reads NAME       what a test read on its last green run
    python3 source/kitstamps.py replay [DAYS]    Step 0: replay the last chats' changes against the recorded reads
"""
import ast
import builtins
import hashlib
import io
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RECORD = os.path.join(ROOT, 'notes', 'kittest-stamps.tsv')
KITTESTS = os.path.join(HERE, 'kittests.py')
ALL = 'ALL'                                     # "this test started another program": reads all of source/ and .claude/
ALL_DIRS = ('source', '.claude')
KEEP = 3                                        # lines kept per test (newest), so the record stays small
SKIP_PARTS = ('/.git/', '/__pycache__/')
HARNESS = {'start', 'stop', '_start_event', '_open', '_imp', '_listdir', '_scandir', '_popen', '_from_importer', '_rel',
           '_program', '_one_step_out', 'tracer', 'traced'}


# ------------------------------------------------------------------------------------------------ the setup a stamp holds
def setup_tag():
    """Python and the drawing libraries' versions: a green on another setup is not a green here (verdict F4)."""
    out = [f'py{sys.version_info[0]}.{sys.version_info[1]}']
    for m in ('numpy', 'PIL', 'numba', 'scipy', 'cv2'):
        try:
            mod = __import__(m)
            out.append(f'{m}{getattr(mod, "__version__", "?")}')
        except Exception:
            out.append(f'{m}-')
    return ' '.join(out)


# ------------------------------------------------------------------------------------------------ hashing what was read
def _rel(p):
    if not p or p.startswith('<'):             # Python's built-in modules (<frozen os>, <string>): not files
        return None
    try:
        a = os.path.realpath(p)
    except Exception:
        return None
    if not a.startswith(ROOT + os.sep) or any(s in a + '/' for s in SKIP_PARTS):
        return None
    return os.path.relpath(a, ROOT)


def _file_hash(rel):
    p = os.path.join(ROOT, rel)
    if os.path.isdir(p):
        try:
            names = sorted(os.listdir(p))
        except OSError:
            return 'unreadable'
        return 'dir:' + hashlib.sha1('\n'.join(names).encode()).hexdigest()[:16]
    try:
        with io.FileIO(p, 'r') as f:
            return hashlib.sha1(f.read()).hexdigest()[:16]
    except OSError:
        return 'missing'


_FN_SRC = {}


def _fn_sources():
    """kittests.py's top-level functions, each with its own lines (decorator included)."""
    st = os.stat(KITTESTS)
    key = (st.st_mtime_ns, st.st_size)
    if _FN_SRC.get('key') != key:
        txt = open(KITTESTS, encoding='utf-8').read()
        lines = txt.splitlines(keepends=True)
        out = {}
        for node in ast.parse(txt).body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start = min([node.lineno] + [d.lineno for d in getattr(node, 'decorator_list', [])])
                out[node.name] = ''.join(lines[start - 1:node.end_lineno])
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):   # module-level names (HERE, TESTS, constants)
                for t in (node.targets if isinstance(node, ast.Assign) else [node.target]):
                    if isinstance(t, ast.Name):
                        out[t.id] = ''.join(lines[node.lineno - 1:node.end_lineno])
        _FN_SRC.clear()
        _FN_SRC.update(key=key, fns=out)
    return _FN_SRC['fns']


def _all_hash():
    r = subprocess.run(['git', '-C', ROOT, 'ls-files', '-s', '--', *ALL_DIRS], capture_output=True, text=True)
    h = hashlib.sha1(r.stdout.encode())
    # tracked files edited but not committed: their content too
    d = subprocess.run(['git', '-C', ROOT, 'diff', '--name-only', '--', *ALL_DIRS], capture_output=True, text=True)
    for rel in sorted(filter(None, d.stdout.split('\n'))):
        h.update(f'{rel}\0{_file_hash(rel)}\n'.encode())
    u = subprocess.run(['git', '-C', ROOT, 'ls-files', '-o', '--exclude-standard', '--', *ALL_DIRS],
                       capture_output=True, text=True)
    for rel in sorted(filter(None, u.stdout.split('\n'))):
        h.update(f'{rel}\0{_file_hash(rel)}\n'.encode())
    return h.hexdigest()[:16]


def item_hash(item, cache=None):
    if cache is not None and item in cache:
        return cache[item]
    if item == ALL:
        v = _all_hash()
    elif '::' in item:
        v = hashlib.sha1(_fn_sources().get(item.split('::', 1)[1], '<gone>').encode()).hexdigest()[:16]
    else:
        v = _file_hash(item)
    if cache is not None:
        cache[item] = v
    return v


def stamp(reads, tag=None, cache=None):
    h = hashlib.sha1((tag or setup_tag()).encode())
    for it in sorted(reads):
        h.update(f'{it}\0{item_hash(it, cache)}\n'.encode())
    return h.hexdigest()[:20]


# ------------------------------------------------------------------------------------------------ the tracer
def _from_importer():
    """A folder listed by Python's own package finder (importlib.metadata looking for installed libraries), not by
    the test: not a read."""
    f = sys._getframe(2)
    return 'importlib' in f.f_code.co_filename


class Tracer:
    """Watches one test at a time. start(); run the test; reads = stop()."""
    TOOL = 4                                    # a sys.monitoring tool id (0-5); 4 and 5 are free for programs like this

    def __init__(self):
        self.on = False
        self.codes = set()
        self.reads, self.written = set(), set()
        self.names = set()                      # kittests.py functions that ran
        self.mods = set()                       # module names an import statement named
        self.all = False
        self.t0 = 0.0
        self._real = {}
        self._mon = hasattr(sys, 'monitoring')
        if self._mon:
            try:
                sys.monitoring.use_tool_id(self.TOOL, 'kitstamps')
            except ValueError:
                self._mon = False
        if self._mon:
            sys.monitoring.register_callback(self.TOOL, sys.monitoring.events.PY_START, self._start_event)
        self._install()

    # each function's first run in a test: note its file, then switch that function's event off until the next test
    def _start_event(self, code, offset):
        if self.on:
            self.codes.add(code)
        return sys.monitoring.DISABLE

    def _install(self):
        me = self
        real_open = builtins.open
        real_import = builtins.__import__
        real_listdir, real_scandir = os.listdir, os.scandir
        real_popen = subprocess.Popen.__init__
        self._real = dict(open=real_open, imp=real_import, listdir=real_listdir, scandir=real_scandir, popen=real_popen)

        def _open(file, mode='r', *a, **k):
            if me.on and isinstance(file, (str, bytes, os.PathLike)):
                rel = _rel(os.fsdecode(file))
                if rel:
                    m = mode if isinstance(mode, str) else 'r'
                    (me.written if any(c in m for c in 'wax+') else me.reads).add(rel)
            return real_open(file, mode, *a, **k)

        def _imp(name, globals=None, locals=None, fromlist=(), level=0):
            mod = real_import(name, globals, locals, fromlist, level)
            if me.on:
                me.mods.add(getattr(mod, '__name__', name))
                for f in fromlist or ():
                    sub = getattr(mod, f, None)
                    if hasattr(sub, '__file__'):
                        me.mods.add(sub.__name__)
            return mod

        def _listdir(path='.'):
            if me.on and isinstance(path, (str, bytes, os.PathLike)) and not _from_importer():
                rel = _rel(os.fsdecode(path))
                if rel:
                    me.reads.add(rel)
            return real_listdir(path)

        def _scandir(path='.'):
            if me.on and isinstance(path, (str, bytes, os.PathLike)) and not _from_importer():
                rel = _rel(os.fsdecode(path))
                if rel:
                    me.reads.add(rel)
            return real_scandir(path)

        def _popen(self_, args, *a, **k):
            if me.on:
                me._program(args, k.get('cwd'))
            return real_popen(self_, args, *a, **k)

        builtins.open = io.open = _open
        builtins.__import__ = _imp
        os.listdir, os.scandir = _listdir, _scandir
        subprocess.Popen.__init__ = _popen

    def _program(self, args, cwd):
        """Another program started: ALL unless it is plainly reading nothing that can change (verdict F2)."""
        argv = [os.fsdecode(a) for a in args] if isinstance(args, (list, tuple)) else [os.fsdecode(args)]
        exe = os.path.basename(argv[0]) if argv else ''
        if 'ffmpeg' in exe:                     # ffmpeg reads only the files named; project ones count as read
            for a in argv[1:]:
                rel = _rel(a) if os.path.isabs(a) or os.path.exists(a) else None
                if rel and os.path.exists(os.path.join(ROOT, rel)):
                    self.reads.add(rel)
            return
        if exe == 'tar' or exe in ('mkdir', 'rm', 'cp'):
            return
        if exe == 'git':
            rest = argv[1:]
            where = cwd
            if rest[:1] == ['-C'] and len(rest) > 1:
                where, rest = rest[1], rest[2:]
            if where and not _rel(where) and os.path.realpath(where) != ROOT:
                return                          # a scratch repository of the test's own
            if rest[:1] == ['init']:
                return
            if rest[:1] in (['show'], ['archive']) and len(rest) > 1 and re.match(r'^[0-9a-f]{7,40}(~\d*)?[:]?', rest[1]):
                return                          # a fixed old version: it never changes
        self.all = True

    def start(self):
        self.codes, self.reads, self.written, self.mods = set(), set(), set(), set()
        self.all = False
        self.t0 = time.time()
        if self._mon:
            sys.monitoring.set_events(self.TOOL, sys.monitoring.events.PY_START)
            sys.monitoring.restart_events()
        self.on = True

    def stop(self):
        """The test's reads as stamp items, or None when a file it read changed while it ran (no stamp then)."""
        self.on = False
        if self._mon:
            sys.monitoring.set_events(self.TOOL, 0)
        if not self._mon:
            return None                         # no per-function events on this Python: never stamp (fail-shut)
        files, names = set(), set()
        kt = os.path.realpath(KITTESTS)
        me = os.path.realpath(__file__)
        for c in self.codes:
            fn = c.co_filename
            if os.path.realpath(fn) == me and c.co_name in HARNESS:
                continue                        # the tracer's own watching, not something the test read
            if os.path.realpath(fn) == kt:
                names.add(c.co_qualname.split('.')[0])
            else:
                rel = _rel(fn)
                if rel:
                    files.add(rel)
        for m in self.mods:
            f = getattr(sys.modules.get(m), '__file__', None)
            rel = _rel(f) if f else None
            if rel and rel != os.path.relpath(kt, ROOT):
                files.add(rel)
        files |= _one_step_out(files)
        files |= {r for r in self.reads if os.path.exists(os.path.join(ROOT, r))}
        files -= self.written
        files.discard(os.path.relpath(kt, ROOT))
        for rel in files:                       # changed while the test ran: the stamp would lie
            try:
                p = os.path.join(ROOT, rel)
                if not os.path.isdir(p) and os.stat(p).st_mtime > self.t0:
                    return None
            except OSError:
                pass
        items = files | {f'source/kittests.py::{n}' for n in names if n not in ('<module>',)}
        if self.all:
            items.add(ALL)
        return items


_ONE = []


def tracer():
    """The one tracer of this process (it patches open/import/listing once; a second would wrap them twice)."""
    if not _ONE:
        _ONE.append(Tracer())
    return _ONE[0]


def traced(fn):
    """Run fn inside the running test, traced on its own: (fn's result, its reads). The outer test's record is
    kept and gets these reads too (used by the kit test that proves the stamps)."""
    t = tracer()
    keep = (t.on, t.codes, t.reads, t.written, t.mods, t.all, t.t0)
    t.start()
    try:
        out = fn()
    finally:
        reads = t.stop()
        on, codes, rd, wr, mods, al, t0 = keep
        t.codes, t.reads, t.written, t.mods = codes | t.codes, rd | t.reads, wr | t.written, mods | t.mods
        t.all, t.t0 = al or t.all, t0
        if on:
            t.on = True
            if t._mon:
                sys.monitoring.set_events(t.TOOL, sys.monitoring.events.PY_START)
    return out, reads


def _one_step_out(files):
    """The project modules and functions each read file holds by name (a constant, a compiled function)."""
    byfile = {}
    for m in list(sys.modules.values()):
        f = getattr(m, '__file__', None)
        rel = _rel(f) if f else None
        if rel:
            byfile.setdefault(rel, m)
    out = set()
    for rel in files:
        m = byfile.get(rel)
        if m is None:
            continue
        for v in list(vars(m).values()):
            tgt = None
            if hasattr(v, '__file__') and isinstance(getattr(v, '__name__', None), str):
                tgt = v.__file__
            else:
                v = getattr(v, 'py_func', v)    # a numba function: its Python original
                mn = getattr(v, '__module__', None)
                if isinstance(mn, str) and mn in sys.modules:
                    tgt = getattr(sys.modules[mn], '__file__', None)
            r = _rel(tgt) if isinstance(tgt, str) else None
            if r:
                out.add(r)
    return out


# ------------------------------------------------------------------------------------------------ the record
def _rows(path=RECORD):
    out = []
    if not os.path.exists(path):
        return out
    for ln in open(path, encoding='utf-8'):
        p = ln.rstrip('\n').split('\t')
        if len(p) >= 6 and not ln.startswith('#'):
            out.append(dict(name=p[0], stamp=p[1], secs=float(p[2] or 0), when=p[3], setup=p[4],
                            reads=[x for x in p[5].split(',') if x]))
    return out


def write_green(results, path=RECORD):
    """results: [(name, reads, secs)] for tests that passed. Appends, then keeps the newest KEEP lines per test."""
    if not results:
        return
    tag = setup_tag()
    cache = {}
    now = datetime.now(timezone.utc).isoformat(timespec='minutes')
    rows = _rows(path)
    for name, reads, secs in results:
        rows.append(dict(name=name, stamp=stamp(reads, tag, cache), secs=secs, when=now, setup=tag, reads=sorted(reads)))
    keep, seen = [], {}
    for r in reversed(rows):
        k = (r['name'], r['stamp'])
        if k in seen:
            continue
        seen[k] = 1
        if sum(1 for x in keep if x['name'] == r['name']) < KEEP:
            keep.append(r)
    keep.reverse()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write('# kit-test stamps (source/kitstamps.py): name, stamp, seconds, when, setup, files read. '
                'One line per green test; merge keeps both sides.\n')
        for r in sorted(keep, key=lambda r: (r['name'], r['when'])):
            f.write('\t'.join([r['name'], r['stamp'], f"{r['secs']:.1f}", r['when'], r['setup'], ','.join(r['reads'])]) + '\n')
    os.replace(tmp, path)


def stale(names, path=RECORD):
    """(stale names in the order given, {name: last known seconds}). A test is fresh when one of its green lines,
    on this setup, matches the files as they are now."""
    tag = setup_tag()
    cache = {}
    rows = _rows(path)
    by = {}
    for r in rows:
        by.setdefault(r['name'], []).append(r)
    out, secs = [], {}
    for n in names:
        mine = by.get(n, [])
        if mine:
            secs[n] = mine[-1]['secs']
        if not any(r['setup'] == tag and stamp(r['reads'], tag, cache) == r['stamp'] for r in mine):
            out.append(n)
    return out, secs


def test_names():
    return re.findall(r'^@test\ndef (\w+)', open(KITTESTS, encoding='utf-8').read(), re.M)


def estimate(names, secs):
    known = [secs[n] for n in names if n in secs]
    unknown = len(names) - len(known)
    avg = (sum(known) / len(known)) if known else 8.0
    return sum(known) + unknown * avg


def say_minutes(s):
    return f'{s / 60:.0f} min' if s >= 90 else f'{s:.0f} s'


# ------------------------------------------------------------------------------------------------ finish.py's gate
def run_stale(log=None):
    """Run the stale kit tests now (kittests.py --stale), the result to notes/logs/kittests-last.log."""
    log = log or os.path.join(ROOT, 'notes', 'logs', 'kittests-last.log')
    os.makedirs(os.path.dirname(log), exist_ok=True)
    with open(log, 'w') as f:
        subprocess.run([sys.executable, KITTESTS, '--stale'], stdout=f, stderr=subprocess.STDOUT, cwd=ROOT, timeout=2400)
    return log


def finish_gate(stale_fn=None, run_fn=None):
    """Change 2 (Sam's pick 1, 25 Nov): no animatic or final on files a kit test has not passed on. The stale tests
    run first (saying how long); what is still not fresh after that refuses, by name. '' when every test is fresh."""
    names = test_names()
    st, secs = (stale_fn or (lambda: stale(names)))()
    if not st:
        print(f'kit tests: all {len(names)} fresh on their stamps (nothing changed since each passed)')
        return ''
    est = estimate(st, secs)
    print(f'kit tests: {len(st)} stale (files changed since their last pass): running them first, about '
          f'{say_minutes(est)}', flush=True)
    t0 = time.time()
    try:
        log = (run_fn or run_stale)()
    except subprocess.TimeoutExpired:
        log = None
    print(f'kit tests: the run took {say_minutes(time.time() - t0)}')
    left, _ = (stale_fn or (lambda: stale(names)))()
    if not left:
        return ''
    reds = []
    if log and os.path.exists(log):
        reds = re.findall(r'^FAIL (\w+): (.*)$', open(log, encoding='utf-8', errors='replace').read(), re.M)
    why = '; '.join(f'{n}: {d[:80]}' for n, d in reds if n in left) or ', '.join(left)
    return (f'{len(left)} kit test(s) without a pass on the current files ({why}): fix them (or the tool they test), '
            'then run finish again (log: notes/logs/kittests-last.log)')


# ------------------------------------------------------------------------------------------------ Step 0: the replay
def _chats(days):
    """The last DAYS of commits, grouped by the chat that made them (its Claude-Session line): files changed, and
    which kittests.py functions changed (from the diff's function lines)."""
    r = subprocess.run(['git', '-C', ROOT, 'log', f'--since={days} days ago', '--no-merges', '-U0', '-p',
                        '--format=@@%H\t%cI\t%(trailers:key=Claude-Session,valueonly,separator=)'],
                       capture_output=True, text=True, errors='replace')
    chats, cur, order, path, pend = {}, None, [], None, []
    for ln in r.stdout.splitlines():
        if ln.startswith('@@') and not ln.startswith('@@ '):
            h, when, sess = (ln[2:].split('\t') + ['', ''])[:3]
            sess = sess.strip().split('/')[-1] or f'nosession-{h[:8]}'
            pend.append((h, sess))
            cur = chats.setdefault(sess, dict(files=set(), fns=set(), when=when, commits=0))
            if sess not in order:
                order.append(sess)
            cur['commits'] += 1
            cur['when'] = min(cur['when'], when)
        elif ln.startswith('+++ b/') and cur is not None:
            path = ln[6:]
            cur['files'].add(path)
        elif ln.startswith('--- a/') and cur is not None:
            cur['files'].add(ln[6:])            # a deleted file counts as changed
        elif ln.startswith('@@ ') and cur is not None and path == 'source/kittests.py':
            m = re.search(r'@@ .*?@@ (?:@test\s*)?def (\w+)', ln)
            if m:
                cur['fns'].add(m.group(1))
        elif ln.startswith('+def ') and cur is not None and path == 'source/kittests.py':
            cur['fns'].add(ln[5:].split('(')[0])
    # automatic commits (ledger lines, Sam's saved messages) carry no chat line: they join the chat before them
    last = None
    for h, sess in reversed(pend):              # oldest first
        if not sess.startswith('nosession-'):
            last = sess
        elif last and sess in chats:
            c = chats.pop(sess)
            chats[last]['files'] |= c['files']
            chats[last]['fns'] |= c['fns']
            chats[last]['commits'] += c['commits']
    return [(s, chats[s]) for s in order if s in chats]


def _shared(path, prefixes):
    """The path rule's idea of shared: under source/ (not a film's own code), .claude/hooks/, guides/kit-*.md."""
    if path.startswith('.claude/hooks/') or re.match(r'guides/kit-.*\.md$', path):
        return True
    if path.startswith('source/') and path.endswith('.py'):
        b = os.path.basename(path)
        return not any(b.startswith(p) for p in prefixes)
    return False


def _film_prefixes():
    sys.path.insert(0, HERE)
    try:
        import handover
        return tuple(handover._film_prefixes())
    except Exception:
        names = [os.path.splitext(f)[0] for f in os.listdir(os.path.join(ROOT, 'story')) if f.endswith('.md')]
        return tuple(n.replace('-', '_') for n in names)


def replay(days=7, path=RECORD, reds_log=None):
    rows = _rows(path)
    reads = {}
    for r in rows:
        reads[r['name']] = set(r['reads'])     # the newest line's reads
    secs = {r['name']: r['secs'] for r in rows}
    names = test_names()
    missing = [n for n in names if n not in reads]
    prefixes = _film_prefixes()
    chats = _chats(days)
    full = sum(secs.get(n, 0) for n in names)
    tot = dict(chats=0, film_only=0, path_runs=0, stamp_runs=0, none=0, full_min=0.0, path_min=0.0, stamp_min=0.0)
    per = []
    for sess, c in chats:
        files = c['files']
        if not files:
            continue
        tot['chats'] += 1
        shared = any(_shared(f, prefixes) for f in files)
        tot['film_only'] += not shared
        hit = []
        for n in names:
            rd = reads.get(n)
            if rd is None or ALL in rd and any(f.startswith(d + '/') for d in ALL_DIRS for f in files) \
                    or rd & files or any(f.split('::')[1] in c['fns'] for f in rd if '::' in f):
                hit.append(n)
        tot['path_runs'] += shared
        tot['stamp_runs'] += bool(hit)
        tot['none'] += not hit
        tot['full_min'] += full / 60
        tot['path_min'] += (full if shared else 0) / 60
        tot['stamp_min'] += sum(secs.get(n, 0) for n in hit) / 60
        per.append((sess, c['when'][:16], len(files), shared, len(hit)))
    # past reds: the first time each test went red, and the commits since the handover before it (another chat's):
    # did any touch what the test reads (its reads as recorded now: named, they may have differed then)?
    reds_log = reds_log or os.path.join(ROOT, 'notes', 'logs', 'kittest-reds.log')
    red_rows = [r for r in (ln.rstrip('\n').split('\t') for ln in open(reds_log, encoding='utf-8'))
                if len(r) >= 3] if os.path.exists(reds_log) else []
    red_rows.sort(key=lambda r: r[0])
    first_red, prev_time = {}, {}
    for i, (when, sid, lst) in enumerate(r[:3] for r in red_rows):
        before = [r[0] for r in red_rows[:i] if r[1] != sid]
        for n in filter(None, lst.split(',')):
            if n not in first_red:
                first_red[n] = (when, before[-1] if before else _minus(when, 24))
    red_check = []
    for n, (when, since) in sorted(first_red.items()):
        rd = reads.get(n)
        if rd is None:
            red_check.append((n, when, 'no record of its reads (gone or never green): it always runs, so caught'))
            continue
        r = subprocess.run(['git', '-C', ROOT, 'log', f'--since={_minus(since, 2)}', f'--until={when}', '-U0',
                            '--format=@@C', '-p', '--', '.'], capture_output=True, text=True)
        touched, fns = set(), set()
        for ln in r.stdout.splitlines():
            if ln.startswith('+++ b/'):
                cur = ln[6:]
                touched.add(cur)
            elif ln.startswith('@@ ') and touched and cur == 'source/kittests.py':
                m = re.search(r'@@ (?:@test\s*)?def (\w+)', ln[2:])
                if m:
                    fns.add(m.group(1))
        hit = sorted(rd & touched) + sorted(f for f in rd if '::' in f and f.split('::')[1] in fns)
        if ALL in rd and any(t.startswith(tuple(d + '/' for d in ALL_DIRS)) for t in touched):
            hit.append('ALL (it starts another program)')
        red_check.append((n, when, f'caught: {len(hit)} of its files changed before it went red ({", ".join(hit[:3])}'
                          f'{" ..." if len(hit) > 3 else ""})' if hit else
                          'MISSED: nothing it reads changed between the green and the red'))
    return dict(tot=tot, per=per, missing=missing, red_check=red_check, tests=len(names), full=full)


def _minus(iso, hours):
    from datetime import timedelta
    t = datetime.fromisoformat(iso)
    return (t - timedelta(hours=hours)).isoformat()


def main(argv):
    cmd = argv[0] if argv else 'stale'
    if cmd == 'stale':
        names = test_names()
        st, secs = stale(names)
        print(f'kitstamps: {len(st)} of {len(names)} kit tests stale (about {say_minutes(estimate(st, secs))} to run)')
        for n in st:
            print('  ' + n)
        return 0
    if cmd == 'reads' and len(argv) > 1:
        for r in _rows():
            if r['name'] == argv[1]:
                print(r['when'], r['stamp'], f"{r['secs']:.1f}s", r['setup'])
                print('  ' + '\n  '.join(r['reads']))
        return 0
    if cmd == 'replay':
        days = int(argv[1]) if len(argv) > 1 else 7
        R = replay(days)
        t = R['tot']
        print(f"replay of the last {days} days: {t['chats']} chats; {R['tests']} tests, a full run {R['full'] / 60:.1f} min")
        print(f"  today (a full run every chat): {t['chats']} runs, {t['full_min']:.0f} min")
        print(f"  path rule (shared code changed): {t['path_runs']} runs, {t['path_min']:.0f} min; "
              f"{t['film_only']} chats film-only")
        print(f"  stamps per test: {t['stamp_runs']} chats re-run something, {t['none']} re-run nothing; "
              f"{t['stamp_min']:.0f} min in all")
        if R['missing']:
            print(f"  tests with no recorded reads (always run): {', '.join(R['missing'])}")
        print('  past reds (kittest-reds.log), first time each went red:')
        for n, when, v in R['red_check']:
            print(f'    {n} ({when}): {v}')
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
