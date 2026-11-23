#!/usr/bin/env python3
"""MAP  ruleproofs: lesson 7 step 2 (rule-needs-check, Sam's option 1, 22 Nov): every rule is a PROVEN PROMISE.
A rule counts as working only when its check has caught a saved example of its own fault (a still, Sam's words, a
message), run by a kit test. "By hand" is never a check. Taste rules are proven by a fresh-eye judge (critic bench) case.

  source/rule_proofs.json .. one entry per rule (rulebook rows; W1-W15 and N1-N24 = the CLAUDE.md rules, ids from
                             notes/proposals/rule-needs-check/rule-table.md): status, tests, example, plan / learn / owed,
                             rank (worst first by step 1's numbers), and _baseline (the rule ids and CLAUDE.md bold
                             phrases that existed on 23 Nov)
  STATUS ................... proven | partly | judge | next | owed | cannot yet
  rulebook_ids(), claude_anchors()  what rules exist now (read from the files, so a new rule is seen unasked)
  faults() ................. for the watcher (every Stop) and handover end: a NEW rule with no entry or no example
                             (the gate), a "by hand" status, a proof naming a missing kittest, a proven rule whose
                             kittest failed in the last background run (a miss = BROKEN)
  start_line() ............. one line at chat start: how many proven, the next three worst first
  sam_list() ............... the rules whose check cannot yet be built, with what must be learned first (one list)

    python3 source/ruleproofs.py              summary (counts, next worst first)
    python3 source/ruleproofs.py faults       what the gate refuses now
    python3 source/ruleproofs.py sam          the cannot-yet list in plain words, for Sam
    python3 source/ruleproofs.py baseline     re-take the baseline (ONLY when Sam has approved the new rules' entries)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'source', 'rule_proofs.json')
RULEBOOK = os.path.join(ROOT, 'guides', 'film-quality-rules.md')
CLAUDE = os.path.join(ROOT, 'CLAUDE.md')
KITLOG = os.path.join(ROOT, 'notes', 'logs', 'kittests-last.log')
STATUS = ('proven', 'partly', 'judge', 'next', 'owed', 'cannot yet')
NEEDS = {'next': 'plan', 'owed': 'owed', 'cannot yet': 'learn', 'judge': 'plan', 'partly': 'plan'}


def load(path=DATA):
    return json.load(open(path, encoding='utf-8'))


def rulebook_ids(text=None):
    """Every row id in the rulebook's rule tables (1, 41, S8, L1 ...)."""
    text = text if text is not None else open(RULEBOOK, encoding='utf-8').read()
    return sorted(set(re.findall(r'^\| *([0-9]{1,3}|[A-Z][0-9]{1,2}) *\|', text, re.M)))


def claude_anchors(text=None):
    """Every rule-like anchor in CLAUDE.md: its section headings and its bold phrases."""
    text = text if text is not None else open(CLAUDE, encoding='utf-8').read()
    heads = [h.strip() for h in re.findall(r'^#+ (.+)$', text, re.M)]
    bold = [b.strip() for b in re.findall(r'\*\*(.+?)\*\*', text, re.S)]
    return sorted(set(heads + [' '.join(b.split()) for b in bold]))


def _tests():
    try:
        return set(re.findall(r'^@test\ndef (\w+)', open(os.path.join(ROOT, 'source', 'kittests.py')).read(), re.M))
    except OSError:
        return set()


def _failed():
    try:
        txt = open(KITLOG, encoding='utf-8', errors='replace').read()
    except OSError:
        return set()
    return set(re.findall(r'^FAIL (\w+)', txt, re.M)) if 'kittests:' in txt else set()


def faults(data=None, book=None, claude=None, tests=None, failed=None):
    """The gate. Each fault is 'rules|plain words'."""
    d = data or load()
    rules, base = d['rules'], d.get('_baseline', {})
    tests = _tests() if tests is None else tests
    failed = _failed() if failed is None else failed
    out = []
    anchored = {r.get('anchor') for r in rules.values() if r.get('anchor')}
    for rid in rulebook_ids(book):
        if rid not in rules and rid not in base.get('rulebook', []):
            out.append(f'rules|rule {rid} is new in the rulebook with no entry in source/rule_proofs.json: a new rule needs '
                       'its saved bad example (a still, Sam\'s words or a message) and the check run on it')
    for a in claude_anchors(claude):
        if a not in base.get('claude', []) and a not in anchored:
            out.append(f'rules|CLAUDE.md has a new rule ("{a[:60]}") with no entry in source/rule_proofs.json (anchor, '
                       'example, check): a new rule needs its saved bad example')
    for rid, r in rules.items():
        st = r.get('status')
        if st not in STATUS:
            out.append(f'rules|rule {rid}: status "{st}" is not a check ("by hand" never counts; use one of {", ".join(STATUS)})')
            continue
        if rid not in base.get('ids', []) and not (r.get('example') or '').strip():
            out.append(f'rules|rule {rid} is new and has no saved bad example')
        if st in ('proven', 'partly') and not r.get('tests'):
            out.append(f'rules|rule {rid} is marked {st} but names no kittest')
        if st in NEEDS and st != 'partly' and not (r.get(NEEDS[st]) or '').strip():
            out.append(f'rules|rule {rid} is "{st}" with no {NEEDS[st]} line')
        for t in r.get('tests', []):
            if tests and t not in tests:
                out.append(f'rules|rule {rid}: its proof names kittest {t}, which does not exist')
            elif t in failed:
                out.append(f'rules|rule {rid} is BROKEN: its kittest {t} no longer catches the saved example')
    return out


def counts(d=None):
    rules = (d or load())['rules']
    c = {s: 0 for s in STATUS}
    for r in rules.values():
        c[r['status']] = c.get(r['status'], 0) + 1
    return c, len(rules)


def worst(d=None, n=3):
    rules = (d or load())['rules']
    todo = [(r.get('rank', 999), rid) for rid, r in rules.items() if r['status'] not in ('proven',)]
    return [rid for _, rid in sorted(todo, key=lambda x: (x[0], x[1]))[:n]]


def start_line():
    d = load()
    c, n = counts(d)
    nxt = ', '.join(f'{rid} ({d["rules"][rid]["status"]})' for rid in worst(d))
    return (f'RULES (ruleproofs): {c["proven"]} of {n} rules proven on a saved example, {c["partly"]} partly; '
            f'{c["cannot yet"]} cannot yet (Sam\'s list); next worst first: {nxt}')


def sam_list(d=None):
    rules = (d or load())['rules']
    groups = {}
    for rid, r in rules.items():
        if r['status'] == 'cannot yet':
            groups.setdefault(r['learn'], []).append(rid)
    return [(ids, learn) for learn, ids in groups.items()]


def take_baseline():
    d = load()
    d['_baseline'] = {'rulebook': rulebook_ids(), 'claude': claude_anchors(), 'ids': sorted(d['rules'])}
    json.dump(d, open(DATA, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    return d['_baseline']


def main(argv):
    cmd = argv[0] if argv else ''
    if cmd == 'faults':
        f = faults()
        print('\n'.join(x.split('|', 1)[1] for x in f) or 'ruleproofs: every rule has its entry; no proof broken')
        return 1 if f else 0
    if cmd == 'sam':
        rules = load()['rules']
        for ids, learn in sam_list():
            print(f'- {", ".join(ids)}: ' + '; '.join(rules[i]['rule'][:60] for i in ids[:3]) + (' ...' if len(ids) > 3 else ''))
            print(f'  needs first: {learn}')
        return 0
    if cmd == 'baseline':
        b = take_baseline()
        print(f'baseline: {len(b["rulebook"])} rulebook rows, {len(b["claude"])} CLAUDE.md anchors, {len(b["ids"])} entries')
        return 0
    print(start_line())
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
