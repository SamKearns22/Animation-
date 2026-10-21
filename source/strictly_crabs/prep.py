"""Strictly Crabs Dancing: cut the crab textures and shapes out of Sam's reference photos.

Every crab part is a "pillow": a picture (colour + outline) and a height map that puffs it up into a solid.
Shells and claws are cut straight from the photos; legs reuse the photos' own shell grain.
Writes tex/*.png and tex/parts.json for crab.js.
"""
import json, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '..', '..', 'refs', 'strictly-crabs')
OUT = os.path.join(HERE, 'tex')
FF = '/usr/local/lib/python3.13/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
rng = np.random.default_rng(7)
parts = {}

velvet = Image.open(f'{REF}/crab-ref-1-velvet-white.webp').convert('RGB')
shore = Image.open(f'{REF}/crab-ref-4-shore-black.jpg').convert('RGB')

# shells: crop (photo coords), outline (fractions of the crop, back at the top, eyes at the bottom)
SHELLS = {
    'velvet': (velvet.rotate(28, Image.BICUBIC, center=(460, 240), fillcolor='white'), (296, 110, 615, 300),
               [(.5, .03), (.25, .08), (.08, .25), (.02, .5), (.08, .75), (.2, .92), (.35, .97), (.65, .97),
                (.8, .92), (.92, .75), (.98, .5), (.92, .25), (.75, .08)], (1.0, .80)),
    'shore': (shore, (148, 0, 452, 180),
              [(.5, .075), (.28, .125), (.09, .3), (.015, .5), (.06, .65), (.16, .75), (.27, .85), (.73, .85),
               (.84, .75), (.94, .65), (.985, .5), (.91, .3), (.72, .125)], (1.0, .76)),
}


def save(name, rgb, alpha, height, size, htop, hbot):
    Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8), 'RGBA').save(f'{OUT}/{name}.png')
    h = np.clip(height / max(height.max(), 1e-6), 0, 1)
    Image.fromarray((h * 255).astype(np.uint8)).save(f'{OUT}/{name}_h.png')
    parts[name] = {'tex': f'{name}.png', 'hmap': f'{name}_h.png', 'size': size, 'htop': htop, 'hbot': hbot}


def puff(alpha, power=0.5, blur=2):
    """Height from distance to the outline: rounded edges, fuller in the middle."""
    d = ndimage.distance_transform_edt(alpha > 127)
    d = ndimage.gaussian_filter(d, blur)
    return (d / max(d.max(), 1e-6)) ** power


def shell(name):
    img, box, poly, size = SHELLS[name]
    W, H = 512, 384
    rgb = np.asarray(img.crop(box).resize((W, H), Image.LANCZOS), np.float32)
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).polygon([(u * W, v * H) for u, v in poly], fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(1.2)), np.float32)
    h = puff(a, .45, 6)
    yy, xx = np.mgrid[0:H, 0:W]
    dome = 1 - ((xx / W - .5) * 1.6) ** 2 - ((yy / H - .45) * 1.5) ** 2
    h = 0.55 * h + 0.45 * np.clip(dome, 0, 1) * (h > 0)
    # darken the rim slightly where the shell curls under
    rgb *= (0.65 + 0.35 * np.clip(h * 3, 0, 1))[..., None]
    save(f'shell_{name}', rgb, a, h, size, 0.22, 0.06)
    return rgb[int(H * .3):int(H * .6), int(W * .3):int(W * .7)]   # a patch of shell grain for the legs


def cut_white(img):
    x = np.asarray(img, np.float32)
    d = np.sqrt(((255 - x) ** 2).sum(2))
    m = ndimage.binary_opening(d > 60, iterations=1)
    lab, n = ndimage.label(m)
    if n > 1:
        m = lab == (np.bincount(lab.ravel())[1:].argmax() + 1)
    m = ndimage.binary_erosion(ndimage.binary_fill_holes(m), iterations=3)
    return x, (ndimage.gaussian_filter(m.astype(np.float32), 0.8) * 255)


def match(rgb, alpha, target_mean, target_std):
    """Recolour towards another crab's palette, keeping the photo's grain."""
    sel = alpha > 127
    out = rgb.copy()
    for c in range(3):
        mu, sd = rgb[..., c][sel].mean(), rgb[..., c][sel].std() + 1e-3
        out[..., c] = (rgb[..., c] - mu) / sd * target_std[c] + target_mean[c]
    return np.clip(out, 0, 255)


def claw(name, recolour=None):
    c = velvet.crop((340, 435, 570, 535)).transpose(Image.FLIP_LEFT_RIGHT)   # wrist at the left, tips right
    c = c.resize((512, 224), Image.LANCZOS)
    rgb, a = cut_white(c)
    # drop the scrap of arm above the wrist
    a[:60, :120] = 0
    if recolour is not None:
        rgb = match(rgb, a, *recolour)
    else:
        rgb = rgb * .8
    h = puff(a, .55, 3)
    save(f'claw_{name}', rgb, a, h, (0.78, 0.36), 0.17, 0.15)


def tile(patch, W, H):
    p = Image.fromarray(np.clip(patch, 0, 255).astype(np.uint8))
    p = p.resize((W // 2, H))
    p = np.asarray(p, np.float32)
    return np.concatenate([p, p[:, ::-1]], 1)[:, :W]


def legs(name, grain, base, light, stripe, joint):
    """Leg segments: tapered, flattened, with the shell grain recoloured to the leg's palette."""
    W, H = 256, 64
    g = tile(grain, W, H)
    lum = g.mean(2, keepdims=True); lum = (lum - lum.mean()) / (lum.std() + 1e-3)
    u = np.linspace(0, 1, W)[None, :]; v = np.linspace(-1, 1, H)[:, None]
    shapes = {
        'merus': (lambda u: .9 - .15 * u, .30),
        'carpus': (lambda u: .75 + .1 * np.sin(np.pi * u), .25),
        'propodus': (lambda u: .75 - .2 * u, .25),
        'dactyl': (lambda u: .7 * (1 - u) ** .7 + .02, .22),
        'paddle': (lambda u: .95 * np.sin(np.pi * np.clip(u * .95 + .03, 0, 1)) ** .6, .10),
        'armmerus': (lambda u: .95 - .1 * u, .32),
        'armcarpus': (lambda u: .8 + .15 * np.sin(np.pi * u), .32),
    }
    for seg, (prof, flat) in shapes.items():
        w = prof(u) * np.ones_like(v)
        end = np.minimum(u / .04, 1) if seg != 'dactyl' else 1
        inside = (np.abs(v) < w) & (u < .995)
        a = (inside * 255).astype(np.float32)
        a = ndimage.gaussian_filter(a, .7)
        cross = np.sqrt(np.clip(1 - (v / np.maximum(w, 1e-3)) ** 2, 0, 1)) * w * (end if np.ndim(end) else 1)
        rgb = np.array(base, np.float32) + lum * 22
        # paler edges, darker spine, a dark stripe each side (velvet), joint colour at the ends
        rgb = rgb + (np.array(light) - np.array(base)) * (np.abs(v) / np.maximum(w, 1e-3))[..., None] ** 3 * .6
        if stripe is not None:
            s = np.exp(-((np.abs(v) / np.maximum(w, 1e-3) - .55) / .08) ** 2)[..., None]
            rgb = rgb * (1 - .7 * s) + np.array(stripe) * .7 * s
        j = (np.exp(-(u / .05) ** 2) + np.exp(-((1 - u) / .05) ** 2))[..., None] * (seg not in ('dactyl', 'paddle'))
        rgb = rgb * (1 - .6 * j) + np.array(joint) * .6 * j
        if seg in ('dactyl', 'paddle'):   # horny tips go amber-black
            t = np.clip((u - .55) / .45, 0, 1)[..., None]
            rgb = rgb * (1 - t * .7) + np.array([60, 35, 15]) * t * .7
        save(f'{seg}_{name}', np.clip(rgb, 0, 255), a, cross, (1.0, 1.0), flat, flat)


def plate():
    """Blurred Strictly ballroom behind the dance floor (a wide shot from the routine, dancers lost in the blur)."""
    src = os.path.join(REF, 'routine-reference.mp4')
    raw = f'{OUT}/plate_raw.png'
    subprocess.run([FF, '-v', 'error', '-y', '-ss', '3.6', '-i', src, '-frames:v', '1', raw], check=True)
    im = Image.open(raw).convert('RGB')
    w, h = im.size
    im = im.crop((0, int(h * .08), w, int(h * .62))).resize((1600, 600), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(9))
    # fade the top into the dark and the bottom into the floor haze, so no edges show (or reflect)
    x = np.asarray(im, np.float32); yy = np.linspace(0, 1, x.shape[0])[:, None, None]
    top = np.clip(yy / .35, 0, 1) ** 1.5; bot = np.clip((1 - yy) / .12, 0, 1)
    x = x * top + np.array([5, 2, 10]) * (1 - top)
    x = x * bot + np.array([20, 10, 34]) * (1 - bot)
    im = Image.fromarray(np.clip(x, 0, 255).astype(np.uint8))
    im.save(f'{OUT}/plate.jpg', quality=90)
    os.remove(raw)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    gv = shell('velvet')
    gs = shell('shore')
    claw('velvet')
    claw('shore', recolour=((88, 82, 46), (30, 28, 18)))
    legs('velvet', gv, base=(52, 42, 30), light=(85, 70, 48), stripe=(30, 34, 58), joint=(120, 45, 35))
    legs('shore', gs, base=(92, 84, 42), light=(140, 120, 60), stripe=None, joint=(160, 95, 40))
    plate()
    json.dump(parts, open(f'{OUT}/parts.json', 'w'), indent=1)
    print(len(parts), 'parts')
