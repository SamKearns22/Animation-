#!/usr/bin/env python3
"""Bingo Bingo (working title): a TikTok satire short (1080 x 1920, 12 fps, about 40 s).

Green Party headquarters the night after losing the Holborn and St Pancras by-election: the office half-trashed,
leaflets on the floor, the victory-party sign falling off the wall. Zack Polanski stoops over a table, seething. His
advisor (Shaggy as a political operative: long scruffy hair, wispy goatee, lip ring, office clothes) walks in with an
A3 card held to his chest, its writing hidden. "Zionism IS racism!" "We know buddy, it's super racism." The card is
flipped: a list of new painful oversimplifications, rejected one by one, until the longest wins. Bingo bingo.

The series' look: burnham.py people, plain circle hands, figure.py arms (solved and guarded), mouths.py lip sync,
the standard captions. One set: every shot is the wide camera moved and zoomed (Part 2: the single is the two-shot
zoomed in), so the room never changes between shots. The table and everything on it come from one plan (TABLE_ITEMS).

Voices: Sam has not recorded yet, so each line is a stand-in made by espeak-ng (robotic, only for timing). When the
recordings arrive (name them by line key, e.g. `polanski-upset.m4a` in source/audio/), they replace the stand-ins
line by line and the whole film re-times itself to them.

    python3 source/polanski.py stills OUT.jpg             key frames on one sheet
    python3 source/polanski.py cast OUT.jpg               the cast in every view the film uses
    python3 source/polanski.py check                      plan checks, subtitles, sound questions and the audit
    python3 source/polanski.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT]
    python3 source/preflight.py polanski OUT_DIR          the series' checks and contact sheet
"""
import math
import os
import shutil
import subprocess
import sys
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import quick as Q            # noqa: E402  (circle hands, captions; installs mossad's brows/hair/tilt and mouths.py)
import figure as F           # noqa: E402
import mouths                # noqa: E402
import mossad as M           # noqa: E402
import mossad_audio as MA    # noqa: E402
import kit                   # noqa: E402
import filmkit               # noqa: E402  the satire checks: audit, eyelines, idle shifts, sound questions
import film_engine as E      # noqa: E402  render with the picture cache; captions put on last
from satire_style import limb, rough   # noqa: E402
from ed import INK, curve, oval, soft   # noqa: E402
from voices import syllables_in          # noqa: E402

FPS = 12
SR = MA.SR
SAFE = (60, 310, 900, 1500)
FY = 1420                                   # the floor line
S = 0.8                                     # both men's scale
NECK = FY - F.SOLE_Y * S                    # neck base height (677.6)
ZX, AX = 760, 300                           # Zack behind the table; where the advisor stops
DATA = os.path.join(HERE, 'data', 'polanski')

# ------------------------------------------------------------------------------------------------- the script
# key, who (Z = Zack, A = advisor), camera, gap before (s), the words as spoken, the caption pieces.
SCRIPT = [
    ('upset', 'A', 'wide', 0.25, "Zack, I know you're upset that everyone is mad at you about the conference motion",
     ["Zack, I know you're upset that everyone", "is mad at you about the conference motion—"]),
    ('zionism', 'Z', 'zack', 0.0, "Zionism IS racism!", ["Zionism IS racism!"]),
    ('know', 'A', 'adv', 0.35, "We know, buddy. It's super racism.", ["We know buddy, it's super racism."]),
    ('heads', 'A', 'zack', 0.3, "But don't worry, we've put our heads together",
     ["But don't worry, we've put our heads together"]),
    ('list', 'A', 'adv', 0.15, "and came up with a new list of painful oversimplifications that people might enjoy more.",
     ["and came up with a new list of painful", "oversimplifications", "that people might enjoy more."]),
    ('hear', 'Z', 'zack_pov', 0.9, "Alright. Let's hear it.", ["Alright, let's hear it."]),
    ('shoplift', 'A', 'flip', 1.4, "Okay. What do you think of, Shoplifting is Sexism.",
     ["Okay. What do you think of,", "Shoplifting Is Sexism."]),
    ('hmm', 'Z', 'zack', 0.6, "Hmmmmm.", ["Hmmm."]),
    ('no', 'Z', 'zack', 0.55, "No.", ["No."]),
    ('drill', 'A', 'card2', 1.0, "Alright. What about, North Sea Drilling is Ableism?",
     ["Alright. What about,", "North Sea Drilling Is Ableism?"]),
    ('absolutely', 'Z', 'zack', 0.4, "It absolutely is.", ["It absolutely is."]),
    ('notthat', 'Z', 'zack', 0.45, "But no, no. Not that.", ["But no, no, not that."]),
    ('well', 'A', 'adv_face', 0.45, "Okay, well.", ["Okay, well…"]),
    ('nuclear', 'A', 'card3', 0.35,
     "Focus groups really liked, Nuclear Proliferation is Inherent Violence Directed Towards Economically "
     "Disadvantaged Native Populations.",
     ["Focus groups really liked", "Nuclear Proliferation Is Inherent Violence", "Directed Towards Economically",
      "Disadvantaged Native Populations."]),
    ('bingo', 'Z', 'zack_bingo', 0.55, "Bingo! Bingo!", ["Bingo bingo!"]),
]
SHOUT = set()                                # Sam: the shout's caption as written, 'Zionism IS racism!' (no all-capitals)
# The stand-in voices: Zack in British English, the advisor slower and higher, an American drawl.
VOICE = {'Z': ['-v', 'en-gb', '-s', '200', '-p', '42'], 'A': ['-v', 'en-us', '-s', '163', '-p', '64']}   # Sam's pace
VOICE_LINE = {'zionism': ['-v', 'en-gb', '-s', '175', '-p', '58', '-a', '200'], 'hmm': ['-v', 'en-gb', '-s', '110', '-p', '36'],
              'list': ['-v', 'en-us', '-s', '128', '-p', '64'],    # the robot rushes short words: slowed to be readable
              'bingo': ['-v', 'en-gb', '-s', '190', '-p', '62', '-a', '180']}


def recording(key, who, words):
    """Sam's recording if it exists (source/audio/polanski-KEY.*), else an espeak-ng stand-in (cached)."""
    for ext in ('m4a', 'wav', 'mp3'):
        if os.path.exists(os.path.join(HERE, 'audio', f'polanski-{key}.{ext}')):
            return MA.line(f'polanski-{key}'), True
    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, f'standin-{key}.wav')
    if not os.path.exists(path):
        if not shutil.which('espeak-ng'):               # no voice at all: silence at Sam's pace
            return np.zeros(int(SR * max(1.0, len(words.split()) / 3.3))), False
        subprocess.run(['espeak-ng'] + VOICE_LINE.get(key, VOICE[who]) + ['-w', path, words], check=True)
    from burnham_film import load
    x = load(path)
    return x / (np.abs(x).max() + 1e-9) * 0.5, False


def build():
    """Place every line one after another (gap, then the words), from the recordings' own stretches of speech."""
    lines, t = [], 0.0
    for key, who, cam, gap, words, pieces in SCRIPT:
        x, real = recording(key, who, words)
        st = (MA.speech(x) if real else MA.pauses(x, 0.12)) or [(0.0, len(x) / SR)]
        start = t + gap
        off = start - st[0][0]
        end = off + st[-1][1]
        hop = SR // 100
        env = np.array([np.sqrt(np.mean(x[k:k + hop] ** 2)) for k in range(0, max(1, len(x) - hop), hop)])
        env = env / (env.max() + 1e-9)
        trk = [(a + off, b + off, s) for a, b, s in mouths.track(words, st, env, 100)]
        # each caption piece is on screen for its share of the syllables, counted over the speech only (not pauses)
        talk = sum(b - a for a, b in st)
        syl = [syllables_in(p) for p in pieces]

        def at(frac):
            need = frac * talk
            for a, b in st:
                if need <= b - a + 1e-9:
                    return off + a + need
                need -= b - a
            return end
        caps, k = [], 0
        for p, n in zip(pieces, syl):
            caps.append(dict(text=p, start=at(k / sum(syl)), end=at((k + n) / sum(syl))))
            k += n
        lines.append(dict(key=key, who=who, cam=cam, start=start, end=end, track=trk, caps=caps, x=x, off=off, st=st,
                          real=real))
        t = end
    return lines


LINES = build()
L = {ln['key']: ln for ln in LINES}
# shots: a new camera at each line whose camera differs from the one before; the cut lands just before the words
# (the interruption cuts on the shout itself)
SHOTS = []
for i, ln in enumerate(LINES):
    if i == 0:
        SHOTS.append([ln['cam'], 0.0, None])
    elif ln['cam'] != LINES[i - 1]['cam']:
        lead = 0.14 if ln['key'] == 'zionism' else min(0.6, (ln['start'] - LINES[i - 1]['end']) * 0.6)   # cut on his turn
        if ln['cam'] in ('flip', 'zack_pov'):
            lead = ln['start'] - LINES[i - 1]['end'] - 0.15        # these shots start at once: the turn, the flip
        cut = ln['start'] - lead
        prev = LINES[i - 1]
        if prev['cam'] != 'wide' and ln['key'] != 'zionism':
            cut = max(cut, min(ln['start'] - 0.1, prev['caps'][-1]['start'] + 1.05))   # the last caption gets 1 s to read
        SHOTS[-1][2] = cut
        SHOTS.append([ln['cam'], cut, None])
BLACK_AT = L['bingo']['end'] + 0.75
DUR = BLACK_AT + 0.35
SHOTS[-1][2] = BLACK_AT
# the long nuclear line is broken by a cut to Zack's face lighting up ("Directed Towards Economically"), then back
# to the card for the end of it (Part 2: no single shot much past 6-8 s; cut to the listener)
_c = L['nuclear']['caps']
REACT = (_c[2]['start'] - 0.1, _c[3]['start'] - 0.1)
CARD3_START = next(s[1] for s in SHOTS if s[0] == 'card3')
_i = next(i for i, s in enumerate(SHOTS) if s[0] == 'card3')
SHOTS[_i:_i + 1] = [['card3', SHOTS[_i][1], REACT[0]], ['zack_react', REACT[0], REACT[1]], ['card3', REACT[1], SHOTS[_i][2]]]
SHOTS = [tuple(s) for s in SHOTS]
TRACK = {w: [x for ln in LINES if ln['who'] == w for x in ln['track']] for w in 'ZA'}
CAPS = [dict(c, shout=ln['key'] in SHOUT, who=ln['who']) for ln in LINES for c in ln['caps']]

WALK_END = 2.5                              # the advisor reaches his spot
STRAIGHTEN = L['list']['end'] + 0.15        # Zack stands up and turns to him
FLIP = (L['shoplift']['start'] - 0.75, L['shoplift']['start'] - 0.2)   # the card turns over
SLAM = L['absolutely']['start'] + 0.42      # his fist on the table at "ab-SO-lutely"


def shot_at(t):
    for s in SHOTS:
        if s[1] <= t < s[2]:
            return s
    return SHOTS[-1]


def caption_at(t):
    for i, c in enumerate(CAPS):
        nxt = CAPS[i + 1]['start'] - 0.05 if i + 1 < len(CAPS) else 1e9
        if c['start'] - 0.05 <= t < min(max(c['end'] + 0.3, c['start'] + 1.0), nxt):   # at least 1 s to read
            if shot_at(t)[1] > c['end']:
                return None                   # never spill into the next shot
            return c['text']
    return None


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def mix(a, b, u):
    return a + (b - a) * u


def lerp2(p, q, u):
    return (p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u)


# ------------------------------------------------------------------------------------------------- the A3 card
CARD_W, CARD_H, CARD_CY = 250, 350, 300     # advisor's units: A3 portrait (297 x 420 mm; a head is about 23 cm)
ITEMS = [  # a real brainstorm sheet: each item in its own place, so a close frame holds only that one (Sam: reveal by
    # the camera's frame, never blur). (number, text, box as card fractions x0, y0, x1, y1)
    ('1.', 'SHOPLIFTING IS SEXISM', (0.04, 0.03, 0.45, 0.31)),
    ('2.', 'NORTH SEA DRILLING IS ABLEISM', (0.55, 0.06, 0.96, 0.36)),
    ('3.', 'NUCLEAR PROLIFERATION IS INHERENT VIOLENCE DIRECTED TOWARDS ECONOMICALLY DISADVANTAGED NATIVE '
           'POPULATIONS', (0.04, 0.64, 0.96, 0.98)),
]
ITEM_Z = 10.5                                # close enough that the frame holds item 1 or 2 alone (checked)
ITEM3_Z = 5.0                                # item 3 is read last: the whole card may show
_CARD = {}


def card_face():
    """The card's written side, drawn once at 2000 x 2800: green marker capitals, each item fitted to its own box."""
    if 'front' in _CARD:
        return _CARD['front']
    W, H = 2000, 2800
    im = Image.new('RGBA', (W, H), (250, 249, 244, 255))
    d = ImageDraw.Draw(im)
    for n, txt, (x0, y0, x1, y1) in ITEMS:
        bx0, by0, bx1, by1 = x0 * W, y0 * H, x1 * W, y1 * H
        size = 300
        while size > 40:                                             # the biggest marker size that fits its box
            f = ImageFont.truetype(B.ANTON, size)
            rows = B.wrap(txt, f, bx1 - bx0 - size * 0.9)
            wide = max(f.getbbox(r)[2] for r in rows)
            if len(rows) * size * 1.08 <= by1 - by0 and wide <= bx1 - bx0 - size * 0.9:   # every row inside its box
                break
            size -= 6
        top = (by0 + by1) / 2 - len(rows) * size * 1.08 / 2
        d.text((bx0, top), n, font=f, fill=(30, 110, 60))
        for i, r in enumerate(rows):
            d.text((bx0 + size * 0.9, top + i * size * 1.08), r, font=f, fill=(22, 90, 48))
    d.line([(W * 0.5, H * 0.05), (W * 0.5, H * 0.4)], fill=(150, 196, 160), width=8)    # marker rules between items
    d.line([(W * 0.05, H * 0.5), (W * 0.95, H * 0.49)], fill=(150, 196, 160), width=8)
    _CARD['front'] = im
    back = Image.new('RGBA', (1000, 1400), (214, 196, 160, 255))     # the plain card back (grey-brown board)
    db = ImageDraw.Draw(back)
    for k in range(0, 1400, 46):
        db.line([(0, k), (1000, k + 8)], fill=(204, 186, 150), width=3)
    _CARD['back'] = back
    return im


def item_at(k, fx=0.5, fy=0.5):
    """World point of item k (0-2) on the card held at the advisor's spot, fx/fy across its box."""
    x0, y0, x1, y1 = ITEMS[k][2]
    cx = -CARD_W / 2 + CARD_W * (x0 + (x1 - x0) * fx)
    cy = CARD_CY - CARD_H / 2 + CARD_H * (y0 + (y1 - y0) * fy)
    return AX + cx * S, NECK + cy * S


def item_cam(k):
    """The close-up on item k: its middle at screen y 700 (clear of the captions)."""
    z = ITEM3_Z if k == 2 else ITEM_Z
    x, y = item_at(k)
    if k == 2:
        x = AX
    return z, x, y + (960 - 700) / z


def flip_angle(t):
    """0 = the back towards us (writing hidden), pi = the writing towards us. The card turns over its long axis."""
    return math.pi * ease((t - FLIP[0]) / (FLIP[1] - FLIP[0]))


def draw_card(img, Lc, t, lift):
    """The card between the advisor's hands (Lc: his local frame), turned by flip_angle (squashed top to bottom)."""
    front = card_face()
    a = flip_angle(t)
    k = abs(math.cos(a))
    if k < 0.04:
        return
    face = front if a > math.pi / 2 else _CARD['back']
    cy = CARD_CY - lift
    x0, y0 = Lc.P(-CARD_W / 2, cy - CARD_H / 2 * k)
    x1, y1 = Lc.P(CARD_W / 2, cy + CARD_H / 2 * k)
    w, h = int(round(x1 - x0)), int(round(y1 - y0))
    if w < 2 or h < 2:
        return
    tile = face.resize((w, h), Image.LANCZOS)
    if a > math.pi / 2:                                               # the writing side, seen as it comes round
        pass
    img.alpha_composite(tile, (int(round(x0)), int(round(y0))))
    p = B.Pen(img, Lc)
    p.poly([(-CARD_W / 2, cy - CARD_H / 2 * k), (CARD_W / 2, cy - CARD_H / 2 * k), (CARD_W / 2, cy + CARD_H / 2 * k),
            (-CARD_W / 2, cy + CARD_H / 2 * k)], None, INK, 2.6)
    if 0.04 < k < 0.6:                                                # the edge catching the light as it turns
        soft(img, Lc, [(-CARD_W / 2, cy - 6), (CARD_W / 2, cy - 6), (CARD_W / 2, cy + 6), (-CARD_W / 2, cy + 6)],
             (255, 255, 255), 0.35 * (1 - k), 3)


# --------------------------------------------------------------------------------------- hands and features
def gesture_hand(p, el, wr, shape, skin, extra=None, t=0.0):
    """Every hand is a plain circle. One named exception: the finger guns at the end need a finger to read, so
    shape 'gun' adds a short finger and a thumb nub to the circle (a deliberate, scripted break of the rule)."""
    d = (wr[0] - el[0], wr[1] - el[1])
    n = math.hypot(*d) or 1.0
    u = (d[0] / n, d[1] / n)
    c = (wr[0] + u[0] * 12, wr[1] + u[1] * 12)
    if shape == 'gun':
        tip = (c[0] + u[0] * 58, c[1] + u[1] * 58)
        p.line([c, tip], INK, 23)
        p.line([c, tip], skin, 16)
        side = (-u[1], u[0]) if u[0] < 0 else (u[1], -u[0])          # the thumb points up
        if side[1] > 0:
            side = (-side[0], -side[1])
        th = (c[0] + side[0] * 34, c[1] + side[1] * 34)
        p.line([c, th], INK, 19)
        p.line([c, th], skin, 12)
    Q.chand(p, c[0], c[1], skin)


B.gesture_hand = gesture_hand
F.HAND['gun'] = 66

_beard, _mouth, _torso = B.beard, B.mouth, B.torso


def beard(p, sp, hx, hy, hw, hh, fx):
    if sp.get('beard') == 'short':
        return short_beard(p, sp, hx, hy, hw, hh, fx)
    if sp.get('beard') != 'goatee':
        return _beard(p, sp, hx, hy, hw, hh, fx)
    c = sp.get('beard_c', (120, 84, 48))
    # a wispy chin tuft and a thin drooping moustache (Shaggy's, evoked)
    p.poly(curve([(fx - 24, hy + hh * 0.86), (fx + 24, hy + hh * 0.86), (fx + 16, hy + hh * 1.14), (fx + 4, hy + hh * 1.34),
                  (fx - 6, hy + hh * 1.3), (fx - 18, hy + hh * 1.1)], 4), c, INK, 2.0)
    for k in range(4):
        x = fx - 12 + 8 * k
        p.line([(x, hy + hh * 1.0), (x + 1, hy + hh * 1.2 - abs(k - 1.5) * 6)], B.dk(c, 0.75), 1.4)
    p.line([(fx - 30, hy + 58), (fx - 14, hy + 47), (fx + 14, hy + 47), (fx + 28, hy + 58)], c, 4.2)
    for sgn in (-1, 1):                                                # a few stray whiskers on the jaw
        p.line([(fx + sgn * 44, hy + 70), (fx + sgn * 47, hy + 80)], c, 1.6)
        p.line([(fx + sgn * 52, hy + 58), (fx + sgn * 56, hy + 67)], c, 1.6)


def blend(a, b, k):
    return tuple(int(round(x + (y - x) * k)) for x, y in zip(a, b))


def short_beard(p, sp, hx, hy, hw, hh, fx):
    """Zack's beard (from Sam's photos): short and light, salt and pepper, kept to a clean line across the cheeks, the
    skin showing through; a light moustache joining it round the mouth."""
    skin, c = sp['skin'], sp.get('beard_c', (120, 104, 92))
    fill = blend(skin, c, 0.55)
    edge = blend(skin, c, 0.85)
    pts = [(hx - hw - 1, hy + 18), (hx - hw * 0.98, hy + hh * 0.62), (hx - hw * 0.62, hy + hh * 1.06),
           (fx, hy + hh * 1.2), (hx + hw * 0.62, hy + hh * 1.06), (hx + hw * 0.98, hy + hh * 0.62),
           (hx + hw + 1, hy + 18), (hx + hw * 0.84, hy + 56), (hx + hw * 0.6, hy + 70), (fx + 26, hy + 74),
           (fx, hy + 78), (fx - 26, hy + 74), (hx - hw * 0.6, hy + 70), (hx - hw * 0.84, hy + 56)]
    p.poly(curve(pts, 5), fill, edge, 1.6)
    p.poly(curve([(fx - 28, hy + 56), (fx - 8, hy + 49), (fx + 8, hy + 49), (fx + 28, hy + 56), (fx + 18, hy + 57),
                  (fx - 18, hy + 57)], 4), fill, edge, 1.2)
    rng = np.random.default_rng(12)                                    # a hint of texture: short fine hairs, some grey
    for _ in range(46):
        a = rng.uniform(0.2, math.pi - 0.2)
        r = rng.uniform(0.6, 0.95)
        x, y = fx + hw * 0.92 * r * math.cos(a), hy + 40 + hh * 0.74 * r * math.sin(a)
        if abs(x - fx) < 34 and hy + 44 < y < hy + 78:
            continue                                                   # keep the lips clear
        p.line([(x, y), (x + 1.5, y + 5)], blend(fill, c, 0.6) if rng.random() < 0.65 else blend(fill, (225, 222, 216), 0.6), 1.1)


def mouth(p, sp, t, fx, my):
    _mouth(p, sp, t, fx, my)
    if sp.get('lip_ring'):                                             # a silver ring through the lower lip, off centre
        m = sp.get('mouth', '')
        low = {'v:AI': 16, 'v:O': 14, 'v:E': 9, 'v:U': 9, 'v:WQ': 8, 'v:L': 13}.get(m, 7)
        p.line(oval(fx + 13, my + low + 6, 6.5, 6.5, 20, -0.4, 2 * math.pi - 1.0), INK, 5.6)
        p.line(oval(fx + 13, my + low + 6, 6.5, 6.5, 20, -0.4, 2 * math.pi - 1.0), (214, 218, 228), 3.0)
        p.ell(fx + 18, my + low + 3, 1.6, 1.6, (255, 255, 255), None)


def torso(img, p, sp, t):
    _torso(img, p, sp, t)
    if sp.get('rosette'):                                              # a green rosette on the lapel (no emblem)
        x, y = -84, 120
        for k in range(2):
            p.poly([(x - 10 + 14 * k, y + 8), (x - 2 + 14 * k, y + 8), (x - 4 + 18 * k, y + 76), (x - 16 + 18 * k, y + 70)],
                   (30, 130, 60), INK, 1.8)
        p.ell(x, y, 26, 26, (40, 156, 72), INK, 2.0)
        for k in range(12):
            a = k * math.pi / 6
            p.line([(x + 12 * math.cos(a), y + 12 * math.sin(a)), (x + 24 * math.cos(a), y + 24 * math.sin(a))],
                   (24, 110, 50), 1.4)
        p.ell(x, y, 10, 10, (248, 248, 240), INK, 1.6)


_hair_front = B.hair_front


def hair_front(p, sp, hx, hy, hw, hh, fx):
    """'fade': Zack's hair (from Sam's photos): short dark top over a receding hairline, the sides clipped close and
    lighter (skin showing through), fading out above the ears."""
    if sp.get('hair') != 'fade':
        return _hair_front(p, sp, hx, hy, hw, hh, fx)
    c, skin = sp.get('hair_c', (72, 58, 48)), sp['skin']
    side = blend(skin, c, 0.42)
    for sgn in (-1, 1):                                                # the clipped sides
        p.poly(curve([(hx + sgn * hw, hy + 2), (hx + sgn * (hw + 2), hy - 40), (hx + sgn * hw * 0.9, hy - hh * 0.62),
                      (hx + sgn * hw * 0.66, hy - hh * 0.62), (hx + sgn * (hw - 10), hy - 30),
                      (hx + sgn * (hw - 6), hy + 2)], 4), side, None)
    top = [(hx - hw * 0.9, hy - hh * 0.58), (hx - hw * 0.76, hy - hh * 0.92), (hx - hw * 0.3, hy - hh * 1.06),
           (hx + hw * 0.3, hy - hh * 1.06), (hx + hw * 0.76, hy - hh * 0.92), (hx + hw * 0.9, hy - hh * 0.58),
           (hx + hw * 0.62, hy - hh * 0.66), (hx + hw * 0.4, hy - hh * 0.86),                  # receding temples
           (fx + 6, hy - hh * 0.74), (hx - hw * 0.4, hy - hh * 0.86), (hx - hw * 0.62, hy - hh * 0.66)]
    p.poly(curve(top, 4), c, INK, 2.2)
    for k in range(5):                                                 # a few strands brushed forward
        x = hx - hw * 0.5 + k * hw * 0.24
        p.line([(x, hy - hh * 1.04), (x + 8, hy - hh * 0.8)], B.dk(c, 0.7), 1.4)


B.beard, B.mouth, B.torso, B.hair_front = beard, mouth, torso, hair_front
_head_front, _torso_front = B.head, B.torso


def head(img, p, sp, t, hx, hy):
    """From behind (Zack facing the wall): ears, the back of the skull, his short dark top over the clipped, lighter
    back and sides, a crease at the nape. No face."""
    if not sp.get('back'):
        return _head_front(img, p, sp, t, hx, hy)
    hw, hh, skin = sp.get('hw', 72), sp.get('hh', 88), sp['skin']
    c = sp.get('hair_c', (72, 58, 48))
    for sgn in (-1, 1):
        if sgn < 0 and sp.get('back_turn', 0.0) > 0:
            continue                                  # the near ear is drawn moving round with the face, below
        p.poly(oval(hx + sgn * (hw + 2), hy + 6, 12, 22), skin, INK, 2.4)
    outline = B.head_outline(hx, hy, hw, hh, sp.get('jaw', 'round'))
    p.poly(outline, skin, INK, 2.6)
    p.poly(curve([(hx - hw * 0.98, hy - 30), (hx - hw, hy + 20), (hx - hw * 0.8, hy + hh * 0.62), (hx, hy + hh * 0.74),
                  (hx + hw * 0.8, hy + hh * 0.62), (hx + hw, hy + 20), (hx + hw * 0.98, hy - 30), (hx, hy - hh * 0.5)], 4),
           blend(skin, c, 0.42), None)                                  # the clipped back and sides
    p.poly(curve([(hx - hw * 0.96, hy - hh * 0.5), (hx - hw * 0.8, hy - hh * 0.92), (hx, hy - hh * 1.06),
                  (hx + hw * 0.8, hy - hh * 0.92), (hx + hw * 0.96, hy - hh * 0.5), (hx + hw * 0.5, hy - hh * 0.1),
                  (hx, hy), (hx - hw * 0.5, hy - hh * 0.1)], 4), c, None)          # the longer top
    bt = sp.get('back_turn', 0.0)
    if bt > 0:                                       # turning to the left (the advisor's side): cheek, beard, nose come round
        w = hw * 0.5 * bt
        p.poly(curve([(hx - hw * 0.99, hy - hh * 0.35), (hx - hw + w, hy - hh * 0.4), (hx - hw + w * 1.15, hy + hh * 0.4),
                      (hx - hw + w * 0.8, hy + hh * 1.0), (hx - hw * 0.8, hy + hh * 0.86), (hx - hw * 0.99, hy + 10)], 4),
               skin, None)
        p.poly(curve([(hx - hw * 0.99, hy + 22), (hx - hw + w * 1.1, hy + 26), (hx - hw + w * 0.85, hy + hh * 1.02),
                      (hx - hw * 0.82, hy + hh * 0.88)], 4), blend(skin, sp.get('beard_c', (112, 96, 86)), 0.55), None)
        p.line([(hx - hw + w * 0.2, hy - hh * 0.38), (hx - hw + w * 0.9, hy - hh * 0.42)], sp.get('brow_c', INK), 3.2)
        if bt > 0.45:                                # the tip of his nose past the outline
            p.poly([(hx - hw + 2, hy - 2), (hx - hw - 12 * bt, hy + 24), (hx - hw + 2, hy + 34)], skin, INK, 2.0)
        p.poly(oval(hx - hw - 2 + hw * 0.42 * bt, hy + 6, 12, 22), skin, INK, 2.4)       # the near ear, moving round
    p.poly(outline, None, INK, 2.6)
    p.line([(hx - 18, hy + hh * 0.95), (hx, hy + hh * 0.9), (hx + 18, hy + hh * 0.95)], B.dk(skin, 0.8), 1.8)


def torso(img, p, sp, t):
    """From behind: the jacket's back with its centre seam and vent, the white shirt collar above it."""
    if not sp.get('back'):
        return _torso_front(img, p, sp, t)
    sw, bottom, skin, jc = sp.get('shoulders', 150), sp.get('bottom', 560), sp['skin'], sp.get('jacket', (36, 38, 48))
    p.poly([(-32, -80), (32, -80), (36, 10), (-36, 10)], skin, INK, 2.6)
    p.poly([(-40, -4), (-sw * 0.8, 12), (-sw, 50), (-sw - 6, 200), (-sw + 6, bottom), (sw - 6, bottom), (sw + 6, 200),
            (sw, 50), (sw * 0.8, 12), (40, -4)], jc, INK, 2.6)
    p.poly([(-40, -12), (40, -12), (44, 8), (-44, 8)], sp.get('shirt', (246, 246, 244)), INK, 2.0)   # shirt collar
    p.poly([(-44, 6), (44, 6), (40, 26), (-40, 26)], B.dk(jc, 0.85), INK, 2.0)                    # jacket collar
    p.line([(0, 26), (0, bottom - 110)], B.dk(jc, 0.7), 2.2)
    p.line([(0, bottom - 110), (0, bottom)], INK, 2.2)                                              # the vent
    soft(img, p.cam, [(-sw, 60), (-sw * 0.4, 30), (-sw * 0.5, bottom), (-sw, bottom)], (0, 0, 0), 0.22, 10)


B.head, B.torso = head, torso


# ------------------------------------------------------------------------------------------------ the cast
OLD_ZACK = dict(skin=B.OLIVE, hw=72, hh=94, jaw='square', hair='crop', hair_c=(38, 32, 28), brow_c=(34, 28, 24),
                brow_w=4.6, beard='trim', beard_c=(60, 50, 44), nose='long')   # the first animatic's Zack
ZACK = dict(name='Zack', skin=(240, 202, 176), hw=76, hh=92, jaw='round', hair='fade', hair_c=(78, 62, 50),
            brow_c=(84, 66, 54), brow_w=4.0, beard='short', beard_c=(112, 96, 86), nose='line', outfit='suit', jacket=(36, 38, 48),
            trousers=(36, 38, 48), shirt=(246, 246, 244), rosette=True, creases=1, full=True, pose='custom')
ADV = dict(name='advisor', skin=(244, 214, 190), hw=62, hh=96, jaw='long', hair='wavy', hair_c=(146, 100, 56),
           brow_c=(110, 76, 44), beard='goatee', beard_c=(130, 92, 52), lip_ring=True, outfit='suit',
           jacket=(112, 124, 72), shirt=(244, 244, 238), tie=(118, 82, 48), trousers=(122, 94, 60), shoulders=128,
           lanyard=True, lanyard_c=(40, 140, 70), full=True, pose='custom')
Z_BLINKS = F.blinks(3, 0.3, DUR, talking=True, per_min=(14, 20))
A_BLINKS = F.blinks(8, 0.3, DUR, talking=True)
TABLE = dict(x0=560, x1=1020, top=1035, depth=40)   # against the back wall: front edge at `top` (just below his hips)
TABLE_LOCAL_Y = (TABLE['top'] - TABLE['depth'] * 0.5 - NECK) / S   # Zack's units: the middle of the table top


def speaking(who, t, pad=0.12):
    return next((ln for ln in LINES if ln['who'] == who and ln['start'] - pad <= t < ln['end'] + pad), None)


def mouth_shape(who, t, rest='set'):
    sh = mouths.at(TRACK[who], t)
    return rest if sh == 'rest' else 'v:' + sh


def zack_state(t):
    """Zack, beat by beat: seething over the table; the shout; skeptical; the thinking hand; the slam; finger guns."""
    sp = dict(ZACK)
    zs, ze = L['zionism']['start'], L['zionism']['end']
    up = ease((t - (zs - 0.18)) / 0.22) - ease((t - (ze + 0.35)) / 0.5)          # arms flung up, then back down
    stand = ease((t - STRAIGHTEN) / 0.5)                                        # straightens up and turns to him
    hunch = 1 - stand
    if zs - 0.3 <= t < ze + 0.5:
        hunch *= 1 - 0.7 * min(up, 1)                                          # the shout lifts him out of the hunch
    sp['shoulder_dy'] = -14 * hunch
    sp['head_dy'] = 24 * hunch
    rig = F.Rig(sp)
    sh = {s: rig.shoulder(s) for s in 'LR'}
    table = {'L': (-196, TABLE_LOCAL_Y), 'R': (196, TABLE_LOCAL_Y)}            # hands planted on the table
    raised = {'L': (-215, -290), 'R': (215, -300)}
    hips = {s: rig.at('hip', s, dy=-40) for s in 'LR'}
    shape = {'L': 'fist', 'R': 'fist'}
    bend = {'L': 'out', 'R': 'out'}
    depth = {'L': 0.0, 'R': 0.0}
    over = set()                                                                # hands on the table: drawn over it
    if t < STRAIGHTEN:
        if up > 0:
            side_out = {'L': (-360, 110), 'R': (360, 110)}                  # out to the side on the way, never past
            tg = {s: (lerp2(table[s], side_out[s], up / 0.5) if up < 0.5 else    # the shoulder (no folded elbow)
                      lerp2(side_out[s], raised[s], (up - 0.5) / 0.5)) for s in 'LR'}
            shape = {'L': 'palm', 'R': 'palm'}
            if up < 0.3:
                over = {'L', 'R'}
        else:
            tg = dict(table)
            over = {'L', 'R'}
    else:
        tg = {s: lerp2(table[s], hips[s], stand) for s in 'LR'}
        if stand < 0.5:
            over = {'L', 'R'}
    # the thinking hand (Hmmm / No), the slam, the wave-off, the finger guns: the right hand (nearest the table's
    # free end) does the work; the left stays on the hip
    chin = (26, -36)                                                          # just under his chin
    h0, n1 = L['hmm']['start'] - 0.35, L['no']['end'] + 0.25
    if h0 <= t < L['absolutely']['start'] - 0.1:
        u = ease((t - h0) / 0.35)
        tg['R'] = lerp2(hips['R'], chin, u)
        shape['R'] = 'fist'
        bend['R'] = 'down' if u > 0.5 else 'out'                             # the elbow comes forward, towards us:
        depth['R'] = 0.45 * u                                                # fist under the chin, the thinker's pose
    a0 = L['absolutely']['start'] - 0.1
    if a0 <= t < L['notthat']['start'] - 0.1:
        lift = (250, -60)
        hit = (186, TABLE_LOCAL_Y)
        if t < SLAM - 0.08:
            u = ease((t - a0) / (SLAM - 0.08 - a0))
            tg['R'] = lerp2(chin, lift, u)
            bend['R'], depth['R'] = 'out', 0.45 * (1 - u)
        elif t < SLAM:
            tg['R'] = lerp2(lift, hit, (t - (SLAM - 0.08)) / 0.08)
            over.add('R')
        else:
            tg['R'] = hit
            over.add('R')
    nt0 = L['notthat']['start'] - 0.1
    if nt0 <= t < L['bingo']['start'] - 0.3:
        u = ease((t - nt0) / 0.3)
        wave = 14 * math.sin(2 * math.pi * 2.2 * (t - nt0))
        tg['R'] = lerp2((186, TABLE_LOCAL_Y), (sh['R'][0] + 120, sh['R'][1] + 190 + wave), u)
        shape['R'] = 'palm'
        if u < 0.4:
            over.add('R')
        if t > L['notthat']['end'] + 0.25:
            tg['R'] = lerp2(tg['R'], hips['R'], ease((t - L['notthat']['end'] - 0.25) / 0.4))
            shape['R'] = 'fist'
    b0 = L['bingo']['start'] - 0.3
    if t >= b0:
        u = ease((t - b0) / 0.25)
        kick = 0.0
        for ph in L['bingo']['st']:                                          # recoil on each "bingo"
            s0 = ph[0] + L['bingo']['off']
            if s0 <= t < s0 + 0.35:
                kick = 30 * math.sin(math.pi * (t - s0) / 0.35)
        tg['L'] = lerp2(hips['L'], (-330, 120 - kick), u)
        tg['R'] = lerp2(hips['R'], (-130, 225 - kick * 0.8), u)
        shape = {'L': 'gun' if u > 0.5 else 'fist', 'R': 'gun' if u > 0.5 else 'fist'}
        bend = {'L': 'down' if u > 0.6 else 'out', 'R': 'depth'}                                   # the right arm reaches across, towards us
    sp['arms'] = {s: rig.arm(s, tg[s], shape[s], bend[s], depth[s]) for s in 'LR'}
    sp['_over'] = over
    # the face
    look_adv = F.look_at(ZX, AX)
    if t < zs - 0.2:
        sp['brows'], sp['lid'], sp['look'] = 'fierce', 5, -0.15
        sp['mouth'] = 'set'
    elif t < ze + 0.4:
        sp['brows'], sp['look'] = 'fierce', -0.4
        sp['mouth'] = mouth_shape('Z', t, 'set')
    elif t < STRAIGHTEN:                                                     # back in the hunch, listening sideways
        sp['brows'], sp['lid'] = 'fierce', 4
        sp['look'] = F.saccade(t, [(0, 0.0), (L['heads']['start'] + 0.5, look_adv), (L['heads']['end'] + 0.4, -0.2),
                                   (L['list']['start'] + 1.2, look_adv)])
        sp['mouth'] = 'set'
    else:
        sp['look'] = look_adv
        sp['turn'] = -0.35 * stand
        sp['brows'] = 'confused'
        sp['mouth'] = mouth_shape('Z', t, 'set')
        if L['absolutely']['start'] - 0.1 <= t < L['notthat']['start']:
            sp['brows'] = 'fierce'
        elif L['notthat']['start'] <= t < L['bingo']['start'] - 0.3:
            sp['brows'] = 'sincere'
            sp['turn'] = -0.35 + 0.22 * math.sin(2 * math.pi * 2.0 * (t - L['notthat']['start'])) * \
                (1 - ease((t - L['notthat']['start'] - 0.9) / 0.3))          # "no, no": a shake of the head
        elif t >= L['bingo']['start'] - 0.3:
            sp['brows'] = 'joy'
            sp['mouth'] = mouth_shape('Z', t, 'smile')
        elif L['hmm']['start'] - 0.3 <= t < L['no']['start']:
            sp['look'] = -0.1                                                # gazing off, considering it
        elif REACT[0] - 0.4 <= t < L['bingo']['start'] - 0.3:               # the nuclear line: his face lights up
            sp['brows'] = 'wow'
            sp['mouth'] = 'smile' if t > REACT[0] + 0.5 else 'set'
    if t >= SPIN[1] and sp.get('look', 0) < -0.3:             # facing round and looking at the advisor (checked)
        filmkit.eyeline('Zack', t, (ZX, NECK - 150 * S), (sp['look'], 0.0), (AX, NECK - 150 * S))
    sp['blink'] = F.blinking(t, Z_BLINKS)
    sp['breath'] = F.breath(t, 2.6 if t < STRAIGHTEN else 4.0, 6 if t < STRAIGHTEN else 2.5)
    return sp


def adv_state(t):
    """The advisor: laid-back, half-lidded and sincere, holding the card in both hands."""
    sp = dict(ADV)
    rig = F.Rig(sp)
    lift = 0.0
    ls, le = L['list']['start'], L['list']['end']
    if ls + 0.3 <= t < le + 0.6:                                             # proud of the list: the card comes up
        lift = 22 * ease((t - ls - 0.3) / 0.4) * (1 - ease((t - le - 0.2) / 0.4))
    hy = CARD_CY - lift
    sp['arms'] = {'L': rig.arm('L', (-CARD_W / 2 + 6, hy), 'fist', 'depth'),
                  'R': rig.arm('R', (CARD_W / 2 - 6, hy), 'fist', 'depth')}
    sp['_lift'] = lift
    sp['lid'] = 3
    sp['brows'] = 'sincere'
    sp['look'] = F.look_at(AX, ZX)
    sp['turn'] = 0.12
    sp['tilt'] = 0.05 + filmkit.shifts(t, seed=2, amount=0.03)               # a loose head: held, small quick shifts
    sp['mouth'] = mouth_shape('A', t, 'smile' if t < L['zionism']['start'] else 'set')
    if L['know']['start'] <= t < L['know']['end']:                           # "we know, buddy": the nods
        sp['head_dy'] = 7 * abs(math.sin(math.pi * (t - L['know']['start']) / 0.45))
    if L['shoplift']['start'] - 0.2 <= t < L['shoplift']['end'] or L['drill']['start'] - 0.2 <= t < L['drill']['end'] \
            or L['nuclear']['start'] - 0.2 <= t < L['nuclear']['end']:      # reading off the card
        sp['lid'], sp['look'], sp['turn'] = 7, 0.1, 0.05
    if L['well']['start'] - 0.3 <= t < L['well']['end'] + 0.2:               # caught out: brows up, a glance down
        sp['brows'] = 'alarm'
        sp['lid'] = 2 if t < L['well']['start'] + 0.35 else 7
    sp['blink'] = F.blinking(t, A_BLINKS)
    sp['breath'] = F.breath(t, 4.2, 2.0, 0.3)
    if sp['look'] > 0.3:                                       # looking at Zack (checked: eyelines)
        filmkit.eyeline('advisor', t, (adv_x(t), NECK - 150 * S), (sp['look'], 0.0), (ZX, NECK - 150 * S))
    return sp


def adv_x(t):
    """He walks in from off the left of the frame and stops at his spot (slowing for the last step)."""
    x0, x1 = -170, AX
    if t >= WALK_END:
        return x1
    u = t / WALK_END
    k = 0.82                                    # constant speed, then ease into the stop
    pos = u / k * (1 - 0.18) if u < k else (1 - 0.18) + 0.18 * ease((u - k) / (1 - k)) * 1.0
    return x0 + (x1 - x0) * min(1.0, pos)


# --------------------------------------------------------------------------------------------- the camera
def camera(t):
    name, a, b = shot_at(t)
    u = (t - a) / max(0.1, b - a)
    head = NECK - 150 * S
    if name == 'wide':
        return B.Cam(1.0 + 0.04 * u, 540, 960 - 20 * u)
    if name in ('zack', 'zack_react'):
        return B.Cam(1.85, ZX, 735)
    if name == 'zack_pov':                                                     # his reaction, pushed in from the advisor's side
        return B.Cam(1.85 + 0.5 * ease(u), ZX - 20 * ease(u), 735 - 70 * ease(u))
    if name == 'zack_bingo':
        return B.Cam(1.85 + 0.12 * u, ZX, 735)
    if name == 'adv':
        return B.Cam(1.85 + 0.12 * u, AX, 760)
    if name == 'adv_face':
        return B.Cam(2.7, AX, head + 30)                                        # the card's top just below the caption
    # card close-ups: each item is revealed only when the frame moves onto it (Sam: by framing, never blur)
    one, two, three = item_cam(0), item_cam(1), item_cam(2)
    blend = lambda p, q, k: B.Cam(p[0] * (q[0] / p[0]) ** k, mix(p[1], q[1], k), mix(p[2], q[2], k))   # even zoom
    if name == 'flip':                                         # down from his face onto item 1, landing before the turn
        k = ease((t - a) / max(0.1, FLIP[0] - a))
        return blend((2.7, AX, head + 40), one, k)
    if name == 'card2':                                        # item 1, then across to item 2 as he says it
        return blend(one, two, ease((t - (L['drill']['caps'][1]['start'] - 0.35)) / 0.5))
    if name == 'card3':                                        # item 2, pulling out onto item 3 (the last: all may show)
        return blend(two, three, ease((t - (L['nuclear']['caps'][1]['start'] - 0.35)) / 0.6))   # at "Nuclear"
    raise KeyError(name)


# ------------------------------------------------------------------------------------------------ the set
WALL, WALL_D = (226, 228, 214), (196, 198, 184)
CARPET, CARPET_D = (124, 128, 128), (106, 110, 110)
GREEN, GREEN_D, GREEN_L = (46, 140, 72), (30, 104, 52), (120, 196, 120)
CORK, BOARD_W = (196, 150, 98), (248, 248, 246)
WOOD, WOOD_D = (190, 160, 118), (150, 122, 86)
# The wall plan (world units): every camera draws these, nothing moves between shots.
WALL_PLAN = {
    'whiteboard': (-60, 380, 210, 640),
    'cork board': (430, 360, 640, 640),
    'window': (830, 320, 1080, 800),
    'sign': (330, 230, 900, 300),
}


def box(p, x0, y0, x1, y1, f, lw=2.6, line=INK):
    """A hand-cut box (satire style: corners nudged a little, the same every frame; never ruler-straight)."""
    amt = min(6.0, 0.05 * min(abs(x1 - x0), abs(y1 - y0)))
    p.poly(rough([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], amt, int(x0 * 7 + y0 * 13) % 9973), f, line, lw)


def text(img, cam, x, y, s, size, fill, angle=0.0, font=None):
    import peepee as PP
    PP.ctext(img, cam, x, y, s, size, fill, font=font or B.ANTON, angle=angle)


def poster(img, p, cam, x, y, w, h, kind, angle=0.0):
    """A campaign poster: green with VOTE GREEN in white capitals (a generic sign, no party emblem)."""
    if kind == 'vote':
        box(p, x - w / 2, y - h / 2, x + w / 2, y + h / 2, GREEN, 2.2)
        text(img, cam, x, y - h * 0.16, 'VOTE', h * 0.26, (250, 250, 246))
        text(img, cam, x, y + h * 0.16, 'GREEN', h * 0.26, (250, 250, 246))
    else:                                                    # a constituency map, the target wards shaded
        box(p, x - w / 2, y - h / 2, x + w / 2, y + h / 2, (246, 246, 236), 2.2)
        rng = np.random.default_rng(4)
        for k in range(9):
            cx, cy = x - w * 0.32 + (k % 3) * w * 0.32, y - h * 0.3 + (k // 3) * h * 0.3
            pts = [(cx + rng.uniform(-14, 14) + w * 0.15 * math.cos(a), cy + rng.uniform(-10, 10) + h * 0.14 * math.sin(a))
                   for a in np.linspace(0, 2 * math.pi, 6, endpoint=False)]
            p.poly(pts, GREEN_L if k in (1, 4, 5) else (230, 230, 220), (120, 120, 120), 1.2)


def room(img, cam, t):
    p = B.Pen(img, cam)
    box(p, -600, -600, 1700, FY - 30, WALL, 0)
    box(p, -600, FY - 30, 1700, FY, WALL_D, 2.4)                               # skirting
    box(p, -600, FY, 1700, 2700, CARPET, 0)                                    # carpet tiles
    for x in range(-600, 1700, 120):
        p.line([(x, FY), (x - 40, 2700)], CARPET_D, 1.6)
    for y in (FY + 90, FY + 220, FY + 400):
        p.line([(-600, y), (1700, y)], CARPET_D, 1.6)
    # the window: a venetian blind, one slat hanging loose
    x0, y0, x1, y1 = WALL_PLAN['window']
    box(p, x0 - 14, y0 - 14, x1 + 14, y1 + 14, (238, 238, 232), 2.6)
    box(p, x0, y0, x1, y1, (34, 42, 62), 2.2)                                  # night outside
    for k, (lx, ly) in enumerate(((900, 420), (990, 560), (1040, 380), (930, 650))):
        p.ell(lx, ly, 4, 4, (250, 220, 140), None)                             # lit windows across the street
    for k in range(13):
        y = y0 + 16 + k * 36
        if k == 8:
            p.poly([(x0, y), (x0 + 60, y), (x1 - 20, y + 70), (x1 - 80, y + 74)], (236, 234, 222), INK, 1.6)
            continue
        box(p, x0, y, x1, y + 14, (236, 234, 222), 1.6)
    p.line([(x0 + 30, y0), (x0 + 30, y1 - 120)], (200, 200, 196), 2)
    # the whiteboard: the constituency, the count, and a graph that went the wrong way
    x0, y0, x1, y1 = WALL_PLAN['whiteboard']
    box(p, x0 - 10, y0 - 10, x1 + 10, y1 + 10, (180, 184, 190), 2.4)
    box(p, x0, y0, x1, y1, BOARD_W, 2.0)
    text(img, cam, (x0 + x1) / 2 + 10, y0 + 36, 'HOLBORN &', 30, (30, 60, 140), font=B.SANS)
    text(img, cam, (x0 + x1) / 2 + 10, y0 + 72, 'ST PANCRAS', 30, (30, 60, 140), font=B.SANS)
    for k, (hgt, c) in enumerate(((150, (150, 150, 160)), (120, (150, 150, 160)), (34, GREEN))):
        bx = x0 + 70 + 52 * k
        box(p, bx, y1 - 30 - hgt, bx + 36, y1 - 30, c, 1.6)
    p.line([(x0 + 60, y1 - 26), (x1 - 20, y1 - 26)], (30, 60, 140), 2.4)
    p.line([(x0 + 160, y1 - 76), (x0 + 196, y1 - 96)], (200, 40, 40), 2.4)     # a red arrow at the tiny green bar
    p.line([(x0 + 160, y1 - 76), (x0 + 170, y1 - 66)], (200, 40, 40), 2.4)
    # the cork board: posters, the map, rosettes, one poster torn down to a corner
    x0, y0, x1, y1 = WALL_PLAN['cork board']
    box(p, x0 - 10, y0 - 10, x1 + 10, y1 + 10, WOOD_D, 2.4)
    box(p, x0, y0, x1, y1, CORK, 2.0)
    poster(img, p, cam, 482, 452, 80, 112, 'vote')
    poster(img, p, cam, 585, 470, 92, 110, 'map')
    poster(img, p, cam, 490, 578, 70, 90, 'vote', 0.0)
    p.poly([(560, 548), (612, 548), (580, 590)], GREEN, INK, 1.6)              # all that's left of a torn poster
    for k in range(4):
        p.ell([462, 504, 548, 600][k], [384, 386, 388, 384][k], 4, 4, (200, 40, 40), INK, 1)   # drawing pins
    # the sign: VICTORY PARTY on sheets of paper taped to the wall; some have fallen (they're on the floor)
    x0, y0, x1, y1 = WALL_PLAN['sign']
    letters = 'VICTORY PARTY'
    fallen = {2, 5, 9, 12}
    step = (x1 - x0) / len(letters)
    for k, ch in enumerate(letters):
        if ch == ' ':
            continue
        cx = x0 + step * (k + 0.5)
        if k in fallen:
            p.poly([(cx - 4, y0 - 2), (cx + 6, y0 - 2), (cx + 6, y0 + 6), (cx - 4, y0 + 6)], (230, 226, 196), None)   # tape left
            continue
        tilt = [0.02, -0.04, 0, 0.05, -0.03, 0, 0.03, 0, -0.05, 0, 0.04, -0.02, 0][k]
        cy = (y0 + y1) / 2 + (18 if k == 10 else 0)
        pts = [(-step * 0.42, -32), (step * 0.42, -32), (step * 0.42, 32), (-step * 0.42, 32)]
        if k == 10:                                                           # hanging by one corner
            tilt = 0.5
        pts = [(cx + a * math.cos(tilt) - b * math.sin(tilt), cy + a * math.sin(tilt) + b * math.cos(tilt)) for a, b in pts]
        p.poly(pts, (252, 252, 248), INK, 1.6)
        text(img, cam, cx, cy - 2, ch, 44, GREEN_D, angle=tilt)
    # stacked boxes of undelivered leaflets, one open and spilling
    for k, (bx, by, bw, bh) in enumerate(((40, FY - 120, 170, 120), (52, FY - 230, 150, 110), (60, FY - 320, 130, 90))):
        kit.contact_shadow(img, cam, bx + bw / 2, by + bh, bw * 1.1) if k == 0 else None
        box(p, bx, by, bx + bw, by + bh, (196, 156, 104), 2.4)
        p.line([(bx, by + 18), (bx + bw, by + 18)], (170, 132, 86), 2)
    p.poly([(66, FY - 320), (40, FY - 352), (190, FY - 352), (190, FY - 320)], (210, 170, 116), INK, 2)   # open flap
    for k in range(5):
        p.poly([(80 + 18 * k, FY - 324), (114 + 18 * k, FY - 332 - 6 * (k % 2)), (118 + 18 * k, FY - 300), (84 + 18 * k, FY - 296)],
               GREEN if k % 2 else (246, 246, 240), INK, 1.2)
    # a VOTE GREEN placard leaning on the wall between them
    kit.contact_shadow(img, cam, 470, FY, 60)
    p.line([(468, FY), (500, FY - 200)], WOOD_D, 7)
    p.poly([(440, FY - 330), (560, FY - 316), (552, FY - 200), (432, FY - 214)], GREEN, INK, 2.2)
    text(img, cam, 497, FY - 290, 'VOTE', 40, (250, 250, 246), angle=0.11)
    text(img, cam, 495, FY - 244, 'GREEN', 40, (250, 250, 246), angle=0.11)
    # a tipped-over bin by the window wall, screwed-up paper rolling out
    kit.contact_shadow(img, cam, 1050, FY, 120)
    p.poly([(990, FY - 70), (1110, FY - 86), (1118, FY - 6), (1000, FY + 4)], (70, 74, 82), INK, 2.4)
    p.ell(993, FY - 33, 12, 38, (40, 42, 48), INK, 2)
    for bx, by in ((960, FY - 10), (930, FY + 14), (975, FY + 24)):
        p.ell(bx, by, 14, 12, (244, 244, 238), INK, 1.6)


LEAFLETS = []
_rng = np.random.default_rng(21)
for _ in range(34):                                          # leaflets and fallen sign sheets all over the floor
    LEAFLETS.append((_rng.uniform(-80, 1160), _rng.uniform(FY + 20, FY + 470), _rng.uniform(0, math.pi), _rng.random() < 0.55))


def floor_litter(img, cam):
    p = B.Pen(img, cam)
    for x, y, a, green in LEAFLETS:
        w, h = 44, 30
        pts = [(x + u * math.cos(a) - v * math.sin(a) * 0.45, y + u * math.sin(a) * 0.45 + v * math.cos(a) * 0.45)
               for u, v in ((-w, -h), (w, -h), (w, h), (-w, h))]
        p.poly(pts, GREEN if green else (246, 246, 240), INK, 1.4)
        if green:
            p.line([lerp2(pts[0], pts[3], 0.35), lerp2(pts[1], pts[2], 0.35)], (250, 250, 246), 2)
    for x, y, letter in ((620, FY + 120, 'T'), (880, FY + 60, 'Y')):            # two of the sign's fallen letters
        p.poly([(x - 34, y - 22), (x + 34, y - 26), (x + 36, y + 22), (x - 32, y + 24)], (252, 252, 248), INK, 1.6)
        text(img, cam, x, y, letter, 30, GREEN_D)
    for x, y in ((600, FY + 40), (990, FY + 160)):                             # deflated green balloons, string trailing
        p.poly(curve([(x - 30, y), (x - 10, y - 18), (x + 26, y - 12), (x + 30, y + 6), (x - 4, y + 12)], 4), GREEN, INK, 1.8)
        p.line([(x + 30, y + 4), (x + 60, y + 30), (x + 50, y + 70)], (80, 80, 80), 1.4)


# the table and everything on it (one plan; x from the table's left edge, depth 0 = front edge, 1 = back edge)
TABLE_ITEMS = {
    'laptop': (40, 150, 0.6),
    'leaflets': (190, 280, 0.35),
    'cup': (330, 370, 0.5),
    'cup tipped': (390, 450, 0.3),
}


def table(img, cam, t):
    p = B.Pen(img, cam)
    x0, x1, top, dp = TABLE['x0'], TABLE['x1'], TABLE['top'], TABLE['depth']
    for lx in (x0 + 26, x1 - 26):
        box(p, lx - 12, top, lx + 12, FY - 6, (150, 150, 156), 2.2)
        kit.contact_shadow(img, cam, lx, FY - 4, 50)
    p.poly([(x0 + 14, top - dp), (x1 - 14, top - dp), (x1, top), (x0, top)], WOOD, INK, 2.6)          # the top
    box(p, x0, top, x1, top + 22, WOOD_D, 2.6)                                                         # its front edge
    py = lambda d: top - dp * d
    a, b, d = TABLE_ITEMS['laptop']
    box(p, x0 + a, py(d) - 12, x0 + b, py(d) + 2, (90, 92, 100), 2)                                    # a closed laptop
    a, b, d = TABLE_ITEMS['leaflets']
    for k in range(4):
        box(p, x0 + a + 4 * k, py(d) - 6 - 6 * k, x0 + b - 6 + 2 * k, py(d) - 6 * k, GREEN if k % 2 else (246, 246, 240), 1.4)
    a, b, d = TABLE_ITEMS['cup']                                                                         # a coffee cup that jumps at the slam
    hop = 0.0 if t < SLAM else 22 * math.exp(-9 * (t - SLAM)) * abs(math.sin(14 * (t - SLAM)))
    cx = x0 + (a + b) / 2
    p.poly([(cx - 17, py(d) - 52 - hop), (cx + 17, py(d) - 52 - hop), (cx + 13, py(d) - hop), (cx - 13, py(d) - hop)],
           (246, 245, 241), INK, 2)
    p.poly([(cx - 19, py(d) - 60 - hop), (cx + 19, py(d) - 60 - hop), (cx + 18, py(d) - 51 - hop), (cx - 18, py(d) - 51 - hop)],
           (60, 60, 66), INK, 1.8)
    a, b, d = TABLE_ITEMS['cup tipped']                                                                  # one on its side, spilt
    soft(img, cam, oval(x0 + a + 10, py(d) + 4, 60, 9), (110, 74, 44), 0.7, 2)
    p.poly([(x0 + a, py(d) - 30), (x0 + b, py(d) - 24), (x0 + b, py(d)), (x0 + a, py(d) - 4)], (246, 245, 241), INK, 2)
    p.ell(x0 + a, py(d) - 17, 6, 14, (60, 60, 66), INK, 1.6)


def person_at(img, cam, x, sp, t, legs=None, flip=1.0):
    keep = B.legs
    if legs:
        B.legs = legs
    try:
        B.person(img, cam, x, NECK + sp.get('bob', 0.0), S, sp, t, flip)
    finally:
        B.legs = keep


TURN = (L['zionism']['start'] - 0.42, L['zionism']['start'] - 0.14)   # he starts to turn in the wide; cut on the action
SPIN = TURN                                    # (kept for older references)


def turn_at(t):
    """Cut on the action, the way live action and South Park hide a turn: in the wide he starts round (head first, his
    cheek, beard and ear coming into view, the shoulders narrowing a little as they rotate); the close-up picks him up
    already facing round, finishing the turn into the shout. Returns (back view?, head turn 0-1, body narrowing,
    extra face turn)."""
    if t < TURN[0]:
        return True, 0.0, 1.0, 0.0
    if t < TURN[1]:
        u = ease((t - TURN[0]) / (TURN[1] - TURN[0]))
        return True, u, 1.0 - 0.14 * u, 0.0
    u = ease((t - TURN[1]) / 0.25)
    return False, 0.0, 0.88 + 0.12 * u, -0.3 * (1 - u)


def zack(img, cam, t):
    sp = zack_state(t)
    back, bt, kx, extra = turn_at(t)
    sp['back'], sp['back_turn'] = back, bt
    sp['turn'] = sp.get('turn', 0.0) + extra
    kit.feet_shadow(img, cam, ZX, NECK, S)
    person_at(img, cam, ZX, sp, t, flip=kx)
    return sp


def advisor(img, cam, t):
    """The advisor walks in behind the desk in the foreground (it hides his legs: the walk is told by the body's bob and
    sway, the cheat Sam agreed until the new walking system exists), turned a little the way he walks, settling to face
    us as he stops. The card and his gripping hands go on top."""
    sp = adv_state(t)
    x = adv_x(t)
    if t < WALK_END:
        u = ease((t - (WALK_END - 0.5)) / 0.5)
        ph = 2 * math.pi * 1.0 * t                                     # two steps a second (Williams: a natural walk)
        sp['bob'] = -7 * abs(math.sin(ph)) * (1 - u)                  # highest as the legs pass, lowest on each contact
        sp['tilt'] = sp.get('tilt', 0.0) + 0.025 * math.sin(ph) * (1 - u)   # the weight going side to side
        sp['turn'] = mix(0.45, sp['turn'], u)
    kit.feet_shadow(img, cam, x, NECK, S)
    person_at(img, cam, x, sp, t)
    Lc = B.Local(cam, x, NECK + sp.get('bob', 0.0), S)
    draw_card(img, Lc, t, sp['_lift'])
    p = B.Pen(img, Lc)
    for side in 'LR':                                         # his hands over the card's edges: the grip
        el, wr, shape = sp['arms'][side][:3]
        B.gesture_hand(p, el, wr, shape, sp['skin'])


FG = dict(x0=-300, x1=590, top=1118)          # the desk nearest the camera (world units; its front runs off the frame)


def fg_desk(img, cam, t):
    """A campaign table in the near foreground, bottom left (green cloth to the floor, hiding the advisor's legs): a closed laptop, leaflets, a mug, a phone; everything on it
    lies low, so nothing rises in front of the advisor's card."""
    p = B.Pen(img, cam)
    x0, x1, top = FG['x0'], FG['x1'], FG['top']
    p.poly([(x0, top - 34), (x1 - 10, top - 34), (x1, top), (x0, top)], WOOD, INK, 3)                  # the wooden top
    # a campaign table: a green cloth draped over the front down to the floor, its folds and hem, a printed slogan
    cloth = [(x0, top - 4)] + [(x, top - 4 + 3 * math.sin(x * 0.05)) for x in range(int(x0) + 40, int(x1), 40)] + \
            [(x1 + 6, top - 4), (x1 + 14, 2700), (x0, 2700)]
    p.poly(cloth, GREEN, INK, 3)
    for k, x in enumerate(range(int(x0) + 70, int(x1), 95)):                                        # hanging folds
        p.line([(x, top + 10), (x + 6 * math.sin(k * 1.7), top + 300), (x - 4, 2700)], GREEN_D, 3)
    p.line([(x0, top + 18), (x1 + 8, top + 18)], GREEN_D, 2.4)                                      # the edge of the top
    box(p, 20, top + 70, 180, top + 170, (248, 248, 242), 2.6)                                      # the printed panel (left,
    text(img, cam, 100, top + 101, 'VOTE', 36, GREEN_D)                                                  # clear of the card's
    text(img, cam, 100, top + 140, 'GREEN', 36, GREEN_D)                                                 # close-ups)
    box(p, 10, top - 40, 190, top - 22, (70, 72, 80), 2.4)                                         # a closed laptop, flat
    p.ell(100, top - 31, 7, 5, GREEN, None)                                                         # its green sticker
    box(p, 470, top - 64, 516, top - 18, (246, 246, 240), 2.2)                                     # a mug (clear of the card)
    p.line(oval(524, top - 42, 12, 14, 16, -1.4, 1.4), INK, 3)
    box(p, 470, top - 52, 516, top - 40, GREEN, 0)
    for k in range(3):                                                                               # leaflets
        p.poly(rough([(250 + 6 * k, top - 22 - 5 * k), (350 + 4 * k, top - 24 - 5 * k), (354, top - 18 - 5 * k),
                      (246, top - 16 - 5 * k)], 2, k), GREEN if k % 2 else (246, 246, 240), INK, 1.4)
    box(p, 520, top - 24, 570, top - 16, (30, 30, 34), 1.6)                                         # a phone, face down


def scene(t, cam):
    img = B.canvas()
    room(img, cam, t)
    floor_litter(img, cam)
    table(img, cam, t)                        # the desk against the wall, behind him
    zack(img, cam, t)
    advisor(img, cam, t)
    fg_desk(img, cam, t)                      # the desk in the foreground, nearest the camera
    return img


def picture(t):
    """The frame without captions (they go on last, so a wording note never re-renders a picture)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    return scene(t, camera(t))


def overlay(img, t):
    c = caption_at(t) if t < BLACK_AT else None
    if c:
        Q.caption(img, c, next(x['shout'] for x in CAPS if x['text'] == c))
    return img


def frame_image(t):
    return overlay(picture(t), t)


# ---------------------------------------------------------------------------------------------------- sound
def sfx_steps(n, rng):
    """Soft shoe steps on carpet: a short muffled tap."""
    tt = np.arange(int(0.12 * SR)) / SR
    tap = rng.standard_normal(len(tt)) * np.exp(-tt * 60)
    tap = np.convolve(tap, np.ones(24) / 24, 'same') + 0.4 * np.sin(2 * np.pi * 90 * tt) * np.exp(-tt * 40)
    return tap * 0.5


def sfx_flip(rng):
    """The card turned over: a quick papery swish."""
    tt = np.arange(int(0.35 * SR)) / SR
    noise = rng.standard_normal(len(tt))
    hi = noise - np.convolve(noise, np.ones(6) / 6, 'same')
    return hi * np.sin(np.pi * tt / 0.35) ** 2 * 0.6


def sfx_thud(rng):
    """A fist on a wooden table, and the cup rattling."""
    tt = np.arange(int(0.6 * SR)) / SR
    thud = np.sin(2 * np.pi * (120 * np.exp(-tt * 9) + 50) * tt) * np.exp(-tt * 14)
    thud += 0.5 * np.sin(2 * np.pi * 330 * tt) * np.exp(-tt * 30) + 0.3 * rng.standard_normal(len(tt)) * np.exp(-tt * 70)
    clink = np.zeros(len(tt))
    for d in (0.06, 0.16, 0.23):
        k = int(d * SR)
        u = tt[:len(tt) - k]
        clink[k:] += 0.18 * np.sin(2 * np.pi * 2300 * u) * np.exp(-u * 50)
    return thud + clink


def place(mix_, seg, at):
    s = int(round(at * SR))
    if s >= len(mix_):
        return
    seg = seg[max(0, -s):]
    s = max(0, s)
    seg = seg[:len(mix_) - s]
    mix_[s:s + len(seg)] += seg


def soundtrack(total):
    n = int(total * SR)
    out = np.zeros(n)
    rng = np.random.default_rng(7)
    real = any(ln['real'] for ln in LINES)
    for ln in LINES:                    # the robot stand-ins set the timing only: Sam never hears them (14 Oct)
        if ln['real']:
            place(out, MA.gate(ln['x'], ln['st']), ln['off'])
    # footsteps: one at each foot contact of the walk
    step = 1 / 2.0
    k = 0.25
    while k < WALK_END - 0.1:
        place(out, sfx_steps(1, rng) * 0.35, k)
        k += step
    place(out, sfx_flip(rng) * 0.4, FLIP[0] + 0.05)
    place(out, sfx_thud(rng) * 0.8, SLAM)
    end = min(n, int(BLACK_AT * SR))
    if real:
        out, _ = MA.master(out, end)                           # -16 LUFS, levelled gently, never squashed past 3 dB
    else:
        out *= 0.35 / (np.abs(out).max() + 1e-9)               # effects only: at a natural level, not raised to voice loudness
    f = int(0.005 * SR)
    out[end - f:end] *= np.linspace(1, 0, f)                   # hard cut to black: picture and sound together
    out[end:] = 0
    return out


# ---------------------------------------------------------------------------------------------------- checks
def checks():
    """The plans don't collide; faces stay inside TikTok's safe area in every shot; hands planted on the table land
    on its top; the card's writing sits inside the safe area in its close-ups."""
    bad = []
    items = {k: (TABLE['x0'] + a, 0, TABLE['x0'] + b, 1) for k, (a, b, d) in TABLE_ITEMS.items()}
    F.check_apart('the table', items)
    F.check_apart('the wall', WALL_PLAN)
    B.SS = 1
    for name, a, b in SHOTS:
        for t in (a + 0.05, (a + b) / 2, b - 0.05):
            cam = camera(t)
            for who, x, hw in (('Zack', ZX, 72), ('advisor', adv_x(t), 62)):
                if name.startswith('card') or name == 'flip' and t > FLIP[0]:
                    continue
                X, Y = cam.P(x, NECK - 150 * S)
                r = hw * S * cam.z
                if X + r < 0 or X - r > 1080:
                    continue                                   # not in this shot
                if X - r < SAFE[0] or X + r > SAFE[2] or Y - r < SAFE[1] or Y + r > SAFE[3]:
                    bad.append(f'{name} {t:.2f} s: {who}\'s face leaves the safe area ({X:.0f}, {Y:.0f})')
    top = TABLE['top'] - TABLE['depth']
    y = NECK + TABLE_LOCAL_Y * S
    if not top <= y <= TABLE['top']:
        bad.append(f'Zack\'s planted hands ({y:.0f}) miss the table top ({top}-{TABLE["top"]})')
    for side in (-1, 1):
        if not TABLE['x0'] < ZX + side * 196 * S < TABLE['x1']:
            bad.append('Zack\'s hands are off the end of the table')
    for k in (0, 1):                                  # Sam: each item revealed by the frame alone (no other item in it)
        z, cx, cy = item_cam(k)
        f = (cx - 540 / z, cy - 960 / z, cx + 540 / z, cy + 960 / z)
        for j in range(3):
            (x0, y0), (x1, y1) = item_at(j, 0, 0), item_at(j, 1, 1)
            if j != k and min(f[2], x1) > max(f[0], x0) and min(f[3], y1) > max(f[1], y0):
                bad.append(f'the close-up on item {k + 1} also shows item {j + 1}')
    B.SS = 2
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    windows = [(ln['off'] + a, ln['off'] + b) for ln in LINES for a, b in ln['st']]
    bad += E.check_mouths(sorted(x for w in 'ZA' for x in TRACK[w]), windows)
    mix_ = soundtrack(DUR)
    for q in filmkit.sound_questions({'mix': mix_}, SR, cuts=[a for _, a, _ in SHOTS[1:]], end=BLACK_AT):
        print('QUESTION FOR SAM:', q)
    if bad:
        raise ValueError('; '.join(bad))


ALLOW = [  # deliberate: (who, from, to, why) for the audit
    ('Zack', TURN[0] - 0.1, TURN[1] + 0.35, 'the turn, cut on the action: back view to front across the cut'),
    ('Zack', L['zionism']['start'] - 0.25, L['zionism']['start'] + 0.15, 'arms flung up with the shout'),
    ('advisor', FLIP[0] - 0.1, FLIP[1] + 0.1, 'the card turning over (its outline squashes)'),
]


def audits():
    """The satire audit: each man drawn alone on every frame he is in shot (in pieces, popping, stretching, frozen),
    then the eyelines."""
    B.SS = 1

    def alone(fn):
        def draw(t):
            lay = Image.new('RGBA', (B.W, B.H), (0, 0, 0, 0))
            fn(lay, camera(t), t)
            return lay
        return draw

    def in_shot(t, x):
        X, _ = camera(t).P(x, NECK)
        return -100 < X < 1180
    actors = {}
    for who, fn, xf in (('Zack', zack, lambda t: ZX), ('advisor', advisor, adv_x)):
        for shot, a, b in SHOTS:
            ts = [i / FPS for i in range(int(math.ceil(a * FPS)), int(b * FPS)) if in_shot(i / FPS, xf(i / FPS))]
            if ts:
                actors[f'{who} [{shot} {a:.1f}s]'] = (ts, alone(fn))
    allow = [(n, a, b, why) for who, a, b, why in ALLOW for n in actors if n.startswith(who)]
    filmkit.EYES.clear()
    faults = filmkit.silhouette_audit(actors, fps=FPS, allow=allow)
    faults += filmkit.check_eyelines()
    return faults


# ---------------------------------------------------------------------------------------------------- output
def stills(out):
    B.SS = 2
    ts = [1.2, L['zionism']['start'] + 0.4, L['know']['start'] + 0.6, L['list']['start'] + 2.0, L['hear']['start'] + 0.4,
          FLIP[0] + 0.25, L['shoplift']['end'] - 0.3, L['hmm']['start'] + 0.3, L['drill']['end'] - 0.3, SLAM + 0.05,
          L['notthat']['start'] + 0.5, L['well']['start'] + 0.3, L['nuclear']['start'] + 2.5, L['nuclear']['end'] - 0.6,
          L['bingo']['start'] + 0.2, L['bingo']['end'] + 0.2]
    tiles = []
    for t in ts:
        im = frame_image(t).convert('RGB').resize((360, 640), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        d.text((10, 600), f'{t:.1f} s', font=ImageFont.truetype(B.SANS, 24), fill=(255, 255, 255), stroke_width=3,
               stroke_fill=(0, 0, 0))
        tiles.append(im)
    cols = 8
    sheet = Image.new('RGB', (cols * 370, ((len(tiles) + cols - 1) // cols) * 650), (20, 20, 20))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * 370, (i // cols) * 650))
    sheet.save(out, quality=88)
    print('stills:', out)


def cast(out):
    """The cast in every view the film uses (satire.md: Sam approves this): Zack from behind at the desk, mid-spin,
    shouting, thinking, delighted; the advisor walking in, standing with the card's back, and the card turned."""
    B.SS = 2
    views = [('Zack: at the desk', 'Z', 1.0), ('Zack: mid-spin', 'Z', SPIN[0] + 0.12), ('Zack: the shout', 'Z', L['zionism']['start'] + 0.3),
             ('Zack: thinking', 'Z', L['hmm']['start'] + 0.4), ('Zack: finger guns', 'Z', L['bingo']['start'] + 0.3),
             ('advisor: walking in', 'A', 1.2), ('advisor: card back', 'A', L['know']['start'] + 0.5),
             ('advisor: card turned', 'A', L['shoplift']['start'] + 0.5)]
    tiles = []
    for label, who, t in views:
        x = ZX if who == 'Z' else adv_x(t)
        cam = B.Cam(1.2, x, NECK + 330)
        img = B.canvas((226, 228, 214))
        (zack if who == 'Z' else advisor)(img, cam, t)
        im = img.convert('RGB').resize((360, 640), Image.LANCZOS).crop((30, 40, 330, 640))
        ImageDraw.Draw(im).text((10, 568), label, font=ImageFont.truetype(B.SANS, 20), fill=(30, 30, 30))
        tiles.append(im)
    sheet = Image.new('RGB', (4 * 306, 2 * 606), (40, 40, 40))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % 4) * 306, (i // 4) * 606))
    sheet.save(out, quality=90)
    print('cast sheet:', out)


def render(out, small=False, reuse=False, redo=()):
    t0 = time.time()
    E.render('polanski', out, size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
             picture=picture, overlay=overlay, shot_of=lambda t: shot_at(t)[0], sound=lambda: soundtrack(DUR),
             write_wav=MA.write_wav, set_ss=lambda v: setattr(B, 'SS', v), crf=24 if small else 20, reuse=reuse,
             redo=redo)
    print(f'render took {time.time() - t0:.0f} s')


def main():
    a = sys.argv[1:]
    if a and a[0] == 'times':
        for ln in LINES:
            print(f"{ln['key']:11s} {ln['who']} {ln['start']:6.2f}-{ln['end']:6.2f}  {ln['cam']}")
        for s in SHOTS:
            print(f'shot {s[0]:11s} {s[1]:6.2f}-{s[2]:6.2f} ({s[2] - s[1]:.1f} s)')
        print(f'black at {BLACK_AT:.2f} s')
        return
    if len(a) == 2 and a[0] == 'cast':
        cast(a[1])
        return
    if a and a[0] == 'check':
        checks()
        f = audits()
        print('\n'.join('AUDIT: ' + x for x in f) or 'audit: clean')
        return
    if len(a) < 2 or a[0] not in ('stills', 'final'):
        print(__doc__)
        return
    checks()
    if a[0] == 'stills':
        stills(a[1])
    else:
        render(a[1], small='--small' in a, reuse='--reuse' in a,
               redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else ())


F.guard(B)                    # every arm drawn is measured against the rig; a wrong one stops the render
import limbs                  # noqa: E402
limbs.install(B)              # the new arms and legs: one outline at the shoulder, smooth shaped legs (Cry Minister)

if __name__ == '__main__':
    main()
