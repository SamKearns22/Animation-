import sys, os
sys.path.insert(0, 'source')
from PIL import Image
import people as PK, people_parts as PPt, places as PL, sitting as S, places_rooms as PR
from satire_style import install_circle_hands
B, V = PPt.B, PPt.V
install_circle_hands(B)
CAST = PK.install(PK.load('patriots5'))
D = PL.load('patriots5')
VIEW = 'cell_front'
L = PL.LevelCam.of(D, VIEW)
img = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
B.SS = 1
cam = B.Cam(1.0, 540, 960)
import patriots5_cast as PC
sp = dict(CAST['tommo'], **PC.SAD)
d = 3.85
s = L.ppm(d) * sp['height'] * 0.84 / 928.0
j = S.pose(sp, 'downcast')
j['chair_draw'] = lambda *a, **k: None
neck_y = L.p(0.0, d - 0.32, 0.0)[1] - 928.0 * s
lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
V.person(lay, cam, 540, neck_y, s, sp, 0.0, 0.0, j)
pcs = {p.it['kind']: p for p in PL.pieces(D, VIEW)}
import numpy as np
pcs['moonbeam'].args['blockers'] = [(np.asarray(lay)[..., 3], d - 0.1)]
for layer in ('back', 'mid', 'front'):
    pt = PL.painter(D, VIEW, layer)
    if pt: pt(img, cam, 0.0)
pcs['night'].draw(img, cam, 0.0)
pcs['moonbeam'].draw(img, cam, 0.0)
pcs['moonbeam'].args['blockers'] = []
pcs['night'].draw(lay, cam, 0.0)
PR.moon_on(lay, pcs["moonbeam"], cam, 0.0)
img.alpha_composite(lay)
img.convert('RGB').save(sys.argv[1], quality=90)
print(sys.argv[1])
