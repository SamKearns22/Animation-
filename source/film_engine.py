"""film_engine: what every Satire-style film and quick.py share, so a new film only writes its story.

  render          the film, with the PICTURE cached per frame and captions + title put on last: a caption or timing
                  note re-renders nothing (about a minute); --redo SHOT re-renders only that shot.
  print_subtitles the subtitles as text with times, to proofread BEFORE rendering.
  check_mouths    every stretch of speech moves a mouth.
Every review copy (a --small animatic or a --span clip) has the film time and the shot burned into its top-left
corner, so Sam's times point straight at the frame (guides/film-quality-rules.md, rule 29); the full-size final never.
"""
import os
import subprocess

import numpy as np
from PIL import Image

_JOB = {}


def _frame(args):
    i, reuse = args
    j = _JOB
    t = i / j['fps']
    j['set_ss'](j['ss'])
    path = os.path.join(j['cache'], f'{i:04d}.png')
    if reuse and os.path.exists(path):
        pic = Image.open(path)
        pic.load()
    else:
        pic = j['picture'](t)
        pic.save(path, compress_level=1)
    im = j['overlay'](pic, t).convert('RGB').resize(j['size'], Image.LANCZOS)
    if j.get('stamp'):
        stamp(im, t, j['shot_of'](t))
    return np.asarray(im).tobytes()


def stamp(im, t, shot):
    """The film time and shot in the top-left corner (inside TikTok's top bar, never over the picture's action)."""
    from PIL import ImageDraw, ImageFont
    k = im.width / 1080
    f = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'DejaVuSans-Bold.ttf'),
                           max(12, int(40 * k)))
    txt = f'{t:5.2f} s   shot {shot}'
    d = ImageDraw.Draw(im, 'RGBA')
    x0, y0, x1, y1 = d.textbbox((int(24 * k), int(24 * k)), txt, font=f)
    d.rectangle((x0 - 10 * k, y0 - 8 * k, x1 + 10 * k, y1 + 8 * k), fill=(0, 0, 0, 170))
    d.text((int(24 * k), int(24 * k)), txt, font=f, fill=(255, 255, 255))
    return im


def render(name, out, *, size, ss, fps, dur, picture, overlay, shot_of, sound, write_wav, set_ss, crf=20,
           reuse=False, redo=(), preset='slow', span=None, stamp=None):
    """picture(t) -> image without captions or title; overlay(img, t) -> img with them; shot_of(t) -> shot name;
    sound() -> the mixed soundtrack array; write_wav(path, mix). The cache ($FILM_CACHE or ~/.cache/filmcache) is
    only trusted when reuse=True: it cannot know what code changed, so name the shots that did (redo).
    span=(t0, t1) renders just that stretch, with its sound: a quick clip of one moment for notes on motion (Sam,
    18 Oct: stills can't show a problem in movement, and a whole animatic is wasted on one moment).
    stamp: the time and shot in the corner; None (the default) = on for every review copy (a span, or smaller than
    full size: rule 29), off for the full-size final."""
    import imageio_ffmpeg
    from multiprocessing import Pool
    cache = os.path.join(os.environ.get('FILM_CACHE', os.path.expanduser('~/.cache/filmcache')),
                         f'{name}-{size[0]}x{size[1]}-ss{ss}')
    os.makedirs(cache, exist_ok=True)
    n = int(round(dur * fps))
    first = 0
    if span:
        first, n = int(round(span[0] * fps)), min(n, int(round(span[1] * fps)))
    redo_set = {i for i in range(n) if shot_of(i / fps) in redo}
    if stamp is None:
        stamp = bool(span) or size[0] < 1080 and size[1] < 1920
    _JOB.update(fps=fps, ss=ss, size=size, cache=cache, picture=picture, overlay=overlay, set_ss=set_ss,
                shot_of=shot_of, stamp=stamp)
    wav = out + '.wav'
    write_wav(wav, sound())
    print(f'picture cache: {cache}' + (f' (re-rendering {sorted(redo)}, reusing the rest)' if reuse else ''), flush=True)
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{size[0]}x{size[1]}', '-r', str(fps), '-i', '-', *(['-ss', f'{first / fps:.3f}'] if first else []), '-i', wav, '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', str(crf), '-preset', preset, '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for k, fr in enumerate(pool.imap(_frame, [(i, reuse and i not in redo_set) for i in range(first, n)], chunksize=2)):
            p.stdin.write(fr)
            if k % 48 == 0:
                print(f'frame {k}/{n - first}', flush=True)
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print(f'done: {out} ({os.path.getsize(out) / 1e6:.2f} MB)', flush=True)


def print_subtitles(caption_at, end, fps):
    rows, last = [], None
    for i in range(int(end * fps) + 1):
        c = caption_at(i / fps)
        if c != last:
            rows.append((i / fps, c))
            last = c
    print('subtitles (proofread these):')
    for (t, c), nxt in zip(rows, rows[1:] + [(end, None)]):
        if c:
            print(f'  {t:6.2f}-{nxt[0]:6.2f} s  {c}')


def check_mouths(track, windows, min_cover=0.3):
    """track: [(t0, t1, shape)] in film time; windows: [(start, end)] when someone speaks. Returns faults."""
    out = []
    for a, b in windows:
        if b - a < 0.25:
            continue
        moving = sum(max(0.0, min(b, y1) - max(a, y0)) for y0, y1, sh in track if sh != 'rest')
        if moving < min_cover * (b - a):
            out.append(f'no mouth movement for the speech at {a:.2f}-{b:.2f} s')
    return out
