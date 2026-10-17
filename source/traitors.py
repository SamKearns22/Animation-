#!/usr/bin/env python3
"""The Traitors (TikTok satire, Sam 17 Oct): the final Round Table. Claudia asks Trump why he thinks Zelensky is a
traitor; Trump, holding up his ZELENSKY slate, answers; across the table sit Putin, spattered in blood, and Zelensky,
head in his hands: "Jesus Christ." Notes and decisions: notes/traitors.md. People: source/traitors_cast.py.
Guide: guides/satire.md.

    python3 source/traitors.py cast OUT.jpg              the cast sheet (every view used, the reaction strengths)
    python3 source/traitors.py stills OUT_DIR T [T ...]  stills at these times (seconds)
    python3 source/traitors.py sheet OUT.jpg [T ...]     several stills side by side on one sheet
    python3 source/traitors.py check                     every check and the audit (also run by preflight.py)
    python3 source/traitors.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import traitors_cast as C        # noqa: E402  (installs the four heads and outfits into burnham)
import views as V                # noqa: E402
import moves                     # noqa: E402
import figure as F               # noqa: E402
import mouths                    # noqa: E402
import mossad_audio as MA        # noqa: E402
import peepee as PP              # noqa: E402
import filmkit                   # noqa: E402
import film_engine as E          # noqa: E402
from ed import INK, curve        # noqa: E402
from satire_style import rough, install_circle_hands   # noqa: E402

install_circle_hands(B)
FPS, SR = 12, MA.SR
NAME = 'traitors'

# =============================================== STORY ==============================================================
# Each take is laid at `at` (film seconds where the file starts, after trimming `trim` seconds of silence off its
# front). Speech in the takes (MA.pauses): Claudia 0.83-6.27 (5 phrases, her slow, dramatic delivery, kept);
# Trump 0.27-13.13 (5 phrases: "...trust him." / "Because ... disgrace." / "... my deals." / "And because." /
# "And because I just don't like looking at him."; the 1.1 s stall before the last is the joke, kept);
# Zelensky 1.42-2.84.
LINES = [
    dict(n=1, who='claudia', text='Donald Trump, why do you think Zelensky is a traitor?', audio='traitors-1',
         trim=0.33, at=0.0),
    dict(n=2, who='trump', text="I'm voting for him because I don't trust him. Because I think he's a disgrace. "
                                "He doesn't like any of my deals. And because. And because I just don't like looking at him.",
         audio='traitors-2', trim=0.0, at=6.63),
    dict(n=3, who='zelensky', text='Jesus Christ.', audio='traitors-3', trim=0.0, at=20.48),
]
L1, L2, L3 = (LINES[0]['at'] - LINES[0]['trim'], LINES[1]['at'], LINES[2]['at'])   # file-time origins
SHOTS = [('claudia', 0.0, 6.5), ('trump', 6.5, 15.4), ('trump_close', 15.4, 20.3), ('arc', 20.3, 24.4)]
DUR = BLACK_AT = 24.4
# Subtitles: (start, end, text): each with its first word (Sam, 16 Oct: never ahead of the voice); the punchline on
# its own, on its word ("I" at 11.32 s in Trump's take, its syllable peak). The second "And because" (0.45 s before
# the punchline) is not given its own subtitle: it would flash up for a third of a second. Times in file seconds + the take's origin.
CAPS = [   # short chunks, two to five words (Sam, 17 Oct: the text changes about once a second)
    (L1 + 0.93, L1 + 2.24, 'Donald Trump,'),
    (L1 + 2.24, L1 + 3.51, 'why do you think'),
    (L1 + 3.61, L1 + 4.77, 'Zelensky'),
    (L1 + 4.80, L1 + 6.57, 'is a traitor?'),
    (L2 + 0.37, L2 + 1.25, "I'm voting for him"),
    (L2 + 1.25, L2 + 2.82, "because I don't trust him."),
    (L2 + 3.27, L2 + 3.88, 'Because I think'),
    (L2 + 3.88, L2 + 5.33, "he's a disgrace."),
    (L2 + 5.75, L2 + 6.30, "He doesn't like"),
    (L2 + 6.30, L2 + 8.38, 'any of my deals.'),
    (L2 + 9.02, L2 + 10.92, 'And because.'),
    (L2 + 10.92, L2 + 11.32, 'And because'),       # brief, but kept (Sam, 17 Oct)
    (L2 + 11.32, L2 + 11.92, "I just don't like"),
    (L2 + 11.92, L2 + 13.5, 'looking at him.'),
    (L3 + 1.52, L3 + 3.2, 'Jesus Christ.'),
]
HOOK = 'The Traitors: the final three'
JABS = [L2 + 1.30, L2 + 3.21, L2 + 9.12, L2 + 11.04]       # "because": Trump jabs his slate (syllable peaks)
SEARCH = (L2 + 9.8, L2 + 10.85)                            # the stall: his eyes drift up and away for a reason
SNEER = (L2 + 11.95, SHOTS[2][2])                           # "looking at him": a glance across at Zelensky, the sneer
Z_SINK = [(20.3, 2.0), (20.7, 2.0), (21.75, 4.0), (23.0, 5.0)]   # Zelensky's head-in-hands strength (Sam: 2 -> 5)
TABLE_Y = 300             # a seated player's edge of the table, in their own units (neck at 0, shoulders at 60)
STAND_Y = 430             # the table's edge for someone standing (Claudia)
SLATE_W = 210             # the slate's width in person units (about 25 cm)
BLOOD = C.spatter()
# ====================================================================================================================


def _voice(ln):
    v = MA.line(ln['audio'])
    return v[int(ln['trim'] * SR):]


for ln in LINES:
    ln['_voice'] = _voice(ln)
    ln['start'] = ln['at']
    ln['end'] = ln['at'] + len(ln['_voice']) / SR
    ln['_stretches'] = MA.pauses(ln['_voice'], 0.12)
TRACK = {ln['who']: [(a + ln['start'], b + ln['start'], sh) for a, b, sh in mouths.track(ln['text'], ln['_stretches'])]
         for ln in LINES}
WINDOWS = {ln['who']: [(ln['start'] + a, ln['start'] + b) for a, b in ln['_stretches']] for ln in LINES}


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def keyed(t, keys):
    """A value eased between (time, value) keys, held before the first and after the last."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t < t1:
            return v0 + (v1 - v0) * ease((t - t0) / (t1 - t0))
    return keys[-1][1]


def talking_mouth(who, t):
    sh = mouths.at(TRACK.get(who, []), t)
    return 'rest' if sh == 'rest' else 'v:' + sh


# ------------------------------------------------------------------------------------------------ poses
HEAD = {2: dict(dy=12, lean=4, hand=(74, -40, 50)), 3: dict(dy=26, lean=10, hand=(62, -34, 80)),
        4: dict(dy=40, lean=16, hand=(44, -46, 96)), 5: dict(dy=54, lean=22, hand=(34, -6, 104)),
        6: dict(dy=74, lean=28, hand=(28, 14, 110))}
DOWN = {1: 0.2, 2: 0.3, 3: 0.5, 4: 0.7, 5: 0.85, 6: 1.0}


def head_in_hands(j, k):
    """Zelensky's head in his hands at any strength from 2 to 6 (between the drawn ones, blended)."""
    a = max(2, min(5, int(math.floor(k))))
    b = min(6, a + 1)
    u = min(1.0, max(0.0, k - a))
    A, Bk = HEAD[a], HEAD[b]
    lerp = lambda x, y: x + (y - x) * u
    dy = lerp(A['dy'], Bk['dy'])
    j['head_dy'] = dy
    j['lean'] = lerp(A['lean'], Bk['lean'])
    hy = -150.0 + dy
    hx, yy, z = (lerp(A['hand'][i], Bk['hand'][i]) for i in range(3))
    for s, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, s, (sg * hx, hy + yy, z), (0.5, 1.0, 0.6), 'palm')
    j['on_face'] = {'L', 'R'}
    return DOWN[a] + (DOWN[b] - DOWN[a]) * u


def seated_pose(sp, kind, strength=4, lift=0.0):
    """The upper body of a player behind the table (the table hides the rest). kind: 'slate' (Trump holds his slate
    up at the chest, a hand on each side; `lift` raises it for a jab), 'folded' (Putin's hands folded on the table),
    'head' (Zelensky's head in his hands, strength 1-6), 'clasped' (Claudia standing, hands together at the waist)."""
    j = V.standing(sp)
    j['props'] = []
    if kind == 'slate':
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * (SLATE_W / 2 + 4), 236.0 - lift, 170.0 + lift * 0.6), 'down', 'fist')
    elif kind == 'folded':
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * 16, TABLE_Y + 40, 230.0), 'down', 'fist')
    elif kind == 'clasped':
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * 16, 400.0, 90.0), 'back')
        j['props'] = [lambda p, j2: (C.frill(p, j2, 'L'), C.frill(p, j2, 'R'))]
    elif kind == 'head':
        if strength < 1.5:                             # 1: one hand rubbing his forehead, the other on the table
            j['head_dy'], j['lean'] = 6, 2
            V.arm_to(j, 'R', (14.0, -198.0, 96.0), (1.0, 0.5, 0.2), 'palm')
            V.arm_to(j, 'L', (-60.0, TABLE_Y + 40, 230.0), 'down', 'fist')
            j['on_face'] = {'R'}
            j['_down'] = DOWN[1]
        else:
            j['_down'] = head_in_hands(j, strength)
    return j


SP = {'trump': C.TRUMP, 'putin': C.PUTIN, 'zelensky': C.ZELENSKY, 'claudia': C.CLAUDIA}


def person(img, cam, x, y, s, who, sp, j, t, blood=True):
    """Draw one person (Putin with his blood laid over him only). Returns the drawn joints (his units)."""
    j2 = {}
    if who == 'putin' and blood:
        C.bloody(img, cam, x, y, s, lambda im: j2.update(V.person(im, cam, x, y, s, sp, t, 0, j)),
                 BLOOD + C.hand_smears([(-16, TABLE_Y + 34), (16, TABLE_Y + 34)]))
    else:
        j2.update(V.person(img, cam, x, y, s, sp, t, 0, j))
    return j2


def arms_over_table(img, cam, x, y, s, who, sp, j, j2):
    """Forearms resting on the table lie over its edge: drawn again after the table (with Putin's blood)."""
    sides = [sd for sd in 'LR' if sd not in j.get('on_face', ()) and j2.get('hand', {}).get(sd) == 'fist'
             and j['wr' + sd][1] > TABLE_Y - 40]
    if not sides:
        return
    L = B.Local(cam, x, y, s)

    def arms(im):
        q = B.Pen(im, L)
        for sd in sides:
            V.arm(q, j2, sd, sp)
    if who == 'putin':
        hands = []
        for sd in sides:
            el, wr = j2['el' + sd], j2['wr' + sd]
            d = math.hypot(wr[0] - el[0], wr[1] - el[1]) or 1.0
            hands.append((wr[0] + (wr[0] - el[0]) / d * 12, wr[1] + (wr[1] - el[1]) / d * 12))
        C.bloody(img, cam, x, y, s, arms, BLOOD + C.hand_smears(hands))
    else:
        arms(img)


# ------------------------------------------------------------------------------------------------ the room
PANEL = (78, 46, 28)
PANEL_L = (98, 60, 36)
PANEL_D = (54, 32, 20)
LATTICE = (40, 24, 16)
SHADE = (250, 214, 140)


def wall(img, cam, x0, x1, y0, y1, seed=0, panel_w=300, lamps=()):
    """The Round Table room's walls (refs 1, 3, 6, 7): dark panelled wood in tall framed panels, a band of diamond
    lattice grilles low down, a moulded rail, brass wall lamps with lit shades. Flat colour, hand-cut edges."""
    p = B.Pen(img, cam)
    p.poly(rough([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 4, seed), PANEL, INK, 2.6)
    k = 0
    x = x0 + 20
    rail = y0 + (y1 - y0) * 0.62
    while x < x1:
        w = panel_w
        p.poly(rough([(x + 16, y0 + 40), (x + w - 16, y0 + 40), (x + w - 16, rail - 30), (x + 16, rail - 30)], 3, seed + k),
               PANEL_L, INK, 2.2)
        p.poly(rough([(x + 34, y0 + 60), (x + w - 34, y0 + 60), (x + w - 34, rail - 50), (x + 34, rail - 50)], 3, seed + k + 50),
               PANEL, PANEL_D, 1.8)
        g0, g1 = rail + 24, y1 - 30                    # the lattice grille in the lower panel
        p.poly([(x + 22, g0), (x + w - 22, g0), (x + w - 22, g1), (x + 22, g1)], LATTICE, INK, 2.0)
        step = 34
        for u in range(-int((g1 - g0) / step), int(w / step) + 2):
            xa = x + 22 + u * step
            p.line([(max(x + 22, xa), g0 + max(0, x + 22 - xa)), (min(x + w - 22, xa + (g1 - g0)), g0 + min(g1 - g0, x + w - 22 - xa))],
                   PANEL_L, 2.2)
            xb = x + w - 22 - u * step
            p.line([(min(x + w - 22, xb), g0 + max(0, xb - (x + w - 22))), (max(x + 22, xb - (g1 - g0)), g0 + min(g1 - g0, xb - x - 22))],
                   PANEL_L, 2.2)
        x += w
        k += 1
    p.poly([(x0, rail - 14), (x1, rail - 14), (x1, rail + 14), (x0, rail + 14)], PANEL_L, INK, 2.2)   # the rail
    for lx, ly in lamps:
        p.poly([(lx - 6, ly + 10), (lx + 6, ly + 10), (lx + 6, ly + 60), (lx - 6, ly + 60)], (150, 112, 52), INK, 1.8)
        p.poly([(lx - 30, ly + 14), (lx + 30, ly + 14), (lx + 20, ly - 30), (lx - 20, ly - 30)], SHADE, INK, 2.0)


def chair_back(img, cam, x, y, s, seat_c=(226, 190, 70)):
    """A carved wooden chair (refs 1, 3, 6) seen from the front of its back, in the units of someone seated in it
    (neck at y): curved crest rail, a cut-out handle, the back down to the table's edge."""
    L = B.Local(cam, x, y, s)
    p = B.Pen(img, L)
    wood, wd = (122, 72, 38), (88, 50, 26)
    back = curve([(-118, 330), (-122, 120), (-128, -20), (-96, -66), (-40, -54), (0, -76), (40, -54), (96, -66),
                  (128, -20), (122, 120), (118, 330)], 3)
    p.poly(back, wood, INK, 2.4)
    p.poly(curve([(-34, -24), (34, -24), (30, 4), (-30, 4)], 3), (30, 18, 12), INK, 1.8)        # the handle cut-out
    p.line([(-100, 60), (-96, 300)], wd, 2.0)
    p.line([(100, 60), (96, 300)], wd, 2.0)


def ell_pt(cx, cy, rx, ry, a, r=1.0):
    return (cx + rx * r * math.cos(a), cy + ry * r * math.sin(a))


def round_table(img, cam, cx, cy, rx, ry, seats, thick=36):
    """The whole Round Table in perspective (refs 1, 2, 4): gilded rim, blue-green border with gold stars, the lit
    ring of white plates (one at every place), polished wood, the compass star, the raised dais with its moon."""
    p = B.Pen(img, cam)
    E_ = lambda r, n=120: [ell_pt(cx, cy, rx, ry, a, r) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    near = [ell_pt(cx, cy, rx, ry, a) for a in np.linspace(0, math.pi, 60)]
    p.poly(near + [(x, y + thick) for x, y in near[::-1]], C.WOOD_D, INK, 2.4)                 # the edge we see
    p.poly(E_(1.0), C.STAR_GOLD, INK, 2.4)
    p.poly(E_(0.985), C.BORDER, None)
    for a in np.linspace(0, 2 * math.pi, 44, endpoint=False):                                    # stars in the border
        x, y = ell_pt(cx, cy, rx, ry, a, 0.94)
        k = 0.3 + 0.7 * (math.sin(a) + 1) / 2                                                   # nearer: bigger
        pts = [(x + (13 if i % 2 == 0 else 5) * k * math.cos(i * math.pi / 8),
                y + (13 if i % 2 == 0 else 5) * k * 0.45 * math.sin(i * math.pi / 8)) for i in range(16)]
        p.poly(pts, C.STAR_GOLD, None)
    p.poly(E_(0.89), C.RING, INK, 1.6)
    p.poly(E_(0.875), C.WOOD, INK, 1.8)
    for a in seats:                                                                              # the lit plates
        x, y = ell_pt(cx, cy, rx, ry, a, 0.88)
        k = 0.45 + 0.55 * (math.sin(a) + 1) / 2
        p.ell(x, y, 30 * k + 5, (30 * k + 5) * ry / rx * 1.1, (60, 50, 44), INK, 1.6)
        p.ell(x, y, 30 * k, 30 * k * ry / rx * 1.1, C.RING, None)
    for i in range(16):                                                                          # the compass star
        a = i * math.pi / 8 - math.pi / 2
        r = 0.8 if i % 2 == 0 else 0.48
        tip = ell_pt(cx, cy, rx, ry, a, r)
        l = ell_pt(cx, cy, rx, ry, a - math.pi / 8 * (0.55 if i % 2 == 0 else 0.4), 0.22)
        rr = ell_pt(cx, cy, rx, ry, a + math.pi / 8 * (0.55 if i % 2 == 0 else 0.4), 0.22)
        m = ell_pt(cx, cy, rx, ry, a, 0.22)
        light, dark = ((246, 240, 228), (40, 40, 52)) if i % 2 == 0 else ((210, 196, 170), (120, 100, 80))
        p.poly([m, l, tip], light, INK, 1.4)
        p.poly([m, rr, tip], dark, INK, 1.4)
    top = [ell_pt(cx, cy - thick * 0.9, rx, ry, a, 0.24) for a in np.linspace(0, 2 * math.pi, 60, endpoint=False)]
    side = [ell_pt(cx, cy, rx, ry, a, 0.24) for a in np.linspace(0, math.pi, 30)]
    p.poly(side + [ell_pt(cx, cy - thick * 0.9, rx, ry, a, 0.24) for a in np.linspace(math.pi, 0, 30)], (20, 20, 26), INK, 2.0)
    p.poly(top, (150, 84, 40), INK, 2.0)                                                         # the dais
    p.poly([ell_pt(cx, cy - thick * 0.9, rx, ry, a, 0.12) for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)],
           (60, 40, 30), INK, 1.6)
    mx, my = ell_pt(cx, cy - thick * 0.9, rx, ry, 0, 0)
    p.ell(mx + rx * 0.02, my, rx * 0.05, ry * 0.05, (214, 178, 96), None)                         # the crescent moon
    p.ell(mx + rx * 0.035, my - ry * 0.01, rx * 0.045, ry * 0.045, (60, 40, 30), None)


# ------------------------------------------------------------------------------------------------ shot 1: Claudia
S1 = dict(cx=540, cy=1750, rx=1000, ry=420, s=1.25)
S1_SEATS = [math.radians(a) for a in range(-90 + 9, 270, 18)]       # 20 places; she stands in the gap at the top


def shot_claudia(img, t):
    cam = claudia_cam(t)
    wall(img, cam, -300, 1380, -200, 1400, seed=3, panel_w=290, lamps=[(170, 560), (910, 560)])
    rim_y = S1['cy'] - S1['ry']
    s = S1['s']
    neck = rim_y - STAND_Y * s - 14
    for a in (math.radians(-90 - 18), math.radians(-90 + 18)):
        x, y = ell_pt(S1['cx'], S1['cy'], S1['rx'] * 1.04, S1['ry'] * 1.04, a)
        chair_back(img, cam, x, y - TABLE_Y * s * 0.95, s * 0.95)
    sp = dict(C.CLAUDIA)
    sp.update(claudia_state(t))
    j = seated_pose(sp, 'clasped')
    person(img, cam, 540 + idle_x('claudia', t), neck, s, 'claudia', sp, j, t)
    round_table(img, cam, S1['cx'], S1['cy'], S1['rx'], S1['ry'], S1_SEATS)


def claudia_cam(t):
    """A slow push in (eased) that keeps her face where it is on screen (about y 640)."""
    z = 1.0 + 0.18 * ease((t - 0.2) / 6.0)
    face = S1['cy'] - S1['ry'] - STAND_Y * S1['s'] - 14 - 140 * S1['s']
    return B.Cam(z, 540, face + (960 - 640) / z)


def claudia_state(t):
    sh = filmkit.shifts(t, seed=11, amount=1.0)
    out = dict(mouth=talking_mouth('claudia', t), look=0.35, blink=F.blinking(t, BLINKS['claudia']),
               head_dx=4 * sh, head_dy=10 + 2 * abs(sh))
    lean = ease((t - (L1 + 5.5)) / 0.6)                # on "traitor?" she leans in a touch (eased)
    out['head_dy'] += 6 * lean
    return out


# ------------------------------------------------------------------------------------------------ shot 2: Trump
S2 = dict(x=540, neck=900, s=1.6)


def jab(t):
    """The slate jabbed up on each "because": up fast (0.12 s), back down eased (0.4 s)."""
    v = 0.0
    for tj in JABS:
        d = t - (tj - 0.06)
        if 0 <= d < 0.12:
            v = max(v, ease(d / 0.12))
        elif 0.12 <= d < 0.52:
            v = max(v, 1 - ease((d - 0.12) / 0.4))
    return 34 * v


def trump_state(t):
    sh = filmkit.shifts(t, seed=21, amount=1.0)
    out = dict(mouth=talking_mouth('trump', t), look=-0.35, blink=F.blinking(t, BLINKS['trump']),
               head_dx=5 * sh, head_dy=16 - 4, frown=1.0)
    if SEARCH[0] <= t < SEARCH[1]:                     # the stall: eyes up and away, searching for a reason
        out.update(look=0.7, gaze_dy=-3.0, frown=0.2, brow_raise=4)
    if t >= SNEER[0]:                                  # "looking at him": eyes across at Zelensky (snap), the sneer
        out.update(look=-0.95, turn=-0.25 * ease((t - SNEER[0]) / 0.5), frown=1.4)
        if out['mouth'] == 'rest':
            out['sneer'] = True
    return out


def shot_trump(img, t, close=False):
    cam = B.Cam(1.0, 540, 960) if not close else B.Cam(1.45, 540, 700)
    wall(img, cam, -200, 1280, -300, 1500, seed=7, panel_w=320, lamps=[(120, 560), (960, 560)])
    s = S2['s']
    chair_back(img, cam, S2['x'], S2['neck'] + 26 * s, s * 0.98)
    sp = dict(C.TRUMP)
    sp.update(trump_state(t))
    lift = jab(t)
    j = seated_pose(sp, 'slate', lift=lift)
    by = 236 + 40 - lift
    j['props'] = [lambda p, j2: C.draw_slate(img, p, 0, by, SLATE_W, 'ZELENSKY', seed=2, stand=True),
                  lambda p, j2: [B.gesture_hand(p, j2['el' + sd], j2['wr' + sd], 'fist', sp['skin']) for sd in 'LR']]
    x = S2['x'] + idle_x('trump', t)
    person(img, cam, x, S2['neck'], s, 'trump', sp, j, t)
    L = B.Local(cam, S2['x'], S2['neck'], s)
    p = B.Pen(img, L)
    C.table_far(img, p, -500, 500, TABLE_Y, seed=1)
    C.plate(p, 0, TABLE_Y + 140)
    C.goblet(p, 250, TABLE_Y + 60)


# ------------------------------------------------------------------------------------------------ shot 3: the arc
S3 = dict(cx=540, cy=1730, rx=1000, ry=500)
S3_SEATS = [math.radians(a) for a in range(-90 + 9, 270, 18)]       # the same 20 places
P_SEAT, Z_SEAT = math.radians(-90 - 20), math.radians(-90 + 20)     # a quarter of the table (Sam): one at each end,
EMPTY = [math.radians(-90)]                                         # one empty place between (Sam: too many chairs)


def seat_place(a):
    """Where a player sits at seat angle a in shot 3: (x, neck y, scale), smaller the further back."""
    x, y = ell_pt(S3['cx'], S3['cy'], S3['rx'], S3['ry'], a, 1.06)
    rim = ell_pt(S3['cx'], S3['cy'], S3['rx'], S3['ry'], a, 1.0)[1]
    s = 1.05 * (rim - 560) / (ell_pt(S3['cx'], S3['cy'], S3['rx'], S3['ry'], P_SEAT)[1] - 560)
    return x, rim - TABLE_Y * s, s


def putin_state(t):
    sh = filmkit.shifts(t, seed=31, amount=1.0)
    return dict(mouth='rest', smirk=1.0, lid=0.48, squint=0.4, look=0.25, turn=0.28, blink=F.blinking(t, BLINKS['putin']),
                head_dx=3 * sh, head_dy=10)


def zelensky_strength(t):
    return keyed(t, Z_SINK)


def shot_arc(img, t):
    cam = B.Cam(1.0, 540, 960)
    wall(img, cam, -200, 1280, -300, 1180, seed=13, panel_w=300, lamps=[(120, 470), (540, 430), (960, 470)])
    for a in sorted(EMPTY, key=lambda a: math.sin(a)):                                           # far ones first
        x, y, s = seat_place(a)
        chair_back(img, cam, x, y + 26 * s, s * 0.98)
    drawn = []
    for who, a in sorted((('putin', P_SEAT), ('zelensky', Z_SEAT)), key=lambda w: math.sin(w[1])):
        x, y, s = seat_place(a)
        chair_back(img, cam, x, y + 26 * s, s * 0.98)
        sp = dict(SP[who])
        if who == 'putin':
            sp.update(putin_state(t))
            j = seated_pose(sp, 'folded')
        else:
            k = zelensky_strength(t)
            j = seated_pose(sp, 'head', strength=k)
            sp.update(down=j['_down'], blink=True, turn=-0.2, mouth=talking_mouth('zelensky', t))
        x += idle_x(who, t) * s
        j2 = person(img, cam, x, y, s, who, sp, j, t)
        drawn.append((who, x, y, s, sp, j, j2))
    round_table(img, cam, S3['cx'], S3['cy'], S3['rx'], S3['ry'], S3_SEATS)
    for who, x, y, s, sp, j, j2 in drawn:
        arms_over_table(img, cam, x, y, s, who, sp, j, j2)
        L = B.Local(cam, x, y, s)
        p = B.Pen(img, L)
        towards = 1 if who == 'putin' else -1          # their things sit on the table in front of them
        if who == 'putin':
            C.draw_slate(img, p, 130 * towards, TABLE_Y + 96, SLATE_W, 'ЗЕЛЕНСКИЙ', cyrillic=True, seed=4)
        else:
            C.draw_slate(img, p, 130 * towards, TABLE_Y + 96, SLATE_W, '', face_up=False)
        C.goblet(p, -105 * towards, TABLE_Y + 70)     # by their outer hand, kept in frame (Sam: each has one)


# ------------------------------------------------------------------------------------------------ idle life
BLINKS = {
    'claudia': [b for b in F.blinks(5, 0.4, 6.5, talking=True)],
    'trump': [b for b in F.blinks(9, 6.8, SNEER[0] - 0.3, talking=True)],          # none on the sneer
    'putin': F.blinks(17, 20.6, DUR, per_min=(6, 9)),                              # the slow, reptile blink
}


def idle_x(who, t):
    """A held position with a small quick weight shift now and then (never a sway)."""
    return 6 * filmkit.shifts(t, seed={'claudia': 41, 'trump': 42, 'putin': 43, 'zelensky': 44}[who], amount=1.0)


# ------------------------------------------------------------------------------------------------ the film
def picture(t):
    """The frame WITHOUT captions or Hook Text (those go on last, so wording notes never re-render a picture)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    img = B.canvas((24, 16, 12))
    s = shot_of(t)
    if s == 'claudia':
        shot_claudia(img, t)
    elif s == 'trump':
        shot_trump(img, t)
    elif s == 'trump_close':
        shot_trump(img, t, close=True)
    else:
        shot_arc(img, t)
    return img


def caption_at(t):
    for a, b, txt in CAPS:
        if a <= t < b:
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


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)     # no added room tone (Sam, 17 Oct: it was heard as static)
    for ln in LINES:
        s = int(ln['start'] * SR)
        seg = ln['_voice'][:max(0, n - s)]
        voice[s:s + len(seg)] += seg
    mix = voice + rest
    end = int(BLACK_AT * SR)
    mix, g = MA.master(mix, end)                                 # -16 LUFS, levelled gently, never squashed
    voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


def checks():
    """Plan checks: seconds. Raises on the first batch of faults; prints the subtitles to proofread."""
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    faults = []
    for who, wins in WINDOWS.items():
        faults += E.check_mouths(TRACK[who], wins)
    for a, b, txt in CAPS:
        ln = max((l for l in LINES if l['start'] <= a), key=lambda l: l['start'])
        first = min(x for x, y in WINDOWS[ln['who']] if y > a - 0.15)
        if a < first - 0.02:
            faults.append(f'subtitle "{txt}" at {a:.2f} s comes up before the voice ({first:.2f} s)')
    _, voice, rest = soundtrack(stems=True)
    allw = [w for ws in WINDOWS.values() for w in ws]
    faults += filmkit.voice_balance(voice, rest, SR, allw)
    n = int((DUR + 0.3) * SR)
    raw = np.zeros(n)
    for ln in LINES:
        s = int(ln['start'] * SR)
        raw[s:s + len(ln['_voice'])] += ln['_voice'][:n - s]
    faults += MA.limit_check(raw, int(BLACK_AT * SR))
    mix, voice, rest = soundtrack(stems=True)
    for q in filmkit.sound_questions({'voice': voice, 'background': rest, 'mix': mix}, SR,
                                     cuts=[a for _, a, _ in SHOTS[1:]], end=BLACK_AT):
        print('QUESTION FOR SAM:', q)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


def alone(who):
    """That person alone, as drawn in the film at time t (for the audit)."""
    def draw(t):
        lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
        s = shot_of(t)
        if who == 'claudia':
            cam = claudia_cam(t)
            sp = dict(C.CLAUDIA)
            sp.update(claudia_state(t))
            rim_y = S1['cy'] - S1['ry']
            person(lay, cam, 540 + idle_x('claudia', t), rim_y - STAND_Y * S1['s'] - 14, S1['s'], 'claudia', sp,
                   seated_pose(sp, 'clasped'), t)
        elif who == 'trump':
            cam = B.Cam(1.0, 540, 960) if s == 'trump' else B.Cam(1.45, 540, 700)
            sp = dict(C.TRUMP)
            sp.update(trump_state(t))
            person(lay, cam, S2['x'] + idle_x('trump', t), S2['neck'], S2['s'], 'trump', sp,
                   seated_pose(sp, 'slate', lift=jab(t)), t)
        else:
            cam = B.Cam(1.0, 540, 960)
            a = P_SEAT if who == 'putin' else Z_SEAT
            x, y, sc = seat_place(a)
            sp = dict(SP[who])
            if who == 'putin':
                sp.update(putin_state(t))
                j = seated_pose(sp, 'folded')
            else:
                j = seated_pose(sp, 'head', strength=zelensky_strength(t))
                sp.update(down=j['_down'], blink=True, turn=-0.2, mouth=talking_mouth('zelensky', t))
            person(lay, cam, x + idle_x(who, t) * sc, y, sc, who, sp, j, t, blood=False)
        return lay
    return draw


def audits():
    """The general audit: each person alone over every frame they are on screen. Returns faults."""
    actors = {}
    on = {'claudia': ('claudia',), 'trump': ('trump', 'trump_close'), 'putin': ('arc',), 'zelensky': ('arc',)}
    for who, shots in on.items():
        for shot, a, b in SHOTS:
            if shot in shots:
                ts = [i / FPS for i in range(int(math.ceil(a * FPS)), int(b * FPS))]
                actors[f'{who} [{shot}]'] = (ts, alone(who))
    return filmkit.silhouette_audit(actors, fps=FPS, still_ok=())


# ------------------------------------------------------------------------------------------------ the cast sheet
def draw_player(img, cam, x, y, s, who, sp_extra=None, kind='folded', strength=4, t=0.0, slate=None):
    """One player at the table (cast sheet): the person, their slate, their goblet, the table edge."""
    sp = dict(SP[who])
    sp.update(sp_extra or {})
    j = seated_pose(sp, kind, strength)
    if who == 'zelensky' and kind == 'head':
        sp.update(down=j['_down'], blink=True)
    if kind == 'slate':
        j['props'] = [lambda p, j2: C.draw_slate(img, p, 0, 236 + 40, SLATE_W, 'ZELENSKY', seed=2, stand=True),
                      lambda p, j2: [B.gesture_hand(p, j2['el' + sd], j2['wr' + sd], 'fist', sp['skin']) for sd in 'LR']]
    j2 = person(img, cam, x, y, s, who, sp, j, t)
    if kind != 'clasped':
        p = B.Pen(img, B.Local(cam, x, y, s))
        C.table_far(img, p, -420, 420, TABLE_Y, seed=sum(map(ord, who)) % 7)
        C.plate(p, 0, TABLE_Y + 140)
        C.goblet(p, 250, TABLE_Y + 60)
        arms_over_table(img, cam, x, y, s, who, sp, j, j2)
        if slate:
            C.draw_slate(img, p, slate[0], TABLE_Y + 50, SLATE_W * 0.9, slate[1], cyrillic=slate[2], seed=slate[3],
                         face_up=slate[4])
    return j


def panel(draw, w=540, h=700, z=2.6, cy=820, bg=(66, 40, 28)):
    img = B.canvas(bg)
    cam = B.Cam(z, 540, cy)
    draw(img, cam)
    return img.crop((0, 1920 // 2 - int(h * 1080 / w) // 2, 1080, 1920 // 2 + int(h * 1080 / w) // 2)).resize((w, h), Image.LANCZOS)


def label(img, x, y, txt, size=30):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), size)
    d.text((x, y), txt, font=f, fill=(250, 250, 250), stroke_width=3, stroke_fill=(20, 20, 20))


def cast_sheet(out):
    """Every view each person appears in: Claudia standing (shot 1); Trump holding up his slate (shot 2), close and
    sneering; Putin with the blood and his Cyrillic vote (shot 3); Zelensky's head in his hands at strengths 1-6 for
    Sam to pick from (the film's key reaction), and his face before it."""
    B.SS = 1
    sheet = Image.new('RGB', (2160, 700 * 2 + 520), (30, 24, 22))
    row = [
        ('Claudia (shot 1)', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'claudia', kind='clasped')),
        ('Trump (shot 2)', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'trump', kind='slate')),
        ('Putin (shot 3)', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'putin', {'smirk': 0.6}, kind='folded',
                                                       slate=(-170, 'ЗЕЛЕНСКИЙ', True, 4, True))),
        ('Zelensky (shot 3), strength 4', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'zelensky', kind='head',
                                                                      strength=4, slate=(170, '', False, 0, False))),
    ]
    for i, (name, fn) in enumerate(row):
        sheet.paste(panel(fn, z=1.9, cy=960), (540 * i, 0))
        label(sheet, 540 * i + 16, 12, name)
    close = [
        ('Claudia, close', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'claudia', kind='clasped')),
        ('Trump: "looking at him"', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'trump', {'sneer': True, 'look': 0.8},
                                                                kind='slate')),
        ('Putin, close', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'putin', {'smirk': 0.6}, kind='folded')),
        ('Zelensky, face', lambda im, cam: draw_player(im, cam, 540, 900, 1.0, 'zelensky', kind='folded')),
    ]
    for i, (name, fn) in enumerate(close):
        sheet.paste(panel(fn, z=3.4, cy=770), (540 * i, 700))
        label(sheet, 540 * i + 16, 712, name)
    for k in range(1, 7):
        im = panel(lambda img, cam, k=k: draw_player(img, cam, 540, 900, 1.0, 'zelensky', kind='head', strength=k),
                   w=360, h=520, z=2.4, cy=860)
        sheet.paste(im, (360 * (k - 1), 1400))
        label(sheet, 360 * (k - 1) + 14, 1410, f'Zelensky {k}', 26)
    sheet.save(out, quality=90)


def stills_sheet(out, times, w=360):
    """Several stills side by side (with their captions), labelled with the time and shot, on one sheet."""
    B.SS = 1
    h = w * 16 // 9
    sheet = Image.new('RGB', (w * len(times), h + 40), (20, 20, 20))
    for i, t in enumerate(times):
        im = frame_image(t).convert('RGB').resize((w, h), Image.LANCZOS)
        sheet.paste(im, (w * i, 40))
        label(sheet, w * i + 10, 4, f'{t:.1f}s {shot_of(t)}', 24)
    sheet.save(out, quality=88)


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        cast_sheet(a[1])
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'sheet':
        stills_sheet(a[1], [float(x) for x in a[2:]])
    elif a[0] == 'times':
        for s, t0, t1 in SHOTS:
            print(f'{s:12s} {t0:5.2f}-{t1:5.2f}')
        for t0, t1, c in CAPS:
            print(f'  {t0:5.2f}-{t1:5.2f} {c}')
    elif a[0] == 'check':
        B.SS = 1
        checks()
        f = audits()
        print('\n'.join(['AUDIT: ' + x for x in f]) or 'audit: clean')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else ())


F.guard(B)   # every arm drawn is measured against the rig; a wrong one stops the render
import limbs                     # noqa: E402
limbs.install(B)                 # natural arms and legs (Cry Minister)

if __name__ == '__main__':
    main()
