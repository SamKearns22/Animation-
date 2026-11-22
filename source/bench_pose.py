#!/usr/bin/env python3
"""MAP  bench_pose: the test bench's solid Jason (learn step L2 of proposal solid-body-moves, chat 33). The measured
MakeHuman body (Jason's build, hand3d_film.MAN) posed onto any house skeleton (lying.Body, metres, the car's frame)
by its own skin weights, as ONE closed body: every bone of the house skeleton aims the matching MakeHuman bones, the
skin follows by the weights (no separate pieces, so nothing can open at a join). Each skin point is labelled with the
part it belongs to (skin, vest, trousers, shoes, hair) for the house colours, and with its bone for the checks.

  jason_mesh() ........ Jason's rest body (metres), triangles, the skeleton, each point's part
  posed(k) ............ the body posed on house skeleton k, in the car's frame (x across, y up, z forward): points,
                        triangles (wound for the car's left-handed frame), parts, the joints used
  car_window() ........ the test space's car: the passenger door with the open front window, the windscreen frame,
                        the roof, the seat, the dash and bonnet line (boxes from gta_cars' Tulip numbers)
  write_obj(path, ..) . for Blender

    python3 source/bench_pose.py OUT_DIR      writes jason.obj, car.obj, parts.json (the K1 seated pose)
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mhuman as H        # noqa: E402

MAN = dict(gender=1.0, age=0.5, muscle=0.75, weight=0.55, height=0.6, proportions=0.6)   # = hand3d_film.MAN
PARTS = ['skin', 'vest', 'trousers', 'shoes', 'hair']
# house bone (from joint, to joint) -> the MakeHuman bones it aims (side letter: the house's R is Jason's right)
CHAIN = [('spine05 spine04 spine03 spine02 spine01', 'pelvis', 'neck'),
         ('neck01 neck02 neck03 head', 'neck', 'head'),
         ('upperarm01.{S} upperarm02.{S}', 'sh{s}', 'el{s}'),
         ('lowerarm01.{S} lowerarm02.{S} wrist.{S}', 'el{s}', 'wr{s}'),
         ('upperleg01.{S} upperleg02.{S}', 'hip{s}', 'kn{s}'),
         ('lowerleg01.{S} lowerleg02.{S}', 'kn{s}', 'an{s}')]


def _u(a):
    a = np.asarray(a, float)
    return a / (np.linalg.norm(a) + 1e-12)


def _align(a, b):
    """The shortest rotation taking direction a to direction b."""
    a, b = _u(a), _u(b)
    v, c = np.cross(a, b), float(np.dot(a, b))
    if c < -0.9999:
        p = _u(np.cross(a, [1, 0, 0] if abs(a[0]) < 0.9 else [0, 1, 0]))
        return 2 * np.outer(p, p) - np.eye(3)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx / (1 + c)


_REST = {}


def jason_mesh():
    if _REST:
        return _REST['v']
    v, g = H.load_base()
    H.apply_macros(v, H.macro_values(**MAN))
    sk = H.Skeleton(v)
    faces = [f for f in g['body']]
    used = sorted({i for f in faces for i in f})
    tris = []
    for f in faces:
        tris.append((f[0], f[1], f[2]))
        if len(f) == 4:
            tris.append((f[0], f[2], f[3]))
    # each point's strongest bone
    best, bw = np.full(len(v), '', object), np.zeros(len(v))
    for b, (idx, w) in sk.weights.items():
        m = w > bw[idx]
        best[idx[m]], bw[idx[m]] = b, w[m]
    _REST.update(v=v, tris=np.array(tris, int), sk=sk, bone=best, used=np.array(used))
    _REST['part'] = _parts(v, best, sk)
    grp = np.zeros((len(v), len(GROUPS)))
    for b, (idx, w) in sk.weights.items():
        grp[idx, _group(b)] += w
    _REST['grp'] = grp / np.maximum(grp.sum(1, keepdims=True), 1e-9)
    return v


GROUPS = ['trunk', 'arm', 'leg', 'head', 'foot']


def _group(b):
    if b.startswith(('upperarm', 'lowerarm', 'wrist', 'finger', 'metacarpal', 'thumb')):
        return 1
    if b.startswith(('upperleg', 'lowerleg')):
        return 2
    if b.startswith(('foot', 'toe')):
        return 4
    if b.startswith(('spine', 'breast', 'pelvis', 'clavicle', 'shoulder', 'root')):
        return 0
    return 3


def part_at(rest, grp):
    """The house clothes decided per dot from its rest-body point (rest: (N,3) MakeHuman decimetres) and its bone
    group (grp: (N,5) shares): clean edges wherever the picture cuts them (per triangle they came out ragged)."""
    x, y, z = rest[:, 0], rest[:, 1], rest[:, 2]
    ax = np.abs(x)
    g = grp.argmax(1)
    part = np.zeros(len(rest), int)
    # trunk by the rest body's SHAPE as well as its bones: inside the shoulder line (|x| < 1.45) skin that moves with
    # the arm is still chest and shoulder top, so the vest strap stays one band when the arm is raised (Sam, 22 Nov,
    # K4 still: the strap was a torn island cut off from the vest front)
    trunk = (g == 0) | ((g == 1) & (ax < 1.45) & (y > 5.0) & (y < 7.95))
    vest = trunk & (y >= 2.6) & ~((ax > 1.5) & (y > 5.7))
    neck_front = (z > 0) & (y > 6.75 - 0.25 * np.clip((ax - 0.0) / 0.9, 0, 1) * 0) & (ax < 0.85)
    neck_back = (z <= 0) & (y > 7.35) & (ax < 0.85)
    vest &= ~(neck_front | neck_back) & (y < 7.95)
    part[vest] = 1
    part[((g == 0) & (y < 2.6)) | (g == 2)] = 2
    part[(g == 4) | ((g == 2) & (y < -6.85))] = 3
    head = g == 3
    ear = ax > 0.72
    hair = head & ~(ear & (y < 10.0)) & ((y > 10.15) | ((z < 0.25) & (y > 9.35)) | ((z < 0.7) & (y > 9.75)))
    part[hair] = 4
    return part


def _parts(v, bone, sk):
    """House clothes on the rest body (MakeHuman decimetres, y up, face +z; pelvis 2.1, shoulders 7.1, head top
    10.85): a white vest (trunk, straps over the shoulders, a scoop neck, arm holes), olive trousers (waistband 2.6
    down), dark shoes (below the ankle), a dark buzz cut on the skull; the rest bare skin."""
    part = np.zeros(len(v), int)
    for i, b in enumerate(bone):
        x, y, z = v[i]
        ax = abs(x)
        trunk = b.startswith(('spine', 'breast', 'pelvis', 'clavicle', 'shoulder')) or b == 'root'
        if y < -6.85 and b.startswith(('foot', 'toe', 'lowerleg')):
            part[i] = 3
        elif y < 2.6 and (trunk or b.startswith(('upperleg', 'lowerleg'))):
            part[i] = 2
        elif b.startswith(('upperleg', 'lowerleg')):
            part[i] = 2
        elif trunk:
            if ax > 1.45 and y > 5.6:
                continue                                    # the arm hole
            if 0.8 <= ax <= 1.45:
                part[i] = 1                                 # the straps
            elif (z > 0 and y > 6.5) or (z <= 0 and y > 7.3) or y > 7.7:
                continue                                    # the scoop neck, front and back
            else:
                part[i] = 1
        elif b.startswith(('head', 'neck03', 'neck02')):
            ear = ax > 0.72 and y < 10.0
            if not ear and (y > 10.15 or (z < 0.25 and y > 9.35) or (z < 0.7 and y > 9.75)):
                part[i] = 4
    return part


def posed(k, M_scale=None):
    """The body on house skeleton k (lying.Body in the car's frame). Returns points (N,3) metres car frame, tris,
    parts, bones. The car's frame is left-handed against MakeHuman's: x is mirrored (Jason's right arm is MakeHuman's
    .R, at MakeHuman -x, the car's +x when he faces forward)."""
    v = jason_mesh()
    sk, tris = _REST['sk'], _REST['tris']
    mir = np.array([-1.0, 1, 1])
    K = {n: np.asarray(p, float) * mir for n, p in k.items()}      # house skeleton into MakeHuman's handedness
    rest_len = np.linalg.norm(sk.rest['neck01'][:3, 3] - sk.rest['spine05'][:3, 3])
    s = M_scale or np.linalg.norm(K['neck'] - K['pelvis']) / rest_len     # metres per decimetre unit
    # the world rotation of each bone: inherited from its parent unless a chain aims it
    aim = {}
    for bones, a, b in CHAIN:
        for S_, s_ in (('L', 'L'), ('R', 'R')) if '{S}' in bones else ((None, None),):
            names = bones.format(S=S_).split() if S_ else bones.split()
            ja, jb = a.format(s=s_) if s_ else a, b.format(s=s_) if s_ else b
            for nm in names:
                aim[nm] = K[jb] - K[ja]
    Q = {}
    for b in sk.order:
        p = sk.bones[b]['parent']
        Qp = Q[p] if p else np.eye(3)
        if b in aim:
            cur = Qp @ sk.rest[b][:3, 1]
            Q[b] = _align(cur, aim[b]) @ Qp
        else:
            Q[b] = Qp
    # the pelvis head goes to the house pelvis; each bone's head follows its parent's transform
    Mx = {}
    for b in sk.order:
        p = sk.bones[b]['parent']
        h = sk.rest[b][:3, 3]
        if p:
            Rp, tp = Mx[p]
            nh = Rp @ h + tp
        else:
            nh = h
        Mx[b] = (Q[b], nh - Q[b] @ h)
    acc = np.zeros((len(v), 3))
    ws = np.zeros(len(v))
    for b, (idx, w) in sk.weights.items():
        R, t = Mx[b]
        acc[idx] += w[:, None] * (v[idx] @ R.T + t)
        ws[idx] += w
    free = ws < 1e-6
    acc[free] = v[free]
    ws[free] = 1
    P = acc / ws[:, None]
    root = Mx['spine05'][0] @ sk.rest['spine05'][:3, 3] + Mx['spine05'][1]
    P = (P - root) * s + K['pelvis']
    P = P * mir                                                     # back into the car's frame
    used = _REST['used']
    keep = np.zeros(len(v), bool)
    keep[used] = True
    return P, tris[:, ::-1], _REST['part'], _REST['bone'], keep


def rest_attrs():
    return _REST['v'], _REST['grp']


def car_window():
    """The test space's car (Tulip numbers, gta_cars): boxes (name, part, lo, hi) in the car's frame. Only what
    frames the passenger: his door with the window open, the windscreen's frame, the roof, his seat, the dash, the
    bonnet's top surface out to the lens side (it hides his lap as the film's car does)."""
    B = []
    hw, wall = 0.985, 0.07
    B.append(('door R', 'door', (hw - wall, 0.30, -0.95), (hw, 0.95, 0.80)))
    B.append(('door L', 'door', (-hw, 0.30, -0.95), (-hw + wall, 0.95, 0.80)))
    B.append(('bonnet', 'body', (-hw, 0.62, 0.80), (hw, 0.98, 2.40)))       # the engine bay over the footwell
    B.append(('bulkhead', 'dash', (-hw + wall, 0.10, 1.10), (hw - wall, 0.62, 1.20)))   # the footwell's end
    B.append(('floor', 'dash', (-hw, 0.0, -1.98), (hw, 0.10, 1.20)))
    B.append(('dash', 'dash', (-hw + wall, 0.60, 0.55), (hw - wall, 0.98, 0.80)))
    B.append(('seat R', 'seat', (0.18, 0.30, -0.35), (0.70, 0.47, 0.25)))
    B.append(('seat back R', 'seat', (0.18, 0.47, -0.45), (0.70, 1.15, -0.30)))
    return B


def windscreen_frame():
    """The windscreen's frame and the A pillars as thin solid rods (base z 0.80 at y 0.95 to roof front z 0.30 at
    y 1.47; half width 0.86 -> 0.70), the roof slab, and the front side window's back post (B pillar)."""
    rods = []
    for sx in (-1, 1):
        rods.append(('A pillar', (sx * 0.86, 0.95, 0.80), (sx * 0.70, 1.47, 0.30), 0.035))
        rods.append(('B pillar', (sx * 0.86, 0.95, -0.95), (sx * 0.70, 1.47, -0.60), 0.035))
    rods.append(('windscreen top', (-0.70, 1.47, 0.30), (0.70, 1.47, 0.30), 0.04))
    rods.append(('windscreen base', (-0.86, 0.97, 0.80), (0.86, 0.97, 0.80), 0.03))
    return rods


def write_obj(path, P, tris, groups=None):
    with open(path, 'w') as f:
        for p in P:
            f.write('v %.5f %.5f %.5f\n' % tuple(p))
        if groups is None:
            for t in tris:
                f.write('f %d %d %d\n' % tuple(np.asarray(t) + 1))
        else:
            for g, ts in groups.items():
                f.write('g %s\nusemtl %s\n' % (g, g))
                for t in ts:
                    f.write('f %d %d %d\n' % tuple(np.asarray(t) + 1))


if __name__ == '__main__':
    import gta_cast as GC
    import leanout as LO
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    sp = dict(GC.cast()['jason'], mood='stern')
    k = LO.seated(sp)
    P, T, part, bone, keep = posed(k)
    groups = {}
    for t in T:
        if keep[t].all():
            groups.setdefault(PARTS[int(np.bincount(part[t]).argmax())], []).append(t)
    write_obj(os.path.join(out, 'jason.obj'), P, None, groups)
    json.dump({n: list(map(float, k[n])) for n in k}, open(os.path.join(out, 'k1.json'), 'w'))
    print('points', int(keep.sum()), 'tris', sum(len(x) for x in groups.values()), {g: len(x) for g, x in groups.items()})
    print('bbox', P[keep].min(0).round(3), P[keep].max(0).round(3))
