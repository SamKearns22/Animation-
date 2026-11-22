"""opt.py BASE_PATCH.py OUT.json [minutes]: random local search over the get-up breakdowns' numbers (B1, B1b, B1c),
starting from BASE_PATCH. Score per frame 0.54-0.96 s (real checks, one solve a frame): crossing depth (cm, every
pair) + 0.05 a crossing point + pops over 8 cm (0.5 per cm). Keeps a change only if the score falls. Writes the
best changes to OUT.json after every improvement (load them with optpatch.py)."""
import sys, os, json, time, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'source'))
import bench_move as M

base, out_json = sys.argv[1], sys.argv[2]
minutes = float(sys.argv[3]) if len(sys.argv) > 3 else 40
spec = importlib.util.spec_from_file_location('bp', base); bp = importlib.util.module_from_spec(spec); spec.loader.exec_module(bp)
bp.patch(M)
BASEKEY = M._key
OV = json.load(open(out_json)) if os.path.exists(out_json) else {}
# the numbers searched: (key, field, side) -> step (metres for points, unitless for ways)
PARAMS = []
for k in ('B1', 'B1b', 'B1c'):
    for f in ('knee', 'ankle'):
        for sd in 'LR':
            PARAMS.append((k, f, sd, 0.03))
    PARAMS += [(k, 'pelvis', None, 0.03), (k, 'c_up', None, 0.12), (k, 'p_fwd', None, 0.12), (k, 'lift', None, 0.03),
               (k, 'handL', None, 0.04)]


def get(d, k, f, sd):
    if f == 'handL':
        return np.asarray(d['hand']['L'][0], float)
    if sd:
        return np.asarray(d[f][sd], float)
    return np.asarray(d[f], float)


def k_over(name):
    d = BASEKEY(name)
    for key_, v in OV.items():
        k, f, sd = key_.split('|')
        if k != name:
            continue
        sd = sd or None
        v = np.array(v, float)
        if f == 'handL':
            d['hand'] = dict(d['hand']); d['hand']['L'] = (v, d['hand']['L'][1])
        elif f == 'lift':
            d['lift'] = float(v)
        elif sd:
            d[f] = dict(d[f]); d[f][sd] = v
        else:
            d[f] = v
    return d


def clear():
    for c in (M._KEYC, M._PELY, M._THIGH, M._ABSH):
        c.clear()


M._key = k_over
M._BD_T.clear(); M._BD_T.update(t for t, _ in M.BREAKDOWNS)
M.fit_seat(); M.fit_knee(); M.fit_ankles()
FR = list(range(13, 24))


def score(verbose=False):
    clear()
    tot, tr, rows = 0.0, [], []
    for i in [12] + FR + [24]:
        g = M.goals_at(i / 24)
        o = M.solve(g)
        tr.append({n: o['J'][n] for n in M.TRACK})
        if i in FR:
            c = M.check_frame(o, g)
            s = 0.0
            for kk in ('car', 'self', 'pistol'):
                for n, v in c[kk].items():
                    s += v[1] + 0.05 * v[0]
            for n, v in c['rom'].items():
                s += max(0, v - 160) * 0.5
            tot += s
            rows.append((i, round(s, 1)))
    _, _, pops = M.jumps(tr)
    pp = sum(max(0, v - 8) * 0.5 for f, n, v in pops)
    if verbose:
        print('frames', rows, 'pops', round(pp, 1), flush=True)
    return tot + pp


rng = np.random.default_rng(int(time.time()))
best = score(True)
print('start score', round(best, 1), flush=True)
t0 = time.time()
it = 0
while time.time() - t0 < minutes * 60:
    it += 1
    old = dict(OV)
    for _ in range(rng.integers(1, 3)):
        k, f, sd, st = PARAMS[rng.integers(len(PARAMS))]
        key_ = '%s|%s|%s' % (k, f, sd or '')
        if key_ in OV:
            cur = np.array(OV[key_], float)
        else:
            clear(); cur = get(BASEKEY(k), k, f, sd) if f != 'lift' else np.array(float(BASEKEY(k).get('lift', 0)))
        new = cur + rng.normal(0, st, np.shape(cur))
        OV[key_] = new.tolist()
    s = score()
    if s < best:
        best = s
        json.dump(OV, open(out_json, 'w'), indent=1)
        print('%d  %.1f min  score %.1f  kept %s' % (it, (time.time() - t0) / 60, s,
              [k for k in OV if OV[k] != old.get(k)]), flush=True)
    else:
        OV.clear(); OV.update(old)
print('done: %d tries, best %.1f' % (it, best), flush=True)
score(True)
