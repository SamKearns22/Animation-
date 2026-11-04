#!/usr/bin/env python3
"""Islamocommunism (notes/islamocommunism.md): three years into Islamic communism, President El-Sayed and Also-
President Ocasio-Cortez share non-alcoholic mimosas in the Oval Office and settle on what's next. Built from the satire
template (guides/satire.md); the room is MidTerminal's, redressed (islamocommunism_office); outside is
islamocommunism_set. Every indoor shot is flat (Sam's note 4, this film only): level, square to the wall, a long lens.

    python3 source/islamocommunism.py stills OUT_DIR T [T ...]   stills at these times (seconds)
    python3 source/islamocommunism.py keys OUT.jpg               one labelled still per beat (the stills sheet)
    python3 source/islamocommunism.py shots                      the timeline in numbers
    python3 source/islamocommunism.py check                      every check and the audit (also run by preflight.py)
    python3 source/islamocommunism.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1] [--nostamp]
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
import islamocommunism_office as OF   # noqa: E402  the Oval Office, redressed (patches midterminal_set on import)
import midterminal_set as MS     # noqa: E402  (its render, put; now drawing the redressed room)
import midterminal_moves as MV   # noqa: E402  the door, the walk-in
import islamocommunism_set as ISET   # noqa: E402  the White House front (shot 1)
import islamocommunism_cast as IC    # noqa: E402  El-Sayed, AOC
import views as V                # noqa: E402
import moves                     # noqa: E402
from ed import INK               # noqa: E402
from satire_style import install_circle_hands   # noqa: E402

mouths.install(B)
install_circle_hands(B)
FPS, SR = 12, MA.SR

# =============================================== STORY =============================================================
# MAP (rule 61: keep it in step; a note is answered by reading only these lines):
#   the cast: islamocommunism_cast.py; the room: islamocommunism_office.py (+ midterminal_set); the door and walk:
#   midterminal_moves.py; outside: islamocommunism_set.py (each has its own MAP). Here: LINES (the script, by number;
#   est = seconds until Sam's take replaces it) 60 | the timeline T 110 | SHOTS, CAMS, marks 150 | the checks' lists 175
#   | props (flutes, handset) 215 | arms and reaching 270 | each person's face and pose 300 | items, picture 440 |
#   captions, sound 490 | checks, audit 540 | sheets, main 610.
NAME = 'islamocommunism'
HAS = {'people', 'rooms', 'voices', 'props'}
TITLE = ()                                        # no title (CLAUDE.md)
TITLE_AT = dict(cap=116, top=310)
CAST = IC.CAST
WHO = ('elsayed', 'aoc')
# The script, word for word (brief rows 8-22). The audio files arrive 5 Nov (Sam); until then each line runs `est` s.
LINES = [
    dict(n=1, audio='islamocommunism-1', who='elsayed', est=4.2,
         text="Really? All diseases? Guess I don't need to call myself 'Doctor' any more."),
    dict(n=2, audio='islamocommunism-2', who='aoc', est=1.4, text='President El-Sayed?'),
    dict(n=3, audio='islamocommunism-3', who='elsayed', est=4.0,
         text='Good morning, Also-President Ocasio-Cortez. What do you have for me?'),
    dict(n=4, audio='islamocommunism-4', who='aoc', est=5.2,
         text='Non-alcoholic mimosa. I figured we deserved a slow morning after we finally solved climate change.'),
    dict(n=5, audio='islamocommunism-5', who='elsayed', est=2.8, text="Mashallah, it's a fine day to be a comrade."),
    dict(n=6, audio='islamocommunism-6', who='elsayed', est=9.5,
         text="You know, Madam President, when we decided to combine the spiritual philosophy of Islam with the "
              "Socio-Economic doctrine of communism, I didn't expect it would work so perfectly."),
    dict(n=7, audio='islamocommunism-7', who='aoc', est=3.4, text='Me neither. But here we are, American dream solved.'),
    dict(n=8, audio='islamocommunism-8', who='elsayed', est=1.2, text='No poverty.'),
    dict(n=9, audio='islamocommunism-9', who='aoc', est=3.5,
         text='Free everything paired inexplicably with total abundance.'),
    dict(n=10, audio='islamocommunism-10', who='elsayed', est=3.0,
         text="It's crazy that nobody had suggested trying it before."),
    dict(n=11, audio='islamocommunism-11', who='elsayed', est=3.0,
         text="So, what's next for our great American experiment?"),
    dict(n=12, audio='islamocommunism-12', who='aoc', est=1.2, text='Invade Europe?'),
    dict(n=13, audio='islamocommunism-13', who='elsayed', est=1.3, text='Invade Europe.'),
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
GAP = 0.3                                         # between one speaker's last word and the next one's first
CLEAR = 0.225                                     # a cut waits till the last subtitle clears (MidTerminal note 36)
T['usa'], T['beneath'] = 0.6, 1.6                 # brief row 6: "USA", 1 s later the line beneath
T['cut2'] = 5.0                                   # shot 2: the office
e = _at(1, T['cut2'] + 0.5)                       # sceptical, on the phone
T['hangup'] = e + 0.15                            # the handset down to the desk (0.45 s)
T['cut3'] = T['hangup'] + 0.55                    # shot 3: the door
T['open'] = T['cut3'] + 0.1
WALK = 1.1                                        # m/s: an easy walk, two full glasses
DOOR_PATH = None                                  # set below (needs the door's wall points)
e = _at(2, T['cut3'] + 1.2)                       # she's through the door and says it
T['cut4'] = e + CLEAR                             # shot 4: back to him; he stands (1.6 s), then line 3
T['rise'] = T['cut4'] + 0.15
e = _at(3, T['rise'] + 1.6)
T['cut5'] = e + CLEAR                             # shot 5: the two-shot; she walks in from the right
T['walk'] = T['cut5']
e = _at(4, T['cut5'] + 0.3)
T['offer'] = word_at(4, 'after we') - 0.2         # she holds his glass out to him for the line's last stretch
T['take'] = e + 0.2                               # brief row 12: he takes the glass, chuckles, then line 5
e = _at(5, T['take'] + 0.7)
T['sip'] = e + 0.4                                # brief row 13: both sip in the silence, smiling (2.4 s)
T['sip_end'] = T['sip'] + 2.4
e = _at(6, T['sip_end'] + 0.15)
e = _at(7, e + GAP)
e = _at(8, e + GAP)
e = _at(9, e + GAP)
e = _at(10, e + GAP)
T['pause'] = e                                    # brief row 19: a small pause
T['cut6'] = e + 0.9                               # shot 6: closer, for the button
e = _at(11, T['cut6'] + 0.2)
e = _at(12, e + GAP)
T['chuckle'] = e + 0.15
e = _at(13, T['chuckle'] + 0.45)
T['clink'] = e + 0.25                             # they clink glasses
DUR = T['clink'] + 1.2
BLACK_AT = DUR
# Sam (4 Nov, stills): vary the shots - singles of each, close-ups, medium two-shots. Each cut's name is its
# staging (office / door / two / clink, which places the people) plus a camera: _ab / _ao close on him / her,
# _aom her waist up, _med both waist up. Cuts between lines wait CLEAR after the last word.
def _after(n):
    return L[n]['end'] + CLEAR


SHOTS = [('ext', 0.0, T['cut2']), ('office', T['cut2'], T['cut3']), ('door', T['cut3'], T['cut4']),
         ('office', T['cut4'], T['cut5']), ('two', T['cut5'], T['take'] + 0.45), ('two_ab', T['take'] + 0.45, _after(5)),
         ('two_med', _after(5), T['sip_end']),
         ('two_ab', T['sip_end'], _after(6)), ('two_ao', _after(6), _after(7)), ('two_ab', _after(7), _after(8)),
         ('two_aom', _after(8), _after(9)), ('two_med', _after(9), T['cut6']),
         ('clink_ab', T['cut6'], _after(11)), ('clink_ao', _after(11), _after(12)), ('clink', _after(12), DUR)]
# Cameras (pos, look, focal), all level and square on (Sam's note 4: flat shots only, this film)
CAMS = {'office': ((0.0, 1.45, 0.4), (0.0, 1.45, 4.4), 1350),         # the desk end, front on, flags at the edges
        'door': OF.door_cam(),                                         # square on to the east door
        'two': ((0.55, 1.45, -0.2), (0.55, 1.45, 4.4), 1350),          # closer, both at the desk
        'clink': ((0.6, 1.5, 0.9), (0.6, 1.5, 4.4), 1200)}             # closer still, waist up
_AOZ = 3.15                                                            # her mark in the 'two' staging (AO)
CAMS.update({'two_ab': ((0.0, 1.55, 3.68 - 2.0), (0.0, 1.55, 6.0), 3000),       # close on him: head and shoulders
             'two_ao': ((1.3, 1.43, _AOZ - 2.0), (1.3, 1.43, 6.0), 3000),       # close on her
             'two_aom': ((1.3, 1.25, _AOZ - 2.3), (1.3, 1.25, 6.0), 2100),      # her, waist up (the hand sweep)
             'two_med': ((0.68, 1.4, 0.8), (0.68, 1.4, 6.0), 1350),       # both, waist up
             'clink_ab': ((0.0, 1.55, 3.68 - 2.0), (0.0, 1.55, 6.0), 3000),
             'clink_ao': ((1.12, 1.43, 3.25 - 2.0), (1.12, 1.43, 6.0), 3000)})
SHOT_CAST = {'ext': [], 'office': ['elsayed'], 'door': ['aoc'], 'two': ['elsayed', 'aoc'], 'clink': ['elsayed', 'aoc'],
             'two_ab': ['elsayed'], 'two_ao': ['aoc'], 'two_aom': ['aoc'], 'two_med': ['elsayed', 'aoc'],
             'clink_ab': ['elsayed'], 'clink_ao': ['aoc']}
LOOKS_AT = {'elsayed': 'aoc', 'aoc': 'elsayed'}
CHAIR = MS.DESK_CHAIR                              # (0, 3.75): seated just in front of it
AB = (0.0, 3.68)                                   # El-Sayed, seated and standing behind the desk
AO = (1.3, 3.15)                                   # her mark: beside the desk's right end
AO_CLINK = (1.12, 3.25)                            # a step nearer him for the clink (she steps in on the cut)
ENTER = [(2.55, 3.15), (2.0, 3.15), AO]            # shot 5: in from frame right, side on, to her mark
DX, _, DZ = MS.wp(MV.DOOR_A, 0.0, -0.9)            # in the corridor
TX, _, TZ = MS.wp(MV.DOOR_A, 0.0, 0.3)             # just through the door
IX, _, IZ = MS.wp(MV.DOOR_A, 0.0, 1.0)             # her stop, a metre in
DOOR_PATH = [(DX, DZ), (TX, TZ), (IX, IZ)]
PLAN = dict(CEIL=5.6, ROOMS=dict(MS.ROOMS, corridor=(4.42, -4.5, 7.0, 0.5)),
            OPENINGS={'east door': dict(wall=('x', 4.42), span=(-2.55, -1.5), sill=0.0, head=2.45,
                                        to='the West Wing corridor: cream walls, a red runner')},
            THINGS={'Resolute desk': dict(at=MS.DESK, size=(1.83, 0.91, 0.76), facing=180, why='ref oval-1')},
            PEOPLE={'elsayed': dict(at=AB, facing=180, who='elsayed', why='at the desk (brief 7)'),
                    'aoc': dict(at=AO, facing=180, who='aoc', why='beside the desk, right')},
            CAMS={k: dict(pos=v[0], look=v[1], focal=v[2]) for k, v in CAMS.items()}, GROUPS={},
            SHOT_MARKS={'office': ['elsayed'], 'two': ['elsayed', 'aoc'], 'clink': ['elsayed', 'aoc'],
                        'two_ab': ['elsayed'], 'two_ao': ['aoc'], 'two_aom': ['aoc'], 'two_med': ['elsayed', 'aoc'],
                        'clink_ab': ['elsayed'], 'clink_ao': ['aoc']})
BENCHMARK = [dict(place='oval office', refs=['oval-1-desk-gold.jpg', 'oval-3-both-ends.jpg'], at=T['cut2'] + 1.0,
                  items=[('gold swag valance and drapes', 'yes, a star band added'), ('three tall windows', 'arched heads'),
                         ('Resolute desk', 'a star on its front'), ('tufted leather chair', 'yes'),
                         ('flags either side', "the film's flag and a red banner"),
                         ('oval carpet with a seal', 'green, a star-and-wheat seal'), ('white pedimented doors', 'yes')]),
             dict(place='white house', refs=['89a1ee64-image.jpg', '49db6798-image.jpg'], at=2.0,
                  items=[(it, 'islamocommunism_set') for it in ('north portico', 'two floors of windows', 'balustrade',
                                                                 'fountain and red flowers', 'flags', 'lawn')])]
HOOK = (ISET.HOOK[0], {'y': ISET.HOOK[1]})         # "MAGAs Worst Nightmare" (Sam, 4 Nov), finish.py --y 410
KEEP_CLEAR = [(n, (lambda b: (lambda t: b if t < T['cut2'] else None))(box)) for n, box in ISET.KEEP_CLEAR
              if n != 'hook text']   # (that box is the Hook's own place in the sky, not something it must miss)
PROP_SIZES, OUTFIT = [], {}
HEIGHTS = {'elsayed': 1.78, 'aoc': 1.65}
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
THREE_QUARTER_OK = []                              # everyone front on at their marks; side on only while walking
PORTAL_OK = [('east door', None, T['open'] + 0.1, 'shut until it opens, then the corridor')]
ALLOWED_CONTACTS = [('elsayed.hand*', 'aoc.hand*', T['take'] - 0.1, T['take'] + 0.3, 'the glass handed over'),
                    ('elsayed.hand*', 'aoc.hand*', T['clink'] - 0.1, DUR, 'the clink')]
ALLOWED_POPS = [('aoc', T['cut3'], T['cut3'] + 1.2, 'through the door from the corridor'),
                ('aoc', T['cut5'], T['cut5'] + 1.2, 'walking in from the frame edge')]
SET_EXCLUDE = []
TOUCHES = [('aoc.handL', 'FLUTE_E', T['offer'], T['take'] + 0.2, 'offering his glass'),
           ('elsayed.handR', 'FLUTE_E', T['take'], DUR, 'his glass from the handover')]
FREE_MOVES, SOUND_SOURCES = [], {}
EFFECTS = []
JOKE_PROPS = []
ORDER_SWAPS = []
HANDS_OK = []
# The acting list (rule 74) is in notes/islamocommunism.md, "Acting"; each beat below names its line.
# ====================================================================================================================


def cut_of(t):
    """The cut on screen at t (its camera and who is drawn)."""
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def shot_of(t):
    """The staging at t (where people stand and what they do): the cut's name before any _camera."""
    return cut_of(t).split('_')[0]


def _ramp(t, a, b):
    return min(1.0, max(0.0, (t - a) / (b - a)))


def _ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def _bump(t, a, b, rise=0.2, fall=0.25):
    """0 -> 1 -> 0: up over `rise` from a, held, down over `fall` ending at b."""
    return _ease(_ramp(t, a, a + rise)) * (1 - _ease(_ramp(t, b - fall, b)))


TRACK = {w: [(a + ln['start'], b + ln['start'], sh) for ln in LINES if ln['who'] == w
             for a, b, sh in mouths.track(ln['text'], ln['_stretches'])] for w in WHO}
BLINKS = {w: F.blinks(17 + i, 0.5, DUR, talking=True) for i, w in enumerate(WHO)}


def _face(who, t):
    shape = mouths.at(TRACK[who], t)
    b, _, _ = beat(who, t)
    return dict(mouth='set' if shape == 'rest' else 'v:' + shape, blink=F.blinking(t, BLINKS[who]), brow_raise=b)


# Sam's note 8 (4 Nov): moderate brow and head moves on the key words (acting list): (who, line, word, brows, nod, tilt)
# brows = brow lift (px), nod = head dip (px, down then back), tilt = head tilt (degrees), over about 0.7 s
BEATS = [('elsayed', 1, 'All', 6, 0, 3), ('elsayed', 1, 'Guess', 0, 5, -3),
         ('elsayed', 3, 'Good', 4, 6, 0), ('elsayed', 3, 'What', 7, 0, 3),
         ('aoc', 4, 'deserved', 6, 0, -3), ('aoc', 4, 'finally', 0, 6, 0), ('aoc', 4, 'climate', 5, 0, 2),
         ('elsayed', 5, 'Mashallah', 7, 6, 0), ('elsayed', 5, 'comrade', 0, 5, 2),
         ('elsayed', 6, 'combine', 6, 0, 3), ('elsayed', 6, 'communism', 0, 6, 0),
         ('aoc', 7, 'neither', 5, 0, -4), ('aoc', 7, 'solved', 0, 6, 0),
         ('elsayed', 8, 'poverty', 3, 7, 0),
         ('aoc', 9, 'Free', 7, 0, -3), ('aoc', 9, 'abundance', 0, 6, 0),
         ('elsayed', 10, 'crazy', 7, 0, 0),
         ('elsayed', 11, 'great', 5, 0, 3), ('aoc', 12, 'Europe', 8, 0, -4), ('elsayed', 13, 'Europe', 3, 7, 0)]


def beat(who, t):
    b = n = tl = 0.0
    for w, ln, word, db, dn, dt in BEATS:
        if w != who:
            continue
        a = word_at(ln, word) - 0.1
        if a - 0.05 <= t < a + 0.75:
            k = _bump(t, a, a + 0.7, 0.15, 0.3)
            b, n, tl = b + db * k, n + dn * math.sin(math.pi * min(1.0, (t - a) / 0.5)) * (t >= a), tl + dt * k
    return b, n, tl


def _beat_j(j, who, t):
    _, n, tl = beat(who, t)
    j['head_dy'] = j.get('head_dy', 0) + n
    j['tilt'] = j.get('tilt', 0) + tl
    return j


def elsayed_j(t, c, x, z):
    return _beat_j(_elsayed_j(t, c, x, z), 'elsayed', t)


def aoc_j(t, c, x, z, walking):
    return _beat_j(_aoc_j(t, c, x, z, walking), 'aoc', t)


# ------------------------------------------------------------------------------------------------ props
MIMOSA = (246, 166, 52)
GLASS = (226, 238, 244)
GLASS_L = (250, 252, 255)


def flute(p, x, y, tilt=0.0, h=150.0):
    """A champagne flute of mimosa held at its stem (x, y = the hand), standing up (tilt: degrees, + leans right)."""
    a = math.radians(tilt)

    def r(dx, dy):                               # dy up (negative), about the hand
        return (x + dx * math.cos(a) - dy * math.sin(a), y + dx * math.sin(a) + dy * math.cos(a))
    w = h * 0.15
    p.poly([r(-w * 1.5, 40), r(w * 1.5, 40), r(w * 1.4, 46), r(-w * 1.4, 46)], GLASS, INK, 1.6)   # the foot
    p.line([r(0, 42), r(0, -42)], INK, 5.0)                                                          # the stem
    p.line([r(0, 42), r(0, -42)], GLASS_L, 2.4)
    bowl = [r(-w, -h + 30), r(w, -h + 30), r(w * 0.9, -60), r(w * 0.45, -44), r(-w * 0.45, -44), r(-w * 0.9, -60)]
    p.poly(bowl, GLASS, INK, 2.0)
    juice = [r(-w * 0.9, -h + 50), r(w * 0.9, -h + 50), r(w * 0.85, -62), r(w * 0.42, -48), r(-w * 0.42, -48),
             r(-w * 0.85, -62)]
    p.poly(juice, MIMOSA, None)
    p.line([r(-w * 0.9, -h + 50), r(w * 0.9, -h + 50)], (255, 214, 140), 2.0)                     # its surface
    p.line([r(-w * 0.55, -h + 40), r(-w * 0.6, -70)], GLASS_L, 2.4)                               # a highlight
    p.poly(bowl, None, INK, 2.0)


def held_flute(side, tilt=0.0):
    def draw(p, j2):
        x, y = j2['wr' + side]
        flute(p, x, y, tilt)
    draw.held = True
    return draw


def handset(side):
    """The desk phone's handset at his ear: a dark curved bar, ear cup at the hand, mouthpiece by the chin, the coiled
    cord falling to the desk."""
    def draw(p, j2):
        x, y = j2['wr' + side]
        ear, mouth = (x + 4, y - 22), (x * 0.4, y + 74)
        p.line([ear, mouth], INK, 30)
        p.line([ear, mouth], (40, 40, 46), 24)
        for c in (ear, mouth):
            p.ell(c[0], c[1], 20, 16, (40, 40, 46), INK, 2.0)
        p.ell(x, y + 18, 27, 27, IC.ELSAYED['skin'], INK, 2.4)                # his hand round it (a plain circle)
        pts = [(mouth[0] + 10 * math.sin(k * 1.6), mouth[1] + 14 + k * 9) for k in range(40)]
        p.line(pts, (40, 40, 46), 3.0)
    return draw


# ------------------------------------------------------------------------------------------------ arms
def _neck_units(c, sp, x, z, wx, wy, wz):
    """A world point in the person's own drawing units (x across the screen, y down from the neck)."""
    f = sp.get('height', 1.75) / 1.75
    neck = 928 * V.M_PER_UNIT * f
    (Xn, Yn), _ = c.project((x, neck, z))
    (Xf, Yf), _ = c.project((x, 0.0, z))
    s = max(1e-3, (Yf - Yn) / 928.0)
    (Xt, Yt), _ = c.project((wx, wy, wz))
    return (Xt - Xn) / s, (Yt - Yn) / s


def reach(j, c, sp, x, z, side, world, shape='grip', k=1.0, fwd=170.0):
    """The hand on `side` towards a world point (a handover, a clink), k of the way from where it is."""
    ux, uy = _neck_units(c, sp, x, z, *world)
    wx, wy, wz = j['wr' + side]
    V.arm_to(j, side, (wx + (ux - wx) * k, wy + (uy - wy) * k, wz + (fwd - wz) * k), 'down', shape)
    return j


def lift_shoulders(j, dy):
    for k in ('shL', 'shR', 'elL', 'elR', 'wrL', 'wrR'):
        if k in j:
            x, y, z = j[k]
            j[k] = (x, y + dy, z)
    j['head_dy'] = j.get('head_dy', 0) + dy
    return j


HOLD = {'L': (-95.0, 290.0, 150.0), 'R': (95.0, 290.0, 150.0)}    # a glass held at the waist, in front
SIP = {'L': (-30.0, -20.0, 150.0), 'R': (30.0, -20.0, 150.0)}      # the rim at the lips


def glass_at(j, side, target, tilt=0.0, face=False):
    V.arm_to(j, side, target, 'down', 'grip')
    j.setdefault('hand', {})[side] = 'grip'
    j['grip'] = set(j.get('grip', set())) | {side}
    j.setdefault('face_props' if face else 'props', []).append(held_flute(side, tilt))
    if face:
        j['on_face'] = set(j.get('on_face', set())) | {side}
        j['props'] = j.get('props', [])
    return j


def _mix(a, b, k):
    return tuple(p + (q - p) * k for p, q in zip(a, b))


# ------------------------------------------------------------------------------------------------ El-Sayed
def elsayed_sp(t):
    sp = dict(IC.ELSAYED, **_face('elsayed', t))
    s = shot_of(t)
    if s == 'office' and t < T['cut3']:            # brief 7: eyes sceptically to the phone at his ear (his right,
        sp['mood'], sp['look'] = 'sceptic', 0.75     # our right); on "Doctor" a dry half-smile
        if t >= word_at(1, 'Guess') - 0.1:
            sp['mood'], sp['look'] = 'neutral', 0.55
        return sp
    if s == 'office':                              # rising, then a warm greeting off to the door (our right)
        sp['mood'], sp['look'] = 'smile', 0.8
        return sp
    sp['look'] = 0.7                               # at her (she's on our right)
    sp['mood'] = 'smile'
    if T['sip'] <= t < T['sip_end']:              # brief 13: contented, eyes half shut, out at the room
        sp['look'], sp['mood'], sp['lid4'] = 0.0, 'neutral', 0.3
    elif L[11]['start'] - 0.2 <= t < word_at(11, 'great') - 0.1:   # "So, what's next": thinking, eyes up and away
        sp['look'], sp['gaze_dy'], sp['mood'] = -0.4, -3.5, 'neutral'
    elif L[8]['start'] - 0.1 <= t < L[8]['end'] + 0.2:
        sp['mood'] = 'neutral'                     # "No poverty": a calm, satisfied nod
    return sp


def _elsayed_j(t, c, x, z):
    """His pose: seated on the phone (line 1), hangs up, rises (1.6 s), hands at his sides; reaches for the glass she
    holds out (row 12) and keeps it; a small open hand on line 6; sips; the clink."""
    sp = IC.ELSAYED
    s = shot_of(t)
    if t < T['rise']:
        j = moves.seated(sp)
        j['seated'] = False                        # the set draws its own chair
        V.arm_to(j, 'L', DESK_ARM, (-0.6, 1.0, 0.7), 'fist')   # Sam's notes 4 + 4b: forward, resting on the desk top
        if t < T['hangup']:
            V.arm_to(j, 'R', (82.0, -140.0, 16.0), (0.6, 1.0, 0.7), 'none')
            j['face_props'] = [handset('R')]
            j['tilt'] = 4.0 * _ease(_ramp(t, word_at(1, 'All') - 0.1, word_at(1, 'All') + 0.15))
        else:
            k = _ease(_ramp(t, T['hangup'], T['hangup'] + 0.45))
            V.arm_to(j, 'R', _mix((82.0, -140.0, 16.0), (120.0, 330.0, 230.0), k), (0.6, 1.0, 0.7), 'none' if k < 1 else 'fist')
            if k < 1:
                j['props'] = [handset('R')]
                j['hand'] = dict(j.get('hand', {}), R='none')
        return j
    if t < T['rise'] + 1.6:
        j = moves.stand_up(sp, 0.18 + 0.82 * (t - T['rise']) / 1.6)   # Sam's note 3: straight up, no lean
        j['lean'] = 0.0                                                   # and sink first
        j['seated'] = False
        return j
    j = V.standing(sp)
    j['tilt'] = filmkit.shifts(t, seed=4)
    if s == 'office':
        if L[3]['start'] <= t < L[3]['end'] + 0.2:     # "What do you have for me?": an open palm out to her
            k = _bump(t, word_at(3, 'What'), L[3]['end'] + 0.2)
            V.arm_to(j, 'R', _mix(j['wrR'], (230.0, 210.0, 200.0), k), 'down', 'palm')
        return j
    has = t >= T['take']
    if not has:
        if t >= T['take'] - 0.45:                   # he reaches for it
            reach(j, c, sp, x, z, 'R', HANDOFF, 'grip', _ease(_ramp(t, T['take'] - 0.45, T['take'])))
        return j
    if T['sip'] <= t < T['sip_end']:
        k = _bump(t, T['sip'], T['sip_end'], 0.35, 0.4)
        return glass_at(j, 'R', _mix(HOLD['R'], SIP['R'], k), -12.5 * k, face=k > 0.5)
    if t >= T['clink'] - 0.45:
        k = _ease(_ramp(t, T['clink'] - 0.45, T['clink']))
        reach(j, c, sp, x, z, 'R', CLINK, 'grip', 1.0)
        tgt = _mix(HOLD['R'], j['wrR'], k)
        return glass_at(j, 'R', tgt, 0.0)
    if t < T['take'] + 0.5:                          # the glass comes back from her hand to his waist
        reach(j, c, sp, x, z, 'R', HANDOFF, 'grip', 1.0)
        tgt = _mix(j['wrR'], HOLD['R'], _ease(_ramp(t, T['take'] + 0.1, T['take'] + 0.5)))
        return glass_at(j, 'R', tgt)
    glass_at(j, 'R', HOLD['R'])
    a, b = word_at(6, 'when we decided'), word_at(6, 'I didn')
    k = _bump(t, a, b, 0.25, 0.35)                 # line 6: the free hand open, palm up, on "combine ... communism"
    if k > 0:
        V.arm_to(j, 'L', _mix(j['wrL'], (-210.0, 230.0, 200.0), k), 'down', 'palm')
    if L[13]['start'] - 0.5 <= t < L[13]['start']:  # the chuckle before "Invade Europe."
        j['head_dy'] = j.get('head_dy', 0) + 4 * abs(math.sin(2 * math.pi * 3.0 * t))
    if L[10]['start'] <= t < L[10]['end']:          # "It's crazy...": a slow small head shake of wonder
        j['tilt'] = j.get('tilt', 0) + 4 * math.sin(2 * math.pi * (t - L[10]['start']) / 1.4)
    return j


# ------------------------------------------------------------------------------------------------ Ocasio-Cortez
def aoc_sp(t):
    sp = dict(IC.AOC, **_face('aoc', t))
    s = shot_of(t)
    if s == 'door':                                # brief 9: bright, eyes to him at the desk (off left)
        sp['mood'], sp['look'] = 'smile', -0.7
        return sp
    sp['mood'], sp['look'] = 'smile', -0.7
    if T['sip'] <= t < T['sip_end']:
        sp['look'], sp['mood'], sp['lid4'] = 0.0, 'neutral', 0.3
    elif L[7]['start'] - 0.1 <= t < word_at(7, 'But') - 0.05:
        sp['mood'] = 'neutral'                     # "Me neither": a shrug, mouth sideways-flat
    elif L[12]['start'] - 0.3 <= t < L[13]['end'] + 0.3:
        sp['mood'] = 'hopeful'                     # brief 21: hopefully, brows up
    return sp


HANDOFF = (0.66, 1.12, 3.4)                         # where the glass changes hands, over the desk's right corner
CLINK = (0.6, 1.3, 3.05)                            # where the glasses meet


def _aoc_j(t, c, x, z, walking):
    """Her pose: two glasses held up in front as she walks (door, then into the two-shot); her left hand (our left,
    towards him) holds his glass out on "Non-alcoholic mimosa" until he takes it; her own glass in her right; a
    shrug on line 7; an open hand on line 9; a sip; the clink."""
    sp = IC.AOC
    j = moves.gait(sp, t, 'walk') if walking else V.standing(sp)
    if not walking:
        j['tilt'] = filmkit.shifts(t, seed=7)
    s = shot_of(t)
    two = s == 'door' or t < T['offer']
    if two:
        glass_at(j, 'L', (-80.0, 250.0, 170.0))
        glass_at(j, 'R', (80.0, 250.0, 170.0))
        return j
    if t < T['take']:                               # his glass held out to him, until his hand closes on it
        k = _ease(_ramp(t, T['offer'], T['offer'] + 0.4))
        start = (-80.0, 250.0, 170.0)
        jj = V.standing(sp) if not walking else j
        reach(jj, c, sp, x, z, 'L', HANDOFF, 'grip', 1.0)
        tgt = _mix(start, jj['wrL'], k)
        glass_at(j, 'L', tgt)
        glass_at(j, 'R', (80.0, 250.0, 170.0))
        return j
    if T['sip'] <= t < T['sip_end']:
        k = _bump(t, T['sip'] + 0.1, T['sip_end'] - 0.1, 0.35, 0.4)
        return glass_at(j, 'R', _mix(HOLD['R'], SIP['R'], k), -12.5 * k, face=k > 0.5)
    if t >= T['clink'] - 0.45:
        jj = V.standing(sp)
        reach(jj, c, sp, x, z, 'L', CLINK, 'grip', 1.0)
        k = _ease(_ramp(t, T['clink'] - 0.45, T['clink']))
        return glass_at(j, 'L', _mix(HOLD['L'], jj['wrL'], k))       # her glass moves to the hand nearer him
    if t >= T['cut6']:
        return glass_at(j, 'L', HOLD['L'])
    glass_at(j, 'R', HOLD['R'])
    if L[7]['start'] - 0.1 <= t < word_at(7, 'But'):  # brief 15: "Alex shrugs"
        k = _bump(t, L[7]['start'] - 0.1, word_at(7, 'But'), 0.15, 0.3)
        lift_shoulders(j, -22 * k)
        V.arm_to(j, 'L', _mix((-60.0, 380.0, 20.0), (-200.0, 300.0, 160.0), k), 'down', 'palm')
    a = word_at(9, 'Free')
    k = _bump(t, a, L[9]['end'] + 0.1, 0.3, 0.35)  # line 9: an open hand sweeping out on "total abundance"
    if k > 0:
        V.arm_to(j, 'L', _mix((-60.0, 380.0, 20.0), (-230.0, 200.0, 190.0), k), 'down', 'palm')
    return j


# ------------------------------------------------------------------------------------------------ items
SOLO = [None]                                     # the audit draws one person alone


def door_d(t):
    return max(0.0, WALK * (t - T['open'] - 0.15))


def walk_d(t):
    return max(0.0, WALK * (t - T['walk']))


def elsayed_item(t):
    x, z = AB
    sp = elsayed_sp(t)

    def draw(im, c):
        MS.put(im, c, sp, x, z, MS.to_cam(c, x, z), elsayed_j(t, c, x, z), t)
    return (x, z - 0.38, draw)                     # sorted at the chair's front: the desk covers his legs


def aoc_item(t):
    s = shot_of(t)
    sp = aoc_sp(t)
    if s == 'door':
        d = door_d(t)
        walking = MV.path_length(DOOR_PATH) - d > 0.02
        return MV.trump_item(t, d, sp, walking=walking, pts=DOOR_PATH,
                             arms=lambda j, c, x, z: aoc_j(t, c, x, z, walking))
    if s == 'two':
        d = walk_d(t)
        walking = MV.path_length(ENTER) - d > 0.02
        return MV.trump_item(t, d, sp, walking=walking, pts=ENTER,
                             arms=lambda j, c, x, z: aoc_j(t, c, x, z, walking))
    x, z = AO_CLINK

    def draw(im, c):
        MS.put(im, c, sp, x, z, MS.to_cam(c, x, z), aoc_j(t, c, x, z, False), t)
    return (x, z, draw)


def cam_for(t):
    pos, look, focal = CAMS[cut_of(t) if cut_of(t) != 'ext' else 'office']   # (ext: the audit asks; unused)
    return MS.S.Cam(pos, look, focal=focal)


DESK_ARM = (-160.0, 180.0, 270.0)                    # his free wrist on the desk top through the call (neck units)


def desk_arm_item(t):
    """The free forearm resting on the desk top, drawn again after the desk (which is in front of him and would hide
    it): his drawing with the arm on the desk, kept only where it differs from the same drawing with that arm down."""
    x, z = AB
    sp = elsayed_sp(t)

    def draw(im, c):
        j = elsayed_j(t, c, x, z)
        j2 = dict(j)
        V.arm_to(j2, 'L', (-200.0, -250.0, 0.0), 'out', 'fist')   # (raised clear, so only the desk arm differs)
        a = Image.new('RGBA', im.size, (0, 0, 0, 0))
        b = Image.new('RGBA', im.size, (0, 0, 0, 0))
        MS.put(a, c, sp, x, z, MS.to_cam(c, x, z), j, t)
        MS.put(b, c, sp, x, z, MS.to_cam(c, x, z), j2, t)
        A, Bv = np.asarray(a), np.asarray(b)
        m = (np.abs(A.astype(int) - Bv.astype(int)).sum(axis=2) > 24) & (A[..., 3] > 0)
        (_, yf), _ = c.project((x, 0.76, MS.DESK[1] - 0.455))     # the desk top's front edge: nothing below it
        m[int(max(0, yf)):] = False
        A2 = A.copy()
        A2[..., 3] = np.where(m, A[..., 3], 0)
        im.alpha_composite(Image.fromarray(A2))
    return (x, 2.3, draw)                          # sorted in front of the desk


def people(t):
    s = shot_of(t)
    out = []
    if s == 'office' and t < T['rise'] and SOLO[0] is None:
        out.append(desk_arm_item(t))
    if s == 'door':
        out += MV.door_items(MV.door_curve(t, T['open'], T['open'] + 0.4, 1e9))
    if 'elsayed' in SHOT_CAST[cut_of(t)] and SOLO[0] in (None, 'elsayed'):
        out.append(elsayed_item(t))
    if 'aoc' in SHOT_CAST[cut_of(t)] and SOLO[0] in (None, 'aoc'):
        out.append(aoc_item(t))
    return out


def picture(t):
    """The frame WITHOUT captions (they go on last, so wording notes never re-render a picture)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    ss = B.SS
    if shot_of(t) == 'ext':
        img = ISET.paint(t)                        # (drawn at 1080 wide, sets B.SS = 1)
        if t >= T['usa']:
            ISET.heading(img, t - T['usa'])
        B.SS = ss
        return img if ss == 1 else img.resize((1080 * ss, 1920 * ss), Image.LANCZOS)
    img = Image.new('RGBA', (1080 * ss, 1920 * ss), (0, 0, 0, 255))
    MS.render(img, cam_for(t), people(t))
    return img


def draw_order(t):
    """Rule 57: back to front, as MS.render sorts by distance from the camera."""
    if t >= BLACK_AT or shot_of(t) == 'ext':
        return ['background']
    c = cam_for(t)
    pos = {'elsayed': (AB[0], AB[1] - 0.38), 'aoc': AO}
    return ['background'] + sorted(SHOT_CAST[cut_of(t)], key=lambda w: -math.dist((pos[w][0], 1.0, pos[w][1]), c.pos))


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
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)        # voices only (CLAUDE.md: no sound effects unless asked)
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


def checks():
    """Plan checks: seconds. Raises on the first batch of faults; prints the subtitles to proofread."""
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches']]
    faults = E.check_mouths(sorted(x for w in WHO for x in TRACK[w]), windows)
    if any(ln['_voice'] is not None for ln in LINES):
        mix, voice, rest = soundtrack(stems=True)
        faults += filmkit.voice_balance(voice, rest, SR, windows)
        faults += filmkit.hiss_check(mix, SR, BLACK_AT, voice=voice + rest)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


# ------------------------------------------------------------------------------------------------ the audit
def scene(t):
    import audit
    s = shot_of(t)
    out = []
    for who in SHOT_CAST[cut_of(t)]:
        if who == 'elsayed':
            out.append(audit.Thing('elsayed', audit.simple('elsayed', AB[0], AB[1], HEIGHTS['elsayed'])))
        else:
            if s == 'door':
                x, z, _ = MV.trump_path(door_d(t), DOOR_PATH)
            elif s == 'two':
                x, z, _ = MV.trump_path(walk_d(t), ENTER)
            else:
                x, z = AO_CLINK
            out.append(audit.Thing('aoc', audit.simple('aoc', x, z, HEIGHTS['aoc'])))
    return out


def mouths_seen(t):
    c = cam_for(t) if shot_of(t) != 'ext' else None
    out = []
    for who in SHOT_CAST[cut_of(t)]:
        sp = elsayed_sp(t) if who == 'elsayed' else aoc_sp(t)
        out.append((who, sp['mouth'], 0.0, 120.0 if c is None else 2 * CAST[who].get('hh', 90) * 0.45))
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
                ts = [i / FPS for i in range(math.ceil(a * FPS), int(b * FPS))]
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


# ------------------------------------------------------------------------------------------------ sheets
KEYS = [   # the stills sheet: one per beat (label, time)
    ('1 outside: "USA", the line beneath', lambda: T['beneath'] + 1.0),
    ('2 on the phone, sceptical (line 1)', lambda: word_at(1, 'All') + 0.3),
    ('2 "Guess I don\'t need..." dry half-smile', lambda: word_at(1, 'Doctor')),
    ('3 the door: "President El-Sayed?" (2)', lambda: L[2]['start'] + 0.4),
    ('4 he rises', lambda: T['rise'] + 0.8),
    ('4 "What do you have for me?" (3)', lambda: word_at(3, 'have') + 0.2),
    ('5 she walks in (4)', lambda: T['walk'] + 0.6),
    ('5 "...solved climate change." glass out (4)', lambda: T['offer'] + 0.8),
    ('5 he takes it, chuckles', lambda: T['take'] + 0.25),
    ('5 "Mashallah..." (5)', lambda: L[5]['start'] + 0.8),
    ('5 the sip, contented (13)', lambda: (T['sip'] + T['sip_end']) / 2),
    ('5 close on him: "...combine..." (6)', lambda: word_at(6, 'combine') + 0.3),
    ('5 close on her: "Me neither." (7)', lambda: L[7]['start'] + 0.3),
    ('5 close: "No poverty." (8)', lambda: L[8]['start'] + 0.4),
    ('5 her waist up: "...total abundance." (9)', lambda: word_at(9, 'total')),
    ('5 both, waist up: "It\'s crazy..." (10)', lambda: L[10]['start'] + 0.6),
    ('6 close on him: "So, what\'s next...?" (11)', lambda: L[11]['start'] + 0.4),
    ('6 close on her: "Invade Europe?" (12)', lambda: L[12]['start'] + 0.5),
    ('6 both: the clink', lambda: T['clink'] + 0.3),
]


def keys(out):
    B.SS = 1
    tw, th, cols = 260, 462, 4
    rows = math.ceil(len(KEYS) / cols)
    sheet = Image.new('RGB', (cols * (tw + 10) + 10, rows * (th + 52) + 10), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 13)
    for i, (label, at) in enumerate(KEYS):
        t = at()
        x, y = 10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 52)
        sheet.paste(frame_image(t).convert('RGB').resize((tw, th), Image.LANCZOS), (x, y + 42))
        d.multiline_text((x, y), f'{label}\n{t:.1f} s', font=f, fill=(30, 30, 30))
    sheet.save(out, quality=86)


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
    elif a[0] == 'keys':
        keys(a[1])
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
                 picture=picture, overlay=overlay, shot_of=cut_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)


# Sam's note 2 (4 Nov): someone turned exactly to the lens sits on the drawing's mirror line, and rounding chose the
# side: in the wide two-shot El-Sayed was drawn mirror-image, so his right hand reached away from her and the glass
# jumped across. A hair off square keeps everyone the same way round in every shot.
_TO_CAM = MS.to_cam
MS.to_cam = lambda cm, x, z: _TO_CAM(cm, x, z) - 0.3
F.guard(B)
import limbs                     # noqa: E402
limbs.install(B)

if __name__ == '__main__':
    main()
