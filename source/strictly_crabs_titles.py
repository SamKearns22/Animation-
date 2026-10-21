"""Strictly Crabs Dancing: swap 'Come' for 'Crabs' in the screen-recorded ident."""
import os, sys, glob, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage
from scipy.signal import fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, 'data', 'strictly-crabs', 'titles')          # working files (git-ignored, rebuilt any time)
IDENT = os.path.join(HERE, '..', 'refs', 'strictly-crabs', 'ident-recording.mov')
FF = '/usr/local/lib/python3.13/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
CROP = '1170:657:0:967'                                           # the picture inside the phone's screen recording
FR = sorted(glob.glob(S + '/fr/*.png'))
REF = 150
BOX = (446, 234, 716, 348)          # 'Come' in the reference frame (picture coords)
FONT = '/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf'


def extract():
    """python3 strictly_crabs_titles.py extract: the recording's frames, cropped to the picture (no phone chrome)."""
    os.makedirs(S + '/fr', exist_ok=True)
    subprocess.run([FF, '-v', 'error', '-y', '-i', IDENT, '-an', '-vf', 'crop=' + CROP, S + '/fr/%04d.png'], check=True)


def gray(im):
    return np.asarray(im.convert('L'), np.float32)


def ncc(img, tpl):
    t = tpl - tpl.mean(); n = t.size
    num = fftconvolve(img, t[::-1, ::-1], mode='valid')
    ones = np.ones_like(t)
    s1 = fftconvolve(img, ones, mode='valid'); s2 = fftconvolve(img * img, ones, mode='valid')
    var = np.maximum(s2 - s1 * s1 / n, 1e-3)
    return num / np.sqrt(var * (t * t).sum())


def track():
    ref = gray(Image.open(FR[REF]))
    x0, y0, x1, y1 = BOX
    tpl0 = ref[y0:y1, x0:x1]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    out = {}
    s_prev = 1.0
    for i in range(70, len(FR)):
        g = gray(Image.open(FR[i]))
        best = (-1, 0, 0, 0)
        for s in np.arange(max(0.8, s_prev - 0.12), s_prev + 0.12, 0.01):
            tw, th = int(round(tpl0.shape[1] * s)), int(round(tpl0.shape[0] * s))
            tpl = np.asarray(Image.fromarray(tpl0).resize((tw, th), Image.BILINEAR), np.float32)
            m = 90
            X0, Y0 = int(cx - tw / 2 - m), int(cy - th / 2 - m)
            win = g[max(Y0, 0):Y0 + th + 2 * m, max(X0, 0):X0 + tw + 2 * m]
            c = ncc(win, tpl)
            k = np.unravel_index(c.argmax(), c.shape)
            if c[k] > best[0]:
                best = (float(c[k]), float(s), max(X0, 0) + k[1] + tw / 2, max(Y0, 0) + k[0] + th / 2)
        out[i] = best
        if best[0] > 0.6:
            s_prev = best[1]
        print(i, [round(v, 3) for v in best], flush=True)
    json.dump(out, open(S + '/track.json', 'w'))


def gold_word(word, size):
    """Gold bevelled lettering with a dark outline, drawn at 2x and returned as RGBA."""
    k = 2
    f = ImageFont.truetype(FONT, size * k)
    l, t, r, b = f.getbbox(word)
    pad = 30 * k
    W, H = r - l + 2 * pad, b - t + 2 * pad
    a = Image.new('L', (W, H)); ImageDraw.Draw(a).text((pad - l, pad - t), word, font=f, fill=255)
    A = np.asarray(a, np.float32) / 255
    # gold ramp by height, chrome-like bands
    y = np.linspace(0, 1, H)[:, None] * np.ones((1, W))
    yy = (y * H - pad) / (H - 2 * pad)
    stops = [(0, (255, 248, 200)), (.3, (246, 200, 90)), (.52, (170, 100, 30)), (.6, (250, 220, 130)),
             (.8, (215, 150, 55)), (1, (120, 60, 15))]
    col = np.zeros((H, W, 3), np.float32)
    for c in range(3):
        col[..., c] = np.interp(yy, [p for p, _ in stops], [v[c] for _, v in stops])
    # bevel lighting from the upper left
    h = ndimage.gaussian_filter(A, 4 * k)
    gy, gx = np.gradient(h)
    light = np.clip(-(gx + gy) * 18 * k, -1, 1)[..., None]
    col = np.where(light > 0, col + (255 - col) * light * .8, col * (1 + light * .55))
    # outline and drop shadow
    ol = ndimage.grey_dilation(A, footprint=disk(5 * k))
    ol = ndimage.gaussian_filter(ol, 1.0 * k)
    sh = ndimage.gaussian_filter(np.roll(ndimage.grey_dilation(A, footprint=disk(7 * k)), (5 * k, 4 * k), (0, 1)), 4 * k)
    dark = np.array([45, 14, 4], np.float32)
    rgb = dark * np.ones((H, W, 1))
    rgb = rgb * (1 - A[..., None]) + col * A[..., None]
    alpha = np.maximum(np.maximum(ol, A), sh * .8)
    rgb = np.where((ol + A)[..., None] > 0.01, rgb, np.array([20, 5, 2], np.float32))
    im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8), 'RGBA')
    return im.resize((W // k, H // k), Image.LANCZOS)


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def plate():
    """RGBA patch in reference coords: ball texture over 'Come', then 'Crabs' on top."""
    ref = Image.open(FR[REF]).convert('RGB')
    x0, y0, x1, y1 = BOX
    W, H = 340, 170
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ox, oy = int(cx - W / 2), int(cy - H / 2)
    # ball texture from just right of the word, mirrored and tiled across
    src = np.asarray(ref.crop((x1 + 2, y0 + 6, x1 + 72, y0 + 6 + H)), np.float32)
    tile = np.concatenate([src, src[:, ::-1]], 1)
    fill = np.concatenate([tile] * (W // tile.shape[1] + 1), 1)[:, :W]
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).rounded_rectangle(
        (x0 - ox - 4, y0 - oy, x1 - ox + 4, y1 - oy), 30, fill=255)
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(6)), np.float32)[..., None] / 255
    base = np.asarray(ref.crop((ox, oy, ox + W, oy + H)), np.float32)
    bg = Image.fromarray((fill * m + base * (1 - m)).astype(np.uint8)).convert('RGBA')
    word = gold_word('Crabs', 116)
    word = word.rotate(4, Image.BICUBIC, expand=True)       # the logo leans uphill
    bg.alpha_composite(word, (W // 2 - word.width // 2 - 4, H // 2 - word.height // 2 + 4))
    a = np.maximum(m[..., 0], np.asarray(bg.getchannel('A'), np.float32) / 255 * 0 + m[..., 0])
    # whole patch is opaque where the old word was; the new word may spill past it
    wa = Image.new('L', (W, H)); wa.paste(word.getchannel('A'), (W // 2 - word.width // 2 - 4, H // 2 - word.height // 2 + 4))
    a = np.maximum(a, np.asarray(wa, np.float32) / 255)
    bg.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    return bg, (ox, oy, cx, cy)


def render(out_dir):
    tr = {int(k): v for k, v in json.load(open(S + '/track.json')).items()}
    P, (ox, oy, cx, cy) = plate()
    P.save(S + '/plate.png')
    for i, f in enumerate(FR):
        im = Image.open(f).convert('RGBA')
        t = tr.get(i)
        if t and t[0] > 0.55:
            sc, fx, fy = t[1], t[2], t[3]
            # plate pixel (u,v) -> ref (ox+u, oy+v) -> frame s*(ref-c)+f
            w, h = int(P.width * sc) + 2, int(P.height * sc) + 2
            px, py = sc * (ox - cx) + fx, sc * (oy - cy) + fy
            Pw = P.resize((max(1, round(P.width * sc)), max(1, round(P.height * sc))), Image.LANCZOS)
            layer = Image.new('RGBA', im.size)
            layer.paste(Pw, (round(px), round(py)))
            im.alpha_composite(layer)
        im.convert('RGB').save(f'{out_dir}/{i:04d}.png')


if __name__ == '__main__':
    {'extract': extract, 'track': track, 'render': lambda: render(sys.argv[2])}[sys.argv[1]]()
