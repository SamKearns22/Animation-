"""where.py PATCH t1,t2..: which body part is inside which car solid (part names, deepest cm)."""
import sys; sys.path.insert(0, '/home/user/Animation-/source'); sys.path.insert(0, '/tmp/claude-0/-home-user-Animation-/4886b434-f7cf-5a97-8291-6d77aeef8332/scratchpad')
import bench_move as M, it, numpy as np
it.load(sys.argv[1]); M.fit_seat(); M.fit_knee(); M.fit_ankles()
r = M.rig()
for t in map(float, sys.argv[2].split(',')):
    o = M._solve(M.goals_at(t), fold=False); P = o['P']
    res = {}
    for sol in M.solids():
        dep = M.inside_depth(P, sol); m = dep > M.TOUCH
        if m.any():
            for rg in np.unique(r['region'][m]):
                mm = m & (r['region'] == rg)
                res['%s<%s' % (M.REG_NAMES.get(rg, 'body'), sol[0])] = round(float(dep[mm].max()) * 100, 1)
    for sd, c in o['balls'].items():
        for sol in M.solids():
            d = M.inside_depth(c[None], sol)[0] + M.HAND_R
            if d > M.TOUCH: res['hand %s<%s' % (sd, sol[0])] = round(d * 100, 1)
    print(t, res, 'head', np.round(o['J']['head'], 2), 'pel', np.round(o['pel'], 2))
