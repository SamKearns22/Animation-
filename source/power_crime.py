#!/usr/bin/env python3
"""Power Crime Action (TikTok satire; notes/power-crime-action.md). Trafalgar Square: a sitting, chanting protest; a
little old lady raises her placard (I OPPOSE / GENOCIDE / I SUPPORT ... the rest never seen); the senior officer's
jaw drops: "Shit. A code red." Armed police storm in from all sides and down ropes, carbines on her; two lift her by
the arms, carry her off and hurl her fifty feet head first into the back of a police van that speeds away, lights
flashing. The interrogation room: "Listen to me, you filth..." Jenkins at the door: "It's urgent." The corridor: a
mass casualty attack... "I don't have time to be dealing with your small fry problems, Jenkins."

Every place is built once in 3D (source/power_crime_set.py) and every shot is a camera on it; the people are the
satire package's (source/power_crime_cast.py), placed in metres and seen through the same camera.

    python3 source/power_crime.py cast OUT.jpg            the cast sheet
    python3 source/power_crime.py stills OUT_DIR T [T ...]
    python3 source/power_crime.py sheet OUT.jpg [T ...]   one still per shot (or at these times) on one sheet
    python3 source/power_crime.py check                   the plan checks and the audit
    python3 source/power_crime.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1]
"""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import power_crime_cast as C     # noqa: E402  (installs mouths, circle hands, the smooth limbs, the arm guard)
import power_crime_set as S3     # noqa: E402
import views as V                # noqa: E402
import moves                     # noqa: E402
import mouths                    # noqa: E402
import figure as F               # noqa: E402
import filmkit                   # noqa: E402
import mossad_audio as MA        # noqa: E402
import peepee as PP              # noqa: E402
import film_engine as E          # noqa: E402
from poker_mon_room import Cam3  # noqa: E402
from ed import INK                # noqa: E402

FPS, SR = 12, MA.SR
FLAT = B.Cam(1.0, 540, 960)
M = V.M_PER_UNIT

# =============================================== STORY =============================================================
NAME = 'power-crime-action'
HOOK = ('Met Police: Getting Priorities Right \U0001F694', {'y': 880})   # Sam, 20 Oct (finish.py adds it)
LINES = [   # (number, who, text, file, where the recording's start is placed)
    dict(n=1, who='CROWD', text='Free Palestine!', audio='power-crime-1', start=-0.35),
    dict(n=2, who='SUPER', text='Shit. A code red.', audio='power-crime-2', start=5.6),
    dict(n=3, who='SUPER', text="Listen to me, you filth. You're going to tell me everything. The location of your "
                                "cells. The nature of your resources. The aims of your organisation.",
         audio='power-crime-3', start=17.25),
    dict(n=4, who='JENKINS', text="Err, excuse me, sir. I need to speak to you outside. It's urgent.",
         audio='power-crime-4', start=29.3),
    dict(n=5, who='JENKINS', text="I'm sorry to interrupt, sir, but there's been a mass casualty attack in",
         audio='power-crime-5', start=34.1),
    dict(n=6, who='SUPER', text="I don't have time to be dealing with your small fry problems, Jenkins. Interrupt me "
                                "again and see what happens.", audio='power-crime-6', start=38.35),
]
# Subtitles (guides/satire.md): two to five words, each up on its first word; the punchline on its own. Each line's
# chunks are given phrase by phrase (the recording's own pauses), and spread over a phrase by syllables.
CHUNKS = {
    1: [['Free Palestine!'], ['Free Palestine!'], ['Free Palestine!'], ['Free Palestine!']],
    2: [['Sh*t.'], ['A code red.']],
    3: [['Listen to me, you filth.'], ["You're going to tell me", 'everything.'], ['The location of your cells.'],
        ['The nature of your resources.'], ['The aims of your organisation.']],
    4: [['Err, excuse me, sir.'], ['I need to speak', 'to you outside.'], ["It's urgent."]],
    5: [["I'm sorry to interrupt, sir,"], ["but there's been", 'a mass casualty', 'attack in—']],
    6: [["I don't have time", 'to be dealing with', 'your small fry problems,', 'Jenkins.'], ['Interrupt me again'],
        ['and see what happens.']],
}
SHOTS = [   # (name, start, end)
    ('wide', 0.0, 1.4),          # the square from the gallery's steps: the packed, chanting protest
    ('gran', 1.4, 4.2),          # pushing in on her: she raises her placard, trembling
    ('police', 4.2, 5.4),        # the police line by the lion: neutral, faintly sour
    ('super', 5.4, 8.7),         # close: his jaw drops (Sam: strength 3). "Shit. A code red."
    ('storm', 8.7, 11.6),        # mid shot on her: armed officers storm in, two down ropes; carbines on her; lifted
    ('throw', 11.6, 17.3),       # side on, tracking: carried off, swung, hurled flat into the van, which speeds off
    ('interro', 17.3, 21.0),     # the interrogation room, two-shot
    ('interro_s', 21.0, 25.8),   # close on him
    ('interro_g', 25.8, 28.6),   # close on her: trembling, unbothered
    ('door', 28.6, 34.0),        # the door opens: Jenkins
    ('corridor', 34.0, 48.4),    # outside: the mass casualty attack; the jab; small fry
]
DUR = 48.4
BLACK_AT = DUR
HORROR_LEVEL = 3                  # Sam, 20 Oct
DROP = 5.75                       # his jaw drops (a snap: eyes and jokes snap)

# Where things are in the square (metres; the column at the origin; north +z). Sam, 20 Oct (refs crowd-low-1..4):
# the crowd sits packed together facing south, the gallery's steps full behind them; every camera at head height or
# lower, inside the crowd, looking north to the gallery. So screen right (looking north) is west: she is carried
# west and the van drives off west.
GRAN_AT = (-3.0, 48.0)            # she stands among the sitting crowd near the gallery's steps, facing south
FACE = (0.0, -1.0)                # the crowd's facing
POLICE = {'SUPER': (-3.0, 18.2), 'PC1': (-4.9, 17.2), 'PC2': (-1.1, 17.2), 'PC3': (-6.8, 17.0), 'PC4': (0.8, 17.0),
          'PC5': (-8.6, 17.1)}    # a line in front of the column and its lions, facing the crowd; the senior officer
                                  # front centre
VAN_AT = (-29.0, 48.0)            # its back doors face the square (east); it drives off west
VAN_HEADING = math.pi
THROW_FROM = (-11.0, 48.0)        # where the carriers swing and let go
VAN_BACK = VAN_AT[0] + 5.93 / 2   # the van's open back (x)
# Timings of the storm and the throw
ROPE_DROP = (8.8, 9.0)            # the ropes fall into frame
SLIDE = (9.05, 10.15)             # the two counter-terror officers slide down
RUN_IN = 8.75                     # the six on foot run in from left, right and behind
GRAB = (10.45, 10.8)              # their hands go to her arms
LIFT = (10.8, 11.25)              # she rises off the ground
CARRY = (11.25, 14.05)            # carried east to the throwing spot (brisk)
SWING = (14.05, 14.55)            # swung back once, then forward; let go at the end
FLIGHT = (14.55, 15.3)            # head first through the air, about 15 m, into the van
SLAM = (15.45, 15.7)              # an officer slams the doors
DRIVE = 15.85                     # lights on, the van speeds off east
STAND_BY = (27.0, 29.2)           # the officer waiting by the van's doors

# The interrogation room: table at the origin; she sits south of it facing the door (+z), he north with his back to it
GRAN_SEAT = (0.0, -0.72, (0.0, 1.0))
SUPER_SEAT = (0.0, 0.72, (0.0, -1.0))
DOOR_OPEN = (28.75, 29.25)
JENKINS_IN = (29.0, 29.9)
# The corridor: the two of them outside the door
CORR_SUPER = (-0.36, 1.3)
CORR_JENKINS = (0.36, 1.3)
JAB = (37.95, 38.2)               # his finger into Jenkins's chest, on the cut-off
LEAN_IN = (38.2, 38.7)            # leaning forward, aggressive
# ====================================================================================================================


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def shot_start(name):
    return next(s[1] for s in SHOTS if s[0] == name)


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def keyed(t, keys):
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, a), (t1, b) in zip(keys, keys[1:]):
        if t <= t1:
            u = ease((t - t0) / (t1 - t0))
            return tuple(x + (y - x) * u for x, y in zip(a, b)) if isinstance(a, tuple) else a + (b - a) * u
    return keys[-1][1]


# ------------------------------------------------------------------------------------------------ the voices
for ln in LINES:
    v = MA.line(ln['audio'])
    ln['_voice'] = v
    ln['end'] = ln['start'] + len(v) / SR
    ln['_stretches'] = MA.pauses(v, 0.12)
TRACK = {}
for ln in LINES:
    if ln['who'] in ('SUPER', 'JENKINS'):
        TRACK.setdefault(ln['who'], []).extend((a + ln['start'], b + ln['start'], sh)
                                               for a, b, sh in mouths.track(ln['text'], ln['_stretches']))
BLINKS = {w: F.blinks(i * 7 + 3, 0.0, DUR, talking=True) for i, w in enumerate(['GRAN', 'SUPER', 'JENKINS'])}


def _chunks():
    """Each subtitle as (start, end, text): a line's chunks laid on its phrases (its recording's own pauses); within a
    phrase each chunk starts where its first syllable falls, a beat after the voice; each stays up until the next
    starts, or until just after its line ends."""
    import voices
    out = []
    for ln in LINES:
        st = ln['_stretches']
        groups = CHUNKS[ln['n']]
        if len(st) != len(groups):                        # the measured phrases spread evenly over the planned ones
            a, b = st[0][0], st[-1][1]
            st = [(a + (b - a) * k / len(groups), a + (b - a) * (k + 1) / len(groups)) for k in range(len(groups))]
        for (a, b), grp in zip(st, groups):
            syl = [max(1, voices.syllables_in(c)) for c in grp]
            acc = 0
            for c, n in zip(grp, syl):
                out.append([ln['start'] + a + (b - a) * acc / sum(syl) + 0.1, ln['end'] + 0.25, c])
                acc += n
    out.sort()
    for i in range(len(out) - 1):
        out[i][1] = min(out[i][1], out[i + 1][0])
    return [tuple(x) for x in out]


SUBS = None


def caption_at(t):
    global SUBS
    if SUBS is None:
        SUBS = _chunks()
    for t0, t1, c in SUBS:
        if t0 <= t < t1:
            return c
    return None


# ------------------------------------------------------------------------------------------------ the crowd
def _crowd():
    """The protest (refs protest-1..3; Sam, 20 Oct: "crowds are pushed together, side by side"): people sitting
    shoulder to shoulder in rough rows (about 0.6 m apart, rows 0.85 m) facing the gallery, a few rows standing at
    the back (south) waving flags; some on the fountains' rims. Narrow aisles are left where the armed officers come
    through and where she is carried (there were gaps like these in the real sit-ins)."""
    rng = np.random.default_rng(42)
    out = []
    for z in np.arange(16.5, 55.5, 0.85):
        off = rng.uniform(0, 0.6)
        for x in np.arange(-25.0 + off, 25.0, 0.6):
            x_, z_ = x + rng.uniform(-0.08, 0.08), z + rng.uniform(-0.12, 0.12)
            if rng.random() < 0.06:                     # the odd gap
                continue
            if any(math.hypot(x_ - fx, z_ - fz) < 9.8 for fx, fz in S3.FOUNTAINS):
                continue
            if math.hypot(x_ - GRAN_AT[0], z_ - GRAN_AT[1]) < 0.75:
                continue
            if abs(z_ - GRAN_AT[1]) < 1.15 and -15 < x_ < 15:   # the aisle along her row (left, right, the carry)
                continue
            if abs(x_ - GRAN_AT[0]) < 0.7 and z_ > GRAN_AT[1]:  # the aisle from behind (north)
                continue
            if z_ < GRAN_AT[1] and abs(x_ - GRAN_AT[0]) < 2.6 and z_ > LOW_CAM[2] - 1.0:
                continue                                 # in front of the low camera: only the sitters in FRONT
            if abs(x_ - LOW_CAM[0]) < 1.4 and LOW_CAM[2] - 1.6 < z_ < LOW_CAM[2] + 0.5:
                continue                                 # where the low camera sits
            if abs(x_ - WIDE_CAM[0]) < 1.2 and abs(z_ - WIDE_CAM[2]) < 1.2:
                continue
            if -10.5 < x_ < 3.5 and 15.0 < z_ < 25.5:    # the police line and the camera's straight view of it
                continue
            if x_ < -9 and abs(z_ - GRAN_AT[1]) < 2.2:     # the throw's path (she flies over the crowd either side)
                continue
            if x_ < -24 and abs(z_ - GRAN_AT[1]) < 4.5:    # round the van
                continue
            if x_ < -6 and GRAN_AT[1] - 9.5 < z_ < GRAN_AT[1] - 7.5:   # where the throw's camera tracks along
                continue
            if x_ < -4 and GRAN_AT[1] - 6.8 < z_ < GRAN_AT[1] - 2.0:   # the lane the police cleared to carry her out
                continue                                                # (one row stays, at the foot of the frame)
            if -10 < x_ < -2 and abs(z_ - GRAN_AT[1]) < 2.3:   # room round the throw's camera as it follows them
                continue
            out.append((x_, z_, z_ > 52.5 or rng.random() < 0.04))
    for k, x in enumerate(np.arange(-10.5, 10.6, 0.62)):  # sitting all over the gallery's steps (refs crowd-low-1..3)
        for r in range(1, 11):
            z_ = S3.SQ_N + r * 0.5 + rng.uniform(-0.05, 0.05)
            if rng.random() < 0.1:
                continue
            out.append((x + rng.uniform(-0.08, 0.08), z_, False))
    for x in np.arange(-40, 40, 0.7):                      # standing along the terrace railings
        if abs(x) < 11.5 or rng.random() < 0.25:
            continue
        out.append((x, S3.SQ_N + 0.9 + rng.uniform(0, 0.6), True))
    people = []
    for k, (x, z, standing) in enumerate(out):
        sp = C.protester(k)
        if rng.random() < 0.025:                       # a steward in an orange hi-vis vest (refs crowd-low-1..3)
            sp['steward'] = True
        people.append(dict(sp=sp, x=x, z=z, standing=standing, seed=k, base=step_height(z)))
    for k, (x, z) in enumerate(FRONT):                 # sitting in front of the low cameras (shots 2 and 5): the
        sp = C.protester(400 + k)                        # middle one's board is the foreground object that hides the
        sp['carry'] = 'board' if k == 1 else None        # bottom of her placard (Sam's brief)
        if k == 1:
            sp['board'] = 'FREE PALESTINE'
            sp['front_board'] = True
            sp['height'] = 1.55                           # a small man, so his head stays below his board's top
        people.append(dict(sp=sp, x=x, z=z, standing=False, seed=400 + k))
    return people


def step_height(z):
    """The ground's height at z: the paving (0), the gallery's steps rising, the terrace (TERRACE_Y)."""
    if z <= S3.SQ_N:
        return 0.0
    return min(S3.TERRACE_Y, S3.TERRACE_Y * (z - S3.SQ_N) / 6.0)


def _front():
    """The foreground sitters: the board man on the line from the low camera to the hidden part of her placard,
    2.3 m from the camera; one either side of him, a little further back."""
    cx, cy, cz = LOW_CAM
    gx, gz = GRAN_AT
    d = math.hypot(gx - cx, gz - cz)
    u = 2.3 / d
    bx, bz = cx + (gx - cx) * u, cz + (gz - cz) * u
    return [(bx - 0.85, bz + 0.5), (bx, bz), (bx + 0.85, bz + 0.45)]


LOW_CAM = (GRAN_AT[0] + 0.25, 0.98, GRAN_AT[1] - 5.2)   # among the sitting protesters, at their eye level
WIDE_CAM = (-1.0, 1.9, 25.0)                            # a standing person's eye height, in the crowd (past the police)
FRONT = _front()
CROWD = _crowd()


def chanting(t):
    """How open the crowd's mouths are: during the chant's phrases, a shout on each syllable."""
    ln = LINES[0]
    for a, b in ln['_stretches']:
        if ln['start'] + a <= t < ln['start'] + b:
            return 1.0 if int((t - ln['start']) * 5) % 2 == 0 else 0.5
    return 0.0


def front_board_y(c):
    """Where the board man's hands go (his own units) so his board's top edge sits on the line from the low camera to
    just above the top of the hidden part of her placard (with a margin)."""
    f = C.HEIGHTS['GRAN'] / 1.75
    neck = 928 * M * f
    hidden_top = neck - (330 - C.PLACARD_H / M * (1 - C.LETTERED)) * M * f + 0.06
    cx, cy, cz = LOW_CAM
    d_board = math.hypot(c['x'] - cx, c['z'] - cz)
    d_gran = math.hypot(GRAN_AT[0] - cx, GRAN_AT[1] - cz)
    top = cy + (hidden_top - cy) * d_board / d_gran                # the board's top edge, metres
    h = 0.6 * 0.62                                               # the board's height (board_prop)
    fm = c['sp'].get('height', 1.75) / 1.75
    neck_m = 928 * M * fm - 470 * M * fm                         # his neck when sitting (bob 470)
    centre = top - h / 2
    hands = centre - h * 0.42                                    # board_prop: centre = hands - 0.42 h (up)
    # the drawn hands sit a little lower than their target: the camera's slight look-down inside the figure
    # (views.ELEV x the 170 forward) and the fist's own offset; measured by the hidden check: about 60 units
    return (neck_m - hands) / (M * fm) - 60.0


def ground_sit(sp, seed=0):
    """Sitting on the paving (refs protest-1..3): the body down so the hips rest on the ground, knees up, feet
    forward (some cross-legged); hands on the knees, or holding a board or flag."""
    j = C.pose_standing(sp)
    rng = np.random.default_rng(seed)
    j['bob'] = 470.0
    floor = 928 - 470
    cross = rng.random() < 0.5
    for sd, sg in (('L', -1), ('R', 1)):
        fx = (-sg * 40) if cross else sg * 80
        j['foot' + sd] = (fx, floor - 40, 300.0 if cross else 360.0)
        V.arm_to(j, sd, (sg * 110.0, 330.0, 230.0), 'down', 'fist')
    return j


def held(c):
    """What this protester holds up: their flag or board, except right under the wide camera's nose or in front
    of the throw's camera (both the full drawing and the simple far one use this)."""
    carry = c['sp'].get('carry')
    if c['sp'].get('front_board'):
        return carry
    if math.hypot(c['x'] - WIDE_CAM[0], c['z'] - WIDE_CAM[2]) < 7 or in_throw_view(c):
        return None
    return carry


def in_throw_view(c):
    """Between the throw's tracking camera and the throw: these sit (no flags or boards held up), so the carry and
    the flight read over their heads."""
    return c['x'] < -4 and GRAN_AT[1] - 7.5 < c['z'] < GRAN_AT[1] - 2.0


def crowd_pose(c, t):
    sp = dict(c['sp'])
    seed = c['seed']
    if c['standing'] and not in_throw_view(c):
        j = C.pose_standing(sp)
    else:
        j = ground_sit(sp, seed)
    ch = chanting(t) * (1 if seed % 5 else 0.0)
    sp['mouth'] = 'shout' if ch > 0.9 else ('open' if ch > 0.2 else 'line')
    sp['blink'] = F.blinking(t, F.blinks(seed, 0.0, DUR))
    sp['tilt'] = filmkit.shifts(t, seed=seed, amount=0.03)
    carry = held(c)
    if carry == 'flag':
        lift = -120.0
        V.arm_to(j, 'R', (sp['shoulders'] * 0.7, lift - 30 * ch, 60.0), 'out', 'fist')
        j['props'].append(C.flag_prop(t, seed=seed))
        j['grip'] = {'R'}
    elif carry == 'board' and sp.get('front_board'):
        y = front_board_y(c)                              # held up in front of his face (drawn over his head)
        for sd, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, sd, (sg * 150.0, y, 170.0), 'down', 'fist')
        j.setdefault('face_props', []).append(C.board_prop(sp['board'], seed=seed, t=t))
    elif carry == 'board':
        y = (140.0 if c['standing'] else 120.0) - 40 * ch
        for sd, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, sd, (sg * 150.0, y, 170.0), 'down', 'fist')
        j['props'].append(C.board_prop(sp['board'], seed=seed, t=t))
        j['grip'] = {'L', 'R'}
    C.outfit(j, sp)
    return sp, j


# ------------------------------------------------------------------------------------------------ drawing people
def put(img, cam, sp, x, z, facing, j, t, lift=0.0, height=None, head_yaw=None, shadow=True, base=0.0):
    """Someone standing (or sitting, or held up `lift` metres) at floor point (x, z), facing (dx, dz), through the
    camera: their real height sets their scale; a soft flat shadow under them first."""
    h = height or C.HEIGHTS.get(sp.get('name'), sp.get('height', 1.75))
    f = h / 1.75
    neck = (928 * M) * f + lift + base
    if cam.depth((x, neck, z)) < 0.4:
        return None
    if shadow:
        ring = [(x + 0.32 * math.cos(u), base + 0.004, z + 0.24 * math.sin(u)) for u in np.linspace(0, 2 * math.pi, 18)]
        if all(cam.depth(q) > 0.3 for q in ring):
            lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            B.Pen(lay, FLAT).poly([cam.project(q)[0] for q in ring], (0, 0, 0, 60 if lift < 0.1 else 30), None)
            img.alpha_composite(lay)
    (X, Y), k = cam.project((x, neck, z))
    s = k * M * f
    if s > 4.0:
        return None
    yaw = cam.yaw_of((x, 0, z), facing)
    hy = None if head_yaw is None else cam.yaw_of((x, 0, z), head_yaw)
    j2 = C.person(img, FLAT, X, Y, s, dict(sp, full=True, pose='custom'), t, yaw, j, hy)
    return X, Y, s, yaw, j2


# ------------------------------------------------------------------------------------------------ her
def gran_raise(t):
    """Her placard from held low (tilted back) to up at her chest (shot 2), trembling."""
    a = shot_start('gran') + 0.55
    return ease((t - a) / 0.9)


def gran_state(t, seated=False):
    sp = dict(C.GRAN)
    sp['blink'] = F.blinking(t, BLINKS['GRAN'])
    sp['mouth'] = 'line'
    sp['brows'] = 'sincere'
    sp['tilt'] = filmkit.shifts(t, seed=91, amount=0.02)
    return sp


def gran_pose(t, sp):
    """Standing with her placard (chest height, trembling) until she is taken; then carried by the arms."""
    if t < GRAB[1] + 0.35:
        u = gran_raise(t)
        j, quad = C.placard_pose(sp, t, 0.0, tremble=1.0, seed=3)      # at her chest (0), trembling
        if u < 1.0:                                         # still coming up: lower, tilted back
            j, quad = low_placard(sp, t, u)
        if t >= LIFT[0] - 0.4:                              # she lets go: the placard falls face down (unseen)
            j = C.pose_standing(sp)
            j['props'] = []
        return j
    return None


def low_placard(sp, t, u):
    """The placard coming up from her waist (u 0) to her chest (u 1), tilting upright as it comes."""
    j = C.pose_standing(sp)
    W_, H_ = C.PLACARD_W / M, C.PLACARD_H / M
    tilt = 0.35 + 0.65 * u
    bottom = 470 + (330 - 470) * u
    jy = 5 * math.sin(t * 41 + 3) * u
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, (sg * (W_ / 2 - 26), bottom - 26 + jy, 110.0), 'out', 'fist')
    quad = [(-W_ / 2, bottom - H_ * tilt + jy), (W_ / 2, bottom - H_ * tilt + jy), (W_ / 2, bottom + jy), (-W_ / 2, bottom + jy)]
    j['props'] = [C.placard_prop(quad, sp['skin'])]
    return j, quad


def gran_where(t):
    """Her floor point, height off the ground, and facing, over the whole square sequence."""
    x, z = GRAN_AT
    if t < LIFT[0]:
        return x, z, 0.0, FACE
    if t < CARRY[0]:
        return x, z, 0.35 * ease((t - LIFT[0]) / (LIFT[1] - LIFT[0])), FACE
    if t < SWING[0]:                                    # carried sideways (Sam), still facing us, legs dangling
        u = (t - CARRY[0]) / (CARRY[1] - CARRY[0])
        return x + (THROW_FROM[0] - x) * u, z + (THROW_FROM[1] - z) * u, 0.35 + 0.03 * math.sin(t * 14), FACE
    return THROW_FROM[0], THROW_FROM[1], 0.35, FACE


def carriers_at(t):
    """The two counter-terror officers either side of her (her left and right arms)."""
    x, z, lift, f = gran_where(t)
    if t < CARRY[0]:
        return (x + 0.55, z), (x - 0.55, z), FACE
    u = ease((t - CARRY[0]) / 0.5)                       # walking off: one a little nearer us, one a little further,
    return (x + 0.45, z - 0.32 * u), (x - 0.45, z + 0.32 * u), (-1.0, 0.0)   # so she shows between them side on


def to_torso(px, pz, facing, sp, world, lean=0.0):
    """A world point (x, y, z) in the torso frame of someone standing at (px, pz) facing (fx, fz): x to their right,
    y down from the neck, z forward (person units), so a hand can be put exactly on it (real contact)."""
    fx, fz = facing
    n = math.hypot(fx, fz) or 1.0
    fx, fz = fx / n, fz / n
    rx, rz = fz, -fx
    f = C.HEIGHTS.get(sp.get('name'), 1.75) / 1.75
    neck = 928 * M * f
    dx, dz = world[0] - px, world[2] - pz
    return ((dx * rx + dz * rz) / (M * f), (neck - world[1]) / (M * f), (dx * fx + dz * fz) / (M * f))


def her_arm(t, side):
    """Her upper arm on one side (side -1: her right, east of her; +1: her left), held out by the carriers."""
    x, z, lift, f = gran_where(t)
    neck = 928 * M * (C.HEIGHTS['GRAN'] / 1.75) + lift
    return (x - side * 0.22, neck - 0.1, z)


# ------------------------------------------------------------------------------------------------ the armed officers
def _rel(dx, dz):
    return (GRAN_AT[0] + dx, GRAN_AT[1] + dz)


RUNNERS = {   # (path in metres, start delay): from the west (screen right), the east, and from behind (north)
    'ARV1': ([_rel(-13.0, -0.4), _rel(-1.6, -0.4), _rel(-1.4, -1.2)], 0.0),
    'ARV2': ([_rel(-14.0, 0.5), _rel(-2.4, 0.5), _rel(-2.0, 0.9)], 0.15),
    'ARV3': ([_rel(0.0, 14.0), _rel(0.0, 2.0), _rel(0.4, 1.4)], 0.1),
    'ARV4': ([_rel(15.0, -0.4), _rel(2.2, -0.4), _rel(1.8, -1.1)], 0.05),
    'ARV5': ([_rel(16.0, 0.5), _rel(2.9, 0.5), _rel(2.5, 1.0)], 0.2),
    'ARV6': ([_rel(0.0, 18.0), _rel(0.0, 2.6), _rel(-0.8, 2.2)], 0.3),
}
ROPES = {'ARV7': (GRAN_AT[0] - 0.55, GRAN_AT[1]), 'ARV8': (GRAN_AT[0] + 0.55, GRAN_AT[1])}


def runner(who, t, cam):
    """One armed officer: running in (rifle low across the body), then aiming at her."""
    sp = dict(C.PEOPLE[who])
    path, delay = RUNNERS[who]
    x, z, yaw, state = moves.travel(path, t, 'run', start=RUN_IN + delay)
    if state == 'moving':
        j = moves.gait(sp, t - RUN_IN - delay, 'run')
        j = C.low_ready(j, sp)
        C.outfit(j, sp)
        facing = (math.sin(math.radians(yaw)), math.cos(math.radians(yaw)))
    else:
        tx, tz = gran_where(t)[:2]
        facing = (tx - x, tz - z)
        j = C.aim_pose(sp, (0, 6))
    sp['blink'] = F.blinking(t, F.blinks(hash(who) % 97, 0, DUR))
    sp['look'] = 0.0
    return sp, j, x, z, facing


def roper(who, t):
    """A counter-terror officer down the rope: sliding (one hand high on the rope), landing knees bent beside her,
    then taking her arm (hooked under her armpit, a hand on her forearm: ref arrest) and carrying her."""
    sp = dict(C.PEOPLE[who])
    x0, z0 = ROPES[who]
    side = -1 if who == 'ARV7' else 1
    if t < SLIDE[1]:
        u = (t - SLIDE[0]) / (SLIDE[1] - SLIDE[0])
        y = 9.0 * (1 - u) ** 1.6 if t >= SLIDE[0] else 9.0
        j = C.pose_standing(sp)
        V.arm_to(j, 'R', (30.0, -300.0, 60.0), 'up', 'fist')
        V.arm_to(j, 'L', (sp['shoulders'] + 40.0, 150.0, 160.0), 'down', 'fist')
        j['footL'] = (-90.0, V.ANKLE_Y - 120, 120.0)
        j['footR'] = (70.0, V.ANKLE_Y - 40, -40.0)
        j['props'].append(C.rope_prop(top=-9000.0, bottom=300.0))
        j['grip'] = {'R'}
        C.outfit(j, sp)
        return sp, j, x0, z0, y, FACE
    (cx, cz), (dx, dz), f = carriers_at(t)
    x, z = (cx, cz) if side < 0 else (dx, dz)
    if t < GRAB[0]:                                          # landed, crouched a moment, rising
        j = C.pose_standing(sp)
        u = ease((t - SLIDE[1]) / 0.3)
        j['bob'] = 60 * (1 - u)
        C.outfit(j, sp)
        return sp, j, x, z, 0.0, FACE
    # holding her arm: his near hand under her armpit, the other on her forearm (both on the arm nearest him)
    if t < CARRY[0]:
        j = C.pose_standing(sp)
        tgt = -side * 70.0
        V.arm_to(j, 'L' if side > 0 else 'R', (tgt, 60.0, 90.0), 'down', 'palm')
        V.arm_to(j, 'R' if side > 0 else 'L', (tgt, 170.0, 150.0), 'down', 'palm')
        C.outfit(j, sp)
        face = (side * 1.0, -0.25)
        return sp, j, x, z, 0.0, face
    phase = t - CARRY[0]
    facing = (-1.0, 0.0)
    if t < SWING[0]:
        j = moves.gait(sp, phase, 'brisk')
    else:
        j = C.pose_standing(sp)
        u = min(1.0, (t - SWING[0]) / (SWING[1] - SWING[0]))
        j['lean'] = -10 + 26 * u                             # back on the swing, then forward on the throw
        if t > SWING[1]:                                     # and upright again, watching her go
            j['lean'] = 16 * (1 - ease((t - SWING[1] - 0.25) / 0.5))
    if t < SWING[1]:                                         # both hands on her arm: one under the armpit, one on the
        grip = her_arm(t, side)                              # forearm (ref arrest), wherever she is (real contact)
        near = 'R' if side < 0 else 'L'                      # the hand on the side nearer her takes the armpit
        far = 'L' if near == 'R' else 'R'
        for sd, dy, dx in ((near, 0.0, 0.0), (far, 0.12, -side * 0.12)):
            tgt = to_torso(x, z, facing, sp, (grip[0] + dx, grip[1] - dy, grip[2]))
            ok = V.reach_ok(j, sd, tgt, 'palm')
            V.arm_to(j, sd, tgt, 'down', 'palm')
            if not ok:
                CONTACT_FAULTS.append((round(t, 2), who, f'{sd} hand cannot reach her arm'))
    else:                                                    # let go: arms follow through, out after her
        for sd in 'LR':
            V.arm_to(j, sd, ((-1 if sd == 'L' else 1) * 120.0, -60.0, 300.0), 'down', 'palm')
    C.outfit(j, sp)
    return sp, j, x, z, 0.0, facing


CONTACT_FAULTS = []


# ------------------------------------------------------------------------------------------------ the police line
POLICE_POSE = {'PC4': 'arms_folded', 'PC5': 'clasped', 'PC2': 'clasped'}


def police(who, t):
    sp = dict(C.PEOPLE[who])
    pose = POLICE_POSE.get(who)
    if pose == 'arms_folded':
        j = C.outfit(moves.pose(sp, 'arms_folded'), sp)
    elif pose == 'clasped':
        j = C.clasped_pose(sp)
    else:
        j = C.pose_standing(sp)
    sp['blink'] = F.blinking(t, F.blinks(hash(who) % 89, 0, DUR))
    sp['tilt'] = filmkit.shifts(t, seed=hash(who) % 50, amount=0.03)
    sp['mouth'] = 'set' if who != 'PC2' else 'line'
    sp['brows'] = 'serious' if who in ('PC1', 'PC3') else ('weary' if who == 'PC4' else None)
    x, z = POLICE[who]
    return sp, j, x, z, (0.0, 1.0)


def super_square(t):
    """The senior officer in the square: watching, then his jaw drops (strength 3) and he speaks."""
    sp = dict(C.SUPER)
    j = C.pose_standing(sp)
    talking(sp, 'SUPER', t)
    if t >= DROP:
        hp = C.horror(sp, HORROR_LEVEL)
        if mouths.at(TRACK['SUPER'], t) != 'rest':
            sp['mouth'] = 'v:' + mouths.at(TRACK['SUPER'], t)
            j['head_props'] = [lambda *a: None] + j['head_props']
            hp2 = C.horror(dict(C.SUPER), HORROR_LEVEL)    # the brows stay up while he speaks
            j['head_props'] = [brows_only(HORROR_LEVEL)] + j['head_props'][1:]
            sp['brows'], sp['brow_c'] = None, sp['skin']
        else:
            j['head_props'] = [hp] + j['head_props']
    sp['tilt'] = filmkit.shifts(t, seed=61, amount=0.02)
    x, z = POLICE['SUPER']
    return sp, j, x, z, (0.0, 1.0)


def brows_only(level):
    """The horror brows on their own (while he talks: the mouth is the lip sync's)."""
    sp = dict(C.SUPER)
    draw = C.horror(sp, level)

    def d(p, view, sp_, hx, hy):
        q = dict(sp_)
        hw, hh = q.get('hw', 72), q.get('hh', 90)
        _, _, _, br = C.HORROR[level]
        up = {'raise4': (3, 1), 'raise9': (6, 2), 'alarm': (10, 2), 'wow': (12, 4)}[br]
        if view not in ('front', 'three'):
            return
        fx = hx + (0.4 * hw if view == 'three' else 0.0)
        k = 1.0 if view == 'front' else 0.8
        from ed import curve
        for sgn in (-1, 1):
            ex, ey = fx - 4 + sgn * 30 * k, hy - 8
            p.poly(curve([(ex - sgn * 8 * k, ey - 22 - up[0]), (ex + sgn * 8 * k, ey - 23 - up[0] + up[1]),
                          (ex + sgn * 24 * k, ey - 17 - up[1]), (ex + sgn * 23 * k, ey - 13 - up[1]),
                          (ex + sgn * 8 * k, ey - 17 - up[0] + up[1]), (ex - sgn * 8 * k, ey - 16 - up[0])], 3),
                   C.SUPER['brow_c'], None)
    return d


def talking(sp, who, t):
    shape = mouths.at(TRACK.get(who, []), t)
    sp['mouth'] = ('set' if who == 'SUPER' else 'line') if shape == 'rest' else 'v:' + shape
    sp['blink'] = F.blinking(t, BLINKS[who])


# ------------------------------------------------------------------------------------------------ cameras


def cam_for(t):
    s = shot_of(t)
    u = (t - shot_start(s))
    if s == 'wide':                                        # at a standing person's eye height, looking at the gallery
        return Cam3((WIDE_CAM[0], WIDE_CAM[1], WIDE_CAM[2] + 0.5 * u), (-1.0, 3.2, 62.0), focal=760)
    if s == 'gran':                                         # zooming in on her from among the sitting crowd
        k = ease(u / 2.6)
        return Cam3(LOW_CAM, (GRAN_AT[0], 1.28 + 0.06 * k, GRAN_AT[1]), focal=900 + 1500 * k)
    if s == 'police':                                      # straight on to the line (Sam: no diagonals), the column
        return Cam3((-3.0, 1.6, 24.5), (-3.0, 1.9, 0.0), focal=1000)   # and its lions behind them
    if s == 'super':                                       # straight on, close
        x, z = POLICE['SUPER']
        return Cam3((x, 1.66, z + 1.25), (x, 1.66, z), focal=1500)
    if s == 'storm':                                       # low among the sitters, straight on (the board in front)
        return Cam3(LOW_CAM, (GRAN_AT[0], 1.9, GRAN_AT[1]), focal=1350)
    if s == 'throw':                                       # from the south, at head height: she goes right (west)
        # side on, straight north (Sam: carried and thrown horizontally), tracking along with them like a side-scroller,
        # then with her in flight, and holding on the van as it speeds off right
        ax = gran_where(t)[0] if t < FLIGHT[0] else (flight_pos(min(t, FLIGHT[1]))[0] if t < FLIGHT[1] + 0.1 else VAN_BACK - 1.5)
        cx = min(ax - 0.6, -6.0)
        cx = max(cx, VAN_BACK - 0.5)
        return Cam3((cx, 1.45, GRAN_AT[1] - 4.2), (cx, 2.3, GRAN_AT[1]), focal=950)   # tilted up: less bare paving
    if s == 'interro':
        return Cam3((2.3, 1.45, -0.25), (0.0, 0.95, 0.0), focal=900)
    if s == 'interro_s':                                   # straight on to him, from her side of the table
        return Cam3((0.0, 1.2, -0.25), (0.0, 1.18, 0.72), focal=1150)
    if s == 'interro_g':                                   # straight on to her
        return Cam3((0.0, 1.1, 0.25), (0.0, 1.05, -0.72), focal=1150)
    if s == 'door':                                        # straight on to the door (to his left behind him)
        return Cam3((0.75, 1.5, -2.0), (0.75, 1.3, 2.2), focal=900)
    return Cam3((0.15, 1.55, 4.6), (0.0, 1.35, 1.3), focal=1150)


# ------------------------------------------------------------------------------------------------ the pictures
def square(img, cam, t):
    S3.square_back(img, cam, t)
    items = list(S3.square_pieces(cam, t))
    for c in CROWD:
        pos = (c['x'], 0.8, c['z'])
        items.append((cam.depth(pos), lambda im, c=c: crowd_draw(im, cam, c, t)))
    # her
    x, z, lift, f = gran_where(t)
    if t < FLIGHT[0]:
        items.append((cam.depth((x, 1.0, z)), lambda im: gran_draw(im, cam, t)))
    elif t < FLIGHT[1] + 0.2:
        items.append((cam.depth(flight_pos(t)), lambda im: gran_flying(im, cam, t)))
    # the police line
    for who in POLICE:
        if who == 'SUPER':
            continue
        items.append((cam.depth((POLICE[who][0], 1, POLICE[who][1])), lambda im, w=who: put(im, cam, *police_args(w, t))))
    items.append((cam.depth((POLICE['SUPER'][0], 1, POLICE['SUPER'][1])), lambda im: put(im, cam, *super_args(t))))
    # the armed officers
    if t >= RUN_IN:
        for who in RUNNERS:
            sp, j, x_, z_, fc = runner(who, t, cam)
            items.append((cam.depth((x_, 1, z_)), lambda im, a=(sp, x_, z_, fc, j): put(im, cam, *a, t)))
        for who in ROPES:
            if t >= ROPE_DROP[0]:
                sp, j, x_, z_, y_, fc = roper(who, t)
                items.append((cam.depth((x_, 1, z_)) - 0.01,
                              lambda im, a=(sp, x_, z_, fc, j), y_=y_: put(im, cam, *a, t, lift=y_, shadow=y_ < 0.2)))
    # the van and the officer by it
    vx, vz = van_at(t)
    items.append((cam.depth((vx, 1.3, vz)), lambda im: S3.van(im, cam, vx, vz, VAN_HEADING, t, doors=door_open(t),
                                                               lights=t >= DRIVE)))
    items.append((cam.depth((VAN_BACK + 0.6, 1, VAN_AT[1] - 1.5)), lambda im: door_officer(im, cam, t)))
    for d, fn in sorted(items, key=lambda v: -v[0]):
        fn(img)


def police_args(who, t):
    sp, j, x, z, f = police(who, t)
    return sp, x, z, f, j, t


def super_args(t):
    sp, j, x, z, f = super_square(t)
    return sp, x, z, f, j, t


def crowd_draw(img, cam, c, t):
    f = c['sp'].get('height', 1.75) / 1.75
    standing = c['standing'] and not in_throw_view(c)
    neck = 928 * M * f - (0 if standing else 470 * M * f) + c.get('base', 0.0)
    if cam.depth((c['x'], neck, c['z'])) < 0.4:
        return
    (X, Y), k = cam.project((c['x'], neck, c['z']))
    s = k * M * f
    if s < 0.3:                                        # beyond a few metres (a head under about 40 px): a simple figure
        return tiny(img, c, X, Y, s, t)
    sp, j = crowd_pose(c, t)
    put(img, cam, sp, c['x'], c['z'], FACE, j, t, base=c.get('base', 0.0))


def tiny(img, c, X, Y, s, t):
    """A far-off protester: coat, head and hair as flat shapes in their own colours (one outline), sitting or
    standing; flags and boards held up as small flat shapes."""
    sp = c['sp']
    p = B.Pen(img, FLAT)
    coat = sp.get('dress', sp.get('jacket', (90, 90, 90)))
    sw = sp.get('shoulders', 140) * s
    standing = c['standing'] and not in_throw_view(c)
    body = 520 * s if standing else 330 * s
    p.poly([(X - sw, Y + 20 * s), (X + sw, Y + 20 * s), (X + sw * 0.9, Y + body), (X - sw * 0.9, Y + body)], coat, INK, 1.0)
    if standing:
        p.poly([(X - sw * 0.6, Y + body), (X + sw * 0.6, Y + body), (X + sw * 0.5, Y + body + 420 * s),
                (X - sw * 0.5, Y + body + 420 * s)], sp.get('trousers', (50, 50, 56)), INK, 1.0)
    else:
        p.poly([(X - sw * 1.1, Y + body - 60 * s), (X + sw * 1.1, Y + body - 60 * s), (X + sw * 1.0, Y + body + 90 * s),
                (X - sw * 1.0, Y + body + 90 * s)], sp.get('trousers', (50, 50, 56)), INK, 1.0)
    if sp.get('steward'):
        p.poly([(X - sw * 0.9, Y + 40 * s), (X + sw * 0.9, Y + 40 * s), (X + sw * 0.85, Y + body * 0.85),
                (X - sw * 0.85, Y + body * 0.85)], (244, 124, 34), INK, 1.0)
    if sp.get('keffiyeh'):
        p.poly([(X - 60 * s, Y - 6 * s), (X + 60 * s, Y - 6 * s), (X, Y + 60 * s)], (240, 240, 236), INK, 1.0)
    hw, hh = sp.get('hw', 68) * s, sp.get('hh', 88) * s
    hy = Y - 150 * s
    if sp.get('hair') in ('long', 'bob'):
        p.ell(X, hy + hh * 0.2, hw * 1.15, hh * 1.05, sp.get('hair_c', (90, 80, 70)), INK, 1.0)
    p.ell(X, hy, hw, hh, sp['skin'], INK, 1.0)
    if sp.get('hair') not in ('bald', 'wisps'):
        p.poly([(X - hw * 1.02, hy - hh * 0.05), (X - hw * 0.7, hy - hh * 0.85), (X, hy - hh * 1.04),
                (X + hw * 0.7, hy - hh * 0.85), (X + hw * 1.02, hy - hh * 0.05), (X + hw * 0.6, hy - hh * 0.45),
                (X - hw * 0.6, hy - hh * 0.45)], sp.get('hair_c', (90, 80, 70)), INK, 1.0)
    if s > 0.08:                                       # a face that reads at this size: eyes, brows, mouth
        for sg in (-1, 1):
            p.ell(X + sg * 28 * s, hy - 6 * s, 9 * s, 10 * s, (250, 250, 248), None)
            p.ell(X + sg * 28 * s, hy - 5 * s, 4.5 * s, 5 * s, INK, None)
        if sp.get('glasses'):
            for sg in (-1, 1):
                p.ell(X + sg * 30 * s, hy - 6 * s, 22 * s, 18 * s, None, sp.get('glasses_c', INK), 1.0)
        op = chanting(t) * (1 if c['seed'] % 5 else 0)
        if op > 0.2:
            p.ell(X, hy + 52 * s, 13 * s, 10 * s * (1 + op), (70, 26, 30), INK, 0.8)
        else:
            p.line([(X - 14 * s, hy + 52 * s), (X + 14 * s, hy + 52 * s)], INK, 0.9)
    carry = held(c)
    wave = math.sin(t * 5.2 + c['seed'])
    if carry == 'flag':
        top = (X + sw + 60 * s * wave, Y - 700 * s)
        p.line([(X + sw, Y + 60 * s), top], (110, 84, 56), 1.4)
        fw, fh = 0.9 / M * s, 0.6 / M * s
        x0, y0 = top
        p.poly([(x0, y0), (x0 + fw, y0 + 8 * s), (x0 + fw, y0 + fh * 0.33 + 8 * s), (x0, y0 + fh * 0.33)], C.PAL_FLAG[0], None)
        p.poly([(x0, y0 + fh * 0.33), (x0 + fw, y0 + fh * 0.33 + 8 * s), (x0 + fw, y0 + fh * 0.67 + 8 * s), (x0, y0 + fh * 0.67)],
               C.PAL_FLAG[1], None)
        p.poly([(x0, y0 + fh * 0.67), (x0 + fw, y0 + fh * 0.67 + 8 * s), (x0 + fw, y0 + fh + 8 * s), (x0, y0 + fh)], C.PAL_FLAG[2], None)
        p.poly([(x0, y0), (x0 + fw * 0.4, y0 + fh / 2), (x0, y0 + fh)], C.PAL_FLAG[3], None)
    elif carry == 'board':
        w, h = 0.6 / M * s, 0.37 / M * s
        cy = Y + 20 * s - 40 * s * chanting(t)
        p.poly([(X - w / 2, cy - h), (X + w / 2, cy - h), (X + w / 2, cy), (X - w / 2, cy)], (246, 244, 236), INK, 1.0)
        p.line([(X - w * 0.3, cy - h * 0.6), (X + w * 0.3, cy - h * 0.6)], (196, 30, 40), 1.2)


def gran_draw(img, cam, t):
    sp = gran_state(t)
    x, z, lift, f = gran_where(t)
    j = gran_pose(t, sp)
    if j is None:                                            # held up by both arms, legs dangling
        j = C.carried_pose(sp, kick=1.0 if t > CARRY[0] else 0.4, t=t)
        sp['brows'] = 'sincere'
    return put(img, cam, sp, x, z, f, j, t, lift=lift, shadow=True)


def flight_pos(t):
    """Her centre on the throw: 15 m from the swing to the van's open back, about 3 m up at the top, fast."""
    u = (t - FLIGHT[0]) / (FLIGHT[1] - FLIGHT[0])
    x0, z0 = THROW_FROM
    x1 = VAN_BACK - 0.6
    return (x0 + (x1 - x0) * u, 1.2 + 1.3 * 4 * u * (1 - u) + 0.2 * u, z0)


def gran_flying(img, cam, t):
    """Hurled head first: her drawing (stiff, arms by her sides, legs together) turned to point along the throw and
    carried along its arc; she goes in through the open doors head first, legs last, and is gone."""
    pos = flight_pos(t)
    back = VAN_BACK
    if pos[0] < back - 1.8:
        return
    sp = gran_state(t)
    sp['brows'] = 'sincere'
    j = C.pose_standing(sp)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    (X, Y), k = cam.project(pos)
    f = C.HEIGHTS['GRAN'] / 1.75
    s = k * M * f
    hip_off = 450 * s
    C.person(lay, FLAT, X, Y - hip_off, s, dict(sp, full=True, pose='custom'), t, 0, j)
    # turn her to point along the throw (head leading): about -90 degrees on screen, a little more as she dips
    (Xa, Ya), _ = cam.project(flight_pos(min(t + 0.02, FLIGHT[1])))
    ang = math.degrees(math.atan2(Ya - Y, Xa - X))
    rot = lay.rotate(-(ang + 90) * ease((t - FLIGHT[0]) / 0.12), Image.BILINEAR, center=(X * B.SS, Y * B.SS))
    if pos[0] < back + 1.6:                                   # going in: what is past the doorway is inside
        (Xb, Yb), _ = cam.project((back, pos[1], pos[2]))
        mask = Image.new('L', img.size, 255)
        from PIL import ImageDraw
        d = ImageDraw.Draw(mask)
        dx, dy = Xa - X, Ya - Y
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        cx, cy = Xb * B.SS, Yb * B.SS
        far = 4000
        d.polygon([(cx - uy * far, cy + ux * far), (cx + uy * far, cy - ux * far),
                   (cx + uy * far + ux * far, cy - ux * far + uy * far), (cx - uy * far + ux * far, cy + ux * far + uy * far)],
                  fill=0)
        a = rot.split()[3]
        from PIL import ImageChops
        rot.putalpha(ImageChops.multiply(a, mask))
    img.alpha_composite(rot)


def door_open(t):
    if t < SLAM[0]:
        return 1.0
    return 1.0 - ease((t - SLAM[0]) / (SLAM[1] - SLAM[0]))


def van_at(t):
    if t < DRIVE + 0.15:
        return VAN_AT
    u = t - DRIVE - 0.15
    return (VAN_AT[0] - 6.0 * u * u, VAN_AT[1])


def door_officer(img, cam, t):
    """An armed officer waiting by the van's open back (ARV in a flat cap) who slams the doors after her."""
    sp = dict(C.ARVS[2])
    if t > DRIVE + 0.6:
        x, z = VAN_BACK + 1.0, VAN_AT[1] - 1.6
    else:
        x, z = VAN_BACK + 0.5, VAN_AT[1] - 1.4
    j = C.pose_standing(sp)
    if SLAM[0] - 0.15 <= t < SLAM[1] + 0.2:                  # both hands on the doors, pushing them shut
        u = ease((t - SLAM[0] + 0.15) / 0.4)
        for sd, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, sd, (sg * 80.0 + 60 * u, 150.0, 260.0 + 60 * u), 'down', 'palm')
    C.outfit(j, sp)
    put(img, cam, sp, x, z, (-1.0, 0.4), j, t)


def interro(img, cam, t):
    door = 0.0 if t < DOOR_OPEN[0] else ease((t - DOOR_OPEN[0]) / (DOOR_OPEN[1] - DOOR_OPEN[0]))
    S3.room(img, cam, t, door)
    S3.light_pool(img, cam)
    items = []
    gx, gz, gf = GRAN_SEAT
    sx, sz, sf = SUPER_SEAT
    items.append((cam.depth((gx, 0.5, gz - 0.1)), lambda im: S3.chair(im, cam, gx, gz - 0.05, gf)))
    items.append((cam.depth((sx, 0.5, sz + 0.1)), lambda im: S3.chair(im, cam, sx, sz + 0.05, sf)))
    items.append((cam.depth((0, 0.7, 0)), lambda im: S3.table(im, cam)))

    def gran(im):
        sp = gran_state(t)
        sp['look'] = 0.0
        j = C.outfit(moves.seated(sp), sp)
        for sd, sg in (('L', -1), ('R', 1)):                 # hands resting on the table, trembling a little
            V.arm_to(j, sd, (sg * 70.0, 260.0 + 4 * math.sin(t * 40 + sg), 330.0), 'down', 'fist')
        j['tilt'] = 0
        sp['tilt'] = 0.012 * math.sin(t * 37) + filmkit.shifts(t, seed=93, amount=0.015)   # the tremble (scripted)
        put(im, cam, sp, gx, gz, gf, j, t, shadow=False)

    def boss(im):
        sp = dict(C.SUPER)
        talking(sp, 'SUPER', t)
        sp['brows'] = 'fierce' if mouths.at(TRACK['SUPER'], t) != 'rest' else 'serious'
        j = C.outfit(moves.seated(sp), sp)
        lean = 14 if 18.0 < t < 28.6 else 6
        j['lean'] = lean
        for sd, sg in (('L', -1), ('R', 1)):                 # forearms on the table, leaning in
            V.arm_to(j, sd, (sg * 110.0, 300.0, 300.0), 'down', 'fist')
        head = None
        if t >= DOOR_OPEN[0] + 0.1:                          # the door behind him: he turns his head to it
            head = (0.0, 1.0)
        put(im, cam, sp, sx, sz, sf, j, t, shadow=False, head_yaw=head)
    items.append((cam.depth((gx, 1.0, gz)), gran))
    items.append((cam.depth((sx, 1.0, sz)), boss))
    if t >= JENKINS_IN[0]:
        u = ease((t - JENKINS_IN[0]) / (JENKINS_IN[1] - JENKINS_IN[0]))
        jx, jz = S3.DOOR[0] - 0.1 * u, S3.ROOM_Z + 0.3 - 0.75 * u

        def jen(im):
            sp = dict(C.JENKINS)
            talking(sp, 'JENKINS', t)
            sp['brows'] = 'sincere'
            j = moves.gait(sp, t - JENKINS_IN[0], 'walk') if u < 1 else C.pose_standing(sp)
            C.outfit(j, sp)
            put(im, cam, sp, jx, jz, (0.0, -1.0), j, t)
        items.append((cam.depth((jx, 1.0, jz)), jen))
    for d, fn in sorted(items, key=lambda v: -v[0]):
        fn(img)


def corridor(img, cam, t):
    S3.corridor(img, cam, t)
    items = []

    def boss(im):
        sp = dict(C.SUPER)
        talking(sp, 'SUPER', t)
        sp['brows'] = 'fierce' if t >= JAB[0] else 'weary'
        j = C.pose_standing(sp)
        if t >= JAB[0]:                                      # his finger in Jenkins's chest, then leaning in
            u = ease((t - JAB[0]) / (JAB[1] - JAB[0]))
            V.arm_to(j, 'R', (60.0, 120.0 + 60 * (1 - u), 160 + 280 * u), 'down', 'point')
            j['lean'] = 13 * ease((t - LEAN_IN[0]) / (LEAN_IN[1] - LEAN_IN[0]))
        else:
            sp['tilt'] = filmkit.shifts(t, seed=71, amount=0.02)
        C.outfit(j, sp)
        put(im, cam, sp, CORR_SUPER[0], CORR_SUPER[1], (1.0, 0.0), j, t)

    def jen(im):
        sp = dict(C.JENKINS)
        talking(sp, 'JENKINS', t)
        sp['brows'] = 'alarm' if t < JAB[0] else 'sincere'
        j = C.pose_standing(sp)
        if t >= JAB[0]:
            j['lean'] = -6 * ease((t - JAB[0]) / 0.3)
        else:
            sp['tilt'] = filmkit.shifts(t, seed=72, amount=0.03)
        C.outfit(j, sp)
        put(im, cam, sp, CORR_JENKINS[0], CORR_JENKINS[1], (-1.0, 0.0), j, t)
    items.append((cam.depth((CORR_SUPER[0], 1, CORR_SUPER[1])), boss))
    items.append((cam.depth((CORR_JENKINS[0], 1, CORR_JENKINS[1])), jen))
    for d, fn in sorted(items, key=lambda v: -v[0]):
        fn(img)


def close_super(img, cam, t):
    """Shot 4: close on him (the square behind him)."""
    square(img, cam, t)


def picture(t):
    """The frame without captions (they go on last)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    cam = cam_for(t)
    img = B.canvas((0, 0, 0))
    s = shot_of(t)
    if s in ('wide', 'gran', 'police', 'super', 'storm', 'throw'):
        square(img, cam, t)
    elif s in ('interro', 'interro_s', 'interro_g', 'door'):
        interro(img, cam, t)
    else:
        corridor(img, cam, t)
    return img


def overlay(img, t):
    if t < BLACK_AT:
        c = caption_at(t)
        if c:
            PP.caption(img, c)
    return img


def frame_image(t):
    return overlay(picture(t), t)


# ------------------------------------------------------------------------------------------------ sound
def chant_crowd():
    """Sam's chant, layered into a crowd: six copies, each a little earlier or later, a little higher or lower,
    quieter than the speaking lines (it is a background)."""
    x = LINES[0]['_voice']
    out = np.zeros(len(x) + SR)
    for k, (dt, pitch, g) in enumerate(((0.0, 1.0, 1.0), (0.09, 0.95, 0.7), (-0.06, 1.06, 0.6), (0.15, 0.9, 0.55),
                                         (0.04, 1.1, 0.5), (-0.11, 0.98, 0.5))):
        n = int(len(x) / pitch)
        y = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
        i = int((0.2 + dt) * SR)
        out[i:i + n] += y[:len(out) - i] * g
    return out / 2.2


def heli(n0, n1):
    """A helicopter overhead (Sam, 20 Oct: yes): the blades' thud about 5 times a second over a low rumble, faded in
    and out (made in code, never a hiss)."""
    n = n1 - n0
    tt = np.arange(n) / SR
    chop = (0.5 + 0.5 * np.sin(2 * math.pi * 5.2 * tt)) ** 6
    rng = np.random.default_rng(5)
    noise = rng.standard_normal(n)
    from scipy.signal import butter, sosfilt
    low = sosfilt(butter(2, 220, 'lp', fs=SR, output='sos'), noise)
    hum = 0.4 * np.sin(2 * math.pi * 62 * tt) + 0.2 * np.sin(2 * math.pi * 124 * tt)
    env = np.minimum(1, tt / 0.8) * np.minimum(1, (tt[-1] - tt) / 0.8)
    return (low * 3.0 * (0.3 + chop) + hum * chop) * env * 0.12


def slam():
    """The van's doors slammed: a hard low thud with a short metallic ring."""
    n = int(0.6 * SR)
    tt = np.arange(n) / SR
    thud = np.sin(2 * math.pi * 70 * tt) * np.exp(-tt * 18)
    ring = 0.3 * np.sin(2 * math.pi * 410 * tt) * np.exp(-tt * 22) + 0.2 * np.sin(2 * math.pi * 655 * tt) * np.exp(-tt * 30)
    rng = np.random.default_rng(7)
    click = rng.standard_normal(n) * np.exp(-tt * 120) * 0.5
    return (thud + ring + click) * 0.6


def engine(n):
    """The van pulling away hard: an engine's growl rising in pitch as it speeds off, fading into the distance."""
    tt = np.arange(n) / SR
    f = 55 + 70 * np.minimum(1, tt / 1.2)
    ph = 2 * math.pi * np.cumsum(f) / SR
    tone = np.sign(np.sin(ph)) * 0.25 + 0.5 * np.sin(ph * 2)
    from scipy.signal import butter, sosfilt
    tone = sosfilt(butter(2, 900, 'lp', fs=SR, output='sos'), tone)
    env = np.minimum(1, tt / 0.15) * np.exp(-np.maximum(0, tt - 0.9) * 1.6)
    return tone * env * 0.35


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)
    for ln in LINES[1:]:
        s = int(ln['start'] * SR)
        seg = ln['_voice'][:max(0, n - s)]
        voice[s:s + len(seg)] += seg
    ch = chant_crowd()
    s = int(max(0, LINES[0]['start']) * SR)
    cut = int(max(0, -LINES[0]['start']) * SR)
    seg = ch[cut:cut + n - s]
    fade = np.ones(len(seg))
    stop = int((shot_start('super') - 0.1 - max(0, LINES[0]['start'])) * SR)       # the chant dies under the close
    if 0 < stop < len(seg):
        fade[stop:] = np.maximum(0, 1 - np.arange(len(seg) - stop) / (0.4 * SR))
    rest[s:s + len(seg)] += seg * fade * 0.8
    a, b = int(ROPE_DROP[0] * SR) - int(0.6 * SR), int(SLAM[0] * SR)     # overhead until the doors slam
    rest[a:b] += heli(a, b)
    filmkit.place(rest, slam(), SLAM[1], SR)
    i = int((DRIVE + 0.1) * SR)
    e = engine(int(shot_start('interro') * SR) - i)                       # ends with the square (the cut)
    e[-int(0.15 * SR):] *= np.linspace(1, 0, int(0.15 * SR))
    rest[i:i + len(e)] += e[:n - i]
    mix = voice + rest
    end = int(BLACK_AT * SR)
    mix, g = MA.master(mix, end)
    voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


# ------------------------------------------------------------------------------------------------ checks
def checks():
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    faults = []
    windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES[1:] for a, b in ln['_stretches']]
    faults += E.check_mouths(sorted(x for w in TRACK for x in TRACK[w]), windows)
    mix, voice, rest = soundtrack(stems=True)
    faults += filmkit.voice_balance(voice, rest, SR, windows)
    faults += filmkit.hiss_check(mix, SR, BLACK_AT)
    if any('ACTION' in c.upper() for _, _, c in _chunks()):
        faults.append('the words Palestine Action appear in a subtitle')
    for q in filmkit.sound_questions({'voice': voice, 'background': rest, 'mix': mix}, SR,
                                     cuts=[a for _, a, _ in SHOTS[1:]], end=BLACK_AT):
        print('QUESTION FOR SAM:', q)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


def hidden_check(step=1):
    """The rest of her placard is never seen (Sam, 20 Oct: it says Palestine Action, only implied). Every frame she
    holds it in shot: its unlettered part painted magenta, the whole frame drawn, and any magenta left in the frame is
    a fault (the frame's edge or the people and boards in front must hide it all)."""
    C.HIDDEN_TEST[0] = True
    faults = []
    try:
        for name, a, b in SHOTS:
            if name not in ('wide', 'gran', 'police', 'storm'):
                continue
            for i in range(int(a * FPS), int(min(b, LIFT[0]) * FPS), step):
                t = i / FPS
                im = np.asarray(picture(t).convert('RGB')).astype(int)
                mag = (im[..., 0] > 230) & (im[..., 1] < 40) & (im[..., 2] > 230)
                n = int(mag.sum())
                if n > 20 * B.SS * B.SS:
                    faults.append(f'{t:.2f} s ({name}): {n} pixels of the hidden part of her placard show')
    finally:
        C.HIDDEN_TEST[0] = False
    return faults


def stills_sheet(out, times):
    tiles = []
    for t in times:
        tiles.append(frame_image(t).convert('RGB').resize((270, 480)))
    cols = min(6, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 270, rows * 480), (255, 255, 255))
    for i, tile in enumerate(tiles):
        sheet.paste(tile, ((i % cols) * 270, (i // cols) * 480))
    sheet.save(out, quality=88)


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        C.cast_sheet(a[1])
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'sheet':
        B.SS = 1
        ts = [float(x) for x in a[2:]] or [(s[1] + s[2]) / 2 for s in SHOTS]
        stills_sheet(a[1], ts)
    elif a[0] == 'check':
        B.SS = 1
        checks()
        f = hidden_check(2 if '--quick' in a else 1)
        print('\n'.join('HIDDEN: ' + x for x in f) or 'hidden part: never seen')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None)


if __name__ == '__main__':
    main()
