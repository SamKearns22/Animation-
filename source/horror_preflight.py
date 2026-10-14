#!/usr/bin/env python3
"""Pre-flight for the horror trailer: every frame of every shot checked BEFORE anything is rendered (minutes, not
hours). It solves each character's pose from the shot recipe (no scene build, no render) and tests the skeleton:

  stretches   a bone changes length (a limb grows, a neck detaches)
  bends       a joint goes past what a body does (elbow folded shut, neck snapped back, spine kinked)
  pops        a joint jumps between frames faster than a body moves (unless the recipe lists it in FAST)
  still       nothing moves for over 2 s (a NOTE, not a fault: stillness is a horror tool; say if it is meant)

    python3 horror_preflight.py [shots/s1_chop.py ...]      (default: every shot in shots/)
The recipe may define FAST = [(t0, t1, 'why')] for deliberate fast moves. The scene checks (checks.py) still run on
every frame at render time; this catches pose faults first, cheaply.
"""
import glob
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

BONES = [('shoulder.R', 'elbow.R'), ('elbow.R', 'wrist.R'), ('shoulder.L', 'elbow.L'), ('elbow.L', 'wrist.L'),
         ('neck01', 'neck03'), ('neck03', 'head'), ('spine02', 'spine05')]
ANGLES = [('shoulder.R', 'elbow.R', 'wrist.R', 25, 180, 'right elbow'), ('shoulder.L', 'elbow.L', 'wrist.L', 25, 180, 'left elbow'),
          ('spine02', 'neck02', 'head', 115, 180, 'neck'), ('spine05', 'spine04', 'spine02', 100, 180, 'spine')]   # spine05 is the lowest; a child leaning over a worktop bends to about 118
SPEED = {'wrist': 4.0, 'elbow': 3.0, 'head': 1.6, 'neck': 1.5, 'spine': 1.2, 'shoulder': 1.5}   # metres a second, at most


def angle3(a, b, c):
    v1, v2 = np.asarray(a) - np.asarray(b), np.asarray(c) - np.asarray(b)
    n = np.linalg.norm(v1) * np.linalg.norm(v2) or 1e-9
    return math.degrees(math.acos(max(-1.0, min(1.0, float(v1 @ v2) / n))))


def _solve(args):
    path, t = args
    import shot
    import mother
    import daughter
    fr = shot.load_recipe(path).frame(float(t))
    out = {}
    for name, mod in (('mother', mother), ('daughter', daughter)):
        if fr.get(name) is not None:
            out[name] = {k: np.asarray(v, float) for k, v in mod.solve(fr[name])['joints'].items()}
    return t, out


def audit(path):
    import shot
    rec = shot.load_recipe(path)
    times = getattr(rec, 'TIMES', None)
    if times is None:
        times = np.arange(0, rec.DURATION - 1e-9, 2 / 24)
    fast = getattr(rec, 'FAST', [])
    with Pool(os.cpu_count()) as pool:
        frames = sorted(pool.map(_solve, [(path, float(t)) for t in times]), key=lambda x: x[0])
    faults, notes, seen = [], [], set()

    def fault(key, msg):
        if key not in seen:
            seen.add(key)
            faults.append(msg)
    for who in sorted({w for _, fr in frames for w in fr}):
        seq = [(t, fr[who]) for t, fr in frames if who in fr]
        ref = {b: np.median([np.linalg.norm(j[b[0]] - j[b[1]]) for _, j in seq if b[0] in j and b[1] in j]) for b in BONES
               if all(b[0] in j and b[1] in j for _, j in seq[:1])}
        still_since = None
        for k, (t, j) in enumerate(seq):
            for b, L in ref.items():
                d = np.linalg.norm(j[b[0]] - j[b[1]])
                if abs(d - L) > 0.03 * L:
                    fault((who, 'len', b), f'{who} at {t:.2f} s: {b[0]}-{b[1]} is {d * 100:.1f} cm, normally {L * 100:.1f} (stretches)')
            for a, b, c, lo, hi, nm in ANGLES:
                if a in j and b in j and c in j:
                    v = angle3(j[a], j[b], j[c])
                    if not lo <= v <= hi:
                        fault((who, 'ang', nm), f'{who} at {t:.2f} s: {nm} bent to {v:.0f} degrees (allowed {lo}-{hi})')
            if k:
                t0, j0 = seq[k - 1]
                dt = t - t0
                ok = any(a <= t <= b for a, b, _ in fast)
                moved = max(np.linalg.norm(j[n] - j0[n]) for n in j if n in j0)
                for n in j:
                    lim = next((v for key, v in SPEED.items() if n.startswith(key)), None)
                    if lim and n in j0 and np.linalg.norm(j[n] - j0[n]) / dt > lim and not ok:
                        fault((who, 'pop', n), f'{who} at {t:.2f} s: {n} jumps {np.linalg.norm(j[n] - j0[n]) * 100:.0f} cm '
                                               f'in {dt:.2f} s (faster than a body moves; list it in FAST if meant)')
                if moved < 0.0005:
                    still_since = t0 if still_since is None else still_since
                    if t - still_since > 2.0 and (who, 'still') not in seen:
                        seen.add((who, 'still'))
                        notes.append(f'{who} from {still_since:.2f} s: completely still for over 2 s (fine if meant)')
                else:
                    still_since = None
    return faults, notes


def main():
    paths = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, 'shots', 's*.py')))
    total = 0
    for p in paths:
        faults, notes = audit(p)
        print(f'{os.path.basename(p)}: {len(faults)} fault(s)')
        for f in faults:
            print('  FAULT', f)
        for n in notes:
            print('  note ', n)
        total += len(faults)
    print('PRE-FLIGHT PASSED' if not total else f'{total} FAULT(S): fix them before rendering')
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
