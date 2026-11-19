"""Test only: a mock of the 'feature slide' (BoJack's nudge) done as a picture warp on the finished front head.
The face's middle slides toward the focus, the outline's edges stay put. Not a kit piece; changes nothing."""
import os, sys
import numpy as np
sys.path.insert(0, '/home/user/Animation-/source'); os.chdir('/home/user/Animation-')
import people as PK, people_parts as PP
from PIL import Image, ImageDraw, ImageFont
from satire_style import install_circle_hands
B, V = PP.B, PP.AV.MC.V
install_circle_hands(B)
a = PK.load('facetool')
cast = PK.install({'andy': a['andy'], 'kemi': a['kemi']})
B.SS = 1
cam = B.Cam(1.0, 540, 960)
F = lambda n: ImageFont.truetype('source/fonts/DejaVuSans-Bold.ttf', n)

def draw(sp, mood, j, yaw=0):
    s = 0.5 * sp['height'] / 1.75
    t = Image.new('RGBA', (1080, 1920), (236, 232, 226, 255))
    V.person(t, cam, 540, 840 - 928 * s, s, dict(sp, **mood), 0.0, yaw, dict(V.standing(sp), **j))
    return np.array(t.convert('RGB'))

def slide(a, cx, y0, y1, half, k):
    """Columns within `half` px of cx shift by k*half*(1-(d/half)^2) (a smooth bump), rows y0..y1, fading at the ends."""
    out = a.copy()
    ys = np.arange(y0, y1)
    fade = np.sin(np.pi * (ys - y0) / (y1 - y0)) ** 0.5
    xs = np.arange(cx - half, cx + half)
    for yi, y in enumerate(ys):
        d = (xs - cx) / half
        sh = k * half * (1 - d * d) * fade[yi]
        src = np.clip(np.round(xs - sh).astype(int), 0, a.shape[1] - 1)
        out[y, xs] = a[y, src]
    return out

rows = []
for w in ('andy', 'kemi'):
    sp = cast[w]
    tiles = [('NOW: turned 45', draw(sp, {}, {}, 45)),
             ('front, no focus', draw(sp, {}, {})),
             ('focus R: eyes + tilt', draw(sp, dict(look=0.9), dict(head_roll=-6.0)))]
    base = draw(sp, dict(look=0.9), dict(head_roll=-6.0))
    tiles.append(('focus R: + features slide (mock)', slide(base, 540, 215, 380, 62, 0.16)))
    baseL = draw(sp, dict(look=-0.9, brow_up=0.02), dict(head_roll=5.0))
    tiles.append(('focus L: + slide (mock)', slide(baseL, 540, 215, 380, 62, -0.16)))
    rows.append((w, tiles))
BOX = (440, 170, 640, 410)
tw = 330; th = int(tw * (BOX[3] - BOX[1]) / (BOX[2] - BOX[0]))
img = Image.new('RGB', (tw * 5, 50 + 2 * (th + 34)), (236, 232, 226)); d = ImageDraw.Draw(img)
d.text((10, 10), 'Front-on focus: the slide is a picture mock, not a kit piece (test only, 19 Nov)', font=F(22), fill=(30, 30, 30))
for r, (w, tiles) in enumerate(rows):
    for c, (lab, arr) in enumerate(tiles):
        im = Image.fromarray(arr).crop(BOX).resize((tw - 8, th), Image.LANCZOS)
        y = 46 + r * (th + 34)
        img.paste(im, (c * tw + 4, y + 26)); d.text((c * tw + 8, y + 4), f'{w.title()}: {lab}', font=F(15), fill=(30, 30, 30))
img.save(sys.argv[1], quality=88); print(sys.argv[1])
