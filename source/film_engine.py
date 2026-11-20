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
import subprocess
import sys

import numpy as np
from PIL import Image

_JOB = {}
HERE = os.path.dirname(os.path.abspath(__file__))
PASSES = os.path.join(os.path.dirname(HERE), 'review', 'preflight-pass')   # rule 59: pre-flight's pass stamps


DRAW_FPS, FILE_FPS = 12, 24     # rule S7: drawings a second, frames a second in the file
HOUSE_LOOK = True                # rule S7 on for every film (Sam, 12 Nov: Y); False only to look at a film without it


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


def write_pass(film, faults, pictures=False):
    """Pre-flight's stamp (rule 59): the code it ran on, how many faults it found, and whether the picture checks
    (every frame drawn with the probes) have passed on this code: pre-flight --pictures, or an animatic render that ran
    them while it drew."""
    os.makedirs(PASSES, exist_ok=True)
    with open(os.path.join(PASSES, f'{film}.json'), 'w') as fh:
        json.dump({'code': code_hash(), 'faults': faults, 'pictures': bool(pictures)}, fh)


def read_pass(film):
    path = os.path.join(PASSES, f'{film}.json')
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        return json.load(fh)


def lock_fault(film, faults_named=False, final=False):
    """Rule 59: why an animatic or final render may not start (None: it may). A render that ran on past a failed
    pre-flight (Flying Whales, animatic 4) cannot happen again: the render itself checks. An animatic may start on
    pre-flight's quick pass (it runs the picture checks itself while it draws); a final needs the picture checks
    passed on this exact code (an animatic, or pre-flight --pictures)."""
    stamp = read_pass(film)
    if stamp is None:
        return f'pre-flight has not been run on {film} in this session: python3 source/preflight.py {film} OUT_DIR'
    if stamp['code'] != code_hash():
        return f'the code has changed since pre-flight last ran on {film}: run it again'
    if stamp['faults'] and not faults_named:
        return (f'pre-flight found {stamp["faults"]} fault(s) on {film}: fix them, or, if every one has been named to '
                f'Sam, add --faults-named')
    if final and not stamp.get('pictures'):
        return (f'the picture checks have not passed on this code: render the animatic (--small) first, which runs '
                f'them, or run pre-flight with --pictures')
    return None


_CHECK = {}                                       # the render's picture checks (rule 59, 13 Nov): the film module


def _checked(t):
    """The picture, drawn with pre-flight's probes; (picture, record). A drawing the figure guard stops is a black
    frame here: the fault is in the record, and the video is refused."""
    import preflight
    pic, rec = preflight.probe(t, _JOB['picture'])
    if pic is None:
        from body import canvas
        pic = canvas((0, 0, 0))
    return pic, rec


def _code_print():
    """A fingerprint of every loaded module in source/ (the film, its kit, this engine): the cache's 'what changed'."""
    import hashlib
    here = os.path.dirname(os.path.abspath(__file__))
    h = hashlib.sha1()
    for f in sorted({os.path.abspath(m.__file__) for m in list(sys.modules.values())
                     if getattr(m, '__file__', None) and os.path.abspath(m.__file__).startswith(here)}):
        if f.endswith('.py') and os.path.exists(f):
            h.update(f.encode())
            with open(f, 'rb') as fh:
                h.update(fh.read())
    return h.hexdigest()


def _frame(args):
    i, reuse = args
    j = _JOB
    t = i / j['fps']
    j['set_ss'](j['ss'])
    path = os.path.join(j['cache'], f'{i:04d}.png')
    rec = None
    recp = path[:-4] + '.rec.pkl'
    bodyp = path[:-4] + '.body.json'              # the body check's faults for this drawing (humancheck, Change 1)
    reuse = reuse and os.path.exists(bodyp)       # a frame cached before the body check is drawn again
    import humancheck as HC
    body = None
    if reuse and os.path.exists(bodyp):
        try:
            with open(bodyp) as fh:
                body = [tuple(f) for f in json.load(fh)]
        except (OSError, ValueError):
            reuse = False
    if j.get('check') and reuse and os.path.exists(path) and os.path.exists(recp):
        import pickle                             # chat 30 (Sam's Y): an unchanged frame and its check record, reused
        pic = Image.open(path)
        pic.load()
        with open(recp, 'rb') as fh:
            rec = pickle.load(fh)
    elif j.get('check'):                          # rule 59 (13 Nov): the picture checks run on this one drawing
        HC.frame_begin()
        pic, rec = _checked(t)
        body = HC.frame_end(t)
        pic.save(path, compress_level=1)
        try:
            import pickle
            with open(recp, 'wb') as fh:
                pickle.dump(rec, fh)
        except Exception:                         # a record that won't save: this frame is simply drawn again next time
            if os.path.exists(recp):
                os.remove(recp)
    elif reuse and os.path.exists(path):
        pic = Image.open(path)
        pic.load()
    else:
        HC.frame_begin()
        pic = j['picture'](t)
        body = HC.frame_end(t)
        pic.save(path, compress_level=1)
    if body is None:                              # (drawn above, or its record lost): never a frame unchecked
        HC.frame_begin()
        j['picture'](t)
        body = HC.frame_end(t)
    with open(bodyp, 'w') as fh:
        json.dump(body, fh)
    if j.get('look'):                             # rule S7: once, on the clean drawing (the cache stays clean)
        import house_look
        pic = house_look.apply(pic).convert(pic.mode)   # same kind of image back (captions want RGBA)
    im = j['overlay'](pic, t).convert('RGB').resize(j['size'], Image.LANCZOS)
    if j.get('stamp'):
        stamp(im, t, j['shot_of'](t))
    return np.asarray(im).tobytes(), rec, body


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
    film but clips; False only for a tool's own demo render, never a film.
    look (rule S7): the house look on every drawing (None = HOUSE_LOOK); False only for a tool's own demo, never a film. A film at 12 fps
    comes out at 24 fps, every drawing held 2 frames (FILE_FPS)."""
    look = HOUSE_LOOK if look is None else look
    main = sys.modules.get('__main__')
    film = os.path.splitext(os.path.basename(getattr(main, '__file__', '') or ''))[0]
    if lock is None:
        lock = not span
    held = os.path.splitext(out)[0] + '.held.mp4'  # chat 30 (Sam's Y, 15 Nov): a stopped render's video, kept aside
    for f in (out, held):                         # rule 66 (Sam, 3 Nov): never an old file standing in for a new render:
        if os.path.exists(f):                     # gone before anything else, so a refused or stopped render leaves none
            os.remove(f)
    check = False
    named = '--faults-named' in sys.argv
    full = not span and not reuse and size[0] >= 1080
    done = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'animations', f'{film}.mp4')
    if full and film and os.path.exists(done) and '--full-ok' not in sys.argv:
        # rule 47 (Sam, 13 Nov: Blessed's one-arm fix ran a 35-minute full redraw when a splice would do)
        sys.exit(f'render REFUSED (rule 47): {film} already has a final ({done}). Redraw only the seconds that changed '
                 f'(final OUT --span T0 T1 --nostamp) and splice them in; a full redraw needs Sam\'s Y (--full-ok)')
    if lock:
        small = ss == 1 and size[0] < 1080
        why = lock_fault(film, named, final=not small)
        if why:
            sys.exit('render REFUSED (rule 59): ' + why)
        check = not (read_pass(film) or {}).get('pictures')   # the animatic runs the picture checks as it draws
        if check:
            import preflight
            preflight.install_probes(main)
            print('picture checks: on, while drawing (rule 59); the video is refused if they find a fault', flush=True)
    import imageio_ffmpeg
    from multiprocessing import Pool
    cache = os.path.join(os.environ.get('FILM_CACHE', os.path.expanduser('~/.cache/filmcache')),
                         f'{name}-{size[0]}x{size[1]}-ss{ss}')
    os.makedirs(cache, exist_ok=True)
    n = int(round(dur * fps))
    first = 0
    if span:
        first, n = int(round(span[0] * fps)), min(n, int(round(span[1] * fps)))
    # chat 30 (Sam's Y, 15 Nov: a re-render after a stop redrew all 427 unchanged frames, 30 min): the cache keeps the
    # code's fingerprint; frames (and their check records) are reused when no code has changed since, or, with
    # --redo SHOT[,SHOT], for every shot not named. Code changed and no shots named: every frame is drawn.
    if '--redo' in sys.argv:
        redo = tuple(redo) + tuple(sys.argv[sys.argv.index('--redo') + 1].split(','))
    code, keyf = _code_print(), os.path.join(cache, 'code.txt')
    same = os.path.exists(keyf) and open(keyf).read() == code
    if same or '--redo' in sys.argv:
        reuse = True
        print('picture cache: ' + ('no code changed since it was drawn: unchanged frames reused' if same else
                                   f'reusing every shot but {list(redo)} (named with --redo)'), flush=True)
    elif check or reuse:
        reuse = False
        print('picture cache: code changed since it was drawn: every frame drawn (--redo SHOT reuses the rest)',
              flush=True)
    if os.path.exists(keyf) and not same:
        os.remove(keyf)                           # the cache is mixed until a whole pass ends
    redo_set = {i for i in range(n) if shot_of(i / fps) in redo}
    if stamp is None:
        stamp = bool(span) or size[0] < 1080 and size[1] < 1920
    _JOB.update(fps=fps, ss=ss, size=size, cache=cache, picture=picture, overlay=overlay, set_ss=set_ss,
                shot_of=shot_of, stamp=stamp, look=look, check=check)
    recs = []
    import humancheck as HC
    hc = HC.Writer(os.path.basename(out))         # the body check (Change 1): every person, every drawing
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
            for k, (fr, rec, body) in enumerate(pool.imap(_frame, [(i, reuse and i not in redo_set) for i in range(first, n)], chunksize=2)):
                p.stdin.write(fr)
                hc.frame((first + k) / fps, body)
                if rec is not None:
                    recs.append(rec)
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
    if not span:
        with open(keyf, 'w') as fh:               # every frame in the cache now matches this code
            fh.write(code)
    if check:                                     # the drawing pass's own checks (pre-flight's picture checks)
        import preflight
        import report
        found, _, _ = preflight.picture_faults(main, film, recs, fps)
        found = report.group(found, getattr(main, 'SHOTS', []))
        report.summarise(f'picture checks ({film})', found, os.path.join(os.path.dirname(os.path.abspath(out)),
                                                                          f'{film}-picture-checks.txt'))
        if found and not named:                   # chat 30 (Sam's Y, 15 Nov: a stopped 31-minute render was thrown
            os.replace(out, held)                 # away): kept aside, never under OUT's name, so nothing sends it unnamed
            sys.exit(f'render STOPPED (rule 59): the picture checks found {len(found)} fault(s), listed above. The video '
                     f'is held as {held} (not a pass). Fix them and render again, or name every one to Sam, then rename '
                     f'the held file to {os.path.basename(out)} and run finish.py with --faults-named (no second render). '
                     f'The final still needs a render whose checks are clean or named.')
        stamp0 = read_pass(film) or {}
        write_pass(film, stamp0.get('faults', 0) + len(found), pictures=True)   # the final may now go ahead
    hc.finish(out, named='--body-named' in sys.argv)   # an unnamed body fault: the video is held aside
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
