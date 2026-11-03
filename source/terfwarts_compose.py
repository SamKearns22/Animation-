#!/usr/bin/env python3
"""Terfwarts: the rough composition sheet (film-quality rule 11): the key shots through the plan's own cameras, the
places as plain blocks (sets.house), the cast as rough colour stand-ins on their plan marks, Myrtle see-through, the
Hat as a rough cone, and the plan from above. For Sam to approve layout and joke before anything is built.

    python3 source/terfwarts_compose.py OUT.jpg
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
import moves as MV               # noqa: E402
import sets as S                 # noqa: E402
import plan as PLN               # noqa: E402
import patriots3_cast as C       # noqa: E402
import terfwarts_plan as PL      # noqa: E402

M = V.M_PER_UNIT
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
FILM = SimpleNamespace(NAME='terfwarts', PLAN=dict(CEIL=PL.CEIL, ROOMS=PL.ROOMS, OPENINGS=PL.OPENINGS, LOOKS=PL.LOOKS,
                                                   THINGS=PL.THINGS, PEOPLE=PL.PEOPLE, CAMS=PL.CAMS,
                                                   GROUPS=PL.GROUPS), SHOTS=[])
ROBE = dict(outfit='suit', jacket=(28, 26, 30), sleeve=(28, 26, 30), trousers=(40, 40, 44), shoe=(20, 20, 20))
STAND_INS = {   # rough: colours and build only (the likeness heads come at the cast sheet)
    'harry': dict(name='Harry', skin=(240, 214, 196), hw=64, hh=86, jaw='soft', hair='crop', hair_c=(44, 34, 28),
                  glasses=True, shoulders=128, mouth='set', seed=51, **ROBE),
    'ron': dict(name='Ron', skin=(244, 216, 198), hw=68, hh=84, jaw='soft', hair='wavy', hair_c=(196, 92, 40),
                shoulders=134, mouth='set', seed=52, **ROBE),
    'myrtle': dict(name='Myrtle', skin=(230, 226, 220), hw=60, hh=86, jaw='soft', hair='long', hair_c=(40, 34, 30),
                   glasses=True, lashes=True, outfit='suit', jacket=(120, 130, 120), sleeve=(120, 130, 120),
                   trousers=(90, 96, 90), shoe=(40, 40, 40), shoulders=128, mouth='set', seed=53),
}
C.HEIGHTS.update({'Harry': 1.42, 'Ron': 1.47, 'Myrtle': 1.50})


def cam(name):
    c = PL.CAMS[name]
    return S.Cam(c['pos'], c['look'], focal=c['focal'])


def figure(img, cm, mark, j=None, lift=0.0, at=None, ghost=False):
    p = PL.PEOPLE[mark]
    sp = STAND_INS[p['who']]
    ax, az = at or p['at']
    spot = C.Spot(sp, ax, az)
    neck = spot.to_world((0.0, 0.0, 0.0))
    neck = (neck[0], neck[1] + lift - (V.SEAT_DROP * spot.k if j is not None and j.get('seated') else 0.0), neck[2])
    if cm.depth(neck) < 0.3:
        return None
    (x, y), k = cm.project(neck)
    bx, bz = cm.pos[0] - ax, cm.pos[2] - az
    yaw = (math.degrees(math.atan2(bx, bz)) - p['facing'] + 540) % 360 - 180
    flat = B.Cam(1.0, 540, 960)
    flat.P = lambda a, b: (a, b)
    flat.S = lambda v: v
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)) if ghost else img
    jj = j or V.standing(sp)
    if j is not None and j.get('seated'):
        jj = dict(jj, bob=0.0)
    C.person(lay, flat, x, y, k * M, sp, 0.0, yaw, jj)
    if ghost:                                        # see-through pale blue (refs myrtle-1/2/3), no glow
        r, g, b, a = lay.split()
        grey = Image.merge('RGB', (r, g, b)).convert('L')
        tint = Image.merge('RGB', (grey.point(lambda v: int(v * 0.55 + 40)), grey.point(lambda v: int(v * 0.75 + 50)),
                                   grey.point(lambda v: int(v * 0.6 + 100))))
        tint.putalpha(a.point(lambda v: int(v * 0.6)))
        img.alpha_composite(tint)
    return x, y, k * M * C.HEIGHTS[sp['name']] / 1.75


def hat(img, x, y, s, talk=True):
    """The Sorting Hat, rough: a slumped brown point, wide floppy brim, a fold for a brow and a mouth (refs)."""
    d = ImageDraw.Draw(img)
    hy = y - 228 * s                                  # the brim sits low, over the eyebrows (refs sorting-hat-scene)
    br = [(x - 190 * s, hy + 30 * s), (x - 120 * s, hy - 10 * s), (x + 120 * s, hy - 10 * s), (x + 200 * s, hy + 34 * s),
          (x + 90 * s, hy + 55 * s), (x - 90 * s, hy + 55 * s)]
    cone = [(x - 100 * s, hy + 10 * s), (x - 70 * s, hy - 160 * s), (x - 10 * s, hy - 250 * s), (x + 70 * s, hy - 300 * s),
            (x + 40 * s, hy - 200 * s), (x + 90 * s, hy + 10 * s)]
    d.polygon(br, fill=(110, 78, 50), outline=(20, 16, 14), width=3)
    d.polygon(cone, fill=(126, 88, 56), outline=(20, 16, 14), width=3)
    d.line([(x - 55 * s, hy - 120 * s), (x - 10 * s, hy - 105 * s), (x + 40 * s, hy - 122 * s)], fill=(60, 40, 26), width=5)
    if talk:
        d.polygon([(x - 50 * s, hy - 60 * s), (x + 50 * s, hy - 62 * s), (x + 30 * s, hy - 20 * s), (x - 34 * s, hy - 22 * s)],
                  fill=(40, 24, 16), outline=(20, 16, 14))


def plaque(img, cm):
    c = PL.THINGS['brass plaque']
    (x, y), k = cm.project((PL.DOOR_X, c['y'], 25.97))
    d = ImageDraw.Draw(img)
    w, h = 0.34 * k / 2, 0.10 * k / 2
    d.rectangle((x - w, y - h, x + w, y + h), fill=(196, 160, 70), outline=(30, 24, 16), width=2)
    d.text((x, y), 'GIRLS', font=ImageFont.truetype(FONT, max(10, int(h * 1.3))), fill=(30, 24, 16), anchor='mm')


def door(img, cm):
    """The shrunk carved door (rough panels) in its pointed arch."""
    d = ImageDraw.Draw(img)
    pts = lambda q: [cm.project(p)[0] for p in q]
    x0, x1, z = PL.DOOR_X - 0.5, PL.DOOR_X + 0.5, 25.99
    arch = [(x0 - 0.12, 0.0, z), (x0 - 0.12, 1.75, z), (PL.DOOR_X, 2.35, z), (x1 + 0.12, 1.75, z), (x1 + 0.12, 0.0, z)]
    leaf = [(x0, 0.0, z), (x0, 1.7, z), (PL.DOOR_X, 2.1, z), (x1, 1.7, z), (x1, 0.0, z)]
    d.polygon(pts(arch), fill=(176, 150, 110), outline=(20, 16, 14), width=3)
    d.polygon(pts(leaf), fill=(110, 72, 40), outline=(20, 16, 14), width=3)
    d.line(pts([(PL.DOOR_X, 0.0, z), (PL.DOOR_X, 2.1, z)]), fill=(20, 16, 14), width=2)
    for i in range(4):
        for xx in (x0 + 0.1, PL.DOOR_X + 0.08):
            yy = 0.2 + i * 0.38
            d.rectangle([*cm.project((xx, yy + 0.3, z))[0], *cm.project((xx + 0.32, yy, z))[0]], outline=(60, 38, 20), width=2)
    plaque(img, cm)


def students(img, cm):
    """Rough backs at the long tables (the real crowd is built varied: satire.md 'The look')."""
    for side in (-1, 1):
        for i in range(10):
            z = 21.0 - i * 1.2
            xw = side * (3.4 - 0.75)
            sp = dict(STAND_INS['ron' if i % 3 == 0 else 'harry'], glasses=False, seed=60 + i,
                      hair_c=[(44, 34, 28), (120, 80, 40), (30, 26, 24), (200, 170, 110)][i % 4])
            spot = C.Spot(sp, xw, z)
            neck = spot.to_world((0, 0, 0))
            neck = (neck[0], neck[1] - V.SEAT_DROP * spot.k, neck[2])
            if cm.depth(neck) < 0.5:
                continue
            (x, y), k = cm.project(neck)
            flat = B.Cam(1.0, 540, 960)
            flat.P = lambda a, b: (a, b)
            flat.S = lambda v: v
            C.person(img, flat, x, y, k * M, sp, 0.0, 90 * side, MV.seated(sp))


def shot(name, people, extra=None):
    cm = cam(name)
    img = B.canvas((255, 255, 255))
    S.house(img, cm, FILM)
    if extra:
        extra(img, cm, 'under')
    out = {}
    order = sorted(people, key=lambda e: -cm.depth((e[1].get('at', PL.PEOPLE[e[0]]['at'])[0], 1.0,
                                                    e[1].get('at', PL.PEOPLE[e[0]]['at'])[1])))
    for mark, kw in order:
        out[mark] = figure(img, cm, mark, **kw)
    if extra:
        extra(img, cm, 'over', out)
    return img


def hall_extra(img, cm, when, out=None):
    if when == 'under':
        students(img, cm)
    elif out.get('harry hall'):
        x, y, s = out['harry hall']
        hat(img, x, y, s, talk=cam is not None)


def door_extra(img, cm, when, out=None):
    if when == 'under':
        door(img, cm)


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
    sit = MV.seated(STAND_INS['harry'])
    run_h = dict(at=(PL.DOOR_X - 0.4, 20.5))
    run_r = dict(at=(PL.DOOR_X + 0.45, 19.6))
    spread = {'L': (-330.0, 40.0, 60.0), 'R': (330.0, 40.0, 60.0)}
    jm = V.standing(STAND_INS['myrtle'])
    for side, tgt in spread.items():
        V.arm_to(jm, side, tgt, 'down', 'fist')
    shots = [
        (shot('hat close', [('harry hall', dict(j=sit))], hall_extra),
         'Shot 1 (the 3 s hook): Harry and the Hat\nfill the frame: "BIOLOGICAL MALE."\nHarry, annoyed. Hook Text: Hat\'s face clear'),
        (shot('corridor run', [('harry', run_h), ('ron', run_r)]),
         'Shot 2: "Later..." From the door down the\ncloister: they race at the lens'),
        (shot('myrtle', [('harry', {}), ('ron', {}), ('myrtle', dict(lift=0.3, ghost=True))], door_extra),
         "Shot 3: over the boys' shoulders: Myrtle\nfloats out through the shrunk door\n(GIRLS plaque). Her lines here"),
        (shot('boys', [('harry', {}), ('ron', {}), ('myrtle', dict(lift=0.3, ghost=True))]),
         "Shot 4: through Myrtle's back at Harry\nand Ron (Harry's and Ron's lines);\nscream and splat heard behind her"),
        (shot('myrtle', [('harry', {}), ('ron', {}), ('myrtle', dict(lift=0.3, ghost=True, j=jm))], door_extra),
         'Shot 5: "When you throw open the door..."\nshe floats round and spreads across\nthe doorway'),
    ]
    tiles = [tile(im, lab) for im, lab in shots]
    top = os.path.join(os.path.dirname(os.path.abspath(out)), '_tw_plan_top.jpg')
    PLN.sketch(FILM, top)
    pim = Image.open(top).convert('RGB')
    pim.thumbnail((540, 868))
    pt = Image.new('RGB', (540, 960), 'white')
    pt.paste(pim, ((540 - pim.width) // 2, 0))
    tiles.append(tile(pt, 'The plan from above (metres): Great\nHall left, cloister and door right'))
    os.remove(top)
    cols = 4
    W = Image.new('RGB', (550 * cols + 10, 975 * 2 + 90), (235, 232, 226))
    d = ImageDraw.Draw(W)
    d.text((20, 20), 'TERFWARTS: rough composition (rule 11): layout and joke only, not the drawing. '
           'Everyone is a colour stand-in.', font=ImageFont.truetype(FONT, 30), fill=(20, 20, 20))
    for i, t in enumerate(tiles):
        W.paste(t, (10 + (i % cols) * 550, 80 + (i // cols) * 975))
    W.save(out, quality=84)
    return out


if __name__ == '__main__':
    print(sheet(sys.argv[1]))
