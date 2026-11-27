#!/usr/bin/env python3
"""parts: one module kept in several files (cost-spike fix 5c, Sam's Y, 27 Nov; notes/cost-spike-fix.md). A big shared
file is cut into contiguous pieces in its own order; the first file (views.py) runs the others inside its OWN
namespace, as if their text still stood where the include line is. So nothing behaves differently: a film or check
that sets `V.person = ...` or `V.FAITHFUL = False` still reaches every function, wherever its text now lives; tracebacks
name the part file and its real line. Import the module (`import views as V`), never a part.

MAP
  include() ..... run each named part file inside the calling module's globals (keeps the module's own docstring)
  family() ...... a module file -> [its file, its parts in order]; a part -> the same list (its parent's)
  parent() ...... a part file's module name ('views' for views_arms.py), else None
  joined() ...... the module's text as one file again (parent with each include line replaced by the parts' text,
                  their PART header lines dropped): the proof that a split moved text and changed nothing
  test() ........ kittest parts_one_namespace: a setter from outside reaches a function whose text moved to a part

  split() ....... cut one module into parts at its own section lines (`# ----`), each part about LIMIT lines at most;
                  writes the parts, puts the include line where their text was, and refuses unless joined() gives back
                  the old file exactly

A part file opens with its docstring (marked PART OF, then its own MAP) and one guard line:
    '''PART OF views.py (cost-spike fix 5c): runs inside views; import views, never this file. ...
    MAP ...
    '''
    if __name__ == 'views_arms': raise ImportError('views_arms is part of views.py: import views')

    python3 source/parts.py split MODULE [--limit 900]   (then: python3 source/maps.py add the parts)
    python3 source/parts.py test
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PART_RE = re.compile(r'^"""PART OF (\w+)\.py\b')
INCL_RE = re.compile(r"^_PARTS\.include\(globals\(\), *([^)]*)\)[ \t]*$", re.M)


def include(g, *names):
    """Run each part (source/NAME.py, beside the calling module) inside g, the calling module's globals."""
    here = os.path.dirname(os.path.abspath(g['__file__']))
    doc = g.get('__doc__')
    for n in names:
        p = os.path.join(here, n + '.py')
        with open(p, encoding='utf-8') as f:
            code = compile(f.read(), p, 'exec')
        exec(code, g)
        g['__doc__'] = doc                   # a part's own MAP docstring must not replace the module's


def parent(path):
    """'views' for a part of views.py, else None."""
    try:
        with open(path, encoding='utf-8') as f:
            head = f.read(400)
    except OSError:
        return None
    m = PART_RE.match(head)
    return m.group(1) if m else None


def _names(src):
    return [n for m in INCL_RE.finditer(src) for n in re.findall(r"'(\w+)'", m.group(1))]


def family(path):
    """[module file, part files in order] for a split module (from the module or any of its parts); else [path]."""
    d = os.path.dirname(os.path.abspath(path))
    p = parent(path)
    top = os.path.join(d, p + '.py') if p else os.path.abspath(path)
    try:
        with open(top, encoding='utf-8') as f:
            src = f.read()
    except OSError:
        return [path]
    names = _names(src)
    return [top] + [os.path.join(d, n + '.py') for n in names] if names else [path]


def joined(path):
    """The split module's text as one file again: each include line replaced by its parts' text (each part's own
    docstring and guard line dropped)."""
    import ast
    fam = family(path)
    src = open(fam[0], encoding='utf-8').read()

    def body(n):
        t = open(os.path.join(os.path.dirname(fam[0]), n + '.py'), encoding='utf-8').read()
        assert PART_RE.match(t), f'{n}: no PART OF docstring'
        lines = t.split('\n')
        end = ast.parse(t).body[0].end_lineno
        assert lines[end].startswith(f"if __name__ == '{n}': raise ImportError"), f'{n}: no guard line'
        return '\n'.join(lines[end + 1:])
    return INCL_RE.sub(lambda m: ''.join(body(n) for n in re.findall(r"'(\w+)'", m.group(1)))[:-1], src)


SECTION = re.compile(r'^# -{8,}')
LIMIT = 900


def split(mod, limit=LIMIT, root=HERE):
    """Cut source/MOD.py into parts at its own top-level section lines. The module keeps its opening (docstring,
    imports and the first sections) and its closing `if __name__ == '__main__'` block; the middle goes to MOD_b.py,
    MOD_c.py ... in order, each at most about `limit` lines (a section longer than that stays whole). The include line
    stands where their text was. Refused (nothing written) unless joined() returns the old text exactly."""
    import ast
    path = os.path.join(root, mod + '.py')
    src = open(path, encoding='utf-8').read()
    if INCL_RE.search(src) or parent(path):
        return f'{mod}: already split'
    lines = src.split('\n')
    tree = ast.parse(src)
    spans = [(n.lineno - 1, n.end_lineno - 1) for n in tree.body]
    for n in tree.body:
        for d in getattr(n, 'decorator_list', []):
            spans.append((d.lineno - 1, n.end_lineno - 1))
    inside = set()
    for a, b in spans:
        inside.update(range(a + 1, b + 1))
    tail = len(lines)
    last = tree.body[-1]
    if isinstance(last, ast.If) and 'ast.Name' and getattr(last.test, 'left', None) is not None \
            and getattr(last.test.left, 'id', '') == '__name__':
        tail = last.lineno - 1
        while tail > 0 and (not lines[tail - 1].strip()):
            tail -= 1
    imports_end = max(n.end_lineno for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))
                      and n.lineno < tail)
    cuts = [i for i, ln in enumerate(lines[:tail]) if SECTION.match(ln) and i not in inside and i >= imports_end]
    if len(cuts) < 2:
        return f'{mod}: fewer than two section lines to cut at'
    bounds = cuts + [tail]
    segs = [(bounds[k], bounds[k + 1]) for k in range(len(bounds) - 1)]
    head_end = cuts[0]
    while segs and segs[0][1] - 0 <= limit * 0.5 and len(segs) > 1:   # a short opening keeps its first sections
        head_end = segs[0][1]
        segs.pop(0)
    chunks, cur = [], None
    for a, b in segs:
        if cur and b - cur[0] > limit:
            chunks.append(cur)
            cur = None
        cur = (cur[0], b) if cur else (a, b)
    if cur:
        if chunks and cur[1] - cur[0] < 150:     # a short last piece joins the one before
            cur = (chunks.pop()[0], cur[1])
        chunks.append(cur)
    if not chunks:
        return f'{mod}: nothing to move'
    letters = 'bcdefghijklmnop'
    names = [f'{mod}_{letters[k]}' for k in range(len(chunks))]
    for nm in names:
        if os.path.exists(os.path.join(root, nm + '.py')):
            return f'{mod}: {nm}.py exists already'
    files = {}
    for nm, (a, b) in zip(names, chunks):
        title = next((ln for ln in lines[a:b] if ln.startswith('#') and not SECTION.fullmatch(ln.strip() + '-' * 0)
                      and not set(ln.strip()) <= set('# -')), '').lstrip('# -').strip()
        doc = (f'"""PART OF {mod}.py (cost-spike fix 5c): runs inside {mod} (one module, parts.py); import {mod}, never '
               f'this file.\nIt holds the old {mod}.py lines {a + 1}-{b}' + (f': {title[:80]}' if title else '') + '.\n"""')
        files[nm] = doc + '\n' + f"if __name__ == '{nm}': raise ImportError('{nm} is part of {mod}.py: import {mod}')" \
            + '\n' + '\n'.join(lines[a:b]) + '\n'
    inc = '_PARTS.include(globals(), ' + ', '.join(f"'{n}'" for n in names) + ')'
    top = lines[:head_end]
    imp = 'import parts as _PARTS        # noqa  (cost-spike fix 5c: this module is kept in parts; parts.py)'
    new = '\n'.join(top[:imports_end] + [imp] + top[imports_end:] + [inc] + lines[chunks[-1][1]:])
    import tempfile
    import shutil
    d = tempfile.mkdtemp()
    try:
        open(os.path.join(d, mod + '.py'), 'w', encoding='utf-8').write(new)
        for nm, t in files.items():
            open(os.path.join(d, nm + '.py'), 'w', encoding='utf-8').write(t)
        back = joined(os.path.join(d, mod + '.py'))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    want = '\n'.join(lines[:imports_end] + [imp] + lines[imports_end:])
    if back != want:
        return f'{mod}: REFUSED: the parts joined again differ from the old file'
    open(path, 'w', encoding='utf-8').write(new)
    for nm, t in files.items():
        open(os.path.join(root, nm + '.py'), 'w', encoding='utf-8').write(t)
    sizes = ', '.join(f'{nm} {t.count(chr(10))}' for nm, t in files.items())
    return f'{mod}: split; {mod}.py now {new.count(chr(10)) + 1} lines; parts: {sizes} (joined again: identical)'


def test():
    """kittest parts_one_namespace. The fault it guards: a plain split (`from views_arms import *`) gives moved code its
    own globals, so `V.person = patched` (kitchecks.install does exactly this) no longer reaches a moved caller.
    Example: the split as a plain re-export misses the patch (caught); as parts it reaches it (passes)."""
    import importlib
    import shutil
    import tempfile
    d = tempfile.mkdtemp()
    try:
        shutil.copy(os.path.join(HERE, 'parts.py'), d)
        head = "import parts as _PARTS\nFAITHFUL = True\n\ndef person():\n    return 'plain'\n\n"
        moved = "def scene():\n    return person() + (' faithful' if FAITHFUL else '')\n"
        part_hdr = ('"""PART OF kitx.py (test)\n\nMAP of the part\n"""\n'
                    "if __name__ == 'kitx_b': raise ImportError('part')\n")
        open(os.path.join(d, 'kitx.py'), 'w').write('"""kitx: the module"""\n' + head + "_PARTS.include(globals(), 'kitx_b')\n")
        open(os.path.join(d, 'kitx_b.py'), 'w').write(part_hdr + moved)
        open(os.path.join(d, 'plainx.py'), 'w').write('"""plain"""\n' + head + "from plainx_b import *\n")
        open(os.path.join(d, 'plainx_b.py'), 'w').write("from plainx import person, FAITHFUL\n" + moved)
        sys.path.insert(0, d)
        try:
            for m in ('kitx', 'kitx_b', 'plainx', 'plainx_b', 'parts'):
                sys.modules.pop(m, None)
            got = {}
            for name in ('plainx', 'kitx'):
                M = importlib.import_module(name)
                M.person = lambda: 'patched'
                M.FAITHFUL = False
                got[name] = M.scene()
            K = sys.modules['kitx']
            ok_doc = K.__doc__ == 'kitx: the module'
            ok_join = joined(os.path.join(d, 'kitx.py')) == '"""kitx: the module"""\n' + head + moved
            try:
                importlib.import_module('kitx_b')
                ok_guard = False
            except ImportError:
                ok_guard = True
            ok_fam = [os.path.basename(x) for x in family(os.path.join(d, 'kitx_b.py'))] == ['kitx.py', 'kitx_b.py']
        finally:
            sys.path.remove(d)
            for m in ('kitx', 'kitx_b', 'plainx', 'plainx_b'):
                sys.modules.pop(m, None)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    caught = got['plainx'] != 'patched'
    passed = got['kitx'] == 'patched'
    print(f"parts: plain split -> {got['plainx']!r} ({'caught' if caught else 'MISSED'}); parts -> {got['kitx']!r} "
          f"({'passes' if passed else 'FAILS'}); docstring kept {ok_doc}; joined text exact {ok_join}; "
          f"part refuses a direct import {ok_guard}; family {ok_fam}")
    return caught and passed and ok_doc and ok_join and ok_guard and ok_fam


if __name__ == '__main__':
    if sys.argv[1:2] == ['test']:
        sys.exit(0 if test() else 1)
    if sys.argv[1:2] == ['split']:
        lim = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else LIMIT
        for m in [a for a in sys.argv[2:] if not a.startswith('--') and not a.isdigit()]:
            print(split(m, lim))
        sys.exit(0)
    print(__doc__)
