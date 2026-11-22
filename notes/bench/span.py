"""span.py A B [C D ...]: check frames A..B-1 (and C..D-1) with the stage-1 checks; prints only faults."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'source'))
import bench_move as M, numpy as np
M.fit_seat(); M.fit_knee(); M.fit_ankles()
a = list(map(int, sys.argv[1:]))
for lo, hi in zip(a[::2], a[1::2]):
    for i in range(lo, hi):
        g = M.goals_at(i / 24); o = M.solve(g); c = M.check_frame(o, g)
        bad = {k: v for k, v in c.items() if k in ('car', 'self', 'pistol', 'rom') and v}
        print(i, round(i / 24, 3), bad or 'clean', flush=True)
