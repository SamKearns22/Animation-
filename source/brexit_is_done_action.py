#!/usr/bin/env python3
"""Open Wounds (brexit-is-done): the background action, beat by beat as notes/brexit-is-done-sets.md's tables
(rule 74; Sam's items 6-9 for shot 2, 13 for shot 3). Every actor is (depth m, draw(img)); the film paints them in
among the place's pieces far to near (places.paint_with), so a man on a scaffold lift is between its inner and outer
frames and a wolf behind Kemi is hidden by her.

MAP (rule 61)
  setup ............ sizes: WOLF_SHOULDER (0.85 m: half a man), the site's depths (ATTACK, LIFT_D, lifts), keyed()
  placing .......... wolf_at(img, L, x, d, z, face, P, ...): a kit wolf through a level camera, its shadow first;
                     person_at(img, L, sp, x, d, z, yaw, j, t); tube(): a held steel tube between two hands
  shot 2: attack ... w1(u): W1 digs, Wa and Wb leap from the left (0.2), knock him down (0.6, lying.fall: the 3D body
                     from the hips down), feed on him the whole shot out of step; his hat flies and rolls, the shovel
                     falls, scraps of hi-vis, chunks and blood (the approved plan: drops land and soak in)
  shot 2: runner ... runner(u): W2 sprints left along the 9.6 m lift (1.5), leaps off the end out of frame (4.6);
                     Wc and Wd 2-3 m behind, skid at the end (4.8), snarl down, turn (two front-on frames) and pace
                     back (6.0)
  shot 2: bars ..... bars(u): W3-W5 on the 6.4 m lift, two-hand tubes, jab as a wolf lunges (a step back first);
                     We and Wf lunge in turn and flinch when struck; Wg circles; W5's swing clangs on a standard
  shot 2: milling .. milling(u): Wh sits (tail sweeps, looks round), Wi paws the dirt (grooves stay), Wj and Wk walk
                     across, one each way; hard hats, vests, blood-drenched (item 9)
  shot 2 ........... site_actors(t, L): all of the above for shot time t
  shot 3 ........... room_actors(t, L): (next) the guests through the doors, Wl-Wo chasing, the lunger Wp
"""
import math
import os
import random
import sys

from PIL import ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figure as FG                  # noqa: E402
import lying                         # noqa: E402
import moves as MV                   # noqa: E402
import people as PK                  # noqa: E402
import people_parts as PPt           # noqa: E402
import wolf as WF                    # noqa: E402
from satire_style import Cam as SCam, Ctx, OUT   # noqa: E402

B = PPt.B
V = PPt.V
FEET = 928.0

# ================================================================================================= setup
WOLF_SHOULDER = 0.85                 # m: half a man's height (Cry Minister's dire wolves; the kit's s=1 is 200 units)
UNITS = 200.0 / WOLF_SHOULDER        # wolf units a metre
ATTACK = dict(x=-1.75, d=7.0)        # W1 digging, low left (places file: people attack 7)
LIFT_D = 24.95                       # between the scaffold's inner (25.6) and outer (24.3) frames: the boards
TOP, MID = 9.6, 6.4                  # the runner's lift, the bar fight's lift (board tops, m)
CROWD = PK.crowds('brexit-is-done')
WORKERS = [PK.crowd_person(CROWD['worker'], i) for i in range(5)]
GUESTS = [PK.crowd_person(CROWD['guest'], i) for i in range(4)]


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def keyed(t, keys):
    """A number from (time, value) keys, eased between them, held outside."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            return lerp(v0, v1, ease((t - t0) / (t1 - t0)))
    return keys[-1][1]


# ================================================================================================= placing
def _ctx(img, s):
    X = Ctx(ImageDraw.Draw(img), SCam(540, 960, 1.0, 1), ol=max(1.0, 5.0 * s))
    return X


def wolf_s(L, d):
    return WOLF_SHOULDER * L.ppm(d) / 200.0


def wolf_at(img, L, x, d, z, face, P, pal=0, wear=None, blood=0.0, seed=0, shade=True):
    """A kit wolf whose body middle stands over (x, d) at height z (m) through level camera L; returns its jaws."""
    s = wolf_s(L, d)
    px, py = L.p(x, d, z)
    X = _ctx(img, s)
    if shade and z < L.up:                          # above the lens we see the boards' undersides: no shadow
        WF.shadow(X, px, py, s, face, P)
    return WF.draw(X, px, py, s, face, pal, P, wear=wear, blood=blood, seed=seed)


def wolf_front_at(img, L, x, d, z, pal=0, wear=None, blood=0.0, seed=0, **kw):
    s = wolf_s(L, d)
    px, py = L.p(x, d, z)
    X = _ctx(img, s)
    if z < L.up:
        WF._blend(X).ellipse([px - 70 * s, py - 8 * s, px + 70 * s, py + 8 * s], fill=(0, 0, 0, 60))
    WF.draw_front(X, px, py, s, pal, wear=wear, blood=blood, seed=seed, **kw)


def scale_at(L, d, sp):
    return L.ppm(d) * sp['height'] * 0.84 / FEET


def person_at(img, L, sp, x, d, z, yaw, j, t, shadow=True):
    """Someone standing on a floor at height z (m), depth d, across x (m) through L; returns the drawn joints."""
    s = scale_at(L, d, sp)
    px, py = L.p(x, d, z)
    if shadow and z < L.up:
        dd = ImageDraw.Draw(img, 'RGBA')
        dd.ellipse([px - 150 * s, py - 18 * s, px + 150 * s, py + 18 * s], fill=(0, 0, 0, 55))
    B.SS = 1
    jj = V.person(img, B.Cam(1.0, 540, 960), px, py - FEET * s, s, sp, t, yaw, j)
    return _screen(jj, px, py - FEET * s, s, yaw)


def _screen(jj, x, y, s, yaw):
    """views.person's returned points are in person units from the neck base: add the screen ones (key + '_px')."""
    jj = dict(jj)
    deg, mirror = V.snap(yaw)
    s = -s if mirror and deg not in (0, 180) else s
    for k in ('wrL', 'wrR', 'elL', 'elR', 'shL', 'shR'):
        if k in jj:
            jj[k + '_px'] = (x + jj[k][0] * s, y + jj[k][1] * abs(s))
    return jj


def tube(img, a, b, w, col=(150, 156, 164)):
    """A steel scaffold tube from a to b (screen), w px thick, one outline."""
    d = ImageDraw.Draw(img)
    d.line([a, b], fill=OUT, width=max(2, int(w + 2)))
    d.line([a, b], fill=col, width=max(1, int(w)))


# ================================================================================================= shot 2: attack
WA = dict(d=6.75, land=-0.62, pal=1, seed=21)      # nearer him: lands over his chest
WB = dict(d=7.3, land=-1.42, pal=3, seed=22)       # behind him: over his belly and legs
RUN_V = 9.0                                         # m/s, the wolves' charge
HIT = 0.6                                           # they hit him
FEEDS = {'a': (1.05, 1.7, 0.0), 'b': (1.25, 2.1, 0.5)}   # (first rip, period, phase): out of step


def _feed_u(u, start, period):
    """Feeding: head down in the kill (worrying), a rip up to the sky (0.3 s), held with the hunk (0.3 s), back down."""
    if u < start:
        return 0.0, -1
    k, v = divmod(u - start, period)
    down = period - 0.85
    if v < down:
        return 0.06 * (0.5 + 0.5 * math.sin(v * 14)), int(k) - 1
    v -= down
    if v < 0.3:
        return ease(v / 0.3), int(k)
    if v < 0.6:
        return 1.0, int(k)
    return 1.0 - ease((v - 0.6) / 0.25), int(k)


def _rips(start, period, until):
    out, k = [], 0
    while start + k * period + period - 0.85 + 0.2 < until:
        out.append(start + k * period + period - 0.85 + 0.2)
        k += 1
    return out


def _attack_wolf(img, L, u, w, key, blood_k):
    """One of the two: charges in from off frame left, leaps (0.2-0.6), lands on him, feeds."""
    s = wolf_s(L, w['d'])
    gy = L.p(0, w['d'], 0)[1]
    x_leap0 = w['land'] - 1.9
    if u < 0.2:                                     # the charge
        x = x_leap0 - RUN_V * (0.2 - u)
        P = WF.pose('run', (x - (x_leap0 - RUN_V * 0.2)) * UNITS)
    elif u < HIT:                                   # the leap: off the ground at 0.2, onto him at 0.6
        v = (u - 0.2) / (HIT - 0.2)
        x = lerp(x_leap0, w['land'], v)
        P = WF.pose('leap', v, lift=150 * math.sin(math.pi * v) + 40 * v)
    elif u < 0.95:
        x = w['land']
        P = WF.pose('land', (u - HIT) / 0.35)
    else:
        x = w['land']
        st, per, ph = FEEDS[key]
        f, _ = _feed_u(u, st, per)
        P = WF.pose('feed', f, hunk=(w['seed'] if f > 0.55 else None))
    bl = dict(muzzle=min(1.0, blood_k * 1.2), ruff=min(1.0, blood_k), paws=min(1.0, blood_k * 0.9))
    jaws = wolf_at(img, L, x, w['d'], 0.0, 1, P, w['pal'], blood=bl if blood_k > 0 else 0.0, seed=w['seed'])
    X = _ctx(img, s)
    for t0 in (0.2, HIT + 0.02):                   # dust where it takes off and where it lands
        px = L.p(x_leap0 if t0 < 0.5 else w['land'], w['d'], 0)[0]
        WF.dust(X, px, gy, s, u - t0, seed=int(w['seed'] + t0 * 10), size=1.1)
    return jaws


def _worker1_pose(sp, u):
    """Digging: bent over the shovel, the blade in the dirt, a push down on the handle every 0.6 s."""
    j = V.standing(sp)
    push = 0.5 + 0.5 * math.sin(u * 2 * math.pi / 0.6)
    j['lean'] = 16 + 6 * push
    V.arm_to(j, 'R', (30.0, 300.0 + 30 * push, 170.0), 'out', 'fist')
    V.arm_to(j, 'L', (-20.0, 470.0 + 30 * push, 270.0), 'out', 'fist')
    j['footR'] = (50, j['footR'][1], -60.0)
    j['footL'] = (-50, j['footL'][1], 90.0)
    return j


def _shovel(img, L, a, b, d):
    """The shovel: a wooden shaft from the top grip a to the blade's heel b (screen points), the blade beyond."""
    pxm = L.ppm(d)
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1.0
    ux, uy = dx / n, dy / n
    tube(img, a, b, 0.035 * pxm, (150, 110, 64))
    bl = 0.28 * pxm
    hw = 0.11 * pxm
    q = [(b[0] - uy * hw, b[1] + ux * hw), (b[0] + uy * hw, b[1] - ux * hw),
         (b[0] + ux * bl + uy * hw * 0.7, b[1] + uy * bl - ux * hw * 0.7),
         (b[0] + ux * bl * 1.15, b[1] + uy * bl * 1.15),
         (b[0] + ux * bl - uy * hw * 0.7, b[1] + uy * bl + ux * hw * 0.7)]
    ImageDraw.Draw(img).polygon(q, fill=(150, 154, 160), outline=OUT)


def w1(img, L, cam3, u):
    """W1 and the two wolves on him: returns [(depth, draw)]."""
    sp = dict(WORKERS[0])
    x, d = ATTACK['x'], ATTACK['d']
    gy = L.p(0, d, 0)[1]
    rips = {k: _rips(*FEEDS[k][:2], 11.0) for k in FEEDS}
    out = []

    def man(img):
        if u < HIT:
            j = _worker1_pose(sp, u)
            got = lying.stand(img, cam3, sp, x, d, (-1.0, 0.0), j, u)
            if got[0] == '2d':
                Xf, Yf, s, _, _ = lying.place(cam3, x, d)
                jj = _screen(got[1], Xf, Yf - FEET * s, s, cam3.yaw_of((x, 0, d), (-1.0, 0.0)))
                a, b = jj['wrR_px'], jj['wrL_px']
                # the shaft runs through both hands and on down to the blade, in the dirt ahead of him
                gy = L.p(0, d, 0.0)[1] - 0.2 * L.ppm(d)
                k = (gy - a[1]) / max(1.0, b[1] - a[1])
                heel = (a[0] + (b[0] - a[0]) * k, gy)
                _shovel(img, L, (a[0] - (b[0] - a[0]) * 0.35, a[1] - (b[1] - a[1]) * 0.35), heel, d)
            return
        bare = dict(sp, kit_hat=None)                              # the hat flies off at the hit
        kind, *rest = lying.fall(bare, u, HIT, x, d, (-1.0, 0.0))
        if kind == 'views':
            lying.stand(img, cam3, bare, x, d, (-1.0, 0.0), rest[0], u)
            return
        k, surf = rest
        if u < 3.0:                                                # boots kicking under them, still by 3 s
            k = {n: (v.copy() if hasattr(v, 'copy') else v) for n, v in k.items()}
            fade = max(0.0, 1.0 - (u - 1.1) / 1.9)
            for side, ph in (('L', 0.0), ('R', 1.9)):
                lift = 0.16 * fade * max(0.0, math.sin(u * 9.0 + ph))
                k['an' + side] = k['an' + side] + [0.0, lift, 0.0]
                k['toe' + side] = k['toe' + side] + [0.0, lift, 0.0]
                k['kn' + side] = k['kn' + side] + [0.0, lift * 0.6, 0.0]
        lying.draw(img, cam3, k, bare, u, surfaces=surf)

    def ground(img):                                               # on the dirt: pool, soaked drops, the props
        s = wolf_s(L, d)
        X = _ctx(img, s)
        if u > 1.0:
            WF.blood(X, L.p(x + 0.9, d - 0.05, 0)[0], gy + 2, 60 * s * min(1.0, (u - 1.0) / 3.0) + 8 * s, 3, 0.18)
        # the shovel: falls from his hands at the hit, tips over, lands flat on the dirt (1.0), still
        if u >= HIT:
            v = min(1.0, (u - HIT) / 0.4)
            ang = lerp(1.0, 0.0, v * v)                            # pivots on its blade, handle down to the dirt
            bounce = 0.05 * math.sin(math.pi * min(1.0, (u - HIT - 0.4) / 0.15)) if u > HIT + 0.4 else 0.0
            hx, hd, ln = x - 0.62, d - 0.12, 1.05
            top = L.p(hx + ln * math.cos(ang), hd, 0.04 + ln * math.sin(ang) + bounce)
            _shovel(img, L, top, L.p(hx, hd, 0.04 + 0.5 * bounce), d)
        # the hard hat: off his head at the hit, up and back, tumbling, lands (1.25), rolls to rest (1.8)
        if u >= HIT:
            v = u - HIT
            hx0, hz0 = x + 0.12, 1.68
            if v < 0.65:
                hx, hz = hx0 + 1.5 * v, hz0 + 2.4 * v - 4.9 * v * v * 1.6
                hz = max(0.12, hz)
                ang = 9.0 * v
            else:
                w = min(1.0, (v - 0.65) / 0.55)
                hx, hz = hx0 + 1.5 * 0.65 + 0.5 * (1 - (1 - w) ** 2), 0.12
                ang = 9.0 * 0.65 + 2.2 * (1 - (1 - w) ** 2)
                ang = round(ang / math.pi) * math.pi + (ang - round(ang / math.pi) * math.pi) * (1 - w)
            hp = L.p(hx, d + 0.2, hz)
            WF.hat_prop(X, hp[0], hp[1], 0.55 * L.ppm(d) / 157.0 * 1.0, ang, 1, blood=0.0, seed=4)
        for i, (t0, vx, ang0) in enumerate(((1.4, -1.1, 0.4), (2.6, 1.3, -0.6), (4.1, -0.7, 1.1))):
            if u >= t0:                                            # torn hi-vis scraps flung from the kill, land, stay
                v = min(u - t0, 0.55)
                sx = x + 0.6 + vx * v
                sz = max(0.03, 0.6 + 2.6 * v - 4.9 * v * v * 1.4)
                q = L.p(sx, d - 0.3 + 0.2 * i, sz)
                WF.scrap(X, q[0], q[1], 0.5 * s / 0.67 * 0.67, ang0 + 3 * v, col=0, seed=10 + i)
        for key, w in (('a', WA), ('b', WB)):                      # blood from each rip: arcs that land and soak in
            for n, tr in enumerate(rips[key]):
                if u >= tr:
                    jx = L.p(w['land'] + 0.55, w['d'], 0)[0]
                    WF.drops(X, jx, L.p(0, w['d'], 0.9)[1], L.p(0, w['d'], 0)[1] + 3, s, u - tr,
                             seed=int(100 * n + ord(key)), n=7, power=0.8, face=(1 if n % 2 else -1))

    def wa(img):
        _attack_wolf(img, L, u, WA, 'a', min(1.0, max(0.0, (u - 0.9) / 2.5)))

    def wb(img):
        _attack_wolf(img, L, u, WB, 'b', min(1.0, max(0.0, (u - 1.1) / 3.0)))

    out += [(WB['d'], wb), (d + 0.01, ground), (d, man), (WA['d'], wa)]
    return out


# ================================================================================================= shot 2: runner
RUN_FROM, RUN_T0, LEAP_T = 13.4, 1.5, 4.6
RUN_SPEED = (RUN_FROM - (-11.6)) / (LEAP_T - RUN_T0)    # m/s: he reaches the lift's end as he leaps


def _runner_x(u):
    return RUN_FROM - RUN_SPEED * (u - RUN_T0)


def runner(img_unused, L, u):
    """W2 on the 9.6 m lift and the two wolves after him."""
    sp = dict(WORKERS[1])
    out = []

    def man(img):
        if u < RUN_T0 - 0.01 or u > LEAP_T + 0.6:
            return
        x = _runner_x(min(u, LEAP_T))
        z = TOP
        j = MV.gait(sp, u - RUN_T0, 'sprint', stride=1.5 / V.M_PER_UNIT, steps_per_s=RUN_SPEED / 1.5)
        if u > LEAP_T:                                             # the leap: up over the end rail, out of frame left
            v = u - LEAP_T
            x -= RUN_SPEED * v
            z += 3.2 * v - 4.9 * v * v
            j = MV.gait(sp, 0.12, 'sprint')
            j['lean'] = 18
            for s_, sg in (('L', -1), ('R', 1)):
                V.arm_to(j, s_, (sg * 200.0, 60.0, 200.0), 'out', 'palm')
        with FG.allow('a sprint seen side on: the back arm swings behind the body (moves.gait)'):
            person_at(img, L, sp, x, LIFT_D, z, -90.0, j, u, shadow=u <= LEAP_T)

    def wolf(img, k):
        lag = (2.3, 3.1)[k]
        x_stop = (-11.0, -10.1)[k]
        d = LIFT_D + (0.18, -0.15)[k]
        if u < RUN_T0:
            return
        x = min(RUN_FROM + lag - RUN_SPEED * (u - RUN_T0), 99.0)
        t_skid = RUN_T0 + (RUN_FROM + lag - x_stop - 0.9) / RUN_SPEED   # where the skid starts
        blood = 0.0
        if u < t_skid:
            P = WF.pose('run', (RUN_FROM + lag - x) * UNITS)
            face = -1
            wolf_at(img, L, x, d, TOP, face, P, pal=(0, 4)[k], seed=30 + k, blood=blood)
            return
        if u < t_skid + 0.45:                                       # skid to a halt at the end, dust thrown ahead
            v = (u - t_skid) / 0.45
            x = x_stop + 0.9 * (1 - (1 - v) ** 2) * -1 + 0.9
            P = WF.pose('skid', v)
            wolf_at(img, L, x, d, TOP, -1, P, pal=(0, 4)[k], seed=30 + k)
            s = wolf_s(L, d)
            X = _ctx(img, s)
            px, py = L.p(x - 0.3, d, TOP)
            WF.dust(X, px, py, s, u - t_skid, seed=40 + k, spray=1.0, size=1.2)
            return
        back = 6.0 + 0.25 * k
        if u < back:                                                # snarling down over the edge
            P = WF.pose('stand', 0.0, neck=0.35, pitch=0.3, jaw=0.6 + 0.2 * math.sin(u * 11 + k), snarl=1.0)
            wolf_at(img, L, x_stop, d, TOP, -1, P, pal=(0, 4)[k], seed=30 + k)
            return
        if u < back + 0.17:                                         # turning round: two frames front on
            wolf_front_at(img, L, x_stop, d, TOP, pal=(0, 4)[k], seed=30 + k, jaw=0.3)
            return
        dist = 1.3 * (u - back - 0.17)                              # pacing back along the boards
        P = WF.pose('walk', dist * UNITS)
        wolf_at(img, L, x_stop + dist, d, TOP, 1, P, pal=(0, 4)[k], seed=30 + k)

    out += [(LIFT_D + 0.18, lambda img: wolf(img, 0)), (LIFT_D, man), (LIFT_D - 0.15, lambda img: wolf(img, 1))]
    return out


# ================================================================================================= shot 2: bars
BAR_MEN = [dict(i=2, x=9.95, d=LIFT_D - 0.2), dict(i=3, x=10.75, d=LIFT_D + 0.25), dict(i=4, x=11.6, d=LIFT_D)]
LUNGES = [(0.5 + 1.5 * k, k % 2) for k in range(7)]          # (time, which wolf): We and Wf in turn
STRIKE = 0.32                                                 # the tube lands this long after the lunge starts
CLANG = 4.3                                                   # W5's swing stops dead on the outer standard at x 11


def _bar_man(sp, u, who):
    """Two hands on the tube at chest height; before a strike he leans back (the wolf comes), then jabs (fast) and
    draws back. Returns (pose, jab 0-1)."""
    j = V.standing(sp)
    jab = 0.0
    lean = 0.0
    for t0, k in LUNGES:
        if (who == 0 and k == 0) or (who == 1 and k == 1):
            v = u - t0
            if 0.0 <= v < STRIKE:
                lean = -8 * ease(v / STRIKE)
                jab = -0.25 * ease(v / STRIKE)
            elif STRIKE <= v < STRIKE + 0.12:
                jab = lerp(-0.25, 1.0, (v - STRIKE) / 0.12)
            elif STRIKE + 0.12 <= v < STRIKE + 0.6:
                jab = 1.0 - ease((v - STRIKE - 0.12) / 0.48)
    j['lean'] = 4 + lean + 6 * max(0.0, jab)
    j['footL'] = (-50, j['footL'][1], 110.0)
    j['footR'] = (50, j['footR'][1], -90.0)
    reach = 150 + 160 * jab
    V.arm_to(j, 'L', (-40.0, 230.0, reach + 110), 'down', 'fist')
    V.arm_to(j, 'R', (40.0, 250.0, max(130.0, reach - 30)), 'down', 'fist')
    return j, jab


def bars(L, u):
    out = []
    for n, m in enumerate(BAR_MEN):
        def man(img, n=n, m=m):
            sp = dict(WORKERS[m['i']])
            if n < 2:
                j, jab = _bar_man(sp, u, n)
            else:                                                   # W5: an overhead swing that clangs on a standard
                j = V.standing(sp)
                v = (u - (CLANG - 0.45))
                ang = keyed(v, [(0.0, 0.0), (0.3, 1.0), (0.45, 0.55), (0.52, 0.62), (0.7, 0.58), (1.6, 0.0)])
                j['lean'] = 4 + 8 * ang
                hy = 300.0 - 260.0 * math.sin(math.pi * ang * 0.9)
                V.arm_to(j, 'L', (-40.0, hy, 240.0 - 40 * ang), 'down', 'fist')
                V.arm_to(j, 'R', (40.0, hy + 40, 140.0 - 20 * ang), 'down', 'fist')
                jab = 0.0
            jj = person_at(img, L, sp, m['x'], m['d'], MID, -90.0, j, u)
            a, b = jj['wrR_px'], jj['wrL_px']                       # back hand, front hand
            dx, dy = b[0] - a[0], b[1] - a[1]
            nn = math.hypot(dx, dy) or 1.0
            pxm = L.ppm(m['d'])
            if n == 2:                                              # the swing's tube pivots in his hands; stopped
                tip_len = 1.5 * pxm
                ang = math.atan2(dy, dx)
                tip = (b[0] + math.cos(ang) * tip_len, b[1] + math.sin(ang) * tip_len)
                stx = L.p(11.0, LIFT_D, 0)[0]                       # the standard it must not pass through
                if tip[0] < stx and b[0] > stx:
                    k = (b[0] - stx) / max(1e-3, b[0] - tip[0])
                    tip = (stx, b[1] + (tip[1] - b[1]) * k)
                tube(img, (a[0] - dx / nn * 0.3 * pxm, a[1] - dy / nn * 0.3 * pxm), tip, 0.05 * pxm + 1)
            else:
                tube(img, (a[0] - dx / nn * 0.4 * pxm, a[1] - dy / nn * 0.4 * pxm),
                     (b[0] + dx / nn * 1.3 * pxm, b[1] + dy / nn * 1.3 * pxm), 0.05 * pxm + 1)
        out.append((m['d'], man))

    for k in range(2):                                              # We and Wf: lunge in turn, struck, flinch
        def wolf(img, k=k):
            d = (LIFT_D - 0.05, LIFT_D + 0.3)[k]
            x = (8.45, 9.25)[k]
            P = WF.pose('stand', 0.0, neck=-0.1, jaw=0.5, snarl=1.0)
            for t0, kk in LUNGES:
                if kk != k:
                    continue
                v = u - t0
                if 0.0 <= v < STRIKE:
                    P = WF.pose('lunge', ease(v / STRIKE))
                elif STRIKE <= v < STRIKE + 0.9:
                    w = v - STRIKE
                    fl = min(1.0, w / 0.12) if w < 0.4 else max(0.0, 1.0 - (w - 0.4) / 0.5)
                    P = WF.pose('lunge', 1.0 - min(1.0, w / 0.5), flinch=fl)
            wolf_at(img, L, x, d, MID, 1, P, pal=(2, 3)[k], seed=50 + k)
        out.append(((LIFT_D - 0.05, LIFT_D + 0.3)[k], wolf))

    def wg(img):                                                    # Wg circles behind them on the boards
        per = 4.4
        v = (u % per) / per
        d = LIFT_D + 0.45
        if v < 0.45:
            x, face, dist = 7.7 + 1.0 * (v / 0.45), 1, v * per * 0.55
        elif v < 0.5:
            wolf_front_at(img, L, 8.7, d, MID, pal=4, seed=52, jaw=0.4)
            return
        elif v < 0.95:
            x, face, dist = 8.7 - 1.0 * ((v - 0.5) / 0.45), -1, (v - 0.5) * per * 0.55
        else:
            wolf_front_at(img, L, 7.7, d, MID, pal=4, seed=52, jaw=0.4)
            return
        wolf_at(img, L, x, d, MID, face, WF.pose('walk', dist * UNITS, jaw=0.4, snarl=0.8), pal=4, seed=52)
    out.append((LIFT_D + 0.45, wg))
    return out


# ================================================================================================= shot 2: milling
WEAR = dict(hat=0, vest=0, torn=0.6)
BLOODY = dict(muzzle=1.0, ruff=0.9, paws=0.9, vest=0.8)


def milling(L, u):
    out = []

    def wh(img):                                                    # sits, tail sweeping, looks round now and then
        back = (u % 3.4) > 2.2
        wolf_at(img, L, -3.1, 13.0, 0.0, 1, WF.pose('sit', u, back=back), pal=0,
                wear=dict(hat=1, vest=0, torn=0.6), blood=BLOODY, seed=60)
    out.append((13.0, wh))

    def wi(img):                                                    # paws the dirt; each rake leaves a groove that stays
        d, x = 11.0, -1.5
        s = wolf_s(L, d)
        px, py = L.p(x, d, 0)
        X = _ctx(img, s)
        rakes = max(0.0, u / 0.9)
        WF.scrape(X, px + (WF.HOME['ff'] - 20) * s, py + 2, s, min(rakes, 4.0), seed=61)
        P = WF.pose('paw', rakes)
        wolf_at(img, L, x, d, 0.0, 1, P, pal=1, wear=dict(hat=2, vest=1, torn=0.4), blood=BLOODY, seed=61)
        k = int(rakes)
        if k >= 1:
            WF.dust(X, px + (WF.HOME['ff'] - 30) * s, py, s, (rakes - k) * 0.9, seed=62 + k, size=0.7)
    out.append((11.0, wi))

    def walker(img, x0, vx, d, face, pal, hat, vest, seed):
        x = x0 + vx * u
        wolf_at(img, L, x, d, 0.0, face, WF.pose('walk', abs(vx) * u * UNITS), pal=pal,
                wear=dict(hat=hat, vest=vest, torn=0.5), blood=BLOODY, seed=seed)
    out.append((14.0, lambda img: walker(img, -7.6, 0.85, 14.0, 1, 3, 0, 1, 63)))
    out.append((11.6, lambda img: walker(img, 1.6, -1.0, 11.6, -1, 2, 2, 0, 64)))
    return out


# ================================================================================================= shot 2
def set_cam(L):
    """The level camera as a 3D set camera (lying.py's bodies and floor-placed people need one)."""
    import sets
    return sets.Cam((0.0, L.up, 0.0), (0.0, L.up, 1.0), focal=L.L, shake=(L.c - 540.0, L.hz - 960.0))


def site_actors(u, L):
    """Every background actor of shot 2 at shot time u: [(depth, draw)]."""
    cam3 = set_cam(L)
    return w1(None, L, cam3, u) + runner(None, L, u) + bars(L, u) + milling(L, u)
