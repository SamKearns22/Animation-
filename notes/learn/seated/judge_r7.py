"""R7's blind judges (chat 2, 25 Nov): two sheets of May, Kemi and Blair seated on R7's lower body (new films), at
phone size, shuffled and numbered. outlines: headless, black (the woman/man judge, as notes/learn/kemi-build/judge.py
for cast v3). look: in colour, whole (the cold look: anything wrong below the waist). Key: judge/key-r7.json.
    python3 notes/learn/seated/judge_r7.py"""
import json, os, random, sys
sys.path.insert(0, 'source')
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import castsheet as CS
import sitting as S
HERE = os.path.dirname(os.path.abspath(__file__))
cast, PP = CS._setup('brexit-is-done', None)
B, V = PP.B, PP.V
VIEWS = ((0, 'upright', 'seated front'), (45, 'upright', 'seated 3/4'), (90, 'upright', 'seated side'),
         (-45, 'cross, knee over knee', 'seated 3/4, legs crossed'))


def figure(who, yaw, pose, outline):
    sp = dict(cast[who]); sp['seat_r7'] = True
    if outline:
        sp['hair_style'] = 'back'
        if 'kit_house' in sp:
            sp['kit_house'] = dict(sp['kit_house'], hair='bald')
        for k in ('hat', 'hat_c', 'specs'):
            sp.pop(k, None)
    tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    s = 0.5 * sp['height'] / 1.75
    j = S.pose(sp, pose)
    y0 = 840 - 928 * s
    V.person(tile, B.Cam(2.0, 540, 470), 540, y0, s, sp, 0.0, yaw, j)
    a = np.asarray(tile.convert('RGB')).copy()
    m = np.abs(a.astype(int) - 255).sum(2) > 30
    if outline:
        neck = int((y0 - 470) * 2.0 + 960 + j.get('bob', 0) * s * 2) + 6
        m[:max(0, neck)] = False
    ys, xs = np.nonzero(m)
    box = (xs.min() - 10, ys.min() - 10, xs.max() + 10, ys.max() + 10)
    o = Image.fromarray(np.where(m[..., None], 20, 255).astype(np.uint8).repeat(3, 2)) if outline else Image.fromarray(a)
    o = o.crop(box)
    h = 300 if outline else 420
    return o.resize((int(o.width * h / o.height), h), Image.LANCZOS)


def sheet(outline, seed, path):
    tiles = [((w, n), figure(w, y, p, outline)) for w in ('may', 'kemi', 'blair') for y, p, n in VIEWS]
    random.Random(seed).shuffle(tiles)
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
    rows = [tiles[:6], tiles[6:]]
    W = max(sum(t.width + 30 for _, t in r) for r in rows) + 30
    h = tiles[0][1].height
    page = Image.new('RGB', (W, 2 * (h + 60) + 20), 'white'); d = ImageDraw.Draw(page)
    for r, row in enumerate(rows):
        x, y = 30, 40 + r * (h + 60)
        for i, (key, t) in enumerate(row):
            page.paste(t, (x, y)); d.text((x, y - 32), str(r * 6 + i + 1), fill='black', font=f); x += t.width + 30
    page.save(path, quality=90)
    return {str(i + 1): list(k) for i, (k, _) in enumerate(tiles)}


if __name__ == '__main__':
    key = {'outlines': sheet(True, 725, os.path.join(HERE, 'judge', 'outlines-r7.jpg')),
           'look': sheet(False, 1125, os.path.join(HERE, 'judge', 'look-r7.jpg'))}
    json.dump(key, open(os.path.join(HERE, 'judge', 'key-r7.json'), 'w'), indent=1)
    print('written: judge/outlines-r7.jpg, judge/look-r7.jpg, judge/key-r7.json')
