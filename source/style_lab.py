#!/usr/bin/env python3
"""style_lab: a test bench for the question "why do the Satire-style films look AI generated, and what would fix it?"

It never changes a film or source/satire_style.py. It only reads the films' own stills and draws test pictures.
All pictures go to review/ai-tells/ (kept off GitHub by .gitignore).

  python3 source/style_lab.py gather          the sample stills, made with each film's own stills/cast commands
  python3 source/style_lab.py sample          sheet 1: the numbered contact sheet of 20 tiles from six films
  python3 source/style_lab.py zoom            close crops of details sheet 1 is too small to show
  python3 source/style_lab.py options         sheet 2: the same three tiles in today's look and in each option
  python3 source/style_lab.py styleframe      Cry Minister's opening redesigned (Filmcow / South Park), faces kept
  python3 source/style_lab.py clip            Hope Again, 11.5 s, today then with the proposal, as a video
  python3 source/style_lab.py example         Hope Again, four shots, today and with the proposal
"""
import math
import os
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from satire_style import rough  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REVIEW = os.path.join(ROOT, 'review', 'ai-tells')
RAW = os.path.join(REVIEW, 'raw')
SANS = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
PAPER = (240, 236, 228)

# ------------------------------------------------------------------------------------------------ 1. the sample

STILLS = [  # (folder, command): each film's own stills or cast command; times are seconds into the film
    ('cm', ['cryminister.py', 'stills', '{out}', '1.5', '6.0', '12.0', '17.0', '21.0', '25.0', '40.0', '56.0']),
    ('cm', ['cryminister.py', 'cast', '{out}/cast.jpg']),
    ('park', ['thepark.py', 'stills', '{out}', '2.0', '6.0']),
    ('park', ['thepark.py', 'cast', '{out}/cast.jpg']),
    ('mos', ['mossad.py', 'stills', '{out}', '1.5', '9.5', '15.0']),
    ('pat', ['patriots2.py', 'stills', '{out}', '2.0', '12.0', '20.0', '45.0']),
    ('hope', ['burnham.py', 'stills', '{out}', '1', '2', '10']),
]


def gather():
    for folder, cmd in STILLS:
        out = os.path.join(RAW, folder)
        os.makedirs(out, exist_ok=True)
        subprocess.run([sys.executable, os.path.join(HERE, cmd[0])] + [c.format(out=out) for c in cmd[1:]], check=True)
    # Russiadent Evil's stills command first runs its sound checks, which stop it (a sound fault, nothing to do with
    # the pictures), so its frames are drawn here with the film's own frame_image and cast_sheet, unchanged.
    sys.path.insert(0, HERE)
    import russiadent as R
    out = os.path.join(RAW, 'rus')
    os.makedirs(out, exist_ok=True)
    R.B.SS = 1
    for t in ('3.0', '14.5', '21.5'):
        R.frame_image(float(t)).convert('RGB').save(os.path.join(out, f't{t}.jpg'), quality=88)
    R.cast_sheet(os.path.join(out, 'cast.jpg'))


TILES = [  # (file in review/ai-tells/raw, label)
    ('cm/1.5.jpg', 'Cry Minister: Andy on the high street'),
    ('cm/6.0.jpg', 'Cry Minister: shoppers, pub, ZapBets'),
    ('cm/17.0.jpg', 'Cry Minister: the big wolf'),
    ('cm/21.0.jpg', 'Cry Minister: the alley, wolf net'),
    ('cm/25.0.jpg', 'Cry Minister: the old lady'),
    ('cm/40.0.jpg', 'Cry Minister: the wide'),
    ('cm/56.0.jpg', 'Cry Minister: close-up'),
    ('cm/cast.jpg', 'Cry Minister: cast sheet'),
    ('park/t2.0.jpg', 'The Park: the wide'),
    ('park/t6.0.jpg', 'The Park: the man, close'),
    ('park/cast.jpg', 'The Park: cast'),
    ('rus/t3.0.jpg', 'Russiadent Evil: opening'),
    ('rus/t14.5.jpg', 'Russiadent Evil: shot 2'),
    ('rus/cast.jpg', 'Russiadent Evil: cast'),
    ('mos/t1.5.jpg', 'Mossad: front'),
    ('mos/t9.5.jpg', 'Mossad: customer'),
    ('pat/t2.0.png', 'Patriots 2: opening'),
    ('pat/t20.0.png', 'Patriots 2: shot 3'),
    ('hope/shot1.png', 'Hope Again: the stage'),
    ('hope/shot2.png', 'Hope Again: the hall'),
]


def fit(im, w, h, bg=PAPER):
    """The whole picture shrunk into a w x h box, centred on paper."""
    im = im.convert('RGB')
    k = min(w / im.width, h / im.height)
    small = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
    box = Image.new('RGB', (w, h), bg)
    box.paste(small, ((w - small.width) // 2, (h - small.height) // 2))
    return box


def grid(items, out, cols, tw, th, title):
    """items: (picture, label). A numbered sheet, labels under each tile."""
    lab, gap, head = 54, 14, 70
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (tw + gap) + gap, head + rows * (th + lab + gap)), PAPER)
    d = ImageDraw.Draw(sheet)
    d.text((gap, 18), title, font=ImageFont.truetype(SANS, 34), fill=(20, 20, 20))
    f = ImageFont.truetype(SANS, 19)
    for i, (im, label) in enumerate(items):
        x, y = gap + (i % cols) * (tw + gap), head + (i // cols) * (th + lab + gap)
        sheet.paste(fit(im, tw, th), (x, y))
        d.rectangle([x, y, x + 46, y + 40], fill=(20, 20, 20))
        d.text((x + 23, y + 20), str(i + 1), font=ImageFont.truetype(SANS, 28), fill=(255, 255, 255), anchor='mm')
        words, line, lines = label.split(), '', []
        for w_ in words:
            if d.textlength(line + ' ' + w_, font=f) > tw and line:
                lines.append(line)
                line = w_
            else:
                line = (line + ' ' + w_).strip()
        lines.append(line)
        for k, ln in enumerate(lines[:2]):
            d.text((x, y + th + 6 + 23 * k), ln, font=f, fill=(30, 30, 30))
    sheet.save(out, quality=90)
    print(out, sheet.size)


def sample(out):
    items = []
    for fn, label in TILES:
        p = os.path.join(RAW, fn)
        if not os.path.exists(p):
            p = os.path.splitext(p)[0] + ('.png' if p.endswith('.jpg') else '.jpg')
        items.append((Image.open(p), label))
    grid(items, out, 5, 340, 604, 'Sheet 1: Satire-style sample, 20 tiles from six films')


ZOOMS = [  # (file, crop box in frame pixels, label): details a small tile can't show
    ('cm/56.0.jpg', (280, 380, 900, 1120), 'A. tile 7: Andy\'s face'),
    ('cm/25.0.jpg', (380, 560, 1080, 1700), 'B. tile 5: the old lady, Andy'),
    ('cm/21.0.jpg', (80, 560, 1000, 1560), 'C. tile 4: wolf net, brick alley'),
    ('cm/6.0.jpg', (0, 560, 900, 1400), 'D. tile 2: shoppers, feeding wolves'),
    ('cm/17.0.jpg', (0, 0, 1080, 1100), 'E. tile 3: poster lettering, wolf'),
    ('park/t2.0.jpg', (0, 280, 1080, 1300), 'F. tile 9: trees, sun, pigeons'),
    ('rus/cast.jpg', (0, 80, 1200, 1000), 'G. tile 14: the cast'),
    ('pat/t20.0.png', (0, 140, 1080, 820), 'H. tile 18: the lifeboat row'),
    ('hope/shot2.png', (0, 1150, 1080, 1920), 'I. tile 20: the audience'),
]


def zoom(out):
    items = [(Image.open(os.path.join(RAW, fn)).crop(box), label) for fn, box, label in ZOOMS]
    grid(items, out, 3, 580, 560, 'Zoom: details from sheet 1')


# ------------------------------------------------------------------------------------------------ 2. the options
# Each option is tried by swapping the shared drawing tools in memory while the lab draws its three test tiles, then
# putting them back. Nothing on disk changes: the films and source/satire_style.py stay exactly as they are.

import contextlib
import time


@contextlib.contextmanager
def swapped(pairs):
    """pairs: (module or class, name, new value). Restored afterwards, whatever happens."""
    old = [(o, n, getattr(o, n)) for o, n, _ in pairs]
    for o, n, v in pairs:
        setattr(o, n, v)
    try:
        yield
    finally:
        for o, n, v in reversed(old):
            setattr(o, n, v)


def _seed(pts):
    """A shape's own random seed, from where it is drawn (so the same drawing always gets the same line)."""
    a, b = pts[0]
    return hash((round(a, 1), round(b, 1), len(pts))) & 0xFFFFFFFF


def _resample(P, step):
    seg = np.hypot(*np.diff(P, axis=0).T)
    s = np.concatenate([[0], np.cumsum(seg)])
    if s[-1] < 1e-6:
        return P, s
    n = max(2, int(s[-1] / step) + 1)
    u = np.linspace(0, s[-1], n)
    return np.stack([np.interp(u, s, P[:, 0]), np.interp(u, s, P[:, 1])], 1), u


def _brush(d, P, width, rnd, col, taper=0.35):
    """One stroke of a brush pen: the width swells and thins along the stroke, the ends taper."""
    P, s = _resample(np.asarray(P, float), max(1.5, width * 0.6))
    L = s[-1] if s[-1] > 0 else 1.0
    k = np.zeros_like(s)
    for _ in range(3):                                      # three slow swells of pressure, each stroke its own
        k += rnd.uniform(0.3, 1.0) * np.sin(2 * math.pi * rnd.uniform(0.4, 2.2) * s / L + rnd.uniform(0, 6.3))
    k = (k - k.min()) / (np.ptp(k) or 1.0)
    w = width * (0.7 + 0.6 * k)
    end = max(width * 2.5, 1.0)
    w *= np.clip(np.minimum(s, L - s) / end, taper, 1.0)
    for i in range(len(P) - 1):
        d.line([tuple(P[i]), tuple(P[i + 1])], fill=col, width=max(1, int(round(w[i]))))
        r = w[i] / 2
        if r >= 1.0:
            d.ellipse([P[i][0] - r, P[i][1] - r, P[i][0] + r, P[i][1] + r], fill=col)


def ink(d, pts, width, closed, seed, col):
    """A line drawn by hand: varying thickness, tapering ends; boxes drawn edge by edge so corners overshoot; round
    shapes closed with a small overlap (or now and then a small gap) where the pen started."""
    rnd = random.Random(seed)
    P = np.asarray(pts, float)
    if len(P) < 2:
        return
    if not closed:
        _brush(d, P, width, rnd, col)
        return
    if len(P) <= 6:                                         # a box or a wedge: one stroke per edge, past the corners
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            n = math.hypot(*(b - a)) or 1.0
            u = (b - a) / n
            _brush(d, [a - u * rnd.uniform(0, 1.6) * width, b + u * rnd.uniform(0, 1.6) * width], width, rnd, col, 0.6)
        return
    P = np.roll(P, -rnd.randrange(len(P)), axis=0)
    loop = np.vstack([P, P[:1]])
    _, s = _resample(loop, 1.0)
    extra = rnd.uniform(0.03, 0.08) if rnd.random() > 0.15 else -rnd.uniform(0.02, 0.04)
    if extra > 0:                                           # run on past the start
        m = max(1, int(len(P) * extra))
        loop = np.vstack([loop, P[1:m + 1]])
    else:                                                   # stop just short: a small gap
        loop = loop[:max(2, int(len(loop) * (1 + extra)))]
    _brush(d, loop, width, rnd, col)


def _flat_soft(orig):
    def soft(img, cam, pts, colr, alpha, blur=6):
        return orig(img, cam, pts, colr, alpha, 0)          # the same shadow shape, hard-edged: cel shading, no airbrush
    return soft


def _banded_gradient(B):
    def gradient(img, cam, box, c_mid, c_edge, centre, radius, squash=1.0, dim=1.0):
        x0, y0 = cam.P(box[0], box[1])
        x1, y1 = cam.P(box[2], box[3])
        x0, y0, x1, y1 = [int(round(v)) for v in (x0, y0, x1, y1)]
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(img.width, x1), min(img.height, y1)
        if x1 <= x0 or y1 <= y0:
            return
        X, Y = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1))
        CX, CY = cam.P(*centre)
        R = cam.S(radius)
        d = np.sqrt(((X - CX) / R) ** 2 + ((Y - CY) / (R * squash)) ** 2)
        k = np.round(np.clip(d, 0, 1) ** 1.3 * 2) / 2      # three flat bands of paint instead of a smooth airbrush
        k = k[..., None]
        a = (np.array(c_mid) * (1 - k) + np.array(c_edge) * k) * dim
        img.alpha_composite(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGB').convert('RGBA'), (x0, y0))
    return gradient


def opt_ink(CM):
    """Option 1: hand-inked line, flat colour only."""
    import ed
    from satire_style import Ctx
    B = CM.B
    INK_ = B.INK

    def pen_poly(self, pts, fill, line=INK_, lw=4):
        q = [self.cam.P(*p) for p in pts]
        if fill is not None:
            self.d.polygon(q, fill=fill)
        if line:
            ink(self.d, q, self.w(lw) * 1.15, True, _seed(pts), line)

    def pen_line(self, pts, colr=INK_, lw=4):
        ink(self.d, [self.cam.P(*p) for p in pts], self.w(lw) * 1.15, False, _seed(pts), colr)

    def ctx_poly(self, pts, fill, line=True):
        P = [self.c.p(*q) for q in pts]
        self.d.polygon(P, fill=fill)
        if line:
            ink(self.d, P, self.c.w(self.ol) * 1.1, True, _seed(pts), CM.OUT)

    def ctx_ell(self, x, y, rx, ry, fill, line=True):
        self.rell(x, y, rx, ry, 0.0, fill, line)

    pairs = [(B.Pen, 'poly', pen_poly), (B.Pen, 'line', pen_line), (Ctx, 'poly', ctx_poly), (Ctx, 'ell', ctx_ell),
             (B, 'gradient', _banded_gradient(B))]
    def glow(img, cam, x, y, r, colr, alpha):
        return                                              # no glows at all: flat colour only
    import types
    from PIL import ImageFilter as IF
    sharp = types.SimpleNamespace(GaussianBlur=lambda r: IF.GaussianBlur(0))   # no soft-focus blur anywhere
    for m in list(sys.modules.values()):
        if getattr(m, 'ImageFilter', None) is IF and m.__name__ in ('burnham', 'cryminister'):
            pairs.append((m, 'ImageFilter', sharp))
        if getattr(m, 'soft', None) is ed.soft:
            pairs.append((m, 'soft', _flat_soft(ed.soft)))
        if getattr(m, 'glow', None) is ed.glow:
            pairs.append((m, 'glow', glow))
    return swapped(pairs)


# Option 2: printed on paper with a short list of inks chosen for the film -----------------------------------------

def _noise(h, w, rnd, sizes=((6, 10), (30, 54), (160, 280)), weights=(0.5, 0.3, 0.2)):
    out = np.zeros((h, w))
    for (a, b), k in zip(sizes, weights):
        small = Image.fromarray((rnd.random((a, b)) * 255).astype(np.uint8))
        out += k * np.asarray(small.resize((w, h), Image.BICUBIC), float) / 255
    return out


def film_inks(im, n=13, key=(1.0, 0.96, 0.88), desat=0.22):
    """A film's ink list: its colours under one light (a warm, overcast cast), pulled a little away from screen-bright
    defaults, cut down to n inks plus the black line."""
    a = np.asarray(im.convert('RGB'), float)
    a = a * (1 - desat) + a.mean(-1, keepdims=True) * desat
    a = np.clip(a * np.array(key), 0, 255).astype(np.uint8)
    q = Image.fromarray(a).quantize(n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:3 * n]
    return pal + [24, 20, 22]


def print_look(im, inks, seed=1, key=(1.0, 0.96, 0.88), desat=0.22):
    """The frame printed in the film's inks on off-white paper: one light over everything, a slight misregistration
    between the colour and the black line, and paper grain that never repeats."""
    rnd = np.random.default_rng(seed)
    a = np.asarray(im.convert('RGB'), float)
    line = a.max(-1) < 60                                   # the black line, printed separately
    a = a * (1 - desat) + a.mean(-1, keepdims=True) * desat
    a = np.clip(a * np.array(key), 0, 255).astype(np.uint8)
    pimg = Image.new('P', (1, 1))
    pimg.putpalette(inks + [0] * (768 - len(inks)))
    q = np.asarray(Image.fromarray(a).quantize(palette=pimg, dither=Image.Dither.NONE).convert('RGB'), float)
    q = np.roll(q, (2, 3), axis=(0, 1))                     # the colour plate lands a hair off the line plate
    q[line] = (24, 20, 22)
    h, w = line.shape
    grain = _noise(h, w, rnd)
    q *= (0.955 + 0.06 * grain)[..., None]                  # paper takes the ink unevenly
    speck = rnd.random((h, w)) < 0.004
    q[speck] = q[speck] * 0.8 + 255 * 0.2                   # tiny voids where the ink missed
    return Image.fromarray(np.clip(q, 0, 255).astype(np.uint8))


# Option 3: everybody a different shape -----------------------------------------------------------------------------

IS_LEAD = [lambda sp: sp.get('name') == 'Andy']           # the film's lead: keeps his caricature
TWOS = [False]                                              # background people held two frames each (6 drawings a second)


def _twos(t):
    return math.floor(t * 6 + 1e-6) / 6 if TWOS[0] else t


def _params(sp):
    name = str(sp.get('name'))
    r = random.Random(name + str(sp.get('skin')) + str(sp.get('jacket')) + str(sp.get('hair')))
    if IS_LEAD[0](sp):                                      # the lead keeps his caricature, just less of a template
        head = dict(sx=0.92, sy=1.08, jaw=-0.16, brow=0.08, fsc=0.86, fdy=8, asym=3.5, tilt=0.035)
        body = dict(kx=0.94, ky=1.0, kl=1.04, lean=0.02)
    else:
        head = dict(sx=r.uniform(0.84, 1.2), sy=r.uniform(0.88, 1.16), jaw=r.uniform(-0.3, 0.32),
                    brow=r.uniform(-0.18, 0.18), fsc=r.uniform(0.74, 1.18), fdy=r.uniform(-14, 18),
                    asym=r.uniform(2, 5) * r.choice((-1, 1)), tilt=r.uniform(-0.07, 0.07))
        body = dict(kx=r.uniform(0.8, 1.32), ky=r.uniform(0.88, 1.1), kl=r.uniform(0.82, 1.14), lean=r.uniform(-0.05, 0.05))
    return head, body


def _sm(e0, e1, x):
    u = min(1.0, max(0.0, (x - e0) / (e1 - e0)))
    return u * u * (3 - 2 * u)


def _head_warp(hp, hx, hy, hw, hh):
    ca, sa = math.cos(hp['tilt']), math.sin(hp['tilt'])

    def f(x, y):
        dx, dy = x - hx, y - hy
        v = dy / hh
        X = dx * hp['sx'] * (1 + hp['jaw'] * max(0.0, v) + hp['brow'] * max(0.0, -v))
        Y = dy * hp['sy']
        fy = 20 * hp['sy']                                  # the features: closer or wider set, higher or lower, uneven
        wgt = max(0.0, 1 - math.hypot(X / (hw * 0.8), (Y - fy) / (hh * 0.85))) ** 1.5
        X *= 1 + (hp['fsc'] - 1) * wgt
        Y += hp['fdy'] * wgt + hp['asym'] * wgt * math.tanh(X / 12)
        Yc = Y - hh                                         # the whole head tipped a little, about the chin
        return hx + X * ca - Yc * sa, hy + hh + X * sa + Yc * ca
    return f


def opt_variety(CM):
    """Option 3: every person a different build, head shape, feature placement and posture."""
    B = CM.B
    cur = {}
    orig_person, orig_head, orig_hair_back, OrigLocal = B.person, B.head, B.hair_back, B.Local

    class WarpPen(B.Pen):
        def __init__(self, base, f):
            self.img, self.cam, self.d, self.f = base.img, base.cam, base.d, f

        def poly(self, pts, fill, line=B.INK, lw=4):
            B.Pen.poly(self, [self.f(*q) for q in pts], fill, line, lw)

        def line(self, pts, colr=B.INK, lw=4):
            B.Pen.line(self, [self.f(*q) for q in pts], colr, lw)

    class Local(OrigLocal):
        def P(self, x, y):
            if cur.get('crowd'):                            # a head in a crowd seen from behind: its own size and spot
                r = random.Random(hash((round(self.ox), round(self.oy))))
                kx, ky, dx = r.uniform(0.8, 1.25), r.uniform(0.85, 1.2), r.uniform(-45, 45)
                return OrigLocal.P(self, x * kx + dx, y * ky if y < 0 else y)
            bp = cur.get('body')
            if bp:
                g = _sm(-80, 40, y)                         # below the neck only; the head has its own shape
                kx = 1 + (bp['kx'] - 1) * g
                yy = y if y < 0 else (y * bp['ky'] if y < 440 else 440 * bp['ky'] + (y - 440) * bp['kl'])
                x, y = x * kx + bp['lean'] * (930 - yy), yy
            return OrigLocal.P(self, x, y)

    def warp_for(sp, hx, hy):
        hp = cur.get('head')
        return _head_warp(hp, hx, hy, sp.get('hw', 72), sp.get('hh', 88)) if hp else None

    def head(img, p, sp, t, hx, hy):
        f = warp_for(sp, hx, hy)
        return orig_head(img, WarpPen(p, f) if f else p, sp, t, hx, hy)

    def hair_back(p, sp, hx, hy, hw, hh):
        f = warp_for(sp, hx, hy)
        return orig_hair_back(WarpPen(p, f) if f else p, sp, hx, hy, hw, hh)

    def person(img, cam, x, y, s, sp, t=0.0, flip=1):
        cur['head'], cur['body'] = _params(sp)
        cur['sp'] = sp
        if not IS_LEAD[0](sp):
            t = _twos(t)
        try:
            return orig_person(img, cam, x, y, s, sp, t, flip)
        finally:
            cur.clear()

    pairs = [(B, 'person', person), (B, 'head', head), (B, 'hair_back', hair_back), (B, 'Local', Local)]
    if hasattr(B, 'heads_from_behind'):
        orig_heads = B.heads_from_behind

        def heads_from_behind(*a, **k):
            if 't' in k:
                k['t'] = _twos(k['t'])
            elif len(a) > 6:
                a = a[:6] + (_twos(a[6]),) + a[7:]
            cur['crowd'] = True
            try:
                return orig_heads(*a, **k)
            finally:
                cur.clear()
        pairs.append((B, 'heads_from_behind', heads_from_behind))
    return swapped(pairs)


# Option 4: a world made and worn by hand ---------------------------------------------------------------------------

def hand_letters(s, font, px, fill, seed, stroke=0, stroke_fill=(24, 20, 22)):
    """Lettering painted by a sign-writer: each letter its own size, lean and height, the spacing uneven, the last
    letters squeezed where the painter ran short of room, and the edges wobbling slightly as a brush does."""
    rnd = random.Random(seed)
    sizes = [px * rnd.uniform(0.93, 1.07) for _ in s]
    n = len(s)
    squeeze = [0.86 if n > 6 and i >= n - 2 else 1.0 for i in range(n)]
    fonts = [ImageFont.truetype(font, max(4, int(z))) for z in sizes]
    adv = [f.getlength(c) * q + px * rnd.uniform(-0.02, 0.05) for f, c, q in zip(fonts, s, squeeze)]
    W_, H_ = int(sum(adv) + px * 0.8), int(px * 1.7)
    lay = Image.new('RGBA', (W_, H_), (0, 0, 0, 0))
    x = px * 0.4
    sw = int(stroke * px / 40)
    for c, f, a, q, z in zip(s, fonts, adv, squeeze, sizes):
        if c != ' ':
            g = Image.new('RGBA', (int(z * 1.6), int(z * 1.8)), (0, 0, 0, 0))
            ImageDraw.Draw(g).text((g.width / 2, g.height / 2), c, font=f, anchor='mm', fill=fill, stroke_width=sw,
                                   stroke_fill=stroke_fill)
            if q != 1.0:
                g = g.resize((max(1, int(g.width * q)), g.height), Image.LANCZOS)
            g = g.rotate(rnd.uniform(-3.5, 3.5), Image.BICUBIC)
            lay.alpha_composite(g, (int(x + a / 2 - g.width / 2), int(H_ / 2 - g.height / 2 + rnd.uniform(-0.04, 0.04) * px)))
        x += a
    # the brush edge: shift every pixel by a slow, uneven wobble (a few percent of the letter height)
    A = np.asarray(lay)
    h, w = A.shape[:2]
    nr = np.random.default_rng(seed)
    dx = (_noise(h, w, nr, ((3, 5), (8, 14), (20, 34)), (0.4, 0.4, 0.2)) - 0.5) * px * 0.05
    dy = (_noise(h, w, nr, ((3, 5), (8, 14), (20, 34)), (0.4, 0.4, 0.2)) - 0.5) * px * 0.05
    Y, X = np.mgrid[0:h, 0:w]
    xs = np.clip((X + dx).astype(int), 0, w - 1)
    ys = np.clip((Y + dy).astype(int), 0, h - 1)
    return Image.fromarray(A[ys, xs])


def opt_handmade(CM):
    """Option 4: hand-lettered signs, boxes that lean like hand-cut card, grime and litter."""
    B = CM.B
    orig_shop, orig_drunk, orig_text = CM.shop, CM.drunk, B.text

    def sign_text(img, cam, x, y, s, size, fill, font=B.ANTON, stroke=0, angle=0.0):
        px = cam.S(size)
        if px < 5:
            return
        lay = hand_letters(s, font, px, fill, hash((s, round(x), round(y))) & 0xFFFF, stroke)
        r = random.Random(s)
        ang = angle + math.radians(r.uniform(-1.2, 1.2))
        lay = lay.rotate(math.degrees(ang), Image.BICUBIC, expand=True)
        X0, Y0 = cam.P(x + r.uniform(-0.03, 0.03) * size * len(s) * 0.4, y)     # never quite centred
        img.alpha_composite(lay, (int(X0 - lay.width / 2), int(Y0 - lay.height / 2)))

    def text(img, cam, x, y, s, size, fill, font=B.ANTON, anchor='la', widen=1.0, stroke=0, stroke_fill=B.INK):
        px = cam.S(size)
        lay = hand_letters(s, font, px, fill, hash(s) & 0xFFFF, stroke, stroke_fill)
        if widen != 1.0:
            lay = lay.resize((int(lay.width * widen), lay.height), Image.LANCZOS)
        X, Y = cam.P(x, y)
        X -= px * 0.4
        Y -= px * 0.25
        if anchor == 'ma':
            X -= lay.width / 2
        img.alpha_composite(lay, (int(X), int(Y)))
        return lay.width / (cam.z * B.SS), lay.height / (cam.z * B.SS)

    def box(X, x0, y0, x1, y1, fill, sd=0, amt=6, line=True):
        r = random.Random(sd * 7 + 1)
        lean = r.uniform(-1, 1) * r.choice((0.0, 0.004, 0.012))           # most stand true, some lean, a few a lot
        sag = r.uniform(-1, 1) * r.choice((0.0, 0.006, 0.015))
        w_, h_ = x1 - x0, y1 - y0
        pts = [(x0 + lean * h_, y0), (x1 + lean * h_, y0 + sag * w_), (x1, y1 + sag * w_ * 0.4), (x0, y1)]
        pts = [(px + r.uniform(-amt, amt) * 0.4, py + r.uniform(-amt, amt) * 0.4) for px, py in pts]
        X.poly(pts, fill, line=line)

    def shop(img, cam, x0, x1, kind_):
        orig_shop(img, cam, x0, x1, kind_)
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        X = CM.X_(lay, cam)
        r = random.Random(int(x0))
        base, top = CM.BASE, CM.BASE - CM.STOREY
        grime = (54, 44, 34, 46)
        xs = np.linspace(x0, x1, 26)                         # dirt splashed up the bottom of the shop front
        edge = [(x, base - 70 - r.uniform(0, 1) ** 2 * 190) for x in xs]
        X.poly(edge + [(x1, base), (x0, base)], grime, line=False)
        for _ in range(r.randint(3, 6)):                     # rain streaks down from the fascia and the sills
            sx = r.uniform(x0 + 80, x1 - 80)
            sy = r.choice((top + 420, top - 1300, top - 600))
            ln = r.uniform(180, 700)
            wd = r.uniform(12, 34)
            X.poly([(sx - wd, sy), (sx + wd, sy), (sx + wd * 0.3, sy + ln), (sx - wd * 0.2, sy + ln * 0.9)], (60, 50, 40, 40), line=False)
        img.alpha_composite(lay)

    def drunk(X, t):
        r = random.Random(4)
        for _ in range(60):                                  # chewing gum, worn grey spots
            gx, gy = r.uniform(-6800, 6000), CM.BASE + r.uniform(60, 1400)
            g = r.uniform(10, 26)
            X.ell(gx, gy, g * 1.3, g * 0.7, (156, 154, 148), line=False)
        for k in range(7):                                   # litter: a crisp packet, a can, receipts, a cup
            lx, ly = r.uniform(-6000, 5200), CM.BASE + r.uniform(80, 700)
            col = [(220, 40, 50), (60, 120, 200), (236, 234, 226), (240, 200, 60), (230, 230, 230)][k % 5]
            s = r.uniform(30, 60)
            X.poly(rough([(lx - s, ly - s * 0.5), (lx + s, ly - s * 0.6), (lx + s * 0.8, ly + s * 0.4), (lx - s * 0.9, ly + s * 0.5)],
                         s * 0.25, k), col)
        return orig_drunk(X, t)

    return swapped([(CM, 'sign_text', sign_text), (B, 'text', text), (CM, 'box', box), (CM, 'shop', shop),
                    (CM, 'drunk', drunk)])


# The three test tiles -----------------------------------------------------------------------------------------------

ANDY_T, STREET_T = 28.5, 40.0
ANDY_BOX, STREET_BOX, CROWD_BOX = (0, 150, 1080, 1630), (330, 720, 1030, 1680), (0, 380, 1080, 1860)


def _film():
    sys.path.insert(0, HERE)
    import cryminister as CM
    return CM


def _full(img, B):
    return img.convert('RGB').resize((1080, 1920), Image.LANCZOS)


def crowd(CM):
    """Five conference-goers in front of the conference backdrop (the people library behind every crowd and
    background person in the series), standing as the films' cast sheets stand them."""
    B, F = CM.B, CM.F
    img = B.canvas((140, 10, 40))
    cam = B.Cam(1.0)
    B.backdrop(img, cam)
    rng = np.random.default_rng(5)
    s, floor = 0.62, 1600
    for i in range(5):
        sp = B.attendee(rng)
        sp.update(full=True, pose='custom', name=f'delegate {i + 1}')
        sp['arms'] = F.Rig(sp).pose('sides')
        _, bp = _params(sp)
        legs = 440 * bp['ky'] + 490 * bp['kl'] if CROWD['vary'] else 930
        x = 130 + 205 * i + (CROWD['dx'][i] if CROWD['vary'] else 0)
        if CROWD['vary'] and i in (1, 3):                    # not everyone stands to attention
            sp['arms'] = F.Rig(sp).pose('hips' if i == 1 else 'clasped')
        B.person(img, cam, x, floor - legs * s, s, sp, 0.3)
    return img


CROWD = dict(vary=False, dx=[-30, 20, 60, -10, 15])


def tiles(CM, post=None):
    B = CM.B
    B.SS = 2
    a = _full(CM.picture(ANDY_T), B)
    b = _full(crowd(CM), B)
    B.SS = 4                                                 # the street in close detail: shop fronts, signs, pavement
    c = CM.picture(STREET_T).convert('RGB').crop(tuple(v * 4 for v in STREET_BOX))
    c = c.resize((c.width // 2, c.height // 2), Image.LANCZOS)
    B.SS = 2
    if post:
        a, c, b = post(a, c, b)
    return [a.crop(ANDY_BOX), b.crop(CROWD_BOX), c]


def _print_post(a, c, b):
    both = Image.new('RGB', (a.width + c.width, max(a.height, c.height)))
    both.paste(a, (0, 0))
    both.paste(c, (a.width, 0))
    inks = film_inks(both, 16)                               # one ink list for the whole of Cry Minister
    return print_look(a, inks, 1), print_look(c, inks, 2), print_look(b, film_inks(b), 3)


COLUMNS = [  # (label, how)
    ('Today', None),
    ('1. Hand-inked line, flat colour', 'ink'),
    ('2. Printed: film inks, paper', 'print'),
    ('3. Everyone a different shape', 'variety'),
    ('4. Hand-made, worn world', 'handmade'),
    ('Recommended: 1 + 3 + 4', 'combo'),
]


def column(CM, how):
    t0 = time.time()
    if how is None:
        out = tiles(CM)
    elif how == 'ink':
        with opt_ink(CM):
            out = tiles(CM)
    elif how == 'print':
        out = tiles(CM, _print_post)
    elif how == 'variety':
        CROWD['vary'] = True
        with opt_variety(CM):
            out = tiles(CM)
        CROWD['vary'] = False
    elif how == 'handmade':
        with opt_handmade(CM):
            out = tiles(CM)
    elif how == 'combo':
        CROWD['vary'] = True
        with opt_ink(CM), opt_variety(CM), opt_handmade(CM):
            out = tiles(CM)
        CROWD['vary'] = False
    secs = time.time() - t0
    print(f'{how}: {secs:.1f} s for the three tiles', flush=True)
    return out, secs


def options(out):
    CM = _film()
    cols = []
    for label, how in COLUMNS:
        imgs, secs = column(CM, how)
        cols.append((label, imgs, secs))
    base = cols[0][2]
    tw, th, lab, gap, head = 300, 412, 64, 12, 70
    rows = ['Main character', 'Background people', 'Location']
    left = 150
    sheet = Image.new('RGB', (left + len(cols) * (tw + gap) + gap, head + lab + 3 * (th + gap) + 10), PAPER)
    d = ImageDraw.Draw(sheet)
    d.text((gap, 16), 'Sheet 2: the same three tiles, today and in each option', font=ImageFont.truetype(SANS, 34),
           fill=(20, 20, 20))
    f, fs = ImageFont.truetype(SANS, 18), ImageFont.truetype(SANS, 15)
    for j, name in enumerate(rows):
        d.text((gap, head + lab + j * (th + gap) + th / 2), name.replace(' ', '\n', 1), font=f, fill=(30, 30, 30))
    for i, (label, imgs, secs) in enumerate(cols):
        x = left + gap + i * (tw + gap)
        words, line_, lines = label.split(), '', []
        for w_ in words:
            if d.textlength(line_ + ' ' + w_, font=f) > tw and line_:
                lines.append(line_)
                line_ = w_
            else:
                line_ = (line_ + ' ' + w_).strip()
        lines.append(line_)
        for k, ln in enumerate(lines[:2]):
            d.text((x, head + k * 22), ln, font=f, fill=(20, 20, 20))
        d.text((x, head + 46), f'drawing time x{secs / base:.1f}' if i else 'drawing time x1.0', font=fs, fill=(90, 80, 80))
        for j, im in enumerate(imgs):
            sheet.paste(fit(im, tw, th, (30, 30, 30)), (x, head + lab + j * (th + gap)))
    sheet.save(out, quality=90)
    print(out, sheet.size)


# ------------------------------------------------------------------------------------------------ 3. an example film

EXAMPLE_SHOTS = ['1', '2', '3', '10']                       # Hope Again: the stage, the hall, the front row, swords


def example(out):
    """Hope Again, four shots: as it was made (top row) and with the proposal (bottom row): hand-drawn line, no blur
    or glow, everyone a different shape. Drawn from the film's own shot list; the film itself is not changed."""
    import types
    sys.path.insert(0, HERE)
    import burnham as H
    film = types.SimpleNamespace(B=H, OUT=H.INK)
    IS_LEAD[0] = lambda sp: sp.get('jaw') == 'long' and sp.get('hh') == 96   # Burnham, and the king he becomes
    shots = {n: (name, fn) for n, name, _, fn in H.BOARD}
    today, new = [], []
    for n in EXAMPLE_SHOTS:
        name, fn = shots[n]
        today.append((H.finish(fn()), f'{n}. {name}: today'))
        with opt_ink(film), opt_variety(film):
            new.append((H.finish(fn()), f'{n}. {name}: proposed'))
        print('shot', n, flush=True)
    grid(today + new, out, 4, 380, 676, 'Hope Again: today (top) and the proposal (bottom)')


# ------------------------------------------------------------------------------------------------ 4. an example clip

CLIP = (9.5, 21.0)                                          # Hope Again: end of the speech, ovation, front row, knights


def _clip_init(proposed):
    global _BF
    from PIL import ImageFilter as IF

    class GaussianBlur(IF.GaussianBlur):                    # Hope Again passes NumPy numbers, which newer Pillow
        def __init__(self, radius=2):                       # rejects; plain numbers here (the film is not changed)
            super().__init__(radius if isinstance(radius, tuple) else float(radius))
    IF.GaussianBlur = GaussianBlur
    sys.path.insert(0, HERE)
    import burnham_film as BF
    import types
    BF.B.SS = 2
    _BF = BF
    if proposed:
        IS_LEAD[0] = lambda sp: sp.get('jaw') == 'long' and sp.get('hh') == 96
        TWOS[0] = True
        film = types.SimpleNamespace(B=BF.B, OUT=BF.B.INK)
        opt_ink(film).__enter__()                           # stays on in this helper process until it ends
        opt_variety(film).__enter__()


def _clip_frame(args):
    i, label = args
    img = _BF.frame_image(i).convert('RGB').resize((1080, 1920), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(SANS, 40)
    w = d.textlength(label, font=f)
    d.rounded_rectangle([540 - w / 2 - 24, 330, 540 + w / 2 + 24, 394], 14, fill=(255, 255, 255))
    d.text((540, 362), label, font=f, fill=(20, 20, 20), anchor='mm')
    return np.asarray(img).tobytes()


def clip(out):
    """The same stretch of Hope Again twice: as made (TODAY), then with the proposal (PROPOSED), with the film's sound."""
    from multiprocessing import Pool
    import imageio_ffmpeg
    fps = 12
    frames = range(int(CLIP[0] * fps), int(CLIP[1] * fps))
    src = os.path.join(ROOT, 'animations', 'king-in-the-north-vertical.mp4')
    a0, a1 = frames[0] / fps, (frames[-1] + 1) / fps
    ff = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                           '-s', '1080x1920', '-r', str(fps), '-i', '-', '-i', src, '-filter_complex',
                           f'[1:a]atrim={a0}:{a1},asetpts=PTS-STARTPTS,asplit[a][b];[a][b]concat=n=2:v=0:a=1[s]',
                           '-map', '0:v', '-map', '[s]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '23',
                           '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    t0 = time.time()
    for proposed, label in ((False, 'TODAY'), (True, 'PROPOSED')):
        with Pool(os.cpu_count(), initializer=_clip_init, initargs=(proposed,)) as pool:
            for k, buf in enumerate(pool.imap(_clip_frame, [(i, label) for i in frames], chunksize=2)):
                ff.stdin.write(buf)
                if k % 24 == 0:
                    print(label, k, '/', len(frames), f'{time.time() - t0:.0f} s', flush=True)
    ff.stdin.close()
    ff.wait()
    print(out, f'{os.path.getsize(out) / 1e6:.1f} MB', f'{time.time() - t0:.0f} s')


# ------------------------------------------------------------------------------------------------ 5. a style frame
# The look redesigned the Filmcow / South Park way: our faces exactly as they are, on small simple bodies; backgrounds
# of a few big flat shapes with no outline (only characters are outlined); little in the frame, each thing on purpose.

DESIGNS = {  # each person's own build (local units, the head is about 140 wide): torso half-width and height,
             # how much it widens to the hem, leg length, a belly, which way the arms hang
    'Andy': dict(tw=70, th=185, flare=1.1, legs=118, belly=0),
    'the old lady': dict(tw=62, th=165, flare=1.45, legs=52, belly=10),
    'the man': dict(tw=98, th=168, flare=1.18, legs=92, belly=34),
    'shopper': dict(tw=56, th=205, flare=1.02, legs=140, belly=0),
}


def tube(p, L, pts, w, col):
    """A stubby arm: a round-ended tube through the points, one outline all round (drawn as a black tube underneath)."""
    o = p.w(2.6) / L.S(1)
    for c, ww in (((24, 20, 22), w + 2 * o), (col, w)):
        for a, b in zip(pts, pts[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            n = math.hypot(dx, dy) or 1.0
            nx, ny = -dy / n * ww / 2, dx / n * ww / 2
            p.poly([(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)], c, None)
        for q in pts:
            p.ell(q[0], q[1], ww / 2, ww / 2, c, None)


def toon(img, cam, x, ground, k, sp, design, hands=None, t=0.0, phone=False):
    """One person in the new proportions, feet on `ground` at x, size k. Our own head and face, unchanged; no neck; a
    body of a few chunky shapes; circle hands. hands: {'L': (x, y), 'R': (x, y)} in the person's own units."""
    from ed import curve
    B = sys.modules['burnham']
    hw, hh = sp.get('hw', 72), sp.get('hh', 88)
    tw, th, fl, legs, belly = design['tw'], design['th'], design['flare'], design['legs'], design['belly']
    L = B.Local(cam, x, ground - (th + legs) * k, k)
    p = B.Pen(img, L)
    skin = sp['skin']
    out = sp.get('outfit', 'suit')
    coat = sp.get('dress') if out == 'dress' else sp.get('jacket', B.NAVY)
    hy = -hh * 0.78
    B.hair_back(p, sp, 0, hy, hw, hh)
    for s_ in (-1, 1):                                       # two stubby legs and flat black shoes
        lx = s_ * tw * fl * 0.42
        leg_c = skin if out == 'dress' else sp.get('trousers', (34, 34, 40))
        p.poly([(lx - 21, th - 20), (lx + 21, th - 20), (lx + 19, th + legs), (lx - 19, th + legs)], leg_c)
        p.ell(lx + s_ * 9, th + legs + 4, 34, 15, (26, 24, 26))
    sh = {s_: (s_ * (tw - 6), 30) for s_ in (-1, 1)}
    hands = hands or {}
    for side, s_ in (('L', -1), ('R', 1)):                   # arms behind the body when they hang down
        hx_, hy_ = hands.get(side, (s_ * (tw * fl + 10), th * 0.74))
        if hy_ > 60:
            tube(p, L, [sh[s_], ((sh[s_][0] + hx_) / 2 + s_ * 6, (sh[s_][1] + hy_) / 2), (hx_, hy_)], 34, coat)
    body = curve([(-34, -8), (-tw * 0.86, 4), (-tw, 42), (-(tw * fl * 0.97 + belly), th * 0.6), (-tw * fl, th),
                  (tw * fl, th), (tw * fl * 0.97 + belly, th * 0.6), (tw, 42), (tw * 0.86, 4), (34, -8)], 3)
    p.poly(body, coat)
    if out == 'suit':                                        # shirt, tie, two lapel lines: nothing more
        p.poly([(-28, -6), (28, -6), (0, th * 0.44)], sp.get('shirt', (230, 234, 240)))
        p.poly([(-8, 4), (8, 4), (11, th * 0.38), (0, th * 0.47), (-11, th * 0.38)], sp.get('tie', (150, 32, 44)))
        p.line([(-28, -6), (-4, th * 0.5)], B.INK, 2.4)
        p.line([(28, -6), (4, th * 0.5)], B.INK, 2.4)
    elif out == 'jumper':                                    # a football shirt: white collar, a badge
        p.poly([(-30, -6), (30, -6), (0, 30)], (240, 240, 240))
        p.ell(tw * 0.42, 52, 13, 15, (240, 240, 240))
    elif out == 'dress':
        for k_ in range(3):                                  # three big buttons
            p.ell(0, 40 + k_ * 40, 7, 7, B.lt(coat, 0.8))
    for side, s_ in (('L', -1), ('R', 1)):                   # raised arms in front
        hx_, hy_ = hands.get(side, (s_ * (tw * fl + 10), th * 0.74))
        if hy_ <= 60:
            tube(p, L, [sh[s_], (sh[s_][0] + s_ * 70, 70), (hx_, hy_)], 34, coat)
    for side, s_ in (('L', -1), ('R', 1)):
        hx_, hy_ = hands.get(side, (s_ * (tw * fl + 10), th * 0.74))
        if phone and side == 'R':
            p.poly([(hx_ - 26, hy_ - 64), (hx_ + 26, hy_ - 64), (hx_ + 26, hy_ + 16), (hx_ - 26, hy_ + 16)], (40, 44, 56))
        p.ell(hx_, hy_, 24, 24, skin)
    B.head(img, p, sp, t, 0, hy)


def _pts(cam, pts):
    return [cam.P(*q) for q in pts]


def flat(d, cam, pts, fill, seed=0, j=5):
    """A background shape: flat colour, no outline, corners cut by hand (a little uneven, never jittered evenly)."""
    r = random.Random(seed)
    d.polygon(_pts(cam, [(x + r.gauss(0, j), y + r.gauss(0, j)) for x, y in pts]), fill=fill)


def style_frame(CM, t=1.5):
    """Cry Minister's opening, redesigned: Andy to camera on the high street; behind him one wolf at its meal and one
    shopper walking past on her phone. Nothing else."""
    import wolf as WF
    B = CM.B
    B.SS = 2
    img = B.canvas((200, 208, 212))
    cam = B.Cam(1.0)
    d = ImageDraw.Draw(img)
    # the street: six big shapes
    flat(d, cam, [(-20, 250), (540, 236), (548, 1170), (-20, 1170)], (238, 230, 212), 1)     # the pub, plaster
    flat(d, cam, [(-20, 200), (520, 214), (560, 262), (-20, 262)], (84, 58, 50), 2)          # its roof
    for k, bx in enumerate((70, 260, 450)):                                                   # three black beams
        flat(d, cam, [(bx - 26, 262), (bx + 26, 262), (bx + 30 + 6 * k, 700), (bx - 22 + 6 * k, 700)], (46, 36, 32), 3 + k)
    flat(d, cam, [(-20, 690), (548, 690), (552, 1170), (-20, 1170)], (44, 76, 56), 7)       # the green pub front
    flat(d, cam, [(30, 860), (300, 852), (304, 1100), (28, 1104)], (232, 198, 116), 8)       # one warm window
    flat(d, cam, [(540, 300), (1100, 290), (1100, 1170), (548, 1170)], (176, 138, 116), 9)  # ZapBets, upstairs
    flat(d, cam, [(660, 400), (880, 396), (884, 590), (662, 594)], (92, 96, 108), 10)
    flat(d, cam, [(548, 690), (1100, 680), (1100, 1170), (552, 1170)], (94, 48, 134), 11)  # ZapBets, purple
    flat(d, cam, [(600, 860), (900, 856), (904, 1110), (598, 1114)], (248, 214, 56), 12)   # its free-bet poster
    flat(d, cam, [(-20, 1160), (1100, 1150), (1100, 1920), (-20, 1920)], (180, 176, 168), 13)  # the pavement
    for s, xx, yy, size, col, font in (('THE GOOSE', 60, 712, 70, (232, 196, 100), CM.PUB_FONT),
                                       ('ZapBets', 640, 700, 96, (248, 214, 56), B.ANTON),
                                       ('FREE', 668, 870, 84, (94, 48, 134), B.ANTON),
                                       ('£10 BET', 628, 968, 84, (200, 30, 60), B.ANTON)):
        lay = hand_letters(s, font, cam.S(size), col, hash(s) & 0xFFFF)
        X0, Y0 = cam.P(xx, yy)
        img.alpha_composite(lay, (int(X0 - size * 0.4 * B.SS), int(Y0 - size * 0.3 * B.SS)))
    # behind him, the absurd thing: one wolf at its meal, a pair of legs sticking out; a flat red pool
    X = CM.X_(img, cam)
    WF.blood(X, 860, 1236, 120, 3)
    for dy, ang in ((0, 0.05), (26, -0.08)):                 # his legs, trousers and shoes, pointing at us
        X.poly([(900, 1214 + dy), (1010, 1206 + dy + 40 * ang), (1012, 1232 + dy + 40 * ang), (900, 1240 + dy)], (60, 70, 96))
        X.ell(1024, 1219 + dy + 40 * ang, 14, 22, (26, 24, 26))
    WF.side(X, 820, 1240, 0.62, -1, 1, feed=0.35, blood=0.6, seed=4)
    # walking past on the left, not looking: a shopper on her phone
    sh_sp = dict(CM.SHOPPER_LOOKS[2], turn=0.0, look=0.4, lid=4, mouth='line', outfit='suit', hair='bob',
                 jacket=(172, 92, 60), shirt=(236, 220, 200), tie=(172, 92, 60), trousers=(40, 40, 46))
    toon(img, cam, 170, 1300, 0.86, sh_sp, DESIGNS['shopper'], hands={'R': (40, 40)}, t=t, phone=True)
    # Andy, to camera, thumbing back over his shoulder at it
    sp = CM.andy_sp(t)
    sp['look'] = 0.0
    toon(img, cam, 520, 1640, 2.35, sp, DESIGNS['Andy'], hands={'L': (-150, 150), 'R': (120, -40)}, t=t)
    return img


def cast_row(CM):
    """The four people of Cry Minister in the new proportions, each a different build, on one flat floor."""
    B = CM.B
    B.SS = 2
    img = B.canvas((214, 208, 198))
    cam = B.Cam(1.0)
    d = ImageDraw.Draw(img)
    flat(d, cam, [(-20, 1400), (1100, 1390), (1100, 1920), (-20, 1920)], (190, 182, 170), 5)
    sp = CM.andy_sp(1.5)
    sp['look'] = 0.0
    people = [(CM.LADY, 'the old lady', 150, 0.95, {'R': (60, 20)}),
              (sp, 'Andy', 410, 1.0, None),
              (dict(CM.MAN, mouth='line'), 'the man', 680, 0.98, {'L': (-150, 120), 'R': (150, 120)}),
              (dict(CM.SHOPPER_LOOKS[5], outfit='suit', mouth='smile'), 'shopper', 920, 0.98, None)]
    for spx, name, x, k, hands in people:
        toon(img, cam, x, 1460, k * 1.12, dict(spx), DESIGNS[name], hands=hands, t=1.5,
             phone=(name == 'the old lady'))
    return img


def styleframe(out):
    CM = _film()
    import ed
    B = CM.B
    quiet = [(m, 'soft', lambda *a, **k: None) for m in list(sys.modules.values()) if getattr(m, 'soft', None) is ed.soft]
    quiet += [(m, 'glow', lambda *a, **k: None) for m in list(sys.modules.values()) if getattr(m, 'glow', None) is ed.glow]
    with swapped(quiet):                                     # flat colour only: no airbrushed shadow on any face
        new = style_frame(CM).convert('RGB').resize((1080, 1920), Image.LANCZOS).convert('RGBA')
        cast = cast_row(CM).convert('RGB').resize((1080, 1920), Image.LANCZOS).crop((0, 560, 1080, 1560))
    B.SS = 1
    new = CM.overlay(new, 1.5).convert('RGB')
    today = Image.open(os.path.join(RAW, 'cm', '1.5.jpg')).convert('RGB')
    tw, th, gap, head = 560, 996, 20, 80
    sheet = Image.new('RGB', (2 * tw + 3 * gap, head + th + 60 + 560 + 60), PAPER)
    dd = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(SANS, 30)
    dd.text((gap, 20), 'Style frame: Cry Minister, opening shot', font=ImageFont.truetype(SANS, 38), fill=(20, 20, 20))
    for i, (im, lab) in enumerate(((today, 'Today'), (new, 'Redesigned (same faces)'))):
        x = gap + i * (tw + gap)
        sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, head))
        dd.text((x, head + th + 12), lab, font=f, fill=(20, 20, 20))
    y = head + th + 60
    cw = 2 * tw + gap
    sheet.paste(cast.resize((cw, int(cast.height * cw / cast.width)), Image.LANCZOS).crop((0, 0, cw, 520)), (gap, y))
    dd.text((gap, y + 524), 'The cast in the new proportions: the old lady, Andy, the man, a shopper', font=f, fill=(20, 20, 20))
    sheet.save(out, quality=90)
    print(out, sheet.size)


def main():
    a = sys.argv[1:]
    if a[0] == 'gather':
        gather()
    elif a[0] == 'sample':
        sample(a[1] if len(a) > 1 else os.path.join(REVIEW, 'sheet1-sample.jpg'))
    elif a[0] == 'zoom':
        zoom(a[1] if len(a) > 1 else os.path.join(REVIEW, 'zoom-details.jpg'))
    elif a[0] == 'example':
        example(a[1] if len(a) > 1 else os.path.join(REVIEW, 'example-hope-again.jpg'))
    elif a[0] == 'styleframe':
        styleframe(a[1] if len(a) > 1 else os.path.join(REVIEW, 'styleframe-cryminister.jpg'))
    elif a[0] == 'clip':
        clip(a[1] if len(a) > 1 else os.path.join(REVIEW, 'example-hope-again.mp4'))
    elif a[0] == 'options':
        options(a[1] if len(a) > 1 else os.path.join(REVIEW, 'sheet2-options.jpg'))


if __name__ == '__main__':
    main()
