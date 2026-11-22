#!/usr/bin/env python3
"""MAP: story post (still, 1080x1920) for the Grand Theft Autism delay (Sam, 22 Nov): the film's own VI logo, WITH
its Grand Theft Autism lettering (that makes it our parody; bare, it would copy Rockstar's logo, so never shown
without it), lifted from the clean render at 1.67 s (logo fully in, city not yet), cut out onto pure black and
doubled in size; Sam's line in front in the cranberry title. (The logo can't be redrawn sharp here: its font is
downloaded at render time and that site is blocked in some sessions.)
    python3 source/gta_story_post.py animations/drafts/grand-theft-autism-clean.mp4 animations/gta-delay-story.png"""
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np                        # noqa: E402
from PIL import Image, ImageFont, ImageFilter   # noqa: E402
import body as B                          # noqa: E402

TEXT = ("SMALL DELAY ON NEXT FILM WHILST 'I' LEARN HOW TO ANIMATE A MAN LEANING OUT A CAR WINDOW "
        "AND SHOOTING SOMEONE IN THE FACE")
LAST = 'BRB KISSES XX'


def logo_from(src):
    png = os.path.join(tempfile.mkdtemp(), 'f.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '1.7', '-i', src, '-frames:v', '1', png], check=True)
    a = np.asarray(Image.open(png).convert('RGB')).astype(np.float32)
    a[:60] = a[100, 20]                                           # drop the time label in the corner
    bg = np.median(a[700:900, :, :].reshape(-1, 3), axis=0)
    d = np.sqrt(((a - bg) ** 2).sum(2))
    alpha = np.clip((d - 14) / 26, 0, 1) * 255
    img = Image.fromarray(a.astype(np.uint8)).convert('RGBA')
    img.putalpha(Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.MaxFilter(3)))
    img = img.crop(img.getbbox())
    return img.resize((img.width * 2, img.height * 2), Image.LANCZOS)


def main(src, out):
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 255))
    logo = logo_from(src)
    img.alpha_composite(logo, ((1080 - logo.width) // 2, (1920 - logo.height) // 2))
    cap = 74
    probe = ImageFont.truetype(B.ANTON, 1000)
    l, t, r, b = probe.getbbox('H')
    f = ImageFont.truetype(B.ANTON, int(round(cap * 1000 / (b - t))))
    lines = B.wrap(TEXT, f, 900 / 1.2) + [LAST]
    B.SS = 1
    B.title_lines(img, lines, cap=cap, top=(1920 - len(lines) * 91) // 2)
    img.convert('RGB').save(out)
    print('wrote', out, lines)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
