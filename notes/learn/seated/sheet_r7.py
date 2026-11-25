"""R7's before/after sheet for Sam (chat 2): his marked frame (BEFORE) beside May, Kemi and Blair seated on R7's lower
body (front, three-quarter, side), waist to feet, at the size a phone shows. python3 notes/learn/seated/sheet_r7.py OUT"""
import os, sys
sys.path.insert(0, 'source')
from PIL import Image, ImageDraw, ImageFont
import castsheet as CS
import sitting as S
HERE = os.path.dirname(os.path.abspath(__file__))
cast, PP = CS._setup('brexit-is-done', None)
B, V = PP.B, PP.V
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
f1, f2, f3 = ImageFont.truetype(F, 40), ImageFont.truetype(F, 30), ImageFont.truetype(F, 28)


def tile(who, yaw):
    sp = dict(cast[who]); sp['seat_r7'] = True
    img = Image.new('RGBA', (1080, 1920), (232, 232, 226, 255))
    s = 0.5 * sp['height'] / 1.75
    V.person(img, B.Cam(2.0, 540, 470), 540, 840 - 928 * s, s, sp, 0.0, yaw, S.pose(sp, 'upright'))
    return img.convert('RGB').crop((240, 1180, 840, 1740))      # from the hands to the feet


sam = Image.open(os.path.join(HERE, 'no-bum-circular-knees-sam.jpg')).convert('RGB')
sam = sam.resize((int(sam.width * 1600 / sam.height), 1600))
cols, rows = ('front', 'three-quarter', 'side'), ('May', 'Kemi', 'Blair')
tw, th = 600, 560
W = sam.width + 60 + 160 + 3 * (tw + 20)
H = 120 + 3 * (th + 20)
page = Image.new('RGB', (W, max(H, sam.height + 120)), 'white'); d = ImageDraw.Draw(page)
d.text((10, 10), 'BEFORE: your note', fill=(150, 20, 20), font=f1)
d.text((10, 60), '"No bum / circular knees"', fill=(60, 60, 60), font=f3)
page.paste(sam, (0, 110))
x0 = sam.width + 30
d.line([(x0, 0), (x0, page.height)], fill=(170, 170, 170), width=4)
d.text((x0 + 30, 10), 'AFTER (v2): the new seated lower body, every new film', fill=(20, 110, 40), font=f1)
for c, name in enumerate(cols):
    d.text((x0 + 190 + c * (tw + 20) + tw // 2 - 90, 66), name, fill='black', font=f2)
for r, who in enumerate(rows):
    y = 110 + r * (th + 20)
    d.text((x0 + 30, y + th // 2 - 15), who, fill='black', font=f2)
    for c, yaw in enumerate((0, 45, 90)):
        page.paste(tile(who.lower(), yaw), (x0 + 190 + c * (tw + 20), y))
page = page.resize((page.width * 2 // 3, page.height * 2 // 3), Image.LANCZOS)
page.save(sys.argv[1], quality=85)
print(sys.argv[1], os.path.getsize(sys.argv[1]) // 1024, 'KB')
