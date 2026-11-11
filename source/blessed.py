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
T['gates2'] = L[6]['start'] + L[6]['_stretches'][0][1] + 0.12   # the cut just after "Blessed!": closer, at his mark
SHOTS = [('arrive', T['s1'], T['s2']), ('oath', T['s2'], T['s3']), ('gavel', T['s3'], T['s4']),
         ('dock', T['s4'], T['van']), ('van', T['van'], T['cell']), ('escort', T['cell'], T['cot']),
         ('cot', T['cot'], T['phone']), ('phone', T['phone'], T['tvroom']), ('tvroom', T['tvroom'], T['tv']),
         ('tv', T['tv'], T['push']), ('push', T['push'], T['gates']), ('gates', T['gates'], T['gates2']),
         ('gates2', T['gates2'], DUR)]
VIEW = {'arrive': 'court_out', 'oath': 'court_box', 'gavel': 'court_bench', 'dock': 'court_dock', 'van': 'van',
        'escort': 'cell', 'cot': 'cell_cot', 'phone': 'phone', 'tvroom': 'tvroom', 'tv': 'tv', 'push': 'tvroom',
        'gates': 'gates', 'gates2': 'gates2'}
SHOT_CAST = {'arrive': ['brand'], 'oath': ['brand', 'judge'], 'gavel': ['judge'], 'dock': ['brand'],
             'van': ['brand'], 'escort': ['brand', 'officer'], 'cot': ['brand'], 'phone': ['brand'],
             'tvroom': ['brand'], 'tv': ['newsreader'], 'push': ['brand'], 'gates': ['brand'],
             'gates2': ['brand']}
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
        return 'showman', ('lowered' if t >= word_at(1, 'mate') else 'on')
    if s == 'oath':
        return 'oath', None
    if s == 'dock':
        return ('hollow' if t >= 15.9 else 'neutral'), None
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


def _box_prop(j, box, col, mark=None):
    """A flat box held in the hand (the Bible), drawn from its 8 corners in 3D, leaning with the body."""
    def draw(p, j2):
        pts = [V.project(V.leaned(q, j.get('lean', 0.0)), j2['yaw'])[0] for q in box]
        p.poly(V._hull(pts), col, INK, 2.4)
        if mark:
            mark(p, j2)
    return draw


# --- arrive: he walks into the scrum, stops, snaps to face the cameras; heart, shades on "mate", arms wide on
#     "super", back to the heart with a little bow on the last "blessed"; at rest by 4.4 s (rule 72)
ARRIVE_FROM, ARRIVE_TO, ARRIVE_STOP = (1.2, 4.9), (0.45, 3.9), 1.35


def arrive(sp, t):
    """(mark, yaw, joints) for Brand arriving."""
    u = min(1.0, max(0.0, (t - T['s1']) / ARRIVE_STOP))
    x = ARRIVE_FROM[0] + (ARRIVE_TO[0] - ARRIVE_FROM[0]) * u
    d = ARRIVE_FROM[1] + (ARRIVE_TO[1] - ARRIVE_FROM[1]) * u
    mark = ST._mark(ST.OUT, x, d)
    walking = t < ARRIVE_STOP
    g = moves.gait(sp, t + 0.37, 'walk')
    j = moves.mix_poses(g, V.standing(sp), _ease(_ramp(t, ARRIVE_STOP - 0.15, ARRIVE_STOP + 0.15)))
    yaw = -45.0 if t < ARRIVE_STOP + 0.2 else 0.0
    if not walking:
        j['bob'] = 0.0
        j['lean'] = 0.0
    feel, mate, sup, last = (word_at(1, 'feeling'), word_at(1, 'mate'), word_at(1, 'super'),
                             word_at(1, 'blessed.'))
    sw = sp.get('shoulders', 150)
    heart = ((-30.0, 135.0, 78.0), 'in', 'palm')
    shades = ((-14.0, -194.0, 100.0), 'in', 'palm')
    wide = lambda sg: ((sg * (sw + 120), 200.0, 110.0), 'out', 'palm')
    arm_keys(j, sp, 'L', t, [(feel - 0.35, None), (feel, heart), (mate - 0.35, heart), (mate - 0.05, shades),
                             (mate + 0.1, shades), (sup + 0.05, wide(-1)), (last - 0.15, wide(-1)), (last + 0.2, heart),
                             (L[1]['end'] + 0.2, heart), (4.4, None)])
    arm_keys(j, sp, 'R', t, [(mate + 0.1, None), (sup + 0.05, ((sw + 120, 200.0, 110.0), 'out', 'fist')),
                             (last - 0.15, ((sw + 120, 200.0, 110.0), 'out', 'fist')), (last + 0.3, None)])
    if mate - 0.3 < t < mate + 0.25:
        j['on_face'] = {'L'}
    bow = _bump(t, last - 0.1, last + 0.7, 0.25, 0.35)
    j['lean'] = j.get('lean', 0.0) + 6 * bow
    j['nod'] = 1.4 * bow
    import grips
    grips.held(j, 'R', sp, _beads(sp))
    return mark, yaw, j


# --- oath: side-on in the box; Bible in the far hand, the near hand raised palm out; eyes up on "Almighty God"
def oath(sp, t):
    j = V.standing(sp)
    sw = sp.get('shoulders', 150)
    a = T['s2']
    up0, up1, dn0, dn1 = a + 0.15, a + 0.65, L[2]['end'] + 0.1, L[2]['end'] + 0.5
    bible = ((46.0, 172.0, 112.0), 'down', 'fist')
    raised = ((-(sw + 70), -40.0, 60.0), 'out', 'palm')
    arm_keys(j, sp, 'R', t, [(up0, None), (up1, bible), (dn0, bible), (dn1, None)])
    arm_keys(j, sp, 'L', t, [(up0, None), (up1, raised), (dn0, raised), (dn1, None)])
    for w in ('blessed evidence', 'blessed truth'):
        k = word_at(2, w)
        b = _bump(t, k - 0.05, k + 0.55, 0.15, 0.3)
        j['lean'] = j.get('lean', 0.0) + 4 * b
        j['nod'] = j.get('nod', 0.0) + 1.0 * b
    if t < dn0 + 0.05:
        import grips
        box = [(x, y, z) for x in (-34.0, 58.0) for y in (100.0, 236.0) for z in (100.0, 130.0)]

        def cross(p, j2):
            c = V.project(V.leaned((12.0, 150.0, 131.0), j.get('lean', 0.0)), j2['yaw'])[0]
            g = (214, 176, 70)
            p.poly([(c[0] - 4, c[1] - 26), (c[0] + 4, c[1] - 26), (c[0] + 4, c[1] + 26), (c[0] - 4, c[1] + 26)], g, None)
            p.poly([(c[0] - 15, c[1] - 12), (c[0] + 15, c[1] - 12), (c[0] + 15, c[1] - 4), (c[0] - 15, c[1] - 4)], g, None)
        grips.held(j, 'R', sp, _box_prop(j, box, (28, 26, 30), cross))
    return j


def oath_gaze(t):
    return -0.6 if word_at(2, 'Almighty') - 0.05 <= t < word_at(2, 'that the') else 0.0


# --- gavel: the judge takes the gavel, raises it to the shoulder, strikes on the bang, a small rebound, rests
GAVEL_HAND = [(T['s3'] + 0.11, (930.0, 1500.0, 0.0)), (T['s3'] + 0.36, (910.0, 1404.0, math.pi)),
              (T['s3'] + 0.71, (900.0, 1150.0, 2.25)), (T['bang'] - 0.15, (910.0, 1135.0, 2.35)),
              (T['bang'], (910.0, 1404.0, math.pi)), (T['bang'] + 0.12, (912.0, 1376.0, math.pi - 0.18)),
              (T['bang'] + 0.3, (910.0, 1404.0, math.pi))]


def gavel_at(t):
    """(hand x, hand y, gavel angle) on the frame: the hand on the handle's end drives the gavel (one grip point)."""
    if t <= GAVEL_HAND[0][0]:
        return GAVEL_HAND[0][1]
    for (t0, a), (t1, b) in zip(GAVEL_HAND, GAVEL_HAND[1:]):
        if t < t1:
            u = _ramp(t, t0, t1)
            u = moves.fast_in(u) if t1 == T['bang'] else _ease(u)
            return tuple(p + (q - p) * u for p, q in zip(a, b))
    return GAVEL_HAND[-1][1]


ST.GAVEL_LIFT = (T['s3'] + 0.36, T['s4'] + 1.0)


def gavel_pose(sp, t, mark):
    j = moves.seated(sp)
    s = _s(sp, mark[2])
    hx, hy, _ = gavel_at(t)
    px, py = _world_to_person(hx, hy, mark, s, 1, j['bob'])
    z = 150.0
    tgt = (px, py - V.ELEV * z, z)
    if t >= GAVEL_HAND[1][0] - 0.25:
        a = _ramp(t, GAVEL_HAND[0][0], GAVEL_HAND[1][0])
        r = _rest_spec(sp, 'R', j)
        _arm(j, 'R', moves.lerp(r[0], tgt, _ease(a)), moves.lerp(r[1], V.POLES['out'], _ease(a)), 14.0, 'fist')
    j['nod'] = 0.6 * _bump(t, T['bang'], T['bang'] + 0.25, 0.04, 0.2)
    return j


def gavel_draw(img, cam, t, pts, mark, sp, j):
    """The held gavel over the bench front and block, then his hand over its handle (P1)."""
    if not (ST.GAVEL_LIFT[0] <= t <= ST.GAVEL_LIFT[1]):
        return
    s = _s(sp, mark[2])
    hx, hy = HANDS[('judge', 'R')]
    ang = gavel_at(t)[2]
    p = B.Pen(img, cam)
    ST.gavel(p, hx + 150 * math.cos(ang), hy - 150 * math.sin(ang), ang)
    V.hand(B.Pen(img, B.Local(cam, mark[0], mark[1] - 928 * s + j['bob'] * s, s)), pts, 'R', sp, 'fist')


# --- dock: hands clasped low; still until 15.9 s, then hollow, the shoulders drop
def dock(sp, t):
    j = V.standing(sp)
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, (sg * 10, 420.0, 60.0), 'back')
    u = _ease(_ramp(t, 15.9, 16.9))
    j['bob'], j['head_dy'], j['lean'] = 12 * u, 10 * u, 4 * u
    return j


# --- van: bent over, forearms on the thighs, hands clasped between the knees, head down; the van sways him
def van(sp, t):
    j = moves.seated(sp)
    lean = 28 + 1.5 * math.sin(2 * math.pi * (t - T['van']) / 2.4)
    for sd, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, sd, unlean((sg * 8, 500.0, 250.0), lean), 'down')
    j['lean'], j['head_dy'], j['nod'] = lean, 10.0, 2.2
    return j


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
        yaw = -30.0
        a = T['cell'] + ESC_STOP
        head = -90.0 if a + 0.3 <= t < a + 0.9 else None      # a look left, then up to the window, then down
        j['nod'] = _keys(t, [(a + 0.9, 0.0), (a + 1.25, -1.6), (a + 1.6, -1.6), (a + 2.0, 1.4)])
    return _cell_mark(x, d), yaw, j, head


def escort_gaze(t):
    a = T['cell'] + ESC_STOP
    return _keys(t, [(a + 0.9, 0.0), (a + 1.2, -0.6), (a + 1.6, -0.6), (a + 1.9, 0.5)])


def officer_grip(sp, j, t, mark, brand_pts, brand_mark, brand_s):
    """His near hand ('L', facing left) on Brand's near upper arm until the stop, then back to his side."""
    k = t - T['cell']
    if k > ESC_STOP + 0.5:
        return j
    sh, el = brand_pts['shL'], brand_pts['elL']
    bx = brand_mark[0] - brand_s * (sh[0] + 0.45 * (el[0] - sh[0]))
    by = brand_mark[1] - 928 * brand_s + brand_s * (brand_pts.get('_bob', 0.0) + sh[1] + 0.45 * (el[1] - sh[1]))
    s = _s(sp, mark[2])
    px, py = _world_to_person(bx, by, mark, s, -1, j.get('bob', 0.0))
    xd = -20.0                                         # a little nearer the lens than his chest
    tgt = (xd, py - V.ELEV * (-xd), px)                # side view: screen x is the body's z; depth is -x
    held = ((tgt, 'down', 'fist'))
    arm_keys(j, sp, 'L', t, [(T['cell'] + ESC_STOP + 0.1, held), (T['cell'] + ESC_STOP + 0.5, None)])
    return j


# --- cot: curled on his side on the cot, weeping, a sob every 0.9 s


def cot_body(sp, t):
    import lying
    k, surf = lying.lie(sp, 'side', -0.65, 2.4, -90.0, ground=0.45)
    ph = ((t - T['cot']) % 0.9) / 0.9
    sob = math.sin(math.pi * min(1.0, ph / 0.35)) if ph < 0.35 else 0.0
    for n in ('neck', 'head', 'shL', 'shR', 'elL', 'elR', 'wrL', 'wrR'):
        if n in k:
            k[n] = k[n] + np.array([0.0, 0.005 * sob, 0.0])
    return k, surf


# --- phone: head down, a slow shake on "at all right now"
def phone_extra(t):
    a = word_at(4, 'at all')
    w = _ramp(t, a, a + 1.0)
    sh = math.sin(2 * math.pi * w) * (1 - w) * 1.4 if 0 < w < 1 else 0.0
    return dict(head_dx=6.0 * sh), 2.5 * sh


# --- TV room and the push: slouched; sits up on 'amazed', leans in on 'overjoyed'
def tv_pose(sp, t):
    j = moves.seated(sp)
    lean = _keys(t, [(T['amazed'], -6.0), (T['amazed'] + 0.6, 0.0), (T['overjoyed'], 0.0), (T['overjoyed'] + 0.6, 6.0)])
    j['lean'] = lean
    j['head_dy'] = _keys(t, [(T['amazed'], 6.0), (T['amazed'] + 0.6, 0.0)])
    j['nod'] = _keys(t, [(T['overjoyed'], 0.0), (T['overjoyed'] + 0.6, -1.0)])
    return j


# --- gates: out of the wicket door (wide), arms flung wide on "Blessed!"; then closer, striding to his mark,
#     a double pump on "everybody!"


def _gates_cut():
    return L[6]['start'] + L[6]['_stretches'][0][1] + 0.12


def _arms_wide(j, sp, t, t_up, side_first=True):
    """Both arms flung up and wide at t_up: out to the side on the way (figure-rig 3's waypoint), then up."""
    sw = sp.get('shoulders', 150)
    for sd, sg in (('L', -1), ('R', 1)):
        side = ((sg * (sw + 200), 120.0, 40.0), 'down', 'palm')
        up = ((sg * (sw + 170), -150.0, 50.0), 'down', 'palm')
        arm_keys(j, sp, sd, t, [(t_up - 0.35, None), (t_up - 0.12, side), (t_up + 0.1, up)])
    return j


def gates_wide(sp, t):
    k = t - T['gates']
    dd = GATE_D_OUT[0] + (GATE_D_OUT[1] - GATE_D_OUT[0]) * min(1.0, k / 0.8)
    mark = ST._mark(ST.GATE, 0.65, dd)
    g = moves.gait(sp, k, 'walk')
    j = moves.mix_poses(g, V.standing(sp), _ease(_ramp(k, 0.7, 0.95)))
    if k > 0.95:
        j['bob'] = 0.0
    _arms_wide(j, sp, t, word_at(6, 'Blessed!') + 0.1)
    return mark, 0.0, j


GATE_D_OUT = (ST.GATE_D + 0.2, ST.GATE_D - 0.52)
G2_FROM, G2_TO = 6.0, 4.6


def gates_close(sp, t):
    a = _gates_cut()
    k = t - a
    walk = (G2_FROM - G2_TO) / moves.speed('walk')
    u = min(1.0, max(0.0, k / walk))
    mark = ST._mark(ST.GATE, 0.6, G2_FROM + (G2_TO - G2_FROM) * u)
    g = moves.gait(sp, k + 0.25, 'walk')
    j = moves.mix_poses(g, V.standing(sp), _ease(_ramp(k, walk - 0.15, walk + 0.15)))
    if k > walk + 0.15:
        j['bob'] = 0.0
    sw = sp.get('shoulders', 150)
    ev = word_at(6, 'everybody')
    for sd, sg in (('L', -1), ('R', 1)):
        up = ((sg * (sw + 170), -150.0, 50.0), 'down', 'palm')
        hi = ((sg * (sw + 120), -230.0, 70.0), 'down', 'palm')
        arm_keys(j, sp, sd, t, [(ev - 0.05, up), (ev + 0.12, hi), (ev + 0.3, up), (ev + 0.45, hi), (ev + 0.7, up)])
    return mark, 0.0, j


# ---------------------------------------------------------------------------------------------- the shots
def _cam(view, t):
    """The camera on a view; the push is a slow zoom into his face on the tvroom painting (brief 14)."""
    if shot_of(t) == 'push':
        u = _ease(_ramp(t, T['push'], T['overjoyed'] + 0.6))
        x, y, ppm = ST.STAGE['tvroom']['brand']
        return B.Cam(1.0 + 1.6 * u, 540 + (x - 540) * u, 960 + (y - 0.95 * ppm - 960) * u)
    if shot_of(t) == 'gates':                     # a slow push on the wicket door
        u = _ease(_ramp(t, T['gates'], T['gates2']))
        x, y = ST.GATE.p(0.65, ST.GATE_D, 1.2)
        return B.Cam(1.0 + 0.35 * u, 540 + (x - 540) * u * 0.6, 960 + (y - 960) * u * 0.6)
    return ST.view_cam(view)[1]


def draw_people(img, cam, shot, t):
    view = VIEW[shot]
    st = ST.STAGE.get(view, {})
    HANDS.clear()
    if shot == 'arrive':
        sp = brand_sp(t, 'trial')
        mark, yaw, j = arrive(sp, t)
        put(img, cam, sp, mark, t, yaw, j)
        press(img, cam, ST.OUT, st['press'], t)
    elif shot == 'oath':
        x, y, ppm = st['judge']
        put_seated(img, cam, dict(BC.JUDGE, **face('judge', t, 'neutral')), (x, y, ppm), t)
        ST.mid(view, img, cam, t)
        sp = dict(brand_sp(t, 'stand'), gaze_dy=oath_gaze(t))
        put(img, cam, sp, st['brand'], t, yaw=-45, j=oath(sp, t))
    elif shot == 'gavel':
        sp = dict(BC.JUDGE, **face('judge', t, 'stern'))
        sp = dict(sp, full=True, pose='custom')
        j = gavel_pose(sp, t, st['judge'])
        j['seated'] = False
        mark = st['judge']
        s = _s(sp, mark[2])
        pts = V.person(img, cam, mark[0], mark[1] - 928 * s, s, sp, t, 0.0, j)
        _log_hands('judge', pts, mark, s, 1, j['bob'])
        DEFER.append(lambda: gavel_draw(img, cam, t, pts, mark, sp, j))
    elif shot == 'dock':
        for g in ('guard1', 'guard2'):
            put_seated(img, cam, dict(GUARDS[g], **face('officer', t, 'neutral')), st[g], t)
        ST.mid(view, img, cam, t)
        sp = brand_sp(t, 'dock')
        put(img, cam, sp, st['brand'], t, j=dock(sp, t))
    elif shot == 'van':
        sp = brand_sp(t, 'prison')
        put_seated(img, cam, dict(sp, gaze_dy=0.6), st['brand'], t, yaw=35, j=van(sp, t))
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
        import lying
        k, _ = cot_body(sp_cot := brand_sp(t, 'prison'), t)
        lying.draw(img, COT_CAM3, k, sp_cot, t)
    elif shot == 'phone':
        sp = brand_sp(t, 'prison')
        dx, roll = phone_extra(t)
        sp = dict(sp, head_dy=sp.get('head_dy', 0) + 8, gaze_dy=0.5, **dx)
        j = handset_pose(sp)
        j['lean'], j['head_roll'] = 5.0, roll
        pts = put(img, cam, sp, st['brand'], t, yaw=-45, j=j)
        phone_cord(img, cam, pts, st['brand'], sp)
        _log_hands('brand', pts, st['brand'], _s(sp, st['brand'][2]), -1)
    elif shot in ('tvroom', 'push'):
        up = dict(gaze_dy=-0.7)                    # everyone watches the TV, high above the lens
        for w in ('inmate3', 'inmate1', 'inmate2'):
            put_seated(img, cam, dict(CAST[w], **face(w, t, 'neutral', **up)), st[w], t)
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
        press(img, cam, ST.GATE, st['press'], t, seed=3)
    elif shot == 'gates2':
        sp = brand_sp(t, 'trial')
        mark, yaw, j = gates_close(sp, t)
        put(img, cam, sp, mark, t, yaw, j)
        press(img, cam, ST.GATE, ST.STAGE['gates']['press'], t, seed=3)


DEFER = []                                        # drawn after the set's front layer (the held gavel over the block)
import sets as S3                                 # noqa: E402  the cot close-up's 3D camera: the cell painting at
COT_CAM3 = S3.Cam((0, 1.55, 0), (0, 1.55, 1), focal=1550, shake=(325.5, -677.35))   # B.Cam(1.55, 330, 1240)


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
