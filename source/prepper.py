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
    dict(n=8, who='Wes', audio='prepper/line-08-wes-too-late', at=24.25, text="It's too late. They're here.",
         chunks=[(0.97, "It's too late."), (2.37, "They're here.")]),
    dict(n=9, who='Andy', audio='prepper/line-09a-beans', at=30.3,
         text='We are already out of time. Did you get the beans? DID YOU GET THE BEANS?',
         chunks=[(0.7, 'We are already'), (1.7, 'out of time.'), (3.29, 'Did you get the beans?'),
                 (4.99, 'DID YOU GET THE BEANS?')]),
    dict(n=10, who='Andy', audio='prepper/line-09b-streeting', at=38.9,
         text="Streeting, you pussy, there's a minigun in the kitchen.",
         chunks=[(0.84, 'Streeting,'), (1.74, 'you p****,'), (3.03, "there's a minigun"), (3.85, 'in the kitchen.')],
         # Sam's notes 33 and 54 (25 Oct): "you" was cut off twice. Sam never said "pussy": he left a gap for the bleep.
         # In the recording "Streeting," runs 0.82-1.54, "you" 1.72-1.90, then his blank gap 1.92-3.0 before "there's".
         # The bleep sits in that gap (it had covered "you"), and the mouth says "pussy" under it
         bleep=(2.0, 2.42)),
]
# Sam's note 30 (25 Oct): hold on robot 5 a second longer after the tin hits it, so shot 11 runs 3 s and the rest
# moves on a second (shot 12 now 51-62 s)
T = dict(s1=0.0, s2=2.1, s3=4.2, s4=6.85, s5=9.3, s6=14.2, s7=18.6, s8=22.1, s9=28.3, s10=43.0, s11=48.0, s12=51.0,
         end=62.0)
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
# shot 8 (Sam's note 35, 25 Oct: the door lingered): the camera arrives in 1.2 s and Wes boots the door as it does;
# Wes's line follows 0.9 s after; robot A walks the hall, turns, takes the bolt in the head and slumps down the wall
DOOR8, ROBOT8, TURN8, BOLT8 = 23.35, 25.3, 26.0, 26.6
BOLT8_HIT = BOLT8 + 0.12
SPIN9, LUNGE9, SHOTS9 = 29.4, 36.8, (37.3, 37.55, 37.8)
WINDOW10, PLASMA10, FIRE10 = 45.0, 45.6, 46.1
GRAB11, THROW11, DENT11 = 48.45, 48.9, 49.6      # the grab; the release (out of frame); the tin strikes robot 5
LAND11 = 50.15                                      # the tin down on the floor, where it stays
# What the shared checks need
KEEP_CLEAR = []
PROP_SIZES = [('crossbow', 'crossbow', 0.72, 0.3, None), ('minigun', 'minigun', 0.9, 0.25, None),
              ('pistol', 'pistol', 0.186, 0.138, None), ('machete', 'machete', 0.6, 0.06, None),
              ('beans', 'can', 0.066, 0.11, None), ('water', '2L bottle', 0.105, 0.33, None),
              ('alexa', 'smart speaker', 0.1 * X.ALEXA_K, 0.09 * X.ALEXA_K, None), ('robot', 'robot', 0.6, 2.1, None)]
HEIGHTS = C.HEIGHTS
OUTFIT = {'Andy': {'shirt hem (tucked, belt)': 468}}
ALLOWED_CONTACTS = [   # (thing or thing.part, thing or thing.part, from, to, why)
    ('WALL*', 'WALL*', None, None, 'walls meet at the corners'),
    ('WALL*', 'DRINKS CABINET', None, None, 'the cabinet stands against the wall'),
    ('WALL*', 'MEDIA UNIT', None, None, 'the media unit stands against the wall'),
    ('Andy.*', 'SOFA', None, T['s8'] + 0.6, 'he sits on it (shots 1-4 and 7; shot 8 starts on him seated)'),
    ('Wes.footR', 'WALL*', DOOR8 - 0.05, DOOR8 + 0.45, 'his kick lands on the door in its frame'),
    ('Wes.*', 'ISLAND', 43.9, 44.45, 'he grabs the minigun off the island top'),
    ('Wes.gun', 'ISLAND', None, None, 'the barrels held just over the island edge (a few cm, the box is the worktop)', 0.05),
]
ALLOWED_POPS = [       # (thing, from, to, why)
    ('robot C', 44.1, 44.4, 'walks in along the outside of the kitchen wall: the wall hides it until the window'),
    ('robot D', 44.25, 44.55, 'walks in along the outside of the kitchen wall: the wall hides it until the window'),
]
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
    if ln.get('bleep'):                              # the mouth moves under the bleep (the word said, not heard)
        ln['_stretches'] = sorted(ln['_stretches'] + [tuple(x - cut for x in ln['bleep'])])
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
        return S.Cam((-2.8, 1.75, 0.95), (-2.85, 0.92, 2.7), focal=1550)   # higher (note 27): the crossbow seen from above
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
        k = ease(u / 1.2)
        i = min(len(pts) - 1, int(k * (len(pts) - 1)))
        look = lerp3((3.0, 1.0, 3.7), PL.CAMS[8]['look'], ease(u / 1.0))
        return S.Cam(pts[i], look, focal=1150)
    if s == 's9':
        return S.Cam((3.0, 1.15, 0.35), (2.7, 1.15, 5.4), focal=760)
    if s == 's10':                                  # Wes with the window behind him; a snap in on his snarl (note 36)
        look0, look1 = (-3.8, 1.4, 3.6), (WES10[0], 1.62, WES10[1])
        k = ease((t - (SNARL10 - 0.25)) / 0.2) if t < SPIN10 - 0.05 else 0.0
        return S.Cam(CAM10, lerp3(look0, look1, k), focal=800 + 1500 * k)
    if s == 's11':                                  # low over the island on the tin; whips after it to robot 5
        start, look0 = CAM11, (TIN_SPOTS[2][0], 0.98, TIN_SPOTS[2][1])
        end, look1 = (-1.55, 1.35, 3.3), (-1.2, 1.45, 5.85)
        if t < THROW11:
            return S.Cam(start, look0, focal=1400)
        k = ease((t - THROW11) / 0.6)
        tin = tin11_at(min(t, DENT11))
        tin = (tin[0], min(tin[1], 1.55), tin[2])          # the whip follows it, never tipping up to the ceiling
        look = lerp3(look0, tin, ease((t - THROW11) / 0.25)) if t < DENT11 else lerp3(tin, look1, ease((t - DENT11) / 0.5))
        return S.Cam(lerp3(start, end, k), look, focal=1400 - 300 * k)
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
    if j is not None and j.get('sofa'):              # how much lower a point a thigh's length nearer sits, this camera
        dz = 0.42
        (_, Yq), _ = cam.project((x + fd[0] * dz, lift, z + fd[1] * dz))
        j['elev'] = max(V.ELEV, (Yq - Yf) / s / (dz / (M * f)))
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
    j['sofa'] = True
    j['bob'] = V.SEAT_DROP - 50                      # sat up on the cushion (his hips were sunk below its top)
    j['lean'] = lean
    return j


_LEG, _TUBE = V.leg, V.tube


def _sofa_leg(p, j, side, yaw, sp):
    """Sam's note 25 (25 Oct): seen from the front on the sofa Andy looked squat (the rig's small fixed camera tilt
    flattened his thighs to nothing, so he read as a short man standing). Seated, his legs are seen through this
    camera's real tilt: the thighs come towards us as a lap, the knees lower and fuller, the shins drop to feet set
    forward of the seat."""
    e = j.get('elev')
    if e is None or abs(((yaw + 180) % 360) - 180) > 30:
        return _LEG(p, j, side, yaw, sp)
    sg = -1 if side == 'L' else 1
    (hx, hy), _ = V.project(j['hip' + side], 0)
    kx, ky = sg * 92.0, hy + max(92.0, e * V.THIGH)   # knees a little apart, nearer us: lower and fuller
    fx_, fy_ = sg * 70.0, ky + V.SHIN * 0.92 + 50      # the hips sat 50 up on the cushion: the feet still on the floor
    _TUBE(p, [(hx, hy), (kx, ky), (fx_, fy_)], [52, 50, 33], sp.get('trousers', (40, 40, 46)))
    p.line([(kx - sg * 30, ky - 6), (kx - sg * 8, ky + 4)], B.dk(sp.get('trousers', (40, 40, 46)), 0.7), 2.0)   # a crease
    shoe = [(fx_ - 34, fy_ - 6), (fx_ + 34, fy_ - 6), (fx_ + 40, fy_ + 22), (fx_ + 30, fy_ + 40), (fx_ - 30, fy_ + 40),
            (fx_ - 40, fy_ + 22)]
    p.poly(V.curve(shoe, 3), sp.get('shoe', (22, 20, 22)), V.INK, 2.4)


V.leg = _sofa_leg


# ------------------------------------------------------------------------------------------------ Andy
# Sam's note 37 (25 Oct): the wave only came up level with his chest. Now a real hello: the hand up beside his head,
# palm to us, three flicks side to side, then down (the elbow out to the side, clear of the shoulder)
WAVE = filmkit.Beats([(0.25, 'set-up', (150, 300, 60)), (0.55, 'raise', (215, -270, 70)),
                      (0.72, 'flick', (275, -275, 60), 'fast'), (0.89, 'flick', (185, -275, 75), 'fast'),
                      (1.06, 'flick', (275, -275, 60), 'fast'), (1.23, 'flick', (200, -270, 75), 'fast'),
                      (1.75, 'down', (150, 300, 60), 'slow')])


# (Sam, 25 Oct: pointed straight at the lens the forearm shrank to nothing and the hand floated off the sleeve: the
# hand comes forward and up, so the forearm stays in view, rising from the elbow to the hand)
REACH2 = filmkit.Beats([(0.0, 'rest', (150, 300, 60)), (0.35, 'reach', (120, 40, 210), 'fast'),
                        (2.0, 'hold', (119, 42, 206))])
PUSH2 = filmkit.Beats([(0.0, 'set', (119, 42, 206)), (0.12, 'push', (112, 30, 245), 'fast'),
                       (0.45, 'settle', (118, 38, 220), 'slow'), (2.0, 'hold', (118, 38, 220))])


def near_hand(side, z):
    """A hand reaching towards the lens, drawn bigger the nearer it comes (the rig's hands are all one size): a plain
    circle, the house hand, over the end of the arm."""
    def draw(p, j2):
        (ex, ey), (wx, wy) = j2['el' + side], j2['wr' + side]
        d = math.hypot(wx - ex, wy - ey) or 1.0
        c = (wx + (wx - ex) / d * 14, wy + (wy - ey) / d * 14)          # where the house hand sits on the wrist
        r = 25 * (1.0 + 0.3 * max(0.0, min(1.0, z / 260.0)))
        p.ell(c[0], c[1], r, r * 0.94, C.ANDY['skin'], V.INK, 2.6)
    draw.held = False
    return draw


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
    if s == 's1':                                    # a hello wave, right hand up by his head
        hx, hy, hz = WAVE.at(u)
        V.arm_to(j, 'R', (hx, hy, hz), 'out', 'palm' if hy < 150 else 'fist')
    elif s == 's2':                                  # Sam's note 39: reaching forward to us, 'here's a fact for you'
        ln = next(l_ for l_ in LINES if l_['n'] == 2)
        nb = ln['start'] + ln['chunks'][1][0] - ln['_cut'] - shot_start(t)   # "no biggie" (in the shot's own time)
        reach = REACH2.at(u) if u < nb - 0.12 else REACH2.at(nb - 0.12) if u < nb - 0.05 else PUSH2.at(u - nb + 0.05)
        V.arm_to(j, 'R', reach, 'down', 'none')
        j['props'] = j.get('props', []) + [near_hand('R', reach[2])]
        V.arm_to(j, 'L', (-70, 420, 260), 'down', 'fist')
        j['lean'] = 14 + 10 * ease(u / 0.35)
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
COFFEE = (3.3, 0.4, 2.3)                             # Andy's coffee on its coaster (Sam's note 32), right of the books
TIN_SPOTS = [(-3.45, 2.75), (-3.3, 2.98), (-3.2, 2.72)]   # moved back a little: the crossbow lies in front (note 27)
BOTTLE_SPOTS = [(-2.75, 2.82), (-2.58, 2.6)]
CROSSBOW_SPOT = ((-2.86, 2.7), 184)               # Sam's note 27: in clear view, limbs across the frame
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
    if t < GRAB10[0]:
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


# ------------------------------------------------------------------------------------------------ shots 8-11
WES_KICK8 = (2.6, 6.0)                              # Wes kicks the door from here (in the hall, behind it)
WES_DOOR8 = (2.55, 5.05)                            # and lurches through the doorway, a step into the room (his raised
#                                                     arm was in the frame's jambs: Sam's note 43)
WES_BACK9 = (1.75, 4.65)                            # shot 9: he backs away from the door to here, beside the cabinet
WES_RUN9 = [(1.75, 4.65), (0.75, 3.9), (-0.2, 3.35), (-0.8, 3.4), (-2.7, 3.55)]   # clear of the cabinet and the opening's edge   # runs for the kitchen (on into 10)
RUN9 = 42.35


def duck(j, k):
    """Down in a crouch, both feet planted (k 0 standing .. 1 down)."""
    drop = 190.0 * k
    j['bob'] = j.get('bob', 0.0) + drop
    floor = V.ANKLE_Y - drop
    j['footR'] = (85.0, floor, 30.0)
    j['footL'] = (-85.0, floor, -25.0)
    j['knee_poleR'] = (0.25, -0.2, 1.0)
    j['knee_poleL'] = (-0.25, -0.2, 1.0)
    j['lean'] = j.get('lean', 0.0) + 22 * k
    return j


def machete_up(j, k=1.0, t=0.0, pole='out'):
    """The machete raised in his right fist, ready (k 0 down at his side .. 1 up by his shoulder), a small shake."""
    sh = 0.0 if k < 1 else 6 * math.sin(t * 9.0)
    V.arm_to(j, 'R', (150 + 10 * k, 330 - 230 * k + sh, 60 + 130 * k), pole, 'fist')   # elbow in (note 43)
    up_ = (0.3 + 0.2 * k, -1.0, 0.25 - 0.1 * k)                   # blade up, tipped out and a little forward (his
    j['props'] = j.get('props', []) + [C.machete('R', aim3=up_)]   # own frame: it turns with him, note 45)
    j['grip'] = set(j.get('grip', set())) | {'R'}
    return j


def wes_face(t, level=5):
    sp = C.fear(C.WES, level, talking=talking('Wes', t))
    sp['skin'] = C.WES['skin']                       # Wes keeps his own colour (the pallor table is Andy's)
    m = mouth_at('Wes', t)
    sp['mouth'] = m or 'set'
    sp['blink'] = F.blinking(t, BLINKS['Wes'])
    return sp


def kick_leg(side, k, sp):
    """A leg kicked straight at the lens, foreshortened the cartoon way (Sam's note 42): the trouser leg widens as it
    comes towards us from the hip, a touch lighter than the jacket and firmly inked so it reads over it, and ends in
    the big sole of the shoe facing us (tread and heel). `k` 0..1: how far out it is."""
    trousers = sp.get('trousers', C.WES.get('trousers', (34, 40, 66)))
    lit = tuple(int(c + (min(255, c * 1.35 + 12) - c) * k) for c in trousers)   # lighter only while it's out
    def draw(p, j2):
        (hx, hy), (fx_, fy_) = j2['hip' + side], j2['foot' + side]
        cx, cy = fx_, fy_ + 10                         # on the real foot, covering its shoe (Sam: a double foot)
        w0, w1 = 52.0, 52.0 + 46.0 * k                                   # widening towards us
        dx, dy = cx - hx, cy - hy
        n = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / n, dx / n
        p.poly([(hx + nx * w0, hy + ny * w0), (cx + nx * w1, cy + ny * w1), (cx - nx * w1, cy - ny * w1),
                (hx - nx * w0, hy - ny * w0)], lit, V.INK, 2.6)
        p.ell(cx, cy, w1, w1 * 0.8, lit, V.INK, 2.6)                     # the trouser hem round the ankle, end on
        sw, sh_ = w1 * 0.78, w1 * 1.25                                   # the sole, toe up, facing us
        p.ell(cx, cy - sh_ * 0.25, sw, sh_ * 0.62, (26, 24, 26), V.INK, 2.6)
        p.ell(cx, cy + sh_ * 0.42, sw * 0.82, sh_ * 0.36, (26, 24, 26), V.INK, 2.6)      # the heel
        for i in range(4):                                                # tread
            yy = cy - sh_ * 0.55 + i * sh_ * 0.16
            p.line([(cx - sw * 0.55, yy), (cx + sw * 0.55, yy)], (70, 66, 70), 2.2)
    draw.held = False
    return draw


def wes8(t):
    """Shot 8: Wes boots the door open from the hall, lurches into the doorway, machete up (fear 5): "It's too late."
    to Andy (to us), a glance back east down the hall, "They're here."; a shocked glance at the robot as the bolt hits
    it, then he turns to face it."""
    sp = wes_face(t)
    hf = None
    if t < DOOR8 + 0.55:                             # the kick (the door hides him until it flies open)
        # Sam's note 42 (25 Oct): the kicking leg was cramped, folded into his lower body (the library's front kick
        # aims the foot at the lens, so the whole leg shrank under the jacket), and it was over before the door showed
        # him. His own kick, still facing us: knee up, then the leg driven out nearly straight (hip to foot 96% of its
        # length), the foot out to his right and up at hip height, drawn over his body; held a third of a second after
        # the door flies open, then the foot comes down as he steps through
        rest = moves.pose(sp, 'standing')
        chamber = moves.pose(sp, 'standing')
        chamber['footR'] = (70.0, 560.0, 190.0)
        chamber['lean'] = -6
        out = moves.pose(sp, 'standing')
        out['footR'] = (70.0, 420.0, 440.0)                  # straight out at the door (at us), hip height
        out['footL'] = (-60.0, V.ANKLE_Y, -30.0)
        out['lean'] = -16
        down = moves.pose(sp, 'standing')
        down['footR'] = (60.0, V.ANKLE_Y, 150.0)
        down['footL'] = (-60.0, V.ANKLE_Y, -60.0)
        down['lean'] = 6
        j = moves.keyed(t, [(DOOR8 - 0.45, rest), (DOOR8 - 0.15, chamber), (DOOR8, out), (DOOR8 + 0.35, out),
                            (DOOR8 + 0.45, chamber), (DOOR8 + 0.55, down)],   # the knee snaps back, then the foot down
                        curve='fast' if t < DOOR8 else 'ease')
        V.arm_to(j, 'L', (-170, 330, 80), 'down', 'fist')     # the free arm forward for balance, close in
        fz = j['footR'][2]
        if fz > 200 and j['footR'][1] < 600:          # the leg coming at us: drawn foreshortened, over his body
            j['props'] = j.get('props', []) + [kick_leg('R', min(1.0, (fz - 200) / 240), sp)]
        machete_up(j, 0.6, t)
        return sp, j, WES_KICK8[0], WES_KICK8[1], 180.0, hf
    u = (t - DOOR8 - 0.55) / 0.4                     # the lurch in: two quick steps
    if u < 1.0:
        j = moves.gait(sp, t - DOOR8, 'brisk')
        k = ease(u)
        x, z = WES_KICK8[0] + (WES_DOOR8[0] - WES_KICK8[0]) * k, WES_KICK8[1] + (WES_DOOR8[1] - WES_KICK8[1]) * k
        j['lean'] = 10.0
        machete_up(j, 0.6 + 0.4 * k, t, pole='down')  # elbow down through the doorway (it caught the jamb)
        return sp, j, x, z, 180.0, hf
    x, z = WES_DOOR8
    j = V.standing(sp)
    j['footL'] = (-80, V.ANKLE_Y, 20.0)
    j['footR'] = (70, V.ANKLE_Y, -15.0)
    j['lean'] = 5.0 + 2 * filmkit.shifts(t, seed=8, amount=1.0)
    machete_up(j, 1.0, t)
    fac = 180.0
    if 25.05 <= t < 25.5:                            # a glance back down the hall, over his left shoulder
        hf = 95.0
    # Sam's note 44 (25 Oct): no duck (Andy has a clear line past him): as the bolt hits, his eyes and head snap
    # over his left shoulder to the robot, shocked (brows up, mouth dropped); then he turns to face it
    if BOLT8_HIT - 0.04 <= t < BOLT8 + 0.6:
        hf = 100.0
        sp.update(wes_face(t, 6))
        sp['skin'] = C.WES['skin']
        sp['mouth'] = 'open'
        j['lean'] = j.get('lean', 0.0) - 4.0
    if t >= BOLT8 + 0.6:                             # facing the robot in the hall
        fac = 0.0
        sp['mouth'] = 'set'
    return sp, j, x, z, fac, hf


def wes9(t):
    """Shot 9: Wes backs away from the door (still facing it), then faces Andy; flinches at the lunge; runs for the
    kitchen as Andy shouts at him."""
    sp = wes_face(t, 5)
    a, b = WES_DOOR8, WES_BACK9
    t0, t1 = 28.4, 30.0
    hf = None
    if t < t0:
        j = V.standing(sp)
        machete_up(j, 1.0, t)
        return sp, j, a[0], a[1], 0.0, hf
    if t < t1:                                       # backing away: the walk run backwards, facing the door
        # Sam's note 47 (25 Oct): the straight diagonal took his shoulder back through the door's west jamb. He backs
        # straight out of the doorway first (0.5 m south), then angles off to the cabinet
        u = ease((t - t0) / (t1 - t0))
        j = moves.gait(sp, -(t - t0) * 0.8, 'walk')
        machete_up(j, 1.0, t)
        mid = (a[0], a[1] - 0.5)
        L1, L2 = math.dist(a, mid), math.dist(mid, b)
        d_ = u * (L1 + L2)
        if d_ < L1:
            q = (a[0], a[1] - d_)
        else:
            k = (d_ - L1) / L2
            q = (mid[0] + (b[0] - mid[0]) * k, mid[1] + (b[1] - mid[1]) * k)
        return sp, j, q[0], q[1], 0.0, hf
    if t < RUN9:
        j = V.standing(sp)
        j['footL'] = (-80, V.ANKLE_Y, 20.0)
        j['footR'] = (75, V.ANKLE_Y, -15.0)
        j['lean'] = 4.0 + 2 * filmkit.shifts(t, seed=9, amount=1.0)
        machete_up(j, 1.0, t)
        fac = 120.0 if t >= 30.15 else 0.0           # turns to Andy (east-south-east of him)
        if LUNGE9 <= t < LUNGE9 + 0.6:               # a flinch back from the lunge
            k = math.sin(math.pi * (t - LUNGE9) / 0.6)
            j['lean'] -= 10 * k
            j['head_dy'] = -8 * k
            fac = 160.0
        if LUNGE9 + 0.6 <= t < SHOTS9[-1] + 0.5:
            fac = 175.0                              # watching the fight
        return sp, j, b[0], b[1], fac, hf
    x, z, yaw, state = moves.travel(WES_RUN9, t, 'run', start=RUN9)
    j = moves.gait(sp, t - RUN9, 'run') if state == 'moving' else V.standing(sp)
    machete_up(j, 0.7, t)
    return sp, j, x, z, yaw, hf


ANDY_AIM9 = (2.95, 2.87)


FLING9 = (29.45, 29.95)                             # the crossbow flung aside: leaves his hands, lands
XBOW_LANDS = ((3.85, 2.45), 35.0)
SIDESTEP9 = (36.95, 37.2)
ANDY_STEP9 = (3.8, 2.8) 


def andy9(t):
    """Shot 9: Andy aiming the crossbow at the door (his back to us), pops round to us, flings the crossbow aside,
    the Glock from behind his belt up by his face for the line; robot B lunges, swipes and misses as he sidesteps; he
    pops to face it and shoots it down; then guards the opening in profile for "Streeting...", eyes flicking to Wes."""
    sp = C.fear(C.ANDY, FEAR_AT['s9'], talking=talking('Andy', t))
    m = mouth_at('Andy', t)
    sp['mouth'] = m or 'set'
    sp['blink'] = F.blinking(t, BLINKS['Andy'])
    x, z = ANDY_AIM9
    hf = None
    rec = {}
    if t < SPIN9:
        j = C.crossbow_aim(sp, (0.0, 2.0), loaded=False)
        return sp, j, x, z, 355.0, hf, rec
    if t < FLING9[0]:                                # popped round to us, the crossbow swinging out to his left
        j = V.standing(sp)
        V.arm_to(j, 'L', (-230, 160, 120), 'out', 'fist')
        V.arm_to(j, 'R', (150, 330, 60), 'out', 'fist')
        return sp, j, x, z, 180.0, hf, rec
    j = V.standing(sp)
    j['footL'] = (-80, V.ANKLE_Y, 15.0)
    j['footR'] = (75, V.ANKLE_Y, -10.0)
    V.arm_to(j, 'L', (-170, 330, 40), 'out', 'palm')
    if t < 29.8:                                     # right hand behind his belt for the Glock
        k = ease((t - FLING9[0]) / 0.35)
        V.arm_to(j, 'R', (150 + 20 * k, 330 + 60 * k, 40 - 140 * k), 'out', 'fist')
        return sp, j, x, z, 180.0, hf, rec
    if t < SIDESTEP9[0]:                             # the Glock up by his face, muzzle up; leaning in on the shout
        k = ease((t - 29.8) / 0.25)
        V.arm_to(j, 'R', (170 - 20 * k, 390 - 450 * k, -100 + 190 * k), 'out', 'fist')
        j['props'] = [C.glock('R', 0.0, (0.0, -1.0, 0.15), rec)]
        j['grip'] = {'R'}
        ln = next(l_ for l_ in LINES if l_['n'] == 9)
        shout = ln['start'] + ln['chunks'][3][0] - ln['_cut']
        if t >= shout - 0.1:
            j['lean'] = 14.0 * ease((t - shout + 0.1) / 0.25)
        j['lean'] = j.get('lean', 0.0) + 1.5 * filmkit.shifts(t, seed=19, amount=1.0)
        return sp, j, x, z, 180.0, hf, rec
    if t < SIDESTEP9[1]:                             # the sidestep away from the blade
        k = ease((t - SIDESTEP9[0]) / (SIDESTEP9[1] - SIDESTEP9[0]))
        x, z = x + (ANDY_STEP9[0] - x) * k, z + (ANDY_STEP9[1] - z) * k
        j = moves.gait(sp, t - SIDESTEP9[0], 'brisk')
        j['lean'] = -8.0
        V.arm_to(j, 'R', (150, -60, 90), 'out', 'fist')
        j['props'] = [C.glock('R', 0.0, (0.0, -1.0, 0.15), rec)]
        j['grip'] = {'R'}
        return sp, j, x, z, 180.0, hf, rec
    x, z = ANDY_STEP9                                # facing it (west): shoots; then guards the opening in profile
    flash = any(0 <= t - s_ < 1 / FPS for s_ in SHOTS9)
    j = C.glock_aim(sp, (0.0, 4.0 if t < SHOTS9[-1] + 0.6 else 1.0), flash=1.0 if flash else 0.0, rec=rec)
    for s_ in SHOTS9:                                # the kick of each shot
        if 0 <= t - s_ < 0.12:
            j['lean'] = -3.0
    ln = next(l_ for l_ in LINES if l_['n'] == 10)
    stre = ln['start'] + ln['chunks'][0][0] - ln['_cut']
    if stre - 0.05 <= t < stre + 0.55:               # his eyes and head flick to Wes on "Streeting"
        hf = 330.0
    return sp, j, x, z, 270.0, hf, rec


def xbow9_at(t):
    """Where the flung crossbow is (x, y, z) and its yaw: out of his left hand, a tumbling arc, down where it lands."""
    a = (ANDY_AIM9[0] + 0.35, 1.1, ANDY_AIM9[1] - 0.1)
    (bx, bz), yaw1 = XBOW_LANDS
    u = (t - FLING9[0]) / (FLING9[1] - FLING9[0])
    if u >= 1.0:
        return (bx, 0.0, bz), yaw1
    u = max(0.0, u)
    y = a[1] * (1 - u) + 0.45 * math.sin(math.pi * u)
    return (a[0] + (bx - a[0]) * u, max(0.0, y), a[2] + (bz - a[2]) * u), yaw1 + 400 * (1 - u)


def _arrive10():
    for k in range(400):
        t = RUN9 + k * 0.01
        if moves.travel(WES_RUN9, t, 'run', start=RUN9)[3] == 'arrived':
            return t
    return RUN9 + 1.5


ARRIVE10 = _arrive10()                              # Wes reaches the island (about 43.8)
DROP10 = ARRIVE10 + 0.08                            # the machete dropped
GRAB10 = (44.05, 44.4)                              # the minigun dragged off the island, up to his hip
BELT10 = (44.55, 44.8)                              # the belt flung over his head: the bandana
SNARL10 = 45.2
SPIN10 = 45.95                                      # Sam's note 36: snarl at us, eyes left, then he spins and fires
WES10 = (-2.7, 3.55)
CAM10 = (-1.0, 1.5, 2.6)                            # east of him: the gun shows side-on, clear of the bottles
MACHETE10 = ((-2.35, 3.8), 115.0)                   # where the dropped machete lies (and stays: shot 12 too)
FACE_CAM10 = math.degrees(math.atan2(CAM10[0] - WES10[0], CAM10[2] - WES10[1])) % 360


def snarl_prop(p, view, sp, hx, hy):
    """Sam's note 36: Wes's snarl (lips drawn back, both rows of teeth bared, the corners pulled down hard)."""
    if view != 'front':
        return
    fx, my = hx, hy + 60
    INK = V.INK
    p.poly([(fx - 32, my - 6), (fx - 12, my - 12), (fx + 12, my - 12), (fx + 32, my - 6), (fx + 26, my + 22),
            (fx - 26, my + 22)], (70, 20, 26), INK, 2.6)
    p.poly([(fx - 27, my - 5), (fx - 11, my - 10), (fx + 11, my - 10), (fx + 27, my - 5), (fx + 24, my + 2),
            (fx - 24, my + 2)], (240, 236, 220), None)
    p.poly([(fx - 22, my + 14), (fx + 22, my + 14), (fx + 21, my + 20), (fx - 21, my + 20)], (240, 236, 220), None)
    for k in range(-2, 3):
        p.line([(fx + k * 9, my - 9), (fx + k * 9, my + 2)], (170, 164, 140), 1.2)
    for sg in (-1, 1):
        p.line([(fx + sg * 32, my - 6), (fx + sg * 40, my + 14)], INK, 2.0)
        p.line([(fx + sg * 16, my - 34), (fx + sg * 28, my - 20)], B.dk(sp['skin'], 0.75), 2.0)   # the nose wrinkled


def wes10(t):
    """Shot 10: Wes runs in, drops the machete, drags the minigun off the island to his hip, flings the belt over his
    head (the bandana), snarls at us, eyes sliding left to the window behind him, spins and opens up on the robots."""
    sp = wes_face(t, 5)
    rec = {}
    if t < ARRIVE10:
        x, z, yaw, state = moves.travel(WES_RUN9, t, 'run', start=RUN9)
        j = moves.gait(sp, t - RUN9, 'run')
        machete_up(j, 0.7, t)
        return sp, j, x, z, yaw, None, rec
    x, z = WES10
    if t < GRAB10[0]:                                # the machete gone; turning to the island, reaching for the gun
        j = V.standing(sp)
        if t < DROP10:
            machete_up(j, 0.7, t)
        k = ease((t - DROP10) / 0.15)
        for sd, sg in (('R', 1), ('L', -1)):
            V.arm_to(j, sd, (sg * 110, 330 + 60 * k, 90 + 170 * k), 'out', 'fist')
        j['lean'] = 18.0 * k
        return sp, j, x, z, 180.0, None, rec
    if t < GRAB10[1]:                                # dragged off the island, swung up to his hip as he turns to us
        k = ease((t - GRAB10[0]) / (GRAB10[1] - GRAB10[0]))
        j = C.minigun_hip(sp, (0.0, 40.0 * (1 - k)), spin=0.0, belt_to=None, rec=rec)
        fac = 180.0 + (FACE_CAM10 - 180.0) * k
        return sp, j, x, z, fac, None, rec
    sp['bandana'] = t >= BELT10[1]
    hang = (110.0, 260.0)
    if t < BELT10[0]:
        belt = None
    elif t < BELT10[1]:                              # flung up and over his head
        k = ease((t - BELT10[0]) / (BELT10[1] - BELT10[0]))
        a = math.pi * k
        belt = (hang[0] + (64 - hang[0]) * k + 120 * math.sin(a), hang[1] + (-196 - hang[1]) * k - 160 * math.sin(a))
    else:
        belt = (64.0, -196.0)
    firing = t >= FIRE10
    f = int(t * FPS)
    if t < SPIN10:
        fac = FACE_CAM10
        if t >= SNARL10:                             # the snarl, straight at us, his eyes sliding left
            sp['mouth'] = 'hidden'
            sp['brows'] = 'outrage'
            sp['look'] = -1.0
            sp['lid'] = -2
            sp['blink'] = False
        j = C.minigun_hip(sp, (0.0, 4.0), spin=0.0, belt_to=belt, rec=rec)
        if t >= SNARL10:
            j['head_props'] = j.get('head_props', []) + [snarl_prop]
            j['lean'] = j.get('lean', 0.0) + 4.0
        return sp, j, x, z, fac, None, rec
    sp['brows'] = 'outrage'
    sp['mouth'] = 'set'                              # jaw clenched as he fires (no voice: the mouth stays shut)
    sp['blink'] = False
    # side-on to us as he fires (seen from behind, the gun was hidden by his back), swung right onto the robots
    if shot_of(t) == 's11' and t < THROW11 + 0.3:    # only his muzzle would poke into the low tin shot: a flame
        firing = False                               # on the worktop with no gun (25 Oct), so no flash there
    j = C.minigun_hip(sp, (22.0, 4.0), spin=(t - FIRE10) * 6.0 if t >= FIRE10 else 0.0,
                      flash=(1.0 if f % 2 == 0 else 0.6) if firing else 0.0, belt_to=belt, rec=rec, seed=f)
    return sp, j, x, z, 228.0, None, rec


def plasma10():
    """Robot D's shot: from its palm, over Wes's left shoulder, past the lens, into the kitchen wall by the lounge."""
    p, _ = robot_pose('D', PLASMA10)
    J, _ = R.skeleton(p)
    o = np.array(J['handL'] if 'handL' in J else J['chest']) + np.array([0.15, 0.0, 0.0])
    a = math.radians(FACE_CAM10 - 90)                 # just over his left shoulder as he faces us
    via = np.array([WES10[0] + 0.28 * math.sin(a), 1.78, WES10[1] + 0.28 * math.cos(a)])
    d = via - o
    k = (0.0 - o[0]) / d[0]
    return tuple(o), tuple(o + d * k)


def _glass10():
    """Sam's note 36: the window going as the minigun opens up: every pane bursts, most of the glass blown out into
    the garden, some back onto the sink run and the floor, each piece its own size and spin; and the spent cases
    pouring from the gun."""
    pieces = []
    w = PL.OPENINGS['kitchen window']
    for i in range(3):
        z0 = w['span'][0] + (w['span'][1] - w['span'][0]) * (i + 0.5) / 3
        for part, y in (('low', 1.3), ('top', 2.05)):
            t0 = FIRE10 + 0.05 * i + (0.08 if part == 'top' else 0.0)
            pieces += X.burst(t0, (-5.6, y, z0), 11, 3.2, 300 + i * 10 + (part == 'top'), col=(214, 236, 246),
                              size=0.05, up=1.0, dirn=(-1.0, 0.0, 0.0), box=(-9.0, -5.6, 0.0, 5.4), tops=[])
            pieces += X.burst(t0, (-5.6, y, z0), 5, 1.8, 320 + i * 10 + (part == 'top'), col=(214, 236, 246),
                              size=0.04, up=0.6, dirn=(1.0, 0.0, 0.0), box=ALEXA_BOX, tops=TOPS)
    return pieces


GLASS10 = _glass10()


def _cases10():
    out = []
    for i in range(int((T['s11'] - FIRE10) * 14)):     # 14 cases a second, kicked out of his right side
        t = FIRE10 + i / 14
        rng = np.random.default_rng(700 + i)
        v = (rng.uniform(-0.4, 0.4), rng.uniform(1.2, 2.0), rng.uniform(1.2, 2.0))
        pc = X.Piece((WES10[0] - 0.05, 0.95, WES10[1] + 0.3), v, t, r=0.008, e=0.4, spin=rng.uniform(-20, 20),
                     box=ALEXA_BOX, tops=TOPS)
        pc.kind, pc.col, pc.size, pc.seed = 'case', X.BRASS, 0.022, 700 + i
        out.append(pc)
    return out


CASES10 = _cases10()


CAM11 = (-2.72, 1.0, 2.36)                          # skimming the island top, close on the tin Andy grabs
TIN_REST = (-1.55, 5.15)                            # where it ends up on the floor (shown in shot 12 too)


def _tin_hit():
    p, _ = robot_pose('5', DENT11)
    J, fr = R.skeleton(p)
    return tuple(J['chest'] + fr['chest'] @ np.array([-0.12, -0.03, 0.16]))   # off the centre ridge, so it shows


def andy_arm11(img, cam, t):
    """Shot 11: only Andy's left arm is in frame (he is just behind the camera, south of the island, the Glock in his
    right): it reaches in over the worktop, grabs the tin, and pulls back out of frame to throw."""
    tx, tz = TIN_SPOTS[2]
    grip = np.array([tx, 0.92 + 0.07, tz - 0.04])
    away = np.array([tx + 0.05, 1.2, 2.02])
    if t < 48.2 or t >= GRAB11 + 0.3:
        return
    if t < GRAB11:
        hand = away + (grip - away) * ease((t - 48.2) / (GRAB11 - 48.2))
    else:
        hand = grip + (away - grip) * ease((t - GRAB11) / 0.3)
    sh = np.array([-3.1, 1.32, 2.12])                   # leaning in over the island's edge
    d = hand - sh
    n = np.linalg.norm(d)
    up_, lo_ = 0.31, 0.29
    n2 = min(n, up_ + lo_ - 1e-3)
    dd = d / n
    pole = np.array([-0.6, 0.6, 0.0])
    pole = pole - dd * np.dot(pole, dd)
    pole /= np.linalg.norm(pole)
    x = (up_ ** 2 - lo_ ** 2 + n2 ** 2) / (2 * n2)
    el = sh + dd * x + pole * math.sqrt(max(0.0, up_ ** 2 - x ** 2))
    pts = []
    for q in (sh, el, hand):
        if cam.depth(tuple(q)) < 0.12:                   # the shoulder is behind the lens: run the arm off the frame
            q = el + (q - el) * 0.7
        pts.append(q)
    (hx, hy), k = cam.project(tuple(hand))
    s_ = k * M * C.HEIGHTS['Andy'] / 1.75
    Lc = B.Local(FLAT, 0.0, 0.0, s_, 1)
    j2 = {sd + 'L': (cam.project(tuple(q))[0][0] / s_, cam.project(tuple(q))[0][1] / s_) for sd, q in zip(('sh', 'el', 'wr'), pts)}
    j2['hand'] = {'L': 'fist'}
    sp = C.fear(C.ANDY, 6)
    V.arm(B.Pen(img, Lc), j2, 'L', sp)
    if t >= GRAB11:                                      # the tin in his fist
        X.tin(img, cam, (hand[0], hand[1] - 0.05, hand[2]))


def bolt8_at(t):
    """The bolt from Andy's crossbow (just behind the camera, unseen) to robot A's head."""
    p, _ = robot_pose('A', BOLT8_HIT)
    J, fr = R.skeleton(p)
    hit = J['head'] + fr['head'] @ np.array([0.0, 0.02, 0.09])
    a = np.array([2.95, 1.45, 2.95])
    u = (t - BOLT8) / (BOLT8_HIT - BOLT8)
    return tuple(a + (hit - a) * min(1.0, max(0.0, u))), tuple((hit - a) / np.linalg.norm(hit - a))


def bolt8_stuck(t):
    """Sam's plan: the bolt stays in robot A's head, moving with it as it slumps."""
    p0, _ = robot_pose('A', BOLT8_HIT)
    J0, fr0 = R.skeleton(p0)
    tip0, d0 = bolt8_at(BOLT8_HIT)
    H0 = fr0['head']
    loc_tip = H0.T @ (np.asarray(tip0) - J0['head'])
    loc_d = H0.T @ np.asarray(d0)
    p, _ = robot_pose('A', t)
    J, fr = R.skeleton(p)
    H = fr['head']
    return tuple(J['head'] + H @ loc_tip), tuple(H @ loc_d)


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
GARDEN = {'7': ((-12.2, 0.7), (-9.0, 1.2)), '8': ((-12.8, 4.7), (-9.2, 3.9))}   # 25 Oct: stop short of C and D lying there
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


def dent5(sp, t):
    """Sam's note 30: the tin leaves a dent in robot 5's chest, there from the hit until it is blown apart."""
    if t >= DENT11:
        sp['holes'].append(dict(part='chest', i=DENT5_I, t=DENT11, dent=True, r=0.07))


def andy_holes(name, sp):
    for i, (s_, who) in enumerate(ANDY_SHOTS):
        if who == name:
            sp['holes'].append(dict(part='chest', i=30 + 41 * i, t=T['s12'] + s_ + 0.03, r=0.026))


def robot_pose(name, t):
    """Every robot's pose at time t (and its spec, with damage so far). Bodies stay where they fall."""
    sp = dict(SPEC[name], name='robot ' + name)
    sp['holes'] = []
    if name == 'A':                                   # shot 8: walks the hall, turns to the door; the bolt; slumps
        # Sam's note 34 (25 Oct): it used to tip back out of sight. Now it staggers back to the hall's north wall and
        # slides down it to sit, the bolt in its head, sparking, and stays there in view (and in shot 12's hall)
        if t < TURN8:
            p = R.pose(**R.walk(t, (3.9, 6.1), (2.75, 6.1), ROBOT8, TURN8, stride=0.48))
            p['sweep'] = R.eye_sweep(t)
            return p, sp
        p = R.pose(pos=(2.75, 6.1), yaw=180 + 90 * (1 - ease((t - TURN8) / 0.15)), sweep=R.eye_sweep(t))
        if t >= BOLT8_HIT:
            sp['dead'] = True
            k1 = ease((t - BOLT8_HIT) / 0.35)              # knocked back to the wall
            k2 = ease((t - BOLT8_HIT - 0.35) / 0.55)       # and slides down it to sit
            p['pos'] = (2.75, 6.1 + 0.3 * k1)              # its head stops at the wall (was 8 cm into it)
            p['head_pitch'] = -28 * k1 + 10 * k2
            p['tilt'] = 14 * k2
            p['lean'] = -12 * k1 - 10 * k2
            p['y'] = -0.55 * k2
            fz, fy = 0.03 + 0.45 * k2, 0.08 + 0.55 * k2
            p['footR'] = (0.16, fy, fz)
            p['footL'] = (-0.18, fy, fz - 0.06)
            p['handR'] = (0.33, 0.96 - 0.04 * k2, 0.08 + 0.3 * k2)     # the hands fall into its lap
            p['handL'] = (-0.33, 0.96 - 0.06 * k2, 0.06 + 0.26 * k2)
            p['sweep'] = 0.0
        return p, sp
    if name == 'B':                                   # shot 9: in from the left (the wide opening), a lunge at Andy
        # Sam's note 28 (25 Oct): it swipes at him before it goes down, and stays wholly in frame: it rushes in from
        # the opening, winds up, swipes the blade across where he stood as he sidesteps, takes three rounds, drops
        if t < LUNGE9 - 0.35:
            return None, sp
        stop = (2.05, 2.9)
        if t < LUNGE9 + 0.35:
            p = R.pose(**R.walk(t, (-0.4, 2.9), stop, LUNGE9 - 0.35, LUNGE9 + 0.35, stride=0.7))
        else:
            p = R.pose(pos=stop, yaw=90.0)
        p['sweep'] = R.eye_sweep(t)
        p['lean'] = 18.0 * ease((t - LUNGE9) / 0.3)
        wind, cut, thru = LUNGE9 + 0.15, LUNGE9 + 0.3, LUNGE9 + 0.5
        up, across, done = (0.55, 1.95, -0.15), (0.05, 1.5, 0.75), (-0.5, 1.25, 0.45)
        if t < wind:
            p['handR'] = lerp3((0.33, 0.96, 0.08), up, ease((t - LUNGE9 + 0.35) / 0.5))
        elif t < cut:
            p['handR'] = lerp3(up, across, ease((t - wind) / (cut - wind)))
        else:
            p['handR'] = lerp3(across, done, ease((t - cut) / (thru - cut)))
        for i, ts in enumerate(SHOTS9):
            sp['holes'].append(dict(part='chest', i=40 + 37 * i, t=ts + 0.04))
            if 0 <= t - ts < 0.15:                    # each round knocks it back a little
                p['lean'] -= 9 * (1 - (t - ts) / 0.15)
        if t >= SHOTS9[-1] + 0.1:
            sp['dead'] = True
            k2 = ease((t - SHOTS9[-1] - 0.1) / 0.7)   # its knees go and it crumples forward towards Andy, in frame,
            p['y'] = -0.6 * k2                        # clear of the sofa, the table and every later path
            p['footR'] = (0.13, 0.08 + 0.6 * k2, 0.03 - 0.45 * k2)
            p['footL'] = (-0.13, 0.08 + 0.6 * k2, 0.03 - 0.4 * k2)
            p['head_pitch'] = 30 * k2
            p['handR'] = (0.05, 0.8, 0.25)           # its hand clear of the coffee table (the walls audit)
            p['fall'] = (30 * k2, 100)
        return p, sp
    if name in ('C', 'D'):                            # shot 10: outside the kitchen window; shot through the glass
        # Sam's note 29 (25 Oct): they just appeared. Now each walks in along the outside wall from behind the window's
        # edge (C from the south, D from the north), turns to the glass, and is cut down there, falling back outside
        z = 2.45 if name == 'C' else 3.4              # both in the part of the window the camera sees
        z0 = 0.6 if name == 'C' else 5.2
        t0, t1 = (44.2, 45.0) if name == 'C' else (44.35, 45.1)
        if t < t0 - 0.05:
            return None, sp
        if t < t1:
            p = R.pose(**R.walk(t, (-6.3, z0), (-6.3, z), t0, t1, stride=0.5, phase=0.5 if name == 'D' else 0.0))
        else:
            p = R.pose(pos=(-6.3, z), yaw=180 if name == 'C' else 0)
            p['yaw'] = (p['yaw'] + (90 - p['yaw']) * ease((t - t1) / 0.15)) if name == 'C' else \
                (0 + 90 * ease((t - t1) / 0.15))
        p['sweep'] = R.eye_sweep(t, 0.3 if name == 'D' else 0.0)
        if name == 'D' and t >= t1:                   # its cannon up at Wes for the shot
            a_, pole = R.aim((WES10[0], 1.7, WES10[1] + 0.35), p['pos'], p['yaw'], 'L', height=1.62)
            p['handL'], p['poleL'] = a_, pole
        die = FIRE10 + (0.3 if name == 'C' else 0.9)
        for k in range(4):                            # rounds striking it: holes and a jolt each
            ts = FIRE10 + (0.05 if name == 'C' else 0.55) + 0.08 * k
            sp['holes'].append(dict(part='chest', i=50 + 23 * k + (name == 'D'), t=ts))
            if 0 <= t - ts < 0.1:
                p['lean'] = p.get('lean', 0.0) - 8 * (1 - (t - ts) / 0.1)
        if t >= die:
            sp['dead'] = True
            k = ease((t - die) / 0.6)
            p['fall'] = (88 * k, 270)
        return p, sp
    if name == '5' and shot_of(t) == 's11':           # shot 11: walks into the hall-to-kitchen door; the tin dents it
        p = R.pose(**R.walk(t, (-1.2, 6.3), (-1.2, 5.9), 48.0, 49.4, stride=0.4))
        p['yaw'] = 180.0
        p['sweep'] = R.eye_sweep(t)
        if t >= DENT11:                               # knocked back, its eye dipping; then it rights itself (the hold)
            k = math.sin(math.pi * min(1.0, (t - DENT11) / 0.7))
            p['lean'] = p.get('lean', 0.0) - 14 * k
            p['head_pitch'] = 22 * k
            if DENT11 + 0.75 <= t < 50.75:            # it looks down at the dent in its chest...
                p['head_pitch'] = 34.0
            p['sweep'] = 0.0 if t < 50.75 else R.eye_sweep(t)   # ...and snaps back up, searching
        dent5(sp, t)
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
        dent5(sp, t)
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
        p['fall'] = (88 * k, {'4': 0.0, '3': 110.0}.get(name, (p['yaw'] + 180) % 360))   # 3: clear of robot 2 (audit)
        p['head_pitch'] = -15 * k
    return p, sp


PLASMA10_PATH = plasma10()
SCORCH10 = dict(t=PLASMA10 + math.dist(*PLASMA10_PATH) / PLASMA_SPEED, at=PLASMA10_PATH[1], n=(-1.0, 0.0, 0.0), kind='scorch', size=0.16, seed=10,
                room='kitchen')
DENT5_I = 0
TIN_HIT = _tin_hit()


def _dent5_i():
    p, _ = robot_pose('5', DENT11)
    ps, J = R.parts(p, dict(SPEC['5']))
    ch = next(q for q in ps if q.name == 'chest')
    return int(np.argmin(np.linalg.norm(ch.pts - np.asarray(TIN_HIT), axis=1)))


DENT5_I = _dent5_i()


def _frags9():
    out = []
    for i, s_ in enumerate(SHOTS9):                     # chrome chips knocked off robot B's chest, each its own
        JB, _ = R.skeleton(robot_pose('B', s_ + 0.04)[0])
        out.append(X.burst(s_ + 0.03, tuple(JB['chest']), 5, 1.8, 130 + i, col=(200, 206, 216), size=0.03, up=1.0,
                           dirn=(-1.0, 0.0, 0.0), box=(0.05, 5.95, 0.05, 5.35), tops=[]))
    return out


FRAGS9 = _frags9()


ROBOTS_IN = {'s8': ['A'], 's9': ['A', 'B'], 's10': ['C', 'D'], 's11': ['5', 'C', 'D'],
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
# Sam's note 47 (25 Oct): Wes backed through the living-room door's frame and no check said so: the audit only knew
# the kitchen units. The living-room furniture and every wall now count, each wall cut into pieces round its doors,
# windows and the wide opening (below a sill and above a head the wall is solid), 10 cm thick
for name in ('sofa', 'coffee table', 'drinks cabinet', 'armchair', 'side table', 'media unit', 'stool 1', 'stool 2'):
    th = PL.THINGS[name]
    (cx, cz), (sx, sz, sy) = th['at'], th['size']
    if th.get('facing', 0) % 180 == 90:
        sx, sz = sz, sx
    SOLID_BOXES.append((name, (cx - sx / 2, 0.0, cz - sz / 2), (cx + sx / 2, sy, cz + sz / 2)))


# The walls a round can strike: (axis, value, normal (0: either side), extent along it, the openings in it)
WALLS = [(0, -5.6, 1, (0.0, 5.4), ['kitchen window']), (0, 0.0, 0, (0.0, 5.4), ['wide opening']),
         (0, 6.0, -1, (0.0, 5.4), ['living window']), (2, 0.0, 1, (-5.6, 6.0), []),
         (2, 5.4, -1, (-5.6, 6.0), ['kitchen door', 'living door'])]


WALL_H, WALL_T = 2.6, 0.05


def _wall_boxes():
    out = []
    for ax, v, _, (a, b), names in WALLS + [(2, 7.0, -1, (-5.6, 6.0), []), (0, 6.0, 0, (5.4, 7.0), ['front door'])]:
        ops = sorted(([PL.OPENINGS[n_] for n_ in names if n_ in PL.OPENINGS]), key=lambda o: o['span'][0])
        cuts = [(a, b, 0.0, WALL_H)]                    # (from, to, low, high) along the wall
        for o in ops:
            s0, s1 = o['span']
            nxt = []
            for c0, c1, y0, y1 in cuts:
                if c1 <= s0 or c0 >= s1 or y0 > 0.0:
                    nxt.append((c0, c1, y0, y1))
                    continue
                if c0 < s0:
                    nxt.append((c0, s0, y0, y1))
                if c1 > s1:
                    nxt.append((s1, c1, y0, y1))
                if o['sill'] > 0:
                    nxt.append((max(c0, s0), min(c1, s1), 0.0, o['sill']))
                nxt.append((max(c0, s0), min(c1, s1), o['head'], WALL_H))
            cuts = nxt
        for c0, c1, y0, y1 in cuts:
            if ax == 0:
                lo, hi = (v - WALL_T, y0, c0), (v + WALL_T, y1, c1)
            else:
                lo, hi = (c0, y0, v - WALL_T), (c1, y1, v + WALL_T)
            out.append((f"wall {'x' if ax == 0 else 'z'}={v} {c0:.2f}-{c1:.2f}", lo, hi))
    return out


WALL_BOXES = _wall_boxes()


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
    elif s == 's8':
        sp, j = andy_sofa(t, 's7')                   # still on the sofa as the camera rises past (it dropped him)
        hf = 180.0 + 95.0 * ease((u - 0.15) / 0.4)   # his head turns over his right shoulder to the door
        x, z = PL.PEOPLE['andy sofa (1-4, 7, start of 8)']['at']
        out.append(dict(at=(x, z), r=0.25, draw=lambda im: put(im, cam, sp, x, z, 180, j, t, head_facing=hf)))
        wsp, wj, wx, wz, wfac, whf = wes8(t)
        out.append(dict(at=(wx, wz), r=0.3, draw=lambda im: masked(im, cam, fx, (wx, wz), lambda l: put(
            l, cam, wsp, wx, wz, wfac, wj, t, head_facing=whf))))
    elif s == 's9':
        asp, aj, ax9, az9, afac, ahf, arec = andy9(t)
        out.append(dict(at=(ax9, az9), r=0.3, draw=lambda im: fx.__setitem__('andy', (masked(im, cam, fx, (ax9, az9), lambda l: put(
            l, cam, asp, ax9, az9, afac, aj, t, head_facing=ahf)), arec))))
        wsp, wj, wx, wz, wfac, whf = wes9(t)
        out.append(dict(at=(wx, wz), r=0.3, draw=lambda im: masked(im, cam, fx, (wx, wz), lambda l: put(
            l, cam, wsp, wx, wz, wfac, wj, t, head_facing=whf))))
        if t >= FLING9[0]:
            (bx, by, bz), byaw = xbow9_at(t)
            out.append(dict(at=(bx, bz), r=0.2, draw=lambda im: X.crossbow3(im, cam, (bx, by, bz), byaw)))
    elif s == 's10':
        wsp, wj, wx, wz, wfac, whf, wrec = wes10(t)
        out.append(dict(at=(wx, wz), r=0.3, draw=lambda im: fx.__setitem__('wes', (masked(im, cam, fx, (wx, wz), lambda l: put(
            l, cam, wsp, wx, wz, wfac, wj, t, head_facing=whf)), wrec))))
    elif s == 's11':                                 # Wes at the window, still firing (seen as the camera follows the tin)
        wsp, wj, wx, wz, wfac, whf, wrec = wes10(t)
        out.append(dict(at=(wx, wz), r=0.3, draw=lambda im: fx.__setitem__('wes', (masked(im, cam, fx, (wx, wz), lambda l: put(
            l, cam, wsp, wx, wz, wfac, wj, t, head_facing=whf)), wrec))))
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
    if s in ('s9', 's10', 's11', 's12') and t >= FLING9[1]:      # things left where they fell (they stay)
        (bx, _, bz), byaw = xbow9_at(t)
        out.append(dict(at=(bx, bz), r=0.2, draw=lambda im: X.crossbow3(im, cam, (bx, 0.0, bz), byaw)))
    if s in ('s10', 's11', 's12') and t >= DROP10:
        (mx_, mz_), myaw = MACHETE10
        k = min(1.0, (t - DROP10) / 0.3)
        out.append(dict(at=(mx_, mz_), r=0.2, draw=lambda im: X.machete_floor(
            im, cam, (mx_, 0.75 * (1 - k * k), mz_), myaw + 60 * (1 - k), tilt=0.5 * (1 - k))))
    if s in ('s11', 's12') and t >= DENT11:
        tp = tin11_at(t)
        out.append(dict(at=(tp[0], tp[2]), r=0.05, draw=lambda im: X.tin(im, cam, tp, dent=1.0)))
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
    st['on'] = {'sink run': lambda im, cam: X.dish_rack(im, cam, smashed=smashed),
                'coffee table': lambda im, cam: X.coffee(im, cam, COFFEE, t)}
    if t >= SCORCH10['t'] and s not in ('s5', 's6'):
        st['marks'] = [SCORCH10]
    if s == 's12':
        _prepare12()
        st['marks'] = [SCORCH10] + [m for m in MARKS if m['t'] <= t]
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
    if s == 's9':                                         # brief row 34: the blade's arc, the rounds, sparks, fragments
        D = Behind(img, cam, fx.get('masks', []))
        tip, d = bolt8_stuck(t)                              # robot A in the hall, the bolt still in its head
        X.bolt(D(tip), cam, tip, d)
        k = int((t - BOLT8_HIT - 0.4) / 0.6)
        X.sparks(D(tip), cam, t, BOLT8_HIT + 0.4 + 0.6 * k, tip, 90 + k, n=6, col='blue', speed=1.2)
        cut, thru = LUNGE9 + 0.3, LUNGE9 + 0.5
        if cut - 0.08 <= t < thru + 0.15:
            tips = [blade_tip('B', cut - 0.08 + (min(t, thru) - cut + 0.08) * q / 7) for q in range(8)]
            JB, _ = R.skeleton(robot_pose('B', t)[0])
            X.blade_arc(D(JB['chest']), cam, [q for q in tips if q is not None][-6:])
        an = fx.get('andy')
        for i, s_ in enumerate(SHOTS9):
            if not 0 <= t - s_ < 0.6:
                continue
            JB, _ = R.skeleton(robot_pose('B', s_ + 0.04)[0])
            g = tuple(JB['chest'] + np.array([0.0, 0.05 * (i - 1), 0.0]))
            if t - s_ < 1 / FPS and an and an[1].get('muzzle') and cam.depth(g) > 0.2:
                (hx, hy), _ = cam.project(g)
                mx, my = an[1]['muzzle']
                B.Pen(img, FLAT).line([(mx + (hx - mx) * 0.25, my + (hy - my) * 0.25),
                                       (mx + (hx - mx) * 0.8, my + (hy - my) * 0.8)], (255, 236, 150), 2.4)
            if t - s_ < 1 / FPS:
                X.flash(D(g), cam, g, 0.07, seed=120 + i)
            X.sparks(D(g), cam, t, s_ + 0.03, g, 121 + i, n=12, col='yellow', speed=2.4)
            for pc in FRAGS9[i]:
                X.draw_piece(D(pc.at(t)[0]), cam, pc, t)
        for i, s_ in enumerate(SHOTS9):                      # the fragments stay where they land
            if t - s_ >= 0.6:
                for pc in FRAGS9[i]:
                    X.draw_piece(D(pc.at(t)[0]), cam, pc, t)
        D.finish()
    if s == 's8' and t >= BOLT8:
        D = Behind(img, cam, fx.get('masks', []))
        if t < BOLT8_HIT:                                   # the bolt in flight (from just behind the lens)
            b, d = bolt8_at(t)
            X.bolt(D(b), cam, b, d)
        else:
            tip, d = bolt8_stuck(t)
            X.bolt(D(tip), cam, tip, d)
            X.sparks(D(tip), cam, t, BOLT8_HIT, tip, 81, n=16, col='yellow', speed=2.2)
            # Sam's note 46 (25 Oct): the blue sparks were barely noticeable: more of them, thicker, living longer
            X.sparks(D(tip), cam, t, BOLT8_HIT + 0.05, tip, 82, n=16, col='blue', speed=2.0, life=0.45)
            if t < BOLT8_HIT + 1 / FPS:
                X.flash(D(tip), cam, tip, 0.07, seed=83)
            X.smoke(D(tip), cam, t, BOLT8_HIT + 0.1, tip, 84, n=3, life=1.2, size=0.06)
            k = int((t - BOLT8_HIT - 0.4) / 0.6)            # then small blue bursts every 0.6 s, the head shorting out
            if k >= 0:
                t0 = BOLT8_HIT + 0.4 + 0.6 * k
                X.sparks(D(tip), cam, t, t0, tip, 90 + k, n=11, col='blue', speed=1.6, life=0.4)
                if t - t0 < 1 / FPS:
                    X.flash(D(tip), cam, tip, 0.05, seed=95 + k, col='blue')
        D.finish()
    if s == 's10':
        D = Behind(img, cam, fx.get('masks', []))
        o, hp = PLASMA10_PATH                              # robot D's plasma: over his shoulder, past the lens
        L_ = math.dist(o, hp) / PLASMA_SPEED
        if PLASMA10 <= t < PLASMA10 + L_:
            k = (t - PLASMA10) / L_
            a, b = lerp3(o, hp, max(0.0, k - 0.6 / (L_ * PLASMA_SPEED))), lerp3(o, hp, k)
            if cam.depth(b) > 0.25:
                X.plasma(D(b), cam, a, b)
            elif cam.depth(a) > 0.25:
                X.plasma(D(a), cam, a, lerp3(a, b, 0.5))
        if t >= FIRE10:
            f = int(t * FPS)
            X.room_flash(img, 1.0 if f % 2 == 0 else 0.45)
            we = fx.get('wes')
            rng = np.random.default_rng(f)
            if we and we[1].get('muzzle'):                 # tracers out through the window at the robots
                mx, my = we[1]['muzzle']
                if f % 2 == 0:                             # a big lumpy muzzle flash every other frame (note 36)
                    C.muzzle_flash(B.Pen(img, FLAT), (mx, my), (-0.97, 0.12), 48, seed=f)
                w = PL.OPENINGS['kitchen window']
                for k in range(3):
                    tgt = (-6.3, rng.uniform(1.0, 2.3), rng.uniform(w['span'][0] + 0.2, w['span'][1] - 0.2))
                    if cam.depth(tgt) > 0.2:
                        (hx, hy), _ = cam.project(tgt)
                        a0 = rng.uniform(0.2, 0.6)
                        B.Pen(img, FLAT).line([(mx + (hx - mx) * a0, my + (hy - my) * a0),
                                               (mx + (hx - mx) * (a0 + 0.3), my + (hy - my) * (a0 + 0.3))], (255, 236, 150), 2.6)
            for name in ('C', 'D'):                        # sparks off the robots as the rounds strike
                pr, spr = robot_pose(name, t)
                if pr is None:
                    continue
                J, _ = R.skeleton(pr)
                for h in spr['holes']:
                    if 0 <= t - h['t'] < 0.4:
                        X.sparks(D(J['chest']), cam, t, h['t'], tuple(J['chest']), h['i'], n=8, col='yellow', speed=2.2)
                        if t - h['t'] < 1 / FPS:
                            X.flash(D(J['chest']), cam, tuple(J['chest']), 0.08, seed=h['i'])
            for pc in GLASS10:
                X.draw_piece(D(pc.at(t)[0]), cam, pc, t)
            for pc in CASES10:
                X.draw_piece(D(pc.at(t)[0]), cam, pc, t)
        D.finish()
    if s == 's11':
        f = int(t * FPS)
        X.room_flash(img, 1.0 if f % 2 == 0 else 0.45)  # Wes still firing
        D = Behind(img, cam, fx.get('masks', []))
        if THROW11 <= t < DENT11:
            tp = tin11_at(t)
            X.tin(D(tp), cam, tp)
        if DENT11 <= t < DENT11 + 0.45:
            X.sparks(D(TIN_HIT), cam, t, DENT11, TIN_HIT, 111, n=8, col='yellow', speed=1.6)
        D.finish()
        andy_arm11(img, cam, t)
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
    """Andy's own caption look (Cry Minister): TikTok Sans Bold, white, a soft dark shadow, centred on the screen (Sam's
    note 40: it sat at 470 px and read as drifting left; 640 px wide at most, it stays clear of the side buttons)."""
    SS = img.width // 1080
    f = ImageFont.truetype(CAP_FONT, 74 * SS)
    while f.getlength(s) > 640 * SS:
        f = ImageFont.truetype(CAP_FONT, int(f.size * 0.92))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((540 * SS, (y + 4) * SS), s, font=f, fill=(0, 0, 0, 200), anchor='mm')
    lay = lay.filter(ImageFilter.GaussianBlur(6 * SS))
    d = ImageDraw.Draw(lay)
    d.text((540 * SS, y * SS), s, font=f, fill=(255, 255, 255, 255), anchor='mm', stroke_width=max(1, SS),
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
          ('door-kicked-open', DOOR8, 0.9), ('robot-scan', TURN8, 0.5), ('crossbow', BOLT8 - 0.05, 0.9),
          ('arrow-woosh', BOLT8 - 0.02, 0.8), ('sparks', BOLT8 + 0.1, 0.6), ('robot-wounded', BOLT8 + 0.15, 0.7),
          ('laser-sword', LUNGE9 + 0.3, 0.6)] + [('pistol', s_, 0.8) for s_ in SHOTS9] + \
         [('robot-wounded', SHOTS9[-1] + 0.1, 0.6), ('glass-shattered', FIRE10, 0.9), ('plasma-gun', PLASMA10, 0.7),
          ('minigun', FIRE10, 0.9), ('minigun', T['s11'], 0.9), ('minigun', T['s12'], 0.9), ('minigun', T['s12'] + 2.4, 0.9), ('minigun', T['s12'] + 4.8, 0.9)]
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
    ev += [('robot-step', ts, 0.45) for ts in steps(ROBOT8, TURN8, (3.9, 6.1), (2.75, 6.1), 0.48)]
    ev += [('robot-step', ts, 0.4) for ts in steps(48.0, 49.4, (-1.2, 6.3), (-1.2, 5.9), 0.4)]       # robot 5 (11)
    ev += [('robot-step', ts, 0.5) for ts in steps(LUNGE9 - 0.35, LUNGE9 + 0.35, (-0.4, 2.9), (2.05, 2.95), 0.7)]
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
            for name, lo, hi in WALL_BOXES:
                rec.add('WALL', [CC.box('WALL', name, lo, hi)])
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
    """Shot 11: the tin's flight from Andy's hand (south of the island, above his head as he throws) over the island to
    robot 5's chest in the hall-to-kitchen door; then it bounces off, down onto the floor, and stays."""
    a = (-3.0, 1.8, 2.2)
    b = TIN_HIT
    if t <= DENT11:
        k = min(1.0, max(0.0, (t - THROW11) / (DENT11 - THROW11)))
        p = lerp3(a, b, k)
        return (p[0], p[1] + 0.45 * math.sin(math.pi * k), p[2])
    k = min(1.0, (t - DENT11) / (LAND11 - DENT11))
    c = (TIN_REST[0], 0.0, TIN_REST[1])
    p = lerp3(b, c, k)
    return (p[0], max(0.0, p[1] + 0.35 * math.sin(math.pi * k)), p[2])


if __name__ == '__main__':
    main()
