import sys, pickle, numpy as np
from PIL import Image, ImageDraw, ImageFont
tiles = pickle.load(open(sys.argv[1], 'rb')); out = sys.argv[2]; mode = sys.argv[3] if len(sys.argv) > 3 else 'colour'
names = ['front', 'three-quarter', 'side', 'back', 'seated 3/4']
rows = [('may', None), ('may', 'woman'), ('kemi', None), ('kemi', 'woman'), ('blair', None)]
def crop(a):
    m = (a < 245).any(2)
    ys, xs = np.where(m)
    return a[max(0,ys.min()-10):ys.max()+10, max(0,xs.min()-10):xs.max()+10], m[max(0,ys.min()-10):ys.max()+10, max(0,xs.min()-10):xs.max()+10]
H = 520; W = 300
img = Image.new('RGB', (180 + W*5, 40 + (H+20)*len(rows)), (236,233,226))
d = ImageDraw.Draw(img)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
except: f = None
for i, n in enumerate(names): d.text((180 + i*W + 10, 8), n, fill=(60,60,60), font=f)
for r, (who, b) in enumerate(rows):
    label = {'may':'May','kemi':'Kemi','blair':'Blair (man)'}[who] + ('\n+ woman\n  build' if b else '\n as now')
    d.text((10, 40 + r*(H+20) + 200), label, fill=(30,30,30), font=f)
    for i, n in enumerate(names):
        a, m = crop(tiles[(who, b, n)])
        if mode == 'outline':
            a = np.where(m[..., None], 20, 255).astype(np.uint8).repeat(3, 2) if a.ndim == 2 else np.where(m[..., None], np.uint8(20), np.uint8(255)) * np.ones_like(a)
        t = Image.fromarray(a.astype(np.uint8))
        k = min((W-20)/t.width, (H-10)/t.height); t = t.resize((int(t.width*k), int(t.height*k)))
        img.paste(t, (180 + i*W + (W - t.width)//2, 40 + r*(H+20) + (H - t.height)))
img.save(out, quality=88); print(out, img.size)
