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
P4.MEASURED['walliams']['philtrum'] += 0.025      # by eye (w01, w03): a long gap the card's smiling photo hid
P4.TUNE['walliams'] = dict(nose_long=2.0, forehead_wide=3.0, mouth_wide=2.5, lip_top=2.0, eye_size=2.0,
                           eyes_apart=3.0, chin_long=3.0, jaw_wide=2.0, lip_low=2.0)   # 12 Nov, likeness check rounds

SKIN = (222, 168, 142)            # card: (208, 144, 121), lifted for the flat style (Brand's is 232, 176, 150)
HAIR = (104, 80, 62)              # brown on top
HAIR_L = (146, 120, 98)
HAIR_GREY = (150, 142, 134)       # the grey sides
BROW = (88, 70, 58)
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


# ---------------------------------------------------------------------------------------------- the beard
def beard(p, f, L):
    """Short and close (w01, w02): from low on the cheeks (about the nose's base) round the jaw and chin, grey-white;
    a grey-brown moustache over the thin upper lip, joining a patch under the lower lip. Tufted edges (AV.tufts)."""
    fw, jw, ny, l0, l13, l17, mw, nw = L['fw'], L['jw'], L['nose_y'], L['lip0'], L['lip13'], L['lip17'], L['mw'], L['nw']
    e = fw * 0.5
    bottom = [(-e - 0.004, 0.5), (-e - 0.002, 0.66), (-jw * 0.47, 0.84), (-jw * 0.3, 0.96), (-0.1, 1.01), (0.0, 1.015),
              (0.1, 1.01), (jw * 0.3, 0.96), (jw * 0.47, 0.84), (e + 0.002, 0.66), (e + 0.004, 0.5)]
    cheek = [(e - 0.02, 0.52), (e * 0.8, ny + 0.02), (mw * 0.75, l0 - 0.005)]
    corner = [(mw * 0.62, l13 + 0.012), (mw * 0.55, l17 + 0.02), (mw * 0.25, l17 + 0.035)]
    right = cheek + corner + [(0.0, l17 + 0.04)]
    left = [(-u, v) for u, v in right[::-1]]
    edge = AV.tufts(bottom, 0.008, 0.016, out=1.0, seed=41)
    inner = AV.tufts(right + left[1:], 0.009, 0.014, out=1.0, seed=42)
    p.poly(f.pts(edge + inner), BD_MID, None)
    low_top = AV.tufts([(e + 0.01, 0.7), (jw * 0.4, 0.8), (mw * 0.45, l17 + 0.07), (0.0, l17 + 0.085),
                        (-mw * 0.45, l17 + 0.07), (-jw * 0.4, 0.8), (-e - 0.01, 0.7)], 0.012, 0.016, out=1.0, seed=43)
    n = len(edge)
    p.poly(f.pts(edge[n // 6: n - n // 6] + low_top), BD_LIGHT, None)
    mt = max(ny + 0.04, l0 - 0.028)                     # a thin band over the lip: skin shows under the nose
    top = AV.tufts([(-mw * 0.62, l13 + 0.01), (-mw * 0.5, mt + 0.012), (-nw * 0.45, mt), (0.0, mt + 0.008),
                    (nw * 0.45, mt), (mw * 0.5, mt + 0.012), (mw * 0.62, l13 + 0.01)], 0.006, 0.012, out=1.0, seed=44)
    under = [(mw * 0.52, l13 + 0.004), (0.0, l0 + 0.004), (-mw * 0.52, l13 + 0.004)]
    p.poly(f.pts(top + under), BD_MOUST, None)
    patch = [(-mw * 0.16, l17 + 0.004), (mw * 0.16, l17 + 0.004), (mw * 0.1, l17 + 0.04), (-mw * 0.1, l17 + 0.04)]
    p.poly(curve(f.pts(patch), 3), BD_MOUST, None)
    rng = np.random.default_rng(45)                      # a few dark flecks in the grey (salt and pepper)
    for _ in range(34):
        u, v = rng.uniform(-e * 0.85, e * 0.85), rng.uniform(0.7, 0.97)
        if abs(u) < jw * 0.5 * (1.0 - max(0.0, v - 0.84) * 2.4) and abs(u) > mw * 0.55:
            p.line([f(u, v), f(u + 0.004, v + 0.018)], (120, 112, 104), 1.3)
    o = curve(f.pts(BC._outline(L)), 4)                  # the face's ink back over the beard's edge
    p.line(o + o[:1], INK, 2.6)


# ---------------------------------------------------------------------------------------------- the hair
def hair(p, f, L):
    """Short (w01, w02): grey, close-cut sides over the ears; brown on top, swept up and back off a high, clear
    forehead into a small lifted front (the quiff leans to our right). Drawn after the face."""
    e, c = L['fw'] * 0.5, L['fhw'] * 0.5
    hl = -0.13                                                   # a high, clear forehead
    cap = [(-e - 0.01, 0.3), (-e - 0.02, 0.04), (-e + 0.04, -0.22), (-0.24, -0.38), (0.0, -0.43), (0.24, -0.38),
           (e - 0.04, -0.22), (e + 0.02, 0.04), (e + 0.01, 0.3), (e - 0.025, 0.3), (c - 0.01, 0.12), (c - 0.05, 0.0),
           (c * 0.6, hl), (0.0, hl - 0.01), (-c * 0.6, hl), (-c + 0.05, 0.0), (-c + 0.01, 0.12), (-e + 0.025, 0.3)]
    p.poly(curve(f.pts(cap), 2), HAIR_GREY, INK, 2.4)           # the grey, close-cut sides hugging the skull
    top = [(-c - 0.02, -0.16), (-c - 0.01, -0.3), (-0.2, -0.47), (-0.02, -0.53), (0.14, -0.555), (0.26, -0.5),
           (c + 0.03, -0.36), (c + 0.03, -0.18), (c * 0.86, -0.1), (c * 0.5, hl), (0.1, hl - 0.03), (-0.04, hl - 0.015),
           (-c * 0.5, hl + 0.005), (-c * 0.85, -0.1)]
    p.poly(curve(f.pts(AV.tufts(top[:7], 0.008, 0.02, out=1.0, seed=51) + top[7:]), 2), HAIR, INK, 2.4)
    for k in range(6):                                           # swept up and back, towards our right
        u = -c * 0.75 + k * c * 0.3
        p.line(curve(f.pts([(u, hl - 0.01), (u + 0.05, -0.3), (u + 0.1, -0.46)]), 3),
               HAIR_L if k % 2 else dk(HAIR, 0.78), 1.6)


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
        P4.nose(p, f, L, SKIN)
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
    P4.nose(p, f, L, SKIN)
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
