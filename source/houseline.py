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
  survey()         each kit beside a person at matched sizes; ratio of outlines (kittest one_line_weight_every_kit).
python3 source/houseline.py survey
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


def _white():
    from PIL import Image
    return Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))


def _person(d):
    import brexit_is_done as F                       # read only: its people are the crowd pack (CLAUDE.md, tests)
    img = _white()
    F.ACT.person_at(img, F._cam('site'), F.ACT.WORKERS[0], 0, d, 0, 90, None, 0.0, shadow=False)
    return img


def _wolf(d):
    import brexit_is_done as F
    img = _white()
    F.ACT.wolf_at(img, F._cam('site'), 0, d, 0, 1, F.ACT.WF.pose('stand', 0), pal=1, shade=False)
    return img


def _whale(fit, ol=None):
    import whale as W
    cam = W.view_cam((0, -30, 3), (1080, 1920), fit=fit)
    img = _white()
    W.draw(cam, W.Pose(), pattern=0, flap=0, beat=0, ol=ol).paste(img)
    return img


def _horse(sc):
    """A chestnut: its points and mane are coat-coloured, so only its outline is ink (a bay's dark legs are not line)."""
    import burnham as B
    import kit
    import mounts as MO
    B.SS = 1
    kit.install(B)
    img = _white()
    MO.Mount('horse', coat='chestnut').draw(img, B.Cam(1.0, 540, 960), 600, 1500, sc, 0.0, 'stand')
    return img


# each kit: (name, [(size label, drawing function)]): sizes span near to far on a 1080-wide frame
KITS = [
    ('wolf', [('5 m', lambda: _wolf(5.0)), ('10 m', lambda: _wolf(10.0))]),
    ('whale', [('close', lambda: _whale(8)), ('far', lambda: _whale(30))]),
    ('horse', [('near', lambda: _horse(0.4)), ('far', lambda: _horse(0.15))]),
]


def survey(kits=None):
    """[(kit, size, ratio of its outline to a person's)], the person measured at 5, 7 and 10 m (their mean)."""
    person = float(np.mean([ring(_person(d)) for d in (5.0, 7.0, 10.0)]))
    rows = []
    for name, sizes in (kits or KITS):
        for lab, fn in sizes:
            rows.append((name, lab, ring(fn()) / person))
    return rows


def faults(rows):
    return [f'{n} ({lab}): outline {r:.2f} times a person\'s (house: {LOW}-{HIGH})'
            for n, lab, r in rows if not LOW <= r <= HIGH]


if __name__ == '__main__':
    if sys.argv[1:2] == ['survey']:
        rows = survey()
        for n, lab, r in rows:
            print(f'{n:6} {lab:6} {r:.2f}')
        f = faults(rows)
        print('\n'.join(f) if f else 'every kit on the house line')
    else:
        print(__doc__)
