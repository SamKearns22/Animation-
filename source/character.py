"""The mother, built on MakeHuman's measured human (see mhuman.py and guides/character-anatomy.md).

Produces the pieces the scene needs, each as a distance grid in its own local frame:
- her head and neck, in head coordinates (origin midway between the eyeballs, x to her left, y up, z out of
  the face - the same frame the hair, eyes and face shading already use), smiling;
- her right hand closed round the cleaver handle, in a frame fixed to the handle;
- her left hand resting on the meat, in a frame fixed to the palm.
Everything is cached on disk, keyed by the code and settings, since each piece takes a minute or two.
"""
import numpy as np

import mesh_sdf
import mhuman as H

SHAPE = dict(gender=0.0, age=0.577, muscle=0.5, weight=0.45, height=0.6, proportions=0.8)  # ~35, slim, 1.75 m

# her own face (MakeHuman's regional sliders): finer nose, fuller lips, higher cheekbones, a neat chin, and the
# small asymmetries every real face has
FACE = {
    'head/head-oval': 0.45, 'head/head-invertedtriangular': 0.3, 'head/head-age-decr': 0.2,
    'forehead/forehead-nubian-decr': 0.3, 'forehead/forehead-temple-decr': 0.2,
    'eyebrows/eyebrows-trans-up': 0.15, 'eyebrows/eyebrows-angle-up': 0.2,
    'nose/nose-scale-horiz-decr': 0.30, 'nose/nose-nostrils-width-decr': 0.35, 'nose/nose-point-width-decr': 0.35,
    'nose/nose-volume-decr': 0.2, 'nose/nose-point-up': 0.15, 'nose/nose-hump-decr': 0.3,
    'mouth/mouth-upperlip-volume-incr': 0.75, 'mouth/mouth-lowerlip-volume-incr': 0.65,
    'mouth/mouth-upperlip-height-incr': 0.3, 'mouth/mouth-lowerlip-height-incr': 0.3,
    'mouth/mouth-cupidsbow-incr': 0.4, 'mouth/mouth-scale-horiz-incr': 0.1,
    'cheek/l-cheek-bones-incr': 0.35, 'cheek/r-cheek-bones-incr': 0.30,
    'chin/chin-width-decr': 0.30, 'chin/chin-prominent-decr': 0.1, 'chin/chin-height-decr': 0.15,
    'eyes/l-eye-scale-incr': 0.15, 'eyes/r-eye-scale-incr': 0.15,
    'eyes/l-eye-height2-incr': 0.2, 'eyes/r-eye-height2-incr': 0.2,
    'eyes/l-eye-corner2-up': 0.2, 'eyes/r-eye-corner2-up': 0.2,
    'neck/neck-scale-horiz-decr': 0.25,
    'asym/asym-eye-1-l': 0.3, 'asym/asym-mouth-1-r': 0.3, 'asym/asym-nose-1-l': 0.2, 'asym/asym-brown-1-r': 0.3,
}

# a warm, genuine smile (the Duchenne markers: cheeks up, lower lids up, mouth corners up, smile lines a
# little deeper, brows down a touch), slightly stronger on her left; kept gentle so the eyes stay open
SMILE = {'LeftCheekUp': 0.55, 'RightCheekUp': 0.45, 'LeftLowerLidUp': 0.20, 'RightLowerLidUp': 0.17,
         'MouthLeftPullUp': 0.50, 'MouthRightPullUp': 0.42, 'MouthLeftPullSide': 0.08,
         'MouthRightPullSide': 0.06, 'NasolabialDeepener': 0.20, 'LeftBrowDown': 0.10, 'RightBrowDown': 0.08,
         'LeftUpperLidClosed': 0.03, 'RightUpperLidClosed': 0.03}

HANDLE_R = 0.0125           # cleaver handle radius, metres
HAND_BONES = ('wrist', 'metacarpal', 'finger')


def base_body():
    v, g = H.load_base()
    H.apply_macros(v, H.macro_values(**SHAPE))
    H.apply_details(v, FACE)
    return v, g, H.Skeleton(v)


def _grid_of(V, quads, lo, hi, voxel):
    V2, q2 = mesh_sdf.catmull_clark(V, quads)
    V2, q2 = mesh_sdf.catmull_clark(V2, q2)
    return mesh_sdf.mesh_to_sdf(V2, mesh_sdf.triangulate(q2), lo, hi, voxel)


def head_grid(voxel=0.001):
    """Head and neck, smiling, in head coordinates (metres). Returns ((lo, d, voxel), eyes) with eyes as a list
    of (centre, radius) in head coordinates, her right eye first."""
    v, g, sk = base_body()
    v = sk.skin(v, sk.localize(H.blend_units(H.face_units(), SMILE)))
    eyes = []
    for side in ('r', 'l'):
        idx = np.unique(np.concatenate([np.array(f) for f in g['helper-%s-eye' % side]]))
        c = v[idx].mean(0)
        eyes.append((c, np.linalg.norm(v[idx] - c, axis=1).mean()))
    mid = (eyes[0][0] + eyes[1][0]) / 2
    V = (v - mid) * 0.1
    eyes = [((c - mid) * 0.1, r * 0.1) for c, r in eyes]
    lo, hi = np.array([-0.100, -0.215, -0.135]), np.array([0.100, 0.140, 0.125])
    keep = [f for f in g['body'] if np.all(V[f][:, 1] > lo[1] - 0.03) and np.all(np.abs(V[f][:, 0]) < 0.2)]
    return _grid_of(V, keep, lo, hi, voxel), eyes


def _hand_faces(g, sk, v, side):
    """Faces of one hand and wrist: those whose vertices are mostly moved by hand bones."""
    own = np.zeros(len(v))
    tot = np.zeros(len(v))
    for b, (idx, w) in sk.weights.items():
        tot[idx] += w
        if b.endswith('.' + side) and b.startswith(HAND_BONES):
            own[idx] += w
    part = own / np.maximum(tot, 1e-9) > 0.5
    return [f for f in g['body'] if part[f].all()]


def right_hand():
    """Right hand closed round the handle. Grid in the handle frame: x along the handle towards the blade
    (the index finger's side), y from the handle axis towards the middle knuckle, z = x cross y; origin on the
    axis level with the middle finger. Returns ((lo, d, voxel), wrist position, forearm direction), all in that
    frame (metres)."""
    v, g, sk = base_body()
    local, c, d, err = H.solve_grip(sk, 'R', HANDLE_R * 10)
    M = sk.pose_matrices(local)
    v2 = sk.skin(v, local)
    k_mid = H.bone_ends(sk, M, 'finger3-1.R')[0]
    k_idx = H.bone_ends(sk, M, 'finger2-1.R')[0]
    k_lit = H.bone_ends(sk, M, 'finger5-1.R')[0]
    if (k_idx - k_lit) @ d < 0:
        d = -d
    o = c + d * ((k_mid - c) @ d)
    y = k_mid - o
    y -= d * (y @ d)
    y /= np.linalg.norm(y)
    z = np.cross(d, y)
    R = np.stack([d, y, z], 1)              # columns: frame axes in MakeHuman space
    V = (v2 - o) @ R * 0.1
    wr = (sk.rest['wrist.R'][:3, 3] - o) @ R * 0.1
    fore = (sk.rest['lowerarm02.R'][:3, 3] - sk.rest['wrist.R'][:3, 3]) @ R
    wx, _, wz = (a @ R for a in sk.axes('wrist.R'))
    faces = _hand_faces(g, sk, v, 'R')
    pts = V[np.unique(np.concatenate([np.array(f) for f in faces]))]
    lo, hi = pts.min(0) - 0.012, pts.max(0) + 0.012
    return _grid_of(V, faces, lo, hi, 0.0007), wr, fore / np.linalg.norm(fore), wx, wz


def left_hand():
    """Left hand lying relaxed on the meat, fingers gently curved. Grid in the palm frame: x along the middle
    finger, y out of the back of the hand, z = x cross y; origin at the centre of the palm's skin. Returns
    ((lo, d, voxel), wrist position, forearm direction) in that frame (metres)."""
    v, g, sk = base_body()
    bends = {2: (10, 14, 8), 3: (12, 16, 9), 4: (14, 18, 10), 5: (16, 20, 12)}
    local = {}
    for f, angs in bends.items():
        for k, a in enumerate(angs):
            local['finger%d-%d.L' % (f, k + 1)] = H.axis_angle([1, 0, 0], a)
    local['finger1-2.L'] = H.axis_angle([1, 0, 0], 8)
    M = sk.pose_matrices(local)
    v2 = sk.skin(v, local)
    h3, t3 = H.bone_ends(sk, M, 'metacarpal3.L')
    h2, _ = H.bone_ends(sk, M, 'metacarpal2.L')
    h4, _ = H.bone_ends(sk, M, 'metacarpal4.L')
    x = t3 - h3
    x /= np.linalg.norm(x)
    across = h2 - h4
    y = np.cross(across, x)                  # back of the hand, for a left hand
    tip = H.bone_ends(sk, M, 'finger3-3.L')[1]
    if (tip - t3) @ y > 0:                   # flexion curls towards the palm, so the back is the other side
        y = -y
    y -= x * (y @ x)
    y /= np.linalg.norm(y)
    z = np.cross(x, y)
    R = np.stack([x, y, z], 1)
    faces = _hand_faces(g, sk, v, 'L')
    idx = np.unique(np.concatenate([np.array(f) for f in faces]))
    centre = (h3 + t3) / 2
    # the palm's skin: the lowest hand point below the centre, measured along -y
    below = v2[idx][np.linalg.norm(np.cross(v2[idx] - centre, y), axis=1) < 0.12]
    o = centre + y * ((below - centre) @ y).min()
    V = (v2 - o) @ R * 0.1
    wr = (sk.rest['wrist.L'][:3, 3] - o) @ R * 0.1
    fore = (sk.rest['lowerarm02.L'][:3, 3] - sk.rest['wrist.L'][:3, 3]) @ R
    wx, _, wz = (a @ R for a in sk.axes('wrist.L'))
    pts = V[idx]
    lo, hi = pts.min(0) - 0.012, pts.max(0) + 0.012
    return _grid_of(V, faces, lo, hi, 0.0007), wr, fore / np.linalg.norm(fore), wx, wz


def hands():
    return right_hand(), left_hand()
