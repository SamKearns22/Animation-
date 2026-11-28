"""A still of one cell view with Danny downcast on the cot, drawn as shot 1's cell_still.py (chat 7: any view).
    python3 notes/patriots5-sets/view_still.py VIEW OUT.jpg [YAW]
Danny sits at plan x 0, depth 3.85; his place on screen comes from the view's own camera (turned or not)."""
import sys
sys.path.insert(0, 'source')
from PIL import Image
import numpy as np
import people as PK, people_parts as PPt, places as PL, sitting as S, places_rooms as PR
from satire_style import install_circle_hands
B, V = PPt.B, PPt.V
install_circle_hands(B)
CAST = PK.install(PK.load('patriots5'))
D = PL.load('patriots5')
VIEW, OUT = sys.argv[1], sys.argv[2]
YAW = float(sys.argv[3]) if len(sys.argv) > 3 else None
L = PL.LevelCam.of(D, VIEW)
cam_line = D['views'][VIEW]['camera']
pcs = {p.it['kind']: p for p in PL.pieces(D, VIEW)}
mb = pcs['moonbeam']
cx, cd = mb.cam_xd(0.0, 3.85)                       # Danny on the plan, in this camera's frame
yaw = YAW if YAW is not None else cam_line.get('facing', 0.0)
img = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
B.SS = 1
cam = B.Cam(1.0, 540, 960)
import patriots5_cast as PC
sp = dict(CAST['tommo'], **PC.SAD)
s = L.ppm(cd) * sp['height'] * 0.84 / 928.0
j = S.pose(sp, 'downcast')
j['chair_draw'] = lambda *a, **k: None
X, _ = L.p(cx, cd, 0.0)
fx, fd = mb.cam_xd(0.0, 3.85 - 0.32)                # his feet, forward of his hips (plan -depth)
neck_y = L.p(fx, fd, 0.0)[1] - 928.0 * s
lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
V.person(lay, cam, X, neck_y, s, sp, 0.0, yaw, j)
mb.args['blockers'] = [(np.asarray(lay)[..., 3], cd - 0.1)]
for layer in ('back', 'mid', 'front'):
    pt = PL.painter(D, VIEW, layer)
    if pt: pt(img, cam, 0.0)
pcs['night'].draw(img, cam, 0.0)
mb.draw(img, cam, 0.0)
mb.args['blockers'] = []
pcs['night'].draw(lay, cam, 0.0)
PR.moon_on(lay, mb, cam, 0.0)
img.alpha_composite(lay)
img.convert('RGB').save(OUT, quality=90)
print(OUT)
