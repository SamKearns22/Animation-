#!/usr/bin/env python3
"""Poker Mon (TikTok satire, Sam 19 Oct): a high-class, high-stakes poker game, played with Poker Mon cards. Player
one lays down four Queens: "Four of a kind." We swing round to player two, who looks at his hand: "Dragonite, use
hyper beam." The shot widens: a Dragonite in a bow tie stands beside him and charges up; player one is slowly lit by
the glow; from above, the beam blows everyone and everything in the room far out of shot (as at the end of The Salt);
player two calmly pulls in the chips. Notes, the brief as a checklist and decisions: notes/poker-mon.md. People,
Dragonite, cards and chips: source/poker_mon_cast.py. Guide: guides/satire.md.

    python3 source/poker_mon.py cast OUT.jpg              the cast sheet (every view used)
    python3 source/poker_mon.py stills OUT_DIR T [T ...]  stills at these times (seconds)
    python3 source/poker_mon.py sheet OUT.jpg T [T ...]   several stills side by side on one sheet
    python3 source/poker_mon.py check                     every check and the audit (also run by preflight.py)
    python3 source/poker_mon.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT] [--span T0 T1]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import poker_mon_cast as C       # noqa: E402  (people, Dragonite, cards, chips)
import poker_mon_room as R       # noqa: E402  (shot 6: the parlour in perspective, the sweep, the physics)
import views as V                # noqa: E402
import moves                     # noqa: E402
import figure as F               # noqa: E402
import mouths                    # noqa: E402
import mossad_audio as MA        # noqa: E402
import peepee as PP              # noqa: E402
import filmkit                   # noqa: E402
import film_engine as E          # noqa: E402
from ed import INK, curve        # noqa: E402
from satire_style import rough   # noqa: E402

FPS, SR = 12, MA.SR
NAME = 'poker-mon'

# =============================================== STORY ==============================================================
# Sam's recordings are still to come ('audio' names the file when they do; until then the line is timed by hand).
LINES = [
    dict(n=1, who='P1', text='Four of a kind.', audio='poker-mon-1', start=1.9, end=3.0),
    dict(n=2, who='P2', text='Dragonite, use hyper beam.', audio='poker-mon-2', start=6.1, end=7.7),
]
SHOTS = [('p1', 0.0, 3.6), ('cards', 3.6, 4.7), ('p2', 4.7, 8.0), ('reveal', 8.0, 11.0), ('lit', 11.0, 12.5),
         ('blast', 12.5, 19.0)]
DUR = BLACK_AT = 19.0
LAY = (0.5, 1.5)          # player one lays his hand: the fan leaves his hand, the cards spread on the felt
LOOK_DOWN = (4.9, 5.9)    # player two inspects his hand
CHARGE = (8.9, 12.6)      # the Dragonite throws its head back; the ball of light grows in its mouth
FIRE = R.Clock.FIRE       # the head snaps forward: the beam
IMPACT = R.Clock.IMPACT   # it reaches player one; then it sweeps round the table (poker_mon_room.SWEEP)
BEAM_END = R.Clock.BEAM_END   # the beam thins and goes out
PULL = R.Clock.PULL       # after a pause (R.Clock.PAUSE), player two pulls the pot in
HOOK = ('', {'y': 880})   # Hook Text pending (Sam); exactly as finish.py will be given it
KEEP_CLEAR = []
PROP_SIZES = [('playing card', 'playing card', 0.063, 0.088, None)]
OUTFIT = {}
HEIGHTS = C.HEIGHTS
ALLOWED, CONTACTS, MOMENTUM, PUSHES = [], [], [], []
LINE_OK = [('GUARD1', 'edge with no line', 566, 106)]   # the shine on his bald head: a flat highlight, the kit's own
TABLE_Y = 300             # a seated player's edge of the table, in their own units (neck at 0)
# ====================================================================================================================

for ln in LINES:                                  # time each line to its recording when there is one
    ln['_voice'], ln['_stretches'] = None, [(0.0, ln['end'] - ln['start'])]
    if ln.get('audio') and os.path.exists(os.path.join(HERE, 'audio', ln['audio'] + '.m4a')):
        v = MA.line(ln['audio'])
        ln['_voice'], ln['end'] = v, ln['start'] + len(v) / SR
        ln['_stretches'] = MA.pauses(v, 0.12)
TRACK = {w: [(a + ln['start'], b + ln['start'], sh) for ln in LINES if ln['who'] == w
             for a, b, sh in mouths.track(ln['text'], ln['_stretches'])] for w in ('P1', 'P2')}
BLINKS = {'P1': [b for b in F.blinks(5, 0.6, 11.0, talking=True) if not 1.7 < b < 3.4],
          'P2': [b for b in F.blinks(9, 4.8, 18.0, talking=True) if not 7.5 < b < 8.6]}
# Subtitles: short chunks, each on its first word; the punchline on its own.
CAPS = [(LINES[0]['start'] + 0.05, LINES[0]['end'] + 0.4, 'Four of a kind.'),
        (LINES[1]['start'] + 0.05, LINES[1]['end'] + 0.3, 'Dragonite, use hyper beam.')]


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
    return None if sh == 'rest' else 'v:' + sh


def idle_x(who, t):
    """A held position with a small quick weight shift now and then (never a sway)."""
    return 6 * filmkit.shifts(t, seed=sum(map(ord, who)), amount=1.0)


# ------------------------------------------------------------------------------------------------ the room
# refs casino-royale-1..4: warm and golden, cream walls with gold trim, crystal chandeliers, pale lampshades hung low
# over the table, cream padded armchairs; a big oval of green felt with a thin yellow line and a dark leather rail.
WALL = (226, 204, 156)
WALL_D = (196, 170, 120)
GOLD = (204, 158, 64)
GOLD_D = (150, 110, 40)
FELT = (34, 112, 72)
FELT_D = (26, 88, 56)
LINE_Y = (226, 196, 70)
RAIL = (64, 38, 28)
RAIL_L = (96, 60, 42)
CARPET = (118, 30, 40)
CARPET_D = (90, 22, 32)
SHADE = (246, 232, 196)
ARMCHAIR = (236, 222, 190)
ARMCHAIR_D = (200, 184, 150)


def wall(img, cam, x0, x1, y0, y1, seed=0, panel_w=280, lamps=()):
    """The casino wall: cream, tall gold-framed panels, a moulded rail, brass sconces with pale shades."""
    p = B.Pen(img, cam)
    p.poly(rough([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 4, seed), WALL, INK, 2.6)
    rail = y0 + (y1 - y0) * 0.66
    x, k = x0 + 30, 0
    while x < x1:
        p.poly(rough([(x + 20, y0 + 50), (x + panel_w - 20, y0 + 50), (x + panel_w - 20, rail - 30),
                      (x + 20, rail - 30)], 3, seed + k), WALL_D, GOLD, 3.0)
        p.poly(rough([(x + 40, y0 + 72), (x + panel_w - 40, y0 + 72), (x + panel_w - 40, rail - 52),
                      (x + 40, rail - 52)], 3, seed + k + 40), WALL, GOLD_D, 2.0)
        p.poly(rough([(x + 20, rail + 30), (x + panel_w - 20, rail + 30), (x + panel_w - 20, y1 - 30),
                      (x + 20, y1 - 30)], 3, seed + k + 80), WALL_D, GOLD, 2.4)
        x += panel_w
        k += 1
    p.poly([(x0, rail - 12), (x1, rail - 12), (x1, rail + 12), (x0, rail + 12)], GOLD, INK, 2.2)
    for lx, ly in lamps:
        p.poly([(lx - 7, ly + 10), (lx + 7, ly + 10), (lx + 7, ly + 70), (lx - 7, ly + 70)], GOLD, INK, 1.8)
        p.poly(rough([(lx - 34, ly + 14), (lx + 34, ly + 14), (lx + 22, ly - 34), (lx - 22, ly - 34)], 2, lx), SHADE,
               INK, 2.0)


def hanging_shade(img, cam, x, y, w, seed=0):
    """A pale lampshade hung low over the table (refs casino-royale-1)."""
    p = B.Pen(img, cam)
    p.line([(x, y - 900), (x, y - w * 0.4)], GOLD_D, 3)
    p.poly(rough([(x - w * 0.36, y - w * 0.42), (x + w * 0.36, y - w * 0.42), (x + w * 0.5, y), (x - w * 0.5, y)], 3,
                 seed), SHADE, INK, 2.6)
    p.poly([(x - w * 0.5, y - 6), (x + w * 0.5, y - 6), (x + w * 0.5, y + 6), (x - w * 0.5, y + 6)], GOLD, INK, 1.8)


def chandelier(img, cam, x, y, w):
    p = B.Pen(img, cam)
    p.line([(x, y - 600), (x, y)], GOLD_D, 3)
    for k, r in enumerate((w * 0.5, w * 0.34, w * 0.18)):
        yy = y + k * w * 0.16
        p.line(curve([(x - r, yy), (x, yy + r * 0.25), (x + r, yy)], 3), GOLD, 4)
        for a in np.linspace(-1, 1, 5 + 2 * (2 - k)):
            cx = x + a * r
            p.poly([(cx, yy + 6), (cx + 9, yy + 26), (cx, yy + 46), (cx - 9, yy + 26)], (250, 248, 236), INK, 1.4)


def armchair_back(img, cam, x, y, s):
    """A cream padded casino armchair seen from the front of its back, in the units of someone seated in it."""
    p = B.Pen(img, B.Local(cam, x, y, s))
    p.poly(curve([(-170, 340), (-180, 60), (-160, -110), (-90, -150), (0, -158), (90, -150), (160, -110), (180, 60),
                  (170, 340)], 4), ARMCHAIR, INK, 2.6)
    for k in range(3):                                                             # the buttoned padding
        for a in (-1, 0, 1):
            p.ell(a * 90 + (45 if k % 2 else 0) * (1 if a < 1 else 0), -80 + k * 90, 5, 5, ARMCHAIR_D, None)


def table_far(img, cam, x, y, s, x0, x1, seed=0):
    """The far side of the table seen across it (a player's own units): leather rail, green felt, the yellow line."""
    p = B.Pen(img, B.Local(cam, x, y, s))
    ry = TABLE_Y
    p.poly(rough([(x0, ry + 90), (x1, ry + 90), (x1, ry + 1400), (x0, ry + 1400)], 3, seed), FELT, INK, 2.6)
    p.line(curve([(x0 + 60, ry + 300), (0, ry + 260), (x1 - 60, ry + 300)], 4), LINE_Y, 4)
    p.poly(rough([(x0, ry - 4), (x1, ry - 4), (x1, ry + 96), (x0, ry + 96)], 3, seed + 3), RAIL, INK, 2.6)
    p.line([(x0, ry + 20), (x1, ry + 20)], RAIL_L, 3)


def arms_over_table(img, cam, x, y, s, sp, j, j2):
    """Forearms resting on the table lie over its edge: drawn again after the table."""
    sides = [sd for sd in 'LR' if j2.get('hand', {}).get(sd) in ('fist', 'palm') and j['wr' + sd][1] > TABLE_Y - 30]
    p = B.Pen(img, B.Local(cam, x, y, s))
    for sd in sides:
        V.arm(p, j2, sd, sp)


# ------------------------------------------------------------------------------------------------ poses
def seated(sp, kind='rest', u=0.0):
    """The upper body of a player behind the table. kind: 'rest' (forearms on the table), 'hold' (player one's hand
    held at his chest, then laid down by u 0..1), 'fan' (player two's hand held up in both hands), 'pull'
    (player two's arms reaching for the pot, u 0 out .. 1 drawn in)."""
    j = V.standing(sp)
    j['props'] = [C.dress_up(sp)]
    if kind == 'rest':
        for sd, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, sd, (sg * 70, TABLE_Y + 40, 240.0), 'down', 'fist')
    elif kind == 'hold':                                   # player one lays his hand: a dealer's spread
        V.arm_to(j, 'L', (-70, TABLE_Y + 40, 240.0), 'down', 'fist')
        V.arm_to(j, 'R', spread_hand(u), 'down', 'palm')
    elif kind == 'fan':
        for sd, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, sd, (sg * 58, 236.0, 200.0), 'down', 'fist')
    elif kind == 'pull':
        for sd, sg in (('L', -1), ('R', 1)):
            z = 330.0 - 110 * u
            V.arm_to(j, sd, (sg * (110 - 40 * u), TABLE_Y + 60, z), 'down', 'palm')
    return j


SPREAD = dict(chest=(40.0, 190.0, 170.0), start=(-130.0, TABLE_Y + 46, 300.0), end=(150.0, TABLE_Y + 46, 300.0),
              rest=(90.0, TABLE_Y + 40, 250.0))


def spread_hand(u):
    """Player one's right hand through the lay, u 0..1: from his chest down onto the felt at the spread's start
    (contact at 0.4), sliding along the felt to its end, the cards fanning out under it (to 0.82), then back to
    rest beside them."""
    a, b, c, d = SPREAD['chest'], SPREAD['start'], SPREAD['end'], SPREAD['rest']
    lerp = lambda p, q, k: tuple(x + (y - x) * k for x, y in zip(p, q))
    if u < 0.4:
        k = ease(u / 0.4)
        out = lerp(a, b, k)
        return (out[0], out[1] - 60 * math.sin(math.pi * k), out[2])      # an arc down onto the table
    if u < 0.82:
        return lerp(b, c, ease((u - 0.4) / 0.42))
    k = ease((u - 0.82) / 0.18)
    out = lerp(c, d, k)
    return (out[0], out[1] - 40 * math.sin(math.pi * k), out[2])


def held_fan(img, n, at, w, spread=10.0, back=True, faces=None):
    """Cards fanned in a hand, seen from the front: their backs (to us), pivoting at the hand point `at`."""
    def draw(p, j2):
        hx, hy = at(j2)
        for i in range(n):
            ang = (i - (n - 1) / 2) * spread
            a = math.radians(ang)
            h = w * C.CH / C.CW
            pts = []
            for dx, dy in ((-w / 2, -h * 0.92), (w / 2, -h * 0.92), (w / 2, h * 0.08), (-w / 2, h * 0.08)):
                pts.append((hx + dx * math.cos(a) - dy * math.sin(a), hy + dx * math.sin(a) + dy * math.cos(a)))
            src = C.card_back() if back else C.card_face(*faces[i])
            C.place_image(img, p.cam, src, pts)
    return draw


# ------------------------------------------------------------------------------------------------ light
def light_level(t):
    """How bright the Hyper Beam's light is on everyone: the charge grows it, the blast peaks it, then it fades."""
    if t < CHARGE[0] + 0.4:
        return 0.0
    if t < FIRE:
        return 0.55 * ease((t - CHARGE[0] - 0.4) / (FIRE - CHARGE[0] - 0.4)) ** 1.4
    if t < BEAM_END[0]:
        return 0.9
    return 0.9 * (1 - ease((t - BEAM_END[0]) / (BEAM_END[1] - BEAM_END[0] + 0.4)))


def wash(img, k, colour=(255, 236, 170), centre=None, cam=None, radius=900):
    """The glow's light falling over the picture (Sam: like the show): a warm wash, strongest near the source."""
    if k <= 0.003:
        return
    a = np.asarray(img, np.float32)
    if centre is not None:
        h, w = a.shape[:2]
        X, Y = np.meshgrid(np.arange(w), np.arange(h))
        cx, cy = cam.P(*centre)
        d = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2) / cam.S(radius)
        m = (np.clip(1.2 - d, 0.25, 1.0))[..., None] * k
    else:
        m = k
    tint = np.array(colour, np.float32) / 255.0                  # warm light: brighter and warmer, blacks kept
    a[..., :3] = a[..., :3] * (1 + 0.9 * m * tint) + 70 * m * tint * (a[..., :3] / 255.0) ** 0.5
    img.paste(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), img.mode))


# ------------------------------------------------------------------------------------------------ shot 1: player one
S1 = dict(x=540, neck=1010, s=1.15)


def p1_face(t):
    sh = filmkit.shifts(t, seed=101, amount=1.0)
    out = dict(look=0.0, blink=F.blinking(t, BLINKS['P1']), head_dx=4 * sh, head_dy=8, lid=2)
    m = talking_mouth('P1', t)
    out['mouth'] = m or ('pleased' if t > LINES[0]['end'] else 'line')
    if t > LINES[0]['end']:
        out.update(brows='confused', lid=4)                    # the smug look: one brow up, heavy lids
    if t >= SHOTS[4][1]:                                       # lit by the glow: the smirk goes, then alarm
        k = (t - SHOTS[4][1]) / (SHOTS[4][2] - SHOTS[4][1])
        out.update(brows='confused' if k < 0.35 else 'alarm', lid=4 if k < 0.35 else 0,
                   mouth='pleased' if k < 0.35 else 'agape', look=0.0)
    return out


def shot_p1(img, t):
    """Player one, from player two's seat: the portrait wall behind him (poker_mon_room: the +x wall, the portrait to
    our left, the window and drapes to our right), his escort standing at his shoulder with her hand on it, the guard
    behind, the man in the card shirt half in frame at our right."""
    close = t >= SHOTS[4][1]
    cam = B.Cam(1.32, 540, 1120) if not close else B.Cam(1.6 + 0.35 * ease((t - SHOTS[4][1]) / 1.2), 540, 820)
    wall(img, cam, -300, 1380, -200, 1500, seed=3, panel_w=300, lamps=[(140, 620), (940, 620)])
    portrait(img, cam, 300, 250, 260, 340)
    drapes(img, cam, 820, 1260, 40, 1180)
    s = S1['s']
    C.person(img, cam, 160, 560, 0.72, C.GUARD2, t, 0, C.pose_standing(C.GUARD2))
    se, ex, ey = 1.02, 300 + idle_x('ESCORT', t) * 0.5, 905
    spe = dict(C.ESCORT, blink=F.blinking(t, BLINKS['P1'][1:]), look=0.4, mouth='pleased' if t < SHOTS[4][1] else 'line')
    if close and (t - SHOTS[4][1]) > 0.5:
        spe.update(brows='alarm', mouth='agape', look=0.0)
    je = C.pose_standing(spe)
    armchair_back(img, cam, 1080, 1160, 0.95)
    jc = seated(C.CARDS, 'rest')
    jc2 = C.person(img, cam, 1080 + idle_x('CARDS', t) * 0.8, 1140, 0.95, dict(C.CARDS, look=-0.6, mouth='line'), t, -45,
                   jc)
    armchair_back(img, cam, S1['x'], S1['neck'] + 26 * s, s)
    sp = dict(C.P1)
    sp.update(p1_face(t))
    u = (t - LAY[0]) / (LAY[1] - LAY[0])
    j = seated(sp, 'hold', min(1.0, max(0.0, u)))
    if u < 0.4:                                                        # the hand still holds the fan (backs to us)
        j['props'].append(held_fan(img, 4, lambda j2: (j2['wrR'][0] - 4, j2['wrR'][1] - 10), 120, 12))
    x = S1['x'] + idle_x('P1', t)
    shL = j['shL']                                                     # her hand rests on his left shoulder
    tgt_screen = (x + s * shL[0], S1['neck'] + s * (shL[1] - 16 + V.ELEV * shL[2]))
    zb = 150.0
    tgt = ((tgt_screen[0] - ex) / se, (tgt_screen[1] - ey) / se - V.ELEV * zb, zb)
    V.arm_to(je, 'R', tgt, 'down', 'palm')
    je2 = C.person(img, cam, ex, ey, se, spe, t, 0, je)
    j2 = C.person(img, cam, x, S1['neck'], s, sp, t, 0, j)
    pe = B.Pen(img, B.Local(cam, ex, ey, se))
    V.arm(pe, je2, 'R', spe)                                           # her arm lies over his shoulder
    table_far(img, cam, S1['x'], S1['neck'], s, -900, 900, seed=1)
    L = B.Local(cam, S1['x'], S1['neck'], s)
    C.chip_stack(img, L, -330, TABLE_Y + 260, 52, 6, 'poke', seed=1)
    C.chip_stack(img, L, -220, TABLE_Y + 300, 52, 4, 'great', seed=2)
    C.chip_stack(img, L, 330, TABLE_Y + 290, 52, 5, 'ultra', seed=3)
    pl = B.Pen(img, L)
    C.glass(pl, -400, TABLE_Y + 200, 110, 'tumbler', (196, 120, 40))
    pl.poly(rough(C.card_quad(-470, TABLE_Y + 330, 140, 30, 0.5), 2, 3), (248, 246, 240), INK, 1.4)   # a napkin
    candles = [(250, TABLE_Y + 170), (290, TABLE_Y + 180)]
    for i, (cx_, cy_) in enumerate(candles):
        C.candle(pl, cx_, cy_, 120, t, 70 + i, w=14)
    laid_queens(img, L, t)
    arms_over_table(img, cam, x, S1['neck'], s, sp, j, j2)
    arms_over_table(img, cam, 1080, 1140, 0.95, C.CARDS, jc, jc2)
    hanging_shade(img, cam, 540, -40, 520, seed=2)
    lights = [(cam.P(540, 1300)[0] / B.SS, cam.P(540, 1300)[1] / B.SS, 650 * cam.z, 0.7, (255, 214, 150))]
    for lx in (140, 940):
        X, Y = cam.P(lx, 600)
        lights.append((X / B.SS, Y / B.SS, 260 * cam.z, 0.5 * C.flicker(t, lx), (255, 196, 120)))
    for i, (cx_, cy_) in enumerate(candles):
        X, Y = L.P(cx_, cy_ - 140)
        lights.append((X / B.SS, Y / B.SS, 220 * L.s, 0.55 * C.flicker(t, 70 + i), (255, 190, 110)))
    if close:                                                          # the Hyper Beam's light, growing on him
        lights.append((540, 760, 1100, 1.6 * light_level(t), (255, 236, 170)))
    R.parlour(img, lights)
    for i, (cx_, cy_) in enumerate(candles):                           # the flames are self-lit
        C.candle(pl, cx_, cy_, 120, t, 70 + i, w=14)


def portrait(img, cam, x, y, w, h):
    """A dark old-master portrait in a gilt frame (a figure in a ruff), flat colour."""
    p = B.Pen(img, cam)
    p.poly(rough([(x - w / 2 - 22, y - 22), (x + w / 2 + 22, y - 22), (x + w / 2 + 22, y + h + 22), (x - w / 2 - 22, y + h + 22)],
                 3, 1), GOLD, INK, 2.6)
    p.poly([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h), (x - w / 2, y + h)], (60, 44, 34), INK, 2.0)
    p.poly([(x - w * 0.36, y + h), (x + w * 0.36, y + h), (x + w * 0.3, y + h * 0.62), (x - w * 0.3, y + h * 0.62)],
           (30, 26, 28), None)
    p.ell(x, y + h * 0.6, w * 0.2, h * 0.06, (226, 220, 206), INK, 1.4)
    p.ell(x, y + h * 0.42, w * 0.14, h * 0.17, (206, 168, 140), INK, 1.6)
    for sg in (-1, 1):                                                 # the sitter's eyes and a stern mouth
        p.ell(x + sg * w * 0.05, y + h * 0.4, 3, 3, INK, None)
    p.line([(x - w * 0.04, y + h * 0.5), (x + w * 0.04, y + h * 0.5)], INK, 2)


def drapes(img, cam, x0, x1, y0, y1):
    """A tall window at night between velvet drapes, a gilt pelmet over them."""
    p = B.Pen(img, cam)
    p.poly([(x0 + 90, y0 + 60), (x1 - 90, y0 + 60), (x1 - 90, y1), (x0 + 90, y1)], (30, 34, 56), INK, 2.2)
    for a0, a1 in ((x0, x0 + 150), (x1 - 150, x1)):
        p.poly(rough([(a0, y0), (a1, y0), (a1 + (10 if a0 == x0 else -10), y1 + 60), (a0, y1 + 60)], 3, int(a0)),
               (120, 22, 40), INK, 2.4)
        for k in range(1, 4):
            xx = a0 + (a1 - a0) * k / 4
            p.line([(xx, y0 + 30), (xx + 6, y1 + 40)], (88, 14, 30), 2.4)
    p.poly(rough([(x0 - 20, y0 - 30), (x1 + 20, y0 - 30), (x1 + 20, y0 + 40), (x0 - 20, y0 + 40)], 3, 4), GOLD, INK, 2.4)


def laid_queens(img, L, t):
    """The four Queens spread face up on the felt from where his hand touched down, each appearing as his palm
    passes over its place (the hand is drawn over them, so it is always on the cards)."""
    u = (t - LAY[0]) / (LAY[1] - LAY[0])
    if u < 0.4:
        return
    hx = spread_hand(min(u, 0.82))[0]
    x0, x1 = SPREAD['start'][0], SPREAD['end'][0]
    for i, suit in enumerate('SCDH'):
        cx = x0 + 10 + i * (x1 - x0 - 20) / 3
        if hx < cx - 30:
            continue
        y = TABLE_Y + 46 + V.ELEV * 300 + 30                    # the felt under the palm, as views draws it
        C.place_image(img, L, C.card_face('Q', suit), C.card_quad(cx, y, 150, (i - 1.5) * 5, 0.55))


# ------------------------------------------------------------------------------------------------ shot 2: the cards
def shot_cards(img, t):
    """The four Queens on the felt from above, readable; chips round them."""
    z = 1.0 + 0.06 * ease((t - SHOTS[1][1]) / (SHOTS[1][2] - SHOTS[1][1]))
    cam = B.Cam(z, 540, 960)
    p = B.Pen(img, cam)
    p.poly([(-200, -200), (1280, -200), (1280, 2200), (-200, 2200)], FELT, None)
    p.line(curve([(-200, 300), (540, 200), (1280, 300)], 4), LINE_Y, 6)
    for i, suit in enumerate('SCDH'):
        C.place_image(img, cam, C.card_face('Q', suit), C.card_quad(240 + i * 200, 960 + abs(i - 1.5) * 30, 300,
                                                                     (i - 1.5) * 7))
    C.chip_stack(img, cam, 180, 1500, 90, 6, 'poke', squash=0.5, seed=4)
    C.chip_stack(img, cam, 400, 1580, 90, 4, 'great', squash=0.5, seed=5)
    C.chip_stack(img, cam, 840, 1520, 90, 7, 'ultra', squash=0.5, seed=6)
    C.chip_stack(img, cam, 860, 440, 90, 3, 'master', squash=0.5, seed=7)
    C.glass(p, 200, 560, 190, 'tumbler', (196, 120, 40))
    lights = [(540, 900, 900, 0.75, (255, 214, 150)), (180, 440, 420, 0.4 * C.flicker(t, 70), (255, 190, 110))]
    R.parlour(img, lights)


# ------------------------------------------------------------------------------------------------ shots 3-4: player two
S3 = dict(x=720, neck=1010, s=1.15)
DRAGON = dict(x=-60, foot=1560, s=0.84)


def p2_face(t):
    sh = filmkit.shifts(t, seed=202, amount=1.0)
    out = dict(look=0.0, blink=F.blinking(t, BLINKS['P2']), head_dx=3 * sh, head_dy=8, mouth='line', brows='serious')
    if LOOK_DOWN[0] <= t < LOOK_DOWN[1]:                       # inspecting his hand: eyes down to the cards
        out.update(lid=7, head_dy=16)
    m = talking_mouth('P2', t)
    if m:
        out['mouth'] = m
    return out


def reveal_cam(t):
    """Close on player two, then the shot widens (eased) to show the Dragonite beside him."""
    if t < SHOTS[3][1] + 0.25:
        return B.Cam(1.7, S3['x'], 800)
    k = ease((t - SHOTS[3][1] - 0.25) / 1.3)
    return B.Cam(1.7 + (0.74 - 1.7) * k, S3['x'] + (330 - S3['x']) * k, 800 + (900 - 800) * k)


def dragon_state(t):
    """The Dragonite's head, mouth, eyes, wings and arms over the film."""
    st = dict(head=0.0, mouth_open=0.0, eyes='open', wings=0.15, arms=0.0, lean=0.0, ball=0.0)
    if t >= CHARGE[0]:
        k = ease((t - CHARGE[0]) / 0.7)
        st.update(head=-34 * k, mouth_open=0.9 * k, eyes='narrow' if k > 0.3 else 'open', wings=0.15 + 0.5 * k,
                  arms=0.35 * k)
        st['ball'] = ease((t - CHARGE[0] - 0.4) / (FIRE - CHARGE[0] - 0.4))
    if t >= FIRE - 0.12:                                        # the head snaps forward and down (fast)
        k = min(1.0, (t - (FIRE - 0.12)) / 0.12)
        st.update(head=-34 + 50 * k, lean=10 * k, mouth_open=1.0, wings=0.65 + 0.35 * k, arms=0.35 + 0.65 * k,
                  eyes='narrow')
    if t >= BEAM_END[1]:                                        # done: settles, mouth shut, pleased with itself
        k = ease((t - BEAM_END[1]) / 0.6)
        st.update(head=16 * (1 - k), lean=10 * (1 - k), mouth_open=1.0 * (1 - k), wings=1.0 - 0.85 * k,
                  arms=1.0 - k, eyes='closed' if k > 0.5 else 'narrow', ball=0.0)
    return st


def sideboard2d(img, cam, t, x, y, flames_only=False):
    """The sideboard against the wall behind player two: dark wood, a decanter, a candelabra (flickering)."""
    p = B.Pen(img, cam)
    if not flames_only:
        p.poly(rough([(x - 260, y - 180), (x + 260, y - 180), (x + 260, y + 120), (x - 260, y + 120)], 3, 8), R.WOOD,
               INK, 2.4)
        p.poly(rough([(x - 280, y - 200), (x + 280, y - 200), (x + 280, y - 170), (x - 280, y - 170)], 2, 9), R.WOOD_D,
               INK, 2.0)
        for dx in (-130, 130):
            p.poly(rough([(x + dx - 100, y - 140), (x + dx + 100, y - 140), (x + dx + 100, y + 90), (x + dx - 100, y + 90)],
                         2, dx + 3), R.WOOD_D, R.GOLD_D, 1.8)
        p.poly(rough([(x - 190, y - 200), (x - 150, y - 200), (x - 140, y - 260), (x - 160, y - 300), (x - 160, y - 330),
                      (x - 180, y - 330), (x - 180, y - 300), (x - 200, y - 260)], 1, 2), (150, 70, 36), INK, 1.8)
    for i, dx in enumerate((100, 140, 180)):
        if not flames_only:
            p.line([(140 + x, y - 200), (140 + x, y - 280)], R.GOLD, 6)
        C.candle(p, x + dx, y - 280 + (14 if i != 1 else 0), 70, t, 31 + i, w=9)


def shot_p2(img, t):
    cam = B.Cam(1.7, S3['x'], 800) if t < SHOTS[3][1] else reveal_cam(t)
    wall(img, cam, -500, 1500, -300, 1500, seed=9, panel_w=300, lamps=[(80, 620), (1000, 620)])
    chandelier(img, cam, 640, 120, 300)
    sideboard2d(img, cam, t, 330, 1000)
    C.person(img, cam, 1060, 560, 0.72, dict(C.WIFE, look=-0.5), t, 0, C.pose_standing(C.WIFE))
    s = S3['s']
    st = dragon_state(t)
    mouth = C.dragonite(img, cam, DRAGON['x'], DRAGON['foot'], DRAGON['s'], t, turn=0.25, flip=1, head=st['head'],
                        mouth_open=st['mouth_open'], eyes=st['eyes'], wings=st['wings'], arms=st['arms'],
                        lean=st['lean'])
    armchair_back(img, cam, S3['x'], S3['neck'] + 26 * s, s)
    sp = dict(C.P2)
    sp.update(p2_face(t))
    j = seated(sp, 'fan')
    j['props'].append(held_fan(img, 5, lambda j2: ((j2['wrL'][0] + j2['wrR'][0]) / 2, (j2['wrL'][1] + j2['wrR'][1]) / 2 - 6),
                               118, 11))
    x = S3['x'] + idle_x('P2', t)
    C.person(img, cam, x, S3['neck'], s, sp, t, 0, j)
    table_far(img, cam, S3['x'], S3['neck'], s, -1400, 900, seed=5)
    L = B.Local(cam, S3['x'], S3['neck'], s)
    C.chip_stack(img, L, -260, TABLE_Y + 260, 52, 8, 'ultra', seed=8)
    C.chip_stack(img, L, 250, TABLE_Y + 280, 52, 5, 'great', seed=9)
    C.chip_stack(img, L, 360, TABLE_Y + 330, 52, 3, 'master', seed=10)
    hanging_shade(img, cam, 640, -80, 520, seed=4)
    lights = [(cam.P(640, 1300)[0] / B.SS, cam.P(640, 1300)[1] / B.SS, 650 * cam.z, 0.7, (255, 214, 150))]
    for lx in (80, 1000):
        X, Y = cam.P(lx, 600)
        lights.append((X / B.SS, Y / B.SS, 260 * cam.z, 0.5 * C.flicker(t, lx + 5), (255, 196, 120)))
    X, Y = cam.P(470, 800)
    lights.append((X / B.SS, Y / B.SS, 260 * cam.z, 0.5 * C.flicker(t, 31), (255, 190, 110)))
    if st['ball'] > 0:
        X, Y = cam.P(*mouth)
        lights.append((X / B.SS, Y / B.SS, 900 * cam.z, 1.5 * light_level(t) + 0.3 * st['ball'], (255, 236, 170)))
    R.parlour(img, lights)
    sideboard2d(img, cam, t, 330, 1000, flames_only=True)
    if st['ball'] > 0:
        C.glow(img, cam, [(mouth[0], mouth[1], 10 + 46 * st['ball'])], strength=0.5 + 0.5 * st['ball'])


# ------------------------------------------------------------------------------------------------ shot 6: the blast
def shot_blast(img, t):
    """The parlour from a high corner, sweeping; the beam swept round the table (poker_mon_room)."""
    R.shot(img, t, sys.modules[__name__])


# ------------------------------------------------------------------------------------------------ the film
def picture(t):
    """The frame WITHOUT captions or Hook Text (those go on last, so wording notes never re-render a picture)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    img = B.canvas(WALL)
    sh = shot_of(t)
    if sh in ('p1', 'lit'):
        shot_p1(img, t)
    elif sh == 'cards':
        shot_cards(img, t)
    elif sh in ('p2', 'reveal'):
        shot_p2(img, t)
    else:
        shot_blast(img, t)
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


# ------------------------------------------------------------------------------------------------ sound
def hum(n, t0, t1):
    """The charge-up: a low hum that rises in pitch and loudness, with a shimmer on top (Sam: yes to effects)."""
    out = np.zeros(n)
    a, b = int(t0 * SR), min(n, int(t1 * SR))
    tt = np.arange(b - a) / SR
    dur = t1 - t0
    f = 70 + 260 * (tt / dur) ** 1.6
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = (tt / dur) ** 1.2
    sig = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3.01 * ph)
    sig += 0.15 * np.sin(2 * np.pi * np.cumsum(f * 6) / SR) * (tt / dur)
    out[a:b] = sig * env * 0.16
    return out


def blast(n, t0, t_end):
    """The beam's roar while it fires, and the boom of the impact (low, short), fading."""
    rng = np.random.default_rng(5)
    out = np.zeros(n)
    a = int(t0 * SR)
    m = min(n - a, int(3.2 * SR))
    tt = np.arange(m) / SR
    noise = rng.standard_normal(m)
    k = np.exp(-np.linspace(0, 1, 40))
    low = np.convolve(noise, k / k.sum(), mode='same')
    boom = np.sin(2 * np.pi * np.cumsum(55 - 25 * np.minimum(tt, 1)) / SR) * np.exp(-tt * 2.2)
    roar_env = np.clip((t_end - t0 - tt) / 0.4, 0, 1) * np.minimum(1, tt / 0.03)
    roar = (0.6 * low + 0.15 * noise) * roar_env + 0.2 * np.sin(2 * np.pi * 180 * tt) * roar_env
    out[a:a + m] = 0.9 * boom + 0.5 * roar + 0.5 * low * np.exp(-tt * 1.5)
    return out


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.random.default_rng(1).standard_normal(n) * 0.002    # quiet room tone
    for ln in LINES:
        if ln['_voice'] is not None:
            s = int(ln['start'] * SR)
            seg = ln['_voice'][:max(0, n - s)]
            voice[s:s + len(seg)] += seg
    rest += hum(n, CHARGE[0] + 0.1, FIRE)
    rest += blast(n, FIRE, BEAM_END[1])
    mix = voice + rest
    end = int(BLACK_AT * SR)
    if np.abs(voice).max() > 1e-6:
        mix, g = MA.master(mix, end)
        voice, rest = voice * g, rest * g
    else:
        mix = mix / max(1e-6, np.abs(mix).max()) * 0.7
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


# ------------------------------------------------------------------------------------------------ checks
def checks():
    """Plan checks: seconds. Raises on the first batch of faults; prints the subtitles to proofread."""
    E.print_subtitles(caption_at, BLACK_AT, FPS)
    faults = []
    if any(ln['_voice'] is not None for ln in LINES):
        windows = [(ln['start'] + a, ln['start'] + b) for ln in LINES for a, b in ln['_stretches']]
        faults += E.check_mouths(sorted(x for w in TRACK for x in TRACK[w]), windows)
        _, voice, rest = soundtrack(stems=True)
        faults += filmkit.voice_balance(voice, rest, SR, windows)
    else:
        print('NOTE: no recordings yet: the lines are timed by hand and silent (Sam is recording them).')
    if any('pokemon' in c[2].lower().replace('é', 'e') for c in CAPS) or any(
            'pokemon' in ln['text'].lower() for ln in LINES):
        faults.append('the word Pokemon is used (Sam: never; only Poker Mon)')
    mix, voice, rest = soundtrack(stems=True)
    for q in filmkit.sound_questions({'voice': voice, 'background': rest, 'mix': mix}, SR,
                                     cuts=[a for _, a, _ in SHOTS[1:]], end=BLACK_AT):
        print('QUESTION FOR SAM:', q)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


def audits():
    """The general audit: player one and player two alone over every frame they are on screen (shots 1-5)."""
    def alone(who):
        def draw(t):
            lay = Image.new('RGBA', (B.W * B.SS, B.H * B.SS), (0, 0, 0, 0))
            sh = shot_of(t)
            if who == 'P1':
                cam = B.Cam(1.0, 540, 960)
                sp = dict(C.P1)
                sp.update(p1_face(t))
                u = (t - LAY[0]) / (LAY[1] - LAY[0])
                C.person(lay, cam, S1['x'] + idle_x('P1', t), S1['neck'], S1['s'], sp, t, 0,
                         seated(sp, 'hold', min(1.0, max(0.0, u))))
            else:
                cam = B.Cam(1.0, 540, 960)
                sp = dict(C.P2)
                sp.update(p2_face(t))
                C.person(lay, cam, S3['x'] + idle_x('P2', t), S3['neck'], S3['s'], sp, t, 0, seated(sp, 'fan'))
            return lay
        return draw
    actors = {}
    for who, shots in (('P1', ('p1', 'lit')), ('P2', ('p2', 'reveal'))):
        for shot, a, b in SHOTS:
            if shot in shots:
                ts = [i / FPS for i in range(int(math.ceil(a * FPS)), int(b * FPS))]
                actors[f'{who} [{shot}]'] = (ts, alone(who))
    faults = filmkit.silhouette_audit(actors, fps=FPS, still_ok=())
    faults += moves.audit()
    return faults


# ------------------------------------------------------------------------------------------------ sheets
def label(img, x, y, txt, size=30):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), size)
    d.text((x, y), txt, font=f, fill=(250, 250, 250), stroke_width=3, stroke_fill=(20, 20, 20))


def cast_sheet(out):
    """Everyone standing, with the body landmarks and a scale person; the Dragonite at rest, charging and firing;
    the cards and chips."""
    import landmarks
    import sizes
    B.SS = 1
    sheet = Image.new('RGB', (2160, 1920 + 760), (40, 34, 30))
    a = B.canvas((214, 196, 150))
    cam = B.Cam(1.0, 540, 960)
    for i, n in enumerate(C.PEOPLE):
        sp = C.PEOPLE[n]
        C.person(a, cam, 140 + (i % 4) * 270, 230 + (i // 4) * 900, 0.62, sp, 0.0, 0, C.pose_standing(sp))
    d = ImageDraw.Draw(a)
    landmarks.draw(d, 540, 230, 0.62, 1000)
    sheet.paste(a.convert('RGB'), (0, 0))
    for i, n in enumerate(C.PEOPLE):
        label(sheet, 20 + (i % 4) * 270, 120 + (i // 4) * 900, n, 26)
    b = B.canvas((214, 196, 150))
    C.dragonite(b, cam, 290, 900, 0.5, turn=0.35)
    C.person(b, cam, 600, 900 - 928 * 0.5, 0.5, C.P2, 0.0, 0, C.pose_standing(C.P2))
    m = C.dragonite(b, cam, 290, 1800, 0.5, turn=0.35, head=-34, mouth_open=0.9, eyes='narrow', wings=0.65, arms=0.35)
    C.glow(b, cam, [(m[0], m[1], 50)])
    m = C.dragonite(b, cam, 800, 1800, 0.5, turn=0.35, head=16, lean=10, mouth_open=1.0, eyes='narrow', wings=1.0,
                    arms=1.0)
    C.glow(b, cam, [(m[0] + 22 * k, m[1] + 30 * k, 40) for k in range(20)])
    sheet.paste(b.convert('RGB'), (1080, 0))
    label(sheet, 1100, 20, 'Dragonite (2.2 m) beside P2 (1.85 m)', 26)
    label(sheet, 1100, 980, 'charging        firing', 26)
    row = Image.new('RGBA', (2160, 760), (34, 112, 72, 255))
    for i, suit in enumerate('SCDH'):
        row.alpha_composite(C.card_face('Q', suit).resize((350, 490)), (20 + 370 * i, 30))
    row.alpha_composite(C.card_back().resize((350, 490)), (1500, 30))
    for i, k in enumerate(C.CHIPS):
        row.alpha_composite(C.chip_face(k, 150), (1880 + (i % 2) * 140, 40 + (i // 2) * 170))
    for i, (r_, s_) in enumerate((('7', 'C'), ('2', 'D'), ('9', 'S'), ('4', 'H'), ('J', 'C'))):
        row.alpha_composite(C.card_face(r_, s_, 60).resize((120, 168)), (20 + 130 * i, 560))
    sheet.paste(row.convert('RGB'), (0, 1920))
    label(sheet, 20, 1930, 'Poker Mon Queens, the back, P2\'s hand, Poke Ball chips', 26)
    sheet.save(out, quality=88)


def LINE_SUBJECTS():
    """Each of the cast alone, large, for the line-work check (linecheck.py); the Dragonite too."""
    out = []
    for who in C.PEOPLE:
        def d(im, who=who):
            sp = C.PEOPLE[who]
            C.person(im, B.Cam(1.0, 540, 960), 540, 420, 1.45, sp, 0.0, 0, C.pose_standing(sp))
        out.append((who, d))
    out.append(('DRAGONITE', lambda im: C.dragonite(im, B.Cam(1.0, 540, 960), 540, 1750, 1.0, turn=0.25)))
    return out


def stills_sheet(out, times, w=360):
    B.SS = 1
    h = w * 16 // 9
    cols = min(6, len(times))
    rows = (len(times) + cols - 1) // cols
    sheet = Image.new('RGB', (w * cols, (h + 40) * rows), (20, 20, 20))
    for i, t in enumerate(times):
        im = frame_image(t).convert('RGB').resize((w, h), Image.LANCZOS)
        x, y = w * (i % cols), (h + 40) * (i // cols)
        sheet.paste(im, (x, y + 40))
        label(sheet, x + 10, y + 4, f'{t:.1f}s {shot_of(t)}', 24)
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
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None)


F.guard(B)   # every arm drawn is measured against the rig; a wrong one stops the render
import limbs                     # noqa: E402
limbs.install(B)                 # natural arms and legs

if __name__ == '__main__':
    main()
