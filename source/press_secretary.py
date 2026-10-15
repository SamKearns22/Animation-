"""The New Press Secretary (working title): one slow push-in on the new White House press secretary's first
briefing. She reads near-gibberish from her notes, keeps looking down at them, flashes big strange smiles at the room,
and ends on a huge flat sigh and "...Venezuela." Silent for now (Sam records the voice later). Brief:
prompts/press-secretary.md. Satire style (flat colour, one outline, hand-cut shapes, circle hands).

    python3 source/press_secretary.py cast OUT.png           her, every view and expression, the reporters
    python3 source/press_secretary.py stills OUT.jpg T [T..] one contact sheet of stills at these times
    python3 source/press_secretary.py final OUT.mp4 [--small]
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402  camera, pen, canvas
from ed import INK, curve, oval, smooth   # noqa: E402
from satire_style import rough   # noqa: E402
import filmkit                   # noqa: E402
import figure as F               # noqa: E402

NAME = 'press-secretary'
FPS = 12
SERIF = os.path.join(HERE, 'fonts', 'Cinzel-Variable.ttf')

# =============================================== STORY ===============================================================
# The draft script as beats. ('say', words, gaze) | ('look', 'up'/'down') | ('smile', level, secs) | ('hold', secs)
# | ('sigh', secs). Speaking time comes from the syllables; '...' leaves a long halting gap, '.' a short one.
# When Sam's recording arrives, these timings are replaced by the recording's.
SCRIPT = [
    ('hold', 0.5, 1),
    ('say', 'Good morning.', 'up'), ('say', 'I am...', 'up'), ('say', 'so honoured.', 'up'),
    ('say', 'To be.', 'up'), ('say', 'Here.', 'up'),
    ('smile', 2, 0.9),
    ('look', 'down'),
    ('say', 'President Trump has...', 'down'), ('say', 'amplified.', 'down'),
    ('look', 'up'), ('say', 'And multiplied.', 'up'),
    ('look', 'down'), ('say', 'And...', 'down'), ('say', 'expanded.', 'down'), ('say', 'The amplification.', 'down'),
    ('smile', 3, 1.3),
    ('say', 'Of wins.', 'up'), ('say', 'For...', 'up'), ('say', 'Americans.', 'up'),
    ('look', 'down'), ('say', 'For... for Americans.', 'down'),
    ('say', 'Attendance is at...', 'down'), ('say', 'record...', 'down'), ('say', 'highs.', 'down'),
    ('smile', 2, 0.9),
    ('say', 'He is an energetic...', 'up'), ('say', 'president.', 'up'),
    ('smile', 3, 0.8),
    ('say', 'Very...', 'up'), ('say', 'energetic.', 'up'),
    ('look', 'down'),
    ('say', 'A historic...', 'down'), ('say', 'one-day...', 'down'), ('say', 'war.', 'down'),
    ('smile', 2, 0.7),
    ('look', 'down'),
    ('say', 'And a great relationship...', 'down'),
    ('hold', 0.3, 0),
    ('sigh', 1.4),
    ('say', 'with Venezuela.', 'down'),
    ('hold', 0.7, 0),
]
SYL = 0.13          # seconds a syllable (the halting comes from the gaps)
# ====================================================================================================================


def syllables(w):
    w = w.lower().strip('.,!?-')
    groups = sum(1 for i, c in enumerate(w) if c in 'aeiouy' and (i == 0 or w[i - 1] not in 'aeiouy'))
    return max(1, groups - (1 if w.endswith('e') and groups > 1 and not w.endswith('le') else 0))


def build_timeline():
    """Each beat with its start and end; the speech as (start, end) windows per syllable run."""
    t, beats, talk = 0.0, [], []
    gaze = 'up'
    for b in SCRIPT:
        kind = b[0]
        if kind == 'say':
            gaze = b[2]
            for chunk in b[1].replace('...', '...|').split('|'):
                words = chunk.split()
                if not words:
                    continue
                d = sum(syllables(w) for w in words) * SYL + 0.04
                talk.append((t, t + d, chunk.strip()))
                beats.append(('say', t, t + d, gaze))
                t += d
                gap = 0.45 if chunk.strip().endswith('...') else 0.2 if chunk.strip().endswith('.') else 0.06
                beats.append(('gap', t, t + gap, gaze))
                t += gap
        elif kind == 'look':
            gaze = b[1]
            beats.append(('look', t, t + 0.25, gaze))
            t += 0.25
        elif kind == 'smile':
            beats.append(('smile', t, t + b[2], b[1]))
            gaze = 'up'
            t += b[2]
        elif kind == 'hold':
            beats.append(('hold', t, t + b[1], b[2]))
            t += b[1]
        elif kind == 'sigh':
            beats.append(('sigh', t, t + b[1], None))
            t += b[1]
    return beats, talk, t


BEATS, TALK, END = build_timeline()
DUR = round(END + 0.25, 2)            # the hard cut to black comes just after the last hold
BLACK_AT = END
BLINKS = F.blinks(17, 0.4, END, talking=True)
SIGH = next(((a, b) for k, a, b, _ in BEATS if k == 'sigh'), (1e9, 1e9))

# ------------------------------------------------------------------------------------------------ the camera
# One slow push-in: the zoom grows at a steady rate (log-linear, so it never seems to speed up), easing in at the
# start. Depth: each layer sits f closer to the camera than her (negative = behind her), so the reporters in front
# swell and slide away under the lens while the back wall barely moves.
Z0, Z1 = 0.6, 3.3
A0, A1 = (560.0, 1250.0), (540.0, 880.0)       # the point the camera looks at: the room, then her face
D0 = Z1 / Z0                                    # her distance at the start (1 at the end)
PUSH_END = END - 0.9                            # arrives on the close-up just before "Venezuela"


def push(t):
    u = max(0.0, min(1.0, t / PUSH_END))
    u = u * u * (3 - 2 * u) * 0.35 + u * 0.65   # a gentle ease in and out over a steady glide
    return u


def cam_at(t, f=0.0):
    u = push(t)
    z = Z0 * (Z1 / Z0) ** (u ** 1.25)               # stays wide a little longer, then closes in
    d = D0 * Z0 / z
    if f:
        if d - f <= 0.08:
            return None
        z *= (d / (d - f)) / (D0 / (D0 - f))
    ax = A0[0] + (A1[0] - A0[0]) * u
    ay = A0[1] + (A1[1] - A0[1]) * (u ** 0.8)
    return B.Cam(z, ax, ay)


# ------------------------------------------------------------------------------------------------ her look
NECK = (540.0, 1000.0)               # her neck base in the world; podium top is 280 below it
SKIN = (236, 190, 160)
SKIN_D = (214, 160, 130)
HAIR = (226, 186, 118)
HAIR_D = (184, 138, 76)
HAIR_L = (246, 220, 162)
BROW = (138, 98, 60)
LIP = (204, 128, 124)
LIP_D = (166, 86, 88)
NAVYJ = (30, 38, 66)
NAVYJ_D = (20, 26, 46)
BLOUSE = (248, 246, 240)
BLOUSE_D = (214, 210, 204)
GOLDB = (222, 176, 72)
IRIS = (96, 120, 112)
PODIUM_TOP = 280


def state(t):
    """Everything about her at time t: where she looks, lids, brows, mouth, head and shoulders."""
    s = dict(gaze='up', lid=0.0, brow=0.0, mouth='rest', smile=0, head_dy=0.0, head_tilt=0.0, sh_dy=0.0,
             closed=False, look_x=0.0, squint=0.0)
    beat = next((b for b in BEATS if b[1] <= t < b[2]), BEATS[-1])
    kind, a, b, arg = beat
    # what her gaze was coming into this beat (the 'look' beats snap on their first frame: an instant glance)
    if kind in ('say', 'gap', 'look'):
        s['gaze'] = arg
    elif kind == 'smile':
        s['gaze'] = 'up'
    elif kind == 'hold':
        s['gaze'] = 'up' if arg else 'down'
    elif kind == 'sigh':
        s['gaze'] = 'down'
    if kind == 'say':
        k = int((t - a) * FPS)
        rnd = random.Random(int(a * 1000) + k // 1)
        seq = ['small', 'mid', 'open', 'mid', 'small', 'open', 'mid']
        s['mouth'] = seq[(k + int(a * 7)) % len(seq)] if (t - a) < (b - a) - 0.06 else 'rest'
        if rnd.random() < 0.12:
            s['mouth'] = 'small'
    if kind == 'smile':
        level = arg
        u = (t - a) / (b - a)
        on = smooth((t - a) / 0.12)                    # the smile switches ON almost at once
        off = 1.0 - smooth((t - (b - 0.1)) / 0.1)      # and OFF, just as suddenly (that is the strangeness)
        if on * off > 0.5:
            s['smile'] = level
            s['brow'] = 6 + 4 * level
            s['squint'] = 0.25 * level
            s['head_tilt'] = 0.05 * (1 if level == 3 else -1) * smooth(u * 4)
    if kind == 'hold' and arg:
        s['smile'] = 1
    if s['gaze'] == 'down':
        s['lid'] = 0.62
        s['head_dy'] = 10.0
        s['brow'] = -2.0
    if kind == 'sigh':
        u = (t - a) / (b - a)
        rise = smooth(u / 0.45) - smooth((u - 0.5) / 0.4) * 1.25
        s['sh_dy'] = -16.0 * rise
        s['head_dy'] = 14.0 - 6 * rise
        s['closed'] = 0.25 < u < 0.8
        s['mouth'] = 'blow' if 0.5 < u < 0.92 else 'rest'
        s['brow'] = 3.0 * rise
    if t >= SIGH[1]:                       # after the sigh: heavier lids, flatter, deader
        s['lid'] = max(s['lid'], 0.7)
        s['brow'] = -3.0
    if any(bt <= t < bt + 0.14 for bt in BLINKS) and s['smile'] == 0:
        s['closed'] = True
    s['head_tilt'] += filmkit.shifts(t, seed=4, amount=0.025)
    s['head_dx'] = 40 * filmkit.shifts(t, seed=9, amount=0.06)
    return s


# ------------------------------------------------------------------------------------------------ drawing her
def head_shape(hx, hy, hw, hh):
    """A slim oval face: wide at the cheekbones, tapering to a narrow, slightly pointed chin."""
    top = oval(hx, hy - 4, hw, hh * 0.98, 24, math.pi, 2 * math.pi)
    return top + [(hx + hw, hy + 8), (hx + hw * 0.96, hy + hh * 0.46), (hx + hw * 0.7, hy + hh * 0.86),
                  (hx + hw * 0.32, hy + hh * 1.1), (hx, hy + hh * 1.16), (hx - hw * 0.32, hy + hh * 1.1),
                  (hx - hw * 0.7, hy + hh * 0.86), (hx - hw * 0.96, hy + hh * 0.46), (hx - hw, hy + 8)]


def wave_edge(x_of, y0, y1, n, amp, phase=0.0):
    """Points down a wavy edge: x_of(u) the base line, plus a soft S-wave (the blow-dried waves)."""
    return [(x_of(k / n) + amp * math.sin(phase + k / n * math.pi * 3.2), y0 + (y1 - y0) * k / n) for k in range(n + 1)]


def hair_mass(p, hx, hy, hw, hh, shrug):
    """The back of the hair: rounded volume above the head, waves falling behind the shoulders to mid-back.
    Narrower than her shoulders, so the blazer's shoulders show either side."""
    right = wave_edge(lambda u: hx + hw + 30 + 26 * math.sin(u * math.pi * 0.8), hy - hh * 0.5, hy + 330 + shrug, 12, 8)
    left = [(2 * hx - x, y) for x, y in right]
    top = oval(hx, hy - 6, hw + 30, hh + 30, 18, math.pi * 1.05, math.pi * 1.95)
    pts = left[::-1][:-1] + [left[0]] + top + right + [(hx + hw + 10, hy + 350 + shrug), (hx - hw - 10, hy + 350 + shrug)]
    pts = left[::-1] + top + right + [(hx, hy + 360 + shrug)]
    p.poly(curve(pts, 3), HAIR_D, INK, 2.6)


def hair_locks(p, hx, hy, hw, hh, sh_dy):
    """The long waves falling in FRONT of each shoulder over the blazer, to mid-chest, framing the face."""
    for sgn in (-1, 1):
        outer = wave_edge(lambda u: hx + sgn * (hw + 22 + 30 * math.sin(u * math.pi * 0.9)), hy - hh * 0.3,
                          hy + 300 + sh_dy, 12, 11 * sgn, 0.4)
        inner = wave_edge(lambda u: hx + sgn * (hw * 0.86 - 4 * u + 6 * math.sin(u * math.pi)), hy + 20,
                          hy + 290 + sh_dy, 10, 7 * sgn, 0.9)
        tip = (hx + sgn * (hw + 18), hy + 330 + sh_dy)
        pts = inner + [tip] + outer[::-1]
        p.poly(curve(pts, 3), HAIR, INK, 2.6)
        for k in range(3):                               # strands following the waves
            line = wave_edge(lambda u: hx + sgn * (hw + 6 + 12 * k + 26 * math.sin(u * math.pi * 0.9)), hy + 10 + 12 * k,
                             hy + 270 - 20 * k + sh_dy, 8, 9 * sgn, 0.6)
            p.line(line, HAIR_D, 1.7)
        hl = wave_edge(lambda u: hx + sgn * (hw + 18 + 26 * math.sin(u * math.pi * 0.9)), hy + 30, hy + 140, 4, 9 * sgn, 0.6)
        p.line(hl, HAIR_L, 3.0)


def hair_top(p, hx, hy, hw, hh, fx):
    """The crown, full and rounded, a side parting (our left), swept to both sides and down past the temples."""
    part = fx - hw * 0.25
    outer = oval(hx, hy - 8, hw + 24, hh + 28, 20, math.pi * 0.97, math.pi * 2.03)
    line = [(hx + hw + 18, hy + 30), (hx + hw * 0.92, hy - hh * 0.3), (hx + hw * 0.62, hy - hh * 0.7),
            (part + hw * 0.25, hy - hh * 0.86), (part, hy - hh * 0.98), (part - hw * 0.2, hy - hh * 0.84),
            (hx - hw * 0.7, hy - hh * 0.62), (hx - hw * 0.94, hy - hh * 0.2), (hx - hw - 18, hy + 30)]
    p.poly(curve(outer + line, 3), HAIR, INK, 2.6)
    p.line([(part, hy - hh * 1.22), (part + 3, hy - hh * 0.98)], HAIR_D, 2.0)
    for k in range(3):
        p.line(curve([(part + 10 + 14 * k, hy - hh * 1.16 + 8 * k), (hx + hw * 0.7 + 6 * k, hy - hh * 0.9 + 12 * k),
                      (hx + hw + 6 + 2 * k, hy - hh * 0.3 + 10 * k)], 3)[:-3], HAIR_D, 1.6)
        p.line(curve([(part - 10 - 12 * k, hy - hh * 1.14 + 8 * k), (hx - hw * 0.7 - 6 * k, hy - hh * 0.86 + 12 * k),
                      (hx - hw - 6 - 2 * k, hy - hh * 0.3 + 10 * k)], 3)[:-3], HAIR_D, 1.6)
    p.line([(part + 16, hy - hh * 1.18), (hx + hw * 0.55, hy - hh * 1.06)], HAIR_L, 3.4)


def eye(p, ex, ey, sgn, st):
    """A large almond eye: heavy dark liner, lashes flicked out at the corner, a hazel iris."""
    lid, squint = st['lid'], st['squint']
    w, h = 21, 10
    if st['closed']:
        p.line([(ex - w, ey + 1), (ex - 8, ey + 6), (ex + 8, ey + 6), (ex + w, ey + 1)], INK, 3.4)
        for k in range(3):
            lx = ex + sgn * (8 + 6 * k)
            p.line([(lx, ey + 5), (lx + sgn * 5, ey + 12)], INK, 1.8)
        return
    low = h * (1 - squint)                                # a big smile pushes the lower lid up
    top_y = ey - h + lid * h * 1.6
    almond = [(ex - w, ey), (ex - w * 0.45, ey - h), (ex + w * 0.45, ey - h), (ex + w, ey), (ex + w * 0.45, ey + low),
              (ex - w * 0.45, ey + low)]
    p.poly(almond, (252, 252, 250), None)
    dx = st['look_x'] * 6
    dy = 5 if st['gaze'] == 'down' else 0
    p.ell(ex + dx, ey + dy, 9, 9, IRIS, INK, 1.4)
    p.ell(ex + dx, ey + dy, 4.2, 4.2, INK, None)
    p.ell(ex + dx + 3, ey + dy - 3, 1.8, 1.8, (255, 255, 255), None)
    if lid > 0:                                           # the upper lid lowered (reading her notes)
        p.poly([(ex - w - 1, ey - 1), (ex - w * 0.45, ey - h - 2), (ex + w * 0.45, ey - h - 2), (ex + w + 1, ey - 1),
                (ex + w * 0.45, top_y), (ex - w * 0.45, top_y)], (206, 166, 150), None)
    p.line([(ex - w * 0.45, ey + low), (ex + w * 0.45, ey + low), (ex + w, ey)], INK, 1.6)
    p.line([(ex - w * 1.02, ey), (ex - w * 0.45, min(ey - 1, top_y)), (ex + w * 0.45, min(ey - 1, top_y)),
            (ex + w * 1.06, ey - 1)], INK, 3.6)           # the liner
    tip = (ex + sgn * w * 1.06, ey - 1)
    p.line([tip, (tip[0] + sgn * 8, tip[1] - 6)], INK, 2.6)        # the winged flick
    for k in range(3):
        lx = ex + sgn * (6 + 6 * k)
        p.line([(lx, min(ey - 1, top_y) - 1), (lx + sgn * 4, min(ey - 1, top_y) - 7 - k)], INK, 1.6)
    p.line([(ex - w * 0.6, ey - h - 9), (ex + w * 0.6, ey - h - 9)], (198, 156, 140), 1.4)   # the crease, made up


def mouth(p, fx, my, st):
    m, sm = st['mouth'], st['smile']
    if sm >= 2:                                           # the big strange smile: wide, all top teeth (3: both rows)
        w = 38 if sm == 2 else 46
        up = 10 if sm == 2 else 14
        drop = 18 if sm == 2 else 26
        outer = curve([(fx - w, my - up), (fx - w * 0.5, my - 4), (fx, my - 3), (fx + w * 0.5, my - 4), (fx + w, my - up),
                       (fx + w * 0.62, my + drop * 0.7), (fx, my + drop), (fx - w * 0.62, my + drop * 0.7)], 4)
        p.poly(outer, LIP, INK, 2.2)
        inner = curve([(fx - w + 7, my - up + 3), (fx, my + 1), (fx + w - 7, my - up + 3), (fx + w * 0.5, my + drop * 0.6),
                       (fx, my + drop - 6), (fx - w * 0.5, my + drop * 0.6)], 4)
        p.poly(inner, (96, 34, 42), None)
        teeth = [(fx - w + 8, my - up + 3), (fx - w * 0.5, my + 1), (fx, my + 2), (fx + w * 0.5, my + 1),
                 (fx + w - 8, my - up + 3), (fx + w * 0.55, my + 10), (fx, my + 12), (fx - w * 0.55, my + 10)]
        p.poly(curve(teeth, 3), (255, 255, 252), None)
        if sm == 3:
            p.poly(curve([(fx - w * 0.5, my + drop * 0.62), (fx, my + drop - 10), (fx + w * 0.5, my + drop * 0.62),
                          (fx, my + drop - 3)], 3), (250, 250, 246), None)
        for k in range(-3, 4):                            # the gaps between teeth, faint
            p.line([(fx + k * w * 0.22, my + 1 + abs(k)), (fx + k * w * 0.22, my + 10 - abs(k))], (226, 222, 216), 1.0)
        p.poly(outer, None, INK, 2.2)
        for sgn in (-1, 1):                               # cheeks bunched up by it
            p.line([(fx + sgn * (w + 4), my - up - 12), (fx + sgn * (w + 10), my - up), (fx + sgn * (w + 4), my - up + 10)],
                   SKIN_D, 1.8)
        return
    if m == 'blow':                                       # the sigh: a small rounded breath out
        p.poly(curve(oval(fx, my + 4, 11, 9, 12)), LIP, INK, 2.0)
        p.ell(fx, my + 4, 5, 4, (96, 34, 42), None)
        return
    if m in ('small', 'mid', 'open'):
        h = {'small': 7, 'mid': 13, 'open': 19}[m]
        w = {'small': 20, 'mid': 22, 'open': 19}[m]
        outer = curve([(fx - w - 3, my), (fx - 8, my - 6), (fx, my - 4), (fx + 8, my - 6), (fx + w + 3, my),
                       (fx + w * 0.6, my + h + 6), (fx, my + h + 8), (fx - w * 0.6, my + h + 6)], 4)
        p.poly(outer, LIP, INK, 2.0)
        p.poly(curve([(fx - w + 2, my), (fx, my - 1), (fx + w - 2, my), (fx + w * 0.5, my + h), (fx, my + h + 1),
                      (fx - w * 0.5, my + h)], 3), (96, 34, 42), None)
        if m != 'small':
            p.poly([(fx - w * 0.7, my), (fx + w * 0.7, my), (fx + w * 0.55, my + 5), (fx - w * 0.55, my + 5)],
                   (255, 255, 252), None)
        p.poly(outer, None, INK, 2.0)
        return
    # resting: full lips, closed (sm == 1: a small closed smile)
    c = 6 if sm == 1 else 0
    top = curve([(fx - 25, my + 1 - c), (fx - 10, my - 8), (fx, my - 5), (fx + 10, my - 8), (fx + 25, my + 1 - c),
                 (fx, my + 2)], 3)
    bot = curve([(fx - 25, my + 1 - c), (fx, my + 2), (fx + 25, my + 1 - c), (fx + 12, my + 13), (fx, my + 15),
                 (fx - 12, my + 13)], 3)
    p.poly(top, LIP_D, INK, 1.8)
    p.poly(bot, LIP, INK, 1.8)
    p.line([(fx - 25, my + 1 - c), (fx - 10, my + 3), (fx + 10, my + 3), (fx + 25, my + 1 - c)], INK, 2.0)


def face(p, hx, hy, hw, hh, st):
    fx = hx
    brow = st['brow']
    for sgn in (-1, 1):                                   # arched, filled-in brows, darker than the hair
        ex = fx + sgn * 29
        by = hy - 30 - brow
        p.poly([(ex - sgn * 18, by + 6), (ex - sgn * 4, by - 3), (ex + sgn * 10, by - 7), (ex + sgn * 24, by + 2),
                (ex + sgn * 10, by - 2), (ex - sgn * 4, by + 2)], BROW, BROW, 1.6)
    for sgn in (-1, 1):
        eye(p, fx + sgn * 29, hy - 6 + st.get('eye_dy', 0), sgn, st)
    p.line([(fx - 3, hy - 4), (fx - 6, hy + 26), (fx - 2, hy + 33), (fx + 7, hy + 31)], INK, 1.8)   # a slim nose
    p.line([(fx - 11, hy + 30), (fx - 7, hy + 33)], INK, 1.4)
    for sgn in (-1, 1):                                   # cheekbones: a flat blush, high
        p.ell(fx + sgn * 38, hy + 22, 12, 6, (240, 176, 156), None, rot=-sgn * 0.3)
    mouth(p, fx, hy + 56, st)


def torso(p, sh_dy):
    """Navy double-breasted blazer with gold buttons; a white tie-neck blouse with a keyhole."""
    sw = 150
    body = [(-40, -4), (-sw * 0.82, 10 + sh_dy), (-sw - 6, 44 + sh_dy), (-sw - 2, 200), (-sw + 4, 460), (sw - 4, 460),
            (sw + 2, 200), (sw + 6, 44 + sh_dy), (sw * 0.82, 10 + sh_dy), (40, -4)]
    p.poly(rough(body, 3, 11), NAVYJ, INK, 2.6)
    p.poly([(-30, -78), (30, -78), (34, 8), (-34, 8)], SKIN, INK, 2.4)                       # neck
    # the blouse in the V, the tie at the neck, the keyhole under it
    p.poly([(-46, -6), (46, -6), (24, 170), (0, 200), (-24, 170)], BLOUSE, INK, 2.2)
    p.poly(curve([(-36, -30), (0, -22), (36, -30), (38, 0), (0, 8), (-38, 0)], 3), BLOUSE, INK, 2.0)  # the collar band
    p.poly(curve([(-8, 66), (0, 20), (8, 66), (0, 84)], 3), SKIN, INK, 1.8)                 # the keyhole
    p.poly(curve([(-22, 4), (0, -6), (22, 4), (12, 22), (0, 26), (-12, 22)], 3), BLOUSE, INK, 2.0)   # the knot
    for sgn in (-1, 1):                                   # the tie's short tails, draped
        p.poly(curve([(sgn * 6, 20), (sgn * 26, 26), (sgn * 34, 70), (sgn * 22, 96), (sgn * 12, 60)], 3), BLOUSE, INK, 1.8)
        p.line([(sgn * 14, 30), (sgn * 24, 80)], BLOUSE_D, 1.4)
    for sgn in (-1, 1):                                   # peaked lapels
        lap = [(sgn * 46, -4), (sgn * 76, 24 + sh_dy * 0.5), (sgn * 60, 86), (sgn * 92, 100), (sgn * 70, 130),
               (sgn * 24, 176), (sgn * 30, 120)]
        p.poly(lap, NAVYJ, INK, 2.2)
    p.line([(-24, 176), (22, 236), (22, 460)], NAVYJ_D, 2.2)    # the front edge, crossing over (double-breasted)
    for bx in (-46, 46):                                  # gold buttons, two rows of two
        for by in (196, 264):
            p.ell(bx, by, 9, 9, GOLDB, INK, 1.6)
            p.ell(bx, by, 4.5, 4.5, (176, 130, 40), None)
    return sw


def arms(p, sh_dy):
    """Upper arms down the sides, forearms forward onto the podium; circle hands either side of her notes."""
    for sgn in (-1, 1):
        sh = (sgn * 140, 40 + sh_dy)
        el = (sgn * 172, 232)
        wr = (sgn * 112, PODIUM_TOP - 24)
        p.poly(curve([(sh[0] + sgn * 14, sh[1]), (el[0] + sgn * 14, el[1]), (wr[0] + sgn * 4, wr[1] + 14),
                      (wr[0] - sgn * 12, wr[1] - 16), (el[0] - sgn * 22, el[1] - 26), (sh[0] - sgn * 26, sh[1] + 40)], 3),
               NAVYJ, INK, 2.4)
        p.ell(wr[0] - sgn * 14, wr[1] + 2, 20, 17, SKIN, INK, 2.2)


def her(img, cam, t, st=None, notes=True):
    st = st or state(t)
    L = B.Local(cam, NECK[0], NECK[1], 1.0)
    p = B.Pen(img, L)
    hw, hh = 60, 84
    hx, hy = st['head_dx'], -138 + st['head_dy']
    sh = st['sh_dy']
    tilt = st['head_tilt']
    hair_mass(p, hx * 0.6, hy, hw, hh, sh)
    torso(p, sh)
    hair_locks(p, hx * 0.6, hy, hw, hh, sh)
    arms(p, sh)
    # the head (tilt by shearing the face sideways a little: flat, never a 3D turn)
    T = B.Local(cam, NECK[0] + 0, NECK[1] + 0, 1.0)

    class Tilted:
        def __init__(self, base):
            self.base, self.s = base, base.s

        def P(self, x, y):
            dx, dy = x - hx, y - (hy + 60)
            c, s_ = math.cos(tilt), math.sin(tilt)
            return self.base.P(hx + dx * c - dy * s_, hy + 60 + dx * s_ + dy * c)

        def S(self, v):
            return self.base.S(v)

    q = B.Pen(img, Tilted(T))
    for sgn in (-1, 1):                                   # ears hidden under the hair; a gold stud shows
        q.ell(hx + sgn * (hw + 1), hy + 14, 9, 17, SKIN, INK, 2.0)
    q.poly(head_shape(hx, hy, hw, hh), SKIN, INK, 2.6)
    face(q, hx, hy, hw, hh, st)
    q.poly(head_shape(hx, hy, hw, hh), None, INK, 2.6)
    hair_top(q, hx, hy, hw, hh, hx)


# ------------------------------------------------------------------------------------------------ the set
SET_BLUE = (120, 178, 214)
SET_BLUE_L = (160, 206, 232)
SET_BLUE_D = (64, 108, 156)
CURTAIN = (26, 44, 92)
CREAM = (236, 228, 210)
WOOD = (120, 70, 40)
PODIUM_C = (30, 32, 42)
CARPET = (34, 44, 92)


def text(img, cam, x, y, s, size, colr, font=SERIF, anchor='mm'):
    """Lettering in world units."""
    f = ImageFont.truetype(font, max(4, int(cam.S(size))))
    try:
        f.set_variation_by_axes([600])
    except Exception:
        pass
    X, Y = cam.P(x, y)
    ImageDraw.Draw(img).text((X, Y), s, font=f, fill=colr, anchor=anchor)


def white_house(p, cx, cy, w):
    """The White House, as on the seal: portico, columns, wings, a flag on the roof."""
    h = w * 0.42
    pal, pal_d = (234, 244, 250), (178, 206, 224)
    p.poly([(cx - w, cy), (cx + w, cy), (cx + w, cy - h * 0.62), (cx - w, cy - h * 0.62)], pal, INK, 1.6)
    p.poly([(cx - w * 0.32, cy), (cx + w * 0.32, cy), (cx + w * 0.32, cy - h * 0.86), (cx - w * 0.32, cy - h * 0.86)],
           pal, INK, 1.6)
    p.poly([(cx - w * 0.36, cy - h * 0.86), (cx + w * 0.36, cy - h * 0.86), (cx, cy - h * 1.16)], pal, INK, 1.6)
    for k in range(6):
        x = cx - w * 0.26 + k * w * 0.104
        p.line([(x, cy - 2), (x, cy - h * 0.8)], pal_d, 2.0)
    for side in (-1, 1):
        for k in range(4):
            x = cx + side * (w * 0.44 + k * w * 0.14)
            p.poly([(x - 5, cy - h * 0.18), (x + 5, cy - h * 0.18), (x + 5, cy - h * 0.42), (x - 5, cy - h * 0.42)],
                   pal_d, None)
    p.line([(cx, cy - h * 1.16), (cx, cy - h * 1.5)], INK, 1.4)
    p.poly([(cx, cy - h * 1.5), (cx + w * 0.12, cy - h * 1.44), (cx, cy - h * 1.38)], (190, 50, 60), None)


def flag(img, cam, x, top, bottom, t):
    """The US flag on a pole, hanging in folds (stars on blue, red and white stripes), a gold finial.
    The stripes and stars are drawn on their own layer and cut to the cloth's outline."""
    p = B.Pen(img, cam)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    q = B.Pen(lay, cam)
    p.poly(rough([(x - 6, top), (x + 6, top), (x + 7, bottom + 600), (x - 7, bottom + 600)], 1, 3), (200, 170, 90), INK, 2)
    p.ell(x, top - 18, 16, 20, (222, 184, 80), INK, 2)
    w = 210
    cloth = [(x + 6, top + 10), (x + w, top + 30), (x + w + 30, top + 300), (x + w - 10, bottom - 120),
             (x + w * 0.5, bottom), (x + 8, bottom - 60)]
    p.poly(curve(cloth, 4), (246, 246, 244), INK, 2.4)
    sh = (bottom - top) / 13.0
    for k in range(0, 13, 2):                             # seven red stripes across the whole cloth
        y0 = top + 10 + k * sh
        q.poly([(x - 40, y0), (x + w + 120, y0 + 10), (x + w + 120, y0 + 10 + sh), (x - 40, y0 + sh)], (190, 40, 54), None)
    q.poly([(x + 8, top + 12), (x + w * 0.62, top + 22), (x + w * 0.66, top + 420), (x + 8, top + 400)], (34, 48, 110), None)
    rng = np.random.default_rng(3)
    for k in range(26):
        sx, sy = x + 24 + (k % 4) * 30 + rng.uniform(-4, 4), top + 40 + (k // 4) * 56 + rng.uniform(-4, 4)
        q.ell(sx, sy, 5, 5, (246, 246, 244), None)
    for k in range(4):                                    # the folds
        fx_ = x + 50 + k * 46
        q.line([(fx_, top + 30), (fx_ + 10, top + 400), (fx_ - 6, bottom - 100)], (120, 30, 40), 2.0)
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).polygon([cam.P(*pt) for pt in curve(cloth, 4)], fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay.getchannel('A')), np.asarray(m))))
    img.alpha_composite(lay)
    p.poly(curve(cloth, 4), None, INK, 2.4)


def backdrop(img, cam, t):
    """The briefing-room wall: cream walls and pilasters, the blue backdrop, dark blue curtains, the seal,
    the frosted side panels with little seals, the flag."""
    p = B.Pen(img, cam)
    p.poly(rough([(-1400, -1400), (2500, -1400), (2500, 1720), (-1400, 1720)], 4, 1), CREAM, INK, 3)
    p.poly([(-1400, -500), (2500, -500), (2500, -460), (-1400, -460)], (214, 204, 184), INK, 2.4)   # crown moulding
    for x in (-430, 1520):                                # white pilasters either side
        p.poly(rough([(x - 70, -460), (x + 70, -460), (x + 70, 1720), (x - 70, 1720)], 3, x), (246, 242, 232), INK, 2.6)
        p.poly([(x - 90, -460), (x + 90, -460), (x + 90, -400), (x - 90, -400)], (246, 242, 232), INK, 2.4)
        p.line([(x - 30, -380), (x - 30, 1700)], (220, 214, 200), 2)
        p.line([(x + 30, -380), (x + 30, 1700)], (220, 214, 200), 2)
    p.poly(rough([(-1250, 600), (-700, 600), (-700, 1720), (-1250, 1720)], 3, 21), (150, 118, 84), INK, 2.6)  # a door
    p.ell(-760, 1180, 12, 12, (222, 184, 80), INK, 1.6)
    p.poly(rough([(1760, 640), (2260, 640), (2260, 1720), (1760, 1720)], 3, 22), (150, 118, 84), INK, 2.6)
    p.ell(1820, 1200, 12, 12, (222, 184, 80), INK, 1.6)
    p.poly(rough([(1780, 300), (2240, 300), (2240, 520), (1780, 520)], 3, 23), (40, 50, 90), INK, 2.4)   # a TV screen
    p.poly(rough([(1800, 318), (2220, 318), (2220, 502), (1800, 502)], 2, 24), (90, 130, 170), None)
    text(img, cam, 2010, 410, 'LIVE', 46, (240, 240, 240), font=B.ANTON)
    # the backdrop: dark curtains either side, a pale blue centre
    p.poly(rough([(-360, -420), (1440, -420), (1440, 1720), (-360, 1720)], 3, 2), CURTAIN, INK, 3)
    for k in range(10):
        x = -340 + k * 22
        p.line([(x, -400), (x + 4, 1700)], (16, 30, 70), 2)
        x = 1260 + k * 18
        p.line([(x, -400), (x + 4, 1700)], (16, 30, 70), 2)
    p.poly(rough([(-120, -380), (1240, -380), (1240, 1720), (-120, 1720)], 3, 4), SET_BLUE, INK, 3)
    for k in range(6):                                    # the frosted glass bands
        x = -100 + k * 36
        p.line([(x, -360), (x, 1700)], SET_BLUE_L, 3)
    for j in range(6):                                    # little seals on the right-hand panel
        for i in range(2):
            cx, cy = 1040 + i * 150, -260 + j * 300 + (i * 150)
            p.ell(cx, cy, 52, 36, SET_BLUE_L, SET_BLUE_D, 2)
            p.poly([(cx - 26, cy + 10), (cx + 26, cy + 10), (cx + 26, cy - 6), (cx - 26, cy - 6)], SET_BLUE_D, None)
    for j in range(5):
        cx, cy = 10, -200 + j * 380
        p.ell(cx, cy, 52, 36, SET_BLUE_L, SET_BLUE_D, 2)
        p.poly([(cx - 26, cy + 10), (cx + 26, cy + 10), (cx + 26, cy - 6), (cx - 26, cy - 6)], SET_BLUE_D, None)
    # the big seal: oval, the house, the words
    cx, cy, rx, ry = 600, 640, 300, 200
    p.ell(cx, cy, rx + 18, ry + 16, (90, 148, 190), INK, 2.6)
    p.ell(cx, cy, rx, ry, (52, 108, 160), (210, 232, 244), 3.4)
    white_house(p, cx, cy + 30, rx * 0.5)
    _seal_words(img, cam, cx, cy)
    flag(img, cam, 150, 420, 1560, t)


def _seal_words(img, cam, cx, cy):
    for s, y, size in (('THE WHITE HOUSE', cy + 100, 52), ('WASHINGTON', cy + 152, 30)):
        f = ImageFont.truetype(SERIF, max(4, int(cam.S(size))))
        try:
            f.set_variation_by_axes([700])
        except Exception:
            pass
        X, Y = cam.P(cx, y)
        ImageDraw.Draw(img).text((X, Y), s, font=f, fill=(236, 244, 250), anchor='mm')


def stage_floor(img, cam):
    """The low stage: navy carpet with small gold stars, a front edge, then the room's carpet."""
    p = B.Pen(img, cam)
    p.poly(rough([(-1400, 1700), (2500, 1700), (2500, 1860), (-1400, 1860)], 3, 31), CARPET, INK, 3)
    rng = np.random.default_rng(8)
    for k in range(70):
        x, y = rng.uniform(-1300, 2400), rng.uniform(1716, 1846)
        p.ell(x, y, 5, 3.5, (210, 180, 90), None)
    p.poly(rough([(-1400, 1860), (2500, 1860), (2500, 1900), (-1400, 1900)], 2, 32), (20, 26, 60), INK, 2.4)
    p.poly(rough([(-1600, 1900), (2700, 1900), (2700, 4400), (-1600, 4400)], 3, 33), (88, 96, 124), INK, 3)


def podium(img, cam):
    """The dark wooden podium: a wood top, a near-black front with the White House plaque, two gooseneck mics."""
    p = B.Pen(img, cam)
    x0, y0 = NECK[0], NECK[1] + PODIUM_TOP
    top = [(x0 - 230, y0 - 4), (x0 + 230, y0 - 4), (x0 + 244, y0 + 26), (x0 - 244, y0 + 26)]
    body = [(x0 - 236, y0 + 26), (x0 + 236, y0 + 26), (x0 + 190, y0 + 560), (x0 + 120, y0 + 720), (x0 - 120, y0 + 720),
            (x0 - 190, y0 + 560)]
    p.poly(rough(body, 3, 41), PODIUM_C, INK, 3)
    p.poly([(x0 - 236, y0 + 26), (x0 - 150, y0 + 26), (x0 - 120, y0 + 720), (x0 - 190, y0 + 560)], (22, 24, 32), None)
    p.poly([(x0 + 236, y0 + 26), (x0 + 150, y0 + 26), (x0 + 120, y0 + 720), (x0 + 190, y0 + 560)], (22, 24, 32), None)
    p.poly(rough(body, 3, 41), None, INK, 3)
    p.poly(rough(top, 2, 42), WOOD, INK, 2.6)
    p.line([(x0 - 228, y0 + 6), (x0 + 228, y0 + 6)], (150, 94, 56), 2)
    # the plaque
    px0, py0, px1, py1 = x0 - 150, y0 + 70, x0 + 150, y0 + 230
    p.poly(rough([(px0, py0), (px1, py0), (px1, py1), (px0, py1)], 2, 43), (18, 18, 22), (90, 90, 100), 2.6)
    p.line([(px0 + 20, py0 + 92), (px1 - 20, py0 + 92)], (196, 36, 46), 4)
    for s, y, size in (('THE WHITE HOUSE', py0 + 54, 40), ('WASHINGTON', py0 + 124, 24)):
        f = ImageFont.truetype(SERIF, max(4, int(cam.S(size))))
        try:
            f.set_variation_by_axes([700])
        except Exception:
            pass
        X, Y = cam.P(x0, y)
        ImageDraw.Draw(img).text((X, Y), s, font=f, fill=(242, 240, 236), anchor='mm')
    for sgn in (-1, 1):                                   # the two thin microphones, leaning in towards her
        base = (x0 + sgn * 150, y0 - 2)
        tip = (x0 + sgn * 96, y0 - 150)
        p.line([base, (x0 + sgn * 140, y0 - 80), tip], (20, 20, 24), 3)
        p.ell(tip[0], tip[1], 7, 12, (20, 20, 24), INK, 1.4, rot=-sgn * 0.5)


def notes(img, cam):
    """Her notes on the podium top: the edge of the paper, poking out between her hands."""
    p = B.Pen(img, cam)
    x0, y0 = NECK[0], NECK[1] + PODIUM_TOP
    p.poly(rough([(x0 - 90, y0 - 10), (x0 + 84, y0 - 12), (x0 + 92, y0 + 4), (x0 - 96, y0 + 6)], 2, 51),
           (250, 250, 246), INK, 2)


# ------------------------------------------------------------------------------------------------ the reporters
REPORTER_ROWS = [  # (f: how much nearer the camera than her, screen y of the heads at the start, count)
    (2.2, 1320, 7), (2.55, 1410, 6), (2.85, 1520, 6), (3.1, 1650, 5), (3.3, 1800, 4), (3.45, 1960, 4)]


def _reporters():
    rng = np.random.default_rng(12)
    out = []
    hairs = [(58, 44, 36), (30, 24, 22), (150, 110, 70), (210, 178, 120), (170, 166, 162), (110, 70, 46), (80, 40, 30)]
    jackets = [B.NAVY, B.CHARCOAL, (110, 40, 50), (70, 90, 120), (90, 96, 80), (60, 60, 70), (40, 110, 90),
               (150, 120, 90), (120, 60, 110)]
    skins = [B.PALE, B.PINK, B.OLIVE, B.BROWN, B.DEEP]
    styles = ['short', 'bob', 'pony', 'long', 'bald', 'short', 'bun', 'curly']
    for ri, (f, sy, n) in enumerate(REPORTER_ROWS):
        k0 = D0 / (D0 - f)
        z0 = Z0 * k0
        s = 0.8 * k0 * 0.62
        wy = A0[1] + (sy - 960) / Z0                     # world position that lands at screen y sy at the start
        width = 1080 / z0 * 1.25
        xs = np.linspace(A0[0] - width * 0.5, A0[0] + width * 0.5, n) + rng.uniform(-0.12, 0.12, n) * width / n
        xs = xs + (width / n * 0.5 if ri % 2 else 0)
        for x in xs:
            hand = rng.random() < 0.38
            out.append(dict(f=f, x=float(x), y=float(wy), s=s, hair=hairs[rng.integers(len(hairs))],
                            jacket=jackets[rng.integers(len(jackets))], skin=skins[rng.integers(5)],
                            style=styles[rng.integers(len(styles))], hand=hand, side=1 if rng.random() < 0.5 else -1,
                            up_at=float(rng.uniform(0, 8)), seed=int(rng.integers(1e6)),
                            props=('pad' if rng.random() < 0.3 else None)))
    return out


REPORTERS = _reporters()


def reporter(img, cam, r, t):
    """A seated reporter from behind: head, hair, shoulders; some with one hand up (a circle hand), held high,
    lowered now and then and raised again. Relaxed and normal; nobody looks round."""
    p = B.Pen(img, B.Local(cam, r['x'], r['y'], r['s']))
    hc, jc, skin, st = r['hair'], r['jacket'], r['skin'], r['style']
    up = False
    if r['hand']:
        ph = (t + r['up_at']) % 9.0
        up = ph < 6.5                                    # up for a long while, down briefly, up again
    if up:
        sg = r['side']
        sway = 6 * filmkit.shifts(t, seed=r['seed'], amount=1.0)
        p.poly([(sg * 76, 30), (sg * 136, 40), (sg * 120 + sway, -230), (sg * 70 + sway, -236)], jc, INK, 3)
        p.ell(sg * 95 + sway, -262, 30, 32, skin, INK, 3)
    p.poly(curve([(-150, 220), (-140, 50), (-70, 0), (70, 0), (140, 50), (150, 220)], 4), jc, INK, 3)
    p.poly([(-28, 2), (28, 2), (24, -30), (-24, -30)], skin, INK, 2.4)
    for sgn in (-1, 1):
        p.ell(sgn * 66, -70, 12, 20, skin, INK, 3)
    if st == 'bald':
        p.ell(0, -84, 64, 78, skin, INK, 3)
        p.poly(curve([(-66, -60), (-60, -20), (0, -6), (60, -20), (66, -60), (40, -40), (-40, -40)], 3), hc, INK, 2.4)
    else:
        p.ell(0, -84, 66, 80, hc, INK, 3)
        if st == 'bob':
            p.poly(curve([(-74, -90), (-80, 0), (0, 12), (80, 0), (74, -90), (0, -150)], 3), hc, INK, 3)
        elif st == 'long':
            p.poly(curve([(-70, -90), (-80, 120), (0, 140), (80, 120), (70, -90), (0, -150)], 3), hc, INK, 3)
        elif st == 'pony':
            p.ell(0, -84, 66, 80, hc, INK, 3)
            p.poly(curve([(-16, -40), (16, -40), (22, 80), (0, 120), (-22, 80)], 3), hc, INK, 2.6)
            p.ell(0, -40, 14, 9, (190, 50, 70), INK, 2)
        elif st == 'bun':
            p.ell(0, -150, 34, 30, hc, INK, 3)
        elif st == 'curly':
            for k in range(10):
                a = math.pi * (1.0 + k / 9.0)
                p.ell(70 * math.cos(a), -84 + 84 * math.sin(a), 22, 22, hc, INK, 2.4)
            p.ell(0, -84, 62, 74, hc, None)
        p.line([(-30, -150), (-20, -100)], B.dk(hc, 0.8), 2)
    if r['props'] == 'pad' and not up:                   # a notepad held up on one shoulder side
        p.poly(rough([(70, 60), (150, 50), (156, 150), (76, 160)], 3, r['seed']), (250, 248, 236), INK, 2.4)


def crowd(img, t):
    """Rows drawn back to front, each with its own depth (nearer rows swell and slide away as we push in)."""
    for f, _, _ in sorted(REPORTER_ROWS, key=lambda r: r[0]):
        cam = cam_at(t, f)
        if cam is None:
            continue
        for r in REPORTERS:
            if r['f'] == f:
                X, Y = cam.P(r['x'], r['y'])
                if -cam.S(300 * r['s']) < X < B.W * B.SS + cam.S(300 * r['s']) and Y < B.H * B.SS + cam.S(420 * r['s']):
                    reporter(img, cam, r, t)


# ------------------------------------------------------------------------------------------------ the frame
def picture(t):
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    img = B.canvas(CREAM)
    backdrop(img, cam_at(t, -0.35), t)
    stage_floor(img, cam_at(t, 0.0))
    cam = cam_at(t)
    her(img, cam, t)
    notes(img, cam)
    podium(img, cam_at(t, 0.04))
    crowd(img, t)
    return img


def overlay(img, t):
    return img


def frame_image(t):
    return overlay(picture(t), t)


# ------------------------------------------------------------------------------------------------ the sheets
def label(img, x, y, s, size=30, colr=(30, 30, 30)):
    f = ImageFont.truetype(B.SANS, size)
    ImageDraw.Draw(img).text((x, y), s, font=f, fill=colr, anchor='mm')


def cast_sheet(out):
    """Her in every expression the film uses (talking, reading her notes, the smile levels, the sigh, the dead
    'Venezuela'), the strength sheet of her smile, and a row of the reporters."""
    B.SS = 1
    W, H = 2160, 2400
    sheet = Image.new('RGB', (W, H), (232, 228, 222))
    base = dict(gaze='up', lid=0.0, brow=0.0, mouth='rest', smile=0, head_dy=0.0, head_tilt=0.0, sh_dy=0.0,
                closed=False, look_x=0.0, squint=0.0, head_dx=0.0)
    looks = [
        ('1  calm, looking at the room', {}),
        ('2  talking', dict(mouth='mid')),
        ('3  reading her notes', dict(gaze='down', lid=0.62, head_dy=10, brow=-2, mouth='small')),
        ('4  smile 1: small, closed', dict(smile=1, brow=4)),
        ('5  smile 2: the big toothy one', dict(smile=2, brow=14, squint=0.5, head_tilt=-0.05)),
        ('6  smile 3: the huge strange one', dict(smile=3, brow=18, squint=0.75, head_tilt=0.05)),
        ('7  the sigh', dict(gaze='down', closed=True, mouth='blow', sh_dy=-14, head_dy=10, brow=3)),
        ('8  "...Venezuela" (flat, dead)', dict(gaze='down', lid=0.72, head_dy=12, brow=-3, mouth='small')),
    ]
    for i, (name, ch) in enumerate(looks):
        col, row = i % 4, i // 4
        tile = Image.new('RGBA', (540, 760), (232, 228, 222, 255))
        bg = B.Pen(tile, B.Cam(1.0, 540, 960))
        cam = B.Cam(1.55, NECK[0], NECK[1] - 140)
        cam.cx, cam.cy = NECK[0], NECK[1] - 140
        st = dict(base, **ch)
        layer = B.canvas(SET_BLUE)
        tc = B.Cam(1.3, NECK[0], NECK[1] + 60)
        her(layer, tc, 0.0, st)
        notes(layer, tc)
        podium(layer, tc)
        crop = layer.convert('RGB').crop((190, 380, 890, 1365)).resize((540, 760))
        sheet.paste(crop, (col * 540, 70 + row * 830))
        label(sheet, col * 540 + 270, 40 + row * 830, name, 26)
    # the whole room, the opening frame, small, and a row of reporters
    wide = picture(0.0).convert('RGB').resize((540, 960))
    sheet.paste(wide.crop((0, 120, 540, 840)), (0, 1700))
    label(sheet, 270, 1675, '9  the room (opening frame)', 26)
    end = picture(PUSH_END + 0.1).convert('RGB').resize((540, 960)).crop((0, 120, 540, 840))
    sheet.paste(end, (540, 1700))
    label(sheet, 810, 1675, '10  the close-up (end of the push)', 26)
    tile = B.canvas((232, 228, 222)).convert('RGBA')
    for i, r in enumerate(REPORTERS[:20:2][:6]):
        rr = dict(r, x=150 + i * 170, y=1300, s=0.55, hand=(i % 2 == 0), up_at=0.0)
        reporter(tile, B.Cam(1.0, 540, 960), rr, 0.0)
    rep = tile.convert('RGB').crop((40, 1000, 1080, 1460)).resize((1040, 460))
    sheet.paste(rep, (1100, 1720))
    label(sheet, 1620, 1675, '11  reporters from behind (all different)', 26)
    sheet.save(out, quality=90)


def stills(out, times):
    B.SS = 1
    n = len(times)
    cols = min(6, n)
    rows = (n + cols - 1) // cols
    tw, th = 360, 640
    sheet = Image.new('RGB', (cols * tw, rows * (th + 44)), (20, 20, 20))
    for i, t in enumerate(times):
        im = frame_image(t).convert('RGB').resize((tw, th))
        sheet.paste(im, ((i % cols) * tw, (i // cols) * (th + 44) + 44))
        label(sheet, (i % cols) * tw + tw // 2, (i // cols) * (th + 44) + 22, f'{t:.1f}s  {beat_name(t)}', 22,
              (240, 240, 240))
    sheet.save(out, quality=88)


def beat_name(t):
    if t >= BLACK_AT:
        return 'black'
    k, a, b, arg = next((x for x in BEATS if x[1] <= t < x[2]), BEATS[-1])
    if k == 'say':
        words = next((w for (s, e, w) in TALK if s <= t < e), '')
        return f'"{words}"'
    return {'smile': f'smile {arg}', 'look': f'looks {arg}', 'sigh': 'SIGH', 'hold': 'hold', 'gap': '(pause)'}[k]


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        cast_sheet(a[1])
    elif a[0] == 'stills':
        stills(a[1], [float(x) for x in a[2:]])
    elif a[0] == 'timeline':
        print(f'length {END:.1f} s, push ends {PUSH_END:.1f} s')
        for k, s, e, arg in BEATS:
            if k != 'gap':
                print(f'{s:5.1f}-{e:5.1f}  {beat_name((s + e) / 2)}')
    elif a[0] == 'final':
        import film_engine as E
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=lambda t: 'push', sound=lambda: np.zeros(int((DUR + 0.3) * 48000)),
                 write_wav=None, set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 22,
                 reuse='--reuse' in a, redo=())


if __name__ == '__main__':
    main()
