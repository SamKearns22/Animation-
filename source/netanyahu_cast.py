#!/usr/bin/env python3
"""Benjamin Netanyahu, satire caricature in the house style (Newsdesk, Sam 26 Oct), from Sam's four photos
(references/newsdesk/netanyahu-1-front, -2-three-quarter, -3-speaking, -4-podium).

What the photos show, and how he is built (guides/satire.md, 'Likeness method'):
  hair      thick silver-white, combed straight back with a slight side sweep, flat-topped volume; receded at the
            temples (a soft M), full and short over the ears
  face      long, heavy lower half: the eyes sit well above the middle of the head, a long nose, a wide mouth low
            down, soft jowls widening the jaw; two or three faint forehead lines
  eyes      narrow, hooded upper lids, bags beneath, dark brown; thin pale grey brows close above them
  nose      long and broad, a rounded tip, the nostril wings drawn
  mouth     wide and thin-lipped; at rest closed, corners a touch down; deep folds from the nose past the corners
  clothes   dark navy suit, white shirt, a plain blue tie (refs 1, 3) or red (refs 2, 4), the Israeli flag pin on his
            left lapel
Exaggerated (caricature): the hooded eyes and bags, the long nose, the folds and jowls, the swept-back white hair.

Moods (sp['mood']): 'neutral' (ref 1: closed, a faint tight smile), 'fury' (ref 3: brows down, mouth open, shouting),
'stern', 'smug', and the shared moods from shocking_cast. Talking mouths: sp['mouth'] = 'v:SHAPE'.

    python3 source/netanyahu_cast.py sheet OUT.jpg       every view, both ties, the faces, beside a 1.75 m person
    python3 source/compare.py references/newsdesk/netanyahu-1-front.jpg OURS.png OUT.jpg   (the likeness check)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import shocking_cast as SC       # noqa: E402  (shared moods and mouths)
from shocking_cast import brows, eye_state, mouth_or_talk, rest_mouth   # noqa: E402
from traitors_cast import dk, eye, ears   # noqa: E402
from ed import INK, curve        # noqa: E402

N_SKIN = (234, 184, 160)
N_HAIR = (234, 234, 232)
N_HAIR_D = (192, 192, 196)
N_BROW = (150, 140, 134)
N_IRIS = (86, 64, 46)
N_LIP = (190, 120, 108)
BLUE_TIE = (36, 92, 206)
RED_TIE = (206, 32, 44)
NAVY = (28, 34, 58)


def netanyahu_head(img, p, sp, t, hx, hy):
    hw, hh, skin = sp.get('hw', 72), sp.get('hh', 100), sp['skin']
    fx = hx + sp.get('turn', 0.0) * hw * 0.2
    fy = hy + 10 * sp.get('down', 0.0)
    ears(p, hx, hy + 14, hw, skin, rx=13, ry=26)                    # largish ears, set a little low
    outline = curve([(hx - hw, hy - 16), (hx - hw * 0.9, hy - hh * 0.74), (hx - hw * 0.46, hy - hh * 1.02),
                     (hx + hw * 0.46, hy - hh * 1.02), (hx + hw * 0.9, hy - hh * 0.74), (hx + hw, hy - 16),
                     (hx + hw * 1.0, hy + hh * 0.42), (hx + hw * 0.9, hy + hh * 0.84), (hx + hw * 0.52, hy + hh * 1.12),
                     (hx, hy + hh * 1.2), (hx - hw * 0.52, hy + hh * 1.12), (hx - hw * 0.9, hy + hh * 0.84),
                     (hx - hw * 1.0, hy + hh * 0.42)], 4)          # long, rounding to a soft chin
    p.poly(outline, skin, INK, 2.6)
    sd = dk(skin, 0.8)
    mood = sp.get('mood', 'neutral')
    f = max(0.0, min(1.0, sp.get('react', 3) / 6.0)) if mood in ('surprised', 'impressed') else 0.0
    sur = f if mood == 'surprised' else 0.0
    for k in range(3 + (sur > 0.3)):                                # forehead lines: deeper when surprised
        y = hy - hh * 0.5 + 12 * k - 8 * sur
        lift = 5 * sur
        p.line(curve([(fx - 30 + 4 * k, y + 2), (fx, y - 1 - lift), (fx + 30 - 4 * k, y + 2)], 3),
               dk(skin, 0.88 - 0.1 * sur), 1.2 + 0.8 * sur)
    st = eye_state(sp, lid=0.4)                                     # hooded: the lid sits low
    if mood == 'surprised':                                         # pack 5: eyes wide open
        st['lid'] = 0.4 * (1 - f) if 'lid' not in sp else sp['lid']
    elif mood == 'impressed':                                       # sizing up: a touch heavier
        st['lid'] = 0.4 + 0.06 * f if 'lid' not in sp else sp['lid']
    for sgn in (-1, 1):
        ex, ey = fx + sgn * 27, fy - 8
        eye(p, ex, ey, sgn, 13, 6.5, N_IRIS, st, dk(skin, 0.86), liner=2.4)
        p.line(curve([(ex - 15, ey - 6), (ex - 2, ey - 13), (ex + 15, ey - 7)], 3), sd, 1.6)          # the hood's fold
        p.line(curve([(ex - 12, ey + 10), (ex, ey + 15), (ex + 12, ey + 10)], 3), sd, 1.6)          # bags
        p.line(curve([(ex - 8, ey + 18), (ex + 2, ey + 21), (ex + 12, ey + 17)], 3), dk(skin, 0.86), 1.2)
    if mood in ('surprised', 'impressed'):                          # his own brows for these (the library's off)
        for sgn in (-1, 1):
            if mood == 'surprised':                                 # both up, the inner ends highest
                up_in, up_out = 8 + 24 * f, 4 + 12 * f
            elif sgn > 0:                                           # impressed: his left brow (screen right) up
                up_in, up_out = 4 + 12 * f, 6 + 20 * f
            else:                                                   # the other a little down
                up_in, up_out = -1 - 2 * f, 0.0
            y0 = fy - 22
            p.line(curve([(fx + sgn * 9, y0 - up_in), (fx + sgn * 26, y0 - (up_in + up_out) / 2 - 3),
                          (fx + sgn * 42, y0 - up_out + 2)], 3), N_BROW, 5.2)
    else:
        bmood = 'fury' if mood in ('fury', 'stern') else mood
        brows(p, dict(sp, mood=bmood, strength=0.6 if mood == 'stern' else sp.get('strength', 1.0)), fx, fy - 22, 27,
              N_BROW, 5.2, 2, 0, 30)                                # grey, low and nearly straight
    # the long, broad nose: the bridge, a rounded tip, both nostril wings
    p.line([(fx - 3, fy - 4), (fx - 7, fy + 28)], INK, 1.8)
    p.line(curve([(fx - 7, fy + 28), (fx - 6, fy + 38), (fx + 2, fy + 42), (fx + 9, fy + 38)], 3), INK, 2.0)    # rounded tip
    for sgn in (-1, 1):                                                                                     # fleshy wings
        p.line(curve([(fx + sgn * 8, fy + 41), (fx + sgn * 17, fy + 39), (fx + sgn * 19, fy + 32), (fx + sgn * 14, fy + 26)], 3),
               INK, 1.8)
    for sgn in (-1, 1):                                             # the deep folds, nose to past the mouth corners
        p.line(curve([(fx + sgn * 20, fy + 30), (fx + sgn * 36, fy + 56), (fx + sgn * 40, fy + 82)], 3), sd, 2.0)
        p.line(curve([(hx + sgn * hw * 0.92, hy + hh * 0.6), (hx + sgn * hw * 0.78, hy + hh * 0.96)], 3), sd, 1.6)   # jowls
    p.line(curve([(fx - 14, hy + hh * 1.08), (fx, hy + hh * 1.11), (fx + 14, hy + hh * 1.08)], 3), sd, 1.4)    # chin
    my = fy + 60
    if mood == 'neutral' and not SC.talking(sp):                    # ref 1: closed, thin lips, a faint tight smile
        p.poly(curve([(fx - 26, my + 3), (fx, my), (fx + 26, my + 3), (fx, my + 7)], 3), N_LIP, None)     # thin lower lip
        p.line(curve([(fx - 28, my + 4), (fx - 10, my + 1), (fx + 10, my + 1), (fx + 28, my + 4)], 3), INK, 2.2)
        for sgn in (-1, 1):                                                                         # tight corners
            p.line([(fx + sgn * 28, my + 4), (fx + sgn * 32, my + 2)], INK, 1.4)
    elif mood == 'stern' and not SC.talking(sp):                    # pressed flat, corners down
        p.line(curve([(fx - 29, my + 5), (fx - 10, my + 1), (fx + 10, my + 1), (fx + 29, my + 5)], 3), INK, 2.4)
    elif mood == 'fury' and not SC.talking(sp):                     # ref 3: shouting, mouth open and squared
        shape = curve([(fx - 28, my - 2), (fx, my - 6), (fx + 28, my - 2), (fx + 22, my + 20), (fx, my + 26),
                       (fx - 22, my + 20)], 3)
        p.poly(shape, SC.MOUTH_IN, INK, 2.2)
        p.poly(curve([(fx - 22, my - 1), (fx, my - 4), (fx + 22, my - 1), (fx, my + 4)], 3), SC.TEETH, None)
        p.poly(curve([(fx - 16, my + 21), (fx, my + 16), (fx + 16, my + 21), (fx, my + 24)], 3), (200, 210, 214), None)
        p.line(shape, INK, 2.2)
    elif mood == 'surprised' and not SC.talking(sp):                # mouth dropped open, the lower lip down
        o = 3 + 15 * f
        shape = curve([(fx - 20 + 4 * f, my), (fx, my - 2), (fx + 20 - 4 * f, my), (fx + 14, my + o), (fx, my + o + 3),
                       (fx - 14, my + o)], 3)
        p.poly(shape, SC.MOUTH_IN, INK, 2.2)
        p.poly(curve([(fx - 14, my + o), (fx, my + o + 3), (fx + 14, my + o), (fx, my + o + 7)], 3), N_LIP, INK, 1.4)
    elif mood == 'impressed' and not SC.talking(sp):                # lips pressed together, corners a little down
        dn = 2 + 5 * f
        p.poly(curve([(fx - 24, my + 3), (fx, my + 1), (fx + 24, my + 3), (fx, my + 8 + 2 * f)], 3), N_LIP, None)
        p.line(curve([(fx - 27, my + 2 + dn), (fx - 12, my + 1), (fx + 12, my + 1), (fx + 27, my + 2 + dn)], 3), INK, 2.4)
        p.line(curve([(fx - 10, my + 14 + 2 * f), (fx, my + 12 + 2 * f), (fx + 10, my + 14 + 2 * f)], 3), sd, 1.4)   # chin pushed up
    else:
        mouth_or_talk(p, sp, fx, my, N_LIP, width=28, lips=True)
    # hair: thick, white, combed back with a slight sweep; receded at the temples, full and short over the ears
    top = hy - hh - 18
    hair = [(hx - hw - 6, hy - 6), (hx - hw - 10, hy - 50), (hx - hw * 0.98, top + 46), (hx - hw * 0.7, top + 12),
            (hx - hw * 0.2, top - 2), (hx + hw * 0.36, top), (hx + hw * 0.82, top + 16), (hx + hw + 8, top + 52),
            (hx + hw + 8, hy - 50), (hx + hw + 5, hy - 6), (hx + hw - 6, hy - 38), (hx + hw * 0.84, hy - hh * 0.7),
            (hx + hw * 0.6, hy - hh * 0.74), (hx + hw * 0.3, hy - hh * 0.86), (hx - hw * 0.1, hy - hh * 0.9),
            (hx - hw * 0.44, hy - hh * 0.84), (hx - hw * 0.66, hy - hh * 0.72), (hx - hw * 0.86, hy - hh * 0.7),
            (hx - hw + 6, hy - 38)]
    p.poly(curve(hair, 4), N_HAIR, INK, 2.6)
    for k in range(6):                                              # strands combed back, a slight sweep to his left
        x0 = hx - hw * 0.62 + k * hw * 0.25
        p.line(curve([(x0, hy - hh * 0.84), (x0 + 10, top + 30), (x0 + 22, top + 12)], 3)[:9], N_HAIR_D, 1.5)
    p.line(curve([(hx - hw * 0.5, hy - hh * 0.86), (hx - hw * 0.46, top + 24), (hx - hw * 0.4, top + 6)], 3)[:8],
           N_HAIR_D, 1.8)                                           # the side parting, on his right
    for sgn in (-1, 1):                                             # short at the sides, over the ears
        p.line(curve([(hx + sgn * (hw + 2), hy - 46), (hx + sgn * (hw + 6), hy - 24), (hx + sgn * (hw + 2), hy - 8)], 3),
               N_HAIR_D, 1.4)
    return fx


def netanyahu_torso(img, p, sp, t):
    tie = sp.get('tie', BLUE_TIE)
    p.poly([(-13, 16), (13, 16), (16, 200), (0, 224), (-16, 200)], tie, INK, 2.0)     # a plain silk tie
    p.poly([(-13, -2), (13, -2), (9, 18), (-9, 18)], tie, INK, 2.0)
    p.line([(4, 22), (8, 190)], dk(tie, 0.82), 1.2)                                  # a soft fold down it
    SC.lapels(p, sp)
    x, y = 58, 96                                                    # the Israeli flag pin, his left lapel
    p.poly([(x - 11, y - 8), (x + 11, y - 8), (x + 11, y + 8), (x - 11, y + 8)], (248, 248, 250), INK, 1.2)
    for yy in (y - 5, y + 5):
        p.line([(x - 10, yy), (x + 10, yy)], (30, 70, 190), 1.8)
    p.poly([(x, y - 3.4), (x + 3, y + 1.7), (x - 3, y + 1.7)], None, (30, 70, 190), 1.0)
    p.poly([(x, y + 3.4), (x + 3, y - 1.7), (x - 3, y - 1.7)], None, (30, 70, 190), 1.0)


# --------------------------------------------------------------------------------------------- the hooks
_head, _torso = B.head, B.torso


def head(img, p, sp, t, hx, hy):
    if sp.get('who') == 'netanyahu':
        return netanyahu_head(img, p, sp, t, hx, hy)
    return _head(img, p, sp, t, hx, hy)


def torso(img, p, sp, t):
    _torso(img, p, sp, t)
    if sp.get('who') == 'netanyahu':
        netanyahu_torso(img, p, sp, t)


B.head, B.torso = head, torso

# hair/brow keys: what views.head_view reads for the other views (three-quarter, side, back)
NETANYAHU = dict(who='netanyahu', name='Netanyahu', skin=N_SKIN, hw=72, hh=100, head_dy=10, jaw='round',
                 hair='side', hair_c=N_HAIR, brow_c=N_BROW, brow_w=4.2, nose='long', outfit='suit', jacket=NAVY,
                 shirt=(248, 248, 250), tie=BLUE_TIE, shoulders=160, trousers=NAVY, full=True, pose='custom',
                 height=1.80)                                       # height: an estimate
NETANYAHU_RED = dict(NETANYAHU, tie=RED_TIE)
CAST = {'netanyahu': NETANYAHU}


def sheet(out):
    """Every view (blue tie), the red-tie outfit, his faces large (rest, stern, shouting, talking, smug), and a
    plain 1.75 m person for scale."""
    import views as V
    import landmarks
    import sizes
    B.SS = 1
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

    d.text((40, 24), 'NEWSDESK: Netanyahu (satire caricature, from Sam\'s four photos)', font=big, fill=(30, 30, 30))
    names = ('front', 'three-quarter', 'side', '3/4 back', 'back', 'red tie')
    for i, (yaw, sp) in enumerate(((0, NETANYAHU), (45, NETANYAHU), (90, NETANYAHU), (135, NETANYAHU),
                                   (180, NETANYAHU), (0, NETANYAHU_RED))):
        tile(lambda im, yaw=yaw, sp=sp: V.person(im, cam, 540, 300, s, dict(sp), 0.0, yaw), (330, 100, 750, 900),
             (20 + 360 * i, 90))
        d.text((230 + 360 * i, 890), names[i], font=small, fill=(40, 40, 40), anchor='mm')
    lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    landmarks.draw(ld, 540, 300, s, 1000)
    sizes.scale_ref(ld, 640, 300 + 928 * s, s / V.M_PER_UNIT)
    img.alpha_composite(lay.crop((450, 100, 870, 900)), (2180, 90))
    d.text((2380, 890), '1.75 m person', font=small, fill=(40, 40, 40), anchor='mm')
    faces = (('neutral', 'rest', 'at rest (ref 1)'), ('stern', 'rest', 'stern'), ('fury', 'rest', 'shouting (ref 3)'),
             ('neutral', 'v:AI', 'talking'), ('smug', 'rest', 'smug'))
    for i, (mood, mouth, label) in enumerate(faces):
        sp = dict(NETANYAHU if i % 2 == 0 else NETANYAHU_RED, mood=mood, mouth=mouth)
        tile(lambda im, sp=sp: V.person(im, cam, 540, 840, 1.45, sp, 0.0, 0), (320, 290, 760, 1130), (40 + 500 * i, 960))
        d.text((260 + 500 * i, 1850), label, font=small, fill=(40, 40, 40), anchor='mm')
    img.convert('RGB').save(out, quality=90)
    return out


def face_png(out, sp=None):
    """His head and shoulders alone, straight on, for compare.py beside the front photo."""
    import views as V
    B.SS = 1
    im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
    V.person(im, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(sp or NETANYAHU), 0.0, 0)
    im.crop((240, 380, 840, 1200)).save(out)
    return out


def reaction_sheet(out, tie=None):
    """Netan-Yahoo! (answer 12, pack 5): the surprised and impressed faces at strengths 1-6, each row beside its photo,
    for Sam to pick a number (default 3)."""
    import views as V
    from PIL import ImageFont
    B.SS = 1
    W, H = 2340, 1060
    sh = Image.new('RGB', (W, H), (232, 228, 222))
    d = ImageDraw.Draw(sh)
    big = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 34)
    sm = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 28)
    base = dict(NETANYAHU_RED if tie is None else dict(NETANYAHU, tie=tie))
    rows = [('surprised', 'netanyahu-surprised.jpg', dict(look=-0.5, gaze_dy=-2.0)),
            ('impressed', 'netanyahu-impressed.jpg', dict(look=-0.7))]
    for r, (mood, ref, extra) in enumerate(rows):
        y = 60 + r * 500
        d.text((20, y - 50), f'{mood} (strength 1 = slight .. 6 = huge); eyes towards Maul (screen left)', font=big,
               fill=(30, 30, 30))
        try:
            ph = Image.open(os.path.join(HERE, '..', 'references', 'netan-yahoo', ref)).convert('RGB')
            ph.thumbnail((330, 440))
            sh.paste(ph, (20, y))
        except OSError:
            d.text((20, y + 200), 'photo missing', font=sm, fill=(160, 30, 30))
        for k in range(1, 7):
            im = Image.new('RGBA', (1080, 1920), (246, 244, 238, 255))
            V.person(im, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(base, mood=mood, react=k, **extra), 0.0, 0)
            tile = im.crop((300, 420, 780, 1060)).convert('RGB').resize((300, 400), Image.LANCZOS)
            x = 370 + (k - 1) * 325
            sh.paste(tile, (x, y))
            d.text((x + 130, y + 404), str(k), font=big, fill=(30, 30, 30))
    sh.save(out, quality=88)
    return out


cast_sheet = sheet


def LINE_SUBJECTS():
    import views as V
    return [('netanyahu', lambda im: V.person(im, B.Cam(1.0, 540, 960), 540, 420, 1.45, dict(NETANYAHU), 0.0, 0))]


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    elif sys.argv[1] == 'face':
        print(face_png(sys.argv[2]))
