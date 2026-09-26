#!/usr/bin/env python3
"""Stamp a title card onto a finished video: bold Impact-style capitals (Anton, a free Impact twin) in
cranberry red, widened 20%, with a bold black outline, centred a third of the way down. It is on screen from the start, holds for three
seconds, then gently fades. The picture and sound are otherwise untouched.

Usage:
    python3 add_title.py IN.mp4 OUT.mp4 "Line one" ["Line two"] [--crf 26 | --bitrate 250k --audio 64k]
"""
import os
import subprocess
import sys
import tempfile

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'fonts', 'Anton-Regular.ttf')
CRANBERRY = (178, 24, 52)
FF = imageio_ffmpeg.get_ffmpeg_exe()
HOLD, FADE = 3.0, 1.0


def size_of(path):
    out = subprocess.run([FF, '-i', path], capture_output=True, text=True).stderr
    for tok in out.split():
        tok = tok.rstrip(',')
        if 'x' in tok and tok.replace('x', '').isdigit():
            w, h = tok.split('x')
            if int(w) > 100 and int(h) > 100:
                return int(w), int(h)
    raise SystemExit('could not read video size')


def _line(text, font, out, colour=(255, 255, 255)):
    """One line of script on its own transparent layer: bold black outline, then the white letters."""
    l, t, r, b = font.getbbox(text, stroke_width=out)
    im = Image.new('RGBA', (r - l + 2 * out, b - t + 2 * out), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pos = (out - l, out - t)
    d.text(pos, text, font=font, fill=(0, 0, 0, 255), stroke_width=out, stroke_fill=(0, 0, 0, 255))
    d.text(pos, text, font=font, fill=colour + (255,), stroke_width=max(1, int(font.size * 0.012)),
           stroke_fill=colour + (255,))
    return im


def title_card(w, h, lines, path, widen=1.2, colour=CRANBERRY):
    """A transparent PNG the size of the video with the title drawn on it, letters widened for legibility."""
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    main = int(min(w * 0.22, h * 0.16))  # long lines shrink to fit below
    layers = []
    for i, line in enumerate(lines):
        size = main if i == 0 else int(main * 0.62)
        while True:
            f = ImageFont.truetype(FONT, size)
            lay = _line(line, f, max(3, int(size * 0.075)), colour)
            lay = lay.resize((int(lay.width * widen), lay.height), Image.LANCZOS)  # wider, easier to read
            if lay.width <= w * 0.92:
                break
            size = int(size * 0.93)
        layers.append(lay)
    total = sum(int(l.height * 0.82) for l in layers)
    y = h / 3 - total / 2
    for lay in layers:
        im.alpha_composite(lay, (int((w - lay.width) / 2), int(y - lay.height * 0.09)))
        y += lay.height * 0.82
    im.save(path)


def main():
    args = sys.argv[1:]
    bitrate = audio = None
    crf = '26'
    if '--crf' in args:
        i = args.index('--crf')
        crf = args[i + 1]
        del args[i:i + 2]
    if '--bitrate' in args:
        i = args.index('--bitrate')
        bitrate = args[i + 1]
        del args[i:i + 2]
    if '--audio' in args:
        i = args.index('--audio')
        audio = args[i + 1]
        del args[i:i + 2]
    src, dst, lines = args[0], args[1], [l.upper() for l in args[2:]]
    w, h = size_of(src)
    with tempfile.TemporaryDirectory() as tmp:
        card = os.path.join(tmp, 'title.png')
        title_card(w, h, lines, card)
        vf = (f'[1:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st={HOLD}:d={FADE}:alpha=1[t];'
              f'[0:v][t]overlay=0:0:eof_action=pass:format=auto,format=yuv420p[v]')
        base = [FF, '-y', '-loglevel', 'error', '-i', src, '-loop', '1', '-t', str(HOLD + FADE), '-i', card,
                '-filter_complex', vf, '-map', '[v]', '-map', '0:a?']
        if bitrate:  # two passes to hit a target size (Discord copies)
            log = os.path.join(tmp, 'pass')
            subprocess.run(base + ['-c:v', 'libx264', '-b:v', bitrate, '-pass', '1', '-passlogfile', log, '-an',
                                   '-f', 'mp4', os.devnull], check=True)
            subprocess.run(base + ['-c:v', 'libx264', '-b:v', bitrate, '-pass', '2', '-passlogfile', log,
                                   '-c:a', 'aac', '-b:a', audio or '64k', '-movflags', '+faststart', dst], check=True)
        else:
            subprocess.run(base + ['-c:v', 'libx264', '-crf', crf, '-preset', 'slow', '-c:a', 'copy',
                                   '-movflags', '+faststart', dst], check=True)
    print(f'{dst}: {os.path.getsize(dst) / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
