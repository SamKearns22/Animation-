#!/usr/bin/env python3
"""Halo No-No, the retry cut (Sam, 30 Oct: the first post stalled at 214 views, 10% to the end).

An edit of the approved film (`halo_no_no.py`, untouched): its pictures are re-timed through a list of kept pieces.
  - starts the second the first Roadster enters (old 4.5 s), the theme on the same beat (0:32 of the song);
  - the radio line starts over the space shot (1.5 s in) and the cut to the cabin comes partway through it;
  - the dead gaps trimmed at the cuts only (never inside a shot: a jump);
  - "Halo Ringworld" alone (no "Russia - Ukraine War"), up at 0 s and gone by 1.2 s.

    python3 source/halo_no_no_retry.py check                  the edit's checks (subtitles, voices over the music)
    python3 source/halo_no_no_retry.py sheet OUT.jpg          stills sheet
    python3 source/halo_no_no_retry.py final OUT.mp4 [--small] [--span T0 T1] [--nostamp]
Then finish.py with the Hook Text and --signoff-speed 1.25.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B                      # noqa: E402
import film_engine as E                  # noqa: E402
import filmkit                           # noqa: E402
import halo_no_no as M                   # noqa: E402  the approved film: every picture comes from it
import peepee as PP                      # noqa: E402

NAME = 'halo-no-no-retry'
FPS, SR = M.FPS, M.SR
# (old start, old end) of each kept piece, in order; the new film plays them back to back
PIECES = [(4.5, 8.5),      # s1: the armada from its first car (the radio line starts over it)
          (11.4, 16.4),    # s2: the cabin, joined partway through the radio line ("what you're doing...")
          (16.4, 21.9),    # s3: Musk close (0.2 s after his line ends)
          (22.45, 31.5),   # s4: the cabin from just before the discharge
          (31.5, 34.2),    # s5: Musk close
          (35.3, 42.3)]    # s6: the ring, starting nearer its first line
MUSIC_UP = 1.40           # the theme 40% louder (Sam, 30 Oct)
SPEECH_FROM = 7.4          # before the cabin, the voices run this far ahead of the picture (old 8.9 s -> 1.5 s)


def _starts():
    out, at = [], 0.0
    for a, b in PIECES:
        out.append(at)
        at += b - a
    return out, at


STARTS, DUR = _starts()
BLACK_AT = DUR


def picture_time(t):
    """The approved film's time shown at new time t."""
    for (a, b), s in zip(PIECES, STARTS):
        if t < s + (b - a):
            return a + (t - s)
    return PIECES[-1][1]


def speech_time(t):
    """The approved film's time heard at new time t (the voices and subtitles)."""
    return t + SPEECH_FROM if t < STARTS[1] else picture_time(t)


def new_time(old):
    """Where a moment of the approved film's speech lands in the new film."""
    if old < PIECES[1][0]:
        return old - SPEECH_FROM
    for (a, b), s in zip(PIECES, STARTS):
        if a <= old < b:
            return s + old - a
    raise ValueError(f'{old} s falls in a cut')


SHOTS = [(M.shot_of(a), s, s + b - a) for (a, b), s in zip(PIECES, STARTS)]
LINES = [dict(ln, start=new_time(ln['start']), end=new_time(ln['end'] - 1e-6)) for ln in M.LINES]


def shot_of(t):
    return next((n for n, a, b in SHOTS if a <= t < b), SHOTS[-1][0])


def picture(t):
    return M.picture(picture_time(t))


def place_title(img, t):
    """"Halo Ringworld" alone (Sam, 30 Oct: no "Russia - Ukraine War"), lower third, from the first frame, gone by
    1.2 s."""
    a = 1.0 if t < 0.9 else max(0.0, (1.2 - t) / 0.3)
    if a <= 0:
        return
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    B.text(lay, B.Cam(1.0, 540, 960), 540, 1440, M.CAPTION_1[0], 64, (255, 255, 255), font=M.HC.SANS, anchor='ma',
           stroke=3, stroke_fill=(0, 0, 0))
    if a < 1:
        lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay)


def caption_at(t):
    return M.caption_at(speech_time(t))


def overlay(img, t):
    if t < BLACK_AT:
        place_title(img, t)
        c = caption_at(t)
        if c:
            PP.caption(img, c)
    return img


def frame_image(t):
    return overlay(picture(t), t)


# ------------------------------------------------------------------------------------------------ sound
def music_gain(n):
    """As the approved film: loud in space, 11 dB down in the cabin, 0.3 s eases; dips under every line (11 dB in
    space, 4 dB in the cabin)."""
    g = np.zeros(n)
    for name, a, b in SHOTS:
        g[int(a * SR):int(b * SR)] = 1.0 if name in M.SPACE_SHOTS else 10 ** (-11 / 20)
    g[int(DUR * SR):] = g[int(DUR * SR) - 1]
    k = np.hanning(int(0.3 * SR))
    g = np.convolve(g, k / k.sum(), 'same')
    for ln in LINES:
        space = shot_of(ln['start']) in M.SPACE_SHOTS
        duck = np.ones(n)
        duck[int((ln['start'] - 0.2) * SR):int((ln['end'] + 0.2) * SR)] = 10 ** ((-11 if space else -4) / 20)
        g *= np.convolve(duck, k / k.sum(), 'same')
    return g


def soundtrack(stems=False):
    from burnham_film import load
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)
    for ln in LINES:
        if ln['_voice'] is not None:
            v = M.radio(ln['_voice']) if ln.get('radio') else ln['_voice']
            s = int(ln['start'] * SR)
            seg = v[:max(0, n - s)]
            voice[s:s + len(seg)] += seg
    theme = load(M.THEME)[int((M.THEME_FROM + PIECES[0][0]) * SR):]     # the cars arrive on the same beat (0:32)
    m = np.zeros(n)
    m[:min(n, len(theme))] = theme[:n]
    m *= 10 ** ((M.MA.LINE_LUFS - 3 - M.MA.lufs(m[:int(DUR * SR)])) / 20)
    m *= MUSIC_UP
    rest += m * music_gain(n)
    end = int(BLACK_AT * SR)
    f = int(0.4 * SR)
    rest[end - f:end] *= np.linspace(1, 0, f)
    mix, g = M.MA.master(voice + rest, end)
    voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


def checks():
    """The edit's own checks (the drawing is the approved film's, checked by its pre-flight): no line or subtitle cut
    by an edit, the subtitles readable, the voices 6 dB over the music."""
    faults = []
    for ln in M.LINES:
        for a, b in zip(PIECES, PIECES[1:]):
            if PIECES[0] != a and ln['start'] < b[0] and ln['end'] > a[1]:
                faults.append(f"line {ln['n']} is cut by the edit at {a[1]}-{b[0]} s")
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    _, voice, rest = soundtrack(stems=True)
    allw = [(ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches']]
    faults += filmkit.voice_balance(voice, rest, SR, allw)
    print('\n'.join(['FAULT: ' + f for f in faults]) or 'retry checks: clean')
    print('shots:', ', '.join(f'{n} {a:.2f}-{b:.2f}' for n, a, b in SHOTS), f'| length {DUR:.2f} s')


def sheet(out, times):
    tiles = []
    f = ImageFont.truetype(M.HC.SANS, 18)
    for t in times:
        im = frame_image(t).convert('RGB').resize((360, 640), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 150, 30), fill=(0, 0, 0))
        d.text((6, 4), f'{shot_of(t)}  {t:.1f}s', fill=(255, 255, 255), font=f)
        tiles.append(im)
    cols = 6
    rows = (len(tiles) + cols - 1) // cols
    s = Image.new('RGB', (cols * 364 + 4, rows * 644 + 4), (255, 255, 255))
    for i, im in enumerate(tiles):
        s.paste(im, (4 + (i % cols) * 364, 4 + (i // cols) * 644))
    s.save(out, quality=86)
    print('wrote', out)


def main():
    a = sys.argv[1:]
    B.SS = 1
    if a[0] == 'check':
        checks()
    elif a[0] == 'sheet':
        sheet(a[1], [float(x) for x in a[2:]] or [0.3, 1.0, 2.0, 3.5, 4.5, 6.5, 10.0, 15.0, 16.5, 20.0, 22.5, 24.5,
                                                   27.0, 30.0, 31.5, 33.0])
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=M.MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)


if __name__ == '__main__':
    main()
