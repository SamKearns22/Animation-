#!/usr/bin/env python3
"""Code-finder change 2, before/after on the frozen replay (built 16 Nov, not adopted). Runs the replay with the finder
as it is, then with change 2 switched on (page.show.deep), and prints both lines.
    python3 notes/proposals/code-finder/change2-replay.py [-v]
"""
import importlib.util as u, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sp = u.spec_from_file_location('replay_show', os.path.join(HERE, '..', 'learn', 'replay-show.py'))
r = u.module_from_spec(sp); sp.loader.exec_module(r)
import page
for deep in (False, True):
    page.show.deep = deep
    lo, st, mx, res = r.run(verbose='-v' in sys.argv)
    miss = [n for n in res if not res[n][0]]
    print(f"{'after ' if deep else 'before'}: loose {lo}/26  strict {st}/14  longest {mx} lines  missed {miss}")
