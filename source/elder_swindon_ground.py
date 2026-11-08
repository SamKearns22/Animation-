#!/usr/bin/env python3
"""elder_swindon_ground: the near-real ground for Elder Scrolls: Swindon (rule 61 MAP below).

MAP
- 30: noise textures (tileable, world-anchored, so a moving camera never swims)
- 60: ground_rays: the ground point under every pixel of a sets.Cam frame
- 75: soil: soil colour, height, low warm sun, grass, stones, litter (cigarette butts, ring-pull)
- 170: dust: wind-blown dust streaks drifting with the wind
- 195: shade_cyl: near-real shading of a lying cylinder (can, scroll pieces)

Near-real on purpose (Sam's brief: the opening as moody and realistic as possible): textures and soft light, no
outlines. Everything here is in metres on the floor (y = 0), seen through sets.Cam, drawn onto burnham.canvas (SS).
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B  # noqa: E402

SUN = np.array([-0.80, 0.36, -0.48])                    # low warm sun from screen left and above (elevation ~21 deg)
SUN = SUN / np.linalg.norm(SUN)
SUN_C = np.array([1.00, 0.80, 0.58])                     # warm sunlight
SKY_C = np.array([0.42, 0.40, 0.44])                     # cool fill in the shadows

# ------------------------------------------------------------------------------------------------ noise
_TEX = {}


FEAT = 12.0                                              # texture pixels per noise feature (a tile repeats every
N_TILE = 1024                                            # 85 features, and each octave is turned: no visible grid)


def _tile(seed, n=N_TILE):
    """A tileable noise texture (n x n), features about FEAT pixels across: FFT-filtered white noise."""
    key = (seed, n)
    if key not in _TEX:
        r = np.random.default_rng(seed).standard_normal((n, n))
        f = np.fft.fftfreq(n)
        fx, fy = np.meshgrid(f, f)
        k = np.sqrt(fx ** 2 + fy ** 2)
        filt = np.exp(-(k * FEAT * 1.6) ** 2) * (k > 0)
        t = np.real(np.fft.ifft2(np.fft.fft2(r) * filt))
        _TEX[key] = (t - t.mean()) / (t.std() + 1e-9)
    return _TEX[key]


def noise(x, z, scale, seed):
    """World-anchored noise (about unit spread) with features about `scale` metres across."""
    t = _tile(seed)
    n = t.shape[0]
    a = (seed * 2.399) % (2 * math.pi)                   # each seed's grid turned its own way
    ca, sa = math.cos(a), math.sin(a)
    u = (ca * x - sa * z) / scale * FEAT + seed * 37.0
    v = (sa * x + ca * z) / scale * FEAT + seed * 53.0
    return ndimage.map_coordinates(t, [v.ravel() % n, u.ravel() % n], order=1, mode='grid-wrap').reshape(x.shape)


# ------------------------------------------------------------------------------------------------ rays
def ground_rays(cam, w, h, ss):
    """World (x, z) on the floor under every pixel (w x h canvas at ss times the 1080 x 1920 frame), and metres
    per canvas pixel there."""
    px, py = np.meshgrid((np.arange(w) + 0.5) / ss, (np.arange(h) + 0.5) / ss)
    f, r, u = (np.asarray(v, float) for v in (cam.f, cam.r, cam.u))
    d = f[None, None, :] + ((px - 540) / cam.focal)[..., None] * r - ((py - 960) / cam.focal)[..., None] * u
    pos = np.asarray(cam.pos, float)
    t = -pos[1] / np.minimum(d[..., 1], -1e-6)
    X = pos[0] + t * d[..., 0]
    Z = pos[2] + t * d[..., 2]
    mpp = t * np.linalg.norm(d, axis=-1) / cam.focal / ss
    return X, Z, mpp


# ------------------------------------------------------------------------------------------------ soil
def soil(cam, ss=2, w=None, h=None, grass=0.55, seed=3, wet=None):
    """The ground: dry brown soil, crumbs and clods, small stones, patchy dry grass, lit by a low warm sun.
    Returns an RGB float array (h, w, 3) in 0..1 and the height field (for things half buried)."""
    w = w or B.W * ss
    h = h or B.H * ss
    X, Z, mpp = ground_rays(cam, w, h, ss)
    # height: big swells, clods, crumbs, grain (metres)
    H = (0.012 * noise(X, Z, 0.9, seed) + 0.006 * noise(X, Z, 0.22, seed + 1)
         + 0.0025 * np.abs(noise(X, Z, 0.06, seed + 2)) + 0.0009 * noise(X, Z, 0.015, seed + 3)
         + 0.0004 * noise(X, Z, 0.004, seed + 4))
    # stones: bumps where a fine noise peaks
    st = noise(X, Z, 0.05, seed + 7)
    stones = np.clip((st - 2.1) * 3.0, 0, 1)
    H = H + 0.008 * stones
    gy, gx = np.gradient(H)
    mp = np.maximum(mpp, 1e-6)
    nx, nz = -gx / mp, -gy / mp
    # screen gradient to world: screen x runs along cam.r, screen y down along -u (projected on the floor)
    r = np.asarray(cam.r, float)
    u = np.asarray(cam.u, float)
    ux, uz = -u[0], -u[2]
    rn = math.hypot(r[0], r[2]) or 1
    un = math.hypot(ux, uz) or 1
    wx = nx * r[0] / rn + nz * ux / un
    wz = nx * r[2] / rn + nz * uz / un
    N = np.stack([wx, np.ones_like(wx), wz], -1)
    N /= np.linalg.norm(N, axis=-1, keepdims=True)
    lam = np.clip(N @ SUN, 0, 1)
    # cast shadow of the bumps (cheap: darken where the height drops towards the sun)
    sh = np.clip(1.0 - 18.0 * np.clip(-(N @ SUN) + 0.15, 0, 1), 0.25, 1.0)
    base_dark = np.array([0.24, 0.19, 0.15])
    base_light = np.array([0.50, 0.42, 0.33])
    mix = np.clip(0.5 + 0.35 * noise(X, Z, 0.35, seed + 5) + 0.15 * noise(X, Z, 0.03, seed + 6), 0, 1)
    alb = base_dark * (1 - mix[..., None]) + base_light * mix[..., None]
    stone_c = np.array([0.55, 0.52, 0.48]) + 0.08 * noise(X, Z, 0.02, seed + 9)[..., None]
    alb = alb * (1 - stones[..., None]) + stone_c * stones[..., None]
    if wet is not None:                                  # a darker damp patch (the drool)
        alb = alb * (1 - 0.45 * wet[..., None])
    col = alb * (SKY_C * 0.55 + SUN_C * 1.25 * (lam * sh)[..., None])
    img = np.clip(col, 0, 1)
    if grass > 0:
        img = _grass(img, X, Z, mpp, cam, ss, grass, seed)
    return img, H


def _grass(img, X, Z, mpp, cam, ss, amount, seed):
    """Patchy dry grass: blades lying mostly with the wind, olive to straw, a lit side and a shadow on the soil."""
    h, w, _ = img.shape
    rng = np.random.default_rng(seed + 11)
    patch = noise(X, Z, 0.5, seed + 12) + 0.5 * noise(X, Z, 0.12, seed + 13)
    m_med = float(np.median(mpp))
    n = int(min(60000, (w * h) * amount / max(1.0, (0.012 / m_med) ** 2) * 0.9))
    ys = rng.integers(0, h, n)
    xs = rng.integers(0, w, n)
    keep = patch[ys, xs] > (1.0 - amount * 1.6)
    ys, xs = ys[keep], xs[keep]
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    shd = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(lay)
    ds = ImageDraw.Draw(shd)
    for x, y in zip(xs, ys):
        L_m = rng.uniform(0.025, 0.08)
        L = L_m / mpp[y, x]
        ang = rng.normal(0.25, 0.5)                      # leaning with the wind (to screen right), some every way
        dx, dy = math.cos(ang) * L, math.sin(ang) * L
        bend = rng.normal(0, 0.25) * L
        mid = (x + dx * 0.5 - dy * bend / L * 0.3, y + dy * 0.5 + dx * bend / L * 0.3)
        tip = (x + dx, y + dy)
        g = rng.uniform(0, 1)
        c0 = np.array([0.42, 0.44, 0.20]) * (1 - g) + np.array([0.78, 0.68, 0.40]) * g
        lit = 0.75 + 0.5 * max(0.0, -math.cos(ang))      # blades facing the sun catch it
        c = tuple(int(255 * min(1, v * lit)) for v in c0) + (255,)
        wd = max(1, int(round(0.0022 / mpp[y, x])))
        d.line([(x, y), mid, tip], fill=c, width=wd)
        off = 0.006 / mpp[y, x]
        ds.line([(x + off, y + off * 0.6), (mid[0] + off, mid[1] + off * 0.6), (tip[0] + off, tip[1] + off * 0.6)],
                fill=150, width=wd + 1)
    shd = np.asarray(shd.filter(ImageFilter.GaussianBlur(1.5)), float)[..., None] / 255
    img = img * (1 - 0.45 * shd)
    la = np.asarray(lay, float) / 255
    a = la[..., 3:4]
    return img * (1 - a) + la[..., :3] * a


def litter(img, cam, ss, items):
    """Cigarette butts and ring-pulls on the soil: [(kind, x, z, angle_deg)]. Near-real, soft shadow."""
    pil = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    sh = Image.new('L', pil.size, 0)
    d = ImageDraw.Draw(pil)
    ds = ImageDraw.Draw(sh)
    for kind, x, z, a in items:
        (cx, cy), k = cam.project((x, 0.004, z))
        cx, cy, k = cx * ss, cy * ss, k * ss
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        if kind == 'butt':
            L, Wd = 0.026 * k, 0.0078 * k
            p0 = (cx - ca * L / 2, cy - sa * L / 2)
            p1 = (cx + ca * L / 2, cy + sa * L / 2)
            pm = (cx + ca * L * 0.1, cy + sa * L * 0.1)
            ds.line([(p0[0] + 3, p0[1] + 2), (p1[0] + 3, p1[1] + 2)], fill=170, width=int(Wd))
            d.line([p0, pm], fill=(196, 132, 70), width=int(Wd))        # the cork-coloured filter
            d.line([pm, p1], fill=(228, 222, 210), width=int(Wd))       # the paper
            d.ellipse([p1[0] - Wd / 2, p1[1] - Wd / 2, p1[0] + Wd / 2, p1[1] + Wd / 2], fill=(70, 62, 56))
        elif kind == 'ringpull':
            R = 0.011 * k
            ds.ellipse([cx - R + 3, cy - R * 0.7 + 2, cx + R + 3, cy + R * 0.7 + 2], outline=160, width=max(2, int(R / 4)))
            d.ellipse([cx - R, cy - R * 0.7, cx + R, cy + R * 0.7], outline=(176, 178, 184), width=max(2, int(R / 4)))
            d.ellipse([cx - R * 0.45 + ca * R, cy - R * 0.35, cx + R * 0.45 + ca * R, cy + R * 0.35],
                      outline=(210, 212, 218), width=max(1, int(R / 6)))
    sh = np.asarray(sh.filter(ImageFilter.GaussianBlur(3)), float)[..., None] / 255
    out = np.asarray(pil, float) / 255
    return out * (1 - 0.35 * sh * (out.mean(-1, keepdims=True) < 0.75))


# ------------------------------------------------------------------------------------------------ dust
def dust(img, cam, ss, t, strength=1.0, seed=21):
    """Wind-blown dust: fine streaks drifting to screen right with the wind, brighter in the sun (the teaser's sand)."""
    h, w, _ = img.shape
    X, Z, mpp = ground_rays(cam, w, h, ss)
    wind = 0.9                                           # metres a second, towards -z (screen right in the low shots)
    s = noise(X * 16.0, Z + wind * t, 0.30, seed) + 0.7 * noise(X * 28.0, Z + wind * 1.7 * t, 0.12, seed + 1)
    gust = 0.6 + 0.4 * math.sin(t * 1.3) ** 2
    a = np.clip((s - 1.0) * 0.22, 0, 0.32) * gust * strength
    c = np.array([0.86, 0.72, 0.52])
    return img * (1 - a[..., None]) + c * a[..., None]


# ------------------------------------------------------------------------------------------------ props
def shade_cyl(nrm, base, spec=0.0, metal=False):
    """Near-real shading across a cylinder: nrm runs -1..1 across its width (screen); the sun from screen left."""
    c = np.sqrt(np.clip(1 - nrm ** 2, 0, 1))
    lam = np.clip(0.55 * c - 0.6 * nrm * 0.8 + 0.25, 0, 1)
    out = np.asarray(base, float)[None, :] * (0.35 + 0.95 * lam)[:, None]
    if metal:
        band = np.exp(-((nrm + 0.38) / 0.12) ** 2) * spec + np.exp(-((nrm - 0.55) / 0.08) ** 2) * spec * 0.35
        out = out * (0.55 + 0.45 * c)[:, None] + np.array([1.0, 0.92, 0.70])[None, :] * band[:, None]
    else:
        out = out + np.exp(-((nrm + 0.42) / 0.10) ** 2)[:, None] * spec
    return np.clip(out, 0, 1)
