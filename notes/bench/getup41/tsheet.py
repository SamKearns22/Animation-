"""tsheet.py OUT.jpg t1,t2,... [views]: solved frames at times, several views, checks under each (scratch)."""
import sys, os
sys.path.insert(0, '/home/user/Animation-/source')
import bench_move as M
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import it
if len(sys.argv) > 4: it.load(sys.argv[4])
from PIL import Image, ImageDraw
M.fit_seat(); M.fit_knee(); M.fit_ankles()
ts = [float(x) for x in sys.argv[2].split(',')]
views = sys.argv[3].split(',') if len(sys.argv) > 3 else ['front', 'above', 'outside']
w = 260; h = int(w * 16 / 9)
sheet = Image.new('RGB', (w * len(ts), (h + 50) * len(views)), (255, 255, 255))
d = ImageDraw.Draw(sheet)
for ci, t in enumerate(ts):
    g = M.goals_at(t); o = M.solve(g); c = M.check_frame(o, g)
    for ri, v in enumerate(views):
        sheet.paste(M.draw_view(o, v, t, (w, h)), (ci * w, ri * (h + 50)))
        bad = {k: v2 for k, v2 in c.items() if k in ('car', 'self', 'pistol', 'rom') and v2}
        txt = '%.3f %s' % (t, ' '.join('%s %s' % (n, (v3[1] if isinstance(v3, tuple) else v3)) for kk in bad for n, v3 in bad[kk].items()) or 'clean')
        if ri == 0:
            print(txt, flush=True)
        for li in range(3):
            d.text((ci * w + 4, ri * (h + 50) + h + 2 + li * 14), txt[li * 42:(li + 1) * 42], fill=(0, 0, 0))
sheet.save(sys.argv[1], quality=85)
