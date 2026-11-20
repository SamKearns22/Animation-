#!/usr/bin/env python3
"""Grand Theft Autism: the 6.5 s opening (Sam, 20 Nov: three seconds longer, a gentler wipe, a hold on the logo over
the city, the chorus of his song under it), a send-up of a game-trailer logo reveal (Sam, 19 Nov).

MAP
- sky set-up (top): the Flying Whales dusk sea, re-coloured pink, the sun right of centre, its orange caps removed
- logo(): our own V + I shield (blue-purple-pink-orange, faint palm leaves, pink outer line); the lettering in the
  game-title font, stretched and stacked as the reference (font fetched by _title_font, never committed)
- clouds(): big two-tier clouds, lit warm from below near the sun
- skyline(): the waterfront city in three depths (pale far, mid, dark near): towers with window grids and a lit edge
  on the sun's side, the big wheel, a seafront shelter, boats, a shaded tree, palms with full fronds; sun path dashes
- reflection(): the city mirrored in the water, darker, broken into rippling rows
- frame(t): dark (0.5 s) -> logo wipes in slowly top to bottom and grows (0.5-2.0) -> city fades in under it (1.8-3.0)
  -> held, logo over the city (to 4.7) -> logo washes pale and dissolves (4.7-5.65) -> city
- music(): the song's chorus (from 36.48 s, so its first hit lands on the wipe's start at 0.5 s), faded out at the end
- house look: the city drawing gets paper edges and shadows (house_look.edges); every frame is laid on paper; drawn on
  twos (12 drawings a second, each held 2 frames at 24 fps)
- python3 source/gta_opener.py OUT.mp4 [--small]      python3 source/gta_opener.py still OUT.png T [T ...]

Reference: Sam's screen recording (19 Nov), 3.4 s. House look: flat colours, one ink outline, no glows.
"""
import math
import os
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage as nd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import flying_whales_sea as S                     # noqa: E402
import house_look as HL                           # noqa: E402

# ---- the sky and sea, re-coloured before anything is baked (the painter caches its first bake)
S.SUN_AZ = math.atan(100 / 1400)                  # the sun a little right of centre, as in the reference
S.SKY = [(0.55, (255, 240, 222)), (1.35, (253, 220, 206)), (2.7, (248, 198, 202)), (4.6, (240, 178, 202)),
         (7.6, (230, 168, 210)), (12.0, (218, 160, 214)), (19.0, (204, 152, 216)), (28.0, (190, 144, 214)),
         (90.0, (174, 134, 208))]
S.GOLD = (255, 248, 232)
S.SEA_DEEP = (70, 36, 82)
S.SEA = [S._mix(c, S.SEA_DEEP, 0.30 + 0.08 * k) for k, (_, c) in enumerate(S.SKY)]
S.CLOUDS = []                                     # our own big clouds instead (clouds())
S._caps = lambda d, t, ss, hy: None               # no orange wave caps: the reference's water is open and calm

W, H = S.SIZE
FPS = 24
DRAW_FPS = 12                                     # on twos
DUR = 6.5
WIPE0, WIPE = 0.5, 1.5                           # the logo's wipe: starts on the chorus's first hit, 1.5 s long
CITY0, CITY_IN = 1.8, 1.2                        # the city fades in under the logo
OUT0 = 4.7                                       # the logo washes pale from here, then dissolves
SONG = os.path.join(HERE, '..', 'music', 'gta-opener-chorus.mp3')   # Sam's song, the chorus cut (20 Nov)
SONG_AT = 36.48                                  # where in the whole song the cut starts (0.5 s before the chorus hits)
INK = (40, 12, 56)
DARK = (27, 26, 36)
OL = 3
TITLE_FONT = os.path.join(HERE, 'fonts', 'Pricedown-Bl.otf')   # free for rendered video; the file may not be shared,
TITLE_URL = 'https://dl.dafont.com/dl/?f=pricedown'            # so it is not on GitHub: fetched here when missing
HY = S.horizon_y()
SUNX = S._sun_x()
WARM = (255, 214, 196)                            # the sun's light on edges that face it


def _title_font():
    """The title font's file, downloaded once (Typodermic's free desktop licence: rendered video is fine, sharing the
    file is not, so it stays out of the repository)."""
    if not os.path.exists(TITLE_FONT):
        import io
        import urllib.request
        import zipfile
        req = urllib.request.Request(TITLE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(req, timeout=60).read()))
        name = next(n for n in z.namelist() if n.lower().endswith(('.otf', '.ttf')))
        open(TITLE_FONT, 'wb').write(z.read(name))
    return TITLE_FONT


def _disk(r):
    y, x = np.mgrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def _ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def _mixc(a, b, k):
    return tuple(int(round(a[i] + (b[i] - a[i]) * k)) for i in range(3))


def _grad(size, stops):
    """Diagonal gradient, top-left to bottom-right, through colour stops."""
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    k = np.clip(xx / w * 0.5 + yy / h * 0.5, 0, 1)
    out = np.zeros((h, w, 3))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        m = (k >= a) & (k <= b)
        f = ((k - a) / (b - a))[m][:, None]
        out[m] = np.array(ca) * (1 - f) + np.array(cb) * f
    return Image.fromarray(out.astype(np.uint8))


def _frond(d, x, y, ang, L, wid, col, s, droop=0.55, notches=0):
    """One palm leaf: a tapered curve from (x, y) out along ang (degrees), drooping at the tip; notches cut the
    edge into leaflets."""
    r = math.radians(ang)
    n = 16
    pts = [(x + math.cos(r) * L * i / n, y + math.sin(r) * L * i / n + droop * L * (i / n) ** 2) for i in range(n + 1)]
    left, right = [], []
    for i, (px, py) in enumerate(pts):
        u = i / n
        w = wid * math.sin(math.pi * min(0.95, u * 0.9 + 0.08))
        if notches and 0.15 < u < 0.95 and i % 2:
            w *= 0.45
        j = min(i, n - 1)
        dx, dy = pts[j + 1][0] - pts[j][0], pts[j + 1][1] - pts[j][1]
        m = math.hypot(dx, dy) or 1
        left.append(((px - dy / m * w) * s, (py + dx / m * w) * s))
        right.append(((px + dy / m * w) * s, (py - dx / m * w) * s))
    d.polygon(left + right[::-1], fill=col)


def _palm(d, x, base, h, lean, col, s, size=1.0, seed=0):
    rnd = random.Random(seed)
    pts = [(x + lean * (i / 10) ** 1.6, base - h * i / 10) for i in range(11)]
    for i, ((ax, ay), (bx, by)) in enumerate(zip(pts, pts[1:])):
        d.line([ax * s, ay * s, bx * s, by * s], fill=col, width=int((8 - 3 * i / 10) * s * size))
    tx, ty = pts[-1]
    for a in (-172, -152, -128, -104, -80, -56, -32, -10, 12, 168):   # fronds fanning out, arching, tips drooping
        a += rnd.uniform(-7, 7)
        up = math.sin(math.radians(a))
        down = 0.18 if up < -0.6 else 0.42
        _frond(d, tx, ty, a, rnd.uniform(80, 104) * size, 12 * size, col, s, droop=down)
    d.ellipse([(tx - 7 * size) * s, (ty - 6 * size) * s, (tx + 7 * size) * s, (ty + 6 * size) * s], fill=col)


def logo(ss=2):
    """The logo on a transparent layer, 920 x 780 px (drawn at ss times and shrunk)."""
    s = ss
    Wd, Hd = 920 * s, 780 * s
    V = [(30, 40), (285, 40), (452, 500), (605, 40), (700, 40), (522, 740), (372, 740)]
    I = [(730, 40), (890, 40), (890, 740), (730, 740)]
    V, I = [[(x, 40 + (y - 40) * 646 / 700) for x, y in P] for P in (V, I)]     # the reference's proportions (4:3)
    shapes = [[(x * s, y * s) for x, y in P] for P in (V, I)]
    mask = Image.new('L', (Wd, Hd), 0)
    md = ImageDraw.Draw(mask)
    for P in shapes:
        md.polygon(P, fill=255)
    fill = _grad((Wd, Hd), [(0, (72, 96, 232)), (0.3, (140, 70, 214)), (0.55, (226, 72, 168)),
                            (0.78, (246, 104, 120)), (1.0, (252, 176, 72))]).convert('RGBA')
    leaves = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))     # faint palm leaves inside, as in the reference
    ld = ImageDraw.Draw(leaves)
    for x, y, a0 in ((180, 120, 0), (640, 200, 40), (820, 520, -20), (420, 650, 10)):
        for a in range(-170, 180, 30):
            _frond(ld, x, y, a + a0, 200, 22, (60, 20, 120, 56), s, droop=0.35)
    fill.alpha_composite(leaves)
    img = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))
    rd = ImageDraw.Draw(img)
    for P in shapes:                                   # pink outer line (the trailer's neon edge, kept flat), dark rim
        rd.line(P + [P[0]], fill=(236, 96, 196, 255), width=44 * s, joint='curve')
    for P in shapes:
        rd.line(P + [P[0]], fill=INK + (255,), width=30 * s, joint='curve')
        rd.polygon(P, fill=INK + (255,))
    body = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))
    body.paste(fill, (0, 0), mask)
    img.alpha_composite(body)
    wd = ImageDraw.Draw(img)
    for P in shapes:
        wd.line(P + [P[0]], fill=(255, 250, 252, 255), width=6 * s, joint='curve')
    # lettering, measured off the reference on a 10 x 10 grid over the shield (19 Nov): the game-title font with its
    # tall letters cut down so they stand only a little above the short ones (as the logo's do), three rows packed
    # tight and stepped, the whole block in ONE thick dark outline with a thin pink line round it (the trailer's
    # glow, kept flat), the letters pure white
    sx = lambda g: (30 + g * 86) * s                   # grid units -> px (shield 30-890 wide, 40-686 tall)
    sy = lambda g: (40 + g * 64.6) * s
    # (word, left, baseline, size): 'autism' is two letters longer than the reference's 'auto', so that row is 8% smaller
    # and starts further left to stay on the shield
    words = (('gRand', 2.4, 2.95, 1.0), ('theft', 3.5, 5.6, 1.0), ('autism', 2.05, 8.2, 0.92))
    xh_px = (sy(8.2) - sy(6.2))                        # the short letters' height: 2.0 grid units
    f = ImageFont.truetype(_title_font(), 100)
    base, xh, asc = f.getbbox('a')[3], f.getbbox('a')[1], f.getbbox('d')[1]
    k = xh_px / (base - xh)
    f = ImageFont.truetype(_title_font(), int(round(100 * k)))
    base, xh, asc = f.getbbox('a')[3], f.getbbox('a')[1], f.getbbox('d')[1]
    asc_new = xh - 0.16 * (base - xh)                  # the tall letters stand 16% above the short ones
    block = np.zeros((Hd, Wd), bool)
    placed = {}
    full = f
    for word, gx, gb, sz in words:
        f = full if sz == 1.0 else ImageFont.truetype(_title_font(), int(round(100 * k * sz)))
        base, xh, asc = f.getbbox('a')[3], f.getbbox('a')[1], f.getbbox('d')[1]
        asc_new = xh - 0.16 * (base - xh)
        m = Image.new('L', (int(f.getlength(word)) + 40, f.getbbox(word)[3] + 40), 0)   # tall enough for the g's tail
        ImageDraw.Draw(m).text((20, 20), word, font=f, fill=255)
        a0 = np.asarray(m).astype(np.float32)
        out = a0.copy()
        top, x_top = asc + 20, xh + 20
        nt = asc_new + 20
        for y in range(0, x_top):                      # remap the rows above the short letters' top
            if y < nt:
                out[y] = 0
            else:
                src = top + (y - nt) * (x_top - top) / (x_top - nt)
                out[y] = a0[int(min(x_top - 1, max(0, round(src))))]
        mm = out > 127
        h, w = mm.shape
        oy = int(sy(gb) - (base + 20))
        ox = int(sx(gx) - 20)
        block[max(0, oy):oy + h, max(0, ox):ox + w] |= mm[max(0, -oy):Hd - oy, max(0, -ox):Wd - ox]
        placed[word] = (ox + 20, f)
    # the reference joins the R's leg straight down into the h of the row below: one white stem through both rows
    (gx0, gf), (tx0, tf) = placed['gRand'], placed['theft']
    r0, r1 = gx0 + gf.getlength('g'), gx0 + gf.getlength('gR')
    h0, h1 = tx0 + tf.getlength('t'), tx0 + tf.getlength('th')
    yR = int(sy(2.95)) - 3
    cols_h = [x for x in range(int(h0), int(h1)) if block[:, x].any()]
    yH = min(np.nonzero(block[:, x])[0][np.nonzero(block[:, x])[0] > yR + 6].min() for x in cols_h
             if (np.nonzero(block[:, x])[0] > yR + 6).any())
    stem = [x for x in cols_h if block[yH + 4 * s, x]]
    stem = [x for x in stem if x < stem[0] + (r1 - r0) * 0.45]        # the h's left stem only
    leg = [x for x in range(int(r0), int(r1)) if block[yR, x]]
    xa, xb = min(stem), max(stem)
    if leg:                                            # the joint spans from the R's leg to the h's stem
        xa, xb = min(xa, max(leg[0], xa - 4 * s)), max(xb, min(leg[-1], xb + 4 * s))
    block[yR - 2 * s:yH + 6 * s, xa:xb + 1] = True
    # the g's tail, as the reference's: a thick bar under the g, joined to its right stem, a thin dark slit above it open to the left
    g0, g1 = int(gx0), int(gx0 + gf.getlength('g'))
    yB = int(sy(2.95))
    gc = [x for x in range(g0, g1) if block[yB - 30 * s:yB - 4 * s, x].any()]
    gl, gr = min(gc), max(gc)
    run = [x for x in range(gl, gr + 1) if block[yB - 40 * s, x]]
    gaps = [nx for x, nx in zip(run, run[1:]) if nx != x + 1]
    stem_l = gaps[-1] if gaps else run[0]              # where the g's right-hand stem starts
    block[yB:yB + 40 * s, gl:gr + 1] = False           # clear the font's own thin tail
    block[yB + 5 * s:yB + 26 * s, gl:gr + 1] = True    # the tail bar, 0.33 grid tall
    block[yB - 6 * s:yB + 26 * s, stem_l:gr + 1] = True   # joined on the RIGHT: the slit opens to the left
    ring = nd.binary_fill_holes(nd.binary_dilation(block, structure=_disk(13 * s)))   # no specks between rows
    pink = nd.binary_dilation(ring, structure=_disk(3 * s))
    rows = np.nonzero(block.any(1))[0]
    rgb = np.zeros((Hd, Wd, 3))
    rgb[pink] = (236, 96, 196)
    rgb[ring] = INK
    rgb[block] = (255, 255, 255)                       # pure white, as the reference
    L = Image.fromarray(np.dstack([rgb.astype(np.uint8), (pink * 255).astype(np.uint8)]), 'RGBA')
    img.alpha_composite(L)
    return img.resize((Wd // ss, Hd // ss), Image.LANCZOS)


def _pale(L):
    """The washed-out logo of the flash: every colour pushed to pink-white, the shape kept."""
    a = np.asarray(L).astype(float)
    rgb = a[..., :3] * 0.3 + np.array([255, 232, 244]) * 0.7
    return Image.fromarray(np.dstack([rgb, a[..., 3]]).astype(np.uint8), 'RGBA')


def _blob(d, lumps, fill, s):
    for x, y, r in lumps:
        d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=fill)


def _shift(a, k):
    """a moved up by k rows (down if k < 0), empty rows filled False."""
    if k > 0:
        return np.vstack([a[k:], np.zeros((k, a.shape[1]), bool)])
    return np.vstack([np.zeros((-k, a.shape[1]), bool), a[:k]])


def clouds(ss=2):
    """Big clouds: a wide base of lumps with smaller lumps piled on top; lavender body, a shaded middle, a pale top,
    the underside lit pink (warm peach near the sun); one ink outline. """
    s = ss
    rnd = random.Random(4)
    rgb = np.zeros((H * s, W * s, 3), np.uint8)
    alpha = np.zeros((H * s, W * s), np.uint8)
    spec = ((170, 300, 560, 1.0), (840, 500, 640, 1.15), (300, 720, 480, 0.8), (930, 150, 420, 0.9),
            (600, 880, 340, 0.6), (110, 960, 260, 0.45), (980, 830, 220, 0.4))
    for cx, cy, wid, sc in spec:
        lumps = []
        n = int(wid / 50)
        for i in range(n):                             # the base
            u = i / (n - 1) - 0.5
            r = (50 + rnd.uniform(0, 30)) * sc * (1 - abs(u) ** 2 * 1.3)
            lumps.append((cx + u * wid, cy - r * 0.3 + rnd.uniform(-8, 8), max(16, r)))
        for i in range(max(2, n // 3)):                # the piled tops
            u = rnd.uniform(-0.3, 0.3)
            r = (60 + rnd.uniform(0, 40)) * sc
            lumps.append((cx + u * wid, cy - r * 0.9 - rnd.uniform(10, 40) * sc, r))
        m = Image.new('L', (W * s, H * s), 0)
        _blob(ImageDraw.Draw(m), lumps, 255, s)
        ImageDraw.Draw(m).rectangle([0, int((cy + 34 * sc) * s), W * s, H * s], fill=0)   # flat-ish bottoms
        full = np.asarray(m) > 127
        ring = np.asarray(m.filter(ImageFilter.MaxFilter(2 * OL * s + 1))) > 127
        below1 = _shift(full, int(20 * sc * s))        # still cloud 20 px below: not the lit underside
        below2 = _shift(full, int(60 * sc * s))        # still cloud 60 px below: above the shaded band
        above = _shift(full, -int(24 * sc * s))
        near = math.exp(-((cx - SUNX) / 380) ** 2) * max(0.0, 1 - (HY - cy) / 1100)
        rgb[ring] = INK
        rgb[full] = _mixc((242, 170, 204), (255, 206, 176), near)
        rgb[full & below1] = (214, 176, 222)
        rgb[full & below2] = (228, 198, 234)
        rgb[full & ~above] = (250, 234, 246)
        alpha[ring] = 255
    img = Image.fromarray(np.dstack([rgb, alpha]), 'RGBA')
    return img.resize((W, H), Image.LANCZOS)


def skyline(ss=2):
    """The waterfront city on the horizon in three depths, as an RGBA layer (sun path included)."""
    s = ss
    hy = HY
    lay = Image.new('RGBA', (W * s, H * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    ink = INK + (255,)
    rnd = random.Random(21)

    def tower(x, w, h, col, steps=0, mast=False, grid=True, setback=False):
        top = hy - h
        body = [(x, top, x + w, hy + 4)]
        if setback:                                     # a narrower upper block
            body = [(x, top + h * 0.3, x + w, hy + 4), (x + w * 0.15, top, x + w * 0.85, top + h * 0.3 + 2)]
        for (a, b, c2, e) in body:
            d.rectangle([a * s, b * s, c2 * s, e * s], fill=col + (255,), outline=ink, width=OL * s)
            lit = _mixc(col, WARM, 0.45)                # the edge facing the sun
            ex = (c2 - 8, c2 - 2) if (a + c2) / 2 < SUNX else (a + 2, a + 8)
            d.rectangle([ex[0] * s, (b + 3) * s, ex[1] * s, (e - 2) * s], fill=lit + (255,))
            if grid:                                    # windows: a grid of small panes, a few lit
                win = _mixc(col, (255, 255, 255), 0.16)
                lw = _mixc(col, WARM, 0.7)
                cols = max(2, int((c2 - a - 16) / 16))
                for yy in np.arange(b + 16, e - 20, 22):
                    for k in range(cols):
                        wx = a + 10 + k * (c2 - a - 20) / cols
                        cw = (c2 - a - 20) / cols - 6
                        c = lw if rnd.random() < 0.06 else win
                        d.rectangle([wx * s, yy * s, (wx + cw) * s, (yy + 10) * s], fill=c + (255,))
        tt = body[-1][1]
        for k in range(steps):                         # a stepped crown
            f = (0.8, 0.62, 0.45)[k]
            cw = w * f
            yy = tt - 26 * (k + 1)
            d.rectangle([(x + (w - cw) / 2) * s, yy * s, (x + (w + cw) / 2) * s, (yy + 26) * s],
                        fill=col + (255,), outline=ink, width=OL * s)
        if mast:
            yy = tt - 26 * steps
            d.line([(x + w * 0.5) * s, (yy - 70) * s, (x + w * 0.5) * s, yy * s], fill=ink, width=OL * s)

    far, mid, near = (238, 196, 214), (220, 168, 198), (196, 138, 180)
    d.ellipse([(SUNX - 50) * s, (hy - 80) * s, (SUNX + 50) * s, (hy + 20) * s], fill=(255, 250, 238, 255))
    for x, w, h in ((-10, 90, 300), (130, 70, 240), (250, 80, 280), (420, 110, 340), (700, 90, 260),
                    (840, 80, 300), (1000, 90, 280)):
        tower(x, w, h, far, grid=False)
    for x, w, h, st, sb in ((-20, 120, 560, 0, False), (95, 70, 470, 0, True), (300, 150, 620, 3, False),
                            (470, 90, 380, 0, True), (960, 140, 600, 0, True)):
        tower(x, w, h, mid, steps=st, mast=st > 0, setback=sb)
    tower(150, 90, 400, near)
    # the sun's path on the water: pale dashes, widening towards us
    rp = random.Random(12)
    for k in range(46):
        u = (k / 46) ** 1.4
        yy = hy + 8 + u * 430 + rp.uniform(-4, 4)
        half = 12 + u * 70
        x = SUNX - half * rp.uniform(0.8, 1.2)
        while x < SUNX + half:
            seg = half * rp.uniform(0.25, 0.7)
            d.line([x * s, yy * s, min(x + seg, SUNX + half) * s, yy * s], fill=(255, 244, 230, 230),
                   width=int((2 + u * 5) * s))
            x += seg + half * rp.uniform(0.1, 0.35)
    # the big wheel, right of the sun, backlit: rim, inner rim, spokes, cabins, legs
    cx, cy, r = 790, hy - 190, 160
    wc = (150, 92, 140, 255)
    d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], outline=wc, width=6 * s)
    d.ellipse([(cx - r + 14) * s, (cy - r + 14) * s, (cx + r - 14) * s, (cy + r - 14) * s], outline=wc, width=3 * s)
    for k in range(24):
        a = 2 * math.pi * k / 24
        ex, ey = cx + math.cos(a) * r, cy + math.sin(a) * r
        d.line([cx * s, cy * s, ex * s, ey * s], fill=wc, width=2 * s)
        d.rounded_rectangle([(ex - 8) * s, (ey - 2) * s, (ex + 8) * s, (ey + 14) * s], radius=4 * s, fill=wc)
    d.ellipse([(cx - 14) * s, (cy - 14) * s, (cx + 14) * s, (cy + 14) * s], fill=wc)
    d.line([((cx - 70) * s, hy * s), (cx * s, cy * s), ((cx + 70) * s, hy * s)], fill=wc, width=7 * s)
    # the waterfront: a dark low band with a lit top edge, a seafront shelter on the left, moored boats
    dark = (104, 58, 106, 255)
    d.rectangle([0, (hy - 34) * s, W * s, (hy + 6) * s], fill=dark)
    d.line([0, (hy - 32) * s, W * s, (hy - 32) * s], fill=_mixc(dark[:3], WARM, 0.35) + (255,), width=3 * s)
    d.line([0, (hy - 34) * s, W * s, (hy - 34) * s], fill=ink, width=OL * s)
    px0, px1, ptop = 190, 420, hy - 120
    for px in np.linspace(px0, px1, 6):
        d.rectangle([(px - 6) * s, ptop * s, (px + 6) * s, (hy - 30) * s], fill=dark, outline=ink, width=2 * s)
    for k in range(3):
        yy = ptop - 4 + k * 12
        d.rectangle([(px0 - 20) * s, yy * s, (px1 + 20) * s, (yy + 8) * s], fill=dark, outline=ink, width=2 * s)
    for px in np.linspace(px0 - 10, px1 + 10, 14):     # the slats on top
        d.line([px * s, (ptop - 12) * s, px * s, (ptop - 2) * s], fill=dark, width=4 * s)
    boat = (236, 196, 214)
    for bx, bw in ((20, 110), (150, 80), (470, 90), (860, 120)):
        d.polygon([(bx * s, (hy - 14) * s), ((bx + bw) * s, (hy - 14) * s), ((bx + bw - 14) * s, (hy + 4) * s),
                   ((bx + 10) * s, (hy + 4) * s)], fill=boat + (255,), outline=ink)
        d.line([(bx + 8) * s, (hy - 8) * s, (bx + bw - 8) * s, (hy - 8) * s], fill=_mixc(boat, INK, 0.4) + (255,),
               width=2 * s)
        d.rectangle([(bx + bw * 0.3) * s, (hy - 30) * s, (bx + bw * 0.6) * s, (hy - 14) * s],
                    fill=boat + (255,), outline=ink, width=2 * s)
        d.line([(bx + bw * 0.45) * s, (hy - 70) * s, (bx + bw * 0.45) * s, (hy - 30) * s], fill=ink, width=2 * s)
    # the big tree, left of the sun: a lumpy crown, darker lumps inside, warm-lit lumps on the sun side
    rt = random.Random(8)
    lumps = [(470 + rt.uniform(-110, 110), hy - 170 + rt.uniform(-70, 50), rt.uniform(40, 70)) for _ in range(18)]
    tm = Image.new('L', lay.size, 0)
    _blob(ImageDraw.Draw(tm), lumps, 255, s)
    trunk = [(455, hy), (485, hy), (478, hy - 140), (500, hy - 190), (490, hy - 196), (470, hy - 150),
             (450, hy - 200), (440, hy - 194), (462, hy - 140)]
    ImageDraw.Draw(tm).polygon([(x * s, y * s) for x, y in trunk], fill=255)
    lay.paste(ink, (0, 0), tm.filter(ImageFilter.MaxFilter(2 * OL * s + 1)))
    lay.paste((96, 52, 100, 255), (0, 0), tm)
    inner = Image.new('L', lay.size, 0)
    _blob(ImageDraw.Draw(inner), [(x - 10, y + 14, r * 0.6) for x, y, r in lumps[::2]], 255, s)
    lay.paste((88, 47, 93, 255), (0, 0), Image.fromarray(np.minimum(np.asarray(inner), np.asarray(tm))))
    litm = Image.new('L', lay.size, 0)
    _blob(ImageDraw.Draw(litm), [(x + 14, y - 16, r * 0.45) for x, y, r in lumps if x > 480], 255, s)
    lay.paste((116, 66, 112, 255), (0, 0), Image.fromarray(np.minimum(np.asarray(litm), np.asarray(tm))))
    # palms, darkest, in front
    pc = (84, 44, 92, 255)
    for i, (x, h, lean, sz) in enumerate(((30, 260, 20, 1.1), (95, 220, -15, 1.0), (165, 250, 25, 1.1),
                                          (240, 200, -10, 0.9), (575, 180, 15, 0.8), (690, 210, -20, 0.9),
                                          (740, 170, 10, 0.7), (900, 230, -25, 1.0), (1050, 260, -35, 1.1))):
        _palm(d, x, hy + 2, h, lean, pc, s, sz, seed=i)
    return lay.resize((W, H), Image.LANCZOS)


def reflection(city):
    """The city upside down in the water: squashed, darker and pinker, see-through, fading with distance."""
    hy = int(HY)
    src = np.asarray(city).astype(np.float32)[hy - 680:hy][::-1]
    ref = Image.fromarray(src.astype(np.uint8), 'RGBA').resize((W, int(src.shape[0] * 0.45)), Image.LANCZOS)
    a = np.asarray(ref).astype(np.float32)
    a[..., :3] = a[..., :3] * 0.55 + np.array([110, 58, 110]) * 0.45
    a[..., 3] *= np.linspace(0.42, 0.0, a.shape[0])[:, None]
    return a


def _ripple(ref, t):
    """The reflection broken into rows, each nudged sideways by a slow wave; every third band dropped (the gaps)."""
    out = np.zeros_like(ref)
    for y in range(ref.shape[0]):
        if (y // 7 + int(t * 4)) % 5 == 0:
            continue
        out[y] = np.roll(ref[(y // 3) * 3], int(round(math.sin(y // 3 * 0.5 + t * 2.4) * (1 + y * 0.03))), axis=0)
    return Image.fromarray(out.astype(np.uint8), 'RGBA')


def _place(img, layer, scale, cx, cy, alpha, reveal=1.0):
    """Put layer at scale, centred on (cx, cy); reveal wipes it in from the top with a soft bottom edge."""
    if alpha <= 0 or reveal <= 0:
        return
    w, h = layer.size
    L = layer.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    a = np.asarray(L.getchannel('A')).astype(float) * alpha
    if reveal < 1:
        hh = L.size[1]
        edge = reveal * (hh + 360) - 360                   # a tall soft edge: the gentle wipe
        a = a * np.clip((edge + 360 - np.arange(hh)[:, None]) / 360, 0, 1)
    L.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(L, (int(cx - L.size[0] / 2), int(cy - L.size[1] / 2)))


def frame(t, LOGO, PALE, CITY, REF):
    # the city: fades in under the logo, a slow push in all the way (the camera drifting forward over the water)
    city_a = _ease((t - CITY0) / CITY_IN)
    img = Image.new('RGBA', (W, H), DARK + (255,))
    if city_a > 0:
        push = 1.0 + 0.08 * (t - CITY0) / (DUR - CITY0)
        bg = S.paint(t).convert('RGBA')
        bg.alpha_composite(_ripple(REF, t), (0, int(HY) + 6))
        bg.alpha_composite(CITY)
        e = HL.edges(np.asarray(bg.convert('RGB'), np.float32) / 255)       # paper edges and shadows
        bg = Image.fromarray((np.clip(e, 0, 1) * 255 + 0.5).astype(np.uint8)).convert('RGBA')
        bw, bh = int(W * push), int(H * push)
        ox, oy = (bw - W) // 2, int((bh - H) * 0.58)
        bg = bg.resize((bw, bh), Image.LANCZOS).crop((ox, oy, ox + W, oy + H))
        img = Image.blend(img, bg, city_a)
    # the logo: wipes in gently top to bottom while growing, keeps growing slowly through the hold, washes pale,
    # dissolves
    u = t - WIPE0
    reveal = _ease(u / WIPE)
    scale = 0.86 + 0.08 * _ease(u / 2.0) + 0.05 * min(1, max(0, u) / (OUT0 + 0.95 - WIPE0))
    a_out = 1 - _ease((t - OUT0 - 0.4) / 0.55)
    pale = _ease((t - OUT0) / 0.45)
    cx, cy = W / 2, 860
    _place(img, LOGO, scale, cx, cy, a_out * (1 - pale), reveal)
    _place(img, PALE, scale, cx, cy, a_out * pale, reveal)
    a = HL.lay_on_paper(np.asarray(img.convert('RGB'), np.float32) / 255, HL.LOOK['paper'])
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def layers():
    L = logo()
    city = clouds()
    sky = skyline()
    city.alpha_composite(sky)
    return L, _pale(L), city, reflection(sky)


def main():
    out = sys.argv[1]
    small = '--small' in sys.argv
    L, P, C, R = layers()
    size = '540x960' if small else '1080x1920'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-vf', f'scale={size}', '-c:v', 'libx264', '-crf', '18',
                          '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out],
                         stdin=subprocess.PIPE)
    step = FPS // DRAW_FPS
    for i in range(0, int(DUR * FPS), step):          # on twos: each drawing held for 2 frames
        fr = frame(i / FPS, L, P, C, R).tobytes()
        for _ in range(step):
            p.stdin.write(fr)
    p.stdin.close()
    p.wait()
    if os.path.exists(SONG) and '--silent' not in sys.argv:      # the chorus under the picture
        tmp = out + '.music.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-i', SONG, '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', tmp], check=True)
        os.replace(tmp, out)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'still':
        L, P, C, R = layers()
        for tt in map(float, sys.argv[3:]):
            frame(tt, L, P, C, R).save(sys.argv[2].replace('.png', f'_{tt}.png'))
    else:
        main()
