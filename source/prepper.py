#!/usr/bin/env python3
"""PREPPER MINISTER (TikTok satire; brief prompts/prepper-minister.md, notes notes/prepper-minister.md). Andy Burnham's
calm stockpiling post on his TikTok turns into a robot invasion of his London house; he and Wes Streeting fight them
off. Built from source/satire_template.py; the house is one 3D set (prepper_set.py, from the plan in metres in
prepper_plan.py), every shot a camera on it; the robots are real 3D figures (prepper_robot.py); the people, their
outfits and what they hold are in prepper_cast.py; the things in the rooms and the effects in prepper_fx.py.

    python3 source/prepper.py cast OUT.jpg               the cast sheet (every view; Andy's fear 1-6; the props)
    python3 source/prepper.py stills OUT_DIR T [T ...]   stills at these times (seconds)
    python3 source/prepper.py check                      the plan checks and the audit
    python3 source/prepper.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import prepper_cast as C         # noqa: E402  (installs the house style's hands, arms and limbs)
import figure as F               # noqa: E402
import mouths                    # noqa: E402
import mossad_audio as MA        # noqa: E402
import filmkit                   # noqa: E402
import film_engine as E          # noqa: E402
import views as V                # noqa: E402
import moves                     # noqa: E402
import prepper_plan as PL        # noqa: E402
import prepper_set as S          # noqa: E402
import prepper_robot as R        # noqa: E402
import prepper_fx as X           # noqa: E402
import audit as A                # noqa: E402
import clipcheck as CC           # noqa: E402

FPS, SR = 12, MA.SR
M = V.M_PER_UNIT
FLAT = S.FLAT

# =============================================== STORY ==============================================================
NAME = 'prepper-minister'
HANDLE = '@TheTikTokPM'                     # the TikTokPM frame from the final Cry Minister (name and description only)
DESCRIPTION = ''                            # Sam, 24 Oct: the TikTok description comes later
HOOK = ('Andy asks the UK to stockpile', {'y': 880})   # Sam, 24 Oct (finish.py adds it with the CranbriJoos sign-off)
# Each line: its recording (source/audio/prepper/), where its speech starts in the film (`at`), and its subtitles as
# (time in the recording, chunk): two to five words, each up on its first word; the punchline on its own.
LINES = [
    dict(n=1, who='Andy', audio='prepper/line-01-hello', at=0.25, text='Hello, Prime Minister here.',
         chunks=[(0.31, 'Hello,'), (0.87, 'Prime Minister here.')]),
    dict(n=2, who='Andy', audio='prepper/line-02-no-biggie', at=2.35, text='So, no biggie.',
         chunks=[(0.51, 'So,'), (1.5, 'no biggie.')]),
    dict(n=3, who='Andy', audio='prepper/line-03-stockpile', at=4.45, text='But you need to stockpile, now.',
         chunks=[(0.45, 'But you need to stockpile,'), (2.08, 'now.')]),
    dict(n=4, who='Andy', audio='prepper/line-04-i-mean', at=7.05, text='I mean, like, right now.',
         chunks=[(0.39, 'I mean,'), (1.01, 'like,'), (1.71, 'right now.')]),
    dict(n=5, who='Andy', audio='prepper/line-05-beans-water-crossbow-minigun', at=9.55, off=True,
         text="I don't just mean beans and water. Crossbow. Minigun.",
         chunks=[(0.86, "I don't just mean"), (1.8, 'beans and water.'), (3.37, 'Crossbow.'), (4.55, 'Minigun.')]),
    dict(n=6, who='Andy', audio='prepper/line-06-test-them', at=14.45, text='Test them. Test them on your Alexa.',
         chunks=[(0.59, 'Test them.'), (1.64, 'Test them'), (2.3, 'on your Alexa.')]),
    dict(n=7, who='Andy', audio='prepper/line-07-cant-stress', at=18.85, text="I can't stress how little time you have.",
         chunks=[(0.73, "I can't stress"), (1.75, 'how little time'), (2.75, 'you have.')]),
    dict(n=8, who='Wes', audio='prepper/line-08-wes-too-late', at=24.6, text="It's too late. They're here.",
         chunks=[(0.97, "It's too late."), (2.37, "They're here.")]),
    dict(n=9, who='Andy', audio='prepper/line-09a-beans', at=30.3,
         text='We are already out of time. Did you get the beans? DID YOU GET THE BEANS?',
         chunks=[(0.7, 'We are already'), (1.7, 'out of time.'), (3.29, 'Did you get the beans?'),
                 (4.99, 'DID YOU GET THE BEANS?')]),
    dict(n=10, who='Andy', audio='prepper/line-09b-streeting', at=38.9,
         text="Streeting, you pussy, there's a minigun in the kitchen.",
         chunks=[(0.84, 'Streeting,'), (1.42, 'you p****,'), (3.03, "there's a minigun"), (3.85, 'in the kitchen.')],
         bleep=(1.45, 1.95)),            # over "pussy" (the word gone); to be checked by ear on the animatic
]
T = dict(s1=0.0, s2=2.1, s3=4.2, s4=6.85, s5=9.3, s6=14.2, s7=18.6, s8=22.1, s9=28.3, s10=43.0, s11=48.0, s12=50.0,
         end=61.0)
SHOTS = [('s1', T['s1'], T['s2']), ('s2', T['s2'], T['s3']), ('s3', T['s3'], T['s4']), ('s4', T['s4'], T['s5']),
         ('s5', T['s5'], T['s6']), ('s6', T['s6'], T['s7']), ('s7', T['s7'], T['s8']), ('s8', T['s8'], T['s9']),
         ('s9', T['s9'], T['s10']), ('s10', T['s10'], T['s11']), ('s11', T['s11'], T['s12']), ('s12', T['s12'], T['end'])]
DUR = T['end'] + 0.4                        # shot 12 is 11 s (Sam, 24 Oct: was 7), then a hard cut to black
BLACK_AT = T['end']
FEAR_AT = {'s1': 1, 's2': 1, 's3': 3, 's4': 4, 's6': 3, 's7': 5, 's9': 6, 's11': 6, 's12': 6}   # notes: stress per shot
# The beats (seconds in the film). Shot 5: the items appear on the beat of each word.
ITEMS_AT = dict(beans=10.64, water=11.09, crossbow=12.06, minigun=13.24)
FIRE6 = 16.95                               # shot 6: he fires as "...Alexa." ends
BOLT6 = 0.8                                 # the bolt's flight (the camera follows it, the Alexa held in view: Sam)
DOOR8, ROBOT8, BOLT8 = 23.7, 26.2, 27.1     # shot 8: the door booted open; the robot over his shoulder; the bolt
SPIN9, LUNGE9, SHOTS9 = 29.4, 36.8, (37.3, 37.55, 37.8)
WINDOW10, PLASMA10, FIRE10 = 45.0, 45.6, 46.1
THROW11, DENT11 = 48.9, 49.6
# What the shared checks need
KEEP_CLEAR = []
PROP_SIZES = [('crossbow', 'crossbow', 0.72, 0.3, None), ('minigun', 'minigun', 0.9, 0.25, None),
              ('pistol', 'pistol', 0.186, 0.138, None), ('machete', 'machete', 0.6, 0.06, None),
              ('beans', 'can', 0.066, 0.11, None), ('water', '2L bottle', 0.105, 0.33, None),
              ('alexa', 'smart speaker', 0.1 * X.ALEXA_K, 0.09 * X.ALEXA_K, None), ('robot', 'robot', 0.6, 2.1, None)]
HEIGHTS = C.HEIGHTS
OUTFIT = {'Andy': {'shirt hem (tucked, belt)': 468}}
ALLOWED_CONTACTS = []
ALLOWED_POPS = []
# ====================================================================================================================


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def shot_start(t):
    return next((s[1] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][1])


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def keyed(t, keys):
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, a), (t1, b) in zip(keys, keys[1:]):
        if t <= t1:
            u = ease((t - t0) / max(1e-6, t1 - t0))
            if isinstance(a, tuple):
                return tuple(x + (y - x) * u for x, y in zip(a, b))
            return a + (b - a) * u
    return keys[-1][1]


# ------------------------------------------------------------------------------------------------ the voices
for ln in LINES:                                     # cut each recording in the silence before its first word
    v = MA.line(ln['audio'])
    st = MA.pauses(v, 0.12)
    onset = st[0][0]
    cut = max(0.0, onset - 0.15)
    ln['_cut'] = cut
    ln['_voice'] = v[int(cut * SR):]
    ln['start'] = ln['at'] - (onset - cut)
    ln['end'] = ln['start'] + len(ln['_voice']) / SR
    ln['_stretches'] = [(a - cut, b - cut) for a, b in st]
    if ln.get('bleep'):                              # the bleep: the word gone, a 1 kHz tone in its place
        b0, b1 = (int((x - cut) * SR) for x in ln['bleep'])
        n_ = b1 - b0
        tone = 0.18 * np.sin(2 * math.pi * 1000 * np.arange(n_) / SR)
        ramp = np.minimum(1, np.minimum(np.arange(n_), n_ - np.arange(n_)) / (0.006 * SR))
        ln['_voice'][b0:b1] = tone * ramp
TRACK = {}
for ln in LINES:
    if ln.get('off'):                                # shot 5: his voice over the empty kitchen (no mouth)
        continue
    joined = []                                      # bursts under 0.2 s apart are one phrase (the shouted "DID YOU
    for a, b in ln['_stretches']:                    # GET THE BEANS?" came as three, and ran out of words)
        if joined and a - joined[-1][1] < 0.2:
            joined[-1] = (joined[-1][0], b)
        else:
            joined.append((a, b))
    TRACK.setdefault(ln['who'], []).extend((a + ln['start'], b + ln['start'], sh)
                                           for a, b, sh in mouths.track(ln['text'], joined))
for k in TRACK:
    TRACK[k].sort()
BLINKS = {'Andy': F.blinks(7, 0.0, DUR, talking=True), 'Wes': F.blinks(11, 0.0, DUR, talking=True)}


def talking(who, t):
    return any(ln['who'] == who and not ln.get('off') and ln['start'] + ln['_stretches'][0][0] - 0.1 <= t <=
               ln['start'] + ln['_stretches'][-1][1] + 0.1 for ln in LINES)


def mouth_at(who, t):
    shape = mouths.at(TRACK.get(who, []), t)
    return None if shape == 'rest' else 'v:' + shape


SUBS = None


def caption_at(t):
    global SUBS
    if SUBS is None:
        out = []
        for ln in LINES:
            for i, (a, c) in enumerate(ln['chunks']):
                out.append([ln['start'] + (a - ln['_cut']) + 0.1, ln['end'] + 0.25, c])
        out.sort()
        for i in range(len(out) - 1):
            out[i][1] = min(out[i][1], out[i + 1][0])
        SUBS = [tuple(x) for x in out]
    for t0, t1, c in SUBS:
        if t0 <= t < t1:
            return c
    return None


# ------------------------------------------------------------------------------------------------ cameras
def lerp3(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


BOLT6_FROM = (-1.62, 1.33, 2.2)                      # the crossbow's tip (shot 6)
ALEXA = (PL.THINGS['alexa']['at'][0], 0.92, PL.THINGS['alexa']['at'][1])
BOLT6_TO = (ALEXA[0], ALEXA[1] + 0.05 * X.ALEXA_K, ALEXA[2])


def _stuck():
    """Where the bolt ends up (Sam, 24 Oct: sticking out of the wall): through the Alexa, on nearly level into the
    splashback just above the worktop, its shaft and vanes standing out towards the room."""
    d = np.subtract(BOLT6_TO, BOLT6_FROM)
    d = np.array([d[0], 0.0, d[2]]) / math.hypot(d[0], d[2])
    d[1] = -0.12
    k = (5.4 - BOLT6_TO[2]) / d[2]
    return (BOLT6_TO[0] + d[0] * k, 1.1, 5.4), tuple(d)


def bolt6_at(t):
    u = (t - FIRE6) / BOLT6
    return lerp3(BOLT6_FROM, BOLT6_TO, min(1.0, max(0.0, u)))


BOLT6_STUCK = _stuck()


def cam_for(t):
    s = shot_of(t)
    u = t - shot_start(t)
    if s in ('s1', 's4'):
        return S.Cam((3.0, 1.15, 0.35), (3.0, 1.02, 3.7), focal=1500)
    if s in ('s2', 's7'):
        return S.Cam((3.0, 1.1, 1.5), (3.0, 1.0, 3.7), focal=1500)
    if s == 's3':
        return S.Cam((3.0, 1.12, 2.92), (3.0, 1.1, 3.75), focal=1500)
    if s == 's5':
        return S.Cam((-2.8, 1.45, 0.9), (-2.8, 0.98, 2.7), focal=1350)
    if s == 's6':
        # Andy waist up in three-quarter, from his right-front (the fridge behind him); on the shot the camera swings
        # after the bolt and rides behind it across the kitchen to the Alexa, settling a metre from it
        start, look0 = (-2.3, 1.42, 1.49), (-1.38, 1.28, 1.92)
        if t < FIRE6 + 0.08:
            return S.Cam(start, look0, focal=1650)
        b = bolt6_at(t)
        d = np.subtract(BOLT6_TO, BOLT6_FROM)
        d = d / np.linalg.norm(d)
        k = ease((t - FIRE6 - 0.08) / 0.35)
        chase = tuple(np.add(b, -d * 0.7) + np.array([0.1, 0.35, 0.0]))   # high enough to clear the island's bottles
        end = (-3.75, 1.12, 4.42)
        if t > FIRE6 + BOLT6:
            v = ease((t - FIRE6 - BOLT6) / 0.5)
            pos = lerp3(chase, end, v)
        else:
            pos = lerp3(start, chase, k)
        look = lerp3(look0, ALEXA, ease((t - FIRE6 - 0.08) / 0.3))   # Sam: the Alexa seen clearly before the bolt lands
        return S.Cam(pos, look, focal=1650 - 450 * k)
    if s == 's8':
        pts = PL.smooth(PL.CAMS[8]['path'])
        k = ease(u / 1.5)
        i = min(len(pts) - 1, int(k * (len(pts) - 1)))
        look = lerp3((3.0, 1.0, 3.7), PL.CAMS[8]['look'], ease(u / 1.3))
        return S.Cam(pts[i], look, focal=1150)
    if s == 's9':
        return S.Cam((3.0, 1.15, 0.35), (2.7, 1.15, 5.4), focal=760)
    if s == 's10':
        return S.Cam((-0.6, 1.45, 2.7), (-4.5, 1.3, 2.7), focal=1100)
    if s == 's11':
        if t < THROW11:
            return S.Cam((-2.35, 1.12, 2.05), (-2.5, 0.95, 2.6), focal=1400)
        k = ease((t - THROW11) / 0.6)
        tin = tin11_at(t)
        return S.Cam(lerp3((-2.35, 1.12, 2.05), (-1.6, 1.35, 3.4), k), lerp3((-2.5, 0.95, 2.6), tin, k), focal=1400 - 300 * k)
    o = PL.CAMS[12]['orbit']
    pos = PL.orbit_pos(min(u, o['seconds']), o)
    return S.Cam(pos, (o['centre'][0], PL.CAMS[12]['look_y'], o['centre'][1]), focal=900)


# ------------------------------------------------------------------------------------------------ placing people
def put(img, cam, sp, x, z, facing, j, t, head_facing=None, lift=0.0, shadow=True):
    """Someone at floor point (x, z) facing `facing` (plan degrees: 0 north, 90 east), through the camera: their
    height sets their scale; soles on the floor point; a flat shadow under them. Returns the drawing frame."""
    h = HEIGHTS.get(sp.get('name'), 1.75)
    f = h / 1.75
    neck = 928 * M * f + lift
    if cam.depth((x, neck, z)) < 0.3:
        return None
    if shadow:
        ring = [(x + 0.3 * math.cos(u), 0.004, z + 0.22 * math.sin(u)) for u in np.linspace(0, 2 * math.pi, 16)]
        if all(cam.depth(q) > 0.2 for q in ring):
            lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            B.Pen(lay, FLAT).poly([cam.project(q)[0] for q in ring], (0, 0, 0, 55), None)
            img.alpha_composite(lay)
    (Xn, Yn), k = cam.project((x, neck, z))
    (Xf, Yf), _ = cam.project((x, lift, z))
    s = max(1e-3, (Yf - Yn) / 928.0) if Yf > Yn else k * M * f
    if s > 6.0:
        return None
    X_ = Xf if Yf > Yn else Xn
    Y_ = Yf - 928 * s if Yf > Yn else Yn
    fd = (math.sin(math.radians(facing)), math.cos(math.radians(facing)))
    yaw = cam.yaw_of((x, 0, z), fd)
    hy = None
    if head_facing is not None:
        hd = (math.sin(math.radians(head_facing)), math.cos(math.radians(head_facing)))
        hy = cam.yaw_of((x, 0, z), hd)
    j2 = C.person(img, FLAT, X_, Y_, s, dict(sp, full=True, pose='custom'), t, yaw, j, hy)
    view, mirror = V.snap(yaw)
    return dict(X=X_, Y=Y_, s=s, yaw=yaw, j2=j2, L=B.Local(FLAT, X_, Y_ + (j.get('bob', 0.0) if j else 0.0) * s, s,
                                                            -1 if mirror else 1))


def sofa_pose(sp, lean=8.0):
    j = moves.seated(sp)
    j['seated'] = False                              # on the sofa (the set draws it), never the library's chair
    j['lean'] = lean
    return j


# ------------------------------------------------------------------------------------------------ Andy
WAVE = filmkit.Beats([(0.3, 'set-up', (150, 300, 60)), (0.6, 'raise', (240, 0, 220)), (0.85, 'flick', (280, -20, 210), 'fast'),
                      (1.05, 'back', (240, 0, 220)), (1.6, 'down', (150, 300, 60), 'slow')])   # held out clear of the
#                                                         shoulder (25 Oct: the elbow folded too tight at 0.5 s)


def andy_sofa(t, s):
    """Andy on the sofa (shots 1-4, 7): leaning forward to the lens, talking to us; his gestures per shot."""
    sp = C.fear(C.ANDY, FEAR_AT.get(s, 1), talking=talking('Andy', t))
    m = mouth_at('Andy', t)
    sp['mouth'] = m or sp.get('mouth') or C.FEAR[max(0, min(5, FEAR_AT.get(s, 1) - 1))]['mouth']   # between words
    if FEAR_AT.get(s, 1) >= 4 and not m:
        sp['mouth'] = 'set'
    sp['blink'] = F.blinking(t, BLINKS['Andy'])
    sp['look'] = 0.0
    sp['tilt'] = filmkit.shifts(t, seed=3, amount=0.03)
    j = sofa_pose(sp, lean=10.0 if s in ('s1', 's4') else 14.0)
    u = t - shot_start(t)
    sw = sp.get('shoulders', 150)
    if s == 's1':                                    # a small flick of a wave, right hand
        hx, hy, hz = WAVE.at(u)
        V.arm_to(j, 'R', (hx, hy, hz), 'out', 'palm' if hy < 100 else 'fist')
    elif s == 's2':                                  # right hand rolling in a circle; left elbow on his knee
        a = u * 5.0
        V.arm_to(j, 'R', (150 + 40 * math.cos(a), 170 + 40 * math.sin(a), 200), 'out', 'palm')
        V.arm_to(j, 'L', (-70, 420, 260), 'down', 'fist')
        j['lean'] = 22
    elif s == 's3':                                  # rictus, a slight tremble (deliberate: listed in allow)
        sp['tilt'] = 0.02 * math.sin(t * 37) + 0.015 * math.sin(t * 23)
    elif s == 's4':                                  # imploring: both hands open to us, pressing on the words
        k = 0.5 + 0.5 * math.sin(u * 4.0)
        for sd, sg in (('R', 1), ('L', -1)):
            V.arm_to(j, sd, (sg * 120, 220 - 20 * k, 260 + 30 * k), 'down', 'palm')
    elif s == 's7':                                  # urging desperately: hands together, shaking on the beats
        k = math.sin(u * 7.0)
        for sd, sg in (('R', 1), ('L', -1)):
            V.arm_to(j, sd, (sg * 40, 200 + 15 * k, 260), 'down', 'fist')
    return sp, j


# ------------------------------------------------------------------------------------------------ the island
TIN_SPOTS = [(-3.35, 2.62), (-3.22, 2.85), (-3.05, 2.6)]
BOTTLE_SPOTS = [(-2.75, 2.82), (-2.58, 2.6)]
CROSSBOW_SPOT = ((-2.15, 2.55), 75)
MINIGUN_SPOT = ((-2.55, 2.95), 100)


def island_items(t):
    """What stands on the island when: shot 5 has them appear on the beat of each word; the crossbow goes with Andy
    (shots 6, 8, 9); Wes takes the minigun in shot 10; Andy throws a tin in shot 11."""
    s = shot_of(t)
    items = []
    if s == 's5':
        for i, spot in enumerate(TIN_SPOTS):
            if t >= ITEMS_AT['beans'] + 0.08 * i:
                items.append(('tin', spot))
        for i, spot in enumerate(BOTTLE_SPOTS):
            if t >= ITEMS_AT['water'] + 0.08 * i:
                items.append(('bottle', spot))
        if t >= ITEMS_AT['crossbow']:
            items.append(('crossbow', CROSSBOW_SPOT))
        if t >= ITEMS_AT['minigun']:
            items.append(('minigun', MINIGUN_SPOT))
        return items
    items += [('tin', sp_) for sp_ in TIN_SPOTS]
    items += [('bottle', sp_) for sp_ in BOTTLE_SPOTS]
    if s == 's6':
        items.append(('minigun', MINIGUN_SPOT))
        return items
    if t < T['s10'] + 1.0:
        items.append(('minigun', MINIGUN_SPOT))
    if t >= THROW11 - 0.6:
        items = [it for it in items if not (it[0] == 'tin' and it[1] == TIN_SPOTS[2])]
    items = [it for it in items if not (it[0] in ('tin', 'bottle') and item_gone(it[0], t))]   # blown up (shot 12)
    return items


def draw_island_items(img, cam, t):
    for kind, spot in sorted(island_items(t), key=lambda it: -math.dist(cam.pos, (it[1][0][0] if it[0] in ('crossbow', 'minigun') else it[1][0], 0.95,
                                                                                    it[1][0][1] if it[0] in ('crossbow', 'minigun') else it[1][1]))):
        if kind == 'tin':
            X.tin(img, cam, (spot[0], 0.92, spot[1]))
        elif kind == 'bottle':
            X.bottle(img, cam, (spot[0], 0.92, spot[1]))
        elif kind == 'crossbow':
            X.crossbow3(img, cam, (spot[0][0], 0.92, spot[0][1]), spot[1])
        elif kind == 'minigun':
            X.minigun3(img, cam, (spot[0][0], 0.92, spot[0][1]), spot[1])


# ------------------------------------------------------------------------------------------------ the Alexa (shot 6)
ALEXA_BOX = (-5.55, -0.05, 0.05, 5.35)               # where its pieces can fly (the kitchen)
TOPS = [(-5.6, -1.8, 4.75, 5.4, 0.92), (-4.0, -1.6, 2.2, 3.2, 0.92), (-5.6, -4.95, 0.65, 4.75, 0.92)]
ALEXA_BITS = (X.burst(FIRE6 + BOLT6, (ALEXA[0], ALEXA[1] + 0.05, ALEXA[2]), 16, 2.2, 61, col=(66, 68, 74), size=0.025,
                      up=1.6, dirn=(-0.5, 0.0, 0.5), box=ALEXA_BOX, tops=TOPS) +
              X.burst(FIRE6 + BOLT6, (ALEXA[0], ALEXA[1] + 0.05, ALEXA[2]), 8, 2.0, 62, col=(40, 140, 80), size=0.02,
                      up=1.4, dirn=(-0.5, 0.0, 0.3), box=ALEXA_BOX, tops=TOPS) +
              X.burst(FIRE6 + BOLT6, (ALEXA[0], ALEXA[1] + 0.05, ALEXA[2]), 6, 1.8, 63, col=(20, 20, 24), size=0.03,
                      up=1.2, dirn=(-0.4, 0.0, 0.4), box=ALEXA_BOX, tops=TOPS))
ALEXA_BALL = X.Piece((ALEXA[0], ALEXA[1] + 0.05 * X.ALEXA_K, ALEXA[2]), (-1.2, 1.5, -0.3), FIRE6 + BOLT6, r=0.05 * X.ALEXA_K, e=0.3, spin=3,
                     box=ALEXA_BOX, tops=TOPS)


ln6 = next(ln for ln in LINES if ln['n'] == 6)
TURN6 = ln6['start'] + (ln6['chunks'][1][0] - ln6['_cut']) - 0.05   # on the second "Test them"
LOOK6 = 245.0                                     # from where he stands, towards the lens


def andy6(t):
    """Shot 6: Andy waist up, grim focus down the sights (fear 3), firing as the line ends; the recoil."""
    sp = C.fear(C.ANDY, 3, talking=talking('Andy', t))
    sp['mouth'] = mouth_at('Andy', t) or 'set'
    sp['blink'] = F.blinking(t, BLINKS['Andy']) and t < FIRE6 - 0.4
    sp['brows'] = 'serious'
    aim_yaw = 317.0
    j = C.crossbow_aim(sp, (0.0, 4.0), loaded=t < FIRE6)
    if FIRE6 <= t < FIRE6 + 0.25:                    # the kick of the shot
        j['lean'] = -3
        j['head_dy'] = -4
    # Sam, 24 Oct: he says "Test them." to us, then his head snaps round to the sights on "Test them on your Alexa"
    head = LOOK6 if t < TURN6 else None
    return sp, j, aim_yaw, head


# ------------------------------------------------------------------------------------------------ shot 12
# Sam's notes 3-11 (24 Oct): 11 s instead of 7; the camera's loop slowed to match (one turn in 11 s, prepper_plan); six
# robots, each with its own beat timed to when the camera faces it (the loop starts south-east and goes round
# anticlockwise: east at 1.6 s, north at 4.4 s, west at 7.1 s, south at 9.9 s): robot 4 at the window while the camera
# looks west; robot 1's blade at Andy seen from the north-west, past Wes; robots 2, 3 and 6 in the wide opening while
# it looks east; robot 5 blown apart while it looks north. Every robot path stays clear of the camera while it passes.
U12 = lambda t: t - T['s12']
ANDY12, WES12 = PL.PEOPLE['andy (11, 12)']['at'], PL.PEOPLE['wes (12)']['at']
SPEC = {   # each robot: its arms (A cannon, B blade, C and D cannon, 1-2 blade, 3-5 cannon: Sam, 24 Oct; 6 cannon)
    'A': dict(arms={'R': 'cannon', 'L': 'hand'}), 'B': dict(arms={'R': 'blade', 'L': 'hand'}),
    'C': dict(arms={'R': 'cannon', 'L': 'hand'}), 'D': dict(arms={'R': 'hand', 'L': 'cannon'}),
    '1': dict(arms={'R': 'blade', 'L': 'hand'}), '2': dict(arms={'R': 'hand', 'L': 'blade'}),
    '3': dict(arms={'R': 'cannon', 'L': 'hand'}), '4': dict(arms={'R': 'cannon', 'L': 'hand'}),
    '5': dict(arms={'R': 'cannon', 'L': 'hand'}), '6': dict(arms={'R': 'cannon', 'L': 'hand'}),
    '7': dict(arms={'R': 'cannon', 'L': 'hand'}), '8': dict(arms={'R': 'hand', 'L': 'cannon'}),
}
# Wes's aim (plan degrees, unwrapped so he swings the short way): robot 4 at the window, round past the hall door to
# robot 2 in the wide opening, robot 6 under it, back to robot 5 coming in from the hall, then on at the opening.
# Sam, 24 Oct: once robot 4 blew he held on the empty window and read as staring at Andy: he now swings the long way
# round (never past Andy) onto robot 3 coming in from the lounge, then on to robot 2
WES_AIM = [(0.0, 236.0), (1.4, 246.0), (2.85, 244.0), (3.45, 468.0), (4.3, 462.0), (4.6, 448.0), (7.2, 451.0), (7.45, 486.0), (8.35, 486.0),
           (8.9, 409.0), (9.85, 409.0), (10.3, 430.0), (11.0, 455.0)]
# Andy: robot 4 (west), a snap turn to robot 1 coming from the east, on his knees under its blade, up again, robot 3.
ANDY_AIM = [(0.0, 282.0), (3.0, 282.0), (3.15, 72.0), (5.6, 72.0), (5.75, 92.0), (8.5, 92.0), (8.75, 29.0), (11.0, 29.0)]
ANDY_SHOTS = [(1.4, '4'), (1.65, '4'), (1.9, '4'), (4.55, '3'), (4.75, '3'), (5.25, '3'), (5.4, '3'), (5.95, '1'),
              (6.15, '1'), (7.15, '1h'), (7.35, '1h'), (9.0, '5'), (9.25, '5'), (9.5, '5')]
DODGES = [(0.45, 0.95, -1), (2.45, 2.95, -1), (3.95, 4.45, 1), (4.85, 5.35, 1)]   # (from, to, side): out of the plasma
KNEEL = (6.4, 6.65, 7.9, 8.5)                        # down, on his knees, up again (the blade passes over him)
SWIPE = (6.1, 6.55, 6.9)                             # robot 1: wind-up, the swipe across, through
HEAD1 = 7.35                                         # Andy shoots robot 1's head off (the camera west: Andy nearest,
DIES = {'2': 7.2, '6': 8.35, '3': 5.6}               # the robot beyond him); cut down (robots 4 and 5 blown apart)
# Sam's note 17 (24 Oct): robot 4 takes the hits (holes, sparks, a jolt each) and explodes like robot 5, while the
# camera still faces the window (it turns away from about 3.2 s)
BLOWN = {'4': 2.75, '5': 9.8}
BLOWN5 = BLOWN['5']
# Robots 7 and 8 (note 17): cannons, stalking across the west garden towards the window; still far short of it when
# the camera turns away, and never inside in this shot (my call on their timing)
GARDEN = {'7': ((-12.2, 0.7), (-7.4, 1.9)), '8': ((-12.8, 4.7), (-7.9, 3.3))}
# The plasma (robot, seconds, what it is aimed at): every shot misses its man (he dodges or it goes wide) and burns
# where it lands; robot 6's two blow up the tins and bottles on the island, two of robot 5's take out the pendants.
PLASMA12 = [('4', 0.5, 'andy'), ('5', 2.0, 'wes'), ('4', 2.5, 'andy'), ('3', 4.0, 'andy'), ('3', 4.9, 'andy'),
            ('5', 5.2, 'wes'), ('6', 6.0, 'tins'), ('6', 6.9, 'bottles'), ('5', 7.6, 'pendant 2'), ('5', 8.4, 'pendant 0'),
            ('5', 9.05, 'wes')]
PLASMA_SPEED = 9.0                                   # metres a second


def bearing(a, b):
    return math.degrees(math.atan2(b[0] - a[0], b[1] - a[1])) % 360


def pendant_at(k):
    ix, iz = PL.THINGS['island']['at']
    return (ix + (-0.7, 0.0, 0.7)[k], S.CEIL - 0.7 + 0.08, iz)


def plasma_aim(what, t):
    """Where a plasma shot is aimed (a world point)."""
    if what == 'andy':
        return (ANDY12[0], 1.3, ANDY12[1])
    if what == 'wes':
        return (WES12[0] + 0.35, 1.45, WES12[1] - 0.2)
    if what == 'tins':
        return (TIN_SPOTS[1][0], 0.97, TIN_SPOTS[1][1])
    if what == 'bottles':
        return (BOTTLE_SPOTS[0][0], 1.05, BOTTLE_SPOTS[0][1])
    return pendant_at(int(what[-1]))


def next_plasma(name, u):
    """The plasma shot this robot is aiming at (its next one, or its last)."""
    mine = [(t0, what) for n, t0, what in PLASMA12 if n == name]
    if not mine:
        return None
    return next(((t0, w) for t0, w in mine if t0 >= u - 0.15), mine[-1])


def aim_cannon(p, name, u, height=1.62):
    nxt = next_plasma(name, u)
    if nxt:
        a, pole = R.aim(plasma_aim(nxt[1], T['s12'] + nxt[0]), p['pos'], p['yaw'], 'R', height=height)
        p['handR'], p['poleR'] = a, pole
    return p


def andy_holes(name, sp):
    for i, (s_, who) in enumerate(ANDY_SHOTS):
        if who == name:
            sp['holes'].append(dict(part='chest', i=30 + 41 * i, t=T['s12'] + s_ + 0.03, r=0.026))


def robot_pose(name, t):
    """Every robot's pose at time t (and its spec, with damage so far). Bodies stay where they fall."""
    sp = dict(SPEC[name], name='robot ' + name)
    sp['holes'] = []
    if name == 'A':                                   # shot 8: in the hall behind Wes; the bolt; falls back
        x, z = PL.ROBOTS['robot A (8)']['at']
        p = R.pose(pos=(x, z), yaw=180, sweep=R.eye_sweep(t))
        if t < ROBOT8:
            p['pos'] = (x + 1.2, z)
            p['yaw'] = 270
        elif t < ROBOT8 + 0.5:
            p['pos'] = lerp3((x + 1.2, 0, z), (x, 0, z), ease((t - ROBOT8) / 0.5))[::2]
        if t >= BOLT8 + 0.08:
            sp['dead'] = True
            k = ease((t - BOLT8 - 0.08) / 0.6)
            p['fall'] = (88 * k, 0.0)
            p['head_pitch'] = -20 * k
        return p, sp
    if name == 'B':                                   # shot 9: lunges from the left (the wide opening); shot; drops
        x, z = PL.ROBOTS['robot B (9)']['at']
        if t < LUNGE9:
            return None, sp
        k = ease((t - LUNGE9) / 0.35)
        pos = lerp3((-0.6, 0, 2.2), (x + 0.9, 0, z), k)[::2]
        p = R.pose(pos=pos, yaw=90, lean=25 * k, sweep=R.eye_sweep(t))
        p['handR'] = (0.45, 1.5 - 0.5 * k, 0.5)
        for i, ts in enumerate(SHOTS9):
            sp['holes'].append(dict(part='chest', i=40 + 37 * i, t=ts + 0.04))
        if t >= SHOTS9[-1] + 0.1:
            sp['dead'] = True
            k2 = ease((t - SHOTS9[-1] - 0.1) / 0.7)
            p['fall'] = (90 * k2, 270)
        return p, sp
    if name in ('C', 'D'):                            # shot 10: at the kitchen window; shot through the glass; fall back
        z = 1.9 if name == 'C' else 3.0
        if t < WINDOW10:
            return None, sp
        p = R.pose(pos=(-6.05, z), yaw=90, sweep=R.eye_sweep(t, 0.3 if name == 'D' else 0.0))
        if t >= FIRE10 + (0.3 if name == 'C' else 0.9):
            sp['dead'] = True
            k = ease((t - FIRE10 - (0.3 if name == 'C' else 0.9)) / 0.6)
            p['fall'] = (88 * k, 270)
        return p, sp
    if name == '5' and shot_of(t) == 's11':           # shot 11: in the hall-to-kitchen door; the tin dents off it
        p = R.pose(pos=(-1.2, 5.65), yaw=180, lean=12, sweep=R.eye_sweep(t))
        return p, sp
    if t < T['s12']:
        return None, sp
    u = U12(t)
    if name == '1':                                   # from the lounge at Andy; the swipe over him; its head off
        start, end = (2.0, 1.7), (-2.05, 1.75)
        if u < 1.6:
            return None, sp
        p = R.pose(**R.walk(min(u, 6.0), start, end, 1.6, 6.0, stride=0.5))
        p['sweep'] = R.eye_sweep(t)
        reach = (0.3, 1.45, 0.62)                     # the blade arm held out in front as it comes
        wind, cut, thru = SWIPE
        if u < wind:
            p['handR'] = reach
        elif u < cut:
            p['handR'] = lerp3(reach, (0.6, 1.78, 0.12), ease((u - wind) / (cut - wind)))
        else:
            p['handR'] = lerp3((0.6, 1.78, 0.12), (-0.5, 1.5, 0.5), ease((u - cut) / (thru - cut)))
        andy_holes('1', sp)
        if u >= HEAD1:
            sp['headless'] = True
            k = ease((u - HEAD1 - 0.15) / 0.9)
            p['fall'] = (88 * k, 91.0)                # back the way it came, along the floor clear of the camera
            p['lean'] = 10 * k
        return p, sp
    if name == '2':                                   # in from the lounge, blade out; Wes cuts it down
        if u < 4.6:
            return None, sp
        p = R.pose(**R.walk(min(u, 7.0), (1.6, 3.6), (-0.7, 3.5), 4.6, 7.0, stride=0.5, phase=0.3))
        p['handL'] = (-0.3, 1.45, 0.62)
        p['sweep'] = R.eye_sweep(t, 0.4)
    elif name == '3':                                 # in from the lounge, firing at Andy
        if u < 2.4:
            return None, sp
        p = R.pose(**R.walk(min(u, 3.8), (1.4, 2.6), (-0.35, 2.7), 2.4, 3.8, stride=0.45))
        p['yaw'] = bearing(p['pos'], ANDY12)          # its cannon on him as it comes
        aim_cannon(p, '3', u)
        p['sweep'] = R.eye_sweep(t, 0.7)
        andy_holes('3', sp)
    elif name == '4':                                 # in through the shot-out window, onto the sink run, firing
        keys = [(0.0, R.pose(pos=(-6.0, 2.3), yaw=90, lean=55, y=0.15, handR=(0.3, 1.2, 0.75), handL=(-0.3, 1.2, 0.75))),
                (1.2, R.pose(pos=(-5.6, 2.3), yaw=90, lean=70, y=0.75, handR=(0.3, 1.0, 0.85), handL=(-0.3, 1.0, 0.85),
                             footR=(0.13, 0.5, -0.4), footL=(-0.13, 0.3, -0.5))),
                (2.2, R.pose(pos=(-5.25, 2.3), yaw=90, lean=30, y=0.92 - 0.38, footR=(0.13, 0.46, 0.25),
                             footL=(-0.13, 0.46, -0.1), handR=(0.3, 0.95, 0.4), handL=(-0.3, 0.95, 0.4))),
                (11.0, R.pose(pos=(-5.22, 2.3), yaw=95, lean=24, y=0.92 - 0.38, footR=(0.13, 0.46, 0.25),
                              footL=(-0.13, 0.46, -0.1), handR=(0.3, 0.95, 0.4), handL=(-0.3, 0.95, 0.4)))]
        p = keys[0][1]
        for (t0, a), (t1, b) in zip(keys, keys[1:]):
            if u >= t0:
                p = R.blend(a, b, ease((u - t0) / (t1 - t0)))
        p['sweep'] = R.eye_sweep(t, 0.2)
        if 0.3 <= u <= 0.8 or u > 2.2:               # a shot from the sill as it climbs; then crouched, firing
            aim_cannon(p, '4', u, height=p.get('y', 0.0) + 1.1 + (0.5 if u < 1 else 0.0))
        andy_holes('4', sp)
        jolt = 0.0                                    # each round that strikes it knocks it back a little
        for k, h in enumerate(h for h in (WES_HITS or []) if h[4] == 'robot 4'):
            if 0 <= t - h[0] < 0.12:
                jolt += (5.0 if k % 2 else 3.0) * (1 - (t - h[0]) / 0.12)
        for s_, who in ANDY_SHOTS:
            if who == '4' and 0 <= u - s_ < 0.25:
                jolt += 9.0 * (1 - (u - s_) / 0.25)
        p['lean'] = p.get('lean', 0.0) - jolt
        if u >= BLOWN['4']:                           # blown apart on the sink run: the legs left, toppling back
            sp['dead'] = True
            sp['headless'] = True
            sp['lost'] = {'armR', 'armL', 'chest', 'ridge', 'cowl', 'shoulder', 'flare', 'rib'}
            k = ease((u - BLOWN['4'] - 0.1) / 0.5)
            p['fall'] = (80 * k, 270.0)
        return p, sp
    elif name in GARDEN:                              # stalking across the garden towards the window
        a, b = GARDEN[name]
        p = R.pose(**R.walk(u, a, b, 0.0, 11.0, stride=0.42, phase=0.5 if name == '8' else 0.0))
        p['sweep'] = R.eye_sweep(t, 0.3 if name == '7' else 0.8)
    elif name == '5':                                 # walks in from the hall door in stages, firing at Wes
        stages = [(0.0, 1.5, (-1.2, 5.9), (-1.2, 5.3)), (3.5, 4.6, (-1.2, 5.3), (-1.25, 5.0)),
                  (6.8, 8.2, (-1.25, 5.0), (-1.3, 4.75))]
        st = next((x for x in stages if u <= x[1]), stages[-1])
        p = R.pose(**R.walk(u, st[2], st[3], st[0], st[1], stride=0.4))
        p['yaw'] = bearing(p['pos'], WES12)           # it keeps its cannon on him as it comes
        aim_cannon(p, '5', u)
        p['sweep'] = R.eye_sweep(t, 0.5)
        andy_holes('5', sp)
        if u >= BLOWN5:                               # blown apart: the legs and hips left, toppling back
            sp['dead'] = True
            sp['headless'] = True
            sp['lost'] = {'armR', 'armL', 'chest', 'ridge', 'cowl', 'shoulder', 'flare', 'rib'}
            k = ease((u - BLOWN5 - 0.1) / 0.5)
            p['fall'] = (85 * k, 0.0)
        return p, sp
    elif name == '6':                                 # under the wide opening, on the right (Sam): fires, riddled
        if u < 4.6:
            return None, sp
        p = R.pose(**R.walk(min(u, 5.7), (1.4, 1.5), (0.15, 1.5), 4.6, 5.7, stride=0.45))
        if u > 5.7:
            p['yaw'] = 270.0
        aim_cannon(p, '6', u)
        p['sweep'] = R.eye_sweep(t, 0.9)
    else:
        return None, sp
    if name in DIES and u >= DIES[name]:
        sp['dead'] = True
        k = ease((u - DIES[name]) / 0.6)
        p['fall'] = (88 * k, {'4': 0.0}.get(name, (p['yaw'] + 180) % 360))
        p['head_pitch'] = -15 * k
    return p, sp


ROBOTS_IN = {'s8': ['A'], 's9': ['A', 'B'], 's10': ['C', 'D'], 's11': ['5'],
             's12': ['A', 'B', 'C', 'D', '1', '2', '3', '4', '5', '6', '7', '8']}


def aim_at(keys, u):
    return keyed(u, keys)


def wes12(t):
    """Wes, pale and manic (fear 6), braced with the minigun at his hip, never stops firing; his eyes on his target."""
    u = U12(t)
    sp = dict(C.WES, bandana=True)
    sp['skin'] = tuple(int(c + (g - c) * 0.3) for c, g in zip(sp['skin'], (236, 232, 222)))
    sp['brows'] = 'outrage'
    sp['mouth'] = 'shout'
    sp['lid'] = -3
    sp['blink'] = False
    fac = aim_at(WES_AIM, u) % 360
    f = int(t * FPS)
    rec = {}
    j = C.minigun_hip(sp, (0.0, 4.0), spin=t * 6.0, flash=1.0 if f % 2 == 0 else 0.6, rec=rec, seed=f)
    return sp, j, fac, rec


def kneel(j, sp, k):
    """Down on his right knee, the left foot planted forward (k 0 standing .. 1 kneeling)."""
    drop = 215.0 * k
    j['bob'] = j.get('bob', 0.0) + drop
    floor = V.ANKLE_Y - drop
    j['footR'] = (60.0, floor + 40 * k, 6.0 - 190 * k)
    j['footL'] = (-70.0, floor, 6.0 + 200 * k)
    j['knee_poleR'] = (0.1, 0.4, 1.0)
    j['knee_poleL'] = (-0.1, -0.3, 1.0)
    return j


def andy12(t):
    u = U12(t)
    sp = C.fear(C.ANDY, 6)
    sp['mouth'] = 'shout' if any(abs(u - d0) < 0.5 for d0, _, _ in DODGES) or KNEEL[0] <= u <= KNEEL[1] + 0.3 else 'set'
    sp['blink'] = False
    fac = aim_at(ANDY_AIM, u) % 360
    flash = any(0 <= u - s_ < 1 / FPS for s_, _ in ANDY_SHOTS)
    d0_, d1_, u0_, u1_ = KNEEL
    kk = ease((u - d0_) / (d1_ - d0_)) if u < u0_ else 1 - ease((u - u0_) / (u1_ - u0_))
    up = -48 * ease((u - d1_) / 0.3) if d1_ <= u <= u0_ else 0.0   # on his knees, aiming up at robot 1's head
    rec = {}
    j = C.glock_aim(sp, (0.0, 2.0 + up), flash=1.0 if flash else 0.0, rec=rec)
    if kk > 0:
        kneel(j, sp, kk)
    x, z = ANDY12
    for d0, d1, side in DODGES:                       # a jink sideways and a duck out of the plasma's way
        if d0 <= u <= d1 + 0.3:
            k = math.sin(math.pi * min(1.0, (u - d0) / (d1 - d0 + 0.3)))
            a = math.radians(fac + 90 * side)
            x += 0.35 * k * math.sin(a)
            z += 0.35 * k * math.cos(a)
            j['bob'] = j.get('bob', 0.0) + 60 * k
            j['lean'] = 12 * k
    return sp, j, fac, rec, (x, z)


# ------------------------------------------------------------------------------------------------ rays and hits
SOLID_BOXES = []
for name in ('island', 'north units', 'sink run', 'tall units'):
    th = PL.THINGS[name]
    (cx, cz), (sx, sz, sy) = th['at'], th['size']
    SOLID_BOXES.append((name, (cx - sx / 2, 0.0, cz - sz / 2), (cx + sx / 2, sy, cz + sz / 2)))
SOLID_BOXES.append(('wall cupboards', (-5.6, 1.58, 5.05), (-1.8, 2.53, 5.4)))


# The walls a round can strike: (axis, value, normal (0: either side), extent along it, the openings in it)
WALLS = [(0, -5.6, 1, (0.0, 5.4), ['kitchen window']), (0, 0.0, 0, (0.0, 5.4), ['wide opening']),
         (0, 6.0, -1, (0.0, 5.4), ['living window']), (2, 0.0, 1, (-5.6, 6.0), []),
         (2, 5.4, -1, (-5.6, 6.0), ['kitchen door', 'living door'])]


def opening_at(ax, v, along, y, pad=0.0):
    """Is this point of a wall (axis, value) in one of its openings? (Shot 12: the kitchen window's glass and frames
    are gone, the doors open.)"""
    key = ('x' if ax == 0 else 'z', v)
    for o in PL.OPENINGS.values():
        if o['wall'] == key and o['span'][0] - pad <= along <= o['span'][1] + pad and o['sill'] - pad <= y <= o['head'] + pad:
            return True
    return False


def ray_hit(o, d, robots=()):
    """Where a shot from o along d lands: the nearest robot (a sphere round its chest), unit or wall. Returns (point,
    normal, what)."""
    o, d = np.asarray(o, float), np.asarray(d, float) / np.linalg.norm(d)
    best = (1e9, None, None, None)
    for name, c, r in robots:
        oc = o - np.asarray(c)
        b = np.dot(oc, d)
        cc = np.dot(oc, oc) - r * r
        disc = b * b - cc
        if disc > 0:
            tt = -b - math.sqrt(disc)
            if 0.05 < tt < best[0]:
                hp = o + d * tt
                best = (tt, hp, (hp - np.asarray(c)) / r, 'robot ' + name)
    for name, lo, hi in SOLID_BOXES:
        tmin, tmax, nrm = -1e9, 1e9, None
        for ax in range(3):
            if abs(d[ax]) < 1e-9:
                if not lo[ax] <= o[ax] <= hi[ax]:
                    tmin = 1e9
                continue
            t1, t2 = (lo[ax] - o[ax]) / d[ax], (hi[ax] - o[ax]) / d[ax]
            n1 = np.zeros(3)
            n1[ax] = -1 if t1 < t2 else 1
            if t1 > t2:
                t1, t2 = t2, t1
            if t1 > tmin:
                tmin, nrm = t1, n1
            tmax = min(tmax, t2)
        if tmin < tmax and 0.05 < tmin < best[0]:
            best = (tmin, o + d * tmin, nrm, name)
    # the walls with their openings (Sam's note 18, 24 Oct: holes hung in the empty window): a round through the
    # shot-out kitchen window, the wide opening or a doorway flies on, and marks only a real surface beyond (or none)
    for ax, v, n, (a0, a1), holes in WALLS:
        if abs(d[ax]) < 1e-9:
            continue
        tt = (v - o[ax]) / d[ax]
        if not 0.05 < tt < best[0]:
            continue
        hp = o + d * tt
        along = hp[2] if ax == 0 else hp[0]
        if not (a0 <= along <= a1 and 0.0 <= hp[1] <= S.CEIL) or opening_at(ax, v, along, hp[1]):
            continue
        nrm = np.zeros(3)
        nrm[ax] = n if n else -math.copysign(1.0, d[ax])
        best = (tt, hp, nrm, 'wall')
    for y, n in ((0.0, 1), (S.CEIL, -1)):             # the floor and ceiling, inside the house only
        if abs(d[1]) < 1e-9:
            continue
        tt = (y - o[1]) / d[1]
        hp = o + d * tt
        if 0.05 < tt < best[0] and -5.6 <= hp[0] <= 6.0 and 0.0 <= hp[2] <= 5.4:
            best = (tt, hp, np.array([0.0, float(n), 0.0]), 'floor' if n > 0 else 'ceiling')
    return best[1], best[2], best[3]


SURFACE = {'island': ((84, 98, 104), 'wood'), 'north units': ((226, 228, 224), 'wood'), 'sink run': ((226, 228, 224), 'wood'),
           'tall units': ((226, 228, 224), 'wood'), 'wall cupboards': ((226, 228, 224), 'wood'),
           'wall': ((238, 238, 234), 'plaster'), 'floor': ((150, 150, 146), 'tile'), 'ceiling': ((246, 244, 238), 'plaster')}




def robot_targets(t):
    out = []
    for name in ROBOTS_IN.get(shot_of(t), []):
        p, sp = robot_pose(name, t)
        if p is None or sp.get('dead') or sp.get('headless'):
            continue
        J, _ = R.skeleton(p)
        out.append((name, tuple(J['chest']), 0.32))
    return out


def wes_shots():
    """Every round Wes fires in shot 12 that lands (12 a second sampled; each leaves a mark, every second one on wood
    a spray of splinters). The barrels ride up to chest height as he leans in."""
    out = []
    for i in range(int((T['end'] - T['s12']) * 12)):
        t = T['s12'] + i / 12
        u = U12(t)
        fac = math.radians(aim_at(WES_AIM, u) + 4 * math.sin(i * 2.3))
        o = (WES12[0] + 0.7 * math.sin(fac), 0.98, WES12[1] + 0.7 * math.cos(fac))
        rise = 0.1                                     # the barrels ride up to the chest of the robot he swings at
        tg = robot_targets(t)                          # (Sam's note 17: robot 4 had taken none of his rounds)
        near = [(abs((math.degrees(math.atan2(c[0] - o[0], c[2] - o[2])) - math.degrees(fac) + 180) % 360 - 180), c)
                for _, c, _ in tg]
        near = [(a, c) for a, c in near if a < 12]
        if near:
            c = min(near)[1]
            rise = (c[1] - o[1]) / max(0.5, math.hypot(c[0] - o[0], c[2] - o[2]))
        d = (math.sin(fac), rise + 0.04 * math.sin(i * 1.7), math.cos(fac))
        hp, n, what = ray_hit(o, d, tg)
        if hp is not None:
            out.append((t, tuple(o), tuple(hp), tuple(n), what, i))
    return out


def plasma_tracks():
    """Each plasma shot: from the robot's palm at the moment it fires towards what it aims at, on until it hits
    something solid (where it scorches and burns); which pendants it passes through on the way."""
    out = []
    for name, u0, what in PLASMA12:
        t0 = T['s12'] + u0
        p, sp = robot_pose(name, t0)
        ps, J = R.parts(p, sp)
        o = np.asarray(next((q.c for q in ps if q.name.startswith('core')), J['handR']), float)
        g = np.asarray(plasma_aim(what, t0), float)
        hp, n, hit = ray_hit(o, g - o)
        if hp is None:                                 # out through an opening into the garden: no mark
            hp, n = o + (g - o) / np.linalg.norm(g - o) * 12.0, np.array([0.0, 1.0, 0.0])
        dist = float(np.linalg.norm(np.asarray(hp) - o))
        tr = dict(name=name, t0=t0, o=tuple(o), hp=tuple(hp), n=tuple(n), what=what, t_hit=t0 + dist / PLASMA_SPEED,
                  pendants={}, lands=hit is not None)
        d = (np.asarray(hp) - o) / dist
        for k in range(3):
            c = np.asarray(pendant_at(k))
            s_ = float(np.dot(c - o, d))
            if 0 < s_ < dist and np.linalg.norm(o + d * s_ - c) < 0.22:
                tr['pendants'][k] = t0 + s_ / PLASMA_SPEED
        out.append(tr)
    return out


WES_HITS = None
PLASMA = None
MARKS = None
DEBRIS12 = None
BURNS = None
BROKEN = None


def _prepare12():
    """Everything shot 12 leaves behind, worked out once: marks, debris, spent cases, burst tins and bottles, the
    broken pendants, robot 5 in pieces."""
    global WES_HITS, PLASMA, MARKS, DEBRIS12, BURNS, BROKEN
    if WES_HITS is not None:
        return
    WES_HITS = wes_shots()
    PLASMA = plasma_tracks()
    MARKS, DEBRIS12, BURNS, BROKEN = [], [], [], {}
    box = (-5.55, 5.95, 0.05, 5.35)
    kbox = (-5.55, -0.05, 0.05, 5.35)
    isl = PL.THINGS['island']
    tops = TOPS + [(isl['at'][0] - 1.2, isl['at'][0] + 1.2, isl['at'][1] - 0.5, isl['at'][1] + 0.5, 0.92)]
    for (t, o, hp, n, what, i) in WES_HITS:
        if what.startswith('robot'):
            continue
        col, kind = SURFACE.get(what, ((220, 220, 214), 'chip'))
        MARKS.append(dict(t=t, at=hp, n=n, kind='hole', size=0.05 + 0.015 * (i % 3), seed=i, room='kitchen', chip=col))
        if kind == 'wood' and i % 2 == 0:              # cupboards splintering (Sam, 24 Oct)
            DEBRIS12.extend(X.burst(t, hp, 6, 2.2, 100 + i, kind='splinter', col=col if i % 4 else (206, 174, 124),
                                    size=0.045, up=1.0, dirn=n, box=box, tops=tops))
        elif i % 3 == 0:
            DEBRIS12.extend(X.burst(t, hp, 5, 2.0, 100 + i, kind='chip', col=col, size=0.03, up=1.0, dirn=n, box=box, tops=tops))
    for i in range(0, len(WES_HITS) + 40, 2):         # spent cases flying off the minigun, landing and staying
        t = T['s12'] + i / 12
        if t >= T['end']:
            break
        fac = math.radians(aim_at(WES_AIM, U12(t)) % 360)
        fwd, rt = np.array([math.sin(fac), 0, math.cos(fac)]), np.array([math.cos(fac), 0, -math.sin(fac)])
        at = np.array([WES12[0], 0.95, WES12[1]]) + fwd * 0.3 + rt * 0.18
        rng = np.random.default_rng(500 + i)
        v = rt * rng.uniform(1.4, 2.2) + fwd * rng.uniform(-0.4, 0.4) + np.array([0, rng.uniform(1.2, 2.0), 0])
        pc = X.Piece(tuple(at), tuple(v), t, r=0.008, e=0.4, spin=rng.uniform(-20, 20), box=box, tops=tops)
        pc.kind, pc.col, pc.size, pc.seed = 'case', X.BRASS, 0.022, 500 + i
        DEBRIS12.append(pc)
    for tr in PLASMA:                                  # the plasma burns where it lands
        if tr['lands']:
            MARKS.append(dict(t=tr['t_hit'], at=tr['hp'], n=tr['n'], kind='scorch', size=0.16, seed=int(tr['t0'] * 10),
                              room='kitchen'))
            BURNS.append((tr['t_hit'], tr['hp'], tr['n'], int(tr['t0'] * 10)))
        for k, tk in tr['pendants'].items():           # a pendant in its way shatters
            if k not in BROKEN:
                BROKEN[k] = tk
                c = pendant_at(k)
                DEBRIS12.extend(X.burst(tk, c, 12, 2.4, 300 + k, kind='glass', size=0.04, up=0.5, box=box, tops=tops))
                DEBRIS12.extend(X.burst(tk, c, 6, 2.2, 310 + k, kind='chip', col=(204, 160, 72), size=0.04, up=0.5,
                                        box=box, tops=tops))
        if tr['what'] in ('tins', 'bottles'):          # the tins and bottles blow up across the worktop
            spots = TIN_SPOTS if tr['what'] == 'tins' else BOTTLE_SPOTS
            for k, (x, z) in enumerate(spots):
                tb = tr['t_hit'] + 0.03 * k
                at = (x, 1.0, z)
                if tr['what'] == 'tins':
                    goo = X.burst(tb, at, 9, 1.7, 400 + k, kind='goop', size=0.05, up=1.3, box=box, tops=tops)
                    ix, iz = isl['at']
                    for pc in goo:                     # a splat at the island's edge runs off it (Sam's note 14)
                        (gx, gy, gz), _ = pc.track[-1]
                        if abs(gy - 0.92 - pc.r) < 0.02:
                            ex, ez = gx - ix, gz - iz
                            if 1.2 - abs(ex) < 0.1:
                                pc.drip = ((ix + math.copysign(1.2, ex), 0.92, gz), (math.copysign(1.0, ex), 0.0))
                            elif 0.5 - abs(ez) < 0.1:
                                pc.drip = ((gx, 0.92, iz + math.copysign(0.5, ez)), (0.0, math.copysign(1.0, ez)))
                    DEBRIS12.extend(goo)
                    DEBRIS12.extend(X.burst(tb, at, 8, 2.0, 405 + k, kind='bean', size=0.016, up=1.6, box=box, tops=tops))
                    DEBRIS12.extend(X.burst(tb, at, 5, 2.2, 410 + k, kind='chip', col=(48, 170, 170), size=0.035, up=1.8,
                                            box=box, tops=tops))
                else:
                    DEBRIS12.extend(X.burst(tb, (x, 1.08, z), 24, 2.0, 420 + k, kind='drop', size=0.03, up=1.4, box=box,
                                            tops=tops))
                    DEBRIS12.extend(X.burst(tb, (x, 1.08, z), 4, 1.8, 430 + k, kind='chip', col=(230, 240, 248), size=0.04,
                                            up=1.4, box=box, tops=tops))
                    DEBRIS12.extend(X.burst(tb, (x, 1.2, z), 1, 1.2, 440 + k, kind='chip', col=(40, 110, 200), size=0.03,
                                            up=2.0, box=box, tops=tops))
    for k, (name, ub) in enumerate(sorted(BLOWN.items())):   # robots 4 and 5 blown to pieces: chunks of plate
        p5, sp5 = robot_pose(name, T['s12'] + ub - 0.01)       # everywhere, staying where they land
        J5, _ = R.skeleton(p5)
        c5 = tuple(J5['chest'])
        dn = (0.5, 0.1, 0.0) if name == '4' else None          # robot 4's thrown into the kitchen, off the sink run
        DEBRIS12.extend(X.burst(T['s12'] + ub, c5, 30, 3.2, 600 + 10 * k, kind='chip', col=R.CHROME[0], size=0.09, up=1.6,
                                box=kbox, tops=tops, spread=1.4, dirn=dn))
        DEBRIS12.extend(X.burst(T['s12'] + ub, c5, 14, 3.0, 601 + 10 * k, kind='chip', col=R.CHROME_D[1], size=0.07,
                                up=1.4, box=kbox, tops=tops, spread=1.4, dirn=dn))
        DEBRIS12.extend(X.burst(T['s12'] + ub, c5, 8, 2.6, 602 + 10 * k, kind='splinter', col=(70, 74, 82), size=0.08,
                                up=1.2, box=kbox, tops=tops, spread=1.4, dirn=dn))
    cr = X.CROCK_AT                                    # the dish rack smashed by robot 4's blast: plate and mug shards
    for k, col in enumerate((X.PLATE, X.PLATE, X.PLATE_RIM)):
        DEBRIS12.extend(X.burst(T['s12'] + BLOWN['4'] + 0.04, (cr[0], cr[1] + 0.15, cr[2]), 9 if k < 2 else 4, 2.2,
                                650 + k, kind='chip', col=col, size=0.045, up=1.2, box=kbox, tops=tops, dirn=(0.5, 0.1, -0.3)))


def item_gone(kind, t):
    """When a tin or bottle on the island has been blown up (shot 12)."""
    if shot_of(t) != 's12':
        return False
    _prepare12()
    return any(tr['what'] == kind + 's' and t >= tr['t_hit'] for tr in PLASMA)


def wes_holes(name):
    _prepare12()
    parts = ['chest', 'shoulderR', 'shoulderL', 'pelvis', 'chest', 'thighL', 'thighR']
    return [dict(part=parts[k % len(parts)], i=17 * k + 5, t=ts + 0.02, r=0.026)
            for k, (ts, o, hp, n, what, i) in enumerate(h for h in WES_HITS if h[4] == 'robot ' + name)]


# ------------------------------------------------------------------------------------------------ the picture
def masked(im, cam, fx, xz, draw):
    """Draw a person on a layer of their own, lay it on, and keep their silhouette (and depth) for Behind."""
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
    r = draw(lay)
    im.alpha_composite(lay)
    fx.setdefault('masks', []).append((cam.depth((xz[0], 1.2, xz[1])), lay.getchannel('A').point(lambda a: 255 if a > 128 else 0)))
    return r


def actors(t, cam, fx):
    """Everyone and everything that moves, as actors for the set's painter (plan point, radius, draw)."""
    s = shot_of(t)
    out = []
    u = t - shot_start(t)
    if s in ('s1', 's2', 's3', 's4', 's7'):
        sp, j = andy_sofa(t, s)
        x, z = PL.PEOPLE['andy sofa (1-4, 7, start of 8)']['at']
        out.append(dict(at=(x, z), r=0.25, draw=lambda im: put(im, cam, sp, x, z, 180, j, t)))
    elif s == 's6':
        sp, j, fac, hf = andy6(t)
        x, z = PL.PEOPLE['andy kitchen (6)']['at']
        out.append(dict(at=(x, z), r=0.25, draw=lambda im: put(im, cam, sp, x, z, fac, j, t, head_facing=hf)))
    elif s == 's12':
        _prepare12()
        sp, j, fac, rec = wes12(t)
        out.append(dict(at=WES12, r=0.3, draw=lambda im: fx.__setitem__('wes', (masked(im, cam, fx, WES12, lambda l: put(
            l, cam, sp, WES12[0], WES12[1], fac, j, t)), rec))))
        sp2, j2, fac2, rec2, (ax_, az_) = andy12(t)
        out.append(dict(at=(ax_, az_), r=0.3, draw=lambda im: fx.__setitem__('andy', (masked(im, cam, fx, (ax_, az_), lambda l: put(
            l, cam, sp2, ax_, az_, fac2, j2, t)), rec2))))
        # the Alexa's remains, up on rod legs, scuttling at Wes with a kitchen knife
        (bx, by, bz), _ = ALEXA_BALL.at(T['s12'] - 0.01)
        k = ease((u - 1.5) / 8.5)
        ax2, az2 = bx + (WES12[0] - 0.35 - bx) * k, bz + (WES12[1] + 0.25 - bz) * k
        face = math.degrees(math.atan2(WES12[0] - ax2, WES12[1] - az2))
        if u < 1.2:
            out.append(dict(at=(bx, bz), r=0.06, draw=lambda im: X.alexa_walker(im, cam, (bx, 0.0, bz), t, face, knife=u > 0.8)))
        else:
            out.append(dict(at=(ax2, az2), r=0.06, draw=lambda im: X.alexa_walker(im, cam, (ax2, 0.0, az2), t, face)))
    for name in ROBOTS_IN.get(s, []):
        p, sp_r = robot_pose(name, t)
        if p is None:
            continue
        if s == 's12':
            sp_r['holes'] = sp_r['holes'] + wes_holes(name)
        J, _ = R.skeleton(p)
        foot = (float(J['hipC'][0]), float(J['hipC'][2]))
        if p.get('fall') and p['fall'][0] > 30:
            foot = (float(J['chest'][0]), float(J['chest'][2]))
        out.append(dict(at=foot, r=0.3, draw=lambda im, p=p, sp_r=sp_r, name=name: fx.setdefault('robots', {}).__setitem__(
            name, R.draw(im, cam, p, sp_r, t))))
    if s == 's12':                                    # the heads shot off (robot 1) and blown off (robot 5), landing
        for name, piece in HEADS.items():
            if t >= piece.t0:
                hp = piece.at(t)
                out.append(dict(at=(hp[0][0], hp[0][2]), r=0.15, draw=lambda im, piece=piece: flying_head(im, cam, t, piece)))
    return out


def _heads():
    out = {}
    for name, u0, v in (('1', HEAD1, (1.4, 2.4, -0.4)), ('5', BLOWN5, (-0.6, 3.2, -1.6)), ('4', BLOWN['4'], (1.9, 3.0, 0.4))):
        p, sp = robot_pose(name, T['s12'] + u0 - 0.01)
        J, _ = R.skeleton(p)
        out[name] = X.Piece(tuple(J['head']), v, T['s12'] + u0, r=0.15, e=0.3, spin=9, box=(-5.55, -0.05, 0.05, 5.35),
                            tops=TOPS)
    return out


HEADS = _heads()


def flying_head(img, cam, t, piece):
    (x, y, z), ang = piece.at(t)
    H = R.rot([1, 0.3, 0.2], ang)
    parts = R.head_parts(np.array([x, y, z]), H, 0.0, {'dead': True})
    pen = B.Pen(img, FLAT)
    L = R.light(cam)
    for q in sorted(parts, key=lambda q: -float(np.dot(q.c - np.asarray(cam.pos), np.asarray(cam.f)))):
        R.draw_part(pen, cam, q, L)


def house_state(t):
    s = shot_of(t)
    st = {'doors': {'living door': 0.0, 'kitchen door': 0.0}, 'marks': [], 'glass': {}}
    if t >= DOOR8 and s not in ('s5', 's6'):
        st['doors']['living door'] = min(100.0, 100 * ease((t - DOOR8) / 0.18)) if t < DOOR8 + 0.3 else 96.0
    if t >= T['s11'] and s not in ('s5', 's6'):
        st['doors']['kitchen door'] = 95.0
    if t >= FIRE10 and s not in ('s5', 's6'):
        for i in range(3):
            for part in ('low', 'top'):
                st['glass'][f'kitchen window {i} {part}'] = {'seed': i * 2 + (part == 'top')}
    if t >= FIRE10 + 0.8 and s not in ('s5', 's6'):   # the minigun shreds the frames too (Sam: robot 4 climbs through)
        st['glass']['_frames_gone'] = ('kitchen window',)
    st['island'] = lambda im, cam: draw_island_items(im, cam, t)
    smashed = s == 's12' and U12(t) >= BLOWN['4']     # robot 4's blast smashes the dish rack beside it (my addition)
    st['on'] = {'sink run': lambda im, cam: X.dish_rack(im, cam, smashed=smashed)}
    if s == 's12':
        _prepare12()
        st['marks'] = [m for m in MARKS if m['t'] <= t]
        st['broken'] = {f'pendant {k}' for k, tk in BROKEN.items() if t >= tk}
    return st


class Behind:
    """Effects drawn at their true depth against the people (Sam, 24 Oct: debris flying behind Andy was drawn over
    him). D(point) gives the picture to draw an effect at that world point on: the frame itself when nothing is nearer,
    or a layer that is cut away wherever a nearer person stands, laid on at finish()."""
    def __init__(self, img, cam, masks):
        self.img, self.cam = img, cam
        self.masks = sorted(masks, key=lambda m: m[0])           # (depth, mask), nearest first
        self.layers = {}

    def __call__(self, at):
        d = self.cam.depth(tuple(float(v) for v in at))
        g = sum(1 for dm, _ in self.masks if dm < d - 0.15)
        if g == 0:
            return self.img
        if g not in self.layers:
            self.layers[g] = Image.new('RGBA', self.img.size, (0, 0, 0, 0))
        return self.layers[g]

    def finish(self):
        from PIL import ImageChops
        for g in sorted(self.layers, reverse=True):              # the farthest first
            lay = self.layers[g]
            cut = self.masks[0][1]
            for _, m in self.masks[1:g]:
                cut = ImageChops.lighter(cut, m)
            lay.putalpha(ImageChops.subtract(lay.getchannel('A'), cut))
            self.img.alpha_composite(lay)


def effects(img, cam, t, fx):
    """The flat effects over the frame, shot by shot."""
    s = shot_of(t)
    p = B.Pen(img, FLAT)
    p = B.Pen(img, FLAT)
    if s == 's6':
        if t < FIRE6 + BOLT6:                         # the Alexa on the worktop, drawn over the units (Sam, 24 Oct:
            X.alexa(img, cam, ALEXA)                  # the painter had it behind them, so it never showed)
        if FIRE6 <= t < FIRE6 + BOLT6:
            b = bolt6_at(t)
            d = np.subtract(BOLT6_TO, BOLT6_FROM)
            X.bolt(img, cam, b, d)
            if t < FIRE6 + 0.1:
                X.flash(img, cam, BOLT6_FROM, 0.12, seed=1)
        if t >= FIRE6 + BOLT6:
            for pc in ALEXA_BITS:
                X.draw_piece(img, cam, pc, t)
            (bx, by, bz), ang = ALEXA_BALL.at(t)
            X.alexa(img, cam, (bx, by - 0.045 * X.ALEXA_K, bz), light=False)
            X.sparks(img, cam, t, FIRE6 + BOLT6, BOLT6_TO, 6, n=18, col='yellow', speed=2.4)
            X.sparks(img, cam, t, FIRE6 + BOLT6 + 0.15, BOLT6_TO, 7, n=10, col='blue', speed=1.6)
            if t < FIRE6 + BOLT6 + 1 / FPS:          # one frame only, small (Sam's note 19: the big two-frame star
                X.flash(img, cam, BOLT6_TO, 0.07, seed=2)   # read as a yellow slab on the worktop)
            X.smoke(img, cam, t, FIRE6 + BOLT6 + 0.1, BOLT6_TO, 8, n=4, life=1.2, size=0.06)
            X.bolt(img, cam, *BOLT6_STUCK)               # through the Alexa and stuck in the splashback
    if s == 's12':
        u = U12(t)
        f = int(t * FPS)
        X.room_flash(img, 1.0 if f % 2 == 0 else 0.45)
        D = Behind(img, cam, fx.get('masks', []))      # effects behind Andy or Wes are hidden by them (Sam, 24 Oct)
        we = fx.get('wes')
        if we and we[1].get('muzzle'):
            mx, my = we[1]['muzzle']
            for (ts, o, hp, n, what, i) in WES_HITS:
                if 0 <= t - ts < 1 / FPS:
                    (hx, hy), k = cam.project(hp)
                    if cam.depth(hp) > 0.2:
                        frac = 0.35 + 0.5 * ((i * 37) % 10) / 10
                        p.line([(mx + (hx - mx) * (frac - 0.25), my + (hy - my) * (frac - 0.25)),
                                (mx + (hx - mx) * frac, my + (hy - my) * frac)], (255, 236, 150), 2.6)
        for (ts, o, hp, n, what, i) in WES_HITS:                 # what he hits: sparks off robots, flashes off walls
            if 0 <= t - ts < 0.45:
                if what.startswith('robot'):
                    X.sparks(D(hp), cam, t, ts, hp, i, n=8, col='yellow' if i % 2 else 'blue', speed=2.2, dirn=n)
                    if t - ts < 1 / FPS:
                        X.flash(D(hp), cam, hp, 0.08, seed=i)
                elif t - ts < 1 / FPS and i % 2 == 0:
                    X.flash(D(hp), cam, hp, 0.06, seed=i)
        for pc in DEBRIS12:
            X.draw_piece(D(pc.at(t)[0]), cam, pc, t)
        an = fx.get('andy')
        for s_, who in ANDY_SHOTS:                                # Andy's rounds: a tracer, sparks where they strike
            if not 0 <= u - s_ < 0.4:
                continue
            o, g = andy_round(s_, who)
            if u - s_ < 1 / FPS and an and an[1].get('muzzle') and cam.depth(g) > 0.2:
                (hx, hy), _ = cam.project(g)
                mx, my = an[1]['muzzle']
                p.line([(mx + (hx - mx) * 0.3, my + (hy - my) * 0.3), (mx + (hx - mx) * 0.8, my + (hy - my) * 0.8)],
                       (255, 236, 150), 2.2)
            X.sparks(D(g), cam, t, T['s12'] + s_, g, int(s_ * 100), n=10, col='yellow', speed=2.5)
        wind, cut, thru = SWIPE                                   # robot 1's blade: the sweep over Andy's head
        if cut <= u < thru + 0.15:
            J1, _ = R.skeleton(robot_pose('1', t)[0])
            tips = [blade_tip('1', T['s12'] + cut + (min(u, thru) - cut) * k / 7) for k in range(8)]
            X.blade_arc(D(J1['chest']), cam, [q for q in tips if q is not None][-6:])
        if HEAD1 <= u < HEAD1 + 1.0:                              # robot 1's head comes off: blue sparks from the neck
            p1, sp1 = robot_pose('1', t)
            J, _ = R.skeleton(p1)
            X.sparks(D(J['neck']), cam, t, T['s12'] + HEAD1, tuple(J['neck']), 33, n=16, col='blue', speed=2.0)
            X.smoke(D(J['neck']), cam, t, T['s12'] + HEAD1 + 0.1, tuple(J['neck']), 34, n=3, life=1.2, size=0.08)
        for name, ub in BLOWN.items():                            # robots 4 and 5 blown apart: flash, sparks, smoke
            if not ub <= u < ub + 2.5:
                continue
            c5, sd = HEADS[name].track[0][0], 55 + 10 * int(name)
            if u < ub + 0.17:
                X.flash(D(c5), cam, c5, 0.5, seed=sd)
            X.sparks(D(c5), cam, t, T['s12'] + ub, c5, sd, n=30, col='yellow', speed=3.4, life=0.5)
            X.sparks(D(c5), cam, t, T['s12'] + ub + 0.05, c5, sd + 1, n=18, col='blue', speed=2.6, life=0.5)
            X.smoke(D(c5), cam, t, T['s12'] + ub + 0.1, c5, sd + 2, n=6, life=2.2, size=0.18)
        for tr in PLASMA:                                         # the plasma bolts, and the flash where they land
            if tr['t0'] <= t < tr['t_hit'] + 0.12:
                L_ = (tr['t_hit'] - tr['t0'])
                k = (t - tr['t0']) / max(1e-6, L_)
                if k <= 1.0:
                    a = lerp3(tr['o'], tr['hp'], max(0.0, k - 0.6 / (L_ * PLASMA_SPEED)))
                    b = lerp3(tr['o'], tr['hp'], min(1.0, k))
                    X.plasma(D(b), cam, a, b)
                elif tr['lands']:
                    X.flash(D(tr['hp']), cam, tr['hp'], 0.22, seed=int(tr['t0'] * 10), col='blue')
            if tr['lands'] and tr['t_hit'] <= t < tr['t_hit'] + 1.5:
                X.smoke(D(tr['hp']), cam, t, tr['t_hit'], tr['hp'], int(tr['t0'] * 10), n=3, life=1.3, size=0.1)
        for tb, at, n, seed in BURNS:                             # and burns there for a few seconds
            X.flames(D(at), cam, t, tb, at, n, seed)
        X.bolt(D(BOLT6_STUCK[0]), cam, *BOLT6_STUCK)  # shot 6's bolt, still in the splashback
        D.finish()


def andy_round(s_, who):
    """One of Andy's rounds in shot 12: from his pistol to the point it strikes (robot `who`'s chest, or its head)."""
    t = T['s12'] + s_
    sp, j, fac, rec, (x, z) = andy12(t)
    kneeling = KNEEL[0] <= s_ <= KNEEL[3]
    a = math.radians(fac)
    o = (x + 0.6 * math.sin(a), 0.95 if kneeling else 1.35, z + 0.6 * math.cos(a))
    p, spr = robot_pose(who[0], t)
    J, _ = R.skeleton(p)
    return o, tuple(J['head'] if who.endswith('h') else J['chest'])


def blade_tip(name, t):
    p, sp = robot_pose(name, t)
    ps, J = R.parts(p, sp)
    tips = [q.pts[4] for q in ps if q.name.startswith('blade') and not q.name.startswith('bladecore')]
    return tuple(tips[0]) if tips else None


def picture(t):
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    cam = cam_for(t)
    img = B.canvas((255, 255, 255))
    fx = {}
    S.house(img, cam, t, actors(t, cam, fx), house_state(t))
    effects(img, cam, t, fx)
    return img


# ------------------------------------------------------------------------------------------------ overlays
CAP_FONT = os.path.join(HERE, 'fonts', 'TikTokSans-Bold.woff')
UI_FONT = os.path.join(HERE, 'fonts', 'TikTokSans-Medium.woff')


def his_caption(img, s, y=1180):
    """Andy's own caption look (Cry Minister): TikTok Sans Bold, white, a soft dark shadow, centred."""
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


def tiktok_ui(img, t):
    """The TikTokPM frame from Cry Minister: his name and description only (the real app draws the rest)."""
    SS = img.width // 1080
    F_ = lambda size, bold=True: ImageFont.truetype(CAP_FONT if bold else UI_FONT, int(size * SS))
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    size = 34
    for layer, col, off in ((sh, (0, 0, 0, 110), 2), (lay, (255, 255, 255, 255), 0)):
        d = ImageDraw.Draw(layer)
        o = off * SS
        name = HANDLE.lstrip('@')
        d.text((60 * SS + o, 1398 * SS + o), name, font=F_(42), fill=col, anchor='ls')
        nx = 60 * SS + d.textlength(name, font=F_(42)) + 14 * SS
        if layer is lay:
            d.ellipse([nx, 1366 * SS, nx + 30 * SS, 1396 * SS], fill=(32, 213, 236, 255))
            d.line([(nx + 8 * SS, 1381 * SS), (nx + 13 * SS, 1387 * SS), (nx + 23 * SS, 1374 * SS)], fill=(255, 255, 255),
                   width=4 * SS)
        d.text((nx + 42 * SS + o, 1398 * SS + o), '· 1d ago', font=F_(36, False),
               fill=col if layer is sh else (210, 210, 210, 255), anchor='ls')
        if DESCRIPTION:
            d.text((60 * SS + o, 1452 * SS + o), DESCRIPTION, font=F_(size, False), fill=col, anchor='ls')
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4 * SS)))
    img.alpha_composite(lay)


def overlay(img, t):
    if t < BLACK_AT:
        tiktok_ui(img, t)
        c = caption_at(t)
        if c:
            his_caption(img, c)
    return img


def frame_image(t):
    return overlay(picture(t), t)


# ------------------------------------------------------------------------------------------------ sound
SFX = {}


# Short slices of Sam's longer files (Sam, 24 Oct: one moment of crockery sound per impact): (file, from, to) seconds
SLICES = {'crockery': ('crockery', 0.08, 0.55), 'robot-step': ('robot-walk', 1.0, 1.45)}


def sfx(name):
    if name not in SFX:
        f, a, b = SLICES.get(name, (name, None, None))
        clip = np.asarray(MA.load(os.path.join(HERE, 'audio', 'prepper', f'sfx-{f}.mp3')), float)
        if a is not None:
            clip = clip[int(a * SR):int(b * SR)].copy()
            fo = int(0.08 * SR)                        # a quick fade out, so the slice never clicks
            clip[-fo:] *= np.linspace(1, 0, fo)
            clip[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
        SFX[name] = clip
    return SFX[name]


def steps(t0, t1, start, end, stride):
    """When a robot's feet come down on a walk (R.walk plants one every stride)."""
    L = math.dist(start, end)
    return [t0 + (t1 - t0) * k * stride / L for k in range(1, int(L / stride) + 1)]


def sound_events():
    """The sound effects Sam sent, placed where they really start (filmkit.place). Shots 5 has none (brief)."""
    ev = [('crossbow', FIRE6, 0.9), ('arrow-woosh', FIRE6 + 0.05, 0.7), ('alexa-hit', FIRE6 + BOLT6, 0.9),
          ('sparks', FIRE6 + BOLT6 + 0.05, 0.5),
          ('door-kicked-open', DOOR8, 0.9), ('robot-scan', ROBOT8, 0.5), ('crossbow', BOLT8 - 0.05, 0.9),
          ('arrow-woosh', BOLT8 - 0.02, 0.8), ('sparks', BOLT8 + 0.1, 0.6), ('robot-wounded', BOLT8 + 0.15, 0.7),
          ('laser-sword', LUNGE9 + 0.1, 0.6)] + [('pistol', s_, 0.8) for s_ in SHOTS9] + \
         [('robot-wounded', SHOTS9[-1] + 0.1, 0.6), ('glass-shattered', FIRE10, 0.9), ('plasma-gun', PLASMA10, 0.7),
          ('minigun', FIRE10, 0.9), ('minigun', T['s12'], 0.9), ('minigun', T['s12'] + 2.4, 0.9), ('minigun', T['s12'] + 4.8, 0.9)]
    ev += [('minigun', T['s12'] + 7.2, 0.9), ('minigun', T['s12'] + 9.6, 0.9)]
    ev += [('pistol', T['s12'] + s_, 0.7) for s_, _ in ANDY_SHOTS]
    ev += [('plasma-gun', T['s12'] + t0, 0.55) for _, t0, _ in PLASMA12]
    ev += [('laser-sword', T['s12'] + SWIPE[1], 0.7)]
    ev += [('robot-wounded', T['s12'] + HEAD1, 0.7), ('sparks', T['s12'] + HEAD1, 0.6)]
    ev += [x for ub in BLOWN.values() for x in (('robot-explosion', T['s12'] + ub, 0.9), ('sparks', T['s12'] + ub + 0.05, 0.6))]
    ev += [('robot-wounded', T['s12'] + u_ + 0.05, 0.5) for u_ in DIES.values()]
    _prepare12()
    ev += [('glass-shattered', tk, 0.5) for tk in BROKEN.values()]
    ev += [('crockery', T['s12'] + BLOWN['4'] + 0.05, 0.6)]   # the dish rack: one smash, in shot (crockery_check)
    s12 = T['s12']                                     # robot footsteps: robot 1 coming at Andy, robot 5's stages
    walks = [(1.6, 6.0, (2.0, 1.7), (-2.05, 1.75), 0.5, 0.45), (0.0, 1.5, (-1.2, 5.9), (-1.2, 5.3), 0.4, 0.4),
             (3.5, 4.6, (-1.2, 5.3), (-1.25, 5.0), 0.4, 0.4), (6.8, 8.2, (-1.25, 5.0), (-1.3, 4.75), 0.4, 0.4)]
    for t0, t1, a, b, stride, g in walks:
        ev += [('robot-step', s12 + ts, g) for ts in steps(t0, t1, a, b, stride)]
    ev += [('robot-step', ROBOT8 + 0.25 * k, 0.45) for k in (0, 1)]
    return ev


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)
    for ln in LINES:
        s_ = int(ln['start'] * SR)
        seg = ln['_voice'][:max(0, n - s_)]
        voice[s_:s_ + len(seg)] += seg
    for name, at, g in sound_events():
        try:
            clip = sfx(name)
        except Exception:
            continue
        filmkit.place(rest, clip * 0.35, at=at, sr=SR, gain=g)
    mix = voice + rest
    end = int(BLACK_AT * SR)
    mix, g = MA.master(mix, end)
    voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


# ------------------------------------------------------------------------------------------------ checks
def _robot_solids(name, p, sp):
    """A robot's solids from its skeleton (2.1 m tall): body, head (unless it is gone), arms and legs as capsules."""
    J, _ = R.skeleton(p)
    lost = sp.get('lost', set())
    out = []
    if 'chest' not in lost:
        out.append(CC.capsule(name, 'body', J['hipC'], J['chest'], 0.2))
    else:
        out.append(CC.sphere(name, 'hips', J['hipC'], 0.17))
    if not sp.get('headless'):
        out.append(CC.sphere(name, 'head', J['head'], 0.14))
    for sd in 'RL':
        if 'arm' + sd not in lost:
            out.append(CC.capsule(name, 'arm' + sd, J['sh' + sd], J['el' + sd], 0.07))
            out.append(CC.capsule(name, 'hand' + sd, J['el' + sd], J['hand' + sd], 0.07))
        out.append(CC.capsule(name, 'leg' + sd, J['hip' + sd], J['knee' + sd], 0.08))
        out.append(CC.capsule(name, 'shin' + sd, J['knee' + sd], J['ankle' + sd], 0.07))
    return out


def scene(t, faces=None):
    """Everyone and everything solid at time t, as picture(t) puts them (audit.py, rule 5); `faces` also collects
    each face drawn (name, mouth, view, head height px) for voices.py (rule 7)."""
    me = sys.modules[__name__]
    with A.Recorder() as rec:
        def put_(img, cam, sp, x, z, facing, j, t_, head_facing=None, lift=0.0, shadow=True):
            name = sp.get('name', 'someone')
            h = HEIGHTS.get(name, 1.75)
            fd = (math.sin(math.radians(facing)), math.cos(math.radians(facing)))
            if cam.depth((x, 1.5, z)) < 0.3:
                return None
            rec.add(name, A.placed(name, j, x, z, fd, h, lift, 0.0, sp))
            if faces is not None:
                yaw = cam.yaw_of((x, 0, z), fd if head_facing is None else
                                 (math.sin(math.radians(head_facing)), math.cos(math.radians(head_facing))))
                (_, y0), k = cam.project((x, h - 0.1, z))
                faces.append((name, sp.get('mouth'), yaw, 0.22 * k))
            return None

        def robot_(img, cam, p, sp, t_):
            rec.add(sp.get('name', 'robot'), _robot_solids(sp.get('name', 'robot'), p, sp))
            return {}

        def house_(img, cam, t_, actors=(), state=None):
            for name, lo, hi in SOLID_BOXES:
                rec.add(name.upper(), [CC.box(name.upper(), 'box', lo, hi)])
            for a in actors:
                a['draw'](img)
        rec.patch(me, 'put', put_)
        rec.patch(me, 'masked', lambda im, cam, fx, xz, draw: draw(im))
        rec.patch(me, 'effects', lambda *a, **k: None)
        rec.patch(me, 'flying_head', lambda *a, **k: None)
        rec.patch(R, 'draw', robot_)
        rec.patch(S, 'house', house_)
        rec.patch(X, 'alexa_walker', lambda *a, **k: None)
        picture(t)
    return rec.things


def mouths_seen(t):
    """Every face on screen with its mouth as drawn (voices.py, rule 7): scene(t)'s run."""
    faces = []
    scene(t, faces)
    return faces


def checks():
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES if not ln.get('off') for a, b in ln['_stretches']]
    faults = E.check_mouths(sorted(x for w in TRACK for x in TRACK[w]), windows)
    faults += facing_check()
    faults += marks_check()
    faults += crockery_check()
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


def crockery_check():
    """Sam, 24 Oct: a crockery sound only when crockery is hit, one per impact, and the hit in frame."""
    out = []
    for name, at, _ in sound_events():
        if name == 'crockery':
            cam = cam_for(at)
            (x, y), _ = cam.project(X.CROCK_AT)
            if not (cam.depth(X.CROCK_AT) > 0.3 and 60 < x < 1020 and 60 < y < 1860):
                out.append(f'{at:.2f}s the crockery sound plays with the dish rack out of frame')
    return out


def marks_check():
    """Sam's note 18 (24 Oct): bullet holes hung in the empty window. Every mark shot 12 leaves must sit on a real
    surface: inside the house, on a wall, unit, floor or ceiling, never in an opening."""
    _prepare12()
    faults = []
    for m in MARKS:
        x, y, z = m['at']
        if not (-5.61 <= x <= 6.01 and -0.01 <= y <= S.CEIL + 0.01 and -0.01 <= z <= 5.41):
            faults.append(f"{m['t']:.2f}s a {m['kind']} outside the house at ({x:.2f}, {y:.2f}, {z:.2f})")
        for ax, v, _, _, _ in WALLS:
            pt = (x, y, z)
            if abs(pt[ax] - v) < 0.02 and opening_at(ax, v, z if ax == 0 else x, y, pad=-0.02):
                faults.append(f"{m['t']:.2f}s a {m['kind']} in an opening at ({x:.2f}, {y:.2f}, {z:.2f})")
    return faults


def facing_check():
    """Sam's note 11 (24 Oct): Andy's face looked backwards while his body faced forwards. Every frame of shots 6 and
    12, Andy and Wes are drawn alone through the shot's camera: the head may turn at most 95 degrees from the body, and
    from behind nothing they hold out in front may be drawn over their back."""
    faults = []
    for s0, s1 in ((T['s6'], T['s7']), (T['s12'], T['end'])):
        for f in range(int(s0 * FPS), int(s1 * FPS)):
            t = f / FPS
            cam = cam_for(t)
            if shot_of(t) == 's6':
                sp, j, fac, hf = andy6(t)
                who = [('Andy', sp, j, fac, hf, PL.PEOPLE['andy kitchen (6)']['at'])]
            else:
                sp, j, fac, rec = wes12(t)
                sp2, j2, fac2, rec2, xz = andy12(t)
                who = [('Wes', sp, j, fac, None, WES12), ('Andy', sp2, j2, fac2, None, xz)]
            for name, sp_, j_, fac_, hf_, (x, z) in who:
                img = B.canvas((255, 255, 255))
                r = put(img, cam, sp_, x, z, fac_, j_, t, head_facing=hf_)
                if not r:
                    continue
                d = r['j2']['_drawn']
                turn = abs((d['head_yaw'] - d['yaw'] + 180) % 360 - 180)
                if turn > 95:
                    faults.append(f'{t:.2f}s {name}: head turned {turn:.0f} degrees from his body')
                if d['held_over_back']:
                    faults.append(f'{t:.2f}s {name}: seen from behind, what he holds is drawn over his back')
    return faults


def audits():
    return []


# ------------------------------------------------------------------------------------------------ the cast sheet
def cast_sheet(out):
    """The cast (guides/satire.md, Start 3): Andy and Wes from every view they appear in, the robot from every view
    with both arms (blade and cannon palm), Andy's fear in six strengths for Sam to pick from, and the props at real
    size beside a 1.75 m scale person and a 1 m ruler (sizes.scale_ref)."""
    import landmarks
    import sizes
    B.SS = 1
    W_, H_ = 2160, 4760
    bg = (236, 232, 224, 255)
    img = Image.new('RGBA', (W_, H_), bg)
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 46)
    mid = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
    cam = B.Cam(1.0, 540, 960)
    d.text((60, 30), "PREPPER MINISTER: the cast", font=big, fill=(30, 30, 30))

    def label(x, y, s_):
        d.text((x, y), s_, font=small, fill=(40, 40, 40), anchor='mm')

    def tile(draw, box, at):
        lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        draw(lay)
        img.alpha_composite(lay.crop(box), at)

    views5 = [(0, 'front'), (45, 'three-quarter'), (90, 'side'), (135, '3/4 back'), (180, 'back')]
    # row 1: Andy (white shirt, top button undone, sleeves rolled, navy chinos, tan belt; the Glock behind it)
    d.text((60, 110), 'ANDY: five views (the Glock tucked behind his belt shows from behind)', font=mid, fill=(30, 30, 30))
    for i, (yaw, name) in enumerate(views5):
        tile(lambda im, yaw=yaw: C.person(im, cam, 540, 300, 0.62, dict(C.fear(C.ANDY, 1), glock_tucked=True), 0.0, yaw),
             (340, 120, 740, 900), (40 + 360 * i, 160))
        label(240 + 360 * i, 960, name)
    tile(lambda im: C.person(im, cam, 540, 300, 0.62, C.fear(C.ANDY, 4), 0.0, 90, C.glock_aim(C.fear(C.ANDY, 4), (0, 0), 1.0)),
         (340, 120, 900, 900), (1830, 160))
    label(1990, 960, 'Glock, firing')
    # row 2: Wes (the torn suit), five views; with the minigun and the belt bandana; with the machete
    d.text((60, 1010), 'WES: five views (suit ripped and dirty, no blood); the minigun and belt; the oiled machete',
           font=mid, fill=(30, 30, 30))
    for i, (yaw, name) in enumerate(views5):
        tile(lambda im, yaw=yaw: C.person(im, cam, 540, 300, 0.62, C.WES, 0.0, yaw), (340, 120, 740, 900), (40 + 280 * i, 1060))
        label(240 + 280 * i, 1860, name)
    w = dict(C.WES, bandana=True)
    tile(lambda im: C.person(im, cam, 540, 300, 0.62, w, 0.0, 30, C.minigun_hip(w, (-25, 0), spin=0.4, flash=1.0)),
         (240, 120, 760, 900), (1390, 1060))
    label(1650, 1860, 'minigun, belt bandana')
    jm = V.standing(C.WES)
    V.arm_to(jm, 'R', (190, 330, 120), 'down', 'fist')
    jm['props'] = [C.machete('R')]
    jm['grip'] = {'R'}
    tile(lambda im: C.person(im, cam, 540, 300, 0.62, C.WES, 0.0, 0, jm), (360, 120, 760, 900), (1760, 1060))
    label(1960, 1860, 'machete')
    # row 3: Andy's fear 1-6, close
    d.text((60, 1920), "ANDY'S FEAR, 1 to 6: pick a number per shot (my plan: 1, 1, 3, 4, -, 3, 5, -, 6, -, 6, 6)",
           font=mid, fill=(30, 30, 30))
    for i in range(6):
        tile(lambda im, i=i: C.person(im, cam, 540, 500, 1.3, C.fear(C.ANDY, i + 1), 0.0, 0), (360, 220, 720, 720),
             (20 + 356 * i, 1980))
        label(200 + 356 * i, 2500, C.FEAR[i]['name'])
    # row 4: the robot
    d.text((60, 2560), 'THE ROBOT (2.1 m): five views; blade arm or cannon palm; one cobalt eye sweeping side to side',
           font=mid, fill=(30, 30, 30))
    for i, (yaw, name) in enumerate([(180, 'front (blade)'), (225, '3/4, cannon aimed'), (270, 'side (blade)'),
                                     (315, '3/4 back (cannon)'), (0, 'back (blade)')]):
        def rob(im, i=i, yaw=yaw):
            rc = S.Cam((0, 1.2, -4.6), (0, 1.12, 0), focal=1300)
            p = R.pose(pos=(0.0, 0.0), yaw=yaw, sweep=[-1, -0.3, 0.4, 1, 0][i])
            if i == 1:
                a_, pole = R.aim((-2.0, 1.5, -4.0), (0, 0), yaw, 'R')
                p['handR'], p['poleR'] = a_, pole
            R.draw(im, rc, p, {'arms': {'R': 'blade' if i % 2 == 0 else 'cannon', 'L': 'hand'}}, 0.0)
        tile(rob, (240, 360, 840, 1520), (30 + 400 * i, 2610))
        label(330 + 400 * i, 3790, name)
    # row 5: the props at real size, beside a 1.75 m person and a 1 m ruler
    d.text((60, 3860), 'THE PROPS at real size (the grey figure is 1.75 m; the red ruler 1 m)', font=mid, fill=(30, 30, 30))
    ppm = 400
    yf = 4640
    sizes.scale_ref(d, 120, yf, ppm)
    pc = S.Cam((0, 0.0, -4.0), (0, 0.0, 0), focal=ppm * 4.0)
    def place(draw_fn, x_m):
        lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        draw_fn(lay)
        img.alpha_composite(lay, (int(x_m), yf - 960))
    place(lambda im: X.tin(im, pc, (0.0, 0.0, 0.0)), 420 - 540)
    place(lambda im: X.bottle(im, pc, (0.0, 0.0, 0.0)), 560 - 540)
    place(lambda im: X.alexa(im, pc, (0.0, 0.0, 0.0)), 730 - 540)
    place(lambda im: X.alexa_walker(im, pc, (0.0, 0.0, 0.0), 0.2, 160), 900 - 540)
    pcs = S.Cam((0, 0.6, -4.0), (0, 0.0, 0), focal=ppm * 4.0)
    place(lambda im: X.crossbow3(im, pcs, (0.0, 0.0, 0.0), 90), 1230 - 540)
    place(lambda im: X.minigun3(im, pcs, (0.0, 0.0, 0.0), 90), 1680 - 540)
    k = ppm * M                                    # the held pistol and machete at the same scale (person units)
    pen = B.Pen(img, B.Local(cam, 0, 0, k))
    j2 = {'elR': (1960 / k - 200, (yf - 260) / k), 'wrR': (1960 / k, (yf - 260) / k), 'yaw': 0}
    C.glock('R')(pen, j2)
    j2 = {'elR': (1890 / k - 200, (yf - 80) / k), 'wrR': (1890 / k, (yf - 80) / k), 'yaw': 0}
    C.machete('R')(pen, j2)
    for x_, s_ in ((490, 'beans, water'), (815, 'Alexa; on legs'), (1230, 'crossbow'), (1680, 'minigun'),
                   (2010, 'Glock, machete')):
        label(x_, yf + 20, s_)
    img.convert('RGB').save(out, quality=88)
    print('saved', out)


def LINE_SUBJECTS():
    def one(sp):
        def d_(im):
            C.person(im, B.Cam(1.0, 540, 960), 540, 420, 1.45, sp, 0.0, 0)
        return d_
    return [('Andy', one(C.ANDY)), ('Wes', one(C.WES))]


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        cast_sheet(a[1])
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'check':
        B.SS = 1
        checks()
        print('check: clean')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None)


def tin11_at(t):
    """Shot 11: the tin's flight from Andy's hand to robot 5 in the hall-to-kitchen door."""
    a, b = (-2.45, 1.15, 2.55), (-1.25, 1.6, 5.45)
    k = min(1.0, max(0.0, (t - THROW11) / (DENT11 - THROW11)))
    p = lerp3(a, b, k)
    return (p[0], p[1] + 0.5 * math.sin(math.pi * k), p[2])


if __name__ == '__main__':
    main()
