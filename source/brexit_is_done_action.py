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
  shot 3 ........... PASSES (who runs where when), along(); _guest_pose (front_run out of the doors, side on
                     across; the butler's tray hand); tray_state/_tray/_flute/_glass_down (the tray flies, hops,
                     rattles flat; glasses shatter, pools stay); lunger(img, L, u) (Wp at 9.0, cut 9.4);
                     room_actors(u, L) -> (room actors far to near, those seen through the doorway)
"""
import math
import os
import random
import sys

from PIL import ImageDraw

from ink import glaze

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figure as FG                  # noqa: E402
import lying                         # noqa: E402
import moves as MV                   # noqa: E402
along = MV.along
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
ATTACK = dict(x=-1.4, d=7.0)         # W1 digging in the open ground left of Kemi (note 13; places file: people attack 7)
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
    """Note 16: the house line weight (wolf.house_ctx), the people's own at the wolf's depth."""
    X = Ctx(ImageDraw.Draw(img), SCam(540, 960, 1.0, 1), ol=max(1.0, 5.0 * s))
    return WF.house_ctx(X, s, s * 200.0 / WOLF_SHOULDER)


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
    s = wolf_s(L, d) * WF.FRONT_K                   # the front view at the side view's real size (wolf.FRONT_K)
    px, py = L.p(x, d, z)
    X = _ctx(img, s)
    if z < L.up:
        WF._blend(X).ellipse([px - 90 * s, py - 10 * s, px + 90 * s, py + 10 * s], fill=(0, 0, 0, 60))
    WF.draw_front(X, px, py, s, pal, wear=wear, blood=blood, seed=seed, **kw)


def scale_at(L, d, sp):
    return L.ppm(d) * sp['height'] * 0.84 / FEET


def person_at(img, L, sp, x, d, z, yaw, j, t, shadow=True):
    """Someone standing on a floor at height z (m), depth d, across x (m) through L; returns the drawn joints."""
    s = scale_at(L, d, sp)
    px, py = L.p(x, d, z)
    if shadow and z < L.up:
        dd = glaze(img)
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


def grip_hands(img, jj, s, sp, sides=('L', 'R')):
    """The circle hands drawn again over a held tube (chat 18, rule 41: the tube laid over two small hands hid them,
    'an arm with no hand'): a grip reads as the hand closed round the tube, so the hand is on top. Same circle as
    satire_style.gesture_hand (r 26, 12 out along the forearm)."""
    from satire_style import OUT as LINE
    d = ImageDraw.Draw(img)
    skin = tuple(sp.get('skin', (200, 150, 110)))[:3]
    for sd in sides:
        el, wr = jj.get('el' + sd + '_px'), jj.get('wr' + sd + '_px')
        if not el or not wr:
            continue
        dx, dy = wr[0] - el[0], wr[1] - el[1]
        n = math.hypot(dx, dy) or 1.0
        k = abs(s)
        cx, cy, r = wr[0] + dx / n * 12 * k, wr[1] + dy / n * 12 * k, 26 * k
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=skin, outline=LINE, width=max(1, int(round(2.4 * k))))


def tube(img, a, b, w, col=(150, 156, 164)):
    """A steel scaffold tube from a to b (screen), w px thick, one outline."""
    d = ImageDraw.Draw(img)
    d.line([a, b], fill=OUT, width=max(2, int(w + 2)))
    d.line([a, b], fill=col, width=max(1, int(w)))


# ================================================================================================= shot 2: attack
# Note 13 (Sam, 26 Nov: "you don't get a moment to take in the scene"; "the wolves jump over the construction worker
# and go past him, yet the construction worker does the falling down motion"; "see the wolves doing their pounce,
# landing on him, and at the moment they land on him, that's when he falls"; as Cry Minister's short leap ONTO the
# man, none overshooting): he stands in the open ground left of Kemi; the attack's clock runs LEAD s late (a beat of
# him digging first); each wolf runs in, crouches, springs a short pounce whose forepaws strike him where he is
# (WA his chest at HIT, WB his hips as he buckles, 0.2 s later), rides him down as he falls, then feeds.
LEAD = 1.1                                          # s of the shot before the attack's own clock starts
WA = dict(d=6.75, land=ATTACK['x'] + 0.1, pal=1, seed=21, hit=0.0, strike=1.25)    # nearer him: jaws at his chest
WB = dict(d=7.3, land=ATTACK['x'] - 0.2, pal=3, seed=22, hit=0.2, strike=0.85)     # behind him: at his belly
RUN_V = 5.5                                         # m/s, the wolves' run in (seen crossing the open ground)
HIT = 0.6                                           # WA's forepaws strike him (attack clock): he starts to fall
REACH = 0.95                                        # m from a leaping wolf's middle to its forepaws (leap pose, v 1)
POUNCE = 0.3                                        # s in the air: a short spring from close, as Cry Minister's
FEEDS = {'a': (1.55, 1.7, 0.0), 'b': (1.8, 2.1, 0.5)}    # (first rip, period, phase): out of step, once settled


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
    """One of the two (note 13): runs in from off frame left, crouches (0.15 s), springs a short pounce whose forepaws
    land ON him where he stands (at its hit: WA his chest, WB his hips), rides him down as he falls (0.5 s to his
    hips, 0.45 s onto his back), settles and feeds standing over his legs, head down at his chest or belly."""
    s = wolf_s(L, w['d'])
    gy = L.p(0, w['d'], 0)[1]
    hit = HIT + w['hit']
    x_hit = ATTACK['x'] - 0.15 - REACH             # its middle as the forepaws reach his front (he faces left)
    x_spring = x_hit - 0.7                          # a short spring from close: none overshoots him
    t_spring = hit - POUNCE
    t_crouch = t_spring - 0.15
    lift_hit = w['strike'] / WOLF_SHOULDER * 200.0 - 110.0     # leap pose v 1: forepaws 110 units over the lift
    if u < t_crouch:                                # the run in
        x = x_spring - RUN_V * (t_crouch - u)
        P = WF.pose('run', (x - x_spring) * UNITS)
    elif u < t_spring:                              # gathers: low, braced (the leap pose's crouch)
        x = x_spring
        P = WF.pose('leap', 0.0, lift=-18 * math.sin(math.pi * (u - t_crouch) / 0.15))
    elif u < hit:                                   # the pounce: an arc up to his chest (or hips)
        v = (u - t_spring) / POUNCE
        x = lerp(x_spring, x_hit, v)
        P = WF.pose('leap', 0.3 + 0.7 * v, lift=lift_hit * v + 60 * math.sin(math.pi * v))
    elif u < hit + 0.5:                             # rides him down: paws on him as he buckles onto his hips
        v = ease((u - hit) / 0.5)
        x = lerp(x_hit, lerp(x_hit, w['land'], 0.55), v)
        P = WF.pose('leap', 1.0, lift=lerp(lift_hit, 25.0, v))
    elif u < hit + 0.95:                            # and onto his back: settles over him
        v = (u - hit - 0.5) / 0.45
        x = lerp(lerp(x_hit, w['land'], 0.55), w['land'], ease(v))
        P = WF.pose('land', v)
    else:
        x = w['land']
        st, per, ph = FEEDS[key]
        f, _ = _feed_u(u, st, per)
        P = WF.pose('feed', f, hunk=(w['seed'] if f > 0.55 else None))
    bl = dict(muzzle=min(1.0, blood_k * 1.2), ruff=min(1.0, blood_k), paws=min(1.0, blood_k * 0.9))
    jaws = wolf_at(img, L, x, w['d'], 0.0, 1, P, w['pal'], blood=bl if blood_k > 0 else 0.0, seed=w['seed'])
    X = _ctx(img, s)
    for t0, at in ((t_spring, x_spring + 0.3), (hit + 0.5, ATTACK['x'] + 0.3)):   # the spring; his hips hit the dirt
        if u >= t0:
            WF.dust(X, L.p(at, w['d'], 0)[0], gy, s, u - t0, seed=int(w['seed'] + t0 * 10), size=1.1)
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
    """W1 and the two wolves on him: returns [(depth, draw)]. u is shot time; the attack's clock starts LEAD s in."""
    u = u - LEAD
    sp = dict(WORKERS[0])
    x, d = ATTACK['x'], ATTACK['d']
    gy = L.p(0, d, 0)[1]
    rips = {k: _rips(*FEEDS[k][:2], 11.0) for k in FEEDS}
    out = []

    # he digs side-on, a little towards the lens (facing straight left he was 104 degrees turned away: his back,
    # chat 16 body check); the wolves' hit twists him 10 degrees as he goes down (HIT to HIT + 0.5), and the lying
    # body takes over at that same 185 (straight left, 180, still showed his back for 2 drawings mid-fall)
    tw = math.radians(195.0 - 10.0 * ease((u - HIT) / 0.5))
    face = (math.cos(tw), math.sin(tw))

    def man(img):
        if u < HIT:
            j = _worker1_pose(sp, u)
            k = ease((u - (HIT - 0.32)) / 0.26)            # sees them spring: jerks upright, rocks back on his heels
            j['lean'] = lerp(j['lean'], -7.0, k)
            got = lying.stand(img, cam3, sp, x, d, face, j, u)
            if got[0] == '2d':
                Xf, Yf, s, _, _ = lying.place(cam3, x, d)
                jj = _screen(got[1], Xf, Yf - FEET * s, s, cam3.yaw_of((x, 0, d), face))
                a, b = jj['wrR_px'], jj['wrL_px']
                # the shaft runs through both hands and on down to the blade, in the dirt ahead of him
                gy = L.p(0, d, 0.0)[1] - 0.2 * L.ppm(d)
                k = (gy - a[1]) / max(1.0, b[1] - a[1])
                heel = (a[0] + (b[0] - a[0]) * k, gy)
                _shovel(img, L, (a[0] - (b[0] - a[0]) * 0.35, a[1] - (b[1] - a[1]) * 0.35), heel, d)
            return
        bare = dict(sp, kit_hat=None)                              # the hat flies off at the hit
        kind, *rest = lying.fall(bare, u, HIT, x, d, (math.cos(math.radians(185.0)), math.sin(math.radians(185.0))))
        if kind == 'views':
            lying.stand(img, cam3, bare, x, d, face, rest[0], u)
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
        j = MV.open_back(MV.gait(sp, u - RUN_T0, 'sprint', stride=1.5 / V.M_PER_UNIT, steps_per_s=RUN_SPEED / 1.5), 'sprint',
                         yaw=-90.0)
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
# Note 14 (Sam, 26 Nov: "more vigorous and desperate on both sides... hitting and stabbing and retreating, advancing,
# really trying to stop wolves from killing them. And the wolves... attacks and pushing forward and bites and
# snarls"): an exchange every 0.75 s, the two wolves in turn (each every 1.5 s), never a still moment. A wolf presses
# in snapping, lunges (pushing 0.45 m forward); its man gives ground as it comes, then steps in with the blow (a
# stab, or a clubbing overhead hit, by turns), and the struck wolf is knocked back, flinching, and comes again.
LUNGES = [(0.3 + 0.75 * k, k % 2) for k in range(16)]        # (time, which wolf): We and Wf in turn
STRIKE = 0.26                                                 # the blow lands this long after the lunge starts
CLANG = 4.3                                                   # W5's swing stops dead on the outer standard at x 11


def _exchange(u, k):
    """The latest exchange of wolf (or man) k at time u: (seconds into it, its number) or (None, -1)."""
    best = (None, -1)
    for n, (t0, kk) in enumerate(LUNGES):
        if kk == k and u >= t0:
            best = (u - t0, n)
    return best


def _bar_man(sp, u, who):
    """Two hands on the tube at chest height. As his wolf lunges he gives ground (a step back, leaning away, the tube
    drawn in), then steps in with the blow: a stab (fast, at full reach) or, every other time, a clubbing hit (the
    tube raised and brought down). Returns (pose, jab 0-1, dx m: his step along the boards, + away from the wolves)."""
    j = V.standing(sp)
    jab, lean, club, dx = 0.0, 0.0, 0.0, 0.0
    v, n = _exchange(u, who)
    hard = (n // 2) % 2 == 1                                   # every other blow a clubbing hit
    if v is not None and v < 1.5:
        if v < STRIKE:                                         # the wolf comes: back a step, brace
            e = ease(v / STRIKE)
            lean, jab, dx = -12 * e, -0.3 * e, 0.22 * e
            club = 0.9 * e if hard else 0.0
        elif v < STRIKE + 0.1:                                 # the blow: a lunge forward with everything
            e = (v - STRIKE) / 0.1
            lean, jab, dx = lerp(-12, 14, e), lerp(-0.3, 1.0, e), lerp(0.22, -0.16, e)
            club = lerp(0.9, -0.2, e) if hard else 0.0
        elif v < STRIKE + 0.7:                                 # drawn back, ready again
            e = ease((v - STRIKE - 0.1) / 0.6)
            lean, jab, dx = lerp(14, 2, e), lerp(1.0, 0.0, e), lerp(-0.16, 0.0, e)
            club = lerp(-0.2, 0.0, e) if hard else 0.0
        else:                                                  # never still: the tube jabs short, feinting
            lean = 3 * math.sin((u + who) * 9.0)
            jab = 0.15 * max(0.0, math.sin((u + who * 0.4) * 11.0))
    j['lean'] = 4 + lean
    j['footL'] = (-50, j['footL'][1], 110.0 + 40 * max(0.0, jab))      # the front foot reaches with the blow
    j['footR'] = (50, j['footR'][1], -90.0)
    reach = 150 + 220 * jab
    pull = 3.5 * min(0.0, lean)                     # leaning back to brace, he draws the tube in to his chest with him
    up = 45.0 if who == 0 else 0.0                  # chat 18: the nearest man's grip was level with the lift's front
    lift = 200.0 * club                             # a clubbing hit: the front hand high, then down through the wolf
    V.arm_to(j, 'L', (-40.0, 230.0 - up - lift, reach + 110 + pull), 'down', 'fist')   # guard rail: hands hidden behind it
    V.arm_to(j, 'R', (40.0, 250.0 - up - lift * 0.45, max(130.0, reach - 30) + pull), 'down', 'fist')
    return j, jab, dx


def bars(L, u):
    out = []
    for n, m in enumerate(BAR_MEN):
        def man(img, n=n, m=m):
            sp = dict(WORKERS[m['i']])
            dx = 0.0
            if n < 2:
                j, jab, dx = _bar_man(sp, u, n)
            else:                                                   # W5: an overhead swing that clangs on a standard
                j = V.standing(sp)
                v = (u - (CLANG - 0.45))
                ang = keyed(v, [(0.0, 0.0), (0.3, 1.0), (0.45, 0.55), (0.52, 0.62), (0.7, 0.58), (1.6, 0.0)])
                if not 0.0 <= v < 1.6:                              # note 14: brandished high over the others, shaking
                    ang = 0.32 + 0.14 * math.sin(u * 7.0) + 0.06 * math.sin(u * 17.0)
                    dx = 0.12 * math.sin(u * 3.1)                   # shuffling behind them, looking for a way in
                j['lean'] = 4 + 8 * ang
                hy = 300.0 - 260.0 * math.sin(math.pi * ang * 0.9)
                V.arm_to(j, 'L', (-40.0, hy, 240.0 - 40 * ang), 'down', 'fist')
                V.arm_to(j, 'R', (40.0, hy + 40, 140.0 - 20 * ang), 'down', 'fist')
                jab = 0.0
            jj = person_at(img, L, sp, m['x'] + dx, m['d'], MID, -90.0, j, u)
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
            grip_hands(img, jj, scale_at(L, m['d'], sp), sp)    # both the jab and the swing: hands over the tube
        out.append((m['d'], man))

    for k in range(2):                                              # We and Wf: lunge in turn, struck, flinch
        def wolf(img, k=k):
            d = (LIFT_D - 0.05, LIFT_D + 0.3)[k]
            x = (8.0, 8.7)[k]                                        # back from the men: the bars, not bodies, meet
            # between lunges it presses in, snapping and snarling, edging forward and back (note 14)
            snap = 0.5 + 0.45 * max(0.0, math.sin((u + 0.7 * k) * 10.0))
            P = WF.pose('lunge', 0.25 + 0.15 * math.sin((u + k) * 5.0), jaw=snap, snarl=1.0)
            push = 0.1 * math.sin((u + 0.5 * k) * 4.3)
            v, _ = _exchange(u, k)
            if v is not None and v < STRIKE:                        # the lunge: jaws wide, 0.3 m forward
                P = WF.pose('lunge', ease(v / STRIKE), snarl=1.0)
                push += 0.3 * ease(v / STRIKE)
            elif v is not None and v < STRIKE + 0.9:                # struck: knocked back, flinching, then again
                w = v - STRIKE
                fl = min(1.0, w / 0.08) if w < 0.35 else max(0.0, 1.0 - (w - 0.35) / 0.4)
                P = WF.pose('lunge', 1.0 - min(1.0, w / 0.4), flinch=fl)
                back = keyed(w, [(0.0, 0.3), (0.12, -0.3), (0.9, 0.0)])
                push = back + (push if w > 0.6 else 0.0) * (w - 0.6) / 0.3
            wolf_at(img, L, x + push, d, MID, 1, P, pal=(2, 3)[k], seed=50 + k)
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


# ================================================================================================= shot 3: the chase
# Blair's room (story/brexit-is-done-places.txt, view blair): back wall at 7 m, the double doors x -1.9 to -0.1 at
# 6.95 m, thrown open at 0.3 s; each leaf settles at 92 degrees, so its free edge stands out to 6.05 m: whoever comes
# through runs straight out between the leaves to 5.95 m before turning (rule 5: through the doorway, never a leaf or
# the wall). The chase band is 4.7-5.85 m, in front of the leaf tips; Blair (2.06 m) hides the right half.
DOOR = dict(x0=-1.9, x1=-0.1, d=6.95, z1=3.0)
GUEST_V, WOLF_V = 4.4, 4.4              # m/s: guests in panic (heels, a tray, a gown); the wolves keep pace, never close
#                                         (chat 12: at 5.0 m/s a wolf's open jaws reached the runner's back foot)
# (guest, start s, path [(x, d) m], wolf, its lag s): the four burst out of the doors in turn, each with a wolf at
# their heels; then they come back across in waves, two side by side (one lane each) with their wolves behind, entering
# on the side they left by. Everyone in frame runs the same way: the next wave comes the other way only once the frame
# is clear (chat 13: lanes 0.8, then 1.4 m apart still met nose to nose, and a wolf ran past a guest's hand; moves.head_on).
# In a pair the near one leads by 0.45 s (moves.within_reach) and the near wolf waits 0.9 s: both guests, then both wolves
LANE_R, LANE_L = 4.60, 6.00             # m: the near and far lanes
PASSES = [
    (0, 0.30, [(-1.30, 7.60), (-1.30, 6.15), (-3.3, LANE_L)], 0, 0.65),   # the butler: he threw the doors open
    (1, 0.85, [(-0.38, 8.60), (-0.38, 5.70), (1.4, LANE_R), (2.9, LANE_R)], 1, 0.55),
    (2, 1.40, [(-1.10, 9.00), (-1.10, 6.10), (-3.0, LANE_L)], 2, 0.55),   # chat 19: guests 1 and 2 0.72 m apart in the doorway (0.55 put his hand on her arm)
    (3, 1.95, [(-1.60, 9.20), (-1.60, 5.70), (0.6, LANE_R), (2.9, LANE_R)], 3, 0.55),
    (0, 2.55, [(-2.7, LANE_R), (2.7, LANE_R)], 0, 0.90),          # wave 1, to the right: the two who left left,
    (2, 3.00, [(-2.7, LANE_L), (2.7, LANE_L)], 2, 0.55),          # the near one leading (perspective opens the gap)
    (1, 4.80, [(2.7, LANE_R), (-2.7, LANE_R)], 1, 0.90),          # wave 2, to the left: the two who left right
    (3, 5.25, [(2.7, LANE_L), (-2.7, LANE_L)], 3, 0.55),
    (2, 6.40, [(2.7, LANE_R), (-2.7, LANE_R)], 2, 0.90),          # wave 3, to the left: wave 1 back again
    (0, 6.85, [(2.7, LANE_L), (-2.7, LANE_L)], 0, 0.55),
    (0, 8.85, [(-2.6, 5.00), (2.7, 5.00)], 0, 0.55),              # still left of his face at the cut
]
# Note 15 (Sam, 26 Nov: they "appear from a sudden blank void at the end of the corridor... materialize suddenly"): the
# corridor now runs 9 m back with a cross passage at 13.35-14.95 m (story/brexit-is-done-places.txt). The four who burst
# out of the doors come from its right-hand opening, out of sight behind the corridor's right wall until they turn
# into it, and run the length of it towards us; each keeps the moment it reaches the doorway (the start moves earlier
# by the extra distance), and each wolf comes round the same corner at its heels.
PASSAGE_D = 14.15                       # m: the cross passage's middle
PASSAGE_X = 1.4                         # m: where they start, out of sight in the passage's right arm


def _from_passage(row):
    k, t0, pts, w, lag = row
    lead = [(PASSAGE_X, PASSAGE_D), (pts[0][0], PASSAGE_D)]
    extra = math.hypot(lead[0][0] - lead[1][0], 0) + abs(PASSAGE_D - pts[0][1])
    return (k, t0 - extra / GUEST_V, lead + list(pts), w, lag)


PASSES[:4] = [_from_passage(r) for r in PASSES[:4]]
# Note 15 too: the doorway times were 0.26 s apart (all four and their wolves in one clump in the doorway); now about
# 0.55 s apart (each about 2.4 m behind the last down the corridor): the butler 0.30, then 0.85, 1.40, 1.95.
# From 8.4 s nothing passes behind Blair's head or shoulders: the lunge from the right is the only thing there.
ROOM_WOLF = [dict(pal=0, seed=60), dict(pal=2, seed=61), dict(pal=4, seed=62), dict(pal=1, seed=63)]
TOSS = 0.70                             # the butler swerves at the turn: the tray flies on (shot time)
RUN_STEP = 0.95                         # m: the run gait's own stride (chat 12: 1.25 kicked the back leg out flat) (feet planted: steps a second = speed / stride)


def _guest_pose(sp, k, tt, dx, dd, u):
    """A running guest's yaw and joints: straight at us out of the doorway (front_run), three-quarter on a diagonal,
    side on across."""
    if dd < -0.8:
        yaw, j = 0.0, MV.gait(sp, tt, 'front_run')
    else:
        yaw = (-90.0 if dx < 0 else 90.0) if abs(dd) < 0.35 else (-45.0 if dx < 0 else 45.0)
        j = MV.open_back(MV.gait(sp, tt + 0.13 * k, 'run', steps_per_s=GUEST_V / RUN_STEP), 'run', yaw=yaw)
    if k == 0 and u < TOSS:                                 # the butler's tray up on his right palm, shoulder high
        V.arm_to(j, 'R', (215.0, -10.0, 150.0), 'out', 'palm')
    return yaw, j


def _beyond_door(d):
    return d > DOOR['d'] - 0.02


def tray_state(u, L):
    """Where the tray and the three glasses are at shot time u: before TOSS on the butler's palm (None: drawn with
    him); after it, flying on with his momentum, tumbling, landing (the tray hops once and rattles flat; each glass
    shatters where it lands and its champagne spreads into a pool that stays)."""
    if u < TOSS:
        return None
    x0, d0 = along(PASSES[0][2], GUEST_V * (TOSS - PASSES[0][1]))[:2]
    x0 += 0.30
    z0 = 1.62
    out = {}
    for n, (vx, vd, vz, spin) in enumerate([(-0.15, -0.95, 2.4, 11.0), (-0.55, -1.25, 2.8, 15.0), (0.05, -0.70, 3.1, -13.0),
                                            (-0.35, -1.10, 2.2, 17.0)]):
        tl = (vz + math.sqrt(vz * vz + 2 * 9.8 * z0)) / 9.8            # time in the air
        tau = u - TOSS
        if tau < tl:
            out[n] = dict(x=x0 + vx * tau, d=d0 + vd * tau, z=z0 + vz * tau - 4.9 * tau * tau, ang=spin * tau, age=None)
        else:
            out[n] = dict(x=x0 + vx * tl, d=d0 + vd * tl, z=0.0, ang=spin * tl, age=tau - tl)
            if n == 0:                       # the tray: kicked along by any feet that reach it (moves.kicked)
                x, d, since, sp = MV.kicked(out[n]['x'], out[n]['d'], TOSS + tl, u, tray_movers())
                out[n].update(x=x, d=d, age=since, spin=sp)
    return out


def tray_movers():
    """Every guest and wolf of the chase as moves.kicked / moves.trodden want them."""
    return MV.chase_movers(PASSES, GUEST_V, WOLF_V)


def tray_track(u):
    """Where the fallen tray lies at u, or None while it is in the air (the check moves.trodden reads it)."""
    st = tray_state(u, None)
    return (st[0]['x'], st[0]['d']) if st and st[0]['age'] is not None else None


def _tray(img, L, st, held=None):
    """The silver tray: an ellipse in perspective (thin when level with the eye), tumbling in the air, flat on the
    floor once landed (a hop, then a rattle that dies away)."""
    from PIL import ImageDraw
    dd = glaze(img)
    if held is not None:
        (px, py), d, z = held
        r = 0.21 * L.ppm(d)
        ry = max(3.0, r * abs(z - L.up) / d)
        ang = 0.0
    else:
        d, z = st['d'], st['z']
        r = 0.21 * L.ppm(d)
        px, py = L.p(st['x'], d, z)
        if st['age'] is None:
            ry = max(3.0, r * abs(math.cos(st['ang'])))
            ang = 0.0
            g = L.p(st['x'], d, 0)
            dd.ellipse([g[0] - r, g[1] - 0.2 * r, g[0] + r, g[1] + 0.2 * r], fill=(0, 0, 0, 40))
        else:
            a = st['age']
            hop = 0.06 * max(0.0, math.sin(math.pi * a / 0.16)) if a < 0.16 else 0.0
            px, py = L.p(st['x'], d, hop)
            flat = r * L.up / d
            ry = flat * (1 + 0.5 * math.exp(-6 * a) * abs(math.sin(a * 40)))   # the rattle
            dd.ellipse([px - r, py - flat * 0.9, px + r, py + flat * 0.9], fill=(0, 0, 0, 45))
    w = max(1.5, 0.008 * L.ppm(d))
    _ell(img, px, py, r, ry, (150, 156, 166), OUT, w)                 # the raised rim (chat 14, critique r5 (d): a
    _ell(img, px, py, r * 0.84, ry * 0.8, (214, 219, 226), OUT, w * 0.6)   # flat disc read as a plate): rim, dish,
    hl = glaze(img)                                                    # a bright shine across the dish, two handles
    hl.ellipse([px - r * 0.55, py - ry * 0.55, px - r * 0.05, py - ry * 0.1], fill=(255, 255, 255, 190))
    for sx in (-1, 1):
        _ell(img, px + sx * r * 0.92, py, r * 0.05, max(1.5, ry * 0.25), (70, 74, 82), None, 0)
    return px, py, r, ry


def _ell(img, x, y, rx, ry, fill, line, w):
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=fill, outline=line, width=int(round(w)) if line else 0)


def _flute(img, x, y, s, ang, full=1.0):
    """A champagne flute (stem, foot, bowl) of height 0.2 m * s px-per-m, turned `ang` radians."""
    from PIL import ImageDraw
    d = glaze(img)
    h = 0.2 * s
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v):
        return (x + u * ca - v * sa, y + u * sa + v * ca)
    w = max(1, int(0.006 * s))
    d.line([P(0, 0), P(0, -0.45 * h)], fill=OUT, width=w + 1)
    d.line([P(-0.12 * h, 0), P(0.12 * h, 0)], fill=OUT, width=w + 1)
    bowl = [P(-0.09 * h, -0.45 * h), P(-0.11 * h, -h), P(0.11 * h, -h), P(0.09 * h, -0.45 * h)]
    d.polygon(bowl, fill=(236, 240, 244, 150), outline=OUT)
    if full > 0:
        d.polygon([P(-0.09 * h, -0.45 * h), P(-0.10 * h, -0.85 * h), P(0.10 * h, -0.85 * h), P(0.09 * h, -0.45 * h)],
                  fill=(232, 196, 96, 220))


def _glass_down(img, L, st, n):
    """A glass that has landed: shards flung a little way and still, champagne spreading into a wet pool."""
    from PIL import ImageDraw
    d_, a = st['d'], st['age']
    s = L.ppm(d_)
    px, py = L.p(st['x'], d_, 0)
    flat = L.up / d_
    r = (0.05 + 0.13 * (1 - math.exp(-5 * a))) * s
    dd = glaze(img)
    dd.ellipse([px - r, py - r * flat, px + r, py + r * flat], fill=(214, 176, 80, 150))
    dd.ellipse([px - r * 0.4, py - r * flat * 0.6, px - r * 0.1, py - r * flat * 0.2], fill=(255, 250, 230, 160))
    rnd = random.Random(500 + n)
    slide = min(1.0, a / 0.15)
    for k in range(6):
        th = rnd.uniform(0, 2 * math.pi)
        dist = rnd.uniform(0.05, 0.22) * s * (1 - (1 - slide) ** 2)
        cx, cy = px + dist * math.cos(th), py + dist * math.sin(th) * flat
        q = rnd.uniform(0.012, 0.025) * s
        tri = [(cx + q * math.cos(th + k2 * 2.1 + k), cy + q * flat * 2 * math.sin(th + k2 * 2.1 + k)) for k2 in range(3)]
        dd.polygon(tri, fill=(236, 242, 246, 230), outline=OUT)
    # what is left whole: the stem and foot lying on their side by the pool (chat 14, critique r5 (d): shards alone
    # read as specks at phone size); rolled a little way out with the spill
    th = rnd.uniform(-0.5, 0.5)
    h = 0.2 * s
    bx, by = px + (0.10 * s + 0.06 * s * slide) * (1 if n % 2 else -1), py + 0.02 * s * flat
    ex, ey = bx + 0.55 * h * math.cos(th), by + 0.55 * h * math.sin(th) * flat
    w = max(2, int(0.01 * s))
    dd.line([(bx, by), (ex, ey)], fill=OUT, width=w + 2)
    dd.line([(bx, by), (ex, ey)], fill=(236, 242, 246, 255), width=w)
    dd.ellipse([bx - 0.008 * s, by - 0.03 * s, bx + 0.008 * s, by + 0.03 * s], fill=(236, 242, 246, 255), outline=OUT)   # the foot, edge on
    bowl = [(ex, ey - 0.09 * h), (ex + 0.3 * h * math.cos(th), ey - 0.06 * h + 0.3 * h * math.sin(th) * flat),
            (ex + 0.3 * h * math.cos(th), ey + 0.06 * h + 0.3 * h * math.sin(th) * flat), (ex, ey + 0.09 * h)]
    dd.polygon(bowl, fill=(236, 240, 244, 200), outline=OUT)        # the bowl's broken lower half still on the stem


def lunger(img, L, u):
    """Wp: in from frame right in mid-leap, coming down on Blair's head from above right, jaws wide, forepaws out; the
    film cuts at 9.4 s (its last frame 9.333 at 12 fps), before it reaches him (item 13). It closes from 3.0 m to his
    shoulder's depth (2.3 m: just behind him, so his head would hide it, never pass through it), growing as it comes.
    Chat 14 (critique r5 (a): "a brown blob with teeth at the right edge for 2 frames"): at 12 fps the lunge has five
    frames (9.0-9.333); the old path had the jaws off the edge for three of them. Now the jaws are on screen from the
    first frame and the head (ear, eye, open jaws) and forepaws are in frame from the second."""
    if u < LUNGE_T:
        return
    v = min(1.0, (u - LUNGE_T) / LUNGE_LEN)
    (x0, y0), (x1, y1) = LUNGE_PATH
    jaw_x, jaw_y = x0 + (x1 - x0) * v, y0 + (y1 - y0) * v      # screen px: the right edge -> just above his hair
    d = 3.2 - 0.85 * v
    P = WF.pose('leap', 0.75 + 0.25 * v, jaw=1.0, snarl=1.0)
    s = wolf_s(L, d)
    from PIL import Image
    probe = Image.new('RGBA', (8, 8))
    jx, jy = WF.draw(_ctx(probe, s), 0.0, 0.0, s, -1, 1, P, blood=0.0, seed=70)
    WF.draw(_ctx(img, s), jaw_x - jx, jaw_y - jy, s, -1, 1, P, blood=0.0, seed=70)


LUNGE_LEN = 0.333                                       # s: 9.0 -> the last frame before the cut
LUNGE_PATH = ((960.0, 215.0), (750.0, 365.0))          # the jaws' front, screen px, first and last frame
LUNGE_T = 9.0


def room_actors(u, L):
    """Every background actor of shot 3 at shot time u: ([(depth, draw)], [draw] seen through the doorway)."""
    room, beyond = [], []
    for k, t0, pts, w, lag in PASSES:
        for who in ('guest', 'wolf'):
            start = t0 + (lag if who == 'wolf' else 0.0)
            v = WOLF_V if who == 'wolf' else GUEST_V
            if u < start:
                continue
            at = along(pts, v * (u - start))
            if at is None:
                continue
            x, d, dx, dd = at
            if who == 'guest':
                def draw(img, k=k, x=x, d=d, dx=dx, dd=dd, tt=u - start):
                    sp = dict(GUESTS[k])
                    yaw, j = _guest_pose(sp, k, tt, dx, dd, u)
                    with FG.allow('a guest running side on: the back arm swings behind the body (moves.gait)'):
                        jj = person_at(img, L, sp, x, d, 0.0, yaw, j, u)
                    if k == 0 and u < TOSS and 'wrR_px' in jj:           # the tray on his palm, glasses on it
                        hx, hy = jj['wrR_px']
                        ppm = L.ppm(d)
                        tx, ty, r, ry = _tray(img, L, None, held=((hx, hy - 0.03 * ppm), d, 1.62))
                        for g, off in enumerate((-0.5, 0.05, 0.55)):
                            _flute(img, tx + off * r, ty - 0.2 * ry, ppm, 0.0)
            else:
                def draw(img, w=w, x=x, d=d, dx=dx, dd=dd, dist=v * (u - start)):
                    m = ROOM_WOLF[w]
                    if dd < -0.8:
                        wolf_front_at(img, L, x, d, 0.0, pal=m['pal'], seed=m['seed'], blood=0.3,
                                      run=dist * 1.6, jaw=0.8)
                    else:
                        wolf_at(img, L, x, d, 0.0, -1 if dx < 0 else 1, WF.pose('run', dist * UNITS),
                                pal=m['pal'], seed=m['seed'], blood=0.3)
            (beyond if _beyond_door(d) else room).append((d, draw) if not _beyond_door(d) else draw)
    st = tray_state(u, L)
    if st:
        for n, g in st.items():
            if n == 0:
                room.append((g['d'], lambda img, g=g: _tray(img, L, g)))
            elif g['age'] is None:
                def fly(img, g=g):
                    px, py = L.p(g['x'], g['d'], g['z'])
                    _flute(img, px, py, L.ppm(g['d']), g['ang'], full=0.6)
                room.append((g['d'] - 0.01, fly))
            else:
                room.append((g['d'] + 0.05, lambda img, g=g, n=n: _glass_down(img, L, g, n)))
    return room, beyond


# ================================================================================================= shot 2
def set_cam(L):
    """The level camera as a 3D set camera (lying.py's bodies and floor-placed people need one)."""
    import sets
    return sets.Cam((0.0, L.up, 0.0), (0.0, L.up, 1.0), focal=L.L, shake=(L.c - 540.0, L.hz - 960.0))


def site_actors(u, L):
    """Every background actor of shot 2 at shot time u: [(depth, draw)]."""
    cam3 = set_cam(L)
    return w1(None, L, cam3, u) + runner(None, L, u) + bars(L, u) + milling(L, u)
