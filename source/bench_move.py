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
            if len(spec) > 3 and spec[3] == 'chest':       # the pole is the elbow's place in the chest's frame
                return sh + chest_R @ spec[1], chest_R @ np.asarray(spec[2], float)
            return sh + chest_R @ spec[1] * np.array([1, 1, 1]), spec[2]
        if spec[0] == 'aim':
            return sh + aim_dir * l_reach, spec[2]
    return np.asarray(spec[0], float), np.asarray(spec[1], float)


class Pose(dict):
    """Joint points (car frame) + .aim (the pistol's way) + .fwd for bench_draw.gun_mesh."""


def _planted(g):
    return g.get('plant') or {'L': 0.0, 'R': 0.0}


def solve(g, seat_dy=None):
    """Goals -> the posed body: dict(P points, J joints, R bone turns, balls, gun (points, tris), aim). Kneeling,
    each knee is settled ON the cushion: a first pass measures each knee's skin gap, the second takes it out."""
    if float(g['knee_w']) <= 0 and max(_planted(g).values()) < 0.999:
        return _solve(g, seat_dy)
    first = _solve(g, seat_dy, fold=False)
    gaps = knee_gaps(first['P'], first['J'])
    return _solve(g, seat_dy, knee_dy={sd: gaps[sd] - 0.001 for sd in 'LR'})


def pistol_mesh(pose, ball, aim_w):
    """The pistol in the gun hand (gun3d_film's blocks). Aimed, it is held upright (its grip straight down from the
    barrel, no cant), the fist round the handle (gun3d_film.GRIP): the slide and barrel clear above the hand ball,
    as in a real grip. Seated (K1) it lies flat on his chest (its grip across the chest), held between fist and
    chest. Between the two, blended by aim_w."""
    import gun3d_film as GF
    V, T, K = GF.mesh(1.0)
    d = _u(pose.aim)
    fwd = np.asarray(pose['fwd'], float)
    flat = np.cross(fwd, d)
    if flat[1] > 0:
        flat = -flat
    flat = _u(flat)
    upright = _u(np.array([0, -1.0, 0]) - d * (-d[1]))
    w = float(np.clip(aim_w, 0, 1))
    down = _u((1 - w) * flat + w * upright + 1e-6)
    down = _u(down - d * np.dot(down, d))
    side = np.cross(d, down)
    ga, gb = GF.GRIP                     # Sam 23 Nov: the fist round the HANDLE, the slide clear above it (it had
    #                                      sat on the slide: the fist's middle level with the slide's bottom edge)
    top = ball - fwd * 0.012 * (1 - w) - d * (ga * GF.UNIT) - down * (gb * GF.UNIT)
    return top + V[:, :1] * d + V[:, 1:2] * down + V[:, 2:3] * side, T


def gun_rests(Pg, P, jw, ball):
    """The pistol RESTS against his own gun arm, never in it: its back end (behind the fist) ran 0.6-1.3 cm into
    the wrist when it pointed out along the forearm (chat 38, 1.0-1.3 s). Each pistol point outside the fist is
    tested against the right forearm's skin near the wrist (nearest skin point and its outward normal); the whole
    pistol moves out along the forearm's normal by the deepest point plus 2 mm (it stays in the fist: a small shift).
    """
    from scipy.spatial import cKDTree
    r = rig()
    tb = _body_tris()
    use = np.unique(tb)
    arm = use[(r['region'][use] == 5) & (np.linalg.norm(P[use] - jw['wrR'], axis=1) < 0.16)]
    if not len(arm):
        return Pg
    N = _normals(P, tb)[arm]
    tree = cKDTree(P[arm])
    for _ in range(3):
        m = np.linalg.norm(Pg - ball, axis=1) > HAND_R
        d, k = tree.query(Pg[m])
        s = np.einsum('ij,ij->i', Pg[m] - P[arm][k], N[k])
        bad = (s < 0) & (d < 0.03)
        if not bad.any():
            break
        push = _u(N[k][bad].mean(0))
        Pg = Pg + push * (float(-s[bad].min()) + 0.002)
    return Pg


def knee_gaps(P, J):
    """Each knee's lowest skin above the cushion's top (metres), the skin within 12 cm of the knee joint."""
    r = rig()
    out = {}
    for sd in 'LR':
        Q = P[r['keep'] & (r['region'] == (6 if sd == 'L' else 8))]
        near = np.linalg.norm(Q - J['kn' + sd], axis=1) < 0.12
        out[sd] = float(Q[near, 1].min() - SEAT_TOP)
    return out


def _solve(g, seat_dy=None, knee_dy=None, fold=True):
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
        kg[1] = SEAT_TOP + KNEE_R - (knee_dy[sd] if knee_dy else 0.0)
        hxz = pel + hipoff[sd]
        dxz = np.hypot(hxz[0] - kg[0], hxz[2] - kg[2])
        y_knee.append(kg[1] + math.sqrt(max(r['L_th'] ** 2 - dxz ** 2, 0.0)) - hipoff[sd][1])
    y_seat = SEAT_Y if seat_dy is None else seat_dy
    w = float(np.clip(g['knee_w'], 0, 1))
    pel[1] = (1 - w) * y_seat + w * float(np.mean(y_knee)) + (1 - w) * float(g.get('lift', 0.0))
    if 'pel_y' in g:
        pel[1] = g['pel_y']
    one = [k for k, sd in enumerate('LR') if _planted(g)[sd] >= 0.999]
    if w < 0.999 and len(one) == 1:             # chat 41: ONE knee down: the hips' height is what that thigh
        pel[1] = y_knee[one[0]]                 # reaches (the knee stays on its spot, no sliding)
    elif w > 0:                                   # kneeling unevenly, the hips tip to the side so BOTH knees rest
        dy = (y_knee[0] - y_knee[1]) * w        # the L hip wants to be this much higher than the R hip
        hw = np.linalg.norm(hipoff['L'] - hipoff['R'])
        from scipy.spatial.transform import Rotation as Ro
        ax = _u(Rp[:, 2])
        best = None
        for sg in (1, -1):
            Rr = Ro.from_rotvec(ax * sg * math.asin(np.clip(dy / hw, -0.5, 0.5))).as_matrix() @ Rp
            err = abs(((Rr @ J0['hipL'])[1] - (Rr @ J0['hipR'])[1]) - dy)
            if best is None or err < best[0]:
                best = (err, Rr)
        Rp = best[1]
        if w >= 0.999 and 'pel_y' not in g:
            # fully on his knees: the hips' height and side tip solved EXACTLY so each thigh reaches its knee's
            # planted spot (the first-order tip above left the left knee sliding 3 cm while planted, chat 38)
            from scipy.optimize import fsolve
            Rp0 = Rp
            kgs = []
            for sd in 'LR':
                kg = np.asarray(g['knee'][sd], float).copy()
                kg[1] = SEAT_TOP + KNEE_R - (knee_dy[sd] if knee_dy else 0.0)
                kgs.append(kg)

            def _err(x):
                Rr = Ro.from_rotvec(ax * x[1]).as_matrix() @ Rp0
                pp = np.array([pel[0], x[0], pel[2]])
                return [np.linalg.norm(kgs[k] - (pp + Rr @ J0['hip' + sd])) - r['L_th'] for k, sd in enumerate('LR')]
            x, _, ok, _ = fsolve(_err, [pel[1], 0.0], full_output=True)
            if ok == 1 and abs(x[1]) < 0.5 and max(abs(e) for e in _err(x)) < 1e-4:
                pel[1] = x[0]
                Rp = Ro.from_rotvec(ax * x[1]).as_matrix() @ Rp0
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
        ky = SEAT_TOP + KNEE_R - (knee_dy[sd] if knee_dy else 0.0)
        kg[1] = kg[1] * (1 - w) + ky * w
        dt = _u(kg - hip)
        kn = hip + dt * r['L_th']
        lik = float(np.clip(g.get('lik_R' if sd == 'R' else 'leg_ik', g.get('leg_ik', 0.0)), 0, 1))
        if w < 0.999 and _planted(g)[sd] >= 0.999:
            # chat 41: this knee is down on its spot: the thigh reaches it (the hips were set from it)
            kg[1] = ky
            dt = _u(kg - hip)
            kn = hip + dt * r['L_th']
        elif 'thigh' in g and THIGH_BLEND:
            # the weight moving seat <-> knees: the thigh's way is given (goals_at), the foot follows its goal
            kn = hip + _u(g['thigh'][sd]) * r['L_th']
            dt = _u(kn - hip)
        elif lik > 0:
            # in-between drawings place the FOOT (the ankle goal is a point) and the knee follows, bending toward
            # the knee goal (two-bone IK), so a foot path round the cushion is a path the foot really takes
            kn_ik, an_ik = _two_bone(hip, np.asarray(g['ankle'][sd], float), r['L_th'], r['L_sh'], kg - hip)
            an_ray = kn + _u(np.asarray(g['ankle'][sd], float) - kn) * r['L_sh']
            kn = hip + _u(kn + (kn_ik - kn) * lik - hip) * r['L_th']
            an_mix = an_ray + (an_ik - an_ray) * lik
            dt = _u(kn - hip)
            g = dict(g)
            g['ankle'] = dict(g['ankle'])
            g['ankle'][sd] = an_mix
        floor = SEAT_TOP + KNEE_R - (knee_dy[sd] if knee_dy else 0.0)
        if kn[1] < floor - 1e-4 and 0.18 <= kn[0] <= 0.70 and -0.35 <= kn[2] <= 0.25 and hip[1] - floor < r['L_th']:
            # a knee coming down over the cushion RESTS on it (it cannot sink in): the thigh keeps its length and
            # its way round, the knee goes onto the cushion's top
            hz = _u(np.array([kg[0] - hip[0], 0.0, kg[2] - hip[2]]) + 1e-9)
            rad = math.sqrt(r['L_th'] ** 2 - (hip[1] - floor) ** 2)
            kn = np.array([hip[0], floor, hip[2]]) + hz * rad
            dt = _u(kn - hip)
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
    if FOLD and fold:
        P = press_folds(P, jw)
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
    Pg, Tg = pistol_mesh(pose, balls['R'], g.get('aim_w', 0.0))
    Pg = gun_rests(Pg, P, jw, balls['R'])
    return dict(P=P, J=jw, balls=balls, gun=(Pg, Tg), aim=pose.aim, pel=pel, Rc=Rc, Rp=Rp, Rh=Rh, pose=pose)


FOLD = True
ANKLE_Y = 0.667                  # kneeling: the ankles' height behind the knees (fit_ankles: shins ON the cushion)


def fit_ankles():
    """ANKLE_Y: the lowest ankle height that keeps the shins' skin on the cushion, not in it (kneeling keys)."""
    global ANKLE_Y
    r = rig()
    seat = [s for s in solids() if s[0] == 'seat R'][0]
    for _ in range(8):
        worst = 0.0
        for k in ('K2', 'K3', 'K4'):
            P = solve(key(k))['P']
            leg = np.isin(r['region'], (6, 8, 12, 14)) & r['keep']
            worst = max(worst, float(inside_depth(P[leg], seat).max()))
        if worst <= 0.001:
            break
        ANKLE_Y += worst + 0.002
    return ANKLE_Y
FOLD_ZONE = {(1, 6): ('hipL', 'pelvis'), (1, 8): ('hipR', 'pelvis'), (1, 7): ('pelvis',), (6, 7): ('pelvis',),
             (7, 8): ('pelvis',), (6, 8): ('pelvis',), (1, 3): ('shL',), (1, 5): ('shR',), (1, 10): ('neck', 'head')}
FOLD_R = 0.20                    # a fold: skin within this of the joint the two parts share (hip, armpit, neck)


def press_folds(P, jw, iters=8, ease=True):
    """Flesh pressed together at the joint folds (groin, armpit, neck): skinning by bone weights lets the skin of
    two parts meeting at a bent joint pass into each other there. Real flesh does not; it presses flat. Each skin
    point of one part found inside the other part's skin, within FOLD_R of their shared joint, is moved out to the
    other part's surface (2 mm outside), a few rounds, then its ring of neighbours eased. Pose errors away from the
    folds (a forearm sunk in the chest) are NOT touched: the checks still see them."""
    from scipy.spatial import cKDTree
    r = rig()
    tb = _body_tris()
    use = np.unique(tb)
    reg = r['region'][use]
    P = P.copy()
    moved = np.zeros(len(P), bool)
    for it in range(iters):
        wide = 0.006 if it < iters - 3 else 0.03
        Q = P[use]
        N = _normals(P, tb)[use]
        cand, dest = [], []
        for (a, b), joints in FOLD_ZONE.items():
            JP = np.array([jw[j] for j in joints])
            for x, y in ((a, b), (b, a)):
                mx, my = reg == x, reg == y
                if not mx.any() or not my.any():
                    continue
                ix = np.where(mx)[0]
                dj = np.min(np.linalg.norm(Q[ix][:, None] - JP[None], axis=2), 1)
                ix = ix[dj < FOLD_R]
                if not len(ix):
                    continue
                iy = np.where(my)[0]
                d, j = cKDTree(Q[iy]).query(Q[ix], distance_upper_bound=0.12)
                ok = np.isfinite(d) & (d > TOUCH * 0.5)
                jj = np.where(ok, j, 0)                            # behind the other part's skin there (its
                ok &= np.einsum('ij,ij->i', Q[ix] - Q[iy[jj]], N[iy[jj]]) < wide   # normal): the only ones to test
                cand.append(ix[ok])
                dest.append(iy[j[ok]])
        if not cand:
            break
        ci, di = np.concatenate(cand), np.concatenate(dest)
        if not len(ci):
            break
        m = _inside2(Q[ci], N[ci], P, tb)
        if os.environ.get('FOLD_DEBUG'):
            print('press round', it, 'cand', len(ci), 'inside', int(m.sum()))
        if not m.any():
            break
        ci, di = ci[m], di[m]
        P[use[ci]] = Q[di] + N[di] * 0.002
        moved[use[ci]] = True
    if moved.any() and ease:                                        # ease the ring around what moved
        nb = {}
        for t in tb:
            for a_ in t:
                nb.setdefault(a_, set()).update(t)
        ring = set()
        for v in np.where(moved)[0]:
            ring |= nb.get(v, set())
        ring = np.array(sorted(ring - set(np.where(moved)[0])), int)
        for _ in range(2):
            P[ring] = 0.5 * P[ring] + 0.5 * np.array([P[list(nb[v])].mean(0) for v in ring])
        P = _settle(P, jw)                                          # the easing can nudge a point back in
    return P


SETTLE_MAX = 0.04                # the farthest a fold-zone skin point may move in one settle step


def _settle(P, jw, rounds=10):
    """Last step of the press: every fold-zone skin point still inside the body goes to the nearest FREE skin point
    (one found outside) of another part, 2 mm out. Free points are outside, so this ends inside-free."""
    from scipy.spatial import cKDTree
    r = rig()
    tb = _body_tris()
    use = np.unique(tb)
    reg = r['region'][use]
    zone = np.zeros(len(use), bool)
    for (a, b), joints in FOLD_ZONE.items():
        JP = np.array([jw[j] for j in joints])
        m = np.isin(reg, (a, b))
        zone[m] |= np.min(np.linalg.norm(P[use][m][:, None] - JP[None], axis=2), 1) < FOLD_R
    zi = np.where(zone)[0]
    mate = {}
    for (a, b) in FOLD_ZONE:
        mate.setdefault(a, set()).add(b)
        mate.setdefault(b, set()).add(a)
    cur = zi                                 # round 1 tests every fold-zone point; later rounds only the points
    for _ in range(rounds):                  # moved last round (a test costs ~2 s: chat 38's render ran 60 s a frame)
        Q = P[use]
        N = _normals(P, tb)[use]
        ins = _inside2(Q[cur], N[cur], P, tb)
        if os.environ.get('FOLD_DEBUG'):
            print('settle inside', int(ins.sum()))
        if not ins.any():
            if len(cur) == len(zi):
                break
            cur = zi                            # a local round came out clean: one full round confirms it
            continue
        free = np.ones(len(use), bool)
        free[cur[ins]] = False
        moved = []
        for i in cur[ins]:
            fm = free & np.isin(reg, list(mate.get(reg[i], ())))
            fi = np.where(fm)[0]
            dd = np.linalg.norm(Q[fi] - Q[i], axis=1)
            j = fi[np.argmin(dd)]
            if dd.min() > SETTLE_MAX:          # flesh presses flat; it never jumps across the body (chat 38: more
                continue                       # rounds without this cap moved a chest point into the head)
            P[use[i]] = Q[j] + N[j] * 0.002
            moved.append(i)
        if not moved:
            break
        mv = np.array(moved, int)               # the moved points and every fold-zone point within 3 cm of one
        near = cKDTree(P[use][mv]).query(P[use][zi], distance_upper_bound=0.03)[0]
        cur = np.union1d(mv, zi[np.isfinite(near)])
    return P


KNEE_R = 0.055                   # the knee's skin below its joint when kneeling (measured: _fit_knee)
SEAT_Y = 0.551                   # the seated pelvis height (solved by fit_seat: his seat on the cushion)


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
def _winding_sum(Q, V, T):
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


# The inside test, fast and exact (proposal bench-speedup step 2, chat 40). The old sum over all 20,304 triangles
# (_winding_sum) stays the referee. The body's skin is closed except two 24-edge holes at the wrists (the 3D hands
# are left out); capped by 48 lid triangles it is closed, so its winding number at a point is a whole number: the
# signed count of skin crossed by a ray from the point (+x), found through a grid of the triangles seen along x.
# The open skin's number is that count minus the lids' own exact share (the same sum over the 48 lids only).
# A ray that grazes an edge, a point on the skin, or a result within 1e-6 of the 0.5 line goes to the old sum.
SLOW_INSIDE = bool(os.environ.get('BENCH_OLD_INSIDE'))
GRID_CELL = 0.01


@njit(cache=True)
def _grid_build(V, T, lo, cell, ny, nz):
    cnt = np.zeros(ny * nz + 1, np.int64)
    for t in range(len(T)):
        y0 = min(V[T[t, 0], 1], V[T[t, 1], 1], V[T[t, 2], 1])
        y1 = max(V[T[t, 0], 1], V[T[t, 1], 1], V[T[t, 2], 1])
        z0 = min(V[T[t, 0], 2], V[T[t, 1], 2], V[T[t, 2], 2])
        z1 = max(V[T[t, 0], 2], V[T[t, 1], 2], V[T[t, 2], 2])
        for a in range(max(0, int((y0 - lo[0]) / cell)), min(ny - 1, int((y1 - lo[0]) / cell)) + 1):
            for b in range(max(0, int((z0 - lo[1]) / cell)), min(nz - 1, int((z1 - lo[1]) / cell)) + 1):
                cnt[a * nz + b + 1] += 1
    start = np.cumsum(cnt)
    fill = start[:-1].copy()
    idx = np.zeros(start[-1], np.int64)
    for t in range(len(T)):
        y0 = min(V[T[t, 0], 1], V[T[t, 1], 1], V[T[t, 2], 1])
        y1 = max(V[T[t, 0], 1], V[T[t, 1], 1], V[T[t, 2], 1])
        z0 = min(V[T[t, 0], 2], V[T[t, 1], 2], V[T[t, 2], 2])
        z1 = max(V[T[t, 0], 2], V[T[t, 1], 2], V[T[t, 2], 2])
        for a in range(max(0, int((y0 - lo[0]) / cell)), min(ny - 1, int((y1 - lo[0]) / cell)) + 1):
            for b in range(max(0, int((z0 - lo[1]) / cell)), min(nz - 1, int((z1 - lo[1]) / cell)) + 1):
                c = a * nz + b
                idx[fill[c]] = t
                fill[c] += 1
    return start, idx


@njit(cache=True)
def _edge(V, u, v, qy, qz):
    sg = 1.0
    if u > v:                                          # each edge computed one way for both its triangles
        u, v = v, u
        sg = -1.0
    return sg * ((V[v, 1] - V[u, 1]) * (qz - V[u, 2]) - (V[v, 2] - V[u, 2]) * (qy - V[u, 1]))


@njit(parallel=True, cache=True)
def _ray_count(Q, V, T, start, idx, lo, cell, ny, nz):
    """Signed skin crossings along +x from each point; flag 1 where the ray is ambiguous (an edge, the skin)."""
    out = np.zeros(len(Q))
    amb = np.zeros(len(Q), np.int64)
    eps = 1e-11
    for i in prange(len(Q)):
        qx, qy, qz = Q[i, 0], Q[i, 1], Q[i, 2]
        a = int(math.floor((qy - lo[0]) / cell))
        b = int(math.floor((qz - lo[1]) / cell))
        if a < 0 or b < 0 or a >= ny or b >= nz:
            continue
        c = a * nz + b
        s = 0.0
        for k in range(start[c], start[c + 1]):
            t = idx[k]
            e0 = _edge(V, T[t, 0], T[t, 1], qy, qz)
            e1 = _edge(V, T[t, 1], T[t, 2], qy, qz)
            e2 = _edge(V, T[t, 2], T[t, 0], qy, qz)
            small = abs(e0) < eps or abs(e1) < eps or abs(e2) < eps
            if small:                                  # on or next to an edge seen along x: let the referee decide
                if (e0 > -eps and e1 > -eps and e2 > -eps) or (e0 < eps and e1 < eps and e2 < eps):
                    amb[i] = 1
                continue
            pos = e0 > 0 and e1 > 0 and e2 > 0
            neg = e0 < 0 and e1 < 0 and e2 < 0
            if not (pos or neg):
                continue
            tot = e0 + e1 + e2                         # each edge's weight belongs to the corner facing it
            x = (e1 * V[T[t, 0], 0] + e2 * V[T[t, 1], 0] + e0 * V[T[t, 2], 0]) / tot
            if abs(x - qx) < 1e-9:
                amb[i] = 1
                continue
            if x > qx:
                s += 1.0 if pos else -1.0
        out[i] = s
    return out, amb


def _lids():
    """The wrist holes' rims (each boundary edge's far end, in order) and the lid fans' triangles (rim, centre)."""
    r = rig()
    if 'lids' not in r:
        tb = _body_tris()
        E = set(map(tuple, np.concatenate([tb[:, [0, 1]], tb[:, [1, 2]], tb[:, [2, 0]]])))
        nxt = {u: v for (u, v) in E if (v, u) not in E}
        loops, seen = [], set()
        for u in list(nxt):
            if u in seen:
                continue
            L = [u]
            seen.add(u)
            c = nxt[u]
            while c != u:
                L.append(c)
                seen.add(c)
                c = nxt[c]
            loops.append(np.array(L, np.int64))
        r['lids'] = loops
    return r['lids']


def _capped(V):
    """The skin's points plus one centre point per wrist hole, and the closed skin's triangles."""
    tb = _body_tris()
    loops = _lids()
    n = len(V)
    Vc = np.concatenate([V, np.array([V[L].mean(0) for L in loops])])
    lid = []
    for li, L in enumerate(loops):
        for j in range(len(L)):
            u, v = L[j], L[(j + 1) % len(L)]       # the skin has u->v; the lid runs v->u
            lid.append((v, u, n + li))
    lid = np.array(lid, np.int64)
    return Vc, np.concatenate([tb, lid]), lid


_SIGN = {}


def _winding(Q, V, T):
    """The body skin's winding number at points Q (same values as _winding_sum to rounding; see above). Any other
    triangle set, or SLOW_INSIDE, uses the old sum."""
    Q = np.ascontiguousarray(Q, float)
    if SLOW_INSIDE or T is not _body_tris() or not len(Q):
        return _winding_sum(Q, V, T)
    Vc, Tc, lid = _capped(np.asarray(V, float))
    lo = np.array([Vc[:, 1].min() - GRID_CELL, Vc[:, 2].min() - GRID_CELL])
    ny = int((Vc[:, 1].max() - lo[0]) / GRID_CELL) + 2
    nz = int((Vc[:, 2].max() - lo[1]) / GRID_CELL) + 2
    start, idx = _grid_build(Vc, Tc, lo, GRID_CELL, ny, nz)
    cnt, amb = _ray_count(Q, Vc, Tc, start, idx, lo, GRID_CELL, ny, nz)
    if 's' not in _SIGN:                              # which way round the count runs on this skin: once, by the
        k = np.where((cnt != 0) & (amb == 0))[0][:8]  # referee on the closed skin (whole numbers there)
        if not len(k):
            return _winding_sum(Q, V, T)
        ref = _winding_sum(Q[k], Vc, Tc)
        _SIGN['s'] = 1.0 if np.sum(cnt[k] * ref) > 0 else -1.0
    w = _SIGN['s'] * cnt - _winding_sum(Q, Vc, lid)
    near = np.abs(np.abs(w) - 0.5) < 1e-6
    redo = (amb > 0) | near
    if redo.any():
        w[redo] = _winding_sum(Q[redo], V, T)
    return w


def _inside2(Q, N, P, tb):
    """Inside the closed skin when stepped 1.5 mm AND 3 mm out along its own skin. A point more than TOUCH (5 mm)
    inside another part is inside at both; a thin flap (the ear) read inside at one step only is not a crossing."""
    w = _wsign()
    m = _winding(Q + N * 0.003, P, tb) * w > 0.5
    if m.any():
        m[m] = _winding(Q[m] + N[m] * 0.0015, P, tb) * w > 0.5
    return m


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
            out.setdefault('bad_pts', []).append(Q[m])
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
        wn = _inside2(Q[cand], N[cand], P, tb)                       # 1.5 and 3 mm out along its own skin: a free
        for i in cand[wn]:                                              # skin point is then outside
            dep = float(near[i])
            if dep <= TOUCH:
                continue
            nm = ' / '.join(sorted({REG_NAMES.get(reg[i], 'body'), REG_NAMES.get(near_reg[i], 'body')}))
            out.setdefault('bad_pts', []).append(Q[i][None])
            n0, d0 = hits.get(nm, (0, 0.0))
            hits[nm] = (n0 + 1, max(d0, round(dep * 100, 1)))
    for sd, c in out['balls'].items():
        S = _sphere(c, HAND_R * 0.98)
        wn = _winding(S, P, tb) * _wsign()
        m = wn > 0.5
        # the circle hand is joined to its own wrist by design (house hands): its ball inside its OWN forearm
        # within a hand's width of the wrist is the join, not a crossing
        own = (r['region'][use] == (3 if sd == 'L' else 5))
        _, ni = tree.query(S)
        join = own[ni] & (np.linalg.norm(S - out['J']['wr' + sd], axis=1) < HAND_R + HAND_OFF)
        m &= ~join
        if m.any():
            dist, _ = tree.query(S[m])
            dep = dist.max()
            if dep > TOUCH:
                hits['hand %s in body' % sd] = (int(m.sum()), round(float(dep) * 100, 1))
                out.setdefault('bad_pts', []).append(S[m])
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
    if dep > TOUCH:
        out.setdefault('bad_pts', []).append(Pg[m])
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
        over = (Q[:, 0] > DOOR_X) & (Q[:, 0] < DOOR_X + 0.07) & (Q[:, 2] > -0.95) & (Q[:, 2] < 0.80)
        if over.any():                                             # folded over the door top: resting ON it
            gap = Q[over, 1].min() - SILL
        else:                                                      # not over it: how far short of its inner face
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
            seat=(150, 128, 112), pillar=(70, 70, 76), gun=(40, 40, 44), hand=(176, 176, 176),
            gun_slide=(40, 40, 44), gun_frame=(40, 40, 44), gun_muzzle=(40, 40, 44))
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
    objs.append((Pg, Tg, gun_kinds(Tg), 'gun'))
    return objs


def gun_kinds(Tg):
    """Each pistol triangle's part (slide, frame, grip, muzzle: gun3d_film's kinds; bench_draw.GUN_PARTS)."""
    import bench_draw as BD
    import gun3d_film as GF
    if 'gun_k' not in RIG:
        _, T, K = GF.mesh(1.0)
        RIG['gun_k'] = (T, np.array([BD.GUN_PARTS[k] for k in K[T[:, 0]]]))
    T, names = RIG['gun_k']
    return names if len(T) == len(Tg) else np.array(['gun'] * len(Tg))


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


SIDE_CAMS = {   # extra views for the key sheet (car frame): beside the window outside, from the front, from above
    'outside': ((3.2, 1.25, -0.2), (0.6, 1.0, 0.0), 1500.0),
    'front': ((0.5, 1.6, 3.2), (0.55, 0.95, 0.0), 1500.0),
    'above': ((0.6, 4.2, 0.05), (0.6, 0.9, 0.0), 1300.0),
}


def draw_view(out, view, t=0.0, size=(540, 960), mark=True):
    """One view of a pose: 'shot' (shot 4's locked camera at t) or a SIDE_CAMS view (the car cut away to what
    touches him: seat, door, door top; the windscreen frame and roof left out so he can be seen). Crossing points
    (bad_pts from the checks) are marked red."""
    import bench_draw as BD
    import sets as S
    from PIL import Image, ImageDraw
    if view == 'shot':
        cam = cam_at(t, shake=False)
        objs = scene(out)
    else:
        p, a, f = SIDE_CAMS[view]
        cam = S.Cam(p, a, f)
        keep = ('seat', 'door', 'dash')
        objs = [o for o in scene(out) if o[3] in ('jason', 'gun') or o[3].startswith('hand') or
                any(o[3].startswith(k) for k in keep)]
        if view == 'outside':
            objs = [o for o in objs if not (o[3].startswith('door') and 'rear' not in o[3])]
    zb, pb, ob, names = BD.raster(cam, objs, 1)
    edge = BD.ink(zb, pb, ob, 3)
    img = np.zeros(zb.shape + (3,), np.uint8)
    img[:] = SKY
    for i, n in enumerate(BD.PART_NAMES):
        img[pb == i] = GREY[n]
    img[edge] = BD.INK
    im = Image.fromarray(img)
    if mark and out.get('bad_pts'):
        Q = np.concatenate(out['bad_pts'])
        xy, z = BD._proj(cam, Q)
        d = ImageDraw.Draw(im)
        for (x, y), zz in zip(xy, z):
            if zz > cam.NEAR:
                d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(230, 30, 30))
    return im.resize(size, Image.LANCZOS)


def key_sheet(path, names=('K1', 'K2', 'K3', 'K4', 'K5'), views=('shot', 'outside', 'front', 'above'), w=300):
    """Each key pose from shot 4's camera and three other sides, its check results written under each row."""
    from PIL import Image, ImageDraw
    fit_seat()
    fit_knee()
    fit_ankles()
    T = dict((k, t) for t, k in reversed(_times()))
    h = int(w * 16 / 9)
    sheet = Image.new('RGB', (w * len(views), (h + 60) * len(names)), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    for ri, k in enumerate(names):
        g = key(k)
        o = solve(g)
        c = check_frame(o, g)
        for ci, v in enumerate(views):
            sheet.paste(draw_view(o, v, T.get(k, 0.0), (w, h)), (ci * w, ri * (h + 60)))
        txt = '%s  %s' % (k, '; '.join('%s %s' % (n, v) for kk in ('car', 'self', 'pistol', 'rom') for n, v in c[kk].items()) or 'clean')
        cs = ' '.join('%s %s' % (n, v) for n, v in c['contacts'].items())
        for li, line in enumerate([txt[i:i + 150] for i in range(0, len(txt), 150)][:2] + [cs[:150]]):
            d.text((6, ri * (h + 60) + h + 4 + li * 16), line, fill=(0, 0, 0))
    sheet.save(path, quality=88)
    return path


# ---------------------------------------------------------------------------------------------------- run
def frame_times():
    T = _times()
    n = int(round(T[-1][0] * FPS)) + 1
    return [i / FPS for i in range(n)]


def run(out_dir, draw_frames=True, every=1, span=None, side=False):
    """span=(t0, t1) seconds: only those frames (a part clip; frames numbered from 0 so clip() can read them).
    A progress line every 12 frames (frame, seconds so far, minutes left)."""
    os.makedirs(os.path.join(out_dir, 'frames'), exist_ok=True)
    fit_seat()
    fit_knee()
    fit_ankles()
    rows, track, fails, outs = [], [], [], []
    aims = []
    t0 = time.time()
    ts = frame_times()
    if span:
        ts = [t for t in ts if span[0] - 1e-6 <= t <= span[1] + 1e-6]
    for i, t in enumerate(ts):
        if i and i % 12 == 0:
            el = time.time() - t0
            print('progress: frame %d of %d (%.2f s), %.0f min so far, about %.0f min left' % (
                i, len(ts), t, el / 60, el / i * (len(ts) - i) / 60), flush=True)
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
            fails.append((int(round(t * FPS)), round(t, 3), bad))
        with open(os.path.join(out_dir, 'frames.log'), 'a') as fh:      # each frame's result kept as it goes
            fh.write('%d %.3f %s %s\n' % (int(round(t * FPS)), t, bad or 'clean', c['contacts']))
        outs.append(out)
    if draw_frames:                      # every frame solved and checked first; then drawn (from the store)
        draw_all(out_dir, outs, ts, every, side)
    top, over, pops = jumps(track)
    held = contacts_held(rows)
    sl = slides(track, rows)
    rep = report(len(ts), fails, top, over, pops, held, sl, aims, time.time() - t0)
    if span:
        rep += '\n(part run %.2f-%.2f s: jumps, steps and contacts count frames from %d = film frame 0 of the part)' % (
            span[0], span[1], int(round(ts[0] * FPS)))
    open(os.path.join(out_dir, 'report.txt'), 'w').write(rep)
    print(rep)
    RUN_LAST.update(ts=ts, aims=aims, top=top, outs=outs, side=side)
    return fails, over, pops, held, sl


RUN_LAST = {}

# The frame store (speed-up step 4, chat 40): each drawn frame is filed under a fingerprint of everything that makes
# it: its solved body (every point), the camera, and the drawing code (this file minus the move and checks
# sections, bench_draw, bench_pose, sets). A fix redraws only frames whose fingerprint changed; the checks always
# run on every frame. Before frames are used, up to 10 stored ones picked at random are drawn again and must match
# pixel for pixel, else the store is wiped and everything is drawn. `keep` files the store as one lossless bundle.
STORE_TAR = os.path.join(HERE, '..', 'notes', 'bench', 'store', 'frames.tar')
STORE_MB = 20
DRAW_WORKERS = 4
_DRAW = {}


def _draw_code():
    h = hashlib.sha256()
    txt = open(os.path.abspath(__file__)).read()
    txt = txt[txt.index('"""', 4) + 3:]                 # the file's description (its MAP) is not drawing code
    mv, ck = txt.index('# ' + '-' * 100 + ' the move'), txt.index('# ' + '-' * 100 + ' solve')
    c0, c1 = txt.index('# ' + '-' * 100 + ' checks'), txt.index('# ' + '-' * 100 + ' drawing')
    h.update((txt[:mv] + txt[ck:c0] + txt[c1:]).encode())
    for f in ('bench_draw.py', 'bench_pose.py', 'sets.py'):
        h.update(open(os.path.join(HERE, f), 'rb').read())
    return h.hexdigest()


def _feed(h, x):
    if isinstance(x, np.ndarray):
        h.update(str((x.dtype, x.shape)).encode())
        h.update(np.ascontiguousarray(x).tobytes())
    elif isinstance(x, dict):
        for k in sorted(x, key=str):
            h.update(repr(k).encode())
            _feed(h, x[k])
    elif isinstance(x, (list, tuple)):
        h.update(b'[%d' % len(x))
        for v in x:
            _feed(h, v)
    elif hasattr(x, '__dict__'):
        _feed(h, vars(x))
    else:
        h.update(repr(x).encode())


def frame_key(out, t, side, code, dressed=False):
    h = hashlib.sha256(code.encode())
    _feed(h, {k: v for k, v in out.items() if k != 'bad_pts'})
    _feed(h, vars(cam_at(t)))
    h.update(b'side' if side else b'shot')
    if dressed:
        h.update(b'dressed')
    return h.hexdigest()[:24]


def _draw_frame(i):
    out, t, side = _DRAW['outs'][i], _DRAW['ts'][i], _DRAW['side']
    from PIL import Image
    if _DRAW.get('dressed'):             # stage 2: the house look, drawn at 2x and brought down (smooth edges)
        im = dressed_draw(out, t, 'shot', 2, shake=True, head_vd=_DRAW['hv'][i]).resize((540, 960), Image.LANCZOS)
    else:
        im = draw(out, cam_at(t))
    if side:                             # left: shot 4's locked camera; right: outside the window, same pose
        both = Image.new('RGB', (im.width * 2, im.height))
        both.paste(im, (0, 0))
        both.paste(dressed_draw(out, t, 'outside', 2).resize(im.size, Image.LANCZOS) if _DRAW.get('dressed') else
                   draw_view(out, 'outside', t, im.size, mark=False), (im.width, 0))
        im = both
    im.save(os.path.join(_DRAW['store'], _DRAW['keys'][i] + '.png'))
    return i


def _pool_map(fn, items):
    if DRAW_WORKERS <= 1 or len(items) < 2:
        return [fn(i) for i in items]
    import multiprocessing as mp
    with mp.get_context('fork').Pool(DRAW_WORKERS) as pool:
        return pool.map(fn, items, chunksize=1)


def draw_all(out_dir, outs, ts, every=1, side=False, dressed=False):
    """Draw (or take from the store) every `every`-th frame into OUT/frames; prints how many were drawn."""
    import random
    import shutil
    from PIL import Image
    store = os.path.join(out_dir, 'store')
    os.makedirs(store, exist_ok=True)
    fdir = os.path.join(out_dir, 'frames')
    os.makedirs(fdir, exist_ok=True)
    code = _draw_code()
    idx = list(range(0, len(ts), every))
    hv = head_plan([head_yaw(o, t) for o, t in zip(outs, ts)]) if dressed else [None] * len(ts)
    keys = {i: frame_key(outs[i], ts[i], side, code + str(hv[i]), dressed) for i in idx}
    if os.path.exists(STORE_TAR) and any(not os.path.exists(os.path.join(store, keys[i] + '.png')) for i in idx):
        import tarfile
        with tarfile.open(STORE_TAR) as tf:              # the bundle kept between chats (only PNGs by name)
            want = {keys[i] + '.png' for i in idx}
            tf.extractall(store, members=[m for m in tf.getmembers() if m.name in want and m.isfile()])
    _DRAW.update(outs=outs, ts=ts, side=side, keys=keys, store=store, dressed=dressed, hv=hv)
    have = [i for i in idx if os.path.exists(os.path.join(store, keys[i] + '.png'))]
    if have:                                             # the store's spot check: drawn again, pixel for pixel
        spot = random.sample(have, min(10, len(have)))
        old = {i: np.asarray(Image.open(os.path.join(store, keys[i] + '.png'))) for i in spot}
        _pool_map(_draw_frame, spot)
        if any(not np.array_equal(old[i], np.asarray(Image.open(os.path.join(store, keys[i] + '.png'))))
               for i in spot):
            print('frame store: a stored frame drew differently: store wiped, every frame drawn', flush=True)
            shutil.rmtree(store)
            os.makedirs(store)
            have, spot = [], []
        else:
            have = [i for i in have if i not in spot]
    else:
        spot = []
    todo = [i for i in idx if i not in have and i not in spot]
    t0 = time.time()
    _pool_map(_draw_frame, todo)
    for i in idx:
        shutil.copyfile(os.path.join(store, keys[i] + '.png'), os.path.join(fdir, 'f%04d.png' % i))
    with open(os.path.join(store, 'index.json'), 'w') as fh:
        json.dump({'%04d' % i: keys[i] for i in idx}, fh)
    print('frames: %d new (%.0f s, %d at a time), %d from the store (%d of them drawn again to check it: same)' % (
        len(todo), time.time() - t0, DRAW_WORKERS, len(have) + len(spot), len(spot)), flush=True)


def keep(out_dir):
    """File OUT's store (the frames of its last run) as the one bundle on GitHub (lossless PNGs, under 20 MB)."""
    import tarfile
    store = os.path.join(out_dir, 'store')
    names = sorted(set(json.load(open(os.path.join(store, 'index.json'))).values()))
    os.makedirs(os.path.dirname(STORE_TAR), exist_ok=True)
    tmp = STORE_TAR + '.tmp'
    with tarfile.open(tmp, 'w') as tf:
        for n in names:
            tf.add(os.path.join(store, n + '.png'), arcname=n + '.png')
    mb = os.path.getsize(tmp) / 1e6
    if mb > STORE_MB:
        os.remove(tmp)
        sys.exit('keep: %.1f MB is over %d MB; not kept' % (mb, STORE_MB))
    os.replace(tmp, STORE_TAR)
    print('kept %d frames, %.1f MB: %s' % (len(names), mb, os.path.relpath(STORE_TAR)))
SLIDE_BAR = 1.0                  # cm: a planted knee or the door hand moving more than this while planted


def checked_clip(out_dir, mp4, span=None, dressed=False):
    """The grey clip through the body check's record (humancheck.Writer), so it can go to Sam (the send guard):
    every frame's solid-body checks (car, body against itself, pistol, joint range) and the clip's own (pops, steps
    over 3 cm, planted slides, contacts) go in as faults; the flat-drawing checks in humancheck have nothing to see
    on a grey solid body (it is not drawn by views), so THESE are its body check. Side by side: shot 4's locked
    camera and outside the window. Unnamed faults hold the video aside (Writer.finish), as for any clip."""
    import humancheck as HC
    fails, over, pops, held, sl = run(out_dir, span=span, side=True, draw_frames=False)   # checks first, no drawing
    ts = RUN_LAST['ts']
    f0 = int(round(ts[0] * FPS))
    W = HC.Writer('grey test body')
    who = 'Jason (grey test body)'
    nm = {'car': 'car', 'self': 'self', 'pistol': 'pistol', 'rom': 'range'}
    for fr, t, bad in fails:
        W.frame(t, [(t, who, nm[k], '%s %s' % (nm[k], ', '.join('%s %s cm' % (a, b[1]) if isinstance(b, tuple) else
                                                                      '%s %s' % (a, b) for a, b in v.items())))
                    for k, v in bad.items()])
    for i, j, cm in pops:
        t = ts[min(i, len(ts) - 1)]
        W.frame(t, [(t, who, 'pop', 'pop: %s jumps off its path (%.1f cm)' % (j, cm))])
    for i, j, cm in over:
        t = ts[min(i, len(ts) - 1)]
        W.frame(t, [(t, who, 'step', 'step over 3 cm a frame: %s (%.1f cm)' % (j, cm))])
    for k, v in sl.items():
        if v > SLIDE_BAR:
            W.frame(ts[0], [(ts[0], who, 'slide', 'planted slide: %s %.1f cm' % (k, v))])
    for f, k, gap in held:
        t = ts[min(f, len(ts) - 1)]
        W.frame(t, [(t, who, 'contact', 'contact: %s gap %.1f cm' % (k, gap))])
    lines = W.lines()                    # the checks-first lock (speed-up step 3): nothing is drawn while a fault
    fh = hashlib.sha256('\n'.join(lines).encode()).hexdigest()[:16]     # is neither fixed nor named
    json.dump(dict(hash=fh, faults=lines), open(os.path.join(out_dir, 'faults.json'), 'w'), indent=1)
    named = _named(out_dir).get(fh) if lines else None
    if lines and not named:
        print('\n'.join(lines), flush=True)
        sys.exit('checks first: %d fault(s) above, NOTHING drawn. Fix them and run again, or name every one: '
                 'python3 source/bench_move.py name %s "why"' % (len(lines), out_dir))
    draw_all(out_dir, RUN_LAST['outs'], ts, 1, side=True, dressed=dressed)
    size = clip(out_dir, mp4)
    print('clip %s: %.0f KB, film frames %d-%d' % (mp4, size / 1024, f0, f0 + len(ts) - 1), flush=True)
    if named:
        print('faults named: %s' % named, flush=True)
    _np = os.path.join(os.path.dirname(HERE), 'notes', 'grand-theft-autism.md')   # named-lines: lines answered there
    W.finish(mp4, named=bool(named), notes=open(_np).read() if os.path.exists(_np) else '')


def _named(out_dir):
    try:
        return json.load(open(os.path.join(out_dir, 'named.json')))
    except (OSError, ValueError):
        return {}


def name_faults(out_dir, why):
    """Name the faults of OUT's last check pass (faults.json) so the clip may be drawn; a new fault list needs a new
    name (the name is filed under the list's fingerprint)."""
    f = json.load(open(os.path.join(out_dir, 'faults.json')))
    d = _named(out_dir)
    d[f['hash']] = why
    json.dump(d, open(os.path.join(out_dir, 'named.json'), 'w'), indent=1)
    print('named %d fault(s): %s' % (len(f['faults']), why))


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


def _old_out(k):
    """An old skeleton pose (leanout's house skeleton) with the solid body posed on it the old way
    (bench_pose.posed), the old pistol and the old hand balls, as an `out` the checks read."""
    import bench_draw as BD
    r = rig()
    P, T, part, bone, keep = BP.posed(k)
    J = {n: np.asarray(k[n], float) for n in ('pelvis', 'neck', 'head', 'shL', 'shR', 'elL', 'elR', 'wrL', 'wrR',
                                               'hipL', 'hipR', 'knL', 'knR', 'anL', 'anR')}
    balls = {sd: c for sd, (c, rad) in zip('LR', BD.hand_balls(k, None))}
    Pg, Tg = BD.gun_mesh(k)
    return dict(P=P, J=J, balls=balls, gun=(Pg, Tg), aim=_u(getattr(k, 'aim', [0, 0, -1])))


def proof(out_dir):
    """Every check first run on the OLD failed poses (learn-step.md's pass list): chat 33's still (the seated K1
    through bench_pose: the seat 7.4 cm and the pistol 4.8 cm must show) and the old move (leanout.at) at each
    key's time, the body posed on it the old way; then the old move's 197 frames for jumps and the door hand."""
    import gta_cast as GC
    import leanout as LO
    os.makedirs(out_dir, exist_ok=True)
    sp = dict(GC.cast()['jason'], mood='stern')
    L = ['Proof: the stage-1 checks on the OLD failed poses (they must catch the old faults)']
    cases = [('chat 33 still (seated K1)', LO.seated(sp))]
    T = dict((k, t) for t, k in reversed(_times()))
    for nm in ('K1', 'K2', 'K3', 'K4', 'K5'):
        cases.append(('old move %s (%.2f s)' % (nm, T[nm]), LO.at(T[nm], sp)))
    for nm, k in cases:
        o = _old_out(k)
        c = dict(car=car(o), gun_car=gun_car(o), self=self_cross(o), pistol=pistol(o))
        bad = {}
        for sd in 'LR':
            J = o['J']
            a = math.degrees(math.acos(np.clip(np.dot(_u(J['el' + sd] - J['sh' + sd]), _u(J['wr' + sd] - J['el' + sd])), -1, 1)))
            if a > ROM['elbow'][1]:
                bad['elbow ' + sd] = round(a)
        firing = nm.startswith('old move K4') or nm.startswith('old move K5')
        aim = ('aim %.2f m off' % aim_err(o)) if firing else ''
        hand = 'door hand gap %.1f cm' % ((o['balls']['L'][1] - HAND_R - SILL) * 100)
        L.append('%-30s car %s | pistol-car %s | self %s | pistol %s | range %s | %s %s' % (
            nm, c['car'] or 0, c['gun_car'] or 0, c['self'] or 0, c['pistol'] or 0, bad or 0, aim, hand))
        if nm.startswith('chat 33'):
            draw_view(o, 'outside', 0.0, (540, 960)).save(os.path.join(out_dir, 'proof-still.png'))
    track = [{n: np.asarray(LO.at(t, sp)[n], float) for n in TRACK} for t in frame_times()]
    top, over, pops = jumps(track)
    L.append('old move, 197 frames: sudden jumps (pops) %d, e.g. %s; steps over 3 cm %d' % (len(pops), pops[:4], len(over)))
    rep = '\n'.join(L)
    open(os.path.join(out_dir, 'proof.txt'), 'w').write(rep)
    print(rep)
    return rep


def house_pose(out):
    """A leanout-style pose (lying.Body) from a solved frame, for the house head drawing (lying_flat via
    bench_draw.house_head): joints from out['J'], the head's centre and the neck point placed as chat 33's seated
    still places them (their offsets measured once on K1, in the head's and chest's own frames)."""
    import copy
    r = rig()
    if 'hp_off' not in RIG:
        o1 = _solve(key('K1'), fold=False)
        k1 = r['k1']
        RIG['hp_off'] = (o1['Rh'].T @ (np.asarray(k1['head']) - o1['J']['head']),
                         o1['Rc'].T @ (np.asarray(k1['neck']) - o1['J']['neck']))
    dh, dn = RIG['hp_off']
    J, Rc, Rh = out['J'], out['Rc'], out['Rh']
    k = copy.deepcopy(r['k1'])
    for n in ('shL', 'elL', 'wrL', 'shR', 'elR', 'wrR', 'hipL', 'knL', 'anL', 'hipR', 'knR', 'anR'):
        k[n] = np.asarray(J[n], float)
    k['pelvis'] = np.asarray(J['pelvis'], float)
    k['neck'] = J['neck'] + Rc @ dn
    k['head'] = J['head'] + Rh @ dh
    k['waist'] = k['pelvis'] + 0.465 * (k['neck'] - k['pelvis'])
    k['fwd'], k['hup'], k['hfwd'] = Rc[:, 2], Rh[:, 1], Rh[:, 2]
    for sd in 'LR':
        k['toe' + sd] = _u(J['an' + sd] - J['kn' + sd])
        k['sup' + sd] = _u(np.cross(k['toe' + sd], np.cross([0, 1.0, 0], k['toe' + sd])) + 1e-9)
    k.aim, k.firing = np.asarray(out['aim'], float), True
    return k


FILM_CAR_HIDES = [False]   # the film (jason3d_film): the bench's stand-in car hides nothing; the film's own drawn
#   car hides him afterwards (Sam, v5 notes 1-2: the stand-in's dash and door did not line up with the film's car)
DRESS_HIDE_NECK = True          # a smooth solid neck column (neck_column) stands in for the skinned neck


def clean_parts(pb, ob, rad):
    """Sam (22 Nov, K4 still, marked crop of the vest strap): the vest's edges were torn, with skin slivers between
    pieces, where the fold press flattened the shoulder skin (the rest-body map deciding vest or skin crumples there).
    A flat drawing's colour areas have clean edges: each of Jason's dots takes the part most of its neighbours within
    rad have (skin, vest, trousers, shoes; his dots only), so slivers thinner than rad go and edges run smooth. The
    ink is drawn after, from these parts."""
    from scipy import ndimage
    body = ob == 0
    kinds = [PI for PI in range(5)]                       # bench_draw.PART_NAMES 0-4: skin vest trousers shoes hair
    votes = np.stack([ndimage.uniform_filter(((pb == k) & body).astype(np.float32), 2 * rad + 1) for k in kinds])
    best = np.array(kinds)[votes.argmax(0)]
    out = pb.copy()
    m = body & np.isin(pb, kinds)
    out[m] = best[m]
    return out


NECK_R = (0.060, 0.052)          # the neck column's radius at its base and under the head (Jason's neck: 6.6 cm
#                                  median skin radius at rest, trapezius included)


def neck_column(out, n_ring=24, n_len=10):
    """Sam (22 Nov, K4 still, two marked crops: "Fix to human standard neck"): the skinned neck under the house head
    was an open tube once the 3D head was hidden (inner edges inked, the vest seen through it) and the flat neck's
    outline drew a line down it. A human neck is one smooth closed column from the shoulders up into the head:
    here a tube along neck base -> neck joint -> head joint -> into the head, bending as the neck does (chest frame
    at the base, head frame at the top), its base sunk into the trunk. Returns (points, tris) to join Jason's body."""
    J, Rc, Rh = out['J'], out['Rc'], out['Rh']
    ctrl = [J['neck'] - Rc[:, 1] * 0.05, J['neck'], J['head'], J['head'] + Rh[:, 1] * 0.06]
    pts, frames = [], []
    for i in range(n_len + 1):                          # a smooth path through the four points (Catmull-Rom)
        u = i / n_len * 3
        k = min(int(u), 2)
        f = u - k
        p0, p1, p2, p3 = (ctrl[max(k - 1, 0)], ctrl[k], ctrl[k + 1], ctrl[min(k + 2, 3)])
        p = 0.5 * ((2 * p1) + (-p0 + p2) * f + (2 * p0 - 5 * p1 + 4 * p2 - p3) * f * f + (-p0 + 3 * p1 - 3 * p2 + p3) * f ** 3)
        pts.append(p)
    pts = np.array(pts)
    V, T = [], []
    for i, p in enumerate(pts):
        a = _u(pts[min(i + 1, n_len)] - pts[max(i - 1, 0)])
        w = i / n_len
        fwd = _u((1 - w) * Rc[:, 2] + w * Rh[:, 2])
        x = _u(np.cross(a, fwd))
        y = np.cross(x, a)
        rad = NECK_R[0] + (NECK_R[1] - NECK_R[0]) * min(1.0, w * 1.5)
        for j in range(n_ring):
            th = 2 * math.pi * j / n_ring
            V.append(p + rad * (math.cos(th) * x + 0.92 * math.sin(th) * y))   # a little deeper side to side
    for i in range(n_len):
        for j in range(n_ring):
            a0, a1 = i * n_ring + j, i * n_ring + (j + 1) % n_ring
            b0, b1 = a0 + n_ring, a1 + n_ring
            T += [(a0, b0, a1), (a1, b0, b1)]
    c0, c1 = len(V), len(V) + 1
    V += [pts[0], pts[-1]]
    for j in range(n_ring):
        T.append((c0, (j + 1) % n_ring, j))
        T.append((c1, n_len * n_ring + j, n_len * n_ring + (j + 1) % n_ring))
    return np.array(V), np.array(T, int)


def dressed_still(path, name='K4', t=1.95, scale=2):
    """Rough early look (Sam's Y, chat 36): one solved key pose dressed as Jason in the house look through shot
    4's locked camera at t (dressed_draw), and the same pose from outside the window (path -outside.png). Prints
    the checks on the pose."""
    fit_seat(); fit_knee(); fit_ankles()
    g = key(name)
    out = solve(g)
    c = check_frame(out, g)
    res = []
    for view in ('shot', 'outside'):
        img = dressed_draw(out, t, view, scale)
        img.save(path if view == 'shot' else path.replace('.png', '-outside.png'))
        res.append(img)
    bad = {kk: v for kk, v in c.items() if kk in ('car', 'self', 'pistol', 'rom') and v}
    print('dressed still %s at %.2f s: checks %s' % (name, t, bad or 'clean'), flush=True)
    return res


def dressed_draw(out, t, view='shot', scale=2, shake=False, head_vd=None, cam=None, xf=None, face=None, car=None,
                 layer=False, depth_car=None):
    """One solved pose dressed as Jason in the house look (stage 2, chat 44: the still's drawing made a frame
    drawer, so the dressed clip and the still are drawn by the same code): house colours by body part (bench_pose
    part_at), house ink, the house head drawing laid at the head's depth, circle hands, the pistol, the smooth neck
    column. view 'shot' = shot 4's locked camera at t; 'outside' = beside the window (front door cut away).
    Returns a PIL image at the camera's size x scale.
    In the film (jason3d_film, chat 46): cam = the film's camera, xf = car frame -> world (the moving Tulip, car its
    gta_cars car), face = the head's acting keys, layer=True: only his own dots (body, hands, pistol, the ink round
    them) on a clear layer; the car solids still hide him by depth. depth_car: the film's car hides him dot by dot
    (depth_cut, chat 50)."""
    import bench_draw as BD
    r = rig()
    sp = dict(dict(r['sp'], mood='stern', squint=0.35, frown=0.07), **(face or {}))
    tk = r['tk']
    neckb = np.array([str(b).startswith('neck') for b in r['bone']])
    # only the neck itself is hidden (rest |x| under 0.62 dm; 0.68 left an ink blot at the join): the shoulder tops
    # out to |x| 1.4 are tied to the neck bones too, and hiding them cut a hole across each vest strap, so the
    # strap's front piece read as an island (Sam, K4 still, 22 Nov; found chat 44)
    neckb &= np.abs(BP._REST['v'][:, 0]) < float(os.environ.get('NECK_HIDE_X', 0.62))
    hide = r['headb'] | (neckb & DRESS_HIDE_NECK)
    # a triangle touching the hidden neck at all goes (its scraps poked through the neck column as a hooked line
    # at the throat, chat 38); the column's base, sunk into the trunk, covers the opening
    tk = tk[~(r['hand'][tk].any(1) | (hide[tk].any(1) if DRESS_HIDE_NECK else hide[tk].all(1)))]
    rv, rg = BP.rest_attrs()
    attrs = np.concatenate([rv, rg], 1)
    Pj = out['P']
    if DRESS_HIDE_NECK:                  # the smooth neck column joins his body (one object: no line where it meets)
        Vn, Tn = neck_column(out)
        # body skin INSIDE the column (the upper chest round the neck's base, the throat) is under the neck's skin:
        # left drawn, its edges poked through the column as a hooked line at the throat (chat 38)
        a0, a1 = out['J']['neck'] - out['Rc'][:, 1] * 0.05, out['J']['head']
        ax_ = _u(a1 - a0)
        d_ = Pj - a0
        al = d_ @ ax_
        rr = np.linalg.norm(d_ - np.outer(al, ax_), axis=1)
        inside_col = (al > 0.0) & (al < np.linalg.norm(a1 - a0) + 0.06) & (rr < NECK_R[1] * 0.98)
        tk = tk[~inside_col[tk].all(1)]
        # the chest and trapezius skin ABOVE the neck's base flows onto the neck (a lip of it stood in front of the
        # column at the throat, its edge inked as a hooked line, chat 38): those points go to just under its skin
        # chat 44: the pull fades in (over 4 cm up from the column's base and 8-12 cm out from its axis) and takes in
        # the shoulder-top skin tied to the neck bones (now drawn): pulled all-or-nothing, the skin left a ledge at
        # the front of the throat, inked as a scribble in every side view
        tgt = NECK_R[1] * 0.97
        def _ss(x):
            x = np.clip(x, 0, 1)
            return x * x * (3 - 2 * x)
        f = _ss(al / 0.04) * (1 - _ss((rr - 0.08) / 0.04)) * (al < np.linalg.norm(a1 - a0))
        lip = np.isin(r['region'], (1, 10)) & (rr > tgt) & (f > 0)
        if lip.any():
            radial = (d_ - np.outer(al, ax_))[lip]
            nr = rr[lip] + (tgt - rr[lip]) * f[lip]
            Pj = Pj.copy()
            Pj[lip] = a0 + np.outer(al[lip], ax_) + radial / rr[lip][:, None] * nr[:, None]
        ni = np.where(neckb & r['keep'])[0]
        src = ni[np.argmin(np.linalg.norm(Pj[ni] - out['J']['neck'], axis=1))]   # its colour: a neck skin point's
        tk = np.concatenate([tk, Tn + len(Pj)])
        attrs = np.concatenate([attrs, np.repeat(attrs[src][None], len(Vn), 0)])
        Pj = np.concatenate([Pj, Vn])
    tp = np.array(['skin'] * len(tk))    # Jason's colours come per dot from part_at (attrs), not per triangle
    objs = [(Pj, tk, tp, 'jason')] + scene(out)[1:]
    if FILM_CAR_HIDES[0] and layer:
        objs = [o for o in objs if o[3] == 'jason' or o[3].startswith('hand') or o[3] == 'gun']
    if xf is not None:
        objs = [(xf(P_), T_, tp_, nm_) for P_, T_, tp_, nm_ in objs]
        if DRESS_HIDE_NECK:
            Vn = xf(Vn)
    if cam is not None:
        ob_ = objs
    elif view == 'shot':
        cam = cam_at(t, shake=shake)
        ob_ = objs
    else:
        import sets as S
        cam = S.Cam(*SIDE_CAMS[view])
        ob_ = [o for o in objs if not (o[3].startswith('door') and 'rear' not in o[3])]
    zb, pb, ob, names = BD.raster(cam, ob_, scale, attrs)
    free = None
    if DRESS_HIDE_NECK:                  # where the neck column is the nearest thing, it never hides the head
        zn = BD.raster(cam, [(Vn, Tn, np.array(['skin'] * len(Tn)), 'neck')], scale)[0]   # drawing (Sam, 23 Nov)
        free = np.isfinite(zn) & (zn <= zb + 1e-6)
    # chat 46: the clean-up reaches 1.8 cm on the body, however near the camera (shot 6's close two-shot: the
    # strap's edge at the raised arm's shoulder zig-zagged 2 cm; 9 dots is ~1 cm there, ~4 cm far off in shot 4)
    chest = (out['J']['neck'] + out['J']['pelvis']) / 2
    if xf is not None:
        chest = xf(chest[None])[0]
    kk = cam.project(tuple(float(c) for c in chest))[1]
    pb = clean_parts(pb, ob, max(9 * scale // 2, int(0.018 * kk * scale)))
    edge = BD.ink(zb, pb, ob, 3 * scale)
    from scipy import ndimage                    # ink specks too small to be a line (left at the throat, chat 38)
    lab, nl = ndimage.label(edge)
    if nl:
        sz = ndimage.sum(edge, lab, range(1, nl + 1))
        edge &= ~np.isin(lab, np.where(sz < 60 * scale * scale)[0] + 1)
    if layer:                            # his own dots and the ink within a line's width of them
        mine = np.isin(ob, [i for i, n in enumerate(names) if n == 'jason' or n.startswith('hand') or n == 'gun'])
        near = ndimage.binary_dilation(mine, iterations=3 * scale)
        pb = np.where(mine, pb, -1)
        edge = edge & near
    img = BD.compose(zb, pb, ob, names, edge, BD.colours(sp), scale)
    if not layer:
        bg = Image.new('RGBA', img.size, SKY + (255,))
        bg.alpha_composite(img)
        img = bg
    k = house_pose(out)
    if xf is not None:
        import leanout as _L
        k = _L.to_world(k, car)
        k.aim, k.firing = _u(xf(np.asarray(out['aim'], float)[None] + out['J']['wrR'][None])[0] - xf(out['J']['wrR'][None])[0]), True
    import lying_flat as LF
    LF.HEAD_VD[0] = head_vd
    try:
        head, _ = BD.house_head(cam, k, sp, neck=not DRESS_HIDE_NECK)
    finally:
        LF.HEAD_VD[0] = None
    hd = cam.depth(tuple(k['head']))
    a_before = np.asarray(img.split()[3]).copy() if (layer and depth_car is not None) else None
    rgb_before = np.asarray(img.convert('RGB')).copy() if a_before is not None else None
    BD.lay_head(img, head, zb, hd, scale, free)
    if a_before is not None:             # GTA v5 notes 2/8/9: the film's car hides him dot by dot (depth_cut)
        headm = np.any(np.asarray(img.convert('RGB')) != rgb_before, 2) | ((np.asarray(img.split()[3]) > 0) & (a_before == 0))
        img = depth_cut(img, zb, ob, names, cam, depth_car, scale, headm, hd, pb)
    return img if layer else img.convert('RGB')


def depth_cut(img, zb, ob, names, cam, car, scale, headm, hd, pb=None, tol=0.01):
    """Per dot, his layer is rubbed out where the film car's solid (gta_cars.solid_depth: its sides, bevels, the door
    tops beside the cabin, bonnet, boot, roof, pillars, parts; the windows are holes) is nearer the lens than he is.
    Sam, GTA v5 notes 2/8/9: "Make sure you don't see green trousers below that black line, just red or black car
    parts"; his hips still show through the open window, where nothing is in front of them. His body dots use their
    own depth, the head drawing the head's, the ink round him the nearest of his dots within a line's width. The car's
    edges are widened by half its outline so its line is drawn over him, never half under him.
    Sam (23 Nov, chat 50, his belly drawn over the black strip under the window: "Other side of the door please"):
    the door is solid up to the window's bottom edge. His clothed body (vest, shorts, shoes) found inside that door
    (beside the cabin, out from the window's plane, below its bottom edge) is on the other side of it: hidden. His
    bare arm draped over the door top stays (it lies over the door, it does not pass through it)."""
    import gta_cars as G
    from scipy import ndimage
    zc = G.solid_depth(car, cam, scale, grow=1.1 * scale)
    mine = np.isin(ob, [i for i, n in enumerate(names) if n == 'jason' or n.startswith('hand') or n == 'gun'])
    zj = np.where(mine, zb, np.inf)
    a = np.asarray(img.split()[3]).astype(np.float32)        # the layer is at the canvas; the depths at x scale
    up = lambda m: np.repeat(np.repeat(m, scale, 0), scale, 1)[:zb.shape[0], :zb.shape[1]]
    ah = up(a) > 0
    hm = up(headm)
    zt = zj.copy()
    rest = ah & ~mine
    if rest.any():
        near = ndimage.grey_erosion(zj, size=(6 * scale + 1, 6 * scale + 1))
        zt[rest] = near[rest]
    zt[hm] = hd
    zt[ah & ~np.isfinite(zt)] = hd
    hidden = ah & (zc < zt - tol)
    if pb is not None:
        hidden |= in_door(car, cam, zb, pb, scale) & ah
    frac = hidden.reshape(hidden.shape[0] // scale, scale, hidden.shape[1] // scale, scale).mean((1, 3))
    DEPTH_LAST[0] = dict(hidden=int((frac > 0.5).sum()), shown=int(((a > 0) & (frac <= 0.5)).sum()))
    a = a * (1 - frac)
    img.putalpha(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))
    return img


DEPTH_LAST = [None]


def in_door(car, cam, zb, pb, scale):
    """His clothed dots (vest, its print, shorts, shoes) that lie inside the car's near door: out from the house's
    side plane, inside the body's skin, below the side window's bottom edge, along the cabin (chat 50, Sam's note
    "Other side of the door please")."""
    import bench_draw as BD
    import gta_cars as G
    cloth = np.isin(pb, [i for i, n in enumerate(BD.PART_NAMES) if n in ('vest', 'trousers', 'shoes') or n.startswith('print')])
    cloth &= np.isfinite(zb)
    out = np.zeros(zb.shape, bool)
    if not cloth.any():
        return out
    yy, xx = np.nonzero(cloth)
    cr, sr = math.cos(cam.roll or 0.0), math.sin(cam.roll or 0.0)
    X = (xx + 0.5) / scale - 540 - cam.shake[0]
    Y = (yy + 0.5) / scale - 960 - cam.shake[1]
    Xu, Yu = X * cr + Y * sr, -X * sr + Y * cr
    f_, r_, u_ = (np.asarray(v, float) for v in (cam.f, cam.r, cam.u))
    z = zb[yy, xx]
    Pw = np.asarray(cam.pos, float)[None] + z[:, None] * (f_[None] + np.outer(Xu / cam.focal, r_) - np.outer(Yu / cam.focal, u_))
    o = np.asarray(car.body_pt((0.0, 0.0, 0.0)), float)
    M = np.stack([np.asarray(car.body_pt(tuple(e)), float) - o for e in np.eye(3)], 1)
    L = np.linalg.solve(M, (Pw - o).T).T                       # car frame: x across, y up, z along
    h = car.spec['house']
    (zb0, zb1), (wb, wr), (yb, yr) = h['base'], h['hw'], h['y']
    ywin = yb + 0.10 * (yr - yb)                               # the side window's bottom edge (gta_cars house decals)
    v = np.clip((L[:, 1] - yb) / (yr - yb), 0, 1)
    plane = wb + (wr - wb) * v
    hw = np.array([G.half_w(car, zz) for zz in L[:, 2]])
    # his shorts and shoes never pass the door at all (Sam, 23 Nov: "Little bit of trouser showing there", a sliver
    # of shorts out through the door's skin on its top edge; v5 note 7, "lower body and legs are on the wrong side of
    # the door"): out from the window's plane below its bottom edge they are hidden however far out. The vest only
    # inside the door (it may hang over the outside). 1.5 cm inside the plane too: the depth test's own slack.
    legs = np.isin(pb[yy, xx], [i for i, n in enumerate(BD.PART_NAMES) if n in ('trousers', 'shoes')])
    inside = (np.abs(L[:, 0]) > plane - 0.015) & ((np.abs(L[:, 0]) < hw + 0.02) | legs) & (L[:, 1] < ywin) & \
        (L[:, 2] > zb0) & (L[:, 2] < zb1)
    # critic r50-p1 / Sam's note 14 (shot 5, 25.6 s, "a white speck and stray tick marks on the bonnet"): his shorts'
    # hems and shoes, the legs stretched out past the dash, came up through the bonnet's top. Legs are in the
    # footwell: nothing of them forward of the windscreen's foot is ever seen (it is inside the bonnet).
    inside |= legs & (L[:, 2] > zb1 - 0.02)
    out[yy[inside], xx[inside]] = True
    return out


def head_yaw(out, t):
    """How far round the head is from shot 4's camera at t (0 = facing us, 90 = profile, 180 = away)."""
    import lying_flat as LF
    k = house_pose(out)
    hup, hfwd = LF._unit(k['hup']), LF._unit(k['hfwd'])
    d = LF._unit(np.asarray(cam_at(t).pos, float) - k['head'])
    return LF.yaw_seen(d, LF._unit(np.cross(hup, hfwd)), hfwd)


VIEWS_DEG = (0, 45, 90, 135, 180)
HEAD_BOUNDS = (22.5, 60.0, 112.5, 157.5)    # front | three | side | three_back | back; three->side at 60, not 67.5:
HEAD_MIN_RUN = 8                            # a head looking past 60 reads as profile (Sam, 23 Nov: 'a bit jarring')


def head_plan(yaws):
    """The drawn head view per frame for a whole clip (Sam, 23 Nov, 'head turn at 2 s a bit jarring': the head
    sat at 57-69 degrees, on the three/side line, so the drawing went side, three, side in half a second). Each
    frame takes its view by HEAD_BOUNDS; a view held fewer than HEAD_MIN_RUN frames between two runs of the same
    view is folded into them (no there-and-back); each remaining switch moves to the frame, between the last frame
    of the old view's own range and the first of the new one's, where the head turns fastest (the drawing changes
    inside the motion, never on a still head)."""
    vs = sorted(VIEWS_DEG)
    y = np.abs(np.asarray(yaws, float))
    raw = [vs[int(np.searchsorted(HEAD_BOUNDS, v))] for v in y]
    runs = []
    for v in raw:
        if runs and runs[-1][0] == v:
            runs[-1][1] += 1
        else:
            runs.append([v, 1])
    changed = True
    while changed:
        changed = False
        for i in range(1, len(runs) - 1):
            if runs[i][1] < HEAD_MIN_RUN and runs[i - 1][0] == runs[i + 1][0]:
                runs[i - 1][1] += runs[i][1] + runs[i + 1][1]
                del runs[i:i + 2]
                changed = True
                break
    plan = sum([[v] * n for v, n in runs], [])
    sp = np.abs(np.gradient(y))
    i0 = 0
    for j in range(len(runs) - 1):
        a, b = runs[j][0], runs[j + 1][0]
        sw = i0 + runs[j][1]
        lo, hi = sw, sw
        while lo > i0 and raw[lo - 1] != a:        # the stretch where the head is between the two views
            lo -= 1
        while hi < sw + runs[j + 1][1] - 1 and raw[hi] != b:
            hi += 1
        best = lo + int(np.argmax(sp[lo:hi + 1]))
        for f in range(lo, hi + 1):
            plan[f] = a if f < best else b
        i0 = sw
    return plan


def clip(out_dir, mp4):
    import subprocess
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(out_dir, 'frames', 'f%04d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '23', '-movflags', '+faststart', mp4], check=True)
    return os.path.getsize(mp4)


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
