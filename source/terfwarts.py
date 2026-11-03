#!/usr/bin/env python3
"""Terfwarts (notes/terfwarts.md): the Sorting Hat calls Harry a BIOLOGICAL MALE; later Moaning Myrtle won't let
Harry and Ron into the girls' bathroom to save Hermione from the troll. Built from the satire template (guides/satire.md).

    python3 source/NAME.py cast OUT.png              the cast on one sheet: approve it before any animation
    python3 source/NAME.py stills OUT_DIR T [T ...]  stills at these times (seconds)
    python3 source/NAME.py check                     every check and the audit (also run by preflight.py)
    python3 source/NAME.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1] [--nostamp]
        --span: a clip of one moment (it carries a review stamp, the time and shot in the corner); --nostamp: no stamp,
        for a stretch rendered at full size to splice into a finished film (rule 47)
"""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402  people: flat shapes, black outlines
import mossad as M               # noqa: E402  (brows, mouths, hair; patched into burnham on import)
import figure as F               # noqa: E402  arms solved and guarded
import mouths                    # noqa: E402  lip sync
import mossad_audio as MA        # noqa: E402  recordings cleaned and levelled
import peepee as PP              # noqa: E402  the series' caption
import filmkit                   # noqa: E402  the general checks
import film_engine as E          # noqa: E402  render with the picture cache, subtitle list, mouth check
import terfwarts_cast as C       # noqa: E402  the cast and the Hat
import terfwarts_plan as PL      # noqa: E402  the world in metres
import views                     # noqa: E402
import moves                     # noqa: E402
import posegallery as PG         # noqa: E402
from satire_style import rough, install_circle_hands   # noqa: E402

mouths.install(B)
install_circle_hands(B)
FPS, SR = 12, MA.SR

# =============================================== STORY =============================================================
# MAP (rule 61: keep it in step; a note is answered by reading only these lines):
#   the cast and the Hat: terfwarts_cast.py (its own MAP); the places (paintings, cameras as sets.View): terfwarts_sets.py;
#   plan: terfwarts_plan.py; layout sheet: terfwarts_compose.py.
#   Here: LINES (the script, by number) and the timeline built from it (T: every beat's time); SHOTS; who is where and
#   how they stand: harry_state / ron_state / myrtle_state / mcg_state; each shot drawn: shot_hat, shot_run,
#   shot_door, shot_boys (and the two close-ups through zoom); sound: soundtrack (scream, thud, run).
NAME = 'terfwarts'
HAS = {'people', 'rooms', 'voices', 'effects', 'props'}
TITLE = ()                                        # no title (CLAUDE.md: TikTok films have none by default)
TITLE_AT = dict(cap=116, top=310)
CAST = C.CAST
WHO = ('harry', 'ron', 'myrtle', 'mcg', 'hat')     # 'hat' speaks; drawn by C.hat
# The script, word for word (brief rows 3, 8-19). est: seconds until Sam's recording replaces it ('audio').
LINES = [
    dict(n=1, audio='terfwarts-1', who='hat', text="He's a Biological Male!", est=1.5),
    dict(n=2, audio='terfwarts-2', who='harry', text='Myrtle, Hermione is under attack by a troll.', est=2.6),
    dict(n=3, audio='terfwarts-3', who='myrtle', text="As a penis'd individual, you expect free license to conduct predatory behaviour "
                                 "inside a female-exclusive space.", est=6.2),
    dict(n=4, audio='terfwarts-4', who='harry', text="What? No, Myrtle, you don't understand. Hermione could be killed at any moment.", est=4.4),
    dict(n=5, audio='terfwarts-5', who='myrtle', text='Yes. By a man masquerading as a woman in a dress. I will not allow you to turn this '
                                 'space into a chapel of wanton molestation.', est=8.0),
    dict(n=6, audio='terfwarts-6', who='ron', text="I don't like spiders, Harry.", est=1.8),
    dict(n=7, audio='terfwarts-7', who='harry', text="Ron, get it together, I'm sick of you already.", est=2.6),
    dict(n=8, audio='terfwarts-8', who='myrtle', text="When you throw open the door of a bathroom or changing room to any man so-called "
                                 "'trying to save the life' of a woman, then you throw it open to anyone wanting to "
                                 "come inside.", est=10.5),
    dict(n=9, audio='terfwarts-9', bleep=(2.56, 2.96), who='harry', text="Well it's not a problem anymore, Myrtle, as she's f****** dead now.", est=3.8),
    dict(n=10, audio='terfwarts-10', who='myrtle', text='Dead is a thought-terminating cliché.', est=2.6),
    dict(n=11, audio='terfwarts-11', who='ron', text="I don't like them, Harry.", est=1.6),
    dict(n=12, audio='terfwarts-12', who='harry', text="I don't like you, Ron.", est=1.5),
]
L = {ln['n']: ln for ln in LINES}
for ln in LINES:                                  # time each line to its recording when there is one
    ln['_voice'] = None
    dur = ln['est']
    if ln.get('audio') and os.path.exists(os.path.join(HERE, 'audio', ln['audio'] + '.m4a')):
        x = MA.line(ln['audio'])                  # Sam's takes carry a second or two of room either side:
        st = MA.pauses(x, 0.12)                   # cut only in silence, just before the first word, just after the last
        a, b = max(0, int((st[0][0] - 0.12) * SR)), min(len(x), int((st[-1][1] + 0.25) * SR))
        x = x[a:b].copy()
        fade = int(0.02 * SR)
        x[:fade] *= np.linspace(0, 1, fade)
        x[-fade:] *= np.linspace(1, 0, fade)
        if ln.get('bleep'):                       # rule 27: Sam says the word, a 1 kHz tone goes over it. Placed from
            b0, b1 = (int(v * SR) for v in ln['bleep'])   # the sound (line 9: the quiet "f" at 2.56 s, the burst of
            k = np.arange(b1 - b0)                # "uck", "ing" fading by 2.96 s; "dead" starts 2.98 s), trimmed take
            ramp = np.minimum(1, np.minimum(k, len(k) - k) / (0.006 * SR))
            x[b0:b1] = 0.18 * np.sin(2 * math.pi * 1000 * k / SR) * ramp
        ln['_voice'] = x
        dur = len(x) / SR
    ln['_dur'] = dur
    ln['_stretches'] = MA.pauses(ln['_voice'], 0.12) if ln['_voice'] is not None else [(0.0, dur)]

# The timeline: every beat follows the one before (so a recording that runs long pushes the rest on).
T = {}
T['hat_land'] = 0.45                              # McGonagall's hands bring the Hat down onto Harry's head
L[1]['start'] = 0.55                              # the hook: "BIOLOGICAL MALE" at about half a second (note 1)
T['annoyed'] = L[1]['start'] + L[1]['_dur'] + 0.1
T['run'] = min(T['annoyed'] + 0.8, 2.95)         # cut: the cloister (no shot over 3 s: Sam, 3 Nov), "Later…"
T['door'] = T['run'] + 2.7                        # cut: Myrtle comes out through the door; the boys skid in
T['halt'] = T['door'] + 0.55


def _after(n, prev_end, gap=0.25):
    L[n]['start'] = prev_end + gap
    L[n]['end'] = L[n]['start'] + L[n]['_dur']
    return L[n]['end']


L[1]['end'] = L[1]['start'] + L[1]['_dur']
e = _after(2, T['door'] + 1.6, 0.0)
for n in (3, 4, 5, 6, 7):
    e = _after(n, e, 0.3 if n in (3, 5) else 0.25)
T['float'] = e + 0.3                              # Myrtle floats round to block the doorway (brief 14) as she speaks
e = _after(8, T['float'], 0.2)
T['scream'] = e + 0.6                             # Hermione's scream through the door (Sam's recording, drawn out)
SCREAM_LEN = 8.6                                  # seconds of the scream used, cut off by the thud
T['thud'] = T['scream'] + SCREAM_LEN
e = _after(9, T['thud'] + 1.1, 0.0)
e = _after(10, e, 0.3)
e = _after(11, e, 0.35)
e = _after(12, e, 0.3)
DUR = e + 0.7
BLACK_AT = DUR
CARDS = [('Later…', T['run'] + 0.05, T['run'] + 1.6)]   # brief 5: the subtitle over the corridor


def _speaker_shots():
    """Shot/reverse at the door: each line from the side of whoever speaks, cutting a quarter second before."""
    out = [('hat', 0.0, T['run']), ('run', T['run'], T['door']), ('door', T['door'], L[2]['start'] - 0.25)]
    for n in range(2, 9):
        cam = 'door' if L[n]['who'] == 'myrtle' else 'boys'
        a = L[n]['start'] - 0.25 if n > 2 else out[-1][2]
        b = L[n + 1]['start'] - 0.25 if n < 7 else (T['float'] - 0.25 if n == 7 else T['scream'])
        if n == 8:
            a = T['float'] - 0.25
        if out[-1][0] == cam:
            out[-1] = (cam, out[-1][1], b)
        else:
            out.append((cam, a, b))
    s = T['scream']                               # the scream: Myrtle obstinate / Harry annoyed, back and forth
    out += [('myrtle close', s, s + 1.8), ('harry close', s + 1.8, s + 3.5), ('door', s + 3.5, s + 5.0),
            ('harry close', s + 5.0, s + 6.5), ('myrtle close', s + 6.5, s + 7.8), ('door', s + 7.8, T['thud'] + 0.9)]
    out += [('boys', T['thud'] + 0.9, L[10]['start'] - 0.25), ('door', L[10]['start'] - 0.25, L[11]['start'] - 0.25),
            ('boys', L[11]['start'] - 0.25, L[12]['start'] - 0.2), ('harry close', L[12]['start'] - 0.2, DUR)]
    return _choppy(out)


# Sam, 3 Nov: quick cuts, no camera held over 3 s. A long hold is cut into even pieces of 2.6 s at most, going
# speaker wide -> speaker close -> the listener's face -> speaker close ...
CUTAWAY = {'door': ('door', 'myrtle close', 'harry close', 'myrtle close'),
           'boys': ('boys', 'harry close', 'myrtle close', 'harry close'),
           'harry close': ('harry close', 'myrtle close'), 'myrtle close': ('myrtle close', 'harry close')}
MOST = 2.6


def _choppy(shots):
    out = []
    for cam, a, b in shots:
        n = math.ceil((b - a) / MOST - 1e-6) if cam in CUTAWAY and b - a > 3.0 else 1
        for i in range(n):
            c = CUTAWAY[cam][i % len(CUTAWAY[cam])] if n > 1 else cam
            p = (c, a + (b - a) * i / n, a + (b - a) * (i + 1) / n)
            if out and out[-1][0] == p[0]:
                out[-1] = (p[0], out[-1][1], p[2])
            else:
                out.append(p)
    return out


SHOTS = _speaker_shots()
SHOT_CAST = {'hat': ['harry', 'mcg'], 'run': ['harry', 'ron'], 'door': ['myrtle', 'harry', 'ron'],
             'boys': ['harry', 'ron'], 'harry close': ['harry'], 'myrtle close': ['myrtle']}
LOOKS_AT = {'harry': 'myrtle', 'ron': None, 'myrtle': 'harry', 'mcg': 'harry'}
PLAN = dict(CEIL=PL.CEIL, ROOMS=PL.ROOMS, OPENINGS=PL.OPENINGS, THINGS=PL.THINGS, PEOPLE=PL.PEOPLE, CAMS=PL.CAMS,
            GROUPS=PL.GROUPS)
# Rule 3: what makes each place recognisable (refs in references/terfwarts/), and how ours has it.
BENCHMARK = [
    dict(place='great hall', refs=['sorting-hat-scene-1', 'sorting-hat-scene-2', 'great-hall-empty-candles'], at=1.0,
         items=[('floating candles', 'terfwarts_sets.hall: 46 candles at many depths'),
                ('tall leaded windows at night', 'two pointed windows, mullions, lead diamonds'),
                ('staff table with candles and goblets', 'white cloth edge, candlesticks, gold goblets'),
                ('warm stone walls', 'stone courses in candlelight'), ('oak panelling', 'panelled dado'),
                ('house banner', 'red and gold banner'), ('the patched Sorting Hat', 'terfwarts_cast.hat'),
                ('the stool', 'off frame below (close-up)')]),
    dict(place='corridor', refs=['corridor', 'trio-hbo-cloister'], at=T['run'] + 1.0,
         items=[('fan vaulting', 'a fan on every shaft, ribs'), ('honey stone', 'STONE colours'),
                ('tracery windows onto the garth', 'west wall, three lights, lawn and the far range'),
                ('stone bench', 'east wall, the whole length'), ('flagstones', 'staggered flags'),
                ('arch at the far end', 'pointed arch, lit'), ('attached shafts at every bay', 'every 2.6 m'),
                ('blind tracery panels', 'three a bay over the bench')]),
    dict(place="girls' bathroom door", refs=['door-1', 'door-2'], at=T['door'] + 1.0,
         items=[('pointed arch with moulded rings', 'four rings'), ('clustered shafts and capitals', 'three a side'),
                ('carved oak double door', 'two leaves, square panels with bosses'), ('ring handles', 'two'),
                ('shrunk to a toilet door', '1.1 m wide (brief 6)'), ('GIRLS plaque', 'brass, on the top panel')]),
]
HOOK = ('Rowling left HBO some edits 😬', {'y': 250})   # Sam's wording, 3 Nov; sits above the Hat (note 1)
# The joke prop must stay clear: the GIRLS plaque in every door shot
KEEP_CLEAR = [('GIRLS plaque', lambda t: SETS.plaque_box(SETS.DOOR, cam_for(t)) if shot_of(t) in ('door',) else None)]
PROP_SIZES = []
OUTFIT = {}
HEIGHTS = dict(C.HEIGHTS)
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
ALLOWED_CONTACTS = [('mcg.hand*', 'HAT', 0.0, T['hat_land'] + 0.15, 'McGonagall lowers the Hat'),
                    ('HAT', 'harry', T['hat_land'], T['run'], 'the Hat sits on his head')]
ALLOWED_POPS = [('myrtle', T['door'], T['door'] + 0.6, 'she comes out through the shut door (a ghost)')]
SET_EXCLUDE = [('stone bench', 'nobody goes near it'), ('brass plaque', 'flat on the door')]
TOUCHES = [('mcg.handL', 'HAT', 0.0, T['hat_land'], 'lowers it'), ('mcg.handR', 'HAT', 0.0, T['hat_land'], 'lowers it')]
FREE_MOVES = []
SOUND_SOURCES = {}
EFFECTS = []
JOKE_PROPS = []
ORDER_SWAPS = []
# ====================================================================================================================

import terfwarts_sets as SETS     # noqa: E402
V = views
MV = moves
FY = 1420


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def _ramp(t, a, b):
    return min(1.0, max(0.0, (t - a) / (b - a)))


def _ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


TRACK = {w: [(a + ln['start'], b + ln['start'], sh) for ln in LINES if ln['who'] == w
             for a, b, sh in mouths.track(ln['text'], ln['_stretches'])] for w in WHO}
BLINKS = {w: F.blinks(11 + i, 0.5, DUR, talking=True) for i, w in enumerate(WHO)}


def _face(who, t, **kw):
    shape = mouths.at(TRACK[who], t)
    f = dict(mouth='set' if shape == 'rest' else 'v:' + shape, blink=F.blinking(t, BLINKS[who]))
    f.update(kw)
    if shape != 'rest' and 'mouth' in kw and kw['mouth'] != 'v:' + shape:
        f['mouth'] = 'v:' + shape                 # speaking always shows the spoken shape
    return f


def talking(who, t):
    return any(a <= t < b for a, b, _ in TRACK[who])


# ------------------------------------------------------------------------------------------------ the people
# Sam's note 8: the boys' arms never just hang; each holds a pose from the gallery (rule 42) that suits the moment,
# blended over a third of a second. (time it starts, pose)
def _poses():
    hp = [(0.0, 'hips'), (L[2]['start'] - 0.1, 'palm_open'), (L[2]['end'] + 0.3, 'relaxed'),
          (L[4]['start'] - 0.2, 'hands_up'), (L[4]['end'] + 0.2, 'hips'), (L[6]['start'], 'relaxed'),
          (L[7]['start'] - 0.2, 'point_ron'), (L[7]['end'] + 0.3, 'relaxed'), (T['float'] + 2.0, 'arms_folded'),
          (L[9]['start'] - 0.1, 'shrug'), (L[9]['end'] + 0.2, 'arms_folded')]
    rp = [(0.0, 'hips'), (L[3]['start'], 'palms_together'), (L[4]['start'], 'relaxed'),
          (L[5]['start'] + 3.0, 'shrug'), (L[5]['end'] - 1.5, 'relaxed'), (L[6]['start'] - 0.2, 'palms_together'),
          (L[7]['end'] + 0.3, 'relaxed'), (T['scream'] + 0.4, 'palms_together'), (L[10]['start'], 'relaxed'),
          (L[11]['start'] - 0.2, 'palms_together')]
    return {'harry': hp, 'ron': rp}


POSES = _poses()


def _pose(sp, name):
    if name == 'hands_up':
        return PG.hands_up(sp)
    if name == 'palms_together':
        return PG.palms_together(sp)
    if name == 'point_ron':                       # the gallery's pointing pose, mirrored: his left hand at Ron
        j = V.standing(sp)
        sw = sp.get('shoulders', 150)
        V.arm_to(j, 'L', (-(sw + 400), 60.0, 250.0), 'down', 'point')
        V.arm_to(j, 'R', (sw - 4, 380.0, 10.0), 'out')
        return j
    return MV.pose(sp, name)


def posed(who, t):
    sched = POSES[who]
    i = max(k for k, (a, _) in enumerate(sched) if a <= t or k == 0)
    sp = CAST[who]
    cur = _pose(sp, sched[i][1])
    if i == 0:
        return cur
    u = _ease(_ramp(t, sched[i][0], sched[i][0] + 0.35))
    return cur if u >= 1 else MV.mix_poses(_pose(sp, sched[i - 1][1]), cur, u)


def harry_state(t):
    """(yaw, joints, face) for Harry at the door. Panting on arrival (hands on hips), pleading (hands up) on line 4,
    his eyes going to Ron on lines 7, 11 and 12 (Sam: never the three-quarter turn), annoyed through the scream
    (annoyance 3)."""
    j = posed('harry', t)
    face = _face('harry', t, look=0.0)
    yaw = 0
    if t < L[2]['end'] + 0.6:                     # panting: the body heaves, mouth open between words
        k = 1.0 - _ramp(t, L[2]['end'], L[2]['end'] + 0.6)
        j['bob'] = 7 * k * (0.5 + 0.5 * math.sin(2 * math.pi * t / 0.5))
        j['lean'] = 7 * k
        if not talking('harry', t):
            face['mouth'] = 'agape'
    if L[4]['start'] - 0.2 <= t < L[4]['end'] + 0.2:
        face.update(brow_raise=6)
    for n in (6, 7, 11, 12):
        if L[n]['start'] - 0.3 <= t < L[n]['end'] + 0.4:
            face['look'] = -0.85                  # his eyes to Ron, on his left as we see them from Myrtle
            if n in (7, 12):
                face.update(brows='fierce', lid=2)
    if T['thud'] - SCREAM_LEN <= t < L[9]['end'] + 0.3 or L[10]['start'] <= t:
        face.update(brows='fierce', lid=2, mouth=face['mouth'] if talking('harry', t) else 'line')
    if T['scream'] + 5.0 <= t < T['thud'] + 0.9:
        face.update(lid=3)                        # more fed up as it goes on
    return yaw, j, face


def ron_state(t):
    """Ron: vacant, gibbering; looks at nothing (up and away); mouth hangs open when he isn't talking."""
    j = posed('ron', t)
    face = _face('ron', t, look=0.6, look_v=-0.5, brow_raise=6)
    if not talking('ron', t):
        face['mouth'] = 'agape'
    if t < L[2]['end'] + 0.6:
        k = 1.0 - _ramp(t, L[2]['end'], L[2]['end'] + 0.6)
        j['bob'] = 8 * k * (0.5 + 0.5 * math.sin(2 * math.pi * (t + 0.2) / 0.45))
        j['lean'] = 8 * k
    return 0, j, face


def myrtle_state(t):
    """Myrtle: (x, z, lift, alpha, joints, face). Out through the door at T['door']; lecturing (pointing at Harry) on
    lines 3 and 5; drifting off to the side, bored, while the boys talk (6-7); floating round to block the doorway on
    line 8, arms spread, and holding it through the scream; arms folded for line 10."""
    sp = CAST['myrtle']
    x, z, lift = PL.DOOR_X, 25.3, 0.3 + 0.04 * math.sin(2 * math.pi * t / 2.2)
    u = _ease(_ramp(t, T['door'], T['door'] + 0.6))
    z = 25.95 - 0.65 * u
    alpha = u
    j = V.standing(sp)
    face = _face('myrtle', t, look=0.0, brows='fierce' if talking('myrtle', t) else None)
    face = {k: v for k, v in face.items() if v is not None}
    if L[3]['start'] - 0.2 <= t < L[3]['end'] or L[5]['start'] - 0.2 <= t < L[5]['end']:
        j = V.standing(sp)                         # the gallery's pointing pose, mirrored: her left hand at Harry
        sw = sp.get('shoulders', 150)
        V.arm_to(j, 'L', (-(sw + 400), 60.0, 250.0), 'down', 'point')
        V.arm_to(j, 'R', (sw - 4, 380.0, 10.0), 'out')
    drift = _ease(_ramp(t, L[6]['start'] - 0.2, L[7]['end'])) * (1 - _ease(_ramp(t, T['float'], T['float'] + 1.6)))
    x -= 0.7 * drift
    lift += 0.25 * math.sin(math.pi * _ramp(t, T['float'], T['float'] + 1.6))   # an arc up and back down
    if L[6]['start'] - 0.2 <= t < T['float']:
        j = PG.arms_folded(sp)
        face.update(look=-0.6, look_v=-0.4)        # bored, looking away
    spread = _ease(_ramp(t, T['float'] + 1.2, T['float'] + 1.7))
    if t >= T['float'] + 1.2 and t < L[10]['start'] - 0.2:
        j = V.standing(sp)
        for side, tgt in {'L': (-330.0, 40.0, 60.0), 'R': (330.0, 40.0, 60.0)}.items():
            lo = {'L': (-80.0, 470.0, 40.0), 'R': (80.0, 470.0, 40.0)}[side]
            V.arm_to(j, side, tuple(a + (b - a) * spread for a, b in zip(lo, tgt)), 'down', 'fist')
        if T['scream'] <= t:
            face.update(look=0.0, look_v=0.3, brows='fierce', lid=2)   # obstinate: chin up, eyes down at Harry
    if t >= L[10]['start'] - 0.2:
        j = PG.arms_folded(sp)
    return x, z, lift, alpha, j, face


def mcg_state(t, brim):
    """McGonagall behind Harry: her hands on the Hat's brim as she lowers it, then back to her sides; she looks
    down at him."""
    sp = CAST['mcg']
    j = V.standing(sp)
    return j, dict(_face('mcg', t), look=0.3, look_v=0.8, mouth='set')


def hat_drop(t):
    """How far above its worn place the Hat is (pixels at Harry's scale), easing down until it lands."""
    return 150 * (1 - _ease(_ramp(t, 0.0, T['hat_land'])))


# ------------------------------------------------------------------------------------------------ the shots
CAM0 = B.Cam(1.0, 540, 960)
# Shot 1 (hat close): Harry seated, his face 300 px tall (rule 50), the Hat over his eyebrows, McGonagall behind on
# just behind him, facing front, a little to the left so her face clears the Hat's point (Sam's note 6); the space
# above her left for the Hook Text (note 1). A flat close-up: 1500 px a metre at Harry, 1000 at McGonagall (half a
# metre behind). The subtitle sits over his chest, clear of his face.
HAT_PXM, HAT_EYE_Y, HARRY_X, MCG_X, MCG_PXM = 1500.0, 1160.0, 580, 470, 1000.0


def cam_for(t):
    s = shot_of(t)
    if s == 'harry close':
        hx, hy = _boys_head('harry', t)
        return B.Cam(2.3, hx, hy + 70)
    if s == 'myrtle close':
        x, z, lift, *_ = myrtle_state(t)
        d = SETS.DOOR.d_of(z)
        mx = SETS.DOOR.P(SETS.DOOR.r_of(x), 0, d)[0]
        my = SETS.DOOR.floor_y(d, lift) - 1.32 * SETS.DOOR.pxm(d)
        return B.Cam(2.0, mx, my + 140)
    return CAM0


def _world(cam, q):
    """A point from screen pixels (times SS, as Pen draws) back to the world (cam's units)."""
    return (q[0] / B.SS - 540) / cam.z + cam.cx, (q[1] / B.SS - 960) / cam.z + cam.cy


def _scale(pxm):
    return pxm * V.M_PER_UNIT


SOLO = [None]                                     # the audit draws one person alone (and no set)


def _draw(img, cam, who, x, floor, pxm, yaw, j, face, lift=0.0, t=0.0, head_props=()):
    if SOLO[0] and SOLO[0] != who:
        return None
    return C.person(img, cam, x, floor, _scale(pxm), who, yaw, j, face, lift=lift, t=t, head_props=head_props)


def shot_hat(img, cam, t):
    if not SOLO[0]:
        img.alpha_composite(SETS.cached('hall', cam, SETS.hall))
    s_h = _scale(HAT_PXM)
    sit = MV.seated(CAST['harry'])
    s2 = s_h * C.HEIGHTS['harry'] / 1.75
    floor = HAT_EYE_Y + 158 * s2 + (928 - 2 * sit['bob']) * s2    # (the cast's person() and views both drop by bob)
    face = _face('harry', t, look=0.0, look_v=-0.9 if t < T['annoyed'] else -0.2)
    if t >= T['annoyed']:
        face.update(brows='fierce', lid=2, mouth='line', look_v=-0.2)      # annoyance 3 (Sam)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    drop = hat_drop(t)
    brim = {}

    def worn(p, view, sp, hx, hy):
        k = sp['hw'] / 120
        yell = talking('hat', t) and mouths.at(TRACK['hat'], t) not in ('rest', 'MBP')
        by = hy - 84 - drop / s2
        C.hat(p, hx, by, k, 'yell' if yell else 'rest')
        brim['ends'] = [_world(cam, p.cam.P(hx - 180 * k, by - 2 * k)), _world(cam, p.cam.P(hx + 180 * k, by - 2 * k))]
    if SOLO[0] in (None, 'harry'):
        C.person(lay, cam, HARRY_X, floor, s_h, 'harry', 0, sit, face, t=t, head_props=[worn])
    else:
        C.person(Image.new('RGBA', img.size, (0, 0, 0, 0)), cam, HARRY_X, floor, s_h, 'harry', 0, sit, face, t=t,
                 head_props=[worn])
    # McGonagall: just behind him, facing us; her hands on both sides of the brim until it lands, then down
    pm = MCG_PXM
    s_m = _scale(pm)
    mfloor = HAT_EYE_Y + 1.0 * pm
    j, mface = mcg_state(t, brim)
    s2m = s_m * C.HEIGHTS['mcg'] / 1.75
    mny = mfloor - 928 * s2m
    hold = t < T['hat_land'] + 0.1
    hands = brim['ends'] if hold else []
    u = _ease(_ramp(t, T['hat_land'] + 0.1, T['hat_land'] + 0.6))     # letting go: hands down to her sides
    if u < 1:
        for side, (tx, ty) in zip(('L', 'R'), brim['ends']):
            rest = (-80.0 if side == 'L' else 80.0, 470.0, 40.0)
            held = ((tx - MCG_X) / s2m, (ty - mny) / s2m, 120.0)
            V.arm_to(j, side, tuple(a + (b - a) * u for a, b in zip(held, rest)), 'down', 'fist')
    _draw(img, cam, 'mcg', MCG_X, mfloor, pm, 0, j, mface, t=t)
    img.alpha_composite(lay)
    p = B.Pen(img, cam)
    for tx, ty in (hands if SOLO[0] in (None, 'mcg') else ()):                          # her hands over the brim (rule S2)
        p.ell(tx, ty, 26 * s2m, 26 * s2m, CAST['mcg']['skin'], B.INK, 2.6)


def shot_run(img, cam, t):
    v = SETS.RUN
    if not SOLO[0]:
        img.alpha_composite(SETS.cached('run', cam, lambda i, c: SETS.cloister(i, c, v)))
        SETS.sconces(img, cam, v, t)
    u = t - T['run']
    dur = T['door'] - T['run']
    out = []
    for who, x0, lag in (('ron', PL.DOOR_X + 0.4, 0.25), ('harry', PL.DOOR_X - 0.35, 0.0)):
        d = max(2.3, 8.0 - 2.15 * u + lag * 2.15)
        out.append((d, who, x0))
    for d, who, x0 in sorted(out, reverse=True):
        pxm = v.pxm(d)
        x = v.P(v.r_of(x0), 0, d)[0]
        j = MV.gait(dict(CAST[who]), u + (0.15 if who == 'ron' else 0.0), 'run')
        face = _face(who, t, mouth='agape' if who == 'ron' else 'set', brows='fierce' if who == 'harry' else None)
        face = {k: vv for k, vv in face.items() if vv is not None}
        _draw(img, cam, who, x, v.floor_y(d), pxm, 0, j, face, t=t)


def _myrtle(img, cam, v, t, yaw):
    x, z, lift, alpha, j, face = myrtle_state(t)
    d = v.d_of(z)
    if d <= 0.2 or alpha <= 0:
        return
    pxm = v.pxm(d)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    _draw(lay, cam, 'myrtle', v.P(v.r_of(x), 0, d)[0], v.floor_y(d, lift), pxm, yaw, j, face, t=t)
    if alpha < 1:
        a = lay.getchannel('A').point(lambda q: int(q * alpha))
        lay.putalpha(a)
    img.alpha_composite(lay)


def shot_door(img, cam, t):
    """Over the boys' shoulders at Myrtle and the shrunk door (the boys' backs big in the foreground)."""
    v = SETS.DOOR
    if not SOLO[0]:
        img.alpha_composite(SETS.cached('door', cam, lambda i, c: SETS.cloister(i, c, v)))
        SETS.sconces(img, cam, v, t)
    if not SOLO[0]:
        SETS.plaque_text(img, v, cam)
    _myrtle(img, cam, v, t, 0)
    arrive = _ease(_ramp(t, T['door'], T['halt']))
    for who in ('harry', 'ron'):
        x0, z0 = PL.PEOPLE[who]['at']
        d = v.d_of(z0) - (1 - arrive) * 0.9
        yaw, j, face = (harry_state if who == 'harry' else ron_state)(t)
        _draw(img, cam, who, v.P(v.r_of(x0), 0, d)[0], v.floor_y(d), v.pxm(d), 180, j, face, t=t)


def _boys_head(who, t):
    v = SETS.BOYS
    x0, z0 = PL.PEOPLE[who]['at']
    d = v.d_of(z0)
    s2 = _scale(v.pxm(d)) * C.HEIGHTS[who] / 1.75
    return v.P(v.r_of(x0), 0, d)[0], v.floor_y(d) - (928 + 150) * s2


def shot_boys(img, cam, t):
    """Myrtle's view: Harry and Ron in front of her, the cloister running away behind them."""
    v = SETS.BOYS
    if not SOLO[0]:
        img.alpha_composite(SETS.cached('boys', cam, lambda i, c: SETS.cloister(i, c, v)))
        SETS.sconces(img, cam, v, t)
    for who in sorted(('harry', 'ron'), key=lambda w: -v.d_of(PL.PEOPLE[w]['at'][1])):
        x0, z0 = PL.PEOPLE[who]['at']
        d = v.d_of(z0)
        yaw, j, face = (harry_state if who == 'harry' else ron_state)(t)
        _draw(img, cam, who, v.P(v.r_of(x0), 0, d)[0], v.floor_y(d), v.pxm(d), yaw, j, face, t=t)


DRAW = {'hat': shot_hat, 'run': shot_run, 'door': shot_door, 'boys': shot_boys, 'harry close': shot_boys,
        'myrtle close': shot_door}


def picture(t):
    """The frame WITHOUT captions or title (those go on last, so wording notes never re-render a picture)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    cam = cam_for(t)
    img = B.canvas()
    DRAW[shot_of(t)](img, cam, t)
    return img


def draw_order(t):
    """Rule 57: the names picture(t) draws, back to front."""
    if t >= BLACK_AT:
        return []
    s = shot_of(t)
    return {'hat': ['background', 'mcg', 'harry', 'HAT'], 'run': ['background', 'ron', 'harry'],
            'door': ['background', 'myrtle', 'harry', 'ron'], 'myrtle close': ['background', 'myrtle', 'harry', 'ron'],
            'boys': ['background', 'ron', 'harry'], 'harry close': ['background', 'ron', 'harry']}[s]


def chunks(text, most=4):
    """Short, quick subtitles (Sam, 3 Nov): split at sentence and comma breaks, each piece into even groups of at most
    four words; a lone last word joins the words before it. Each chunk: (words, its share of the line)."""
    import re
    parts = [p.strip().split() for p in re.split(r'(?<=[.,?!])\s+', text) if p.strip()]
    out = []
    for w in parts:
        k = math.ceil(len(w) / most)
        cuts = [round(i * len(w) / k) for i in range(k + 1)]
        groups = [w[cuts[i]:cuts[i + 1]] for i in range(k)]
        for g in groups:
            if len(g) == 1 and out and out[-1][-1][-1] not in '.?!' and len(out[-1]) < 5:
                out[-1] = out[-1] + g
            else:
                out.append(g)
    n = sum(len(c) for c in out)
    return [(' '.join(c), len(c) / n) for c in out]


def caption_at(t):
    for a, b, text in [(c[1], c[2], c[0]) for c in CARDS]:
        if a <= t < b:
            return text
    for i, ln in enumerate(LINES):
        nxt = LINES[i + 1]['start'] - 0.05 if i + 1 < len(LINES) else 1e9
        if ln['start'] - 0.05 <= t < min(ln['end'] + 0.25, nxt):
            talk = ln['_stretches']                # each chunk takes its share of the talking time, pauses skipped
            total = sum(q - p for p, q in talk) or 1.0
            u, done = t - ln['start'], 0.0
            for p, q in talk:
                if u < q:
                    done += max(0.0, u - p)
                    break
                done += q - p
            acc = 0.0
            for text, share in chunks(ln['text']):
                acc += share * total
                if done < acc - 1e-6:
                    return text
            return text
    return None


def overlay(img, t):
    if t < BLACK_AT:
        c = caption_at(t)
        if c:
            PP.caption(img, c, italic=c == CARDS[0][0])
    return img


def frame_image(t):
    return overlay(picture(t), t)


SFX = {'scream': os.path.join(HERE, 'audio', 'terfwarts-scream.mp3'),   # Sam's picks (3 Nov)
       'thud': os.path.join(HERE, 'audio', 'terfwarts-thud.mp3'),
       'run': os.path.join(HERE, 'audio', 'terfwarts-run.mp3')}


def soundtrack(stems=False):
    from burnham_film import load
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)        # no room tone: white noise under a film comes up as a hiss (Sam, 19 Oct)
    for ln in LINES:
        if ln['_voice'] is not None:
            s = int(ln['start'] * SR)
            seg = ln['_voice'][:max(0, n - s)]
            voice[s:s + len(seg)] += seg
    scream = load(SFX['scream'])                  # through the door: muffled a little, cut off dead by the thud
    s0 = int(0.45 * SR)
    seg = scream[s0:s0 + int(SCREAM_LEN * SR)].copy()
    seg[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    filmkit.place(rest, seg, at=T['scream'], sr=SR, gain=0.8)
    thud = load(SFX['thud'])[:int(1.0 * SR)].copy()   # its 3 s rumble ran under Harry's "Well it's not...": the hit
    thud[-int(0.4 * SR):] *= np.linspace(1, 0, int(0.4 * SR))   # kept, the tail faded out by 1 s
    filmkit.place(rest, thud, at=T['thud'], sr=SR, gain=1.0)
    run = load(SFX['run'])[:int((T['door'] - T['run'] + 0.6) * SR)].copy()
    run[-int(0.4 * SR):] *= np.linspace(1, 0, int(0.4 * SR))      # fades as they skid to a halt
    filmkit.place(rest, run, at=T['run'], sr=SR, gain=0.7)
    mix = voice + rest
    end = int(BLACK_AT * SR)
    if np.abs(voice).max() > 1e-6:                              # -16 LUFS, levelled gently, never squashed by more
        mix, g = MA.master(mix, end)                             # than 3 dB (hard limiting crackles on a phone)
        voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


def checks():
    """Plan checks: seconds. Raises on the first batch of faults; prints the subtitles to proofread."""
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches']]
    faults = E.check_mouths(sorted(x for w in WHO for x in TRACK[w]), windows)
    if any(ln['_voice'] is not None for ln in LINES):
        _, voice, rest = soundtrack(stems=True)
        faults += filmkit.voice_balance(voice, rest, SR, windows)
        n = int((DUR + 0.3) * SR)
        raw = np.zeros(n)
        for ln in LINES:
            if ln['_voice'] is not None:
                s = int(ln['start'] * SR)
                raw[s:s + len(ln['_voice'])] += ln['_voice'][:n - s]
        faults += MA.limit_check(raw, int(BLACK_AT * SR))     # more than 3 dB of limiting crackles on a phone
    mix, voice, rest = soundtrack(stems=True)
    # no steady hiss (rule 60), heard where nothing is meant to sound: with the gaps between Sam's trimmed lines now
    # 0.25 s, the only voice-free stretches were the running feet and the scream (their own highs, -49 dBFS); with
    # both silent the film measures -94 dBFS (3 Nov)
    faults += filmkit.hiss_check(mix, SR, BLACK_AT, voice=voice + rest)
    for q in filmkit.sound_questions({'voice': voice, 'background': rest, 'mix': mix}, SR,
                                     cuts=[a for _, a, _ in SHOTS[1:]], end=BLACK_AT):
        print('QUESTION FOR SAM:', q)        # may be meant: ask, never change it without him
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


# ------------------------------------------------------------------------------------------------ the audit
# audit.py (rules 5, 6): everyone where the plan puts them (Myrtle as she floats), the set from PLAN by itself.
def scene(t):
    import audit
    s = shot_of(t)
    out = []
    if s == 'hat':
        x, z = PL.PEOPLE['harry hall']['at']
        out.append(audit.Thing('harry', audit.simple('harry', x, z, C.HEIGHTS['harry'], sitting=True)))
        return out
    for who in SHOT_CAST[s]:
        if who == 'myrtle':
            x, z, lift, alpha, *_ = myrtle_state(t)
            if alpha > 0.5:
                out.append(audit.Thing('myrtle', audit.simple('myrtle', x, z, C.HEIGHTS['myrtle'], base=lift)))
        elif s != 'run':
            x, z = PL.PEOPLE[who]['at']
            out.append(audit.Thing(who, audit.simple(who, x, z, C.HEIGHTS[who])))
    return out


def audits():
    """The general audit: each person alone over every frame they are on screen; the eyelines. Returns faults."""
    def alone(who):
        def draw(t):
            SOLO[0] = who
            try:
                lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
                DRAW[shot_of(t)](lay, cam_for(t), t)
                return lay
            finally:
                SOLO[0] = None
        return draw
    actors = {}
    for who in ('harry', 'ron', 'myrtle', 'mcg'):
        for shot, a, b in SHOTS:
            if who in SHOT_CAST[shot]:
                ts = [i / FPS for i in range(int(a * FPS), int(b * FPS))]
                if ts:
                    actors[f'{who} [{shot} {a:.1f}]'] = (ts, alone(who))
    filmkit.EYES.clear()
    faults = filmkit.silhouette_audit(actors, fps=FPS, still_ok=())
    faults += moves.audit()                                  # the movement library's own checks (gaits, poses)
    return faults


def LINE_SUBJECTS():
    """Each of the cast alone, large, for the line-work check (linecheck.py)."""
    def one(who):
        def d(im):
            C.person(im, B.Cam(1.0, 540, 960), 540, 1800, 1.45, who)
        return d
    return [(who, one(who)) for who in C.ORDER]


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        C.sheet(a[1])
    elif a[0] == 'shots':
        for s in SHOTS:
            print(f'{s[0]:13s} {s[1]:6.2f} {s[2]:6.2f}')
        for ln in LINES:
            print(ln['n'], ln['who'], round(ln['start'], 2), round(ln['end'], 2))
        print({k: round(v, 2) for k, v in T.items()}, 'DUR', round(DUR, 2))
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'check':
        B.SS = 1
        checks()
        f = audits()
        import audit
        f += [x[len('AUDIT: '):] for x in audit.check(sys.modules[__name__])]   # collisions, pop-ins (preflight too)
        print('\n'.join(['AUDIT: ' + x for x in f]) or 'audit: clean')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)   # --nostamp: a clip to splice into a final (rule 47)


F.guard(B)   # every arm drawn is measured against the rig; a wrong one stops the render
import limbs                     # noqa: E402
limbs.install(B)                 # natural arms and legs: one outline at the shoulder, smooth shaped legs (Cry Minister)

if __name__ == '__main__':
    main()
