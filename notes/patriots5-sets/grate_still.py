"""A still of a cell view with someone at the window (chat 8; shots 3 and 5, later 6):
    python3 notes/patriots5-sets/grate_still.py VIEW OUT.jpg [WHO] [MOOD] [NECK_Z]
WHO 'both': the two at once (shot 6). WHO 'patriot' (default): outside, plan x 0.07 (his face between two bars), depth 4.75 (0.1 m past the bars), facing
into the cell, neck NECK_Z m up (default 2.06: his chin just over the outer sill). WHO 'danny': inside, up on the cot,
x -0.02, depth 4.0, facing the window, on his toes (neck 2.0 m). Whoever is on the far side of the wall from the lens
is drawn through the window (paint_with's `beyond`: between the sky or the dark cell and the bars, cut to the
opening); whoever is on the lens's side is drawn over the set."""
import sys
sys.path.insert(0, 'source')
from PIL import Image
import people as PK, places as PL, places_rooms as PR
import patriots5_cast as PC
CAST = PK.install(PK.load('patriots5'))
PC.install()
B, V = PC.PP.B, PC.PP.V
D = PL.load('patriots5')
VIEW, OUT = sys.argv[1], sys.argv[2]
WHO = sys.argv[3] if len(sys.argv) > 3 else 'patriot'
MOOD = sys.argv[4] if len(sys.argv) > 4 else 'rest'
def who_at(who):
    """(sp, pose, plan x, depth, facing on the plan (0: towards shot 1's lens), neck height m)."""
    if who == 'patriot':
        sp, j = PC.patriot(MOOD)
        return sp, j, 0.07, 4.75, 0.0, 2.06
    sp = dict(CAST['tommo'])
    return sp, PC.danny_sill(sp), -0.02, 4.0, 180.0, 2.0
L = PL.LevelCam.of(D, VIEW)
pcs = {p.it['kind']: p for p in PL.pieces(D, VIEW)}
win = pcs['grated window']
img = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
B.SS = 1
cam = B.Cam(1.0, 540, 960)
far, near = [], []
for w in (['patriot', 'danny'] if WHO == 'both' else [WHO]):
    sp, j, px, pd, pf, nz = who_at(w)
    nz = float(sys.argv[5]) if len(sys.argv) > 5 and WHO != 'both' else nz
    cx, cd = win.cam_xd(px, pd)
    yaw = (D['views'][VIEW]['camera'].get('facing', 0.0) - pf) % 360   # 0: facing us
    s = L.ppm(cd) * sp['height'] * 0.84 / 928.0
    X, neck_y = L.p(cx, cd, nz)
    fn = (lambda X, neck_y, s, sp, yaw, j: lambda im: V.person(im, cam, X, neck_y, s, dict(sp, full=True,
                                                                  pose='custom'), 0.0, yaw, j))(X, neck_y, s, sp, yaw, j)
    beyond = win.cam_d(px, pd) > win.cam_d(0.0, win.d0 + win.args['deep'] / 2)   # the far side of the wall
    (far if beyond else near).append((fn, cd))
PL.paint_with(img, D, VIEW, cam, 0.0, [], layers=('back', 'mid', 'front'), beyond=[f for f, _ in far])
lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
for fn, _ in near:                                   # on the lens's side: in the cell's night, lit by the moonbeam
    fn(lay)
pcs['night'].draw(img, cam, 0.0)
if 'moonbeam' in pcs:
    mb = pcs['moonbeam']
    if near:
        import numpy as np
        mb.args['blockers'] = [(np.asarray(lay)[..., 3], near[0][1] - 0.1)]
    mb.draw(img, cam, 0.0)
    mb.args['blockers'] = []
if near:
    pcs['night'].draw(lay, cam, 0.0)
    if 'moonbeam' in pcs:
        PR.moon_on(lay, pcs['moonbeam'], cam, 0.0)
    img.alpha_composite(lay)
img.convert('RGB').save(OUT, quality=90)
print(OUT)
