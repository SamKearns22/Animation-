#!/usr/bin/env python3
"""MAP  cutmatch: the cut-match check (GTA chat 26, Sam 21 Nov: "Jason's glitch at the shot 4 -> 5 join").

A cut on the SAME camera (the shots join without the view changing) must not jump: whatever is not moving fast
stays where it was. No check compared a shot's last drawing with the next shot's first, so Jason became another
drawing at 22.3 s (two figure kits) and nothing saw it.

For each cut: the last four drawings of shot n and the first drawing of shot n+1. The scenery's top band (sky, roofs) says whether the camera is the same (its change across the
cut no bigger than normal movement). On a same-camera cut, the change across it, cell by cell, is compared with the
change between the two drawings before it (normal movement): cells that jump much more than they moved are faults,
named by place, with a marked picture.

    python3 source/cutmatch.py FILM_MODULE [--out DIR]     e.g. gta_film (needs SHOTS, FPS, frame_image(t))
    import cutmatch; cutmatch.faults(module, out_dir)       -> ['cut 4->5 (22.30 s): ...', ...]
"""
import importlib
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

W, H = 270, 480          # compared at this size (phone size: what a viewer sees jump)
GRID = 12                # cells across (rows in proportion)
SAME_CAM = 2.0           # top-band change across the cut at most this x normal movement (+ a floor): same camera
JUMP = 3.0               # a cell's change across the cut this x its normal movement (+ a floor) is a jump
FLOOR = 6.0              # grey levels: changes below this are noise (shake, glints)


def _arr(im):
    return np.asarray(im.convert('RGB').resize((W, H), Image.BILINEAR), np.float32)


def _diff(x, y):
    """The change from x to y with any even wash taken out (a siren's red or blue light tints the whole frame:
    first run, 21 Nov, flagged cuts 3->4 and 7->8 on that alone): each colour's median change is removed."""
    d = y - x
    return np.abs(d - np.median(d.reshape(-1, 3), axis=0))


def _cells(d):
    """Mean change per cell (rows, cols)."""
    g = d.mean(axis=2)
    ch = H // (W // GRID)
    cw = W // GRID
    rows = H // ch
    return np.array([[g[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw].mean() for c in range(GRID)] for r in range(rows)]), ch, cw


def check_cut(frame_image, t_cut, fps, label, out=None):
    prev = [_arr(frame_image(t_cut - k / fps)) for k in (4, 3, 2, 1)]
    a1 = prev[-1]
    b = _arr(frame_image(t_cut))
    # normal movement: the most each cell changed between any two of the four drawings before the cut (a siren
    # flips blue/red every few drawings: two drawings alone missed it, first run 21 Nov flagged 3->4 and 7->8)
    cells = [_cells(_diff(x, y)) for x, y in zip(prev, prev[1:])]
    ch, cw = cells[0][1], cells[0][2]
    move = np.max([c[0] for c in cells], axis=0)
    cut, _, _ = _cells(_diff(a1, b))
    top = slice(0, max(1, cut.shape[0] // 4))
    same = cut[top].mean() <= SAME_CAM * move[top].mean() + FLOOR
    if not same:
        return [], False
    bad = cut > JUMP * move + FLOOR
    faults = []
    if bad.any():
        rows, cols = np.nonzero(bad)
        where = lambda r, c: ('top' if r < cut.shape[0] / 3 else 'middle' if r < 2 * cut.shape[0] / 3 else 'bottom') + \
            ' ' + ('left' if c < GRID / 3 else 'centre' if c < 2 * GRID / 3 else 'right')
        places = sorted({where(r, c) for r, c in zip(rows, cols)})
        faults.append(f'{label} ({t_cut:.2f} s): same camera, but {int(bad.sum())} of {bad.size} cells jump at the cut '
                      f'(worst {cut[bad].max():.0f} grey levels vs {move[bad].max():.0f} of normal movement): '
                      f'{", ".join(places)}')
        if out:
            os.makedirs(out, exist_ok=True)
            pa, pb = Image.fromarray(a1.astype(np.uint8)), Image.fromarray(b.astype(np.uint8))
            for im in (pa, pb):
                d = ImageDraw.Draw(im)
                for r, c in zip(rows, cols):
                    d.rectangle([c * cw, r * ch, (c + 1) * cw - 1, (r + 1) * ch - 1], outline=(255, 0, 0), width=2)
            sh = Image.new('RGB', (2 * W + 6, H), 'white')
            sh.paste(pa, (0, 0))
            sh.paste(pb, (W + 6, 0))
            fn = os.path.join(out, f'cutmatch-{label.replace(" ", "").replace(">", "")}.jpg')
            sh.save(fn, quality=88)
            faults[-1] += f' (picture {fn})'
    return faults, True


def faults(mod, out=None, only=None):
    res = []
    shots = mod.SHOTS
    fps = getattr(mod, 'FPS', 12)
    for (na, _, ea), (nb, sb, _) in zip(shots, shots[1:]):
        lab = f'cut {na.split()[-1]}->{nb.split()[-1]}'
        if only and lab not in only:
            continue
        f, same = check_cut(mod.frame_image, sb, fps, lab, out)
        res += f
        if not f:
            print(f'cutmatch: {lab} ({sb:.2f} s): ' + ('same camera, clean' if same else 'a new camera (a real cut)'))
    return res


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(2)
    out = a[a.index('--out') + 1] if '--out' in a else None
    only = [x.replace('_', ' ') for x in a[a.index('--only') + 1].split(',')] if '--only' in a else None
    m = importlib.import_module(a[0])
    fl = faults(m, out, only)
    print('\n'.join(fl) or 'cutmatch: clean')
    sys.exit(1 if fl else 0)
