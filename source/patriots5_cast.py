#!/usr/bin/env python3
"""MAP  The Patriot 5 (Sam, 27 Nov: "run The Patriot character through our new drawing style"): the Patriot on the
house head (facehouse: the measured head, house eyes and brows, the turned views) under the house balaclava
(facehouse_d), on the people kit's body, in The Patriots' own clothes (patriots3_cast: the black jacket with grey
sleeves, stand collar, zip and ribbed hem, the belly, the PP and doodle badges, the poppy, olive combat trousers with
cargo pockets, black boots). No photos: he is fictional and masked; his face under the knit is the average face pushed
thick-set (references/faces/patriot/pick, made by hand).

  patriot(mood) ..... his person (sp) and pose (j), ready for views.person; mood: MOODS key
  draw(img, cam, x, y, s, sp, j, yaw) .. one drawing of him
  sheet(OUT) ........ every view full length on one floor at 1.78 m, beside a 1.75 m person, the five turns of his
                      head large, his moods large (python3 source/patriots5_cast.py sheet OUT.jpg)
  tables: LINES, MOODS
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from PIL import Image, ImageDraw, ImageFont   # noqa: E402
import facehouse as F                         # noqa: E402
import patriots3_cast as P3                   # noqa: E402  (his clothes; it also hangs the badges and cargo pockets)
import people_parts as PP                     # noqa: E402

LINES = dict(hair='bald', outfit=('jumper', P3.JACKET), height=1.78, dome=-0.33, dome_wide=0.42, head=False,
             balaclava=True, eye_scale=1.2, liner=3.0)
BODY = dict(sleeve=P3.SLEEVE, trousers=P3.COMBAT, shoe=(22, 20, 22), shoulders=168, bottom=500, patches=True,
            belly=True, cargo=True, neck_c=F.BALA, neck_w=1.2, figure='stout', name='Patriot')
MOODS = {   # the house moods (the old sheet's rest, talking, cross, scared), in the house face's own keys
    'rest': dict(),
    'talking': dict(mouth='v:AI'),
    'cross': dict(frown=0.03, brow_up=-0.01, lid4=0.3),
    'scared': dict(brow_up=0.05, lid4=0.0, look=0.0),
    'stare': dict(brow_up=0.035, lid4=0.0),
}


def patriot(mood='rest'):
    import views as V
    sp = F.person('patriot', 'detail', **dict(LINES))
    sp.update(BODY)
    sp.update(MOODS[mood])
    j = V.standing(sp)
    j['body_props'] = [P3.patriot_jacket] + j.get('body_props', [])
    j['_dressed'] = True
    return sp, j


_READY = []


def install():
    if _READY:
        return
    from satire_style import install_circle_hands
    install_circle_hands(PP.B)
    TC = F.install()
    F.install_turned()
    TC.HEADS['patriot'] = F.house_head
    _READY.append(TC)


def draw(img, cam, x, y, s, sp, j, yaw=0):
    install()
    P3.FROM_BEHIND[0] = yaw in (135, 180)
    return PP.V.person(img, cam, x, y, P3.scale_for(sp, s), dict(sp, full=True, pose='custom'), 0.0, yaw, j)


def sheet(out):
    import body as B
    install()
    B.SS = 1
    W, H = 2900, 2500
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 40)
    small = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 26)
    d.text((30, 16), 'THE PATRIOT 5: the Patriot in the new house style', font=big, fill=(30, 30, 30))
    floor = 1380
    views = [(0, 'front'), (45, 'three-quarter'), (90, 'side'), (135, '3/4 back'), (180, 'back')]
    for i, (yaw, name) in enumerate(views):
        sp, j = patriot()
        x = 230 + i * 440
        cam = B.Cam(1.0, 0, 0)
        tile = Image.new('RGBA', (1080, 2600), (0, 0, 0, 0))
        draw(tile, B.Cam(1.0, 540, 960), 540, 1500, 0.62, sp, j, yaw)
        bb = tile.getbbox()
        part = tile.crop(bb)
        img.alpha_composite(part, (x - part.width // 2, floor - part.height))
        d.text((x - 60, floor + 14), name, font=small, fill=(30, 30, 30))
    # a 1.75 m person beside him (grey): his height against it
    tile = Image.new('RGBA', (1080, 2600), (0, 0, 0, 0))
    sp, j = patriot()
    draw(tile, B.Cam(1.0, 540, 960), 540, 1500, 0.62, sp, j, 0)
    bb = tile.getbbox()
    h175 = int((bb[3] - bb[1]) * 1.75 / 1.78)
    x = 230 + 5 * 440
    d.rounded_rectangle([x - 60, floor - h175 + 110, x + 60, floor], 26, fill=(150, 150, 160))
    d.ellipse([x - 45, floor - h175, x + 45, floor - h175 + 100], fill=(150, 150, 160))
    d.text((x - 110, floor + 14), 'Patriot 1.78 m', font=small, fill=(30, 30, 30))
    # the head turned, large; then his moods, large
    T = 420
    for row, items in enumerate(([(n, yaw, 'rest') for yaw, n in views],
                                 [(m, 0, m) for m in MOODS])):
        y = 1490 + row * (T + 70)
        for k, (label, yaw, mood) in enumerate(items):
            sp, j = patriot(mood)
            tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
            draw(tile, B.Cam(1.0, 540, 960), 540, 900, 1.6, sp, j, yaw)
            crop = tile.crop((150, 230, 930, 1010)).convert('RGBA').resize((T, T))
            img.alpha_composite(crop, (60 + k * (T + 120), y))
            d.text((60 + k * (T + 120), y + T + 8), label, font=small, fill=(30, 30, 30))
    a = img.convert('RGB')                        # the empty band over the figures taken out
    top = min(r for r in range(70, floor) if any(px != (232, 228, 222) for px in a.crop((0, r, W, r + 1)).getdata())) - 30
    a = Image.fromarray(__import__('numpy').vstack([__import__('numpy').asarray(a)[:70], __import__('numpy').asarray(a)[top:]]))
    a.save(out, quality=88)
    return out


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    else:
        print(__doc__)
