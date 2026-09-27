#!/usr/bin/env python3
"""Quick looks at the MakeHuman-based character: head (front, three-quarter, profile, close) and hands.

Usage:
    python3 mh_lab.py head OUT.png
"""
import sys
import time

import numpy as np
from PIL import Image

import mesh_sdf
import mhuman as H
import sdf3d as S
from mother_scene import mat_table, new_params, SKIN, EYE


def build_mesh(shape=None, details=None, local=None):
    """The shaped, posed body mesh in metres: (verts, quads of the skin, eye centres and radius)."""
    v, g = H.load_base()
    H.apply_macros(v, H.macro_values(**(shape or {})))
    H.apply_details(v, details or {})
    sk = H.Skeleton(v)
    if local:
        v = sk.skin(v, sk.localize(local))
    eyes = []
    for side in ('l', 'r'):
        idx = np.unique(np.concatenate([np.array(f) for f in g['helper-%s-eye' % side]]))
        c = v[idx].mean(0)
        eyes.append((c * 0.1, np.linalg.norm(v[idx] - c, axis=1).mean() * 0.1))
    return v * 0.1, g['body'], eyes, sk


def head_sdf(V, quads, voxel=0.001, box=None):
    lo, hi = box
    keep = [f for f in quads if np.all(V[f][:, 1] > lo[1] - 0.03)]
    V2, q2 = mesh_sdf.catmull_clark(V, keep)
    V2, q2 = mesh_sdf.catmull_clark(V2, q2)
    T = mesh_sdf.triangulate(q2)
    return mesh_sdf.mesh_to_sdf(V2, T, lo, hi, voxel)


def render_views(grid, eyes, out, centre, size=0.30):
    b = S.Builder()
    b.set_frame((0, 0, 0), None)
    b.group('head', margin=0.01)
    lo, d, voxel = grid
    b.grid(lo, d, voxel, SKIN, op=S.UNION)
    for c, r in eyes:
        b.sphere(c, r, EYE, op=S.UNION)
    P, G = b.build()
    GB = b.grid_buffer()
    SP = new_params()
    SP[0:3] = (100.0, 100.0, 100.0)  # no painted-on face features: the geometry has to carry the face
    SP[3:12] = np.eye(3).reshape(-1)
    for e, (ec, er) in enumerate(eyes):
        SP[12 + 3 * e:15 + 3 * e] = ec
    SP[18:21] = (0.0, -0.05, 1.0) / np.linalg.norm((0.0, -0.05, 1.0))
    SP[21] = np.arcsin(min(0.0059 / eyes[0][1], 0.99))
    SP[22] = np.arcsin(min(0.0020 / eyes[0][1], 0.99))
    M = mat_table()
    key = np.array([0.55, 0.55, 0.65])
    key /= np.linalg.norm(key)
    Lt = np.array([[0, *key, 1.30, 1.26, 1.20, 2, 0, 0, 0, 1],
                   [0, -0.6, 0.3, -0.7, 0.45, 0.48, 0.55, 0, 0, 0, 0, 0]], dtype=np.float64)
    sm = S.ShadowMaps()
    sm.add(P, G, GB, key, centre, 0.5, 1600, np.tan(np.radians(7)))
    SM, SMP = sm.arrays()
    c = np.asarray(centre)
    views = [(c + [0, 0.02, 1.2], 14), (c + [0.75, 0.10, 0.95], 14), (c + [1.2, 0.02, 0.0], 14),
             (c + [0.45, 0.05, 0.6], 9)]
    tiles = []
    for pos, fov in views:
        cam = S.camera(tuple(pos), tuple(c), fov, 1.0)
        res = S.render_image(640, 640, cam, P, G, M, Lt, SP, GB, SM, SMP, bands=2, verbose=False)
        tiles.append((S.tonemap(res['rgb'], 1.05) * 255).astype(np.uint8))
    Image.fromarray(np.concatenate([np.concatenate(tiles[:2], 1), np.concatenate(tiles[2:], 1)], 0)).save(out)


def head_test(out, shape=None, details=None, local=None):
    t0 = time.time()
    V, quads, eyes, sk = build_mesh(shape, details, local)
    head = sk.rest['head'][:3, 3] * 0.1
    lo = head + np.array([-0.11, -0.16, -0.14])
    hi = head + np.array([0.11, 0.17, 0.16])
    grid = head_sdf(V, quads, 0.001, (lo, hi))
    print(f'sdf {time.time() - t0:.0f}s', flush=True)
    centre = (eyes[0][0] + eyes[1][0]) / 2 + np.array([0, -0.03, 0])
    render_views(grid, eyes, out, centre)
    print('saved', out, f'{time.time() - t0:.0f}s')


YOUNG_WOMAN = dict(gender=0.0, age=0.577, muscle=0.5, weight=0.45, height=0.6, proportions=0.8)
# her own face, from MakeHuman's regional sliders (see guides/character-anatomy.md, section 4): a softer,
# more feminine structure - finer nose, fuller lips, higher cheekbones, a neat chin - and the small
# asymmetries every real face has
MOTHER_FACE = {
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
# a warm, genuine smile (the Duchenne markers: cheeks up, lower lids up, mouth corners up and back, a little
# deepening of the smile lines, brows down a touch) - slightly stronger on her left, as real faces are
GENTLE_SMILE = {'LeftCheekUp': 0.55, 'RightCheekUp': 0.45, 'LeftLowerLidUp': 0.35, 'RightLowerLidUp': 0.30,
                'MouthLeftPullUp': 0.50, 'MouthRightPullUp': 0.42, 'MouthLeftPullSide': 0.08,
                'MouthRightPullSide': 0.06, 'NasolabialDeepener': 0.20, 'LeftBrowDown': 0.10,
                'RightBrowDown': 0.08,
                # relaxed upper lids: resting just over the top of the iris, not staring
                'LeftUpperLidClosed': 0.10, 'RightUpperLidClosed': 0.10}

if __name__ == '__main__':
    if sys.argv[1] == 'head':
        head_test(sys.argv[2], YOUNG_WOMAN)
    if sys.argv[1] == 'smile':
        head_test(sys.argv[2], YOUNG_WOMAN, local=H.blend_units(H.face_units(), GENTLE_SMILE))
    if sys.argv[1] == 'mother':
        head_test(sys.argv[2], YOUNG_WOMAN, MOTHER_FACE, local=H.blend_units(H.face_units(), GENTLE_SMILE))
