#!/usr/bin/env python3
"""MAP: story post for DLC (Bayeux Season Pass): the film's opening up to the end of the title reveal (0-14.77 s,
cut on the last clean title frame before the glitch into NEW SKINS), with Sam's cranberry text over it.
    python3 source/bayeux_story_post.py animations/bayeux-season-pass-vertical.mp4 animations/bayeux-season-pass-story.mp4
Text at the top (Sam, 3 Nov), above the tapestry band (y 140-310), on from the first frame."""
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image                       # noqa: E402
import burnham as B                         # noqa: E402
from hook_text import emoji_img, FF         # noqa: E402

LINES = ['GIVE THIS ONE', 'SOME LOVE']
END, CAP, TOP = 14.77, 78, 140


def overlay(path):
    B.SS = 1
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    B.title_lines(img, LINES[:1], cap=CAP, top=TOP)
    row = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))                     # second row on its own layer
    B.title_lines(row, LINES[1:], cap=CAP, top=0)
    x0, y0, x1, y1 = row.getbbox()
    row = row.crop((x0, y0, x1, y1))
    e = emoji_img('\U0001F525', int(row.height * 1.0))
    left = 540 - (row.width + 10 + e.width) // 2                              # row + emoji centred
    top = img.getbbox()[3] - 6
    img.alpha_composite(row, (left, top))
    img.alpha_composite(e, (left + row.width + 10, top))
    img.save(path)


if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    png = os.path.join(tempfile.mkdtemp(), 'text.png')
    overlay(png)
    subprocess.run([FF, '-v', 'error', '-y', '-i', src, '-i', png, '-t', str(END), '-filter_complex',
                    '[0:v][1:v]overlay=0:0,format=yuv420p[v];[0:a]afade=t=out:st=%.2f:d=0.4[a]' % (END - 0.4),
                    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '22', '-preset', 'slow',
                    '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)
    print('wrote', out)
