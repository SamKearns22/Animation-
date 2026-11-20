#!/usr/bin/env python3
"""MAP  Grand Theft Autism's cast (chat 4, 20 Nov). The three people come from the people kit's plain lines in
story/grand-theft-autism-people.txt (Jason, Lucia, her); this file only loads them, adds what the film needs on top
(Jason's pistol is prepper_cast's Glock; her fidget spinner), and draws the cast sheet: front, side and back at
true heights (rule 38), each face large beside its game reference (rule 89).

    python3 source/gta_cast.py sheet OUT.jpg          the cast sheet (front, side, back; faces beside references)
    python3 source/gta_cast.py busts OUT.jpg [YAW]    the three seated busts as the windscreen sees them

Map: load 25 | bust (one person, waist up) 40 | sheet 70 | main 110
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import people as PK                                  # noqa: E402  the people kit
import people_parts as PP                            # noqa: E402
from satire_style import install_circle_hands       # noqa: E402

B, V = PP.B, PP.AV.MC.V
FILM = 'grand-theft-autism'
REFS = os.path.join(ROOT, 'references', FILM)
_CAST = None


def cast():
    """The three people, installed on the engine once (views.person draws them)."""
    global _CAST
    if _CAST is None:
        install_circle_hands(B)
        _CAST = PK.install(PK.load(FILM))
        B.SS = 1
    return _CAST


def draw(img, x, y, s, who, yaw=0.0, t=0.0, joints=None, head_yaw=None, **over):
    """One person with the neck base at (x, y) in pixels, s pixels per rig unit (soles 928 units below)."""
    sp = dict(cast()[who], **over)
    cam = B.Cam(1.0, img.width / 2, img.height / 2)
    return V.person(img, cam, x, y, s, sp, t, yaw, joints, head_yaw)


def bust(who, yaw=0.0, size=(500, 560), s=1.0, **over):
    """One person from the waist up, large (the windscreen's framing)."""
    img = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
    sp = cast()[who]
    k = s * sp['height'] / 1.85
    draw(img, 540, 600, k, who, yaw, **over)
    top = int(600 - 300 * k)
    return img.crop((540 - size[0] // 2, top, 540 + size[0] // 2, top + size[1])).convert('RGB')


def _font(n):
    return ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)


REF_OF = {'jason': 'jason-portrait.jpg', 'lucia': 'lucia-portrait.jpg', 'her': None}


def sheet(out):
    """Rule 38 and 89: front, side and back at true heights, then each bust large beside its reference."""
    c = cast()
    tw, th = 300, 620
    img = Image.new('RGB', (40 + 3 * 3 * tw, 80 + th + 620), (232, 228, 222))
    d = ImageDraw.Draw(img)
    d.text((20, 18), 'Grand Theft Autism: the cast (front, side, back; busts beside the game)', font=_font(32),
           fill=(30, 30, 30))
    for i, who in enumerate(c):
        for k, yaw in enumerate((0, 90, 180)):
            tile = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
            s = 0.9 * c[who]['height'] / 1.85
            draw(tile, 540, 1700 - 928 * s, s, who, yaw)
            tile = tile.crop((290, 1700 - int(1180 * s), 790, 1720)).convert('RGB')
            tile.thumbnail((tw, th - 40))
            x0 = 20 + (i * 3 + k) * tw
            img.paste(tile, (x0, 80 + 30))
            d.text((x0 + 6, 80), f"{c[who]['name'].split(' (')[0]} {('front', 'side', 'back')[k]}", font=_font(18),
                   fill=(30, 30, 30))
        y0 = 80 + th
        b = bust(who)
        b.thumbnail((450, 520))
        img.paste(b, (20 + i * 3 * tw, y0))
        if REF_OF[who]:
            r = Image.open(os.path.join(REFS, REF_OF[who])).convert('RGB')
            r.thumbnail((430, 520))
            img.paste(r, (20 + i * 3 * tw + 460, y0))
    img.save(out, quality=88)
    return out


def busts(out, yaw=0.0):
    ims = [bust(w, yaw) for w in cast()]
    img = Image.new('RGB', (sum(i.width for i in ims), ims[0].height), (232, 228, 222))
    x = 0
    for i in ims:
        img.paste(i, (x, 0))
        x += i.width
    img.save(out, quality=88)
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    elif sys.argv[1] == 'busts':
        print(busts(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.0))
