#!/usr/bin/env python3
"""BLESSED (Sam, 11 Nov): Russell Brand, sentenced, repeats his 'feeling blessed' line at arrival, the oath, the
sentence and in prison, until the early release scheme frees him. From satire_template.py, drawn the Vance way
(views.person on flat paintings, one per camera). Guide: guides/satire.md.

MAP (rule 61: keep it in step; a note is answered by reading only these lines)
  the cast: blessed_cast.py; the sets: blessed_sets.py (each has its own MAP). Here: STORY (LINES, the timeline T,
  SHOTS) 60 | checks' lists 130 | people on the sets (put, put_seated, press) 175 | faces and moods 215 | each shot's
  drawing 245 | picture, captions, sound 380 | checks 430 | sheets, main 470.
  The moves stage (next) replaces the held poses in the shot functions with the acting list's moves.

    python3 source/blessed.py stills OUT_DIR T [T ...]
    python3 source/blessed.py check
    python3 source/blessed.py final OUT.mp4 [--small] [--span T0 T1]
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
import figure as F               # noqa: E402  blinks, breaths
import mouths                    # noqa: E402  lip sync
import subtitles as SUB          # noqa: E402  short, quick, readable subtitles timed from the recordings (rule 62)
import mossad_audio as MA        # noqa: E402  recordings cleaned and levelled
import filmkit                   # noqa: E402  the general checks
import film_engine as E          # noqa: E402  render with the picture cache, subtitle list, mouth check
import blessed_cast as BC        # noqa: E402  Brand, the judge, the officer, the newsreader
import blessed_sets as ST        # noqa: E402  the eight places
import blessed_jury as JY        # noqa: E402  the twelve jurors (Sam's note 10)
import blessed_checks as CK      # noqa: E402  the checks it was never set up for (chat 3, rule 59)
import press_secretary as PS     # noqa: E402,F401  (its seated reporters are no longer drawn: Sam's note 4)
import views as V                # noqa: E402
import moves                     # noqa: E402
from satire_style import install_circle_hands   # noqa: E402
from ed import INK, curve        # noqa: E402

mouths.install(B)
install_circle_hands(B)
BC.MC.CAST.clear()
BC.MC.CAST.update(BC.CAST)
FPS, SR = 12, MA.SR

# =============================================== STORY =============================================================
NAME = 'blessed'
HAS = {'people', 'rooms', 'voices', 'props', 'effects'}   # effects: his tears, the TV's light (chat 3)
TITLE = ()                                        # no title (CLAUDE.md)
TITLE_AT = dict(cap=116, top=310)
INMATE = dict(skin=(196, 150, 120), hw=66, hh=96, head_dy=10, hair='bald', hair_c=(40, 32, 28), outfit='jumper',
              jacket=BC.TRACK, sleeve=BC.TRACK, trousers=BC.TRACK, shoe=(240, 240, 240), shoulders=156, full=True,
              pose='custom', height=1.78)
CAST = dict(BC.CAST,
            inmate1=dict(INMATE, who='inmate1', name='Inmate 1', seed=301),
            inmate2=dict(INMATE, who='inmate2', name='Inmate 2', skin=(120, 82, 60), hair='bald', hair_c=(30, 24, 20),
                         jacket=(110, 116, 124), sleeve=(110, 116, 124), shoulders=170, height=1.84, seed=302),
            inmate3=dict(INMATE, who='inmate3', name='Inmate 3', skin=(232, 190, 164), hair='bald',
                         hair_c=(170, 120, 70), jacket=(150, 152, 156), sleeve=(150, 152, 156), height=1.72, seed=303),
            **JY.JURORS)
LINES = [   # the script word for word (brief rows 5, 6, 7, 11, 13-14, 15); Sam's takes time every line
    dict(n=1, audio='blessed-1', who='brand', text="Yeah, I'm feeling blessed, mate, super blessed."),
    dict(n=2, audio='blessed-2', who='brand', text="I swear by Almighty God that the blessed evidence I shall give "
         "shall be the truth, the whole truth, and nothing but the blessed truth."),
    dict(n=3, audio='blessed-3', who='brand', text="Well that doesn't feel very blessed."),
    dict(n=4, audio='blessed-4', who='brand', text="Yeah, love. I'm just not feeling very... blessed right now."),   # Sam's take (note 19)
    dict(n=5, audio='blessed-bbc', who='newsreader', text="Our breaking news. The government has announced a new "
         "round of the early release scheme, as way of dealing with the prison capacity crisis. The Prime Minister "
         "has said that it is necessary to stop overcrowding."),
    dict(n=6, audio='blessed-5', who='brand', text="Blessed! I'm feeling so blessed right now, everybody!"),
]
L = {ln['n']: ln for ln in LINES}
for ln in LINES:                                  # cut each take only in silence: before the first word, after the last
    x = MA.line(ln['audio'])
    st = MA.pauses(x, 0.12)
    a, b = max(0, int((st[0][0] - 0.12) * SR)), min(len(x), int((st[-1][1] + 0.25) * SR))
    x = x[a:b].copy()
    fade = int(0.02 * SR)
    x[:fade] *= np.linspace(0, 1, fade)
    x[-fade:] *= np.linspace(1, 0, fade)
    ln['_voice'], ln['_dur'] = x, len(x) / SR
    ln['_stretches'] = MA.pauses(x, 0.18)
FADE_FROM = 1                                     # brief 14: the reporter drifts away after her first two phrases


def _at(n, start):
    L[n]['start'], L[n]['end'] = start, start + L[n]['_dur']
    return L[n]['end']


# The timeline: each beat follows the one before, so a take that runs long pushes the rest on.
T = {}
T['s1'] = 0.0
T['s2'] = _at(1, 0.5) + 0.7                       # arrival (line 1), then the oath
T['s3'] = _at(2, T['s2'] + 0.5) + 0.6             # the oath, then the sentencing (the dock)
# Sam's note 10 (12 Nov): in the middle of the oath, 180 to the jury staring at him (cut in the pause after
# "Almighty God", back in the pause after "shall be the truth"; his voice carries over)
T['jury'] = L[2]['start'] + L[2]['_stretches'][0][1] + 0.12
T['oath2'] = L[2]['start'] + L[2]['_stretches'][2][1] + 0.12
T['bang'] = T['s3']                               # the gavel is only HEARD, on the dock shot's first frame
T['s4'] = T['s3']                                 # (Sam, 12 Nov: no gavel shot)
T['hollow'] = T['s4'] + 0.3                       # the stillness cracks just before line 3
T['van'] = _at(3, T['s4'] + 0.9) + 0.8
T['cell'] = T['van'] + 2.8                        # montage: van, escorted in, weeping on the cot
T['cot'] = T['cell'] + 3.2
T['phone'] = T['cot'] + 2.8
T['tvroom'] = _at(4, T['phone'] + 0.5) + 0.7
T['tv'] = T['tvroom'] + 2.6                       # his eyes drift up to the screen
_at(5, T['tv'] + 0.4)
T['push'] = L[5]['start'] + L[5]['_stretches'][min(FADE_FROM, len(L[5]['_stretches']) - 1)][1] + 0.2
T['amazed'] = T['push'] + 1.2                     # the face change on the slow push in (brief 14)
T['overjoyed'] = T['push'] + 3.2
T['gates'] = T['overjoyed'] + 1.6               # her voice has faded out by the cut
DUR = _at(6, T['gates'] + 0.8) + 1.0
T['gates2'] = L[6]['start'] + L[6]['_stretches'][0][1] + 0.12   # the cut just after "Blessed!": closer, at his mark
# Brief 14: she drifts away. Her take is faded to silence by T['gates'] (soundtrack), so the film's record of line 5
# ends where she is last heard, in the pause after "crisis." (12 Nov, chat 3: the script and mouth checks read the
# whole take as heard and found her mouth shut at 50.8 s, off screen and inaudible). The full script stays in 'script'.
_k = L[5]['_stretches'][FADE_FROM + 1][1] + 0.25
_n = int(_k * SR)
L[5]['script'] = L[5]['text']
L[5]['text'] = ("Our breaking news. The government has announced a new round of the early release scheme, as way of "
                "dealing with the prison capacity crisis.")
L[5]['_voice'] = L[5]['_voice'][:_n].copy()
L[5]['_voice'][-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
L[5]['_dur'] = _n / SR
L[5]['end'] = L[5]['start'] + L[5]['_dur']
L[5]['_stretches'] = MA.pauses(L[5]['_voice'], 0.18)


def _voice_env(who):
    """The speaker's loudness per drawing over the whole film (for headlife)."""
    env = np.zeros(int((DUR + 1) * FPS))
    n = SR // FPS
    for ln in LINES:
        if ln['who'] == who:
            v = ln['_voice']
            e = [np.sqrt(np.mean(v[i * n:(i + 1) * n] ** 2)) for i in range(len(v) // n)]
            i0 = int(round(ln['start'] * FPS))
            env[i0:i0 + len(e)] = e[:len(env) - i0]
    return env


import headlife                  # noqa: E402  (rule 74: every talking head tilts and nods on the voice)
HEAD_LIFE = {'brand': headlife.HeadLife(_voice_env('brand'), 0.0, seed=5),
             'newsreader': headlife.HeadLife(_voice_env('newsreader'), 0.0, seed=9)}
SHOTS = [('arrive', T['s1'], T['s2']), ('oath', T['s2'], T['jury']), ('jury', T['jury'], T['oath2']),
         ('oath2', T['oath2'], T['s3']),
         ('dock', T['s4'], T['van']), ('van', T['van'], T['cell']), ('escort', T['cell'], T['cot']),
         ('cot', T['cot'], T['phone']), ('phone', T['phone'], T['tvroom']), ('tvroom', T['tvroom'], T['tv']),
         ('tv', T['tv'], T['push']), ('push', T['push'], T['gates']), ('gates', T['gates'], T['gates2']),
         ('gates2', T['gates2'], DUR)]
VIEW = {'arrive': 'court_out', 'oath': 'court_box', 'jury': 'court_jury', 'oath2': 'court_box', 'dock': 'court_dock', 'van': 'van',
        'escort': 'cell', 'cot': 'cot_top', 'phone': 'phone', 'tvroom': 'tvroom', 'tv': 'tv', 'push': 'tvroom',
        'gates': 'gates', 'gates2': 'gates2'}
SHOT_CAST = {'arrive': ['brand'], 'oath': ['brand', 'judge'], 'oath2': ['brand', 'judge'],
             # Sam's note 10: "the jury, staring at him". The front row's two end jurors (1, 6) sit outside the frame
             # all shot (the scene check, chat 3); the ten in frame are the jury he sees
             'jury': [j for j in JY.JURORS if j not in ('juror1', 'juror6')],
             'dock': ['brand'],
             'van': ['brand'], 'escort': ['brand', 'officer'], 'cot': ['brand'], 'phone': ['brand'],
             'tvroom': ['brand'], 'tv': ['newsreader'], 'push': ['brand'], 'gates': ['brand'],
             'gates2': ['brand']}
BENCHMARK = ST.BENCHMARK                          # rule 3: the sets' own (blessed_sets.py)
SET_BOXES, SET_MEANT = ST.SET_BOXES, ST.SET_MEANT  # rule 83
# Rule 1: the plan. A flat film: each place is its painting's Level camera in metres (blessed_sets); the marks are
# STAGE there. Listed for plan.py with each camera.
_PX = {v: 20.0 * i for i, v in enumerate(ST.BACK)}   # each painting is its own place: laid side by side, never
#                                                   overlapping (pre-flight read one shared box as rooms overlapping)
PLAN = dict(CEIL=3.0, ROOMS={v: (_PX[v] - 6.0, 0.0, _PX[v] + 6.0, 18.0) for v in ST.BACK}, OPENINGS={}, THINGS={},
            PEOPLE={}, CAMS={v: dict(pos=(_PX[v], 1.6, 1.0), look=(_PX[v], 1.6, 6.0)) for v in ST.BACK}, GROUPS={})

# What the shared checks need (preflight.py runs them all; guides/satire.md, 'Getting it right first time'):
HOOK = ('Russell Brand this week', {'y': 420})     # brief 17 (Claude's pick); over the court's upper windows, clear
#                                                   of the sign and his hair (rule 75, measured 11 Nov)
SUBS_IN_PICTURE = True
PIECE_FIX = {2: {2: 2.9, 3: 4.24, 4: 5.48, 5: 6.4, 6: 7.35}, 4: {1: 3.2, 2: 4.47},
             5: {2: 3.0, 3: 4.25, 4: 6.35, 5: 7.3, 6: 8.25}}   # subtitles pinned to the takes' spoken stretches (Sam, 12 Nov);
#   chat 3: the fast stretches' pieces come up up to 0.3 s early (rule 62's tolerance) so each is readable (rule 62)
KEEP_CLEAR = [('the court sign', lambda t: (330, 640, 1030, 730) if t < T['s2'] else None),
              ('his face and hair', lambda t: (620, 950, 925, 1215) if t < T['s2'] else None)]
PROP_SIZES = []
OUTFIT = {}
HEIGHTS = {w: c['height'] for w, c in CAST.items()}
FAMOUS = ['Russell Brand']                        # the name as drawn (chat 4: 'brand' never matched)
CUT_RESTS_OK = []
# Rule 41's meant exceptions, each looked at full size (chat 4, 12 Nov): (who, side, kind, t0, t1, why)
HANDS_OK = [('Journalist*', '*', 'no hand', T['s1'], T['s2'], 'seen from behind, the hand is under the phone or TV '
             'camera they hold up (drawn over it): the kit shows where the hand is'),
            ('Journalist*', '*', 'no hand', T['gates'], DUR, 'the same pack at the gates, from behind, hands under '
             'their raised phones and cameras'),
            ('Russell Brand', '*', 'prop hidden', T['s1'], T['s2'], "his hand on his heart: the 'prop' is only the "
             "sleeve's ink edge (_sleeve_edge), under the hand by design; nothing he holds is hidden"),
            ('Russell Brand', '*', 'seam', T['s1'], T['s2'], 'his long curly hair hangs over both shoulders: the '
             'lines across the arm are the hair\'s edge, the jacket runs straight into the sleeve beneath'),
            ('Russell Brand', '*', 'no hand', T['van'], T['cell'], 'hands clasped between his knees: one fist over '
             'the other, as clasped hands are'),
            ('Prison officer', '*', 'over *', T['cell'], T['cot'], "the officer's grip on Brand's arm, walking him "
             'in (brief 9; touch_faults checks the hand sits on the arm)')]
LOOKS_AT = {}
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
ALLOWED_CONTACTS, ALLOWED_POPS, SET_EXCLUDE = [], [], []
TOUCHES, FREE_MOVES, RESTS = [], [], []
SOUND_SOURCES, JOKE_PROPS, ORDER_SWAPS = {}, [], []
LINE_OK = [('brand', 'line weight', 540, 289),                 # his moustache: a filled shape, not a line
           ('officer', 'no outline', 647, 932), ('officer', 'no outline', 648, 966),   # the key chain: a thin line itself
           ('officer', 'edge with no line', 614, 649), ('officer', 'edge with no line', 693, 497),   # the shirt's flat
           ('juror4', 'edge with no line', 660, 486), ('juror4', 'edge with no line', 600, 691),     # shadow side, the
           ('juror9', 'edge with no line', 632, 482), ('juror9', 'edge with no line', 599, 691),     # cardigans' (the kit's
           #                                                                                         allowed exception)
           ('juror7', 'no outline', 458, 99), ('juror11', 'no outline', 462, 99),   # a curl at the crown: a line itself
           ('juror7', 'edge with no line', 497, 195), ('juror7', 'edge with no line', 582, 196),   # light brows: colour
           ('juror8', 'edge with no line', 509, 195), ('juror8', 'edge with no line', 569, 195),   # strokes, not shapes
           ('juror9', 'edge with no line', 508, 197), ('juror9', 'edge with no line', 570, 197),   # (as Ad-Vanced
           ('juror11', 'edge with no line', 503, 200), ('juror11', 'edge with no line', 576, 200)]   # Notice's brows)
STILL_OK = ()                                     # nobody is meant to hold dead still

GUARDS = {'guard1': BC.OFFICER,                   # two different officers (pass 2: twins)
          'guard2': dict(BC.OFFICER, who='guard2', skin=(236, 196, 170), hair='bob', hair_c=(170, 120, 70), shoulders=150,
                         height=1.68, seed=97, lashes=True)}
TRACK = {w: [] for w in CAST}
for ln in LINES:
    TRACK[ln['who']] += [(a + ln['start'], b + ln['start'], sh) for a, b, sh in mouths.track(ln['text'], ln['_stretches'])]
BLINKS = {w: F.blinks(7 + 3 * i, 0.5, DUR, talking=True) for i, w in enumerate(CAST)}


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def _ramp(t, a, b):
    return min(1.0, max(0.0, (t - a) / max(1e-6, b - a)))


def _ease(u):
    return u * u * (3 - 2 * u)


# ---------------------------------------------------------------------------------------------- people on the sets
def _s(sp, ppm):
    return ST.s_for(ppm, sp['height'])


def put(img, cam, sp, mark, t, yaw=0.0, j=None, head_yaw=None):
    """Someone standing on a mark (screen x, ground y, pixels per metre)."""
    x, y, ppm = mark
    s = _s(sp, ppm)
    if not CK.keep(sp):                           # the body audit draws one person alone (blessed_checks)
        img = CK.scratch()
    if sp.get('look_') == 'trial' and j is not None and abs(yaw) > 10:
        j = dict(j, body_props=list(j.get('body_props', [])) + [_scarf_turned])
    return V.person(img, cam, x, y - 928 * s, s, sp, t, yaw, j, head_yaw=head_yaw)


def _scarf_turned(pen, view, sp):
    """His long white scarf when he is turned (hunt 1, 12 Nov: it vanished in the three-quarter walk): the front
    torso draws it only straight on; here both ends hang down the chest's front, the near one wider."""
    if view == 'front':
        return
    for x0, w in ((6, 26), (-22, 18)) if view != 'side' else ((14, 24),):
        pts = [(x0 - w / 2, -4), (x0 + w / 2, -4), (x0 + w / 2 + 4, 210), (x0 + w / 2 + 2, 420), (x0 - w / 2, 428),
               (x0 - w / 2 - 2, 210)]
        pen.poly(B.curve(pts, 3) if hasattr(B, 'curve') else pts, BC.SCARF, INK, 2.2)


def put_seated(img, cam, sp, mark, t, yaw=0.0, j=None):
    """Someone seated, feet on the floor at the mark (the seated pose's own drop lowers him onto the seat)."""
    x, y, ppm = mark
    s = _s(sp, ppm)
    if not CK.keep(sp):
        img = CK.scratch()
    j = j or moves.seated(sp)
    j['seated'] = False                           # the set paints the seat
    return V.person(img, cam, x, y - 928 * s, s, dict(sp, full=True, pose='custom'), t, yaw, j)


PRESS_HAIR = [(58, 44, 36), (30, 24, 22), (150, 110, 70), (170, 166, 162), (110, 70, 46), (196, 196, 192)]
PRESS_JKT = [B.NAVY, B.CHARCOAL, (110, 40, 50), (70, 90, 120), (90, 96, 80), (150, 120, 90), (60, 60, 70)]
PRESS_STYLE = ['short', 'bob', 'pony', 'crop', 'bald', 'curly', 'long', 'side']
PRESS_KIT = ['tv', 'phone', 'tv', 'none', 'boom', 'pad', 'phone', 'boom']   # a TV camera in clear view at both
PRESS_YAW = {'short': 145, 'crop': -145, 'side': 140}   # three turned three-quarter (Sam's note 4), the rest backs on
PRESS_FACE = [dict(face_wide=0.05, jaw_wide=0.06), dict(face_wide=-0.04, chin_long=0.02), dict(), dict(jaw_wide=0.08),
              dict(face_wide=0.06), dict(face_wide=-0.02), dict(face_wide=-0.05, jaw_wide=-0.05), dict(jaw_wide=0.03)]


def press_sp(i, seed):
    """Journalist i: their own build, clothes, haircut and turning head (blessed_cast.press_person)."""
    k = (i + 2 * seed) % 8
    style, hc = PRESS_STYLE[k], PRESS_HAIR[(i + seed) % 6]
    if style == 'bald':
        hc = (128, 120, 114)                         # a grey horseshoe, cropped short
    skin = [B.PALE, B.PINK, B.OLIVE, B.BROWN][i % 4]
    jk = PRESS_JKT[(i * 3 + seed) % 7]
    head = BC.press_person('press%d' % k, style, skin, hc, 500 + k, PRESS_FACE[k])
    small = style in ('bob', 'pony', 'long')
    full = dict(head, name='Journalist %d' % (i + 1), skin=skin, hw=62 if small else 66, hh=96, head_dy=10, hair='bald',
                hair_c=hc, outfit='suit', jacket=jk, sleeve=jk, trousers=B.dk(jk, 0.6) if i % 2 else (40, 40, 46),
                shirt=(246, 246, 246), tie=None, shoe=(24, 20, 18), shoulders=138 if small else 150 + 6 * (i % 3),
                full=True, pose='custom', height=(1.64 if small else 1.76) + 0.05 * ((i * 7 + seed) % 3), seed=600 + i,
                kit=PRESS_KIT[(i + seed) % 8], yaw=PRESS_YAW.get(style, 180))
    import turnhead
    turnhead.PEOPLE[head['who']].sheet = lambda d=full: d    # the turnaround sheet draws them (chat 4: had none)
    return full


def press_pose(sp, t):
    """Their arms: the camera operator's near hand up on the camera's grip, a boom held up in front (hands hidden by
    the body), a phone held up filming, a notebook at the chest; the rest hang at rest."""
    j = V.standing(sp)
    kit, sw = sp['kit'], sp['shoulders']
    if kit == 'tv':
        V.arm_to(j, 'R', (sw - 30, -40.0, 60.0), 'down', 'fist')
    elif kit == 'boom':                               # both hands up on the pole, one over the other (critique 1)
        V.arm_to(j, 'R', (70.0, -250.0, 40.0), 'out', 'fist')
        V.arm_to(j, 'L', (40.0, -110.0, 50.0), 'in', 'fist')
    elif kit == 'phone':                              # held up above the head, filming over the others
        V.arm_to(j, 'R', (95.0, -250.0, 40.0), 'out', 'fist')
    elif kit == 'pad':
        V.arm_to(j, 'L', (-30.0, 160.0, 150.0), 'down', 'palm')
        V.arm_to(j, 'R', (20.0, 170.0, 160.0), 'out', 'fist')
    sway = 4 * math.sin(t * 1.3 + sp['seed'])            # a little life: weight shifting
    j['lean'] = 1.5 * math.sin(t * 0.9 + sp['seed'] % 5)
    j['bob'] = 0.0 * sway
    return j


def press(img, cam, L, spots, t, seed=0, reach=480, at=(0.5, 4.0)):
    """The press pack from behind (Sam's note 4): standing people with shoulders, collars, arms and turning heads, far
    to near on the pavement at (x, d) metres through the set's Level camera; the kit on top of the nearest arms."""
    people = []
    for i, (x, d) in enumerate(spots):
        X, Y = L.p(x, d)
        people.append((d, i, (X, Y, L.ppm(d))))
    for d, i, mark in sorted(people, key=lambda q: -q[0]):
        sp = press_sp(i, seed)
        x, d = spots[i]                               # everyone faces him, body and head (Sam, 11 Nov): from
        sp['yaw'] = 180 - math.degrees(math.atan2(at[0] - x, at[1] - d))   # behind, turned towards his mark
        kit = sp['kit']
        s = _s(sp, mark[2])
        neck = (mark[0], mark[1] - 928 * s)
        r = dict(x=neck[0], y=neck[1], s=s * 1.0, seed=sp['seed'])
        j = press_pose(sp, t)
        if kit == 'boom':                             # the pole from his hands (drawn over it) up and forward
            back = -1 if abs(sp['yaw']) > 90 else 1
            r['hands'] = [(back * j['wr' + k][0], j['wr' + k][1]) for k in 'LR']
            r['reach'] = reach
            _boom(img, cam, r, t)
        pts = put(img, cam, sp, mark, t, sp['yaw'], j)
        if kit == 'tv':                               # on the raised hand's side (his right: our left from behind)
            _tv_camera(img, cam, r, 1 if pts['wrR'][0] > 0 else -1)
        elif kit == 'phone':
            _phone_up(img, cam, r, pts, 1 if pts['wrR'][0] > 0 else -1)


def _phone_up(img, cam, r, pts, sg):
    """A phone held up filming, seen from behind: its back over the hand, the screen's glow round its edge."""
    p = B.Pen(img, B.Local(cam, r['x'], r['y'], r['s']))
    wx, wy = pts['wrR']
    x, y = wx + sg * 4, wy - 70                                       # just above his raised fist, clear of the hair
    p.poly([(x - 34, y - 60), (x + 34, y - 60), (x + 34, y + 60), (x - 34, y + 60)], (30, 30, 34), INK, 2.4)
    p.ell(x - 18, y - 42, 8, 8, (70, 70, 76), INK, 1.4)               # the lens


def _tv_camera(img, cam, r, sg=1):
    """A TV camera on the right shoulder, seen from behind: the body beside the head, the battery on its back,
    the carry handle, the lens hood just showing past it (O3: the press must read as press)."""
    p = B.Pen(img, B.Local(cam, r['x'], r['y'], r['s'], sg))
    p.poly([(56, -150), (250, -160), (256, -30), (60, -24)], (44, 46, 52), INK, 2.6)
    p.poly([(70, -132), (150, -136), (150, -44), (72, -40)], (24, 24, 28), INK, 1.8)         # the battery
    p.poly([(110, -186), (220, -190), (224, -160), (114, -156)], (60, 62, 68), INK, 2.0)     # the handle
    p.poly([(180, -176), (196, -176), (196, -150), (180, -150)], (60, 62, 68), None)
    p.poly([(40, -110), (70, -112), (72, -70), (42, -68)], (20, 20, 24), INK, 1.8)             # the eyepiece, our side
    p.ell(176, -60, 8, 8, (200, 40, 40), None)                                               # the tally light
    #                                                 (no lens hood: from behind the lens points away, at him)


def _boom(img, cam, r, t):
    """A boom microphone held up over the scrum: the pole from his hands (in front of him, hidden) up and forward,
    the furry grey windshield at its tip."""
    p = B.Pen(img, B.Local(cam, r['x'], r['y'], r['s']))
    sw = 1.0 + 0.02 * math.sin(t * 1.7 + r['seed'] % 7)
    (ax, ay), (bx, by) = r.get('hands', [(30, 60), (-20, -100)])
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy) or 1.0
    base = (ax - dx / n * 40, ay - dy / n * 40)                     # a little past the lower hand
    reach = r.get('reach', 480)                                      # shorter at the court: under its sign
    tip = (bx + dx / n * reach * sw, by + dy / n * reach)
    p.line([base, tip], (70, 72, 78), 9)
    p.line([base, tip], INK, 1.2)
    p.ell(tip[0] - 10, tip[1] - 30, 46, 82, (150, 150, 146), INK, 2.4, rot=0.2)
    for k in range(10):
        a = 2 * math.pi * k / 10
        p.line([(tip[0] - 10 + 44 * math.cos(a), tip[1] - 30 + 80 * math.sin(a)),
                (tip[0] - 10 + 54 * math.cos(a), tip[1] - 30 + 92 * math.sin(a))], (150, 150, 146), 3.0)


# ---------------------------------------------------------------------------------------------- faces and moods
def face(who, t, mood, **extra):
    shape = mouths.at(TRACK[who], t)
    d = dict(mood=mood, mouth='rest' if shape == 'rest' else 'v:' + shape, blink=F.blinking(t, BLINKS[who]))
    d.update(extra)
    return d


def brand_mood(t):
    """The acting list: sincere showman (arrival, shades lowered on 'mate'); stiff and earnest (the oath); hollow
    (the sentence); numb, weeping, dejected (prison); dejected to amazed to overjoyed (the push); showman (gates)."""
    s = shot_of(t)
    if s == 'arrive':
        return 'showman', ('lowered' if t >= word_at(1, 'mate') else 'on')
    if s in ('oath', 'oath2'):
        return 'oath', None
    if s == 'dock':
        return ('hollow' if t >= T['hollow'] else 'neutral'), None
    if s in ('van', 'escort'):
        return 'numb', None
    if s == 'cot':
        return 'weeping', None
    if s == 'phone':
        return 'phone', None                       # eyes open, looking down (Sam, 12 Nov)
    if s in ('tvroom', 'tv'):
        return 'deadeyed', None                    # note 22: no tears, dead-eyed
    if s == 'push':
        return ('overjoyed' if t >= T['overjoyed'] else 'amazed' if t >= T['amazed'] else 'deadeyed'), None
    return 'overjoyed', 'on'


def brand_sp(t, look):
    mood, shades = brand_mood(t)
    return dict(BC.LOOKS[look], head_life=HEAD_LIFE['brand'], **face('brand', t, mood, shades=shades))


# ---------------------------------------------------------------------------------------------- moves
# The moves plan (notes/blessed.md, "The moves plan"): each shot's pose from the acting list. Bodies and feelings
# ease; eyes and jokes snap. Every arm is solved from where its hand goes (views.arm_to); a hand moving between two
# places blends its CONTACT point and its elbow's pole, so nothing pops.
ANCHORS = {(2, 'Almighty'): (0, 0.42), (2, 'blessed evidence'): (1, 0.2), (2, 'blessed truth'): (4, 0.62),
           (6, 'everybody'): (1, 0.72)}       # where the take pauses between phrases, pin a word to its stretch


def word_at(n, words):
    """When line n reaches `words` (from ad_vanced_notice: the share of the text before them, spread over the take's
    spoken stretches, or pinned by ANCHORS)."""
    ln = L[n]
    st = ln['_stretches']
    if (n, words) in ANCHORS and len(st) > ANCHORS[(n, words)][0]:
        i, f = ANCHORS[(n, words)]
        return ln['start'] + st[i][0] + f * (st[i][1] - st[i][0])
    tot = sum(b - a for a, b in st) or 1.0
    k = ln['text'].index(words) / len(ln['text']) * tot
    for a, b in st:
        if k <= b - a:
            return ln['start'] + a + k
        k -= b - a
    return ln['start'] + st[-1][1]


def _bump(t, a, b, rise=0.2, fall=0.25):
    return _ease(_ramp(t, a, a + rise)) * (1 - _ease(_ramp(t, b - fall, b)))


def _keys(t, keys):
    """A number eased between timed keys [(t, value)], held before the first and after the last."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, a), (t1, b) in zip(keys, keys[1:]):
        if t < t1:
            return a + (b - a) * _ease(_ramp(t, t0, t1))
    return keys[-1][1]


def _contact(j, side, off):
    el, wr = j['el' + side], j['wr' + side]
    return V._add(wr, V._mul(V._unit(V._sub(wr, el)), off))


def _rest_spec(sp, side, j=None):
    """The hand where the standing pose (or `j`) puts it, as an arm spec: (contact point, pole, hand shape)."""
    j = j or V.standing(sp)
    shape = j.get('hand', {}).get(side, 'fist')
    sg = -1 if side == 'L' else 1
    e = V._unit(V._sub(j['el' + side], j['sh' + side]))
    return _contact(j, side, F.HAND.get(shape, 14)), (sg * e[0], e[1], e[2]), shape


def _arm(j, side, target, pole, off, shape):
    """views.arm_to with the hand's reach beyond the wrist given (`off`), so a hand changing shape never pops."""
    sg = -1 if side == 'L' else 1
    px, py, pz = V.POLES[pole] if isinstance(pole, str) else pole
    el, end = V.ik3(j['sh' + side], target, F.UPPER * 0.98, F.FORE * 0.98 + off, (sg * px, py, pz))
    j['el' + side], j['wr' + side] = el, V._add(el, V._mul(V._unit(V._sub(end, el)), F.FORE * 0.98))
    j.setdefault('hand', {})[side] = shape
    return j


def arm_keys(j, sp, side, t, keys):
    """The hand on `side` through timed keys [(t, spec)]: spec = (target, pole, shape) in the torso frame, or None
    for the hand where `j` already has it (rest). Between two keys the contact point and the pole blend, eased."""
    rest = _rest_spec(sp, side, j)

    def spec(s):
        if s is None:
            return rest
        tgt, pole, shape = s
        return tgt, V.POLES[pole] if isinstance(pole, str) else pole, shape
    if t <= keys[0][0]:
        a = b = spec(keys[0][1])
        u = 0.0
    elif t >= keys[-1][0]:
        a = b = spec(keys[-1][1])
        u = 0.0
    else:
        (t0, sa), (t1, sb) = next(((k0, k1) for k0, k1 in zip(keys, keys[1:]) if t < k1[0]))
        a, b = spec(sa), spec(sb)
        u = _ease(_ramp(t, t0, t1))
    if a is rest and b is rest:
        return j
    tgt = moves.lerp(a[0], b[0], u)
    pole = moves.lerp(a[1], b[1], u)
    off = F.HAND.get(a[2], 14) + (F.HAND.get(b[2], 14) - F.HAND.get(a[2], 14)) * u
    return _arm(j, side, tgt, pole, off, b[2] if u >= 0.5 else a[2])


def unlean(p, lean):
    """A point where it should end up AFTER the body leans `lean` degrees, in the torso frame before the lean."""
    if not lean:
        return p
    c, s = math.cos(math.radians(lean)), math.sin(math.radians(lean))
    x, y, z = p
    dy = y - V.HIP_Y
    return x, V.HIP_Y + c * dy - s * z, s * dy + c * z


HANDS = {}                                      # (who, side) -> the hand circle's middle on the frame (world px)


def _log_hands(who, pts, mark, s, flip, bob=0.0):
    x, y = mark[0], mark[1] - 928 * s + bob * s
    for sd in 'LR':
        el, wr = pts['el' + sd], pts['wr' + sd]
        c = V._add(wr, V._mul(V._unit(V._sub(wr, el)), 12.0))
        HANDS[(who, sd)] = (x + flip * s * c[0], y + s * c[1])


def _world_to_person(wx, wy, mark, s, flip, bob=0.0):
    return flip * (wx - mark[0]) / s, (wy - (mark[1] - 928 * s)) / s - bob


# the prayer beads (arrival): a loop of wooden beads and a small cross hanging from his right fist
def _beads(sp):
    def draw(p, j2):
        el, wr = j2['elR'], j2['wrR']
        u = V._unit(V._sub(wr, el))
        cx, cy = wr[0] + 12 * u[0], wr[1] + 12 * u[1] + 52
        pts = [(cx + 20 * math.sin(2 * math.pi * k / 22), cy - 46 * math.cos(2 * math.pi * k / 22)) for k in range(22)]
        p.line(pts + pts[:1], (60, 40, 26), 1.6)
        for q in pts:
            p.ell(q[0], q[1], 5.2, 5.2, (122, 78, 44), INK, 1.1)
        p.poly([(cx - 3, cy + 48), (cx + 3, cy + 48), (cx + 3, cy + 80), (cx - 3, cy + 80)], (122, 78, 44), INK, 1.1)
        p.poly([(cx - 11, cy + 56), (cx + 11, cy + 56), (cx + 11, cy + 62), (cx - 11, cy + 62)], (122, 78, 44), INK, 1.1)
    return draw


def _sleeve_edge(sp):
    """An ink-edged, slightly darker forearm over the jacket, so the arm on the heart does not merge with it (Sam, hunt 2)."""
    base = sp.get('sleeve', (120, 120, 124))
    dk = tuple(int(c * 0.78) for c in base)

    def draw(p, j2):
        el, wr = j2['elL'], j2['wrL']
        p.line([el, wr], INK, 30)
        p.line([el, wr], dk, 23)
    return draw


def _box_prop(j, box, col, mark=None):
    """A flat box held in the hand (the Bible), drawn from its 8 corners in 3D, leaning with the body."""
    def draw(p, j2):
        pts = [V.project(V.leaned(q, j.get('lean', 0.0)), j2['yaw'])[0] for q in box]
        p.poly(V._hull(pts), col, INK, 2.4)
        if mark:
            mark(p, j2)
    return draw


# How Brand moves (notes/blessed.md "How Brand moves", from 2008-2021 reviews): a rock-star swagger (chest out, a
# loose sway, a long easy stride), big open-handed gestures, a dip at the knees on the punchline, chin up to preen.
# The showman is in the arrival, the oath (held in) and the gates; prison has none of it (the contrast is the joke).
moves.GAITS['swagger'] = dict(moves.GAITS['walk'], sps=1.8, step=0.5, swing=0.42, bend=0.25, lean=-3)


def _sway(t, sps=1.8):
    """The swagger's roll of the head and shoulders, towards each planted foot."""
    return 3.5 * math.sin(math.pi * sps * t)


def _dip(j, amt, splay=0.2):
    """Down at the knees by `amt` person units, feet kept on the floor, knees opening a little."""
    if amt <= 0:
        return j
    j['bob'] = j.get('bob', 0.0) + amt
    for sd, sg in (('L', -1), ('R', 1)):
        x, y, z = j['foot' + sd]
        j['foot' + sd] = (x, y - amt, z)
        j['knee_pole' + sd] = (sg * splay, 0.0, 1.0)
    return j


# --- arrive: he walks into the scrum, stops, snaps to face the cameras; heart, shades on "mate", arms wide on
#     "super", back to the heart with a little bow on the last "blessed"; at rest by 4.4 s (rule 72)
ARRIVE_FROM, ARRIVE_TO, ARRIVE_STOP = (1.2, 4.9), (0.45, 3.9), 1.35


def arrive(sp, t):
    """(mark, yaw, joints) for Brand arriving: swaggers in, leans in to the press on "mate", dips with his arms
    flung open on "super", springs up chin high, then hand to heart and a small bow on the last "blessed"."""
    u = min(1.0, max(0.0, (t - T['s1']) / ARRIVE_STOP))
    x = ARRIVE_FROM[0] + (ARRIVE_TO[0] - ARRIVE_FROM[0]) * u
    d = ARRIVE_FROM[1] + (ARRIVE_TO[1] - ARRIVE_FROM[1]) * u
    mark = ST._mark(ST.OUT, x, d)
    walking = t < ARRIVE_STOP
    g = moves.gait(sp, t + 0.37, 'swagger')
    settle = _ease(_ramp(t, ARRIVE_STOP - 0.15, ARRIVE_STOP + 0.15))
    j = moves.mix_poses(g, V.standing(sp), settle)
    yaw = 0.0                                     # note 26: front-on even walking in (South Park)
    if not walking:
        j['bob'] = 0.0
        j['lean'] = 0.0
    j['head_roll'] = _sway(t + 0.37) * (1 - settle)
    feel, mate, sup, last = (word_at(1, 'feeling'), word_at(1, 'mate'), word_at(1, 'super'),
                             word_at(1, 'blessed.'))
    sw = sp.get('shoulders', 150)
    heart = ((-30.0, 135.0, 78.0), 'in', 'palm')
    shades = ((-88.0, -204.0, 70.0), 'in', 'palm')       # at the frame's side: the nose stays clear
    wide = lambda sg: ((sg * (sw + 300), 40.0, 150.0), 'out', 'palm')   # flung open at shoulder height
    arm_keys(j, sp, 'L', t, [(feel - 0.35, None), (feel, heart), (mate - 0.35, heart), (mate - 0.05, shades),
                             (mate + 0.1, shades), (sup + 0.05, wide(-1)), (last - 0.1, wide(-1)), (last + 0.2, heart),
                             (L[1]['end'] + 0.2, heart), (4.4, None)])
    arm_keys(j, sp, 'R', t, [(mate + 0.1, None), (sup + 0.05, ((sw + 300, 40.0, 150.0), 'out', 'fist')),
                             (last - 0.1, ((sw + 300, 40.0, 150.0), 'out', 'fist')), (last + 0.3, None)])
    if mate - 0.3 < t < mate + 0.25:
        j['on_face'] = {'L'}
    lean_in = _bump(t, mate - 0.35, sup + 0.05, 0.25, 0.2)            # in close to the scrum on "mate"
    dip = _bump(t, sup - 0.12, last + 0.02, 0.14, 0.12)               # down at the knees on "super", springs up
    chin = _bump(t, sup - 0.05, last + 0.05, 0.12, 0.15)              # chin up, preening, as the arms open
    bow = _bump(t, last - 0.1, last + 0.7, 0.25, 0.35)
    _dip(j, 60 * dip)
    j['lean'] = j.get('lean', 0.0) + 7 * lean_in + 6 * bow
    j['nod'] = 1.4 * bow - 2.5 * chin
    j['head_roll'] = j.get('head_roll', 0.0) + 5 * lean_in
    import grips
    grips.held(j, 'R', sp, _beads(sp))
    if (feel < t < mate - 0.2) or (last + 0.25 < t < L[1]['end'] + 0.2):   # hand on the heart: the sleeve gets an ink edge
        grips.held(j, 'L', sp, _sleeve_edge(sp))
    return mark, yaw, j


OATH_BIBLE = ((-6.0, 120.0, 128.0), 'down', 'fist')     # far hand (L) at the shirt opening
OATH_RAISE = (40.0, -140.0, 100.0, (1.0, 0.8, 0.3))                  # near hand (R) up beside the head, palm out
OATH_BOOK = [(x, y, z) for x in (-70.0, 52.0) for y in (14.0, 190.0) for z in (122.0, 150.0)]   # bigger (chat 2)


# --- oath: side-on in the box (facing left, so his R is the near side): the near hand raised palm out, the Bible
#     in the far hand held up on the white shirt; eyes up on "Almighty God"
def oath(sp, t):
    j = V.standing(sp)
    sw = sp.get('shoulders', 150)
    a = T['s2']
    up0, up1 = a + 0.15, a + 0.65
    dn0 = T['s3'] + 0.05                          # held to the cut (rule 72; chat 4: dropped 0.4 s before it)
    dn1 = dn0 + 0.4
    bible = OATH_BIBLE
    raised = ((sw + OATH_RAISE[0], OATH_RAISE[1], OATH_RAISE[2]), OATH_RAISE[3], 'palm')
    arm_keys(j, sp, 'L', t, [(up0, None), (up1, bible), (dn0, bible), (dn1, None)])
    mid = ((sw + 70.0, 60.0, 90.0), OATH_RAISE[3], 'palm')      # out and up on the way: the elbow never folds tight
    arm_keys(j, sp, 'R', t, [(up0, None), ((up0 + up1) / 2, mid), (up1, raised), (dn0, raised), (dn1, mid),
                             (dn1 + 0.15, None)])
    for w in ('blessed evidence', 'blessed truth'):
        k = word_at(2, w)
        b = _bump(t, k - 0.05, k + 0.55, 0.15, 0.3)
        j['nod'] = j.get('nod', 0.0) - 1.1 * b        # the showman held in: bolt upright, the chin lifts on each "blessed"
    if up0 + 0.25 < t < dn1 - 0.1:                # chat 6: from 4.83 s only its top edge cleared the box front (22%)
        import grips
        c = _contact(j, 'L', F.HAND.get('fist', 14))  # the book moves WITH the hand (chat 4: it was eased on its own
        lift = V._sub(c, bible[0])                  # path and floated 1.1 hand-widths off it on the way up)
        box = [V._add(q, lift) for q in OATH_BOOK]

        def marks(p, j2):
            pr = lambda q: V.project(V.leaned(V._add(q, lift), j.get('lean', 0.0)), j2['yaw'])[0]
            x0, x1 = OATH_BOOK[0][0], OATH_BOOK[-1][0]
            y0, y1 = OATH_BOOK[0][1], OATH_BOOK[-1][1]
            zf = OATH_BOOK[-1][2]
            # the pale page edge along the far (spine-less) side, seen past the cover
            e = [pr((x0, y0 + 6, zf - 4)), pr((x0, y1 - 6, zf - 4)), pr((x0, y1 - 6, OATH_BOOK[0][2] + 4)),
                 pr((x0, y0 + 6, OATH_BOOK[0][2] + 4))]
            p.poly(e, (250, 244, 222), INK, 2.0)
            c = pr(((x0 + x1) / 2, (y0 + y1) / 2, zf + 1))
            g = (214, 176, 70)
            p.poly([(c[0] - 4, c[1] - 26), (c[0] + 4, c[1] - 26), (c[0] + 4, c[1] + 26), (c[0] - 4, c[1] + 26)], g, None)
            p.poly([(c[0] - 15, c[1] - 12), (c[0] + 15, c[1] - 12), (c[0] + 15, c[1] - 4), (c[0] - 15, c[1] - 4)], g, None)
        grips.held(j, 'L', sp, _box_prop(j, box, (40, 30, 34), marks))
    return j


def oath_gaze(t):
    return -0.6 if word_at(2, 'Almighty') - 0.05 <= t < word_at(2, 'that the') else 0.0


# --- dock: hands clasped low; the gavel is heard on its first frame (a small flinch); still, then hollow, the shoulders drop
def dock(sp, t):
    j = V.standing(sp)
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, (sg * 10, 420.0, 60.0), 'back')
    u = _ease(_ramp(t, T['hollow'], T['hollow'] + 1.0))
    j['bob'], j['head_dy'], j['lean'] = 12 * u, 10 * u, 4 * u
    j['bob'] += 5 * _bump(t, T['bang'], T['bang'] + 0.3, 0.03, 0.25)      # a small start at the bang
    return j


# --- van: bent over, forearms on the thighs, hands clasped between the knees, head down; the van sways him
VAN_HANDS = lambda sg: (sg * 10, 400.0, 360.0)      # both fists together, between the knees


def van(sp, t):
    j = moves.seated(sp)
    lean = 28 + 1.5 * math.sin(2 * math.pi * (t - T['van']) / 2.4)
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, unlean(VAN_HANDS(sg), lean), 'down')
    j['lean'], j['head_dy'], j['nod'] = lean, 10.0, 2.2
    j['hide_legs'], j['knee_round'] = {'L', 'R'}, True                    # note 16: the legs and seat are drawn here, before the jumper
    j['pre'] = [lambda p, j2, view: _seat(p, j, sp, j2['yaw'])]
    return j


VAN_YAW = 35          # Sam, 12 Nov: he keeps this three-quarter pose ("I even said I like the pose")


def _seat(p, j, sp, yaw):
    """Note 16: seen turned and seated, the body had no hips: the jumper stopped at the waist and the thighs began in
    mid-air. His seat and hips as one rounded shape from the waist down to the thigh tops, drawn before the legs and
    the jumper, so both lie over its edges and nothing floats. The legs are drawn first (far one first), then the seat
    over their cut roots (chat 1 drew the seat first and the thighs' notched ends lay on top of it; it also used the
    pose's 35 degrees, not the drawn view's 45, so the seat sat off the body)."""
    far = sorted('LR', key=lambda sd: V.project(j['hip' + sd], yaw)[1])
    pts = []
    for sd in 'LR':
        hx, hy, hz = j['hip' + sd]
        for a in range(0, 360, 30):                   # round each hip joint, pushed back for the seat
            c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
            pts.append(V.project((hx + 48 * c, hy + 40 * s_, hz - 10 + 30 * c), yaw)[0])   # a normal seat, not
        #                                             pushed back (Sam, 12 Nov: the bigger one read as a huge bottom)
        knee = V.knee_of(j, sd)
        if knee:
            u = 0.35                                    # a third of the way down the thigh, so the join is hidden
            pts.append(V.project(tuple(a + (b - a) * u for a, b in zip(j['hip' + sd], knee)), yaw)[0])
    hull, col = curve(V._hull(pts), 3), sp.get('trousers', (40, 40, 46))
    p.poly(hull, col, INK, 2.4)                       # under the legs: its outline is the seat's edge
    cx, cy = sum(q[0] for q in hull) / len(hull), sum(q[1] for q in hull) / len(hull)
    for sd in far:
        V.leg(p, j, sd, yaw, sp)
    p.poly([(cx + (x - cx) * 0.9, cy + (y - cy) * 0.9) for x, y in hull], col, None)   # over the thighs' roots,
    #                                                 no outline: the thighs grow out of the seat, no notched ends


# --- escort: the officer walks him in by the arm; he stops, turns, and looks round numbly
CELL = ST.Level(1.55, 803.0, 1000.0, cx=540)
ESC_FROM, ESC_TO = (1.0, 2.1), (0.15, 2.35)
ESC_GO = 0.0                                    # into the shot (he enters mid-stride)
ESC_STOP = math.hypot(ESC_TO[0] - ESC_FROM[0], ESC_TO[1] - ESC_FROM[1]) / moves.speed('stroll')
OFF_BEHIND = (0.45, -0.25)


def _cell_mark(x, d):
    X, Y = CELL.p(x, d, 0.0)
    return (X, Y, CELL.ppm(d))


def escort(sp, t, who='brand'):
    """(mark, yaw, joints, head_yaw) for Brand or the officer in the escort."""
    k = t - T['cell']
    u = min(1.0, max(0.0, k / ESC_STOP))
    x = ESC_FROM[0] + (ESC_TO[0] - ESC_FROM[0]) * u
    d = ESC_FROM[1] + (ESC_TO[1] - ESC_FROM[1]) * u
    if who == 'officer':
        x, d = x + OFF_BEHIND[0], d + OFF_BEHIND[1]
    g = moves.gait(sp, k + (0.31 if who == 'brand' else 0.62), 'stroll')
    j = moves.mix_poses(g, V.standing(sp), _ease(_ramp(k, ESC_STOP - 0.2, ESC_STOP + 0.15)))
    if k >= ESC_STOP:
        j['bob'] = 0.0
    yaw, head = -90.0, None
    if who == 'brand' and k >= ESC_STOP + 0.15:
        yaw = 0.0                                 # notes 17/26: front-on once he stops
        a = T['cell'] + ESC_STOP
        head = -90.0 if a + 0.3 <= t < a + 0.9 else None      # a look left, then up to the window, then down
        j['nod'] = _keys(t, [(a + 0.9, 0.0), (a + 1.25, -1.6), (a + 1.6, -1.6), (a + 2.0, 1.4)])
    return _cell_mark(x, d), yaw, j, head


def escort_gaze(t):
    a = T['cell'] + ESC_STOP
    return _keys(t, [(a + 0.9, 0.0), (a + 1.2, -0.6), (a + 1.6, -0.6), (a + 1.9, 0.5)])


GRIP_AT = [None]                                 # where the officer's hand should be on Brand's arm (touch check)


def officer_grip(sp, j, t, mark, brand_pts, brand_mark, brand_s):
    """His near hand ('L', facing left) on Brand's near upper arm until the stop, then back to his side."""
    k = t - T['cell']
    if k > ESC_STOP + 0.5:
        return j
    sh, el = brand_pts['shL'], brand_pts['elL']
    bx = brand_mark[0] - brand_s * (sh[0] + 0.45 * (el[0] - sh[0]))
    by = brand_mark[1] - 928 * brand_s + brand_s * (brand_pts.get('_bob', 0.0) + sh[1] + 0.45 * (el[1] - sh[1]))
    GRIP_AT[0] = (bx, by)
    s = _s(sp, mark[2])
    px, py = _world_to_person(bx, by, mark, s, -1, j.get('bob', 0.0))
    xd = -20.0                                         # a little nearer the lens than his chest
    tgt = (xd, py - V.ELEV * (-xd), px)                # side view: screen x is the body's z; depth is -x
    held = ((tgt, 'down', 'fist'))
    arm_keys(j, sp, 'L', t, [(T['cell'] + ESC_STOP + 0.1, held), (T['cell'] + ESC_STOP + 0.5, None)])
    return j


# --- cot: sat on the cot's edge, hands limp in his lap, weeping at us, a sob every 0.9 s (chat 4: lying curled on it
#     from this camera, head at the pillow, the rig drew his face upside down; rule 42, looked at full size)
COT_MARK, COT_YAW = (540, 1800, 740.0), 0.0       # note 18: cot_top, lying flat seen from above (drawn standing)


def cot_pose(sp, t):
    """Sam's note 18: lying flat on his back, seen from straight above (drawn front-on), arms limp at his sides,
    staring up at the ceiling (the lens); a sob every 1.4 s lifts his chest and shoulders a touch."""
    j = V.standing(sp)
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, (sg * 200, 520.0, 10.0), 'back')
    ph = ((t - T['cot']) % 1.4) / 1.4
    sob = math.sin(math.pi * min(1.0, ph / 0.3)) if ph < 0.3 else 0.0
    j['bob'] = -4.0 * sob
    j['head_dy'] = 2.0 - 2.0 * sob
    return j


# --- phone: head down, a slow shake on "blessed right now"
def phone_extra(t):
    a = word_at(4, 'blessed right')
    w = _ramp(t, a, a + 1.0)
    sh = math.sin(2 * math.pi * w) * (1 - w) * 1.4 if 0 < w < 1 else 0.0
    return dict(head_dx=6.0 * sh), 2.5 * sh


# --- TV room and the push: slouched; sits up on 'amazed', leans in on 'overjoyed'
def asleep_pose(sp, t):
    """Note 22: asleep in his chair in front of the TV: slumped, chin dropped, head lolled to one side, a slow
    breath lifting the shoulders."""
    j = moves.seated(sp)
    j['lean'] = -6.0
    j['head_roll'] = 16.0
    j['nod'] = 0.6
    j['head_dy'] = 10.0 + 3.0 * math.sin(t * 2 * math.pi / 3.6)
    return j


def pool_pose(sp, t):
    """Note 22: bent low over the pool table facing us, lining up a shot: bridge hand flat on the cloth, the cue
    hand by his chest drawing back and forward in small practice strokes."""
    j = V.standing(sp)
    j['hide_legs'] = ('L', 'R')                    # behind the table: the cloth hides them
    j['lean'] = 62.0
    j['nod'] = -0.6                                # chin up, eyes along the cue
    V.arm_to(j, 'L', (-120.0, 120.0, 360.0), 'out', 'palm')
    k = 26.0 * math.sin(t * 2 * math.pi / 1.4)       # the practice strokes
    V.arm_to(j, 'R', (70.0, 60.0, 150.0 - k), 'back', 'grip')
    return j


def pool_cue(img, cam, mark, sp, pts):
    """The cue from his cue hand through the bridge hand on the cloth, its tip at the cue ball."""
    x, y, ppm = mark
    s = _s(sp, ppm)
    sc = lambda q: (x + s * q[0], y - 928 * s + s * q[1])
    a, b = sc(pts['wrR']), sc(pts['wrL'])
    d = (b[0] - a[0], b[1] - a[1])
    tip = (b[0] + 0.25 * d[0], b[1] + 0.25 * d[1])
    p = B.Pen(img, cam)
    p.line([(a[0] - 0.5 * d[0], a[1] - 0.5 * d[1]), tip], (150, 104, 60), 5.0)
    p.line([(a[0] - 0.5 * d[0], a[1] - 0.5 * d[1]), tip], INK, 1.0)
    p.ell(tip[0] + 4, tip[1] + 8, 9, 6, (246, 246, 240), INK, 1.0)                       # the cue ball


def tv_pose(sp, t):
    j = moves.seated(sp)
    lean = _keys(t, [(T['amazed'], -6.0), (T['amazed'] + 0.6, 0.0), (T['overjoyed'], 0.0), (T['overjoyed'] + 0.6, 6.0)])
    j['lean'] = lean
    j['head_dy'] = _keys(t, [(T['amazed'], 6.0), (T['amazed'] + 0.6, 0.0)])
    j['nod'] = _keys(t, [(T['overjoyed'], 0.0), (T['overjoyed'] + 0.6, -1.0)])
    return j


# --- gates: swaggers out of the wicket door (wide), arms flung up and open, chin high, on "Blessed!"; then closer,
#     striding to his mark; on "everybody!" he dips with his arms swept open to the pack and springs back up


def _gates_cut():
    return L[6]['start'] + L[6]['_stretches'][0][1] + 0.12


GATE_V = lambda sw, sg: ((sg * (sw + 290), -110.0, 90.0), 'out', 'palm')     # up and out, palms open: the messiah
GATE_OPEN = lambda sw, sg: ((sg * (sw + 300), 40.0, 160.0), 'out', 'palm')   # swept open at shoulder height


def _arms_wide(j, sp, t, t_up, side_first=True):
    """Both arms flung up and open at t_up: out to the side on the way (figure-rig 3's waypoint), then up."""
    sw = sp.get('shoulders', 150)
    for sd, sg in (('L', -1), ('R', 1)):
        side = ((sg * (sw + 200), 120.0, 40.0), 'down', 'palm')
        arm_keys(j, sp, sd, t, [(t_up - 0.35, None), (t_up - 0.12, side), (t_up + 0.1, GATE_V(sw, sg))])
    return j


def gates_wide(sp, t):
    k = t - T['gates']
    dd = GATE_D_OUT[0] + (GATE_D_OUT[1] - GATE_D_OUT[0]) * min(1.0, k / 0.8)
    mark = ST._mark(ST.GATE, 0.65, dd)
    g = moves.gait(sp, k, 'swagger')
    settle = _ease(_ramp(k, 0.7, 0.95))
    j = moves.mix_poses(g, V.standing(sp), settle)
    if k > 0.95:
        j['bob'] = 0.0
    j['head_roll'] = _sway(k) * (1 - settle)
    up = word_at(6, 'Blessed!') + 0.1
    _arms_wide(j, sp, t, up)
    chin = _ease(_ramp(t, up - 0.1, up + 0.2))
    j['nod'] = -1.5 * chin
    j['lean'] = j.get('lean', 0.0) - 3 * chin
    return mark, 0.0, j


GATE_D_OUT = (ST.GATE_D + 0.2, ST.GATE_D - 0.52)
G2_FROM, G2_TO = 8.5, 7.6                          # out of the wicket into the pack


def gates_close(sp, t):
    a = _gates_cut()
    k = t - a
    walk = (G2_FROM - G2_TO) / moves.speed('swagger')
    u = min(1.0, max(0.0, k / walk))
    mark = ST._mark(ST.GATE, 0.6, G2_FROM + (G2_TO - G2_FROM) * u)
    g = moves.gait(sp, k + 0.25, 'swagger')
    settle = _ease(_ramp(k, walk - 0.15, walk + 0.15))
    j = moves.mix_poses(g, V.standing(sp), settle)
    if k > walk + 0.15:
        j['bob'] = 0.0
    sw = sp.get('shoulders', 150)
    ev = word_at(6, 'everybody')
    for sd, sg in (('L', -1), ('R', 1)):
        arm_keys(j, sp, sd, t, [(ev - 0.3, GATE_V(sw, sg)), (ev + 0.05, GATE_OPEN(sw, sg)),
                                (ev + 0.25, GATE_OPEN(sw, sg)), (ev + 0.55, GATE_V(sw, sg))])
    dip = _bump(t, ev - 0.25, ev + 0.5, 0.25, 0.22)               # down at the knees with the sweep, springs up
    _dip(j, 40 * dip)
    chin = 1 - _bump(t, ev - 0.3, ev + 0.5, 0.2, 0.25)
    j['nod'] = -1.5 * chin + 0.8 * dip                             # chin high, a dip of the head into the sweep
    j['lean'] = j.get('lean', 0.0) - 3 * chin + 5 * dip
    j['head_roll'] = _sway(k + 0.25) * (1 - settle) + 4 * _ease(_ramp(t, ev + 0.5, ev + 0.9))   # a preening tilt to hold
    return mark, 0.0, j


# ---------------------------------------------------------------------------------------------- the shots
TV_READER = (540, 1010)                           # the newsreader's face on the TV painting (screen px at zoom 1)
def _cam(view, t):
    """The camera on a view; the push is a slow zoom into his face on the tvroom painting (brief 14)."""
    if shot_of(t) == 'push':
        u = _ease(_ramp(t, T['push'], T['overjoyed'] + 0.6))
        x, y, ppm = ST.STAGE['tvroom']['brand']
        # note 23: onto his FACE, not his torso (the face sits 1.35 m over his seated mark, measured on the still)
        return B.Cam(1.0 + 2.0 * u, 540 + (x - 540) * u, 960 + (y - 0.95 * ppm - 250 - 960) * u)
    if shot_of(t) == 'tv':                        # note 23: a slow zoom in on the newsreader in the set
        u = _ease(_ramp(t, T['tv'], T['push']))
        return B.Cam(1.0 + 0.9 * u, 540 + (TV_READER[0] - 540) * u, 960 + (TV_READER[1] - 960) * u)
    if shot_of(t) == 'cot':                       # note 18: the camera sinks slowly toward him from above
        u = _ease(_ramp(t, T['cot'], T['phone']))
        return B.Cam(1.0 + 0.45 * u, 540, 960 + (560 - 960) * u)
    if shot_of(t) == 'jury':                      # a slow push in on the twelve faces
        u = _ease(_ramp(t, T['jury'], T['oath2']))
        return B.Cam(1.04 + 0.12 * u, 540, 1240 + 40 * u)   # the jurors above the caption (hunt 1)
    if shot_of(t) == 'phone':                     # note 20: 200 px right, so the second booth is in the room with him
        return B.Cam(1.0, 740, 960)
    if shot_of(t) == 'gates':                     # a slow push on the wicket door
        u = _ease(_ramp(t, T['gates'], T['gates2']))
        x, y = ST.GATE.p(0.65, ST.GATE_D, 1.2)
        return B.Cam(1.0 + 0.55 * u, 540 + (x - 540) * u * 0.6, 980 + 120 * u)   # opens on the towers (hunt 1), pushes to the gate
        #                                                                       (Sam, 11 Nov: he was a distant speck)
    return ST.view_cam(view)[1]


def draw_people(img, cam, shot, t):
    view = VIEW[shot]
    st = ST.STAGE.get(view, {})
    HANDS.clear()
    if shot == 'arrive':
        sp = brand_sp(t, 'trial')
        mark, yaw, j = arrive(sp, t)
        put(img, cam, sp, mark, t, yaw, j)
        press(img, cam, ST.OUT, st['press'], t, reach=230, at=(0.45, 3.9))
    elif shot == 'jury':
        JY.draw(img, cam, t, word_at(2, 'blessed evidence'), put_seated, face, ST)
    elif shot in ('oath', 'oath2'):
        x, y, ppm = st['judge']
        sj = dict(BC.JUDGE, **face('judge', t, 'neutral'))
        jj = moves.seated(sj)                       # chat 4: he held dead still 2.5 s; small weight shifts, no sway
        jj['lean'] = jj.get('lean', 0.0) + filmkit.shifts(t, seed=41, amount=1.6, hold=(0.9, 1.7))
        jj['head_roll'] = filmkit.shifts(t, seed=42, amount=2.5, hold=(1.0, 1.8))
        jj['nod'] = filmkit.shifts(t, seed=43, amount=0.5, hold=(1.1, 2.0))
        put_seated(img, cam, sj, (x, y, ppm), t, j=jj)
        ST.mid(view, img, cam, t)
        sp = dict(brand_sp(t, 'stand'), gaze_dy=oath_gaze(t))
        put(img, cam, sp, st['brand'], t, yaw=0, j=oath(sp, t))   # notes 13/26: front-on, South Park style
    elif shot == 'dock':
        for g in ('guard1', 'guard2'):
            put_seated(img, cam, dict(GUARDS[g], **face('officer', t, 'neutral')), st[g], t)
        ST.mid(view, img, cam, t)
        sp = brand_sp(t, 'dock')
        put(img, cam, sp, st['brand'], t, j=dock(sp, t))
    elif shot == 'van':
        sp = brand_sp(t, 'prison')
        put_seated(img, cam, dict(sp, gaze_dy=0.6), st['brand'], t, yaw=VAN_YAW, j=van(sp, t))   # note 16: Sam keeps the 3/4 pose; limbs fixed
    elif shot == 'escort':
        sp = dict(brand_sp(t, 'prison'), gaze_dy=escort_gaze(t))
        bm, by, bj, bh = escort(sp, t)
        so = dict(BC.OFFICER, **face('officer', t, 'neutral'))
        om, oy, oj, _ = escort(so, t, 'officer')
        bs = _s(sp, bm[2])
        bpts = put(img, cam, sp, bm, t, by, bj, head_yaw=bh)
        bpts['_bob'] = bj.get('bob', 0.0)
        _log_hands('brand', bpts, bm, bs, -1 if by < 0 else 1, bpts['_bob'])
        officer_grip(so, oj, t, om, bpts, bm, bs)
        opts = put(img, cam, so, om, t, oy, oj)
        _log_hands('officer', opts, om, _s(so, om[2]), -1, oj.get('bob', 0.0))
    elif shot == 'cot':
        sp = brand_sp(t, 'prison')
        put(img, cam, sp, ST.STAGE['cot_top']['brand'], t, 0.0, cot_pose(sp, t))   # note 18: flat on his back, from above
    elif shot == 'phone':
        sp = brand_sp(t, 'prison')
        dx, roll = phone_extra(t)
        sp = dict(sp, head_dy=sp.get('head_dy', 0) + 8, gaze_dy=0.55, **dx)   # eyes open, looking down at the phone
        j = handset_pose(sp)
        j['lean'], j['head_roll'] = 5.0, roll
        pts = put(img, cam, sp, st['brand'], t, yaw=0, j=j)   # notes 21/26: front-on
        phone_cord(img, cam, pts, st['brand'], sp)
        _log_hands('brand', pts, st['brand'], _s(sp, st['brand'][2]), -1)
    elif shot in ('tvroom', 'push'):
        # Sam's note 22: Brand alone on a plastic chair, watching; behind on the left a man asleep in his chair
        # facing the TV; behind on the right an inmate bent over the pool table, lining up a shot
        pts = put(img, cam, dict(CAST['inmate2'], **face('inmate2', t, 'neutral', gaze_dy=0.5)), st['inmate2'], t,
                  j=pool_pose(CAST['inmate2'], t))
        pool_cue(img, cam, st['inmate2'], CAST['inmate2'], pts)
        put_seated(img, cam, dict(CAST['inmate1'], **face('inmate1', t, 'neutral', blink=True, mouth='rest')),
                   st['inmate1'], t, j=asleep_pose(CAST['inmate1'], t))
        sp = brand_sp(t, 'prison')
        if shot == 'tvroom':                       # brief 12: his eyes drift up to the screen
            sp['gaze_dy'] = -0.7 * _ease(_ramp(t, T['tvroom'] + 0.8, T['tvroom'] + 1.8))
        else:
            sp['gaze_dy'] = -0.7
        put_seated(img, cam, sp, st['brand'], t, j=tv_pose(sp, t))
    elif shot == 'gates':
        sp = brand_sp(t, 'trial')
        mark, yaw, j = gates_wide(sp, t)
        put(img, cam, sp, mark, t, yaw, j)
        press(img, cam, ST.GATE, st['press'], t, at=(0.65, ST.GATE_D - 0.3))   # the same pack as the arrival (Sam's answer 6)
    elif shot == 'gates2':
        sp = brand_sp(t, 'trial')
        mark, yaw, j = gates_close(sp, t)
        put(img, cam, sp, mark, t, yaw, j)
        press(img, cam, ST.GATE, ST.STAGE['gates']['press'], t, at=(0.6, G2_TO))


DEFER = []                                        # drawn after the set's front layer (the held gavel over the block)


def handset_pose(sp, side='L'):
    """The landing phone's steel handset at his ear (moves.phone_at_ear's hold, his near hand: facing left he is
    drawn mirrored, so 'L' is the side nearer us); the cord is drawn by phone_cord."""
    j = V.standing(sp)
    sg = 1 if side == 'R' else -1
    hw = sp.get('hw', 70)
    V.arm_to(j, side, (sg * (hw + 22), -96.0, 12.0), (1.0, 0.35, 0.6), 'grip')
    top, bot = (-176.0, -40.0), (-60.0, 24.0)
    ay, az = bot[0] - top[0], bot[1] - top[1]
    n = math.hypot(ay, az)
    wy, wz = -az / n * 24, ay / n * 24
    box = [(sg * x, y + k * wy, z + k * wz) for x in (hw + 2, hw + 22) for y, z in (top, bot) for k in (-1, 1)]

    def draw(p, j2):
        pts = [V.project(V.leaned(q, j2.get('lean', 0.0)), j2['yaw'])[0] for q in box]
        p.poly(V._hull(pts), (176, 182, 188), INK, 2.4)              # brushed steel, chunkier than a mobile
    import grips
    return grips.held(j, side, sp, draw)


def phone_cord(img, cam, pts, mark, sp, side='L'):
    """The handset's armoured steel cord, from under his hand sagging back to the phone (blessed_sets.PHONE_CORD).
    Front-on (notes 21/26): screen x = mark x + s * x."""
    from ed import open_curve
    x0, y0, ppm = mark
    s = _s(sp, ppm)
    wx, wy = pts['wr' + side]
    a = (x0 + s * wx, y0 - 928 * s + s * (wy + 70))   # front-on (notes 21/26) he is drawn unmirrored: + s * x
    b = ST.PHONE_CORD
    cord = open_curve([a, ((a[0] + b[0]) / 2, max(a[1], b[1]) + 160), b], 8)
    p = B.Pen(img, cam)
    p.line(cord, (150, 156, 162), 7.0)
    p.line(cord, INK, 1.0)


def picture(t):
    """The frame WITHOUT captions (those go on last, so wording notes never re-render a picture)."""
    shot = shot_of(t)
    view, _ = ST.view_cam(VIEW[shot])
    cam = _cam(VIEW[shot], t)
    img = B.canvas((0, 0, 0))
    feed = ST.studio_feed(t, dict(BC.NEWSREADER, head_life=HEAD_LIFE['newsreader'], **face('newsreader', t, 'neutral'))) if view == 'tv' else None
    ST.back(view, img, cam, t, feed)
    if view not in ST.MID:                          # those put the mid layer between their people
        ST.mid(view, img, cam, t)
    DEFER.clear()
    draw_people(img, cam, shot, t)
    ST.front(view, img, cam, t)
    for f in DEFER:
        f()
    return img


def set_still(view):
    """blessed_sets.alone's tile: the view with the cast at their marks, at the middle of its first shot."""
    shot = next(s for s, v in VIEW.items() if v == view) if view in VIEW.values() else None
    if shot is None:
        return ST.picture(view)
    a, b = next((s[1], s[2]) for s in SHOTS if s[0] == shot)
    keep = B.SS
    B.SS = 1
    try:
        return picture(0.5 * (a + b))
    finally:
        B.SS = keep


def draw_order(t):
    return ['set back', 'people', 'set front']


def caption_at(t):
    return SUB.caption_at(LINES, t, PIECE_FIX)      # line 5 ends where she is last heard (brief 14: she drifts away)


def overlay(img, t):
    c = caption_at(t) if SUBS_IN_PICTURE else None
    if c:
        SUB.draw(img, c)
    return img


def frame_image(t):
    return overlay(picture(t), t)


def _gavel_knock():
    """A wooden gavel on a block: a sharp click, a hollow 'tock' and a short ring, about 0.5 s (made here: no sample)."""
    t = np.arange(int(0.5 * SR)) / SR
    rng = np.random.default_rng(12)
    click = rng.standard_normal(len(t)) * np.exp(-t * 400)
    tock = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 28) + 0.5 * np.sin(2 * np.pi * 420 * t) * np.exp(-t * 45)
    ring = 0.12 * np.sin(2 * np.pi * 1180 * t) * np.exp(-t * 22)
    x = 0.5 * click + 0.8 * tock + ring
    x[:int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))
    return 0.9 * x / np.abs(x).max()


MUSIC = os.path.join(HERE, '..', 'music', 'the-mountain-sad-hope.mp3')
MUSIC_SAD_END, MUSIC_PEAK = 12.9, 65.4   # the track's sad opening ends in a hush at 12.9 s; its hopeful lift hits 65.4 s


def music(n):
    """Sam's note 27: The Mountain under the film from the cell (prison) on: its sad opening, then (joined in the hush
    at 12.9 s) the build, so the hopeful lift lands as Brand hears the news (T['amazed'], the zoom on his face), to
    the end. Under every line it dips 12 dB; it fades out over the last 1.5 s. Licence: see music/README.md."""
    from burnham_film import load
    x = load(MUSIC)
    a = T['cell']
    jump = a + MUSIC_SAD_END                       # film time of the join
    p = MUSIC_PEAK - (T['amazed'] - jump)          # where the track picks up after the join
    out = np.zeros(n)
    i0, i1 = int(a * SR), int(jump * SR)
    out[i0:i1] = x[:i1 - i0]
    tail = x[int(p * SR):int(p * SR) + n - i1]
    xf = int(0.4 * SR)                            # a short crossfade in the hush
    out[i1 - xf:i1] *= np.linspace(1, 0, xf)
    tail = tail.copy()
    tail[:xf] *= np.linspace(0, 1, xf)
    out[i1 - xf:i1 - xf + len(tail)] += tail
    g = np.full(n, 0.30)                           # under the voices: lower than them, never fighting them
    k = np.hanning(int(0.3 * SR))
    for ln in LINES:
        g[int((ln['start'] - 0.15) * SR):int((ln['end'] + 0.15) * SR)] = 0.30 * 10 ** (-12 / 20)
    g = np.convolve(g, k / k.sum(), 'same')
    g[:i0 + int(0.8 * SR)] *= np.clip(np.linspace(-i0 / (0.8 * SR), 1, i0 + int(0.8 * SR)), 0, 1)   # in over 0.8 s
    e = int(DUR * SR)
    g[e - int(1.5 * SR):e] *= np.linspace(1, 0, int(1.5 * SR))
    g[e:] = 0
    return out * g * (np.abs(np.concatenate([ln['_voice'] for ln in LINES])).max() / (np.abs(x).max() + 1e-9))


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)
    for ln in LINES:
        s = int(ln['start'] * SR)
        seg = ln['_voice'][:max(0, n - s)].copy()
        if ln['n'] == 5:                              # brief 14: after the first phrases she drifts away and fades
            k0 = int((T['push'] - ln['start']) * SR)
            k1 = int((T['gates'] - 0.1 - ln['start']) * SR)
            if 0 < k0 < k1:
                m = min(len(seg), k1)
                seg[k0:m] *= (np.linspace(1.0, 0.0, k1 - k0) ** 1.5)[:m - k0]
                seg[k1:] = 0.0
        voice[s:s + len(seg)] += seg
    k = _gavel_knock()                                # Sam, 12 Nov: the gavel heard at the start of the sentencing shot
    i0 = int(T['bang'] * SR)
    rest[i0:i0 + len(k)] += k[:max(0, n - i0)]
    rest += music(n)                                  # note 27: The Mountain, from the cell on
    mix = voice + rest
    end = int(DUR * SR)
    if np.abs(voice).max() > 1e-6:
        mix, g = MA.master(mix, end)
        voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


def touch_faults():
    """The hands that hold or touch something, sampled through their shots (HANDS is the drawn hand circle's middle):
    the Bible in Brand's hand, the
    officer's grip on Brand's arm until the stop. TOUCHES stays empty: the flat film has no 3D scene for kitchecks."""
    out = []
    import numpy as _np
    a = T['s2']
    for t in _np.arange(a + 0.7, L[2]['end'], 0.5):                          # the Bible in the far hand
        sp = brand_sp(float(t), 'stand')
        j = oath(sp, float(t))
        c = _contact(j, 'L', F.HAND.get('fist', 14))
        xs, ys, zs = zip(*OATH_BOOK)
        if not (min(xs) - 20 <= c[0] <= max(xs) + 20 and min(ys) - 20 <= c[1] <= max(ys) + 20
                and min(zs) - 40 <= c[2] <= max(zs) + 20):
            out.append(f'oath {t:.2f}s: the hand is off the Bible ({c[0]:.0f}, {c[1]:.0f}, {c[2]:.0f})')
    for t in _np.arange(T['cell'] + 0.05, T['cell'] + ESC_STOP, 0.2):         # the officer's grip
        img = Image.new('RGBA', (1080, 1920))
        draw_people(img, _cam('escort', t), 'escort', float(t))
        ox, oy = HANDS[('officer', 'L')]
        gx, gy = GRIP_AT[0]
        if math.hypot(ox - gx, oy - gy) > 45:
            out.append(f'escort {t:.2f}s: the officer\'s hand is {math.hypot(ox - gx, oy - gy):.0f} px off his arm')
    return out


def checks():
    """Plan checks: subtitles printed to proofread, mouths on the words, the voice level. Raises on faults."""
    E.print_subtitles(caption_at, DUR, FPS)
    windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches']]
    faults = E.check_mouths(sorted(x for w in TRACK for x in TRACK[w]), windows)
    _, voice, rest = soundtrack(stems=True)
    faults += filmkit.voice_balance(voice, rest, SR, windows)
    import setcheck
    faults += setcheck.faults(SET_BOXES, SET_MEANT)
    import benchmark
    faults += benchmark.faults(sys.modules[__name__])
    faults += touch_faults()
    faults += BC.eye_faults()                     # rule S5, measured
    people = {sp['who']: sp.get('name', sp['who']) for sp in list(CAST.values()) + list(GUARDS.values())
              if sp['who'] != 'newsreader'}       # (she speaks: her mouth is the lip sync's, every frame)
    faults += BC.mouth_faults(people)             # notes 5, 13, 15: no front face without a mouth
    if faults:
        raise ValueError('check: ' + '; '.join(faults))
    print('checks: clean')


def _fx_tears(img):
    """His tears alone, large (rule S7: an effect drawn alone for the shape check)."""
    f = lambda u, v: (540 + 900 * u, 700 + 900 * v)
    BC.tears(B.Pen(img, B.Cam(1.0)), f, dict(ecx=0.12, ew=0.1, eye_y=0.0))


EFFECTS = [('tears', 'trail', _fx_tears),
           ('the TV light', 'glow', lambda img: ST.tv_flicker(img, B.Cam(1.0), 40.0))]
CK.install(sys.modules[__name__])


def main():
    a = sys.argv[1:]
    if a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'times':
        for s, t0, t1 in SHOTS:
            print(f'{s:8s} {t0:6.2f} {t1:6.2f}')
        print('DUR', round(DUR, 2))
    elif a[0] == 'check':
        B.SS = 1
        checks()
    elif a[0] == 'final':
        small = '--small' in a
        global SUBS_IN_PICTURE
        SUBS_IN_PICTURE = '--span' in a              # rule 70: a whole render goes on to finish.py
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)


if __name__ == '__main__':
    main()
