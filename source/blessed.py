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
import press_secretary as PS     # noqa: E402  the press pack from behind
import views as V                # noqa: E402
import moves                     # noqa: E402
from satire_style import install_circle_hands   # noqa: E402
from ed import INK               # noqa: E402

mouths.install(B)
install_circle_hands(B)
BC.MC.CAST.clear()
BC.MC.CAST.update(BC.CAST)
FPS, SR = 12, MA.SR

# =============================================== STORY =============================================================
NAME = 'blessed'
HAS = {'people', 'rooms', 'voices', 'props'}
TITLE = ()                                        # no title (CLAUDE.md)
TITLE_AT = dict(cap=116, top=310)
INMATE = dict(skin=(196, 150, 120), hw=66, hh=88, head_dy=10, hair='short', hair_c=(40, 32, 28), outfit='jumper',
              jacket=BC.TRACK, sleeve=BC.TRACK, trousers=BC.TRACK, shoe=(240, 240, 240), shoulders=156, full=True,
              pose='custom', height=1.78)
CAST = dict(BC.CAST,
            inmate1=dict(INMATE, who='inmate1', name='Inmate 1', seed=301),
            inmate2=dict(INMATE, who='inmate2', name='Inmate 2', skin=(120, 82, 60), hair='bald', hair_c=(30, 24, 20),
                         jacket=(110, 116, 124), sleeve=(110, 116, 124), shoulders=170, height=1.84, seed=302),
            inmate3=dict(INMATE, who='inmate3', name='Inmate 3', skin=(232, 190, 164), hair='side',
                         hair_c=(170, 120, 70), jacket=(150, 152, 156), sleeve=(150, 152, 156), height=1.72, seed=303))
LINES = [   # the script word for word (brief rows 5, 6, 7, 11, 13-14, 15); Sam's takes time every line
    dict(n=1, audio='blessed-1', who='brand', text="Yeah, I'm feeling blessed, mate, super blessed."),
    dict(n=2, audio='blessed-2', who='brand', text="I swear by Almighty God that the blessed evidence I shall give "
         "shall be the truth, the whole truth, and nothing but the blessed truth."),
    dict(n=3, audio='blessed-3', who='brand', text="Well that doesn't feel very blessed."),
    dict(n=4, audio='blessed-4', who='brand', text="Yeah, love. I'm not just not feeling blessed at all right now."),
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
T['s3'] = _at(2, T['s2'] + 0.5) + 0.6             # the oath, then the gavel
T['bang'] = T['s3'] + 0.9
T['s4'] = T['bang'] + 0.7                         # the dock: line 3
T['van'] = _at(3, T['s4'] + 0.6) + 0.8
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
SHOTS = [('arrive', T['s1'], T['s2']), ('oath', T['s2'], T['s3']), ('gavel', T['s3'], T['s4']),
         ('dock', T['s4'], T['van']), ('van', T['van'], T['cell']), ('escort', T['cell'], T['cot']),
         ('cot', T['cot'], T['phone']), ('phone', T['phone'], T['tvroom']), ('tvroom', T['tvroom'], T['tv']),
         ('tv', T['tv'], T['push']), ('push', T['push'], T['gates']), ('gates', T['gates'], DUR)]
VIEW = {'arrive': 'court_out', 'oath': 'court_box', 'gavel': 'court_bench', 'dock': 'court_dock', 'van': 'van',
        'escort': 'cell', 'cot': 'cell_cot', 'phone': 'phone', 'tvroom': 'tvroom', 'tv': 'tv', 'push': 'tvroom',
        'gates': 'gates'}
SHOT_CAST = {'arrive': ['brand'], 'oath': ['brand', 'judge'], 'gavel': ['judge'], 'dock': ['brand'],
             'van': ['brand'], 'escort': ['brand', 'officer'], 'cot': ['brand'], 'phone': ['brand'],
             'tvroom': ['brand'], 'tv': ['newsreader'], 'push': ['brand'], 'gates': ['brand']}
BENCHMARK = ST.BENCHMARK                          # rule 3: the sets' own (blessed_sets.py)
SET_BOXES, SET_MEANT = ST.SET_BOXES, ST.SET_MEANT  # rule 83
# Rule 1: the plan. A flat film: each place is its painting's Level camera in metres (blessed_sets); the marks are
# STAGE there. Listed for plan.py with each camera.
PLAN = dict(CEIL=3.0, ROOMS={v: (-6.0, 0.0, 6.0, 18.0) for v in ST.BACK}, OPENINGS={}, THINGS={},
            PEOPLE={}, CAMS={v: dict(pos=(0.0, 1.6, -1.0), look=(0.0, 1.6, 4.0)) for v in ST.BACK}, GROUPS={})

# What the shared checks need (preflight.py runs them all; guides/satire.md, 'Getting it right first time'):
HOOK = ('Russell Brand this week', {'y': 880})     # brief 17 (Claude's pick)
SUBS_IN_PICTURE = True
PIECE_FIX = {}
KEEP_CLEAR = []
PROP_SIZES = []
OUTFIT = {}
HEIGHTS = {w: c['height'] for w, c in CAST.items()}
FAMOUS = ['brand']
CUT_RESTS_OK = []
LOOKS_AT = {}
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
ALLOWED_CONTACTS, ALLOWED_POPS, SET_EXCLUDE = [], [], []
TOUCHES, FREE_MOVES, RESTS = [], [], []
SOUND_SOURCES, EFFECTS, JOKE_PROPS, ORDER_SWAPS = {}, [], [], []

GUARDS = {'guard1': BC.OFFICER,                   # two different officers (pass 2: twins)
          'guard2': dict(BC.OFFICER, skin=(236, 196, 170), hair='bob', hair_c=(170, 120, 70), shoulders=150,
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
    return V.person(img, cam, x, y - 928 * s, s, sp, t, yaw, j, head_yaw=head_yaw)


def put_seated(img, cam, sp, mark, t, yaw=0.0, j=None):
    """Someone seated, feet on the floor at the mark (the seated pose's own drop lowers him onto the seat)."""
    x, y, ppm = mark
    s = _s(sp, ppm)
    j = j or moves.seated(sp)
    j['seated'] = False                           # the set paints the seat
    return V.person(img, cam, x, y - 928 * s, s, dict(sp, full=True, pose='custom'), t, yaw, j)


PRESS_HAIR = [(58, 44, 36), (30, 24, 22), (150, 110, 70), (170, 166, 162), (110, 70, 46), (196, 196, 192)]
PRESS_JKT = [B.NAVY, B.CHARCOAL, (110, 40, 50), (70, 90, 120), (90, 96, 80), (150, 120, 90), (60, 60, 70)]
PRESS_STYLE = ['short', 'bob', 'pony', 'short', 'bald', 'curly', 'long', 'short']


def press(img, cam, L, spots, t, seed=0):
    """The press pack from behind (press_secretary.reporter: each their own build, clothes and haircut), far to
    near, standing on the pavement at (x, d) metres through the set's Level camera."""
    rng = np.random.default_rng(40 + seed)
    out = []
    for i, (x, d) in enumerate(spots):
        h = 1.62 + 0.2 * rng.random()
        X, Y = L.p(x, d, h - 0.25)                # the neck point
        out.append((d, dict(x=X, y=Y, s=L.ppm(d) / 650.0, hair=PRESS_HAIR[(i + seed) % 6],
                            jacket=PRESS_JKT[(i * 3 + seed) % 7], skin=[B.PALE, B.PINK, B.OLIVE, B.BROWN][i % 4],
                            style=PRESS_STYLE[(i + 2 * seed) % 8], hand=False, side=1, up_at=0.0,
                            seed=int(rng.integers(1e6)), empty=False, phone=False, pad=False, typing=False)))
    for i, (d, r) in enumerate(sorted(out, key=lambda q: -q[0])):
        kit = PRESS_KIT[(i + seed) % len(PRESS_KIT)]
        if kit == 'boom':
            _boom(img, cam, r, t)                          # the pole rises from hands hidden in front of him
        PS.reporter(img, cam, r, t)
        if kit == 'tv':
            _tv_camera(img, cam, r)


PRESS_KIT = ['tv', 'none', 'boom', 'none', 'tv', 'none', 'none', 'boom']


def _tv_camera(img, cam, r):
    """A TV camera on the right shoulder, seen from behind: the body beside the head, the battery on its back,
    the carry handle, the lens hood just showing past it (O3: the press must read as press)."""
    p = B.Pen(img, B.Local(cam, r['x'], r['y'], r['s']))
    p.poly([(56, -150), (250, -160), (256, -30), (60, -24)], (44, 46, 52), INK, 2.6)
    p.poly([(70, -132), (150, -136), (150, -44), (72, -40)], (24, 24, 28), INK, 1.8)         # the battery
    p.poly([(110, -186), (220, -190), (224, -160), (114, -156)], (60, 62, 68), INK, 2.0)     # the handle
    p.poly([(180, -176), (196, -176), (196, -150), (180, -150)], (60, 62, 68), None)
    p.ell(236, -96, 28, 34, (30, 30, 34), INK, 2.0)                                          # the lens hood
    p.ell(176, -60, 8, 8, (200, 40, 40), None)                                               # the tally light


def _boom(img, cam, r, t):
    """A boom microphone held up over the scrum: the pole from his hands (in front of him, hidden) up and forward,
    the furry grey windshield at its tip."""
    p = B.Pen(img, B.Local(cam, r['x'], r['y'], r['s']))
    sw = 1.0 + 0.02 * math.sin(t * 1.7 + r['seed'] % 7)
    tip = (-60 * sw, -640)
    p.line([(30, 60), tip], (70, 72, 78), 9)
    p.line([(30, 60), tip], INK, 1.2)
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
        return 'showman', ('lowered' if t > L[1]['start'] + 0.9 else 'on')
    if s == 'oath':
        return 'oath', None
    if s == 'dock':
        return 'hollow', None
    if s in ('van', 'escort'):
        return 'numb', None
    if s == 'cot':
        return 'weeping', None
    if s in ('phone', 'tvroom', 'tv'):
        return 'dejected', None
    if s == 'push':
        return ('overjoyed' if t >= T['overjoyed'] else 'amazed' if t >= T['amazed'] else 'dejected'), None
    return 'overjoyed', 'on'


def brand_sp(t, look):
    mood, shades = brand_mood(t)
    return dict(BC.LOOKS[look], **face('brand', t, mood, shades=shades))


# ---------------------------------------------------------------------------------------------- the shots
def _cam(view, t):
    """The camera on a view; the push is a slow zoom into his face on the tvroom painting (brief 14)."""
    if shot_of(t) == 'push':
        u = _ease(_ramp(t, T['push'], T['overjoyed'] + 0.6))
        x, y, ppm = ST.STAGE['tvroom']['brand']
        return B.Cam(1.0 + 1.6 * u, 540 + (x - 540) * u, 960 + (y - 0.95 * ppm - 960) * u)
    return ST.view_cam(view)[1]


def draw_people(img, cam, shot, t):
    view = VIEW[shot]
    st = ST.STAGE.get(view, {})
    if shot == 'arrive':
        put(img, cam, brand_sp(t, 'trial'), st['brand'], t)
        press(img, cam, ST.OUT, st['press'], t)
    elif shot == 'oath':
        x, y, ppm = st['judge']
        sj = _s(BC.JUDGE, ppm)
        put_seated(img, cam, dict(BC.JUDGE, **face('judge', t, 'neutral')), (x, y, ppm), t)
        ST.mid(view, img, cam, t)
        put(img, cam, brand_sp(t, 'stand'), st['brand'], t, yaw=-45)
    elif shot == 'gavel':
        put_seated(img, cam, dict(BC.JUDGE, **face('judge', t, 'neutral')), st['judge'], t)
    elif shot == 'dock':
        for g in ('guard1', 'guard2'):
            put_seated(img, cam, dict(GUARDS[g], **face('officer', t, 'neutral')), st[g], t)
        ST.mid(view, img, cam, t)
        put(img, cam, brand_sp(t, 'dock'), st['brand'], t)
    elif shot == 'van':
        put_seated(img, cam, brand_sp(t, 'prison'), st['brand'], t, yaw=35)
    elif shot == 'escort':
        put(img, cam, brand_sp(t, 'prison'), st['brand'], t, yaw=-30)
        put(img, cam, dict(BC.OFFICER, **face('officer', t, 'neutral')), st['officer'], t, yaw=-45)
    elif shot == 'cot':
        put_seated(img, cam, brand_sp(t, 'prison'), ST.STAGE['cell_cot']['brand'], t, yaw=30)
    elif shot == 'phone':
        sp = brand_sp(t, 'prison')
        pts = put(img, cam, sp, st['brand'], t, yaw=-45, j=handset_pose(sp))
        phone_cord(img, cam, pts, st['brand'], sp)
    elif shot in ('tvroom', 'push'):
        up = dict(gaze_dy=-0.7)                    # everyone watches the TV, high above the lens
        for w in ('inmate3', 'inmate1', 'inmate2'):
            put_seated(img, cam, dict(CAST[w], **face(w, t, 'neutral', **up)), st[w], t)
        sp = brand_sp(t, 'prison')
        if shot == 'tvroom':                       # brief 12: his eyes drift up to the screen
            sp['gaze_dy'] = -0.7 * _ease(_ramp(t, T['tvroom'] + 0.8, T['tvroom'] + 1.8))
        else:
            sp['gaze_dy'] = -0.7
        put_seated(img, cam, sp, st['brand'], t)
    elif shot == 'gates':
        put(img, cam, brand_sp(t, 'trial'), st['brand'], t)
        press(img, cam, ST.GATE, st['press'], t, seed=3)


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
    Facing left he is drawn mirrored: screen x = mark x - s * x."""
    from ed import open_curve
    x0, y0, ppm = mark
    s = _s(sp, ppm)
    wx, wy = pts['wr' + side]
    a = (x0 - s * wx, y0 - 928 * s + s * (wy + 70))
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
    feed = ST.studio_feed(t, dict(BC.NEWSREADER, **face('newsreader', t, 'neutral'))) if view == 'tv' else None
    ST.back(view, img, cam, t, feed)
    if view not in ('court_box', 'court_dock'):     # those two put the mid layer between their people
        ST.mid(view, img, cam, t)
    draw_people(img, cam, shot, t)
    ST.front(view, img, cam, t)
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
    c = SUB.caption_at(LINES, t, PIECE_FIX)
    if c and T['push'] + 2.5 < t < L[6]['start']:
        return None                                # brief 14: her words drift away (the voice fades too)
    return c


def overlay(img, t):
    c = caption_at(t) if SUBS_IN_PICTURE else None
    if c:
        SUB.draw(img, c)
    return img


def frame_image(t):
    return overlay(picture(t), t)


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)
    for ln in LINES:
        s = int(ln['start'] * SR)
        seg = ln['_voice'][:max(0, n - s)].copy()
        if ln['n'] == 5:                              # brief 14: after the first phrases she drifts away and fades
            k0 = int((T['push'] - ln['start']) * SR)
            k1 = min(len(seg), int((T['gates'] - 0.1 - ln['start']) * SR))
            if 0 < k0 < k1:
                seg[k0:k1] *= np.linspace(1.0, 0.0, k1 - k0) ** 1.5
                seg[k1:] = 0.0
        voice[s:s + len(seg)] += seg
    mix = voice + rest
    end = int(DUR * SR)
    if np.abs(voice).max() > 1e-6:
        mix, g = MA.master(mix, end)
        voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


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
    if faults:
        raise ValueError('check: ' + '; '.join(faults))
    print('checks: clean')


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
