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

SUN = np.array([-0.80, 0.25, -0.48])                    # early evening (Sam, note 11): low golden sun, ~15 deg up
SUN = SUN / np.linalg.norm(SUN)
SUN_C = np.array([1.00, 0.70, 0.42])                     # golden evening sunlight (note 11)
SKY_C = np.array([0.38, 0.38, 0.48])                     # cool blue evening fill in the shadows

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
def _lod(scale, mpp):
    """How much of a noise octave to keep: features under about 3 pixels across fade out (no shimmer as the camera
    climbs)."""
    return np.clip((scale / np.maximum(mpp, 1e-9) - 3.0) / 4.0, 0, 1)


def soil(cam, ss=2, w=None, h=None, grass=0.55, seed=3, wet=None, t=0.0, gust=0.0, sun=None, rays=None):
    """The ground: dry brown soil, crumbs and clods, small stones, patchy dry grass, lit by a low warm sun.
    Returns an RGB float array (h, w, 3) in 0..1 and the height field (for things half buried).
    sun(X, Z) -> 0..1: how much sunlight reaches each point (a cast shadow, e.g. the lamp post's); rays: ground_rays
    already worked out for this frame; t, gust: the grass leaning in the wind."""
    w = w or B.W * ss
    h = h or B.H * ss
    X, Z, mpp = rays if rays is not None else ground_rays(cam, w, h, ss)
    # height: big swells, clods, crumbs, grain (metres); the octaves too fine for the pixels fade out
    H = (0.012 * noise(X, Z, 0.9, seed) + 0.006 * noise(X, Z, 0.22, seed + 1)
         + 0.0025 * _lod(0.06, mpp) * np.abs(noise(X, Z, 0.06, seed + 2))
         + 0.0009 * _lod(0.015, mpp) * noise(X, Z, 0.015, seed + 3)
         + 0.0004 * _lod(0.004, mpp) * noise(X, Z, 0.004, seed + 4))
    # stones: bumps where a fine noise peaks
    st = noise(X, Z, 0.05, seed + 7)
    stones = np.clip((st - 2.1) * 3.0, 0, 1) * _lod(0.02, mpp)
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
    lit = lam * sh * (sun(X, Z) if sun is not None else 1.0)
    col = alb * (SKY_C * 0.55 + SUN_C * 1.25 * lit[..., None])
    img = np.clip(col, 0, 1)
    if grass > 0:
        img = _grass(img, X, Z, mpp, cam, ss, grass, seed, t, gust)
    return img, H


_BLADES = {}
GRASS_MASK = None                                        # f(x, z) -> where grass may grow (the film sets it)
GRASS_AREA = (-5.0, -5.0, 5.0, 5.0)                      # the world area grass can grow in (x0, z0, x1, z1), metres


def _blades(amount, seed):
    """Every blade of grass in the world, made once (so a moving camera never re-scatters them): base (x, z), length,
    lean (radians from the wind, -z), bend, straw shade, all in metres; kept where the patch noise allows."""
    key = (round(amount, 3), seed)
    if key not in _BLADES:
        rng = np.random.default_rng(seed + 11)
        x0, z0, x1, z1 = GRASS_AREA
        n = int((x1 - x0) * (z1 - z0) * 0.9 * amount / 0.012 ** 2)
        x = rng.uniform(x0, x1, n)
        z = rng.uniform(z0, z1, n)
        patch = noise(x, z, 0.5, seed + 12) + 0.5 * noise(x, z, 0.12, seed + 13)
        keep = patch > (1.0 - amount * 1.6)
        if GRASS_MASK is not None:
            keep &= GRASS_MASK(x, z)
        m = int(keep.sum())
        _BLADES[key] = dict(x=x[keep], z=z[keep], L=rng.uniform(0.025, 0.08, m), ang=rng.normal(0.0, 0.5, m),
                            bend=rng.normal(0, 0.25, m), g=rng.uniform(0, 1, m), ph=rng.uniform(0, 6.28, m))
    return _BLADES[key]


def project_many(cam, P):
    """sets.Cam.project for many world points (N x 3): frame x, y (1080 x 1920 units) and pixels per metre."""
    d = P - np.asarray(cam.pos, float)
    z = np.maximum(cam.NEAR, d @ np.asarray(cam.f, float))
    k = cam.focal / z
    return 540 + (d @ np.asarray(cam.r, float)) * k, 960 - (d @ np.asarray(cam.u, float)) * k, k


def _grass(img, X, Z, mpp, cam, ss, amount, seed, t=0.0, gust=0.0):
    """Patchy dry grass: blades lying mostly with the wind, olive to straw, a lit side and a shadow on the soil.
    The blades live in the world (_blades), so they stay put as the camera moves; they sway a little in the gusts.
    Too small to see (under 2 pixels long): left as a tint of the patch instead."""
    h, w, _ = img.shape
    bl = _blades(amount, seed)
    xa, xb, za, zb = X.min(), X.max(), Z.min(), Z.max()
    sel = (bl['x'] > xa - 0.1) & (bl['x'] < xb + 0.1) & (bl['z'] > za - 0.1) & (bl['z'] < zb + 0.1)
    idx = np.nonzero(sel)[0]
    m_med = float(np.median(mpp))
    if len(idx) == 0:
        return img
    if 0.05 / m_med < 2.0 or len(idx) > 150000:         # too small to draw blade by blade: a straw tint
        patch = noise(X, Z, 0.5, seed + 12) + 0.5 * noise(X, Z, 0.12, seed + 13)
        a = np.clip((patch - (1.0 - amount * 1.6)) * 0.8, 0, 0.55)
        if a.shape != (h, w):
            a = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize((w, h)), float) / 255
        return img * (1 - a[..., None]) + np.array([0.52, 0.50, 0.28]) * a[..., None]
    x, z, L = bl['x'][idx], bl['z'][idx], bl['L'][idx]
    sway = 0.25 * gust * np.sin(t * 6.0 + bl['ph'][idx]) + 0.35 * gust
    ang = bl['ang'][idx]
    dx, dz = np.sin(ang), -np.cos(ang)                   # leaning with the wind (-z), some every way
    bend = bl['bend'][idx]
    tipx = x + dx * L - dz * bend * L * 0.3
    tipz = z + dz * L + dx * bend * L * 0.3 - sway * L * 0.4
    midx, midz = x + dx * L * 0.5 - dz * bend * L * 0.25, z + dz * L * 0.5 + dx * bend * L * 0.25 - sway * L * 0.15
    y0, y1, y2 = np.full_like(x, 0.002), np.full_like(x, 0.006), np.full_like(x, 0.004)
    P = np.concatenate([np.stack([x, y0, z], 1), np.stack([midx, y1, midz], 1), np.stack([tipx, y2, tipz], 1)])
    sx, sy, kk = project_many(cam, P)
    n = len(x)
    sx, sy, kk = sx * ss, sy * ss, kk * ss
    sun_xz = np.array([-0.857, -0.514])
    lit = 0.75 + 0.5 * np.maximum(0.0, dx * sun_xz[0] + dz * sun_xz[1])
    g = bl['g'][idx]
    c0 = np.array([0.42, 0.44, 0.20])[None, :] * (1 - g)[:, None] + np.array([0.78, 0.68, 0.40])[None, :] * g[:, None]
    cols = (np.clip(c0 * lit[:, None], 0, 1) * 255).astype(int)
    wd = np.maximum(1, np.round(0.0022 * kk[:n])).astype(int)
    off = 0.006 * kk[:n]
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    shd = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(lay)
    ds = ImageDraw.Draw(shd)
    onscr = (sx[:n] > -50) & (sx[:n] < w + 50) & (sy[:n] > -50) & (sy[:n] < h + 50)
    for j in np.nonzero(onscr)[0]:
        pts = [(sx[j], sy[j]), (sx[n + j], sy[n + j]), (sx[2 * n + j], sy[2 * n + j])]
        o = off[j]
        ds.line([(px + o, py + o * 0.6) for px, py in pts], fill=150, width=int(wd[j]) + 1)
        d.line(pts, fill=(int(cols[j, 0]), int(cols[j, 1]), int(cols[j, 2]), 255), width=int(wd[j]))
    shd = np.asarray(shd.filter(ImageFilter.GaussianBlur(1.5 * ss)), float)[..., None] / 255
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
def dust(img, cam, ss, t, strength=1.0, seed=21, rays=None, gust=None):
    """Wind-blown dust: fine streaks drifting with the wind (-z), brighter in the sun (the teaser's sand).
    gust: 0..1 how hard the wind blows now (None: a gentle swell); a gust thickens and speeds the streaks."""
    h, w, _ = img.shape
    X, Z, mpp = rays if rays is not None else ground_rays(cam, w, h, ss)
    wind = 0.9                                           # metres a second, towards -z
    s = noise(X * 16.0, Z + wind * t, 0.30, seed) + 0.7 * noise(X * 28.0, Z + wind * 1.7 * t, 0.12, seed + 1)
    g = (0.6 + 0.4 * math.sin(t * 1.3) ** 2) if gust is None else 0.55 + 0.8 * gust
    a = np.clip((s - 1.0 + 0.4 * (g - 0.6)) * 0.20, 0, 0.30 + 0.08 * max(0.0, g - 1.0)) * min(g, 1.1) * strength
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
