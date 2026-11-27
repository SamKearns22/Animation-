#!/usr/bin/env python3
"""MAP  bench_move: stage 1 of proposal solid-body-moves (chat 34, Sam's "Y 1"): the lean out of the passenger
window and back as a plain grey solid body, in the test space only (Jason, his seat, the door with the open window,
the windscreen frame, the roof, the bonnet; shot 4's locked camera). Nothing here touches shot 4 or the film.

PARTS: one module in 4 files (cost-spike fix 5c; parts.py runs them inside bench_move, so setters reach all):
  bench_move_b.py (solve); bench_move_c.py (checks); bench_move_d.py (run). Import bench_move, never a part; touch.py
  NAME gives the file and line.

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
  run(OUT) .......... every frame of shot 4 (10.25 s at 24, Sam's 25% slower): solve and check ALL first, then draw grey (draw_all:
                      from the frame store, only changed frames drawn, 4 at a time); writes OUT/frames, report.txt
  checked_clip ...... the clip for Sam: checks first; NOTHING drawn while a fault is neither fixed nor named
  dressed_draw ...... stage 2 (chat 44): a solved pose in the house look (part_at colours, ink, house head, neck
                      column); dressed_still and the --dressed clip both use it
  frame store ....... frame_key (body points + camera + drawing code), spot check of 10, keep -> notes/bench/store
  inside test ....... _winding: counted ray crossings on the capped skin (exact); _winding_sum: the old referee
  proof(OUT) ........ every check first run on old failed frames (pass list, notes/bench/learn-step.md)

    python3 source/bench_move.py run OUT_DIR        the clip's frames + the check table (prints it)
    python3 source/bench_move.py clip OUT_DIR OUT.mp4 [T0 T1]   checks first, then the side-by-side grey clip
    python3 source/bench_move.py clip OUT_DIR OUT.mp4 [T0 T1] --dressed   the same in the house look
    python3 source/bench_move.py dressed OUT.png [KEY] [T]   one key pose dressed (shot camera + outside)
    python3 source/bench_move.py name OUT_DIR "why"   name the last check pass's faults (lets the clip draw)
    python3 source/bench_move.py keep OUT_DIR       file the frame store on GitHub (notes/bench/store/frames.tar)
    python3 source/bench_move.py proof OUT_DIR      the checks against the old failed frames
    python3 source/bench_move.py keys OUT.jpg       the key poses from three sides (a sheet)
"""
import hashlib
import json
import math
import os
import sys
import time

import numpy as np
from numba import njit, prange
from PIL import Image

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


# Sam, 23 Nov (chat 46): "Jason has lost a lot of his bulk in the new version ... he's a muscled guy" (the game art:
# broad shoulders, thick arms, deep chest). MakeHuman's own muscle and weight sliders move the shoulders only 3-4%,
# so the skin is filled out round the house skeleton (the joints, the poses and the clothes' regions are unchanged):
# the arms grow round their bones, the chest gains depth and the shoulders width. Blended by each point's arm weight,
# so the armpit and shoulder joins stay smooth.
FACE_IN = float(os.environ.get('BULK_FI', 1.0))
BULK = dict(upper=float(os.environ.get('BULK_UP', 1.5)), fore=float(os.environ.get('BULK_FO', 1.2)),
            chest_w=float(os.environ.get('BULK_CW', 1.06)), chest_d=float(os.environ.get('BULK_CD', 1.06)))


def _seg_closest(P, a, b):
    ab = b - a
    u = np.clip(((P - a) @ ab) / (ab @ ab), 0, 1)
    return a + u[:, None] * ab


def bulk(V, J, R):
    """The rest skin filled out to Jason's build (BULK): arms round their bones, chest depth and shoulder width."""
    V = V.copy()
    bone = R['bone']
    w_arm = R['grp'][:, 1]
    for sd, S_ in (('L', '.L'), ('R', '.R')):
        for pre, (a, b), f in (('upperarm', ('sh', 'el'), BULK['upper']), ('lowerarm', ('el', 'wr'), BULK['fore'])):
            m = np.array([str(x).startswith(pre) and str(x).endswith(S_) for x in bone])
            if not m.any():
                continue
            A_, B_ = J[a + sd], J[b + sd]
            ab = B_ - A_
            u = np.clip(((V[m] - A_) @ ab) / (ab @ ab), 0, 1)
            c = A_ + u[:, None] * ab
            # the muscle swells mid-bone (biceps, forearm), not at the joint: from the armpit in, the bigger arm
            # pressed 12 cm into the chest (self check, chat 46)
            tap = np.clip(u / 0.35, 0, 1) * np.clip((1 - u) / 0.2, 0, 1) if pre == 'upperarm' else np.clip((1 - u) / 0.35, 0, 1)
            tap = tap * tap * (3 - 2 * tap)
            # the side facing the trunk stays (the arm grows outward, away from the chest)
            out_ = V[m] - c
            side_ = np.sign(A_[0]) if abs(A_[0]) > 1e-6 else 1.0
            face_in = np.clip(-(out_[:, 0] * side_) / (np.linalg.norm(out_, axis=1) + 1e-9), 0, 1)
            k = 1 + (f - 1) * np.clip(w_arm[m], 0, 1) * tap * (1 - FACE_IN * face_in)
            V[m] = c + (V[m] - c) * k[:, None]
    # the trunk from the waist up: wider at the shoulders, deeper at the chest (pelvis at y 0, neck at J['neck'])
    yn = float(J['neck'][1])
    tr = R['grp'][:, 0] > 0.5
    up = np.clip((V[:, 1] - 0.25 * yn) / (0.6 * yn), 0, 1)
    up = up * up * (3 - 2 * up) * tr * (V[:, 1] < yn + 0.02)
    V[:, 0] *= 1 + (BULK['chest_w'] - 1) * up
    zc = 0.0
    V[:, 2] = zc + (V[:, 2] - zc) * (1 + (BULK['chest_d'] - 1) * up)
    return V


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
    V = bulk(V, J, R)
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


KNEES = {'L': _v(0.60, 0.525, 0.14), 'R': _v(0.60, 0.525, -0.12)}   # kneeling K2-K4: planted, the same spots
TARGET = _v(0.05, 1.31, -7.68)   # the lead cruiser's windscreen (leanout.TARGET, car frame)
DOOR_HAND = _v(0.955, SILL + HAND_R + 0.002, 0.16)   # the free hand resting on the door top (reference C)


def key(name):
    """A key pose as goals (car frame, metres). Reference letters: notes/bench/l3-reference.jpg."""
    k = _key(name)
    k.setdefault('leg_ik', 0.0)
    k.setdefault('lift', 0.0)                   # chat 41: the hips lifted off the cushion (metres), seated keys
    k.setdefault('plant', {sd: float(k['knee_w']) for sd in 'LR'})   # chat 41: ONE knee planted on its spot
    k.setdefault('lik_R', k['leg_ik'])   # chat 41 (this account's trials, notes/bench/getup41): the right leg's own foot-led share
    return k


def _key(name):
    r = rig()
    if name == 'K1':          # seated (shot 3's frame): pistol flat on his chest, left hand on his thigh
        return dict(pelvis=_v(0.42, 0.0, -0.06), p_up=_v(0, 1, -0.12), p_fwd=_v(0, 0, 1), c_up=_v(0, 1, 0.02),
                    c_fwd=_v(0, 0, 1), h_fwd=_v(0, -0.05, 1),
                    hand={'L': (_v(0.26, 0.72, 0.36), _v(-1, -0.6, -0.2)), 'R': (_v(0.40, 1.00, 0.26), _v(1, -0.5, 0.3))},
                    aim_w=0.0, gun=_v(-0.7, 0.65, 0.3), kick=0.0, belly=0.0,   # barrel up across his chest, along the forearm
                    knee={'L': _v(0.31, 0.64, 0.42), 'R': _v(0.53, 0.64, 0.42)},
                    ankle={'L': _v(0.31, 0.18, 0.50), 'R': _v(0.53, 0.18, 0.50)}, knee_w=0.0, seat_w=1.0)
    if name == 'K2':          # up on his knees, turned to the window, ducking: chest at the window, forearm and
        #                       free hand onto the door top (photo A), the gun held low, muzzle down
        return dict(pelvis=_v(0.56, 0.0, 0.02), p_up=_v(0.45, 1, 0), p_fwd=_v(1, 0, -0.15), c_up=_v(0.9, 1, 0),
                    c_fwd=_v(1, 0, -0.2), h_fwd=_v(1, -0.1, -0.15),
                    hand={'L': (DOOR_HAND, _v(0.3, -1, 0.6)), 'R': (_v(0.72, 0.90, -0.16), _v(0.2, -0.3, -1))},   # chat 43: 2 cm inboard, 4 cm up (the pistol's slide brushed the door top)
                    aim_w=0.0, gun=_v(0.1, -1, -0.1), kick=0.0, belly=0.0,   # chat 43: muzzle less out (0.3): with the
                    #   fist round the handle (Sam 23 Nov) the slide dipped into the door top coming back in, 9.1 s
                    knee=KNEES,
                    ankle={'L': _v(0.20, ANKLE_Y, 0.18), 'R': _v(0.18, ANKLE_Y, -0.16)}, knee_w=1.0, seat_w=0.0)
    if name == 'K3':          # head and shoulders out over the door top, the head leading the turn back (D),
        #                       gun up beside his head, muzzle up
        return dict(pelvis=_v(0.70, 0.0, 0.01), p_up=_v(0.5, 1, 0), p_fwd=_v(1, 0, -0.25), c_up=_v(0.8, 1, -0.05),
                    c_fwd=_v(1, 0, -0.5), h_fwd=_v(0.5, 0, -1),
                    hand={'L': (DOOR_HAND, _v(0.5, -1, 0.6)), 'R': ('rel', _v(0.06, 0.34, -0.10), _v(0.3, -1, -0.5))},
                    aim_w=0.0, gun=_v(0, 1, -0.1), kick=0.0, belly=0.0,
                    knee=KNEES,
                    ankle={'L': _v(0.20, ANKLE_Y, 0.18), 'R': _v(0.18, ANKLE_Y, -0.16)}, knee_w=1.0, seat_w=0.0)
    if name in ('C1', 'C1b', 'C1c', 'C2', 'C2b', 'C2c', 'C3'):
        return _climb(name)
    if name == 'B1':          # breakdown, getting up (and its mirror sitting down): rocking back on his seat, knees
        #                       drawn up and turning toward the window, feet lifted off the floor in front of the
        #                       cushion, left hand pushing on the cushion beside his hip, the pistol at his chest
        return dict(pelvis=_v(0.43, 0.0, -0.05), p_up=_v(0.08, 1, -0.30), p_fwd=_v(0.25, 0, 1), c_up=_v(0.12, 1, 0.08),
                    c_fwd=_v(0.4, 0, 1), h_fwd=_v(0.7, -0.15, 1),
                    hand={'L': (_v(0.40, 0.86, 0.32), _v(-1, -0.6, 0.0)),     # chat 39: lifting off his thigh,
                          'R': (_v(0.46, 1.02, 0.28), _v(1, -0.5, 0.3))},     # on its way up to the door top
                    aim_w=0.0, gun=_v(-0.2, 0.8, 0.6), kick=0.0, belly=0.0,
                    knee={'L': _v(0.36, 0.74, 0.34), 'R': _v(0.58, 0.74, 0.30)},
                    ankle={'L': _v(0.26, 0.40, 0.56), 'R': _v(0.46, 0.40, 0.54)}, knee_w=0.0, seat_w=1.0, leg_ik=1.0)
    if name == 'B1b':         # breakdown: still on his seat, turned further, knees high over the cushion, both feet
        #                       swung up and inboard IN FRONT of the cushion (above its front edge's height), so the
        #                       shins can come back beside it (past its inboard edge), not through it
        return dict(pelvis=_v(0.42, 0.0, -0.03), p_up=_v(0.15, 1, -0.25), p_fwd=_v(0.6, 0, 0.8), c_up=_v(0.3, 1, 0.05),
                    c_fwd=_v(0.75, 0, 0.6), h_fwd=_v(1, -0.3, 0.6),
                    hand={'L': (_v(0.70, 1.04, 0.24), _v(0.0, -1, 0.6)),      # chat 39: reaching for the door
                          'R': (_v(0.56, 1.04, 0.18), _v(1, -0.5, 0.0))},     # top (it pulls him up; was a push
#                                                                               on the cushion: 1.3 m of hand travel)
                    aim_w=0.0, gun=_v(0.1, 0.9, 0.3), kick=0.0, belly=0.0,
                    knee={'L': _v(0.48, 0.78, 0.26), 'R': _v(0.64, 0.78, 0.06)},
                    ankle={'L': _v(0.06, 0.60, 0.42), 'R': _v(0.14, 0.62, 0.32)}, knee_w=0.0, seat_w=1.0, leg_ik=1.0)
    if name == 'B2':          # breakdown: knees landed on their spots on the cushion (planted from here), shins across
        #                       it, feet past its inboard edge, sitting back toward his heels, leaning to the window,
        #                       head ducked, left hand reaching for the door top, the gun up in front on his right
        #                       (chat 39: hips back at x 0.28, over his heels, so the knees land on their spots
        #                       instead of being thrown out toward the door; the left hand already on the door top,
        #                       pulling him up)
        return dict(pelvis=_v(0.28, 0.0, 0.02), p_up=_v(0.45, 1, 0), p_fwd=_v(1, 0, 0.1), c_up=_v(0.9, 1, 0.05),
                    c_fwd=_v(1, 0, 0.05), h_fwd=_v(1, -0.5, 0.05),
                    hand={'L': (_v(0.93, SILL + HAND_R + 0.01, 0.17), _v(0.3, -1, 0.6)),
                          'R': (_v(0.66, 1.00, -0.12), _v(0.2, -0.6, -1))},
                    aim_w=0.0, gun=_v(0.7, 0.3, -0.2), kick=0.0, belly=0.0,
                    knee=KNEES,
                    ankle={'L': _v(0.20, ANKLE_Y, 0.18), 'R': _v(0.18, ANKLE_Y, -0.16)}, knee_w=1.0, seat_w=0.0)
    if name == 'B3':          # breakdown between K2 and K3 (and back): the gun comes up IN FRONT of his chest, elbow
        #                       down, on its way from low to beside his head (straight between the two, the hand
        #                       would pass through his shoulder and the elbow fold past its range: a snap)
        k = _lerp_goal(key('K2'), key('K3'), 0.5)
        k['hand'] = dict(k['hand'])
        k['hand']['L'] = (DOOR_HAND, _v(0.4, -1, 0.6))
        # in front of his RIGHT shoulder, outboard of the shoulder line (chest frame: +x away from his head), so the
        # gun rises outside his face to beside his head (chat 38: from in front of his chest the pistol cut through
        # his face, 3.8 cm, 1.25-1.33 s)
        k['hand']['R'] = ('rel', _v(0.05, 0.10, 0.26), _v(0.3, -0.7, -0.8))
        k['gun'] = _v(0.05, 0.6, 0.8)       # muzzle turning up THROUGH the car's front (not out over the door top)
        return k
    if name in ('K4', 'K5'):  # out to the waist, folded over the door top (B, C), chest turned back along the car
        #                       (D), the gun arm along the line to the lead cruiser; K5 the kick
        k = dict(pelvis=_v(0.755, 0.0, 0.0), p_up=_v(0.55, 1, 0), p_fwd=_v(1, 0, -0.3), c_up=_v(1.15, 1, -0.05),
                 c_fwd=_v(1, 0, -0.85), h_fwd=_v(-0.05, 0, -1),
                 hand={'L': (DOOR_HAND, _v(0.6, -0.6, 0.8)), 'R': ('aim', None, _v(0.3, -1, 0.2))},
                 aim_w=1.0, gun=None,
                 knee=KNEES,
                 ankle={'L': _v(0.20, ANKLE_Y, 0.18), 'R': _v(0.18, ANKLE_Y, -0.16)}, knee_w=1.0, seat_w=0.0)
        k['kick'] = 1.0 if name == 'K5' else 0.0
        k['belly'] = 1.0
        return k
    raise KeyError(name)


def _gun_with_chest(k, raise_=(0.0, 0.0, 0.0), src='K1'):
    """K1's pistol hold carried by this key's chest: the gun hand at K1's place from his right shoulder in his
    chest's frame ('rel'), the barrel turned with the chest (the pistol stays flat on his chest while he climbs)."""
    k1 = key(src)                                 # chat 41: from C2 on, K2's hold (low at his right side,
    o = _solve(k1, fold=False)                    # muzzle down), clear of the left arm reaching across his chest
    off = o['Rc'].T @ (o['balls']['R'] - o['J']['shR']) + np.asarray(raise_, float)   # (his right, up, forward)
    Rc = _frame(k['c_up'], k['c_fwd'])
    k['hand']['R'] = ('rel', off, Rc @ (o['Rc'].T @ _u(k1['hand']['R'][1])))
    k['gun'] = Rc @ (o['Rc'].T @ _u(k1['gun']))
    return k


def _climb(name):
    """Chat 41: getting up from sitting to kneeling, re-planned from how a person climbs onto a seat on their
    knees (one knee at a time, the hips lifted first): C1 the hips lifted off the cushion, pushing on the left
    thigh, both feet still on the floor; C1b the right (window-side) knee lifted high, its foot up in front of the
    cushion's front edge; C2 the right knee down on its spot (the rear one), the shin across the cushion, the left
    foot still on the floor, the hips over the middle of the cushion; C2b the left knee lifted, its foot up in
    front; C3 both knees on their spots, the hips still low and inboard, the left hand on the door top. Right knee
    FIRST: its spot is the rear one, so the left shin (front) never has to be crossed. Sitting down is the same
    path backwards (left knee off first)."""
    up = dict(knee_w=0.0, seat_w=1.0, leg_ik=1.0, aim_w=0.0, kick=0.0, belly=0.0)
    if name == 'C1':
        k = dict(up, pelvis=_v(0.41, 0.0, 0.01), p_up=_v(0.12, 1, 0.10), p_fwd=_v(0.35, 0, 1),
                 c_up=_v(0.45, 1, 0.35), c_fwd=_v(0.6, -0.3, 1), h_fwd=_v(0.7, -0.3, 1), lift=0.10,
                 hand={'L': (_v(0.32, 0.87, 0.30), _v(-1, -0.6, -0.2)), 'R': None},
                 knee={'L': _v(0.10, 0.66, 0.42), 'R': _v(0.57, 0.70, 0.36)},
                 ankle={'L': _v(0.16, 0.19, 0.44), 'R': _v(0.56, 0.18, 0.44)})
    elif name == 'C1b':
        k = dict(up, pelvis=_v(0.34, 0.0, 0.02), p_up=_v(0.2, 1, 0.12), p_fwd=_v(0.6, 0, 0.8),   # chat 43: hips 0.38 -> 0.34
                 c_up=_v(0.9, 1, 0.1), c_fwd=_v(0.8, -0.4, 0.7), h_fwd=_v(0.8, -0.6, 0.5), lift=0.20,
                 hand={'L': (_v(0.62, 1.02, 0.28), _v(0.4, -1, 0.6)), 'R': None},
                 knee={'L': _v(-0.02, 0.64, 0.43), 'R': _v(0.82, 0.58, 0.16)},   # chat 43: the slower move's new in-betweens put this thigh 3 cm
#                                  into the door (aiming the knee up ran it into his chest and gun arm): hips 4 cm inboard
                 ankle={'L': _v(0.02, 0.19, 0.44), 'R': _v(0.60, 0.58, 0.36)})
    elif name == 'C2':
        k = dict(up, pelvis=_v(0.26, 0.0, -0.02), p_up=_v(0.3, 1, 0.12), p_fwd=_v(0.85, 0, 0.5),
                 c_up=_v(1.9, 1, 0.15), c_fwd=_v(1, -0.8, 0.3), h_fwd=_v(1, -1.1, 0.3),
                 hand={'L': (_v(0.90, SILL + HAND_R + 0.02, 0.20), _v(0.3, -1, 0.6)), 'R': None},
                 knee={'L': _v(0.16, 0.64, 0.44), 'R': KNEES['R']},
                 ankle={'L': _v(0.02, 0.21, 0.43), 'R': _v(0.18, ANKLE_Y, -0.16)},
                 plant={'L': 0.0, 'R': 1.0})
    elif name == 'C2b':
        k = dict(up, pelvis=_v(0.30, 0.0, 0.03), p_up=_v(0.35, 1, 0.08), p_fwd=_v(0.95, 0, 0.3),
                 c_up=_v(1.5, 1, 0.1), c_fwd=_v(1, -0.6, 0.1), h_fwd=_v(1, -0.7, 0.1),
                 hand={'L': (_v(0.93, SILL + HAND_R + 0.01, 0.18), _v(0.3, -1, 0.6)), 'R': None},
                 knee={'L': _v(0.52, 0.84, 0.36), 'R': KNEES['R']},
                 ankle={'L': _v(0.30, 0.50, 0.40), 'R': _v(0.18, ANKLE_Y, -0.16)},
                 plant={'L': 0.0, 'R': 1.0})
    elif name == 'C1c':     # sitting down only: the right foot lifted clear of the cushion as the knee comes up off
        #                     its spot (backwards, the path is shorter: 0.05 s; without it the foot drags through)
        k = _lerp_goal(key('C2'), key('C1b'), 0.5)
        k.update(knee={'L': _v(-0.02, 0.64, 0.43), 'R': _v(0.80, 0.62, 0.06)},
                 ankle={'L': _v(0.02, 0.19, 0.44), 'R': _v(0.48, 0.68, 0.16)}, plant={'L': 0.0, 'R': 0.0},
                 knee_w=0.0, leg_ik=1.0)
        k['hand'] = dict(k['hand'])
        for sd in 'LR':
            if isinstance(k['hand'][sd], tuple) and k['hand'][sd] and k['hand'][sd][0] == 'mix':
                k['hand'][sd] = None
        k['hand']['L'] = (_v(0.80, 1.03, 0.24), _v(0.2, -1, 0.6))
        k['gun'] = None
    elif name == 'C2c':     # the left knee coming over the cushion onto its spot, its foot above the front edge
        k = dict(up, pelvis=_v(0.36, 0.0, 0.03), p_up=_v(0.38, 1, 0.05), p_fwd=_v(1, 0, 0.15),
                 c_up=_v(1.25, 1, 0.08), c_fwd=_v(1, -0.45, 0.05), h_fwd=_v(1, -0.6, 0.05),
                 hand={'L': (_v(0.94, SILL + HAND_R + 0.005, 0.17), _v(0.3, -1, 0.6)), 'R': None},
                 knee={'L': _v(0.62, 0.68, 0.20), 'R': KNEES['R']},
                 ankle={'L': _v(0.24, 0.62, 0.28), 'R': _v(0.18, ANKLE_Y, -0.16)},
                 plant={'L': 0.0, 'R': 1.0})
    else:   # C3
        k = dict(up, pelvis=_v(0.44, 0.0, 0.02), p_up=_v(0.4, 1, 0.03), p_fwd=_v(1, 0, 0.05),
                 c_up=_v(1.0, 1, 0.05), c_fwd=_v(1, -0.3, -0.05), h_fwd=_v(1, -0.45, -0.05),
                 hand={'L': (DOOR_HAND, _v(0.3, -1, 0.6)), 'R': None},
                 knee=KNEES, ankle={'L': _v(0.20, ANKLE_Y, 0.18), 'R': _v(0.18, ANKLE_Y, -0.16)},
                 knee_w=1.0, seat_w=0.0, leg_ik=0.0)
    k['hand'] = dict(k['hand'])
    lift_gun = {'C1b': (-0.03, 0.16, 0), 'C2': (0.06, 0.11, -0.03), 'C2b': (0.04, 0.02, -0.02), 'C2c': (0.04, 0.05, -0.01), 'C3': (0.03, 0.03, 0.03), 'C1c': (0, 0.10, 0)}.get(name, (0, 0, 0))   # the gun arm up, clear of the rising knee (chat 43: C2c, C3 3 cm higher: the gun hand touched the right thigh; C2-C2c 3-4 cm back from the door: with the fist
    #   round the handle, Sam 23 Nov, the slide reached the door)
    return _gun_with_chest(k, lift_gun, 'K2' if name == 'C3' else 'K1')


KICK_DEG = 7.0                   # the pistol's kick: the forearm flips up this much (a real one-hand kick)


_BD0 = [(0.56, 'C1'), (0.62, 'C1b'), (0.71, 'C2'), (0.77, 'C2b'), (0.83, 'C2c'), (0.89, 'C3'), (1.2, 'B3'),
        (7.175, 'B3'), (7.45, 'C3'), (7.49, 'C2c'), (7.53, 'C2b'), (7.57, 'C2'), (7.635, 'C1b'), (7.70, 'C1')]
import leanout as _LO   # noqa: E402
import parts as _PARTS        # noqa  (cost-spike fix 5c: this module is kept in parts; parts.py)
BREAKDOWNS = [(round(t * _LO.SLOW, 4), k) for t, k in _BD0]   # Sam 23 Nov: 25% slower (leanout.SLOW)
#   chat 41: the get-up / sit-down re-planned (_climb: hips first, then one knee at a time, the window-side knee
#   first; sitting down the same path backwards); chat 39's B1, B1b, B2 kept below, unused   # chat 39: the knees' landing given 0.2 s (was 0.14 s; the beats K1 0.5, K2 1.0 unchanged)
#   in-between drawings that shape the path between two locked beats (the feet go up over the cushion's front edge, not through it); beats unchanged


def _times():
    import leanout as LO
    return sorted(LO.TIMES + BREAKDOWNS, key=lambda x: x[0])


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
_BD_T = {t for t, _ in BREAKDOWNS}


def _abs_spec(x):
    return isinstance(x, tuple) and len(x) == 2 and not isinstance(x[0], str) and x[0] is not None


GUN_THROUGH = {t for t, k in _LO.TIMES if k == 'K2'}   # K2's times: the gun hand (only) passes K2 with speed (chat 39: stopping dead
#                                  there and whipping up made the elbow pop); the pose at K2 is still met exactly


def _herm(p, tt, s, i, through=()):
    """Monotone cubic through four values p[0..3] at times tt[0..3], at s in [0,1] between p[1] and p[2]. A locked
    beat (not a breakdown) has zero speed (he settles on it); a breakdown is passed THROUGH with speed (no stop:
    a stop there is a pop), its speed per number made zero where the path turns back (no overshoot)."""
    p = [np.asarray(v, float) for v in p]
    h = tt[2] - tt[1]
    d = [(p[k + 1] - p[k]) / max(tt[k + 1] - tt[k], 1e-6) for k in range(3)]

    def tan(k):                                   # the speed at key k (1 or 2)
        if tt[k] not in _BD_T and tt[k] not in through:
            return np.zeros_like(p[1])
        a, b = d[k - 1], d[k]
        m = (a + b) / 2
        m = np.where(a * b <= 0, 0.0, m)
        lim = 3 * np.minimum(np.abs(a), np.abs(b))
        return np.clip(m, -lim, lim)
    s2, s3 = s * s, s * s * s
    return ((2 * s3 - 3 * s2 + 1) * p[1] + (s3 - 2 * s2 + s) * h * tan(1) + (-2 * s3 + 3 * s2) * p[2] +
            (s3 - s2) * h * tan(2))


_ABSH = {}
_PELY = {}


def _pel_y(name):
    """A key's own hip height (its pelvis joint's y, solved once)."""
    if name not in _PELY:
        _PELY[name] = float(_solve(_KEYC.setdefault(name, key(name)), fold=False)['pel'][1])
    return _PELY[name]


_THIGH = {}
THIGH_BLEND = True


def _thigh(name, sd):
    """A key's own thigh way (hip -> knee, car frame, solved once)."""
    if (name, sd) not in _THIGH:
        o = _solve(_KEYC.setdefault(name, key(name)), fold=False)
        _THIGH[(name, sd)] = _u(o['J']['kn' + sd] - o['J']['hip' + sd])
    return _THIGH[(name, sd)]


def _rel_hand(name, sd, spec):
    """A key's hand goal as an offset from his own shoulder in his chest's frame (a 'rel' goal): solved once per
    key. Blended this way, a hand on its way somewhere moves WITH his body (the shoulder carries it), so it cannot
    cut through the shoulder while the body turns and rises."""
    if (name, sd) not in _ABSH:
        o = _solve(_KEYC.setdefault(name, key(name)), fold=False)
        _ABSH[(name, sd)] = (o['Rc'].T @ (o['balls'][sd] - o['J']['sh' + sd]),
                             o['Rc'].T @ (o['J']['el' + sd] - o['J']['sh' + sd]))
    hand, elb = _ABSH[(name, sd)]
    if isinstance(spec, tuple) and spec and isinstance(spec[0], str) and spec[0] == 'rel':
        hand = np.asarray(spec[1], float)
    # the elbow's bend: where the key's own elbow sits from his shoulder, in his chest's frame (chat 39: a pole
    # blended as a fixed way in the car swung the elbow out and back 22 cm a frame at 1.1 s, while the gun hand
    # folded in past his shoulder; blended with the chest, the elbow stays down in front and the forearm swings up)
    return (hand, elb)


def _herm_goal(G, tt, s, fallback, names=()):
    """_herm over every number of four goal dicts; parts that are not plain numbers (aim, 'rel' hands) fall back to
    the eased blend of the two keys."""
    out = {}
    for n in G[1]:
        xs = [g[n] for g in G]
        if isinstance(xs[1], dict):
            out[n] = {}
            for sd in xs[1]:
                vs = [x[sd] for x in xs]
                if n == 'hand' and any(isinstance(v[0], str) for v in vs):
                    rv = [_rel_hand(nm, sd, v) for nm, v in zip(names, vs)]
                    th = GUN_THROUGH if sd == 'R' else ()
                    out[n][sd] = ('rel', _herm([v[0] for v in rv], tt, s, 0, th),
                                  _herm([v[1] for v in rv], tt, s, 0, th), 'chest')
                elif all(_abs_spec(v) for v in vs):
                    out[n][sd] = (_herm([v[0] for v in vs], tt, s, 0), _herm([v[1] for v in vs], tt, s, 0))
                elif all(not isinstance(v, tuple) for v in vs):
                    out[n][sd] = _herm(vs, tt, s, 0)
                else:
                    out[n][sd] = fallback[n][sd]
        elif any(x is None for x in xs):
            out[n] = fallback[n]
        else:
            out[n] = _herm(xs, tt, s, 0)
            if n in ('knee_w', 'seat_w', 'aim_w', 'kick', 'belly'):
                out[n] = float(np.clip(out[n], 0, 1))
    return out


def goals_at(t):
    T = _times()
    t = min(max(t, T[0][0]), T[-1][0])
    for i, ((t0, a), (t1, b)) in enumerate(zip(T, T[1:])):
        if t0 <= t <= t1:
            u = 0.0 if t1 == t0 else _ease((t - t0) / (t1 - t0))
            ka = _KEYC.setdefault(a, key(a))
            kb = _KEYC.setdefault(b, key(b))
            if t1 == t0 or not ({t0, t1} & _BD_T):
                return _lerp_goal(ka, kb, u)
            # parts the smooth path cannot carry (the aim, 'rel' hands) still pass a breakdown with speed: a
            # time-warp with speed 1 at the breakdown end(s) and 0 at a locked beat
            s_ = (t - t0) / (t1 - t0)
            if t0 in _BD_T and t1 in _BD_T:
                uw = s_
            elif t1 in _BD_T:
                uw = -s_ ** 3 + 2 * s_ ** 2
            else:
                uw = s_ + s_ ** 2 - s_ ** 3
            lin = _lerp_goal(ka, kb, uw)
            # a span touching a breakdown: a smooth path through it (Hermite), not a stop on it
            tp, pa = T[max(i - 1, 0)]
            tn, nb = T[min(i + 2, len(T) - 1)]
            G = [_KEYC.setdefault(k, key(k)) for k in (pa, a, b, nb)]
            out = _herm_goal(G, [tp, t0, t1, tn], (t - t0) / (t1 - t0), lin, (pa, a, b, nb))
            if any(_KEYC[k].get('lift', 0) or max(_KEYC[k]['plant'].values()) > 0 and _KEYC[k]['knee_w'] < 0.999
                   for k in (a, b)) and (ka['knee_w'] >= 0.999) == (kb['knee_w'] >= 0.999):
                # chat 41: hips lifted, or one knee down: the hips' height follows the keys' own solved heights
                out['pel_y'] = float(_herm([_pel_y(k) for k in (pa, a, b, nb)], [tp, t0, t1, tn], (t - t0) / (t1 - t0), 0))
            if (ka['knee_w'] >= 0.999) != (kb['knee_w'] >= 0.999):
                # the weight moving from his seat to his knees (or back): the hips' height follows a smooth path
                # between the two poses' own heights (blending the two supports' heights jumps)
                out['pel_y'] = float(_herm([_pel_y(k) for k in (pa, a, b, nb)], [tp, t0, t1, tn], (t - t0) / (t1 - t0), 0))
                # ... and each thigh TURNS smoothly from one pose's way to the other's (chat 39: aiming the knee at
                # a blended point nearer than a thigh's length overshot it into the cushion, which pushed the knee
                # flat out 25 cm in one frame, a 54 cm pop at 0.79 s and 7.56 s)
                out['thigh'] = {sd: _u(_herm([_thigh(k, sd) for k in (pa, a, b, nb)], [tp, t0, t1, tn],
                                             (t - t0) / (t1 - t0), 0)) for sd in 'LR'}
            return out
    return key(T[-1][1])


_PARTS.include(globals(), 'bench_move_b', 'bench_move_c', 'bench_move_d')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'run':
        run(sys.argv[2], span=(float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else None)
    elif cmd == 'clip':          # clip OUT_DIR OUT.mp4 [T0 T1] [--dressed]
        dr = '--dressed' in sys.argv
        av = [a for a in sys.argv if a != '--dressed']
        checked_clip(av[2], av[3], span=(float(av[4]), float(av[5])) if len(av) > 5 else None, dressed=dr)
    elif cmd == 'dressed':       # dressed OUT.png [KEY] [T]
        dressed_still(sys.argv[2], *(sys.argv[3:4] or ['K4']), *[float(x) for x in sys.argv[4:5]])
    elif cmd == 'checks':
        run(sys.argv[2], draw_frames=False)
    elif cmd == 'name':          # name OUT_DIR "why": the last check pass's faults named, so the clip may draw
        name_faults(sys.argv[2], sys.argv[3])
    elif cmd == 'keep':          # keep OUT_DIR: the frame store as the bundle on GitHub
        keep(sys.argv[2])
    elif cmd == 'proof':
        proof(sys.argv[2])
    elif cmd == 'keys':
        key_sheet(sys.argv[2], *(sys.argv[3:4] and [sys.argv[3].split(',')]))
