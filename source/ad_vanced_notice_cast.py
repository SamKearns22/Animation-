#!/usr/bin/env python3
"""MAP  Ad-Vanced Notice (7 Nov): the cast. Vance is a measured likeness head (likeness.py card on the three official
portraits, references/ad-vanced-notice/) on the patriots4 face layout, drawn the Islamocommunism way.

    VANCE  JD Vance (card, 7 Nov): brows low and heavy (97th centile), long chin (95th), wide nose (93rd), brows rising
           to the outside, narrow hooded eyes, wide mouth, thin upper lip. Medium-dark brown hair swept up and over from
           a parting on his right (our left), receding at the temples into an M, short at the sides, a little grey
           over the ears. A short, full, brown beard with a ginger cast, joined to the moustache, up the cheeks to a
           line from mid-ear to past the mouth corners; blue eyes. Navy suit, white shirt, red tie, flag pin (Sam,
           7 Nov: the same in every shot). 1.88 m.
    MAN    The gas-station driver (invented, from the brief): 17 stone (108 kg), 1.80 m, a belly over his belt; a blue
           and red checked shirt, blue jeans, brown boots; a black goatee, balding pate with dark sides.

    python3 source/ad_vanced_notice_cast.py sheet OUT.jpg     front, side, back of both, a 1.75 m person
    python3 source/ad_vanced_notice_cast.py faces OUT.jpg     the faces large in every mood
    python3 source/ad_vanced_notice_cast.py head WHO OUT.png  one head straight on (for likeness.py check)

Map: colours 35 | measures 50 | Vance head 70 | man head 140 | torsos 175 | people 215 | sheets 235
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import midterminal_cast as MC   # noqa: E402  (installs the hooks chain and the sheet helpers)
from midterminal_cast import B, TC, P4, V, dk, blend, FONT  # noqa: E402
from ed import INK, curve, oval, open_curve  # noqa: E402

# ---------------------------------------------------------------------------------------------- colours
V_SKIN = (232, 178, 152)          # fair, pink (card: 232, 172, 148)
V_HAIR = (82, 60, 44)             # medium-dark brown
V_HAIR_L = (120, 92, 70)
V_BEARD = (136, 100, 72)          # brown with a ginger cast, a touch of grey
V_IRIS = (92, 140, 186)           # blue
V_LIP = (204, 134, 120)
NAVY = (30, 38, 62)
RED_TIE = (150, 26, 38)
M_SKIN = (226, 170, 140)
M_HAIR = (26, 22, 22)
M_SHIRT = (60, 86, 150)           # the check's base blue
M_CHECK = (178, 44, 48)
M_JEANS = (58, 84, 128)
M_BOOT = (96, 64, 40)

# ---------------------------------------------------------------------------------------------- measures (7 Nov)
_card = json.load(open(os.path.join(HERE, '..', 'references', 'ad-vanced-notice', 'vance-card.json')))
_VM, _VA = _card['measures'], _card['average']
P4.MEASURED['vance'] = {k: P4.AVG[k] + _VM[k] - _VA[k] for k in P4.AVG}   # differences from likeness.py's average
P4.PUSH['vance'] = 1.6
P4.TUNE['vance'] = dict(brow_high=1.3, chin_long=2.0, nose_wide=3.2, brow_slope=1.6, eyes_apart=5.0, mouth_wide=3.0, eye_tilt=5.5, eye_open=0.5)   # 7 Nov, likeness check rounds
P4.MEASURED['man'] = dict(P4.AVG, face_wide=P4.AVG['face_wide'] + 0.06, jaw_wide=P4.AVG['jaw_wide'] + 0.08,
                          eye_size=P4.AVG['eye_size'] - 0.02, brow_high=P4.AVG['brow_high'] - 0.06)
P4.PUSH['man'] = 1.0
P4.TUNE['man'] = {}

SMILE = {'neutral': 0.6, 'sincere': 0.35, 'smile': 1.4, 'proud': 1.2, 'angry': -0.6, 'glare': -0.4}


def _ears(p, f, L, skin):
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.5:
            continue
        ex, ey = f(sgn * (L['fw'] * 0.5 + 0.01), 0.42)
        p.poly(oval(ex, ey, 11, 24, 20), skin, INK, 2.4)
        p.line([(ex - sgn * 2, ey - 10), (ex + sgn * 3, ey), (ex - sgn * 1, ey + 10)], dk(skin, 0.7), 1.4)


# ---------------------------------------------------------------------------------------------- Vance's head
def vance_head(img, p, sp, t, hx, hy):
    L = P4.layout(P4.target('vance', sp.get('average', False)))
    f = P4.Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin, mood = V_SKIN, sp.get('mood', 'neutral')
    _ears(p, f, L, skin)
    out = curve(f.pts(P4.outline_uv(L, 0.4, crown=-0.42)), 4)
    p.poly(out, skin, INK, 2.6)
    fw, jw, ny, l0, l13, l17 = L['fw'], L['jw'], L['nose_y'], L['lip0'], L['lip13'], L['lip17']
    mw = L['mw']
    # the beard: one shape, short and full, from mid-ear down the jaw and round a long chin, up the cheeks to a line
    # sloping from the sideburn to just outside the mouth corners, the moustache joined to it; the lips clear
    beard = [(-fw * 0.5 - 0.004, 0.46), (-fw * 0.5 - 0.006, 0.6), (-jw * 0.5 - 0.004, 0.8), (-0.2, 1.0), (0.0, 1.05),
             (0.2, 1.0), (jw * 0.5 + 0.004, 0.8), (fw * 0.5 + 0.006, 0.6), (fw * 0.5 + 0.004, 0.46),
             (fw * 0.5 - 0.035, 0.5), (fw * 0.4, 0.66), (mw * 0.62, l13 - 0.01),               # cheek line, low
             (mw * 0.55, l0 - 0.005), (L['nw'] * 0.5, ny + 0.03), (0.0, ny + 0.035),           # moustache, thin
             (-L['nw'] * 0.5, ny + 0.03), (-mw * 0.55, l0 - 0.005), (-mw * 0.62, l13 - 0.01),
             (-fw * 0.4, 0.66), (-fw * 0.5 + 0.035, 0.5)]
    p.poly(curve(f.pts(beard), 4), V_BEARD, None)
    for u, v in ((-0.22, 0.86), (-0.12, 0.95), (0.0, 0.98), (0.12, 0.95), (0.22, 0.86), (-0.3, 0.72), (0.3, 0.72)):
        a, b = f(u, v), f(u * 1.02, v + 0.035)
        p.line([a, b], dk(V_BEARD, 0.78), 1.6)                     # a few short strokes for texture
    p.line(open_curve(f.pts(beard[:9]), 4), INK, 2.6)              # the jaw's ink line round the beard
    # the lips sit in a clear patch inside the beard (a soft gap round the lower lip, as in all three portraits)
    p.poly(curve(f.pts([(-mw * 0.4, l13), (0.0, l13 - 0.008), (mw * 0.4, l13), (mw * 0.24, l17 + 0.01),
                        (0.0, l17 + 0.018), (-mw * 0.24, l17 + 0.01)]), 3), blend(V_BEARD, skin, 0.55), None)
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', 0.13)), V_IRIS, dk(skin, 0.82), liner=2.6)
    # the hooded outer corners (card: eyes drooping at the outside): a fold of lid over each eye's outer top corner,
    # its edge sloping down and out, so the opening droops at the outside as in all three portraits
    if not sp.get('blink'):
        w, h = L['ew'] * P4.H / 2, L['eh'] * P4.H / 1.8
        for sgn in (-1, 1):
            ex, ey = f(sgn * L['ecx'], L['eye_y'])
            ww = w * (1 - 0.3 * f.tq if sgn < 0 else 1.0)
            hood = [(ex + sgn * ww * 0.05, ey - h * 1.25), (ex + sgn * ww * 1.2, ey - h * 1.0),
                    (ex + sgn * ww * 1.12, ey + h * 0.15), (ex + sgn * ww * 0.6, ey - h * 0.55),
                    (ex + sgn * ww * 0.05, ey - h * 0.92)]
            p.poly(hood, skin, None)
            p.line(curve([(ex + sgn * ww * 0.05, ey - h * 0.92), (ex + sgn * ww * 0.6, ey - h * 0.55),
                          (ex + sgn * ww * 1.12, ey + h * 0.15)], 3), INK, 2.4)
    raise_ = {'sincere': 0.012, 'teasing': 0.03}.get(mood, 0.0) + sp.get('brow_up', 0.0)
    frown = {'angry': 0.03}.get(mood, 0.0) + sp.get('frown', 0.0)
    P4.brows(p, f, L, dk(V_HAIR, 0.85), 0.05, raise_, frown)
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, l13)
    P4.lips(p, f, L, dict(sp, smile=SMILE.get(mood, 0.6)), V_LIP, (fx, my - 6))
    # the hair: swept up and over to our right from a parting on our left, volume on top, receding temples (an M)
    fhw = L['fhw']
    c = fhw * 0.5
    hl = -0.05                                                  # a high hairline: a broad forehead below it
    hair = [(-fw * 0.5 + 0.004, 0.36), (-fw * 0.5 - 0.02, 0.18), (-c - 0.04, -0.04), (-c * 0.85, -0.24),
            (-0.2, -0.36), (-0.04, -0.42), (0.12, -0.43), (0.26, -0.38), (c * 0.9, -0.28), (c + 0.06, -0.1),
            (fw * 0.5 + 0.022, 0.16), (fw * 0.5 - 0.004, 0.36), (fw * 0.5 - 0.03, 0.22),       # sideburn, cropped
            (fw * 0.5 - 0.05, 0.06), (c * 0.86, -0.1), (c * 0.62, -0.14),                     # the temple, receding (M)
            (0.18, hl - 0.02), (0.06, hl + 0.0), (-0.06, hl - 0.01), (-0.16, hl - 0.03),      # the forelock, swept
            (-c * 0.62, -0.13), (-c * 0.86, -0.09), (-fw * 0.5 + 0.05, 0.07), (-fw * 0.5 + 0.03, 0.22)]
    p.poly(curve(f.pts([(-c * 0.8, 0.16), (-c * 0.76, -0.18), (c * 0.76, -0.18), (c * 0.8, 0.16)]), 3), skin, None)
    p.poly(curve(f.pts(hair), 4), V_HAIR, INK, 2.4)
    for a, b in (((-0.2, -0.06), (0.06, -0.38)), ((-0.06, -0.08), (0.2, -0.36)), ((0.08, -0.08), (0.3, -0.28)),
                 ((-0.3, 0.0), (-0.16, -0.3))):
        p.line(curve(f.pts([a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 0.03), b]), 3), V_HAIR_L, 1.6)
    p.line(curve(f.pts([(-c * 0.62, hl + 0.04), (-c * 0.64, -0.2), (-c * 0.54, -0.32)]), 3), dk(V_HAIR, 0.7), 1.8)  # parting
    for sgn in (-1, 1):                                                                # a little grey over the ears
        if sgn < 0 and f.tq > 0.5:
            continue
        p.line(curve(f.pts([(sgn * (fw * 0.5 + 0.004), 0.24), (sgn * (fw * 0.5 + 0.012), 0.32)]), 2),
               (150, 142, 136), 2.2)
    return fx


# ---------------------------------------------------------------------------------------------- the man's head
def man_head(img, p, sp, t, hx, hy):
    L = P4.layout(P4.target('man'))
    f = P4.Face(hx, hy, sp.get('three', 0.0), sp.get('turn', 0.0), sp.get('down', 0.0))
    skin, mood = M_SKIN, sp.get('mood', 'glare')
    _ears(p, f, L, skin)
    fw, fhw, ny, l0, l13, l17 = L['fw'], L['fhw'], L['nose_y'], L['lip0'], L['lip13'], L['lip17']
    # balding: dark hair only round the sides and back, the pate bare and shiny (drawn under the skin outline)
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.5:
            continue
        side = [(sgn * (fw * 0.5 - 0.01), 0.4), (sgn * (fw * 0.5 + 0.03), 0.22), (sgn * (fw * 0.5 + 0.02), 0.1),
                (sgn * (fw * 0.5 - 0.03), 0.12), (sgn * (fw * 0.5 - 0.035), 0.38)]
        p.poly(curve(f.pts(side), 3), M_HAIR, INK, 2.2)
    out = curve(f.pts(P4.outline_uv(L, 0.46, crown=-0.2)), 4)
    p.poly(out, skin, INK, 2.6)
    for sgn in (-1, 1):                                         # the side hair over the outline at the temples
        if sgn < 0 and f.tq > 0.5:
            continue
        side = [(sgn * (fw * 0.5 + 0.008), 0.4), (sgn * (fw * 0.5 + 0.02), 0.22), (sgn * (fw * 0.5 + 0.004), 0.12),
                (sgn * (fw * 0.5 - 0.035), 0.16), (sgn * (fw * 0.5 - 0.035), 0.38)]
        p.poly(curve(f.pts(side), 3), M_HAIR, INK, 2.0)
    p.line(curve(f.pts([(-0.12, -0.14), (-0.04, -0.17), (0.04, -0.16)]), 3), (246, 214, 196), 3.0)   # pate shine
    # the black goatee: moustache joined round the mouth to a short block on the chin
    mw = L['mw']
    goatee = [(-mw * 0.62, l13 + 0.02), (-mw * 0.58, l0 - 0.01), (-L['nw'] * 0.45, ny + 0.014), (0.0, ny + 0.02),
              (L['nw'] * 0.45, ny + 0.014), (mw * 0.58, l0 - 0.01), (mw * 0.56, l13 + 0.02), (mw * 0.34, l17 + 0.07),
              (0.08, 0.98), (0.0, 0.99), (-0.08, 0.98), (-mw * 0.34, l17 + 0.07)]
    p.poly(curve(f.pts(goatee), 4), M_HAIR, None)
    P4.eyes(p, f, L, dict(sp, lid4=sp.get('lid4', 0.22) + 0.04 * (sp.get('anger') or 0), gaze_dy=sp.get('gaze_dy', -0.5)), (82, 60, 42),
            dk(skin, 0.82), liner=2.6)
    ang = sp.get('anger')                       # the strength scale, 1 (slight) to 6 (huge): brows down, mouth down
    frown = (0.012 * ang if ang else {'angry': 0.05, 'glare': 0.045}.get(mood, 0.0)) + sp.get('frown', 0.0)
    P4.brows(p, f, L, M_HAIR, 0.05, sp.get('brow_up', 0.0), frown)
    P4.nose(p, f, L, skin)
    fx, my = f(0.0, l13)
    smile = -0.2 * ang if ang else SMILE.get(mood, -0.4)
    P4.lips(p, f, L, dict(sp, smile=smile), (176, 110, 100), (fx, my - 6))
    return fx


# ---------------------------------------------------------------------------------------------- torsos
def vance_torso(img, p, sp, t):
    """The flag pin on his left lapel (our right)."""
    sw = sp.get('shoulders', 158)
    x, y = sw * 0.46, 92
    p.poly([(x - 9, y - 6), (x + 9, y - 6), (x + 9, y + 6), (x - 9, y + 6)], (246, 246, 246), INK, 1.2)
    p.poly([(x - 9, y - 6), (x - 1, y - 6), (x - 1, y), (x - 9, y)], (40, 60, 140), None)
    for k in (-3, 1, 5):
        p.line([(x - 1, y + k), (x + 9, y + k)], (196, 36, 48), 1.4)


def man_torso(img, p, sp, t):
    """The checked shirt over a belly: red check lines on blue, a button placket, a collar, a belt under the belly."""
    sw = sp.get('shoulders', 186)
    bottom = int(sp.get('bottom', 560))
    belly = [(-sw * 0.92, 250), (-sw * 1.06, 380), (-sw * 0.98, bottom - 20), (sw * 0.98, bottom - 20),
             (sw * 1.06, 380), (sw * 0.92, 250)]
    belly = curve(belly, 4)
    p.poly(belly, M_SHIRT, INK, 2.6)
    body = [(-40, -4), (-sw * 0.8, 12), (-sw, 50), (-sw - 6, 200)] + belly + [(sw + 6, 200), (sw, 50), (sw * 0.8, 12), (40, -4)]
    check_lines(p, body, -sw * 1.1, sw * 1.1, 0, bottom)
    p.line([(0, 0), (0, bottom - 22)], dk(M_SHIRT, 0.7), 2.2)
    for y in range(60, bottom - 40, 70):
        p.ell(0, y, 5, 5, (236, 232, 222), INK, 1.0)
    for sgn in (-1, 1):
        p.poly([(sgn * 36, -6), (sgn * 64, 16), (sgn * 22, 40), (0, 10)], M_SHIRT, INK, 2.0)
    p.poly([(-sw * 0.98, bottom - 24), (sw * 0.98, bottom - 24), (sw * 0.96, bottom), (-sw * 0.96, bottom)],
           (60, 40, 28), INK, 2.0)                                                     # the belt
    p.poly([(-16, bottom - 22), (16, bottom - 22), (16, bottom - 2), (-16, bottom - 2)], (196, 176, 120), INK, 1.4)


_torso_view = V.torso_view


def _inside(poly, x, y):
    """Point in polygon (ray casting)."""
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
            c = not c
    return c


def check_lines(p, poly, x0, x1, y0, y1, step=34, col=M_CHECK, inset=4):
    """The shirt's check, cut to the shirt's outline (never past its edge)."""
    def runs(a, b):
        pts = [(a[0] + (b[0] - a[0]) * k / 60, a[1] + (b[1] - a[1]) * k / 60) for k in range(61)]
        seg = []
        for q in pts:
            ok = all(_inside(poly, q[0] + dx, q[1] + dy) for dx, dy in ((inset, 0), (-inset, 0), (0, inset), (0, -inset)))
            if ok:
                seg.append(q)
            elif seg:
                if len(seg) > 1:
                    p.line(seg, col, 2.0)
                seg = []
        if len(seg) > 1:
            p.line(seg, col, 2.0)
    for x in range(int(x0) // step * step, int(x1), step):
        runs((x, y0), (x, y1))
    for y in range(int(y0) // step * step, int(y1), step):
        runs((x0, y), (x1, y))


def torso_view(img, p, sp, view, seated=False):
    """The man's side and back: a belly pushing his shirt out in front (side), and the check all round, cut to the
    shirt's outline."""
    _torso_view(img, p, sp, view, seated)
    if sp.get('who') != 'man':
        return
    sw = sp.get('shoulders', 186)
    bottom = int(min(sp.get('bottom', V.JACKET), 470) if seated else sp.get('bottom', V.JACKET))
    if view == 'side':
        d = 0.6 * sw
        body = curve([(-34, -8), (-d * 0.92, 22), (-d * 1.02, 130), (-d * 0.96, 320), (-d * 0.92, bottom),
                      (d * 1.24, bottom), (d * 1.42, 400), (d * 1.32, 300), (d * 0.9, 150), (d * 0.86, 30),
                      (30, -6)], 3)
        p.poly(body, M_SHIRT, INK, 2.6)
        check_lines(p, body, -d * 1.1, d * 1.5, 0, bottom)
        p.poly([(-d * 0.92, bottom - 20), (d * 1.24, bottom - 20), (d * 1.22, bottom), (-d * 0.92, bottom)],
               (60, 40, 28), INK, 2.0)
    elif view == 'back':
        body = [(-40, -4), (-sw * 0.8, 12), (-sw, 50), (-(sw + 6), 200), (-sw * B.HEM, bottom),
                (sw * B.HEM, bottom), (sw + 6, 200), (sw, 50), (sw * 0.8, 12), (40, -4)]
        check_lines(p, body, -sw - 10, sw + 10, 0, bottom)


V.torso_view = torso_view
TC.HEADS.update(vance=vance_head, man=man_head)
TC.TORSOS.update(vance=vance_torso, man=man_torso)

# ---------------------------------------------------------------------------------------------- the people
VANCE = dict(who='vance', name='JD Vance', skin=V_SKIN, hw=72, hh=94, head_dy=10, hair='slick', hair_c=V_HAIR,
             brow_c=V_HAIR, brow_w=4.4, beard='trim', beard_c=V_BEARD, outfit='suit', jacket=NAVY, sleeve=NAVY,
             trousers=NAVY, shirt=(246, 246, 248), tie=RED_TIE, shoe=(20, 16, 14), shoulders=158, full=True,
             pose='custom', height=1.88, seed=81)
MAN = dict(who='man', name='The driver', skin=M_SKIN, hw=80, hh=92, head_dy=12, hair='bald', hair_c=M_HAIR,
           brow_c=M_HAIR, brow_w=4.6, beard='goatee', beard_c=M_HAIR, outfit='jumper', jacket=M_SHIRT, sleeve=M_SHIRT,
           trousers=M_JEANS, shirt=M_SHIRT, tie=None, shoe=M_BOOT, shoulders=186, leg_k=1.35, full=True, pose='custom',
           height=1.80, seed=82)
CAST = {'vance': VANCE, 'man': MAN}


# ---------------------------------------------------------------------------------------------- the sheets
def sheet(out):
    import landmarks
    import sizes
    MC.CAST.clear()
    MC.CAST.update(CAST)
    B.SS = 1
    W, H = 1900, 1880
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(FONT, 40)
    small = ImageFont.truetype(FONT, 26)
    cam = B.Cam(1.0, 540, 960)
    d.text((40, 24), 'AD-VANCED NOTICE: the cast (front, side, back)', font=big, fill=(30, 30, 30))
    for r, key in enumerate(('vance', 'man')):
        sp = CAST[key]
        s = 0.5 * sp['height'] / 1.75
        y0 = 100 + r * 900
        d.text((40, y0 - 4), f"{sp['name']} ({sp['height']:.2f} m)", font=big, fill=(30, 30, 30))
        for i, yaw in enumerate((0, 90, 180)):
            MC._tile(img, lambda im, yaw=yaw, sp=sp, s=s: V.person(im, cam, 540, 840 - 928 * s, s, dict(sp), 0.0, yaw),
                     (190, 60, 890, 880), (20 + 440 * i, y0 + 40))
            d.text((370 + 440 * i, y0 + 860), ('front', 'side', 'back')[i], font=small, fill=(40, 40, 40), anchor='mm')
    lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    landmarks.draw(ld, 540, 840 - 928 * 0.5, 0.5, 1000)
    sizes.scale_ref(ld, 640, 840, 0.5 / V.M_PER_UNIT)
    img.alpha_composite(lay.crop((390, 60, 890, 880)), (1360, 140))
    d.text((1610, 960), '1.75 m person', font=small, fill=(40, 40, 40), anchor='mm')
    img.convert('RGB').save(out, quality=88)
    return out


def faces_sheet(out):
    """The faces large, each mood; the references beside Vance's (rule 76)."""
    B.SS = 1
    rows = {'vance': [('neutral', 'rest', 'rest'), ('sincere', 'rest', 'sincere'), ('smile', 'rest', 'big smile'),
                      ('teasing', 'rest', 'teasing'), ('neutral', 'v:AI', 'talking')],
            'man': [(k, 'rest', f'anger {k}') for k in range(1, 7)]}
    W, H = 6 * 400 + 40, 3 * 560 + 40
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    small = ImageFont.truetype(FONT, 26)
    cam = B.Cam(1.0, 540, 960)
    for r, key in enumerate(('vance', 'man')):
        for i, (mood, mouth, label) in enumerate(rows[key]):
            sp = dict(CAST[key], mouth=mouth)
            sp.update(anger=mood, gaze_dy=-0.8) if isinstance(mood, int) else sp.update(mood=mood)
            MC._tile(img, lambda im, sp=sp: V.person(im, cam, 540, 900, 1.3, sp, 0.0, 0), (340, 470, 740, 980),
                     (20 + 400 * i, 20 + r * 560))
            d.text((220 + 400 * i, 550 + r * 560), label, font=small, fill=(40, 40, 40), anchor='mm')
    ref = os.path.join(HERE, '..', 'references', 'ad-vanced-notice')
    for i, n in enumerate(('vance-front-2023', 'vance-front-2025', 'vance-front-2026', 'vance-caricature-2022')):
        im = Image.open(os.path.join(ref, n + '.jpg')).convert('RGBA')
        im.thumbnail((380, 500))
        img.alpha_composite(im, (20 + 400 * i + (380 - im.width) // 2, 20 + 2 * 560 + (500 - im.height) // 2))
    d.text((W - 220, 2 * 560 + 260), 'references', font=small, fill=(40, 40, 40), anchor='mm')
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
