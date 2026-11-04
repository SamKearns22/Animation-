#!/usr/bin/env python3
"""MidTerminal (notes/midterminal.md): Trump storms into the Oval Office to have a go at Satan about the midterms;
the hellfire ghost of Epstein drifts in. Built from the satire template (guides/satire.md).

    python3 source/midterminal.py stills OUT_DIR T [T ...]  stills at these times (seconds)
    python3 source/midterminal.py shots                     the timeline in numbers
    python3 source/midterminal.py check                     every check and the audit (also run by preflight.py)
    python3 source/midterminal.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1] [--nostamp]
"""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402  people: flat shapes, black outlines
import mossad as M               # noqa: E402,F401  (brows, mouths, hair; patched into burnham on import)
import figure as F               # noqa: E402  arms solved and guarded
import mouths                    # noqa: E402  lip sync
import subtitles as SUB          # noqa: E402  short, quick, readable subtitles timed from the recordings
import mossad_audio as MA        # noqa: E402  recordings cleaned and levelled
import peepee as PP              # noqa: E402  the series' caption
import filmkit                   # noqa: E402  the general checks
import film_engine as E          # noqa: E402  render with the picture cache, subtitle list, mouth check
import midterminal_set as MS     # noqa: E402  the Oval Office in 3D
import midterminal_cast as MC    # noqa: E402  Satan, Epstein, Trump
import midterminal_moves as MV   # noqa: E402  the door, the walk-in, the float, the ghost and skull
import views as V                # noqa: E402
import moves                     # noqa: E402
import posegallery as PG         # noqa: E402
from satire_style import install_circle_hands   # noqa: E402

mouths.install(B)
install_circle_hands(B)
FPS, SR = 12, MA.SR

# =============================================== STORY =============================================================
# MAP (rule 61: keep it in step; a note is answered by reading only these lines):
#   the cast: midterminal_cast.py; the room: midterminal_set.py; the door, walk, float, ghost, skull: midterminal_moves.py
#   (each has its own MAP). Here: LINES (the script, by number; est = seconds until Sam's take replaces it) 50 |
#   the timeline T 95 | SHOTS and cameras 125 | the checks' lists 150 | each person's state (trump_sp, satan_j,
#   epstein_j) 200 | picture 280 | captions, overlay 320 | sound 345 | checks, audit 380 | main 450.
NAME = 'midterminal'
HAS = {'people', 'rooms', 'voices', 'effects', 'props'}
TITLE = ()                                        # no title (CLAUDE.md)
TITLE_AT = dict(cap=116, top=310)
CAST = MC.CAST
WHO = ('trump', 'satan', 'epstein')
# The script, word for word (shot list 1-10; brief rows 7-17). bleep: (start, end) in the trimmed take, from the sound.
LINES = [
    dict(n=1, audio='midterminal-1', who='trump', text='Thank you, everyone, no more questions.', est=1.9),
    dict(n=2, audio='midterminal-2', who='trump', text="Satan, what the f***? This isn't what you promised.", est=2.7,
         bleep=(1.47, 1.82)),                     # "fuck": 2.10-2.45 s in Sam's take (from the sound)
    dict(n=3, audio='midterminal-3', who='satan', text="I said don't invade Iran, you invaded Iran.", est=2.4),
    dict(n=4, audio='midterminal-4', who='trump', text="Yeah! Cos Bibi told me to! I thought he was one of yours?",
         est=3.0),
    dict(n=5, audio='midterminal-5', who='satan', text="Ha, no. Bibi is in a league of his own.", est=2.0),
    dict(n=7, audio='midterminal-7', who='epstein', text="Donald, don't even worry about it. Why don't you come join "
         "me down here? It's so warm here, Donald. Nobody ever gouges out your eyes on an hourly basis.", est=6.5),
    dict(n=8, audio='midterminal-8', who='trump', text="F*** off, Jeffrey. I know it's you that keeps adding algae to "
         "the reflecting pool.", est=4.0, bleep=(0.13, 0.30)),   # "fuck": 0.97-1.14 s in Sam's take (from the sound)
    dict(n=9, audio='midterminal-9', who='epstein', text='Releeeaaaseee the fiiilleesss and ennndd myyy torrrmenttt',
         est=3.0),
    dict(n=10, audio='midterminal-10', who='trump', text="Oooo, release the files! Maybe if Satan had done his job, "
         "maybe I wouldn't have to!", est=4.0, mock_end=3.06),   # Sam's takes 9 + 10 joined; the mock ends here
]
L = {ln['n']: ln for ln in LINES}
for ln in LINES:                                  # time each line to its recording when there is one
    ln['_voice'] = None
    dur = ln['est']
    if ln.get('audio') and os.path.exists(os.path.join(HERE, 'audio', ln['audio'] + '.m4a')):
        x = MA.line(ln['audio'])                  # cut only in silence: just before the first word, after the last
        st = MA.pauses(x, 0.12)
        a, b = max(0, int((st[0][0] - 0.12) * SR)), min(len(x), int((st[-1][1] + 0.25) * SR))
        x = x[a:b].copy()
        fade = int(0.02 * SR)
        x[:fade] *= np.linspace(0, 1, fade)
        x[-fade:] *= np.linspace(1, 0, fade)
        if ln.get('bleep'):                       # rule 27: Sam says the word, a 1 kHz tone goes over it (from the sound)
            b0, b1 = (int(v * SR) for v in ln['bleep'])
            k = np.arange(b1 - b0)
            ramp = np.minimum(1, np.minimum(k, len(k) - k) / (0.006 * SR))
            x[b0:b1] = 0.18 * np.sin(2 * math.pi * 1000 * k / SR) * ramp
        ln['_voice'] = x
        dur = len(x) / SR
    ln['_dur'] = dur
    ln['_stretches'] = MA.pauses(ln['_voice'], 0.18) if ln['_voice'] is not None else [(0.0, dur)]   # (0.12 split "have to!")


def _at(n, start):
    L[n]['start'] = start
    L[n]['end'] = start + L[n]['_dur']
    return L[n]['end']


DOOR_WALK = 1.35                                   # m/s (the brisk gait, as the test clips Sam passed)
# The timeline: each beat follows the one before, so a take that runs long pushes the rest on.
T = {}
CLEAR = 0.45                                      # a cut waits till the last subtitle clears (Sam's note 36)
e = _at(1, 0.05)                                  # shot 1: talking to the press over his shoulder as he comes in
T['slam'] = max(1.3, e - 0.45)                    # the door slams on his last word; shut 0.25 s later = the cut
T['open'] = 0.1                                   # open from the start: we see him at once (Sam's note 1, 4 Nov)
T['cut2'] = T['slam'] + 0.25
T['stop'] = T['cut2'] + MV.path_length(MV.ENTRY) / DOOR_WALK   # he stops for a beat (Sam's note 32)
T['angry'] = T['stop'] + 0.4                      # a quick breath (0.4 s), then the frown snaps on
e = _at(2, T['angry'])                            # then he looks at Satan, points and speaks
T['cut3'] = e + CLEAR
e = _at(3, T['cut3'] + 0.25)                      # Satan's shrug
T['cut4'] = e + CLEAR
e = _at(4, T['cut4'] + 0.15)                      # the reverse on Trump, pointing
T['cut5'] = e + CLEAR
e = _at(5, T['cut5'] + 0.2)                       # Satan chuckles
T['cut6'] = e + CLEAR                             # held (no zoom, note 38); the ghost fades in; Satan's eyes go to him
T['ghost'] = T['cut6'] + 0.5
T['eyes'] = T['ghost'] + 0.5
T['cut7'] = T['ghost'] + 1.6
e = _at(7, T['cut7'] + 0.2)
st = L[7]['_stretches'][3] if len(L[7]['_stretches']) > 3 else (L[7]['_dur'] * 0.5, L[7]['_dur'] * 0.65)
T['away'] = L[7]['start'] + st[0] - 0.1         # Sam, 4 Nov (Q1): 2 s on Trump, disgusted, on "It's so warm here,
T['back'] = L[7]['start'] + st[1] + 0.25        # Donald." (Epstein heard off-screen), then back to Epstein
T['cut8'] = e + CLEAR
e = _at(8, T['cut8'] + 0.15)
T['cut9'] = e + CLEAR
e = _at(9, T['cut9'] + 0.25)                      # the silly-ghost arms, the melt, fading away
T['melt'] = L[9]['start'] + 0.4
T['gone'] = e + 0.9
T['cut10'] = T['gone'] + 0.1
e = _at(10, T['cut10'] + 0.2)
T['cut11'] = L[10]['start'] + L[10]['mock_end'] + 0.05   # note 43: back to the shot 2 angle for the last sentence
T['flinch'] = T['cut11'] + 0.3                    # Satan flinches from the jabbing finger
DUR = e + 0.6
BLACK_AT = DUR
SHOTS = [('door', 0.0, T['cut2']), ('two', T['cut2'], T['cut3']), ('satan', T['cut3'], T['cut4']),
         ('trump', T['cut4'], T['cut5']), ('satan', T['cut5'], T['cut6']), ('three', T['cut6'], T['cut7']),
         ('epstein', T['cut7'], T['away']), ('trump', T['away'], T['back']), ('epstein', T['back'], T['cut8']),
         ('trump', T['cut8'], T['cut9']), ('epstein', T['cut9'], T['cut10']),
         ('trump', T['cut10'], T['cut11']), ('two', T['cut11'], DUR)]
# Cameras (pos, look, focal): key shots 1-4 from the composition sheet (Sam's yes, 4 Nov); the singles new.
CAMS = dict(MV.SHOT_CAMS)
CAMS['two'] = ((0.0, 1.55, -1.7), (0.05, 1.45, 2.5), 1200)        # note 33: a little tighter, Satan forward
CAMS['three'] = ((0.0, 1.6, -1.4), (-0.25, 1.45, 2.6), 780)        # key shot 3, held (note 38), Epstein clear
CAMS['epstein'] = ((-2.85, 1.85, 1.25), (-1.8, 1.75, 2.85), 1150)
CAMS['satan'] = ((0.3, 1.8, -0.35), (0.0, 1.85, 1.45), 1350)     # Satan from Trump's side, the desk and windows behind
CAMS['trump'] = ((-0.3, 1.72, 2.0), (0.7, 1.6, 1.0), 1150)      # the reverse (180): from Satan's side at Trump
SHOT_CAST = {'door': ['trump'], 'two': ['trump', 'satan'], 'satan': ['satan'], 'trump': ['trump'],
             'three': ['trump', 'satan', 'epstein'], 'epstein': ['epstein']}
LOOKS_AT = {'trump': 'satan', 'satan': 'trump', 'epstein': 'trump'}
TX, TZ = MV.WALK_TO
SX, SZ = MV.SATAN_AT
EX, EZ = MV.EPSTEIN_AT
PLAN = dict(CEIL=5.6, ROOMS=dict(MS.ROOMS, corridor=(4.42, -4.5, 7.0, 0.5)),   # the oval as its bounding box; the
            # east door (wall angle 112, curved) on the box's east side, where it meets the corridor
            OPENINGS={'east door': dict(wall=('x', 4.42), span=(-2.55, -1.5), sill=0.0, head=2.45,
                                        to='the West Wing corridor: cream walls, a red runner')},
            THINGS={'Resolute desk': dict(at=MS.DESK, size=(1.83, 0.91, 0.76), facing=180, why='ref oval-1')},
            PEOPLE={'trump': dict(at=(TX, TZ), facing=0, who='trump', why='his mark: right of Satan (note 23)'),
                    'satan': dict(at=(SX, SZ), facing=180, who='satan', why='floating before the desk'),
                    'epstein': dict(at=(EX, EZ), facing=150, who='epstein', why='beside the desk, left (note 23)')},
            CAMS={k: dict(pos=v[0], look=v[1], focal=v[2]) for k, v in CAMS.items()}, GROUPS={},
            SHOT_MARKS={'two': ['satan'], 'satan': ['satan'], 'trump': ['trump'], 'three': ['trump', 'satan', 'epstein'],
                        'epstein': ['epstein']})
BENCHMARK = [dict(place='oval office', refs=['oval-1-desk-gold.jpg', 'oval-3-both-ends.jpg', 'oval-5-fisheye.jpg'], at=T['cut2'] + 1.0,
                  items=[('gold swag valance and drapes', 'midterminal_set windows'), ('three tall windows', 'yes'),
                         ('Resolute desk', 'yes'), ('tufted leather chair', 'yes'), ('flags either side', 'yes'),
                         ('navy oval carpet with the seal', 'our own simplified seal'),
                         ('white pedimented doors', 'four'), ('fireplace with a portrait', 'yes (reverse)')])]
HOOK = ('Trump after Midterm results', {'y': 250})   # brief row 19, Sam's words exactly
KEEP_CLEAR, PROP_SIZES, OUTFIT = [], [], {}
HEIGHTS = {'trump': 1.90, 'satan': 1.88, 'epstein': 1.83}
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
# rule 38: everyone is DRAWN square to each shot's lens (MS.to_cam in every item); the plan's one facing per person
# cannot follow that, so these shots are listed with that reason (the stills sheet shows them front on)
THREE_QUARTER_OK = [('trump', 'trump', 'drawn turned square to the lens (MS.to_cam)'),
                    ('three', 'trump', 'drawn turned square to the lens (MS.to_cam)'),
                    ('epstein', 'epstein', 'drawn turned square to the lens (MS.to_cam)')]
# rule 2: the east door is shut until T['open'] (Sam's note 22: Trump hidden behind it until it opens): its white
# panels are the door, not a flat fill; once open the corridor shows
PORTAL_OK = [('east door', None, T['open'] + 0.1, 'shut until it opens, then the corridor (note 22)')]
ALLOWED_CONTACTS = []
ALLOWED_POPS = [('epstein', T['ghost'], T['ghost'] + 0.8, 'the ghost fades in'),
                ('epstein', T['melt'], T['gone'], 'the melt: he runs down in drips to a skeleton (note 41)'),
                ('epstein', T['gone'] - 0.9, T['gone'], 'the ghost fades away')]
SET_EXCLUDE = []
TOUCHES, FREE_MOVES, SOUND_SOURCES = [], [], {}
EFFECTS = [('hellfire', 'flames', lambda im: MV.flames(__import__('PIL.ImageDraw').ImageDraw.Draw(im), 540, 1500,
                                                         400, 560, 0.0, 11, n=6, bed=True))]
JOKE_PROPS = []
ORDER_SWAPS = []
HANDS_OK = []
# ====================================================================================================================


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


def _face(who, t):
    shape = mouths.at(TRACK[who], t)
    return dict(mouth='set' if shape == 'rest' else 'v:' + shape, blink=F.blinking(t, BLINKS[who]))


# ------------------------------------------------------------------------------------------------ the people


def door_d(t):
    """He stands just inside the open doorway talking to the press (off right) until 1.3 s before the slam, then strides
    in (Sam's note 1: the door open from the start, so we see him)."""
    return 0.6 + DOOR_WALK * max(0.0, t - (T['slam'] - 1.3))


def entry_d(t):
    return min(MV.path_length(MV.ENTRY), DOOR_WALK * (t - T['cut2']))


def trump_sp(t):
    """Trump's face: eyes to the press (right, off-screen) until the threshold; angry from line 2; mocking on line 10."""
    sp = dict(MC.TRUMP, **_face('trump', t))
    s = shot_of(t)
    if s == 'door':
        sp['look'] = -0.9 if door_d(t) < 1.2 else 0.0    # to the press, off LEFT (Sam's note 31)
        return sp
    sp['frown'] = 0.03
    if s == 'two':                                # note 32: eyes ahead on the walk; the breath; angry, eyes to Satan
        sp['look'] = -0.8 if t >= T['stop'] + 0.2 else -0.2
        sp['frown'] = 0.0 if t < T['angry'] else 0.05
    elif s == 'trump':
        sp['look'] = -0.35                        # at Satan, just off the lens to our left
        if T['cut4'] <= t < T['cut5']:            # note 35: exasperated (brows up), then accusing
            acc = t >= word_at(4, 'I thought') - 0.1
            sp['frown'] = 0.05 if acc else 0.0
            sp['brow_up'] = 0.0 if acc else 0.03
        if T['away'] <= t < T['back']:            # Q1: disgusted at Epstein's "so warm here, Donald"
            k = _ease(_ramp(t, T['away'], T['away'] + 0.25))
            sp['look'], sp['frown'], sp['lid4'] = -0.6, 0.08 * k, 0.38 * k    # brows down hard, eyes narrowed, mouth down
        if T['cut8'] <= t < T['cut9']:            # note 40: angry; eyes narrowed on "I know it's you"; smug at the end
            if t >= word_at(8, "I know") - 0.1:
                sp['lid4'], sp['frown'] = 0.42, 0.045
            if t >= word_at(8, 'reflecting') - 0.25:
                sp['lid4'], sp['frown'], sp['sneer'] = 0.3, 0.0, True
                sp['brow_up'] = (0.0, 0.03)
        if T['cut10'] <= t < T['cut11']:          # note 42: the childish mock: pout, brows up
            sp['frown'], sp['brow_up'], sp['pout'] = 0.0, 0.035, True
    if s == 'two' and t >= T['cut11']:            # note 43: furious at Satan
        sp['frown'], sp['look'] = 0.06, -0.8
    elif s == 'three':
        sp['look'] = -0.8 if t < T['eyes'] else -0.9
    return sp


FLASHES = (0.25, 0.58, 0.83, 1.25)               # press camera flashes, one frame each, from the left (note 31)


def flash_at(t):
    return 1.0 if any(int(f * FPS + 1e-6) == int(t * FPS + 1e-6) for f in FLASHES) else 0.0


def press_palm(j, t):
    """Shot 1: his hand up, palm out to the press on our left, "no, thank you" (Sam's note 31); down by the threshold."""
    k = _ease(_ramp(t, 0.15, 0.45)) * (1 - _ease(_ramp(t, L[1]['end'] - 0.35, L[1]['end'])))
    if k <= 0:
        return j
    sx, sy, sz = j['shL']
    wx, wy, wz = j['wrL']                         # the hand travels from where the walk has it up to by his face, the
    tx, ty, tz = sx - 95, sy - 175, sz + 110      # arm solved on the way (a blend of two poses swung the forearm at
    up = dict(j)                                  # the lens half way: rule 41)
    up['hand'] = dict(j.get('hand', {}))
    V.arm_to(up, 'L', (wx + (tx - wx) * k, wy + (ty - wy) * k, min(wz, tz) + (tz - min(wz, tz)) * k), 'down', 'palm')
    return up


def lift_shoulders(j, dy):
    """Shoulders (and the arms hanging from them, and the head) raised by dy (negative = up, in drawing units)."""
    for k in ('shL', 'shR', 'elL', 'elR', 'wrL', 'wrR'):
        if k in j:
            x, y, z = j[k]
            j[k] = (x, y + dy, z)
    j['head_dy'] = j.get('head_dy', 0) + dy
    return j


def word_at(n, words):
    """When line n reaches `words`: the share of the text before them, spread over the take's spoken stretches only
    (not its pauses); a phrase that starts a stretch snaps to that stretch's start (from the sound)."""
    ln = L[n]
    st = ln['_stretches']
    tot = sum(b - a for a, b in st) or 1.0
    k = ln['text'].index(words) / len(ln['text']) * tot
    for a, b in st:
        if k <= b - a:
            est = a + k
            break
        k -= b - a
    else:
        est = st[-1][1]
    near = min((a for a, _ in st), key=lambda a: abs(a - est))
    return ln['start'] + (near if abs(near - est) < 0.6 else est)


def jab(t, t0, n=2, each=0.36):
    """A jabbing finger: 0 (drawn back) .. 1 (thrust out), n quick jabs from t0, then held out."""
    u = (t - t0) / each
    if u < 0:
        return 0.0
    if u >= n:
        return 1.0
    f = u % 1.0
    return min(1.0, f / 0.3) if f < 0.3 else 1.0 - 0.6 * (f - 0.3) / 0.7


def _jabbed(j, k):
    """The pointing arm drawn back towards the shoulder by (1 - k) (k = jab(...))."""
    side = next((sd for sd in 'LR' if j.get('hand', {}).get(sd) == 'point'), None)
    if side is None:
        return j
    sx, sy, sz = j['sh' + side]
    wx, wy, wz = j['wr' + side]
    f = 0.55 + 0.45 * k
    V.arm_to(j, side, (sx + (wx - sx) * f, sy + (wy - sy) * f, sz + (wz - sz) * f), 'down', 'point')
    return j


def trump_j(t):
    """His whole-body acting, as a pose (None = standing / walking):
    line 2: the breath (note 32); line 4: palms flung up and out on "Yeah, because Bibi told me to" (note 35);
    line 8: hands on hips, then arms folded, smug, on "reflecting pool" (note 40); line 10: the floppy silly-ghost wave,
    head waggling (note 42)."""
    sp = MC.TRUMP
    s = shot_of(t)
    if s == 'two' and T['stop'] <= t < T['angry']:   # a quick breath: shoulders up and down once (a beat, not a bob)
        return lift_shoulders(V.standing(sp), -14 * math.sin(math.pi * (t - T['stop']) / (T['angry'] - T['stop'])))
    if s == 'trump' and T['cut4'] <= t < word_at(4, 'I thought') - 0.1:
        k = _ease(_ramp(t, L[4]['start'], L[4]['start'] + 0.18))      # flung, fast
        up = V.standing(sp)
        for side in 'LR':
            sx, sy, sz = up['sh' + side]
            g = -1 if side == 'L' else 1
            V.arm_to(up, side, (sx + g * 185, sy - 30, sz + 110), 'down', 'palm')    # up and out, above the shoulders
        lift_shoulders(up, -12)
        return moves.mix_poses(V.standing(sp), up, k)
    if s == 'trump' and T['away'] <= t < T['back']:   # recoiling a little from the ghost
        j = V.standing(sp)
        j['lean'] = -5 * _ease(_ramp(t, T['away'], T['away'] + 0.3))
        return j
    if s == 'trump' and T['cut8'] <= t < T['cut9']:
        fold = word_at(8, 'reflecting') - 0.25
        if t < fold:
            return moves.pose(sp, 'hips')
        return moves.mix_poses(moves.pose(sp, 'hips'), moves.pose(sp, 'arms_folded'), _ease(_ramp(t, fold, fold + 0.3)))
    if s == 'trump' and T['cut10'] <= t < T['cut11']:
        u = 0.5 + 0.5 * math.sin(2 * math.pi * (t - L[10]['start']) / 0.42)
        a, b = V.standing(sp), V.standing(sp)   # Epstein's silly-ghost wave, smaller and floppier (wrists low)
        V.arm_to(a, 'L', (-260.0, 40.0, 20.0), 'down', 'palm')   # out to the sides, never at the lens (rule 41)
        V.arm_to(a, 'R', (230.0, -10.0, 20.0), 'down', 'palm')
        V.arm_to(b, 'L', (-230.0, -10.0, 20.0), 'down', 'palm')
        V.arm_to(b, 'R', (260.0, 40.0, 20.0), 'down', 'palm')
        j = moves.mix_poses(a, b, _ease(u))      # already waving on the cut (a blend from standing folded his elbow)
        j['tilt'] = 7 * math.sin(2 * math.pi * 2.4 * (t - L[10]['start']))     # head waggling
        return j
    return None


def satan_j(t):
    """The shrug on line 3: shoulders snap up, elbows at his sides, forearms up and out, palms up by the hips (Sam's
    note 34: quick and noticeable, never arms hanging in a U); the chuckle on line 5 (shoulders bobbing); the flinch
    on line 10's second sentence (note 43)."""
    sp = MC.SATAN
    j0 = V.standing(sp)
    a, b = L[3]['start'] + 0.3, L[3]['end'] - 0.1
    u = _ease(_ramp(t, a, a + 0.15)) * (1 - _ease(_ramp(t, b, b + 0.3)))
    if u > 0:
        sh = V.standing(sp)
        for side in 'LR':
            sx, sy, sz = sh['sh' + side]
            g = -1 if side == 'L' else 1
            V.arm_to(sh, side, (sx + g * 70, sy + 150, sz + 210), 'back', 'palm')   # elbows in, forearms forward
        lift_shoulders(sh, -24)
        return moves.mix_poses(j0, sh, u)
    if L[5]['start'] - 0.1 <= t < L[5]['end'] + 0.4:
        j0['head_dy'] = 4 * abs(math.sin(2 * math.pi * 3.0 * t))   # the chuckle: little shoulder-and-head bobs
    if t >= T['flinch']:                           # note 43: he flinches back a little from the jabbing finger
        k = _ease(_ramp(t, T['flinch'], T['flinch'] + 0.15))
        j0['tilt'] = j0.get('tilt', 0) - 5 * k
        j0['head_dx'] = j0.get('head_dx', 0) + 6 * k
        lift_shoulders(j0, -6 * k)
    return j0


def satan_sp(t):
    sp = dict(MC.SATAN, **_face('satan', t))
    s = shot_of(t)
    sp['look'] = {'two': 0.6, 'satan': 0.55, 'three': 0.6}.get(s, 0.0)
    if s == 'three' and t >= T['eyes']:
        sp['look'] = -0.8                         # his pupils go to the ghost (brief 13)
    if t >= T['flinch']:                          # note 43: one brow up, sceptical, mouth flat
        k = _ease(_ramp(t, T['flinch'], T['flinch'] + 0.2))
        sp['brow_up'] = (0.0, 0.035 * k)
        sp['mood'] = 'stern'
        return sp
    if L[5]['start'] - 0.2 <= t < T['cut6'] + 0.5 or s == 'three':
        sp['mood'] = 'smirk'
    return sp


def satan_item(t):
    lift, spread = MV.satan_float(t)
    j = satan_j(t)
    sp = dict(satan_sp(t), spread=spread)

    def draw(im, c):
        MS.put(im, c, sp, SX, SZ, MS.to_cam(c, SX, SZ), j, t, lift=lift)
    return (SX, SZ, draw)


WAVE = 0.5                                       # one silly-ghost wave (up-left, up-right) every half second


def epstein_j(t):
    if L[9]['start'] - 0.2 <= t < T['gone']:
        sp = MC.EPSTEIN
        u = 0.5 + 0.5 * math.sin(2 * math.pi * (t - L[9]['start']) / WAVE)
        a = PG.flapping(sp, 'up')
        b = PG.flapping(sp, 'up')
        V.arm_to(a, 'L', (-330.0, -40.0, 60.0), 'out', 'palm')
        V.arm_to(a, 'R', (260.0, -120.0, 60.0), 'out', 'palm')
        V.arm_to(b, 'L', (-260.0, -120.0, 60.0), 'out', 'palm')
        V.arm_to(b, 'R', (330.0, -40.0, 60.0), 'out', 'palm')
        k = _ease(_ramp(t, L[9]['start'] - 0.2, L[9]['start'] + 0.15))
        return moves.mix_poses(V.standing(sp), moves.mix_poses(a, b, _ease(u)), k)
    a, b = word_at(7, 'Why') - 0.15, word_at(7, "It's so warm") + 0.2
    k = _ease(_ramp(t, a, a + 0.3)) * (1 - _ease(_ramp(t, b, b + 0.4)))
    if k > 0:                                     # note 39: arms open, imploring, on "why don't you come and join me?"
        sp = MC.EPSTEIN
        op = V.standing(sp)
        for side in 'LR':
            sx, sy, sz = op['sh' + side]
            g = -1 if side == 'L' else 1
            V.arm_to(op, side, (sx + g * 160, sy + 150, sz + 170), 'down', 'palm')
        op['lean'] = 4
        return moves.mix_poses(V.standing(sp), op, k)
    return None


def epstein_fade(t):
    if t < T['ghost']:
        return 0.0
    if t < T['cut9']:
        return _ease(_ramp(t, T['ghost'], T['ghost'] + 0.8))
    return 1 - _ease(_ramp(t, T['gone'] - 0.9, T['gone']))


def epstein_item(t):
    melt = _ease(_ramp(t, T['melt'], L[9]['end'] - 0.2))
    sp = dict(MC.EPSTEIN, **_face('epstein', t))
    if melt > 0:
        sp['mouth'] = 'v:o' if t < L[9]['end'] else 'set'
    return MV.epstein_item(t, sp, epstein_fade(t), melt, look=0.8 if shot_of(t) == 'epstein' else 0.6,
                           j=epstein_j(t), arrive=t - T['ghost'] if shot_of(t) == 'three' else None)


def trump_item(t):
    s = shot_of(t)
    if s == 'door':
        return MV.trump_item(t, door_d(t), trump_sp(t), walking=t >= T['slam'] - 1.3, arms=lambda j, c, x, z: press_palm(j, t))
    sp = trump_sp(t)
    j = trump_j(t)
    point = None
    accusing = s == 'trump' and word_at(4, 'I thought') - 0.1 <= t < T['cut5']   # note 35: lean in, jab twice
    if (s == 'two' and t >= L[2]['start'] - 0.15) or accusing:
        point = (SX, 1.45 + MV.satan_float(t)[0], SZ) if s == 'two' else (0.1, 1.6, 1.75)
    t_jab = word_at(4, 'I thought') if accusing else T['cut11'] + 0.1 if t >= T['cut11'] else None

    def arms(jj, c, x, z):
        if j is not None:
            jj = MV._copy(j)
        if point is not None:
            MV.point_at(jj, c, x, z, point)
            if t_jab is not None:                  # notes 35 and 43: jabbing the finger
                _jabbed(jj, jab(t, t_jab))
                jj['lean'] = jj.get('lean', 0) + 7 * _ease(_ramp(t, t_jab - 0.1, t_jab + 0.15))
        return jj
    return MV.trump_item(t, entry_d(t) if s == 'two' else MV.path_length(MV.ENTRY), sp, front=True, pts=MV.ENTRY,
                         arms=arms)


SOLO = [None]                                    # the audit draws one person alone


def cam_for(t):
    s = shot_of(t)
    pos, look, focal = CAMS[s]
    return MS.S.Cam(pos, look, focal=focal)


def people(t):
    s = shot_of(t)
    out = []
    if s == 'door':
        out += MV.door_items(MV.door_curve(t, T['open'], T['open'] + 0.35, T['slam']), flash_at(t))
    want = SHOT_CAST[s]
    if s == 'satan' or s == 'trump':              # singles: the other is behind the camera
        pass
    if 'trump' in want and SOLO[0] in (None, 'trump'):
        out.append(trump_item(t))
    if 'satan' in want and SOLO[0] in (None, 'satan'):
        out.append(satan_item(t))
    if ('epstein' in want or s == 'three') and epstein_fade(t) > 0 and SOLO[0] in (None, 'epstein'):
        out.append(epstein_item(t))
    return out


def picture(t):
    """The frame WITHOUT captions (they go on last, so wording notes never re-render a picture)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    img = Image.new('RGBA', (1080 * B.SS, 1920 * B.SS), (0, 0, 0, 255))
    MS.render(img, cam_for(t), people(t))
    return img


def draw_order(t):
    """Rule 57: back to front, as MS.render sorts by distance from the camera."""
    if t >= BLACK_AT:
        return []
    c = cam_for(t)
    pos = {'trump': (TX, TZ), 'satan': (SX, SZ), 'epstein': (EX, EZ)}
    names = [w for w in SHOT_CAST[shot_of(t)] if w != 'epstein' or epstein_fade(t) > 0]
    return ['background'] + sorted(names, key=lambda w: -math.dist((pos[w][0], 1.0, pos[w][1]), c.pos))


def caption_at(t):
    for i, ln in enumerate(LINES):
        nxt = LINES[i + 1]['start'] - 0.05 if i + 1 < len(LINES) else 1e9
        if ln['start'] - 0.05 <= t < min(ln['end'] + 0.45, nxt):
            return SUB.line_caption(ln, t - ln['start'])
    return None


def overlay(img, t):
    if t < BLACK_AT:
        c = caption_at(t)
        if c:
            PP.caption(img, c)
    return img


def frame_image(t):
    return overlay(picture(t), t)


SFX = {'slam': os.path.join(HERE, 'audio', 'midterminal-slam.m4a'),     # Sam's files (4 Nov): door slam,
       'fire': os.path.join(HERE, 'audio', 'midterminal-fire.m4a')}       # fire breath at double speed


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)        # no room tone (Sam, 19 Oct)
    for ln in LINES:
        if ln['_voice'] is not None:
            s = int(ln['start'] * SR)
            seg = ln['_voice'][:max(0, n - s)]
            voice[s:s + len(seg)] += seg
    if os.path.exists(SFX['slam']):
        slam = MA.load(SFX['slam']) if hasattr(MA, 'load') else __import__('burnham_film').load(SFX['slam'])
        filmkit.place(rest, slam[:int(1.0 * SR)], at=T['slam'] + 0.25, sr=SR, gain=0.9)
    if os.path.exists(SFX['fire']):               # Sam, 4 Nov: the fire breath (double speed) as his Hell entrance
        fire = MA.load(SFX['fire']) if hasattr(MA, 'load') else __import__('burnham_film').load(SFX['fire'])
        from scipy.signal import butter, sosfiltfilt
        fire = sosfiltfilt(butter(4, 90, 'high', fs=SR, output='sos'), fire)   # its deep rumble cut (pre-flight)
        for at in (T['ghost'] - 0.1, T['gone'] - 1.0):      # and exit, under the flame burst and the fade away
            filmkit.place(rest, fire, at=at, sr=SR, gain=0.6)
    mix = voice + rest
    end = int(BLACK_AT * SR)
    if np.abs(voice).max() > 1e-6:
        mix, g = MA.master(mix, end)
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
        faults += MA.limit_check(raw, int(BLACK_AT * SR))
    mix, voice, rest = soundtrack(stems=True)
    faults += filmkit.hiss_check(mix, SR, BLACK_AT, voice=voice + rest)
    for q in filmkit.sound_questions({'voice': voice, 'background': rest, 'mix': mix}, SR,
                                     cuts=[a for _, a, _ in SHOTS[1:]], end=BLACK_AT):
        print('QUESTION FOR SAM:', q)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


# ------------------------------------------------------------------------------------------------ the audit
def scene(t):
    import audit
    s = shot_of(t)
    out = []
    for who in SHOT_CAST[s]:
        if who == 'trump':
            if s == 'door':
                x, z, _ = MV.trump_path(door_d(t))
            elif s == 'two':
                x, z, _ = MV.trump_path(entry_d(t), MV.ENTRY)
            else:
                x, z = TX, TZ
            out.append(audit.Thing('trump', audit.simple('trump', x, z, HEIGHTS['trump'])))
        elif who == 'satan':
            out.append(audit.Thing('satan', audit.simple('satan', SX, SZ, HEIGHTS['satan'], base=MV.satan_float(t)[0])))
        elif who == 'epstein' and epstein_fade(t) > 0.5:
            out.append(audit.Thing('epstein', audit.simple('epstein', EX, EZ, HEIGHTS['epstein'], base=0.5)))
    return out


def audits():
    """The general audit: each person alone over every frame they are on screen. Returns faults."""
    def alone(who):
        def draw(t):
            SOLO[0] = who
            try:
                lay = Image.new('RGBA', (1080 * B.SS, 1920 * B.SS), (0, 0, 0, 0))
                for _, _, fn in people(t):
                    fn(lay, cam_for(t))
                return lay
            finally:
                SOLO[0] = None
        return draw
    actors = {}
    for who in WHO:
        for shot, a, b in SHOTS:
            if who in SHOT_CAST[shot]:
                ts = [i / FPS for i in range(math.ceil(a * FPS), int(b * FPS))     # ceil: never the frame before the cut
                      if who != 'epstein' or epstein_fade(i / FPS) > 0.5]
                if ts:
                    actors[f'{who} [{shot} {a:.1f}]'] = (ts, alone(who))
    filmkit.EYES.clear()
    faults = filmkit.silhouette_audit(actors, fps=FPS, still_ok=(),
                                      allow=[(k, t0, t1, why) for n, t0, t1, why in ALLOWED_POPS for k in actors
                                             if k.startswith(n + ' [')])
    faults += moves.audit()
    return faults


def LINE_SUBJECTS():
    def one(who):
        def d(im):
            V.person(im, MS.FLAT, 540, 420, 1.2, dict(CAST[who], full=True, pose='custom'), 0.0, 0.0)
        return d
    return [(who, one(who)) for who in WHO]


def main():
    a = sys.argv[1:]
    if a[0] == 'shots':
        for s in SHOTS:
            print(f'{s[0]:8s} {s[1]:6.2f} {s[2]:6.2f}')
        for ln in LINES:
            print(ln['n'], ln['who'], round(ln['start'], 2), round(ln['end'], 2), 'take' if ln['_voice'] is not None else 'est')
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
        f += [x[len('AUDIT: '):] for x in audit.check(sys.modules[__name__])]
        print('\n'.join(['AUDIT: ' + x for x in f]) or 'audit: clean')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)


F.guard(B)
import limbs                     # noqa: E402
limbs.install(B)

if __name__ == '__main__':
    main()
