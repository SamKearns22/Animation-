#!/usr/bin/env python3
"""MAP  still (savings 1, Sam's go, 27 Nov: "Why do you redraw the still rather than taking the one you had already
drawn?"). A fixing chat's look at a note: the BEFORE picture is cut straight from the film's latest render (the clean render beside the animatic) (what Sam
saw when he wrote the note: one step, nothing to get wrong; the replay test spent 3 of 19 steps redrawing a shot and
drew the wrong layer first); the AFTER picture is drawn fresh by the film's frame_image, the same crop beside it.

    before(film, t) ......... the animatic's frame at t (animations/drafts/FILM-animatic.mp4, else -clean.mp4)
    after(film, t) .......... the film's frame_image(t) as the code draws it now, at the video's size
    sheet(film, ts, box, ...) one labelled strip: before (and after) per time, cropped to box, written to OUT

    python3 source/still.py FILM T [T2 ...] [--box X0,Y0,X1,Y1] [--after] [--out PATH]
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
OUT_DIR = os.path.expanduser('~/.cache/stills')


def video(film):
    """The latest clean render (the animatic's pictures on the film's own clock), else the animatic, else None. The
    animatic itself runs on another clock (Brexit: 33.9 s against the film's 35.5 s), so a time from the notes table
    lands on the wrong frame in it."""
    slug = film.replace('_', '-')
    for kind in ('clean', 'animatic'):
        p = os.path.join(ROOT, 'animations', 'drafts', f'{slug}-{kind}.mp4')
        if os.path.exists(p):
            return p
    return None


def before(film, t, path=None):
    """The animatic's frame at t as a PIL image (None when the film has no animatic yet)."""
    from PIL import Image
    import io
    src = path or video(film)
    if not src:
        return None
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1', '-f', 'image2pipe',
                          '-vcodec', 'png', '-'], capture_output=True).stdout
    return Image.open(io.BytesIO(raw)).convert('RGB') if raw else None


def after(film, t, size=None):
    """The film's frame_image(t) as its code draws it now (resized to the animatic's size when given)."""
    import importlib
    mod = importlib.import_module(film.replace('-', '_'))
    im = mod.frame_image(t).convert('RGB')
    return im.resize(size) if size and im.size != size else im


def sheet(film, ts, box=None, with_after=False, out=None):
    """One strip: per time, the animatic's frame (and the code's) cropped to box, labelled; returns the path."""
    from PIL import Image, ImageDraw
    tiles = []
    for t in ts:
        b = before(film, t)
        row = [('before (last render)', b)] if b is not None else []
        if with_after:
            row.append(('after (code now)', after(film, t, b.size if b is not None else None)))
        for label, im in row:
            im = im.crop(box) if box else im
            k = 540 / max(im.size)
            im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))))
            ImageDraw.Draw(im).text((6, im.height - 16), f'{t:.2f}s {label}', fill=(255, 0, 0))
            tiles.append(im)
    if not tiles:
        return None
    w, h = sum(i.width for i in tiles), max(i.height for i in tiles)
    s = Image.new('RGB', (w, h), 'white')
    x = 0
    for i in tiles:
        s.paste(i, (x, 0))
        x += i.width
    os.makedirs(OUT_DIR, exist_ok=True)
    out = out or os.path.join(OUT_DIR, f'{film}-{"-".join(f"{t:.2f}" for t in ts)}.png')
    s.save(out)
    return out


def test():
    """The animatic's frame and the code's frame line up in time (an unchanged film: before ~ after)."""
    import numpy as np
    film = 'brexit-is-done'
    if not video(film):
        return False, 'COULD NOT TEST: no Brexit animatic in animations/drafts'
    t = 20.0
    b = before(film, t)
    a = after(film, t, b.size)
    diff = float(np.abs(np.asarray(b, float) - np.asarray(a, float)).mean())
    late = min(float(np.abs(np.asarray(before(film, t + dt), float) - np.asarray(a, float)).mean()) for dt in (-1.5, 1.5))
    p = sheet(film, [t], with_after=True, out=os.path.join(OUT_DIR, 'still-test.png'))
    ok = b is not None and p is not None and diff < late
    return ok, (f'animatic {b.size} cut at {t}s; code frame differs by {diff:.1f} per pixel, the nearest frame 1.5 s off by '
                f'{late:.1f} (the times line up: {diff < late}); sheet written')


def main(a):
    if not a or a[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    if a[0] == 'test':
        ok, d = test()
        print('PASS' if ok else 'FAIL', d)
        return 0 if ok else 1
    film, rest = a[0], a[1:]
    box = None
    if '--box' in rest:
        i = rest.index('--box')
        box = tuple(int(v) for v in rest[i + 1].split(','))
        rest = rest[:i] + rest[i + 2:]
    out = None
    if '--out' in rest:
        i = rest.index('--out')
        out = rest[i + 1]
        rest = rest[:i] + rest[i + 2:]
    with_after = '--after' in rest
    ts = [float(x) for x in rest if x != '--after']
    p = sheet(film, ts, box, with_after, out)
    print(f'still: {p}' if p else f'still: no animatic for {film} yet (animations/drafts); draw with --after')
    return 0 if p else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
