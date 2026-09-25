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
        if fill is not None:
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
    return [2, 1, 3, 1, 2, 0][int(p * 11) % 6]


def soft(img, cam, pts, colr, alpha, blur=6):
    """A soft painted shadow or highlight."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).polygon([cam.P(*q) for q in pts], fill=colr + (int(255 * alpha),))
    if blur:
        lay = lay.filter(ImageFilter.GaussianBlur(cam.S(blur)))
    img.alpha_composite(lay)


def curve(pts, n=6):
    """Catmull-Rom through the points (closed): soft, hand-drawn curves."""
    p = np.asarray(pts, float)
    out = []
    for i in range(len(p)):
        p0, p1, p2, p3 = p[i - 1], p[i], p[(i + 1) % len(p)], p[(i + 2) % len(p)]
        for u in np.linspace(0, 1, n, endpoint=False):
            out.append(tuple(0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                                    + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)))
    return out


def oval(cx, cy, rx, ry, n=48, a0=0.0, a1=2 * math.pi):
    return [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in np.linspace(a0, a1, n)]


def ed(img, pen, cam, t):
    """Drawn in the later deadpan style: real proportions, almond eyes with small pupils, fine lines, soft shading."""
    LW = 2.6
    x = 640 + 2.0 * math.sin(t * 0.7)
    sp = speaking(t)
    look_down = (int(t / 2.7) % 3 == 1) and sp is not None
    # guitar slung on his back: the neck and headstock over his left shoulder
    pen.poly([(x - 70, 300), (x - 58, 296), (x - 120, 150), (x - 132, 155)], (128, 78, 44), INK, LW)
    pen.poly([(x - 140, 108), (x - 118, 104), (x - 114, 156), (x - 136, 158)], (72, 44, 28), INK, LW)
    for k in range(3):
        pen.ell(x - 143, 116 + k * 14, 3.5, 3, (215, 215, 215), INK, 1.5)
        pen.ell(x - 111, 114 + k * 14, 3.5, 3, (215, 215, 215), INK, 1.5)
    # body: a baggy lilac tee over broad, sloping shoulders
    tee = [(x - 60, 268), (x - 128, 292), (x - 176, 330), (x - 196, 420), (x - 150, 436), (x - 140, 400),
           (x - 136, 640), (x + 136, 640), (x + 140, 400), (x + 150, 436), (x + 196, 420), (x + 176, 330),
           (x + 128, 292), (x + 60, 268)]
    pen.poly(tee, LILAC, INK, LW)
    soft(img, cam, [(x + 60, 290), (x + 170, 330), (x + 190, 420), (x + 136, 640), (x + 70, 640), (x + 90, 400)],
         (120, 100, 170), 0.28, 10)
    pen.line([(x - 150, 436), (x - 140, 400), (x - 144, 360)], LILAC_D, 2)
    pen.line([(x + 150, 436), (x + 140, 400), (x + 144, 360)], LILAC_D, 2)
    pen.line([(x - 100, 300), (x + 110, 560)], (78, 54, 40), 6)  # guitar strap
    # neck
    pen.poly([(x - 34, 230), (x + 34, 230), (x + 38, 286), (x - 38, 286)], SKIN, INK, LW)
    soft(img, cam, [(x - 34, 236), (x + 34, 236), (x + 30, 262), (x - 30, 262)], (170, 110, 90), 0.35, 4)
    pen.line(oval(x, 262, 58, 24, 30, 0.15, math.pi - 0.15), INK, LW)  # crew neckline
    # left arm hanging, tattooed from elbow to wrist
    pen.poly([(x - 196, 420), (x - 150, 436), (x - 158, 560), (x - 190, 558)], SKIN, INK, LW)
    rng = np.random.default_rng(11)
    for i in range(9):
        cx, cy = x - 174 + rng.uniform(-10, 10), 446 + i * 12
        pen.ell(cx, cy, rng.uniform(6, 11), rng.uniform(4, 7), TATS[i % 5], None, rot=rng.uniform(0, 3))
    pen.poly([(x - 192, 556), (x - 156, 556), (x - 154, 592), (x - 170, 604), (x - 190, 592)], SKIN, INK, LW)
    # head: a proper oval with a squarer jaw, turned very slightly to his right
    hx, hy = x + 4, 150 + 1.2 * math.sin(t * 1.1)
    head = oval(hx, hy - 6, 74, 88, 40, math.pi, 2 * math.pi) + [
        (hx + 74, hy + 10), (hx + 66, hy + 58), (hx + 40, hy + 92), (hx, hy + 102), (hx - 40, hy + 92),
        (hx - 66, hy + 58), (hx - 74, hy + 10)]
    for sgn in (-1, 1):  # ears, one with the in-ear monitor
        pen.poly(oval(hx + sgn * 76, hy + 6, 13, 24), SKIN, INK, LW)
    pen.ell(hx + 78, hy + 6, 5, 6, INK, None)
    pen.line([(hx + 80, hy + 12), (hx + 86, hy + 80), (hx + 90, 260)], INK, 1.6)
    pen.poly(head, SKIN, INK, LW)
    soft(img, cam, [(hx + 30, hy - 60), (hx + 74, hy - 10), (hx + 66, hy + 58), (hx + 40, hy + 92), (hx + 30, hy + 30)],
         (190, 120, 100), 0.32, 8)
    # short ginger hair, swept a little to one side
    hair = [(hx - 74, hy - 8), (hx - 76, hy - 50), (hx - 56, hy - 86), (hx - 10, hy - 102), (hx + 40, hy - 98),
            (hx + 72, hy - 70), (hx + 76, hy - 14), (hx + 64, hy - 40), (hx + 34, hy - 62), (hx - 10, hy - 68),
            (hx - 50, hy - 58), (hx - 66, hy - 34)]
    pen.poly(curve(hair), GINGER, INK, LW)
    for k in range(4):
        pen.line([(hx - 40 + 26 * k, hy - 92 + 4 * k), (hx - 30 + 26 * k, hy - 70 + 3 * k)], GINGER_D, 2)
    # forehead creases (sincere concern)
    for k in range(2):
        pen.line([(hx - 30, hy - 44 + 9 * k), (hx - 6, hy - 48 + 9 * k), (hx + 24, hy - 45 + 9 * k)], SKIN_D, 1.8)
    # eyes: white almonds with small pupils and heavy lids
    blink = (t % 3.9) < 0.12
    for sgn in (-1, 1):
        ex, ey = hx - 8 + sgn * 30, hy - 8
        if blink:
            pen.line([(ex - 16, ey), (ex, ey + 3), (ex + 16, ey)], INK, 2.4)
            continue
        almond = [(ex - 17, ey), (ex - 8, ey - 8), (ex + 8, ey - 8), (ex + 17, ey), (ex + 8, ey + 7), (ex - 8, ey + 7)]
        pen.poly(almond, (250, 250, 248), INK, 2.0)
        py = ey + (3 if look_down else -1)
        pen.ell(ex - 3, py, 4.5, 4.5, INK, None)
        lid = 3 if look_down else 0  # heavy, tired upper lids
        pen.line([(ex - 17, ey - 1 + lid), (ex - 8, ey - 9 + lid), (ex + 8, ey - 9 + lid), (ex + 17, ey - 1 + lid)], INK, 2.6)
        # thin worried brows, inner ends raised
        pen.line([(ex - sgn * 4, ey - 24), (ex + sgn * 20, ey - 18)], GINGER_D, 3.2)
    # nose: a single line down and round to the nostril
    pen.line([(hx - 4, hy - 4), (hx - 12, hy + 26), (hx - 6, hy + 32), (hx + 6, hy + 30)], INK, 2.0)
    pen.line([(hx - 16, hy + 30), (hx - 12, hy + 33)], INK, 1.6)
    # fine ginger stubble dots on the jaw and lip
    rng = np.random.default_rng(5)
    for i in range(55):
        a = rng.uniform(0.3, math.pi - 0.3)
        r = rng.uniform(0.6, 0.95)
        sx, sy = hx + 64 * r * math.cos(a), hy + 30 + 66 * r * math.sin(a)
        if abs(sx - hx + 4) < 24 and hy + 48 < sy < hy + 84:
            continue
        pen.ell(sx, sy, 0.9, 0.9, (196, 128, 92), None)
    # the mouth, moving with every word
    m = mouth_shape(t)
    mx, my = hx - 4, hy + 60
    if m == 0:
        pen.line([(mx - 16, my + 2), (mx, my), (mx + 16, my + 3)], INK, 2.4)
    else:
        h = {1: 7, 2: 13, 3: 18}[m]
        w = {1: 15, 2: 17, 3: 14}[m]
        pen.poly([(mx - w, my - 2), (mx + w, my - 3), (mx + w * 0.7, my + h), (mx - w * 0.7, my + h)], (70, 26, 30), INK, 2.2)
        if m >= 2:
            pen.poly([(mx - w * 0.8, my - 1), (mx + w * 0.8, my - 2), (mx + w * 0.7, my + 3), (mx - w * 0.7, my + 3)],
                     (245, 245, 240), None)
    # a single tear on the thank-yous
    if t > 54.4:
        k = min(1.0, (t - 54.4) / 5.0)
        tx, ty = hx - 40, hy + 2 + 64 * k
        pen.poly([(tx, ty - 10), (tx + 5, ty + 2), (tx, ty + 7), (tx - 5, ty + 2)], (200, 225, 255), INK, 1.5)
    # the teleprompter glow from below
    glow(img, cam, hx, hy + 90, 80, (170, 190, 240), 0.14)
    # right arm up: elbow down at his side, hand holding the mic under his chin
    ex2, ey2 = x + 236, 478  # elbow out past his side, forearm angled up and in to his mouth
    hx2, hy2 = hx + 78, hy + 112
    pen.poly([(x + 152, 432), (x + 196, 418), (ex2 + 18, ey2 - 4), (ex2 - 14, ey2 + 12)], SKIN, INK, LW)
    pen.ell(ex2 + 2, ey2 + 4, 19, 17, SKIN, INK, LW)
    pen.poly([(ex2 - 14, ey2 + 12), (ex2 + 18, ey2 - 6), (hx2 + 18, hy2 - 6), (hx2 - 12, hy2 + 14)], SKIN, INK, LW)
    for i in range(6):
        q = (i + 0.5) / 6
        pen.ell(ex2 + (hx2 - ex2) * q + 2, ey2 + (hy2 - ey2) * q, 8, 5, TATS[(i + 2) % 5], None, rot=-0.9)
    # the handheld mic, tilted up to his mouth
    mx2, my2 = hx + 22, hy + 70
    pen.poly([(hx2 - 6, hy2 + 16), (hx2 + 8, hy2 + 10), (mx2 + 8, my2 + 4), (mx2 - 6, my2 + 10)], (28, 28, 32), INK, 2)
    pen.ell(mx2, my2 + 4, 11, 10, (70, 70, 76), INK, 2)
    pen.poly([(hx2 - 18, hy2 - 8), (hx2 + 16, hy2 - 14), (hx2 + 22, hy2 + 12), (hx2 - 12, hy2 + 22)], SKIN, INK, LW)
    for k in range(3):
        pen.line([(hx2 - 14, hy2 - 2 + 7 * k), (hx2 + 16, hy2 - 7 + 7 * k)], SKIN_D, 1.4)


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
    stage(img, Pen(img, cam), cam, t)
    img = img.filter(ImageFilter.GaussianBlur(cam.S(5)))  # a soft, out-of-focus background
    spotlight(img, cam)
    ed(img, Pen(img, cam), cam, t)
    front = Image.new('RGBA', img.size, (0, 0, 0, 0))
    audience(front, Pen(front, cam), cam, t)
    img.alpha_composite(front.filter(ImageFilter.GaussianBlur(cam.S(4))))
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
        from multiprocessing import Pool
        with Pool(os.cpu_count()) as pool:  # draw several frames at once, written out in order
            for f, fr in enumerate(pool.imap(render, range(n), chunksize=4)):
                p.stdin.write(fr.tobytes())
                if f % 60 == 0:
                    print(f'frame {f}/{n}', flush=True)
        p.stdin.close()
        p.wait()
        print(f'done: {out} ({os.path.getsize(out) / 1e6:.1f} MB)')


if __name__ == '__main__':
    main()
