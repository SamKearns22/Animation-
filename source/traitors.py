#!/usr/bin/env python3
"""The Traitors (TikTok satire, Sam 17 Oct): the final Round Table. Claudia asks Trump why he thinks Zelensky is a
traitor; Trump, holding up his ZELENSKY slate, answers; across the table sit Putin, spattered in blood, and Zelensky,
head in his hands: "Jesus Christ." Notes and decisions: notes/traitors.md. People: source/traitors_cast.py.
Guide: guides/satire.md.

    python3 source/traitors.py cast OUT.jpg              the cast sheet (every view used, the reaction strengths)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import traitors_cast as C        # noqa: E402  (installs the four heads and outfits into burnham)
import views as V                # noqa: E402
import moves                     # noqa: E402
from satire_style import install_circle_hands   # noqa: E402

install_circle_hands(B)
FPS = 12
NAME = 'traitors'

# =============================================== STORY ==============================================================
LINES = [   # 'audio': source/audio/NAME.m4a (Sam's takes, matched 17 Oct)
    dict(n=1, who='claudia', text='Donald Trump, why do you think Zelensky is a traitor?', audio='traitors-1'),
    dict(n=2, who='trump', text="I'm voting for him because I don't trust him. Because I think he's a disgrace. "
                                "He doesn't like any of my deals. And because. And because I just don't like looking at him.",
         audio='traitors-2'),
    dict(n=3, who='zelensky', text='Jesus Christ.', audio='traitors-3'),
]
HOOK = 'The Traitors: the final three'
TABLE_Y = 300             # a seated player's edge of the table, in their own units (neck at 0, shoulders at 60)
SLATE_W = 210             # the slate's width in person units (about 25 cm)
BLOOD = C.spatter()
# ====================================================================================================================


def seated_pose(sp, kind, strength=4):
    """The upper body of a seated player behind the table (the table hides the rest). kind: 'slate' (Trump holds his
    slate up at the chest, a hand on each side), 'folded' (Putin's hands folded on the table), 'head' (Zelensky's
    head in his hands, strength 1-6), 'clasped' (Claudia standing, hands together at the waist)."""
    j = V.standing(sp)
    j['props'] = []
    sw = sp.get('shoulders', 150)
    if kind == 'slate':
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * (SLATE_W / 2 + 4), 236.0, 170.0), 'down', 'fist')
    elif kind == 'folded':
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * 16, TABLE_Y + 40, 230.0), 'down', 'fist')
    elif kind == 'clasped':
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * 16, 400.0, 90.0), 'back')
        j['props'] = [lambda p, j2: (C.frill(p, j2, 'L'), C.frill(p, j2, 'R'))]
    elif kind == 'head':
        k = strength
        dy = {1: 6, 2: 12, 3: 26, 4: 40, 5: 54, 6: 74}[k]
        j['head_dy'] = dy
        j['lean'] = {1: 2, 2: 4, 3: 10, 4: 16, 5: 22, 6: 28}[k]
        hy = -150.0 + dy
        if k == 1:                                     # one hand rubbing his forehead
            V.arm_to(j, 'R', (14.0, hy - 54, 96.0), (1.0, 0.5, 0.2), 'palm')
            V.arm_to(j, 'L', (-60.0, TABLE_Y + 40, 230.0), 'down', 'fist')
            j['on_face'] = {'R'}
        else:
            hx_off, yy, z = {2: (74, hy - 40, 50), 3: (62, hy - 34, 80), 4: (44, hy - 46, 96), 5: (34, hy - 6, 104),
                             6: (28, hy + 14, 110)}[k]
            for s, sg in (('L', -1), ('R', 1)):
                V.arm_to(j, s, (sg * hx_off, yy, z), (0.5, 1.0, 0.6), 'palm')
            j['on_face'] = {'L', 'R'}
    return j


def draw_player(img, cam, x, y, s, who, sp_extra=None, kind='folded', strength=4, t=0.0, slate=None):
    """One player at the table: the person, their slate (held or on its stand), their goblet, the table edge."""
    sp = dict({'trump': C.TRUMP, 'putin': C.PUTIN, 'zelensky': C.ZELENSKY, 'claudia': C.CLAUDIA}[who])
    sp.update(sp_extra or {})
    if who == 'zelensky' and kind == 'head':
        sp.update(down={1: 0.2, 2: 0.3, 3: 0.5, 4: 0.7, 5: 0.85, 6: 1.0}[strength], blink=True)
    j = seated_pose(sp, kind, strength)
    if kind == 'slate':                                # held up in front of his chest, over his body, under his hands
        j['props'] = [lambda p, j2: C.draw_slate(img_ref[0], p, 0, 236 + 40, SLATE_W, 'ZELENSKY', seed=2, stand=True),
                      lambda p, j2: [B.gesture_hand(p, j2['el' + sd], j2['wr' + sd], 'fist', sp['skin']) for sd in 'LR']]
    img_ref = [img]
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    j2 = {}
    shapes = BLOOD + C.hand_smears([(-16, TABLE_Y + 34), (16, TABLE_Y + 34)])
    if who == 'putin':
        C.bloody(img, cam, x, y, s, lambda im: j2.update(V.person(im, cam, x, y, s, sp, t, 0, j)), shapes)
    else:
        j2.update(V.person(img, cam, x, y, s, sp, t, 0, j))
    if kind != 'clasped':
        C.table_far(img, p, -420, 420, TABLE_Y, seed=sum(map(ord, who)) % 7)
        C.plate(p, 0, TABLE_Y + 140)
        C.goblet(p, 250, TABLE_Y + 60)
        on_table = [sd for sd in 'LR' if sd not in j.get('on_face', ()) and kind in ('folded', 'head')]
        if on_table:                                   # forearms resting on the table lie over its edge
            def arms(im):
                q = B.Pen(im, L)
                for sd in on_table:
                    V.arm(q, j2, sd, sp)
            if who == 'putin':
                hands = []
                for sd in on_table:
                    el, wr = j2['el' + sd], j2['wr' + sd]
                    d = ((wr[0] - el[0]) ** 2 + (wr[1] - el[1]) ** 2) ** 0.5 or 1.0
                    hands.append((wr[0] + (wr[0] - el[0]) / d * 12, wr[1] + (wr[1] - el[1]) / d * 12))
                C.bloody(img, cam, x, y, s, arms, BLOOD + C.hand_smears(hands))
            else:
                arms(img)
        if slate:
            C.draw_slate(img, p, slate[0], TABLE_Y + 50, SLATE_W * 0.9, slate[1], cyrillic=slate[2], seed=slate[3],
                         face_up=slate[4])
    return j


def panel(draw, w=540, h=700, z=2.6, cy=820, bg=(66, 40, 28)):
    img = B.canvas(bg)
    cam = B.Cam(z, 540, cy)
    draw(img, cam)
    return img.crop((0, 1920 // 2 - int(h * 1080 / w) // 2, 1080, 1920 // 2 + int(h * 1080 / w) // 2)).resize((w, h), Image.LANCZOS)


def label(img, x, y, txt, size=30):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), size)
    d.text((x, y), txt, font=f, fill=(250, 250, 250), stroke_width=3, stroke_fill=(20, 20, 20))


def cast_sheet(out):
    """Every view each person appears in: Claudia standing (shot 1); Trump holding up his slate (shot 2), close and
    sneering; Putin with the blood and his Cyrillic vote (shot 3); Zelensky's head in his hands at strengths 1-6 for
    Sam to pick from (the film's key reaction), and his face before it."""
    B.SS = 1
    sheet = Image.new('RGB', (2160, 700 * 2 + 520), (30, 24, 22))
    row = [
        ('Claudia (shot 1)', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'claudia', kind='clasped')),
        ('Trump (shot 2)', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'trump', kind='slate')),
        ('Putin (shot 3)', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'putin', {'smirk': 0.6}, kind='folded',
                                                       slate=(-170, 'ЗЕЛЕНСКИЙ', True, 4, True))),
        ('Zelensky (shot 3), strength 4', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'zelensky', kind='head',
                                                                      strength=4, slate=(170, '', False, 0, False))),
    ]
    for i, (name, fn) in enumerate(row):
        sheet.paste(panel(fn, z=1.9, cy=960), (540 * i, 0))
        label(sheet, 540 * i + 16, 12, name)
    close = [
        ('Claudia, close', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'claudia', kind='clasped')),
        ('Trump: "looking at him"', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'trump', {'sneer': True, 'look': 0.8},
                                                                kind='slate')),
        ('Putin, close', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'putin', {'smirk': 0.6}, kind='folded')),
        ('Zelensky, face', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'zelensky', kind='folded')),
    ]
    for i, (name, fn) in enumerate(close):
        sheet.paste(panel(fn, z=3.4, cy=770), (540 * i, 700))
        label(sheet, 540 * i + 16, 712, name)
    for k in range(1, 7):
        im = panel(lambda img, cam, k=k: draw_player(img, cam, 540, 900, 1.0, 'zelensky', kind='head', strength=k),
                   w=360, h=520, z=2.4, cy=860)
        sheet.paste(im, (360 * (k - 1), 1400))
        label(sheet, 360 * (k - 1) + 14, 1410, f'Zelensky {k}', 26)
    sheet.save(out, quality=90)


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        cast_sheet(a[1])


if __name__ == '__main__':
    main()
