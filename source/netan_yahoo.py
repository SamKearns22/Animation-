#!/usr/bin/env python3
"""NETAN-YAHOO! (TikTok satire; brief prompts/netan-yahoo.md, notes notes/netan-yahoo.md). An Israeli prime
ministerial debate: the presenter introduces the moderate incumbent, Netanyahu, and Darth Maul; asked about the West
Bank, Maul ignites his saberstaff, flips across the studio, cuts the presenter into four steaming pieces and takes his
chair. Netanyahu: "S***, he's good." Built from source/satire_template.py; the studio is the built 3D set
(newsdesk_set.py), every shot a camera on it; the plan in metres is netan_yahoo_plan.py.

    python3 source/netan_yahoo.py cast OUT.jpg               the cast sheet (new looks, eyes, Maul's action poses)
    python3 source/netan_yahoo.py faces OUT.jpg              Netanyahu's surprised and impressed faces, strength 1-6
    python3 source/netan_yahoo.py stills OUT_DIR T [T ...]   stills at these times (seconds)
    python3 source/netan_yahoo.py check                      the plan checks and the audit
    python3 source/netan_yahoo.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import newsdesk_set as NS        # noqa: E402
import newsdesk_props as NP      # noqa: E402
import newsdesk_cast as NC       # noqa: E402  (the presenter's head and torso hooks)
import netanyahu_cast as NN      # noqa: E402
import maul_cast as MC           # noqa: E402
import netan_yahoo_plan as PLN   # noqa: E402
import figure as F               # noqa: E402
import mouths                    # noqa: E402
import mossad_audio as MA        # noqa: E402
import peepee as PP              # noqa: E402
import filmkit                   # noqa: E402
import film_engine as E          # noqa: E402
import views as V                # noqa: E402
import moves                     # noqa: E402
import sets as S                 # noqa: E402
import prepper_fx as X           # noqa: E402
import audit as A                # noqa: E402
import lying as LY               # noqa: E402  3D bodies on the floor (the pile)
import clipcheck as CC           # noqa: E402
from ed import INK               # noqa: E402

FPS, SR = 12, MA.SR
M = V.M_PER_UNIT
FLAT = NS.FLAT

# =============================================== STORY ==============================================================
NAME = 'netan-yahoo'
HOOK = ('Israeli Prime Ministerial Debate \U0001F605', {'y': 540, 'x': 225, 'w': 330, 'until': 3.95})
# Sam, 26 Oct: beside the presenter in shot 1 (screen left: the open dark wall, clear of him as the camera pushes in),
# with the sweat-smile emoji; until the first cut
NS.SCREEN_CAPTION = ('עימות לראשות הממשלה', '2026')      # answer 14: 'Debate for the Premiership 2026' (my Hebrew)
NS.SCREEN_CAPTION_BOX = (-2.45, -0.75, 1.5)               # big, across the screen (over its white bar)
# Each line: its recording (source/audio/), where its speech starts in the film (`at`), and its subtitles as
# (time in the recording, chunk): two to five words, each up on its first word; the punchline on its own.
# Chunk times: from the recording's phrases (voices.py) and its syllables, estimated within each phrase.
HOLD = 1.85                      # Sam, 26 Oct: the silence after line 4 held a few beats longer (all after it moves on)
CLOSE = (21.9, 23.9)             # ...with a close-up of Maul's face, staring, in it (then back to the wide for the attack)
LINES = [
    dict(n=1, who='PRESENTER', audio='netan-yahoo-1', at=0.35,
         text="It's time to introduce the candidates for tonight's debate.",           # Sam's wording, 26 Oct
         chunks=[(1.04, "It's time to introduce"), (2.24, 'the candidates'), (3.04, "for tonight's debate.")]),
    dict(n=2, who='PRESENTER', audio='netan-yahoo-2', at=4.2,
         text='Liberal, moderate, gently-gently, incumbent Prime Minister Benjamin Netanyahu.',   # Sam, 26 Oct
         chunks=[(1.01, 'Liberal, moderate,'), (2.55, 'gently-gently, incumbent'), (4.29, 'Prime Minister'),
                 (5.45, 'Benjamin Netanyahu.')]),
    dict(n=3, who='PRESENTER', audio='netan-yahoo-3', at=10.85,
         text='And Sith Lord and Scourge of the Galaxy, Darth Maul.',
         chunks=[(3.43, 'And Sith Lord'), (4.66, 'and Scourge of the Galaxy,'), (6.34, 'Darth Maul.')]),
    dict(n=4, who='PRESENTER', audio='netan-yahoo-4', at=15.1,
         text="Let's start with you, Maul. What would be your approach to the West Bank if you were elected?",
         chunks=[(0.85, "Let's start with you, Maul."), (2.88, 'What would be your approach'),
                 (4.36, 'to the West Bank if you were elected?')]),   # 4.36: measured on the recording
    dict(n=5, who='NETANYAHU', audio='netan-yahoo-5', at=28.6 + HOLD, text="S***, he's good.",
         chunks=[(0.98, "S***, he's good.")], bleep=(1.17, 1.37)),   # answer 13: the S heard, the rest bleeped
]
# the action (seconds; shot 4's action plan: ignition sound leads the jump, answer 6)
IGNITE = 22.3 + HOLD             # both blades light (the sound's real start)
TAKEOFF = 22.62 + HOLD           # he springs
LAND = 23.36 + HOLD              # the crouch landing (thump)
S1, S2, S3 = 23.78 + HOLD, 24.08 + HOLD, 24.38 + HOLD   # the three strikes: shoulder to hip, the other arm, the thighs
FALL = S3 + 0.04                 # the pieces part and fall
SPRING = 25.35 + HOLD            # onto the chair
ON_CHAIR = 25.82 + HOLD
FLICK = (21.05, 21.45)           # the presenter's eyes to the camera and back (brief)
NOD = 9.35                       # Netanyahu's nod on his name ("Netanyahu", line 2)
T = dict(s1=0.0, s2=3.95, s3=10.6, s4=14.85, s4c=CLOSE[0], s4b=CLOSE[1], s5=28.25 + HOLD, end=31.4 + HOLD)
SHOTS = [('s1', T['s1'], T['s2']), ('s2', T['s2'], T['s3']), ('s3', T['s3'], T['s4']), ('s4', T['s4'], T['s4c']),
         ('s4c', T['s4c'], T['s4b']), ('s4b', T['s4b'], T['s5']), ('s5', T['s5'], T['end'])]
WIDE = ('s4', 's4b')             # the wide shot, both halves (the close-up of Maul's stare between them)
DUR = T['end'] + 0.2
BLACK_AT = T['end']
PLAN = 'netan_yahoo_plan'                        # rule 1: the world in metres
P_AT, M_AT, N_AT = PLN.P, PLN.M, PLN.N
CHAIR_P = PLN.chair_of(P_AT)
LAND_AT = (P_AT[0] + 0.85 * (M_AT[0] - P_AT[0]) / math.dist(M_AT, P_AT),
           P_AT[1] + 0.85 * (M_AT[1] - P_AT[1]) / math.dist(M_AT, P_AT))   # 0.85 m from the presenter, Maul's side
HEIGHTS = {'PRESENTER': 1.80, 'NETANYAHU': 1.70, 'MAUL': 1.75}
SPECS = {'PRESENTER': dict(NC.PRESENTER, name='PRESENTER'),     # Sam (26 Oct): the bearded one, as built
         'NETANYAHU': dict(NN.NETANYAHU_RED, name='NETANYAHU'),
         'MAUL': dict(MC.MAUL_HOOD, name='MAUL')}
SHOT_CAST = {'s1': ['PRESENTER'], 's2': ['NETANYAHU'], 's3': ['MAUL'], 's4': ['PRESENTER', 'NETANYAHU', 'MAUL'],
             's4c': ['MAUL'], 's4b': ['PRESENTER', 'NETANYAHU', 'MAUL'],
             's5': ['NETANYAHU']}
REACT = {'s4': 1, 's5': 4}       # Netanyahu's strength (answer 12: shot 4 mild; Sam, 26 Oct: 4 on both shot 5 faces)
KEEP_CLEAR = []        # filled below once the cameras are known (the presenter's head and body in shot 1)


def _box_of(t, x, z, dx, y0, y1):
    if shot_of(t) != 's1':
        return None
    c = cam_for(t)
    pts = [c.project((x + sx, y, z))[0] for sx in (-dx, dx) for y in (y0, y1)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))
PROP_SIZES = [('saberstaff blade', 'saber blade', MC.BLADE_M, 0.04, None),
              ('armchair', 'wooden armchair', 2 * PLN.CHAIR_R, NP.RAIL_TOP, None)]
OUTFIT = {}
ALLOWED_CONTACTS = [
    ('MAUL.*', 'PRESENTER*', S1 - 0.1, FALL + 0.1, 'the strikes land (brief)'),
    ('MAUL.*', 'CHAIR_PRESENTER', ON_CHAIR - 0.1, None, 'he crouches on the seat, a hand on the armrest (brief)'),
    ('PIECE*', 'PIECE*', FALL, None, 'the pieces fall into one pile (brief)'),
    ('PIECE*', 'CHAIR_PRESENTER', FALL, None, 'the pile lies against his chair legs'),
]
ALLOWED_POPS = [('PRESENTER', FALL - 0.05, FALL + 0.1, 'cut into four pieces: PIECE 1-4 take his place'),
                ('PIECE*', FALL - 0.05, FALL + 0.15, 'the four pieces of the presenter, where he stood, as he comes apart')]
SET_EXCLUDE = []
TOUCHES, FREE_MOVES = [], [('PIECE*', FALL, None, 'cut free: they fall under gravity and stay')]
SOUND_SOURCES = {}
EFFECTS = []                    # filled below (rule 15: each drawn alone on the cast sheet)
JOKE_PROPS = []
BENCHMARK = [dict(place='studio', refs=['../newsdesk/set-1-wide-desk.jpg', 'debate-layout.jpg'], at=T['s4'] + 1.0,
                  items=[('glossy black floor', 'done (newsdesk_set)'),
                         ('round floor graphic', 'done; the three stand round it (Sam\'s sketch)'),
                         ('huge curved ring desk, open to the cameras', 'done, drawn in pieces (nearer on top)'),
                         ('tall blue screen with a caption', 'done: the debate caption in Hebrew, big'),
                         ('navy back wall, white ticks', 'done'), ('white pillars, red light edges', 'done'),
                         ('newsroom through glass', 'done'), ('lighting grid', 'done'),
                         ('debate: three standing in a shallow line, chairs behind (pack 3, Sam)', 'done: horseshoe'),
                         ('no set dressing (Sam: real sets are clean)', 'done')])]
# ====================================================================================================================


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def shot_start(t):
    return next((s[1] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][1])


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def lerp3(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


# ------------------------------------------------------------------------------------------------ the voices
for ln in LINES:                                     # cut each recording in the silence before its first word
    v = np.asarray(MA.line(ln['audio']), float).copy()
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
    TRACK.setdefault(ln['who'], []).extend((a + ln['start'], b + ln['start'], sh)
                                           for a, b, sh in mouths.track(ln['text'], ln['_stretches']))
for w in SPECS:
    TRACK.setdefault(w, [])
SPOKEN_END = max(b for a, b, sh in TRACK['NETANYAHU'] if a > T['s5'])   # his last mouth shape on 'good'
BLINKS = {'PRESENTER': F.blinks(3, 0.5, DUR, talking=True), 'NETANYAHU': F.blinks(5, 0.5, DUR),
          'MAUL': [b for b in F.blinks(7, 0.5, DUR) if not (T['s3'] - 0.3 < b < IGNITE + 0.3)]}   # his stare: unblinking
BLINKS['NETANYAHU'] = [b for b in BLINKS['NETANYAHU'] if not (T['s5'] - 0.2 < b < T['end'])]   # no blink on the punchline


def talking(who, t):
    return mouths.at(TRACK[who], t) not in (None, 'rest')


# ------------------------------------------------------------------------------------------------ the cameras
def cam_for(t):
    s, u = shot_of(t), t - shot_start(t)
    C = PLN.CAMS
    if s == 's1':                                    # zooming in across the studio: mid-large to mid-close
        k = ease(u / (T['s2'] - T['s1']))
        a, b = C['s1 start'], C['s1 end']
        return S.Cam(a['pos'], lerp3(a['look'], b['look'], k), focal=a['focal'] + (b['focal'] - a['focal']) * k)
    if s in ('s2', 's5'):
        c = C['s2']
        return S.Cam(c['pos'], c['look'], focal=c['focal'])
    if s == 's3':
        c = C['s3']
        return S.Cam(c['pos'], c['look'], focal=c['focal'])
    if s == 's4c':                                   # the close-up: his face, dead still; the faintest push in
        a, b = C['s4 close'], C['s4 close end']
        k = ease(u / (T['s4b'] - T['s4c']))
        return S.Cam(a['pos'], lerp3(a['look'], b['look'], k), focal=a['focal'] + (b['focal'] - a['focal']) * k)
    a, b = C['s4'], C['s4 push']                     # shot 4: all three; pushes in as Maul ignites
    k = ease((t - IGNITE) / (ON_CHAIR - IGNITE))
    return S.Cam(a['pos'], lerp3(a['look'], b['look'], k), focal=a['focal'] + (b['focal'] - a['focal']) * k)


def facing_cam(cam, x, z):
    return math.degrees(math.atan2(cam.pos[0] - x, cam.pos[2] - z))


def look_towards(cam, me, other, h=1.6):
    """The burnham 'look' (-1 .. 1, + = screen right) for eyes pointing from `me` to `other` (plan points)."""
    (xa, _), _ = cam.project((me[0], h, me[1]))
    (xb, _), _ = cam.project((other[0], h, other[1]))
    return max(-1.0, min(1.0, (xb - xa) / 260.0))


# ------------------------------------------------------------------------------------------------ placing people
def put(img, cam, sp, x, z, facing, j, t, lift=0.0, head_yaw=None):
    """Someone at floor point (x, z) facing `facing` (plan degrees), `lift` metres up, through the camera: their
    height sets their scale. Returns the drawing frame (screen neck point, scale, yaw, 2D joints)."""
    h = HEIGHTS.get(sp.get('name'), 1.75)
    f = h / 1.75
    neck = 928 * M * f + lift
    if cam.depth((x, neck, z)) < 0.3:
        return None
    (Xn, Yn), k = cam.project((x, neck, z))
    (Xf, Yf), _ = cam.project((x, lift, z))
    s = max(1e-3, (Yf - Yn) / 928.0)
    fd = (math.sin(math.radians(facing)), math.cos(math.radians(facing)))
    yaw = cam.yaw_of((x, 0, z), fd)
    j2 = V.person(img, FLAT, Xf, Yf - 928 * s, s, dict(sp, full=True, pose='custom'), t, yaw, j, head_yaw)
    view, mirror = V.snap(yaw)
    return dict(X=Xf, Y=Yf - 928 * s, s=s, yaw=yaw, j2=j2, mirror=mirror, k=k)


def in_frame(cam, x, z, h=1.6, margin=200):
    if cam.depth((x, h, z)) < 0.3:
        return False
    (X_, Y_), k = cam.project((x, h, z))
    return -margin - 0.4 * k < X_ < 1080 + margin + 0.4 * k


# ------------------------------------------------------------------------------------------------ the presenter
KEEP_CLEAR += [('his head', lambda t: _box_of(t, P_AT[0], P_AT[1], 0.13, 1.5, 1.88)),
               ('his body', lambda t: _box_of(t, P_AT[0], P_AT[1], 0.3, 0.0, 1.5))]


def presenter(t, cam):
    """Upright, quick head moves (answer 2); eyes to the camera in shot 1, then to whoever he addresses; the flick
    to the camera after the question; alarm, hands up, the arch as each strike lands (pack 2, ref 4)."""
    sp = dict(SPECS['PRESENTER'])
    j = V.standing(sp)
    j['lean'] = -2.0                                  # more upright
    s = shot_of(t)
    shape = mouths.at(TRACK['PRESENTER'], t)
    sp['mouth'] = 'set' if shape in (None, 'rest') else 'v:' + shape
    sp['blink'] = F.blinking(t, BLINKS['PRESENTER'])
    sp['tilt'] = filmkit.shifts(t, seed=11, amount=0.06, hold=(0.8, 1.4), move=0.14)   # quicker head moves
    sp['breath'] = F.breath(t, 3.6, 1.5, 0.2)
    if s == 's1':
        sp['look'] = 0.0
    else:
        target = N_AT if t < LINES[2]['start'] - 0.3 else M_AT
        sp['look'] = look_towards(cam, P_AT, target)
        if FLICK[0] <= t < FLICK[1]:
            sp['look'] = 0.0                          # the eyes snap to the camera and back (jumps, not eased)
    if t >= IGNITE + 0.12:                           # sees it coming (Poker Mon note 37): alarm, then hands up
        sp['mood'] = 'alarm'
        sp['look'] = look_towards(cam, P_AT, maul_xz(t))
        u = ease((t - (TAKEOFF + 0.05)) / 0.35)
        sw = sp.get('shoulders', 152)
        if u > 0:
            for side, sg in (('R', 1), ('L', -1)):
                a = (sg * (sw + 24), 466.0, 44.0)
                b = (sg * (sw - 30), -40.0, 210.0)
                V.arm_to(j, side, lerp3(a, b, u), 'down', 'palm')
            j['lean'] = -2.0 - 6.0 * u                # backing off
        for sk in (S1, S2, S3):                       # each blow: the back arches, head thrown back, arms jerk up
            w = max(0.0, 1.0 - abs(t - (sk + 0.05)) / 0.12)
            if w > 0:
                j['lean'] = j['lean'] - 14.0 * w
                sp['gaze_dy'] = -4.0 * w
    return sp, j


# ------------------------------------------------------------------------------------------------ Netanyahu
def netanyahu(t, cam):
    sp = dict(SPECS['NETANYAHU'])
    j = V.standing(sp)
    s = shot_of(t)
    shape = mouths.at(TRACK['NETANYAHU'], t)
    sp['mouth'] = 'set' if shape in (None, 'rest') else 'v:' + shape
    sp['blink'] = F.blinking(t, BLINKS['NETANYAHU'])
    sp['tilt'] = filmkit.shifts(t, seed=21, amount=0.04)
    sp['breath'] = F.breath(t, 4.4, 1.2, 0.6)
    j['lean'] = 2.0 * filmkit.shifts(t, seed=23, amount=1.0)   # a small weight shift now and then (never a sway)
    sp['look'] = look_towards(cam, N_AT, P_AT)
    w = max(0.0, 1.0 - abs(t - NOD) / 0.3)           # the respectful nod on his name: head down and back up
    sp['down'] = 0.9 * ease(w)
    j['head_dy'] = 10.0 * ease(w)
    if t >= IGNITE + 0.25:                           # eyes on Maul from the ignition on
        sp['look'] = look_towards(cam, N_AT, maul_xz(t))
    if s in WIDE and t >= IGNITE + 0.25:             # shot 4: mild surprise from the ignition: brows up, a small
        sp['mood'], sp['react'] = 'surprised', REACT['s4']   # lean back (more as Maul lands), no step
        j['lean'] += -4.0 * ease((t - IGNITE - 0.25) / 0.4) - 3.0 * ease((t - LAND) / 0.3)
    if s == 's5':                                    # surprised on the line, then settles into the impressed look
        sp['mood'], sp['react'] = 'surprised', REACT['s5']
        if t > SPOKEN_END:                           # Sam, 26 Oct: the mouth shut as 'good' ends, not a second on
            sp['mood'] = 'impressed'
    return sp, j


# ------------------------------------------------------------------------------------------------ Maul
def _flight(t0, t1, a, b, apex, base_a=0.0, base_b=0.0):
    """A jump's arc: (x, z, lift) at time t from a to b, `apex` metres above the straight line."""
    def at(t):
        u = min(1.0, max(0.0, (t - t0) / (t1 - t0)))
        x = a[0] + (b[0] - a[0]) * u
        z = a[1] + (b[1] - a[1]) * u
        return x, z, base_a + (base_b - base_a) * u + 4 * apex * u * (1 - u)
    return at


LEAP = _flight(TAKEOFF, LAND, M_AT, LAND_AT, 1.0)
HOP = _flight(SPRING, ON_CHAIR, LAND_AT, CHAIR_P[:2], 0.75, 0.0, NP.SEAT_H)


def maul_xz(t):
    if t < TAKEOFF:
        return M_AT
    if t < LAND:
        return LEAP(t)[:2]
    if t < SPRING:
        return LAND_AT
    if t < ON_CHAIR:
        return HOP(t)[:2]
    return CHAIR_P[:2]


def _pose_ready(sp, lit):
    """Pack 1, maul-10: after ignition: feet very wide, knees bent, saber hand raised back with the blade up, the free
    arm flung out sideways, fingers spread."""
    sw = sp.get('shoulders', 150)
    j = V.standing(sp)
    d = 70.0
    j['bob'] = d
    j['footR'] = (175.0, V.ANKLE_Y - d, 30.0)
    j['footL'] = (-185.0, V.ANKLE_Y - d, -30.0)
    V.arm_to(j, 'R', (sw + 40, -60.0, 20.0), 'out', 'fist')
    V.arm_to(j, 'L', (-(sw + 260), 110.0, 30.0), 'down', 'palm')
    j['props'] = [MC.saberstaff('R', (0.15, -1.0, -0.1), lit)]
    j['grip'] = {'R'}
    return j


def _pose_tuck(sp):
    """Pack 1, maul-9/11: the top of the leap: knees tucked high, staff upright in one hand, free hand up and out."""
    sw = sp.get('shoulders', 150)
    j = V.standing(sp)
    j['footR'] = (55.0, 600.0, 230.0)
    j['footL'] = (-55.0, 640.0, 200.0)
    j['lean'] = 22.0
    V.arm_to(j, 'R', (sw - 10, 330.0, 160.0), 'out', 'fist')
    V.arm_to(j, 'L', (-(sw + 150), -80.0, 90.0), 'down', 'palm')
    j['props'] = [MC.saberstaff('R', (0.0, -1.0, 0.1))]
    j['grip'] = {'R'}
    return j


def _pose_crouch(sp, hand_floor=True, low=320.0):
    """Pack 1, maul-7: the predatory crouch: the back knee near the floor, the front foot planted, the free hand's
    fingertips on the floor in front, head low and eyes up, the staff held out to the side, both blades lit."""
    sw = sp.get('shoulders', 150)
    j = V.standing(sp)
    j['bob'] = low
    j['footR'] = (95.0, V.ANKLE_Y - low, 170.0)
    j['footL'] = (-110.0, V.ANKLE_Y - low, -210.0)
    j['lean'] = 28.0
    if hand_floor:
        V.arm_to(j, 'L', (-50.0, V.ANKLE_Y - low - 40.0, 270.0), 'out', 'palm')
    V.arm_to(j, 'R', (sw + 170, 260.0, 30.0), 'down', 'fist')
    j['props'] = [MC.saberstaff('R', (0.97, 0.12, 0.2))]
    j['grip'] = {'R'}
    return j


# the strikes, as (saber hand target in his own units, the staff's aim, his bob, lean, front foot z): windup ->
# contact -> follow-through (pack 1, maul-8: the deep lunge, the staff diagonal behind, looking back)
STRIKES = [
    ((140.0, -150.0, 60.0), (0.55, -0.8, -0.2), 40.0, -4.0,    # 1: shoulder to hip, from high on his right
     (-30.0, 360.0, 250.0), (-0.65, 0.7, 0.2), 150.0, 20.0),
    ((-120.0, 40.0, 140.0), (-0.9, -0.35, 0.1), 90.0, 6.0,     # 2: the other arm, back across from his left
     (230.0, 160.0, 230.0), (0.95, -0.15, 0.2), 120.0, 14.0),
    ((240.0, 330.0, -40.0), (0.9, 0.25, -0.3), 160.0, 18.0,    # 3: low, across the thighs
     (-170.0, 420.0, 260.0), (-0.95, 0.15, 0.25), 190.0, 24.0),
]


def _pose_strike(sp, hand, aim, bob, lean):
    sw = sp.get('shoulders', 150)
    j = V.standing(sp)
    j['bob'] = bob
    j['footR'] = (110.0, V.ANKLE_Y - bob, 200.0)
    j['footL'] = (-120.0, V.ANKLE_Y - bob, -230.0)
    j['lean'] = lean
    V.arm_to(j, 'R', hand, 'out', 'fist')
    V.arm_to(j, 'L', (-(sw + 200), 160.0, 120.0), 'down', 'palm')   # the free hand out, open (maul-8)
    j['props'] = [MC.saberstaff('R', aim)]
    j['grip'] = {'R'}
    return j


def _pose_chair(sp, snap):
    """Answer 11: crouched on the seat, weight forward, one hand on the armrest, both blades lit and held low across
    him, ready: body still; the head snaps from look to look."""
    j = _pose_crouch(sp, hand_floor=False, low=300.0)
    sw = sp.get('shoulders', 150)
    j['footR'] = (110.0, V.ANKLE_Y - 300.0, 90.0)
    j['footL'] = (-110.0, V.ANKLE_Y - 300.0, -60.0)
    j['lean'] = 20.0
    V.arm_to(j, 'L', (-(sw + 120), 520.0, 40.0), 'out', 'palm')   # on the armrest
    V.arm_to(j, 'R', (60.0, 430.0, 200.0), 'down', 'fist')
    j['props'] = [MC.saberstaff('R', (0.97, 0.1, 0.22))]
    return j


SNAPS = [(ON_CHAIR, -0.85, -0.5), (ON_CHAIR + 0.75, 0.9, 0.55), (ON_CHAIR + 1.35, -0.2, -0.1), (ON_CHAIR + 1.9, 0.95, 0.6)]


def _towards(a, b, k):
    """Plan heading a turned the fraction k of the way to heading b (the short way round)."""
    d = (b - a + 180.0) % 360.0 - 180.0
    return a + d * k


def _maul_look(cam, me, other):
    """Maul's glance towards `other`. Sam, 26 Oct: in the wide shot it went the wrong way: his face is drawn mirrored
    there (checked at the eyes: look -0.65 put the pupils on the right), so the wide shot's glance is turned round and
    held short of the corner (at the full -1 the pupil slides out of the eye and only the yellow shows)."""
    k = look_towards(cam, me, other)
    if cam.pos[0] < me[0] and cam.pos[2] < me[1] and abs(cam.pos[0] - me[0]) > 1.0:    # the wide camera (to his left, far)
        return -max(-0.75, min(0.75, k))
    return k


def maul(t, cam):
    """Maul's spec, pose, where he is and how he is turned: (sp, j, x, z, lift, facing, roll)."""
    sp = dict(SPECS['MAUL'])
    sp['blink'] = F.blinking(t, BLINKS['MAUL'])
    sp['mood'] = 'neutral'                            # the glare
    x, z = M_AT
    lift, roll = 0.0, 0.0
    to_p = math.degrees(math.atan2(P_AT[0] - x, P_AT[1] - z))
    facing = facing_cam(cam, x, z)
    if t < IGNITE:                                    # still, staring at the presenter; staff unlit at his side
        j = MC.pose('stand', sp)
        j['props'] = [MC.saberstaff('R', (0.5, 1.0, 0.45), (False, False))]
        sp['look'] = _maul_look(cam, M_AT, P_AT)
        sp['tilt'] = 0.0                              # the stare is the joke: dead still (listed in the audit)
        return sp, j, x, z, lift, facing, roll
    sp['mood'] = 'snarl'
    if t < TAKEOFF:                                   # ignites: the ready stance, both blades lit
        j = _pose_ready(sp, (True, True))
        sp['look'] = _maul_look(cam, M_AT, P_AT)
        return sp, j, x, z, lift, facing, roll
    if t < LAND:                                      # the leap-flip: up and over, the hood falls back in the roll
        x, z, lift = LEAP(t)
        u = (t - TAKEOFF) / (LAND - TAKEOFF)
        if u > 0.45:
            sp = dict(MC.MAUL, name='MAUL', mood='snarl', blink=False)
        j = _pose_tuck(sp) if 0.12 < u < 0.88 else _pose_ready(sp, (True, True))
        facing = to_p                                 # side on, travelling towards the presenter
        roll = 360.0 * ease(min(1.0, max(0.0, (u - 0.08) / 0.84)))
        lift = max(0.0, lift)
        return sp, j, x, z, lift, facing, roll
    sp = dict(MC.MAUL, name='MAUL', mood='snarl', blink=sp['blink'])
    x, z = LAND_AT
    to_p = math.degrees(math.atan2(P_AT[0] - x, P_AT[1] - z))
    facing = to_p - 40.0                              # three-quarter: towards the presenter, open to the camera
    sp['look'] = _maul_look(cam, LAND_AT, P_AT)
    if t < S1 - 0.14:                                 # the landing crouch, then rising into the first wind-up
        k = ease((t - (S1 - 0.3)) / 0.16)
        a = _pose_crouch(sp)
        if k <= 0:
            return sp, a, x, z, lift, facing, roll
        h, aim, bob, lean = STRIKES[0][:4]
        b = _pose_strike(sp, h, aim, bob, lean)
        return sp, moves.mix_poses(a, b, k), x, z, lift, facing, roll
    if t < SPRING - 0.2:                              # the three strikes: wind-up, contact, follow-through
        for i, sk in enumerate((S1, S2, S3)):
            h0, aim0, bob0, lean0, h1, aim1, bob1, lean1 = STRIKES[i]
            if t < sk + 0.14 or i == 2:
                u = (t - (sk - 0.14)) / 0.28             # fast into the hit, easing out (pace 'fast' in, 'slow' out)
                if u < 0.5:
                    w = moves.fast_in(u * 2) * 0.5
                else:
                    w = 0.5 + ease((u - 0.5) * 2) * 0.5
                w = min(1.0, max(0.0, w))
                hand = lerp3(h0, h1, w)
                aim = lerp3(aim0, aim1, w)
                j = _pose_strike(sp, hand, aim, bob0 + (bob1 - bob0) * w, lean0 + (lean1 - lean0) * w)
                if i < 2 and t >= sk + 0.14 - 1e-6:
                    continue
                if i == 2 and t > sk + 0.14:         # held follow-through, then gathering for the spring
                    k = ease((t - (SPRING - 0.45)) / 0.25)
                    end = _pose_strike(sp, h1, aim1, bob1, lean1)
                    j = moves.mix_poses(end, _pose_crouch(sp, hand_floor=False, low=200.0), k)
                return sp, j, x, z, lift, facing, roll
    if t < ON_CHAIR:                                  # springs over the pile onto the chair
        x, z, lift = HOP(t)
        u = (t - SPRING) / (ON_CHAIR - SPRING)
        j = _pose_tuck(sp) if 0.15 < u < 0.85 else _pose_crouch(sp, hand_floor=False, low=200.0)
        j['props'] = [MC.saberstaff('R', (0.95, -0.2, 0.1))]
        facing = math.degrees(math.atan2(CHAIR_P[0] - LAND_AT[0], CHAIR_P[1] - LAND_AT[1]))
        return sp, j, x, z, lift, facing, roll
    x, z = CHAIR_P[:2]                                # on the seat: still body, the head snapping round
    lift = NP.SEAT_H
    facing = facing_cam(cam, x, z) - 55.0             # three-quarter, so the crouch reads (front on, the robe hides it)
    look, turn = SNAPS[0][1:]
    for ts, lk, tn in SNAPS:
        if t >= ts:
            look, turn = lk, tn
    sp['look'], sp['turn'] = look, turn
    return sp, _pose_chair(sp, turn), x, z, lift, facing, roll


# ------------------------------------------------------------------------------------------------ the cut and the pieces
# Strikes 1-3 leave glowing cut lines on him (drawn on the flat figure while he stands). As the last lands he comes
# apart into four pieces (answer 8): head and shoulder, torso, arm, legs. Sam (26 Oct, note 4): the pieces are 3D
# bodies on the floor (lying.py, the same logic as anyone lying down), each falls under gravity, turns and slumps
# fully to the floor, the pile a little further from the chair. Cut faces scorched black, rims orange, cooling; no blood.
CUTS = [((-260.0, 330.0), (120.0, -60.0)), ((150.0, -40.0), (150.0, 520.0)), ((-300.0, 610.0), (300.0, 610.0))]
SCORCH = (34, 26, 24)
GLOW_HOT, GLOW_COOL = (255, 186, 70), (150, 62, 30)
G = 9.8
_away = np.subtract(P_AT, CHAIR_P[:2])
_away = _away / np.linalg.norm(_away)
PILE_AT = (P_AT[0] + 0.02, P_AT[1] - 0.38)       # Sam: a little further from the chair (towards us, clear of Maul)
# each piece: its parts, how it turns as it goes down (axis, degrees), where it ends up from the pile's centre
PIECES = {
    'PIECE 1': dict(name='head and shoulder', parts=('neck', 'head', 'hair', 'ear', 'shoulderL', 'armL', 'forearmL', 'handL'),
                    axis=(0.25, 0.0, 1.0), deg=100.0, to=(-0.5, -0.12), spin=40.0),
    'PIECE 2': dict(name='torso', parts=('chest', 'belly', 'shoulderR', 'pelvis', 'thighupL', 'thighupR'),
                    axis=(0.0, 0.0, 1.0), deg=82.0, to=(-0.06, 0.34), spin=-15.0),
    'PIECE 3': dict(name='arm', parts=('armR', 'forearmR', 'handR'), axis=(1.0, 0.0, 0.2), deg=88.0,
                    to=(0.22, -0.3), spin=60.0),
    'PIECE 4': dict(name='legs', parts=('thighloL', 'thighloR', 'shinL', 'shinR', 'shoeL', 'shoeR'),
                    axis=(1.0, 0.0, 0.0), deg=-86.0, to=(0.05, -0.08), spin=10.0),
}
_BODY = {}


def _cut_pose():
    """His pose as the last blow lands (frozen for the pieces)."""
    cam0 = cam_for(S3)
    return presenter(S3 + 0.05, cam0)


def cut_body():
    """The presenter's 3D body as cut: {piece: [lying.Part]} standing where he stood, and his spec."""
    if 'pieces' not in _BODY:
        sp, j = _cut_pose()
        fd = facing_cam(cam_for(S3), *P_AT)
        k = LY.from_views(j, sp, P_AT[0], P_AT[1], (math.sin(math.radians(fd)), math.cos(math.radians(fd))))
        prts = []
        for q in LY.parts(k, sp):
            if q.name.startswith('thigh'):
                prts.extend(LY.split_part(q, 0.45))       # strike 3: across the thighs
            else:
                prts.append(q)
        diag = (k['neck'] + k['shL']) / 2 + (k['shR'] - k['shL']) * 0.0
        for q in prts:                                    # the scorched faces of the other two cuts
            if q.name in ('neck', 'shoulderL', 'chest', 'armL'):
                q.scorch.append((diag, 0.12))              # strike 1: shoulder to hip
            if q.name in ('shoulderR', 'armR', 'chest'):
                q.scorch.append((k['shR'].copy(), 0.075))  # strike 2: the other arm
        out = {}
        for name, pc in PIECES.items():
            want = set(pc['parts'])
            out[name] = [q for q in prts if q.name in want or (q.name == 'ear' and 'ear' in want)]
        _BODY['pieces'], _BODY['sp'] = out, dict(sp)
    return _BODY['pieces'], _BODY['sp']


def _centre(prts):
    return np.mean([q.a for q in prts] + [q.b for q in prts], axis=0)


def _mass(q):
    """A part's rough volume (its weight in the piece's centre of mass)."""
    if q.kind == LY.ROUND:
        return (q.ra + q.rb) ** 2 * (np.linalg.norm(q.b - q.a) + q.ra + q.rb)
    return float(np.prod(q.radii))


def _com(prts):
    w = np.array([_mass(q) for q in prts])
    c = np.array([(q.a + q.b) / 2 for q in prts])
    return (c * w[:, None]).sum(0) / w.sum()


def _blobs(prts):
    """Balls along each part (centre, radius): for keeping the pieces out of each other."""
    out = []
    for q in prts:
        if q.kind == LY.ROUND:
            n = max(2, int(np.linalg.norm(q.b - q.a) / 0.05) + 1)
            for u in np.linspace(0, 1, n):
                out.append((q.a + (q.b - q.a) * u, q.ra + (q.rb - q.ra) * u))
        else:
            out.append((q.a, float(np.mean(q.radii))))
    return out


_REST = {}


def _rest():
    """Sam's notes 4 and 11: each piece settles as a real thing would, lying on its broadest side (its weight as
    low as it goes: no balancing on one point), resting on the floor, not on or inside another piece; the head
    lies with the neck's cut end turned away from the camera (it read as an eye). {piece: (R, (dx, dz))}."""
    if _REST:
        return _REST
    pcs, _ = cut_body()
    to_cam = np.array(PLN.CAMS['s4']['pos']) - np.array([PILE_AT[0], 0.0, PILE_AT[1]])
    to_cam[1] = 0.0
    to_cam /= np.linalg.norm(to_cam)
    placed = {}
    for name, pc in PIECES.items():
        prts = pcs[name]
        c0 = _com(prts)
        R0 = LY.rot((0, 1, 0), pc['spin']) @ LY.rot(pc['axis'], pc['deg'])
        stump = None                                     # the neck's open end: its end furthest from the head
        neck = next((q for q in prts if q.name == 'neck'), None)
        head = next((q for q in prts if q.name == 'head'), None)
        if neck is not None and head is not None:
            hc = (head.a + head.b) / 2
            stump = max((neck.a, neck.b), key=lambda e: np.linalg.norm(e - hc)) - hc   # the way the cut end faces
        best = None
        for ax in range(0, 360, 10):
            for az in range(-90, 91, 10):
                R = LY.rot((0, 0, 1), az) @ LY.rot((1, 0, 0), ax) @ R0
                turned = LY.moved(prts, R, c0, (0, 0, 0))
                h = _com(turned)[1] - (c0[1] + LY.lowest(turned) - c0[1])
                cost = h + 0.0004 * (abs(ax if ax <= 180 else 360 - ax) + abs(az))   # nearest the planned fall
                if stump is not None:                    # the neck's cut end away from us, or down
                    d = R @ stump
                    d = d / (np.linalg.norm(d) + 1e-9)
                    cost += 0.3 * max(0.0, d @ to_cam + 0.3)
                if best is None or cost < best[0]:
                    best = (cost, R)
        placed[name] = [best[1], np.array(pc['to'], float)]
    for _ in range(60):                                   # push apart any that lie in each other
        moved_any = False
        shapes = {}
        for name, (R, off) in placed.items():
            prts = pcs[name]
            c0 = _com(prts)
            t = LY.moved(prts, R, c0, (PILE_AT[0] + off[0] - c0[0], 0.0, PILE_AT[1] + off[1] - c0[2]))
            shapes[name] = _blobs(t)
        names = list(placed)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                worst = 0.0
                for pa, ra in shapes[names[i]]:
                    for pb, rb in shapes[names[j]]:
                        worst = max(worst, ra + rb + 0.01 - np.linalg.norm(pa - pb))
                if worst > 0:
                    ca = np.mean([p for p, _ in shapes[names[i]]], axis=0)
                    cb = np.mean([p for p, _ in shapes[names[j]]], axis=0)
                    d = np.array([ca[0] - cb[0], ca[2] - cb[2]])
                    d = d / (np.linalg.norm(d) + 1e-9) * min(0.03, worst / 2 + 0.005)
                    placed[names[i]][1] += d
                    placed[names[j]][1] -= d
                    moved_any = True
        if not moved_any:
            break
    _REST.update({n: (R, tuple(off)) for n, (R, off) in placed.items()})
    return _REST


def _axis_angle(R):
    ang = math.degrees(math.acos(max(-1.0, min(1.0, (np.trace(R) - 1) / 2))))
    if ang < 1e-3:
        return (0.0, 1.0, 0.0), 0.0
    v = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
    if np.linalg.norm(v) < 1e-6:                          # a half turn: the axis from R + I
        w, V_ = np.linalg.eigh((R + np.eye(3)) / 2)
        return tuple(V_[:, -1]), ang
    return tuple(v / np.linalg.norm(v)), ang


def piece_at(name, t):
    """The piece's parts at time t: turning as it falls under gravity, coming to rest settled on the floor."""
    pcs, _ = cut_body()
    prts = pcs[name]
    c0 = _com(prts)
    Rf, off = _rest()[name]
    tau = max(0.0, t - FALL)
    fall_t = math.sqrt(2 * max(0.2, c0[1]) / G)            # about how long it takes to come down
    u = min(1.0, tau / fall_t)
    axis, deg = _axis_angle(Rf)
    R = LY.rot(axis, deg * u * u)                           # the turn builds up as it falls
    tx = (PILE_AT[0] + off[0] - c0[0]) * (1 - (1 - u) ** 2)
    tz = (PILE_AT[1] + off[1] - c0[2]) * (1 - (1 - u) ** 2)
    turned = LY.moved(prts, R, c0, (tx, 0.0, tz))
    rest_y = -LY.lowest(turned)                             # the drop that rests it on the floor
    y = max(-0.5 * G * tau * tau, rest_y) if u < 1.0 else rest_y
    return LY.moved(turned, np.eye(3), c0, (0.0, y, 0.0))


def _pile_down():
    """When the last piece comes to rest (its fall from its height under gravity)."""
    pcs, _ = cut_body()
    return FALL + max(math.sqrt(2 * max(0.2, _centre(p)[1]) / G) for p in pcs.values())


PILE_DOWN = _pile_down()
_PILE_CACHE = {}


def draw_pile(img, cam, t):
    """The four pieces as one 3D drawing (lying.draw), with their contact shadow on the floor; drawn once and reused
    once everything has settled and the camera has stopped."""
    still = t >= max(PILE_DOWN, ON_CHAIR)
    key = (B.SS, img.size, cam.pos, cam.at, cam.focal, cam.shake, cam.roll)   # Sam's note 6: shot 4's copy was
    if still and key in _PILE_CACHE:                    # pasted into shot 5 (the key had no camera)
        img.alpha_composite(_PILE_CACHE[key])
        return
    _, sp = cut_body()
    prts = [q for name in PIECES for q in piece_at(name, t)]
    rim = tuple(int(x + (y - x) * min(1.0, max(0.0, (t - S3) / 1.0))) for x, y in zip(GLOW_HOT, GLOW_COOL))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    LY.shadow(lay, cam, None, sp, [((0.0, 0.0, 0.0), (0.0, 1.0, 0.0))], prts=prts, reach=0.03)   # Sam's note 11
    LY.draw(lay, cam, None, dict(sp, cut_rim=rim), prts=prts)
    if still:
        _PILE_CACHE[key] = lay
    img.alpha_composite(lay)
    for name in PIECES:
        PIECES[name]['_at'] = tuple(_centre(piece_at(name, t)))


def _person_layer(img, cam, sp, j, t):
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    fd = facing_cam(cam, *P_AT)
    fr = put(lay, cam, sp, P_AT[0], P_AT[1], fd, j, t)
    return lay, fr


def _to_screen(fr, u, v):
    m = -1 if fr['mirror'] else 1
    ss = B.SS
    return ((fr['X'] + m * u * fr['s']) * ss, (fr['Y'] + v * fr['s']) * ss)


def _draw_cuts(lay, fr, t, n):
    """The cut lines so far on him: a scorched black band, its rim bright orange at first, cooling to a thin line."""
    alpha = lay.getchannel('A')
    band = Image.new('RGBA', lay.size, (0, 0, 0, 0))
    db = ImageDraw.Draw(band)
    for i in range(n):
        sk = (S1, S2, S3)[i]
        cool = min(1.0, max(0.0, (t - sk) / 1.0))
        a, b = _to_screen(fr, *CUTS[i][0]), _to_screen(fr, *CUTS[i][1])
        w = max(4, int(0.035 / M * fr['s'] * B.SS))          # a scorched band 3.5 cm wide
        db.line([a, b], fill=SCORCH + (255,), width=w)
        col = tuple(int(x + (y - x) * cool) for x, y in zip(GLOW_HOT, GLOW_COOL))
        db.line([a, b], fill=col + (255,), width=max(2, int(w * (0.5 - 0.3 * cool))))
    band.putalpha(ImageChops.multiply(band.getchannel('A'), alpha))
    lay.alpha_composite(band)


def steam(img, cam, t):
    """Wisps of flat steam rising off the pile's cut faces (the mug steam, prepper_fx; answer 9)."""
    if t < PILE_DOWN + 0.2:
        return
    p = B.Pen(img, FLAT)
    for i, name in enumerate(PIECES):
        at = PIECES[name].get('_at')
        if at is None:
            continue
        top = (at[0], max(0.12, at[1]) + 0.06, at[2])
        fade0 = min(1.0, (t - PILE_DOWN - 0.2) / 0.4)
        for k in range(2):
            ph = t * 1.1 + k * 0.5 + i * 0.23
            u = ph % 1.0
            pts = []
            for q in range(7):
                v = q / 6
                y = top[1] + 0.02 + 0.32 * (u * 0.5 + v * 0.5)
                dx = 0.02 * math.sin(5.0 * v + ph * 3 + k + i) + (k - 0.5) * 0.05
                pts.append((top[0] + dx, y, top[2]))
            fade = math.sin(math.pi * u) * fade0
            if fade > 0.15 and all(cam.depth(q) > 0.3 for q in pts):
                cam.line(p, pts, (196, 202, 210), max(2.4, 0.012 * cam.project(top)[1] * fade))


# ------------------------------------------------------------------------------------------------ the saber's glow
BLADE_COLS = [MC.BLADE, MC.CORE]


def saber_glow(img, lay):
    """The soft glow round the blades only (answer 10: Sam's Poker Mon exception): the blade pixels, blurred, red."""
    a = np.asarray(lay)
    m = np.zeros(a.shape[:2], bool)
    for c in BLADE_COLS:
        m |= (np.abs(a[..., :3].astype(int) - np.array(c)).sum(axis=2) < 24) & (a[..., 3] > 200)
    if not m.any():
        return
    mask = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(
        ImageFilter.GaussianBlur(9 * B.SS))
    glow = Image.new('RGBA', img.size, (255, 60, 50, 0))
    glow.putalpha(mask.point(lambda v: int(v * 0.75)))
    img.alpha_composite(glow)


# ------------------------------------------------------------------------------------------------ the strikes' effects
def contact_point(i):
    """Where strike i lands on him (world), the middle of its cut line."""
    cam0 = cam_for(S3)
    f = HEIGHTS['PRESENTER'] / 1.75
    (a, b) = CUTS[i]
    u, v = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    if i == 2:
        u = 120.0                                     # the cut's near end, where the blade comes through
    fd = facing_cam(cam0, *P_AT)
    right = np.array((math.cos(math.radians(fd)), 0.0, -math.sin(math.radians(fd))))
    return tuple(np.array((P_AT[0], (928.0 - v) * M * f, P_AT[1])) + right * u * M * f + np.array((0, 0, -0.05)))


def effects(img, cam, t):
    for i, sk in enumerate((S1, S2, S3)):
        c = contact_point(i)
        X.sparks(img, cam, t, sk, c, seed=50 + i, n=10, speed=2.4, life=0.35)
        X.smoke(img, cam, t, sk + 0.03, c, seed=60 + i, n=2, life=0.9, size=0.045)


_TEST_CAM = S.Cam((0.0, 1.2, -1.2), (0.0, 1.2, 0.0), focal=1400)


def _test_sparks(im):
    X.sparks(im, _TEST_CAM, 0.12, 0.0, (0.0, 1.2, 0.0), seed=50, n=10, speed=2.4, life=0.35)


def _test_smoke(im):
    X.smoke(im, _TEST_CAM, 0.3, 0.0, (0.0, 1.2, 0.0), seed=60, n=2, life=0.9, size=0.045)


def _test_steam(im):
    old = {k: v.get('_at') for k, v in PIECES.items()}
    for k in PIECES:
        PIECES[k]['_at'] = (0.0, 0.9, 0.0)
    steam(im, _TEST_CAM, PILE_DOWN + 1.0)
    for k, v in old.items():
        PIECES[k]['_at'] = v


EFFECTS = [('sparks', 'sparks', _test_sparks), ('smoke', 'smoke', _test_smoke),
           ('steam', 'smoke', _test_steam)]   # no flare at the strikes (Sam, 26 Oct)


# ------------------------------------------------------------------------------------------------ the picture
def actors(t, cam):
    """Everyone and everything standing in the studio, as (x, z, draw) for the set's far-to-near sort."""
    out = []
    for who in ('presenter', 'maul', 'netanyahu'):
        p = {'presenter': P_AT, 'maul': M_AT, 'netanyahu': N_AT}[who]
        cx, cz, cf = PLN.chair_of(p)
        out.append((cx, cz, lambda im, c, cx=cx, cz=cz, cf=cf: NP.round_chair(im, c, cx, cz, cf)))
    # the presenter: whole, cut (glowing lines), or in pieces
    if t < S1:
        sp, j = presenter(t, cam)
        out.append((P_AT[0], P_AT[1], lambda im, c, sp=sp, j=j: put(im, c, sp, P_AT[0], P_AT[1],
                                                                    facing_cam(c, *P_AT), j, t)))
    elif t < FALL:
        sp, j = presenter(t, cam)
        n = sum(1 for sk in (S1, S2, S3) if t >= sk)

        def cut_one(im, c, sp=sp, j=j, n=n):
            lay, fr = _person_layer(im, c, sp, j, t)
            if fr is not None:
                _draw_cuts(lay, fr, t, n)
                im.alpha_composite(lay)
        out.append((P_AT[0], P_AT[1], cut_one))
    else:
        out.append((PILE_AT[0], PILE_AT[1], lambda im, c: draw_pile(im, c, t)))
    sp, j = netanyahu(t, cam)
    out.append((N_AT[0], N_AT[1], lambda im, c, sp=sp, j=j: put(im, c, sp, N_AT[0], N_AT[1], facing_cam(c, *N_AT), j, t)))
    msp, mj, mx, mz, ml, mf, mr = maul(t, cam)
    sort_z = mz - (0.3 if t >= ON_CHAIR - 0.1 else 0.0)   # on the chair: drawn after it

    def draw_maul(im, c, msp=msp, mj=mj, mx=mx, mz=mz, ml=ml, mf=mf, mr=mr):
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
        fr = put(lay, c, msp, mx, mz, mf, mj, t, lift=ml)
        if fr is None:
            return
        if abs(mr) > 0.5:                             # the flip: his drawing turned about his middle
            (Xc, Yc), _ = c.project((mx, ml + 0.85, mz))
            lay = lay.rotate(mr, resample=Image.BICUBIC, center=(Xc * B.SS, Yc * B.SS))
        saber_glow(im, lay)
        im.alpha_composite(lay)
    out.append((mx, sort_z, draw_maul))
    return out


def picture(t):
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    cam = cam_for(t)
    img = B.canvas((0, 0, 0))
    NS.render(img, cam, actors(t, cam))
    if shot_of(t) in WIDE:
        effects(img, cam, t)
        steam(img, cam, t)
    return img


# ------------------------------------------------------------------------------------------------ captions
SUBS = []
for ln in LINES:
    for i, (rt, txt) in enumerate(ln['chunks']):
        a = ln['start'] + (rt - ln['_cut']) + 0.1     # up on its first word (about 0.1 s after it starts)
        SUBS.append((a, txt))
SUBS.sort()


def caption_at(t):
    for i, (a, txt) in enumerate(SUBS):
        ln = next(l for l in LINES if any(c[1] == txt for c in l['chunks']))
        nxt = SUBS[i + 1][0] if i + 1 < len(SUBS) else 1e9
        end = min(nxt, ln['end'] + 0.3)
        if a <= t < end:
            return txt
    return None


def overlay(img, t):
    if t < BLACK_AT:
        c = caption_at(t)
        if c:
            PP.caption(img, c)
    return img


def frame_image(t):
    return overlay(picture(t), t)


# ------------------------------------------------------------------------------------------------ sound
SFX_DIR = os.path.join(HERE, 'audio', 'netan-yahoo-sfx')
SFX = {}


def sfx(name):
    if name not in SFX:
        SFX[name] = np.asarray(MA.load(os.path.join(SFX_DIR, name + '.mp3')), float)
    return SFX[name]


def _thump():
    """The landing thump (my addition, Sam approved): a short low knock."""
    n = int(0.22 * SR)
    tt = np.arange(n) / SR
    rng = np.random.default_rng(3)
    return (np.sin(2 * math.pi * 62 * tt) * 0.9 + rng.normal(0, 0.12, n)) * np.exp(-tt * 22)


def _creak():
    """The chair creak as he lands on it (my addition): a short squeak of rubbed wood, its pitch sagging."""
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    f0 = 520 - 260 * tt / tt[-1]
    ph = 2 * math.pi * np.cumsum(f0) / SR
    rough = 1 + 0.6 * np.sign(np.sin(2 * math.pi * 38 * tt))
    return 0.25 * np.sin(ph) * rough * np.sin(math.pi * tt / tt[-1]) ** 2


def _hiss(seconds=2.4):
    """The steam's hiss off the pile (my addition): soft, high, fading."""
    n = int(seconds * SR)
    rng = np.random.default_rng(9)
    x = rng.normal(0, 1, n)
    x = np.diff(np.concatenate(([0.0], x)))           # tilted up: a hiss, not a roar
    env = np.minimum(1, np.arange(n) / (0.3 * SR)) * np.linspace(1, 0, n) ** 1.5
    return 0.05 * x * env


def sound_events():
    """Sam's sounds, placed where they really start (filmkit.place); mine (thump, creak, hiss) made in code."""
    return [('saber-turn-on', IGNITE, 0.9), ('whoosh-2', TAKEOFF + 0.05, 0.7), (_thump(), LAND, 0.8),
            ('whoosh', S1 - 0.12, 0.6), ('strike-1', S1, 0.9),
            ('whoosh', S2 - 0.12, 0.6), ('strike-2', S2, 0.9),
            ('whoosh', S3 - 0.12, 0.6), ('strike-1', S3, 0.85),
            ('body-falling', FALL + 0.45, 0.9), (_hiss(), PILE_DOWN + 0.2, 0.6),
            ('whoosh-2', SPRING + 0.05, 0.6), (_creak(), ON_CHAIR + 0.02, 0.7)]


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)
    for ln in LINES:
        s_ = int(ln['start'] * SR)
        seg = ln['_voice'][:max(0, n - s_)]
        voice[s_:s_ + len(seg)] += seg
    for name, at, g in sound_events():
        try:
            clip = sfx(name) if isinstance(name, str) else name
        except Exception as e:                         # a sound Sam keeps off GitHub, missing in a new chat
            print(f'SOUND MISSING: {name} ({e}); re-attach it')
            continue
        filmkit.place(rest, clip * 0.35, at=at, sr=SR, gain=g)
    mix = voice + rest
    end = int(BLACK_AT * SR)
    mix, g = MA.master(mix, end)
    voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


# ------------------------------------------------------------------------------------------------ checks
def _rot_about(pts, c, axis, deg):
    """Points turned about the axis through c (Rodrigues)."""
    k = np.asarray(axis, float)
    k = k / np.linalg.norm(k)
    th = math.radians(deg)
    out = []
    for p in pts:
        v = np.asarray(p, float) - c
        out.append(c + v * math.cos(th) + np.cross(k, v) * math.sin(th) + k * np.dot(k, v) * (1 - math.cos(th)))
    return out


def scene(t, faces=None):
    """Everyone and everything solid at time t, as picture(t) puts them (audit.py, rule 5); `faces` also collects
    each face drawn (name, mouth, view, head height px) for voices.py (rule 7)."""
    cam = cam_for(t)
    things = []

    def add(name, sp, j, x, z, facing, lift=0.0, roll=0.0):
        if not in_frame(cam, x, z):
            return
        h = HEIGHTS.get(name, 1.75)
        fd = (math.sin(math.radians(facing)), math.cos(math.radians(facing)))
        sol = A.placed(name, j, x, z, fd, h, lift, 0.0, sp)
        if abs(roll) > 0.5:                           # the flip: turned about the camera's line of sight
            c = np.array((x, lift + 0.85, z))
            axis = np.subtract(cam.pos, c)
            axis[1] = 0.0
            for s_ in sol:
                s_.a, s_.b = _rot_about([s_.a, s_.b], c, axis, -roll)
        things.append(A.Thing(name, sol))
        if faces is not None:
            yaw = cam.yaw_of((x, 0, z), fd)
            (_, _), k = cam.project((x, h - 0.1, z))
            faces.append((name, sp.get('mouth'), yaw, 0.22 * k))
    if t < FALL:
        sp, j = presenter(t, cam)
        add('PRESENTER', sp, j, P_AT[0], P_AT[1], facing_cam(cam, *P_AT))
    else:
        for name in PIECES:
            sol = []
            for q in piece_at(name, t):
                r = max(q.ra, q.rb) if q.kind == LY.ROUND else float(max(q.radii))
                sol.append(CC.capsule(name, q.name, q.a, q.b, r) if q.kind == LY.ROUND else CC.sphere(name, q.name, q.a, r))
            things.append(A.Thing(name, sol))
    sp, j = netanyahu(t, cam)
    add('NETANYAHU', sp, j, N_AT[0], N_AT[1], facing_cam(cam, *N_AT))
    msp, mj, mx, mz, ml, mf, mr = maul(t, cam)
    msp['mouth'] = 'set'
    add('MAUL', msp, mj, mx, mz, mf, ml, mr)
    return things                                     # the desk and chairs: from PLAN (rule 12)


def mouths_seen(t):
    faces = []
    scene(t, faces)
    return faces


def checks():
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches']]
    faults = E.check_mouths(sorted(x for w in TRACK for x in TRACK[w]), windows)
    _, voice, rest = soundtrack(stems=True)
    faults += filmkit.voice_balance(voice, rest, SR, windows)
    mix, voice, rest = soundtrack(stems=True)
    faults += filmkit.hiss_check(mix, SR, BLACK_AT)
    for q in filmkit.sound_questions({'voice': voice, 'background': rest, 'mix': mix}, SR,
                                     cuts=[a for _, a, _ in SHOTS[1:]], end=BLACK_AT):
        print('QUESTION FOR SAM:', q)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


# the general audit (template): each person alone over every frame they are on screen
AUDIT_ALLOW = [   # (name, from, to, why): fast or still on purpose
    ('MAUL [s3]', T['s3'], T['s4'], 'the stare: dead still at the presenter, the joke (brief: "intensely and stilly")'),
    ('MAUL [s4]', T['s4'], T['s4c'], 'the stare and the silence before he ignites (brief)'),
    ('MAUL [s4c]', T['s4c'], T['s4b'], 'the close-up stare in the silence (Sam, 26 Oct): dead still'),
    ('MAUL [s4b]', T['s4b'], IGNITE, 'the stare, back in the wide, before he ignites'),
    ('MAUL [s4b]', IGNITE, ON_CHAIR + 0.1, 'the action: ignition, the leap-flip, the strikes, the spring (fast on purpose)'),
    ('PRESENTER [s4b]', S1 - 0.1, FALL + 0.1, 'struck: the arch on each blow, then cut apart'),
    ('NETANYAHU [s2]', NOD - 0.35, NOD + 0.35, 'the nod'),
]


def audits():
    """The general audit: each person alone over every frame they are on screen (in pieces, popping, stretching,
    frozen), and the eyelines. Returns faults."""
    def alone(who):
        def draw(t):
            cam = cam_for(t)
            lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
            if who == 'PRESENTER':
                if t < FALL:
                    sp, j = presenter(t, cam)
                    put(lay, cam, sp, P_AT[0], P_AT[1], facing_cam(cam, *P_AT), j, t)
            elif who == 'NETANYAHU':
                sp, j = netanyahu(t, cam)
                put(lay, cam, sp, N_AT[0], N_AT[1], facing_cam(cam, *N_AT), j, t)
            else:
                msp, mj, mx, mz, ml, mf, mr = maul(t, cam)
                fr = put(lay, cam, msp, mx, mz, mf, mj, t, lift=ml)
                if fr is not None and abs(mr) > 0.5:
                    (Xc, Yc), _ = cam.project((mx, ml + 0.85, mz))
                    lay = lay.rotate(mr, resample=Image.BICUBIC, center=(Xc * B.SS, Yc * B.SS))
            return lay
        return draw
    actors = {}
    where = {'PRESENTER': lambda t: P_AT, 'NETANYAHU': lambda t: N_AT, 'MAUL': maul_xz}
    for who in SPECS:
        for shot, a, b in SHOTS:
            ts = [i / FPS for i in range(int(math.ceil(a * FPS)), int(b * FPS))
                  if who in SHOT_CAST[shot] and in_frame(cam_for(i / FPS), *where[who](i / FPS))]
            if ts:
                actors[f'{who} [{shot}]'] = (ts, alone(who))
    return filmkit.silhouette_audit(actors, fps=FPS, allow=AUDIT_ALLOW)


# ------------------------------------------------------------------------------------------------ the cast sheet
def cast_sheet(out):
    """The new looks before anything moves: the younger presenter beside the built one; eyes turning (all three);
    Maul's action poses (ready, leap-flip, landing crouch, the three strikes, on the chair); the cut and the pieces;
    a 1.75 m person and a 1 m ruler for scale."""
    from PIL import ImageFont
    import sizes
    B.SS = 1
    W, H = 2700, 2700
    sh = Image.new('RGB', (W, H), (232, 228, 222))
    d = ImageDraw.Draw(sh)
    big = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 34)
    sm = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 24)

    def person_tile(sp, j, yaw=0.0, s=0.5, w=330, h=620, roll=0.0, lab='', head_crop=False):
        im = Image.new('RGBA', (1080, 1920), (246, 244, 238, 255))
        lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        V.person(lay, FLAT, 540, 700, s, dict(sp, full=True, pose='custom'), 0.0, yaw, j)
        if roll:
            lay = lay.rotate(roll, resample=Image.BICUBIC, center=(540, 700 + 420 * s))
        saber_glow(im, lay)
        im.alpha_composite(lay)
        if head_crop:                                 # the head and collar, large: the crop the tile's own shape
            half = 230 * s                                # (Sam, 26 Oct: a squeezed crop made everyone look thinner)
            cy = 700 - 90 * s
            box = (540 - half, cy - half * h / w, 540 + half, cy + half * h / w)
        else:                                         # the whole figure, whatever it does
            bb = lay.getbbox() or (0, 0, 1080, 1920)
            cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
            half = max(bb[2] - bb[0], (bb[3] - bb[1]) * w / h) / 2 + 20
            box = (cx - half, cy - half * h / w, cx + half, cy + half * h / w)
        tile = im.crop(tuple(int(v) for v in box)).convert('RGB').resize((w, h), Image.LANCZOS)
        return tile

    y = 20
    d.text((20, y), "The presenter (Sam, 26 Oct: the bearded one, as built); his three-quarter now from his own head",
           font=big, fill=(30, 30, 30))
    y += 50
    young = dict(NC.PRESENTER)
    x = 20
    for yaw in (0, 45):
        sh.paste(person_tile(young, V.standing(young), yaw, 0.55, 300, 560), (x, y))
        d.text((x + 10, y + 565), 'front' if yaw == 0 else 'three-quarter', font=sm, fill=(30, 30, 30))
        x += 320
    for yaw in (0, 45):
        sh.paste(person_tile(young, V.standing(young), yaw, 1.3, 300, 300, head_crop=True), (x, y + 120))
        d.text((x + 10, y + 425), 'front' if yaw == 0 else 'three-quarter', font=sm, fill=(30, 30, 30))
        x += 320
    y += 620
    d.text((20, y), 'Eyes turn, bodies face the camera (Sam, 26 Oct): look left / ahead / right', font=big,
           fill=(30, 30, 30))
    y += 50
    x = 20
    for sp in (young, dict(NN.NETANYAHU_RED), dict(MC.MAUL_HOOD)):
        for lk in (-0.9, 0.0, 0.9):
            sh.paste(person_tile(dict(sp, look=lk), V.standing(sp), 0, 1.3, 270, 270, head_crop=True), (x, y))
            x += 285
    y += 300
    d.text((20, y), "Maul's action (pack 1): ready, leap-flip (hood falls back), landing crouch, three strikes "
           "(wind-up and follow-through), on the chair", font=big, fill=(30, 30, 30))
    y += 50
    hood, bare = dict(MC.MAUL_HOOD, mood='snarl'), dict(MC.MAUL, mood='snarl')
    tiles = [(hood, _pose_ready(hood, (True, True)), 0, 0, 'ready (ignited)'),
             (hood, _pose_tuck(hood), -90, 90, 'flip, going over'),
             (bare, _pose_tuck(bare), -90, 250, 'flip, hood back'),
             (bare, _pose_crouch(bare), -60, 0, 'landing crouch')]
    for i in range(3):
        h0, a0, b0, l0, h1, a1, b1, l1 = STRIKES[i]
        tiles.append((bare, _pose_strike(bare, h0, a0, b0, l0), -55, 0, f'strike {i + 1}: wind-up'))
        tiles.append((bare, _pose_strike(bare, h1, a1, b1, l1), -55, 0, f'strike {i + 1}: through'))
    tiles.append((dict(bare, look=-0.85, turn=-0.5), _pose_chair(bare, -0.5), -55, 0, 'on the chair'))
    x = 20
    for k, (sp, j, yaw, roll, lab) in enumerate(tiles):
        if k == 6:
            x, y = 20, y + 500
        sh.paste(person_tile(sp, j, yaw, 0.5, 300, 440, roll), (x, y))
        d.text((x + 6, y + 445), lab, font=sm, fill=(30, 30, 30))
        x += 320
    y += 500
    d.text((20, y), 'The cut (answer 8-9): three cut lines, then four pieces in a pile; scorched faces, orange rims '
           'cooling; no blood', font=big, fill=(30, 30, 30))
    y += 50
    for k, tt in enumerate((S1 + 0.02, S3 + 0.02, FALL + 0.25, PILE_DOWN + 1.2)):
        cam = cam_for(tt)
        im = picture(tt)
        crop = im.crop((0, 500, 1080, 1700)).convert('RGB')
        crop.thumbnail((420, 470))
        sh.paste(crop, (20 + k * 440, y))
    sizes.scale_ref(d, W - 300, y + 420, 0.3 / M)
    sh.save(out, quality=88)
    return out


def LINE_SUBJECTS():
    def one(sp):
        def d(im):
            V.person(im, FLAT, 540, 420, 1.45, dict(sp, full=True, pose='custom'), 0.0, 0, V.standing(sp))
        return d
    return [('presenter', one(NC.PRESENTER))]


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        cast_sheet(a[1])
    elif a[0] == 'faces':
        NN.reaction_sheet(a[1])
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'check':
        B.SS = 1
        checks()
        f = [x[len('AUDIT: '):] for x in A.check(sys.modules[__name__])]
        print('\n'.join(['AUDIT: ' + x for x in f]) or 'audit: clean')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None)


F.guard(B)   # every arm drawn is measured against the rig; a wrong one stops the render
import limbs                     # noqa: E402
limbs.install(B)

if __name__ == '__main__':
    main()
