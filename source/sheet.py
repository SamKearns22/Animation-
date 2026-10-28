#!/usr/bin/env python3
"""sheet: ONE labelled contact sheet from any film, in one command (film-quality-rules 48: look at several frames once,
never one at a time; Build list 27 Oct, item 0).

    python3 source/sheet.py FILM TIMES... [--out PATH] [--crop X0 Y0 X1 Y1] [--width PX] [--cols N] [--clean]

TIMES are seconds (12.5), ranges (3.6-4.0: every frame between, at the film's FPS) or ranges with a step
(20-30/2: every 2 s). Each tile carries its time and shot. --crop cuts the same box (full-frame pixels, 1080 x 1920)
from every frame, for a detail (a hand, a face); --width is each tile's width (default 270, a phone-ish size; 540 for
detail); --clean draws the picture without captions and title (the film's picture(t), if it has one). The sheet is
saved to --out (default source/data/FILM-sheet.jpg) and its path printed: open that one file.
"""
import importlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402

_JOB = {}


def times(specs, fps):
    """'12.5', '3.6-4.0' (every frame), '20-30/2' (every 2 s) -> sorted seconds."""
    out = []
    for s in specs:
        step = None
        if '/' in s:
            s, step = s.split('/')
            step = float(step)
        if '-' in s[1:]:
            a, b = (float(x) for x in s.split('-', 1)) if not s.startswith('-') else (float(s), float(s))
            step = step or 1.0 / fps
            n = int(round((b - a) / step))
            out += [round(a + k * step, 4) for k in range(n + 1)]
        else:
            out.append(float(s))
    return sorted(set(out))


def _tile(t):
    film, crop, width, clean = _JOB['film'], _JOB['crop'], _JOB['width'], _JOB['clean']
    im = (film.picture(t) if clean and hasattr(film, 'picture') else film.frame_image(t)).convert('RGB')
    if im.size != (1080, 1920):
        im = im.resize((1080, 1920))
    if crop:
        im = im.crop(crop)
    h = int(round(im.height * width / im.width))
    im = im.resize((width, h))
    shot = next((s[0] for s in getattr(film, 'SHOTS', []) if s[1] <= t < s[2]), '')
    tile = Image.new('RGB', (width, h + 30), (18, 18, 22))
    tile.paste(im, (0, 30))
    font = ImageFont.truetype(B.SANS, 22)
    ImageDraw.Draw(tile).text((6, 3), f'{t:.2f} s  {shot}', font=font, fill=(255, 255, 255))
    return tile


def make(film, ts, out, crop=None, width=270, cols=None, clean=False, ss=1):
    """The sheet of film at times ts, saved to out; returns out."""
    _JOB.update(film=film, crop=crop, width=width, clean=clean)
    B.SS = ss
    from multiprocessing import Pool
    with Pool(min(len(ts), os.cpu_count())) as pool:
        tiles = pool.map(_tile, ts)
    cols = cols or min(len(tiles), max(1, 2160 // width))
    w, h = tiles[0].size
    hmax = max(tl.height for tl in tiles)
    sheet = Image.new('RGB', (cols * w, ((len(tiles) + cols - 1) // cols) * hmax), (8, 8, 10))
    for i, tl in enumerate(tiles):
        sheet.paste(tl, ((i % cols) * w, (i // cols) * hmax))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sheet.save(out, quality=85)
    return out


def main():
    args = sys.argv[1:]

    def opt(name, n=1, default=None):
        if name not in args:
            return default
        k = args.index(name)
        v = args[k + 1:k + 1 + n]
        del args[k:k + 1 + n]
        return v if n > 1 else (v[0] if n == 1 else True)
    out = opt('--out')
    crop = opt('--crop', 4)
    width = int(opt('--width', default=270))
    cols = opt('--cols')
    clean = opt('--clean', 0)
    if len(args) < 2:
        sys.exit(__doc__)
    name, specs = args[0], args[1:]
    film = importlib.import_module(name)
    ts = times(specs, getattr(film, 'FPS', 12))
    if len(ts) > 60:
        sys.exit(f'sheet: {len(ts)} frames is too many for one look (60 at most): use a step, e.g. 0-40/1')
    out = out or os.path.join(HERE, 'data', f'{name}-sheet.jpg')
    print(make(film, ts, out, tuple(int(c) for c in crop) if crop else None, width, int(cols) if cols else None,
               bool(clean)))


if __name__ == '__main__':
    main()
