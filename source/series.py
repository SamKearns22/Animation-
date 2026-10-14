#!/usr/bin/env python3
"""Shared tools for the TikTok parody series (flat cartoon look: burnham.py people, Mossad and The Patriots 2).

Started for "A Professional" so each new film stops copying from the last one. patriots2.py is posted and final, so
it is never changed: what was reusable there (people always with legs, set plans checked for overlaps) lives here
now, plus what the series was missing:
- a perspective camera for sets (`Room`): every location is one plan in metres, and every camera, including the
  reverse angle, draws from that plan, so people's sizes follow their distance and feet always meet the floor;
- a camera that turns the whole drawing (`Turned`), for people tumbling, flying or floating;
- rolled-up sleeves, boots, and a profile head for model sheets;
- the placeholder timeline (lines timed from Sam's natural pace before his recordings arrive);
- the storyboard sheet and the render to MP4.

Read guides/figure-rig.md first.
"""
import math
import os
import re
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import burnham as B
import peepee as PP          # the series' caption, ctext, Rot
import mossad as M           # brows, mouths, hair styles and head tilt (patched into burnham on import)
import figure as F
import kit
import mouths
from ed import INK, curve, oval, soft

kit.install(B)
mouths.install(B)

M_PER_UNIT = 0.00152         # one unit of a burnham person in metres (neck base to soles, 928 units, is 1.41 m)
BOOTS = (92, 62, 40)
SHOES = (22, 20, 22)


# ------------------------------------------------------------------------------------------- sleeves
_STYLE = {'rolled': None}    # set while a person with rolled sleeves is drawn (skin colour)
_arm_inner = B.arm


def _arm(p, sh, el, wr, sleeve, w=30):
    """burnham's sleeve, or (rolled sleeves) the sleeve to just below the elbow, a rolled cuff, a bare forearm."""
    skin = _STYLE['rolled']
    if not skin or w > 40:
        return _arm_inner(p, sh, el, wr, sleeve, w)
    _arm_inner(p, sh, el, wr, skin, w * 0.86)                     # the bare forearm (and elbow) first
    cuff = (el[0] + (wr[0] - el[0]) * 0.22, el[1] + (wr[1] - el[1]) * 0.22)
    dx, dy = sh[0] - el[0], sh[1] - el[1]
    n = math.hypot(dx, dy) or 1
    u = (dx / n, dy / n)
    nx, ny = -u[1], u[0]
    top = (sh[0], sh[1])
    p.poly([(top[0] + nx * w, top[1] + ny * w), (el[0] + nx * w * 0.95, el[1] + ny * w * 0.95),
            (el[0] - nx * w * 0.95, el[1] - ny * w * 0.95), (top[0] - nx * w, top[1] - ny * w)], sleeve, INK, 2.6)
    p.ell(el[0], el[1], w * 0.95, w * 0.95, sleeve, INK, 2.6)
    # the rolled cuff: a fat band across the forearm just below the elbow
    fx, fy = wr[0] - el[0], wr[1] - el[1]
    m = math.hypot(fx, fy) or 1
    v = (fx / m, fy / m)
    vx, vy = -v[1], v[0]
    c0 = (cuff[0] - v[0] * 14, cuff[1] - v[1] * 14)
    p.poly([(c0[0] + vx * w, c0[1] + vy * w), (cuff[0] + vx * w * 0.98, cuff[1] + vy * w * 0.98),
            (cuff[0] - vx * w * 0.98, cuff[1] - vy * w * 0.98), (c0[0] - vx * w, c0[1] - vy * w)], B.lt(sleeve, 1.08), INK, 2.2)


B.arm = _arm


# ------------------------------------------------------------------------------------------- legs
def standing_legs(shoe=SHOES, boots=False, stance=0.0):
    """burnham's standing legs with the footwear chosen (boots have a cuff and a thick sole)."""
    def legs(img, p, sp):
        tc = sp.get('trousers', sp.get('jacket', B.NAVY))
        o = sp.get('stance', stance)
        for sgn in (-1, 1):
            leg = [(sgn * 6, 440), (sgn * 104, 440), (sgn * (100 + o * 0.6), 700), (sgn * (90 + o), 900),
                   (sgn * (30 + o), 902), (sgn * (18 + o * 0.6), 700)]
            p.poly(leg, tc, INK, 2.6)
            soft(img, p.cam, [(sgn * 70, 450), (sgn * 100, 450), (sgn * (88 + o), 896), (sgn * (66 + o), 896)], (0, 0, 0), 0.3, 6)
            if boots:
                p.poly([(sgn * (26 + o), 836), (sgn * (96 + o), 836), (sgn * (98 + o), 900), (sgn * (24 + o), 900)], shoe, INK, 2.4)
                p.line([(sgn * (28 + o), 852), (sgn * (94 + o), 852)], B.dk(shoe, 0.7), 2.0)
            p.poly(curve([(sgn * (24 + o), 896), (sgn * (94 + o), 894), (sgn * (128 + o), 910), (sgn * (124 + o), 928),
                          (sgn * (20 + o), 928)], 4), shoe, INK, 2.4)
            if boots:
                p.line([(sgn * (22 + o), 922), (sgn * (126 + o), 922)], (40, 34, 30), 3.0)
    legs.__name__ = 'legs'
    return legs


def seated_legs(shoe=SHOES):
    """Sitting, seen from the front, with the rig's own leg lengths: hips on the seat (430 units below the neck base),
    thighs coming towards us (seen nearly end-on, so short), knees at 480, shins down to the soles on the floor at
    700 (shin and foot 220, as standing). The seat is 270 units (0.41 m) high."""
    def legs(img, p, sp):
        tc = sp.get('trousers', sp.get('jacket', B.NAVY))
        o = sp.get('knees', 0.0)                    # knees apart (+) or together (-)
        for sgn in (-1, 1):
            p.poly([(sgn * 30, 662), (sgn * (112 + o), 660), (sgn * (110 + o), 482), (sgn * (24 + o * 0.5), 486)], tc, INK, 2.6)
            soft(img, p.cam, [(sgn * (84 + o), 490), (sgn * (110 + o), 490), (sgn * (108 + o), 660), (sgn * 86, 660)],
                 (0, 0, 0), 0.25, 5)
            p.poly(curve([(sgn * 10, 426), (sgn * (118 + o), 426), (sgn * (128 + o), 470), (sgn * (118 + o), 500),
                          (sgn * (22 + o * 0.5), 504), (sgn * 6, 470)], 3), B.dk(tc, 0.92), INK, 2.6)
            p.poly(curve([(sgn * 22, 656), (sgn * 116, 654), (sgn * 128, 672), (sgn * 126, 700), (sgn * 18, 700),
                          (sgn * 14, 676)], 3), shoe, INK, 2.4)
    legs.__name__ = 'legs'
    return legs


SEAT_FEET = 700              # seated: the soles, below the neck base
SEAT_HIP = 430               # seated: the hips on the seat


def walking_legs(phase, stride=46, lift_h=18, shoe=SHOES):
    def legs(img, p, sp):
        tc = sp.get('trousers', (40, 40, 46))
        for k, sgn in enumerate((-1, 1)):
            sw = stride * math.sin(phase + k * math.pi)
            lift = max(0.0, lift_h * math.sin(phase + k * math.pi + 1.2))
            p.poly([(sgn * 6, 440), (sgn * 104, 440), (sgn * 100 + sw * 0.5, 700), (sgn * 90 + sw, 900 - lift),
                    (sgn * 30 + sw, 902 - lift), (sgn * 18 + sw * 0.5, 700)], tc, INK, 2.6)
            p.poly(curve([(sgn * 24 + sw, 896 - lift), (sgn * 94 + sw, 894 - lift), (sgn * 128 + sw, 910 - lift),
                          (sgn * 124 + sw, 928 - lift), (sgn * 20 + sw, 928 - lift)], 4), shoe, INK, 2.4)
    legs.__name__ = 'legs'
    return legs


def person(img, cam, x, y, s, sp, t, legs=None, flip=1):
    """Everyone has legs and feet, always (the set may hide them; nothing here can leave them out).
    legs: None (standing, shoes or sp['boots']), or a legs function from this module."""
    sp = dict(sp, full=True)
    if legs is None:
        legs = standing_legs(sp.get('shoe', SHOES), sp.get('boots', False))
    assert getattr(legs, '__name__', '') == 'legs', 'legs must be drawn'
    keep = B.legs
    B.legs = legs
    _STYLE['rolled'] = sp['skin'] if sp.get('rolled') else None
    where = F.CONTEXT['where']
    F.CONTEXT['where'] = (where + ' ' if where else '') + sp.get('name', 'someone')   # a fault names the person
    try:
        return B.person(img, cam, x, y, s, sp, t, flip)
    finally:
        B.legs = keep
        _STYLE['rolled'] = None
        F.CONTEXT['where'] = where


# ------------------------------------------------------------------------------------------- cameras
class Turned:
    """A camera that turns everything drawn through it by `a` radians about the world point (px, py): for people
    tumbling, flying horizontally or floating (draw them through it as through any camera)."""

    def __init__(self, cam, a, px, py):
        self.cam, self.c, self.s_, self.px, self.py = cam, math.cos(a), math.sin(a), px, py
        self.z, self.s = cam.z, cam.s

    def P(self, x, y):
        dx, dy = x - self.px, y - self.py
        return self.cam.P(self.px + dx * self.c - dy * self.s_, self.py + dx * self.s_ + dy * self.c)

    def S(self, v):
        return self.cam.S(v)


class Room:
    """A perspective camera on one set's plan, in metres: X across the room (to the right, seen from the front),
    Y up from the floor, Z from the front wall into the room. `facing` is 'front' (looking at the front wall) or
    'back' (the reverse angle, looking at the back wall). f: the lens (pixels per metre at one metre away);
    (sx, sy): where the camera's axis meets the picture. Everything is projected into burnham's world units at
    zoom 1, so draw with B.Cam(1.0, 540, 960)."""

    def __init__(self, X, Y, Z, f, facing='front', sx=540, sy=960, tilt=0.0):
        self.X, self.Y, self.Z, self.f, self.facing, self.sx, self.sy, self.tilt = X, Y, Z, f, facing, sx, sy, tilt

    def depth(self, Z):
        return (self.Z - Z) if self.facing == 'front' else (Z - self.Z)

    def P(self, X, Y, Z):
        d = max(0.05, self.depth(Z))
        sgn = 1 if self.facing == 'front' else -1
        return (self.sx + sgn * self.f * (X - self.X) / d, self.sy - self.f * (Y - self.Y) / d + self.tilt * self.f)

    def k(self, Z):
        """Pixels per metre at depth Z."""
        return self.f / max(0.05, self.depth(Z))

    def person(self, X, Z, seated=False):
        """(x, y, s) for burnham: the neck base of someone whose feet are on the floor at (X, Z)."""
        s = self.k(Z) * M_PER_UNIT
        feet = self.P(X, 0.0, Z)
        return feet[0], feet[1] - (SEAT_FEET if seated else F.SOLE_Y) * s, s

    def quad(self, pts):
        return [self.P(*q) for q in pts]


# ------------------------------------------------------------------------------------------- a profile head
def profile_head(img, p, sp, hx, hy, mouth='smile', look=1.0):
    """A head seen side-on, facing to our right (flip the person to face left): brow, nose, lips, chin, the ear, and
    the hair styles our cast use ('swept', 'bob'). For the model sheet's profile view and any side-on shot."""
    skin, hc = sp['skin'], sp.get('hair_c', (60, 44, 34))
    hh = sp.get('hh', 90)
    st = sp.get('hair')
    if st == 'bob':
        p.poly(curve([(hx - 70, hy - 70), (hx - 92, hy + 20), (hx - 70, hy + 108), (hx + 10, hy + 112), (hx + 4, hy - 100),
                      (hx - 30, hy - hh - 14)], 4), hc, INK, 2.6)
    face_pts = [(hx - 62, hy - 70), (hx - 40, hy - hh - 6), (hx + 20, hy - hh - 4), (hx + 58, hy - 56), (hx + 66, hy - 24),
                (hx + 64, hy - 6), (hx + 86, hy + 30), (hx + 66, hy + 36), (hx + 70, hy + 52), (hx + 64, hy + 60),
                (hx + 68, hy + 74), (hx + 56, hy + 98), (hx + 20, hy + 104), (hx - 20, hy + 86), (hx - 60, hy + 40)]
    p.poly(curve(face_pts, 3), skin, INK, 2.6)
    p.poly(oval(hx - 16, hy + 8, 12, 22), skin, INK, 2.2)                                 # the ear
    p.line([(hx - 18, hy - 4), (hx - 12, hy + 12)], B.dk(skin, 0.8), 1.6)
    soft(img, p.cam, [(hx - 50, hy - 40), (hx - 10, hy - 30), (hx - 20, hy + 70), (hx - 54, hy + 40)], (160, 100, 90), 0.2, 8)
    ex, ey = hx + 40, hy - 10                                                              # the eye, side-on
    p.poly([(ex - 10, ey), (ex + 2, ey - 7), (ex + 12, ey - 2), (ex + 4, ey + 5)], (250, 250, 248), INK, 1.8)
    p.ell(ex + 4 + 2 * look, ey - 1, 3.4, 3.4, INK, None)
    bc = sp.get('brow_c', B.dk(hc, 0.8))
    p.line([(ex - 12, ey - 18), (ex + 2, ey - 22), (ex + 16, ey - 18)], bc, 3.2)
    if mouth == 'grin':
        p.poly([(hx + 50, hy + 54), (hx + 68, hy + 50), (hx + 64, hy + 64), (hx + 50, hy + 64)], (250, 250, 246), INK, 1.8)
        p.line([(hx + 40, hy + 46), (hx + 50, hy + 54)], INK, 2.0)
    else:
        p.line([(hx + 46, hy + 60), (hx + 66, hy + 58)], INK, 2.2)
    if st == 'swept':
        p.poly(curve([(hx - 66, hy - 30), (hx - 70, hy - 80), (hx - 30, hy - hh - 22), (hx + 30, hy - hh - 30),
                      (hx + 70, hy - hh + 4), (hx + 52, hy - hh + 14), (hx + 30, hy - hh + 20), (hx - 10, hy - 56),
                      (hx - 30, hy - 20), (hx - 50, hy - 4)], 3), hc, INK, 2.6)
        for k in range(3):
            p.line([(hx - 30 + 22 * k, hy - hh - 10 + 4 * k), (hx + 30 + 16 * k, hy - hh - 2 + 6 * k)], B.dk(hc, 0.72), 1.8)
    elif st == 'bob':
        p.poly(curve([(hx - 66, hy - 60), (hx - 40, hy - hh - 14), (hx + 30, hy - hh - 10), (hx + 64, hy - 60),
                      (hx + 50, hy - 50), (hx + 10, hy - hh + 20), (hx - 30, hy - 40), (hx - 40, hy + 30), (hx - 64, hy + 30)], 3),
               hc, INK, 2.6)
    if sp.get('earring'):
        p.ell(hx - 18, hy + 34, 4, 4, B.GOLD, INK, 1.2)


# ------------------------------------------------------------------------------------------- captions
def caption(img, s, italic=False):
    """The series' speech caption (bold white, black outline, centred on x = 540, at most 700 px wide)."""
    PP.caption(img, s, italic=italic)


def shout(img, s, bottom=1480):
    """A shouted line: big Anton capitals, white with a heavy outline, centred on x = 540, at most 700 px and 2 rows."""
    S = B.SS
    size = 110
    while True:
        f = ImageFont.truetype(B.ANTON, size * S)
        rows = B.wrap(s, f, 700 * S)
        if len(rows) <= 2 and max(f.getbbox(r)[2] for r in rows) <= 700 * S:
            break
        size -= 4
    d = ImageDraw.Draw(img)
    top = bottom - len(rows) * size * 1.08 - size * 0.12
    for i, row in enumerate(rows):
        d.text((540 * S, (top + i * size * 1.08) * S), row, font=f, fill=(255, 255, 255), anchor='ma',
               stroke_width=int(size * 0.07) * S, stroke_fill=(0, 0, 0))


# ------------------------------------------------------------------------------------------- placeholder timing
def word_times(start, wps, pieces, stop=0.32, comma=0.15):
    """[(word, start, end, piece index)] from a natural pace (words a second), with pauses after punctuation."""
    out, t = [], start
    for i, piece in enumerate(pieces):
        for w in piece.split():
            d = (0.62 + 0.38 * min(2.0, len(re.sub(r'\W', '', w)) / 4.5)) / wps
            out.append((w, t, t + d, i))
            t += d
            if w[-1] in '.?!:':
                t += stop
            elif w[-1] in ',;' or w.endswith('...'):
                t += comma
    return out


def stretches(words, gap=0.12):
    """The stretches of speech (start, end) in a placeholder line: words joined unless a pause separates them."""
    out = []
    for _, a, b, _ in words:
        if out and a - out[-1][1] < gap:
            out[-1] = (out[-1][0], b)
        else:
            out.append((a, b))
    return out


# ------------------------------------------------------------------------------------------- sheets and render
def sheet(stills, dst, cols=6, cw=360, ch=640, title=None):
    """A storyboard (or model) sheet: [(label, image)] in a grid, labels underneath."""
    lab = 92
    rows = (len(stills) + cols - 1) // cols
    top = 70 if title else 0
    sh = Image.new('RGB', (cols * (cw + 16) + 16, top + rows * (ch + lab + 12) + 16), (245, 242, 236))
    d = ImageDraw.Draw(sh)
    f = ImageFont.truetype(B.SANS, 20)
    if title:
        d.text((18, 18), title, font=ImageFont.truetype(B.SANS, 34), fill=(20, 20, 20))
    for i, (name, im) in enumerate(stills):
        x, y = 16 + (i % cols) * (cw + 16), top + 16 + (i // cols) * (ch + lab + 12)
        sh.paste(im.convert('RGB').resize((cw, ch), Image.LANCZOS), (x, y))
        rows_ = B.wrap(name, f, cw - 4)
        for k, r in enumerate(rows_[:3]):
            d.text((x + 2, y + ch + 8 + 25 * k), r, font=f, fill=(20, 20, 20))
    sh.save(dst, quality=88)


def render(frame_image, soundtrack, dur, out, size, crf, ss, fps=12):
    """Draw every frame (all cores), add the soundtrack, encode an MP4."""
    import imageio_ffmpeg
    from multiprocessing import Pool
    import mossad_audio as MA
    wav = out + '.wav'
    mix = soundtrack()
    print(f'sound: {MA.lufs(mix):.1f} LUFS, peak {MA.true_peak_db(mix):.1f} dBTP', flush=True)
    MA.write_wav(wav, mix)
    n = int(round(dur * fps))
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{size[0]}x{size[1]}', '-r', str(fps), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    global _FRAME
    _FRAME = (frame_image, size, ss, fps)
    with Pool(os.cpu_count()) as pool:
        for i, fr in enumerate(pool.imap(_render_one, range(n), chunksize=2)):
            p.stdin.write(fr)
            if i % 48 == 0:
                print(f'frame {i}/{n}', flush=True)
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print(f'done: {out} ({os.path.getsize(out) / 1e6:.1f} MB)', flush=True)


_FRAME = None


def _render_one(i):
    frame_image, size, ss, fps = _FRAME
    B.SS = ss
    return np.asarray(frame_image(i / fps).convert('RGB').resize(size, Image.LANCZOS)).tobytes()
