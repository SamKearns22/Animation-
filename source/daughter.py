"""The daughter: a slight, fair girl of about six or seven, "a straw hair waif with curious eyes", in a droopy
felt Santa hat. Blank, mildly curious. (See story/animation-test.md.)

Built like her mother on MakeHuman's measured body (rig.py, character.py). Her face is her own - drawn from
the qualities the director's reference photos share, not copied from any one face: large, wide-set, pale
eyes under soft lids and fairly straight light brows; a soft, rounded face with full cheeks; a small nose
turned up at the tip; small closed lips; a small rounded chin; and the small asymmetries every real face has.

    python3 daughter.py head OUT.png        quick look at her head: front, three-quarter, profile, close
"""
import sys

import numpy as np

import character as C
from cache import cached

# about 6-7 years old, slight and small for her age: 1.16 m, eyes 1.06 m - just over the worktop (0.92 m).
# (MakeHuman's age slider mixes a baby and a child shape below 11; a little past halfway keeps her a girl, not
# a toddler, and the height slider brings her down to size.)
SHAPE = dict(gender=0.0, age=0.14, muscle=0.45, weight=0.35, height=0.6, proportions=0.5)

FACE = {
    # a soft oval narrowing to a small, neat chin (a little heart-shaped)
    'head/head-oval': 0.35, 'head/head-invertedtriangular': 0.25,
    # large, wide-set, almond eyes; soft lids
    'eyes/l-eye-scale-incr': 0.60, 'eyes/r-eye-scale-incr': 0.60,
    'eyes/l-eye-trans-out': 0.12, 'eyes/r-eye-trans-out': 0.12,
    'eyes/l-eye-corner2-up': 0.10, 'eyes/r-eye-corner2-up': 0.10,
    # fairly straight brows
    'eyebrows/eyebrows-angle-down': 0.15,
    # a small nose with a gently turned-up tip; neat nostrils
    'nose/nose-point-down': 0.12, 'nose/nose-nostrils-angle-down': 0.35, 'nose/nose-scale-horiz-decr': 0.20, 'nose/nose-nostrils-width-decr': 0.30,
    'nose/nose-volume-decr': 0.15, 'nose/nose-flaring-decr': 0.25,
    # small, soft, closed lips with a clear bow - not pouting
    'mouth/mouth-scale-horiz-decr': 0.15, 'mouth/mouth-cupidsbow-incr': 0.30,
    'mouth/mouth-lowerlip-volume-decr': 0.15, 'mouth/mouth-upperlip-volume-decr': 0.10,
    'mouth/mouth-trans-backward': 0.35, 'mouth/mouth-trans-up': 0.25, 'mouth/mouth-scale-depth-decr': 0.35, 'chin/chin-prominent-incr': 0.10,
    # soft cheeks (not chubby), a small chin
    'cheek/l-cheek-volume-incr': 0.12, 'cheek/r-cheek-volume-incr': 0.08,
    'chin/chin-width-decr': 0.25, 'chin/chin-height-incr': 0.10,
    # small asymmetries
    'asym/asym-eye-1-r': 0.25, 'asym/asym-mouth-1-l': 0.20, 'asym/asym-nose-1-r': 0.15, 'asym/asym-brown-1-l': 0.20,
}

IRIS = (0.28, 0.36, 0.42)   # pale blue-grey

# blank and mildly curious: brows lifted a touch (more on one side), eyes a little wider, mouth relaxed and
# closed with the barest hint at one corner - not a smile
CURIOUS = {'LeftInnerBrowUp': 0.15, 'RightInnerBrowUp': 0.11, 'LeftOuterBrowUp': 0.06, 'RightOuterBrowUp': 0.10,
           'LeftUpperLidClosed': 0.12, 'RightUpperLidClosed': 0.10, 'LeftLowerLidUp': 0.30, 'RightLowerLidUp': 0.34,
           'MouthLeftPullUp': 0.05}
IRIS_RADIUS, PUPIL_RADIUS = 0.0060, 0.0016   # a child's iris is nearly adult-sized; a small daylight pupil


# her pale long-sleeved top: thin cotton, close but not tight, a soft crew neck
TOP = dict(thick=0.005, drape=0.6, bridge=0.015, smooth=0.008, hem=0.06, cuff=0.010, voxel=0.002,
           collar=('crew', 0.046, 0.006))

# long, fine, straight-to-softly-waved straw-blonde hair from a centre parting, falling forward over both
# shoulders, with stray strands catching the light (it comes out from under the hat's fur band)
HAIRLINE = (0.056, 0.014, 0.040, 0.048)
HAIR = dict(scalp_c=(0.0, 0.020, -0.052), scalp_r=(0.066, 0.086, 0.086), part=np.radians(-4.0),
            hairline=HAIRLINE, top=(34, 36), under=40, length_top=(0.20, 0.38), length_under=(0.22, 0.35),
            r_top=(0.0030, 0.0080), r_under=(0.0045, 0.0085), wave=(0.12, 0.22, 0.10), fullness=0.24,
            forward='both', crown_lift=0.003, flyaways=(25, 0.0009, 0.06), base=(0.005, 0.009),
            box=((-0.26, -0.48, -0.26), (0.28, 0.16, 0.22)), voxel=0.0014, seed=5, close=0.0015,
            shoulder_drop=0.09)

# her hands resting on the worktop, fingers loosely curled
BENDS = {2: (6, 10, 6), 3: (7, 11, 6), 4: (8, 12, 7), 5: (10, 14, 8)}

_BODY = []


def body():
    import rig
    if not _BODY:
        _BODY.append(rig.Body(SHAPE, FACE))
    return _BODY[0]


def deps():
    import mother
    return mother.mh_deps() + [SHAPE, FACE, CURIOUS]


def head_parts():
    """Her head and neck with her expression, in head coordinates: ((lo, d, voxel), eyes)."""
    # (a child's neck is short: keep only down to the collar, or the skin of her chest would show through her top)
    return cached('girlhead', lambda: C.head_grid(0.001, SHAPE, FACE, CURIOUS, below=0.125), deps())


def hand_parts():
    """Her right and left hands lying relaxed, as (grid, wrist, forearm direction, wrist axes) in palm frames."""
    return cached('girlhands', lambda: (C.left_hand(SHAPE, FACE, 'R', BENDS, 6), C.left_hand(SHAPE, FACE, 'L', BENDS, 6)),
                  deps() + [C.left_hand, BENDS])


def hat_parts():
    import hat
    return cached('girlhat', lambda: hat.make(head_parts()[0], side=1.0),
                  deps() + [hat.make, hat._capsule_chain, hat._fbm, hat.bezier])


def eyes_mid_rest():
    b = body()
    cs = []
    for side in ('r', 'l'):
        idx = np.unique(np.concatenate([np.array(f) for f in b.groups['helper-%s-eye' % side]]))
        cs.append(b.v_dm[idx].mean(0))
    return b.to_m((cs[0] + cs[1]) / 2)


def solve(spec):
    """Her pose from a shot's description. spec keys:
      position, yaw          where she stands and which way she faces (180: towards her mother)
      lean                   degrees she leans forward over the island
      look_at                the point she stares at (her head turns head_share of the way, eyes the rest)
      hands                  {'R': (palm point, finger direction), 'L': ...} her hands resting on a surface
      rest_on                height of the surface the hands rest on
      poles                  points her right and left elbows point towards
    """
    import mhuman as MH
    import rig
    from mother import surface_points, wrist_bend
    from rig import unit
    from sdf3d import rot
    b = body()
    pose = rig.Pose(b, spec['position'], spec.get('yaw', 0.0))
    lean = spec.get('lean', 0.0)
    for bone in ('spine04', 'spine03', 'spine02'):
        pose.rot[bone] = MH.axis_angle([1, 0, 0], lean / 3)
    look = np.asarray(spec['look_at'], float)
    pose.aim_head(np.eye(3))
    M0 = pose.matrices()
    d = pose.world_R().T @ unit(look - pose.point(M0, 'head', eyes_mid_rest()))
    share = spec.get('head_share', 0.7)
    pose.aim_head(rot(np.degrees(np.arctan2(d[0], d[2])) * share, np.degrees(np.arcsin(-d[1])) * share,
                      spec.get('head_roll', 0.0)))
    hands, bends, short = [], [], []
    up = np.array([0, 1.0, 0])
    for i, s in enumerate('RL'):
        grid, wr, fore, wx, wz = hand_parts()[i]
        palm, fdir = spec['hands'][s]
        x = unit(np.asarray(fdir, float) - up * (np.asarray(fdir, float) @ up))
        R = np.stack([x, up, np.cross(x, up)], 1)
        o = np.asarray(palm, float).copy()
        pts = surface_points(grid)
        o[1] += spec['rest_on'] + 0.001 - (o + pts @ R.T)[:, 1].min()     # resting on the surface
        w = o + R @ wr
        e, sh = pose.arm_ik(s, w, spec['poles'][i])
        hands.append((o, R, w))
        short.append(sh)
    M = pose.matrices()
    J = pose.joints(M)
    for i, s in enumerate('RL'):
        o, R, w = hands[i]
        part = hand_parts()[i]
        bends.append(wrist_bend(R, part[2], part[3], part[4], unit(J['elbow.' + s] - w)))
    Hc = pose.point(M, 'head', eyes_mid_rest())
    Rh = M['head'][:3, :3]
    gaze = tuple(Rh.T @ unit(look - Hc))
    return dict(spec=dict(spec, gaze=gaze), pose=pose, M=M, joints=J, hands=hands, bends=bends, short=tuple(short),
                head=(Hc, Rh))


def prepare(state):
    import clothes
    import hair
    import hat as hatmod
    import rig
    from mother import pose_key, torso_key
    b = body()
    state['top'] = cached('girltop', lambda key: clothes.top(b, state['pose'], state['joints'], TOP),
                          [clothes.top, TOP, clothes.TORSO, rig.Body.skin, rig.Body.surface, rig.Body.part_map,
                           rig.drape, rig.robust_distance] + deps(), pose_key(state))
    Hc, Rh = state['head']
    ht = hat_parts()
    under = hatmod.hidden(ht)
    state['hat'] = ht
    state['hair'] = cached('girlhair', lambda key: hair.grid(HAIR, Hc, Rh, head_parts()[0],
                                                             (state['top'], (ht['felt'], Hc, Rh), (ht['fur'], Hc, Rh)),
                                                             hides=lambda p: under(Rh.T @ (p - Hc))),
                           hair.DEPS + [HAIR, rig.smin, rig.robust_distance] + deps() + [hatmod.make],
                           (np.round(Hc, 5).tolist(), np.round(Rh, 5).tolist(), torso_key(state)))
    return state


def build(b, state):
    import sdf3d as S
    from materials import SKIN, EYE, FELT, FUR, STRAW_HAIR, COTTON
    Hc, Rh = state['head']
    b.set_frame(Hc, Rh)
    b.group('girl_head', margin=0.01)
    (lo, d, vox), eyes = head_parts()
    b.grid(lo, d, vox, SKIN, op=S.UNION)
    for c, r in eyes:
        b.sphere(c, r, EYE, op=S.UNION)
    ht = state['hat']
    b.group('girl_hat', margin=0.01)
    b.grid(*ht['felt'], FELT, op=S.UNION)
    b.group('girl_hat_fur', margin=0.01)
    b.grid(*ht['fur'], FUR, op=S.UNION)
    b.set_frame((0, 0, 0), None)
    lo, d, vox, flow = state['hair']
    b.group('girl_hair', disp=S.D_HAIR, dparams=[Hc[0], Hc[1], Hc[2], 0.08, 0.07, 0.0003], margin=0.01)
    b.grid(lo, d, vox, STRAW_HAIR, op=S.UNION)
    lo, d, vox, part = state['top']
    b.group('girl_top', margin=0.01)
    b.grid(lo, d, vox, COTTON, op=S.UNION)
    for name, (o, R, _), part_ in zip(('girl_right_hand', 'girl_left_hand'), state['hands'], hand_parts()):
        b.set_frame(o, R)
        b.group(name, margin=0.01)
        b.grid(part_[0][0], part_[0][1], part_[0][2], SKIN, op=S.UNION)
    b.set_frame((0, 0, 0), None)


def pieces(state, pov=False):
    """Every grid of her in the scene, as (grid, origin, rotation)."""
    Hc, Rh = state['head']
    ht = state['hat']
    out = [(head_parts()[0], Hc, Rh), (ht['felt'], Hc, Rh), (ht['fur'], Hc, Rh), (state['hair'][:3], None, None),
           (state['top'][:3], None, None)]
    for (o, R, _), part in zip(state['hands'], hand_parts()):
        out.append((part[0], o, R))
    return out


# her painted details: lips mapped from her mother's measured mouth by the lip bones; fine, light brows; rosy
# cheeks
LIPS = [0.017, -0.0435, -0.0377, 0.0008, -0.0473, -0.0566]
BROWS = [0.010, 0.044, 0.0150, 0.0025, 0.007, 0.0019]


def fill_params(SP, state):
    from rig import unit
    Hc, Rh = state['head']
    eyes = head_parts()[1]
    SP[0:3] = Hc
    SP[3:12] = Rh.reshape(-1)
    for e, (c, r) in enumerate(eyes):
        SP[12 + 3 * e:15 + 3 * e] = Hc + Rh @ c
    SP[18:21] = Rh @ unit(state['spec']['gaze'])
    SP[21] = np.arcsin(min(IRIS_RADIUS / eyes[0][1], 0.99))
    SP[22] = np.arcsin(min(PUPIL_RADIUS / eyes[0][1], 0.99))
    SP[29] = abs(eyes[0][0][0])
    SP[40:46] = BROWS
    SP[100:106] = LIPS
    SP[107:110] = (0.80, 0.47, 0.47)
    SP[110:114] = HAIRLINE
    SP[114] = 1.0
    SP[125:128] = IRIS
    SP[128] = 0.22      # light, fine brows
    SP[129] = 0.12      # rosy cheeks


def head_test(out):
    import mh_lab
    (lo, d, vox), eyes = head_parts()
    centre = np.array([0.0, -0.03, 0.0])
    mh_lab.render_views((lo, d, vox), eyes, out, centre, size=0.24, iris=IRIS, radii=(IRIS_RADIUS, PUPIL_RADIUS))
    print('saved', out)


if __name__ == '__main__':
    if sys.argv[1] == 'head':
        head_test(sys.argv[2])
