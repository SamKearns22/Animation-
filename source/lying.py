#!/usr/bin/env python3
"""lying: people lying down, and people seen from a high camera, with real depth (Build list item 12, Sam 25 Oct;
Poker Mon note 80: "players who land flat on the table look like 2D paper ... a cardboard cut out").

Why: Poker Mon's faceplant built a lying body from 3D tubes but outlined every tube by itself (it read as cut-out
pieces), filled each flat with no shadow side and no clothes; and views.py drew everyone as if the camera were just
above eye level, so from a high camera a person stayed an upright flat picture.

- One 3D skeleton in metres (`Body`: pelvis, waist, neck, head and its facing, shoulders, elbows, wrists, hips,
  knees, ankles, which way each shoe points), so a body lies in true perspective from any camera (sets.Cam).
  Poses (`POSES`): 'face_down', 'back', 'side' (curled), 'slump' (sat against a wall). `place` puts one in the
  room; `settle` drops it onto the floor (or table top) so it rests, never floats or sinks.
- Drawn as ONE body (`draw`): rounded volumes (head, chest, hips, arms, legs, shoes; circle hands) traced through
  the camera, then one outline round the whole silhouette and a line only where a part lies over another (an arm
  over the chest, one leg over the other) or two colours meet; flat fills with one darker shadow tone on the side
  away from the light (house style, no gradient); collar, tie or bow tie, cuffs, jacket hem, belt (outfits with
  no jacket), shoe soles; the person's own face and hair (the library drawings, burnham.head and views' back of
  the head) laid onto the head, so the face turns with it through the camera. A flat contact shadow on the floor
  (and the wall) where the body rests on it.
- Checks (`contact_faults`): every part a pose rests on touches the surface (within 1.5 cm), nothing passes
  through it (more than 0.5 cm). `solids` hands the body to the collision audit (clipcheck capsules; rule 12).
- `fall`: moves.fall's knees and hips stages (the flat drawing), then from the moment the hips land the 3D body
  takes over from that exact pose (`from_views`) and settles into the lying pose: no pop (checked: `check`).
- `stand`: anyone from a 3D set camera at its real tilt: up to views.HIGH (40 degrees) the flat drawing
  (views.person(tilt=...): more shoulders and shoe tops, shorter legs, a floor shadow); steeper, the 3D body of
  the same pose (head top and shoulders, the feet under the body).

    python3 source/lying.py sheet OUT.jpg     the test sheet (three people, every pose, four camera heights)
    python3 source/lying.py check             contacts for every pose and person, and the fall's hand-over
"""
import math
import os
import sys

import numpy as np
from numba import njit, prange
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import clipcheck as CC       # noqa: E402
import figure as F           # noqa: E402
import moves                 # noqa: E402
import sets as S             # noqa: E402
import views as V            # noqa: E402
from ed import INK           # noqa: E402

M = V.M_PER_UNIT                                     # metres per person unit
UPPER, FORE = F.UPPER * 0.98 * M, F.FORE * 0.98 * M  # the rig's bones, in metres
THIGH, SHIN = V.THIGH * M, V.SHIN * M
NECK_HEAD = 150 * M                                  # neck base to the head's centre
SHADE = 0.8                                          # the shadow side: one darker tone
SOLE_C = (120, 100, 86)


def _v(*a):
    return np.array(a, float)


def _unit(a):
    a = np.asarray(a, float)
    return a / (np.linalg.norm(a) or 1.0)


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


# ------------------------------------------------------------------------------------------------ the skeleton
POINTS = ('pelvis', 'waist', 'neck', 'head', 'shL', 'elL', 'wrL', 'shR', 'elR', 'wrR', 'hipL', 'knL', 'anL',
          'hipR', 'knR', 'anR')
DIRS = ('hup', 'hfwd', 'fwd', 'toeL', 'toeR', 'supL', 'supR')


class Body(dict):
    """One person's 3D skeleton in metres (world: y up). Points: POINTS; unit directions: DIRS (hup / hfwd the
    head's crown and face; fwd the chest's front; toe* where each shoe points, sup* from its sole to its top)."""

    def copy(self):
        return Body({k: np.array(v, float) for k, v in self.items()})


def limb(root, target, l1, l2, pole):
    """Two bones (metres) from root towards target, the middle joint bending towards `pole`: (middle, end)."""
    mid, end = V.ik3(tuple(root), tuple(target), l1, l2, tuple(pole))
    return np.array(mid), np.array(end)


def _thigh_r(sp):
    """The thigh's radius at the hip and the knee (fuller under a gown)."""
    return (0.092, 0.084) if sp.get('outfit') == 'dress' else (0.078, 0.064)


def _limb_clear(root, target, l1, l2, pole, r_mid, floor):
    """limb(), but a joint never in the floor: the elbow or knee is turned up off it (its bend lifted) until it
    rests on it at most."""
    pole = np.asarray(pole, float)
    target = np.asarray(target, float)
    mid, end = limb(root, target, l1, l2, pole)
    for _ in range(40):
        if floor is None or mid[1] - r_mid >= floor - 0.002:
            break
        pole = pole + _v(0, 0.3, 0)
        mid, end = limb(root, target, l1, l2, pole)
    return mid, end


def _build(pelvis, waist, neck, X, hup, hfwd, arms, legs, sp, floor=0.0, shrug=None, hips_off=(0, 0, 0)):
    """A Body from its spine, its right-hand direction X, the head's directions and the limbs: arms = {side:
    (hand target, elbow pole)}, legs = {side: (ankle target, knee pole, toe direction, sole-to-top)}. No shoulder,
    elbow or knee goes into the floor (y = floor; None: no floor check); `shrug` = {side: (in, forward)} pulls a
    shoulder in towards the neck and forward (metres): the lower shoulder of someone on their side rolls forward;
    `hips_off` moves the hip joints off the pelvis's centre (lying flat they sit nearer the floor, so the thighs
    rest on it)."""
    pelvis, waist, neck = _v(*pelvis), _v(*waist), _v(*neck)
    up = _unit(neck - pelvis)
    X = _unit(np.asarray(X, float) - up * np.dot(X, up))
    fwd = np.cross(X, up)
    hup = _unit(hup)
    hfwd = _unit(np.asarray(hfwd, float) - hup * np.dot(hfwd, hup))
    k = Body(pelvis=pelvis, waist=waist, neck=neck, fwd=fwd, hup=hup, hfwd=hfwd,
             head=neck + _unit(up * 0.45 + hup * 0.55) * NECK_HEAD)
    sw = (sp.get('shoulders', 150) - 14) * M
    tr = _thigh_r(sp)
    hw = 0.52 * 0.82 * sp.get('shoulders', 150) * M * B.HEM - 2 * (tr[0] - 0.078)   # hip joints inside the hips
    if hips_off[1] < 0:                                  # lying flat: fuller thighs (a gown) sit their centre higher
        hips_off = (hips_off[0], hips_off[1] + tr[0] - 0.078, hips_off[2])
    for side, sg in (('L', -1), ('R', 1)):
        sin, sfw = (shrug or {}).get(side, (0.0, 0.0))
        sh = neck + X * sg * (sw - sin) - up * 0.06 + fwd * sfw
        k['sh' + side] = sh
        tgt, pole = arms[side]
        k['el' + side], k['wr' + side] = _limb_clear(sh, tgt, UPPER, FORE, pole, 0.05, floor)
        hip = pelvis + X * sg * hw + _v(*hips_off)
        k['hip' + side] = hip
        tgt, pole, toe, sup = legs[side]
        k['kn' + side], k['an' + side] = _limb_clear(hip, tgt, THIGH, SHIN, pole, tr[1], floor)
        k['toe' + side] = _unit(toe)
        k['sup' + side] = _unit(np.asarray(sup, float) - k['toe' + side] * np.dot(sup, k['toe' + side]))
    return k


def _head_down(k, sp, floor=0.0):
    """The head let down onto the floor (or up off it): turned about the neck until it just rests on it."""
    def gap(kk):
        return [q for q in parts(kk, sp) if q.name == 'head'][0].low(_v(0, 1, 0), _v(0, floor, 0))
    up = _unit(k['neck'] - k['pelvis'])
    for _ in range(60):
        g = gap(k)
        if abs(g) < 0.004:
            break
        step = _v(0, -0.04 if g > 0 else 0.04, 0)
        k['hup'] = _unit(k['hup'] + step)
        k['hfwd'] = _unit(k['hfwd'] - k['hup'] * np.dot(k['hfwd'], k['hup']))
        k['head'] = k['neck'] + _unit(up * 0.45 + k['hup'] * 0.55) * NECK_HEAD
    return k


# The poses, in their own frame: the floor at y = 0, the head towards +x, the body's right towards -z or +z as
# each says. Each lists what it rests on (contact_faults checks them).
def face_down(sp):
    """Flat on their face: the cheek on the floor (head turned to one side), one arm flung past the head, the
    other by the hip, one knee drawn out, the tops of the feet on the floor and the soles up."""
    flip = 1
    X = (0, 0, -flip)                                    # the body's right side: front down means fwd = -y
    turn = (0, 0, -flip)                                 # face turned towards its right, left cheek down
    arms = {'R': ((1.02, 0.066, -flip * 0.34), (0.2, 1.0, -flip * 0.6)),
            'L': ((0.12, 0.066, flip * 0.34), (0.3, 1.0, flip * 0.8))}
    legs = {'R': ((-0.665, 0.042, -flip * 0.13), (0.0, 0.2, -flip * 1.0), (-1, -0.12, 0), (0, -1, 0)),
            'L': ((-0.48, 0.042, flip * 0.4), (0.15, 0.0, flip * 1.0), (-0.9, -0.12, flip * 0.3), (0, -1, 0))}
    return _head_down(_build((0, 0.105, 0), (0.22, 0.11, 0), (0.66, 0.12, 0), X, (1, 0, 0), turn, arms, legs, sp,
                             hips_off=(0, -0.028, 0)), sp)


def on_back(sp):
    """Flat on the back, looking up a little to one side: arms flung out bent at the elbow, one knee up with the
    foot flat, the other leg out straight on its heel, toes up."""
    flip = 1
    X = (0, 0, flip)
    arms = {'R': ((0.82, 0.066, flip * 0.56), (0.3, 1.0, flip * 0.2)),
            'L': ((0.22, 0.066, -flip * 0.52), (-0.2, 1.0, -flip * 0.3))}
    legs = {'R': ((-0.4, 0.06, flip * 0.16), (-0.3, 1.0, flip * 0.3), (-1, 0, 0.1), (0, 1, 0)),
            'L': ((-0.68, 0.07, -flip * 0.17), (0.0, 1.0, -flip * 0.1), (-0.25, 0.9, -flip * 0.35), (1, 0, 0))}
    return _head_down(_build((0, 0.105, 0), (0.22, 0.11, 0), (0.66, 0.12, 0), X, (1, 0, 0),
                             (0.1, 1, -flip * 0.35), arms, legs, sp, hips_off=(0, -0.028, 0)), sp)


def curled(sp):
    """On the side, curled up: knees drawn up towards the chest, the lower arm out under the head, the upper arm
    over the body with its hand on the floor in front, the head tucked down."""
    X = (0, -1, 0)                                       # the right side down: fwd = +z
    f = 1
    arms = {'R': ((0.86, 0.066, f * 0.3), (0.0, 0.2, f * 1.0)),
            'L': ((0.42, 0.066, f * 0.42), (0.2, 1.0, f * 0.3))}
    legs = {'R': ((-0.16, 0.055, f * 0.5), (0.3, 0.0, f * 1.0), (-0.9, 0, f * 0.3), (0, 0, -f)),
            'L': ((-0.02, 0.2, f * 0.5), (0.4, 0.4, f * 1.0), (-0.9, -0.2, f * 0.4), (0, 0.3, -f))}
    hc = 0.82 * sp.get('shoulders', 150) * M            # the chest's half width: what it lies on
    k = _build((0, hc * B.HEM, 0), (0.22, hc * 0.95, f * 0.05), (0.6, hc, f * 0.07), X, (1, -0.3, f * 0.35),
               (-0.25, -0.1, f * 1), arms, legs, sp, shrug={'R': (0.115, 0.07)})
    return _head_down(k, sp)


def slump(sp):
    """Collapsed sitting against a wall (the wall behind, at x = -0.17): the back on it, the head dropped forward
    and to one side, one knee up with its foot flat, the other leg out, the hands limp on the floor and lap."""
    flip = 1
    X = (0, 0, -flip)                                    # facing +x, away from the wall
    arms = {'R': ((0.14, 0.066, -flip * 0.34), (-0.4, 0.2, -flip * 1.0)),
            'L': ((0.3, 0.2, flip * 0.1), (-0.3, 0.3, flip * 1.0))}
    legs = {'R': ((0.5, 0.06, -flip * 0.16), (0.3, 1.0, -flip * 0.2), (1, 0, -flip * 0.1), (0, 1, 0)),
            'L': ((0.7, 0.052, flip * 0.2), (0.0, 1.0, flip * 0.1), (0.3, 0.9, flip * 0.35), (-1, 0, 0))}
    return _build((0.0, 0.105, 0), (-0.04, 0.3, -flip * 0.03), (-0.02, 0.66, -flip * 0.11), X,
                  (0.55, 0.75, -flip * 0.35),
                  (0.8, -0.55, -flip * 0.1), arms, legs, sp)


POSES = {'face_down': face_down, 'back': on_back, 'side': curled, 'slump': slump}
RESTS = {'face_down': ['chest', 'pelvis', 'head', 'thighL', 'thighR', 'handL', 'handR', 'shoeL', 'shoeR'],
         'back': ['chest', 'pelvis', 'head', 'handL', 'handR', 'shoeL', 'shoeR'],
         'side': ['chest', 'pelvis', 'head', 'thighR', 'handL', 'handR'],
         'slump': ['pelvis', 'handR', 'shoeL', 'shoeR']}
WALL_RESTS = {'slump': ['chest', 'hair']}             # any one of these (long hair between the back and the wall)
SLUMP_WALL = -0.17                                       # the wall behind a slumped body (its own frame)


def mirror(k):
    """The same pose the other way round (left and right swapped, z negated): lying on the other side."""
    out = Body()
    for n, v in k.items():
        w = np.array(v, float)
        w[2] = -w[2]
        out[n[:-1] + {'L': 'R', 'R': 'L'}[n[-1]] if n[-1] in 'LR' else n] = w
    return out


def place(k, x, z, yaw, ground=0.0):
    """A pose's frame put into the room: turned `yaw` degrees about the vertical (0: its head towards +x... as
    built; 90: towards -z), its origin at floor point (x, z), the floor `ground` high (a table top)."""
    a = math.radians(yaw)
    c, s = math.cos(a), math.sin(a)
    R = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    out = Body()
    for n, v in k.items():
        w = R @ np.asarray(v, float)
        out[n] = w + _v(x, ground, z) if n in POINTS else w
    return out


def blend(a, b, u):
    """In between two skeletons (u 0..1): points slide, directions turn; the elbows and knees are solved again, so
    bones keep their lengths."""
    out = Body()
    for n in a:
        if n in POINTS:
            out[n] = a[n] + (b[n] - a[n]) * u
        else:
            out[n] = _unit(a[n] + (b[n] - a[n]) * u + 1e-6)
    for side in 'LR':
        for root, mid, end, l1, l2 in (('sh', 'el', 'wr', UPPER, FORE), ('hip', 'kn', 'an', THIGH, SHIN)):
            pa = a[mid + side] - (a[root + side] + a[end + side]) / 2
            pb = b[mid + side] - (b[root + side] + b[end + side]) / 2
            out[mid + side], out[end + side] = limb(out[root + side], out[end + side], l1, l2, pa + (pb - pa) * u)
    return out


def from_views(j, sp, x, z, facing, ground=0.0, head_facing=None):
    """A views.py pose (person units, the torso frame, lean about the hips) as a 3D Body standing at floor point
    (x, z) facing (fx, fz): the same skeleton the flat drawing used, in metres."""
    fx, fz = _unit((facing[0], facing[1]))
    r = _v(-fz, 0, fx)                                   # views' +x: screen right when they face us (sets.Cam)
    f3 = _v(fx, 0, fz)
    lean, bob = j.get('lean', 0.0), j.get('bob', 0.0)

    def W(p, upper=False):
        if upper:
            p = V.leaned(tuple(p), lean)
        px, py, pz = p
        return _v(x, ground, z) + r * px * M + f3 * pz * M + _v(0, (928 - py - bob) * M, 0)
    hdy = sp.get('head_dy', 0) + j.get('head_dy', 0)
    k = Body(pelvis=(W(j['hipL']) + W(j['hipR'])) / 2, waist=W((0, 270, 0), True), neck=W((0, 0, 0), True))
    up = _unit(k['neck'] - k['pelvis'])
    k['fwd'] = _unit(W((0, 0, 100), True) - W((0, 0, 0), True))
    hc = W((sp.get('head_dx', 0.0), -150 + hdy, 0), True)
    k['head'] = hc
    k['hup'] = _unit(W((0, -250, 0), True) - W((0, -150, 0), True))
    hf = k['fwd']
    if head_facing is not None:
        hf = _unit(_v(head_facing[0], 0, head_facing[1]))
    k['hfwd'] = _unit(hf - k['hup'] * np.dot(hf, k['hup']))
    for side in 'LR':
        k['sh' + side], k['el' + side], k['wr' + side] = (W(j[n + side], True) for n in ('sh', 'el', 'wr'))
        k['hip' + side], k['an' + side] = W(j['hip' + side]), W(j['foot' + side])
        k['kn' + side] = W(V.knee_of(j, side))
        a = math.radians(j.get('toe' + side, 0.0))
        k['toe' + side] = _unit(f3 * math.cos(a) + _v(0, -math.sin(a), 0))
        k['sup' + side] = _unit(_v(0, 1, 0) - k['toe' + side] * k['toe' + side][1])
    _ = up
    return k


# ------------------------------------------------------------------------------------------------ the volumes
ROUND, ELL = 0, 1
NC = 24


class Part:
    def __init__(self, name, kind, a, b=None, ra=0.0, rb=0.0, axes=None, radii=None, mat='top', group=0):
        self.name, self.kind, self.mat, self.group = name, kind, mat, group
        self.a = np.asarray(a, float)
        self.b = np.asarray(b if b is not None else a, float)
        self.ra, self.rb = ra, rb
        self.axes = np.asarray(axes if axes is not None else np.eye(3), float)
        self.radii = np.asarray(radii if radii is not None else (ra, ra, ra), float)

    def row(self):
        r = np.zeros(NC)
        r[0], r[1] = self.kind, self.group
        r[2] = 0.05 if self.group == 1 else 0.025
        r[3:6], r[6:9], r[9], r[10] = self.a, self.b, self.ra, self.rb
        r[11:20] = self.axes.ravel()
        r[20:23] = self.radii
        return r

    def low(self, n, p0):
        """The part's nearest reach along -n from the plane through p0 (its gap to the surface; < 0: inside)."""
        if self.kind == ROUND:
            return min(np.dot(self.a - p0, n) - self.ra, np.dot(self.b - p0, n) - self.rb)
        return np.dot(self.a - p0, n) - math.sqrt(sum((r * np.dot(ax, n)) ** 2 for r, ax in zip(self.radii, self.axes)))


def _frame(X, up):
    X = _unit(X - up * np.dot(X, up))
    return np.array([X, up, np.cross(X, up)])


def parts(k, sp):
    """The body's volumes: [Part] (a 'group' melts its parts into one smooth shape: the torso)."""
    out = []
    sw = sp.get('shoulders', 150) * M
    dress = sp.get('outfit') == 'dress'
    up_p = _unit(k['waist'] - k['pelvis'])
    up_c = _unit(k['neck'] - k['waist'])
    X = _unit(k['shR'] - k['shL'])
    fc = _frame(X, up_c)
    fp = _frame(X, up_p)
    clen = np.linalg.norm(k['neck'] - k['waist'])
    out.append(Part('chest', ELL, k['waist'] + (k['neck'] - k['waist']) * 0.58, axes=fc,
                    radii=(sw * 0.8, clen * 0.52, 0.112), mat='top', group=1))
    out.append(Part('belly', ELL, k['waist'] + up_c * 0.01, axes=fc, radii=(sw * 0.68, 0.14, 0.1), mat='top',
                    group=1))                            # the waist: narrower than the chest and the hips
    for side in 'LR':
        out.append(Part('shoulder' + side, ELL, k['sh' + side] + up_c * 0.012 - fc[2] * 0.005, axes=fc,
                        radii=(0.07, 0.062, 0.066), mat='top', group=1))
    out.append(Part('pelvis', ELL, k['pelvis'] + up_p * 0.03, axes=fp,
                    radii=(sw * 0.82 * B.HEM, 0.14, 0.105), mat='hips', group=1))
    hb = k['head'] - k['hup'] * sp.get('hh', 90) * M * 0.62
    out.append(Part('neck', ROUND, k['neck'] - up_c * 0.03, hb, 0.05, 0.046, mat='neck', group=2))
    hx = _unit(np.cross(k['hup'], k['hfwd']))
    fh = np.array([hx, k['hup'], k['hfwd']])
    hw, hh = sp.get('hw', 72) * M, sp.get('hh', 90) * M
    out.append(Part('head', ELL, k['head'], axes=fh, radii=(hw, hh, hw * 1.08), mat='head', group=2))
    if V._hair(sp)[2] != 'long':
        for sg in (-1, 1):
            out.append(Part('ear', ELL, k['head'] + hx * sg * hw * 0.96 + k['hfwd'] * 0.0, axes=fh,
                            radii=(0.014, 0.033, 0.022), mat='skin', group=0))
    elif k['hfwd'][1] > 0.55:                            # long hair, face up: spread on the floor round the head
        ln = V._hair(sp)[3] * M
        a_, b_ = _unit(hx * _v(1, 0, 1)), _unit(k['hup'] * _v(1, 0, 1))
        floor = k['head'][1] - hw * 1.08 * k['hfwd'][1]
        c_ = _v(k['head'][0], floor + 0.022, k['head'][2]) + b_ * 0.03
        out.append(Part('hair', ELL, c_, axes=np.array([a_, _unit(np.cross(_v(0, 1, 0), a_)), _v(0, 1, 0)]),
                        radii=(hw * 1.45, hh * 1.05 + ln * 0.3, 0.022), mat='hair', group=0))
    else:                                                # long hair falls behind the head and down the back
        ln = V._hair(sp)[3] * M
        out.append(Part('hair', ELL, k['head'] - k['hfwd'] * hw * 0.35 - k['hup'] * ln * 0.35, axes=fh,
                        radii=(hw * 1.12, hh * 0.75 + ln * 0.45, hw * 0.72), mat='hair', group=0))
    for side in 'LR':
        out.append(Part('arm' + side, ROUND, k['sh' + side], k['el' + side], 0.056, 0.05, mat='sleeve'))
        out.append(Part('forearm' + side, ROUND, k['el' + side], k['wr' + side], 0.049, 0.041, mat='cuff'))
        d = _unit(k['wr' + side] - k['el' + side])
        out.append(Part('hand' + side, ELL, k['wr' + side] + d * 0.03, radii=(0.044, 0.044, 0.044), mat='skin'))
        tr = _thigh_r(sp)                                # a gown over the thigh: fuller, flaring to the knee
        out.append(Part('thigh' + side, ROUND, k['hip' + side], k['kn' + side], tr[0], tr[1],
                        mat='hips' if dress else 'legs'))
        out.append(Part('shin' + side, ROUND, k['kn' + side], k['an' + side], 0.06, 0.043, mat='legs'))
        t_, s_ = k['toe' + side], k['sup' + side]
        fs = np.array([_unit(np.cross(s_, t_)), s_, t_])
        out.append(Part('shoe' + side, ELL, k['an' + side] + t_ * 0.055 - s_ * 0.008, axes=fs,
                        radii=(0.047, 0.05, 0.125), mat='shoe'))
    return out


ADJ = {('belly', 'chest'), ('belly', 'pelvis'), ('belly', 'arm'), ('belly', 'shoulder'), ('chest', 'arm'), ('chest', 'neck'), ('shoulder', 'arm'), ('shoulder', 'chest'), ('chest', 'pelvis'),
       ('arm', 'forearm'), ('forearm', 'hand'), ('pelvis', 'thigh'), ('thigh', 'shin'), ('shin', 'shoe'),
       ('neck', 'head'), ('head', 'ear'), ('pelvis', 'skirt'), ('skirt', 'thigh'), ('chest', 'skirt'),
       ('shoulder', 'neck'), ('shoulder', 'shoulder'), ('head', 'hair'), ('neck', 'hair')}


def _adjacent(a, b):
    """Two parts joined on the body (no line where they meet): the same side's arm and forearm, etc."""
    if a.name == b.name:
        return True
    na, nb = a.name, b.name
    sa, sb = na[-1] if na[-1] in 'LR' else '', nb[-1] if nb[-1] in 'LR' else ''
    ba, bb = na.rstrip('LR') if sa else na, nb.rstrip('LR') if sb else nb
    if sa and sb and sa != sb:
        return ba == bb and ba in ('shoulder', 'skirt')
    return (ba, bb) in ADJ or (bb, ba) in ADJ


# ------------------------------------------------------------------------------------------------ tracing
@njit(cache=True, fastmath=True)
def _pd(P, i, x, y, z):
    if P[i, 0] == 0.0:                                   # a round cone (iq: sdRoundCone)
        ax, ay, az = P[i, 3], P[i, 4], P[i, 5]
        bax, bay, baz = P[i, 6] - ax, P[i, 7] - ay, P[i, 8] - az
        r1, r2 = P[i, 9], P[i, 10]
        l2 = bax * bax + bay * bay + baz * baz
        if l2 < 1e-10:
            dx, dy, dz = x - ax, y - ay, z - az
            return math.sqrt(dx * dx + dy * dy + dz * dz) - r1
        rr = r1 - r2
        a2 = l2 - rr * rr
        il2 = 1.0 / l2
        pax, pay, paz = x - ax, y - ay, z - az
        yy = pax * bax + pay * bay + paz * baz
        zz = yy - l2
        qx, qy, qz = pax * l2 - bax * yy, pay * l2 - bay * yy, paz * l2 - baz * yy
        x2 = qx * qx + qy * qy + qz * qz
        y2 = yy * yy * l2
        z2 = zz * zz * l2
        sr = 1.0 if rr > 0 else (-1.0 if rr < 0 else 0.0)
        k = sr * rr * rr * x2
        sz = 1.0 if zz > 0 else (-1.0 if zz < 0 else 0.0)
        sy = 1.0 if yy > 0 else (-1.0 if yy < 0 else 0.0)
        if sz * a2 * z2 > k:
            return math.sqrt(x2 + z2) * il2 - r2
        if sy * a2 * y2 < k:
            return math.sqrt(x2 + y2) * il2 - r1
        return (math.sqrt(x2 * a2 * il2) + yy * rr) * il2 - r1
    dx, dy, dz = x - P[i, 3], y - P[i, 4], z - P[i, 5]       # an ellipsoid (iq's bound)
    lx = (dx * P[i, 11] + dy * P[i, 12] + dz * P[i, 13]) / P[i, 20]
    ly = (dx * P[i, 14] + dy * P[i, 15] + dz * P[i, 16]) / P[i, 21]
    lz = (dx * P[i, 17] + dy * P[i, 18] + dz * P[i, 19]) / P[i, 22]
    k0 = math.sqrt(lx * lx + ly * ly + lz * lz)
    k1 = math.sqrt((lx / P[i, 20]) ** 2 + (ly / P[i, 21]) ** 2 + (lz / P[i, 22]) ** 2)
    if k1 < 1e-9:
        return -min(P[i, 20], min(P[i, 21], P[i, 22]))
    return k0 * (k0 - 1.0) / k1


@njit(cache=True, fastmath=True)
def _sd(P, x, y, z):
    best, bid, tot, acc, cg, ck = 1e9, -1, 1e9, 1e9, -1.0, 0.0
    for i in range(P.shape[0]):
        d = _pd(P, i, x, y, z)
        if d < best:
            best, bid = d, i
        g = P[i, 1]
        if g == 0.0:
            tot = min(tot, d)
        elif g != cg:
            tot = min(tot, acc)
            acc, cg, ck = d, g, P[i, 2]
        else:
            h = max(ck - abs(acc - d), 0.0) / ck
            acc = min(acc, d) - h * h * ck * 0.25
    return min(tot, acc), bid


@njit(parallel=True, cache=True, fastmath=True)
def _march(P, o, D, t0, t1, T, ID, N):
    for n in prange(D.shape[0]):
        T[n], ID[n] = -1.0, -1
        if t1[n] <= t0[n]:
            continue
        t = t0[n]
        for _ in range(160):
            x, y, z = o[0] + D[n, 0] * t, o[1] + D[n, 1] * t, o[2] + D[n, 2] * t
            d, i = _sd(P, x, y, z)
            if d < 0.0003 + 0.0004 * t:
                T[n], ID[n] = t, i
                e = 0.0015
                N[n, 0] = _sd(P, x + e, y, z)[0] - _sd(P, x - e, y, z)[0]
                N[n, 1] = _sd(P, x, y + e, z)[0] - _sd(P, x, y - e, z)[0]
                N[n, 2] = _sd(P, x, y, z + e)[0] - _sd(P, x, y, z - e)[0]
                break
            t += max(d * 0.9, 0.0004)
            if t > t1[n]:
                break


@njit(parallel=True, cache=True, fastmath=True)
def _under(P, Q, nrm, reach, OUT):
    """For points on a surface (floor, wall): 1 where the body is within `reach` metres over it along its normal."""
    for n in prange(Q.shape[0]):
        OUT[n] = 0
        for h in (0.008, 0.02, 0.04, 0.07, 0.1, 0.14, 0.18, 0.22):
            if h > reach:
                break
            d, _ = _sd(P, Q[n, 0] + nrm[0] * h, Q[n, 1] + nrm[1] * h, Q[n, 2] + nrm[2] * h)
            if d < 0.0:
                OUT[n] = 1
                break


# ------------------------------------------------------------------------------------------------ the face
class _TexCam:
    def __init__(self, ppu, s):
        self.ppu, self.s, self.c = ppu, s, 384

    def P(self, x, y):
        return self.c + x * self.ppu / B.SS, self.c + y * self.ppu / B.SS

    def S(self, v):
        return v * self.ppu / B.SS


TEX_PPU = 3.0                                            # texture pixels per person unit
_TEX = {}


def _head_tex(sp, t, view, s_screen):
    """The library's head drawing (front: burnham.head; back: views' back of the head) on a texture, line weights
    set for how big it will be on screen."""
    key = (sp.get('name'), view, sp.get('blink'), str(sp.get('mouth')), round(s_screen, 1), sp.get('look'),
           sp.get('brows'))
    if key in _TEX:
        return _TEX[key]
    img = Image.new('RGBA', (768, 768), (0, 0, 0, 0))
    # lines as thick as the flat drawing's at this size: Pen.w(lw) = lw*SS*0.75*s^0.6 on screen, here in texels
    s_eq = (s_screen ** 0.6 * TEX_PPU / (B.SS * s_screen)) ** (1 / 0.6)
    cam = _TexCam(TEX_PPU * B.SS, s_eq)
    L = B.Local(cam, 0, 0, 1.0)
    p = B.Pen(img, L)
    q = dict(sp, turn=0.0, head_dy=0)
    if view == 'front':
        B.head(img, p, q, t, 0.0, 0.0)
    else:
        V.head_view(img, p, q, t, 'back', 0.0, 0.0)
    a = np.asarray(img).astype(np.float32)
    _TEX[key] = a
    if len(_TEX) > 400:
        _TEX.pop(next(iter(_TEX)))
    return a


def _sample(tex, u, v):
    """Texture colours (RGBA float) at person-unit points (u across, v down) from the head's centre."""
    xi = np.clip((384 + u * TEX_PPU).astype(int), 0, 767)
    yi = np.clip((384 + v * TEX_PPU).astype(int), 0, 767)
    return tex[yi, xi]


# ------------------------------------------------------------------------------------------------ drawing
def _colours(sp):
    out = sp.get('outfit', 'suit')
    top = sp.get('dress', (190, 30, 44)) if out == 'dress' else sp.get('jacket', (40, 40, 46))
    return dict(skin=sp['skin'], top=top, sleeve=sp.get('sleeve', top), legs=sp.get('trousers', (40, 40, 46)),
                shirt=sp.get('shirt', (244, 244, 240)), shoe=sp.get('shoe', (22, 20, 22)),
                hair=sp.get('hair_c', (60, 44, 34)) if V._hair(sp)[2] != 'bald' else sp['skin'],
                tie=sp.get('tie'), bow=sp.get('bow'), belt=sp.get('belt', (52, 36, 28)))


def _ray_dirs(cam, xs, ys):
    X = xs / B.SS - 540 - cam.shake[0]
    Y = ys / B.SS - 960 - cam.shake[1]
    if cam.roll:
        c, s = math.cos(-cam.roll), math.sin(-cam.roll)
        X, Y = X * c - Y * s, X * s + Y * c
    f, r, u = (np.asarray(v, float) for v in (cam.f, cam.r, cam.u))
    D = f[None, :] + (X / cam.focal)[:, None] * r[None, :] - (Y / cam.focal)[:, None] * u[None, :]
    return D / np.linalg.norm(D, axis=1)[:, None]


def _bbox(cam, prts, img):
    pts = []
    for q in prts:
        r = max(q.ra, q.rb, *q.radii) + 0.03
        for c in (q.a, q.b):
            for d in ((r, 0, 0), (-r, 0, 0), (0, r, 0), (0, -r, 0), (0, 0, r), (0, 0, -r)):
                w = c + np.asarray(d)
                if cam.depth(w) > cam.NEAR:
                    pts.append(cam.project(w)[0])
    if not pts:
        return None
    a = np.array(pts) * B.SS
    W, H = img.size
    x0, y0 = max(0, int(a[:, 0].min()) - 8), max(0, int(a[:, 1].min()) - 8)
    x1, y1 = min(W, int(a[:, 0].max()) + 8), min(H, int(a[:, 1].max()) + 8)
    return (x0, y0, x1, y1) if x1 > x0 and y1 > y0 else None


def _lw(k_px):
    """The house line weight (Pen.w for lw 2.6) for a body this many frame pixels per metre."""
    s = k_px * M
    return max(2, int(round(2.6 * B.SS * 0.75 * max(0.25, s) ** 0.6)))


def shadow(img, cam, k, sp, surfaces, alpha=60):
    """The flat contact shadow on each surface [(point, normal, (lo, hi) bounds in x/z or None)] where the body
    rests on or over it (within 22 cm), before the body is drawn."""
    prts = parts(k, sp)
    P = np.array([q.row() for q in prts])
    box = _bbox(cam, prts, img)
    if box is None:
        return
    x0, y0, x1, y1 = box
    pad = (x1 - x0) // 6
    x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(img.size[0], x1 + pad), min(img.size[1], y1 + pad)
    xs, ys = np.meshgrid(np.arange(x0, x1, 2) + 1.0, np.arange(y0, y1, 2) + 1.0)
    D = _ray_dirs(cam, xs.ravel(), ys.ravel())
    o = np.asarray(cam.pos, float)
    lay = np.zeros((ys.shape[0], xs.shape[1]), bool)
    for p0, nrm in surfaces:
        p0, nrm = np.asarray(p0, float), _unit(nrm)
        den = D @ nrm
        tt = np.where(np.abs(den) > 1e-6, ((p0 - o) @ nrm) / np.where(np.abs(den) > 1e-6, den, 1), -1)
        Q = o[None, :] + D * tt[:, None]
        OUT = np.zeros(len(Q), np.int32)
        ok = tt > 0
        sub = np.zeros(int(ok.sum()), np.int32)
        _under(P, np.ascontiguousarray(Q[ok]), nrm, 0.22 if nrm[1] > 0.7 else 0.045, sub)   # a wall: the touch
        OUT[ok] = sub
        lay |= OUT.reshape(lay.shape).astype(bool)
    if not lay.any():
        return
    m = Image.fromarray((lay * alpha).astype(np.uint8)).resize((x1 - x0, y1 - y0), Image.BILINEAR)
    sh = Image.new('RGBA', (x1 - x0, y1 - y0), (0, 0, 0, 0))
    sh.putalpha(m)
    img.alpha_composite(sh, (x0, y0))


def draw(img, cam, k, sp, t=0.0, light=None, surfaces=None):
    """Draw the Body k through cam (sets.Cam) as one body: traced volumes, one outline, a flat shadow side, the
    person's own face and clothes. `surfaces`: [(point, normal)] it rests on, for the contact shadow (drawn
    first). Returns {joint: frame point} for props and checks, or None if off camera."""
    if surfaces:
        shadow(img, cam, k, sp, surfaces)
    prts = parts(k, sp)
    P = np.ascontiguousarray(np.array([q.row() for q in prts]))
    box = _bbox(cam, prts, img)
    if box is None:
        return None
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    xs, ys = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
    D = np.ascontiguousarray(_ray_dirs(cam, xs.ravel(), ys.ravel()))
    o = np.asarray(cam.pos, float)
    cen = np.mean([q.a for q in prts] + [q.b for q in prts], axis=0)
    R = max(np.linalg.norm(q.a - cen) + max(q.ra, *q.radii) for q in prts) + 0.05
    oc = o - cen
    bq = D @ oc
    disc = bq * bq - (oc @ oc - R * R)
    sq = np.sqrt(np.maximum(disc, 0))
    t0 = np.where(disc > 0, np.maximum(-bq - sq, cam.NEAR), 1.0)
    t1 = np.where(disc > 0, -bq + sq, 0.0)
    T = np.zeros(len(D))
    ID = np.zeros(len(D), np.int64)
    N = np.zeros((len(D), 3))
    _march(P, o, D, np.ascontiguousarray(t0), np.ascontiguousarray(t1), T, ID, N)
    hit = (T > 0).reshape(h, w)
    if not hit.any():
        return None
    idm = ID.reshape(h, w)
    N /= np.linalg.norm(N, axis=1)[:, None] + 1e-9
    Pw = o[None, :] + D * T[:, None]
    col = _paint(prts, idm.ravel(), Pw, sp, t, cam, hit.ravel())
    reg = col[:, 3].astype(np.int64).reshape(h, w)
    rgb = col[:, :3]
    # the light from high on the left, a little beyond the subject: the shadow side is the right and underneath
    L = _unit(light if light is not None else (_v(0, 1, 0) - np.asarray(cam.r) * 0.75 + np.asarray(cam.f) * 0.2))
    dark = (N @ L) < 0.0
    rgb = np.where(dark[:, None], rgb * SHADE, rgb)
    # the lines: the silhouette; parts that lie over others (not joined on the body); colours meeting; a body
    # part in front of another of the same part (depth jump)
    dep = T.reshape(h, w)
    edge = np.zeros((h, w), bool)
    adj = np.array([[_adjacent(a, b) for b in prts] for a in prts])
    for dy, dx in ((0, 1), (1, 0)):
        A = (slice(0, h - dy), slice(0, w - dx))
        Bs = (slice(dy, h), slice(dx, w))
        ha, hb = hit[A], hit[Bs]
        e = ha != hb
        both = ha & hb
        ia, ib = idm[A], idm[Bs]
        e |= both & ~adj[np.maximum(ia, 0), np.maximum(ib, 0)]
        e |= both & (reg[A] != reg[Bs])
        e |= both & (np.abs(dep[A] - dep[Bs]) > 0.035)
        edge[A] |= e
        edge[Bs] |= e
    kpx = cam.focal / max(cam.NEAR, cam.depth(cen))
    lw = _lw(kpx)
    ink = ndimage.binary_dilation(edge, structure=_disk(lw)) & (ndimage.binary_dilation(hit, iterations=lw // 2 + 1))
    out = np.zeros((h, w, 4), np.uint8)
    out[..., :3] = rgb.reshape(h, w, 3).clip(0, 255).astype(np.uint8)
    out[..., 3] = hit * 255
    out[ink, :3] = INK[:3]
    out[ink, 3] = 255
    img.alpha_composite(Image.fromarray(out, 'RGBA'), (x0, y0))
    return {n: cam.project(k[n])[0] for n in POINTS}


def _disk(lw):
    r = lw / 2.0
    n = int(math.ceil(r))
    yy, xx = np.mgrid[-n:n + 1, -n:n + 1]
    return (xx * xx + yy * yy) <= r * r + 0.25


def _paint(prts, ids, Pw, sp, t, cam, hit):
    """Each traced point's colour and colour region (r, g, b, region): the part's material, its clothes details,
    the face drawing on the head."""
    C = _colours(sp)
    out = np.zeros((len(ids), 4))
    pal = {}

    def code(c):
        return pal.setdefault(tuple(int(v) for v in c), len(pal) + 1)
    suit = sp.get('outfit', 'suit') in ('suit', 'blouse')
    dress = sp.get('outfit') == 'dress'
    jacketed = suit or sp.get('outfit') in ('coat',)
    for i, q in enumerate(prts):
        m = (ids == i) & hit
        if not m.any():
            continue
        X = Pw[m]
        base = {'top': C['top'], 'hips': C['top'], 'sleeve': C['sleeve'], 'cuff': C['sleeve'], 'legs': C['legs'],
                'skin': C['skin'], 'neck': C['skin'], 'hair': C['hair'], 'shoe': C['shoe'],
                'head': C['skin']}[q.mat]
        c = np.tile(np.array(base, float), (len(X), 1))
        ax = q.axes
        loc = (X - q.a) @ ax.T                           # the part's own frame (x across, y up it, z its front)
        if q.mat == 'top':                               # the chest: shirt and tie in the jacket's V; a dress neckline
            ry = q.radii[1]
            yt = loc[:, 1] / ry                          # -1 waist .. +1 neck
            front = loc[:, 2] > 0
            if q.name == 'chest' and suit:
                vw = 0.11 * np.clip((yt - 0.05) / 0.95, 0, 1)
                v = front & (np.abs(loc[:, 0]) < vw) & (yt > 0.05)
                c[v] = C['shirt']
                if C['tie'] is not None:
                    c[v & (np.abs(loc[:, 0]) < 0.019) & (yt < 0.93)] = C['tie']
                if C['bow'] is not None:
                    bw_ = 0.05 * (1 - np.abs(yt - 0.9) * 6)
                    c[front & (np.abs(loc[:, 0]) < bw_) & (yt > 0.76)] = C['bow']
            elif q.name == 'chest' and dress:
                c[front & (yt > 0.62) & (np.abs(loc[:, 0]) < 0.12 * (yt - 0.62) / 0.38 + 0.03)] = C['skin']
        elif q.mat == 'hips':
            if q.name == 'pelvis' and not dress:
                hem = -0.065 if jacketed else 0.075     # the jacket's hem below the hips; else the belt line
                c[loc[:, 1] < hem] = C['legs']
                if not jacketed:
                    c[(loc[:, 1] >= hem) & (loc[:, 1] < hem + 0.03)] = C['belt']
        elif q.mat == 'neck' and (suit or not dress):
            u = ((X - q.a) @ _unit(q.b - q.a)) / (np.linalg.norm(q.b - q.a) or 1)
            c[u < 0.42] = C['shirt'] if suit else C['top']   # the collar round the neck
        elif q.mat == 'cuff' and suit:
            u = ((X - q.a) @ _unit(q.b - q.a)) / (np.linalg.norm(q.b - q.a) or 1)
            c[u > 0.86] = C['shirt']
        elif q.mat == 'shoe':
            c[loc[:, 1] < -0.012] = SOLE_C if C['shoe'][0] < 90 else B.dk(C['shoe'], 0.6)
        elif q.mat == 'head':
            # the face drawing covers the front of the head (where it faces within 70 degrees of straight out), laid
            # on flat as the drawing is; the crown and sides round it take the hair (or skin) as the flat drawing has
            # it: short hair down to the ears, long hair to the jaw, bald skin; the back takes the back drawing
            u, v = loc[:, 0] / M, -loc[:, 1] / M         # person units, v down, from the head's centre
            nl = loc / q.radii[None, :]
            nz = nl[:, 2]
            s_scr = cam.focal / max(cam.NEAR, cam.depth(q.a)) * M
            res = np.zeros((len(X), 4), np.float32)
            face, back = nz >= 0.34, nz <= -0.34
            for view, sel, sgn in (('front', face, 1), ('back', back, -1)):
                if sel.any():
                    tex = _head_tex(sp, t, view, s_scr)
                    res[sel] = _sample(tex, sgn * u[sel] * 0.9, v[sel] * 0.9)
            a = res[:, 3:4] / 255.0
            kind = V._hair(sp)[2]
            low = {'bald': -9.0, 'long': 0.55}.get(kind, -0.05)   # how far down the sides the hair comes
            hairy = (-nl[:, 1] < -low) if kind != 'bald' else np.zeros(len(X), bool)
            if kind == 'bald' and V._hair(sp)[0] != sp['skin']:
                hairy = (-nl[:, 1] > -0.15) & (-nl[:, 1] < 0.35) & (nz < 0.2)   # a fringe round the back
            under = np.where(hairy[:, None], np.array(C['hair'], float), np.array(C['skin'], float))
            c = res[:, :3] * a + under * (1 - a)
        rg = np.zeros(len(X))
        if q.mat == 'head':                              # the drawing has its own lines: none added inside the head,
            rg[:] = code(C['skin'])                      # and none where it meets the neck (no jaw crease from behind)
        else:
            for cc in {tuple(x) for x in c.astype(int)}:
                rg[(c.astype(int) == cc).all(1)] = code(cc)
        out[m, :3], out[m, 3] = c, rg
    return out


# ------------------------------------------------------------------------------------------------ fitting and checks
def surfaces_of(pose, k=None, ground=0.0, yaw=0.0, x=0.0, z=0.0):
    """The surfaces a placed pose rests on: [(name, point, normal)] (the floor; the wall behind a slump)."""
    out = [('floor', _v(0, ground, 0), _v(0, 1, 0))]
    if pose == 'slump':
        a = math.radians(yaw)
        n = _v(math.cos(a), 0, -math.sin(a))             # the pose's +x turned, away from the wall
        out.append(('wall', _v(x, ground, z) + n * SLUMP_WALL, n))
    return out


def settle(k, sp, surf):
    """Rest the body on its surfaces: moved along each surface's normal (floor first) so its lowest part just
    touches it, never floating or sunk."""
    k = k.copy()
    for _, p0, n in surf:
        gap = min(q.low(n, p0) for q in parts(k, sp))
        for name in POINTS:
            k[name] = k[name] - n * gap
    return k


def _rests(pose, sp, flip=1):
    """What a pose rests on the floor with (left and right swapped when it lies the other way round)."""
    sw = {'L': 'R', 'R': 'L'}
    return [n[:-1] + sw[n[-1]] if flip < 0 and n[-1] in 'LR' else n for n in RESTS.get(pose, [])]


SOFT = {'ear'}                                           # squashed under the head when lying on it, never seen


ENDS = {'handL': ('shL', 'elL', 'wrL', UPPER, FORE, 0.05), 'handR': ('shR', 'elR', 'wrR', UPPER, FORE, 0.05),
        'shoeL': ('hipL', 'knL', 'anL', THIGH, SHIN, 0.064), 'shoeR': ('hipR', 'knR', 'anR', THIGH, SHIN, 0.064)}


def rest(k, sp, pose, surf, flip=1):
    """Rest a placed pose on its surfaces: the trunk (every resting part but the hands and feet) moved along the
    floor's normal until its lowest just touches; then each resting hand and foot lowered or raised onto it, the
    arm or leg solved again (bones keep their length; out of reach stays a fault); then the wall, if any."""
    k = k.copy()
    _, p0, n = surf[0]
    need = _rests(pose, sp, flip)
    core = [q for q in parts(k, sp) if q.name in need and q.name not in ENDS] or parts(k, sp)
    gap = min(q.low(n, p0) for q in core)
    for name in POINTS:
        k[name] = k[name] - n * gap
    for end in need:
        if end not in ENDS:
            continue
        root, mid, tip, l1, l2, rm = ENDS[end]
        for _ in range(14):
            g = [q for q in parts(k, sp) if q.name == end][0].low(n, p0)
            if abs(g) < 0.004:
                break
            pole = k[mid] - (k[root] + k[tip]) / 2
            k[mid], k[tip] = _limb_clear(k[root], k[tip] - n * g, l1, l2, pole, rm, p0[1])
    for name, q0, nn in surf[1:]:
        want = WALL_RESTS.get(pose, [])
        gap = min((q.low(nn, q0) for q in parts(k, sp) if q.name in want), default=0.0)
        gap = min(gap, min(q.low(nn, q0) for q in parts(k, sp)))
        for nm in POINTS:
            k[nm] = k[nm] - nn * gap
    return k


def lie(sp, pose, x, z, yaw, ground=0.0, flip=1):
    """A lying pose ready to draw: built, placed at floor point (x, z) turned `yaw`, settled onto the floor (and a
    slump's wall). Returns (Body, surfaces)."""
    k = POSES[pose](sp)
    k = place(k if flip > 0 else mirror(k), x, z, yaw, ground)
    surf = surfaces_of(pose, k, ground, yaw, x, z)
    return rest(k, sp, pose, surf, flip), surf


def contact_faults(k, sp, pose, surf, who='someone', flip=1):
    """What rests where it should (within 1.5 cm) and nothing through a surface (more than 0.5 cm), in words."""
    out = []
    prts = parts(k, sp)
    for name, p0, n in surf:
        for q in prts:
            g = q.low(n, p0)
            if g < -0.005 and q.name not in SOFT:
                out.append(f"{who} ({pose}): the {q.name} passes {-g * 100:.1f} cm into the {name}")
        if name == 'floor':
            for want in _rests(pose, sp, flip):
                g = min((q.low(n, p0) for q in prts if q.name == want), default=None)
                if g is not None and g > 0.015:
                    out.append(f"{who} ({pose}): the {want} floats {g * 100:.1f} cm off the {name}")
        else:
            want = WALL_RESTS.get(pose, [])
            g = min((q.low(n, p0) for q in prts if q.name in want), default=None)
            if g is not None and g > 0.015:
                out.append(f"{who} ({pose}): the {' or '.join(want)} floats {g * 100:.1f} cm off the {name}")
    return out


def solids(name, k, sp):
    """The body for the collision audit (clipcheck capsules; the torso as 'body', so audit's position tracks it)."""
    out = []
    for q in parts(k, sp):
        part = 'body' if q.name in ('chest', 'pelvis') else q.name
        if q.kind == ROUND:
            out.append(CC.capsule(name, part, q.a, q.b, (q.ra + q.rb) / 2))
        else:
            o = np.argsort(q.radii)
            long_ax = q.axes[o[2]]
            half = max(0.0, q.radii[o[2]] - q.radii[o[1]])
            out.append(CC.capsule(name, part, q.a - long_ax * half, q.a + long_ax * half, q.radii[o[1]]))
    return out


# ------------------------------------------------------------------------------------------------ moving into it
def fall(sp, t, t0, x, z, facing, ground=0.0, pose='back', flip=1):
    """Falling backwards, in stages: moves.fall's knees buckling and drop onto the hips (the flat drawing, best
    side-on), then from the moment the hips land (t0 + 0.5) the 3D body takes over from that exact skeleton and
    settles back onto the shoulders into the lying pose over 0.45 s (eased: no pop). Returns ('views', j) or
    ('3d', Body, surfaces)."""
    if t < t0 + 0.5:
        return ('views', moves.fall(sp, t, t0)[0])
    j_sit = moves.fall(sp, t0 + 0.5, t0)[0]
    k0 = from_views(j_sit, sp, x, z, facing, ground)
    fx, fz = _unit(facing)
    yaw = math.degrees(math.atan2(fz, -fx))              # head towards the back of where they faced
    px, pz = k0['pelvis'][0], k0['pelvis'][2]
    k1, surf = lie(sp, pose, px, pz, yaw, ground, flip)
    return ('3d', blend(k0, k1, ease((t - t0 - 0.5) / 0.45)), surf)


def stand(img, cam, sp, x, z, facing, j, t, ground=0.0, head_facing=None, shadow_alpha=55):
    """Someone standing (or sitting: any views pose) at floor point (x, z), seen through a 3D camera at its real
    tilt. Up to views.HIGH degrees down: the flat drawing with the real tilt and a floor shadow; steeper: the 3D
    body of the same pose. Returns ('2d', views j2) or ('3d', joints on screen)."""
    mid = _v(x, ground + 0.9, z)
    d = mid - np.asarray(cam.pos, float)
    tilt = math.degrees(math.atan2(-d[1], math.hypot(d[0], d[2])))
    if tilt >= V.HIGH:
        k = from_views(j, sp, x, z, facing, ground, head_facing)
        return ('3d', draw(img, cam, k, sp, t, surfaces=[(_v(0, ground, 0), _v(0, 1, 0))]))
    ring = [(x + 0.3 * math.cos(u), ground + 0.004, z + 0.22 * math.sin(u)) for u in np.linspace(0, 2 * math.pi, 18)]
    if all(cam.depth(q) > 0.2 for q in ring):
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        B.Pen(lay, S.FLAT).poly([cam.project(q)[0] for q in ring], (0, 0, 0, shadow_alpha), None)
        img.alpha_composite(lay)
    (Xf, Yf), kf = cam.project((x, ground, z))
    (_, Yn), _ = cam.project((x, ground + 928 * M, z))
    (_, _), km = cam.project(tuple(mid))
    s = km * M
    c = max(0.15, min(1.0, (Yf - Yn) / (928 * s)))
    tc = _unit(_v(cam.pos[0] - x, 0, cam.pos[2] - z))   # how much lower a point 0.42 m nearer us sits (Prepper)
    (_, Yq), _ = cam.project(tuple(_v(x, ground, z) + tc * 0.42))
    e = max(V.ELEV, (Yq - Yf) / s / (0.42 / M))
    yaw = cam.yaw_of((x, 0, z), facing)
    hy = cam.yaw_of((x, 0, z), head_facing) if head_facing is not None else None
    return ('2d', V.person(img, S.FLAT, Xf, Yf - 928 * s, s, sp, t, yaw, j, hy, tilt=(e, c)))


# ------------------------------------------------------------------------------------------------ the sheet
ROWS = [('eye level (1.6 m up)', None, 6.2), ('30 degrees down', 30, 4.6), ('60 degrees down', 60, 4.3),
        ('straight down', 89.6, 4.3)]
COLS = [('face down', 'face_down'), ('on the back', 'back'), ('on the side, curled', 'side'),
        ('slumped against a wall', 'slump'), ('standing (any views pose)', 'stand')]
CAST = ('P1', 'LADY', 'MAGNATE')
SPOTS = [(-1.2, 0.12, -100.0), (0.0, -0.05, 75.0), (1.2, 0.1, -60.0)]   # x, z, yaw (heads every way)
SLUMP_SPOTS = [(-1.0, -0.55, -90.0), (0.0, -0.55, -90.0), (1.0, -0.55, -90.0)]
STAND_SPOTS = [(-0.75, 0.0, (0.35, 1.0)), (0.0, -0.1, (0.0, 1.0)), (0.75, 0.0, (-0.4, 1.0))]


def _cam_for(angle, dist, look):
    look = np.asarray(look, float)
    if angle is None:
        pos = look + _v(0.0, 0.0, dist)
        pos[1] = 1.6
        return S.Cam(tuple(pos), tuple(look), focal=1000 * dist / 3.9)
    a = math.radians(angle)
    pos = look + _v(0.0, math.sin(a) * dist, math.cos(a) * dist)
    return S.Cam(tuple(pos), tuple(look), focal=1000 * dist / 3.7)


def _fit(cam, pts, fill=0.84):
    """The camera slid (never turned) and zoomed so the points fill the middle square of the frame."""
    pts = [np.asarray(p, float) for p in pts]
    for _ in range(4):
        a = np.array([cam.project(tuple(p))[0] for p in pts])
        lo, hi = a.min(0), a.max(0)
        c = (lo + hi) / 2
        k = cam.focal / max(cam.NEAR, cam.depth(tuple(np.mean(pts, 0))))
        sh = (np.asarray(cam.r) * (c[0] - 540) - np.asarray(cam.u) * (c[1] - 960)) / k
        z = fill * 1080 / max(hi[0] - lo[0], hi[1] - lo[1], 1.0)
        cam = S.Cam(tuple(np.asarray(cam.pos) + sh), tuple(np.asarray(cam.at) + sh), focal=cam.focal * min(z, 3.0))
    return cam


def _room(img, cam, wall=None):
    p = B.Pen(img, S.FLAT)
    floor, board = (196, 160, 118), (176, 140, 100)
    cam.poly(p, [(-6, 0, -6), (6, 0, -6), (6, 0, 6), (-6, 0, 6)], floor, None)
    for zz in np.arange(-6, 6.01, 0.22):
        cam.line(p, [(-6, 0.0005, zz), (6, 0.0005, zz)], board, 1.6)
    if wall is not None:
        wz = wall
        cam.poly(p, [(-6, 0, wz), (6, 0, wz), (6, 2.4, wz), (-6, 2.4, wz)], (214, 206, 188), INK, 2.0)
        cam.poly(p, [(-6, 0, wz + 0.001), (6, 0, wz + 0.001), (6, 0.12, wz + 0.02), (-6, 0.12, wz + 0.02)],
                 (240, 236, 226), INK, 1.8)             # a skirting board


def _cast():
    import poker_mon_cast as PC                          # the test people (Poker Mon's: a finished film's cast)
    out = []
    for n in CAST:
        sp = dict(PC.PEOPLE[n])
        out.append(sp)
    return out


def panel(col, row, cast):
    """One test picture: the three people in one pose, from one camera height (1080 x 1080 crop of the frame)."""
    name, angle, dist = ROWS[row]
    pose = COLS[col][1]
    img = B.canvas((214, 206, 188))
    if pose == 'stand':
        look = (0.0, 0.85, 0.0)
    elif pose == 'slump':
        look = (0.0, 0.3, -0.25)
    else:
        look = (0.0, 0.1, 0.0)
    pts = []
    for i, sp in enumerate(cast):
        if pose == 'stand':
            x, z, f = STAND_SPOTS[i]
            kk = from_views(V.standing(sp), sp, x, z, f)
            pts += [kk[n] for n in POINTS] + [kk['head'] + _v(0, 0.14, 0), _v(x, 0, z)]
        else:
            x, z, yaw = (SLUMP_SPOTS if pose == 'slump' else SPOTS)[i]
            kk = lie(sp, pose, x, z, yaw, flip=1 if i != 1 else -1)[0]
            pts += [kk[n] for n in POINTS]
    cam = _fit(_cam_for(angle, dist, look), pts)
    wall = None
    if pose == 'slump':
        wall = SLUMP_SPOTS[0][1] + SLUMP_WALL
    _room(img, cam, wall)
    faults = []
    order = []
    for i, sp in enumerate(cast):
        if pose == 'stand':
            x, z, f = STAND_SPOTS[i]
            order.append((cam.depth((x, 0.9, z)), i, None))
        else:
            x, z, yaw = (SLUMP_SPOTS if pose == 'slump' else SPOTS)[i]
            fl = 1 if i != 1 else -1
            k, surf = lie(sp, pose, x, z, yaw, flip=fl)
            faults += contact_faults(k, sp, pose, surf, sp['name'], fl)
            order.append((cam.depth(tuple(k['pelvis'])), i, (k, surf)))
    for _, i, ks in sorted(order, key=lambda v: -v[0]):
        sp = dict(cast[i])
        if pose == 'stand':
            x, z, f = STAND_SPOTS[i]
            stand(img, cam, sp, x, z, f, V.standing(sp), 0.0)
        else:
            k, surf = ks
            if pose != 'back':
                sp['blink'] = True                       # out cold; on the back, dazed with the eyes open
            draw(img, cam, k, sp, 0.0, surfaces=[(p0, n) for _, p0, n in surf])
    im = img.convert('RGB').resize((1080, 1920), Image.LANCZOS)
    return im.crop((0, 420, 1080, 1500)), faults


def old_frame():
    """Poker Mon's finished film at 20.0 s: the two players face down on the table (note 89's version, the one
    Sam's note 80 still applies to)."""
    import subprocess
    import tempfile
    src = os.path.join(HERE, '..', 'animations', 'poker-mon-vertical.mp4')
    out = os.path.join(tempfile.mkdtemp(), 'pm.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '20.0', '-i', src, '-frames:v', '1', out], check=True)
    im = Image.open(out).convert('RGB')
    return im.crop((120, 860, 1000, 1500))


def sheet(out_path, cell=430):
    from PIL import ImageFont
    cast = _cast()
    font = ImageFont.truetype(B.SANS, 26) if os.path.exists(str(B.SANS)) else ImageFont.load_default()
    small = ImageFont.truetype(B.SANS, 21) if os.path.exists(str(B.SANS)) else ImageFont.load_default()
    left = 250
    oldw = cell + 40
    W = left + cell * len(COLS) + oldw
    H = 70 + cell * len(ROWS) + 60
    sh = Image.new('RGB', (W, H), (246, 244, 238))
    d = ImageDraw.Draw(sh)
    d.text((16, 16), 'Build item 12: people lying down and seen from a high camera (3D body, one outline, '
                     'a flat shadow side). Test people: P1, LADY, MAGNATE (Poker Mon cast).', fill=(20, 20, 20),
           font=font)
    faults = []
    for c, (title, _) in enumerate(COLS):
        d.text((left + c * cell + 10, 46), title, fill=(20, 20, 20), font=small)
    for r, (title, _, _) in enumerate(ROWS):
        y = 70 + r * cell
        d.text((14, y + cell // 2 - 12), title, fill=(20, 20, 20), font=small)
        for c in range(len(COLS)):
            im, f = panel(c, r, cast)
            faults += f
            sh.paste(im.resize((cell - 8, cell - 8), Image.LANCZOS), (left + c * cell + 4, y + 4))
            print(f'  panel {title} / {COLS[c][0]}', flush=True)
    ox = left + cell * len(COLS) + 20
    d.text((ox, 46), 'Before: Poker Mon at 20 s', fill=(150, 20, 20), font=small)
    try:
        om = old_frame()
        om = om.resize((oldw - 30, int(om.height * (oldw - 30) / om.width)), Image.LANCZOS)
        sh.paste(om, (ox, 74))
        d.text((ox, 80 + om.height), '(tubes outlined one by one,\nflat fills, no clothes)', fill=(150, 20, 20),
               font=small)
    except Exception as e:                               # noqa: BLE001
        d.text((ox, 80), f'(old frame unavailable: {e})', fill=(150, 20, 20), font=small)
    note = ('Contact check: ' + ('every pose rests on the floor, nothing through it' if not faults else
                                 f'{len(faults)} faults (see the console)'))
    d.text((16, H - 44), note, fill=(20, 90, 30) if not faults else (170, 20, 20), font=small)
    sh.save(out_path, quality=90)
    for f in faults:
        print('FAULT:', f)
    return faults


def check():
    """Every pose for every test person: contacts; and the fall's hand-over: the body's centre and every joint
    move smoothly across the switch from the flat drawing to the 3D body (the pop-in audit's jump test)."""
    cast = _cast()
    faults = []
    for sp in cast:
        for pose in POSES:
            for yaw, fl in ((0.0, 1), (90.0, -1), (215.0, 1), (300.0, -1)):
                k, surf = lie(sp, pose, 0.3, -0.2, yaw, flip=fl)
                faults += contact_faults(k, sp, pose, surf, sp['name'], fl)
    import audit
    sp = cast[0]
    t0, fps = 1.0, 24
    prev = None
    worst = 0.0
    for n in range(int(2.0 * fps)):
        t = t0 - 0.2 + n / fps
        r = fall(sp, t, t0, 0.0, 0.0, (0.0, 1.0))
        if r[0] == 'views':
            sol = audit.placed(sp['name'], r[1], 0.0, 0.0, (0.0, 1.0), sp=sp)
        else:
            sol = solids(sp['name'], r[1], sp)
        thing = audit.Thing(sp['name'], sol, 'full')
        if prev is not None:
            step = float(np.linalg.norm(thing.pos - prev))
            worst = max(worst, step)
            if step > audit.JUMP:
                faults.append(f'fall: the body jumps {step:.2f} m at {t:.2f} s')
        prev = thing.pos
    print(f'fall hand-over: largest step of the body in one frame {worst * 100:.1f} cm (audit flags {audit.JUMP} m)')
    for f in faults:
        print('FAULT:', f)
    print('lying check:', 'OK' if not faults else f'{len(faults)} faults')
    return faults


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        sheet(a[1] if len(a) > 1 else 'lying-sheet.jpg')
    elif a and a[0] == 'check':
        sys.exit(1 if check() else 0)
    else:
        print(__doc__)
