import sys, os
sys.path.insert(0, 'source')
import numpy as np
from PIL import Image
import castsheet as CS
cast, PP = CS._setup('brexit-is-done', None)
B, V = PP.B, PP.V
import sitting as S
OUT = sys.argv[1]
def one(sp, yaw, seated=False):
    tile = Image.new('RGBA', (1080, 1920), (255,255,255,255))
    s = 0.5 * sp['height'] / 1.75
    cam = B.Cam(2.0, 540, 470)
    j = None
    if seated:
        j = S.pose(sp, 'upright')
    y0 = 840 - 928 * s
    V.person(tile, cam, 540, y0, s, dict(sp), 0.0, yaw, j)
    a = np.asarray(tile.convert('RGB')).copy()
    # headless: blank above the neck base (screen y of world y0, minus the collar)
    neck_sy = int((y0 - 470) * 2.0 + 960 + ((j.get('bob',0) if j else 0)*s*2)) + 6
    a[:max(0, neck_sy)] = 255
    return a
rows = [('may', None), ('may', 'woman'), ('kemi', None), ('kemi', 'woman'), ('blair', None)]
views = [(0, False, 'front'), (45, False, 'three-quarter'), (90, False, 'side'), (180, False, 'back'), (45, True, 'seated 3/4')]
tiles = {}
for who, build in rows:
    sp = dict(cast[who])
    sp['hair_style'] = 'back'
    for k in ('hat', 'hat_c', 'specs'):
        sp.pop(k, None)
    if build: sp['figure'] = build
    for yaw, seated, name in views:
        try:
            a = one(sp, yaw, seated)
        except Exception as e:
            print('FAIL', who, build, name, e); a = np.full((1920,1080,3),200,np.uint8)
        tiles[(who, build, name)] = a
np.save(OUT + '.npy', np.array([0]))
import pickle; pickle.dump(tiles, open(OUT + '.pkl', 'wb'))
print('ok', len(tiles))
