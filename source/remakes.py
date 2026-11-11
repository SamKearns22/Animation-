#!/usr/bin/env python3
"""Remakes (the Ocarina of Time remake satire): the film file. Modelled on flying_whales.py (custom-drawn cast, no
burnham people): the sets are remakes_sets, the children and gunman remakes_cast, KG, Navi and the Goron
remakes_creatures. The simplest staging that tells each beat (Sam, 10 Nov: the week at 75%): holds and cuts, one
move per beat. Notes: notes/remakes.md ("Shots and the acting list").

MAP (rule 61)
  lines and timing ..... LINES (recording, who, shot, gap before); _time() lays them end to end; BEATS (the action
                         times: snap, gate, Navi, slam) come from the lines
  shots ................ SHOTS from the beats; shot_of(t)
  helpers .............. _talk (0-1 mouth open from the recording), _kid (a child or gunman, with talk, fall and
                         rotation), _prompt (the R1 / R2 button), _splat/_blast/_flash/_bits (flat effects)
  one function per shot  s1_branch .. s13_pinned; picture(t)
  sound ................ soundtrack(): voices with bleeps, the MG42, the neck crack, Navi's blast (Decision 6)
  subtitles ............ caption_at (drawn by finish.py: SUBTITLES_AT_FINISH)

    python3 source/remakes.py stills OUT_DIR T [T ...]
    python3 source/remakes.py check
    python3 source/remakes.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1] [--nostamp]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import mossad_audio as MA        # noqa: E402
import mouths                    # noqa: E402
import subtitles as SUB          # noqa: E402
import filmkit                   # noqa: E402
import film_engine as E          # noqa: E402
import views as V                # noqa: E402
import remakes_sets as RS        # noqa: E402
import remakes_cast as RC        # noqa: E402
import remakes_creatures as CR   # noqa: E402
from ed import INK               # noqa: E402

FPS, SR = 12, MA.SR
W, H = 1080, 1920

# =============================================== STORY ==============================================================
NAME = 'remakes'
TITLE = ()
HAS = {'voices', 'effects', 'props'}             # rule 58: custom-drawn cast (not burnham people), painted sets
CAST = {}
LOOKS_AT = {}
SUBTITLES_AT_FINISH = True
HOOK = ('Ocarina of Time, remade for 2026', {'y': 1150})   # below KG, over the near bush (at 352 it hid his face)
SWEARS_OK = []                                   # note 52 (11 Nov): "shit" bleeped too ("god-damn" heard)
# n, recording, who, text, shot, gap before (s), bleeps in the recording's own seconds (found from the sound: the
# f of the word and its vowel in the high band, 10 Nov)
_L = [
    (1, '01', 'kg', 'Hello, Link! Are you ready for a f****** adventure!', 'S1', 0.3, [(3.39, 3.56)]),   # note 43: just the "uck"
    (2, '02', 'link', 'Uh, yeah, I think so?', 'S2', 0.2, []),
    (3, '03', 'kg', "Great, here's some wisdom!", 'S3', 0.2, []),
    (4, '04', 'link', 'Ok?', 'S4', 0.2, []),
    (5, '05', 'kg', 'Press R1 for an EXECUTION MOVE.', 'S5', 0.45, []),
    (6, '06', 'link', 'Oh my god!', 'S6', 0.25, []),      # note 66: no beat of silence after the move
    (7, '07', 'kg', 'Clear enemy encampments to clear segments of the map.', 'S7', 0.9, []),
    (8, '08', 'link', "I don't think I can do this.", 'S7', 0.2, []),
    (9, '09', 'kg', 'R2 FOR GRENADES.', 'S7', 0.6, []),      # note 38: line 8's subtitle now reads for 2 s
    (10, '10', 'link', 'This is horrible.', 'S9', 1.75, []),
    (11, '11', 'kg', 'FIVE ROMANCE OPTIONS TO CHOOSE FROM', 'S10', 0.4, []),
    (12, '12', 'link', 'Um, I am 9 years old.', 'S11', 0.6, []),
    (13, '13', 'kg', "Now listen here, you s***. You're gonna grow up real f****** fast.", 'S12', 0.6,
     [(2.08, 2.40), (4.67, 4.94)]),                    # notes 43, 52: the "it" of shit; note 69: "ucki" (the
                                                       # u 4.68, the k gap 4.78, the i to 4.94; it sat on "in")
    (14, '13b', 'kg', "And you've got some god-damn CHOICES to make.", 'S12', 0.25, []),
    (15, '14', 'link', 'I want to go home.', 'S13', 0.45, []),
]
LINES = []
t = 0.0
for n, rec, who, text, shot, gap, bl in _L:
    v = MA.line('remakes-' + rec)
    ps = MA.pauses(v, 0.12)
    a0 = ps[0][0] - 0.06
    seg = MA.gate(v, ps)[int(a0 * SR):int((ps[-1][1] + 0.12) * SR)]
    start = t + gap
    ln = dict(n=n, who=who, text=text, shot=shot, start=start, end=start + len(seg) / SR, audio='remakes-' + rec,
              _voice=seg, _open=mouths.loudness_open(seg, SR), _stretches=[(a - a0, b - a0) for a, b in ps])
    ln['_dur'] = ln['end'] - ln['start']
    if bl:
        ln['bleep'] = [(start + b0 - a0, start + b1 - a0) for b0, b1 in bl]
        if len(bl) == 1:
            ln['bleep'] = ln['bleep'][0]
    LINES.append(ln)
    t = ln['end']
del t
L = {ln['n']: ln for ln in LINES}


def _voice_env(who):
    """The speaker's loudness per drawing over the whole film (for headlife)."""
    env = np.zeros(int(70 * FPS))
    n = SR // FPS
    for ln in LINES:
        if ln['who'] == who:
            v = ln['_voice']
            e = [np.sqrt(np.mean(v[i * n:(i + 1) * n] ** 2)) for i in range(len(v) // n)]
            i0 = int(round(ln['start'] * FPS))
            env[i0:i0 + len(e)] = e
    return env


import headlife                  # noqa: E402  (Job K rule, satire.md Look: heads tilt and nod on the voice)
HEAD_LIFE = HL = {'kg': headlife.HeadLife(_voice_env('kg'), 0.0, seed=5), 'link': headlife.HeadLife(_voice_env('link'), 0.0, seed=7)}

# the action beats, from the lines
SNAP = L[5]['start'] + 2.86                       # note 45: the snap ON "move" (its syllable beat in the take);
                                                  # the grip lands on "ex-" of "execution" (1.74 into the line)
GATE = L[6]['end'] + 0.3                          # S7 starts on the camp quiet, the gate shut
BLAST = GATE + 0.25                               # note 46: then the gate blows (3 frames of 'everything fine' first)
# the camp (note 32): KG storms in through the gate, shoots the tower lookout on his way, then the man who runs in
# lower left; Link scuttles in through the gate behind him; the last man comes in middle right
KG_T = (BLAST + 0.3, L[7]['start'] + 0.45, L[7]['start'] + 1.6, L[7]['start'] + 2.3)   # in, stop, on, at his mark
BURST1 = (L[7]['start'] + 0.5, L[7]['start'] + 1.55)             # up at the tower, from "enemy"
HIT1 = BURST1[0] + 0.85
G3_IN = (L[7]['start'] + 1.75, L[7]['start'] + 2.35)             # the lower-left man runs in
BURST2 = (L[7]['start'] + 2.45, L[7]['start'] + 3.2)
HIT3 = BURST2[0] + 0.4
FIRE0, FIRE1 = BURST1[0], BURST2[1]
SCUTTLE = (HIT3 + 0.05, L[8]['start'] - 0.15)            # Link in through the gate, at his mark for line 8
S8_AT = L[9]['start'] + 0.42 * (L[9]['end'] - L[9]['start'])   # the push to Navi on "GRENADES"
ZIP = L[9]['end'] + 0.1                           # Navi zips at the gunman
BOOM = ZIP + 0.55                                 # note 63: a zip the camera can follow
INCOMING = (L[8]['start'] + 0.15, BOOM - 0.05)    # notes 47, 63: the right-hand man, kneeling just off the right of
                                                  # S7's frame, fires on them until Navi reaches him; S8 follows her
S9_AT = min(BOOM + 1.1, L[10]['start'] - 0.1)
S10_AT = L[10]['end'] + 0.2
S11_AT = L[12]['start'] - 0.15
S12_AT = L[12]['end'] + 0.3
SLAM = S12_AT + 0.25
S13_AT = L[14]['end'] + 0.15
DUR = L[15]['end'] + 0.7
BLACK_AT = DUR

SHOTS = [('S1', 0.0, L[2]['start'] - 0.1), ('S2', L[2]['start'] - 0.1, L[3]['start'] - 0.1),
         ('S3', L[3]['start'] - 0.1, L[4]['start'] - 0.1), ('S4', L[4]['start'] - 0.1, L[5]['start'] - 0.2),
         ('S5', L[5]['start'] - 0.2, L[6]['start'] - 0.15), ('S6', L[6]['start'] - 0.15, GATE),
         ('S7', GATE, S8_AT), ('S8', S8_AT, S9_AT), ('S9', S9_AT, S10_AT), ('S10', S10_AT, S11_AT),
         ('S11', S11_AT, S12_AT), ('S12', S12_AT, L[14]['start'] - 0.12), ('S12b', L[14]['start'] - 0.12, S13_AT),
         ('S13', S13_AT, DUR)]
SHOT_CAST = {'S1': ['kg'], 'S2': ['link', 'navi'], 'S3': ['kg'], 'S4': ['link', 'navi'], 'S5': ['gunman', 'kg'],
             'S6': ['link', 'navi'], 'S7': ['kg', 'link', 'gunman1', 'gunman2', 'gunman3', 'navi'],
             'S8': ['navi', 'gunman2'], 'S9': ['link'], 'S10': ['kg', 'zelda', 'malon', 'ruto', 'goron', 'saria'],
             'S11': ['link'], 'S12': ['kg', 'link', 'navi'], 'S12b': ['kg', 'link', 'navi'], 'S13': ['link']}
PLAN = dict(ROOMS={}, OPENINGS={}, THINGS={}, PEOPLE={}, CAMS={}, GROUPS={})   # rule 1: the sets' plan is in
BENCHMARK = []                                   # remakes_sets (CAMP, TOWN, STAGE; its BENCHMARK, setcheck clean)
KEEP_CLEAR, PROP_SIZES, JOKE_PROPS = [], [], []
OUTFIT, HEIGHTS = {}, {}
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
ALLOWED_CONTACTS, ALLOWED_POPS, SET_EXCLUDE = [], [], []
TOUCHES, FREE_MOVES, SOUND_SOURCES = [], [], {}
EFFECTS = []
CUT_RESTS_OK, FAMOUS = [], []
# ====================================================================================================================


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def _talk(who, t):
    """0-1 mouth opening for `who` at t (None when not speaking)."""
    for ln in LINES:
        if ln['who'] == who and ln['start'] <= t < ln['end']:
            op = ln['_open']
            return float(op[min(len(op) - 1, int((t - ln['start']) * 100))])
    return None


def _shape(o):
    if o is None or o < 0.15:
        return None
    return 'etc' if o < 0.4 else ('E' if o < 0.7 else 'AI')


def _lay(img):
    return Image.new('RGBA', img.size, (0, 0, 0, 0))


def _kid(img, cam, who, x, y, ppm, t, mood=None, j=None, yaw=0, head_yaw=None, flip=1, rot=0.0, talk=True,
         sp_extra=None):
    """A child or the gunman with their soles at (x, y) (screen px through cam), ppm pixels a metre; mood, pose,
    talking from the recording; rot degrees tips the drawing about the soles (a fall)."""
    key = 'gunman' if who.startswith('gunman') else who
    sp = dict(RC.CAST[key])
    if key == 'link':
        sp['head_life'] = HL['link']                                  # Job K: never a still talking photo
    if mood:
        sp['mood'] = mood
    if sp_extra:
        sp.update(sp_extra)
    sh = _shape(_talk(key, t)) if talk else None
    if sh:
        sp['mouth'] = 'v:' + sh
    s = RS.s_for(ppm)
    k = RC.scale_for(sp, s)
    tgt = _lay(img) if rot else img
    if flip < 0:
        RC.person(tgt, B.Local(cam, x, 0, 1.0, -1), 0, y - 928 * k, s, sp, t, yaw, j, head_yaw)
    else:
        RC.person(tgt, cam, x, y - 928 * k, s, sp, t, yaw, j, head_yaw)
    if rot:
        cx, cy = cam.P(x, y)
        img.alpha_composite(tgt.rotate(rot, center=(cx, cy), resample=Image.BICUBIC))
    return s, k


def _gun_pose():
    import copy
    return copy.deepcopy(RC.poses('gunman')['aiming'])


def _font(n):
    return ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), int(n))


def _prompt(img, label, text, x, y, age, press=None):
    """A game button prompt (Decision 5): a dark rounded pill, the button in a white ring, the action in caps; it
    pops in over 0.15 s. press = seconds since the action is taken (Sam, 11 Nov): the whole prompt flashes silver
    at that moment (a white-silver pill with a bright halo, a small punch in size), fading back over 0.35 s."""
    if age < 0:
        return
    k = (0.6 + 0.55 * ease(age / 0.1) - 0.15 * ease((age - 0.1) / 0.08)) * B.SS
    fl = 0.0 if press is None or press < 0 else max(0.0, 1 - press / 0.35)
    if fl > 0:
        k *= 1 + 0.22 * fl
        d = ImageDraw.Draw(img)
        f2 = _font(40 * k)
        w, h = 110 * k + d.textlength(text, font=f2) + 50 * k, 96 * k
        X, Y = x * B.SS - w / 2, y * B.SS - h / 2
        lay = _lay(img)
        dl = ImageDraw.Draw(lay)
        for g in (34, 20, 9):                                         # the halo
            dl.rounded_rectangle((X - g * k, Y - g * k, X + w + g * k, Y + h + g * k), radius=h / 2 + g * k,
                                 fill=(255, 255, 255, int(70 * fl)))
        mix = lambda c0, c1: tuple(int(a_ + (b_ - a_) * fl) for a_, b_ in zip(c0, c1)) + (255,)
        dl.rounded_rectangle((X, Y, X + w, Y + h), radius=h / 2, fill=mix((20, 22, 30), (214, 220, 230)),
                             outline=(255, 255, 255), width=int(5 * k))
        dl.rounded_rectangle((X + 8 * k, Y + 8 * k, X + w - 8 * k, Y + h * 0.45), radius=h / 4,
                             fill=(255, 255, 255, int(200 * fl)))       # the silver's shine along the top
        cx, cy = X + 52 * k, Y + h / 2
        dl.ellipse((cx - 36 * k, cy - 36 * k, cx + 36 * k, cy + 36 * k), fill=(255, 255, 255), outline=INK, width=int(3 * k))
        dl.text((cx, cy), label, font=_font(46 * k), fill=(20, 22, 30), anchor='mm')
        dl.text((X + 104 * k, cy), text, font=f2, fill=mix((255, 255, 255), (20, 22, 30)), anchor='lm')
        img.alpha_composite(lay)
        return
    d = ImageDraw.Draw(img)
    f1, f2 = _font(46 * k), _font(40 * k)
    tw = d.textlength(text, font=f2)
    w, h = 110 * k + tw + 50 * k, 96 * k
    X, Y = x * B.SS - w / 2, y * B.SS - h / 2
    d.rounded_rectangle((X, Y, X + w, Y + h), radius=h / 2, fill=(20, 22, 30, 230), outline=(255, 255, 255), width=int(4 * k))
    cx, cy = X + 52 * k, Y + h / 2
    d.ellipse((cx - 36 * k, cy - 36 * k, cx + 36 * k, cy + 36 * k), fill=(240, 240, 240), outline=INK, width=int(3 * k))
    d.text((cx, cy), label, font=f1 if len(label) < 3 else f2, fill=(20, 22, 30), anchor='mm')
    d.text((X + 104 * k, cy), text, font=f2, fill=(255, 255, 255), anchor='lm')


def _blob(cam, x, y, r, n=11, seed=0, bump=0.3):
    rng = np.random.default_rng(seed)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1 - bump / 2 + bump * rng.random())
        pts.append(cam.P(x + rr * math.cos(a), y + rr * math.sin(a)))
    return pts


def _flash(img, cam, x, y, r, seed=0, dirx=None, diry=0.0):
    """A flat lumpy flash, never a star: yellow round white. With a direction (dirx, diry) it is a muzzle flash
    (Fable r3 #26: not a round octagon floating off the gun): a flame cone out of the muzzle at (x, y), wide at
    its mouth, ragged, with a short back-blast, its length flickering per frame."""
    d = ImageDraw.Draw(img)
    if dirx is None:
        d.polygon(_blob(cam, x, y, r, 12, seed), fill=(255, 196, 60), outline=INK)
        d.polygon(_blob(cam, x, y, r * 0.6, 10, seed + 1), fill=(255, 244, 190))
        return
    n = math.hypot(dirx, diry) or 1.0
    ux, uy = dirx / n, diry / n
    px, py = -uy, ux
    rng = np.random.default_rng(seed)
    ln = r * (2.2 + 0.9 * rng.random())

    def cone(k):
        pts = [(x + px * r * 0.18 * k, y + py * r * 0.18 * k)]
        for i, (f, w) in enumerate(((0.35, 0.55), (0.6, 0.95), (0.8, 0.6), (1.0, 0.0), (0.8, -0.6), (0.6, -0.95),
                                    (0.35, -0.55))):
            j = 1 + 0.25 * (rng.random() - 0.5)
            pts.append((x + ux * ln * f * k * j + px * r * w * k, y + uy * ln * f * k * j + py * r * w * k))
        pts.append((x - px * r * 0.18 * k, y - py * r * 0.18 * k))
        return [cam.P(*q) for q in pts]
    d.polygon(cone(1.0), fill=(255, 196, 60), outline=INK)
    d.polygon(cone(0.55), fill=(255, 244, 190))


def _splat(img, cam, x, y, r, seed=0):
    d = ImageDraw.Draw(img)
    d.polygon(_blob(cam, x, y, r, 13, seed, 0.6), fill=(178, 22, 30), outline=INK)
    d.polygon(_blob(cam, x - r * 0.2, y - r * 0.2, r * 0.4, 9, seed + 3, 0.5), fill=(214, 46, 50))


BITS = [((178, 22, 30), 1.0), ((92, 96, 70), 1.2), ((40, 40, 44), 0.9), ((150, 110, 70), 0.7), ((178, 22, 30), 0.8),
        ((214, 46, 50), 0.6), ((92, 96, 70), 0.9), ((130, 92, 60), 0.6), ((178, 22, 30), 1.1), ((60, 64, 52), 0.8),
        ((214, 46, 50), 0.7), ((150, 110, 70), 0.5), ((178, 22, 30), 0.9), ((40, 40, 44), 0.7)]


def _bits(img, cam, x, y, age, size, seed=5, g=2600.0, ground=None):
    """Body parts, cloth and dirt flung out and falling (Decision 7: splattier, flat house-style pieces)."""
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(img)
    for i, (col, sz) in enumerate(BITS):
        a = -math.pi * (0.1 + 0.8 * rng.random())
        sp = size * (5 + 7 * rng.random())
        bx = x + math.cos(a) * sp * age
        by = y + math.sin(a) * sp * age + 0.5 * g * (size / 100) * age * age
        if ground is not None and by > ground:
            by = ground
        r = size * 0.22 * sz
        spin = age * (6 + 4 * rng.random()) + i
        if i in (2, 9, 13):                                           # Fable r3 #25: parts that can be named: the
            c_, s_ = math.cos(spin), math.sin(spin)                   # rifle, the helmet, a boot
            R_ = lambda pts: [cam.P(bx + (px * c_ - py * s_) * r, by + (px * s_ + py * c_) * r) for px, py in pts]
            if i == 2:
                d.polygon(R_([(-2.6, -0.18), (2.6, -0.18), (2.6, 0.18), (-0.6, 0.2), (-0.8, 0.8), (-1.2, 0.8),
                              (-1.1, 0.25), (-2.6, 0.3)]), fill=(30, 30, 34), outline=INK)
            elif i == 9:
                d.polygon(R_([(-1.1, 0.3)] + [(1.1 * math.cos(math.pi + k * math.pi / 8), 0.3 + 1.0 * math.sin(math.pi + k * math.pi / 8))
                                              for k in range(9)] + [(1.25, 0.45), (-1.25, 0.45)]), fill=(66, 72, 58), outline=INK)
            else:
                d.polygon(R_([(-0.4, -1.0), (0.3, -1.0), (0.3, 0.2), (1.1, 0.3), (1.1, 0.7), (-0.4, 0.7)]),
                          fill=(34, 30, 28), outline=INK)
            continue
        d.polygon(_blob(cam, bx, by, r, 7, seed + i, 0.7), fill=col, outline=INK)


def _smoke(img, cam, x, y, age, size, seed=9):
    lay = _lay(img)
    d = ImageDraw.Draw(lay)
    a = int(200 * max(0.0, 1 - age / 1.4))
    for i in range(5):
        ox = (i - 2) * size * 0.35
        r = size * (0.4 + 0.5 * min(1, age / 0.8)) * (0.8 + 0.1 * i % 3)
        d.polygon(_blob(cam, x + ox, y - size * 0.3 * i % 2 - age * size * 0.6, r, 10, seed + i, 0.3),
                  fill=(120, 116, 110, a))
    img.alpha_composite(lay)


def _shake(t, t0, amp, dur=0.45):
    """Note 46: the camera kicked by a blast at t0, dying away over dur (world px)."""
    a = t - t0
    if a < 0 or a > dur:
        return 0.0, 0.0
    k = amp * (1 - a / dur) ** 2
    i = int(a * FPS)
    return k * (1 if i % 2 else -1) * (0.6 + 0.4 * math.sin(i * 2.3)), k * (0.5 if i % 3 else -0.7)


def _explosion(img, cam, x, y, a, size, seed=0, planks=False, gy=None):
    """Note 46 (Sam: one frame fine, the next all on the ground): a real blast over many frames. A white-out frame,
    a fireball that swells and burns down into black smoke, a shockwave ring along the ground, sparks, dust rolling
    out low, and the gate's planks (planks=True) or dirt clods flung out tumbling. (x, y) its heart, size its
    fireball's radius, gy the ground under it (world px); a seconds since it went off."""
    if a < 0:
        return
    gy = y + size * 0.6 if gy is None else gy
    rng = np.random.default_rng(seed)
    lay = _lay(img)
    d = ImageDraw.Draw(lay)
    for i in range(10):                                               # the smoke: dark billows rising and spreading
        a0 = 0.12 + 0.05 * i
        u = a - a0
        if u < 0 or u > 2.6:
            continue
        px = x + (rng.random() - 0.5) * size * 1.3 + (rng.random() - 0.3) * size * 0.4 * u
        py = y - size * 0.15 - u * size * (1.0 + 0.6 * rng.random())
        r = size * (0.32 + 0.2 * rng.random()) * (0.6 + 0.9 * min(1.0, u / 0.9))
        g = int(52 + 70 * min(1.0, u / 2.0))
        al = int(235 * max(0.0, 1 - u / 2.6))
        d.polygon(_blob(cam, px, py, r, 11, seed + 30 + i, 0.3), fill=(g, g - 4, g - 8, al))
    for i in range(10):                                               # dust rolling out low along the ground
        sd = -1 if i % 2 else 1
        f = 0.5 + 0.6 * rng.random()
        u = a - 0.03
        if u < 0 or u > 1.8:
            continue
        px = x + sd * size * (0.3 + 2.4 * f * ease(u / 0.9))
        py = gy - size * (0.12 + 0.25 * rng.random()) - size * 0.2 * u
        r = size * (0.22 + 0.12 * rng.random()) * (0.7 + 0.8 * min(1.0, u / 0.7))
        d.polygon(_blob(cam, px, py, r, 9, seed + 50 + i, 0.35), fill=(198, 172, 128, int(220 * max(0.0, 1 - u / 1.8))))
    img.alpha_composite(lay)
    lay = _lay(img)
    d = ImageDraw.Draw(lay)
    if a < 0.32:                                                      # the shockwave: a pale ring out along the ground
        u = a / 0.32
        rx = size * (0.6 + 4.2 * u)
        (X0, Y0), (X1, Y1) = cam.P(x - rx, gy - rx * 0.3), cam.P(x + rx, gy + rx * 0.3)
        d.ellipse((X0, Y0, X1, Y1), outline=(255, 248, 226, int(230 * (1 - u))),
                  width=max(1, int(cam.S(size * 0.1 * (1 - u)))))
    if a < 0.62:                                                      # the fireball: swells, then burns down to smoke
        k = ease(a / 0.16)
        fade = int(255 * (1 - ease((a - 0.36) / 0.26)))
        r = size * (0.45 + 0.6 * k) * (1 + 0.25 * a)
        lift = size * 0.5 * a
        for rr, col, sd in ((1.0, (196, 58, 28), 1), (0.8, (242, 120, 34), 2), (0.6, (255, 186, 60), 3),
                            (0.42 * max(0.0, 1 - a / 0.42), (255, 246, 206), 4)):
            if rr * r < 2:
                continue
            dk = min(1.0, a / 0.5) * (1.0 if sd == 1 else 0.6)            # the outside goes sooty first
            c = tuple(int(v * (1 - 0.55 * dk) + 40 * 0.55 * dk) for v in col)
            d.polygon(_blob(cam, x, y - lift * rr, r * rr, 13, seed + sd + int(a * FPS) * 7, 0.32),
                      fill=c + (fade,), outline=INK + (fade,) if sd == 1 else None)
    if a < 0.5:                                                       # sparks: streaks flying out
        for i in range(16):
            ang = -math.pi * rng.random() * 1.15 + 0.08
            sp = size * (4 + 6 * rng.random())
            u0, u1 = max(0.0, a - 0.05), a
            p0 = (x + math.cos(ang) * sp * u0, y + math.sin(ang) * sp * u0 + 2.5 * size * u0 * u0)
            p1 = (x + math.cos(ang) * sp * u1, y + math.sin(ang) * sp * u1 + 2.5 * size * u1 * u1)
            d.line([cam.P(*p0), cam.P(*p1)], fill=(255, 226, 130, int(255 * (1 - a / 0.5))),
                   width=max(1, int(cam.S(size * 0.035))))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    for i in range(9 if planks else 8):                               # planks (or clods) flung out, tumbling
        if a > 1.3:
            break
        ang = -math.pi * (0.12 + 0.76 * rng.random())
        sp = size * (3.2 + 3.5 * rng.random())
        near = 1 + (2.2 * rng.random() if planks else 0.6) * a    # flying at the lens: bigger as they come
        bx = x + math.cos(ang) * sp * a
        by = y + math.sin(ang) * sp * a + 3.2 * size * a * a
        if by > gy + size * 3:
            continue
        if planks:
            ln_, wd = size * (0.35 + 0.35 * rng.random()) * near, size * 0.09 * near
            th = rng.random() * 3 + (rng.random() - 0.5) * 14 * a
            c, s_ = math.cos(th), math.sin(th)
            pts = [(bx + c * px_ - s_ * py_, by + s_ * px_ + c * py_)
                   for px_, py_ in ((-ln_ / 2, -wd / 2), (ln_ / 2, -wd / 2), (ln_ / 2 - wd, wd / 2), (-ln_ / 2, wd / 2))]
            col = (150, 156, 160) if i % 4 == 3 else ((142, 102, 62) if i % 2 else (118, 84, 52))
            d.polygon([cam.P(*p) for p in pts], fill=col, outline=INK)
        else:
            d.polygon(_blob(cam, bx, by, size * 0.07 * near * (0.7 + 0.6 * rng.random()), 7, seed + 70 + i, 0.6),
                      fill=(122, 92, 60), outline=INK)
    if a < 0.17:                                                      # Fable r3 #21 (O6: no white flash): a warm
        img.alpha_composite(Image.new('RGBA', img.size, (255, 170, 70, 70 if a < 0.083 else 30)))   # glow, not a white-out


def _hit(img, cam, x, y, a, ppm, dirx, seed=0, ground=None):
    """Note 48 (Sam: hits very rudimentary): a man hit by a burst. Three wounds land one after another, each with a
    red mist puff, a spray of drops flung out of his back (away from the gun, dirx) arcing down, and the drops
    splat where they land (ground, world y)."""
    if a < 0:
        return
    rng = np.random.default_rng(seed)
    lay = _lay(img)
    dl = ImageDraw.Draw(lay)
    d = ImageDraw.Draw(img)
    for w in range(3):
        u = a - 0.08 * w
        if u < 0:
            continue
        wx, wy = x + (rng.random() - 0.5) * 0.18 * ppm, y + (w - 1) * 0.12 * ppm
        if u < 0.3:                                                   # the mist
            dl.polygon(_blob(cam, wx + dirx * 0.2 * ppm * u / 0.3, wy, 0.1 * ppm * (1 + 2.5 * u / 0.3), 9, seed + w, 0.5),
                       fill=(196, 30, 36, int(170 * (1 - u / 0.3))))
        for k in range(7):                                            # the spray
            ang = (rng.random() - 0.6) * 1.1
            sp = ppm * (2.2 + 2.6 * rng.random())
            bx = wx + dirx * math.cos(ang) * sp * u
            by = wy + math.sin(ang) * sp * u + 4.5 * ppm * u * u
            r = 0.035 * ppm * (0.6 + 0.8 * rng.random())
            if ground is not None and by > ground:
                if u < 1.4:
                    d.polygon(_blob(cam, bx, ground, r * 2.2, 8, seed + 9 * w + k, 0.5), fill=(160, 18, 26))
                continue
            if u < 0.9:
                d.polygon(_blob(cam, bx, by, r, 7, seed + 9 * w + k, 0.4), fill=(190, 24, 32), outline=INK)
        if u < 1.2:                                                   # the wound
            d.polygon(_blob(cam, wx, wy, 0.06 * ppm, 8, seed + 40 + w, 0.6), fill=(150, 14, 22), outline=INK)
    img.alpha_composite(lay)


def _puff(img, cam, x, y, a, r, spark=False, seed=0):
    """A bullet striking near someone (notes 47, 48): a dirt kick on the ground, or a spark off tin and wood."""
    if a < 0 or a > 0.33:
        return
    u = a / 0.33
    lay = _lay(img)
    d = ImageDraw.Draw(lay)
    if spark:
        if u < 0.4:                                                   # a lumpy flash, never a star
            d.polygon(_blob(cam, x, y, r * 0.35, 9, seed, 0.5), fill=(255, 226, 120, 255))
        for k in range(3):                                            # chips flying off it
            ang = -2.4 + 0.9 * k + 0.3 * math.sin(seed)
            p0 = (x + math.cos(ang) * r * 0.4 * (1 + 2 * u), y + math.sin(ang) * r * 0.4 * (1 + 2 * u))
            d.line([cam.P(*p0), cam.P(p0[0] + math.cos(ang) * r * 0.3, p0[1] + math.sin(ang) * r * 0.3)],
                   fill=(255, 232, 140, int(255 * (1 - u))), width=max(1, int(cam.S(r * 0.1))))
    else:
        d.polygon(_blob(cam, x, y - r * u, r * (0.5 + 0.8 * u), 9, seed, 0.4), fill=(186, 158, 116, int(230 * (1 - u))))
        for k in range(4):
            d.polygon(_blob(cam, x + (k - 1.5) * r * 0.5 * u, y - r * 2.2 * math.sin(math.pi * min(1, u * 1.3)) * (0.6 + 0.2 * k),
                            r * 0.14, 6, seed + k, 0.5), fill=(120, 92, 60, 255))
    img.alpha_composite(lay)


# ================================================================================================ the shots
def _forest(view, t, cast):
    img = B.canvas((0, 0, 0))
    cam = B.Cam(1.0)
    RS.forest(img, cam, view, t)
    cast(img, cam)
    RS.forest_front(img, cam, view, t)
    return img


def _alive(t, seed):
    """Note 44 (Sam: KG frozen in S1): blinks every 2-3 s, eye darts held a beat each, a slow sway (degrees)."""
    rng = np.random.default_rng(seed)
    blinks = np.cumsum(1.4 + 1.6 * rng.random(40))
    shut = any(0 <= t - b < 0.13 for b in blinks)
    darts = rng.uniform(-1.0, 1.0, 80)
    k = int(t / 0.75)
    u = ease((t - k * 0.75) / 0.08)
    look = _lerp(darts[k - 1] if k else 0.0, darts[k], u)
    roll, nod = HL['kg'].at_time(t)                                   # Job K: held tilts and nods from his voice,
    return shut, look, 1.8 * roll - 2.5 * nod                         # never a sine sway (the whole owl rocks on
                                                                      # his toes: his head is one with his body)


def _wing_pair(L_, R_):
    return {'L': L_, 'R': ((-R_[0][0], R_[0][1]), (-R_[1][0], R_[1][1]), R_[2])}


def s1_branch(t):
    x, y, ppm = RS.STAGE['forest_up']['kg']
    shut, look, sway = _alive(t, 3)
    m = dict(CR.KG_MOODS['hype'], eyes='shut') if shut else 'hype'
    adv = L[1]['start'] + 3.0                                         # "adventure!": a big double flap
    big = math.sin(math.pi * min(1.0, max(0.0, (t - adv) / 0.5))) if t >= adv else 0.0
    w = []
    for sg, ph in ((1, 0.0), (-1, 1.3)):                             # each wing flaps on its own beat
        f = math.sin(t * 6.0 + ph) * 0.5 + 0.5 * math.sin(t * 2.6 + ph)
        el = (300 + 20 * f, -150 - 60 * f - 80 * big)
        hd = (470 + 30 * f + 40 * big, -260 - 110 * f - 200 * big)
        w.append((el, hd, 'spread'))
    return _forest('up', t, lambda img, cam: RS.kg_on_branch(img, cam, x, RS.s_for(ppm), mood=m,
                                                              wings=_wing_pair(w[0], w[1]), t=t,
                                                              talk=_talk('kg', t), look=look, sway=sway))


KIND = dict(eyes='open', pupil=1.05, shine2=True, brows=(-0.3, 14), beak='smile')   # note 44: S3's eyes open


def s3_branch(t):
    x, y, ppm = RS.STAGE['forest_up']['kg']
    shut, look, sway = _alive(t, 8)
    wis = L[3]['start'] + 0.9                                         # "wisdom!": eyes closed in the smile
    m = 'kindly' if wis <= t < wis + 0.9 else (dict(KIND, eyes='shut') if shut else KIND)
    wag = math.sin(t * 7.0)                                           # the teacher's raised wing wagging
    L_ = ((300, -150 - 15 * wag), (430 + 20 * wag, -330 - 45 * wag), 'point')   # Fable r3 #37: out clear of his crest
    br = 0.5 + 0.5 * math.sin(t * 3.0)                                # the folded wing breathing on his side
    R_ = ((192 + 8 * br, -30), (172 + 12 * br, 90 - 10 * br), 'fold')
    return _forest('up', t, lambda img, cam: RS.kg_on_branch(img, cam, x, RS.s_for(ppm), mood=m,
                                                              wings=_wing_pair(L_, R_), t=t, talk=_talk('kg', t),
                                                              look=0.0 if m == 'kindly' else look * 0.8, sway=sway))


def s2_down(t):
    x, y, ppm = RS.STAGE['forest_down']['link']

    import copy
    j = copy.deepcopy(RC.poses('link')['shrug'])                      # Fable r3 #17: the shrug moves: shoulders and
    sh = ease((t - L[2]['start'] - 0.25) / 0.25) - ease((t - L[2]['end'] + 0.1) / 0.3)   # palms rise on "I think
    for sd in 'LR':                                                   # so?" and drop after
        px, py, pz = j['sh' + sd]
        j['sh' + sd] = (px, py - 22 * sh, pz)
        wx, wy, wz = j['wr' + sd]
        V.arm_to(j, sd, (wx * (1 + 0.1 * sh), wy - 60 * sh, wz), 'back', 'palm')
    j['head_dy'] = 14 + 10 * sh
    a = t * 3.2                                                       # Navi circling him: round BEHIND his head
    nav = (x + 0.7 * ppm * math.cos(a), y - 1.55 * ppm + 0.12 * ppm * math.sin(a))   # (she crossed his face)

    def cast(img, cam):
        RS.foot_shadow(img, cam, x, y, ppm, RS.SHADOW_W['link'])
        if math.sin(a) < 0:
            CR.navi(img, cam, *nav, RS.s_for(ppm) * 1.2, t=t)
        _kid(img, cam, 'link', x, y, ppm, t, 'unsure', j=j)
        if math.sin(a) >= 0:
            CR.navi(img, cam, *nav, RS.s_for(ppm) * 1.2, t=t)
    img = B.canvas((0, 0, 0))
    cam = B.Cam(2.0, x + 30, y - 0.66 * ppm)                          # Fable r3 #17: in closer (his face read small)
    RS.forest(img, cam, 'down', t)
    cast(img, cam)
    RS.forest_front(img, cam, 'down', t)
    return img


def _close(view_fn, t, mood, navi=None, jolt=0.0, debris=None, cam_bg=None, j=None, sp_extra=None):
    """Link's close-up: the set, Link big at the close mark, Navi near his cheek."""
    img = B.canvas((0, 0, 0))
    cam = B.Cam(1.0)
    view_fn(img, cam_bg or cam, t)
    x, y, ppm = RS.STAGE['forest_close']['link']
    _kid(img, cam, 'link', x, y - 40 * jolt, ppm * (1 - 0.04 * jolt), t, mood, j=j, sp_extra=sp_extra)
    if navi:
        nx, ny, heat = navi
        CR.navi(img, cam, nx, ny, 1.25, t=t, heat=heat)
    if debris:
        debris(img, cam)
    return img


def s4_ok(t):
    """Note 58 (Sam, 11 Nov): Navi bouncing off the top of Link's cap again and again, like a ball (the nuzzle was
    too subtle); Link doubtful, looking ahead."""
    u = t - SHOTS[3][1]
    per = 0.36                                                        # one bounce
    k, f = int(u / per), (u % per) / per
    hop = 4 * f * (1 - f)                                             # a ball's arc: 0 on the cap, 1 at the top
    side = (-1) ** k
    nx = 545 + side * _lerp(-55, 55, f)                               # each bounce goes off at a slant, back the
    ny = 935 - 230 * hop                                              # next time
    squash = max(0.0, 1 - min(f, 1 - f) / 0.12)                       # flattened against the cap at each hit
    img = _close(lambda im, c, tt: (RS.forest(im, c, 'close', tt)), t, 'doubtful', jolt=-0.25 * squash * 0)
    cam = B.Cam(1.0)
    RS.forest_front(img, cam, 'close', t)
    lay = _lay(img)
    CR.navi(lay, cam, nx, ny, 1.25, t=t, heat=0.0)
    if squash > 0:                                                    # squashed wide and flat on the cap
        cx, cy = cam.P(nx, ny + 40)
        sq = lay.resize(lay.size, Image.BICUBIC, box=None)
        sq = lay.transform(lay.size, Image.AFFINE, (1 / (1 + 0.35 * squash), 0, cx * (1 - 1 / (1 + 0.35 * squash)),
                                                    0, 1 / (1 - 0.3 * squash), cy * (1 - 1 / (1 - 0.3 * squash))),
                           Image.BICUBIC)
        lay = sq
    img.alpha_composite(lay)
    return img


def s6_god(t):
    u = t - SHOTS[5][1]
    jolt = ease(u / 0.15) if u < 0.6 else 1.0
    sp = RC.CAST['link']
    j = V.standing(sp)                                               # note 36: both hands fly up to his cheeks
    up = ease((u - 0.02) / 0.22)
    for sd, sg in (('L', -1), ('R', 1)):                              # Fable r3 #11: from his hanging hands (not
        if up <= 0.0:                                                 # the hips), elbows out so the upper arms show
            continue
        x0, y0, z0 = j['wr' + sd]
        V.arm_to(j, sd, (_lerp(x0, sg * 92, up), _lerp(y0, -118.0, up), _lerp(z0, 80.0, up) + 150 * math.sin(math.pi * up)),
                 'out', 'palm')
    if up > 0.7:
        j['on_face'] = {'L', 'R'}                                     # palms on his cheeks, in front of his face
    img = _close(lambda im, c, tt: RS.forest(im, c, 'close', tt), t, 'aghast', jolt=jolt,
                 navi=(800, 900 - 120 * ease(u / 0.2) + 20 * math.sin(u * 8), 0.0), j=j)
    RS.forest_front(img, B.Cam(1.0), 'close', t)
    return img


NECK_GRIP = ((66, 1128), (236, 1122))                                 # screen: the back of the gunman's neck, and
                                                                      # under his jaw (note 34; check: s5_contact)


def _s5_wings(t, kx, ky, ks):
    """KG's wings in S5, his own units: up as he lands, closing on the gunman's neck and jaw before the twist
    (note 34), wrenching across on the snap, then flung open."""
    snap = t - SNAP
    fl = 70 * math.sin(t * 15.0) * (1 - ease((snap + 1.2) / 0.3))   # Fable r3 #16: hovering, the wings beat (they
    up = {'R': ((-300, -260 + fl * 0.5), (-520, -420 + fl)), 'L': ((300, -260 + fl * 0.5), (520, -420 + fl))}   # hung still)
    tg = {'R': ((NECK_GRIP[0][0] - kx) / ks, (NECK_GRIP[0][1] - ky) / ks),
          'L': ((NECK_GRIP[1][0] - kx) / ks, (NECK_GRIP[1][1] - ky) / ks)}
    el = {'R': (-290, 20), 'L': (60, 60)}                             # elbows out and down, reaching forward to him
    g = ease((snap + 1.15) / 0.3)                                     # note 45: on by "execution", held, the twist on "move"
    tw = ease(snap / 0.1) if snap >= 0 else 0.0                       # the wrench: one hand back, one forward
    out = ease((snap - 0.22) / 0.3)                                   # and let go, wings flung open
    w = {}
    for sd, sg in (('R', -1), ('L', 1)):
        e = (_lerp(up[sd][0][0], el[sd][0], g), _lerp(up[sd][0][1], el[sd][1], g))
        h = (_lerp(up[sd][1][0], tg[sd][0] + sg * 70 * tw, g), _lerp(up[sd][1][1], tg[sd][1] - 20 * tw, g))
        e = (_lerp(e[0], up[sd][0][0], out), _lerp(e[1], up[sd][0][1], out))
        h = (_lerp(h[0], up[sd][1][0], out), _lerp(h[1], up[sd][1][1], out))
        w[sd] = (e, h, 'grip' if (g > 0.5 and out < 0.5) else 'spread')
    return w, (g >= 1.0 and out <= 0.0)


def s5_contact():
    """Note 34's check: at the twist both wing hands are on the gunman's neck (within a hand of his neck base)."""
    gx, gy, gppm = RS.STAGE['forest_edge']['gunman']
    k = RC.scale_for(RC.CAST['gunman'], RS.s_for(gppm))
    nx, ny = gx, gy - 928 * k
    w, held = _s5_wings(SNAP - 0.05, *S5_KG)
    bad = []
    for sd in 'LR':
        hx, hy = S5_KG[0] + w[sd][1][0] * S5_KG[2], S5_KG[1] + w[sd][1][1] * S5_KG[2]
        if not held or abs(hy - ny) > 70 or abs(hx - nx) > 150:
            bad.append('S5: wing %s is at (%d, %d), the neck at (%d, %d)' % (sd, hx, hy, nx, ny))
    return bad


S5_KG = (470, 940, 1.05)                                              # where he lands behind the gunman
S5_DX = 120                                                           # Fable r3 #5: S5's camera moved left this much


def _rifle_fall(img, cam, rx, ry, rp, a):
    """S5's rifle dropping out of the dead man's hands (Fable r3 #3), turned a radians, centred (rx, ry)."""
    d = ImageDraw.Draw(img)
    c_, s_ = math.cos(a), math.sin(a)
    L_ = 0.55 * rp
    pts = [(-L_, -0.035 * rp), (L_, -0.035 * rp), (L_, 0.035 * rp), (-L_ * 0.4, 0.05 * rp), (-L_ * 0.5, 0.12 * rp),
           (-L_ * 0.6, 0.05 * rp), (-L_, 0.06 * rp)]
    d.polygon([cam.P(rx + c_ * px - s_ * py, ry + s_ * px + c_ * py) for px, py in pts], fill=(30, 30, 34), outline=INK)
S5_SWOOP = (0.1, 0.8)                                                 # seconds into the shot: in from top right


def s5_edge(t):
    u = t - SHOTS[4][1]
    gx, gy, gppm = RS.STAGE['forest_edge']['gunman']
    img = B.canvas((0, 0, 0))
    cam = B.Cam(1.0, W / 2 - S5_DX, H / 2)                            # Fable r3 #5: the pair in from the left edge
    RS.forest(img, cam, 'edge', t)
    snap = t - SNAP
    kx, ky, ks = S5_KG
    j = _gun_pose()
    rot, hy_ = 0.0, None
    drop = 0.0
    if snap >= 0:                                                     # Fable r3 #5: the head wrenched round to face
        hy_ = 90 * (1 - ease(snap / 0.12))                            # us over two frames (180 went black in one)
    if snap >= 0.1:                                                   # Fable r3 #3: dead, he crumples: the rifle
        k = ease((snap - 0.1) / 0.35)                                 # drops, arms go limp, knees buckle, the head
        j = V.standing(RC.CAST['gunman'])                             # lolls and he sinks out of the bottom of frame
        sw = RC.CAST['gunman']['shoulders']
        V.arm_to(j, 'L', (-sw + 10, 260.0 - 60 * k, 70.0), 'down', 'palm')
        V.arm_to(j, 'R', (sw - 10, 250.0 - 40 * k, 90.0), 'down', 'palm')
        for sd, dz in (('L', 90), ('R', -50)):
            fx, fy, fz = j['foot' + sd]
            j['foot' + sd] = (fx, fy - 240 * k, fz + dz * k)
        j['head_dy'] = 40 * k
        rot = -9 * k
        drop = 0.75 * gppm * ease((snap - 0.25) / 0.6)
        rifle = (img, cam, gx - 0.25 * gppm, gy - 1.25 * gppm + 0.9 * gppm * ease((snap - 0.1) / 0.4) ** 2, gppm,
                    math.radians(-25 * k))
    else:
        rifle = None
    wings, held = None, False
    v = (u - S5_SWOOP[0]) / (S5_SWOOP[1] - S5_SWOOP[0])
    if 0 <= v < 1:                                                    # note 35: a swoop down from top right, side on,
        e = 1 - (1 - v) ** 2                                          # wings swept back, levelling out as he arrives
        x = _lerp(1330, kx - 170, e)
        y = _lerp(120, ky, e) - 150 * math.sin(math.pi * e) * (1 - e)
        CR.kg(img, cam, x, y, ks, view='side', mood='glee', wings='swoop', perched=False, t=t,
              flip=-1, lean=_lerp(62, 10, ease((v - 0.45) / 0.55)), talk=_talk('kg', t))
    elif v >= 1:                                                      # landed behind him (drawn first), facing us
        wings, held = _s5_wings(t, kx, ky, ks)
        flare = 1 - ease((u - S5_SWOOP[1]) / 0.3)                     # the landing: a last beat of the wings, settling
        bob = 18 * math.sin(t * 15.0 - 0.8) * (1 - ease((t - SNAP + 1.2) / 0.3))   # rising and dipping on each beat
        CR.kg(img, cam, kx, ky - 26 * flare + bob, ks, view='front', mood='glee', wings=wings, perched=False, t=t,
              talk=_talk('kg', t), part='all', tail=0.35)                # Fable r3 #16: tail tucked up (it hung in
                                                                      # among the rifle and arm)
    _kid(img, cam, 'gunman', gx, gy + drop, gppm, t, j=j, yaw=90, head_yaw=hy_, rot=rot, talk=False)
    if rifle:
        _rifle_fall(*rifle)
    if wings and wings['L'][2] == 'grip':                             # his wing hands again OVER the gunman: seen
        CR.kg_grips(img, cam, kx, ky, ks, wings)                      # closed on the neck and jaw (note 34)
                                                                      # Fable r3 #40: no spark at the neck (it read
                                                                      # as a muzzle flash); the crack carries it
    if L[5]['start'] <= t:
        _prompt(img, 'R1', 'EXECUTION', 640, 330, t - L[5]['start'] - 0.05, press=t - SNAP)
    return img


def _camp_cam(z=1.0, cx=W / 2, cy=H / 2):
    return B.Cam(z, cx, cy)


def _lerp(a, b, u):
    return a + (b - a) * u


def _kg_camp(t):
    """KG in the camp (note 32): (x, d, mode). He storms in through the gate, stops to shoot the tower lookout
    ('tower'), storms on to his mark, turns his gun on the man who runs in lower left ('low'), then stands."""
    kx, kd = RS.CAMP_MARKS['kg']
    if t < KG_T[0]:
        return None
    if t < KG_T[1]:
        u = (t - KG_T[0]) / (KG_T[1] - KG_T[0])
        return _lerp(0.0, 0.1, u), _lerp(RS.WALL_D + 0.6, 7.6, u), 'run'
    if t < KG_T[2]:
        return 0.1, 7.6, 'tower'
    if t < KG_T[3]:
        u = ease((t - KG_T[2]) / (KG_T[3] - KG_T[2]))
        return _lerp(0.1, kx, u), _lerp(7.6, kd, u), 'run'
    if t < BURST2[1] + 0.25:
        return kx, kd, 'low'
    return kx, kd, 'stand'


def _link_camp(t):
    """Link in the camp: (x, d, u) with u 0-1 through his scuttle in through the gate behind KG; None before it."""
    if t < SCUTTLE[0]:
        return None
    lx, ld = RS.CAMP_MARKS['link']
    u = min(1.0, (t - SCUTTLE[0]) / (SCUTTLE[1] - SCUTTLE[0]))
    v = 1 - (1 - u) ** 1.6                                            # quick in, settling at his mark
    return _lerp(-0.8, lx, v), _lerp(RS.WALL_D + 0.4, ld, v), u      # Fable r3 #28: in through the gate's left
                                                                      # half, clear of KG's crest (hidden behind it)


def _scuttle_pose(tt, u):
    """Note 37b: a crouched front-on run (the kit's front_run with the hips dropped), hands clamped over his ears;
    returns the pose and how far the crouch drops him (person units)."""
    import moves
    sp = RC.CAST['link']
    j = moves.gait(sp, tt, 'front_run') if u < 1.0 else V.standing(sp)
    c = 84 if u < 1.0 else 56                                         # the crouch: knees bent, hips low
    for sd in 'LR':
        fx, fy, fz = j['foot' + sd]
        j['foot' + sd] = (fx * 1.5, fy - c, fz)                       # feet apart, a scuttle
    sw = sp['shoulders']
    for s_, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, s_, (sg * (sw - 14), -98.0, 60.0), 'down', 'palm')   # Fable r3 #6: both palms on his ears,
                                                                      # elbows out (the old target read as a salute)
    j['head_dy'] = 26
    return j, c


def _kg_draw(img, cam, x, y, s, t, view, flip=1, rot=0.0, mood='war', firing=False, look=0.0, aim=0.0):
    """KG with the MG42 at his body's middle (x, y), tipped rot degrees about it (side on: leaning back to fire up
    at the tower). Returns the muzzle and its direction (world px)."""
    rec = 6 * s if firing else 0.0
    a = math.radians(rot)
    dx, dy = flip * math.cos(a), -math.sin(a)
    tgt = _lay(img) if rot else img
    hands = CR.kg(tgt, cam, x - rec * dx, y - rec * dy, s, view=view, perched=False, stand=True, wings='gun', band=True,
                  mood=mood, t=t, flip=flip, talk=_talk('kg', t), look=look, gun_aim=aim, head_tilt=0.7 * aim)
    if rot:
        img.alpha_composite(tgt.rotate(rot * flip, center=cam.P(x, y), resample=Image.BICUBIC))
    if aim:                                                           # note 59: only the gun and head swing up
        a = math.radians(aim)
        dx, dy = flip * math.cos(a), -math.sin(a)
    hx = sum(h[0] for h in hands.values()) / 2 / B.SS
    hy = sum(h[1] for h in hands.values()) / 2 / B.SS
    wx = (hx - W / 2) / cam.z + cam.cx                                # hands are screen px through cam: back to world
    wy = (hy - H / 2) / cam.z + cam.cy
    ox, oy = wx - x, wy - 20 * s - y                                  # the barrel line, turned with him
    rb = math.radians(rot)                                            # the body's own turn (not the aim)
    ca, sa = math.cos(-rb * flip), math.sin(-rb * flip)
    bx, by = x + ox * ca - oy * sa, y + ox * sa + oy * ca
    return (bx + dx * 400 * s, by + dy * 400 * s), (dx, dy)


def _kg_camp_face(t, firing, mode):
    """Note 54 (Sam: KG needs more dynamic faces, eyes and body in the camp storm): his mood, eye line and body
    rock at t. Blinks and darts (_alive); a war roar on each burst broken by a crazed grin every third beat; fury on
    his stressed words, glee on "GRENADES"; eyes snapping right at the rounds whipping past; the body rocking on his
    voice (headlife) and shuddering with the gun's recoil (degrees)."""
    shut, look, sway = _alive(t, 7)
    roll, nod = HL['kg'].at_time(t)
    name = 'war'
    if firing is not None:
        name = 'glee' if int(t * 5) % 3 == 2 else 'war'
    elif _talk('kg', t) is not None:
        name = 'glee' if L[9]['start'] <= t < L[9]['end'] + 0.2 else ('fury' if nod > 0.45 else 'war')
    elif INCOMING[0] <= t < INCOMING[1]:
        name, look = 'fury', 2.2                                      # glaring hard off right at the shooter
    m = dict(CR.KG_MOODS[name])
    m['brows'] = (m['brows'][0] + 0.25 * math.sin(t * 7.3), m['brows'][1] + 6 * nod)
    if shut and firing is None:
        m['eyes'] = 'shut'
    rock = sway * 1.4
    if firing is not None:
        rock += 3.0 * math.sin(t * 61) + (2.0 if int(t * FPS) % 2 else -2.0)
    return m, look, rock


def _camp(t, cam, draw_navi=True, boom_view=False):
    """The camp at t through cam (note 32's staging): the gate blown in at GATE; KG storms in through it, shoots the
    tower lookout on his way, then the man who runs in lower left; Link scuttles in through the gate behind him; the
    last man comes in middle right and Navi blows him up. Nobody is behind KG."""
    import moves
    img = B.canvas((0, 0, 0))
    gate = ease((t - BLAST) / 0.12)                                   # flat open under the fireball (note 46)
    RS.camp(img, cam, t, gate)
    st = RS.STAGE['camp']
    C = RS.CAMP
    gx0, gy0 = C.p(0, RS.WALL_D, 1.1)
    _explosion(img, cam, gx0, gy0, t - BLAST, 1.5 * C.ppm(RS.WALL_D), seed=11, planks=True,
               gy=C.p(0, RS.WALL_D, 0)[1])
    lx, ly, lppm = st['link']
    kg = _kg_camp(t)
    burst = next((k for k, (b0, b1) in enumerate((BURST1, BURST2)) if b0 <= t < b1), None)
    firing = burst is not None and int(t * FPS) % 2 == 0

    def gunman(who, x, y, ppm, flip, hit, j=None, fall=1):
        rot = fall * 82 * ease((t - hit) / 0.35) if t >= hit else 0.0
        if who == 'gunman2' and t >= BOOM - 0.28:                     # Fable r3 #47: he recoils from Navi on his
            rot = -14 * ease((t - BOOM + 0.28) / 0.12)                # chest (he sat unmoved)
        if who == 'gunman3' and t < hit:                              # Fable r3 #27: aiming down at KG, not level
            rot = -11.0                                               # over his head at Link and Navi
        if who == 'gunman3' and t >= hit:                             # Fable r3 #15: a slower crumple (he popped
            rot = -fall * 30 * ease((t - hit) / 0.6)                 # out in three frames)
        if who != 'gunman1':
            RS.foot_shadow(img, cam, x, y, ppm, RS.SHADOW_W['gunman'])
        hx = x
        j = j or _gun_pose()
        if t >= hit:                                                  # critique r3: the hit jolts him back
            x += -flip * 0.14 * ppm * math.sin(math.pi * min(1.0, (t - hit) / 0.2))
        if who == 'gunman3' and t >= hit:                             # note 65 (Sam): no stiff model laid flat:
            k = ease((t - hit) / 0.45)                                # he crumples, knees buckling, arms flung,
            if t - hit > 1.0:                                        # the rifle flying, and goes off screen left
                _hit(img, cam, hx - flip * 0.06 * ppm, y - 1.12 * ppm, t - hit, ppm, -flip, seed=len(who) + int(hit),
                     ground=y + 0.1 * ppm)
                return
            x -= 0.35 * ppm * ease((t - hit) / 0.8)
            j = V.standing(RC.CAST['gunman'])
            sw = RC.CAST['gunman']['shoulders']
            V.arm_to(j, 'L', (-sw - 60 * k, -120.0 - 160 * k, 60.0), 'up', 'palm')
            V.arm_to(j, 'R', (sw + 40 * k, -60.0 - 200 * k, -40.0), 'up', 'palm')
            for sd, dz in (('L', 120), ('R', -60)):
                fx, fy, fz = j['foot' + sd]
                j['foot' + sd] = (fx, fy - 260 * k, fz + dz * k)      # knees buckle
            j['head_dy'] = -30 * k
            ra = math.radians(140 * k)                                # the rifle spins away
            _rifle_spin(img, cam, x - flip * 0.6 * ppm * k, y - (1.3 - 0.4 * k) * ppm, ppm, ra)
            y -= 0.0
        _kid(img, cam, who, x, y + (1.7 * ppm * ease((t - hit - 0.1) / 0.85) if who == 'gunman3' and t >= hit else 0),
             ppm, t, j=j, yaw=90, flip=flip, rot=rot, talk=False)
        _hit(img, cam, x - flip * 0.06 * ppm, y - 1.12 * ppm, t - hit, ppm, -flip, seed=len(who) + int(hit),
             ground=y + 0.1 * ppm)                                    # note 48; Fable r3 #22: the tower man's
                                                                      # blood lands on his box, never hangs in the air

    def _rifle_spin(img_, cam_, rx, ry, rp, a):
        d_ = ImageDraw.Draw(img_)
        c_, s_ = math.cos(a), math.sin(a)
        L_ = 0.55 * rp
        pts = [(-L_, -0.035 * rp), (L_, -0.035 * rp), (L_, 0.035 * rp), (-L_, 0.06 * rp)]
        d_.polygon([cam_.P(rx + c_ * px - s_ * py, ry + s_ * px + c_ * py) for px, py in pts], fill=(30, 30, 34), outline=INK)

    def run_in(who, u, tt):
        """The aiming pose on running legs while he comes in (u < 1)."""
        j = _gun_pose()
        if u < 1.0:
            g = moves.gait(RC.CAST['gunman'], tt, 'run')
            for k_ in ('footL', 'footR', 'toeL', 'toeR'):
                j[k_] = g[k_]
        return j

    # the tower lookout (far, up in his box), aiming down at the gate
    x, y, ppm = st['gunman1']
    gunman('gunman1', x, y, ppm, -1, HIT1, fall=-1)
    if BLAST + 0.35 <= t < HIT1 and int(t * FPS) % 3 == 0:            # Fable r3 #22: not frozen: he fires down at
        _flash(img, cam, x - G2_MUZZLE[0] * ppm, y - G2_MUZZLE[1] * ppm, 0.12 * ppm, seed=int(t * 12), dirx=-1.0,
               diry=0.5)                                              # the gate till KG cuts him down
    targets = {0: (x - 0.05 * ppm, y - 1.25 * ppm)}
    # far to near: Link (behind KG, in through the gate), KG, the middle-right man, the lower-left man
    lk = _link_camp(t)
    link_at = None
    if lk:
        x_, d_, u = lk
        sx, sy = C.p(x_, d_)
        ppm = C.ppm(d_)
        j, c = _scuttle_pose(t - SCUTTLE[0], u)
        k = RC.scale_for(RC.CAST['link'], RS.s_for(ppm))
        if u >= 1.0:                                                  # Fable r3 #6: at his mark he cowers, not
            duck = 1.0 if (INCOMING[0] <= t < INCOMING[1] and int(t * FPS) % 3 == 0) or firing else 0.0   # frozen:
            c += 18 + 26 * duck                                       # trembling, ducking at each burst
            sx += 3 * math.sin(t * 47)
        RS.foot_shadow(img, cam, sx, sy, ppm, RS.SHADOW_W['link'])
        _kid(img, cam, 'link', sx, sy + c * k, ppm, t, 'aghast' if t < L[8]['start'] - 0.1 else 'wince', j=j)
        link_at = (sx, sy, ppm)
    muzzle = None
    if kg:
        x_, d_, mode = kg
        sx, sy = C.p(x_, d_)
        ppm = C.ppm(d_)
        s = RS.s_for(ppm)
        stomp = 0.0
        if mode == 'run':
            stomp = 26 * s * abs(math.sin((t - KG_T[0]) * math.pi * 4.0))       # four stamping steps a second
            sx += 10 * s * math.sin((t - KG_T[0]) * math.pi * 4.0)
        RS.foot_shadow(img, cam, sx, sy, ppm, RS.SHADOW_W['kg'])
        face, look, rock = _kg_camp_face(t, burst, mode)             # note 54
        # note 67 (Sam): a turn JUMPS to the other view (South Park); never a squeezed 2D swivel
        if mode == 'tower':
            turn = ease((t - KG_T[1]) / 0.12)
            muzzle = _kg_draw(img, cam, sx, sy - 272 * s, s, t, 'side', 1, 0.0, firing=firing,
                              mood=face, aim=50 * turn)               # note 59: planted; gun and head aim up
        else:
            if mode == 'run':
                rock += 6 * math.sin((t - KG_T[0]) * math.pi * 4.0)      # rolling side to side as he stamps
            fl_ = -1 if mode in ('low', 'stand') else 1               # Fable r3 #20: he stays turned to the low man
            muzzle = _kg_draw(img, cam, sx, sy - 272 * s - stomp, s, t, 'front', fl_,   # (the gun flipped back)
                              rot=rock, firing=firing, mood=face, look=look * fl_)
    # the right-hand man (note 63): kneeling just off the right of S7's frame, firing on them till Navi gets him
    x, y, ppm = _g2()
    if t < BOOM:
        drop = 215.0 * RC.scale_for(RC.CAST['gunman'], RS.s_for(ppm))
        j = _gun_pose()
        j['footR'] = (60.0, 890.0 - 215 + 40, 6.0 - 190)              # down on his right knee, the left foot
        j['footL'] = (-70.0, 890.0 - 215, 6.0 + 200)                  # planted forward (prepper.kneel)
        j['knee_poleR'] = (0.1, 0.4, 1.0)
        j['knee_poleL'] = (-0.1, -0.3, 1.0)
        for k_ in ('toeL', 'toeR'):
            j.pop(k_, None)
        gunman('gunman2', x, y + drop, ppm, -1, 1e9, j)
        if INCOMING[0] <= t < BOOM - 0.28 and int(t * FPS) % 2 == 0 and cam.P(x - G2_MUZZLE[0] * ppm, y)[0] < W * B.SS:
            _flash(img, cam, x - G2_MUZZLE[0] * ppm, y + drop - G2_MUZZLE[1] * ppm, 0.12 * ppm, seed=int(t * 12),
                   dirx=-1.0)
    # the lower-left man: runs in from the bottom left, nearest the lens, and is cut down
    x, y, ppm = st['gunman3']
    if t >= G3_IN[0]:
        u = min(1.0, (t - G3_IN[0]) / (G3_IN[1] - G3_IN[0]))
        x3 = x - (1 - ease(u)) * 1.5 * ppm
        gunman('gunman3', x3, y, ppm, 1, HIT3, run_in('gunman3', u, t - G3_IN[0]), fall=-1)   # critique r3: he
                                                                      # crumples forward, into frame (he fell out of it)
        targets[1] = (x3 + 0.1 * ppm, y - 1.25 * ppm)
    if INCOMING[0] <= t < INCOMING[1] and kg:                   # note 47: the middle-right man fires from off
        kx_, ky_ = C.p(kg[0], kg[1])                                  # screen: rounds whip past KG and Link, kicking
        kp = C.ppm(kg[1])                                             # up dirt and sparking off the barrels
        lay = _lay(img)
        dl = ImageDraw.Draw(lay)
        g2x, g2y, g2p = _g2()
        rx = g2x - 1.1 * g2p                                          # from his muzzle
        fr = int(t * FPS)                                             # note 67 (Sam): steady bursts, every round
        for k in range(2):                                            # whipping close past KG (inconsistent before):
            hy = (0.04, 1.5, 0.1, 1.4)[(fr * 2 + k) % 4]              # skimming the dirt at his toes, just over his
            p0 = (rx, ky_ - kp * hy)                                  # head between the crests (never through him)
            p1 = (kx_ - kp * 3.0, ky_ - kp * (hy + 0.03 * k))
            f = ((fr * 0.37 + k * 0.5) % 1.0) * 0.55
            q0 = (_lerp(p0[0], p1[0], f), _lerp(p0[1], p1[1], f))
            q1 = (_lerp(p0[0], p1[0], f + 0.4), _lerp(p0[1], p1[1], f + 0.4))
            dl.line([cam.P(*q0), cam.P(*q1)], fill=(255, 214, 110, 150), width=int(cam.S(9)))
            dl.line([cam.P(*q0), cam.P(*q1)], fill=(255, 250, 220, 255), width=max(1, int(cam.S(3.5))))
        img.alpha_composite(lay)
        # note 67 (Sam): no dirt kicks or sparks where no round lands
    if firing and muzzle:
        (mx, my), (dx, dy) = muzzle
        s = RS.s_for(C.ppm(kg[1]))
        _flash(img, cam, mx, my, 40 * s, seed=int(t * FPS), dirx=dx, diry=dy)
        d = ImageDraw.Draw(img)
        tx, ty = targets[burst]
        if burst == 1 and t > HIT3 + 0.12:                            # Fable r3 #15: no tracers into empty air
            pass
        elif burst == 0:
            d.line([cam.P(mx, my), cam.P(tx, ty)], fill=(255, 230, 120), width=int(3 * cam.z * B.SS))
        else:                                                         # the near man: tracers down past the lens
            d.line([cam.P(mx, my), cam.P(tx, ty)], fill=(255, 230, 120), width=int(4 * cam.z * B.SS))
        for k in range(3):                                            # cases falling
            cx = mx - dx * 300 * s + 30 * s * k
            ay = (t * 5 + k * 0.3) % 1
            d.rectangle([cam.P(cx, my + 40 * s + ay * 200 * s), cam.P(cx + 8 * s + 2, my + 52 * s + ay * 200 * s + 2)],
                        fill=(210, 170, 70))
    # Navi: at Link's shoulder as he comes in, then red, then zip, then the blast
    if draw_navi and t < BOOM and link_at:
        sx, sy, ppm = link_at
        uu = ease(_link_camp(t)[2]) if _link_camp(t) else 1.0        # Fable r3 #28: over his head as he runs in
        nx, ny = sx + _lerp(0.25, -0.5, uu) * ppm, sy - _lerp(1.75, 1.3, uu) * ppm   # Fable r3 #6: clear of his hands (one hidden
                                                                      # read as a salute)
        heat = ease((t - S8_AT) / 0.5)
        if t >= ZIP:
            gx, gy, gppm = _g2()
            u = ease((t - ZIP) / (BOOM - ZIP))
            nx, ny = nx + (gx - nx) * u, ny + (gy - 0.95 * gppm - ny) * u
        CR.navi(img, cam, nx, ny + 12 * math.sin(t * 9), RS.s_for(lppm) * 1.3, t=t, heat=heat)
    if t >= BOOM:                                                     # note 46: the grenade blast, the same as the
        gx, gy, gppm = _g2()                                          # gate's, with his pieces in it
        a = t - BOOM
        lay = _lay(img)                                               # Fable r3 #25: a scorch on the dirt and the
        ImageDraw.Draw(lay).ellipse([cam.P(gx - 1.1 * gppm, gy - 0.12 * gppm), cam.P(gx + 1.1 * gppm, gy + 0.32 * gppm)],
                                    fill=(30, 26, 22, int(170 * min(1.0, a / 0.2))))   # sandbags beside him
        img.alpha_composite(lay)
        if a > 0.25:
            _splat(img, cam, gx, gy, 0.35 * gppm * min(1.0, (a - 0.25) / 0.3 + 0.4), seed=4)
        _explosion(img, cam, gx, gy - 0.8 * gppm, a, 0.75 * gppm, seed=21, gy=gy + 0.1 * gppm)
        _bits(img, cam, gx, gy - 0.9 * gppm, a, 0.5 * gppm, ground=gy + 0.3 * gppm)
    RS.camp_front(img, cam, t)
    if t >= L[9]['start']:
        _prompt(img, 'R2', 'GRENADES', 540, 330, t - L[9]['start'] - 0.05, press=t - ZIP)   # screen px, not through cam
    return img


def s7_camp(t):
    dx, dy = _shake(t, BLAST, 34)                                     # note 46: the blast kicks the camera
    u = ease(min(1.0, max(0.0, (t - KG_T[2]) / (KG_T[3] - KG_T[2] + 0.25))))   # Fable r3 #10: tight on the gate
    z, cx, cy = _lerp(2.0, 1.4, u), _lerp(690, 565, u), _lerp(760, 790, u)   # and the tower as he bursts in (he
    return _camp(t, B.Cam(z, cx + dx, cy + dy))                       # was 1/14 of the frame), out as he storms on                              # note 32: in on the action (the cast were small
                                                                      # in the top half over an empty yard)


def _g2():
    """The right-hand man's mark (note 63): just past the right of S7's frame, level with KG."""
    C = RS.CAMP
    x, y = C.p(G2_X, RS.CAMP_MARKS['kg'][1] - 0.4)
    return x, y, C.ppm(RS.CAMP_MARKS['kg'][1] - 0.4)


G2_X = 3.3                                                            # note 67: right off S7's frame (his rifle
                                                                      # and flash showed at its edge)
G2_MUZZLE = (0.68, 1.39)                                              # his muzzle from his feet (ppm)


def s8_navi(t):
    st = RS.STAGE['camp']
    lx, ly, _ = st['link']
    gx, gy, gp = _g2()
    u = ease((t - ZIP) / (BOOM - ZIP - 0.12))                         # note 63: the camera follows Navi to him,
                                                                      # there before she strikes (note 67)
    dx, dy = _shake(t, BOOM, 40)
    cx = min((lx + 90) + (gx - lx - 90) * u, S8_CX_MAX - 40) + dx       # Fable r3 #1: the pan stops where the
    cy = _lerp(ly - 160, gy - 0.75 * gp, u)                           # painting ends; note 67: the strike lands in
    return _camp(t, B.Cam(1.7, cx, cy + dy))                          # the middle of the frame (clear of the app's
                                                                      # buttons down the right)


S8_CX_MAX = RS.CAMP.p(11, RS.WALL_D, 0)[0] - W / 2 / 1.7               # the right edge of the frame on the wall's end


def s9_horrible(t):
    u = t - S9_AT

    def bg(im, c, tt):
        lx, ly, _ = RS.STAGE['camp']['link']
        cam = B.Cam(2.4, lx - 140, ly - 250)                          # Fable r3 #36: the red barrel off his head
        RS.camp(im, cam, tt, 1.0)

    def debris(img, cam):                                             # Fable r3 #36: clods and scraps either side
        d = ImageDraw.Draw(img)                                       # of his face (one crossed his mouth like a
        for i in range(8):                                            # tongue; red ones read as petals)
            x = [150, 270, 330, 760, 830, 940, 220, 880][i]
            y = 600 + ((u * 700 + i * 260) % 1700)
            col = [(118, 84, 56), (92, 96, 70), (150, 20, 26), (118, 84, 56), (70, 66, 60), (150, 20, 26),
                   (92, 96, 70), (118, 84, 56)][i]
            d.polygon(_blob(cam, x, y, 20 + (i % 3) * 8, 7, i, 0.5), fill=col, outline=INK)
        land = ease(u / 0.5)                                         # one scrap lands on his cap and stays
        d.polygon(_blob(cam, 600, 560 + 440 * land, 34, 8, 31, 0.5), fill=(150, 20, 26), outline=INK)
    return _close(bg, t, 'horror', debris=debris)


LINEUP_Z, LINEUP_C = 1.55, (715, 1110)   # critique r3: still small at phone size


def s10_square(t):
    img = B.canvas((0, 0, 0))
    cam = B.Cam(LINEUP_Z, *LINEUP_C)                                  # note 49: in on the five, less square
    kcam = B.Cam(0.85, 595, 553)                                      # KG, the presenter, near the lens: a little
    RS.town(img, cam, 'square', t)                                    # smaller and lower so the five lead
    from PIL import ImageFilter                                       # Fable r3 #30: the square softened and hazed
    img = img.filter(ImageFilter.GaussianBlur(2.5 * B.SS))            # back behind the five (a stallholder seemed to
    img.alpha_composite(Image.new('RGBA', img.size, (236, 232, 222, 70)))   # stand on the Goron's shoulder; the
                                                                      # stalls crowded their heads)
    st = RS.STAGE['town_square']
    romance = L[11]['start'] + 0.55
    re_ = ease((t - romance) / 0.35)                                  # note 39: the line-up reacts on "ROMANCE"
    for who, (x, y, ppm) in st.items():
        if who != 'kg':
            RS.foot_shadow(img, cam, x, y, ppm, RS.SHADOW_W.get(who, 0.55))
    for who, (x, y, ppm) in sorted(st.items(), key=lambda kv: kv[1][1]):
        s = RS.s_for(ppm)
        if who == 'kg':
            sweep = ease((t - L[11]['start']) / 1.5)
            wing = {'L': ((300, -120 - 50 * sweep), (400 - 10 * sweep, -250 - 30 * sweep), 'spread'),   # (kept
                                                                      # below Malon, who steps forward: note 39)
                    'R': ((-192, -30), (-172, 90), 'fold')}
            mood = dict(CR.KG_MOODS['show'])                          # Fable r3 #31: eyes open on the line as the
            if t < L[11]['start'] + 1.7:                              # wing sweeps along it, then the shut-eyed
                mood.update(eyes='open', pupil=1.1, shine2=True)      # game-show grin at us
            CR.kg(img, kcam, x, y - 272 * s, s, view='front', perched=False, stand=True, wings=wing, mood=mood, t=t,
                  talk=_talk("kg", t), look=-(0.9 * (1 - sweep) + 0.3))
        elif who == 'goron':
            CR.goron(img, cam, x, y, s, t=t, drool=1.0 + 1.3 * re_)    # note 39: he drools more
        else:
            jj = dict(next(iter(RC.poses(who).values())))
            mood = jj.get('_mood')
            sw = RC.CAST[who]['shoulders']
            dx = dy = 0.0
            zoom = 1.0
            if who == 'saria' and t >= romance:
                mood = 'wink'
            if who == 'zelda':                                        # she shrinks: shoulders up round her ears,
                mood = 'down'                                         # head sunk, a small step back and away
                for sd in 'LR':
                    hx_, hy_, hz_ = jj['sh' + sd]
                    jj['sh' + sd] = (hx_ * (1 - 0.08 * re_), hy_ - 26 * re_, hz_)
                V.arm_to(jj, 'L', (-8.0, 330.0 - 60 * re_, 70.0), 'down', 'fist')
                V.arm_to(jj, 'R', (8.0, 330.0 - 60 * re_, 74.0), 'down', 'fist')
                jj['head_dy'] = jj.get('head_dy', 0) + 30 * re_
                dx, dy, zoom = 14 * re_, -16 * re_, 1 - 0.05 * re_
            if who == 'malon':                                        # she steps forward, the bottle thrust up at us
                V.arm_to(jj, 'R', (70.0 - 20 * re_, 170.0 - 90 * re_, 230.0 + 50 * re_), 'down', 'grip')
                hop = math.sin(math.pi * min(1.0, max(0.0, (t - romance) / 0.3)))
                dy, zoom = 52 * re_ - 14 * hop, 1 + 0.09 * re_
            if who == 'ruto':                                         # she preens: a hand up to smooth her head-fin,
                V.arm_to(jj, 'L', (_lerp(-sw * 0.72, -112.0, re_), _lerp(345.0, -150.0, re_),   # chin lifted
                                   _lerp(0.0, 20.0, re_) + 150 * math.sin(math.pi * re_)), 'out', 'palm')
                jj['head_dy'] = jj.get('head_dy', 0) - 10 * re_
                jj['head_roll'] = 7 * re_
            _kid(img, cam, who, x + dx, y + dy, ppm * zoom, t, mood, j=jj, talk=False)
    return img


def s11_nine(t):
    def bg(im, c, tt):
        RS.town(im, B.Cam(2.0, 540, 530), 'reverse', tt)               # note 56: the reverse angle; Fable r3 #42:
        from PIL import ImageFilter                                   # the planters down below his ears, the busy
        im.paste(im.filter(ImageFilter.GaussianBlur(3 * B.SS)))       # street softened behind the deadpan
        im.alpha_composite(Image.new('RGBA', im.size, (236, 232, 222, 60)))
    return _close(bg, t, 'deadpan', sp_extra={'mouth_k': 0.7})       # critique r3: deadpan talks small


# the wall (notes 33, 37c): KG side on, head tipped up so his face and beak are seen; both wings out in front of
# him and up, below his beak, closed on Link's collar; Link side on facing him, held off the cobbles. No bandana.
LIFT = {'R': ((190, -300), (420, -540), 'grip'), 'L': ((245, -125), (455, -465), 'grip')}
WALL_DX = 150                                                         # the pair moved right, off the frame's edge
WALL_TILT = 24                                                        # degrees his head is tipped up at Link


def _wall_scene(t, cam, shake=0.0):
    img = B.canvas((0, 0, 0))
    RS.town(img, cam, 'wall', t)
    st = RS.STAGE['town_wall']
    _, base, ppm = st['link']
    kx, _, s, _ = _wall_kg()
    g = ease((t - S12_AT) / GRAB)                                     # Fable r3 #9: a grab, a lift and a slam:
    u = ease((t - S12_AT - GRAB) / (SLAM - S12_AT - GRAB))            # the wings shoot out to his collar, haul him
    sx = shake * 14 * math.sin(t * 60)                                # up and drive him back into the pier
    hit = t - SLAM
    ldx = 150 * (1 - u) - (14 * math.sin(math.pi * min(1.0, hit / 0.14)) if hit >= 0 else 0.0)
    rs = _reslam(t)                                                   # note 69 (Sam): he works Link against the
    ldx += 0.16 * ppm * rs                                            # wall: pulled off it and slammed back on his
    if hit >= 0:                                                      # stresses, and shoved up and down in time
        ws = ease(min(1.0, hit / 0.4))                                # with his words
        roll_, nod_ = HL['kg'].at_time(t)
        vy = ws * (0.07 * ppm * math.sin(t * 5.2) - 0.09 * ppm * nod_)
    else:
        vy = 0.0
    k = RC.scale_for(RC.CAST['link'], RS.s_for(ppm))                  # Link at his own scale (KG's is smaller)
    ky = base - 272 * s
    grip = [((LIFT[sd][1][0]), LIFT[sd][1][1]) for sd in 'LR']        # the two wing hands, his own units
    gx_ = sum(g[0] for g in grip) / 2 + 30                            # the collar: between them, just past the tips
    gy_ = sum(g[1] for g in grip) / 2 - 95                            # (his chin clear above the knuckles)
    cx, cy = kx - gx_ * s, ky + gy_ * s                               # (he faces screen left)
    lift = (base - 928 * k) - cy                                      # how far his collar is hauled up
    j = V.standing(RC.CAST['link'])
    kick = math.sin(t * 9.0) * (1.0 if u >= 1 else 0.0)               # his feet dangle and kick a little
    for sd, sg in (('L', -1), ('R', 1)):
        fx, fy, fz = j['foot' + sd]
        j['foot' + sd] = (fx, fy - 14, fz + sg * 34 * kick)
        V.arm_to(j, sd, (sg * 24.0, 120.0, 120.0), 'down', 'grip')     # both hands up on the wings that hold him
    lxx, lyy = cx + ldx + sx * 0.6, base - lift * u + vy
    hits = [(t - ts, lyy - 0.7 * ppm) for ts in [SLAM] + RESLAMS]
    _pier(img, cam, cx - PIER_GAP * ppm, base, ppm, hits)              # Fable r3 #2: something at his back
    _kid(img, cam, 'link', lxx, lyy, ppm, t, 'terrified', j=j, yaw=90, talk=True)
    CR.navi(img, cam, cx + 330 * s, cy - 330 * s + 14 * math.sin(t * 6), s * 1.2, t=t,   # above KG's beak, between
            heat=0.3 + 0.6 * ease((t - SLAM) / 7.0))                              # the faces: whole in all 3 framings
    yk = ky + (1 - u) * 0
    dn = (lift * (1 - u) + vy) / s                                    # the lift: his wing hands stay on the collar
    rc = 170 * (1 - g)                                                # the reach: hands from his chest to the collar
    wl = {sd: ((LIFT[sd][0][0] - rc * 0.5, LIFT[sd][0][1] + dn * 0.45 + rc * 0.3),
               (LIFT[sd][1][0] - rc, LIFT[sd][1][1] + dn + rc * 0.4), 'grip' if g > 0.7 else 'spread')
          for sd in 'LR'}                                             # as it rises (they crossed Link's head before)
    roll, nod = HL['kg'].at_time(t)                                   # note 57 (Job K rule): his head jabs and
    tilt = WALL_TILT + 2.6 * roll + 9 * nod                           # tilts on his own voice, held between
    mood = dict(CR.KG_MOODS['fury' if nod > 0.45 else 'rage'])       # the stressed words: a hissing squint
    if t < S12_AT + 0.5 or abs(roll) < 1.2:                           # held tilts that sit near level: eyes wider
        mood['pupil'] = 0.22
    if _talk('kg', t) is None and t > L[14]['end']:                   # after his last word: a slow menacing lean in
        tilt += 4 * ease((t - L[14]['end']) / 0.6)
    CR.kg(img, cam, kx + ldx + sx, yk, s, view='side', perched=False, stand=True, wings=wl, band=False,
          mood=mood, t=t, flip=-1, talk=_talk('kg', t), head_tilt=tilt)
    return img


def _reslams():
    """Note 69: the moments KG re-slams Link into the wall: his strongest stressed beats (headlife nods) after the
    first slam, at least 1.1 s apart, none in the last half second of his lines."""
    out, last = [], SLAM
    tt = SLAM + 0.9
    while tt < L[14]['end'] - 0.5:
        n0, n1, n2 = (HL['kg'].at_time(tt + d_)[1] for d_ in (-1.0 / FPS, 0.0, 1.0 / FPS))
        if n1 > 0.5 and n1 >= n0 and n1 >= n2 and tt - last >= 1.1:
            out.append(tt)
            last = tt
        tt += 1.0 / FPS
    return out


def _reslam(t):
    """0-1: how far Link is pulled off the wall for the next re-slam (0.18 s back, then slammed in 0.06 s)."""
    for ts in RESLAMS:
        if ts - 0.24 <= t < ts - 0.06:
            return math.sin(0.5 * math.pi * (t - ts + 0.24) / 0.18)
        if ts - 0.06 <= t < ts:
            return 1 - (t - ts + 0.06) / 0.06
    return 0.0


GRAB = 0.1                                                            # seconds the wings take to reach his collar
PIER_GAP = 0.07                                                       # the pier's face behind Link's soles (ppm)


def _pier(img, cam, x1, base, ppm, hit):
    """Fable r3 #2: a stone pier jutting out of the wall at Link's back (he was held in mid-air against a flat
    backdrop): its face at x1, from the ground up out of frame; hit: (seconds since a slam, Link's back y) for each."""
    p = B.Pen(img, cam)
    w = 0.4 * ppm
    stone, dark = (168, 164, 156), (128, 124, 118)
    p.poly([(x1 - w, -200), (x1, -200), (x1, base + 30), (x1 - w, base + 30)], stone, INK, 2.6)
    p.poly([(x1 - 0.14 * ppm, -200), (x1, -200), (x1, base + 30), (x1 - 0.14 * ppm, base + 30)], dark, None)
    for k in range(14):                                               # the courses of stone
        y = base + 30 - k * 0.32 * ppm
        p.line([(x1 - w, y), (x1, y)], INK, 1.6)
        xo = x1 - w * (0.45 if k % 2 else 0.75)
        p.line([(xo, y), (xo, y - 0.32 * ppm)], INK, 1.4)
    p.poly([(x1 - w, -200), (x1, -200), (x1, base + 30), (x1 - w, base + 30)], None, INK, 2.6)
    for h_, hy_ in hit:                                               # note 69 (Sam): a gentle puff of grey dust
        if 0 <= h_ < 0.7:                                             # off the stone on each slam (no flying clods)
            u_ = h_ / 0.7
            lay = _lay(img)
            d_ = ImageDraw.Draw(lay)
            for k in range(3):
                d_.polygon(_blob(cam, x1 + (0.04 + 0.1 * u_) * ppm, hy_ + (k - 1) * 0.22 * ppm - 0.05 * ppm * u_,
                                 (0.07 + 0.12 * u_) * ppm, 9, 3 + k, 0.35), fill=(196, 194, 190, int(120 * (1 - u_))))
            img.alpha_composite(lay)


KG_WALL = 0.85                                                        # Fable r3 #12: KG at the wall at 0.85 of the
                                                                      # shared scale (side on he was four Links wide;
                                                                      # in the camp he stands about Link's height)


def _wall_kg():
    """KG at the wall: his x (moved so Link's collar stays where it was), feet y, scale, and Link's scale k."""
    _, base, ppm = RS.STAGE['town_wall']['link']
    s0 = RS.s_for(ppm)
    s = s0 * KG_WALL
    gx_ = sum(LIFT[sd][1][0] for sd in 'LR') / 2 + 30
    return RS.STAGE['town_wall']['kg'][0] + WALL_DX - gx_ * (s0 - s), base - 272 * s, s, RC.scale_for(RC.CAST['link'], s0)


def wall_contact():
    """Note 37c's check: at the wall both wing hands are at Link's collar (his neck base), not across his chest."""
    kx, ky, s, k = _wall_kg()
    hs = [(kx - LIFT[sd][1][0] * s, ky + LIFT[sd][1][1] * s) for sd in 'LR']
    cx = kx - (sum(LIFT[sd][1][0] for sd in 'LR') / 2 + 30) * s      # his neck base, as _wall_scene puts it
    cy = ky + (sum(LIFT[sd][1][1] for sd in 'LR') / 2 - 95) * s
    return ['S12: wing hand at (%d, %d), the collar at (%d, %d)' % (hx, hy, cx, cy) for hx, hy in hs
            if not (0 <= hy - cy <= 190 * k and abs(hx - cx) <= 90 * k)]


def _wall_marks():
    """Link's collar and scale at the wall, and KG's x (as _wall_scene places them)."""
    kx, ky, s, k = _wall_kg()
    cx = kx - (sum(LIFT[sd][1][0] for sd in 'LR') / 2 + 30) * s
    cy = ky + (sum(LIFT[sd][1][1] for sd in 'LR') / 2 - 95) * s
    return cx, cy, k, kx, ky, s


def s12_wall(t):
    choices = L[14]['start'] + 1.2
    shake = 1.0 if (choices <= t < choices + 0.8 or SLAM <= t < SLAM + 0.3) else 0.0
    if any(ts <= t < ts + 0.15 for ts in RESLAMS):                    # note 69: a jolt on each re-slam
        shake = max(shake, 0.6)
    if shot_of(t) == 'S12b':                                          # 13b: a cut in closer for the shake, the two
        cx, cy, k, kx, ky, s = _wall_marks()                          # faces either side of the middle
        return _wall_scene(t, B.Cam(1.3, (cx + kx) / 2 + 20, cy + 150 * s), shake)
    return _wall_scene(t, B.Cam(1.0), shake)


RESLAMS = _reslams()
S13_TRACK = mouths.track(L[15]['text'], L[15]['_stretches'], L[15]['_open'])   # note 53: the full mouth set


def s13_pinned(t):
    """Note 53 (Sam: front-on Link at "I want to go home", fuller mouth movements): the camera where KG's face is,
    Link square on to it, pinned to the wall and held off the ground, terrified, tears; every syllable's mouth shape
    from the line (mouths.track), drawn bigger; KG's two wings reach in from the bottom corners and grip his collar;
    Navi, nearly red, at his shoulder."""
    img = B.canvas((0, 0, 0))
    wcx, wcy = _wall_marks()[:2]                                     # Fable r3 #24: the same patch of wall as at
    zb = 2.6                                                          # his back in S12 (stones, not the window box
    RS.town(img, B.Cam(zb, wcx - 40, wcy - 250 / zb), 'wall', t)     # and banner from the far end of the wall)
    x, y, ppm = RS.STAGE['forest_close']['link']
    s = RS.s_for(ppm)
    k = RC.scale_for(RC.CAST['link'], s)
    cam = B.Cam(1.5, x, y - 928 * k - 250 / 1.5)                      # in close: his collar a little below middle
    x += 4 * math.sin(t * 47) + 2.5 * math.sin(t * 29)                # trembling
    j = V.standing(RC.CAST['link'])
    # critique r3: his arms hang limp at his sides, held up off the ground (on the wings the hands were lost)
    sp_extra = {'mouth_k': 1.6}
    if L[15]['start'] <= t < L[15]['end']:
        sh = mouths.at(S13_TRACK, t - L[15]['start'])
        if sh != 'rest':
            sp_extra['mouth'] = 'v:' + sh
    _kid(img, cam, 'link', x, y, ppm, t, 'terrified', j=j, talk=False, sp_extra=sp_extra)
    nx, ny = x, y - 928 * k                                           # his collar (neck base)
    ws = 0.62                                                         # the wings at KG's own scale near the lens
    p = B.Pen(img, B.Local(cam, 0, 0, ws))
    roll, nod = HL['kg'].at_time(t)
    for sg, sd in ((-1, 1), (1, -1)):                                 # KG's wings, up from below, closed on the collar
        hx, hy = nx + sg * 70 * k, ny + 20 * k
        el = (x + sg * 300 + 5 * roll, ny + 330 + 8 * nod)
        sh_ = (x + sg * 380, ny + 900)
        CR._kg_wing(p, (sh_[0] / ws, sh_[1] / ws), (el[0] / ws, el[1] / ws), (hx / ws, hy / ws), 'grip', sd)
    hb = (x + 6 * roll, ny + 540 + 10 * nod)                          # Fable r3 #14: the back of KG's head in the
    for sg in (-1, 1):                                                # foreground (over the wings), his crests sweeping up either
        CR._crest(p, ((hb[0] + sg * 120) / ws, (hb[1] - 170) / ws),   # side of Link (the bare wings read as straps)
                  [((hb[0] + sg * 250) / ws, (hb[1] - 400) / ws), ((hb[0] + sg * 320) / ws, (hb[1] - 640) / ws),
                   ((hb[0] + sg * 300) / ws, (hb[1] - 840) / ws), ((hb[0] + sg * 230) / ws, (hb[1] - 900) / ws)],
                  80, seed=2 if sg < 0 else 1, out=sg)
    p.ell(hb[0] / ws, hb[1] / ws, 300 / ws, 230 / ws, CR.KG_BROWN, INK, 3.0)
    for k_ in range(3):                                               # the feather tufts on the crown
        a_ = -0.7 + 0.7 * k_
        p.line([((hb[0] + 220 * math.sin(a_)) / ws, (hb[1] - 150 * math.cos(a_)) / ws),
                ((hb[0] + 120 * math.sin(a_)) / ws, (hb[1] - 60 * math.cos(a_)) / ws)], CR.dk(CR.KG_BROWN, 0.7), 3.0)
    CR.navi(img, cam, x - 290, y - 928 * k - 380 + 14 * math.sin(t * 6), 1.0, t=t,   # Fable r3 #23: on the banner side
            heat=0.3 + 0.6 * ease((t - SLAM) / 7.0))
    return img


SHOT_FN = {'S1': s1_branch, 'S2': s2_down, 'S3': s3_branch, 'S4': s4_ok, 'S5': s5_edge, 'S6': s6_god,
           'S7': s7_camp, 'S8': s8_navi, 'S9': s9_horrible, 'S10': s10_square, 'S11': s11_nine, 'S12': s12_wall, 'S12b': s12_wall,
           'S13': s13_pinned}


CLOSE_IN = {'S4': (1.7, 1150), 'S6': (1.7, 1250), 'S9': (1.7, 1250), 'S11': (1.3, 1150)}   # note 68: S11 halfway back out   # zoom, centre y (px)


def picture(t):
    if t >= BLACK_AT:
        return Image.new('RGB', (W, H), (0, 0, 0))
    sh = shot_of(t)
    img = SHOT_FN[sh](t)
    if sh in CLOSE_IN:                                                # Fable r3 #34: Link's close-ups in to the chest
        z, cy = CLOSE_IN[sh]                                          # (they were waist-up, his face a quarter of the
        w, h = img.size[0] / z, img.size[1] / z                       # width); cropped from the full-size picture
        cx, cy = img.size[0] / 2, cy * img.size[1] / H
        img = img.crop((int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2)))
    return img.convert('RGB').resize((W, H), Image.LANCZOS) if img.size != (W, H) else img.convert('RGB')


# ================================================================================================ subtitles
def _pieces(ln):
    """Note 51 (Sam, 11 Nov): 3-5 words at a time, each up on the syllable it starts with (the take's syllable
    beats), never joined into longer rows; a piece shorter than 0.45 s pushes the next one a touch later."""
    if '_pieces' in ln:
        return ln['_pieces']
    import press_secretary as PS
    ch = [c for c, _ in SUB.chunks(ln.get('sub') or ln['text'], most=4)]
    out = [[ch[0], 0.0]]
    if len(ch) > 1:
        beats = PS._syllable_beats(ln['_voice'], ln['_stretches'])
        syl = [sum(mouths._syllables(w) for w in c.split()) for c in ch]
        acc = 0
        for c, n in zip(ch[1:], syl[:-1]):
            acc += n
            k = min(len(beats) - 1, int(round(acc / sum(syl) * len(beats))))
            out.append([c, max(out[-1][1] + 0.45, beats[k] - 0.06 if len(beats) else out[-1][1] + 0.8)])
    ln['_pieces'] = [tuple(p) for p in out]
    return ln['_pieces']


def caption_at(t):
    for i, ln in enumerate(LINES):
        nxt = LINES[i + 1]['start'] - 0.05 if i + 1 < len(LINES) else 1e9
        if ln['start'] - 0.05 <= t < min(ln['end'] + 0.45, nxt):
            u = t - ln['start']
            return [c for c, a in _pieces(ln) if a <= u or a == 0.0][-1]
    return None


def draw_subtitle(img, text):
    """Note 51: larger (66 px, was 50), a thick outline, lower third, at most two rows."""
    S = B.SS
    f = ImageFont.truetype(B.SANS, int(66 * S))
    rows = B.wrap(text, f, 900 * S)
    lay = _lay(img)
    d = ImageDraw.Draw(lay)
    for i, row in enumerate(rows):
        y = (1450 - 84 * (len(rows) - 1 - i)) * S
        d.text((540 * S, y), row, font=f, fill=(255, 255, 255), anchor='mm', stroke_width=int(7 * S),
               stroke_fill=(0, 0, 0))
    img.alpha_composite(lay)


def overlay(img, t):
    return img


def frame_image(t):
    return picture(t)


# ================================================================================================ sound
SFX = os.path.join(HERE, 'audio', 'patriots3-sfx')
_SFX = {}


def _sfx(name, t0=0.0, t1=None):
    if (name, t0, t1) not in _SFX:
        x = MA.load(os.path.join(SFX, name))
        _SFX[(name, t0, t1)] = x[int(t0 * SR):None if t1 is None else int(t1 * SR)]
    return _SFX[(name, t0, t1)]


def _crack():
    """The neck crack: two sharp clicks of filtered noise, 40 ms apart."""
    rng = np.random.default_rng(2)
    n = int(0.12 * SR)
    x = np.zeros(n)
    for at in (0, int(0.04 * SR)):
        m = int(0.018 * SR)
        x[at:at + m] += rng.standard_normal(m) * np.exp(-np.linspace(0, 6, m))
    return x * 0.6


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice = np.zeros(n)
    rest = np.zeros(n)
    for ln in LINES:
        s = int(ln['start'] * SR)
        seg = ln['_voice'].copy()
        bl = ln.get('bleep')
        for b0, b1 in ([bl] if bl and not isinstance(bl[0], (list, tuple)) else (bl or [])):
            i0, i1 = int((b0 - ln['start']) * SR), int((b1 - ln['start']) * SR)
            tt = np.arange(i1 - i0) / SR
            lvl = np.sqrt(np.mean(seg[max(0, i0 - SR // 2):i0] ** 2)) * 1.4 + 1e-4
            seg[i0:i1] = np.sin(2 * math.pi * 1000 * tt) * lvl
        seg = seg[:max(0, n - s)]
        voice[s:s + len(seg)] += seg
    mg = _sfx('mg42.mp3', 2.8, 5.0)
    for b0, b1 in (BURST1, BURST2):                                   # two bursts: the tower, then the near man
        k = int((b1 - b0) * SR)
        burst = np.tile(mg, k // len(mg) + 1)[:k].copy()
        burst[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))
        filmkit.place(rest, burst, at=b0, sr=SR, gain=0.35)
    crack = np.zeros(n)
    filmkit.place(crack, _crack(), at=SNAP, sr=SR, gain=0.9)        # the crack lands on "move" by design: not ducked
    filmkit.place(rest, _sfx('explosion.mp3'), at=BLAST, sr=SR, gain=0.6)   # note 46: the gate blows
    k = int(0.35 * SR)                                                # note 47: his short bursts from off screen
    for b0 in np.arange(INCOMING[0], BOOM - 0.3, 0.7):
        filmkit.place(rest, mg[:k] * np.linspace(1, 0.2, k), at=float(b0), sr=SR, gain=0.16)
    filmkit.place(rest, _sfx('explosion.mp3'), at=BOOM, sr=SR, gain=0.6)
    end = int(BLACK_AT * SR)
    # check sheet 11 Nov: the gate blast and gunfire sat as loud as "Clear enemy" and the grenade tail as loud as
    # "This is": the effects duck about 15 dB under any voice (quick down, slower up)
    on = np.zeros(n)
    for ln in LINES:
        on[int(ln['start'] * SR):int(ln['end'] * SR)] = 1.0           # the whole line, not each syllable
    k_ = int(0.15 * SR)
    duck = np.convolve(on, np.ones(k_) / k_, mode='same')
    rest = rest * (1 - 0.82 * np.clip(duck, 0, 1)) + crack
    rest[end:] = 0
    mix = voice + rest
    mix, g = MA.master(mix, end)
    voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


def checks():
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    import voices
    faults = voices.bleep_check(sys.modules[__name__], []) + s5_contact() + wall_contact()
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


def main():
    a = sys.argv[1:]
    if a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'check':
        B.SS = 1
        checks()
        print('checks: clean')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)


if __name__ == '__main__':
    main()
