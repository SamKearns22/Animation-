#!/usr/bin/env python3
"""Andrew the Hutt: a silent satire short for TikTok (1080 x 1920, 12 fps, about 19 s).

A serious PR man in a posh drawing room asks Andrew whether he really wants to sue the police. The camera swings
round 180 degrees: Andrew, remodelled as a vast drooling slug-king on a dais (the throne-room tableau from Return of
the Jedi, evoked, never copied), with a line of fashion models chained by the neck where the princess sat. He
answers in Huttese. Hard cut back to the PR man, who has seen this coming.

The series' look (burnham.py people, circle hands, figure.py arms, mouths.py lip sync, the standard captions).
The room is one strip of three walls, so the swing is one camera turning, and every shot of each wall draws the
same set. No sound yet: the words are timed at a natural pace and a silent track keeps players happy.

    python3 source/hutt.py stills OUT.jpg             the key frames on one sheet (about 30 s)
    python3 source/hutt.py final OUT.mp4 [--scale 0.5] [--secs 3]
    python3 source/preflight.py hutt OUT_DIR          the series' checks and contact sheet
"""
import math
import os
import subprocess
import sys
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import quick as Q            # noqa: E402  (circle hands, captions, mossad's tilted heads and brows)
import figure as F           # noqa: E402
import mouths                # noqa: E402
from ed import INK, curve, oval, soft   # noqa: E402

FPS = 12
SAFE = (60, 310, 900, 1500)
FY = 1420                                     # the floor line of the room (every wall)
U0 = {'A': 0, 'C': 2300, 'B': 4600}           # the three walls along the camera's turn (A behind the PR man)
SPAN = (-610, 1690)                           # each wall's extent in its own coordinates

# ------------------------------------------------------------------------------------------------- the script
PAN0, PAN1 = 6.7, 7.9                         # the 180-degree swing
CUT_BACK = 15.7                               # hard cut back to the PR man
BLACK_AT = 19.3
DUR = BLACK_AT + 0.35
SCRIPT = [  # who, words ('|' splits the caption at a pause), start, length (no recordings yet: a natural pace)
    ('PR', "Andrew, you're already | the most hated man in the country.", 0.2, 2.9),
    ('PR', 'Are you absolutely sure | you want to sue the police?', 3.4, 2.9),
    ('AJ', 'Mee shall ruin those clowns, | che da they did tah je um', 8.7, 3.5),
    ('AJ', 'myo good best pateesa Epstein. Ho ho ho!', 12.3, 3.05),
    ('PR', "Yes, I was afraid you'd say that.", 16.65, 2.0),
]
LAUGH = (14.0, 15.45)
TUG = 9.3                                    # "ruin": he yanks the chain
SHOTS = [('PR man', 0.0, PAN0), ('swing', PAN0, PAN1), ('Andrew', PAN1, CUT_BACK), ('PR man again', CUT_BACK, BLACK_AT)]

LINES = []
for who, cap, st, d in SCRIPT:
    text = cap.replace(' | ', ' ')
    stretches = [(0.0, d)] if who != 'AJ' or 'Ho' not in text else [(0.0, LAUGH[0] - st - 0.05), (LAUGH[0] - st, d)]
    trk = [(a + st, b + st, s) for a, b, s in mouths.track(text, stretches)]
    pieces, words, k = cap.split(' | '), len(text.split()), 0
    for j, pc in enumerate(pieces):                       # each caption piece is on screen for its share of the words
        n = len(pc.split())
        a, b = st + d * k / words, st + d * (k + n) / words
        k += n
        LINES.append(dict(who=who, text=pc, start=a, end=b, track=trk if j == 0 else []))
TRACK = {w: [x for ln in LINES if ln['who'] == w for x in ln['track']] for w in ('PR', 'AJ')}


def caption_at(t):
    for i, ln in enumerate(LINES):
        nxt = LINES[i + 1]['start'] - 0.05 if i + 1 < len(LINES) else 1e9
        if ln['start'] - 0.05 <= t < min(ln['end'] + 0.25, nxt):
            if PAN0 <= t < PAN1:
                return None                   # no caption across the swing
            return ln['text']
    return None


def spring(u, amp=1.0, k=5.0, w=13.0):
    """A jolt that rings and dies away (u = seconds since the jolt)."""
    return 0.0 if u < 0 else amp * math.exp(-k * u) * math.sin(w * u)


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


# --------------------------------------------------------------------------------------------- the camera
def camera(t):
    """One camera on the spot, turning from the PR man (wall A) to Andrew (wall B)."""
    a = B.Cam(1.6, 540, 658)                                  # shot 1: the PR man, waist up
    if t < PAN0:
        return B.Cam(1.6 + 0.06 * t / PAN0, 540, 658)          # a slow creep in while he asks
    if t < PAN1:
        u = ease((t - PAN0) / (PAN1 - PAN0))
        z0, z1 = 1.66, 1.0
        return B.Cam(z0 + (z1 - z0) * u, a.cx + (U0['B'] - U0['A']) * u, 658 + (960 - 658) * u)
    if t < CUT_BACK:
        k = ease((t - PAN1) / (CUT_BACK - PAN1))
        return B.Cam(1.0 + 0.05 * k, U0['B'] + 540, 960 - 50 * k)   # a slow push towards his face
    k = ease((t - CUT_BACK) / (BLACK_AT - CUT_BACK))
    return B.Cam(1.66 + 0.1 * k, 540, 658 - 12 * k)


def wall_cam(cam, w):
    return B.Cam(cam.z, cam.cx - U0[w], cam.cy)


# -------------------------------------------------------------------------------------------- the room
GREEN, GREEN_D, GREEN_L = (52, 88, 72), (38, 66, 54), (70, 112, 92)
CREAM, CREAM_D = (236, 226, 202), (206, 192, 164)
CRIMSON, CRIMSON_D = (150, 28, 40), (104, 18, 30)
GILT, GILT_D = (214, 170, 72), (160, 118, 44)
WOOD, WOOD_D = (128, 82, 50), (96, 60, 36)


def box(p, x0, y0, x1, y1, f, lw=3, line=INK):
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], f, line, lw)


def wallpaper(img, p, x0, x1):
    """Damask green above a cream dado, skirting, parquet: the same in every direction."""
    box(p, x0, -700, x1, 1060, GREEN, 0)
    for y in range(-640, 1040, 110):                          # a quiet damask motif
        off = 55 if (y // 110) % 2 else 0
        for x in range(int(x0) + off, int(x1), 110):
            p.poly([(x, y - 22), (x + 14, y), (x, y + 22), (x - 14, y)], GREEN_L, None)
            p.ell(x, y, 4, 4, GREEN_D, None)
    box(p, x0, 1040, x1, 1062, CREAM_D, 2.4)                  # dado rail
    box(p, x0, 1062, x1, FY - 34, CREAM, 0)
    for x in range(int(x0) + 30, int(x1) - 120, 230):         # panel mouldings
        box(p, x, 1100, x + 190, FY - 70, None, 2.0, CREAM_D)
    box(p, x0, FY - 34, x1, FY, WOOD_D, 2.4)                  # skirting
    box(p, x0, FY, x1, 2700, (150, 102, 62), 0)                # parquet
    for x in range(int(x0) - 400, int(x1), 90):
        p.line([(x, FY), (x - 260, 2700)], (126, 84, 50), 2.2)


def drape(p, x0, x1, top, bottom, flip=1):
    """A heavy crimson curtain with folds and a gold tie-back."""
    p.poly([(x0, top), (x1, top), (x1 - flip * 30, bottom - 360), (x1 + flip * 10, bottom), (x0, bottom)], CRIMSON, INK, 3)
    for k in range(1, 4):
        x = x0 + (x1 - x0) * k / 4
        p.line([(x, top + 10), (x + flip * 8, bottom - 380), (x + flip * 14, bottom - 10)], CRIMSON_D, 3)
    ty = bottom - 380
    p.poly([(x0 - 4, ty - 12), (x1 - flip * 26, ty - 12), (x1 - flip * 26, ty + 14), (x0 - 4, ty + 14)], GILT, INK, 2.4)


def painting(p, x0, y0, x1, y1, subject='horse'):
    box(p, x0 - 22, y0 - 22, x1 + 22, y1 + 22, GILT, 3)
    box(p, x0 - 8, y0 - 8, x1 + 8, y1 + 8, GILT_D, 2)
    box(p, x0, y0, x1, y1, (70, 84, 60), 2)
    w, h = x1 - x0, y1 - y0
    box(p, x0, y0, x1, y0 + h * 0.55, (160, 150, 120), 0)     # a pale sky over a dark field
    if subject == 'horse':                                    # a stiff old sporting picture of a bay horse
        cx, cy, s = x0 + w * 0.5, y0 + h * 0.62, w / 300
        p.poly([(cx - 70 * s, cy - 20 * s), (cx + 50 * s, cy - 24 * s), (cx + 80 * s, cy - 70 * s), (cx + 100 * s, cy - 60 * s),
                (cx + 76 * s, cy - 10 * s), (cx + 60 * s, cy + 20 * s), (cx - 70 * s, cy + 22 * s)], (110, 62, 36), INK, 2)
        for lx in (-60, -40, 40, 56):
            p.line([(cx + lx * s, cy + 18 * s), (cx + lx * s, cy + 70 * s)], (90, 50, 30), 4 * s)
        p.line([(cx - 70 * s, cy - 14 * s), (cx - 96 * s, cy + 30 * s)], (40, 28, 20), 4 * s)
    else:                                                     # a distant country house
        box(p, x0 + w * 0.3, y0 + h * 0.4, x0 + w * 0.7, y0 + h * 0.62, (190, 180, 160), 2)
        p.poly([(x0 + w * 0.28, y0 + h * 0.4), (x0 + w * 0.5, y0 + h * 0.28), (x0 + w * 0.72, y0 + h * 0.4)], (120, 110, 100), INK, 2)


def palace_painting(img, p, cam, x0, y0, x1, y1):
    """A big bright oil of a British royal palace: a long pale-stone front with a pillared centre and its balcony,
    the royal standard flying, black and gold railings, scarlet guardsmen, a blue summer sky (generic, no likeness
    of any one building)."""
    box(p, x0 - 26, y0 - 26, x1 + 26, y1 + 26, (238, 192, 76), 3)
    box(p, x0 - 10, y0 - 10, x1 + 10, y1 + 10, (190, 140, 40), 2)
    w, h = x1 - x0, y1 - y0
    X = lambda u: x0 + w * u
    Y = lambda v: y0 + h * v
    box(p, x0, y0, x1, y1, (72, 150, 226), 2)                                 # summer sky
    soft(img, cam, [(x0, Y(0.3)), (x1, Y(0.3)), (x1, Y(0.62)), (x0, Y(0.62))], (180, 220, 250), 0.6, 20)
    for cx, cy, r in ((0.15, 0.12, 0.07), (0.24, 0.1, 0.05), (0.7, 0.16, 0.08), (0.8, 0.13, 0.05), (0.46, 0.08, 0.04)):
        p.ell(X(cx), Y(cy), w * r, h * r * 0.9, (252, 252, 255), None)
    box(p, x0, Y(0.78), x1, y1, (226, 210, 166), 0)                          # the forecourt
    box(p, x0, Y(0.7), X(0.06), y1, (58, 140, 66), 0)                         # trees at either end
    box(p, X(0.94), Y(0.7), x1, y1, (58, 140, 66), 0)
    for u in (0.02, 0.05, 0.95, 0.98):
        p.ell(X(u), Y(0.6), w * 0.04, h * 0.14, (70, 156, 72), INK, 1.6)
    stone, stone_d = (246, 232, 198), (214, 196, 156)
    box(p, X(0.06), Y(0.36), X(0.94), Y(0.8), stone, 2)                       # the long front
    box(p, X(0.06), Y(0.33), X(0.94), Y(0.37), stone_d, 1.6)                  # balustrade along the roof
    for k in range(60):
        u = 0.07 + 0.86 * k / 59
        p.line([(X(u), Y(0.33)), (X(u), Y(0.37))], (190, 172, 132), 1.2)
    for row, (v0, v1) in enumerate(((0.42, 0.52), (0.58, 0.68), (0.71, 0.77))):
        for k in range(22):
            u = 0.08 + 0.84 * k / 21
            if 0.38 < u < 0.62 and row < 2:
                continue
            box(p, X(u) - w * 0.009, Y(v0), X(u) + w * 0.009, Y(v1), (60, 84, 120), 1.2)
    box(p, X(0.38), Y(0.3), X(0.62), Y(0.8), (252, 242, 214), 2)              # the pillared centre
    p.poly([(X(0.37), Y(0.3)), (X(0.5), Y(0.2)), (X(0.63), Y(0.3))], (252, 242, 214), INK, 2)   # pediment
    p.poly([(X(0.41), Y(0.29)), (X(0.5), Y(0.23)), (X(0.59), Y(0.29))], None, stone_d, 1.4)
    for k in range(8):
        u = 0.395 + 0.21 * k / 7
        box(p, X(u) - w * 0.006, Y(0.33), X(u) + w * 0.006, Y(0.78), (255, 250, 232), 1.2)
    box(p, X(0.43), Y(0.53), X(0.57), Y(0.56), stone_d, 1.6)                 # the balcony, hung with crimson
    p.poly([(X(0.44), Y(0.56)), (X(0.56), Y(0.56)), (X(0.55), Y(0.6)), (X(0.45), Y(0.6))], (196, 20, 40), INK, 1.4)
    for k in range(3):
        box(p, X(0.455 + 0.035 * k), Y(0.44), X(0.48 + 0.035 * k), Y(0.53), (60, 84, 120), 1.2)
    p.line([(X(0.5), Y(0.2)), (X(0.5), Y(0.04))], (60, 60, 60), 2)            # flagpole and the royal standard
    fx, fy, fw, fh = X(0.5), Y(0.04), w * 0.09, h * 0.09
    for (a, b, c) in (((0, 0), (220, 30, 40), 0), ((1, 0), (250, 200, 40), 0), ((0, 1), (30, 70, 170), 0), ((1, 1), (220, 30, 40), 0)):
        box(p, fx + a[0] * fw / 2, fy + a[1] * fh / 2, fx + (a[0] + 1) * fw / 2, fy + (a[1] + 1) * fh / 2, b, 0)
    box(p, fx, fy, fx + fw, fy + fh, None, 1.6)
    p.line([(x0, Y(0.86)), (x1, Y(0.86))], (24, 24, 28), 2.4)                # black railings with gilded gates
    for k in range(70):
        u = k / 69
        p.line([(X(u), Y(0.86)), (X(u), Y(0.95))], (24, 24, 28), 1.4)
    for u in (0.44, 0.56):
        box(p, X(u) - w * 0.03, Y(0.83), X(u) + w * 0.03, Y(0.95), None, 2.4, (250, 196, 50))
    for u in (0.2, 0.32, 0.68, 0.8):                                          # guardsmen: bearskin, scarlet, black
        gx = X(u)
        p.ell(gx, Y(0.8), w * 0.007, h * 0.03, (20, 20, 22), None)
        box(p, gx - w * 0.006, Y(0.83), gx + w * 0.006, Y(0.88), (214, 24, 36), 0)
        box(p, gx - w * 0.005, Y(0.88), gx + w * 0.005, Y(0.93), (20, 20, 22), 0)
    soft(img, cam, [(X(0.06), Y(0.36)), (X(0.2), Y(0.36)), (X(0.2), Y(0.8)), (X(0.06), Y(0.8))], (120, 90, 60), 0.18, 10)


def chandelier(p, cx, top, s=1.0):
    p.line([(cx, top - 400), (cx, top)], GILT_D, 4)
    p.ell(cx, top + 40 * s, 120 * s, 26 * s, GILT, INK, 2.6)
    for k in range(-3, 4):
        x = cx + k * 34 * s
        p.line([(x, top + 60 * s), (x, top + (110 + 20 * (3 - abs(k))) * s)], (230, 236, 240), 2)
        p.ell(x, top + (116 + 20 * (3 - abs(k))) * s, 6 * s, 9 * s, (236, 244, 250), INK, 1.4)
        p.poly([(x - 5 * s, top + 40 * s), (x + 5 * s, top + 40 * s), (x + 5 * s, top + 10 * s), (x - 5 * s, top + 10 * s)],
               (250, 246, 230), INK, 1.4)
        p.ell(x, top + 2 * s, 4 * s, 8 * s, (255, 210, 110), None)


def wall_a(img, cam, t):
    """Behind the PR man: a tall window with crimson drapes, a sporting picture, a console table and lamp."""
    p = B.Pen(img, cam)
    wallpaper(img, p, *SPAN)
    box(p, 214, 250, 446, 1010, (176, 206, 226), 4)           # the window: a pale grey English sky
    soft(img, cam, [(214, 700), (446, 640), (446, 1010), (214, 1010)], (220, 232, 236), 0.6, 30)
    for x in (330,):
        p.line([(x, 250), (x, 1010)], CREAM, 9)
    for y in (500, 760):
        p.line([(214, y), (446, y)], CREAM, 9)
    box(p, 200, 1004, 460, 1030, CREAM, 2.4)                   # sill
    drape(p, 120, 240, 200, FY - 10, 1)
    drape(p, 540, 420, 200, FY - 10, -1)
    box(p, 100, 176, 560, 236, CRIMSON_D, 3)                   # pelmet
    painting(p, 690, 380, 960, 610)
    box(p, 650, 1000, 1010, 1030, WOOD, 3)                     # console table and its lamp and decanter
    for x in (670, 990):
        box(p, x, 1030, x + 18, FY - 2, WOOD_D, 2.4)
    p.poly([(860, 1000), (880, 920), (900, 1000)], GILT, INK, 2.4)
    p.poly([(830, 920), (930, 920), (906, 840), (854, 840)], (242, 230, 200), INK, 2.4)
    soft(img, cam, oval(880, 900, 90, 70), (255, 230, 160), 0.25, 20)
    p.ell(730, 970, 22, 30, (200, 220, 226), INK, 2.2)          # a crystal decanter
    p.poly([(722, 944), (738, 944), (736, 916), (724, 916)], (200, 220, 226), INK, 2)
    p.ell(730, 908, 9, 9, (200, 220, 226), INK, 1.8)


def wall_c(img, cam, t):
    """The side wall the camera sweeps past: bookcase, door, long-case clock."""
    p = B.Pen(img, cam)
    wallpaper(img, p, *SPAN)
    box(p, -560, 200, -60, FY - 2, WOOD, 3)
    rng = np.random.default_rng(3)
    for k in range(5):
        y = 260 + k * 230
        box(p, -540, y + 190, -80, y + 208, WOOD_D, 2)
        x = -530
        while x < -110:
            w = int(rng.integers(18, 34))
            h = int(rng.integers(130, 180))
            box(p, x, y + 190 - h, x + w, y + 190, tuple(int(v) for v in rng.choice([(120, 30, 34), (40, 60, 90), (60, 80, 50), (140, 110, 60)])), 1.6)
            x += w + 2
    box(p, 300, 380, 640, FY - 2, (240, 236, 224), 3)            # a panelled door
    for y0, y1 in ((420, 860), (900, FY - 50)):
        for x0 in (330, 480):
            box(p, x0, y0, x0 + 130, y1, None, 2, CREAM_D)
    p.ell(610, 960, 10, 10, GILT, INK, 2)
    box(p, 980, 520, 1100, FY - 2, WOOD_D, 3)                    # long-case clock
    p.ell(1040, 620, 50, 50, (246, 240, 224), INK, 2.4)
    p.line([(1040, 620), (1040, 584)], INK, 3)
    p.line([(1040, 620), (1066, 630)], INK, 3)
    painting(p, 1300, 420, 1560, 640, 'house')


# ------------------------------------------------------------------------------------------ Andrew the Hutt
SLUG, SLUG_D, SLUG_L = (206, 168, 128), (168, 128, 92), (236, 208, 168)
FACE_SKIN = (230, 184, 160)
HAIR_W = (236, 236, 232)


class Squash:
    """A camera wrapper that lets his whole mass breathe, bounce and settle about the base of the body."""
    def __init__(self, cam, base_x, base_y, sy=1.0, dy=0.0, dx=0.0):
        self.cam, self.bx, self.by, self.sy, self.dy, self.dx = cam, base_x, base_y, sy, dy, dx
        self.s, self.z = cam.s, getattr(cam, 'z', cam.s)

    def P(self, x, y):
        return self.cam.P(self.bx + (x - self.bx) * (2 - self.sy) ** 0.5 + self.dx, self.by + (y - self.by) * self.sy + self.dy)

    def S(self, v):
        return self.cam.S(v)


def hutt_state(t):
    """His acting, beat by beat."""
    shape = mouths.at(TRACK['AJ'], t)
    open_ = {'rest': 0.0, 'MBP': 0.0, 'etc': 0.3, 'E': 0.45, 'AI': 0.95, 'O': 0.8, 'U': 0.4, 'WQ': 0.35, 'FV': 0.2,
             'L': 0.6}.get(shape, 0.0)
    laugh = 0.0
    if LAUGH[0] <= t < LAUGH[1]:
        u = (t - LAUGH[0]) / (LAUGH[1] - LAUGH[0])
        laugh = math.sin(math.pi * min(1.0, u * 1.4)) if u < 0.72 else max(0.0, 1 - (u - 0.72) / 0.28) * 0.6
        open_ = max(open_, 0.55 + 0.4 * abs(math.sin(math.pi * (t - LAUGH[0]) * 2.4)))
    bounce = -abs(math.sin(math.pi * (t - LAUGH[0]) * 2.4)) * 16 * laugh if laugh else 0.0
    sy = 1.0 + 0.008 * math.sin(2 * math.pi * t / 3.6) - (0.025 * laugh * abs(math.sin(math.pi * (t - LAUGH[0]) * 2.4)))
    look = 0.75 if t < 8.25 else (0.0 if t < 13.0 else -0.15)  # eyes slide from his pizza to us, then sidelong
    blink = F.blinking(t, HUTT_BLINKS) or laugh > 0.3
    tug = 0.0
    if t >= TUG:
        u = t - TUG
        tug = ease(u / 0.12) if u < 0.12 else max(0.0, 1 - (u - 0.12) / 0.5)
    return dict(open=open_, laugh=laugh, bounce=bounce, sy=sy, look=look, blink=blink, tug=tug)


HUTT_BLINKS = F.blinks(21, 8.0, 16.0, per_min=(8, 12))


def hookah(img, p, cam, t):
    x, base = 1020, 1338
    p.ell(x, base - 6, 46, 12, GILT_D, INK, 2.4)
    p.poly([(x - 30, base - 8), (x + 30, base - 8), (x + 46, base - 70), (x + 30, base - 120), (x - 30, base - 120),
            (x - 46, base - 70)], (90, 140, 150), INK, 2.6)                    # the glass water bowl
    soft(img, cam, [(x - 30, base - 100), (x - 14, base - 110), (x - 20, base - 30), (x - 34, base - 40)], (255, 255, 255), 0.4, 3)
    box(p, x - 9, base - 330, x + 9, base - 120, GILT, 2.4)                    # the stem
    for y in (base - 160, base - 240):
        p.ell(x, y, 20, 8, GILT, INK, 2)
    p.poly([(x - 30, base - 330), (x + 30, base - 330), (x + 18, base - 360), (x - 18, base - 360)], GILT, INK, 2.4)
    p.ell(x, base - 362, 18, 6, (220, 90, 40), INK, 1.6)                        # the coals
    rng = np.random.default_rng(9)
    for k in range(5):                                                         # smoke, drifting up and fading
        ph = ((t * 0.32 + k / 5) % 1.0)
        sx = x - 10 + 40 * math.sin(ph * 5 + k) * ph
        sy = base - 380 - ph * 420
        soft(img, cam, oval(sx, sy, 22 + 40 * ph, 16 + 26 * ph, 20), (236, 236, 240), 0.32 * (1 - ph), 10)
    # the hose looping down onto the dais
    p.line([(x + 24, base - 70), (x + 70, base - 20), (x + 40, base + 30)], (40, 70, 60), 7)


def pizza_slice(p, hx, hy, ang):
    """A slice held by its crust (laid over the circle hand)."""
    ca, sa = math.cos(ang), math.sin(ang)
    R = lambda x, y: (hx + x * ca - y * sa, hy + x * sa + y * ca)
    p.poly([R(-46, 0), R(46, 0), R(0, -150)], (246, 204, 96), INK, 2.6)
    p.poly([R(-50, 6), R(50, 6), R(46, -14), R(-46, -14)], (206, 146, 74), INK, 2.4)
    for (x, y) in ((-14, -40), (16, -60), (-4, -96), (10, -26)):
        p.ell(*R(x, y), 10, 10, (190, 50, 40), INK, 1.4)


class Tilt:
    """The head group: drawn in its own upright coordinates, then leant over to one side and moved onto the body."""
    def __init__(self, cam, a, pivot, off):
        self.cam, self.a, self.pv, self.off = cam, a, pivot, off
        self.s, self.z = cam.s, getattr(cam, 'z', cam.s)

    def W(self, x, y):
        dx, dy = x - self.pv[0], y - self.pv[1]
        ca, sa = math.cos(self.a), math.sin(self.a)
        return self.pv[0] + self.off[0] + dx * ca - dy * sa, self.pv[1] + self.off[1] + dx * sa + dy * ca

    def P(self, x, y):
        return self.cam.P(*self.W(x, y))

    def S(self, v):
        return self.cam.S(v)


TAIL_TOP = ([24, 60, 160, 300, 400, 450], [1236, 1214, 1186, 1130, 1040, 920])
HK = 0.9                                      # he and his hookah sit on the high platform, a little smaller
HUTT_AT = (540 - HK * 540, 1150 - HK * 1338)   # local (540, 1338), the base of his body, lands at (540, 1150)


def hutt(img, cam, t):
    """The slug-king reclining on his dais like the throne-room Hutt: the tail stretched out to the left, the upper
    body propped up on the right, the head leant over towards the hookah. Wall-B coordinates."""
    st = hutt_state(t)
    J = Squash(cam, 640, 1338, st['sy'], st['bounce'])
    p = B.Pen(img, J)
    # the body: one long tapering mass, the tail tip lifting off the dais
    body = curve([(24, 1236), (60, 1214), (160, 1186), (300, 1130), (400, 1040), (450, 920), (480, 800), (580, 730),
                  (760, 722), (900, 790), (966, 950), (996, 1140), (980, 1338), (500, 1340),
                  (200, 1338), (90, 1318), (40, 1286)], 7)
    p.poly(body, SLUG, INK, 3.4)
    soft(img, J, [(860, 800), (940, 960), (980, 1150), (960, 1330), (860, 1330), (840, 900)], (90, 50, 30), 0.25, 30)
    soft(img, J, [(40, 1290), (300, 1300), (480, 1320), (480, 1338), (60, 1330)], (90, 50, 30), 0.2, 14)
    rng = np.random.default_rng(4)
    for _ in range(30):                                                        # mottling along the back and tail
        x = rng.uniform(90, 520)
        top = float(np.interp(x, *TAIL_TOP))
        y = rng.uniform(top + 22, 1310)
        p.ell(x, y, rng.uniform(7, 16), rng.uniform(5, 10), SLUG_D, None)
    for x in range(70, 430, 40):                                               # the ridges across the tail
        top = float(np.interp(x, *TAIL_TOP))
        p.line([(x, top + 6), (x - 6, (top + 1334) / 2), (x + 4, 1332)], (176, 136, 100), 2.4)
    p.poly(curve([(560, 940), (780, 900), (900, 1000), (940, 1180), (900, 1330), (600, 1336), (500, 1220),
                  (510, 1040)], 6), SLUG_L, INK, 2.4)                          # the pale belly with its rings
    for k in range(6):
        y = 1010 + 52 * k
        w = 170 + 26 * math.sin(k * 0.7 + 0.4) + 14 * k
        p.line([(722 - w, y + 10), (722, y + 24), (722 + w, y)], (206, 176, 136), 2.6)
    # the head group, leant over towards the hookah (more when he laughs, settling as he breathes)
    lean = 0.16 + 0.012 * math.sin(2 * math.pi * t / 5.0) - 0.05 * st['laugh']
    H = Tilt(J, lean, (540, 900), (135, -12))
    hp = B.Pen(img, H)
    hx, hy = 540, 690
    hp.poly([(492, 872), (540, 904), (518, 930)], (246, 246, 246), INK, 2.2)  # shirt collar and a funeral-black tie
    hp.poly([(588, 872), (540, 904), (562, 930)], (246, 246, 246), INK, 2.2)
    hp.poly([(530, 900), (550, 900), (556, 924), (524, 924)], (24, 24, 28), INK, 2)
    hp.poly([(526, 924), (554, 924), (562, 1040), (540, 1062), (518, 1040)], (24, 24, 28), INK, 2)
    hp.ell(540, 990, 4, 6, (200, 200, 210), INK, 1)
    hp.poly(curve([(306, 700), (330, 590), (420, 530), (540, 512), (660, 530), (750, 590), (774, 700), (740, 800),
                   (660, 856), (540, 878), (420, 856), (340, 800)], 7), FACE_SKIN, INK, 3)
    soft(img, H, [(640, 560), (760, 640), (760, 790), (640, 850)], (160, 90, 80), 0.22, 18)
    for k, y in enumerate((852, 878, 900)):                                    # chins
        w = 150 - 26 * k
        hp.line([(540 - w, y - 20), (540 - w * 0.4, y), (540 + w * 0.4, y), (540 + w, y - 20)], (190, 138, 116), 2.6)
    for sgn in (-1, 1):                                                        # jowls
        hp.line([(hx + sgn * 62, 742), (hx + sgn * 112, 790), (hx + sgn * 150, 840)], (190, 138, 116), 2.6)
        hp.poly(curve([(hx + sgn * 150, 720), (hx + sgn * 214, 760), (hx + sgn * 200, 830), (hx + sgn * 150, 800)], 4),
                FACE_SKIN, None)
    L = B.Local(H, hx, hy - 4, 2.15)                                           # the series' face, scaled up
    sp = dict(skin=FACE_SKIN, hair_c=(196, 196, 192), brow_c=(206, 204, 198), brow_w=5.2, look=st['look'],
              blink=st['blink'], lid=3, harrow=0.85, age=True, creases=3,
              brows='joy' if st['laugh'] > 0.3 else ('fierce' if TUG <= t < TUG + 1.2 else None))
    B.face(img, B.Pen(img, L), sp, t, 0, 0, 68, 88)
    hp.poly(curve([(350, 610), (380, 556), (450, 518), (540, 506), (640, 516), (716, 556), (736, 610), (700, 588),
                   (630, 566), (560, 560), (470, 568), (400, 590)], 6), HAIR_W, INK, 2.6)   # white, swept back
    for k in range(5):
        x = 440 + 50 * k
        hp.line([(x, 572 - 6 * (2 - abs(k - 2))), (x + 50, 530)], (196, 196, 196), 2.2)
    # the mouth: very wide, corners down, opening on the words
    o = st['open']
    my = 784
    corners = 168
    smile = 14 * st['laugh']
    top = [(hx - corners, my + 16 - smile), (hx - 80, my - 4), (hx, my - 8 - 18 * o), (hx + 80, my - 4), (hx + corners, my + 16 - smile)]
    bot = [(hx + corners, my + 16 - smile), (hx + 90, my + 8 + 46 * o), (hx, my + 10 + 64 * o), (hx - 90, my + 8 + 46 * o)]
    if o > 0.05:
        hp.poly(curve(top + bot, 5), (44, 10, 16), INK, 3.6)
        hp.poly(curve([(hx - 70, my + 8 + 46 * o), (hx, my + 14 + 30 * o), (hx + 70, my + 8 + 46 * o), (hx, my + 6 + 62 * o)], 4),
                (176, 70, 80), None)                                           # the tongue
        hp.line(top, (200, 140, 120), 6)                                       # the thick upper lip
        hp.line(top, INK, 2.4)
    else:
        hp.line(top, INK, 3.4)
    hp.line([(hx - 70, my + 22 + 74 * o), (hx, my + 26 + 76 * o), (hx + 70, my + 22 + 74 * o)], (206, 150, 126), 2.4)  # wet lip
    # drool from both corners, hanging straight down whatever the lean: it stretches, snaps and drops
    for sgn, ph, sway in ((-1, 0.0, 1.0), (1, 0.45, -0.7)):
        cx, cy = H.W(hx + sgn * (corners - 8), my + 18 - smile)
        u = (t * 0.42 + ph) % 1.0
        ln = 30 + 140 * u
        tip = (cx + sway * 8 * math.sin(t * 2.2 + ph * 6), cy + ln)
        mid = ((cx + tip[0]) / 2 + sgn * 4, (cy + tip[1]) / 2)
        p.line([(cx, cy), mid, tip], INK, 9)
        p.line([(cx, cy), mid, tip], (214, 230, 200), 6)
        p.ell(tip[0], tip[1] + 6, 9, 12, (214, 230, 200), INK, 1.8)
        if u < 0.25:                                                           # the last drop, falling
            fy = cy + 170 + 600 * u
            if fy < 1040:
                p.ell(tip[0] + sgn * 2, fy, 8, 13, (214, 230, 200), INK, 1.6)
    # the stubby arms with their circle hands: left on the chain, right with a slice of pizza
    lh = (575 - 14 * st['tug'], 1000 - 22 * st['tug'])
    p.poly(curve([(600, 900), (660, 950), (620, 1010), (lh[0] + 20, lh[1] + 26), (lh[0] - 12, lh[1] - 22)], 4), SLUG, INK, 3)
    Q.chand(p, lh[0], lh[1], SLUG, 36)
    rh = (888, 968 + 6 * math.sin(t * 1.3))
    p.poly(curve([(850, 880), (800, 930), (830, 980), (rh[0] - 26, rh[1] + 22), (rh[0] + 14, rh[1] - 22)], 4), SLUG, INK, 3)
    pizza_slice(p, rh[0], rh[1] - 4, -0.35)
    Q.chand(p, rh[0], rh[1] + 10, SLUG, 36)
    return J.P(*lh)                                                            # where the chain starts (pixels)


# ------------------------------------------------------------------------------------------------ the models
MODEL_FEET = 1600
MODELS = [  # x, hair, colour, skin, what she is doing (one sentence each); her own height (s) and build
    dict(x=130, hair='blonde', hair_c=(232, 202, 128), skin=B.PALE, act='phone',      # scrolling her phone, head down
         s=0.455, sw=114, waist=0.72, hips=0.94, hw=56, hh=86, jaw='long'),          # very tall and willowy
    dict(x=305, hair='bob', hair_c=(74, 48, 34), skin=B.PINK, act='hips',            # hands on hips, glaring at him
         s=0.385, sw=126, waist=0.74, hips=1.2, hw=62, hh=80, jaw='round'),          # short and curvy
    dict(x=480, hair='long', hair_c=(150, 72, 40), skin=B.PALE, act='bored',         # hands clasped, eyes half shut
         s=0.425, sw=140, waist=0.84, hips=0.96, hw=60, hh=82, jaw='square'),        # athletic, broad shoulders
    dict(x=655, hair='long', hair_c=(32, 28, 30), skin=B.PINK, act='selfie',         # a selfie, smiling, arm up
         s=0.44, sw=134, waist=0.92, hips=1.16, hw=64, hh=82, jaw='soft'),           # tall with a fuller figure
    dict(x=830, hair='bob', hair_c=(238, 230, 212), skin=B.PALE, act='nails',        # inspecting her nails, yawning
         s=0.395, sw=110, waist=0.78, hips=1.0, hw=56, hh=80, jaw='soft'),           # petite
]
MODEL_BLINKS = [F.blinks(30 + i, 7.0, 16.0) for i in range(len(MODELS))]


def leia_torso(orig):
    """A gold bodice, a long burgundy skirt panel on a gold belt, and a gold slave collar (the costume evoked)."""
    def torso(img, p, sp, t):
        if not sp.get('leia'):
            return orig(img, p, sp, t)
        bottom = sp.get('bottom', 560)
        sw = sp.get('shoulders', 150)
        wa, hp = sw * sp.get('waist', 0.8), sw * sp.get('hips', 1.0)
        skin = sp['skin']
        p.poly([(-32, -80), (32, -80), (36, 10), (-36, 10)], skin, INK, 2.6)                # neck
        soft(img, p.cam, [(-32, -76), (32, -76), (30, -40), (-30, -40)], (150, 90, 80), 0.35, 4)
        gown = curve([(-40, -4), (-sw * 0.8, 12), (-sw, 52), (-sw * 0.98, 170), (-wa, 300), (-hp, 450), (-hp * 1.05, bottom),
                      (hp * 1.05, bottom), (hp, 450), (wa, 300), (sw * 0.98, 170), (sw, 52), (sw * 0.8, 12), (40, -4)], 4)
        p.poly(gown, sp.get('dress', B.GOLD), INK, 2.6)                               # the gown, shaped to her build
        p.poly([(-46, -4), (46, -4), (30, 50), (0, 70), (-30, 50)], skin, INK, 2.2)     # neckline
        soft(img, p.cam, [(sw * 0.4, 30), (sw, 60), (hp, 450), (hp, bottom), (hp * 0.5, bottom)], (0, 0, 0), 0.22, 10)
        p.poly([(-wa - 2, 296), (wa + 2, 296), (wa * 1.04 + 2, 334), (-wa * 1.04 - 2, 334)], B.GOLD, INK, 2.2)
        p.poly([(-wa * 0.55, 334), (wa * 0.55, 334), (hp * 0.6, bottom - 2), (-hp * 0.6, bottom - 2)], (128, 30, 44), INK, 2.2)
        p.line([(0, 350), (0, bottom - 10)], (100, 22, 34), 2)
        p.poly(oval(0, -26, 40, 14, 24), B.GOLD, INK, 2.2)                         # the collar
        p.ell(0, -10, 8, 8, None, INK, 2.6)                                       # its ring
    return torso


B.torso = leia_torso(B.torso)


def model_sp(i, t):
    m = MODELS[i]
    sp = dict(skin=m['skin'], hw=m['hw'], hh=m['hh'], jaw=m['jaw'], hair=m['hair'], hair_c=m['hair_c'], outfit='dress',
              dress=(214, 168, 64), trousers=(214, 168, 64), bottom=884, shoulders=m['sw'], waist=m['waist'],
              hips=m['hips'], full=True, pose='custom',
              leia=True, lips=True, name=f'model {i + 1}', earring=i % 2 == 0)
    rig = F.Rig(sp)
    sp['blink'] = F.blinking(t, MODEL_BLINKS[i])
    sp['breath'] = F.breath(t, 3.6 + 0.3 * i, 1.4, 0.7 * i)
    jolt = spring(t - TUG - 0.06 * i, 1.0) * max(0.0, 1 - 0.3 * i)            # the yank travels down the chain
    sp['tilt'] = -0.05 * jolt
    a, mouth, look = m['act'], 'set', 0.0
    if a == 'phone':
        arms = dict(rig.pose('sides'), **rig.pose('hold', side='R', lift=0.85))
        sp.update(lid=6, head_dy=5)
    elif a == 'hips':
        arms = rig.pose('hips')
        look, mouth = 0.8, 'set'
        sp['brows'] = 'fierce' if t > TUG else 'serious'
    elif a == 'bored':
        arms = rig.pose('clasped')
        sp['lid'] = 5
    elif a == 'selfie':
        sh = rig.shoulder('R')
        arms = dict(rig.pose('sides'), R=rig.arm('R', (sh[0] + 50, sh[1] - 250), 'palm', 'out'))
        mouth, look = 'smile', 0.0
        sp['tilt'] = 0.12 + sp['tilt']
    else:  # nails: one hand held up in front of her, looked at; a yawn now and then
        arms = dict(rig.pose('sides'), **rig.pose('hold', side='L', lift=1.0))
        look = -0.5
        yawn = (t % 5.2) / 5.2
        if 0.55 < yawn < 0.75:
            mouth, sp['blink'] = 'v:O', True
    sp.update(arms=arms, mouth=mouth, look=look)
    return sp, rig


def hand_centre(arm):
    el, wr = arm[0], arm[1]
    d = (wr[0] - el[0], wr[1] - el[1])
    n = math.hypot(*d) or 1.0
    return wr[0] + d[0] / n * 12, wr[1] + d[1] / n * 12


def phone(p, x, y, back=False, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    R = lambda u, v: (x + u * ca - v * sa, y + u * sa + v * ca)
    p.poly([R(-20, -36), R(20, -36), R(20, 36), R(-20, 36)], (30, 30, 36), INK, 2.2)
    if back:
        p.ell(*R(-9, -26), 5, 5, (90, 90, 100), INK, 1)
    else:
        p.poly([R(-15, -30), R(15, -30), R(15, 30), R(-15, 30)], (150, 200, 236), None)


def models(img, cam, t, chain_start):
    """The line of models on the floor in front of the dais, chained collar to collar back to his hand."""
    collars = []
    for i, m in enumerate(MODELS):
        soft(img, cam, oval(m['x'], MODEL_FEET + 2, 190 * m['s'], 14, 24), (0, 0, 0), 0.3, 6)
    for i, m in enumerate(MODELS):
        sp, rig = model_sp(i, t)
        x = m['x'] + 2.0 * math.sin(2 * math.pi * t / (4.0 + 0.6 * i) + i)        # a gentle sway, never in step
        x -= 10 * spring(t - TUG - 0.06 * i) * max(0.0, 1 - 0.3 * i)
        neck = MODEL_FEET - F.SOLE_Y * m['s']                                     # every pair of feet on the same floor
        B.person(img, cam, x, neck, m['s'], sp, t)
        L = B.Local(cam, x, neck, m['s'])
        lp = B.Pen(img, L)
        if m['act'] in ('phone', 'selfie'):
            hx, hy = hand_centre(sp['arms']['R'])
            phone(lp, hx, hy - 18, back=m['act'] == 'selfie', ang=0.3 if m['act'] == 'selfie' else 0.0)
            Q.chand(lp, hx, hy, sp['skin'])
        collars.append(L.P(0, -6))
    # the chain: from his hand down to the middle model's collar, and collar to collar along the line
    d = ImageDraw.Draw(img)
    lw = max(2, int(cam.S(3)))
    gap = cam.P((MODELS[2]['x'] + MODELS[3]['x']) / 2, MODEL_FEET - 200)       # the slack hangs between two models
    for j, ((x0, y0), (x1, y1)) in enumerate([(chain_start, collars[2])] + list(zip(collars, collars[1:]))):
        if j == 0:   # from his hand the chain drops through the gap, below the collars, and loops up to hers
            ctl = (gap[0] - cam.S(10), gap[1])
        else:
            ctl = ((x0 + x1) / 2, (y0 + y1) / 2 + 0.32 * math.hypot(x1 - x0, y1 - y0))
        ln = math.hypot(ctl[0] - x0, ctl[1] - y0) + math.hypot(x1 - ctl[0], y1 - ctl[1])
        n = max(6, int(ln / cam.S(13)))
        for k in range(n):
            u = (k + 0.5) / n
            x = (1 - u) ** 2 * x0 + 2 * u * (1 - u) * ctl[0] + u * u * x1
            y = (1 - u) ** 2 * y0 + 2 * u * (1 - u) * ctl[1] + u * u * y1
            r = cam.S(6.5 if k % 2 == 0 else 2.5)
            d.ellipse([x - cam.S(6.5), y - r, x + cam.S(6.5), y + r], fill=(176, 176, 184), outline=(24, 22, 26), width=lw)


def wall_b(img, cam, t):
    """Andrew's end of the room: the palace picture, crimson drapes, a red dais, the hookah, him, the models."""
    p = B.Pen(img, cam)
    wallpaper(img, p, *SPAN)
    palace_painting(img, p, cam, 150, 150, 930, 560)                           # the royal palace, big and bright
    drape(p, -40, 110, 60, FY - 10, 1)
    drape(p, 1120, 970, 60, FY - 10, -1)
    box(p, -610, 1112, 1690, 1152, (176, 40, 52), 3)                          # the dais: velvet top, gilt edge
    box(p, -610, 1152, 1690, FY + 30, (140, 26, 40), 3)
    p.line([(-610, 1158), (1690, 1158)], GILT, 5)
    for x in range(-500, 1690, 250):                                          # panels with brass ring pulls
        box(p, x, 1190, x + 220, FY - 4, None, 2.4, (110, 18, 30))
        p.ell(x + 110, 1290, 20, 20, None, GILT_D, 4)
    box(p, -100, 1460, 1180, 2700, (120, 36, 44), 3)                          # a Persian rug in front
    box(p, -60, 1490, 1140, 2700, (150, 56, 54), 0)
    for x in range(-40, 1140, 70):
        p.poly([(x, 1475), (x + 14, 1468), (x + 28, 1475), (x + 14, 1482)], GILT, None)
    H = B.Local(cam, HUTT_AT[0], HUTT_AT[1], HK)
    soft(img, H, oval(520, 1338, 500, 26), (0, 0, 0), 0.35, 10)
    start = hutt(img, H, t)
    hookah(img, B.Pen(img, H), H, t)
    models(img, cam, t, start)


# ------------------------------------------------------------------------------------------------ the PR man
PR = dict(skin=B.PALE, hw=70, hh=90, jaw='square', hair='side', hair_c=(132, 128, 126), outfit='suit',
          jacket=(46, 48, 58), trousers=(46, 48, 58), shirt=(240, 242, 246), tie=(36, 50, 96), glasses=True,
          age=True, creases=2, full=True, pose='custom', name='PR man')
PR_S = 0.8
PR_NECK = FY - F.SOLE_Y * PR_S
PR_BLINKS = F.blinks(5, 0.4, DUR, talking=True)


def pr_state(t):
    sp = dict(PR)
    rig = F.Rig(sp)
    speaking = any(ln['who'] == 'PR' and ln['start'] - 0.1 <= t < ln['end'] + 0.2 for ln in LINES)
    arms = dict(rig.pose('sides'), **rig.pose('hold', side='L', lift=0.7))       # the folder held to his chest
    if speaking and t < PAN0:                                                  # small beats with the free hand
        w = math.sin(2 * math.pi * 1.0 * t)
        sh = rig.shoulder('R')
        arms['R'] = rig.arm('R', (sh[0] + 70 + 14 * w, sh[1] + 160 - 20 * w), 'palm', 'down')
    sp['arms'] = arms
    shape = mouths.at(TRACK['PR'], t)
    sp['mouth'] = 'set' if shape == 'rest' else 'v:' + shape
    sp['blink'] = F.blinking(t, PR_BLINKS) or 16.05 <= t < 16.45                # the weary blink before "Yes"
    sp['brows'] = 'serious'
    if 3.55 <= t < 4.6:                                                        # "absolutely sure?"
        sp['brow_raise'], sp['brows'] = 5, None
    sp['lid'] = 2 if t >= CUT_BACK else 0
    sp['breath'] = F.breath(t, 4.0, 1.5) + (4 * math.sin(math.pi * (t - 16.1) / 0.8) if 16.1 <= t < 16.9 else 0)
    return sp


def pr_man(img, cam, t):
    sp = pr_state(t)
    soft(img, cam, oval(540, FY + 2, 130, 16), (0, 0, 0), 0.3, 6)
    B.person(img, cam, 540, PR_NECK, PR_S, sp, t)
    L = B.Local(cam, 540, PR_NECK, PR_S)
    lp = B.Pen(img, L)
    hx, hy = hand_centre(sp['arms']['L'])
    lp.poly([(hx - 30, hy - 150), (hx + 80, hy - 150), (hx + 80, hy + 30), (hx - 30, hy + 30)], (70, 40, 30), INK, 2.6)
    lp.line([(hx - 18, hy - 150), (hx - 18, hy + 30)], (50, 28, 20), 2)
    Q.chand(lp, hx, hy, sp['skin'])


# ------------------------------------------------------------------------------------------------ the frame
def scene(t, cam):
    img = B.canvas()
    lo, hi = cam.cx - 560 / cam.z, cam.cx + 560 / cam.z
    for w, fn in (('A', wall_a), ('C', wall_c), ('B', wall_b)):
        if U0[w] + SPAN[1] < lo or U0[w] + SPAN[0] > hi:
            continue
        wc = wall_cam(cam, w)
        fn(img, wc, t)
        if w == 'A':
            pr_man(img, wc, t)
    for w in ('C', 'B'):                                                       # the corners of the room
        x = U0[w] + SPAN[0]
        if lo < x < hi:
            px = cam.P(x, 0)[0]
            ImageDraw.Draw(img).line([(px, 0), (px, B.H * B.SS)], fill=(20, 30, 26), width=int(cam.S(6)))
    return img


def frame_image(t):
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    if PAN0 <= t < PAN1:                                                       # motion blur through the swing
        n = 9
        acc = None
        for k in range(n):
            tt = t + (k / (n - 1) - 0.5) * 0.6 / FPS
            a = np.asarray(scene(tt, camera(tt)), np.float32)
            acc = a if acc is None else acc + a
        img = Image.fromarray((acc / n).astype(np.uint8), 'RGBA')
    else:
        img = scene(t, camera(t))
    c = caption_at(t)
    if c:
        Q.caption(img, c)
    return img


def checks():
    """Faces inside TikTok's safe area in each held shot, at both ends of each push."""
    B.SS = 1
    bad = []
    for t in (0.1, PAN0 - 0.05, PAN1 + 0.05, CUT_BACK - 0.05, CUT_BACK + 0.05, BLACK_AT - 0.05):
        cam = camera(t)
        heads = []
        if t < PAN0 or t >= CUT_BACK:
            heads.append(('PR man', cam.P(540, PR_NECK - 150 * PR_S), 75 * PR_S * cam.z))
        else:
            c = wall_cam(cam, 'B')
            heads.append(('Andrew', c.P(HUTT_AT[0] + HK * 670, HUTT_AT[1] + HK * 700), 190 * cam.z))
            for i, m in enumerate(MODELS):
                heads.append((f'model {i + 1}', c.P(m['x'], MODEL_FEET - F.SOLE_Y * m['s'] - 150 * m['s']), 62 * m['s'] * cam.z))
        for name, (x, y), r in heads:
            if x - r < SAFE[0] or x + r > SAFE[2] or y - r < SAFE[1] or y + r > SAFE[3]:
                bad.append(f'{t:.2f} s: {name}\'s face leaves the safe area ({x:.0f}, {y:.0f})')
    B.SS = 2
    if bad:
        raise ValueError('; '.join(bad))


# ------------------------------------------------------------------------------------------------ output
def stills(out):
    B.SS = 2
    ts = [1.6, 4.0, 7.2, 8.6, 10.6, 14.2, 16.2, 17.4]
    tiles = []
    for t in ts:
        im = frame_image(t).convert('RGB').resize((540, 960), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        d.text((14, 912), f'{t:.1f} s', font=ImageFont.truetype(B.SANS, 30), fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
        tiles.append(im)
    sheet = Image.new('RGB', (4 * 540 + 30, 2 * 960 + 10), (20, 20, 20))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % 4) * 550, (i // 4) * 970))
    sheet.save(out, quality=88)
    print('stills:', out)


def render_frame(args):
    i, size, ss = args
    B.SS = ss
    return np.asarray(frame_image(i / FPS).convert('RGB').resize(size, Image.LANCZOS)).tobytes()


def render(out, scale=1.0, secs=None):
    import imageio_ffmpeg
    from multiprocessing import Pool
    size = (int(1080 * scale) // 2 * 2, int(1920 * scale) // 2 * 2)
    ss = 2 if scale > 0.6 else 1
    total = secs or DUR
    n = int(round(total * FPS))
    t0 = time.time()
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{size[0]}x{size[1]}', '-r', str(FPS), '-i', '-', '-f', 'lavfi', '-i',
                          'anullsrc=channel_layout=stereo:sample_rate=48000', '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '64k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for k, fr in enumerate(pool.imap(render_frame, [(i, size, ss) for i in range(n)], chunksize=2)):
            p.stdin.write(fr)
            if k % 24 == 0:
                print(f'frame {k}/{n}', flush=True)
    p.stdin.close()
    p.wait()
    print(f'done: {out} ({os.path.getsize(out) / 1e6:.2f} MB, {n} frames, {time.time() - t0:.0f} s)')


def main():
    a = sys.argv[1:]
    if len(a) < 2 or a[0] not in ('stills', 'final'):
        print(__doc__)
        return
    checks()
    if a[0] == 'stills':
        stills(a[1])
    else:
        scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
        secs = float(a[a.index('--secs') + 1]) if '--secs' in a else None
        render(a[1], scale, secs)


if __name__ == '__main__':
    main()
