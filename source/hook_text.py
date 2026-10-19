#!/usr/bin/env python3
"""Stamp the Hook Text (the opening line that introduces the joke) onto a finished TikTok video, in TikTok's own caption look (Sam, 15 Oct: readability
first, like the app's native text): TikTok Sans Bold, sentence case, black on a white rounded box, near the middle of
the safe area, over the picture while it plays. On from the first frame, gone (a quick fade) at `--until` seconds -
by default the first cut. Picture and sound are otherwise untouched.

    python3 hook_text.py IN.mp4 OUT.mp4 "Zack Polanski this week" [--until 3.6] [--y 880] [--x 540] [--centre]
"""
import os
import subprocess
import sys
import tempfile

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'fonts', 'TikTokSans-Bold.woff')
FF = imageio_ffmpeg.get_ffmpeg_exe()
SAFE_X0, SAFE_X1 = 60, 900                    # TikTok's safe area at 1080 wide (guides/tiktok-design.md)


def emoji_img(ch, px):
    """An emoji as a picture (Google's Noto emoji, in source/fonts/emoji/<hex>.png): TikTok Sans has no emoji."""
    path = os.path.join(HERE, 'fonts', 'emoji', f'{ord(ch):x}.png')
    return Image.open(path).convert('RGBA').resize((px, px), Image.LANCZOS)


def card(w, h, text, y_mid, path, size=74, centre=False, x_mid=None):
    k = w / 1080
    text = text.replace('\ufe0f', '')                 # emoji variation selectors: the picture is the emoji
    tail = ''
    while text and ord(text[-1]) > 0x2000:          # trailing emoji are drawn as pictures after the last word
        tail, text = text[-1] + tail, text[:-1]
    text = text.rstrip()
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    while True:                                # one or two balanced lines, inside the safe width
        f = ImageFont.truetype(FONT, int(size * k))
        words = text.split()
        rows = [text]
        if d.textlength(text, font=f) > (SAFE_X1 - SAFE_X0 - 80) * k:
            cut = min(range(1, len(words)), key=lambda i: abs(d.textlength(' '.join(words[:i]), font=f)
                                                               - d.textlength(' '.join(words[i:]), font=f)))
            rows = [' '.join(words[:cut]), ' '.join(words[cut:])]
        room = (f.size + int(10 * k)) * len(tail)        # the emoji count towards the width (four suits overran it)
        if max(d.textlength(r, font=f) + (room if i == len(rows) - 1 else 0)
               for i, r in enumerate(rows)) <= (SAFE_X1 - SAFE_X0 - 80) * k:
            break
        size -= 4
    lh = int(f.size * 1.18)
    em = int(f.size * 1.0)
    emw = (em + int(10 * k)) * len(tail)             # room for the emoji on the last row
    pad_x, pad_y = int(30 * k), int(16 * k)
    cx = (x_mid if x_mid is not None else 540 if centre else (SAFE_X0 + SAFE_X1) / 2) * k   # --centre: the middle
    # of the frame (Sam, 15 Oct); --x: the card's middle anywhere across (Shocking Behaviour: onto the tower's windows)
    top = y_mid * k - len(rows) * lh / 2
    for i, r in enumerate(rows):               # each row its own white box, like the app's caption style
        tw = d.textlength(r, font=f) + (emw if i == len(rows) - 1 else 0)
        y = top + i * lh
        d.rounded_rectangle([cx - tw / 2 - pad_x, y - pad_y, cx + tw / 2 + pad_x, y + lh + pad_y - int(6 * k)],
                            radius=int(18 * k), fill=(255, 255, 255, 255))
    for i, r in enumerate(rows):
        last = i == len(rows) - 1
        tw = d.textlength(r, font=f) + (emw if last else 0)
        d.text((cx - tw / 2, top + i * lh + int(2 * k)), r, font=f, fill=(0, 0, 0, 255))
        if last:
            ex = cx - tw / 2 + d.textlength(r, font=f) + int(10 * k)
            for ch in tail:
                im.alpha_composite(emoji_img(ch, em), (int(ex), int(top + i * lh + (lh - em) / 2)))
                ex += em + int(10 * k)
    im.save(path)


def main():
    a = sys.argv[1:]
    until, y_mid = 3.6, 880
    centre = '--centre' in a
    if centre:
        a.remove('--centre')
    if '--until' in a:
        i = a.index('--until'); until = float(a[i + 1]); del a[i:i + 2]
    if '--y' in a:
        i = a.index('--y'); y_mid = float(a[i + 1]); del a[i:i + 2]
    x_mid = None
    if '--x' in a:
        i = a.index('--x'); x_mid = float(a[i + 1]); del a[i:i + 2]
    src, dst, text = a[0], a[1], ' '.join(a[2:])
    probe = subprocess.run([FF, '-i', src], capture_output=True, text=True).stderr
    w, h = next((int(x), int(y)) for t in probe.replace(',', ' ').split() if 'x' in t
                for x, _, y in [t.partition('x')] if x.isdigit() and y.isdigit() and int(x) > 100)
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, "hook.png")
        card(w, h, text, y_mid, png, centre=centre, x_mid=x_mid)
        fade = 0.25
        vf = (f'[1:v]format=rgba,fade=t=out:st={until - fade}:d={fade}:alpha=1[t];'
              f'[0:v][t]overlay=0:0:eof_action=pass:format=auto,format=yuv420p[v]')
        subprocess.run([FF, '-y', '-loglevel', 'error', '-i', src, '-loop', '1', '-t', str(until), '-i', png,
                        '-filter_complex', vf, '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-crf', '20',
                        '-preset', 'slow', '-c:a', 'copy', '-movflags', '+faststart', dst], check=True)
    print(f'{dst}: {os.path.getsize(dst) / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
