#!/usr/bin/env python3
"""MAP  Blessed, note 25 (Sam, 12 Nov): David Walliams led by two officers into the prison door Brand just left, at the
end of the gates shot. Front-on only (Sam: "everyone front-on, South Park movement"), scared and alarmed. His head is
a measured likeness (likeness.py card on w01-w03, references/blessed/likeness/) on the patriots4 face layout, drawn
at Brand's size (blessed_cast HEAD_K), the Brand way.

    WALLIAMS  card (12 Nov): a short nose (98th centile), a narrow forehead (97th), narrow hooded eyes (92nd), a wide
              mouth (91st), a wide nose (87th), a thin upper lip (85th). By eye: short brown hair swept up and back off
              a clear, high forehead, grey at the sides; a short salt-and-pepper beard, grey-white on the chin and jaw,
              darker grey-brown at the moustache; light skin. Very tall (1.96 m). Prison: Brand's grey tracksuit.

    python3 source/blessed_walliams.py head OUT.png [--average] [--mood M]   his head straight on (likeness.py check)
    python3 source/blessed_walliams.py faces OUT.jpg                          his face in each mood, his photos beside

Map: measures 35 | moods 45 | beard 55 | hair 95 | mouth 140 | head 165 | the person 205 | sheets 225
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import blessed_cast as BC          # noqa: E402  (P4, TC, the house head size, the tracksuit)
from blessed_cast import P4, TC, AV, B, V, dk, INK, curve, oval  # noqa: E402

# ---------------------------------------------------------------------------------------------- measures (12 Nov)
_card = json.load(open(os.path.join(HERE, '..', 'references', 'blessed', 'likeness', 'walliams-card.json')))
_WM, _WA = _card['measures'], _card['average']
P4.MEASURED['walliams'] = {k: P4.AVG[k] + _WM[k] - _WA[k] for k in P4.AVG}
P4.PUSH['walliams'] = 1.6
# Note 29 (Sam, 12 Nov: not recognisable): a new card from Sam's straight-on photos w06, w07 with w01, w02. Its top
# measures: a broad, square jaw (99th), a long chin (98th), a narrow forehead, a long gap nose to lip, small wide-set
# eyes. Its 'short nose' (82nd, the photos disagree) is the long chin taking the face's height: by eye the nose is
# long and straight, so it is pushed the other way (TUNE -1.5), as the first try's tiny button nose taught.
P4.TUNE['walliams'] = dict(nose_long=-1.5, chin_long=2.2, jaw_wide=2.0, face_wide=0.4, forehead_wide=1.2,
                           eyes_apart=0.5, eye_size=1.0, eye_open=0.8, mouth_wide=-1.5, lip_top=0.6, lip_low=0.6)

SKIN = (226, 172, 146)            # card: light (w06, w07), lifted for the flat style (Brand's is 232, 176, 150)
HAIR = (84, 64, 50)               # dark brown on top (w06, w07, w09)
HAIR_L = (120, 96, 78)
HAIR_GREY = (104, 90, 80)        # the short sides, greying (w07)
STUBBLE = (206, 170, 154)         # note 29: short grey stubble (w07, w10) instead of the full white beard, so the jaw
#                                   and long chin (his strongest shapes) show
BROW = (72, 56, 46)
IRIS = (92, 74, 54)
LIP = (196, 132, 120)
BD_LIGHT = (214, 210, 204)        # grey-white beard on the chin and jaw
BD_MID = (168, 158, 148)          # grey on the cheeks
BD_MOUST = (126, 112, 100)        # darker grey-brown at the moustache

# ---------------------------------------------------------------------------------------------- moods
# brow: up (+); frown (-) lifts the inner ends (worry); lid: upper lid down; wide: the stare (P4.eyes)
MOODS = {'neutral': dict(brow=0.0, frown=0.0, lid=0.24, wide=0.0, mouth='lips', smile=0.1),
         # scared and alarmed (note 25): brows high and pinched up in the middle, eyes wide, mouth pulled into a
         # wide grimace, the teeth showing
         'scared': dict(brow=0.05, frown=-0.07, lid=0.0, wide=1.0, mouth='grimace'),
         'alarmed': dict(brow=0.06, frown=-0.04, lid=0.0, wide=0.8, mouth='gasp')}


# ---------------------------------------------------------------------------------------------- the stubble
def beard(p, f, L):
    """Note 29: short grey stubble (w07, w10), a shade over the jaw, chin and upper lip that keeps the face's shape:
    the broad square jaw and the long chin (with its dimple) read through it."""
    fw, jw, ny, l0, l13, l17, mw, nw = L['fw'], L['jw'], L['nose_y'], L['lip0'], L['lip13'], L['lip17'], L['mw'], L['nw']
    e = fw * 0.5
    o = BC._outline(L)
    low = [q for q in o if q[1] > 0.62]                  # the face's own edge from cheek to cheek, round the chin
    low.sort(key=lambda q: q[0])
    top = [(e * 0.86, 0.62), (e * 0.62, ny + 0.03), (mw * 0.62, l0 - 0.01), (nw * 0.4, ny + 0.035), (0.0, ny + 0.04),
           (-nw * 0.4, ny + 0.035), (-mw * 0.62, l0 - 0.01), (-e * 0.62, ny + 0.03), (-e * 0.86, 0.62)]
    p.poly(curve(f.pts(low + top), 2), STUBBLE, None)
    p.poly(curve(f.pts([(-mw * 0.5, l13), (mw * 0.5, l13), (mw * 0.42, l17 + 0.012), (0.0, l17 + 0.02),
                        (-mw * 0.42, l17 + 0.012)]), 3), SKIN, None)      # the lips' skin
    sd = dk(SKIN, 0.78)
    cy = (l17 + 1.0) / 2 + 0.02                         # the chin: a crease under the lip, the dimple below
    p.line(curve(f.pts([(-mw * 0.28, l17 + 0.045), (0.0, l17 + 0.055), (mw * 0.28, l17 + 0.045)]), 3), sd, 1.6)
    p.line(f.pts([(0.0, cy), (0.0, cy + 0.04)]), sd, 1.8)
    for sgn in (-1, 1):                                  # the square jaw's corner
        p.line(curve(f.pts([(sgn * jw * 0.44, 0.74), (sgn * jw * 0.36, 0.86)]), 3), sd, 1.4)
    oo = curve(f.pts(o), 4)                              # the face's ink back over the stubble's edge
    p.line(oo + oo[:1], INK, 2.6)


# ---------------------------------------------------------------------------------------------- the hair
def hair(p, f, L):
    """Note 29 (w06, w07, w09): dark brown, short at the sides and greying there; on top swept up and back off a high
    forehead that recedes at the temples, lifted at the front, parted on our right."""
    e, c = L['fw'] * 0.5, L['fhw'] * 0.5
    hl = -0.12                                                   # the hairline over the middle
    tl = -0.04                                                   # the temples: higher (receding)
    cap = [(-e - 0.005, 0.27), (-e - 0.012, 0.04), (-e + 0.03, -0.2), (-0.24, -0.34), (0.0, -0.38), (0.24, -0.34),
           (e - 0.03, -0.2), (e + 0.012, 0.04), (e + 0.005, 0.27), (e - 0.02, 0.27), (c - 0.005, 0.1),
           (c - 0.02, tl), (c - 0.09, tl - 0.03), (0.0, hl), (-c + 0.09, tl - 0.03), (-c + 0.02, tl),
           (-c + 0.005, 0.1), (-e + 0.02, 0.27)]
    p.poly(curve(f.pts(cap), 2), HAIR_GREY, INK, 2.4)           # the short sides, close to the skull
    top = [(-c + 0.0, -0.12), (-c - 0.005, -0.25), (-0.2, -0.38), (-0.1, -0.45), (0.04, -0.46), (0.19, -0.42),
           (c + 0.0, -0.3), (c + 0.005, -0.16), (c - 0.07, tl - 0.05), (c * 0.45, hl - 0.03), (0.06, hl - 0.04),
           (-0.08, hl - 0.03), (-c * 0.55, hl - 0.02), (-c + 0.06, tl - 0.06)]
    p.poly(curve(f.pts(AV.tufts(top[:7], 0.006, 0.016, out=1.0, seed=51) + top[7:]), 2), HAIR, INK, 2.4)
    p.line(curve(f.pts([(c * 0.62, hl - 0.02), (c * 0.66, -0.28), (c * 0.6, -0.4)]), 3), dk(HAIR, 0.6), 1.8)  # parting
    for k in range(6):                                           # swept up and back from the front
        u = -c * 0.55 + k * c * 0.22
        p.line(curve(f.pts([(u, hl - 0.03), (u - 0.02, -0.28), (u - 0.05, -0.4)]), 3),
               HAIR_L if k % 2 else dk(HAIR, 0.75), 1.5)


def long_nose(p, f, L, skin):
    """Note 29: long and straight, by eye (the first try's card made it a button): both sides of the bridge from
    between the eyes down to a broad, rounded tip, then P4's wings and nostrils."""
    nw, y = L['nw'], L['nose_y']
    sd = dk(skin, 0.74)
    for sgn in (-1, 1):
        p.line(curve(f.pts([(sgn * 0.035, L['eye_y'] + 0.01), (sgn * 0.04, (L['eye_y'] + y) / 2),
                            (sgn * nw * 0.3, y - 0.07)]), 3), sd, 1.7)
    p.line(curve(f.pts([(-nw * 0.24, y - 0.05), (0.0, y - 0.07), (nw * 0.24, y - 0.05)]), 3), dk(skin, 0.86), 1.4)
    P4.nose(p, f, L, skin)


# ---------------------------------------------------------------------------------------------- the mouth
def mouth(p, f, L, kind):
    """'grimace' (scared: wide and flat, the corners pulled out and down, both rows of teeth), 'gasp' (an open O)."""
    hw, l0, l13, l17 = L['mw'] / 2, L['lip0'], L['lip13'], L['lip17']
    if kind == 'gasp':
        x, y = f(0.0, (l13 + l17) / 2 + 0.01)
        rx, ry = hw * P4.H * 0.6, (l17 - l0) * P4.H * 0.9
        p.poly(oval(x, y, rx, ry, 24), (70, 26, 30), INK, 2.4)
        p.poly(oval(x, y + ry * 0.25, rx * 0.6, ry * 0.5, 20), (40, 14, 18), None)
        p.poly(oval(x, y - ry * 0.74, rx * 0.66, ry * 0.16, 14), (250, 248, 240), None)
        return
    hw *= 1.1
    pts = [(-hw, l13 + 0.02), (-hw * 0.5, l13 - 0.012), (0.0, l13 - 0.016), (hw * 0.5, l13 - 0.012), (hw, l13 + 0.02),
           (hw * 0.6, l17 + 0.022), (0.0, l17 + 0.028), (-hw * 0.6, l17 + 0.022)]
    p.poly(curve(f.pts(pts), 3), (70, 26, 30), INK, 2.4)
    p.poly(curve(f.pts([(-hw * 0.85, l13 + 0.012), (0.0, l13 - 0.01), (hw * 0.85, l13 + 0.012), (hw * 0.6, l13 + 0.03),
                        (0.0, l13 + 0.026), (-hw * 0.6, l13 + 0.03)]), 3), (250, 248, 240), None)    # top teeth
    p.poly(curve(f.pts([(-hw * 0.55, l17 + 0.006), (0.0, l17 + 0.0), (hw * 0.55, l17 + 0.006), (hw * 0.45, l17 + 0.02),
                        (0.0, l17 + 0.024), (-hw * 0.45, l17 + 0.02)]), 3), (240, 238, 230), None)   # bottom teeth
    p.line(curve(f.pts([(-hw * 0.7, l13 + 0.03), (0.0, l13 + 0.035), (hw * 0.7, l13 + 0.03)]), 3), (200, 196, 190), 1.2)


# ---------------------------------------------------------------------------------------------- his head
def walliams_head(img, p, sp, t, hx, hy):
    with BC._Big():
        return _head(img, p, sp, t, hx, BC._lift(hy))


def _head(img, p, sp, t, hx, hy):
    L = P4.layout(P4.target('walliams', sp.get('average', False)))
    f = P4.Face(hx, hy, 0.0, sp.get('turn', 0.0), sp.get('down', 0.0))
    look = MOODS.get(sp.get('mood', 'neutral'), MOODS['neutral'])
    AV._ears(p, f, L, SKIN)
    p.poly(curve(f.pts(BC._outline(L)), 4), SKIN, INK, 2.6)
    beard(p, f, L)
    if sp.get('empty'):                                  # the likeness check's bare face
        long_nose(p, f, L, SKIN)
        P4.lips(p, f, L, dict(sp, smile=0.1), LIP, f(0.0, L['lip13']))
        hair(p, f, L)
        return f(0.0, L['lip13'])[0]
    sh = dk(SKIN, 0.84)                                  # hooded lids: a soft fold over each eye; bags below
    for sgn in (-1, 1):
        cx, ey, w = sgn * L['ecx'], L['eye_y'], L['ew'] * 0.6
        p.line(curve(f.pts([(cx - sgn * w, ey - 0.035), (cx, ey - 0.05), (cx + sgn * w * 1.15, ey - 0.008)]), 3), sh,
               1.6)                                       # the hood droops over the outer corner
        p.line(curve(f.pts([(cx - sgn * w * 0.6, ey + 0.046), (cx, ey + 0.064), (cx + sgn * w * 0.7, ey + 0.05)]), 3), sh,
               1.5)
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', look['lid']), look=sp.get('look', 0.0),
                          gaze_dy=BC.gaze(L, sp.get('gaze_dy', 0.0))), IRIS, dk(SKIN, 0.8), liner=2.8,
            wide=look['wide'])
    P4.brows(p, f, L, BROW, 0.05, look['brow'] + sp.get('brow_up', 0.0), look['frown'] + sp.get('frown', 0.0))
    long_nose(p, f, L, SKIN)
    fx, my = f(0.0, L['lip13'])
    if str(sp.get('mouth', 'rest')).startswith('v:') or look['mouth'] == 'lips':
        P4.lips(p, f, L, dict(sp, smile=look.get('smile', 0.0)), LIP, (fx, my - 6))
    else:
        mouth(p, f, L, look['mouth'])
    hair(p, f, L)
    return fx


# ---------------------------------------------------------------------------------------------- the person
WALLIAMS = dict(who='walliams', name='David Walliams', neck_w=1.3, neck_shade=True, skin=SKIN, hw=66, hh=96, head_dy=10, hair='crop',
                hair_c=HAIR, brow_c=BROW, brow_w=4.6, outfit='jumper', jacket=BC.TRACK, sleeve=BC.TRACK,
                trousers=BC.TRACK, shirt=BC.TRACK, tie=None, shoe=(236, 236, 236), shoulders=158, full=True,
                pose='custom', height=1.96, seed=95, look_='prison', mood='scared')
TC.HEADS['walliams'] = walliams_head
TC.TORSOS['walliams'] = BC.brand_torso           # look_='prison': the tracksuit's collar and zip
BC.FACE_HEADS.add(walliams_head)                 # he has a mouth at rest (blessed_cast.mouth_faults)
BC.CAST['walliams'] = WALLIAMS


# ---------------------------------------------------------------------------------------------- sheets
def head_png(out, average=False, mood='neutral'):
    """His head straight on, as likeness.py check wants it (the bare face; --average: the average face, the bias)."""
    B.SS = 1
    im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    V.person(im, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(WALLIAMS, average=average, mood=mood), 0.0, 0)
    im.crop((180, 300, 900, 1250)).convert('RGB').save(out)
    return out


def faces_sheet(out):
    """His face large in each mood, two photos beside (rule 76)."""
    B.SS = 1
    tw, th = 420, 520
    img = Image.new('RGB', (tw * 5, th + 50), (232, 228, 222))
    d = ImageDraw.Draw(img)
    refs = os.path.join(HERE, '..', 'references', 'blessed', 'likeness')
    for i, name in enumerate(('w01-front-guardian.jpg', 'w02-front-bbc2024.jpg')):
        ph = Image.open(os.path.join(refs, name)).convert('RGB')
        ph.thumbnail((tw - 10, th - 10))
        img.paste(ph, (i * tw + 5, 45))
        d.text((i * tw + 8, 10), name[:3] + ' (photo)', font=BC._font(26), fill=(30, 30, 30))
    for j, mood in enumerate(('neutral', 'scared', 'alarmed')):
        im = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
        V.person(im, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(WALLIAMS, mood=mood), 0.0, 0)
        tile = im.crop((180, 280, 900, 1170)).convert('RGB')
        tile.thumbnail((tw - 10, th - 10))
        x = (j + 2) * tw
        img.paste(tile, (x + 5, 45))
        d.text((x + 8, 10), mood, font=BC._font(26), fill=(30, 30, 30))
    img.save(out, quality=88)
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'head':
        mood = sys.argv[sys.argv.index('--mood') + 1] if '--mood' in sys.argv else 'neutral'
        print(head_png(sys.argv[2], '--average' in sys.argv, mood))
    elif sys.argv[1] == 'faces':
        print(faces_sheet(sys.argv[2]))
