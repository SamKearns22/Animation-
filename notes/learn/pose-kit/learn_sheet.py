import sys, os, time, json, traceback
sys.path.insert(0, 'source'); sys.path.insert(0, 'notes/learn/seated/solid')
import numpy as np
from PIL import Image
import sheet_solid as SH, solid_seat as SO, castsheet as CS, sitting as S, views as V
OUT = sys.argv[1]
SH.MODE = 'body'
VIEWS = SH.VIEWS + ((0, 'upright, apart', 'front apart'),)
res = {}
for who in ('kemi', 'blair', 'may'):
    for yaw, pose, n in VIEWS:
        key = f'{who} {n}'; t0 = time.time()
        try:
            im, chk = SH.tile(who, yaw, pose, full=True)
            chk = dict(chk)
            a = np.asarray(im)
            chk['seated_look'] = CS.seated_look(a, SH.cast[who]['trousers'], n, tones=(yaw != 90))
            if 'apart faults' not in chk and pose == 'upright, apart':
                chk['apart faults'] = SO.apart_faults(im, SH.cast[who])
            im.save(f'{OUT}/{who}-{n.replace(" ","_")}-body.png')
            # posted look: same pose, the posted drawing (no R7 switches)
            sp = dict(SH.cast[who]); img = Image.new('RGBA', (1080, 1920), (232, 232, 226, 255))
            s = 0.5 * sp['height'] / 1.75
            SH.V.person(img, SH.B.Cam(2.0, 540, 470), 540, 840 - 928 * s, s, sp, 0.0, yaw, S.pose(sp, pose))
            img.convert('RGB').save(f'{OUT}/{who}-{n.replace(" ","_")}-posted.png')
        except Exception as e:
            chk = {'ERROR': traceback.format_exc()[-600:]}
        res[key] = chk
        print(key, round(time.time() - t0, 1), json.dumps(chk, default=str)[:700], flush=True)
json.dump(res, open(f'{OUT}/checks.json', 'w'), default=str, indent=1)
