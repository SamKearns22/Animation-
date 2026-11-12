"""film_engine: what every Satire-style film shares, so a new film only writes its story.

  render          the film, with the PICTURE cached per frame and captions + title put on last: a caption or timing
                  note re-renders nothing (about a minute); --redo SHOT re-renders only that shot. The house look
                  (rule S7, house_look.py: paper, light top edges, soft shadows) goes on every drawing here, once,
                  before the captions; a film drawn at 12 a second is written as a 24 fps file, each drawing held
                  for 2 frames (look_faults: what pre-flight checks).
  print_subtitles the subtitles as text with times, to proofread BEFORE rendering.
  check_mouths    every stretch of speech moves a mouth.
Every review copy (a --small animatic or a --span clip) has the film time and the shot burned into its top-left
corner, so Sam's times point straight at the frame (guides/film-quality-rules.md, rule 29); the full-size final never.
"""
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image

_JOB = {}
HERE = os.path.dirname(os.path.abspath(__file__))
PASSES = os.path.join(os.path.dirname(HERE), 'review', 'preflight-pass')   # rule 59: pre-flight's pass stamps


DRAW_FPS, FILE_FPS = 12, 24     # rule S7: drawings a second, frames a second in the file
HOUSE_LOOK = False               # rule S7 on for every film: True once Sam says Y to the side-by-side (12 Nov)


def look_faults(film):
    """Rule S7, for pre-flight: the house look is the engine's alone (a film never lays its own paper, so it goes on
    once), and the film is drawn at 12 a second, so its 24 fps file has every frame in a pair; a film drawn at 24
    says why (SMOOTH_WHY: slow camera glides judder in steps)."""
    import inspect
    out = []
    fps = getattr(film, 'FPS', None)
    if fps != DRAW_FPS and not getattr(film, 'SMOOTH_WHY', None):
        out.append(f'S7: drawn at {fps} a second, not {DRAW_FPS} (frames in pairs); if smooth on purpose, set SMOOTH_WHY')
    try:
        src = inspect.getsource(film)
    except (OSError, TypeError):
        src = ''
    if 'house_look' in src or 'lay_on_paper' in src:
        out.append('S7: the film lays the house look itself; the engine does it (it would go on twice)')
    return out


def code_hash():
    """One fingerprint of all the code (source/ and its folders): any change to any file changes it, so a pass stamp
    can only ever mean "pre-flight passed on the code as it is now"."""
    h = hashlib.sha1()
    for f in sorted(glob.glob(os.path.join(HERE, '**', '*.py'), recursive=True)):
        if '__pycache__' in f:
            continue
        h.update(os.path.relpath(f, HERE).encode())
        with open(f, 'rb') as fh:
            h.update(fh.read())
    return h.hexdigest()


def write_pass(film, faults, not_run=0):
    """Pre-flight's stamp (rule 59): the code it ran on, how many faults it found, and how many of them are checks
    that did not run (left out, never set up, or a CHECKS_OFF entry without Sam's yes)."""
    os.makedirs(PASSES, exist_ok=True)
    with open(os.path.join(PASSES, f'{film}.json'), 'w') as fh:
        json.dump({'code': code_hash(), 'faults': faults, 'not_run': not_run}, fh)


def lock_fault(film, faults_named=False):
    """Rule 59: why an animatic or final render may not start (None: it may). A render that ran on past a failed
    pre-flight (Flying Whales, animatic 4) cannot happen again: the render itself checks."""
    path = os.path.join(PASSES, f'{film}.json')
    if not os.path.exists(path):
        return f'pre-flight has not been run on {film} in this session: python3 source/preflight.py {film} OUT_DIR'
    with open(path) as fh:
        stamp = json.load(fh)
    if stamp['code'] != code_hash():
        return f'the code has changed since pre-flight last ran on {film}: run it again'
    if stamp.get('not_run'):                    # rule 59 (audit, 12 Nov): naming it is not enough; a check that did
        return (f'pre-flight on {film}: {stamp["not_run"]} check(s) did not run (NOT RUN at the top of its list): '
                'set each up, or record Sam\'s yes in the film\'s CHECKS_OFF; --faults-named does not cover these')
    if stamp['faults'] and not faults_named:
        return (f'pre-flight found {stamp["faults"]} fault(s) on {film}: fix them, or, if every one has been named to '
                f'Sam, add --faults-named')
    return None


SKIP_YES = re.compile(r'^.*Checks skipped \(Sam\'s yes\):.*?["\u201c]([^"\u201d]{3,})["\u201d]', re.M)
SKIP_USED = 'Checks skipped, used:'


def _film_notes(main, film):
    """The film's notes file (its NOTES, notes/NAME.md with _ or -, or the archived one); None for a tool's demo."""
    root = os.path.dirname(HERE)
    for p in [getattr(main, 'NOTES', None)] + [os.path.join(root, 'notes', d, f'{n}.md') for d in ('', 'archive')
                                               for n in (film, film.replace('_', '-'))]:
        if p and os.path.exists(p):
            return p
    return None


def skip_fault(main, film, out, use=True):
    """Rule 59, audit item 3 (Sam, 12 Nov): a render with the checks skipped (lock=False) needs Sam's yes, and each
    yes covers ONE render. His yes is a line in the film's notes, 'Checks skipped (Sam's yes): DATE, note N: "his
    words"'; the render that uses it adds 'Checks skipped, used: DATE, FILE ("his words")', and that yes is spent.
    None: go (and, with use, the yes is now spent). A tool's own demo (no notes file) needs none."""
    path = _film_notes(main, film)
    if path is None:
        return None
    text = open(path).read()
    used = text.split(SKIP_USED)
    spent = [q for q in SKIP_YES.findall(text) if any(f'("{q}")' in u.split('\n', 1)[0] for u in used[1:])]
    free = [q for q in SKIP_YES.findall(text) if q not in spent]
    if not free:
        return (f'the checks are skipped (lock off) but {os.path.relpath(path, os.path.dirname(HERE))} has no unused '
                f'"Checks skipped (Sam\'s yes): DATE, note N: \"his words\"" line: a yes to skip the checks covers one '
                f'render (rule 59); ask Sam, or run pre-flight')
    if use:
        import datetime
        with open(path, 'a') as fh:
            fh.write(f'\n{SKIP_USED} {datetime.date.today():%d %b}, {os.path.basename(out)} ("{free[0]}")\n')
    return None


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
    if j.get('look'):                             # rule S7: once, on the clean drawing (the cache stays clean)
        import house_look
        pic = house_look.apply(pic).convert(pic.mode)   # same kind of image back (captions want RGBA)
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
           reuse=False, redo=(), preset='slow', span=None, stamp=None, lock=None, look=None):
    """picture(t) -> image without captions or title; overlay(img, t) -> img with them; shot_of(t) -> shot name;
    sound() -> the mixed soundtrack array; write_wav(path, mix). The cache ($FILM_CACHE or ~/.cache/filmcache) is
    only trusted when reuse=True: it cannot know what code changed, so name the shots that did (redo).
    span=(t0, t1) renders just that stretch, with its sound: a quick clip of one moment for notes on motion (Sam,
    18 Oct: stills can't show a problem in movement, and a whole animatic is wasted on one moment).
    stamp: the time and shot in the corner; None (the default) = on for every review copy (a span, or smaller than
    full size: rule 29), off for the full-size final.
    lock (rule 59): an animatic or final (no span) needs pre-flight's pass on the code as it is now; None = on for every
    film but clips; False for a tool's own demo render, or a film with an unused yes of Sam's to skip the checks (one
    render each: skip_fault).
    look (rule S7): the house look on every drawing (None = HOUSE_LOOK); False only for a tool's own demo, never a film. A film at 12 fps
    comes out at 24 fps, every drawing held 2 frames (FILE_FPS)."""
    look = HOUSE_LOOK if look is None else look
    main = sys.modules.get('__main__')
    film = os.path.splitext(os.path.basename(getattr(main, '__file__', '') or ''))[0]
    if lock is None:
        lock = not span
    if os.path.exists(out):                       # rule 66 (Sam, 3 Nov): never an old file standing in for a new render:
        os.remove(out)                            # gone before anything else, so a refused or stopped render leaves none
    if lock:
        why = lock_fault(film, '--faults-named' in sys.argv)
        if why:
            sys.exit('render REFUSED (rule 59): ' + why)
    elif not span:                                # the checks skipped: one render per yes of Sam's (audit item 3)
        why = skip_fault(main, film, out)
        if why:
            sys.exit('render REFUSED (rule 59): ' + why)
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
                shot_of=shot_of, stamp=stamp, look=look)
    hold = FILE_FPS // fps if look and fps == DRAW_FPS else 1          # rule S7: 12 drawings a second, each shown twice
    wav = out + '.wav'
    write_wav(wav, sound())
    print(f'picture cache: {cache}' + (f' (re-rendering {sorted(redo)}, reusing the rest)' if reuse else ''), flush=True)
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{size[0]}x{size[1]}', '-r', str(fps), '-i', '-', *(['-ss', f'{first / fps:.3f}'] if first else []), '-i', wav, '-map', '0:v', '-map', '1:a',
                          *(['-r', str(fps * hold)] if hold > 1 else []), '-c:v', 'libx264', '-crf', str(crf), '-preset', preset, '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    try:
        with Pool(os.cpu_count()) as pool:
            for k, fr in enumerate(pool.imap(_frame, [(i, reuse and i not in redo_set) for i in range(first, n)], chunksize=2)):
                p.stdin.write(fr)
                if k % 48 == 0:
                    print(f'frame {k}/{n - first}', flush=True)
        p.stdin.close()
        p.wait()
        if p.returncode:
            raise RuntimeError(f'ffmpeg failed ({p.returncode})')
    except BaseException:                         # stopped, killed by a signal's exception, or failed: delete the partial
        try:
            p.kill()
        except Exception:
            pass
        for f in (out, wav):
            if os.path.exists(f):
                os.remove(f)
        raise
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
