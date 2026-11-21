#!/usr/bin/env python3
"""gta_shots58: Grand Theft Autism shots 5-8 (plan rows 5-8), built on shot 4's world (gta_rehearse.world4's parts)
in a file of their own so chat 17's shot 4 work is never touched (Sam's Y, chat 16).

MAP
  ZC, R_T .......... the corner: shot 4's street (A, along z) meets the new main road (B, along +x) at z = ZC, a T
  to_local/camB .... B is drawn as a second shop strip in its own frame (x' across, z' along): the camera is turned
                     into that frame, so every strip piece (ground, shops, palms, people) is reused unchanged
  path/tulip58 ..... the Tulip from shot 4's end: brakes, Lucia yanks the wheel, slides right round the corner onto B
  chaser58 ......... cruisers 2 and 3 follow the same path, a gap behind, closing in from shot 6 to shot 8
  crowd_b .......... B's passers-by: walk or watch, heads turn to the chase as it roars past
  ground58 ......... A's ground, the junction mouth cut out of A's east pavement, B's road, kerbs and pavements
  inside58 ......... all three in their seats (Jason too, gun flat on his chest): acting keys per line (lines 3-6)
  world58 .......... one frame at world time t (shot 4's clock: shot 5 starts at 6.2)
  cam6 ............. shot 6's closer two-shot through the windscreen
  SHOTS58 .......... shot 5-8 frame functions, their world start times and lengths

    python3 source/gta_shots58.py still SHOT T OUT.jpg     one frame (T in the shot's own seconds)
    python3 source/gta_shots58.py clip SHOT OUT.mp4        one shot as a clip
    python3 source/gta_shots58.py layers|bodies SHOT.. [--every K]   rule 17's checks
"""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gta_rehearse as R         # noqa: E402  shot 4's world: street pieces, cars, cast, effects
import sets as S                 # noqa: E402
import gta_cars as G             # noqa: E402
import gta_cast as GC            # noqa: E402
B, V, PC, FX = R.B, R.V, R.PC, R.FX
smooth, bump = R.smooth, R.bump

# Shots 5-8 keep their own clock u (shot 5 starts at u = 6.2, every timing below is on it). Shot 4 is now longer (8.2 s,
# chat 23), so shot 5 starts SH seconds later on shot 4's clock and the car is S_OFF metres further up the street:
# the corner moves up the street by S_OFF and everything of shot 4's world is read at u + SH (21 Nov, Sam: shot 5 had
# vanished: the braking and the corner were timed for the old, shorter shot 4).
T5 = 6.2
SH = R.SHOT4_LEN - T5
S_OFF = R.V4 * SH
ZC, R_T = 116.0 + S_OFF, 6.0             # the T junction's middle (z) and the corner's radius
S0 = ZC - 5.0 - R_T              # path distance (= z on A) where the arc starts
ARC = math.pi / 2 * R_T


# ------------------------------------------------------------------------------------------------ road B's frame
def to_local(p):
    """World (x, y, z) -> B's own strip frame (x' across, y, z' along B): B is a strip like A, turned a quarter."""
    return (ZC - p[2], p[1], p[0])


def to_world(q):
    return (q[2], q[1], ZC - q[0])


def camB(cam):
    c = S.Cam(to_local(cam.pos), to_local(cam.at), cam.focal, cam.shake, cam.roll)
    return c


def _strip_b():
    rng = np.random.RandomState(91)
    cols = [(244, 204, 214), (186, 222, 232), (250, 230, 176), (204, 196, 238), (246, 196, 166), (196, 232, 206),
            (238, 232, 218), (232, 190, 222)]
    blocks, people, palms = [], [], []
    for side in (-1, 1):
        z = 10.0
        while z < 470:
            w = rng.uniform(9, 17)
            blocks.append(dict(side=side, z0=z, z1=z + w, h=rng.uniform(5.0, 11.0), col=cols[rng.randint(len(cols))],
                               awn=cols[rng.randint(len(cols))], seed=int(rng.randint(1 << 20))))
            z += w
        z = 12.0
        while z < 440:
            z += rng.uniform(3.0, 9.0)
            people.append(dict(at=(side * rng.uniform(8.2, 9.5), z), face=rng.choice([0.0, 180.0, 90.0 * -side]),
                               i=1000 + len(people), walk=rng.uniform(0, 1)))
    for k, z in enumerate(np.arange(18.0, 460, 21.0)):
        for s in (-1, 1):
            if (k + (s > 0)) % 2 == 0:
                palms.append(((7.6 if s < 0 else 9.2) * s, z))
    return blocks, people, palms


BLOCKS_B, PEOPLE_B, PALMS_B = _strip_b()


def _trim_a():
    """A's east side loses what stands where B's mouth and corner blocks are (z within ZC +- 24 behind x = 10)."""
    out = []
    lo, hi = ZC - 24.0, ZC + 24.0
    for b in R.BLOCKS4:
        if b['side'] < 0 or b['z1'] <= lo or b['z0'] >= hi:
            out.append(b)
            continue
        if b['z0'] < lo:
            out.append(dict(b, z1=lo))
        if b['z1'] > hi:
            out.append(dict(b, z0=hi))
    people = [pp for pp in R.PEOPLE4 if not (pp['at'][0] > 0 and abs(pp['at'][1] - ZC) < 13)]
    palms = [(x, z) for x, z in R.PALMS4 if not (x > 0 and abs(z - ZC) < 11)]
    return out, people, palms


BLOCKS_A, PEOPLE_A, PALMS_A = _trim_a()


# ------------------------------------------------------------------------------------------------ the Tulip's path
def path(s):
    """(x, z, heading) on the path at distance s: north up A's outer lane (s = z), the arc, east down B's outer lane."""
    if s < S0:
        return R.LANE4, s, 0.0
    if s < S0 + ARC:
        a = (s - S0) / R_T
        return R.LANE4 + R_T - R_T * math.cos(a), S0 + R_T * math.sin(a), math.degrees(a)
    return R.LANE4 + R_T + (s - S0 - ARC), ZC - 5.0, 90.0


def _speed(t):
    return R.V4 - 6.5 * bump(t, 6.22, 6.62, 7.55)      # brakes hard into the corner, floors it out


def _s_table():
    dt = 1 / 480.0
    ts, ss = [T5], [R.V4 * T5 + S_OFF]
    while ts[-1] < 23.5:
        ts.append(ts[-1] + dt)
        ss.append(ss[-1] + _speed(ts[-1]) * dt)
    return np.array(ts), np.array(ss)


_TS, _SS = _s_table()


def s_at(t):
    if t <= T5:
        return R.V4 * t + S_OFF
    return float(np.interp(t, _TS, _SS))


def _lateral(x, z, head, off):
    """A point `off` metres to the left of the path at (x, z) heading `head`."""
    h = math.radians(head)
    return x - off * math.cos(h), z + off * math.sin(h)


def drift(s, k=1.0):
    """The back end sliding out round the corner: yaw ahead of the heading, caught with a flick after."""
    return k * (24.0 * bump(s, S0 - 1.0, S0 + ARC * 0.7, S0 + ARC + 7.0)
                - 7.0 * bump(s, S0 + ARC + 3.0, S0 + ARC + 7.0, S0 + ARC + 13.0))


def wheel58(t):
    """Lucia's wheel (deg, + right): the yank as the arc starts, held, unwound, a catch the other way."""
    s = s_at(t)
    return 120.0 * bump(s, S0 - 2.4, S0 + 0.6, S0 + ARC + 1.0) - 34.0 * bump(s, S0 + ARC, S0 + ARC + 3.5, S0 + ARC + 9.0)


def throw(t):
    """How hard everyone is thrown toward the car's left (0..1): the corner's pull, a beat behind the wheel."""
    s = s_at(t - 0.08)
    return bump(s, S0 - 0.8, S0 + ARC * 0.55, S0 + ARC + 6.0)


def tulip58(t):
    s = s_at(t)
    x, z, head = path(s)
    wob = 0.10 * math.sin((t + SH) * 1.7) * (1 - smooth((t - T5) / 0.4))    # shot 4's weave, settling as she brakes
    x += wob
    w = wheel58(t)
    th = throw(t)
    car = G.Car('tulip', pos=(x, z), yaw=head + drift(s), roll=0.7 * math.sin(t * 2.3) - 6.5 * th, pitch=0.5 - 1.8 * bump(t, 6.2, 6.45, 6.9),
                spin=s / 0.34, steer=0.28 * w)
    car.wheel = w
    car.open_windows = R.OPEN4
    return car


GAP0 = {1: R.GAPS[1], 2: R.GAPS[2]}


def gap(t, i):
    """Cruisers 2 and 3 close in from shot 6 to shot 8: lights growing in the back window (shot 7)."""
    close = {1: 6.8, 2: 8.5}[i]
    return GAP0[i] - close * smooth((t - 12.5) / 6.0)


def chaser58(t, i):
    if t <= T5:
        return R.chaser_at(t + SH, i)
    c0 = R.chaser_at(T5 + SH, i)
    off0 = R.LANE4 - c0.pos[0]                       # in the inner lane after swerving round the crash: back out
    s = s_at(t) - gap(t, i)
    x, z, head = path(s)
    off = off0 * (1 - smooth((t - T5) / 1.1)) + 0.25 * math.sin(t * 1.9 + 2 * i)
    x, z = _lateral(x, z, head, off)
    yaw = head + drift(s, 0.8)
    return G.Car('cruiser', pos=(x, z), yaw=yaw, roll=-5.0 * bump(s, S0 - 0.8, S0 + ARC * 0.55, S0 + ARC + 6.0),
                 pitch=0.4, steer=0.25 * wheel58(t + gap(t, i) / R.V4), spin=s / 0.37)


# ------------------------------------------------------------------------------------------------ B's passers-by
def crowd_b(pp, t):
    """(x', z', facing, joints, head) in B's frame: walkers stroll, watchers face the road; heads turn to the chase."""
    x0, z0 = pp['at']
    side = 1 if x0 > 0 else -1
    walker = pp['walk'] > 0.45
    dirz = 1.0 if pp['face'] == 0.0 else -1.0
    sp = R._walker(pp['i'])
    j = V.standing(sp)
    tz = to_local((*tulip58(t).pos[:1], 0.0, tulip58(t).pos[1]))[2] if t > 7.0 else -50.0
    near = abs(z0 - tz) < 26
    z = z0 + (dirz * R.WALK_V * (t - 3.0) if walker else 0.0)
    F = (0.0, 0.0, dirz) if walker else (-side * 1.0, 0.0, 0.0)
    head = None
    if walker:
        ph = (t + pp['walk'] * 3) * math.pi * 1.9
        R._stride(j, ph, 120.0, 40.0, 70.0)
        j['bob'] = 6 * abs(math.sin(ph))
        for sd in ('L', 'R'):
            fx, fy, fz = j['foot' + sd]
            j['foot' + sd] = (fx, fy - j['bob'], fz)
    if near:
        head = S._norm((R.LANE4 - x0, 0.0, tz - z))
    return x0, z, F, j, head


# ------------------------------------------------------------------------------------------------ the ground
def _q(cam, p, pts, col, line=None, lw=0):
    R._quad(cam, p, pts, col, line, lw)


def ground58(img, cam, cb, p):
    R.strip_ground(img, cam, p)                                        # sky, A's road, pavements, kerbs, lines
    # B's mouth cut out of A's east pavement (drawn in world: x 6.95..10.05, z within ZC +- 7)
    for y in (0.0, 0.155):
        _q(cam, p, [(6.95, y, ZC - 7), (10.05, y, ZC - 7), (10.05, y, ZC + 7), (6.95, y, ZC + 7)], R.ROAD)
    # B in its own frame: road between its kerbs from A's kerb line, pavements and kerbs, lines
    zc = cb.pos[2]
    z_far = max(zc + 1400, 200.0)
    z1 = max(zc + 160, 60.0)
    _q(cb, p, [(-7.0, 0, 7.0), (7.0, 0, 7.0), (7.0, 0, z_far), (-7.0, 0, z_far)], R.ROAD)
    for s in (-1, 1):
        _q(cb, p, [(s * 7.0, 0.15, 7.0), (s * 10.0, 0.15, 7.0), (s * 10.0, 0.15, z1), (s * 7.0, 0.15, z1)], R.PAVE)
        _q(cb, p, [(s * 7.0, 0, 7.0), (s * 7.0, 0.15, 7.0), (s * 7.0, 0.15, z1), (s * 7.0, 0, z1)], R.KERB, R.INK, 1.4)
        _q(cb, p, [(s * 7.03, 0.152, 7.0), (s * 7.25, 0.152, 7.0), (s * 7.25, 0.152, z1), (s * 7.03, 0.152, z1)], R.KERB)
        for z in np.arange(10.5, z1, 1.5):
            if abs(z - zc) < 70:
                cb.line(p, [(s * 7.25, 0.152, z), (s * 10.0, 0.152, z)], (150, 130, 136), 1.0)
    for dx in (-0.12, 0.12):
        _q(cb, p, [(dx - 0.05, 0.01, 10.5), (dx + 0.05, 0.01, 10.5), (dx + 0.05, 0.01, z1), (dx - 0.05, 0.01, z1)], (236, 196, 70))
    for z in np.arange(12.0, z1, 6.0):
        for x in (-3.5, 3.5):
            _q(cb, p, [(x - 0.06, 0.01, z), (x + 0.06, 0.01, z), (x + 0.06, 0.01, z + 3), (x - 0.06, 0.01, z + 3)], (236, 232, 228))


# ------------------------------------------------------------------------------------------------ the three inside
def keys_at(keys, t):
    """Eased value from [(t, value)] keys (numbers or tuples)."""
    if t <= keys[0][0]:
        return keys[0][1]
    for a, b in zip(keys, keys[1:]):
        if a[0] <= t <= b[0]:
            e = smooth((t - a[0]) / (b[0] - a[0]))
            if isinstance(a[1], tuple):
                return tuple(x + (y - x) * e for x, y in zip(a[1], b[1]))
            return a[1] + (b[1] - a[1]) * e
    return keys[-1][1]


def step_at(keys, t):
    v = keys[0][1]
    for k, x in keys:
        if t >= k:
            v = x
    return v


def line(t0, phones):
    """A spoken line: (start, [(time from start, viseme)]) from [(duration, viseme)]."""
    out, u = [], 0.0
    for d, v in phones:
        out.append((u, v))
        u += d
    out.append((u, 'rest'))
    return t0, out


def mouth(t, ln):
    t0, keys = ln
    u = t - t0
    if u < 0 or u > keys[-1][0]:
        return None
    return 'v:' + step_at(keys, u)


def word_at(ln, k):
    """The time the k-th viseme of a line starts (to land acting on a word)."""
    return ln[0] + ln[1][k][0]


# Sam's pace (3.3 words a second); every voice is his to record, these are the timings the mouths follow
LINE3 = line(7.45, [(.14, 'E'), (.14, 'AI'), (.12, 'rest'), (.12, 'AI'), (.08, 'etc'), (.08, 'E'), (.06, 'etc'),
                    (.10, 'etc'), (.08, 'L'), (.14, 'AI'), (.06, 'etc'), (.06, 'etc'), (.14, 'AI'), (.08, 'etc')])
LINE4 = line(9.65, [(.10, 'WQ'), (.10, 'U'), (.08, 'WQ'), (.12, 'AI'), (.06, 'etc'), (.06, 'etc'), (.08, 'U'),
                    (.06, 'etc'), (.10, 'E'), (.08, 'L'), (.08, 'MBP'), (.12, 'E'), (.08, 'WQ'), (.14, 'AI'),
                    (.08, 'WQ'), (.10, 'E'), (.06, 'MBP'), (.06, 'etc'), (.16, 'O'), (.08, 'etc'), (.08, 'etc'),
                    (.10, 'E'), (.06, 'AI'), (.08, 'etc'), (.10, 'E'), (.12, 'etc')])
LINE5 = line(12.15, [(.14, 'AI'), (.06, 'etc'), (.14, 'O'), (.08, 'etc'), (.06, 'WQ'), (.12, 'U'), (.35, 'rest'),
                     (.08, 'etc'), (.10, 'E'), (.06, 'etc'), (.12, 'AI'), (.06, 'MBP'), (.08, 'E'), (.08, 'FV'),
                     (.08, 'E'), (.06, 'etc'), (.10, 'AI'), (.06, 'etc'), (.06, 'E'), (.06, 'etc'), (.08, 'E'),
                     (.06, 'etc'), (.06, 'etc'), (.10, 'O'), (.08, 'MBP'), (.04, 'MBP'), (.12, 'AI'), (.06, 'etc'),
                     (.08, 'E'), (.06, 'etc'), (.06, 'MBP'), (.04, 'L'), (.12, 'O'), (.08, 'etc'), (.06, 'E'),
                     (.06, 'FV'), (.06, 'etc'), (.30, 'rest'),
                     (.06, 'etc'), (.08, 'E'), (.06, 'etc'), (.06, 'etc'), (.12, 'O'), (.06, 'MBP'), (.06, 'WQ'),
                     (.08, 'U'), (.04, 'etc'), (.08, 'etc'), (.04, 'etc'), (.10, 'AI'), (.06, 'FV'), (.06, 'WQ'),
                     (.10, 'E'), (.06, 'etc'), (.06, 'WQ'), (.06, 'E'), (.04, 'etc'), (.10, 'AI'), (.06, 'U'),
                     (.06, 'etc'), (.08, 'etc'), (.12, 'E')])
LINE6 = line(19.20, [(.06, 'MBP'), (.14, 'AI'), (.08, 'etc'), (.10, 'E'), (.06, 'FV'), (.06, 'FV'), (.14, 'U'),
                     (.06, 'etc'), (.08, 'E'), (.06, 'etc'), (.06, 'etc'), (.12, 'AI'), (.06, 'etc'), (.10, 'O'),
                     (.04, 'etc'), (.04, 'L'), (.08, 'E'), (.06, 'etc'), (.06, 'E'), (.06, 'etc'), (.10, 'E'),
                     (.06, 'etc')])
def fit(ln, real):
    """The mouths stretched to the length of Sam's recording of the line (21 Nov), start unchanged."""
    k = real / ln[1][-1][0]
    return ln[0], [(u * k, v) for u, v in ln[1]]


LINE3 = fit(LINE3, 1.20)     # his takes: "Yeah, I didn't like that." 1.20 s
LINE4 = fit(LINE4, 2.24)     # Lucia 2.24 s
LINE5 = fit(LINE5, 5.59)     # Jason 5.59 s (three phrases, two pauses)
LINE6 = fit(LINE6, 1.80)     # "My safe food is nitroglycerin." 1.80 s
TOLD = (word_at(LINE5, 1), word_at(LINE5, 6))         # "told you": his eyes shut
HYPER = word_at(LINE5, 10)                            # "hyperfixation": the free hand opens
EXPLO = word_at(LINE5, 28)                            # "explosives": he counts the point
WITHOUT = word_at(LINE5, 54)                          # "without her": open palm toward her
BROUGHT = word_at(LINE4, 16)                          # "brought": Lucia's nod back at her
NITRO = word_at(LINE6, 10)                            # "nitroglycerin": their eyes slide to each other


def sit(lay, cam, car, who, neck_l, t, hands=(), over=None, head_dir=None, props=(), grip=(), feet_z=0.62, rec=None,
        name=None):
    """One person in a seat (gta_rehearse.seated, plus a gun grip and the body points for the bodies check).
    hands: [(side, point, pole, shape)], point in the car's frame (metres) or ('fig', units) in the person's own."""
    sp = dict(GC.cast()[who], **(over or {}))
    m = sp.get('height', 1.75) / R.FIG_H
    neck = car.body_pt(neck_l)
    F = S._norm(car.body_dir((0, 0, 1)))
    F = S._norm((F[0], 0.0, F[2]))
    a = R.fig_yaw(cam, neck, F)
    fig = lambda w: tuple(c / m for c in R.to_fig(cam, neck, a, S._sub(w, neck)))
    j = V.standing(sp)
    for sd, dx in (('L', -0.14), ('R', 0.14)):
        j['foot' + sd] = fig(car.body_pt((neck_l[0] + dx, 0.28, neck_l[2] + feet_z)))
    for sd, at, pole, shape in hands:
        tgt = at[1] if at[0] == 'fig' else fig(car.body_pt(at))
        V.arm_to(j, sd, tgt, pole, shape)
    j['props'] += list(props)
    if grip:
        j['grip'] = set(grip)
    out = R.person_at(lay, cam, sp, neck, F, t, j, head_dir)
    if rec is not None:
        rec.append((name or who, R.body_pts3(cam, neck, a, j, m, who)))
    return out


EYES_LEAD = 0.17     # the pupils reach a new look two drawings before the face slides (acting.py)


def focused(over, keys, t):
    """Front-on focus (focus.py, the BoJack look: -1 screen left .. +1 screen right) from [(t, focus)] keys; the eyes
    lead. Sam's note on the shots 5-8 clip (chat 19): "a lack of imagination with the acting when they are speaking";
    "J always faces forward even though he's indicating other things"."""
    over['focus'] = keys_at(keys, t)
    over['focus_eyes'] = keys_at(keys, t + EYES_LEAD)
    over['look'] = 0.0
    return over


# Where each person looks (world time; + = screen right in both cameras: Jason sits screen left, her in the middle,
# Lucia screen right). Chat 19 found the old looks went the wrong way: Lucia's "turn to Jason" and both "eyes slide to
# each other" on "nitroglycerin" looked AWAY from each other (+ is screen right).
H1 = LINE5[0] + 0.95                # "Her" (hyperfixation...): Jason's thumb back at her
JOB = word_at(LINE5, 38)            # "This job..."
J_FOCUS = [(0, 0.0), (6.28, 0.0), (6.42, 0.8), (7.3, 0.8), (7.6, 0.0),            # the yank: "what are you doing"
           (7.70, 0.0), (7.85, 0.45), (8.6, 0.45), (8.9, 0.0),                    # line 3: a glance back at her
           (12.05, 0.0), (12.25, 0.7), (12.9, 0.7),                               # "I told you" to Lucia, eyes shut
           (H1 - 0.12, 0.45), (H1 + 0.45, 0.45), (H1 + 0.7, 0.95), (15.25, 0.95),  # at her, then explains to Lucia
           (15.45, 0.35), (JOB - 0.05, 0.35), (JOB + 0.12, 0.85), (WITHOUT - 0.1, 0.85),
           (WITHOUT + 0.08, 0.45), (17.55, 0.45), (17.95, 0.0),                   # "without her": at her, then fed up
           (NITRO + 0.12, 0.0), (NITRO + 0.4, 0.7)]                              # eyes slide to Lucia, held
L_FOCUS = [(0, 0.0), (LINE4[0] - 0.12, 0.0), (LINE4[0] + 0.08, -0.9), (BROUGHT - 0.12, -0.9),
           (BROUGHT + 0.05, -0.45), (BROUGHT + 0.5, -0.45), (BROUGHT + 0.8, 0.0),  # "brought her": a jerk back at her
           (TOLD[0], 0.0), (TOLD[0] + 0.12, -0.4), (TOLD[1] + 0.2, -0.4), (TOLD[1] + 0.45, 0.0),
           (WITHOUT, 0.0), (WITHOUT + 0.15, -0.55), (WITHOUT + 0.6, -0.55), (WITHOUT + 0.85, 0.0),   # side-eye
           (NITRO + 0.05, 0.0), (NITRO + 0.3, -0.7)]
H_FOCUS = [(0, 0.0), (7.75, 0.0), (7.85, -0.25), (7.97, 0.25), (8.09, -0.2), (8.2, 0.0),   # "didn't": a small headshake
           (8.3, 0.5), (8.85, 0.5), (9.05, 0.0),                                   # "like that": at the driver
           (LINE4[0] + 0.25, 0.0), (LINE4[0] + 0.4, 0.5), (BROUGHT, 0.5), (BROUGHT + 0.2, 0.0),
           (HYPER - 0.1, 0.0), (HYPER + 0.05, -0.5), (15.4, -0.5), (15.6, 0.0)]  # "hyperfixation": at Jason


def her_spin_t(t):
    """The spinner's own clock: it spins, and stops as she brightens before her line (shot 8)."""
    t_stop = LINE6[0] - 0.25
    if t < t_stop:
        return t
    return t_stop + 0.12 * (1 - math.exp(-(t - t_stop) / 0.12))


def inside58(t, rec=None):
    def paint(lay, cam, car):
        rot = getattr(car, 'wheel', 0.0)
        th = throw(t)
        fwd = S._norm(car.body_dir((0, 0, 1)))
        hd = lambda d: S._norm(car.body_dir(d))
        # ---- her (line 3 after the corner; line 6, brightening, the punchline)
        tug = bump(t, 8.95, 9.15, 9.45)                           # straightens her jumper after line 3
        lean_in = smooth((t - (LINE6[0] - 0.5)) / 0.45)         # leans forward a little for line 6
        her_neck = (0.0 - 0.11 * th, 0.91, -0.80 + 0.07 * lean_in)
        mo = mouth(t, LINE3) or mouth(t, LINE6)
        pinch = bump(t, LINE3[0] - 0.4, LINE3[0] + 0.3, LINE3[0] + 2.0)
        down = 1 - bump(t, LINE3[0] + 0.5, LINE3[0] + 0.9, LINE3[0] + 2.3)  # eyes down on the spinner, up then forward
        bright = smooth((t - (LINE6[0] - 0.35)) / 0.35)
        her_over = dict(mood='phone' if bright < 0.5 and down > 0.5 else None, gaze_dy=0.7 * down * (1 - bright) - 0.45 * bright,
                        squint=0.35 * th, frown=-0.04 + 0.10 * pinch - 0.06 * bright, smile=-0.4 + 2.0 * bright,
                        brow_up=0.075 * bright)
        if her_over['mood'] is None:
            her_over.pop('mood')
        proud = bump(t, EXPLO - 0.1, EXPLO + 0.2, EXPLO + 1.2) + bump(t, WITHOUT, WITHOUT + 0.25, WITHOUT + 1.1)
        her_over['smile'] += 0.7 * proud                                   # a little proud on "explosives", "without her"
        her_over['brow_up'] += 0.03 * proud
        her_over['gaze_dy'] += 0.45 * bump(t, BROUGHT + 0.1, BROUGHT + 0.3, BROUGHT + 1.0)   # "brought her": eyes drop
        focused(her_over, H_FOCUS, t)
        if mo:
            her_over['mouth'] = mo
        fid = 0.012 * math.sin(t * 19.0) * (1 - bright)
        sx = -0.11 * th
        spin_at = (sx + fid, 0.87 - 0.10 * tug, -0.50 + 0.05 * lean_in)
        her_hands = [('L', (sx - 0.05 + fid - 0.08 * tug, 0.85 - 0.25 * tug, -0.53 + 0.05 * lean_in), 'down', 'fist'),
                     ('R', (sx + 0.05 + fid + 0.08 * tug, 0.87 - 0.25 * tug, -0.50 + 0.05 * lean_in), 'down', 'fist')]
        # ---- Lucia: the yank (face screwed up), line 4 (turns to Jason on "you", nods back at her on "brought")
        nod = bump(t, BROUGHT - 0.1, BROUGHT + 0.12, BROUGHT + 0.45)
        yank = bump(t, 6.25, 6.55, 7.6)
        roll = bump(t, HYPER - 0.05, HYPER + 0.2, HYPER + 0.75)      # "hyperfixation": her eyes roll up
        mirror = bump(t, 17.7, 18.0, 18.9)                          # shot 7: eyes up to the mirror, the lights
        lu_over = dict(mood='stern', squint=0.45 + 0.35 * yank - 0.15 * roll, frown=0.09 + 0.05 * yank, brow_up=-0.01 + 0.03 * roll,
                       gaze_dy=0.25 * nod - 0.7 * roll - 0.45 * mirror)
        focused(lu_over, L_FOCUS, t)   # the nod back at her: eyes, never
        #                                       the head (turned away, her ponytail crossed her face: chat 16)
        lm = mouth(t, LINE4)
        if lm:
            lu_over['mouth'] = lm
        lu_neck = (-0.42 - 0.07 * th, 0.94, 0.05)
        lu_dir = None   # the look is the focus kit now (no 3D head turn: her ponytail crossed her face, chat 16)   # a small turn: further, her ponytail
        # swings over her face (chat 16, full size); her eyes do the rest
        # Sam's note 1 on shot 4 v4: opposite grips (the hands carried round with the wheel until the arms crossed) are
        # "not how humans drive". Here she feeds the wheel: hands near ten and two, carried only a little way by a turn
        # and never crossing (chat 16). Shot 4's hand-over-hand is chat 17's rebuild.
        carry = 0.28 * rot
        lu_hands = [('L', R.wheel_pt(0.0, 150 - carry), 'down', 'fist'), ('R', R.wheel_pt(0.0, 30 - carry), 'down', 'fist')]
        # ---- Jason: gun flat on his chest; braced through the corner; line 5 (eyes shut on "told you", the free hand
        # opens on "hyperfixation", counts on "explosives", open palm toward her on "without her")
        shut = TOLD[0] + 0.02 <= t <= TOLD[1] + 0.12
        j_over = dict(mood='stern', squint=0.35 - 0.2 * (t > 9.5), frown=0.07, blink=shut,
                      brow_up=0.015 * bump(t, TOLD[0], TOLD[1], TOLD[1] + 2.5) + 0.03 * bump(t, JOB, JOB + 0.2, WITHOUT))
        focused(j_over, J_FOCUS, t)
        jm = mouth(t, LINE5)
        if jm:
            j_over['mouth'] = jm
        j_neck = (0.42 - 0.07 * th, 1.02, 0.0)      # 0.918 + 0.10: he sat lower than in shots 1-4 (Sam 21 Nov: 'sunken')
        thigh = (0.30 - 0.07 * th, 0.31, 0.30)
        dash = (0.34, 0.82, 0.52)
        # Sam's note (chat 19): "his arm poses could use work". The free hand now works where the camera sees it, up
        # beside his face on the window side, forearm upright (it reached across his chest from that shoulder: a
        # thick diagonal with a lump at the frame's bottom, chat 19), and his head goes where his hand points: a
        # thumb back at her, an open hand explaining to Lucia with beats on the words, palm up on "this job", the
        # thumb back at her again on "without her" (grudging), then down, fed up.
        lift = (0.52, 0.96, 0.22)
        thumb = (0.60, 1.16, 0.06)
        expl = (0.64, 1.12, 0.16)
        beat = lambda u, d=0.045: (expl[0], expl[1] - d, expl[2])
        shrug = (0.66, 1.08, 0.22)
        her_hand = (0.60, 1.16, 0.06)
        b1, b2, b3 = word_at(LINE5, 20), word_at(LINE5, 24), EXPLO
        lh = keys_at([(0, thigh), (6.30, thigh), (6.50, dash), (7.40, dash), (7.75, thigh),
                      (12.0, thigh), (12.3, lift), (H1 - 0.25, lift), (H1 - 0.05, thumb), (H1 + 0.45, thumb),
                      (H1 + 0.75, expl), (b1 - 0.05, expl), (b1 + 0.08, beat(0)), (b1 + 0.2, expl),
                      (b2 - 0.05, expl), (b2 + 0.08, beat(0)), (b2 + 0.2, expl),
                      (b3 - 0.05, expl), (b3 + 0.1, beat(0, 0.06)), (b3 + 0.25, expl), (15.3, expl),
                      (JOB - 0.05, lift), (JOB + 0.2, shrug), (WITHOUT - 0.12, shrug), (WITHOUT + 0.1, her_hand),
                      (17.45, her_hand), (17.9, thigh)], t)
        lshape = step_at([(0, 'palm'), (H1 - 0.12, 'thumb'), (H1 + 0.6, 'palm'), (WITHOUT - 0.05, 'thumb'), (17.6, 'palm')], t)
        lpole = 'out' if WITHOUT + 0.6 < t < 18.2 else 'down'   # the hand coming down from his ear: 'down' folded
        #                                                       the elbow across his chest (figure check, shot 7)
        j_hands = [('R', ('fig', (120.0, 25.0, 80.0)), 'down', 'fist'), ('L', lh, lpole, lshape)]
        gun = PC.glock('R', flash=0.0, aim3=(0.9, -1.0, 0.05), size=1.0)
        R.bench(lay, cam, car)
        order = sorted([('case', (0.4, 0.7, -0.85)), ('her', her_neck), ('lucia', lu_neck), ('jason', j_neck)],
                       key=lambda s: -math.dist(car.body_pt(s[1]), cam.pos))
        for who, at in order:
            if who == 'case':
                R.cash_case(lay, cam, car)
            elif who == 'her':
                sit(lay, cam, car, 'her', her_neck, t, her_hands, her_over, feet_z=0.55, rec=rec)
                R.spinner(lay, cam, car.body_pt(spin_at), her_spin_t(t), r=0.065)
            elif who == 'lucia':
                sit(lay, cam, car, 'lucia', lu_neck, t, lu_hands, lu_over, head_dir=lu_dir, rec=rec)
                R.steering_wheel(lay, cam, car, rot)
            else:
                sit(lay, cam, car, 'jason', j_neck, t, j_hands, j_over, props=[], grip=(), rec=rec,
                    head_dir=fwd)
    return paint


# ------------------------------------------------------------------------------------------------ one frame
WHEEL58 = (-0.42, 0.87, 0.47)    # Lucia's wheel 8 cm lower than shot 3's: the closer, lower two-shot put its rim across
#                                  her mouth as she speaks (chat 16); too small to see between shots


def world58(t, cam_fn, record=None):
    keep = R.WHEEL_C
    R.WHEEL_C = WHEEL58
    try:
        return _world58(t, cam_fn, record)
    finally:
        R.WHEEL_C = keep


def seen_round_corner(cam, q):
    """False when world point q stands on the other road, hidden behind the corner blocks: the shops draw first and
    everything else after (gta_rehearse.world4's way, right on one straight street), so a palm, person or smoke on A
    painted over B's shop fronts (chat 16, shot 8). Seen only down the gap between the two corners (z within ZC +- 10)."""
    cx, cz = cam.pos[0], cam.pos[2]
    x, z = q[0], q[2]
    if (cx - 10.0) * (x - 10.0) >= 0:
        return True
    u = (10.0 - cx) / (x - cx)
    return abs(cz + u * (z - cz) - ZC) < 10.5


def _world58(t, cam_fn, record=None):
    GC.cast()
    B.SS = 2
    FX.SIZE = (1080 * B.SS, 1920 * B.SS)
    img = B.canvas((240, 170, 170))
    tul = tulip58(t)
    lead = R.lead_at(t + SH)
    chasers = [chaser58(t, 1), chaser58(t, 2)]
    cam = cam_fn(t, tul)
    cb = camB(cam)
    p = S.pen(img)
    ground58(img, cam, cb, p)
    # shops of both roads, far to near (B's in its own frame: same depth either way)
    hole = None
    if R.IMPACT and t + SH >= R.IMPACT[0]:
        hole = (R.IMPACT[1][1] + 2.6 * math.cos(math.radians(R.IMPACT[2])), t + SH - R.IMPACT[0])
    shops = []
    for b, c in [(b, cam) for b in BLOCKS_A] + [(b, cb) for b in BLOCKS_B]:
        if c.depth((b['side'] * R.SHOP4, 1.0, b['z0'])) < -2 and c.depth((b['side'] * R.SHOP4, 1.0, b['z1'])) < -2:
            continue
        if min(abs(b['z0'] - c.pos[2]), abs(b['z1'] - c.pos[2])) > 160 and not (b['z0'] < c.pos[2] < b['z1']):
            continue
        d = math.dist(c.pos, (b['side'] * (R.SHOP4 + 7), b['h'] / 2, (b['z0'] + b['z1']) / 2))
        shops.append((d, b, c))
    for d, b, c in sorted(shops, key=lambda e: -e[0]):
        h = hole if (c is cam and hole and b['side'] == 1 and b['z0'] < hole[0] < b['z1']) else None
        R.shop_block(img, c, p, b, h)
    items = []
    for crowd_fn, people, c, tag in ((R.crowd, PEOPLE_A, cam, 'person'), (crowd_b, PEOPLE_B, cb, 'person b')):
        for pp in people:
            if c is cb and abs(pp['at'][1] - c.pos[2]) > 90:
                continue
            x, z, F_, j_, hd = crowd_fn(pp, t + SH if crowd_fn is R.crowd else t)
            d = c.depth((x, 1.0, z))
            wq = to_world((x, 1.0, z)) if c is cb else (x, 1.0, z)
            if 0.2 < d < 70 and seen_round_corner(cam, wq):
                sp_ = R._walker(pp['i'])
                hgt = sp_.get('height', 1.75)
                m_ = hgt / R.FIG_H
                neck_ = (x, 0.15 + 928 * m_, z)
                (gx, gy), _ = c.project((x, 0.15, z))
                (_, ty), _ = c.project((x, 0.15 + hgt, z))
                a_ = R.fig_yaw(c, neck_, F_)
                pts = R.body_pts3(c, neck_, a_, j_, m_, 'p', lean=j_.get('lean', 0.0))
                if c is cb:
                    pts = [(n, to_world(q)) for n, q in pts]
                inf = dict(pts3=pts, ground_px=(gx, gy), height_px=gy - ty)
                if d < 38:
                    fn = lambda im, c=c, sp_=sp_, neck_=neck_, F_=F_, j_=j_, hd=hd: R.person_at(im, c, sp_, neck_, F_, t, j_, hd)
                else:
                    fn = lambda im, c=c, pp=pp, neck_=neck_, F_=F_: R.person_cached(im, c, R._walker(pp['i']), pp['i'], neck_, F_)
                items.append((f"{tag} {pp['i']}", d, fn, inf))
    for palms, c, tag in ((PALMS_A, cam, 'palm'), (PALMS_B, cb, 'palm b')):
        for k, (x, z) in enumerate(palms):
            d = c.depth((x, 3.0, z))
            wq = to_world((x, 3.0, z)) if c is cb else (x, 3.0, z)
            if 0.5 < d < 160 and seen_round_corner(cam, wq):
                items.append((f'{tag} {k}', d, lambda im, c=c, x=x, z=z, k=k: R.palm(im, c, S.pen(im), (x, z), seed=k)))
    if R.HYDRANT:
        hx, hz = R.HYDRANT[1]
        d = cam.depth((hx, 0.5, hz))
        if seen_round_corner(cam, (hx, 0.5, hz)):
            items.append(('hydrant', d, lambda im: R.hydrant_stump(im, cam, S.pen(im), (hx, hz))))
    for k, (c, ins) in enumerate(((lead, R.cop_inside(0, t + SH, True)), (chasers[0], R.cop_inside(1, t + SH)), (chasers[1], R.cop_inside(2, t + SH)))):
        d = cam.depth((c.pos[0], 0.8, c.pos[1]))
        if d > 0.5 and seen_round_corner(cam, (c.pos[0], 0.8, c.pos[1])):
            items.append(('lead cruiser' if k == 0 else f'cruiser {k + 1}', d,
                          lambda im, c=c, ins=ins: G.draw_car(im, cam, c, t=t, inside=ins)))
    fx_seen = seen_round_corner(cam, (lead.pos[0], 1.0, lead.pos[1]))   # the crash's fire, smoke and jet: all at the crash
    items += [(f'effect {k}', d, fn) for k, (d, fn) in enumerate(R.fx_items(cam, t + SH, lead)) if fx_seen]
    d_t = cam.depth((tul.pos[0], 0.8, tul.pos[1]))
    seat_pts = []
    tinf = {}

    def tulip_draw(im):
        seat_pts.clear()
        G.draw_car(im, cam, tul, t=t, inside=inside58(t, seat_pts))
        tinf['pts3'] = [(f'{who} {n}', q) for who, pts in seat_pts for n, q in pts]
    items.append(('tulip', d_t, tulip_draw, tinf))
    for e in sorted(items, key=lambda e: -e[1]):
        e[2](img)
    if record is not None:
        tinf['may_touch'] = ('tulip (solid)',)            # seated people are in the cabin: their own car never counts
        record += items
        record += solids58(cam, [('lead cruiser', lead)] + [(f'cruiser {k + 2}', c) for k, c in enumerate(chasers)])
    R.light_wash(img, cam, [lead] + chasers, t + SH)
    return img


def street_solid58(q):
    x, y, z = q
    if x > 6.9 and abs(z - ZC) < 26:                     # B's corner: judged in B's frame
        xl, yl, zl = to_local(q)
        if abs(xl) > R.SHOP4 + 0.05 and y < 12:
            for b in BLOCKS_B:
                if b['side'] * xl > 0 and b['z0'] < zl < b['z1'] and y < b['h']:
                    return 'a shop wall'
        g = 0.15 if (abs(xl) > 7.0 and zl > 7.0) else 0.0
        if y < g - 0.03:
            return 'the pavement' if g else 'the road'
        return None
    if abs(x) > R.SHOP4 + 0.05 and y < 12:
        for b in BLOCKS_A:
            if b['side'] * x > 0 and b['z0'] < z < b['z1'] and y < b['h']:
                return 'a shop wall'
    g = 0.15 if abs(x) > R.KERB4 else 0.0
    if y < g - 0.03:
        return 'the pavement' if g else 'the road'
    return None


def solids58(cam, cars):
    out = [('street', 0, None, dict(solid=street_solid58, cam=cam))]
    for nm, c in cars:
        out.append((nm + ' (solid)', 0, None, dict(solid=lambda q, c=c: G.solid_at(c, q, ()))))
    return out


# ------------------------------------------------------------------------------------------------ cameras and shots
CAM6 = ((0.00, 1.18, 2.70), (0.00, 1.06, -0.30), 2050)   # shot 6: the closer two-shot, Lucia and Jason, her small between


def cam6(t, car):
    pos, at, focal = CAM6
    rng = np.random.RandomState(int((t + 10) * 24))
    return S.Cam(car.ground_pt(pos), car.ground_pt(at), focal, shake=(rng.uniform(-1.6, 1.6), rng.uniform(-1.3, 1.3)))


SHOTS58 = {  # shot: (world start, length, camera)
    5: (T5, 3.2, R.shot3_cam),
    6: (T5 + 3.2, 8.0, cam6),
    7: (T5 + 11.2, 1.4, R.shot3_cam),
    8: (T5 + 12.6, 3.6, R.shot3_cam),
}


def shot_fn(n):
    t0, ln, cf = SHOTS58[n]
    return lambda t, record=None: world58(t0 + t, cf, record)


OVERLAP_OK58 = R.OVERLAP_OK4

if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) >= 4 and a[0] == 'still':
        shot_fn(int(a[1]))(float(a[2])).convert('RGB').resize((1080, 1920), Image.LANCZOS).save(a[3], quality=90)
    elif len(a) >= 3 and a[0] == 'clip':
        n = int(a[1])
        fd = a[a.index('--frames') + 1] if '--frames' in a else None
        R.clip(shot_fn(n), SHOTS58[n][1], a[2], fd)
    elif len(a) >= 2 and a[0] in ('layers', 'bodies'):
        import viewchecks as VC
        k = int(a[a.index('--every') + 1]) if '--every' in a else 1
        faults = []
        for nm in [x for x in a[1:] if x.isdigit() and x != str(k)]:
            n = int(nm)
            if a[0] == 'layers':
                faults += VC.layer_faults(shot_fn(n), SHOTS58[n][1], allowed=OVERLAP_OK58, label=f'shot{n}', step=k) \
                    if 'step' in VC.layer_faults.__code__.co_varnames else VC.layer_faults(shot_fn(n), SHOTS58[n][1], allowed=OVERLAP_OK58, label=f'shot{n}')
            else:
                faults += VC.solid_faults(shot_fn(n), SHOTS58[n][1], step=k, label=f'shot{n}')
        print('\n'.join(faults) or f'{a[0]}: clean')
    else:
        print(__doc__)
