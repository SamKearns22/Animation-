#!/usr/bin/env python3
"""Newsdesk (untitled film, Sam 26 Oct): the news presenter, an ORIGINAL person in the satire house style.

Blended from the look of Sam's three reference presenters (references/newsdesk/presenter-1..3.jpg) so he reads as a
believable Israeli evening-news anchor, but built to look like none of them: he takes the type, never a face.
  from the refs: navy suit, white shirt, dark tie, a tiny clip mic on the tie, dark-framed glasses, a trimmed dark
                 beard, a level, serious on-air face
  his own:       a longer, narrower face with a high forehead; thick dark hair cut short at the sides with a soft
                 wave on top pushed back off the face (none of the refs has it); slim rounded-rectangle frames in
                 dark tortoiseshell; a close-cropped beard that follows the jaw with a joined moustache; heavy straight
                 brows; deep-set hazel eyes; a slightly long nose with a small bump; aged about 40, a little grey at
                 the temples; a deep burgundy tie with a fine diagonal stripe
His front head is drawn here; every other view comes from views.head_view, which reads the same design keys (hair,
beard, glasses, colours), so he stays the same man from any angle.

Moods (sp['mood']): 'neutral' (on-air, the default), 'grave' (bad news), 'smile' (sign-off), plus the shared
moods from shocking_cast ('alarm', 'wtf', 'scared', ...).

    python3 source/newsdesk_cast.py sheet OUT.jpg     the presenter in every view, seated, close-up, beside a 1.75 m person
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import shocking_cast as SC       # noqa: E402  (installs the shared mouths; its head/torso hooks stay in the chain)
from shocking_cast import brows, eye_state, mouth_or_talk   # noqa: E402
from traitors_cast import blend, dk, eye, ears             # noqa: E402
from ed import INK, curve, oval  # noqa: E402

P_SKIN = (220, 176, 140)
P_HAIR = (40, 32, 28)
P_HAIR_L = (70, 56, 48)
P_GREY = (150, 144, 140)
P_IRIS = (120, 104, 58)          # hazel
P_FRAME = (78, 52, 36)           # dark tortoiseshell
P_FRAME_L = (128, 88, 56)
P_LIP = (184, 118, 104)
P_TIE = (104, 28, 44)            # deep burgundy
NAVY_SUIT = (30, 38, 62)


def _beard(p, sp, hx, hy, hw, hh, fx, fy):
    """A short, close-trimmed beard: a band along the jaw from the sideburns, a neat moustache joined to it at the
    corners of the mouth, bare cheeks above. One flat shape, lighter than the hair (a crop, not a bush), its cheek edge
    softened by a few short strokes; the mouth is drawn over it."""
    c = blend(sp['skin'], P_HAIR, 0.5)
    edge = blend(sp['skin'], P_HAIR, 0.75)
    top = hy + 4
    jaw = [(hx - hw * 0.99, top), (hx - hw * 0.98, hy + hh * 0.46), (hx - hw * 0.85, hy + hh * 0.83),
           (hx - hw * 0.46, hy + hh * 1.1), (fx, hy + hh * 1.18), (hx + hw * 0.46, hy + hh * 1.1),
           (hx + hw * 0.85, hy + hh * 0.83), (hx + hw * 0.98, hy + hh * 0.46), (hx + hw * 0.99, top)]
    inner = [(hx + hw * 0.9, top), (hx + hw * 0.82, fy + 48), (hx + hw * 0.62, fy + 64), (fx + 30, fy + 58),
             (fx + 24, fy + 42), (fx + 10, fy + 38), (fx, fy + 40), (fx - 10, fy + 38), (fx - 24, fy + 42),
             (fx - 30, fy + 58), (hx - hw * 0.62, fy + 64), (hx - hw * 0.82, fy + 48), (hx - hw * 0.9, top)]
    p.poly(curve(jaw + inner, 4), c, INK, 2.0)
    rng = np.random.default_rng(11)
    for _ in range(16):                                   # short strokes on the cheek edge: cropped, not painted on
        sgn = -1 if rng.random() < 0.5 else 1
        u = rng.uniform(0.0, 1.0)
        x = hx + sgn * hw * (0.88 - 0.2 * u)
        y = top + 6 + u * (fy + 50 - top)
        p.line([(x, y), (x - sgn * 3, y + 5)], edge, 1.2)


def presenter_head(img, p, sp, t, hx, hy):
    hw, hh, skin = sp.get('hw', 66), sp.get('hh', 100), sp['skin']
    fx = hx + sp.get('turn', 0.0) * hw * 0.2
    fy = hy + 10 * sp.get('down', 0.0)
    ears(p, hx, hy + 6, hw, skin)
    outline = curve([(hx - hw, hy - 14), (hx - hw * 0.9, hy - hh * 0.76), (hx - hw * 0.46, hy - hh * 1.06),
                     (hx + hw * 0.46, hy - hh * 1.06), (hx + hw * 0.9, hy - hh * 0.76), (hx + hw, hy - 14),
                     (hx + hw * 1.0, hy + hh * 0.46), (hx + hw * 0.86, hy + hh * 0.84), (hx + hw * 0.46, hy + hh * 1.1),
                     (hx, hy + hh * 1.16), (hx - hw * 0.46, hy + hh * 1.1), (hx - hw * 0.86, hy + hh * 0.84),
                     (hx - hw * 1.0, hy + hh * 0.46)], 4)          # long and narrow, a high forehead
    p.poly(outline, skin, INK, 2.6)
    young = sp.get('young', False)
    if sp.get('beard'):
        _beard(p, sp, hx, hy, hw, hh, fx, fy)
    else:                                                 # clean-shaven: the chin's soft crease only
        p.line(curve([(fx - 12, fy + 80), (fx, fy + 83), (fx + 12, fy + 80)], 3), dk(skin, 0.84), 1.3)
    sd = dk(skin, 0.84)
    st = eye_state(sp, lid=0.26)                          # deep-set: the lid sits a little low
    for sgn in (-1, 1):
        ex, ey = fx + sgn * 25, fy - 8
        p.line(curve([(ex - 13, ey - 11), (ex, ey - 14), (ex + 13, ey - 11)], 3), sd, 1.4)   # the socket's shadow
        eye(p, ex, ey, sgn, 12, 7, P_IRIS, st, dk(skin, 0.86), liner=2.4)
        if not young:
            p.line([(ex - 9, ey + 11), (ex + 1, ey + 13), (ex + 9, ey + 11)], sd, 1.2)      # a faint line under
    mood = sp.get('mood', 'neutral')
    bsp = dict(sp, mood={'grave': 'upset'}.get(mood, mood), strength=0.45 if mood == 'grave' else sp.get('strength', 1.0))
    brows(p, bsp, fx, fy - 30, 25, sp.get('hair_c', P_HAIR), 6.5, 1, 0, 30)  # heavy, straight brows
    # the glasses: slim rounded-rectangle frames, tortoiseshell, thicker along the top
    for sgn in (-1, 1):
        ex, ey = fx + sgn * 26, fy - 7
        fr = curve([(ex - 21, ey - 12), (ex + 21, ey - 12), (ex + 20, ey + 12), (ex - 20, ey + 12)], 3)
        p.line(fr + [fr[0]], P_FRAME, 3.4)
        p.line([(ex - 20, ey - 12), (ex + 20, ey - 12)], P_FRAME, 4.6)
        p.line([(ex - 14, ey - 13), (ex - 4, ey - 13)], P_FRAME_L, 1.6)
        p.line([(ex + sgn * 21, ey - 8), (hx + sgn * (hw + 1), fy - 12)], P_FRAME, 2.8)
    p.line([(fx - 6, fy - 14), (fx, fy - 17), (fx + 6, fy - 14)], P_FRAME, 3.0)
    # a slightly long nose with a small bump on the bridge
    p.line([(fx - 1, fy - 2), (fx - 4, fy + 10), (fx - 3, fy + 14), (fx - 7, fy + 30), (fx, fy + 36), (fx + 9, fy + 33)],
           INK, 1.9)
    p.line([(fx - 11, fy + 33), (fx - 7, fy + 36)], INK, 1.4)
    my = fy + 52
    if mood == 'grave':
        p.poly(curve([(fx - 20, my + 3), (fx, my - 1), (fx + 20, my + 3), (fx, my + 10)], 3), P_LIP, INK, 1.6)
        p.line(curve([(fx - 20, my + 4), (fx, my + 2), (fx + 20, my + 5)], 3), INK, 2.4)
    elif mood == 'smile':
        p.poly(curve([(fx - 22, my - 1), (fx, my + 1), (fx + 22, my - 1), (fx, my + 12)], 3), P_LIP, INK, 1.6)
        p.line(curve([(fx - 22, my - 1), (fx - 8, my + 6), (fx + 8, my + 6), (fx + 22, my - 1)], 3), INK, 2.4)
    else:
        mouth_or_talk(p, sp, fx, my, P_LIP, width=21, lips=True)
    # hair: short at the sides, a soft wave on top pushed back off the face; grey just at the temples
    hc = sp.get('hair_c', P_HAIR)
    hl = sp.get('hair_l', P_HAIR_L)
    full = 14 if young else 0                             # the younger man: fuller on top and at the sides
    top = hy - hh - 22 - full
    hair = [(hx - hw - 5, hy - 8), (hx - hw - 8 - full * 0.4, hy - 50), (hx - hw * 0.96, top + 40), (hx - hw * 0.66, top + 10),
            (hx - hw * 0.24, top - 6), (hx + hw * 0.2, top - 10), (hx + hw * 0.62, top - 2), (hx + hw * 0.94, top + 24),
            (hx + hw + 8 + full * 0.4, hy - 52), (hx + hw + 5, hy - 8), (hx + hw - 5, hy - 44), (hx + hw * 0.8, hy - hh * 0.8),
            (hx + hw * 0.42, hy - hh * 0.94), (hx, hy - hh * 0.98), (hx - hw * 0.44, hy - hh * 0.96),
            (hx - hw * 0.8, hy - hh * 0.82), (hx - hw + 5, hy - 44)]
    p.poly(curve(hair, 4), hc, INK, 2.6)
    for k in range(5):                                    # the wave: strands lifting up and back
        x0 = hx - hw * 0.62 + k * hw * 0.3
        p.line(curve([(x0, hy - hh * 0.92), (x0 + 6, top + 20), (x0 + 18, top + 6)], 3)[:9], hl, 1.5)
    for sgn in ((-1, 1) if sp.get('grey') else ()):                                   # a little grey at the temples: three fine strokes
        for k in range(3):
            x = hx + sgn * (hw - 1 + 2 * k)
            p.line([(x, hy - 14 - 4 * k), (x + sgn * 1, hy - 40 - 2 * k)], P_GREY, 1.6)
    return fx


def presenter_torso(img, p, sp, t):
    tie = sp.get('tie', P_TIE)
    p.poly([(-12, 16), (12, 16), (15, 196), (0, 220), (-15, 196)], tie, INK, 2.0)
    p.poly([(-12, -2), (12, -2), (9, 18), (-9, 18)], tie, INK, 2.0)
    for k in range(9):                                    # a fine diagonal stripe
        y = 34 + 19 * k
        p.line([(-12, y), (12, y + 10)], dk(tie, 0.72), 1.1)
    SC.lapels(p, sp)
    p.poly([(-5, 70), (5, 70), (5, 84), (-5, 84)], (24, 24, 26), INK, 1.2)       # the clip mic on the tie
    p.line([(0, 84), (6, 120), (16, 150)], (24, 24, 26), 1.2)                   # its thin black lead


# --------------------------------------------------------------------------------------------- the hooks
_head, _torso = B.head, B.torso


def head(img, p, sp, t, hx, hy):
    if sp.get('who') == 'presenter':
        return presenter_head(img, p, sp, t, hx, hy)
    return _head(img, p, sp, t, hx, hy)


def torso(img, p, sp, t):
    _torso(img, p, sp, t)
    if sp.get('who') == 'presenter':
        presenter_torso(img, p, sp, t)


B.head, B.torso = head, torso

# hair/beard/glasses keys: what views.head_view reads for every other view (three-quarter, side, back)
PRESENTER = dict(who='presenter', name='Presenter', skin=P_SKIN, hw=66, hh=100, head_dy=8, jaw='long',
                 hair='side', hair_c=P_HAIR, grey=P_GREY, beard='short', beard_c=P_HAIR, glasses=True,
                 glasses_c=P_FRAME, brow_c=P_HAIR, brow_w=6.0, nose='long', outfit='suit', jacket=NAVY_SUIT,
                 shirt=(246, 246, 244), tie=P_TIE, shoulders=152, trousers=NAVY_SUIT, full=True, pose='custom',
                 height=1.80)
# Netan-Yahoo! (Sam, 26 Oct, answer 2): the same man, younger: same navy suit and glasses; no beard, no grey; darker,
# fuller hair; quicker head moves and more upright (both in the film's acting, not the drawing)
P_HAIR_Y, P_HAIR_YL = (26, 20, 18), (58, 44, 38)
PRESENTER_YOUNG = dict(PRESENTER, beard=None, grey=None, hair_c=P_HAIR_Y, hair_l=P_HAIR_YL, brow_c=P_HAIR_Y, young=True,
                       height=1.80)
CAST = {'presenter': PRESENTER, 'presenter_young': PRESENTER_YOUNG}


def sheet(out):
    """The presenter in every view (front, three-quarter, side, three-quarter back, back), seated behind a desk of the
    set's height, his face large in three moods, beside a plain 1.75 m person and a 1 m ruler."""
    import views as V
    import moves
    import landmarks
    import sizes
    from PIL import ImageFont
    B.SS = 1                                              # sheets draw at frame size (as prepper's)
    W, H = 2560, 1880
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 40)
    small = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 26)
    cam = B.Cam(1.0, 540, 960)
    s = 0.62

    def tile(draw, box, at):
        lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        draw(lay)
        img.alpha_composite(lay.crop(box), at)

    d.text((40, 24), 'NEWSDESK: the presenter (an original person, not any of the reference presenters)', font=big,
           fill=(30, 30, 30))
    names = ('front', 'three-quarter', 'side', '3/4 back', 'back')
    for i, yaw in enumerate((0, 45, 90, 135, 180)):
        tile(lambda im, yaw=yaw: V.person(im, cam, 540, 300, s, dict(PRESENTER), 0.0, yaw), (330, 110, 750, 900),
             (20 + 380 * i, 90))
        d.text((230 + 380 * i, 890), names[i], font=small, fill=(40, 40, 40), anchor='mm')
    lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    landmarks.draw(ld, 540, 300, s, 1000)
    sizes.scale_ref(ld, 640, 300 + 928 * s, s / V.M_PER_UNIT)
    img.alpha_composite(lay.crop((330, 110, 750, 900)), (1920, 90))
    d.text((2130, 890), '1.75 m person, 1 m ruler', font=small, fill=(40, 40, 40), anchor='mm')

    def seated(im):                                       # seated at the desk: a plain bar at the desk's 0.78 m
        j = moves.seated(PRESENTER)
        j['seated'] = False
        V.person(im, cam, 540, 300, s, dict(PRESENTER), 0.0, 0, j)   # the pose's own bob seats him
        dd = ImageDraw.Draw(im)
        floor = 300 + 928 * s
        top = floor - 0.78 / V.M_PER_UNIT * s
        dd.rectangle([330, top, 750, floor], fill=(40, 90, 190), outline=INK, width=3)
        dd.rectangle([330, top - 12, 750, top], fill=(246, 246, 246), outline=INK, width=3)
    tile(seated, (330, 200, 750, 900), (20, 960))
    d.text((230, 1850), 'seated at the desk', font=small, fill=(40, 40, 40), anchor='mm')
    for i, mood in enumerate(('neutral', 'grave', 'smile', 'talk')):
        sp = dict(PRESENTER, mood=mood if mood != 'talk' else 'neutral', mouth='v:AI' if mood == 'talk' else 'rest')
        tile(lambda im, sp=sp: V.person(im, cam, 540, 820, 1.5, sp, 0.0, 0), (310, 280, 770, 1150),
             (440 + 520 * i, 960))
        label = {'neutral': 'on air', 'grave': 'grave news', 'smile': 'sign-off', 'talk': 'talking'}[mood]
        d.text((670 + 520 * i, 1850), label, font=small, fill=(40, 40, 40), anchor='mm')
    img.convert('RGB').save(out, quality=90)
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))


cast_sheet = sheet                                       # the kit catalogue's name for it


def LINE_SUBJECTS():
    """The presenter alone, large, for the line-work check (linecheck.py), and the chair."""
    import views as V
    import newsdesk_props as NP
    import sets as S

    def presenter(im):
        V.person(im, B.Cam(1.0, 540, 960), 540, 420, 1.45, dict(PRESENTER), 0.0, 0)

    def chair(im):
        NP.round_chair(im, S.Cam((0.0, 1.3, -1.6), (0.0, 0.42, 0.0), focal=1500), 0.0, 0.0, 200)
    return [('presenter', presenter), ('round chair', chair)]
