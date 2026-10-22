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
from PIL import Image, ImageDraw, ImageFont

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

TALL = os.environ.get('STRICTLY_WIDE') != '1'    # TikTok (Sam, 22 Oct): a full 9:16 picture, no blurred bands
B.W, B.H = (1080, 1920) if TALL else (1280, 720)
FIT = 1080 / 1280 if TALL else 1.0     # tall cameras zoom out so each shot keeps its widescreen width
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
XS = {'CRAIG': 200, 'MOTSI': 490, 'SHIRLEY': 790, 'ANTON': 1080}
BLUE = (22, 44, 128)
BLUE_L = (64, 110, 214)
BLUE_LL = (150, 190, 246)
PINK = (232, 128, 206)
PURPLE = (148, 82, 206)
SILVER = (214, 214, 230)


def backdrop(img, cam):
    """Deep blue with pale beams fanning down from the lighting rig, and sparkles (refs 05, 07, 10: flat, no glow)."""
    p = B.Pen(img, cam)
    p.poly([(-900, -3200), (2200, -3200), (2200, 1200), (-900, 1200)], BLUE, None, 0)
    rng = np.random.default_rng(5)
    for k in range(15):
        x = -620 + k * 175
        w = 50 + 20 * (k % 3)
        y0 = -1500 if TALL else -300                 # tall frame: the same beams, carried on up to the rig
        x0 = x + (y0 + 300) * 150 / 1200
        p.poly(rough([(x0 - 14, y0), (x0 + 14, y0), (x + 150 + w, 900), (x + 150 - w, 900)], 4, k), BLUE_L, None, 0)
        p.poly(rough([(x0 - 5, y0), (x0 + 5, y0), (x + 150 + w * 0.35, 900), (x + 150 - w * 0.35, 900)], 3, k + 20),
               (96, 142, 230), None, 0)
    for _ in range(520 if TALL else 260):
        x, y = rng.uniform(-700, 2000), rng.uniform(-1500 if TALL else -260, 760)
        r = rng.uniform(1.5, 4.2)
        p.ell(x, y, r, r, BLUE_LL if rng.random() < 0.7 else (250, 250, 255), None, 0)


def table(img, cam):
    """The judges' desk (refs 05, 07, 12): a long glittery front in pink, purple and silver bands, a silver lip on top,
    the round glitter-ball emblem in the middle."""
    p = B.Pen(img, cam)
    top = NECK_WIDE + TABLE_Y * S_WIDE
    x0, x1 = -600, 1880
    p.poly(rough([(x0, top - 14), (x1, top - 14), (x1, top + 10), (x0, top + 10)], 2, 1), SILVER, INK, 3)   # desk top
    bands = [(PURPLE, 34), (SILVER, 10), (PINK, 40), (SILVER, 10), (PURPLE, 44), (PINK, 60)]
    y = top + 10
    for k, (c, h) in enumerate(bands):
        p.poly(rough([(x0, y), (x1, y), (x1, y + h), (x0, y + h)], 1.5, k + 3), c, INK, 2.4)
        y += h
    rng = np.random.default_rng(9)                 # glitter: flat specks, never a glow
    for _ in range(700):
        gx, gy = rng.uniform(x0, x1), rng.uniform(top - 12, top + 206)
        p.ell(gx, gy, 1.6, 1.6, (255, 240, 255) if rng.random() < 0.6 else (110, 60, 160), None, 0)
    floor(p, y)
    cx, cy = 640, top + 104                         # the emblem
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


def floor(p, y0):
    """The dance floor in front of the desk: dark and polished, the desk's bands mirrored in it, flat."""
    p.poly([(-600, y0), (1880, y0), (1880, 3200), (-600, 3200)], (34, 20, 58), INK, 2.4)
    y = y0 + 3
    for k, (c, h) in enumerate([((92, 52, 128), 16), ((110, 60, 110), 12), ((70, 40, 100), 22)]):
        p.poly(rough([(-600, y), (1880, y), (1880, y + h), (-600, y + h)], 1.0, 60 + k), c, None, 0)
        y += h + 6
    for k in range(6):                              # a few long highlights in the polish
        x = 40 + k * 230
        p.poly(rough([(x, y0 + 70), (x + 140, y0 + 70), (x + 160, y0 + 76), (x + 20, y0 + 76)], 1.0, 70 + k),
               (60, 44, 96), None, 0)


DESK_BOTTOM = NECK_WIDE + TABLE_Y * S_WIDE + 10 + 198


def paddle(p, x, y, k, text='290', a=0.0, flat=1.0):
    """A scoring paddle (ref 12): a white disc with big black numbers on a short white handle. (x, y) = the grip."""
    ca, sa = math.cos(a), math.sin(a)
    R = lambda dx, dy: (x + dx * ca - dy * sa, y + dx * sa + dy * ca)
    # flat: 1 held up facing us; lying on the desk it is seen edge-on (squashed), the numbers face down
    p.poly([R(-9 * k, 0), R(9 * k, 0), R(9 * k, -70 * k * flat), R(-9 * k, -70 * k * flat)], (246, 246, 242), INK, 2.4)
    cx, cy = R(0, -150 * k * flat)
    p.ell(cx, cy, 86 * k, 86 * k * flat, (248, 248, 244), INK, 3)
    return (cx, cy, 86 * k)


def paddle_text(img, cam, disc, text='290'):
    """The paddle's numbers, centred on the disc (cam may be a person's own frame, B.Local)."""
    cx, cy, r = disc
    f = ImageFont.truetype(B.ANTON, max(4, int(cam.S(r * 0.95))))
    l, t, rr, b = f.getbbox(text)
    lay = Image.new('RGBA', (rr - l + 4, b - t + 4), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((2 - l, 2 - t), text, font=f, fill=INK)
    X, Y = cam.P(cx, cy)
    img.alpha_composite(lay, (int(X - lay.width / 2), int(Y - lay.height / 2)))


# ------------------------------------------------------------------------------------------------ the shots
# Times are seconds from the start of the judges' section (it follows the dance at 33.9 s of the film).
import mossad_audio as MA        # noqa: E402
import filmkit                   # noqa: E402
import json                      # noqa: E402

J1_DUR, J2_DUR = 6.2, 9.1
DUR = J1_DUR + J2_DUR
TITLES = 116 / 24                 # the logo moves until 4.85 s (Sam, 21 Oct), so the cut is on frame 116 at 24 fps
BEAT = 60 / 136
CUT_FROM, CUT_BEATS = 0.302 + 16 * BEAT, 8   # Sam, 22 Oct: the dance's second shot (beats 16-24) is removed
DANCE_A = 177 / 24                # dance frames kept before the cut (0 .. beat 16), then from beat 24 to the end
DANCE_B0 = 0.302 + 24 * BEAT
DANCE_LEN = DANCE_A + round((24.9 - DANCE_B0) * 24) / 24
FILM_AT = TITLES + DANCE_LEN      # where the judges start in the whole film
SHOTS = [('J1', 0.0, J1_DUR), ('J2', J1_DUR, DUR)]
LINES = [   # start: where the recording's first sample sits (Craig's begins with 0.9 s of silence, cut in silence)
    dict(n=1, who='CRAIG', text="I don't really understand the joke, darling, but I'm having an amazing time.",
         audio='strictly-craig', start=-0.91),
    dict(n=2, who='ANTON', text='Two hundred and ninety!', audio='strictly-anton', start=J1_DUR + 5.2),
]
for ln in LINES:
    ln['_voice'] = MA.line(ln['audio'])
    ln['_stretches'] = MA.pauses(ln['_voice'], 0.12)
    ln['end'] = ln['start'] + len(ln['_voice']) / MA.SR
TRACK = {w: [(a + ln['start'], b + ln['start'], sh) for ln in LINES if ln['who'] == w
             for a, b, sh in mouths.track(ln['text'], ln['_stretches'])] for w in CAST}
SPEAKING = [(ln['who'], ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches']]
REST_MOUTH = {'CRAIG': 'line', 'MOTSI': 'smile', 'SHIRLEY': 'smile', 'ANTON': 'grin'}
_keep = [(J1_DUR + 5.75, J1_DUR + 8.35)]                # no blink on Anton's spring and his "290"
BLINKS = {w: [b for b in F.blinks(40 + k, 0.4, DUR, talking=(w == 'CRAIG'))
              if not any(a - 0.2 <= b <= z for a, z in _keep)] for k, w in enumerate(ORDER)}

# Shot J2's camera (flat): the four at the desk, the dance floor in front for the crabs.
Z2, CX2, CY2 = 0.7, 640, 420
PASS_DIR = os.path.join(HERE, 'data', 'strictly-crabs', 'pass')   # the crabs alone, see-through (render.mjs pass)
PASS_T0 = 26.77                   # dance seconds at the start of J2 (the pair enters from the left about 0.4 s in)
CRAB_FLOOR = 622                  # the crabs' middles land here on J2's frame (px): on the dance floor strip
_PASS = None


def pass_info():
    global _PASS
    if _PASS is None:
        with open(os.path.join(PASS_DIR, 'pass.json')) as f:
            _PASS = json.load(f)
    return _PASS


def crab_frame(s2):
    """The crab layer's frame index for J2 time s2 (seconds into the shot)."""
    d = pass_info()
    return min(len(d['frames']) - 1, max(0, round((PASS_T0 + s2 - d['T0']) * d['fps'])))


def crabs_x(s2):
    """Where the dancing pair is across J2's frame (frame px, the middle of the two), or None when off screen,
    with which side they are off ('L' before, 'R' after)."""
    d = pass_info()
    xs = [x * 1280 / d['w'] for x, _ in d['frames'][crab_frame(s2)]['scr']]
    m = sum(xs) / len(xs)
    if max(xs) < -60:
        return None, 'L'
    if min(xs) > 1340:
        return None, 'R'
    return m, None


def crab_drop():
    """How far the crab layer moves down so the pair's middle sits on CRAB_FLOOR (from the render's own camera)."""
    d = pass_info()
    ys = [y * 1280 / d['w'] for f in d['frames'] for _, y in f['scr']]
    return CRAB_FLOOR - sum(ys) / len(ys)


def to_world2(fx):
    return (fx - 640) / Z2 + CX2


ANTON_UP = J1_DUR + 5.95          # he springs up once the crabs have gone


def anton_rise(t):
    """How far Anton has risen (person units): a small dip, a fast spring up with an overshoot, two puppyish bounces
    on his toes, then still and proud."""
    u = t - ANTON_UP
    if u < -0.15:
        return 0.0
    if u < 0:
        return -14 * math.sin(math.pi * (u + 0.15) / 0.15 / 2)          # the dip before the spring
    if u < 0.2:
        e = u / 0.2
        return -14 + 224 * (1 - (1 - e) ** 3)                           # up, fast out of the dip
    if u < 0.4:
        return 210 - 20 * math.sin(math.pi * (u - 0.2) / 0.4)
    if u < 1.1:
        return 190 + 16 * abs(math.sin(math.pi * (u - 0.4) / 0.35)) * (1 - (u - 0.4) / 0.9)   # the bounces
    return 190.0 + 4 * filmkit.shifts(t, seed=77, amount=1.0)


CRAIG_ARMS = filmkit.Beats([   # J1: hands {side: target} in his torso's units (x right, y down from the neck, z to us)
    # the one-hand flourishes use his screen-left hand, the side with room (Motsi sits on his other side)
    (0.0, 'rest', {'L': (-70, 282, 160), 'R': (70, 282, 160)}),
    (0.35, 'set-up', {'L': (-120, 210, 180), 'R': (70, 282, 160)}),
    (0.95, 'flourish up', {'L': (-215, -60, 120), 'R': (70, 282, 160)}, 'fast'),
    (1.65, 'rolls out', {'L': (-290, 30, 100), 'R': (70, 282, 160)}),
    (2.2, 'darling', {'L': (-150, 120, 240), 'R': (70, 282, 160)}, 'fast'),
    (2.95, 'hold', {'L': (-160, 132, 230), 'R': (80, 280, 160)}, 'slow'),
    (3.35, 'set-up', {'L': (-150, 200, 180), 'R': (150, 200, 180)}),
    (4.1, 'amazing', {'L': (-290, -130, 60), 'R': (205, -190, 70)}, 'fast'),
    (4.95, 'hold', {'L': (-300, -160, 60), 'R': (210, -215, 70)}, 'slow'),
    (5.75, 'settle', {'L': (-70, 282, 160), 'R': (70, 282, 160)}, 'slow'),
])
CRAIG_HEAD = filmkit.Beats([(0.0, 'rest', 0.0), (0.95, 'tilt in', 0.07, 'slow'), (1.65, 'tilt', 0.04),
                            (2.2, 'darling', -0.07, 'fast'), (3.35, 'level', 0.0, 'slow'),
                            (4.1, 'back', -0.05, 'fast'), (5.75, 'rest', 0.0, 'slow')])
ANTON_ARM = filmkit.Beats([    # J2 (seconds of the section): his paddle hand, from the desk straight up overhead
    (ANTON_UP - 0.1, 'grip', (70, 282, 160)),
    (ANTON_UP + 0.18, 'thrust', (92, -200, 60), 'fast'),
    (DUR, 'hold', (94, -196, 60), 'slow'),
])


def eyes_at(who, t):
    """Where each judge looks in J2: the crabs (followed smoothly while they pass), ahead of them before they come,
    where they went after; then (from Anton's spring) at Anton. Anton himself looks straight out once he is up."""
    s2 = t - J1_DUR
    if who == 'ANTON' and t >= ANTON_UP:
        return 0.0
    if who != 'ANTON' and t >= ANTON_UP + 0.05:
        return F.look_at(XS[who], XS['ANTON'])
    m, side = crabs_x(s2)
    wx = to_world2(m) if m is not None else (-400 if side == 'L' else 1700)
    return F.look_at(XS[who], wx, 500)


def state(who, t):
    """Everything about one person at time t: arms, mouth, blink, eyes, head."""
    sp = dict(CAST[who])
    j = joints(sp)
    rise = 0.0
    if who == 'CRAIG' and t < J1_DUR:
        arms = CRAIG_ARMS.at(t)
        for sd in 'LR':
            V.arm_to(j, sd, arms[sd], 'out')
        sp['tilt'] = CRAIG_HEAD.at(t)
        sp['brow_raise'] = 4 + (5 if 2.1 <= t < 3.3 else 0)
        sp['look'] = -0.12 if 0.9 <= t < 2.0 else 0.0
    else:
        sp['tilt'] = filmkit.shifts(t, seed=ORDER.index(who) + 3, amount=0.035)
        sp['look'] = eyes_at(who, t) if t >= J1_DUR else (F.look_at(XS[who], XS['CRAIG']) if who == 'MOTSI' else 0.0)
    if who == 'ANTON':
        rise = anton_rise(t)
        if t >= ANTON_UP - 0.1:
            V.arm_to(j, 'R', ANTON_ARM.at(t), 'out')
            V.arm_to(j, 'L', (-24, 330 - rise * 0.0, 80), 'out')      # formal: hand on his jacket front
            j['grip'] = {'R'}
            sp['brows'] = 'joy'
        j['props'].append(held_paddle(t))
    shape = mouths.at(TRACK[who], t)
    sp['mouth'] = REST_MOUTH[who] if shape == 'rest' else 'v:' + shape
    sp['blink'] = F.blinking(t, BLINKS[who])
    sp['breath'] = F.breath(t, 4.0, 1.5, 0.2 * ORDER.index(who))
    return sp, j, rise


def held_paddle(t):
    """Anton's paddle: lying on the desk under his hand (numbers down), then up in his fist facing us. The hand holds
    it all along, so it only moves when his hand does."""
    def draw(p, j2):
        x, y = j2['wrR']
        flat = 1.0 if t >= ANTON_UP + 0.12 else (0.2 if t < ANTON_UP else 0.2 + 0.8 * (t - ANTON_UP) / 0.12)
        disc = paddle(p, x, y + 8, 1.0, flat=flat)
        draw.disc = disc if flat > 0.9 else None
    return draw


def scene_people(img, cam, t):
    for who in ORDER:
        sp, j, rise = state(who, t)
        person(img, cam, XS[who], NECK_WIDE - rise * S_WIDE, S_WIDE, sp, t, j)
        if who == 'ANTON':
            d = j['props'][-1]
            if getattr(d, 'disc', None):            # the numbers, in the person's frame (scaled with him)
                paddle_text(img, B.Local(cam, XS[who], NECK_WIDE - rise * S_WIDE, S_WIDE, 1), d.disc)


def shot_of(t):
    return 'J1' if t < J1_DUR else 'J2'


def cam_for(t):
    return B.Cam(1.6 * FIT, XS['CRAIG'] + 10, NECK_WIDE + 10 + (150 if TALL else 0)) if t < J1_DUR else B.Cam(Z2 * FIT, CX2, CY2)
    # tall J1 sits 150 higher so the desk ends above TikTok's bottom band and the subtitle has floor to sit on


def picture(t):
    cam = cam_for(t)
    img = B.canvas()
    backdrop(img, cam)
    scene_people(img, cam, t)
    table(img, cam)
    if t >= J1_DUR:
        k = crab_frame(t - J1_DUR)
        lay = Image.open(os.path.join(PASS_DIR, f'{k:04d}.png')).convert('RGBA')
        k = cam.z / Z2 * B.SS                      # the crab layer was rendered for J2's widescreen frame (1280 px)
        lay = lay.resize((round(1280 * k), round(720 * k)), Image.LANCZOS)
        x0, y0 = cam.P(CX2 - 640 / Z2, CY2 + (crab_drop() - 360) / Z2)
        top = Image.new('RGBA', img.size); top.paste(lay, (int(round(x0)), int(round(y0))))
        img.alpha_composite(top)
    return img


def overlay(img, t):
    return img


# ------------------------------------------------------------------------------------------------ sound
MUSIC = os.path.join(HERE, '..', 'refs', 'strictly-crabs', 'music.mp3')
SB0 = 9.302                       # song time of the dance's beat 0
FOLD_AT, FOLD_BACK = 48, 24       # Sam, 22 Oct: the crowd claps in the song's last bars (beats 48-56, heard at 23-26 s).
                                  # At beat 48 the music jumps back 24 beats (6 bars: harmony match 0.977, 0.3 dB) and
                                  # carries on from there, folding back again if it gets to 48 again; the claps never play.
UNDER = 0.085 * 1.3               # the music under the judges (Sam, 22 Oct: 30% louder than before; was 0.085)


def song_time(f):
    """Film time (array) -> where in the song to play."""
    d = f - TITLES
    s = np.where(d < CUT_FROM, 9.0 + d, 9.0 + d + CUT_BEATS * BEAT)      # the removed shot: 8 beats skipped, on a bar line
    b = (s - SB0) / BEAT
    return np.where(b >= FOLD_AT, SB0 + (FOLD_AT - FOLD_BACK + (b - FOLD_AT) % FOLD_BACK) * BEAT, s)


def music_bed(f0, dur):
    """The song for film times f0..f0+dur, following song_time, with a 30 ms crossfade at every jump (on bar lines);
    full volume through the dance, eased down to UNDER at the cut to the judges, faded out over the last 0.8 s."""
    song = MA.load(MUSIC)
    sr = MA.SR
    n = int(dur * sr)
    f = f0 + np.arange(n) / sr
    m = song_time(f)
    at = lambda pos: song[np.clip((pos * sr).astype(int), 0, len(song) - 1)] * (pos * sr < len(song))
    out = at(m)
    h = int(0.015 * sr)
    for i in np.nonzero(np.abs(np.diff(m) - 1 / sr) > 1e-3)[0] + 1:
        k = np.arange(max(0, i - h), min(n, i + h))
        r = (k - (i - h)) / (2 * h)
        left = at(m[i - 1] + (k - (i - 1)) / sr)
        right = at(m[i] + (k - i) / sr)
        out[k] = left * np.cos(r * np.pi / 2) + right * np.sin(r * np.pi / 2)
    g = np.clip(f / 0.15, 0, 1)                          # the song starts part-way in: a quick fade-in, no click
    g = np.where(f >= FILM_AT, g * (1 - (1 - UNDER) * np.clip((f - FILM_AT) / 0.25, 0, 1)), g)
    g *= np.clip((FILM_AT + DUR - f) / 0.8, 0, 1)
    return out * g


def voices(dur=None):
    n = int(((dur or DUR) + 0.3) * MA.SR)
    v = np.zeros(n)
    for ln in LINES:
        x = ln['_voice']
        s = int(ln['start'] * MA.SR)
        if s < 0:
            x, s = x[-s:], 0
        seg = x[:max(0, n - s)]
        v[s:s + len(seg)] += seg
    return v


def soundtrack(stems=False):
    """The judges' section on its own (for clips): the voices over the song, already lowered."""
    v = voices()
    bed = music_bed(FILM_AT, len(v) / MA.SR)
    mix, g = MA.master(v + bed, int(DUR * MA.SR))
    return (mix, v * g, bed * g) if stems else mix


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
    sheet.paste(picture(J1_DUR + 0.1).convert('RGB'), (0, 720))
    sheet.paste(picture(0.0).convert('RGB'), (0, 1440))
    sheet.save(out, quality=90)


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        cast_sheet(a[1])
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            picture(float(x)).convert('RGB').save(os.path.join(a[1], f'j{x}.jpg'), quality=88)
    elif a[0] == 'final':
        import film_engine as E
        small = '--small' in a
        E.render('strictly-judges', a[1], size=((540, 960) if small else (1080, 1920)) if TALL else ((640, 360) if small else (1280, 720)), ss=1 if small else 2, fps=FPS,
                 dur=DUR, picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None)


if __name__ == '__main__':
    main()
