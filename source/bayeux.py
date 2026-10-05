"""The Bayeux Tapestry Season Pass: a video-game season pass trailer for a 950-year-old tapestry.

Proof-of-concept cut: the gallery and the title, then the pan along the tapestry with four weapon swaps.
Everything inside the tapestry is stitched (bayeux_stitch.py, bayeux_weapons.py); the trailer effects play over
the top. Sam will record the trailer voice; until then the words slam on screen with the music.

    python3 bayeux.py stills OUT_DIR T [T ...]    single frames at full size
    python3 bayeux.py animatic OUT.mp4           half size (540 x 960), 24 fps, with sound
    python3 bayeux.py final OUT.mp4              full size (1080 x 1920)
    python3 bayeux.py times                      the timeline
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage as ndi

import bayeux_stitch as BS
import bayeux_weapons as BW

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, 'fonts')
W0, H0 = 1080, 1920
FPS = 24
R = 1.0                       # render scale (0.5 for the animatic)

# ------------------------------------------------------------------------------------------- the timeline
T_INTRO = 0.15                # INTRODUCING
T_BAYEUX, T_TAPESTRY = 0.95, 1.20
ARROWS_AT = [1.48, 1.62, 1.80, 1.94]      # the four flaming arrows land (two per Y)
T_SEASON = 2.25               # SEASON PASS wipes in, in fire
D = 2.0                       # the title lingers this much longer while SEASON PASS roars
CUT_TAPESTRY = 3.95 + D       # glitch cut to the tapestry
T_NEW = 4.10 + D              # NEW WEAPONS
SWAPS = {'rifle': 5.35 + D, 'claw': 7.20 + D, 'ghost': 9.00 + D, 'stapler': 12.10 + D}
NAMES = {'rifle': 'PLASMA LONGSHOT RIFLE', 'claw': 'ICE CLAW', 'ghost': 'GHOST PISTOL', 'stapler': 'STAPLER'}
STAPLER_FADE = 15.30          # all the stapler's glory fades away...
NAME_OUT = {'rifle': 6.90 + D, 'claw': 8.70 + D, 'ghost': 10.90 + D, 'stapler': STAPLER_FADE + 0.45}
GHOST_FLY = (9.30 + D, 9.85 + D)   # the ghost streams out of the pistol
STAPLER_CLICK = 16.00         # ...and it fires one single staple: click
STAPLE_HIT = 16.20            # the staple reaches the messenger
CUT_END_TITLE = 17.20         # the title slams back
BLACK_AT = 18.60              # hard cut to black
DUR = 18.90


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def lerp(a, b, x):
    return a + (b - a) * x


def keyed(t, keys):
    """Smoothly interpolated value from (time, value...) keys."""
    if t <= keys[0][0]:
        return keys[0][1:]
    for k0, k1 in zip(keys, keys[1:]):
        if t <= k1[0]:
            x = ease((t - k0[0]) / (k1[0] - k0[0]))
            return tuple(lerp(a, b, x) for a, b in zip(k0[1:], k1[1:]))
    return keys[-1][1:]


# -------------------------------------------------------------------------------------------------- noise
def _noise_tex(n=256, seed=1, smooth=6.0):
    rng = np.random.default_rng(seed)
    a = rng.standard_normal((n, n))
    f = np.fft.fft2(a)
    ky = np.fft.fftfreq(n)[:, None]
    kx = np.fft.fftfreq(n)[None, :]
    f *= np.exp(-(kx ** 2 + ky ** 2) * (smooth ** 2) * 40)
    out = np.real(np.fft.ifft2(f))
    out = (out - out.min()) / (out.max() - out.min())
    return out.astype(np.float32)


NOISE = [_noise_tex(seed=s) for s in (1, 2, 3)]


def noise(k, x, y):
    return ndi.map_coordinates(NOISE[k], [np.asarray(y) % 256, np.asarray(x) % 256], order=1, mode='wrap')


# --------------------------------------------------------------------------------------------------- fire
FIRE_STOPS = np.array([[0.00, 0, 0, 0, 0.0], [0.18, 110, 12, 0, 0.35], [0.40, 210, 58, 6, 0.85],
                       [0.62, 255, 136, 22, 1.0], [0.82, 255, 210, 90, 1.0], [1.05, 255, 250, 215, 1.0]],
                      np.float32)


def fire_colour(h):
    out = np.zeros(h.shape + (4,), np.float32)
    for c in range(4):
        out[..., c] = np.interp(h, FIRE_STOPS[:, 0], FIRE_STOPS[:, c + 1])
    return out


def fire(src, t, rise, seed=0, lick=1.0):
    """Flames rising off a source (2-D array 0..1): heat carried upwards and fading, broken into licking
    tongues by noise that scrolls upwards, swaying more the higher it goes."""
    h, w = src.shape
    a = math.exp(-1.0 / max(1.0, rise))
    heat = src.astype(np.float32).copy()
    for y in range(h - 2, -1, -1):          # carried upwards, fading
        np.maximum(heat[y], heat[y + 1] * a, out=heat[y])
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    sc = 1.0 / max(R, 0.25)
    fx, fy = xx * sc, yy * sc
    above = np.clip(heat - ndi.gaussian_filter(src.astype(np.float32), 1.5), 0, 1)
    sway = (noise(0, fx / 16 + seed * 37, fy / 22 + t * 30) - 0.5) * 60 * R * lick
    dy = (noise(1, fx / 9 + seed * 53, fy / 9 + t * 60) - 0.5) * 16 * R * lick
    heat = ndi.map_coordinates(heat, [yy + dy, xx + sway * (0.3 + above)], order=1, mode='constant')
    n = noise(2, fx / 3.2 + seed * 11, fy / 11 + t * 120)
    tongue = np.clip((heat * 1.45 - (1 - n) * 0.75) * 1.9, 0, 0.95)
    core = ndi.gaussian_filter(src.astype(np.float32), 1.0 * R + 0.5)
    inner = noise(1, fx / 4 + seed * 7, fy / 6 + t * 90)
    heat = np.maximum(core * (0.70 + 0.32 * inner), tongue)
    return fire_colour(np.clip(heat, 0, 1.1))


def add_light(base, rgba, x0, y0):
    """Additive light (fire, glows) onto an RGB float array at (x0, y0)."""
    h, w = rgba.shape[:2]
    H, W = base.shape[:2]
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb:
        return
    sub = rgba[ya - y0:yb - y0, xa - x0:xb - x0]
    base[ya:yb, xa:xb] += sub[..., :3] * sub[..., 3:4]


def over(base, rgba, x0, y0, alpha=1.0):
    h, w = rgba.shape[:2]
    H, W = base.shape[:2]
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb:
        return
    sub = rgba[ya - y0:yb - y0, xa - x0:xb - x0]
    a = sub[..., 3:4] * alpha
    base[ya:yb, xa:xb] = base[ya:yb, xa:xb] * (1 - a) + sub[..., :3] * a


# ------------------------------------------------------------------------------------------- the strip
HB = 900                      # the tapestry band's height on screen at zoom 1 (design pixels)
BAND_Y = 800                  # where the band's middle sits on screen
MARGIN, DIV = 320, 210
PANELS = ['rifle', 'claw', 'ghost', 'stapler']
REF_H = {'rifle': 711, 'claw': 330, 'ghost': 330, 'stapler': 350}


class Strip:
    """The tapestry, panel by panel, at the size it is shown: before and after each swap."""

    def __init__(self, scale):
        self.k = scale                       # strip pixels per design pixel
        hs = int(round(HB * scale))
        self.h = hs
        self.items = []                      # (x0 design, name, {state: array})
        x = MARGIN
        tree = tree_image()
        for i, name in enumerate(PANELS):
            ims = {}
            for st in ('before', 'after') + (('pistol',) if name == 'ghost' else ()):
                im = Image.open(os.path.join(BW.CACHE, f'{name}-{st}.png')).convert('RGB')
                w = int(round(im.width * hs / im.height))
                ims[st] = np.asarray(im.resize((w, hs), Image.LANCZOS), np.float32)
            wd = ims['before'].shape[1] / scale
            self.items.append([x, name, ims])
            x += wd
            if i < len(PANELS) - 1:
                self.items.append([x - DIV * 0.25, 'tree', {'before': tree_strip(tree, hs, int(DIV * 1.5 * scale))}])
                x += DIV
        self.width = x + MARGIN
        self.ref_scale = {n: HB / REF_H[n] for n in PANELS}
        self.x0 = {it[1]: it[0] for it in self.items}
        self.linen = np.array(BS.WOOL['linen'], np.float32) * 0.97
        self._glow = {}

    def ref_to_design(self, name, x, y):
        s = self.ref_scale[name]
        return self.x0[name] + x * s, y * s

    def window(self, x0, x1, states):
        """The strip between design x0 and x1, at strip resolution, with each panel in its current state."""
        k = self.k
        a, b = int(math.floor(x0 * k)), int(math.ceil(x1 * k))
        out = np.empty((self.h, b - a, 3), np.float32)
        out[:] = self.linen
        # the linen ground's weave in the margins: borrow a column-tiled slice of the first panel's linen
        for x, name, ims in self.items:
            st = states.get(name, 'before')
            im = ims[st] if not callable(st) else st(ims)
            px = int(round(x * k))
            w = im.shape[1]
            lo, hi = max(a, px), min(b, px + w)
            if lo >= hi:
                continue
            if name == 'tree':
                al = im[lo - px:hi - px, :, 3:4] if False else None
                seg = im[:, lo - px:hi - px]
                alpha = seg[..., 3:4]
                out[:, lo - a:hi - a] = out[:, lo - a:hi - a] * (1 - alpha) + seg[..., :3] * alpha
            else:
                seg = im[:, lo - px:hi - px]
                # soften the panel's side edges into the linen, under the trees
                ew = int(60 * k)
                wts = np.ones(hi - lo, np.float32)
                cols = np.arange(lo - px, hi - px)
                wts = np.minimum(wts, np.clip(cols / ew, 0, 1))
                wts = np.minimum(wts, np.clip((w - 1 - cols) / ew, 0, 1))
                out[:, lo - a:hi - a] = out[:, lo - a:hi - a] * (1 - wts[None, :, None]) + seg * wts[None, :, None]
        return out


def tree_image():
    """A Bayeux tree to divide the scenes: a stem with interlaced tendrils and a fan of leaves, stitched."""
    h, w = 825, 230
    L = BW.Layer(w, h)
    s = BW.S
    L.lab = Image.new('L', (w, h), BS.IDX['linen'])
    L.ang = Image.new('F', (w, h), float('nan'))
    L.dl, L.da = ImageDraw.Draw(L.lab), ImageDraw.Draw(L.ang)
    cx = w / 2 / s
    top, bot = 70 / s * 2.5, h / s
    # stem
    L.poly([(cx - 5, bot), (cx + 5, bot), (cx + 4, top + 40), (cx - 4, top + 40)], 'ochre', math.pi / 2, 'madder', 1.6)
    # two tendrils winding round the stem, crossing over and under
    for ph, wool in ((0.0, 'bluegreen'), (math.pi, 'terracotta')):
        pts = [(cx + 22 * math.sin(ph + (bot - y) / 26.0), y) for y in np.linspace(bot - 10, top + 50, 60)]
        L.line(pts, wool, 3.2)
    # the fan of leaves on top
    for i, ang in enumerate(np.linspace(-2.5, -0.64, 5)):
        lx, ly = cx + 26 * math.cos(ang), top + 46 + 30 * math.sin(ang)
        wool = ['sage', 'terracotta', 'ochre', 'terracotta', 'sage'][i]
        pts = []
        for j in range(24):
            q = 2 * math.pi * j / 24
            r1, r2 = 24, 9
            u, v = r1 * math.cos(q), r2 * math.sin(q)
            pts.append((lx + u * math.cos(ang) - v * math.sin(ang), ly + u * math.sin(ang) + v * math.cos(ang)))
        L.poly(pts, wool, ang, 'madder', 1.3)
    # curling side shoots
    for side in (-1, 1):
        for y0 in (bot - 150, bot - 260):
            pts = [(cx + side * (6 + 30 * math.sin(q) * (q / 3)), y0 - 26 * (1 - math.cos(q)) * 0.6)
                   for q in np.linspace(0, 3.0, 20)]
            L.line(pts, 'sage', 2.6)
            L.ellipse(pts[-1][0], pts[-1][1], 6, 4, 'terracotta', 0.0, 'madder', 1.0)
    lab, ang = L.arrays()
    forced = np.where(np.isnan(ang), np.nan, ang)
    rgb = BS.stitch(lab.astype(np.int16), 3.0, forced, seed=11)
    alpha = (lab != BS.IDX['linen']).astype(np.float32)
    alpha = ndi.gaussian_filter(alpha, 1.0)
    return np.dstack([rgb.astype(np.float32), np.clip(alpha * 1.4, 0, 1)])


def tree_strip(tree, hs, ws):
    rgb = Image.fromarray(tree[..., :3].astype(np.uint8)).resize((ws, hs), Image.LANCZOS)
    a = Image.fromarray((tree[..., 3] * 255).astype(np.uint8)).resize((ws, hs), Image.LANCZOS)
    return np.dstack([np.asarray(rgb, np.float32), np.asarray(a, np.float32)[..., None] / 255.0])


# ------------------------------------------------------------------------------------------- the gallery
def project(cam, p):
    """A simple pinhole camera: cam = (x, y, z, yaw, pitch, focal) in metres/radians/pixels."""
    cx, cy, cz, yaw, pitch, f = cam
    x, y, z = p[0] - cx, p[1] - cy, p[2] - cz
    c, s = math.cos(yaw), math.sin(yaw)
    x, z = c * x - s * z, s * x + c * z
    c, s = math.cos(pitch), math.sin(pitch)
    y, z = c * y - s * z, s * y + c * z
    z = max(z, 0.05)
    return (W0 / 2 + f * x / z, H0 * 0.5 - f * y / z), z


def homography(src, dst):
    A = []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    b = [c for p in dst for c in p]
    return np.linalg.solve(np.array(A, float), np.array(b, float))


GALLERY_CAM = (0.42, 1.55, -1.3, math.radians(-15), math.radians(-27), 1000)
# The London 2026 exhibit (Sam's references): the tapestry lies almost flat, tilted a little towards the visitor,
# in a long low glass case at waist height; a tall black wall behind it with glowing blue line drawings of the
# scenes and white captions; black metal frames over the glass; a warm light strip along the floor.
CASE = dict(xn=0.0, yn=0.90, xf=-0.50, yf=1.00, z0=-1.2, z1=60.0)   # the tapestry's near and far edges
WALL_X = -1.05
PANEL_STEP = 2.4                                                     # glass frames every 2.4 m


def line_art(strip, h_px):
    """The wall's glowing drawings: the tapestry's own outlines, traced as thin cyan light."""
    full = strip.window(0, strip.width, {})
    lum = full.mean(2)
    lin = np.array(BS.WOOL['linen'], np.float32).mean()
    ink = ndi.binary_opening(lum < lin * 0.45, iterations=1).astype(np.float32)
    edge = np.clip(ink - ndi.binary_erosion(ink > 0.5, iterations=2), 0, 1)
    im = Image.fromarray((edge * 255).astype(np.uint8))
    w = int(im.width * h_px / im.height)
    e = np.asarray(im.resize((w, h_px), Image.LANCZOS), np.float32) / 255
    return e


def gallery(strip):
    """The exhibition room (flat cartoon style), after Sam's London 2026 references. Drawn at design size."""
    cam = GALLERY_CAM
    S2 = 2
    img = Image.new('RGB', (W0 * S2, H0 * S2), (6, 7, 10))
    d = ImageDraw.Draw(img)

    def P(p):
        (x, y), z = project(cam, p)
        return (x * S2, y * S2)

    zf = 70.0
    c = CASE
    # floor: dark, glossy
    d.polygon([P((WALL_X, 0, -2)), P((3.0, 0, -2)), P((3.0, 0, zf)), P((WALL_X, 0, zf))], fill=(14, 15, 18))
    # the black wall behind
    d.polygon([P((WALL_X, 0, -2)), P((WALL_X, 4.0, -2)), P((WALL_X, 4.0, zf)), P((WALL_X, 0, zf))], fill=(7, 8, 12))
    # the case body: black, front face towards the visitor, with the warm light strip at its foot
    d.polygon([P((c['xn'] + 0.08, 0, c['z0'])), P((c['xn'] + 0.08, 0, zf)), P((c['xn'] + 0.08, c['yn'] - 0.05, zf)),
               P((c['xn'] + 0.08, c['yn'] - 0.05, c['z0']))], fill=(30, 30, 35))
    d.polygon([P((c['xn'] + 0.08, c['yn'] - 0.05, c['z0'])), P((c['xn'] + 0.08, c['yn'] - 0.05, zf)),
               P((c['xn'], c['yn'], zf)), P((c['xn'], c['yn'], c['z0']))], fill=(30, 30, 34))
    d.polygon([P((c['xn'] + 0.08, 0.0, c['z0'])), P((c['xn'] + 0.08, 0.0, zf)), P((c['xn'] + 0.11, 0.0, zf)),
               P((c['xn'] + 0.11, 0.0, c['z0']))], fill=(255, 210, 150))
    for k, col in enumerate(((60, 44, 30), (34, 26, 20))):
        e = 0.11 + 0.10 * (k + 1)
        d.polygon([P((c['xn'] + 0.11, 0.0, c['z0'])), P((c['xn'] + 0.11, 0.0, zf)), P((c['xn'] + e, 0.0, zf)),
                   P((c['xn'] + e, 0.0, c['z0']))], fill=col) if False else None
    # the case's back wall between the tapestry and the black wall
    d.polygon([P((c['xf'], c['yf'], c['z0'])), P((c['xf'], c['yf'], zf)), P((WALL_X, 1.25, zf)), P((WALL_X, 1.25, c['z0']))],
              fill=(12, 13, 16))
    img = img.resize((W0, H0), Image.LANCZOS)
    a = np.asarray(img, np.float32)

    def quad(za, zb, near, far):
        q = [P((far[0], far[1], za)), P((far[0], far[1], zb)), P((near[0], near[1], zb)), P((near[0], near[1], za))]
        return [(u / S2, v / S2) for u, v in q]

    def paste(src, q, frac=1.0):
        nonlocal a
        tw, th = src.size
        coef = homography(q, [(0, 0), (tw * frac, 0), (tw * frac, th), (0, th)])
        warped = np.asarray(src.transform((W0, H0), Image.PERSPECTIVE, tuple(coef), Image.BICUBIC), np.float32)
        m = Image.new('L', (W0, H0), 0)
        ImageDraw.Draw(m).polygon(q, fill=255)
        mm = np.asarray(m, np.float32)[..., None] / 255
        return warped, mm

    # the white mount the tapestry lies on (a margin on the near side), then the tapestry, tiled at true shape
    mount = quad(c['z0'], 40, (c['xn'] - 0.02, c['yn'] + 0.004), (c['xf'] - 0.02, c['yf'] + 0.004))
    m = Image.new('L', (W0, H0), 0)
    ImageDraw.Draw(m).polygon(mount, fill=255)
    mm = np.asarray(m, np.float32)[..., None] / 255
    a = a * (1 - mm) + np.array([218, 218, 212], np.float32) * mm
    full = strip.window(0, strip.width, {})
    tap = Image.fromarray(np.clip(full, 0, 255).astype(np.uint8))
    depth = math.hypot(c['xf'] - c['xn'], c['yf'] - c['yn']) * 0.86
    metres = strip.width * depth / HB
    near = (c['xn'] - 0.07, c['yn'] + 0.014)
    far = (near[0] + (c['xf'] - c['xn']) * 0.86, near[1] + (c['yf'] - c['yn']) * 0.86)
    zc = c['z0']
    while zc < 40:
        zb = zc + metres
        w, mm = paste(tap, quad(zc, zb, near, far))
        a = a * (1 - mm) + w * mm * np.array([1.0, 0.98, 0.93])
        zc = zb
    # the black wall's glowing line drawings and captions
    art = line_art(strip, 300)
    artim = Image.fromarray((art * 255).astype(np.uint8))
    yb, yt = 1.55, 2.55
    zc = 0.5
    while zc < 45:
        seg_m = (yt - yb) * art.shape[1] / art.shape[0]
        piece = min(seg_m, 2.2)
        frac = piece / seg_m
        q = [P((WALL_X + 0.01, yt, zc)), P((WALL_X + 0.01, yt, zc + piece)), P((WALL_X + 0.01, yb, zc + piece)),
             P((WALL_X + 0.01, yb, zc))]
        q = [(u / S2, v / S2) for u, v in q]
        x0 = int((zc * 300) % max(1, art.shape[1] - int(art.shape[1] * frac)))
        crop = artim.crop((x0, 0, x0 + int(art.shape[1] * frac), art.shape[0]))
        coef = homography(q, [(0, 0), (crop.width, 0), (crop.width, crop.height), (0, crop.height)])
        g = np.asarray(crop.transform((W0, H0), Image.PERSPECTIVE, tuple(coef), Image.BILINEAR), np.float32) / 255
        glow = ndi.gaussian_filter(g, 3)
        a += (g[..., None] * np.array([110, 190, 255]) * 0.8 + glow[..., None] * np.array([30, 90, 255]) * 0.9)
        # a small caption block beside each drawing: lines of white text
        for k in range(4):
            yy = yt + 0.12 - k * 0.07
            L = 0.9 - (0.3 if k == 3 else 0.0)
            pa, pb = P((WALL_X + 0.01, yy, zc - 1.25)), P((WALL_X + 0.01, yy, zc - 1.25 + L))
            dd = Image.new('L', (W0, H0), 0)
            ImageDraw.Draw(dd).line([(pa[0] / S2, pa[1] / S2), (pb[0] / S2, pb[1] / S2)], fill=200,
                                     width=max(1, int(26 / max(1.0, project(cam, (0, 0, zc))[1]))))
            a += np.asarray(dd, np.float32)[..., None] / 255 * np.array([170, 180, 190])
        zc += piece + 2.6
    # the glass: black metal frames over the case, every few metres, and a long top rail
    fr = Image.new('L', (W0, H0), 0)
    df = ImageDraw.Draw(fr)
    gh = 0.22
    for i in range(30):
        z = c['z0'] + 1.0 + i * PANEL_STEP
        zz = project(cam, (0, 0, z))[1]
        wd = max(1, int(26 / zz * 1.0))
        p1, p2 = P((c['xn'], c['yn'] + gh, z)), P((c['xf'] - 0.05, c['yf'] + gh, z))
        p3, p4 = P((c['xn'], c['yn'], z)), P((c['xf'] - 0.05, c['yf'], z))
        for u, v in ((p1, p2), (p1, p3), (p2, p4)):
            df.line([(u[0] / S2, u[1] / S2), (v[0] / S2, v[1] / S2)], fill=255, width=wd)
    for yy, xx in ((c['yn'] + gh, c['xn']), (c['yf'] + gh, c['xf'] - 0.05)):
        u, v = P((xx, yy, c['z0'])), P((xx, yy, zf))
        df.line([(u[0] / S2, u[1] / S2), (v[0] / S2, v[1] / S2)], fill=255, width=6)
    frm = np.asarray(fr, np.float32)[..., None] / 255
    a = a * (1 - frm) + np.array([14, 14, 16], np.float32) * frm
    # light: the tapestry glows softly; a faint sheen on the glass; the floor strip glows on the floor
    lit = ndi.gaussian_filter(np.clip(a.mean(2) - 120, 0, 255) / 135, 26)
    a += lit[..., None] * np.array([40, 36, 30])
    yy = np.arange(H0, dtype=np.float32)[:, None]
    xx = np.arange(W0, dtype=np.float32)[None, :]
    sheen = np.exp(-(((xx - yy * 0.9) - (-350)) / 90) ** 2) * (yy > 900)
    a += sheen[..., None] * 18
    return np.clip(a, 0, 255)


# ---------------------------------------------------------------------------------------------- lettering
def font(name, size, weight=None):
    f = ImageFont.truetype(os.path.join(FONTS, name), max(4, int(size)))
    if weight:
        f.set_variation_by_axes([weight])
    return f


def gold(mask, top, bot, bevel):
    """Game-logo metal: a gold gradient with a bevelled edge lit from the upper left, dark rim, shadow."""
    m = mask.astype(np.float32)
    dist = ndi.distance_transform_edt(m > 0.5)
    hgt = np.clip(dist / bevel, 0, 1)
    hgt = hgt * hgt * (3 - 2 * hgt)
    gy, gx = np.gradient(ndi.gaussian_filter(hgt, 0.8))
    nz = 1.0 / np.sqrt(1 + (gx * 3) ** 2 + (gy * 3) ** 2)
    lx, ly, lz = -0.45, -0.65, 0.62
    shade = np.clip((-gx * 3 * lx - gy * 3 * ly + lz) * nz, 0, 1)
    H = m.shape[0]
    yy = np.arange(H, dtype=np.float32)[:, None]
    v = np.clip((yy - top) / max(1, bot - top), 0, 1)
    c_top, c_mid, c_bot = np.array([255, 236, 168]), np.array([222, 168, 64]), np.array([128, 70, 22])
    band = np.where(v[..., None] < 0.5, c_top + (c_mid - c_top) * (v[..., None] * 2),
                    c_mid + (c_bot - c_mid) * ((v[..., None] - 0.5) * 2))
    band = np.broadcast_to(band, m.shape + (3,)).astype(np.float32)
    rgb = band * (0.45 + 0.75 * shade[..., None])
    spec = np.clip(shade - 0.82, 0, 1) * 5
    rgb += spec[..., None] * np.array([255, 250, 230]) * 0.6
    # a horizon line across the middle of the metal, like game logos
    rgb *= (1 - 0.18 * np.exp(-((v - 0.52) / 0.03) ** 2))[..., None]
    rgb = np.clip(rgb, 0, 255)
    rim = ndi.binary_dilation(m > 0.5, iterations=max(1, int(4 * R + 1)))
    outer = ndi.binary_dilation(rim, iterations=max(1, int(4 * R + 1)))
    out = np.zeros(m.shape + (4,), np.float32)
    out[outer] = [20, 10, 4, 1]
    out[rim] = [70, 36, 10, 1]
    sel = m > 0.5
    out[sel, :3] = rgb[sel]
    out[sel, 3] = 1
    return out


class Title:
    """BAYEUX / TAPESTRY in gold, the Ys made of two flaming arrows each; SEASON PASS beneath in fire."""

    def __init__(self):
        self.f1 = font('CinzelDecorative-Black.ttf', 168 * R)
        self.f3 = font('Cinzel-Variable.ttf', 104 * R, 900)
        self.lines = [('BAYEUX', 2, 690), ('TAPESTRY', 7, 880)]
        self.w = int(W0 * R)
        self.h = int(H0 * R)
        self.layers = []           # (rgba, x0, y0, x_from, x_to) for the wipe
        self.ys = []               # the Y boxes, in frame pixels
        for text, yi, base in self.lines:
            f = self.f1
            total = f.getlength(text)
            fit = min(1.0, 860 * R / total)
            if fit < 1.0:
                f = font('CinzelDecorative-Black.ttf', 168 * R * fit)
                total = f.getlength(text)
            x = (self.w - total) / 2
            y = base * R
            m = Image.new('L', (self.w, int(300 * R)), 0)
            d = ImageDraw.Draw(m)
            yl = int(230 * R)
            pre, post = text[:yi], text[yi + 1:]
            d.text((x, yl), pre, font=f, fill=255, anchor='ls')
            xp = x + f.getlength(text[:yi + 1])
            d.text((xp, yl + 0), post, font=f, fill=255, anchor='ls')
            # the Y's box (from the font's own Y)
            bx0, by0, bx1, by1 = f.getbbox('Y', anchor='ls')
            xy = x + f.getlength(pre)
            cap = f.getbbox('T', anchor='ls')
            self.ys.append((xy + bx0, y - yl + yl + cap[1], xy + bx1, y - yl + yl + cap[3], f))
            arr = np.asarray(m, np.float32) / 255
            rgba = gold(arr, yl + cap[1], yl + cap[3], 7 * R)
            top = int(y - yl)
            self.layers.append((rgba, 0, top, x, x + total))
        # SEASON PASS: its letters as the shape of the fire
        f3 = self.f3
        text = 'SEASON PASS'
        tw = f3.getlength(text)
        fit = min(1.0, 780 * R / tw)
        if fit < 1:
            f3 = font('Cinzel-Variable.ttf', 104 * R * fit, 900)
            tw = f3.getlength(text)
        self.sp_box = int((self.w - tw) / 2 - 30 * R), int(880 * R + 40 * R), int((self.w + tw) / 2 + 30 * R), int(880 * R + 250 * R)
        x0, y0, x1, y1 = self.sp_box
        m = Image.new('L', (x1 - x0, y1 - y0), 0)
        ImageDraw.Draw(m).text((30 * R, (y1 - y0) - 40 * R), text, font=f3, fill=255, anchor='ls')
        self.sp_mask = np.asarray(m.filter(ImageFilter.GaussianBlur(0.6 * R)), np.float32) / 255
        self.sp_x = (30 * R + x0, 30 * R + x0 + tw)
        # the arrows: for each Y, a long stroke and a short one meeting it
        self.arrows = []
        for i, (bx0, by0, bx1, by1, f) in enumerate(self.ys):
            w, h = bx1 - bx0, by1 - by0
            if i == 0:     # BAYEUX: long stroke from top right to the foot; short from top left to its middle
                a0, a1 = (bx1 - 0.02 * w, by0), (bx0 + 0.52 * w, by1)
                b0 = (bx0 + 0.0 * w, by0)
            else:          # TAPESTRY: the mirror image
                a0, a1 = (bx0 + 0.02 * w, by0), (bx1 - 0.52 * w, by1)
                b0 = (bx1 - 0.0 * w, by0)
            j = (a0[0] + (a1[0] - a0[0]) * 0.50, a0[1] + (a1[1] - a0[1]) * 0.50)
            th = 0.22 * h
            self.arrows.append(dict(tail=a0, tip=a1, th=th))
            self.arrows.append(dict(tail=b0, tip=j, th=th * 0.92))
        self.arrows = [self.arrows[k] for k in (0, 1, 2, 3)]

    # -- drawing --------------------------------------------------------------------------------------
    def draw(self, a, t, t0=None, slam=None):
        """Draw the logo on frame array a at time t. t0: when the wipe starts (None = already complete)."""
        w, h = self.w, self.h
        lay = np.zeros((h, w, 4), np.float32)
        for i, (rgba, _, top, xa, xb) in enumerate(self.layers):
            ts = (T_BAYEUX, T_TAPESTRY)[i] if t0 is None else t0 + i * 0.12
            p = 1.0 if t0 is None and slam is not None else ease((t - ts) / 0.30)
            if p <= 0:
                continue
            front = xa + (xb - xa + 40 * R) * p
            sub = rgba.copy()
            cols = np.arange(w, dtype=np.float32)
            vis = np.clip((front - cols) / (24 * R), 0, 1)
            sub[..., 3] *= vis[None, :]
            hh = sub.shape[0]
            lay[top:top + hh] = blend(lay[top:top + hh], sub)
            if p < 1:   # the light at the wipe's leading edge
                edge = np.exp(-((cols - front) / (26 * R)) ** 2)[None, :] * (rgba[..., 3] > 0)
                lay[top:top + hh, :, :3] += edge[..., None] * np.array([255, 240, 200]) * 0.9
                lay[top:top + hh, :, 3] = np.maximum(lay[top:top + hh, :, 3], edge * 0.8)
        # glint passing over the metal after it lands
        if t0 is None and slam is None and 2.75 < t < 3.35:
            g = (t - 2.75) / 0.6
            yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
            band = np.exp(-(((xx + yy * 0.5) - (g * (w + h * 0.5))) / (30 * R)) ** 2)
            on = lay[..., 3] > 0.5
            lay[..., :3] += (band * on)[..., None] * np.array([255, 245, 210]) * 0.7
        shadow = ndi.gaussian_filter(lay[..., 3], 6 * R)
        sh = np.roll(np.roll(shadow, int(8 * R), 0), int(5 * R), 1)
        a *= (1 - 0.65 * sh[..., None])
        a[:] = a * (1 - lay[..., 3:4]) + np.clip(lay[..., :3], 0, 400) * lay[..., 3:4]
        # the arrows
        for k, arr in enumerate(self.arrows):
            tl = ARROWS_AT[k] if t0 is None or slam is None else t0
            if t0 is None and slam is not None:
                tl = -1
            self.arrow(a, arr, t, tl, k)
        # SEASON PASS in fire
        tsp = T_SEASON if slam is None else -1
        self.season(a, t, tsp)

    def arrow(self, a, arr, t, tl, k):
        if t < tl - 0.20:
            return
        (x0, y0), (x1, y1) = arr['tail'], arr['tip']
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        fly = max(0.0, (tl - t) / 0.20)            # 1 -> 0 as it arrives, straight along its own line
        off = (fly ** 1.4) * 1500 * R
        wob = 0.0
        if t > tl:
            wob = 0.06 * math.exp(-(t - tl) * 9) * math.sin((t - tl) * 70)
        c, s = math.cos(wob), math.sin(wob)
        ext = 0.50 * L                              # shaft runs on past the letter: fletching outside it
        th = arr['th']

        def pt(u, v):  # u along from the tip backwards, v across
            px, py = -u * ux - v * -uy, -u * uy - v * ux
            px, py = c * px - s * py, s * px + c * py
            return (x1 - ux * off + px, y1 - uy * off + py)

        h, w = a.shape[:2]
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        Ls = L + ext
        # a medieval war arrow: a plain ash shaft, a forged iron broadhead, grey goose flights, and a bundle of
        # pitch-soaked tow bound behind the head (the fire arrow)
        sw = th * 0.30
        d.polygon([pt(th * 1.3, -sw), pt(Ls, -sw), pt(Ls, sw), pt(th * 1.3, sw)],
                  fill=(178, 136, 88, 255), outline=(40, 24, 12, 255))
        d.polygon([pt(th * 1.3, -sw), pt(Ls, -sw), pt(Ls, -sw * 0.2), pt(th * 1.3, -sw * 0.2)], fill=(206, 168, 116, 255))
        # the iron broadhead: a long socket, then two barbed blades
        d.polygon([pt(th * 1.0, -sw * 1.1), pt(th * 1.9, -sw * 1.05), pt(th * 1.9, sw * 1.05), pt(th * 1.0, sw * 1.1)],
                  fill=(62, 60, 60, 255), outline=(18, 16, 16, 255))
        d.polygon([pt(-th * 0.2, 0), pt(th * 0.85, -th * 0.55), pt(th * 1.15, -th * 0.62), pt(th * 1.0, -sw),
                   pt(th * 1.0, sw), pt(th * 1.15, th * 0.62), pt(th * 0.85, th * 0.55)],
                  fill=(84, 84, 88, 255), outline=(18, 16, 16, 255))
        d.line([pt(-th * 0.15, 0), pt(th * 0.9, 0)], fill=(150, 150, 156, 255), width=max(1, int(th * 0.08)))
        # the burning tow, bound on behind the head
        d.polygon([pt(th * 1.9, -sw * 1.8), pt(th * 3.0, -sw * 1.6), pt(th * 3.0, sw * 1.6), pt(th * 1.9, sw * 1.8)],
                  fill=(46, 30, 20, 255), outline=(16, 10, 6, 255))
        for u in (2.2, 2.6):
            d.line([pt(th * u, -sw * 1.9), pt(th * u + th * 0.15, sw * 1.9)], fill=(110, 70, 30, 255),
                   width=max(1, int(th * 0.07)))
        # three grey goose flights (two seen edge-on above and below), bound with thread
        for sgn, col in ((-1, (150, 146, 140, 255)), (1, (196, 192, 184, 255))):
            d.polygon([pt(Ls - th * 2.4, sgn * sw), pt(Ls - th * 0.8, sgn * th * 0.5), pt(Ls - th * 0.15, sgn * th * 0.48),
                       pt(Ls - th * 0.3, sgn * sw)], fill=col, outline=(70, 66, 62, 255))
        for u in (Ls - th * 2.5, Ls - th * 0.2):
            d.line([pt(u, -sw * 1.1), pt(u, sw * 1.1)], fill=(120, 30, 24, 255), width=max(1, int(th * 0.12)))
        d.polygon([pt(Ls, -sw), pt(Ls + th * 0.15, -sw * 0.6), pt(Ls + th * 0.15, sw * 0.6), pt(Ls, sw)],
                  fill=(150, 112, 70, 255))
        # its fire: along the shaft, licking upwards
        src = Image.new('L', (w, h), 0)
        ds = ImageDraw.Draw(src)
        ds.line([pt(th * 1.9, 0), pt(th * 3.0, 0)], fill=255, width=max(2, int(th * 1.2)))
        ds.line([pt(th * 3.0, 0), pt(L * 0.55, 0)], fill=60, width=max(2, int(th * 0.4)))
        bx0 = int(max(0, min(pt(0, 0)[0], pt(Ls, 0)[0]) - 60 * R))
        bx1 = int(min(w, max(pt(0, 0)[0], pt(Ls, 0)[0]) + 60 * R))
        by0 = int(max(0, min(pt(0, 0)[1], pt(Ls, 0)[1]) - 150 * R))
        by1 = int(min(h, max(pt(0, 0)[1], pt(Ls, 0)[1]) + 30 * R))
        if bx1 > bx0 and by1 > by0:
            sm = np.asarray(src, np.float32)[by0:by1, bx0:bx1] / 255 * 0.9
            fl = fire(sm, t, 40 * R, seed=k + 1, lick=0.9)
            fl[..., 3] *= 0.85
            add_light(a, fl, bx0, by0)
        arr_np = np.asarray(im, np.float32)
        al = arr_np[..., 3:4] / 255
        a[:] = a * (1 - al) + arr_np[..., :3] * al
        if 0 <= t - tl < 0.25:    # the impact: a burst of sparks
            self.sparks(a, arr['tip'], t - tl, k)

    def sparks(self, a, p, dt, k):
        rng = np.random.default_rng(100 + k)
        d = ImageDraw.Draw(img := Image.new('L', (a.shape[1], a.shape[0]), 0))
        for i in range(26):
            ang = rng.uniform(-math.pi, 0.2)
            sp = rng.uniform(300, 900) * R
            x = p[0] + math.cos(ang) * sp * dt
            y = p[1] + math.sin(ang) * sp * dt + 900 * R * dt * dt
            x2 = x - math.cos(ang) * 14 * R
            y2 = y - math.sin(ang) * 14 * R
            d.line([(x2, y2), (x, y)], fill=int(255 * (1 - dt / 0.25)), width=max(1, int(3 * R)))
        g = np.asarray(img.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[..., None] / 255
        a += g * np.array([255, 200, 90])

    def season(self, a, t, ts):
        x0, y0, x1, y1 = self.sp_box
        m = self.sp_mask
        if ts >= 0:
            p = ease((t - ts) / 0.42)
            if p <= 0:
                return
            front = self.sp_x[0] - 60 * R + (self.sp_x[1] - self.sp_x[0] + 120 * R) * p
            cols = np.arange(x0, x1, dtype=np.float32)
            vis = np.clip((front - cols) / (40 * R), 0, 1)
            src = m * vis[None, :]
            burst = np.exp(-((cols - front) / (30 * R)) ** 2)[None, :] * (m > 0.2) * (p < 1)
            src = np.maximum(src, burst * 1.0)
        else:
            src = m
        # a dark backing so the burning letters read against anything
        dark = ndi.gaussian_filter(src, 7 * R)
        a[y0:y1, x0:x1] *= (1 - 0.75 * np.clip(dark * 1.8, 0, 1))[..., None]
        # flames licking up off the letters (kept out of the letters themselves, so each letter stays clear)
        fl = fire(src, t, 55 * R, seed=9, lick=1.2)
        inside = ndi.gaussian_filter(ndi.binary_dilation(src > 0.4, iterations=max(1, int(3 * R))).astype(np.float32), R)
        fl[..., 3] *= 1 - inside
        add_light(a, fl, x0, y0)
        # the letters: made of fire, orange at the edges, yellow-white at the heart, flickering
        hh, ww = src.shape
        yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
        n = noise(2, xx / R / 5 + t * 40, yy / R / 7 + t * 140)
        depth = np.clip(ndi.distance_transform_edt(src > 0.5) / (6 * R), 0, 1)
        col = fire_colour(0.50 + 0.30 * depth + 0.22 * n)
        rgba = np.dstack([col[..., :3], np.clip(src * 1.2, 0, 1)])
        over(a, rgba, x0, y0)
        glow = ndi.gaussian_filter(src, 10 * R)
        add_light(a, np.dstack([np.broadcast_to(np.array([255, 120, 20], np.float32), src.shape + (3,)), glow * 0.5]), x0, y0)


def blend(dst, src):
    a = src[..., 3:4]
    out = dst.copy()
    out[..., :3] = dst[..., :3] * (1 - a) + src[..., :3] * a
    out[..., 3:4] = dst[..., 3:4] * (1 - a) + a
    return out


# ------------------------------------------------------------------------------------------- slam text
def slam(a, text, t, t0, t1, cy, size, colour=(255, 255, 255), glow=(255, 255, 255), fontname='Anton-Regular.ttf',
         maxw=840, spacing=0, fade=0.10):
    """Trailer text: punches in big and settles, holds, then glitches out."""
    if t < t0 or t > t1:
        return
    p = (t - t0) / 0.14
    sc = 1.0 + 0.55 * (1 - ease(p)) if p < 1 else 1.0 + 0.02 * (t - t0 - 0.14)
    alpha = min(1.0, p * 1.5)
    if t1 - t < fade:
        alpha *= (t1 - t) / fade
    f = font(fontname, size * R)
    lines = wrap(text, f, maxw * R)
    while len(lines) > 2 or max(f.getlength(l) for l in lines) > maxw * R:
        size *= 0.92
        f = font(fontname, size * R)
        lines = wrap(text, f, maxw * R)
    lh = size * R * 1.02
    w, h = a.shape[1], a.shape[0]
    pad = int(size * R * 0.6)
    tw = int(max(f.getlength(l) for l in lines) + 2 * pad)
    th = int(lh * len(lines) + 2 * pad)
    im = Image.new('L', (tw, th), 0)
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        d.text((tw / 2, pad + lh * (i + 0.5)), l, font=f, fill=255, anchor='mm')
    if sc != 1.0:
        im = im.resize((max(1, int(tw * sc)), max(1, int(th * sc))), Image.BICUBIC)
    m = np.asarray(im, np.float32) / 255
    hh, ww = m.shape
    x0, y0 = int(w / 2 - ww / 2), int(cy * R - hh / 2)
    # shadow, glow, chromatic split, then the letters
    gl = ndi.gaussian_filter(m, 10 * R) * 0.8
    sh = ndi.gaussian_filter(m, 3 * R)
    rgba = np.zeros((hh, ww, 4), np.float32)
    rgba[..., :3] = 0
    rgba[..., 3] = np.clip(sh * 1.4, 0, 1) * 0.85 * alpha
    over(a, rgba, x0 + int(4 * R), y0 + int(6 * R))
    add_light(a, np.dstack([np.broadcast_to(np.array(glow, np.float32), (hh, ww, 3)), gl * 0.45 * alpha]), x0, y0)
    if p < 1.4:
        k = int((1.4 - min(p, 1.4)) * 10 * R) + 1
        for ch, dxx in ((0, -k), (2, k)):
            col = np.zeros(3, np.float32)
            col[ch] = 255
            add_light(a, np.dstack([np.broadcast_to(col, (hh, ww, 3)), m * 0.5 * alpha]), x0 + dxx, y0)
    rgba = np.dstack([np.broadcast_to(np.array(colour, np.float32), (hh, ww, 3)), m * alpha])
    over(a, rgba, x0, y0)


def wrap(text, f, maxw):
    words = text.split()
    if f.getlength(text) <= maxw or len(words) == 1:
        return [text]
    best = None
    for i in range(1, len(words)):
        l1, l2 = ' '.join(words[:i]), ' '.join(words[i:])
        m = max(f.getlength(l1), f.getlength(l2))
        if best is None or m < best[0]:
            best = (m, [l1, l2])
    return best[1]


# ------------------------------------------------------------------------------------------- the shots
STRIP = None
TITLE = None
ROOM = None


def setup():
    global STRIP, TITLE, ROOM
    if STRIP is None:
        STRIP = Strip(R * 1.45)
        TITLE = Title()
        room = gallery(Strip(0.5))
        im = Image.fromarray(room.astype(np.uint8))
        ROOM = np.asarray(im.resize((int(W0 * R * 1.12), int(H0 * R * 1.12)), Image.LANCZOS), np.float32)


def room_frame(t, dark=0.0):
    """Shot 1: the gallery, the camera creeping forward."""
    k = 1.0 + 0.10 * ease(t / CUT_TAPESTRY)
    w, h = int(W0 * R), int(H0 * R)
    big = ROOM
    bh, bw = big.shape[:2]
    cw, ch = bw / 1.12 / k * 1.0, bh / 1.12 / k
    cx, cy = bw * 0.47 + 10 * R * t, bh * 0.5
    im = Image.fromarray(big.astype(np.uint8)).resize((w, h), Image.BICUBIC,
                                                       box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
    a = np.asarray(im, np.float32)
    if dark:
        a *= 1 - dark
    return a


CAM = [  # (t, strip x, band y, zoom): where the camera looks along the tapestry
    (CUT_TAPESTRY, 640, 450, 1.00), (5.10, 760, 430, 1.06), (5.30, 830, 330, 1.26), (6.88, 880, 330, 1.32),
]


def cam_at(t):
    s = STRIP
    rx, ry = s.ref_to_design('rifle', 410, 190)
    cx, cy = s.ref_to_design('claw', 300, 128)
    gx, gy = s.ref_to_design('ghost', 330, 80)
    sx, sy = s.ref_to_design('stapler', 262, 190)
    keys = [(CUT_TAPESTRY, rx - 260, 450, 1.0), (5.12, rx - 60, 440, 1.04), (5.30, rx, ry + 40, 1.24),
            (6.86, rx + 50, ry + 40, 1.30),
            (7.06, cx, cy + 40, 1.22), (8.66, cx + 40, cy + 40, 1.28),
            (8.86, gx - 120, gy + 160, 1.0), (9.30, gx - 100, gy + 160, 1.0), (9.95, gx + 40, gy + 150, 1.02),
            (10.86, gx + 70, gy + 150, 1.04),
            (11.06, sx - 140, sy + 120, 1.0), (12.06, sx - 40, sy + 60, 1.16), (12.14, sx + 10, sy - 20, 1.9)]
    keys = [(k[0] + D,) + k[1:] if k[0] > CUT_TAPESTRY - D + 0.01 else k for k in keys]
    keys[0] = (CUT_TAPESTRY,) + keys[0][1:]
    mx, my = s.ref_to_design('stapler', 345, 175)
    keys += [(STAPLER_FADE, sx + 30, sy - 20, 2.0), (STAPLER_CLICK - 0.1, mx, my, 1.55), (CUT_END_TITLE, mx + 10, my, 1.57)]
    return keyed(t, [(k[0],) + tuple(k[1:]) for k in keys])


WHIPS = [(6.86 + D, 7.06 + D), (8.66 + D, 8.86 + D), (10.86 + D, 11.06 + D)]


def tapestry_frame(t, fi):
    s = STRIP
    x, y, z = cam_at(t)
    w, h = int(W0 * R), int(H0 * R)
    states = {}
    for name, ts in SWAPS.items():
        if t >= ts:
            states[name] = 'after'
    if t >= SWAPS['ghost']:
        gp = ease((t - GHOST_FLY[0]) / (GHOST_FLY[1] - GHOST_FLY[0]))
        states['ghost'] = ghost_state(gp)
    view_w = W0 / z
    x0, x1 = x - view_w / 2 - 2, x + view_w / 2 + 2
    win = s.window(x0, x1, states)
    k = s.k
    # band: its top on screen
    band_h = HB * z * R
    top = (BAND_Y - (y - HB / 2) * z - HB / 2 * z) * R if False else (BAND_Y - y * z) * R + 0
    top = BAND_Y * R - (y - HB / 2) * z * R - band_h / 2
    a = np.zeros((h, w, 3), np.float32)
    case_background(a, top, band_h, t)
    bx = (x - view_w / 2 - x0) * k
    im = Image.fromarray(np.clip(win, 0, 255).astype(np.uint8))
    band = im.resize((w, max(1, int(round(band_h)))), Image.BICUBIC, box=(bx, 0, bx + view_w * k, win.shape[0]))
    b = np.asarray(band, np.float32)
    for wa, wb in WHIPS:     # whip pans: a fast smear sideways
        if wa < t < wb:
            amt = math.sin(math.pi * (t - wa) / (wb - wa))
            b = ndi.uniform_filter1d(b, max(1, int(160 * R * amt)), axis=1)
    # lit softly from above
    yy = np.linspace(0, 1, b.shape[0], dtype=np.float32)[:, None, None]
    b *= 1.04 - 0.16 * yy
    t0 = int(round(top))
    ya, yb = max(0, t0), min(h, t0 + b.shape[0])
    if yb > ya:
        a[ya:yb] = b[ya - t0:yb - t0]
    # glows that belong to the trailer, over the wool
    effects(a, t, x, y, z, top)
    # glass: a long soft reflection drifting across
    yy2, xx2 = np.mgrid[0:h, 0:w].astype(np.float32)
    refl = np.exp(-(((xx2 - yy2 * 0.35) - (w * 0.2 + (t - CUT_TAPESTRY) * 60 * R - x * 0.08 * R)) / (60 * R)) ** 2)
    a += refl[..., None] * 14
    return a


def ghost_state(p):
    def f(ims):
        before, after = ims['pistol'], ims['after']
        if p >= 1:
            return after
        w = after.shape[1]
        # the ghost streams out from the muzzle: reveal everything new from the muzzle rightwards
        mx = STRIP.ref_scale['ghost'] * 255 * STRIP.k
        front = mx + (w - mx) * p
        cols = np.arange(w, dtype=np.float32)
        vis = np.clip((front - cols) / (30 * STRIP.k), 0, 1)[None, :, None]
        return before * (1 - vis) + after * vis
    return f


def case_background(a, top, band_h, t):
    """Around the band: the dark case, its lit top edge, its wooden ledge below, the gallery's dark."""
    h, w = a.shape[:2]
    a[:] = np.array([16, 13, 12], np.float32)
    yy = np.arange(h, dtype=np.float32)[:, None]
    t0, t1 = top, top + band_h
    up = np.clip(1 - (t0 - yy) / (220 * R), 0, 1) * (yy < t0)
    a += (up ** 2 * 26)[..., None] * np.array([1.0, 0.85, 0.65])[None, None]
    lit = np.exp(-((yy - (t0 - 26 * R)) / (5 * R)) ** 2)
    a += (lit * 230)[..., None] * np.array([1.0, 0.93, 0.8])[None, None]
    ledge = (yy > t1 + 18 * R) & (yy < t1 + 90 * R)
    a[np.broadcast_to(ledge, a.shape[:2])] = np.array([44, 32, 24])
    edge = np.exp(-((yy - (t1 + 20 * R)) / (3 * R)) ** 2)
    a += (edge * 90)[..., None] * np.array([1.0, 0.85, 0.6])[None, None]


def effects(a, t, x, y, z, top):
    """Trailer light over the stitches: the rifle's plasma glow, the claw's cold mist, the stapler's aura."""
    s = STRIP
    h, w = a.shape[:2]

    def to_screen(name, rx, ry):
        dx, dy = s.ref_to_design(name, rx, ry)
        return (W0 / 2 + (dx - x) * z) * R, top + dy * z * R

    if t >= SWAPS['rifle'] and t < NAME_OUT['rifle'] + 0.2:
        px, py = to_screen('rifle', 400, 125)
        pulse = 0.75 + 0.25 * math.sin(t * 9)
        glow_blob(a, px, py, 360 * R * z, 120 * R * z, (90, 255, 80), 0.55 * pulse, ang=-0.29)
        if t - SWAPS['rifle'] < 0.4:
            glow_blob(a, px, py, 600 * R * z, 200 * R * z, (150, 255, 140), 0.9 * (1 - (t - SWAPS['rifle']) / 0.4), ang=-0.29)
    if t >= SWAPS['claw'] and t < NAME_OUT['claw'] + 0.2:
        px, py = to_screen('claw', 262, 124)
        mist(a, px, py, 260 * R * z, t)
        glow_blob(a, px, py, 200 * R * z, 140 * R * z, (160, 220, 255), 0.35)
    if t >= SWAPS['ghost'] and t < NAME_OUT['ghost'] + 0.2:
        gp = ease((t - GHOST_FLY[0]) / (GHOST_FLY[1] - GHOST_FLY[0]))
        if gp > 0:
            px, py = to_screen('ghost', 255 + 300 * gp, 80)
            glow_blob(a, px, py, 260 * R * z, 120 * R * z, (220, 240, 255), 0.35 * gp)
    if t >= SWAPS['stapler']:
        staple(a, t, to_screen, z)
    if t >= SWAPS['stapler'] and t < NAME_OUT['stapler'] + 0.2:
        px, py = to_screen('stapler', 284, 158)
        dt = t - SWAPS['stapler']
        fade = 1 - ease((t - STAPLER_FADE) / 0.45)
        if fade > 0:
            rays(a, px, py, t, 0.9 * fade * min(1, dt / 0.15) * (0.7 + 0.3 * math.exp(-dt * 3)))
            glow_blob(a, px, py, 180 * R * z, 90 * R * z, (255, 210, 120), 0.55 * fade)
        if dt < 0.35:
            glow_blob(a, px, py, 900 * R, 900 * R, (255, 240, 200), 1.6 * (1 - dt / 0.35))


def staple(a, t, to_screen, z):
    """One single staple, fired flat across at the messenger, where it stays."""
    if t < STAPLER_CLICK:
        return
    p = min(1.0, (t - STAPLER_CLICK) / (STAPLE_HIT - STAPLER_CLICK))
    x0, y0 = 318, 158            # the stapler's mouth (reference pixels)
    x1, y1 = 362, 165            # the messenger's forearm, just behind his pointing hand
    x, y = to_screen('stapler', x0 + (x1 - x0) * p, y0 + (y1 - y0) * p)
    s = 13.0 * z * R             # a staple, flying legs-first: about 6 reference pixels across
    im = Image.new('RGBA', (a.shape[1], a.shape[0]), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    leg = s * 0.9 if p < 1 else s * 0.25     # stuck in: the legs bitten into his arm, only the crown shows
    pts = [(x + leg, y - s * 0.55), (x, y - s * 0.55), (x, y + s * 0.55), (x + leg, y + s * 0.55)]
    if p < 1:                    # a faint streak behind it in flight
        d.line([(x - s * 6, y - s * 0.4), (x - s * 1.5, y - s * 0.4)], fill=(120, 120, 126, 110), width=max(1, int(z * R)))
    d.line(pts, fill=(20, 20, 24, 255), width=max(3, int(4.5 * z * R)))
    d.line(pts, fill=(196, 200, 206, 255), width=max(1, int(2.2 * z * R)))
    m = np.asarray(im, np.float32)
    al = m[..., 3:4] / 255
    a[:] = a * (1 - al) + m[..., :3] * al


def glow_blob(a, cx, cy, rx, ry, col, amt, ang=0.0):
    h, w = a.shape[:2]
    x0, x1 = int(max(0, cx - rx * 1.6)), int(min(w, cx + rx * 1.6))
    y0, y1 = int(max(0, cy - rx * 1.6)), int(min(h, cy + rx * 1.6))
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    c, s = math.cos(ang), math.sin(ang)
    u, v = (xx - cx) * c + (yy - cy) * s, -(xx - cx) * s + (yy - cy) * c
    g = np.exp(-((u / rx) ** 2 + (v / ry) ** 2) * 2.2)
    a[y0:y1, x0:x1] += g[..., None] * np.array(col, np.float32) * amt


def mist(a, cx, cy, r, t):
    h, w = a.shape[:2]
    x0, x1 = int(max(0, cx - r * 1.5)), int(min(w, cx + r * 1.5))
    y0, y1 = int(max(0, cy - r * 1.2)), int(min(h, cy + r * 1.5))
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    n = noise(0, (xx / R) / 14 + t * 6, (yy / R) / 14 - t * 3)
    n2 = noise(1, (xx / R) / 7 - t * 9, (yy / R) / 9)
    fall = np.exp(-(((xx - cx) / r) ** 2 + ((yy - cy) / (r * 0.9)) ** 2) * 1.6)
    m = np.clip(n * 0.7 + n2 * 0.5 - 0.45, 0, 1) * fall
    a[y0:y1, x0:x1] += m[..., None] * np.array([200, 230, 255], np.float32) * 0.8


def rays(a, cx, cy, t, amt):
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ang = np.arctan2(yy - cy, xx - cx)
    r = np.hypot(xx - cx, yy - cy)
    beams = np.clip(np.sin(ang * 9 + t * 0.8) * 0.5 + 0.5, 0, 1) ** 6
    fall = np.exp(-r / (520 * R))
    a += (beams * fall * amt)[..., None] * np.array([255, 222, 150], np.float32) * 0.6


def glitch(a, fi, amt):
    """A digital glitch: slices shoved sideways, colours split, a flash of noise."""
    h, w = a.shape[:2]
    rng = np.random.default_rng(fi * 7 + 3)
    out = a.copy()
    for _ in range(int(6 + 10 * amt)):
        y0 = rng.integers(0, h)
        hh = int(rng.integers(4, 60) * R) + 1
        dx = int(rng.normal(0, 80 * R * amt))
        out[y0:y0 + hh] = np.roll(a[y0:y0 + hh], dx, axis=1)
    k = int(14 * R * amt) + 1
    out[..., 0] = np.roll(out[..., 0], k, axis=1)
    out[..., 2] = np.roll(out[..., 2], -k, axis=1)
    out += rng.normal(0, 18 * amt, (h, 1, 1)).astype(np.float32)
    return out


def frame(t, fi=0):
    setup()
    w, h = int(W0 * R), int(H0 * R)
    if t >= BLACK_AT:
        return np.zeros((h, w, 3), np.uint8)
    shake = (0.0, 0.0)
    if t < CUT_TAPESTRY:
        a = room_frame(t)
        # INTRODUCING, then the logo
        slam(a, 'INTRODUCING', t, T_INTRO, T_BAYEUX + 0.05, 520, 66, colour=(236, 228, 210), glow=(255, 220, 160),
             fontname='Cinzel-Variable.ttf')
        TITLE.draw(a, t)
        for tl in ARROWS_AT:
            if 0 <= t - tl < 0.12:
                shake = (math.sin(t * 190) * 9 * R, math.cos(t * 170) * 7 * R)
    elif t < CUT_END_TITLE:
        a = tapestry_frame(t, fi)
        slam(a, 'NEW WEAPONS', t, T_NEW, SWAPS['rifle'] - 0.12, 800, 190, glow=(255, 230, 170))
        for name, ts in SWAPS.items():
            col = {'rifle': (120, 255, 100), 'claw': (170, 225, 255), 'ghost': (235, 240, 255), 'stapler': (255, 214, 120)}[name]
            slam(a, NAMES[name], t, ts + 0.06, NAME_OUT[name] - 0.02, 1370, 118, glow=col,
                 fade=0.45 if name == 'stapler' else 0.10)
        if abs(t - SWAPS['stapler']) < 0.1:
            shake = (math.sin(t * 210) * 14 * R, math.cos(t * 180) * 10 * R)
    else:
        a = room_frame(CUT_TAPESTRY, dark=0.45)
        p = ease((t - CUT_END_TITLE) / 0.12)
        TITLE.draw(a, t, slam=True)
        if t - CUT_END_TITLE < 0.18:
            a += (1 - (t - CUT_END_TITLE) / 0.18) * 160
            shake = (math.sin(t * 200) * 12 * R, 0.0)
    # glitches on the cuts and the swaps
    for tg, dur in [(CUT_TAPESTRY, 0.16), (CUT_END_TITLE, 0.10)] + [(ts, 0.14) for ts in SWAPS.values()]:
        if tg - dur * 0.5 <= t < tg + dur * 0.5:
            a = glitch(a, fi, 1 - abs(t - tg) / (dur * 0.5))
            if abs(t - tg) < 1.0 / FPS:
                a += 70
    if shake != (0.0, 0.0):
        a = np.roll(np.roll(a, int(shake[1]), 0), int(shake[0]), 1)
    # a filmic finish: slight vignette
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    v = 1 - 0.28 * (((xx - w / 2) / (w * 0.75)) ** 2 + ((yy - h / 2) / (h * 0.62)) ** 2)
    a *= v[..., None]
    return np.clip(a, 0, 255).astype(np.uint8)


# --------------------------------------------------------------------------------------------- the sound
SR = 48000


def tone_env(n, a, d):
    e = np.ones(n)
    ka, kd = int(a * SR), int(d * SR)
    if ka:
        e[:ka] = np.linspace(0, 1, ka)
    if kd:
        e[-kd:] *= np.linspace(1, 0, kd)
    return e


def boom(big=1.0):
    """A trailer hit: a sub drop, a body thump, a crack of noise, and an upper layer phones can play."""
    n = int(2.6 * SR)
    t = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t * 7)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)
    body = np.tanh(2.5 * np.sin(2 * np.pi * np.cumsum(55 + 120 * np.exp(-t * 18)) / SR)) * np.exp(-t * 6)
    rng = np.random.default_rng(5)
    crack = rng.standard_normal(n) * np.exp(-t * 30)
    from scipy.signal import butter, sosfilt
    crack = sosfilt(butter(2, [400, 5000], 'band', fs=SR, output='sos'), crack)
    upper = np.sin(2 * np.pi * 110 * t) * np.exp(-t * 4) * 0.4 + np.sin(2 * np.pi * 220 * t) * np.exp(-t * 6) * 0.2
    x = 0.9 * sub + 0.55 * body + 0.35 * crack + 0.5 * upper
    x[:48] *= np.linspace(0, 1, 48)
    return x * big


def whoosh(d=0.45, rise=True, seed=1):
    from scipy.signal import butter, sosfilt
    n = int(d * SR)
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    steps = 24
    for i in range(steps):
        a, b = i * n // steps, (i + 1) * n // steps
        f = 300 + 4000 * (i / steps if rise else 1 - i / steps)
        out[a:b] = sosfilt(butter(2, [f * 0.6, min(f * 1.6, 20000)], 'band', fs=SR, output='sos'), x[a:b])
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    return out * env


def thunk(seed=0):
    """An arrow biting into wood: a short knock and a twang."""
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(seed + 20)
    knock = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 40) + 0.4 * rng.standard_normal(n) * np.exp(-t * 90)
    twang = np.sin(2 * np.pi * (330 + 20 * seed) * t) * np.exp(-t * 9) * (1 + 0.5 * np.sin(2 * np.pi * 18 * t)) * 0.35
    return knock + twang


def roar(d, seed=4):
    """Fire: a low rumble and crackles."""
    from scipy.signal import butter, sosfilt
    n = int(d * SR)
    rng = np.random.default_rng(seed)
    x = sosfilt(butter(2, [80, 900], 'band', fs=SR, output='sos'), rng.standard_normal(n))
    x *= 0.6 + 0.4 * np.abs(np.sin(np.linspace(0, 25, n)))
    cr = np.zeros(n)
    for i in rng.integers(0, n - 400, int(d * 40)):
        cr[i:i + 300] += rng.standard_normal(300) * np.exp(-np.arange(300) / 40) * rng.uniform(0.2, 1)
    cr = sosfilt(butter(2, 1500, 'high', fs=SR, output='sos'), cr)
    return x * 0.6 + cr * 0.35


def drone(n):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for f, g in ((36.7, 1.0), (55.0, 0.6), (73.4, 0.4), (110.0, 0.18), (146.8, 0.08)):
        out += g * np.sin(2 * np.pi * f * t + np.sin(2 * np.pi * 0.2 * t) * 0.5)
    return out


def riser(d):
    from scipy.signal import butter, sosfilt
    n = int(d * SR)
    t = np.arange(n) / SR
    f = 120 * (2 ** (t / d * 3))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
    rng = np.random.default_rng(7)
    nz = sosfilt(butter(2, 2000, 'high', fs=SR, output='sos'), rng.standard_normal(n))
    env = (t / d) ** 2
    return (tone * 0.4 + nz * 0.5) * env


def ghost_wooo(d=1.1):
    """A faint silly 'woooooo': a sliding hollow tone with wobble."""
    from scipy.signal import butter, sosfilt
    n = int(d * SR)
    t = np.arange(n) / SR
    f = 330 + 110 * np.sin(np.pi * t / d) - 60 * t / d + 14 * np.sin(2 * np.pi * 6 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sign(np.sin(ph)) * 0.3 + np.sin(ph)
    x = sosfilt(butter(2, [250, 900], 'band', fs=SR, output='sos'), x)
    rng = np.random.default_rng(9)
    x += 0.15 * sosfilt(butter(2, [400, 1200], 'band', fs=SR, output='sos'), rng.standard_normal(n))
    return x * np.sin(np.pi * t / d) ** 0.7


def click():
    """The stapler: one small, flat click."""
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(3)
    x = rng.standard_normal(n) * np.exp(-t * 400) + 0.6 * np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 300)
    x += 0.5 * rng.standard_normal(n) * np.exp(-(t - 0.035).clip(0) * 500) * (t > 0.035)
    return x


def tink():
    """The staple landing: a tiny, high, thin tick."""
    n = int(0.08 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 5200 * t) * np.exp(-t * 120) + 0.3 * np.sin(2 * np.pi * 7900 * t) * np.exp(-t * 200)


def glitch_snd(d=0.18, seed=2):
    n = int(d * SR)
    rng = np.random.default_rng(seed)
    x = np.zeros(n)
    i = 0
    while i < n:
        k = int(rng.uniform(0.008, 0.03) * SR)
        f = rng.uniform(200, 3000)
        x[i:i + k] = np.sign(np.sin(2 * np.pi * f * np.arange(min(k, n - i)) / SR)) * rng.uniform(0.2, 0.7)
        i += k
    return x


def place(mix, s, at, g):
    i = int(at * SR)
    j = min(len(mix), i + len(s))
    if i < len(mix) and j > i:
        mix[i:j] += s[:j - i] * g


def soundtrack():
    import mossad_audio as MA
    from mossad import limiter
    n = int(DUR * SR)
    mix = np.zeros(n)
    end = int(BLACK_AT * SR)
    # the drone under everything, swelling into the title and again into the stapler
    dr = drone(end)
    tt = np.arange(end) / SR
    env = 0.35 + 0.4 * np.clip(tt / 2.0, 0, 1)
    mix[:end] += 0.16 * dr * env
    place(mix, boom(0.7), T_INTRO - 0.01, 0.55)
    place(mix, whoosh(0.5, True, 1), T_BAYEUX - 0.30, 0.35)
    place(mix, boom(), T_BAYEUX, 0.7)
    place(mix, boom(0.8), T_TAPESTRY, 0.6)
    for k, tl in enumerate(ARROWS_AT):
        place(mix, whoosh(0.22, False, 10 + k), tl - 0.21, 0.35)
        place(mix, thunk(k), tl, 0.55)
    place(mix, whoosh(0.55, True, 3), T_SEASON - 0.15, 0.4)
    place(mix, boom(1.1), T_SEASON, 0.75)
    r = roar(CUT_TAPESTRY - T_SEASON)
    r[:int(0.1 * SR)] *= np.linspace(0, 1, int(0.1 * SR))
    r[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    place(mix, r, T_SEASON, 0.22)
    place(mix, glitch_snd(0.2, 1), CUT_TAPESTRY - 0.08, 0.3)
    place(mix, boom(1.0), T_NEW, 0.8)
    # a driving pulse under the weapons
    for b in np.arange(T_NEW + 0.5, SWAPS['stapler'] - 1.2, 0.5):
        place(mix, boom(0.35)[:int(0.4 * SR)] * np.linspace(1, 0, int(0.4 * SR)), b, 0.35)
    for name, ts in SWAPS.items():
        place(mix, whoosh(0.35, True, 20 + len(name)), ts - 0.33, 0.3)
        place(mix, glitch_snd(0.14, len(name)), ts - 0.07, 0.25)
        place(mix, boom(1.3 if name == 'stapler' else 1.0), ts, 0.8 if name != 'stapler' else 0.95)
    for wa, wb in WHIPS:
        place(mix, whoosh(wb - wa + 0.1, True, 40), wa - 0.05, 0.4)
    place(mix, ghost_wooo(1.2), GHOST_FLY[0] + 0.05, 0.12)
    place(mix, riser(SWAPS['stapler'] - 11.0 - D), 11.0 + D, 0.35)
    # after the stapler's huge reveal everything drops out for one small flat click
    a, b = int(STAPLER_FADE * SR), int((CUT_END_TITLE - 0.02) * SR)
    k = int(0.45 * SR)
    fade = np.ones(b - a)
    fade[:k] = np.linspace(1, 0, k)
    fade[k:] = 0
    mix[a:b] *= fade
    place(mix, click(), STAPLER_CLICK, 0.5)
    place(mix, tink(), STAPLE_HIT, 0.18)
    place(mix, boom(1.3), CUT_END_TITLE, 0.95)
    place(mix, roar(BLACK_AT - CUT_END_TITLE, 6), CUT_END_TITLE, 0.2)
    k = int(0.005 * SR)
    mix[end - k:end] *= np.linspace(1, 0, k)
    mix[end:] = 0
    for _ in range(3):
        mix *= 10 ** ((-14.0 - MA.lufs(mix[:end])) / 20)
        mix = limiter(mix, -2.8)
    return mix


# --------------------------------------------------------------------------------------------- rendering
def _render(i):
    return frame(i / FPS, i).tobytes()


def render(out):
    import imageio_ffmpeg
    import time
    from multiprocessing import Pool
    import mossad_audio as MA
    t0 = time.time()
    setup()
    wav = out + '.wav'
    mix = soundtrack()
    print(f'sound: {MA.lufs(mix[:int(BLACK_AT * SR)]):.1f} LUFS, peak {MA.true_peak_db(mix):.1f} dBTP', flush=True)
    MA.write_wav(wav, mix)
    n = int(round(DUR * FPS))
    w, h = int(W0 * R), int(H0 * R)
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt',
                          'rgb24', '-s', f'{w}x{h}', '-r', str(FPS), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', '20', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for f, fr in enumerate(pool.imap(_render, range(n), chunksize=2)):
            p.stdin.write(fr)
            if f % 48 == 0:
                print(f'frame {f}/{n}  {time.time() - t0:.0f}s', flush=True)
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print(f'done: {out} ({os.path.getsize(out) / 1e6:.1f} MB) in {time.time() - t0:.0f}s', flush=True)


def main():
    global R
    cmd = sys.argv[1]
    if cmd == 'times':
        for k, v in list(globals().items()):
            if k.isupper() and isinstance(v, (float, dict, list, tuple)) and k not in ('FIRE_STOPS', 'NOISE', 'CAM', 'REF_H'):
                print(k, v)
    elif cmd == 'stills':
        R = float(os.environ.get('BX_R', '1.0'))
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for t in sys.argv[3:]:
            Image.fromarray(frame(float(t), int(float(t) * FPS))).save(os.path.join(out, f'still-{float(t):05.2f}.png'))
    elif cmd == 'animatic':
        R = 0.5
        render(sys.argv[2])
    elif cmd == 'final':
        R = 1.0
        render(sys.argv[2])


if __name__ == '__main__':
    main()
