#!/usr/bin/env python3
"""Patriots 3: the rough composition sheet (film-quality rule 11): the key shots through the plan's own cameras, the
room as plain blocks (sets.house), the beach through the slit, the cast standing on their plan marks, and the plan
from above. For Sam to approve the layout and the joke before anything is built.

    python3 source/patriots3_compose.py OUT.jpg
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import views as V                # noqa: E402
import sets as S                 # noqa: E402
import plan as PLN               # noqa: E402
import patriots3_cast as C       # noqa: E402
import patriots3_bunker as K     # noqa: E402
import patriots3_plan as PL      # noqa: E402
import patriots3 as FILM         # noqa: E402
from ed import INK               # noqa: E402
from satire_style import rough   # noqa: E402

M = V.M_PER_UNIT
SPS = {'patriot': C.PATRIOT, 'gunner': C.GUNNER, 'loader': C.LOADER}
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')


def cam(name):
    c = PL.CAMS[name]
    return S.Cam(c['pos'], c['look'], focal=c['focal'])


def painter(cm):
    plain = S.plain_room(FILM)
    horizon = cm.project((cm.pos[0], 1.5, cm.pos[2] + 2000.0))[0][1]

    def paint(img, cam_, space):
        if space == 'outside':                         # the beach through the slit (patriots3_bunker.beach_layer)
            h = int(min(max(10, horizon), img.size[1] * 0.6))
            lay = K.beach_layer(img.size, h)
            img.alpha_composite(lay.convert('RGBA'))
            return
        plain(img, cam_, space)
    return paint


def figure(img, cm, label, arms=None, lean=0.0):
    """One of the cast on a plan mark, drawn at the camera's scale and angle there (rough: the real drawing, the
    view snapped to the nearest one the kit draws)."""
    p = PL.PEOPLE[label]
    sp = SPS[p['who']]
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
    if lean:
        j['lean'] = lean
    flat = B.Cam(1.0, 540, 960)
    flat.P = lambda a, b: (a, b)
    flat.S = lambda v: v
    C.person(img, flat, x, y, k * M, sp, 0.0, yaw, j)


def gun(img, cm, butt=(0.0, 1.33, 0.22)):
    """The MG42 as a dark block on the sill (rough)."""
    parts = [S.obox((butt[0], butt[1] - 0.05, butt[2] + 0.62), (0.09, 0.14, 1.22), 0.0,
                    cols={f: (52, 54, 58) for f in ('top', 'front', 'back', 'left', 'right', 'bottom')})]
    S.draw_parts(img, cm, parts)


def room_shot(name, people, gun_at=True):
    cm = cam(name)
    img = B.canvas((255, 255, 255))
    S.house(img, cm, FILM, paint=painter(cm), here='casemate')
    if gun_at:
        gun(img, cm)
    order = sorted(people, key=lambda q: -cm.depth(C.Spot(SPS[PL.PEOPLE[q[0]]['who']], *PL.PEOPLE[q[0]]['at'])
                                                   .to_world((0.0, 0.0, 0.0))))
    for label, arms in order:
        figure(img, cm, label, arms)
    return img


def coast():
    """Shot 1, rough: high above the sea looking south; the black cliffs, the beach, six craft, bursts, flashes."""
    cm = cam('s1')
    img = B.canvas((196, 198, 196))
    p = S.pen(img)
    P = lambda x, y, z: cm.project((x, y, z))[0]
    p.poly([P(-3000, 0, -3000), P(3000, 0, -3000), P(3000, 0, 3000), P(-3000, 0, 3000)], (96, 110, 114), INK, 0)
    p.poly(rough([P(-600, 0, 0), P(600, 0, 0), P(600, 0, 60), P(-600, 0, 60)], 4, 1), (188, 176, 150), INK, 2)
    p.poly(rough([P(-600, 0, 60), P(600, 0, 60), P(600, 0, 75), P(-600, 0, 75)], 4, 2), (150, 140, 122), INK, 2)
    cliff = [P(-600, 0, 0)] + [P(x, 32 + 6 * math.sin(x * 0.03), 0) for x in range(-600, 601, 40)] + [P(600, 0, 0)]
    p.poly(rough(cliff, 6, 3), (40, 40, 44), INK, 2)
    p.poly([P(-600, 32, 0), P(600, 32, 0), P(600, 30, -400), P(-600, 30, -400)], (90, 100, 70), INK, 2)
    for i, (x, z) in enumerate([(-70, 150), (-35, 190), (0, 140), (30, 200), (60, 160), (95, 210)]):
        hull = [P(x - 2, 0, z), P(x + 2, 0, z), P(x + 2, 0, z + 11), P(x - 2, 0, z + 11)]
        p.poly(rough(hull, 3, 10 + i), (104, 110, 112), INK, 2)
        for k in range(8):
            q = P(x - 1.2 + (k % 3) * 1.2, 1.0, z + 2 + (k // 3) * 3)
            p.poly(rough([(q[0] - 4, q[1] - 3), (q[0] + 4, q[1] - 3), (q[0] + 4, q[1] + 3), (q[0] - 4, q[1] + 3)],
                         2, k), (86, 96, 70), INK, 1)
        p.poly(rough([P(x - 3, 0, z + 11), P(x + 3, 0, z + 11), P(x + 6, 0, z + 40), P(x - 6, 0, z + 40)], 4, i),
               (226, 228, 222), INK, 0)
    for i, (x, z) in enumerate([(-120, 40), (40, 55), (150, 90), (-20, 110)]):
        c = P(x, 0, z)
        p.poly(rough([(c[0] - 26, c[1]), (c[0] - 10, c[1] - 70), (c[0] + 12, c[1] - 60), (c[0] + 26, c[1])], 8, i),
               (226, 220, 200), INK, 2)
    for i, x in enumerate((-300, -160, -40, 90, 230, 380)):
        c = P(x, 26, 0)
        p.poly(rough([(c[0] - 9, c[1] - 5), (c[0] + 9, c[1] - 6), (c[0] + 8, c[1] + 6), (c[0] - 8, c[1] + 5)], 3, i),
               (250, 214, 90), INK, 1)
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
    salute = {'R': (-30.0, -170.0, 330.0)}
    flap = {'R': (-170.0, -230.0, 140.0), 'L': (150.0, -40.0, 170.0)}
    shots = [
        (coast(), 'Shot 1 (0-3.6 s): high above the coast\nblack cliffs flashing, artillery, six craft\nHook Text in the sky at the top'),
        (room_shot('s3', [('gunner turned', None), ('loader turned', None), ('patriot in the doorway', None)]),
         'Shot 3: over their helmets, the Patriot\nleaning in the doorway: "What can I say?..."'),
        (room_shot('s6', [('gunner facing him', salute), ('loader facing him', salute)]),
         'Shot 6: "Ah, you are with the Führer?"\nboth salute: "Heil!" (the battle behind)'),
        (room_shot('s8', [('patriot approached', flap), ('gunner after the blast', None),
                          ('loader after the blast', None)]),
         'Shot 8 (the wide): the blast on the slit\nthrows them to the west wall; he walks\nto the free gun: "Anyway..."'),
        (room_shot('s9 start', [('patriot at the gun', None), ('gunner after the blast', None),
                                ('loader after the blast', None)]),
         'Shot 9: from the slit: "They ain\'t even\nwearing poppies." He fires; then the\npush-in on their glance'),
    ]
    tiles = [tile(im, lab) for im, lab in shots]
    top = os.path.join(os.path.dirname(os.path.abspath(out)), '_p3_plan_top.jpg')
    from types import SimpleNamespace         # the plan without the aerial camera (it is 760 m out to sea)
    PLN.sketch(SimpleNamespace(PLAN=dict(FILM.PLAN, CAMS={k: v for k, v in PL.CAMS.items() if k != 's1'}),
                               SHOTS=FILM.SHOTS[1:], NAME=FILM.NAME), top)
    pim = Image.open(top).convert('RGB')
    pim.thumbnail((540, 868))
    pt = Image.new('RGB', (540, 960), 'white')
    pt.paste(pim, ((540 - pim.width) // 2, 0))
    tiles.append(tile(pt, 'The plan from above (metres):\nslit at the top (the sea beyond),\ndoor in the back wall'))
    os.remove(top)
    W = Image.new('RGB', (540 * 3 + 40, 960 * 2 + 110), (235, 232, 226))
    d = ImageDraw.Draw(W)
    d.text((20, 20), 'PATRIOTS 3: rough composition (rule 11): layout and joke only, not the drawing',
           font=ImageFont.truetype(FONT, 34), fill=(20, 20, 20))
    for i, t in enumerate(tiles):
        W.paste(t, (10 + (i % 3) * 550, 80 + (i // 3) * 975))
    W.save(out, quality=86)
    return out


if __name__ == '__main__':
    print(sheet(sys.argv[1]))
