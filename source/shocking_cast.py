#!/usr/bin/env python3
"""Shocking Behaviour (TikTok satire): the five people, drawn from Sam's reference photos (references/shocking/).

Each likeness is its own head (face shape, hair, eyes, brows, nose, resting mouth) and outfit details; talking mouths
come from the series' lip-sync shapes. Bodies are the satire package's (views.person, front view). Hooked into
burnham by `who` in the person's dict, so everyone else is untouched.

    Farage     bright royal-blue suit, pale pink shirt, busy pink paisley tie, lapel badge; silver hair swept straight
               back from a high receding hairline, long ruddy face, heavy-lidded bulging eyes, deep smile lines
    Jenrick    navy suit, white shirt, green knitted tie, glasses (his Reform look); short mid-brown hair swept up,
               broad full face, small close-set eyes
    Tice       navy suit, white shirt, teal tie, Union Jack pin; big floppy sandy-ginger hair, long tanned face,
               strong jaw, pale blue eyes, crow's feet
    Braverman  pale grey skirt suit, white top, sparkly earrings; long dark-brown hair with caramel ends, parted off
               centre; slim face, arched brows
    Journalist 28, long blonde hair, a slightly prominent nose; white buttoned blouse, navy skirt, Reform lanyard,
               a small handbag on a thin black strap over her shoulder

Moods (sp['mood']): 'grin' (dancing), 'cool', 'neutral', 'contempt', 'fury', 'scared', 'alarm', 'upset', 'wtf'.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import mouths                    # noqa: E402
import traitors_cast as TC       # noqa: E402  (shared face parts: eye, brow, ears)
from traitors_cast import blend, dk, eye, brow, ears   # noqa: E402
from ed import INK, curve, oval  # noqa: E402

mouths.install(B)

TEETH = (250, 248, 240)
MOUTH_IN = (96, 30, 36)
REFORM = (18, 182, 207)          # Reform UK's turquoise


def talking(sp):
    m = sp.get('mouth', 'rest')
    return isinstance(m, str) and m.startswith('v:') and m != 'v:rest'


def brows(p, sp, fx, ey, gap, c, w, inner0, outer0, length):
    """Brows by mood: angry (inner ends down), worried (inner ends up), alarmed (both up), contempt (one up)."""
    mood = sp.get('mood', 'neutral')
    k = sp.get('strength', 1.0)
    for sgn in (-1, 1):
        inner, outer = inner0, outer0
        if mood == 'fury':
            inner, outer = inner + 9 * k, outer - 5 * k
        elif mood in ('scared', 'upset'):
            inner, outer = inner - 11 * k, outer + 3 * k
        elif mood in ('alarm', 'wtf'):
            inner, outer = inner - 8 * k, outer - 7 * k
        elif mood == 'contempt':
            inner, outer = (inner + 6, outer - 2) if sgn < 0 else (inner - 4, outer - 9)
        elif mood == 'grin':
            inner, outer = inner - 3, outer - 4
        elif mood == 'sing':                           # brows lifted, singing along
            inner, outer = inner - 7, outer - 5
        elif mood == 'bliss':                          # lost in the music: brows up and soft in the middle
            inner, outer = inner - 6, outer + 1
        elif mood == 'pout':                           # cool: brows down a touch, level
            inner, outer = inner + 3, outer + 1
        elif mood == 'smug':                           # cheeky: one brow cocked
            inner, outer = (inner + 2, outer) if sgn < 0 else (inner - 8, outer - 10)
        if mood == 'wtf' and sgn > 0:                  # one brow higher: 'what am I looking at'
            inner, outer = inner - 5, outer - 6
        brow(p, fx + sgn * gap, ey + sp.get('brow_dy', 0), sgn, c, w, inner, outer, length)


def rest_mouth(p, sp, fx, my, lip, width=24, lips=False):
    """The resting mouth for each mood (when not talking)."""
    mood = sp.get('mood', 'neutral')
    w = width
    if mood == 'grin':                                  # a wide open smile, top teeth showing
        shape = curve([(fx - w - 6, my - 4), (fx, my + 2), (fx + w + 6, my - 4), (fx + w * 0.6, my + 16), (fx, my + 22),
                       (fx - w * 0.6, my + 16)], 3)
        p.poly(shape, MOUTH_IN, INK, 2.0)
        p.poly(curve([(fx - w - 2, my - 2), (fx, my + 3), (fx + w + 2, my - 2), (fx + w * 0.6, my + 6), (fx, my + 9),
                      (fx - w * 0.6, my + 6)], 3), TEETH, None)
        p.line(shape, INK, 2.0)
        for sgn in (-1, 1):
            p.line([(fx + sgn * (w + 6), my - 4), (fx + sgn * (w + 11), my - 9)], INK, 1.6)
    elif mood == 'fury':                                # teeth bared, pulled wide and square
        shape = [(fx - w - 2, my - 6), (fx + w + 2, my - 6), (fx + w - 2, my + 16), (fx - w + 2, my + 16)]
        p.poly(curve(shape, 2), TEETH, INK, 2.2)
        p.line([(fx - w, my + 5), (fx + w, my + 5)], INK, 1.6)
        for k in range(-2, 3):
            p.line([(fx + k * w * 0.36, my - 5), (fx + k * w * 0.36, my + 15)], (200, 196, 186), 1.2)
    elif mood == 'contempt':                            # lip curled up on one side
        p.line(curve([(fx - w, my + 4), (fx - w * 0.2, my + 3), (fx + w * 0.5, my - 2), (fx + w + 2, my - 8)], 3), INK, 2.4)
        p.line([(fx + w + 2, my - 8), (fx + w + 8, my - 12)], INK, 1.6)
    elif mood == 'scared':                              # a wobbly, downturned mouth, just open
        shape = curve([(fx - w * 0.9, my + 8), (fx - w * 0.3, my - 2), (fx + w * 0.3, my - 1), (fx + w * 0.9, my + 9),
                       (fx + w * 0.3, my + 7), (fx - w * 0.3, my + 6)], 3)
        p.poly(shape, MOUTH_IN, INK, 2.0)
    elif mood == 'alarm':                               # pulled wide and tight, teeth together
        shape = [(fx - w, my), (fx + w, my), (fx + w * 0.9, my + 9), (fx - w * 0.9, my + 9)]
        p.poly(curve(shape, 2), TEETH, INK, 2.0)
        p.line([(fx - w * 0.9, my + 4.5), (fx + w * 0.9, my + 4.5)], INK, 1.3)
    elif mood in ('upset', 'shock'):                    # mouth fallen open
        p.poly(curve(oval(fx, my + 8, w * 0.55, 14, 14)), MOUTH_IN, INK, 2.0)
        p.line(curve([(fx - w * 0.4, my + 17), (fx, my + 14), (fx + w * 0.4, my + 17)], 3), (200, 90, 96), 2.0)
    elif mood == 'wtf':                                 # slack, slightly open, flat
        p.poly(curve([(fx - w * 0.6, my + 2), (fx + w * 0.6, my + 1), (fx + w * 0.4, my + 9), (fx - w * 0.4, my + 9)], 3),
               MOUTH_IN, INK, 1.8)
    elif mood == 'sing':                                # singing along: open, round-topped, top teeth showing
        shape = curve([(fx - w * 0.7, my), (fx, my - 5), (fx + w * 0.7, my), (fx + w * 0.5, my + 20), (fx, my + 26),
                       (fx - w * 0.5, my + 20)], 3)
        p.poly(shape, MOUTH_IN, INK, 2.0)
        p.poly(curve([(fx - w * 0.6, my), (fx, my - 4), (fx + w * 0.6, my), (fx, my + 5)], 3), TEETH, None)
        p.poly(curve(oval(fx, my + 19, w * 0.3, 5, 10)), (200, 96, 100), None)              # the tongue
        p.line(shape, INK, 2.0)
    elif mood == 'pout':                                # the cool pout: lips pushed out in a small rosebud
        p.poly(curve(oval(fx, my + 4, w * 0.42, 9, 14)), lip if lips else (200, 120, 110), INK, 1.9)
        p.line([(fx - w * 0.3, my + 4), (fx, my + 6), (fx + w * 0.3, my + 4)], INK, 1.8)
    elif mood == 'bliss':                               # eyes shut, a soft wide smile
        p.line(curve([(fx - w - 4, my - 7), (fx - w * 0.4, my + 9), (fx + w * 0.4, my + 9), (fx + w + 4, my - 7)], 3), INK, 2.6)
    elif mood == 'smug':                                # a lopsided, cheeky smile
        p.line(curve([(fx - w, my + 3), (fx - w * 0.2, my + 6), (fx + w * 0.5, my + 2), (fx + w + 4, my - 8)], 3), INK, 2.4)
        p.line([(fx + w + 4, my - 8), (fx + w + 9, my - 4)], INK, 1.6)
    else:                                               # neutral / cool: closed, a faint smile
        k = 0.6 if mood == 'neutral' else 0.2
        if lips:
            p.poly(curve([(fx - w, my + 2), (fx, my - 3), (fx + w, my + 2), (fx, my + 11)], 3), lip, INK, 1.6)
        p.line(curve([(fx - w, my + 1 - 4 * k), (fx, my + 4), (fx + w, my + 1 - 4 * k)], 3), INK, 2.2)


def mouth_or_talk(p, sp, fx, my, lip, width=24, lips=False):
    if talking(sp):
        mouths.draw(p, dict(sp, lips=lips, lip_c=lip), fx, my, sp['mouth'][2:])
    else:
        rest_mouth(p, sp, fx, my, lip, width, lips)


def eye_state(sp, lid=0.2, squint=0.0):
    mood = sp.get('mood', 'neutral')
    l = sp.get('lid', lid)
    if mood in ('fury', 'contempt'):
        l, squint = max(l, 0.32), 0.2
    elif mood in ('scared', 'alarm', 'upset', 'shock'):
        l, squint = 0.0, 0.0
    elif mood == 'grin':
        squint = 0.35
    elif mood == 'wtf':
        l = 0.35 if not sp.get('wide') else 0.0
    elif mood == 'sing':
        l, squint = 0.1, 0.15
    elif mood == 'pout':
        l = max(l, 0.38)                               # cool, heavy-lidded
    elif mood == 'smug':
        l, squint = max(l, 0.3), 0.25
    return dict(lid=l, look=sp.get('look', 0.0), squint=squint, closed=sp.get('blink', False) or mood == 'bliss',
                gaze_dy=sp.get('gaze_dy', 0.0))


def flush(p, sp, fx, fy, skin):
    """Fury reddens the face: a flat flush over the cheeks and forehead (flat colour, no glow)."""
    if sp.get('mood') == 'fury' and sp.get('red', 0) > 0:
        c = blend(skin, (214, 70, 60), 0.35 * sp['red'])
        for sgn in (-1, 1):
            p.poly(curve(oval(fx + sgn * 40, fy + 26, 20, 13, 12)), c, None)


# --------------------------------------------------------------------------------------------- Farage
# The recurring character: the most exacting likeness (Sam, 18 Oct), from refs farage-1..4. What makes him him:
# a long face tapering to a rounded chin with soft jowls at the jaw; big ears that stand out; silver hair with real
# volume, brushed up and back off the forehead into a rounded front, the temples receding (an M hairline), the sides
# brushed back over the ears; high arched brows; heavy hooded lids drooping at the outer corners over pale grey-blue
# eyes, pouches beneath; a long straight nose with a fleshy tip; deep parentheses from the nose wings past the mouth;
# a wide mouth, thin upper lip, fuller lower lip; forehead creases; the famous grin, all upper teeth.
F_SKIN = (234, 170, 140)
F_SKIN_D = (206, 134, 108)       # creases and folds
F_FLUSH = (226, 140, 118)        # the ruddy cheeks and nose
F_HAIR = (212, 210, 204)
F_HAIR_D = (164, 162, 158)
F_HAIR_L = (236, 234, 230)
F_BROW = (150, 134, 118)
F_IRIS = (128, 150, 162)
F_LIP = (190, 110, 100)


def farage_mouth(p, sp, fx, my):
    """His mouths: the big grin (all upper teeth), the pressed, downturned mouth at rest (ref 5: long and thin, the
    corners pulled down, the lower lip pushed up), contempt, fury."""
    mood = sp.get('mood', 'neutral')
    if talking(sp):
        mouths.draw(p, dict(sp, lips=True, lip_c=F_LIP), fx, my, sp['mouth'][2:])
        return
    if mood == 'grin':                                   # the caricaturists' grin: huge, ear to ear
        w = 41
        shape = curve([(fx - w, my - 10), (fx - w * 0.5, my - 3), (fx, my - 1), (fx + w * 0.5, my - 3), (fx + w, my - 10),
                       (fx + w * 0.74, my + 16), (fx + w * 0.34, my + 28), (fx - w * 0.34, my + 28), (fx - w * 0.74, my + 16)], 3)
        p.poly(shape, MOUTH_IN, INK, 2.4)
        teeth = curve([(fx - w + 5, my - 8), (fx - w * 0.5, my - 1), (fx, my + 1), (fx + w * 0.5, my - 1), (fx + w - 5, my - 8),
                       (fx + w * 0.7, my + 8), (fx + w * 0.3, my + 14), (fx - w * 0.3, my + 14), (fx - w * 0.7, my + 8)], 3)
        p.poly(teeth, TEETH, None)                       # one solid, even row of big upper teeth (Sam: no gaps)
        for x in (-30, -18, -6, 6, 18, 30):
            p.line([(fx + x, my + abs(x) * 0.12 - 1), (fx + x * 0.97, my + 13 - abs(x) * 0.16)], (206, 200, 188), 1.2)
        p.line(shape, INK, 2.4)
        for sgn in (-1, 1):                              # the corners dig deep into the cheeks
            p.line([(fx + sgn * w, my - 10), (fx + sgn * (w + 8), my - 17)], INK, 2.0)
        return
    if mood in ('neutral', 'cool'):                      # pressed and downturned, an upside-down U
        w = 32
        p.poly(curve([(fx - w * 0.62, my + 6), (fx, my + 3), (fx + w * 0.62, my + 6), (fx + w * 0.4, my + 15), (fx, my + 17),
                      (fx - w * 0.4, my + 15)], 3), blend(F_SKIN, F_LIP, 0.4), None)        # the lower lip pushed up
        p.line(curve([(fx - w, my + 10), (fx - w * 0.6, my + 3), (fx, my + 1), (fx + w * 0.6, my + 3), (fx + w, my + 10)], 3),
               INK, 2.6)
        p.line(curve([(fx - w * 0.45, my + 24), (fx, my + 20), (fx + w * 0.45, my + 24)], 3), dk(F_SKIN, 0.72), 1.8)
        return
    rest_mouth(p, sp, fx, my, F_LIP, width=30)


def farage_head(img, p, sp, t, hx, hy):
    hw, hh, skin = 66, 108, F_SKIN                       # a long oval (Sam, 18 Oct: 15% more oval)
    fx = hx + sp.get('turn', 0.0) * hw * 0.2
    fy = hy + 10 * sp.get('down', 0.0)
    mood = sp.get('mood', 'neutral')
    for sgn in (-1, 1):                                  # big ears that stand out, set a little high
        p.poly(curve(oval(hx + sgn * (hw + 7), hy - 2, 16, 30, 18)), skin, INK, 2.4)
        p.line(curve([(hx + sgn * (hw + 4), hy - 20), (hx + sgn * (hw + 14), hy - 12), (hx + sgn * (hw + 14), hy + 8),
                      (hx + sgn * (hw + 6), hy + 18)], 3), F_SKIN_D, 1.6)
    outline = curve([(hx - hw, hy - 16), (hx - hw * 0.92, hy - hh * 0.72), (hx - hw * 0.5, hy - hh * 1.02),
                     (hx + hw * 0.5, hy - hh * 1.02), (hx + hw * 0.92, hy - hh * 0.72), (hx + hw, hy - 16),
                     (hx + hw * 1.0, hy + hh * 0.34), (hx + hw * 0.88, hy + hh * 0.7),            # soft, rounded jaw
                     (hx + hw * 0.62, hy + hh * 0.98), (hx + hw * 0.3, hy + hh * 1.13), (hx, hy + hh * 1.17),
                     (hx - hw * 0.3, hy + hh * 1.13), (hx - hw * 0.62, hy + hh * 0.98), (hx - hw * 0.88, hy + hh * 0.7),
                     (hx - hw * 1.0, hy + hh * 0.34)], 4)
    face_c = skin
    if mood == 'fury':
        face_c = blend(skin, (222, 100, 86), 0.32 * sp.get('red', 1.0))
    p.poly(outline, face_c, INK, 2.6)
    sd = dk(face_c, 0.7)
    lift = -5 if mood in ('grin', 'alarm', 'wtf') else (3 if mood == 'fury' else 0)
    for k in range(3):                                   # long creases right across the forehead (ref 5)
        y = fy - 68 + 11 * k + lift
        p.line(curve([(fx - 44 + 3 * k, y + 3), (fx - 18, y - 1), (fx + 6, y + 1), (fx + 26, y - 2), (fx + 44 - 3 * k, y + 3)], 3),
               sd, 1.8)
    p.line([(fx - 6, fy - 34), (fx - 4, fy - 22)], sd, 1.6)                                   # between the brows
    p.line([(fx + 6, fy - 34), (fx + 4, fy - 22)], sd, 1.6)
    st = eye_state(sp, lid=0.36)
    grin = mood == 'grin' and sp.get('laugh') and not talking(sp)   # eyes squeezed shut only on a big laugh
    for sgn in (-1, 1):
        ex, ey = fx + sgn * 28, fy - 8
        if grin:                                         # squeezed shut into crescents, the cheeks bunched up
            p.line(curve([(ex - 15, ey + 2), (ex, ey - 7), (ex + 15, ey + 2)], 3), INK, 2.8)
            p.line(curve([(ex - 16, ey + 13), (ex, ey + 20), (ex + 16, ey + 12)], 3), sd, 2.2)
            p.line([(ex + sgn * 17, ey + 1), (ex + sgn * 27, ey - 4)], sd, 1.6)
            p.line([(ex + sgn * 17, ey + 5), (ex + sgn * 27, ey + 8)], sd, 1.6)
            continue
        eye(p, ex, ey, sgn, 17, 12, F_IRIS, st, dk(face_c, 0.9), liner=2.6)   # larger, not wider (Sam, 18 Oct)
        if not st['closed']:                             # the heavy lid fold, sloping down over the outer corner
            p.line(curve([(ex - sgn * 15, ey - 13), (ex - sgn * 2, ey - 17), (ex + sgn * 12, ey - 15),
                          (ex + sgn * 22, ey - 6), (ex + sgn * 26, ey + 3)], 3), INK, 2.4)
        # big puffy bags: a rounded pouch under each eye, and the crease running down across the cheek
        p.line(curve([(ex - 17, ey + 12), (ex - 4, ey + 21), (ex + 8, ey + 21), (ex + 19, ey + 12)], 3), sd, 2.2)
        p.line(curve([(ex + sgn * 16, ey + 16), (ex + sgn * 20, ey + 30), (ex + sgn * 18, ey + 42)], 3), sd, 1.6)   # cheek fold
    # low, straight brows sloping down at the outer ends (the 'sad' set of his eyes, ref 5)
    brows(p, sp, fx, fy - 26, 28, F_BROW, 6, -3, 6, 34)
    # a long nose, broad at the base, a fleshy rounded tip and flared wings
    p.line([(fx - 5, fy - 14), (fx - 8, fy + 24)], INK, 1.9)
    p.line(curve([(fx - 23, fy + 32), (fx - 18, fy + 41), (fx - 7, fy + 43), (fx, fy + 47), (fx + 7, fy + 43),
                  (fx + 18, fy + 41), (fx + 23, fy + 32)], 3), INK, 2.1)
    for sgn in (-1, 1):
        p.line(curve([(fx + sgn * 23, fy + 32), (fx + sgn * 25, fy + 22), (fx + sgn * 16, fy + 17)], 3), INK, 1.8)
    my = fy + 70                                         # a long upper lip
    wide = 1.15 if mood == 'grin' else 1.0
    for sgn in (-1, 1):                                  # the deep lines, nose wings to past the mouth corners
        p.line(curve([(fx + sgn * 24, fy + 28), (fx + sgn * 36 * wide, fy + 48), (fx + sgn * 42 * wide, fy + 70),
                      (fx + sgn * 40 * wide, fy + 92)], 3), sd, 2.6)
        p.line(curve([(hx + sgn * hw * 0.92, hy + hh * 0.66), (hx + sgn * hw * 0.76, hy + hh * 0.88),
                      (hx + sgn * hw * 0.62, hy + hh * 0.98)], 3), sd, 1.6)                     # jowl folds
    farage_mouth(p, sp, fx, my)
    # the hair: short, close to the head, brushed straight back; deep recesses at the temples (ref 5)
    top = hy - hh - 10
    hair = [(hx - hw - 1, hy - 6), (hx - hw - 4, hy - 50), (hx - hw * 0.94, top + 30), (hx - hw * 0.6, top + 4),
            (hx, top - 2), (hx + hw * 0.6, top + 4), (hx + hw * 0.94, top + 30), (hx + hw + 4, hy - 50),
            (hx + hw + 1, hy - 6), (hx + hw - 5, hy - 34), (hx + hw * 0.86, hy - hh * 0.58),
            (hx + hw * 0.66, hy - hh * 0.8), (hx + hw * 0.5, hy - hh * 0.9),                # the deep temple recess
            (hx + hw * 0.3, hy - hh * 0.84), (hx, hy - hh * 0.78), (hx - hw * 0.3, hy - hh * 0.84),
            (hx - hw * 0.5, hy - hh * 0.9), (hx - hw * 0.66, hy - hh * 0.8), (hx - hw * 0.86, hy - hh * 0.58),
            (hx - hw + 5, hy - 34)]
    p.poly(curve(hair, 4), F_HAIR, INK, 2.6)
    for k in range(5):                                   # combed straight back
        x0 = hx - hw * 0.36 + k * hw * 0.18
        p.line(curve([(x0, hy - hh * 0.82), (x0 + 1, hy - hh * 0.95), (x0 + 3, top + 12)], 3)[:-2], F_HAIR_D, 1.5)
    for sgn in (-1, 1):
        p.line(curve([(hx + sgn * hw * 0.88, hy - hh * 0.52), (hx + sgn * (hw - 2), hy - hh * 0.7),
                      (hx + sgn * hw * 0.8, top + 26)], 3)[:-2], F_HAIR_D, 1.4)
    return fx


def farage_torso(img, p, sp, t):
    for sgn in (-1, 1):                                  # the cords and folds of his neck above the collar
        p.line([(sgn * 12, -78), (sgn * 18, -24)], F_SKIN_D, 1.6)
    p.line(curve([(-16, -40), (0, -34), (16, -40)], 3), F_SKIN_D, 1.4)
    tie = sp.get('tie', (226, 140, 170))
    p.poly([(-12, 16), (12, 16), (16, 200), (0, 226), (-16, 200)], tie, INK, 2.0)
    p.poly([(-12, -2), (12, -2), (9, 18), (-9, 18)], tie, INK, 2.0)
    rng = np.random.default_rng(3)
    for _ in range(14):                                 # paisley: small teardrops in two colours
        x, y = rng.uniform(-9, 9), rng.uniform(24, 196)
        c = (132, 72, 120) if rng.random() < 0.5 else (240, 200, 150)
        p.ell(x, y, 3, 4.5, c, None, rot=rng.uniform(0, 3))
    jc = sp.get('jacket')
    for sgn in (-1, 1):
        p.poly([(sgn * 44, -2), (sgn * 70, 30), (sgn * 46, 110), (sgn * 62, 150), (sgn * 4, 250), (sgn * 22, 150)],
               jc, INK, 2.2)
    p.ell(-58, 100, 6, 6, (226, 196, 90), INK, 1.2)     # the small lapel badge


# --------------------------------------------------------------------------------------------- Jenrick
J_SKIN = (244, 202, 176)
J_HAIR = (112, 80, 54)
J_HAIR_D = (80, 56, 38)


def jenrick_head(img, p, sp, t, hx, hy):
    hw, hh, skin = 80, 90, J_SKIN
    fx = hx + sp.get('turn', 0.0) * hw * 0.2
    fy = hy + 10 * sp.get('down', 0.0)
    ears(p, hx, hy + 8, hw, skin)
    outline = curve([(hx - hw, hy - 10), (hx - hw * 0.88, hy - hh * 0.72), (hx - hw * 0.42, hy - hh * 1.02),
                     (hx + hw * 0.42, hy - hh * 1.02), (hx + hw * 0.88, hy - hh * 0.72), (hx + hw, hy - 10),
                     (hx + hw * 1.04, hy + hh * 0.42), (hx + hw * 0.88, hy + hh * 0.82), (hx + hw * 0.5, hy + hh * 1.06),
                     (hx, hy + hh * 1.12), (hx - hw * 0.5, hy + hh * 1.06), (hx - hw * 0.88, hy + hh * 0.82),
                     (hx - hw * 1.04, hy + hh * 0.42)], 4)
    p.poly(outline, skin, INK, 2.6)
    sd = dk(skin, 0.85)
    for sgn in (-1, 1):                                 # full cheeks
        p.line(curve([(fx + sgn * 52, fy + 20), (fx + sgn * 46, fy + 44), (fx + sgn * 36, fy + 58)], 3), sd, 1.6)
    st = eye_state(sp, lid=0.18)
    for sgn in (-1, 1):                                 # small, close-set eyes behind the glasses
        ex, ey = fx + sgn * 25, fy - 4
        eye(p, ex, ey, sgn, 11, 6, (96, 110, 120), st, dk(skin, 0.88), liner=2.4)
        if sp.get('mood') == 'grin':
            p.line([(ex + sgn * 14, ey + 2), (ex + sgn * 20, ey - 2)], sd, 1.3)
            p.line([(ex + sgn * 14, ey + 6), (ex + sgn * 20, ey + 8)], sd, 1.3)
    brows(p, sp, fx, fy - 26, 25, J_HAIR_D, 5, 0, -2, 26)
    for sgn in (-1, 1):                                 # the glasses: dark rounded-rectangle frames, a bridge
        ex, ey = fx + sgn * 26, fy - 4
        fr = curve([(ex - 20, ey - 13), (ex + 20, ey - 13), (ex + 21, ey + 11), (ex - 21, ey + 11)], 3)
        p.line(fr + [fr[0]], (40, 34, 30), 3.6)
        p.line([(ex + sgn * 21, ey - 8), (hx + sgn * (hw - 2), fy - 10)], (40, 34, 30), 3.0)
    p.line([(fx - 6, fy - 10), (fx, fy - 13), (fx + 6, fy - 10)], (40, 34, 30), 3.2)
    p.line([(fx - 2, fy + 4), (fx - 6, fy + 26), (fx + 1, fy + 31), (fx + 9, fy + 28)], INK, 1.8)     # a small nose
    my = fy + 52
    mouth_or_talk(p, sp, fx, my, (204, 132, 120), width=22)
    # short mid-brown hair swept up and back, a slight side parting, thin at the temples
    top = hy - hh - 16
    hair = [(hx - hw - 4, hy - 4), (hx - hw - 6, hy - 46), (hx - hw * 0.94, top + 36), (hx - hw * 0.6, top + 4),
            (hx - hw * 0.1, top - 6), (hx + hw * 0.44, top - 2), (hx + hw * 0.86, top + 18), (hx + hw + 6, hy - 50),
            (hx + hw + 4, hy - 4), (hx + hw - 6, hy - 40), (hx + hw * 0.76, hy - hh * 0.7), (hx + hw * 0.4, hy - hh * 0.86),
            (hx - hw * 0.2, hy - hh * 0.9), (hx - hw * 0.62, hy - hh * 0.86), (hx - hw * 0.82, hy - hh * 0.66),
            (hx - hw + 6, hy - 40)]
    p.poly(curve(hair, 4), J_HAIR, INK, 2.6)
    p.line(curve([(hx - hw * 0.42, hy - hh * 0.9), (hx - hw * 0.36, top + 20), (hx - hw * 0.3, top + 2)], 3)[:8], J_HAIR_D, 1.6)
    for k in range(4):
        x0 = hx - hw * 0.24 + k * hw * 0.2
        p.line(curve([(x0, hy - hh * 0.9), (x0 + 8, top + 16), (x0 + 16, top + 8)], 3)[:8], J_HAIR_D, 1.3)
    return fx


def knitted_tie(p, sp, tie):
    p.poly([(-12, 16), (12, 16), (13, 196), (-13, 196)], tie, INK, 2.0)   # a knitted tie: square end
    p.poly([(-12, -2), (12, -2), (9, 18), (-9, 18)], tie, INK, 2.0)
    for k in range(8):
        p.line([(-11, 34 + 20 * k), (11, 34 + 20 * k)], dk(tie, 0.78), 1.2)


def lapels(p, sp):
    for sgn in (-1, 1):
        p.poly([(sgn * 44, -2), (sgn * 70, 30), (sgn * 46, 110), (sgn * 62, 150), (sgn * 4, 250), (sgn * 22, 150)],
               sp.get('jacket'), INK, 2.2)


def jenrick_torso(img, p, sp, t):
    knitted_tie(p, sp, sp.get('tie', (40, 104, 64)))
    lapels(p, sp)


# --------------------------------------------------------------------------------------------- Tice
T_SKIN = (230, 164, 124)
T_HAIR = (178, 124, 72)
T_HAIR_L = (206, 160, 104)
T_HAIR_D = (132, 88, 50)


def tice_head(img, p, sp, t, hx, hy):
    hw, hh, skin = 72, 98, T_SKIN
    fx = hx + sp.get('turn', 0.0) * hw * 0.2
    fy = hy + 10 * sp.get('down', 0.0)
    ears(p, hx, hy + 8, hw, skin)
    outline = curve([(hx - hw, hy - 12), (hx - hw * 0.9, hy - hh * 0.72), (hx - hw * 0.45, hy - hh * 1.02),
                     (hx + hw * 0.45, hy - hh * 1.02), (hx + hw * 0.9, hy - hh * 0.72), (hx + hw, hy - 12),
                     (hx + hw * 1.0, hy + hh * 0.5), (hx + hw * 0.9, hy + hh * 0.86), (hx + hw * 0.5, hy + hh * 1.1),
                     (hx, hy + hh * 1.14), (hx - hw * 0.5, hy + hh * 1.1), (hx - hw * 0.9, hy + hh * 0.86),
                     (hx - hw * 1.0, hy + hh * 0.5)], 4)                       # long, with a strong square jaw
    p.poly(outline, skin, INK, 2.6)
    sd = dk(skin, 0.8)
    st = eye_state(sp, lid=0.22)
    for sgn in (-1, 1):
        ex, ey = fx + sgn * 28, fy - 6
        eye(p, ex, ey, sgn, 14, 8, (130, 176, 214), st, dk(skin, 0.88), liner=2.4)
        for k in range(3):                              # crow's feet, fanning out
            p.line([(ex + sgn * 18, ey - 2 + 5 * k), (ex + sgn * 28, ey - 6 + 9 * k)], sd, 1.3)
        p.line([(ex - 11, ey + 11), (ex, ey + 14), (ex + 11, ey + 11)], sd, 1.3)
    brows(p, sp, fx, fy - 28, 28, T_HAIR_D, 5, 0, -2, 28)
    p.line([(fx - 2, fy - 6), (fx - 6, fy + 30), (fx + 1, fy + 35), (fx + 10, fy + 31)], INK, 1.9)
    for sgn in (-1, 1):
        p.line(curve([(fx + sgn * 20, fy + 34), (fx + sgn * 34, fy + 56), (fx + sgn * 36, fy + 74)], 3), sd, 1.8)
        p.line([(hx + sgn * hw * 0.9, hy + hh * 0.5), (hx + sgn * hw * 0.8, hy + hh * 0.84)], sd, 1.4)
    my = fy + 60
    mouth_or_talk(p, sp, fx, my, (200, 120, 104), width=27)
    # the big floppy mop: lots of volume on top, swept back and over to our right, a lock falling forward
    top = hy - hh - 40
    hair = [(hx - hw - 8, hy + 10), (hx - hw - 18, hy - 40), (hx - hw - 14, top + 60), (hx - hw * 0.7, top + 14),
            (hx - hw * 0.1, top - 4), (hx + hw * 0.6, top + 4), (hx + hw + 14, top + 34), (hx + hw + 22, hy - 60),
            (hx + hw + 12, hy + 6), (hx + hw - 4, hy - 30), (hx + hw * 0.74, hy - hh * 0.62),
            (hx + hw * 0.3, hy - hh * 0.72), (hx - hw * 0.1, hy - hh * 0.64), (hx - hw * 0.34, hy - hh * 0.5),
            (hx - hw * 0.44, hy - hh * 0.66), (hx - hw * 0.74, hy - hh * 0.7), (hx - hw + 4, hy - 30)]
    p.poly(curve(hair, 4), T_HAIR, INK, 2.6)
    for k in range(6):                                  # strands swept up and over
        x0 = hx - hw * 0.8 + k * hw * 0.26
        p.line(curve([(x0, hy - hh * 0.62), (x0 + 12, top + 34), (x0 + 26, top + 18)], 3)[:9],
               T_HAIR_L if k % 2 else T_HAIR_D, 1.6)
    p.line(curve([(hx - hw * 0.1, hy - hh * 0.9), (hx - hw * 0.3, hy - hh * 0.62), (hx - hw * 0.38, hy - hh * 0.52)], 3),
           T_HAIR_D, 1.6)                                # the lock flopping forward
    return fx


def tice_torso(img, p, sp, t):
    tie = sp.get('tie', (34, 150, 150))
    p.poly([(-12, 16), (12, 16), (16, 200), (0, 226), (-16, 200)], tie, INK, 2.0)
    p.poly([(-12, -2), (12, -2), (9, 18), (-9, 18)], tie, INK, 2.0)
    for k in range(6):
        p.line([(-12, 40 + 28 * k), (12, 52 + 28 * k)], dk(tie, 0.8), 1.2)
    lapels(p, sp)
    x, y = -60, 96                                      # the Union Jack pin
    p.poly([(x - 10, y - 6), (x + 10, y - 6), (x + 10, y + 6), (x - 10, y + 6)], (36, 50, 120), INK, 1.2)
    p.line([(x - 10, y - 6), (x + 10, y + 6)], (240, 240, 240), 2.2)
    p.line([(x - 10, y + 6), (x + 10, y - 6)], (240, 240, 240), 2.2)
    p.line([(x - 10, y), (x + 10, y)], (200, 30, 44), 2.4)
    p.line([(x, y - 6), (x, y + 6)], (200, 30, 44), 2.4)


# --------------------------------------------------------------------------------------------- long hair (one shape)
def _edge(x_of, y0, y1, n, amp, phase=0.0):
    """Points down a softly waving edge: x_of(u) the base line plus a gentle S."""
    return [(x_of(k / n) + amp * math.sin(phase + k / n * math.pi * 2.6), y0 + (y1 - y0) * k / n) for k in range(n + 1)]


def _lock(hx, hy, hw, hh, sgn, length, wave, u0=0.0):
    """One long lock falling past the shoulder from up inside the crown, tapering to an uneven point (never a
    rounded end). u0 > 0 gives only the part of the lock below that fraction (its lighter ends), on the same edges."""
    outer = lambda u: hx + sgn * (hw + 20 + 22 * math.sin(u * math.pi * 0.85))
    inner = lambda u: hx + sgn * (hw * 0.84 + 10 * math.sin(u * math.pi * 0.9) - 6 * u)
    y0o, y0i, y1 = hy - hh * 0.55, hy + 10, hy + length
    n = 14
    o = [pt for pt in _edge(outer, y0o, y1, n, wave * sgn, 0.0) if (pt[1] - y0o) / (y1 - y0o) >= u0]
    i = [pt for pt in _edge(inner, y0i, y1 - 14, n, wave * 0.7 * sgn, 0.9) if (pt[1] - y0i) / (y1 - 14 - y0i) >= u0 + (0.14 if u0 else 0)]
    tip = [(hx + sgn * (hw + 30), y1 + 26), (hx + sgn * (hw + 16), y1 + 12), (hx + sgn * (hw + 6), y1 + 30)]
    head = [] if u0 > 0 else [(hx + sgn * hw * 0.55, hy - hh * 0.72)]
    return curve(head + i + tip[::-1] + o[::-1], 3)


def _crown(hx, hy, hw, hh, part, top=26):
    """The crown, its lower edge the hairline across the forehead from the parting."""
    outer = oval(hx, hy - 8, hw + 22, hh + top, 22, math.pi * 0.97, math.pi * 2.03)
    line = [(hx + hw + 16, hy + 30), (hx + hw * 0.92, hy - hh * 0.3), (hx + hw * 0.62, hy - hh * 0.72),
            (part + hw * 0.22, hy - hh * 0.88), (part, hy - hh * 1.0), (part - hw * 0.22, hy - hh * 0.86),
            (hx - hw * 0.68, hy - hh * 0.64), (hx - hw * 0.94, hy - hh * 0.2), (hx - hw - 16, hy + 30)]
    return curve(outer + line, 3), curve(line, 3)[7:-7]


def long_hair_front(p, hx, hy, hw, hh, part, col, dark, length=270, ends=None, wave=8):
    """Locks and crown as ONE shape with ONE outline (Sam, 16 Oct): every piece outlined first, then every fill laid
    on top, so no seam or second layer shows. Lighter ends (balayage) are a fill inside the same edges, no outline.
    Drawn before the face; the crown and hairline go over the face after (long_hair_top)."""
    pieces = [_lock(hx, hy, hw, hh, sgn, length, wave) for sgn in (-1, 1)] + [_crown(hx, hy, hw, hh, part)[0]]
    for pts in pieces:
        p.poly(pts, col, INK, 5.2)
    for pts in pieces:
        p.poly(pts, col, None)
    if ends:
        for sgn in (-1, 1):
            p.poly(_lock(hx, hy, hw, hh, sgn, length, wave, u0=0.66), ends, None)
    for sgn in (-1, 1):                                  # two soft strands inside each lock, never past its edge
        for k in range(2):
            line = _edge(lambda u: hx + sgn * (hw + 12 + 8 * k + 16 * math.sin(u * math.pi * 0.85)), hy + 30 + 30 * k,
                         hy + length - 40 - 30 * k, 8, wave * 0.8 * sgn, 0.3)
            p.line(line, dark, 1.5)


def long_hair_top(p, hx, hy, hw, hh, part, col, dark):
    shape, line = _crown(hx, hy, hw, hh, part)
    p.poly(shape, col, None)
    p.line(line, INK, 2.6)
    p.line([(part, hy - hh * 1.22), (part + 3, hy - hh * 1.0)], dark, 2.0)
    for k in range(2):
        p.line(curve([(part + 14 + 16 * k, hy - hh * 1.16 + 8 * k), (hx + hw * 0.7 + 6 * k, hy - hh * 0.9 + 12 * k),
                      (hx + hw + 4, hy - hh * 0.3 + 10 * k)], 3)[:-3], dark, 1.5)
        p.line(curve([(part - 12 - 12 * k, hy - hh * 1.14 + 8 * k), (hx - hw * 0.7 - 6 * k, hy - hh * 0.86 + 12 * k),
                      (hx - hw - 4, hy - hh * 0.3 + 10 * k)], 3)[:-3], dark, 1.5)


def hair_mass(p, hx, hy, hw, hh, col, length):
    """The back of the hair, seen only in the gap behind the neck: kept inside the front locks' outline so no
    second edge ever shows round them."""
    p.poly([(hx - hw - 4, hy - hh * 0.3), (hx + hw + 4, hy - hh * 0.3), (hx + hw + 4, hy + length - 20),
            (hx - hw - 4, hy + length - 20)], col, None)


# --------------------------------------------------------------------------------------------- Braverman
S_SKIN = (182, 124, 92)
S_HAIR = (52, 36, 28)
S_HAIR_D = (34, 24, 18)
S_HAIR_L = (104, 72, 48)         # the caramel ends, inside the same outline
S_LIP = (156, 88, 80)


def braverman_hair_back(p, sp, hx, hy, hw, hh):
    hair_mass(p, hx, hy, hw, hh, S_HAIR_D, 250)


def braverman_head(img, p, sp, t, hx, hy):
    hw, hh, skin = 60, 88, S_SKIN
    fx = hx + sp.get('turn', 0.0) * hw * 0.2
    fy = hy + 10 * sp.get('down', 0.0)
    part = hx - hw * 0.22                               # parted a little off centre (our left)
    long_hair_front(p, hx, hy, hw, hh, part, S_HAIR, S_HAIR_D, length=250, ends=S_HAIR_L, wave=6)
    outline = curve([(hx - hw, hy - 10), (hx - hw * 0.9, hy - hh * 0.7), (hx - hw * 0.45, hy - hh * 1.04),
                     (hx + hw * 0.45, hy - hh * 1.04), (hx + hw * 0.9, hy - hh * 0.7), (hx + hw, hy - 10),
                     (hx + hw * 0.98, hy + hh * 0.4), (hx + hw * 0.7, hy + hh * 0.9), (hx + hw * 0.26, hy + hh * 1.1),
                     (hx, hy + hh * 1.12), (hx - hw * 0.26, hy + hh * 1.1), (hx - hw * 0.7, hy + hh * 0.9),
                     (hx - hw * 0.98, hy + hh * 0.4)], 4)
    p.poly(outline, skin, INK, 2.6)
    st = eye_state(sp, lid=0.14)
    for sgn in (-1, 1):
        eye(p, fx + sgn * 25, fy - 4, sgn, 16, 9, (46, 30, 24), st, dk(skin, 0.85), liner=3.2, lower=1.8, lashes=True)
    brows(p, sp, fx, fy - 27, 25, (40, 28, 22), 5, 2, -6, 26)              # neatly arched
    p.line([(fx - 2, fy), (fx - 5, fy + 26), (fx, fy + 31), (fx + 7, fy + 29)], INK, 1.7)
    for sgn in (-1, 1):
        p.line([(fx + sgn * 40, fy + 12), (fx + sgn * 34, fy + 34)], dk(skin, 0.88), 1.4)   # cheekbones
    my = fy + 52
    mouth_or_talk(p, sp, fx, my, S_LIP, width=19, lips=True)
    long_hair_top(p, hx, hy, hw, hh, part, S_HAIR, S_HAIR_D)
    for sgn in (-1, 1):                                  # sparkly earrings, just showing under the hair
        x, y = hx + sgn * (hw - 2), hy + 30
        p.ell(x, y, 5, 5, (236, 230, 220), INK, 1.3)
    return fx


def braverman_torso(img, p, sp, t):
    p.poly([(-40, -4), (40, -4), (34, 140), (0, 236), (-34, 140)], (248, 246, 242), INK, 2.0)     # white top, round neck
    p.poly(curve(oval(0, -2, 34, 16, 16, 0.1, math.pi - 0.1), 3) + [(0, -2)], sp['skin'], None)
    p.line(curve(oval(0, -2, 34, 16, 16, 0.1, math.pi - 0.1), 3), INK, 1.8)
    for sgn in (-1, 1):                                  # the pale grey jacket's lapels
        p.poly([(sgn * 40, -2), (sgn * 70, 30), (sgn * 52, 110), (sgn * 62, 150), (sgn * 30, 240), (sgn * 36, 150)],
               sp.get('jacket'), INK, 2.2)


# --------------------------------------------------------------------------------------------- the journalist
N_SKIN = (246, 214, 194)
N_HAIR = (232, 200, 124)
N_HAIR_D = (196, 158, 88)
N_LIP = (214, 140, 140)


def journalist_hair_back(p, sp, hx, hy, hw, hh):
    hair_mass(p, hx, hy, hw, hh, N_HAIR_D, 270)


def shock_eye(p, ex, ey, sgn, w, h, look=0.0):
    """Wide with shock (South Park): a big white opening, no lid over it, a tiny pupil."""
    p.poly(curve(oval(ex, ey, w, h, 20)), (252, 252, 250), INK, 2.4)
    p.ell(ex + look * w * 0.35, ey + 1, 3.4, 3.4, INK, None)
    p.line([(ex + sgn * w * 0.9, ey - h * 0.5), (ex + sgn * (w + 5), ey - h * 0.8)], INK, 1.8)     # a lash


def journalist_head(img, p, sp, t, hx, hy):
    hw, hh, skin = 60, 88, N_SKIN
    fx = hx + sp.get('turn', 0.0) * hw * 0.2
    fy = hy + 10 * sp.get('down', 0.0)
    part = hx + hw * 0.3                                # side parting (our right)
    long_hair_front(p, hx, hy, hw, hh, part, N_HAIR, N_HAIR_D, length=270, wave=9)
    outline = curve([(hx - hw, hy - 10), (hx - hw * 0.9, hy - hh * 0.7), (hx - hw * 0.45, hy - hh * 1.04),
                     (hx + hw * 0.45, hy - hh * 1.04), (hx + hw * 0.9, hy - hh * 0.7), (hx + hw, hy - 10),
                     (hx + hw * 0.96, hy + hh * 0.44), (hx + hw * 0.66, hy + hh * 0.92), (hx + hw * 0.24, hy + hh * 1.1),
                     (hx, hy + hh * 1.12), (hx - hw * 0.24, hy + hh * 1.1), (hx - hw * 0.66, hy + hh * 0.92),
                     (hx - hw * 0.96, hy + hh * 0.44)], 4)
    p.poly(outline, skin, INK, 2.6)
    st = eye_state(sp, lid=0.12)
    shock = sp.get('mood') == 'wtf'
    for sgn in (-1, 1):
        if shock and not st['closed']:
            shock_eye(p, fx + sgn * 25, fy - 8, sgn, 19, 16, st['look'])
        else:
            eye(p, fx + sgn * 25, fy - 6, sgn, 15, 9, (92, 132, 170), st, dk(skin, 0.88), liner=2.8, lower=1.6,
                lashes=True)
    if shock:
        for sgn in (-1, 1):                              # high, tilted up in the middle (worried disbelief)
            p.line([(fx + sgn * 10, fy - 36), (fx + sgn * 38, fy - 30)], (150, 116, 70), 4.6)
    else:
        brows(p, sp, fx, fy - 29, 25, (176, 140, 90), 4.5, 0, -3, 25)
    # a slightly prominent nose: longer, a defined bridge and a rounded tip
    p.line([(fx - 3, fy - 4), (fx - 8, fy + 28)], INK, 1.8)
    p.line(curve([(fx - 10, fy + 26), (fx - 6, fy + 36), (fx + 4, fy + 38), (fx + 12, fy + 33), (fx + 8, fy + 27)], 3), INK, 1.8)
    p.line([(fx - 13, fy + 32), (fx - 9, fy + 35)], INK, 1.3)
    my = fy + 57
    if shock and not talking(sp):                       # hanging open: a dark shape, the top edge drooping
        k = sp.get('gape', 1.0)
        p.poly(curve([(fx - 15, my + 6), (fx - 6, my + 1), (fx, my + 2), (fx + 6, my + 1), (fx + 15, my + 6),
                      (fx + 13, my + 6 + 12 * k), (fx, my + 8 + 15 * k), (fx - 13, my + 6 + 12 * k)], 3),
               (40, 20, 24), INK, 2.0)
    else:
        mouth_or_talk(p, sp, fx, my, N_LIP, width=19, lips=True)
    long_hair_top(p, hx, hy, hw, hh, part, N_HAIR, N_HAIR_D)
    return fx


def journalist_torso(img, p, sp, t):
    """A white buttoned blouse (collar, a placket of buttons); the Reform lanyard round her neck with its card."""
    p.poly([(-sp['shoulders'] + 8, 0), (sp['shoulders'] - 8, 0), (sp['shoulders'], 50), (sp['shoulders'] - 6, 420),
            (-sp['shoulders'] + 6, 420), (-sp['shoulders'], 50)], (250, 250, 248), None)
    for sgn in (-1, 1):                                  # the collar points
        p.poly([(sgn * 6, 20), (sgn * 40, -6), (sgn * 54, 4), (sgn * 30, 44)], (252, 252, 250), INK, 1.8)
    p.line([(0, 20), (0, 420)], (214, 214, 214), 1.6)
    for k in range(5):
        p.ell(6, 60 + 70 * k, 3.5, 3.5, (226, 226, 226), INK, 1.0)
    for sgn in (-1, 1):                                  # the lanyard
        p.line([(sgn * 30, -60), (sgn * 26, 40), (sgn * 6, 170)], REFORM, 6)
    p.poly([(-34, 170), (34, 170), (34, 250), (-34, 250)], (250, 250, 250), INK, 1.6)    # the pass
    p.poly([(-34, 170), (34, 170), (34, 194), (-34, 194)], REFORM, INK, 1.4)
    p.poly([(-24, 204), (-2, 204), (-2, 236), (-24, 236)], (200, 200, 206), None)
    for k in range(3):
        p.line([(4, 208 + 10 * k), (26 - 6 * k, 208 + 10 * k)], (150, 150, 156), 2.0)
    skirt(p, sp, top=392)                                # the blouse tucked into the skirt at the waist
    handbag(p, sp)


def handbag(p, sp, side=-1):
    """A small handbag on a thin black strap over her shoulder, hanging at her hip (Sam, 18 Oct: not held)."""
    sw = sp['shoulders']
    x, y = side * (sw + 6), 470
    p.line([(side * (sw - 30), -2), (side * (sw - 6), 120), (x - side * 20, y - 6)], (20, 18, 20), 2.6)
    p.poly(curve([(x - 40, y), (x + 40, y), (x + 46, y + 64), (x - 46, y + 64)], 2), (36, 34, 48), INK, 2.2)
    p.line([(x - 40, y + 16), (x + 40, y + 16)], (70, 66, 84), 1.6)
    p.ell(x, y + 18, 5, 4, (200, 176, 110), INK, 1.0)


# --------------------------------------------------------------------------------------------- skirts
def skirt(p, sp, top=400):
    """A straight skirt from the waist to the knee (Sam, 18 Oct: start higher, end higher), front view."""
    c = sp.get('skirt')
    w = sp['shoulders'] - 26
    p.poly(curve([(-w, top), (w, top), (w + 14, 690), (-w - 14, 690)], 2), c, INK, 2.4)
    p.line([(-w - 6, 640), (-w * 0.2, 690)], dk(c, 0.8), 1.4)
    if sp.get('who') == 'journalist':                    # the waistband over the tucked-in blouse
        p.line([(-w, top + 8), (w, top + 8)], dk(c, 0.75), 1.6)


# --------------------------------------------------------------------------------------------- the hooks
HEADS = {'farage': farage_head, 'jenrick': jenrick_head, 'tice': tice_head, 'braverman': braverman_head,
         'journalist': journalist_head}
TORSOS = {'farage': farage_torso, 'jenrick': jenrick_torso, 'tice': tice_torso, 'braverman': braverman_torso,
          'journalist': journalist_torso}
BACKS = {'braverman': braverman_hair_back, 'journalist': journalist_hair_back}
_head, _torso = B.head, B.torso


def head(img, p, sp, t, hx, hy):
    f = HEADS.get(sp.get('who'))
    return f(img, p, sp, t, hx, hy) if f else _head(img, p, sp, t, hx, hy)


def torso(img, p, sp, t):
    who = sp.get('who')
    if who in BACKS:                                     # long hair falls behind the shoulders
        BACKS[who](p, sp, sp.get('head_dx', 0.0), -150 + sp.get('head_dy', 0), sp.get('hw', 60), sp.get('hh', 88))
    if sp.get('skirt') and who != 'journalist':
        skirt(p, sp)                                     # under the jacket, which ends at the waist
    _torso(img, p, sp, t)
    f = TORSOS.get(who)
    if f:
        f(img, p, sp, t)


B.head, B.torso = head, torso

FARAGE = dict(who='farage', name='Farage', skin=F_SKIN, hw=70, hh=100, head_dy=6, outfit='suit', jacket=(46, 96, 196),
              shirt=(246, 214, 220), tie=(226, 140, 170), shoulders=150, trousers=(46, 96, 196), full=True, pose='custom')
JENRICK = dict(who='jenrick', name='Jenrick', skin=J_SKIN, hw=80, hh=90, head_dy=12, outfit='suit', jacket=(34, 42, 72),
               shirt=(246, 246, 244), tie=(40, 104, 64), shoulders=150, trousers=(34, 42, 72), full=True, pose='custom')
TICE = dict(who='tice', name='Tice', skin=T_SKIN, hw=72, hh=98, head_dy=8, outfit='suit', jacket=(30, 38, 66),
            shirt=(246, 246, 244), tie=(34, 150, 150), shoulders=156, trousers=(30, 38, 66), full=True, pose='custom')
BRAVERMAN = dict(who='braverman', name='Braverman', skin=S_SKIN, hw=60, hh=88, head_dy=10, outfit='suit',
                 jacket=(206, 204, 198), shirt=(248, 246, 242), shoulders=128, skirt=(196, 194, 188), trousers=S_SKIN,
                 bottom=430,
                 shoe=(40, 36, 40), full=True, pose='custom')
JOURNALIST = dict(who='journalist', name='Journalist', skin=N_SKIN, hw=60, hh=88, head_dy=10, outfit='blouse',
                  jacket=(250, 250, 248), shirt=(250, 250, 248), shoulders=124, skirt=(34, 44, 84), trousers=N_SKIN,
                  bottom=420,
                  shoe=(30, 30, 40), full=True, pose='custom')
CAST = {'farage': FARAGE, 'jenrick': JENRICK, 'tice': TICE, 'braverman': BRAVERMAN, 'journalist': JOURNALIST}
