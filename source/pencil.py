#!/usr/bin/env python3
"""Turn a photo (or a video frame) into a graphite pencil drawing: clean contour lines, tone built from
hatching that follows the form (strands of hair, the curve of a cheek, the folds of a jumper), soft diagonal
hatching in the open areas, highlights left as bare paper, on a lightly grained sheet.

This is how the film's look would be made: real people filmed in a real room, every frame redrawn
in pencil, so the full 3D depth, light and weight of the scene survives into the drawing.

Usage:
    python3 pencil.py IN.jpg OUT.png [--height 1400] [--seed 1]
"""
import sys

import numpy as np
from PIL import Image


def blur(a, sigma):
    """Gaussian blur (done in the frequency domain, fast for any size)."""
    if sigma <= 0:
        return a
    h, w = a.shape
    ph, pw = h + int(4 * sigma), w + int(4 * sigma)
    p = np.pad(a, ((0, ph - h), (0, pw - w)), mode='reflect')
    fy = np.fft.fftfreq(ph)[:, None]
    fx = np.fft.rfftfreq(pw)[None, :]
    k = np.exp(-2 * (np.pi * sigma) ** 2 * (fx ** 2 + fy ** 2))
    return np.fft.irfft2(np.fft.rfft2(p) * k, (ph, pw))[:h, :w]


def sample(a, x, y):
    """Read the array at fractional positions (bilinear)."""
    h, w = a.shape
    x = np.clip(x, 0, w - 1.001)
    y = np.clip(y, 0, h - 1.001)
    x0, y0 = x.astype(int), y.astype(int)
    fx, fy = x - x0, y - y0
    return (a[y0, x0] * (1 - fx) * (1 - fy) + a[y0, x0 + 1] * fx * (1 - fy)
            + a[y0 + 1, x0] * (1 - fx) * fy + a[y0 + 1, x0 + 1] * fx * fy)


def flow_field(g, default_angle, scale):
    """Which way the pencil should travel at each point: along the edges and strands where the picture
    has a clear direction, and a steady diagonal where it doesn't."""
    s = blur(g, 1.2 * scale)
    gy, gx = np.gradient(s)
    jxx, jxy, jyy = (blur(v, 5 * scale) for v in (gx * gx, gx * gy, gy * gy))
    tr = jxx + jyy + 1e-9
    coh = np.sqrt((jxx - jyy) ** 2 + 4 * jxy ** 2) / tr  # 0 = no direction, 1 = strongly directional
    strength = np.clip(tr / (np.percentile(tr, 90) + 1e-9), 0, 1)
    wgt = np.clip(coh * 1.4, 0, 1) * strength ** 0.5
    # blend directions in 'double-angle' form so opposite-pointing strokes don't cancel out
    edge2 = np.arctan2(2 * jxy, jxx - jyy)  # double angle of the gradient
    tan2 = edge2 + np.pi  # tangent = gradient turned 90 degrees
    c2 = wgt * np.cos(tan2) + (1 - wgt) * np.cos(2 * default_angle)
    s2 = wgt * np.sin(tan2) + (1 - wgt) * np.sin(2 * default_angle)
    th = 0.5 * np.arctan2(s2, c2)
    return np.cos(th), np.sin(th)


def lic(noise, vx, vy, length):
    """Smear the noise along the flow: this is what turns random grain into pencil strokes."""
    h, w = noise.shape
    ys, xs = np.mgrid[0:h, 0:w].astype(float)
    acc = noise.copy()
    for sgn in (1, -1):
        x, y = xs.copy(), ys.copy()
        px, py = vx * sgn, vy * sgn
        for i in range(length):
            dx, dy = sample(vx, x, y), sample(vy, x, y)
            flip = np.sign(dx * px + dy * py)
            flip[flip == 0] = 1
            dx, dy = dx * flip, dy * flip
            x, y = x + dx, y + dy
            px, py = dx, dy
            acc += sample(noise, x, y) * (1 - i / length)
    return acc


def pencil(img, height=1400, seed=1):
    rng = np.random.default_rng(seed)
    im = img.convert('RGB')
    w = int(im.width * height / im.height)
    im = im.resize((w, height), Image.LANCZOS)
    a = np.asarray(im).astype(float) / 255
    g = a @ [0.3, 0.59, 0.11]
    scale = height / 1000

    # the tone the drawing aims for: paper-white highlights, deep hair, firm midtones
    lo, hi = np.percentile(g, 2), np.percentile(g, 98)
    t = np.clip((g - lo) / (hi - lo + 1e-9), 0, 1)
    t = blur(t, 0.8 * scale)
    t = np.clip(t + 0.7 * (t - blur(t, 30 * scale)), 0, 1)  # bring out the modelling: the turn of cheek, jaw, brow
    tone = np.clip(t * 1.08, 0, 1) ** 1.25
    dark = 1 - tone

    # contour lines: a 'colour dodge' of the picture against a blurred negative of itself
    inv = blur(1 - g, 3.5 * scale)
    lines = np.clip(g / (1 - inv + 1e-3), 0, 1)
    lines = np.clip((lines - 0.5) / 0.5, 0, 1) ** 1.5

    # two layers of strokes: one following the form, one crossing it for the deepest shadows
    vx, vy = flow_field(g, np.deg2rad(-58), scale)
    L = int(11 * scale)
    grain = blur(rng.random(g.shape), 0.7 * scale)
    s1 = lic(grain, vx, vy, L)
    grain2 = blur(rng.random(g.shape), 0.7 * scale)
    c, s = np.cos(np.deg2rad(55)), np.sin(np.deg2rad(55))
    s2 = lic(grain2, vx * c - vy * s, vx * s + vy * c, L)
    norm = lambda z: (z - z.mean()) / (z.std() + 1e-9)
    s1, s2 = norm(s1), norm(s2)
    # a stroke appears where the page needs to be darker than the stroke texture allows
    # graphite rubbed smooth for the soft gradations of skin, hatching laid over it as the tone deepens
    smudge = np.clip(blur(dark, 2.0 * scale), 0, 1) ** 1.1 * 0.66 * np.clip(0.82 + 0.18 * s1, 0.5, 1.2)
    m1 = np.clip((dark * 2.3 - 1.05 - s1 * 0.45) * 1.8, 0, 1) * np.clip((dark - 0.5) * 2.5, 0, 1)
    m2 = np.clip((dark * 2.4 - 1.75 - s2 * 0.45) * 2.0, 0, 1)
    fine = np.clip(0.5 + s1 * 0.5, 0, 1) * np.clip(dark * 3, 0, 1) * 0.05  # a fine grain in the midtones
    marks = 1 - (1 - smudge) * (1 - m1 * 0.6) * (1 - m2 * 0.6) * (1 - fine)

    # paper: warm white with a faint tooth
    tooth = blur(rng.standard_normal(g.shape), 0.6 * scale) * 0.025
    paper = 0.965 + tooth
    out = paper * (1 - marks * 0.94) * (0.4 + 0.6 * lines)
    out = out[4:-4, 4:-4]
    out = np.clip(out, 0, 1)
    rgb = np.stack([out * 1.0, out * 0.985, out * 0.96], -1)
    return Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8))


def main():
    args = sys.argv[1:]
    height = int(args[args.index('--height') + 1]) if '--height' in args else 1400
    seed = int(args[args.index('--seed') + 1]) if '--seed' in args else 1
    pencil(Image.open(args[0]), height, seed).save(args[1], optimize=True)
    print('saved', args[1])


if __name__ == '__main__':
    main()
