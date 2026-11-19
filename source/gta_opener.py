#!/usr/bin/env python3
"""Grand Theft Autism: the 3.5 s opening, a send-up of a game-trailer logo reveal (Sam, 19 Nov).

MAP
- shield(): the parody 'VI' shield (our own shape, purple-pink-orange), lettering 'grand / theft / autism'
- skyline(): a flat waterfront city on the Flying Whales dusk sea (towers, palms, big wheel, pier)
- frame(t): the timeline (dark -> logo pops in and settles -> city fades in -> logo flashes pale and fades -> city)
- main: python3 source/gta_opener.py OUT.mp4 [--small]

House look: flat colours, one ink outline, no glows (the flash is a flat fade to pale).
"""
import math
import os
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import flying_whales_sea as S                     # noqa: E402

W, H = S.SIZE
FPS = 30
DUR = 3.5
INK = (36, 14, 48)
DARK = (28, 27, 38)
FONT = os.path.join(HERE, 'fonts', 'Anton-Regular.ttf')


def _ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def _back(x):
    """Overshoot then settle (the pop-in)."""
    x = min(1.0, max(0.0, x))
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def _grad(size, stops):
    """Diagonal gradient (top-left to bottom-right) through colour stops."""
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    k = (xx / w * 0.45 + yy / h * 0.55)
    out = np.zeros((h, w, 3))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        m = (k >= a) & (k <= b)
        f = ((k - a) / (b - a))[m][:, None]
        out[m] = np.array(ca) * (1 - f) + np.array(cb) * f
    return Image.fromarray(out.astype(np.uint8))


def shield(ss=2):
    """The logo on a transparent layer, about 820 px wide (ss times larger)."""
    Wd, Hd = 900 * ss, 760 * ss
    img = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))
    s = ss
    # our own shape: a slanted V with a tall I bar on its right, joined at the top
    V = [(40, 60), (290, 60), (420, 470), (560, 60), (650, 60), (650, 40), (860, 40), (860, 720), (650, 720),
         (650, 330), (520, 720), (320, 720)]
    V = [(x * s, y * s) for x, y in V]
    mask = Image.new('L', (Wd, Hd), 0)
    ImageDraw.Draw(mask).polygon(V, fill=255)
    fill = _grad((Wd, Hd), [(0, (88, 70, 220)), (0.42, (214, 64, 168)), (0.7, (240, 92, 120)),
                            (1.0, (250, 170, 70))])
    d = ImageDraw.Draw(img)
    d.polygon(V, fill=INK)                             # the thick dark rim, drawn as a fatter copy below
    rim = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))
    ImageDraw.Draw(rim).line(V + [V[0]], fill=INK + (255,), width=34 * s, joint='curve')
    img.alpha_composite(rim)
    body = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))
    body.paste(fill, (0, 0), mask)
    img.alpha_composite(body)
    ImageDraw.Draw(img).line(V + [V[0]], fill=(255, 255, 255, 255), width=7 * s, joint='curve')
    # lettering: chunky, each letter bobbed a little off the line (the bouncy game-title look)
    rows = [('grand', 175, 250), ('theft', 245, 395), ('autism', 130, 540)]
    rnd = random.Random(6)
    for word, x0, y0 in rows:
        f = ImageFont.truetype(FONT, 168 * s)
        x = x0 * s
        for ch in word:
            dy = rnd.uniform(-5, 5) * s
            lay = Image.new('RGBA', (260 * s, 300 * s), (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            ld.text((30 * s, 20 * s), ch, font=f, fill=(255, 255, 255, 255), stroke_width=13 * s,
                    stroke_fill=INK + (255,))
            lay = lay.rotate(rnd.uniform(-2.5, 2.5), resample=Image.BICUBIC, center=(90 * s, 150 * s))
            img.alpha_composite(lay, (int(x - 30 * s), int(y0 * s - 150 * s + dy)))
            x += f.getlength(ch) * 1.0
    return img.resize((Wd // ss, Hd // ss), Image.LANCZOS)


def _palm(d, x, base, h, lean, col, s):
    pts = [(x + lean * (i / 8) ** 1.6, base - h * i / 8) for i in range(9)]
    d.line([(px * s, py * s) for px, py in pts], fill=col, width=int(7 * s))
    tx, ty = pts[-1]
    for a in (-160, -125, -90, -55, -20, 200):
        r = math.radians(a)
        L = h * 0.42
        ex, ey = tx + math.cos(r) * L, ty + math.sin(r) * L * 0.55 + L * 0.35
        mx, my = tx + math.cos(r) * L * 0.5, ty + math.sin(r) * L * 0.5 - 6
        d.line([(tx * s, ty * s), (mx * s, my * s), (ex * s, ey * s)], fill=col, width=int(9 * s), joint='curve')


def skyline(ss=2):
    """A flat waterfront city standing on the horizon, as an RGBA layer the size of the frame."""
    hy = S.horizon_y()
    lay = Image.new('RGBA', (W * ss, H * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    s = ss
    rnd = random.Random(19)
    far, near = (150, 104, 160), (104, 66, 122)
    # far towers, paler (haze), then near towers darker; each with the one ink outline
    for col, n, hmin, hmax, wmin, wmax in ((far, 16, 160, 420, 50, 110), (near, 12, 140, 560, 60, 140)):
        x = rnd.uniform(-60, 0)
        while x < W + 40:
            w = rnd.uniform(wmin, wmax)
            h = rnd.uniform(hmin, hmax)
            if 120 < x < 420 and col == near:          # keep the sunset gap clear (the sun sits left)
                x += w * 1.6
                continue
            top = hy - h
            box = [x * s, top * s, (x + w) * s, (hy + 4) * s]
            d.rectangle(box, fill=col + (255,), outline=INK + (255,), width=int(3 * s))
            if rnd.random() < 0.4:                     # a stepped crown on some
                cw = w * 0.55
                d.rectangle([(x + (w - cw) / 2) * s, (top - h * 0.12) * s, (x + (w + cw) / 2) * s, top * s],
                            fill=col + (255,), outline=INK + (255,), width=int(3 * s))
            # lit window rows, faint
            for yy in np.arange(top + 18, hy - 10, 26):
                d.line([(x + 10) * s, yy * s, (x + w - 10) * s, yy * s], fill=_lift(col, 18) + (255,),
                       width=int(4 * s))
            x += w + rnd.uniform(-10, 30)
    # the big wheel, right
    cx, cy, r = 880, hy - 215, 190
    d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], outline=INK + (255,), width=int(6 * s))
    for k in range(16):
        a = 2 * math.pi * k / 16
        d.line([cx * s, cy * s, (cx + math.cos(a) * r) * s, (cy + math.sin(a) * r) * s], fill=INK + (255,),
               width=int(3 * s))
        d.ellipse([(cx + math.cos(a) * r - 9) * s, (cy + math.sin(a) * r - 9) * s,
                   (cx + math.cos(a) * r + 9) * s, (cy + math.sin(a) * r + 9) * s], fill=INK + (255,))
    d.polygon([((cx - 70) * s, hy * s), (cx * s, cy * s), ((cx + 70) * s, hy * s)], outline=INK + (255,),
              width=int(6 * s))
    # pier along the waterline, then palms in front
    d.rectangle([0, (hy - 30) * s, 760 * s, (hy + 6) * s], fill=(70, 40, 88, 255))
    for px in range(10, 760, 46):
        d.line([px * s, (hy - 30) * s, px * s, (hy + 8) * s], fill=INK + (255,), width=int(4 * s))
    d.line([0, (hy - 30) * s, 760 * s, (hy - 30) * s], fill=INK + (255,), width=int(4 * s))
    for px, h, lean in ((40, 230, 30), (110, 190, -20), (470, 250, 25), (560, 200, -30), (640, 235, 15),
                        (760, 210, -25), (1040, 240, -35)):
        _palm(d, px, hy + 6, h, lean, (52, 26, 66, 255), s)
    return lay.resize((W, H), Image.LANCZOS)


def _lift(c, k):
    return tuple(min(255, v + k) for v in c)


def _scale_place(img, layer, scale, cx, cy, alpha):
    if alpha <= 0:
        return
    w, h = layer.size
    L = layer.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    if alpha < 1:
        a = L.getchannel('A').point(lambda v: int(v * alpha))
        L.putalpha(a)
    img.alpha_composite(L, (int(cx - L.size[0] / 2), int(cy - L.size[1] / 2)))


def frame(t, LOGO, PALE, CITY):
    # the city: fades in from dark at 1.4-2.0 s, slow push all the way
    push = 1.0 + 0.05 * t / DUR
    city_a = _ease((t - 1.4) / 0.6)
    img = Image.new('RGBA', (W, H), DARK + (255,))
    if city_a > 0:
        bg = S.paint(t).convert('RGBA')
        bg.alpha_composite(CITY)
        bw, bh = int(W * push), int(H * push)
        bg = bg.resize((bw, bh), Image.LANCZOS).crop(((bw - W) // 2, (bh - H) // 2, (bw - W) // 2 + W,
                                                      (bh - H) // 2 + H))
        img = Image.blend(img, bg, city_a)
    # the logo: pops in (0-0.45 s), holds, turns pale (2.0-2.4 s), fades out (2.4-2.9 s)
    pop = _back(t / 0.45)
    scale = (0.55 + 0.45 * pop) * (1.0 + 0.04 * t / DUR)
    a_in = _ease(t / 0.2)
    a_out = 1 - _ease((t - 2.4) / 0.5)
    pale = _ease((t - 2.0) / 0.4)
    cy = 760
    _scale_place(img, LOGO, scale, W / 2 + 15, cy, a_in * a_out * (1 - pale))
    _scale_place(img, PALE, scale, W / 2 + 15, cy, a_in * a_out * pale)
    return img.convert('RGB')


def main():
    out = sys.argv[1]
    small = '--small' in sys.argv
    LOGO = shield()
    pale = Image.new('RGBA', LOGO.size, (255, 236, 246, 0))
    pale.putalpha(LOGO.getchannel('A').point(lambda v: int(v * 0.85)))
    PALE = Image.blend(LOGO, pale, 0.0)
    PALE = Image.alpha_composite(LOGO, pale)
    CITY = skyline()
    size = '540x960' if small else '1080x1920'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-vf', f'scale={size}', '-c:v', 'libx264', '-crf', '20',
                          '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(i / FPS, LOGO, PALE, CITY).tobytes())
    p.stdin.close()
    p.wait()


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'still':
        L, C = shield(), skyline()
        P = Image.alpha_composite(L, Image.new('RGBA', L.size, (0, 0, 0, 0)))
        for tt in map(float, sys.argv[3:]):
            frame(tt, L, P, C).resize((540, 960)).save(sys.argv[2].replace('.png', f'_{tt}.png'))
    else:
        main()
