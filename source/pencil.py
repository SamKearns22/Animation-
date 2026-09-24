#!/usr/bin/env python3
"""Coloured-pencil drawing toolkit shared by the animations in this project.

Draws shapes onto a paper texture so they look like coloured pencil, and
turns a sequence of drawings plus a sound track into an MP4 video.
"""
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
FPS = 12
M = 120  # margin so the pencil grain can be shifted each drawing
NG = 3   # number of pencil grain directions


# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
def col(r, g, b):
    return np.array([r, g, b], np.float32)


PAPER = col(0.97, 0.95, 0.90)
WHITE = col(1.0, 1.0, 1.0)
BROWN = col(0.58, 0.37, 0.21)
BROWN_D = col(0.33, 0.19, 0.10)
TAN = col(0.88, 0.72, 0.52)
TEETH = col(0.99, 0.84, 0.50)
NOSE = col(0.18, 0.11, 0.10)
INK = col(0.12, 0.10, 0.10)
PINK = col(0.96, 0.58, 0.60)
MOUTH = col(0.40, 0.12, 0.14)
SKY = col(0.78, 0.89, 0.97)
GREEN_F = col(0.50, 0.66, 0.55)
GREEN_G = col(0.55, 0.72, 0.38)
GREEN1 = col(0.42, 0.66, 0.32)
GREEN2 = col(0.24, 0.47, 0.26)
GREEN_L = col(0.62, 0.80, 0.34)
TRUNK = col(0.50, 0.33, 0.20)
WATER = col(0.48, 0.70, 0.88)
WATER_D = col(0.25, 0.47, 0.74)
MUD = col(0.47, 0.31, 0.18)
STICKS = [col(0.55, 0.38, 0.22), col(0.40, 0.25, 0.14), col(0.66, 0.48, 0.30)]
FIRE_Y = col(1.0, 0.88, 0.30)
FIRE_O = col(0.99, 0.56, 0.14)
FIRE_R = col(0.86, 0.22, 0.10)
SPACE = col(0.09, 0.11, 0.24)
ROCK = col(0.50, 0.44, 0.41)
ROCK_D = col(0.29, 0.25, 0.25)
ROCK_B = col(0.45, 0.32, 0.26)
SMOKE = col(0.62, 0.62, 0.64)
PUFF = col(0.96, 0.96, 0.97)
SOOT = col(0.16, 0.14, 0.14)
OCEAN = col(0.26, 0.47, 0.80)
OCEAN_D = col(0.14, 0.28, 0.58)
ATMOS = col(0.62, 0.82, 1.0)
DESERT = col(0.80, 0.68, 0.42)
LIGHT = col(1.0, 0.95, 0.72)


# ---------------------------------------------------------------------------
# Paper and pencil grain (made once)
# ---------------------------------------------------------------------------
def _uniform(a, rng):
    s = rng.choice(a.ravel(), 200000)
    q = np.quantile(s, np.linspace(0, 1, 257))
    return np.interp(a, q, np.linspace(0, 1, 257)).astype(np.float32)


def _make_grain(angle, seed):
    r = np.random.default_rng(seed)
    gh, gw = H + 2 * M, W + 2 * M
    big = int(math.hypot(gw, gh)) + 8
    small = r.random((big // 3, big // 12)).astype(np.float32)
    im = Image.fromarray((small * 255).astype(np.uint8)).resize((big, big), Image.BILINEAR)
    im = im.rotate(angle, resample=Image.BILINEAR)
    a = np.asarray(im, np.float32) / 255
    y0, x0 = (big - gh) // 2, (big - gw) // 2
    a = a[y0:y0 + gh, x0:x0 + gw]
    return _uniform(a, r)


_r0 = np.random.default_rng(7)
GRAIN = [_make_grain(a, 11 + i) for i, a in enumerate((32, -38, 78))]
_tooth = Image.fromarray((_r0.random((H, W)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.8))
TOOTH = _uniform(np.asarray(_tooth, np.float32), _r0)
_mottle = np.asarray(Image.fromarray((_r0.random((H // 80, W // 80)) * 255).astype(np.uint8))
                     .resize((W, H), Image.BICUBIC), np.float32) / 255
PAPER_IMG = (PAPER[None, None, :] * (1 - 0.05 * (TOOTH - 0.5) - 0.035 * (_mottle - 0.5))[..., None]).astype(np.float32)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def clamp01(x):
    return max(0.0, min(1.0, x))


def sstep(a, b, x):
    t = clamp01((x - a) / (b - a))
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def ell(cx, cy, rx, ry, rot=0.0, n=40):
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x, y = rx * np.cos(th), ry * np.sin(th)
    if rot:
        a = math.radians(rot)
        ca, sa = math.cos(a), math.sin(a)
        x, y = x * ca - y * sa, x * sa + y * ca
    return np.stack([cx + x, cy + y], 1)


def blob(cx, cy, r, seed, n=36, amt=0.18):
    rr = np.random.default_rng(seed)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    rad = np.ones(n)
    for k in range(2, 6):
        rad += rr.uniform(-amt, amt) / k * 2 * np.cos(k * th + rr.uniform(0, 6.3))
    return np.stack([cx + r * rad * np.cos(th), cy + r * rad * np.sin(th)], 1)


# ---------------------------------------------------------------------------
# Canvas: draws shapes that look like coloured pencil
# ---------------------------------------------------------------------------
class Canvas:
    def __init__(self, d):
        self.d = d
        self.n = 0
        self.img = PAPER_IMG.copy()
        self.cam = (1.0, 0.0, 0.0)
        r = np.random.default_rng(1000 + d // 4)  # pencil texture shifts 3 times a second
        self.goff = [(int(r.integers(0, 2 * M)), int(r.integers(0, 2 * M))) for _ in range(NG)]

    def rng(self):
        self.n += 1
        return np.random.default_rng(((self.d // 2) * 7919 + self.n * 104729) % (2 ** 32))  # lines wobble 6 times a second

    def scr(self, pts):
        s, ox, oy = self.cam
        return np.asarray(pts, np.float64) * s + np.array([ox, oy])

    @staticmethod
    def jitter(p, amp, r):
        n = len(p)
        if n < 2 or amp <= 0:
            return p
        k = max(4, n // 5)
        ctrl = r.normal(0, amp, (k, 2))
        idx = np.linspace(0, k, n, endpoint=False)
        i0 = np.floor(idx).astype(int) % k
        i1 = (i0 + 1) % k
        f = (idx - np.floor(idx))[:, None]
        f = f * f * (3 - 2 * f)
        return p + ctrl[i0] * (1 - f) + ctrl[i1] * f

    def _box(self, p, pad):
        x0 = int(max(0, math.floor(p[:, 0].min()) - pad))
        x1 = int(min(W, math.ceil(p[:, 0].max()) + pad))
        y0 = int(max(0, math.floor(p[:, 1].min()) - pad))
        y1 = int(min(H, math.ceil(p[:, 1].max()) + pad))
        if x1 - x0 < 1 or y1 - y0 < 1:
            return None
        return x0, y0, x1, y1

    def _mask(self, p, width=0, closed=True):
        b = self._box(p, width + 3)
        if b is None:
            return None
        x0, y0, x1, y1 = b
        im = Image.new('L', (x1 - x0, y1 - y0), 0)
        dr = ImageDraw.Draw(im)
        q = [(float(x - x0), float(y - y0)) for x, y in p]
        if width == 0:
            if len(q) >= 3:
                dr.polygon(q, fill=255)
        else:
            if closed:
                q = q + [q[0]]
            dr.line(q, fill=255, width=int(width), joint='curve')
            r = width / 2
            for (x, y) in (q[0], q[-1]):
                dr.ellipse((x - r, y - r, x + r, y + r), fill=255)
        return np.asarray(im, np.float32) / 255, x0, y0

    def _apply(self, m, x0, y0, color, pressure, opacity, gi):
        h, w = m.shape
        ox, oy = self.goff[gi]
        g = GRAIN[gi][oy + y0:oy + y0 + h, ox + x0:ox + x0 + w]
        t = TOOTH[y0:y0 + h, x0:x0 + w]
        cov = np.clip((0.78 * g + 0.22 * t - (1 - pressure)) * 3.2, 0, 1)
        a = (m * cov * opacity)[..., None]
        reg = self.img[y0:y0 + h, x0:x0 + w]
        reg += (color - reg) * a

    def poly(self, pts, fill=None, line=None, lw=5, pressure=0.85, lp=0.95,
             jit=2.2, opacity=1.0, closed=True, grain=None):
        if opacity <= 0.003:
            return
        r = self.rng()
        p = self.jitter(self.scr(pts), jit, r)
        gi = int(r.integers(0, NG)) if grain is None else grain
        if fill is not None and closed:
            res = self._mask(p)
            if res is not None:
                self._apply(*res, fill, pressure, opacity, gi)
        if line is not None:
            w = max(1.5, lw * self.cam[0])
            res = self._mask(p, width=int(round(w)), closed=closed)
            if res is not None:
                self._apply(*res, line, lp, opacity, (gi + 1) % NG)

    def line(self, pts, color, lw=5, pressure=0.9, jit=1.5, opacity=1.0):
        self.poly(pts, None, color, lw=lw, lp=pressure, jit=jit, opacity=opacity, closed=False)

    def hatch(self, pts, color, spacing=16, angle=45, lw=3, pressure=0.8, opacity=1.0):
        r = self.rng()
        p = self.jitter(self.scr(pts), 2.0, r)
        res = self._mask(p)
        if res is None:
            return
        m, x0, y0 = res
        h, w = m.shape
        im = Image.new('L', (w, h), 0)
        dr = ImageDraw.Draw(im)
        a = math.radians(angle)
        dx, dy = math.cos(a), math.sin(a)
        nx, ny = -dy, dx
        L = w + h
        sp = max(5.0, spacing * self.cam[0])
        cx, cy = w / 2, h / 2
        for off in np.arange(-L, L, sp):
            o = off + r.normal(0, sp * 0.12)
            px, py = cx + nx * o, cy + ny * o
            dr.line([(px - dx * L, py - dy * L), (px + dx * L, py + dy * L)], fill=255,
                    width=max(1, int(round(lw * max(0.5, self.cam[0])))))
        lm = np.asarray(im, np.float32) / 255
        self._apply(m * lm, x0, y0, color, pressure, opacity, int(r.integers(0, NG)))

    def strokes(self, arr, color, width, pressure=0.9, opacity=1.0, boil=0.5, clip=None):
        """Draw many short pencil strokes at once. arr has shape (N, k, 2) in world units."""
        if opacity <= 0.003 or len(arr) == 0:
            return
        s, ox, oy = self.cam
        p = np.asarray(arr, np.float64) * s + np.array([ox, oy])
        b = self._box(p.reshape(-1, 2), width * s + 4)
        if b is None:
            return
        x0, y0, x1, y1 = b
        r = self.rng()
        if boil > 0:
            p = p + r.normal(0, boil, (p.shape[0], 1, 2))
        p = p - np.array([x0, y0])
        im = Image.new('L', (x1 - x0, y1 - y0), 0)
        dr = ImageDraw.Draw(im)
        w = max(1, int(round(width * s)))
        for ln in p:
            if ln[:, 0].max() < -w or ln[:, 1].max() < -w or ln[:, 0].min() > x1 - x0 + w or ln[:, 1].min() > y1 - y0 + w:
                continue
            dr.line([tuple(q) for q in ln], fill=255, width=w, joint='curve')
        m = np.asarray(im, np.float32) / 255
        if clip is not None:
            cm = Image.new('L', (x1 - x0, y1 - y0), 0)
            cd = ImageDraw.Draw(cm)
            for poly in clip:
                q = np.asarray(poly, np.float64) * s + np.array([ox - x0, oy - y0])
                cd.polygon([tuple(v) for v in q], fill=255)
            m = m * (np.asarray(cm, np.float32) / 255)
        self._apply(m, x0, y0, color, pressure, opacity, int(r.integers(0, NG)))

    def fill_screen(self, color, pressure=0.9, opacity=1.0):
        gi = int(self.rng().integers(0, NG))
        self._apply(np.ones((H, W), np.float32), 0, 0, color, pressure, opacity, gi)

    def _blend(self, a, x0, y0, color, textured=True):
        h, w = a.shape
        if textured:
            ox, oy = self.goff[0]
            a = a * (0.7 + 0.3 * GRAIN[0][oy + y0:oy + y0 + h, ox + x0:ox + x0 + w])
        reg = self.img[y0:y0 + h, x0:x0 + w]
        reg += (color - reg) * a[..., None]

    def glow(self, cx, cy, rad, color, strength, power=2.0):
        s, ox, oy = self.cam
        X, Y, R = cx * s + ox, cy * s + oy, rad * s
        b = self._box(np.array([[X - R, Y - R], [X + R, Y + R]]), 0)
        if b is None or strength <= 0:
            return
        x0, y0, x1, y1 = b
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        dd = np.sqrt((xx - X) ** 2 + (yy - Y) ** 2) / R
        a = np.clip(1 - dd, 0, 1) ** power * strength
        self._blend(np.clip(a, 0, 1).astype(np.float32), x0, y0, color)

    def vgrad(self, color, a_top, a_bot, y_top=0, y_bot=H):
        y = np.arange(H, dtype=np.float32)
        f = np.clip((y - y_top) / max(1, (y_bot - y_top)), 0, 1)
        a = (a_top + (a_bot - a_top) * f)[:, None] * np.ones((1, W), np.float32)
        self._blend(np.clip(a, 0, 1).astype(np.float32), 0, 0, color)

    def wash(self, color, alpha, textured=False):
        if alpha <= 0:
            return
        self._blend(np.full((H, W), min(1.0, alpha), np.float32), 0, 0, color, textured)

    def result(self):
        return (np.clip(self.img, 0, 1) * 255 + 0.5).astype(np.uint8)


# ---------------------------------------------------------------------------
# The beaver


# ---------------------------------------------------------------------------
# Common effects
# ---------------------------------------------------------------------------
FIRE = (col(0.86, 0.22, 0.10), col(0.99, 0.56, 0.14), col(1.0, 0.88, 0.30))


def flame(c, bx, by, dx, dy, length, width, t, seed=0, layers=3, opacity=1.0, palette=FIRE, line=True, wobble=1.0,
          pressure=0.95):
    """A tapered tongue of fire starting at (bx, by) pointing along (dx, dy)."""
    n = math.hypot(dx, dy)
    dx, dy = dx / n, dy / n
    nx, ny = -dy, dx
    specs = [(palette[0], 1.0, 1.0), (palette[1], 0.75, 0.68), (palette[2], 0.5, 0.38)][:layers]
    for li, (colr, lf, wf) in enumerate(specs):
        Lh, Wd = length * lf, width * wf
        left, right = [], []
        for u in np.linspace(0, 1, 16):
            w = Wd * (1 - u) ** 0.75
            wob = math.sin(u * 9 + t * 22 + seed + li) * Wd * 0.22 * u * wobble
            px, py = bx + dx * u * Lh, by + dy * u * Lh
            left.append((px + nx * (w + wob), py + ny * (w + wob)))
            right.append((px - nx * (w - wob), py - ny * (w - wob)))
        cap = [(bx - dx * Wd * 0.6 * math.sin(q) + nx * Wd * math.cos(q),
                by - dy * Wd * 0.6 * math.sin(q) + ny * Wd * math.cos(q)) for q in np.linspace(0, np.pi, 9)]
        c.poly(left + right[::-1] + cap[::-1][1:-1], fill=colr, line=palette[0] if (li == 0 and line) else None,
               lw=5, pressure=pressure, jit=3, opacity=opacity)


def smoke_wisp(c, x, y, t, seed, length=10, opacity=0.8, lw=7, colr=col(0.62, 0.62, 0.64)):
    pts = []
    for k in range(length):
        pts.append((x + (6 + k * 2.2) * math.sin(k * 0.65 - t * 5 + seed), y - k * 20))
    c.line(pts, colr, lw=lw, pressure=0.7, opacity=opacity)


def stars(c, n=70, seed=5, streak=0.0, dim=1.0):
    """Stars in screen space. streak > 0 draws them as downward streaks (moving fast upward)."""
    r = np.random.default_rng(seed)
    cam = c.cam
    c.cam = (1.0, 0.0, 0.0)
    shift = r.uniform(0, H)
    for i in range(n):
        x, y = r.uniform(0, W), r.uniform(0, H)
        s = r.uniform(1.5, 4.5)
        colr = col(1, 0.97, 0.86)
        if streak > 0:
            y = (y + streak * c.d * 90 + shift) % (H + 200) - 100
            c.line([(x, y), (x, y + streak * s * 40)], colr, lw=s * 0.8, jit=0.3, opacity=0.8 * dim)
        else:
            if s > 4.0:
                c.line([(x - 8, y), (x + 8, y)], colr, lw=2, jit=0.3, opacity=dim)
                c.line([(x, y - 8), (x, y + 8)], colr, lw=2, jit=0.3, opacity=dim)
            c.poly(ell(x, y, s * 0.7, s * 0.7, 0, 8), fill=colr, pressure=1.0, jit=0.3, opacity=dim * r.uniform(0.5, 1))
    c.cam = cam


# ---------------------------------------------------------------------------
# Sound helpers
# ---------------------------------------------------------------------------
SR = 44100


def band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.clip((f - lo * 0.8) / (lo * 0.4 + 1e-9), 0, 1) * np.clip((hi * 1.2 - f) / (hi * 0.4), 0, 1)
    return np.fft.irfft(X * m, len(x))


def noise(dur, lo, hi, seed):
    x = band(np.random.default_rng(seed).normal(size=int(dur * SR)), lo, hi)
    return x / (np.abs(x).max() + 1e-9)


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def decay(dur, tau):
    return np.exp(-tt(dur) / tau)


def sweep(dur, f0, f1):
    f = f0 + (f1 - f0) * tt(dur) / dur
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


class Track:
    def __init__(self, dur):
        self.out = np.zeros(int(dur * SR))

    def add(self, t0, sig):
        """Mix a sound in at t0, with a tiny fade in and out so it can never click."""
        sig = np.array(sig, np.float64)
        a, r = min(len(sig), int(0.003 * SR)), min(len(sig), int(0.01 * SR))
        sig[:a] *= np.linspace(0, 1, a)
        sig[len(sig) - r:] *= np.linspace(1, 0, r)
        i = int(t0 * SR)
        j = min(len(self.out), i + len(sig))
        if j > i:
            self.out[i:j] += sig[:j - i]

    def silence(self, t0, t1, fade=0.03):
        """Cut to silence between t0 and t1. A very quick fade keeps the cut sudden but click-free."""
        i0, i1, n = int(t0 * SR), int(t1 * SR), int(fade * SR)
        self.out[max(0, i0 - n):i0] *= np.linspace(1, 0, min(n, i0))
        self.out[i0:i1] = 0.0
        m = min(n, len(self.out) - i1)
        self.out[i1:i1 + m] *= np.linspace(0, 1, m)

    def save(self, path):
        out = self.out.copy()
        n = int(0.05 * SR)
        out[-n:] *= np.linspace(1, 0, n)
        out = out / (np.abs(out).max() + 1e-9) * 0.89
        with wave.open(path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SR)
            wf.writeframes((out * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------------------
# Video
# ---------------------------------------------------------------------------
def render_video(path, render, n_frames, make_audio, crf=27, size=(720, 1280)):
    """Draw every frame in parallel, encode an iPhone-friendly MP4 and add the sound."""
    import imageio.v2 as imageio
    import imageio_ffmpeg
    from multiprocessing import Pool
    tmp_v, tmp_a = path + '.video.mp4', path + '.audio.wav'
    wr = imageio.get_writer(tmp_v, fps=FPS, codec='libx264', quality=None, pixelformat='yuv420p', macro_block_size=8,
                            ffmpeg_params=['-vf', f'scale={size[0]}:{size[1]}:flags=lanczos', '-crf', str(crf),
                                           '-preset', 'slow'])
    with Pool(os.cpu_count()) as pool:
        for i, frame in enumerate(pool.imap(render, range(n_frames), chunksize=2)):
            wr.append_data(frame)
            if i % 48 == 0:
                print(f'frame {i}/{n_frames}', flush=True)
    wr.close()
    make_audio(tmp_a)
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', tmp_v, '-i', tmp_a,
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-shortest', path],
                   check=True)
    os.remove(tmp_v)
    os.remove(tmp_a)
    print(f'done: {path} ({os.path.getsize(path) / 1e6:.1f} MB)')
