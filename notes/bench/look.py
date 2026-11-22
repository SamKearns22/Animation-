"""look.py OUT.jpg F1 F2 ...: each frame solved, checked and drawn from four sides (shot 4's camera, outside the
window, the front, above), crossing points red; one row a frame, the faults written under it. A viewer's look."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'source'))
import bench_move as M
from PIL import Image, ImageDraw
M.fit_seat(); M.fit_knee(); M.fit_ankles()
out_p, fr = sys.argv[1], list(map(int, sys.argv[2:]))
views = ('shot', 'outside', 'front', 'above')
w, h = 300, 533
sheet = Image.new('RGB', (w * len(views), (h + 40) * len(fr)), (255, 255, 255))
d = ImageDraw.Draw(sheet)
for r, i in enumerate(fr):
    t = i / 24
    g = M.goals_at(t); o = M.solve(g); c = M.check_frame(o, g)
    bad = {k: v for k, v in c.items() if k in ('car', 'self', 'pistol', 'rom') and v}
    for k, v in enumerate(views):
        sheet.paste(M.draw_view(o, v, t, (w, h)), (k * w, r * (h + 40)))
    d.text((4, r * (h + 40) + h + 2), 'frame %d (%.2f s) %s' % (i, t, str(bad)[:180] or 'clean'), fill=(0, 0, 0))
    print(i, bad or 'clean', flush=True)
sheet.save(out_p, quality=88)
