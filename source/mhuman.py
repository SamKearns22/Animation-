#!/usr/bin/env python3
"""A real human body for our characters, built on MakeHuman's measured model (CC0 since 2020,
https://github.com/makehumancommunity/makehuman/blob/master/LICENSE.md).

MakeHuman gives an anatomically correct base mesh, thousands of shape "targets" (age, gender, build, face
shape...), a skeleton with every finger and facial muscle, skinning weights, and facial expression units.
This module downloads those files (they are not kept in our repository), mixes the shape, poses the skeleton
and hands back a triangle mesh, which mesh_sdf.py then turns into a shape our renderer can draw.

The formulas follow MakeHuman's own code (apps/human.py, shared/skeleton.py, shared/animation.py); see
guides/character-anatomy.md, section 5. MakeHuman units are decimetres, y up, the face towards +z.
"""
import json
import os
import subprocess
import tempfile

import numpy as np

MH_REPO = 'https://github.com/makehumancommunity/makehuman.git'
MH_DIR = os.environ.get('MAKEHUMAN_DATA', os.path.join(tempfile.gettempdir(), 'makehuman'))


def data_dir():
    """MakeHuman's data folder, downloaded (about 140 MB) the first time it is needed."""
    d = os.path.join(MH_DIR, 'makehuman', 'data')
    if not os.path.exists(os.path.join(d, '3dobjs', 'base.obj')):
        subprocess.run(['git', 'clone', '-q', '--depth', '1', '--filter=blob:none', '--sparse', MH_REPO, MH_DIR],
                       check=True)
        subprocess.run(['git', '-C', MH_DIR, 'sparse-checkout', 'set', 'makehuman/data'], check=True)
    return d


# ---------------------------------------------------------------------------
# The base mesh
# ---------------------------------------------------------------------------
def load_base():
    """Vertices (N,3) and the quads/triangles of each face group of base.obj."""
    verts, groups, group = [], {}, None
    with open(os.path.join(data_dir(), '3dobjs', 'base.obj')) as f:
        for line in f:
            if line.startswith('v '):
                verts.append([float(x) for x in line.split()[1:4]])
            elif line.startswith('g '):
                group = line.split()[1]
                groups.setdefault(group, [])
            elif line.startswith('f '):
                groups[group].append([int(t.split('/')[0]) - 1 for t in line.split()[1:]])
    return np.array(verts, np.float64), groups


def load_target(path):
    idx, d = [], []
    with open(path) as f:
        for line in f:
            if line[:1].isdigit():
                p = line.split()
                idx.append(int(p[0]))
                d.append([float(p[1]), float(p[2]), float(p[3])])
    return np.array(idx, int), np.array(d, np.float64)


def add_target(v, rel, weight):
    if weight == 0:
        return
    idx, d = load_target(os.path.join(data_dir(), 'targets', rel))
    if len(idx):
        v[idx] += weight * d


# ---------------------------------------------------------------------------
# Shape: MakeHuman's "macro" mix (see apps/human.py _set*Vals)
# ---------------------------------------------------------------------------
def macro_values(gender=0.0, age=0.5, muscle=0.5, weight=0.5, height=0.5, proportions=0.5,
                 african=0.0, asian=0.0, caucasian=1.0):
    v = {'male': gender, 'female': 1 - gender}
    if age < 0.5:
        v['old'] = 0.0
        v['baby'] = max(0.0, 1 - age * 5.333)
        v['young'] = max(0.0, (age - 0.1875) * 3.2)
        v['child'] = max(0.0, min(1.0, 5.333 * age) - v['young'])
    else:
        v['child'] = v['baby'] = 0.0
        v['old'] = max(0.0, age * 2 - 1)
        v['young'] = 1 - v['old']
    for name, x in (('muscle', muscle), ('weight', weight)):
        v['max' + name] = max(0.0, x * 2 - 1)
        v['min' + name] = max(0.0, 1 - x * 2)
        v['average' + name] = 1 - v['max' + name] - v['min' + name]
    v['maxheight'] = max(0.0, height * 2 - 1)
    v['minheight'] = max(0.0, 1 - height * 2)
    v['averageheight'] = 1 - max(v['maxheight'], v['minheight'])
    v['idealproportions'] = max(0.0, proportions * 2 - 1)
    v['uncommonproportions'] = max(0.0, 1 - proportions * 2)
    v['regularproportions'] = 1 - max(v['idealproportions'], v['uncommonproportions'])
    tot = african + asian + caucasian
    v.update(african=african / tot, asian=asian / tot, caucasian=caucasian / tot)
    return v


def apply_macros(v, vals):
    """Add every macro target, each weighted by the product of the values named in its filename."""
    base = os.path.join(data_dir(), 'targets', 'macrodetails')
    for sub in ('', 'height', 'proportions'):
        folder = os.path.join(base, sub)
        for fn in sorted(os.listdir(folder)):
            if not fn.endswith('.target'):
                continue
            parts = fn[:-7].split('-')
            if parts[0] == 'universal':
                parts = parts[1:]
            w = 1.0
            for p in parts:
                w *= vals.get(p, 0.0)
            if w > 1e-4:
                add_target(v, os.path.join('macrodetails', sub, fn), w)


def apply_details(v, details):
    """details: {'nose/nose-point-width-decr': 0.3, ...} - the regional face and body sliders."""
    for rel, w in details.items():
        add_target(v, rel + '.target', w)


# ---------------------------------------------------------------------------
# Skeleton and skinning (see shared/skeleton.py and shared/animation.py)
# ---------------------------------------------------------------------------
class Skeleton:
    def __init__(self, verts):
        d = data_dir()
        s = json.load(open(os.path.join(d, 'rigs', 'default.mhskel')))
        self.bones = s['bones']
        self.joint_idx = s['joints']
        self.planes = s['planes']
        # breadth-first order, parents first
        order, queue = [], [b for b, x in self.bones.items() if not x['parent']]
        while queue:
            b = queue.pop(0)
            order.append(b)
            queue += sorted(c for c, x in self.bones.items() if x['parent'] == b)
        self.order = order
        self.set_rest(verts)
        w = json.load(open(os.path.join(d, 'rigs', 'default_weights.mhw')))['weights']
        self.weights = {b: (np.array([i for i, _ in w[b]], int), np.array([x for _, x in w[b]]))
                        for b in w if b in self.bones}

    def joint(self, name, verts):
        return verts[self.joint_idx[name]].mean(0)

    def set_rest(self, verts):
        self.rest = {}
        for b in self.order:
            x = self.bones[b]
            head, tail = self.joint(x['head'], verts), self.joint(x['tail'], verts)
            rp = x['rotation_plane']
            planes = rp if isinstance(rp, list) and rp and isinstance(rp[0], str) and rp[0] in self.planes \
                else ([rp] if isinstance(rp, str) else [])
            n = np.zeros(3)
            for pl in planes:
                j1, j2, j3 = self.planes[pl]
                p1, p2, p3 = (self.joint(j, verts) for j in (j1, j2, j3))
                pv = (p2 - p1) / np.linalg.norm(p2 - p1)
                yv = (p3 - p2) / np.linalg.norm(p3 - p2)
                c = np.cross(yv, pv)
                n += c / np.linalg.norm(c)
            if not np.any(n):
                n = np.array([0, 1.0, 0])
            self.rest[b] = bone_matrix(head, tail, n)

    def localize(self, pose):
        """Poses are written with rotations along the world axes (as MakeHuman's pose files are); turn them
        into rotations about each bone's own rest axes (skeleton.py setPose)."""
        return {b: self.rest[b][:3, :3].T @ R @ self.rest[b][:3, :3] for b, R in pose.items() if b in self.rest}

    def pose_matrices(self, local):
        """local: {bone: 3x3 rotation in the bone's own axes}. Returns {bone: 4x4 vertex transform}."""
        glob, out = {}, {}
        for b in self.order:
            p = self.bones[b]['parent']
            R = np.eye(4)
            if b in local:
                R[:3, :3] = local[b]
            if p:
                rel = np.linalg.inv(self.rest[p]) @ self.rest[b]
                glob[b] = glob[p] @ rel @ R
            else:
                glob[b] = self.rest[b] @ R
            out[b] = glob[b] @ np.linalg.inv(self.rest[b])
        return out

    def skin(self, verts, local):
        """Linear blend skinning of verts by the pose."""
        M = self.pose_matrices(local)
        acc = np.zeros((len(verts), 3, 4))
        wsum = np.zeros(len(verts))
        for b, (idx, w) in self.weights.items():
            acc[idx] += w[:, None, None] * M[b][None, :3, :4]
            wsum[idx] += w
        free = wsum < 1e-6
        acc[free] = np.eye(4)[:3]
        wsum[free] = 1.0
        acc /= wsum[:, None, None]
        return np.einsum('nij,nj->ni', acc[:, :, :3], verts) + acc[:, :, 3]

    def axes(self, b):
        """World axes of a bone at rest: x (main bending axis), y (along the bone), z."""
        m = self.rest[b]
        return m[:3, 0], m[:3, 1], m[:3, 2]


def bone_matrix(head, tail, normal):
    y = (tail - head) / np.linalg.norm(tail - head)
    n = normal / np.linalg.norm(normal)
    z = np.cross(n, y)
    z /= np.linalg.norm(z)
    x = np.cross(y, z)
    m = np.eye(4)
    m[:3, 0], m[:3, 1], m[:3, 2], m[:3, 3] = x, y, z, head
    return m


def axis_angle(axis, deg):
    a = np.asarray(axis, float)
    a /= np.linalg.norm(a)
    t = np.radians(deg)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K


# ---------------------------------------------------------------------------
# Facial expression units (face-poseunits.bvh, see plugins/7_expression_mixer.py)
# ---------------------------------------------------------------------------
def face_units():
    """{unit name: {bone: 3x3 local rotation}} read from MakeHuman's facial pose units."""
    d = data_dir()
    names = json.load(open(os.path.join(d, 'poseunits', 'face-poseunits.json')))['framemapping']
    lines = open(os.path.join(d, 'poseunits', 'face-poseunits.bvh')).read().split('\n')
    joints, chans = [], []
    i = 0
    while not lines[i].strip().startswith('MOTION'):
        t = lines[i].split()
        if t and t[0] in ('ROOT', 'JOINT'):
            joints.append(t[1])
        if t and t[0] == 'CHANNELS':
            chans.append(t[2:])
        i += 1
    nframes = int(lines[i + 1].split()[1])
    data = [list(map(float, l.split())) for l in lines[i + 3:i + 3 + nframes]]
    units = {}
    for f, name in enumerate(names[:nframes]):
        row, k, pose = data[f], 0, {}
        for j, ch in zip(joints, chans):
            order = ''
            angles = []
            for c in ch:
                val = row[k]
                k += 1
                # the file is z-up (MakeHuman detects this from its joint offsets): Y rotations become
                # negated Z ones, Z rotations become Y ones (bvh.py calculateFrames, convertFromZUp)
                if c == 'Xrotation':
                    order, a = 'x' + order, np.radians(val)
                elif c == 'Yrotation':
                    order, a = 'z' + order, -np.radians(val)
                elif c == 'Zrotation':
                    order, a = 'y' + order, np.radians(val)
                else:
                    continue
                angles.append(a)
            if angles and any(abs(a) > 1e-6 for a in angles):
                # static-frame euler as in bvh.py: euler_matrix(a[2], a[1], a[0], 's' + order)
                pose[j] = euler_static(order, angles[::-1])
        units[name] = pose
    return units


def euler_static(order, angles):
    """Rotation for static-axis euler angles applied in `order` (first letter first)."""
    R = np.eye(3)
    for a, t in zip(order, angles):
        c, s = np.cos(t), np.sin(t)
        M = {'x': np.array([[1, 0, 0], [0, c, -s], [0, s, c]]),
             'y': np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]),
             'z': np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])}[a]
        R = M @ R
    return R


def blend_units(units, weights):
    """Blend unit poses: each slerped from rest by its weight, then multiplied (additive blending)."""
    out = {}
    for name, w in weights.items():
        for b, R in units[name].items():
            Rw = rot_power(R, w)
            out[b] = Rw @ out.get(b, np.eye(3))
    return out


def rot_power(R, w):
    """The rotation R scaled by w along its own axis (slerp from identity)."""
    ang = np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1))
    if ang < 1e-8:
        return np.eye(3)
    axis = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]]) / (2 * np.sin(ang))
    return axis_angle(axis, np.degrees(ang * w))
