#!/usr/bin/env python3
"""Line work: every shape outlined, at the house line weight (Sam, 18 Oct: parts of the journalist's and others'
line work were missing or inconsistent, and he had to point them out). A film lists what to check in
LINE_SUBJECTS() -> [(name, draw)], draw(img) painting one character (or prop) alone, large, on a clear
1080 x 1920 layer. Three tests, each fault with where it is:
1. the outside edge is inked all the way round (no run of more than RUN px without an outline);
2. no edge between two colours inside the shape goes without a line (a flat shadow side is the one allowed
   exception: list it in LINE_OK);
3. the lines are one weight: no line much thicker or thinner than the house weight (filled black shapes, such as
   pupils and dark hair, are not lines and are skipped).
A marked picture (faults in red) is saved for one look, instead of a picture per character.

    python3 source/linecheck.py FILM [OUT.jpg]
"""
import importlib
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as ND

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RUN = 25                         # px: an outline gap longer than this is a fault (at 1080 x 1920)
EDGE = 60                        # px: a colour edge with no line this long is a fault (a button, a tie spot: shorter)
STEP = 60.0                      # colour difference that counts as an edge between two flat colours


def analyse(img):
    """(faults as (kind, x, y, detail), a mask of the faulty pixels) for one subject on a clear layer."""
    a = np.asarray(img.convert('RGBA'), np.float32)
    alpha = a[..., 3] > 200
    rgb = a[..., :3]
    luma = rgb @ np.array([0.299, 0.587, 0.114])
    ink = alpha & (luma < 85)
    near_ink = ND.binary_dilation(ink, iterations=3)
    out, bad = [], np.zeros(alpha.shape, bool)
    edge = alpha & ~ND.binary_erosion(alpha, iterations=1)       # 1. the outside edge
    edge[:2], edge[-2:], edge[:, :2], edge[:, -2:] = False, False, False, False   # (cut off by the canvas: not an edge)
    gap = edge & ~near_ink
    lab, n = ND.label(gap, structure=np.ones((3, 3)))
    for i, sl in enumerate(ND.find_objects(lab), 1):
        size = int((lab[sl] == i).sum())
        if size > RUN:
            y, x = (sl[0].start + sl[0].stop) // 2, (sl[1].start + sl[1].stop) // 2
            out.append(('no outline', x, y, f'{size} px of edge'))
            bad |= lab == i
    inside = ND.binary_erosion(alpha, iterations=3) & ~near_ink    # 2. colour edges inside with no line
    # an edge between two broad areas of flat colour: the colour holds THICK px either side of it (a thin stroke of
    # colour, such as a brow, a crease, a hair strand or a seam drawn as a line, is a line itself and is skipped)
    T = 9

    def same(p, q):
        return np.linalg.norm(p - q, axis=-1) < 18
    cedge = np.zeros(alpha.shape, bool)
    L, R = rgb[:, T:-T - 1], rgb[:, T + 1:-T]
    cedge[:, T:-T - 1] = (np.linalg.norm(R - L, axis=-1) > STEP) & same(rgb[:, :-2 * T - 1], L) & same(rgb[:, 2 * T + 1:], R)
    Up, Dn = rgb[T:-T - 1], rgb[T + 1:-T]
    cedge[T:-T - 1] |= (np.linalg.norm(Dn - Up, axis=-1) > STEP) & same(rgb[:-2 * T - 1], Up) & same(rgb[2 * T + 1:], Dn)
    cedge &= inside
    lab, n = ND.label(ND.binary_dilation(cedge), structure=np.ones((3, 3)))
    for i, sl in enumerate(ND.find_objects(lab), 1):
        size = int(((lab[sl] == i) & cedge[sl]).sum())
        if size > EDGE:
            y, x = (sl[0].start + sl[0].stop) // 2, (sl[1].start + sl[1].stop) // 2
            out.append(('edge with no line', x, y, f'{size} px'))
            bad |= (lab == i) & cedge
    dt = ND.distance_transform_edt(ink)                           # 3. line weight
    ridge = ink & (dt >= ND.maximum_filter(dt, size=3) - 1e-6) & (dt > 0.5)
    widths = 2 * dt[ridge]
    if len(widths) > 50:
        house = float(np.median(widths))
        lab, n = ND.label(ink, structure=np.ones((3, 3)))
        for i, sl in enumerate(ND.find_objects(lab), 1):
            m = (lab[sl] == i)
            w = 2 * dt[sl][m & ridge[sl]]
            if len(w) < 30:
                continue
            wm = float(np.median(w))
            if wm > 2.8 * house:                                   # a filled dark shape (a brow, a pupil), not a line
                continue
            if wm > 1.7 * house or wm < 0.55 * house:
                y, x = (sl[0].start + sl[0].stop) // 2, (sl[1].start + sl[1].stop) // 2
                out.append(('line weight', x, y, f'{wm:.1f} px against the house {house:.1f} px'))
                bad[sl] |= m
    return out, bad


def faults(film, sheet=None):
    if not hasattr(film, 'LINE_SUBJECTS'):
        return []
    ok = getattr(film, 'LINE_OK', ())
    import burnham as B
    keep, B.SS = B.SS, 1
    out, tiles = [], []
    for name, draw in film.LINE_SUBJECTS():
        lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        draw(lay)
        found, bad = analyse(lay)
        for kind, x, y, det in found:
            if any(name == n and kind == k and abs(x - ox) < 60 and abs(y - oy) < 60 for n, k, ox, oy in ok):
                continue
            out.append(f'{name}: {kind} at ({x}, {y}): {det}')
        if sheet:
            show = Image.new('RGBA', lay.size, (235, 235, 235, 255))
            show.alpha_composite(lay)
            red = np.asarray(show).copy()
            red[ND.binary_dilation(bad, iterations=4)] = (255, 0, 0, 255)
            tiles.append(Image.fromarray(red).crop(lay.getbbox() or (0, 0, 1080, 1920)))
    B.SS = keep
    if sheet and tiles:
        h = 900
        tiles = [t.resize((max(1, int(t.width * h / t.height)), h)) for t in tiles]
        im = Image.new('RGB', (sum(t.width for t in tiles), h), (255, 255, 255))
        x = 0
        for t in tiles:
            im.paste(t.convert('RGB'), (x, 0))
            x += t.width
        im.save(sheet, quality=85)
    return out


if __name__ == '__main__':
    import burnham as B
    B.SS = 1
    f = faults(importlib.import_module(sys.argv[1]), sys.argv[2] if len(sys.argv) > 2 else None)
    print('\n'.join(f) if f else 'line work: every shape outlined, one weight')
