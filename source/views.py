#!/usr/bin/env python3
"""views: anyone from any angle, posed on a hidden 3D skeleton (the satire package's people; see
guides/movement-system-plan.md and guides/reference-pack.md).

- Five real drawings per person, facing right: 'front', 'three' (three-quarter), 'side' (profile), 'three_back',
  'back'; facing left is the same drawing mirrored. A turn swaps drawings (the standard is a straight 180 pop).
  The side and back views are worked out from the front design: hair by kind (short, long, bald), beard by kind,
  clothes by outfit, all in the person's own colours (Sam: logical from what we see from the front).
- Arms and legs come from a skeleton in 3D (x across the body, y down, z forward): say where a hand or foot goes and
  the elbow or knee is solved (two bones, the rig's lengths). The camera sits a little above, so nearer points sit a
  little lower (ELEV): perspective inside the figure as well as on the floor (stage.py).
- `lean` tips the upper body forward (+) or back (-) about the hips: runs, rising from a chair, punches, falls.
- Limbs on the far side are drawn behind the body; `behind` puts an arm behind it on purpose (hands behind the back).

The joints dict ("a pose"): hipL/R, footL/R, shL/R, elL/R, wrL/R (3D), plus bob (the whole body lower, +), lean
(degrees), head_dy, hand {'L': shape, 'R': shape} ('fist', 'palm', 'gun', 'none' for a hidden hand), behind (set),
props (list of draw(p, j2d) callables), seated (bool: the chair is drawn).
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import figure as F           # noqa: E402
from ed import INK, curve, oval, soft   # noqa: E402

VIEWS = {0: 'front', 45: 'three', 90: 'side', 135: 'three_back', 180: 'back'}
THIGH, SHIN, ANKLE_Y = 228, 218, 890          # person units: hips at 450, soles at 928 (knees just soft standing)
M_PER_UNIT = 0.00152                          # metres per person unit (series.py: neck to soles 1.41 m)
ELEV = 0.14                                   # the camera a little above: nearer points sit lower
HIP_Y = 450.0
JACKET = 505.0                                # jacket hem just below the hips: more leg shows (Sam, 14 Oct)
SEAT_DROP = 222.0                             # seated: the body lower by this (knee-height chair, thighs level)
LONG_HAIR = {'long': 150, 'bob': 110, 'blonde': 260, 'wavy': 230}
BALD = {'bald', 'wisps'}


def blend(a, b, k):
    return tuple(int(round(x + (y - x) * k)) for x, y in zip(a, b))


def snap(yaw):
    """Nearest drawn view (degrees 0-180) for an angle (0 = facing us, 90 = facing right, -90 = left, 180 = away),
    and whether it is mirrored (facing left)."""
    y = ((yaw + 180) % 360) - 180
    m = min(VIEWS, key=lambda v: abs(abs(y) - v))
    return m, y < 0


def project(p3, yaw):
    """A body point seen from the camera, the body facing `yaw` degrees: (screen x, y) and depth (+ = nearer)."""
    a = math.radians(yaw)
    x, y, z = p3
    depth = -x * math.sin(a) + z * math.cos(a)
    return (x * math.cos(a) + z * math.sin(a), y + ELEV * depth), depth


def leaned(p3, lean):
    """An upper-body point tipped forward by `lean` degrees about the hips (head goes forward and down)."""
    if not lean:
        return p3
    L = math.radians(lean)
    x, y, z = p3
    dy = y - HIP_Y
    return x, HIP_Y + dy * math.cos(L) + z * math.sin(L), z * math.cos(L) - dy * math.sin(L)


# ------------------------------------------------------------------------------------------------ the skeleton
def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def _mul(a, k):
    return tuple(x * k for x in a)


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _unit(a):
    n = math.sqrt(_dot(a, a)) or 1.0
    return _mul(a, 1 / n)


def ik3(root, target, l1, l2, pole):
    """Two bones from `root` towards `target` (lengths l1, l2): the middle joint bends towards `pole` (a direction).
    The end stops at full reach if the target is too far. Returns (middle, end)."""
    d = _sub(target, root)
    dist = math.sqrt(_dot(d, d)) or 1e-6
    dist = min(max(dist, abs(l1 - l2) + 1e-3), l1 + l2 - 1e-3)
    n = _unit(d)
    along = (l1 * l1 - l2 * l2 + dist * dist) / (2 * dist)
    h = math.sqrt(max(0.0, l1 * l1 - along * along))
    pv = _sub(pole, _mul(n, _dot(pole, n)))
    pv = _unit(pv) if _dot(pv, pv) > 1e-9 else _unit((n[1], -n[0], 0.0))
    mid = _add(_add(root, _mul(n, along)), _mul(pv, h))
    return mid, _add(root, _mul(n, dist))


POLES = {'out': (1.0, 0.4, -0.35), 'down': (0.35, 1.0, -0.25), 'back': (0.25, 0.3, -1.0), 'front': (0.2, 0.2, 1.0),
         'up': (0.5, -1.0, 0.0), 'in': (-0.6, 0.6, 0.4)}


def reach_ok(j, side, target, shape='fist'):
    """Can the hand reach `target` without stretching? (for the checks)"""
    d = _sub(target, j['sh' + side])
    return math.sqrt(_dot(d, d)) <= (F.UPPER + F.FORE) * 0.98 + F.HAND.get(shape, 14) + 1


def arm_to(j, side, target, pole='down', shape='fist'):
    """Put a hand's contact point (fist, palm, point...: figure.HAND) on `target` (torso frame, before any lean).
    `pole`: which way the elbow points ('out', 'down', 'back', 'front', 'up', 'in'), mirrored for the left arm."""
    sg = -1 if side == 'L' else 1
    px, py, pz = POLES[pole] if isinstance(pole, str) else pole
    up, fore = F.UPPER * 0.98, F.FORE * 0.98
    off = F.HAND.get(shape, 14)
    el, end = ik3(j['sh' + side], target, up, fore + off, (sg * px, py, pz))
    wr = _add(el, _mul(_unit(_sub(end, el)), fore))
    j['el' + side], j['wr' + side] = el, wr
    j.setdefault('hand', {})[side] = shape
    return j


def standing(sp):
    """Standing relaxed: feet a little apart, arms hanging just in front of the body, hands loose fists."""
    sw = sp.get('shoulders', 150)
    j = {'bob': 0.0, 'lean': 0.0, 'hand': {}, 'behind': set(), 'props': []}
    for side, sg in (('L', -1), ('R', 1)):
        j['hip' + side] = (sg * 55, HIP_Y, 0.0)
        j['foot' + side] = (sg * 60, ANKLE_Y, 6.0)
        j['sh' + side] = (sg * (sw - 14), 60.0, 0.0)
        arm_to(j, side, (sg * (sw + 24), 466.0, 44.0), 'back')     # hands clear of the jacket, not tucked in (Sam)
    return j


def set_arm(j, side, swing, bend, out=0.12):
    """Arm joints from angles (both bones keep the rig's lengths): swing brings the upper arm forward (+) or back."""
    sg = -1 if side == 'L' else 1
    sx, sy, sz = j['sh' + side]
    u = (sg * math.sin(out), math.cos(swing) * math.cos(out), math.sin(swing) * math.cos(out))
    el = (sx + u[0] * F.UPPER * 0.98, sy + u[1] * F.UPPER * 0.98, sz + u[2] * F.UPPER * 0.98)
    a = swing + bend
    v = (sg * math.sin(out) * 0.5, math.cos(a), math.sin(a))
    n = math.sqrt(sum(c * c for c in v))
    wr = tuple(e + c / n * F.FORE * 0.98 for e, c in zip(el, v))
    j['el' + side], j['wr' + side] = el, wr


# ------------------------------------------------------------------------------------------------ the limbs
def tube(p, pts, widths, col):
    """One smooth limb through the points (rounded at each joint), tapering through `widths`."""
    P = np.asarray(pts, float)
    dense, wd = [], []
    for i in range(len(P) - 1):
        for u in np.linspace(0, 1, 12, endpoint=False):
            dense.append(P[i] + (P[i + 1] - P[i]) * u)
            wd.append(widths[i] + (widths[i + 1] - widths[i]) * u)
    dense.append(P[-1])
    wd.append(widths[-1])
    D = np.asarray(dense)
    T = np.gradient(D, axis=0)
    N = np.stack([-T[:, 1], T[:, 0]], 1) / (np.hypot(*T.T)[:, None] + 1e-9)
    left = D + N * np.asarray(wd)[:, None]
    right = D - N * np.asarray(wd)[:, None]
    p.poly(curve([tuple(v) for v in np.vstack([left, right[::-1]])], 2), col, INK, 2.6)


def _hull(pts):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], q) <= 0:
            hi.pop()
        hi.append(q)
    return lo[:-1] + hi[:-1]


def knee_of(j, side):
    hip, foot = j['hip' + side], j['foot' + side]
    sg = -1 if side == 'L' else 1
    knee, _ = ik3(hip, foot, THIGH, SHIN, j.get('knee_pole' + side, (0.12 * sg, 0.0, 1.0)))
    return knee


def leg(p, j, side, yaw, sp):
    hip3, foot3 = j['hip' + side], j['foot' + side]
    knee3 = knee_of(j, side)
    pts = [project(q, yaw)[0] for q in (hip3, knee3, foot3)]
    tube(p, pts, [48, 38, 27], sp.get('trousers', (40, 40, 46)))
    fx, fy, fz = foot3
    a = math.radians(j.get('toe' + side, 0.0))                       # heel lifted (toe-off, a kick), degrees

    def foot_pt(dx, dy, dz):
        return (fx + dx, fy + dy - dz * math.sin(a), fz + dz * math.cos(a))
    box = [foot_pt(sx, sy, sz) for sx in (-28, 28) for sy in (0, 36) for sz in (-28, 92)]   # the shoe starts at the ankle
    hull = _hull([project(q, yaw)[0] for q in box])
    p.poly(curve(hull, 3), sp.get('shoe', (22, 20, 22)), INK, 2.4)


def check_arm3(j, side, where='an arm'):
    """The arm checker for skeleton arms, in 3D (on screen an arm pointing at the camera is rightly short): both bones
    at the rig's lengths, and the elbow never folded tighter than 25 degrees."""
    sh, el, wr = j['sh' + side], j['el' + side], j['wr' + side]
    u, f = _sub(el, sh), _sub(wr, el)
    lu, lf = math.sqrt(_dot(u, u)), math.sqrt(_dot(f, f))
    if lu > F.UPPER * 1.06 or lf > F.FORE * 1.06:
        F.fail(f'{where}: a bone is longer than the rig')
    cosang = _dot(_mul(u, -1), f) / ((lu * lf) or 1)
    if math.degrees(math.acos(max(-1.0, min(1.0, cosang)))) < 25:
        F.fail(f'{where}: elbow folded tighter than 25 degrees')


def arm(p, j2, side, sp, shape=None):
    sh, el, wr = j2['sh' + side], j2['el' + side], j2['wr' + side]
    with F.allow('a skeleton arm, checked in 3D (check_arm3); on screen it may be foreshortened'):
        B.arm(p, sh, el, wr, sp.get('sleeve', sp.get('jacket', (40, 40, 46))))
    shape = shape or j2.get('hand', {}).get(side, 'fist')
    if shape != 'none':
        B.gesture_hand(p, el, wr, shape, sp['skin'])


# ------------------------------------------------------------------------------------------------ the chair
def chair(p, view, j2, sp, under=True):
    """A plain office chair at knee height for anyone seated: `under` = the parts behind and below the person (drawn
    first), else the seat's front edge (drawn over the thighs' tops in a front view)."""
    c, cd = sp.get('chair_c', (60, 62, 70)), sp.get('chair_d', (40, 42, 48))
    hipy = (j2['hipL'][1] + j2['hipR'][1]) / 2
    if view in ('front', 'back'):
        if under:
            p.poly([(-120, hipy - 330), (120, hipy - 330), (110, hipy - 60), (-110, hipy - 60)], c, INK, 2.6)
            p.line([(0, hipy + 40), (0, hipy + 250)], cd, 9)
            for dx in (-110, 110):
                p.line([(0, hipy + 250), (dx, hipy + 290)], cd, 7)
            p.poly([(-130, hipy + 4), (130, hipy + 4), (122, hipy + 40), (-122, hipy + 40)], c, INK, 2.6)
    elif under:
        p.poly([(-120, hipy - 320), (-90, hipy - 320), (-80, hipy - 20), (-112, hipy - 20)], c, INK, 2.6)
        p.line([(10, hipy + 30), (10, hipy + 250)], cd, 9)
        for dx in (-100, 120):
            p.line([(10, hipy + 250), (dx, hipy + 290)], cd, 7)
        p.poly([(-110, hipy - 6), (150, hipy - 6), (146, hipy + 30), (-106, hipy + 30)], c, INK, 2.6)


# ------------------------------------------------------------------------------------------------ torso views
class Lean:
    """The drawing frame of the upper body, tipped by the pose's lean: a side view rotates about the hips; a front
    view foreshortens (the chest comes towards us and down)."""
    def __init__(self, L, lean, yaw):
        self.L, self.cam, self.s = L, L.cam, L.s
        a = math.radians(lean)
        cy = abs(math.cos(math.radians(yaw)))
        self.k = (math.cos(a) - ELEV * math.sin(a)) * cy + (1 - cy)
        self.r = a * math.sin(math.radians(yaw))
        self.c, self.s_ = math.cos(self.r), math.sin(self.r)

    def P(self, x, y):
        dy = (y - HIP_Y) * self.k
        return self.L.P(x * self.c - dy * self.s_, HIP_Y + x * self.s_ + dy * self.c)

    def S(self, v):
        return self.L.S(v)


def torso_view(img, p, sp, view, seated=False):
    """The torso for each non-front view, facing right, in the person's own clothes."""
    sw, skin = sp.get('shoulders', 150), sp['skin']
    bottom = min(sp.get('bottom', JACKET), 470) if seated else sp.get('bottom', JACKET)
    out = sp.get('outfit', 'suit')
    jc = sp.get('dress', (190, 30, 44)) if out == 'dress' else sp.get('jacket', (40, 40, 46))
    sc = sp.get('shirt', (244, 244, 240))
    jd = B.dk(jc, 0.72)
    tie = sp.get('tie')
    if view == 'three':
        o = 0.32 * sw
        p.poly([(-24, -80), (40, -80), (46, 10), (-20, 10)], skin, INK, 2.6)
        p.poly([(-30, -4), (-sw * 0.74, 12), (-sw * 0.92, 50), (-sw * 0.97, 200), (-sw * 0.86, bottom), (sw * 0.78, bottom),
                (sw * 0.84, 200), (sw * 0.8, 50), (sw * 0.62, 12), (52, -4)], jc, INK, 2.6)
        if out in ('suit', 'blouse'):
            p.poly([(o - 28, -4), (o + 26, -4), (o + 14, 150), (o + 2, 220), (o - 18, 150)], sc, INK, 2.2)
            if tie:
                p.poly([(o - 8, 16), (o + 10, 16), (o + 13, 180), (o + 2, 206), (o - 10, 180)], tie, INK, 2.0)
            else:
                p.poly([(o - 28, -4), (o - 4, 40), (o - 14, 54), (o - 34, 6)], sc, INK, 2.0)
                p.poly([(o + 26, -4), (o + 6, 38), (o + 14, 50), (o + 30, 6)], sc, INK, 2.0)
                p.poly([(o - 4, 40), (o + 6, 38), (o, 60)], skin, None)
            for sg, k in ((-1, 1.0), (1, 0.6)):
                p.poly([(o + sg * 30, -2), (o + sg * 52 * k, 30), (o + sg * 34 * k, 110), (o + sg * 46 * k, 150),
                        (o + sg * 4, 240), (o + sg * 16 * k, 150)], jc, INK, 2.2)
            p.line([(o, 240), (o + 4, bottom)], jd, 2.2)
        elif out == 'dress':
            p.poly([(o - 34, -4), (o + 30, -4), (o + 18, 46), (o, 62), (o - 22, 46)], skin, INK, 2.0)
        else:
            p.line(oval(o - 4, -2, 40, 18, 20, 0.2, math.pi - 0.2), INK, 2.4)
        p.line([(-sw * 0.6, 60), (-sw * 0.72, bottom - 10)], jd, 2.0)
        soft(img, p.cam, [(-sw * 0.97, 50), (-sw * 0.6, 40), (-sw * 0.6, bottom), (-sw * 0.88, bottom)], (0, 0, 0), 0.25, 10)
        if sp.get('rosette'):
            p.ell(o - 70, 120, 20, 20, (40, 156, 72), INK, 2.4)
            p.ell(o - 70, 120, 8, 8, (248, 248, 240), INK, 1.4)
        if sp.get('lanyard'):
            lc = sp.get('lanyard_c', (40, 140, 70))
            p.line([(o - 30, 0), (o - 12, 200)], lc, 6)
            p.line([(o + 26, 0), (o + 10, 200)], lc, 5)
            p.poly([(o - 30, 196), (o + 24, 196), (o + 24, 270), (o - 30, 270)], (248, 248, 248), INK, 2.0)
    elif view == 'side':
        d = 0.6 * sw
        p.poly([(-26, -80), (24, -80), (34, 8), (-30, 8)], skin, INK, 2.6)
        p.poly(curve([(-34, -8), (-d * 0.92, 22), (-d * 1.02, 130), (-d * 0.96, 320), (-d * 0.92, bottom), (d * 1.0, bottom),
                      (d * 1.02, 300), (d * 1.12, 140), (d * 0.86, 30), (30, -6)], 3), jc, INK, 2.6)
        if out in ('suit', 'blouse'):
            p.poly([(4, -14), (36, -6), (34, 24), (16, 12)], sc, INK, 2.0)
            if tie:
                p.poly([(30, 10), (42, 12), (d * 0.9, 190), (d * 0.8, 186)], tie, INK, 1.8)
            p.line([(34, 0), (d * 0.86, 120), (d * 1.0, 290)], jd, 2.2)
        elif out == 'dress':
            p.poly([(10, -10), (40, -4), (36, 40), (14, 24)], skin, None)
        soft(img, p.cam, [(-d * 1.02, 60), (-d * 0.5, 60), (-d * 0.5, bottom), (-d * 0.92, bottom)], (0, 0, 0), 0.25, 10)
        if sp.get('rosette'):
            p.ell(d * 0.7, 120, 16, 20, (40, 156, 72), INK, 2.4)
        if sp.get('lanyard'):
            lc = sp.get('lanyard_c', (40, 140, 70))
            p.line([(30, 0), (d * 0.95, 200)], lc, 6)
            p.poly([(d * 0.85, 196), (d * 1.05, 196), (d * 1.05, 270), (d * 0.85, 270)], (248, 248, 248), INK, 2.0)
    else:
        k, off = (0.9, -0.22 * sw) if view == 'three_back' else (1.0, 0.0)
        p.poly([(-32, -80), (32, -80), (36, 10), (-36, 10)], skin, INK, 2.6)       # the neck stays under the head
        p.poly([(-40, -4), (-sw * 0.8 * k, 12), (-sw * k, 50), (-(sw + 6) * k, 200), (-(sw - 6) * k, bottom),
                ((sw - 6) * k, bottom), ((sw + 6) * k, 200), (sw * k, 50), (sw * 0.8 * k, 12), (40, -4)], jc, INK, 2.6)
        if out in ('suit', 'blouse'):
            p.poly([(-40, -12), (40, -12), (44, 8), (-44, 8)], sc, INK, 2.0)            # the collar round the neck
            p.poly([(-44, 6), (44, 6), (40, 26), (-40, 26)], B.dk(jc, 0.85), INK, 2.0)
            p.line([(off, 26), (off, bottom - 110)], jd, 2.2)
            p.line([(off, bottom - 110), (off, bottom)], INK, 2.2)
        soft(img, p.cam, [(-sw * k, 60), (-sw * 0.4 * k, 30), (-sw * 0.5 * k, bottom), (-sw * k, bottom)], (0, 0, 0), 0.22, 10)


# ------------------------------------------------------------------------------------------------ head views
def _hair(sp):
    """(top colour, clipped-side colour, kind, length below the ear), from the person's front design."""
    st = sp.get('hair')
    c, skin = sp.get('hair_c', (60, 44, 34)), sp['skin']
    side = blend(skin, c, 0.42) if st == 'fade' else c
    kind = 'bald' if st in BALD else ('long' if st in LONG_HAIR else 'short')
    return c, side, kind, LONG_HAIR.get(st, 0)


def _beard_col(sp):
    skin, c = sp['skin'], sp.get('beard_c', sp.get('hair_c', (90, 80, 74)))
    light = sp.get('beard') in ('short', 'stubble', 'goatee')
    return blend(skin, c, 0.55 if light else 0.9), blend(skin, c, 0.85 if light else 1.0)


def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
    """The head for each view, facing right. 'front' is the library's own head; the others are drawn here from the
    same design (hair kind and colour, beard kind, eyes, brows, nose, glasses, mouth shapes)."""
    if view == 'front':
        return B.head(img, p, sp, t, hx, hy)
    hw, hh, skin = sp.get('hw', 72), sp.get('hh', 90), sp['skin']
    c, side_c, kind, length = _hair(sp)
    bc = sp.get('brow_c', B.dk(c, 0.8))
    bw = sp.get('brow_w', 3.4)
    beard = sp.get('beard')
    bfill, bedge = _beard_col(sp)
    brows = sp.get('brows')
    if view == 'three':
        fx = hx + 0.4 * hw
        if kind == 'long':
            p.poly(curve([(hx - hw * 1.05, hy - 30), (hx - hw * 1.1, hy + length * 0.6), (hx - hw * 0.8, hy + length),
                          (hx + hw * 0.3, hy + length * 0.8), (hx + hw * 0.4, hy + 20), (hx, hy - hh)], 4), c, INK, 2.6)
        outline = curve([(hx - hw, hy - 10), (hx - hw * 0.86, hy - hh * 0.72), (hx - hw * 0.3, hy - hh * 1.04),
                         (hx + hw * 0.45, hy - hh * 0.98), (hx + hw * 0.92, hy - hh * 0.6), (hx + hw * 1.0, hy - 6),
                         (hx + hw * 0.92, hy + hh * 0.55), (hx + hw * 0.62, hy + hh * 1.0), (hx + hw * 0.3, hy + hh * 1.14),
                         (hx - hw * 0.22, hy + hh * 1.04), (hx - hw * 0.72, hy + hh * 0.66), (hx - hw * 0.96, hy + hh * 0.3)], 4)
        p.poly(outline, skin, INK, 2.6)
        p.poly(oval(hx - 0.5 * hw, hy + 6, 12, 22), skin, INK, 2.4)
        p.line([(hx - 0.5 * hw - 2, hy - 4), (hx - 0.5 * hw + 3, hy + 12)], B.dk(skin, 0.8), 1.6)
        soft(img, p.cam, [(hx - hw * 0.95, hy - 20), (hx - hw * 0.6, hy - 30), (hx - hw * 0.6, hy + hh * 0.7),
                          (hx - hw * 0.8, hy + hh * 0.6)], (160, 100, 90), 0.18, 8)
        if beard in ('short', 'trim', 'full', 'white'):
            low = 1.14 if beard in ('short', 'trim') else 1.4
            p.poly(curve([(hx - hw * 0.62, hy + 22), (hx - hw * 0.8, hy + hh * 0.6), (hx - hw * 0.22, hy + hh * low * 0.92),
                          (hx + hw * 0.3, hy + hh * low), (hx + hw * 0.62, hy + hh * 1.0), (hx + hw * 0.92, hy + hh * 0.55),
                          (hx + hw * 0.9, hy + 40), (fx + 22, hy + 74), (fx - 10, hy + 76), (hx - hw * 0.1, hy + 62),
                          (hx - hw * 0.4, hy + 40)], 4), bfill, bedge, 1.6)
            p.poly(curve([(fx - 26, hy + 56), (fx - 6, hy + 49), (fx + 10, hy + 49), (fx + 24, hy + 55), (fx + 14, hy + 57),
                          (fx - 18, hy + 58)], 4), bfill, None)
        elif beard == 'goatee':
            p.poly(curve([(fx - 16, hy + hh * 0.86), (fx + 22, hy + hh * 0.86), (fx + 14, hy + hh * 1.2),
                          (fx + 2, hy + hh * 1.32), (fx - 10, hy + hh * 1.1)], 4), bfill, INK, 1.8)
            p.line([(fx - 24, hy + 56), (fx - 6, hy + 47), (fx + 12, hy + 47), (fx + 24, hy + 56)], bfill, 4)
        elif beard == 'stubble':
            rng = np.random.default_rng(5)
            for _ in range(50):
                a = rng.uniform(0.3, math.pi - 0.3)
                r = rng.uniform(0.6, 0.95)
                p.ell(fx + hw * 0.7 * r * math.cos(a), hy + 30 + hh * 0.7 * r * math.sin(a), 0.9, 0.9, bedge, None)
        blink = sp.get('blink')
        for ex, w in ((fx - 26, 1.0), (fx + 24, 0.62)):
            ey = hy - 8
            if blink:
                p.line([(ex - 15 * w, ey), (ex, ey + 3), (ex + 15 * w, ey)], INK, 2.4)
            else:
                p.poly([(ex - 17 * w, ey), (ex - 8 * w, ey - 8), (ex + 8 * w, ey - 8), (ex + 17 * w, ey), (ex + 8 * w, ey + 7),
                        (ex - 8 * w, ey + 7)], (250, 250, 248), INK, 2.0)
                p.ell(ex + 5 * w, ey + 1, 4.5 * w, 4.5, INK, None)
            if brows == 'fierce':
                p.line([(ex - 14 * w, ey - 26), (ex + 18 * w, ey - 14)], bc, bw * 1.15)
            elif brows in ('joy', 'wow', 'alarm', 'outrage'):
                p.line([(ex - 16 * w, ey - 24), (ex, ey - 32), (ex + 18 * w, ey - 26)], bc, bw)
            else:
                rz = sp.get('brow_raise', 0)
                p.line([(ex - 16 * w, ey - 20 - rz), (ex + 18 * w, ey - 22 - rz)], bc, bw * (0.85 + 0.15 * w))
            if sp.get('glasses'):
                gc = sp.get('glasses_c', (30, 28, 34))
                p.poly([(ex - 24 * w, ey - 16), (ex + 24 * w, ey - 16), (ex + 22 * w, ey + 14), (ex - 22 * w, ey + 14)],
                       None, gc, 4.0)
        if sp.get('glasses'):
            gc = sp.get('glasses_c', (30, 28, 34))
            p.line([(fx - 2, hy - 18), (fx + 2, hy - 18)], gc, 3.4)
            p.line([(fx - 50, hy - 18), (hx - 0.5 * hw + 6, hy - 6)], gc, 3.0)
        if sp.get('nose') == 'long':
            p.line([(fx, hy - 6), (fx + 28, hy + 36), (fx + 12, hy + 42)], INK, 2.0)
        else:
            p.line([(fx, hy - 6), (fx + 22, hy + 28), (fx + 10, hy + 35)], INK, 2.0)
        p.line([(fx + 2, hy + 33), (fx + 6, hy + 36)], INK, 1.6)
        B.mouth(p, sp, t, fx + 4, hy + sp.get('mouth_y', 62))
        p.poly(outline, None, INK, 2.6)           # the head's outline, then hair over it: no skull line in the hair (Sam)
        if sp.get('earring'):
            p.ell(hx - 0.5 * hw, hy + 32, 4, 4, B.GOLD, INK, 1.2)
        if kind == 'bald':
            p.poly(curve([(hx - hw * 0.98, hy - 20), (hx - hw * 0.92, hy - hh * 0.55), (hx - hw * 0.5, hy - hh * 0.6),
                          (hx - hw * 0.62, hy + 4), (hx - hw * 0.95, hy + 24)], 4), c, INK, 2.0)
            p.ell(hx + hw * 0.1, hy - hh * 0.74, hw * 0.24, hh * 0.08, (255, 240, 230), None, rot=0.2)
        else:
            p.poly(curve([(hx - hw * 0.98, hy - 20), (hx - hw * 0.84, hy - hh * 0.7), (hx - hw * 0.3, hy - hh * 1.04),
                          (hx + hw * 0.2, hy - hh * 1.0), (hx - hw * 0.05, hy - hh * 0.6), (hx - hw * 0.32, hy - 10),
                          (hx - hw * 0.62, hy + 4), (hx - hw * 0.95, hy + 24)], 4), side_c, INK, 2.2)
            front = 0.72 if sp.get('hair') != 'fade' else 0.4
            p.poly(curve([(hx - hw * 0.92, hy - hh * 0.5), (hx - hw * 0.76, hy - hh * 0.94), (hx - hw * 0.1, hy - hh * 1.1),
                          (hx + hw * 0.55, hy - hh * 0.98), (hx + hw * 0.9, hy - hh * 0.62), (hx + hw * front, hy - hh * 0.7),
                          (hx + hw * 0.12, hy - hh * 0.66), (hx - hw * 0.25, hy - hh * 0.6)], 4), c, INK, 2.2)
            if kind == 'long':
                p.poly(curve([(hx - hw * 1.08, hy - hh * 0.4), (hx - hw * 1.1, hy + 20), (hx - hw * 0.9, hy + length * 0.5),
                              (hx - hw * 0.4, hy + length * 0.45), (hx - hw * 0.45, hy - 20), (hx - hw * 0.3, hy - hh * 0.6)], 4),
                       c, INK, 2.2)                   # covers the back of the skull

    elif view == 'side':
        face = [(hx - 62, hy - 70), (hx - 40, hy - hh - 6), (hx + 20, hy - hh - 4), (hx + 58, hy - 56), (hx + 64, hy - 24),
                (hx + 62, hy - 6), (hx + 84, hy + 28), (hx + 64, hy + 36), (hx + 68, hy + 52), (hx + 62, hy + 60),
                (hx + 66, hy + 74), (hx + 54, hy + 100), (hx + 18, hy + 108), (hx - 22, hy + 88), (hx - 60, hy + 40)]
        if sp.get('nose') == 'long':
            face[6] = (hx + 92, hy + 32)
        outline = curve(face, 3)
        p.poly(outline, skin, INK if kind == 'bald' else None, 2.6)
        if kind == 'long':                          # long hair falls over the back of the head (no skull showing through)
            p.poly(curve([(hx - 40, hy - hh), (hx - 90, hy - 30), (hx - 96, hy + length * 0.7), (hx - 70, hy + length),
                          (hx - 10, hy + length * 0.8), (hx - 6, hy + 10)], 4), c, INK, 2.6)
        if beard in ('short', 'trim', 'full', 'white'):
            low = 0 if beard in ('short', 'trim') else 30
            p.poly(curve([(hx - 40, hy + 26), (hx - 22, hy + 88 + low), (hx + 18, hy + 108 + low), (hx + 54, hy + 100 + low),
                          (hx + 66, hy + 74), (hx + 60, hy + 64), (hx + 40, hy + 66), (hx + 30, hy + 50), (hx + 40, hy + 40),
                          (hx + 66, hy + 44), (hx + 62, hy + 36), (hx + 20, hy + 34), (hx - 6, hy + 20)], 3), bfill, bedge, 1.4)
        elif beard == 'goatee':
            p.poly(curve([(hx + 30, hy + 74), (hx + 66, hy + 72), (hx + 60, hy + 112), (hx + 40, hy + 106)], 3), bfill, INK, 1.6)
        p.poly(oval(hx - 18, hy + 8, 12, 22), skin, INK, 2.2)
        p.line([(hx - 20, hy - 4), (hx - 14, hy + 12)], B.dk(skin, 0.8), 1.6)
        ex, ey = hx + 42, hy - 10
        if sp.get('blink'):
            p.line([(ex - 10, ey), (ex + 10, ey + 2)], INK, 2.2)
        else:
            p.poly([(ex - 10, ey), (ex + 2, ey - 7), (ex + 12, ey - 2), (ex + 4, ey + 5)], (250, 250, 248), INK, 1.8)
            p.ell(ex + 5, ey - 1, 3.4, 3.4, INK, None)
        tilt = {'fierce': 6, 'joy': -4, 'wow': -6}.get(brows, 0)
        p.line([(ex - 12, ey - 18 - tilt), (ex + 2, ey - 22), (ex + 16, ey - 18 + tilt)], bc, bw)
        if sp.get('glasses'):
            gc = sp.get('glasses_c', (30, 28, 34))
            p.poly([(ex - 6, ey - 14), (ex + 18, ey - 14), (ex + 16, ey + 12), (ex - 4, ey + 12)], None, gc, 3.6)
            p.line([(ex - 6, ey - 8), (hx - 14, hy - 4)], gc, 3.0)
        m = sp.get('mouth', 'set')
        if isinstance(m, str) and m.startswith('v:') and m[2:] not in ('rest', 'MBP'):
            p.poly([(hx + 50, hy + 50), (hx + 66, hy + 48), (hx + 64, hy + 64), (hx + 50, hy + 62)], (120, 30, 40), INK, 1.8)
        elif m in ('smile', 'grin'):
            p.line([(hx + 44, hy + 58), (hx + 56, hy + 62), (hx + 66, hy + 54)], INK, 2.2)
        else:
            p.line([(hx + 46, hy + 58), (hx + 64, hy + 56)], INK, 2.2)
        if kind != 'long':                          # the head's outline first, the hair over it (Sam: never a skull line
            p.poly(outline, None, INK, 2.6)         # showing through hair)
        else:                                       # long hair hides the back of the skull: ink the face's edge only
            p.line(outline[9:40], INK, 2.6)         # (forehead to jaw; curve() closes, so slice the outline)
        if kind == 'bald':
            p.poly(curve([(hx - 66, hy - 30), (hx - 64, hy - 70), (hx - 40, hy - 56), (hx - 34, hy - 20), (hx - 40, hy + 30),
                          (hx - 62, hy + 24)], 3), c, INK, 2.0)
            p.ell(hx, hy - hh * 0.8, 20, 6, (255, 240, 230), None)
        else:
            p.poly(curve([(hx - 66, hy - 30), (hx - 70, hy - 76), (hx - 34, hy - hh - 16), (hx + 24, hy - hh - 14),
                          (hx + 44, hy - hh + 8), (hx + 20, hy - hh + 14), (hx - 6, hy - 56), (hx - 34, hy - 20), (hx - 40, hy + 30),
                          (hx - 62, hy + 24)], 3), side_c, INK, 2.6)       # its back edge is the head's silhouette: lined
            reach = 46 if sp.get('hair') == 'fade' else 60
            p.poly(curve([(hx - 62, hy - 64), (hx - 36, hy - hh - 18), (hx + 26, hy - hh - 16), (hx + reach, hy - hh + 6),
                          (hx + 18, hy - hh + 12), (hx - 10, hy - 62), (hx - 44, hy - 46)], 3), c, INK, 2.2)
        if sp.get('earring'):
            p.ell(hx - 18, hy + 34, 4, 4, B.GOLD, INK, 1.2)
    else:                                           # from behind: the back of the skull, the neck rising straight into it,
        bt = 0.6 if view == 'three_back' else 0.0  # hair drawn over it; no chin, no jaw crease, no stray bits of face (Sam)
        for side in (-1, 1):
            if not (side > 0 and bt > 0):
                p.poly(oval(hx + side * (hw + 2), hy + 6, 12, 22), skin, INK, 2.4)
        outline = curve([(hx - hw, hy - 10), (hx - hw * 0.86, hy - hh * 0.72), (hx, hy - hh * 1.06), (hx + hw * 0.86, hy - hh * 0.72),
                         (hx + hw, hy - 10), (hx + hw * 0.92, hy + hh * 0.42), (hx + hw * 0.66, hy + hh * 0.72), (hx, hy + hh * 0.8),
                         (hx - hw * 0.66, hy + hh * 0.72), (hx - hw * 0.92, hy + hh * 0.42)], 4)
        p.poly(outline, skin, INK, 2.6)
        nw, ny = 32.0, hy + hh * 0.55               # the same neck the body draws
        p.poly([(hx - nw, ny), (hx + nw, ny), (hx + nw, hy + 132), (hx - nw, hy + 132)], skin, None)
        for sg in (-1, 1):
            p.line([(hx + sg * nw, hy + hh * 0.66), (hx + sg * nw, hy + 132)], INK, 2.6)
        if bt > 0:                                  # the near ear, come round towards us
            p.poly(oval(hx + hw * (1 - 0.42 * bt), hy + 6, 12, 22), skin, INK, 2.4)
        if kind == 'bald':
            p.poly(curve([(hx - hw, hy - 10), (hx - hw * 0.9, hy + hh * 0.5), (hx, hy + hh * 0.62), (hx + hw * 0.9, hy + hh * 0.5),
                          (hx + hw, hy - 10), (hx, hy + 10)], 4), c, None)
            p.ell(hx, hy - hh * 0.6, hw * 0.3, hh * 0.1, (255, 240, 230), None)
        else:
            p.poly(curve([(hx - hw * 0.99, hy - 30), (hx - hw * 0.97, hy + 20), (hx - hw * 0.8, hy + hh * 0.5), (hx, hy + hh * 0.66),
                          (hx + hw * 0.8, hy + hh * 0.5), (hx + hw * 0.97, hy + 20), (hx + hw * 0.99, hy - 30), (hx, hy - hh * 0.5)], 4),
                   side_c, INK, 2.2)
            p.poly(curve([(hx - hw * 1.0, hy - hh * 0.5), (hx - hw * 0.84, hy - hh * 0.94), (hx, hy - hh * 1.09),
                          (hx + hw * 0.84, hy - hh * 0.94), (hx + hw * 1.0, hy - hh * 0.5), (hx + hw * 0.5, hy - hh * 0.1),
                          (hx, hy), (hx - hw * 0.5, hy - hh * 0.1)], 4), c, INK, 2.2)
            if kind == 'long':
                p.poly(curve([(hx - hw * 1.08, hy - hh * 0.4), (hx - hw * 1.12, hy + length * 0.7), (hx - hw * 0.8, hy + length),
                              (hx + hw * 0.8, hy + length), (hx + hw * 1.12, hy + length * 0.7), (hx + hw * 1.08, hy - hh * 0.4),
                              (hx, hy - hh * 1.1)], 4), c, INK, 2.6)


# ------------------------------------------------------------------------------------------------ one person
def person(img, cam, x, y, s, sp, t, yaw, joints=None, head_yaw=None):
    """Draw someone facing `yaw` degrees (snapped to the nearest drawn view), neck base at world (x, y), scale s,
    in the pose `joints` (standing() if none). Returns the pose's 2D points (person units) for props and checks."""
    view_deg, mirror = snap(yaw)
    view = VIEWS[view_deg]
    j = joints or standing(sp)
    lean = j.get('lean', 0.0)
    L = B.Local(cam, x, y + j.get('bob', 0.0) * s, s, -1 if mirror else 1)
    p = B.Pen(img, L)
    up = Lean(L, lean, view_deg)
    j2, depth = {}, {}
    for k in ('hipL', 'hipR', 'footL', 'footR'):
        j2[k], depth[k] = project(j[k], view_deg)
    for k in ('shL', 'shR', 'elL', 'elR', 'wrL', 'wrR'):
        j2[k], depth[k] = project(leaned(j[k], lean), view_deg)
    j2['hand'] = j.get('hand', {})
    j2['yaw'] = view_deg                       # so a prop can project its own 3D shape (a steering wheel)
    sp_draw = dict(sp)
    sp_draw['head_dy'] = sp.get('head_dy', 0) + j.get('head_dy', 0)
    seated = j.get('seated', False)
    hips_far = sorted('LR', key=lambda sd: depth['hip' + sd])
    arms_far = sorted('LR', key=lambda sd: depth['sh' + sd])
    behind = set(j.get('behind', set()))
    if view in ('three', 'side', 'three_back'):
        behind.add(arms_far[0])
    if view == 'back':
        behind |= {sd for sd in 'LR' if depth['wr' + sd] < depth['sh' + sd] - 10}   # hands in front of him: hidden by his back (Sam)
    if seated:
        chair(p, view, j2, sp, under=True)
    for sd in hips_far:
        leg(p, j, sd, view_deg, sp)
    for sd in 'LR':
        check_arm3(j, sd, f"{sp.get('name', 'someone')}'s {sd} arm")
    for sd in arms_far:
        if sd in behind:
            arm(p, j2, sd, sp)
    if view == 'front':
        q = dict(sp_draw, pose='none', full=False)
        q.setdefault('bottom', JACKET)
        if seated:
            q['bottom'] = min(q.get('bottom', 560), 470)
        B.torso(img, B.Pen(img, up), q, t)
    else:
        bent = dict(sp_draw, bottom=min(sp_draw.get('bottom', JACKET), 470)) if lean > 12 else sp_draw
        torso_view(img, B.Pen(img, up), bent, view, seated)   # bending: the hem stops at the hips, never a long tail (Sam)
    for sd in arms_far:
        if sd not in behind:
            arm(p, j2, sd, sp)
    if any(getattr(d, 'held', False) for d in j.get('props', [])) and not j.get('grip'):
        raise ValueError(f"{sp.get('name', 'someone')} holds a prop with no hand in front of it: set j['grip']")
    for draw in j.get('props', []):
        draw(p, j2)
    for sd in sorted(j.get('grip', ())):          # a hand gripping a held prop (a fan of cards) is in front of it:
        arm(p, j2, sd, sp)                         # its fingers wrap the side we see (Sam, 19 Oct: Poker Mon)
    hv = VIEWS[snap(head_yaw)[0]] if head_yaw is not None else view
    head_view(img, B.Pen(img, up), sp_draw, t, hv, sp_draw.get('head_dx', 0.0), -150.0 + sp_draw['head_dy'])
    for sd in sorted(j.get('on_face', ())):       # a hand touching the face is in front of it, never inside the skull
        arm(p, j2, sd, sp)
    for draw in j.get('face_props', []):
        draw(p, j2)
    return j2


if __name__ == '__main__':
    print(__doc__)
