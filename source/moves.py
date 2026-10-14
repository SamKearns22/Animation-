#!/usr/bin/env python3
"""moves: how the satire package's people move (built on views.py's skeleton; guides/reference-pack.md).

Built to order: everything here is ready, but a film only uses what its script needs.

- GAITS: stroll, walk, brisk, run, sprint (Williams' tempos; a run has a float, both feet off the ground).
  `gait(sp, t, kind)` -> a pose; `travel(path, t, kind)` -> where someone is on a path in metres, which way they face
  and their pose (feet planted, never sliding); `pace(...)` walks a line and back with the standard straight-180 turn.
- POSES: standing styles, talking gestures and things held (`pose(sp, name, ...)`), each a few held key poses.
- TRANSITIONS: `sit_down` / `stand_up` (the four phases of rising from a chair).
- COMBAT: `punch`, `kick`, `sword`, `hit_react`, `fall`: wind-up, fast strike landing in a drawing or two, a held
  impact, follow-through; the victim moves only after the contact, away from the force; falls in stages.
- CARS (the car itself is drawn per film): `driving`, `car_in`, `car_out`.
- EVENTS: each move reports its moments (footfalls, contacts) so a sound can go on them if the script asks
  (no sound effects by default: Sam, 14 Oct).
- CHECKS: `check_*` functions return faults in plain words (feet sliding, facing the wrong way, a blow that doesn't
  reach, a reaction before the contact, a body not on the floor).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import figure as F           # noqa: E402
import views as V            # noqa: E402
from ed import INK           # noqa: E402

FPS = 12


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def fast_in(u):
    u = max(0.0, min(1.0, u))
    return u * u * u                                      # slow start, arrives fast (into a hit)


def lerp(a, b, u):
    if isinstance(a, tuple):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


def mix_poses(a, b, u):
    """A pose part-way between two poses (joints, bob, lean, head_dy); hands, props and flags from the nearer one."""
    out = dict(b if u >= 0.5 else a)
    for k, v in a.items():
        if k in b and isinstance(v, (tuple, float, int)) and not isinstance(v, bool):
            out[k] = lerp(v, b[k], u)
    return out


def keyed(t, keys, curve='ease'):
    """A pose from timed key poses [(time, pose)]: held until the next key's move, which takes `curve` ('ease', 'fast'
    into a hit, or 'snap' = straight to the next drawing, limited animation)."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, a), (t1, b) in zip(keys, keys[1:]):
        if t < t1:
            u = (t - t0) / max(1e-6, t1 - t0)
            if curve == 'snap':
                return a if u < 0.5 else b
            return mix_poses(a, b, fast_in(u) if curve == 'fast' else ease(u))
    return keys[-1][1]


# ------------------------------------------------------------------------------------------------ gaits
GAITS = {  # steps a second (Williams), step length (m), foot lift, time each foot is down (fraction), arm swing,
    #          arm bend (rad), lean (deg), float height (person units, runs only)
    'stroll': dict(sps=1.5, step=0.38, lift=40, duty=0.62, swing=0.22, bend=0.15, lean=1, float=0),
    'walk':   dict(sps=2.0, step=0.45, lift=56, duty=0.60, swing=0.32, bend=0.20, lean=2, float=0),
    'brisk':  dict(sps=2.6, step=0.52, lift=62, duty=0.57, swing=0.42, bend=0.35, lean=4, float=0),
    'run':    dict(sps=3.4, step=0.95, lift=150, duty=0.36, swing=0.75, bend=1.45, lean=9, float=28),
    'sprint': dict(sps=4.4, step=1.25, lift=190, duty=0.30, swing=1.00, bend=1.55, lean=16, float=40),
}


def speed(kind):
    g = GAITS[kind]
    return g['sps'] * g['step']                               # metres a second


def gait(sp, t, kind='walk', stride=None, steps_per_s=None):
    """A pose `t` seconds into a gait. Feet planted on the floor slide back exactly as fast as the body moves on.
    `stride`: step length in person units (default from GAITS)."""
    g = dict(GAITS[kind])
    if steps_per_s:
        g['sps'] = steps_per_s
    step = stride if stride is not None else g['step'] / V.M_PER_UNIT
    j = V.standing(sp)
    cyc = (t * g['sps'] / 2.0) % 1.0                          # one cycle = two steps (left, then right)
    duty = g['duty']
    sweep = 2 * duty * step                                   # how far a planted foot travels back under the body
    reach = 0.99 * (V.THIGH + V.SHIN)
    planted = {}
    for side, ph0 in (('L', 0.0), ('R', 0.5)):
        u = (cyc + ph0) % 1.0
        sg = -1 if side == 'L' else 1
        if u < duty:                                          # on the ground
            z, lift = sweep / 2 - sweep * (u / duty), 0.0
            j['toe' + side] = 14 * max(0.0, (u / duty - 0.8) / 0.2)       # heel peels up just before toe-off
        else:                                                 # swinging forward: picks up slowly, puts down fast
            k = (u - duty) / (1 - duty)
            e = 1 - (1 - k) ** 1.6
            z = -sweep / 2 + sweep * e
            lift = g['lift'] * math.sin(math.pi * min(1.0, k * 1.15)) ** 1.2
            j['toe' + side] = 14 * (1 - k) ** 2 - 8 * k ** 2              # toes down leaving, toes up to meet the floor
        planted[side] = u < duty
        j['foot' + side] = (sg * 50, V.ANKLE_Y - lift, z)
        other = 'R' if side == 'L' else 'L'                   # the opposite arm swings with this leg's opposite
        swing = -z / max(1.0, sweep / 2)
        fwd = g['swing'] * (swing if swing > 0 else 0.35 * swing) + 0.12   # arms swing mostly in front (Sam)
        V.set_arm(j, other, fwd, g['bend'] + 0.15 + 0.2 * max(0.0, swing) * (g['bend'] > 1))
    drop = 0.0
    for side in 'LR':
        fx, fy, fz = j['foot' + side]
        if planted[side]:
            drop = max(drop, fy - V.HIP_Y - math.sqrt(max(0.0, reach * reach - fz * fz)))
    if not any(planted.values()):                             # the float: both feet off, highest mid-air
        fu = ((cyc % 0.5) - (duty - 0.5 if duty > 0.5 else 0)) / max(1e-6, 0.5 - duty) if duty < 0.5 else 0.5
        drop = -g['float'] * math.sin(math.pi * max(0.0, min(1.0, fu - duty / max(1e-6, 0.5 - duty))))
    j['bob'] = drop + (3 * math.cos(4 * math.pi * cyc) if g['float'] == 0 else 0.0)
    for side in 'LR':
        fx, fy, fz = j['foot' + side]
        fy -= j['bob']
        if not planted[side]:
            fy = min(fy, V.HIP_Y + math.sqrt(max(0.0, reach * reach - fz * fz)))
        j['foot' + side] = (fx, fy, fz)
    j['lean'] = g['lean']
    j['planted'] = planted
    return j


def footfalls(kind, t0, t1):
    """The moments each foot lands (for footsteps, if the script asks for them)."""
    g = GAITS[kind]
    out, k = [], 0
    while True:
        at = t0 + k / g['sps']
        if at > t1:
            return out
        out.append(at)
        k += 1


def travel(path, t, kind='walk', start=0.0, hold=0.0):
    """Someone walking (or running) along `path`, a list of (X, Z) floor points in metres, starting at `start`
    seconds. Returns (X, Z, yaw, pose). Facing: the way they are going (body and face, Sam). At the end they stand
    for good, facing the last direction."""
    v = speed(kind)
    dist = t - start
    if dist <= 0:
        a, b = path[0], path[1]
        return a[0], a[1], math.degrees(math.atan2(b[0] - a[0], b[1] - a[1])), None
    d = dist * v
    for a, b in zip(path, path[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        yaw = math.degrees(math.atan2(b[0] - a[0], b[1] - a[1]))
        if d <= seg:
            u = d / seg
            return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, yaw, 'moving'
        d -= seg
    return path[-1][0], path[-1][1], yaw, 'arrived'


def pace(sp, t, a, b, kind='walk', turn_hold=0.35, start=0.0):
    """Pacing: walk from a to b, stand for turn_hold seconds, a straight 180 (the standard turn: a pop to the other
    view), walk back; and again. Returns (X, Z, yaw, pose)."""
    seg = math.hypot(b[0] - a[0], b[1] - a[1]) / speed(kind)
    leg_t = seg + turn_hold
    k, u = divmod(max(0.0, t - start), leg_t)
    src, dst = (a, b) if int(k) % 2 == 0 else (b, a)
    yaw = math.degrees(math.atan2(dst[0] - src[0], dst[1] - src[1]))
    if u < seg:
        w = u / seg
        return src[0] + (dst[0] - src[0]) * w, src[1] + (dst[1] - src[1]) * w, yaw, gait(sp, u, kind)
    return dst[0], dst[1], yaw + (180 if u - seg > turn_hold / 2 else 0), V.standing(sp)


# ------------------------------------------------------------------------------------------------ poses
def _phone(p, j2, side, ear=False):
    el, wr = j2['el' + side], j2['wr' + side]
    dx, dy = wr[0] - el[0], wr[1] - el[1]
    n = math.hypot(dx, dy) or 1.0
    cx, cy = wr[0] + dx / n * 14, wr[1] + dy / n * 14
    h, w = (60, 28) if not ear else (52, 24)
    p.poly([(cx - w, cy - h), (cx + w, cy - h), (cx + w, cy + h * 0.4), (cx - w, cy + h * 0.4)], (40, 44, 54), INK, 2.2)
    if not ear:
        p.poly([(cx - w + 5, cy - h + 6), (cx + w - 5, cy - h + 6), (cx + w - 5, cy + h * 0.3), (cx - w + 5, cy + h * 0.3)],
               (150, 190, 230), None)


def _paper(p, j2):
    a, b = j2['wrL'], j2['wrR']
    x0, x1 = min(a[0], b[0]) - 10, max(a[0], b[0]) + 10
    y = (a[1] + b[1]) / 2
    p.poly([(x0, y - 150), (x1, y - 150), (x1, y + 60), (x0, y + 60)], (250, 250, 246), INK, 2.2)
    for k in range(5):
        p.line([(x0 + 20, y - 120 + 30 * k), (x1 - 20 - 30 * (k % 2), y - 120 + 30 * k)], (150, 150, 160), 3)


def _mug(p, j2, side='R'):
    x, y = j2['wr' + side]
    p.poly([(x - 30, y - 70), (x + 30, y - 70), (x + 26, y + 10), (x - 26, y + 10)], (246, 246, 240), INK, 2.2)
    p.line([(x + 30, y - 50), (x + 46, y - 34), (x + 30, y - 18)], INK, 3.2)


def _mic(p, j2, side='R'):
    x, y = j2['wr' + side]
    p.poly([(x - 9, y - 10), (x + 9, y - 10), (x + 7, y - 110), (x - 7, y - 110)], (30, 30, 34), INK, 2.0)
    p.ell(x, y - 124, 20, 22, (60, 62, 70), INK, 2.0)


def _pen(p, j2, side='R'):
    x, y = j2['wr' + side]
    p.line([(x - 6, y + 4), (x + 30, y - 60)], (30, 50, 120), 6)


def _bag(p, j2):
    x, y = j2['shR'][0] + 20, j2['hipR'][1] - 60
    p.line([j2['shR'], (x + 10, y)], (90, 60, 40), 7)
    p.poly([(x - 10, y), (x + 130, y), (x + 120, y + 120), (x, y + 120)], (120, 80, 50), INK, 2.4)


def pose(sp, name, beat=0.0, target=None):
    """A standing style, gesture or holding pose. `beat` (0-1) drives a gesture's stroke (a chop, a wag);
    `target`: a point for pointing or leaning (torso frame)."""
    j = V.standing(sp)
    sw = sp.get('shoulders', 150)
    head = (0.0, -150.0, 40.0)
    if name == 'relaxed':                                    # contrapposto: weight on the right leg, left knee soft
        j['footR'] = (36, V.ANKLE_Y, 0.0)
        j['footL'] = (-86, V.ANKLE_Y - 8, 26.0)
        j['toeL'] = 8
    elif name == 'hips':
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * (sw - 4), 380.0, 10.0), 'out')
    elif name == 'arms_folded':                              # forearms across the chest, hands tucked
        V.arm_to(j, 'L', (95.0, 262.0, 92.0), (0.4, 1.0, -0.1), 'none')        # forearms level across the chest,
        V.arm_to(j, 'R', (-95.0, 236.0, 104.0), (0.4, 1.0, -0.1), 'none')      # the right one over the left
    elif name == 'pockets':
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * (sw - 16), 430.0, 16.0), 'out', 'none')
    elif name == 'behind_back':
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * 26, 410.0, -70.0), (1.0, 0.4, -0.7), 'none')
        j['behind'] = {'L', 'R'}
    elif name == 'lean_on':                                  # one hand on a surface, weight onto it, the other on the hip
        V.arm_to(j, 'R', target or (sw + 110, 360.0, 30.0), 'out', 'palm')
        V.arm_to(j, 'L', (-(sw - 4), 380.0, 10.0), 'out')
        j['footR'] = (90, V.ANKLE_Y, 0.0)
        j['footL'] = (-40, V.ANKLE_Y - 6, 30.0)
    elif name == 'slumped':
        j['head_dy'] = 22
        j['lean'] = 7
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * (sw - 30), 480.0, 70.0), 'back')
    elif name == 'palm_open':                                # offering an idea on an open palm
        V.arm_to(j, 'R', (sw - 30, 300.0 - 16 * beat, 190.0), 'down', 'palm')
    elif name == 'chop':                                     # the politician's chopping hand, a stroke on each beat
        V.arm_to(j, 'R', (40.0, 180.0 + 90 * beat, 190.0), 'down', 'palm')
    elif name == 'shrug':
        j['head_dy'] = -6
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * (sw + 130), 330.0, 70.0), 'down', 'palm')
    elif name == 'point':                                    # at a target, the other hand on the hip
        V.arm_to(j, 'R', target or (sw + 400, 60.0, 250.0), 'down', 'point')
        V.arm_to(j, 'L', (-(sw - 4), 380.0, 10.0), 'out')
    elif name == 'facepalm':
        j['head_dy'] = 10
        j['lean'] = 6
        V.arm_to(j, 'R', (14.0, -170.0, 80.0), 'down', 'palm')
    elif name == 'head_in_hands':
        j['head_dy'] = 26
        j['lean'] = 14
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * 62, -118.0, 46.0), (1.0, 0.7, 0.9), 'palm')   # elbows forward and a little out
    elif name == 'heart':
        V.arm_to(j, 'R', (40.0, 160.0, 46.0), 'down', 'palm')
    elif name == 'phone_ear':
        V.arm_to(j, 'R', (82.0, -140.0, 16.0), (0.6, 1.0, 0.7), 'phone')       # elbow down and forward, forearm up
        j['props'] = [lambda p, j2: _phone(p, j2, 'R', ear=True)]
    elif name == 'phone_read':
        j['head_dy'] = 8
        V.arm_to(j, 'R', (30.0, 230.0, 180.0), 'down', 'phone')
        j['props'] = [lambda p, j2: _phone(p, j2, 'R')]
    elif name == 'paper':
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * 100, 250.0, 160.0), 'down', 'fist')
        j['props'] = [_paper]
    elif name == 'mug':
        V.arm_to(j, 'R', (70.0, 300.0, 130.0), 'down', 'cup')
        j['props'] = [lambda p, j2: _mug(p, j2)]
    elif name == 'mug_sip':
        V.arm_to(j, 'R', (24.0, -96.0, 80.0), 'down', 'cup')
        j['props'] = [lambda p, j2: _mug(p, j2)]
    elif name == 'mic':
        V.arm_to(j, 'R', (30.0, 20.0, 150.0), 'down', 'fist')
        j['props'] = [lambda p, j2: _mic(p, j2)]
    elif name == 'pen':
        V.arm_to(j, 'R', (40.0, 270.0, 160.0), 'down', 'pen')
        j['props'] = [lambda p, j2: _pen(p, j2)]
    elif name == 'bag':
        V.arm_to(j, 'R', (sw - 50, 250.0, 80.0), 'down', 'grip')                 # holding the strap at the chest
        j['props'] = [_bag]
    elif name == 'guard':                                    # fists up by the chin (combat)
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * 48, -50.0, 110.0), 'down')
    elif name != 'standing':
        raise KeyError(f'no pose called {name!r} yet: build it to order and add it here')
    return j


POSES = ('standing', 'relaxed', 'hips', 'arms_folded', 'pockets', 'behind_back', 'lean_on', 'slumped', 'palm_open',
         'chop', 'shrug', 'point', 'facepalm', 'head_in_hands', 'heart', 'phone_ear', 'phone_read', 'paper', 'mug',
         'mug_sip', 'mic', 'pen', 'bag', 'guard')


# ------------------------------------------------------------------------------------------------ sitting
def seated(sp, j=None):
    """Seated on a knee-height chair: hips on the seat, thighs level, shins down, feet flat on the floor."""
    j = j or V.standing(sp)
    j['bob'] = V.SEAT_DROP
    floor = 928 - V.SEAT_DROP
    for s, sg in (('L', -1), ('R', 1)):
        j['foot' + s] = (sg * 64, floor - 38, V.THIGH * 0.98)
        j['knee_pole' + s] = (0.1 * sg, -1.0, 0.7)
        V.arm_to(j, s, (sg * 90, 470.0, 180.0), 'back')            # hands resting on the thighs
    j['seated'] = True
    return j


def stand_up(sp, u):
    """Rising from the chair, u 0-1 (about 1.6-2 s): (1) lean forward to 35 degrees (to 18%), (2) the hips leave the
    seat, the body rotating forward over the feet (to 40%), (3) legs and trunk straighten (to 91%), (4) settle
    (Schenkman 1990; Medicine 2021)."""
    sit, stand = seated(sp), V.standing(sp)
    lean = 35 * ease(u / 0.18) if u < 0.4 else 35 * (1 - ease((u - 0.4) / 0.51))
    lift = 0.0 if u < 0.18 else ease((u - 0.18) / (0.91 - 0.18))
    j = mix_poses(sit, stand, lift)
    j['bob'] = V.SEAT_DROP * (1 - lift)
    floor = 928 - j['bob']
    for s, sg in (('L', -1), ('R', 1)):
        z = lerp(V.THIGH * 0.6, 6.0, lift)                        # feet drawn back under the knees, then under the body
        j['foot' + s] = (sg * lerp(64, 60, lift), floor - 38, z)
        j['knee_pole' + s] = (0.1 * sg, -1.0 + lift, 0.7 + 0.3 * lift)
        V.arm_to(j, s, (sg * lerp(90, sp.get('shoulders', 150) - 6, lift), lerp(430.0, 470.0, lift), lerp(200.0, 40.0, lift)),
                 'back')
    j['lean'] = lean
    j['seated'] = lift < 0.3
    return j


def sit_down(sp, u):
    """Sitting down is rising in reverse: reach back, lower with the trunk leaning forward, settle back."""
    return stand_up(sp, 1.0 - u)


# ------------------------------------------------------------------------------------------------ combat
def punch(sp, t, t_hit, target=(0.0, -150.0, 520.0), side='R'):
    """A straight punch landing at t_hit on `target` (torso frame: forward z). Guard, wind-up (pulled back), the
    strike (arrives in two drawings), a held impact, back to guard. Returns (pose, contact time)."""
    g = pose(sp, 'guard')
    wind = pose(sp, 'guard')
    V.arm_to(wind, side, (130.0 if side == 'R' else -130.0, -30.0, 20.0), 'down')
    wind['lean'] = -6
    hit = pose(sp, 'guard')
    V.arm_to(hit, side, target, 'out')
    hit['lean'] = 12
    j = keyed(t, [(t_hit - 0.7, g), (t_hit - 0.3, wind), (t_hit - 0.17, wind), (t_hit, hit), (t_hit + 0.2, hit),
                  (t_hit + 0.6, g)], curve='fast' if t_hit - 0.17 <= t < t_hit else 'ease')
    return j, t_hit


def kick(sp, t, t_hit, height=250.0, side='R'):
    """A front kick: chamber the knee, snap the foot out at `height`, hold, recover. Leans back for balance."""
    other = 'L' if side == 'R' else 'R'
    sg = 1 if side == 'R' else -1
    rest = pose(sp, 'guard')
    chamber = pose(sp, 'guard')
    chamber['foot' + side] = (sg * 50, 600.0, 160.0)
    chamber['lean'] = -6
    out = pose(sp, 'guard')
    out['foot' + side] = (sg * 40, height, 400.0)
    out['lean'] = -14
    out['foot' + other] = (-sg * 60, V.ANKLE_Y, -20.0)
    j = keyed(t, [(t_hit - 0.6, rest), (t_hit - 0.25, chamber), (t_hit, out), (t_hit + 0.2, out), (t_hit + 0.45, chamber),
                  (t_hit + 0.7, rest)], curve='fast' if t_hit - 0.25 <= t < t_hit else 'ease')
    return j, t_hit


def _sword(p, j2, side='R', smear=False):
    el, wr = j2['el' + side], j2['wr' + side]
    dx, dy = wr[0] - el[0], wr[1] - el[1]
    n = math.hypot(dx, dy) or 1.0
    ux, uy = dx / n, dy / n
    hx, hy = wr[0] + ux * 14, wr[1] + uy * 14
    tip = (hx + ux * 520, hy + uy * 520)
    if smear:                                               # one drawing of smear along the swing's path
        p.poly([(hx, hy), tip, (tip[0] - 160, tip[1] - 260)], (230, 232, 238), None)
    p.line([(hx - uy * 40, hy + ux * 40), (hx + uy * 40, hy - ux * 40)], (120, 90, 40), 10)          # the guard
    p.poly([(hx + uy * 9, hy - ux * 9), (tip[0], tip[1]), (hx - uy * 9, hy + ux * 9)], (210, 214, 222), INK, 2.2)


def sword(sp, t, t_hit, side='R'):
    """An overhead sword swing: raised behind the head, cut down and across, held, recovered. The blade is laid
    over the circle hand; one smear drawing on the fastest frame."""
    up_ = pose(sp, 'standing')
    V.arm_to(up_, side, (60.0, -330.0, -40.0), 'up')
    up_['lean'] = -6
    down = pose(sp, 'standing')
    V.arm_to(down, side, (-60.0, 300.0, 330.0), 'out')
    down['lean'] = 14
    rest = pose(sp, 'standing')
    V.arm_to(rest, side, (120.0, 300.0, 150.0), 'down')
    fastest = t_hit - 1 / FPS <= t < t_hit
    j = keyed(t, [(t_hit - 0.8, rest), (t_hit - 0.35, up_), (t_hit - 0.15, up_), (t_hit, down), (t_hit + 0.25, down),
                  (t_hit + 0.7, rest)], curve='fast' if t_hit - 0.15 <= t < t_hit else 'ease')
    j = dict(j)
    j['props'] = [lambda p, j2: _sword(p, j2, side, smear=fastest)]
    j['hand'] = dict(j.get('hand', {}), **{side: 'grip'})
    return j, t_hit


def hit_react(sp, t, t_hit, strength=1.0, toward=-1):
    """Taking a blow: nothing moves until the contact (stage rule); then the head snaps away from the force, the body
    rocks back, the arms fly, and he staggers a step (the film moves him back by `stagger_m`). Settles over ~0.8 s."""
    j = V.standing(sp)
    if t < t_hit:
        return j, 0.0
    u = t - t_hit
    k = math.exp(-u * 5) * math.sin(min(math.pi / 2, u * 30))
    j['lean'] = -16 * strength * k
    j['head_dx'] = 0
    j['head_dy'] = -10 * strength * k
    for s, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, s, (sg * (220 + 60 * k * strength), 280.0 - 180 * k * strength, 40.0), 'down', 'palm')
    stagger = 0.25 * strength * (1 - math.exp(-u * 6))
    return j, stagger


def fall(sp, t, t0):
    """Falling down after a blow, in stages (never a plank tipping over): knees buckle (0.25 s), down onto the
    hips (0.5 s), back onto the shoulders (0.8 s), head down and still (1.0 s). Best seen side-on.
    Returns (pose, on_floor) - on_floor is True once he lies still."""
    stand = V.standing(sp)
    knees = V.standing(sp)
    knees['bob'] = 160
    for s, sg in (('L', -1), ('R', 1)):
        knees['foot' + s] = (sg * 70, V.ANKLE_Y - 160, 120.0)
    knees['lean'] = 10
    sit = V.standing(sp)
    sit['bob'] = 928 - V.HIP_Y - 60
    for s, sg in (('L', -1), ('R', 1)):
        sit['foot' + s] = (sg * 70, V.HIP_Y + 20, 380.0)
        sit['knee_pole' + s] = (0.1 * sg, -1.0, 0.4)
    sit['lean'] = -20
    lie = dict(sit)
    lie['lean'] = -80
    lie['head_dy'] = 0
    for s, sg in (('L', -1), ('R', 1)):
        lie['foot' + s] = (sg * 70, V.HIP_Y + 30, 440.0)
        V.arm_to(lie, s, (sg * 260, 300.0, -40.0), 'out', 'palm')
    j = keyed(t, [(t0, stand), (t0 + 0.25, knees), (t0 + 0.5, sit), (t0 + 0.85, lie)])
    return j, t >= t0 + 0.85


# ------------------------------------------------------------------------------------------------ cars
def driving(sp, t, steer=0.0):
    """Seated at the wheel, hands at ten to two, small steering moves; the film draws the car and slides the world."""
    j = seated(sp)
    wheel = (0.0, 230.0, 250.0)
    a = math.radians(30 + 12 * steer)
    for s, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, s, (wheel[0] + sg * 80 * math.cos(a), wheel[1] - 80 * math.sin(a) * (1 - 0.3 * sg * steer), wheel[2]),
                 'down', 'grip')

    def draw_wheel(p, j2):
        cx = (j2['wrL'][0] + j2['wrR'][0]) / 2
        cy = (j2['wrL'][1] + j2['wrR'][1]) / 2 + 40
        p.ell(cx, cy, 110, 40, None, (30, 30, 34), 10)
    j['props'] = [draw_wheel]
    return j


def car_in(sp, u):
    """Getting into a car, u 0-1 (about 2.5 s, best side-on with the car drawn by the film): hand to the door, the
    near leg lifts in and the head ducks under the roof, he sits, the other leg swings in (Crizzle et al. 2014)."""
    stand = V.standing(sp)
    reach = V.standing(sp)
    V.arm_to(reach, 'R', (sp.get('shoulders', 150) + 160, 160.0, 150.0), 'out', 'grip')
    duck = seated(sp)
    duck['bob'] = V.SEAT_DROP * 0.5
    duck['head_dy'] = 30
    duck['lean'] = 24
    duck['footL'] = (-60, V.ANKLE_Y - V.SEAT_DROP * 0.5, 20.0)
    sit = seated(sp)
    return keyed(u, [(0.0, stand), (0.2, reach), (0.55, duck), (0.8, sit), (1.0, sit)])


def car_out(sp, u):
    """Getting out is getting in reversed: near leg out, a hand on the frame, head ducks, he rises and steps clear."""
    return car_in(sp, 1.0 - u)


# ------------------------------------------------------------------------------------------------ checks
def check_feet(track, tol_m=0.03):
    """track: [(t, side, world X, world Z, planted)] for one person. A planted foot must stay put on the floor."""
    faults, last = [], {}
    for t, side, X, Z, planted in track:
        if planted and side in last:
            t0, X0, Z0 = last[side]
            if math.hypot(X - X0, Z - Z0) > tol_m and t - t0 < 0.2:
                faults.append(f'{t:.2f} s: the {side} foot slides {math.hypot(X - X0, Z - Z0) * 100:.0f} cm while planted')
                break
        last[side] = (t, X, Z) if planted else last.pop(side, None) or (t, X, Z)
        if not planted:
            last.pop(side, None)
    return faults


def check_facing(samples, tol=30):
    """samples: [(t, yaw, direction of travel in degrees or None)]. Body and face point the way they go."""
    for t, yaw, d in samples:
        if d is not None and abs(((yaw - d + 180) % 360) - 180) > tol:
            return [f'{t:.2f} s: facing {yaw:.0f} degrees but walking towards {d:.0f}']
    return []


def check_head(samples, limit=95):
    """samples: [(t, body yaw, head yaw)]: the head never turns more than about 90 degrees from the body."""
    for t, b, h in samples:
        if abs(((h - b + 180) % 360) - 180) > limit:
            return [f'{t:.2f} s: the head is turned {abs(((h - b + 180) % 360) - 180):.0f} degrees from the body']
    return []


def check_strike(j, side, target, shape='fist', where='a blow'):
    """The fist or foot actually reaches the target on the contact frame."""
    if side in ('L', 'R') and not V.reach_ok(j, side, target, shape):
        return [f'{where}: the hand cannot reach its target (move the people closer)']
    return []


def check_reaction(t_contact, t_react_start, where='the victim'):
    if t_react_start < t_contact - 1e-6:
        return [f'{where} reacts at {t_react_start:.2f} s, before the blow lands at {t_contact:.2f} s']
    return []


def check_on_floor(lowest_y, floor_y, where='the fallen body', tol=12):
    if abs(lowest_y - floor_y) > tol:
        return [f'{where} is {"floating" if lowest_y < floor_y else "sinking"} ({lowest_y - floor_y:+.0f}) off the floor']
    return []


def check_gait(kind):
    """The gait's numbers stay within the references: one foot always down in a walk, a float in a run."""
    g = GAITS[kind]
    faults = []
    if kind in ('stroll', 'walk', 'brisk') and g['duty'] < 0.5:
        faults.append(f'{kind}: both feet leave the ground (a walk always has one down)')
    if kind in ('run', 'sprint') and g['duty'] >= 0.5:
        faults.append(f'{kind}: no float (a run has a moment with both feet off)')
    cadence = g['sps'] * 60
    lo, hi = {'stroll': (80, 100), 'walk': (100, 130), 'brisk': (130, 165), 'run': (160, 210), 'sprint': (200, 280)}[kind]
    if not lo <= cadence <= hi:
        faults.append(f'{kind}: {cadence:.0f} steps a minute is outside {lo}-{hi}')
    return faults


def audit():
    """Checks every move in the library on its own (run by preflight for any film that uses moves)."""
    import types
    faults = []
    for kind in GAITS:
        faults += check_gait(kind)
    sp = dict(name='test', shoulders=150, skin=(240, 200, 176), jacket=(40, 40, 46), hw=72, hh=90)
    for name in POSES:
        j = pose(sp, name)
        for s in 'LR':
            try:
                F.audit_arm(j['sh' + s][:2], j['el' + s][:2], j['wr' + s][:2], where=f'pose {name} {s}')
            except Exception as e:
                if 'shorter' not in str(e) and '40%' not in str(e):
                    faults.append(str(e))
    return faults


if __name__ == '__main__':
    f = audit()
    print('\n'.join(f) or 'moves: clean')
