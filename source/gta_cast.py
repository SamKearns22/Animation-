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

B, V = PP.B, PP.V
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
    top = int(600 - 380 * k)
    return img.crop((540 - size[0] // 2, top, 540 + size[0] // 2, top + size[1])).convert('RGB')


def _font(n):
    return ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)


REF_OF = {'jason': 'sam-jason-lucia-bike-key-art.jpg', 'lucia': 'sam-lucia-portrait-art.jpg', 'her': None}
# the whole figure as the game draws it (GTA cast chat, Sam 20 Nov: "the correct body shapes"), beside the sheet
FIGURE_OF = {'jason': 'game-art-jason-lucia-launch.jpg', 'lucia': 'game-art-jason-lucia-robbery.jpg'}


CROPS = {'sam-jason-lucia-bike-key-art.jpg': (1126, 0, 2432, 1440),     # Jason, in Sam's key art
         'sam-lucia-portrait-art.jpg': None,
         'game-art-jason-lucia-launch.jpg': (300, 0, 800, 1440),          # Jason standing, head to knee
         'game-art-jason-lucia-robbery.jpg': (960, 150, 1660, 1440)}      # Lucia, head to thigh


def _ref(name, h):
    r = Image.open(os.path.join(REFS, name)).convert('RGB')
    if CROPS.get(name):
        r = r.crop(CROPS[name])
    r.thumbnail((10_000, h))
    return r


def sheet(out):
    """Rule 38 and 89: one row each: front, side and back at true heights (one scale for all three people), the
    bust large, then Sam's picture and the game's whole figure (GTA cast chat: shapes judged against the game)."""
    c = cast()
    tw, th = 270, 640
    rows = []
    for who in c:
        row = Image.new('RGB', (3600, th + 50), (232, 228, 222))
        d = ImageDraw.Draw(row)
        d.text((14, 8), c[who]['name'].split(' (')[0], font=_font(30), fill=(30, 30, 30))
        x = 10
        for k, yaw in enumerate((0, 90, 180)):
            tile = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
            s = 0.9 * c[who]['height'] / 1.85
            draw(tile, 540, 1720 - 928 * s, s, who, yaw)
            tile = tile.crop((300, 1720 - int(1240 * 0.9), 780, 1740)).convert('RGB')
            tile = tile.resize((int(tile.width * th / tile.height), th))
            row.paste(tile, (x, 46))
            x += tile.width - 20
        b = bust(who, size=(500, 600))
        b = b.resize((int(b.width * th / b.height), th))
        row.paste(b, (x + 10, 46))
        x += b.width + 24
        for name in (REF_OF.get(who), FIGURE_OF.get(who)):
            if name:
                r = _ref(name, th)
                row.paste(r, (x, 46))
                x += r.width + 12
        rows.append(row.crop((0, 0, x, row.height)))
    W = max(r.width for r in rows)
    img = Image.new('RGB', (W, 60 + sum(r.height for r in rows)), (232, 228, 222))
    ImageDraw.Draw(img).text((14, 12), 'Grand Theft Autism: the cast (front, side, back; face; Sam\'s picture; the game)',
                             font=_font(30), fill=(30, 30, 30))
    y = 60
    for r in rows:
        img.paste(r, (0, y))
        y += r.height
    img.save(out, quality=86)
    return out


def panels(out_dir):
    """One picture per person for the critique (rule 89): front, side, back at true height beside the bust."""
    os.makedirs(out_dir, exist_ok=True)
    c, outs = cast(), []
    for who in c:
        row = Image.new('RGB', (1500, 900), (232, 228, 222))
        for k, yaw in enumerate((0, 90, 180)):
            tile = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
            s = 0.75 * c[who]['height'] / 1.85
            draw(tile, 540, 1800 - 928 * s, s, who, yaw)
            tile = tile.crop((340, 1800 - int(1260 * s), 740, 1820)).convert('RGB')
            tile.thumbnail((300, 880))
            row.paste(tile, (k * 300, 10))
        b = bust(who)
        b.thumbnail((600, 880))
        row.paste(b, (900, 10))
        f = os.path.join(out_dir, f'{who}.jpg')
        row.save(f, quality=90)
        outs.append(f)
    return outs


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
    elif sys.argv[1] == 'panels':
        print(panels(sys.argv[2]))
    elif sys.argv[1] == 'busts':
        print(busts(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.0))
