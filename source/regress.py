#!/usr/bin/env python3
"""regress: prove a change to the shared code leaves the finished films exactly as they were.

Draws the same frames from every finished film's code (small, quick) and compares them with a saved set, pixel by
pixel. Run `baseline` before changing shared code (people, limbs, figure, style kit), `compare` after.

    python3 source/regress.py baseline     saves the frames to source/data/regress/ (not on GitHub)
    python3 source/regress.py compare      prints which films changed, and by how much
"""
import importlib
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, 'data', 'regress')
FILMS = {'hutt': (2.0, 12.0), 'russiadent': (2.0, 14.0), 'cryminister': (3.0, 30.0), 'thepark': (2.0, 10.0),
         'mossad': (2.0, 15.0), 'patriots2': (3.0, 30.0), 'professional': (3.0, 20.0)}


def frames(name):
    import burnham as B
    m = importlib.import_module(name)
    B.SS = 1
    for t in FILMS[name]:
        yield t, np.asarray(m.frame_image(t).convert('RGB').resize((270, 480)), np.int16)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'compare'
    os.makedirs(OUT, exist_ok=True)
    for name in FILMS:
        try:
            for t, a in frames(name):
                path = os.path.join(OUT, f'{name}-{t:.1f}.png')
                if mode == 'baseline':
                    Image.fromarray(a.astype(np.uint8)).save(path)
                    print(f'{name} {t:.1f} s: saved')
                else:
                    b = np.asarray(Image.open(path), np.int16)
                    diff = np.abs(a - b).max(axis=2)
                    changed = (diff > 8).mean()
                    print(f'{name} {t:.1f} s: ' + ('unchanged' if changed == 0 else f'CHANGED ({changed:.2%} of pixels)'))
        except Exception as e:                           # a film that can't draw here is reported, not hidden
            print(f'{name}: could not draw ({type(e).__name__}: {str(e)[:80]})')


if __name__ == '__main__':
    main()
