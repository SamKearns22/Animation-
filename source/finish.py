#!/usr/bin/env python3
"""The finishing step for every TikTok film (Sam, 15 Oct), so nothing is forgotten: from the clean, untitled render,
burn in the captions (rule 62), deliver at 1.1x with voices at their normal pitch (rule 70), add the Hook Text (rule
75) and the CranbriJoos sign-off (rule 52) with the film's follow line (story/follow-lines.md), in that order.

    python3 finish.py CLEAN.mp4 OUT.mp4 --film NAME
    python3 finish.py CLEAN.mp4 OUT.mp4 --film NAME ["Hook Text"] [--y 1180] [--x 540] [--w 400] [--until 3.6] [--centre]
    either way: [--signoff-speed 1.0]

--film NAME reads source/NAME.py (refused without it, or without the film's captions):
  * its caption_at(t): the captions, read on every frame and drawn in the kit's style (subtitles.draw: Montserrat
    Black, white, black outline and shadow; a film's own draw_subtitle only if it has one), so a caption wording or
    timing note costs seconds, not a render. The film's whole renders leave them out. A film with no caption_at is
    refused (rule 62: captions on every animatic and final; tool job, 11 Nov: no more SUBTITLES_AT_FINISH opt-in).
    Films finished before 11 Nov drew their captions in the picture: they are never finished again.
  * then the whole film is sped to SPEED (1.1x, subtitles.SPEED) with the voices kept at their pitch, so the Hook
    Text's 0.5 s pop and the sign-off's 1.6 s, added after, stay as they are on the delivered file;
  * its HOOK = (text, {'y':, 'x':, 'w':, 'until':, 'centre':}): the Hook Text and where it sits ('until' in seconds of
    the delivered file); the Hook Text check (hookcheck.py, rule 10) runs first and stops on a fault unless that line
    has its own written answer in the notes' "## Exceptions" (named-lines, Sam's Y 23 Nov: --faults-named no longer
    passes a list). Hook Text words or flags typed on the command line override HOOK (and say so).
  * the readable check (could-not-test 3, 23 Nov): every text piece the places painter drew (name cards, signs,
    notices) and every KEEP_CLEAR box, as the render drew them (CLEAN.mp4.readable.json, written by the render),
    against the captions and the Hook Text: 5% or more of one covered is a fault (each line answered in the notes, as above).
  * the kit tests (Sam's pick 1, 25 Nov): every kit test must have a pass on the current files (source/kitstamps.py);
    the stale ones run first, and any still without a pass refuses (Override still applies).
  * a check pre-flight could not run (clipcheck's COULD NOT TEST) refuses even with --faults-named: only that check's
    row in the notes' "## Exceptions" with Sam's Y lets it by (film_engine.untested_fault).

Keep CLEAN.mp4 (in source/data/FILM/, not on GitHub) so the Hook Text and captions can change without a re-render.
A --small clean render (540 x 960) works too: the captions are drawn at full size and scaled to fit.
"""
import importlib
import os
import re
import subprocess
import sys
import tempfile

import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
FF = imageio_ffmpeg.get_ffmpeg_exe()
HOOK_FLAGS = ('--y', '--x', '--w', '--until', '--tilt')


def has_sound(path):
    return 'Audio:' in subprocess.run([FF, '-i', path], capture_output=True, text=True).stderr


def video_info(path):
    """(width, height, fps) of a video."""
    err = subprocess.run([FF, '-i', path], capture_output=True, text=True).stderr
    line = next(ln for ln in err.splitlines() if 'Video:' in ln)
    w, h = map(int, re.search(r', (\d{2,5})x(\d{2,5})', line).groups())
    fps = float(re.search(r'([\d.]+) fps', line).group(1))
    return w, h, fps


def load_film(name):
    sys.path.insert(0, HERE)
    name = name.replace('-', '_')                 # either spelling of the film's name (late-faults change 1)
    print(f'reading the film ({name}.py) ...', flush=True)
    return importlib.import_module(name)


def film_hook(film):
    """The film's HOOK as finish.py's own arguments: (text, [flags])."""
    if not hasattr(film, 'HOOK'):
        return '', []
    text, opts = film.HOOK
    flags = []
    for k in ('y', 'x', 'w', 'until', 'tilt'):
        if opts.get(k) is not None:
            flags += [f'--{k}', str(opts[k])]
    if opts.get('centre'):
        flags.append('--centre')
    return text, flags


def subtitle_list(film, n, fps):
    """[(first frame, last frame + 1, text)] from the film's caption_at, frame by frame."""
    end = getattr(film, 'BLACK_AT', getattr(film, 'DUR', n / fps))
    out = []
    for i in range(n):
        t = i / fps
        c = film.caption_at(t) if t < end else None
        if out and out[-1][2] == c and out[-1][1] == i:
            out[-1][1] = i + 1
        elif c:
            out.append([i, i + 1, c])
    return out


def burn_subtitles(film, src, dst):
    """Every frame through Python: the film's subtitle drawn on top, exactly as its render would have."""
    import numpy as np
    from PIL import Image
    w, h, fps = video_info(src)
    n = int(round(_duration(src) * fps))
    subs = subtitle_list(film, n, fps)
    print(f'subtitles: {len(subs)} burned in (proofread):', flush=True)
    for a, b, c in subs:
        print(f'  {a / fps:6.2f}-{b / fps:6.2f} s  {c}')
    import subtitles as SUB
    B = sys.modules.get('burnham')
    draw = getattr(film, 'draw_subtitle', None) or SUB.draw      # rule 62: the kit's style unless the film has its own
    layers = {}

    def layer(c):
        if c not in layers:
            old = B.SS if B else None
            if B:
                B.SS = 1
            lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
            draw(lay, c)
            if B:
                B.SS = old
            if (w, h) != (1080, 1920):
                lay = lay.resize((w, h), Image.LANCZOS)
            layers[c] = lay
        return layers[c]

    at = {}
    for a, b, c in subs:
        for i in range(a, b):
            at[i] = c
    dec = subprocess.Popen([FF, '-loglevel', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}',
                            '-r', f'{fps:g}', '-i', '-', '-i', src, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264',
                            '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
                            '-movflags', '+faststart', dst], stdin=subprocess.PIPE)
    size, i = w * h * 3, 0
    while True:
        raw = dec.stdout.read(size)
        if len(raw) < size:
            break
        if i in at:
            im = Image.frombuffer('RGB', (w, h), raw, 'raw', 'RGB', 0, 1).convert('RGBA')
            im.alpha_composite(layer(at[i]))
            raw = np.asarray(im.convert('RGB')).tobytes()
        enc.stdin.write(raw)
        i += 1
    enc.stdin.close()
    dec.wait()
    if enc.wait() or dec.returncode:
        sys.exit('finish: burning the subtitles failed')


def speed_up(src, dst, speed):
    """Rule 70: the picture and the sound played `speed` times faster, the voices at their own pitch (atempo keeps
    pitch); the frame rate stays the film's own."""
    w, h, fps = video_info(src)
    subprocess.run([FF, '-y', '-loglevel', 'error', '-i', src, '-filter_complex',
                    f'[0:v]setpts=PTS/{speed}[v];[0:a]atempo={speed}[a]', '-map', '[v]', '-map', '[a]', '-r', f'{fps:g}',
                    '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                    '-b:a', '192k', '-movflags', '+faststart', dst], check=True)


def _duration(path):
    err = subprocess.run([FF, '-i', path], capture_output=True, text=True).stderr
    hh, mm, ss = err.split('Duration: ')[1].split(',')[0].split(':')
    return int(hh) * 3600 + int(mm) * 60 + float(ss)


def take(rest, flag, n=1):
    """Remove `flag` (and its n values) from rest; return the values (or None if absent)."""
    if flag not in rest:
        return None
    i = rest.index(flag)
    vals = rest[i + 1:i + 1 + n]
    del rest[i:i + 1 + n]
    return vals

def _left(film, name, lines, named=False):
    """named-lines change 2 (Sam's Y, 23 Nov; rule 59): the lines with no written answer of their own in the film's
    notes (blind ones always). --faults-named no longer passes a list; it is only reported."""
    if not lines:
        return []
    import preflight
    import waivers
    p = preflight.notes_path(film, name)
    done, left = waivers.split(lines, open(p).read() if os.path.exists(p) else '', film)
    if done:
        print(f'{len(done)} line(s) answered in the notes')
    for x in waivers.todo_rows(left):
        print('row to fill: ' + x)
    if left and named:
        print('--faults-named given: it no longer passes a list (rule 59, Sam 23 Nov)')
    return left



def main():
    src, dst = sys.argv[1], sys.argv[2]
    rest, extra = sys.argv[3:], []
    for flag in HOOK_FLAGS:                       # passed on to hook_text.py (e.g. a lower line, clear of a face)
        v = take(rest, flag)
        if v:
            extra += [flag, v[0]]
    v = take(rest, '--signoff-speed')             # the default is 1.25 (1.6 s, Sam's rule, 2 Nov); 1.0 = the old 2 s
    if v:
        os.environ['SIGNOFF_SPEED'] = v[0]
    if take(rest, '--centre', 0) is not None:
        extra.append('--centre')
    named = take(rest, '--faults-named', 0) is not None
    name = take(rest, '--film')
    if not name:
        sys.exit('finish REFUSED (rule 62): give --film NAME: the captions come from the film\'s caption_at')
    import propose                                # lesson 7 step 3 (fail closed): no animatic while a change slipped
    slipped = propose.open_letthroughs()          # the proposal route unsettled; no --faults-named way past
    if slipped:
        __import__('override').refuse('finish REFUSED (the proposal route, fail closed): ' + ' | '.join(x[:140] for x in slipped) +
                 ' ; settle each: python3 source/propose.py settle CHAT8 "routed: NAME" | "false block: why"')
    if not os.environ.get('KITTESTS_RUNNING'):    # kit-tests-when change 2 (Sam's pick 1, 25 Nov): no animatic or
        import kitstamps                          # final on files a kit test has not passed on; the stale ones run first
        why = kitstamps.finish_gate()
        if why:
            __import__('override').refuse('finish REFUSED (kit tests): ' + why)
    film = load_film(name[0])
    if not hasattr(film, 'caption_at'):
        sys.exit(f'finish REFUSED (rule 62): {name[0]}.py has no caption_at(t), so the film would go out with no '
                 'captions (start from the template: subtitles.caption_at)')
    import subtitles as SUB
    hook = ' '.join(rest)
    ftext, fflags = film_hook(film)
    if hook and hook != ftext:
        print(f'Hook Text from the command line ("{hook}"), not the film\'s HOOK ("{ftext}")')
    if extra and extra != fflags:
        print(f'Hook Text position from the command line {extra}, not the film\'s HOOK {fflags}')
    hook, extra = hook or ftext, extra or fflags
    if hook:                                       # rule 75: the Hook Text check on every animatic and final
        import hookcheck
        faults = hookcheck.faults(film) if (hook, extra) == (ftext, fflags) else []
        for f in faults:
            print('HOOK TEXT FAULT: ' + f)
        faults = _left(film, name[0], faults, named)          # named-lines: each line its own written answer
        if faults:
            __import__('override').refuse('finish REFUSED (rule 10): fix the Hook Text position in HOOK, or answer each line in the notes\' '
                     '"## Exceptions" (rows to fill above; --faults-named no longer passes a list)')
        if not faults:
            print('Hook Text check: clear of everything listed')
    import cover                                  # could-not-test (3, Sam's pick 1, 22 Nov): what the film lists (name
    side = src + cover.SIDE                       # cards, signs, KEEP_CLEAR) measured against the captions and the Hook
    if os.path.exists(side):                      # Text on the frames the render actually drew (its boxes, kept beside
        import json                               # the clean video), never re-drawn from the code
        with open(side) as fh:
            rfaults = cover.readable_faults(film, json.load(fh), film.HOOK if hook and (hook, extra) == (ftext, fflags)
                                            and hasattr(film, 'HOOK') else None)
    else:
        rfaults = [f'readable check: COULD NOT TEST: {os.path.basename(src)} has no record of what it drew '
                   f'({os.path.basename(side)}): render the clean video again with the render tool']
    for f in rfaults:
        print('READABLE FAULT: ' + f)
    rfaults = _left(film, name[0], rfaults, named)            # named-lines: each line its own written answer
    if rfaults:
        __import__('override').refuse('finish REFUSED (could-not-test 3): a listed thing is under a caption or the Hook Text: fix it, or '
                 'answer each line in the notes\' "## Exceptions" (--faults-named no longer passes a list)')
    if not rfaults:
        print('readable check: every listed thing clear of the captions and Hook Text, on the frames drawn')
    import film_engine                            # could-not-test (1): a check that could not test stops here even with
    why = film_engine.untested_fault(name[0])     # --faults-named; only its Exceptions row with Sam's Y lets it by
    if why:
        __import__('override').refuse('finish REFUSED (could-not-test): ' + why)
    import follow_line                            # rule 52: the film's follow line on the sign-off (story/follow-lines.md)
    follow = follow_line.line_for(name[0])
    with tempfile.TemporaryDirectory() as tmp:
        step = src
        if not has_sound(step):                    # a silent film gets a silent track, so the sign-off's slurp can join on
            quiet = os.path.join(tmp, 'quiet.mp4')
            subprocess.run([FF, '-y', '-loglevel', 'error', '-i', step, '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono',
                            '-shortest', '-c:v', 'copy', '-c:a', 'aac', quiet], check=True)
            step = quiet
        subbed = os.path.join(tmp, 'subbed.mp4')   # rule 62: captions burned in here, never in the picture render
        burn_subtitles(film, step, subbed)
        step = subbed
        fast = os.path.join(tmp, 'fast.mp4')       # rule 70: 1.1x, voices at their pitch; Hook Text and sign-off after,
        speed_up(step, fast, SUB.SPEED)            # so the 0.5 s pop and the 1.6 s sign-off keep their own timing
        step = fast
        print(f'delivered at {SUB.SPEED:g}x (rule 70)')
        if hook:
            hooked = os.path.join(tmp, 'hooked.mp4')
            subprocess.run([sys.executable, os.path.join(HERE, 'hook_text.py'), step, hooked, hook] + extra, check=True)
            step = hooked
        subprocess.run([sys.executable, os.path.join(HERE, 'signoff.py'), 'add', step, dst, follow], check=True)
    sys.path.insert(0, HERE)
    import humancheck                              # the finished video carries its clean render's body check record
    humancheck.copy_record(src, dst)               # (faults, names, critique): the send gate reads it (Change 1)
    if 'animatic' in os.path.basename(dst):        # rule P16 (Sam, 15 Nov): the latest animatic and its clean render are
        import shutil                              # kept on GitHub, so a fix to a few seconds is a splice, not a redraw
        keep = os.path.join(os.path.dirname(HERE), 'animations', 'drafts')
        os.makedirs(keep, exist_ok=True)
        slug = str(name[0]).replace('_', '-')
        for f in os.listdir(keep):
            if f.startswith(slug + '-'):
                os.remove(os.path.join(keep, f))   # only the latest is kept
        shutil.copy(dst, os.path.join(keep, f'{slug}-animatic.mp4'))
        shutil.copy(src, os.path.join(keep, f'{slug}-clean.mp4'))
        if os.path.exists(src + cover.SIDE):       # what it drew, so a later finish from the kept copy can check it
            shutil.copy(src + cover.SIDE, os.path.join(keep, f'{slug}-clean.mp4' + cover.SIDE))
        print(f'kept on GitHub: animations/drafts/{slug}-animatic.mp4 and -clean.mp4 (commit and push them)')


if __name__ == '__main__':
    main()
