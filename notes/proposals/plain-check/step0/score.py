#!/usr/bin/env python3
"""Step 0 scorer (plain-check, 23 Nov): checker A (fixed shape and names) and checker C (blind reader), scored on the
saved cases against Sam's own replies. C2 = C with Sam's words: a word the reader can't explain counts only when Sam
has never used it himself in his saved messages (notes/ledger/sam). Run: python3 notes/proposals/plain-check/step0/score.py"""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, os.path.join(ROOT, 'source'))
import propose as P
cases = json.load(open(os.path.join(HERE, 'cases.json')))
for k, c in cases.items():
    d = os.path.join(HERE, 'reader', k)
    if not os.path.exists(os.path.join(d, 'result.md')):
        continue
    look, res = open(os.path.join(d, 'look.md')).read(), open(os.path.join(d, 'result.md')).read()
    v = P.reader_verdict(look, res)
    c['C'] = 'pass' if v['pass'] else 'fail'
    c['C_words'] = v['words']
    c['C2_words'] = v['unknown']
    c['C_wrong'] = v['wrong']
    c['C2'] = 'pass' if v['pass_sam'] else 'fail'
json.dump(cases, open(os.path.join(HERE, 'cases.json'), 'w'), indent=1)
rows = []
for grp in ('must-fail', 'must-pass', 'routine', 'mixed'):
    ks = [k for k in sorted(cases) if cases[k]['label'] == grp and 'C' in cases[k]]
    for chk in ('A', 'A_names', 'C', 'C2'):
        caught = sum(cases[k][chk] == 'fail' for k in ks)
        rows.append(f'{grp:9} {chk:7} fail {caught}/{len(ks)}')
    both = sum(cases[k]['A'] == 'fail' or cases[k]['C2'] == 'fail' for k in ks)
    rows.append(f'{grp:9} A+C2    fail {both}/{len(ks)}')
conf = [k for k in cases if cases[k].get('sam_confused') and 'C' in cases[k]]
rows.append(f'Sam actually confused: C2 caught {sum(cases[k]["C2"] == "fail" for k in conf)}/{len(conf)}')
print('\n'.join(rows))
for k in sorted(cases):
    c = cases[k]
    if 'C' in c:
        print(f'{k:22} {c["label"]:9} A {c["A"]:4} C {c["C"]:4} C2 {c["C2"]:4} wrong {c["C_wrong"]} unknown-to-Sam {c["C2_words"][:6]}')
