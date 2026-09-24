#!/usr/bin/env python3
"""Oxford Rap Battle: a penguin in a check shirt takes apart a pigeon in a blue jumper.

The real battle audio plays unchanged. Most lines are shown literally as rough pencil
cutaways; the rest of the time we are in the common room with a crowd of birds.

Usage:
    python3 rap.py stills OUT_DIR T1 T2 ...   # single frames at given seconds
    python3 rap.py render OUT.mp4 [CRF]       # the full video with sound
"""
import json
import math
import os
import sys

os.environ.setdefault('PENCIL_W', '1280')
os.environ.setdefault('PENCIL_H', '720')
os.environ.setdefault('PENCIL_FPS', '8')

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from pencil import Canvas, blob, clamp01, col, ell, lerp, render_video, sstep, W, H, FPS, SR  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 239.4
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
INK = col(0.13, 0.12, 0.13)
BLACK = col(0.14, 0.14, 0.16)
WHITE = col(1.0, 1.0, 1.0)
PAPER_W = col(0.97, 0.95, 0.90)
ORANGE = col(0.98, 0.58, 0.16)
PLAID = col(0.70, 0.79, 0.93)
PLAID_D = col(0.36, 0.48, 0.74)
JUMPER = col(0.55, 0.69, 0.88)
JUMPER_D = col(0.40, 0.54, 0.76)
PIGEON = col(0.62, 0.64, 0.70)
PIGEON_D = col(0.45, 0.47, 0.53)
NECK_G = col(0.30, 0.58, 0.46)
NECK_P = col(0.55, 0.36, 0.62)
PINK = col(0.92, 0.55, 0.62)
EYE_O = col(0.96, 0.52, 0.16)
WALL = col(0.93, 0.87, 0.71)
WOOD = col(0.58, 0.40, 0.22)
WOOD_D = col(0.38, 0.25, 0.14)
AMBER = col(1.0, 0.82, 0.48)
BENCH = col(0.74, 0.26, 0.36)
CARPET = col(0.46, 0.32, 0.28)
NAVY = col(0.14, 0.17, 0.30)
RED = col(0.86, 0.20, 0.18)
GREEN = col(0.35, 0.62, 0.30)
YELLOW = col(0.99, 0.86, 0.30)
GREY = col(0.62, 0.62, 0.64)
SICK = col(0.62, 0.72, 0.30)
BROWN = col(0.47, 0.33, 0.18)
SKY = col(0.78, 0.88, 0.96)
TAN = col(0.85, 0.72, 0.5)


class Sketch(Canvas):
    """Steady pencil: each shape keeps exactly the same slight hand-drawn wobble in every frame,
    and the paper grain never moves, so only things that really move change on screen."""
    def __init__(self, d):
        super().__init__(d)
        self.goff = [(40, 70), (90, 20), (10, 110)]
        self._seed = 0

    def rng(self):
        return np.random.default_rng(self._seed)

    def poly(self, pts, fill=None, line=None, lw=5, pressure=0.85, lp=0.95, jit=2.2, **kw):
        p = np.asarray(pts, np.float64)
        self._seed = int(abs(np.round(p[:3] / 4).sum() * 7919 + len(p) * 104729)) % (2 ** 32)
        super().poly(pts, fill, line, lw=lw, pressure=max(pressure, 1.35), lp=max(lp, 1.3), jit=jit * 0.5, **kw)

    def hatch(self, pts, color, **kw):
        p = np.asarray(pts, np.float64)
        self._seed = int(abs(np.round(p[:3] / 4).sum() * 131 + len(p))) % (2 ** 32)
        super().hatch(pts, color, **kw)


def E(cx, cy, rx, ry, rot=0.0, n=28):
    return ell(cx, cy, rx, ry, rot, n)


def text(c, s, x, y, size, colr, rot=0.0, opacity=1.0):
    """Hand-lettered-ish text through the pencil grain (world coords)."""
    sc, ox, oy = c.cam
    X, Y, S = x * sc + ox, y * sc + oy, max(6, int(size * sc))
    font = ImageFont.truetype(FONT, S)
    l, t_, r, b = font.getbbox(s)
    pad = 8
    im = Image.new('L', (r - l + 2 * pad, b - t_ + 2 * pad), 0)
    ImageDraw.Draw(im).text((pad - l, pad - t_), s, font=font, fill=255)
    if rot:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    w, h = im.size
    x0, y0 = int(X - w / 2), int(Y - h / 2)
    m = np.asarray(im, np.float32) / 255
    cx0, cy0 = max(0, x0), max(0, y0)
    cx1, cy1 = min(W, x0 + w), min(H, y0 + h)
    if cx1 <= cx0 or cy1 <= cy0:
        return
    m = m[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0]
    c._apply(m, cx0, cy0, colr, 1.05, opacity, 0)


# ---------------------------------------------------------------------------
# Timing: lyric lines and the shot list
# ---------------------------------------------------------------------------
SHOTS = [
    (0, 8.2, 'examine'), (8.2, 10.9, 'stage'), (10.9, 13.3, 'lullaby'), (13.3, 17.7, 'nullified'),
    (17.7, 22.9, 'supervision'), (22.9, 25.2, 'permission'), (25.2, 27.7, 'dish'), (27.7, 32.5, 'scrub'),
    (32.5, 35.1, 'surgery'), (35.1, 38.6, 'reporter'), (38.6, 42.7, 'waxwork'), (42.7, 45.5, 'stage'),
    (45.5, 48.2, 'vanity'), (48.2, 52.1, 'yeti'), (52.1, 55.6, 'weak'), (55.6, 60.6, 'vomit'),
    (60.6, 66.6, 'lost'), (66.6, 72.9, 'stage'), (72.9, 75.93, 'eagle'), (75.93, 79.16, 'defiled'), (79.16, 85.8, 'chin'),
    (85.8, 89.6, 'yarn'), (89.6, 93.7, 'gasp'), (93.7, 97.5, 'stage'), (97.5, 99.3, 'noggin'), (99.3, 103.6, 'stage'),
    (103.6, 105.0, 'corn'), (105.0, 107.0, 'stage'), (107.0, 109.3, 'veal'), (109.3, 112.9, 'keepreal'), (112.9, 122.8, 'pillow'),
    (122.8, 126.4, 'pipe'), (126.4, 129.1, 'innate'), (129.1, 132.2, 'mistakes'), (132.2, 139.8, 'gasp'),
    (139.8, 141.9, 'wait'), (141.9, 147.4, 'firesale'), (147.4, 150.0, 'crake'), (150.0, 151.2, 'gasp'),
    (151.2, 162.54, 'crap'), (162.54, 166.2, 'blackeye'), (166.2, 168.9, 'factory'), (168.9, 171.9, 'gasp'),
    (171.9, 175.9, 'practice'), (175.9, 185.9, 'collapse'), (185.9, 191.7, 'expectations'), (191.7, 195.6, 'integrity'),
    (195.6, 197.7, 'dinner'), (197.7, 201.1, 'podium'), (201.1, 206.4, 'sunday'), (206.4, 211.6, 'hit'),
    (211.6, 213.3, 'snap'), (213.3, 217.9, 'gasp'), (217.9, 221, 'spectacle'), (221, 224.5, 'rentafool'), (224.5, 227.9, 'miracles'),
    (227.9, DUR + 1, 'finale'),
]


def shot_at(t):
    for a, b, name in SHOTS:
        if a <= t < b:
            return a, b, name
    return SHOTS[-1]


# loudness of the real audio, for the penguin's beak and the crowd
def _load_audio():
    import subprocess
    import imageio_ffmpeg
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-i',
                          os.path.join(HERE, 'audio', 'rap-battle.m4a'), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float64) / 32767
    n = SR // 24
    env = np.array([np.sqrt((x[i:i + n] ** 2).mean()) for i in range(0, len(x) - n, n)])
    med = np.median(env)
    return np.clip((env - med * 0.6) / (env.max() * 0.55 - med * 0.6), 0, 1)


LOUD = _load_audio()


def loud(t):
    i = int(t * 24)
    return float(LOUD[i]) if 0 <= i < len(LOUD) else 0.0


# every rapped word with its timing, and the bits nobody could make out
_WD = json.load(open(os.path.join(HERE, 'data', 'rap_words.json')))
WORDS, LINE_STARTS = _WD['words'], set(_WD['line_starts'])
UNINTELLIGIBLE = [tuple(f) for f in _WD['flashes']]


def line_subs(wd):
    """One subtitle per lyric line, shown from the moment the line starts until the next one does."""
    starts = wd['line_starts'] + [len(wd['words'])]
    lines = []
    for k, t0 in enumerate(wd['line_times']):
        words = [w[0] for w in wd['words'][starts[k]:starts[k + 1]] if w[0] != '*']
        if t0 is None or not words:
            continue
        txt = ' '.join(words)
        shown = (wd.get('line_text') or [None] * len(wd['line_times']))[k]  # the script, with its punctuation
        lines.append([t0, t0 + 3.5 + 0.6 * len(words), shown or txt[0].upper() + txt[1:]])
    for k in range(len(lines) - 1):
        lines[k][1] = min(lines[k][1], lines[k + 1][0])
    return [tuple(x) for x in lines]


SUBS = line_subs(_WD)


def _speaking(t):
    """How far into the current spoken word (or unintelligible bit) we are, or None between words."""
    for a, b in UNINTELLIGIBLE:
        if a <= t < b:
            return t - a
    for w, a, b in WORDS:
        if a <= t < a + min(b - a, 0.6) + 0.05:
            return t - a
    return None


def beak_open(t):
    """The penguin's beak flaps open and shut, frame by frame, for every word he raps."""
    p = _speaking(t)
    if p is None:
        return 0.0
    return (1.0 if loud(t) > 0.45 else 0.7) if int(p * FPS) % 2 == 0 else 0.1


# ---------------------------------------------------------------------------
# Characters
# ---------------------------------------------------------------------------
class Rig:
    """Local drawing space for a character: u forward (towards facing), v up, 1 unit = s pixels."""
    def __init__(self, c, x, y, s, face=1, lean=0.0):
        self.c, self.x, self.y, self.s, self.face = c, x, y, s, face
        self.ca, self.sa = math.cos(math.radians(lean)), math.sin(math.radians(lean))
        self.ux = 1.0  # squeeze sideways (T is a slim chap)

    def P(self, u, v):
        u = u * self.ux
        u, v = u * self.ca + v * self.sa, -u * self.sa + v * self.ca
        return self.x + u * self.face * self.s, self.y - v * self.s

    def pts(self, lst):
        return [self.P(u, v) for u, v in lst]

    def E(self, u, v, rx, ry, rot=0.0, n=26):
        r = math.radians(rot)
        return [self.P(u + rx * math.cos(q) * math.cos(r) - ry * math.sin(q) * math.sin(r),
                       v + rx * math.cos(q) * math.sin(r) + ry * math.sin(q) * math.cos(r))
                for q in np.linspace(0, 2 * math.pi, n, endpoint=False)]

    def lw(self, k=1.0):
        return max(1.5, self.s * 0.012 * k)


def smooth(pts, n=6, closed=True):
    """Catmull-Rom smoothing: turns a handful of points into a flowing pencil curve."""
    p = np.asarray(pts, float)
    m = len(p)
    out = []
    rng = range(m) if closed else range(m - 1)
    for i in rng:
        p0 = p[i - 1] if (closed or i > 0) else p[0]
        p1, p2 = p[i], p[(i + 1) % m]
        p3 = p[(i + 2) % m] if (closed or i + 2 < m) else p[-1]
        for tq in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = tq * tq, tq * tq * tq
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * tq + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed:
        out.append(p[-1])
    return out


def limb(r, shoulder, ang, length, w0, w1, colr, sleeve=None, sleeve_frac=0.55, sleeve_d=None, bars=False):
    """A rounded flipper/wing from shoulder at angle (0 = hanging down, 90 = forward, 180 = up),
    with an optional sleeve over its upper part."""
    a = math.radians(ang)
    dx, dy = math.sin(a), -math.cos(a)
    sx, sy = shoulder
    nx, ny = -dy, dx

    def along(q, w):
        return (sx + dx * length * q + nx * w, sy + dy * length * q + ny * w)
    prof = [0.0, 0.2, 0.45, 0.7, 0.9, 1.0]
    wid = [w0, w0 * 1.1, w1 * 1.15, w1 * 0.9, w1 * 0.5, 0.0]
    side1 = [along(q, w) for q, w in zip(prof, wid)]
    side2 = [along(q, -w) for q, w in zip(prof[::-1], wid[::-1])][1:]
    shape = smooth(side1 + side2 + [along(-0.05, 0.0)], 5)
    r.c.poly(r.pts(shape), fill=colr, line=INK, lw=r.lw())
    if bars:  # a pigeon's two dark wing bars
        for q in (0.72, 0.82):
            r.c.line(r.pts([along(q, wid[3] * 0.8), along(q + 0.03, 0), along(q, -wid[3] * 0.8)]), PIGEON_D, lw=r.lw(1.6))
    if sleeve is not None:
        L = sleeve_frac
        sl = smooth([along(-0.06, w0 * 1.25), along(L * 0.5, w0 * 1.3), along(L, w0 * 1.2), along(L + 0.03, 0),
                     along(L, -w0 * 1.2), along(L * 0.5, -w0 * 1.3), along(-0.06, -w0 * 1.25)], 5)
        r.c.poly(r.pts(sl), fill=sleeve, line=INK, lw=r.lw())
        if sleeve_d is not None:
            r.c.hatch(r.pts(sl), sleeve_d, spacing=r.s * 0.055, angle=math.degrees(a), lw=r.lw(0.55), opacity=0.8)
            r.c.hatch(r.pts(sl), sleeve_d, spacing=r.s * 0.055, angle=math.degrees(a) + 90, lw=r.lw(0.55), opacity=0.8)
        r.c.line(r.pts(smooth([along(L - 0.05, w0 * 1.15), along(L - 0.02, 0), along(L - 0.05, -w0 * 1.15)], 5, False)),
                 INK, lw=r.lw(0.8))
    return along(1.0, 0.0)


def ell_pts(cu, cv, ru, rv, a0, a1, n=20):
    return [(cu + ru * math.cos(q), cv + rv * math.sin(q)) for q in np.linspace(a0, a1, n)]


EAGLE_BROWN = col(0.33, 0.22, 0.13)
EAGLE_BELLY = col(0.45, 0.31, 0.18)
EAGLE_GOLD = col(0.99, 0.78, 0.15)


def penguin(c, x, y, s, face=-1, arms=(10, 10), lean=0.0, beak=0.0, eye='normal', shirt=True, hat=None,
            prop=None, eagle=False):
    """The rapper: a penguin in a light blue check shirt, sleeves rolled. arms = (front, back) flipper angles.
    eagle=True makes him a bald-eagle penguin: brown body, white head, golden hooked beak, fierce brow."""
    s *= 1.15  # tall and slim: stands as tall as the pigeon
    r = Rig(c, x, y, s, face, lean)
    lw = r.lw()
    body_c = EAGLE_BROWN if eagle else BLACK
    feet_c = EAGLE_GOLD if eagle else ORANGE
    SLIM = 0.74
    back = limb(r, (-0.13 * SLIM, 0.7), arms[1], 0.44 * (1.25 if eagle else 1), 0.075, 0.07 * (1.4 if eagle else 1), body_c,
                PLAID if shirt else None, sleeve_d=PLAID_D)
    r.ux = SLIM
    for du in (-0.1, 0.12):
        c.poly(r.pts(smooth([(du - 0.1, 0.0), (du + 0.13, 0.0), (du + 0.1, 0.05), (du - 0.08, 0.05)], 4)), fill=feet_c,
               line=INK, lw=lw)
        if eagle:  # talons
            for k in range(3):
                c.line(r.pts([(du + 0.02 + 0.04 * k, 0.01), (du + 0.05 + 0.04 * k, -0.02)]), INK, lw=lw)
    # a plump, egg-shaped body, black behind and white in front
    c.poly(r.E(0, 0.46, 0.31, 0.46, 0, 40), fill=body_c, line=INK, lw=lw)
    c.poly(r.E(0.08, 0.42, 0.21, 0.37, 0, 36), fill=EAGLE_BELLY if eagle else WHITE, line=INK, lw=lw * 0.6)
    if eagle:
        c.hatch(r.E(0.08, 0.42, 0.21, 0.37, 0, 36), EAGLE_BROWN, spacing=s * 0.05, angle=60, lw=lw * 0.5, opacity=0.5)
    if shirt:
        # the shirt follows the curve of his body, from shoulders to hips, open at the collar
        top = ell_pts(0, 0.46, 0.315, 0.465, math.radians(20), math.radians(160), 18)
        shirt_pts = [(u, v) for u, v in top if v > 0.0] + ell_pts(0, 0.46, 0.315, 0.465, math.radians(160),
                                                               math.radians(200), 6)
        shirt_pts = ell_pts(0, 0.46, 0.318, 0.47, math.radians(-25), math.radians(205), 36)
        hem = smooth([(-0.29, 0.26), (-0.1, 0.19), (0.12, 0.19), (0.29, 0.26)], 5, False)
        poly = [(u, max(v, 0.22)) for u, v in shirt_pts] + hem[::-1]
        poly = [(u, v) for u, v in poly if v >= 0.18]
        c.poly(r.pts(poly), fill=PLAID, line=INK, lw=lw)
        c.hatch(r.pts(poly), PLAID_D, spacing=s * 0.065, angle=0, lw=lw * 0.55, opacity=0.85)
        c.hatch(r.pts(poly), PLAID_D, spacing=s * 0.065, angle=90, lw=lw * 0.55, opacity=0.85)
        # open collar: a white V of penguin chest, with the collar points folded over
        c.poly(r.pts(smooth([(0.02, 0.86), (0.2, 0.84), (0.12, 0.6)], 4)), fill=WHITE, line=INK, lw=lw * 0.8)
        c.poly(r.pts([(0.0, 0.86), (0.08, 0.72), (0.13, 0.84)]), fill=PLAID, line=INK, lw=lw)
        c.poly(r.pts([(0.2, 0.84), (0.17, 0.7), (0.26, 0.78)]), fill=PLAID, line=INK, lw=lw)
        c.line(r.pts([(0.12, 0.6), (0.14, 0.2)]), PLAID_D, lw=lw * 0.8)  # the button placket
        for v in (0.5, 0.4, 0.3):
            c.poly(r.E(0.125 + (0.6 - v) * 0.05, v, 0.013, 0.013, 0, 8), fill=WHITE, line=INK, lw=lw * 0.4)
        c.poly(r.pts([(-0.14, 0.62), (-0.03, 0.62), (-0.03, 0.52), (-0.14, 0.52)]), None, INK, lw=lw * 0.6)  # pocket
    # head, with the eye ring and a very expressive brow
    r.ux = 0.88
    hu, hv = 0.04, 0.97
    if eagle:  # a proud white head with a ruff of feathers at the neck
        ruff = [(hu + 0.24 * math.cos(q), hv - 0.02 + 0.23 * math.sin(q) - (0.04 if k % 2 else 0) * (math.sin(q) < -0.3))
                for k, q in enumerate(np.linspace(0, 2 * math.pi, 22, endpoint=False))]
        c.poly(r.pts(ruff), fill=WHITE, line=INK, lw=lw)
    else:
        c.poly(r.E(hu, hv, 0.21, 0.195, 0, 32), fill=BLACK, line=INK, lw=lw)
    c.poly(r.E(hu + 0.1, hv + 0.03, 0.068, 0.062, 0, 20), fill=EAGLE_GOLD if eagle else WHITE, line=INK, lw=lw * 0.6)
    if eye == 'closed':
        c.line(r.pts(smooth([(hu + 0.055, hv + 0.03), (hu + 0.1, hv + 0.055), (hu + 0.145, hv + 0.03)], 4, False)), INK,
               lw=lw * 1.2)
    else:
        pr = 0.03 if eye != 'wide' else 0.022
        c.poly(r.E(hu + 0.118, hv + 0.028, pr, pr, 0, 12), fill=INK)
        c.poly(r.E(hu + 0.126, hv + 0.038, pr * 0.35, pr * 0.35, 0, 8), fill=WHITE)
    if eye in ('smug', 'angry') or eagle:
        tilt = 0.035 if (eye == 'angry' or eagle) else -0.022
        c.line(r.pts([(hu + 0.03, hv + 0.085 + tilt), (hu + 0.17, hv + 0.085 - tilt)]), INK if eagle else WHITE,
               lw=lw * (2.4 if eagle else 1.8))
    # beak: upper mandible, and a lower one that drops open with the words
    bu, bv = hu + 0.18, hv - 0.02
    # lower mandible first, so the upper one sits over its hinge; nothing fills the gap between them
    a = math.radians(-10 - 32 * beak)
    tip = (bu + 0.16 * math.cos(a), bv - 0.012 + 0.16 * math.sin(a))
    c.poly(r.pts(smooth([(bu - 0.03, bv - 0.012), tip, (bu - 0.03, bv - 0.048)], 3)),
           fill=col(0.85, 0.62, 0.1) if eagle else col(0.9, 0.46, 0.1), line=INK, lw=lw)
    if eagle:  # a heavy hooked raptor's beak
        c.poly(r.pts(smooth([(bu - 0.04, bv + 0.07), (bu + 0.12, bv + 0.06), (bu + 0.22, bv + 0.0), (bu + 0.2, bv - 0.07),
                             (bu + 0.14, bv - 0.01), (bu - 0.04, bv - 0.01)], 4)), fill=EAGLE_GOLD, line=INK, lw=lw)
    else:
        c.poly(r.pts(smooth([(bu - 0.03, bv + 0.05), (bu + 0.09, bv + 0.035), (bu + 0.2, bv - 0.005),
                             (bu - 0.03, bv - 0.01)], 4)), fill=ORANGE, line=INK, lw=lw)
    if hat == 'surgeon':
        c.poly(r.pts(smooth([(hu - 0.2, hv + 0.08), (hu, hv + 0.25), (hu + 0.2, hv + 0.1), (hu, hv + 0.12)], 4)),
               fill=col(0.55, 0.78, 0.72), line=INK, lw=lw)
    if hat == 'nightcap':
        c.poly(r.pts([(hu - 0.2, hv + 0.08), (hu + 0.18, hv + 0.14), (hu - 0.35, hv + 0.35)]), fill=col(0.5, 0.6, 0.9),
               line=INK, lw=lw)
    r.ux = 1.0
    front = limb(r, (0.1 * SLIM, 0.7), arms[0], 0.44 * (1.25 if eagle else 1), 0.075, 0.07 * (1.4 if eagle else 1), body_c,
                 PLAID if shirt else None, sleeve_d=PLAID_D)
    return r, front, back


def pigeon(c, x, y, s, face=1, arms=(15, 15), lean=0.0, mood='neutral', knees=0.0, t=0.0, jumper=True,
           head_tilt=0.0, beak=None, blackeye=0.0):
    """The opponent: a pigeon with a little belly, in a sky-blue V-neck jumper.
    mood: neutral, grin, smirk, sick, laugh, shock, hurt, dizzy, sleepy, cross. blackeye: 0..1 how bad the shiner is."""
    r = Rig(c, x, y, s, face, lean)
    lw = r.lw()
    wob = knees * 0.05 * math.sin(t * 40)
    # pink legs and splayed toes (knocking together when his knees go)
    for du in (-0.08, 0.1):
        c.line(r.pts([(du, 0.02), (du + wob + (0.03 if knees else 0) * (1 if du < 0 else -1), 0.1), (du, 0.2)]), PINK,
               lw=s * 0.032)
        for k in (-1, 0, 1):
            c.line(r.pts([(du, 0.02), (du + 0.07 + 0.02 * k, 0.0 - 0.012 * abs(k))]), PINK, lw=s * 0.02)
    c.poly(r.pts(smooth([(-0.25, 0.36), (-0.56, 0.22), (-0.55, 0.13), (-0.2, 0.24)], 4)), fill=PIGEON_D, line=INK, lw=lw)
    limb(r, (-0.12, 0.74), arms[1], 0.46, 0.085, 0.08, PIGEON, JUMPER if jumper else None, 0.62, bars=True)
    # a trim body with just a little belly, in a fine-knit sky-blue V-neck
    body = smooth([(-0.24, 0.32), (-0.24, 0.6), (-0.13, 0.82), (0.08, 0.86), (0.22, 0.74), (0.25, 0.55), (0.29, 0.36),
                   (0.2, 0.16), (0.0, 0.1), (-0.18, 0.15)], 6)
    # grey neck feathers (just a hint of a pigeon's sheen), showing in the V of the jumper
    c.poly(r.pts(smooth([(-0.03, 0.78), (0.0, 0.98), (0.12, 1.02), (0.23, 0.93), (0.23, 0.76), (0.1, 0.72)], 5)),
           fill=PIGEON, line=INK, lw=lw)
    c.poly(r.pts(smooth([(0.04, 0.86), (0.1, 0.95), (0.19, 0.9), (0.17, 0.83)], 4)), fill=NECK_P, opacity=0.25)
    c.poly(r.pts(body), fill=JUMPER if jumper else PIGEON, line=INK, lw=lw)
    if jumper:
        c.hatch(r.pts(body), JUMPER_D, spacing=s * 0.03, angle=90, lw=lw * 0.35, opacity=0.18)  # fine knit
        hem = smooth([(-0.19, 0.2), (0.0, 0.14), (0.22, 0.2)], 5, False)
        c.line(r.pts(hem), JUMPER_D, lw=s * 0.03)
        vneck = smooth([(-0.06, 0.845), (0.04, 0.8), (0.1, 0.64), (0.16, 0.76), (0.2, 0.8)], 4, False)
        c.poly(r.pts([(-0.06, 0.845), (0.1, 0.64), (0.21, 0.79), (0.08, 0.865)]), fill=PIGEON)
        c.line(r.pts(vneck), JUMPER_D, lw=s * 0.025)
    else:
        c.poly(r.pts(smooth([(-0.03, 0.78), (0.0, 0.98), (0.12, 1.02), (0.23, 0.93), (0.23, 0.76), (0.1, 0.72)], 5)),
               fill=PIGEON, line=INK, lw=lw)
    # a small round head
    hu, hv = 0.12 + 0.05 * head_tilt, 1.1
    c.poly(r.E(hu, hv, 0.15, 0.14, 0, 30), fill=SICK if mood == 'sick' else PIGEON, line=INK, lw=lw)
    eu, ev = hu + 0.06, hv + 0.03
    if mood in ('laugh', 'sleepy'):
        c.line(r.pts(smooth([(eu - 0.04, ev), (eu, ev + 0.03), (eu + 0.04, ev)], 4, False)), INK, lw=lw * 1.3)
    elif mood == 'dizzy':
        c.line(r.pts([(eu - 0.03, ev - 0.03), (eu + 0.03, ev + 0.03)]), INK, lw=lw)
        c.line(r.pts([(eu - 0.03, ev + 0.03), (eu + 0.03, ev - 0.03)]), INK, lw=lw)
    else:
        er = 0.052 if mood == 'shock' else 0.042
        c.poly(r.E(eu, ev, er, er, 0, 16), fill=EYE_O, line=INK, lw=lw * 0.6)
        pr = 0.011 if mood == 'shock' else 0.02
        c.poly(r.E(eu + 0.008, ev, pr, pr, 0, 10), fill=INK)
    if blackeye > 0:  # a proper shiner: swollen, purple-black in the middle, yellow-green at the edges
        c.poly(r.E(eu, ev, 0.085 * (0.8 + 0.2 * blackeye), 0.075, 0, 20), fill=col(0.75, 0.78, 0.35), opacity=0.7 * blackeye)
        c.poly(r.E(eu, ev, 0.068, 0.06, 0, 20), fill=col(0.38, 0.2, 0.42), opacity=0.9 * blackeye)
        c.poly(r.E(eu, ev - 0.005, 0.05, 0.045, 0, 20), fill=col(0.2, 0.1, 0.22), opacity=blackeye)
        c.poly(r.E(eu + 0.005, ev - 0.012, 0.03, 0.012, 0, 12), fill=col(0.95, 0.9, 0.85), line=INK, lw=lw * 0.5)
        c.poly(r.E(eu + 0.008, ev - 0.012, 0.009, 0.009, 0, 8), fill=INK)
        c.line(r.pts(smooth([(eu - 0.04, ev + 0.0), (eu, ev + 0.012), (eu + 0.04, ev + 0.0)], 4, False)), INK, lw=lw)
    if mood in ('cross', 'angry'):
        c.line(r.pts([(eu - 0.06, ev + 0.075), (eu + 0.05, ev + 0.035)]), INK, lw=lw * 1.6)
    if mood == 'smirk':
        c.line(r.pts([(eu - 0.05, ev + 0.05), (eu + 0.05, ev + 0.06)]), INK, lw=lw * 1.2)
    if mood == 'brow':  # one sceptical raised eyebrow
        c.line(r.pts(smooth([(eu - 0.05, ev + 0.07), (eu, ev + 0.1), (eu + 0.05, ev + 0.08)], 3, False)), INK, lw=lw * 1.3)
    if mood in ('grin', 'laugh', 'smirk'):
        c.line(r.pts(smooth([(hu - 0.03, hv - 0.06), (hu + 0.05, hv - 0.1), (hu + 0.13, hv - 0.065)], 4, False)), INK,
               lw=lw)
    if mood == 'hurt':
        c.line(r.pts([(eu - 0.05, ev + 0.075), (eu + 0.05, ev + 0.045)]), INK, lw=lw * 1.3)
    if mood == 'sick':
        c.poly(r.E(hu - 0.02, hv - 0.05, 0.06, 0.04), fill=col(0.5, 0.66, 0.22), opacity=0.7)
        c.poly(r.E(hu + 0.02, hv - 0.02, 0.05, 0.035), fill=col(0.5, 0.66, 0.22), opacity=0.7)
    op = {'laugh': 0.6, 'shock': 0.7, 'sick': 0.35, 'grin': 0.2}.get(mood, 0.0) if beak is None else 0.75 * beak
    bu, bv = hu + 0.14, hv - 0.02
    beakc = col(0.28, 0.28, 0.31)
    c.poly(r.pts(smooth([(bu - 0.02, bv + 0.03), (bu + 0.13, bv - 0.008), (bu - 0.02, bv - 0.01)], 3)), fill=beakc,
           line=INK, lw=lw)
    c.poly(r.pts(smooth([(bu - 0.02, bv - 0.012), (bu + 0.11, bv - 0.02 - 0.08 * op), (bu - 0.02, bv - 0.035)], 3)),
           fill=beakc, line=INK, lw=lw)
    c.poly(r.E(bu, bv + 0.03, 0.032, 0.02), fill=col(0.95, 0.94, 0.9), line=INK, lw=lw * 0.5)
    front = limb(r, (0.12, 0.74), arms[0], 0.46, 0.085, 0.08, PIGEON, JUMPER if jumper else None, 0.62, bars=True)
    return r, front


BIRDS = {
    'owl': dict(body=col(0.58, 0.44, 0.30), belly=col(0.84, 0.74, 0.58), head=col(0.58, 0.44, 0.30), beak=col(0.9, 0.75, 0.3),
                bk='hook', eyes='owl'),
    'puffin': dict(body=BLACK, belly=WHITE, head=BLACK, face=WHITE, beak=ORANGE, bk='puffin'),
    'flamingo': dict(body=col(0.97, 0.62, 0.68), belly=col(0.99, 0.75, 0.8), head=col(0.97, 0.62, 0.68),
                     beak=col(0.2, 0.2, 0.2), bk='bent', neck=True),
    'duck': dict(body=col(0.96, 0.94, 0.88), belly=col(0.99, 0.98, 0.95), head=col(0.96, 0.94, 0.88), beak=ORANGE,
                 bk='bill'),
    'parrot': dict(body=col(0.3, 0.7, 0.35), belly=col(0.95, 0.85, 0.3), head=col(0.85, 0.2, 0.2), beak=col(0.95, 0.9, 0.8),
                   bk='hook'),
    'toucan': dict(body=BLACK, belly=col(0.98, 0.95, 0.7), head=BLACK, beak=col(0.99, 0.66, 0.15), bk='toucan'),
    'robin': dict(body=col(0.55, 0.42, 0.3), belly=col(0.93, 0.45, 0.25), head=col(0.55, 0.42, 0.3), beak=col(0.3, 0.25, 0.2),
                  bk='small'),
    'host': dict(body=col(0.74, 0.54, 0.38), belly=col(0.86, 0.70, 0.54), head=col(0.76, 0.56, 0.40),
                 wing=col(0.64, 0.46, 0.32), beak=col(0.3, 0.26, 0.24), bk='small'),
    'heron': dict(body=col(0.7, 0.72, 0.76), belly=col(0.9, 0.9, 0.92), head=col(0.85, 0.86, 0.9), beak=col(0.9, 0.75, 0.2),
                  bk='long', neck=True),
}


def bird(c, x, y, s, kind, react='idle', t=0.0, face=1, seed=0, dress=None, top=None, bob_k=1.0):
    """A member of the crowd, sitting. react: idle, laugh, gasp, cover, cheer, sleep.
    dress(r, hv) draws clothes over the body; top(r, hv, react) draws hair, glasses and props over the head."""
    k = BIRDS[kind]
    bob = 0.0
    if react == 'laugh':
        bob = 0.04 * abs(math.sin(t * 14 + seed))
    elif react == 'cheer':
        bob = 0.06 * abs(math.sin(t * 10 + seed))
    else:
        bob = 0.01 * math.sin(t * 2 + seed)
    r = Rig(c, x, y - bob * bob_k * s, s, face)
    lw = r.lw()
    hv = 0.85 if k.get('neck') else 0.72
    c.poly(r.E(0, 0.35, 0.3, 0.35), fill=k['body'], line=INK, lw=lw)
    c.poly(r.E(0.08, 0.3, 0.18, 0.25), fill=k['belly'], line=INK, lw=lw * 0.5)
    if dress:
        dress(c, r, hv)
    if k.get('neck'):
        c.line(r.pts([(0.05, 0.55), (0.12, 0.7), (0.06, hv)]), k['body'], lw=s * 0.08)
    c.poly(r.E(0.06, hv, 0.17, 0.16), fill=k['head'], line=INK, lw=lw)
    if 'face' in k:
        c.poly(r.E(0.1, hv, 0.1, 0.1), fill=k['face'], line=INK, lw=lw * 0.5)
    eu, ev = 0.11, hv + 0.03
    if k.get('eyes') == 'owl':
        for du in (-0.06, 0.07):
            c.poly(r.E(eu + du, ev, 0.06, 0.06), fill=WHITE, line=INK, lw=lw * 0.6)
            if react not in ('laugh', 'sleep'):
                c.poly(r.E(eu + du, ev, 0.025 if react != 'gasp' else 0.015, 0.025 if react != 'gasp' else 0.015, 0, 8),
                       fill=INK)
        c.poly(r.pts([(-0.06, hv + 0.14), (-0.02, hv + 0.24), (0.02, hv + 0.14)]), fill=k['head'], line=INK, lw=lw)
        c.poly(r.pts([(0.12, hv + 0.14), (0.18, hv + 0.24), (0.2, hv + 0.12)]), fill=k['head'], line=INK, lw=lw)
    if react in ('laugh', 'sleep'):
        c.line(r.pts([(eu - 0.03, ev), (eu, ev + 0.025), (eu + 0.03, ev)]), INK, lw=lw * 1.2)
    elif k.get('eyes') != 'owl':
        rr = 0.035 if react == 'gasp' else 0.025
        c.poly(r.E(eu, ev, rr, rr, 0, 10), fill=WHITE, line=INK, lw=lw * 0.5)
        c.poly(r.E(eu + 0.005, ev, rr * 0.5, rr * 0.5, 0, 8), fill=INK)
    op = 1.0 if react in ('gasp', 'laugh', 'cheer') else 0.0
    bu, bv = 0.2, hv - 0.02
    bk = k['bk']
    if bk == 'puffin':
        c.poly(r.pts([(bu - 0.03, bv + 0.07), (bu + 0.14, bv), (bu - 0.03, bv - 0.07 - 0.04 * op)]), fill=ORANGE, line=INK,
               lw=lw)
        c.line(r.pts([(bu + 0.03, bv + 0.05), (bu + 0.03, bv - 0.05)]), RED, lw=lw)
    elif bk == 'toucan':
        c.poly(r.pts([(bu - 0.03, bv + 0.06), (bu + 0.32, bv - 0.02), (bu + 0.28, bv - 0.07 - 0.05 * op),
                      (bu - 0.03, bv - 0.05)]), fill=k['beak'], line=INK, lw=lw)
        c.poly(r.pts([(bu + 0.25, bv), (bu + 0.32, bv - 0.02), (bu + 0.28, bv - 0.06)]), fill=BLACK)
    elif bk == 'bill':
        c.poly(r.pts([(bu - 0.03, bv + 0.03), (bu + 0.14, bv + 0.01), (bu + 0.14, bv - 0.03 - 0.05 * op),
                      (bu - 0.03, bv - 0.04)]), fill=ORANGE, line=INK, lw=lw)
    elif bk == 'long':
        c.poly(r.pts([(bu - 0.03, bv + 0.02), (bu + 0.3, bv - 0.02), (bu - 0.03, bv - 0.03 - 0.05 * op)]),
               fill=k['beak'], line=INK, lw=lw)
    elif bk == 'bent':
        c.poly(r.pts([(bu - 0.03, bv + 0.03), (bu + 0.1, bv + 0.01), (bu + 0.12, bv - 0.08), (bu + 0.06, bv - 0.04),
                      (bu - 0.03, bv - 0.03)]), fill=k['beak'], line=INK, lw=lw)
    else:
        c.poly(r.pts([(bu - 0.03, bv + 0.04), (bu + 0.08, bv - 0.01), (bu - 0.03, bv - 0.04 - 0.04 * op)]),
               fill=k['beak'], line=INK, lw=lw)
    if top:
        top(c, r, hv, react)
    # wings: at rest, over the eyes, up in a cheer, or to the cheeks in a gasp
    wing_col = k.get('wing', k['body'])
    if react == 'cover':
        c.poly(r.E(0.12, ev, 0.12, 0.06, -10), fill=wing_col, line=INK, lw=lw)
    elif react == 'cheer':
        for du in (-0.2, 0.2):
            c.poly(r.E(du, 0.75, 0.06, 0.2, 20 * (1 if du > 0 else -1)), fill=wing_col, line=INK, lw=lw)
    elif react == 'gasp':
        c.poly(r.E(0.2, hv - 0.1, 0.05, 0.12, -20), fill=wing_col, line=INK, lw=lw)
    else:
        c.poly(r.E(-0.05, 0.4, 0.12, 0.22, 10), fill=wing_col, line=INK, lw=lw)
    return r


# ---------------------------------------------------------------------------
# The common room (the stage)
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# The audience: each bird is dressed as one of the real people in the room
# ---------------------------------------------------------------------------
def _glasses(c, r, u, v, rr=0.055, two=False):
    for du in ((-0.065, 0.065) if two else (0.0,)):
        c.poly(r.E(u + du, v, rr, rr * 0.85, 0, 14), None, col(0.75, 0.75, 0.78), lw=r.lw(1.9))
        c.poly(r.E(u + du, v, rr, rr * 0.85, 0, 14), None, INK, lw=r.lw(0.7))
    if two:
        c.line(r.pts([(u - 0.01, v), (u + 0.01, v)]), INK, lw=r.lw())
    c.line(r.pts([(u - rr - (0.065 if two else 0), v + 0.01), (u - 0.16, v + 0.03)]), INK, lw=r.lw(0.8))


def _long_hair(c, r, hv, colr, fringe=False, wavy=False):
    w = 0.02 if wavy else 0.0
    hair = smooth([(0.16, hv + 0.13), (0.02, hv + 0.2), (-0.14, hv + 0.14), (-0.2, hv - 0.05), (-0.22 - w, hv - 0.25),
                   (-0.16, hv - 0.38), (-0.08 + w, hv - 0.3), (-0.06, hv - 0.1), (-0.02, hv + 0.06), (0.1, hv + 0.1)], 6)
    c.poly(r.pts(hair), fill=colr, line=INK, lw=r.lw(0.8))
    if wavy:
        for k in range(3):
            c.line(r.pts(smooth([(-0.17 + 0.04 * k, hv - 0.05), (-0.2 + 0.04 * k, hv - 0.15), (-0.16 + 0.04 * k,
                                                                                           hv - 0.27)], 3, False)),
                   INK, lw=r.lw(0.5))
    if fringe:  # a shaggy fringe right down to the eyebrows
        c.poly(r.pts([(0.0, hv + 0.17), (0.2, hv + 0.12), (0.2, hv + 0.06), (0.16, hv + 0.09), (0.12, hv + 0.05),
                      (0.08, hv + 0.09), (0.03, hv + 0.06)]), fill=colr, line=INK, lw=r.lw(0.7))


def _swept_hair(c, r, hv, colr):
    """Thick black hair, swept over to one side."""
    hair = smooth([(-0.17, hv - 0.02), (-0.2, hv + 0.1), (-0.08, hv + 0.2), (0.08, hv + 0.22), (0.2, hv + 0.17),
                   (0.24, hv + 0.1), (0.16, hv + 0.11), (0.06, hv + 0.13), (-0.06, hv + 0.1), (-0.1, hv + 0.02)], 6)
    c.poly(r.pts(hair), fill=colr, line=INK, lw=r.lw(0.8))
    for k in range(3):
        c.line(r.pts(smooth([(-0.1 + 0.07 * k, hv + 0.12), (0.02 + 0.07 * k, hv + 0.18), (0.12 + 0.06 * k, hv + 0.15)],
                            3, False)), col(0.3, 0.28, 0.3), lw=r.lw(0.5))


def _curls(c, r, hv, colr):
    for k in range(8):
        a = math.pi * (0.42 + 0.68 * k / 7)
        c.poly(r.E(0.02 + 0.16 * math.cos(a), hv + 0.04 + 0.15 * math.sin(a), 0.055, 0.055), fill=colr, line=INK,
               lw=r.lw(0.6))
    for k in range(3):
        c.poly(r.E(-0.14, hv - 0.08 - 0.08 * k, 0.06, 0.05), fill=colr, line=INK, lw=r.lw(0.6))


def _top(c, r, colr, pattern=None, open_front=False):
    body = [(u, v) for u, v in r_ell(0, 0.35, 0.31, 0.36) if v < 0.6]
    if open_front:  # a cardigan or blazer, open over the chest
        left = [(u, v) for u, v in body if u < 0.02] + [(0.02, 0.05)]
        c.poly(r.pts(left), fill=colr, line=INK, lw=r.lw())
        c.poly(r.pts([(0.02, 0.6), (0.2, 0.52), (0.26, 0.3), (0.18, 0.1), (0.1, 0.08), (0.12, 0.35)]), fill=colr,
               line=INK, lw=r.lw())
        return
    c.poly(r.pts(body), fill=colr, line=INK, lw=r.lw())
    if pattern == 'zigzag':
        for v in (0.18, 0.32, 0.46):
            c.line(r.pts([(-0.26 + 0.07 * k, v + (0.05 if k % 2 else 0)) for k in range(9)]), BLACK, lw=r.lw(1.6))


def r_ell(cu, cv, ru, rv, n=30):
    return [(cu + ru * math.cos(q), cv + rv * math.sin(q)) for q in np.linspace(0, 2 * math.pi, n, endpoint=False)]


def _scarf(c, r, hv, colr, stripe, tassels=True):
    c.poly(r.pts(smooth([(-0.18, hv - 0.12), (0.2, hv - 0.14), (0.24, hv - 0.24), (-0.16, hv - 0.24)], 4)), fill=colr,
           line=INK, lw=r.lw())
    end = [(0.12, hv - 0.2), (0.22, hv - 0.2), (0.24, hv - 0.5), (0.13, hv - 0.5)]
    c.poly(r.pts(end), fill=colr, line=INK, lw=r.lw())
    c.hatch(r.pts(end), stripe, spacing=r.s * 0.05, angle=0, lw=r.lw(0.6), opacity=0.8)
    if tassels:
        for k in range(4):
            c.line(r.pts([(0.135 + 0.03 * k, hv - 0.5), (0.135 + 0.03 * k, hv - 0.58)]), colr, lw=r.lw(1.2))


AUDIENCE = {
    # the MC: warm light-brown feathers, glasses, swept black hair, white shirt, grey waistcoat, never still
    'host': dict(kind='host',
                 dress=lambda c, r, hv: (c.poly(r.E(0.06, 0.32, 0.22, 0.27), fill=WHITE, line=INK, lw=r.lw(0.6)),
                                         c.poly(r.pts([(-0.24, 0.1), (-0.28, 0.5), (-0.1, 0.62), (0.04, 0.32),
                                                       (0.16, 0.62), (0.3, 0.45), (0.24, 0.1)]), fill=GREY, line=INK,
                                                lw=r.lw()),
                                         [c.poly(r.E(0.05, v, 0.014, 0.014), fill=INK) for v in (0.22, 0.32, 0.42)]),
                 top=lambda c, r, hv, react: (_swept_hair(c, r, hv, col(0.08, 0.07, 0.07)),
                                              _glasses(c, r, 0.12, hv + 0.03, 0.065))),
    # the bearded man in glasses and a dark jumper
    'beard': dict(kind='owl',
                  dress=lambda c, r, hv: _top(c, r, col(0.18, 0.19, 0.24)),
                  top=lambda c, r, hv, react: (
                      c.poly(r.pts(smooth([(-0.08, hv - 0.02), (0.2, hv - 0.06), (0.2, hv - 0.18), (0.06, hv - 0.24),
                                           (-0.08, hv - 0.14)], 4)), fill=col(0.42, 0.28, 0.16), line=INK, lw=r.lw(0.7)),
                      c.poly(r.pts(smooth([(-0.12, hv + 0.12), (0.04, hv + 0.2), (0.2, hv + 0.14), (0.1, hv + 0.1),
                                           (-0.04, hv + 0.08)], 4)), fill=col(0.42, 0.28, 0.16), line=INK, lw=r.lw(0.7)),
                      _glasses(c, r, 0.11, hv + 0.03, 0.058, two=True))),
    # the blonde woman in the black-and-white dress, drink in hand
    'blonde_dress': dict(kind='flamingo',
                         dress=lambda c, r, hv: (_top(c, r, BLACK),
                                                 c.poly(r.pts([(0.0, 0.58), (0.14, 0.55), (0.12, 0.1), (0.02, 0.1)]),
                                                        fill=WHITE, line=INK, lw=r.lw(0.6))),
                         top=lambda c, r, hv, react: (
                             _long_hair(c, r, hv, col(0.93, 0.8, 0.5)),
                             c.poly(r.pts([(0.26, 0.45), (0.36, 0.45), (0.31, 0.33)]), fill=col(0.9, 0.95, 1.0),
                                    line=INK, lw=r.lw(0.6)),
                             c.line(r.pts([(0.31, 0.33), (0.31, 0.24)]), INK, lw=r.lw(0.6)))),
    # the woman with long wavy auburn hair and the big grey-and-white tasselled scarf
    'auburn_scarf': dict(kind='robin',
                         dress=lambda c, r, hv: _top(c, r, col(0.2, 0.2, 0.22)),
                         top=lambda c, r, hv, react: (_long_hair(c, r, hv, col(0.7, 0.33, 0.15), wavy=True),
                                                      _scarf(c, r, hv, col(0.88, 0.88, 0.86), GREY))),
    # the woman with dark curly hair, glasses, red cardigan and patterned scarf
    'curly_red': dict(kind='parrot',
                      dress=lambda c, r, hv: _top(c, r, col(0.75, 0.12, 0.2), open_front=True),
                      top=lambda c, r, hv, react: (_curls(c, r, hv, col(0.15, 0.1, 0.08)),
                                                   _glasses(c, r, 0.11, hv + 0.03),
                                                   _scarf(c, r, hv, col(0.7, 0.2, 0.25), col(0.85, 0.85, 0.85), False))),
    # the woman with the shaggy fringe in the zigzag top, filming it all on her phone
    'fringe_phone': dict(kind='duck',
                         dress=lambda c, r, hv: _top(c, r, WHITE, pattern='zigzag'),
                         top=lambda c, r, hv, react: (
                             _long_hair(c, r, hv, col(0.62, 0.45, 0.28), fringe=True),
                             c.poly(r.pts([(0.26, hv - 0.1), (0.38, hv - 0.1), (0.38, hv + 0.1), (0.26, hv + 0.1)]),
                                    fill=BLACK, line=INK, lw=r.lw(0.7)),
                             c.poly(r.E(0.24, hv - 0.18, 0.06, 0.12, -30), fill=col(0.96, 0.94, 0.88), line=INK,
                                    lw=r.lw()))),
    # the blonde woman in the green top
    'blonde_green': dict(kind='puffin',
                         dress=lambda c, r, hv: _top(c, r, col(0.15, 0.5, 0.38)),
                         top=lambda c, r, hv, react: _long_hair(c, r, hv, col(0.95, 0.85, 0.55))),
    # the man in the grey blazer, clapping along
    'blazer': dict(kind='heron',
                   dress=lambda c, r, hv: (_top(c, r, col(0.32, 0.33, 0.37), open_front=True),
                                           c.poly(r.pts([(0.02, 0.58), (0.1, 0.4), (0.14, 0.58)]), fill=col(0.3, 0.3, 0.32),
                                                  line=INK, lw=r.lw(0.6)))),
}
CROWD = [(70, 'blazer'), (175, 'blonde_dress'), (275, 'fringe_phone'), (475, 'host'), (930, 'curly_red'),
         (1030, 'beard'), (1130, 'auburn_scarf'), (1225, 'blonde_green')]
HOST_MOODS = ['cheer', 'laugh', 'cheer', 'gasp', 'laugh', 'cheer', 'cover', 'laugh']


def host_react(t):
    """The MC is never still: cheering, cackling, gasping, hiding his face, all in quick succession."""
    return HOST_MOODS[int(t * 1.3) % len(HOST_MOODS)]


def audience(c, x, y, s, who, react, t, face=1, seed=0):
    a = AUDIENCE[who]
    if who == 'host':
        react = host_react(t) if react in (None, 'idle') else react
    return bird(c, x, y, s, a['kind'], react, t, face, seed, dress=a.get('dress'), top=a.get('top'),
                bob_k=2.2 if who == 'host' else 1.0)


def crowd(c, t, react_all=None, seed=0, skip_host=False):
    """The audience along the back bench. They laugh on big moments unless told otherwise."""
    lv = max(loud(t - 0.1), loud(t - 0.2))
    for i, (x, who) in enumerate(CROWD):
        if skip_host and who == 'host':
            continue
        if react_all is not None:
            react = react_all[i % len(react_all)] if isinstance(react_all, list) else react_all
        else:
            react = 'laugh' if (lv > 0.85 and (i + int(t * 2)) % 3 != 0) else 'idle'
        audience(c, x, 565, 160 if who == 'host' else 145, who, None if who == 'host' else react, t,
                 face=1 if x < 640 else -1, seed=i + seed)


def room(c, t, clock_speed=0.02):
    c.wash(WALL, 0.85, textured=True)
    # window with tartan curtains
    c.poly([(40, 90), (250, 90), (250, 400), (40, 400)], fill=NAVY, line=INK, lw=5)
    for x in (110, 180):
        c.line([(x, 90), (x, 400)], WHITE, lw=5)
    c.line([(40, 245), (250, 245)], WHITE, lw=5)
    for x0 in (10, 230):
        cur = [(x0, 70), (x0 + 60, 70), (x0 + 55, 440), (x0 + 5, 440)]
        c.poly(cur, fill=col(0.72, 0.28, 0.2), line=INK, lw=4)
        c.hatch(cur, col(0.3, 0.45, 0.25), spacing=14, angle=0, lw=3, opacity=0.8)
        c.hatch(cur, YELLOW, spacing=22, angle=90, lw=2, opacity=0.8)
    # the glowing wooden alcove shelves
    c.poly([(520, 70), (730, 70), (730, 470), (520, 470)], fill=WOOD, line=INK, lw=5)
    c.poly([(540, 90), (710, 90), (710, 450), (540, 450)], fill=AMBER, line=INK, lw=4)
    c.glow(625, 270, 260, AMBER, 0.35)
    for y in (180, 300, 400):
        c.poly([(540, y), (710, y), (710, y + 10), (540, y + 10)], fill=WOOD, line=INK, lw=3)
    c.poly([(600, 110), (640, 110), (640, 170), (600, 170)], fill=WHITE, line=INK, lw=2)
    c.poly([(660, 350), (672, 350), (672, 390), (660, 390)], fill=WHITE, line=INK, lw=2)
    # framed photos
    for (x, y, w, h) in ((770, 110, 85, 105), (780, 260, 75, 95), (380, 150, 90, 70)):
        c.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill=INK, line=INK, lw=3)
        c.poly([(x + 10, y + 10), (x + w - 10, y + 10), (x + w - 10, y + h - 10), (x + 10, y + h - 10)],
               fill=col(0.8, 0.8, 0.78))
        c.poly([(x + 16, y + h - 14), (x + w / 2, y + 22), (x + w - 16, y + h - 14)], fill=col(0.55, 0.55, 0.55))
    # the wall clock, always there (its hands race when someone is made to wait)
    c.poly(E(975, 130, 42, 42), fill=WHITE, line=INK, lw=5)
    for i in range(12):
        q = i / 12 * 2 * math.pi
        c.line([(975 + 34 * math.sin(q), 130 - 34 * math.cos(q)), (975 + 39 * math.sin(q), 130 - 39 * math.cos(q))], INK, lw=2)
    a = t * clock_speed
    c.line([(975, 130), (975 + 30 * math.sin(a), 130 - 30 * math.cos(a))], INK, lw=4)
    c.line([(975, 130), (975 + 18 * math.sin(a / 12), 130 - 18 * math.cos(a / 12))], INK, lw=6)
    # the door and its notices
    c.poly([(1090, 60), (1250, 60), (1250, 520), (1090, 520)], fill=WOOD_D, line=INK, lw=5)
    c.poly([(1110, 150), (1160, 150), (1160, 215), (1110, 215)], fill=col(0.3, 0.45, 0.8), line=INK, lw=2)
    c.poly([(1170, 160), (1225, 160), (1225, 230), (1170, 230)], fill=WHITE, line=INK, lw=2)
    # benches and the low table with cups
    c.poly([(0, 470), (1280, 470), (1280, 560), (0, 560)], fill=BENCH, line=INK, lw=4)
    c.hatch([(0, 470), (1280, 470), (1280, 560), (0, 560)], col(0.6, 0.18, 0.28), spacing=28, angle=90, lw=2,
            opacity=0.6)
    c.poly([(0, 560), (1280, 560), (1280, 720), (0, 720)], fill=CARPET, line=INK, lw=4)


def penguin_x(t):
    """He keeps advancing on his opponent as the verse goes on."""
    return lerp(930, 640, sstep(0, 227, t))


GESTURES = {
    'point': (95, 20), 'jab': (80, 60), 'wide': (120, 160), 'up': (170, 30), 'chest': (40, 10), 'shrug': (70, 150),
    'down': (15, 10), 'both': (100, 110), 'finger': (140, 20),
}
MOODS = {  # per shot, a few gestures the penguin cycles through as he delivers
    'stage': ['point', 'wide', 'jab', 'chest', 'up', 'shrug'],
    'gasp': ['point', 'jab', 'wide', 'finger'],
    'examine': ['down'],
}


def penguin_pose(t, pool):
    """A new gesture on each stressed beat, held until the next: choppy, like the real thing."""
    beat = int(t * 2.2)
    rng = np.random.default_rng(beat * 31 + 7)
    g = pool[int(rng.integers(0, len(pool)))]
    a = GESTURES[g]
    lean = 6 + 10 * loud(t) + (8 if g in ('jab', 'point') else 0)
    return a, lean


REACTS = [  # (mood, arms): how the listener takes it, changing every second or so
    ('neutral', (15, 15)), ('grin', (40, 35)), ('laugh', (20, 60)), ('grin', (60, 15)), ('neutral', (35, 35)),
    ('shock', (15, 15)), ('laugh', (95, 20)), ('neutral', (20, 20)), ('grin', (60, 60)), ('neutral', (15, 45)),
]


def listener_react(t, seed=0):
    """Pick the listener's current reaction: a new one roughly every 1.2 seconds, with little laughs."""
    beat = int(t / 2.2)
    rng = np.random.default_rng(beat * 97 + 11 + seed)
    mood, arms = REACTS[int(rng.integers(0, len(REACTS)))]
    if loud(t) > 0.85 and beat % 2:
        mood = 'laugh'
    laughing = mood == 'laugh'
    lean = (-8 + 6 * abs(math.sin(t * 13))) if laughing else 3 * math.sin(t * 1.3 + seed)
    return mood, arms, lean, laughing


def pigeon_listens(c, t, x=300):
    mood, arms, lean, laughing = listener_react(t)
    return pigeon(c, x, 690 - (8 * abs(math.sin(t * 13)) if laughing else 0), 330, 1, arms=arms, lean=lean, mood=mood,
                  t=t, head_tilt=0.3 * math.sin(t * 0.7))


SMILED = (70.3, 72.9)  # grins from 70.3, the line itself starts at 70.9  # 'oh look, I think it smiled': he points at him


def stage(c, t, name):
    room(c, t)
    px = penguin_x(t)
    if name == 'examine':
        crowd(c, t, 'idle')
        pigeon(c, 300, 690, 330, 1, mood='neutral', t=t)
        u = clamp01(t / 8.2)
        r, front, back = penguin(c, px, 690, 300, -1, arms=(95, 20), lean=14, beak=beak_open(t), eye='wide')
        # the magnifying glass, held out towards the pigeon
        fx, fy = r.P(*front)
        c.line([(fx, fy), (fx - 40, fy - 25)], WOOD_D, lw=10)
        c.poly(E(fx - 60, fy - 40, 34, 34), fill=col(0.85, 0.93, 1.0), line=INK, lw=6, opacity=0.9)
        if 4.0 < t < 7.5:
            text(c, '?', 380, 280 - 10 * math.sin(t * 6), 80, INK)
        return
    if name == 'collapse':
        crowd(c, t, 'cheer')
        u = t - 175.9
        # the pigeon turns away, doubled over laughing, face in his wing
        pigeon(c, 300, 690, 330, -1 if u < 6 else 1, arms=(150, 60), lean=-20 if u < 6 else 25, mood='laugh', t=t)
        penguin(c, px, 690, 300, -1, arms=GESTURES['wide'], lean=-6, beak=0.3, eye='smug')
        return
    if name == 'finale':
        u = t - 227.9
        crowd(c, t, 'cheer')
        if u < 1.5:
            pigeon(c, 300, 690, 330, 1, mood='shock', t=t)
            r, front, back = penguin(c, px, 690, 300, -1, arms=(100, 20), lean=10, beak=0.0, eye='smug')
            # a flipper drop
            fx, fy = r.P(*front)
            c.poly(E(fx, fy + 30 + 200 * u * u, 10, 22), fill=INK, line=INK, lw=2)
        else:
            # the hug
            k = min(1.0, (u - 1.5) / 1.0)
            pigeon(c, lerp(300, 470, k), 690, 330, 1, arms=(110, 110), mood='laugh', t=t)
            penguin(c, lerp(px, 600, k), 690, 300, -1, arms=(115, 115), lean=10, beak=0.0, eye='closed')
            if u > 4:
                text(c, 'RESPECT.', 640, 120, 60, INK, opacity=clamp01((u - 4) / 1.0))
        return
    # ordinary delivery, or a gasp line where the crowd are scandalised
    if name == 'gasp':
        crowd(c, t, ['gasp', 'cover', 'gasp', 'laugh', 'cover', 'gasp', 'laugh', 'cover'])
        pigeon(c, 300, 690, 330, 1, mood='shock', t=t)
    elif name == 'hit':
        crowd(c, t, ['gasp', 'laugh', 'cheer', 'gasp', 'laugh', 'cover', 'cheer', 'gasp'])
        pigeon(c, 300, 690, 330, 1, lean=-14, mood='hurt', t=t, arms=(40, 30))
    elif 8.2 <= t < 10.9:  # the apology: he just raises an eyebrow
        crowd(c, t)
        pigeon(c, 300, 690, 330, 1, arms=(15, 15), mood='neutral' if t < 8.9 else 'brow', t=t)
    elif 66.6 <= t < SMILED[0]:  # stung... blank... a twitch at the corner of the beak...
        crowd(c, t)
        mood = 'hurt' if t < 67.8 else ('neutral' if t < 68.9 else 'smirk')
        pigeon(c, 300, 690, 330, 1, arms=(15, 15), mood=mood, t=t)
    elif SMILED[0] <= t < SMILED[1]:
        crowd(c, t)
        pigeon(c, 300, 690, 330, 1, arms=(15, 15), mood='grin', t=t)  # ...and it did smile
    else:
        crowd(c, t)
        pigeon_listens(c, t)
    arms, lean = penguin_pose(t, MOODS.get(name, MOODS['stage']))
    if 70.9 <= t < SMILED[1]:  # pointing at him as he says it
        arms, lean = GESTURES['point'], 16
    penguin(c, px, 690, 300, -1, arms=arms, lean=lean, beak=beak_open(t), eye='angry' if loud(t) > 0.7 else 'smug')


def stage_cam(c, t, name, a, b):
    """Vary the framing: wide, then push in on the penguin or the pigeon for the punchline."""
    k = int(a * 10) % 3
    u = (t - a) / max(0.1, b - a)
    if name in ('examine', 'finale', 'gasp', 'collapse'):
        return
    if name == 'hit':
        c.cam = (1.8, -300 * 1.8 + 640, -420 * 1.8 + 360)
        return
    if k == 1 and u > 0.35:
        px = penguin_x(t)
        c.cam = (1.6, -px * 1.6 + 640, -470 * 1.6 + 360)
    elif k == 2 and u > 0.5:
        c.cam = (1.45, -520 * 1.45 + 640, -470 * 1.45 + 360)


# ---------------------------------------------------------------------------
# The literal cutaways
# ---------------------------------------------------------------------------
def wash(c, colr, amount=0.8):
    c.wash(colr, amount, textured=True)


def talk(t):
    return beak_open(t)


def owl_brows(c, r, cross=True):
    """Stern eyebrows over an owl's big eyes (r = the rig bird() returns)."""
    hv = 0.72
    for du, sg in ((-0.06, 1), (0.07, -1)):
        c.line(r.pts([(0.11 + du - 0.06, hv + 0.12 + 0.03 * sg), (0.11 + du + 0.06, hv + 0.12 - 0.03 * sg)]), INK,
               lw=r.lw(2.2))


def captain(c, x, y, s, t):
    """An old sea dog of a captain: peaked cap, huge black beard, navy jumper with an anchor, and a pipe."""
    skin = col(0.96, 0.8, 0.68)
    navy = col(0.13, 0.17, 0.32)
    c.poly([(x - 0.42 * s, y), (x - 0.4 * s, y - 0.55 * s), (x + 0.4 * s, y - 0.55 * s), (x + 0.42 * s, y)], fill=navy,
           line=INK, lw=5)
    c.poly([(x - 0.07 * s, y - 0.4 * s), (x + 0.07 * s, y - 0.4 * s), (x, y - 0.25 * s)], fill=None, line=WHITE, lw=4)
    c.line([(x, y - 0.45 * s), (x, y - 0.2 * s)], WHITE, lw=4)
    c.line(smooth([(x - 0.08 * s, y - 0.26 * s), (x, y - 0.2 * s), (x + 0.08 * s, y - 0.26 * s)], 4, False), WHITE, lw=4)
    hy = y - 0.78 * s
    c.poly(E(x, hy, 0.25 * s, 0.28 * s), fill=skin, line=INK, lw=5)
    beard = smooth([(x - 0.26 * s, hy - 0.02 * s), (x - 0.24 * s, hy + 0.22 * s), (x, hy + 0.4 * s),
                    (x + 0.24 * s, hy + 0.22 * s), (x + 0.26 * s, hy - 0.02 * s), (x + 0.12 * s, hy + 0.08 * s),
                    (x - 0.12 * s, hy + 0.08 * s)], 5)
    c.poly(beard, fill=col(0.1, 0.1, 0.12), line=INK, lw=4)
    c.poly(E(x + 0.04 * s, hy + 0.02 * s, 0.07 * s, 0.06 * s), fill=col(0.95, 0.6, 0.55), line=INK, lw=3)  # nose
    for sg in (-1, 1):
        c.poly(E(x + sg * 0.1 * s, hy - 0.07 * s, 0.025 * s, 0.025 * s), fill=INK)
        c.line([(x + sg * 0.16 * s, hy - 0.16 * s), (x + sg * 0.04 * s, hy - 0.12 * s)], INK, lw=6)  # bushy brows
    c.poly([(x - 0.27 * s, hy - 0.2 * s), (x + 0.27 * s, hy - 0.2 * s), (x + 0.3 * s, hy - 0.34 * s),
            (x - 0.3 * s, hy - 0.34 * s)], fill=navy, line=INK, lw=4)  # cap
    c.poly(smooth([(x - 0.3 * s, hy - 0.34 * s), (x - 0.26 * s, hy - 0.45 * s), (x + 0.26 * s, hy - 0.45 * s),
                   (x + 0.3 * s, hy - 0.34 * s)], 4), fill=WHITE, line=INK, lw=4)
    c.poly([(x - 0.3 * s, hy - 0.2 * s), (x + 0.1 * s, hy - 0.2 * s), (x + 0.05 * s, hy - 0.13 * s),
            (x - 0.28 * s, hy - 0.15 * s)], fill=BLACK, line=INK, lw=3)  # peak
    c.poly(E(x, hy - 0.27 * s, 0.04 * s, 0.035 * s), fill=YELLOW, line=INK, lw=2)
    # the pipe, puffing
    c.line([(x + 0.15 * s, hy + 0.12 * s), (x + 0.35 * s, hy + 0.16 * s)], WOOD_D, lw=8)
    c.poly([(x + 0.33 * s, hy + 0.2 * s), (x + 0.42 * s, hy + 0.2 * s), (x + 0.41 * s, hy + 0.06 * s),
            (x + 0.34 * s, hy + 0.06 * s)], fill=WOOD_D, line=INK, lw=3)
    for i in range(3):
        ph = (t * 0.8 + i / 3) % 1
        c.poly(E(x + 0.38 * s + 30 * ph, hy - 40 - 120 * ph, 10 + 16 * ph, 8 + 12 * ph), None, GREY, lw=3,
               opacity=1 - ph)


def terrier(c, x, y, s, t, face=1):
    """A small white wire-haired fox terrier, sitting up alertly at the bow."""
    f = face
    c.poly(E(x, y - 0.3 * s, 0.32 * s, 0.3 * s), fill=WHITE, line=INK, lw=4)
    c.line([(x - f * 0.28 * s, y - 0.4 * s), (x - f * 0.42 * s, y - 0.62 * s - 10 * math.sin(t * 12))], WHITE, lw=10)
    c.poly(E(x + f * 0.2 * s, y - 0.72 * s, 0.2 * s, 0.18 * s), fill=WHITE, line=INK, lw=4)
    c.poly([(x + f * 0.3 * s, y - 0.8 * s), (x + f * 0.62 * s, y - 0.7 * s), (x + f * 0.6 * s, y - 0.6 * s),
            (x + f * 0.3 * s, y - 0.6 * s)], fill=WHITE, line=INK, lw=4)  # a long terrier snout
    c.poly(E(x + f * 0.62 * s, y - 0.66 * s, 0.05 * s, 0.04 * s), fill=INK)
    c.poly(E(x + f * 0.26 * s, y - 0.77 * s, 0.025 * s, 0.03 * s), fill=INK)
    for du in (0.05, 0.25):
        c.poly([(x + f * du * s, y - 0.86 * s), (x + f * (du + 0.08) * s, y - 1.02 * s), (x + f * (du + 0.14) * s,
                y - 0.84 * s)], fill=WHITE, line=INK, lw=3)
    for du in (-0.1, 0.12):
        c.line([(x + f * du * s, y - 0.1 * s), (x + f * du * s, y)], WHITE, lw=12)


def cow(c, x, y, s, lid=0.0, face=1, lid_dx=0.0):
    """A black-and-white cow. lid lifts her top half off like a Russian doll."""
    f = face
    body = [(x - 0.6 * s, y - 0.3 * s), (x + 0.6 * s, y - 0.3 * s), (x + 0.62 * s, y - 0.75 * s), (x - 0.62 * s, y - 0.75 * s)]
    for du in (-0.45, -0.25, 0.3, 0.5):
        c.line([(x + du * s, y - 0.32 * s), (x + du * s, y)], WHITE, lw=max(4, 0.1 * s))
        c.line([(x + du * s - 0.05 * s, y), (x + du * s + 0.05 * s, y)], INK, lw=max(3, 0.04 * s))
    c.poly(E(x + 0.05 * s, y - 0.3 * s, 0.12 * s, 0.05 * s), fill=PINK, line=INK, lw=3)  # udder
    lo = [(px, max(py, y - 0.52 * s)) for px, py in smooth(body, 4)]
    c.poly(lo, fill=WHITE, line=INK, lw=5)
    c.poly(E(x - 0.25 * s, y - 0.42 * s, 0.14 * s, 0.08 * s), fill=INK)
    x += lid_dx
    top = [(x - 0.62 * s, y - 0.52 * s - lid), (x + 0.62 * s, y - 0.52 * s - lid), (x + 0.6 * s, y - 0.8 * s - lid),
           (x - 0.6 * s, y - 0.8 * s - lid)]
    c.poly(top, fill=WHITE, line=INK, lw=5)
    c.poly(E(x + 0.15 * s, y - 0.66 * s - lid, 0.18 * s, 0.09 * s), fill=INK)
    hx, hy = x + f * 0.72 * s, y - 0.82 * s - lid
    c.poly(E(hx, hy, 0.2 * s, 0.22 * s), fill=WHITE, line=INK, lw=5)
    c.poly(E(hx + f * 0.06 * s, hy + 0.13 * s, 0.16 * s, 0.1 * s), fill=PINK, line=INK, lw=4)
    for sg in (-1, 1):
        c.poly(E(hx + f * 0.02 * s + sg * 0.08 * s, hy - 0.05 * s, 0.025 * s, 0.03 * s), fill=INK)
        c.poly([(hx + sg * 0.12 * s, hy - 0.18 * s), (hx + sg * 0.2 * s, hy - 0.3 * s), (hx + sg * 0.16 * s, hy - 0.16 * s)],
               fill=col(0.95, 0.92, 0.8), line=INK, lw=3)
    c.line([(x - f * 0.6 * s, y - 0.7 * s - lid), (x - f * 0.75 * s, y - 0.4 * s - lid)], INK, lw=max(3, 0.03 * s))


def s_veal(c, t, u):
    """This isn't beef: it's barely veal. Andy carves into a big cow and finds a smaller one inside."""
    wash(c, col(0.96, 0.93, 0.86))
    c.poly([(0, 640), (1280, 640), (1280, 720), (0, 720)], fill=col(0.75, 0.62, 0.45), line=INK, lw=4)
    k1, k2 = sstep(0.3, 0.5, u), sstep(0.7, 0.85, u)
    cow(c, 600, 630, 440, lid=180 * k1, lid_dx=-560 * k1)
    if u > 0.3:  # the smaller cow inside, standing on the cut, then the tiny one inside that
        cow(c, 600, 405, 200, lid=90 * k2, lid_dx=-260 * k2)
    if u > 0.7:
        cow(c, 600, 302, 90)
    if u < 0.3 or 0.5 < u < 0.7:  # the knife going in
        kx = lerp(250, 900, (u * 5) % 1)
        ky = 630 - 0.52 * 440 if u < 0.3 else 405 - 0.52 * 200
        c.poly([(kx, ky - 10), (kx + 110, ky), (kx, ky + 10)], fill=SILVER, line=INK, lw=3)
        c.line([(kx - 60, ky), (kx, ky)], WOOD_D, lw=16)
    penguin(c, 1100, 700, 300, -1, arms=(100, 20), lean=6, beak=talk(t), eye='angry', hat='surgeon' if False else None)
    text(c, 'BEEF?', 1000, 90, 56, INK)
    if u > 0.45:
        text(c, 'VEAL.', 1080, 160, 56, RED)
    if u > 0.85:
        text(c, 'barely.', 1130, 230, 46, RED, rot=-5)


def craker(c, x, y, s, skin, hair, t, seed=0):
    """One of Crake's serene, beautiful post-humans: sitting in the long grass, eyes closed, purring."""
    c.poly(smooth([(x - 0.36 * s, y), (x - 0.3 * s, y - 0.45 * s), (x + 0.3 * s, y - 0.45 * s), (x + 0.36 * s, y)], 4),
           fill=skin, line=INK, lw=4)
    c.poly(E(x, y - 0.66 * s, 0.2 * s, 0.24 * s), fill=skin, line=INK, lw=4)
    c.poly(smooth([(x - 0.22 * s, y - 0.62 * s), (x - 0.2 * s, y - 0.86 * s), (x, y - 0.94 * s), (x + 0.2 * s, y - 0.86 * s),
                   (x + 0.22 * s, y - 0.62 * s), (x + 0.15 * s, y - 0.8 * s), (x - 0.15 * s, y - 0.8 * s)], 4), fill=hair,
           line=INK, lw=3)
    for sg in (-1, 1):
        c.line(smooth([(x + sg * 0.1 * s - 0.04 * s, y - 0.66 * s), (x + sg * 0.1 * s, y - 0.64 * s),
                       (x + sg * 0.1 * s + 0.04 * s, y - 0.66 * s)], 3, False), INK, lw=3)
    c.line(smooth([(x - 0.06 * s, y - 0.55 * s), (x, y - 0.52 * s), (x + 0.06 * s, y - 0.55 * s)], 3, False), INK, lw=3)
    for k in range(5):  # a garland of leaves
        a = math.pi * (0.15 + 0.7 * k / 4)
        c.poly(E(x + 0.28 * s * math.cos(a), y - 0.45 * s + 0.08 * s * math.sin(a), 0.06 * s, 0.03 * s, math.degrees(a)),
               fill=GREEN, line=INK, lw=2)


def churchgoer(c, x, y, s, t):
    """A rapper in his Sunday best: pressed three-piece church suit, tie, pocket square, polished shoes, gloves on."""
    skin = col(0.42, 0.28, 0.2)
    suit = col(0.16, 0.18, 0.26)
    for sg in (-1, 1):  # legs and shoes
        c.poly([(x + sg * 0.03 * s, y - 0.45 * s), (x + sg * 0.14 * s, y - 0.45 * s), (x + sg * 0.14 * s, y - 0.04 * s),
                (x + sg * 0.03 * s, y - 0.04 * s)], fill=suit, line=INK, lw=4)
        c.poly(smooth([(x + sg * 0.02 * s, y), (x + sg * 0.02 * s, y - 0.05 * s), (x + sg * 0.16 * s, y - 0.05 * s),
                       (x + sg * 0.22 * s, y)], 3), fill=BLACK, line=INK, lw=3)
    c.poly([(x - 0.2 * s, y - 0.42 * s), (x - 0.22 * s, y - 0.9 * s), (x + 0.22 * s, y - 0.9 * s), (x + 0.2 * s, y - 0.42 * s)],
           fill=suit, line=INK, lw=5)  # jacket
    c.poly([(x - 0.08 * s, y - 0.9 * s), (x, y - 0.66 * s), (x + 0.08 * s, y - 0.9 * s)], fill=WHITE, line=INK, lw=3)
    c.poly([(x - 0.02 * s, y - 0.88 * s), (x + 0.02 * s, y - 0.88 * s), (x + 0.025 * s, y - 0.7 * s), (x, y - 0.66 * s),
            (x - 0.025 * s, y - 0.7 * s)], fill=col(0.6, 0.1, 0.15), line=INK, lw=2)  # tie
    c.poly([(x - 0.08 * s, y - 0.7 * s), (x + 0.08 * s, y - 0.7 * s), (x + 0.08 * s, y - 0.5 * s),
            (x - 0.08 * s, y - 0.5 * s)], fill=col(0.25, 0.26, 0.34), line=INK, lw=3)  # waistcoat
    c.poly([(x + 0.1 * s, y - 0.8 * s), (x + 0.17 * s, y - 0.8 * s), (x + 0.16 * s, y - 0.76 * s)], fill=WHITE, line=INK,
           lw=2)  # pocket square
    c.poly(E(x - 0.03 * s, y - 0.72 * s, 0.018 * s, 0.018 * s), fill=YELLOW, line=INK, lw=2)
    for sg, ang in ((-1, 30 + 10 * math.sin(t * 6)), (1, 40 + 10 * math.sin(t * 6 + 1))):  # arms up in a guard
        sx, sy = x + sg * 0.2 * s, y - 0.86 * s
        ex, ey = sx + sg * 0.12 * s, sy + 0.2 * s
        hx, hy = x + sg * 0.1 * s, y - 1.02 * s - 0.02 * s * math.sin(t * 6)
        c.line([(sx, sy), (ex, ey), (hx, hy)], suit, lw=0.09 * s)
        c.poly(E(hx, hy, 0.06 * s, 0.065 * s), fill=RED, line=INK, lw=4)  # boxing gloves
    c.line([(x, y - 0.9 * s), (x, y - 0.95 * s)], skin, lw=0.08 * s)
    hy = y - 1.07 * s
    c.poly(E(x, hy, 0.12 * s, 0.14 * s), fill=skin, line=INK, lw=4)
    c.poly(smooth([(x - 0.12 * s, hy - 0.02 * s), (x - 0.11 * s, hy - 0.12 * s), (x, hy - 0.15 * s), (x + 0.11 * s, hy - 0.12 * s),
                   (x + 0.12 * s, hy - 0.02 * s), (x + 0.08 * s, hy - 0.1 * s), (x - 0.08 * s, hy - 0.1 * s)], 4),
           fill=col(0.08, 0.06, 0.05), line=INK, lw=2)  # close-cropped hair
    # clean-shaven, a serious little frown, and a pair of slatted shutter shades
    c.poly([(x - 0.11 * s, hy - 0.05 * s), (x + 0.11 * s, hy - 0.05 * s), (x + 0.1 * s, hy + 0.01 * s),
            (x - 0.1 * s, hy + 0.01 * s)], fill=WHITE, line=INK, lw=3)
    for k in range(5):
        yy = hy - 0.04 * s + k * 0.011 * s
        c.line([(x - 0.1 * s, yy), (x + 0.1 * s, yy)], INK, lw=2)
    c.line([(x - 0.07 * s, hy - 0.075 * s), (x - 0.02 * s, hy - 0.06 * s)], INK, lw=4)
    c.line([(x + 0.07 * s, hy - 0.075 * s), (x + 0.02 * s, hy - 0.06 * s)], INK, lw=4)
    c.line(smooth([(x - 0.035 * s, hy + 0.085 * s), (x, hy + 0.075 * s), (x + 0.035 * s, hy + 0.085 * s)], 3, False),
           col(0.35, 0.18, 0.15), lw=4)


def sparkle(c, x, y, r, colr=YELLOW):
    c.poly([(x, y - r), (x + r * 0.25, y - r * 0.25), (x + r, y), (x + r * 0.25, y + r * 0.25), (x, y + r),
            (x - r * 0.25, y + r * 0.25), (x - r, y), (x - r * 0.25, y - r * 0.25)], fill=colr, line=INK, lw=2)


def s_snap(c, t, u):
    """The MC can't contain himself: OOOH SNAP!"""
    wash(c, col(0.98, 0.85, 0.35))
    for i in range(16):  # a burst of lines behind him
        a = i * math.pi / 8 + t * 0.5
        c.poly([(640, 360), (640 + 900 * math.cos(a), 360 + 900 * math.sin(a)),
                (640 + 900 * math.cos(a + 0.12), 360 + 900 * math.sin(a + 0.12))], fill=col(1.0, 0.95, 0.6))
    shake = 8 * math.sin(t * 45)
    audience(c, 520 + shake, 1150, 1100, 'host', 'laugh', t, 1)
    text(c, 'OOOH', 960 + shake, 150, 110, RED, rot=-8)
    text(c, 'SNAP!', 1000 - shake, 290, 130, RED, rot=-6)


def standing_heron(c, x, y, s, t, face=1):
    """The nurse: a heron on long stilt legs, in a nurse's cap."""
    for du in (-0.08, 0.08):
        c.line([(x + du * s, y), (x + du * s * 1.2, y - 0.75 * s)], col(0.85, 0.7, 0.2), lw=max(4, 0.035 * s))
        c.line([(x + du * s, y), (x + du * s + face * 0.12 * s, y + 0.01 * s)], col(0.85, 0.7, 0.2), lw=max(3, 0.025 * s))
    r = bird(c, x, y - 0.72 * s, s, 'heron', 'idle', t, face)
    hx, hy = r.P(0.06, 0.85 + 0.19)
    c.poly([(hx - 0.1 * s, hy + 0.02 * s), (hx + 0.1 * s, hy + 0.02 * s), (hx + 0.07 * s, hy - 0.07 * s),
            (hx - 0.07 * s, hy - 0.07 * s)], fill=WHITE, line=INK, lw=3)
    c.line([(hx - 0.02 * s, hy - 0.025 * s), (hx + 0.02 * s, hy - 0.025 * s)], RED, lw=4)
    c.line([(hx, hy - 0.045 * s), (hx, hy - 0.005 * s)], RED, lw=4)
    return r


def hannibal(c, x, y, s, t):
    """The good doctor, seated: slicked-back grey hair, unblinking pale eyes, thin polite smile, white jumpsuit."""
    skin = col(0.93, 0.8, 0.7)
    suit = col(0.94, 0.94, 0.9)
    for sg in (-1, 1):  # seated: thighs forward, shins down to polished shoes
        c.poly([(x + sg * 0.12 * s, y - 0.05 * s), (x + sg * 0.12 * s - 0.35 * s, y - 0.02 * s),
                (x + sg * 0.12 * s - 0.35 * s, y + 0.1 * s), (x + sg * 0.12 * s, y + 0.1 * s)], fill=suit, line=INK, lw=4)
        c.poly([(x + sg * 0.12 * s - 0.35 * s, y + 0.02 * s), (x + sg * 0.12 * s - 0.25 * s, y + 0.02 * s),
                (x + sg * 0.12 * s - 0.26 * s, y + 0.28 * s), (x + sg * 0.12 * s - 0.35 * s, y + 0.28 * s)], fill=suit,
               line=INK, lw=4)
        c.poly(smooth([(x + sg * 0.12 * s - 0.44 * s, y + 0.33 * s), (x + sg * 0.12 * s - 0.44 * s, y + 0.27 * s),
                       (x + sg * 0.12 * s - 0.25 * s, y + 0.27 * s), (x + sg * 0.12 * s - 0.25 * s, y + 0.33 * s)], 3),
               fill=BLACK, line=INK, lw=3)
    c.poly(smooth([(x - 0.3 * s, y), (x - 0.32 * s, y - 0.55 * s), (x - 0.14 * s, y - 0.66 * s), (x + 0.14 * s, y - 0.66 * s),
                   (x + 0.32 * s, y - 0.55 * s), (x + 0.3 * s, y)], 4), fill=suit, line=INK, lw=5)
    c.line([(x, y - 0.64 * s), (x, y - 0.1 * s)], GREY, lw=3)
    c.poly([(x - 0.08 * s, y - 0.66 * s), (x, y - 0.56 * s), (x + 0.08 * s, y - 0.66 * s)], fill=WHITE, line=INK, lw=3)
    c.line([(x, y - 0.66 * s), (x, y - 0.72 * s)], skin, lw=0.1 * s)
    hy = y - 0.88 * s
    c.poly(smooth([(x - 0.16 * s, hy - 0.05 * s), (x - 0.14 * s, hy + 0.12 * s), (x, hy + 0.2 * s), (x + 0.14 * s, hy + 0.12 * s),
                   (x + 0.16 * s, hy - 0.05 * s), (x, hy - 0.2 * s)], 5), fill=skin, line=INK, lw=4)
    c.poly(smooth([(x - 0.17 * s, hy - 0.02 * s), (x - 0.15 * s, hy - 0.16 * s), (x, hy - 0.22 * s), (x + 0.15 * s, hy - 0.16 * s),
                   (x + 0.17 * s, hy - 0.02 * s), (x + 0.12 * s, hy - 0.12 * s), (x - 0.12 * s, hy - 0.12 * s)], 4),
           fill=col(0.62, 0.6, 0.58), line=INK, lw=3)  # slicked back
    for k in range(3):
        c.line([(x - 0.08 * s + 0.08 * s * k, hy - 0.2 * s), (x - 0.1 * s + 0.08 * s * k, hy - 0.12 * s)], col(0.45, 0.43, 0.42), lw=2)
    for sg in (-1, 1):  # unblinking eyes
        ex = x + sg * 0.065 * s
        c.poly(E(ex, hy - 0.02 * s, 0.035 * s, 0.022 * s), fill=WHITE, line=INK, lw=3)
        c.poly(E(ex, hy - 0.02 * s, 0.014 * s, 0.014 * s), fill=col(0.45, 0.6, 0.75))
        c.poly(E(ex, hy - 0.02 * s, 0.006 * s, 0.006 * s), fill=INK)
        c.line([(ex - 0.04 * s, hy - 0.06 * s), (ex + 0.04 * s, hy - 0.055 * s - sg * 0.005 * s)], INK, lw=3)
    c.line([(x, hy), (x - 0.015 * s, hy + 0.06 * s), (x + 0.01 * s, hy + 0.065 * s)], INK, lw=2)
    c.line(smooth([(x - 0.06 * s, hy + 0.1 * s), (x, hy + 0.115 * s), (x + 0.06 * s, hy + 0.1 * s)], 3, False), INK, lw=3)
    return hy


def chair(c, x, y, face):
    c.poly([(x - face * 20, y - 330), (x + face * 10, y - 330), (x + face * 10, y - 120), (x - face * 20, y - 120)], fill=WOOD,
           line=INK, lw=4)
    c.line([(x - 60, y), (x - 60, y - 120)], WOOD_D, lw=10)
    c.line([(x + 60, y), (x + 60, y - 120)], WOOD_D, lw=10)


def s_keepreal(c, t, u):
    """Listening to this dickhead, keeping it real, like: is he alright? Sam on a skateboard, shades on... then not."""
    wash(c, col(0.92, 0.9, 0.86))
    c.poly([(0, 620), (1280, 620), (1280, 720), (0, 720)], fill=col(0.62, 0.62, 0.64), line=INK, lw=4)
    for x in range(0, 1300, 160):
        c.line([(x, 660), (x + 70, 660)], WHITE, lw=5)
    crash = sstep(0.62, 0.7, u)  # 'is he alright?'
    x = lerp(150, 760, sstep(0.0, 0.62, u))
    if crash < 1:
        hop = 90 * max(0.0, math.sin(math.pi * (u - 0.5) / 0.12)) if 0.5 < u < 0.62 else 0
        spin = 360 * sstep(0.5, 0.62, u)
        # the board
        bx, by = x, 612 - hop
        ra = math.radians(spin)
        c.poly([(bx - 110 * math.cos(ra), by - 10 * math.sin(ra) - 8), (bx + 110 * math.cos(ra), by + 10 * math.sin(ra) - 8),
                (bx + 110 * math.cos(ra), by + 10 * math.sin(ra) + 6), (bx - 110 * math.cos(ra), by - 10 * math.sin(ra) + 6)],
               fill=col(0.85, 0.3, 0.2), line=INK, lw=4)
        for wx in (-70, 70):
            c.poly(E(bx + wx * math.cos(ra), by + 16, 12, 12), fill=YELLOW, line=INK, lw=3)
        r, front = pigeon(c, x, 600 - hop * 1.2, 300, 1, arms=(95, 60) if u < 0.5 else (150, 160), lean=-8 + 5 * math.sin(t * 3),
                          mood='smirk', t=t)
    else:  # sprawled on the tarmac, board rolling off on its own
        r, front = pigeon(c, 800, 690, 300, 1, arms=(150, 30), lean=-80, mood='dizzy', t=t)
        bx = lerp(820, 1350, sstep(0.7, 1.0, u))
        c.poly([(bx - 110, 604), (bx + 110, 604), (bx + 110, 618), (bx - 110, 618)], fill=col(0.85, 0.3, 0.2), line=INK, lw=4)
        for i in range(4):
            q = t * 6 + i * 1.57
            text(c, '*', 700 + 90 * math.cos(q), 520 + 25 * math.sin(q), 40, YELLOW)
    # shades (and a backwards cap)
    hx, hy = r.P(0.2, 1.13)
    c.poly([(hx - 32, hy - 12), (hx + 44, hy - 12), (hx + 40, hy + 12), (hx - 28, hy + 12)], fill=BLACK)
    c.poly(r.pts(smooth([(-0.05, 1.2), (0.12, 1.28), (0.28, 1.2), (0.1, 1.17)], 4)), fill=col(0.2, 0.4, 0.8), line=INK,
           lw=r.lw())
    c.poly(r.pts([(-0.05, 1.21), (-0.2, 1.17), (-0.03, 1.15)]), fill=col(0.2, 0.4, 0.8), line=INK, lw=r.lw())
    # the crowd winces
    for i, (cx, who) in enumerate(((1060, 'beard'), (1190, 'auburn_scarf'))):
        audience(c, cx, 610, 170, who, 'cover' if crash > 0 else 'idle', t, -1, seed=i)


def s_lullaby(c, t, u):
    wash(c, col(0.25, 0.28, 0.5))
    c.poly(E(1100, 130, 60, 60), fill=YELLOW, line=INK, lw=4)
    c.poly(E(1125, 115, 50, 50), fill=col(0.25, 0.28, 0.5))
    for i in range(12):
        c.poly(E(80 + i * 97 % 1200, 60 + (i * 53) % 250, 4, 4), fill=YELLOW)
    c.poly([(380, 540), (900, 540), (900, 720), (380, 720)], fill=WOOD, line=INK, lw=5)  # a cot
    r, _ = pigeon(c, 640, 560, 260, 1, arms=(60, 50), mood='sleepy', t=t, lean=-6 * math.sin(t * 1.5))
    # a striped nightcap flopping off the back of his head, with a bobble
    cap = smooth([(-0.03, 1.19), (0.1, 1.26), (0.27, 1.19), (0.12, 1.33), (-0.12, 1.36), (-0.3, 1.22)], 5)
    c.poly(r.pts(cap), fill=col(0.55, 0.65, 0.95), line=INK, lw=r.lw())
    c.line(r.pts(smooth([(-0.04, 1.19), (0.1, 1.25), (0.26, 1.19)], 4, False)), WHITE, lw=r.lw(2.5))
    c.poly(r.E(-0.32, 1.2, 0.05, 0.05), fill=WHITE, line=INK, lw=r.lw())
    for x in range(400, 900, 50):
        c.line([(x, 540), (x, 420)], WOOD, lw=8)
    c.line([(380, 420), (900, 420)], WOOD, lw=10)
    for i in range(4):
        ph = (u * 2 + i * 0.25) % 1
        text(c, '♪' if i % 2 else '♫', 800 + 200 * ph, 380 - 250 * ph, 60, WHITE, opacity=1 - ph)
    text(c, 'Zzz', 520, 200 - 10 * math.sin(t * 2), 50, WHITE)


def s_nullified(c, t, u):
    wash(c, col(0.3, 0.42, 0.34))
    c.poly([(240, 100), (1040, 100), (1040, 560), (240, 560)], fill=col(0.18, 0.28, 0.22), line=WOOD, lw=16)
    text(c, 'GAME PLAN', 640, 150, 50, WHITE)
    for (x0, y0, x1, y1) in ((330, 300, 520, 250), (520, 250, 700, 380), (700, 380, 900, 280)):
        c.line([(x0, y0), (x1, y1)], WHITE, lw=5)
    for (x, y) in ((330, 300), (700, 380)):
        text(c, 'X', x, y, 40, WHITE)
        c.poly(E(900, 280, 22, 22), None, WHITE, lw=5)
    k = sstep(0.35, 0.6, u)
    if k > 0:
        c.line([(280, 130), (280 + 720 * k, 130 + 400 * k)], RED, lw=26)
        c.line([(1000, 130), (1000 - 720 * k, 130 + 400 * k)], RED, lw=26)
    if u > 0.65:
        text(c, 'NULL', 640, 640, 90, RED, rot=-8)


def s_supervision(c, t, u):
    """First look: the owl parents glare at the kid enjoying the forbidden rhymes.
    Second look: Mum steps in and swipes the headphones clean off; the kid bawls."""
    wash(c, col(0.9, 0.86, 0.8))
    c.poly([(300, 60), (980, 60), (980, 230), (300, 230)], fill=BLACK, line=INK, lw=6)
    c.poly([(310, 70), (970, 70), (970, 130), (310, 130)], fill=WHITE)
    text(c, 'PARENTAL', 640, 100, 44, BLACK)
    text(c, 'SUPERVISION', 640, 180, 58, WHITE)
    second = u > 0.5
    step = sstep(0.52, 0.58, u) if second else 0.0
    swipe = sstep(0.58, 0.63, u) if second else 0.0
    ox = lerp(330, 470, step)
    ra = bird(c, ox, 690 - 25 * math.sin(math.pi * step), 320, 'owl', 'idle', t, 1)
    rb = bird(c, 950, 690, 320, 'owl', 'idle', t, -1, seed=3)
    owl_brows(c, ra)
    owl_brows(c, rb)
    cry = second and u > 0.63
    kid = bird(c, 640, 700, 200, 'robin', 'laugh' if cry else 'idle', t, 1)
    hx, hy = kid.P(0.06, 0.72)
    if not second:
        for i in range(3):  # bopping along happily to the music
            ph = (u * 3 + i / 3) % 1
            text(c, '♪', hx + 60 + 30 * i, hy - 60 - 90 * ph, 40, INK, opacity=1 - ph)
    if second:
        # her wing, attached at the shoulder: raised, then swung hard across
        sx, sy = ra.P(0.12, 0.48)
        ang = math.radians(lerp(-115, 25, swipe))
        L = 175
        cx, cy = sx + math.cos(ang) * L / 2, sy + math.sin(ang) * L / 2
        c.poly(E(cx, cy, L / 2, 30, math.degrees(ang)), fill=col(0.52, 0.39, 0.26), line=INK, lw=5)
        tx, ty = sx + math.cos(ang) * L, sy + math.sin(ang) * L
        for k in (-1, 0, 1):  # feather tips
            a2 = ang + k * 0.25
            c.line([(tx - math.cos(ang) * 30, ty - math.sin(ang) * 30), (tx + math.cos(a2) * 18, ty + math.sin(a2) * 18)],
                   INK, lw=4)
        if 0.6 < u < 0.66:
            text(c, 'SWIPE!', sx + 120, sy - 150, 48, RED, rot=-8)
    # the headphones: on his head, then flying off across the room
    k = sstep(0.62, 0.9, u) if second else 0.0
    fx = lerp(hx, 1350, k)
    fy = hy - 280 * math.sin(math.pi * k)
    rr = math.radians(720 * k)
    band = [(fx + 55 * math.cos(q + rr), fy - 12 + 50 * math.sin(q + rr)) for q in np.linspace(math.pi, 2 * math.pi, 10)]
    c.line(band, INK, lw=8)
    for sg in (-1, 1):
        c.poly(E(fx + sg * 52 * math.cos(rr), fy + sg * 52 * math.sin(rr), 14, 20, math.degrees(rr)), fill=INK)
    if cry:  # floods of tears
        for sg in (-1, 1):
            ex, ey = kid.P(0.11 + 0.03 * sg, 0.73)
            for j in range(4):
                ph = (t * 3 + j / 4) % 1
                c.poly(E(ex + sg * (20 + 60 * ph), ey + 90 * ph * ph, 7, 10), fill=col(0.55, 0.75, 1.0), line=INK, lw=2)
        text(c, 'WAAAH', 760, 360, 50, RED, rot=-4 + 8 * (int(t * 6) % 2))


def s_permission(c, t, u):
    wash(c, col(0.92, 0.9, 0.84))
    penguin(c, 380, 700, 380, 1, arms=(95, 20), lean=5, beak=talk(t), eye='smug')
    c.poly([(560, 250), (900, 230), (920, 640), (580, 660)], fill=WHITE, line=INK, lw=6, jit=3)
    c.poly([(680, 225), (780, 220), (782, 255), (682, 260)], fill=SILVER if False else GREY, line=INK, lw=4)
    text(c, 'PERMISSION', 740, 310, 42, INK, rot=2)
    text(c, 'SLIP', 740, 360, 42, INK, rot=2)
    for i in range(4):
        c.line([(620, 420 + i * 45), (860, 410 + i * 45)], GREY, lw=4)
    text(c, 'sign here  X ____', 740, 610, 26, INK, rot=2)


SILVER = col(0.75, 0.76, 0.79)


def s_dish(c, t, u):
    wash(c, col(0.35, 0.18, 0.22))
    c.poly([(0, 520), (1280, 520), (1280, 720), (0, 720)], fill=WHITE, line=INK, lw=4)  # tablecloth
    c.poly(E(640, 560, 400, 90), fill=SILVER, line=INK, lw=6)
    c.poly(E(640, 550, 340, 70), fill=col(0.88, 0.89, 0.92), line=INK, lw=3)
    pigeon(c, 640, 590, 230, 1, arms=(20, 20), mood='shock', t=t)
    for (x, y) in ((420, 560), (860, 560), (520, 600), (760, 600)):
        c.poly(E(x, y, 30, 14), fill=GREEN, line=INK, lw=3)
        c.poly(E(x + 20, y - 5, 12, 8), fill=RED, line=INK, lw=2)
    k = sstep(0.0, 0.35, u)
    lift = 420 * k
    dome = [(640 + 330 * math.cos(q), 540 - lift - 300 * math.sin(q)) for q in np.linspace(0, math.pi, 20)]
    c.poly(dome, fill=SILVER, line=INK, lw=6)
    c.poly(E(640, 540 - lift - 305, 30, 18), fill=SILVER, line=INK, lw=4)
    if u > 0.4:
        text(c, 'SERVED.', 640, 90, 70, WHITE)


def s_scrub(c, t, u):
    wash(c, col(0.8, 0.9, 0.88))
    c.poly([(0, 560), (1280, 560), (1280, 720), (0, 720)], fill=col(0.7, 0.75, 0.78), line=INK, lw=4)
    c.poly([(700, 380), (1100, 380), (1080, 560), (720, 560)], fill=WHITE, line=INK, lw=5)  # sink
    c.line([(900, 380), (900, 260), (960, 260)], SILVER, lw=16)
    for i in range(6):
        ph = (u * 6 + i / 6) % 1
        c.line([(960, 270 + 110 * ph), (962, 290 + 110 * ph)], col(0.5, 0.7, 1.0), lw=5)
    arm = 80 + 25 * math.sin(t * 14)
    penguin(c, 560, 700, 380, 1, arms=(arm, 180 - arm), lean=6, shirt=False, hat='surgeon', eye='smug')
    c.poly(E(330, 150, 90, 90), fill=WHITE, line=INK, lw=6)  # stopwatch
    c.poly(E(330, 50, 20, 14), fill=SILVER, line=INK, lw=4)
    a = u * 2 * math.pi * 3
    c.line([(330, 150), (330 + 70 * math.sin(a), 150 - 70 * math.cos(a))], RED, lw=6)
    for i in range(12):
        q = i / 12 * 2 * math.pi
        c.line([(330 + 75 * math.sin(q), 150 - 75 * math.cos(q)), (330 + 86 * math.sin(q), 150 - 86 * math.cos(q))], INK,
               lw=3)
    for i in range(8):
        c.poly(E(640 + 60 * math.sin(i * 2.3 + t * 3), 300 - 40 * i % 180, 14, 14), None, col(0.6, 0.8, 1.0), lw=3)


def s_surgery(c, t, u):
    wash(c, col(0.72, 0.86, 0.84))
    c.glow(640, 0, 500, WHITE, 0.6)
    c.poly(E(640, 60, 180, 50), fill=col(0.95, 0.95, 0.9), line=INK, lw=5)  # operating lamp
    c.poly([(330, 520), (930, 520), (930, 560), (330, 560)], fill=SILVER, line=INK, lw=5)
    c.line([(390, 560), (390, 720)], SILVER, lw=16)
    c.line([(870, 560), (870, 720)], SILVER, lw=16)
    # the pigeon lying on the table, with a dotted line on his jumper
    c.poly(E(610, 480, 250, 55), fill=JUMPER, line=INK, lw=6)
    c.poly(E(860, 455, 65, 58), fill=PIGEON, line=INK, lw=6)
    c.poly(E(885, 440, 17, 17), fill=EYE_O, line=INK, lw=3)
    c.poly(E(890, 440, 6, 6), fill=INK)
    c.poly([(918, 460), (975, 470), (918, 478)], fill=col(0.3, 0.3, 0.33), line=INK, lw=3)
    for i in range(9):
        c.line([(420 + i * 40, 455), (440 + i * 40, 455)], INK, lw=5)
    # the nurse hands over the scalpel...
    standing_heron(c, 170, 700, 250, t, 1)
    # ...and the surgeon, standing beside the table, catches it and holds it up
    catch = u > 0.42
    r, front, back = penguin(c, 1110, 700, 300, -1, arms=(150 if catch else 95, 20), lean=4, shirt=False,
                             hat='surgeon', eye='angry')
    k = sstep(0.1, 0.42, u)
    if not catch:  # flying across, end over end
        sx, sy = lerp(260, 1000, k), 330 - 140 * math.sin(math.pi * k)
        a = k * 4 * math.pi
    else:
        sx, sy = r.P(*front)
        a = -math.pi / 2
    dx, dy = math.cos(a), math.sin(a)
    c.line([(sx - 30 * dx, sy - 30 * dy), (sx + 20 * dx, sy + 20 * dy)], SILVER, lw=10)
    tipx, tipy = sx + 20 * dx, sy + 20 * dy
    c.poly([(tipx - 8 * dy, tipy + 8 * dx), (tipx + 40 * dx, tipy + 40 * dy), (tipx + 8 * dy, tipy - 8 * dx)], fill=SILVER,
           line=INK, lw=3)
    if catch and u < 0.55:
        sparkle(c, sx + 30, sy - 70, 22, WHITE)
    text(c, 'SCALPEL.', 330, 120, 50, INK)


def s_reporter(c, t, u):
    """Thanks for your input, Tintin: our boy reporter, his old sea-dog captain and the dog, off on an adventure."""
    wash(c, col(0.98, 0.85, 0.6))
    c.glow(1050, 160, 220, YELLOW, 0.5)
    c.poly(E(1050, 160, 70, 70), fill=YELLOW, line=INK, lw=4)
    bob = 12 * math.sin(t * 2.2)
    tilt = 3 * math.sin(t * 2.2 + 0.8)
    # the boat and its passengers (drawn before the hull, so they sit inside it)
    captain(c, 380, 560 + bob, 330, t)
    r, _ = pigeon(c, 690, 600 + bob, 320, 1, arms=(95, 20), mood='grin', t=t, jumper=True, lean=tilt)
    quiff = smooth([(0.0, 1.2), (0.06, 1.32), (0.15, 1.42), (0.25, 1.43), (0.29, 1.38), (0.24, 1.36),
                    (0.2, 1.3), (0.18, 1.22)], 6)
    c.poly(r.pts(quiff), fill=col(0.95, 0.6, 0.25), line=INK, lw=r.lw())
    c.line(r.pts(smooth([(0.07, 1.23), (0.12, 1.33), (0.2, 1.39)], 4, False)), col(0.75, 0.4, 0.15), lw=r.lw(0.8))
    fx, fy = r.P(0.5, 0.74)
    c.poly([(fx - 10, fy - 55), (fx + 70, fy - 60), (fx + 72, fy + 15), (fx - 8, fy + 20)], fill=WHITE, line=INK, lw=4)
    text(c, 'INPUT:', fx + 30, fy - 30, 18, INK)
    terrier(c, 1010, 540 + bob, 150, t)
    hull = [(160, 520 + bob), (1150, 520 + bob), (1060, 660 + bob), (230, 660 + bob)]
    c.poly(hull, fill=col(0.85, 0.2, 0.2), line=INK, lw=6)
    c.line([(170, 548 + bob), (1140, 548 + bob)], WHITE, lw=10)
    text(c, 'ADVENTURE', 650, 605 + bob, 34, WHITE)
    # the sea
    waves = [(0, 640)] + [(x, 640 + 14 * math.sin(x / 50 + t * 3)) for x in range(0, 1300, 40)] + [(1280, 720), (0, 720)]
    c.poly(waves, fill=col(0.2, 0.45, 0.75), line=INK, lw=4)


def s_waxwork(c, t, u):
    wash(c, col(0.55, 0.2, 0.25))
    c.poly([(0, 600), (1280, 600), (1280, 720), (0, 720)], fill=col(0.3, 0.12, 0.16), line=INK, lw=4)
    for x in (200, 700):
        c.poly([(x, 540), (x + 380, 540), (x + 380, 620), (x, 620)], fill=col(0.9, 0.88, 0.8), line=INK, lw=5)
    pigeon(c, 390, 545, 360, 1, mood='neutral', t=0.0)
    c.glow(390, 330, 260, WHITE, 0.25)
    # Bigfoot's dim twin beside him
    bf = [(840, 540), (820, 300), (860, 170), (950, 150), (1030, 190), (1060, 320), (1040, 540)]
    c.poly(bf, fill=BROWN, line=INK, lw=6)
    c.hatch(bf, col(0.35, 0.24, 0.12), spacing=18, angle=70, lw=3, opacity=0.8)
    c.poly(E(915, 225, 18, 12), fill=WHITE, line=INK, lw=3)
    c.poly(E(985, 225, 18, 12), fill=WHITE, line=INK, lw=3)
    c.poly(E(918, 228, 5, 5), fill=INK)
    c.poly(E(983, 222, 5, 5), fill=INK)
    c.line([(920, 280), (950, 290), (980, 278)], INK, lw=4)
    # the six-foot measuring stick
    c.poly([(120, 90), (160, 90), (160, 540), (120, 540)], fill=YELLOW, line=INK, lw=4)
    for i in range(7):
        c.line([(120, 540 - i * 75), (145, 540 - i * 75)], INK, lw=4)
    text(c, "6'", 140, 70, 34, INK)
    for x, s in ((390, 'WAX'), (870, 'DIM TWIN')):
        text(c, s, x + 5, 585, 34, INK)
    c.line([(0, 640), (1280, 640)], RED, lw=6)


def s_vanity(c, t, u):
    wash(c, col(0.95, 0.85, 0.88))
    c.poly(E(820, 300, 220, 250), fill=col(0.85, 0.92, 0.95), line=WOOD, lw=16)
    for i in range(7):
        c.poly(E(820 + 230 * math.cos(i / 7 * 2 * math.pi), 300 + 260 * math.sin(i / 7 * 2 * math.pi), 16, 16),
               fill=YELLOW, line=INK, lw=3)
    pigeon(c, 440, 720, 380, 1, arms=(150 + 15 * math.sin(t * 9), 20), mood='grin', t=t)
    pigeon(c, 820, 480, 190, -1, arms=(150 + 15 * math.sin(t * 9), 20), mood='grin', t=t)  # the reflection, inside the glass
    c.poly(E(300, 120, 70, 70), fill=WHITE, line=INK, lw=5)  # clock racing round
    a = u * 2 * math.pi * 6
    c.line([(300, 120), (300 + 55 * math.sin(a), 120 - 55 * math.cos(a))], INK, lw=5)
    c.line([(300, 120), (300 + 35 * math.sin(a / 12), 120 - 35 * math.cos(a / 12))], INK, lw=7)


def s_yeti(c, t, u):
    wash(c, col(0.86, 0.92, 0.96))
    c.poly([(560, 300), (720, 300), (720, 640), (560, 640)], fill=col(0.3, 0.3, 0.32), line=INK, lw=5)  # barber chair
    c.poly([(520, 560), (760, 560), (760, 620), (520, 620)], fill=col(0.3, 0.3, 0.32), line=INK, lw=5)
    base = smooth([(470, 610), (440, 420), (470, 250), (560, 170), (720, 170), (810, 250), (840, 420), (810, 610)], 8)
    # shaggy fur: push every other outline point outwards
    cx, cy = 640, 400
    yeti = [(cx + (x - cx) * (1.05 if i % 2 else 0.97), cy + (y - cy) * (1.05 if i % 2 else 0.97))
            for i, (x, y) in enumerate(base)]
    c.poly(yeti, fill=WHITE, line=INK, lw=5)
    c.hatch(yeti, col(0.8, 0.84, 0.9), spacing=16, angle=75, lw=3)
    for (ax, ay, d) in ((440, 460, -1), (840, 460, 1)):  # big shaggy arms on the armrests
        arm = smooth([(ax, ay - 110), (ax + d * 60, ay - 40), (ax + d * 55, ay + 110), (ax - d * 10, ay + 120),
                      (ax - d * 20, ay)], 5)
        c.poly(arm, fill=WHITE, line=INK, lw=5)
    # a gleaming, perfectly coiffed side-parted do
    do = smooth([(510, 215), (540, 150), (620, 118), (720, 125), (790, 170), (785, 215), (700, 185), (600, 180)], 6)
    c.poly(do, fill=col(0.97, 0.97, 1.0), line=INK, lw=5)
    c.line(smooth([(590, 125), (605, 160), (600, 182)], 4, False), INK, lw=4)  # a crisp side parting
    for i in range(3):
        c.line(smooth([(630 + i * 40, 130 + i * 4), (660 + i * 40, 150), (700 + i * 30, 170)], 4, False),
               col(0.75, 0.8, 0.9), lw=3)
    c.glow(700, 140, 30, WHITE, 0.9)
    c.poly(E(640, 260, 90, 60), fill=PIGEON, line=INK, lw=5)  # a pigeon's face peeking out
    c.poly(E(670, 250, 14, 14), fill=EYE_O, line=INK, lw=3)
    c.poly(E(672, 250, 5, 5), fill=INK)
    c.line([(645, 222), (690, 238)], INK, lw=6)  # a cross little brow
    c.poly([(700, 265), (750, 272), (700, 282)], fill=col(0.3, 0.3, 0.33), line=INK, lw=3)
    # the barber pole
    c.poly([(1050, 150), (1110, 150), (1110, 560), (1050, 560)], fill=WHITE, line=INK, lw=5)
    for i in range(6):
        y = 205 + ((i * 60 + u * 120) % 350)
        c.line([(1054, y), (1106, y - 44)], RED, lw=14)
    # scissors snipping at his fringe, and the clippings drifting down
    k = 0.22 * abs(math.sin(t * 14))
    px, py = 470, 150
    for sgn in (1, -1):
        a = math.radians(-20 + sgn * 8 + sgn * 25 * k)
        tip = (px + 110 * math.cos(a), py + 110 * math.sin(a))
        c.poly([(px, py - 5), tip, (px, py + 5)], fill=SILVER, line=INK, lw=3)
        hx, hy = px - 45 * math.cos(a), py - 45 * math.sin(a) + sgn * 18
        c.line([(px, py), (hx, hy)], INK, lw=6)
        c.poly(E(hx - 10, hy + sgn * 8, 18, 14), None, RED, lw=6)
    c.poly(E(px, py, 5, 5), fill=INK)
    for i in range(7):
        ph = (u * 2.5 + i / 7) % 1
        x = 560 + (i * 41) % 150 + 20 * math.sin(ph * 9 + i)
        c.line([(x, 170 + 380 * ph), (x + 14, 176 + 380 * ph)], col(0.7, 0.72, 0.8), lw=4)


def s_weak(c, t, u):
    wash(c, col(0.93, 0.9, 0.8))
    arms = (-10 + 20 * math.sin(t * 20), 10 - 15 * math.sin(t * 17))
    r, front = pigeon(c, 640, 700, 470, 1, arms=arms, mood='shock', knees=1.0, t=t, lean=3 * math.sin(t * 25))
    sweat = col(0.6, 0.8, 1.0)
    # sweaty palms: drips running off his wing tips
    for k, (tx, ty) in enumerate((r.P(*front), r.P(-0.2, 0.3))):
        for i in range(4):
            ph = (t * 1.6 + i / 4 + k * 0.4) % 1
            c.poly(E(tx + 4 * math.sin(i * 3), ty + 10 + 150 * ph * ph, 7, 11), fill=sweat, line=INK, lw=2, opacity=1 - ph)
    for i in range(3):  # and a bead or two on his brow
        ph = (t * 0.9 + i / 3) % 1
        bx, by = r.P(0.05 + 0.05 * i, 1.2)
        c.poly(E(bx, by + 40 * ph, 6, 9), fill=sweat, line=INK, lw=2, opacity=1 - ph)
    text(c, 'weak', 300, 600, 40, INK, rot=10)
    text(c, 'pathetic', 1000, 400, 40, INK, rot=-10)


def s_vomit(c, t, u):
    wash(c, col(0.9, 0.93, 0.82))
    heave = sstep(0.12, 0.25, u)
    r, front = pigeon(c, 560, 700, 470, 1, arms=(-15 + 10 * math.sin(t * 20) * heave, 20), mood='sick', t=t,
                      lean=4 + 8 * heave + 2 * math.sin(t * 30) * heave, head_tilt=0.3 * heave)
    sweat = col(0.6, 0.8, 1.0)  # still sweating from the last scene
    c.poly(r.E(-0.1, 0.55, 0.07, 0.1), fill=JUMPER_D, opacity=0.5)
    for k, (tx, ty) in enumerate((r.P(*front), r.P(-0.2, 0.3))):
        for i in range(3):
            ph = (t * 1.6 + i / 3 + k * 0.4) % 1
            c.poly(E(tx, ty + 10 + 140 * ph * ph, 7, 11), fill=sweat, line=INK, lw=2, opacity=1 - ph)
    for i in range(3):
        ph = (t * 0.9 + i / 3) % 1
        bx, by = r.P(0.02 + 0.05 * i, 1.2)
        c.poly(E(bx, by + 40 * ph, 6, 9), fill=sweat, line=INK, lw=2, opacity=1 - ph)
    SICK_D = col(0.55, 0.6, 0.2)
    if u > 0.22:
        k = sstep(0.22, 0.34, u)
        gush = 1.0 if u < 0.75 else max(0.0, 1 - (u - 0.75) / 0.12)
        # the stream: out of the beak, arcing forward, then straight down onto his chest
        path = [(0.4 + 0.1 * q - 0.26 * q * q, 1.07 - 0.47 * q * q) for q in np.linspace(0, 1, 12)]
        n = max(2, int(12 * k))
        if gush > 0:
            pts = r.pts(path[:n])
            c.line(pts, INK, lw=r.s * 0.06 * gush + 6)
            c.line(pts, SICK, lw=r.s * 0.06 * gush)
            for i in range(5):  # chunks tumbling in the stream
                q = ((u * 7 + i / 5) % 1) * k
                cx, cy = r.P(0.4 + 0.1 * q - 0.26 * q * q, 1.07 - 0.47 * q * q)
                c.poly(E(cx + 6 * math.sin(i * 3), cy, 7, 5), fill=SICK_D)
        if k >= 1:
            # the splat spreading across the knitted jumper, with drips running down it
            g = sstep(0.34, 0.6, u)
            spl = smooth([(0.07, 0.62), (0.19, 0.68), (0.27, 0.6), (0.28, 0.46), (0.23, 0.4), (0.13, 0.44),
                          (0.05, 0.52)], 5)
            cu, cv = 0.18, 0.54
            spl = [(cu + (a - cu) * (0.5 + 0.5 * g), cv + (b - cv) * (0.5 + 0.5 * g)) for a, b in spl]
            c.poly(r.pts(spl), fill=SICK, line=INK, lw=r.lw(0.7))
            for i, du in enumerate((0.1, 0.16, 0.22, 0.26)):
                d = min(0.26, g * (0.1 + 0.05 * i) + 0.3 * max(0, u - 0.6) * (1 + i % 2))
                v0 = 0.5 - 0.03 * i
                c.line(r.pts([(du, v0), (du - 0.01, v0 - d)]), SICK, lw=r.lw(1.6))
                c.poly(r.E(du - 0.01, v0 - d, 0.018, 0.022), fill=SICK, line=INK, lw=r.lw(0.4))
            for i in range(6):
                c.poly(r.E(0.1 + 0.03 * i, 0.5 + 0.05 * math.sin(i * 2.1), 0.014, 0.01), fill=SICK_D)
            # a puddle building at his feet
            pw = 0.12 + 0.3 * sstep(0.45, 1.0, u)
            c.poly(r.E(0.3, 0.0, pw, pw * 0.18), fill=SICK, line=INK, lw=r.lw(0.6))
    if u > 0.55:
        text(c, 'DRY CLEAN ONLY', 330, 250, 34, INK, rot=-8)
        c.line([(420, 275), (520, 400)], INK, lw=4)
    # mum's pancetta bruschetta, the likely culprit
    c.poly(E(1030, 600, 190, 50), fill=WHITE, line=INK, lw=5)
    for x in (940, 1030, 1120):
        c.poly([(x - 40, 590), (x + 40, 580), (x + 45, 610), (x - 35, 620)], fill=col(0.85, 0.65, 0.35), line=INK, lw=3)
        c.poly(E(x, 585, 30, 10), fill=RED, line=INK, lw=2)
        c.poly(E(x + 10, 578, 18, 6), fill=col(0.95, 0.7, 0.7), line=INK, lw=2)
    text(c, "MUM'S", 1030, 500, 34, INK)
    if t > 59.4:  # ...with pesto and feta, piled on as he says it
        k = sstep(59.4, 60.2, t)
        for i, x in enumerate((945, 1035, 1125)):
            if k > i / 3:  # a green drizzle of pesto
                c.line(smooth([(x - 35, 572), (x - 15, 560), (x, 574), (x + 18, 560), (x + 35, 570)], 3, False),
                       col(0.3, 0.55, 0.2), lw=7)
                c.poly(E(x + 5, 566, 6, 4), fill=col(0.2, 0.4, 0.15))
        for j in range(int(6 * sstep(59.9, 60.5, t))):
            fx = 940 + j * 38
            c.poly([(fx, 548), (fx + 16, 548), (fx + 16, 564), (fx, 564)], fill=WHITE, line=INK, lw=2)  # feta cubes
        if k > 0:
            text(c, '+ pesto & feta', 1030, 460, 26, INK)


def s_lost(c, t, u):
    wash(c, col(0.96, 0.9, 0.7))
    # a vast hedge maze, the pigeon in the middle shrinking away to nothing
    for i in range(9):
        m = 40 + i * 70
        c.poly([(m, m * 0.56), (W - m, m * 0.56), (W - m, H - m * 0.56), (m, H - m * 0.56)], None, GREEN, lw=18 - i)
    s = 160 * (1 - sstep(0.0, 0.9, u)) ** 1.3
    if s > 3:
        pigeon(c, 640, 380 + s * 0.7, s, 1 if int(t * 2) % 2 else -1, mood='shock', t=t)
        if s > 30:
            text(c, '?', 640 + 30 * s / 160, 380 - s * 0.6, max(12, 60 * s / 160), INK)


def s_eagle(c, t, u):
    """You're the eagle, I'm the child: Andy as a noble bald-eagle penguin, Sam in a pram."""
    wash(c, SKY)
    c.poly([(0, 620), (1280, 620), (1280, 720), (0, 720)], fill=GREEN, line=INK, lw=4)
    c.poly(smooth([(120, 640), (180, 520), (420, 500), (520, 640)], 4), fill=GREY, line=INK, lw=5)  # his rock
    spread = 8 * math.sin(t * 2)
    penguin(c, 330, 560, 380, 1, arms=(60 + spread, 165 - spread), lean=-4, beak=talk(t), eye='angry', eagle=True)
    # the child: Sam, child-sized, bib on, pacifier in, gazing up at the eagle
    pr, _ = pigeon(c, 900, 640, 170, -1, arms=(20, 20), mood='neutral', t=t, head_tilt=-0.4)
    c.poly(pr.pts(smooth([(-0.02, 0.84), (0.26, 0.82), (0.24, 0.52), (0.1, 0.44), (-0.02, 0.52)], 4)), fill=WHITE, line=INK,
           lw=pr.lw())  # bib
    c.poly(pr.E(0.11, 0.62, 0.05, 0.04), fill=col(1.0, 0.75, 0.8))
    bx, by = pr.P(0.3, 1.08)
    c.poly(E(bx, by, 14, 16), fill=col(0.4, 0.7, 1.0), line=INK, lw=3)  # pacifier
    c.poly(E(bx - 10, by, 6, 20), fill=col(0.95, 0.9, 0.4), line=INK, lw=2)


def s_defiled(c, t, u):
    """The fact that I'm battling you leaves me feeling defiled: slimed, disgusted, scrubbing like mad."""
    wash(c, col(0.8, 0.9, 0.95))
    c.poly([(400, 60), (880, 60), (880, 700), (400, 700)], fill=col(0.9, 0.95, 0.98), line=INK, lw=5)
    for y in range(60, 700, 60):
        c.line([(400, y), (880, y)], col(0.7, 0.8, 0.85), lw=3)
    c.line([(780, 60), (780, 110), (720, 140)], SILVER, lw=12)
    for i in range(16):
        ph = (u * 4 + i * 0.07) % 1
        c.line([(560 + (i * 23) % 200, 150 + 450 * ph), (560 + (i * 23) % 200, 170 + 450 * ph)], col(0.5, 0.7, 1.0), lw=4)
    a = 95 + 55 * math.sin(t * 22)
    shake = 6 * math.sin(t * 31)
    r, front, back = penguin(c, 640 + shake, 690, 380, -1, arms=(a, 190 - a), shirt=False, eye='closed', lean=-6)
    # the sludge, slowly washing off him
    sludge = col(0.42, 0.4, 0.2)
    left = 1 - 0.6 * sstep(0.2, 1.0, u)
    for i, (su, sv, sr) in enumerate(((0.05, 0.9, 0.1), (-0.12, 0.62, 0.09), (0.12, 0.5, 0.11), (-0.05, 0.3, 0.08),
                                      (0.18, 0.78, 0.06))):
        c.poly(r.E(su, sv, sr * left, sr * 0.7 * left), fill=sludge, line=INK, lw=2, opacity=0.9)
        dx, dy = r.P(su, sv - sr * 0.6)
        c.line([(dx, dy), (dx, dy + 40 * left)], sludge, lw=6)
    # a grossed-out face: tongue out, beak twisted
    bx, by = r.P(0.2, 0.93)
    c.poly(E(bx + 5, by + 18, 14, 9, 20), fill=PINK, line=INK, lw=2)
    ex, ey = r.P(0.14, 1.02)
    c.line([(ex - 20, ey - 14), (ex + 18, ey - 4)], INK, lw=5)
    # scrubbing brushes in both flippers, and suds flying
    for tip in (front, back):
        fx, fy = r.P(*tip)
        c.poly([(fx - 30, fy - 12), (fx + 30, fy - 12), (fx + 30, fy + 12), (fx - 30, fy + 12)], fill=WOOD, line=INK, lw=3)
        for k in range(5):
            c.line([(fx - 24 + 12 * k, fy + 12), (fx - 24 + 12 * k, fy + 22)], YELLOW, lw=3)
    for i in range(14):
        ph = (t * 1.5 + i * 0.13) % 1
        sx = 640 + 180 * math.cos(i * 2.1) * (0.5 + ph)
        sy = 420 + 160 * math.sin(i * 1.7) * (0.5 + ph)
        c.poly(E(sx, sy, 14 + 6 * (i % 3), 14 + 6 * (i % 3)), fill=WHITE, line=col(0.6, 0.8, 1.0), lw=3, opacity=1 - ph)
    text(c, 'EWW', 1060, 220, 60, col(0.42, 0.4, 0.2), rot=8)


def s_chin(c, t, u):
    wash(c, col(0.93, 0.92, 0.88))
    c.cam = (1.0, 0.0, 0.0)
    r, front = pigeon(c, 560, 1400, 1100, 1, mood='grin', t=t)
    # the magnifying glass on the crease of his chin
    k = sstep(0.2, 0.5, u)
    mx, my = lerp(1100, 780, k), lerp(600, 330, k)
    c.poly(E(mx, my, 120, 120), fill=col(0.85, 0.93, 1.0), line=INK, lw=10, opacity=0.6)
    c.line([(mx + 85, my + 85), (mx + 200, my + 200)], WOOD_D, lw=24)
    if u > 0.45:
        for i in range(7):
            c.poly(blob(mx - 40 + (i * 29) % 90, my - 20 + (i * 37) % 60, 10, i, 8, 0.3), fill=BROWN, line=INK, lw=2)
        for i in range(3):
            q = t * 8 + i * 2
            fx, fy = mx + 90 * math.cos(q), my - 60 + 30 * math.sin(q * 1.3)
            c.poly(E(fx, fy, 8, 6), fill=INK)
            c.poly(E(fx - 5, fy - 8, 7, 4, 30), fill=WHITE, line=INK, lw=1.5)


def s_yarn(c, t, u):
    """Not spinning a yarn, tying a noose: the more he knits, the tighter his own knitting cinches round his neck."""
    wash(c, col(0.95, 0.88, 0.8))
    k = sstep(0.1, 0.9, u)
    r, front = pigeon(c, 560, 700, 420, 1, arms=(100, 70), mood='shock', t=t, head_tilt=0.3 * k)
    fx, fy = r.P(*front)
    click = 8 * math.sin(t * 18)
    c.line([(fx - 60, fy - 60 + click), (fx + 60, fy + 20)], SILVER, lw=6)  # knitting needles going
    c.line([(fx - 40, fy + 20), (fx + 70, fy - 50 - click)], SILVER, lw=6)
    c.poly(E(980, 620, 70, 60), fill=RED, line=INK, lw=5)
    # loose loops of wool that draw in towards his neck as he knits
    nx, ny = r.P(0.1, 0.9)
    for i in range(7):
        a0 = i * 0.9
        rx, ry = lerp(210, 70, k) + 12 * i * (1 - k), lerp(160, 30, k) + 6 * i * (1 - k)
        pts = [(nx + rx * math.cos(a0 + q), ny + ry * math.sin(a0 + q)) for q in np.linspace(0, 2 * math.pi, 16)]
        c.line(pts, RED, lw=6)
    c.line([(980, 620), (820, 520), (fx, fy)], RED, lw=6)
    if k > 0.6:  # a snug knitted collar, eyes bulging, face going green
        hx, hy = r.P(0.14, 1.12)
        c.poly(E(hx, hy, 60, 55), fill=col(0.55, 0.75, 0.3), opacity=0.35 * (k - 0.6) / 0.4)
        for sg in (-1, 1):
            c.line([(hx + 45 + 10 * sg, hy - 50), (hx + 55 + 20 * sg, hy - 75)], INK, lw=3)


def s_noggin(c, t, u):
    wash(c, col(0.9, 0.92, 0.95))
    r, _ = pigeon(c, 610, 700, 250, 1, mood='neutral', t=t)
    knock = abs(math.sin(t * 9))
    # he steps in and raps his flipper on the pigeon's head
    penguin(c, 800, 700, 330, -1, arms=(108 + 8 * knock, 15), lean=0, beak=talk(t), eye='smug')
    hx, hy = r.P(0.1, 1.24)
    if knock > 0.85:
        for k in (-1, 0, 1):
            c.line([(hx + 25 * k, hy - 20), (hx + 38 * k, hy - 48)], INK, lw=3)
    # a light bulb over the pigeon's head that will not come on
    c.poly(E(hx - 60, hy - 120, 45, 55), fill=col(0.85, 0.85, 0.8) if int(t * 4) % 3 else YELLOW, line=INK, lw=5)
    c.poly([(hx - 78, hy - 70), (hx - 42, hy - 70), (hx - 44, hy - 48), (hx - 76, hy - 48)], fill=GREY, line=INK, lw=4)


def s_corn(c, t, u):
    wash(c, col(0.99, 0.95, 0.75))
    r, front = pigeon(c, 540, 810, 440, 1, arms=(95, 90), mood='grin', t=t)
    # a corn on the cob, typewriter-style: munch along the row, DING, back to the start
    ph = (u * 2) % 1
    x0 = lerp(700, 400, ph)
    L = 360
    cob = smooth([(x0, 340), (x0 + L * 0.5, 325), (x0 + L, 340), (x0 + L, 400), (x0 + L * 0.5, 412), (x0, 400)], 5)
    c.poly(cob, fill=YELLOW, line=INK, lw=5)
    eaten = max(0, (740 - x0))  # the part that has been past his beak is bare
    for i in range(14):
        for j in range(3):
            kx = x0 + 14 + i * 24 + (j % 2) * 12
            if kx - x0 < eaten:
                continue
            c.poly(E(kx, 345 + j * 22, 10, 9), fill=col(0.98, 0.82, 0.25), line=col(0.8, 0.6, 0.1), lw=2)
    if eaten > 0:
        c.poly([(x0 + 4, 350), (x0 + min(L, eaten), 350), (x0 + min(L, eaten), 392), (x0 + 4, 392)],
               fill=col(0.95, 0.9, 0.7), line=None)
    for (hx, d) in ((x0 + L, 1),):  # husk leaves at the far end
        c.poly([(hx, 345), (hx + d * 70, 300), (hx + d * 30, 370), (hx + d * 80, 430), (hx, 395)], fill=GREEN,
               line=INK, lw=4)
    for i in range(6):
        ph = (u * 5 + i * 0.17) % 1
        c.poly(E(700 + 200 * ph, 420 + 280 * ph * ph, 8, 6), fill=YELLOW, line=INK, lw=2)
    text(c, 'DING!', 1050, 220, 44, RED) if (u * 2) % 1 < 0.15 else None


def s_pillow(c, t, u):
    wash(c, col(0.85, 0.83, 0.9))
    r, front = pigeon(c, 480, 700, 430, 1, arms=(100, 95), mood='grin', t=t)
    fx, fy = r.P(*front)
    c.poly(blob(fx + 60, fy, 90, 3, 20, 0.12), fill=WHITE, line=INK, lw=6)
    for i in range(4):
        ph = (u * 2 + i * 0.25) % 1
        c.poly(E(fx + 40 + 150 * ph, fy - 60 - 100 * ph, 10, 5, 30 * i), fill=WHITE, line=INK, lw=2, opacity=1 - ph)
    text(c, 'FIGHT NIGHT', 640, 90, 56, RED)


def s_pipe(c, t, u):
    wash(c, col(0.85, 0.83, 0.9))
    r, front = pigeon(c, 380, 700, 380, 1, arms=(90, 90), mood='shock', knees=1.0, t=t)
    fx, fy = r.P(*front)
    c.poly(blob(fx + 50, fy, 70, 3, 20, 0.12), fill=WHITE, line=INK, lw=6)
    # the pipe held low, tapped menacingly into his other flipper
    tap = abs(math.sin(t * 5))
    rr, pf, pb = penguin(c, 930, 700, 340, -1, arms=(60 + 25 * tap, 70), lean=4, beak=talk(t), eye='angry')
    px, py = rr.P(*pf)
    qx, qy = rr.P(*pb)
    dx, dy = qx - px, qy - py
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    ax, ay = px - ux * 170, py - uy * 170  # a long, heavy length of pipe, well past both flippers
    bx2, by2 = qx + ux * 60, qy + uy * 60
    nx, ny = -uy * 17, ux * 17
    c.poly([(ax + nx, ay + ny), (bx2 + nx, by2 + ny), (bx2 - nx, by2 - ny), (ax - nx, ay - ny)], fill=SILVER, line=INK, lw=5)
    c.line([(ax + nx * 0.4, ay + ny * 0.4), (bx2 + nx * 0.4, by2 + ny * 0.4)], WHITE, lw=5)
    for (ex, ey) in ((ax, ay), (bx2, by2)):
        c.poly(E(ex, ey, 19, 19), fill=col(0.35, 0.35, 0.38), line=INK, lw=4)
        c.poly(E(ex, ey, 10, 10), fill=col(0.15, 0.15, 0.17))
    sparkle(c, ax + ux * 60 + nx, ay + uy * 60 + ny - 10, 14 + 6 * abs(math.sin(t * 4)), WHITE)


def s_innate(c, t, u):
    """It's entirely innate: the egg shakes, cracks, and out he bursts, shimmering and already rapping."""
    wash(c, col(0.95, 0.92, 0.85))
    text(c, 'INNATE.', 640, 80, 60, INK)
    burst = sstep(0.35, 0.5, u)
    shell = col(0.97, 0.95, 0.88)
    egg = smooth([(640, 250), (760, 330), (800, 480), (740, 640), (640, 670), (540, 640), (480, 480), (520, 330)], 8)
    if burst <= 0:
        wob = 8 * math.sin(t * 30) * sstep(0.05, 0.3, u)
        c.poly([(x + wob, y) for x, y in egg], fill=shell, line=INK, lw=6)
        crack = [(500, 440), (560, 410), (600, 460), (650, 400), (700, 455), (750, 420), (790, 440)]
        n = 1 + int(6 * sstep(0.08, 0.32, u))
        c.line([(x + wob, y) for x, y in crack[:n + 1]], INK, lw=6)
        return
    # the shell blows apart into jagged pieces
    pieces = [([(520, 440), (560, 410), (600, 460), (650, 400), (650, 250), (560, 280)], -1.0, -1.2),
              ([(650, 400), (700, 455), (750, 420), (790, 440), (770, 320), (650, 250)], 1.0, -1.1),
              ([(480, 480), (500, 440), (560, 520), (540, 640)], -1.3, 0.3),
              ([(800, 480), (790, 440), (730, 520), (740, 640)], 1.3, 0.4)]
    for pts, dx, dy in pieces:
        k = burst
        ox, oy = dx * 420 * k, dy * 300 * k + 400 * k * k
        rot = 200 * k * dx
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        ra = math.radians(rot)
        moved = [(cx + ox + (x - cx) * math.cos(ra) - (y - cy) * math.sin(ra),
                  cy + oy + (x - cx) * math.sin(ra) + (y - cy) * math.cos(ra)) for x, y in pts]
        c.poly(moved, fill=shell, line=INK, lw=5)
    # the jagged bottom of the shell he stands in
    c.poly([(560, 700), (720, 700), (740, 640), (705, 600), (680, 630), (650, 590), (620, 630), (590, 600), (545, 640)],
           fill=shell, line=INK, lw=5)
    pop = 0.7 + 0.3 * sstep(0.35, 0.55, u)
    c.glow(640, 420, 330, YELLOW, 0.55)
    arms = (95, 20) if int(t * 2.2) % 2 else (125, 160)
    penguin(c, 640, 680, 330 * pop, 1, arms=arms, lean=6, beak=talk(t), eye='smug')
    for i in range(10):  # shimmering
        a = i * 0.63 + t * 1.5
        rr = 230 + 40 * math.sin(t * 5 + i)
        sparkle(c, 640 + rr * math.cos(a), 430 + rr * 0.8 * math.sin(a), 12 + 8 * abs(math.sin(t * 7 + i)))


def s_mistakes(c, t, u):
    wash(c, col(0.94, 0.94, 0.92))
    c.poly([(380, 520), (900, 520), (900, 560), (380, 560)], fill=WOOD, line=INK, lw=5)
    c.line([(420, 560), (420, 720)], WOOD, lw=12)
    c.line([(860, 560), (860, 720)], WOOD, lw=12)
    r, _ = pigeon(c, 640, 700, 330, 1, mood='hurt', t=t)
    # a dunce's cap perched on his head
    c.poly(r.pts([(-0.04, 1.2), (0.28, 1.21), (0.1, 1.72)]), fill=col(0.95, 0.9, 0.7), line=INK, lw=r.lw())
    c.line(r.pts([(0.02, 1.33), (0.22, 1.34)]), RED, lw=r.lw(1.5))
    text(c, 'D', *r.P(0.12, 1.38), 30, INK)
    c.poly([(470, 460), (720, 450), (730, 520), (475, 525)], fill=WHITE, line=INK, lw=4)
    for i in range(min(5, int(u * 8))):
        text(c, 'X', 500 + i * 48, 490, 40, RED)
    text(c, 'F', 900, 200, 160, RED, rot=-12)


def s_wait(c, t, u):
    """Go ahead, I'll wait: same room, same moment; he folds his flippers and taps his foot while the clock races."""
    t0 = 139.8
    room(c, t, clock_speed=0.02 + 6 * sstep(t0 + 0.3, t0 + 0.8, t))
    k = sstep(t0, t0 + 0.5, t)  # ease out of the previous shot rather than jumping
    crowd(c, t, ['gasp', 'cover', 'gasp', 'laugh', 'cover', 'gasp', 'laugh', 'cover'] if k < 0.5 else None)
    pigeon_listens(c, t)
    (a0, b0), lean0 = penguin_pose(t0 - 0.01, MOODS['gasp'])
    tap = abs(math.sin(t * 8)) * k
    arms = (lerp(a0, 55, k), lerp(b0, 55, k))
    penguin(c, penguin_x(t), 690 - 6 * tap, 300, -1, arms=arms, lean=lerp(lean0, -6, k), beak=talk(t), eye='smug')
    if k > 0.6:
        text(c, 'tap', penguin_x(t) + 60, 700 - 40 * tap, 28, INK)


def s_firesale(c, t, u):
    wash(c, col(0.98, 0.85, 0.6))
    c.poly([(300, 250), (980, 250), (980, 600), (300, 600)], fill=col(0.85, 0.75, 0.6), line=INK, lw=6)  # a market stall
    for i in range(7):
        c.poly([(300 + i * 97, 200), (397 + i * 97, 200), (397 + i * 97, 250), (300 + i * 97, 250)],
               fill=RED if i % 2 else WHITE, line=INK, lw=4)
    for i in range(8):
        ph = (t * 3 + i * 0.37) % 1
        x = 330 + i * 85
        c.poly([(x - 30, 250), (x, 250 - 90 - 40 * math.sin(t * 13 + i)), (x + 30, 250)], fill=col(1, 0.55, 0.15),
               line=RED, lw=4)
    text(c, 'FIRE SALE', 640, 120, 60, RED)
    text(c, 'DATES  1p', 640, 330, 44, INK)
    for x in range(420, 880, 70):
        c.poly(E(x, 420, 26, 14), fill=BROWN, line=INK, lw=3)
    r, front = pigeon(c, 1100, 700, 300, -1, arms=(90, 10), mood='hurt', t=t)
    fx, fy = r.P(*front)
    c.poly([(fx - 35, fy - 25), (fx + 35, fy - 25), (fx + 35, fy + 25), (fx - 35, fy + 25)], fill=BROWN, line=INK, lw=3)
    c.poly(E(fx, fy - 45, 14, 8), fill=GREY, line=INK, lw=2)  # a moth out of the wallet
    text(c, 'still no date', 1060, 280, 30, INK)


def s_crake(c, t, u):
    """A child of Crake: serene, flawless, grass-eating, citrus-scented, purring in a circle, bug-proof."""
    wash(c, col(0.86, 0.94, 0.8))
    c.glow(640, 380, 420, col(1, 0.97, 0.8), 0.4)
    text(c, 'CHILD OF CRAKE', 640, 70, 50, col(0.25, 0.45, 0.25))
    tones = [col(0.45, 0.3, 0.2), col(0.95, 0.78, 0.65), col(0.75, 0.55, 0.38), col(0.6, 0.42, 0.28)]
    hairs = [col(0.1, 0.08, 0.06), col(0.85, 0.7, 0.35), col(0.3, 0.2, 0.1), col(0.15, 0.1, 0.08)]
    for i, x in enumerate((170, 390, 890, 1110)):
        craker(c, x, 560 + 6 * math.sin(t * 2 + i), 330, tones[i], hairs[i], t, i)
    r, _ = pigeon(c, 640, 600, 300, 1, arms=(95, 20), mood='sleepy', t=t, lean=2 * math.sin(t * 2))
    c.glow(640, 420, 170, WHITE, 0.3)
    lx, ly = r.P(0.45, 0.8)  # munching a leaf
    c.poly(E(lx, ly, 34, 16, -20), fill=GREEN, line=INK, lw=3)
    c.poly([(0, 560), (1280, 560), (1280, 720), (0, 720)], fill=col(0.45, 0.7, 0.35), line=INK, lw=4)
    for x in range(0, 1300, 26):
        c.line([(x, 560), (x + 8, 520 + 12 * math.sin(x))], col(0.35, 0.6, 0.3), lw=4)
    text(c, 'purrrr', 300 + 20 * math.sin(t * 5), 300, 34, INK, rot=-6)
    text(c, 'purrrr', 980 + 20 * math.sin(t * 5 + 1), 300, 34, INK, rot=6)
    # a citrus scent that keeps the insects off
    c.poly(E(1180, 170, 45, 32), fill=YELLOW, line=INK, lw=4)
    text(c, 'citrus', 1180, 230, 22, INK)
    for i in range(4):
        ph = (t * 1.3 + i / 4) % 1
        mx = 640 + 260 * math.cos(i * 1.6 + t) * (1 - 0.3 * math.sin(ph * math.pi))
        my = 250 + 60 * math.sin(i * 2.2 + t * 2)
        c.line([(mx - 8, my - 8), (mx + 8, my + 8)], INK, lw=3)
        c.line([(mx - 8, my + 8), (mx + 8, my - 8)], INK, lw=3)
        c.poly(E(mx, my, 5, 3), fill=INK)


def s_crap(c, t, u):
    wash(c, col(0.9, 0.9, 0.86))
    pile = [(380, 700), (420, 560), (460, 580), (480, 430), (540, 450), (560, 300), (640, 330), (660, 200), (720, 230),
            (760, 350), (800, 340), (820, 480), (880, 470), (900, 580), (940, 580), (980, 700)]
    k = sstep(0.0, 0.3, u)
    c.poly([(x, 700 - (700 - y) * k) for x, y in pile], fill=BROWN, line=INK, lw=6)
    if u > 0.3:
        pigeon(c, 690, 230, 120, 1, mood='grin', t=t)  # on top, pleased with himself
        c.line([(760, 130), (760, 30)], INK, lw=5)
        c.poly([(760, 30), (840, 50), (760, 70)], fill=RED, line=INK, lw=3)
        for i in range(4):
            q = t * 7 + i * 1.6
            c.poly(E(640 + 200 * math.cos(q), 400 + 80 * math.sin(q * 1.4), 7, 5), fill=INK)
    c.poly([(1080, 110), (1120, 110), (1120, 700), (1080, 700)], fill=YELLOW, line=INK, lw=4)
    for i in range(7):
        c.line([(1080, 700 - i * 95), (1105, 700 - i * 95)], INK, lw=4)
    text(c, "6'", 1100, 85, 34, INK)
    if u > 0.55:
        text(c, 'impressive.', 300, 150, 50, INK, rot=-6)


def s_blackeye(c, t, u):
    wash(c, col(0.94, 0.86, 0.86))
    hit = u > 0.5
    shake = 10 * math.sin(t * 40) * (1 - sstep(0.5, 0.65, u)) if hit else 0
    r, front = pigeon(c, 420 + shake, 700, 360, 1, mood='hurt' if hit else 'neutral', t=t, lean=-10 if hit else 0,
                      blackeye=sstep(0.5, 0.7, u))
    if hit:
        ex, ey = r.P(0.18, 1.13)
        for i in range(4):
            q = t * 6 + i * 1.57
            text(c, '*', ex + 90 * math.cos(q), ey - 90 + 25 * math.sin(q), 40, YELLOW)
    a = 90 + 30 * math.sin(t * 20) if u < 0.42 else (95 if u > 0.55 else 90)
    px = 950 if not (0.42 < u < 0.55) else 760  # the punch lands
    penguin(c, px, 700, 360, -1, arms=(a, 180 - a) if u < 0.42 else (90, 20), lean=12 if u < 0.42 else 25,
            beak=talk(t), eye='angry')
    if 0.45 < u < 0.55:
        text(c, 'POW', 600, 300, 80, RED, rot=-10)
    text(c, 'half a mind...', 950, 150, 40, INK)


def s_factory(c, t, u):
    wash(c, col(0.75, 0.76, 0.78))
    c.poly([(0, 520), (1280, 520), (1280, 570), (0, 570)], fill=col(0.3, 0.3, 0.32), line=INK, lw=5)  # conveyor
    for i in range(16):
        x = (i * 90 + u * 400) % 1400 - 60
        c.poly(E(x, 575, 22, 22), None, INK, lw=4)
    for i in range(5):
        x = (i * 280 + u * 400) % 1400 - 100
        c.poly(E(x, 460, 50, 62), fill=col(0.95, 0.94, 0.9), line=INK, lw=5)
    c.poly([(560, 60), (720, 60), (720, 300), (560, 300)], fill=GREY, line=INK, lw=6)  # the stamping press
    y = 300 + 80 * max(0.0, math.sin(t * 6))
    c.poly([(580, 300), (700, 300), (700, y), (580, y)], fill=SILVER, line=INK, lw=5)


def s_practice(c, t, u):
    """Please, you need to keep practicing: rapping at the mirror, trying far too hard, one single tear."""
    wash(c, col(0.9, 0.9, 0.95))
    c.poly([(760, 100), (1100, 100), (1100, 640), (760, 640)], fill=col(0.85, 0.92, 0.95), line=WOOD, lw=14)
    beat = int(t * 2.5) % 3
    arms = [(95, 20), (100, 125), (60, 130)][beat]
    wb = 0.9 if int(t * 6) % 2 else 0.1
    r, front = pigeon(c, 480, 700, 400, 1, arms=arms, lean=8, mood='cross', t=t, beak=wb)
    rr, _ = pigeon(c, 930, 600, 300, -1, arms=arms, lean=8, mood='cross', t=t, beak=wb)  # his reflection
    for rig in (r, rr):  # a single tear rolling down his cheek
        ex, ey = rig.P(0.16, 1.1)
        ty = ey + 20 + 60 * ((t * 0.6) % 1)
        c.poly([(ex + 3, ty - 14), (ex + 10, ty + 2), (ex + 3, ty + 8), (ex - 4, ty + 2)], fill=col(0.55, 0.78, 1.0),
               line=INK, lw=2)
    for i in range(3):
        ph = (t * 2 + i / 3) % 1
        bx, by = r.P(0.4, 1.3)
        c.line([(bx + 30 * i, by - 10 - 40 * ph), (bx + 30 * i + 12, by - 30 - 40 * ph)], INK, lw=3, opacity=1 - ph)


def s_expectations(c, t, u):
    """I'll expectorate on each one of your expectations separately: he flies over, spitting on each box in turn."""
    wash(c, SKY)
    c.poly([(0, 600), (1280, 600), (1280, 720), (0, 720)], fill=GREEN, line=INK, lw=4)
    boxes = [(170, 'HOPES'), (440, 'DREAMS'), (710, 'PLANS'), (1030, 'EXPECTATIONS')]
    px = lerp(60, 1200, u)
    spit_c = col(0.85, 0.93, 0.97)
    for i, (x, lab) in enumerate(boxes):
        w = 110 if i < 3 else 150
        c.poly([(x - w, 470), (x + w, 470), (x + w, 600), (x - w, 600)], fill=col(0.85, 0.75, 0.55), line=INK, lw=5)
        text(c, lab, x, 540, 30 if i < 3 else 27, INK)
        # a gob of spit falls from his beak as he passes over each box, then splats on its lid
        drop_x = x - 60
        tu = (px - drop_x) / 1140.0
        if 0 < tu < 0.08:
            k = tu / 0.08
            c.poly(E(drop_x + 40 + 30 * k, lerp(250, 460, k * k), 12, 16), fill=spit_c, line=INK, lw=3)
        elif tu >= 0.08:
            c.poly(blob(x, 468, 45, 7 + i, 12, 0.35), fill=spit_c, line=INK, lw=3, opacity=0.9)
            c.poly(E(x + 25, 490, 8, 18), fill=spit_c, line=INK, lw=2)  # a drip down the side
    r, f, b = penguin(c, px, 260, 180, 1, arms=(170, 170), beak=0.8 if int(t * 5) % 2 else 0.1, eye='angry')
    c.poly([(px - 60, 200), (px - 30, 200), (px - 30, 260), (px - 60, 260)], fill=SILVER, line=INK, lw=3)
    c.poly([(px - 55, 260), (px - 35, 260), (px - 45, 300 + 20 * math.sin(t * 30))], fill=ORANGE, line=RED, lw=3)
    text(c, 'PTOO!', px + 90, 180, 34, INK, rot=-8)


def s_integrity(c, t, u):
    """An imminent threat to your physical integrity: the pigeon gets steadily more battered."""
    wash(c, col(0.95, 0.9, 0.8))
    stage_n = int(sstep(0.05, 0.95, u) * 4.999)
    jolt = 12 * math.sin(t * 50) * max(0.0, 1 - ((u * 5) % 1) * 4)
    r, front = pigeon(c, 540 + jolt, 700, 440, 1, arms=(40, 20) if stage_n < 3 else (90, 20),
                      mood=['shock', 'hurt', 'hurt', 'dizzy', 'dizzy'][stage_n], t=t,
                      lean=[0, -4, -6, -10, -14][stage_n] + 2 * math.sin(t * 3), blackeye=1.0 if stage_n >= 2 else 0.0,
                      knees=0.6 if stage_n >= 3 else 0.0)
    bruise = col(0.45, 0.3, 0.55)
    if stage_n >= 1:  # a bruise on the cheek and a sticking plaster
        c.poly(r.E(0.02, 1.03, 0.05, 0.035), fill=bruise, opacity=0.8)
        c.poly(r.pts([(-0.05, 1.2), (0.12, 1.25), (0.13, 1.21), (-0.04, 1.16)]), fill=TAN, line=INK, lw=3)
    if stage_n >= 2:  # bruises down his front and a bent tail feather
        for (bu, bv) in ((0.05, 0.6), (-0.1, 0.45), (0.15, 0.35)):
            c.poly(r.E(bu, bv, 0.05, 0.04), fill=bruise, opacity=0.6)
    if stage_n >= 3:  # head bandaged, wing in a sling
        c.poly(r.pts(smooth([(-0.04, 1.15), (0.1, 1.26), (0.27, 1.15), (0.27, 1.1), (0.1, 1.2), (-0.04, 1.1)], 4)),
               fill=WHITE, line=INK, lw=3)
        c.poly(r.pts([(-0.05, 0.85), (0.3, 0.55), (0.34, 0.45), (0.2, 0.42), (-0.1, 0.8)]), fill=WHITE, line=INK, lw=3)
    if stage_n >= 4:  # a crutch, and feathers floating off
        cx, cy = r.P(0.45, 0.0)
        c.line([(cx, cy), (cx - 20, cy - 330)], WOOD, lw=12)
        c.line([(cx - 55, cy - 330), (cx + 15, cy - 330)], WOOD, lw=14)
        for i in range(4):
            ph = (t * 0.7 + i / 4) % 1
            fx, fy = 540 + 200 * math.sin(i * 2 + ph * 3), 200 + 400 * ph
            c.poly(E(fx, fy, 22, 8, 40 * math.sin(t * 3 + i)), fill=PIGEON, line=INK, lw=2)
    for i in range(stage_n):
        text(c, ['BOP', 'WHACK', 'THUD', 'CRUNCH'][i], 200 + (i % 2) * 850, 150 + 120 * i, 44, RED, rot=(-1) ** i * 10)


def s_dinner(c, t, u):
    """Dining in good company: T and Hannibal, seated, sharing a bloody steak and fava beans, glasses raised."""
    wash(c, col(0.35, 0.15, 0.18))
    c.glow(640, 380, 300, AMBER, 0.35)
    chair(c, 250, 690, 1)
    chair(c, 1030, 690, -1)
    # the mask, hung politely on the back of his chair
    c.poly([(1030 + 20, 380), (1090, 380), (1090, 430), (1030 + 20, 430)], None, INK, lw=5)
    for x in range(1060, 1090, 10):
        c.line([(x, 380), (x, 430)], INK, lw=3)
    cheers = u > 0.6
    penguin(c, 290, 600, 280, 1, arms=(115 if cheers else 80, 20), beak=talk(t), eye='smug')
    hy = hannibal(c, 990, 600, 330, t)
    # the table
    c.poly([(330, 480), (950, 480), (950, 510), (330, 510)], fill=WHITE, line=INK, lw=4)
    c.poly([(330, 510), (950, 510), (945, 575), (335, 575)], fill=col(0.97, 0.96, 0.93), line=INK, lw=4)
    for x in (400, 640, 880):
        c.line([(x, 515), (x - 2, 570)], col(0.85, 0.84, 0.8), lw=3)
    for x in (370, 910):  # table legs
        c.line([(x, 575), (x, 700)], WOOD_D, lw=14)
    for x in (480, 800):  # plates of rare steak with fava beans
        c.poly(E(x, 480, 95, 24), fill=WHITE, line=INK, lw=4)
        c.poly(E(x - 15, 474, 48, 16), fill=col(0.5, 0.22, 0.16), line=INK, lw=3)
        c.poly(E(x - 15, 473, 30, 8), fill=col(0.78, 0.25, 0.28))
        c.poly(E(x + 30, 488, 26, 6), fill=col(0.65, 0.05, 0.1), opacity=0.8)
        for i in range(4):
            c.poly(E(x + 40 + (i % 2) * 14, 470 + 7 * i // 2, 8, 5), fill=GREEN, line=INK, lw=2)
    c.poly([(625, 480), (655, 480), (650, 380), (630, 380)], fill=col(0.3, 0.12, 0.14), line=INK, lw=4)  # chianti
    c.poly([(620, 440), (660, 440), (657, 470), (623, 470)], fill=col(0.95, 0.85, 0.55), line=INK, lw=2)
    c.line([(700, 480), (700, 400)], col(0.97, 0.95, 0.85), lw=12)  # candle
    c.poly(E(700, 390, 7, 12), fill=YELLOW, line=ORANGE, lw=2)
    c.glow(700, 390, 60, YELLOW, 0.5)
    for (gx, lx) in ((lerp(420, 600, sstep(0.6, 0.75, u)), 380), (lerp(870, 690, sstep(0.6, 0.75, u)), 920)):
        gy = 400 if cheers else 470
        c.poly([(gx - 16, gy - 40), (gx + 16, gy - 40), (gx + 10, gy), (gx - 10, gy)], fill=col(0.55, 0.05, 0.12), line=INK, lw=3)
        c.line([(gx, gy), (gx, gy + 25)], INK, lw=3)
    if cheers and u < 0.8:
        text(c, 'clink', 645, 330, 32, INK)


def s_podium(c, t, u):
    wash(c, col(0.25, 0.25, 0.4))
    for (x, h, n) in ((640, 260, '1'), (360, 180, '2'), (920, 130, '3')):
        c.poly([(x - 130, 720 - h), (x + 130, 720 - h), (x + 130, 720), (x - 130, 720)], fill=col(0.9, 0.9, 0.92), line=INK,
               lw=5)
        text(c, n, x, 720 - h / 2, 90, INK)
        penguin(c, x, 720 - h, 180, -1 if x > 640 else 1, arms=(170, 30), beak=talk(t) if n == '1' else 0.2, eye='smug')
    c.glow(640, 200, 300, YELLOW, 0.4)
    for i in range(20):
        ph = (u * 2 + i * 0.07) % 1
        c.poly(E((i * 97) % 1280, ph * 720, 8, 4, i * 40), fill=[RED, YELLOW, GREEN, WHITE][i % 4])
    text(c, 'BEST OF THE BEST OF THE BESTEST', 640, 60, 38, YELLOW)


def s_sunday(c, t, u):
    """Kanye West, dressed in his Sunday best, gloves on, in the ring with him."""
    wash(c, col(0.2, 0.2, 0.25))
    c.poly([(80, 600), (1200, 600), (1200, 720), (80, 720)], fill=col(0.3, 0.45, 0.7), line=INK, lw=5)
    c.line([(80, 300), (80, 720)], WHITE, lw=14)
    c.line([(1200, 300), (1200, 720)], WHITE, lw=14)
    penguin(c, 360, 680, 330, 1, arms=(100 + 20 * math.sin(t * 12), 80), lean=8, beak=talk(t), eye='angry')
    churchgoer(c, 930, 700, 500, t)
    for y in (380, 450, 520):
        c.line([(80, y), (1200, y)], RED, lw=8)
    text(c, 'SUNDAY BEST', 640, 60, 44, YELLOW)
    if int(t * 3) % 2:
        text(c, 'DING DING', 360, 90, 56, YELLOW)


def s_spectacle(c, t, u):
    wash(c, col(0.95, 0.92, 0.85))
    r, front = pigeon(c, 560, 700, 460, 1, mood='shock', t=t)
    ex, ey = r.P(0.16, 1.11)
    k = sstep(0.0, 0.25, u)
    s = 60 + 110 * k
    for dx in (-s * 0.9, s * 0.9):
        c.poly(E(ex + dx, ey, s * 0.8, s * 0.7), fill=col(0.85, 0.93, 1.0), line=INK, lw=12, opacity=0.8)
    c.line([(ex - s * 0.1, ey), (ex + s * 0.1, ey)], INK, lw=12)
    if u > 0.5:
        c.poly([(860, 220), (1210, 180), (1230, 310), (880, 350)], None, RED, lw=12)
        text(c, 'NOT', 1045, 230, 56, RED, rot=7)
        text(c, 'ACCEPTABLE', 1050, 295, 44, RED, rot=7)


def s_rentafool(c, t, u):
    wash(c, SKY)
    c.poly([(0, 600), (1280, 600), (1280, 720), (0, 720)], fill=col(0.5, 0.5, 0.52), line=INK, lw=4)
    k = sstep(0.0, 0.45, u)
    vx = lerp(1500, 640, k)
    c.poly([(vx - 320, 300), (vx + 170, 300), (vx + 170, 600), (vx - 320, 600)], fill=WHITE, line=INK, lw=6)
    c.poly([(vx + 170, 390), (vx + 300, 390), (vx + 330, 480), (vx + 330, 600), (vx + 170, 600)], fill=RED, line=INK, lw=6)
    for x in (vx - 220, vx + 220):
        c.poly(E(x, 610, 50, 50), fill=INK)
    text(c, 'RENT-A-FOOL', vx - 75, 400, 50, RED)
    text(c, 'we deliver', vx - 75, 470, 30, INK)
    if u > 0.5:
        # unloaded: the fool, jester's hat and all, popping out of a delivery box
        pop = sstep(0.5, 0.6, u)
        r, _ = pigeon(c, 230, 760 - 150 * pop, 260, 1, arms=(115, 165), mood='grin', t=t)
        for i, (du, dv, colr) in enumerate(((-0.28, 1.28, RED), (0.12, 1.5, YELLOW), (0.45, 1.3, GREEN))):
            c.poly(r.pts([(-0.04, 1.18), (du, dv), (0.28, 1.2)]), fill=colr, line=INK, lw=r.lw())
            c.poly(r.E(du, dv, 0.04, 0.04), fill=YELLOW, line=INK, lw=r.lw(0.6))
        c.poly([(90, 520), (370, 520), (370, 720), (90, 720)], fill=col(0.8, 0.65, 0.45), line=INK, lw=6)
        c.line([(90, 520), (40, 470)], INK, lw=5)
        c.line([(370, 520), (420, 470)], INK, lw=5)
        c.poly([(90, 520), (40, 470), (40, 500), (90, 550)], fill=col(0.7, 0.55, 0.38), line=INK, lw=4)
        c.poly([(370, 520), (420, 470), (420, 500), (370, 550)], fill=col(0.7, 0.55, 0.38), line=INK, lw=4)
        text(c, 'FRAGILE', 230, 620, 34, RED, rot=-4)
    # the crowd birds who ordered him, holding tools
    bird(c, 1150, 720, 150, 'parrot', 'laugh', t, -1)
    c.line([(1110, 560), (1060, 480)], GREY, lw=10)
    c.poly([(1040, 470), (1080, 460), (1085, 490), (1045, 500)], fill=GREY, line=INK, lw=3)


def s_miracles(c, t, u):
    wash(c, col(0.98, 0.94, 0.8))
    c.glow(640, 350, 360, YELLOW, 0.3)
    c.poly([(470, 180), (810, 180), (840, 640), (440, 640)], fill=col(0.88, 0.95, 1.0), line=INK, lw=8, opacity=0.9)
    c.poly([(500, 140), (780, 140), (780, 185), (500, 185)], fill=WOOD, line=INK, lw=5)
    text(c, 'MIRACLES', 640, 300, 56, INK)
    left = 1 - sstep(0.0, 0.7, u)
    for i in range(int(12 * left)):
        c.poly(E(520 + (i * 53) % 240, 600 - (i // 4) * 40, 26, 10), None, YELLOW, lw=6)
    r, front = pigeon(c, 1050, 700, 330, -1, arms=(150, 150), mood='shock', t=t)
    if u > 0.7:
        text(c, 'EMPTY', 640, 520, 60, RED, rot=-10)


CUTAWAYS = {
    'lullaby': s_lullaby, 'nullified': s_nullified, 'supervision': s_supervision, 'permission': s_permission,
    'dish': s_dish, 'scrub': s_scrub, 'surgery': s_surgery, 'reporter': s_reporter, 'waxwork': s_waxwork,
    'vanity': s_vanity, 'yeti': s_yeti, 'weak': s_weak, 'vomit': s_vomit, 'lost': s_lost, 'eagle': s_eagle,
    'defiled': s_defiled, 'chin': s_chin, 'yarn': s_yarn, 'noggin': s_noggin, 'corn': s_corn, 'pillow': s_pillow,
    'pipe': s_pipe, 'innate': s_innate, 'mistakes': s_mistakes, 'wait': s_wait, 'firesale': s_firesale,
    'crake': s_crake, 'crap': s_crap, 'blackeye': s_blackeye, 'factory': s_factory, 'practice': s_practice,
    'expectations': s_expectations, 'integrity': s_integrity, 'dinner': s_dinner, 'podium': s_podium,
    'sunday': s_sunday, 'veal': s_veal, 'snap': s_snap, 'keepreal': s_keepreal, 'spectacle': s_spectacle, 'rentafool': s_rentafool, 'miracles': s_miracles,
}


def render(d):
    t = d / FPS
    c = Sketch(d)
    a, b, name = shot_at(t)
    u = clamp01((t - a) / max(0.1, b - a))
    if name in CUTAWAYS:
        # a quick snap back to the penguin mid-delivery on long cutaways, then back to the picture
        if b - a > 4.5 and 0.42 < u < 0.52 and name not in ('crap', 'keepreal'):
            stage_cam(c, t, 'stage', 1.2, 1.3)
            c.cam = (1.6, -penguin_x(t) * 1.6 + 640, -470 * 1.6 + 360)
            stage(c, t, 'stage')
        else:
            CUTAWAYS[name](c, t, u)
    else:
        stage_cam(c, t, name, a, b)
        stage(c, t, name)
    return overlay(c.result(), t)


_FONT_CACHE = {}


def _font(size):
    if size not in _FONT_CACHE:
        _FONT_CACHE[size] = ImageFont.truetype(FONT, size)
    return _FONT_CACHE[size]


def overlay(frame, t):
    """Subtitles in white along the bottom, and a big red UNINTELLIGIBLE flash when nobody can tell."""
    im = Image.fromarray(frame)
    dr = ImageDraw.Draw(im)
    flash = next(((a, b) for a, b in UNINTELLIGIBLE if a <= t < b), None)
    if flash:
        k = int((t - flash[0]) * FPS)
        if k % 3 != 2:  # on, on, off: a flashing sign
            size = 118 if k % 2 else 126
            lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
            ImageDraw.Draw(lay).text((W / 2, H / 2), 'UNINTELLIGIBLE', font=_font(size), fill=(220, 20, 20, 255),
                                     anchor='mm', stroke_width=7, stroke_fill=(255, 255, 255, 255))
            lay = lay.rotate(-4 if k % 2 else 3, resample=Image.BICUBIC, center=(W / 2, H / 2))
            im.paste(lay, (0, 0), lay)
            dr = ImageDraw.Draw(im)
    else:
        for a, b, txt in SUBS:
            if a <= t < b:
                rows, cur = [], ''
                for w in txt.split():  # wrap long lines onto two or three rows
                    if cur and len(cur) + 1 + len(w) > 46:
                        rows.append(cur)
                        cur = w
                    else:
                        cur = (cur + ' ' + w).strip()
                rows.append(cur)
                for i, row in enumerate(rows):
                    dr.text((W / 2, H - 30 - 42 * (len(rows) - 1 - i)), row, font=_font(34), fill=(255, 255, 255),
                            anchor='mm', stroke_width=4, stroke_fill=(0, 0, 0))
                break
    return np.asarray(im)


def make_audio(path):
    import subprocess
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i',
                    os.path.join(HERE, 'audio', 'rap-battle.m4a'), '-t', str(DUR), '-af',
                    f'afade=t=out:st={DUR - 1.5}:d=1.5', path], check=True)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for ts in sys.argv[3:]:
            Image.fromarray(render(int(round(float(ts) * FPS)))).save(os.path.join(out, f'rap_{float(ts):06.2f}s.png'))
            print('saved', ts)
    elif mode == 'render':
        render_video(sys.argv[2], render, int(DUR * FPS), make_audio,
                     crf=int(sys.argv[3]) if len(sys.argv) > 3 else 32, size=(W, H))
