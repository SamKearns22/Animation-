#!/usr/bin/env python3
"""touch: "if I change this, what else uses it, and which checks must I rerun?" in one step and about 20 lines
(cost-spike fix steps 1-2, Sam's Y, 27 Nov; notes/proposals/cost-spike-fix.md). Fixing chats spent ~35 steps a note,
most of them searching and tracing by hand; page.py show guesses from a note's words, this answers exactly.

MAP
  build() ...... the index, from the code's own structure (ast), never from words: every top-level def, class method
                 and module-level table in source/*.py and .claude/hooks/*.py, and every exact use of one. A use is a
                 name resolved through the file's imports (`import body as B` ... `B.arm()` -> body.arm; `from people
                 import head` ... `head()` -> people.head; a same-file name; `self.m()` in a class -> Class.m). Uses
                 that cannot be resolved (`film.frame_image()` on a parameter) are kept apart as name-only "maybe".
                 Files are parsed once and kept until they change (~/.claude/touch/), so a query after an edit costs
                 a second; a full build is ~8 s and runs at session start (.claude/hooks/setup.sh).
  lookup() ..... NAME -> the def(s): `head_faults`, `people.head_faults`, `Class.method`. Not a def name: the defs whose
                 name holds the word (a find, ranked shortest first).
  report() ..... one def: where (file:line-end), who calls it (film code and shared code apart, each with the calling
                 def and line), name-only maybes (count + first few), the checks it feeds (callers named like a check:
                 *_faults, check_*, *_guard ...), and the kit tests whose calls reach it (followed back through the
                 callers, nearest first), ending in the one command that reruns just those.
  rerun() ...... step 2: after an edit, the defs whose lines changed (git diff against HEAD, or --since REF) -> the kit
                 tests that reach them, as one 'RERUN:' line. Never runs them; the chat decides.
  stale_faults() handover.py end: an index missing or older than the code, or a file the index cannot parse (its
                 uses would be invisible), is a fault.
  test() ....... kittest touch_index: the fault it catches is the hand trace that missed a caller (see the test).

    python3 source/touch.py NAME [-n 20]       who uses NAME, which checks cover it (never read the index whole)
    python3 source/touch.py rerun [--since REF] the kit tests touching the functions changed since HEAD (or REF)
    python3 source/touch.py build              rebuild now (prints files, defs, uses, seconds)
    python3 source/touch.py test               the kit test
"""
import ast
import json
import os
import pickle
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.environ.get('TOUCH_CACHE') or os.path.expanduser('~/.claude/touch')
DIRS = ('source', os.path.join('.claude', 'hooks'))
CHECK_NAME = re.compile(r'(_faults$|^check_|_check$|gate|^audit|_audit$|_guard$|^lint|^test$)')
VERSION = 6


# ------------------------------------------------------------------------------------------------ one file -> facts
def _files(root=ROOT):
    out = []
    for d in DIRS:
        p = os.path.join(root, d)
        if os.path.isdir(p):
            out += [os.path.join(d, f) for f in sorted(os.listdir(p)) if f.endswith('.py')]
    return out


def _mod(rel):
    return os.path.basename(rel)[:-3]


class _Scope(ast.NodeVisitor):
    """The names one def uses: resolved (module, name) pairs and name-only attributes."""

    def __init__(self, fx, aliases, froms, cls=None):
        self.fx, self.aliases, self.froms, self.cls = fx, aliases, froms, cls
        self.local = set()
        self.uses = []            # (target 'mod.name', line, how) how: call/use/sets
        self.maybe = []           # (attr, line)
        self.strings = []
        self.known = set()

    def visit_Name(self, n):
        if isinstance(n.ctx, ast.Load) and n.id not in self.local:
            if n.id in self.froms:
                self.uses.append(('%s.%s' % self.froms[n.id], n.lineno, 'use'))
            elif n.id in self.fx['top']:
                self.uses.append(('%s.%s' % (self.fx['mod'], n.id), n.lineno, 'use'))

    def visit_Attribute(self, n):
        v = n.value
        if isinstance(v, ast.Name) and v.id in self.aliases and v.id not in self.local:
            how = 'sets' if isinstance(n.ctx, ast.Store) else 'use'
            self.uses.append(('%s.%s' % (self.aliases[v.id], n.attr), n.lineno, how))
        elif isinstance(v, ast.Name) and v.id in self.froms and v.id not in self.local:
            how = 'sets' if isinstance(n.ctx, ast.Store) else 'use'   # `from people_parts import FA` ... FA.x
            self.uses.append(('%s.%s.%s' % (self.froms[v.id] + (n.attr,)), n.lineno, how))
        elif isinstance(v, ast.Name) and v.id in ('self', 'cls') and self.cls:
            self.uses.append(('%s.%s.%s' % (self.fx['mod'], self.cls, n.attr), n.lineno, 'use'))
        elif isinstance(v, ast.Name) and v.id in self.fx['classes'] and v.id not in self.local:
            self.uses.append(('%s.%s.%s' % (self.fx['mod'], v.id, n.attr), n.lineno, 'use'))
        else:
            self.maybe.append((n.attr, n.lineno))
        self.generic_visit(n)

    def visit_Constant(self, n):
        if not isinstance(n.value, str):
            return
        if '.py' in n.value:
            self.strings += re.findall(r'(\w+)\.py\b', n.value)
        if self.fx['mod'] != 'touch' and 'import ' in n.value and ('\n' in n.value or ';' in n.value):
            self._code(n.value, n.lineno)

    def _code(self, text, line):
        """Code a kit test runs in a fresh Python (`python3 -c "import people as PK; PK.head_faults(w)"`): its uses
        count as this def's ('runs')."""
        text = re.sub(r'%\(\w+\)[rsd]|%[rsd]', '0', text).replace('%%', '%')
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError):
            return
        al, fr = _imports(tree, self.known)
        inner = _Scope(dict(self.fx, top=set()), al, fr)
        inner.known = self.known
        inner.local = _locals(tree) - set(al) - set(fr)
        inner.visit(tree)
        self.uses += [(t, line, 'runs') for t, _, _ in inner.uses]


def _locals(fn):
    """Parameters and names assigned inside a def (they shadow module names)."""
    out = set()
    if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        a = fn.args
        out |= {x.arg for x in a.args + a.kwonlyargs + getattr(a, 'posonlyargs', [])}
        out |= {x.arg for x in (a.vararg, a.kwarg) if x}
    for n in ast.walk(fn):
        if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            out.add(n.id)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n is not fn:
            out.add(n.name)
    return out


def _imports(node, known):
    """`import x as y` -> {y: x}; `from x import a as b` -> {b: (x, a)}; only modules in the index."""
    aliases, froms = {}, {}
    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for a in n.names:
                base = a.name.split('.')[-1] if a.asname else a.name.split('.')[0]
                if base in known:
                    aliases[a.asname or a.name.split('.')[0]] = base
        elif isinstance(n, ast.ImportFrom) and n.module and n.module.split('.')[-1] in known:
            for a in n.names:
                if a.name != '*':
                    froms[a.asname or a.name] = (n.module.split('.')[-1], a.name)
        elif isinstance(n, ast.ImportFrom) and not n.module:
            for a in n.names:
                if a.name in known:
                    aliases[a.asname or a.name] = a.name
    return aliases, froms


def parse_file(path, rel, known):
    """One file -> its defs, its uses and its name-only maybes (plain data, kept in the cache)."""
    try:
        src = open(path, encoding='utf-8').read()
        tree = ast.parse(src)
    except (SyntaxError, UnicodeDecodeError, ValueError) as e:
        return {'error': str(e)[:120]}
    mod = _mod(rel)
    top, classes, defs = set(), set(), []
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            top.add(n.name)
            kind = 'class' if isinstance(n, ast.ClassDef) else 'def'
            deco = [d.id for d in n.decorator_list if isinstance(d, ast.Name)]
            defs.append({'id': f'{mod}.{n.name}', 'line': n.lineno, 'end': n.end_lineno, 'kind': kind,
                         'doc': (ast.get_docstring(n) or '').strip().split('\n')[0][:100], 'deco': deco})
            if kind == 'class':
                classes.add(n.name)
                for m in n.body:
                    if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        defs.append({'id': f'{mod}.{n.name}.{m.name}', 'line': m.lineno, 'end': m.end_lineno,
                                     'kind': 'method', 'doc': (ast.get_docstring(m) or '').strip().split('\n')[0][:100],
                                     'deco': []})
        elif isinstance(n, (ast.Assign, ast.AnnAssign)):
            for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                for x in ast.walk(t):
                    if isinstance(x, ast.Name):
                        top.add(x.id)
                        defs.append({'id': f'{mod}.{x.id}', 'line': n.lineno, 'end': n.end_lineno, 'kind': 'table',
                                     'doc': '', 'deco': []})
    fx = {'mod': mod, 'top': top, 'classes': classes}
    m_alias, m_from = _imports(ast.Module(body=[n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))],
                                          type_ignores=[]), known)
    reexport = {k: '%s.%s' % v for k, v in m_from.items()}
    uses, maybe, strings = [], [], {}

    def scan(caller, node, cls=None, extra=None):
        al, fr = dict(m_alias), dict(m_from)
        if extra is not None:
            a2, f2 = _imports(extra, known)
            al.update(a2)
            fr.update(f2)
        s = _Scope(fx, al, fr, cls)
        s.known = known
        s.local = _locals(node) - set(al) - set(fr) if extra is not None else set()
        s.visit(node)
        uses.extend((caller, t, ln, how) for t, ln, how in s.uses)
        maybe.extend((caller, a, ln) for a, ln in s.maybe)
        if s.strings:
            strings[caller] = sorted(set(s.strings))

    rest = []
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for d in n.decorator_list:
                scan(f'{mod}.{n.name}', d)
            scan(f'{mod}.{n.name}', n, extra=n)
        elif isinstance(n, ast.ClassDef):
            for m in n.body:
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    scan(f'{mod}.{n.name}.{m.name}', m, cls=n.name, extra=m)
                else:
                    scan(f'{mod}.{n.name}', m, cls=n.name)
        elif not isinstance(n, (ast.Import, ast.ImportFrom)):
            rest.append(n)
            tgt = [x.id for t in getattr(n, 'targets', [getattr(n, 'target', None)]) if t is not None
                   for x in ast.walk(t) if isinstance(x, ast.Name)]
            scan(f'{mod}.{tgt[0]}' if tgt else f'{mod}.<module>', n)
    return {'mod': mod, 'defs': defs, 'uses': uses, 'modalias': m_alias, 'maybe': maybe, 'strings': strings, 'reexport': reexport,
            'lines': len(src.splitlines()), 'map': 'MAP' in (ast.get_docstring(tree) or '')}


# ------------------------------------------------------------------------------------------------ the index
def film_modules(root=ROOT):
    """A film's own code: a module with a top-level SHOTS (or its stem's sibling), as checkaudit counts it."""
    sys.path.insert(0, os.path.join(root, 'source'))
    try:
        import checkaudit
        return set(checkaudit.film_modules())
    except Exception:
        return set()


def build(root=ROOT, cache=CACHE, quiet=True):
    """Every file parsed (or taken from the cache when unchanged) and joined into one index; written to the cache."""
    t0 = time.time()
    os.makedirs(os.path.join(cache, 'parse'), exist_ok=True)
    files = _files(root)
    known = {_mod(f) for f in files}
    per, stamps, parsed = {}, {}, 0
    for rel in files:
        p = os.path.join(root, rel)
        st = os.stat(p)
        stamp = [st.st_mtime_ns, st.st_size]
        cp = os.path.join(cache, 'parse', rel.replace(os.sep, '__') + '.pkl')
        got = None
        try:
            with open(cp, 'rb') as f:
                c = pickle.load(f)
            if c.get('stamp') == stamp and c.get('v') == VERSION and c.get('known') == len(known):
                got = c['fx']
        except (OSError, EOFError, pickle.UnpicklingError, KeyError, AttributeError):
            pass
        if got is None:
            got = parse_file(p, rel, known)
            parsed += 1
            with open(cp, 'wb') as f:
                pickle.dump({'stamp': stamp, 'v': VERSION, 'known': len(known), 'fx': got}, f)
        per[rel] = got
        stamps[rel] = stamp
    films = film_modules(root)
    idx = {'v': VERSION, 'built': time.time(), 'stamps': stamps, 'films': sorted(films),
           'errors': {r: fx['error'] for r, fx in per.items() if 'error' in fx},
           'files': {fx['mod']: r for r, fx in per.items() if 'mod' in fx},
           'lines': {r: fx['lines'] for r, fx in per.items() if 'lines' in fx},
           'maps': {r: fx['map'] for r, fx in per.items() if 'map' in fx},
           'defs': {}, 'callers': {}, 'maybe': {}, 'tests': [], 'calls': {}}
    reexport = {}
    for rel, fx in per.items():
        for d in fx.get('defs', []):
            idx['defs'].setdefault(d['id'], dict(d, file=rel))
        for k, v in fx.get('reexport', {}).items():
            reexport[f"{fx['mod']}.{k}"] = v
    defs = idx['defs']
    modalias = {fx['mod']: fx.get('modalias', {}) for fx in per.values() if 'mod' in fx}

    def resolve(t):
        for _ in range(4):                       # `from body import arm` in views, used as views.arm
            p = t.split('.')
            if len(p) == 3 and p[1] in modalias.get(p[0], {}):   # people_parts.FA.house_mouth -> faces.house_mouth
                t = modalias[p[0]][p[1]] + '.' + p[2]
                continue
            if t in defs or t not in reexport:
                break
            t = reexport[t]
        return t
    method_names = {}
    for i in defs:
        method_names.setdefault(i.rsplit('.', 1)[1], []).append(i)
    for rel, fx in per.items():
        for caller, t, ln, how in fx.get('uses', []):
            t = resolve(t)
            if t in defs and t != caller:
                idx['callers'].setdefault(t, []).append([caller, rel, ln, how])
                idx['calls'].setdefault(caller, []).append(t)
        for caller, a, ln in fx.get('maybe', []):
            if a in method_names:
                idx['maybe'].setdefault(a, []).append([caller, rel, ln])
        for caller, names in fx.get('strings', {}).items():   # a kit test that runs `python3 source/X.py test`
            if not caller.startswith('kittests.'):        # elsewhere a file name in a string is a message, not a run
                continue
            for nm in names:
                for t in (f'{nm}.test', f'{nm}.main'):
                    if t in defs:
                        idx['callers'].setdefault(t, []).append([caller, rel, 0, 'runs'])
                        idx['calls'].setdefault(caller, []).append(t)
    idx['tests'] = sorted(d['id'] for d in defs.values() if d['id'].startswith('kittests.') and 'test' in d['deco'])
    for k in idx['callers']:
        seen, uniq = set(), []
        for c in idx['callers'][k]:
            if (c[0], c[2]) not in seen:
                seen.add((c[0], c[2]))
                uniq.append(c)
        idx['callers'][k] = uniq
    idx['secs'] = round(time.time() - t0, 1)
    idx['parsed'] = parsed
    with open(os.path.join(cache, 'index.json'), 'w') as f:
        json.dump(idx, f)
    if not quiet:
        print(f"touch: index built: {len(files)} files ({parsed} parsed, the rest unchanged), {len(defs)} defs, "
              f"{sum(map(len, idx['callers'].values()))} exact uses, {len(idx['tests'])} kit tests, "
              f"{len(idx['errors'])} unparsable, {idx['secs']} s")
    return idx


def load(root=ROOT, cache=CACHE):
    """The index, rebuilt first for any file changed since (only those are parsed again)."""
    try:
        idx = json.load(open(os.path.join(cache, 'index.json')))
    except (OSError, ValueError):
        return build(root, cache)
    if idx.get('v') != VERSION or _changed(idx, root):
        return build(root, cache)
    return idx


def _changed(idx, root=ROOT):
    now = {}
    for rel in _files(root):
        st = os.stat(os.path.join(root, rel))
        now[rel] = [st.st_mtime_ns, st.st_size]
    return sorted(r for r in set(now) | set(idx['stamps']) if now.get(r) != idx['stamps'].get(r))


def stale_faults(root=ROOT, cache=CACHE):
    """For handover.py end: the index is missing or older than the code, or a file cannot be parsed."""
    try:
        idx = json.load(open(os.path.join(cache, 'index.json')))
    except (OSError, ValueError):
        return ['the who-uses-this index (source/touch.py) was never built in this chat: setup.sh did not run it; '
                'run python3 source/touch.py build']
    out = []
    ch = _changed(idx, root)
    if idx.get('v') != VERSION:
        out.append('the who-uses-this index is from an older touch.py; run python3 source/touch.py build')
    elif ch:
        out.append(f'the who-uses-this index is older than {len(ch)} file(s) ({", ".join(ch[:3])}): a query would '
                   f'rebuild it, but nothing has since this chat changed them; run python3 source/touch.py build')
    for rel, err in sorted(idx.get('errors', {}).items()):
        out.append(f'{rel} cannot be parsed ({err}); its uses are invisible to touch.py')
    return out


# ------------------------------------------------------------------------------------------------ questions
def lookup(idx, name):
    """NAME -> (exact defs, near defs). Exact: the whole id, its tail (`head_faults`, `Class.m`) or `mod.name`."""
    defs = idx['defs']
    if name in defs:
        return [name], []
    exact = [i for i in defs if i.endswith('.' + name)]
    if exact:
        return sorted(exact, key=lambda i: (defs[i]['kind'] == 'table', len(i))), []
    w = name.lower().replace(' ', '_')
    near = [i for i in defs if w in i.rsplit('.', 1)[1].lower() and defs[i]['kind'] != 'table']
    return [], sorted(near, key=lambda i: (len(i.rsplit('.', 1)[1]), i))


HUBS = ('main', '<module>')


def reach(idx, target, limit=4000, wide=False):
    """Every def whose calls lead to target, nearest first: {caller: (depth, via)}. A command's main() (a dispatcher:
    one test runs one of its subcommands) is not followed further unless wide, else a kit test running
    `handover.py end` would count as covering every face function."""
    out, frontier = {}, [target]
    depth = 0
    while frontier and len(out) < limit:
        depth += 1
        nxt = []
        for t in frontier:
            if not wide and t != target and t.rsplit('.', 1)[1] in HUBS:
                continue
            for c in idx['callers'].get(t, []):
                if c[0] not in out and c[0] != target:
                    out[c[0]] = (depth, t)
                    nxt.append(c[0])
        frontier = nxt
    return out


def tests_for(idx, targets, wide=False):
    """The kit tests whose calls reach any of targets (a target that is a kit test is its own)."""
    tests = set(idx['tests'])
    got = {}
    for t in targets:
        if t in tests:
            got[t] = (0, t)
        for c, (d, via) in reach(idx, t, wide=wide).items():
            if c in tests and (c not in got or d < got[c][0]):
                got[c] = (d, via)
    return dict(sorted(got.items(), key=lambda kv: (kv[1][0], kv[0])))


def _secs():
    try:
        import kitstamps
        return kitstamps.stale(kitstamps.test_names())[1]
    except Exception:
        return {}


def rerun_line(idx, tests, secs=None, short=None):
    """One line: how many kit tests, about how long, and the command (long lists by --touching / --changed)."""
    if not tests:
        return 'RERUN: no kit test reaches these (the tests reach code by exact calls; say so if a fix needs one)'
    names = [t.split('.', 1)[1] for t in tests]
    secs = _secs() if secs is None else secs
    est = ''
    if secs:
        import kitstamps
        est = f', about {kitstamps.say_minutes(kitstamps.estimate(names, secs))}'
    cmd = f'--names {",".join(names)}' if len(names) <= 8 or not short else short
    return f'RERUN ({len(names)} kit test{"s" * (len(names) != 1)}{est}): python3 source/kittests.py {cmd}'


def _where(idx, i):
    d = idx['defs'][i]
    return f"{d['file']}:{d['line']}"


def report(idx, name, n=20):
    """The ~20-line answer for one NAME."""
    if name in idx['files'] and name not in idx['defs']:
        return module_report(idx, name, n)
    if name.startswith('find '):
        w = name[5:].strip().lower().replace(' ', '_')
        exact, near = [], sorted((i for i in idx['defs'] if w in i.rsplit('.', 1)[1].lower()
                                  and idx['defs'][i]['kind'] != 'table'), key=lambda i: (len(i.rsplit('.', 1)[1]), i))
    else:
        exact, near = lookup(idx, name)
    lines = []
    if not exact:
        if not near:
            return [f'touch: nothing in the code is called "{name}" or holds it in its name']
        lines.append(f'touch: no def is named "{name}"; {len(near)} hold it (say which: touch.py MODULE.NAME):')
        lines += [f"  {i}  {_where(idx, i)}  {idx['defs'][i]['doc'][:70]}" for i in near[:n - 1]]
        return lines
    i = exact[0]
    d = idx['defs'][i]
    films = set(idx['films'])
    lines.append(f"touch {i} [{d['kind']}]  {d['file']}:{d['line']}-{d['end']}  {d['doc'][:80]}")
    if len(exact) > 1:
        lines.append(f'  also named "{name}" ({len(exact) - 1}; say which: touch.py MODULE.NAME): '
                     + '; '.join(f"{x} {_where(idx, x)}" for x in exact[1:5]))
    calls = idx['callers'].get(i, [])
    film_c = [c for c in calls if c[0].split('.')[0] in films]
    shared_c = [c for c in calls if c[0].split('.')[0] not in films and not c[0].startswith('kittests.')]
    kit_c = [c for c in calls if c[0].startswith('kittests.')]
    room = max(3, (n - 8) // 2)

    def row(c):
        how = '' if c[3] in ('use', 'call') else f' ({c[3]})'
        return f'{c[0]}@{c[1]}:{c[2]}{how}'
    lines.append(f'  film code ({len(film_c)}): ' + ('; '.join(row(c) for c in film_c[:room]) or '-')
                 + (f'; +{len(film_c) - room} more' if len(film_c) > room else ''))
    lines.append(f'  shared ({len(shared_c)}): ' + ('; '.join(row(c) for c in shared_c[:room]) or '-')
                 + (f'; +{len(shared_c) - room} more' if len(shared_c) > room else ''))
    short = i.rsplit('.', 1)[1]
    mb = [m for m in idx['maybe'].get(short, []) if m[0] != i]
    if mb and d['kind'] in ('def', 'method'):
        lines.append(f'  name-only maybe ({len(mb)}, `x.{short}` on a value the index cannot name): '
                     + '; '.join(f'{m[0]}@{m[1]}:{m[2]}' for m in mb[:3]))
    up = reach(idx, i)
    checks = [c for c in up if CHECK_NAME.search(c.rsplit('.', 1)[1]) and not c.startswith('kittests.')]
    checks.sort(key=lambda c: up[c][0])
    lines.append(f'  checks it feeds ({len(checks)}): ' + (', '.join(checks[:6]) or '-')
                 + (f', +{len(checks) - 6} more' if len(checks) > 6 else ''))
    tests = tests_for(idx, [i])
    direct = [t for t, (dp, _) in tests.items() if dp == 1]
    lines.append(f'  kit tests ({len(tests)}; {len(direct)} call it directly, {len(kit_c)} uses in kittests.py): '
                 + ', '.join(f"{t.split('.', 1)[1]}" + (f' (via {v.split(".", 1)[1]})' if dp > 1 else '')
                             for t, (dp, v) in list(tests.items())[:6])
                 + (f', +{len(tests) - 6} more' if len(tests) > 6 else ''))
    lines.append('  ' + rerun_line(idx, list(tests), short=f'--touching {i}'))
    wide = len(tests_for(idx, [i], wide=True)) - len(tests)
    if wide > 0:
        lines.append(f"  +{wide} kit tests reach it only through a command's main() (a whole tool run): the final's "
                     f"kit run covers them")
    near = [x for x in idx['defs'] if short.lower() in x.rsplit('.', 1)[1].lower() and x not in exact
            and idx['defs'][x]['kind'] != 'table']
    if near:
        lines.append(f'  {len(near)} other defs hold "{short}" in their name: python3 source/touch.py "find {short}"')
    return lines


def module_report(idx, mod, n=20):
    """A whole file: its size, which files use it (film and shared apart), its most-used defs, the kit tests reaching
    any of them."""
    rel = idx['files'][mod]
    films = set(idx['films'])
    mine = [i for i in idx['defs'] if i.split('.', 1)[0] == mod]
    users, count = {}, {}
    for i in mine:
        for c in idx['callers'].get(i, []):
            m = c[0].split('.', 1)[0]
            if m != mod:
                users.setdefault(m, 0)
                users[m] += 1
                count[i] = count.get(i, 0) + 1
    fu = sorted((m for m in users if m in films), key=lambda m: -users[m])
    su = sorted((m for m in users if m not in films), key=lambda m: -users[m])
    top = sorted(count, key=lambda i: -count[i])
    tests = tests_for(idx, [i for i in mine if idx['defs'][i]['kind'] != 'class'])
    room = max(4, n - 7)
    return [f"touch {mod} [file]  {rel}  {idx['lines'].get(rel, '?')} lines, {len(mine)} defs"
            + ('' if idx['maps'].get(rel) else ', NO MAP'),
            f'  film code using it ({len(fu)}): ' + ', '.join(f'{m} {users[m]}' for m in fu[:room]),
            f'  shared using it ({len(su)}): ' + ', '.join(f'{m} {users[m]}' for m in su[:room]),
            f'  most used: ' + ', '.join(f"{i.split('.', 1)[1]} {count[i]}" for i in top[:8]),
            f'  kit tests reaching it: {len(tests)}; ask about one def for its own rerun line (touch.py {mod}.NAME)']


# ------------------------------------------------------------------------------------------------ step 2: after an edit
def changed_defs(idx, since='HEAD', root=ROOT):
    """The defs whose lines a diff touched (working tree against `since`), from the diff's own line numbers."""
    try:
        diff = subprocess.run(['git', 'diff', '-U0', since, '--', 'source', '.claude/hooks'], cwd=root,
                              capture_output=True, text=True, timeout=30).stdout
        new = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', 'source', '.claude/hooks'],
                             cwd=root, capture_output=True, text=True, timeout=30).stdout.split()
    except (OSError, subprocess.SubprocessError):
        return []
    spans, cur = {}, None
    for ln in diff.splitlines():
        if ln.startswith('+++ '):
            cur = ln[6:] if ln.startswith('+++ b/') else None
        elif ln.startswith('@@') and cur and cur.endswith('.py'):
            m = re.search(r'\+(\d+)(?:,(\d+))?', ln)
            a, b = int(m.group(1)), int(m.group(2) or 1)
            spans.setdefault(cur, []).append((a, a + max(b, 1) - 1))
    for f in new:
        if f.endswith('.py'):
            spans.setdefault(f, []).append((1, 10 ** 6))
    out = []
    for i, d in idx['defs'].items():
        if d['file'] in spans and d['kind'] != 'class' and any(a <= d['end'] and b >= d['line']
                                                              for a, b in spans[d['file']]):
            out.append(i)
    return sorted(out)


def rerun(idx, since='HEAD', root=ROOT, secs=None):
    ch = changed_defs(idx, since, root)
    if not ch:
        return ch, {}, f'RERUN: no function changed since {since}'
    tests = tests_for(idx, ch)
    kinds = idx['defs']
    ch = sorted(ch, key=lambda i: (kinds[i]['kind'] == 'table', i))
    shown = ', '.join(ch[:5]) + (f' +{len(ch) - 5}' if len(ch) > 5 else '')
    return ch, tests, f'{len(ch)} changed ({shown}). ' + rerun_line(idx, list(tests), secs,
                                                                    short='--changed' + ('' if since == 'HEAD' else ' ' + since))


# ------------------------------------------------------------------------------------------------ the kit test
def test():
    """The fault it catches, saved as an example: a hand trace of `people.head_faults` (the crowd-head check, Sam
    26 Nov) by `grep -n "head_faults("` misses the uses that never write the bracket (a kit test that passes the
    function as a value) and cannot say which kit tests reach it through callers; it also counts the docstring and
    comment mentions as uses. Here: a tiny code tree with exactly those traps."""
    import shutil
    import tempfile
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, 'source'))
    os.makedirs(os.path.join(d, '.claude', 'hooks'))
    w = lambda name, text: open(os.path.join(d, 'source', name), 'w').write(text)
    w('people.py', 'def head_faults(x):\n    """head_faults( in a docstring is not a use"""\n    return x\n\n'
                   'def install():\n    return head_faults(1)\n')
    w('views.py', 'from people import head_faults as hf\n\ndef draw():\n    return hf(2)\n')
    w('reel.py', 'SHOTS = []\nimport views as V\n\ndef frame_image(t):\n    return V.draw()\n')
    w('checkaudit.py', 'def film_modules():\n    return {"reel"}\n')
    w('kittests.py', 'TESTS = []\ndef test(fn):\n    TESTS.append(fn)\n    return fn\n\n'
                     '@test\ndef crowd_head_installed():\n    import people as P\n    check = P.head_faults\n'
                     '    return check\n\n@test\ndef reel_frames():\n    import reel\n    return reel.frame_image(0)\n\n'
                     '@test\ndef unrelated():\n    return 1\n')
    cache = os.path.join(d, 'cache')
    bad = []
    try:
        idx = build(d, cache)
        callers = {c[0] for c in idx['callers'].get('people.head_faults', [])}
        want = {'people.install', 'views.draw', 'kittests.crowd_head_installed'}
        if callers != want:
            bad.append(f'callers {sorted(callers)} != {sorted(want)}')
        t = set(tests_for(idx, ['people.head_faults']))
        if t != {'kittests.crowd_head_installed', 'kittests.reel_frames'}:
            bad.append(f'kit tests reaching it: {sorted(t)} (want crowd_head_installed and reel_frames via views.draw)')
        grep = subprocess.run(['grep', '-rn', 'head_faults(', os.path.join(d, 'source')], capture_output=True,
                              text=True).stdout.splitlines()
        hand = {ln.split(':')[0].rsplit('/', 1)[1] for ln in grep}
        if 'kittests.py' in hand:
            bad.append('the trap is gone: grep now finds the kit test, so the example no longer shows the fault')
        rep = report(idx, 'head_faults')
        if len(rep) > 22 or 'film code (0)' not in rep[1] or 'reel_frames' not in rep[-1]:
            bad.append('report: ' + ' | '.join(rep))
        # step 2: an edit inside views.draw names the reel test; touching nothing names none
        import subprocess as sp
        sp.run(['git', 'init', '-q'], cwd=d)
        sp.run(['git', '-c', 'user.email=t@t', '-c', 'user.name=t', 'add', '-A'], cwd=d)
        sp.run(['git', '-c', 'user.email=t@t', '-c', 'user.name=t', 'commit', '-qm', 'x'], cwd=d)
        if rerun(idx, root=d, secs={})[0]:
            bad.append('rerun named a change on a clean tree')
        w('views.py', 'from people import head_faults as hf\n\ndef draw():\n    return hf(3)\n')
        idx = load(d, cache)
        ch, tests, line = rerun(idx, root=d, secs={})
        if ch != ['views.draw'] or set(tests) != {'kittests.reel_frames'} or '--names reel_frames' not in line:
            bad.append(f'rerun after editing views.draw: {ch} {sorted(tests)} {line}')
        st = os.path.join(d, 'said')
        h1 = hook({'tool_input': {'file_path': os.path.join(d, 'source', 'views.py')}, 'transcript_path': 'c'},
                  st, d, cache, secs={})
        h2 = hook({'tool_input': {'file_path': os.path.join(d, 'source', 'views.py')}, 'transcript_path': 'c'},
                  st, d, cache, secs={})
        h3 = hook({'tool_input': {'file_path': os.path.join(d, 'notes.md')}, 'transcript_path': 'c'}, st, d, cache)
        if not h1 or 'reel_frames' not in json.dumps(h1) or h2 or h3:
            bad.append(f'edit hook: first {h1}, repeat {h2}, a notes edit {h3}')
        # staleness: an index older than the code is a fault at handover
        open(os.path.join(d, 'source', 'views.py'), 'a').write('\n# later edit\n')
        if not stale_faults(d, cache):
            bad.append('a stale index was not flagged')
        build(d, cache)
        if stale_faults(d, cache):
            bad.append(f'a fresh index was flagged: {stale_faults(d, cache)}')
        w('broken.py', 'def (:\n')
        build(d, cache)
        if not any('broken.py' in f for f in stale_faults(d, cache)):
            bad.append('an unparsable file was not flagged')
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print('touch test: ' + ('OK (grep missed the kit test and the caller chain; the index found both)'
                            if not bad else 'FAILED: ' + '; '.join(bad)))
    return not bad, '; '.join(bad) or 'callers, reaching kit tests, rerun line, staleness and parse errors all right'


def hook(inp, state_dir=None, root=ROOT, cache=CACHE, secs=None):
    """PostToolUse on Edit/Write: after an edit to code, the one RERUN line for everything changed since HEAD, said
    only when it differs from the last one this chat was told (so ten edits to one function say it once)."""
    tin = inp.get('tool_input') or {}
    path = tin.get('file_path') or tin.get('notebook_path') or ''
    rel = os.path.relpath(path, root) if os.path.isabs(path) else path
    if not rel.endswith('.py') or not any(rel.startswith(d + os.sep) for d in DIRS):
        return None
    state_dir = state_dir or os.path.join(cache, 'said')
    os.makedirs(state_dir, exist_ok=True)
    sp = os.path.join(state_dir, os.path.basename(inp.get('transcript_path') or 'chat') + '.txt')
    ch, tests, line = rerun(load(root, cache), 'HEAD', root, secs)
    key = ','.join(sorted(tests))
    try:
        if open(sp).read() == key:
            return None
    except OSError:
        pass
    open(sp, 'w').write(key)
    return {'hookSpecificOutput': {'hookEventName': 'PostToolUse', 'additionalContext': 'After this edit: ' + line}}


def main(argv):
    if not argv:
        print(__doc__.split('MAP')[0].strip())
        return 0
    if argv[0] == 'test':
        return 0 if test()[0] else 1
    if argv[0] == 'hook':
        try:
            import hookran
            hookran.ran('touch.py hook')
        except Exception:
            pass
        try:
            out = hook(json.load(sys.stdin))
        except Exception:
            return 0                              # never break a chat over a reminder
        if out:
            print(json.dumps(out))
        return 0
    if argv[0] == 'build':
        build(quiet=False)
        return 0
    n = int(argv[argv.index('-n') + 1]) if '-n' in argv else 20
    idx = load()
    if argv[0] == 'rerun':
        since = argv[argv.index('--since') + 1] if '--since' in argv else 'HEAD'
        print(rerun(idx, since)[2])
        return 0
    if argv[0] == 'stale':
        f = stale_faults()
        print('\n'.join(f) or 'touch: index fresh')
        return 1 if f else 0
    print('\n'.join(report(idx, argv[0], n)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
