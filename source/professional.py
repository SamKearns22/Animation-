#!/usr/bin/env python3
"""A Professional: a TV series' spokesperson calmly insists that explorer Steve Backshall, stranded on Neptune, will be
fine, because "Steve is a professional", while we cut to Steve earnestly presenting through ever more impossible peril
(prompts/a-professional.md; from Sam's Tiny Island Times article).

The series' flat look (burnham.py people, Mossad, The Patriots 2), made vertical (1080 x 1920), drawn with the shared
tools: series.py (people always with legs, the press room as one plan seen by every camera, turned bodies), figure.py
(arms solved from where the hands go), kit.py (hands, contact shadows, things that swing a beat behind), mouths.py.

Steve is an affectionate caricature (dark swept hair, broad toothy grin, wiry, rolled sleeves, outdoor shirt, boots, a
helmet with a head torch, a chest camera). Everyone else is invented. No real show names or logos.

The voices come later: every line is timed from Sam's natural pace (about 3.3 words a second) until his recordings
(named 01-10 by script line) arrive; captions, mouths and cuts follow the placeholders now and his takes later.

Usage:
    python3 professional.py times                    the timeline
    python3 professional.py stills OUT_DIR T1 T2 ...  frames at those times (seconds)
    python3 professional.py sheet OUT.jpg            the storyboard
    python3 professional.py model OUT.jpg            the model sheet (cast, views, objects)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import series as S
import burnham as B
import peepee as PP
import figure as F
import kit
import mouths
from ed import INK, curve, oval, soft

FPS = 12
TITLE = 'A PROFESSIONAL'
CAM0 = B.Cam(1.0, 540, 960)

# ------------------------------------------------------------------------------------------- colours
KHAKI = (196, 174, 124)
OLIVE_T = (88, 92, 70)
HELMET = (238, 238, 232)
KAYAK = (206, 40, 40)
EXPEDITION = (236, 120, 36)
NAVY_BLAZER = (40, 48, 76)
WALL = (212, 216, 224)
CARPET = (92, 100, 116)
WOOD = (176, 136, 96)
TEAL = (24, 128, 136)
STRAP = (52, 54, 60)

# ------------------------------------------------------------------------------------------- the cast
STEVE = dict(name='Steve', skin=(232, 186, 152), hw=64, hh=92, jaw='long', hair='swept', hair_c=(44, 32, 26),
             brow_c=(40, 28, 22), brow_w=3.6, outfit='jumper', jacket=KHAKI, trousers=OLIVE_T, shoulders=136, bottom=530,
             rolled=True, boots=True, shoe=S.BOOTS, kit='steve', helmet=HELMET, mouth='toothy', brows='sincere',
             pose='custom')
SPOKES = dict(name='the spokesperson', skin=(238, 202, 178), hw=62, hh=86, jaw='soft', hair='bob', hair_c=(34, 28, 30),
              brow_c=(44, 34, 34), outfit='blouse', jacket=NAVY_BLAZER, shirt=(244, 242, 238), trousers=NAVY_BLAZER,
              shoulders=138, bottom=560, lips=True, lip_c=(170, 76, 88), earring=True, brows='serious', mouth='line',
              badge=TEAL, pose='custom')
# the journalists (seated, facing the lectern): each with a clear action
EDITOR = dict(name='the science editor', skin=(204, 150, 112), hw=62, hh=86, jaw='round', hair='bob', hair_c=(70, 44, 32),
              glasses=True, glasses_c=(60, 30, 40), outfit='jumper', jacket=(110, 60, 80), trousers=(44, 44, 54),
              shoulders=136, bottom=540, lips=True, lip_c=(150, 70, 80), magazine=True, badge=(200, 60, 60), pose='custom')
ASKER = dict(name='the journalist', skin=B.PINK, hw=70, hh=90, jaw='square', hair='crop', hair_c=(120, 92, 64),
             beard='stubble', beard_c=(120, 92, 64), outfit='jumper', jacket=(186, 150, 60), trousers=(60, 62, 72),
             shoulders=148, bottom=560, badge=(200, 60, 60), pose='custom')
PHONE = dict(name='the phone journalist', skin=B.DEEP, hw=62, hh=86, jaw='soft', hair='afro', hair_c=(30, 24, 22),
             outfit='blouse', jacket=(70, 110, 96), shirt=(236, 230, 214), trousers=(40, 40, 46), shoulders=134, bottom=550,
             lips=True, lip_c=(120, 56, 60), badge=(200, 60, 60), pose='custom')
CUP = dict(name='the coffee journalist', skin=B.OLIVE, hw=68, hh=88, jaw='round', hair='slick', hair_c=(36, 30, 28),
           outfit='suit', jacket=(70, 70, 78), shirt=(220, 228, 240), trousers=(70, 70, 78), shoulders=146, bottom=560,
           badge=(200, 60, 60), pose='custom')
BACKROW = [  # background journalists: skin, hair, hair colour, outfit, jacket, action
    (B.PALE, 'side', (150, 110, 70), 'jumper', (80, 96, 140), 'write'),
    (B.BROWN, 'crop', (30, 26, 24), 'suit', (50, 54, 64), 'phone'),
    (B.PINK, 'wavy', (170, 120, 70), 'blouse', (140, 70, 60), 'write'),
    (B.DEEP, 'crop', (24, 20, 20), 'jumper', (96, 120, 90), 'cup'),
    (B.PALE, 'bald', (120, 100, 90), 'suit', (60, 60, 70), 'write'),
    (B.OLIVE, 'long', (50, 36, 30), 'jumper', (170, 140, 110), 'phone'),
]
PHOTOG = dict(name='the photographer', skin=B.BROWN, hw=68, hh=88, jaw='square', hair='crop', hair_c=(28, 24, 22),
              beard='trim', beard_c=(40, 32, 28), outfit='jumper', jacket=(40, 40, 46), trousers=(50, 52, 60),
              shoulders=146, bottom=560, badge=(200, 60, 60), pose='custom')
TVOP = dict(name='the camera operator', skin=B.PALE, hw=66, hh=88, jaw='square', hair='beanie', beanie_c=(60, 64, 70),
            hair_c=(90, 70, 50), outfit='jumper', jacket=(30, 32, 36), trousers=(40, 40, 46), shoulders=146, bottom=560,
            pose='custom')
EXPERTS = [  # matching expedition jackets
    dict(name='expert 1', skin=B.PALE, hw=64, hh=88, jaw='square', hair='crop', hair_c=(150, 110, 60), outfit='jumper',
         jacket=EXPEDITION, trousers=(50, 54, 60), shoulders=140, bottom=540, kit='expert', helmet=(240, 200, 40),
         boots=True, shoe=S.BOOTS, pose='custom'),
    dict(name='expert 2', skin=B.BROWN, hw=62, hh=86, jaw='soft', hair='bob', hair_c=(30, 24, 22), outfit='jumper',
         jacket=EXPEDITION, trousers=(50, 54, 60), shoulders=134, bottom=540, kit='expert', helmet=(240, 200, 40),
         boots=True, shoe=S.BOOTS, pose='custom'),
]
RIG = {}


def rig(sp):
    if sp['name'] not in RIG:
        RIG[sp['name']] = F.Rig(sp, name=sp['name'])
    return RIG[sp['name']]


# ------------------------------------------------------------------------------------------- drawing extras
_torso, _hair_front, _mouth, _hand = B.torso, B.hair_front, B.mouth, B.gesture_hand


def steve_shirt(img, p, sp):
    """An outdoor shirt: open collar, button placket, two flapped chest pockets; the chest-camera harness."""
    sw, bottom, c, skin = sp['shoulders'], sp['bottom'], sp['jacket'], sp['skin']
    cd = B.dk(c, 0.78)
    tous = sp.get('tousle', 0.0)
    p.poly([(-34, -6), (34, -6), (0, 66)], skin, None)
    soft(img, p.cam, [(-20, 0), (20, 0), (0, 50)], (150, 90, 80), 0.25, 3)
    for sgn in (-1, 1):                                                           # the collar points
        lift = 10 * tous if sgn > 0 else 0
        p.poly([(sgn * 30, -14), (sgn * 66, -4 - lift), (sgn * 52, 46 - lift), (sgn * 4, 66)], B.lt(c, 1.06), INK, 2.2)
    p.line([(0, 66), (0, bottom - 4)], cd, 2.2)
    for k in range(6):
        p.ell(6, 100 + 70 * k, 3.5, 3.5, cd, None)
    for sgn in (-1, 1):                                                           # chest pockets with flaps
        x0, x1 = sgn * 30, sgn * 96
        p.poly([(x0, 112), (x1, 112), (x1, 196), (x0, 196)], c, INK, 1.8)
        flap_up = (sgn < 0) * 18 * tous
        p.poly([(x0, 104 - flap_up), (x1, 104 - flap_up), (x1, 130 - flap_up), ((x0 + x1) / 2, 136 - flap_up), (x0, 130 - flap_up)],
               B.lt(c, 1.05), INK, 1.8)
    if tous > 0:                                                                  # sweat, a torn hem, grime
        for pts in ([(-sw + 6, 70), (-sw + 60, 90), (-sw + 50, 220), (-sw + 4, 230)],
                    [(sw - 6, 70), (sw - 60, 90), (sw - 50, 220), (sw - 4, 230)], [(-40, 200), (40, 200), (30, 320), (-30, 320)]):
            soft(img, p.cam, pts, B.dk(c, 0.6), 0.45 * tous, 10)
        for x in (-90, 20, 100):
            p.poly([(x - 12, bottom - 1), (x + 12, bottom - 1), (x, bottom - 26 * tous)], B.dk(c, 0.5), None)
        for x, y in ((-70, 300), (60, 380), (-20, 450)):
            p.ell(x, y, 12 * tous, 7 * tous, B.dk(c, 0.7), None)
    # the harness: two straps over the shoulders to a chest plate, the little camera on it
    for sgn in (-1, 1):
        p.line([(sgn * 64, -6), (sgn * 30, 150)], STRAP, 9)
    p.line([(-sw + 14, 176), (sw - 14, 176)], STRAP, 9)
    p.poly([(-34, 140), (34, 140), (34, 192), (-34, 192)], (30, 30, 34), INK, 2.0)
    p.ell(0, 166, 15, 15, (60, 64, 74), INK, 2.0)
    p.ell(-4, 162, 5, 5, (170, 190, 220), None)
    p.ell(26, 148, 3, 3, (230, 40, 40), None)


def expert_jacket(img, p, sp):
    sw, bottom, c = sp['shoulders'], sp['bottom'], sp['jacket']
    p.poly([(-46, -14), (46, -14), (40, 20), (-40, 20)], B.dk(c, 0.9), INK, 2.2)  # the high collar
    p.line([(0, 20), (0, bottom - 4)], B.dk(c, 0.6), 2.6)                         # the zip
    p.poly([(-sw + 4, 250), (sw - 4, 250), (sw - 2, 276), (-sw + 2, 276)], (220, 224, 228), INK, 1.6)  # reflective band
    p.line([(-sw + 20, 60), (-30, 70)], STRAP, 8)                                 # the harness the rope is tied to
    p.line([(-sw + 10, 420), (sw - 10, 420)], STRAP, 10)


def lanyard(img, p, sp):
    """A pass on a lanyard round the neck; sp['swing'] (radians) swings the pass a beat behind the body."""
    sw = sp.get('swing', 0.0)
    bx, by = 210 * math.sin(sw), 210 * math.cos(sw) - 10
    lc = sp['badge']
    p.line([(-30, -2), (bx - 12, by)], lc, 6)
    p.line([(30, -2), (bx + 12, by)], lc, 6)
    p.poly([(bx - 32, by), (bx + 32, by), (bx + 32, by + 82), (bx - 32, by + 82)], (248, 248, 248), INK, 2.0)
    p.poly([(bx - 32, by), (bx + 32, by), (bx + 32, by + 18), (bx - 32, by + 18)], lc, None)
    for k in range(2):
        p.line([(bx - 22, by + 40 + 16 * k), (bx + 22 - 16 * k, by + 40 + 16 * k)], (160, 160, 170), 2.4)


def magazine(img, p, sp):
    """A magazine tucked under the arm on our left (drawn before the arm, so the arm holds it against her side)."""
    sw = sp['shoulders']
    pts = [(-sw - 40, 150), (-sw + 46, 136), (-sw + 60, 380), (-sw - 26, 394)]
    p.poly(pts, (40, 90, 170), INK, 2.2)
    p.poly([(-sw - 30, 160), (-sw + 40, 148), (-sw + 44, 196), (-sw - 26, 206)], (246, 246, 240), None)
    p.poly([(-sw - 10, 250), (-sw + 46, 240), (-sw + 52, 330), (-sw - 4, 340)], (240, 180, 60), None)


def torso(img, p, sp, t):
    _torso(img, p, sp, t)
    k = sp.get('kit')
    if k == 'steve':
        steve_shirt(img, p, sp)
    elif k == 'expert':
        expert_jacket(img, p, sp)
    if sp.get('magazine'):
        magazine(img, p, sp)
    if sp.get('badge'):
        lanyard(img, p, sp)


def helmet(p, sp, hx, hy, hw, hh, fx):
    """A climbing helmet sitting on the head (the fringe and sides of the hair show under it), a head torch on the
    front, the chin strap down past the ears."""
    c = sp['helmet']
    brim, top = hy - hh * 0.7, hy - hh * 1.42
    w = hw * 1.1
    for sgn in (-1, 1):
        p.line([(hx + sgn * (hw - 2), brim + 12), (hx + sgn * (hw - 6), hy + 20), (hx + sgn * hw * 0.55, hy + hh * 1.0)],
               STRAP, 2.6)
    dome = curve([(hx - w, brim + 6), (hx - w * 0.98, hy - hh * 1.06), (hx - w * 0.6, top + 10), (hx, top),
                  (hx + w * 0.6, top + 10), (hx + w * 0.98, hy - hh * 1.06), (hx + w, brim + 6)], 4)
    p.poly(dome + [(hx + w * 0.9, brim + 14), (hx - w * 0.9, brim + 14)], c, INK, 2.6)
    p.poly([(hx - w * 0.5, top + 26), (hx - w * 0.2, top + 16), (hx - w * 0.22, top + 40), (hx - w * 0.5, top + 46)],
           B.dk(c, 0.82), None)
    p.line([(hx - w * 0.96, brim - 4), (hx + w * 0.96, brim - 4)], STRAP, 5)       # the torch's band
    tx = fx + (hx - fx) * 0.2
    p.poly(curve([(tx - 22, brim - 22), (tx + 22, brim - 22), (tx + 24, brim + 6), (tx - 24, brim + 6)], 2), (50, 52, 58), INK, 2.0)
    p.ell(tx, brim - 7, 10, 9, (255, 240, 150) if sp.get('torch', True) else (120, 120, 110), INK, 1.6)
    if sp.get('plastered'):                                                        # sweat-sodden strands stuck to the brow
        hc = B.dk(sp.get('hair_c', (40, 30, 24)), 0.8)
        for k, x in enumerate((-30, -6, 18)):
            p.line([(fx + x, brim + 8), (fx + x - 8, brim + 40 + 8 * k), (fx + x + 2, brim + 56 + 6 * k)], hc, 5)


def hair_front(p, sp, hx, hy, hw, hh, fx):
    _hair_front(p, sp, hx, hy, hw, hh, fx)
    if sp.get('helmet'):
        helmet(p, sp, hx, hy, hw, hh, fx)
    if sp.get('sweat'):
        for k, (x, y) in enumerate(((-38, -50), (30, -60), (54, 4), (-56, 20))):
            if (k + 1) / 4 <= sp['sweat'] + 0.01:
                p.poly([(fx + x, hy + y - 10), (fx + x + 6, hy + y + 4), (fx + x, hy + y + 9), (fx + x - 6, hy + y + 4)],
                       (210, 236, 250), INK, 1.4)


def mouth(p, sp, t, fx, my):
    m = sp.get('mouth', 'line')
    if m in ('toothy', 'toothy_open'):          # the broad toothy grin (open: mid-exclamation)
        o = 12 if m == 'toothy_open' else 0
        w = 32
        pts = curve([(fx - w, my - 10), (fx, my - 5), (fx + w, my - 10), (fx + w * 0.72, my + 10 + o), (fx, my + 15 + o),
                     (fx - w * 0.72, my + 10 + o)], 4)
        p.poly(pts, (96, 30, 36), INK, 2.4)
        p.poly([(fx - w + 6, my - 8), (fx + w - 6, my - 8), (fx + w * 0.7, my + 3), (fx - w * 0.7, my + 3)], (250, 250, 246), None)
        if o < 6:
            p.poly([(fx - w * 0.6, my + 9), (fx + w * 0.6, my + 9), (fx + w * 0.5, my + 13), (fx - w * 0.5, my + 13)],
                   (240, 240, 236), None)
        for x in (-16, -5, 6, 17):
            p.line([(fx + x, my - 7), (fx + x, my + 2)], (190, 190, 186), 1.2)
        skin_d = B.dk(sp['skin'], 0.78)
        for sgn in (-1, 1):                     # the grin's creases
            p.line([(fx + sgn * (w + 4), my - 16), (fx + sgn * (w + 8), my - 4), (fx + sgn * (w + 2), my + 6)], skin_d, 1.8)
        return
    _mouth(p, sp, t, fx, my)


def gesture_hand(p, el, wr, shape, skin, extra=None, t=0.0):
    """Extra hands for this film: a phone held up to record (we see its back), a mallet, a tent peg."""
    dx, dy = wr[0] - el[0], wr[1] - el[1]
    n = math.hypot(dx, dy) or 1
    d = (dx / n, dy / n)
    c = (wr[0] + d[0] * 18, wr[1] + d[1] * 18)
    if shape == 'phoneback':
        cx, cy = c[0], c[1] - 22
        p.poly([(cx - 22, cy - 40), (cx + 22, cy - 40), (cx + 22, cy + 40), (cx - 22, cy + 40)], (36, 36, 42), INK, 2.2)
        p.ell(cx - 11, cy - 28, 5, 5, (90, 96, 110), INK, 1.2)
        p.ell(cx + 1, cy - 28, 5, 5, (90, 96, 110), INK, 1.2)
        p.ell(cx, cy + 34, 22, 18, skin, INK, 2.2)
        return
    if shape in ('mallet', 'peg'):
        ang = extra if extra is not None else math.atan2(d[1], d[0])
        u = (math.cos(ang), math.sin(ang))
        nrm = (-u[1], u[0])
        if shape == 'mallet':                   # a wooden handle and a rubber head
            a = (c[0] - u[0] * 30, c[1] - u[1] * 30)
            b = (c[0] + u[0] * 120, c[1] + u[1] * 120)
            p.line([a, b], (150, 110, 70), 9)
            hp = [(b[0] + nrm[0] * 40 + u[0] * 0, b[1] + nrm[1] * 40), (b[0] - nrm[0] * 40, b[1] - nrm[1] * 40),
                  (b[0] - nrm[0] * 40 + u[0] * 34, b[1] - nrm[1] * 40 + u[1] * 34), (b[0] + nrm[0] * 40 + u[0] * 34, b[1] + nrm[1] * 40 + u[1] * 34)]
            p.poly(hp, (40, 40, 44), INK, 2.2)
        else:                                   # a steel tent peg, point first
            a = (c[0] - u[0] * 20, c[1] - u[1] * 20)
            b = (c[0] + u[0] * 110, c[1] + u[1] * 110)
            p.line([a, b], (190, 196, 206), 7)
            p.line([(a[0] - nrm[0] * 12, a[1] - nrm[1] * 12), (a[0] + nrm[0] * 14, a[1] + nrm[1] * 14)], (190, 196, 206), 7)
        p.ell(c[0], c[1], 24, 21, skin, INK, 2.6)
        for k in range(3):
            p.line([(c[0] - 12 + 8 * k, c[1] - 14), (c[0] - 10 + 8 * k, c[1] + 12)], B.dk(skin, 0.8), 1.6)
        return
    _hand(p, el, wr, shape, skin, extra, t)


B.torso, B.hair_front, B.mouth, B.gesture_hand = torso, hair_front, mouth, gesture_hand
F.HAND.update({'phoneback': 26, 'mallet': 18, 'peg': 18})


def talk(track, t, rest='line'):
    """The mouth shape now from a line's track (placeholder or recording), or the resting mouth."""
    if not track:
        return rest
    s = mouths.at(track, t)
    return rest if s == 'rest' else 'v:' + s


# ------------------------------------------------------------------------------------------- the script and timeline
# (who, words a second, caption pieces). Sam's natural pace is about 3.3 words a second; the dreamy line is slower, the
# last line much slower ("as if explaining something obvious to a dim child"). The words are the script's.
LINE_DEFS = [
    ('news', 3.4, ["The producers of Steve Backshall's TV series", 'have confirmed that the explorer', 'is stranded on the planet Neptune:',
                   'the ice giant,', 'eighth planet from the sun.']),
    ('spokes', 3.3, ['We would encourage fans', 'not to panic or speculate.', 'Steve is a professional.',
                     'He would have the training and know-how', 'to survive a supercritical strata', 'of hydrogen sulfide and ammonia.']),
    ('spokes', 3.3, ['Steve has survived perils', 'on ice and on water.', 'And luckily for him,', 'Neptune is an inseparable mix of both.',
                     'Make no mistake:', 'he will be able to kayak to safety.']),
    ('asker', 3.5, ['How is he supposed to handle', 'winds of 1,300 miles an hour,', 'as he plummets through clouds of methane?']),
    ('spokes', 3.3, ['Steve is a professional.', 'He has abseiled down cliffs in Oman', 'and navigated deep jungle in Suriname.',
                     'Some combination of rope-work', 'will keep him from being', 'violently tossed about,', 'as he searches for',
                     'the best place to camp.']),
    ('spokes', 3.0, ['Eventually he will reach a layer', 'so pressurised and hot', 'that methane molecules break apart.',
                     'Imagine his wonder,', 'when the carbon crystallises into diamonds', "that rain down towards the planet's core.",
                     "He'll say things like..."]),
    ('steve', 2.8, ['WOW!', 'THIS IS WHY EXPLORATION', 'IS SO IMPORTANT!']),
    ('spokes', 3.2, ['His shirt will be tousled,', 'his hair sweat-sodden.', 'His earnest smile will inspire',
                     'a new generation of maniacs.']),
    ('editor', 3.3, ['No suit in existence could withstand', 'the molten, crushing pressure', "of Neptune's core."]),
    ('spokes', 1.7, ['Steve is a professional.', 'A professional.']),
]
SHOUTED = {6}
T = {}
LINES = []          # (who, start, end, pieces, words, track)


def build_timeline():
    def line(i, at, stop=0.32):
        who, wps, pieces = LINE_DEFS[i]
        if i == 9:   # slowly, with a long pause before the repeat
            w = S.word_times(at, wps, pieces[:1], stop=0.0)
            w += [(x, a, b, 1) for x, a, b, _ in S.word_times(w[-1][2] + 0.9, wps * 0.9, pieces[1:])]
        else:
            w = S.word_times(at, wps, pieces, stop=stop)
        st = S.stretches([(x, a - at, b - at, k) for x, a, b, k in w])
        LINES.append((who, at, w[-1][2], pieces, w, (at, mouths.track(' '.join(pieces), st))))
        return w

    def piece_start(w, k):
        return next(a for _, a, _, i in w if i == k)
    w = line(0, 0.25)                                   # 1. Neptune, cold open: the premise at once
    T['s2a'] = w[-1][2] + 0.3                           # 2a. press room, slow push-in
    w = line(1, T['s2a'] + 0.3)
    T['s2b'] = piece_start(w, 3) - 0.12                 # 2b. closer for the first laugh ("supercritical strata")
    T['s3a'] = w[-1][2] + 0.35                          # 3a. Neptune: the sea, paddling
    w = line(2, T['s3a'] + 0.3)
    T['s3b'] = piece_start(w, 4) - 0.12                 # 3b. "kayak to safety": turning in circles
    T['s4'] = w[-1][2] + 0.4                            # 4. the journalists (reverse angle)
    T['hand'] = T['s4'] + 0.15                          #    the journalist's pen goes up
    w = line(3, T['s4'] + 0.7)
    T['s5'] = w[-1][2] + 0.25                           # 5. the huff, then her list
    T['huff'] = T['s5'] + 0.15
    w = line(4, T['s5'] + 0.95)
    T['s6'] = piece_start(w, 3) - 0.12                  # 6. Neptune, the gale
    T['s7'] = w[-1][2] + 0.35                           # 7. press room: the diagram, the marker deeper
    w = line(5, T['s7'] + 0.3)
    T['s8'] = piece_start(w, 3) - 0.12                  # 8. Neptune, deeper: diamonds
    T['s9'] = w[-1][2] + 0.25                           # 9. Steve to camera: "Wow!"
    w = line(6, T['s9'] + 0.25, stop=0.45)
    T['s10'] = w[-1][2] + 0.3                           # 10. slow push on his grin
    w = line(7, T['s10'] + 0.3)
    T['s11'] = w[-1][2] + 0.3                           # 11. the science editor
    w = line(8, T['s11'] + 0.45)
    T['s12'] = w[-1][2] + 0.3                           # 12. the spokesperson, slowly
    w = line(9, T['s12'] + 0.6)
    T['s13'] = w[-1][2] + 0.6                           # 13. tiny in the glow, thumbs up
    T['black'] = T['s13'] + 3.0                         #     hard cut to black
    T['dur'] = T['black'] + 0.4


build_timeline()
BLACK_AT, DUR = T['black'], T['dur']
SHOTS = [('open', 0.0, T['s2a']), ('press_wide', T['s2a'], T['s2b']), ('press_close', T['s2b'], T['s3a']),
         ('kayak', T['s3a'], T['s3b']), ('circles', T['s3b'], T['s4']), ('journalists', T['s4'], T['s5']),
         ('huff', T['s5'], T['s6']), ('gale', T['s6'], T['s7']), ('diagram', T['s7'], T['s8']), ('deeper', T['s8'], T['s9']),
         ('wow', T['s9'], T['s10']), ('grin', T['s10'], T['s11']), ('editor', T['s11'], T['s12']),
         ('slowly', T['s12'], T['s13']), ('end', T['s13'], T['black'])]
# the STEVE marker on the press room's diagram: a little deeper every time we cut back (0 surface - 1 core)
MARKER = {'press_wide': 0.12, 'press_close': 0.14, 'huff': 0.3, 'diagram': 0.58, 'slowly': 0.97}


def line_of(who, t):
    """The line being spoken by `who` at t (or the nearest one), for the mouths."""
    for L in LINES:
        if L[0] == who and L[1] - 0.2 <= t <= L[2] + 0.2:
            return L
    return None


def mouth_of(who, t, rest='line'):
    L = line_of(who, t)
    if not L:
        return rest
    at, trk = L[5]
    return talk(trk, t - at, rest)


def shot_at(t):
    for name, a, b in SHOTS:
        if a <= t < b:
            return name, t - a
    return SHOTS[-1][0], t - SHOTS[-1][1]


# ------------------------------------------------------------------------------------------- the press room (one plan)
# Metres. X across (to the right seen from the back of the room), Y up, Z from the front wall into the room.
ROOM_X, ROOM_Z, CEIL = 4.0, 9.0, 3.0
SCREEN = (0.05, 0.95, 1.55, 2.45)          # the diagram screen on the front wall: X0, X1, Y0, Y1
BANNER = (-1.50, -0.20, 2.15)              # a pull-up banner standing on the floor against the wall: X0, X1, top
LECTERN = (-0.40, 1.00, 0.56, 1.00)        # front face centre X, Z; width; height (her elbow height)
SPOKES_AT = (-0.40, 0.72)                  # where she stands
TABLE = (0.30, 0.70, 0.95, 1.25, 0.74)     # the side table with the water: X0, X1, Z0, Z1, height
BOOM = ((-2.4, 2.1, 2.0), (-0.36, 2.22, 1.02))   # the boom: the operator's hands (off to the side) to the windshield
ROWS = (3.2, 4.3, 5.4)                     # the rows of chairs
SEATS = (-1.3, -0.5, 0.5, 1.3)             # chairs in each row (a centre aisle)
SEAT_H = (S.SEAT_FEET - S.SEAT_HIP) * S.M_PER_UNIT
TVCAM = (2.25, 6.1)                        # the TV camera on its tripod (operator behind it)
PHOTOG_AT = (0.0, 4.9)                     # the photographer standing in the aisle
DOOR = (-2.4, -1.4)                        # on the back wall
SEATING = {(0, 1.3): 'editor', (0, 0.5): 'asker', (0, -0.5): 'phone', (0, -1.3): 0, (1, 1.3): 1, (1, 0.5): 2,
           (1, -0.5): 'cup', (1, -1.3): 3, (2, 0.5): 4, (2, -1.3): 5}


def check_plan():
    """Set pieces that must stay apart, from the plan (front wall pieces in X/Y; floor pieces in X/Z)."""
    F.check_apart('the front wall', {'screen': (SCREEN[0], SCREEN[2], SCREEN[1], SCREEN[3]),
                                     'banner': (BANNER[0], 0.0, BANNER[1], BANNER[2])})
    lx, lz, lw, _ = LECTERN
    floor = {'lectern': (lx - lw / 2, lz - 0.45, lx + lw / 2, lz), 'table': (TABLE[0], TABLE[2], TABLE[1], TABLE[3]),
             'tv camera': (TVCAM[0] - 0.4, TVCAM[1] - 0.4, TVCAM[0] + 0.4, TVCAM[1] + 0.9),
             'photographer': (PHOTOG_AT[0] - 0.25, PHOTOG_AT[1] - 0.2, PHOTOG_AT[0] + 0.25, PHOTOG_AT[1] + 0.2)}
    for r, z in enumerate(ROWS):
        for x in SEATS:
            floor[f'chair {r}{x}'] = (x - 0.24, z - 0.22, x + 0.24, z + 0.24)
    F.check_apart('the press room floor', floor)


check_plan()


def poly3(img, room, pts, fill, line=INK, lw=2.4):
    B.Pen(img, CAM0).poly(room.quad(pts), fill, line, lw)


def line3(img, room, pts, colr, lw):
    B.Pen(img, CAM0).line(room.quad(pts), colr, lw)


def diagram(img, box, depth, t, laser=None):
    """The cutaway of Neptune on the press room screen: the layers as rings (blue methane clouds; a hot, crushing
    layer; diamond rain; the core), the near side cut away; the little STEVE marker on its way down."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    S_ = B.SS
    lay = Image.new('RGBA', (int(w * S_), int(h * S_)), (14, 20, 44, 255))
    d = ImageDraw.Draw(lay)
    cx, cy, R = 0.27 * w * S_, 0.57 * h * S_, 0.25 * w * S_
    rings = [(1.0, (110, 200, 236)), (0.78, (70, 90, 190)), (0.56, (44, 40, 120)), (0.30, (246, 140, 50))]
    for r, c in rings:
        d.ellipse([cx - R * r, cy - R * r, cx + R * r, cy + R * r], fill=c, outline=(10, 10, 20), width=max(1, int(2 * S_)))
    # the far side: the planet's banded surface over the left half (the right half is the cut-away)
    surf = Image.new('RGBA', lay.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(surf)
    sd.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(90, 170, 226, 255))
    for k in range(-4, 5):
        yy = cy + k * R * 0.2
        sd.line([(cx - R, yy), (cx + R, yy + R * 0.04)], fill=(150, 210, 240, 255), width=max(1, int(3 * S_)))
    sd.ellipse([cx - R * 0.5, cy + R * 0.1, cx - R * 0.15, cy + R * 0.3], fill=(40, 80, 160, 255))
    mask = Image.new('L', lay.size, 0)
    ImageDraw.Draw(mask).rectangle([0, 0, cx, lay.height], fill=255)
    lay.paste(surf, (0, 0), Image.composite(surf.getchannel('A'), Image.new('L', lay.size, 0), mask))
    d.line([(cx, cy - R), (cx, cy + R)], fill=(10, 10, 20), width=max(1, int(2 * S_)))
    rng = np.random.default_rng(3)
    for _ in range(14):                                   # the diamond rain: sparkles in the third ring
        a = rng.uniform(-1.5, 1.5)
        r = rng.uniform(0.33, 0.53) * R
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        if px > cx + 4:
            d.polygon([(px, py - 5 * S_), (px + 3 * S_, py), (px, py + 5 * S_), (px - 3 * S_, py)], fill=(240, 250, 255))
    f = ImageFont.truetype(B.SANS, int(h * 0.046 * S_))
    labels = [(0.89, 'CLOUDS'), (0.67, 'HOT LAYER'), (0.43, 'DIAMOND RAIN'), (0.12, 'CORE')]
    for r, s in labels:
        lx, ly = cx + R * 1.12, cy - R * r * 0.98
        d.line([(cx + R * r * 0.5, cy - R * r * 0.87 + 2), (lx - 4, ly)], fill=(220, 226, 236), width=max(1, int(1.4 * S_)))
        d.text((lx, ly), s, font=f, fill=(236, 240, 246), anchor='lm')
    d.text((0.05 * w * S_, 0.04 * h * S_), 'NEPTUNE', font=ImageFont.truetype(B.SANS, int(h * 0.075 * S_)), fill=(236, 240, 246))
    # the marker: down a dotted line from the surface towards the core
    ang = math.radians(32)
    ux, uy = math.cos(ang), math.sin(ang)
    for k in range(20):
        r = R * (1 - k / 20 * 0.92)
        d.ellipse([cx + r * ux - 1.5 * S_, cy + r * uy - 1.5 * S_, cx + r * ux + 1.5 * S_, cy + r * uy + 1.5 * S_], fill=(250, 250, 250))
    r = R * (1.0 - 0.9 * depth)
    mx, my = cx + r * ux, cy + r * uy
    d.ellipse([mx - 8 * S_, my - 8 * S_, mx + 8 * S_, my + 8 * S_], fill=(232, 30, 40), outline=(255, 255, 255), width=int(2 * S_))
    tag = ImageFont.truetype(B.SANS, int(h * 0.06 * S_))
    l, tp, rr, bb = d.textbbox((0, 0), 'STEVE', font=tag)
    tx, ty = mx + 12 * S_, my + 10 * S_
    d.rectangle([tx, ty, tx + (rr - l) + 10 * S_, ty + (bb - tp) + 8 * S_], fill=(232, 30, 40), outline=(255, 255, 255), width=int(1.5 * S_))
    d.text((tx + 5 * S_ - l, ty + 4 * S_ - tp), 'STEVE', font=tag, fill=(255, 255, 255))
    if laser is not None:                                 # her laser pointer, circling the marker
        lx_, ly_ = mx + 22 * S_ * math.cos(t * 7), my + 16 * S_ * math.sin(t * 7)
        d.ellipse([lx_ - 5 * S_, ly_ - 5 * S_, lx_ + 5 * S_, ly_ + 5 * S_], fill=(255, 40, 40))
    img.alpha_composite(lay, (int(x0 * S_), int(y0 * S_)))


def front_wall(img, room, t, depth):
    """The front wall and everything against it, seen by a camera looking at it (Z = 0)."""
    p = B.Pen(img, CAM0)
    poly3(img, room, [(-ROOM_X, 0, 0), (ROOM_X, 0, 0), (ROOM_X, CEIL, 0), (-ROOM_X, CEIL, 0)], WALL, None)
    poly3(img, room, [(-ROOM_X, CEIL, 0), (ROOM_X, CEIL, 0), (ROOM_X, CEIL, room.Z - 0.3), (-ROOM_X, CEIL, room.Z - 0.3)],
          (236, 236, 238), None)
    for x in (-1.6, 0.6):                                            # ceiling light panels
        poly3(img, room, [(x, CEIL, 0.8), (x + 1.0, CEIL, 0.8), (x + 1.0, CEIL, 1.4), (x, CEIL, 1.4)], (252, 252, 246), INK, 1.6)
    poly3(img, room, [(-ROOM_X, 0, 0), (ROOM_X, 0, 0), (ROOM_X, 0, room.Z - 0.3), (-ROOM_X, 0, room.Z - 0.3)], CARPET, None)
    line3(img, room, [(-ROOM_X, 0.1, 0.001), (ROOM_X, 0.1, 0.001)], (180, 184, 192), 3)  # the skirting
    # the pull-up banner: plain mountains and lettering (no logo)
    x0, x1, top = BANNER
    poly3(img, room, [(x0 + 0.1, 0, 0.12), (x1 - 0.1, 0, 0.12), (x1 - 0.1, 0.06, 0.12), (x0 + 0.1, 0.06, 0.12)], (120, 124, 130))
    poly3(img, room, [(x0, 0.06, 0.1), (x1, 0.06, 0.1), (x1, top, 0.1), (x0, top, 0.1)], (30, 44, 82))
    mtn = [(x0, 1.0), (x0 + 0.25, 1.45), (x0 + 0.42, 1.28), (x0 + 0.72, 1.72), (x0 + 0.95, 1.4), (x0 + 1.1, 1.55), (x1, 1.2), (x1, 1.0)]
    poly3(img, room, [(x, y, 0.1) for x, y in mtn], (70, 96, 150), None)
    poly3(img, room, [(x0 + 0.62, 1.6, 0.1), (x0 + 0.72, 1.72, 0.1), (x0 + 0.8, 1.62, 0.1)], (236, 240, 246), None)
    tx, ty = room.P((x0 + x1) / 2, 1.92, 0.1)
    PP.ctext(img, CAM0, tx, ty, 'PRESS BRIEFING', 0.075 * room.k(0.1), (236, 240, 246), font=B.ANTON)
    # the screen with the diagram
    sx0, sx1, sy0, sy1 = SCREEN
    poly3(img, room, [(sx0 - 0.03, sy0 - 0.03, 0.02), (sx1 + 0.03, sy0 - 0.03, 0.02), (sx1 + 0.03, sy1 + 0.03, 0.02),
                      (sx0 - 0.03, sy1 + 0.03, 0.02)], (24, 24, 28))
    a, b = room.P(sx0, sy1, 0.02), room.P(sx1, sy0, 0.02)
    diagram(img, (a[0], a[1], b[0], b[1]), depth, t, laser=True if room.Y > 1.8 else None)


def lectern_top(img, room):
    lx, lz, lw, lh = LECTERN
    x0, x1 = lx - lw / 2, lx + lw / 2
    poly3(img, room, [(x0, lh + 0.06, lz - 0.32), (x1, lh + 0.06, lz - 0.32), (x1, lh, lz), (x0, lh, lz)], B.dk(WOOD, 0.9))


def lectern(img, room, t):
    lx, lz, lw, lh = LECTERN
    x0, x1 = lx - lw / 2, lx + lw / 2
    p = B.Pen(img, CAM0)
    for k, dx in enumerate((-0.07, -0.02, 0.03, 0.08)):                      # the cluster of microphones
        base, head = room.P(lx + dx * 0.6, lh + 0.04, lz - 0.06), room.P(lx + dx * 1.3, lh + 0.2 + 0.02 * (k % 2), lz - 0.2)
        p.line([base, head], (40, 40, 44), 4.0)
        r = 0.032 * room.k(lz - 0.2)
        if k in (0, 3):
            cube = [(lx + dx * 1.3 - 0.022, lh + 0.13, lz - 0.17), (lx + dx * 1.3 + 0.022, lh + 0.13, lz - 0.17),
                    (lx + dx * 1.3 + 0.022, lh + 0.17, lz - 0.17), (lx + dx * 1.3 - 0.022, lh + 0.17, lz - 0.17)]
            poly3(img, room, cube, [(200, 50, 50), (60, 120, 200)][k // 3], INK, 1.2)
        p.ell(head[0], head[1], r * 0.75, r, (52, 52, 58), INK, 1.6)
    poly3(img, room, [(x0, 0, lz), (x1, 0, lz), (x1, lh, lz), (x0, lh, lz)], WOOD)
    poly3(img, room, [(x0 + 0.06, 0.15, lz), (x1 - 0.06, 0.15, lz), (x1 - 0.06, lh - 0.1, lz), (x0 + 0.06, lh - 0.1, lz)],
          NAVY_BLAZER, INK, 1.6)
    a = room.P(lx, 0.66, lz)
    PP.ctext(img, CAM0, a[0], a[1], '▲', 0.12 * room.k(lz), (210, 220, 236))
    kit.contact_shadow(img, CAM0, *room.P(lx, 0, lz), lw * room.k(lz) * 1.1)


def side_table(img, room):
    x0, x1, z0, z1, h = TABLE
    kit.contact_shadow(img, CAM0, *room.P((x0 + x1) / 2, 0, z1), (x1 - x0) * room.k(z1) * 1.2)
    for x in (x0 + 0.04, x1 - 0.04):
        line3(img, room, [(x, 0, z1 - 0.04), (x, h, z1 - 0.04)], (60, 60, 66), 3)
    poly3(img, room, [(x0, h, z0), (x1, h, z0), (x1, h, z1), (x0, h, z1)], (226, 226, 230))
    poly3(img, room, [(x0, h - 0.03, z1), (x1, h - 0.03, z1), (x1, h, z1), (x0, h, z1)], (190, 190, 196))
    # a jug of water and a glass
    jx, gx, z = x0 + 0.12, x0 + 0.3, (z0 + z1) / 2
    k = room.k(z)
    a = room.P(jx, h, z)
    p = B.Pen(img, CAM0)
    jw, jh = 0.12 * k, 0.24 * k
    p.poly([(a[0] - jw / 2, a[1]), (a[0] + jw / 2, a[1]), (a[0] + jw * 0.55, a[1] - jh), (a[0] - jw * 0.4, a[1] - jh)],
           (206, 228, 240), INK, 1.8)
    p.poly([(a[0] - jw / 2 + 2, a[1] - 2), (a[0] + jw / 2 - 2, a[1] - 2), (a[0] + jw * 0.5, a[1] - jh * 0.65), (a[0] - jw * 0.45, a[1] - jh * 0.65)],
           (150, 196, 226), None)
    p.line([(a[0] + jw * 0.5, a[1] - jh * 0.85), (a[0] + jw * 0.85, a[1] - jh * 0.6), (a[0] + jw * 0.5, a[1] - jh * 0.3)], INK, 2.0)
    g = room.P(gx, h, z)
    gw, gh = 0.07 * k, 0.11 * k
    p.poly([(g[0] - gw / 2, g[1]), (g[0] + gw / 2, g[1]), (g[0] + gw * 0.6, g[1] - gh), (g[0] - gw * 0.6, g[1] - gh)], (214, 232, 242), INK, 1.6)
    p.poly([(g[0] - gw / 2 + 1, g[1] - 1), (g[0] + gw / 2 - 1, g[1] - 1), (g[0] + gw * 0.55, g[1] - gh * 0.6), (g[0] - gw * 0.55, g[1] - gh * 0.6)],
           (160, 200, 228), None)


def boom(img, room, t):
    (hx, hy, hz), (wx, wy, wz) = BOOM
    bob = 0.01 * math.sin(t * 1.3)
    a, b = room.P(hx, hy, hz), room.P(wx, wy + bob, wz)
    p = B.Pen(img, CAM0)
    p.line([a, b], (60, 62, 68), max(3, 0.02 * room.k(wz) * 0.8))
    k = room.k(wz)
    rng = np.random.default_rng(4)
    pts = [(b[0] + 0.15 * k * math.cos(u) * (1 + 0.05 * rng.uniform(-1, 1)), b[1] + 0.04 * k * math.sin(u) * (1 + 0.15 * rng.uniform(-1, 1)))
           for u in np.linspace(0, 2 * math.pi, 26, endpoint=False)]
    p.poly(pts, (96, 94, 92), INK, 1.8)
    for k_ in range(10):
        u = rng.uniform(0, 2 * math.pi)
        p.line([(b[0] + 0.09 * k * math.cos(u), b[1] + 0.03 * k * math.sin(u)), (b[0] + 0.12 * k * math.cos(u), b[1] + 0.05 * k * math.sin(u))],
               (100, 98, 96), 1.4)


def LECTERN_HANDS(r):
    """Her hands resting on the lectern's top at elbow height: the upper arms hang, the forearms come forward over the
    top towards us (drawn short), the hands lying flat on it."""
    out = {}
    for side, sgn in (('L', -1), ('R', 1)):
        sh = r.shoulder(side)
        el = (sh[0] + sgn * 10, sh[1] + r.upper * 0.97)
        out[side] = (el, (el[0] - sgn * 52, el[1] + 52), 'flat')
    return out


def spokes_sp(t, mouth='line', **kw):
    """Her standing pose behind the lectern: hands resting on its edges, the pass swinging a beat behind her moves."""
    r = rig(SPOKES)
    base = dict(SPOKES, arms=LECTERN_HANDS(r),
                mouth=mouth, swing=0.03 * math.sin(t * 1.1), lid=1, blink=F.blinking(t, F.blinks(7, 0, 90, talking=True)))
    base.update(kw)
    return base


def press_front(t, room, depth, sp=None):
    img = B.canvas()
    front_wall(img, room, t, depth)
    x, y, s = room.person(*SPOKES_AT)
    kit.feet_shadow(img, CAM0, x, y, s)
    near = room.depth(LECTERN[1]) > 0.4       # (a camera right up at the screen is past the lectern)
    if near:
        lectern_top(img, room)                # her hands rest on its top; its front hides her below
    S.person(img, CAM0, x, y, s, sp or spokes_sp(t), t)
    if near:
        lectern(img, room, t)
    if room.depth(TABLE[3]) > 0.4:
        side_table(img, room)
    if room.depth(BOOM[1][2]) > 0.4:
        boom(img, room, t)
    return img


# --- the reverse angle: the journalists, from beside the lectern
def chair(img, room, X, Z):
    k = room.k(Z)
    for dx in (-0.2, 0.2):
        for dz in (-0.18, 0.2):
            line3(img, room, [(X + dx, 0, Z + dz), (X + dx, SEAT_H, Z + dz)], (50, 52, 58), 3)
            kit.contact_shadow(img, CAM0, *room.P(X + dx, 0, Z + dz), 0.06 * k)
    poly3(img, room, [(X - 0.22, 0.45, Z + 0.22), (X + 0.22, 0.45, Z + 0.22), (X + 0.22, 0.88, Z + 0.24), (X - 0.22, 0.88, Z + 0.24)],
          (60, 86, 120))
    poly3(img, room, [(X - 0.27, SEAT_H, Z - 0.22), (X + 0.27, SEAT_H, Z - 0.22), (X + 0.27, SEAT_H, Z + 0.22), (X - 0.27, SEAT_H, Z + 0.22)],
          (70, 96, 132))
    poly3(img, room, [(X - 0.27, SEAT_H - 0.04, Z - 0.22), (X + 0.27, SEAT_H - 0.04, Z - 0.22), (X + 0.27, SEAT_H, Z - 0.22), (X - 0.27, SEAT_H, Z - 0.22)],
          (50, 70, 100))


def notepad_hands(r, t, writing=True, ph=0.0):
    """A notepad held flat on the lap in one hand, the pen writing on it with the other."""
    wig = 8 * math.sin(t * 14 + ph) if writing else 0.0
    return {'L': r.arm('L', (-56, 420), 'flat', 'depth'), 'R': r.arm('R', (30 + wig, 400 + 0.5 * wig), 'pen', 'depth')}


def notepad(img, cam, x, y, s):
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    p.poly([(-110, 380), (40, 384), (46, 470), (-104, 466)], (248, 246, 226), INK, 2.0)
    for k in range(4):
        p.line([(-96, 400 + 16 * k), (20, 402 + 16 * k)], (150, 170, 200), 1.6)
    p.line([(-110, 380), (40, 384)], (60, 60, 70), 4)


def journalist(img, room, key, t, seated_at, act=None):
    """One seated journalist at (X, Z), facing the lectern, doing their thing."""
    X, Z = seated_at
    x, y, s = room.person(X, Z, seated=True)
    if isinstance(key, int):
        sk, hair, hc, outfit, jc, action = BACKROW[key]
        sp = dict(name=f'journalist {key}', skin=sk, hw=66, hh=88, jaw=['square', 'soft', 'round'][key % 3], hair=hair,
                  hair_c=hc, outfit=outfit, jacket=jc, shirt=(232, 234, 240), trousers=B.dk(jc, 0.7), shoulders=140,
                  bottom=540, badge=(200, 60, 60), pose='custom', look=-0.2 * X)
    else:
        sp = dict({'editor': EDITOR, 'asker': ASKER, 'phone': PHONE, 'cup': CUP}[key])
        action = {'editor': 'editor', 'asker': 'write', 'phone': 'phone', 'cup': 'cup'}[key]
        sp['look'] = -0.25 * X
    sp['bottom'] = 452                          # seated: the jumper or jacket ends at the lap
    r = rig(sp)
    seed = sum(map(ord, str(key))) % 1000
    sp['blink'] = F.blinking(t, F.blinks(seed, 0, 90))
    sp['swing'] = 0.02 * math.sin(t * 0.9 + seed)
    if action == 'write':
        sp['arms'] = notepad_hands(r, t, ph=seed)
        sp['look'], sp['head_dy'] = 0.0, 10
    elif action == 'phone':
        sp['arms'] = {'L': r.pose('sides')['L'], 'R': r.arm('R', (170 + 4 * math.sin(t * 2 + seed), -60), 'phoneback', 'down', depth=0.5)}
    elif action == 'cup':
        sip = max(0.0, math.sin((t + seed % 7) * 0.8)) ** 6
        sp['arms'] = {'L': r.arm('L', (-60, 430), 'flat', 'depth'),
                      'R': r.arm('R', (-10 + 40 * (1 - sip), -50 + 380 * (1 - sip)), 'cup', 'down')}
    elif action == 'editor':
        sp['arms'] = {'L': r.arm('L', (-sp['shoulders'] + 30, 440), 'relaxed', 'depth'), 'R': r.arm('R', (40, 430), 'flat', 'depth')}
    if act:
        act(sp, r, t)
    if action == 'write':
        notepad(img, CAM0, x, y, s)
    chair(img, room, X, Z)
    S.person(img, CAM0, x, y, s, sp, t, legs=S.seated_legs())
    if action == 'write':                          # the pad lies on the lap, in front of the legs, under the hands
        pass
    return x, y, s


def tv_camera(img, room, t):
    X, Z = TVCAM
    x, y, s = room.person(X, Z + 0.45)
    op = dict(TVOP, look=-0.2, arms=rig(TVOP).arms(((-40, 270), 'grip', 'down'), ((180, 310), 'grip', 'down')))
    kit.feet_shadow(img, CAM0, x, y, s)
    S.person(img, CAM0, x, y, s, op, t)
    k = room.k(Z)
    for dx, dz in ((-0.35, 0.25), (0.35, 0.25), (0.0, -0.4)):
        line3(img, room, [(X, 1.25, Z), (X + dx, 0, Z + dz)], (40, 40, 44), 4)
        kit.contact_shadow(img, CAM0, *room.P(X + dx, 0, Z + dz), 0.08 * k)
    poly3(img, room, [(X - 0.13, 1.3, Z - 0.25), (X + 0.13, 1.3, Z - 0.25), (X + 0.13, 1.56, Z - 0.25), (X - 0.13, 1.56, Z - 0.25)],
          (36, 36, 40))
    c = room.P(X, 1.42, Z - 0.3)
    p = B.Pen(img, CAM0)
    p.ell(c[0], c[1], 0.09 * k, 0.09 * k, (20, 20, 24), INK, 2.0)
    p.ell(c[0] - 0.02 * k, c[1] - 0.02 * k, 0.03 * k, 0.03 * k, (90, 100, 130), None)
    a = room.P(X + 0.12, 1.62, Z - 0.1)
    p.ell(a[0], a[1], 0.025 * k, 0.025 * k, (230, 40, 40) if int(t * 2) % 2 else (120, 30, 30), None)  # the tally light


def photographer(img, room, t, flash):
    X, Z = PHOTOG_AT
    x, y, s = room.person(X, Z)
    r = rig(PHOTOG)
    sp = dict(PHOTOG, arms={'L': r.arm('L', (-70, -70), 'grip', 'down'), 'R': r.arm('R', (90, -120), 'grip', 'down')},
              blink=True, head_dy=4)
    kit.feet_shadow(img, CAM0, x, y, s)
    S.person(img, CAM0, x, y, s, sp, t)
    L = B.Local(CAM0, x, y, s)
    p = B.Pen(img, L)
    p.poly([(-70, -190), (90, -190), (90, -90), (-70, -90)], (30, 30, 34), INK, 2.4)
    p.poly([(-50, -214), (20, -214), (20, -190), (-50, -190)], (30, 30, 34), INK, 2.0)
    p.ell(0, -140, 44, 44, (20, 20, 24), INK, 2.4)
    p.ell(-8, -148, 16, 16, (100, 110, 140), None)
    for hx, hy in ((-70, -70), (90, -120)):
        p.ell(hx, hy - 20, 24, 21, PHOTOG['skin'], INK, 2.4)
    if flash > 0:
        a = L.P(-15, -205)
        glow = Image.new('RGBA', img.size, (0, 0, 0, 0))
        r_ = L.S(260)
        ImageDraw.Draw(glow).ellipse([a[0] - r_, a[1] - r_, a[0] + r_, a[1] + r_], fill=(255, 255, 255, int(200 * flash)))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(r_ * 0.35)))


def press_back(t, room, acts=None, flash=0.0):
    """The reverse angle: from beside the lectern, looking at the rows of journalists, the TV camera, the door."""
    acts = acts or {}
    img = B.canvas()
    near = room.Z + 0.3
    poly3(img, room, [(-ROOM_X, 0, ROOM_Z), (ROOM_X, 0, ROOM_Z), (ROOM_X, CEIL, ROOM_Z), (-ROOM_X, CEIL, ROOM_Z)], WALL, None)
    for sgn in (-1, 1):
        poly3(img, room, [(sgn * ROOM_X, 0, near), (sgn * ROOM_X, 0, ROOM_Z), (sgn * ROOM_X, CEIL, ROOM_Z), (sgn * ROOM_X, CEIL, near)],
              B.dk(WALL, 0.93), None)
    poly3(img, room, [(-ROOM_X, 0, near), (ROOM_X, 0, near), (ROOM_X, 0, ROOM_Z), (-ROOM_X, 0, ROOM_Z)], CARPET, None)
    poly3(img, room, [(-ROOM_X, CEIL, near), (ROOM_X, CEIL, near), (ROOM_X, CEIL, ROOM_Z), (-ROOM_X, CEIL, ROOM_Z)], (236, 236, 238), None)
    for z in (3.0, 5.4, 7.8):
        poly3(img, room, [(-0.5, CEIL, z), (0.5, CEIL, z), (0.5, CEIL, z + 0.6), (-0.5, CEIL, z + 0.6)], (252, 252, 246), INK, 1.4)
    d0, d1 = DOOR
    poly3(img, room, [(d0, 0, ROOM_Z), (d1, 0, ROOM_Z), (d1, 2.05, ROOM_Z), (d0, 2.05, ROOM_Z)], (150, 120, 92))
    a = room.P(d1 - 0.12, 1.05, ROOM_Z)
    B.Pen(img, CAM0).ell(a[0], a[1], 4, 4, (200, 200, 190), INK, 1.2)
    c = room.P(0.9, 2.3, ROOM_Z)
    k = room.k(ROOM_Z)
    p = B.Pen(img, CAM0)
    p.ell(c[0], c[1], 0.17 * k, 0.17 * k, (250, 250, 248), INK, 2.0)
    p.line([c, (c[0], c[1] - 0.12 * k)], INK, 2.0)
    p.line([c, (c[0] + 0.08 * k, c[1] + 0.03 * k)], INK, 2.0)
    # everything on the floor, far to near
    items = [(TVCAM[1], lambda: tv_camera(img, room, t)), (PHOTOG_AT[1], lambda: photographer(img, room, t, flash))]
    for (row, X), key in SEATING.items():
        Z = ROWS[row]
        items.append((Z, (lambda key=key, X=X, Z=Z: journalist(img, room, key, t, (X, Z), acts.get(key)))))
    for Z, fn in sorted(items, key=lambda it: -room.depth(it[0])):
        if room.depth(Z) > 0.4:
            fn()
    return img


# ------------------------------------------------------------------------------------------- Neptune
def palette(d):
    """Neptune's colours by depth: 0 bright cyan clouds, 0.5 dark indigo, 1 the hot orange glow near the core."""
    keys = [(0.0, (34, 120, 206), (150, 226, 248)), (0.25, (24, 70, 160), (90, 170, 230)), (0.5, (16, 22, 70), (50, 52, 140)),
            (0.75, (20, 14, 44), (150, 70, 80)), (1.0, (50, 16, 30), (252, 160, 70))]
    for (a, t0, b0), (b, t1, b1) in zip(keys, keys[1:]):
        if a <= d <= b:
            u = (d - a) / (b - a)
            return (tuple(int(t0[i] + (t1[i] - t0[i]) * u) for i in range(3)), tuple(int(b0[i] + (b1[i] - b0[i]) * u) for i in range(3)))
    return keys[-1][1], keys[-1][2]


_GRAD = {}


def sky(img, d, t, rise=600.0, wind=0.0, seed=1, clouds=14, spot=True):
    """The sky at depth d; streaks of methane cloud rushing up past a falling camera (rise, px a second) or sideways
    in a gale (wind, px a second)."""
    W, H = img.size
    key = (round(d, 2), W)
    if key not in _GRAD:
        top, bot = palette(d)
        y = np.linspace(0, 1, H)[:, None, None] ** 1.2
        g = np.array(top)[None, None] * (1 - y) + np.array(bot)[None, None] * y
        _GRAD[key] = Image.fromarray(np.repeat(g, W, axis=1).astype(np.uint8), 'RGB').convert('RGBA')
    img.alpha_composite(_GRAD[key])
    S_ = B.SS
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(lay)
    if d < 0.35:                                          # faint rings, Triton far off, the dark storm spot
        a = int(70 * (1 - d / 0.35))
        for k in range(3):
            dr.arc([-600 * S_, (150 + 26 * k) * S_, 1700 * S_, (700 + 26 * k) * S_], 196, 344, fill=(230, 240, 250, a), width=int(3 * S_))
        dr.ellipse([200 * S_, 400 * S_, 252 * S_, 452 * S_], fill=(220, 226, 236, a + 40))
        if spot:
            dr.ellipse([700 * S_, 560 * S_, 940 * S_, 650 * S_], fill=(20, 40, 110, a))
    rng = np.random.default_rng(seed)
    cc = (255, 255, 255) if d < 0.5 else (255, 220, 190)
    for _ in range(clouds):
        x0, y0 = rng.uniform(-200, 1280), rng.uniform(0, 2400)
        ln, wd = rng.uniform(260, 700), rng.uniform(30, 90)
        al = rng.uniform(0.25, 0.6) * (1 - 0.6 * d)
        if wind:
            x = (x0 + wind * t) % 1700 - 300
            box = [x * S_, (y0 % 1920) * S_, (x + ln * 1.6) * S_, (y0 % 1920 + wd * 0.5) * S_]
        else:
            y = (y0 - rise * t) % 2400 - 300
            box = [x0 * S_, y * S_, (x0 + wd * 0.8) * S_, (y + ln) * S_]
        dr.ellipse(box, fill=cc + (int(255 * al),))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(14 * S_)))
    if d > 0.55:                                          # the heat below
        glow = Image.new('RGBA', img.size, (0, 0, 0, 0))
        u = (d - 0.55) / 0.45
        ImageDraw.Draw(glow).ellipse([-400 * S_, (1500 - 700 * u) * S_, 1480 * S_, 3000 * S_], fill=(255, 150, 60, int(160 * u)))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120 * S_)))


def lightning(img, x, y, t, seed, length=700):
    rng = np.random.default_rng(seed)
    pts, px, py = [(x, y)], x, y
    while py < y + length:
        px += rng.uniform(-60, 60)
        py += rng.uniform(40, 90)
        pts.append((px, py))
    p = B.Pen(img, CAM0)
    glow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    B.Pen(glow, CAM0).line(pts, (200, 230, 255, 160), 26)
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10 * B.SS)))
    p.line(pts, (250, 252, 255), 5)


def diamonds(img, t, n=40, seed=7, speed=900, size=1.0, box=(0, 0, 1080, 1920)):
    """Glittering diamonds raining down past him (faster than he falls)."""
    rng = np.random.default_rng(seed)
    p = B.Pen(img, CAM0)
    x0, y0, x1, y1 = box
    for i in range(n):
        x = rng.uniform(x0, x1)
        sp = speed * rng.uniform(0.6, 1.3)
        y = (rng.uniform(0, 2000) + sp * t) % (y1 - y0 + 200) + y0 - 100
        r = size * rng.uniform(7, 16)
        tw = 0.5 + 0.5 * math.sin(t * 9 + i)
        p.poly([(x, y - r * 1.3), (x + r, y), (x, y + r * 1.3), (x - r, y)], (220, 246, 255), (120, 170, 220), 1.4)
        p.poly([(x, y - r * 1.3), (x + r, y), (x, y)], (255, 255, 255), None)
        if tw > 0.7:
            k = r * 2.2 * tw
            p.line([(x - k, y), (x + k, y)], (255, 255, 255), 1.6)
            p.line([(x, y - k), (x, y + k)], (255, 255, 255), 1.6)


def warm_light(img, amount):
    """The core's orange light from below, over everything (lit from underneath)."""
    if amount <= 0:
        return
    W, H = img.size
    y = np.linspace(0, 1, H)[:, None] ** 2.0
    a = (y * 120 * amount).astype(np.uint8)
    lay = Image.new('RGBA', img.size, (255, 140, 60, 0))
    lay.putalpha(Image.fromarray(np.repeat(a, W, axis=1), 'L'))
    img.alpha_composite(lay)


# --- Steve's views
def steve_sp(t, **kw):
    sp = dict(STEVE, blink=F.blinking(t, F.blinks(11, 0, 90, per_min=(10, 14))))
    sp.update(kw)
    return sp


def hair_whip(img, cam, x, y, s, t, direction=(0, -1), n=5, tilt=0.0):
    """Strands of his hair whipped by the wind past the helmet's edge (direction: where the wind blows them)."""
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, PP.Rot(L, tilt, pivot=(0, -60)) if tilt else L)
    ux, uy = direction
    for k in range(n):
        bx, by = -60 + 30 * k, -212
        pts = [(bx, by)]
        for j in range(1, 5):
            wob = 14 * math.sin(t * 16 + k * 1.7 + j)
            pts.append((bx + ux * 26 * j - uy * wob, by + uy * 26 * j + ux * wob))
        p.line(pts, STEVE['hair_c'], 7)


def steve_falling(img, cam, x, y, s, t, ang=0.0, d=0.0, wonder=0.0, thumbs=True, mouth=None, look=0.0):
    """Falling or floating: arms out (one thumb up), legs apart, hair whipped upwards; ang turns the whole body."""
    r = rig(STEVE)
    flap = math.sin(t * 9)
    arms = {'L': r.arm('L', (-300, 120 + 20 * flap), 'wave' if wonder else 'relaxed', 'down'),
            'R': r.arm('R', (230, -120), 'thumbs', 'down') if thumbs else r.arm('R', (300, 110 - 20 * flap), 'wave', 'down')}
    sp = steve_sp(t, arms=arms, stance=34, look=look, brows='wow' if wonder else 'sincere',
                  mouth=mouth or ('toothy_open' if wonder > 0.5 else 'toothy'))
    tc = Turnedmaybe(cam, ang, x, y)
    S.person(img, tc, x, y, s, sp, t)
    return sp


def Turnedmaybe(cam, a, x, y):
    return S.Turned(cam, a, x, y) if a else cam


KAYAK_L = 4.0 / S.M_PER_UNIT        # the sea kayak, 4 m long, in Steve's units (one size, always against him)
KAYAK_W = 0.6 / S.M_PER_UNIT


def kayak(img, cam, x, y, s, theta, t, steve_fn, squash=0.32, paddle=None):
    """The red sea kayak on the water at (x, y) (the cockpit), seen from a little above; theta turns it on the water
    (0 = side-on, bow to our right). Steve sits in the cockpit (drawn by steve_fn, clipped by the deck)."""
    k = s
    c, sn = math.cos(theta), math.sin(theta)
    N = 28
    pts_top, pts_bot = [], []
    for i in range(N + 1):
        u = (i / N - 0.5) * KAYAK_L
        w = 0.5 * KAYAK_W * max(0.0, 1 - (2 * u / KAYAK_L) ** 2) ** 0.55
        for v, out in ((w, pts_top), (-w, pts_bot)):
            out.append((x + (u * c - v * sn) * k, y + (u * sn + v * c) * k * squash))
    deck = pts_top + pts_bot[::-1]
    hull_h = 0.22 / S.M_PER_UNIT * k
    p = B.Pen(img, cam)
    # the near side of the hull (the lower outline on screen), down to the water
    near = pts_bot if c >= 0 else pts_top
    near = sorted(near, key=lambda q: q[0])
    side = [(qx, qy) for qx, qy in near] + [(qx, qy + hull_h * (1 - abs(2 * i / max(1, len(near) - 1) - 1) ** 3)) for i, (qx, qy) in enumerate(near)][::-1]
    p.poly(side, B.dk(KAYAK, 0.72), INK, 2.4)
    p.poly(deck, KAYAK, INK, 2.6)
    for f in (0.32, -0.32):                                   # deck lines (bungee cords)
        u = f * KAYAK_L
        a = (x + (u * c - 0.18 * KAYAK_W * sn) * k, y + (u * sn + 0.18 * KAYAK_W * c) * k * squash)
        b = (x + (u * c + 0.18 * KAYAK_W * sn) * k, y + (u * sn - 0.18 * KAYAK_W * c) * k * squash)
        p.line([a, b], (30, 30, 34), 3)
    rim = [(x + (0.42 / S.M_PER_UNIT * math.cos(a) * c - 0.2 / S.M_PER_UNIT * math.sin(a) * sn) * k,
            y + (0.42 / S.M_PER_UNIT * math.cos(a) * sn + 0.2 / S.M_PER_UNIT * math.sin(a) * c) * k * squash)
           for a in np.linspace(0, 2 * math.pi, 30, endpoint=False)]
    p.poly(rim, (30, 28, 30), INK, 2.4)
    # Steve, cut off where the deck in front of him hides his legs
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    steve_fn(lay)
    front = max(q[1] for q in rim)
    S_ = B.SS
    mask = Image.new('L', img.size, 255)
    md = ImageDraw.Draw(mask)
    md.rectangle([0, int(cam.P(0, front - 6)[1]), img.width, img.height], fill=0)
    md.polygon([cam.P(*q) for q in rim], fill=255)
    md.rectangle([0, 0, img.width, int(cam.P(0, y - 0.06 / S.M_PER_UNIT * k)[1])], fill=255)
    lay.putalpha(Image.composite(lay.getchannel('A'), Image.new('L', img.size, 0), mask))
    img.alpha_composite(lay)
    p.line(rim[len(rim) // 4: 3 * len(rim) // 4 + 1], (40, 38, 40), 6)      # the coaming in front of him
    return deck


def paddle_arms(r, phase, one_side=False):
    """The double paddle across his chest, held out in front of him (the arms reach towards us, so they are drawn
    shorter); strokes alternate sides (or only on one side: round in circles)."""
    a = 0.35 * math.sin(phase) if not one_side else 0.35 + 0.25 * math.sin(phase)
    c = (0.0, 230.0)
    half = 160
    hl = (c[0] - half * math.cos(a), c[1] - half * math.sin(a))
    hr = (c[0] + half * math.cos(a), c[1] + half * math.sin(a))
    return a, c, {'L': r.arm('L', hl, 'grip', 'down', depth=0.3), 'R': r.arm('R', hr, 'grip', 'down', depth=0.3)}


def draw_paddle(img, cam, x, y, s, a, c, splash_y=None, t=0.0):
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    ln = 1100
    ux, uy = math.cos(a), math.sin(a)
    e1 = (c[0] - ux * ln, c[1] - uy * ln)
    e2 = (c[0] + ux * ln, c[1] + uy * ln)
    p.line([e1, e2], (70, 72, 80), 22)
    for e, sg in ((e1, -1), (e2, 1)):
        nx, ny = -uy, ux
        bl = [(e[0] - sg * ux * 220 + nx * 40, e[1] - sg * uy * 220 + ny * 40), (e[0] + nx * 56, e[1] + ny * 56),
              (e[0] - nx * 56, e[1] - ny * 56), (e[0] - sg * ux * 220 - nx * 40, e[1] - sg * uy * 220 - ny * 40)]
        p.poly(bl, (244, 200, 40), INK, 2.4)
    for hx in (-160, 160):
        h = (c[0] + ux * hx, c[1] + uy * hx)
        p.ell(h[0], h[1], 26, 23, STEVE['skin'], INK, 2.4)
        for k in range(3):
            p.line([(h[0] - 10 + 8 * k, h[1] - 16), (h[0] - 8 + 8 * k, h[1] + 14)], B.dk(STEVE['skin'], 0.8), 1.6)
    return L.P(*e1), L.P(*e2)


def sea(img, t, horizon=1060, d=0.1, chop=1.0):
    """Neptune's churning cyan sea, ice and water mixed, waves rolling towards us."""
    p = B.Pen(img, CAM0)
    top, bot = palette(d)
    p.poly([(0, horizon), (1080, horizon), (1080, 1920), (0, 1920)], (40, 150, 190), None)
    rng = np.random.default_rng(5)
    for k in range(14):
        yb = horizon + (k + (t * 0.6) % 1) ** 1.6 * 14
        amp = (6 + 3 * k) * chop
        pts = [(x, yb + amp * math.sin(x / (60 + 12 * k) + t * 3 + k)) for x in range(-20, 1120, 20)]
        p.poly(pts + [(1100, 1940), (-20, 1940)], (36 + 2 * k, 140 - 2 * k, 184 - 3 * k), None)
        p.line(pts, (170, 236, 250), max(1.5, 0.35 * k))
    for i in range(9):                                     # ice floes
        x = (rng.uniform(0, 1400) + 40 * t) % 1400 - 160
        y = horizon + rng.uniform(40, 760)
        w = rng.uniform(40, 120) * (y - horizon + 200) / 600
        p.poly([(x - w, y), (x - w * 0.6, y - w * 0.25), (x + w * 0.7, y - w * 0.22), (x + w, y), (x + w * 0.5, y + w * 0.12)],
               (234, 248, 252), INK, 1.8)


# ------------------------------------------------------------------------------------------- the shots
def shot_open(t):
    """1. Cold open: Steve already tumbling through bright cyan methane clouds, beaming, thumbs up."""
    img = B.canvas()
    sky(img, 0.0, t, rise=900, seed=1)
    ang = 0.32 * math.sin(t * 0.8) - 0.05
    steve_falling(img, CAM0, 540, 900 + 20 * math.sin(t * 1.3), 0.85, t, ang=ang)
    return img


def shot_press_wide(t):
    """2a. The press room: slow push-in on the spokesperson; the diagram behind her, STEVE in the clouds."""
    u = F.ease(t / max(0.1, T['s2b'] - T['s2a']))
    room = S.Room(0.05, 1.5, 3.05 - 0.45 * u, 1300)
    tt = t + T['s2a']
    return press_front(tt, room, MARKER['press_wide'], spokes_sp(tt, mouth=mouth_of('spokes', tt)))


def shot_press_close(t):
    """2b. Closer on her: "a supercritical strata of hydrogen sulfide and ammonia"."""
    room = S.Room(-0.12, 1.62, 1.95 - 0.08 * F.ease(t / 5), 1300)
    tt = t + T['s2b']
    return press_front(tt, room, MARKER['press_close'], spokes_sp(tt, mouth=mouth_of('spokes', tt)))


def shot_kayak(t):
    """3a. Neptune's sea: Steve in the red kayak, paddling earnestly; lightning."""
    img = B.canvas()
    sky(img, 0.12, t, rise=0, wind=120, seed=3, clouds=10)
    if 1.2 < t % 3.1 < 1.45:
        lightning(img, 760, 380, t, seed=int(t / 3.1))
    sea(img, t)
    r = rig(STEVE)
    ph = t * 5.0
    a, c, arms = paddle_arms(r, ph)
    x, y, s = 540, 1300 + 12 * math.sin(t * 2.2), 0.5
    bob = 0.05 * math.sin(t * 1.7)
    sp = steve_sp(t, arms=arms, turn=0.25, look=0.4, mouth='toothy', brows='sincere', tilt=bob)

    def steve(lay):
        S.person(lay, CAM0, x, y - 430 * s, s, sp, t, legs=S.seated_legs(S.BOOTS))
    kayak(img, CAM0, x, y, s, 0.62 + 0.06 * math.sin(t), t, steve)
    draw_paddle(img, CAM0, x, y - 430 * s, s, a, c)
    return img


def shot_circles(t):
    """3b. "He will be able to kayak to safety": paddling on one side only, round and round in circles."""
    img = B.canvas()
    sky(img, 0.12, t, rise=0, wind=120, seed=3, clouds=10)
    sea(img, t, horizon=900)
    th = 1.0 + t * 2.4
    x, y, s = 540 + 140 * math.cos(th), 1290 + 50 * math.sin(th), 0.5
    p = B.Pen(img, CAM0)
    p.line([(540 + 150 * math.cos(u), 1300 + 56 * math.sin(u)) for u in np.linspace(th - 3.5, th - 0.3, 20)], (220, 246, 252), 9)
    r = rig(STEVE)
    a, c, arms = paddle_arms(r, t * 6.0, one_side=True)
    sp = steve_sp(t, arms=arms, turn=0.6 * math.sin(th), look=0.3, mouth='toothy', brows='sincere')

    def steve(lay):
        S.person(lay, CAM0, x, y - 430 * s, s, sp, t, legs=S.seated_legs(S.BOOTS))
    kayak(img, CAM0, x, y, s, th + math.pi / 2, t, steve, squash=0.4)
    draw_paddle(img, CAM0, x, y - 430 * s, s, a, c)
    return img


def shot_journalists(t):
    """4. The reverse angle: notepads and raised phones; one journalist asks about the winds."""
    tt = t + T['s4']
    room = S.Room(0.0, 1.2, 0.9, 1500, facing='back')

    def asker(sp, r, t_):
        up = F.overshoot((t_ - T['hand']) / 0.35)
        if t_ > T['hand']:
            sp['arms'] = dict(sp['arms'], R=r.arm('R', (150 + 60 * up, 400 - 600 * up), 'pen', 'down'))
            sp['look'], sp['head_dy'] = 0.1, 0
        sp['mouth'] = mouth_of('asker', t_)
        sp['brows'] = 'serious' if line_of('asker', t_) else None
    flash = max(0.0, 1 - ((t - 1.3) % 2.6) / 0.15) if (t - 1.3) % 2.6 < 0.15 and t > 1.3 else 0.0
    return press_back(tt, room, acts={'asker': asker}, flash=flash)


def shot_huff(t):
    """5. Her contemptuous huff (eyes shut, a little toss of the head), then the list."""
    tt = t + T['s5']
    room = S.Room(-0.15, 1.62, 1.9, 1300)
    h = math.sin(min(1.0, max(0.0, (tt - T['huff']) / 0.55)) * math.pi)
    r = rig(SPOKES)
    talking = line_of('spokes', tt)
    arms = LECTERN_HANDS(r)
    if talking and tt > LINES[4][1] + 1.5:
        g = F.ease((tt - LINES[4][1] - 1.5) / 0.4)
        arms['R'] = r.arm('R', (170 + 110 * g, 300 - 260 * g), 'palm', 'down')
    sp = spokes_sp(tt, mouth=('small' if h > 0.3 else mouth_of('spokes', tt)), arms=arms, blink=h > 0.3,
                   tilt=-0.12 * h, head_dy=-8 * h, swing=0.03 * math.sin(tt * 1.1) + kit.follow(tt, [(0, 0), (T['huff'] + 0.3, 0.25)]),
                   brows='weary' if h > 0.1 else 'serious')
    return press_front(tt, room, MARKER['huff'], sp)


def flier(img, cam, x, y, s, sp, t, ang):
    """Someone blown flat in the gale, roped on (drawn through a turned camera)."""
    tc = S.Turned(cam, ang, x, y)
    S.person(img, tc, x, y, s, sp, t)


def rope_y(x, t, base, amp=26):
    return base + amp * math.sin(x / 140.0 - t * 9.0) + 10 * math.sin(x / 47.0 - t * 15.0)


def rope_pts(t, a, b, n=40, amp=26):
    """The rope from a to b, whipping in the gale (a wave running down it)."""
    out = []
    for k in range(n + 1):
        u = k / n
        x, y = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
        out.append((x, y + amp * math.sin(u * 9 - t * 9.0) * math.sin(math.pi * u) + 8 * math.sin(u * 27 - t * 15)))
    return out


def shot_gale(t):
    """6. 1,300 mph: Steve horizontal, roped to his team of experts, all flapping like bunting; he hammers a tent
    peg into nothing ("the best place to camp")."""
    img = B.canvas()
    sky(img, 0.25, t, rise=0, wind=2200, seed=6, clouds=26, spot=False)
    # Steve nearest the camera, flat out downwind (head into the wind, on our left); the rope from his harness runs
    # back up to the two experts, further off and higher
    r = rig(STEVE)
    sx, sy, ss = 300, 1010 + 26 * math.sin(t * 6.0), 0.68
    ang = -math.pi / 2 + 0.1 * math.sin(t * 8 + 0.7)
    harness = S.Turned(CAM0, ang, sx, sy).P(sx + 0 * ss, sy + 420 * ss)
    harness = (harness[0] / B.SS, harness[1] / B.SS)
    anchors = [(-120, 420), (150, 560), (330, 690), harness]
    p = B.Pen(img, CAM0)
    for a, b in zip(anchors, anchors[1:]):
        p.line(rope_pts(t + a[0] * 0.003, a, b, amp=18), (226, 200, 120), 7)
    for i, ((ex, ey), s_, ph) in enumerate((((150, 560), 0.3, 0.0), ((330, 690), 0.38, 1.9))):
        sp = dict(EXPERTS[i], arms=rig(EXPERTS[i]).arms(((-60, 330), 'grip', 'down'), ((100, 360), 'grip', 'down')),
                  mouth='O', brows='alarm', stance=40, tilt=0.4)
        a_ = -math.pi / 2 + 0.2 * math.sin(t * 8 + ph)
        flier(img, CAM0, ex - 420 * s_, ey - 30 * s_ + 14 * math.sin(t * 7 + ph), s_, sp, t, a_)
    swing = 0.5 + 0.5 * math.sin(t * 7.5)
    arms = {'L': r.arm('L', (-300, 200), 'peg', 'down'),
            'R': r.arm('R', (-130 + 110 * swing, 110 - 170 * swing), 'mallet', 'down')}
    sp = steve_sp(t, arms=arms, stance=40, tilt=0.55, mouth='toothy', brows='sincere', look=-0.3)
    tc = S.Turned(CAM0, ang, sx, sy)
    hair_whip(img, tc, sx, sy, ss, t, direction=(0, 1))
    S.person(img, tc, sx, sy, ss, sp, t)
    return img


def shot_diagram(t):
    """7. The press room's screen: the STEVE marker now deep in the hot layer; her laser dot circling it."""
    tt = t + T['s7']
    room = S.Room(0.5, 2.0, 1.25 - 0.05 * F.ease(t / 4), 1300)
    return press_front(tt, room, MARKER['diagram'] + 0.02 * F.ease(t / 4), spokes_sp(tt, mouth=mouth_of('spokes', tt)))


def shot_deeper(t):
    """8. Deeper: indigo turning to orange heat; diamonds begin to glitter and rain past him; wonder."""
    img = B.canvas()
    dur = T['s9'] - T['s8']
    d = 0.5 + 0.25 * t / dur
    sky(img, d, t, rise=300, seed=8, clouds=8, spot=False)
    diamonds(img, t, n=int(10 + 30 * min(1, t / 2.5)), speed=700)
    steve_falling(img, CAM0, 540, 900, 0.55 + 0.05 * t / dur, t, ang=0.08 * math.sin(t), wonder=1.0, thumbs=False, look=0.3)
    warm_light(img, (d - 0.5) * 2)
    return img


def steve_close(t, z, d, mouth, brows='wow', tous=0.0, sweat=0.0, plastered=False, pings=True, look=0.0):
    img = B.canvas()
    sky(img, d, t, rise=260, seed=9, clouds=8, spot=False)
    diamonds(img, t, n=30, speed=800, size=1.3)
    cam = B.Cam(z, 540, 700)
    r = rig(STEVE)
    sp = steve_sp(t, arms={'L': r.pose('sides')['L'], 'R': r.arm('R', (200, -60), 'thumbs', 'down')}, mouth=mouth,
                  brows=brows, tousle=tous, sweat=sweat, plastered=plastered, look=look,
                  hair_c=B.dk(STEVE['hair_c'], 0.7) if plastered else STEVE['hair_c'])
    S.person(img, cam, 540, 900, 1.0, sp, t)
    if pings:                                             # diamonds pinging off his helmet
        p = B.Pen(img, cam)
        for k in range(3):
            u = (t * 2.2 + k * 0.37) % 1.0
            if u < 0.35:
                hx, hy = 540 + (-40 + 50 * k), 900 - 270 - 6
                bx, by = hx + (k - 1) * 90 * u, hy - 160 * u + 300 * u * u
                p.poly([(bx, by - 12), (bx + 9, by), (bx, by + 12), (bx - 9, by)], (230, 250, 255), INK, 1.4)
                if u < 0.08:
                    for a in range(6):
                        p.line([(hx + 14 * math.cos(a), hy - 4 + 14 * math.sin(a)), (hx + 30 * math.cos(a), hy - 4 + 30 * math.sin(a))],
                               (255, 255, 220), 2.4)
    warm_light(img, (d - 0.5) * 2)
    return img


def shot_wow(t):
    """9. Steve to camera, shouting over the wind: "Wow! This is why exploration is so important!" """
    tt = t + T['s9']
    m = mouth_of('steve', tt, rest='toothy')
    return steve_close(t, 1.55, 0.75, 'toothy_open' if m == 'line' else m, sweat=0.5, tous=0.3)


def shot_grin(t):
    """10. A slow push on his earnest grin: shirt tousled, hair plastered."""
    u = F.ease(t / max(0.1, T['s11'] - T['s10']))
    return steve_close(t, 1.6 + 0.6 * u, 0.8 + 0.08 * u, 'toothy', brows='sincere', tous=1.0, sweat=1.0, plastered=True, pings=False)


def shot_editor(t):
    """11. The reverse angle again, moved in on the front row: the science editor."""
    tt = t + T['s11']
    room = S.Room(1.12, 1.15, 2.05, 1400, facing='back')

    def editor(sp, r, t_):
        sp['mouth'] = mouth_of('editor', t_)
        sp['brows'] = 'serious'
        sp['look'] = -0.5
        if t_ > T['s11'] + 1.2:
            g = F.ease((t_ - T['s11'] - 1.2) / 0.4)
            sp['arms'] = dict(sp['arms'], R=r.arm('R', (150 + 110 * g, 420 - 200 * g), 'palm', 'down'))

    def glance(sp, r, t_):
        sp['look'] = 0.8
    acts = {'editor': editor, 'asker': glance, 2: glance, 1: glance}
    return press_back(tt, room, acts=acts)


def shot_slowly(t):
    """12. The spokesperson, slowly, as if to a dim child: "A professional." The marker at the core."""
    tt = t + T['s12']
    room = S.Room(-0.25, 1.64, 1.7 - 0.12 * F.ease(t / 5), 1300)
    L = LINES[9]
    second = tt > L[4][-2][1] - 0.2 if len(L[4]) > 1 else False
    sp = spokes_sp(tt, mouth=mouth_of('spokes', tt), lid=3, brows='sincere' if second else 'weary',
                   tilt=0.07 if second else 0.0, head_dy=6 * second)
    return press_front(tt, room, MARKER['slowly'], sp)


def shot_end(t):
    """13. Steve tiny in the vast glowing haze, still giving a thumbs-up, drifting down towards the core."""
    img = B.canvas()
    sky(img, 1.0, t, rise=120, seed=13, clouds=10, spot=False)
    diamonds(img, t, n=24, speed=300, size=0.6)
    steve_falling(img, CAM0, 540, 900 + 40 * t, 0.14, t, ang=0.1 * math.sin(t * 0.8))
    warm_light(img, 0.8)
    return img


SHOT_FN = dict(open=shot_open, press_wide=shot_press_wide, press_close=shot_press_close, kayak=shot_kayak,
               circles=shot_circles, journalists=shot_journalists, huff=shot_huff, gale=shot_gale, diagram=shot_diagram,
               deeper=shot_deeper, wow=shot_wow, grin=shot_grin, editor=shot_editor, slowly=shot_slowly, end=shot_end)


# ------------------------------------------------------------------------------------------- frames
def caption_at(t):
    for idx, (who, a, b, pieces, words, _) in enumerate(LINES):
        starts = [next(s for w, s, e, i in words if i == k) for k in range(len(pieces))]
        nxt = LINES[idx + 1][1] if idx + 1 < len(LINES) else 1e9
        for k, piece in enumerate(pieces):
            s0 = starts[k] - 0.05
            s1 = starts[k + 1] - 0.05 if k + 1 < len(pieces) else min(b + 0.45, nxt - 0.05)
            if s0 <= t < s1:
                return piece
    return None


def frame_image(t, captions=True, title=True):
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    view, local = shot_at(t)
    img = SHOT_FN[view](local)
    if captions:
        c = caption_at(t)
        if c:
            idx = next(i for i, L in enumerate(LINES) if L[1] - 0.1 <= t <= L[2] + 0.5)
            (S.shout if idx in SHOUTED else S.caption)(img, c)
    if title and t < 1.0:   # the standard title over the clouds, gone by 1 s
        B.title(img, TITLE, alpha=1.0 if t < 0.75 else 1.0 - (t - 0.75) / 0.25, maxw=840)
    return img


# ------------------------------------------------------------------------------------------- sheets
def model_sheet(dst):
    """The cast and their views, the recurring objects at their one size, for approval before the storyboard."""
    tiles = []

    def tile(label, draw, bg=(246, 244, 240), crop=(140, 360, 940, 1560), sky_d=None, t=0.0):
        img = B.canvas(bg)
        if sky_d is not None:
            sky(img, sky_d, t, rise=0, seed=2, clouds=6, spot=False)
        draw(img)
        S_ = B.SS
        tiles.append((label, img.crop(tuple(int(v * S_) for v in crop))))
    r = rig(STEVE)
    stand = {'L': r.pose('sides')['L'], 'R': r.arm('R', (230, -120), 'thumbs', 'down')}
    tile('STEVE, front: swept dark hair, toothy grin, rolled sleeves, chest camera, helmet + head torch, boots',
         lambda im: (kit.feet_shadow(im, CAM0, 540, 560, 0.85), S.person(im, CAM0, 540, 560, 0.85, steve_sp(0, arms=stand), 0)),
         crop=(90, 230, 990, 1430))
    tile('STEVE, three-quarter',
         lambda im: (kit.feet_shadow(im, CAM0, 540, 560, 0.85), S.person(im, CAM0, 540, 560, 0.85, steve_sp(0, arms=r.pose('sides'), turn=0.7, look=0.8), 0)),
         crop=(90, 230, 990, 1430))
    tile('STEVE, profile', lambda im: steve_profile(im, CAM0, 540, 560, 0.85), crop=(90, 230, 990, 1430))

    def kay(im):
        sea(im, 0.0, horizon=700)
        a, c, arms = paddle_arms(r, 0.8)
        sp = steve_sp(0, arms=arms, turn=0.25, look=0.4)
        kayak(im, CAM0, 540, 1150, 0.36, 0.42, 0, lambda lay: S.person(lay, CAM0, 540, 1150 - 430 * 0.36, 0.36, sp, 0, legs=S.seated_legs(S.BOOTS)))
        draw_paddle(im, CAM0, 540, 1150 - 430 * 0.36, 0.36, a, c)
    tile('Seated in the kayak (4 m sea kayak, one size against him; legs drawn, hidden by the deck)', kay, crop=(0, 600, 1080, 1500))

    def fly(im):
        sky(im, 0.25, 0.0, wind=1, seed=6, clouds=10, spot=False)
        pp = B.Pen(im, CAM0)
        pp.line([(x, rope_y(x, 0.3, 960)) for x in range(-40, 1140, 20)], (220, 196, 120), 8)
        arms = {'L': r.arm('L', (-300, 200), 'peg', 'down'), 'R': r.arm('R', (-80, 40), 'mallet', 'down')}
        sp = steve_sp(0, arms=arms, stance=40, tilt=0.55, look=-0.3)
        tc = S.Turned(CAM0, -math.pi / 2, 600, 920)
        hair_whip(im, tc, 600, 920, 0.5, 0.3, direction=(0, 1))
        S.person(im, tc, 600, 920, 0.5, sp, 0)
    tile('Flying flat on the rope (the gale), hammering a peg into nothing', fly, crop=(0, 600, 1080, 1500))

    def flo(im):
        sky(im, 0.6, 0.0, seed=8, clouds=6, spot=False)
        diamonds(im, 0.3, n=20)
        steve_falling(im, CAM0, 540, 760, 0.6, 0.0, ang=0.1, wonder=1.0, thumbs=False, look=0.3)
        warm_light(im, 0.2)
    tile('Floating down, in wonder (diamonds)', flo, crop=(90, 300, 990, 1500))
    tile('Expressions: grin / "Wow!" / tousled, sweat-sodden',
         lambda im: [S.person(im, B.Cam(1.0, 540, 960), x, 700, 0.62,
                              steve_sp(0, arms=r.pose('sides'), mouth=m, brows=b, tousle=tz, sweat=sw, plastered=pl,
                                       hair_c=B.dk(STEVE['hair_c'], 0.7) if pl else STEVE['hair_c']), 0)
                     for x, m, b, tz, sw, pl in ((230, 'toothy', 'sincere', 0, 0, False), (540, 'v:AI', 'wow', 0.3, 0.5, False),
                                                  (850, 'toothy', 'sincere', 1.0, 1.0, True))], crop=(60, 420, 1020, 1200))
    rs = rig(SPOKES)
    hands = LECTERN_HANDS(rs)
    side = rs.pose('sides')
    tile('THE SPOKESPERSON, front: composed, blazer, lanyard, polite contempt',
         lambda im: (kit.feet_shadow(im, CAM0, 540, 560, 0.85), S.person(im, CAM0, 540, 560, 0.85, dict(SPOKES, arms=side), 0)),
         crop=(90, 230, 990, 1430))
    tile('Spokesperson, three-quarter',
         lambda im: (kit.feet_shadow(im, CAM0, 540, 560, 0.85), S.person(im, CAM0, 540, 560, 0.85, dict(SPOKES, arms=side, turn=-0.7, look=-0.8), 0)),
         crop=(90, 230, 990, 1430))
    tile('Spokesperson, profile', lambda im: spokes_profile(im, CAM0, 540, 560, 0.85), crop=(90, 230, 990, 1430))
    tile('Her faces: composed / the huff / "A professional." (slowly)',
         lambda im: [S.person(im, B.Cam(1.0, 540, 960), x, 700, 0.62, dict(SPOKES, arms=hands, **kw), 0)
                     for x, kw in ((230, dict(mouth='line', lid=1)), (540, dict(mouth='small', blink=True, tilt=-0.12, brows='weary')),
                                   (850, dict(mouth='v:O', lid=3, brows='sincere', tilt=0.07)))], crop=(60, 420, 1020, 1200))

    def seated(im):
        room = S.Room(0.0, 1.0, -2.4, 1500, facing='back')
        for X, key in ((-1.1, 'asker'), (-0.37, 'phone'), (0.37, 'cup'), (1.1, 'editor')):
            journalist(im, room, key, 0.0, (X, 1.0))
    tile('THE JOURNALISTS, seated: notepad, coffee, phone recording, the science editor (glasses, magazine)',
         seated, crop=(0, 560, 1080, 1460))

    def team(im):
        for x, e in ((320, EXPERTS[0]), (760, EXPERTS[1])):
            kit.feet_shadow(im, CAM0, x, 560, 0.7)
            S.person(im, CAM0, x, 560, 0.7, dict(e, arms=rig(e).pose('sides')), 0)
    tile('THE EXPERTS: matching expedition jackets, harness for the rope', team, crop=(60, 260, 1020, 1300))

    def crew(im):
        kit.feet_shadow(im, CAM0, 300, 560, 0.7)
        S.person(im, CAM0, 300, 560, 0.7, dict(PHOTOG, arms=rig(PHOTOG).pose('sides')), 0)
        kit.feet_shadow(im, CAM0, 780, 560, 0.7)
        S.person(im, CAM0, 780, 560, 0.7, dict(TVOP, arms=rig(TVOP).pose('sides')), 0)
    tile('Press photographer; TV camera operator', crew, crop=(60, 260, 1020, 1300))

    def diag(im):
        diagram(im, (90, 600, 990, 1500), 0.58, 0.0)
    tile('The cutaway on the press room screen (STEVE marker goes deeper each time)', diag, crop=(60, 560, 1020, 1540))
    cols = 4
    cw, ch, lab = 420, 520, 84
    rows = (len(tiles) + cols - 1) // cols
    sh = Image.new('RGB', (cols * (cw + 16) + 16, 80 + rows * (ch + lab + 12)), (245, 242, 236))
    d = ImageDraw.Draw(sh)
    d.text((18, 20), 'A PROFESSIONAL: model sheet', font=ImageFont.truetype(B.SANS, 36), fill=(20, 20, 20))
    f = ImageFont.truetype(B.SANS, 19)
    for i, (label, im) in enumerate(tiles):
        x, y = 16 + (i % cols) * (cw + 16), 80 + (i // cols) * (ch + lab + 12)
        im = im.convert('RGB')
        k = min(cw / im.width, ch / im.height)
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        sh.paste(im, (x + (cw - im.width) // 2, y + (ch - im.height) // 2))
        for j, row in enumerate(B.wrap(label, f, cw - 4)[:3]):
            d.text((x + 2, y + ch + 6 + 24 * j), row, font=f, fill=(20, 20, 20))
    sh.save(dst, quality=88)


def side_body(img, cam, x, y, s, sp, head_fn):
    """A person seen side-on, facing our right: legs, torso, the near arm hanging, then the profile head."""
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    tc, jc, skin = sp['trousers'], sp['jacket'], sp['skin']
    shoe = sp.get('shoe', S.SHOES)
    for dx, c in ((-14, B.dk(tc, 0.8)), (14, tc)):
        p.poly([(dx - 50, 440), (dx + 50, 440), (dx + 40, 700), (dx + 36, 900), (dx - 30, 900), (dx - 44, 700)], c, INK, 2.6)
        p.poly(curve([(dx - 36, 880), (dx + 40, 880), (dx + 96, 904), (dx + 96, 928), (dx - 40, 928)], 3), shoe, INK, 2.4)
    p.poly([(-26, -80), (26, -80), (30, 10), (-30, 10)], skin, INK, 2.4)
    body = curve([(-40, -6), (40, -6), (76, 80), (82, 200), (70, sp['bottom']), (-70, sp['bottom']), (-78, 260), (-74, 80)], 3)
    p.poly(body, jc, INK, 2.6)
    soft(img, L, [(-70, 60), (-30, 60), (-40, sp['bottom']), (-70, sp['bottom'])], (0, 0, 0), 0.2, 8)
    head_fn(p, L)
    sleeve = jc
    S._STYLE['rolled'] = skin if sp.get('rolled') else None
    try:
        B.arm(p, (0, 60), (-14, 270), (6, 440), sleeve)
    finally:
        S._STYLE['rolled'] = None
    p.ell(10, 462, 24, 22, skin, INK, 2.4)


def steve_profile(img, cam, x, y, s):
    kit.feet_shadow(img, cam, x, y, s)
    sp = dict(STEVE)

    def head(p, L):
        p.poly([(40, 120), (100, 110), (104, 196), (44, 204)], (30, 30, 34), INK, 2.0)        # the chest camera
        p.ell(108, 156, 10, 16, (60, 64, 74), INK, 1.6)
        p.line([(0, -4), (60, 120)], STRAP, 9)
        S.profile_head(img, p, sp, -4, -150, mouth='grin')
        hy, hh = -150, sp['hh']
        p.poly(curve([(-80, hy - hh * 0.66), (-74, hy - hh * 1.2), (-10, hy - hh * 1.48), (60, hy - hh * 1.3), (84, hy - hh * 0.86),
                      (90, hy - hh * 0.66)], 4), HELMET, INK, 2.6)
        p.line([(-78, hy - hh * 0.72), (88, hy - hh * 0.72)], STRAP, 5)
        p.poly([(80, hy - hh * 0.88), (104, hy - hh * 0.88), (104, hy - hh * 0.62), (80, hy - hh * 0.62)], (50, 52, 58), INK, 1.8)
        p.ell(104, hy - hh * 0.75, 4, 9, (255, 240, 150), INK, 1.2)
        p.line([(-30, hy - hh * 0.66), (-24, hy + 20), (10, hy + hh * 1.02)], STRAP, 2.6)
    side_body(img, cam, x, y, s, sp, head)


def spokes_profile(img, cam, x, y, s):
    kit.feet_shadow(img, cam, x, y, s)
    sp = dict(SPOKES)

    def head(p, L):
        p.line([(30, -2), (66, 200)], sp['badge'], 6)
        p.poly([(52, 196), (84, 196), (84, 276), (52, 276)], (248, 248, 248), INK, 1.8)
        p.poly([(-30, -6), (46, -6), (70, 140), (20, 150)], sp['shirt'], INK, 2.0)
        S.profile_head(img, p, sp, -4, -150, mouth='line')
    side_body(img, cam, x, y, s, sp, head)


def storyboard(dst):
    def mid(name, frac=0.5):
        a, b = next((s[1], s[2]) for s in SHOTS if s[0] == name)
        return a + (b - a) * frac
    stills = [('1. Cold open: tumbling through the cyan clouds (title, gone by 1 s)', 0.5),
              ('1. "...eighth planet from the sun."', mid('open', 0.8)),
              ('2a. Press room: push-in; diagram, STEVE in the clouds', mid('press_wide', 0.3)),
              ('2b. Closer: "supercritical strata..." (first laugh)', mid('press_close', 0.6)),
              ('3a. The sea: paddling the red kayak', mid('kayak', 0.5)),
              ('3b. "...kayak to safety": round in circles', mid('circles', 0.5)),
              ('4. Reverse angle: the journalists; the winds question', mid('journalists', 0.55)),
              ('5. The huff; "Steve is a professional"', T['huff'] + 0.3),
              ('5. Her list: Oman, Suriname', mid('huff', 0.85)),
              ('6. The gale: roped, flapping, a peg into nothing', mid('gale', 0.5)),
              ('7. The diagram: STEVE in the hot layer', mid('diagram', 0.5)),
              ('8. Deeper: diamonds, wonder', mid('deeper', 0.6)),
              ('9. "WOW! This is why exploration..."', mid('wow', 0.4)),
              ('10. Push on the grin: tousled, sweat-sodden', mid('grin', 0.7)),
              ('11. The science editor: "No suit in existence..."', mid('editor', 0.5)),
              ('12. "A professional." STEVE at the core', mid('slowly', 0.85)),
              ('13. Tiny in the glow, thumbs up; hard cut to black', mid('end', 0.5))]
    S.sheet([(f'{n}  [{t:.1f} s]', frame_image(t)) for n, t in stills], dst, cols=6,
            title=f'A PROFESSIONAL: storyboard ({DUR:.0f} s, voices timed at Sam\'s pace until the recordings arrive)')


def main():
    mode = sys.argv[1]
    B.SS = 1
    if mode == 'times':
        for k, v in T.items():
            print(f'{k:8s} {v:6.2f}')
        for n, a, b in SHOTS:
            print(f'{n:12s} {a:6.2f} - {b:6.2f}  ({b - a:4.1f} s)')
    elif mode == 'stills':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for s in sys.argv[3:]:
            frame_image(float(s)).convert('RGB').save(os.path.join(out, f't{s}.png'))
    elif mode == 'sheet':
        storyboard(sys.argv[2])
    elif mode == 'model':
        model_sheet(sys.argv[2])


F.guard(B)   # every arm drawn is measured against the rig; a wrong one stops the render (guides/figure-rig.md)

if __name__ == '__main__':
    main()
