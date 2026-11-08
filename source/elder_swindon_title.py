#!/usr/bin/env python3
"""elder_swindon_title: the teaser's end card over the roundabout (shot 6). Timings from Sam's teaser stills:
the picture dims (ours half way; the teaser goes to black) and gold rings bloom from 17.45 s; "The Elder Scrolls VI"
fades in 18.5-19.5 s with a thin rule under it; "SWINDON" burns in letter by letter with a glowing, ragged edge
22-27 s (Sam, 8 Nov: like SENTINEL), white-hot as it appears, gold, then cooled to dull bronze by 29 s.

MAP
- 25: timings and colours
- 40: the SWINDON letter masks (made once) and the burn
- 95: title(pil, t): dim, rings, small title, SWINDON
    python3 source/elder_swindon_title.py strip OUT.jpg     frames 17.5 .. 30 s on one strip (over the roundabout)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ed import INK                     # noqa: E402

T_RINGS, T_SMALL, T_BURN, T_BURN_END, T_COOL = 17.45, 18.5, 22.0, 27.0, 29.0
GOLD, HOT, BRONZE = np.array([228, 182, 108.]), np.array([255, 246, 210.]), np.array([150, 104, 58.])
CY = 450                               # the title's centre height: above the roundabout, so the island, traffic and e-bikes stay clear
FONT = os.path.join(HERE, 'fonts', 'Cinzel-Variable.ttf')
_M = {}


def sm(a, b, t):
    u = min(1.0, max(0.0, (t - a) / (b - a)))
    return u * u * (3 - 2 * u)


def _font(size, bold=True):
    f = ImageFont.truetype(FONT, size)
    if bold:
        try:
            f.set_variation_by_name('Bold')
        except Exception:
            pass
    return f


def _masks(w, h):
    """SWINDON as a fill mask and an outline mask, and each letter's span (x0, x1) on the canvas."""
    key = (w, h)
    if key in _M:
        return _M[key]
    k = w / 1080
    f = _font(int(178 * k))
    word = 'SWINDON'
    fill = Image.new('L', (w, h))
    edge = Image.new('L', (w, h))
    total = f.getlength(word)
    x = w / 2 - total / 2
    spans = []
    for ch in word:
        lw = f.getlength(ch)
        ImageDraw.Draw(fill).text((x, CY * k + 40 * k), ch, font=f, fill=255, anchor='lm')
        ImageDraw.Draw(edge).text((x, CY * k + 40 * k), ch, font=f, fill=255, anchor='lm', stroke_width=int(5 * k),
                                  stroke_fill=255)
        spans.append((x, x + lw))
        x += lw
    rng = np.random.default_rng(7)
    noise = Image.fromarray((rng.random((h // 8, w // 8)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    noise = np.asarray(noise.filter(ImageFilter.GaussianBlur(6 * k)), float) / 255
    noise = (noise - noise.mean()) / (noise.std() + 1e-6)
    _M[key] = (np.asarray(fill, float) / 255, np.asarray(edge, float) / 255, spans, noise)
    return _M[key]


def burn_progress(i, t):
    """Letter i's burn 0..1: each letter takes 1.2 s, starting 0.63 s apart, so the last ends at 27 s."""
    t0 = T_BURN + i * (T_BURN_END - T_BURN - 1.2) / 6
    return min(1.0, max(0.0, (t - t0) / 1.2)), t0


def title(pil, t):
    w, h = pil.size
    k = w / 1080
    if t < T_RINGS:
        return
    pil.alpha_composite(Image.new('RGBA', pil.size, (8, 6, 4, int(255 * 0.42 * sm(T_RINGS, T_RINGS + 1.2, t)))))
    # gold rings bloom outward from behind the title, then hang faint
    lay = Image.new('RGBA', pil.size)
    d = ImageDraw.Draw(lay)
    for n, (ox, oy, r) in enumerate(((-150, -60, 300), (170, -40, 280), (0, 160, 330), (-60, -260, 230), (120, 260, 260))):
        u = sm(T_RINGS + n * 0.18, T_RINGS + n * 0.18 + 1.6, t)
        if u <= 0:
            continue
        rr = r * (0.55 + 0.45 * u)
        a = int(255 * (0.25 + 0.75 * math.sin(math.pi * min(u, 1) * 0.5) * (1 - 0.45 * sm(T_RINGS + 2, T_RINGS + 5, t))))
        cx, cy = w / 2 + ox * k, CY * k + oy * k
        d.ellipse([cx - rr * k, cy - rr * k, cx + rr * k, cy + rr * k], outline=tuple(GOLD.astype(int)) + (a,),
                  width=max(1, int(3 * k)))
    glow = lay.filter(ImageFilter.GaussianBlur(6 * k))
    pil.alpha_composite(glow)
    pil.alpha_composite(lay)
    # The Elder Scrolls VI, small, with a thin rule
    a = sm(T_SMALL, T_SMALL + 1.0, t)
    if a > 0:
        lay = Image.new('RGBA', pil.size)
        d = ImageDraw.Draw(lay)
        col = tuple(GOLD.astype(int)) + (int(255 * a),)
        d.text((w / 2, CY * k - 120 * k), 'The Elder Scrolls VI', font=_font(int(52 * k), False), fill=col,
               anchor='mm', stroke_width=int(3 * k), stroke_fill=INK + (int(255 * a),))
        half = 240 * k * sm(T_SMALL, T_SMALL + 1.0, t)
        d.line([w / 2 - half, CY * k - 78 * k, w / 2 + half, CY * k - 78 * k], fill=col, width=max(1, int(3 * k)))
        pil.alpha_composite(lay)
    if t < T_BURN:
        return
    # SWINDON: each letter burns in from a ragged front; the front glows white-hot, the letter cools gold to bronze
    fill, edge, spans, noise = _masks(w, h)
    xs = np.arange(w, dtype=float)[None, :]
    reveal = np.zeros((h, w))
    front = np.zeros((h, w))
    heat = np.zeros((h, w))
    for i, (x0, x1) in enumerate(spans):
        p, t0 = burn_progress(i, t)
        if p <= 0:
            continue
        cols = slice(int(x0 - 10 * k), int(x1 + 10 * k))
        rel = (xs[:, cols] - x0) / (x1 - x0)                             # 0..1 across the letter
        field = rel * 0.75 + 0.18 * noise[:, cols] + 0.12             # burns left to right, ragged
        lvl = p * 1.25
        reveal[:, cols] = np.clip((lvl - field) / 0.05, 0, 1)
        front[:, cols] = np.clip(1 - np.abs(lvl - field) / 0.06, 0, 1) * (p < 1)
        age = t - t0 - 1.2 * (field.clip(0, 1) / 1.25)                 # seconds since this bit appeared
        heat[:, cols] = np.clip(1 - age / 1.6, 0, 1)
    cool = sm(T_BURN_END, T_COOL, t)
    base = GOLD * (1 - cool) + BRONZE * cool
    colr = base[None, None, :] * (1 - heat[..., None]) + HOT[None, None, :] * heat[..., None]
    a_fill = fill * reveal
    a_edge = np.clip(edge * reveal - a_fill, 0, 1)
    img = np.asarray(pil, float)
    rgb = img[..., :3]
    rgb = rgb * (1 - a_edge[..., None]) + np.array(INK, float)[None, None, :3] * a_edge[..., None]
    rgb = rgb * (1 - a_fill[..., None]) + colr * a_fill[..., None]
    # the glow: the burning front (and the hot letters) bloom orange
    g = np.clip(front * edge * 1.0 + heat * a_fill * 0.5 + (1 - cool) * a_fill * 0.12, 0, 1)
    gi = Image.fromarray((g * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10 * k))
    gl = np.asarray(gi, float)[..., None] / 255 * 1.6
    rgb = rgb + gl * np.array([255, 150, 50.])[None, None, :] * 0.9
    sp = np.asarray(Image.fromarray((front * edge * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2 * k)),
                    float)[..., None] / 255
    rgb = rgb * (1 - sp) + np.array([255, 236, 190.]) * sp
    img[..., :3] = np.clip(rgb, 0, 255)
    pil.paste(Image.fromarray(img.astype(np.uint8), 'RGBA'))


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'strip':
        import elder_swindon_aerial as A
        ts = [17.8, 19.0, 22.4, 23.6, 25.0, 26.4, 27.5, 29.5]
        tiles = []
        for t in ts:
            big = Image.new('RGBA', (1080 * A.SS, 1920 * A.SS))
            A.draw(big, A.held_cam(t), t)
            im = big.resize((1080, 1920), Image.LANCZOS)
            title(im, t)
            tiles.append(im.convert('RGB').resize((270, 480), Image.LANCZOS))
        sheet = Image.new('RGB', (270 * 4, 480 * 2))
        for i, tl in enumerate(tiles):
            ImageDraw.Draw(tl).text((6, 6), f'{ts[i]:.1f} s', fill=(255, 230, 120))
            sheet.paste(tl, ((i % 4) * 270, (i // 4) * 480))
        sheet.save(sys.argv[2], quality=88)
        print('strip:', sys.argv[2])
    else:
        print(__doc__)
