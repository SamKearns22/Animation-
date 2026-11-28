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
  crew(i, disguised) the seven more men (CREW: Nick and six), plain or in brief row 17's disguise (DISGUISE,
                      source/disguise.py); grey_man() the grey test man; patriot_disguised(mood)
  cast_sheets(OUT_DIR) the cast sheet (cast chat 4, 28 Nov): sheet 1 Danny (front, side, back; slumped on the cot,
                      at the window bars from outside, the side and behind; his head turned beside his photo), the two
                      officers, the boat beside the Patriot; sheet 2 the eight men plain and disguised, front, side,
                      back, true heights (python3 source/patriots5_cast.py cast OUT_DIR)
  danny_sill(sp) .... his palms on the window's inner sill (shots 5, 6: the bars are out of reach in the plan)
  tables: LINES, MOODS, CREW, DISGUISE, COT, SAD
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from PIL import Image, ImageDraw, ImageFont   # noqa: E402
from ink import INK                            # noqa: E402
import facehouse as F                         # noqa: E402
import patriots3_cast as P3                   # noqa: E402  (his clothes; it also hangs the badges and cargo pockets)
import people_parts as PP                     # noqa: E402

LINES = dict(hair='bald', outfit=('jumper', P3.JACKET), height=1.78, dome=-0.33, dome_wide=0.42, head=False,
             balaclava=True, eye_scale=1.2, liner=3.0)
BODY = dict(sleeve=P3.SLEEVE, trousers=P3.COMBAT, shoe=(22, 20, 22), shoulders=168, bottom=500, patches=True,
            belly=True, cargo=True, neck_c=F.BALA, neck_w=1.2, figure='stout', name='Patriot',
            collar='band')   # the stand collar a band in the jacket's black, every view (note 4)
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


# The seven more Patriot Platform men (cast chat 4, 28 Nov; brief row 7: eight in the tower, one is Nick): the house
# head under the balaclava (only eyes and brows show, so each man's eyes, brows and the skin round them differ), the
# Patriot's jacket cut in each man's own dark shade, varied heights and builds, so eight read as eight at phone size.
CREW = [   # name, height, build (figure, shoulders), jacket, sleeve, trousers, eyes, brows, skin round the eyes, eye size
    # Sam, 28 Nov: "Give them all the black outfit used in the protests" (references/patriots5/dover: black hoodies and
    # jackets, black joggers, black trainers, faces covered): every man in near-black, each a slightly different black
    # so they still read as eight; all white British men (Sam, 28 Nov), so the skin round the eyes stays fair.
    dict(name='Nick', height=1.86, figure=None, shoulders=158, jacket=(30, 31, 36), sleeve=(30, 31, 36),
         trousers=(24, 24, 28), iris=(70, 110, 150), brow=(150, 110, 70), skin=(244, 206, 186), eye=1.15),
    dict(name='Gaz', height=1.70, figure='stout', shoulders=176, jacket=(22, 22, 24), sleeve=(22, 22, 24),
         trousers=(30, 30, 34), iris=(70, 50, 36), brow=(40, 30, 26), skin=(236, 190, 160), eye=1.05),
    dict(name='Kev', height=1.80, figure=None, shoulders=150, jacket=(26, 26, 30), sleeve=(40, 40, 46),
         trousers=(22, 22, 26), iris=(90, 120, 90), brow=(196, 160, 110), skin=(250, 214, 198), eye=1.3),
    dict(name='Wayne', height=1.66, figure=None, shoulders=146, jacket=(36, 36, 40), sleeve=(36, 36, 40),
         trousers=(26, 26, 30), iris=(60, 44, 34), brow=(60, 44, 34), skin=(238, 196, 172), eye=1.0),
    dict(name='Dean', height=1.92, figure='stout', shoulders=184, jacket=(18, 18, 20), sleeve=(18, 18, 20),
         trousers=(32, 32, 36), iris=(80, 100, 130), brow=(120, 84, 56), skin=(240, 196, 176), eye=1.1),
    dict(name='Lee', height=1.75, figure=None, shoulders=162, jacket=(32, 30, 32), sleeve=(32, 30, 32),
         trousers=(20, 20, 24), iris=(56, 40, 30), brow=(30, 24, 22), skin=(242, 202, 180), eye=1.2),
    dict(name='Darren', height=1.73, figure='stout', shoulders=170, jacket=(28, 28, 34), sleeve=(28, 28, 34),
         trousers=(24, 24, 28), iris=(110, 130, 150), brow=(176, 120, 84), skin=(248, 210, 192), eye=0.95),
]
HOOD = (34, 34, 38)          # their hoods black too (the protest photos: black hoods up over the face coverings)
# Brief row 17 (Sam's words, the news photos): the disguise each wears in shot 8. At least two in niqabs; white caps
# on some; prayer beads in one hand; orange life jackets on all. Sam, 28 Nov: "remove the scarf. Keep life jacket"
# (the red-and-white blanket round the shoulders is gone from everyone).
DISGUISE = {'Patriot': dict(kufi=True, beads='R'),
            'Nick': dict(niqab=True),
            'Gaz': dict(kufi=True, puffer=True, hood=HOOD),
            'Kev': dict(niqab=True, puffer=True),
            'Wayne': dict(kufi=True, beads='R', hood=HOOD),
            'Dean': dict(hood=HOOD, puffer=True),
            'Lee': dict(kufi=True, beads='L'),
            'Darren': dict(hood=HOOD, puffer=True)}


def _jacket_in(col):
    """The Patriot's jacket drawn in another man's shade (patriots3_cast reads its colour from JACKET)."""
    def draw(p, view, sp):
        old = P3.JACKET
        P3.JACKET = col
        try:
            P3.patriot_jacket(p, view, sp)
        finally:
            P3.JACKET = old
    return draw


def crew(i, disguised=False, kit=None):
    """Crew man i (0-6: CREW) as (sp, j); disguised: brief row 17's kit over his outfit (DISGUISE)."""
    import views as V
    c = CREW[i]
    sp = F.person('patriot', 'detail', **dict(LINES, height=c['height'], eye_scale=1.2 * c['eye'],
                                                 iris_c=c['iris'], brow_c=c['brow']))
    sp.update(BODY)
    sp.update(name=c['name'], jacket=c['jacket'], sleeve=c['sleeve'], trousers=c['trousers'], skin=c['skin'],
              shoulders=c['shoulders'], patches=i % 2 == 0)
    if c['figure']:
        sp['figure'] = c['figure']
    else:
        sp.pop('figure', None)
        sp['belly'] = False
    P3.HEIGHTS[c['name']] = c['height']               # his own height (scale_for reads it by name)
    j = V.standing(sp)
    j['body_props'] = [_jacket_in(c['jacket'])] + j.get('body_props', [])
    j['_dressed'] = True
    if disguised:
        import disguise
        sp, j = disguise.dress(sp, j, kit if kit is not None else DISGUISE[c['name']])
    return sp, j


def grey_man():
    """A plain grey test man under the house balaclava (rule 89: people in tests are the crowd pack or grey)."""
    import views as V
    sp = F.person('patriot', 'detail', **dict(LINES))
    sp.update(BODY)
    grey = (150, 150, 156)
    sp.update(name='grey', jacket=grey, sleeve=grey, trousers=(120, 120, 126), patches=False, belly=False)
    sp.pop('figure', None)
    j = V.standing(sp)
    j['_dressed'] = True
    return sp, j


# The tower's sway as the window sees it (chat 9; brief rows 8 and 11): the Patriot is the top of the tower, so at the
# window he moves exactly as shot 4's top man does (shoulder_tower.sway: the column pivots about the base's feet, each
# tier a little later and further). Tier heights from the lesson: base shoulders 1.45 m, 0.6 m a tier. Side-on in
# shot 4 that sway is towards and away from the wall, so from inside he nears and leaves the bars; a small sideways
# wobble too (a real stack wobbles both ways; side-on at 6 m it is too small to see, so the shots agree).
NEAR_PAST_BARS = 0.1         # his neck at the sway's near end (m past the bars): chat 8's place, his face at the bars
#                              (between two of them); the sway only ever carries him back from there, never through
WOBBLE = (0.03, 3.1)         # the sideways wobble at the top: metres either way, seconds a cycle


def top_sway(t, n=8):
    """The top man's movement at time t (m): (towards the wall +, sideways +)."""
    import shoulder_tower as ST
    toward = 1.45 * math.sin(ST.sway(0, t)) + sum(0.6 * math.sin(ST.sway(i, t)) for i in range(1, n))
    return toward, WOBBLE[0] * math.sin(2 * math.pi * t / WOBBLE[1] + 0.8)


def window_depth(t, bars=4.65):
    """The Patriot's plan depth at the window at time t: the near end of the sway puts his neck NEAR_PAST_BARS past
    the bars (his face at them); every other moment is further back by the sway."""
    near = max(top_sway(k / 50.0)[0] for k in range(200))
    return bars + NEAR_PAST_BARS + (near - top_sway(t)[0])


# Brief row 12 (shot 6, "He is exaggerating with his hands"): talking hands up in the window's opening, beside his face
# (his body is below the sill, out of sight), behind the bars (never past them: z under 60, the bars 0.15 m out). Each
# gesture is held, then moved to the next over GESTURE_MOVE s, eased; the beats are laid on Sam's recorded line later.
GESTURES = {   # (left hand, right hand) targets, torso frame (x across, y down from the neck, z forward); shape
    # chat 9: over and beside his face (pale hands read on the black balaclava), inside the opening's sides and above
    # its sill (both hands always in view), never past his own face (z under 55: at the sway's near end his face is
    # at the bars, so the hands stay behind them)
    'open':  (((-90, -115, 52), 'palm'), ((90, -115, 52), 'palm')),       # "we've got a plan": palms out, wide
    'point': (((-95, -100, 45), 'palm'), ((30, -125, 55), 'point')),      # "boss": a finger at Danny
    'chop':  (((-95, -100, 45), 'palm'), ((75, -215, 50), 'palm')),       # "infiltration": a hand up, chopping down
    'wide':  (((-115, -185, 48), 'palm'), ((115, -185, 48), 'palm')),     # "completely invisible": spread by his eyes
    'hush':  (((-95, -100, 45), 'palm'), ((10, -130, 55), 'point')),      # "British authorities": finger to the mask
}
GESTURE_ORDER = ['open', 'point', 'chop', 'wide', 'hush']
GESTURE_HOLD, GESTURE_MOVE = 0.9, 0.3


def gesture_at(t, order=None):
    """(name before, name after, 0..1 eased) at time t through the gesture list."""
    order = order or GESTURE_ORDER
    step = GESTURE_HOLD + GESTURE_MOVE
    k = int(t // step)
    u = max(0.0, (t - k * step - GESTURE_HOLD) / GESTURE_MOVE)
    a, b = order[k % len(order)], order[(k + 1) % len(order)]
    return a, b, u * u * (3 - 2 * u)


def patriot_talk(t, mood='talking', order=None):
    """The Patriot at the window, talking with his hands at time t (shot 6; the same in 3 and 5 if they need it)."""
    import views as V
    sp, j = patriot(mood)
    a, b, u = gesture_at(t, order)
    for k, sd in enumerate(('L', 'R')):
        (pa, sa), (pb, sb) = GESTURES[a][k], GESTURES[b][k]
        tgt = tuple(pa[i] + (pb[i] - pa[i]) * u for i in range(3))
        shape = sa if u < 0.5 else sb
        # elbows out: hands inside his shoulders' width (the rig's check: an elbow never folds across the chest)
        V.arm_to(j, sd, tgt, 'out', shape)
    return sp, j


def patriot_disguised(mood='rest', kit=None):
    import disguise
    sp, j = patriot(mood)
    return disguise.dress(sp, j, kit if kit is not None else DISGUISE['Patriot'])


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


# ---------------------------------------------------------------------------------------------- the cast sheets
COT = dict(h=230, front=120, rear=-260, width=200, col=(96, 98, 104), top=(150, 156, 168))   # the cell's cot (a seat)
SAD = dict(brow_up=0.012, frown=-0.05, lid4=0.55, smile=-0.8)    # Danny downcast (shot 1: sighing deeply)
BARS = (60, 62, 70)


def danny_slumped(sp):
    """Shot 1: on the cot's edge, leaning forward, hands in his lap, head dropped."""
    import sitting as ST
    seat = ST.Seat('stool', **COT)
    spec = ST.spec_upright(sp, seat, hands='lap')
    spec['lean'] = 16.0
    j = ST.realize(sp, seat, spec)
    j['head_dy'] = j.get('head_dy', 0) + 14
    return j


def danny_window(sp):
    """Shots 2, 5, 6: standing on the bunk, a fist round a bar of the grate either side of his face."""
    import views as V
    j = V.standing(sp)
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, (sg * 82.0, -150.0, 130.0), 'down', 'fist')
    j['head_dy'] = -6
    return j


def danny_sill(sp):
    """Shots 5 and 6 (chat 8): up on the cot on his toes, both palms flat on the window's inner sill (the cell plan:
    the sill 2.05 m up at the wall's room face, 0.2 m in front of his face; the bars 0.45 m further out, out of his
    reach, so danny_window's fists round the bars cannot happen in this wall)."""
    import views as V
    j = V.standing(sp)
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, (sg * 100.0, -30.0, 150.0), 'down', 'palm')
    j['head_dy'] = -6
    return j


def _grate(p, x, y, s, view, front):
    """The cell window's bars at his fists (body frame: fists at +-82 across, 150 up, 130 forward)."""
    if view == 'side':                  # the cell wall, cut through: brick above and below the window's opening, the
        wx = x + 136 * s                # bars in it where his fists hold them
        brick = (150, 96, 74)
        for y0, y1 in ((y - 400 * s, y - 250 * s), (y - 40 * s, y + 300 * s)):
            p.poly([(wx, y0), (wx + 150 * s, y0), (wx + 150 * s, y1), (wx, y1)], brick, INK, 2.4)
            for yy in np.arange(y0 + 34 * s, y1, 34 * s):
                p.line([(wx, yy), (wx + 150 * s, yy)], (120, 74, 56), 1.4)
        p.poly([(wx, y - 250 * s), (wx + 12 * s, y - 250 * s), (wx + 12 * s, y - 40 * s), (wx, y - 40 * s)], BARS, INK, 1.8)
        return
    top, bot = y - 270 * s, y - 30 * s
    hw = 150 if front else 230
    if not front:                       # from behind: the moonlit window beyond him (wider than his head), its bars
        p.poly([(x - hw * s, top), (x + hw * s, top), (x + hw * s, bot), (x - hw * s, bot)], (40, 52, 84), INK, 3)
    for bx in ((-82, -28, 28, 82) if front else (-190, -136, -82, 82, 136, 190)):
        p.poly([(x + (bx - 6) * s, top), (x + (bx + 6) * s, top), (x + (bx + 6) * s, bot), (x + (bx - 6) * s, bot)],
               BARS, INK, 1.8)
    for by in (top, bot):
        p.poly([(x - hw * s, by - 6 * s), (x + hw * s, by - 6 * s), (x + hw * s, by + 6 * s), (x - hw * s, by + 6 * s)],
               BARS, INK, 1.8)


def _crop(tile, bg):
    import numpy as np
    a = np.asarray(tile.convert('RGB')).astype(int)
    m = (np.abs(a - np.array(bg)).sum(2) > 12)
    ys, xs = np.nonzero(m)
    return tile.crop((xs.min() - 6, ys.min() - 6, xs.max() + 7, ys.max() + 7))


def _carry(sp, j):
    """The man as the boat and the tower take him: his clothes and kit ride in sp['_dress'] (they rebuild his pose)."""
    sp = dict(sp)
    sp['_dress'] = {k: j[k] for k in ('body_props', 'head_props', 'props', '_dressed') if k in j}
    return sp


def boat_men():
    """Shot 8's eight in the boat (Sam, 28 Nov: "Include The Patriot in the boat, at the front"), disguised: the near
    row first (left to right), the far row after. The far row stands half a place ahead, so its last place is the
    very front of the boat (the boat walks left to right): the Patriot's, with Wayne (the shortest) in front of him in
    the near row so his head and badges show. The tall men stand in the far row, their heads over the near row."""
    order = ['Darren', 'Gaz', 'Lee', 'Wayne', 'Kev', 'Nick', 'Dean', 'Patriot']

    def kit(name, near):
        # beads only in a hand we see: the near row's near (right) hand on the tube; a far hand is inside the boat,
        # and beads drawn there would show through the tube (seen 28 Nov, Lee's beads over the near tube)
        k = dict(DISGUISE[name])
        k.pop('beads', None)
        if near and DISGUISE[name].get('beads'):
            k['beads'] = 'R'
        return k
    men = {}
    for n in order:
        near = order.index(n) < 4
        if n == 'Patriot':
            men[n] = _carry(*patriot_disguised(kit=kit(n, near)))
        else:
            men[n] = _carry(*crew([c['name'] for c in CREW].index(n), True, kit=kit(n, near)))
    return [men[n] for n in order]


def tower_men():
    """Shot 4's tower (brief row 7: all eight), plain: the heaviest at the base, Nick under the Patriot ("Nick's
    head is up my arse"), the Patriot on top at the window."""
    sp, j = patriot()
    men = {c['name']: _carry(*crew(i, False)) for i, c in enumerate(CREW)}
    men['Patriot'] = _carry(sp, j)
    order = ['Dean', 'Gaz', 'Darren', 'Lee', 'Kev', 'Wayne', 'Nick', 'Patriot']
    return [men[n] for n in order]


def boat_panel():
    """The orange walking boat (source/walking_boat.py) with shot 8's crew in it, disguised, the Patriot at the bow
    (Sam, 28 Nov: "Include The Patriot in the boat, at the front, not outside it")."""
    import walking_boat as WB
    install()
    B = WB.B
    bt = WB.Boat(boat_men(), WB.S, WB.GROUND_Y, 540.0)
    ss, B.SS = B.SS, 2
    img = B.canvas(WB.NIGHT)
    cam = B.Cam(1.0, 540, 960)
    WB.scene(img, cam, bt.X(0.0), bt)
    bt.draw(img, cam, 0.0)
    B.SS = ss
    return img.resize((1080, 1920), Image.LANCZOS).crop((0, 700, 1080, 1450)).convert('RGBA')


def cast_sheets(out_dir):
    import numpy as np
    import body as B
    import people
    import views as V
    from PIL import Image, ImageDraw
    os.makedirs(out_dir, exist_ok=True)
    install()
    cast = people.install(people.load('patriots5'))
    B.SS = 1
    BG = (232, 228, 222)
    big = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 40)
    small = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 34)
    S0 = 0.5                                            # a 1.78 m man's scale on the sheets

    def fig(drawfn, yaw, s=S0, extra=None, under=None):
        tile = Image.new('RGBA', (1400, 2600), BG + (255,))
        y = 1000.0
        if under:
            under(B.Pen(tile, B.Cam(1.0, 540, 960)), 700, y, s)
        drawfn(tile, 700, y, s, yaw)
        if extra:
            extra(B.Pen(tile, B.Cam(1.0, 540, 960)), 700, y, s)
        return tile, y + 928 * s

    def kit(sp, j=None):
        return lambda img, x, y, s, yaw: V.person(img, B.Cam(1.0, 540, 960), x, y, s * sp['height'] / 1.78,
                                                  dict(sp), 0.0, float(yaw), j)

    def lay(img, row, floor, d):                         # row: [(tile, foot_y, label)], one floor, left to right
        x = 30
        for tile, foot, label in row:
            part = _crop(tile, BG)                       # (the whole figure: a taller man's feet are lower)
            img.alpha_composite(part, (x, floor - part.height + 6))
            d.text((x + 4, floor + 12), label, font=small, fill=(30, 30, 30))
            x += part.width + 30
        return x

    # ---- sheet 1: Danny, the officers, the boat
    W, H = 2600, 2760
    img = Image.new('RGBA', (W, H), BG + (255,))
    d = ImageDraw.Draw(img)
    d.text((30, 16), 'THE PATRIOT 5: Danny Tommo, the prison officers, the boat', font=big, fill=(30, 30, 30))
    img.alpha_composite(Image.new('RGBA', (1, 1), BG + (255,)), (0, 0))
    row = []
    for who, lab in (('tommo', 'Danny'), ('officer', 'officer 1'), ('guard2', 'officer 2')):
        sp = cast[who]
        for yaw, vn in ((0, 'front'), (90, 'side'), (180, 'back')):
            t, f = fig(kit(sp), yaw)
            row.append((t, f, lab if vn == 'front' else ''))
    lay(img, row, 780, d)
    d.text((1900, 740), 'each: front, side, back', font=small, fill=(90, 90, 90))
    sp = dict(cast['tommo'], **SAD)
    row = []
    for yaw, lab in ((0, 'on his cot'), (90, '')):
        t, f = fig(kit(sp, danny_slumped(sp)), yaw)
        row.append((t, f, lab))
    sp = cast['tommo']
    for yaw, lab, front in ((0, 'at the bars', True), (90, '', None), (180, 'from behind', False)):
        t, f = fig(kit(sp, danny_window(sp)), yaw,
                   extra=(lambda p, x, y, s, fr=front, yw=yaw: _grate(p, x, y, s, 'side' if yw == 90 else 'front', True))
                   if front else None,
                   under=(lambda p, x, y, s: _grate(p, x, y, s, 'side' if yaw == 90 else 'back', False))
                   if not front else None)
        row.append((t, f, lab))
    x = lay(img, row, 1500, d)
    # his head turned, beside his photo
    T = 300
    for k, yaw in enumerate((0, 45, 90, 135, 180)):
        tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
        V.person(tile, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(sp), 0.0, float(yaw))
        img.alpha_composite(tile.crop((300, 300, 780, 780)).resize((T, T)), (30 + k * (T + 14), 1580))
    ph = Image.open(os.path.join(HERE, '..', 'references', 'faces', 'tommo', '04-front-mirror.jpg')).convert('RGBA')
    ph.thumbnail((2 * T, T))
    img.alpha_composite(ph, (30 + 5 * (T + 14), 1580))
    d.text((30, 1580 + T + 8), "Danny's head beside his photo", font=small, fill=(30, 30, 30))
    boat = boat_panel()
    if boat is not None:
        boat.thumbnail((1100, 760))
        img.alpha_composite(boat, (30, 1960))
        d.text((30 + boat.width + 20, 1980), 'the orange boat: the eight\nin disguise, the Patriot\nat the front (right)', font=small, fill=(30, 30, 30))
    out1 = os.path.join(out_dir, 'patriot-5-cast-sheet-1.jpg')
    a = img.convert('RGB')
    a.crop((0, 0, W, min(H, 1960 + (boat.height + 20 if boat is not None else 0)))).save(out1, quality=86)

    # ---- sheet 2: the eight men, plain and disguised
    men = [('Patriot', lambda dis: patriot_disguised() if dis else patriot())]
    men += [(c['name'], (lambda dis, i=i: crew(i, dis))) for i, c in enumerate(CREW)]
    rows = [(False, 0, 'front'), (False, 90, 'side'), (False, 180, 'back'),
            (True, 0, 'disguised front'), (True, 90, 'disguised side'), (True, 180, 'disguised back')]
    W2 = 2700
    img = Image.new('RGBA', (W2, 120 + len(rows) * 640), BG + (255,))
    d = ImageDraw.Draw(img)
    d.text((30, 16), 'THE PATRIOT 5: the eight Patriot Platform men (true heights), plain and in the shot 8 disguise',
           font=big, fill=(30, 30, 30))
    for r, (dis, yaw, rname) in enumerate(rows):
        row = []
        for name, make in men:
            sp, j = make(dis)
            t, f = fig(lambda img_, x, y, s, yw, sp=sp, j=j: draw(img_, B.Cam(1.0, 540, 960), x, y, s, sp, j, yw), yaw,
                       s=0.42)
            row.append((t, f, name if r in (0, 3) else ''))
        floor = 120 + (r + 1) * 640 - 60
        lay(img, row, floor, d)
        d.text((W2 - 330, floor - 40), rname, font=small, fill=(90, 90, 90))
    out2 = os.path.join(out_dir, 'patriot-5-cast-sheet-2.jpg')
    img.convert('RGB').save(out2, quality=86)
    return out1, out2


def disguise_sheet(out):
    """Each piece alone on a grey test person (rule 89; people in tests are grey), five turns."""
    from PIL import Image, ImageDraw
    import disguise as D
    import sys as _s
    P5 = _s.modules[__name__]
    P5.install()
    B = D.B
    B.SS = 1
    rows = [('life jacket', dict(life=True)), ('puffer + hood + life jacket', dict(puffer=True, hood=True)),
            ('blanket + beads', dict(life=False, blanket=True, beads='R')), ('niqab', dict(life=False, niqab=True)),
            ('kufi', dict(life=False, kufi=True))]
    T = 300
    img = Image.new('RGB', (5 * T + 220, len(rows) * (T + 30) + 20), (232, 228, 222))
    d = ImageDraw.Draw(img)
    for r, (name, kit) in enumerate(rows):
        d.text((10, 20 + r * (T + 30) + T // 2), name, fill=(0, 0, 0))
        for k, yaw in enumerate((0, 45, 90, 135, 180)):
            sp, j = P5.grey_man()
            sp, j = D.dress(sp, j, kit)
            tile = Image.new('RGBA', (1080, 2600), (232, 228, 222, 255))
            P5.draw(tile, B.Cam(1.0, 540, 960), 540, 1500, 0.62, sp, j, yaw)
            t = tile.crop((290, 1250, 790, 2110)).convert('RGB')
            t.thumbnail((T, T))
            img.paste(t, (220 + k * T, 20 + r * (T + 30)))
    img.save(out, quality=88)
    return out



if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'cast':
        print(cast_sheets(sys.argv[2]))
    elif len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    elif len(sys.argv) > 2 and sys.argv[1] == 'disguise':
        print(disguise_sheet(sys.argv[2]))
    else:
        print(__doc__)
