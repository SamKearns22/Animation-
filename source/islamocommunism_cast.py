#!/usr/bin/env python3
"""MAP  Islamocommunism (Sam, 4 Nov): the cast. Both are measured likeness heads (likeness.py cards, 4 Nov) on the
patriots4 face layout, drawn the MidTerminal way. References: references/islamocommunism/.

    ELSAYED  Abdul El-Sayed (card on 107e061d, 70cfd30c): close-set eyes, narrow face, high straight brows sloping down
             at the outside, a long nose, full lower lip. Short near-black hair slicked back off a straight hairline,
             a short trimmed full beard and moustache. Dark charcoal suit, open white collar (no tie), white pocket
             square, flag pin (Sam's Y, 4 Nov). 1.78 m.
    AOC      Alexandria Ocasio-Cortez (card on 0019c908, 445628df, 9797c588): big wide-open eyes tilted up at the
             outside, strong dark brows, a long nose, a short philtrum, full red lips (red lipstick). Long near-black
             hair, centre parting, falling past the shoulders. Black jacket over a black top, pearl earrings (Sam's Y).
             1.65 m.

Moods: 'neutral' (a warm closed smile), 'sceptic' (one brow up, mouth flat), 'smile' (big), 'hopeful' (brows up) +
talking (sp['mouth'] = 'v:SHAPE').

    python3 source/islamocommunism_cast.py sheet OUT.jpg     front, side, back of both, a 1.75 m person
    python3 source/islamocommunism_cast.py faces OUT.jpg     the faces large in every mood
    python3 source/islamocommunism_cast.py head WHO OUT.png  one head straight on (for likeness.py check)

Map: colours 30 | measures 45 | El-Sayed head 65 | AOC head 130 | hooks 215 | people 245 | sheets 260
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import midterminal_cast as MC   # noqa: E402  (installs the hooks chain and the sheet helpers)
from midterminal_cast import B, TC, P4, V, dk, blend, FONT  # noqa: E402
from ed import INK, curve, oval, open_curve  # noqa: E402

# ---------------------------------------------------------------------------------------------- colours
A_SKIN = (214, 160, 124)          # warm olive
A_HAIR = (34, 28, 26)
A_HAIR_L = (70, 60, 56)
A_IRIS = (78, 52, 36)
A_LIP = (188, 118, 104)
A_SUIT = (44, 46, 54)             # charcoal (ref 1)
O_SKIN = (226, 172, 140)
O_HAIR = (26, 20, 20)
O_HAIR_L = (64, 50, 46)
O_IRIS = (74, 46, 30)
O_LIP = (196, 30, 44)             # red lipstick (official portrait)
O_JACKET = (24, 24, 28)

# ---------------------------------------------------------------------------------------------- measures (4 Nov)
# El-Sayed (4 Nov, second pass): measured on the straight-on photo alone (107e061d), and laid on patriots4's average
# as differences from likeness.py's average (the two averages differ; pushing raw numbers sent four features the
# wrong way: check fell to 0%)
_E = dict(face_wide=0.839, jaw_wide=0.812, forehead_wide=0.917, eyes_apart=1.257, eye_size=0.181, eye_open=0.31,
          eye_tilt=0.259, brow_high=0.678, brow_slope=-14.056, nose_long=0.414, nose_wide=0.725, mouth_wide=0.913,
          lip_top=0.097, lip_low=0.17, philtrum=0.139, chin_long=0.324)
_LA = dict(face_wide=0.816, jaw_wide=0.806, forehead_wide=0.941, eyes_apart=1.296, eye_size=0.185, eye_open=0.327,
           eye_tilt=2.593, brow_high=0.592, brow_slope=-9.969, nose_long=0.392, nose_wide=0.714, mouth_wide=1.019,
           lip_top=0.104, lip_low=0.167, philtrum=0.102, chin_long=0.26)
P4.MEASURED['elsayed'] = {k: P4.AVG[k] + _E[k] - _LA[k] for k in P4.AVG}
P4.PUSH['elsayed'] = 1.8
P4.TUNE['elsayed'] = dict(face_wide=-1.5, jaw_wide=-1, brow_slope=1.0, chin_long=0.5)   # 4 Nov round 3: leaner face, straighter brows (by eye against all refs)
P4.MEASURED['aoc'] = dict(face_wide=0.847, jaw_wide=0.79, forehead_wide=0.95, eyes_apart=1.177, eye_size=0.212,
                          eye_open=0.369, eye_tilt=5.619, brow_high=0.528, brow_slope=-6.891, nose_long=0.426,
                          nose_wide=0.654, mouth_wide=0.832, lip_top=0.135, lip_low=0.195, philtrum=0.124,
                          chin_long=0.294)
P4.PUSH['aoc'] = 1.5
P4.TUNE['aoc'] = {}

SMILE = {'neutral': 0.7, 'sceptic': -0.1, 'smile': 1.4, 'hopeful': 0.9}


def _ears(p, f, L, skin):
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.5:
            continue
        ex, ey = f(sgn * (L['fw'] * 0.5 + 0.01), 0.42)
        p.poly(oval(ex, ey, 11, 24, 20), skin, INK, 2.4)
        p.line([(ex - sgn * 2, ey - 10), (ex + sgn * 3, ey), (ex - sgn * 1, ey + 10)], dk(skin, 0.7), 1.4)
        yield sgn, ex, ey


# ---------------------------------------------------------------------------------------------- El-Sayed's head
def elsayed_head(img, p, sp, t, hx, hy):
    L = P4.layout(P4.target('elsayed', sp.get('average', False)))
    f = P4.Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin, mood = A_SKIN, sp.get('mood', 'neutral')
    list(_ears(p, f, L, skin))
    p.poly(curve(f.pts(P4.outline_uv(L, 0.42)), 4), skin, INK, 2.6)
    fw, fhw = L['fw'], L['fhw']
    # the facial hair (Sam, 4 Nov, close-up ref 18d7e6e5: "a thin black moustache and a small black goatee; he is
    # quite a handsome man"): a faint shadow along the jaw only, a thin black moustache line, a soul patch under the
    # lower lip and a small goatee round the chin. The lips stay clear of it all (drawn after, below).
    # (Sam, 4 Nov, round 2: "the thin beard around his chin and lower cheeks"): a short, thin beard band along the
    # jaw from the sideburns, over the lower cheeks, thickening into the goatee at the chin; the upper cheeks clear
    # Checked against ALL his refs (107e061d, 70cfd30c, a7e25e61, 03d4bfce, the caricature 4f71c922, close-up
    # 18d7e6e5): one short, even beard, the same tone throughout: from the sideburns along a slanting cheek line to the
    # mouth corners, over the lower cheeks and jaw, round the chin; the thin moustache meets it at the mouth corners;
    # a soul patch under the lower lip, with small clear patches either side of it.
    bb = blend(A_HAIR, skin, 0.3)
    jw2 = L['jw'] * 0.5
    mc = L['mw'] * 0.56
    # (Sam, 4 Nov, round 3: "not anywhere near that thick, nor does it go up to the top of the ears"): it starts
    # halfway down the ear and is a narrow band hugging the jaw, widening only round the chin and mouth
    band = [(-fw * 0.5 - 0.004, 0.5), (-fw * 0.5 - 0.006, 0.62), (-jw2 * 0.98, 0.82), (-0.17, 0.99), (0.0, 1.02),
            (0.17, 0.99), (jw2 * 0.98, 0.82), (fw * 0.5 + 0.006, 0.62), (fw * 0.5 + 0.004, 0.5),
            (fw * 0.5 - 0.025, 0.52), (fw * 0.5 - 0.035, 0.66), (jw2 * 0.86, 0.8), (mc + 0.04, L['lip17'] + 0.01),
            (mc + 0.01, L['lip13']), (mc * 0.55, L['lip17'] + 0.06), (0.03, L['lip17'] + 0.05), (0.0, L['lip17'] + 0.01),
            (-0.03, L['lip17'] + 0.05), (-mc * 0.55, L['lip17'] + 0.06), (-mc - 0.01, L['lip13']),
            (-mc - 0.04, L['lip17'] + 0.01), (-jw2 * 0.86, 0.8), (-fw * 0.5 + 0.035, 0.66), (-fw * 0.5 + 0.025, 0.52)]
    p.poly(curve(f.pts(band), 4), bb, None)
    p.line(open_curve(f.pts(band[:9]), 4), INK, 2.6)        # the jaw's ink line over it
    gc = bb
    must = [(-mc - 0.02, L['lip13']), (-mc, L['lip0'] - 0.004), (-L['nw'] * 0.45, L['lip0'] - 0.03), (0.0, L['lip0'] - 0.032),
            (L['nw'] * 0.45, L['lip0'] - 0.03), (mc, L['lip0'] - 0.004), (mc + 0.02, L['lip13']), (mc - 0.01, L['lip0'] + 0.004),
            (0.0, L['lip0'] - 0.012), (-mc + 0.01, L['lip0'] + 0.004)]
    p.poly(curve(f.pts(must), 3), gc, None)              # the thin moustache, down to the beard at the corners
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', 0.06)), A_IRIS, dk(skin, 0.82), liner=2.6)
    raise_ = {'hopeful': 0.02}.get(mood, 0.0) + sp.get('brow_up', 0.0)
    P4.brows(p, f, L, A_HAIR, 0.042, raise_, sp.get('frown', 0.0))
    if mood == 'sceptic':                              # one brow cocked up (his right, our left)
        bx, by = f(-L['ecx'], L['brow_y'] - 0.05) if 'brow_y' in L else f(-L['ecx'], L['eye_y'] - 0.12)
        p.line(curve([(bx - 18, by + 6), (bx, by - 6), (bx + 16, by + 2)], 3), A_HAIR, 5.0)
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, L['lip13'])
    P4.lips(p, f, L, dict(sp, smile=SMILE.get(mood, 0.6)), A_LIP, (fx, my - 6))
    # the hair: short, near black, slicked straight back off a straight hairline, a little height on top
    # the hair (Sam, 4 Nov: "too big, almost hat-like"): short and close to the skull, combed straight back, only a
    # little lift at the front; sides cropped tight above the ears; a soft M at the hairline (refs 107e061d, 70cfd30c)
    hl = 0.06
    c = fhw * 0.5 * 0.93
    hair = [(-fw * 0.5 + 0.005, 0.34), (-fw * 0.5 - 0.012, 0.2), (-c - 0.022, 0.0), (-c * 0.8, -0.13), (-0.12, -0.22),
            (0.0, -0.235), (0.12, -0.22), (c * 0.8, -0.13), (c + 0.022, 0.0), (fw * 0.5 + 0.012, 0.2),
            (fw * 0.5 - 0.005, 0.34), (fw * 0.5 - 0.035, 0.22), (c - 0.02, hl + 0.03), (0.17, hl - 0.005),
            (0.08, hl + 0.015), (0.0, hl + 0.005), (-0.08, hl + 0.015), (-0.17, hl - 0.005), (-c + 0.02, hl + 0.03),
            (-fw * 0.5 + 0.035, 0.22)]
    p.poly(curve(f.pts(hair), 4), A_HAIR, INK, 2.4)
    for k in range(5):                                 # comb lines straight back
        u = -0.16 + k * 0.08
        p.line(curve(f.pts([(u, hl - 0.015), (u * 1.05, -0.08), (u * 1.08, -0.18)]), 3)[:8], A_HAIR_L, 1.4)
    return fx


# ---------------------------------------------------------------------------------------------- AOC's head
def aoc_head(img, p, sp, t, hx, hy):
    L = P4.layout(P4.target('aoc', sp.get('average', False)))
    f = P4.Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin, mood = O_SKIN, sp.get('mood', 'neutral')
    ears = list(_ears(p, f, L, skin))
    p.poly(curve(f.pts(P4.outline_uv(L, 0.34)), 4), skin, INK, 2.6)
    for sgn, ex, ey in ears:                           # pearl earrings
        p.ell(ex, ey + 22, 6, 6, (246, 242, 232), INK, 1.4)
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', 0.04)), O_IRIS, dk(skin, 0.8), liner=3.2, wide=0.1)
    for sgn in (-1, 1):                                # lashes flicked up at the outer corners
        if sgn < 0 and f.tq > 0.5:
            continue
        cx, cy = f(sgn * (L['ecx'] + L['ew'] * 0.5), L['eye_y'] - L['eh'] * 0.3)
        p.line([(cx, cy), (cx + sgn * 9, cy - 7)], INK, 2.6)
    raise_ = {'hopeful': 0.03}.get(mood, 0.0) + sp.get('brow_up', 0.0)
    P4.brows(p, f, L, O_HAIR, 0.04, raise_, sp.get('frown', 0.0))
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, L['lip13'])
    P4.lips(p, f, L, dict(sp, smile=SMILE.get(mood, 0.6)), O_LIP, (fx, my - 6))
    # the hair: centre parting, falling smooth either side of the face and on past the jaw (the back is in hair_back)
    fw, fhw = L['fw'], L['fhw']
    # (Sam, 4 Nov: "wavier and thicker, a bit straighter"): a full, heavy curtain each side, falling mostly straight
    # with soft waves that grow toward the ends, the inner edge over the cheek
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.7:
            continue
        outer, inner = [], []
        for i in range(15):
            v = -0.1 + i * 0.115                       # from the temple down to below the shoulders
            w = 0.07 * min(1.0, max(0.0, v - 0.15)) * math.sin(v * 6.5)
            outer.append((sgn * (fw * 0.5 + 0.13 + 0.07 * max(0.0, v - 0.2) + w), v))
            inner.append((sgn * (fw * 0.5 - 0.035 + 0.02 * max(0.0, v - 0.6) + w * 0.8), v))
        side = ([(0.0, -0.44), (sgn * fhw * 0.48, -0.39), (sgn * (fhw * 0.5 + 0.12), -0.2)] + outer
                + [(sgn * (fw * 0.5 + 0.06), 1.62)] + inner[::-1][:-2]
                + [(sgn * (fhw * 0.5 - 0.03), 0.12), (sgn * fhw * 0.4, 0.0), (sgn * 0.14, -0.11), (0.0, -0.16)])
        p.poly(curve(f.pts(side), 4), O_HAIR, INK, 2.6)
        for k in range(4):                             # strands following the waves
            pts = [(o[0] * (1 - t_) + q[0] * t_, o[1]) for o, q in zip(outer, inner) for t_ in [0.25 + 0.17 * k]]
            p.line(curve(f.pts(pts[2:13]), 3), O_HAIR_L, 1.4)
        p.line(curve(f.pts([(sgn * 0.03, -0.4), (sgn * 0.22, -0.32), (sgn * (fhw * 0.5 + 0.04), -0.08)]), 3), O_HAIR_L, 1.5)
    return fx


def aoc_hair_back(p, sp, hx, hy, hw, hh):
    p.poly(curve([(hx - hw - 22, hy - 60), (hx - hw - 44, hy + 140), (hx - hw - 40, hy + 330), (hx + hw + 40, hy + 330),
                  (hx + hw + 44, hy + 140), (hx + hw + 22, hy - 60), (hx, hy - hh - 16)], 5), O_HAIR, INK, 2.6)


# ---------------------------------------------------------------------------------------------- torsos and hooks
def elsayed_torso(img, p, sp, t):
    """Open collar (no tie), a white pocket square, a small flag pin on his left lapel."""
    sw = sp.get('shoulders', 150)
    p.poly([(sw * 0.42, 150), (sw * 0.72, 146), (sw * 0.7, 162), (sw * 0.44, 164)], (250, 250, 250), INK, 1.4)
    p.poly([(-sw * 0.5, 70), (-sw * 0.38, 70), (-sw * 0.38, 80), (-sw * 0.5, 80)], (40, 60, 140), INK, 1.0)
    p.line([(-sw * 0.5, 76), (-sw * 0.38, 76)], (200, 40, 50), 1.6)


def aoc_torso(img, p, sp, t):
    """A black top inside the jacket's open neck."""
    p.poly([(-30, -2), (30, -2), (16, 90), (0, 120), (-16, 90)], (14, 14, 16), INK, 1.6)


TC.HEADS.update(elsayed=elsayed_head, aoc=aoc_head)
TC.TORSOS.update(elsayed=elsayed_torso, aoc=aoc_torso)
_hair_back = B.hair_back


def hair_back(p, sp, hx, hy, hw, hh):
    if sp.get('who') == 'aoc':
        return aoc_hair_back(p, sp, hx, hy, hw, hh)
    return _hair_back(p, sp, hx, hy, hw, hh)


B.hair_back = hair_back
V.LONG_HAIR['aoc_long'] = 300          # her long hair in the side and back views

# ---------------------------------------------------------------------------------------------- the people
ELSAYED = dict(who='elsayed', name='Abdul El-Sayed', skin=A_SKIN, hw=66, hh=92, head_dy=10, hair='slick',
               hair_c=A_HAIR, brow_c=A_HAIR, brow_w=4.0, beard='goatee', beard_c=A_HAIR, outfit='suit', jacket=A_SUIT,
               sleeve=A_SUIT, trousers=A_SUIT, shirt=(248, 248, 250), tie=None, shoe=(18, 16, 16), shoulders=150,
               full=True, pose='custom', height=1.78, seed=71)
AOC = dict(who='aoc', name='Alexandria Ocasio-Cortez', skin=O_SKIN, hw=62, hh=88, head_dy=10, hair='aoc_long',
           hair_c=O_HAIR, brow_c=O_HAIR, brow_w=3.6, outfit='suit', jacket=O_JACKET, sleeve=O_JACKET,
           trousers=O_JACKET, shirt=(14, 14, 16), tie=None, shoe=(16, 14, 14), shoulders=128, full=True,
           pose='custom', height=1.65, seed=72)
CAST = {'elsayed': ELSAYED, 'aoc': AOC}


# ---------------------------------------------------------------------------------------------- the sheets
def sheet(out):
    MC.CAST.clear()
    MC.CAST.update(CAST)
    return _sheet(out)


def _sheet(out):
    """Front, side, back of both at true heights, a 1.75 m person; then the faces large, front and side."""
    import landmarks
    import sizes
    B.SS = 1
    W, H = 1900, 1880
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(FONT, 40)
    small = ImageFont.truetype(FONT, 26)
    cam = B.Cam(1.0, 540, 960)
    d.text((40, 24), 'ISLAMOCOMMUNISM: the cast (front, side, back)', font=big, fill=(30, 30, 30))
    names = ('front', 'side', 'back')
    for r, key in enumerate(('elsayed', 'aoc')):
        sp = CAST[key]
        s = 0.5 * sp['height'] / 1.75
        y0 = 100 + r * 900
        d.text((40, y0 - 4), f"{sp['name']} ({sp['height']:.2f} m)", font=big, fill=(30, 30, 30))
        for i, yaw in enumerate((0, 90, 180)):
            MC._tile(img, lambda im, yaw=yaw, sp=sp, s=s: V.person(im, cam, 540, 840 - 928 * s, s, dict(sp), 0.0, yaw),
                     (190, 60, 890, 880), (20 + 440 * i, y0 + 40))
            d.text((370 + 440 * i, y0 + 860), names[i], font=small, fill=(40, 40, 40), anchor='mm')
    lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    landmarks.draw(ld, 540, 840 - 928 * 0.5, 0.5, 1000)
    sizes.scale_ref(ld, 640, 840, 0.5 / V.M_PER_UNIT)
    img.alpha_composite(lay.crop((390, 60, 890, 880)), (1360, 140))
    d.text((1610, 960), '1.75 m person', font=small, fill=(40, 40, 40), anchor='mm')
    img.convert('RGB').save(out, quality=88)
    return out


def faces_sheet(out):
    """The faces large: each mood, plus talking."""
    B.SS = 1
    moods = [('neutral', 'rest'), ('sceptic', 'rest'), ('smile', 'rest'), ('hopeful', 'rest'), ('neutral', 'v:AI')]
    labels = ['rest', 'sceptical', 'big smile', 'hopeful', 'talking']
    W, H = 5 * 400 + 40, 2 * 560 + 40
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    small = ImageFont.truetype(FONT, 26)
    cam = B.Cam(1.0, 540, 960)
    for r, key in enumerate(('elsayed', 'aoc')):
        for i, (mood, mouth) in enumerate(moods):
            sp = dict(CAST[key], mood=mood, mouth=mouth)
            MC._tile(img, lambda im, sp=sp: V.person(im, cam, 540, 900, 1.3, sp, 0.0, 0), (340, 470, 740, 980),
                     (20 + 400 * i, 20 + r * 560))
            d.text((220 + 400 * i, 550 + r * 560), labels[i], font=small, fill=(40, 40, 40), anchor='mm')
    img.convert('RGB').save(out, quality=88)
    return out


def head_png(who, out, average=False):
    B.SS = 1
    im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    V.person(im, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(CAST[who], average=average), 0.0, 0)
    im.crop((240, 380, 840, 1200)).convert('RGB').save(out)
    return out


cast_sheet = sheet

if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    elif sys.argv[1] == 'faces':
        print(faces_sheet(sys.argv[2]))
    elif sys.argv[1] == 'head':
        print(head_png(sys.argv[2], sys.argv[3], '--average' in sys.argv))
