"""The Bayeux Tapestry Season Pass: the tapestry, stitched in code.

Sam's reference photographs are traced into the tapestry's own small palette of wools (one colour per area,
like the real embroidery), then every area is re-stitched in code: laid-and-couched fills (long parallel
threads held down by cross stitches), stem-stitch lines, and the linen ground with its weave. No pixel of a
photograph reaches the film; only the traced colour areas do.

    python3 bayeux_stitch.py trace OUT_DIR      the traced colour maps, flat, for checking
    python3 bayeux_stitch.py panels OUT_DIR     every panel stitched, before and after its weapon swap
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '..', 'references', 'bayeux')

# The wools. Index 0 is the linen ground. Colours as they look under the gallery's soft light.
WOOL = {
    'linen': (226, 214, 186),
    'ochre': (196, 152, 74),
    'buff': (204, 182, 136),
    'terracotta': (148, 58, 42),
    'madder': (100, 40, 34),     # the darker red-brown
    'sage': (128, 134, 92),
    'bluegreen': (58, 98, 94),
    'navy': (38, 48, 74),
    'black': (36, 32, 32),
    'mail': (222, 214, 192),     # a mail coat: rings stitched over a pale ground
    # the season pass wools: new colours, the same stitches
    'plasma': (96, 214, 74),
    'plasmapale': (190, 246, 160),
    'ice': (160, 206, 228),
    'frost': (236, 244, 246),
    'steel': (112, 118, 124),
    'pistol': (24, 24, 28),
    'ghost': (240, 238, 228),
}
NAMES = list(WOOL)
IDX = {n: i for i, n in enumerate(NAMES)}
RGB = np.array([WOOL[n] for n in NAMES], np.float32)
TAPESTRY = ['linen', 'ochre', 'buff', 'terracotta', 'madder', 'sage', 'bluegreen', 'navy', 'black', 'mail']
RING = (52, 88, 92)   # the mail rings' wool

# How each reference's colours map onto the wools: per photograph, its own measured colour for each wool it
# uses (the photos differ in light and white balance). Measured by sampling each reference.
PROTO = {
    'rifle': {'linen': [(241, 237, 218), (231, 224, 201), (214, 205, 182)], 'ochre': [(189, 160, 119), (162, 124, 84)],
              'terracotta': [(126, 77, 52)], 'madder': [(84, 34, 19)], 'navy': [(20, 19, 25), (40, 45, 62)],
              'black': [(62, 62, 64)], 'buff': [(114, 113, 106)]},
    'claw': {'linen': [(252, 231, 204), (254, 247, 225), (234, 210, 182), (201, 178, 154)],
             'terracotta': [(144, 100, 82)], 'madder': [(116, 79, 62)], 'buff': [(185, 153, 123)],
             'ochre': [(226, 187, 144)], 'bluegreen': [(48, 76, 82)], 'black': [(64, 54, 42)],
             'navy': [(85, 92, 89)], 'sage': [(162, 128, 104)]},
    'ghost': {'linen': [(253, 220, 166), (254, 237, 190), (254, 252, 223), (224, 188, 151)],
              'madder': [(111, 54, 38), (118, 85, 70)], 'black': [(59, 26, 13)], 'terracotta': [(150, 86, 57)],
              'ochre': [(184, 123, 70)], 'buff': [(198, 154, 114)], 'sage': [(155, 121, 97)], 'navy': [(55, 50, 53)]},
    'stapler': {'linen': [(228, 226, 229), (243, 241, 245), (208, 205, 207), (179, 172, 174)],
                'madder': [(100, 82, 86)], 'navy': [(57, 61, 71)], 'bluegreen': [(119, 109, 112), (145, 138, 142)],
                'terracotta': [(154, 92, 89), (169, 126, 114)], 'ochre': [(200, 151, 132), (231, 193, 162)]},
}
FILES = {'rifle': 'weapon-1-plasma-longshot-rifle.jpg', 'claw': 'weapon-2-ice-claw-wider.jpg',
         'ghost': 'weapon-3-ghost-pistol.jpg', 'stapler': 'weapon-4-stapler.jpg'}


def find_mail(lab, ring_area=40, density=0.16):
    """Mail coats are drawn as many small rings on the pale ground: find where small specks crowd together."""
    specks = np.zeros(lab.shape, bool)
    for k in np.unique(lab):
        if k == IDX['linen']:
            continue
        comp, n = ndi.label(lab == k)
        area = ndi.sum(np.ones_like(comp), comp, np.arange(1, n + 1))
        specks |= np.concatenate([[False], area < ring_area])[comp]
    dens = ndi.uniform_filter(specks.astype(np.float32), 9)
    m = dens > density
    m = ndi.binary_closing(m, np.ones((5, 5)))
    m = ndi.binary_fill_holes(m)
    m = ndi.binary_opening(m, np.ones((3, 3)))
    comp, n = ndi.label(m)
    area = ndi.sum(np.ones_like(comp), comp, np.arange(1, n + 1))
    m = np.concatenate([[False], area > 120])[comp]
    return m & ((lab == IDX['linen']) | specks)


def trace(name, s=2.5):
    """The reference traced into wools at s times its size. Enlarged smoothly and sharpened first, so the
    thin outlines and the small mail rings survive; then only a gentle clean."""
    a = flatten_light(load_ref(FILES[name]))
    im = Image.fromarray(a.astype(np.uint8))
    im = im.resize((int(round(im.width * s)), int(round(im.height * s))), Image.BICUBIC)
    im = im.filter(ImageFilter.UnsharpMask(radius=s * 1.2, percent=160, threshold=2))
    lab = classify(np.asarray(im, np.float32), PROTO[name])
    lab = mode_filter(lab, 3)
    lab = remove_specks(lab, int(3 * s * s))
    return mode_filter(lab, 3)


def load_ref(name):
    return np.asarray(Image.open(os.path.join(REF, name)).convert('RGB'), np.float32)


def flatten_light(a, size=61):
    """Even out the lighting: divide by a smooth estimate of the linen's brightness."""
    lum = a.mean(2)
    bright = ndi.maximum_filter(ndi.percentile_filter(lum[::2, ::2], 70, size=size // 2), size // 4)
    bright = ndi.gaussian_filter(bright, size / 6)
    bright = np.array(Image.fromarray(bright).resize((a.shape[1], a.shape[0]), Image.BILINEAR))
    return np.clip(a * (235.0 / np.maximum(bright, 40))[..., None], 0, 255)


def classify(a, protos):
    """Each pixel -> the wool whose sampled colour it is nearest (chroma counts more than brightness)."""
    names, cols = [], []
    for n, cs in protos.items():
        for c in cs:
            names.append(IDX[n])
            cols.append(c)
    cols = np.array(cols, np.float32)
    w = np.array([0.8, 1.2, 1.0], np.float32)

    def opp(x):  # a simple opponent space: brightness, red-green, yellow-blue
        r, g, b = x[..., 0], x[..., 1], x[..., 2]
        return np.stack([(r + g + b) / 3, (r - g) * 1.2, (r + g) / 2 - b], -1) * w

    d = ((opp(a)[:, :, None, :] - opp(cols)[None, None]) ** 2).sum(-1)
    return np.array(names)[d.argmin(-1)]


def mode_filter(lab, size=3, n=len(NAMES)):
    """Majority vote in a small window: removes speckle, keeps edges."""
    best = np.zeros(lab.shape, np.float32) - 1
    out = lab.copy()
    for k in np.unique(lab):
        c = ndi.uniform_filter((lab == k).astype(np.float32), size)
        m = c > best
        out[m] = k
        best[m] = c[m]
    return out


def remove_specks(lab, min_area):
    """Areas smaller than min_area (pixels) are stray specks of the photo: give them to their neighbours."""
    mask = np.zeros(lab.shape, bool)
    for k in np.unique(lab):
        comp, n = ndi.label(lab == k)
        if n == 0:
            continue
        area = ndi.sum(np.ones_like(comp), comp, np.arange(1, n + 1))
        small = np.concatenate([[False], area < min_area])
        mask |= small[comp]
    return fill_from_neighbours(lab, mask) if mask.any() else lab


def clean(lab, min_area=14):
    lab = mode_filter(lab, 3)
    lab = remove_specks(lab, min_area)
    return mode_filter(lab, 3)


def upscale_labels(lab, s, smooth=1.2):
    """Bigger, with smooth boundaries: each wool's area blurred and the strongest wins."""
    H, W = lab.shape
    nh, nw = int(round(H * s)), int(round(W * s))
    best = np.full((nh, nw), -1.0, np.float32)
    out = np.zeros((nh, nw), np.int16)
    for k in np.unique(lab):
        m = Image.fromarray(((lab == k) * 255).astype(np.uint8)).resize((nw, nh), Image.BILINEAR)
        m = ndi.gaussian_filter(np.asarray(m, np.float32), smooth * s * 0.5)
        sel = m > best
        out[sel] = k
        best[sel] = m[sel]
    return out


def fill_from_neighbours(lab, mask, exclude=()):
    """Erase what is under the mask: every masked pixel takes the wool of the nearest unmasked pixel
    (the linen, the tunic or the horse the weapon crossed), so nothing of it is left."""
    keep = ~mask
    for e in exclude:
        keep &= lab != IDX[e]
    _, (iy, ix) = ndi.distance_transform_edt(~keep, return_indices=True)
    out = lab.copy()
    out[mask] = lab[iy[mask], ix[mask]]
    return out


# ------------------------------------------------------------------------------------------- the stitching
def _hash(*a):
    h = np.zeros_like(a[0], dtype=np.uint32)
    for i, v in enumerate(a):
        h ^= (v.astype(np.int64).astype(np.uint32) + np.uint32(0x9E3779B9) + (h << 6) + (h >> 2)) * np.uint32(2654435761 + i)
    return (h & 0xFFFF).astype(np.float32) / 65535.0


def direction_map(lab, forced=None):
    """The thread direction in every area: along the long axis of each connected area (laid work), or as
    forced for a drawn weapon part."""
    ang = np.zeros(lab.shape, np.float32)
    for k in np.unique(lab):
        if k == IDX['linen']:
            continue
        comp, n = ndi.label(lab == k)
        if n == 0:
            continue
        idx = np.arange(1, n + 1)
        yy, xx = np.mgrid[0:lab.shape[0], 0:lab.shape[1]]
        cnt = ndi.sum(np.ones_like(comp), comp, idx)
        mx, my = ndi.sum(xx, comp, idx) / cnt, ndi.sum(yy, comp, idx) / cnt
        sxx = ndi.sum(xx * xx, comp, idx) / cnt - mx * mx
        syy = ndi.sum(yy * yy, comp, idx) / cnt - my * my
        sxy = ndi.sum(xx * yy, comp, idx) / cnt - mx * my
        a = 0.5 * np.arctan2(2 * sxy, sxx - syy)
        lut = np.concatenate([[0], a]).astype(np.float32)
        ang[comp > 0] = lut[comp[comp > 0]]
    if forced is not None:
        m = ~np.isnan(forced)
        ang[m] = forced[m]
    return ang


def stitch(lab, scale=3.0, forced=None, seed=0):
    """Render a wool map as embroidery. `scale` is pixels per thread width (about)."""
    H, W = lab.shape
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = RGB[lab]
    linen = lab == IDX['linen']

    # the linen: a plain weave (tiny over-under grid), slubs in the thread, faint horizontal creases
    p = max(2.0, scale * 0.9)
    wx, wy = np.sin(xx * np.pi / p), np.sin(yy * np.pi / p)
    weave = 0.5 + 0.5 * np.sign(wx * wy) * np.minimum(np.abs(wx), np.abs(wy)) ** 0.5
    rng = np.random.default_rng(seed)
    slub = ndi.gaussian_filter(rng.standard_normal((H, W)).astype(np.float32), (0.6, scale * 4))
    slub /= slub.std() + 1e-6
    crease = ndi.gaussian_filter(rng.standard_normal((H, 1)).astype(np.float32), (scale * 6, 0))
    crease = np.repeat(crease / (crease.std() + 1e-6), W, 1)
    lin_shade = 1.0 + 0.045 * (weave - 0.5) + 0.02 * slub + 0.012 * crease

    # the laid-and-couched fills: threads side by side along the area's direction, each thread a little
    # different, held down by couching stitches across them every few thread widths
    ang = direction_map(lab, forced)
    c, s = np.cos(ang), np.sin(ang)
    u = xx * c + yy * s          # along the threads
    v = -xx * s + yy * c         # across the threads
    tw = scale * 1.6             # thread width
    ti = np.floor(v / tw)
    tv = v / tw - ti
    ridge = np.sin(np.pi * tv) ** 0.6                       # each thread round in section
    twist = 0.5 + 0.5 * np.sin((u / (tw * 1.6) + ti * 0.37) * 2 * np.pi)
    per_thread = _hash(ti.astype(np.int64), lab.astype(np.int64))
    lay = 0.62 + 0.40 * ridge + 0.06 * twist + 0.10 * (per_thread - 0.5)
    # couching: a cross stitch over the threads every `cs` along them, staggered row to row
    cs = tw * 6.0
    band = np.floor(v / (tw * 3.0))
    cu = (u + (band % 2) * cs * 0.5) / cs
    cf = cu - np.floor(cu)
    couch = np.exp(-((cf - 0.5) * cs / (scale * 0.7)) ** 2)
    lay = lay * (1 - 0.45 * couch) + 0.10 * couch * (np.sin(np.pi * ((v / (tw * 0.5)) % 1)) ** 2)
    fill_shade = lay

    # the stem-stitch outlines: where an area meets another, a dark twisted line
    edge = np.zeros((H, W), bool)
    edge[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    edge[1:, :] |= lab[1:, :] != lab[:-1, :]
    d = ndi.distance_transform_edt(~edge)
    line_w = scale * 0.6
    on_line = (d < line_w) & ~linen
    # outline wool: darker than the fill it bounds
    dark = base * 0.80
    gy, gx = np.gradient(ndi.gaussian_filter(edge.astype(np.float32), 1.5))
    t_ang = np.arctan2(gy, gx) + np.pi / 2
    tu = xx * np.cos(t_ang) + yy * np.sin(t_ang)
    rope = 0.75 + 0.25 * np.sin((tu / (scale * 1.1) + d / line_w * 0.5) * 2 * np.pi)

    shade = np.where(linen, lin_shade, fill_shade)
    out = base * shade[..., None]
    mail = lab == IDX['mail']
    if mail.any():
        cell = scale * 5.0
        rh = cell * 0.866
        row = np.floor(yy / rh)
        off = (row % 2) * cell * 0.5
        cx = (np.floor((xx - off) / cell) + 0.5) * cell + off
        cy = (row + 0.5) * rh
        dist = np.hypot(xx - cx, yy - cy)
        ring = np.exp(-((dist - cell * 0.32) / (scale * 0.55)) ** 2)
        ringcol = np.array(RING, np.float32) * (0.85 + 0.25 * np.sin(np.arctan2(yy - cy, xx - cx) * 3))[..., None]
        out = np.where(mail[..., None], out * (1 - ring[..., None]) + ringcol * ring[..., None], out)
    out = np.where(on_line[..., None], dark * rope[..., None], out)
    # wool sits a little above the linen: a soft shadow just outside every stitched area on the linen
    raised = ndi.gaussian_filter((~linen).astype(np.float32), scale * 0.8)
    out = np.where(linen[..., None], out * (1 - 0.18 * raised[..., None]), out)
    # fuzz: tiny fibres, and the gentle unevenness of hand work
    fuzz = rng.standard_normal((H, W)).astype(np.float32)
    out *= (1 + 0.035 * ndi.gaussian_filter(fuzz, 0.5))[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)


def flat(lab):
    return Image.fromarray(RGB[lab].astype(np.uint8))


if __name__ == '__main__':
    cmd, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    if cmd == 'trace':
        for name in FILES:
            lab = trace(name)
            flat(lab).save(os.path.join(out, name + '-flat.png'))
            Image.fromarray(stitch(lab, 3.0)).save(os.path.join(out, name + '-stitched.png'))
