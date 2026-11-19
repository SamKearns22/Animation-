#!/usr/bin/env python3
"""Grand Theft Autism: the 3.5 s opening, a send-up of a game-trailer logo reveal (Sam, 19 Nov).

MAP
- sky set-up (top): the Flying Whales dusk sea, re-coloured pink and the sun moved right of centre (as the reference)
- logo(): our own V + I shield (blue-purple-pink-orange, faint palm leaves inside), 'grand / theft / autism'
- clouds(), skyline(): big flat clouds; the waterfront city (towers, pergola, big tree, palms, big wheel, boats)
- frame(t): dark -> logo wipes in top to bottom and grows -> city fades in -> logo washes pale and dissolves -> city
- python3 source/gta_opener.py OUT.mp4 [--small]      python3 source/gta_opener.py still OUT.png T [T ...]

Reference: Sam's screen recording (19 Nov), 3.4 s. House look: flat colours, one ink outline, no glows.
"""
import math
import os
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import flying_whales_sea as S                     # noqa: E402

# ---- the sky and sea, re-coloured before anything is baked (the painter caches its first bake)
S.SUN_AZ = math.atan(100 / 1400)                  # the sun a little right of centre, as in the reference
S.SKY = [(0.55, (255, 240, 222)), (1.35, (253, 220, 206)), (2.7, (248, 198, 202)), (4.6, (240, 178, 202)),
         (7.6, (230, 168, 210)), (12.0, (218, 160, 214)), (19.0, (204, 152, 216)), (28.0, (190, 144, 214)),
         (90.0, (174, 134, 208))]
S.GOLD = (255, 248, 232)
S.SEA_DEEP = (70, 36, 82)
S.SEA = [S._mix(c, S.SEA_DEEP, 0.30 + 0.08 * k) for k, (_, c) in enumerate(S.SKY)]
S.CLOUDS = []                                     # our own big clouds instead (clouds())

W, H = S.SIZE
FPS = 30
DUR = 3.5
INK = (40, 12, 56)
DARK = (27, 26, 36)
OL = 3
FONT = os.path.join(HERE, 'fonts', 'Montserrat-Black.ttf')
HY = S.horizon_y()
SUNX = S._sun_x()


def _ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def _grad(size, stops):
    """Diagonal gradient, top-left to bottom-right, through colour stops."""
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    k = np.clip(xx / w * 0.5 + yy / h * 0.5, 0, 1)
    out = np.zeros((h, w, 3))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        m = (k >= a) & (k <= b)
        f = ((k - a) / (b - a))[m][:, None]
        out[m] = np.array(ca) * (1 - f) + np.array(cb) * f
    return Image.fromarray(out.astype(np.uint8))


def _frond(d, x, y, ang, L, wid, col, s, droop=0.55):
    """One palm leaf: a tapered curve from (x, y) out along ang (degrees), drooping at the tip."""
    r = math.radians(ang)
    pts = []
    for i in range(9):
        u = i / 8
        pts.append((x + math.cos(r) * L * u, y + math.sin(r) * L * u + droop * L * u * u))
    left, right = [], []
    for i, (px, py) in enumerate(pts):
        u = i / 8
        w = wid * math.sin(math.pi * min(0.95, u * 0.9 + 0.08))
        if i < 8:
            dx, dy = pts[i + 1][0] - px, pts[i + 1][1] - py
        else:
            dx, dy = px - pts[i - 1][0], py - pts[i - 1][1]
        n = math.hypot(dx, dy) or 1
        left.append(((px - dy / n * w) * s, (py + dx / n * w) * s))
        right.append(((px + dy / n * w) * s, (py - dx / n * w) * s))
    d.polygon(left + right[::-1], fill=col)


def _palm(d, x, base, h, lean, col, s, size=1.0):
    pts = [(x + lean * (i / 8) ** 1.6, base - h * i / 8) for i in range(9)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        d.line([ax * s, ay * s, bx * s, by * s], fill=col, width=int(6 * s * size))
    tx, ty = pts[-1]
    for a in (-170, -140, -110, -75, -40, -10, 150, 30):
        _frond(d, tx, ty, a, 70 * size, 9 * size, col, s)


def logo(ss=2):
    """The logo on a transparent layer, 920 x 780 px (drawn at ss times and shrunk)."""
    s = ss
    Wd, Hd = 920 * s, 780 * s
    V = [(30, 40), (285, 40), (452, 500), (605, 40), (700, 40), (522, 740), (372, 740)]
    I = [(730, 40), (890, 40), (890, 740), (730, 740)]
    shapes = [[(x * s, y * s) for x, y in P] for P in (V, I)]
    mask = Image.new('L', (Wd, Hd), 0)
    md = ImageDraw.Draw(mask)
    for P in shapes:
        md.polygon(P, fill=255)
    fill = _grad((Wd, Hd), [(0, (72, 96, 232)), (0.3, (140, 70, 214)), (0.55, (226, 72, 168)),
                            (0.78, (246, 104, 120)), (1.0, (252, 176, 72))]).convert('RGBA')
    leaves = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))     # faint palm leaves inside, as in the reference
    ld = ImageDraw.Draw(leaves)
    for x, y, a0 in ((180, 120, 0), (640, 200, 40), (820, 520, -20), (420, 650, 10)):
        for a in range(-170, 180, 34):
            _frond(ld, x, y, a + a0, 190, 20, (60, 20, 120, 60), s, droop=0.35)
    fill.alpha_composite(leaves)
    img = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))
    rd = ImageDraw.Draw(img)
    for P in shapes:
        rd.line(P + [P[0]], fill=INK + (255,), width=30 * s, joint='curve')
        rd.polygon(P, fill=INK + (255,))
    body = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))
    body.paste(fill, (0, 0), mask)
    img.alpha_composite(body)
    wd = ImageDraw.Draw(img)
    for P in shapes:
        wd.line(P + [P[0]], fill=(255, 250, 252, 255), width=6 * s, joint='curve')
    # lettering: chunky, white, thick dark outline, each letter bobbed and tipped a little (the game-title look)
    rnd = random.Random(6)
    f = ImageFont.truetype(FONT, 168 * s)
    fR = ImageFont.truetype(FONT, 184 * s)
    for word, x0, y0 in (('grand', 95, 255), ('theft', 190, 425), ('autism', 85, 595)):
        x = x0 * s
        for ch in word:
            big = ch == 'r' and word == 'grand'            # the reference's odd capital R
            fc, c = (fR, 'R') if big else (f, ch)
            lay = Image.new('RGBA', (300 * s, 320 * s), (0, 0, 0, 0))
            ImageDraw.Draw(lay).text((40 * s, 30 * s), c, font=fc, fill=(255, 255, 255, 255), stroke_width=14 * s,
                                     stroke_fill=INK + (255,))
            lay = lay.rotate(rnd.uniform(-3, 3), resample=Image.BICUBIC, center=(110 * s, 160 * s))
            dy = rnd.uniform(-6, 6) * s - (8 * s if big else 0)
            img.alpha_composite(lay, (int(x - 40 * s), int(y0 * s - 190 * s + dy)))
            x += fc.getlength(c) * 0.9
    return img.resize((Wd // ss, Hd // ss), Image.LANCZOS)


def _pale(L):
    """The washed-out logo of the flash: every colour pushed to pink-white, the shape kept."""
    a = np.asarray(L).astype(float)
    rgb = a[..., :3] * 0.3 + np.array([255, 232, 244]) * 0.7
    return Image.fromarray(np.dstack([rgb, a[..., 3]]).astype(np.uint8), 'RGBA')


def _blob(d, lumps, fill, s):
    for x, y, r in lumps:
        d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=fill)


def clouds(ss=2):
    """Big flat clouds: lavender bodies, pale tops, pink undersides, one ink outline."""
    s = ss
    rnd = random.Random(4)
    rgb = np.zeros((H * s, W * s, 3), np.uint8)
    alpha = np.zeros((H * s, W * s), np.uint8)
    for cx, cy, wid, sc in ((180, 330, 520, 1.0), (820, 520, 600, 1.15), (330, 760, 460, 0.8),
                            (900, 180, 420, 0.9), (640, 930, 300, 0.55)):
        lumps = []
        n = int(wid / 55)
        for i in range(n):
            u = i / (n - 1) - 0.5
            r = (60 + rnd.uniform(0, 45)) * sc * (1 - abs(u) ** 2 * 1.4)
            lumps.append((cx + u * wid, cy - r * 0.35 + rnd.uniform(-12, 12), max(18, r)))
        m = Image.new('L', (W * s, H * s), 0)
        _blob(ImageDraw.Draw(m), lumps, 255, s)
        ImageDraw.Draw(m).rectangle([0, int((cy + 40 * sc) * s), W * s, H * s], fill=0)   # flat-ish bottoms
        full = np.asarray(m) > 127
        ring = np.asarray(m.filter(ImageFilter.MaxFilter(2 * OL * s + 1))) > 127
        k1, k2 = int(22 * sc * s), int(26 * sc * s)
        below = np.zeros_like(full)
        below[:-k1] = full[k1:]
        above = np.zeros_like(full)
        above[k2:] = full[:-k2]
        rgb[ring] = INK
        rgb[full] = (240, 172, 204)
        rgb[full & below] = (226, 196, 230)
        rgb[full & ~above] = (250, 232, 244)
        alpha[ring] = 255
    return Image.fromarray(np.dstack([rgb, alpha]), 'RGBA').resize((W, H), Image.LANCZOS)


def skyline(ss=2):
    """The waterfront city on the horizon, hazy pinks far to dark mauve near, as an RGBA layer."""
    s = ss
    hy = HY
    lay = Image.new('RGBA', (W * s, H * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    ink = INK + (255,)

    def tower(x, w, h, col, steps=False):
        top = hy - h
        d.rectangle([x * s, top * s, (x + w) * s, (hy + 4) * s], fill=col + (255,), outline=ink, width=OL * s)
        if steps:
            for k, f in enumerate((0.8, 0.62, 0.45)):
                cw = w * f
                yy = top - 26 * (k + 1)
                d.rectangle([(x + (w - cw) / 2) * s, yy * s, (x + (w + cw) / 2) * s, (yy + 26) * s],
                            fill=col + (255,), outline=ink, width=OL * s)
            d.line([(x + w * 0.5) * s, (top - 140) * s, (x + w * 0.5) * s, (top - 78) * s], fill=ink, width=OL * s)
        lit = tuple(min(255, c + 14) for c in col) + (255,)
        for yy in np.arange(top + 20, hy - 14, 24):
            d.line([(x + 8) * s, yy * s, (x + w - 8) * s, yy * s], fill=lit, width=3 * s)

    far, mid, near = (234, 184, 206), (214, 158, 192), (190, 132, 176)
    d.ellipse([(SUNX - 46) * s, (hy - 70) * s, (SUNX + 46) * s, (hy + 22) * s], fill=(255, 250, 238, 255))
    for x, w, h in ((700, 90, 250), (420, 110, 340), (250, 80, 260)):
        tower(x, w, h, far)
    for x, w, h, st in ((-20, 120, 560, False), (95, 70, 470, False), (300, 150, 640, True), (470, 90, 380, False),
                        (960, 140, 600, False)):
        tower(x, w, h, mid, steps=st)
    tower(150, 90, 400, near)
    # the sun's path on the water: pale dashes, widening towards us
    rnd = random.Random(12)
    for k in range(46):
        u = (k / 46) ** 1.4
        yy = hy + 8 + u * 430 + rnd.uniform(-4, 4)
        half = 12 + u * 70
        x = SUNX - half * rnd.uniform(0.8, 1.2)
        while x < SUNX + half:                     # each row broken into a few dashes with gaps
            seg = half * rnd.uniform(0.25, 0.7)
            d.line([x * s, yy * s, min(x + seg, SUNX + half) * s, yy * s], fill=(255, 244, 230, 230),
                   width=int((2 + u * 5) * s))
            x += seg + half * rnd.uniform(0.1, 0.35)
    # the big wheel, right of the sun, backlit
    cx, cy, r = 790, hy - 190, 160
    wc = (150, 92, 140, 255)
    d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], outline=wc, width=6 * s)
    d.ellipse([(cx - r + 14) * s, (cy - r + 14) * s, (cx + r - 14) * s, (cy + r - 14) * s], outline=wc, width=3 * s)
    for k in range(24):
        a = 2 * math.pi * k / 24
        ex, ey = cx + math.cos(a) * r, cy + math.sin(a) * r
        d.line([cx * s, cy * s, ex * s, ey * s], fill=wc, width=2 * s)
        d.ellipse([(ex - 8) * s, (ey - 8) * s, (ex + 8) * s, (ey + 8) * s], fill=wc)
    d.line([((cx - 60) * s, hy * s), (cx * s, cy * s), ((cx + 60) * s, hy * s)], fill=wc, width=6 * s)
    # the waterfront: a dark low band, a pergola on the left, moored boats
    dark = (104, 58, 106, 255)
    d.rectangle([0, (hy - 34) * s, W * s, (hy + 6) * s], fill=dark)
    d.line([0, (hy - 34) * s, W * s, (hy - 34) * s], fill=ink, width=OL * s)
    px0, px1, ptop = 190, 420, hy - 120
    for px in np.linspace(px0, px1, 6):
        d.rectangle([(px - 6) * s, ptop * s, (px + 6) * s, (hy - 30) * s], fill=dark, outline=ink, width=2 * s)
    for k in range(3):
        yy = ptop - 4 + k * 12
        d.rectangle([(px0 - 20) * s, yy * s, (px1 + 20) * s, (yy + 8) * s], fill=dark, outline=ink, width=2 * s)
    boat = (236, 196, 214, 255)
    for bx, bw in ((20, 110), (150, 80), (470, 90), (860, 120)):
        d.polygon([(bx * s, (hy - 14) * s), ((bx + bw) * s, (hy - 14) * s), ((bx + bw - 14) * s, (hy + 4) * s),
                   ((bx + 10) * s, (hy + 4) * s)], fill=boat, outline=ink)
        d.rectangle([(bx + bw * 0.3) * s, (hy - 30) * s, (bx + bw * 0.6) * s, (hy - 14) * s],
                    fill=boat, outline=ink, width=2 * s)
    # the big tree, left of the sun
    rnd = random.Random(8)
    lumps = [(470 + rnd.uniform(-110, 110), hy - 170 + rnd.uniform(-70, 50), rnd.uniform(40, 70)) for _ in range(16)]
    tm = Image.new('L', lay.size, 0)
    _blob(ImageDraw.Draw(tm), lumps, 255, s)
    ImageDraw.Draw(tm).polygon([(455 * s, hy * s), (485 * s, hy * s), (478 * s, (hy - 140) * s),
                                (462 * s, (hy - 140) * s)], fill=255)
    lay.paste(ink, (0, 0), tm.filter(ImageFilter.MaxFilter(2 * OL * s + 1)))
    lay.paste((96, 52, 100, 255), (0, 0), tm)
    # palms, darkest, in front
    pc = (84, 44, 92, 255)
    for x, h, lean, sz in ((30, 260, 20, 1.1), (95, 220, -15, 1.0), (165, 250, 25, 1.1), (240, 200, -10, 0.9),
                           (575, 180, 15, 0.8), (690, 210, -20, 0.9), (740, 170, 10, 0.7), (900, 230, -25, 1.0),
                           (1050, 260, -35, 1.1)):
        _palm(d, x, hy + 2, h, lean, pc, s, sz)
    return lay.resize((W, H), Image.LANCZOS)


def _place(img, layer, scale, cx, cy, alpha, reveal=1.0):
    """Put layer at scale, centred on (cx, cy); reveal wipes it in from the top with a soft bottom edge."""
    if alpha <= 0 or reveal <= 0:
        return
    w, h = layer.size
    L = layer.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    a = np.asarray(L.getchannel('A')).astype(float) * alpha
    if reveal < 1:
        hh = L.size[1]
        edge = reveal * (hh + 160) - 160
        a = a * np.clip((edge + 160 - np.arange(hh)[:, None]) / 160, 0, 1)
    L.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(L, (int(cx - L.size[0] / 2), int(cy - L.size[1] / 2)))


def frame(t, LOGO, PALE, CITY):
    # the city: fades in 1.25-2.0 s, a slow push in all the way (the camera drifting forward over the water)
    city_a = _ease((t - 1.25) / 0.75)
    img = Image.new('RGBA', (W, H), DARK + (255,))
    if city_a > 0:
        push = 1.0 + 0.06 * (t - 1.25) / (DUR - 1.25)
        bg = S.paint(t).convert('RGBA')
        bg.alpha_composite(CITY)
        bw, bh = int(W * push), int(H * push)
        ox, oy = (bw - W) // 2, int((bh - H) * 0.58)
        bg = bg.resize((bw, bh), Image.LANCZOS).crop((ox, oy, ox + W, oy + H))
        img = Image.blend(img, bg, city_a)
    # the logo: wipes in top to bottom (0-0.3 s) while growing, keeps growing slowly, washes pale (2.0-2.4 s),
    # dissolves (2.35-2.85 s)
    reveal = _ease(t / 0.3) if t < 0.3 else 1.0
    scale = 0.86 + 0.08 * _ease(t / 0.6) + 0.05 * min(1, t / 2.85)
    a_out = 1 - _ease((t - 2.35) / 0.5)
    pale = _ease((t - 2.0) / 0.4)
    cx, cy = W / 2, 860
    _place(img, LOGO, scale, cx, cy, a_out * (1 - pale), reveal)
    _place(img, PALE, scale, cx, cy, a_out * pale, reveal)
    return img.convert('RGB')


def layers():
    L = logo()
    city = clouds()
    city.alpha_composite(skyline())
    return L, _pale(L), city


def main():
    out = sys.argv[1]
    small = '--small' in sys.argv
    L, P, C = layers()
    size = '540x960' if small else '1080x1920'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-vf', f'scale={size}', '-c:v', 'libx264', '-crf', '20',
                          '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(frame(i / FPS, L, P, C).tobytes())
    p.stdin.close()
    p.wait()


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'still':
        L, P, C = layers()
        for tt in map(float, sys.argv[3:]):
            frame(tt, L, P, C).resize((540, 960)).save(sys.argv[2].replace('.png', f'_{tt}.png'))
    else:
        main()
