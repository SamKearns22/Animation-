"""A posable MakeHuman body, for any of our characters (see guides/character-anatomy.md).

The whole body is MakeHuman's measured model with its real skeleton. For each pose the skin is bent by the
skeleton exactly as MakeHuman (and every animation package) does it - each point of skin moved by a weighted
blend of its nearby bones, so elbows and shoulders bend smoothly with no seams - and then turned into a
distance grid our renderer can draw. Clothes are made from the bent body: its surface swollen by the cloth's
thickness, loose cloth falling straight down under gravity where it hangs (a jumper from the bust), and cut
off at hems, cuffs and collars. Heads and hands are finer work and are made separately (see mother.py).

Coordinates: metres, y up, the body facing +z in its own frame, feet on y = 0 at rest. A character is put in
the world by a placement: position on the floor and a turn about the vertical (yaw).
"""
import numpy as np

import mesh_sdf
import mhuman as H

# which bones move which piece of the body; the first bone listed carries the piece
PIECES = {
    'hips': ('spine04', ('root', 'pelvis.L', 'pelvis.R', 'spine05', 'spine04')),
    'chest': ('spine02', ('spine03', 'spine02', 'spine01', 'breast.L', 'breast.R', 'clavicle.L', 'clavicle.R',
                          'neck01', 'neck02', 'neck03')),
    'upperarm.R': ('upperarm01.R', ('shoulder01.R', 'upperarm01.R', 'upperarm02.R')),
    'forearm.R': ('lowerarm01.R', ('lowerarm01.R', 'lowerarm02.R')),
    'upperarm.L': ('upperarm01.L', ('shoulder01.L', 'upperarm01.L', 'upperarm02.L')),
    'forearm.L': ('lowerarm01.L', ('lowerarm01.L', 'lowerarm02.L')),
    'thigh.R': ('upperleg01.R', ('upperleg01.R', 'upperleg02.R')),
    'shin.R': ('lowerleg01.R', ('lowerleg01.R', 'lowerleg02.R')),
    'foot.R': ('foot.R', ('foot.R',)),
    'thigh.L': ('upperleg01.L', ('upperleg01.L', 'upperleg02.L')),
    'shin.L': ('lowerleg01.L', ('lowerleg01.L', 'lowerleg02.L')),
    'foot.L': ('foot.L', ('foot.L',)),
}


def piece_of_bone(b):
    for name, (_, bones) in PIECES.items():
        if b in bones:
            return name
    side = b[-2:] if b[-2:] in ('.L', '.R') else ''
    if b.startswith(('wrist', 'metacarpal', 'finger')):
        return 'hand' + side
    if b.startswith('toe'):
        return 'foot' + side
    return 'head'


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def rot_between(a, b):
    """The smallest rotation taking direction a to direction b."""
    a, b = unit(a), unit(b)
    c = np.cross(a, b)
    s, cc = np.linalg.norm(c), a @ b
    if s < 1e-9:
        if cc > 0:
            return np.eye(3)
        p = unit(np.cross(a, [1.0, 0, 0] if abs(a[0]) < 0.9 else [0, 1.0, 0]))
        return H.axis_angle(p, 180.0)
    return H.axis_angle(c / s, np.degrees(np.arctan2(s, cc)))


def yaw_matrix(deg):
    t = np.radians(deg)
    return np.array([[np.cos(t), 0, np.sin(t)], [0, 1.0, 0], [-np.sin(t), 0, np.cos(t)]])


def smin(a, b, k):
    if k <= 0:
        return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b + (a - b) * h - k * h * (1 - h)


def smax(a, b, k):
    return -smin(-a, -b, k)


def robust_distance(F, voxel):
    """Turn an inside/outside function F (negative inside) into distances: F over its slope close to the
    surface, and further away the straight-line distance to the nearest surface voxel plus that voxel's own
    exact distance, lightly smoothed (it steps a little from voxel to voxel, which would show wherever another
    shape is blended in softly). The two are cross-faded, so the result is smooth everywhere."""
    from scipy import ndimage
    gx, gy, gz = np.gradient(F, voxel)
    near = (F / np.maximum(np.sqrt(gx * gx + gy * gy + gz * gz), 1e-6)).astype(np.float32)
    del gx, gy, gz
    inside = F < 0
    d_out, i_out = ndimage.distance_transform_edt(~inside, return_indices=True)
    far = (d_out * voxel + near[i_out[0], i_out[1], i_out[2]]).astype(np.float32)
    del d_out, i_out
    d_in, i_in = ndimage.distance_transform_edt(inside, return_indices=True)
    far_in = (-(d_in * voxel - near[i_in[0], i_in[1], i_in[2]])).astype(np.float32)
    del d_in, i_in
    far = np.where(inside, far_in, far).astype(np.float32)
    far = ndimage.gaussian_filter(far, 1.2)
    w = np.clip((np.abs(far) - 1.8 * voxel) / (1.2 * voxel), 0, 1)
    w = np.where((np.sign(near) != np.sign(far)) & (np.abs(far) > 2 * voxel), 1.0, w)
    near = np.clip(near, -3 * voxel, 3 * voxel)
    return (near * (1 - w) + far * w).astype(np.float32)


class Body:
    """A MakeHuman body shaped by `shape` (macro sliders) and `details` (regional sliders)."""

    def __init__(self, shape, details=None):
        v, g = H.load_base()
        H.apply_macros(v, H.macro_values(**shape))
        H.apply_details(v, details or {})
        self.v_dm, self.groups = v, g
        self.sk = H.Skeleton(v)
        idx = np.unique(np.concatenate([np.array(f) for f in g['body']]))
        self.skin_idx = idx                                    # the skin only (base.obj also holds helpers)
        self.floor = -v[idx, 1].min() * 0.1                    # lifts the feet onto y = 0
        self.faces = g['body']
        # each vertex belongs to the piece whose bones move it most
        names = list(PIECES) + ['hand.L', 'hand.R', 'head']
        acc = np.zeros((len(v), len(names)))
        for b, (vi, w) in self.sk.weights.items():
            acc[vi, names.index(piece_of_bone(b))] += w
        self.piece_names = names
        self.label = acc.argmax(1)

    # --- rest pose, in metres ------------------------------------------------------------------------------
    def to_m(self, p_dm):
        return np.asarray(p_dm) * 0.1 + np.array([0, self.floor, 0])

    def joint(self, bone, end=0):
        """Rest position (metres) of a bone's head (end=0) or tail (end=1)."""
        x = self.sk.bones[bone]
        return self.to_m(self.sk.joint(x['tail'] if end else x['head'], self.v_dm))

    def verts_m(self):
        return self.to_m(self.v_dm)

    # --- the bent body --------------------------------------------------------------------------------------
    def skin(self, pose):
        """Every vertex of the body moved into the pose, in the world (metres)."""
        M = pose.matrices()
        V = self.verts_m()
        acc = np.zeros((len(V), 3, 4))
        wsum = np.zeros(len(V))
        for bn, (vi, w) in self.sk.weights.items():
            acc[vi] += w[:, None, None] * M[bn][None, :3, :4]
            wsum[vi] += w
        free = wsum < 1e-6
        acc[free] = np.eye(4)[:3]
        wsum[free] = 1.0
        acc /= wsum[:, None, None]
        return np.einsum('nij,nj->ni', acc[:, :, :3], V) + acc[:, :, 3]

    def surface(self, Vw, lo, hi, voxel):
        """Distance to the (bent) skin over a box of the world: one smoothing subdivision, then exact
        distances to the triangles near the surface."""
        keep = [f for f in self.faces if np.all((Vw[f] > lo - 0.04) & (Vw[f] < hi + 0.04))]
        V2, q2 = mesh_sdf.catmull_clark(Vw, keep)
        return mesh_sdf.mesh_to_sdf(V2, mesh_sdf.triangulate(q2), lo, hi, voxel, vote=True)[1]

    def part_map(self, Vw, lo, shape, voxel, groups, coarse=0.006):
        """Which part of the body each cell is nearest to: groups = [set of piece names, ...]; returns the
        index of the group (or -1), looked up on a coarse grid and spread to the fine one."""
        from scipy.spatial import cKDTree
        cn = np.maximum((np.array(shape) - 1) * voxel / coarse, 1).astype(int) + 2
        axes = [lo[q] + np.arange(cn[q]) * coarse for q in range(3)]
        grid = np.stack(np.meshgrid(*axes, indexing='ij'), -1).reshape(-1, 3)
        idx = self.skin_idx
        _, near = cKDTree(Vw[idx]).query(grid)
        gid = np.full(len(self.piece_names), -1, np.int8)
        for gi, names in enumerate(groups):
            for nm in names:
                gid[self.piece_names.index(nm)] = gi
        lab = gid[self.label[idx][near]].reshape(cn)
        ii = [np.minimum(np.round(np.arange(shape[q]) * voxel / coarse).astype(int), cn[q] - 1) for q in range(3)]
        return lab[np.ix_(*ii)]


def drape(d, voxel, slope):
    """Loose cloth falls straight down from where it hangs: going down the grid (axis 1 is up), the surface
    never tucks back in faster than `slope` per unit of fall."""
    step = slope * voxel
    for j in range(d.shape[1] - 2, -1, -1):
        np.minimum(d[:, j, :], d[:, j + 1, :] + step, out=d[:, j, :])
    return d


# ---------------------------------------------------------------------------
# Posing
# ---------------------------------------------------------------------------
class Pose:
    """World-axis rotations per bone (as MakeHuman's pose files give them) plus where the body stands.
    Rotations are about each bone's joint, in the body's own frame at rest, applied on top of its parents'."""

    def __init__(self, body, position=(0, 0, 0), yaw=0.0):
        self.body = body
        self.rot = {}
        self.position = np.asarray(position, float)
        self.yaw = yaw

    def world_R(self):
        return yaw_matrix(self.yaw)

    def chain(self, bone):
        """Total rotation (body frame) carried by a bone: the product of its ancestors' and its own."""
        sk = self.body.sk
        seq = []
        b = bone
        while b:
            seq.append(b)
            b = sk.bones[b]['parent']
        R = np.eye(3)
        for b in reversed(seq):
            R = R @ self.rot.get(b, np.eye(3))
        return R

    def matrices(self):
        """{bone: 4x4} taking rest-pose points (metres) to the world."""
        body, sk = self.body, self.body.sk
        local = sk.localize(self.rot)
        M = sk.pose_matrices(local)          # in MakeHuman units (dm), its own origin
        A = np.eye(4)
        A[:3, :3] *= 0.1
        A[1, 3] = body.floor                  # dm -> m, feet on the floor
        W = np.eye(4)
        W[:3, :3] = self.world_R()
        W[:3, 3] = self.position
        Ai = np.linalg.inv(A)
        return {b: W @ A @ m @ Ai for b, m in M.items()}

    def point(self, M, bone, p_rest):
        m = M[bone]
        return m[:3, :3] @ p_rest + m[:3, 3]

    def joint_world(self, M, bone, end=0):
        return self.point(M, bone, self.body.joint(bone, end))

    def joints(self, M=None):
        """World positions of the joints clothes and checks need: shoulders, elbows, wrists, neck, head,
        spine."""
        M = self.matrices() if M is None else M
        J = {}
        for s in ('R', 'L'):
            J['shoulder.' + s] = self.joint_world(M, 'upperarm01.' + s)
            J['elbow.' + s] = self.joint_world(M, 'lowerarm01.' + s)
            J['wrist.' + s] = self.joint_world(M, 'wrist.' + s)
        for bn in ('neck01', 'neck02', 'neck03', 'head', 'spine02', 'spine04', 'spine05'):
            J[bn] = self.joint_world(M, bn)
        return J

    # --- building a pose -------------------------------------------------------------------------------------
    def set_share(self, bones, R_total):
        """Spread a rotation over a chain of bones (e.g. the neck and head turning together)."""
        from scipy.spatial.transform import Rotation
        rv = Rotation.from_matrix(R_total).as_rotvec() / len(bones)
        for b in bones:
            self.rot[b] = Rotation.from_rotvec(rv).as_matrix()

    def aim_head(self, R_head, neck_share=0.4):
        """Turn the head to R_head (body frame, relative to rest), the neck taking neck_share of it."""
        from scipy.spatial.transform import Rotation
        rv = Rotation.from_matrix(R_head).as_rotvec()
        self.set_share(['neck01', 'neck02', 'neck03'], Rotation.from_rotvec(rv * neck_share).as_matrix())
        P = self.chain('neck03')
        self.rot['head'] = P.T @ R_head

    def arm_ik(self, side, wrist_world, pole_world):
        """Bend the arm so its wrist lands on wrist_world, the elbow pointing towards pole_world. Returns the
        elbow and how far (m) the wrist is out of reach (0 when it reaches)."""
        b = self.body
        s = '.' + side
        for bone in ('upperarm01', 'upperarm02', 'lowerarm01', 'lowerarm02'):
            self.rot.pop(bone + s, None)
        M = self.matrices()
        Rw = self.world_R()
        sh = self.joint_world(M, 'upperarm01' + s)
        e0, w0, s0 = b.joint('lowerarm01' + s), b.joint('wrist' + s), b.joint('upperarm01' + s)
        L1, L2 = np.linalg.norm(e0 - s0), np.linalg.norm(w0 - e0)
        d = wrist_world - sh
        D = np.linalg.norm(d)
        short = max(0.0, D - (L1 + L2 - 1e-4))
        Dc = np.clip(D, abs(L1 - L2) + 1e-4, L1 + L2 - 1e-4)
        u = d / D
        a = (L1 ** 2 - L2 ** 2 + Dc ** 2) / (2 * Dc)
        h = np.sqrt(max(L1 ** 2 - a ** 2, 0.0))
        base = sh + u * a
        pv = pole_world - base
        pv -= u * (pv @ u)
        elbow = base + unit(pv) * h
        wrist = elbow + unit(sh + u * Dc - elbow) * L2
        # turn these world directions into the bones' rotations (body frame)
        P = self.chain(self.body.sk.bones['upperarm01' + s]['parent'])
        ut, ft = Rw.T @ unit(elbow - sh), Rw.T @ unit(wrist - elbow)
        u0, f0 = unit(e0 - s0), unit(w0 - e0)
        R1 = rot_between(u0, ut)
        # twist the upper arm about itself so the elbow bends the way the arm's hinge bends
        a0 = f0 - u0 * (f0 @ u0)
        bt = ft - ut * (ft @ ut)
        if np.linalg.norm(a0) > 1e-6 and np.linalg.norm(bt) > 1e-6:
            a1 = R1 @ unit(a0)
            a1 -= ut * (a1 @ ut)
            ang = np.arctan2(np.cross(unit(a1), unit(bt)) @ ut, unit(a1) @ unit(bt))
            R1 = H.axis_angle(ut, np.degrees(ang)) @ R1
        self.rot['upperarm01' + s] = P.T @ R1
        self.rot['lowerarm01' + s] = rot_between(f0, R1.T @ ft)
        return elbow, short
