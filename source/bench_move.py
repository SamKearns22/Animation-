#!/usr/bin/env python3
"""MAP  bench_move: stage 1 of proposal solid-body-moves (chat 34, Sam's "Y 1"): the lean out of the passenger
window and back as a plain grey solid body, in the test space only (Jason, his seat, the door with the open window,
the windscreen frame, the roof, the bonnet; shot 4's locked camera). Nothing here touches shot 4 or the film.

The body is the measured MakeHuman body (bench_pose: Jason's build) driven straight from GOALS on the car, every
1/24 s, on its OWN skeleton (so a goal met is met by the skin, not by a stand-in skeleton):
  pelvis place and facing, chest facing (the spine bends between the two, bone by bone), head facing,
  knee points on the seat cushion (the pelvis height is solved from them: the knees stay planted),
  hand goals (the free hand's point on the door top; the gun hand along the aim from its own shoulder),
  each limb by two-bone IK with its hinge kept on the bend (no twisted elbows or knees).
Key poses (KEYS) come from the reference sheet notes/bench/l3-reference.jpg (photo A: lean starts, forearm on the
door top; B, C: folded at the waist over the door top, free hand resting on it; D: chest turned back along the car,
the head leading). The beats and their times are shot 4's locked acting rows (leanout.TIMES).

  RIG / rig() ....... the body's rest points (car-handed, metres), triangles, regions, its own joints and lengths
  KEYS, goals_at(t) . the key poses as goals, eased in-betweens (goals, not joints, are blended)
  solve(g) .......... goals -> joints, bone turns, skin points, hand balls, the pistol
  CHECKS ............ car(), self_cross(), pistol(), contacts(), jumps(), ranges(), aim(): the stage-1 bar
  run(OUT) .......... every frame of shot 4 (8.2 s at 24): solve, check, draw grey; writes OUT/frames, report.txt
  proof(OUT) ........ every check first run on old failed frames (pass list, notes/bench/learn-step.md)

    python3 source/bench_move.py run OUT_DIR        the clip's frames + the check table (prints it)
    python3 source/bench_move.py proof OUT_DIR      the checks against the old failed frames
    python3 source/bench_move.py keys OUT.jpg       the key poses from three sides (a sheet)
"""
import math
import os
import sys
import time

import numpy as np
from numba import njit, prange

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bench_pose as BP   # noqa: E402

FPS = 24
MIR = np.array([-1.0, 1, 1])
HAND_R = 26 * 0.00152            # the house circle hand as a ball (bench_draw.hand_balls)
HAND_OFF = 12 * 0.00152
TOUCH = 0.005                    # a body point deeper than this inside a solid is a crossing (touching is not)

# ---------------------------------------------------------------------------------------------------- the rig
RIG = {}
JOINTS = dict(pelvis='spine05', neck='neck01', head='head', shL='upperarm01.L', shR='upperarm01.R',
              elL='lowerarm01.L', elR='lowerarm01.R', wrL='wrist.L', wrR='wrist.R', hipL='upperleg01.L',
              hipR='upperleg01.R', knL='lowerleg01.L', knR='lowerleg01.R', anL='foot.L', anR='foot.R')
MOUTH = None
HAND_BONES = ('wrist', 'finger', 'metacarpal', 'thumb')


def _u(a):
    a = np.asarray(a, float)
    return a / (np.linalg.norm(a) + 1e-12)


def rig():
    if RIG:
        return RIG
    import gta_cast as GC
    import leanout as LO
    v = BP.jason_mesh()
    R = BP._REST
    sk = R['sk']
    sp = dict(GC.cast()['jason'], mood='stern')
    k1 = LO.seated(sp)
    rest_len = np.linalg.norm(sk.rest['neck01'][:3, 3] - sk.rest['spine05'][:3, 3])
    s = np.linalg.norm(np.asarray(k1['neck']) - np.asarray(k1['pelvis'])) / rest_len   # = bench_pose's scale
    o = sk.rest['spine05'][:3, 3]
    V = (v - o) * s * MIR                                          # rest body, metres, car-handed, pelvis at 0
    heads = {b: (sk.rest[b][:3, 3] - o) * s * MIR for b in sk.order}
    J = {n: heads[b] for n, b in JOINTS.items()}
    keep = np.zeros(len(v), bool)
    keep[R['used']] = True
    bone = R['bone']
    hand = np.array([str(b).startswith(HAND_BONES) for b in bone])
    headb = np.array([str(b).startswith(('head', 'jaw', 'eye', 'oculi', 'tongue', 'levator', 'oris', 'orbicularis',
                                         'risorius', 'temporalis', 'special', 'mandible')) for b in bone])
    grp = R['grp'].argmax(1)
    side = np.where(V[:, 0] > 0.02, 1, np.where(V[:, 0] < -0.02, -1, 0))
    region = grp * 3 + np.where(np.isin(grp, (1, 2, 4)), side + 1, 1)      # trunk / arm L,R / leg L,R / head / foot L,R
    tris = R['tris'][:, ::-1]                                       # wound for the mirrored frame
    tk = tris[keep[tris].all(1)]
    global MOUTH
    MOUTH = np.array([str(b).startswith(('oris', 'levator', 'tongue', 'jaw', 'mandible', 'risorius')) for b in bone])
    RIG.update(s=s, V=V, heads=heads, J=J, sk=sk, keep=keep, hand=hand, headb=headb, tris=tris, tk=tk,
               region=region, part=R['part'], bone=bone, sp=sp, k1=k1,
               L_up=np.linalg.norm(J['elR'] - J['shR']), L_fo=np.linalg.norm(J['wrR'] - J['elR']),
               L_th=np.linalg.norm(J['knR'] - J['hipR']), L_sh=np.linalg.norm(J['anR'] - J['knR']))
    # each bone's driver: which frame turns it ('P' pelvis, 'C' chest, 'H' head, spine/neck blends, limbs)
    drv = {}
    for b in sk.order:
        if b in ('root', 'spine05') or b.startswith('pelvis'):
            drv[b] = ('P',)
        elif b in ('spine04', 'spine03', 'spine02'):
            drv[b] = ('PC', {'spine04': 0.3, 'spine03': 0.6, 'spine02': 0.85}[b])
        elif b == 'spine01':
            drv[b] = ('C',)
        elif b in ('neck01', 'neck02', 'neck03'):
            drv[b] = ('CH', {'neck01': 0.3, 'neck02': 0.6, 'neck03': 0.85}[b])
        elif b == 'head':
            drv[b] = ('H',)
        elif b.startswith('upperarm'):
            drv[b] = ('up' + b[-1],)
        elif b.startswith('lowerarm'):
            drv[b] = ('fo' + b[-1],)
        elif b.startswith('upperleg'):
            drv[b] = ('th' + b[-1],)
        elif b.startswith('lowerleg'):
            drv[b] = ('sh' + b[-1],)
    RIG['drv'] = drv
    # rest frames of the limbs: (bone direction, hinge axis)
    rf = {}
    for sd in 'LR':
        du, df = _u(J['el' + sd] - J['sh' + sd]), _u(J['wr' + sd] - J['el' + sd])
        hinge = _u(np.cross(du, df))
        rf['up' + sd], rf['fo' + sd] = (du, hinge), (df, hinge)
        dt, ds = _u(J['kn' + sd] - J['hip' + sd]), _u(J['an' + sd] - J['kn' + sd])
        hl = _u(np.cross(dt, np.array([0, 0, -1.0])))               # the knee bends back: hinge across the body
        rf['th' + sd], rf['sh' + sd] = (dt, hl), (ds, hl)
    RIG['rf'] = rf
    return RIG


def _frame(up, fwd):
    """Rotation taking the rest frame (up +y, front +z, right +x) to (up, fwd)."""
    up = _u(up)
    fwd = _u(np.asarray(fwd, float) - up * np.dot(fwd, up))
    return np.stack([np.cross(up, fwd), up, fwd], 1)


def _map(d0, n0, d1, n1):
    """Rotation taking direction d0 to d1 with axis n0 (across it) to n1."""
    def basis(d, n):
        d = _u(d)
        n = _u(np.asarray(n, float) - d * np.dot(n, d))
        return np.stack([d, n, np.cross(d, n)], 1)
    return basis(d1, n1) @ basis(d0, n0).T


def _slerp(Ra, Rb, u):
    from scipy.spatial.transform import Rotation as Ro, Slerp
    r = Ro.from_matrix(np.stack([Ra, Rb]))
    return Slerp([0, 1], r)([u]).as_matrix()[0]


def _two_bone(root, target, l1, l2, pole):
    """Middle and end joints from root toward target (bones l1, l2), the bend toward pole."""
    root, target = np.asarray(root, float), np.asarray(target, float)
    d = target - root
    dist = np.clip(np.linalg.norm(d), abs(l1 - l2) + 1e-4, l1 + l2 - 1e-4)
    d = _u(d)
    end = root + d * dist
    a = (l1 * l1 + dist * dist - l2 * l2) / (2 * dist)
    h = math.sqrt(max(l1 * l1 - a * a, 0.0))
    p = _u(np.asarray(pole, float) - d * np.dot(pole, d))
    return root + d * a + p * h, end


# ---------------------------------------------------------------------------------------------------- the car
SEAT_TOP, SILL = 0.47, 0.95
DOOR_X = 0.915                   # the door's inner face; its top y 0.95, outer face 0.985


def glass_x(y):
    """The greenhouse's side (the window line) at height y: 0.86 at the sill to 0.70 at the roof."""
    return 0.86 - 0.16 * (np.asarray(y) - 0.95) / 0.52


def solids():
    """The test space's solids, each (name, part, kind, data): boxes (bench_pose.car_window, plus the roof, the
    rear door and the rear side glass) and rods (the windscreen frame, the pillars, the roof's side rail)."""
    S = [(nm, pt, 'box', (np.array(lo), np.array(hi))) for nm, pt, lo, hi in BP.car_window()]
    S.append(('roof', 'body', 'box', (np.array([-0.70, 1.47, -1.80]), np.array([0.70, 1.52, 0.30]))))
    S.append(('rear door R', 'door', 'box', (np.array([0.915, 0.30, -1.85]), np.array([0.985, 0.95, -0.95]))))
    S.append(('rear glass R', 'pillar', 'glass', (-1.80, -0.95)))
    for nm, a, b, r in BP.windscreen_frame():
        S.append((nm, 'pillar', 'rod', (np.array(a), np.array(b), r)))
    S.append(('roof rail R', 'pillar', 'rod', (np.array([0.70, 1.47, 0.30]), np.array([0.70, 1.47, -1.80]), 0.035)))
    return S


def inside_depth(Q, sol):
    """How far each point of Q is inside a solid (metres; <= 0 outside)."""
    nm, pt, kind, d = sol
    if kind == 'box':
        lo, hi = d
        return np.minimum(Q - lo, hi - Q).min(1)
    if kind == 'rod':
        a, b, r = d
        ab = b - a
        u = np.clip(((Q - a) @ ab) / (ab @ ab), 0, 1)
        return r - np.linalg.norm(Q - (a + u[:, None] * ab), axis=1)
    if kind == 'glass':
        z0, z1 = d
        gx = glass_x(Q[:, 1])
        th = 0.008
        dep = np.minimum.reduce([th - np.abs(Q[:, 0] - gx), Q[:, 2] - z0, z1 - Q[:, 2], Q[:, 1] - 0.95, 1.47 - Q[:, 1]])
        return dep
    raise KeyError(kind)


# ---------------------------------------------------------------------------------------------------- the move
def _v(*a):
    return np.array(a, float)


TARGET = _v(0.05, 1.31, -7.68)   # the lead cruiser's windscreen (leanout.TARGET, car frame)
DOOR_HAND = _v(0.955, SILL + HAND_R + 0.002, 0.16)   # the free hand resting on the door top (reference C)


def key(name):
    """A key pose as goals (car frame, metres). Reference letters: notes/bench/l3-reference.jpg."""
    r = rig()
    if name == 'K1':          # seated (shot 3's frame): pistol flat on his chest, left hand on his thigh
        return dict(pelvis=_v(0.42, 0.0, -0.06), p_up=_v(0, 1, -0.12), p_fwd=_v(0, 0, 1), c_up=_v(0, 1, 0.02),
                    c_fwd=_v(0, 0, 1), h_fwd=_v(0, -0.05, 1),
                    hand={'L': (_v(0.28, 0.66, 0.34), _v(-0.3, -0.2, -1)), 'R': (_v(0.40, 0.98, 0.18), _v(0.7, -1, -0.3))},
                    aim_w=0.0, gun=_v(0.85, 0.5, 0.2), kick=0.0, belly=0.0,
                    knee={'L': _v(0.31, 0.64, 0.42), 'R': _v(0.53, 0.64, 0.42)},
                    ankle={'L': _v(0.31, 0.18, 0.50), 'R': _v(0.53, 0.18, 0.50)}, knee_w=0.0, seat_w=1.0)
    if name == 'K2':          # up on his knees, turned to the window, ducking: chest at the window, forearm and
        #                       free hand onto the door top (photo A), the gun held low, muzzle down
        return dict(pelvis=_v(0.56, 0.0, 0.02), p_up=_v(0.45, 1, 0), p_fwd=_v(1, 0, -0.15), c_up=_v(0.9, 1, 0),
                    c_fwd=_v(1, 0, -0.2), h_fwd=_v(1, -0.1, -0.15),
                    hand={'L': (DOOR_HAND, _v(0.3, -1, 0.6)), 'R': (_v(0.74, 0.86, -0.16), _v(0.2, -0.3, -1))},
                    aim_w=0.0, gun=_v(0.3, -1, -0.1), kick=0.0, belly=0.0,
                    knee={'L': _v(0.62, 0.0, 0.14), 'R': _v(0.60, 0.0, -0.12)},
                    ankle={'L': _v(0.20, 0.53, 0.18), 'R': _v(0.18, 0.53, -0.16)}, knee_w=1.0, seat_w=0.0)
    if name == 'K3':          # head and shoulders out over the door top, the head leading the turn back (D),
        #                       gun up beside his head, muzzle up
        return dict(pelvis=_v(0.70, 0.0, 0.01), p_up=_v(0.5, 1, 0), p_fwd=_v(1, 0, -0.25), c_up=_v(0.8, 1, -0.05),
                    c_fwd=_v(1, 0, -0.5), h_fwd=_v(0.5, 0, -1),
                    hand={'L': (DOOR_HAND, _v(0.5, -1, 0.6)), 'R': ('rel', _v(0.06, 0.34, -0.10), _v(0.3, -1, -0.5))},
                    aim_w=0.0, gun=_v(0, 1, -0.1), kick=0.0, belly=0.0,
                    knee={'L': _v(0.63, 0.0, 0.14), 'R': _v(0.61, 0.0, -0.12)},
                    ankle={'L': _v(0.20, 0.53, 0.18), 'R': _v(0.18, 0.53, -0.16)}, knee_w=1.0, seat_w=0.0)
    if name in ('K4', 'K5'):  # out to the waist, folded over the door top (B, C), chest turned back along the car
        #                       (D), the gun arm along the line to the lead cruiser; K5 the kick
        k = dict(pelvis=_v(0.76, 0.0, 0.0), p_up=_v(0.55, 1, 0), p_fwd=_v(1, 0, -0.3), c_up=_v(1.15, 1, -0.05),
                 c_fwd=_v(1, 0, -0.85), h_fwd=_v(-0.05, 0, -1),
                 hand={'L': (DOOR_HAND, _v(0.6, -0.6, 0.8)), 'R': ('aim', None, _v(0.3, -1, 0.2))},
                 aim_w=1.0, gun=None,
                 knee={'L': _v(0.64, 0.0, 0.14), 'R': _v(0.62, 0.0, -0.12)},
                 ankle={'L': _v(0.20, 0.53, 0.18), 'R': _v(0.18, 0.53, -0.16)}, knee_w=1.0, seat_w=0.0)
        k['kick'] = 1.0 if name == 'K5' else 0.0
        k['belly'] = 1.0
        return k
    raise KeyError(name)


KICK_DEG = 7.0                   # the pistol's kick: the forearm flips up this much (a real one-hand kick)


def _times():
    import leanout as LO
    return LO.TIMES


def _ease(u):
    return u * u * (3 - 2 * u)


def _lerp_goal(a, b, u):
    out = {}
    for n in a:
        x, y = a[n], b[n]
        if isinstance(x, dict):
            out[n] = {}
            for s in x:
                xa, xb = x[s], y[s]
                if isinstance(xa, tuple):
                    out[n][s] = ('mix', xa, xb, u)
                else:
                    out[n][s] = xa + (xb - xa) * u
        elif x is None or y is None:
            out[n] = x if u < 0.5 else y
            if n == 'gun':
                out[n] = ('mix', x, y, u)
        else:
            out[n] = np.asarray(x, float) + (np.asarray(y, float) - np.asarray(x, float)) * u
    return out


_KEYC = {}


def goals_at(t):
    T = _times()
    t = min(max(t, T[0][0]), T[-1][0])
    for (t0, a), (t1, b) in zip(T, T[1:]):
        if t0 <= t <= t1:
            u = 0.0 if t1 == t0 else _ease((t - t0) / (t1 - t0))
            ka = _KEYC.setdefault(a, key(a))
            kb = _KEYC.setdefault(b, key(b))
            return _lerp_goal(ka, kb, u)
    return key(T[-1][1])


# ---------------------------------------------------------------------------------------------------- solve
def _fk(Rw, root_pos):
    r = rig()
    sk, heads = r['sk'], r['heads']
    Mx = {}
    for b in sk.order:
        p = sk.bones[b]['parent']
        h = heads[b]
        if not p:
            Mx[b] = (Rw[b], root_pos - Rw[b] @ heads['spine05'])   # the pelvis point goes to root_pos
            continue
        Rp, tp = Mx[p]
        Mx[b] = (Rw[b], Rp @ h + tp - Rw[b] @ h)
    return Mx


def _world_rots(Rd):
    """Each bone's world turn: its driver's, or its parent's."""
    r = rig()
    sk, drv = r['sk'], r['drv']
    Rw = {}
    for b in sk.order:
        p = sk.bones[b]['parent']
        d = drv.get(b)
        if d is None:
            Rw[b] = Rw[p] if p else np.eye(3)
        elif d[0] == 'PC':
            Rw[b] = _slerp(Rd['P'], Rd['C'], d[1])
        elif d[0] == 'CH':
            Rw[b] = _slerp(Rd['C'], Rd['H'], d[1])
        else:
            Rw[b] = Rd.get(d[0], Rw[p] if p else np.eye(3))
    return Rw


def _hand_goal(spec, sh, chest_R, aim_dir, l_reach):
    if isinstance(spec, tuple) and spec and isinstance(spec[0], str):
        if spec[0] == 'mix':
            _, a, b, u = spec
            ta, pa = _hand_goal(a, sh, chest_R, aim_dir, l_reach)
            tb, pb = _hand_goal(b, sh, chest_R, aim_dir, l_reach)
            return ta + (tb - ta) * u, pa + (pb - pa) * u
        if spec[0] == 'rel':
            return sh + chest_R @ spec[1] * np.array([1, 1, 1]), spec[2]
        if spec[0] == 'aim':
            return sh + aim_dir * l_reach, spec[2]
    return np.asarray(spec[0], float), np.asarray(spec[1], float)


class Pose(dict):
    """Joint points (car frame) + .aim (the pistol's way) + .fwd for bench_draw.gun_mesh."""


def solve(g, seat_dy=None):
    """Goals -> the posed body: dict(P points, J joints, R bone turns, balls, gun (points, tris), aim)."""
    r = rig()
    J0 = r['J']
    Rp = _frame(g['p_up'], g['p_fwd'])
    Rc = _frame(g['c_up'], g['c_fwd'])
    hup = _u(0.45 * _u(g['c_up']) + 0.55 * np.array([0, 1.0, 0]))
    Rh = _frame(hup, g['h_fwd'])
    pel = np.array(g['pelvis'], float)
    # the pelvis's height: on the seat (its lowest skin on the cushion), or from the knees on the cushion
    hipoff = {sd: Rp @ J0['hip' + sd] for sd in 'LR'}
    y_knee = []
    for sd in 'LR':
        kg = g['knee'][sd].copy()
        kg[1] = SEAT_TOP + KNEE_R
        hxz = pel + hipoff[sd]
        dxz = np.hypot(hxz[0] - kg[0], hxz[2] - kg[2])
        y_knee.append(kg[1] + math.sqrt(max(r['L_th'] ** 2 - dxz ** 2, 0.0)) - hipoff[sd][1])
    y_seat = SEAT_Y if seat_dy is None else seat_dy
    w = float(np.clip(g['knee_w'], 0, 1))
    pel[1] = (1 - w) * y_seat + w * float(np.mean(y_knee))
    Rd = {'P': Rp, 'C': Rc, 'H': Rh}
    Rw = _world_rots(Rd)
    Mx = _fk(Rw, pel)
    heads = r['heads']
    jw = {n: Mx[b][0] @ heads[b] + Mx[b][1] for n, b in JOINTS.items()}
    # the pistol's way: aimed at the target (plus the kick), or the key's own way
    aim_dir = _u(TARGET - jw['shR'])
    kick = float(g.get('kick', 0.0))
    if kick:
        ax = _u(np.cross(aim_dir, [0, 1, 0]))
        from scipy.spatial.transform import Rotation as Ro
        aim_dir = Ro.from_rotvec(-ax * math.radians(KICK_DEG) * kick).apply(aim_dir)
        if aim_dir[1] < _u(TARGET - jw['shR'])[1]:
            aim_dir = Ro.from_rotvec(ax * math.radians(KICK_DEG) * kick).apply(_u(TARGET - jw['shR']))
    reach = (r['L_up'] + r['L_fo']) * 0.975
    for sd in 'LR':
        tgt, pole = _hand_goal(g['hand'][sd], jw['sh' + sd], Rc, aim_dir, reach)
        # the hand goal is the BALL's centre: the wrist sits HAND_OFF back along the forearm
        el, wr = _two_bone(jw['sh' + sd], tgt, r['L_up'], r['L_fo'] + HAND_OFF, pole)
        wr = el + _u(wr - el) * r['L_fo']
        du, df = _u(el - jw['sh' + sd]), _u(wr - el)
        hn = np.cross(du, df)
        if np.linalg.norm(hn) < 1e-3:
            hn = np.cross(_u(np.asarray(pole) - du * np.dot(pole, du)), du)
        hn = _u(hn)
        Rd['up' + sd] = _map(*r['rf']['up' + sd], du, hn)
        Rd['fo' + sd] = _map(*r['rf']['fo' + sd], df, hn)
    for sd in 'LR':
        hip = jw['hip' + sd]
        kg = np.asarray(g['knee'][sd], float).copy()
        ky = SEAT_TOP + KNEE_R
        kg[1] = kg[1] * (1 - w) + ky * w
        if w > 0:                                                   # kneeling: the knee ON the cushion, at the
            dxz = _v(kg[0] - hip[0], 0, kg[2] - hip[2])            # thigh's length from the hip (slid along the
            want = math.sqrt(max(r['L_th'] ** 2 - (hip[1] - kg[1]) ** 2, 1e-6))   # line from the hip)
            kk = hip + _u(dxz) * want
            kk[1] = kg[1]
            kg = kg * (1 - w) + kk * w
        dt = _u(kg - hip)
        kn = hip + dt * r['L_th']
        ds = _u(np.asarray(g['ankle'][sd], float) - kn)
        hn = np.cross(dt, ds)
        if np.linalg.norm(hn) < 1e-3:
            hn = np.cross(dt, -_u(np.asarray(g['p_fwd'], float)))
        hn = _u(hn)
        Rd['th' + sd] = _map(*r['rf']['th' + sd], dt, hn)
        Rd['sh' + sd] = _map(*r['rf']['sh' + sd], ds, hn)
    Rw = _world_rots(Rd)
    Mx = _fk(Rw, pel)
    jw = {n: Mx[b][0] @ heads[b] + Mx[b][1] for n, b in JOINTS.items()}
    # skin
    V = r['V']
    acc = np.zeros_like(V)
    ws = np.zeros(len(V))
    for b, (idx, wt) in r['sk'].weights.items():
        R_, t_ = Mx[b]
        acc[idx] += wt[:, None] * (V[idx] @ R_.T + t_)
        ws[idx] += wt
    ws[ws < 1e-9] = 1
    P = acc / ws[:, None]
    balls = {sd: jw['wr' + sd] + _u(jw['wr' + sd] - jw['el' + sd]) * HAND_OFF for sd in 'LR'}
    gun_way = g['gun']
    if isinstance(gun_way, tuple):
        _, a, b, u = gun_way
        a = aim_dir if a is None else _u(a)
        b = aim_dir if b is None else _u(b)
        gun_way = _u(a + (b - a) * u)
    elif gun_way is None:
        gun_way = aim_dir
    pose = Pose({n: v for n, v in jw.items()})
    pose['fwd'] = Rc[:, 2]
    pose.aim = _u(gun_way)
    import bench_draw as BD
    Pg, Tg = BD.gun_mesh(pose)
    return dict(P=P, J=jw, balls=balls, gun=(Pg, Tg), aim=pose.aim, pel=pel, Rc=Rc, Rp=Rp, Rh=Rh, pose=pose)


KNEE_R = 0.055                   # the knee's skin below its joint when kneeling (measured: _fit_knee)
SEAT_Y = 0.60                    # the seated pelvis height (solved by fit_seat: his seat on the cushion)


def fit_seat():
    """The seated pelvis height that puts his lowest seat skin on the cushion (touching, not in)."""
    global SEAT_Y
    r = rig()
    k = key('K1')
    for _ in range(6):
        out = solve(k)
        P = out['P'][r['keep']]
        seat = [s for s in solids() if s[0] == 'seat R'][0]
        dep = inside_depth(P, seat)
        lo, hi = seat[3]
        over = (P[:, 0] > lo[0]) & (P[:, 0] < hi[0]) & (P[:, 2] > lo[2]) & (P[:, 2] < hi[2])
        gap = (P[over, 1] - hi[1]).min() if over.any() else 0.0
        SEAT_Y -= gap - 0.001
        if abs(gap - 0.001) < 0.0005:
            break
    return SEAT_Y


def fit_knee():
    """KNEE_R: the knee skin's depth below the knee joint when kneeling (so the knees rest ON the cushion)."""
    global KNEE_R
    r = rig()
    for _ in range(5):
        out = solve(key('K4'))
        P = out['P']
        leg = np.isin(r['region'], (6, 8)) & r['keep']
        seat = [s for s in solids() if s[0] == 'seat R'][0]
        lo, hi = seat[3]
        Q = P[leg]
        over = (Q[:, 0] > lo[0]) & (Q[:, 0] < hi[0]) & (Q[:, 2] > lo[2]) & (Q[:, 2] < hi[2])
        gap = (Q[over, 1] - hi[1]).min()
        KNEE_R -= gap - 0.001
        if abs(gap - 0.001) < 0.0005:
            break
    return KNEE_R


# ---------------------------------------------------------------------------------------------------- checks
@njit(parallel=True, cache=True)
def _winding(Q, V, T):
    out = np.zeros(len(Q))
    for i in prange(len(Q)):
        q = Q[i]
        s = 0.0
        for t in range(len(T)):
            a = V[T[t, 0]] - q
            b = V[T[t, 1]] - q
            c = V[T[t, 2]] - q
            la = math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])
            lb = math.sqrt(b[0] * b[0] + b[1] * b[1] + b[2] * b[2])
            lc = math.sqrt(c[0] * c[0] + c[1] * c[1] + c[2] * c[2])
            det = (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
                   + a[2] * (b[0] * c[1] - b[1] * c[0]))
            den = (la * lb * lc + (a[0] * b[0] + a[1] * b[1] + a[2] * b[2]) * lc
                   + (b[0] * c[0] + b[1] * c[1] + b[2] * c[2]) * la + (c[0] * a[0] + c[1] * a[1] + c[2] * a[2]) * lb)
            s += 2.0 * math.atan2(det, den)
        out[i] = s / (4.0 * math.pi)
    return out


def _body_tris():
    """The body's closed skin for inside tests: the kept triangles, the 3D hands left out (circle hands stand in)."""
    r = rig()
    if 'tb' not in r:
        tk = r['tk']
        r['tb'] = tk[~r['hand'][tk].any(1)]
    return r['tb']


def _wsign():
    """The winding number's sign for 'inside' on this mesh (its triangles' handedness)."""
    r = rig()
    if 'wsg' not in r:
        V = r['V']
        c = V[r['keep'] & (r['region'] == 1)].mean(0)
        w = _winding(c[None, :], V, _body_tris())[0]
        r['wsg'] = 1.0 if w > 0 else -1.0
    return r['wsg']


def car(out):
    """Body (skin, hand balls) points inside the car's solids: {solid: (points, deepest cm)} past TOUCH."""
    r = rig()
    P = out['P'][r['keep'] & ~r['hand']]
    hits = {}
    ball_pts = [_sphere(c, HAND_R) for c in out['balls'].values()]
    Q = np.concatenate([P] + ball_pts)
    for sol in solids():
        d = inside_depth(Q, sol)
        m = d > TOUCH
        if m.any():
            hits[sol[0]] = (int(m.sum()), round(float(d[m].max()) * 100, 1))
    return hits


def _sphere(c, rad, n=60):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    th = math.pi * (1 + 5 ** 0.5) * i
    return np.asarray(c) + rad * np.stack([np.cos(th) * np.sin(phi), np.cos(phi), np.sin(th) * np.sin(phi)], 1)


REG_NAMES = {1: 'trunk', 3: 'arm L', 5: 'arm R', 6: 'leg L', 8: 'leg R', 10: 'head', 12: 'foot L', 14: 'foot R'}


def _normals(P, tb):
    import mesh_sdf as MS
    N = MS.vertex_normals(P, tb)
    N = N / (np.linalg.norm(N, axis=1, keepdims=True) + 1e-12)
    use = np.unique(tb)
    if np.median(np.einsum('ij,ij->i', P[use] - P[use].mean(0), N[use])) < 0:
        N = -N
    return N


def self_cross(out):
    """Body against itself: skin points of one part (arm, leg, trunk, head, foot; each side apart) that lie inside
    the body's closed skin (winding number over 0.75 at a skin point means inside ANOTHER part: a free skin point
    reads 0.5), deeper than TOUCH from the other part's nearest skin. The hand balls inside the body count too
    (the gun hand's ball holding the grip is the grip, not a crossing). {pair: (points, deepest cm)}"""
    from scipy.spatial import cKDTree
    r = rig()
    P = out['P']
    tb = _body_tris()
    use = np.unique(tb)
    reg = r['region'][use]
    Q = P[use]
    tree = cKDTree(Q)
    # each skin point's nearest skin point of ANOTHER part (distance, which part)
    near = np.full(len(Q), np.inf)
    near_reg = np.zeros(len(Q), int)
    for rg in np.unique(reg):
        m = reg == rg
        d, _ = cKDTree(Q[m]).query(Q[~m], distance_upper_bound=0.12)
        idx = np.where(~m)[0]
        better = d < near[idx]
        near[idx[better]] = d[better]
        near_reg[idx[better]] = rg
    cand = np.where((near < 0.12) & ~MOUTH[use])[0]                 # (the lips' inside is inside by design)
    hits = {}
    if len(cand):
        N = _normals(P, tb)[use]
        wn = _winding(Q[cand] + N[cand] * 0.003, P, tb) * _wsign()   # 3 mm out along its own skin: a free
        for i in cand[wn > 0.5]:                                        # skin point is then outside (0)
            dep = float(near[i])
            if dep <= TOUCH:
                continue
            nm = ' / '.join(sorted({REG_NAMES.get(reg[i], 'body'), REG_NAMES.get(near_reg[i], 'body')}))
            n0, d0 = hits.get(nm, (0, 0.0))
            hits[nm] = (n0 + 1, max(d0, round(dep * 100, 1)))
    for sd, c in out['balls'].items():
        S = _sphere(c, HAND_R * 0.98)
        wn = _winding(S, P, tb) * _wsign()
        m = wn > 0.5
        if m.any():
            dist, _ = tree.query(S[m])
            dep = dist.max()
            if dep > TOUCH:
                hits['hand %s in body' % sd] = (int(m.sum()), round(float(dep) * 100, 1))
    return hits


def pistol(out):
    """The pistol's points inside the body (past TOUCH), but not those inside the gun hand's ball (the grip)."""
    from scipy.spatial import cKDTree
    r = rig()
    Pg, _ = out['gun']
    tb = _body_tris()
    wn = _winding(Pg, out['P'], tb) * _wsign()
    m = wn > 0.5
    m &= np.linalg.norm(Pg - out['balls']['R'], axis=1) > HAND_R
    if not m.any():
        return {}
    tree = cKDTree(out['P'][np.unique(tb)])
    dist, _ = tree.query(Pg[m])
    dep = dist.max()
    return {'pistol in body': (int(m.sum()), round(float(dep) * 100, 1))} if dep > TOUCH else {}


def gun_car(out):
    Pg, _ = out['gun']
    hits = {}
    for sol in solids():
        d = inside_depth(Pg, sol)
        m = d > TOUCH
        if m.any():
            hits['pistol in ' + sol[0]] = (int(m.sum()), round(float(d[m].max()) * 100, 1))
    return hits


def contact_state(out, g):
    """The planted contacts this frame: name -> (held?, gap cm). Knees on the cushion (kneeling), the free hand's
    ball on the door top, the belly / hips against the door top (out to the waist)."""
    r = rig()
    res = {}
    if g['knee_w'] >= 0.999:
        for sd in 'LR':
            leg = r['keep'] & (r['region'] == (6 if sd == 'L' else 8))
            Q = out['P'][leg]
            kn = out['J']['kn' + sd]
            near = np.linalg.norm(Q - kn, axis=1) < 0.12
            gap = Q[near, 1].min() - SEAT_TOP
            res['knee %s on seat' % sd] = round(gap * 100, 1)
    hs = g['hand']['L']
    planted = isinstance(hs, tuple) and len(hs) == 2 and not isinstance(hs[0], str) and \
        np.allclose(np.asarray(hs[0], float), DOOR_HAND)
    if planted:
        c = out['balls']['L']
        res['free hand on door top'] = round((c[1] - HAND_R - SILL) * 100, 1)
    if g.get('belly', 0) >= 0.999:
        trunk = r['keep'] & (r['region'] == 1)
        Q = out['P'][trunk]
        near = (np.abs(Q[:, 1] - SILL) < 0.06) & (Q[:, 2] > -0.95) & (Q[:, 2] < 0.80)
        gap = DOOR_X - Q[near, 0].max() if near.any() else 9.0
        res['belly on door top'] = round(gap * 100, 1)
    return res


ROM = dict(elbow=(0, 150), knee=(0, 160), spine_twist=(-50, 50), neck_turn=(-80, 80), spine_bend=(0, 70))


def ranges(out):
    """Joints within a person's range: elbow and knee bend, the spine's twist and bend, the neck's turn."""
    J = out['J']
    bad = {}
    for sd in 'LR':
        a = math.degrees(math.acos(np.clip(np.dot(_u(J['el' + sd] - J['sh' + sd]), _u(J['wr' + sd] - J['el' + sd])), -1, 1)))
        if not ROM['elbow'][0] <= a <= ROM['elbow'][1]:
            bad['elbow ' + sd] = round(a)
        a = math.degrees(math.acos(np.clip(np.dot(_u(J['kn' + sd] - J['hip' + sd]), _u(J['an' + sd] - J['kn' + sd])), -1, 1)))
        if not ROM['knee'][0] <= a <= ROM['knee'][1]:
            bad['knee ' + sd] = round(a)
    Rp, Rc, Rh = out['Rp'], out['Rc'], out['Rh']
    def yaw(Ra, Rb):            # turn of b's front about a's up, seen in a's frame
        f = Ra.T @ Rb[:, 2]
        return math.degrees(math.atan2(f[0], f[2]))
    tw = yaw(Rp, Rc)
    if not ROM['spine_twist'][0] <= tw <= ROM['spine_twist'][1]:
        bad['spine twist'] = round(tw)
    nt = yaw(Rc, Rh)
    if not ROM['neck_turn'][0] <= nt <= ROM['neck_turn'][1]:
        bad['neck turn'] = round(nt)
    bend = math.degrees(math.acos(np.clip(np.dot(Rp[:, 1], Rc[:, 1]), -1, 1)))
    if bend > ROM['spine_bend'][1]:
        bad['spine bend'] = round(bend)
    return bad, dict(twist=round(tw), neck=round(nt), bend=round(bend))


def aim_err(out):
    """How far the barrel's line passes from the lead cruiser's windscreen (metres)."""
    Pg, _ = out['gun']
    c = out['balls']['R']
    d = out['aim']
    v = TARGET - c
    return float(np.linalg.norm(v - d * np.dot(v, d))) if np.dot(v, d) > 0 else 99.0


TRACK = ('pelvis', 'neck', 'head', 'shL', 'shR', 'elL', 'elR', 'wrL', 'wrR', 'hipL', 'hipR', 'knL', 'knR', 'anL',
         'anR')


def jumps(track, fps=FPS):
    """track: [frame] -> {joint: point}. Returns the largest step a frame per joint (cm), the frames over 3 cm,
    and the pops: a step more than 3 cm off the smooth path through its neighbours (a jump, not speed)."""
    over, pops, top = [], [], {}
    for n in TRACK:
        p = np.array([f[n] for f in track])
        st = np.linalg.norm(np.diff(p, axis=0), axis=1)
        top[n] = round(float(st.max()) * 100, 1)
        for i in np.where(st > 0.03)[0]:
            over.append((i + 1, n, round(float(st[i]) * 100, 1)))
        acc = np.linalg.norm(p[2:] - 2 * p[1:-1] + p[:-2], axis=1)
        for i in np.where(acc > 0.03)[0]:
            pops.append((i + 1, n, round(float(acc[i]) * 100, 1)))
    return top, over, pops


def contacts_held(rows):
    """rows: [(frame, {contact: gap cm})]. A contact is held while it lasts if its gap stays within 1 cm
    (resting, not floating, not sunk) and the planted point does not slide (the door hand and knees: under 1 cm)."""
    bad = []
    for f, cs in rows:
        for nm, gap in cs.items():
            if gap > 1.0 or gap < -TOUCH * 100:
                bad.append((f, nm, gap))
    return bad


def slides(track, rows):
    """The planted points' slide while planted: the door hand's ball and each knee (cm, largest)."""
    out = {}
    for nm, jn in (('free hand on door top', 'wrL'), ('knee L on seat', 'knL'), ('knee R on seat', 'knR')):
        fr = [f for f, cs in rows if nm in cs]
        if len(fr) < 2:
            continue
        pts = np.array([track[f][jn] for f in fr])
        segs = np.split(np.arange(len(fr)), np.where(np.diff(fr) > 1)[0] + 1)
        mx = 0.0
        for s in segs:
            if len(s) > 1:
                mx = max(mx, float(np.linalg.norm(pts[s] - pts[s[0]], axis=1).max()))
        out[nm] = round(mx * 100, 1)
    return out


def check_frame(out, g):
    hits = car(out)
    hits.update(gun_car(out))
    sc = self_cross(out)
    pi = pistol(out)
    rb, rv = ranges(out)
    return dict(car=hits, self=sc, pistol=pi, contacts=contact_state(out, g), rom=rb, romv=rv)


# ---------------------------------------------------------------------------------------------------- drawing
GREY = dict(skin=(176, 176, 176), vest=(176, 176, 176), trousers=(176, 176, 176), shoes=(176, 176, 176),
            hair=(176, 176, 176), door=(214, 120, 112), body=(214, 120, 112), dash=(120, 112, 110),
            seat=(150, 128, 112), pillar=(70, 70, 76), gun=(40, 40, 44), hand=(176, 176, 176))
SKY = (232, 236, 240)


def cam_at(t, shake=True):
    import gta_rehearse as GR
    import sets as S
    pos, at, focal = GR._key(t)
    sh = (0.0, 0.0)
    if shake:
        rng = np.random.RandomState(int(t * 24))
        sh = [rng.uniform(-2.5, 2.5), rng.uniform(-2.0, 2.0)]
        for ts in GR.SHOTS:
            w = t - ts
            if 0 <= w < 0.16:
                sh[0] += 7 * (1 - w / 0.16) * (1 if int(ts * 100) % 2 else -1)
                sh[1] += 9 * (1 - w / 0.16)
    return S.Cam(pos, at, focal, shake=tuple(sh))


def scene(out):
    import bench_draw as BD
    r = rig()
    tk = r['tk']
    tk = tk[~r['hand'][tk].any(1)]
    objs = [(out['P'], tk, np.array(['skin'] * len(tk)), 'jason')]
    for nm, pt, kind, d in solids():
        if kind == 'box':
            Pb, Tb = BD._box(*d)
        elif kind == 'rod':
            Pb, Tb = BD._rod(d[0], d[1], d[2])
        else:
            continue                                               # the closed rear glass: clear
        objs.append((Pb, Tb, np.array([pt] * len(Tb)), nm))
    for sd, c in out['balls'].items():
        Pb, Tb = BD._ball(c, HAND_R)
        objs.append((Pb, Tb, np.array(['hand'] * len(Tb)), 'hand' + sd))
    Pg, Tg = out['gun']
    objs.append((Pg, Tg, np.array(['gun'] * len(Tg)), 'gun'))
    return objs


def draw(out, cam, size=(540, 960)):
    """The grey figure in the test space through cam: one pass, depth per dot, house-width ink lines."""
    import bench_draw as BD
    from PIL import Image
    objs = scene(out)
    zb, pb, ob, names = BD.raster(cam, objs, 1)
    edge = BD.ink(zb, pb, ob, 3)
    img = np.zeros(zb.shape + (3,), np.uint8)
    img[:] = SKY
    for i, n in enumerate(BD.PART_NAMES):
        img[pb == i] = GREY[n]
    img[edge] = BD.INK
    return Image.fromarray(img).resize(size, Image.LANCZOS)


# ---------------------------------------------------------------------------------------------------- run
def frame_times():
    T = _times()
    n = int(round(T[-1][0] * FPS)) + 1
    return [i / FPS for i in range(n)]


def run(out_dir, draw_frames=True, every=1):
    os.makedirs(os.path.join(out_dir, 'frames'), exist_ok=True)
    fit_seat()
    fit_knee()
    rows, track, fails = [], [], []
    aims = []
    t0 = time.time()
    ts = frame_times()
    for i, t in enumerate(ts):
        g = goals_at(t)
        out = solve(g)
        c = check_frame(out, g)
        rows.append((i, c['contacts']))
        track.append(out['J'])
        firing = g.get('aim_w', 0) >= 0.999
        if firing:
            aims.append((i, aim_err(out)))
        bad = {k: v for k, v in c.items() if k in ('car', 'self', 'pistol', 'rom') and v}
        if bad:
            fails.append((i, round(t, 3), bad))
        if draw_frames and i % every == 0:
            draw(out, cam_at(t)).save(os.path.join(out_dir, 'frames', 'f%04d.png' % i))
    top, over, pops = jumps(track)
    held = contacts_held(rows)
    sl = slides(track, rows)
    rep = report(len(ts), fails, top, over, pops, held, sl, aims, time.time() - t0)
    open(os.path.join(out_dir, 'report.txt'), 'w').write(rep)
    print(rep)
    return fails, over, pops, held, sl


def report(n, fails, top, over, pops, held, sl, aims, secs):
    L = ['Stage 1 bench results (bench_move.py run): %d frames at 1/24 s, %.0f s' % (n, secs)]
    cats = {'car': 'body-car crossings', 'self': 'body against itself', 'pistol': 'body-pistol', 'rom': 'joint range'}
    for k, nm in cats.items():
        fr = [(i, b[k]) for i, t, b in fails if k in b]
        L.append('%-22s %s' % (nm + ':', 'frames 0' if not fr else '%d frames, e.g. %s' % (len(fr), fr[:3])))
    L.append('%-22s %s' % ('sudden jumps (pops):', 'none' if not pops else '%d, e.g. %s' % (len(pops), pops[:4])))
    L.append('%-22s %d steps (fastest a frame: %s)' % ('steps over 3 cm:', len(over),
                                                     ', '.join('%s %s' % (k, v) for k, v in sorted(top.items(), key=lambda x: -x[1])[:4])))
    L.append('%-22s %s' % ('contacts held:', 'yes' if not held else '%d frames off, e.g. %s' % (len(held), held[:3])))
    L.append('%-22s %s' % ('planted slide (cm):', sl))
    if aims:
        e = [a for _, a in aims]
        L.append('%-22s worst %.2f m off the cruiser windscreen while aimed (%d frames)' % ('aim:', max(e), len(e)))
    return '\n'.join(L)


def clip(out_dir, mp4):
    import subprocess
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(out_dir, 'frames', 'f%04d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '23', '-movflags', '+faststart', mp4], check=True)
    return os.path.getsize(mp4)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'run':
        run(sys.argv[2])
    elif cmd == 'checks':
        run(sys.argv[2], draw_frames=False)
