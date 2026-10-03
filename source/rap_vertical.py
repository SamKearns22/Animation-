#!/usr/bin/env python3
"""TikTok versions of the two Oxford rap battle films, following guides/tiktok-design.md.

The widescreen picture (drawn untitled and without subtitles) is enlarged by a third over fitting the
width and sits in the middle of a 1080 x 1920 frame, with a soft glow of its own top and bottom edges
above and below. The title, subtitles and UNINTELLIGIBLE flashes are drawn fresh at full size inside the
safe area (x 60-900, y 310-1500).

Usage:
    python3 rap_vertical.py andy|sam stills OUT_DIR T1 T2 ...
    python3 rap_vertical.py andy|sam render OUT.mp4
"""
import os
import sys

os.environ['PENCIL_W'], os.environ['PENCIL_H'], os.environ['PENCIL_FPS'] = '1280', '720', '8'

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

import pencil_cartoon  # noqa: E402
sys.modules['pencil'] = pencil_cartoon  # rap.py was drawn with this version of the pencil kit

FILM = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ('andy', 'sam') else 'andy'
if FILM == 'sam':
    import sam as F  # noqa: E402
    import rap as R  # noqa: E402  (sam.py points R's subtitles and flashes at its own battle)
    TITLE = 'SAM'
else:
    import rap as F  # noqa: E402
    R = F
    TITLE = 'ANDY'

HERE = os.path.dirname(os.path.abspath(__file__))
ANTON = os.path.join(HERE, 'fonts', 'Anton-Regular.ttf')
SANS = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
CRANBERRY = (178, 24, 52)
VW, VH = 1080, 1920
SCALE = 1.125                      # a third larger than fitting the width (1080 / 1280 * 4 / 3)
PW, PH = int(1280 * SCALE), int(720 * SCALE)
PIC_TOP = 500                      # picture spans y 500-1310, between the title and the subtitles
TITLE_HOLD, TITLE_GONE = 0.75, 1.0
FPS = R.FPS

R.overlay = lambda frame, t: frame  # draw the picture clean; words are added below at full size
_fonts = {}


def font(path, size):
    if (path, size) not in _fonts:
        _fonts[path, size] = ImageFont.truetype(path, size)
    return _fonts[path, size]


def wrap(s, f, width):
    rows, cur = [], ''
    for w in s.split():
        if cur and f.getlength(cur + ' ' + w) > width:
            rows.append(cur)
            cur = w
        else:
            cur = (cur + ' ' + w).strip()
    rows.append(cur)
    if len(rows) == 2:  # balance two rows so the second is not a lone word
        words = s.split()
        best = min(range(1, len(words)), key=lambda k: abs(f.getlength(' '.join(words[:k])) -
                                                            f.getlength(' '.join(words[k:]))))
        a, b = ' '.join(words[:best]), ' '.join(words[best:])
        if max(f.getlength(a), f.getlength(b)) <= width:
            rows = [a, b]
    return rows


def glow(edge, height, flip):
    """A soft glow made from one edge of the picture, fading into the scene's own colour."""
    row = edge.mean(axis=0, keepdims=True)                       # one colour per column, no streaks
    row = np.asarray(Image.fromarray(row.astype(np.uint8)).resize((VW // 8, 1), Image.BILINEAR)
                     .filter(ImageFilter.GaussianBlur(4)).resize((VW, 1), Image.BILINEAR), float)
    base = edge.reshape(-1, 3).mean(axis=0)
    d = np.linspace(0, 1, height)[:, None, None]                 # 0 at the picture, 1 at the frame edge
    d = 1 - (1 - d) ** 2
    pad = row * (1 - d) + base * d
    pad = pad * (1 - 0.18 * d)                                   # a touch darker towards the frame edge
    return pad[::-1] if flip else pad


def compose(pic):
    """The widescreen drawing, enlarged and centred, with glow pads above and below."""
    big = np.asarray(Image.fromarray(pic).resize((PW, PH), Image.LANCZOS), float)
    x0 = (PW - VW) // 2
    big = big[:, x0:x0 + VW]
    out = np.empty((VH, VW, 3))
    out[PIC_TOP:PIC_TOP + PH] = big
    out[:PIC_TOP] = glow(big[:24], PIC_TOP, True)
    out[PIC_TOP + PH:] = glow(big[-24:], VH - PIC_TOP - PH, False)
    for y0, sign in ((PIC_TOP, 1), (PIC_TOP + PH, -1)):          # soften the seams
        for k in range(1, 7):
            a = 0.5 * (1 - k / 7)
            y = y0 - k if sign > 0 else y0 + k - 1
            yi = y0 if sign > 0 else y0 - 1
            out[y] = out[y] * (1 - a) + out[yi] * a
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert('RGBA')


def title(img, t):
    if t >= TITLE_GONE:
        return
    alpha = 1.0 if t < TITLE_HOLD else 1 - (t - TITLE_HOLD) / (TITLE_GONE - TITLE_HOLD)
    probe = font(ANTON, 1000)
    l, tp, r, b = probe.getbbox('H')
    size = int(round(148 * 1000 / (b - tp)))                     # capitals 148 px tall: the account's standard
    f = font(ANTON, size)
    out = max(3, int(size * 0.075))
    l, tp, r, b = f.getbbox(TITLE, stroke_width=out)
    lay = Image.new('RGBA', (r - l + 2 * out, b - tp + 2 * out), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((out - l, out - tp), TITLE, font=f, fill=(0, 0, 0), stroke_width=out, stroke_fill=(0, 0, 0))
    d.text((out - l, out - tp), TITLE, font=f, fill=CRANBERRY, stroke_width=max(1, int(size * 0.012)),
           stroke_fill=CRANBERRY)
    lay = lay.resize((int(lay.width * 1.2), lay.height), Image.LANCZOS)
    if alpha < 1:
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * alpha)))
    img.alpha_composite(lay, (int(540 - lay.width / 2), 330 - out))


def caption(img, s, bottom=1495):
    """Speech: bold white letters with a black outline, wrapped to 700 px, centred on the frame."""
    size = 46
    while True:
        f = font(SANS, size)
        rows = wrap(s, f, 700)
        if len(rows) <= 3 or size <= 34:
            break
        size -= 2
    d = ImageDraw.Draw(img)
    step = int(size * 1.25)
    for i, row in enumerate(rows):
        d.text((540, bottom - size // 2 - 4 - step * (len(rows) - 1 - i)), row, font=f, fill=(255, 255, 255),
               anchor='mm', stroke_width=5, stroke_fill=(0, 0, 0))


def flash(img, t, a, b):
    """The flashing red UNINTELLIGIBLE sign, redrawn to fit the safe width, over the middle of the picture."""
    k = int((t - a) * FPS)
    if k % 3 == 2:  # on, on, off
        return
    words = 'UNINTELLIGIBLE'
    mid = (a + b) / 2
    if a == 99.3 and mid <= t < mid + 0.375 and R is F:  # one single flash of... what was that?
        words = 'FROG IN THE HOB?'
    f = font(SANS, 96)
    while f.getlength(words) + 14 > 700:
        f = font(SANS, f.size - 2)
    if k % 2 == 0:
        f = font(SANS, int(f.size * 0.94))
    lay = Image.new('RGBA', (VW, VH), (0, 0, 0, 0))
    cy = PIC_TOP + PH // 2
    ImageDraw.Draw(lay).text((540, cy), words, font=f, fill=(220, 20, 20, 255), anchor='mm', stroke_width=6,
                             stroke_fill=(255, 255, 255, 255))
    lay = lay.rotate(-4 if k % 2 else 3, resample=Image.BICUBIC, center=(540, cy))
    img.alpha_composite(lay)


def render(n):
    t = n / FPS
    img = compose(F.render(n))
    fl = next(((a, b) for a, b in R.UNINTELLIGIBLE if a <= t < b), None)
    if fl:
        flash(img, t, *fl)
    else:
        for a, b, txt in R.SUBS:
            if a <= t < b:
                caption(img, txt)
                break
    title(img, t)
    return np.asarray(img.convert('RGB'))


if __name__ == '__main__':
    mode = sys.argv[2]
    if mode == 'stills':
        out = sys.argv[3]
        os.makedirs(out, exist_ok=True)
        for ts in sys.argv[4:]:
            Image.fromarray(render(int(round(float(ts) * FPS)))).save(os.path.join(out, f'{FILM}_{float(ts):06.2f}s.png'))
    elif mode == 'render':
        pencil_cartoon.render_video(sys.argv[3], render, int(F.DUR * FPS), F.make_audio, crf=26, size=(VW, VH))
