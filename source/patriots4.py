#!/usr/bin/env python3
"""Patriots 4 (TikTok satire): the Celebrity Traitors winner's table. Romesh and Bash name their refugee charities;
then Claudia turns to the fourth winner nobody had seen: the Patriot. "Errrrr...". "Traitors."

From source/satire_template.py (guides/satire.md). The cast: patriots4_cast.py; the room, painted once all round with
the camera turning on the spot over the coins: patriots4_room.py; the plan in metres: patriots4_plan.py.

    python3 source/patriots4.py cast OUT.jpg               the cast sheet
    python3 source/patriots4.py stills OUT_DIR T [T ...]   stills at these times (seconds)
    python3 source/patriots4.py sheet OUT.jpg [T ...]      one labelled sheet, a still per shot (rule 48)
    python3 source/patriots4.py check                      every check and the audit (also run by preflight.py)
    python3 source/patriots4.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1] [--nostamp]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import mossad as M               # noqa: E402,F401
import figure as F               # noqa: E402
import mouths                    # noqa: E402
import mossad_audio as MA        # noqa: E402
import peepee as PP              # noqa: E402
import filmkit                   # noqa: E402
import film_engine as E          # noqa: E402
from satire_style import install_circle_hands   # noqa: E402
from ed import INK               # noqa: E402
import patriots4_cast as PC      # noqa: E402
import patriots4_room as RM      # noqa: E402
import patriots4_plan as PL      # noqa: E402
import patriots4_wide as WV      # noqa: E402
import posegallery as PG         # noqa: E402
import views as V                # noqa: E402

mouths.install(B)
install_circle_hands(B)
FPS, SR = 12, MA.SR
MA.LOW_BIRDS.add('patriots4-claudia-1')   # animatic 3 note 33: her birds at 3-4 kHz (below debird's 4 kHz floor)

# =============================================== STORY =============================================================
NOTES = os.path.join(os.path.dirname(HERE), 'notes', 'patriots-4.md')
NAME = 'patriots4'
TITLE = ()                                        # no title (Sam, 15 Oct)
TITLE_AT = dict(cap=116, top=310)
CAST = PC.CAST
WHO = ('claudia', 'bash', 'romesh', 'patriot')
LOOKS_AT = {'claudia': 'bash', 'bash': 'claudia', 'romesh': 'claudia', 'patriot': 'claudia'}
ERR_USE, ERR_FADE = 18.0, 4.0                     # Sam: 15-20 s of the 40 s "Errrr", faded gently out
LINES = [   # start = where the recording's file starts (its speech starts later: see the notes' table)
    dict(n=1, who='claudia', text='Romesh and Bash, remind us who you did this for?', audio='patriots4-claudia-1',
         start=0.0, chunks=['Romesh and Bash,', 'remind us', 'who you did this for?'],
         parts=['Romesh', 'and Bash,', 'remind us', 'who you', 'did this for?']),   # slow: a pause after each
    dict(n=2, who='bash', text='I did this for a wonderful organisation, they are called Choose Love. They help displaced '
         'people all over the world including queer refugees.', audio='patriots4-bash', start=6.69,
         chunks=['I did this for a wonderful organisation,', 'they are called Choose Love.',
                 'They help displaced people', 'all over the world including', 'queer refugees.'],
         parts=['I did this for a wonderful organisation, they are called Choose Love. They help displaced people all '
                'over the world including', 'queer refugees.']),   # one part per stretch of speech (after a pause)
    dict(n=3, who='romesh', text="I'm doing this for a cause that is very dear to my heart, it's the Refugee Council.",
         audio='patriots4-romesh', start=15.47,
         chunks=["I'm doing this for a cause", 'that is very dear to my heart,', "it's the Refugee Council."]),
    dict(n=4, who='claudia', text='And what about you?', audio='patriots4-claudia-2', start=22.2,
         chunks=['And what about you?'], parts=['And what', 'about', 'you?']),
    dict(n=5, who='patriot', text='Errrrrrrrrrrrrrrrrrrrrrr...', audio='patriots4-patriot-err', start=26.43,
         cut=0.37 + ERR_USE, chunks=['Errrrrrrrrrrrrrrrrrrrrrr...']),   # Sam: one fixed line (fewer r's: fits 700 px)
    dict(n=6, who='patriot', text='Traitors.', audio='patriots4-patriot-traitors', start=45.71, chunks=['Traitors.'], hold=1.1),   # held into shot 13 (readable)
]
# (camera, start, end): the camera turns on the spot (heading: degrees round the clock from Claudia, 12 o'clock)
SHOTS = [('claudia', 0.0, 6.9), ('bash', 6.9, 15.8), ('romesh', 15.8, 21.8), ('claudia 2', 21.8, 25.6),
         ('patriot', 25.6, 29.3), ('claudia close', 29.3, 32.3), ('bash close', 32.3, 35.3),
         ('patriot close', 35.3, 38.3), ('his view', 38.3, 41.3), ('claudia close 2', 41.3, 44.8),
         ('patriot 2', 44.8, 46.8), ('traitors', 46.8, 48.2),
         ('reaction', 48.2, 50.2)]   # Sam, 1 Nov: Romesh's and Bash's reaction (his yes to my proposal)
A = RM.ANGLES
PANS = {}   # Sam, 1 Nov (animatic 1 note 1): the swings read as the table spinning: plain jump cuts instead
STILL = {   # shot: (heading, zoom, whose face the camera centres, or None for the room's middle)
    'claudia': (0.0, 1.0, None), 'bash': (270.0, 1.0, None), 'romesh': (180.0, 1.0, None),
    'claudia 2': (0.0, 1.0, None), 'patriot': (90.0, 1.0, None), 'claudia close': (0.0, 1.75, 'claudia'), 'claudia close 2': (0.0, 1.75, 'claudia'),
    'bash close': (270.0, 1.75, 'bash'), 'patriot close': (90.0, 1.75, 'patriot'), 'his view': (212.0, 1.0, None),
    'patriot 2': (90.0, 1.2, 'patriot'), 'traitors': (90.0, 1.15, 'patriot'), 'reaction': (212.0, 1.0, None),
}
CHEAT = {   # a film cheat for shots 9 and 13: Romesh and Bash stand 90 degrees apart, too far for one frame with faces
    'his view': {'romesh': 200.0, 'bash': 224.0},   # big enough for the eye slide, so they are moved closer for it.
    'reaction': {'romesh': 200.0, 'bash': 224.0},   # Removed for note 26, then the wide view built (patriots4_wide.py);
}                                                   # Sam, 1 Nov (note 29): back to this cheat
WIDE = ()   # shots drawn with patriots4_wide's real camera (none now: note 29; it was 'his view' and 'reaction')
T_ASK_EYES = 24.78           # "you?": Claudia's eyes go to her left (the Patriot, off frame)
T_WIDEN = 26.4               # the Patriot's eyes widen (stare 1), then grow slowly to 4 (Sam, 1 Nov)
T_STARE4 = 44.8
T_SLIDE = 36.3               # his eyes slide sideways to Romesh (head still)
T_MEET = 39.3                # Romesh and Bash slide their eyes to each other
T_NARROW = 46.85             # narrowed, accusing; both arms out: "Traitors."
T_POINT = 46.95
T_WONDERFUL = (8.5, 9.2)     # Bash's eyes close on "wonderful"
T_EACH = 48.6                # shot 13: their eyes slide to each other, and hold (no dropped mouths: animatic 1 note 2)
PLAN = dict(CEIL=PL.CEIL, ROOMS=PL.ROOMS, OPENINGS=PL.OPENINGS, LOOKS=PL.LOOKS, THINGS=PL.THINGS, PEOPLE=PL.PEOPLE,
            CAMS=PL.CAMS, GROUPS=PL.GROUPS, SHOT_MARKS=PL.SHOT_MARKS)
SHOT_CAMS = {'claudia': 'claudia', 'bash': 'bash', 'romesh': 'romesh', 'claudia 2': 'claudia', 'patriot': 'patriot',
             'claudia close': 'claudia close', 'bash close': 'bash close', 'patriot close': 'patriot close',
             'his view': 'his view', 'claudia close 2': 'claudia close', 'patriot 2': 'patriot', 'traitors': 'patriot',
             'reaction': 'his view'}
BENCHMARK = [dict(place="winner's room", refs=['references/patriots-4/01-claudia-winners-table-front.jpg', 'references/patriots-4/03-three-at-winners-table-wide.jpg',
                                                 'references/patriots-4/12-room-from-above.jpg'], at=1.0,
                  items=[('the pointed wooden arch the banished leave by', 'patriots4_room.arch'),
                         ('diamond lattice over red-lit panes either side and above', 'patriots4_room.lattice'),
                         ('panelled double doors in the passage beyond', 'patriots4_room.arch'),
                         ('tall dark wooden panelled walls', 'patriots4_room.panels'),
                         ('fire baskets on iron stands either side of the arch', 'patriots4_room.fire_basket'),
                         ('torches in iron cages, candles', 'patriots4_room.torch, candles'),
                         ('a round red-brown table with a cream inlaid ring and light rim', 'patriots4_room.table_top'),
                         ('a pyramid of big gold coins on it', 'patriots4_room.coin_pile'),
                         ('the Round Table hall through the opening behind Romesh', 'patriots4_room.round_table_room')])]
SHOT_CAST = {'claudia': ['claudia'], 'bash': ['bash'], 'romesh': ['romesh'], 'claudia 2': ['claudia'],
             'patriot': ['patriot'], 'claudia close': ['claudia'], 'bash close': ['bash'], 'patriot close': ['patriot'],
             'his view': ['romesh', 'bash'], 'claudia close 2': ['claudia'], 'patriot 2': ['patriot'],
             'traitors': ['patriot'], 'reaction': ['romesh', 'bash']}
THREE_QUARTER_OK = []
HOOK = ('Celebrity Traitors winners reveal their charities', {'y': 330})   # Sam: over the arch, shot 1
KEEP_CLEAR = []
PROP_SIZES = []
OUTFIT = {}
HEIGHTS = PC.HEIGHTS
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
ALLOWED_CONTACTS = [(f'{w}.hand*', "winner's table", 0.0, 50.2, 'hands resting on the table edge (refs 03, 09)')
                    for w in ('claudia', 'bash', 'romesh')]
ALLOWED_POPS = []
SET_EXCLUDE = [('fire bowl', 'painted on the panorama, out of reach'), ('round table', 'far off in the hall, painted')]
TOUCHES, FREE_MOVES, SOUND_SOURCES = [], [], {}
EFFECTS = []
JOKE_PROPS = []
LOOKS_OK = []
HANDS_OK = []
LINE_OK = [('patriot', 'line weight', x, y) for x, y in ((485, 182), (583, 183), (495, 210), (574, 210), (321, 616),
                                                         (743, 615), (767, 615))]     # as Patriots 3 (same drawing)
LINE_OK_WHY = {'patriot': "his black balaclava and jacket count as ink, so the check's 'house' weight is the jacket: "
                          "his real outlines read as thin (as Patriots 3)"}
# ====================================================================================================================

S = 1.1                                           # people's drawing scale at zoom 1 (patriots4_room: about 1.5 m away)
DUR = SHOTS[-1][2]
BLACK_AT = DUR
for ln in LINES:
    v = MA.line(ln['audio'])
    if ln.get('cut'):
        n = int(ln['cut'] * SR)
        v = v[:n].copy()
        f = int(ERR_FADE * SR)
        v[-f:] *= np.linspace(1.0, 0.0, f) ** 1.5             # faded gently out (Sam)
    ln['_voice'] = v
    ln['_stretches'] = MA.pauses(v, 0.12)
    ln['_speech'] = (ln['start'] + ln['_stretches'][0][0], ln['start'] + ln['_stretches'][-1][1])
    ln['end'] = ln['_speech'][1]
LINE = {ln['n']: ln for ln in LINES}


def _track(ln):
    """The mouth shapes for a line; a line given in `parts` is tracked one part per stretch of speech (mouths.track
    lets a long first stretch take every word, leaving the words after a pause with a shut mouth)."""
    if not ln.get('parts'):
        return mouths.track(ln['text'], ln['_stretches'])
    st = ln['_stretches']
    return [x for part, s in zip(ln['parts'], st) for x in mouths.track(part, [s])]


TRACK = {w: [(a + ln['start'], b + ln['start'], sh) for ln in LINES if ln['who'] == w and ln['n'] != 5
             for a, b, sh in _track(ln)] for w in WHO}
ERR = LINE[5]['_speech']
KEY_FACES = [(T_WONDERFUL[0] - 0.3, T_WONDERFUL[1]), (T_ASK_EYES - 0.3, T_ASK_EYES + 0.6),
             (T_SLIDE - 0.4, T_SLIDE + 0.8), (T_MEET - 0.4, T_MEET + 1.4), (T_NARROW - 0.3, DUR)]
BLINKS = {w: [b for b in F.blinks(7 + i * 5, 0.5, DUR, talking=True) if not any(a <= b <= c for a, c in KEY_FACES)]
          for i, w in enumerate(WHO)}
BLINKS['patriot'] = [b for b in BLINKS['patriot'] if b < T_WIDEN - 0.5]   # the stare does not blink (the joke)
BLINKS['claudia'] = [b for b in BLINKS['claudia'] if not 29.3 <= b < 32.3] + [42.0, 43.55]   # shot 6 stares; 10 blinks
BLINKS['bash'] = [b for b in BLINKS['bash'] if not 32.3 <= b < 35.3] + [33.0, 34.3]          # shot 7: staring, blinking


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def chunk_times(ln):
    """Each subtitle chunk on its first word (Sam, 16 Oct): the words' syllables laid over the recording's own
    stretches of speech, in order (so a slow line with pauses keeps its pauses)."""
    chunks = ln['chunks']
    syl = [max(1, sum(mouths._syllables(w) for w in c.split())) for c in chunks]
    st = [(ln['start'] + a, ln['start'] + b) for a, b in ln['_stretches']]
    total = sum(b - a for a, b in st)
    out, acc = [], 0
    for c, n in zip(chunks, syl):
        k = acc / float(sum(syl)) * total                 # speech time before this chunk's first syllable
        for a, b in st:
            if k <= b - a:
                out.append((a + k + 0.1, c))
                break
            k -= b - a
        acc += n
    return out


CHUNKS = [(t, c, ln) for ln in LINES for t, c in chunk_times(ln)]


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def neck_y(who):
    """Feet on the floor line: the neck's world y for this person's real height."""
    return RM.FLOOR_Y - 928 * PC.P3.scale_for(CAST[who], S)


def face_y(who):
    return neck_y(who) - 150 * PC.P3.scale_for(CAST[who], S)


LOWER = 230.0        # frame pixels the camera looks lower in shots 9 and 13 (the beams were the top 200)
NEAR_Z, NEAR_CY = 1.35, 1050.0   # Sam, 1 Nov notes 8-9: every table shot with the camera in at the table's edge; the
                                # table's extra scale puts its near rim at the frame's foot (patriots4_room.near_for)


def pancam(t):
    s = shot_of(t)
    if s in PANS:
        h0, h1, a, b = PANS[s]
        u = ease((t - a) / (b - a))
        pc = RM.PanCam(h0 + (h1 - h0) * u, NEAR_Z, NEAR_CY)
        pc.near = RM.near_for(pc)
        return pc
    h, z, who = STILL[s]
    cy = 960.0 if who is None else face_y(who) + 200 / z
    if s in ('claudia', 'bash', 'romesh', 'claudia 2', 'patriot'):   # Sam, 1 Nov notes 8-9: at the table's edge
        z = NEAR_Z
        cy = RM.rim_cy(z)                         # animatic 2 note 25: the one table size; its near rim at the foot
    if s in ('patriot 2', 'traitors'):            # animatic 1 note 3: out a little, Bash's and Romesh's backs in both
        z = 1.15
        cy = RM.rim_cy(z)
    if s in ('his view', 'reaction'):             # the cheat (note 29): a little wider, so both fit, hands and all;
        z = 1.1                                   # the one table size (note 25)
        cy = RM.rim_cy(z) + LOWER / z             # animatic 3 note 31: the camera down, the beamed roof out of the top
    pc = RM.PanCam(h, z, cy)
    pc.near = RM.near_for(pc)
    return pc


def cam_for(t):
    return pancam(t).cam


_pancam = pancam


def pancam(t):                                    # noqa: F811  (the camera, told which shot it is in)
    pc = _pancam(t)
    pc.shot = shot_of(t)
    return pc


# ------------------------------------------------------------------------------------------------ acting
def stare(t):
    """The Patriot's stare strength: 1 when his eyes widen, growing slowly to 4 (Sam, 1 Nov)."""
    if t < T_WIDEN:
        return None
    return 1.0 + 3.0 * ease((t - T_WIDEN) / (T_STARE4 - T_WIDEN))


def look(who, t):
    """Where each one's pupils point (-1 our left .. 1 our right), from the plan's clock: see the notes' eyeline list."""
    if who == 'claudia':
        if t < LINE[2]['_speech'][0]:                     # shot 1: between them, a look per phrase (animatic 1 note 2)
            return -0.3 if claudia_asks(t) == 'romesh' else -0.75
        if t < LINE[3]['_speech'][0] - 0.3:
            return -0.7                                   # Bash
        if t < T_ASK_EYES:
            return -0.3                                   # Romesh, then back for "And what about you?"
        return 0.9                                        # her left: the Patriot
    if who == 'bash':
        if t < 25.0:
            return 0.6                                    # Claudia (his left, our right)
        if t < T_MEET:
            return -0.3                                   # the Patriot (straight across at 3 o'clock; shot 9: his
        if t < 46.0:                                      # shoulder in the bottom-left corner)
            return -0.9                                   # Romesh
        return -0.3 if t < T_EACH else -0.9              # back to the Patriot; then Romesh again (shot 13)
    if who == 'romesh':
        if t < 25.0:
            return -0.25                                  # Claudia, straight across (12 o'clock from his 6)
        if t < T_MEET:
            return -0.3                                   # the Patriot (his shoulder bottom-left in shot 9)
        if t < 46.0:
            return 0.9                                    # Bash
        return -0.3 if t < T_EACH else 0.9               # back to the Patriot; then Bash again (shot 13)
    if who == 'patriot':
        if t < T_SLIDE:
            return -0.9                                   # Claudia, who asked him (his right, our left)
        if t < 44.8:
            return 0.45                                   # sideways to Romesh, head still
        return 0.0                                        # ahead: the awkward silence, then "Traitors."
    return 0.0


def claudia_asks(t):
    """Shot 1: whom Claudia's eyes are on: Romesh, Bash, Romesh, Bash, Romesh, one per phrase of her question (each
    move a little before the phrase starts)."""
    ln = LINE[1]
    k = sum(1 for a, _ in ln['_stretches'][1:] if t >= ln['start'] + a - 0.15)
    return ('romesh', 'bash')[k % 2]


def looking_at(who, t):
    """Who each one is looking at (the eyeline check's target), matching look() above."""
    if who == 'claudia':
        if t < LINE[2]['_speech'][0]:
            return claudia_asks(t)
        return 'bash' if t < LINE[3]['_speech'][0] - 0.3 else 'romesh' if t < T_ASK_EYES else 'patriot'
    if who in ('bash', 'romesh'):
        other = 'romesh' if who == 'bash' else 'bash'
        if t < 25.0:
            return 'claudia'
        if t < T_MEET or 46.0 <= t < T_EACH:
            return 'patriot'
        return other
    return 'claudia' if t < T_SLIDE else 'romesh'


def mouth(who, t):
    if who == 'patriot' and ERR[0] <= t < ERR[1] - 1.2:
        return 'v:E'                                      # the "Errrr" held (the knit moves over it)
    shape = mouths.at(TRACK[who], t)
    return 'rest' if shape == 'rest' else 'v:' + shape


def state(who, t):
    """Everything about one person at time t: the pose (joints), look, mouth, blink, face. Logs their eyeline."""
    sp = dict(CAST[who])
    sp['mouth'] = mouth(who, t)
    sp['blink'] = F.blinking(t, BLINKS[who])
    sp['look'] = look(who, t)
    if who == 'claudia':
        sp['smile'] = 0.6 if t < T_ASK_EYES else 0.0
        j = PG.hands_on_table(sp)
    elif who == 'romesh':
        if LINE[3]['_speech'][0] - 0.2 <= t <= LINE[3]['_speech'][1] + 0.3:
            sp['frown'] = -0.015                          # sincere
        j = PG.hands_on_table(sp)
    elif who == 'bash':
        a, b = LINE[2]['_speech']
        if a - 0.2 <= t <= b + 0.4:
            sp['frown'] = -0.03                           # moved, excited: brows up in the middle
            sp['brow_up'] = 0.01
            j = PG.palms_together(sp)
            if T_WONDERFUL[0] <= t < T_WONDERFUL[1]:
                sp['blink'] = True                        # eyes shut on "wonderful"
        else:
            j = PG.hands_on_table(sp)
        if 32.3 <= t < 35.3:
            sp['wide'] = 0.3
    else:
        k = stare(t)
        if t >= T_NARROW:
            sp['brows'], sp['lid'] = 'fierce', 3            # the library's own narrowed eyes (Patriots 3's 'cross')
        elif k is not None:
            sp['stare'] = k                               # in the library's eye style (animatic 1 note 5)
            sp['brow_c_real'] = sp.get('brow_c', tuple(int(v * 0.8) for v in sp.get('hair_c', (60, 44, 34))))
            sp['brow_c'] = sp['skin']                     # the library's own brows hidden under the raised ones
        j = point_at_them(sp) if t >= T_POINT else V.standing(sp)
    j['bob'] = 0.0      # animatic 3 note 32: the breathing bob read as floating; they stand still
    return sp, j


def point_at_them(sp):
    """Shot 12: a real point (Sam, 1 Nov note 7: "more like pointing", as at the end of Power Crime Action): both arms
    thrust out straight from the shoulder, down towards the two shoulders in the frame's corners, a finger sticking
    out of each round hand along the arm; his right hand (our left) at Bash, his left (our right) at Romesh."""
    j = V.standing(sp)
    reach = (F.UPPER + F.FORE) * 0.98 + F.HAND['point'] - 4      # all but straight: no bend at the elbow
    for side, sg in (('L', -1), ('R', 1)):
        sx, sy, sz = j['sh' + side]
        d = (sg * 0.4, 0.5, 0.77)              # down and out at the two shoulders; drawn over the table (arms_mask)
        n = math.sqrt(sum(c * c for c in d))
        V.arm_to(j, side, (sx + d[0] / n * reach, sy + d[1] / n * reach, sz + d[2] / n * reach), 'down', 'point')
    return j


def install_point_finger(B):
    """The 'point' hand of Power Crime Action (Sam, 20 Oct; asked for again here): the plain circle with one short
    round-ended finger sticking out the way the forearm points, drawn first so the circle covers its root."""
    circle = B.gesture_hand

    def gesture_hand(p, el, wr, shape, skin, extra=None, t=0.0):
        if shape == 'point':
            dx, dy = wr[0] - el[0], wr[1] - el[1]
            n = math.hypot(dx, dy) or 1.0
            ux, uy = dx / n, dy / n
            cx, cy = wr[0] + ux * 12, wr[1] + uy * 12
            tip = (cx + ux * 62, cy + uy * 62)                     # a touch longer and thicker than Power Crime
            w = 10.5                                               # Action's, so it reads at this distance
            p.poly([(cx - uy * w, cy + ux * w), (tip[0] - uy * w, tip[1] + ux * w), (tip[0] + uy * w, tip[1] - ux * w),
                    (cx + uy * w, cy - ux * w)], skin, INK, 2.2)
            p.ell(tip[0], tip[1], w, w, skin, INK, 2.2)
            p.poly([(tip[0] - ux * 6 - uy * (w - 1.5), tip[1] - uy * 6 + ux * (w - 1.5)),
                    (tip[0] - ux * 6 + uy * (w - 1.5), tip[1] - uy * 6 - ux * (w - 1.5)),
                    (cx + uy * (w - 1.5), cy - ux * (w - 1.5)), (cx - uy * (w - 1.5), cy + ux * (w - 1.5))], skin, None)
        return circle(p, el, wr, shape, skin, extra, t)
    gesture_hand.point_finger = True
    B.gesture_hand = gesture_hand


import patriots3_cast  # noqa: E402,F401  (these two loaded now: on first use (the Round Table hall) they would
import traitors        # noqa: E402,F401   put the plain circle hands back)
install_point_finger(B)


# ------------------------------------------------------------------------------------------------ drawing
def angle(who, pc):
    return CHEAT.get(pc.shot, {}).get(who, A[who])


def place(who, pc):
    return pc.x(angle(who, pc)), neck_y(who)


def visible(who, pc):
    return pc.seen(angle(who, pc), 260)


def draw_wide(img, who, t):
    """Shots 9 and 13: Romesh or Bash standing at the table, seen from the Patriot's place (patriots4_wide)."""
    sp, j = state(who, t)
    breath = j.get('bob', 0.0)
    (x, y), s, s2, d = WV.body(who, HEIGHTS[CAST[who]['name']])
    j = WV.standing_hands(sp, j, s2, (x, y), WV.rim_y, who)
    j['bob'] = breath
    j2 = PC.person(img, WV.screen_cam(), x, y, s, sp, t, WV.YAW[who], j, 0)   # the face to the lens (rule 38)
    hy = (y + (j['bob'] - 150) * s2) * B.SS
    other = {'romesh': 'bash', 'bash': 'romesh'}[who]
    target = looking_at(who, t)
    tx = WV.body(other, 1.78)[0][0] if target == other else 150.0     # the Patriot: his shoulder, bottom left
    filmkit.eyeline(who, t, (x * B.SS, hy), (sp['look'], 0.0), (tx * B.SS, hy))
    j2['_at'] = (x, y + j['bob'] * s2, s2)
    return j2, sp


def draw_person(img, pc, who, t):
    if pc.shot in WIDE:
        return draw_wide(img, who, t)
    sp, j = state(who, t)
    x, y = place(who, pc)
    j2 = PC.person(img, pc.cam, x, y, S, sp, t, 0, j)
    hx, hy = pc.cam.P(x, y - 150 * PC.P3.scale_for(sp, S))
    filmkit.eyeline(who, t, (hx, hy), (sp['look'], 0.0),
                    (pc.cam.P(pc.x(angle(looking_at(who, t), pc)), y)[0], hy))
    return j2, sp


def arms_mask(pc, who, j2, sp):
    """Where this person's forearms and hands are on screen: they rest on the table top, so they are drawn again over
    it (the table hides everything else of them below its far edge)."""
    from PIL import ImageDraw as D
    m = Image.new('L', (B.W * B.SS, B.H * B.SS), 0)
    d = D.Draw(m)
    if '_at' in j2:                                # the wide view (shots 9, 13): drawn in frame pixels
        x, y, s2 = j2['_at']
        cam, z = WV.screen_cam(), B.SS
    else:
        s2 = PC.P3.scale_for(sp, S)
        x, y = place(who, pc)
        cam, z = pc.cam, pc.zoom * B.SS
    for side in 'LR':
        el, wr = j2['el' + side], j2['wr' + side]
        pts = [cam.P(x + u * s2, y + v * s2) for u, v in (el, wr)]   # already in drawing pixels (P carries SS:
        # fixed 1 Nov, the extra * SS put every hand over the table at twice its place in full-quality renders)
        dx, dy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        n = math.hypot(dx, dy) or 1.0
        hand = (pts[1][0] + dx / n * 12 * s2 * z, pts[1][1] + dy / n * 12 * s2 * z)   # the circle hand's own centre
        d.line([pts[0], pts[1]], fill=255, width=int(64 * s2 * z))
        r = 28 * s2 * z                    # the hand and its outline only (bigger showed a rim of sleeve: animatic 1)
        d.ellipse((hand[0] - r, hand[1] - r, hand[0] + r, hand[1] + r), fill=255)
        if j2.get('hand', {}).get(side) == 'point':              # the pointing finger too (shot 12)
            tip = (hand[0] + dx / n * 104 * s2 * z, hand[1] + dy / n * 104 * s2 * z)
            d.line([hand, tip], fill=255, width=int(30 * s2 * z))
    return m


def shoulder(img, who, x, y, s):
    """Someone's back and shoulder in a corner of the frame, close to the lens (over-the-shoulder shots)."""
    cam = B.Cam(1.0, 540, 960)
    cam.P = lambda a, b: (a * B.SS, b * B.SS)    # output pixels (fixed 1 Nov: at full quality, SS 2, they were misplaced)
    cam.S = lambda v: v * B.SS
    sp = dict(CAST[who], mouth='rest')
    PC.person(img, cam, x, y, s, sp, 0.0, 180)


def on_screen(t, pc=None):
    """Who is drawn in this frame."""
    pc = pc or pancam(t)
    if pc.shot in WIDE:
        return list(SHOT_CAST[pc.shot])
    on = [w for w in WHO if visible(w, pc)]
    if t < 25.6:
        on = [w for w in on if w != 'patriot']            # never in shot before the reveal (brief 10)
    return on


def scene(t):
    """The solids for the collision and pop-in tests: each person on screen at their mark on the plan (metres), as a
    simple figure (their hands rest on the table: ALLOWED_CONTACTS); the table and every THING come from PLAN."""
    import audit
    out = []
    for who in on_screen(t):
        x, z = PL.PEOPLE[who]['at']
        h = PC.HEIGHTS.get(CAST[who].get('name', ''), 1.75)
        out.append(audit.Thing(who, audit.simple(who, x, z, height=h, facing=(-x, -z))))
    return out


def audits():
    """The general audit: each person alone over every frame they are on screen (in pieces, popping, stretching,
    frozen), and the eyelines. Returns faults."""
    def alone(who):
        def draw(t):
            lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
            draw_person(lay, pancam(t), who, t)
            return lay
        return draw
    actors = {}
    for who in WHO:
        for shot, a, b in SHOTS:
            ts = [i / FPS for i in range(int(a * FPS), int(b * FPS)) if who in on_screen(i / FPS)]
            if ts:
                actors[f'{who} [{shot}]'] = (ts, alone(who))
    filmkit.EYES.clear()
    faults = filmkit.silhouette_audit(actors, fps=FPS, still_ok=())
    faults += filmkit.check_eyelines(allow=[('patriot', 44.8, DUR, 'ahead in the awkward silence, then at both as he points')])
    return faults


def picture(t):
    """The frame WITHOUT captions (those go on last, so wording notes never re-render a picture)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    if not getattr(B.gesture_hand, 'point_finger', False):   # drawing the Patriot from behind loads patriots3_cast,
        install_point_finger(B)                              # which puts the plain circle hands back (found 1 Nov)
    pc = pancam(t)
    img = B.canvas((0, 0, 0))
    if pc.shot in WIDE:
        return wide_picture(img, pc, t)
    RM.room(img, pc, t)
    on = on_screen(t, pc)
    layers = {}
    for who in on:
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        j2, sp = draw_person(lay, pc, who, t)
        img.alpha_composite(lay)
        layers[who] = (lay, j2, sp)
    RM.table_top(img, pc)
    for who, (lay, j2, sp) in layers.items():
        if who != 'patriot' or t >= T_POINT:
            img.paste(lay, (0, 0), Image.composite(lay.getchannel('A'), Image.new('L', lay.size, 0), arms_mask(pc, who, j2, sp)))
    RM.coin_pile(img, pc)
    s = shot_of(t)
    if s == 'his view':                           # (shot 13: just Romesh and Bash, Sam 1 Nov)
        shoulder(img, 'patriot', 20, 1720, 1.6)   # bottom left: he sits to their left (3 o'clock)
    if s in ('patriot 2', 'traitors'):            # in both, so they never appear from nowhere (animatic 1 note 3)
        shoulder(img, 'bash', 70, 1830, 1.6)
        shoulder(img, 'romesh', 1030, 1830, 1.6)
    return img


def wide_picture(img, pc, t):
    """Shots 9 and 13 (patriots4_wide): the room behind, them (far to near), the table over their
    laps, their forearms and hands again over its top, the coins; in shot 9 the Patriot's shoulder in the corner."""
    WV.room(img, t)
    layers = {}
    for who in sorted(SHOT_CAST[pc.shot], key=lambda w: -WV.body(w, 1.78)[3]):
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        j2, sp = draw_person(lay, pc, who, t)
        img.alpha_composite(lay)
        layers[who] = (lay, j2, sp)
    WV.table(img)
    for who, (lay, j2, sp) in layers.items():
        img.paste(lay, (0, 0), Image.composite(lay.getchannel('A'), Image.new('L', lay.size, 0), arms_mask(pc, who, j2, sp)))
    WV.coin_pile(img)
    if pc.shot == 'his view':                     # (shot 13: just Romesh and Bash, Sam 1 Nov)
        shoulder(img, 'patriot', 20, 1720, 1.6)   # bottom left: his own shoulder, the camera at his seat
    return img


def caption_at(t):
    for i, (a, c, ln) in enumerate(CHUNKS):
        nxt = CHUNKS[i + 1][0] if i + 1 < len(CHUNKS) else 1e9
        if a <= t < min(nxt, ln['end'] + ln.get('hold', 0.35)):
            return c
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
    voice, rest = np.zeros(n), np.zeros(n)        # voices only (Sam: no sound effects); no room tone
    for ln in LINES:
        s = int(ln['start'] * SR)
        seg = ln['_voice'][:max(0, n - s)]
        voice[s:s + len(seg)] += seg
    mix = voice + rest
    end = int(BLACK_AT * SR)
    mix, g = MA.master(mix, end)
    voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


def mouths_seen(t):
    pc = pancam(t)
    out = []
    for who in WHO:
        if visible(who, pc) and not (who == 'patriot' and t < 25.6):
            out.append((who, mouth(who, t), 0.0, 2 * CAST[who].get('hh', 90) * S * pc.zoom))
    return out


def checks():
    """Plan checks: seconds. Raises on the first batch of faults; prints the subtitles to proofread."""
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches'] if ln['n'] != 5]
    faults = E.check_mouths(sorted(x for w in WHO for x in TRACK[w]), windows)
    _, voice, rest = soundtrack(stems=True)
    faults += filmkit.voice_balance(voice, rest, SR, windows)
    n = int((DUR + 0.3) * SR)
    raw = np.zeros(n)
    for ln in LINES:
        s = int(ln['start'] * SR)
        raw[s:s + len(ln['_voice'])] += ln['_voice'][:n - s]
    faults += MA.limit_check(raw, int(BLACK_AT * SR))
    mix, voice, rest = soundtrack(stems=True)
    faults += filmkit.hiss_check(mix, SR, BLACK_AT)
    for q in filmkit.sound_questions({'voice': voice, 'background': rest, 'mix': mix}, SR,
                                     cuts=[a for _, a, _ in SHOTS[1:]], end=BLACK_AT):
        print('QUESTION FOR SAM:', q)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


def sheet(out, times=None):
    """One labelled sheet: a still per shot (the middle of each, or the given times), time and shot on each tile."""
    B.SS = 1
    times = times or [round((a + b) / 2 if s not in PANS else PANS[s][3] + 0.6, 2) for s, a, b in SHOTS]
    font = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 30)
    tiles = []
    import hook_text
    import tempfile
    hook = os.path.join(tempfile.mkdtemp(), 'hook.png')
    hook_text.card(1080, 1920, HOOK[0], HOOK[1]['y'], hook)
    for t in times:
        im = frame_image(t).convert('RGBA')
        if t < SHOTS[0][2]:                                # the Hook Text as finish.py will lay it (shot 1 only)
            im.alpha_composite(Image.open(hook).convert('RGBA').resize(im.size))
        im = im.convert('RGB').resize((432, 768))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 432, 44), fill=(0, 0, 0))
        d.text((8, 6), f'{t:.1f}s  {SHOTS.index(next(x for x in SHOTS if x[0] == shot_of(t))) + 1}: {shot_of(t)}',
               font=font, fill=(255, 255, 255))
        tiles.append(im)
    cols = 6
    rows = (len(tiles) + cols - 1) // cols
    W = Image.new('RGB', (cols * 442 + 10, rows * 778 + 10), (20, 20, 20))
    for i, im in enumerate(tiles):
        W.paste(im, (10 + (i % cols) * 442, 10 + (i // cols) * 778))
    W.save(out, quality=84)
    return out


def LINE_SUBJECTS():
    return PC.LINE_SUBJECTS()


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        print(PC.sheet(a[1]))
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'sheet':
        print(sheet(a[1], [float(x) for x in a[2:]] or None))
    elif a[0] == 'check':
        B.SS = 1
        checks()
        print('plan checks: clean')
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
import moves                     # noqa: E402,F401
import perform                   # noqa: E402,F401

if __name__ == '__main__':
    main()
