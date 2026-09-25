#!/usr/bin/env python3
"""An Honest Chat: a sombre pop star at the mic, sincerely missing the point.

Flat, deadpan cartoon style (plain shapes, clean black outlines, dot eyes). One continuous shot:
a slow push-in from the middle of the stadium while he reads his statement. The voice is the
recorded speech, cleaned of breaths and given a big stadium echo (audio/ed-speech.m4a).

Usage:
    python3 ed.py stills OUT_DIR T1 T2 ...
    python3 ed.py render OUT.mp4 [CRF]
"""
import json
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, SS = 1280, 720, 12, 2
DUR = 62.5
AUDIO = os.path.join(HERE, 'audio', 'ed-speech.m4a')
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
_WD = json.load(open(os.path.join(HERE, 'data', 'ed_words.json')))
WORDS, LINE_STARTS, LINE_TEXT = _WD['words'], _WD['line_starts'], _WD['line_text']

INK = (24, 20, 22)
SKIN = (246, 204, 178)
SKIN_D = (226, 176, 150)
GINGER = (201, 104, 46)
GINGER_D = (160, 78, 34)
LILAC = (190, 176, 226)
LILAC_D = (160, 146, 204)
TROUSER = (34, 34, 42)
TATS = [(66, 120, 190), (70, 150, 90), (220, 120, 60), (200, 60, 70), (120, 90, 170)]


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def speaking(t):
    for w, a, b in WORDS:
        if a <= t < b + 0.04:
            return t - a
    return None


class Cam:
    """Slow push-in from the middle of the stadium towards his face."""
    def __init__(self, t):
        k = smooth(t / 60.0)
        self.z = 1.0 + 0.6 * k
        self.cx, self.cy = 640, 400 - 130 * k

    def P(self, x, y):
        return ((x - self.cx) * self.z + W / 2) * SS, ((y - self.cy) * self.z + H / 2) * SS

    def S(self, v):
        return v * self.z * SS


class Pen:
    def __init__(self, img, cam):
        self.img, self.cam = img, cam
        self.d = ImageDraw.Draw(img)

    def poly(self, pts, fill, line=INK, lw=4):
        q = [self.cam.P(*p) for p in pts]
        self.d.polygon(q, fill=fill)
        if line:
            self.d.line(q + [q[0]], fill=line, width=max(1, int(self.cam.S(lw) / 2)), joint='curve')

    def ell(self, cx, cy, rx, ry, fill, line=INK, lw=4, rot=0, n=40):
        pts = [(cx + rx * math.cos(a) * math.cos(rot) - ry * math.sin(a) * math.sin(rot),
                cy + rx * math.cos(a) * math.sin(rot) + ry * math.sin(a) * math.cos(rot))
               for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]
        self.poly(pts, fill, line, lw)

    def line(self, pts, colr=INK, lw=4):
        self.d.line([self.cam.P(*p) for p in pts], fill=colr, width=max(1, int(self.cam.S(lw) / 2)), joint='curve')


def glow(img, cam, x, y, r, colr, alpha):
    """A soft pool of light."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    X, Y = cam.P(x, y)
    R = cam.S(r)
    ImageDraw.Draw(lay).ellipse([X - R, Y - R * 0.55, X + R, Y + R * 0.55], fill=colr + (int(255 * alpha),))
    lay = lay.filter(ImageFilter.GaussianBlur(R * 0.35))
    img.alpha_composite(lay)


def spotlight(img, cam):
    """A single cold spotlight falling from the rig above onto him."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.polygon([cam.P(600, -400), cam.P(680, -400), cam.P(860, 700), cam.P(420, 700)], fill=(200, 215, 255, 34))
    d.polygon([cam.P(620, -400), cam.P(660, -400), cam.P(770, 700), cam.P(510, 700)], fill=(215, 225, 255, 26))
    lay = lay.filter(ImageFilter.GaussianBlur(cam.S(18)))
    img.alpha_composite(lay)


def stage(img, pen, cam, t):
    # the vast black LED screen behind, switched off, with a faint pink rim from the tour graphics
    pen.poly([(-900, -500), (2200, -500), (2200, 420), (-900, 420)], (8, 8, 12), None)
    pen.poly([(-600, -300), (1880, -300), (1880, 330), (-600, 330)], (14, 12, 18), (70, 30, 60), lw=3)
    # the round, raised stage
    pen.ell(640, 600, 760, 150, (32, 32, 40), (12, 12, 16), lw=4)
    pen.poly([(-120, 600), (1400, 600), (1400, 640), (-120, 640)], (20, 20, 26), None)
    pen.ell(640, 600, 760, 150, (38, 38, 48), None)
    glow(img, cam, 640, 600, 330, (190, 205, 245), 0.33)
    # a loop pedal at his feet, one tiny green light on
    pen.poly([(700, 598), (770, 598), (772, 616), (698, 616)], (40, 40, 44), INK, 3)
    pen.ell(716, 604, 4, 4, (90, 230, 120), None)
    # a mic stand behind him, unused (as in the photo)
    pen.line([(820, 600), (822, 330)], (60, 60, 66), 5)
    pen.line([(790, 600), (820, 585), (850, 600)], (60, 60, 66), 4)


def audience(img, pen, cam, t):
    """Below the stage lip: a dark sea of heads, a few phone screens glowing."""
    pen.poly([(-900, 640), (2200, 640), (2200, 1400), (-900, 1400)], (4, 4, 7), None)
    rng = np.random.default_rng(7)
    for row in range(5):
        y = 690 + row * 45
        for i in range(40):
            x = -600 + i * 65 + (row % 2) * 30 + rng.uniform(-12, 12)
            pen.ell(x, y, 20, 24, (12, 12, 17), None)
            pen.poly([(x - 34, y + 20), (x + 34, y + 20), (x + 40, y + 70), (x - 40, y + 70)], (12, 12, 17), None)
    rng = np.random.default_rng(3)
    for i in range(14):
        x, y = rng.uniform(-400, 1700), rng.uniform(660, 860)
        on = (int(t * 0.4 + i) % 5) != 0
        if on:
            pen.poly([(x - 6, y - 10), (x + 6, y - 10), (x + 6, y + 10), (x - 6, y + 10)], (190, 205, 235), None)
            glow(img, cam, x, y, 22, (170, 190, 235), 0.25)


def mouth_shape(t):
    p = speaking(t)
    if p is None:
        return 0
    return [2, 1, 2, 0, 1][int(p * 11) % 5]


def ed(img, pen, cam, t):
    x, base = 640, 600
    sway = 2.5 * math.sin(t * 0.7)
    x += sway
    # legs and shoes
    for dx in (-26, 26):
        pen.poly([(x + dx - 22, base - 175), (x + dx + 22, base - 175), (x + dx + 20, base - 8), (x + dx - 20, base - 8)],
                 TROUSER)
        pen.poly([(x + dx - 26, base - 12), (x + dx + 30, base - 12), (x + dx + 32, base + 4), (x + dx - 28, base + 4)],
                 (240, 240, 240))
    # the guitar slung on his back: the neck and headstock poke up over his shoulder
    pen.poly([(x - 48, 262), (x - 36, 258), (x - 92, 110), (x - 104, 114)], (120, 72, 40))
    pen.poly([(x - 108, 70), (x - 88, 66), (x - 86, 116), (x - 106, 118)], (70, 42, 26))
    for k in range(3):
        pen.ell(x - 111, 78 + k * 13, 4, 3, (200, 200, 200), None)
        pen.ell(x - 84, 76 + k * 13, 4, 3, (200, 200, 200), None)
    # a baggy lilac t-shirt, boxy and a size too big
    pen.poly([(x - 92, 250), (x + 92, 250), (x + 98, 432), (x - 98, 432)], LILAC)
    pen.poly([(x - 92, 252), (x - 150, 290), (x - 132, 362), (x - 88, 344)], LILAC)  # sleeves
    pen.poly([(x + 92, 252), (x + 150, 290), (x + 132, 362), (x + 88, 344)], LILAC)
    pen.line([(x - 30, 250), (x, 268), (x + 30, 250)], LILAC_D, 5)  # neckline
    pen.line([(x - 90, 262), (x + 70, 420)], (70, 50, 40), 7)  # the guitar strap
    # tattooed forearms: the left hanging, the right up holding the mic
    pen.poly([(x - 146, 350), (x - 116, 356), (x - 124, 470), (x - 150, 468)], SKIN)
    rng = np.random.default_rng(11)
    for i in range(7):
        pen.ell(x - 136 + rng.uniform(-6, 6), 368 + i * 14, 9, 6, TATS[i % 5], None, rot=rng.uniform(0, 3))
    pen.ell(x - 138, 480, 16, 16, SKIN)

    # head (big and round), ears with an in-ear monitor
    hx, hy = x + 2, 170 + 1.5 * math.sin(t * 1.1)
    pen.ell(hx - 94, hy + 8, 15, 22, SKIN)
    pen.ell(hx + 94, hy + 8, 15, 22, SKIN)
    pen.ell(hx + 96, hy + 10, 6, 7, INK, None)
    pen.line([(hx + 98, hy + 16), (hx + 104, hy + 80)], INK, 2)
    pen.ell(hx, hy, 96, 104, SKIN)
    # short ginger hair and ginger stubble
    pen.poly([(hx - 92, hy - 26), (hx - 78, hy - 82), (hx - 22, hy - 108), (hx + 44, hy - 106), (hx + 88, hy - 76),
              (hx + 94, hy - 26), (hx + 66, hy - 64), (hx, hy - 76), (hx - 66, hy - 60)], GINGER)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    jaw = [cam.P(hx + 92 * math.cos(q) * 0.97, hy + 10 + 100 * math.sin(q) * 0.86) for q in np.linspace(0.08, math.pi - 0.08, 30)]
    jaw += [cam.P(hx - 50, hy + 40), cam.P(hx - 18, hy + 30), cam.P(hx + 18, hy + 30), cam.P(hx + 50, hy + 40)][::-1][::-1]
    ImageDraw.Draw(lay).polygon(jaw, fill=GINGER + (70,))
    img.alpha_composite(lay)
    pen.ell(hx, hy, 96, 104, None)  # redraw the outline over the stubble
    # the teleprompter glow from below
    glow(img, cam, hx, hy + 70, 90, (170, 190, 240), 0.18)
    # eyes: little dots, glancing down to the prompter every so often, blinking
    look_down = (int(t / 2.7) % 3 == 1) and speaking(t) is not None
    blink = (t % 3.9) < 0.12
    ey = hy - 6 + (7 if look_down else 0)
    for sgn in (-1, 1):
        ex = hx + sgn * 30
        if blink:
            pen.line([(ex - 9, hy - 4), (ex + 9, hy - 4)], INK, 4)
        else:
            pen.ell(ex, ey, 7.5, 8.5, INK, None)
        # sad, sincere brows: tilted up at the inner ends
        pen.line([(ex - sgn * 4, hy - 34), (ex + sgn * 16, hy - 26)], GINGER_D, 7)
    # a small nose
    pen.line([(hx - 4, hy + 6), (hx + 6, hy + 22), (hx - 6, hy + 26)], SKIN_D, 4)
    # the mouth, moving with every word
    m = mouth_shape(t)
    my = hy + 48
    if m == 0:
        pen.line([(hx - 18, my), (hx, my + 2), (hx + 18, my)], INK, 4)
    elif m == 1:
        pen.ell(hx, my + 2, 13, 7, (90, 30, 34))
    else:
        pen.ell(hx, my + 4, 15, 13, (90, 30, 34))
        pen.poly([(hx - 10, my - 4), (hx + 10, my - 4), (hx + 8, my + 1), (hx - 8, my + 1)], (250, 250, 250), None)
    # a single tear on the thank-yous
    if t > 54.4:
        k = min(1.0, (t - 54.4) / 5.0)
        tx, ty = hx - 32, hy + 8 + 70 * k
        pen.poly([(tx, ty - 12), (tx + 6, ty + 2), (tx, ty + 8), (tx - 6, ty + 2)], (190, 220, 255), INK, 2)
    # the mic in his hand, on its stand in front of him
    pen.line([(x + 40, 600), (x + 44, hy + 90)], (64, 64, 70), 6)
    pen.line([(x + 10, 600), (x + 40, 586), (x + 70, 600)], (64, 64, 70), 5)
    pen.poly([(x + 36, hy + 92), (x + 52, hy + 90), (x + 44, hy + 58), (x + 30, hy + 60)], (30, 30, 34))
    pen.ell(x + 36, hy + 58, 12, 11, (60, 60, 66))
    ex, ey = x + 128, 350  # elbow at the sleeve, forearm angled up to the mic
    hx2, hy2 = x + 62, hy + 104
    pen.poly([(ex - 14, ey + 6), (ex + 14, ey - 6), (hx2 + 14, hy2 - 8), (hx2 - 12, hy2 + 10)], SKIN)
    for i in range(5):
        q = (i + 0.5) / 5
        pen.ell(ex + (hx2 - ex) * q, ey + (hy2 - ey) * q, 9, 6, TATS[(i + 2) % 5], None, rot=0.9)
    pen.ell(hx2, hy2, 20, 18, SKIN)  # his hand around the mic


def subtitle(img, t):
    d = ImageDraw.Draw(img)
    starts = LINE_STARTS + [len(WORDS)]
    for k, s in enumerate(LINE_STARTS):
        a = WORDS[s][1]
        b = WORDS[starts[k + 1] - 1][2] + 0.6
        if k + 1 < len(LINE_STARTS):
            b = min(b, WORDS[starts[k + 1]][1])
        if a <= t < b:
            txt = LINE_TEXT[k]
            font = ImageFont.truetype(FONT, 34 * SS)
            rows, cur = [], ''
            for w in txt.split():
                if cur and len(cur) + 1 + len(w) > 50:
                    rows.append(cur)
                    cur = w
                else:
                    cur = (cur + ' ' + w).strip()
            rows.append(cur)
            for i, row in enumerate(rows):
                d.text((W * SS / 2, (H - 32 - 42 * (len(rows) - 1 - i)) * SS), row, font=font, fill=(255, 255, 255),
                       anchor='mm', stroke_width=4 * SS, stroke_fill=(0, 0, 0))
            break


def render(frame):
    t = frame / FPS
    cam = Cam(t)
    img = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 255))
    pen = Pen(img, cam)
    stage(img, pen, cam, t)
    spotlight(img, cam)
    pen = Pen(img, cam)
    ed(img, pen, cam, t)
    audience(img, Pen(img, cam), cam, t)
    subtitle(img, t)
    out = img.convert('RGB').resize((W, H), Image.LANCZOS)
    a = np.asarray(out).astype(np.float32)
    fade = min(1.0, t / 1.2) * min(1.0, max(0.0, (DUR - t) / 1.5))
    return (a * fade).astype(np.uint8)


def main():
    mode = sys.argv[1]
    if mode == 'stills':
        os.makedirs(sys.argv[2], exist_ok=True)
        for ts in sys.argv[3:]:
            Image.fromarray(render(int(float(ts) * FPS))).save(os.path.join(sys.argv[2], f'ed_{float(ts):05.1f}.png'))
    elif mode == 'render':
        import imageio_ffmpeg
        out = sys.argv[2]
        crf = sys.argv[3] if len(sys.argv) > 3 else '28'
        ff = imageio_ffmpeg.get_ffmpeg_exe()
        n = int(DUR * FPS)
        p = subprocess.Popen([ff, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                              '-r', str(FPS), '-i', '-', '-i', AUDIO, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264',
                              '-crf', crf, '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-t', str(DUR),
                              '-af', f'afade=t=out:st={DUR - 1.5}:d=1.5', '-movflags', '+faststart', out],
                             stdin=subprocess.PIPE)
        for f in range(n):
            p.stdin.write(render(f).tobytes())
            if f % 60 == 0:
                print(f'frame {f}/{n}', flush=True)
        p.stdin.close()
        p.wait()
        print(f'done: {out} ({os.path.getsize(out) / 1e6:.1f} MB)')


if __name__ == '__main__':
    main()
