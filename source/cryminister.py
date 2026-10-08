#!/usr/bin/env python3
"""Cry Minister (Satire style, from satire_template.py). Brief: prompts/cry-minister.md. Notes: notes/cryminister.md.

Andy Burnham, the TikTok Prime Minister, films one of his sincere addresses on a British high street. The subject: wolf
attacks on our high streets. Behind him a pack of five dire wolves tears a man in a Man City shirt to pieces; he carries
on. He sets out the little he can do (smaller wolves, wolf nets, means-tested wolfproof armour for pensioners), cracks
a little at having no money, and is chased off by the same five wolves, still filming himself.

Looks like one of his own TikToks, only hinted: handheld phone framing that drifts and settles, his word-by-word
captions (white, rounded, soft shadow, a couple of words at a time), a parody handle @TheTikTokPM, one on-screen caption
of his. No fake buttons, no real logos.

    python3 source/cryminister.py cast OUT.png              the cast sheet (every view of every wolf, Andy's stress 1-6)
    python3 source/cryminister.py stills OUT_DIR [T ...]    stills (no times: one per shot, at its key moment)
    python3 source/cryminister.py voices OUT.m4a            Sam's 20 lines, cleaned and matched, back to back
    python3 source/cryminister.py check                     every check and the audit
    python3 source/cryminister.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT]
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402  people: flat shapes, black outlines
import mossad as M               # noqa: E402  (brows, mouths, hair; patched into burnham on import)
import figure as F               # noqa: E402  arms solved and guarded
import mouths                    # noqa: E402  lip sync
import mossad_audio as MA        # noqa: E402  recordings cleaned
import filmkit                   # noqa: E402  the general checks
import film_engine as E          # noqa: E402  render with the picture cache, subtitle list, mouth check
import wolf as W                 # noqa: E402  the dire wolves
from burnham_film import load    # noqa: E402
from satire_style import Cam as SCam, Ctx, blob, limb, rough, install_circle_hands, OUT   # noqa: E402

mouths.install(B)
install_circle_hands(B)
FPS, SR = 12, MA.SR
INK = (24, 20, 22)
PUB_FONT = os.path.join(HERE, 'fonts', 'CinzelDecorative-Black.ttf')
CAP_FONT = os.path.join(HERE, 'fonts', 'TikTokSans-Bold.woff')   # his captions' font (TikTok Sans, OFL)

# =============================================== STORY ==============================================================
NAME = 'cryminister'
TITLE = ('CRY', 'MINISTER')
TITLE_AT = dict(cap=92, top=430)                  # Cranberry Title style, two lines, under the search bar; checked
TITLE_HOLD = 0.0                                  # Sam (8 Oct): no title in the video; the Cranberry title lives on the cover
HANDLE = '@TheTikTokPM'                           # the parody handle (never his real account name)
# Each line is one shot (hard cuts). audio: (file in source/audio, from s, to s); a file holding several lines is
# cut where Sam paused or, if he ran them together, at the quietest moment between the words.
LINES = [
    dict(n=1, shot='mid', text="Now here's a familiar sight you must recognise.", audio=('cry-1', 0.0, None)),
    dict(n=2, shot='half', text="Wolf attacks on British high streets. They're violent, they're concerning, and they've got to stop.",
         audio=('cry-2', 0.0, None)),
    dict(n=3, shot='mid', text='My Labour government are doing everything in their power to get this under control.',
         audio=('cry-3', 0.0, None)),
    dict(n=4, shot='bigwolf', text="We've implemented smaller wolves.", audio=('cry-4-6', 0.0, 2.72)),
    dict(n=5, shot='alley', text='More wolf nets down every alleyway.', audio=('cry-4-6', 2.72, 5.42)),
    dict(n=6, shot='lady', text='And means-tested wolfproof armour for pensioners.', audio=('cry-4-6', 5.42, None)),
    dict(n=7, shot='close', text="But there's more to do.", audio=('cry-7', 0.0, None)),
    dict(n=8, shot='mid', text="So I'm asking you, begging you.", audio=('cry-8', 0.0, None)),
    dict(n=9, shot='close', text='Please get a job.', audio=('cry-9', 0.0, None)),
    dict(n=10, shot='mid', text='Any job.', audio=('cry-10', 0.0, None)),
    dict(n=11, shot='further', text='We have NO money.', audio=('cry-11', 0.0, None)),
    dict(n=12, shot='wide', text='You want change when I can barely afford to faff about with the margins.',
         audio=('cry-12', 0.0, None)),
    dict(n=13, shot='eyes', text="I'm so stressed.", audio=('cry-13', 0.0, None)),
    dict(n=14, shot='mid', text="I haven't slept for weeks.", audio=('cry-14', 0.0, None)),
    dict(n=15, shot='close', text="I CAN'T stop every wolf attack.", audio=('cry-15', 0.0, None)),
    dict(n=16, shot='mid', text="I know it's a problem,", audio=('cry-16-18', 0.0, 2.235)),
    dict(n=17, shot='maul', text='Okay,', audio=('cry-16-18', 2.235, 2.67)),
    dict(n=18, shot='mid', text='Just STOP YELLING.', audio=('cry-16-18', 2.67, None)),
    dict(n=19, shot='close', text="I'm going to keep fighting for a fairer and safer country.", audio=('cry-19', 0.0, None)),
    dict(n=20, shot='run', text='Aw fook, here come some now.', audio=('cry-20', 0.0, None)),
]
PADS = {1: (0.35, 0.25), 2: (0.25, 0.55), 3: (0.15, 0.25), 4: (0.75, 0.5), 5: (0.9, 1.3), 6: (0.25, 0.7),
        12: (0.3, 0.5), 16: (0.12, 0.0), 17: (0.0, 0.08), 18: (0.0, 0.45), 19: (0.15, 0.45), 20: (0.35, 1.8)}
STRESS = 4                                    # Andy's stress in shots 13-14, 1-6 (Sam picks from the cast sheet)
ANDY = dict(B.BURNHAM, full=True, pose='custom', name='Andy')
MAN = dict(skin=B.PALE, hw=66, hh=86, jaw='round', hair='crop', hair_c=(150, 112, 74), outfit='jumper',
           jacket=(108, 172, 222), trousers=(28, 28, 32), bottom=470, full=True, pose='custom', name='the man')
LADY = dict(skin=(244, 214, 200), hw=62, hh=80, jaw='soft', hair=None, outfit='dress', dress=(238, 150, 184),
            shoulders=120, bottom=600, full=True, pose='custom', name='the old lady', age=True)
WOLF_S = 2.2                                  # dire wolves: shoulder about half a man's height (people at 0.8)
# ====================================================================================================================

AX, NECK, S = 540, 1000, 0.8                  # Andy's neck, his scale (front plane)
FY = NECK + F.SOLE_Y * S                      # the pavement under his feet
LADY_S = 0.64
MAN_X = -2600                                 # the man, in the street plane (x across, ground at y 0)


# ------------------------------------------------------------------------------------------------- the voices
def _cut(x, t):
    """The quietest moment within 60 ms of t (seconds): where to split lines Sam ran together."""
    hop, w = int(0.005 * SR), int(0.02 * SR)
    best, bt = 1e9, t
    for k in range(-12, 13):
        c = int((t + k * 0.005) * SR)
        e = float(np.mean(x[max(0, c - w):c + w] ** 2))
        if e < best:
            best, bt = e, t + k * 0.005
    return bt


def _match_tone(lines):
    """Make the takes sound like one session: each line's tone (its average spectrum, smoothed to thirds of an octave)
    is nudged towards the average of all of them, by at most 4 dB at any pitch. No echo, no pitch change."""
    from scipy.signal import firwin2, welch, fftconvolve
    specs = []
    for x in lines:
        f, p = welch(x, SR, nperseg=2048)
        specs.append(p + 1e-14)
    target = np.exp(np.mean([np.log(p) for p in specs], axis=0))
    out = []
    for x, p in zip(lines, specs):
        g_db = 10 * np.log10(target / p)
        sm = np.array([np.mean(g_db[(f >= fc / 2 ** (1 / 6)) & (f <= fc * 2 ** (1 / 6))]) if fc > 0 else 0.0 for fc in f])
        sm = np.clip(np.nan_to_num(sm), -4.0, 4.0)
        sm[f < 80] = sm[f > 80][0] if np.any(f > 80) else 0.0
        h = firwin2(1025, f / (SR / 2), 10 ** (sm / 20))
        out.append(fftconvolve(x, h, mode='same'))
    return out


VOICE_LUFS = -20.0


def _voices():
    """Sam's 20 lines: hum and hiss out, cut from their files, the takes matched in tone and set to one loudness.
    A file holding several lines keeps their loudness relative to each other (the shouts stay shouts)."""
    files = {}
    for ln in LINES:
        name = ln['audio'][0]
        if name not in files:
            x = load(os.path.join(HERE, 'audio', name + '.m4a'))
            files[name] = MA.denoise(MA.dehum(x))
    raw = []
    for ln in LINES:
        name, a, b = ln['audio']
        x = files[name]
        i = int(_cut(x, a) * SR) if a > 0 else 0
        j = int(_cut(x, b) * SR) if b is not None else len(x)
        seg = x[i:j]
        st = MA.pauses(seg, 0.12)
        if st:                                  # trim the silence round the words (50 ms kept each side)
            s0, s1 = max(0, int((st[0][0] - 0.05) * SR)), min(len(seg), int((st[-1][1] + 0.08) * SR))
            if a > 0:                           # a line cut from the middle of a run starts on its own word
                s0 = 0
            seg = seg[s0:s1]
        raw.append(seg)
    raw = _match_tone(raw)
    gains = {}
    for ln, x in zip(LINES, raw):               # loudness per file: lines from one file keep their balance
        gains.setdefault(ln['audio'][0], []).append(x)
    g = {k: 10 ** ((VOICE_LUFS - MA.lufs(np.concatenate(v))) / 20) for k, v in gains.items()}
    return [MA.edges(x * g[ln['audio'][0]]) for ln, x in zip(LINES, raw)]


VOICES = _voices()

# ------------------------------------------------------------------------------------------------- the timeline
T = 0.0
SHOTS = []                                    # (key, start, end, line index)
for i, ln in enumerate(LINES):
    pre, post = PADS.get(ln['n'], (0.12, 0.25))
    v = VOICES[i]
    ln['_voice'] = v
    ln['start'] = T + pre
    ln['end'] = ln['start'] + len(v) / SR
    ln['_stretches'] = MA.pauses(v, 0.12) or [(0.0, len(v) / SR)]
    SHOTS.append((f"{ln['n']}-{ln['shot']}", T, ln['end'] + post, i))
    T = ln['end'] + post
BLACK_AT = T                                  # hard cut to black...
DUR = T + 0.5                                 # ...held half a second
TRACK = [(a + ln['start'], b + ln['start'], sh) for ln in LINES
         for a, b, sh in mouths.track(ln['text'], ln['_stretches'])]
BLINKS = F.blinks(7, 0.4, DUR, talking=True)


def word_times(ln):
    """Each word's (start, end) in film seconds, spread over the recording's stretches the way the mouths are."""
    words = ln['text'].split()
    syl = [mouths._syllables(w) for w in words]
    st = ln['_stretches']
    per = sum(b - a for a, b in st) / max(1, sum(syl))
    out, k = [], 0
    for a, b in st:
        t, need, k0 = a, 0.0, k
        while k < len(words) and (need + syl[k] * per <= (b - a) * 1.25 or k == k0):
            need += syl[k] * per
            k += 1
        sc = (b - a) / max(need, 1e-6)
        for j in range(k0, k):
            d = syl[j] * per * sc
            out.append((ln['start'] + t, ln['start'] + t + d))
            t += d
    while len(out) < len(words):
        out.append((out[-1][1], out[-1][1] + 0.2) if out else (ln['start'], ln['end']))
    return out


def shot_at(t):
    for s in SHOTS:
        if s[1] <= t < s[2]:
            return s
    return SHOTS[-1]


def shot_of(t):
    return shot_at(t)[0]


def kind(t):
    return LINES[shot_at(t)[3]]['shot']


def line_of(n):
    return LINES[n - 1]


def word_at(n, k):
    """The start time of word k of line n."""
    return word_times(line_of(n))[k][0]


ATTACK = SHOTS[1][1] + 1.0                    # the first wolf's jaws reach the man's throat
POP = word_at(4, 2)                           # "smaller": the wolf pops to 60%
ARMOUR = word_at(6, 3)                        # "wolfproof": armour (and a wolf biting it) appear on the old lady
CHASE = SHOTS[19][1]


def u_in(t):
    """Seconds since the start of the current shot."""
    return t - shot_at(t)[1]


# ------------------------------------------------------------------------------------------------- cameras
# Each shot: Andy's camera (front plane: zoom, x, y at the frame's centre) and the street's (the shops and the wolves,
# further back). Between shots the camera moves (hard cuts), so the street is framed for each shot on its own.
CAMS = {
    'mid': ((2.6, AX, 895), (0.42, -1600, -1089)),
    'half': ((2.6, AX - 520 / 2.6, 918), (0.62, MAN_X + 250 / 0.62, -440)),
    'close': ((4.4, AX, 905), (0.7, -1700, -931)),
    'further': ((1.6, AX, 1060), (0.26, -1650, -1468)),
    'wide': ((0.42, AX + 240, 599), (0.13, -400, -2698)),
    'eyes': ((16.0, AX - 4, 886), (2.3, -1650, -1000)),
    'lady': ((1.15, AX - 40, 1190), (0.36, 1480, -560)),
    'bigwolf': (None, (1.05, 430, -470)),
    'maul': (None, (1.35, MAN_X + 40, -260)),
}


def drift(t, amount=9.0):
    """The phone in his hand: held, with a small quick shift now and then (never a sine wobble). Screen pixels."""
    sh = shot_at(t)
    seed = sh[3] * 7 + 3
    return (filmkit.shifts(t, seed=seed, amount=amount, hold=(0.9, 1.8), move=0.2),
            filmkit.shifts(t, seed=seed + 1, amount=amount * 0.7, hold=(1.1, 2.0), move=0.2))


def cams(t):
    """(Andy's camera, the street's camera) for time t, the handheld drift applied to both (it is the phone moving)."""
    k = kind(t)
    a, s = CAMS[k]
    dx, dy = drift(t)
    ac = B.Cam(a[0], a[1] - dx / a[0], a[2] - dy / a[0]) if a else None
    sc = B.Cam(s[0], s[1] - dx / s[0], s[2] - dy / s[0])
    return ac, sc


def X_(img, cam, ol=4):
    return Ctx(ImageDraw.Draw(img), SCam(cam.cx, cam.cy, cam.z, B.SS), ol=ol)


# ------------------------------------------------------------------------------------------------- the high street
SHOPS = [   # (x0, x1, kind): street-plane units, left to right; Andy stands in front of ZapBets
    (-7000, -4600, 'gold'), (-4600, -1600, 'pub'), (-1600, 1100, 'zap'), (1100, 3600, 'boarded'), (3600, 6200, 'nails')]
BASE, STOREY = -160, 1880                     # where the shop fronts meet the pavement; one storey


def box(X, x0, y0, x1, y1, fill, sd=0, amt=6, line=True):
    X.poly(rough([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], amt, sd), fill, line=line)


def sign_text(img, cam, x, y, s, size, fill, font=B.ANTON, stroke=0, angle=0.0):
    """Lettering on the street plane (shop signs, graffiti tags), centred on (x, y)."""
    px = cam.S(size)
    if px < 5:
        return
    f = ImageFont.truetype(font, int(px))
    l, t_, r, b = f.getbbox(s, stroke_width=int(stroke * px / 40))
    lay = Image.new('RGBA', (r - l + 8, b - t_ + 8), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((4 - l, 4 - t_), s, font=f, fill=fill, stroke_width=int(stroke * px / 40), stroke_fill=INK)
    if angle:
        lay = lay.rotate(math.degrees(angle), Image.BICUBIC, expand=True)
    X0, Y0 = cam.P(x, y)
    img.alpha_composite(lay, (int(X0 - lay.width / 2), int(Y0 - lay.height / 2)))


def window(X, x0, y0, x1, y1, sd, frame=(240, 236, 226), glass=(70, 84, 96), panes=(2, 1)):
    box(X, x0, y0, x1, y1, frame, sd, 4)
    m = 34
    nx, ny = panes
    for i in range(nx):
        for j in range(ny):
            a = x0 + m + (x1 - x0 - m) * i / nx
            b = y0 + m + (y1 - y0 - m) * j / ny
            box(X, a, b, a + (x1 - x0 - m) / nx - m, b + (y1 - y0 - m) / ny - m, glass, sd + i * 3 + j, 3)


def shop(img, cam, x0, x1, kind_):
    X = X_(img, cam)
    top = BASE - 2 * STOREY - 260
    if kind_ == 'pub':                         # The Goose and Cranberry: a Tudor pub, black beams on white plaster
        box(X, x0, top, x1, BASE - STOREY, (244, 238, 222), 11)
        for k in range(9):                                                   # the beams
            bx = x0 + 60 + (x1 - x0 - 120) * k / 8
            box(X, bx - 34, top + 40, bx + 34, BASE - STOREY - 20, (40, 32, 30), 30 + k, 3)
        box(X, x0, top + 40, x1, top + 110, (40, 32, 30), 41, 3)
        box(X, x0, BASE - STOREY - 120, x1, BASE - STOREY - 40, (40, 32, 30), 42, 3)
        for k in range(4):                                                   # crossed braces
            bx = x0 + 60 + (x1 - x0 - 120) * (2 * k + 1) / 8
            X.seg((bx - 150, top + 110), (bx + 150, BASE - STOREY - 120), 50, (40, 32, 30))
            X.seg((bx + 150, top + 110), (bx - 150, BASE - STOREY - 120), 50, (40, 32, 30))
        for k in range(3):                                                   # leaded windows upstairs
            wx = x0 + 380 + (x1 - x0 - 760) * k / 2
            box(X, wx - 230, top + 330, wx + 230, top + 900, (60, 50, 44), 50 + k, 4)
            for g in range(5):
                X.seg((wx - 220 + 92 * g, top + 340), (wx - 130 + 92 * g, top + 890), 8, (150, 150, 140))
                X.seg((wx + 220 - 92 * g, top + 340), (wx + 130 - 92 * g, top + 890), 8, (150, 150, 140))
        box(X, x0 - 40, top - 260, x1 + 40, top + 30, (96, 70, 60), 60, 10)       # the roof
        box(X, x0, BASE - STOREY, x1, BASE, (40, 70, 52), 61)                     # dark green pub front
        box(X, x0 + 60, BASE - STOREY + 60, x1 - 60, BASE - STOREY + 380, (24, 46, 34), 62, 4)
        sign_text(img, cam, (x0 + x1) / 2, BASE - STOREY + 220, 'THE GOOSE AND CRANBERRY', 170, (226, 190, 96), PUB_FONT)
        for wx in (x0 + 520, x1 - 520):
            window(X, wx - 380, BASE - STOREY + 520, wx + 380, BASE - 420, int(wx) % 97, (40, 70, 52), (230, 196, 120), (3, 2))
        box(X, (x0 + x1) / 2 - 230, BASE - STOREY + 520, (x0 + x1) / 2 + 230, BASE, (30, 50, 40), 63)   # door
        X.ell((x0 + x1) / 2 + 150, BASE - 640, 18, 18, (226, 190, 96))
    elif kind_ == 'zap':                       # ZapBets: a loud betting shop, purple and yellow, frosted windows
        box(X, x0, top + 120, x1, BASE - STOREY, (176, 150, 128), 71)
        for k in range(2):
            window(X, x0 + 300 + k * (x1 - x0 - 600) - 260, top + 400, x0 + 300 + k * (x1 - x0 - 600) + 260, top + 1100, 72 + k)
        box(X, x0 - 20, top + 60, x1 + 20, top + 160, (150, 128, 108), 74, 4)
        box(X, x0, BASE - STOREY, x1, BASE, (86, 40, 128), 75)
        box(X, x0 + 40, BASE - STOREY + 40, x1 - 40, BASE - STOREY + 420, (60, 24, 96), 76, 4)
        X.poly([(x0 + 300, BASE - STOREY + 70), (x0 + 210, BASE - STOREY + 250), (x0 + 290, BASE - STOREY + 240),
                (x0 + 220, BASE - STOREY + 400), (x0 + 400, BASE - STOREY + 190), (x0 + 310, BASE - STOREY + 200)], (250, 216, 40))
        sign_text(img, cam, (x0 + x1) / 2 + 120, BASE - STOREY + 230, 'ZapBets', 300, (250, 216, 40), stroke=3)
        for k, wx in enumerate((x0 + 480, x1 - 480)):
            box(X, wx - 400, BASE - STOREY + 520, wx + 400, BASE - 420, (210, 216, 222), 77 + k, 4)
            sign_text(img, cam, wx, BASE - STOREY + 760, 'WIN', 150, (86, 40, 128))
            sign_text(img, cam, wx, BASE - STOREY + 960, 'BIG!', 150, (200, 30, 60))
            sign_text(img, cam, wx, BASE - STOREY + 1170, '£££', 120, (60, 140, 70))
        box(X, (x0 + x1) / 2 - 200, BASE - STOREY + 520, (x0 + x1) / 2 + 200, BASE, (40, 40, 46), 79)
    elif kind_ == 'boarded':                   # an empty shop: boarded up, a torn TO LET, a faded fascia
        box(X, x0, top + 200, x1, BASE - STOREY, (150, 120, 100), 81)
        for k in range(2):
            wx = x0 + 600 + k * (x1 - x0 - 1200)
            box(X, wx - 260, top + 450, wx + 260, top + 1150, (120, 112, 104), 82 + k, 5)
            for g in range(3):
                box(X, wx - 300, top + 520 + 200 * g, wx + 300, top + 600 + 200 * g, (176, 140, 92), 90 + k * 3 + g, 6)
        box(X, x0, BASE - STOREY, x1, BASE, (120, 116, 108), 84)
        box(X, x0 + 40, BASE - STOREY + 40, x1 - 40, BASE - STOREY + 400, (170, 166, 150), 85, 4)
        sign_text(img, cam, (x0 + x1) / 2, BASE - STOREY + 220, 'SO  P  ORLD', 180, (130, 126, 116))
        rnd = random.Random(8)
        for k in range(7):                                                   # plywood boards over windows and door
            bx = x0 + 70 + (x1 - x0 - 140) * k / 7
            box(X, bx, BASE - STOREY + 470, bx + (x1 - x0 - 140) / 7 - 10, BASE - 10, (196, 158, 104) if k % 2 else (184, 146, 94), 100 + k, 5)
        box(X, x0 + 300, BASE - STOREY + 700, x0 + 1000, BASE - STOREY + 1050, (236, 236, 228), 110, 8)     # TO LET, torn
        sign_text(img, cam, x0 + 650, BASE - STOREY + 875, 'TO LET', 130, (200, 30, 40))
        X.poly([(x0 + 900, BASE - STOREY + 1050), (x0 + 1000, BASE - STOREY + 960), (x0 + 1000, BASE - STOREY + 1050)], (184, 146, 94))
        graffiti(img, cam, x0, x1)
    else:                                      # the outer shops of the wide shot: Cash 4 Gold, Nails & Vapes
        col, label, tc = ((40, 40, 46), 'CASH 4 GOLD', (236, 196, 60)) if kind_ == 'gold' else ((236, 170, 200), 'NAILS & VAPES', (40, 30, 60))
        box(X, x0, top + 160, x1, BASE - STOREY, (196, 170, 140) if kind_ == 'gold' else (168, 150, 140), 120 + len(kind_))
        for k in range(2):
            window(X, x0 + 520 + k * (x1 - x0 - 1040) - 240, top + 450, x0 + 520 + k * (x1 - x0 - 1040) + 240, top + 1150, 122 + k)
        box(X, x0, BASE - STOREY, x1, BASE, col, 125)
        sign_text(img, cam, (x0 + x1) / 2, BASE - STOREY + 220, label, 200, tc)
        window(X, x0 + 120, BASE - STOREY + 500, x1 - 120, BASE - 380, 126, (230, 230, 226), (90, 100, 110), (3, 1))


def graffiti(img, cam, x0, x1):
    """Graffiti on the boarded-up shop, drawn by hand in the show's lines: scrawled marker tags with drips, two
    bubble-letter pieces, and crude doodles. All of it sits on the boards and fascia, a little faded."""
    d = ImageDraw.Draw(img)
    w = lambda v: max(1, int(cam.S(v)))
    rnd = random.Random(23)
    top, base = BASE - STOREY + 60, BASE - 60
    # 1. scrawled tags: loopy one-stroke signatures in one colour, a few drips running down
    for k in range(8):
        col = [(40, 40, 46), (40, 110, 190), (190, 50, 140), (50, 140, 70), (220, 120, 40)][k % 5]
        gx, gy = x0 + 120 + rnd.uniform(0, x1 - x0 - 700), rnd.uniform(top + 380, base - 200)
        ph, n, h = rnd.uniform(0, 6), rnd.randint(9, 15), rnd.uniform(50, 90)
        pts = [(gx + 30 * q + 26 * math.cos(q * 2.3 + ph), gy - h * (0.5 + 0.5 * math.sin(q * 1.7 + ph)) * (1 + 0.25 * math.sin(q * 0.6)))
               for q in [i / 6 for i in range(n * 6)]]                             # smooth loops, like joined-up writing
        pts.append((pts[-1][0] + 40, gy + 20))
        pts.append((gx - 20, gy + 34))                                             # the underline swoosh back
        d.line([cam.P(*p) for p in pts], fill=col, width=w(11), joint='curve')
        for i in rnd.sample(range(len(pts) - 2), 2):                               # drips
            px, py = pts[i]
            ln = rnd.uniform(40, 120)
            d.line([cam.P(px, py), cam.P(px + 2, py + ln)], fill=col, width=w(7))
            X0, Y0 = cam.P(px + 2, py + ln)
            r = cam.S(9)
            d.ellipse([X0 - r, Y0 - r, X0 + r, Y0 + r], fill=col)
    # 2. two bubble-letter pieces: fat rounded letters, black outline, a colour fill, a white shine; each letter tipped
    for word, cx, cy, size, fill, sd in (('OI', x0 + 0.52 * (x1 - x0), top + 520, 300, (70, 170, 230), 1),
                                         ('ZEB', x0 + 0.78 * (x1 - x0), base - 520, 250, (130, 220, 90), 2)):
        rr = random.Random(sd)
        px = cam.S(size)
        if px < 6:
            continue
        f = ImageFont.truetype(CAP_FONT, int(px))
        adv = 0.0
        widths = [f.getlength(c) * 1.05 + px * 0.1 for c in word]
        start = cx - cam.S(0) - sum(widths) / 2 / max(cam.z * B.SS, 1e-6) * 0
        lx = cam.P(cx, cy)[0] - sum(widths) / 2
        for c, cw in zip(word, widths):
            o = int(px * 0.06)
            lay = Image.new('RGBA', (int(px * 1.6), int(px * 1.8)), (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            pos = (lay.width / 2, lay.height / 2)
            ld.text(pos, c, font=f, anchor='mm', fill=INK, stroke_width=o + max(2, int(px * 0.035)), stroke_fill=INK)
            ld.text(pos, c, font=f, anchor='mm', fill=fill, stroke_width=o, stroke_fill=fill)
            ld.ellipse([pos[0] - px * 0.2, pos[1] - px * 0.32, pos[0] - px * 0.08, pos[1] - px * 0.22], fill=(255, 255, 255))
            lay = lay.rotate(rr.uniform(-12, 12), Image.BICUBIC, expand=False)
            ly = cam.P(cx, cy)[1] + rr.uniform(-0.08, 0.08) * px
            img.alpha_composite(lay, (int(lx + cw / 2 - lay.width / 2), int(ly - lay.height / 2)))
            lx += cw
    # 5. crude doodles in marker: a smiley, a heart with initials, a badly drawn wolf, DAZZA WOZ ERE
    ink = (30, 30, 36)
    sx, sy = x0 + 0.2 * (x1 - x0), top + 760                                       # the smiley
    r = cam.S(90)
    X, Y = cam.P(sx, sy)
    d.ellipse([X - r, Y - r, X + r, Y + r], outline=ink, width=w(9))
    for k in (-1, 1):
        d.ellipse([X + k * r * 0.35 - r * 0.1, Y - r * 0.35, X + k * r * 0.35 + r * 0.1, Y - r * 0.12], fill=ink)
    d.arc([X - r * 0.55, Y - r * 0.5, X + r * 0.55, Y + r * 0.55], 20, 160, fill=ink, width=w(9))
    hx, hy = x0 + 0.36 * (x1 - x0), base - 330                                     # a heart, initials inside
    heart = [(hx + 110 * 16 * math.sin(a) ** 3 / 17, hy - 110 * (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a)
              - math.cos(4 * a)) / 17) for a in [2 * math.pi * i / 40 for i in range(41)]]
    d.line([cam.P(*p) for p in heart], fill=(200, 40, 60), width=w(9), joint='curve')
    scrawl(img, cam, hx, hy - 10, 'D+K', 70, (200, 40, 60), 4)
    wx, wy = x0 + 0.88 * (x1 - x0), top + 760                                      # a badly drawn wolf head
    wolf_pts = [(-80, 0), (-60, -110), (-30, -40), (30, -40), (60, -110), (80, 0), (50, 70), (-50, 70), (-80, 0)]
    d.line([cam.P(wx + a, wy + b) for a, b in wolf_pts], fill=ink, width=w(8), joint='curve')
    d.line([cam.P(wx - 40 + 16 * i, wy + 40 + (12 if i % 2 else -6)) for i in range(6)], fill=ink, width=w(6))
    for k in (-1, 1):
        d.line([cam.P(wx + k * 22 - 10, wy - 10), cam.P(wx + k * 22 + 10, wy)], fill=ink, width=w(7))
    scrawl(img, cam, x0 + 0.62 * (x1 - x0), base - 150, 'DAZZA WOZ ERE', 60, (40, 90, 170), 9)


def scrawl(img, cam, x, y, text, size, col, seed):
    """Words written by hand in marker: each letter its own slight tilt, size and height (never a straight typed line)."""
    px = cam.S(size)
    if px < 5:
        return
    rr = random.Random(seed)
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), int(px))
    total = sum(f.getlength(c) for c in text)
    X, Y = cam.P(x, y)
    lx = X - total / 2
    for c in text:
        cw = f.getlength(c)
        if c != ' ':
            lay = Image.new('RGBA', (int(px * 1.6), int(px * 1.6)), (0, 0, 0, 0))
            ImageDraw.Draw(lay).text((lay.width / 2, lay.height / 2), c, font=ImageFont.truetype(
                os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), int(px * rr.uniform(0.85, 1.15))), anchor='mm', fill=col)
            lay = lay.rotate(rr.uniform(-14, 14), Image.BICUBIC)
            img.alpha_composite(lay, (int(lx + cw / 2 - lay.width / 2), int(Y + rr.uniform(-0.12, 0.12) * px - lay.height / 2)))
        lx += cw


def cam_pt(cam, x, y):
    return cam.P(x, y)


def street(img, cam, t, wide=False):
    """The high street (street plane): sky, the shop fronts, the pavement; then the wolves' kill in front of the pub."""
    X = X_(img, cam)
    box(X, -12000, -12000, 12000, BASE - 2 * STOREY - 200, (188, 200, 210), 1, 0, line=False)           # a grey British sky
    skyline(img, cam, X)
    for x0, x1, k in SHOPS:
        shop(img, cam, x0, x1, k)
    box(X, -12000, BASE, 12000, 20000, (176, 174, 168), 2, 0, line=False)                              # the pavement
    for k in range(-30, 31):
        X.seg((k * 480, BASE), (k * 480 * 1.25, 3000), 5, (150, 148, 142))
    for k in range(6):
        X.seg((-12000, BASE + 140 * k * (1 + 0.3 * k)), (12000, BASE + 140 * k * (1 + 0.3 * k)), 5, (150, 148, 142))
    X.rect(-12000, BASE - 20, 12000, BASE + 10, (120, 118, 114), line=False)
    for lx in (-4800, 1250, 6400):                                                                      # lampposts, a bin
        X.rect(lx - 26, BASE - 2 * STOREY - 100, lx + 26, BASE + 120, (40, 46, 50))
        X.rect(lx - 26, BASE - 2 * STOREY - 100, lx + 220, BASE - 2 * STOREY - 50, (40, 46, 50))
        X.ell(lx + 210, BASE - 2 * STOREY - 30, 50, 34, (250, 240, 200))
    X.rect(-1250, BASE - 430, -950, BASE + 100, (36, 60, 44), r=30)
    busy = kind(t) not in ('bigwolf', 'maul')
    if busy:
        shoppers(img, cam, t, back=True)
    drunk(X, t)
    kill(img, cam, t)
    if busy:
        shoppers(img, cam, t, back=False)


def skyline(img, cam, X):
    """Behind the shops: a charming old church spire over the pub, and a drab concrete office block on the right."""
    roof = BASE - 2 * STOREY - 260
    stone, stone_d = (204, 192, 168), (164, 152, 130)
    tx0, tx1 = -3650, -2950                                              # the tower
    box(X, tx0, roof - 2300, tx1, roof + 200, stone, 201, 8)
    for k in range(6):
        X.seg((tx0 + 10, roof - 2300 + 380 * k), (tx1 - 10, roof - 2300 + 380 * k), 6, stone_d)
    X.poly(rough([(tx0 + 230, roof - 1950), (tx1 - 230, roof - 1950), (tx1 - 230, roof - 1500), (tx0 + 230, roof - 1500)], 6, 202), (70, 64, 60))
    X.poly([(tx0 + 230, roof - 1950), ((tx0 + tx1) / 2, roof - 2130), (tx1 - 230, roof - 1950)], (70, 64, 60))
    for k in range(4):
        X.seg((tx0 + 250, roof - 1900 + 100 * k), (tx1 - 250, roof - 1900 + 100 * k), 14, stone_d)   # belfry louvres
    X.ell((tx0 + tx1) / 2, roof - 1050, 170, 170, (236, 232, 220))                                 # the clock
    X.seg(((tx0 + tx1) / 2, roof - 1050), ((tx0 + tx1) / 2, roof - 1180), 18)
    X.seg(((tx0 + tx1) / 2, roof - 1050), ((tx0 + tx1) / 2 + 90, roof - 1010), 18)
    for sgn in (-1, 1):                                                  # little corner pinnacles
        cx = tx0 + 40 if sgn < 0 else tx1 - 40
        X.poly([(cx - 60, roof - 2300), (cx, roof - 2650), (cx + 60, roof - 2300)], stone)
    X.poly(rough([(tx0 + 60, roof - 2300), ((tx0 + tx1) / 2, roof - 5200), (tx1 - 60, roof - 2300)], 10, 203), (150, 156, 150))  # the spire
    for k in range(1, 6):
        u = k / 6
        hw_ = (tx1 - tx0 - 120) / 2 * (1 - u)
        X.seg(((tx0 + tx1) / 2 - hw_, roof - 2300 - 2900 * u), ((tx0 + tx1) / 2 + hw_, roof - 2300 - 2900 * u), 5, (120, 126, 122))
    cx = (tx0 + tx1) / 2                                                 # the weathercock on its rod
    X.seg((cx, roof - 5200), (cx, roof - 5600), 14)
    X.seg((cx - 90, roof - 5420), (cx + 90, roof - 5420), 10)
    blob(X, [(cx + 10, roof - 5640, 110, 55, 0.0), (cx + 100, roof - 5700, 40, 40, 0.0)], (210, 170, 70), ol=4)
    X.poly([(cx - 90, roof - 5650), (cx - 170, roof - 5740), (cx - 150, roof - 5600)], (210, 170, 70))
    ox0, ox1, top = 1500, 7000, roof - 4300                              # the office block: grey, gridded, unloved
    box(X, ox0, top, ox1, roof + 200, (150, 152, 148), 211, 6)
    for r in range(9):
        y = top + 260 + r * 420
        box(X, ox0 + 120, y, ox1 - 120, y + 220, (96, 108, 116), 212 + r, 4)
        for c in range(1, 18):
            x = ox0 + 120 + (ox1 - ox0 - 240) * c / 18
            X.seg((x, y), (x, y + 220), 6, (130, 132, 128))
    box(X, ox0 + 600, top - 420, ox0 + 1700, top, (136, 138, 134), 230, 6)        # plant room on the roof
    for k in range(5):
        X.seg((ox0 + 700 + 200 * k, top - 380), (ox0 + 700 + 200 * k, top - 40), 8, (110, 112, 108))
    X.rect(ox1 - 900, top - 700, ox1 - 860, top, (90, 92, 90))                      # an aerial mast


def drunk(X, t):
    """A drunk lying face down in a puddle on the pavement outside the boarded-up shop, breathing; a can beside him."""
    x, y = 2250, 210
    b = 6 * max(0.0, math.sin(t * 2 * math.pi / 4.2))                   # slow breaths lift his back
    X.ell(x - 330, y + 40, 330, 58, (120, 136, 150), line=False)         # the puddle
    X.ell(x - 360, y + 34, 200, 26, (150, 166, 180), line=False)
    for k, dy in enumerate((0, 30)):                                     # legs in jeans, trainers up
        limb(X, (x + 230, y - 40 + dy), (x + 640, y - 10 + dy), 92, (60, 84, 130))
        X.rell(x + 700, y - 30 + dy, 40, 56, 0.3, (236, 236, 232))
    blob(X, [(x + 30, y - 70 - b, 250, 92 + b, 0.03), (x - 150, y - 60 - b, 130, 84 + b, 0.0)], (70, 110, 76), ol=4)   # hoodie
    limb(X, (x - 140, y - 40), (x - 470, y + 20), 70, (70, 110, 76))     # an arm flopped out into the puddle
    X.ell(x - 490, y + 22, 30, 26, B.PALE)
    X.ell(x - 330, y - 30, 92, 78, (118, 84, 60))                        # the back of his head, face in the water
    X.ell(x - 300, y - 40, 22, 30, B.PALE)                               # an ear
    X.rect(x + 820, y - 70, x + 880, y + 40, (190, 30, 40), r=10)        # his can
    X.seg((x + 820, y - 30), (x + 880, y - 30), 6, (236, 236, 232))


# ---- shoppers: going about their day, glancing (eyes and head jump together) at the wolves or the Prime Minister
SHOPPER_PALS = [((120, 40, 50), (60, 50, 44), (230, 200, 180), (240, 140, 60)), ((60, 90, 140), (200, 170, 110), (200, 150, 120), (60, 150, 90)),
                ((150, 120, 90), (40, 36, 34), (240, 214, 196), (200, 40, 60)), ((90, 90, 96), (180, 180, 186), (160, 110, 80), (240, 220, 60)),
                ((176, 88, 140), (120, 70, 40), (236, 206, 186), (80, 120, 200)), ((50, 120, 110), (30, 30, 34), (120, 80, 56), (236, 236, 236))]


def _shoppers():
    """Each shopper: (enters at, starting x, direction, lane y, size, palette, stride seed, glances [(from, to, at)])."""
    out, rnd = [], random.Random(77)
    for k in range(15):
        d = 1 if k % 2 == 0 else -1
        t0 = -4.0 + 4.6 * k + rnd.uniform(-0.8, 0.8)
        x0 = -5600 if d > 0 else 2600
        lane = -80 if k % 3 else 300
        size = rnd.uniform(0.86, 1.04)
        # when each one passes the kill: a quick glance at the wolves; some also glance at the PM
        tk = t0 + abs(MAN_X - x0) / 640 - 0.5
        g = [(tk, tk + rnd.uniform(0.6, 1.0), 'wolves')]
        if k % 2 == 1:
            tp = t0 + abs(-1500 - x0) / 640
            g.append((tp, tp + 0.7, 'pm'))
        out.append((t0, x0, d, lane, size, k % len(SHOPPER_PALS), k, g))
    return out


SHOPPERS = _shoppers()


def _shopper_looks():
    """Each shopper's look: Hope Again's conference-goers from the same people library, changed up (no lanyards, everyday
    coats and colours, different hair), so the street matches the show's usual people."""
    rng = np.random.default_rng(31)
    out = []
    coats = [(120, 40, 50), (60, 90, 140), (150, 120, 90), (90, 90, 96), (176, 88, 140), (50, 120, 110), (200, 160, 60)]
    for k in range(len(SHOPPERS)):
        sp = B.attendee(rng)
        sp.update(lanyard=False, pose='custom', full=False, mouth='line', name=f'shopper {k + 1}',
                  jacket=coats[k % len(coats)], dress=coats[k % len(coats)],
                  trousers=[(40, 42, 50), (70, 60, 50), (30, 30, 34), (90, 80, 70)][k % 4])
        out.append(sp)
    return out


SHOPPER_LOOKS = _shopper_looks()


TUTTER, TUT = 1, (6.0, 9.9)                  # the man at the back in shot 2: stops dead, hands on hips, glares, shakes his head
_tau = ((math.ceil(0.95 * 8.0 + SHOPPERS[TUTTER][6] * 0.37) - SHOPPERS[TUTTER][6] * 0.37) / 0.95)   # a whole stride: both feet down
SHOPPERS[TUTTER] = (TUT[0] - _tau, -2250 + 640 * _tau) + tuple(SHOPPERS[TUTTER][2:])                  # behind the pack as he stops


def shopper_x(k, t):
    """Where shopper k is: walking at 640 a second, except the tutter, who stops dead while he reacts (note 33)."""
    t0, x0, d = SHOPPERS[k][0], SHOPPERS[k][1], SHOPPERS[k][2]
    tau = t - t0
    if k == TUTTER:
        tau -= max(0.0, min(t, TUT[1]) - TUT[0])
    return x0 + d * 640 * tau, tau


def shoppers(img, cam, t, back):
    """People going about their day along the pavement: the show's usual people, walking in a three-quarter view
    (walker.py) so we see faces and clothes while their legs stride the way they go. The nearer lane is drawn bigger.
    Now and then eyes and head snap to the wolves or the Prime Minister, then back."""
    import walker
    X = X_(img, cam)
    for k, (t0, x0, d, lane, size, pal, sd, g) in enumerate(SHOPPERS):
        if (lane < 0) != back or t < t0:
            continue
        x, tau = shopper_x(k, t)
        sx = cam.P(x, lane)[0] / B.SS
        if not -300 < sx < 1380:
            continue
        sc = S * size * (1 + lane / 2000)                         # nearer us, bigger
        sp = dict(SHOPPER_LOOKS[k])
        look = next((w for a, b, w in g if a <= t < b), None)
        turn = None
        speed = 640
        hips, blend = None, 0.0
        if k == TUTTER and TUT[0] <= t < TUT[1]:                   # stops dead, hands on hips, glares at the pack,
            u = t - TUT[0]                                         # three slow big shakes of the head, glares, walks on
            hips = F.Rig(sp).pose('hips')
            blend = min(1.0, u / 0.25, (TUT[1] - t) / 0.3)
            shake = -0.55 + 0.45 * math.sin(2 * math.pi * (u - 0.9) / 0.6) if 0.9 <= u < 2.7 else -0.55
            turn, sp['look'] = shake, -0.9
            sp.update(brows='fierce', lid=3, mouth='set')
        elif look == 'pm':
            turn, sp['look'] = 0.0, 0.0                            # a glance straight at him
        elif look == 'wolves':
            turn = 0.5 if MAN_X > x else -0.5
            sp['look'] = 0.9 if MAN_X > x else -0.9
        sp['blink'] = ((t + sd) % 3.7) < 0.12
        ph = (tau * 0.95 + sd * 0.37) % 1.0
        drawn = walker.walk(img, cam, B, F, x, lane, sc, sp, t, d, ph, speed, turn=turn, limb=limb, arms=hips, blend=blend)
        if sd % 3 != 0:                                            # a shopping bag from one hand
            el, wr = drawn['arms']['R'][:2]
            neck = lane - F.SOLE_Y * sc
            hx, hy = x + wr[0] * sc * 0.78, neck + (wr[1] + 30) * sc
            X.seg((hx, hy), (hx, hy + 50 * sc), 5 * sc)
            X.poly(rough([(hx - 55 * sc, hy + 45 * sc), (hx + 55 * sc, hy + 45 * sc), (hx + 64 * sc, hy + 190 * sc),
                          (hx - 64 * sc, hy + 190 * sc)], 4, sd), SHOPPER_PALS[pal][3])

# ------------------------------------------------------------------------------------------------- the kill
PACK = [   # (offset from the man, depth (+ = nearer), facing, palette, phase of its feeding): shot 2's five wolves
    (-620, -40, 1, 0, 0.0), (560, -50, -1, 1, 0.35), (-210, -110, 1, 2, 0.7), (250, -100, -1, 3, 0.15), (40, 40, 1, 4, 0.55)]
RIP = 1.4                                     # one feeding cycle: head down, worry it, rip a hunk up to the sky


def arrive(i):
    """Wolf i's leap at the man: its start time and where it takes off from (street units)."""
    t0 = ATTACK - 0.75 + 0.18 * i
    return t0


def wolf_kill_state(i, t):
    """Where wolf i of the pack is and what it is doing at time t (street plane). None before it appears."""
    dx, dz, face, pal, ph = PACK[i]
    t_leap = ATTACK - 0.45 + 0.2 * i                              # each takes off in turn (the first at the throat)
    t_land = t_leap + 0.45
    gx, gy = MAN_X + dx, dz
    if t < t_leap - 0.9:
        return None
    side = 1 if face > 0 else -1                                    # the left-hand wolves come from the left, the
    run_in = 600 if side > 0 else 500                              # right-hand ones sweep in from the right (behind
    if t < t_leap:                                                 # Andy), so none overshoots the man
        k = (t_leap - t) / 0.9
        x = gx - side * (2600 * k + run_in)
        return dict(x=x, y=gy, face=side, pal=pal, run=(t * 2.4 + i * 0.3) % 1.0)
    if t < t_land:                                                 # a short leap onto him: jaws first, landing on him
        u = (t - t_leap) / 0.45
        sx = gx - side * run_in
        x = sx + (gx - sx) * u
        lift = (260 if side > 0 else 180) * 4 * u * (1 - u) + 120 * (1 - u) * (i == 0)
        return dict(x=x, y=gy, face=side, pal=pal, leap=min(1.0, u * 1.6), lift=lift, jaw=1.0)
    c = ((t - t_land) / RIP + ph) % 1.0                           # feeding: down (0-0.55), worry, rip up (0.7-0.8), hold
    feed = 0.0 if c < 0.6 else (min(1.0, (c - 0.6) / 0.12) if c < 0.85 else max(0.0, 1.0 - (c - 0.85) / 0.15))
    blood = min(1.0, (t - t_land) / 3.0 + 0.2)
    hunk = None
    if 0.66 <= c < 0.8:
        hunk = 30 + i
    return dict(x=gx, y=gy, face=face, pal=pal, feed=feed, blood=blood, hunk=hunk, jaw=0.15 if hunk else 0.45)


def rips(t):
    """Every hunk flung so far: (release time, from, landing spot, flight time, size, seed)."""
    out = []
    for i in range(5):
        dx, dz, face, pal, ph = PACK[i]
        t_land = ATTACK - 0.45 + 0.2 * i + 0.45
        k = 0
        while True:
            # the rip-up moment of cycle k: c = 0.8
            rel = t_land + (k + 0.8 - ph) * RIP if 0.8 - ph >= 0 else t_land + (k + 1.8 - ph) * RIP
            if rel > t:
                break
            if k % 3 == i % 3 and k < 9:                           # now and then a hunk is let go, flung up
                rnd = random.Random(i * 31 + k)
                frm = (MAN_X + dx + face * 300 * WOLF_S / 2.2, dz - 520)
                land = (MAN_X + rnd.uniform(-900, 900), rnd.uniform(-60, 140))
                out.append((rel, frm, land, rnd.uniform(0.7, 1.1), rnd.uniform(40, 70), i * 31 + k))
            k += 1
    return out


def kill(img, cam, t, alone=None):
    """The man, the pack and the gore, in the street plane. alone: draw only that wolf (for the audit)."""
    X = X_(img, cam)
    downed = t >= ATTACK
    if alone is None:
        if downed:                                                 # the blood pool spreads, then stays
            r = 380 * min(1.0, 0.35 + (t - ATTACK) / 2.5)
            W.blood(X, MAN_X + 60, 30, r, 5, flat=0.3)
            W.blood(X, MAN_X - 420, 90, r * 0.35, 6, flat=0.3)
        for (rel, frm, land, d, sz, sd) in rips(t):                # hunks flung up: they land and stay
            u = t - rel
            if u >= d:
                W.meat(X, land[0], land[1] - sz * 0.4, sz, sd)
        if not downed:
            the_man(img, cam, t)
    order = sorted(range(5), key=lambda i: PACK[i][1])
    laid = False
    for i in order:
        if alone is None and downed and not laid and PACK[i][1] > -45:   # he lies between the back wolves and the front two
            man_down(img, cam, t)
            laid = True
        if alone is not None and i != alone:
            continue
        st = wolf_kill_state(i, t)
        if st is None:
            continue
        W.side(X, st['x'], st['y'], WOLF_S, st['face'], st['pal'], run=st.get('run'), leap=st.get('leap'),
               feed=st.get('feed'), jaw=st.get('jaw', 0.5), blood=st.get('blood', 0.0), hunk=st.get('hunk'),
               lift=st.get('lift', 0.0), seed=i * 13, blink=False)
    if alone is None:
        for (rel, frm, land, d, sz, sd) in rips(t):
            u = t - rel
            if 0 <= u < d:                                         # in flight, tumbling under gravity
                g = 5200.0
                vy = (land[1] - frm[1] - g * d * d / 2) / d
                x = frm[0] + (land[0] - frm[0]) * u / d
                y = frm[1] + vy * u + g * u * u / 2
                W.meat(X, x, y, sz, sd + int(u * 12))


CITY_PALE = (206, 228, 246)                    # the shirt's pale trim (collar, cuffs)


def city_shirt(img, cam, x, neck, sc, sp, tilt=0.0):
    """Over the man's sky-blue top, Sam's reference Man City home shirt in the show's flat style: a pale crew collar,
    short sleeves with pale cuffs (bare forearms), a made-up round crest and a made-up sponsor across the chest.
    No real badge, maker's logo or sponsor."""
    import peepee as PP
    L = B.Local(cam, x, neck, sc)
    p = B.Pen(img, L)
    p.line(B.oval(0, -2, 46, 22, 24, 0.15, math.pi - 0.15), CITY_PALE, 9)                     # collar
    p.line(B.oval(0, -2, 52, 27, 24, 0.15, math.pi - 0.15), B.INK, 1.6)
    PP.ctext(img, L, 0, 196, 'SKYHAD', 46, (255, 255, 255), font=CAP_FONT)                      # sponsor (made up)
    PP.ctext(img, L, 0, 236, 'AIRWAYS', 22, (255, 255, 255), font=CAP_FONT)
    p.ell(64, 92, 20, 22, (72, 132, 196), CITY_PALE, 3.0)                                      # crest (made up)
    p.ell(64, 92, 9, 10, CITY_PALE, None)
    rig = F.Rig(sp)
    for side in 'LR':                                                                          # short sleeves: bare forearms
        el, wr = sp['arms'][side][:2]
        shape = sp['arms'][side][2]
        cuff = (el[0] + 0.2 * (wr[0] - el[0]), el[1] + 0.2 * (wr[1] - el[1]))

        def band(a, b, wa, wb, col):
            dx, dy = b[0] - a[0], b[1] - a[1]
            n = math.hypot(dx, dy) or 1.0
            nx, ny = -dy / n, dx / n
            p.poly([(a[0] + nx * wa, a[1] + ny * wa), (b[0] + nx * wb, b[1] + ny * wb),
                    (b[0] - nx * wb, b[1] - ny * wb), (a[0] - nx * wa, a[1] - ny * wa)], col, B.INK, 2.2)
        band(el, wr, 19, 15, sp['skin'])                                               # bare forearm over the sleeve
        band(el, cuff, 22, 21, CITY_PALE)                                              # the short sleeve's pale cuff
        B.gesture_hand(p, el, wr, shape, sp['skin'])


def man_down(img, cam, t):
    """The man after the attack: the same character, flat on his back on the pavement under the pack, head towards the
    pub door, an arm flung up, eyes shut, mouth open. Drawn standing on a layer, then laid down (turned a quarter turn)."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    hip = (MAN_X + 80, -125)                                      # where his hips rest (half a body's depth off the ground)
    neck = hip[1] - 440 * S
    sp = dict(MAN)
    rig = F.Rig(sp)
    sp['arms'] = {'L': rig.arm('L', (-300, 120), 'fist', 'out', strict=False),
                  'R': rig.arm('R', (230, 330), 'fist', 'depth', strict=False)}
    sp.update(blink=True, mouth='v:O', brows='alarm', look=0.0, tilt=0.0)
    B.person(lay, cam, hip[0], neck, S, sp, t)
    city_shirt(lay, cam, hip[0], neck, S, sp)
    X = X_(lay, cam)
    for k in (-1, 1):                                              # his white trainers, toes up
        X.rell(hip[0] + k * 70 * S, neck + 918 * S, 62 * S, 22 * S, 0, (250, 250, 248))
    px, py = cam.P(*hip)
    img.alpha_composite(lay.rotate(90, Image.BICUBIC, center=(px, py)))


def the_man(img, cam, t):
    """The man before the attack: standing on the pavement in front of the pub, looking at his phone."""
    sp = dict(MAN)
    rig = F.Rig(sp)
    sp['arms'] = dict(rig.pose('sides'), R=rig.pose('hold', side='R', shape='phone', lift=0.7)['R'])
    sp['look'], sp['tilt'], sp['mouth'] = 0.1, 0.06, 'line'
    sp['blink'] = (t % 3.1) < 0.12
    sp['lid'] = 3
    if ATTACK - 0.4 <= t:                                          # he looks up: too late
        sp['look'], sp['lid'], sp['brows'], sp['tilt'] = -0.9, -2, 'alarm', 0.0
    neck = -F.SOLE_Y * S + 20
    B.person(img, cam, MAN_X, neck, S, sp, t)
    city_shirt(img, cam, MAN_X, neck, S, sp)
    X = X_(img, cam)
    for k in (-1, 1):                                              # white trainers over his shoes
        X.rell(MAN_X + k * 70 * S, neck + 918 * S, 62 * S, 22 * S, 0, (250, 250, 248))


# ------------------------------------------------------------------------------------------------- Andy
def B_(n, *beats):
    return filmkit.Beats([(line_of(n)['start'] + a, nm, p, *e) for a, nm, p, *e in beats])


# His gestures, line by line: each hand's target in his own units (x right, y down from the neck), as beats timed from
# the start of the line. Every frame of every gesture is tested (audits).
GEST = {
    1: dict(L=B_(1, (-0.2, 'set-up', (-40, 330)), (0.5, 'hold', (-40, 330)), (1.2, 'open', (-270, 200), 'slow')),
            R=B_(1, (-0.2, 'set-up', (40, 330)), (0.55, 'hold', (40, 330)), (1.25, 'open', (270, 200), 'slow'))),
    2: dict(R=B_(2, (0.0, 'set-up', (170, 300)), (0.5, 'chop', (200, 230)), (0.7, 'down', (180, 320), 'fast'),
                 (2.6, 'chop', (210, 220)), (2.8, 'down', (190, 320), 'fast'), (3.6, 'chop', (210, 220)),
                 (3.8, 'down', (190, 330), 'fast'), (5.0, 'settle', (170, 320), 'slow'))),
    3: dict(R=B_(3, (0.0, 'set-up', (150, 330)), (0.8, 'offer', (230, 260)), (2.2, 'turn', (200, 300)),
                 (3.2, 'offer', (240, 250)), (4.6, 'settle', (160, 330), 'slow'))),
    6: dict(L=B_(6, (-0.2, 'set-up', (-200, 300)), (0.2, 'thumb', (-310, 215), 'fast'), (6.0, 'hold', (-305, 220)))),
    8: dict(L=B_(8, (-0.1, 'set-up', (-60, 260)), (0.3, 'together', (-30, 190)), (0.9, 'press', (-30, 220)),
                 (1.4, 'together', (-30, 180)), (3.0, 'hold', (-30, 200))),
            R=B_(8, (-0.1, 'set-up', (60, 260)), (0.3, 'together', (30, 190)), (0.9, 'press', (30, 220)),
                 (1.4, 'together', (30, 180)), (3.0, 'hold', (30, 200)))),
    10: dict(L=B_(10, (-0.1, 'set-up', (-200, 300)), (0.25, 'wide', (-410, 30), 'slow'), (2.0, 'hold', (-400, 40))),
             R=B_(10, (-0.1, 'set-up', (200, 300)), (0.25, 'wide', (410, 30), 'slow'), (2.0, 'hold', (400, 40)))),
    11: dict(R=B_(11, (0.0, 'set-up', (170, 250)), (0.35, 'lift', (200, 180)), (0.55, 'chop', (190, 330), 'fast'),
                  (1.6, 'settle', (170, 320), 'slow'))),
    12: dict(R=B_(12, (0.0, 'set-up', (170, 300)), (1.0, 'offer', (250, 240)), (2.5, 'turn', (200, 300)),
                  (3.5, 'offer', (260, 230)), (5.5, 'settle', (170, 320)))),
    15: dict(R=B_(15, (-0.25, 'set-up', (140, 260)), (-0.12, 'swing out', (290, 60)), (-0.02, 'up', (190, -160)), (0.1, 'palm', (-8, -212), 'fast'), (4.0, 'hold', (-10, -214)))),
    16: dict(L=B_(16, (-0.12, 'raise', (-330, 0)), (0.18, 'pull', (-250, 190), 'fast'), (0.3, 'COME ON', (-115, 200), 'fast'), (0.5, 'shake', (-125, 175)),
                  (0.7, 'COME ON', (-115, 205), 'fast'), (1.4, 'hold', (-118, 200))),
             R=B_(16, (-0.12, 'raise', (330, 0)), (0.18, 'pull', (250, 190), 'fast'), (0.3, 'COME ON', (115, 200), 'fast'), (0.5, 'shake', (125, 175)),
                  (0.7, 'COME ON', (115, 205), 'fast'), (1.4, 'hold', (118, 200)))),
    18: dict(L=B_(18, (-0.05, 'set-up', (-200, 260)), (0.2, 'palms out', (-260, -30), 'fast'), (2.0, 'hold', (-250, -20))),
             R=B_(18, (-0.05, 'set-up', (200, 260)), (0.2, 'palms out', (260, -30), 'fast'), (2.0, 'hold', (250, -20)))),
}
BEND = {6: {'L': 'down'}, 10: {'L': 'down', 'R': 'down'}, 16: {'L': 'down', 'R': 'down'}, 18: {'L': 'down', 'R': 'down'}}
FACE = {   # brows, lids, harrow (the weight of it: rings under the eyes), what he does with his mouth between words
    1: dict(brows='sincere', lid=2), 2: dict(brows='serious', lid=2), 3: dict(brows='sincere', lid=3),
    6: dict(brows='confused', lid=5, rest='smile'), 7: dict(brows='sincere', lid=2, harrow=0.2),
    8: dict(brows='alarm', lid=0, harrow=0.3), 9: dict(brows='sincere', lid=1, harrow=0.35),
    10: dict(brows='alarm', lid=-1, harrow=0.4), 11: dict(brows='outrage', lid=-1, harrow=0.45),
    12: dict(brows='alarm', lid=0, harrow=0.5), 13: dict(brows='alarm', stress=True), 14: dict(brows='alarm', stress=True),
    15: dict(brows='alarm', lid=7, harrow=0.45, rest='set'), 16: dict(brows='fierce', lid=2, harrow=0.6),
    18: dict(brows='alarm', lid=-2, harrow=0.65), 19: dict(brows='sincere', lid=2, harrow=0.3),
    20: dict(brows='alarm', lid=-2, harrow=0.4)}
LEVELS = [   # Andy's stress (shots 13-14), 1 = slight, 6 = huge: rings, red rims, eye size, pupil, lid twitch, sweat, hair
    dict(name='1 Tired', harrow=0.35, rim=0.0, eye=1.0, pupil=4.5, twitch=False, sweat=0, hair=0),
    dict(name='2 Strained', harrow=0.55, rim=0.35, eye=1.05, pupil=4.2, twitch=False, sweat=0, hair=1),
    dict(name='3 Frayed', harrow=0.7, rim=0.6, eye=1.15, pupil=3.8, twitch=False, sweat=1, hair=2),
    dict(name='4 Haunted', harrow=0.85, rim=0.8, eye=1.25, pupil=3.2, twitch=True, sweat=1, hair=3),
    dict(name='5 Unravelling', harrow=1.0, rim=1.0, eye=1.38, pupil=2.6, twitch=True, sweat=2, hair=4),
    dict(name='6 Gone', harrow=1.0, rim=1.0, eye=1.5, pupil=2.0, twitch=True, sweat=3, hair=6)]


def andy_sp(t, n=None):
    """Everything about Andy at time t: arms, face, mouth, blink, the tilt of his head."""
    n = n or line_of_t(t)
    sp = dict(ANDY)
    rig = F.Rig(sp)
    arms = rig.pose('sides')
    for side, beats in GEST.get(n, {}).items():
        arms[side] = rig.arm(side, beats.at(t), 'fist', BEND.get(n, {}).get(side, 'out'), strict=False)
    sp['arms'] = arms
    fc = FACE.get(n, dict(brows='sincere', lid=2))
    sp['brows'] = fc.get('brows')
    sp['lid'] = fc.get('lid', 2)
    sp['harrow'] = fc.get('harrow', 0.0)
    if fc.get('stress'):
        sp['harrow'] = LEVELS[STRESS - 1]['harrow']
    shape = mouths.at(TRACK, t)
    talking = any(ln['start'] - 0.1 <= t <= ln['end'] for ln in LINES)
    sp['mouth'] = 'v:' + shape if shape != 'rest' else ('v:rest' if fc.get('rest') is None or talking else fc['rest'])
    if n == 15 and shape == 'E':                     # despairing: a grimace, never the wide 'E' that reads as a smile
        sp['mouth'] = 'v:etc'
    sp['blink'] = F.blinking(t, BLINKS) or bool(fc.get('stress'))
    sp['look'] = 0.0                                   # into the lens: he is talking to us
    sp['tilt'] = filmkit.shifts(t, seed=11, amount=0.035)
    if n == 6:
        sp['tilt'] = 0.06 + filmkit.shifts(t, seed=12, amount=0.02)
    if n == 15:                                      # head sinking further into the palm as he despairs
        sp['tilt'] = -0.1 - 0.06 * min(1.0, max(0.0, (t - line_of(15)['start']) / 2.0))
    filmkit.eyeline('Andy', t, (AX, NECK - 150 * S), (sp['look'], 0.0), (AX, NECK - 150 * S))
    return sp


def line_of_t(t):
    return LINES[shot_at(t)[3]]['n']


WIDE_X = -1200                                # shot 12: he stands on the street itself, among the shoppers, at their size


def andy(img, cam, t, x=AX):
    n = line_of_t(t)
    sp = andy_sp(t, n)
    neck = NECK
    if kind(t) == 'wide':
        cam, x, neck = cams(t)[1], WIDE_X, 200 - F.SOLE_Y * S
    B.person(img, cam, x, neck, S, sp, t)
    if n == 15:                                    # the face-palm: forearm and hand come in front of his face
        p = B.Pen(img, B.Local(cam, x, NECK, S))
        el, wr = sp['arms']['R'][:2]
        sh = F.Rig(ANDY).shoulder('R')
        B.arm(p, sh, el, wr, ANDY['jacket'])
        B.gesture_hand(p, el, wr, 'fist', ANDY['skin'])
    if FACE.get(n, {}).get('stress'):
        stressed_eyes(img, cam, x, sp, t, LEVELS[STRESS - 1])


def stressed_eyes(img, cam, x, sp, t, lv):
    """His eyes at a stress level: wider, red-rimmed, pin pupils, a twitching lid, sweat, hair coming loose. Drawn over
    the library's eyes (switched off by a 'blink'), then his glasses again on top."""
    import peepee as PP
    L = B.Local(cam, x, NECK, S)
    p = B.Pen(img, PP.Rot(L, sp.get('tilt', 0.0), pivot=(0, -60)))
    hx, hy, hw = 0, -150, ANDY['hw']
    k = lv['eye']
    tw = lv['twitch'] and (t * 5.3) % 1.0 < 0.18
    for sgn in (-1, 1):
        ex, ey = -4 + sgn * 30, hy - 8
        if lv['rim'] > 0:                                    # red-rimmed: a sore pink ring round each eye
            p.poly(B.curve([(ex - 21 * k, ey + 1), (ex - 9 * k, ey - 11 * k), (ex + 9 * k, ey - 11 * k), (ex + 21 * k, ey + 1),
                            (ex + 9 * k, ey + 10 * k), (ex - 9 * k, ey + 10 * k)], 6),
                   B.lt((206, 92, 100), 1.0 + 0.2 * (1 - lv['rim'])), None)
        almond = B.curve([(ex - 17 * k, ey), (ex - 8 * k, ey - 8 * k), (ex + 8 * k, ey - 8 * k), (ex + 17 * k, ey),
                          (ex + 8 * k, ey + 7 * k), (ex - 8 * k, ey + 7 * k)], 6)
        p.poly(almond, (250, 244, 240), B.INK, 2.0)
        if lv['rim'] > 0.5:                                  # bloodshot veins
            for a in (-0.5, 0.4):
                p.line([(ex + 15 * k * math.cos(a) * sgn, ey + 5 * k * math.sin(a)), (ex + 9 * k * sgn, ey + 2)], (214, 70, 80), 1.2)
        p.ell(ex, ey + 0.5, lv['pupil'], lv['pupil'], B.INK, None)
        if tw and sgn == -1:                                 # his right lid flickers down
            p.poly([(ex - 18 * k, ey - 1), (ex - 8 * k, ey - 9 * k), (ex + 8 * k, ey - 9 * k), (ex + 18 * k, ey - 1),
                    (ex + 8 * k, ey + 1), (ex - 8 * k, ey + 1)], B.dk(ANDY['skin'], 0.9), B.INK, 2.0)
    for j in range(lv['sweat']):                             # sweat at the temple
        sx, sy = hw * 0.8 + 6 * j, hy - 40 + 30 * j
        p.poly([(sx, sy - 14), (sx + 7, sy), (sx, sy + 6), (sx - 7, sy)], (170, 214, 236), B.INK, 1.8)
    for j in range(lv['hair']):                              # hair coming loose: strands sticking up
        a = -1.2 + 0.4 * j
        bx = -40 + 16 * j
        p.line([(bx, hy - ANDY['hh'] + 4), (bx + 10 * math.cos(a + 1.6), hy - ANDY['hh'] - 26 + 4 * (j % 2))], ANDY['hair_c'], 3.0)
    gc = (30, 28, 34)                                        # his glasses, back on top
    for sgn in (-1, 1):
        ex = -4 + sgn * 30
        p.poly([(ex - 25, hy - 24), (ex + 25, hy - 24), (ex + 23, hy + 8), (ex - 23, hy + 8)], None, gc, 4.2)
    p.line([(-9, hy - 18), (-4, hy - 21), (1, hy - 18)], gc, 3.6)


# ------------------------------------------------------------------------------------------------- the old lady
LADY_X = AX - 60                             # shot 6: she stands to his right (our left)
ANDY6_X = AX + 300
LADY_NECK = FY - F.SOLE_Y * LADY_S


ARM_OUT = filmkit.Beats([(0.0, 'set-up', (-190, 380)), (0.35, 'offered', (-480, 75), 'slow')])
BITE = 0.5                                    # seconds after the armour: the wolf lunges in and clamps on


def lady_arm(rig, t):
    """Her left arm: hanging by her side; once armoured, she holds it straight out for the wolf, unbothered."""
    if t < ARMOUR:
        return rig.arm('L', (-150, 400), 'fist', 'depth', strict=False)
    return rig.arm('L', ARM_OUT.at(t - ARMOUR), 'fist', 'down', strict=False)


def lady_sp(t):
    sp = dict(LADY)
    rig = F.Rig(sp)
    sp['arms'] = {'L': lady_arm(rig, t), 'R': rig.arm('R', (120, 380), 'fist', 'depth', strict=False)}
    sp['look'] = -0.55                                 # far away: somewhere over our left shoulder
    sp['brows'], sp['lid'] = None, 5
    sp['mouth'] = 'line'
    sp['blink'] = (t % 4.3) < 0.12
    sp['tilt'] = -0.05 + filmkit.shifts(t, seed=21, amount=0.015)
    return sp


def the_lady(img, cam, t, armour=None):
    """Little, petite: a pink frock trimmed in black, curly white hair, big white-and-pink striped glasses, a far-away
    look and a twitching right eye; a walking stick and a maroon handbag on the same side."""
    import peepee as PP
    if armour is None:
        armour = t >= ARMOUR
    sp = lady_sp(t)
    L = B.Local(cam, LADY_X, LADY_NECK, LADY_S)
    p = B.Pen(img, L)
    el, wr, _ = sp['arms']['R']
    p.line([(wr[0] + 20, wr[1] + 10), (wr[0] + 40, F.SOLE_Y)], (90, 60, 40), 9)               # the walking stick
    p.line([(wr[0] - 4, wr[1] + 4), (wr[0] + 26, wr[1] - 6)], (90, 60, 40), 9)
    B.person(img, cam, LADY_X, LADY_NECK, LADY_S, sp, t)
    sw, bottom = LADY['shoulders'], LADY['bottom']
    p.line([(-46, -4), (0, 70), (46, -4)], B.INK, 7)                                        # black trim: neckline, hem
    p.line([(-sw + 6, bottom - 6), (sw - 6, bottom - 6)], B.INK, 9)
    q = B.Pen(img, PP.Rot(L, sp['tilt'], pivot=(0, -60)))
    hx, hy, hw, hh = 0, -150, LADY['hw'], LADY['hh']
    rnd = random.Random(4)                                                                  # curly white hair
    for k in range(34):
        a = rnd.uniform(math.pi * 0.95, math.pi * 2.05)
        r = rnd.uniform(0.9, 1.18)
        cx, cy = hx + hw * 1.02 * r * math.cos(a), hy - hh * 0.25 + hh * 0.95 * r * math.sin(a)
        q.ell(cx, cy, 15, 13, (246, 244, 240), B.INK, 1.6)
    for sgn in (-1, 1):                                                                     # big striped glasses
        ex = -4 + sgn * 30
        q.ell(ex, hy - 6, 30, 26, None, (250, 250, 250), 9)
        for j in range(8):
            a0 = j * math.pi / 4
            q.line([(ex + 30 * math.cos(a0), hy - 6 + 26 * math.sin(a0)),
                    (ex + 30 * math.cos(a0 + 0.35), hy - 6 + 26 * math.sin(a0 + 0.35))], (236, 120, 170), 9)
        q.ell(ex, hy - 6, 34, 30, None, B.INK, 1.6)
    q.line([(-8, hy - 10), (0, hy - 14), (8, hy - 10)], (236, 120, 170), 5)
    if (t * 1.7) % 1.0 < 0.12:                                                              # her right eye twitches
        ex, ey = -4 - 30, hy - 8
        q.poly([(ex - 17, ey - 2), (ex, ey - 9), (ex + 17, ey - 2), (ex + 17, ey + 3), (ex - 17, ey + 3)], B.dk(LADY['skin'], 0.88), B.INK, 2.0)
        q.line([(ex - 34, ey - 10), (ex - 40, ey), (ex - 34, ey + 10)], B.INK, 2.0)
    # the maroon handbag, hanging from her right forearm
    bx, by = el[0] + 0.5 * (wr[0] - el[0]), el[1] + 0.5 * (wr[1] - el[1])
    p.line([(bx - 20, by), (bx - 30, by + 60)], (90, 20, 36), 5)
    p.line([(bx + 20, by), (bx + 30, by + 60)], (90, 20, 36), 5)
    p.poly([(bx - 52, by + 58), (bx + 52, by + 58), (bx + 60, by + 150), (bx - 60, by + 150)], (120, 26, 48), B.INK, 2.4)
    p.ell(bx, by + 76, 8, 6, (220, 190, 100), B.INK, 1.4)
    if armour:
        wolfproof(img, p, sp)


def wolfproof(img, p, sp):
    """Means-tested wolfproof armour: a bulky black body-armour vest with plates, WOLFPROOF across the chest, and
    ribbed guards on both forearms."""
    import peepee as PP
    vest = [(-70, 0), (70, 0), (130, 60), (136, 430), (-136, 430), (-130, 60)]
    p.poly(vest, (52, 56, 50), B.INK, 3.0)
    for k in range(3):
        p.poly([(-110, 120 + 100 * k), (110, 120 + 100 * k), (110, 200 + 100 * k), (-110, 200 + 100 * k)], (70, 76, 66), B.INK, 2.0)
    p.poly([(-118, 64), (118, 64), (118, 112), (-118, 112)], (236, 236, 228), B.INK, 2.0)
    PP.ctext(img, p.cam, 0, 88, 'WOLFPROOF', 30, (30, 30, 34), font=B.ANTON)
    rig = F.Rig(LADY)
    for side in 'LR':                          # Kevlar the whole length of both arms: ribbed sleeves, shoulder to wrist
        el, wr = sp['arms'][side][:2]
        sh = rig.shoulder(side)
        for a0, b0, n in ((sh, el, 4), (el, wr, 4)):
            for k in range(n):
                u0, u1 = k / n + 0.02, (k + 1) / n - 0.02
                a = (a0[0] + u0 * (b0[0] - a0[0]), a0[1] + u0 * (b0[1] - a0[1]))
                b = (a0[0] + u1 * (b0[0] - a0[0]), a0[1] + u1 * (b0[1] - a0[1]))
                p.line([a, b], B.INK, 48)
                p.line([a, b], (60, 64, 58), 42)
        p.ell(sh[0], sh[1] + 6, 40, 34, (52, 56, 50), B.INK, 2.6)       # shoulder pad


def biter(img, cam, t, alone=False):
    """One of the government's smaller wolves (60%, shot 4's), reared up on its hind legs, jaws clamped on her outstretched
    Kevlar sleeve, gnawing uselessly and tugging now and then."""
    if t < ARMOUR + BITE - 0.15:
        return
    rig = F.Rig(LADY)
    el, wr, _ = lady_arm(rig, t)
    tx, ty = LADY_X + (el[0] + 0.6 * (wr[0] - el[0])) * LADY_S, LADY_NECK + (el[1] + 0.6 * (wr[1] - el[1])) * LADY_S
    tug = filmkit.shifts(t, seed=33, amount=1.0, hold=(0.35, 0.7), move=0.1)
    probe = Image.new('RGBA', (2, 2))
    best = None                                   # stood on all fours on the pavement, tipped until its jaws meet her arm
    for k in range(-60, 31):
        a = k * 0.02
        jaw = W.side(X_(probe, cam), 0, 0, WOLF_S * 0.6, 1, 0, ang=a, jaw=0.1)
        err = abs(FY + jaw[1] - ty)
        if best is None or err < best[0]:
            best = (err, a, jaw)
    _, a, jaw = best
    X = X_(img, cam)
    chew = 0.08 + 0.32 * abs(math.sin((t - ARMOUR) * 2 * math.pi * 1.6))   # jaws working away at the sleeve
    lunge = max(0.0, 1.0 - (t - (ARMOUR + BITE - 0.15)) / 0.15) * 700     # it springs in from the left
    j = W.side(X, tx - jaw[0] - 6 * tug - lunge, FY, WOLF_S * 0.6, 1, 0, ang=a + 0.02 * tug, jaw=chew, snarl=1.0, seed=7)
    if chew < 0.14:                                                 # teeth skid off the Kevlar: two little scrape marks
        for k in (-1, 1):
            X.seg((tx + 18 * k - 8, ty - 30), (tx + 18 * k + 8, ty - 52), 4, (250, 250, 250))


# ------------------------------------------------------------------------------------------------- perspective sets
FOC = 4.0                                     # people at 0.8 scale stand 4 m from the lens
PXM = 537.0                                   # pixels per metre at 4 m


def proj(X, Y, d, vp):
    """A point X metres across, Y metres up, d metres away, on screen (vanishing point vp, eye 1.6 m up)."""
    k = PXM * FOC / max(d, 0.3)
    return (vp[0] + X * k, vp[1] + (1.6 - Y) * k)


def quad(X, pts, fill, line=True):
    X.d.polygon(pts, fill=fill)
    if line:
        X.d.line(pts + [pts[0]], fill=OUT, width=max(1, int(3 * B.SS)), joint='curve')


def screen_ctx(img):
    X = Ctx(ImageDraw.Draw(img), SCam(540, 960, 1.0, B.SS), ol=4)
    return X


# ---- shot 5: the alley, the wolf net
ALLEY_VP = (540, 760)
NET_D, NET_Y0, NET_Y1, ALLEY_W = 7.0, 1.15, 2.75, 1.4


NET_BAR = 3.2                                 # the rolled-up net hangs on a bar this high (metres): he runs under it
NET_FALL = 0.32                               # seconds from release to landing on the wolf


def first_tangle():
    """The moment (seconds into shot 5) the net lands on the wolf: as it reaches the spot under the bar."""
    return (19.5 - NET_D - 0.05) / 6.6


def alley_run(t):
    """(the man's depth, duck (none now); the wolf's depth, leap (none), pinned under the net) at time t (shot 5)."""
    u = t - SHOTS[4][1]
    man_d = 17.0 - 6.2 * u
    wolf_d = max(19.5 - 6.6 * u, NET_D + 0.05)
    return man_d, 0.0, wolf_d, None, u >= first_tangle(), u


def alley(img, t, only=None):
    vp = ALLEY_VP
    X = screen_ctx(img)
    W_ = ALLEY_W
    man_d, duck, wolf_d, leap, tangled, u = alley_run(t)
    if only is None:
        quad(X, [(0, 0), (1080 * B.SS, 0), (1080 * B.SS, 1920 * B.SS), (0, 1920 * B.SS)], (188, 200, 210), False)
        P = lambda x, y, d: tuple(v * B.SS for v in proj(x, y, d, vp))
        quad(X, [P(-W_, 0, 1.0), P(W_, 0, 1.0), P(W_, 0, 32), P(-W_, 0, 32)], (70, 66, 70))              # the ground
        quad(X, [P(-W_, 7, 32), P(W_, 7, 32), P(W_, 0, 32), P(-W_, 0, 32)], (214, 220, 212))           # the street beyond
        for sgn, col in ((-1, (150, 74, 56)), (1, (136, 66, 52))):                                    # brick walls
            quad(X, [P(sgn * W_, 0, 1.0), P(sgn * W_, 0, 32), P(sgn * W_, 9, 32), P(sgn * W_, 9, 1.0)], col)
            for k in range(1, 40):                                                                   # courses of brick
                y = k * 0.24
                X.d.line([P(sgn * W_, y, 1.0), P(sgn * W_, y, 32)], fill=B.dk(col, 0.8), width=max(1, B.SS))
            for d in (3, 5, 8, 12, 17, 24):
                X.d.line([P(sgn * W_, 0, d), P(sgn * W_, 9, d)], fill=B.dk(col, 0.8), width=max(1, 2 * B.SS))
        quad(X, [P(-W_, 0.0, 10.5), P(-W_ + 0.7, 0, 10.5), P(-W_ + 0.7, 1.1, 10.5), P(-W_, 1.1, 10.5)], (40, 90, 60))   # a bin
        X.d.line([P(W_, 0, 5.0), P(W_, 8, 5.0)], fill=(60, 60, 64), width=int(20 * B.SS))                          # drainpipe
        sx = P(-W_, 2.6, 5.4)                                                                        # the council sign
        quad(X, [P(-W_, 3.3, 5.0), P(-W_, 3.3, 6.0), P(-W_, 2.6, 6.0), P(-W_, 2.6, 5.0)], (236, 236, 228))
        sign_txt(img, ((P(-W_, 3.12, 5.5)[0]), P(-W_, 3.12, 5.5)[1]), 'WOLF NET', 30, (178, 24, 40))
        sign_txt(img, ((P(-W_, 2.82, 5.5)[0]), P(-W_, 2.82, 5.5)[1]), 'No. 4', 22, (40, 40, 46))
    things = [(NET_D, 'net'), (wolf_d + 0.01, 'wolf'), (man_d, 'man')]
    for d, what in sorted(things, reverse=True):              # furthest first
        if what == 'net' and only is None:
            net(img, X, t, tangled, u)
        elif what == 'man' and only in (None, 'man') and man_d > 1.3:
            alley_man(img, X, man_d, duck, u)                     # running at us; he ducks under the net
        elif what == 'wolf' and only in (None, 'wolf'):
            alley_wolf(X, wolf_d, leap, tangled, u)


def alley_wolf(X, wolf_d, leap, tangled, u):
    """The wolf behind him: bounding, then a leap at him, into the net."""
    if True:
        k = FOC / wolf_d
        gx, gy = proj(0.1, 0.0, wolf_d, ALLEY_VP)
        s = WOLF_S * k
        if tangled:
            struggle = u
            W.front(X, gx, gy, s * 0.92, 3, net=True, struggle=struggle, jaw=0.7 + 0.3 * math.sin(u * 9), seed=3)
        else:
            lift = 0.0 if leap is None else 330 * s * math.sin(min(1.0, leap) * math.pi * 0.5)
            W.front(X, gx, gy - lift, s, 3, run=(u * 2.6) % 1.0 if leap is None else None, leap=leap, seed=3)
        return


def sign_txt(img, xy, s, size, fill, font=None):
    f = ImageFont.truetype(font or B.ANTON, max(6, int(size * B.SS)))
    d = ImageDraw.Draw(img)
    d.text(xy, s, font=f, fill=fill, anchor='mm')


def alley_man(img, X, d, duck, u):
    k = FOC / d
    sc = S * k
    gx, gy = proj(-0.15 - 0.95 * max(0.0, (NET_D - d) / (NET_D - 1.3)), 0.0, d, ALLEY_VP)   # past the net he veers off
    sp = dict(MAN)
    rig = F.Rig(sp)
    ph = (u * 3.0) % 1.0                                           # three strides a second, arms pumping
    sw = math.sin(2 * math.pi * ph)
    def pump(side):                                                # elbows bent at his sides, hands pumping in turn:
        f = 0.5 + 0.5 * side * sw                                  # forward = fist up in front of his stomach,
        return (side * (175 - 115 * f), 360 - 210 * f)            # back = fist down by his hip
    sp['arms'] = {'L': rig.arm('L', pump(-1), 'fist', 'out', strict=False),
                  'R': rig.arm('R', pump(1), 'fist', 'out', strict=False)}
    sp['full'] = False
    sp.update(brows='alarm', lid=-2, mouth='v:AI', look=0.0, tilt=0.0)
    bob = 18 * abs(sw)                                             # up on each stride
    neck = gy - (F.SOLE_Y + bob) * sc
    cam = B.Cam(1.0, 540, 960)
    Xp = Ctx(ImageDraw.Draw(img), SCam(540, 960, 1.0, B.SS), ol=4)
    for side in (-1, 1):                                           # front-on stride: the lifted knee comes up and at us,
        up = max(0.0, -sw * side)                                  # its foot tucked under; the other leg drives down
        hip = (gx + side * 52 * sc, neck + 450 * sc)
        knee = (gx + side * 62 * sc, neck + (690 - 190 * up) * sc)
        foot = (gx + side * 58 * sc, neck + (F.SOLE_Y + bob - 10 - 230 * up) * sc)
        limb(Xp, hip, knee, 74 * sc, MAN['trousers'])
        limb(Xp, knee, foot, 58 * sc, MAN['trousers'])
        Xp.ell(foot[0], foot[1] + 4 * sc, 52 * sc, 24 * sc, (250, 250, 248))
    B.person(img, cam, gx, neck, sc, sp, u)
    city_shirt(img, cam, gx, neck, sc, sp)


def net(img, X, t, tangled, u):
    """The council wolf net: rolled up on a bar high across the alley; as the wolf comes under it, it unrolls, drops over
    the wolf and pins it to the ground, where it stays draped over it as the wolf thrashes."""
    vp = ALLEY_VP
    P = lambda x, y: proj(x, y, NET_D, vp)
    a, b = P(-ALLEY_W, NET_BAR + 0.08), P(ALLEY_W, NET_BAR + 0.08)
    X.seg(a, b, 14, (90, 90, 96))                                              # the bar
    rel = first_tangle() - NET_FALL
    col = (226, 214, 180)
    if u < rel:                                                                # rolled up, waiting
        ra, rb = P(-ALLEY_W + 0.05, NET_BAR - 0.08), P(ALLEY_W - 0.05, NET_BAR - 0.08)
        X.seg(ra, rb, 34, OUT)
        X.seg(ra, rb, 28, col)
        for k in range(1, 9):
            q = (ra[0] + (rb[0] - ra[0]) * k / 9, ra[1] + (rb[1] - ra[1]) * k / 9)
            X.seg((q[0] - 6, q[1] - 12), (q[0] + 6, q[1] + 12), 3, (170, 160, 130))
        return
    nx, ny = 16, 10
    s_ = WOLF_S * FOC / NET_D
    gx, gy = proj(0.1, 0.0, NET_D + 0.05, vp)
    kk = PXM * FOC / NET_D                                                     # pixels per metre at the net
    R, H = 255 * s_, 480 * s_                                                  # the dome it makes over the wolf
    f = min(1.0, (u - rel) / NET_FALL)                                         # falling and unrolling
    m = min(1.0, max(0.0, (u - first_tangle()) / 0.15))                        # settling into a drape
    m = m * m * (3 - 2 * m)
    wob = 0.0 if m < 1 else 8 * math.sin(u * 7.0)                              # tugged about as the wolf thrashes
    pts = {}
    for i_ in range(nx + 1):
        for j_ in range(ny + 1):
            uu, vv = -1 + 2 * i_ / nx, j_ / ny
            top_y = NET_BAR - (NET_BAR - H / kk) * f * f                       # the sheet's top falls to the wolf's back;
            sx, sy = P(uu * ALLEY_W * 0.9, max(0.0, top_y - vv * 2.6 * f))     # its hem stops on the ground (bunching)
            dome_top = gy - H * math.sqrt(max(0.0, 1 - uu * uu))
            dx = gx + uu * R * (1 + 0.45 * vv) + wob * (1 - vv)
            dy = dome_top * (1 - vv) + (gy + 6) * vv
            pts[i_, j_] = (sx + (dx - sx) * m, sy + (dy - sy) * m)
    for i_ in range(nx + 1):
        for j_ in range(ny):
            for di in (-1, 1):
                if 0 <= i_ + di <= nx:
                    X.seg(pts[i_, j_], pts[i_ + di, j_ + 1], 4, col)
    if tangled and m >= 1:                                                     # a paw shoved through the mesh
        w = math.sin(u * 7 - 1)
        X.ell(gx - (120 + 12 * w) * s_, gy - 120 * s_ - 30 * w * s_, 26 * s_, 18 * s_, W.PALS[3][0])


# ---- shot 20: running for it, filming himself over his shoulder
RUN_VP = (330, 820)
SMALL_CHASERS = (2, 4)


def run_scene(img, t, only=None):
    u = t - SHOTS[19][1]
    bob = 16 * abs(math.sin(u * math.pi * 3.0))                   # his running jolts the phone
    vp = (RUN_VP[0] + 10 * math.sin(u * 9.4), RUN_VP[1] - bob)
    X = screen_ctx(img)
    P = lambda x, y, d: tuple(v * B.SS for v in proj(x, y, d, vp))
    if only is None:
        quad(X, [(0, 0), (1080 * B.SS, 0), (1080 * B.SS, 1920 * B.SS), (0, 1920 * B.SS)], (188, 200, 210), False)
        quad(X, [P(-40, 0, 1.2), P(40, 0, 1.2), P(40, 0, 200), P(-40, 0, 200)], (176, 174, 168))              # pavement
        quad(X, [P(3.5, 0, 1.2), P(40, 0, 1.2), P(40, 0, 200), P(3.5, 0, 200)], (84, 84, 90))                 # the road
        quad(X, [P(-3.5, 0, 1.0), P(-3.5, 0, 200), P(-3.5, 9, 200), P(-3.5, 9, 1.0)], (176, 150, 128))       # shop fronts
        shift = (u * 6.0) % 7.0                                    # he runs away from them: they slide off into the distance
        cols = [(40, 70, 52), (86, 40, 128), (120, 116, 108), (40, 40, 46), (236, 170, 200)]
        for k in range(12):
            d0, d1 = 2.0 + k * 7.0 + shift, 2.0 + k * 7.0 + 6.4 + shift
            c = cols[k % len(cols)]
            quad(X, [P(-3.5, 0, d0), P(-3.5, 0, d1), P(-3.5, 3.4, d1), P(-3.5, 3.4, d0)], c)
            quad(X, [P(-3.5, 2.6, d0), P(-3.5, 2.6, d1), P(-3.5, 3.4, d1), P(-3.5, 3.4, d0)], B.dk(c, 0.7))
            if k % 5 == 0:
                for j in range(5):
                    dd = d0 + 0.6 + j * 1.15
                    X.d.line([P(-3.5, 3.6, dd), P(-3.5, 8.6, dd)], fill=(40, 32, 30), width=max(1, int(18 * B.SS * 4 / dd)))
        fronts = [(46, 92, 70), (176, 52, 48), (40, 56, 96), (210, 170, 60), (96, 60, 110)]
        for k in reversed(range(10)):                              # the far side of the road: brick terraces, lived in (note 31)
            d0 = 4.0 + k * 9.0 + shift
            brick = (150, 78, 60) if k % 2 else (140, 72, 56)
            Q = lambda a, b, y0, y1, c, ln=True: quad(X, [P(9.0, y0, d0 + a), P(9.0, y0, d0 + b), P(9.0, y1, d0 + b),
                                                          P(9.0, y1, d0 + a)], c, ln)
            Q(0, 8.6, 0, 8, brick)
            fr = fronts[(k * 3) % len(fronts)]
            Q(0.3, 8.3, 2.7, 3.4, fr)                              # the shop's fascia board
            Q(0.6, 5.6, 0.5, 2.5, (150, 176, 190))                 # its window
            Q(6.2, 7.6, 0.0, 2.4, B.dk(fr, 0.75))                  # its door
            for a in (0.9, 3.7, 6.5):                              # sash windows upstairs, white frames
                Q(a, a + 1.4, 4.3, 6.2, (236, 232, 222))
                Q(a + 0.15, a + 1.25, 4.45, 6.05, (70, 80, 92) if (k + int(a)) % 3 else (150, 170, 184))
            Q(8.45, 8.6, 0.0, 8.0, (60, 60, 64), False)            # a drainpipe between houses
    # the five wolves, bounding after him, gaining; the leader leaps at the lens at the end
    if only in (None, 'wolves'):
        order = []
        for i in range(5):
            d = 15.5 - 3.4 * u + [0.0, 2.5, 4.0, 1.4, 5.5][i]
            x = [-0.9, 0.5, -0.3, -1.7, 1.0][i]
            order.append((d, i, x))
        for d, i, x in sorted(order, reverse=True):
            if d < 1.6:
                continue
            k = FOC / d
            gx, gy = proj(x, 0.0, d, vp)
            last = SHOTS[19][2] - t
            leap = None if not (i == 0 and last < 0.5) else 1.0 - last / 0.5
            small = i in SMALL_CHASERS                                 # two of the government's smaller wolves, scrambling
            size = WOLF_S * (0.6 if small else 1.0)                    # along on quicker, shorter strides
            rate = 3.6 if small else 2.4
            W.front(X, gx, gy, size * k * (1 + (leap or 0) * 0.8), i, run=(u * rate + 0.27 * i) % 1.0 if leap is None else None,
                    leap=leap, blood=0.7, seed=i * 13)


def run_andy(img, t):
    u = t - SHOTS[19][1]
    bob = 16 * abs(math.sin(u * math.pi * 3.0))
    cam = B.Cam(2.8, AX - 230 / 2.8, 900 - (40 - bob) / 2.8)
    sp = andy_sp(t, 20)
    rig = F.Rig(sp)
    # his phone arm reaches out to the lens and leaves the frame bottom left: the phone is the camera (note 29)
    sp['arms'] = dict(rig.pose('sides'), L=rig.arm('L', (-330, 400), 'fist', 'out', 0.0, strict=False))
    wt = word_times(line_of(20))
    talking = sp['mouth'] != 'v:rest'
    if t < wt[1][1] + 0.1:                                         # "Aw fook": pissed off - brows driven down, teeth bared
        mode = 'angry'
    elif t < wt[3][1] or (t > line_of(20)['end'] and (u % 1.4) > 0.75):
        mode = 'terrified'                                         # "here come", and each glance back: terrified
    else:
        mode = 'stressed'                                          # to the lens between: haunted, sweating, grimacing
    shape = sp['mouth'][2:]
    opened = shape in ('AI', 'O', 'U', 'WQ', 'E', 'L')
    if mode == 'angry':                                            # shouting it, teeth bared (never a pucker or grin)
        sp.update(brows='fierce', lid=4, look=0.0, turn=0.0, tilt=-0.06)
        sp['mouth'] = 'shout' if talking and opened else 'v:etc'
    elif mode == 'terrified':                                      # gaping, the corners pulled down
        sp.update(brows='outrage', lid=-4, look=-0.95, turn=-0.3, tilt=0.02)   # back over his shoulder at them (note 30)
        sp['mouth'] = 'agape'                                      # never closes into a calm line
    else:                                                          # panicked: brows shot up, eyes wide, gritted teeth
        sp.update(brows='outrage', lid=-2, look=0.0, turn=0.0, tilt=-0.08, harrow=0.0)
        if not talking or shape == 'E':
            sp['mouth'] = 'hidden'                                 # the grimace is drawn below instead
    B.person(img, cam, AX, NECK, S, sp, t)
    if mode in ('stressed', 'terrified'):
        import peepee as PP
        p = B.Pen(img, PP.Rot(B.Local(cam, AX, NECK, S), sp.get('tilt', 0.0), pivot=(0, -60)))
        my = -150 + 60
        if mode == 'stressed':
            p.poly([(-30, my + 6), (-14, my - 2), (14, my - 2), (30, my + 6), (24, my + 16), (-24, my + 16)], (250, 250, 246), B.INK, 2.4)
            p.line([(-28, my + 7), (28, my + 7)], B.INK, 1.6)              # clenched teeth, top and bottom
            for k in (-14, 0, 14):
                p.line([(k, my), (k, my + 14)], B.INK, 1.2)
        for j_, (sx, sy) in enumerate(((ANDY['hw'] * 0.82, -195), (ANDY['hw'] * 0.9, -160))):   # sweat at his temple
            p.poly([(sx, sy - 14), (sx + 7, sy), (sx, sy + 6), (sx - 7, sy)], (170, 214, 236), B.INK, 1.8)


# ------------------------------------------------------------------------------------------------- frames
def picture(t):
    """The frame WITHOUT captions, title or the TikTok hints (they go on last)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    img = B.canvas((188, 200, 210))
    k = kind(t)
    if k == 'alley':
        alley(img, t)
        return img
    if k == 'run':
        run_scene(img, t)
        run_andy(img, t)
        return img
    ac, sc = cams(t)
    street(img, sc, t)
    if k == 'bigwolf':
        big_wolf(img, sc, t)
        return img
    if k == 'maul':
        return img
    if k == 'lady':
        the_lady(img, ac, t)
        biter(img, ac, t)                                  # in front of her arm: its jaws round the sleeve
        andy(img, ac, t, ANDY6_X)
        return img
    andy(img, ac, t)
    return img


def big_wolf(img, cam, t, alone=False):
    """Shot 4: a big dire wolf snarling on the pavement; on "smaller" it pops to 60% of its size, still snarling."""
    X = X_(img, cam)
    if not alone:
        X.rect(-40, -260, 40, 40, (40, 44, 48), r=10)                    # a bollard, for its size
        X.ell(0, -260, 40, 18, (40, 44, 48))
    s = WOLF_S * 1.15 * (0.6 if t >= POP else 1.0)
    jaw = 0.55 + 0.3 * max(0.0, filmkit.shifts(t, seed=41, amount=1.0, hold=(0.3, 0.6), move=0.08))
    W.side(X, 560, 40, s, -1, 1, jaw=jaw, snarl=1.0, seed=5, blink=(t % 2.9) < 0.1)


# ------------------------------------------------------------------------------------------------- overlay
def chunks(ln):
    """His caption style: a couple of words at a time, each chunk shown as it is said. A chunk closes at a comma or full
    stop, or once it has been on screen about 0.75 s (at most 4 words or 22 letters); a stray last word joins the one
    before, so nothing flashes by too fast to read."""
    words = ln['text'].split()
    wt = word_times(ln)
    out, cur = [], []
    for w, (a, b) in zip(words, wt):
        if cur:
            full = len(cur) >= 4 or len(' '.join([x[0] for x in cur] + [w])) > 22
            long_enough = a - cur[0][1] >= 0.75 and (len(cur) >= 2 or a - cur[0][1] >= 0.9)
            stop = cur[-1][0][-1] == '.' or (cur[-1][0][-1] == ',' and (len(cur) >= 2 or a - cur[0][1] >= 0.5))
            if full or stop or long_enough:
                out.append(cur)
                cur = []
        cur.append((w, a))
    if cur:
        if out and ln['end'] - cur[0][1] < 0.6 and len(' '.join(x[0] for x in out[-1] + cur)) <= 26:
            out[-1] += cur
        else:
            out.append(cur)
    return [(c[0][1], ' '.join(x[0] for x in c)) for c in out]


CAP_Y = {'mid': 1170, 'close': 1250, 'eyes': 1250, 'wide': 1000, 'lady': 1000, 'further': 1060, 'half': 1150,
         'bigwolf': 900, 'maul': 1250, 'alley': 1250, 'run': 1220}


def caption_at(t):
    for i, ln in enumerate(LINES):
        nxt = LINES[i + 1]['start'] - 0.05 if i + 1 < len(LINES) else 1e9
        if ln['start'] - 0.05 <= t < min(ln['end'] + 0.25, nxt):
            ch = chunks(ln)
            cur = ch[0][1]
            for a, txt in ch:
                if t >= a - 0.04:
                    cur = txt
            return cur.rstrip('.,')
    return None


def his_caption(img, s, y):
    """Andy's own caption look: TikTok Sans Bold, white, a soft dark shadow, centred."""
    SS = img.width // 1080
    f = ImageFont.truetype(CAP_FONT, 74 * SS)
    while f.getlength(s) > 640 * SS:
        f = ImageFont.truetype(CAP_FONT, int(f.size * 0.92))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((470 * SS, (y + 4) * SS), s, font=f, fill=(0, 0, 0, 200), anchor='mm')
    lay = lay.filter(ImageFilter.GaussianBlur(6 * SS))
    d = ImageDraw.Draw(lay)
    d.text((470 * SS, y * SS), s, font=f, fill=(255, 255, 255, 255), anchor='mm', stroke_width=max(1, SS),
           stroke_fill=(30, 30, 30, 90))
    img.alpha_composite(lay)


UI_FONT = os.path.join(HERE, 'fonts', 'TikTokSans-Medium.woff')
DESCRIPTION = 'Tough on wolves. Tough on the causes of wolves.'
COUNTS = ('94.2K', '4,817', '6,102', '11.9K')        # likes, comments, saves, shares (made up, like his real posts)


def _icon_heart(d, cx, cy, r, fill):
    pts = []
    for k in range(60):
        a = 2 * math.pi * k / 60
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + x * r / 17, cy + y * r / 17))
    d.polygon(pts, fill=fill)


def _icon_bubble(d, cx, cy, r, fill, dot):
    d.ellipse([cx - r, cy - r * 0.86, cx + r, cy + r * 0.86], fill=fill)
    d.polygon([(cx + r * 0.3, cy + r * 0.6), (cx + r * 0.85, cy + r * 1.05), (cx + r * 0.75, cy + r * 0.4)], fill=fill)
    for k in (-1, 0, 1):
        d.ellipse([cx + k * r * 0.42 - r * 0.12, cy - r * 0.12, cx + k * r * 0.42 + r * 0.12, cy + r * 0.12], fill=dot)


def _icon_bookmark(d, cx, cy, r, fill):
    d.polygon([(cx - r * 0.72, cy - r), (cx + r * 0.72, cy - r), (cx + r * 0.72, cy + r), (cx, cy + r * 0.5),
               (cx - r * 0.72, cy + r)], fill=fill)


def _icon_share(d, cx, cy, r, fill):
    d.polygon([(cx + r, cy - r * 0.05), (cx + r * 0.05, cy - r * 0.95), (cx + r * 0.05, cy - r * 0.45), (cx - r * 0.3, cy - r * 0.4),
               (cx - r * 0.85, cy + r * 0.1), (cx - r * 0.95, cy + r * 0.9), (cx - r * 0.5, cy + r * 0.35),
               (cx + r * 0.05, cy + r * 0.3), (cx + r * 0.05, cy + r * 0.85)], fill=fill)


_AVATAR = {}


def _avatar(size):
    """His account picture: the cartoon Andy, head and shoulders, in a white ring."""
    if size not in _AVATAR:
        keep = B.SS
        B.SS = 1
        im = B.canvas((108, 150, 96))
        sp = dict(ANDY, mouth='smile', look=0.0, brows='sincere', lid=2)
        sp['arms'] = F.Rig(sp).pose('sides')
        B.person(im, B.Cam(4.2, AX, NECK - 80), AX, NECK, S, sp, 0.0)
        B.SS = keep
        im = im.crop((540 - 300, 960 - 300, 540 + 300, 960 + 300)).resize((size, size), Image.LANCZOS)
        m = Image.new('L', (size, size), 0)
        ImageDraw.Draw(m).ellipse([0, 0, size - 1, size - 1], fill=255)
        im.putalpha(m)
        _AVATAR[size] = im
    return _AVATAR[size]


def tiktok_ui(img, t):
    """A TikTok screen over the film, always on, so there is no doubt it is his TikTok. Every piece sits just inside
    where the real app draws its own (search bar under the top tabs, buttons left of the real column, name and
    description above the real ones), so the viewer's own TikTok never covers ours completely."""
    SS = img.width // 1080
    F_ = lambda size, bold=True: ImageFont.truetype(CAP_FONT if bold else UI_FONT, int(size * SS))
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))                  # soft shadows first
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    for layer, col, off in ((sh, (0, 0, 0, 110), 2), (lay, (255, 255, 255, 255), 0)):
        d = ImageDraw.Draw(layer)
        o = off * SS
        # the search bar
        d.line([(62 * SS + o, 366 * SS + o), (84 * SS + o, 344 * SS + o)], fill=col, width=5 * SS)
        d.line([(62 * SS + o, 366 * SS + o), (84 * SS + o, 388 * SS + o)], fill=col, width=5 * SS)
        d.rounded_rectangle([118 * SS + o, 326 * SS + o, 1010 * SS + o, 406 * SS + o], radius=20 * SS, outline=col, width=3 * SS)
        d.ellipse([150 * SS + o, 348 * SS + o, 180 * SS + o, 378 * SS + o], outline=col, width=4 * SS)
        d.line([(176 * SS + o, 374 * SS + o), (190 * SS + o, 388 * SS + o)], fill=col, width=4 * SS)
        d.text((206 * SS + o, 366 * SS + o), 'Find related content', font=F_(38, False), fill=col, anchor='lm')
        d.line([(830 * SS + o, 342 * SS + o), (830 * SS + o, 390 * SS + o)], fill=col, width=2 * SS)
        d.text((990 * SS + o, 366 * SS + o), 'Search', font=F_(38), fill=col, anchor='rm')
        # the button column
        cx = 836 * SS + o
        _icon_heart(d, cx, 900 * SS + o, 40 * SS, col)
        _icon_bubble(d, cx, 1032 * SS + o, 38 * SS, col, (0, 0, 0, 0) if layer is sh else (150, 150, 150, 255))
        _icon_bookmark(d, cx, 1162 * SS + o, 34 * SS, col)
        _icon_share(d, cx, 1290 * SS + o, 38 * SS, col)
        for y, txt in zip((962, 1092, 1222, 1352), COUNTS):
            d.text((cx, y * SS + o), txt, font=F_(30), fill=col, anchor='mm')
        # his name, the tick, how long ago; the description; the progress bar
        name = HANDLE.lstrip('@')
        d.text((60 * SS + o, 1398 * SS + o), name, font=F_(42), fill=col, anchor='ls')
        nx = 60 * SS + d.textlength(name, font=F_(42)) + 14 * SS
        if layer is lay:
            d.ellipse([nx, 1366 * SS, nx + 30 * SS, 1396 * SS], fill=(32, 213, 236, 255))
            d.line([(nx + 8 * SS, 1381 * SS), (nx + 13 * SS, 1387 * SS), (nx + 23 * SS, 1374 * SS)], fill=(255, 255, 255), width=4 * SS)
        d.text((nx + 42 * SS + o, 1398 * SS + o), '· 1d ago', font=F_(36, False), fill=col if layer is sh else (210, 210, 210, 255), anchor='ls')
        d.text((60 * SS + o, 1452 * SS + o), DESCRIPTION, font=F_(34, False), fill=col, anchor='ls')
        d.text((60 * SS + o + d.textlength(DESCRIPTION + '  ', font=F_(34, False)), 1452 * SS + o), 'more', font=F_(34), fill=col, anchor='ls')
    d = ImageDraw.Draw(lay)
    u = min(1.0, t / BLACK_AT)
    d.rounded_rectangle([60 * SS, 1478 * SS, 1020 * SS, 1483 * SS], radius=3 * SS, fill=(255, 255, 255, 90))
    d.rounded_rectangle([60 * SS, 1478 * SS, (60 + 960 * u) * SS, 1483 * SS], radius=3 * SS, fill=(255, 255, 255, 230))
    d.ellipse([(60 + 960 * u - 7) * SS, 1473 * SS, (60 + 960 * u + 7) * SS, 1487 * SS], fill=(255, 255, 255, 255))
    av = _avatar(100 * SS)                                         # his account picture, with the red follow button
    ImageDraw.Draw(sh).ellipse([786 * SS, 718 * SS, 890 * SS, 822 * SS], fill=(0, 0, 0, 110))
    lay.alpha_composite(av, (786 * SS, 716 * SS))
    d.ellipse([786 * SS, 716 * SS, 886 * SS, 816 * SS], outline=(255, 255, 255), width=4 * SS)
    d.ellipse([815 * SS, 796 * SS, 857 * SS, 838 * SS], fill=(234, 40, 78))
    d.line([(826 * SS, 817 * SS), (846 * SS, 817 * SS)], fill=(255, 255, 255), width=5 * SS)
    d.line([(836 * SS, 807 * SS), (836 * SS, 827 * SS)], fill=(255, 255, 255), width=5 * SS)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4 * SS)))
    img.alpha_composite(lay)


def overlay(img, t):
    if t < BLACK_AT:
        tiktok_ui(img, t)
        c = caption_at(t)
        if c:
            his_caption(img, c, CAP_Y.get(kind(t), 1100))
        if t < TITLE_HOLD:
            B.title_lines(img, TITLE, **TITLE_AT, alpha=1.0 if t < TITLE_HOLD - 0.25 else max(0.0, (TITLE_HOLD - t) / 0.25))
    return img


def frame_image(t):
    return overlay(picture(t), t)


# ------------------------------------------------------------------------------------------------- sound
def soundtrack(stems=False):
    """Sam's voice only (every sound made in code was removed at his request)."""
    n = int((DUR + 0.3) * SR)
    voice = np.zeros(n)
    for ln in LINES:
        s_ = int(ln['start'] * SR)
        seg = ln['_voice'][:max(0, n - s_)]
        voice[s_:s_ + len(seg)] += seg
    rest = np.zeros(n)
    mix = voice.copy()
    end = int(BLACK_AT * SR)
    g = 10 ** ((-14.0 - MA.lufs(mix[:end])) / 20)                     # master: about -14 LUFS
    mix, voice = smooth_limit(mix * g, -2.6), voice * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


def smooth_limit(x, ceiling_db):
    """Keep the peaks under the ceiling without crackle (note 32): the old limiter changed the volume within 4 ms, riding
    the voice's own waves on every loud word. Here the volume eases down over 10 ms just ahead of a peak and recovers
    over about 150 ms."""
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    c, blk = 10 ** (ceiling_db / 20), int(0.001 * SR)
    nb = -(-len(x) // blk)
    a = np.abs(np.pad(x, (0, nb * blk - len(x)))).reshape(nb, blk).max(1)
    need = minimum_filter1d(np.minimum(1.0, c / np.maximum(a, 1e-9)), 21)    # 10 ms either side
    g, rel = need.copy(), 1 - math.exp(-1 / 150)
    for i in range(1, nb):
        g[i] = min(need[i], g[i - 1] + (1 - g[i - 1]) * rel)
    g = np.minimum(need, uniform_filter1d(g, 5))
    g = np.minimum(g, uniform_filter1d(g, 5))
    gs = np.interp(np.arange(len(x)), np.arange(nb) * blk + blk / 2, g)
    return np.clip(x * gs, -c, c)


def voices_reel(out):
    """All 20 lines back to back (half a second apart), as cleaned and matched for the film: for Sam to hear."""
    gap = np.zeros(int(0.5 * SR))
    x = np.concatenate([np.concatenate([v, gap]) for v in VOICES])
    x = x * 10 ** ((-16.0 - MA.lufs(x)) / 20)
    wav = out + '.wav'
    MA.write_wav(wav, M.limiter(x, -1.5))
    import imageio_ffmpeg
    import subprocess
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'aac', '-b:a', '160k', out],
                   check=True)
    os.remove(wav)


# ------------------------------------------------------------------------------------------------- checks
def checks():
    """Plan checks: subtitles printed to proofread, mouths move for every phrase, voice above the rest, title clear."""
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    print('Lines as written (the subtitles follow these words):')
    for ln in LINES:
        print(f"  {ln['n']:>2}. {ln['start']:6.2f}-{ln['end']:6.2f} s  {ln['text']}")
    windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches']]
    on_screen = [(a, b, s_) for a, b, s_ in TRACK if kind((a + b) / 2) not in ('maul', 'bigwolf', 'alley')]
    faults = E.check_mouths(on_screen, [w for w in windows if kind(sum(w) / 2) not in ('maul', 'bigwolf', 'alley')])
    mix, voice, rest = soundtrack(stems=True)
    faults += filmkit.voice_balance(voice, rest, SR, windows)
    faults += title_check()
    for q in filmkit.sound_questions({'voice': voice, 'background': rest, 'mix': mix}, SR,
                                     cuts=[s[1] for s in SHOTS[1:]], end=BLACK_AT):
        print('QUESTION FOR SAM:', q)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


def title_check():
    t = 1.0
    title = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
    B.title_lines(title, TITLE, **TITLE_AT)
    lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
    andy(lay, cams(t)[0], t)
    return filmkit.title_clear(title, {'Andy': lay})


def audits():
    """Each character alone over every frame they are on screen; every gesture on every frame; eyelines."""
    def layer():
        return Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))

    def draw_andy(t):
        lay = layer()
        k = kind(t)
        if k == 'run':
            run_andy(lay, t)
        else:
            andy(lay, cams(t)[0], t, ANDY6_X if k == 'lady' else AX)
        return lay

    def draw_wolf(i):
        def d(t):
            lay = layer()
            kill(lay, cams(t)[1], t, alone=i)
            return lay
        return d

    def draw_lady(t):
        lay = layer()
        the_lady(lay, cams(t)[0], t)
        return lay

    def draw_big(t):
        lay = layer()
        big_wolf(lay, cams(t)[1], t, alone=True)
        return lay

    def draw_alley(who):
        def d(t):
            lay = layer()
            alley(lay, t, only=who)
            return lay
        return d

    frames = lambda a, b: [i / FPS for i in range(int(math.ceil(a * FPS)), int(b * FPS))]
    actors = {}
    for key, a, b, i in SHOTS:
        if LINES[i]['shot'] not in ('maul', 'bigwolf', 'alley'):
            actors[f'Andy [{key}]'] = (frames(a, b), draw_andy)
    s2 = SHOTS[1]
    for i in range(5):
        actors[f'wolf {i + 1} [shot 2]'] = (frames(s2[1], s2[2]), draw_wolf(i))
    actors['the old lady [shot 6]'] = (frames(SHOTS[5][1], SHOTS[5][2]), draw_lady)
    actors['the big wolf [shot 4]'] = (frames(SHOTS[3][1], SHOTS[3][2]), draw_big)
    actors['the man [shot 5]'] = (frames(SHOTS[4][1], SHOTS[4][2]), draw_alley('man'))
    actors['the net wolf [shot 5]'] = (frames(SHOTS[4][1], SHOTS[4][2]), draw_alley('wolf'))
    allow = [('the big wolf [shot 4]', POP - 0.1, POP + 0.1, 'pops to 60% on "smaller": the joke'),
             ('the old lady [shot 6]', ARMOUR - 0.1, ARMOUR + 0.1, 'the armour appears in an instant: the joke'),
             ('the net wolf [shot 5]', SHOTS[4][1], SHOTS[4][2], 'bounding at us, growing as it comes; the leap'),
             ('the man [shot 5]', SHOTS[4][1], SHOTS[4][2], 'running at us, growing as he comes'),
             ('Andy [20-run]', SHOTS[19][1], SHOTS[19][2], 'running: the phone jolts every stride'),
             ('Andy [12-wide]', SHOTS[11][1], SHOTS[11][2], 'tiny in frame: the hand-held phone drift moves him a few pixels')]
    allow += [(f'wolf {i + 1} [shot 2]', s2[1], s2[2], 'bounding in and leaping on the man') for i in range(5)]
    allow += [(f'Andy [{k}]', a, a + 0.5, 'his gesture snaps into place at the cut') for k, a, b, i in SHOTS]
    filmkit.EYES.clear()
    faults = filmkit.silhouette_audit(actors, fps=FPS, allow=allow)
    faults += filmkit.check_eyelines()
    rig = F.Rig(ANDY)

    def rule_for(side, bend):
        def rule(target):
            el, wr = rig.arm(side, target, 'fist', bend, strict=False)[:2]
            sh = rig.shoulder(side)
            out = filmkit.check_joints({'sh': sh, 'el': el, 'wr': wr, 'head': (0, -150)},
                                       [('angle', 'sh', 'el', 'wr', 25, 180), ('apart', 'wr', 'head', 90)])
            return out
        return rule
    for n, g in GEST.items():
        for side, beats in g.items():
            if n == 15:
                continue                                   # the face-palm: his hand is meant to be on his face
            faults += beats.audit(rule_for(side, BEND.get(n, {}).get(side, 'out')), label=f'Andy line {n} {side} hand')
    return faults


# ------------------------------------------------------------------------------------------------- the sheets
def label(img, x, y, s, size=34):
    ImageDraw.Draw(img).text((x, y), s, fill=(20, 20, 20), font=ImageFont.truetype(CAP_FONT, size))


def tile(fn, bg=(232, 228, 220)):
    img = Image.new('RGBA', (1080, 1080), bg + (255,))
    fn(img)
    return img


def cast_sheet(out):
    """Everyone, and every view each one appears in: Andy, the man, the old lady (and in her armour, bitten), the five
    wolves, each wolf view (loping, leaping, feeding, coming at us, leaping at the lens, tangled in the net, the big one
    and its 60% self), the gore, and Andy's stress levels 1-6 for Sam to pick from."""
    B.SS = 1
    cols, size = 4, 540
    tiles = []

    def person_tile(draw, cam, lab):
        tiles.append((tile(lambda im: draw(im, cam)), lab))

    tc = lambda z, x, y: B.Cam(z, x, y + 420 / z)      # world (x, y) at the middle of a square tile
    person_tile(lambda im, c: andy(im, c, line_of(1)['start'] + 2.0), tc(0.85, AX, NECK + 330), 'Andy (Hope Again model)')
    person_tile(lambda im, c: the_man(im, c, 0.0), tc(0.85, MAN_X, -380), 'the man (Man City shirt)')
    person_tile(lambda im, c: the_lady(im, c, ARMOUR - 0.5, armour=False), tc(1.1, LADY_X, LADY_NECK + 260), 'the old lady')

    def armoured(im, c):
        biter(im, c, ARMOUR + 0.4)
        the_lady(im, c, ARMOUR + 0.4, armour=True)
    person_tile(armoured, tc(0.95, LADY_X - 230, LADY_NECK + 300), 'wolfproof armour, bitten')
    SX = lambda im: Ctx(ImageDraw.Draw(im), SCam(540, 960, 1.0, 1), ol=4)

    def wolves_lineup(im):
        X = SX(im)
        for i in range(5):
            W.side(X, 230 + 300 * (i % 3) + 150 * (i // 3), 470 + 400 * (i // 3), 0.85, 1, i, jaw=0.4, seed=i * 13)
    tiles.append((tile(wolves_lineup), 'the five wolves (each different)'))
    views = [('loping (side)', lambda X: W.side(X, 500, 760, 1.6, 1, 0, run=0.0, seed=0)),
             ('loping, half a stride on', lambda X: W.side(X, 500, 760, 1.6, 1, 0, run=0.5, seed=0)),
             ('the leap at the throat', lambda X: W.side(X, 470, 860, 1.5, 1, 3, leap=1.0, jaw=1.0, seed=39)),
             ('feeding: head down in it', lambda X: W.side(X, 560, 800, 1.6, -1, 2, feed=0.0, blood=0.7, seed=26)),
             ('feeding: a hunk ripped up', lambda X: W.side(X, 600, 900, 1.5, -1, 4, feed=1.0, blood=0.9, hunk=3, jaw=0.15, seed=52)),
             ('coming at us', lambda X: W.front(X, 540, 1000, 2.0, 0, run=0.2, seed=0)),
             ('leaping at the lens', lambda X: W.front(X, 540, 1080, 1.9, 1, leap=1.0, seed=13)),
             ('the big one, then 60% (shot 4)', lambda X: (W.side(X, 330, 800, 1.35, -1, 1, jaw=0.7, seed=5),
                                                           W.side(X, 830, 800, 0.81, -1, 1, jaw=0.7, seed=5)))]
    for lab, fn in views:
        tiles.append((tile(lambda im, fn=fn: fn(SX(im))), lab))

    def tangled(im):
        im2 = B.canvas((40, 36, 40))
        t = SHOTS[4][1] + first_tangle() + 0.8
        alley(im2, t)
        im.paste(im2.crop((0, 260, 1080, 1340)).convert('RGBA'), (0, 0))
    tiles.append((tile(tangled), 'tangled in the wolf net (shot 5)'))

    def gore(im):
        street(im, tc(0.62, MAN_X, -300), ATTACK + 6.0)
    tiles.append((tile(gore), 'the kill: flat red, the man hidden'))

    for i, lv in enumerate(LEVELS):
        def stress(im, i=i, lv=lv):
            global STRESS
            keep = STRESS
            STRESS = i + 1
            t = line_of(14)['start'] + 0.6
            andy(im, tc(3.6, AX, 885), t)
            STRESS = keep
        tiles.append((tile(stress, (214, 206, 196)), f'Andy stress {lv["name"]}'))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * size, rows * (size + 50) + 70), (250, 248, 244))
    label(sheet, 20, 14, 'CRY MINISTER: cast sheet. Pick Andy\'s stress number (shots 13-14) from the last row.', 36)
    for k, (im, lab) in enumerate(tiles):
        x, y = (k % cols) * size, 70 + (k // cols) * (size + 50)
        sheet.paste(im.convert('RGB').resize((size, size), Image.LANCZOS), (x, y))
        label(sheet, x + 12, y + size + 6, lab, 30)
    sheet.save(out, quality=90)


def key_times():
    """One still per shot, at its key moment (two for shot 4: before and after the pop)."""
    out = []
    for key, a, b, i in SHOTS:
        ln = LINES[i]
        n = ln['n']
        if n == 2:
            out.append((key, ATTACK + 1.9))
        elif n == 4:
            out += [(key + 'a', POP - 0.3), (key + 'b', POP + 0.4)]
        elif n == 5:
            out.append((key, a + first_tangle() + 0.6))
        elif n == 6:
            out.append((key, ARMOUR + 0.5))
        elif n == 20:
            out.append((key, b - 0.9))
        else:
            out.append((key, ln['start'] + 0.6 * (ln['end'] - ln['start'])))
    out[0] = ('1-mid', 1.2)
    return out


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        B.SS = 1
        cast_sheet(a[1])
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        todo = [(x, float(x)) for x in a[2:]] or key_times()
        for name, t in todo:
            frame_image(t).convert('RGB').save(os.path.join(a[1], f'{name}.jpg'), quality=88)
            print(name, f'{t:.2f} s')
    elif a[0] == 'voices':
        voices_reel(a[1])
    elif a[0] == 'times':
        for key, s0, s1, i in SHOTS:
            print(f'{key:12s} {s0:6.2f} - {s1:6.2f}')
        print('length', round(DUR, 2), 's')
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
