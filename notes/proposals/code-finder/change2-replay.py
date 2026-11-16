#!/usr/bin/env python3
"""Code-finder change 2, before/after on the frozen replay (built 16 Nov, Sam's yes 16 Nov). Runs the frozen replay with
the finder as change 1 left it (page.show.deep off), with change 2, and with change 2 given the notes table's who
column too (--who, as a round chat would pass it). Targets and inputs of the frozen replay are untouched.
    python3 notes/proposals/code-finder/change2-replay.py [-v]
"""
import importlib.util as u, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sp = u.spec_from_file_location('replay_show', os.path.join(HERE, '..', 'learn', 'replay-show.py'))
r = u.module_from_spec(sp); sp.loader.exec_module(r)
import page
WHO = {}
for l in open(os.path.join(r.ROOT, 'notes/archive/blessed-notes-animatics-1-2.md'), encoding='utf-8'):
    p = [x.strip() for x in l.split('|')]
    if len(p) > 6 and p[1].isdigit():
        WHO[re.sub(r"[^A-Za-z0-9' ]", ' ', p[4])[:160]] = p[5]
plain = page.show
for name, deep, who in (('before', False, False), ('after', True, False), ('after + who', True, True)):
    page.show.deep = deep
    page.show = (lambda f, n, b=40, s=None, a=None: plain(f, n, b, s, a, WHO.get(n))) if who else plain
    page.show.__dict__.update(plain.__dict__)
    lo, st, mx, res = r.run(verbose='-v' in sys.argv)
    print(f'{name:12}: loose {lo}/26  strict {st}/14  longest {mx} lines  missed {[n for n in res if not res[n][0]]}')
    n2 = page.show('blessed', re.sub(r"[^A-Za-z0-9' ]", ' ', r.rows()[2][2])[:160], 40, 'cast sheet', None)
    tops = [h.split()[0] for h, rs in n2 if rs]
    print(f"{'':12}  note 2: Brand's chin line is answer {tops.index('blessed_cast.py:65') + 1 if 'blessed_cast.py:65' in tops else '-'} of {len(tops)}")
page.show = plain
