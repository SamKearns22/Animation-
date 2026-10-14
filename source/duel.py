#!/usr/bin/env python3
"""duel: a 30-second wordless short with the Bingo Bingo pair (Zack and the advisor), made to celebrate the movement
system (Sam, 14 Oct). Every beat follows from the one before; no sound effects (none asked for).

    python3 source/duel.py check              every frame posed and drawn small (finds arm faults), no video
    python3 source/duel.py stills OUT.jpg     a sheet of key frames for checking
    python3 source/duel.py film OUT.mp4 [--small]   the film (--small: the quick animatic size)
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import kit                   # noqa: E402
import moves as MV           # noqa: E402
import series                # noqa: E402
import views as V            # noqa: E402
from ed import INK, curve    # noqa: E402

FPS, DUR = 12, 30.0
U = V.M_PER_UNIT
NECK = 928 * U                                   # neck base above the floor (m)
ZC = 7.5                                         # the camera's distance from the back wall (m)
WALL, FLOOR, SKIRT = (226, 228, 214), (176, 168, 150), (150, 140, 124)
DESK = dict(x0=-0.7, x1=0.7, z0=0.1, z1=0.7, top=0.74)
SHELF = dict(x0=2.85, x1=3.55, z0=0.05, z1=0.4, top=0.95)
PLAQUE = (3.2, 1.62)                             # the crossed swords on the wall (X, Y)
CUP_A, CUP_B = (-0.42, DESK['top'], 0.6), (0.3, DESK['top'], 0.6)    # where the cup is set down, first and last
STEEL, GRIP, BRASS = (214, 218, 226), (70, 46, 30), (196, 160, 70)


def cast():
    import polanski as PZ
    return dict(PZ.ZACK, mouth='set', brows=None), dict(PZ.ADV, mouth='set', brows=None)


ZACK, ADV = cast()


# ------------------------------------------------------------------------------------------------ small helpers
def seg(t, keys):
    """A value eased between timed keys [(t, value)], held before and after."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, a), (t1, b) in zip(keys, keys[1:]):
        if t < t1:
            return MV.lerp(a, b, MV.ease((t - t0) / max(1e-6, t1 - t0)))
    return keys[-1][1]


def view_of(yaw):
    return V.snap(yaw)


def to_local(a, P):
    """A world point (X, Y, Z metres) in actor a's own frame (person units: x right, y down from the neck, z ahead)."""
    deg, mir = view_of(a['yaw'])
    dX, dZ = P[0] - a['X'], P[2] - a['Z']
    if mir:
        dX = -dX
    r = math.radians(deg)
    return ((dX * math.cos(r) - dZ * math.sin(r)) / U, (NECK - P[1]) / U, (dX * math.sin(r) + dZ * math.cos(r)) / U)


def to_world(a, p):
    deg, mir = view_of(a['yaw'])
    r = math.radians(deg)
    x, y, z = p
    dX = (x * math.cos(r) + z * math.sin(r)) * U
    dZ = (-x * math.sin(r) + z * math.cos(r)) * U
    return (a['X'] + (-dX if mir else dX), NECK - y * U - a['j'].get('bob', 0.0) * U, a['Z'] + dZ)


def actor(sp, X, Z, yaw, j, **face):
    return dict(sp=sp, X=X, Z=Z, yaw=yaw, j=j, face=face, head_yaw=face.pop('head_yaw', None), items=[])


def stance(j, sg=1, wide=150.0):
    """Feet apart, front and back (fighting)."""
    j['footL'] = (-50, V.ANKLE_Y, wide)
    j['footR'] = (50, V.ANKLE_Y - 6, -wide)
    j['toeR'] = 10
    return j


def crouch(sp, depth=170.0):
    j = V.standing(sp)
    j['bob'] = depth
    for s, sg in (('L', -1), ('R', 1)):
        j['foot' + s] = (sg * 70, V.ANKLE_Y - depth, 110.0)
    j['lean'] = 24
    return j


def airborne(sp, lift):
    j = V.standing(sp)
    j['bob'] = -lift
    j['footL'] = (-60, V.ANKLE_Y - 230, 160.0)
    j['footR'] = (60, V.ANKLE_Y - 150, -60.0)
    j['lean'] = 10
    return j


# ------------------------------------------------------------------------------------------------ swords
SWORD = {   # L hand (the near hand in a side view) and the blade's direction (person frame)
    'guard': ((-40, 170, 250), (0, -0.7, 0.71)),
    'high': ((-40, -90, 300), (0, -0.35, 0.94)),
    'low': ((-40, 320, 280), (0, 0.3, 0.95)),
    'mid': ((-40, 90, 330), (0, -0.55, 0.83)),
    'over': ((-60, -330, -40), (0, -0.3, -0.95)),
    'cut': ((-20, 230, 360), (0, 0.45, 0.89)),
    'block': ((-40, -250, 190), (0, -0.04, 1.0)),
    'thrust': ((-20, 100, 470), (0, 0.0, 1.0)),
    'lock': ((-40, 60, 250), (0, -0.8, 0.6)),
}
BLADE = 0.8 / U                                   # 80 cm of blade


def sword_pose(sp, name, lean=None):
    hand, vec = SWORD[name]
    j = stance(V.standing(sp))
    V.arm_to(j, 'L', hand, 'up' if name == 'over' else ('out' if name in ('cut', 'thrust') else 'down'), 'grip')
    V.arm_to(j, 'R', (150.0, 200.0, -160.0), 'out', 'fist')        # the free arm back for balance
    j['lean'] = lean if lean is not None else {'cut': 12, 'thrust': 14, 'over': -6, 'lock': 8}.get(name, 4)
    j['blade'] = vec
    return j


# ------------------------------------------------------------------------------------------------ the camera
def camera(t):
    """(X, Y, f, sy, shake) for the moment; cuts are instant changes between shots."""
    if t < 4.6:
        return 0.1, 1.05, 2600, 1060, 0
    if t < 9.6:
        return -0.45, 1.25, seg(t, [(4.6, 3700), (9.6, 3950)]), 900, 0
    if t < 14.3:
        return None, 1.05, 2500, 1060, 0                       # follows the chase
    if t < 18.2:
        return 2.35, 1.05, 2900, 1060, 0
    if t < 18.6:
        return 3.0, 1.55, 4300, 1150, 0
    if t < 22.6:
        return None, 1.1, 2800, 1060, 1
    if t < 23.8:
        return 1.7, 1.45, 5600, 960, 0.5
    if t < 25.0:
        return 1.7, 1.15, 2900, 1060, 2
    if t < 26.8:
        return 1.6, 1.25, 2500, 1060, 0
    return None, 1.15, seg(t, [(26.8, 2900), (28.2, 3900)]), 1040, 0


# ------------------------------------------------------------------------------------------------ the story
def blink(t, off):
    return ((t + off) % 3.3) < 0.12


def state(t):
    """Everything at time t: the two people, the loose things in the room, effects, and the camera."""
    S = dict(cup=None, leaflets='shelf', pot='shelf', swords='wall', flying=[], fx=[], debris=[])
    zf = dict(blink=blink(t, 0.4))
    af = dict(blink=blink(t, 1.9))

    # ---- 1. the advisor puts his coffee down and turns to the notice board; Zack wanders in and spots it
    if t < 4.6:
        if t < 0.5:
            aj = MV.pose(ADV, 'mug')
        elif t < 1.0:
            aj = V.standing(ADV)
        else:
            aj = MV.pose(ADV, 'behind_back')                         # reading the notices
        A = actor(ADV, -0.95, 0.95, 90 if t < 1.0 else 180, aj, **af)
        if 0.5 <= t < 1.0:
            V.arm_to(aj, 'R', to_local(A, CUP_A), 'down', 'grip' if t < 0.8 else 'palm')
            if t < 0.8:
                MV.hold_cup(aj, ADV)
        S['cup'] = None if t < 0.8 else ('at', CUP_A)
        X, Z, yaw, st = MV.travel([(2.4, 0.95), (0.1, 0.95)], t, 'walk')
        if st == 'moving':
            zj = MV.gait(ZACK, t, 'walk')
            Zk = actor(ZACK, X, Z, yaw, zj, **zf)
        else:
            zj = V.standing(ZACK)
            Zk = actor(ZACK, 0.1, 0.95, -90 if t < 2.6 or t > 3.4 else -45, zj, **zf)
            if 2.6 <= t < 3.1:                                       # spots the coffee
                Zk['face'].update(brows='wow', mouth='pleased', blink=False)
                zj['head_dy'] = 10
            elif t < 3.4:                                           # a glance at the advisor's back
                Zk['face'].update(brows='fierce', mouth='pleased', look=-1.0, blink=False)
                Zk['head_yaw'] = -100
            elif t < 3.8:                                           # takes it
                V.arm_to(zj, 'R', to_local(Zk, CUP_A), 'down', 'grip' if t >= 3.6 else 'palm')
                if t >= 3.6:
                    MV.hold_cup(zj, ZACK)
                S['cup'] = ('at', CUP_A) if t < 3.6 else None
                Zk['face'].update(mouth='pleased')
            else:                                                   # and sips: bliss
                Zk['j'] = MV.pose(ZACK, 'mug_sip')
                Zk['face'].update(blink=True, brows='joy', mouth='pleased')
                S['cup'] = None
        return A, Zk, S

    # ---- 2. caught: the advisor turns round; an argument without words
    if t < 9.6:
        A = actor(ADV, -0.95, 0.95, 45, V.standing(ADV), **af)
        Zk = actor(ZACK, 0.1, 0.95, -45, MV.pose(ZACK, 'mug_sip' if t < 5.4 else 'mug'), **zf)
        if t < 5.4:
            A['face'].update(brows='outrage', mouth='agape', blink=False)
            Zk['face'].update(brows='alarm', mouth='set', look=-1.0, blink=False)
        elif t < 6.4:                                                # "that's MINE"
            A['j'] = MV.pose(ADV, 'point', target=to_local(A, (0.1, 1.3, 0.95)))
            A['face'].update(brows='fierce', mouth='shout', blink=False)
            Zk['face'].update(brows='alarm', mouth='set')
        elif t < 7.4:                                                # "is it?"
            Zk['j'] = MV.pose(ZACK, 'shrug')
            MV.hold_cup(Zk['j'], ZACK)
            Zk['face'].update(brows='sincere', mouth='pleased')
            A['face'].update(brows='fierce', mouth='set')
        elif t < 8.2:
            A['j'] = MV.pose(ADV, 'hips')
            A['face'].update(brows='fierce', mouth='set', blink=False)
            Zk['face'].update(brows='sincere', mouth='pleased')
        elif t < 9.0:                                                # a long, slow, deliberate sip
            A['j'] = MV.pose(ADV, 'hips')
            A['face'].update(brows='outrage', mouth='agape')
            Zk['j'] = MV.pose(ZACK, 'mug_sip')
            Zk['face'].update(brows='fierce', mouth='pleased', look=-1.0, blink=False)
        else:                                                        # fists up; he puts it down and bolts
            A['j'] = MV.pose(ADV, 'guard')
            A['face'].update(brows='fierce', mouth='shout', blink=False)
            Zk['yaw'] = -90 if t < 9.45 else 90
            zj = V.standing(ZACK)
            if t < 9.45:
                V.arm_to(zj, 'R', to_local(Zk, CUP_B), 'down', 'grip' if t < 9.3 else 'palm')
                if t < 9.3:
                    MV.hold_cup(zj, ZACK)
            Zk['j'] = zj
            Zk['face'].update(brows='alarm', mouth='agape', blink=False)
        S['cup'] = None if t < 9.3 else ('at', CUP_B)
        return A, Zk, S

    S['cup'] = ('at', CUP_B)
    # ---- 3. the chase, and things thrown
    if t < 14.3:
        X, Z, yaw, st = MV.travel([(0.1, 0.95), (2.95, 0.95)], t, 'run', start=9.6)
        if st == 'moving':
            Zk = actor(ZACK, X, Z, yaw, MV.gait(ZACK, t - 9.6, 'run'), brows='alarm', mouth='agape', blink=False)
        else:
            Zk = actor(ZACK, 2.95, 0.95, -90, V.standing(ZACK), **zf)
        aX, aZ, ayaw, ast = MV.travel([(-0.95, 0.95), (1.9, 0.95)], t, 'run', start=9.72)
        if ast == 'moving':
            A = actor(ADV, aX, aZ, ayaw, MV.gait(ADV, t - 9.72, 'run'), brows='fierce', mouth='shout', blink=False)
        else:
            A = actor(ADV, 1.9, 0.95, 90, MV.pose(ADV, 'guard'), brows='fierce', mouth='set', **af)
        leaf_hand = (SHELF['x0'] + 0.15, SHELF['top'] + 0.04, 0.22)
        pot_hand = (SHELF['x0'] + 0.5, SHELF['top'] + 0.1, 0.22)
        if st != 'moving' and t < 11.05:                             # grabs the leaflets, turns, winds up
            if t < 10.85:
                Zk['yaw'] = 160
                V.arm_to(Zk['j'], 'R', to_local(Zk, leaf_hand), 'down', 'grip')
                S['leaflets'] = 'hand' if t > 10.7 else 'shelf'
            else:
                V.arm_to(Zk['j'], 'R', (140.0, -230.0, -150.0), 'up', 'grip')
                S['leaflets'] = 'hand'
            Zk['face'].update(brows='fierce', mouth='grin', blink=False)
        elif 11.05 <= t < 11.4:                                      # the throw
            V.arm_to(Zk['j'], 'R', (60.0, 0.0, 430.0), 'down', 'palm')
            Zk['j']['lean'] = 10
            S['leaflets'] = 'thrown'
        elif 11.4 <= t < 11.95:                                      # grabs the plant, winds up overhead
            S['leaflets'] = 'thrown'
            if t < 11.7:
                Zk['yaw'] = 160
                V.arm_to(Zk['j'], 'R', to_local(Zk, pot_hand), 'down', 'grip')
                S['pot'] = 'hand' if t > 11.55 else 'shelf'
            else:
                V.arm_to(Zk['j'], 'R', (60.0, -330.0, -60.0), 'up', 'grip')
                Zk['j']['lean'] = -6
                S['pot'] = 'hand'
            Zk['face'].update(brows='fierce', mouth='grin', blink=False)
        elif t >= 11.95:
            S['leaflets'] = 'thrown'
            S['pot'] = 'thrown'
            if t < 12.3:
                V.arm_to(Zk['j'], 'R', (40.0, -60.0, 420.0), 'down', 'palm')
                Zk['j']['lean'] = 12
        if 11.1 <= t < 11.9 and ast != 'moving':                     # batting through the paper storm
            aj = V.standing(ADV)
            for s, sg in (('L', -1), ('R', 1)):
                V.arm_to(aj, s, (sg * (60 + 50 * math.sin(t * 40 + sg)), -120.0, 200.0), 'down', 'palm')
            aj['head_dy'] = 12
            A['j'] = aj
            A['face'].update(brows='alarm', mouth='agape', blink=True)
        if 12.2 <= t < 13.05:                                        # catches the plant, one-handed; a smug pause
            aj = MV.pose(ADV, 'standing')
            if t < 12.8:
                V.arm_to(aj, 'R', (60.0, -60.0, 380.0) if t < 12.4 else (90.0, -40.0, 300.0), 'down', 'grip')
                A['face'].update(brows='joy', mouth='grin', blink=False)
                Zk['face'].update(brows='alarm', mouth='agape', blink=False)
            else:
                V.arm_to(aj, 'R', (60.0, -330.0, -60.0), 'up', 'grip')
                aj['lean'] = -6
                A['face'].update(brows='fierce', mouth='grin', blink=False)
            A['j'] = aj
            S['pot'] = 'thrown' if t < 12.3 else 'caught'
        elif 13.05 <= t < 13.5:
            aj = MV.pose(ADV, 'standing')
            V.arm_to(aj, 'R', (40.0, -60.0, 420.0), 'down', 'palm')
            aj['lean'] = 12
            A['j'] = aj
            S['pot'] = 'back'
        if t >= 13.3:                                                # it lands on his head
            hj, _ = MV.hit_react(ZACK, t, 13.3, 1.2)
            Zk['j'] = hj
            Zk['face'].update(brows='alarm', mouth='agape', blink=(t < 13.6))
            S['pot'] = 'back' if t < 13.35 else 'broken'
            if 13.4 <= t < 14.1:
                S['fx'].append(('stars', Zk, t))
            if 14.0 <= t < 14.3:                                     # shakes it off
                Zk['head_yaw'] = -90 + (40 if int(t * 12) % 2 else -40)
                Zk['face'].update(brows='fierce', mouth='set', blink=False)
        return A, Zk, S

    S['leaflets'] = 'floor'
    S['pot'] = 'broken'
    # ---- 4. fists and feet
    if t < 19.8:
        zX = seg(t, [(14.3, 2.95), (14.7, 2.55)])
        aX = 1.9
        Zk = actor(ZACK, zX, 0.95, -90, MV.pose(ZACK, 'guard'), brows='fierce', mouth='set', **{'blink': blink(t, 0.4)})
        A = actor(ADV, aX, 0.95, 90, MV.pose(ADV, 'guard'), brows='fierce', mouth='set', **{'blink': blink(t, 1.9)})
        if 14.3 <= t < 14.7:
            Zk['j'] = MV.gait(ZACK, t - 14.3, 'walk')
        gap = lambda: abs(Zk['X'] - A['X']) / U
        if 14.4 <= t < 15.6:                                         # Zack's punch
            Zk['j'], _ = MV.punch(ZACK, t, 15.0, (0.0, -150.0, gap() - 60))
            if t >= 15.0:
                A['j'], st = MV.hit_react(ADV, t, 15.0)
                A['X'] = 1.9 - st
                A['face'].update(brows='alarm', mouth='agape', blink=t < 15.2)
                if t < 15.12:
                    S['fx'].append(('pow', (A['X'] + 0.05, 1.55, A['Z'] + 0.05)))
        if 15.5 <= t < 16.8:                                         # the advisor's kick
            A['X'] = seg(t, [(15.5, 1.65), (15.8, 1.9)])
            A['j'], _ = MV.kick(ADV, t, 16.1)
            A['face'].update(brows='fierce', mouth='shout', blink=False)
            if t >= 16.1:
                Zk['j'], st = MV.hit_react(ZACK, t, 16.1)
                Zk['X'] = 2.55 + st
                Zk['face'].update(brows='alarm', mouth='agape', blink=t < 16.3)
                if t < 16.22:
                    S['fx'].append(('pow', (Zk['X'] - 0.1, 1.0, Zk['Z'] + 0.05)))
        if 16.4 <= t < 17.6:                                         # Zack's kick
            Zk['X'] = seg(t, [(16.4, 2.8), (16.7, 2.55)])
            Zk['j'], _ = MV.kick(ZACK, t, 17.0)
            Zk['face'].update(brows='fierce', mouth='shout', blink=False)
            if t >= 17.0:
                A['j'], st = MV.hit_react(ADV, t, 17.0)
                A['X'] = 1.9 - st
                A['face'].update(brows='alarm', mouth='agape', blink=t < 17.2)
                if t < 17.12:
                    S['fx'].append(('pow', (A['X'] + 0.1, 1.0, A['Z'] + 0.05)))
        if 17.2 <= t < 18.2:                                         # the advisor's big punch
            A['X'] = seg(t, [(17.2, 1.65), (17.45, 1.9)])
            A['j'], _ = MV.punch(ADV, t, 17.7, (0.0, -150.0, gap() - 60))
            A['face'].update(brows='fierce', mouth='shout', blink=False)
            if t >= 17.7:
                Zk['j'], st = MV.hit_react(ZACK, t, 17.7, 1.6)
                Zk['X'] = seg(t, [(17.7, 2.55), (18.15, 3.1)])
                Zk['Z'] = seg(t, [(17.7, 0.95), (18.15, 0.6)])
                Zk['face'].update(brows='alarm', mouth='agape', blink=t < 17.9)
                if t < 17.82:
                    S['fx'].append(('pow', (Zk['X'] - 0.05, 1.55, Zk['Z'] + 0.05)))
        if t >= 18.2:
            A['X'] = 1.9
            Zk['X'], Zk['Z'] = 3.1, 0.6
            Zk['j'] = V.standing(ZACK)
        if 18.2 <= t < 18.6:                                         # ...and he sees the swords
            Zk['yaw'] = -45
            Zk['j']['head_dy'] = -14
            Zk['face'].update(brows='wow', mouth='grin', look=0.6, blink=False)
        elif 18.6 <= t < 18.95:
            Zk['yaw'] = 180
            for s, dx in (('L', -0.16), ('R', 0.16)):
                V.arm_to(Zk['j'], s, to_local(Zk, (PLAQUE[0] + dx, PLAQUE[1], 0.03)), 'out', 'grip')
            S['swords'] = 'wall' if t < 18.85 else 'zack2'
        elif t >= 18.95:                                             # one each: he tosses one over, fair's fair
            S['swords'] = 'zack2' if t < 19.15 else 'toss'
            Zk['X'] = seg(t, [(18.95, 3.1), (19.4, 3.0)])
            Zk['Z'] = seg(t, [(18.95, 0.6), (19.4, 0.95)])
            if t < 19.15:
                zj = V.standing(ZACK)
                V.arm_to(zj, 'L', (-120.0, 120.0, 300.0), 'down', 'grip')
                V.arm_to(zj, 'R', (120.0, 120.0, 300.0), 'down', 'grip')
                zj['blade'] = (0, -0.7, 0.71)
                Zk['j'] = zj
                Zk['face'].update(brows='fierce', mouth='grin', blink=False)
            else:
                Zk['j'] = sword_pose(ZACK, 'guard')
                Zk['face'].update(brows='fierce', mouth='grin', blink=False)
            if t >= 19.45:
                S['swords'] = 'both'
                A['j'] = sword_pose(ADV, 'guard')
                A['X'] = seg(t, [(19.5, 1.9), (19.8, 1.6)])
                A['face'].update(brows='fierce', mouth='grin', blink=False)
            elif t >= 19.2:
                aj = V.standing(ADV)
                V.arm_to(aj, 'L', (-60.0, -40.0, 360.0), 'down', 'palm')
                A['j'] = aj
                A['face'].update(brows='wow', mouth='agape', blink=False)
        return A, Zk, S

    S['swords'] = 'both'
    # ---- 5. the sword fight
    return sword_fight(t, S)


FLURRY = [('high', 'high'), ('low', 'low'), ('mid', 'mid'), ('cut', 'block'), ('high', 'high'), ('low', 'low'),
          ('thrust', 'mid'), ('mid', 'mid')]


def sword_fight(t, S):
    f = int(round(t * FPS))
    A = actor(ADV, 1.6, 0.95, 90, sword_pose(ADV, 'guard'), brows='fierce', mouth='grin', blink=False)
    Zk = actor(ZACK, 3.0, 0.95, -90, sword_pose(ZACK, 'guard'), brows='fierce', mouth='grin', blink=False)
    if t < 21.0:                                                     # a) the opening exchange, two drawings a clash
        A['X'] = seg(t, [(19.8, 1.6), (21.0, 1.85)])
        Zk['X'] = seg(t, [(19.8, 3.0), (21.0, 3.25)])
        k = int((t - 19.8) * FPS)
        if k % 2:
            a, z = FLURRY[(k // 2) % len(FLURRY)]
            A['j'], Zk['j'] = sword_pose(ADV, a), sword_pose(ZACK, z)
            S['clash'] = True
        else:
            A['j'], Zk['j'] = sword_pose(ADV, 'over' if (k // 2) % 2 else 'guard'), sword_pose(ZACK, 'guard')
        A['face']['mouth'] = 'shout' if k % 4 == 1 else 'grin'
        return A, Zk, S
    if t < 21.6:                                                     # b) the advisor spins round, blade out; Zack ducks
        A['X'], Zk['X'] = 1.85, 3.25
        k = int((t - 21.0) * FPS)
        A['yaw'] = [90, 0, -90, 180, 90, 0, -90, 180][min(k, 7)] if k < 5 else 90
        A['j'] = sword_pose(ADV, 'thrust' if k < 5 else 'guard')
        Zk['j'] = crouch(ZACK) if 1 <= k < 6 else sword_pose(ZACK, 'guard')
        if 1 <= k < 6:
            V.arm_to(Zk['j'], 'L', (-60.0, 200.0, 250.0), 'down', 'grip')
            Zk['j']['blade'] = (0, -0.3, 0.95)
            Zk['face'].update(brows='alarm', mouth='agape')
        return A, Zk, S
    if t < 22.6:                                                     # c) Zack leaps right over him
        u = (t - 21.7) / 0.55
        A['X'] = 1.85 if t < 22.35 else seg(t, [(22.35, 1.85), (22.6, 2.25)])
        if t < 21.7:
            Zk['X'] = 3.25
            Zk['j'] = crouch(ZACK, 120)
            V.arm_to(Zk['j'], 'L', (-60.0, 100.0, 250.0), 'down', 'grip')
            Zk['j']['blade'] = (0, -0.7, 0.71)
            A['j'] = sword_pose(ADV, 'guard')
        elif u < 1.0:
            Zk['X'] = 3.25 + (1.2 - 3.25) * u
            Zk['j'] = airborne(ZACK, 700 * math.sin(math.pi * u))
            V.arm_to(Zk['j'], 'L', (-60.0, -260.0, 160.0), 'down', 'grip')
            Zk['j']['blade'] = (0, -0.9, 0.4)
            Zk['face'].update(mouth='cheer', brows='joy')
            A['j'] = sword_pose(ADV, 'low')                          # sweeps at the empty air where he was
            A['face'].update(brows='wow', mouth='agape')
            A['head_yaw'] = 45
        else:
            Zk['X'] = 1.2
            Zk['yaw'] = 90
            A['yaw'] = -90 if t >= 22.35 else 90
            Zk['j'] = sword_pose(ZACK, 'guard')
            A['j'] = sword_pose(ADV, 'guard')
            A['face'].update(brows='outrage', mouth='agape')
        return A, Zk, S
    Zk['yaw'], A['yaw'] = 90, -90
    if t < 23.8:                                                     # d) blades locked, nose to nose
        Zk['X'], A['X'] = 1.2, 2.25
        A['j'], Zk['j'] = sword_pose(ADV, 'lock'), sword_pose(ZACK, 'lock')
        w = 30 * math.sin(t * 9)
        A['j']['lean'] += 4 + w * 0.1
        Zk['j']['lean'] += 4 - w * 0.1
        S['clash'] = int(t * 12) % 3 == 0
        S['fx'].append(('sweat', Zk, t))
        S['fx'].append(('sweat', A, t + 0.5))
        return A, Zk, S
    if t < 25.0:                                                     # e) faster than the eye: a clash every drawing
        Zk['X'] = seg(t, [(23.8, 1.2), (24.0, 1.0)])
        A['X'] = seg(t, [(23.8, 2.25), (24.0, 2.4)])
        if t >= 24.0:
            a, z = FLURRY[f % len(FLURRY)]
            A['j'], Zk['j'] = sword_pose(ADV, a), sword_pose(ZACK, z)
            S['clash'] = True
            S['smear'] = True
            S['fx'].append(('speed', t))
            A['face']['mouth'] = 'shout' if f % 2 else 'grin'
            Zk['face']['mouth'] = 'grin' if f % 2 else 'shout'
        return A, Zk, S
    if t < 26.8:                                                     # f) one almighty cut, and the end of Zack's sword
        Zk['X'] = 1.0
        A['X'] = seg(t, [(25.0, 2.4), (25.3, 2.2)])
        if t < 25.25:
            A['j'] = sword_pose(ADV, 'over')
            Zk['j'] = sword_pose(ZACK, 'block')
        elif t < 25.9:
            A['j'] = sword_pose(ADV, 'cut' if t >= 25.35 else 'over')
            Zk['j'] = sword_pose(ZACK, 'block')
        else:
            A['j'] = V.standing(ADV)
            Zk['j'] = sword_pose(ZACK, 'block')
        S['broken'] = t >= 25.4
        if 25.35 <= t < 25.5:
            S['clash'] = True
        if t >= 25.4:
            Zk['face'].update(brows='alarm', mouth='agape')
            A['face'].update(brows='joy', mouth='grin')
            Zk['j']['head_dy'] = -10 if t < 26.2 else 16              # watches the tip fly up, then come down
        if t >= 26.4:                                                 # drops the hilt; hands up
            Zk['j'] = MV.pose(ZACK, 'standing')
            for s, sg in (('L', -1), ('R', 1)):
                V.arm_to(Zk['j'], s, (sg * 210.0, -300.0, 60.0), 'out', 'palm')
            Zk['face'].update(brows='alarm', mouth='set')
            S['hilt'] = 'floor'
        if t >= 26.5:
            S['adv_sword'] = 'floor'
        return A, Zk, S
    return finale(t, S)


def finale(t, S):
    """g) The winner goes back for the coffee."""
    S['broken'], S['hilt'], S['adv_sword'] = True, 'floor', 'floor'
    zj = MV.pose(ZACK, 'standing')
    for s, sg in (('L', -1), ('R', 1)):
        V.arm_to(zj, s, (sg * 210.0, -300.0, 60.0), 'out', 'palm')
    Zk = actor(ZACK, 1.0, 0.95, 90, zj, brows='alarm', mouth='set', blink=blink(t, 0.4))
    X, Z, yaw, st = MV.travel([(2.2, 1.25), (0.35, 1.25)], t, 'brisk', start=26.8)
    if st == 'moving':
        A = actor(ADV, X, Z, yaw, MV.gait(ADV, t - 26.8, 'brisk'), brows='joy', mouth='grin', blink=blink(t, 1.9))
        Zk['head_yaw'] = 0 if X < 1.3 else 90                       # his eyes follow her past
        return A, Zk, S
    A = actor(ADV, 0.35, 1.25, 180, V.standing(ADV), brows='joy', mouth='grin', blink=blink(t, 1.9))
    Zk['head_yaw'] = -45
    if t < 28.35:                                                    # picks it up
        V.arm_to(A['j'], 'R', to_local(A, CUP_B), 'down', 'grip' if t > 28.15 else 'palm')
        # his back is to us: the cup in his hand is hidden in front of him
        S['cup'] = None if t > 28.15 else ('at', CUP_B)
        return A, Zk, S
    S['cup'] = None
    A['yaw'] = 0
    if t < 28.7:                                                     # raised in triumph
        V.arm_to(A['j'], 'R', (200.0, -260.0, 60.0), 'out', 'grip')
        MV.hold_cup(A['j'], ADV)
        A['face'].update(brows='joy', mouth='cheer', blink=False)
    elif t < 29.1:                                                   # the victory sip
        A['j'] = MV.pose(ADV, 'mug_sip')
        A['face'].update(brows='joy', mouth='pleased', blink=True)
    elif t < 29.55:                                                  # ...empty. Upside down: one drop
        V.arm_to(A['j'], 'R', (250.0, -40.0, 140.0), 'out', 'grip')          # held out to the side, upside down
        A['j']['upturned'] = True
        A['face'].update(brows='confused', mouth='set', blink=False, look=0.0)
        if t >= 29.25:
            S['fx'].append(('drop', A, t))
    else:                                                            # to us, deadpan
        V.arm_to(A['j'], 'R', (250.0, -40.0, 140.0), 'out', 'grip')          # held out to the side, upside down
        A['j']['upturned'] = True
        A['face'].update(brows='weary', mouth='set', blink=False, look=0.0)
        Zk['face'].update(brows='sincere', mouth='pleased')
    return A, Zk, S


# ------------------------------------------------------------------------------------------------ drawing the set
def lw(room, Z, w=2.6):
    return w * (room.k(Z) * U) ** 0.6 / max(1e-6, 1.0) ** 0.6


def box(p, room, x0, x1, y0, y1, z0, z1, top, front, side):
    """A box seen from the front camera: its top, its front, and the side that faces the camera's line."""
    L = lw(room, z1)
    p.poly(room.quad([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)]), top, INK, L)
    if room.X > x1:
        p.poly(room.quad([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)]), side, INK, L)
    elif room.X < x0:
        p.poly(room.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)]), side, INK, L)
    p.poly(room.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]), front, INK, L)


def cup_world(p, room, P, upright=True):
    X, Y, Z = P
    k = room.k(Z)
    L = lw(room, Z, 2.2)
    c = room.P(X, Y, Z)
    h, w = 0.12 * k, 0.04 * k
    pts = [(c[0] - w, c[1] - h), (c[0] + w, c[1] - h), (c[0] + w * 0.78, c[1]), (c[0] - w * 0.78, c[1])]
    p.poly(pts, (246, 245, 241), INK, L)
    p.poly([(c[0] - w * 1.1, c[1] - h * 1.18), (c[0] + w * 1.1, c[1] - h * 1.18), (c[0] + w * 1.05, c[1] - h * 0.96),
            (c[0] - w * 1.05, c[1] - h * 0.96)], (60, 60, 66), INK, L * 0.8)
    p.poly([(c[0] - w * 0.94, c[1] - h * 0.6), (c[0] + w * 0.94, c[1] - h * 0.6), (c[0] + w * 0.86, c[1] - h * 0.3),
            (c[0] - w * 0.86, c[1] - h * 0.3)], (170, 120, 80), None)


def leaflet_quad(c, k, ang, colr, p, L):
    w, h = 0.105 * k, 0.074 * k
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(c[0] + x * ca - y * sa, c[1] + x * sa + y * ca) for x, y in ((-w, -h), (w, -h), (w, h), (-w, h))]
    p.poly(pts, colr, INK, L)
    p.line([(pts[0][0] * 0.7 + pts[2][0] * 0.3, pts[0][1] * 0.7 + pts[2][1] * 0.3),
            (pts[1][0] * 0.7 + pts[3][0] * 0.3, pts[1][1] * 0.7 + pts[3][1] * 0.3)], (40, 120, 60), max(1.0, L * 0.6))


def pot_at(p, c, k, L, ang=0.0):
    """A terracotta pot with a leafy plant, centred on c (pixels at zoom 1), k pixels a metre."""
    ca, sa = math.cos(ang), math.sin(ang)
    R = lambda x, y: (c[0] + (x * ca - y * sa) * k, c[1] + (x * sa + y * ca) * k)
    for lx, ly, s in ((-0.08, -0.2, 1), (0.0, -0.26, 1), (0.08, -0.19, 1), (-0.03, -0.16, -1), (0.05, -0.15, 1)):
        p.poly([R(0, -0.06), R(lx - 0.03 * s, ly + 0.03), R(lx, ly), R(lx + 0.03 * s, ly + 0.05)], (70, 140, 70), INK, L * 0.8)
    p.poly([R(-0.08, -0.07), R(0.08, -0.07), R(0.06, 0.08), R(-0.06, 0.08)], (190, 100, 64), INK, L)
    p.poly([R(-0.09, -0.09), R(0.09, -0.09), R(0.09, -0.05), R(-0.09, -0.05)], (204, 114, 76), INK, L)


def sword_line(p, a, b, L, length_frac=1.0, colr=STEEL):
    """A sabre from hilt end a towards b (pixels at zoom 1): grip, guard, blade."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1.0
    ux, uy = dx / n, dy / n
    g = (a[0] + ux * n * 0.16, a[1] + uy * n * 0.16)
    tip = (g[0] + ux * n * 0.84 * length_frac, g[1] + uy * n * 0.84 * length_frac)
    p.line([a, g], GRIP, L * 3.2)
    p.line([(g[0] - uy * n * 0.06, g[1] + ux * n * 0.06), (g[0] + uy * n * 0.06, g[1] - ux * n * 0.06)], BRASS, L * 2.6)
    wb = max(2.0, n * 0.018)
    p.poly([(g[0] - uy * wb, g[1] + ux * wb), (tip[0], tip[1]), (g[0] + uy * wb, g[1] - ux * wb)], colr, INK, L)
    return g, tip


def draw_set(img, cam, room, S, t):
    p = B.Pen(img, cam)
    L0 = lw(room, 0.0)
    W_ = 1080
    # the wall and the floor
    p.poly([(-4000, -4000), (6000, -4000), (6000, room.P(0, 0, 0.0)[1]), (-4000, room.P(0, 0, 0.0)[1])], WALL, None)
    near = ZC - 0.6
    p.poly(room.quad([(-9, 0, 0), (9, 0, 0), (9, 0, near), (-9, 0, near)]), FLOOR, None)
    z = 0.5
    while z < near:
        p.line(room.quad([(-9, 0, z), (9, 0, z)]), (166, 158, 140), max(1.0, L0 * 0.5))
        z += 0.5
    p.poly(room.quad([(-9, 0, 0.0), (9, 0, 0.0), (9, 0.1, 0.0), (-9, 0.1, 0.0)]), SKIRT, INK, L0)
    # things on the wall: the notice board, a clock, a poster, the swords
    p.poly(room.quad([(-1.4, 1.2, 0), (-0.5, 1.2, 0), (-0.5, 1.8, 0), (-1.4, 1.8, 0)]), (182, 140, 96), INK, L0)
    for i, (x, y, c) in enumerate(((-1.28, 1.7, (250, 250, 240)), (-1.0, 1.66, (200, 230, 200)), (-0.75, 1.72, (250, 240, 200)),
                                   (-1.15, 1.42, (240, 240, 250)), (-0.82, 1.4, (250, 250, 240)))):
        p.poly(room.quad([(x, y, 0), (x + 0.2, y, 0), (x + 0.2, y - 0.22, 0), (x, y - 0.22, 0)]), c, INK, L0 * 0.7)
        p.ell(*room.P(x + 0.1, y - 0.02, 0), 3, 3, (200, 40, 40), None)
    cx, cy = room.P(0.25, 2.25, 0)
    r = 0.16 * room.k(0)
    p.ell(cx, cy, r, r, (250, 250, 246), INK, L0)
    ang = t * 0.5
    p.line([(cx, cy), (cx + r * 0.7 * math.sin(ang), cy - r * 0.7 * math.cos(ang))], INK, L0)
    p.line([(cx, cy), (cx + r * 0.45 * math.sin(ang / 12), cy - r * 0.45 * math.cos(ang / 12))], INK, L0 * 1.3)
    p.poly(room.quad([(1.2, 1.25, 0), (1.85, 1.25, 0), (1.85, 2.05, 0), (1.2, 2.05, 0)]), (40, 140, 70), INK, L0)
    lc = room.P(1.525, 1.7, 0)
    k0 = room.k(0)
    p.poly([(lc[0], lc[1] - 0.2 * k0), (lc[0] + 0.12 * k0, lc[1]), (lc[0], lc[1] + 0.2 * k0), (lc[0] - 0.12 * k0, lc[1])],
           (250, 250, 240), INK, L0)
    p.line([(lc[0], lc[1] - 0.16 * k0), (lc[0], lc[1] + 0.26 * k0)], (40, 140, 70), L0 * 1.2)
    px, py = PLAQUE
    p.poly(room.quad([(px - 0.3, py + 0.22, 0), (px + 0.3, py + 0.22, 0), (px + 0.24, py - 0.18, 0), (px, py - 0.3, 0),
                      (px - 0.24, py - 0.18, 0)]), (120, 76, 44), INK, L0)
    if S['swords'] == 'wall':
        for s in (-1, 1):
            a = room.P(px + s * 0.28, py - 0.26, 0)
            b = room.P(px - s * 0.38, py + 0.4, 0)
            sword_line(p, a, b, L0)
    else:
        for s in (-1, 1):
            p.ell(*room.P(px + s * 0.12, py + 0.08, 0), 4, 4, (90, 90, 96), INK, L0 * 0.6)
    # the desk and its cup; the low shelf with leaflets and a plant
    d = DESK
    box(p, room, d['x0'], d['x1'], 0, d['top'], d['z0'], d['z1'], (150, 110, 74), (128, 90, 58), (112, 80, 52))
    if S['cup'] and S['cup'][0] == 'at':
        cup_world(p, room, S['cup'][1])
    sh = SHELF
    box(p, room, sh['x0'], sh['x1'], 0, sh['top'], sh['z0'], sh['z1'], (236, 236, 228), (220, 220, 210), (200, 200, 190))
    zm = (sh['z0'] + sh['z1']) / 2
    if S['leaflets'] == 'shelf':
        for i in range(5):
            leaflet_quad(room.P(sh['x0'] + 0.18, sh['top'] + 0.01 + 0.012 * i, zm), room.k(zm), 0.0,
                         (60, 150, 80) if i == 4 else (250, 250, 244), p, lw(room, zm, 1.4))
    if S['pot'] == 'shelf':
        pot_at(p, room.P(sh['x0'] + 0.5, sh['top'] + 0.08, zm), room.k(zm), lw(room, zm))


def draw_floor_things(img, cam, room, S, t, Zk):
    """Things lying on the floor (drawn before the people)."""
    p = B.Pen(img, cam)
    if S['leaflets'] in ('thrown', 'floor'):
        rng = np.random.default_rng(3)
        for i in range(14):
            fx, fz = 1.5 + rng.uniform(0, 1.1), 0.5 + rng.uniform(0, 1.0)
            land = 11.9 + rng.uniform(0, 0.5)
            if t >= land:
                k = room.k(fz)
                c = room.P(fx, 0.003, fz)
                leaflet_quad(c, k, rng.uniform(-0.4, 0.4), (60, 150, 80) if i % 3 == 0 else (250, 250, 244), p,
                             lw(room, fz, 1.2))
    if S['pot'] == 'broken' and t >= 13.6:
        X, Z = 2.7, 1.2
        k = room.k(Z)
        L = lw(room, Z)
        c = room.P(X, 0, Z)
        p.poly(curve([(c[0] - 0.14 * k, c[1]), (c[0] - 0.05 * k, c[1] - 0.05 * k), (c[0] + 0.08 * k, c[1] - 0.04 * k),
                      (c[0] + 0.16 * k, c[1])], 4), (96, 70, 48), INK, L)
        for dx, ang in ((-0.2, 0.4), (0.22, -0.6), (0.05, 1.2)):
            q = room.P(X + dx, 0, Z + 0.05)
            p.poly([(q[0] - 0.04 * k, q[1]), (q[0] + 0.04 * k * math.cos(ang), q[1] - 0.03 * k), (q[0] + 0.05 * k, q[1])],
                   (190, 100, 64), INK, L * 0.8)
        pot_at(p, room.P(X - 0.25, 0.04, Z + 0.1), k, L, ang=1.4)
    if S.get('hilt') == 'floor' and t >= 26.55:
        a, b = room.P(0.75, 0.01, 1.15), room.P(1.0, 0.01, 1.2)
        sword_line(p, a, b, lw(room, 1.2), length_frac=0.35)
    if S.get('adv_sword') == 'floor' and t >= 26.65:
        a, b = room.P(2.55, 0.01, 0.75), room.P(3.35, 0.01, 0.85)
        sword_line(p, a, b, lw(room, 0.8))


def hand_px(a, room, side):
    """Where actor a's hand is, in pixels at zoom 1, and the person's scale."""
    x, y, s = room.person(a['X'], a['Z'])
    j = a['j']
    deg, mir = view_of(a['yaw'])
    w2, _ = V.project(V.leaned(j['wr' + side], j.get('lean', 0.0)), deg)
    return (x + (-w2[0] if mir else w2[0]) * s, y + (w2[1] + j.get('bob', 0.0)) * s), s


def blade_px(a, room):
    j = a['j']
    if 'blade' not in j:
        return None
    deg, mir = view_of(a['yaw'])
    (hx, hy), s = hand_px(a, room, 'L')
    d2, _ = V.project(j['blade'], deg)
    dx, dy = (-d2[0] if mir else d2[0]), d2[1]
    return (hx - dx * 0.16 * BLADE * s, hy - dy * 0.16 * BLADE * s), (hx + dx * BLADE * s, hy + dy * BLADE * s)


def draw_held(img, cam, room, a, S, who, t):
    p = B.Pen(img, cam)
    L = lw(room, a['Z'])
    if who == 'zack' and S['leaflets'] == 'hand':
        (hx, hy), s = hand_px(a, room, 'R')
        k = room.k(a['Z'])
        for i in range(4):
            leaflet_quad((hx, hy - 0.02 * k * i), k, 0.3, (60, 150, 80) if i == 3 else (250, 250, 244), p, L * 0.6)
    if (who == 'zack' and S['pot'] == 'hand') or (who == 'adv' and S['pot'] == 'caught'):
        (hx, hy), s = hand_px(a, room, 'R')
        pot_at(p, (hx, hy - 0.04 * room.k(a['Z'])), room.k(a['Z']), L)
    if a['j'].get('upturned'):
        (hx, hy), s = hand_px(a, room, 'R')
        cup_world_px(p, (hx, hy + 0.08 * room.k(a['Z'])), room.k(a['Z']), L)
    b = blade_px(a, room)
    if b is not None:
        if who == 'zack' and a['j'].get('blade') and S['swords'] == 'zack2':
            (hx, hy), s = hand_px(a, room, 'R')
            sword_line(p, (hx - 0.12 * (b[1][0] - b[0][0]) / 1.16, hy - 0.12 * (b[1][1] - b[0][1]) / 1.16),
                       (hx + (b[1][0] - b[0][0]) * 0.86, hy + (b[1][1] - b[0][1]) * 0.86), L)
        frac = 0.3 if (who == 'zack' and S.get('broken')) else 1.0
        if S.get('smear') and t >= 24.0:
            prev = state(t - 1.0 / FPS)
            pa = prev[0] if who == 'adv' else prev[1]
            pb = blade_px(pa, room)
            if pb:
                p.poly([b[0], b[1], pb[1], pb[0]], (236, 238, 244), None)
        sword_line(p, b[0], b[1], L, frac)
    return b


def cup_world_px(p, c, k, L):
    """The takeaway cup held upside down by its base (c: the hand, pixels at zoom 1)."""
    h, w = 0.12 * k, 0.04 * k
    p.poly([(c[0] - w * 0.78, c[1] - h * 0.1), (c[0] + w * 0.78, c[1] - h * 0.1), (c[0] + w, c[1] + h * 0.9),
            (c[0] - w, c[1] + h * 0.9)], (246, 245, 241), INK, L)
    p.poly([(c[0] - w * 1.1, c[1] + h * 1.08), (c[0] + w * 1.1, c[1] + h * 1.08), (c[0] + w * 1.05, c[1] + h * 0.86),
            (c[0] - w * 1.05, c[1] + h * 0.86)], (60, 60, 66), INK, L * 0.8)
    p.ell(c[0], c[1], 0.022 * k, 0.02 * k, ADV['skin'], INK, L)


def arc(P0, P1, u, height):
    return (P0[0] + (P1[0] - P0[0]) * u, P0[1] + (P1[1] - P0[1]) * u + height * 4 * u * (1 - u), P0[2] + (P1[2] - P0[2]) * u)


def draw_flying(img, cam, room, S, t, A, Zk):
    p = B.Pen(img, cam)
    if S['leaflets'] == 'thrown' and t < 12.5:                       # the paper storm
        rng = np.random.default_rng(3)
        for i in range(14):
            fx, fz = 1.5 + rng.uniform(0, 1.1), 0.5 + rng.uniform(0, 1.0)
            land = 11.9 + rng.uniform(0, 0.5)
            if t < land:
                u = max(0.0, (t - 11.05) / (land - 11.05))
                P0 = (2.75, 1.6, 0.95)
                P1 = (fx, 0.003, fz)
                Q = arc(P0, P1, u, 0.5 + rng.uniform(0, 0.4))
                Q = (Q[0] + 0.08 * math.sin(t * 9 + i), Q[1], Q[2])
                leaflet_quad(room.P(*Q), room.k(Q[2]), math.sin(t * 7 + i * 1.3) * 1.2, (60, 150, 80) if i % 3 == 0 else (250, 250, 244),
                             p, lw(room, Q[2], 1.2))
    if S['pot'] == 'thrown':                                         # Zack -> the advisor's hand
        u = min(1.0, (t - 11.95) / 0.35)
        Q = arc((2.85, 1.85, 0.95), (2.4, 1.45, 0.95), u, 0.25)
        pot_at(p, room.P(*Q), room.k(Q[2]), lw(room, Q[2]), ang=u * 4)
    if S['pot'] == 'back':                                           # ...and straight back at his head
        u = min(1.0, (t - 13.05) / 0.3)
        Q = arc((2.35, 1.75, 0.95), (2.95, 1.65, 0.95), u, 0.15)
        pot_at(p, room.P(*Q), room.k(Q[2]), lw(room, Q[2]), ang=-u * 5)
    if S['pot'] == 'broken' and t < 13.6:                            # bounces off and falls
        u = min(1.0, (t - 13.35) / 0.25)
        Q = (2.95 - 0.25 * u, 1.65 - 1.6 * u * u, 1.1)
        pot_at(p, room.P(*Q), room.k(Q[2]), lw(room, Q[2]), ang=2 + u * 3)
        for i in range(6):
            q = room.P(2.95 + 0.06 * math.cos(i), 1.6 - 1.2 * u * (0.5 + i / 10), 1.0)
            p.ell(q[0], q[1], 3, 3, (96, 70, 48), None)
    if S['swords'] == 'toss':                                        # a sabre spun across the room
        u = min(1.0, (t - 19.15) / 0.3)
        Q = arc((2.8, 1.4, 0.95), (2.25, 1.35, 0.95), u, 0.35)
        c = room.P(*Q)
        k = room.k(Q[2])
        ang = u * 9
        a = (c[0] - 0.45 * k * math.cos(ang), c[1] - 0.45 * k * math.sin(ang))
        b = (c[0] + 0.5 * k * math.cos(ang), c[1] + 0.5 * k * math.sin(ang))
        sword_line(p, a, b, lw(room, Q[2]))
    if S.get('broken') and t < 26.25:                                # the tip: up, over, and down into the floor
        u = (t - 25.4) / 0.85
        Q = (1.35 + 0.0 * u, 1.85 + 2.6 * u - 4.3 * u * u, 1.0)
        c = room.P(*Q)
        k = room.k(1.0)
        ang = u * 14
        sword_line(p, (c[0] - 0.28 * k * math.cos(ang), c[1] - 0.28 * k * math.sin(ang)),
                   (c[0] + 0.28 * k * math.cos(ang), c[1] + 0.28 * k * math.sin(ang)), lw(room, 1.0), colr=STEEL)
    elif S.get('broken'):                                            # stuck in the floor at his toes
        base = room.P(1.33, 0.0, 1.12)
        k = room.k(1.12)
        wob = 0.06 * math.sin((t - 26.25) * 40) * math.exp(-(t - 26.25) * 4)
        tip_end = (base[0] - 0.5 * k * math.sin(0.25 + wob), base[1] - 0.5 * k * math.cos(0.25 + wob))
        wb = 0.012 * k
        p.poly([(tip_end[0] - wb, tip_end[1]), (base[0], base[1] + 0.02 * k), (tip_end[0] + wb, tip_end[1])], STEEL, INK,
               lw(room, 1.12))
        if t < 26.6:
            for s in (-1, 1):
                p.line([(tip_end[0] + s * 0.05 * k, tip_end[1] + 0.05 * k), (tip_end[0] + s * 0.1 * k, tip_end[1])], INK,
                       lw(room, 1.12) * 0.8)


def star(p, c, r, colr=(255, 236, 120), n=8, inner=0.45, L=2.0):
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        rr = r if i % 2 == 0 else r * inner
        pts.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a)))
    p.poly(pts, colr, INK, L)


def nearest(a, b):
    """The closest point between two segments (pixels): where the blades meet."""
    best = None
    for i in range(11):
        u = i / 10
        P = (a[0][0] + (a[1][0] - a[0][0]) * u, a[0][1] + (a[1][1] - a[0][1]) * u)
        for jx in range(11):
            v = jx / 10
            Q = (b[0][0] + (b[1][0] - b[0][0]) * v, b[0][1] + (b[1][1] - b[0][1]) * v)
            d = math.hypot(P[0] - Q[0], P[1] - Q[1])
            if best is None or d < best[0]:
                best = (d, ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2))
    return best[1]


def draw_fx(img, cam, room, S, t, blades):
    p = B.Pen(img, cam)
    for fx in S['fx']:
        if fx[0] == 'pow':
            c = room.P(*fx[1])
            star(p, c, 0.16 * room.k(fx[1][2]), (255, 250, 220), 9, 0.5, lw(room, fx[1][2]))
        elif fx[0] == 'stars':
            a, tt = fx[1], fx[2]
            x, y, s = room.person(a['X'], a['Z'])
            for i in range(3):
                ang = tt * 7 + i * 2.1
                c = (x + 90 * s * math.cos(ang), y - 290 * s + 26 * s * math.sin(ang))
                star(p, c, 22 * s, (255, 226, 90), 5, 0.45, lw(room, a['Z']) * 0.8)
        elif fx[0] == 'sweat':
            a, tt = fx[1], fx[2]
            x, y, s = room.person(a['X'], a['Z'])
            u = (tt * 2.0) % 1.0
            c = (x + 30 * s, y - 230 * s + 120 * s * u)
            p.poly([(c[0], c[1] - 18 * s), (c[0] + 9 * s, c[1]), (c[0], c[1] + 8 * s), (c[0] - 9 * s, c[1])], (190, 226, 250),
                   INK, lw(room, a['Z']) * 0.7)
        elif fx[0] == 'drop':
            a, tt = fx[1], fx[2]
            (hx, hy), s = hand_px(a, room, 'R')
            u = min(1.0, (tt - 29.25) / 0.3)
            fall_px = (room.P(a['X'], 0, a['Z'])[1] - hy) * u * u
            c = (hx, hy + 0.2 * room.k(a['Z']) + fall_px)
            p.poly([(c[0], c[1] - 14 * s * 2), (c[0] + 8 * s * 2, c[1]), (c[0], c[1] + 7 * s * 2), (c[0] - 8 * s * 2, c[1])],
                   (150, 104, 66), INK, lw(room, a['Z']) * 0.7)
    if S.get('clash') and blades[0] and blades[1]:
        c = nearest(blades[0], blades[1])
        r = 0.09 * room.k(1.0) * (1.6 if S.get('broken') else 1.0)
        star(p, c, r, (255, 244, 170), 10, 0.35, lw(room, 1.0))
        for i in range(8):
            a = i * 0.8 + t * 5
            p.line([(c[0] + r * 0.9 * math.cos(a), c[1] + r * 0.9 * math.sin(a)),
                    (c[0] + r * 1.7 * math.cos(a), c[1] + r * 1.7 * math.sin(a))], (255, 200, 60), lw(room, 1.0))


def speed_lines(img, cam, t):
    p = B.Pen(img, cam)
    rng = np.random.default_rng(int(t * 12))
    for _ in range(26):
        y = rng.uniform(150, 1800)
        x0 = rng.uniform(-100, 900)
        p.line([(x0, y), (x0 + rng.uniform(200, 600), y)], (246, 246, 240), rng.uniform(3, 8))


# ------------------------------------------------------------------------------------------------ one frame
SIDE_MOUTH = {'shout': 'v:A', 'agape': 'v:O', 'cheer': 'v:A', 'pleased': 'smile'}


def draw_actor(img, cam, room, a, t):
    x, y, s = room.person(a['X'], a['Z'])
    kit.feet_shadow(img, cam, x, y, s)
    sp = dict(a['sp'], **a['face'])
    deg, _ = view_of(a['yaw'] if a['head_yaw'] is None else a['head_yaw'])
    if deg in (90, 135, 180) and sp.get('mouth') in SIDE_MOUTH:
        sp['mouth'] = SIDE_MOUTH[sp['mouth']]
    if sp.get('brows') in ('outrage', 'alarm', 'sincere', 'confused', 'weary', 'serious') and deg != 0:
        sp['brows'] = {'outrage': 'wow', 'alarm': 'wow', 'sincere': 'joy'}.get(sp['brows'])
    V.person(img, cam, x, y, s, sp, t, a['yaw'], a['j'], a['head_yaw'])


def render(t, small=False):
    B.SS = 1 if small else 2
    A, Zk, S = state(t)
    cX, cY, f, sy, shake = camera(t)
    if cX is None:
        cX = (A['X'] + Zk['X']) / 2 if t < 26.8 else seg(t, [(26.8, 1.6), (28.2, 0.68)])
        if 9.6 <= t < 14.3:
            cX = min(2.35, cX + 0.2)
    rng = np.random.default_rng(int(t * FPS) + 7)
    jx = jy = 0.0
    if shake and (S.get('clash') or S['fx'] and S['fx'][0][0] == 'pow'):
        jx, jy = rng.uniform(-14, 14) * shake, rng.uniform(-10, 10) * shake
    room = series.Room(cX, cY, ZC, f, sx=540 + jx, sy=sy + jy)
    img = B.canvas(WALL)
    cam = B.Cam(1.0, 540, 960)
    draw_set(img, cam, room, S, t)
    if S['fx'] and S['fx'][-1][0] == 'speed':
        speed_lines(img, cam, t)
    draw_floor_things(img, cam, room, S, t, Zk)
    blades = {}
    for who, a in sorted((('adv', A), ('zack', Zk)), key=lambda w: w[1]['Z']):
        draw_actor(img, cam, room, a, t)
        blades[who] = draw_held(img, cam, room, a, S, who, t)
    draw_flying(img, cam, room, S, t, A, Zk)
    draw_fx(img, cam, room, S, t, (blades.get('adv'), blades.get('zack')))
    out = img.convert('RGB')
    size = (540, 960) if small else (1080, 1920)
    return out.resize(size, Image.LANCZOS)


def _frame(args):
    i, small = args
    return np.asarray(render(i / FPS, small)).tobytes()


def film(out, small=False):
    import imageio_ffmpeg
    from multiprocessing import Pool
    n = int(DUR * FPS)
    w, h = (540, 960) if small else (1080, 1920)
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{w}x{h}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '24' if small else '21',
                          '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for buf in pool.imap(_frame, [(i, small) for i in range(n)], chunksize=4):
            p.stdin.write(buf)
    p.stdin.close()
    p.wait()
    print(f'film: {out} ({DUR:.0f} s, {os.path.getsize(out) / 1e6:.1f} MB)')


def check():
    bad = []
    for i in range(int(DUR * FPS)):
        try:
            render(i / FPS, small=True)
        except Exception as e:                                       # noqa: BLE001
            bad.append(f'{i / FPS:5.2f}s: {e}')
    print('\n'.join(bad) if bad else 'duel: every frame draws cleanly')


def stills(out, times):
    ims = [render(t, small=True).resize((270, 480)) for t in times]
    cols = 8
    sh = Image.new('RGB', (cols * 270, ((len(ims) + cols - 1) // cols) * 480), (0, 0, 0))
    for i, im in enumerate(ims):
        ImageDraw.Draw(im).text((6, 6), f'{times[i]:.1f}', fill=(200, 0, 0))
        sh.paste(im, ((i % cols) * 270, (i // cols) * 480))
    sh.save(out, quality=85)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if cmd == 'check':
        check()
    elif cmd == 'stills':
        stills(sys.argv[2], [float(x) for x in sys.argv[3].split(',')])
    elif cmd == 'film':
        film(sys.argv[2], '--small' in sys.argv)
