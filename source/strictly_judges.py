#!/usr/bin/env python3
"""Strictly Crabs Dancing: the judges (Satire style), after the crab dance. Widescreen 1280 x 720 like the rest of the
film. Refs: refs/strictly-crabs/judges/ (judges-ref-01..12). Notes: notes/strictly-crabs.md.

Shot J1: Craig alone, flamboyant and droll: "I don't really understand the joke, darling, but I'm having an amazing time."
Shot J2: all four at the table (left to right Craig, Motsi, Shirley, Anton); the crabs spin past in front and every
judge's eyes follow them; once they have passed, Anton shoots up with his paddle like a formal, excited puppy: "290!"

People are the satire package's (views.person); only their outfits are drawn here (Craig's flower-pattern jacket,
Motsi's ruffle, Shirley's silver swirls, the bow ties, the bun), with the table, the backdrop and the paddle.

    python3 source/strictly_judges.py cast OUT.jpg     the cast sheet (approve before anything moves)
    python3 source/strictly_judges.py stills OUT_DIR T [T ...]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import mossad                    # noqa: E402,F401  (brows, mouths, hair; patched into burnham on import)
import mouths                    # noqa: E402
import views as V                # noqa: E402
import poker_mon_cast as PC      # noqa: E402  (bow_tie; installs circle hands and mouths)
from ed import INK, curve, open_curve, oval   # noqa: E402
from satire_style import rough   # noqa: E402

import figure as F               # noqa: E402
import limbs                     # noqa: E402

B.W, B.H = 1280, 720             # the film is widescreen (the crab dance is 16:9)
F.guard(B)                       # the house style, as in the template: every arm measured against the rig,
limbs.install(B)                 # and the smooth arms and legs (Sam, 21 Oct: the boxy arms came back here)
FPS = 12

# ------------------------------------------------------------------------------------------------ the people
SHIRT = (244, 244, 240)
TUX = (24, 24, 30)
CRAIG_RED = (176, 28, 30)
GOLD = (226, 178, 52)
# Craig (refs 01, 02): long face, high forehead, dark hair slicked straight back, arched brows, a knowing half-lid;
# red jacket with a black flower pattern, white dress shirt with black studs, black bow tie, white pocket square.
CRAIG = dict(name='CRAIG', skin=(232, 188, 162), hw=64, hh=98, jaw='long', hair='slick', hair_c=(54, 40, 34),
             brow_c=(54, 40, 34), brow_w=3.6, brow_raise=4, lid=2, outfit='suit', jacket=CRAIG_RED, shirt=SHIRT,
             trousers=TUX, shoulders=148, bow=(16, 16, 20), studs=True, flowers=True, pocket=True, mouth='line', seed=31)
# Motsi (refs 10, 11): hair pulled up into a bun, big gold drop earrings, yellow one-shoulder ruffled dress, bare arms.
MOTSI = dict(name='MOTSI', skin=(110, 66, 46), hw=60, hh=88, jaw='soft', hair='slick', hair_c=(28, 22, 20),
             brow_c=(28, 22, 20), brow_w=2.6, lashes=True, outfit='dress', dress=(250, 204, 46), jacket=(250, 204, 46),
             trousers=(232, 186, 34), lip_c=(150, 66, 70), shoulders=122, bun=True, gold_drops=True,
             neckline='one', ruffle=(250, 204, 46), mouth='smile', seed=32)
# Shirley (refs 07, 08): dark wavy bob, big earrings, black off-shoulder dress with silver swirls along the neckline.
SHIRLEY = dict(name='SHIRLEY', skin=(234, 196, 172), hw=62, hh=86, jaw='soft', hair='bob', hair_c=(58, 36, 28),
               brow_c=(48, 32, 26), brow_w=2.8, lashes=True, outfit='dress', dress=(26, 24, 30), jacket=(26, 24, 30),
               trousers=(26, 24, 30), lip_c=(176, 66, 76), shoulders=124, waves=True, neckline='off', swirls=True,
               pearl_drops=True, mouth='line', seed=33)
# Anton (refs 04, 06): short grey-brown hair, a big warm smile; black dinner jacket, white shirt, black bow tie.
ANTON = dict(name='ANTON', skin=(232, 186, 160), hw=66, hh=90, jaw='square', hair='crop', hair_c=(132, 116, 102),
             brow_c=(112, 96, 84), brow_w=3.2, outfit='suit', jacket=TUX, shirt=SHIRT, trousers=TUX, shoulders=150,
             bow=(16, 16, 20), studs=True, mouth='grin', seed=34)
CAST = {'CRAIG': CRAIG, 'MOTSI': MOTSI, 'SHIRLEY': SHIRLEY, 'ANTON': ANTON}
ORDER = ('CRAIG', 'MOTSI', 'SHIRLEY', 'ANTON')        # left to right at the table (refs 05, 07, 12)
HEIGHTS = {'CRAIG': 1.80, 'MOTSI': 1.75, 'SHIRLEY': 1.60, 'ANTON': 1.80}


def flower(p, x, y, r):
    """One black daisy rosette of Craig's jacket: a ring of petals round a dot."""
    for k in range(8):
        a = k * math.pi / 4
        p.ell(x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a), r * 0.36, r * 0.17, (40, 8, 10), None, 0, rot=a)
    p.ell(x, y, r * 0.2, r * 0.2, (40, 8, 10), None, 0)


def flower_grid(p, x0, y0, x1, y1, inside, r=13, seed=0):
    rng = np.random.default_rng(seed)
    for gy in np.arange(y0, y1, r * 2.3):
        for gx in np.arange(x0 + (int(gy / (r * 2.3)) % 2) * r * 1.15, x1, r * 2.3):
            if inside(gx, gy):
                flower(p, gx + rng.uniform(-1.5, 1.5), gy + rng.uniform(-1.5, 1.5), r)


def body_dress(p, view, sp):
    """Clothing over the torso (front view, the torso's own frame): necklines, the jacket pattern, studs, pocket."""
    sw = sp.get('shoulders', 150)
    skin = sp['skin']
    if sp.get('flowers'):                        # the pattern on the jacket fronts, kept off the shirt and lapels
        def inside(x, y):
            return 30 + y * 0.25 < abs(x) < sw * (0.98 - 0.12 * y / 500) and 50 < y < 490
        flower_grid(p, -sw, 50, sw, 510, inside, 10, sp.get('seed', 0))
    if sp.get('pocket'):
        x0, x1, y = sw * 0.5, sw * 0.8, 120             # his left breast pocket (screen right, ref 01): on the
        p.poly(rough([(x0, y), (x0 + 12, y - 16), (x0 + 22, y - 6), (x0 + 34, y - 22), (x0 + 46, y - 4),
                      (x1, y)], 1.0, 3), (248, 248, 246), INK, 1.8)       # chest, outside the lapel, above a welt
        p.line([(x0 - 4, y), (x1 + 4, y + 2)], INK, 2.2)
    if sp.get('studs'):
        for k in range(3):
            p.ell(0, 70 + 44 * k, 4, 4, (20, 20, 24), None, 0)
    neck = sp.get('neckline')
    if neck == 'off':                             # off the shoulders: skin above a straight neckline across the chest
        p.poly(rough([(-sw + 6, 52), (-sw * 0.5, 30), (-30, 10), (30, 10), (sw * 0.5, 30), (sw - 6, 52),
                      (sw - 4, 112), (0, 128), (-sw + 4, 112)], 1.5, 5), skin, INK, 2.4)
    elif neck == 'one':                          # one shoulder: bare on her left (screen right), strap on her right
        p.poly(rough([(-30, 10), (30, 10), (sw * 0.5, 30), (sw - 6, 52), (sw - 4, 120), (sw * 0.2, 150),
                      (-sw * 0.3, 70)], 1.5, 6), skin, INK, 2.4)
    if sp.get('swirls'):                         # silver crystal swirls along the neckline (ref 08)
        for sg in (-1, 1):
            c = open_curve([(sg * 10, 132), (sg * 40, 112), (sg * 62, 128), (sg * 54, 150), (sg * 34, 140),
                            (sg * 70, 104), (sg * 104, 118), (sg * 110, 98)], 4)
            p.line(c, (214, 214, 224), 9)
            for x, y in c[::3]:
                p.ell(x, y, 3.2, 3.2, (250, 250, 255), None, 0)


def ruffle(p, j2, sp):
    """Motsi's big ruffle over her right shoulder (screen left) and down the bodice (ref 10)."""
    sw = sp.get('shoulders', 122)
    c = sp['ruffle']
    dk = B.dk(c, 0.82)
    for k, (x, y, rx, ry) in enumerate([(-sw + 10, 40, 58, 44), (-sw + 46, 2, 46, 40), (-sw * 0.38, 70, 54, 46),
                                       (-sw * 0.7, 108, 48, 40), (-sw * 0.1, 128, 44, 34)]):
        p.poly(curve(rough(oval(x, y, rx, ry, 14), 6, 40 + k), 3), c, INK, 2.4)
        p.line(open_curve([(x - rx * 0.5, y + ry * 0.2), (x, y - ry * 0.25), (x + rx * 0.5, y + ry * 0.15)], 3), dk, 2.4)


def dress_up(sp):
    """Drawn after the arms (front view): bow tie, ruffle."""
    def draw(p, j2):
        if sp.get('flowers'):                     # the pattern down the sleeves too
            for sd in 'LR':
                pts = [j2['sh' + sd], j2['el' + sd], j2['wr' + sd]]
                for a, b in zip(pts, pts[1:]):
                    n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 22))
                    for i in range(n):
                        u = (i + 0.5) / n
                        x, y = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
                        flower(p, x + (8 if i % 2 else -8), y, 9)
        if sp.get('ruffle'):
            ruffle(p, j2, sp)
        if sp.get('bow'):
            PC.bow_tie(p, 0, 4, sp['bow'])
    return draw


def updo(p, sp, hx, hy, hw, hh):
    """Motsi's hair (judges refs 10, 11 and motsi-hair-refs: sleek, swept up from a side parting into a big bun on
    top; a full sweep across the forehead from her right). One shape, one outline; a few sweep lines inside."""
    c = sp['hair_c']
    hi = B.lt(c, 1.9) if hasattr(B, 'lt') else (70, 58, 54)
    bun = curve(rough(oval(hx + 8, hy - hh - 40, 56, 40, 18), 5, 7), 3)
    p.poly(bun, c, INK, 2.6)
    p.line(open_curve([(hx - 30, hy - hh - 46), (hx + 8, hy - hh - 66), (hx + 46, hy - hh - 44)], 3), hi, 2.4)
    p.line(open_curve([(hx - 20, hy - hh - 24), (hx + 14, hy - hh - 40), (hx + 40, hy - hh - 22)], 3), hi, 2.4)
    cap = [(hx - hw - 6, hy - hh * 0.05), (hx - hw - 10, hy - hh * 0.55), (hx - hw * 0.6, hy - hh - 14),
           (hx, hy - hh - 26), (hx + hw * 0.7, hy - hh - 10), (hx + hw + 10, hy - hh * 0.5), (hx + hw + 6, hy - hh * 0.05),
           (hx + hw - 6, hy - hh * 0.4), (hx + hw * 0.45, hy - hh * 0.62),          # the hairline, swept from her right
           (hx - hw * 0.1, hy - hh * 0.58), (hx - hw * 0.55, hy - hh * 0.44), (hx - hw + 4, hy - hh * 0.2)]
    p.poly(curve(cap, 4), c, INK, 2.6)
    for k in range(3):
        p.line(open_curve([(hx - hw * (0.7 - 0.1 * k), hy - hh * (0.42 + 0.14 * k)),
                           (hx - hw * 0.1, hy - hh * (0.78 + 0.1 * k)), (hx + hw * (0.55 - 0.1 * k), hy - hh * (0.86 + 0.06 * k))], 3),
               hi, 2.0)


def wave_bob(p, sp, hx, hy, hw, hh):
    """Shirley's bob (refs 07, 08): full dark waves at each side down to the jaw, framing the face."""
    c = sp['hair_c']
    hi = B.lt(c, 1.9) if hasattr(B, 'lt') else (110, 80, 66)
    for sg in (-1, 1):
        pts = [(hx + sg * (hw - 10), hy - hh * 0.75), (hx + sg * (hw + 20), hy - hh * 0.6)]
        for k in range(4):
            pts.append((hx + sg * (hw + 22 + 9 * (k % 2)), hy - hh * 0.3 + k * hh * 0.25))
        pts += [(hx + sg * (hw + 6), hy + hh * 0.62), (hx + sg * (hw - 8), hy + hh * 0.5), (hx + sg * (hw - 4), hy - hh * 0.1)]
        p.poly(curve(pts, 4), c, INK, 2.6)
        p.line(open_curve([(hx + sg * (hw + 4), hy - hh * 0.4), (hx + sg * (hw + 16), hy), (hx + sg * (hw + 6), hy + hh * 0.35)], 3),
               hi, 2.0)


def head_dress(p, view, sp, hx, hy):
    """Worn on the head: Motsi's updo, Shirley's waves, the earrings."""
    hw, hh = sp.get('hw', 64), sp.get('hh', 88)
    if sp.get('bun'):
        updo(p, sp, hx, hy, hw, hh)
    if sp.get('waves'):
        wave_bob(p, sp, hx, hy, hw, hh)
    for sg in (-1, 1):
        ex, ey = hx + sg * (hw + 6), hy + hh * 0.08     # on the lobes, clear of the cheeks
        if sp.get('gold_drops'):
            p.ell(ex, ey + 22, 11, 20, GOLD, INK, 2.0)
            p.ell(ex, ey + 22, 4, 8, B.dk(GOLD, 0.75), None, 0)
        if sp.get('pearl_drops'):
            p.ell(ex, ey + 18, 11, 13, (238, 238, 244), INK, 2.0)


def joints(sp, pose='table', **kw):
    """Seated at the judges' desk: forearms on the desk top, hands together in front (the table hides the rest)."""
    j = V.standing(sp)
    sw = sp.get('shoulders', 150)
    if pose == 'table':
        for side, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, side, (sg * kw.get('hands', 70), TABLE_Y - 18, 160.0), 'out')
    elif pose == 'sides':
        pass
    j['props'] = [dress_up(sp)]
    j['body_props'] = [body_dress]
    j['head_props'] = [head_dress]
    for side in 'LR':
        j.setdefault('hand', {})[side] = j['hand'].get(side, 'fist')
    return j


def person(img, cam, x, y, s, sp, t=0.0, j=None, yaw=0):
    sp = dict(sp, full=True, pose='custom')
    if sp.get('outfit') == 'dress':
        sp['sleeve'] = sp['skin'] if sp.get('neckline') == 'one' else sp['dress']
    return V.person(img, cam, x, y, s, sp, t, yaw, j or joints(sp))


# ------------------------------------------------------------------------------------------------ the set
TABLE_Y = 300.0          # the desk top, in person units below the neck (chest height, as on the show)
S_WIDE = 0.62            # people's scale in the wide shot
NECK_WIDE = 300          # neck height in the wide shot (frame px)
XS = {'CRAIG': 230, 'MOTSI': 500, 'SHIRLEY': 780, 'ANTON': 1050}
BLUE = (22, 44, 128)
BLUE_L = (64, 110, 214)
BLUE_LL = (150, 190, 246)
PINK = (232, 128, 206)
PURPLE = (148, 82, 206)
SILVER = (214, 214, 230)


def backdrop(img, cam):
    """Deep blue with pale beams fanning down from the lighting rig, and sparkles (refs 05, 07, 10: flat, no glow)."""
    p = B.Pen(img, cam)
    p.poly([(-200, -200), (1480, -200), (1480, 900), (-200, 900)], BLUE, None, 0)
    rng = np.random.default_rng(5)
    for k in range(9):
        x = -60 + k * 175
        w = 50 + 20 * (k % 3)
        p.poly(rough([(x - 14, -40), (x + 14, -40), (x + 120 + w, 760), (x + 120 - w, 760)], 4, k), BLUE_L, None, 0)
        p.poly(rough([(x - 5, -40), (x + 5, -40), (x + 120 + w * 0.35, 760), (x + 120 - w * 0.35, 760)], 3, k + 20),
               (96, 142, 230), None, 0)
    for _ in range(140):
        x, y = rng.uniform(-100, 1380), rng.uniform(-60, 700)
        r = rng.uniform(1.5, 4.2)
        p.ell(x, y, r, r, BLUE_LL if rng.random() < 0.7 else (250, 250, 255), None, 0)


def table(img, cam):
    """The judges' desk (refs 05, 07, 12): a long glittery front in pink, purple and silver bands, a silver lip on top,
    the round glitter-ball emblem in the middle."""
    p = B.Pen(img, cam)
    top = NECK_WIDE + TABLE_Y * S_WIDE
    x0, x1 = -600, 1880
    p.poly(rough([(x0, top - 14), (x1, top - 14), (x1, top + 10), (x0, top + 10)], 2, 1), SILVER, INK, 3)   # desk top
    bands = [(PURPLE, 34), (SILVER, 10), (PINK, 40), (SILVER, 10), (PURPLE, 44), (PINK, 60), (PURPLE, 400)]
    y = top + 10
    for k, (c, h) in enumerate(bands):
        p.poly(rough([(x0, y), (x1, y), (x1, y + h), (x0, y + h)], 1.5, k + 3), c, INK, 2.4)
        y += h
    rng = np.random.default_rng(9)                 # glitter: flat specks, never a glow
    for _ in range(700):
        gx, gy = rng.uniform(x0, x1), rng.uniform(top - 12, 760)
        p.ell(gx, gy, 1.6, 1.6, (255, 240, 255) if rng.random() < 0.6 else (110, 60, 160), None, 0)
    cx, cy = 640, top + 150                         # the emblem
    p.ell(cx, cy, 120, 120, PINK, INK, 3)
    p.ell(cx, cy, 98, 98, PURPLE, INK, 2.6)
    p.ell(cx, cy, 74, 74, SILVER, INK, 2.6)
    for a in range(0, 360, 30):                     # the glitter ball's facets
        r = math.radians(a)
        p.line([(cx + 74 * math.cos(r), cy + 74 * math.sin(r) * 0.3), (cx - 74 * math.cos(r), cy - 74 * math.sin(r) * 0.3)],
               (170, 170, 190), 1.6)
    for yy in (-50, -20, 10, 40):
        hw = math.sqrt(max(0, 74 ** 2 - yy ** 2))
        p.line([(cx - hw, cy + yy), (cx + hw, cy + yy)], (170, 170, 190), 1.6)


def paddle(p, x, y, k, text='290', a=0.0):
    """A scoring paddle (ref 12): a white disc with big black numbers on a short white handle. (x, y) = the grip."""
    ca, sa = math.cos(a), math.sin(a)
    R = lambda dx, dy: (x + dx * ca - dy * sa, y + dx * sa + dy * ca)
    p.poly([R(-9 * k, 0), R(9 * k, 0), R(9 * k, -70 * k), R(-9 * k, -70 * k)], (246, 246, 242), INK, 2.4)
    cx, cy = R(0, -150 * k)
    p.ell(cx, cy, 86 * k, 86 * k, (248, 248, 244), INK, 3)
    return (cx, cy, 86 * k)


def paddle_text(img, cam, disc, text='290'):
    cx, cy, r = disc
    B.text(img, cam, cx, cy, text, int(r * (1.0 if len(text) < 3 else 0.78)), INK, anchor='mm')


# ------------------------------------------------------------------------------------------------ frames
def wide(t=0.0, poses=None):
    cam = B.Cam(1.0, 640, 360)
    img = B.canvas()
    backdrop(img, cam)
    for who in ORDER:
        person(img, cam, XS[who], NECK_WIDE, S_WIDE, CAST[who], t, (poses or {}).get(who))
    table(img, cam)
    return img


def craig_close(t=0.0, j=None):
    cam = B.Cam(1.7, XS['CRAIG'] + 10, NECK_WIDE + 20)
    img = B.canvas()
    backdrop(img, cam)
    person(img, cam, XS['CRAIG'], NECK_WIDE, S_WIDE, CAST['CRAIG'], t, j)
    table(img, cam)
    return img


def cast_sheet(out):
    """The four standing (body landmarks across, a 1 m ruler and the paddle beside Anton), then the two shots."""
    import landmarks
    B.SS = 1
    sheet = Image.new('RGB', (1280, 720 * 3), (230, 226, 220))
    img = Image.new('RGBA', (1280, 720), (230, 226, 220, 255))
    cam = B.Cam(1.0, 640, 360)
    s = 0.62
    for i, who in enumerate(ORDER):
        sp = dict(CAST[who], full=True, pose='custom')
        person(img, cam, 150 + 270 * i, 90, s, sp, 0.0, joints(sp, 'sides'))
    p = B.Pen(img, cam)
    disc = paddle(p, 1170, 470, s * 0.25 / 0.25)
    paddle_text(img, cam, disc)
    d = ImageDraw.Draw(img)
    landmarks.draw(d, 640, 90, s, 1240)
    sheet.paste(img.convert('RGB'), (0, 0))
    sheet.paste(wide().convert('RGB'), (0, 720))
    sheet.paste(craig_close().convert('RGB'), (0, 1440))
    sheet.save(out, quality=90)


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        cast_sheet(a[1])
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            wide(float(x)).convert('RGB').save(os.path.join(a[1], f'j{x}.jpg'), quality=88)


if __name__ == '__main__':
    main()
