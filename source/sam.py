#!/usr/bin/env python3
"""Oxford Rap Battle, round two: the pigeon in the blue jumper answers the penguin.

Same world, same cast and same drawing kit as rap.py; this time the pigeon raps and the
penguin takes it. The real audio plays unchanged, with subtitles.

Usage:
    python3 sam.py stills OUT_DIR T1 T2 ...
    python3 sam.py render OUT.mp4 [CRF]
"""
import json
import math
import os
import sys

import numpy as np

import rap as R
from rap import (Image, E, text, smooth, clamp01, lerp, sstep, W, H, FPS, SR, Sketch, penguin, pigeon, bird, room,
                 limb, Rig, wash, render_video, col, INK, BLACK, WHITE, ORANGE, PLAID, JUMPER, PIGEON, PIGEON_D,
                 WOOD, WOOD_D, AMBER, NAVY, RED, GREEN, YELLOW, GREY, BROWN, SKY, SILVER, PINK, WALL)

HERE = R.HERE
DUR = 178.0
AUDIO = os.path.join(HERE, 'audio', 'sam-battle.m4a')
RAP_START = 28.1  # the host talks before this; the pigeon raps after


# ---------------------------------------------------------------------------
# Point the shared machinery (loudness, beak flaps, subtitles) at this battle's audio
# ---------------------------------------------------------------------------
def _load_audio():
    import subprocess
    import imageio_ffmpeg
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-i', AUDIO, '-ac', '1', '-ar',
                          str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float64) / 32767
    n = SR // 24
    env = np.array([np.sqrt((x[i:i + n] ** 2).mean()) for i in range(0, len(x) - n, n)])
    med = np.median(env)
    return np.clip((env - med * 0.6) / (env.max() * 0.55 - med * 0.6), 0, 1)


R.LOUD = _load_audio()
_WD = json.load(open(os.path.join(HERE, 'data', 'sam_words.json')))
R.WORDS, R.LINE_STARTS = _WD['words'], set(_WD['line_starts'])
R.UNINTELLIGIBLE = [tuple(f) for f in _WD['flashes']]
R.SUBS = R.line_subs(_WD)
loud, beak_open = R.loud, R.beak_open

TAN = col(0.85, 0.72, 0.5)
STONE = col(0.8, 0.78, 0.74)
DARK = col(0.22, 0.22, 0.26)


def rap_beak(t):
    return beak_open(t) if t >= RAP_START else 0.0


def host_talking(t):
    return t < RAP_START and beak_open(t) > 0.5


# ---------------------------------------------------------------------------
# Shots
# ---------------------------------------------------------------------------
SHOTS = [
    (0, 14.1, 'intro'), (14.1, 28.1, 'fest'), (28.1, 35.9, 'arrive'), (35.9, 38.06, 'obnoxious'),
    (38.06, 40.83, 'coarse'), (40.83, 43.55, 'degenerate'), (43.55, 45.71, 'stage'), (45.71, 48.41, 'illiterate'),
    (48.41, 51.18, 'facts'), (51.18, 53.82, 'getout'), (53.82, 56.31, 'stage'), (56.31, 58.66, 'gasp'),
    (58.66, 61.4, 'bring'), (61.4, 65.27, 'king'), (65.27, 67.81, 'bothered'), (67.81, 70.89, 'ring'),
    (70.89, 76.11, 'list'), (76.11, 80.93, 'far'), (80.93, 83.74, 'level'), (83.74, 90.22, 'wife'),
    (90.22, 92.84, 'court'), (92.84, 97.37, 'stork'), (97.37, 101.24, 'phone'), (101.24, 106.16, 'police'),
    (106.16, 108.82, 'maggot'), (108.82, 110.94, 'rooster'), (110.94, 114.79, 'fish'), (114.79, 117.33, 'gasp'),
    (117.33, 120.17, 'hear'), (120.17, 122.22, 'syringe'), (122.22, 124.81, 'mandy'), (124.81, 128.29, 'planb'),
    (128.29, 132.96, 'stairs'), (132.96, 137.04, 'stage'), (137.04, 139.39, 'statue'), (139.39, 141.77, 'criminal'),
    (141.77, 144.34, 'minuscule'), (144.34, 147.09, 'pinnacle'), (147.09, 148.98, 'stage'), (148.98, 153.31, 'drunk'),
    (153.31, 157.26, 'dictionary'), (157.26, 163.08, 'retreat'), (163.08, 167.6, 'joke'), (167.6, DUR + 1, 'finale'),
]


def shot_at(t):
    for a, b, name in SHOTS:
        if a <= t < b:
            return a, b, name
    return SHOTS[-1]


# ---------------------------------------------------------------------------
# Extra characters and props
# ---------------------------------------------------------------------------
def host(c, x, y, s, t, face=1, react=None):
    """The MC: glasses, swept black hair, white shirt and grey waistcoat, never still for a second."""
    if react is None and host_talking(t):
        react = 'cheer' if int(t * 3) % 2 else 'gasp'
    return R.audience(c, x, y, s, 'host', react, t, face)


def rooster(c, x, y, s, face=1, plucked=0.0, mood='angry'):
    r = Rig(c, x, y, s, face)
    lw = r.lw()
    for du in (-0.06, 0.06):
        c.line(r.pts([(du, 0.25), (du, 0.0)]), YELLOW, lw=s * 0.03)
        c.line(r.pts([(du, 0.0), (du + 0.08, 0.0)]), YELLOW, lw=s * 0.02)
    n_tail = int(round(5 * (1 - plucked)))
    for i in range(n_tail):
        a = 0.5 + i * 0.35
        c.line(r.pts(smooth([(-0.25, 0.45), (-0.45 - 0.05 * math.cos(a), 0.6 + 0.2 * math.sin(a)),
                             (-0.5 + 0.05 * i, 0.4 + 0.05 * i)], 4, False)), col(0.12, 0.35, 0.3), lw=s * 0.05)
    if plucked > 0:  # a sore pink rump with a sticking plaster
        c.poly(r.E(-0.28, 0.42, 0.07, 0.06), fill=PINK, line=INK, lw=lw)
        c.poly(r.pts([(-0.36, 0.4), (-0.2, 0.47), (-0.19, 0.43), (-0.35, 0.36)]), fill=TAN, line=INK, lw=lw * 0.6)
    c.poly(r.E(0, 0.42, 0.28, 0.2, -10), fill=col(0.85, 0.5, 0.2), line=INK, lw=lw)
    c.poly(r.E(0.15, 0.72, 0.1, 0.18, 10), fill=col(0.9, 0.62, 0.25), line=INK, lw=lw)
    c.poly(r.E(0.2, 0.9, 0.11, 0.1), fill=col(0.9, 0.62, 0.25), line=INK, lw=lw)
    for i in range(3):  # the red comb
        c.poly(r.E(0.12 + i * 0.07, 1.0 + 0.02 * (i % 2), 0.045, 0.06), fill=RED, line=INK, lw=lw * 0.7)
    c.poly(r.E(0.3, 0.8, 0.03, 0.06), fill=RED, line=INK, lw=lw * 0.7)  # wattle
    c.poly(r.pts([(0.29, 0.92), (0.4, 0.88), (0.29, 0.85)]), fill=YELLOW, line=INK, lw=lw)
    c.poly(r.E(0.23, 0.93, 0.025, 0.025), fill=WHITE, line=INK, lw=lw * 0.5)
    c.poly(r.E(0.235, 0.93, 0.012, 0.012), fill=INK)
    if mood == 'angry':
        c.line(r.pts([(0.18, 0.98), (0.27, 0.95)]), INK, lw=lw * 1.2)
    return r


def police_helmet(c, r, u=0.02, v=1.02, k=1.0):
    """A British bobby's helmet on a character's rig, at its head top."""
    c.poly(r.pts(smooth([(u - 0.2 * k, v), (u - 0.17 * k, v + 0.2 * k), (u, v + 0.3 * k), (u + 0.17 * k, v + 0.2 * k),
                         (u + 0.2 * k, v)], 5)), fill=NAVY, line=INK, lw=r.lw())
    c.poly(r.E(u, v + 0.31 * k, 0.03 * k, 0.03 * k), fill=SILVER, line=INK, lw=r.lw(0.6))
    c.poly(r.E(u, v + 0.12 * k, 0.05 * k, 0.05 * k), fill=SILVER, line=INK, lw=r.lw(0.6))


def crown(c, r, u, v, k=1.0):
    pts = [(u - 0.15 * k, v), (u - 0.15 * k, v + 0.16 * k), (u - 0.08 * k, v + 0.08 * k), (u, v + 0.2 * k),
           (u + 0.08 * k, v + 0.08 * k), (u + 0.15 * k, v + 0.16 * k), (u + 0.15 * k, v)]
    c.poly(r.pts(pts), fill=YELLOW, line=INK, lw=r.lw())
    for du in (-0.08, 0.0, 0.08):
        c.poly(r.E(u + du * k, v + 0.04 * k, 0.018 * k, 0.018 * k), fill=RED)


def sign(c, x, y, w, h, s, size=44, colr=INK, fill=WHITE, rot=0.0):
    c.poly([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)], fill=fill,
           line=INK, lw=5)
    text(c, s, x, y, size, colr, rot=rot)


def speech(c, x, y, w, h, s, size=34, tail=None):
    c.poly(E(x, y, w, h), fill=WHITE, line=INK, lw=4)
    if tail:
        c.poly([(x - 15, y + h * 0.8), tail, (x + 20, y + h * 0.85)], fill=WHITE, line=INK, lw=4)
        c.poly(E(x, y, w - 4, h - 4), fill=WHITE)
    text(c, s, x, y, size, INK)


# ---------------------------------------------------------------------------
# The common room: this time the pigeon raps and the penguin listens
# ---------------------------------------------------------------------------
P_GEST = {
    # the front wing stays below his face; big raised gestures use the back wing, behind his head
    'point': (95, 20), 'jab': (75, 40), 'wide': (100, 130), 'up': (60, 140), 'chest': (35, 15), 'shrug': (70, 125),
    'down': (10, 10), 'both': (100, 105), 'palm': (85, 125), 'chin': (60, 15),
}
P_POOL = ['point', 'wide', 'jab', 'chest', 'up', 'shrug', 'both', 'palm']


def pigeon_x(t):
    """Sam keeps closing in on Andy, getting right in his face."""
    return lerp(320, 600, sstep(RAP_START, 165, t))


def pigeon_pose(t):
    beat = int(t * 2.3)
    rng = np.random.default_rng(beat * 17 + 3)
    g = P_POOL[int(rng.integers(0, len(P_POOL)))]
    return P_GEST[g], 4 + 12 * loud(t) + (10 if g in ('jab', 'point') else 0)


PENGUIN_EYE = {'neutral': 'normal', 'smirk': 'smug', 'laugh': 'closed', 'grin': 'smug', 'cross': 'angry',
               'shock': 'wide'}


def andy(c, t, x=950, eye=None, arms=None, lean=-3):
    """Andy takes it: amused, stung, scowling, and now and then cracking up."""
    mood, a2, l2, laughing = R.listener_react(t, seed=5)
    if eye is None:
        eye = PENGUIN_EYE[mood]
    beak = (0.4 + 0.5 * abs(math.sin(t * 13))) if laughing else (0.25 if mood == 'shock' else 0.0)
    return penguin(c, x, 690 - (8 * abs(math.sin(t * 13)) if laughing else 0), 300, -1, arms=arms or a2,
                   lean=lean + l2, beak=beak, eye=eye)


def crowd(c, t, react_all=None, skip_host=False):
    R.crowd(c, t, react_all, skip_host=skip_host)


def stage(c, t, name):
    room(c, t)
    if name == 'gasp':
        crowd(c, t, ['gasp', 'cover', 'gasp', 'laugh', 'cover', 'gasp', 'laugh', 'cover'])
        andy(c, t, eye='wide', arms=(30, 20), lean=-12)
    else:
        crowd(c, t)
        andy(c, t)
    arms, lean = pigeon_pose(t)
    pigeon(c, pigeon_x(t), 690, 330, 1, arms=arms, lean=lean, mood='neutral', t=t, beak=rap_beak(t))


def stage_cam(c, t, a, b):
    k = int(a * 10) % 3
    u = (t - a) / max(0.1, b - a)
    if k == 1 and u > 0.35:
        c.cam = (1.6, -pigeon_x(t) * 1.6 + 640, -470 * 1.6 + 360)
    elif k == 2 and u > 0.5:
        c.cam = (1.45, -760 * 1.45 + 640, -470 * 1.45 + 360)


def s_intro(c, t, u):
    """The MC introduces them: Sam, meet Andy. Andy, meet Sam."""
    room(c, t)
    crowd(c, t, 'idle' if t < 10 else 'cheer', skip_host=True)
    k = sstep(11.2, 13.2, t)
    wide = t < 4
    host(c, 640, 640, 230, t)
    pigeon(c, lerp(330, 450, k), 690, 330, 1, arms=(100, 160) if wide else ((95, 15) if k > 0.6 else (15, 15)),
           mood='grin', t=t)
    penguin(c, lerp(950, 830, k), 690, 300, -1, arms=(95, 10) if k > 0.6 else (12, 8), eye='smug')
    if t > 10.6:
        sign(c, 330, 150, 200, 110, 'SAM', 44, RED)
        text(c, 'HELLO my name is', 330, 110, 18, INK)
    if t > 12.4:
        sign(c, 950, 150, 200, 110, 'ANDY', 44, RED)
        text(c, 'HELLO my name is', 950, 110, 18, INK)


def s_fest(c, t, u):
    room(c, t)
    # a banner with bunting
    c.line([(80, 60), (1200, 60)], INK, lw=3)
    for i in range(14):
        x = 100 + i * 78
        c.poly([(x, 60), (x + 50, 60), (x + 25, 100)], fill=[RED, YELLOW, GREEN, JUMPER][i % 4], line=INK, lw=3)
    sign(c, 640, 170, 520, 110, 'RAP FEST', 80, RED, fill=col(1, 0.95, 0.8), rot=-2)
    crowd(c, t, 'cheer' if t < 20 else None, skip_host=True)
    host(c, 640, 560, 140, t)
    # Sam paces, hand on his chin, getting ready
    x = 330 + 60 * math.sin(t * 0.9)
    pigeon(c, x, 690, 330, 1 if math.cos(t * 0.9) > 0 else -1, arms=P_GEST['chin'] if t > 18 else (15, 15),
           mood='neutral', t=t)
    penguin(c, 950, 690, 300, -1, arms=(12, 8), eye='smug')


def s_arrive(c, t, u):
    """Arriving at Oxford: dreaming spires, a suitcase and high hopes."""
    wash(c, col(0.98, 0.86, 0.66))
    c.glow(900, 200, 400, YELLOW, 0.4)
    for (x, w, h) in ((150, 90, 330), (330, 70, 420), (520, 110, 300), (760, 80, 460), (980, 100, 350),
                      (1150, 70, 400)):
        tower = [(x - w / 2, 640), (x - w / 2, 640 - h + 90), (x, 640 - h), (x + w / 2, 640 - h + 90), (x + w / 2, 640)]
        c.poly(tower, fill=STONE, line=INK, lw=5)
        for yy in range(640 - h + 120, 620, 70):
            c.poly(E(x, yy, w * 0.14, 18), fill=NAVY, line=INK, lw=2)
    c.poly([(0, 640), (1280, 640), (1280, 720), (0, 720)], fill=GREEN, line=INK, lw=4)
    c.poly([(560, 640), (560, 380), (720, 380), (720, 640)], fill=STONE, line=INK, lw=5)  # the college gate
    c.poly([(590, 640), (590, 470), (640, 420), (690, 470), (690, 640)], fill=WOOD_D, line=INK, lw=4)
    sign(c, 640, 330, 480, 70, 'UNIVERSITY OF OXFORD', 34, NAVY, fill=col(0.97, 0.95, 0.88))
    x = lerp(-80, 420, sstep(0, 0.6, u))
    r, front = pigeon(c, x, 700, 280, 1, arms=(40, 20), mood='grin', t=t, lean=4 * math.sin(t * 10))
    fx, fy = r.P(0.45, 0.35)
    c.poly([(fx - 60, fy), (fx + 40, fy), (fx + 40, fy + 70), (fx - 60, fy + 70)], fill=col(0.6, 0.3, 0.2), line=INK,
           lw=4)  # suitcase
    c.line([(fx - 20, fy), (fx - 20, fy - 15), (fx + 5, fy - 15), (fx + 5, fy)], INK, lw=5)
    # a stripy college scarf
    c.line(r.pts([(-0.02, 0.84), (0.14, 0.82), (0.26, 0.83)]), RED, lw=r.s * 0.07)
    c.line(r.pts([(0.25, 0.83), (0.3, 0.6)]), RED, lw=r.s * 0.06)
    if u > 0.6:
        pass


def s_obnoxious(c, t, u):
    """...and the people he met there."""
    wash(c, col(0.62, 0.2, 0.25))
    c.poly([(0, 560), (1280, 560), (1280, 720), (0, 720)], fill=col(0.35, 0.12, 0.15), line=INK, lw=4)
    for i, (x, kind, line) in enumerate(((220, 'parrot', 'ACTUALLY...'), (520, 'duck', "Daddy's yacht"),
                                          (820, 'flamingo', 'Have you read Proust?'), (1100, 'toucan', 'Rah!'))):
        r = bird(c, x, 560, 320, kind, 'laugh' if i % 2 else 'gasp', t + i, face=-1 if x > 640 else 1, seed=i)
        # a white bow tie and a mortarboard
        bx, by = r.P(0.1, 0.56)
        c.poly([(bx - 22, by - 12), (bx, by), (bx - 22, by + 12)], fill=WHITE, line=INK, lw=3)
        c.poly([(bx + 22, by - 12), (bx, by), (bx + 22, by + 12)], fill=WHITE, line=INK, lw=3)
        hx, hy = r.P(0.06, 0.9)
        c.poly([(hx - 50, hy - 5), (hx + 50, hy - 5), (hx + 40, hy - 25), (hx - 40, hy - 25)], fill=BLACK, line=INK, lw=3)
        if u > 0.12 * i:
            speech(c, x, 110 + 50 * (i % 2), 145, 55, line, 20 if len(line) > 12 else 30)


def s_coarse(c, t, u):
    """Of course, on this course you'll meet people who are coarse."""
    wash(c, col(0.93, 0.9, 0.84))
    r, _, _ = penguin(c, 820, 690, 380, -1, arms=(20, 15), eye='smug')
    r.ux = 0.74  # match his slim body for the sandpaper texture
    if u > 0.45:  # he turns out to be made of sandpaper
        pts = r.pts(smooth([(-0.32, 0.1), (-0.33, 0.6), (-0.15, 0.9), (0.15, 0.9), (0.33, 0.6), (0.32, 0.1)], 5))
        c.hatch(pts, BROWN, spacing=9, angle=35, lw=2, opacity=0.5)
        c.hatch(pts, BROWN, spacing=13, angle=-50, lw=2, opacity=0.4)
        pass
    text(c, 'COURSE', 330, 200, 90, INK, rot=-3)
    if u > 0.45:
        c.line([(180, 205), (480, 195)], RED, lw=10)
        text(c, 'COARSE', 330, 330, 90, RED, rot=-5)


def s_degenerate(c, t, u):
    """Three generations of penguin, going steadily downhill."""
    wash(c, col(0.9, 0.84, 0.72))
    for i, (x, lbl) in enumerate(((230, 'GRANDAD'), (640, 'DAD'), (1050, 'ANDY'))):
        c.poly([(x - 170, 90), (x + 170, 90), (x + 170, 560), (x - 170, 560)], fill=WOOD, line=INK, lw=6)
        c.poly([(x - 145, 115), (x + 145, 115), (x + 145, 535), (x - 145, 535)], fill=col(0.95, 0.92, 0.84), line=INK,
               lw=3)
        if i < 2 or u > 0.3:
            r, _, _ = penguin(c, x, 520, 330, -1 if x > 640 else 1, arms=(15, 10) if i < 2 else (140, 60),
                              eye='normal' if i == 0 else ('smug' if i == 1 else 'closed'), shirt=i == 2,
                              lean=0 if i < 2 else 12 * math.sin(t * 3))
            if i == 0:  # a monocle and top hat
                c.poly(r.E(0.12, 0.93, 0.05, 0.05), None, SILVER, lw=4)
                c.poly(r.pts([(-0.13, 1.08), (0.17, 1.08), (0.13, 1.4), (-0.09, 1.4)]), fill=BLACK, line=INK, lw=4)
            if i == 1:  # a sensible tie
                c.poly(r.pts([(0.02, 0.8), (0.07, 0.8), (0.1, 0.5), (0.04, 0.45), (-0.01, 0.5)]), fill=RED, line=INK,
                       lw=3)
            if i == 2:
                c.poly(r.pts([(0.3, 0.8), (0.36, 0.8), (0.37, 1.05), (0.29, 1.05)]), fill=col(0.4, 0.6, 0.3), line=INK,
                       lw=3)  # a bottle
        text(c, lbl, x, 600, 36, INK)
    if u > 0.55:
        pass


def s_illiterate(c, t, u):
    wash(c, col(0.88, 0.9, 0.95))
    c.poly([(140, 120), (760, 100), (790, 640), (160, 660)], fill=WHITE, line=INK, lw=6)  # his lyric sheet
    for i in range(9):
        c.line([(170, 180 + i * 50), (770, 165 + i * 50)], col(0.7, 0.8, 0.95), lw=2)
    lines = ['RAPZ BY ANDEE', 'i am the bestt', 'rappa in oxfud', 'you are a', 'poo head', ':)']
    for i, s in enumerate(lines[:1 + int(u * 7)]):
        text(c, s, 460, 170 + i * 75, 44 if i == 0 else 38, [RED, col(0.2, 0.4, 0.9), GREEN][i % 3], rot=-3 + 4 * (i % 2))
    r, f, b = penguin(c, 1020, 700, 360, -1, arms=(95 + 10 * math.sin(t * 16), 20), eye='smug')
    fx, fy = r.P(*f)
    c.line([(fx, fy), (fx - 40, fy + 60)], RED, lw=14)  # a fat crayon
    if u > 0.75:
        text(c, 'F', 700, 560, 140, RED, rot=12)


def s_facts(c, t, u):
    """Face facts: nose to nose with a wall of them."""
    wash(c, col(0.95, 0.93, 0.86))
    c.poly([(80, 60), (820, 60), (820, 660), (80, 660)], fill=col(0.72, 0.55, 0.36), line=INK, lw=6)  # corkboard
    for i, s in enumerate(['FACT: you lost', 'FACT: quit', 'FACT: you are', 'a prick', 'FACT: see above']):
        x, y = 250 + (i % 2) * 330, 140 + i * 105
        c.poly([(x - 150, y - 40), (x + 150, y - 40), (x + 150, y + 40), (x - 150, y + 40)], fill=col(1, 0.97, 0.7),
               line=INK, lw=3)
        c.poly(E(x, y - 38, 9, 9), fill=RED, line=INK, lw=2)
        text(c, s, x, y, 30, INK)
    k = sstep(0.1, 0.5, u)
    penguin(c, lerp(1100, 900, k), 700, 380, -1, arms=(10, 10), lean=lerp(0, 18, k), eye='wide')


def s_getout(c, t, u):
    wash(c, col(0.9, 0.9, 0.86))
    c.poly([(760, 110), (1040, 110), (1040, 660), (760, 660)], fill=col(0.2, 0.2, 0.22), line=INK, lw=6)  # doorway
    k = sstep(0.0, 0.6, u)
    door = 1 - sstep(0.7, 0.85, u)
    if k < 1:
        penguin(c, lerp(560, 900, k), 690, 300, 1, arms=(20, 150), lean=-10, eye='wide')
    c.poly([(1040, 110), (1040 - 280 * (1 - door), 110), (1040 - 280 * (1 - door), 660), (1040, 660)], fill=WOOD,
           line=INK, lw=6)
    sign(c, 900, 60, 200, 60, 'EXIT', 40, WHITE, fill=GREEN)
    pigeon(c, 300, 690, 330, 1, arms=(95, 20), mood='grin', t=t, beak=rap_beak(t))
    if u > 0.85:
        pass


def s_bring(c, t, u):
    """I want to hear what you bring: a party table, and Andy's contribution."""
    wash(c, col(0.98, 0.9, 0.8))
    sign(c, 640, 90, 520, 80, 'BRING A DISH', 50, RED, fill=col(1, 0.97, 0.88))
    c.poly([(80, 460), (1200, 460), (1200, 520), (80, 520)], fill=WHITE, line=INK, lw=5)
    for x, colr in ((230, col(0.9, 0.5, 0.3)), (420, col(0.95, 0.85, 0.4)), (860, col(0.6, 0.35, 0.25)),
                    (1050, col(0.9, 0.4, 0.5))):  # everyone else's feasts
        c.poly(E(x, 450, 90, 25), fill=WHITE, line=INK, lw=4)
        c.poly(smooth([(x - 70, 450), (x - 40, 380), (x + 40, 370), (x + 70, 450)], 4), fill=colr, line=INK, lw=4)
    # Andy's: one sad fish finger
    c.poly(E(640, 450, 90, 25), fill=WHITE, line=INK, lw=4)
    c.poly([(610, 440), (670, 438), (672, 452), (612, 454)], fill=col(0.9, 0.6, 0.2), line=INK, lw=3)
    penguin(c, 640, 720, 200, -1, arms=(60, 10), eye='closed')
    if u > 0.5:
        pass


def s_king(c, t, u):
    """Presents from a peasant to an almighty king."""
    wash(c, col(0.55, 0.14, 0.2))
    c.poly([(300, 150), (560, 150), (560, 650), (300, 650)], fill=col(0.8, 0.15, 0.2), line=YELLOW, lw=12)  # throne
    r, _ = pigeon(c, 430, 640, 360, 1, arms=(20, 20), mood='grin', t=t, beak=rap_beak(t), lean=-4)
    crown(c, r, 0.12, 1.2)
    k = sstep(0.1, 0.5, u)
    rp, f, b = penguin(c, lerp(1250, 850, k), 700, 300, -1, arms=(100, 95), lean=25, shirt=False, eye='closed')
    fx, fy = rp.P(*f)
    c.poly([(fx - 35, fy - 30), (fx + 35, fy - 30), (fx + 35, fy + 20), (fx - 35, fy + 20)], fill=col(0.6, 0.5, 0.35),
           line=INK, lw=4)  # a lumpy parcel
    c.line([(fx, fy - 30), (fx, fy + 20)], RED, lw=5)
    c.poly(rp.pts([(-0.3, 0.1), (-0.32, 0.65), (0.32, 0.65), (0.3, 0.1)]), fill=col(0.62, 0.5, 0.33), line=INK, lw=4,
           opacity=0.95)  # a sackcloth tunic
    if u > 0.5:
        pass


def s_bothered(c, t, u):
    wash(c, col(0.8, 0.92, 0.98))
    c.poly([(0, 560), (1280, 560), (1280, 720), (0, 720)], fill=col(0.95, 0.85, 0.6), line=INK, lw=4)  # a beach
    c.glow(1100, 100, 200, YELLOW, 0.6)
    c.poly(E(1100, 100, 60, 60), fill=YELLOW, line=INK, lw=4)
    c.poly([(420, 640), (620, 640), (680, 450), (480, 450)], fill=col(0.3, 0.6, 0.9), line=INK, lw=5)  # deckchair
    c.hatch([(420, 640), (620, 640), (680, 450), (480, 450)], WHITE, spacing=30, angle=70, lw=8)
    r, _ = pigeon(c, 560, 640, 300, 1, arms=(60, 60), mood='sleepy', t=t, lean=-18)
    hx, hy = r.P(0.2, 1.13)
    c.poly([(hx - 30, hy - 12), (hx + 50, hy - 12), (hx + 45, hy + 12), (hx - 25, hy + 12)], fill=BLACK)  # shades
    pass
    if u > 0.45:
        pass


def s_ring(c, t, u):
    """I'll ring your scrawny neck: a big brass bell collar, rung with gusto."""
    wash(c, col(0.95, 0.9, 0.95))
    r, _, _ = penguin(c, 820, 690, 380, -1, arms=(30, 20), eye='wide', lean=-4)
    nx, ny = r.P(0.02, 0.83)
    c.line([(nx - 70, ny + 5), (nx + 70, ny - 5)], RED, lw=16)  # collar
    sw = 10 * math.sin(t * 25)
    c.poly([(nx - 30 + sw, ny + 70), (nx - 20, ny + 12), (nx + 20, ny + 12), (nx + 30 + sw, ny + 70)], fill=YELLOW,
           line=INK, lw=4)
    c.poly(E(nx + sw, ny + 75, 10, 10), fill=INK)
    pr, f = pigeon(c, 330, 690, 330, 1, arms=(110 + 25 * math.sin(t * 25), 20), mood='grin', t=t, beak=rap_beak(t))
    for i in range(4):
        ph = (u * 4 + i / 4) % 1
        pass


def s_list(c, t, u):
    """A million synonyms, and a list of all the things I hate about you."""
    wash(c, col(0.94, 0.9, 0.8))
    r, f = pigeon(c, 260, 700, 330, 1, arms=(100, 95), mood='grin', t=t, beak=rap_beak(t))
    c.poly([(60, 150), (360, 140), (370, 250), (70, 260)], fill=col(0.5, 0.2, 0.2), line=INK, lw=5)  # a thesaurus
    text(c, '1,000,000', 215, 180, 34, YELLOW)
    text(c, 'SYNONYMS', 215, 225, 30, YELLOW)
    top = 60
    length = lerp(150, 900, sstep(0.1, 0.9, u))
    c.poly([(520, top), (1000, top), (1000, top + length), (520, top + length)], fill=col(0.98, 0.94, 0.8), line=INK,
           lw=5)
    c.poly(E(760, top, 250, 22), fill=col(0.9, 0.85, 0.7), line=INK, lw=5)
    text(c, 'THINGS I HATE ABOUT YOU', 760, top + 50, 30, RED)
    items = ['1. your raps', '2. your shirt', '3. your face', '4. your walk', '5. your beak', '6. your mum*',
             '7. your raps (again)', '8. flippers', '9. ...']
    for i, s in enumerate(items):
        y = top + 110 + i * 62
        if y < top + length - 20:
            text(c, s, 760, y, 30, INK)


def s_far(c, t, u):
    """Don't be trying, Andy, you won't be getting very far."""
    wash(c, col(0.9, 0.93, 0.95))
    c.poly([(420, 560), (1000, 560), (1040, 640), (380, 640)], fill=DARK, line=INK, lw=6)  # treadmill
    for i in range(10):
        x = 400 + ((i * 64 - t * 300) % 640)
        c.line([(x, 590), (x + 10, 630)], GREY, lw=4)
    c.line([(960, 560), (1000, 250)], DARK, lw=16)
    sign(c, 1010, 230, 230, 90, '0.0 km', 44, col(0.3, 1, 0.4), fill=BLACK)
    run = math.sin(t * 16)
    r, _, _ = penguin(c, 700, 580, 330, 1, arms=(60 + 50 * run, 60 - 50 * run), lean=14, eye='angry')
    for i in range(4):
        ph = (u * 3 + i / 4) % 1
        dx, dy = r.P(-0.2, 1.0)
        c.poly(E(dx - 40 * ph, dy + 80 * ph, 7, 11), fill=col(0.6, 0.8, 1.0), line=INK, lw=2)
    pass


def s_level(c, t, u):
    """A different level: Sam in the penthouse, Andy in the basement."""
    wash(c, SKY)
    c.poly([(0, 520), (1280, 520), (1280, 720), (0, 720)], fill=GREEN, line=INK, lw=4)
    c.poly([(300, 20), (980, 20), (980, 620), (300, 620)], fill=col(0.85, 0.82, 0.78), line=INK, lw=6)
    c.poly([(300, 520), (980, 520), (980, 620), (300, 620)], fill=col(0.55, 0.45, 0.35), line=INK, lw=6)
    for y in (180, 300, 410):
        c.line([(300, y), (980, y)], INK, lw=5)
    text(c, 'LEVEL 99', 400, 50, 30, INK)
    text(c, 'LEVEL -1', 400, 545, 26, WHITE)
    c.glow(640, 110, 200, YELLOW, 0.5)
    pr, _ = pigeon(c, 640, 175, 130, 1, arms=(95, 90), mood='grin', t=t, beak=rap_beak(t))
    c.poly([(690, 120), (800, 120), (800, 175), (690, 175)], fill=WOOD, line=INK, lw=3)  # his writing desk
    penguin(c, 640, 612, 80, 1, arms=(170, 170), eye='wide')
    for i in range(3):
        c.poly([(760 + i * 60, 612), (810 + i * 60, 612), (810 + i * 60, 572), (760 + i * 60, 572)], fill=TAN, line=INK,
               lw=3)
    k = sstep(0.2, 0.8, u)
    c.line([(1100, 650), (1100, 60)], INK, lw=4)
    c.poly([(1080, 650 - 560 * k), (1120, 650 - 560 * k), (1100, 620 - 560 * k)], fill=RED)
    pass


def s_wife(c, t, u):
    """Can't wait for your wife to admit that she never loved you."""
    wash(c, col(0.98, 0.9, 0.92))
    # the wedding photo on the wall
    c.poly([(80, 80), (420, 80), (420, 380), (80, 380)], fill=YELLOW, line=INK, lw=6)
    c.poly([(100, 100), (400, 100), (400, 360), (100, 360)], fill=col(0.95, 0.95, 1.0), line=INK, lw=3)
    penguin(c, 200, 350, 140, 1, arms=(10, 10), eye='closed')
    rw, _, _ = penguin(c, 310, 350, 130, -1, arms=(10, 10), eye='closed', shirt=False)
    c.poly(rw.pts(smooth([(-0.25, 1.05), (0.1, 1.15), (0.3, 0.9), (0.4, 0.4), (-0.2, 0.5)], 4)), fill=WHITE, line=INK,
           lw=2, opacity=0.7)
    if u > 0.4:  # a crack across the glass
        c.line([(120, 120), (230, 220), (200, 280), (330, 350)], INK, lw=4)
    # Andy, and his wife holding up a sign
    penguin(c, 640, 700, 300, 1, arms=(20, 20), eye='wide')
    rw, f, b = penguin(c, 1000, 700, 300, -1, arms=(150, 150), eye='smug', shirt=False)
    c.poly(rw.E(0.1, 0.99, 0.1, 0.05), fill=PINK, line=INK, lw=2)  # a bow
    c.poly(rw.E(0.2, 0.99, 0.08, 0.05), fill=PINK, line=INK, lw=2)
    if u > 0.3:
        sign(c, 1000, 180, 330, 110, 'NEVER', 50, RED, fill=WHITE, rot=4)
        text(c, 'LOVED YOU', 1000, 215, 30, INK, rot=4)
    # Sam with popcorn: he couldn't wait
    r, _ = pigeon(c, 470, 330, 150, 1, arms=(100, 90), mood='grin', t=t)
    c.poly([(500, 250), (560, 250), (550, 310), (510, 310)], fill=WHITE, line=RED, lw=4)
    for i in range(5):
        c.poly(E(510 + i * 11, 245 - 6 * (i % 2), 10, 9), fill=col(1, 0.97, 0.85), line=INK, lw=2)


def s_court(c, t, u):
    """They say I murder this shit, but to me it's just manslaughter."""
    wash(c, col(0.7, 0.55, 0.4))
    c.poly([(420, 260), (860, 260), (860, 520), (420, 520)], fill=WOOD, line=INK, lw=6)  # the bench
    wr = Rig(c, 640, 250, 200, 1)
    c.poly(wr.pts(smooth([(-0.22, 0.85), (-0.25, 1.02), (0.06, 1.12), (0.34, 1.0), (0.32, 0.75), (0.36, 0.5),
                          (-0.3, 0.5)], 5)), fill=col(0.96, 0.95, 0.9), line=INK, lw=4)  # wig, behind his face
    for v in (0.6, 0.7, 0.8):
        c.line(wr.pts([(-0.3, v), (-0.2, v)]), GREY, lw=3)
        c.line(wr.pts([(0.26, v), (0.35, v)]), GREY, lw=3)
    bird(c, 640, 250, 200, 'owl', 'idle', t, 1)
    k = abs(math.sin(t * 5))
    c.line([(820, 250 - 30 * k), (760, 300)], WOOD_D, lw=12)
    c.poly(E(820, 245 - 30 * k, 26, 16), fill=WOOD_D, line=INK, lw=3)
    pigeon(c, 200, 700, 280, 1, arms=(60, 20), mood='grin', t=t, beak=rap_beak(t))
    c.poly([(80, 520), (330, 520), (330, 700), (80, 700)], fill=WOOD_D, line=INK, lw=5)  # the dock
    sign(c, 1080, 200, 300, 90, 'MURDER', 50, INK, fill=WHITE, rot=-3)
    if u > 0.5:
        c.line([(940, 200), (1220, 200)], RED, lw=10)
        sign(c, 1060, 380, 380, 90, 'MANSLAUGHTER', 44, RED, fill=WHITE, rot=3)


def s_stork(c, t, u):
    """Never able to have a son or a daughter: the stork turns round and flies off."""
    wash(c, SKY)
    c.poly([(0, 600), (1280, 600), (1280, 720), (0, 720)], fill=GREEN, line=INK, lw=4)
    c.poly(E(300, 540, 150, 60), fill=col(0.6, 0.75, 0.95), line=INK, lw=5)  # an empty pram
    c.poly([(150, 540), (220, 440), (300, 480)], fill=col(0.4, 0.55, 0.85), line=INK, lw=5)
    for x in (200, 400):
        c.poly(E(x, 610, 30, 30), None, INK, lw=6)
    sign(c, 300, 380, 280, 60, 'OUT OF ORDER', 32, RED, rot=-5)
    turn = u > 0.4
    x = lerp(1350, 800, sstep(0, 0.4, u)) if not turn else lerp(800, 1450, sstep(0.45, 1.0, u))
    face = -1 if not turn else 1
    y = 220 + 20 * math.sin(t * 6)
    r = Rig(c, x, y, 160, face)
    c.poly(r.E(0, 0, 0.45, 0.2), fill=WHITE, line=INK, lw=4)
    flap = math.sin(t * 9)
    c.poly(r.pts([(-0.2, 0.05), (0.15, 0.05), (-0.1, 0.6 * flap)]), fill=WHITE, line=INK, lw=4)
    c.line(r.pts([(0.3, 0.1), (0.55, 0.3)]), WHITE, lw=18)
    c.poly(r.E(0.6, 0.33, 0.09, 0.08), fill=WHITE, line=INK, lw=3)
    c.poly(r.pts([(0.66, 0.35), (1.0, 0.25), (0.66, 0.29)]), fill=ORANGE, line=INK, lw=3)
    c.line(r.pts([(-0.4, -0.05), (-0.85, -0.15)]), ORANGE, lw=6)
    bx, by = r.P(0.95, 0.15)
    c.poly(E(bx, by + 40, 40, 30), fill=col(0.97, 0.92, 0.95), line=INK, lw=3)  # the bundle
    c.line([(bx, by), (bx, by + 15)], INK, lw=3)
    if turn:
        pass


def s_phone(c, t, u):
    wash(c, col(0.95, 0.9, 0.8))
    r, f = pigeon(c, 520, 700, 460, 1, arms=(60, 168), mood='neutral', t=t, beak=rap_beak(t), lean=-5)
    hx, hy = r.P(-0.02, 1.1)
    c.poly([(hx - 30, hy - 60), (hx - 5, hy - 66), (hx + 10, hy + 60), (hx - 15, hy + 66)], fill=DARK, line=INK, lw=5)
    for i, d in enumerate('999'):
        if u > 0.15 + 0.2 * i:
            text(c, d, 900 + i * 110, 240, 150, RED, rot=(-1) ** i * 6)


def s_police(c, t, u):
    """Kearns here, emergency services, connect me straight to the police."""
    wash(c, col(0.85, 0.88, 0.95))
    c.line([(640, 0), (640, 720)], INK, lw=6)
    r, _ = pigeon(c, 320, 700, 380, 1, arms=(60, 168), mood='grin', t=t, beak=rap_beak(t))
    hx, hy = r.P(-0.02, 1.1)
    c.poly([(hx - 24, hy - 48), (hx - 4, hy - 53), (hx + 8, hy + 48), (hx - 12, hy + 53)], fill=DARK, line=INK, lw=4)
    pr = bird(c, 960, 690, 360, 'duck', 'idle', t, -1)
    police_helmet(c, pr, 0.06, 0.86, 0.9)
    c.poly([(1120, 380), (1250, 380), (1250, 700), (1120, 700)], fill=NAVY, line=INK, lw=5)  # a police box
    on = int(t * 4) % 2
    c.glow(1185, 360, 90, col(0.3, 0.5, 1.0) if on else RED, 0.8)
    c.poly(E(1185, 360, 22, 16), fill=col(0.4, 0.6, 1.0) if on else RED, line=INK, lw=3)
    text(c, 'POLICE', 1185, 420, 26, WHITE)
    if u > 0.3:
        speech(c, 900, 150, 200, 60, 'Go on, Mr Kearns', 26, (920, 260))


def s_maggot(c, t, u):
    """A little maggot in need of a beating: into the mixing bowl with the whisk."""
    wash(c, col(0.96, 0.93, 0.86))
    c.poly(smooth([(360, 380), (920, 380), (860, 640), (420, 640)], 4), fill=col(0.85, 0.9, 0.95), line=INK, lw=6)
    # Andy, dressed as a maggot, peeking over the rim
    r, _, _ = penguin(c, 640, 560, 260, -1, arms=(150, 150), eye='wide', shirt=False)
    mag = r.pts(smooth([(-0.32, 0.1), (-0.34, 0.8), (-0.1, 1.2), (0.2, 1.2), (0.36, 0.8), (0.32, 0.1)], 6))
    c.poly(mag, fill=col(0.97, 0.93, 0.78), line=INK, lw=4, opacity=0.9)
    for v in (0.3, 0.55, 0.8, 1.02):
        c.line(r.pts([(-0.3, v), (0.32, v + 0.02)]), col(0.75, 0.68, 0.5), lw=4)
    c.poly(r.E(0.1, 0.95, 0.06, 0.06), fill=WHITE, line=INK, lw=3)
    c.poly(r.E(0.12, 0.95, 0.025, 0.025), fill=INK)
    c.poly(smooth([(360, 380), (920, 380), (900, 470), (380, 470)], 4), fill=col(0.85, 0.9, 0.95), line=INK, lw=6)
    ang = t * 20
    wx, wy = 640 + 180 * math.cos(ang), 330 + 30 * math.sin(ang)  # the whisk going round
    c.line([(wx, wy), (wx + 60, wy - 220)], SILVER, lw=12)
    for k in range(-2, 3):
        c.line([(wx, wy), (wx + 10 * k - 10, wy + 60), (wx + 5 * k, wy + 120)], SILVER, lw=4)
    pass


def s_rooster(c, t, u):
    """You'll smell the cock he's been eating."""
    wash(c, col(0.97, 0.94, 0.84))
    r, _, _ = penguin(c, 450, 700, 380, 1, arms=(20, 20), eye='smug')
    for i in range(3):  # the smell
        ph = (u * 3 + i / 3) % 1
        x0, y0 = r.P(0.3, 1.0)
        c.line(smooth([(x0 + 20 * i, y0 - 30 * ph), (x0 + 30 + 20 * i, y0 - 70 - 30 * ph), (x0 + 10 + 20 * i, y0 - 110 - 30 * ph),
                       (x0 + 40 + 20 * i, y0 - 150 - 30 * ph)], 4, False), col(0.5, 0.65, 0.2), lw=6, opacity=1 - ph)
    bx, by = r.P(0.36, 0.95)
    for i in range(3):  # a few feathers stuck to his beak
        c.line([(bx + i * 12, by), (bx + 20 + i * 14, by - 30)], col(0.12, 0.35, 0.3), lw=6)
    rooster(c, 950, 700, 320, -1, plucked=1.0)
    pass


def s_fish(c, t, u):
    """You are what you eat."""
    wash(c, col(0.8, 0.92, 0.96))
    pass
    if u < 0.4:
        r, f, b = penguin(c, 640, 700, 380, -1, arms=(110, 20), eye='closed', beak=0.6)
        fx, fy = r.P(*f)
        c.poly(E(fx, fy - 20, 60, 22), fill=SILVER, line=INK, lw=4)
        c.poly([(fx + 55, fy - 20), (fx + 90, fy - 45), (fx + 90, fy + 5)], fill=SILVER, line=INK, lw=4)
    else:  # he's turned into one: a fish in a check shirt
        wob = 10 * math.sin(t * 8)
        body = smooth([(380, 420 + wob), (560, 300), (800, 320), (900, 420), (800, 520), (560, 540)], 6)
        c.poly(body, fill=SILVER, line=INK, lw=6)
        c.poly([(360, 420 + wob), (240, 320 + wob), (260, 520 + wob)], fill=SILVER, line=INK, lw=6)
        shirt = smooth([(520, 310), (700, 310), (720, 520), (520, 530)], 4)
        c.poly(shirt, fill=PLAID, line=INK, lw=4)
        c.hatch(shirt, R.PLAID_D, spacing=18, angle=0, lw=3, opacity=0.7)
        c.hatch(shirt, R.PLAID_D, spacing=18, angle=90, lw=3, opacity=0.7)
        c.poly(E(820, 390, 22, 22), fill=WHITE, line=INK, lw=4)
        c.poly(E(826, 390, 9, 9), fill=INK)
        c.line([(860, 450), (895, 440)], INK, lw=5)
        for i in range(4):
            ph = (u * 3 + i / 4) % 1
            c.poly(E(920 + 30 * i, 420 - 250 * ph, 10 + 4 * i, 10 + 4 * i), None, WHITE, lw=4)


def s_hear(c, t, u):
    """What's that? I'm sorry, I didn't hear you, Andy."""
    wash(c, col(0.93, 0.9, 0.84))
    r, f = pigeon(c, 380, 700, 360, 1, arms=(100, 20), mood='neutral', t=t, beak=rap_beak(t), lean=12)
    hx, hy = r.P(0.05, 1.12)
    c.poly([(hx - 20, hy - 10), (hx + 30, hy - 20), (hx + 420, hy - 120), (hx + 420, hy + 80), (hx + 30, hy + 20)],
           fill=YELLOW, line=INK, lw=5)  # an ear trumpet
    c.poly(E(hx + 420, hy - 20, 30, 100), fill=col(0.8, 0.6, 0.2), line=INK, lw=5)
    penguin(c, 1080, 700, 160, -1, arms=(95, 10), eye='angry', beak=beak_open(t * 1.3 + 1))
    if u > 0.4:
        pass


def s_syringe(c, t, u):
    wash(c, col(0.85, 0.95, 0.93))
    c.poly([(560, 560), (1200, 560), (1200, 620), (560, 620)], fill=WHITE, line=INK, lw=5)  # hospital bed
    c.line([(600, 620), (600, 710)], SILVER, lw=12)
    c.line([(1160, 620), (1160, 710)], SILVER, lw=12)
    penguin(c, 880, 560, 200, -1, arms=(40, 20), eye='wide')
    R.standing_heron(c, 260, 700, 300, t, 1)
    k = sstep(0.1, 0.5, u)
    x0 = lerp(300, 560, k)
    c.poly([(x0, 330), (x0 + 260, 330), (x0 + 260, 400), (x0, 400)], fill=col(0.9, 0.95, 1.0), line=INK, lw=5)
    c.poly([(x0 + 20, 340), (x0 + 200, 340), (x0 + 200, 390), (x0 + 20, 390)], fill=col(1.0, 0.85, 0.3))
    c.line([(x0 + 260, 365), (x0 + 360, 365)], SILVER, lw=4)
    c.line([(x0 - 80, 365), (x0, 365)], SILVER, lw=16)
    text(c, '20cc PENICILLIN', x0 + 130, 300, 30, INK)


def s_mandy(c, t, u):
    """Twenty kilos of Mandy: a flamingo called Mandy on the bathroom scales."""
    wash(c, col(0.94, 0.95, 0.98))
    c.poly(smooth([(420, 540), (860, 540), (860, 620), (420, 620)], 3), fill=WHITE, line=INK, lw=6)
    kg = int(20 * sstep(0.1, 0.5, u))
    c.poly([(560, 555), (720, 555), (720, 605), (560, 605)], fill=DARK, line=INK, lw=3)
    text(c, f'{kg} kg', 640, 580, 34, col(0.4, 1, 0.5))
    bird(c, 640, 550, 300, 'flamingo', 'cheer' if u > 0.5 else 'idle', t, 1)
    sign(c, 660, 470, 170, 60, 'MANDY', 32, RED, fill=WHITE, rot=-6)
    text(c, 'HELLO my name is', 660, 450, 13, INK, rot=-6)
    pigeon(c, 180, 700, 260, 1, arms=(95, 20), mood='grin', t=t, beak=rap_beak(t))


def s_planb(c, t, u):
    wash(c, col(0.92, 0.92, 0.9))
    c.poly([(160, 80), (1120, 80), (1120, 580), (160, 580)], fill=WHITE, line=GREY, lw=14)  # whiteboard
    text(c, 'PLAN A', 400, 200, 70, col(0.2, 0.4, 0.8))
    c.line([(260, 200), (540, 200)], RED, lw=10)
    if u > 0.25:
        text(c, 'PLAN B', 860, 200, 70, col(0.2, 0.4, 0.8))
        c.poly(E(860, 200, 190, 70), None, RED, lw=6)
    if u > 0.6:
        pass
    pigeon(c, 1180, 720, 200, -1, arms=(100, 20), mood='grin', t=t, beak=rap_beak(t))


def s_stairs(c, t, u):
    """Push you down the stairs, but make it low-key: stairs made of piano keys."""
    wash(c, col(0.95, 0.92, 0.86))
    for i in range(8):
        x0, y0 = 120 + i * 130, 260 + i * 50
        c.poly([(x0, y0), (x0 + 130, y0), (x0 + 130, 720), (x0, 720)], fill=WHITE, line=INK, lw=4)
        c.poly([(x0 + 85, y0), (x0 + 125, y0), (x0 + 125, y0 + 30), (x0 + 85, y0 + 30)], fill=INK)
    pass
    pigeon(c, 150, 260, 200, 1, arms=(95, 20), mood='grin', t=t, beak=rap_beak(t))
    k = sstep(0.15, 1.0, u)
    step = min(7, int(k * 8))
    x = 250 + step * 130 + (k * 8 - step) * 130
    y = 260 + step * 50 - 50 * math.sin((k * 8 - step) * math.pi)
    penguin(c, x, y, 150, 1, arms=(150, 150), lean=int(k * 16) * 45 % 360 if u > 0.15 else 0, eye='wide')
    if u > 0.15:
        c.glow(250 + step * 130, 260 + step * 50, 60, YELLOW, 0.8)  # the key he lands on
        for i in range(3):
            ph = (u * 4 + i / 3) % 1
            text(c, '♪', x + 40 * i, y - 150 - 90 * ph, 50, INK, opacity=1 - ph)


def s_statue(c, t, u):
    wash(c, col(0.35, 0.28, 0.4))
    c.glow(640, 200, 400, YELLOW, 0.5)
    c.poly([(470, 470), (810, 470), (840, 720), (440, 720)], fill=STONE, line=INK, lw=6)  # plinth
    text(c, 'SEMINAL', 640, 510, 30, INK)
    text(c, 'IMMORTAL', 640, 550, 30, INK)
    text(c, 'INCREDIBLE', 640, 590, 30, INK)
    r, _ = pigeon(c, 640, 470, 300, 1, arms=(60, 170), mood='grin', t=t, beak=rap_beak(t))
    for i in range(7):  # a laurel wreath
        a = math.pi * (0.1 + 0.8 * i / 6)
        c.poly(r.E(0.12 + 0.17 * math.cos(a), 1.12 + 0.12 * math.sin(a), 0.05, 0.025, math.degrees(a)), fill=GREEN,
               line=INK, lw=2)
    for x, kind in ((150, 'owl'), (1130, 'puffin')):
        bird(c, x, 720, 200, kind, 'cheer', t, 1 if x < 640 else -1)


def s_criminal(c, t, u):
    """To ignore my metaphors would be criminal."""
    wash(c, col(0.94, 0.92, 0.88))
    for i, s in enumerate(('METAPHOR', 'SIMILE', 'PUN')):
        x = 250 + i * 390
        c.poly([(x - 150, 90), (x + 150, 90), (x + 150, 330), (x - 150, 330)], fill=YELLOW, line=INK, lw=6)
        c.poly([(x - 125, 115), (x + 125, 115), (x + 125, 305), (x - 125, 305)], fill=col(0.6, 0.8, 0.95), line=INK,
               lw=3)
        text(c, s, x, 210, 34, INK)
    k = sstep(0.0, 0.5, u)
    rp, _, _ = penguin(c, lerp(200, 700, k), 700, 280, 1, arms=(10, 10), eye='closed', lean=-10)
    if u > 0.5:
        pr = bird(c, 980, 700, 280, 'duck', 'gasp', t, -1)
        police_helmet(c, pr, 0.06, 0.86, 0.9)
        c.poly(E(820, 520, 30, 20), None, SILVER, lw=8)  # handcuffs
        c.poly(E(870, 520, 30, 20), None, SILVER, lw=8)
        sign(c, 640, 400, 480, 70, 'CRIME: IGNORING ART', 34, RED)


def s_minuscule(c, t, u):
    wash(c, col(0.94, 0.93, 0.9))
    for (x, y, w, h, colr) in ((140, 560, 160, 60, DARK), (230, 500, 90, 80, GREY), (120, 480, 70, 90, BROWN),
                               (270, 600, 120, 40, RED)):
        c.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill=colr, line=INK, lw=4)  # a scrap pile
    c.poly(E(200, 650, 70, 30), None, DARK, lw=16)
    pass
    c.poly([(640, 700), (760, 700), (740, 620), (660, 620)], fill=DARK, line=INK, lw=5)  # microscope
    c.line([(700, 620), (700, 380)], DARK, lw=24)
    c.poly([(670, 400), (730, 400), (720, 330), (680, 330)], fill=DARK, line=INK, lw=4)
    penguin(c, 560, 700, 260, 1, arms=(95, 20), lean=20, eye='wide')
    c.poly(E(1000, 300, 220, 220), fill=col(0.9, 0.97, 0.9), line=INK, lw=8)  # the view down the lens
    c.poly(E(1000, 300, 3, 3), fill=INK)
    c.line([(1010, 310), (1100, 400)], INK, lw=3)
    pass


def s_pinnacle(c, t, u):
    wash(c, SKY)
    c.poly([(80, 720), (640, 150), (1200, 720)], fill=col(0.6, 0.6, 0.65), line=INK, lw=6)
    c.poly([(500, 290), (640, 150), (780, 290), (700, 260), (640, 300), (580, 260)], fill=WHITE, line=INK, lw=5)
    for x in (200, 1080):
        c.poly(E(x, 150, 120, 40), fill=WHITE, line=INK, lw=3)
    k = sstep(0.0, 0.5, u)
    x, y = lerp(300, 640, k), lerp(560, 150, k)
    pigeon(c, x, y, 150, 1, arms=(160, 30) if k >= 1 else (60 + 40 * math.sin(t * 12), 20), mood='grin', t=t,
           beak=rap_beak(t))
    if k >= 1:
        c.line([(700, 150), (700, 40)], INK, lw=5)
        c.poly([(700, 40), (790, 60), (700, 80)], fill=RED, line=INK, lw=3)
        text(c, 'SAM', 740, 62, 22, WHITE)
    penguin(c, 1000, 715, 80, -1, arms=(170, 170), eye='wide')


def s_drunk(c, t, u):
    """Can't leave his flat without coming back all over the place."""
    wash(c, col(0.4, 0.38, 0.5))
    c.poly([(80, 60), (560, 60), (560, 720), (80, 720)], fill=col(0.8, 0.75, 0.65), line=INK, lw=6)  # the flat
    c.poly([(220, 250), (420, 250), (420, 720), (220, 720)], fill=col(0.1, 0.1, 0.12), line=INK, lw=5)
    sign(c, 320, 200, 150, 50, 'FLAT 2B', 28, INK)
    c.poly([(0, 690), (1280, 690), (1280, 720), (0, 720)], fill=DARK, line=INK, lw=3)
    # out he comes... and straight back in
    k = u * 2 if u < 0.5 else 2 - u * 2
    x = lerp(320, 900, sstep(0, 1, k)) + 60 * math.sin(t * 3)
    penguin(c, x, 700, 300, 1 if u < 0.5 else -1, arms=(130 + 30 * math.sin(t * 5), 40), lean=18 * math.sin(t * 2.5),
            eye='closed')
    for i, (bx, rot) in enumerate(((700, 80), (1000, -60), (1150, 90))):
        c.poly(E(bx, 680, 40, 12, rot / 4), fill=col(0.3, 0.55, 0.3), line=INK, lw=3)
    for i in range(3):
        ph = (u * 2 + i / 3) % 1
        c.poly(E(x + 40 + 20 * i, 250 - 120 * ph, 10 + 5 * i, 10 + 5 * i), None, WHITE, lw=4)
    pass


def s_dictionary(c, t, u):
    wash(c, col(0.9, 0.85, 0.75))
    book = [(120, 90), (640, 120), (1160, 90), (1160, 660), (640, 690), (120, 660)]
    c.poly(book, fill=col(0.98, 0.96, 0.9), line=INK, lw=6)
    c.line([(640, 120), (640, 690)], INK, lw=4)
    for i in range(10):
        c.line([(170, 150 + i * 50), (590, 170 + i * 50)], GREY, lw=3)
    text(c, 'shit-faced', 900, 200, 50, INK)
    text(c, '(adj.)', 900, 250, 28, GREY)
    text(c, '1. very, very drunk', 900, 320, 30, INK)
    if u > 0.35:
        text(c, '2. see: ANDY', 900, 380, 36, RED)
        penguin(c, 900, 620, 170, -1, arms=(130, 40), lean=15, eye='closed')
        c.poly([(780, 420), (1020, 420), (1020, 640), (780, 640)], None, INK, lw=3)


def s_retreat(c, t, u):
    """Back on his feet, and rapping against me again at the guided retreat."""
    wash(c, col(0.85, 0.95, 0.85))
    c.poly([(0, 560), (1280, 560), (1280, 720), (0, 720)], fill=GREEN, line=INK, lw=4)
    for x in (100, 1180):
        c.line([(x, 560), (x, 250)], BROWN, lw=24)
        c.poly(E(x, 230, 120, 90), fill=col(0.3, 0.55, 0.3), line=INK, lw=4)
    sign(c, 640, 90, 440, 80, 'GUIDED RETREAT', 44, col(0.3, 0.5, 0.3), fill=col(1, 0.98, 0.9))
    for x in (380, 700, 1000):
        c.poly([(x - 110, 660), (x + 110, 660), (x + 100, 690), (x - 120, 690)], fill=[PINK, JUMPER, YELLOW][x % 3],
               line=INK, lw=3)
    guru = bird(c, 700, 660, 220, 'owl', 'sleep', t, 1)
    stand = sstep(0.0, 0.35, u)
    penguin(c, 380, 690, lerp(150, 260, stand), 1, arms=(100, 110) if u > 0.4 else (170, 170),
            lean=lerp(80, 0, stand), eye='angry', beak=beak_open(t) * (u > 0.4))
    pigeon(c, 1000, 690, 250, -1, arms=(50, 50), mood='sleepy', t=t)
    pass


def s_joke(c, t, u):
    """The biggest joke: Andy in the spotlight, the crowd in stitches."""
    wash(c, col(0.1, 0.08, 0.12))
    c.glow(640, 400, 330, YELLOW, 0.5)
    c.poly(E(640, 690, 260, 40), fill=col(0.5, 0.2, 0.25), line=INK, lw=4)
    penguin(c, 640, 690, 330, -1, arms=(95, 20), eye='smug')
    c.line([(560, 480), (560, 690)], SILVER, lw=8)  # a mic stand
    c.poly(E(560, 470, 16, 24), fill=DARK, line=INK, lw=3)
    pass
    for i, (x, kind) in enumerate(((120, 'owl'), (280, 'duck'), (1000, 'parrot'), (1160, 'robin'))):
        bird(c, x, 720, 170, kind, 'laugh', t, 1 if x < 640 else -1, seed=i)
    if u > 0.75:
        pass


def s_finale(c, t, u):
    """Applause: the MC rolls on the floor laughing, and the two of them hug it out."""
    room(c, t)
    crowd(c, t, 'cheer', skip_host=True)
    v = t - 167.6
    # the MC, on his back, kicking with laughter
    host(c, 1120, 715, 170, t, react='laugh')
    k = min(1.0, max(0.0, (v - 1.0) / 1.2))
    pigeon(c, lerp(pigeon_x(t), 470, k), 690, 330, 1, arms=(110, 110) if k > 0.8 else (20, 20),
           mood='laugh' if v > 1 else 'grin', t=t)
    penguin(c, lerp(950, 800, k), 690, 300, -1, arms=(115, 115) if k > 0.8 else (15, 10), lean=8 * k, eye='closed')
    if v > 3.5:
        text(c, 'RESPECT.', 640, 120, 60, INK, opacity=clamp01((v - 3.5) / 1.0))


CUTAWAYS = {k[2:]: v for k, v in globals().items() if k.startswith('s_') and callable(v)}


def render(d):
    t = d / FPS
    c = Sketch(d)
    a, b, name = shot_at(t)
    u = clamp01((t - a) / max(0.1, b - a))
    if name in CUTAWAYS:
        if False:  # (no mid-picture cutbacks: they interrupt the gag)
            c.cam = (1.6, -pigeon_x(t) * 1.6 + 640, -470 * 1.6 + 360)
            stage(c, t, 'stage')
        else:
            CUTAWAYS[name](c, t, u)
    else:
        stage_cam(c, t, a, b)
        stage(c, t, name)
    return R.overlay(c.result(), t)


def make_audio(path):
    import subprocess
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', AUDIO, '-t', str(DUR), '-af',
                    f'afade=t=out:st={DUR - 1.5}:d=1.5', path], check=True)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for ts in sys.argv[3:]:
            Image.fromarray(render(int(round(float(ts) * FPS)))).save(os.path.join(out, f'sam_{float(ts):06.2f}s.png'))
    elif mode == 'render':
        render_video(sys.argv[2], render, int(DUR * FPS), make_audio,
                     crf=int(sys.argv[3]) if len(sys.argv) > 3 else 32, size=(W, H))
