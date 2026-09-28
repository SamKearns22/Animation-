"""The kneeling man of the 'Merry Chr' shot: a man in his early fifties, in a plain pale shirt and dark blue
trousers, kneeling with his forehead to the wall (see story/horror-merry-chr.md).

Built on MakeHuman's measured body like the mother and daughter (rig.py), but he is seen from behind across a
room, so he is made more simply: his whole bent skin is one distance grid (head, hands and feet included), with
a shirt and trousers made over it (clothes.py) and short greying hair as a close shell over his scalp.

    python3 man.py look OUT.png         quick grey views of him posed (front, side, back)
"""
import sys

import numpy as np

import clothes
import rig
from cache import cached
from rig import unit

# early fifties (MakeHuman age 0.5 = 25 years, 1.0 = 90), a little heavy through the middle, 1.78 m
SHAPE = dict(gender=1.0, age=0.71, muscle=0.5, weight=0.58, height=0.55, proportions=0.5)
FACE = {'head/head-square': 0.3, 'neck/neck-scale-horiz-incr': 0.2}

# a plain, pale cotton shirt with a band collar, tucked in; dark blue trousers
SHIRT = dict(thick=0.014, drape=0.3, bridge=0.10, smooth=0.040, hem=-0.02, cuff=0.012, voxel=0.004,
             collar=('crew', 0.058, 0.007))

_BODY = []


def body():
    if not _BODY:
        _BODY.append(rig.Body(SHAPE, FACE))
    return _BODY[0]


def deps():
    import mother
    return mother.mh_deps() + [SHAPE, FACE]


def solve(spec):
    """His pose from a shot's description. spec keys:
      position   (x, z) of the point midway between his knees, on the floor
      yaw        which way he faces (180: towards -z, the back wall of the spare room)
      lean       degrees his body leans forward from the hips (towards the wall)
      nod        degrees his head is bowed forward on his neck (his forehead to the wall)
      head_roll  degrees his head is tipped to one side
      hands      'hang': his arms hang limp at his sides
    For animation (the head strikes):
      root       his body's exact placement (pose.position, from the pose at contact), so his knees stay
                 put while he moves; replaces the placement on the floor and against the wall
      upper      extra degrees his upper back (and neck) bend forward (negative: pulled back)
      jolt       degrees his shoulders are thrown forward and down (the impact running through them)
      swing      (left, right) metres his dead hands have swung forward of where they hang
    """
    import mhuman as MH
    b = body()
    pose = rig.Pose(b, (0, 0, 0), spec.get('yaw', 180.0))
    X = lambda deg: MH.axis_angle([1, 0, 0], deg)
    # kneeling: thighs nearly upright (hips pushed a little forward), shins flat on the floor behind him, the
    # tops of his feet flat on the boards (soles up)
    hip = spec.get('hip', 6.0)
    for s in 'LR':
        pose.rot['upperleg01.' + s] = X(hip)
        pose.rot['lowerleg01.' + s] = X(88.0 - hip)
        pose.rot['foot.' + s] = X(spec.get('ankle', 55.0))
    lean = spec.get('lean', 0.0)
    upper = spec.get('upper', 0.0)
    for bone in ('spine05', 'spine04', 'spine03', 'spine02'):
        pose.rot[bone] = X(lean / 4 + (upper / 2 if bone in ('spine03', 'spine02') else 0.0))
    jolt = spec.get('jolt', 0.0)
    if jolt:
        Y = lambda deg: MH.axis_angle([0, 1, 0], deg)
        Z = lambda deg: MH.axis_angle([0, 0, 1], deg)
        pose.rot['clavicle.L'] = Y(-jolt) @ Z(-jolt * 0.6)
        pose.rot['clavicle.R'] = Y(jolt * 0.85) @ Z(jolt * 0.5)      # (never quite twins)
    pose.aim_head(X(spec.get('nod', 0.0)) @ MH.axis_angle([0, 0, 1], spec.get('head_roll', 0.0)), neck_share=0.5)
    # stand him on his knees: find where the bent body reaches the floor, and put that on y = 0
    Vw = b.skin(pose)
    legs = np.isin(b.label, [b.piece_names.index(n) for n in ('shin.L', 'shin.R', 'foot.L', 'foot.R')])
    legs &= np.isin(np.arange(len(Vw)), b.skin_idx)
    M = pose.matrices()
    knees = (pose.joint_world(M, 'lowerleg01.L') + pose.joint_world(M, 'lowerleg01.R')) / 2
    x, z = spec['position']
    pose.position = np.array([x - knees[0], -Vw[legs, 1].min() + 0.004, z - knees[2]])
    if 'root' in spec:
        pose.position = np.array(spec['root'], float)
    elif 'wall_z' in spec:          # slide him on his knees until his forehead just meets the wall (in -z)
        pose.position[2] += spec['wall_z'] + 0.002 - forehead(dict(verts=b.skin(pose), yaw=spec.get('yaw', 180.0)))[2]
    M = pose.matrices()
    J = pose.joints(M)
    # arms hang limp at his sides, a little forward of his hips, the elbows soft
    Rw = pose.world_R()
    fwd, side = Rw @ np.array([0, 0, 1.0]), Rw @ np.array([1.0, 0, 0])
    swing = dict(zip('LR', spec.get('swing', (0.0, 0.0))))
    for s, sg in (('R', -1), ('L', 1)):
        sh = J['shoulder.' + s]
        w = sh + np.array([0, -0.50, 0]) + fwd * (0.10 + swing[s]) + side * sg * 0.05
        pose.arm_ik(s, w, sh + np.array([0, -0.3, 0]) - fwd * 0.4 + side * sg * 0.1)
    M = pose.matrices()
    J = pose.joints(M)
    head = M['head'][:3, :3], pose.joint_world(M, 'head')
    return dict(spec=spec, pose=pose, M=M, joints=J, head=head, yaw=spec.get('yaw', 180.0))


def pieces(state):
    """Every grid of him in the scene, as (grid, origin, rotation) like mother.pieces (all world grids)."""
    return [(state[k][:3], None, None) for k in ('skin', 'hair', 'socks', 'shirt', 'trousers')]


def forehead(state):
    """World position of the part of his head furthest forward - where it meets the wall (with his head
    bowed, his forehead)."""
    b = body()
    Vw = state['verts']
    idx = b.skin_idx[b.label[b.skin_idx] == b.piece_names.index('head')]
    fwd = rig.yaw_matrix(state.get('yaw', 180.0)) @ np.array([0, 0, 1.0])
    return Vw[idx[np.argmax(Vw[idx] @ fwd)]]


def forehead_rest_height(state):
    """How far above his eyes (at rest) that point is: positive when it is his forehead, not his nose."""
    b = body()
    idx = b.skin_idx[b.label[b.skin_idx] == b.piece_names.index('head')]
    fwd = rig.yaw_matrix(state.get('yaw', 180.0)) @ np.array([0, 0, 1.0])
    k = idx[np.argmax(state['verts'][idx] @ fwd)]
    return b.verts_m()[k, 1] - (b.joint('head')[1] + 0.075)


def skin_grid(state, voxel=0.004):
    """His whole bent skin as one distance grid (world)."""
    b = body()
    Vw = state['verts']
    idx = b.skin_idx
    lo, hi = Vw[idx].min(0) - 0.03, Vw[idx].max(0) + 0.03
    n = np.round((hi - lo) / voxel).astype(int) + 1
    d = b.surface(Vw, lo, lo + (n - 1) * voxel, voxel)
    return lo, rig.robust_distance(d.astype(np.float32), voxel), voxel


def trousers(state, voxel=0.004):
    """Loose dark trousers from his waist to his ankles (world grid)."""
    b = body()
    Vw, J, M, pose = state['verts'], state['joints'], state['M'], state['pose']
    sel = np.isin(b.label, [b.piece_names.index(n) for n in ('hips', 'thigh.L', 'thigh.R', 'shin.L', 'shin.R')])
    sel &= np.isin(np.arange(len(Vw)), b.skin_idx)
    lo, hi = Vw[sel].min(0) - 0.10, Vw[sel].max(0) + 0.10
    n = np.round((hi - lo) / voxel).astype(int) + 1
    d = b.surface(Vw, lo, lo + (n - 1) * voxel, voxel)
    # (his arms and hands hang beside his thighs: leave them out, or the cloth would wrap them)
    part = b.part_map(Vw, lo, d.shape, voxel, [{'upperarm.L', 'upperarm.R', 'forearm.L', 'forearm.R', 'hand.L',
                                                 'hand.R'}])
    d = rig.robust_distance(np.where(part == 0, np.maximum(d, 0.03), d).astype(np.float32), voxel)
    # loose cloth: bridges the gap between the legs at the crotch, a little full, no fine detail
    d = d - 0.012
    d = rig.robust_distance(rig.robust_distance(d - 0.025, voxel) + 0.025, voxel)
    d = rig.robust_distance(rig.robust_distance(d + 0.012, voxel) - 0.012, voxel)
    axes = [lo[q] + np.arange(n[q]) * voxel for q in range(3)]
    X, Y, Z = np.meshgrid(*axes, indexing='ij', sparse=True)
    # the waistband, level round his waist (in his body's frame), the shirt tucked in above it
    wb = J['spine05'] + (J['spine04'] - J['spine05']) * 0.9
    up = unit(J['spine04'] - J['spine05'])
    d = rig.smax(d, (X - wb[0]) * up[0] + (Y - wb[1]) * up[1] + (Z - wb[2]) * up[2], 0.004)
    # the hems, just past the ankles
    for s in 'LR':
        a = pose.joint_world(M, 'foot.' + s)
        k = pose.joint_world(M, 'lowerleg01.' + s)
        ax = unit(a - k)
        c = a + ax * 0.01
        d = rig.smax(d, (X - c[0]) * ax[0] + (Y - c[1]) * ax[1] + (Z - c[2]) * ax[2]
                     - 1e3 * (((X - a[0]) ** 2 + (Y - a[1]) ** 2 + (Z - a[2]) ** 2) > 0.12 ** 2), 0.004)
    return lo, rig.robust_distance(d.astype(np.float32), voxel), voxel


def socks(state, skin):
    """Dark socks: his skin over the feet, 2 mm proud (a small grid round his feet only)."""
    b = body()
    lo, d, vox = skin
    Vw = state['verts']
    feet = np.isin(b.label, [b.piece_names.index(n) for n in ('foot.L', 'foot.R')])
    feet &= np.isin(np.arange(len(Vw)), b.skin_idx)
    i0 = np.maximum(((Vw[feet].min(0) - 0.03 - lo) / vox).astype(int), 0)
    i1 = np.minimum(((Vw[feet].max(0) + 0.03 - lo) / vox).astype(int) + 1, np.array(d.shape))
    sub = d[i0[0]:i1[0], i0[1]:i1[1], i0[2]:i1[2]]
    lo2 = lo + i0 * vox
    part = b.part_map(Vw, lo2, sub.shape, vox, [{'foot.L', 'foot.R'}])
    f = np.where(part == 0, sub - 0.004, np.maximum(sub, 0.004) + 0.01)
    f = rig.robust_distance(f.astype(np.float32), vox)
    f = rig.robust_distance(rig.robust_distance(f - 0.012, vox) + 0.012, vox)      # a sock: no toes
    return lo2, f, vox


def hair(state, skin, voxel=0.003):
    """Short, greying hair: a close shell (7 mm) over the top, back and sides of his head, stopping at a
    hairline over the forehead, above the ears and at the nape."""
    b = body()
    lo_s, d_s, vs = skin
    Mh = state['M']['head']
    Rinv = np.linalg.inv(Mh)
    hj = b.joint('head')
    eye = hj + np.array([0, 0.075, 0])              # rest pose: eye level above the head joint
    c = state['pose'].point(state['M'], 'head', hj + np.array([0, 0.10, 0]))
    lo, hi = c - 0.16, c + 0.16
    n = np.round((hi - lo) / voxel).astype(int) + 1
    axes = [lo[q] + np.arange(n[q]) * voxel for q in range(3)]
    P = np.stack(np.meshgrid(*axes, indexing='ij'), -1)
    # sample the skin's distance here
    from scipy import ndimage
    idx = ((P - lo_s) / vs).reshape(-1, 3).T
    d = ndimage.map_coordinates(d_s, idx, order=1, mode='nearest').reshape(n) - 0.007
    # where each point sits on his head at rest
    Pr = P @ Rinv[:3, :3].T + Rinv[:3, 3]
    x, y, z = Pr[..., 0] - eye[0], Pr[..., 1] - eye[1], Pr[..., 2] - eye[2]
    # hairline: over the forehead 6.5 cm above the eyes (a little receded at the temples), down to just above
    # the ears at the sides, to the nape at the back
    front = y - (0.062 + 0.012 * np.clip(np.abs(x) / 0.05, 0, 1))
    side = y + 0.01 + 0.03 * np.clip(-(z + 0.02) / 0.08, 0, 1)
    nape = y + 0.075
    cut = np.where(z > 0.02, front, np.where(z > -0.06, np.minimum(np.maximum(front, -(z - 0.02) * 2), side), nape))
    # the ears stay bare
    ear = np.sqrt((np.abs(x) - 0.072) ** 2 + (y + 0.02) ** 2 + (z + 0.035) ** 2) - 0.035
    # thinning out towards the hairline rather than stopping at a hard edge
    d = d + 0.006 * (1 - np.clip(cut / 0.025, 0, 1))
    d = rig.smax(d, -cut, 0.012)
    d = rig.smax(d, -ear, 0.006)
    return lo, rig.robust_distance(d.astype(np.float32), voxel), voxel


def prepare(state):
    b = body()
    key = (np.round(state['M']['head'], 5).tolist(), sorted((k, np.round(v, 5).tolist())
                                                            for k, v in state['pose'].rot.items()),
           np.round(state['pose'].position, 5).tolist())
    state['verts'] = b.skin(state['pose'])
    dep = deps() + [rig.Body.skin, rig.Body.surface, rig.robust_distance]
    state['skin'] = cached('manskin', lambda k: skin_grid(state), dep + [skin_grid], key)
    state['shirt'] = cached('manshirt', lambda k: clothes.top(b, state['pose'], state['joints'], SHIRT),
                            dep + [clothes.top, SHIRT, rig.drape, rig.Body.part_map], key)
    state['trousers'] = cached('mantrousers', lambda k: trousers(state), dep + [trousers], key)
    state['socks'] = cached('mansocks', lambda k: socks(state, state['skin']), dep + [socks, skin_grid], key)
    state['hair'] = cached('manhair', lambda k: hair(state, state['skin']), dep + [hair, skin_grid], key)
    return state


def build(b, state):
    import sdf3d as S
    from materials import MAN_SKIN, SHIRT as SHIRT_M, TROUSERS, MAN_HAIR, SOCK
    b.set_frame((0, 0, 0), None)
    b.group('man_skin', margin=0.01)
    b.grid(*state['skin'], MAN_SKIN, op=S.UNION)
    b.group('man_hair', margin=0.01)
    b.grid(*state['hair'], MAN_HAIR, op=S.UNION)
    b.group('man_socks', margin=0.01)
    b.grid(*state['socks'], SOCK, op=S.UNION)
    lo, d, vox, part = state['shirt']
    b.group('man_shirt', margin=0.01)
    b.grid(lo, d, vox, SHIRT_M, op=S.UNION)
    b.group('man_trousers', margin=0.01)
    b.grid(*state['trousers'], TROUSERS, op=S.UNION)


def look(out):
    """Quick grey views of him posed: front, side and back."""
    import sdf3d as S
    from PIL import Image
    from materials import mat_table, new_params, default_lights
    st = prepare(solve(dict(position=(0.0, 0.0), yaw=180.0, lean=12.0, nod=18.0)))
    b = S.Builder()
    build(b, st)
    b.group('floor', margin=0.01)
    import materials as MT
    b.box((0, -0.05, 0), (2, 0.05, 2), MT.PAINT, op=S.UNION)
    P, G = b.build()
    GB = b.grid_buffer()
    SP = new_params()
    SP[65] = 1
    Lt = default_lights()
    Lt[:, 7] = 0
    imgs = []
    for ang in (180, 90, 0, 35):
        a = np.radians(ang)
        pos = (2.6 * np.sin(a), 1.1, 2.6 * np.cos(a) - 0.0)
        cam = S.camera(pos, (0, 0.6, 0), 32, 0.75)
        res = S.render_image(360, 480, cam, P, G, mat_table(), Lt, SP, GB, None, None, bands=4, verbose=False)
        imgs.append((S.tonemap(res['rgb'], 1.0) * 255).astype(np.uint8))
    Image.fromarray(np.concatenate(imgs, 1)).save(out)
    print('saved', out, 'forehead', forehead(st))


if __name__ == '__main__':
    if sys.argv[1] == 'look':
        look(sys.argv[2])
