#!/usr/bin/env python3
"""Patriots 4: the rough composition sheet (film-quality rule 11): the key shots through the plan's own cameras, the
room as plain blocks (sets.house), the cast as rough stand-ins on their plan marks (the Patriot is his real drawing;
Claudia, Romesh and Bash are colour stand-ins until their likeness heads are built), and the plan from above.
For Sam to approve the layout and the joke before anything is built.

    python3 source/patriots4_compose.py OUT.jpg
"""
import math
import os
import sys
from types import SimpleNamespace

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import views as V                # noqa: E402
import sets as S                 # noqa: E402
import plan as PLN               # noqa: E402
import patriots3_cast as C       # noqa: E402
import patriots4_plan as PL      # noqa: E402

M = V.M_PER_UNIT
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
FILM = SimpleNamespace(NAME='patriots4', PLAN=dict(CEIL=PL.CEIL, ROOMS=PL.ROOMS, OPENINGS=PL.OPENINGS, LOOKS=PL.LOOKS,
                                                    THINGS=PL.THINGS, PEOPLE=PL.PEOPLE, CAMS=PL.CAMS,
                                                    GROUPS=PL.GROUPS), SHOTS=[])
STAND_INS = {   # rough: colours and build only
    'patriot': C.PATRIOT,
    'claudia': dict(name='Claudia', skin=(232, 196, 172), hw=62, hh=88, jaw='soft', hair='bob', hair_c=(22, 20, 22),
                    outfit='suit', jacket=(28, 26, 30), sleeve=(28, 26, 30), trousers=(28, 26, 30),
                    shoe=(20, 20, 20), shoulders=140, lashes=True, mouth='set', seed=41),
    'romesh': dict(name='Romesh', skin=(176, 120, 86), hw=66, hh=98, jaw='long', hair='crop', hair_c=(28, 26, 28),
                   beard='full', beard_c=(54, 50, 50), glasses=True, outfit='suit', jacket=(170, 82, 40),
                   sleeve=(170, 82, 40), trousers=(170, 82, 40), shoe=(236, 234, 228), shoulders=152, mouth='set',
                   seed=42),
    'bash': dict(name='Bash', skin=(236, 204, 182), hw=60, hh=94, jaw='long', hair='side', hair_c=(96, 64, 40),
                 outfit='suit', jacket=(36, 44, 52), sleeve=(36, 44, 52), trousers=(36, 44, 52), shoe=(30, 26, 22),
                 shoulders=146, mouth='set', seed=43),
}


def cam(name):
    c = PL.CAMS[name]
    return S.Cam(c['pos'], c['look'], focal=c['focal'])


def figure(img, cm, who, arms=None):
    p = PL.PEOPLE[who]
    sp = STAND_INS[who]
    spot = C.Spot(sp, *p['at'])
    neck = spot.to_world((0.0, 0.0, 0.0))
    if cm.depth(neck) < 0.3:
        return
    (x, y), k = cm.project(neck)
    bx, bz = cm.pos[0] - p['at'][0], cm.pos[2] - p['at'][1]
    yaw = (math.degrees(math.atan2(bx, bz)) - p['facing'] + 540) % 360 - 180
    j = V.standing(sp)
    for side, tgt in (arms or {}).items():
        V.arm_to(j, side, tgt, 'down', 'fist')
    flat = B.Cam(1.0, 540, 960)
    flat.P = lambda a, b: (a, b)
    flat.S = lambda v: v
    C.person(img, flat, x, y, k * M, sp, 0.0, yaw, j)


def table(img, cm):
    """The table top (drawn over the people: it hides them below about 0.8 m) and the coin pile as gold tiers."""
    wood = dict(side=(110, 66, 40), top=(132, 80, 50))
    gold = dict(side=(196, 150, 50), top=(226, 186, 80))
    parts = [S.cylinder((0.0, PL.TABLE_H - 0.05, 0.0), 0.65, 0.05, wood, n=40)]
    for i in range(7):
        parts.append(S.cylinder((0.0, PL.TABLE_H + i * 0.042, 0.0), 0.28 * (1 - i / 8), 0.042, gold, n=28))
    S.draw_parts(img, cm, parts)


def shot(name, people, arms=None):
    cm = cam(name)
    img = B.canvas((255, 255, 255))
    S.house(img, cm, FILM)
    order = sorted(people, key=lambda w: -cm.depth(C.Spot(STAND_INS[w], *PL.PEOPLE[w]['at']).to_world((0, 0, 0))))
    for w in order:
        figure(img, cm, w, (arms or {}).get(w))
    table(img, cm)
    return img


def tile(img, label, w=540, h=960):
    im = img.convert('RGB').resize((w, h))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 20)
    d.rectangle((0, h - 92, w, h), fill=(255, 255, 255))
    for i, line in enumerate(label.split('\n')):
        d.text((10, h - 86 + 26 * i), line, font=f, fill=(20, 20, 20))
    return im


def sheet(out):
    B.SS = 1
    point = {'R': (330.0, 40.0, 250.0), 'L': (-330.0, 40.0, 250.0)}
    everyone = ['claudia', 'patriot', 'romesh', 'bash']
    shots = [
        (shot('claudia', everyone), 'Shots 1, 4: across the coins at Claudia\n"Romesh and Bash, remind us..."\nHook Text over the arch'),
        (shot('bash', everyone), 'Shot 2: circle round the coins to Bash\n"...Choose Love..." (hands at chest)'),
        (shot('romesh', everyone), 'Shot 3: on round to Romesh (7 o\'clock)\n"...the Refugee Council."\nRound Table hall far behind him'),
        (shot('patriot', everyone), 'Shot 5: "And what about you?" -\ncircle to her left: the Patriot,\neyes widen: "Errrrrrr"'),
        (shot('his view', everyone), "Shot 9: over the Patriot's shoulder:\nRomesh and Bash slide their eyes\nto each other"),
        (shot('patriot', everyone, {'patriot': point}), 'Shot 12: both arms out, a finger at\neach, narrowed eyes: "Traitors."'),
    ]
    tiles = [tile(im, lab) for im, lab in shots]
    top = os.path.join(os.path.dirname(os.path.abspath(out)), '_p4_plan_top.jpg')
    PLN.sketch(FILM, top)
    pim = Image.open(top).convert('RGB')
    pim.thumbnail((540, 868))
    pt = Image.new('RGB', (540, 960), 'white')
    pt.paste(pim, ((540 - pim.width) // 2, 0))
    tiles.append(tile(pt, 'The plan from above (metres): arch at\nthe top, Round Table hall at the bottom;\nthe camera circles the coins (blue)'))
    os.remove(top)
    cols = 4
    W = Image.new('RGB', (550 * cols + 10, 975 * 2 + 90), (235, 232, 226))
    d = ImageDraw.Draw(W)
    d.text((20, 20), 'PATRIOTS 4: rough composition (rule 11): layout and joke only, not the drawing. '
           'Claudia, Romesh and Bash are colour stand-ins.', font=ImageFont.truetype(FONT, 30), fill=(20, 20, 20))
    for i, t in enumerate(tiles):
        W.paste(t, (10 + (i % cols) * 550, 80 + (i // cols) * 975))
    W.save(out, quality=84)
    return out


if __name__ == '__main__':
    print(sheet(sys.argv[1]))
