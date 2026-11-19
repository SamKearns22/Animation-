"""Test only (job 1, 19 Nov): Andy and Kemi drawn front-on with a focus, beside the current turned view. Changes nothing."""
import os, sys
sys.path.insert(0, '/home/user/Animation-/source')
os.chdir('/home/user/Animation-')
import people as PK, people_parts as PP
from PIL import Image, ImageDraw, ImageFont
from satire_style import install_circle_hands
B, V = PP.B, PP.AV.MC.V
install_circle_hands(B)
a = PK.load('milburn'); k = PK.load('facetool')
print('milburn', list(a)); print('facetool', list(k))
cast = PK.install({'andy': a['burnham'] if 'burnham' in a else a[[w for w in a if 'burn' in w or 'andy' in w][0]],
                   'kemi': k[[w for w in k if 'baden' in w or 'kemi' in w][0]]})
B.SS = 1
cam = B.Cam(1.0, 540, 960)
F = lambda n: ImageFont.truetype('source/fonts/DejaVuSans-Bold.ttf', n)
VARS = [('NOW: turned 45 (3/4 route)', 45, {}, {}),
        ('front, no focus', 0, {}, {}),
        ('front-on, focus RIGHT: eyes', 0, dict(look=0.9), {}),
        ('focus RIGHT: eyes + tilt + lean', 0, dict(look=0.9), dict(head_roll=-6.0, lean=3.0)),
        ('focus LEFT: eyes + tilt', 0, dict(look=-0.9), dict(head_roll=6.0)),
        ('focus RIGHT, wary: eyes, brow, lid', 0, dict(look=0.9, brow_up=0.03, frown=-0.01, lid4=0.12), dict(head_roll=-4.0))]
BOX = tuple(int(v) for v in os.environ.get('BOX', '340 150 740 640').split())
tw, th = 330, 400
img = Image.new('RGB', (tw * len(VARS), 60 + 2 * (th + 40)), (236, 232, 226))
d = ImageDraw.Draw(img)
d.text((10, 10), 'Front-on focus test (19 Nov): Andy and Kemi unchanged; only eyes, tilt and mood set per tile', font=F(22), fill=(30, 30, 30))
for r, w in enumerate(('andy', 'kemi')):
    sp = cast[w]
    s = 0.5 * sp['height'] / 1.75
    for c, (lab, yaw, mood, j) in enumerate(VARS):
        tile = Image.new('RGBA', (1080, 1920), (236, 232, 226, 255))
        jj = dict(V.standing(sp), **j)
        V.person(tile, cam, 540, 840 - 928 * s, s, dict(sp, **mood), 0.0, yaw, jj)
        tile = tile.crop(BOX).resize((tw - 10, int((tw - 10) * (BOX[3]-BOX[1]) / (BOX[2]-BOX[0]))))
        tile = tile.crop((0, 0, tw - 10, th))
        y = 50 + r * (th + 40)
        img.paste(tile.convert('RGB'), (c * tw + 5, y + 30))
        d.text((c * tw + 8, y + 6), f'{w.title()}: {lab}', font=F(15), fill=(30, 30, 30))
out = sys.argv[1]
img.save(out, quality=88); print(out)
