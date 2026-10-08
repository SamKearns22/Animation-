#!/usr/bin/env python3
"""Does a new drawing still look like the approved ones? Compares its tones (brightness, contrast, how much is deep
shadow and how much is paper white, and the whole tonal spread) with the approved frames in lookbook/ for the same
shot (file names start with the shot: s1-, s2-...), so the look can't drift unnoticed between rounds.

    python3 lookbook_check.py DRAWING.png [DRAWING2.png ...]   (or a folder of draw_*.png from shot.py sequence)
A drawing whose name or folder starts with s1/s2/s3 is compared with that shot's lookbook frames, otherwise all.
"""
import glob
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMITS = dict(mean=0.08, std=0.06, dark=0.10, light=0.15, hist=0.45)   # how far a drawing may drift from the lookbook


def tones(path):
    g = np.asarray(Image.open(path).convert('L').resize((270, 480)), float) / 255
    h = np.histogram(g, 32, (0, 1))[0] / g.size
    return dict(mean=g.mean(), std=g.std(), dark=(g < 0.25).mean(), light=(g > 0.85).mean(), hist=h)


def compare(path, refs):
    a = tones(path)
    best = None
    for r in refs:
        b = tones(r)
        d = dict(mean=abs(a['mean'] - b['mean']), std=abs(a['std'] - b['std']), dark=abs(a['dark'] - b['dark']),
                 light=abs(a['light'] - b['light']), hist=float(np.abs(a['hist'] - b['hist']).sum()))
        score = sum(d[k] / LIMITS[k] for k in d)
        if best is None or score < best[0]:
            best = (score, r, d)
    _, r, d = best
    bad = [f'{k} off by {d[k]:.2f} (limit {LIMITS[k]})' for k in d if d[k] > LIMITS[k]]
    return r, bad


def main():
    files = []
    for a in sys.argv[1:]:
        files += sorted(glob.glob(os.path.join(a, 'draw_*.png'))) if os.path.isdir(a) else [a]
    lb = sorted(glob.glob(os.path.join(ROOT, 'lookbook', '*.jpg')) + glob.glob(os.path.join(ROOT, 'lookbook', '*.png')))
    n_bad = 0
    for f in files:
        if np.asarray(Image.open(f).convert('L'), float).mean() < 8:      # a black frame (a cut to black): nothing to compare
            print(f'{os.path.basename(f)}: black, skipped')
            continue
        tag = next((s for s in ('s1', 's2', 's3', 's4', 's5') if s in os.path.basename(os.path.dirname(f) + '/' + f).lower()), None)
        refs = [r for r in lb if tag and os.path.basename(r).startswith(tag)] or lb
        r, bad = compare(f, refs)
        print(f'{os.path.basename(f)}: ' + ('matches ' + os.path.basename(r) if not bad else 'DRIFTS from ' + os.path.basename(r) + ': ' + '; '.join(bad)))
        n_bad += bool(bad)
    print('LOOKBOOK: all match' if not n_bad else f'LOOKBOOK: {n_bad} drawing(s) drift from the approved look')
    sys.exit(1 if n_bad else 0)


if __name__ == '__main__':
    main()
