#!/usr/bin/env python3
"""Halo No-No (notes/halo-no-no.md): Elon Musk, in Master Chief's armour, flies a Roadster armada at the Halo ring
with anime Cortana. Started from source/satire_template.py. The cast is source/halo_cast.py, the places
source/halo_sets.py (flat paintings, rule 39); the armada is the Roadster film's white car (roadster.car), flown in
3D through each painting's camera.

    python3 source/halo_no_no.py cast OUT.jpg                the cast sheet (halo_cast)
    python3 source/halo_no_no.py sets OUT.jpg                the sets beside Sam's references (halo_sets)
    python3 source/halo_no_no.py stills OUT_DIR T [T ...]    stills at these times (seconds)
    python3 source/halo_no_no.py sheet OUT.jpg [T ...]       one labelled stills sheet (default: the key beats)
    python3 source/halo_no_no.py check                       the plan checks and the audit (also run by preflight.py)
    python3 source/halo_no_no.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1] [--nostamp]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402  flat shapes, black outlines
import figure as F               # noqa: E402  arms solved and guarded
import mouths                    # noqa: E402  lip sync
import mossad_audio as MA        # noqa: E402  recordings cleaned and levelled
import peepee as PP              # noqa: E402  the series' caption
import filmkit                   # noqa: E402  the general checks
import film_engine as E          # noqa: E402  render with the picture cache, subtitle list, mouth check
from satire_style import rough   # noqa: E402
from ed import INK               # noqa: E402

FPS, SR = 12, MA.SR

# =============================================== STORY ==============================================================
import halo_cast as HC           # noqa: E402  Musk in the armour, anime Cortana
import halo_sets as HS           # noqa: E402  the space wide, the ring close-up, the cabin
import roadster as RD            # noqa: E402  the white Roadster (the armada)

NAME = 'halo-no-no'
NOTES = os.path.join(os.path.dirname(HERE), 'notes', 'halo-no-no.md')
TITLE = ()                                        # no title (Sam, 15 Oct)
TITLE_AT = dict(cap=116, top=310)
CAST = {'musk': dict(name='Musk'), 'cortana': dict(name='Cortana')}
LOOKS_AT = {'cortana': 'musk'}                    # Musk looks out at the lens (rule 43: the plan's eyelines)
THEME = os.path.join(HERE, 'audio', 'halo-theme.mp3')
THEME_FROM = 27.5                                 # the film starts at 0:27.5 of the theme (Sam, 30 Oct: 4 s later in the song)
# Lines by number (never by position). Times are the plan's guesses until Sam's recordings arrive (Sam, 29 Oct:
# build and time from the script with subtitles first).
LINES = [
    dict(n=1, who='radio', text="Musker Chief, you mind telling me what you're doing in that Roadster?", start=8.9,
         end=13.2, audio='halo-no-no-radio', radio=True,
         chunks=['Musker Chief,', 'you mind telling me', "what you're doing", 'in that Roadster?']),
    dict(n=2, who='musk', text='Sir, finishing this fight.', start=13.4, end=16.1, audio='halo-no-no-musk-1',
         chunks=['Sir, finishing this fight.']),
    dict(n=3, who='musk', text="If we don't stop Zelensky from using the Halo, all life on Earth could be wiped out.",
         start=16.5, end=21.8, audio='halo-no-no-musk-2',
         chunks=["If we don't stop Zelensky", 'from using the Halo,', 'all life on Earth could be wiped out.']),
    dict(n=4, who='cortana', text="Oh, Musker Chief, we're going to make him look like such Le Epic Chungus!! Kawaiii!!",
         start=23.4, end=31.2, audio='halo-no-no-cortana-1',
         chunks=['Oh, Musker Chief,', "we're going to make him", 'look like such', 'Le Epic Chungus!!', 'Kawaiii!!']),
    dict(n=5, who='musk', text='We sure will, Breeder 04.', start=31.7, end=34.1, audio='halo-no-no-musk-3',
         chunks=['We sure will,', 'Breeder 04.']),
    dict(n=6, who='cortana', text='Musk-San, please let me die.', start=35.9, end=39.2, audio='halo-no-no-cortana-2',
         chunks=['Musk-San,', 'please let me die.']),
    dict(n=7, who='musk', text='No.', start=40.1, end=41.0, audio='halo-no-no-musk-4', chunks=['No.']),
]
SHOTS = [   # (shot, start, end)
    ('s1', 0.0, 8.5),     # the wide: planet, ring, galaxy; the armada streams in at 4.5 (0:28 of the theme in the brief; Sam moved the song 4 s on, 30 Oct: now 0:32)
    ('s2', 8.5, 16.4),   # the cabin from the windscreen: Musk at the yoke; the radio; "Sir, finishing this fight."
    ('s3', 16.4, 22.1),   # hard cut to Musk close: "If we don't stop Zelensky..."
    ('s4', 22.1, 31.5),   # the cabin: the discharge, Cortana appears over the passenger seat; her Chungus line
    ('s5', 31.5, 34.4),   # Musk close, a glance at her: "We sure will, Breeder 04."
    ('s6', 34.4, 42.3),   # the ring close-up (Showstopper Shot): the armada skims the hull; the last two lines
]
CAMS = {'s1': 'space', 's2': 'wide', 's3': 'close', 's4': 'wide', 's5': 'close', 's6': 'ring'}
SHOT_CAST = {'s2': ['musk'], 's3': ['musk'], 's4': ['musk', 'cortana'], 's5': ['musk']}
DUR = 42.3
# Rule 1: the cabin in metres (x across the car, + to the driver's side; z from the windscreen back; y up). The space
# shots are paintings with their own cameras (halo_sets: the wide's vanishing point, the ring's RingCam).
PLAN = dict(
    CEIL=1.15,
    ROOMS={'cabin': (-0.72, 0.0, 0.72, 1.6)},
    OPENINGS={'rear window': dict(wall=('z', 1.6), span=(-0.58, 0.58), sill=0.62, head=1.08, to='space')},
    THINGS={'driver seat': dict(at=(0.37, 1.05), size=(0.54, 0.55, 1.1), facing=180),
            'passenger seat': dict(at=(-0.37, 1.05), size=(0.54, 0.55, 1.1), facing=180),
            'console': dict(at=(0.0, 0.8), size=(0.16, 0.9, 0.5), facing=0),
            'dash': dict(at=(0.0, 0.15), size=(1.44, 0.3, 0.8), facing=0),
            'roof glass': dict(at=(0.0, 0.8), size=(1.1, 1.2, 0.02), y=1.13, facing=0, solid=False,
                               why='two black glass panels overhead onto space (the plan has openings in walls only)')},
    PEOPLE={'musk': dict(at=(0.37, 0.95), facing=180, who='musk', seated=True, on='driver seat'),
            'cortana': dict(at=(-0.37, 0.9), facing=180, who='cortana', floating=0.75, on='passenger seat')},
    CAMS={'s1': dict(pos=(-30.0, 0.0, -200.0), look=(0.0, 0.0, 0.0), outside=True),   # the space painting
          's2': dict(pos=(0.0, 1.0, 0.0), look=(0.0, 0.9, 1.6)), 's4': dict(pos=(0.0, 1.0, 0.0), look=(0.0, 0.9, 1.6)),
          's3': dict(pos=(0.37, 1.25, 0.25), look=(0.37, 1.25, 1.0)),
          's5': dict(pos=(0.37, 1.25, 0.25), look=(0.37, 1.25, 1.0)),
          's6': dict(pos=(0.0, 50.0, -300.0), look=(0.0, 0.0, 0.0), outside=True)},       # the ring painting
    SHOT_MARKS={'s2': ['musk'], 's3': ['musk'], 's4': ['musk', 'cortana'], 's5': ['musk']},
    GROUPS={'armada': dict(arriving='the lead car alone, then the rest in a loose wedge, some spinning nose over tail',
                           stopped='never stops', leaving='streams away towards the planet (s1), along the hull (s6)')},
)
REFS = 'references/halo-no-no/'
BENCHMARK = [   # rule 3: the full lists are in the notes ("Benchmarks"); the sheet is `halo_sets.py sheet`
    dict(place='space wide', refs=[REFS + '01.jpg'], at=3.0,
         items=[('big orange-brown planet on the left', 'banded, blotched, one outline'),
                ('night side top-left', 'dusk band then night side'), ('thin dark ring in front of its lower half', 'yes'),
                ('the galaxy back right', "ref 02's blue stripe (Sam, note 5)"), ('nebula', 'flat lumps'),
                ('dense stars', 'round dots'), ('room for the Hook Text and caption', 'dark sky top, lower third'),
                ('a lane for the armada', 'the right side')]),
    dict(place='ring close-up', refs=[REFS + '02.jpg'], at=36.5,
         items=[('dark hull sweeping top left to lower right', 'a true circle projected'), ('panels, ports, lights', 'yes'),
                ('far side rising as seas, land, cloud', 'yes, grey rim walls'), ('planet behind left', 'lower left'),
                ('blue galaxy band top right', 'yes'), ('stars and nebula', 'yes'), ('no car shadows', 'Sam, 29 Oct'),
                ('room for the cars', 'the stream from the top down to the bend')]),
    dict(place='the cabin', refs=[REFS + r for r in ('03.jpg', '04.jpg', '05.jpg')], at=10.5,
         items=[('white sport seats', 'yes'), ('ROADSTER plates', 'yes'), ('black glass roof', 'yes'),
                ('black console and screen', 'yes'), ('red trim light', 'doors, bulkhead, dash'), ('black yoke', 'yes'),
                ('rear window onto space', 'with a Roadster drifting past'), ('doors and dash detail', 'yes')]),
]
HOOK = ('Elon Finishes The Fight', {'y': 330, 'until': 3.5})   # Sam, 29 Oct: upper middle, 0-3.5 s
CAPTION_1 = ('Halo Ringworld', 'Russia - Ukraine War')         # white bold, lower third, 0.5-4 s (the brief)
KEEP_CLEAR = []
PROP_SIZES = []
OUTFIT, HEIGHTS = {}, {'musk': 2.1, 'cortana': 0.85}
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
ALLOWED_CONTACTS = [('musk.hand*', 'YOKE', 8.5, 34.4, 'his hands on the yoke the whole time (the brief)')]
ALLOWED_MOUTHS = []
ALLOWED_POPS = [('cortana', 22.5, 23.6, 'she forms out of the discharge (the brief)'),
                ('cortana', 30.4, 30.6, 'her poses snap on her words (the brief: overemphasised): side on to turned away')]
SET_EXCLUDE = [('driver seat', 'Musk sits in it (the cabin is one flat painting, drawn behind him)'),
               ('passenger seat', 'Cortana hangs in mid-air in front of it (painted behind her)')]
TOUCHES = [('musk.handL', 'YOKE', 8.5, 34.4, 'turning the yoke'), ('musk.handR', 'YOKE', 8.5, 34.4, 'turning the yoke')]
FREE_MOVES = [('ARMADA', 3.8, 8.5, 'the cars fly'), ('ARMADA', 34.4, 42.3, 'the cars fly')]
SOUND_SOURCES = {}
EFFECTS = []                                      # filled in below the drawing code (each drawn alone, rule 15)
JOKE_PROPS = []
THREE_QUARTER_OK = [('s4', 'cortana thrust', 'the brief: shoving her chest at him (side on, facing him)'),
                    ('s4', 'cortana turn', 'the brief: showing her behind (from the back, looking back at him)')]
# ====================================================================================================================

BLACK_AT = DUR
WHO = ('musk', 'cortana')
for ln in LINES:                                  # time each line to its recording when there is one
    ln['_voice'], ln['_stretches'] = None, [(0.0, ln['end'] - ln['start'])]
    if ln.get('audio') and os.path.exists(os.path.join(HERE, 'audio', ln['audio'] + '.m4a')):
        v = MA.line(ln['audio'])
        ln['_voice'], ln['end'] = v, ln['start'] + len(v) / SR
        ln['_stretches'] = MA.pauses(v, 0.12)
TRACK = {w: [(a + ln['start'], b + ln['start'], sh) for ln in LINES if ln['who'] == w
             for a, b, sh in mouths.track(ln['text'], ln['_stretches'])] for w in WHO}
LINE = {ln['n']: ln for ln in LINES}


def S0(name):
    return next(a for s, a, _ in SHOTS if s == name)


def S1(name):
    return next(b for s, _, b in SHOTS if s == name)


def chunk_times(ln):
    """Each subtitle chunk comes up on its first word (Sam, 16 Oct). Until the recording is in, the words are spread
    over the line by their syllables (a placeholder, never final)."""
    chunks = ln.get('chunks') or [ln['text']]
    syl = [sum(mouths._syllables(w) for w in c.split()) for c in chunks]
    tot = float(sum(syl)) or 1.0
    out, acc = [], 0
    for c, n in zip(chunks, syl):
        out.append((ln['start'] + 0.1 + (ln['end'] - ln['start']) * acc / tot, c))
        acc += n
    return out


SUB_EARLIER = {(4, 2): 0.5, (4, 3): 0.5, (4, 4): 0.5, (6, 1): -0.5}          # Sam, 31 Oct: "look like such" and "Kawaiii!!" come up 0.5 s sooner (subtitles only; her poses keep their times); 31 Oct: "Le Epic Chungus" 0.5 s sooner, "please let me die" 0.5 s later
CHUNKS = [(t - SUB_EARLIER.get((ln['n'], i), 0.0), c, ln) for ln in LINES for i, (t, c) in enumerate(chunk_times(ln))]


def chunk_at(n, i):
    return chunk_times(LINE[n])[i][0]


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def cam_for(t):
    k = CAMS[shot_of(t)]
    return HS.cam_close() if k == 'close' else HS.cam_wide()


# ------------------------------------------------------------------------------------------------ Musk
T_FLASH = 22.6                                    # the digital discharge (shot 4)
GLANCE = (31.95, 32.95)                           # "We sure will": a glance to her side, then back out at the lens
_BL = F.blinks(17, S0('s2'), S1('s5'), talking=True)
BLINKS = {'musk': [b for b in _BL if not (GLANCE[0] - 0.3 <= b <= GLANCE[1])],   # never on the glance
          'cortana': F.blinks(29, T_FLASH + 1.0, S1('s4'), talking=True)}


def _yoke_keys():
    """Turning the yoke back and forth (the brief): a held angle, then a turn the other way, each its own size and
    timing (never a looping sway)."""
    r = np.random.default_rng(9)
    t, a, keys, sg = S0('s2'), 0.0, [], 1
    keys.append((t, 0.0))
    while t < S1('s5'):
        t += r.uniform(0.35, 0.8)
        keys.append((t, a))                                     # hold
        a = sg * r.uniform(10, 24)
        t += r.uniform(0.55, 0.85)
        keys.append((t, a))                                     # the turn, eased in and out
        sg = -sg
    return keys


YOKE_KEYS = _yoke_keys()


def _ease(u):
    return u * u * (3 - 2 * u)


def yoke_turn(t):
    for (t0, a0), (t1, a1) in zip(YOKE_KEYS, YOKE_KEYS[1:]):
        if t0 <= t < t1:
            return a0 + (a1 - a0) * _ease((t - t0) / (t1 - t0))
    return YOKE_KEYS[-1][1]


def musk_state(t):
    shape = mouths.at(TRACK['musk'], t) or 'rest'
    look = -1.0 if GLANCE[0] <= t < GLANCE[1] else 0.0          # the eyes jump (filmkit.glance), never eased
    lean = filmkit.shifts(t, seed=3, amount=1.6)                # small quick weight shifts in the seat (degrees)
    return dict(mouth=shape, look=look, blink=F.blinking(t, BLINKS['musk']), turn=yoke_turn(t), lean=lean)


# ------------------------------------------------------------------------------------------------ Cortana
C_SCALE = 0.446                                   # as on the approved cast sheet (about 0.8 m), in mid-air over the seat


def cortana_pose(t):
    """Her poses snap on her words (all overemphasised and enthusiastic, the brief): arriving with arms flung up; the
    point at him on "Oh, Musker Chief"; fists by her cheeks; the thrust at him on "Le Epic Chungus"; turned away,
    looking back over her shoulder, on "Kawaiii"."""
    c = chunk_times(LINE[4])
    if t < c[0][0]:
        return 'appear', dict(mouth='O' if t < T_FLASH + 0.9 else 'smile')
    if t < c[1][0]:
        return 'point', dict(hip=-0.8)
    if t < c[3][0]:
        return 'kawaii', dict(chest=0.6, wink=c[2][0] <= t < c[2][0] + 0.6)
    if t < c[4][0]:
        return 'thrust', dict(lean=-5, wink=True)
    return 'turn', dict()


def cortana_state(t):
    pose, extra = cortana_pose(t)
    shape = mouths.at(TRACK['cortana'], t)
    st = dict(pose=pose, look=1.0, blink=F.blinking(t, BLINKS['cortana']),
              appear=min(1.0, max(0.0, (t - T_FLASH - 0.08) / 0.8)),
              flicker=0.4 if int(t * FPS) % 23 == 7 else 0.0)
    st.update(extra)
    if shape and shape != 'rest':
        st['mouth'] = shape
    st.setdefault('mouth', 'smile')
    eye = (HS.CORTANA_AT[0], cortana_y(t) - 150 * C_SCALE)
    filmkit.eyeline('cortana', t, eye, (st['look'], 0.0), (HS.MUSK[0], HS.MUSK[1] - 150 * HS.MUSK[2]))
    return st


def cortana_y(t):
    """She hangs in mid-air: a small quick bob now and then (a held height between, never a sine float)."""
    return HS.CORTANA_AT[1] + 40 + 12 * filmkit.shifts(t, seed=11, amount=1.0)   # her feet clear of the cushion


def discharge(img, cam, t):
    """The digital discharge (the brief): one frame of a big lumpy flash, then pixel crackle (small square sparks,
    blue and white) round where she forms, dying away over 0.9 s."""
    x, y = HS.CORTANA_AT[0], HS.CORTANA_AT[1] + 140
    p = B.Pen(img, cam)
    if T_FLASH <= t < T_FLASH + 1.0 / FPS:
        _flash(p, x, y, 300, int(t * 100))
    k = (t - T_FLASH) / 0.9
    if 0 <= k < 1:
        r = np.random.default_rng(int(t * FPS) + 3)
        for _ in range(int(90 * (1 - k)) + 6):
            a, d = r.uniform(0, 2 * math.pi), abs(r.normal(0, 150))
            px, py = x + d * math.cos(a), y + d * math.sin(a) * 1.5
            s = r.choice([6, 9, 12, 16])
            col = [(255, 255, 255), (160, 220, 255), (90, 170, 255)][r.integers(3)]
            p.poly([(px, py), (px + s, py), (px + s, py + s), (px, py + s)], col, None)


def _flash(p, x, y, R, seed):
    """A lumpy burst (house style: no star, no glow): white in the middle, pale blue round it, one outline."""
    r = np.random.default_rng(seed)
    for k, col in ((1.0, (150, 210, 255)), (0.62, (255, 255, 255))):
        pts = []
        for i in range(22):
            a = 2 * math.pi * i / 22
            rr = R * k * r.uniform(0.7, 1.0)
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a) * 1.2))
        from ed import curve
        p.poly(curve(pts, 3), col, INK if k == 1.0 else None, 3)


# ------------------------------------------------------------------------------------------------ the armada
VP = (360, 1080)                                  # shot 1: where the armada heads (by the ring, in front of the planet)
F1 = 1100.0                                       # shot 1's focal length (px), for the view angle on each car
T_ARMADA = 4.5                                    # 0:28 of the theme (the brief)


def _armada_1():
    """About 15 cars (Sam, 29 Oct), in arrowheads (Sam, 30 Oct): a V of 5 first, then a V of 3 high up and a V of 3 low
    down, each arriving at its own time; four lone cars spinning nose over tail like in Roadster, spread out between
    them. A V flies as one, level: the point car in front, each pair a step behind it and out to the sides. Each car:
    (enter time, offset at depth 1, start depth, speed in depth a second, spin degrees a second)."""
    cars = []
    #            enter    across  up/down  depth  speed   the V's size
    for te, X, Y, z0, v, n in ((T_ARMADA, 660, -40, 0.66, 0.55, 5),
                               (T_ARMADA + 1.3, 640, -330, 0.68, 0.58, 3),
                               (T_ARMADA + 2.2, 620, 260, 0.64, 0.52, 3)):
        for k in range(n):       # 0: the point; then a pair a row (Sam, 30 Oct: flat, level with it), out to each side
            row, side = (k + 1) // 2, (-1) ** k              # and a step behind it (nearer us: it flies away from us)
            cars.append(dict(te=te, off=(X + side * 170 * row, Y + 75 * row), z0=z0 - 0.07 * row, v=v, spin=0.0))
                                                           # seen a little from above: each pair a step lower: a ^
    for te, X, Y, z0, v, spin in ((T_ARMADA + 0.7, 520, 330, 0.66, 0.60, 220),     # the lone spinners
                                  (T_ARMADA + 1.8, 380, -170, 0.70, 0.50, -260),
                                  (T_ARMADA + 2.9, 560, 60, 0.64, 0.62, 170),
                                  (T_ARMADA + 3.1, 450, -420, 0.72, 0.56, -200)):
        cars.append(dict(te=te, off=(X, Y), z0=z0, v=v, spin=spin))
    return cars


ARMADA_1 = _armada_1()


def armada_1(img, cam, t):
    out = []
    for c in ARMADA_1:
        z = c['z0'] + c['v'] * (t - c['te'])     # before te it is nearer us, off the right edge, flying in
        if z < 0.12:
            continue
        x, y = VP[0] + c['off'][0] / z, VP[1] + c['off'][1] / z
        out.append((z, x, y, c))
    for z, x, y, c in sorted(out, key=lambda q: -q[0]):
        s = 0.42 / z
        yaw = 270 - math.degrees(math.atan((x - VP[0]) / F1))
        elev = 6 + math.degrees(math.atan((y - VP[1]) / F1))
        flip = c['spin'] * (t - c['te'])
        if x - 260 * s * 2 > 1080 + 40 or s < 0.02:
            continue
        RD.car(img, cam, x, y, s, RD.View(yaw=yaw, elev=elev, flip=flip), jets=0.55, t=t,
               smoke=False)      # the jets on, as in Roadster (Sam, 30 Oct), shorter here so the Vs read


def _armada_6():
    """About 8 cars (Sam, 29 Oct) skimming the hull in a loose stream, each at its own speed so the stream stretches:
    big and near as they pass over us, shrinking towards the ring's bend. Each: angle along the ring at the shot's
    start (degrees), speed (degrees a second), height off the hull, place across it, spin."""
    return [dict(th=2.0, w=1.8, lift=0.030, h=-0.045, spin=0), dict(th=4.5, w=2.2, lift=0.040, h=-0.055, spin=0),
            dict(th=7.0, w=1.6, lift=0.022, h=-0.042, spin=0), dict(th=10.5, w=2.0, lift=0.034, h=-0.050, spin=200),
            dict(th=0.4, w=2.4, lift=0.026, h=-0.044, spin=0), dict(th=-2.0, w=2.6, lift=0.038, h=-0.053, spin=-240),
            dict(th=-5.0, w=2.2, lift=0.024, h=-0.043, spin=0), dict(th=-9.0, w=2.8, lift=0.032, h=-0.048, spin=180)]


ARMADA_6 = _armada_6()
RC = HS.RingCam(**HS.RING_CAM)


def _ring_view(th, flip):
    """A car on the ring: nose along the ring (the way it flies), roof out from the hull, seen through the ring's camera
    (its roll included), as a roadster.View."""
    T = np.array([-math.sin(th), math.cos(th), 0.0])
    Rr = np.array([math.cos(th), math.sin(th), 0.0])
    Lf = np.cross(Rr, T)
    # roof up the screen, wheels and jets down (Sam, 31 Oct: they flew upside down); turned 50 degrees about the roof
    # so the camera sees the car's side and the jets leave its underside (end on, from behind, the plumes read as
    # coming off its end)
    Mc = np.stack([T, -Lf, -Rr], 1) @ RD.rot('z', math.radians(50)) @ RD.rot('y', math.radians(flip))
    c, s = RC.c, RC.s
    right = -RC.Rt * c + RC.U * s
    up = RC.Rt * s + RC.U * c
    A = np.stack([right, RC.F, up])
    v = RD.View()
    v.R, v.Rc = A @ Mc, Mc
    return v


def armada_6(img, cam, t):
    out = []
    for c in ARMADA_6:
        th = math.radians(c['th'] + c['w'] * (t - S0('s6')))
        if not math.radians(1.0) < th < math.radians(40):
            continue
        q = RC(HS.ring_point(th, c['h'], c['lift']))
        if q is None:
            continue
        (x, y), z = q
        out.append((z, x, y, th, c))
    for z, x, y, th, c in sorted(out, key=lambda q: -q[0]):
        # seen from behind and a little above, nose the way it flies, roof up, jets under it (Sam, 31 Oct, twice: the
        # ring's own frame tipped their roofs away from us, so we saw their undersides and the plumes read as
        # leaving their ends); the spinners tumble nose over tail as before
        RD.car(img, cam, x, y, 0.034 / z, RD.View(yaw=-80, elev=22, flip=c['spin'] * (t - S0('s6'))),
               jets=1.0, t=t, smoke=False)      # the four jets on, as in Roadster (Sam, 30 Oct)


# ------------------------------------------------------------------------------------------------ the picture
_PAINT = {}


def _painting(key, make):
    k = (key, B.SS)
    if k not in _PAINT:
        _PAINT[k] = make()
    return _PAINT[k].copy()


def drift_at(t):
    """The approved passer-by (Sam, 29 Oct): one Roadster from the armada drifting across the rear window."""
    u = (t - 9.5) / 6.5
    return u if 0 <= u <= 1 else None


def radio_light(t):
    """A small light by the speaker comes on while the radio voice speaks (Sam, 30 Oct: so we know it is an outside
    signal), from his first word to his last."""
    ln = LINE[1]
    return ln['start'] + ln['_stretches'][0][0] <= t < ln['start'] + ln['_stretches'][-1][1]


def picture(t):
    """The frame WITHOUT captions (those go on last, so wording notes never re-render a picture)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    sh, cam = shot_of(t), cam_for(t)
    if sh == 's1':
        img = _painting('space', HS.space_wide)
        armada_1(img, cam, t)
        return img
    if sh == 's6':
        img = _painting('ring', HS.ring_close)
        armada_6(img, cam, t)
        return img
    img = B.canvas(HS.SPACE)
    HS.cabin_back(img, cam, t, drift_at(t), radio_light(t))
    HC.chief(img, cam, *HS.MUSK, musk_state(t), t)
    if sh == 's4' and t >= T_FLASH:
        HC.cortana(img, cam, HS.CORTANA_AT[0], cortana_y(t), C_SCALE, cortana_state(t), t)
        discharge(img, cam, t)
    HS.cabin_front(img, cam)
    return img


def caption_at(t):
    for i, (a, c, ln) in enumerate(CHUNKS):
        nxt = CHUNKS[i + 1][0] if i + 1 < len(CHUNKS) else 1e9
        if a <= t < min(nxt, ln['end'] + 0.35):
            return c
    return None


def place_caption(img, t):
    """Shot 1's white bold caption (the brief), lower third, 0.5-4 s, under the Hook Text's area."""
    if not 0.5 <= t < 4.0:
        return
    cam = B.Cam(1.0, 540, 960)
    for i, s in enumerate(CAPTION_1):         # the second line fades in half a second after the first (Sam, 30 Oct)
        a = max(0.0, min(1.0, (t - 0.5 - 0.5 * i) / 0.25, (4.0 - t) / 0.25))   # both fade out together
        if a <= 0:
            continue
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        B.text(lay, cam, 540, 1440 + i * 84, s, 64 if i == 0 else 52, (255, 255, 255), font=HC.SANS, anchor='ma',
               stroke=3, stroke_fill=(0, 0, 0))
        if a < 1:
            lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
        img.alpha_composite(lay)


def overlay(img, t):
    if t < BLACK_AT:
        place_caption(img, t)
        c = caption_at(t)
        if c:
            PP.caption(img, c)
    return img


def frame_image(t):
    return overlay(picture(t), t)


# ------------------------------------------------------------------------------------------------ sound
def radio(v):
    """Through the radio (the brief): a telephone band (300-3,400 Hz) and a little grit."""
    from scipy.signal import butter, sosfilt
    y = sosfilt(butter(4, [300, 3400], 'band', fs=SR, output='sos'), v)
    y = np.tanh(y * 3.0) / 3.0
    return y * (np.abs(v).max() / (np.abs(y).max() + 1e-9))


SPACE_SHOTS = ('s1', 's6')


def music_gain(n):
    """The theme never stops (Sam, 29 Oct): loud in the space shots, quieter but noticeable in the cabin, easing down
    and up over 0.3 s at each cut; under every line it dips so the voice stays 6 dB clear."""
    g = np.zeros(n)
    for name, a, b in SHOTS:
        g[int(a * SR):int(b * SR)] = 1.0 if name in SPACE_SHOTS else 10 ** (-11 / 20)
    g[int(DUR * SR):] = g[int(DUR * SR) - 1]
    k = np.hanning(int(0.3 * SR))
    g = np.convolve(g, k / k.sum(), 'same')
    for ln in LINES:
        space = CAMS[shot_of(ln['start'])] in ('space', 'ring')
        if True:
            duck = np.ones(n)
            duck[int((ln['start'] - 0.2) * SR):int((ln['end'] + 0.2) * SR)] = 10 ** ((-10 if space else -4) / 20)
            g *= np.convolve(duck, k / k.sum(), 'same')
    return g


def soundtrack(stems=False):
    from burnham_film import load
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)
    for ln in LINES:
        if ln['_voice'] is not None:
            v = radio(ln['_voice']) if ln.get('radio') else ln['_voice']
            s = int(ln['start'] * SR)
            seg = v[:max(0, n - s)]
            voice[s:s + len(seg)] += seg
    theme = load(THEME)[int(THEME_FROM * SR):]
    m = np.zeros(n)
    m[:min(n, len(theme))] = theme[:n]
    m *= 10 ** ((MA.LINE_LUFS - 3 - MA.lufs(m[:int(DUR * SR)])) / 20)    # the space level, a little under the voices
    rest += m * music_gain(n)
    end = int(BLACK_AT * SR)
    f = int(0.4 * SR)
    rest[end - f:end] *= np.linspace(1, 0, f)                  # into the sign-off
    mix = voice + rest
    mix, g = MA.master(mix, end)
    voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


# ------------------------------------------------------------------------------------------------ checks
def checks():
    """Plan checks: seconds. Raises on the first batch of faults; prints the subtitles to proofread."""
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    faults = []
    windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES if ln['who'] in WHO for a, b in ln['_stretches']]
    faults += E.check_mouths(sorted(x for w in WHO for x in TRACK[w]), windows)
    if any(ln['_voice'] is not None for ln in LINES):
        _, voice, rest = soundtrack(stems=True)
        allw = [(ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches']]
        faults += filmkit.voice_balance(voice, rest, SR, allw)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


def mouths_seen(t):
    """Every face on screen at t with its mouth as drawn (voices.py, rule 7)."""
    sh = shot_of(t)
    out = []
    if sh in ('s2', 's3', 's4', 's5'):
        z = cam_for(t).z
        out.append(('musk', musk_state(t)['mouth'], 0.0, 300 * HS.MUSK[2] * z))
        if sh == 's4' and t >= T_FLASH + 0.9:
            st = cortana_state(t)
            out.append(('cortana', st['mouth'], 0.0 if st['pose'] in ('point', 'kawaii', 'appear') else 90.0,
                        300 * C_SCALE * z))
    return out


CUSHION_M = 0.3                                    # the cushion top, metres off the cabin floor (HS.CUSHION_Y on screen)


def project(cam, P):
    """Plan metres (x across, + the driver's side; y up; z back from the windscreen) to the frame: the cabin painting's
    scale (HS.PX_M) at the seats, then the shot's camera."""
    X = (HS.SEAT_X['driver'] + HS.SEAT_X['passenger']) / 2 + P[:, 0] * HS.PX_M
    Y = HS.CUSHION_Y - (P[:, 1] - CUSHION_M) * HS.PX_M
    return (X - cam.cx) * cam.z + 540, (Y - cam.cy) * cam.z + 960, P[:, 2] + 1.0


def _to_m(x, y, z):
    """A point of the wide framing (pixels) at depth z (metres) into plan metres."""
    mid = (HS.SEAT_X['driver'] + HS.SEAT_X['passenger']) / 2
    return ((x - mid) / HS.PX_M, CUSHION_M + (HS.CUSHION_Y - y) / HS.PX_M, z)


def scene(t):
    """Everyone solid at time t (audit.py, rules 5 and 6), in the plan's metres. Musk sits with his gloves on the yoke
    (the yoke a little in front of him); Cortana hangs in mid-air in front of the passenger seat."""
    import clipcheck as CC
    import audit
    sh = shot_of(t)
    if CAMS[sh] not in ('wide', 'close'):
        return []
    out = []
    x, y, s = HS.MUSK
    zb, zh = PLAN['PEOPLE']['musk']['at'][1], 0.6                 # his body; his hands and the yoke, in front
    m = lambda px, py, z: _to_m(x + px * s, y + py * s, z)
    st = musk_state(t)
    sol = [CC.capsule('musk', 'body', m(0, 40, zb), _to_m(x, HS.CUSHION_Y - 30, zb), 180 * s / HS.PX_M),
           CC.sphere('musk', 'head', m(0, -150, zb), 120 * s / HS.PX_M)]
    arms = HC.chief_arms(st['turn'])
    grips = []
    for side in 'LR':
        el, wr, _ = arms[side]
        d = np.subtract(wr, el) / (np.linalg.norm(np.subtract(wr, el)) + 1e-9)
        hx, hy = wr[0] + d[0] * 26, wr[1] + d[1] * 26
        sol.append(CC.sphere('musk', 'hand' + side, m(hx, hy, zh), 34 * s / HS.PX_M))
        grips.append(m(*HC.yoke_grips(st['turn'])[side], zh))
    out.append(audit.Thing('musk', sol))
    out.append(audit.Thing('YOKE', [CC.capsule('YOKE', 'yoke', grips[0], grips[1], 0.02)]))
    if sh == 's4' and t >= T_FLASH:
        cx, cy = HS.CORTANA_AT[0], cortana_y(t)
        neck = _to_m(cx, cy, PLAN['PEOPLE']['cortana']['at'][1])
        f = HEIGHTS['cortana'] / 1.75
        out.append(audit.Thing('cortana', audit.simple('cortana', neck[0], neck[2], height=HEIGHTS['cortana'],
                                                       base=neck[1] - 1.41 * f)))
    return out


def audits():
    """The general audit: each person alone over every frame they are on screen (in pieces, popping, stretching,
    frozen), and the eyelines. Returns faults."""
    def alone(who):
        def draw(t):
            lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
            if who == 'musk':
                HC.chief(lay, cam_for(t), *HS.MUSK, musk_state(t), t)
            else:
                HC.cortana(lay, cam_for(t), HS.CORTANA_AT[0], cortana_y(t), C_SCALE, cortana_state(t), t)
            return lay
        return draw
    actors = {}
    for shot, a, b in SHOTS:
        for who in SHOT_CAST.get(shot, []):
            ts = [i / FPS for i in range(int(a * FPS), int(b * FPS))
                  if who == 'musk' or i / FPS >= T_FLASH + 0.9]          # she forms out of the discharge first
            if ts:
                actors[f'{who} [{shot}]'] = (ts, alone(who))
    filmkit.EYES.clear()
    snap = [('cortana [s4]', 30.4, 30.6, 'her poses snap on her words (the brief): side on to turned away')]
    faults = filmkit.silhouette_audit(actors, fps=FPS, still_ok=(), allow=snap)
    faults += filmkit.check_eyelines()
    return faults


def LINE_SUBJECTS():
    """Each of the cast alone, large, for the line-work check (linecheck.py)."""
    def musk(im):
        HC.chief(im, B.Cam(1.0, 540, 960), 540, 700, 1.1, dict(turn=0.0), 0.0)

    def cortana(im):
        HC.cortana(im, B.Cam(1.0, 540, 960), 540, 500, 0.9, dict(pose='point', hip=-0.8), 1.0)
    return [('musk', musk), ('cortana', cortana)]


EFFECTS[:] = [
    ('the digital discharge', 'burst', lambda im: _flash(B.Pen(im, B.Cam(1.0, 540, 960)), 540, 960, 300, 5)),
]


def cast_sheet(out):
    HC.sheet(out)


def stills_sheet(out, times):
    tiles = []
    f = ImageFont.truetype(HC.SANS, 18)
    for t in times:
        im = frame_image(t).convert('RGB').resize((360, 640), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 150, 30), fill=(0, 0, 0))
        d.text((6, 4), f'{shot_of(t)}  {t:.1f}s', fill=(255, 255, 255), font=f)
        tiles.append(im)
    cols = min(6, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 364 + 4, rows * 644 + 4), (255, 255, 255))
    for i, tile in enumerate(tiles):
        sheet.paste(tile, (4 + (i % cols) * 364, 4 + (i // cols) * 644))
    sheet.save(out, quality=86)
    print('wrote', out)


KEY_TIMES = [1.5, 4.8, 6.5, 8.0, 11.0, 15.0, 18.5, 22.6, 23.1, 24.1, 26.0, 28.0, 30.3, 32.3, 35.5, 38.0, 40.5]


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        cast_sheet(a[1])
    elif a[0] == 'sets':
        HS.sheet(a[1])
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'sheet':
        B.SS = 1
        stills_sheet(a[1], [float(x) for x in a[2:]] or KEY_TIMES)
    elif a[0] == 'check':
        B.SS = 1
        checks()
        import audit
        f = [x[len('AUDIT: '):] for x in audit.check(sys.modules[__name__])]
        print('\n'.join(['AUDIT: ' + x for x in f]) or 'audit: clean')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)


F.guard(B)   # every arm drawn is measured against the rig; a wrong one stops the render

if __name__ == '__main__':
    main()
