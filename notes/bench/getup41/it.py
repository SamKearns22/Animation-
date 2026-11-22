"""it.py PATCH.py [full] [lo hi]: get-up frames with a patch applied: joint steps/pops (fast, no fold); 'full' adds
the real checks in 4 processes. Default frames 12-25 (0.5-1.04 s)."""
import sys, os, importlib.util
sys.path.insert(0, '/home/user/Animation-/source')
import numpy as np
import bench_move as M

def load(p):
    spec = importlib.util.spec_from_file_location('patch', p); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); m.patch(M)
    M._BD_T.clear(); M._BD_T.update(t for t, _ in M.BREAKDOWNS); M._KEYC.clear(); M._PELY.clear(); M._THIGH.clear(); M._ABSH.clear()

def full(args):
    p, i = args
    load(p); M.fit_seat(); M.fit_knee(); M.fit_ankles()
    g = M.goals_at(i / 24); o = M.solve(g); c = M.check_frame(o, g)
    bad = {k: v for k, v in c.items() if k in ('car', 'self', 'pistol', 'rom') and v}
    return i, ' '.join('%s %s' % (n, (v3[1] if isinstance(v3, tuple) else v3)) for kk in bad for n, v3 in bad[kk].items()) or 'clean'

if __name__ == '__main__':
    p = sys.argv[1]; rest = sys.argv[2:]
    fl = 'full' in rest; rest = [x for x in rest if x != 'full']
    lo, hi = (int(rest[0]), int(rest[1])) if rest else (11, 26)
    load(p); M.fit_seat(); M.fit_knee(); M.fit_ankles()
    tr = []
    for i in range(lo, hi):
        o = M._solve(M.goals_at(i / 24), fold=False); tr.append({n: o['J'][n] for n in M.TRACK})
    top, over, pops = M.jumps(tr)
    print('largest step cm:', {k: v for k, v in top.items() if v > 6})
    pp = {}
    for f, n, v in pops:
        if v > 6: pp.setdefault(f + lo, []).append('%s %.0f' % (n, v))
    print('pops >6cm (frame: joint cm):', pp)
    if fl:
        for i in range(lo, hi):
            g = M.goals_at(i / 24); o = M.solve(g); c = M.check_frame(o, g)
            bad = {k: v for k, v in c.items() if k in ('car', 'self', 'pistol', 'rom') and v}
            print(i, round(i / 24, 3), ' '.join('%s %s' % (n, (v3[1] if isinstance(v3, tuple) else v3)) for kk in bad for n, v3 in bad[kk].items()) or 'clean', flush=True)
