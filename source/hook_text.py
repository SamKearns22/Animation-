#!/usr/bin/env python3
"""Stamp the Hook Text (the opening line that introduces the joke) onto a finished TikTok video, in TikTok's own caption look (Sam, 15 Oct: readability
first, like the app's native text): TikTok Sans Bold, sentence case, black on a white rounded box, near the middle of
the safe area, over the picture while it plays. On from the first frame, gone (a quick fade) at `--until` seconds -
by default the first cut. Picture and sound are otherwise untouched.

    python3 hook_text.py IN.mp4 OUT.mp4 "Zack Polanski this week" [--until 3.6] [--y 880] [--x 540] [--w 400] [--centre]
"""
import os
import subprocess
import sys
import tempfile

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'fonts', 'TikTokSans-Bold.woff')
NOTO = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'   # colour emoji (installed at session start)
FF = imageio_ffmpeg.get_ffmpeg_exe()
SAFE_X0, SAFE_X1 = 60, 900                    # TikTok's safe area at 1080 wide (guides/tiktok-design.md)


def emoji_img(ch, px):
    """An emoji as a picture (Google's Noto emoji, in source/fonts/emoji/<hex>.png): TikTok Sans has no emoji."""
    path = os.path.join(HERE, 'fonts', 'emoji', f'{ord(ch):x}.png')
    if os.path.exists(path):
        return Image.open(path).convert('RGBA').resize((px, px), Image.LANCZOS)
    f = ImageFont.truetype(NOTO, 109)                   # any other emoji: the colour font (its pictures are 136 px)
    im = Image.new('RGBA', (136, 128), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox() or (0, 0, 136, 128))
    side = max(im.size)                                 # square it, centred, so it sits like the PNG ones
    sq = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    sq.alpha_composite(im, ((side - im.width) // 2, (side - im.height) // 2))
    return sq.resize((px, px), Image.LANCZOS)


def _rows(d, words, f, n):
    """The words in n balanced rows (the widest row as short as it can be)."""
    if n == 1 or len(words) < n:
        return [' '.join(words)]
    best = None
    for i in range(1, len(words) - n + 2):
        rest = _rows(d, words[i:], f, n - 1)
        rows = [' '.join(words[:i])] + rest
        wmax = max(d.textlength(r, font=f) for r in rows)
        if best is None or wmax < best[0]:
            best = (wmax, rows)
    return best[1]


def card(w, h, text, y_mid, path, size=74, centre=False, x_mid=None, width=None):
    """`width`: the card's widest row (at 1080 wide) when it sits beside someone (Netan-Yahoo!): up to three rows."""
    k = w / 1080
    room_w = (width if width else SAFE_X1 - SAFE_X0 - 80) * k
    max_rows = 3 if width else 2
    text = text.replace('\ufe0f', '')                 # emoji variation selectors: the picture is the emoji
    tail = ''
    while text and ord(text[-1]) > 0x2000:          # trailing emoji are drawn as pictures after the last word
        tail, text = text[-1] + tail, text[:-1]
    text = text.rstrip()
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    while True:                                # one to three balanced rows, inside the safe width
        f = ImageFont.truetype(FONT, int(size * k))
        words = []
        for wd in text.split():                    # a number or Roman numeral stays with the word before it
            if words and wd.strip('.,!?').isdigit() or words and set(wd.strip('.,!?')) <= set('IVX'):
                words[-1] += ' ' + wd                  # ("Blue Planet / III looks" read badly)
            else:
                words.append(wd)
        room = (f.size + int(10 * k)) * len(tail)        # the emoji count towards the width (four suits overran it)
        fits = None
        for n in range(1, max_rows + 1):
            rows = _rows(d, words, f, n)
            if max(d.textlength(r, font=f) + (room if i == len(rows) - 1 else 0)
                   for i, r in enumerate(rows)) <= room_w:
                fits = rows
                break
        if fits:
            rows = fits
            break
        size -= 4
    lh = int(f.size * 1.18)
    em = int(f.size * 1.0)
    emw = (em + int(10 * k)) * len(tail) + (d.textlength(' ', font=f) / 2 if tail else 0)   # room for the emoji
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
            ex = cx - tw / 2 + d.textlength(r, font=f) + int(10 * k) + d.textlength(' ', font=f) / 2   # a gap after the word
            for ch in tail:
                im.alpha_composite(emoji_img(ch, em), (int(ex), int(top + i * lh + (lh - em) / 2)))
                ex += em + int(10 * k)
    im.save(path)


def _pop_frames(png, tmp, fps, scales=(0.6, 1.08, 1.0)):
    """The card's pop-in (rule 82) as numbered frames in tmp: it grows from 60% past full size and settles, about
    0.2 s, each frame scaled about the card's own middle."""
    im = Image.open(png).convert('RGBA')
    box = im.getbbox()
    piece = im.crop(box)
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    n = max(3, int(round(0.2 * fps)))
    names = []
    for i in range(n):
        g = i / (n - 1) * (len(scales) - 1)
        j = min(int(g), len(scales) - 2)
        s = scales[j] + (scales[j + 1] - scales[j]) * (g - j)
        w, h = max(1, int(piece.width * s)), max(1, int(piece.height * s))
        fr = Image.new('RGBA', im.size, (0, 0, 0, 0))
        fr.alpha_composite(piece.resize((w, h), Image.LANCZOS), (int(cx - w / 2), int(cy - h / 2)))
        name = os.path.join(tmp, f'pop_{i:03d}.png')
        fr.save(name)
        names.append(name)
    return names


def main():
    a = sys.argv[1:]
    until, y_mid, start = 3.6, 880, 0.5           # rule 82: it pops in 0.5 s into the film
    if '--from' in a:
        i = a.index('--from'); start = float(a[i + 1]); del a[i:i + 2]
    centre = '--centre' in a
    if centre:
        a.remove('--centre')
    if '--until' in a:
        i = a.index('--until'); until = float(a[i + 1]); del a[i:i + 2]
    if '--y' in a:
        i = a.index('--y'); y_mid = float(a[i + 1]); del a[i:i + 2]
    width = None
    if '--w' in a:
        i = a.index('--w'); width = float(a[i + 1]); del a[i:i + 2]
    x_mid = None
    if '--x' in a:
        i = a.index('--x'); x_mid = float(a[i + 1]); del a[i:i + 2]
    src, dst, text = a[0], a[1], ' '.join(a[2:])
    probe = subprocess.run([FF, '-i', src], capture_output=True, text=True).stderr
    w, h = next((int(x), int(y)) for t in probe.replace(',', ' ').split() if 'x' in t
                for x, _, y in [t.partition('x')] if x.isdigit() and y.isdigit() and int(x) > 100)
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, "hook.png")
        card(w, h, text, y_mid, png, centre=centre, x_mid=x_mid, width=width)
        fps = next((float(t) for t, n in zip(probe.split(), probe.split()[1:]) if n.startswith('fps')
                    and t.replace('.', '').isdigit()), 24.0)
        pop = _pop_frames(png, tmp, fps)                       # rule 82: a quick pop (small, overshoot, settle)
        dur = len(pop) / fps
        fade = 0.25
        vf = (f'[1:v]format=rgba,setpts=PTS+{start}/TB[p];'
              f'[2:v]format=rgba,fade=t=out:st={until - fade}:d={fade}:alpha=1[t];'
              f"[0:v][p]overlay=0:0:eof_action=pass:enable='between(t,{start},{start + dur - 0.001})'[a];"
              f"[a][t]overlay=0:0:eof_action=pass:enable='gte(t,{start + dur})',format=yuv420p[v]")
        subprocess.run([FF, '-y', '-loglevel', 'error', '-i', src,
                        '-framerate', str(fps), '-i', os.path.join(tmp, 'pop_%03d.png'),
                        '-loop', '1', '-t', str(until), '-i', png,
                        '-filter_complex', vf, '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-crf', '20',
                        '-preset', 'slow', '-c:a', 'copy', '-movflags', '+faststart', dst], check=True)
    print(f'{dst}: {os.path.getsize(dst) / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
