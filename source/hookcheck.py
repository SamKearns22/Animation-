#!/usr/bin/env python3
"""The Hook Text must not cover anything that matters (Sam, 18 Oct: it sat over the MILLBANK TOWER sign). A film
lists what must stay readable in KEEP_CLEAR [(name, box_at)], box_at(t) -> (x0, y0, x1, y1) on the 1080 x 1920
frame (or None when not in view), and its Hook Text in HOOK = (text, {'y': .., 'x': .., 'until': .., 'centre': ..})
with the same settings finish.py is given. preflight.py runs it; each fault names the time and the thing covered.

    python3 source/hookcheck.py FILM
"""
import importlib
import os
import sys
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hook_text as H            # noqa: E402


def hook_box(text, y=880, x=None, centre=False, w=None, **_):
    """Where the Hook Text's white boxes sit on the frame (x0, y0, x1, y1)."""
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, 'hook.png')
        H.card(1080, 1920, text, y, png, centre=centre, x_mid=x, width=w)
        return Image.open(png).getbbox()


def faults(film):
    if not hasattr(film, 'HOOK') or not hasattr(film, 'KEEP_CLEAR'):
        return []
    text, opts = film.HOOK
    hb = hook_box(text, **opts)
    until = opts.get('until', 3.6)
    fps = getattr(film, 'FPS', 12)
    out = []
    for name, box_at in film.KEEP_CLEAR:
        for i in range(int(until * fps)):
            b = box_at(i / fps)
            if b and min(hb[2], b[2]) - max(hb[0], b[0]) > 0 and min(hb[3], b[3]) - max(hb[1], b[1]) > 0:
                out.append(f'{i / fps:.2f} s: the Hook Text {hb} covers {name} {tuple(int(v) for v in b)}')
                break
    return out


if __name__ == '__main__':
    f = faults(importlib.import_module(sys.argv[1]))
    print('\n'.join(f) if f else 'Hook Text check: clear of everything listed')
