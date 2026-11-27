#!/usr/bin/env python3
"""checkaudit: every check in the project listed in one table, with what it caught (R8, Sam 26 Nov: "audit every
check we do in this project ... whether they still serve a function or whether they are duplicates/can be combined").

MAP
  inventory() ...... every check, found in the code itself (never typed by hand, so the list cannot go stale):
                     hooks (.claude/settings.json), handover checks (handover.py *_faults), pre-flight and picture
                     checks (every *_faults / *gate* function in a shared module), cast sheet checks, kit tests
                     (kittests.py @test), checks that live in one film's code only, and the rulebook's check column
  evidence() ....... what each check flagged, from the per-check record (notes/ledger/FILM/checks.jsonl): runs,
                     distinct faults, and REPEATS (the same fault, numbers aside, on 3+ runs: never fixed, so
                     either noise or ignored); plus which check Sam's notes say should have caught them
                     (the notes' "should have caught" column) and kit test reds (notes/logs/kittest-reds.log)
  main ............. `python3 source/checkaudit.py [OUT.tsv]` writes the table (default notes/checks/audit.tsv)
                     and prints the counts by kind; `--repeats FILM` prints the faults that came back unchanged

The table is the listing; the judgement (dead, merge, smarter, move into the kit) is written in the audit report
(notes/check-audit.md), one row per check, so a later audit starts from this table and that report.
"""
import ast
import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPEAT_RUNS = 3


def _doc(node):
    d = ast.get_docstring(node) or ''
    return ' '.join(d.split())[:160]


def _parse(path):
    try:
        return ast.parse(open(path, encoding='utf-8').read())
    except (SyntaxError, UnicodeDecodeError):
        return None


def film_modules():
    """A film's own code: a module with a top-level SHOTS (or a name starting with a film's)."""
    films = set()
    for f in os.listdir(HERE):
        if f.endswith('.py'):
            src = open(os.path.join(HERE, f), encoding='utf-8', errors='replace').read()
            if re.search(r'^SHOTS\s*=', src, re.M):
                films.add(f[:-3])
    stems = {f.split('_')[0] for f in films if len(f.split('_')[0]) > 3}
    for f in os.listdir(HERE):
        if f.endswith('.py') and f[:-3] not in films and f.split('_')[0] in stems and f.split('_')[0] + '.py' in os.listdir(HERE):
            films.add(f[:-3])
    return films


CHECK_NAME = re.compile(r'(_faults$|^check_|_check$|gate|^audit|_audit$|_guard$|^lint)')
KIND_BY_MODULE = {'handover': 'handover', 'castsheet': 'cast sheet', 'preflight': 'pre-flight',
                  'film_engine': 'render lock', 'finish': 'finish', 'propose': 'proposal route',
                  'kitfilm': 'kit tests per film', 'override': 'override', 'watcher': 'watcher',
                  'humancheck': 'body check', 'critique': 'critique', 'ledger': 'cost', 'movesize': 'move size'}


def inventory():
    rows = []
    try:
        hooks = json.load(open(os.path.join(ROOT, '.claude', 'settings.json'))).get('hooks', {})
    except (OSError, ValueError):
        hooks = {}
    for when, entries in hooks.items():
        for e in entries:
            for h in e.get('hooks', []):
                cmd = h.get('command', '')
                name = re.sub(r'.*/', '', cmd.split('"')[-1].strip() or cmd).strip()
                rows.append(dict(kind='hook', name=name, where=when, film='', doc=e.get('matcher', '')))
    films = film_modules()
    for f in sorted(os.listdir(HERE)):
        if not f.endswith('.py') or f.startswith('kittests') or f == 'checkaudit.py':
            continue
        tree = _parse(os.path.join(HERE, f))
        if tree is None:
            continue
        mod = f[:-3]
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and CHECK_NAME.search(node.name) and not node.name.startswith('_'):
                kind = 'film only' if mod in films else KIND_BY_MODULE.get(mod, 'shared check')
                rows.append(dict(kind=kind, name='%s.%s' % (mod, node.name), where=f, film=mod if mod in films else '',
                                 doc=_doc(node)))
    for kf in sorted(f for f in os.listdir(HERE) if f.startswith('kittests') and f.endswith('.py')):
        tree = _parse(os.path.join(HERE, kf))      # kittests.py and its topic files (split 27 Nov)
        for node in (tree.body if tree else []):
            if isinstance(node, ast.FunctionDef) and any(getattr(d, 'id', '') == 'test' for d in node.decorator_list):
                rows.append(dict(kind='kit test', name=node.name, where=kf, film='', doc=_doc(node)))
    rb = os.path.join(ROOT, 'guides', 'film-quality-rules.md')
    for line in open(rb, encoding='utf-8'):
        c = [x.strip() for x in line.strip().strip('|').split('|')]
        if line.startswith('| ') and len(c) >= 3 and c[0] not in ('#', 'CLAUDE.md section') and not c[0].startswith('-'):
            hand = 'by hand' in c[-1].lower() or c[-1].lower().startswith('critique')
            rows.append(dict(kind='rule (by hand)' if hand else 'rule', name='rule %s' % c[0], where='rulebook',
                             film='', doc=c[-1][:160]))
    return rows


def _norm(fault):
    return re.sub(r'\[\d+ like it\]', '', re.sub(r'\d+(\.\d+)?', '#', fault)).strip()


def evidence(root=ROOT):
    """{check: {'runs', 'faults', 'distinct', 'repeats', 'films'}} from every film's checks.jsonl."""
    ev = collections.defaultdict(lambda: dict(runs=0, faults=0, distinct=set(), repeats=set(), films=set()))
    led = os.path.join(root, 'notes', 'ledger')
    for film in sorted(os.listdir(led)) if os.path.isdir(led) else []:
        p = os.path.join(led, film, 'checks.jsonl')
        if not os.path.exists(p):
            continue
        per = collections.defaultdict(set)
        for line in open(p, encoding='utf-8'):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            k = d.get('check') or '?'
            if re.match(r'^[\d.#]+ s$|^# s$', k):
                k = 'layers (drawn over, rule 17)'
            e = ev[k]
            e['runs'] += 1
            e['films'].add(film)
            for f in d.get('faults') or []:
                e['faults'] += 1
                n = _norm(f)
                e['distinct'].add(n)
                per[(k, n)].add(d.get('run'))
        for (k, n), runs in per.items():
            if len(runs) >= REPEAT_RUNS:
                ev[k]['repeats'].add(n)
    return ev


def should_have_caught(root=ROOT):
    """Counter of the 'should have caught' column across the films' notes (current and archived)."""
    c = collections.Counter()
    paths = [os.path.join(root, 'notes', f) for f in os.listdir(os.path.join(root, 'notes')) if f.endswith('.md')]
    arch = os.path.join(root, 'notes', 'archive')
    paths += [os.path.join(arch, f) for f in os.listdir(arch) if f.endswith('.md')] if os.path.isdir(arch) else []
    for p in paths:
        hdr = None
        for line in open(p, encoding='utf-8', errors='replace'):
            if line.startswith('|') and 'should have caught' in line.lower():
                hdr = [x.strip().lower() for x in line.strip().strip('|').split('|')]
                continue
            if hdr and line.startswith('|') and not line.startswith('|-'):
                cells = [x.strip() for x in line.strip().strip('|').split('|')]
                i = hdr.index('should have caught')
                if i < len(cells):
                    v = cells[i].lower()
                    key = 'none' if v.startswith(('none', '-', 'why')) or not v else v.split('(')[0].strip()[:40]
                    c[key] += 1
            elif not line.startswith('|'):
                hdr = None
    return c


def critique_saw(root=ROOT):
    """Counter of the 'critique saw it?' column (Sam's Y, 26 Nov): yes / no / no critique, across the films' notes."""
    c = collections.Counter()
    notes = os.path.join(root, 'notes')
    paths = [os.path.join(notes, f) for f in os.listdir(notes) if f.endswith('.md')]
    arch = os.path.join(notes, 'archive')
    paths += [os.path.join(arch, f) for f in os.listdir(arch) if f.endswith('.md')] if os.path.isdir(arch) else []
    for p in paths:
        hdr = None
        for line in open(p, encoding='utf-8', errors='replace'):
            if line.startswith('|') and 'critique saw' in line.lower():
                hdr = [x.strip().lower() for x in line.strip().strip('|').split('|')]
                continue
            if hdr and line.startswith('|') and not line.startswith('|-'):
                cells = [x.strip() for x in line.strip().strip('|').split('|')]
                i = next(k for k, h in enumerate(hdr) if 'critique saw' in h)
                ni = next((k for k, h in enumerate(hdr) if h.startswith('note')), 3)
                if i < len(cells) and ni < len(cells) and cells[ni]:
                    v = cells[i].lower()
                    c['yes' if v.startswith('yes') else 'no' if v.startswith('no') and 'critique' not in v
                      else 'no critique' if 'critique' in v else 'blank'] += 1
            elif not line.startswith('|'):
                hdr = None
    return c


def main(argv):
    if '--repeats' in argv:
        film = argv[argv.index('--repeats') + 1]
        ev = evidence()
        for k, e in sorted(ev.items()):
            if film in e['films'] and e['repeats']:
                print('%s: %d fault(s) came back unchanged on %d+ runs' % (k, len(e['repeats']), REPEAT_RUNS))
                for n in sorted(e['repeats'])[:5]:
                    print('   ', n[:150])
        return 0
    out = argv[0] if argv else os.path.join(ROOT, 'notes', 'checks', 'audit.tsv')
    rows, ev = inventory(), evidence()
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write('kind\tname\twhere\truns\tfaults\tdistinct\trepeats\tdoc\n')
        for r in rows:
            short = r['name'].split('.')[-1]
            e = ev.get(r['name']) or ev.get(short) or {}
            fh.write('\t'.join([r['kind'], r['name'], r['where'], str(e.get('runs', '')), str(e.get('faults', '')),
                                str(len(e.get('distinct', ()))) if e else '', str(len(e.get('repeats', ()))) if e else '',
                                r['doc'].replace('\t', ' ')]) + '\n')
    kinds = collections.Counter(r['kind'] for r in rows)
    print('%d checks: %s' % (len(rows), ', '.join('%s %d' % kv for kv in kinds.most_common())))
    print('recorded by name (checks.jsonl):', ', '.join('%s %d runs, %d repeat(s)' % (k, e['runs'], len(e['repeats']))
                                                         for k, e in sorted(ev.items()) if e['faults']))
    print('should have caught (Sam\'s notes):', dict(should_have_caught()))
    print('critique saw it too (Sam\'s notes):', dict(critique_saw()))
    print('table:', os.path.relpath(out, ROOT))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
