#!/usr/bin/env python3
"""Ad-Vanced Notice (notes/ad-vanced-notice.md): JD Vance's campaign ad. He swivels round in his study to say hello,
walks calmly at us along a cliff over the Strait of Hormuz while a missile turns the tanker behind him into an oil
fire, tells us in close-up none of this is his fault, then puts his arm round a furious driver at a Midwest gas
station. Built from the satire template (guides/satire.md); every place is a flat painting, one per camera
(ad_vanced_notice_sets), the explosion is ad_vanced_notice_fx, the cast ad_vanced_notice_cast.

    python3 source/ad_vanced_notice.py stills OUT_DIR T [T ...]   stills at these times (seconds)
    python3 source/ad_vanced_notice.py keys OUT.jpg               one labelled still per beat (the check sheet)
    python3 source/ad_vanced_notice.py shots                      the timeline in numbers
    python3 source/ad_vanced_notice.py check                      every check and the audit (also run by preflight.py)
    python3 source/ad_vanced_notice.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1] [--nostamp]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

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
import ad_vanced_notice_sets as ST   # noqa: E402  the study, the cliff and strait, the gas station
import ad_vanced_notice_fx as X      # noqa: E402  the showstopper
import ad_vanced_notice_cast as AC   # noqa: E402  Vance, the driver
import ad_vanced_notice_comp as CP   # noqa: E402  (the cast's setup and screen placing)
import sitting                   # noqa: E402  the swivel chair, hands folded
import moves                     # noqa: E402  the walks
import views as V                # noqa: E402
from satire_style import install_circle_hands, OUT   # noqa: E402

mouths.install(B)
install_circle_hands(B)
CP.setup()
FPS, SR = 12, MA.SR

# =============================================== STORY =============================================================
# MAP (rule 61: keep it in step; a note is answered by reading only these lines):
#   the cast: ad_vanced_notice_cast.py; the sets: ad_vanced_notice_sets.py; the explosion: ad_vanced_notice_fx.py
#   (each has its own MAP). Here: LINES (the script by number; est = seconds until Sam's take replaces it) 60 | the
#   timeline T 95 | SHOTS, marks, checks' lists 125 | the acting beats 175 | the study 215 | the cliff 270 | the
#   close-up 320 | the gas station 335 | picture, captions, sound 420 | checks, audit 470 | sheets, main 520.
NAME = 'ad-vanced-notice'
HAS = {'people', 'rooms', 'voices', 'effects', 'props'}
TITLE = ()                                        # no title (CLAUDE.md)
TITLE_AT = dict(cap=116, top=310)
CAST = AC.CAST
WHO = ('vance', 'man')
# The script, word for word (brief rows 7, 13, 19, 25, 26). Sam records every voice; until the takes come, each line
# runs `est` seconds.
LINES = [
    dict(n=1, audio='ad-vanced-notice-1', who='vance', est=2.6, text="Hello, America. I'm J.D Vance."),
    dict(n=2, audio='ad-vanced-notice-2', who='vance', est=2.5, text="I know things haven't gone well recently."),
    dict(n=3, audio='ad-vanced-notice-3', who='vance', est=1.7, text='That you have your concerns.'),
    dict(n=4, audio='ad-vanced-notice-4', who='vance', est=2.4, text="But there's something I need you to know."),
    dict(n=5, audio='ad-vanced-notice-5', who='vance', est=1.9, text='None of this is my fault.'),
    dict(n=6, audio='ad-vanced-notice-6', who='vance', est=1.5, text='Aggravating, right?'),
    dict(n=7, audio='ad-vanced-notice-7', who='vance', est=1.9, text="You know who isn't responsible?"),
    dict(n=8, audio='ad-vanced-notice-8', who='vance', est=1.0, text='This guy.'),
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
        ln['_voice'] = x
        dur = len(x) / SR
    ln['_dur'] = dur
    ln['_stretches'] = MA.pauses(ln['_voice'], 0.18) if ln['_voice'] is not None else [(0.0, dur)]


def _at(n, start):
    L[n]['start'] = start
    L[n]['end'] = start + L[n]['_dur']
    return L[n]['end']


def word_at(n, words):
    """When line n reaches `words`: the share of the text before them, spread over the take's spoken stretches."""
    ln = L[n]
    st = ln['_stretches']
    tot = sum(b - a for a, b in st) or 1.0
    k = ln['text'].index(words) / len(ln['text']) * tot
    for a, b in st:
        if k <= b - a:
            return ln['start'] + a + k
        k -= b - a
    return ln['start'] + st[-1][1]


# The timeline: each beat follows the one before, so a take that runs long pushes the rest on.
T = {}
GAP = 0.3                                         # between one line's last word and the next one's first
CLEAR = 0.225                                     # a cut waits till the last subtitle clears
SWIVEL = 0.8                                      # the kit's swivel turn (note 27)
T['swivel'] = 0.1                                 # brief row 0: the film opens on him swivelling round
T['fold'] = T['swivel'] + SWIVEL                  # his hands come down onto the desk, folded (0.4 s)
e = _at(1, T['fold'] + 0.45)                      # "Hello, America." (acting 1: nod on "America")
T['cut2'] = e + 0.55                              # shot 2: the cliff; he is already walking, mid-stride
e = _at(2, T['cut2'] + 0.45)
e = _at(3, e + GAP)
e = _at(4, e + GAP)
T['stop'] = word_at(4, 'need') - 0.15             # acting 4: he stops at his mark on "need"
T['hit'] = e + 0.75                               # the missile lands (it drops for 0.4 s before)
T['cut3'] = T['hit'] + 2.6                        # shot 3: the close-up (Sam, 8 Nov, note 33: cut at 15.5 s and
e = _at(5, T['cut3'] + 0.45)                      # carry on the showstopper from there); line 5 within half a
                                                  # second of the cut (note 36)                      # "None of this is my fault." (smile on "fault")
T['cut4'] = e + 0.7                               # shot 4: the gas station; the driver glares at the board
T['enter'] = T['cut4'] + 0.9                      # Vance walks in from the right (brief 24)
WALK_IN = 1.5                                     # seconds from the frame edge to his mark beside the driver
T['arm'] = T['enter'] + WALK_IN                   # his arm goes round the driver's shoulders (0.45 s)
e = _at(6, T['arm'] + 0.35)                       # "Aggravating, right?" (squeeze on "right")
e = _at(7, e + GAP)                               # "You know who isn't responsible?" (leans in)
T['off'] = e + 0.1                                # the arm comes off (0.35 s), thumbs to his chest
e = _at(8, T['off'] + 0.4)                        # "This guy." (thumbs on "This")
DUR = e + 1.4                                     # (the script continues here: Sam, brief row 26)
BLACK_AT = DUR

SHOTS = [('study', 0.0, T['cut2']), ('cliff', T['cut2'], T['cut3']), ('close', T['cut3'], T['cut4']),
         ('gas', T['cut4'], DUR)]
SHOT_CAST = {'study': ['vance'], 'cliff': ['vance'], 'close': ['vance'], 'gas': ['vance', 'man']}
LOOKS_AT = {'vance': 'lens', 'man': 'board'}
# Marks, in each set's own metres (ad_vanced_notice_sets): the study's chair; the cliff walk to his mark; the gas
# station's two marks on the forecourt, 4.5 m from the lens
STROLL = 'stroll'                                 # brief row 12: "walking calmly and gently towards the camera"
CLIFF_V = moves.speed(STROLL)                     # 0.57 m/s
CLIFF_FROM = (ST.VANCE_MARK[0] + 0.25, ST.VANCE_MARK[1] + CLIFF_V * (T['stop'] - T['cut2']))
GAS_IN = 1.4                                      # world x where he comes in (just off frame right)
PLAN = dict(CEIL=3.2, ROOMS={'study': (-2.6, 0.0, 2.6, ST.D_WALL)},
            OPENINGS={}, THINGS={'desk': dict(at=(0.0, ST.D_FAR), size=(1.8, 0.8, 0.82), facing=180, why='brief 2')},
            PEOPLE={'vance': dict(at=(0.0, ST.D_V), facing=180, who='vance', why='behind the desk (brief 2)')},
            CAMS={'study': dict(pos=(0.0, 1.45, 0.0), look=(0.0, 1.45, 5.0), focal=1600),
                  'cliff': dict(pos=(0.0, 1.6, 0.0), look=(0.0, 1.6, 5.0), focal=ST.CLIFF_F),    # (its own world:
                  'close': dict(pos=(0.0, 1.7, 0.0), look=(0.0, 1.7, 5.0), focal=1500),          # sets, strait)
                  'gas': dict(pos=(0.0, 1.5, 0.0), look=(0.0, 1.5, 5.0), focal=1300)}, GROUPS={},
            SHOT_MARKS={'study': ['vance']})
BENCHMARK = ST.BENCHMARK
HOOK = ('JD Vance Addresses The Nation', {'y': 330, 'until': 3.9})   # Sam, 8 Nov (his capitals); pops at 0.5 s
KEEP_CLEAR = [('his face', lambda t: (300, 470, 780, 900) if t < T['cut2'] else None)]
PROP_SIZES, OUTFIT = [], {}
HEIGHTS = {'vance': 1.88, 'man': 1.80}
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
THREE_QUARTER_OK = []
ALLOWED_CONTACTS = [('vance*', 'man*', T['arm'] - 0.3, T['off'] + 0.5, "his arm round the driver's shoulders, "
                      'standing close beside him')]
ALLOWED_POPS = [('vance', T['enter'], T['enter'] + 0.6, 'walking in from the frame edge'),
                ('vance', T['enter'] + 0.6, T['arm'] + 0.15, 'side on, walking across the frame at 0.5 m a frame, then '
                 'the standard turn to the lens at his mark (checked by eye, 8 Nov: legs and arms whole every frame)')]
SET_EXCLUDE = [('WALL', 'every shot is a flat painting through its own camera; the study plan has no walls the '
                'outdoor shots stand in')]
TOUCHES = []                                      # the nozzle is drawn at his fist every frame (_nozzle): it never moves
FREE_MOVES, SOUND_SOURCES = [], {}
RESTS = [('*Vance.forearm*', 'desk', T['fold'] + 0.4, T['cut2'], 'line 1: hands folded on the desk')]
EFFECTS = X.EFFECTS
JOKE_PROPS = []
ORDER_SWAPS = []
HANDS_OK = [('*Vance*', '*', 'no hand', 0.0, T['swivel'] + SWIVEL * 0.7, 'his back to us in the swivel chair: '
             'his hands are in front of him; they come round with him'),
            ('*Vance*', 'R', '*sleeve*', T['stop'], L[4]['end'] + 0.6, 'the open hand rising beside his chest on '
             '"need" (acting 4): looked at full size, 8 Nov: the hand shows beside the chest, the forearm short'),
            ('*driver*', 'R', '*', T['enter'], DUR, "standing close beside him, the driver's fist hangs at his side "
             "in front of Vance's jacket (no touch: a hand's width in front)")]
LINE_OK = [('vance', 'edge with no line', 538, 313),     # the beard: inked round its outer edge only (Sam's note 7)
           ('man', 'line weight', 505, 230), ('man', 'line weight', 575, 230),   # his angry brows (anger 4): solid
           ('man', 'line weight', 509, 245), ('man', 'line weight', 571, 245)]   # shapes, not lines
# The acting list (rule 74) is in notes/ad-vanced-notice.md, "Acting"; each beat below names its line.
# ====================================================================================================================


def cut_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


shot_of = cut_of


def _ramp(t, a, b):
    return min(1.0, max(0.0, (t - a) / (b - a)))


def _ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def _bump(t, a, b, rise=0.2, fall=0.25):
    return _ease(_ramp(t, a, a + rise)) * (1 - _ease(_ramp(t, b - fall, b)))


TRACK = {w: [(a + ln['start'], b + ln['start'], sh) for ln in LINES if ln['who'] == w
             for a, b, sh in mouths.track(ln['text'], ln['_stretches'])] for w in WHO}
BLINKS = {w: F.blinks(31 + i, 0.5, DUR, talking=True) for i, w in enumerate(WHO)}


# The acting list (rule 74): (line, word, brows, nod px, tilt degrees), each over about 0.7 s
BEATS = [(1, 'America', 4, 7, 0),                 # nod on "America"
         (2, "haven't", 7, 0, 0),                 # brows up a touch in the middle on "haven't gone well"
         (3, 'concerns', 3, 0, 5),                # understanding tilt on "concerns"
         (4, 'need', 2, 3, 0),                    # earnest, the stop on "need"
         (6, 'right', 4, 0, -3),                  # the squeeze on "right"
         (7, 'responsible', 8, 0, 4),             # eyebrows up, teasing, the lean on "responsible"
         (8, 'This', 3, 4, 0)]                    # thumbs on "This"


def beat(t):
    b = n = tl = 0.0
    for ln, word, db, dn, dt in BEATS:
        a = word_at(ln, word) - 0.1
        if a - 0.05 <= t < a + 0.75:
            k = _bump(t, a, a + 0.7, 0.15, 0.3)
            b, n, tl = b + db * k, n + dn * math.sin(math.pi * min(1.0, (t - a) / 0.5)) * (t >= a), tl + dt * k
    return b, n, tl


def face(who, t, mood):
    shape = mouths.at(TRACK[who], t)
    d = dict(mood=mood, mouth='rest' if shape == 'rest' else 'v:' + shape, blink=F.blinking(t, BLINKS[who]))
    if who == 'vance':
        d['brow_up'] = beat(t)[0] * 0.004
    return d


def vance_mood(t):
    """Acting list: warm half-smile (1), sincere walking (2-4), calm with a small smile (5), cheerful (6), teasing (7),
    proud (8); the big grin as he swivels round (brief row 0)."""
    if t < T['fold'] + 0.2:
        return 'smile'
    if t < T['cut2']:
        return 'neutral'
    if t < T['cut4']:
        return 'smile' if L[5]['start'] <= t and t >= word_at(5, 'fault') - 0.1 else 'sincere'
    if t < L[7]['start'] - 0.1:
        return 'smile'
    if t < T['off']:
        return 'teasing'
    return 'proud'


def _head(j, t, seed=1, lean=True):
    """The acting beats on the head, plus idle life: never frozen; held poses with small quick shifts, no sway."""
    _, n, tl = beat(t) if seed == 1 else (0.0, 0.0, 0.0)
    j['head_dy'] = j.get('head_dy', 0) + n + F.breath(t, 4.0, 5.0, 0.3 * seed)
    if lean:                                      # (the kit has no head tilt: the beat's tilt is a small lean;
        j['lean'] = j.get('lean', 0) + 0.5 * tl + filmkit.shifts(t, seed=seed, amount=1.6, hold=(0.9, 1.7))   # seated: none, rule 78)
    return j


# ---------------------------------------------------------------------------------------------- shot 1: the study
SEAT = sitting.Seat('office', desk=sitting.Desk(), back_top=440, col=ST.CHAIR,
                    top=ST.mix(ST.CHAIR, (255, 255, 255), 0.12))   # note 27: the kit's swivel chair, oxblood leather


def _in_study(j):
    """The kit chair drawn, the kit desk not (the set paints its own); the painted desk top between his body and his
    forearms, so they rest on it (rule 78)."""
    j['pre'] = []
    j['mid'] = [lambda p, j2, view: SEAT.draw(p, view, j, 'mid'),
                lambda p, j2, view: p.img.alpha_composite(ST.study_desktop())]
    return j


def study_j(t):
    """(joints, yaw, head_yaw): the swivel round to us (0.8 s), then the steepled hands come down to fold on the desk
    (0.4 s), then hands folded with his acting (line 1)."""
    sp = AC.VANCE
    if t < T['fold']:
        spec = sitting.swivel(sp, SEAT, _ramp(t, T['swivel'], T['fold']))
        return _in_study(sitting.realize(sp, SEAT, spec)), spec['yaw'], spec['head_yaw']
    a = sitting.realize(sp, SEAT, sitting.spec_steeple(sp, SEAT))
    b = sitting.realize(sp, SEAT, sitting.spec_hands_folded(sp, SEAT))
    k = _ease(_ramp(t, T['fold'], T['fold'] + 0.4))
    j = moves.mix_poses(a, b, k)
    j = dict(j, **{q: (b if k >= 1 else a)[q] for q in ('spec', 'seat', 'seated', 'lap')})   # resting once down
    return _head(_in_study(j), t, lean=False), 0.0, None


def study(t):
    im = ST.study_back(t, chair=False)
    j, yaw, hy = study_j(t)
    v = ST.STUDY_VANCE
    V.person(im, AC.B.Cam(1.0, 540, 960), v['x'], v['neck_y'], v['s'], dict(AC.VANCE, **face('vance', t, vance_mood(t))),
             t, yaw, j, head_yaw=hy)
    im.alpha_composite(ST.study_front())
    return im


# ---------------------------------------------------------------------------------------------- shot 2: the cliff
def cliff_at(t):
    """(world x, y, joints): walking slowly at the lens from CLIFF_FROM (already mid-stride at the cut), stopping at
    his mark on "need" (acting 4), one open hand coming up to chest height; then still, never looking round."""
    sp = AC.VANCE
    if t < T['stop']:
        k = (t - T['cut2']) / (T['stop'] - T['cut2'])
        x = CLIFF_FROM[0] + (ST.VANCE_MARK[0] - CLIFF_FROM[0]) * k
        y = CLIFF_FROM[1] + (ST.VANCE_MARK[1] - CLIFF_FROM[1]) * k
        j = moves.gait(sp, t - T['cut2'] + 0.37, STROLL)
    else:
        j = moves.mix_poses(moves.gait(sp, T['stop'] - T['cut2'] + 0.37, STROLL), V.standing(sp),
                            _ease(_ramp(t, T['stop'], T['stop'] + 0.35)))
        x, y = ST.VANCE_MARK
    h = _bump(t, word_at(4, 'need') - 0.2, L[4]['end'] + 0.5, 0.35, 0.4)   # the open hand, chest height
    if h > 0.01:
        V.arm_to(j, 'R', (60 + 70 * h, 330 - 150 * h, 40 + 50 * h), 'down', 'palm')   # beside his chest, not at us
    return x, y, _head(j, t)


def cliff(t):
    u = t - T['hit']
    v = X.held(u)
    im = ST.strait('wide', t, X.near(v), X.fx(v))
    x, y, j = cliff_at(t)
    sx, sy, ppm = ST.place_cliff(x, y)
    ST.cliff_shadow(im, sx, sy, ppm)
    CP.person(im, AC.VANCE, sx, sy, ppm, 0, j, **face('vance', t, vance_mood(t)))
    im = X.light(im, v)
    return X.shift(im, *X.jolt(u))


# ---------------------------------------------------------------------------------------------- shot 3: the close-up
def close(t):
    u = t - T['hit']
    im = ST.strait('close', t, X.near(u), X.fx(u))
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
    j = _head(V.standing(AC.VANCE), t)
    CP.person(lay, AC.VANCE, 430, 1920 + 1500, 1500, 0, j, **face('vance', t, vance_mood(t)))
    im.alpha_composite(X.hellfire(lay, u))            # note 31: lit a little by the fire over his left shoulder
    return X.light(im, u, ST.CLOSE)


# ---------------------------------------------------------------------------------------------- shot 4: the gas station
MAN_X = ST.MAN_X + 0.45                           # the driver, further right (note 35): the board up to his left
GAS_VX, GAS_VD = MAN_X + 0.24, 4.66               # Vance's mark: in close behind the driver's shoulder (note 34)
STEP_OUT = 0.34                                   # m: the side step out for "This guy.", clear of the driver
STEP_FWD = 0.0                                    # (note 37: stepping forward took him through the driver)
ARM_ROUND = (-300.0, 40.0, 60.0)                  # his left hand on the driver's far shoulder (Vance's own units)
THUMBS = {'L': (-80.0, 115.0, 125.0), 'R': (80.0, 115.0, 125.0)}   # both index fingers up and in at his chest
# (note 37: the pointing finger from the earlier films; the elbows low, so each finger points up at his chest)


def gas_vance(t):
    """(world x, yaw, joints): walking in from the right, side on, turning front-on at his mark (yaw 0) as his arm
    goes round the driver; the squeeze on "right"; leaning in on "responsible"; the arm off and both thumbs at his
    chest for "This guy." (acting 6-8)."""
    sp = AC.VANCE
    if t < T['arm'] - 0.25:
        k = _ramp(t, T['enter'], T['arm'] - 0.25)
        x = GAS_IN + (GAS_VX - GAS_IN) * k
        return x, -90.0, moves.gait(sp, t - T['enter'], 'walk')
    j = V.standing(sp)
    yaw = -90.0 * (1 - _ease(_ramp(t, T['arm'] - 0.25, T['arm'] + 0.1)))
    arm = _ease(_ramp(t, T['arm'], T['arm'] + 0.45)) * (1 - _ease(_ramp(t, T['off'], T['off'] + 0.35)))
    sq = _bump(t, word_at(6, 'right') - 0.1, word_at(6, 'right') + 0.5, 0.12, 0.3)
    if arm > 0.01:
        rest = (-120.0, 330.0, 40.0)
        tgt = tuple(r + (a - r) * arm for r, a in zip(rest, ARM_ROUND))
        tgt = (tgt[0] + 14 * sq, tgt[1] + 10 * sq, tgt[2])
        V.arm_to(j, 'L', tgt, 'out', 'palm')
    th = _ease(_ramp(t, T['off'] + 0.1, T['off'] + 0.45))
    if th > 0.01:
        for s in 'LR':
            r = (-120.0 if s == 'L' else 120.0, 330.0, 40.0)
            V.arm_to(j, s, tuple(a + (b - a) * th for a, b in zip(r, THUMBS[s])), 'down', 'point')
    j['lean'] = j.get('lean', 0) + 6.0 * _bump(t, word_at(7, 'responsible') - 0.2, L[7]['end'] + 0.3, 0.25, 0.3)
    j['_arm'], j['_sq'] = arm, sq
    if arm >= 0.85:
        j['hand'] = dict(j.get('hand', {}), L='none')   # his hand is drawn over the driver's shoulder (_arm_over)
    x = GAS_VX
    k = _ramp(t, T['off'], T['off'] + 0.45)        # a side step out to his right, clear of the driver, for the thumbs
    if k > 0:
        step = STEP_OUT / V.M_PER_UNIT               # (person units)
        e = _ease(k)
        x = GAS_VX + STEP_OUT * e
        dl = -step * e + step * _ease(_ramp(k, 0.5, 1.0))          # the left foot planted, then follows
        dr = -step * e + step * _ease(_ramp(k, 0.0, 0.5))          # the right foot steps out first
        for side, d, lift in (('L', dl, math.sin(math.pi * _ramp(k, 0.5, 1.0))),
                              ('R', dr, math.sin(math.pi * _ramp(k, 0.0, 0.5)))):
            fx, fy, fz = j['foot' + side]
            j['foot' + side] = (fx + d, fy - 34 * lift, fz)
    return x, yaw, _head(j, t)


SHAKE = 4.5                                       # fist shakes a second (note 35)


def gas_man(t):
    """The driver: glaring up and left at the board, shaking his free fist at it, 50% angrier while he does (anger 6,
    Sam's note 35); the fist comes down as Vance's arm goes round him, and he stands rigid, the pump in his other
    hand; his eyes slide to Vance on "right" and stay."""
    j = _head(V.standing(AC.MAN), t, seed=5)
    V.arm_to(j, 'L', (-250, 330, 60), 'down', 'fist')
    up = _ease(_ramp(t, T['cut4'] + 0.15, T['cut4'] + 0.45)) * (1 - _ease(_ramp(t, T['enter'] + 0.3, T['enter'] + 0.7)))   # down as Vance comes in
    if up > 0.01:
        w = 2 * math.pi * SHAKE * t
        rest = (170.0, 330.0, 40.0)
        fist = (200.0 + 22 * math.sin(w), -190.0 + 30 * math.sin(w + 1.2), 90.0)   # raised up beside his head
        mid = (300.0, 120.0, 170.0)                  # the lift swings out and forward, clear of the shoulder
        k1, k2 = min(1.0, up * 2), max(0.0, up * 2 - 1)
        p1 = tuple(r + (m - r) * k1 for r, m in zip(rest, mid))
        V.arm_to(j, 'R', tuple(a + (f - a) * k2 for a, f in zip(p1, fist)), 'out', 'fist')
    side = _ease(_ramp(t, word_at(6, 'right') - 0.05, word_at(6, 'right') + 0.25))
    glare = _ease(_ramp(t, T['cut4'], T['cut4'] + 0.2)) * (1 - side)   # looking up at the board
    j['lean'] = j.get('lean', 0) - 5.0 * glare                         # leaning back a little to glare up at it
    fury = 1 if up > 0.5 else 0                    # note 37: the brows jump between the two faces, no morph
    return j, dict(head_yaw=-12, anger=4 + 2 * fury,
                   frown=0.06 * fury,                     # note 36: the face's frown is capped at anger 4, so the
                   lid4=0.02 - 0.035 * (4 + 2 * fury + 5),   # extra on top; the eyes kept open (the cast
                   # shuts them as anger rises) so you can see where they look
                   head_dx=-26 * up, head_dy=-6 * up, neck_lean=True,   # note 39: back to neutral as the fist comes down;   # note 38: the head up-left, the neck
                   # drawn once by the kit, leaning to follow it (no cut-out pieces)
                   gaze_dy=-1.0 * glare - 0.2 * side, look=-0.9 * glare + 0.8 * side)


NOZZLE = (40, 40, 44)
HOSE = (24, 24, 26)


def _nozzle(pen, hand):
    """The pump's nozzle in the driver's hand (brief 23): its black hose sagging from the pump's holster, the grip
    under his fist, the spout pointing down and forward."""
    hx, hy = hand
    fx, fy = ST.gas_points()['hose_from']
    pts = [(fx + (hx - fx) * k, fy + (hy - fy) * k + 260 * math.sin(math.pi * k)) for k in np.linspace(0, 1, 18)]
    pen.line(pts, ST.INK, 15)
    pen.line(pts, HOSE, 10)
    pen.poly([(hx - 22, hy - 16), (hx + 30, hy - 10), (hx + 34, hy + 8), (hx - 18, hy + 22)], NOZZLE, 2.4)
    pen.poly([(hx + 26, hy - 4), (hx + 74, hy + 22), (hx + 70, hy + 32), (hx + 24, hy + 10)], (150, 150, 156), 2.4)


def _top(alpha, x, y_from):
    """The first drawn pixel going down column x from y_from (the top of the driver's shoulder there)."""
    col = alpha[int(y_from):, int(x)]
    hit = np.nonzero(col > 128)[0]
    return int(y_from) + (int(hit[0]) if len(hit) else 0)


def _arm_over(im, man, j, mx, mneck, sm, s, vx, vneck, vlay):
    """His arm round the driver's shoulders (notes 34, 36: never through his chest): one sleeve lying ALONG THE TOP
    of both his shoulders, half against the sky, from Vance's own shoulder behind him, behind the driver's neck, over
    his far shoulder, the hand cupping its front; the driver's neck and head laid back over it, so it passes behind
    them. Measured from the driver's drawing every frame, so it follows him."""
    if j.get('_arm', 0.0) < 0.85:
        return
    al = np.asarray(man)[..., 3]
    neck_w = 34 * sm
    xs_far = np.linspace(mx - 175 * sm, mx - neck_w * 1.4, 6)      # over the far shoulder, to the neck
    xs_near = np.linspace(mx + neck_w * 1.4, min(vx - 120 * s, mx + 170 * sm), 5)
    w = 19 * s                                                       # the sleeve's half width
    lift = w * 0.45                                                  # its middle a little above his outline
    far = [(x, _top(al, x, mneck - 20 * sm) - lift) for x in xs_far]
    near = [(x, _top(al, x, mneck - 20 * sm) - lift) for x in xs_near]
    sq = j.get('_sq', 0.0)
    hx, hy = far[0][0] + 4 * sq, far[0][1] + w * 1.2 + 4 * sq        # the hand over the front of his far shoulder
    path = [(hx, hy)] + far + near + [(vx - 140 * s, vneck + 62 * s)]   # ... back to Vance's shoulder
    ink, fill = ST.layer(), ST.layer()
    ST.Pen(ink).line(path, ST.INK, 2 * w + 5)
    pf = ST.Pen(fill)
    pf.line(path, AC.NAVY, 2 * w)
    pf.ell(hx, hy + 6 * s, 26 * s, 26 * s, AC.V_SKIN, 2.4)
    ink = np.asarray(ST.shrink(ink)).copy()
    own = (np.asarray(vlay)[..., 3] > 128) & (np.asarray(man)[..., 3] < 128)   # over his own jacket: one body (rule
    ink[..., 3] = np.where(own, 0, ink[..., 3])                                  # 81, note 37), no line at the join
    im.alpha_composite(Image.fromarray(ink, 'RGBA'))
    im.alpha_composite(ST.shrink(fill))
    m = np.asarray(man).copy()                                       # his neck and head back over the sleeve
    yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
    keep = (yy < mneck + 30 * sm) & (np.abs(xx - mx) < neck_w * 1.25)
    keep |= yy < mneck - 2 * sm                                      # (everything above the neck's base: the head)
    keep &= np.abs(xx - mx) < 110 * sm
    m[..., 3] = np.where(keep, m[..., 3], 0)
    im.alpha_composite(Image.fromarray(m, 'RGBA'))


def vance_d(t):
    """His distance from the lens: a touch behind the driver, then forward with the side step."""
    return GAS_VD - STEP_FWD * _ease(_ramp(t, T['off'], T['off'] + 0.45))


def gas(t):
    im = ST.gas_back()
    mx, feet, ppm = ST.place_gas(MAN_X)
    sm = CP.nts(AC.MAN) * ppm / 928
    mneck = feet - 928 * sm
    jm, mk = gas_man(t)
    j = None
    vlay = None
    if t >= T['enter']:
        x, yaw, j = gas_vance(t)
        vx, vfeet, vppm = ST.place_gas(x, vance_d(t))
        vlay = Image.new('RGBA', im.size, (0, 0, 0, 0))
        CP.person(vlay, AC.VANCE, vx, vfeet + 10, vppm * 1.01, yaw, j, **face('vance', t, vance_mood(t)))
        if not vance_front(t):
            im.alpha_composite(vlay)
    wx, wy, _ = jm['wrL']
    lay = ST.layer()
    _nozzle(ST.Pen(lay), (mx + wx * sm, mneck + wy * sm + 12 * sm))
    im.alpha_composite(ST.shrink(lay))
    man = Image.new('RGBA', im.size, (0, 0, 0, 0))
    CP.person(man, AC.MAN, mx, feet, ppm, 0, jm, **dict(face('man', t, None), **mk))
    im.alpha_composite(man)
    if j is not None:
        vs = CP.nts(AC.VANCE) * vppm * 1.01 / 928
        _arm_over(im, man, j, mx, mneck, sm, vs, vx, vfeet + 10 - 928 * vs, vlay)
    if vlay is not None and vance_front(t):
        im.alpha_composite(vlay)
    im.alpha_composite(ST.gas_front())
    return im


# ---------------------------------------------------------------------------------------------- picture, captions, sound
DRAW = {'study': study, 'cliff': cliff, 'close': close, 'gas': gas}


def picture(t):
    """The frame WITHOUT captions (they go on last, so wording notes never re-render a picture)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    B.SS = 1
    return DRAW[shot_of(t)](t)


def vance_front(t):
    """Vance is in front of the driver once he has stepped forward and out for "This guy." (the step's second half)."""
    return False                                  # note 37: he stays behind the driver; the step only goes sideways


def draw_order(t):
    if cut_of(t) == 'gas' and t >= T['enter']:
        return ['background'] + (['man', 'vance'] if vance_front(t) else ['vance', 'man'])
    return ['background'] + SHOT_CAST[cut_of(t)]


def caption_at(t):
    for i, ln in enumerate(LINES):
        nxt = LINES[i + 1]['start'] - 0.05 if i + 1 < len(LINES) else 1e9
        if ln['start'] - 0.05 <= t < min(ln['end'] + CLEAR, nxt):
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


def soundtrack(stems=False):
    """Voices only until Sam's takes and the sounds he OK'd (question 9: the crackle, the explosion, the splashes)
    are filed: silent until then."""
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)
    for ln in LINES:
        if ln['_voice'] is not None:
            s = int(ln['start'] * SR)
            seg = ln['_voice'][:max(0, n - s)]
            voice[s:s + len(seg)] += seg
    mix = voice + rest
    end = int(BLACK_AT * SR)
    if np.abs(voice).max() > 1e-6:
        mix, g = MA.master(mix, end)
        voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


# ---------------------------------------------------------------------------------------------- checks, audit
def checks():
    """Plan checks: raises on the first batch of faults; prints the subtitles to proofread."""
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches']]
    faults = E.check_mouths(sorted(x for w in WHO for x in TRACK[w]), windows)
    if any(ln['_voice'] is not None for ln in LINES):
        mix, voice, rest = soundtrack(stems=True)
        faults += filmkit.voice_balance(voice, rest, SR, windows)
        faults += filmkit.hiss_check(mix, SR, BLACK_AT, voice=voice + rest)
    for t in np.arange(T['swivel'], T['cut2'], 1 / FPS):           # the sitting kit's own checks, every frame seated
        j, _, _ = study_j(float(t))
        faults += [f'{t:.2f} s: {f}' for f in sitting.check_frame(j, float(t), 'Vance in the study')]
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


def cam_for(t):
    """Every shot is a flat painting through its own camera (ad_vanced_notice_sets): the audit counts all as seen."""
    return None


def scene(t):
    """Everyone solid, where they stand in their shot's own metres (the audit's contact test)."""
    import audit
    s = shot_of(t)
    out = []
    if s == 'gas':
        out.append(audit.Thing('man', audit.simple('man', MAN_X, ST.D_MEN, HEIGHTS['man'])))
        if t >= T['enter']:
            out.append(audit.Thing('vance', audit.simple('vance', gas_vance(t)[0], vance_d(t), HEIGHTS['vance'])))
    elif s == 'cliff':
        x, y, _ = cliff_at(t)
        out.append(audit.Thing('vance', audit.simple('vance', x, y, HEIGHTS['vance'])))
    else:
        out.append(audit.Thing('vance', audit.simple('vance', 0.0, 0.0, HEIGHTS['vance'], sitting=s == 'study')))
    return out


def mouths_seen(t):
    s = shot_of(t)
    hh = {'study': 120.0, 'cliff': 90.0, 'close': 420.0, 'gas': 110.0}[s]
    out = [('vance', face('vance', t, vance_mood(t))['mouth'], 0.0, hh)]
    if s == 'gas':
        out.append(('man', face('man', t, None)['mouth'], 0.0, hh))
    return out


def audits():
    """Each person alone over every frame they are on screen (in pieces, popping, stretching, frozen)."""
    def alone(who):
        def draw(t):
            lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
            s = shot_of(t)
            if s == 'gas':
                if who == 'man':
                    jm, mk = gas_man(t)
                    mx, feet, ppm = ST.place_gas(MAN_X)
                    CP.person(lay, AC.MAN, mx, feet, ppm, 0, jm, **dict(face('man', t, None), **mk))
                elif t >= T['enter']:
                    x, yaw, j = gas_vance(t)
                    vx, vfeet, vppm = ST.place_gas(x, vance_d(t))
                    CP.person(lay, AC.VANCE, vx, vfeet + 10, vppm * 1.01, yaw, j, **face('vance', t, vance_mood(t)))
            elif s == 'study':
                j, yaw, hy = study_j(t)
                v = ST.STUDY_VANCE
                V.person(lay, AC.B.Cam(1.0, 540, 960), v['x'], v['neck_y'], v['s'],
                         dict(AC.VANCE, **face('vance', t, vance_mood(t))), t, yaw, j, head_yaw=hy)
            elif s == 'cliff':
                x, y, j = cliff_at(t)
                sx, sy, ppm = ST.place_cliff(x, y)
                CP.person(lay, AC.VANCE, sx, sy, ppm, 0, j, **face('vance', t, vance_mood(t)))
            else:
                CP.person(lay, AC.VANCE, 430, 1920 + 1500, 1500, 0, _head(V.standing(AC.VANCE), t),
                          **face('vance', t, vance_mood(t)))
            return lay
        return draw
    actors = {}
    for who in WHO:
        for shot, a, b in SHOTS:
            if who in SHOT_CAST[shot]:
                ts = [i / FPS for i in range(math.ceil(a * FPS), int(b * FPS))]
                if ts:
                    actors[f'{who} [{shot} {a:.1f}]'] = (ts, alone(who))
    filmkit.EYES.clear()
    return filmkit.silhouette_audit(actors, fps=FPS, still_ok=(),
                                    allow=[(k, t0, t1, why) for n, t0, t1, why in ALLOWED_POPS for k in actors
                                           if k.startswith(n + ' [')])


def LINE_SUBJECTS():
    def one(who):
        def d(im):
            V.person(im, AC.B.Cam(1.0, 540, 960), 540, 400, 1.0, dict(CAST[who], full=True, pose='custom'), 0.0, 0.0)
        return d
    return [(who, one(who)) for who in WHO]


# ---------------------------------------------------------------------------------------------- sheets, main
KEYS = [   # the check sheet: one per beat (label, time); the first carries the Hook Text (Sam, 3 Nov)
    ('1 back to us, the swivel starts (0)', lambda: T['swivel'] + 0.05),
    ('1 swivelling round, big grin (0)', lambda: T['swivel'] + SWIVEL * 0.6),
    ('1 Hook Text; hands folded', lambda: T['fold'] + 0.4),
    ('1 nod on "America" (1)', lambda: word_at(1, 'America') + 0.15),
    ('2 walking at us, mid-stride (2)', lambda: T['cut2'] + 0.3),
    ('2 brows on "haven\'t gone well" (2)', lambda: word_at(2, "haven't") + 0.2),
    ('2 tilt on "concerns" (3)', lambda: word_at(3, 'concerns') + 0.25),
    ('2 stops on "need", open hand (4)', lambda: word_at(4, 'need') + 0.35),
    ('2 the missile', lambda: T['hit'] - 0.2),
    ('2 the hit: flame-light', lambda: T['hit'] + 0.25),
    ('2 pieces fly, the ship breaks', lambda: T['hit'] + 1.2),
    ('2 the fireball climbs', lambda: T['hit'] + 3.0),
    ('3 close-up, the fire behind (5)', lambda: L[5]['start'] + 0.3),
    ('3 small smile on "fault" (5)', lambda: word_at(5, 'fault') + 0.25),
    ('4 the driver glares at the board', lambda: T['cut4'] + 0.5),
    ('4 Vance walks in from the right', lambda: T['enter'] + 0.7),
    ('4 arm round, "Aggravating" (6)', lambda: L[6]['start'] + 0.3),
    ('4 squeeze; his eyes slide (6)', lambda: word_at(6, 'right') + 0.3),
    ('4 leans in, "responsible?" (7)', lambda: word_at(7, 'responsible') + 0.25),
    ('4 both thumbs: "This guy." (8)', lambda: L[8]['start'] + 0.25),
]


def keys(out):
    import hook_text as H
    import tempfile
    tw, th, cols = 260, 462, 4
    rows = math.ceil(len(KEYS) / cols)
    sheet = Image.new('RGB', (cols * (tw + 10) + 10, rows * (th + 52) + 10), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 13)
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, 'hook.png')
        H.card(1080, 1920, HOOK[0], HOOK[1]['y'], png)
        card = Image.open(png).convert('RGBA')
    for i, (label, at) in enumerate(KEYS):
        t = at()
        x, y = 10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 52)
        im = frame_image(t).convert('RGBA')
        if 0.5 <= t < HOOK[1]['until']:            # the check sheet shows the Hook Text frame (Sam, 3 Nov)
            im.alpha_composite(card)
        sheet.paste(im.convert('RGB').resize((tw, th), Image.LANCZOS), (x, y + 42))
        d.multiline_text((x, y), f'{label}\n{t:.1f} s', font=f, fill=(30, 30, 30))
    sheet.save(out, quality=86)


def main():
    a = sys.argv[1:]
    if a[0] == 'shots':
        for s in SHOTS:
            print(f'{s[0]:8s} {s[1]:6.2f} {s[2]:6.2f}')
        for ln in LINES:
            print(ln['n'], round(ln['start'], 2), round(ln['end'], 2), 'take' if ln['_voice'] is not None else 'est')
        print({k: round(v, 2) for k, v in T.items()}, 'DUR', round(DUR, 2))
    elif a[0] == 'stills':
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'keys':
        keys(a[1])
    elif a[0] == 'check':
        checks()
        f = audits()
        import audit
        f += [x[len('AUDIT: '):] for x in audit.check(sys.modules[__name__])]
        print('\n'.join(['AUDIT: ' + x for x in f]) or 'audit: clean')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=cut_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', 1), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)


F.guard(B)
import limbs                     # noqa: E402
limbs.install(B)


def _point_hand(prev):
    """Power Crime Action's pointing finger (Sam, 8 Nov, note 39: ours read as something rude): short and slim, one
    round-ended finger the way the forearm points, its tip's join painted over so it reads as one finger, not a
    tube with a cap; drawn first so the circle hand covers its root."""
    def hand(p, el, wr, shape, skin, extra=None, t=0.0):
        if shape != 'point':
            return prev(p, el, wr, shape, skin, extra, t)
        dx, dy = wr[0] - el[0], wr[1] - el[1]
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        cx, cy = wr[0] + ux * 12, wr[1] + uy * 12
        tip = (cx + ux * 50, cy + uy * 50)
        w = 8.5
        p.poly([(cx - uy * w, cy + ux * w), (tip[0] - uy * w, tip[1] + ux * w), (tip[0] + uy * w, tip[1] - ux * w),
                (cx + uy * w, cy - ux * w)], skin, OUT, 2.2)
        p.ell(tip[0], tip[1], w, w, skin, OUT, 2.2)
        p.poly([(tip[0] - ux * 6 - uy * (w - 1.5), tip[1] - uy * 6 + ux * (w - 1.5)),
                (tip[0] - ux * 6 + uy * (w - 1.5), tip[1] - uy * 6 - ux * (w - 1.5)),
                (cx + uy * (w - 1.5), cy - ux * (w - 1.5)), (cx - uy * (w - 1.5), cy + ux * (w - 1.5))], skin, None)
        return prev(p, el, wr, 'fist', skin, extra, t)
    hand.point_finger = True
    return hand


B.gesture_hand = _point_hand(B.gesture_hand)

if __name__ == '__main__':
    main()
