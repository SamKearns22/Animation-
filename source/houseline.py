"""MAP: one line weight for every kit (R8 A6, 27 Nov).
Open Wounds note 16 (Sam, 26 Nov: "the line work on the wolves is very thick in comparison to our house style") was
one kit drawing its own outline. The fix there (wolf.house_ctx) is now the shared rule: every kit's outline is the
people's own at the same size on screen.
  weight(ppm)      the people's pen weight (lying._lw) for a body this many frame pixels a metre: for kits that draw
                   with burnham's Pen (wolf, horse, robot) or scale their own lines from it.
  px(W)            the house outline in final frame pixels for kits that draw their own fixed-pixel line (whale):
                   measured to match a person at the same frame width (people measure about 2 px at 1080 wide, any size).
  ctx(X, s, ppm)   set a kit's drawing context (X.ol, X.line_k) to the house weight: wolf.house_ctx's rule for any kit.
  ring(img)        the measurer: how thick the outer ink outline is round a drawing on white (house ink only, reached
                   from the outside edge, so a dark coat or the whale's dark back is not read as line).
  faults(rows)     kits off the house line; the survey itself (each kit beside a person) is kittests.line_survey,
                   since it draws a film's cast (kittest one_line_weight_every_kit).
python3 source/kittests.py one_line_weight_every_kit   (the survey, each kit beside a person)
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUT = (20, 16, 16)          # the house ink (satire_style.OUT)
INK_SEEN = (22, 18, 19)     # the people's ink as it lands in a frame (measured, 27 Nov)
PX_1080 = 1.5               # an own-pixel outline at 1080 wide that looks and measures like a person's (27 Nov)
LOW, HIGH = 0.7, 1.35       # a kit's outline within these times a person's counts as the house line


def weight(ppm):
    """The people's own pen weight for a body this many frame pixels a metre (lying._lw)."""
    import lying
    return float(lying._lw(ppm))


def px(W=1080):
    """The house outline in final frame pixels for a frame W wide (kits that draw their own pixel lines)."""
    return max(1.0, PX_1080 * W / 1080.0)


def ctx(X, s, ppm, native=5.0):
    """A kit drawing context of scale s whose own outline is `native` kit units: set to the house weight at ppm
    (X.ol) with every crease and inner line in proportion (X.line_k). wolf.house_ctx is this with native 5."""
    ol = weight(ppm)
    X.line_k = min(1.0, ol / max(1e-6, native * s))
    X.ol = min(native * s, ol) if native * s > 1.0 else ol
    return X


def ring(img):
    """Outline width (px) round a drawing on white: the house-ink shapes that reach the outside edge, their area
    over half their edge length (a line w wide has area w x length and two sides). Solid ink patches wider than any
    line (a black mane, a pupil) are taken out first; dark coats are not house ink, so never read as line."""
    from scipy import ndimage as ND
    a = np.asarray(img.convert('RGB')).astype(int)
    white = a.min(-1) > 245
    lab, _ = ND.label(white)
    bg = np.isin(lab, np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) & white
    d = ND.distance_transform_edt(~bg)
    ink = np.abs(a - np.array(INK_SEEN)).max(-1) <= 20
    yy, xx = np.mgrid[-7:8, -7:8]
    ink &= ~ND.binary_opening(ink, structure=(yy * yy + xx * xx) <= 49)
    lab2, _ = ND.label(ink)
    keep = np.unique(lab2[ink & (d <= 2.5)])
    m = np.isin(lab2, keep[keep > 0])
    edge = int((m & ~ND.binary_erosion(m)).sum())
    return 2.0 * float(m.sum()) / max(1, edge)


def faults(rows, low=LOW, high=HIGH):
    """rows: [(kit, size label, its outline / a person's)] -> a line per kit off the house line."""
    return [f'{n} ({lab}): outline {r:.2f} times a person\'s (house: {low}-{high})'
            for n, lab, r in rows if not low <= r <= high]


if __name__ == '__main__':
    print(__doc__)                    # the survey: python3 source/kittests.py one_line_weight_every_kit
