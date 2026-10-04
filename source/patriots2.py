#!/usr/bin/env python3
"""The Patriots 2: the protester writes the RNLI a letter, has a heart attack, and the NHS treats him the way he
wanted the RNLI to treat others (prompts/patriots-2.md).

Same look as The Patriots and Mossad (peepee.py, mossad.py, burnham.py): flat shapes, clean black outlines,
almond eyes with small pupils, soft shading, deadpan staging, hard cuts. Made vertical (1080 x 1920); faces
and text inside TikTok's safe area (x 60-900, y 310-1500).

The protester is the same man as in The Patriots (peepee.protester): black balaclava, black jacket, combat
trousers, the "PP" badge and his felt-tip doodle badge. Everyone else is invented. Real organisations are only
suggested: a navy-hulled lifeboat with an orange top and crew in yellow; green and yellow checks and the word
AMBULANCE; a generic "A&E" sign. No logos, no brands (plain cans, plain takeaway tubs).

Every line is Sam's own recording (REC below): the cuts, mouths, keyboard clicks and captions follow it.

Usage:
    python3 patriots2.py stills OUT_DIR T1 T2 ...   frames at those times (seconds), full size
    python3 patriots2.py sheet OUT.jpg              the storyboard sheet
    python3 patriots2.py animatic OUT.mp4           half size, quick, to check timing
    python3 patriots2.py final OUT.mp4              full size
"""
import math
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import burnham as B
import peepee as PP          # the protester, his badges, ctext, Rot, the series' caption
import mossad as M           # brows, mouths, hair styles and head tilt (patched into burnham on import)
import mossad_audio as MA
from burnham_film import onepole_lp, normal, reverb
from ed import INK, curve, oval, smooth, soft

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 12
SR = 48000
TITLE = 'THE PATRIOTS 2'

# ------------------------------------------------------------------------------------------- timeline
# Placeholder timing from a natural pace (Sam's own pace on The Patriots and Mossad was 3.0-3.6 words a second).
# Each line: (who, start, words a second, caption pieces). Word times are worked out from the pace, with short
# pauses at commas and full stops; each caption piece shows from its first word to the next piece.
LINE_DEFS = [
    ('pro', 0.35, 3.4, ['Dear RNLI.', 'As a British patriot, I have the deepest respect', 'for your work saving lives at sea.',
                        'However, I have some concerns.']),
    ('pro', None, 3.4, ['I recognise the courage and resilience', 'your people require to do what they do.']),
    ('pro', None, 3.4, ["What you've failed to consider", "is that some of the so-called 'people'", 'you go to rescue',
                        "are those who I personally don't like."]),
    ('pro', None, 3.5, ['The lot of you are, on reflection, traitors.', 'Consider this the start',
                        'of a lengthy campaign of harassment', 'in which I shall-']),
    ('para', None, 3.6, ["He's treating us like a bloody taxi service."]),
    ('para', None, 3.6, ["We believe it's a heart attack, Doctor."]),
    ('doc', None, 3.3, ['This is an urgent situation.', 'This man is clearly in serious danger.', 'Unfortunately,',
                        "I just don't like him personally.", 'Shall we go get lunch?']),
]


# Sam's recordings (source/audio/patriots2-*.m4a), cleaned and levelled by mossad_audio.line, otherwise exactly as
# recorded. Line index -> (file, from, to, caption pieces with their start in the recording). Captions follow Sam's
# words; piece starts sit on his own pauses.
REC = {
    0: ('patriots2-protester-1', 0.40, 11.90, [('Dear RNLI.', 0.49), ('As a British patriot, I have the deepest respect', 3.10),
                                               ('for your work saving lives at sea.', 6.60), ('However, I have some concerns.', 9.38)]),
    1: ('patriots2-protester-2', 0.40, 5.90, [('I recognise the courage', 0.50), ('and resilience your people require', 2.27),
                                               ('to do what they do.', 4.64)]),
    2: ('patriots2-protester-3', 0.35, 8.85, [("What you've failed to consider", 0.46), ("is that some of the so-called 'people'", 2.13),
                                               ('you go to rescue', 4.87), ("are those who I personally don't like.", 6.43)]),
    3: ('patriots2-protester-4', 0.62, 8.80, [('The lot of you are, on reflection, traitors.', 0.77),
                                               ('Consider this the start', 4.32), ('of a lengthy campaign of harassment', 5.45),
                                               ('in which I shall-', 7.60)]),
    4: ('patriots2-paramedic-1', 0.90, 3.80, [("He's treating us like a bloody taxi service.", 1.04)]),
    5: ('patriots2-paramedic-2', 0.90, 3.30, [("We believe it's a heart attack, Doctor.", 1.02)]),
    6: ('patriots2-doctor-1', 2.20, 11.05, [('This is an urgent situation.', 2.34), ('This man is clearly in serious danger.', 4.27),
                                             ('Unfortunately,', 7.30), ("I just don't like him personally.", 8.20),
                                             ('Shall we go get lunch?', 9.95)]),
}
GURGLE = ('patriots2-protester-gurgle', 0.20, 2.60)
CHOKE = ('patriots2-protester-choke', 0.30, 2.70)   # his strangled noise as his eyes cross


def word_times(start, wps, pieces, short=False):
    """[(word, start, end, piece index)] from the pace, with pauses after punctuation."""
    out, t = [], start
    stop, comma = (0.2, 0.1) if short else (0.32, 0.15)
    for i, piece in enumerate(pieces):
        for w in piece.split():
            d = (0.62 + 0.38 * min(2.0, len(re.sub(r'\W', '', w)) / 4.5)) / wps
            out.append((w, t, t + d, i))
            t += d
            if w[-1] in '.?':
                t += stop
            elif w[-1] == ',':
                t += comma
    return out


# Where things happen. Each line's start is fixed relative to the shot it sits in.
T = {}
LINES = []


def build_timeline():
    """Lay the lines and shots end to end. Every number that matters is here."""
    t = 0.0
    words = []

    def line(i, at):
        who, _, wps, pieces = LINE_DEFS[i]
        if i in REC:
            f, s0, s1, pcs = REC[i]
            starts = [at + pt - s0 for _, pt in pcs] + [at + s1 - s0]
            w = [(txt, starts[k], starts[k + 1], k) for k, (txt, _) in enumerate(pcs)]
            LINES.append((who, at, at + s1 - s0, [txt for txt, _ in pcs], w, (f, s0, s1)))
            return at + s1 - s0
        w = word_times(at, wps, pieces, short=(who == 'doc'))
        LINES.append((who, at, w[-1][2], pieces, w, None))
        return w[-1][2]
    end1 = line(0, 0.30)                       # 1. his room: the letter begins at once
    T['knock'] = 3.7                           #    his hand nudges a can (it wobbles and clinks)
    T['s2'] = end1 + 0.25                      # 2. the lifeboat
    end2 = line(1, T['s2'] + 0.2)
    T['s3'] = end2 + 0.25                      # 3. the dinghy
    end3 = line(2, T['s3'] + 0.2)
    T['s4'] = end3 + 0.3                       # 4. his room, from the screen's side
    end4 = line(3, T['s4'] + 0.2)
    T['cut_off'] = end4                        #    "in which I shall-"
    T['cross'] = end4 + 0.05                   #    his eyes cross, a strangled sound
    T['clutch'] = end4 + 0.25                  #    he clutches his chest
    T['topple'] = end4 + 1.55                  #    and topples sideways out of frame, on the second choke
    T['crash'] = end4 + 1.95
    T['can'] = end4 + 1.85                     #    a can rolls off the desk
    T['s5'] = end4 + 2.65                      # 5. the ambulance (after his choke has ended)
    end5 = line(4, T['s5'] + 0.45)
    T['eyeroll'] = end5 - 0.15
    T['s6'] = end5 + 0.7                       # 6a. A&E: the doors bang open, the trolley rushed through
    T['s6w'] = T['s6'] + 1.5                   # 6b. pushed fast into the ward
    T['stop'] = T['s6w'] + 0.95                #     skids to a halt in the bay, by the doctor
    end6 = line(5, T['s6w'] + 0.75)            #     "We believe it's a heart attack, Doctor."
    T['nod'] = end6 + 0.05
    T['s6b'] = end6 + 0.45                     # 6c. the doctor, unbroken
    end7 = line(6, T['s6b'] + 0.3)
    T['agree'] = end7 + 0.15                   #     everyone nods
    T['leave'] = end7 + 0.7                    #     and they all walk off together, chatting
    T['s7'] = end7 + 2.1                       # 7. alone in the bay
    T['gurgle'] = T['s7'] + 0.55
    T['black'] = T['gurgle'] + (GURGLE[2] - GURGLE[1]) + 0.2   # hard cut to black, just after the gurgle
    T['dur'] = T['black'] + 0.35


build_timeline()
SHOTS = [('room', 0.0, T['s2']),
         ('lifeboat', T['s2'], T['s3']), ('dinghy', T['s3'], T['s4']), ('screen', T['s4'], T['s5']),
         ('ambulance', T['s5'], T['s6']), ('ae', T['s6'], T['s6w']), ('ward', T['s6w'], T['s6b']),
         ('doctor', T['s6b'], T['s7']),
         ('alone', T['s7'], T['black'])]
BLACK_AT, DUR = T['black'], T['dur']


ENVS = {}


def envelope(rec):
    """Loudness of a stretch of a cleaned recording, 100 times a second, 0-1."""
    if rec not in ENVS:
        f, s0, s1 = rec
        a = MA.line(f)[int(s0 * SR):int(s1 * SR)]
        hop = SR // 100
        lv = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
        ENVS[rec] = np.clip(lv / (np.percentile(lv, 95) + 1e-9), 0, 1)
    return ENVS[rec]


def level(who, t):
    """How loud this person's voice is now (0-1): from the recording, or a simple talking rhythm for a placeholder."""
    t += 1.0 / FPS  # the mouth leads the sound by a frame
    for w_, a, b, _, words, rec in LINES:
        if w_ != who or not (a <= t < b):
            continue
        if rec:
            lv = envelope(rec)
            return float(lv[min(int((t - a) * 100), len(lv) - 1)])
        for w, s, e, _ in words:
            if s <= t < e:
                n = max(1, round(len(re.sub(r'\W', '', w)) / 3))
                u = (t - s) / (e - s)
                return float(0.15 + 0.85 * abs(math.sin(math.pi * n * u)))
        return 0.0
    return 0.0


def syllables():
    """(time, who) of every syllable, for the keyboard clicks: the peaks of the recorded voice, or the placeholder pace."""
    from scipy.signal import find_peaks
    out = []
    for who, a, b, _, words, rec in LINES:
        if rec:
            lv = np.convolve(envelope(rec), np.hanning(7) / np.hanning(7).sum(), 'same')
            pk, _ = find_peaks(lv, distance=12, prominence=0.12, height=0.15)
            out += [(a + k / 100, who) for k in pk]
            continue
        for w, s, e, _ in words:
            n = max(1, round(len(re.sub(r'\W', '', w)) / 3))
            out += [(s + (e - s) * k / n, who) for k in range(n)]
    return out


SYL = syllables()
TYPING = [(a, b) for a, b in ((0.0, T['s2']), (T['s4'], T['cut_off']))]
CLICKS = [s for s, who in SYL if who == 'pro' and any(a <= s < b for a, b in TYPING)]


def tap(t, phase=0.0):
    """How far a typing finger is pressed (0-1): a quick jab on each click."""
    k = sum(math.exp(-((t - c - phase) / 0.035) ** 2) for c in CLICKS if abs(t - c - phase) < 0.15)
    return min(1.0, k)


def shot_at(t):
    for v, a, b in SHOTS:
        if a <= t < b:
            return v, t - a
    return 'black', 0.0


# ------------------------------------------------------------------------------------------- colours
NIGHT_WALL = (96, 92, 108)
CARPET = (84, 70, 70)
DESK = (122, 92, 66)
DESK_D = (86, 64, 46)
PLASTIC = (46, 48, 54)
CAN_GOLD = (206, 170, 70)
CAN_GREEN = (64, 120, 78)
CAN_SILVER = (196, 200, 206)
FOIL = (200, 204, 210)
CURRY = (196, 110, 40)
HULL = (24, 40, 80)
LIFE_ORANGE = (238, 112, 30)
CREW_YELLOW = (244, 204, 40)
JACKET_ORANGE = (240, 118, 34)
SEA = (98, 112, 116)
SEA_D = (70, 84, 90)
SKY = (164, 170, 174)
DINGHY = (112, 116, 122)
PARA_GREEN = (46, 92, 70)
SCRUBS = (52, 78, 132)
SCRUBS_L = (120, 168, 206)
HOSP_WALL = (226, 232, 230)
HOSP_FLOOR = (196, 204, 198)
CURTAIN = (138, 176, 200)
CHECK_GREEN = (40, 150, 70)
CHECK_YELLOW = (248, 220, 30)


# --------------------------------------------------------------------------------------- small helpers

def world_of(cam, X, Y):
    """Canvas pixel -> world point."""
    return ((X / B.SS - B.W / 2) / cam.z + cam.cx, (Y / B.SS - B.H / 2) / cam.z + cam.cy)


def with_legs(fn, legs_fn):
    """Run a drawing call with burnham's legs swapped (seated, walking or hidden)."""
    keep = B.legs
    B.legs = legs_fn
    try:
        return fn()
    finally:
        B.legs = keep


def seated_legs(img, p, sp):
    """Sitting: thighs coming forward to the knees, shins down to the feet (mostly hidden by the desk)."""
    tc = sp.get('trousers', PP.COMBAT)
    for sgn in (-1, 1):
        p.poly([(sgn * 8, 430), (sgn * 120, 430), (sgn * 130, 560), (sgn * 20, 570)], B.dk(tc, 0.9), INK, 2.6)
        p.poly([(sgn * 30, 560), (sgn * 126, 556), (sgn * 118, 820), (sgn * 44, 822)], tc, INK, 2.6)
        p.poly(curve([(sgn * 36, 812), (sgn * 124, 810), (sgn * 150, 832), (sgn * 146, 850), (sgn * 30, 850)], 4),
               (22, 20, 22), INK, 2.4)


def walking_legs(phase, stride=46, lift_h=18):
    def legs(img, p, sp):
        tc = sp.get('trousers', (40, 40, 46))
        for k, sgn in enumerate((-1, 1)):
            sw = stride * math.sin(phase + k * math.pi)
            lift = max(0.0, lift_h * math.sin(phase + k * math.pi + 1.2))
            leg = [(sgn * 6, 440), (sgn * 104, 440), (sgn * 100 + sw * 0.5, 700), (sgn * 90 + sw, 900 - lift),
                   (sgn * 30 + sw, 902 - lift), (sgn * 18 + sw * 0.5, 700)]
            p.poly(leg, tc, INK, 2.6)
            fx = sw
            p.poly(curve([(sgn * 24 + fx, 896 - lift), (sgn * 94 + fx, 894 - lift), (sgn * 128 + fx, 910 - lift),
                          (sgn * 124 + fx, 928 - lift), (sgn * 20 + fx, 928 - lift)], 4), (22, 20, 22), INK, 2.4)
    return legs


def person(img, cam, x, y, s, sp, t, legs=None, flip=1):
    """Everyone has legs and feet, always (the set may hide them; nothing here can leave them out).
    legs: standing (None), seated_legs or walking_legs(...)."""
    sp = dict(sp, full=True)
    if legs is None:
        return B.person(img, cam, x, y, s, sp, t, flip)
    assert legs in (seated_legs,) or legs.__name__ == 'legs', 'legs must be drawn'
    return with_legs(lambda: B.person(img, cam, x, y, s, sp, t, flip), legs)


def eyes_over(img, cam, x, y, s, sp, dx=0.0, dy=0.0, cross=0.0, lid=None, bala=False):
    """Redraw a person's eyes with the pupils placed freely: rolled up, crossed, glancing about."""
    L = B.Local(cam, x, y + sp.get('sit', 0.0) * 230 * s, s)
    tilt = sp.get('tilt', 0.0)
    R = PP.Rot(L, tilt, pivot=(0, -60)) if tilt else L
    p = B.Pen(img, R)
    hx, hy = sp.get('head_dx', 0.0), -150 + sp.get('head_dy', 0.0)
    hw = 76 if bala else sp.get('hw', 72)
    turn = sp.get('turn', 0.0)
    fx = hx + turn * hw * 0.22
    skin = PP.EYE_SKIN if bala else sp['skin']
    lid = sp.get('lid', 0) if lid is None else lid
    for sgn in (-1, 1):
        ex, ey = (fx - 2 + sgn * 30, hy - 14) if bala else (fx - 4 + sgn * 30, hy - 8)
        p.poly([(ex - 17, ey), (ex - 8, ey - 8), (ex + 8, ey - 8), (ex + 17, ey), (ex + 8, ey + 7), (ex - 8, ey + 7)],
               (250, 250, 248), INK, 2.0)
        px = ex + dx * 7 - sgn * cross * 8
        py = ey + 1 + dy * 4
        p.ell(px, py, 4.5, 4.5, INK, None)
        if lid > 0:
            p.poly([(ex - 18, ey - 2), (ex - 8, ey - 10), (ex + 8, ey - 10), (ex + 18, ey - 2), (ex + 17, ey - 1 + lid),
                    (ex + 8, ey - 9 + lid), (ex - 8, ey - 9 + lid), (ex - 17, ey - 1 + lid)], B.dk(skin, 0.84), None)
        p.line([(ex - 17, ey - 1 + lid), (ex - 8, ey - 9 + lid), (ex + 8, ey - 9 + lid), (ex + 17, ey - 1 + lid)], INK, 2.6)


def light_pass(img, cam, lights, ambient=(0.13, 0.15, 0.26), sheen=(10, 20, 44)):
    """Night: everything sinks into near-black blue, except where the screen's cool light falls."""
    w, h = img.size
    q = 8
    gw, gh = w // q, h // q
    X, Y = np.meshgrid((np.arange(gw) + 0.5) * q, (np.arange(gh) + 0.5) * q)
    Lm = np.zeros((gh, gw, 3))
    for (lx, ly, r, colr, sq) in lights:
        PX, PY = cam.P(lx, ly)
        R = cam.S(r)
        d2 = ((X - PX) / R) ** 2 + ((Y - PY) / (R * sq)) ** 2
        Lm += np.exp(-d2)[..., None] * np.array(colr)[None, None, :]
    mult = np.array(ambient)[None, None, :] + Lm
    lm = Image.fromarray(np.clip(mult * 100, 0, 255).astype(np.uint8), 'RGB').resize((w, h), Image.BILINEAR)
    add = Image.fromarray(np.clip(np.clip(Lm, 0, 1) * np.array(sheen)[None, None, :], 0, 255).astype(np.uint8),
                          'RGB').resize((w, h), Image.BILINEAR)
    a = np.asarray(img.convert('RGB'), dtype=np.float32)
    out = a * (np.asarray(lm, dtype=np.float32) / 100.0) + np.asarray(add, dtype=np.float32)
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGB').convert('RGBA'))


def glow_spot(img, cam, x, y, rx, ry, colr, alpha):
    soft(img, cam, oval(x, y, rx, ry, 28), colr, alpha, max(rx, ry) * 0.5)


# ------------------------------------------------------------------------------------------ the props

def can(img, cam, x, y, h, colr=CAN_GOLD, crushed=False, lying=0.0, seed=0):
    """A plain lager can (no brand), standing with its base centre at (x, y), h tall. lying: turned on its side."""
    p = B.Pen(img, cam)
    w = h * 0.55
    if lying:
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        can(lay, cam, x, y, h, colr, crushed, 0.0, seed)
        X, Y = cam.P(x, y - w / 2)
        img.alpha_composite(lay.rotate(math.degrees(lying), Image.BICUBIC, center=(X, Y)))
        return
    if crushed:
        rng = np.random.default_rng(seed)
        pts = []
        for k in range(6):
            pts.append((x - w / 2 + rng.uniform(-6, 6) * h / 100, y - h * k / 5 * 0.6))
        for k in range(5, -1, -1):
            pts.append((x + w / 2 + rng.uniform(-8, 8) * h / 100 - (k % 2) * w * 0.25, y - h * k / 5 * 0.6))
        p.poly(pts, colr, INK, 2.2)
        p.poly([(x - w * 0.3, y - h * 0.32), (x + w * 0.25, y - h * 0.4), (x + w * 0.1, y - h * 0.2)], B.dk(colr, 0.75), None)
        p.line([(x - w * 0.4, y - h * 0.15), (x + w * 0.3, y - h * 0.22)], B.lt(colr, 1.3), 1.6)
        return
    p.poly([(x - w / 2, y - h * 0.9), (x + w / 2, y - h * 0.9), (x + w / 2, y - h * 0.05), (x - w / 2, y - h * 0.05)], colr, INK, 2.2)
    p.ell(x, y - h * 0.04, w / 2 * 0.92, h * 0.05, CAN_SILVER, INK, 2.0)
    p.poly([(x - w / 2, y - h * 0.9), (x - w * 0.38, y - h), (x + w * 0.38, y - h), (x + w / 2, y - h * 0.9)], CAN_SILVER, INK, 2.0)
    p.ell(x, y - h, w * 0.38, h * 0.045, (170, 174, 180), INK, 1.6)
    p.poly([(x - w / 2, y - h * 0.62), (x + w / 2, y - h * 0.62), (x + w / 2, y - h * 0.5), (x - w / 2, y - h * 0.5)],
           (244, 240, 230), None)  # a plain band, no name
    p.line([(x - w * 0.28, y - h * 0.86), (x - w * 0.28, y - h * 0.1)], B.lt(colr, 1.35), 2.2)


def foil_tray(img, cam, x, y, w, lid_off=0.0):
    """An empty foil takeaway tray with sauce smeared round it; its card lid askew beside it."""
    p = B.Pen(img, cam)
    h = w * 0.36
    p.poly([(x - w / 2, y - h), (x + w / 2, y - h), (x + w * 0.44, y), (x - w * 0.44, y)], FOIL, INK, 2.2)
    p.poly([(x - w * 0.44, y - h * 0.86), (x + w * 0.44, y - h * 0.86), (x + w * 0.38, y - h * 0.35),
            (x - w * 0.38, y - h * 0.35)], B.dk(FOIL, 0.85), None)
    for k in range(3):
        p.line([(x - w * 0.3 + k * w * 0.22, y - h * 0.7), (x - w * 0.2 + k * w * 0.2, y - h * 0.45)], CURRY, 3.0)
    for k in range(5):
        p.line([(x - w * 0.46 + k * w * 0.22, y - h * 0.95), (x - w * 0.42 + k * w * 0.22, y - h * 0.05)], B.lt(FOIL, 1.1), 1.2)
    if lid_off:
        lx = x + w * 0.55 * lid_off
        p.poly([(lx - w * 0.5, y - h * 1.15), (lx + w * 0.48, y - h * 1.45), (lx + w * 0.55, y - h * 1.2),
                (lx - w * 0.42, y - h * 0.92)], (236, 232, 222), INK, 2.0)


def tub(img, cam, x, y, w, lid=0.0):
    """A round plastic takeaway tub, scraped out; its lid tipped against it."""
    p = B.Pen(img, cam)
    h = w * 0.55
    p.poly([(x - w / 2, y - h), (x + w / 2, y - h), (x + w * 0.42, y), (x - w * 0.42, y)], (232, 234, 236), INK, 2.2)
    p.ell(x, y - h, w / 2, w * 0.14, (226, 228, 230), INK, 2.0)
    p.ell(x, y - h, w * 0.44, w * 0.1, (214, 140, 60), None)
    p.ell(x + w * 0.08, y - h, w * 0.25, w * 0.05, (236, 236, 236), None)
    if lid:
        p.ell(x + w * 0.4 * lid, y - h * 1.35, w * 0.5, w * 0.16, (220, 224, 230), INK, 2.0, rot=-0.5 * lid)


def keyboard(img, cam, x, y, w, depth, press=0.0, far=False):
    """A plain dark keyboard: (x, y) the middle of its front edge."""
    p = B.Pen(img, cam)
    d = depth
    p.poly([(x - w / 2, y), (x + w / 2, y), (x + w / 2 - d * 0.18, y - d), (x - w / 2 + d * 0.18, y - d)], PLASTIC, INK, 2.2)
    rows = 4
    for r in range(rows):
        v0, v1 = (r + 0.15) / rows, (r + 0.85) / rows
        n = 13
        for k in range(n):
            u0, u1 = (k + 0.12) / n, (k + 0.88) / n

            def at(u, v):
                half = w / 2 - d * 0.18 * v
                return (x - half + 2 * half * u, y - d * v)
            col = (74, 76, 84)
            p.poly([at(u0, v0), at(u1, v0), at(u1, v1), at(u0, v1)], col, None)
    if far:
        p.line([(x - w / 2 + d * 0.18, y - d), (x + w / 2 - d * 0.18, y - d)], (90, 92, 100), 2.0)


def mouse(img, cam, x, y, s):
    p = B.Pen(img, cam)
    p.ell(x, y, 26 * s, 18 * s, PLASTIC, INK, 2.0)
    p.line([(x - 6 * s, y - 14 * s), (x - 4 * s, y - 2 * s)], (90, 92, 100), 1.4)


def office_chair(img, cam, x, y, s, back=True):
    """An office chair: x, y the middle of the seat; back drawn behind the sitter."""
    p = B.Pen(img, cam)
    if back:
        p.poly(curve([(x - 150 * s, y - 40 * s), (x - 160 * s, y - 380 * s), (x, y - 430 * s), (x + 160 * s, y - 380 * s),
                      (x + 150 * s, y - 40 * s)], 4), (34, 34, 40), INK, 2.4)
        return
    p.poly([(x - 170 * s, y - 20 * s), (x + 170 * s, y - 20 * s), (x + 160 * s, y + 30 * s), (x - 160 * s, y + 30 * s)],
           (34, 34, 40), INK, 2.4)
    p.line([(x, y + 30 * s), (x, y + 250 * s)], (90, 92, 98), max(2, 22 * s))
    for k in range(-2, 3):
        p.line([(x, y + 250 * s), (x + k * 110 * s, y + 300 * s)], (40, 40, 46), max(2, 16 * s))
        p.ell(x + k * 110 * s, y + 310 * s, 16 * s, 12 * s, (24, 24, 28), INK, 1.4)


# -------------------------------------------------------------------------------------- the protester

def pro_st(t, **kw):
    lv = level('pro', t)
    st = dict(arms=PP.REST, turn=0.0, look=0.0, lid=3, brows='flat', puff=0.3, shrug=0.0, tilt=0.0, head_dx=0.0,
              head_dy=-4 * lv, lv=lv, blink=M.blinking(t, (2.6, 6.9, 11.0, 23.4, 26.0)))
    st.update(kw)
    return st


def seated_protester(img, cam, x, y, s, st, t):
    with_legs(lambda: PP.protester(img, cam, x, y, s, st, t), seated_legs)


# ----------------------------------------------------------------------------------- shot 1: his room

ROOM_LIGHT = (330, 900)


def room_set(img, cam, t):
    p = B.Pen(img, cam)
    p.poly([(-400, -200), (1500, -200), (1500, 1500), (-400, 1500)], NIGHT_WALL, None)
    p.poly([(-400, 1350), (1500, 1350), (1500, 2400), (-400, 2400)], CARPET, None)
    p.line([(-400, 1350), (1500, 1350)], B.dk(CARPET, 0.7), 3)
    p.poly([(-400, 140), (1500, 140), (1500, 170), (-400, 170)], B.dk(NIGHT_WALL, 0.85), None)
    # the window behind him, curtains drawn tight, a slit of orange street light
    p.poly([(700, 300), (1060, 300), (1060, 760), (700, 760)], (60, 60, 84), INK, 2.4)
    p.poly([(690, 280), (884, 280), (880, 790), (694, 800)], (92, 58, 66), INK, 2.4)
    p.poly([(876, 280), (1072, 280), (1068, 800), (880, 790)], (92, 58, 66), INK, 2.4)
    p.line([(882, 300), (881, 780)], (210, 150, 80), 2.0)
    for k in range(4):
        p.line([(720 + k * 44, 300), (716 + k * 46, 790)], (74, 46, 54), 1.8)
        p.line([(900 + k * 44, 300), (904 + k * 44, 790)], (74, 46, 54), 1.8)
    p.line([(660, 276), (1100, 276)], (60, 52, 50), 6)
    # a shelf: a dartboard and some clutter
    p.ell(240, 470, 74, 74, (40, 40, 40), INK, 2.4)
    for r, c in ((60, (220, 60, 50)), (46, (232, 222, 196)), (30, (60, 140, 70)), (12, (220, 60, 50))):
        p.ell(240, 470, r, r, c, None)
    p.poly([(-40, 640), (420, 640), (420, 660), (-40, 660)], DESK_D, INK, 2.0)
    for k, (bx, bh, c) in enumerate(((30, 90, (120, 40, 40)), (70, 110, (40, 70, 110)), (110, 80, (190, 170, 120)))):
        p.poly([(bx, 640 - bh), (bx + 36, 640 - bh), (bx + 36, 640), (bx, 640)], c, INK, 1.8)
    can(img, cam, 260, 640, 64, CAN_GREEN)
    can(img, cam, 320, 640, 64, CAN_GOLD, crushed=True, seed=3)


def desk_front(img, cam, t, knock=0.0):
    """The desk between us and him, with the debris of the evening."""
    p = B.Pen(img, cam)
    p.poly([(-300, 1080), (1400, 1080), (1400, 1150), (-300, 1150)], DESK, INK, 2.6)
    p.poly([(-300, 1150), (1400, 1150), (1400, 1185), (-300, 1185)], DESK_D, INK, 2.4)
    p.poly([(-300, 1185), (1400, 1185), (1400, 1700), (-300, 1700)], (40, 32, 30), None)   # under the desk: darkness
    for X in (-120, 1250):
        p.poly([(X, 1185), (X + 40, 1185), (X + 40, 1700), (X, 1700)], DESK_D, INK, 2.0)


def room_props(img, cam, t, knock=0.0):
    foil_tray(img, cam, 760, 1128, 190, lid_off=0.6)
    tub(img, cam, 975, 1120, 110, lid=1.0)
    tub(img, cam, 180, 1140, 96, lid=-0.8)
    can(img, cam, 900, 1146, 96, CAN_GOLD)
    can(img, cam, 1010, 1150, 96, CAN_GREEN, crushed=True, seed=1)
    can(img, cam, 60, 1150, 96, CAN_GOLD, crushed=True, seed=4)
    can(img, cam, 700, 1104, 90, CAN_GREEN, lying=knock)


def monitor_back(img, cam, t):
    """The monitor in the foreground on the left, seen from behind and the side, its screen facing him."""
    p = B.Pen(img, cam)
    p.poly([(250, 1086), (330, 1086), (318, 1050), (262, 1050)], PLASTIC, INK, 2.2)
    p.poly([(276, 1050), (306, 1050), (300, 980), (282, 980)], PLASTIC, INK, 2.2)
    p.poly([(60, 700), (370, 740), (380, 1010), (70, 1040)], (36, 38, 44), INK, 2.6)
    p.poly([(370, 740), (404, 748), (412, 1002), (380, 1010)], (70, 74, 82), INK, 2.2)
    p.poly([(140, 790), (300, 806), (306, 950), (146, 964)], (44, 46, 52), None)


def room_emissive(img, cam, t):
    """The screen's glow spilling round its edge (drawn after the night pass)."""
    p = B.Pen(img, cam)
    p.line([(404, 750), (412, 1000)], (190, 220, 255), 4)
    glow_spot(img, cam, 440, 880, 70, 150, (150, 200, 255), 0.35)


def shot_room(t):
    """1. The dark box room, a slow push-in from the upper left towards his lit face, moving from frame one."""
    k = smooth(t / T['s2'])
    cam = B.Cam(1.22 + 0.6 * k, 560 + 70 * k, 960 - 110 * k)
    img = B.canvas()
    room_set(img, cam, t)
    x, y, s = 650, 860, 0.8
    office_chair(img, cam, x, y + 330 * s, s, back=True)
    st = pro_st(t, turn=-0.55, look=-1.0, lid=3, head_dx=-14, tilt=-0.04)
    tp = tap(t)
    tp2 = tap(t, 0.06)
    st['arms'] = {'L': ((-235, 230), (-252, 300 + 24 * tp), 'point'),
                  'R': ((125, 240), (-55, 300 + 24 * tp2), 'point')}
    seated_protester(img, cam, x, y, s, st, t)
    desk_front(img, cam, t)
    keyboard(img, cam, 520, 1140, 420, 46)
    for side in ('L', 'R'):  # his forearms resting over the desk, hands on the keys
        PP.protester(img, cam, x, y, s, dict(st, arm_only=side), t)
    mouse(img, cam, 820, 1150, 1.0)
    kn = t - T['knock']
    room_props(img, cam, t, knock=0.18 * math.sin(kn * 22) * math.exp(-kn * 5) if kn > 0 else 0.0)
    monitor_back(img, cam, t)
    light_pass(img, cam, [(ROOM_LIGHT[0] + 270, 860, 250, (0.72, 0.9, 1.15), 1.35), (540, 1120, 260, (0.45, 0.58, 0.8), 0.45)],
               ambient=(0.07, 0.08, 0.16))
    room_emissive(img, cam, t)
    return img


def shot_insert(t):
    """1b. His fingers jabbing the keys beside a can."""
    cam = B.Cam(1.0, 540, 960)
    img = B.canvas()
    p = B.Pen(img, cam)
    p.poly([(-20, -20), (1100, -20), (1100, 2000), (-20, 2000)], DESK, None)
    for k in range(9):
        p.line([(-20, 300 + 200 * k), (1100, 260 + 200 * k)], B.dk(DESK, 0.92), 2)
    # the keyboard, big and close
    x0, y0 = -80, 760
    for r in range(4):
        for c in range(7):
            kx, ky = x0 + c * 170 + r * 24, y0 + r * 170
            p.poly([(kx, ky), (kx + 150, ky), (kx + 150, ky + 150), (kx, ky + 150)], (54, 56, 62), INK, 2.4)
            p.poly([(kx + 14, ky + 10), (kx + 136, ky + 10), (kx + 132, ky + 120), (kx + 18, ky + 120)], (74, 76, 84), None)
    p.poly([(x0 - 40, y0 - 40), (x0 + 1260, y0 - 40), (x0 + 1260, y0 - 10), (x0 - 40, y0 - 10)], PLASTIC, INK, 2.4)
    # a lager can standing by the keyboard, and a crushed one
    can(img, cam, 820, 700, 360, CAN_GOLD)
    can(img, cam, 160, 690, 300, CAN_GREEN, crushed=True, seed=7)
    # two hands seen from behind, fingers curled, each index finger jabbing down onto a key
    sk, skd = PP.EYE_SKIN, B.dk(PP.EYE_SKIN, 0.82)
    for side, (sx, phase) in enumerate(((300, 0.0), (650, 0.06))):
        sgn = -1 if side == 0 else 1
        tp = tap(t + T['insert'][0], phase)
        hy = 1180 - 30 * tp        # the hand dips forward onto the key
        B.arm(p, (sx - sgn * 160, 2150), (sx - sgn * 90, 1700), (sx - sgn * 20, hy + 230), PP.SLEEVE, w=120)
        # the index finger: short (seen end-on, pointing away and down), a nail at its tip
        fx = sx + sgn * 62
        p.poly(curve([(fx - 34, hy - 30), (fx - 30, hy - 150 + 20 * tp), (fx, hy - 172 + 20 * tp), (fx + 30, hy - 150 + 20 * tp),
                      (fx + 34, hy - 30)], 4), sk, INK, 3)
        p.poly(curve([(fx - 18, hy - 140 + 20 * tp), (fx, hy - 160 + 20 * tp), (fx + 18, hy - 140 + 20 * tp), (fx, hy - 122 + 20 * tp)], 3),
               (246, 222, 210), INK, 1.8)
        p.line([(fx - 22, hy - 92 + 10 * tp), (fx + 22, hy - 92 + 10 * tp)], skd, 2.0)
        # the back of the hand, the other three fingers curled under: knuckle bumps
        back = [(sx - 130, hy + 40), (sx - 120, hy - 50), (sx - 70, hy - 70), (sx + 70, hy - 70), (sx + 120, hy - 50),
                (sx + 130, hy + 40), (sx + 100, hy + 190), (sx - 100, hy + 190)]
        p.poly(curve(back, 4), sk, INK, 3)
        for kk in range(3):
            kx = sx - sgn * (90 - 50 * kk) - sgn * 10
            p.ell(kx, hy - 52, 30, 22, sk, INK, 2.4)
        p.poly(curve([(sx - sgn * 150, hy + 60), (sx - sgn * 170, hy - 10), (sx - sgn * 120, hy - 30), (sx - sgn * 96, hy + 40)], 3),
               sk, INK, 2.6)   # the thumb tucked at the side
        for kk in range(3):
            p.line([(sx - 60 + 50 * kk, hy + 10), (sx - 50 + 46 * kk, hy + 130)], skd, 2.0)
        p.ell(fx, hy - 172 + 20 * tp + 12, 40, 10, (30, 30, 34), None)
    light_pass(img, cam, [(560, 760, 620, (0.62, 0.8, 1.05), 1.0)], ambient=(0.08, 0.09, 0.17))
    return img


# ------------------------------------------------------------------------------ shots 2-3: the Channel

def sky_sea(img, cam, t, horizon=640, drift=0.0):
    S = B.SS
    h = img.height
    _, hy = cam.P(0, horizon)
    y = np.arange(h)[:, None]
    top, hor = np.array((128, 136, 142.0)), np.array((176, 180, 180.0))
    k = np.clip(y / max(1, hy), 0, 1) ** 1.2
    col = np.where(y < hy, top * (1 - k) + hor * k, np.array(SEA, float))
    a = np.broadcast_to(col[:, None, :], (h, img.width, 3)).astype(np.uint8)
    img.paste(Image.fromarray(np.ascontiguousarray(a), 'RGB'))
    p = B.Pen(img, cam)
    for i, (cx, cy, rx, ry) in enumerate([(100, 380, 380, 60), (700, 300, 420, 70), (420, 520, 460, 40), (980, 470, 300, 50)]):
        soft(img, cam, oval(cx + t * 8 + drift * 0.2, cy, rx, ry, 30), (110, 116, 124), 0.5, 30)
    p.poly([(-600, horizon - 8), (1700, horizon - 8), (1700, horizon + 4), (-600, horizon + 4)], (120, 132, 136), None)
    rng = np.random.default_rng(5)
    for row in range(26):  # choppy grey water: rows of wave crests, bigger nearer
        z = 1 + row * 0.9
        yy = horizon + 14 + (row ** 1.55) * 9
        amp = 3 + row * 1.1
        n = 10 + row // 3
        for kk in range(n):
            ph = rng.uniform(0, 1)
            wx = ((kk + ph) / n * 2200 + drift * (0.3 + row * 0.08) + t * 30) % 2200 - 600
            ww = 40 + row * 9
            p.poly([(wx - ww, yy), (wx - ww * 0.3, yy - amp), (wx, yy - amp * 1.4), (wx + ww * 0.5, yy - amp * 0.6),
                    (wx + ww, yy)], SEA_D if kk % 2 else B.lt(SEA, 1.12), None)
            if row > 8 and kk % 3 == 0:
                p.line([(wx - ww * 0.3, yy - amp), (wx, yy - amp * 1.4), (wx + ww * 0.3, yy - amp * 1.0)], (226, 230, 230), 1.6 + row * 0.08)


def helmet(p, hx, hy, hw, hh, colr=(236, 236, 232)):
    p.poly(curve([(hx - hw - 10, hy - 20), (hx - hw - 6, hy - hh * 0.9), (hx, hy - hh * 1.28), (hx + hw + 6, hy - hh * 0.9),
                  (hx + hw + 10, hy - 20), (hx, hy - 50)], 4), colr, INK, 2.6)
    p.line([(hx - hw - 4, hy - 36), (hx + hw + 4, hy - 36)], B.dk(colr, 0.8), 2.4)
    p.line([(hx - hw + 4, hy + 6), (hx - hw * 0.6, hy + hh * 0.9)], (40, 40, 40), 2.2)  # the chin strap


CREW = [
    dict(skin=B.PALE, hw=68, hh=88, jaw='square', hair='crop', hair_c=(90, 70, 50), outfit='jumper', jacket=CREW_YELLOW,
         shoulders=150, bottom=560, pose='custom', brows='serious', mouth='set', beard='stubble', beard_c=(110, 90, 70)),
    dict(skin=B.PINK, hw=64, hh=86, jaw='soft', hair='bob', hair_c=(176, 130, 76), outfit='jumper', jacket=CREW_YELLOW,
         shoulders=136, bottom=560, pose='custom', brows='serious', mouth='line'),
    dict(skin=B.OLIVE, hw=68, hh=90, jaw='round', hair='crop', hair_c=(40, 32, 28), outfit='jumper', jacket=CREW_YELLOW,
         shoulders=148, bottom=560, pose='custom', brows='weary', mouth='set', beard='trim', beard_c=(50, 42, 36)),
]


def crew_member(img, cam, x, y, s, sp, t, arms):
    sp = dict(sp, arms=arms)
    person(img, cam, x, y, s, sp, t)
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    for k in (0, 1):  # reflective bands on the jacket
        p.poly([(-sp['shoulders'] + 6, 330 + 60 * k), (sp['shoulders'] - 6, 330 + 60 * k), (sp['shoulders'] - 6, 350 + 60 * k),
                (-sp['shoulders'] + 6, 350 + 60 * k)], (220, 222, 216), None)
    helmet(B.Pen(img, PP.Rot(L, sp.get('tilt', 0.0))), sp.get('head_dx', 0), -150 + sp.get('head_dy', 0), sp['hw'], sp['hh'])


def lifeboat(img, cam, x, y, s, t, crew_fn=None):
    """An inshore lifeboat side-on, bow to the left: a navy hull, an orange top (tubes and console), the crew standing
    in the open boat behind a low windscreen. (x, y): waterline at mid-ship."""
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    hull = [(-520, -40), (-470, -140), (430, -150), (470, -120), (480, 20), (-300, 30)]
    p.line([(250, -150), (262, -520)], (60, 60, 66), 6)          # the A-frame mast behind the crew
    p.line([(330, -150), (270, -520)], (60, 60, 66), 6)
    p.ell(266, -530, 14, 10, LIFE_ORANGE, INK, 1.6)
    if crew_fn:
        crew_fn(L)
    p.poly([(-250, -150), (-40, -150), (-60, -250), (-210, -250)], LIFE_ORANGE, INK, 2.6)   # the console
    p.poly([(-200, -250), (-70, -250), (-50, -330), (-170, -330)], (150, 176, 196), INK, 2.2)  # its windscreen
    soft(img, L, [(-180, -320), (-130, -320), (-160, -258), (-196, -258)], (255, 255, 255), 0.35, 3)
    p.poly(hull, HULL, INK, 2.8)
    p.poly(curve([(-520, -120), (-470, -190), (440, -196), (480, -150), (440, -110), (-460, -96)], 3),
           LIFE_ORANGE, INK, 2.4)   # the orange tube along the gunwale
    for k in range(7):
        p.line([(-400 + 120 * k, -186), (-404 + 120 * k, -108)], B.dk(LIFE_ORANGE, 0.8), 1.8)
    p.line([(-430, -60), (440, -66)], B.lt(HULL, 1.5), 2.0)
    soft(img, L, [(-500, -40), (480, -40), (480, 20), (-300, 30)], (0, 0, 0), 0.25, 8)


def spray(img, cam, x, y, t, n=18, seed=1, size=1.0):
    p = B.Pen(img, cam)
    rng = np.random.default_rng(seed + int(t * FPS))
    for _ in range(n):
        a = rng.uniform(-2.6, -1.6)
        r = rng.uniform(20, 160) * size
        bx, by = x + math.cos(a) * r, y + math.sin(a) * r * 0.8
        rr = rng.uniform(6, 22) * size
        p.ell(bx, by, rr, rr * 0.8, (238, 242, 242), (200, 208, 210), 1.2)


def shot_lifeboat(t):
    """2. The lifeboat skims the rough grey Channel under a low sky, spray off the bow; the crew stare ahead."""
    cam = B.Cam(1.25, 480, 960)
    img = B.canvas()
    sky_sea(img, cam, t, horizon=640, drift=-260 * t)
    bob = 10 * math.sin(t * 3.1)
    roll = 0.03 * math.sin(t * 2.3 + 0.6)
    x, y, s = 600 - 12 * t, 1240 + bob, 1.05
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))

    def crew(L):
        for i, (dx, dy, sp, hs) in enumerate(((-110, -330, CREW[0], 0.36), (60, -325, CREW[1], 0.34), (210, -332, CREW[2], 0.36))):
            arms = {'L': ((-130, 280), (-230, 330), 'fist'), 'R': ((130, 290), (40, 360), 'fist')}
            st = dict(sp, turn=-0.55, look=-1.0, blink=M.blinking(t, (1.1 + i * 0.7, 3.4 + i * 0.4)),
                      head_dy=3 * math.sin(t * 3.1 + i))
            X, Y = L.P(dx, dy)
            crew_member(layer, cam, *world_of(cam, X, Y), s * hs, st, t, arms)
    lifeboat(layer, cam, x, y, s, t, crew)
    X, Y = cam.P(x, y)
    img.alpha_composite(layer.rotate(math.degrees(roll), Image.BICUBIC, center=(X, Y)))
    p = B.Pen(img, cam)
    for k in range(6):  # the wake and foam along the waterline
        p.ell(x - 460 + 170 * k + 30 * math.sin(t * 6 + k), y + 20, 110, 18, (226, 232, 232), None)
    spray(img, cam, x - 470, y - 40, t, n=26, seed=3, size=1.2)
    spray(img, cam, x - 360, y - 10, t, n=14, seed=9, size=0.9)
    return img


MIGRANTS = [  # back row on the far tube, left to right: (skin, hair, beard, jacket colour, life jacket, look, woman)
    (B.DEEP, 'crop', 'stubble', (70, 80, 96), True, 0.6, False),
    (B.BROWN, 'crop', 'full', (90, 70, 60), True, 0.8, False),
    ((150, 100, 70), 'scarf', None, (88, 60, 92), True, 0.7, True),
    (B.OLIVE, 'crop', 'trim', (60, 66, 70), False, 1.0, False),
    (B.DEEP, 'afro', None, (110, 50, 46), True, 0.5, False),
    ((160, 108, 76), 'side', 'stubble', (64, 74, 60), True, 0.9, False),
    (B.BROWN, 'bald', 'full', (50, 54, 70), True, 0.7, False),
]
FRONT = [  # nearer, seated on the near tube
    ((140, 92, 64), 'crop', 'trim', (80, 70, 60), True, 0.9, False),
    (B.DEEP, 'crop', None, (60, 60, 70), True, 0.6, False),
    (B.OLIVE, 'side', 'full', (96, 84, 70), False, 1.0, False),
    ((120, 80, 56), 'afro', 'stubble', (70, 90, 110), True, 0.8, False),
    (B.BROWN, 'crop', 'stubble', (60, 76, 66), True, 1.0, False),
]


def life_jacket(img, L):
    p = B.Pen(img, L)
    for sgn in (-1, 1):
        p.poly([(sgn * 30, -10), (sgn * 120, 30), (sgn * 128, 380), (sgn * 20, 400), (sgn * 26, 120)], JACKET_ORANGE, INK, 2.4)
        p.line([(sgn * 40, 140), (sgn * 116, 150)], B.dk(JACKET_ORANGE, 0.8), 2.0)
        p.line([(sgn * 38, 260), (sgn * 120, 266)], B.dk(JACKET_ORANGE, 0.8), 2.0)
    p.poly(curve([(-60, -30), (0, -40), (60, -30), (40, 10), (-40, 10)], 3), JACKET_ORANGE, INK, 2.2)  # the collar
    p.line([(-120, 300), (120, 300)], (40, 40, 44), 4)
    p.poly([(-12, 290), (12, 290), (12, 312), (-12, 312)], (30, 30, 30), None)


def scarf(img, L, hx, hy, hw, hh, colr):
    p = B.Pen(img, L)
    p.poly(curve([(hx - hw - 18, hy + 60), (hx - hw - 22, hy - 40), (hx - hw * 0.5, hy - hh - 20), (hx + hw * 0.5, hy - hh - 20),
                  (hx + hw + 22, hy - 40), (hx + hw + 18, hy + 60), (hx + hw + 30, hy + 140), (hx - hw - 30, hy + 140)], 4),
           colr, INK, 2.6)


def scarf_front(img, L, hx, hy, hw, hh, colr):
    p = B.Pen(img, L)
    p.poly(curve([(hx - hw - 4, hy + 50), (hx - hw - 6, hy - 30), (hx - hw * 0.4, hy - hh * 1.02), (hx + hw * 0.4, hy - hh * 1.02),
                  (hx + hw + 6, hy - 30), (hx + hw + 4, hy + 50), (hx + hw * 0.75, hy - 10), (hx + hw * 0.5, hy - hh * 0.7),
                  (hx - hw * 0.5, hy - hh * 0.7), (hx - hw * 0.75, hy - 10)], 4), colr, INK, 2.4)


def migrant(img, cam, x, y, s, spec, t, i, reach=0.0):
    skin, hair, beard, jc, jacket, look, woman = spec
    wet = B.dk(jc, 0.8)
    sp = dict(skin=skin, hw=64 if woman else 68, hh=86 if woman else 90, jaw='soft' if woman else ['square', 'round', 'long'][i % 3],
              hair=None if hair == 'scarf' else hair, hair_c=(26, 22, 22), outfit='jumper', jacket=wet, shoulders=130 if woman else 146,
              bottom=560, pose='custom', beard=beard, beard_c=(30, 26, 24), brows='weary' if i % 3 else 'sincere',
              brow_c=(30, 24, 22), lid=3 + (i % 3), mouth='set' if i % 2 else 'line', look=look, turn=0.25 * look,
              blink=M.blinking(t, (0.7 + i * 0.53, 3.9 + i * 0.37, 6.4 + i * 0.29)),
              head_dy=2 * math.sin(t * 2.0 + i), tilt=0.04 * math.sin(i * 1.7))
    if i in (2, 9):
        sp['age'] = True
    ra = ((150, 260), (150 + 140 * reach, 140 - 40 * reach), 'palm') if reach else ((160, 290), (110, 440), 'fist')
    sp['arms'] = {'L': ((-160, 290), (-110, 440), 'fist'), 'R': ra}
    L = B.Local(cam, x, y, s)
    if hair == 'scarf':
        scarf(img, L, 0, -150, sp['hw'], sp['hh'], (60, 40, 70))
    person(img, cam, x, y, s, sp, t, legs=seated_legs)
    if jacket:
        life_jacket(img, L)
        if reach:  # the reaching arm in front of the jacket
            B.Pen(img, L)
            B.arm(B.Pen(img, L), (132, 60), ra[0], ra[1], wet)
            B.gesture_hand(B.Pen(img, L), ra[0], ra[1], ra[2], skin)
    if hair == 'scarf':
        scarf_front(img, L, 0, -150 + sp['head_dy'], sp['hw'], sp['hh'], (60, 40, 70))
    p = B.Pen(img, L)
    for k in range(3):  # soaked: water dripping from hair and chin
        dx = -30 + 30 * k + 6 * i
        p.line([(dx, -150 + 98 + 6 * k), (dx + 1, -150 + 112 + 6 * k)], (200, 220, 236), 1.6)


def dinghy(img, cam, x, y, w, part, t):
    """The grey inflatable: 'far' tube behind the people, 'near' tube in front of them."""
    p = B.Pen(img, cam)
    if part == 'far':
        p.poly(curve([(x - w / 2, y - 250), (x + w / 2, y - 260), (x + w / 2 + 40, y - 200), (x - w / 2 - 40, y - 190)], 4),
               DINGHY, INK, 2.6)
        p.poly([(x - w / 2, y - 210), (x + w / 2, y - 220), (x + w / 2, y - 40), (x - w / 2, y - 30)], (60, 64, 70), None)
        return
    tube = curve([(x - w / 2 - 80, y - 90), (x, y - 110), (x + w / 2 + 80, y - 100), (x + w / 2 + 120, y - 10),
                  (x + w / 2 + 60, y + 70), (x, y + 80), (x - w / 2 - 60, y + 70), (x - w / 2 - 110, y)], 4)
    p.poly(tube, DINGHY, INK, 2.8)
    soft(img, cam, [(x - w / 2, y - 80), (x + w / 2, y - 92), (x + w / 2, y - 60), (x - w / 2, y - 50)], (255, 255, 255), 0.25, 8)
    soft(img, cam, [(x - w / 2, y + 30), (x + w / 2, y + 30), (x + w / 2, y + 76), (x - w / 2, y + 76)], (0, 0, 0), 0.3, 10)
    for k in range(9):  # the grab line along the side
        a, b = x - w / 2 + k * w / 9, x - w / 2 + (k + 1) * w / 9
        p.line([(a, y - 10), ((a + b) / 2, y + 12), (b, y - 10)], (40, 44, 50), 2.2)
    for k in range(5):
        p.ell(x - w / 2 + 40 + k * w / 4.4, y + 84, 70, 12, (220, 228, 230), None)


def shot_dinghy(t):
    """3. The lifeboat draws alongside an overloaded grey inflatable; a crew member reaches out a hand."""
    u = t / (T['s4'] - T['s3'])
    cam = B.Cam(1.0, 540, 960)
    img = B.canvas()
    sky_sea(img, cam, t, horizon=560, drift=-40 * t)
    bob = 8 * math.sin(t * 2.2)
    dx = 90 * (1 - smooth(u * 1.4))
    x, y = 420 - dx, 1210 + bob
    dinghy(img, cam, x, y, 760, 'far', t)
    for i, spec in enumerate(MIGRANTS):
        mx = x - 330 + i * 108
        migrant(img, cam, mx, y - 520 + 6 * math.sin(i * 2.1), 0.4, spec, t, i)
    for i, spec in enumerate(FRONT):
        mx = x - 300 + i * 150
        reach = smooth((u - 0.45) / 0.35) if i == 4 else 0.0
        migrant(img, cam, mx, y - 420 + 8 * math.cos(i * 1.3), 0.5, spec, t, i + 7, reach)
    dinghy(img, cam, x, y, 760, 'near', t)
    # the lifeboat's side at the right, a crew member leaning out with a hand held out
    p = B.Pen(img, cam)
    bx = 905 + 6 * math.sin(t * 1.9)
    p.poly([(bx - 40, 1000), (1200, 990), (1200, 1700), (bx + 10, 1700)], HULL, INK, 2.8)
    p.poly([(bx - 50, 980), (1200, 970), (1200, 1030), (bx - 46, 1036)], LIFE_ORANGE, INK, 2.4)
    k = smooth((u - 0.3) / 0.45)
    sp = dict(CREW[2], turn=-0.6, look=-1.0, head_dx=-10, tilt=-0.12, blink=M.blinking(t, (2.2, 5.6)))
    arms = {'L': ((-200 - 40 * k, 280), (-280 - 200 * k, 360 + 20 * k), 'palm'), 'R': ((140, 300), (60, 420), 'fist')}
    crew_member(img, cam, bx + 85, 760, 0.52, sp, t, arms)
    p.poly([(bx - 40, 1000), (1200, 990), (1200, 1700), (bx + 10, 1700)], HULL, INK, 2.8)
    p.poly([(bx - 50, 980), (1200, 970), (1200, 1030), (bx - 46, 1036)], LIFE_ORANGE, INK, 2.4)
    spray(img, cam, bx - 40, 1060, t, n=10, seed=4, size=0.7)
    return img


# ------------------------------------------------------------------------------- shot 4: from the screen

def shot_screen(t):
    """4. From where the monitor is, straight at his lit face, pushing in closer; then the heart attack."""
    tt = t + T['s4']
    u = t / (T['s5'] - T['s4'])
    k = smooth(u)
    cam = B.Cam(1.3 + 0.35 * k, 540, 860 - 70 * k)
    img = B.canvas()
    p = B.Pen(img, cam)
    p.poly([(-400, -200), (1500, -200), (1500, 1500), (-400, 1500)], NIGHT_WALL, None)
    # behind him: the door, a poster of a bulldog, the bed's corner
    p.poly([(60, 260), (330, 260), (330, 1240), (60, 1240)], (120, 100, 84), INK, 2.4)
    p.ell(296, 760, 12, 12, (200, 180, 120), INK, 1.6)
    p.poly([(690, 380), (970, 380), (970, 640), (690, 640)], (90, 70, 50), INK, 2.4)   # a framed print of the white cliffs
    p.poly([(706, 396), (954, 396), (954, 624), (706, 624)], (170, 200, 220), None)
    p.poly([(706, 540), (954, 540), (954, 624), (706, 624)], (80, 120, 140), None)
    p.poly([(706, 470), (790, 450), (880, 470), (954, 460), (954, 548), (706, 548)], (240, 240, 232), INK, 1.6)
    p.poly([(706, 450), (790, 432), (880, 452), (954, 444), (954, 466), (880, 474), (790, 454), (706, 472)], (110, 150, 80), None)
    p.poly([(-400, 1240), (1500, 1240), (1500, 2400), (-400, 2400)], CARPET, None)
    x, y, s = 540, 830, 1.0
    # the collapse: eyes cross, he clutches his chest, then topples sideways out of frame to our left
    a_cross = smooth((tt - T['cross']) / 0.12)
    a_clutch = smooth((tt - T['clutch']) / 0.18)
    a_fall = smooth((tt - T['topple']) / 0.45) if tt >= T['topple'] else 0.0
    office_chair(img, cam, x, y + 330 * s, s, back=True)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    tp, tp2 = tap(tt), tap(tt, 0.06)
    st = pro_st(tt, turn=0.0, look=0.0, lid=2 if tt < T['cut_off'] - 3.5 else 4, brows='flat' if tt < T['s4'] + 2 else 'cross')
    st['arms'] = {'L': ((-205, 330), (-75, 455 + 24 * tp), 'point'),
                  'R': ((205, 330), (75, 455 + 24 * tp2), 'point')}
    typing = a_clutch <= 0
    if a_cross > 0:
        st.update(brows='raised', lid=0, head_dy=-10 * a_cross, puff=0.0)
    if a_clutch > 0:
        st['arms'] = {'L': ((-230 + 20 * a_clutch, 300 - 40 * a_clutch), (-120 + 130 * a_clutch, 430 - 230 * a_clutch), 'fist'),
                      'R': ((215 + 20 * a_clutch, 300 - 20 * a_clutch), (110 - 10 * a_clutch, 430 - 150 * a_clutch), 'fist')}
        st['shrug'] = 0.6 * a_clutch
        st['tilt'] = -0.08 * a_clutch
    seated_protester(lay, cam, x, y, s, st, tt)
    if a_cross > 0:
        eyes_over(lay, cam, x, y, s, dict(st, turn=0.0), cross=a_cross, lid=0, bala=True)
    if a_fall > 0:
        X, Y = cam.P(x - 60, y + 450)
        lay = lay.rotate(85 * a_fall, Image.BICUBIC, center=(X, Y), translate=(-cam.S(900) * a_fall ** 2, cam.S(120) * a_fall))
    img.alpha_composite(lay)
    office_chair(img, cam, x + 30 * math.sin(max(0, tt - T['topple']) * 14) * math.exp(-max(0, tt - T['topple']) * 3),
                 y + 330 * s, s, back=False)
    # the desk in front, seen from the screen's side: keyboard's far edge, tubs, cans
    p = B.Pen(img, cam)
    p.poly([(-300, 1300), (1400, 1300), (1400, 1500), (-300, 1500)], DESK, INK, 2.6)
    p.poly([(-300, 1500), (1400, 1500), (1400, 1560), (-300, 1560)], DESK_D, INK, 2.4)
    keyboard(img, cam, 540, 1340, 420, 40, far=True)
    if typing:  # his forearms over the desk, hands on the keys, fingers jabbing
        for side in ('L', 'R'):
            PP.protester(img, cam, x, y, s, dict(st, arm_only=side), tt)
    foil_tray(img, cam, 150, 1380, 200, lid_off=-0.5)
    tub(img, cam, 900, 1380, 120, lid=-1)
    can(img, cam, 260, 1300, 100, CAN_GREEN, crushed=True, seed=2)
    can(img, cam, 820, 1310, 104, CAN_GOLD)
    # the knocked can rolls along the edge and drops off
    rc = max(0.0, tt - T['can'])
    cx = 700 + 260 * min(rc, 0.7) / 0.7
    cy = 1420 + (0 if rc < 0.7 else 1600 * (rc - 0.7) ** 2)
    can(img, cam, cx, cy, 100, CAN_GOLD, lying=(0 if rc <= 0 else 1.57 + rc * 9))
    light_pass(img, cam, [(540, 800, 380, (0.75, 0.92, 1.18), 1.2), (540, 1380, 460, (0.45, 0.58, 0.8), 0.45)],
               ambient=(0.07, 0.08, 0.16))
    return img


# ------------------------------------------------------------------------------- shots 5-7: ambulance, A&E

PARA_F = dict(skin=B.PALE, hw=62, hh=86, jaw='soft', hair='bob', hair_c=(120, 86, 56), outfit='jumper', jacket=PARA_GREEN,
              trousers=PARA_GREEN, shoulders=126, bottom=600, pose='custom', brow_c=(90, 64, 44), lashes=True, full=True,
              brows='weary', lid=2)
PARA_M = dict(skin=B.PINK, hw=70, hh=90, jaw='square', hair='crop', hair_c=(60, 48, 40), outfit='jumper', jacket=PARA_GREEN,
              trousers=PARA_GREEN, shoulders=146, bottom=600, pose='custom', beard='trim', beard_c=(80, 64, 54), full=True,
              brow_c=(60, 48, 40), lid=3)
DOCTOR = dict(skin=B.PALE, hw=72, hh=90, jaw='round', hair='crop', hair_c=(176, 136, 90), beard='trim', beard_c=(176, 146, 110),
              outfit='jumper',
              jacket=SCRUBS, trousers=SCRUBS, shoulders=144, bottom=600, pose='custom', age=True, brow_c=(100, 78, 60),
              brows='sincere', lid=2, full=True, glasses=True, glasses_c=(40, 40, 48), mouth='smile')
NURSE = dict(skin=B.DEEP, hw=64, hh=86, jaw='round', hair='afro', hair_c=(36, 30, 28), outfit='jumper', jacket=SCRUBS_L,
             trousers=SCRUBS_L, shoulders=132, bottom=600, pose='custom', brow_c=(30, 24, 22), full=True, lashes=True)
NURSE2 = dict(skin=B.OLIVE, hw=66, hh=88, jaw='square', hair='slick', hair_c=(30, 26, 26), outfit='jumper', jacket=SCRUBS_L,
              trousers=SCRUBS_L, shoulders=140, bottom=600, pose='custom', brow_c=(30, 26, 26), full=True)


def uniform_bits(img, cam, x, y, s, sp, kind):
    """Reflective strips and epaulettes for paramedics; a stethoscope and lanyard for the doctor."""
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    sw = sp['shoulders']
    if kind == 'para':
        for yb in (360,):
            p.poly([(-sw + 4, yb), (sw - 4, yb), (sw - 2, yb + 22), (-sw + 2, yb + 22)], (210, 214, 210), None)
        for sgn in (-1, 1):
            p.poly([(sgn * 50, 4), (sgn * (sw - 10), 34), (sgn * (sw - 14), 56), (sgn * 50, 26)], (30, 50, 40), None)
        p.poly([(-sw * 0.6, 120), (-sw * 0.2, 120), (-sw * 0.2, 150), (-sw * 0.6, 150)], (236, 236, 230), None)
    elif kind == 'doc':
        p.line([(-56, 0), (-70, 120), (-30, 220), (0, 240)], (40, 40, 44), 4)
        p.line([(56, 0), (70, 120), (30, 220), (0, 240)], (40, 40, 44), 4)
        p.ell(0, 252, 16, 16, (190, 196, 204), INK, 2.0)
        p.line([(-30, 0), (-14, 170)], (40, 90, 160), 5)
        p.line([(30, 0), (14, 170)], (40, 90, 160), 5)
        p.poly([(-30, 166), (30, 166), (30, 236), (-30, 236)], (248, 248, 248), INK, 1.8)
        p.poly([(-30, 166), (30, 166), (30, 180), (-30, 180)], (40, 90, 160), None)
    elif kind == 'nurse':
        p.line([(-40, 0), (-20, 180)], (200, 60, 70), 5)
        p.line([(40, 0), (20, 180)], (200, 60, 70), 5)
        p.poly([(-26, 176), (26, 176), (26, 236), (-26, 236)], (248, 248, 248), INK, 1.8)


def lying_protester(img, cam, x, y, s, t, look=(0.0, 0.0), blink=False, brows='flat', lid=2, gurgle=0.0):
    """On his back on the stretcher, head to our left, balaclava on, the oxygen mask over the mouth, a blanket."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    st = dict(arms=PP.REST, turn=0.0, look=0.0, lid=lid, brows=brows, puff=0.0, blink=blink, lv=0.0)
    PP.protester(lay, cam, x, y, s, st, t)
    if not blink:
        eyes_over(lay, cam, x, y, s, st, dx=look[0], dy=look[1], lid=lid, bala=True)
    L = B.Local(cam, x, y, s)
    p = B.Pen(lay, L)
    # the blanket over his legs and middle
    p.poly(curve([(-230, 380), (230, 380), (250, 700), (240, 960), (-240, 960), (-250, 700)], 3), (150, 190, 214), INK, 2.6)
    for k in range(6):
        p.line([(-220 + 6 * k, 420 + 90 * k), (220 - 6 * k, 420 + 90 * k)], (128, 168, 196), 1.8)
    # the oxygen mask over the mouth, its elastic and tube
    my = -150 + 52
    p.line([(-76, my - 20), (76, my - 20)], (230, 230, 220), 3)
    puff_ = 1 + 0.12 * gurgle
    p.poly(curve([(-40 * puff_, my - 14), (40 * puff_, my - 14), (34 * puff_, my + 30), (0, my + 40), (-34 * puff_, my + 30)], 4),
           (190, 222, 206), (110, 150, 130), 2.4)
    soft(lay, L, oval(-10, my + 6, 14, 10, 12), (255, 255, 255), 0.5, 3)
    p.line([(0, my + 40), (20, my + 120), (60, my + 200), (140, my + 240)], (190, 222, 206), 7)
    # monitor leads from inside his collar
    for k, c in enumerate(((220, 60, 50), (240, 230, 60), (60, 160, 70))):
        p.line([(-20 + 20 * k, 40), (-40 + 30 * k, 10), (-200 - 30 * k, -40)], c, 2.2)
    X, Y = cam.P(x, y)
    img.alpha_composite(lay.rotate(90, Image.BICUBIC, center=(X, Y)))


def stretcher(img, cam, x, y, length, part, legs=True, s=1.0):
    """A wheeled stretcher seen from slightly above: x, y the middle of the mattress top; part 'base' or 'rails'."""
    p = B.Pen(img, cam)
    l = length / 2
    if part == 'base':
        if legs:
            for X in (x - l + 60 * s, x + l - 60 * s):
                p.line([(X, y + 70 * s), (X, y + 330 * s)], (150, 156, 164), max(2, 14 * s))
                p.ell(X - 30 * s, y + 350 * s, 24 * s, 24 * s, (30, 30, 34), INK, 1.6)
                p.ell(X + 30 * s, y + 350 * s, 24 * s, 24 * s, (30, 30, 34), INK, 1.6)
            p.line([(x - l + 60 * s, y + 220 * s), (x + l - 60 * s, y + 220 * s)], (150, 156, 164), max(2, 12 * s))
        p.poly([(x - l, y - 90 * s), (x + l, y - 90 * s), (x + l + 10 * s, y + 60 * s), (x - l - 10 * s, y + 60 * s)],
               (236, 240, 242), INK, 2.6)
        p.poly([(x - l - 10 * s, y + 60 * s), (x + l + 10 * s, y + 60 * s), (x + l + 10 * s, y + 90 * s), (x - l - 10 * s, y + 90 * s)],
               (60, 70, 90), INK, 2.4)
        return
    p.line([(x - l - 10 * s, y + 40 * s), (x + l + 10 * s, y + 40 * s)], (170, 176, 184), max(2, 10 * s))
    for X in np.linspace(x - l + 40 * s, x + l - 40 * s, 6):
        p.line([(X, y + 40 * s), (X, y + 70 * s)], (170, 176, 184), max(2, 6 * s))


def heart_monitor(img, cam, x, y, w, t, beat_times):
    p = B.Pen(img, cam)
    h = w * 0.7
    p.poly([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)], (70, 74, 84), INK, 2.6)
    p.poly([(x - w * 0.42, y - h * 0.38), (x + w * 0.42, y - h * 0.38), (x + w * 0.42, y + h * 0.3), (x - w * 0.42, y + h * 0.3)],
           (16, 22, 24), None)
    pts = []
    for k in range(60):
        u = k / 59
        tt = t - (1 - u) * 2.0
        v = 0.0
        for b in beat_times:
            d = tt - b
            if -0.05 < d < 0.12:
                v += math.sin(d / 0.12 * 2 * math.pi) * (1.0 if d < 0.05 else 0.5)
        pts.append((x - w * 0.4 + w * 0.8 * u, y - h * 0.05 - v * h * 0.22))
    p.line(pts, (90, 240, 120), 2.6)
    PP.ctext(img, cam, x + w * 0.3, y - h * 0.26, '72', w * 0.12, (90, 240, 120))
    for k, c in enumerate(((240, 80, 70), (240, 230, 90), (90, 200, 240))):
        p.ell(x - w * 0.3 + k * w * 0.16, y + h * 0.4, w * 0.04, w * 0.04, c, None)


BEATS = list(np.arange(0.2, 80, 0.83))


def shot_ambulance(t):
    """5. Inside the ambulance: he lies on the stretcher; two paramedics tend to him calmly."""
    tt = t + T['s5']
    cam = B.Cam(1.32, 530, 975)
    img = B.canvas((214, 220, 222))
    p = B.Pen(img, cam)
    sway = 4 * math.sin(t * 5.3) + 2 * math.sin(t * 11)
    # the body of the ambulance: cabinets, a grab rail, lights, the rear windows
    p.poly([(-20, 120), (1100, 120), (1100, 220), (-20, 220)], (236, 238, 238), INK, 2.2)
    for X in (200, 540, 880):
        p.poly([(X - 90, 150), (X + 90, 150), (X + 90, 190), (X - 90, 190)], (252, 252, 236), None)
    p.line([(40, 270), (1040, 270)], (170, 176, 184), 8)
    for k in range(4):
        x0 = 40 + k * 250
        p.poly([(x0, 300), (x0 + 230, 300), (x0 + 230, 560), (x0, 560)], (240, 242, 244), INK, 2.2)
        p.poly([(x0 + 10, 310), (x0 + 220, 310), (x0 + 220, 400), (x0 + 10, 400)], (196, 214, 226), None)
        p.line([(x0 + 100, 520), (x0 + 130, 520)], INK, 3)
    p.poly([(-20, 1240), (1100, 1240), (1100, 2000), (-20, 2000)], (120, 130, 136), None)
    for k in range(10):
        p.line([(-20 + 120 * k, 1240), (-60 + 140 * k, 2000)], (110, 118, 124), 2)
    heart_monitor(img, cam, 525, 560, 220, tt, BEATS)
    # the paramedics behind the stretcher
    lv = level('para', tt)
    roll = smooth((tt - T['eyeroll']) / 0.2) * (1 - smooth((tt - T['eyeroll'] - 0.7) / 0.2))
    m_sp = dict(PARA_M, turn=0.45, look=0.8, head_dy=sway * 0.3, mouth='set',
                arms={'L': ((-150, 300), (-80, 520), 'fist'), 'R': ((150, 290), (120, 530), 'fist')},
                blink=M.blinking(tt, (T['s5'] + 1.0,)), brows='weary' if roll > 0.3 else None)
    f_sp = dict(PARA_F, turn=-0.5, look=-0.6, head_dy=sway * 0.3, mouth=M.talk_mouth(lv, tt),
                arms={'L': ((-160, 300), (-210, 540), 'fist'), 'R': ((140, 300), (130, 540), 'fist')},
                blink=M.blinking(tt, (T['s5'] + 2.0,)), brows='weary')
    person(img, cam, 330, 730, 0.62, m_sp, tt)
    uniform_bits(img, cam, 330, 730, 0.62, m_sp, 'para')
    if roll > 0.05:
        eyes_over(img, cam, 330, 730, 0.62, m_sp, dx=0.2, dy=-2.2 * roll, lid=1)
    person(img, cam, 720, 740, 0.6, f_sp, tt)
    uniform_bits(img, cam, 720, 740, 0.6, f_sp, 'para')
    # the stretcher across the front, him on it
    sy = 1180 + sway * 0.5
    stretcher(img, cam, 540, sy, 940, 'base', legs=True, s=0.8)
    lying_protester(img, cam, 360, sy - 10, 0.66, tt, look=(0.4, -0.5), lid=3, blink=M.blinking(tt, (T['s5'] + 1.6,)))
    stretcher(img, cam, 540, sy, 940, 'rails', s=0.8)
    p = B.Pen(img, cam)
    for k, c in enumerate(((220, 60, 50), (240, 230, 60), (60, 160, 70))):  # leads up to the monitor
        p.line([(460, sy - 10 + 8 * k), (500, sy - 250), (505 + 20 * k, 640)], c, 2.0)
    # the hand on him: hers on his shoulder
    return img


def ae_room(img, cam, t, doors=0.0):
    p = B.Pen(img, cam)
    p.poly([(-400, -200), (1500, -200), (1500, 1260), (-400, 1260)], HOSP_WALL, None)
    p.poly([(-400, 1260), (1500, 1260), (1500, 2400), (-400, 2400)], HOSP_FLOOR, None)
    p.poly([(-400, 1220), (1500, 1220), (1500, 1260), (-400, 1260)], (120, 160, 190), None)   # the kick rail
    for k in range(12):
        p.line([(-400 + 180 * k, 1260), (-900 + 300 * k, 2400)], B.dk(HOSP_FLOOR, 0.94), 2)
    for X in (120, 560, 1000):
        p.poly([(X - 120, -100), (X + 120, -100), (X + 120, 0), (X - 120, 0)], (250, 250, 240), None)
    # the double doors: glass above, and outside, the back of the ambulance with its checks
    dx0, dx1, top = 110, 650, 400
    p.poly([(dx0 - 30, top - 30), (dx1 + 30, top - 30), (dx1 + 30, 1260), (dx0 - 30, 1260)], (150, 160, 170), INK, 2.4)
    p.poly([(dx0, top), (dx1, top), (dx1, 1260), (dx0, 1260)], (112, 126, 152), None)       # dusk outside
    p.poly([(dx0, 900), (dx1, 900), (dx1, 1260), (dx0, 1260)], (90, 92, 96), None)
    ax, ay = 380, 420
    p.poly([(ax - 230, ay), (ax + 230, ay), (ax + 230, ay + 600), (ax - 230, ay + 600)], (246, 240, 120), INK, 2.2)
    for sgn in (-1, 1):  # roof lights
        p.poly([(ax + sgn * 200, ay - 26), (ax + sgn * 140, ay - 26), (ax + sgn * 140, ay), (ax + sgn * 200, ay)], (70, 120, 220), INK, 1.6)
    PP.ctext(img, cam, ax, ay + 50, 'AMBULANCE', 50, (20, 70, 40))
    for r in range(2):
        for c in range(9):
            colr = CHECK_GREEN if (r + c) % 2 == 0 else CHECK_YELLOW
            cx0 = ax - 230 + c * 460 / 9
            p.poly([(cx0, ay + 100 + r * 50), (cx0 + 460 / 9, ay + 100 + r * 50), (cx0 + 460 / 9, ay + 150 + r * 50),
                    (cx0, ay + 150 + r * 50)], colr, None)
    p.line([(ax, ay + 80), (ax, ay + 600)], INK, 2.2)
    for sgn in (-1, 1):
        p.poly([(ax + sgn * 40, ay + 230), (ax + sgn * 200, ay + 230), (ax + sgn * 200, ay + 380), (ax + sgn * 40, ay + 380)],
               (60, 70, 86), INK, 2.0)
    # the door leaves, swinging (0 shut, 1 wide open): steel below, glass above
    half = (dx1 - dx0) / 2
    for sgn, hinge in ((-1, dx0), (1, dx1)):
        w = half * math.cos(doors * 1.3)
        x_in = hinge - sgn * w
        lean = 60 * math.sin(doors * 1.3)
        g0, g1 = top + 30, top + 360
        glass = [(hinge, g0), (x_in, g0 - lean * 0.3), (x_in, g1 - lean * 0.2), (hinge, g1)]
        soft(img, cam, glass, (220, 236, 250), 0.25, 0)
        p.poly(glass, None, (176, 186, 196), 6)
        p.poly([(hinge, g1), (x_in, g1 - lean * 0.2), (x_in, 1260 + lean * 0.4), (hinge, 1260)], (196, 204, 210), INK, 2.6)
        p.poly([(hinge, top), (x_in, top - lean * 0.4), (x_in, g0 - lean * 0.3), (hinge, g0)], (196, 204, 210), INK, 2.2)
        if w > 60:
            p.poly([(hinge - sgn * 16, 920), (x_in + sgn * 16, 920), (x_in + sgn * 16, 950), (hinge - sgn * 16, 950)],
                   (150, 160, 170), None)
    # the generic sign, hanging from the ceiling beside the doors
    p.line([(760, 260), (760, 330)], (120, 124, 130), 3)
    p.line([(960, 260), (960, 330)], (120, 124, 130), 3)
    p.poly([(720, 330), (1000, 330), (1000, 450), (720, 450)], (30, 60, 130), (240, 240, 240), 2.0)
    B.text(img, cam, 860, 344, 'A&E', 84, (255, 255, 255), font=B.SANS, anchor='ma')


RAIL = {'L': ((-150, 300), (-110, 560), 'fist'), 'R': ((150, 300), (70, 560), 'fist')}


def trolley_team(img, cam, tx, ty, k, tt, ph, moving, staff=None):
    """The trolley with him on it, and three staff behind it, hands on its rail, running while it moves."""
    lv = level('para', tt)
    ps = 0.6 * k / 0.7
    ny = ty - 440 * k / 0.7
    team = [(PARA_M, -250, 0.0, 'para', dict(mouth='set', brows='serious')),
            (NURSE, 30, 1.7, 'nurse', dict(brows='serious')),
            (PARA_F, 240, 3.0, 'para', dict(mouth=M.talk_mouth(lv, tt), brows='alarm' if lv > 0 else 'serious'))]
    for i, (sp0, off, phase, kind, extra) in enumerate(team):
        ov = (staff or [{}] * 3)[i]
        bob = 7 * abs(math.sin(ph + phase)) if moving else 0.0
        sp = dict(sp0, turn=0.45, look=0.9, arms=RAIL, head_dx=18 if moving else 0, head_dy=bob * 0.5 + (6 if moving else 0),
                  tilt=0.08 if moving else 0.0, **extra)
        if sp0 is PARA_F:
            sp.update(turn=0.6, look=1.0)
        sp.update(ov.get('sp', {}))
        X = tx + off * k / 0.7 + ov.get('dx', 0.0)
        Y = ny + bob + ov.get('dy', 0.0)
        legs = ov.get('legs', walking_legs(ph + phase, 64, 28) if moving else None)
        person(img, cam, X, Y, ps, sp, tt, legs=legs)
        uniform_bits(img, cam, X, Y, ps, sp, kind)
    stretcher(img, cam, tx, ty, 1170 * k, 'base', legs=True, s=k)
    lying_protester(img, cam, tx - 330 * k, ty - 14 * k, 0.83 * k, tt, look=(0.0, -0.8), lid=3)
    stretcher(img, cam, tx, ty, 1170 * k, 'rails', s=k)


def speed_lines(img, cam, tx, ty, k, amount):
    p = B.Pen(img, cam)
    for j in range(4):
        yy = ty - 60 * k + j * 60 * k
        p.line([(tx - 600 * k - 40 * j, yy), (tx - 600 * k - 40 * j - 140 * amount, yy)], (150, 156, 164), 3)


def shot_ae(t):
    """6a. Urgent: the A&E doors bang open and the trolley is rushed through, staff running with it, straight past us."""
    tt = t + T['s6']
    dur = T['s6w'] - T['s6']
    doors = 1.0 * smooth(t / 0.07) if t < 0.45 else abs(math.exp(-(t - 0.45) * 2.2) * math.cos((t - 0.45) * 8.0))
    u = t / dur
    k = 0.62 + 0.3 * u
    tx = 430 + 640 * u ** 1.3
    ty = 1270 + 110 * u
    shake = 7 * math.sin(t * 90) * (1 - t / 0.25) if t < 0.25 else 0.0
    cam = B.Cam(1.0, 540 + shake, 960 + shake * 0.6)
    img = B.canvas()
    ae_room(img, cam, tt, doors=doors)
    trolley_team(img, cam, tx, ty, k, tt, t * 15.0, True)
    return img


def ward_set(img, cam, t, clock=True, monitor=True):
    """The ward: a bay with its curtains pulled back, the wall's oxygen panel, a clock just before one."""
    p = B.Pen(img, cam)
    p.poly([(-400, -200), (1500, -200), (1500, 1280), (-400, 1280)], HOSP_WALL, None)
    p.poly([(-400, 1280), (1500, 1280), (1500, 2400), (-400, 2400)], HOSP_FLOOR, None)
    for k in range(12):
        p.line([(-400 + 180 * k, 1280), (-900 + 300 * k, 2400)], B.dk(HOSP_FLOOR, 0.94), 2)
    p.poly([(-400, 820), (1500, 820), (1500, 880), (-400, 880)], (196, 214, 222), INK, 2.0)   # the bed-head trunking
    for X in (300, 700):
        p.ell(X, 850, 14, 14, (240, 240, 240), INK, 1.6)
    p.line([(-400, 200), (1500, 200)], (170, 176, 184), 10)
    for side, (x0, x1) in enumerate(((-120, 130), (950, 1200))):   # the curtains, bunched back at each side
        for k in range(5):
            a = x0 + (x1 - x0) * k / 5
            b_ = x0 + (x1 - x0) * (k + 1) / 5
            p.poly([(a, 205), (b_, 205), (b_ + 6, 1270), (a + 6, 1270)], CURTAIN if k % 2 else B.dk(CURTAIN, 0.9), INK, 1.6)
    p.poly([(330, 300), (650, 300), (650, 640), (330, 640)], (160, 190, 214), INK, 2.4)   # a window onto the car park
    p.line([(490, 300), (490, 640)], INK, 2.2)
    p.poly([(330, 560), (650, 560), (650, 640), (330, 640)], (140, 150, 150), None)
    if clock:
        p.ell(820, 420, 60, 60, (250, 250, 248), INK, 3)
        for k in range(12):
            a = k / 12 * 2 * math.pi
            p.line([(820 + 48 * math.sin(a), 420 - 48 * math.cos(a)), (820 + 55 * math.sin(a), 420 - 55 * math.cos(a))], INK, 2.2)
        p.line([(820, 420), (820 - 26 * math.sin(0.1), 420 - 29 * math.cos(0.1))], INK, 4)
        p.line([(820, 420), (820 - 44 * math.sin(0.1), 420 - 44 * math.cos(0.1))], INK, 2.6)
    if monitor:
        heart_monitor(img, cam, 160, 660, 150, t, BEATS)


# One ward, seen by two cameras: the wide (6b, 7) and the doctor's close-up, which is the wide camera moved in on him,
# so everyone and everything stays exactly where it is.
WARD_TX, WARD_TY, WARD_K = 430, 1280, 0.72     # where the trolley comes to rest
WARD_DOC = (840, 700, 0.72)                     # where the doctor stands


def shot_ward(t):
    """6b. Pushed fast into the ward; it skids to a halt in the bay by the doctor; the paramedic tells him; he nods."""
    tt = t + T['s6w']
    run = T['stop'] - T['s6w']
    u = min(1.0, t / run)
    d = 1 - (1 - u) ** 2.2
    jolt = 16 * math.exp(-(t - run) * 9) * math.sin((t - run) * 30) if t > run else 0.0
    k = 0.72
    tx = -600 + (WARD_TX + 600) * d + jolt
    ty = 1280
    shake = 6 * math.sin((t - run) * 80) * math.exp(-(t - run) * 10) if t > run else 0.0
    cam = B.Cam(1.0, 540 + shake, 960)
    img = B.canvas()
    ward_set(img, cam, tt)
    moving = t < run
    # the doctor, already in the bay, turning to meet them; one nod at the end
    nod = math.sin(min(1.0, max(0.0, (tt - T['nod']) / 0.4)) * math.pi)
    d_sp = dict(DOCTOR, turn=-0.5, look=-0.9, head_dy=10 * nod, mouth='line', brows='serious' if tt < T['nod'] else 'sincere',
                arms={'L': ((-140, 300), (-120, 480), 'fist'), 'R': ((140, 300), (120, 480), 'fist')},
                blink=M.blinking(tt, (T['nod'] + 0.1,)))
    person(img, cam, *WARD_DOC, d_sp, tt)
    uniform_bits(img, cam, *WARD_DOC, d_sp, 'doc')
    trolley_team(img, cam, tx, ty, k, tt, t * 15.0, moving)
    return img


def shot_doctor(t):
    """6c. The same ward, the camera moved in on the doctor: one calm breath; everyone nods; they all walk off, chatting."""
    tt = t + T['s6b']
    x, y, s_ = WARD_DOC
    cam = B.Cam(1.6, x, y - 150 * s_ - (600 - 960) / 1.6)
    img = B.canvas()
    ward_set(img, cam, tt)
    lv = level('doc', tt)
    agree = math.sin(min(1.0, max(0.0, (tt - T['agree']) / 0.45)) * math.pi * 2) * (tt > T['agree'])
    walk = max(0.0, tt - T['leave'])
    chat = walk > 0.1
    # the doctor: speaks, nods, then turns and strolls off to the right with the others
    d_walk = max(0.0, walk - 0.25)
    d_sp = dict(DOCTOR, turn=-0.3 + 0.8 * smooth(walk / 0.3), look=-0.6 if not chat else 0.8, head_dy=8 * agree,
                arms={'L': ((-140, 300), (-120, 480), 'fist'), 'R': ((140, 300), (120, 480), 'fist')},
                mouth=M.talk_mouth(lv, tt) if lv > 0 else ('smile' if chat else 'line'),
                blink=M.blinking(tt, (T['s6b'] + 1.9, T['s6b'] + 4.3, T['s6b'] + 7.2)), brows='sincere')
    dx = x + 190 * d_walk ** 1.3
    person(img, cam, dx, y + 5 * abs(math.sin(d_walk * 8)) * (d_walk > 0), s_, d_sp, tt,
           legs=walking_legs(d_walk * 8) if d_walk > 0 else None)
    uniform_bits(img, cam, dx, y, s_, d_sp, 'doc')
    # the staff behind the trolley: they glance at the doctor, nod, then walk off after him, chatting
    staff = []
    for i, ph0 in enumerate((0.0, 1.5, 3.0)):
        w = max(0.0, walk - 0.1 * i)
        staff.append(dict(dx=230 * w ** 1.3, dy=5 * abs(math.sin(w * 8 + ph0)) * (w > 0),
                          legs=walking_legs(w * 8 + ph0) if w > 0 else None,
                          sp=dict(turn=0.5, look=0.9, head_dy=8 * agree, arms={'L': ((-140, 300), (-60, 470), 'fist'),
                                                                              'R': ((140, 300), (60, 470), 'fist')},
                                  mouth=['small', 'line', 'mid', 'line'][int(tt * (5 + i)) % 4] if chat else 'line',
                                  brows='sincere' if chat else None,
                                  blink=M.blinking(tt, (T['s6b'] + 1.3 + i, T['s6b'] + 4.8 + i)))))
    trolley_team(img, cam, WARD_TX, WARD_TY, WARD_K, tt, 0.0, False, staff=staff)
    return img


def shot_alone(t):
    """7. The same ward, everyone gone: him alone on the trolley where it stopped; the monitor beeps; an unhappy gurgle."""
    tt = t + T['s7']
    cam = B.Cam(1.35, 400, 1060)
    img = B.canvas()
    ward_set(img, cam, tt)
    g = smooth((tt - T['gurgle']) / 0.15) * (1 - smooth((tt - T['gurgle'] - 0.7) / 0.2))
    look = (-0.6 + 1.2 * smooth((tt - T['s7'] - 0.2) / 0.3), -0.6) if tt < T['gurgle'] else (0.9 * math.sin((tt - T['gurgle']) * 3), 0.6)
    tx, ty, k = WARD_TX, WARD_TY, WARD_K
    stretcher(img, cam, tx, ty, 1170 * k, 'base', legs=True, s=k)
    lying_protester(img, cam, tx - 330 * k, ty - 14 * k, 0.83 * k, tt, look=look, lid=1 if g > 0.2 else 3,
                    brows='raised' if g > 0.2 else 'flat', gurgle=g)
    stretcher(img, cam, tx, ty, 1170 * k, 'rails', s=k)
    p = B.Pen(img, cam)
    for j, c in enumerate(((220, 60, 50), (240, 230, 60), (60, 160, 70))):   # leads up to the monitor on the wall
        p.line([(tx - 200 * k, ty - 20 + 6 * j), (200, 900), (150 + 15 * j, 715)], c, 2.0)
    return img


# --------------------------------------------------------------------------------------------- frames

SHOT_FN = dict(room=shot_room, insert=shot_insert, lifeboat=shot_lifeboat, dinghy=shot_dinghy, screen=shot_screen,
               ambulance=shot_ambulance, ae=shot_ae, ward=shot_ward, doctor=shot_doctor, alone=shot_alone)


def caption_at(t):
    for idx, (who, a, b, pieces, words, rec) in enumerate(LINES):
        starts = [next(s for w, s, e, i in words if i == k) for k in range(len(pieces))]
        nxt_line = LINES[idx + 1][1] if idx + 1 < len(LINES) else 1e9
        for k, piece in enumerate(pieces):
            s0 = starts[k] - 0.05
            s1 = starts[k + 1] - 0.05 if k + 1 < len(pieces) else min(b + 0.35, nxt_line - 0.05)
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
            PP.caption(img, c)
    if title and t < 1.0:  # the standard title, over the dark room, gone by 1 s
        B.title(img, TITLE, alpha=1.0 if t < 0.75 else 1.0 - (t - 0.75) / 0.25, maxw=840)
    return img


# ----------------------------------------------------------------------------------------------- sound
rng = np.random.default_rng(31)
place = M.place
band = M.band


def key_click():
    n = int(0.03 * SR)
    tt = np.arange(n) / SR
    x = band(rng.standard_normal(n), 1800, 7000) * np.exp(-tt * 260) + 0.6 * np.sin(2 * np.pi * 420 * tt) * np.exp(-tt * 300)
    return normal(x)


def can_clink(roll=False):
    n = int(0.4 * SR)
    tt = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * d) for f, d in ((1840, 30), (2950, 40), (4400, 55)))
    return normal(x * (1 - np.exp(-tt * 3000)))


def can_roll(dur=0.7):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    x = band(rng.standard_normal(n), 900, 4000) * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * tt)) * np.minimum(1, tt / 0.05)
    x += 0.3 * np.sin(2 * np.pi * 2200 * tt) * (0.5 + 0.5 * np.sin(2 * np.pi * 18 * tt))
    return normal(x * np.minimum(1, (dur - tt) / 0.05))


def thud(f0=70, dur=0.5, crack=0.4):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = f0 + 80 * np.exp(-tt * 20)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
    harm = np.sin(2 * np.pi * np.cumsum(f * 3) / SR) * np.exp(-tt * 14)
    cr = band(rng.standard_normal(n), 600, 5000) * np.exp(-tt * 40)
    return normal(body + 0.4 * harm + crack * normal(cr))


def chair_crash():
    out = np.zeros(int(1.0 * SR))
    place(out, thud(60, 0.6, 0.6), 0.0, 1.0)            # him hitting the floor
    place(out, thud(110, 0.3, 0.9), 0.12, 0.6)          # the chair's base clattering
    for k in range(5):                                   # the castors rattling to a stop
        at = 0.25 + 0.09 * k + 0.02 * k * k
        place(out, M.clink() * 0.3, at, 0.5 * (0.7 ** k))
        place(out, thud(300, 0.08, 1.0) * 0.4, at, 0.5 * (0.7 ** k))
    return normal(out)


def strangled():
    """A short strangled 'hnnk': a choked voiced sound (placeholder until Sam records one)."""
    from scipy.signal import butter, sosfilt
    n = int(0.55 * SR)
    tt = np.arange(n) / SR
    f = 150 + 70 * np.sin(np.pi * tt / 0.55)
    ph = 2 * np.pi * np.cumsum(f) / SR
    buzz = sum(np.sin(h * ph) / h for h in range(1, 30))
    x = sosfilt(butter(2, [500, 1400], 'band', fs=SR, output='sos'), buzz) * (0.6 + 0.4 * (np.sin(2 * np.pi * 32 * tt) > 0))
    env = np.minimum(1, tt / 0.03) * np.minimum(1, (0.55 - tt) / 0.08)
    return normal(x * env)


def gurgle():
    """An unhappy little gurgle through the oxygen mask (placeholder until Sam records one)."""
    from scipy.signal import butter, sosfilt
    n = int(0.8 * SR)
    tt = np.arange(n) / SR
    f = 120 - 30 * tt / 0.8
    ph = 2 * np.pi * np.cumsum(f) / SR
    buzz = sum(np.sin(h * ph) / h for h in range(1, 30))
    wob = 0.5 + 0.5 * np.sin(2 * np.pi * (9 + 4 * np.sin(2 * np.pi * 1.5 * tt)) * tt)
    x = sosfilt(butter(2, [300, 1000], 'band', fs=SR, output='sos'), buzz) * wob
    bub = band(rng.standard_normal(n), 300, 1200) * (np.sin(2 * np.pi * 11 * tt) > 0.7) * 0.4
    env = np.minimum(1, tt / 0.05) * np.minimum(1, (0.8 - tt) / 0.15)
    return normal(onepole_lp(x + bub, 2500) * env)


def engine(n):
    tt = np.arange(n) / SR
    out = np.zeros(n)
    for f0, g in ((38.0, 1.0), (57.0, 0.6), (76.0, 0.4)):
        ph = 2 * np.pi * np.cumsum(f0 * (1 + 0.02 * np.sin(2 * np.pi * 0.7 * tt))) / SR
        out += g * sum(np.sin(h * ph + h) / h ** 0.8 for h in range(1, 16))
    out = onepole_lp(out, 900)
    return normal(out * (0.8 + 0.2 * np.sin(2 * np.pi * 3.1 * tt)))


def wave_slap():
    n = int(0.7 * SR)
    tt = np.arange(n) / SR
    x = band(rng.standard_normal(n), 200, 3000) * np.exp(-tt * 7) * np.minimum(1, tt / 0.015)
    th = thud(55, 0.5, 0.0)
    x[:len(th)] += 0.36 * th
    return normal(x)


def spray_burst():
    n = int(0.9 * SR)
    tt = np.arange(n) / SR
    x = band(rng.standard_normal(n), 2000, 9000) * np.exp(-tt * 4.5) * np.minimum(1, tt / 0.02)
    return normal(x)


def beep():
    n = int(0.12 * SR)
    tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * 1000 * tt) * np.minimum(1, tt / 0.005) * np.minimum(1, (0.12 - tt) / 0.01)
    return x


def siren(dur=0.9):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    f = np.where((tt % 0.6) < 0.3, 700, 950)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + np.sin(2 * np.pi * np.cumsum(f) / SR)
    x = onepole_lp(onepole_lp(x, 1200), 1200)  # muffled, from inside
    return normal(x * np.minimum(1, tt / 0.05) * np.minimum(1, (dur - tt) / 0.25))


def rattle(dur):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    x = band(rng.standard_normal(n), 1500, 6000) * (rng.random(n) < 0.004).astype(float)
    x = np.convolve(x, np.exp(-np.arange(int(0.01 * SR)) / SR * 500), 'same')
    return normal(x * np.minimum(1, tt / 0.05) * np.minimum(1, (dur - tt) / 0.05))


def door_swing():
    n = int(0.8 * SR)
    tt = np.arange(n) / SR
    x = thud(90, 0.4, 0.3)
    out = np.zeros(n)
    place(out, x, 0.0, 1.0)
    place(out, x * 0.4, 0.35, 1.0)
    squeak = np.sin(2 * np.pi * np.cumsum(900 + 300 * tt) / SR) * np.exp(-tt * 6) * 0.15
    return normal(out + squeak)


def wheels(dur):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    x = onepole_lp(rng.standard_normal(n), 400) * (0.7 + 0.3 * np.sin(2 * np.pi * 7 * tt))
    x += 0.3 * band(rng.standard_normal(n), 2000, 5000) * (rng.random(n) < 0.002)
    return normal(x * np.minimum(1, tt / 0.1) * np.minimum(1, (dur - tt) / 0.3))


def footstep():
    n = int(0.12 * SR)
    tt = np.arange(n) / SR
    return normal(band(rng.standard_normal(n), 150, 2500) * np.exp(-tt * 45))


def chatter(dur):
    """Two or three people chatting as they walk off: speech-like murmur, fading."""
    n = int(dur * SR)
    from scipy.signal import butter, sosfilt
    out = np.zeros(n)
    vowels = [(730, 1090), (530, 1840), (270, 2290), (570, 840), (660, 1720)]
    for v, f0 in enumerate((210, 120, 180)):
        t = 0.05 + 0.2 * v
        while t < dur - 0.3:
            d = rng.uniform(0.1, 0.22)
            m = int(d * SR)
            tt = np.arange(m) / SR
            ph = 2 * np.pi * np.cumsum(f0 * (1 + 0.06 * rng.uniform(-1, 1)) * (1 - 0.05 * tt / d)) / SR
            buzz = sum(np.sin(h * ph) / h for h in range(1, 14))
            f1, f2 = vowels[rng.integers(len(vowels))]
            syl = sosfilt(butter(2, [f1 * 0.8, f1 * 1.2], 'band', fs=SR, output='sos'), buzz) \
                + 0.5 * sosfilt(butter(2, [f2 * 0.85, f2 * 1.15], 'band', fs=SR, output='sos'), buzz)
            place(out, syl * np.sin(np.pi * tt / d) ** 1.5 * rng.uniform(0.5, 1.0), t)
            t += d + rng.uniform(0.0, 0.08)
            if rng.random() < 0.15:
                t += rng.uniform(0.3, 0.7)
    tt = np.arange(n) / SR
    return normal(onepole_lp(out, 3000) * np.clip(1 - tt / dur, 0, 1) ** 1.5)


def faded(x, a=0.02, b=0.05):
    x = x.copy()
    ka, kb = int(a * SR), int(b * SR)
    x[:ka] *= np.linspace(0, 1, ka)
    x[-kb:] *= np.linspace(1, 0, kb)
    return x


def soundtrack():
    n = int(DUR * SR)
    mix = np.zeros(n)
    click = key_click()
    for c in CLICKS:  # the keyboard, in step with his words
        place(mix, click * rng.uniform(0.6, 1.0), c, 0.1)
    place(mix, can_clink(), T['knock'], 0.14)                      # his hand nudges a can
    # the sea
    a, b = T['s2'], T['s4']
    place(mix, faded(engine(int((b - a) * SR)), 0.01, 0.01) * np.linspace(1.0, 0.6, int((b - a) * SR)), a, 0.10)
    place(mix, wave_slap(), T['s2'], 0.22)
    place(mix, spray_burst(), T['s2'] + 0.1, 0.1)
    place(mix, spray_burst(), T['s2'] + 2.2, 0.07)
    place(mix, wave_slap(), T['s3'], 0.2)
    place(mix, wave_slap(), T['s3'] + 3.6, 0.1)
    place(mix, M.reverb(PP.gull_call(), 1.0, 0.2) if hasattr(M, 'reverb') else PP.gull_call(), T['s2'] + 1.3, 0.07)
    # the heart attack
    place(mix, chair_crash(), T['crash'], 0.45)
    place(mix, can_roll(0.7), T['can'], 0.12)
    place(mix, can_clink(), T['can'] + 0.85, 0.16)
    # the ambulance
    place(mix, siren(0.9), T['s5'], 0.06)
    place(mix, rattle(T['s6'] - T['s5']), T['s5'], 0.05)
    for bt in BEATS:
        if T['s5'] <= bt < T['s6'] - 0.12:
            place(mix, beep(), bt, 0.05)
    # A&E
    place(mix, door_swing(), T['s6'], 0.32)
    place(mix, thud(80, 0.4, 0.8), T['s6'] + 0.02, 0.25)        # the doors banging open
    place(mix, wheels(T['stop'] - T['s6'] + 0.2), T['s6'], 0.2)
    place(mix, door_swing(), T['s6w'] + 0.1, 0.12)                 # the ward's doors, further off
    for k in range(int((T['stop'] - T['s6']) / 0.16)):            # running feet
        place(mix, footstep(), T['s6'] + 0.05 + 0.16 * k + 0.03 * (k % 2), 0.11)
    place(mix, rattle(0.4), T['stop'], 0.12)                       # the trolley jolting to a stop
    walk_end = T['s7']
    k = 0
    while T['leave'] + 0.3 * k < walk_end:
        place(mix, footstep(), T['leave'] + 0.3 * k, 0.07 * (1 - 0.6 * (0.3 * k) / (walk_end - T['leave'])))
        k += 1
    place(mix, chatter(walk_end - T['leave'] + 0.6), T['leave'], 0.05)
    for bt in BEATS:
        if T['s7'] <= bt < BLACK_AT - 0.12:
            place(mix, beep(), bt, 0.06)
    end = int(BLACK_AT * SR)
    k = int(0.005 * SR)
    mix[end - k:end] *= np.linspace(1, 0, k)   # hard cut to black: a few-millisecond fade, then nothing
    mix[end:] = 0
    # the voices: cleaned and levelled, otherwise exactly as recorded (volume only)
    def voice(f, s0, s1, at):
        seg = MA.line(f)[int(s0 * SR):int(s1 * SR)].copy()
        k = int(0.02 * SR)
        seg[:k] *= np.linspace(0, 1, k)
        seg[-k:] *= np.linspace(1, 0, k)
        place(mix, seg, at, 1.0)
    for who, a, b, _, words, rec in LINES:
        if rec:
            voice(*rec, a)
    voice(*GURGLE, T['gurgle'])
    voice(*CHOKE, T['cross'] - 0.05)
    mix[end - k:end] *= np.linspace(1, 0, k)
    mix[end:] = 0
    # master: about -14 LUFS, peaks no higher than -1 dBTP
    for _ in range(3):
        mix *= 10 ** ((-14.0 - MA.lufs(mix[:end])) / 20)
        mix = M.limiter(mix, -2.6)
    return mix


# ------------------------------------------------------------------------------------------- render

def render_frame(args):
    i, size, ss = args
    B.SS = ss
    return np.asarray(frame_image(i / FPS).convert('RGB').resize(size, Image.LANCZOS)).tobytes()


def render(out, size, crf, ss):
    import imageio_ffmpeg
    from multiprocessing import Pool
    wav = out + '.wav'
    mix = soundtrack()
    print(f'sound: {MA.lufs(mix):.1f} LUFS, peak {MA.true_peak_db(mix):.1f} dBTP', flush=True)
    MA.write_wav(wav, mix)
    n = int(round(DUR * FPS))
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{size[0]}x{size[1]}', '-r', str(FPS), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '160k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for f, fr in enumerate(pool.imap(render_frame, [(i, size, ss) for i in range(n)], chunksize=2)):
            p.stdin.write(fr)
            if f % 48 == 0:
                print(f'frame {f}/{n}', flush=True)
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print(f'done: {out} ({os.path.getsize(out) / 1e6:.1f} MB)', flush=True)


def closeup(t, z, cx, cy):
    """A close look at part of a shot (the desk, the crew, the dinghy), for the storyboard."""
    keep = B.Cam

    class Zoomed(keep):
        def __init__(self, z0=1.0, cx0=540, cy0=960):
            super().__init__(z0 * z, cx, cy)
    B.Cam = Zoomed
    try:
        return frame_image(t, captions=False, title=False)
    finally:
        B.Cam = keep


def sheet(dst):
    cw, ch, lab = 360, 640, 70
    stills = [('1. His room (title)', frame_image(0.5)),
              ('1. Push-in continues', frame_image(T['s2'] - 0.6)),
              ('2. The lifeboat', frame_image(T['s2'] + 1.6)), ('3. The dinghy', frame_image(T['s4'] - 1.0)),
              ('4. From the screen', frame_image(T['s4'] + 2.0)), ('4. "...I shall-"', frame_image(T['clutch'] + 0.2)),
              ('4. Topples out', frame_image(T['topple'] + 0.3)),
              ('5. Ambulance', frame_image(T['s5'] + 1.2)), ('6a. Rushed through A&E', frame_image(T['s6'] + 0.6)),
              ('6b. Into the ward', frame_image(T['s6w'] + 0.5)), ('6b. "Heart attack, Doctor"', frame_image(T['nod'] - 0.6)),
              ('6c. The doctor', frame_image(T['s6b'] + 5.5)), ('6c. They walk off', frame_image(T['leave'] + 0.9)),
              ('7. Alone; gurgle', frame_image(T['gurgle'] + 0.3)),
              ('Close-up: the desk', closeup(4.5, 2.0, 780, 1090)),
              ('Close-up: the crew', closeup(T['s2'] + 1.6, 2.4, 610, 830)),
              ('Close-up: the dinghy', closeup(T['s4'] - 1.0, 1.7, 470, 760))]
    cols = 6
    rows = (len(stills) + cols - 1) // cols
    sh = Image.new('RGB', (cols * (cw + 16) + 16, rows * (ch + lab + 12) + 16), (245, 242, 236))
    d = ImageDraw.Draw(sh)
    f = ImageFont.truetype(B.SANS, 22)
    for i, (name, im) in enumerate(stills):
        x, y = 16 + (i % cols) * (cw + 16), 16 + (i // cols) * (ch + lab + 12)
        sh.paste(im.convert('RGB').resize((cw, ch), Image.LANCZOS), (x, y))
        d.text((x + 2, y + ch + 10), name, font=f, fill=(20, 20, 20))
    sh.save(dst, quality=88)


def main():
    mode = sys.argv[1]
    if mode == 'times':
        for k, v in T.items():
            print(f'{k:10s} {v}')
        return
    if mode == 'stills':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for s in sys.argv[3:]:
            frame_image(float(s)).convert('RGB').resize((B.W, B.H), Image.LANCZOS).save(os.path.join(out, f't{s}.png'))
    elif mode == 'sheet':
        sheet(sys.argv[2])
    elif mode == 'animatic':
        render(sys.argv[2], (540, 960), 26, 1)
    elif mode == 'final':
        render(sys.argv[2], (1080, 1920), 20, 2)


if __name__ == '__main__':
    main()
