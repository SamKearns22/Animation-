"""film_engine: what every Satire-style film and quick.py share, so a new film only writes its story.

  render          the film, with the PICTURE cached per frame and captions + title put on last: a caption or timing
                  note re-renders nothing (about a minute); --redo SHOT re-renders only that shot.
  print_subtitles the subtitles as text with times, to proofread BEFORE rendering.
  check_mouths    every stretch of speech moves a mouth.
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
    return np.asarray(j['overlay'](pic, t).convert('RGB').resize(j['size'], Image.LANCZOS)).tobytes()


def render(name, out, *, size, ss, fps, dur, picture, overlay, shot_of, sound, write_wav, set_ss, crf=20,
           reuse=False, redo=(), preset='slow'):
    """picture(t) -> image without captions or title; overlay(img, t) -> img with them; shot_of(t) -> shot name;
    sound() -> the mixed soundtrack array; write_wav(path, mix). The cache ($FILM_CACHE or ~/.cache/filmcache) is
    only trusted when reuse=True: it cannot know what code changed, so name the shots that did (redo)."""
    import imageio_ffmpeg
    from multiprocessing import Pool
    cache = os.path.join(os.environ.get('FILM_CACHE', os.path.expanduser('~/.cache/filmcache')),
                         f'{name}-{size[0]}x{size[1]}-ss{ss}')
    os.makedirs(cache, exist_ok=True)
    n = int(round(dur * fps))
    redo_set = {i for i in range(n) if shot_of(i / fps) in redo}
    _JOB.update(fps=fps, ss=ss, size=size, cache=cache, picture=picture, overlay=overlay, set_ss=set_ss)
    wav = out + '.wav'
    write_wav(wav, sound())
    print(f'picture cache: {cache}' + (f' (re-rendering {sorted(redo)}, reusing the rest)' if reuse else ''), flush=True)
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{size[0]}x{size[1]}', '-r', str(fps), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', str(crf), '-preset', preset, '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for k, fr in enumerate(pool.imap(_frame, [(i, reuse and i not in redo_set) for i in range(n)], chunksize=2)):
            p.stdin.write(fr)
            if k % 48 == 0:
                print(f'frame {k}/{n}', flush=True)
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
