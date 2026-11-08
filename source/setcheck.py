#!/usr/bin/env python3
"""Rule 83 (Sam, 8 Nov, Ad-Vanced Notice note 42b: the study's portrait clipped into the mantel clock and nothing caught
it): in a flat painted set, no painted object overlaps another unless the set lists it as meant. A set file gives
SET_BOXES = [(name, (x0, y0, x1, y1))] in any one unit (its wall metres, or screen px) and SET_MEANT = [(a, b, why)];
the film's checks() calls faults(SET_BOXES, SET_MEANT).

    python3 source/setcheck.py SETMODULE
"""
import importlib
import sys


def faults(boxes, meant=()):
    ok = {frozenset((a, b)) for a, b, *_ in meant}
    out = []
    for i, (a, A) in enumerate(boxes):
        for b, Bx in boxes[i + 1:]:
            w = min(A[2], Bx[2]) - max(A[0], Bx[0])
            h = min(A[3], Bx[3]) - max(A[1], Bx[1])
            if w > 0 and h > 0 and frozenset((a, b)) not in ok:
                out.append(f'SET OVERLAP (rule 83): {a} and {b} overlap ({w:.3g} x {h:.3g}): move one, or list it in '
                           f'SET_MEANT with why')
    return out


if __name__ == '__main__':
    m = importlib.import_module(sys.argv[1])
    f = faults(m.SET_BOXES, getattr(m, 'SET_MEANT', ()))
    print('\n'.join(f) if f else 'set overlaps: none unmeant')
