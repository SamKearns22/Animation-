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
    (6, '06', 'link', 'Oh my god!', 'S6', 1.0, []),
    (7, '07', 'kg', 'Clear enemy encampments to clear segments of the map.', 'S7', 0.9, []),
    (8, '08', 'link', "I don't think I can do this.", 'S7', 0.2, []),
    (9, '09', 'kg', 'R2 FOR GRENADES.', 'S7', 0.6, []),      # note 38: line 8's subtitle now reads for 2 s
    (10, '10', 'link', 'This is horrible.', 'S9', 1.75, []),
    (11, '11', 'kg', 'FIVE ROMANCE OPTIONS TO CHOOSE FROM', 'S10', 0.4, []),
    (12, '12', 'link', 'Um, I am 9 years old.', 'S11', 0.6, []),
    (13, '13', 'kg', "Now listen here, you s***. You're gonna grow up real f****** fast.", 'S12', 0.6,
     [(2.08, 2.40), (4.87, 4.99)]),                    # notes 43, 52: the "it" of shit, the "uck"
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
GATE = L[6]['end'] + 0.3                          # the gate bursts in: S7 starts
# the camp (note 32): KG storms in through the gate, shoots the tower lookout on his way, then the man who runs in
# lower left; Link scuttles in through the gate behind him; the last man comes in middle right
KG_T = (GATE + 0.08, L[7]['start'] + 0.45, L[7]['start'] + 1.6, L[7]['start'] + 2.3)   # in, stop, on, at his mark
BURST1 = (L[7]['start'] + 0.5, L[7]['start'] + 1.55)             # up at the tower, from "enemy"
HIT1 = BURST1[0] + 0.85
G3_IN = (L[7]['start'] + 1.75, L[7]['start'] + 2.35)             # the lower-left man runs in
BURST2 = (L[7]['start'] + 2.45, L[7]['start'] + 3.2)
HIT3 = BURST2[0] + 0.4
FIRE0, FIRE1 = BURST1[0], BURST2[1]
SCUTTLE = (L[7]['start'] + 2.3, L[8]['start'] - 0.15)            # Link in through the gate, at his mark for line 8
G2_IN = (L[8]['start'] + 0.1, L[8]['start'] + 0.75)              # the middle-right man runs in
S8_AT = L[9]['start'] + 0.42 * (L[9]['end'] - L[9]['start'])   # the push to Navi on "GRENADES"
ZIP = L[9]['end'] + 0.1                           # Navi zips at the gunman
BOOM = ZIP + 0.35
S9_AT = BOOM + 1.1
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


def _flash(img, cam, x, y, r, seed=0):
    """A flat lumpy flash, never a star: yellow round white."""
    d = ImageDraw.Draw(img)
    d.polygon(_blob(cam, x, y, r, 12, seed), fill=(255, 196, 60), outline=INK)
    d.polygon(_blob(cam, x, y, r * 0.6, 10, seed + 1), fill=(255, 244, 190))


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
    L_ = ((250, -170 - 15 * wag), (290 + 20 * wag, -380 - 45 * wag), 'point')
    br = 0.5 + 0.5 * math.sin(t * 3.0)                                # the folded wing breathing on his side
    R_ = ((192 + 8 * br, -30), (172 + 12 * br, 90 - 10 * br), 'fold')
    return _forest('up', t, lambda img, cam: RS.kg_on_branch(img, cam, x, RS.s_for(ppm), mood=m,
                                                              wings=_wing_pair(L_, R_), t=t, talk=_talk('kg', t),
                                                              look=0.0 if m == 'kindly' else look * 0.8, sway=sway))


def s2_down(t):
    x, y, ppm = RS.STAGE['forest_down']['link']

    def cast(img, cam):
        RS.foot_shadow(img, cam, x, y, ppm, RS.SHADOW_W['link'])
        _kid(img, cam, 'link', x, y, ppm, t, 'unsure', j=RC.poses('link')['shrug'])
        a = t * 3.2                                                   # Navi circling him
        CR.navi(img, cam, x + 150 * math.cos(a), y - 1.05 * ppm + 40 * math.sin(a), RS.s_for(ppm) * 1.2, t=t)
    return _forest('down', t, cast)


def _close(view_fn, t, mood, navi=None, jolt=0.0, debris=None, cam_bg=None, j=None):
    """Link's close-up: the set, Link big at the close mark, Navi near his cheek."""
    img = B.canvas((0, 0, 0))
    cam = B.Cam(1.0)
    view_fn(img, cam_bg or cam, t)
    x, y, ppm = RS.STAGE['forest_close']['link']
    _kid(img, cam, 'link', x, y - 40 * jolt, ppm * (1 - 0.04 * jolt), t, mood, j=j)
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
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, (sg * _lerp(sp['shoulders'] + 30, 92, up), _lerp(330.0, -118.0, up),
                         _lerp(40.0, 80.0, up) + 150 * math.sin(math.pi * up)),
                 'down', 'palm')
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
    up = {'R': ((-300, -260), (-520, -420)), 'L': ((300, -260), (520, -420))}
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
S5_SWOOP = (0.1, 0.8)                                                 # seconds into the shot: in from top right


def s5_edge(t):
    u = t - SHOTS[4][1]
    gx, gy, gppm = RS.STAGE['forest_edge']['gunman']
    img = B.canvas((0, 0, 0))
    cam = B.Cam(1.0)
    RS.forest(img, cam, 'edge', t)
    snap = t - SNAP
    kx, ky, ks = S5_KG
    j = _gun_pose()
    rot, hy_ = 0.0, None
    drop = 0.0
    if snap >= 0:
        hy_ = 180                                                     # the head turned right round
        rot = -14 * ease((snap - 0.15) / 0.4)
        drop = 60 * ease((snap - 0.15) / 0.4)
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
        CR.kg(img, cam, kx, ky - 26 * flare, ks, view='front', mood='glee', wings=wings, perched=False, t=t,
              talk=_talk('kg', t), part='all')
    _kid(img, cam, 'gunman', gx, gy + drop, gppm, t, j=j, yaw=90, head_yaw=hy_, rot=rot, talk=False)
    if wings and wings['L'][2] == 'grip':                             # his wing hands again OVER the gunman: seen
        CR.kg_grips(img, cam, kx, ky, ks, wings)                      # closed on the neck and jaw (note 34)
    if 0 <= snap < 0.12:
        _flash(img, cam, 170, 1150, 50, seed=3)
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
    return _lerp(-0.15, lx, v), _lerp(RS.WALL_D + 0.4, ld, v), u


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
        V.arm_to(j, s_, (sg * (sw + 10), -150.0, 40.0), 'down', 'palm')
    j['head_dy'] = 26
    return j, c


def _kg_draw(img, cam, x, y, s, t, view, flip=1, rot=0.0, mood='war', firing=False):
    """KG with the MG42 at his body's middle (x, y), tipped rot degrees about it (side on: leaning back to fire up
    at the tower). Returns the muzzle and its direction (world px)."""
    rec = 6 * s if firing else 0.0
    a = math.radians(rot)
    dx, dy = flip * math.cos(a), -math.sin(a)
    tgt = _lay(img) if rot else img
    hands = CR.kg(tgt, cam, x - rec * dx, y - rec * dy, s, view=view, perched=False, stand=True, wings='gun', band=True,
                  mood=mood, t=t, flip=flip, talk=_talk('kg', t))
    if rot:
        img.alpha_composite(tgt.rotate(rot * flip, center=cam.P(x, y), resample=Image.BICUBIC))
    hx = sum(h[0] for h in hands.values()) / 2 / B.SS
    hy = sum(h[1] for h in hands.values()) / 2 / B.SS
    wx = (hx - W / 2) / cam.z + cam.cx                                # hands are screen px through cam: back to world
    wy = (hy - H / 2) / cam.z + cam.cy
    ox, oy = wx - x, wy - 20 * s - y                                  # the barrel line, turned with him
    ca, sa = math.cos(-a * flip), math.sin(-a * flip)
    bx, by = x + ox * ca - oy * sa, y + ox * sa + oy * ca
    return (bx + dx * 400 * s, by + dy * 400 * s), (dx, dy)


def _camp(t, cam, draw_navi=True, boom_view=False):
    """The camp at t through cam (note 32's staging): the gate blown in at GATE; KG storms in through it, shoots the
    tower lookout on his way, then the man who runs in lower left; Link scuttles in through the gate behind him; the
    last man comes in middle right and Navi blows him up. Nobody is behind KG."""
    import moves
    img = B.canvas((0, 0, 0))
    gate = ease((t - GATE) / 0.25)
    RS.camp(img, cam, t, gate)
    st = RS.STAGE['camp']
    C = RS.CAMP
    lx, ly, lppm = st['link']
    kg = _kg_camp(t)
    burst = next((k for k, (b0, b1) in enumerate((BURST1, BURST2)) if b0 <= t < b1), None)
    firing = burst is not None and int(t * FPS) % 2 == 0

    def gunman(who, x, y, ppm, flip, hit, j=None, fall=1):
        rot = fall * 82 * ease((t - hit) / 0.35) if t >= hit else 0.0
        if who != 'gunman1':
            RS.foot_shadow(img, cam, x, y, ppm, RS.SHADOW_W['gunman'])
        _kid(img, cam, who, x, y, ppm, t, j=j or _gun_pose(), yaw=90, flip=flip, rot=rot, talk=False)
        if hit <= t < hit + 0.3:
            _splat(img, cam, x + flip * 0.1 * ppm, y - 1.3 * ppm, 0.28 * ppm, seed=len(who) + int(hit))

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
        if mode == 'tower':
            turn = ease((t - KG_T[1]) / 0.12)
            muzzle = _kg_draw(img, cam, sx, sy - 272 * s, s, t, 'side', 1, 50 * turn, firing=firing)
        else:
            muzzle = _kg_draw(img, cam, sx, sy - 272 * s - stomp, s, t, 'front', -1 if mode == 'low' else 1,
                              firing=firing)
    # the middle-right man: runs in from the right, level with KG, and opens fire
    x, y, ppm = st['gunman2']
    if G2_IN[0] <= t < BOOM:
        u = min(1.0, (t - G2_IN[0]) / (G2_IN[1] - G2_IN[0]))
        x2 = x + (1 - ease(u)) * 1.6 * ppm
        gunman('gunman2', x2, y, ppm, -1, 1e9, run_in('gunman2', u, t - G2_IN[0]))
        if u >= 1.0 and int(t * FPS) % 3 == 0:                        # he fires at them
            _flash(img, cam, x - 1.05 * ppm, y - 1.32 * ppm, 0.16 * ppm, seed=int(t * 12))
    # the lower-left man: runs in from the bottom left, nearest the lens, and is cut down
    x, y, ppm = st['gunman3']
    if t >= G3_IN[0]:
        u = min(1.0, (t - G3_IN[0]) / (G3_IN[1] - G3_IN[0]))
        x3 = x - (1 - ease(u)) * 1.5 * ppm
        gunman('gunman3', x3, y, ppm, 1, HIT3, run_in('gunman3', u, t - G3_IN[0]))
        targets[1] = (x3 + 0.1 * ppm, y - 1.25 * ppm)
    if firing and muzzle:
        (mx, my), (dx, dy) = muzzle
        s = RS.s_for(C.ppm(kg[1]))
        _flash(img, cam, mx + dx * 30 * s, my + dy * 30 * s, 50 * s, seed=int(t * FPS))
        d = ImageDraw.Draw(img)
        tx, ty = targets[burst]
        if burst == 0:
            d.line([cam.P(mx, my), cam.P(tx, ty)], fill=(255, 230, 120), width=int(3 * cam.z * B.SS))
        else:                                                         # the near man: tracers down past the lens
            d.line([cam.P(mx, my), cam.P(tx, ty)], fill=(255, 230, 120), width=int(4 * cam.z * B.SS))
        for k in range(3):                                            # cases falling
            cx = mx - dx * 300 * s + 30 * s * k
            ay = (t * 5 + k * 0.3) % 1
            d.rectangle([cam.P(cx, my + 40 * s + ay * 200 * s), cam.P(cx + 8 * s + 2, my + 52 * s + ay * 200 * s + 2)],
                        fill=(210, 170, 70))
    if GATE <= t < GATE + 0.18:
        g0, g1 = C.p(0, RS.WALL_D, 1.2)
        _flash(img, cam, g0, g1, 220, seed=11)
    # Navi: at Link's shoulder as he comes in, then red, then zip, then the blast
    if draw_navi and t < BOOM and link_at:
        sx, sy, ppm = link_at
        nx, ny = sx + 0.42 * ppm, sy - 1.12 * ppm
        heat = ease((t - S8_AT) / 0.5)
        if t >= ZIP:
            gx, gy, gppm = st['gunman2']
            u = ease((t - ZIP) / (BOOM - ZIP))
            nx, ny = nx + (gx - nx) * u, ny + (gy - 1.25 * gppm - ny) * u
        CR.navi(img, cam, nx, ny + 12 * math.sin(t * 9), RS.s_for(lppm) * 1.3, t=t, heat=heat)
    if t >= BOOM:
        gx, gy, gppm = st['gunman2']
        a = t - BOOM
        _bits(img, cam, gx, gy - 1.2 * gppm, a, 0.5 * gppm, ground=gy + 0.3 * gppm)
        if a < 0.3:
            _flash(img, cam, gx, gy - 1.1 * gppm, (0.6 + 1.2 * a) * gppm, seed=21)
        _smoke(img, cam, gx, gy - 1.0 * gppm, a, 0.8 * gppm)
        if a > 0.3:
            _splat(img, cam, gx, gy, 0.35 * gppm, seed=4)
    RS.camp_front(img, cam, t)
    if t >= L[9]['start']:
        _prompt(img, 'R2', 'GRENADES', 540, 330, t - L[9]['start'] - 0.05, press=t - ZIP)   # screen px, not through cam
    return img


def s7_camp(t):
    return _camp(t, B.Cam(1.4, 565, 790))                              # note 32: in on the action (the cast were small
                                                                      # in the top half over an empty yard)


def s8_navi(t):
    st = RS.STAGE['camp']
    lx, ly, _ = st['link']
    gx, gy, _ = st['gunman2']
    u = ease((t - ZIP) / 0.5)
    return _camp(t, B.Cam(1.7, (lx + 90) + (gx - lx - 90) * u, (ly - 160) + (gy - ly) * u * 0.6))


def s9_horrible(t):
    u = t - S9_AT

    def bg(im, c, tt):
        lx, ly, _ = RS.STAGE['camp']['link']
        cam = B.Cam(2.4, lx, ly - 250)
        RS.camp(im, cam, tt, 1.0)

    def debris(img, cam):
        d = ImageDraw.Draw(img)
        for i in range(9):
            x = 120 + i * 113
            y = -100 + ((u * 700 + i * 260) % 2100)
            d.polygon(_blob(cam, x, y, 14 + (i % 3) * 6, 7, i, 0.7), fill=[(130, 92, 60), (178, 22, 30), (92, 96, 70)][i % 3], outline=INK)
        land = ease(u / 0.5)                                         # one bit lands on his cap
        d.polygon(_blob(cam, 560, -60 + 690 * land, 22, 7, 31, 0.7), fill=(178, 22, 30), outline=INK)
    return _close(bg, t, 'horror', debris=debris)


def s10_square(t):
    img = B.canvas((0, 0, 0))
    cam = B.Cam(1.0)
    RS.town(img, cam, 'square', t)
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
            CR.kg(img, cam, x, y - 272 * s, s, view='front', perched=False, stand=True, wings=wing, mood='show', t=t,
                  talk=_talk('kg', t))
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
        RS.town(im, B.Cam(2.0, 540, 600), 'square', tt)
    return _close(bg, t, 'deadpan')


# the wall (notes 33, 37c): KG side on, head tipped up so his face and beak are seen; both wings out in front of
# him and up, below his beak, closed on Link's collar; Link side on facing him, held off the cobbles. No bandana.
LIFT = {'R': ((230, -180), (430, -510), 'grip'), 'L': ((245, -125), (455, -465), 'grip')}
WALL_DX = 150                                                         # the pair moved right, off the frame's edge
WALL_TILT = 24                                                        # degrees his head is tipped up at Link


def _wall_scene(t, cam, shake=0.0):
    img = B.canvas((0, 0, 0))
    RS.town(img, cam, 'wall', t)
    st = RS.STAGE['town_wall']
    _, base, ppm = st['link']
    kx = st['kg'][0] + WALL_DX
    s = RS.s_for(ppm)
    u = ease((t - S12_AT) / (SLAM - S12_AT))
    sx = shake * 14 * math.sin(t * 60)
    ldx = 60 * (1 - u)
    k = RC.scale_for(RC.CAST['link'], s)
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
    lxx, lyy = cx + ldx + sx * 0.6, base - lift * u + (cy - (base - 928 * k) + lift) * 0
    _kid(img, cam, 'link', lxx, lyy, ppm, t, 'terrified', j=j, yaw=90, talk=True)
    CR.navi(img, cam, cx + 330 * s, cy - 330 * s + 14 * math.sin(t * 6), s * 1.2, t=t,   # above KG's beak, between
            heat=0.3 + 0.6 * ease((t - SLAM) / 7.0))                              # the faces: whole in all 3 framings
    yk = ky + (1 - u) * 0
    dn = lift * (1 - u) / s                                           # the lift: his wing hands stay on the collar
    wl = {sd: ((LIFT[sd][0][0], LIFT[sd][0][1] + dn * 0.45), (LIFT[sd][1][0], LIFT[sd][1][1] + dn), 'grip')
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


def wall_contact():
    """Note 37c's check: at the wall both wing hands are at Link's collar (his neck base), not across his chest."""
    st = RS.STAGE['town_wall']
    _, base, ppm = st['link']
    s = RS.s_for(ppm)
    kx, ky = st['kg'][0] + WALL_DX, base - 272 * s
    hs = [(kx - LIFT[sd][1][0] * s, ky + LIFT[sd][1][1] * s) for sd in 'LR']
    cx = kx - (sum(LIFT[sd][1][0] for sd in 'LR') / 2 + 30) * s      # his neck base, as _wall_scene puts it
    cy = ky + (sum(LIFT[sd][1][1] for sd in 'LR') / 2 - 95) * s
    k = RC.scale_for(RC.CAST['link'], s)
    return ['S12: wing hand at (%d, %d), the collar at (%d, %d)' % (hx, hy, cx, cy) for hx, hy in hs
            if not (0 <= hy - cy <= 190 * k and abs(hx - cx) <= 90 * k)]


def _wall_marks():
    """Link's collar and scale at the wall, and KG's x (as _wall_scene places them)."""
    st = RS.STAGE['town_wall']
    _, base, ppm = st['link']
    s = RS.s_for(ppm)
    kx, ky = st['kg'][0] + WALL_DX, base - 272 * s
    cx = kx - (sum(LIFT[sd][1][0] for sd in 'LR') / 2 + 30) * s
    cy = ky + (sum(LIFT[sd][1][1] for sd in 'LR') / 2 - 95) * s
    return cx, cy, RC.scale_for(RC.CAST['link'], s), kx, ky, s


def s12_wall(t):
    choices = L[14]['start'] + 1.2
    shake = 1.0 if (choices <= t < choices + 0.8 or SLAM <= t < SLAM + 0.15) else 0.0
    if shot_of(t) == 'S12b':                                          # 13b: a cut in closer for the shake, the two
        cx, cy, k, kx, ky, s = _wall_marks()                          # faces either side of the middle
        return _wall_scene(t, B.Cam(1.3, (cx + kx) / 2 + 20, cy + 150 * s), shake)
    return _wall_scene(t, B.Cam(1.0), shake)


def s13_pinned(t):
    cx, cy, k, kx, ky, s = _wall_marks()                              # his face, held up at KG's grip, with the
    return _wall_scene(t, B.Cam(2.1, cx + 150 * s, cy + 40 * k))      # wings on his collar and KG's beak below


SHOT_FN = {'S1': s1_branch, 'S2': s2_down, 'S3': s3_branch, 'S4': s4_ok, 'S5': s5_edge, 'S6': s6_god,
           'S7': s7_camp, 'S8': s8_navi, 'S9': s9_horrible, 'S10': s10_square, 'S11': s11_nine, 'S12': s12_wall, 'S12b': s12_wall,
           'S13': s13_pinned}


def picture(t):
    if t >= BLACK_AT:
        return Image.new('RGB', (W, H), (0, 0, 0))
    img = SHOT_FN[shot_of(t)](t)
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
    filmkit.place(rest, _crack(), at=SNAP, sr=SR, gain=0.9)
    filmkit.place(rest, _sfx('explosion.mp3'), at=BOOM, sr=SR, gain=0.6)
    end = int(BLACK_AT * SR)
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
