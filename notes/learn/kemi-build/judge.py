"""The blind judge's sheet for cast v3 (Open Wounds chat 6): May, Kemi and Blair headless, black, front / 3/4 /
back / seated 3/4, shuffled, numbered, at phone size (each figure about 300 px tall). Key: judge_key.json."""
import json, os, random, sys
sys.path.insert(0, 'source')
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import castsheet as CS
import sitting as S
HERE = os.path.dirname(os.path.abspath(__file__))
cast, PP = CS._setup('brexit-is-done', None)
B, V = PP.B, PP.V
tiles = []
for who in ('may', 'kemi', 'blair'):
    for yaw, seated, name in ((0, False, 'front'), (45, False, 'three-quarter'), (180, False, 'back'), (45, True, 'seated 3/4')):
        sp = dict(cast[who]); sp['hair_style'] = 'back'
        for k in ('hat', 'hat_c', 'specs'):
            sp.pop(k, None)
        tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
        s = 0.5 * sp['height'] / 1.75
        cam = B.Cam(2.0, 540, 470)
        j = S.pose(sp, 'upright') if seated else None
        y0 = 840 - 928 * s
        V.person(tile, cam, 540, y0, s, dict(sp), 0.0, yaw, j)
        a = np.asarray(tile.convert('RGB')).copy()
        neck = int((y0 - 470) * 2.0 + 960 + ((j.get('bob', 0) if j else 0) * s * 2)) + 6
        m = np.abs(a.astype(int) - 255).sum(2) > 30
        m[:max(0, neck)] = False
        ys, xs = np.nonzero(m)
        o = Image.fromarray(np.where(m[..., None], 20, 255).astype(np.uint8).repeat(3, 2)).crop(
            (xs.min() - 10, ys.min() - 10, xs.max() + 10, ys.max() + 10))
        k = 300 / o.height
        tiles.append(((who, name), o.resize((int(o.width * k), 300), Image.LANCZOS)))
random.Random(624).shuffle(tiles)
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
W = max(sum(t.width + 30 for _, t in tiles[:6]), sum(t.width + 30 for _, t in tiles[6:])) + 30
page = Image.new('RGB', (W, 2 * 360 + 20), 'white'); d = ImageDraw.Draw(page)
x, y = 30, 40
for i, (key, t) in enumerate(tiles):
    if i == 6:
        x, y = 30, 400
    page.paste(t, (x, y)); d.text((x, y - 32), str(i + 1), fill='black', font=f); x += t.width + 30
page.save(sys.argv[1], quality=90)
json.dump({str(i + 1): list(k) for i, (k, _) in enumerate(tiles)}, open(os.path.join(HERE, 'judge_key.json'), 'w'))
print(sys.argv[1])
