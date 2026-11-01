#!/usr/bin/env python3
"""Flying Whales: the dusk sky and sea, painted flat in the house style for the film's one locked camera (1 Nov).

What it paints (refs dusk-pink-sky-rig, dusk-sunset-waves, fire-dusk-glow):
- the sky in flat bands, purple at the top through pink to orange at the horizon; the sun has just set left of
  frame, so the warm bands swell up into a dome over that spot (a pale gold sliver right at the horizon there);
  the band edges are hand-cut (wavy, never ruler-straight);
- streaky clouds lit from below (gold near the sunset, pink further off), each with the one ink outline;
- the sea mirroring the sky in bands (the same colours turned upside down, deeper and bluer towards us);
- ripple strokes laid on the sea in perspective (tiny near the horizon, long near us), rising and falling on a slow
  swell and drifting with the wind; a glitter path of gold flecks under the sunset that twinkle;
- a row of low wave caps in front (dark, lit warm along the crest, ink outline on top), bobbing on the swell;
- glow(): the sea turned orange in a column under any fire (for the explosions and the burning deck).

The camera is the film's camera (CAM): 8 m above the sea, 120 m from the rig's nearest corner (the rig stands round
the world origin; whale.py's axes: x right, y away from us, z up). Pass the same CAM to whale.draw and the rig.
Camera shake and drift are done by the compositor on the finished frame (a small shift), so this painting is baked
once and only the moving parts are drawn each frame.

    python3 source/flying_whales_sea.py sheet OUT.jpg            the sheet for Sam (with whales at real size for scale)
    python3 source/flying_whales_sea.py reel OUT.mp4 [--small]   a few seconds of the sea moving

Use in the film:
    import flying_whales_sea as S
    frame = S.paint(t, glows=[((x, y, z), strength, width_m)])   # RGB 1080x1920
    S.sea_z(x, y, t)                                             # the swell height (m) at a point, for foam at legs
"""
import functools
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import whale as W                                    # noqa: E402  (the Cam class and the house ink)

INK = W.INK
SIZE = (1080, 1920)
CAM = W.Cam(pos=(0.0, -120.0, 8.0), yaw=0.0, pitch=6.0, focal=1400.0, size=SIZE)
OL = 5                                               # the house outline, px at 1080 wide

SUN_AZ = math.atan(-0.24)                            # where the sun went down: a little left of straight ahead
DUSK_TINT = (255, 150, 170, 0.14)                    # for whale.draw(tint=...): the pink dusk light on everything

# sky bands from the horizon up: (top edge in degrees above the horizon, away from the sunset; colour)
SKY = [
    (0.55, (250, 196, 140)),     # pale orange at the horizon
    (1.35, (246, 166, 128)),     # salmon
    (2.7, (236, 138, 140)),      # coral pink
    (4.6, (214, 120, 152)),      # pink
    (7.6, (180, 104, 156)),      # mauve
    (12.0, (142, 88, 150)),      # violet
    (19.0, (110, 74, 138)),      # purple
    (28.0, (82, 62, 122)),       # dusk purple
    (90.0, (60, 50, 104)),       # indigo, the top of the frame
]
GOLD = (252, 224, 164)           # the sliver where the sun went down
SEA_DEEP = (40, 36, 84)          # what the sea darkens towards as it comes to us
DOME = 1.3                       # how much the warm bands swell over the sunset
DOME_W = 0.32                    # its width (radians of azimuth)


def _mix(a, b, k):
    return tuple(int(round(a[i] + (b[i] - a[i]) * k)) for i in range(3))


SEA = [_mix(c, SEA_DEEP, 0.24 + 0.07 * k) for k, (_, c) in enumerate(SKY)]


# --------------------------------------------- the baked painting --------------------------------------------------
def _rays(cam, ss):
    """Elevation and azimuth (radians) of every pixel's ray, at ss times the frame size (roll 0 camera)."""
    w, h = cam.size
    f = cam.focal
    p = math.radians(6.0) if cam is CAM else -math.asin(float(cam.R[2, 1]))     # pitch from the camera's matrix
    xs = ((np.arange(w * ss, dtype=np.float32) + 0.5) / ss - w / 2) / f
    ys = (h / 2 - (np.arange(h * ss, dtype=np.float32) + 0.5) / ss) / f
    a, b = np.meshgrid(xs, ys)
    yp = math.cos(p) - math.sin(p) * b
    zp = math.sin(p) + math.cos(p) * b
    return np.arctan2(zp, np.hypot(a, yp)), np.arctan2(a, yp)


def _edges(az, k, sea):
    """Band k's top edge (radians) along each azimuth: swelled over the sunset, hand-cut wavy."""
    e = math.radians(SKY[k][0])
    g = np.exp(-((az - SUN_AZ) / DOME_W) ** 2)
    e = e * (1 + DOME * g * max(0.0, 1 - k / 5) * (0.45 if sea else 1.0))   # only the warm low bands swell
    rnd = random.Random(31 + k)
    ph = [rnd.uniform(0, 6.3) for _ in range(4)]
    deg = math.radians(1)
    if sea:   # the reflection: a short, shallow ripple along the edge
        wob = (0.06 * np.sin(60 * az + ph[0]) + 0.04 * np.sin(130 * az + ph[1])) * deg * (0.4 + 0.15 * k)
    else:     # hand-cut: one or two long gentle waves across the frame, a smaller one on top
        wob = (0.35 * np.sin(9 * az + ph[0]) + 0.18 * np.sin(23 * az + ph[1]) + 0.06 * np.sin(61 * az + ph[2])) \
            * deg * (0.3 + 0.1 * k)
    return e + wob


def _bands(elev, az, sea):
    x = np.abs(elev)
    idx = np.zeros(x.shape, np.int16)
    for k in range(len(SKY) - 1):
        idx += (x > _edges(az, k, sea)).astype(np.int16)
    pal = np.array([c for c in (SEA if sea else [c for _, c in SKY])], np.uint8)
    out = pal[idx]
    if not sea:   # the gold sliver
        g = np.exp(-((az - SUN_AZ) / (DOME_W * 0.55)) ** 2)
        out[x < math.radians(0.7) * g] = GOLD
    return out


# clouds: (x px, elevation degrees, length px, thickness px, tilt px over its length, seed). Kept off the rig's middle.
CLOUDS = [
    (150, 3.4, 420, 34, -10, 1),
    (360, 6.2, 300, 26, 6, 2),
    (880, 4.0, 380, 30, -6, 3),
    (120, 11.5, 520, 46, 14, 4),
    (760, 15.5, 560, 50, -12, 5),
    (420, 23.0, 640, 60, 8, 6),
    (980, 27.0, 420, 44, 4, 7),
]


def _screen_y(cam, elev_deg, x=None):
    """Screen y of a direction elev_deg above the horizon, straight ahead (good enough to place clouds)."""
    p = 6.0 if cam is CAM else -math.degrees(math.asin(float(cam.R[2, 1])))
    return cam.size[1] / 2 - cam.focal * math.tan(math.radians(elev_deg - p))


def _cloud(img, cx, cy, length, thick, tilt, seed, ss):
    """One streak: lumps along a gently tilted line, a lit underside, the one ink outline round it all."""
    rnd = random.Random(seed)
    n = max(5, int(length / (thick * 0.9)))
    lumps = []
    for i in range(n):
        u = i / (n - 1) - 0.5
        taper = 1 - (2 * abs(u)) ** 2.2 * 0.7
        rx = thick * rnd.uniform(0.9, 1.6) * taper
        ry = thick * rnd.uniform(0.38, 0.62) * taper
        lumps.append((cx + u * length + rnd.uniform(-6, 6), cy + u * tilt + rnd.uniform(-0.25, 0.1) * thick, rx, ry))
    x0 = int((min(l[0] - l[2] for l in lumps) - 20) * ss)
    y0 = int((min(l[1] - l[3] for l in lumps) - 20) * ss)
    x1 = int((max(l[0] + l[2] for l in lumps) + 20) * ss)
    y1 = int((max(l[1] + l[3] for l in lumps) + 20) * ss)
    m = Image.new('L', (x1 - x0, y1 - y0), 0)
    d = ImageDraw.Draw(m)
    for x, y, rx, ry in lumps:
        d.ellipse([(x - rx) * ss - x0, (y - ry) * ss - y0, (x + rx) * ss - x0, (y + ry) * ss - y0], fill=255)
    mask = np.asarray(m) > 127
    lit_h = int(thick * 0.32 * ss)
    up = np.zeros_like(mask)
    up[:-lit_h] = mask[lit_h:]
    lit = mask & ~up
    # colours from where it sits: lit gold near the sunset, pink further off; body a muted purple of its sky
    el = (_screen_y(CAM, 0) - cy) / CAM.focal
    near_sun = math.exp(-(((cx - (540 + CAM.focal * math.tan(SUN_AZ))) / 420) ** 2))
    body = _mix((150, 100, 150), (92, 70, 128), min(1, el * 3.2))
    litc = _mix((242, 150, 150), (252, 206, 150), near_sun)
    ring = np.asarray(m.filter(ImageFilter.MaxFilter(2 * int(OL * ss / 2) + 1))) > 127
    rgb = np.zeros(mask.shape + (3,), np.uint8)
    rgb[ring] = INK
    rgb[mask] = body
    rgb[lit] = litc
    alpha = (ring * 255).astype(np.uint8)
    tile = Image.fromarray(np.dstack([rgb, alpha]), 'RGBA')
    img.alpha_composite(tile, (x0, y0))


@functools.lru_cache(maxsize=2)
def base(ss=2):
    """The still part, baked once: sky bands, clouds, sea bands. RGB at the frame size."""
    elev, az = _rays(CAM, ss)
    sky = _bands(elev, az, False)
    sea = _bands(elev, az, True)
    arr = np.where((elev >= 0)[..., None], sky, sea)
    img = Image.fromarray(arr, 'RGB').convert('RGBA')
    for x, e, length, thick, tilt, seed in CLOUDS:
        _cloud(img, x, _screen_y(CAM, e), length, thick, tilt, seed, ss)
    return img.convert('RGB').resize(SIZE, Image.LANCZOS)


def horizon_y(cam=CAM):
    return _screen_y(cam, 0.0)


# --------------------------------------------- the moving parts ----------------------------------------------------
SWELL_A, SWELL_L, SWELL_T = 0.22, 22.0, 7.0          # m, m, s: a slow, low swell
WIND = 0.18                                          # m/s, the ripples' drift to the right


def sea_z(x, y, t):
    """Swell height (m) at a sea point: two long slow waves crossing (for foam at the rig's legs and the caps)."""
    k = 2 * math.pi / SWELL_L
    w = 2 * math.pi / SWELL_T
    return SWELL_A * (np.sin(k * y - w * t) * 0.7 + np.sin(k * 0.63 * (y * 0.8 + x * 0.6) - w * 0.8 * t + 1.3) * 0.5)


def _ground(cam, sx, sy):
    """The sea point (z = 0) seen at screen (sx, sy)."""
    w, h = cam.size
    ray = np.stack([(sx - w / 2) / cam.focal, np.ones_like(sx), (h / 2 - sy) / cam.focal], -1)
    d = ray @ cam.R
    s = -cam.pos[2] / d[..., 2]
    return cam.pos[None, :] + d * s[..., None]


@functools.lru_cache(maxsize=1)
def _strokes(n=2300):
    """Ripple strokes fixed on the sea: world point, screen length and thickness (at rest), colour kind, phase."""
    rnd = np.random.default_rng(7)
    hy = horizon_y()
    v = rnd.random(n) ** 1.7                          # more rows near the horizon, where they are tiny
    sy = hy + 4 + v * (SIZE[1] - hy - 4)
    sx = rnd.uniform(-120, SIZE[0] + 120, n)
    P = _ground(CAM, sx, sy)
    frac = (sy - hy) / (SIZE[1] - hy)
    length = rnd.uniform(10, 54, n) * (0.3 + 0.9 * frac)
    thick = 1.0 + 4.5 * frac ** 1.3
    kind = rnd.random(n) < 0.55                       # True: a light face (reflecting higher sky), False: a trough
    phase = rnd.uniform(0, 6.3, n)
    depth = P[:, 1] - CAM.pos[1]
    return P, length * depth / CAM.focal, thick, kind, phase


def _project(cam, P):
    q = (P - cam.pos) @ cam.R.T
    d = np.maximum(q[..., 1], 0.05)
    return cam.size[0] / 2 + cam.focal * q[..., 0] / d, cam.size[1] / 2 - cam.focal * q[..., 2] / d, d


def _sun_x(cam=CAM):
    return cam.size[0] / 2 + cam.focal * math.tan(SUN_AZ)


def _caps(d, t, ss, hy):
    """Low wave caps close in front: dark humps lit warm along the crest, ink along the top, bobbing on the swell."""
    rnd = random.Random(11)
    span = 24.0                                       # m of sea the caps wrap round as they drift
    for i in range(9):
        y = -100.0 - i * 0.55 + rnd.uniform(-0.2, 0.2)   # 15-20 m out, far first (the frame's foot is 15 m out)
        x = rnd.uniform(-span / 2, span / 2) + 0.35 * t
        x = (x + span / 2) % span - span / 2
        half = rnd.uniform(1.4, 2.4)
        h = rnd.uniform(0.45, 0.75) * (0.85 + 0.15 * math.sin(1.1 * t + i))
        lump = [rnd.uniform(0.75, 1.0) for _ in range(5)]
        top, bot = [], []
        for j in range(17):
            u = j / 16
            xx = x - half + 2 * half * u
            bump = math.sin(math.pi * u) ** 1.4 * lump[min(4, int(u * 5))]
            zz = float(sea_z(xx, y, t)) + h * bump
            top.append((xx, y, zz))
            bot.append((xx, y, float(sea_z(xx, y, t)) - 0.08))
        tp = np.array(top)
        bp = np.array(bot)
        X, Y, _ = _project(CAM, tp)
        BX, BY, _ = _project(CAM, bp[::-1])
        crest = [(a * ss, b * ss) for a, b in zip(X, Y)]
        foot = [(a * ss, b * ss) for a, b in zip(BX, BY)]
        d.polygon(crest + foot, fill=(38, 34, 82))
        # the lit band along the crest: the top third
        lit_lo = [(a * ss, (b + (fb - b) * 0.38) * ss) for (a, b), (fa, fb) in zip(zip(X, Y), zip(BX[::-1], BY[::-1]))]
        d.polygon(crest + lit_lo[::-1], fill=(236, 146, 128))
        d.line(crest, fill=INK, width=int(OL * ss), joint='curve')


def glow(img, cam, pos, strength=1.0, width_m=12.0):
    """The sea turned orange under a fire at world pos (x, y, z above the sea), in two flat steps, with warm streaks.
    The column runs from the waterline under the fire down towards us, about as long as the fire is high, mirrored."""
    x, y, z = pos
    fx, fy, _ = _project(cam, np.array([x, y, z], float))
    wx, wy, dep = _project(cam, np.array([x, y, 0.0], float))
    length = max(40.0, (wy - fy) * 1.3)
    half = cam.focal * width_m / 2 / dep
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rnd = random.Random(int(x * 13 + y * 7))
    # the column is a stack of flat horizontal bars with ragged ends (the sea's ripples catching the light), an outer
    # orange step and an inner yellow one, thinning out towards us; plus loose flecks beyond it
    al = int(255 * min(1.0, strength))
    yy = wy
    while yy < wy + length:
        v = (yy - wy) / length
        bh = max(2.0, 2 + 9 * v) * rnd.uniform(0.6, 1.2)
        hw = half * (0.9 + 0.7 * v) * rnd.uniform(0.6, 1.15)
        cx = wx + rnd.uniform(-0.15, 0.15) * half
        if rnd.random() < 0.93 - 0.35 * v:
            d.rectangle([cx - hw, yy, cx + hw, yy + bh], fill=(236, 116, 72, al))
            if rnd.random() < 0.8 - 0.4 * v:
                iw = hw * rnd.uniform(0.35, 0.7)
                ix = cx + rnd.uniform(-0.25, 0.25) * hw
                d.rectangle([ix - iw, yy + bh * 0.15, ix + iw, yy + bh * 0.85], fill=(255, 196, 100, al))
        yy += bh + max(1.0, 1 + 5 * v) * rnd.uniform(0.6, 1.4)
    for i in range(int(30 * strength) + 6):
        v = rnd.random()
        sy = wy + v * length * 1.25
        sw = half * (0.3 + 0.8 * v) * rnd.uniform(0.3, 0.9)
        sx = wx + rnd.uniform(-1, 1) * half * (1.4 + 0.8 * v)
        col = (255, 226, 150) if rnd.random() < 0.5 else (250, 140, 80)
        d.line([(sx - sw / 2, sy), (sx + sw / 2, sy)], fill=col + (al,), width=max(1, int(1 + 3 * v)))
    hy = int(horizon_y(cam))
    lay.paste((0, 0, 0, 0), (0, 0, img.size[0], max(0, hy)))   # never on the sky
    img.alpha_composite(lay)


def paint(t, glows=(), cam=CAM, ss=2):
    """One frame of sky and sea at time t (s). glows: [((x, y, z), strength 0-1, width_m)] fires lighting the sea."""
    img = base().copy()
    hy = horizon_y(cam)
    top = int(hy) - 2
    H = SIZE[1] - top
    lay = Image.new('RGBA', (SIZE[0] * ss, H * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    P, Lw, thick, kind, phase = _strokes()
    Q = P.copy()
    Q[:, 0] += WIND * t
    Q[:, 2] = sea_z(Q[:, 0], Q[:, 1], t)
    X, Y, dep = _project(cam, Q)
    breathe = 0.78 + 0.22 * np.sin(1.3 * t + phase)
    half = cam.focal * Lw / dep / 2 * breathe
    sunx = _sun_x(cam)
    frac = np.clip((Y - hy) / (SIZE[1] - hy), 0, 1)
    path = np.abs(X - sunx) < 30 + 190 * frac
    twinkle = np.sin(4.2 * t + phase * 3.1) > -0.2
    src = np.asarray(img)
    for i in np.argsort(dep)[::-1]:                   # far first
        x, y = X[i], Y[i]
        if y < hy + 1 or y > SIZE[1] + 4 or x < -80 or x > SIZE[0] + 80:
            continue
        under = src[int(min(SIZE[1] - 1, max(0, y))), int(min(SIZE[0] - 1, max(0, x)))]
        if path[i]:
            if not twinkle[i]:
                continue
            col = (255, 228, 160) if kind[i] else (252, 186, 170)
        elif kind[i]:
            col = _mix(tuple(int(c) for c in under), (255, 196, 186), 0.32)
        else:
            col = _mix(tuple(int(c) for c in under), SEA_DEEP, 0.38)
        yy = (y - top) * ss
        d.line([((x - half[i]) * ss, yy), ((x + half[i]) * ss, yy)], fill=col,
               width=max(1, int(round(thick[i] * ss))))
    _caps_layer = d
    # the caps are drawn in screen space offset by top
    cap = Image.new('RGBA', (SIZE[0] * ss, SIZE[1] * ss), (0, 0, 0, 0))
    _caps(ImageDraw.Draw(cap), t, ss, hy)
    lay.alpha_composite(cap.crop((0, top * ss, SIZE[0] * ss, SIZE[1] * ss)))
    small = lay.resize((SIZE[0], H), Image.LANCZOS)
    out = img.convert('RGBA')
    out.alpha_composite(small, (0, top))
    for g in glows:
        glow(out, cam, *g)
    return out.convert('RGB')


# --------------------------------------------- sheet and reel ------------------------------------------------------
def _label(img, text, size=34):
    lab = W._font(size)
    d = ImageDraw.Draw(img)
    tw = d.textlength(text, font=lab)
    d.rectangle([0, 0, tw + 28, size + 22], fill=(250, 248, 242))
    d.text((14, 9), text, fill=(30, 30, 30), font=lab)


def _whales(frame, t):
    """Five whales at real size (14 m) placed as in the composition, for scale on the sheet only."""
    spots = [  # (pos, yaw, pitch, roll, pattern)
        ((-12.0, -80.0, 7.0), 35, 10, -12, 0),
        ((9.0, -68.0, 12.0), -38, 12, 14, 1),
        ((-18.0, -40.0, 16.0), 30, 8, -10, 2),
        ((14.0, -25.0, 24.0), -32, 6, 8, 3),
        ((-2.0, -5.0, 32.0), 25, 4, -6, 4),
    ]
    out = frame.convert('RGBA')
    sprs = []
    for pos, yaw, pitch, roll, pat in spots:
        spr = W.draw(CAM, W.Pose(pos, yaw, pitch, roll), pattern=pat, t=t, tint=DUSK_TINT, blow=0.4 if pat == 1 else None)
        if spr:
            sprs.append(spr)
    for spr in sorted(sprs, key=lambda s: -s.depth):
        spr.paste(out)
    return out.convert('RGB')


def sheet(path):
    import time
    t0 = time.time()
    a = paint(0.0)
    b = _whales(paint(2.0), 2.0)
    c = paint(4.0, glows=[((-6.0, 20.0, 34.0), 1.0, 26.0), ((14.0, 8.0, 12.0), 0.7, 10.0)])
    # stand-in fireballs for the glow panel, so the column has a source (the real ones come with the effects)
    dc = ImageDraw.Draw(c)
    for (x, y, z), r in [((-6.0, 20.0, 34.0), 13.0), ((14.0, 8.0, 12.0), 5.0)]:
        px, py, dep = _project(CAM, np.array([x, y, z]))
        rr = CAM.focal * r / dep
        dc.ellipse([px - rr, py - rr, px + rr, py + rr], fill=(250, 150, 60), outline=INK, width=OL)
        dc.ellipse([px - rr * 0.5, py - rr * 0.5, px + rr * 0.5, py + rr * 0.5], fill=(255, 228, 140))
    print('three frames in %.1f s' % (time.time() - t0))
    panels = [(a, '1  dusk, t = 0 (no rig yet)'), (b, '2  five whales at real size, for scale'),
              (c, '3  the sea glowing under fires (stand-ins)')]
    tiles = []
    for im, text in panels:
        im = im.resize((720, 1280), Image.LANCZOS)
        _label(im, text, 28)
        tiles.append(im)
    # a full-size detail of the sea: the glitter path and caps
    det = a.crop((0, 1150, 1080, 1920)).resize((720, 513), Image.LANCZOS)
    _label(det, '4  detail: glitter path, ripples, wave caps', 28)
    det2 = a.crop((0, 330, 1080, 1180)).resize((720, 567), Image.LANCZOS)
    _label(det2, '5  detail: clouds lit from below, band edges', 28)
    gap = 20
    Wd = 720 * 4 + gap * 5
    out = Image.new('RGB', (Wd, 1280 + gap * 2), (250, 248, 242))
    for i, tl in enumerate(tiles):
        out.paste(tl, (gap + i * (720 + gap), gap))
    x4 = gap + 3 * (720 + gap)
    out.paste(det2, (x4, gap))
    out.paste(det, (x4, gap + 567 + gap))
    ImageDraw.Draw(out).text((x4, gap + 567 + gap + 513 + 30),
                             'Sun just set, left of frame. Clouds: my addition (set dressing).\n'
                             'Camera 8 m up, 120 m from the rig, looking a touch up.',
                             fill=(30, 30, 30), font=W._font(24))
    out.save(path, quality=88)
    print('saved', path, '%.0f KB' % (os.path.getsize(path) / 1024))


def reel(path, small=False, secs=4.0, fps=30):
    import subprocess
    import time
    import imageio_ffmpeg
    t0 = time.time()
    size = (540, 960) if small else SIZE
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % size,
           '-r', str(fps), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for i in range(int(secs * fps)):
        fr = paint(i / fps)
        if small:
            fr = fr.resize(size, Image.LANCZOS)
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    p.wait()
    print('saved', path, '%.0f KB in %.0f s' % (os.path.getsize(path) / 1024, time.time() - t0))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'sheet'
    if cmd == 'sheet':
        sheet(sys.argv[2] if len(sys.argv) > 2 else 'review/flying-whales-sea-sheet.jpg')
    elif cmd == 'reel':
        reel(sys.argv[2], small='--small' in sys.argv)
    else:
        print(__doc__)
