"""satire_parts: the two small pieces hutt.py and polanski.py borrowed from the old quick-video tool (removed 11 Nov).

Importing it also does what importing quick.py did for those films: mossad's brows, tilted heads and hair styles are
patched into burnham, mouths.py is installed and every burnham hand is a plain circle, so their pictures do not change.

    chand(p, x, y, skin, r=26)                 the plain circle hand
    caption(img, s, shout=False, bottom=1480)  the old white caption (finished films only; new films use the kit's)
"""
import math
import os
import sys

from PIL import ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import mossad                # noqa: E402,F401  (brows, tilted heads, hair styles, limiter: patched into burnham)
import figure                # noqa: E402,F401  the same imports, in the same order, as quick.py had: same patches
import mouths                # noqa: E402
import mossad_audio          # noqa: E402,F401
from ed import INK           # noqa: E402
import filmkit               # noqa: E402,F401
import film_engine           # noqa: E402,F401
import satire_style          # noqa: E402,F401

mouths.install(B)


def chand(p, x, y, skin, r=26):
    p.ell(x, y, r, r, skin, INK, 2.4)


def gesture_hand(p, el, wr, shape, skin, extra=None, t=0.0):
    d = (wr[0] - el[0], wr[1] - el[1])
    n = math.hypot(*d) or 1.0
    chand(p, wr[0] + d[0] / n * 12, wr[1] + d[1] / n * 12, skin)


B.gesture_hand = gesture_hand          # every hand is a plain circle (props are laid over it), as quick.py did


def caption(img, s, shout=False, bottom=1480):
    SS = B.SS
    d = ImageDraw.Draw(img)
    if shout:
        size = 120
        while size > 40:
            f = ImageFont.truetype(B.ANTON, size * SS)
            rows = B.wrap(s.upper(), f, 700 * SS)
            if len(rows) <= 2:
                break
            size -= 4
        for i, row in enumerate(rows):
            y = (bottom - 0.6 * size - size * 1.1 * (len(rows) - 1 - i)) * SS
            d.text((540 * SS, y), row, font=f, fill=(255, 255, 255), anchor='mm', stroke_width=int(size * 0.07) * SS, stroke_fill=(0, 0, 0))
        return
    f = ImageFont.truetype(B.SANS, 50 * SS)
    rows = B.wrap(s, f, 700 * SS)
    for i, row in enumerate(rows):
        y = (bottom - 34 - 64 * (len(rows) - 1 - i)) * SS
        d.text((540 * SS, y), row, font=f, fill=(255, 255, 255), anchor='mm', stroke_width=5 * SS, stroke_fill=(0, 0, 0))

