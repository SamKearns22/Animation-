#!/usr/bin/env python3
"""The CranbriJoos sign-off (Sam, 15 Oct): the profile picture itself. The beaver never blinks; the white fire
behind him dances; in his paw, where the leaves were, a white juice box with the CranbriJoos logo in big red
balloon letters ("Cranbri" larger than "Joos"); its straw goes up to his mouth and he takes a sip. About 1.5 s,
silent unless Sam asks for a slurp. Joined onto the end of every film, after the last line.

    python3 signoff.py sheet OUT.jpg          a few frames side by side, for checking
    python3 signoff.py clip OUT.mp4           the sign-off on its own (1080 x 1920, 12 fps)
    python3 signoff.py add FILM.mp4 OUT.mp4   a finished film with the sign-off joined on the end
"""
import math
import os
import subprocess
import sys
import tempfile

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PFP = os.path.join(ROOT, 'profile', 'cranbrijoos-tiktok-1080-eyes-open.png')   # eyes open: he never blinks
FONT = os.path.join(HERE, 'fonts', 'TikTokSans-Bold.woff')
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, DUR = 12, 2.0
W, H = 1080, 1920
SIZE = 860                                   # the profile picture in the middle of the screen, white all round (Sam)
DX, DY = (W - SIZE) // 2, (H - SIZE) // 2 - 60
PAPER = (250, 250, 248)
SLURP = os.path.join(HERE, 'audio', 'signoff-slurp.m4a')
SIP_AT = 0.45                                # the juice starts up the straw (and the slurp starts) here
INK = (24, 20, 22)
RED = np.array([206, 22, 48], float)
MOUTH = (0.50 * SIZE + DX, 0.706 * SIZE + DY)           # his own mouth: the dark oval just under his teeth (Sam)
BOX = tuple(int(f * SIZE + o) for f, o in ((0.57, DX), (0.70, DY), (1.05, DX), (1.10, DY)))   # where the leaves were
PAW = (0.585, 0.885, 0.05, 0.04)
EYES = ((0.293, 0.357), (0.707, 0.357))                 # his eyes (fractions of the square)


def sucking(t):
    """0-1: how hard he is sucking (eyes wide, mouth a black O round the straw), from the sip to just after it."""
    a = min(1.0, max(0.0, (t - (SIP_AT - 0.08)) / 0.15))
    b = min(1.0, max(0.0, (t - (SIP_AT + 1.15)) / 0.3))
    return a * (1 - b)


def widen(img, k):
    """His eyes open wide (k 0-1): each eye drawn larger in place, mostly taller."""
    if k <= 0:
        return
    for fx, fy in EYES:
        cx, cy = fx * SIZE + DX, fy * SIZE + DY
        r = 0.055 * SIZE
        box = (int(cx - r), int(cy - r), int(cx + r), int(cy + r))
        patch = img.crop(box)
        sx, sy = 1 + 0.55 * k, 1 + 0.95 * k
        big = patch.resize((int(patch.width * sx), int(patch.height * sy)), Image.LANCZOS)
        m = Image.new('L', big.size, 0)
        ImageDraw.Draw(m).ellipse([big.width * 0.18, big.height * 0.18, big.width * 0.82, big.height * 0.82], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(4))
        img.paste(big, (int(cx - big.width / 2), int(cy - big.height / 2)), m)


def o_mouth(img, k):
    """While he sucks, his mouth snaps into a round black O around the straw (Sam: his own mouth, no extra lips)."""
    if k < 0.5:
        return
    d = ImageDraw.Draw(img)
    r = 0.036 * SIZE
    d.ellipse([MOUTH[0] - r, MOUTH[1] - r * 0.95, MOUTH[0] + r, MOUTH[1] + r * 0.95], fill=(14, 10, 10))


_cache = {}


def plates():
    """The picture split once: the beaver (leaves removed) with a soft-edged mask, and the background (fire and sky)
    with the beaver filled in from its surroundings, so the fire can move behind him."""
    if _cache:
        return _cache
    sq = np.asarray(Image.open(PFP).convert('RGB').resize((SIZE, SIZE), Image.LANCZOS)).astype(float)
    r, g, b = sq[..., 0], sq[..., 1], sq[..., 2]
    leaf = (g > r + 12) & (g > b + 6)
    brown = (r > b + 18) & (r > 60)
    body = ndimage.binary_closing(brown | leaf, iterations=6)
    body = ndimage.binary_fill_holes(body)                     # eyes, nose and claws inside him count as him
    lab, n = ndimage.label(body)
    if n > 1:
        sizes = ndimage.sum(body, lab, range(1, n + 1))
        body = lab == (1 + int(np.argmax(sizes)))
    leaf = ndimage.binary_dilation(leaf, iterations=4) & body
    _, (iy, ix) = ndimage.distance_transform_edt(leaf, return_indices=True)
    fur = sq[iy, ix]                                           # leaves replaced by the nearest fur
    fur = np.where(leaf[..., None], ndimage.uniform_filter(fur, (9, 9, 1)), sq)
    _, (by, bx) = ndimage.distance_transform_edt(body, return_indices=True)
    bg = sq[by, bx]                                            # behind him: the nearest fire or sky
    bg = np.where(body[..., None], ndimage.uniform_filter(bg, (25, 25, 1)), sq)
    alpha = ndimage.gaussian_filter(body.astype(float), 1.2)
    _cache.update(fur=fur, bg=bg, alpha=alpha)
    return _cache


def dancing(bg, t):
    """The fire flickers and sways: each column of flame bends side to side, more towards its tips, and the flames
    stretch up and down a little."""
    h, w, _ = bg.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    up = 1 - yy / h                                            # higher up sways more (the tips)
    sx = xx + (14 * np.sin(yy / 46 - t * 9.0) + 7 * np.sin(yy / 17 + xx / 60 + t * 13)) * (0.35 + up)
    sy = yy + 9 * np.sin(xx / 38 + t * 11) * (0.3 + up)
    sx, sy = xx + (sx - xx) * SIZE / 1350, yy + (sy - yy) * SIZE / 1350      # sway scaled to the picture's size
    out = np.empty_like(bg)
    for c in range(3):
        out[..., c] = ndimage.map_coordinates(bg[..., c], [np.clip(sy, 0, h - 1), np.clip(sx, 0, w - 1)], order=1)
    return out


def balloon(text, size):
    """Red balloon letters: rounded, shaded like inflated rubber, with a shine, as an RGBA image."""
    f = ImageFont.truetype(FONT, size)
    pad = size // 3
    gap = size * 0.1                                                       # each letter its own balloon
    dd = ImageDraw.Draw(Image.new('L', (1, 1)))
    tw = int(sum(dd.textlength(ch, font=f) for ch in text) + gap * (len(text) - 1))
    m = Image.new('L', (tw + 2 * pad, int(size * 1.3) + 2 * pad), 0)
    md = ImageDraw.Draw(m)
    x = pad
    for ch in text:
        md.text((x, pad), ch, font=f, fill=255, stroke_width=size // 22, stroke_fill=255)
        x += dd.textlength(ch, font=f) + gap
    mask = np.asarray(m.filter(ImageFilter.GaussianBlur(size / 45)), float) / 255
    solid = mask > 0.5
    hgt = ndimage.gaussian_filter(solid.astype(float), size / 14)           # the puff
    gy, gx = np.gradient(hgt)
    k = size / 6
    nx, ny, nz = -gx * k, -gy * k, np.ones_like(hgt)
    n = np.sqrt(nx * nx + ny * ny + nz * nz)
    lx, ly, lz = -0.45, -0.6, 0.66
    diff = np.clip((nx * lx + ny * ly + nz * lz) / n, 0, 1)
    spec = np.clip((nx * -0.3 + ny * -0.5 + nz * 0.8) / n, 0, 1) ** 40
    col = RED[None, None, :] * (0.45 + 0.75 * diff[..., None]) + 255 * 0.9 * spec[..., None]
    edge = solid & ~ndimage.binary_erosion(solid, iterations=max(3, size // 22))
    col[edge] = (110, 8, 24)
    rgba = np.dstack([np.clip(col, 0, 255), solid * 255.0]).astype(np.uint8)
    return Image.fromarray(rgba, 'RGBA')


def juice_box(img, sip, sucking_now=False):
    """The white box in his paw, the logo on its front, the straw up to his mouth; `sip` 0-1: juice up the straw,
    the box's sides drawn in a little."""
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = BOX
    dent = 12 * sip
    side = 30
    d.polygon([(x1, y0), (x1 + side, y0 - 18), (x1 + side, y1 - 18), (x1, y1)], fill=(206, 208, 210), outline=INK, width=4)
    d.polygon([(x0, y0), (x1, y0), (x1 + side, y0 - 18), (x0 + side, y0 - 18)], fill=(236, 237, 238), outline=INK, width=4)
    d.polygon([(x0, y0), (x1, y0), (x1 - dent, (y0 + y1) / 2), (x1, y1), (x0, y1), (x0 + dent, (y0 + y1) / 2)],
              fill=(252, 252, 250), outline=INK, width=6)
    cx = (x0 + x1) / 2
    hh = y1 - y0
    for word, size, y in (('Cranbri', 120, y0 + 0.05 * hh), ('Joos', 92, y0 + 0.37 * hh)):
        lg = balloon(word, size)
        if lg.width > (x1 - x0) - 16:
            lg = lg.resize((int(x1 - x0 - 16), int(lg.height * (x1 - x0 - 16) / lg.width)), Image.LANCZOS)
        img.paste(lg, (int(cx - lg.width / 2), int(y)), lg)
    for dx, f in ((-34, 0.90), (0, 0.87), (32, 0.91)):                    # three cranberries under the name
        dy = f * hh
        d.ellipse([cx + dx - 14, y0 + dy - 14, cx + dx + 14, y0 + dy + 14], fill=(206, 22, 48), outline=INK, width=3)
        d.ellipse([cx + dx - 7, y0 + dy - 9, cx + dx - 2, y0 + dy - 4], fill=(255, 220, 220))
    # the straw: out of the top, up, and bent across into the corner of his mouth
    sx, sy = x0 + 34, y0 - 10
    bend = MOUTH[1] - 70                                                   # up, then across and down into his mouth
    end = (MOUTH[0] + (0.0 if sucking_now else 0.045 * SIZE), MOUTH[1])
    pts = [(sx, sy), (sx, bend), end]
    d.line(pts, fill=INK, width=18, joint='curve')
    d.line(pts, fill=(250, 250, 250), width=11, joint='curve')
    if sip > 0:                                                            # the juice climbs the straw
        full = sy - bend
        top = sy - full * min(1.0, sip * 1.3)
        d.line([(sx, sy), (sx, top)], fill=tuple(int(c) for c in RED), width=7)
        if sip * 1.3 > 1:
            u = min(1.0, (sip * 1.3 - 1) / 0.3)
            d.line([(sx, bend), (sx + (end[0] - sx) * u, bend + (end[1] - bend) * u)],
                   fill=tuple(int(c) for c in RED), width=7)


def frame(t):
    p = plates()
    bg = dancing(p['bg'], t)
    a = p['alpha'][..., None]
    sq = bg * (1 - a) + p['fur'] * a
    img = Image.new('RGB', (W, H), PAPER)
    pic = Image.fromarray(np.clip(sq, 0, 255).astype(np.uint8))
    m = Image.new('L', (SIZE, SIZE), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], 44, fill=255)
    img.paste(pic, (DX, DY), m)
    sip = min(1.0, max(0.0, (t - SIP_AT) / 0.6))
    k = sucking(t)
    widen(img, k)
    o_mouth(img, k)
    juice_box(img, sip, k >= 0.5)
    # his paw over the bottom of the box, so he is holding it
    px, py, rx, ry = PAW
    fur = Image.fromarray(np.clip(p['fur'], 0, 255).astype(np.uint8))
    cx, cy, ex, ey = px * SIZE, py * SIZE, rx * SIZE, ry * SIZE
    m = Image.new('L', fur.size, 0)
    ImageDraw.Draw(m).ellipse([cx - ex, cy - ey, cx + ex, cy + ey], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(1.5))
    box = (int(cx - ex - 6), int(cy - ey - 6), int(cx + ex + 6), int(cy + ey + 6))
    img.paste(fur.crop(box), (box[0] + DX, box[1] + DY), m.crop(box))
    return img


def clip(out):
    n = int(round(DUR * FPS))
    sound = os.path.splitext(out)[0] + '-slurp.wav'
    slurp_track(sound)
    p = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-i', sound, '-shortest',
                          '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-movflags', '+faststart',
                          out], stdin=subprocess.PIPE)
    for k in range(n):
        p.stdin.write(np.asarray(frame(k / FPS)).tobytes())
    p.stdin.close()
    p.wait()
    os.remove(sound)


def slurp_track(path):
    """Sam's slurp (asked for, 15 Oct): its sound starts as the juice starts up the straw, at a natural level."""
    import mossad_audio as MA
    from burnham_film import load, SR
    x = MA.denoise(MA.dehum(load(SLURP)))                                  # cleaned like the voices
    st = MA.speech(x) or [(0.0, len(x) / SR)]
    a, b = st[0]                                                           # the slurp alone (the later sound was noise)
    x = x[max(0, int((a - 0.04) * SR)):int((b + 0.08) * SR)]
    f = int(0.01 * SR)
    x[:f] *= np.linspace(0, 1, f)
    x[-f:] *= np.linspace(1, 0, f)
    x = x * 10 ** ((-20 - MA.lufs(x)) / 20)
    out = np.zeros(int(DUR * SR) + SR)
    i = int(SIP_AT * SR)
    out[i:i + len(x)] += x[:len(out) - i]
    import wave
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(out[:int(DUR * SR)], -1, 1) * 32767).astype('<i2').tobytes())


def add(film, out):
    """Join the sign-off onto the end of a finished film (1080 x 1920, 12 fps), its sound kept."""
    with tempfile.TemporaryDirectory() as tmp:
        so = os.path.join(tmp, 'signoff.mp4')
        clip(so)
        subprocess.run([FF, '-y', '-loglevel', 'error', '-i', film, '-i', so, '-filter_complex',
                        '[0:v]fps=12,format=yuv420p[a];[1:v]fps=12,format=yuv420p[b];[0:a]aresample=48000[x];'
                        '[1:a]aresample=48000[y];[a][x][b][y]concat=n=2:v=1:a=1[v][s]',
                        '-map', '[v]', '-map', '[s]', '-c:v', 'libx264', '-crf', '20', '-preset', 'slow', '-c:a', 'aac',
                        '-b:a', '160k', '-movflags', '+faststart', out], check=True)
    print(f'{out}: {os.path.getsize(out) / 1e6:.1f} MB')


def sheet(out, times=(0.0, 0.5, 0.8, 1.2)):
    ims = [frame(t).resize((360, 640)) for t in times]
    s = Image.new('RGB', (360 * len(ims), 640))
    for i, im in enumerate(ims):
        s.paste(im, (360 * i, 0))
    s.save(out, quality=88)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'sheet':
        sheet(sys.argv[2])
    elif cmd == 'clip':
        clip(sys.argv[2])
    elif cmd == 'add':
        add(sys.argv[2], sys.argv[3])
