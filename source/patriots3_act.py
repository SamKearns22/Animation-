#!/usr/bin/env python3
"""Patriots 3: who stands where, facing which way, in what pose, at every moment (the acting, shot by shot).

Every person is an Actor on the plan's floor (metres, patriots3_plan): x, z, facing in degrees (0 north to the slit,
90 east), a pose in their own body frame (views joints), face settings, and a `roll` (degrees: the whole figure tipped
about the feet, for leaning on the door post). The MG42 stays where it stands on the sill (one Gun in the world); a
person at it puts their hands on its grips, and it is drawn with them (their hands over it).

Timeline (seconds; the plan's guesses until the recordings arrive):
  3.6-6.4   the Gunner fires two bursts, the Loader spots (binoculars) and points, barking
  6.4       "Small boat problem?" (off): they freeze; 6.95 they turn round, startled (a straight 180)
  7.6-14.9  the Patriot leans in the doorway, arms folded, ankles crossed; 12.6 they glance at each other, 13.1 back
  14.9-16.9 he pushes off the post and walks up to them; 16.0 they turn to face him
  20.45     the salute (both), "Heil!" 20.6; 21.9 the arms come down (he flaps at them in shot 7)
  21.6-26.0 his arms dart about: hands up, pat down, point round the room, wag a finger
  26.8      the shell hits the slit's lip: the Gunner thrown back against the east wall, the Loader staggers back
  30.6-32.3 he walks to the gun; 32.4 he takes it; 33.7 he shakes his head; 36.6 he fires; 41.0 their eyes meet
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import views as V                # noqa: E402
import moves as MV               # noqa: E402
import figure as F               # noqa: E402
import filmkit                   # noqa: E402
import patriots3_cast as C       # noqa: E402
import patriots3_bunker as K     # noqa: E402
import patriots3_plan as PL      # noqa: E402

T_FREEZE, T_TURN = 6.45, 6.95
G_BURSTS = [(3.85, 4.9), (5.55, 6.4)]
T_GLANCE, T_BACK = 12.6, 13.1
T_UNFOLD, T_WALK = 14.6, 14.95
T_FACE = 16.0
T_SALUTE, T_SALUTE_DOWN = 20.45, 21.9
T_BLAST = 26.8
G_FLIGHT, L_FLIGHT = 0.42, 0.95                    # how long the Gunner flies, the Loader staggers
T_TO_GUN = 30.6
T_SHAKE = (33.7, 34.4)
T_TAKE = 36.25                                     # he leans in and takes both grips, then fires
P_BURSTS = [(36.6, 37.9), (38.3, 39.6), (40.65, 41.5), (41.8, 42.6)]   # a gap for 'Traitors' (39.75, Sam 27 Oct)
T_MEET = 41.0

PLACE = PL.PEOPLE
DOOR = (0.5, -2.28)                                 # leaning on the west post (0.2): his shoulder on it when tipped
APPROACH = PLACE['patriot approached']['at']
G_WALL = (1.66, -0.6)                               # his back against the east wall (2.0)
L_BACK = PLACE['loader after the blast']['at']
AT_GUN = (0.0, -0.02)

REST = K.Crew('spot')                               # the gun at rest on the sill (where the Gunner set it up)
GUN = REST.gun


def gun_at(fire_t):
    """The gun this frame: the same place, pushed back a little on the frames it kicks."""
    frame = int(round((fire_t or 0.0) * 12))
    kick = 0.016 if (fire_t is not None and fire_t >= 0 and frame % 2 == 0) else 0.0
    return C.Gun(REST.butt, REST.aim, kick)


def burst_t(t, bursts):
    for a, b in bursts:
        if a <= t < b:
            return t - a
    return None


class Actor:
    def __init__(self, who, x, z, facing, j, sp=None, head_facing=None, roll=0.0, crew=None, holds=False,
                 fire_t=None, reach=1.0):
        self.who, self.x, self.z, self.facing, self.j = who, x, z, facing, j
        self.sp = dict(sp or {})
        self.head_facing, self.roll, self.crew = head_facing, roll, crew
        self.holds, self.fire_t, self.reach = holds, fire_t, reach        # at the gun: hands go on its grips
        self.one_hand = False                                              # only the hand nearest the gun on it


def toward(a, b):
    return math.degrees(math.atan2(b[0] - a[0], b[1] - a[1])) % 360


def _idle(j, t, seed):
    """Never frozen, never wobbling: a held pose with a quick small shift now and then (filmkit.shifts)."""
    j['head_dy'] = j.get('head_dy', 0) + 30 * filmkit.shifts(t, seed=seed, amount=0.15)
    j['lean'] = j.get('lean', 0.0) + 20 * filmkit.shifts(t, seed=seed + 7, amount=0.06)
    return j


def _sw(sp):
    return sp.get('shoulders', 150)


def startled(sp):
    """Jumped: arms come up and out a little, weight back, the chin up."""
    j = V.standing(sp)
    sw = _sw(sp)
    for s, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, s, (sg * (sw + 70), 300.0, 90.0), 'out', 'palm')
    j['lean'] = -5
    j['head_dy'] = -6
    return j


def salute(sp, k=1.0, steep=0.62, out=0.3):
    """The salute (refs salute-1, -2): the right arm straight out, forward and up, the hand flat; k eases it up
    (0 down, 1 up). `steep`: how far up (the Gunner's goes higher, so it passes over the Loader's helmet)."""
    j = V.standing(sp)
    sh = j['shR']
    reach = (F.UPPER + F.FORE) * 0.97 + F.HAND['palm']
    d1 = np.array([out, -steep, max(0.3, 1.0 - steep)])
    d1 /= np.linalg.norm(d1)
    d0 = np.array([min(0.25, out + 0.05), 0.95, 0.2])   # hanging at his side
    d0 /= np.linalg.norm(d0)
    w = math.acos(max(-1.0, min(1.0, float(d0 @ d1))))  # swung up round the shoulder (an arc, never cutting in
    d = (math.sin((1 - k) * w) * d0 + math.sin(k * w) * d1) / math.sin(w)   # across the man beside him)
    V.arm_to(j, 'R', tuple(np.array(sh) + d * reach * (0.92 + 0.08 * k)), 'out', 'palm')
    j['head_dy'] = -4 * k
    return j


def _shake_head(t):
    """The sad head shake: the head turns one way, the other, and back (a straight jump each time), 0.18 s a turn."""
    a, b = T_SHAKE
    if not (a <= t < b):
        return None
    n = int((t - a) / 0.18)
    return (-35, 35, -35, 35, 0)[min(n, 4)]


# ------------------------------------------------------------------------------------------------ the Gunner
def gunner(t):
    sp = dict(brows='serious')
    if t < T_TURN:
        mode = 'point' if 4.0 <= t < 6.3 else 'spot'
        fire_t = burst_t(t, G_BURSTS) if t < T_FREEZE else None
        crew = K.Crew(mode, fire_t, t)
        sp = dict(crew.people()[0][1])
        sp = {k: v for k, v in sp.items() if k in ('brows', 'lid')}
        if t >= T_FREEZE:
            sp['brows'] = 'alarm'
        return Actor('gunner', *K.GUNNER_AT, 0, crew.jg, sp, crew=crew, holds=True, fire_t=fire_t)
    if t < T_BLAST:
        at = PLACE['gunner turned']['at']
        facing = 165 if t < T_FACE else 215
        if t < T_TURN + 0.7:
            j = startled(C.GUNNER)
            sp.update(brows='alarm', mouth='v:O' if t < T_TURN + 0.45 else 'set')
        elif T_SALUTE <= t < T_SALUTE_DOWN + 0.3:
            k = min(1.0, (t - T_SALUTE) / 0.15) if t < T_SALUTE_DOWN else max(0.0, 1 - (t - T_SALUTE_DOWN) / 0.3)
            j = salute(C.GUNNER, k, steep=0.9, out=0.0)    # the Loader is on his right: straight up and forward
            sp['brows'] = 'fierce'
        else:
            j = _idle(V.standing(C.GUNNER), t, 3)
            if t >= T_SALUTE_DOWN + 0.3:
                sp['brows'] = 'confused'
        head = None
        if T_GLANCE <= t < T_BACK:
            head = toward(at, PLACE['loader turned']['at'])      # a look at each other
        return Actor('gunner', at[0], at[1], facing, j, sp, head)
    u = t - T_BLAST
    a0 = PLACE['gunner turned']['at']
    sp.update(brows='alarm')
    if u < G_FLIGHT:                                   # flung back: fast off the mark, still moving when he hits
        k = u / G_FLIGHT
        k = 1 - (1 - k) ** 1.6
        x, z = MV.lerp(a0, G_WALL, k)
        j, _ = MV.hit_react(C.GUNNER, t, T_BLAST, strength=1.6)
        j['footL'] = (-70.0, V.ANKLE_Y - 60 * math.sin(math.pi * k), 60.0)
        j['footR'] = (70.0, V.ANKLE_Y - 30 * math.sin(math.pi * k), 90.0)
        sp['mouth'] = 'v:O'
        return Actor('gunner', x, z, 271, j, sp)
    facing = 271 if t < 32.0 else PLACE['gunner watching him']['facing']
    j = V.standing(C.GUNNER)
    w = u - G_FLIGHT
    if w < 0.5:                                        # the back hits the wall: rocks, palms flat on it
        j['lean'] = 6 * math.exp(-w * 6)
    if t < 32.0:                                       # palms flat on the wall behind him until he turns
        for s, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s, (sg * (_sw(C.GUNNER) + 70), 400.0, -12.0), 'out', 'palm')
    j = _idle(j, t, 5)
    sp['brows'] = 'confused' if t > T_BLAST + 2.0 else 'alarm'
    if t >= 33.5:
        sp['lid'] = 0                                  # wide-eyed, dumbfounded
    head = None
    if t >= T_MEET:
        head = toward(G_WALL, L_BACK)
    return Actor('gunner', G_WALL[0], G_WALL[1], facing, j, sp, head)


# ------------------------------------------------------------------------------------------------ the Loader
def loader(t):
    sp = {}
    if t < T_TURN:
        mode = 'point' if 4.0 <= t < 6.3 else 'spot'
        crew = K.Crew(mode, None, t)
        lsp = crew.people()[1][1]
        sp = {k: v for k, v in lsp.items() if k in ('brows',)}
        if t >= T_FREEZE:
            sp['brows'] = 'alarm'
        return Actor('loader', *K.LOADER_AT, 0, crew.jl, sp, crew=crew)
    if t < T_BLAST:
        at = PLACE['loader turned']['at']
        facing = 140 if t < T_FACE else 195
        if t < T_TURN + 0.7:
            j = startled(C.LOADER)
            sp.update(brows='alarm', mouth='v:O' if t < T_TURN + 0.45 else None)
        elif T_SALUTE <= t < T_SALUTE_DOWN + 0.3:
            k = min(1.0, (t - T_SALUTE) / 0.15) if t < T_SALUTE_DOWN else max(0.0, 1 - (t - T_SALUTE_DOWN) / 0.3)
            j = salute(C.LOADER, k, steep=0.7)
            sp['brows'] = 'serious'
        else:
            j = _idle(V.standing(C.LOADER), t, 4)
            sp['brows'] = 'confused' if T_TURN + 0.7 <= t < T_SALUTE else 'sincere' if t < T_SALUTE else 'confused'
        head = None
        if T_GLANCE <= t < T_BACK:
            head = toward(at, PLACE['gunner turned']['at'])
        sp = {k: v for k, v in sp.items() if v is not None}
        return Actor('loader', at[0], at[1], facing, j, sp, head)
    u = t - T_BLAST
    a0 = PLACE['loader turned']['at']
    if u < L_FLIGHT:                                   # staggers back three quick steps, arms flung up
        k = u / L_FLIGHT
        k = 1 - (1 - k) ** 2
        x, z = MV.lerp(a0, L_BACK, k)
        j = MV.gait(C.LOADER, u * 0.9, 'brisk')
        for s in 'LR':                                 # walking backwards: the planted feet slide forward under him
            fx, fy, fz = j['foot' + s]
            j['foot' + s] = (fx, fy, -fz)
        r, _ = MV.hit_react(C.LOADER, t, T_BLAST, strength=1.2)
        for k2 in ('elL', 'elR', 'wrL', 'wrR', 'hand'):
            j[k2] = r[k2]
        j['lean'] = r['lean']
        sp.update(brows='alarm', mouth='v:O')
        return Actor('loader', x, z, PLACE['loader after the blast']['facing'], j, sp)
    facing = PLACE['loader after the blast']['facing'] if t < 32.0 else PLACE['loader watching him']['facing']
    j = _idle(V.standing(C.LOADER), t, 6)
    sp['brows'] = 'alarm' if t < T_BLAST + 2.0 else 'confused'
    head = None
    if t >= T_MEET:                                # turned to the Gunner, but only three-quarter from the slit's
        a, c = toward(L_BACK, G_WALL), toward(L_BACK, (-0.25, 1.55))   # camera: in profile his look read as past
        head = (a + 0.35 * (((c - a + 180) % 360) - 180)) % 360     # him; the eyes do the rest (Sam, 27 Oct)
    return Actor('loader', L_BACK[0], L_BACK[1], facing, j, sp, head)


# ------------------------------------------------------------------------------------------------ the Patriot
def leaning(sp):
    """Leaning in the doorway (refs lean-1, -2): arms folded, the right ankle crossed over the left, the weight on
    the post (the figure is tipped onto it by Actor.roll)."""
    j = MV.pose(sp, 'arms_folded')
    j['footL'] = (36.0, V.ANKLE_Y, 0.0)
    j['footR'] = (-58.0, V.ANKLE_Y - 6, 34.0)
    j['toeR'] = 10
    return j


FLAPS = {                                          # his arms darting about (shot 7): body-frame hand targets, wide
    'up':     {'L': (-300.0, -80.0, 50.0), 'R': (300.0, -80.0, 50.0)},      # and high enough to read on a phone; hands out at the sleeves' ends, not folded back into them (Sam, 27 Oct)
    'pat':    {'L': (-290.0, 170.0, 70.0), 'R': (290.0, 170.0, 70.0)},      # flapping down: "keep it down!"
    'pat2':   {'L': (-320.0, 30.0, 60.0), 'R': (320.0, 30.0, 60.0)},
    'pointL': {'L': (-430.0, -120.0, 80.0), 'R': (200.0, 260.0, 120.0)},
    'pointR': {'L': (-200.0, 260.0, 120.0), 'R': (430.0, -120.0, 80.0)},
    'wag1':   {'L': (-220.0, 420.0, 60.0), 'R': (90.0, -160.0, 200.0)},
    'wag2':   {'L': (-220.0, 420.0, 60.0), 'R': (220.0, -160.0, 200.0)},
    'across': {'L': (-220.0, 420.0, 60.0), 'R': (-200.0, 40.0, 220.0)},
    'down':   {'L': (-190.0, 440.0, 60.0), 'R': (190.0, 440.0, 60.0)},
}
HANDS = {'pointL': {'L': 'point', 'R': 'palm'}, 'pointR': {'L': 'palm', 'R': 'point'},
         'wag1': {'L': 'fist', 'R': 'point'}, 'wag2': {'L': 'fist', 'R': 'point'}}
FLAP_KEYS = [(21.5, 'down'), (21.62, 'up'), (21.9, 'pat'), (22.12, 'pat2'), (22.34, 'pat'), (22.56, 'pat2'),
             (22.8, 'pat'), (22.98, 'pointL'), (23.4, 'pointR'), (23.85, 'pointL'), (24.25, 'pat'), (24.45, 'wag1'),
             (24.62, 'wag2'), (24.8, 'wag1'), (24.98, 'wag2'), (25.25, 'across'), (25.6, 'pat'), (25.82, 'pat2'),
             (26.04, 'pat'), (26.6, 'down')]
LOOKS_ROUND = [(22.95, -40), (23.4, 40), (23.85, -40), (24.25, None)]   # "the Free Speech Police are everywhere"


def flap_pose(sp, name):
    j = V.standing(sp)
    for s in 'LR':
        V.arm_to(j, s, FLAPS[name][s], 'out', HANDS.get(name, {}).get(s, 'palm'))
    return j


def flapping(sp, t):
    keys = [(a, flap_pose(sp, n)) for a, n in FLAP_KEYS]
    j = MV.keyed(t, keys)
    j['hand'] = dict(V.standing(sp)['hand'])
    for (a, n), (b, _) in zip(FLAP_KEYS, FLAP_KEYS[1:] + [(1e9, None)]):
        if a <= t:
            j['hand'] = {s: HANDS.get(n, {}).get(s, 'palm') for s in 'LR'}
    return j


def _into_walk(u, t, path, start):
    """The walk eased in from standing over its first 0.25 s and out over its last 0.25 s (no pop)."""
    total = sum(math.dist(a, b) for a, b in zip(path, path[1:])) / MV.speed('walk')
    k = min(1.0, u / 0.25, max(0.0, (total - u) / 0.25))
    return MV.mix_poses(V.standing(C.PATRIOT), MV.gait(C.PATRIOT, u, 'walk'), MV.ease(k))


def at_gun(sp, k=1.0):
    """At the MG42 like the Gunner (patriots3_bunker.Crew): leaning in over it, feet braced; k eases him into it.
    The hands are put on the grips by the film (patriots3.hold_gun), where the camera sees them."""
    j = V.standing(sp)
    j['lean'] = K.LEAN_G * k
    j['footL'] = MV.lerp(j['footL'], (-70.0, V.ANKLE_Y, 64.0), k)
    j['footR'] = MV.lerp(j['footR'], (84.0, V.ANKLE_Y, -56.0), k)
    j['head_dy'] = 22 * k
    return j


def patriot(t):
    sp = dict(brows='serious')
    if t < T_UNFOLD + 0.35:                            # in the doorway, leaning on the west post
        k = max(0.0, min(1.0, (t - T_UNFOLD) / 0.35))
        j = leaning(C.PATRIOT) if k == 0 else MV.mix_poses(leaning(C.PATRIOT), V.standing(C.PATRIOT), MV.ease(k))
        j = _idle(j, t, 9)
        roll = -7.0 * (1 - MV.ease(k))
        sp['brows'] = 'sincere' if t < 12.4 else 'serious'
        return Actor('patriot', DOOR[0], DOOR[1], 340, j, sp, roll=roll)
    if t < T_SALUTE - 0.2:                              # walks up to them; "Just a regular man..." hand on his chest
        x, z, yaw, state = MV.travel([DOOR, APPROACH], t, 'walk', start=T_WALK)
        if state == 'moving':
            j = _into_walk(t - T_WALK, t, [DOOR, APPROACH], T_WALK)
            return Actor('patriot', x, z, yaw % 360, j, dict(sp, brows='sincere'))
        j = MV.pose(C.PATRIOT, 'heart') if 17.1 <= t < 18.5 else V.standing(C.PATRIOT)
        sp['brows'] = 'sincere'
        return Actor('patriot', x, z, 30, _idle(j, t, 10), sp)
    if t < T_BLAST:                                    # the salute; then he flaps at them
        j = flapping(C.PATRIOT, t) if t >= 21.5 else _idle(V.standing(C.PATRIOT), t, 11)
        face_cam = toward(APPROACH, PL.CAMS['s7']['pos'][::2]) if 21.5 <= t < 26.3 else 30
        sp.update(brows='alarm', lid=0) if t >= 20.5 else None
        head = None
        for a, h in LOOKS_ROUND:
            if t >= a:
                head = None if h is None else (face_cam + h) % 360
        return Actor('patriot', APPROACH[0], APPROACH[1], face_cam, j, sp, head)
    u = t - T_BLAST
    if u < 0.9:                                        # he flinches: ducks, arms up round his head, then straightens
        duck = MV.pose(C.PATRIOT, 'guard')
        duck['head_dy'] = 24
        duck['lean'] = 12
        k = min(1.0, u / 0.1) if u < 0.5 else max(0.0, 1 - (u - 0.5) / 0.4)
        j = MV.mix_poses(V.standing(C.PATRIOT), duck, MV.ease(k))
        sp['brows'] = 'alarm'
        return Actor('patriot', APPROACH[0], APPROACH[1], 30, j, sp)
    path = [APPROACH, (-0.35, -0.5), AT_GUN]
    if t < T_TO_GUN:
        j = MV.pose(C.PATRIOT, 'palm_open', beat=0.5) if 28.6 <= t < 29.6 else V.standing(C.PATRIOT)
        sp['brows'] = 'sincere'
        return Actor('patriot', APPROACH[0], APPROACH[1], 45, _idle(j, t, 12), sp)
    x, z, yaw, state = MV.travel(path, t, 'walk', start=T_TO_GUN)
    if state == 'moving':
        return Actor('patriot', x, z, yaw % 360, _into_walk(t - T_TO_GUN, t, path, T_TO_GUN), dict(sp, brows='sincere'))
    arrive = T_TO_GUN + sum(math.dist(a, b) for a, b in zip(path, path[1:])) / MV.speed('walk')
    k = max(0.0, min(1.0, (t - arrive - 0.1) / 0.45))
    fire_t = burst_t(t, P_BURSTS)
    up = T_SHAKE[0] - 0.2 <= t < T_TAKE                # the head shake and the poppy line: stood up behind the gun,
    if up:                                             # one hand on it, his chest (and the poppy) clear (Sam, note 8)
        k = min(k, 1.0 - MV.ease(min(1.0, (t - (T_SHAKE[0] - 0.2)) / 0.4)))
    elif t >= T_TAKE:
        k = MV.ease(min(1.0, (t - T_TAKE) / 0.3))
    j = at_gun(C.PATRIOT, k)
    j = _idle(j, t, 14) if fire_t is None else j
    if fire_t is not None:                             # the gun shoves him on every kick
        j['lean'] += 2.0 if int(round(fire_t * 12)) % 2 == 0 else 0.0
    sp['brows'] = 'weary' if t < 36.4 else 'fierce'
    if fire_t is not None:
        sp['lid'] = 3
    hs = _shake_head(t)
    a = Actor('patriot', AT_GUN[0], AT_GUN[1], 0, j, sp, None if hs is None else hs % 360, holds=True,
              fire_t=fire_t, reach=1.0 if up else MV.ease(k))
    a.one_hand = up
    return a


def everyone(t):
    out = [gunner(t), loader(t), patriot(t)]
    for a in out:                                      # a glance turns the head, never past the shoulder
        if a.head_facing is not None:
            d = (a.head_facing - a.facing + 540) % 360 - 180
            a.head_facing = (a.facing + max(-75.0, min(75.0, d))) % 360
    return out


# ------------------------------------------------------------------------------------------------ the gun
def gun_prop(spot, fire_t, g=None):
    """The MG42, its belt and ammo box, drawn in a holder's frame (hands go over it)."""
    g = g or gun_at(fire_t)
    firing = fire_t is not None and fire_t >= 0
    frame = int(round((fire_t or 0.0) * 12))
    flash = 1.0 if (firing and frame % 3 != 2) else 0.0

    def draw(p, j2):
        yaw = j2['yaw']
        path = C.belt_path(REST.belt_points(), 48)
        phase = -(fire_t or 0.0) * 20 * 0.032 if firing else 0.0
        C.draw_box(p, spot.to_body, yaw, REST.box_at)
        C.draw_belt(p, spot.to_body, yaw, path, g.a, phase)
        C.draw_mg42(p, spot.to_body, yaw, g, flash, seed=int((fire_t or 0) * 12))
        if firing:
            C.cases(p, spot.to_body, yaw, g, fire_t)
    draw.held = True
    return draw


def flash_on(t):
    """Is the muzzle flashing on this frame (and how bright the room is lit by it)?"""
    for bursts in (G_BURSTS, P_BURSTS):
        ft = burst_t(t, bursts)
        if ft is not None and (bursts is not G_BURSTS or t < T_FREEZE):
            return 1.0 if int(round(ft * 12)) % 3 != 2 else 0.0
    return 0.0

