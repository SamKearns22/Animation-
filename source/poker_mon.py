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
    dict(n=1, who='P1', text='Four of a kind.', audio='poker-mon-1', start=0.55, end=3.0),   # start: where the recording's file begins (it opens with a second of room tone)
    dict(n=2, who='P2', text='Dragonite, use hyper beam.', audio='poker-mon-2', start=5.76, end=7.7),
]
SHOTS = [('p1', 0.0, 3.6), ('cards', 3.6, 4.7), ('p2', 4.7, 9.5), ('reveal', 9.5, 14.0), ('lit', 14.0, 15.5),
         ('blast', 15.5, R.Clock.END)]
DUR = BLACK_AT = R.Clock.END
LAY = (0.5, 1.5)          # player one lays his hand: the fan leaves his hand, the cards spread on the felt
LOOK_DOWN = (4.9, 6.25)   # player two inspects his hand: looks down, one brow rises (a bad hand), looks up
CHARGE = (R.Clock.CHARGE0, 15.6)   # after 1.5 s looking neutral (Sam): head back, the light grows in its mouth
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
LINE_OK = [('GUARD1', 'edge with no line', 566, 106), ('MAGNATE', 'edge with no line', 567, 105)]   # the shine on his bald head: a flat highlight, the kit's own
TABLE_Y = 300             # a seated player's edge of the table, in their own units (neck at 0)
# ====================================================================================================================

for ln in LINES:                                  # time each line to its recording when there is one
    ln['_voice'], ln['_stretches'] = None, [(0.0, ln['end'] - ln['start'])]
    if ln.get('audio') and os.path.exists(os.path.join(HERE, 'audio', ln['audio'] + '.m4a')):
        v = MA.line(ln['audio'])
        ln['_voice'], ln['end'] = v, ln['start'] + len(v) / SR
        ln['_stretches'] = MA.pauses(v, 0.12)
for ln in LINES:                                  # when the words are actually spoken (the file has quiet at each end)
    ln['_say'] = (ln['start'] + ln['_stretches'][0][0], ln['start'] + ln['_stretches'][-1][1])
TRACK = {w: [(a + ln['start'], b + ln['start'], sh) for ln in LINES if ln['who'] == w
             for a, b, sh in mouths.track(ln['text'], ln['_stretches'])] for w in ('P1', 'P2')}
BLINKS = {'P1': [b for b in F.blinks(5, 0.6, 16.0, talking=True) if not 1.7 < b < 3.4],
          'P2': [b for b in F.blinks(9, 4.8, 21.0, talking=True) if not 9.0 < b < 10.1 and not LOOK_DOWN[0] < b < LOOK_DOWN[1] + 0.4]}
# Subtitles: short chunks, each on its first word; the punchline on its own.
CAPS = [(LINES[0]['_say'][0] - 0.05, LINES[0]['_say'][1] + 0.4, 'Four of a kind.'),
        (LINES[1]['_say'][0] - 0.05, min(SHOTS[3][1], LINES[1]['_say'][1] + 0.3), 'Dragonite, use hyper beam.')]


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
            V.arm_to(j, sd, (sg * 15, 70.0, 250.0), 'down', 'fist')      # both hands together at the fan's foot, at his
                                                                         # chest, well clear of the table (Sam: held)
    elif kind == 'pull':
        for sd, sg in (('L', -1), ('R', 1)):
            z = 330.0 - 110 * u
            V.arm_to(j, sd, (sg * (110 - 40 * u), TABLE_Y + 60, z), 'down', 'palm')
    return j


CARD_U = 0.063 / V.M_PER_UNIT      # a card's width in person units (real size, Sam: never oversized)
CHIP_U = 0.0195 / V.M_PER_UNIT     # a chip's radius
SPREAD = dict(chest=(40.0, 190.0, 170.0), start=(-60.0, TABLE_Y + 46, 300.0), end=(80.0, TABLE_Y + 46, 300.0),
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
    draw.held = True               # held in a hand: views.person refuses it unless the gripping hand is drawn over it
    return draw


# ------------------------------------------------------------------------------------------------ light
def light_level(t):
    """How bright the Hyper Beam's light is on everyone: the charge grows it, the blast peaks it, then it fades."""
    if t < CHARGE[0] + 0.4:
        return 0.0
    if t < FIRE:
        return 0.8 * ease((t - CHARGE[0] - 0.4) / (FIRE - CHARGE[0] - 0.4)) ** 1.2   # brighter (Sam, 19 Oct)
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
    out['mouth'] = m or ('pleased' if t > LINES[0]['_say'][1] else 'line')
    if t > LINES[0]['_say'][1]:
        out.update(brows='confused', lid=4)                    # the smug look: one brow up, heavy lids
    if t >= SHOTS[4][1]:                                       # lit by the glow: the smirk goes, then alarm
        k = (t - SHOTS[4][1]) / (SHOTS[4][2] - SHOTS[4][1])
        out.update(brows='confused' if k < 0.35 else 'alarm', lid=4 if k < 0.35 else 0,
                   mouth='pleased' if k < 0.35 else 'agape', look=0.0)
    return out


# ------------------------------------------------------------------------------------------------ shot 2: the cards
# ------------------------------------------------------------------------------------------------ shots 3-4: player two
S3 = dict(x=720, neck=1010, s=1.15)
DRAGON = dict(x=-60, foot=1560, s=0.84)


def p2_face(t):
    sh = filmkit.shifts(t, seed=202, amount=1.0)
    out = dict(look=0.0, blink=F.blinking(t, BLINKS['P2']), head_dx=3 * sh, head_dy=8, mouth='line', brows='serious')
    if LOOK_DOWN[0] <= t < LOOK_DOWN[0] + 0.65:                # eyes all the way down to his cards (Sam, 19 Oct)
        out.update(lid=7, head_dy=26, look_v=1.0)
    elif LOOK_DOWN[0] + 0.65 <= t < LOOK_DOWN[1]:              # then across the table at his opponent, heavy-lidded
        out.update(lid=7, head_dy=16)                          # (Sam liked this look)
    if LOOK_DOWN[0] + 0.65 <= t < LOOK_DOWN[1] + 0.35:         # one eyebrow up: a bad hand; it stays up a moment
        out['brows'] = 'confused'                              # as he settles
    m = talking_mouth('P2', t)
    if m:
        out['mouth'] = m
    return out


def fire_eyes(t):
    """Sam's pick from the eye sheet (19 Oct): 4 'aim' for the first half of the beam, 6 'puppy' for the second."""
    return 'aim' if t < (FIRE + BEAM_END[0]) / 2 else 'puppy'


def dragon_state(t):
    """The Dragonite's head, mouth, eyes, wings and arms over the film. Its mouth is only ever closed (the plain muzzle
    of Sam's photo) or the round O of the Hyper Beam, never a jaw working up and down (Sam, 19 Oct). Closed when we
    first see it; a small O once the charge is under way; wide open only as it blasts (Sam, 19 Oct)."""
    st = dict(head=0.0, mouth_open=0.0, eyes='open', wings=0.15, arms=0.0, lean=0.0, ball=0.0, shape='jaw')
    if t >= CHARGE[0]:                                          # charging: head back, then a small O, light growing
        k = ease((t - CHARGE[0]) / 0.7)
        st.update(head=-18 * k, eyes='soft' if k > 0.3 else 'open', wings=0.15 + 0.5 * k, arms=0.35 * k)
        if t >= CHARGE[0] + 0.6:
            st.update(mouth_open=0.12, shape='o')
        st['ball'] = ease((t - CHARGE[0] - 0.6) / (FIRE - CHARGE[0] - 0.6))
    if t >= FIRE - 0.12:                                        # the head snaps forward and down (fast): firing
        k = min(1.0, (t - (FIRE - 0.12)) / 0.12)
        st.update(head=-18 + 30 * k, lean=8 * k, mouth_open=1.0, shape='o', wings=0.65 + 0.35 * k,
                  arms=0.35 + 0.65 * k, eyes=fire_eyes(t) if k > 0.5 else 'soft')
    if t >= BEAM_END[1]:                                        # done: the smile back at once; settles, pleased
        k = ease((t - BEAM_END[1]) / 0.6)
        st.update(head=12 * (1 - k), lean=8 * (1 - k), mouth_open=0.0, shape='jaw', wings=1.0 - 0.85 * k,
                  arms=1.0 - k, eyes='arc' if k > 0.5 else 'soft', ball=0.0)     # a happy closed-eye smile
    return st


# ------------------------------------------------------------------------------------------------ shot 6: the blast
def shot_blast(img, t):
    """The parlour from a high corner, sweeping; the beam swept round the table (poker_mon_room)."""
    R.shot(img, t, sys.modules[__name__])


# ------------------------------------------------------------------------------------------------ the film
def cam_p1(t):
    """Shot 1: close across the table on player one, so his Poker Mon cards and chips read (Sam, 19 Oct: shot one
    closer, the concept was missed), a slow push in through his line. Shot 5 (lit): from player two's seat, pushing in."""
    if t < SHOTS[4][1]:
        k0 = ease(t / SHOTS[0][2])
        return R.Cam3((0.62, 1.3, -0.22), (1.42, 0.9 + 0.05 * k0, 0.04), focal=1050.0 + 220.0 * k0)
    k = ease((t - SHOTS[4][1]) / 1.2)
    look, f = (1.55 + 0.15 * k, 0.95 + 0.25 * k, 0.0), 2400.0 + 2200.0 * k
    return R.Cam3((-0.95, 1.7, -0.35), look, focal=f)


def cam_cards(t):
    """Shot 2: down on player one's Queens, his chips and his whisky beside them."""
    k = ease((t - SHOTS[1][1]) / (SHOTS[1][2] - SHOTS[1][1]))
    return R.Cam3((1.05, 1.08, -0.66), (1.31, 0.86, 0.14), focal=1500.0 + 150.0 * k)


def cam_p2(t):
    """Shots 3 and 4: player two from player one's seat; then the shot widens to show the Dragonite beside him."""
    look, f = (-1.74, 1.1, -0.05), 5200.0
    if t >= SHOTS[3][1] + 0.25:
        k = ease((t - SHOTS[3][1] - 0.25) / 1.3)
        look = (-1.74 - 0.25 * k, 1.1 + 0.3 * k, -0.05 + 0.55 * k)
        f = 5200.0 + (1450.0 - 5200.0) * k
    return R.Cam3((1.5, 1.28, -0.25), look, focal=f)


def picture(t):
    """The frame WITHOUT captions or Hook Text. One set for the whole film (Sam, 19 Oct): every shot is a camera on
    the same parlour, table and things (poker_mon_room.render)."""
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    img = B.canvas(WALL)
    sh = shot_of(t)
    me = sys.modules[__name__]
    fill = [(540, 900, 1100, 0.5, (255, 214, 160))]   # the lamp over the table is out of frame in shots 1 and 2:
    if sh in ('p1', 'lit'):                            # its light still falls on them (Sam, 19 Oct: shot 2 was darker)
        extra = [(540, 820, 760, 0.9 * light_level(t), (255, 236, 170))] if sh == 'lit' else fill
        R.render(img, t, me, cam_p1(t), extra)
    elif sh == 'cards':
        R.render(img, t, me, cam_cards(t), fill)
    elif sh in ('p2', 'reveal'):
        R.render(img, t, me, cam_p2(t))
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
    m = min(n - a, int((t_end - t0 + 2.0) * SR))
    tt = np.arange(m) / SR
    noise = rng.standard_normal(m)
    k = np.exp(-np.linspace(0, 1, 40))
    low = np.convolve(noise, k / k.sum(), mode='same')
    boom = np.sin(2 * np.pi * np.cumsum(55 - 25 * np.minimum(tt, 1)) / SR) * np.exp(-tt * 2.2)
    roar_env = np.clip((t_end - t0 - tt) / 0.4, 0, 1) * np.minimum(1, tt / 0.03)
    from scipy.signal import butter, sosfilt         # the roar's grit kept under 2.5 kHz: raw white noise hisses
    grit = sosfilt(butter(4, 2500, 'low', fs=SR, output='sos'), noise)
    roar = (0.6 * low + 0.15 * grit) * roar_env + 0.2 * np.sin(2 * np.pi * 180 * tt) * roar_env
    out[a:a + m] = 0.9 * boom + 0.5 * roar + 0.5 * low * np.exp(-tt * 1.5)
    return out


def glass_break(n, t0):
    """The window going (Sam, 19 Oct: "a tinkling glass"): a short bright crash, then shards tinkling down for about
    a second and a half, each a quick high ping. Every part is short and decays: never a steady noise (no hiss)."""
    from scipy.signal import butter, sosfilt
    rng = np.random.default_rng(9)
    out = np.zeros(n)
    a = int(t0 * SR)
    m = min(n - a, int(0.35 * SR))
    if m <= 0:
        return out
    tt = np.arange(m) / SR
    crash = sosfilt(butter(4, [1800, 7000], 'band', fs=SR, output='sos'), rng.standard_normal(m))
    out[a:a + m] += 0.5 * crash * np.exp(-tt * 14)
    for i in range(34):                                       # the tinkles: shards landing, thinning out
        s0 = a + int((0.05 + 1.5 * rng.uniform(0, 1) ** 1.6) * SR)
        L = int(0.09 * SR)
        if s0 + L >= n:
            continue
        u = np.arange(L) / SR
        f = rng.uniform(3200, 7200)
        ping = (np.sin(2 * np.pi * f * u) + 0.4 * np.sin(2 * np.pi * f * 1.51 * u)) * np.exp(-u * 55)
        out[s0:s0 + L] += ping * rng.uniform(0.04, 0.12)
    return out


def gasp(n, t0):
    """The young man's gasp at the four Queens (Sam, 19 Oct): a quick sharp breath in, breathy and voiced a little,
    rising, a third of a second, never a steady noise. Made in code; a recording of Sam's ("S1 gasp") would replace it."""
    from scipy.signal import butter, sosfilt
    rng = np.random.default_rng(31)
    out = np.zeros(n)
    a = int(t0 * SR)
    m = min(n - a, int(0.38 * SR))
    tt = np.arange(m) / SR
    breath = sosfilt(butter(2, [700, 2600], 'band', fs=SR, output='sos'), rng.standard_normal(m))
    env = np.minimum(1, tt / 0.04) * np.exp(-np.maximum(0, tt - 0.08) * 9)
    voice = np.sin(2 * np.pi * np.cumsum(260 + 160 * tt / 0.38) / SR) * 0.25
    out[a:a + m] = (breath * 0.35 + voice * 0.12) * env
    return out


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)        # no room tone: white noise under a film comes up as a hiss (Sam, 19 Oct)
    for ln in LINES:
        if ln['_voice'] is not None:
            s = int(ln['start'] * SR)
            seg = ln['_voice'][:max(0, n - s)]
            voice[s:s + len(seg)] += seg
    rest += hum(n, CHARGE[0] + 0.1, FIRE)
    rest += gasp(n, R.GASP[0] + 0.05)                  # Sam asked for it (19 Oct)
    rest += blast(n, FIRE, BEAM_END[1])
    win = R.through_window(dragon_state(FIRE + 0.05))
    if win:
        rest += glass_break(n, win[4])                     # Sam asked for it (19 Oct)
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
    faults += filmkit.hiss_check(mix, SR, BLACK_AT)
    for q in filmkit.sound_questions({'voice': voice, 'background': rest, 'mix': mix}, SR,
                                     cuts=[a for _, a, _ in SHOTS[1:]], end=BLACK_AT):
        print('QUESTION FOR SAM:', q)
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


THING_R = dict(chip=0.0195, card=0.045, tumbler=0.04, napkin=0.07, flute=0.035, martini=0.05, ashtray=0.06,
               cigarbox=0.1, pad=0.08, shoe=0.1, button=0.025, tray=0.2, candelabra=0.12, bucket=0.11)
HAND_R = 0.05      # a hand resting on the felt, in metres


def hit_check():
    """Nobody is thrown before the beam touches them (Sam, 19 Oct: the woman in red flipped up into the air before
    it reached her). At each person's hit, in the blast camera, the drawn beam must overlap them on screen."""
    faults = []
    d = dragon_state(FIRE + 0.05)
    for (kind, who), h in R.blast_hits(d).items():
        if kind == 'T':                                      # a thing on the table: the beam within reach of it
            x, z = R.THINGS[who][1]
            m, dr = R.beam_ray(h[0], d)
            dd, _ = R.dist_to_ray((x, R.TABLE_H + 0.03, z), m, dr, R.beam_end(m, dr)[1])
            if dd > R.THING_HIT_R * 1.05:
                faults.append(f'a {R.THINGS[who][0]} at ({x:.2f}, {z:.2f}) flies at {h[0]:.2f} s with the beam '
                              f'{dd:.2f} m away')
            continue
        if kind != 'P':
            continue
        t = h[0]
        cam = R.sweep_cam(t)
        x, neck, z = h[3]
        body = (x, neck - 0.25, z)
        if cam.depth(body) < 0.5:
            continue
        (px, py), k = cam.project(body)
        m, dr = R.beam_ray(t, d)
        end, _ = R.beam_end(m, dr)
        (ax, ay), km = cam.project(m)
        (bx, by), _ = cam.project(end)
        vx, vy = bx - ax, by - ay
        u = max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / max(1e-6, vx * vx + vy * vy)))
        gap = math.hypot(ax + vx * u - px, ay + vy * u - py)
        reach = 0.3 * k + 0.13 * km                          # half a body plus the beam's drawn half-width
        if math.hypot(end[0] - x, end[2] - z) < R.END_R:     # the blast where the beam meets the wall, beside them
            continue
        if gap > reach * 1.25:
            faults.append(f'{who} is thrown at {t:.2f} s with the beam {gap:.0f} px away on screen (touching is '
                          f'{reach:.0f} px)')
    return faults


def table_check():
    """One table plan, nothing inside anything (Sam, 19 Oct: the table well populated, never clipping): no two things
    on the table overlap (cards may), and nothing stands on a chip stack."""
    faults = []
    big = [(k, xz) for k, xz, ex in R.THINGS if k != 'chip']
    for a in range(len(big)):
        for b in range(a + 1, len(big)):
            (k1, p1), (k2, p2) = big[a], big[b]
            if k1 == 'card' and k2 == 'card':
                continue
            if math.dist(p1, p2) < 0.8 * (THING_R.get(k1, 0.05) + THING_R.get(k2, 0.05)):
                faults.append(f'table plan: a {k1} at {p1} and a {k2} at {p2} overlap')
    for k, (x, z), ex in R.THINGS:                       # everything on the table top, never past its edge in
        if (x / R.TABLE_A[0]) ** 2 + (z / R.TABLE_A[1]) ** 2 > 0.97:     # the air (Sam, 19 Oct: a glass floated)
            faults.append(f'table plan: a {k} at ({x:.2f}, {z:.2f}) is past the table\'s edge, in mid-air')
    stacks = [xz for k, xz, ex in R.THINGS if k == 'chip' and not ex.get('loose')]
    for k, xz in big:
        if k not in ('card', 'tray') and any(math.dist(xz, c) < THING_R.get(k, 0.05) + 0.0195 for c in stacks):
            faults.append(f'table plan: a {k} at {xz} sits on a chip stack')
    return faults


def clearance_check():
    """Nothing passes through anything (Sam, 19 Oct: player one's resting hand sat in his chip stacks): each hand
    resting on the felt keeps clear of every thing on the table (sizes in THING_R)."""
    faults = []
    rests = {'R': (R.P1_REST_X, R.P1_REST_Z), 'L': (R.P1_REST_X, -R.P1_REST_Z)}
    for sd, (hx, hz) in rests.items():
        for kind, (x, z), ex in R.THINGS:
            gap = math.hypot(hx - x, hz - z) - HAND_R - THING_R.get(kind, 0.05)
            if gap < 0.03:
                faults.append(f"player one's resting {sd} hand at ({hx:.2f}, {hz:.2f}) goes into a {kind} at "
                              f"({x:.2f}, {z:.2f})")
    return sorted(set(faults))


def hands_check():
    """Hands that touch something must be seen touching it (Sam, 19 Oct: player two's hands were hidden under the
    table as he drew in the pot, then player one's as he laid his Queens, and nothing caught either). On frames of the
    lay and of the pull, the patch of picture at each hand on the felt must be that hand, not the felt or the rail."""
    faults = []
    keep = B.SS
    B.SS = 1
    c = R.Clock
    frames = [(float(t), 'P1', 'R') for t in np.linspace(LAY[0] + 0.45 * (LAY[1] - LAY[0]), LAY[1] - 0.05, 4)]
    frames += [(float(t), 'P1', 'L') for t in (LAY[0] + 0.3, 3.0)]
    frames += [(float(t), 'P2', sd) for t in np.linspace(c.PULL[0] + 0.05, c.PULL[1] - 0.05, 4) for sd in 'LR']
    names = {'P1': 'player one', 'P2': 'player two'}
    cache = {}
    for t, who, sd in frames:
        if t not in cache:
            cache[t] = (np.asarray(picture(t).convert('RGB')).astype(int), dict(R.DRAWN))
        im, drawn = cache[t]
        if who not in drawn:
            faults.append(f'{names[who]} is not drawn at {t:.2f} s (hand check)')
            continue
        X, Y, s, yaw, mirror, j, j2 = drawn[who]
        wx, wy = j2['wr' + sd]
        px, py = int(X + s * wx * (-1 if mirror else 1)), int(Y + s * wy)
        patch = im[max(0, py - 4):py + 5, max(0, px - 4):px + 5]
        felt = ((patch[..., 1] > patch[..., 0] + 10) | (patch.sum(-1) < 140)).mean()
        if felt > 0.5:
            faults.append(f"{names[who]}'s {sd} hand is hidden at {t:.2f} s (the table is drawn over it)")
    B.SS = keep
    return faults


def contact_check():
    """Every touch is real (Sam, 19 Oct: the pot slid to him with no hand on it). Through player one's lay and
    player two's put-down, reach and pull, every hand must reach what it is meant to touch (never stopped short at the
    end of the arm: poker_mon_room.CONTACT_FAULTS), and the pot may only move while his hands are on it."""
    keep = B.SS
    B.SS = 1
    R.CONTACT_FAULTS.clear()
    c = R.Clock
    times = list(np.linspace(LAY[0], LAY[1], 6)) + list(np.linspace(c.PUTDOWN[0], c.RELEASE[0], 10))
    for t in times:
        picture(float(t))
    faults = [f'{who}: {what} at {t:.2f} s' for t, who, what in R.CONTACT_FAULTS]
    for t in np.linspace(c.TOPPLE[0], c.END, 60):          # the pile moves only between the start and end of the pull
        moving = abs(R.grip(t + 0.004)[0] - R.grip(t)[0]) > 1e-7
        if moving and not (c.PULL[0] - 0.005 <= t <= c.PULL[1]):
            faults.append(f'the pot moves at {t:.2f} s with no hands on it')
    B.SS = keep
    return faults


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
    faults += hands_check()
    faults += clearance_check()
    faults += table_check()
    faults += hit_check()
    faults += contact_check()
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
