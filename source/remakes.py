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
SWEARS_OK = [(13, 'shit', 'Sam: bleep the f-word only ("god-damn" heard)')]
# n, recording, who, text, shot, gap before (s), bleeps in the recording's own seconds (found from the sound: the
# f of the word and its vowel in the high band, 10 Nov)
_L = [
    (1, '01', 'kg', 'Hello, Link! Are you ready for a f****** adventure!', 'S1', 0.3, [(3.33, 3.72)]),
    (2, '02', 'link', 'Uh, yeah, I think so?', 'S2', 0.2, []),
    (3, '03', 'kg', "Great, here's some wisdom!", 'S3', 0.2, []),
    (4, '04', 'link', 'Ok?', 'S4', 0.2, []),
    (5, '05', 'kg', 'Press R1 for an EXECUTION MOVE.', 'S5', 0.45, []),
    (6, '06', 'link', 'Oh my god!', 'S6', 1.0, []),
    (7, '07', 'kg', 'Clear enemy encampments to clear segments of the map.', 'S7', 0.9, []),
    (8, '08', 'link', "I don't think I can do this.", 'S7', 0.2, []),
    (9, '09', 'kg', 'R2 FOR GRENADES.', 'S7', 0.15, []),
    (10, '10', 'link', 'This is horrible.', 'S9', 1.75, []),
    (11, '11', 'kg', 'FIVE ROMANCE OPTIONS TO CHOOSE FROM', 'S10', 0.4, []),
    (12, '12', 'link', 'I am 9 years old.', 'S11', 0.6, []),
    (13, '13', 'kg', "Now listen here, you shit. You're gonna grow up real f****** fast.", 'S12', 0.6, [(4.81, 5.05)]),
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

# the action beats, from the lines
SNAP = L[5]['end'] + 0.12                         # the neck snap, just after "MOVE"
GATE = L[6]['end'] + 0.3                          # the gate bursts in: S7 starts
FIRE0 = L[7]['start'] + 0.5                       # firing from "enemy"
FIRE1 = L[7]['end'] + 0.15
HIT1, HIT3 = L[7]['start'] + 1.4, L[7]['start'] + 2.5   # KG guns down the tower lookout, then the far gunman
SCUTTLE = (L[8]['start'] - 0.7, L[8]['start'] + 0.3)
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


def _prompt(img, label, text, x, y, age):
    """A game button prompt (Decision 5): a dark rounded pill, the button in a white ring, the action in caps; it
    pops in over 0.15 s."""
    if age < 0:
        return
    k = (0.6 + 0.55 * ease(age / 0.1) - 0.15 * ease((age - 0.1) / 0.08)) * B.SS
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


def s1_branch(t):
    x, y, ppm = RS.STAGE['forest_up']['kg']
    bob = 10 * math.sin(t * 7.0)
    return _forest('up', t, lambda img, cam: RS.kg_on_branch(img, cam, x, RS.s_for(ppm), mood='hype', wings='wide',
                                                              t=t, talk=_talk('kg', t), look=0.0) if True else None)


def s3_branch(t):
    x, y, ppm = RS.STAGE['forest_up']['kg']
    return _forest('up', t, lambda img, cam: RS.kg_on_branch(img, cam, x, RS.s_for(ppm), mood='kindly', wings='teach',
                                                              t=t, talk=_talk('kg', t)))


def s2_down(t):
    x, y, ppm = RS.STAGE['forest_down']['link']

    def cast(img, cam):
        RS.foot_shadow(img, cam, x, y, ppm, RS.SHADOW_W['link'])
        _kid(img, cam, 'link', x, y, ppm, t, 'unsure', j=RC.poses('link')['shrug'])
        a = t * 3.2                                                   # Navi circling him
        CR.navi(img, cam, x + 150 * math.cos(a), y - 1.05 * ppm + 40 * math.sin(a), RS.s_for(ppm) * 1.2, t=t)
    return _forest('down', t, cast)


def _close(view_fn, t, mood, navi=None, jolt=0.0, debris=None, cam_bg=None):
    """Link's close-up: the set, Link big at the close mark, Navi near his cheek."""
    img = B.canvas((0, 0, 0))
    cam = B.Cam(1.0)
    view_fn(img, cam_bg or cam, t)
    x, y, ppm = RS.STAGE['forest_close']['link']
    _kid(img, cam, 'link', x, y - 40 * jolt, ppm * (1 - 0.04 * jolt), t, mood)
    if navi:
        nx, ny, heat = navi
        CR.navi(img, cam, nx, ny, 1.25, t=t, heat=heat)
    if debris:
        debris(img, cam)
    return img


def s4_ok(t):
    u = t - SHOTS[3][1]
    nuz = 0.5 + 0.5 * math.sin(u * 5.0)                              # nuzzling in to his cheek and back
    img = _close(lambda im, c, tt: (RS.forest(im, c, 'close', tt)), t, 'sceptical',
                 navi=(735 - 45 * nuz, 1000 + 10 * math.sin(u * 9), 0.0))
    RS.forest_front(img, B.Cam(1.0), 'close', t)
    return img


def s6_god(t):
    u = t - SHOTS[5][1]
    jolt = ease(u / 0.15) if u < 0.6 else 1.0
    img = _close(lambda im, c, tt: RS.forest(im, c, 'close', tt), t, 'aghast', jolt=jolt,
                 navi=(800, 900 - 120 * ease(u / 0.2) + 20 * math.sin(u * 8), 0.0))
    RS.forest_front(img, B.Cam(1.0), 'close', t)
    return img


def s5_edge(t):
    u = t - SHOTS[4][1]
    gx, gy, gppm = RS.STAGE['forest_edge']['gunman']
    img = B.canvas((0, 0, 0))
    cam = B.Cam(1.0)
    RS.forest(img, cam, 'edge', t)
    snap = t - SNAP
    rise = ease((u - 0.2) / 0.8)
    # KG rises behind the gunman (drawn first: he is behind), glee from "Press R1"
    kx, ky, ks = 470, 1500 - 560 * rise, 1.05
    head = (190, 760)                                                 # the gunman's head on screen
    if snap > -0.5:                                                   # the wings close round the head
        hx, hy = (head[0] - kx) / ks, (head[1] - ky) / ks
        g = ease((snap + 0.5) / 0.35)
        wings = {'R': ((-160 - 40 * g, -200), (-180 + (hx - 60 + 180) * g, -300 + (hy + 300) * g), 'grip'),
                 'L': ((170 - 120 * g, -160), (200 + (hx + 80 - 200) * g, -180 + (hy - 20 + 180) * g), 'grip')}
    else:
        wings = 'up'
    j = _gun_pose()
    rot, hy_ = 0.0, None
    drop = 0.0
    if snap >= 0:
        hy_ = 180                                                     # the head turned right round
        rot = -14 * ease((snap - 0.15) / 0.4)
        drop = 60 * ease((snap - 0.15) / 0.4)
    if rise > 0:
        CR.kg(img, cam, kx, ky, ks, view='front', mood='glee', wings=wings, perched=False, t=t,
              talk=_talk('kg', t), part='all')
    _kid(img, cam, 'gunman', gx, gy + drop, gppm, t, j=j, yaw=90, head_yaw=hy_, rot=rot, talk=False)
    if 0 <= snap < 0.12:
        _flash(img, cam, head[0] + 30, head[1] + 60, 50, seed=3)
    if L[5]['start'] <= t:
        _prompt(img, 'R1', 'EXECUTION', 640, 330, t - L[5]['start'] - 0.05)
    return img


def _camp_cam(z=1.0, cx=W / 2, cy=H / 2):
    return B.Cam(z, cx, cy)


def _camp(t, cam, draw_navi=True, boom_view=False):
    """The camp at t through cam: the gate (blown in at GATE), the three gunmen (two gunned down, one blown up),
    KG firing, Link scuttling in, Navi by Link until she goes."""
    img = B.canvas((0, 0, 0))
    gate = ease((t - GATE) / 0.25)
    RS.camp(img, cam, t, gate)
    st = RS.STAGE['camp']
    kx, ky, kppm = st['kg']
    lx, ly, lppm = st['link']
    firing = FIRE0 <= t < FIRE1 and int(t * FPS) % 2 == 0
    marks = []
    for who in ('gunman1', 'gunman3', 'gunman2'):
        x, y, ppm = st[who]
        hit = {'gunman1': HIT1, 'gunman3': HIT3, 'gunman2': BOOM}[who]
        if t >= hit and who == 'gunman2':
            continue                                                  # blown apart
        rot = 0.0
        if t >= hit:
            rot = 80 * ease((t - hit) / 0.35)
        if (st[who][0], st[who][1]) and who != 'gunman1':
            RS.foot_shadow(img, cam, x, y, ppm, RS.SHADOW_W['gunman'])
        _kid(img, cam, who, x, y, ppm, t, j=_gun_pose(), yaw=90, flip=-1 if x > 540 else 1, rot=rot, talk=False)
        if hit <= t < hit + 0.3 and who != 'gunman2':
            _splat(img, cam, x - 0.1 * ppm, y - 1.3 * ppm, 0.28 * ppm, seed=len(who))
        if who == 'gunman2' and L[8]['start'] <= t < BOOM and int(t * FPS) % 3 == 0:   # he fires back
            _flash(img, cam, x - 1.05 * ppm, y - 1.32 * ppm, 0.16 * ppm, seed=int(t * 12))
        marks.append((who, x, y, ppm))
    # Link scuttles in from the left, front on, low (hands over ears), wince
    if t >= SCUTTLE[0]:
        u = ease((t - SCUTTLE[0]) / (SCUTTLE[1] - SCUTTLE[0]))
        x = -150 + (lx + 150) * u
        bob = 18 * abs(math.sin((t - SCUTTLE[0]) * 14)) * (1 - u)
        j = V.standing(RC.CAST['link'])
        sw = RC.CAST['link']['shoulders']
        for s_, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s_, (sg * (sw + 10), -150.0, 40.0), 'down', 'palm')
        j['head_dy'] = 20
        RS.foot_shadow(img, cam, x, ly, lppm, RS.SHADOW_W['link'])
        _kid(img, cam, 'link', x, ly - bob, lppm, t, 'wince', j=j)
    # KG standing, the MG42 furled in his wings, war face, bandana
    s = RS.s_for(kppm)
    RS.foot_shadow(img, cam, kx, ky, kppm, RS.SHADOW_W['kg'])
    rec = 6 if firing else 0
    hands = CR.kg(img, cam, kx - rec, ky - 272 * s, s, view='front', perched=False, stand=True, wings='gun', band=True,
                  mood='war', t=t, talk=_talk('kg', t))
    hx = max(h[0] for h in hands.values()) / B.SS
    hy = sum(h[1] for h in hands.values()) / 2 / B.SS
    # hands are screen px through cam; back to world for the flash
    mx = (hx - W / 2) / cam.z + cam.cx + 330 * s
    my = (hy - H / 2) / cam.z + cam.cy - 20 * s
    if firing:
        _flash(img, cam, mx + 30 * s, my, 46 * s, seed=int(t * FPS))
        d = ImageDraw.Draw(img)
        for who, x, y, ppm in marks:
            if who != 'gunman2':
                d.line([cam.P(mx + 60 * s, my), cam.P(x - 0.1 * ppm, y - 1.3 * ppm)], fill=(255, 230, 120), width=int(3 * cam.z * B.SS))
        for k in range(3):                                            # cases falling
            cx = mx - 240 * s + 30 * k
            ay = (t * 5 + k * 0.3) % 1
            d.rectangle([cam.P(cx, my + 40 * s + ay * 200 * s), cam.P(cx + 8, my + 52 * s + ay * 200 * s)], fill=(210, 170, 70))
    if GATE <= t < GATE + 0.18:
        g0, g1 = RS.CAMP.p(0, RS.WALL_D, 1.2)
        _flash(img, cam, g0, g1, 220, seed=11)
    # Navi: by Link, then red, then zip, then the blast
    if draw_navi and t < BOOM:
        nx, ny = (lx + 90, ly - 1.25 * lppm) if t >= SCUTTLE[1] else (kx - 1.0 * kppm, ky - 1.6 * kppm)
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
        _prompt(img, 'R2', 'GRENADES', 540, 330, t - L[9]['start'] - 0.05)
    return img


def s7_camp(t):
    return _camp(t, B.Cam(1.0))


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
    for who, (x, y, ppm) in st.items():
        if who != 'kg':
            RS.foot_shadow(img, cam, x, y, ppm, RS.SHADOW_W.get(who, 0.55))
    for who, (x, y, ppm) in sorted(st.items(), key=lambda kv: kv[1][1]):
        s = RS.s_for(ppm)
        if who == 'kg':
            sweep = ease((t - L[11]['start']) / 1.5)
            wing = {'L': ((300, -120 - 80 * sweep), (480 + 40 * sweep, -200 - 240 * sweep), 'spread'),
                    'R': ((-192, -30), (-172, 90), 'fold')}
            CR.kg(img, cam, x, y - 272 * s, s, view='front', perched=False, stand=True, wings=wing, mood='show', t=t,
                  talk=_talk('kg', t))
        elif who == 'goron':
            CR.goron(img, cam, x, y, s, t=t)
        else:
            jj = dict(next(iter(RC.poses(who).values())))
            mood = jj.get('_mood')
            if who == 'saria' and t >= romance:
                mood = 'wink'
            if who == 'zelda':
                mood = 'down'
            bounce = 10 if (romance <= t < romance + 0.25 and who in ('malon', 'ruto')) else 0
            _kid(img, cam, who, x, y - bounce, ppm, t, mood, j=jj, talk=False)
    return img


def s11_nine(t):
    def bg(im, c, tt):
        RS.town(im, B.Cam(2.0, 540, 600), 'square', tt)
    return _close(bg, t, 'deadpan')


def _wall_scene(t, cam, shake=0.0):
    img = B.canvas((0, 0, 0))
    RS.town(img, cam, 'wall', t)
    st = RS.STAGE['town_wall']
    lx, base, ppm = st['link']
    kx = st['kg'][0]
    s = RS.s_for(ppm)
    u = ease((t - S12_AT) / (SLAM - S12_AT))
    hand_y = base - 272 * s - 485 * s                                 # his wings up high, holding Link off the cobbles
    k = RC.scale_for(RC.CAST['link'], s)
    lift = (base - 928 * k) - (hand_y - 70 * s)                       # his collar up at KG's grip
    sx = shake * 14 * math.sin(t * 60)
    ldx = 60 * (1 - u)
    j = V.standing(RC.CAST['link'])
    lx = kx - 335 * s                                                 # at KG's grip
    _kid(img, cam, 'link', lx + ldx + sx * 0.6, base - lift * u, ppm, t, 'terrified', j=j, talk=True)
    CR.navi(img, cam, 180, 760 + 20 * math.sin(t * 6), s * 1.2, t=t, heat=0.3 + 0.6 * ease((t - SLAM) / 7.0))
    CR.kg(img, cam, kx + ldx + sx, base - 272 * s, s, view='side', perched=False, stand=True, wings=LIFT, band=True,
          mood='fury', t=t, flip=-1, talk=_talk('kg', t))
    return img


LIFT = {'R': ((150, -300), (300, -500), 'grip'), 'L': ((170, -260), (330, -470), 'grip')}   # side: both wings up at
                                                                  # Link's collar, lifting him


def s12_wall(t):
    choices = L[14]['start'] + 1.2
    shake = 1.0 if (choices <= t < choices + 0.8 or SLAM <= t < SLAM + 0.15) else 0.0
    if shot_of(t) == 'S12b':                                          # 13b: a cut in closer for the shake
        st = RS.STAGE['town_wall']
        return _wall_scene(t, B.Cam(1.3, st['kg'][0] - 160, st['kg'][1] - 520), shake)
    return _wall_scene(t, B.Cam(1.0), shake)


def s13_pinned(t):
    st = RS.STAGE['town_wall']
    lx, base, ppm = st['link']
    s = RS.s_for(ppm)
    head = base - 272 * s - 485 * s - 230 * s                         # his face, held up at KG's grip
    return _wall_scene(t, B.Cam(2.1, st['kg'][0] - 300 * s, head + 120))


SHOT_FN = {'S1': s1_branch, 'S2': s2_down, 'S3': s3_branch, 'S4': s4_ok, 'S5': s5_edge, 'S6': s6_god,
           'S7': s7_camp, 'S8': s8_navi, 'S9': s9_horrible, 'S10': s10_square, 'S11': s11_nine, 'S12': s12_wall, 'S12b': s12_wall,
           'S13': s13_pinned}


def picture(t):
    if t >= BLACK_AT:
        return Image.new('RGB', (W, H), (0, 0, 0))
    img = SHOT_FN[shot_of(t)](t)
    return img.convert('RGB').resize((W, H), Image.LANCZOS) if img.size != (W, H) else img.convert('RGB')


# ================================================================================================ subtitles
def caption_at(t):
    for i, ln in enumerate(LINES):
        nxt = LINES[i + 1]['start'] - 0.05 if i + 1 < len(LINES) else 1e9
        if ln['start'] - 0.05 <= t < min(ln['end'] + 0.45, nxt):
            return SUB.line_caption(ln, t - ln['start'])   # a few words at a time, on the syllable they start with
    return None


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
    k = int((FIRE1 - FIRE0) * SR)
    burst = np.tile(mg, k // len(mg) + 1)[:k].copy()
    burst[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))
    filmkit.place(rest, burst, at=FIRE0, sr=SR, gain=0.35)
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
    faults = voices.bleep_check(sys.modules[__name__], [])
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
