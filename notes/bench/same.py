"""same.py record|compare DIR [--draw-only]: the speed-up's sameness bar (proposal bench-speedup, chat 40).

record: the start-up fits (numbers, seconds), every 8th frame's solved body (a hash of every skin point, exact bytes)
and its checks (word for word), 12 grey frames (a hash of every pixel), per-part seconds and how busy the 4
processors were; written to DIR/same.json. compare: the same again, against DIR/same.json; prints every difference
(the bar: none) and the new seconds. A speed-up is kept only if compare prints SAME."""
import sys, os, time, json, hashlib, resource
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'source'))
import numpy as np
import bench_move as M

FRAMES = list(range(0, 197, 8)) + [196]
DRAWN = list(range(0, 197, 16))[:12]


def _cpu():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime + r.ru_stime


def _h(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]


def measure(draw_only=False):
    res = dict(frames={}, drawn={}, secs={})
    t0, c0 = time.time(), _cpu()
    fits = (M.fit_seat(), M.fit_knee(), M.fit_ankles())
    res['fits'] = [repr(float(x)) for x in fits]
    res['secs']['fits'] = round(time.time() - t0, 1)
    ts = M.frame_times()
    ts_solve = tc_solve = ts_check = 0.0
    outs = {}
    for i in sorted(set(FRAMES) | set(DRAWN)):
        g = M.goals_at(ts[i])
        a, ca = time.time(), _cpu()
        o = M.solve(g)
        b = time.time()
        ts_solve += b - a
        tc_solve += _cpu() - ca
        outs[i] = o
        if i in FRAMES and not draw_only:
            c = M.check_frame(o, g)
            ts_check += time.time() - b
            res['frames'][str(i)] = dict(P=_h(o['P']), checks=repr({k: c[k] for k in sorted(c)}))
    n = len(outs)
    res['secs']['solve per frame'] = round(ts_solve / n, 2)
    res['secs']['processors busy in solve'] = '%d%%' % round(100 * tc_solve / max(ts_solve, 1e-9) / os.cpu_count())
    if not draw_only:
        res['secs']['checks per frame'] = round(ts_check / len(FRAMES), 2)
    a = time.time()
    for i in DRAWN:
        im = M.draw(outs[i], M.cam_at(ts[i]))
        res['drawn'][str(i)] = _h(np.asarray(im))
    res['secs']['draw per frame'] = round((time.time() - a) / len(DRAWN), 2)
    res['secs']['all'] = round(time.time() - t0, 1)
    res['secs']['processors busy overall'] = '%d%%' % round(100 * (_cpu() - c0) / (time.time() - t0) / os.cpu_count())
    return res


if __name__ == '__main__':
    cmd, d = sys.argv[1], sys.argv[2]
    draw_only = '--draw-only' in sys.argv
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, 'same.json')
    r = measure(draw_only)
    if cmd == 'record':
        json.dump(r, open(path, 'w'), indent=1)
        print('recorded', path, r['secs'])
    else:
        old = json.load(open(path))
        diff = []
        if r['fits'] != old['fits']:
            diff.append('fits %s -> %s' % (old['fits'], r['fits']))
        for k in ('frames', 'drawn'):
            for i, v in r[k].items():
                if old[k].get(i) != v:
                    diff.append('%s %s differs' % (k, i))
        print('old seconds', old['secs'])
        print('new seconds', r['secs'])
        print('SAME' if not diff else 'DIFFERENT:\n  ' + '\n  '.join(diff))
