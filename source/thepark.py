#!/usr/bin/env python3
"""The Park, rebuilt as a full Satire-style film (from satire_template.py). Sam's voice and birdsong are kept; every
drawing and every movement is new.

Story: an old man on a park bench (flat cap, camel coat, grey beard) feeds the pigeons, unimpressed. He glances at the
one on the bench beside him. Close on it: it tips its head back, looks up at him and opens its beak: "Nobody will
believe you." He is stunned. It flies off. The other pigeons just carry on being
pigeons, and his eyes dart from one to the next in case one of them speaks too.
References (Sam, 8 Oct): a rock dove (grey body, dark head, green-purple neck sheen, two dark wing bars, orange eye,
pink feet); a pigeon tipping its head back with its beak wide open; older Black men in a park (flat cap, camel coat,
short grey beard); their shock (eyes wide with white all round, raised brows, forehead lines, mouth open).

    python3 source/thepark.py cast OUT.png              the cast on one sheet: approve it before any animation
    python3 source/thepark.py stills OUT_DIR T [T ...]  stills at these times (seconds)
    python3 source/thepark.py check                     every check and the audit
    python3 source/thepark.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT]
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402  people: flat shapes, black outlines
import mossad as M               # noqa: E402  (brows, mouths, hair; patched into burnham on import)
import figure as F               # noqa: E402  arms solved and guarded
import mossad_audio as MA        # noqa: E402  recordings cleaned and levelled
import peepee as PP              # noqa: E402  the series' caption
import filmkit                   # noqa: E402  the general checks
import film_engine as E          # noqa: E402  render with the picture cache, subtitle list, mouth check
from burnham_film import load    # noqa: E402
from satire_style import Cam as SCam, Ctx, blob, limb, rough, install_circle_hands   # noqa: E402

install_circle_hands(B)
FPS, SR = 12, MA.SR
INK = (24, 20, 22)

# =============================================== STORY ==============================================================
NAME = 'thepark'
TITLE = ('THE', 'PARK')
LINE = 'Nobody will believe you.'
VOICE, VOICE_FROM, VOICE_TO, VOICE_GAIN = 'park-1', 1.45, 3.75, 1.6        # Sam's take (the pigeon)
BIRDS = os.path.join(HERE, 'audio', 'park-ambient-clip.mp3')            # his birdsong
VL = VOICE_TO - VOICE_FROM
T1 = 5.0                    # cut to the bench pigeon, close: it looks up at him
SAY = T1 + 1.9              # it speaks, after a slow push in on its stare (Sam: tension first)
T2 = SAY + VL + 0.7         # back to the wide: he is stunned
FLY = T2 + 2.0              # it takes off, after a long beat of the two staring at each other
DUR = FLY + 5.2             # he stares after it, then the sting: his eyes flick from pigeon to pigeon
SHOTS = [('wide', 0.0, T1 - 1.0), ('glance', T1 - 1.0, T1), ('talk', T1, T2), ('end', T2, DUR)]
MAN = dict(skin=B.DEEP, hair='bald', hair_c=(150, 150, 154), jacket=(176, 122, 72), shirt=(60, 62, 70), tie=None,
           trousers=(70, 64, 58), outfit='suit', jaw='round', hw=74, hh=90, age=True, full=False, pose='custom',
           beard='full', beard_c=(170, 168, 166), beard_grey=(214, 212, 210))
CAP, CAP_D = (126, 58, 46), (92, 40, 32)      # his flat cap
SHOCK = 2                                     # how shocked he is, 1-6 (Sam picks from the shock sheet)
SHOCKS = [   # eye (w, h), pupil, brow lift and arch, forehead lines, open mouth (w, h), cap jump, sweat drops, tremble
    dict(name='1 Puzzled', eye=(15, 15), pupil=6.0, brow=4, arch=4, one_brow=True, lines=0, mouth=None, pop=12, sweat=0, tremble=False),
    dict(name='2 Taken aback', eye=(16, 18), pupil=5.5, brow=6, arch=6, lines=1, mouth=(6, 7), pop=18, sweat=0, tremble=False),
    dict(name='3 Alarmed', eye=(18, 21), pupil=4.5, brow=9, arch=9, lines=2, mouth=(10, 12), pop=30, sweat=0, tremble=False),
    dict(name='4 Shocked', eye=(19, 23), pupil=4.0, brow=12, arch=11, lines=3, mouth=(12, 17), pop=42, sweat=0, tremble=False),
    dict(name='5 Aghast', eye=(22, 26), pupil=3.0, brow=16, arch=13, lines=3, mouth=(15, 25), pop=58, sweat=1, tremble=False),
    dict(name='6 Frozen rigid', eye=(25, 30), pupil=2.0, brow=20, arch=15, lines=4, mouth=(16, 36), pop=90, sweat=2, tremble=True)]
X0, S = 470, 0.66                             # where he sits, his scale (seated: head about 1.35 m off the ground)
NECK = 1046 - 560 * S                         # his neck, so his coat's hem sits on the seat
BENCH_P = (800, 1040)                        # the talking pigeon's feet, on the seat
PALS = [   # (body, wing and tail, head, neck sheen 1, sheen 2): blue-bar, dark, pale, red-chequer, smoky
    ((150, 158, 172), (110, 118, 134), (96, 104, 124), (80, 140, 110), (130, 90, 140)),
    ((92, 94, 108), (62, 64, 78), (52, 54, 66), (70, 120, 96), (110, 80, 120)),
    ((206, 208, 214), (168, 172, 182), (150, 154, 166), (120, 170, 140), (160, 130, 170)),
    ((168, 134, 110), (130, 98, 78), (110, 84, 70), (100, 140, 110), (140, 100, 120)),
    ((126, 132, 128), (90, 98, 94), (76, 82, 84), (80, 130, 100), (120, 90, 130))]
FLOCK = [(150, 1330, 0.8, 1, 0.1, 0), (420, 1395, 1.15, -1, 0.5, 1), (690, 1318, 0.9, 1, 0.8, 2), (900, 1420, 0.75, -1, 0.3, 0),
         (265, 1480, 1.2, 1, 0.65, 3), (630, 1488, 0.95, -1, 0.2, 2), (85, 1455, 0.7, 1, 0.9, 4)]    # x, y, size, facing, seed, palette
TOSS = filmkit.Beats([(0.0, 'set-up', (150, 330)), (0.45, 'wind-up', (110, 230)), (0.62, 'contact', (300, 250), 'fast'),
                      (1.4, 'settle', (150, 330), 'slow')])       # one throw of seed (his right hand), repeated
# ====================================================================================================================
BLACK_AT = DUR


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def cam_for(t):
    if shot_of(t) == 'glance':
        return B.Cam(2.5, X0 + 16, NECK - 158 * S + 58)      # the original's hard cut in on his face
    return B.Cam(1.0, 500, 1000)                              # the original's wide


def ctx(img, cam):
    X = Ctx(ImageDraw.Draw(img), SCam(cam.cx, cam.cy, cam.z, B.SS), ol=3)
    return X


# ------------------------------------------------------------------------------------------------- the park
def park(img, cam, t):
    X = ctx(img, cam)
    X.rect(-900, -900, 2000, 830, (136, 184, 208), line=False)                     # sky: one flat colour
    X.ell(880, 290, 92, 92, (240, 212, 104))                                       # sun: a flat disc
    for cx, cy, k in [(240, 330, 1.0), (650, 470, 0.7)]:
        ox = cx + 12 * math.sin(t * 0.25 + cx)
        blob(X, [(ox - 70 * k, cy + 10 * k, 55 * k, 40 * k, 0.2), (ox, cy - 15 * k, 72 * k, 56 * k, -0.1),
                 (ox + 84 * k, cy + 8 * k, 58 * k, 42 * k, 0.15), (ox + 20 * k, cy + 28 * k, 90 * k, 34 * k, 0.0)],
             (244, 240, 230), ol=3)
    X.rect(-900, 730, 2000, 815, (80, 120, 68), line=False)                       # far hedge
    for x, y, r in [(120, 560, 190), (390, 600, 150), (700, 520, 200), (960, 600, 160), (-30, 640, 150)]:
        rnd = random.Random(int(x) + 11)
        lean = rnd.uniform(-14, 14)
        X.poly([(x - 18, 820), (x + lean - 11, y + 10), (x + lean + 13, y + 10), (x + 20, 820)], (92, 62, 44))
        sway = 4 * math.sin(t * 0.9 + x)
        blob(X, [(x + sway + rnd.uniform(-0.55, 0.55) * r + lean, y - 30 + rnd.uniform(-0.45, 0.35) * r,
                  r * rnd.uniform(0.5, 0.85), r * rnd.uniform(0.45, 0.75), rnd.uniform(-0.5, 0.5)) for _ in range(4)],
             (60, 106, 58), ol=3)
    X.rect(-900, 800, 2000, 2800, (118, 158, 82), line=False)                     # lawn, a few tufts
    rnd = random.Random(5)
    for _ in range(46):
        tx, ty = rnd.uniform(-450, 1500), rnd.uniform(830, 1170)
        for dx in (-9, 0, 9):
            X.seg((tx + dx, ty), (tx + dx * 1.6, ty - rnd.uniform(14, 26)), 4, (84, 124, 62))
    X.poly(rough([(-900, 1200), (2000, 1200), (2000, 2800), (-900, 2800)], 8, 3), (200, 176, 136))   # gravel path
    rnd = random.Random(3)
    for _ in range(80):
        X.ell(rnd.uniform(-500, 1600), rnd.uniform(1230, 1700), 6, 3, (176, 154, 116), line=False)
    # the bench: rough planks, iron legs
    wood, dark = (150, 96, 54), (110, 70, 40)
    for k, y in enumerate((820, 880, 940)):
        X.poly(rough([(220, y), (900, y), (900, y + 44), (220, y + 44)], 4, 20 + k), wood)
    X.poly(rough([(220, 800), (252, 800), (252, 1130), (220, 1130)], 3, 30), dark)
    X.poly(rough([(868, 800), (900, 800), (900, 1130), (868, 1130)], 3, 31), dark)
    X.poly(rough([(210, 1020), (910, 1020), (910, 1066), (210, 1066)], 4, 32), wood)
    X.poly([(240, 1066), (270, 1066), (270, 1300), (240, 1300)], (70, 70, 80))
    X.poly([(850, 1066), (880, 1066), (880, 1300), (850, 1300)], (70, 70, 80))
    X.ell(560, 1312, 340, 16, (172, 150, 112), line=False)


# ------------------------------------------------------------------------------------------------- pigeons
def pigeon(X, x, y, s, face, pal=0, peck=0.0, beak=0.0, wing=0.0, legs=True, lid=0.45, turn=0.0, flap=None, up=0.0, shine=False):
    """A rock dove side-on, Satire style: a plump lumpy body with one outline, a darker head, the green-purple neck sheen,
    two dark bars on the wing, a white cere on a small dark beak, an orange eye, pink feet. (x, y): its feet.
    peck dips the head; up (0-1) tips the head right back to look up; beak (0-1) opens it; turn (0-1) swings the head
    round to stare at us; flap (radians) spreads the wings."""
    body, wingc, head, sh1, sh2 = PALS[pal]
    f = face
    P = lambda dx, dy: (x + f * dx * s, y + dy * s)
    if legs:
        for lx in (-12, 10):
            X.seg(P(lx, -40), P(lx + 2, 0), 7 * s, (214, 112, 112))
            for tx in (-8, 6, 18):
                X.seg(P(lx + 2, 0), P(lx + 2 + tx, 3), 5 * s, (214, 112, 112))
    X.poly([P(-58, -90), P(-124, -84), P(-120, -54), P(-56, -50)], wingc)                 # tail
    X.poly([P(-118, -82), P(-124, -84), P(-120, -54), P(-112, -56)], (40, 42, 50), line=False)   # its dark tip
    if flap is not None:                                                                # far wing, behind
        a = math.sin(flap)
        X.poly([P(-10, -90), P(-60, -90 - 120 * a), P(-10, -100 - 140 * a), P(30, -96)], wingc)
    blob(X, [(*P(0, -74), 72 * s, 46 * s, 0.0), (*P(34, -70), 42 * s, 34 * s, 0.3)], body, ol=3)     # plump body, puffed breast
    # the neck rises to the head; tipped back, it stretches up and the head turns its beak to the sky
    lift = 46 * peck - 40 * up
    hx, hy = P(62 - 14 * up, -112 + lift)
    nx0, ny0 = P(40, -86)
    X.poly([(nx0 - 26 * s, ny0), (nx0 + 26 * s, ny0), (hx + 22 * s, hy + 8 * s), (hx - 22 * s, hy + 8 * s)], head)
    X.poly([(nx0 - 24 * s, ny0 - 2 * s), (nx0 + 24 * s, ny0 - 2 * s), ((nx0 + hx) / 2 + 20 * s, (ny0 + hy) / 2),
            ((nx0 + hx) / 2 - 20 * s, (ny0 + hy) / 2)], sh1, line=False)                # the neck's sheen: green...
    X.poly([((nx0 + hx) / 2 - 20 * s, (ny0 + hy) / 2), ((nx0 + hx) / 2 + 20 * s, (ny0 + hy) / 2),
            (hx + 18 * s, hy + 12 * s), (hx - 18 * s, hy + 12 * s)], sh2, line=False)     # ...and purple
    X.ell(hx, hy, 27 * s, 25 * s, head)
    if turn < 0.5:                                  # the beak: forward, or tipped up to the sky; opens when it speaks
        th = math.radians(70 * up)
        d, n = (f * math.cos(th), -math.sin(th)), (f * math.sin(th), math.cos(th))
        Q = lambda u, v: (hx + (d[0] * u + n[0] * v) * s, hy + (d[1] * u + n[1] * v) * s)
        op = beak
        if op > 0:
            X.poly([Q(18, 0), Q(46, -2 - 6 * op), Q(42, 6 + 18 * op)], (226, 116, 128), line=False)   # inside the mouth
        X.poly([Q(18, -9), Q(50, -2 - 6 * op), Q(18, 1)], (64, 54, 58))                  # upper
        X.poly([Q(18, 2), Q(44, 6 + 18 * op), Q(18, 9)], (64, 54, 58))                   # lower, drops as it opens
        X.ell(*Q(22, -7), 7 * s, 5 * s, (236, 236, 230))                                  # the white cere
    ex = hx + f * 7 * s * (1 - turn)
    for dx in ((0,) if turn < 0.5 else (-11, 11)):          # one eye in profile, two staring straight at us
        X.ell(ex + dx * s, hy - 7 * s, 10 * s, 10 * s, (242, 140, 40))
        X.ell(ex + dx * s, hy - 7 * s, 4.5 * s, 4.5 * s, INK, line=False)
        if shine:                                                                   # a catchlight: friendly, not shifty
            X.ell(ex + dx * s - 2.5 * s, hy - 10 * s, 1.8 * s, 1.8 * s, (255, 255, 255), line=False)
        if lid > 0:
            X.poly([(ex + dx * s - 11 * s, hy - 18 * s), (ex + dx * s + 11 * s, hy - 18 * s),
                    (ex + dx * s + 11 * s, hy - 18 * s + 20 * lid * s), (ex + dx * s - 11 * s, hy - 18 * s + 20 * lid * s)], head, line=False)
            X.seg((ex + dx * s - 11 * s, hy - 18 * s + 20 * lid * s), (ex + dx * s + 11 * s, hy - 18 * s + 20 * lid * s), 3)
    if turn >= 0.5:
        X.poly([(hx - 7 * s, hy + 4 * s), (hx + 7 * s, hy + 4 * s), (hx, hy + 18 * s)], (60, 52, 56))
    if flap is not None:
        a = math.sin(flap + 0.6)
        X.poly([P(-10, -80), P(-40, -70 - 130 * a), P(10, -86 - 150 * a), P(40, -84)], body)
    else:
        X.rell(*P(-10, -78), 52 * s, 27 * s, f * (-0.15 + wing), wingc)
        for k in (0, 1):                                                                # the two dark bars
            X.seg(P(-34 + 16 * k, -64), P(-8 + 16 * k, -76), 7 * s, (50, 52, 62))
    return hx, hy


def pecks(t, seed, rate=1.2):
    ph = (t * rate + seed) % 1.0
    return (1 - abs(ph * 4 - 1)) if ph < 0.5 else 0.0


def flock(X, t):
    """The pigeons on the ground, just being pigeons: pottering about, bobbing, pecking at the seed. Friendly open eyes."""
    for i, (x, y, s, f, sd, pal) in enumerate(FLOCK):
        wx = x + 26 * s * math.sin(t * 0.45 + i * 1.7)                              # a slow potter back and forth
        X.ell(wx, y + 6 * s, 66 * s, 11 * s, (172, 150, 112), line=False)
        pigeon(X, wx, y, s, f, pal, peck=pecks(t, sd), lid=0.0, shine=True)


def bench_pigeon(X, t):
    """The one on the bench: still, side-on, looking at him; then it flies off, up and away over the trees."""
    x, y = BENCH_P
    u = t - FLY
    if u < 0:
        bob = 0.1 * max(0.0, math.sin(t * 2.2))
        pigeon(X, x, y, 1.0, -1, 0, peck=bob, lid=0.5)
        return x, y
    fx, fy = x + 330 * u + 30 * u * u, y - 260 * u - 60 * u * u
    pigeon(X, fx, fy, 1.0 - 0.12 * u, 1, 0, legs=u < 0.15, flap=u * 24)
    return fx, fy


def _handfuls():
    """Every grain he throws: (release time, start, landing spot, flight time, size, colour, spin). Loose and uneven."""
    out, rnd = [], random.Random(17)
    k = 0
    while k * 1.4 + 0.62 < T2:
        r = k * 1.4 + 0.62
        hx, hy = TOSS.at(0.62)
        h = (X0 + hx * S, NECK + hy * S)
        for _ in range(rnd.randint(7, 11)):
            land = (rnd.uniform(560, 1010), rnd.uniform(1235, 1470))
            out.append((r + rnd.uniform(0, 0.06), h, land, rnd.uniform(0.45, 0.8), rnd.uniform(3.0, 5.5),
                        rnd.choice([(232, 200, 90), (214, 176, 96), (196, 150, 82), (240, 220, 150)]), rnd.uniform(0, 3)))
        k += 1
    return out


GRAINS = _handfuls()


def seeds(X, t):
    """The thrown seed: each grain arcs out of his hand under gravity, lands on the path and stays there."""
    g = 2400.0
    for r, h, land, d, sz, col, ph in GRAINS:
        u = t - r
        if u < 0:
            continue
        if u >= d:
            X.ell(land[0], land[1], sz * 1.2, sz * 0.7, col, line=False)              # lying on the ground
            continue
        vy = (land[1] - h[1] - g * d * d / 2) / d
        x = h[0] + (land[0] - h[0]) * u / d
        y = h[1] + vy * u + g * u * u / 2
        X.ell(x, y, sz * (0.8 + 0.4 * abs(math.sin(u * 14 + ph))), sz, col, line=False)    # tumbling as it flies


# ------------------------------------------------------------------------------------------------- the man
def man_state(t):
    sp = dict(MAN)
    rig = F.Rig(sp)
    stunned = t >= T2
    arms = rig.pose('sides')
    arms['L'] = rig.arm('L', (-150, 360), 'grip', 'depth', 0.3, strict=False)                # the seed bag on his knee
    if stunned:
        arms['R'] = rig.arm('R', (175, 380), 'palm', 'depth', 0.3, strict=False)   # the arm drops, and stays
    else:
        arms['R'] = rig.arm('R', TOSS.at(t % 1.4), 'palm', 'out', strict=False)
    sp['arms'] = arms
    look = 0.25 if t < T1 - 1.0 else (0.25 + 0.75 * min(1.0, (t - (T1 - 0.8)) / 0.3) if t < T2 else 0.9)
    sp['look'] = look
    sp['tilt'] = 0.04 * math.sin(t * 1.3) if not stunned else head_turn(t)   # stunned: still, turning only to look
    sp['mouth'] = 'set'
    if stunned:                                   # his own brows hidden: the shock draws raised grey ones
        sp['brows'], sp['brow_c'] = 'wow', MAN['skin']
        if SHOCKS[SHOCK - 1]['mouth']:
            sp['mouth'] = 'hidden'                # one mouth only: the shock draws its own, in the same place
    sp['blink'] = ((t % 3.4) < 0.12 and not stunned) or stunned       # stunned: his own eyes are drawn wide over the top
    return sp


DARTS = [(1.8, 1), (2.3, 6), (2.8, 3), (3.3, 4), (3.8, 2), (4.3, 5), (4.7, 0)]   # (seconds after take-off, which pigeon)


def head_turn(t):
    """Stunned, his head holds dead still, then snaps to each new pigeon a frame after his eyes do: paranoid, not woozy."""
    gx, gy = gaze(t - 1.0 / FPS)
    return -0.02 - 0.10 * max(-1.0, min(1.0, (gx - X0) / 450))


def gaze(t):
    """The spot his shocked eyes are on: the bench pigeon, then it as it flies, then (the sting) each pigeon on the
    ground in turn as they carry on pecking, as if any of them might speak next. Each move is a quick two-frame flick."""
    u = t - FLY
    if u < 0:
        return BENCH_P[0], BENCH_P[1] - 100
    x, y = BENCH_P[0] + 330 * u + 30 * u * u, BENCH_P[1] - 100 - 260 * u - 60 * u * u
    if u < DARTS[0][0]:
        return min(x, 1300), max(y, 200)
    prev = (min(BENCH_P[0] + 330 * DARTS[0][0] + 30 * DARTS[0][0] ** 2, 1300), 200)
    for k, (at, i) in enumerate(DARTS):
        nxt = DARTS[k + 1][0] if k + 1 < len(DARTS) else 1e9
        if at <= u < nxt:
            tgt = (FLOCK[i][0], FLOCK[i][1] - 60 * FLOCK[i][2])
            f = min(1.0, (u - at) / (2.0 / FPS))
            return prev[0] + (tgt[0] - prev[0]) * f, prev[1] + (tgt[1] - prev[1]) * f
        prev = (FLOCK[i][0], FLOCK[i][1] - 60 * FLOCK[i][2])
    return prev


def man(img, cam, t):
    sp = man_state(t)
    stunned = t >= T2
    X = ctx(img, cam)
    B.person(img, cam, X0, NECK, S, sp, t)
    for dx in (-1, 1):                     # seated, front on: thighs come at us over the coat's hem, knees, shins, shoes
        limb(X, (X0 + dx * 64, 1092), (X0 + dx * 72, 1262), 58, MAN['trousers'])
        X.ell(X0 + dx * 76, 1276, 48, 22, (40, 32, 30))
        limb(X, (X0 + dx * 34, 1018), (X0 + dx * 62, 1084), 82, MAN['trousers'])
        X.ell(X0 + dx * 63, 1088, 44, 34, MAN['trousers'])                          # the knee, nearest us
    L = B.Local(cam, X0, NECK, S)
    import peepee
    p = B.Pen(img, peepee.Rot(L, sp['tilt'], pivot=(0, -60)))                      # his head, as tilted
    hx, hy, hw, hh = 0, -150, MAN['hw'], MAN['hh']
    lv = SHOCKS[SHOCK - 1]
    gx, gy = gaze(t)                                                                # where his pupils point
    ew = (X0, NECK - 158 * S)
    d = math.hypot(gx - ew[0], gy - ew[1]) or 1.0
    ox, oy = 4 + (lv['eye'][0] - lv['pupil'] - 3) * (gx - ew[0]) / d, (lv['eye'][1] - lv['pupil'] - 3) * (gy - ew[1]) / d
    if stunned:                     # shock, at the chosen level: eyes, pupils, brows, forehead, mouth, cap, sweat, tremble
        for sgn in (-1, 1):
            ex, ey = -4 + sgn * 30, hy - 8
            p.ell(ex, ey, lv['eye'][0], lv['eye'][1], (252, 252, 248), INK, 2.4)
            p.ell(ex + ox, ey + oy, lv['pupil'], lv['pupil'], INK, None)
            other = lv.get('one_brow') and sgn == -1                                 # puzzled: one brow stays down
            by = ey - lv['eye'][1] - 7 - (0 if other else lv['brow'])
            arch = 1 if other else lv['arch']
            pts = [(ex + u, by + 6 - arch * math.cos(u / 22 * math.pi / 2) + (0 if other else 4 * sgn * u / 22))
                   for u in range(-22, 23, 4)]                                       # a rounded arch, inner end lifted
            p.line(pts, INK, 8.0)
            p.line(pts, (214, 212, 210), 5.0)
        for k in range(lv['lines']):
            y = hy - 8 - lv['eye'][1] - 7 - lv['brow'] - 16 - 9 * k
            p.line([(-36, y + 4), (-4, y), (30, y + 4)], B.dk(MAN['skin'], 0.7), 2.0)
        if lv['mouth']:
            p.ell(-4, hy + 60 + lv['mouth'][1] * 0.3, lv['mouth'][0], lv['mouth'][1], (60, 24, 30), INK, 2.2)
        for k in range(lv['sweat']):                                                 # sweat drops at his temple
            sx, sy = hw * 0.78 + 4 * k, hy - 30 + 34 * k
            p.poly([(sx, sy - 16), (sx + 8, sy), (sx, sy + 7), (sx - 8, sy)], (170, 214, 236), INK, 2.0)
        if lv['tremble']:                                                            # tremble marks beside his head
            for sgn in (-1, 1):
                for k in range(2):
                    x = sgn * (hw + 22 + 14 * k)
                    p.line([(x, hy - 24 + 6 * k), (x + sgn * 6, hy - 6), (x, hy + 12 - 6 * k)], INK, 2.6)
    up = min(1.0, (t - T2) / 0.12) if stunned else 0.0                               # the cap jumps, then settles a little
    pop = lv['pop'] * (1.3 * up - 0.3 * max(0.0, min(1.0, (t - T2 - 0.12) / 0.3))) if stunned else 0.0
    hy -= pop
    # the flat cap: a soft crown and a short peak across the brow
    p.poly([(hx - hw - 6, hy - hh * 0.40), (hx - hw * 0.9, hy - hh * 0.85), (hx - hw * 0.2, hy - hh * 1.08), (hx + hw * 0.7, hy - hh * 1.0),
            (hx + hw + 8, hy - hh * 0.55), (hx + hw + 6, hy - hh * 0.40)], CAP, INK, 2.6)
    p.poly([(hx - hw * 0.8, hy - hh * 0.46), (hx + hw * 0.9, hy - hh * 0.48), (hx + hw * 0.75, hy - hh * 0.30), (hx - hw * 0.7, hy - hh * 0.28)],
           CAP_D, INK, 2.4)
    hxw, hyw = L.P(0, -150)
    hxw, hyw = (hxw / B.SS - cam.cx / 1) if False else hxw, hyw
    bag = (X0 - 150 * S, NECK + 360 * S)                                            # the paper bag over his left hand
    X.poly(rough([(bag[0] - 30, bag[1] - 44), (bag[0] + 30, bag[1] - 44), (bag[0] + 27, bag[1] + 24), (bag[0] - 27, bag[1] + 24)], 4, 9),
           (196, 166, 112))
    eye = (X0 + 26 * S, NECK - 158 * S)
    if t < T1 - 1.0:
        filmkit.eyeline('the man', t, eye, (sp['look'], 0.0), (700, 1330))
    elif t < T1 - 0.5:
        pass                                                                        # his eyes travel to the pigeon
    elif t < FLY:
        filmkit.eyeline('the man', t, eye, (sp['look'], 0.0), BENCH_P)


# ------------------------------------------------------------------------------------------------- shot 3: his view
def pov_cam(t):
    """The original's angle, straight down at it through his eyes, slowly pushing in towards its face."""
    u = max(0.0, min(1.0, (t - T1) / (T2 - T1)))
    u = u * u * (3 - 2 * u)
    return B.Cam(1.35 + 0.45 * u, 540, 900 + 90 * u)


def pov_pigeon(X, t):
    """The bench pigeon from above: tail away from him, wings folded with their two bars, the neck's sheen; its head
    tips right back to stare up into the lens, and its beak opens as it speaks."""
    body, wingc, head, sh1, sh2 = PALS[0]
    cx = 540 + 6 * math.sin(t * 1.3)
    up = max(0.0, min(1.0, (t - (T1 + 0.15)) / 0.3))
    for fx in (-1, 1):                                  # feet under its breast: legs hidden, toes peeking out either side
        for ex, ey in ((124, 1012), (150, 1002), (166, 970)):                       # three thick toes, pointing forward
            X.seg((cx + fx * 108, 930), (cx + fx * ex, ey), 20, (214, 112, 112))
            X.ell(cx + fx * ex, ey, 6, 6, (70, 52, 56), line=False)              # claws
        X.ell(cx + fx * 110, 935, 30, 26, (214, 112, 112))                        # the foot, under its breast
    X.poly(rough([(cx - 70, 560), (cx - 125, 320), (cx, 290), (cx + 125, 320), (cx + 70, 560)], 5, 71), wingc)   # tail
    X.poly([(cx - 125, 320), (cx, 290), (cx + 125, 320), (cx + 118, 352), (cx, 324), (cx - 118, 352)], (40, 42, 50))
    blob(X, [(cx, 740, 195, 270, 0.0), (cx, 860, 170, 150, 0.0)], body, ol=3)
    for sg in (-1, 1):                                                              # folded wings, two dark bars each
        X.rell(cx + sg * 118, 690, 82, 240, -sg * 0.14, wingc)
        for k in (0, 1):
            X.seg((cx + sg * 160, 640 + 70 * k), (cx + sg * 84, 660 + 70 * k), 13, (50, 52, 62))
    X.ell(cx, 940, 128, 74, sh1)                                                    # the neck: green over purple
    X.ell(cx, 968, 112, 46, sh2, line=False)
    hx, hy = cx, 1010 + 60 * (1 - up)
    X.ell(hx, hy, 118, 110, head)
    blink = (t % 2.6) < 0.1 and not (up >= 1 and t < T2)
    for ex in (-62, 62):                                                            # orange eyes, dead on the lens
        X.ell(hx + ex, hy - 18, 30, 30, (242, 140, 40))
        if blink:
            X.seg((hx + ex - 26, hy - 18), (hx + ex + 26, hy - 18), 7)
        else:
            r = 12 + 4 * up
            X.ell(hx + ex, hy - 18 + 8 * (1 - up), r, r, INK, line=False)
    talking = any(a <= t - SAY <= b for a, b in STRETCHES)
    beak = (0.55 + 0.45 * math.sin((t - SAY) * 17)) if talking else 0.0
    X.ell(hx, hy + 26, 26, 14, (236, 236, 230))                                     # the white cere
    if beak > 0:                                                                    # beak at us, foreshortened: it opens
        X.ell(hx, hy + 62 + 8 * beak, 30, 12 + 18 * beak, (196, 70, 86))
        X.poly([(hx - 24, hy + 36), (hx + 24, hy + 36), (hx, hy + 60 - 4 * beak)], (64, 54, 58))
        X.poly([(hx - 22, hy + 66 + 24 * beak), (hx + 22, hy + 66 + 24 * beak), (hx, hy + 88 + 26 * beak)], (64, 54, 58))
    else:
        X.poly([(hx - 24, hy + 36), (hx + 24, hy + 36), (hx, hy + 84)], (64, 54, 58))
    return up


def talk(img, t):
    cam = pov_cam(t)
    X = ctx(img, cam)
    X.rect(-200, -200, 1300, 2100, (150, 96, 54), line=False)                       # the bench seat from above
    for k, y in enumerate(range(-60, 2000, 330)):
        X.poly(rough([(-200, y), (1300, y), (1300, y + 22), (-200, y + 22)], 4, 80 + k), (70, 44, 28), line=False)
        X.seg((60, y + 140), (500, y + 152), 3, (124, 78, 44))
        X.seg((600, y + 230), (1000, y + 220), 3, (124, 78, 44))
    X.ell(546, 840, 250, 330, (118, 74, 42), line=False)                             # its shadow
    pov_pigeon(X, t)
    X.poly(rough([(-200, 1540), (330, 1560), (350, 2100), (-200, 2100)], 8, 91), MAN['jacket'])    # his coat, his knee
    X.poly(rough([(760, 1590), (1300, 1570), (1300, 2100), (740, 2100)], 8, 92), MAN['trousers'])


# ------------------------------------------------------------------------------------------------- frames
def picture(t):
    """The frame WITHOUT the caption or title (they go on last)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    img = B.canvas()
    if shot_of(t) == 'talk':
        talk(img, t)
        return img
    cam = cam_for(t)
    park(img, cam, t)
    X = ctx(img, cam)
    man(img, cam, t)
    bench_pigeon(X, t)
    seeds(X, t)
    flock(X, t)
    return img


def caption_at(t):
    return LINE if SAY <= t < T2 - 0.2 else None


def overlay(img, t):
    if t < BLACK_AT:
        c = caption_at(t)
        if c:
            PP.caption(img, c)
        if t < 2.0:
            B.title_lines(img, (' '.join(TITLE),), cap=116, top=310, alpha=1.0 if t < 1.75 else max(0.0, 1.0 - (t - 1.75) / 0.25))
    return img


def frame_image(t):
    return overlay(picture(t), t)


# ------------------------------------------------------------------------------------------------- sound
def _voice():
    v = load(os.path.join(HERE, 'audio', VOICE + '.m4a'))[int(VOICE_FROM * SR):int(VOICE_TO * SR)]
    return v * VOICE_GAIN


STRETCHES = MA.pauses(_voice(), 0.12)


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice = np.zeros(n)
    v = _voice()
    s = int(SAY * SR)
    voice[s:s + len(v)] = v[:max(0, n - s)]
    b = load(BIRDS)
    birds = np.resize(b, n)
    tt = np.arange(n) / SR
    lo = 0.08                                   # never dead silence: a faint bed of birdsong stays under the line
    env = np.where(tt < T1, 1.0, np.where(tt < T1 + 1.0, 1.0 - (1 - lo) * (tt - T1), lo))
    up = np.clip((tt - (T2 - 0.25)) / 0.8, 0.0, 1.0)                                  # eased back up across the cut
    env = np.where(tt >= T2 - 0.25, lo + (1 - lo) * up * up * (3 - 2 * up), env)
    rest = birds * env
    w = load(os.path.join(HERE, 'audio', 'park-takeoff.mp3')) * 1.33               # Sam's wing-flap clip: its first
    a = int((FLY - 0.3) * SR)                                                       # flap lands as it leaves the bench
    rest[a:a + len(w)] += w[:max(0, n - a)]
    mix = voice + rest
    end = int(BLACK_AT * SR)
    g = 10 ** ((-14.0 - MA.lufs(mix[:end])) / 20)
    mix, voice, rest = M.limiter(mix * g, -2.6), voice * g, rest * g
    k = int(0.005 * SR)
    mix[end - k:end] *= np.linspace(1, 0, k)
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


# ------------------------------------------------------------------------------------------------- checks
def checks():
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    windows = [(SAY + a, SAY + b) for a, b in STRETCHES]
    beak = [(SAY + a, SAY + b, 'open') for a, b in STRETCHES]
    _, voice, rest = soundtrack(stems=True)
    faults = E.check_mouths(beak, windows) + filmkit.voice_balance(voice, rest, SR, windows)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


def talk_alone(img, t):
    pov_pigeon(ctx(img, pov_cam(t)), t)


def audits():
    def alone(fn):
        def draw(t):
            lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
            fn(lay, t)
            return lay
        return draw
    frames = lambda a, b: [i / FPS for i in range(int(a * FPS), int(b * FPS))]
    actors = {'the man [wide]': (frames(0, T1 - 1.0), alone(lambda im, t: man(im, cam_for(t), t))),
              'the man [glance]': (frames(T1 - 1.0, T1), alone(lambda im, t: man(im, cam_for(t), t))),
              'the man [end]': (frames(T2, DUR), alone(lambda im, t: man(im, cam_for(t), t))),
              'the talking pigeon': (frames(T1, T2), alone(lambda im, t: talk_alone(im, t))),
              'the bench pigeon': (frames(0, T1 - 1.0) + frames(T2, DUR),
                                   alone(lambda im, t: bench_pigeon(ctx(im, cam_for(t)), t)))}
    allow = [('the bench pigeon', FLY - 0.1, DUR, 'flies away'), ('the bench pigeon', T1 - 1.1, T2 + 0.1, 'the cut')]
    filmkit.EYES.clear()
    faults = filmkit.silhouette_audit(actors, fps=FPS, allow=allow, still_ok=('the bench pigeon',))
    faults += filmkit.check_eyelines()
    rig = F.Rig(dict(MAN))

    def arm_rule(target):
        el, wr = rig.arm('R', target, 'palm', 'out', strict=False)[:2]
        return filmkit.check_joints({'sh': rig.shoulder('R'), 'el': el, 'wr': wr, 'head': (0, -150)},
                                    [('angle', 'sh', 'el', 'wr', 25, 180), ('apart', 'wr', 'head', 90)])
    return faults + TOSS.audit(arm_rule, label='seed toss')


def cast_sheet(out):
    img = Image.new('RGBA', (1080, 1080), (230, 226, 220, 255))
    man(img, B.Cam(1.0, 740, 1330), T2 + 0.6)
    X = ctx(img, B.Cam(1.0, 540, 900))
    for i in range(len(PALS)):
        pigeon(X, 690 + 230 * (i % 2), 230 + 220 * (i // 2), 0.9, -1, i)
    pigeon(X, 920, 670, 0.9, -1, 0, beak=1.0, lid=0.0, up=1.0)
    img.convert('RGB').save(out)


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        B.SS = 1
        cast_sheet(a[1])
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'shocks':             # his six levels of shock side by side, numbered, to choose from
        global SHOCK
        from PIL import ImageDraw, ImageFont
        B.SS = 1
        out = Image.new('RGB', (3 * 540, 2 * 640), (255, 255, 255))
        for i in range(6):
            SHOCK = i + 1
            img = B.canvas()
            cam = B.Cam(2.2, X0 + 16, NECK - 158 * S + 40)
            park(img, cam, T2 + 1.0)
            man(img, cam, T2 + 1.0)
            tile = img.convert('RGB').crop((0, 380, 1080, 1580)).resize((540, 600))
            out.paste(tile, ((i % 3) * 540, (i // 3) * 640 + 40))
            ImageDraw.Draw(out).text(((i % 3) * 540 + 16, (i // 3) * 640 + 2), SHOCKS[i]['name'], fill=(0, 0, 0),
                                     font=ImageFont.load_default(size=34))
        out.save(a[1], quality=88)
    elif a[0] == 'check':
        B.SS = 1
        checks()
        f = audits()
        print('\n'.join(['AUDIT: ' + x for x in f]) or 'audit: clean')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else ())


F.guard(B)

if __name__ == '__main__':
    main()
