#!/usr/bin/env python3
"""The CranbriJoos sign-off (Sam, 15 Oct): the profile beaver, deadpan behind a little bar counter, takes one sip
from a CranbriJoos juice box through a straw; the account name is on the counter. About a second, silent unless Sam
asks for a slurp. Added to the end of every film, after the last line (never before the punchline).

    python3 signoff.py still OUT.png          one frame, for approval
    python3 signoff.py clip OUT.mp4           the sign-off on its own (1080 x 1920, 12 fps)
    python3 signoff.py add FILM.mp4 OUT.mp4   a finished film with the sign-off joined on the end
"""
import math
import os
import subprocess
import sys
import tempfile

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OPEN = os.path.join(ROOT, 'profile', 'cranbrijoos-tiktok-1080-eyes-open.png')
SHUT = os.path.join(ROOT, 'profile', 'cranbrijoos-tiktok-1080.png')
TITLE_FONT = os.path.join(HERE, 'fonts', 'Anton-Regular.ttf')
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 12
W, H = 1080, 1920
SIZE, CROP = 1350, 135                       # the profile square enlarged to fill the top; its sides trimmed
TOP = 0
COUNTER = int(SIZE * 0.712)                  # the counter's top edge: hides the paws and leaves
CRANBERRY, INK = (178, 24, 52), (24, 20, 22)
MOUTH = (int(0.555 * SIZE) - CROP, int(0.6 * SIZE))   # the corner of the mouth, beside the teeth


def background(img):
    """Above the square: the profile picture's own dark sky, stretched up so the frame is full."""
    sq = Image.open(OPEN).convert('RGB')
    strip = sq.crop((0, 0, 1080, 40)).resize((1080, TOP), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    img.paste(strip, (0, 0))


def juice_box(d, cx, base, squeeze=0.0):
    """A small cranberry-red juice box on the counter, its straw up to the beaver's mouth; `squeeze` 0-1 dents its
    sides as he sips."""
    w, h = 124, 150
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, base - h, base
    dent = 10 * squeeze
    d.polygon([(x0, y0), (x1, y0), (x1 - dent, (y0 + y1) / 2), (x1, y1), (x0, y1), (x0 + dent, (y0 + y1) / 2)],
              fill=CRANBERRY, outline=INK, width=5)
    d.polygon([(x0, y0), (x1, y0), (x1 - 14, y0 - 16), (x0 + 14, y0 - 16)], fill=(150, 18, 42), outline=INK, width=4)
    d.rounded_rectangle([x0 + 12, y0 + 24, x1 - 12, y0 + 88], 10, fill=(250, 246, 240), outline=INK, width=3)
    f = ImageFont.truetype(TITLE_FONT, 22)
    for i, word in enumerate(('CRANBRI', 'JOOS')):
        tw = d.textlength(word, font=f)
        d.text((cx - tw / 2, y0 + 30 + i * 27), word, font=f, fill=CRANBERRY)
    for dx, dy in ((-24, 118), (0, 110), (22, 120)):                      # cranberries on the side
        d.ellipse([cx + dx - 11, y0 + dy - 11, cx + dx + 11, y0 + dy + 11], fill=(200, 30, 60), outline=INK, width=3)
    # the straw: out of the top corner, a bend, up into the mouth; it fills with juice as he sips
    sx, sy = x0 + 30, y0 - 10
    pts = [(sx, sy), (sx - 10, sy - 26), (MOUTH[0], MOUTH[1])]
    for wdt, col in ((20, INK), (13, (250, 250, 250))):
        d.line(pts, fill=col, width=wdt, joint='curve')
    if squeeze > 0:
        u = min(1.0, squeeze * 1.6)
        d.line([(sx, sy), (sx - 10 * u, sy - 26 * u)], fill=CRANBERRY, width=8)


def counter(d):
    d.rectangle([0, COUNTER, W, H], fill=(112, 66, 40))
    d.rectangle([0, COUNTER, W, COUNTER + 34], fill=(140, 86, 52), outline=INK, width=5)
    for y in range(COUNTER + 80, H, 70):                                   # wood grain
        d.line([(0, y), (W, y + 6)], fill=(98, 56, 34), width=3)
    f = ImageFont.truetype(TITLE_FONT, 150)
    name = 'CranbriJoos'
    tw = d.textlength(name, font=f)
    x, y = 480 - tw / 2, COUNTER + 120                                     # centred in the safe area (x 60-900)
    d.text((x, y), name, font=f, fill=CRANBERRY, stroke_width=8, stroke_fill=INK)


def frame(k, n):
    """Frame k of n: eyes open; then the sip (eyes shut, box squeezed, juice up the straw); then back to us, deadpan."""
    u = k / max(1, n - 1)
    sipping = 0.3 <= u < 0.68
    img = Image.new('RGB', (W, H), (40, 44, 52))
    sq = Image.open(SHUT if sipping else OPEN).convert('RGB').resize((SIZE, SIZE), Image.LANCZOS)
    img.paste(sq.crop((CROP, 0, CROP + W, SIZE)), (0, TOP))
    d = ImageDraw.Draw(img)
    counter(d)
    juice_box(d, MOUTH[0] + 120, COUNTER + 16, squeeze=min(1.0, (u - 0.3) / 0.25) if sipping else (0.4 if u >= 0.68 else 0.0))
    return img


def frames(dur=1.2):
    n = int(round(dur * FPS))
    return [frame(k, n) for k in range(n)]


def clip(out, dur=1.2):
    p = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono', '-shortest',
                          '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-movflags', '+faststart',
                          out], stdin=subprocess.PIPE)
    for im in frames(dur):
        p.stdin.write(np.asarray(im).tobytes())
    p.stdin.close()
    p.wait()


def add(film, out):
    """Join the sign-off onto the end of a finished film (same size and frame rate), sound kept."""
    with tempfile.TemporaryDirectory() as tmp:
        so = os.path.join(tmp, 'signoff.mp4')
        clip(so)
        subprocess.run([FF, '-y', '-loglevel', 'error', '-i', film, '-i', so, '-filter_complex',
                        '[0:v]fps=12,format=yuv420p[a];[1:v]fps=12,format=yuv420p[b];[0:a]aresample=48000[x];'
                        '[1:a]aresample=48000[y];[a][x][b][y]concat=n=2:v=1:a=1[v][s]',
                        '-map', '[v]', '-map', '[s]', '-c:v', 'libx264', '-crf', '20', '-preset', 'slow', '-c:a', 'aac',
                        '-b:a', '160k', '-movflags', '+faststart', out], check=True)
    print(f'{out}: {os.path.getsize(out) / 1e6:.1f} MB')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'still':
        frame(int(sys.argv[3]) if len(sys.argv) > 3 else 0, 14).save(sys.argv[2])
    elif cmd == 'clip':
        clip(sys.argv[2])
    elif cmd == 'add':
        add(sys.argv[2], sys.argv[3])
