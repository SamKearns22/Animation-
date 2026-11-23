#!/usr/bin/env python3
"""gta_film: Grand Theft Autism's eight shots on the whole film's clock, for sheet.py (Sam's standing order, 20 Nov:
"keep working on this until you can render the whole film shot sheet").

MAP
  SHOTS ........... (name, start, end) on the film's clock: the opener (6.5 s + 0.5 s of darkness first, Sam 21 Nov), then the plan's
                    rows 2-8 at their planned lengths
  frame_image ..... the frame at film time t, from the shot's own file (gta_opener, gta_rehearse, gta_shots58)

    python3 source/sheet.py gta_film 1.0 5.5 ... --out OUT.jpg
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gta_opener as O           # noqa: E402
import gta_rehearse as R         # noqa: E402
import gta_shots58 as M          # noqa: E402

FPS = 12
LEAD = 0.125                    # Sam, 23 Nov: the darkness 75% shorter (was 0.5 s, Sam 21 Nov) before the logo swipes in
LEAD_WAS = 0.5                  # the clock every time in grand_theft_autism.py was written on (shifted by LEAD - LEAD_WAS)
_L = [O.DUR + LEAD, R.SHOT2_LEN, R.SHOT3_LEN, R.SHOT4_LEN] + [M.SHOTS58[n][1] for n in (5, 6, 7, 8)]
SHOTS, _t = [], 0.0
for _n, _ln in enumerate(_L, 1):
    SHOTS.append((f'shot {_n}', round(_t, 3), round(_t + _ln, 3)))
    _t += _ln
LENGTH = _t
_OL = None


def frame_image(t):
    global _OL
    n = next((k for k, (_, a, b) in enumerate(SHOTS, 1) if a <= t < b), len(SHOTS))
    u = t - SHOTS[n - 1][1]
    if n == 1:
        if _OL is None:
            _OL = O.layers()
        if u < LEAD:
            return O.dark_frame()
        return O.frame(u - LEAD, *_OL)
    if n == 2:
        return R.shot2(u)
    if n == 3:
        return R.shot3(u)
    if n == 4:
        return R.shot4(u)
    return M.shot_fn(n)(u)


if __name__ == '__main__':
    for s in SHOTS:
        print(*s)
    print('length', round(LENGTH, 2))
