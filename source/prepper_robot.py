#!/usr/bin/env python3
"""Prepper Minister: the robot, a gleaming chrome Centurion (2004 Battlestar Galactica; refs robot-1..7 in
references/prepper-minister/), built as a real 3D figure so it turns smoothly however the camera moves (shot 12 goes
all the way round). Drawn in the house style: flat chrome in three tones (lit, shadow side, a hard highlight), one
outline weight, no glows.

What the references show, and where each is drawn (the reference checklist, guides/satire.md):
- the hooded head: a tall rounded hood with a raised crest down its middle (`hood`, `crest`); a narrow face plate
  tapering to a pointed, jaw-like chin (`face`); one horizontal visor slot across it (`slot`) with a single eye in it,
  cobalt for us (the show's is red), sweeping from side to side like a searchlight (`eye`, EYE_SWEEP);
- a segmented neck (`neck*`); big curved shoulder plates rising either side like a cowl (`shoulder*`, `cowl`);
- a chest plate with a centre ridge (`chest`, `ridge`), a slim ribbed waist (`rib*`), a pelvis plate (`pelvis`);
- long thin arms: plain upper arms, plated forearms, jointed fingers (`upper*`, `fore*`, `hand*`);
- long thin legs: plated thighs, knees, shins, three-toed feet (`thigh*`, `knee*`, `shin*`, `toe*`);
- one arm a glowing cobalt blade (ref robot-blade-arm: the forearm opens into a long curved blade, pale core) or an
  open palm with a cobalt core that fires the plasma (ref robot-cannon-palm).
Height 2.1 m (Sam, 24 Oct): they duck through the 2.04 m doors.

The pose: where it stands and faces, how far it leans or twists, where each hand and foot goes (two-bone reach, the
elbow or knee pointing the way it naturally bends), the head's turn; `fall` tips the whole body over about its feet.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
from ed import INK               # noqa: E402

HEIGHT = 2.1
CHROME = ((198, 204, 214), (136, 144, 158), (244, 247, 250))          # lit, shadow, highlight
CHROME_D = ((150, 156, 168), (98, 104, 118), (206, 212, 220))         # the darker plates (face, waist, neck)
SLOT = ((26, 30, 38), (18, 20, 26), (60, 66, 80))
COBALT, COBALT_L, COBALT_D = (48, 112, 255), (176, 214, 255), (24, 64, 190)
WIRE = [(214, 60, 40), (240, 200, 60), (60, 160, 90), (40, 40, 44)]
UPPER, FORE = 0.33, 0.32
THIGH, SHIN = 0.5, 0.46
EYE_SWEEP = 1.6                                                       # seconds for one sweep there and back


# ------------------------------------------------------------------------------------------------ vectors
def _n(v):
    v = np.asarray(v, float)
    n = np.linalg.norm(v)
    return v / n if n > 1e-9 else v


def rot(axis, ang):
    """Rotation matrix about a unit axis (Rodrigues)."""
    a = _n(axis)
    c, s = math.cos(ang), math.sin(ang)
    x, y, z = a
    return np.array([[c + x * x * (1 - c), x * y * (1 - c) - z * s, x * z * (1 - c) + y * s],
                     [y * x * (1 - c) + z * s, c + y * y * (1 - c), y * z * (1 - c) - x * s],
                     [z * x * (1 - c) - y * s, z * y * (1 - c) + x * s, c + z * z * (1 - c)]])


def yaw_m(deg):
    """Local (x right, y up, z forward) to world for a body facing `deg` (0 = north, 90 = east)."""
    a = math.radians(deg)
    return np.array([[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]])


def ik(root, target, l1, l2, pole):
    root, target = np.asarray(root, float), np.asarray(target, float)
    d = target - root
    dist = float(np.linalg.norm(d)) or 1e-6
    dist = min(max(dist, abs(l1 - l2) + 1e-3), l1 + l2 - 1e-4)
    n = d / (np.linalg.norm(d) or 1e-6)
    along = (l1 * l1 - l2 * l2 + dist * dist) / (2 * dist)
    h = math.sqrt(max(0.0, l1 * l1 - along * along))
    pv = np.asarray(pole, float) - n * float(np.dot(pole, n))
    pv = _n(pv) if np.linalg.norm(pv) > 1e-6 else _n(np.cross(n, [1, 0, 0]))
    mid = root + n * along + pv * h
    return mid, root + n * dist


# ------------------------------------------------------------------------------------------------ the pose
STAND = dict(pos=(0.0, 0.0), y=0.0, yaw=0.0, lean=0.0, twist=0.0, tilt=0.0, head_yaw=0.0, head_pitch=0.0,
             handR=(0.33, 0.96, 0.08), handL=(-0.33, 0.96, 0.08), poleR=(0.6, 0.0, -1.0), poleL=(-0.6, 0.0, -1.0),
             footR=(0.13, 0.08, 0.03), footL=(-0.13, 0.08, 0.03), fall=None, sweep=0.0)


def pose(**kw):
    p = dict(STAND)
    p.update(kw)
    return p


def blend(a, b, k):
    """Between two poses (k 0..1): numbers and tuples mixed, the rest from the nearer one."""
    out = {}
    for key in set(a) | set(b):
        va, vb = a.get(key, STAND.get(key)), b.get(key, STAND.get(key))
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            out[key] = va + (vb - va) * k
        elif isinstance(va, tuple) and isinstance(vb, tuple) and len(va) == len(vb) and \
                all(isinstance(q, (int, float)) for q in va + vb):
            out[key] = tuple(x + (y - x) * k for x, y in zip(va, vb))
        else:
            out[key] = va if k < 0.5 else vb
    return out


def skeleton(p):
    """World positions of every joint, and the frames of the chest and head (columns: right, up, forward)."""
    W = yaw_m(p['yaw'])
    base = np.array([p['pos'][0], p['y'], p['pos'][1]])
    hipC = np.array([0.0, 1.05, 0.0])
    # upper body: twist about the spine, lean forward about the hips, tilt sideways
    U = rot([0, 1, 0], math.radians(-p['twist'])) @ rot([1, 0, 0], math.radians(p['lean'])) @ \
        rot([0, 0, 1], math.radians(-p['tilt']))
    def up(v):
        return hipC + U @ (np.asarray(v, float) - hipC)
    J = {}
    J['hipC'] = hipC
    for s, sg in (('R', 1), ('L', -1)):
        J['hip' + s] = np.array([sg * 0.12, 1.02, 0.0])
        J['sh' + s] = up([sg * 0.27, 1.62, 0.0])
        J['hand' + s] = up(p['hand' + s])
        J['el' + s], J['wr' + s] = ik(J['sh' + s], J['hand' + s], UPPER, FORE, U @ np.asarray(p['pole' + s], float))
        J['knee' + s], J['ankle' + s] = ik(J['hip' + s], p['foot' + s], THIGH, SHIN, [sg * 0.15, 0.1, 1.0])
    J['chest'] = up([0, 1.47, 0])
    J['neck'] = up([0, 1.72, 0])
    H = U @ rot([0, 1, 0], math.radians(-p['head_yaw'])) @ rot([1, 0, 0], math.radians(p['head_pitch']))
    J['head'] = J['neck'] + H @ np.array([0, 0.22, 0.02])
    frames = {'chest': U, 'head': H, 'root': np.eye(3)}
    # into the world, then the fall
    F = None
    if p.get('fall'):
        ang, dir_deg = p['fall'][0], p['fall'][1]
        d = np.array([math.sin(math.radians(dir_deg)), 0.0, math.cos(math.radians(dir_deg))])
        axis = np.cross([0, 1, 0], d)                       # tipping towards d
        F = rot(axis, math.radians(ang)) if np.linalg.norm(axis) > 1e-6 else np.eye(3)
    out = {}
    for k, v in J.items():
        w = W @ v
        if F is not None:                                   # tipped over about its feet
            w = F @ w
        out[k] = w + base
    fr = {}
    for k, m in frames.items():
        fr[k] = (F if F is not None else np.eye(3)) @ W @ m
    return out, fr


# ------------------------------------------------------------------------------------------------ shapes
def _ell(c, R, ax, n=9, e=1.0, taper=0.0, squash=None):
    """Points and normals on a (super)ellipsoid: centre c, frame R (columns x, y, z), semi-axes ax; e < 1 boxier;
    taper widens the top (+) or the bottom (-)."""
    pts, nrm = [], []
    for i, a in enumerate(np.linspace(-math.pi / 2, math.pi / 2, n)):
        for b in np.linspace(0, 2 * math.pi, 2 * n, endpoint=False):
            ca, sa, cb, sb = math.cos(a), math.sin(a), math.cos(b), math.sin(b)
            f = lambda v: math.copysign(abs(v) ** e, v)
            x, y, z = f(ca) * f(cb), f(sa), f(ca) * f(sb)
            k = 1.0 + taper * y
            loc = np.array([x * ax[0] * k, y * ax[1], z * ax[2] * k])
            nl = np.array([ca * cb / ax[0], sa / ax[1], ca * sb / ax[2]])
            pts.append(c + R @ loc)
            nrm.append(_n(R @ nl))
    return np.array(pts), np.array(nrm)


def _seg(a, b, r0, r1, n=8, flat=1.0, up=None):
    """A tapered limb from a to b with rounded ends (radius r0 at a, r1 at b)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    L = float(np.linalg.norm(d)) or 1e-6
    ax = d / L
    ref = np.array([0, 1, 0]) if abs(ax[1]) < 0.9 else np.array([1, 0, 0])
    u = _n(np.cross(ax, ref) if up is None else up)
    v = np.cross(ax, u)
    pts, nrm = [], []
    for s in np.linspace(0, 1, 5):
        r = r0 + (r1 - r0) * s
        for q in np.linspace(0, 2 * math.pi, 2 * n, endpoint=False):
            dirn = u * math.cos(q) + v * math.sin(q) * flat
            pts.append(a + d * s + dirn * r)
            nrm.append(_n(dirn))
    for end, r, sg in ((a, r0, -1), (b, r1, 1)):          # the caps
        for q in np.linspace(0, 2 * math.pi, n, endpoint=False):
            for h in (0.5, 0.85):
                dirn = (u * math.cos(q) + v * math.sin(q) * flat) * math.sqrt(1 - h * h) + ax * sg * h
                pts.append(end + dirn * r)
                nrm.append(_n(dirn))
    return np.array(pts), np.array(nrm)


class Part:
    def __init__(self, name, pts, nrm, tone, lw=1.6, flat=None, fill=None):
        self.name, self.pts, self.nrm, self.tone, self.lw = name, pts, nrm, tone, lw
        self.flat, self.fill = flat, fill               # flat: a 3D polygon drawn as is (the blade)
        self.c = pts.mean(axis=0)


def parts(p, spec, t=0.0):
    """Every part of the robot in this pose, in the world."""
    J, Fr = skeleton(p)
    C, H, R0 = Fr['chest'], Fr['head'], Fr['root']
    out = []
    lost = spec.get('lost', set())
    def add(name, pts_nrm, tone, **kw):
        if name.rstrip('LR0123456789') in lost or name in lost:
            return
        out.append(Part(name, pts_nrm[0], pts_nrm[1], tone, **kw))
    X = lambda v: np.asarray(v, float)
    hipC = J['hipC']
    # pelvis, waist, chest
    add('pelvis', _ell(hipC + R0 @ X([0, -0.01, 0]), R0, (0.16, 0.08, 0.12), e=0.6), CHROME)
    for i in range(4):
        add(f'rib{i}', _ell(hipC + C @ X([0, 0.08 + 0.055 * i, 0]), C, (0.085, 0.024, 0.07), n=7), CHROME_D)
    add('chest', _ell(J['chest'], C, (0.23, 0.2, 0.15), e=0.55, taper=0.36), CHROME)
    add('ridge', _ell(J['chest'] + C @ X([0, -0.02, 0.148]), C, (0.026, 0.16, 0.02), n=7), CHROME)
    add('cowl', _ell(J['neck'] + C @ X([0, -0.03, -0.04]), C, (0.24, 0.1, 0.17), e=0.75), CHROME)
    for s, sg in (('R', 1), ('L', -1)):
        Rs = C @ rot([0, 0, 1], math.radians(sg * 26))
        add('shoulder' + s, _ell(J['sh' + s] + C @ X([sg * 0.04, 0.05, 0]), Rs, (0.145, 0.065, 0.16), e=0.55), CHROME)
        Rf = C @ rot([0, 0, 1], math.radians(-sg * 30))      # the hood flaring down onto the shoulders (refs robot-1, 2)
        add('flare' + s, _ell(J['neck'] + C @ X([sg * 0.12, 0.03, 0.01]), Rf, (0.05, 0.11, 0.1), e=0.8), CHROME)
    if not spec.get('headless'):
        for i in range(3):
            add(f'neck{i}', _ell(J['neck'] + H @ X([0, 0.02 + 0.04 * i, 0]), H, (0.055, 0.02, 0.05), n=7), CHROME_D)
        out += head_parts(J['head'], H, p.get('sweep', 0.0), spec)
    else:
        add('stump', _ell(J['neck'] + C @ X([0, 0.03, 0]), C, (0.06, 0.03, 0.055), n=7), SLOT)
    # arms
    for s, sg in (('R', 1), ('L', -1)):
        if 'arm' + s in lost:
            continue
        sh, el, wr = J['sh' + s], J['el' + s], J['wr' + s]
        add('upper' + s, _seg(sh, el, 0.042, 0.04), CHROME_D)
        add('elbow' + s, _ell(el, C, (0.05, 0.05, 0.05), n=7), CHROME)
        kind = spec.get('arms', {}).get(s, 'hand')
        add('fore' + s, _seg(el, wr, 0.07, 0.05), CHROME)
        fd = _n(wr - el)
        if kind == 'blade':
            out += blade_parts(s, wr, fd, C, spec)
        elif kind == 'cannon':
            out += palm_parts(s, wr, fd, C, cannon=True)
        else:
            out += palm_parts(s, wr, fd, C, cannon=False)
    # legs
    for s, sg in (('R', 1), ('L', -1)):
        hip, kn, an = J['hip' + s], J['knee' + s], J['ankle' + s]
        add('thigh' + s, _seg(hip, kn, 0.068, 0.05), CHROME)
        add('knee' + s, _ell(kn, R0, (0.055, 0.055, 0.06), n=7), CHROME_D)
        add('shin' + s, _seg(kn, an, 0.05, 0.034), CHROME)
        fwd = R0 @ X([0, 0, 1])
        fwd = _n(np.array([fwd[0], 0, fwd[2]]))
        rt = np.cross([0, 1, 0], fwd)
        for k, a in enumerate((-0.42, 0.0, 0.42)):        # three toes fanning forward, a heel spur back
            d = fwd * math.cos(a) - rt * math.sin(a)
            add(f'toe{s}{k}', _seg(an + X([0, -0.05, 0]), an + d * 0.17 + X([0, -0.07, 0]), 0.03, 0.018, n=6), CHROME)
        add('heel' + s, _seg(an + X([0, -0.04, 0]), an - fwd * 0.07 + X([0, -0.07, 0]), 0.028, 0.02, n=6), CHROME_D)
        add('ankle' + s, _ell(an, R0, (0.042, 0.042, 0.042), n=6), CHROME_D)
    return out, J


def head_parts(c, H, sweep, spec):
    """The hooded head (refs robot-1..3, 6): hood, crest, the tapering face plate, the visor slot and the eye."""
    X = lambda v: np.asarray(v, float)
    out = [Part('hood', *_ell(c + H @ X([0, 0.02, -0.03]), H, (0.14, 0.2, 0.175), e=0.9, taper=-0.38), CHROME),
           Part('crest', *_ell(c + H @ X([0, 0.12, -0.03]), H, (0.022, 0.07, 0.15), n=7), CHROME),
           Part('face', *_ell(c + H @ X([0, -0.05, 0.095]), H, (0.078, 0.15, 0.07), e=0.8, taper=0.62), CHROME_D),
           Part('slot', *_ell(c + H @ X([0, 0.035, 0.158]), H, (0.058, 0.013, 0.014), n=7, e=0.35), SLOT)]
    for i in range(2):                                        # the vents down the chin (ref robot-6)
        out.append(Part(f'vent{i}', *_ell(c + H @ X([0, -0.06 - 0.04 * i, 0.152 - 0.015 * i]), H,
                                         (0.03 - 0.008 * i, 0.004, 0.01), n=5, e=0.4), SLOT, lw=0.8))
    if not spec.get('dead'):
        u = 0.05 * sweep
        out.append(Part('eye', *_ell(c + H @ X([u, 0.035, 0.176]), H, (0.022, 0.011, 0.006), n=6, e=0.5),
                        (COBALT, COBALT, COBALT_L)))
    return out


def palm_parts(s, wr, fd, C, cannon):
    """The hand: an open palm across the wrist with three jointed fingers. A cannon palm turns back to face its
    target (the plasma fires from it) with the cobalt core in its centre (ref robot-cannon-palm)."""
    X = lambda v: np.asarray(v, float)
    side = C @ X([1 if s == 'R' else -1, 0, 0])
    up = _n(np.cross(fd, side)) if np.linalg.norm(np.cross(fd, side)) > 1e-6 else C @ X([0, 1, 0])
    if cannon:
        R = np.column_stack([_n(np.cross(up, fd)), up, fd])
        c = wr + fd * 0.035
        out = [Part('palm' + s, *_ell(c, R, (0.055, 0.06, 0.022), n=7), CHROME_D),
               Part('core' + s, *_ell(c + fd * 0.024, R, (0.03, 0.03, 0.006), n=7), (COBALT, COBALT, COBALT_L))]
        for k, a in enumerate((-0.7, 0.0, 0.7)):
            base = c + up * 0.05 * math.cos(a) + R[:, 0] * 0.05 * math.sin(a)
            tip = base + fd * 0.06 + (base - c) * 0.6
            out.append(Part(f'finger{s}{k}', *_seg(base, tip, 0.014, 0.011, n=5), CHROME))
        return out
    c = wr + fd * 0.06
    R = np.column_stack([_n(np.cross(up, fd)), fd, up])
    out = [Part('palm' + s, *_ell(c, np.column_stack([R[:, 0], fd, up]), (0.04, 0.055, 0.022), n=7), CHROME_D)]
    for k, o in enumerate((-0.025, 0.0, 0.025)):
        base = c + fd * 0.05 + R[:, 0] * o
        mid = base + fd * 0.05 - up * 0.01
        tip = mid + fd * 0.035 - up * 0.025
        out.append(Part(f'finger{s}{k}', *_seg(base, mid, 0.012, 0.011, n=5), CHROME))
        out.append(Part(f'fingertip{s}{k}', *_seg(mid, tip, 0.011, 0.009, n=5), CHROME))
    return out


def blade_parts(s, wr, fd, C, spec):
    """The blade arm (ref robot-blade-arm): the forearm opens into a long, curved cobalt blade with a pale core, its
    edge forward, flat in the arm's vertical plane (it foreshortens when it points at us)."""
    X = lambda v: np.asarray(v, float)
    side = C @ X([1 if s == 'R' else -1, 0, 0])
    nrm = side - fd * float(np.dot(side, fd))
    nrm = _n(nrm)
    up = _n(np.cross(nrm, fd))
    if up[1] < 0:
        up = -up
    L = spec.get('blade_len', 0.78)
    def P(u, v):                                            # u along the blade, v across it (edge up), a curve back
        return wr + fd * u + up * (v - 0.12 * (u / L) ** 2)
    outer = [P(-0.06, 0.03), P(0.1, 0.07), P(0.4, 0.075), P(0.65, 0.05), P(L, -0.05), P(0.6, -0.02), P(0.3, -0.03),
             P(0.05, -0.05), P(-0.08, -0.03)]
    inner = [P(0.05, 0.02), P(0.35, 0.04), P(0.6, 0.025), P(L - 0.08, -0.03), P(0.5, -0.008), P(0.2, -0.012)]
    housing = _seg(wr - fd * 0.04, wr + fd * 0.06, 0.055, 0.045)
    return [Part('blade' + s, np.array(outer), np.tile(nrm, (len(outer), 1)), (COBALT, COBALT, COBALT), flat=True),
            Part('bladecore' + s, np.array(inner), np.tile(nrm, (len(inner), 1)), (COBALT_L, COBALT_L, COBALT_L),
                 flat=True, lw=0),
            Part('housing' + s, housing[0], housing[1], CHROME_D)]


# ------------------------------------------------------------------------------------------------ drawing
def project(cam, P):
    """Many world points at once: screen x, y (1080 x 1920) and depth."""
    d = P - np.asarray(cam.pos)
    z = np.maximum(d @ np.asarray(cam.f), cam.NEAR)
    k = cam.focal / z
    x, y = (d @ np.asarray(cam.r)) * k, -(d @ np.asarray(cam.u)) * k
    if getattr(cam, 'roll', 0.0):
        c, s = math.cos(cam.roll), math.sin(cam.roll)
        x, y = x * c - y * s, x * s + y * c
    return 540 + x + cam.shake[0], 960 + y + cam.shake[1], d @ np.asarray(cam.f)


def _hull(xy):
    pts = sorted(set((round(float(a), 1), round(float(b), 1)) for a, b in xy))
    if len(pts) < 3:
        return pts
    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for q in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], q) <= 0:
            hi.pop()
        hi.append(q)
    return lo[:-1] + hi[:-1]


FLAT = B.Cam(1.0, 540, 960)


def light(cam):
    """The light comes from above the camera's left shoulder (the same on every robot, every shot)."""
    return _n(np.asarray(cam.u) * 0.75 - np.asarray(cam.r) * 0.45 - np.asarray(cam.f) * 0.5)


def draw_part(pen, cam, part, L, tint=None):
    X, Y, D = project(cam, part.pts)
    if (D < cam.NEAR + 0.02).any():
        return
    lit, shade, hi = part.tone
    if tint is not None:
        lit, shade, hi = (tuple(int(a + (b - a) * tint[1]) for a, b in zip(c, tint[0])) for c in (lit, shade, hi))
    if part.flat:
        pen.poly(list(zip(X, Y)), lit, INK if part.lw else None, part.lw or 1)
        return
    h = _hull(zip(X, Y))
    if len(h) < 3:
        return
    pen.poly(h, lit, None)
    dots = part.nrm @ L
    dark = dots < -0.05
    if dark.sum() >= 3:
        hs = _hull(zip(X[dark], Y[dark]))
        if len(hs) >= 3:
            pen.poly(hs, shade, None)
    view = _n(np.asarray(cam.pos) - part.c)
    half = _n(L + view)
    spec = (part.nrm @ half) > 0.8
    if spec.sum() >= 3:                                       # a hard highlight: the shiniest spot, shrunk and rounded
        hs = _hull(zip(X[spec], Y[spec]))
        if len(hs) >= 3:
            cx, cy = sum(q[0] for q in hs) / len(hs), sum(q[1] for q in hs) / len(hs)
            hs = [(cx + (q[0] - cx) * 0.6, cy + (q[1] - cy) * 0.6) for q in hs]
            from ed import curve
            pen.poly(curve(hs, 3), hi, None)
    pen.poly(h, None, INK, part.lw)


def draw(img, cam, p, spec, t=0.0, tint=None):
    """Draw one robot. Returns its joints (world) and the key points for effects: the eye, the palm core (the plasma
    leaves from it), the blade's tip."""
    ps, J = parts(p, spec, t)
    pen = B.Pen(img, FLAT)
    L = light(cam)
    holes = spec.get('holes', [])
    for part in sorted(ps, key=lambda q: -float(np.dot(q.c - np.asarray(cam.pos), np.asarray(cam.f)))):
        draw_part(pen, cam, part, L, tint)
        for h in holes:                                         # bullet holes stay where they hit
            if h['part'] == part.name and t >= h['t']:
                hole(pen, cam, part, h)
    if spec.get('headless'):                                    # torn wiring from the neck
        for k, col in enumerate(WIRE):
            a = J['neck'] + np.array([0.02 * (k - 1.5), 0.04, 0.0])
            b = a + np.array([0.04 * math.sin(k * 2.1 + t * 7), 0.08 + 0.02 * k, 0.04 * math.cos(k * 1.7 + t * 5)])
            X, Y, D = project(cam, np.array([a, b]))
            if (D > cam.NEAR).all():
                pen.line(list(zip(X, Y)), col, 3.0)
    key = {'joints': J}
    for q in ps:
        if q.name.startswith('core'):
            key['core' + q.name[-1]] = q.c
        if q.name == 'eye':
            key['eye'] = q.c
        if q.name.startswith('blade') and not q.name.startswith('bladecore'):
            key['blade' + q.name[-1]] = q.pts[4]
    return key


def hole(pen, cam, part, h):
    """A bullet hole: a dark puncture with a bright torn rim, on the part's surface where it was hit."""
    i = h.get('i', 0) % len(part.pts)
    c, n = part.pts[i], part.nrm[i]
    if float(np.dot(n, np.asarray(cam.pos) - c)) <= 0:
        return
    a = _n(np.cross(n, [0, 1, 0]) if abs(n[1]) < 0.9 else np.cross(n, [1, 0, 0]))
    b = np.cross(n, a)
    if h.get('dent'):                                           # a dent (the tin, Sam's note 30): a shallow dish
        r = h.get('r', 0.05)                                    # pushed in, its upper lip in shadow, a hard glint
        rim = np.array([c + n * 0.002 + (a * math.cos(q) * 1.15 + b * math.sin(q) * 0.85) * r * (1 + 0.12 * math.sin(4 * q))
                        for q in np.linspace(0, 2 * math.pi, 12, endpoint=False)])
        X, Y, D = project(cam, rim)
        pen.poly(list(zip(X, Y)), CHROME[1], INK, 1.2)
        top = np.array([c + n * 0.003 + (a * math.cos(q) * 1.0 + b * math.sin(q) * 0.7) * r
                        for q in np.linspace(0.15 * math.pi, 0.85 * math.pi, 7)] +
                       [c + n * 0.003 + (a * math.cos(q) * 0.8 + b * (math.sin(q) * 0.25 + 0.1)) * r
                        for q in np.linspace(0.85 * math.pi, 0.15 * math.pi, 7)])
        X, Y, D = project(cam, top)
        pen.poly(list(zip(X, Y)), (70, 74, 82), None)
        X, Y, D = project(cam, np.array([c + n * 0.004 - b * r * 0.45 - a * r * 0.4, c + n * 0.004 - b * r * 0.5 + a * r * 0.3]))
        pen.line(list(zip(X, Y)), (250, 252, 255), 2.0)
        return
    r = h.get('r', 0.016)
    ring = np.array([c + n * 0.002 + (a * math.cos(q) + b * math.sin(q)) * r * (1.0 + 0.25 * math.sin(3 * q))
                     for q in np.linspace(0, 2 * math.pi, 8, endpoint=False)])
    X, Y, D = project(cam, ring)
    pen.poly(list(zip(X, Y)), CHROME[2], INK, 1.0)
    X, Y, D = project(cam, c + n * 0.003 + (ring - c) * 0.55)
    pen.poly(list(zip(X, Y)), (20, 20, 24), None)


def solids(p, spec):
    """Spheres for the collision and pop-in audits (audit.py): (name, centre, radius)."""
    ps, J = parts(p, spec)
    out = []
    for q in ps:
        if q.flat:
            continue
        r = float(np.max(np.linalg.norm(q.pts - q.c, axis=1)))
        out.append((q.name, tuple(q.c), r * 0.85))
    return out


# ------------------------------------------------------------------------------------------------ movement
def eye_sweep(t, phase=0.0):
    """The eye runs back and forth across the slot like a searchlight: quick across, a beat at each end."""
    u = ((t + phase) / EYE_SWEEP) % 1.0
    s = math.sin(2 * math.pi * u)
    return max(-1.0, min(1.0, 1.25 * s))


def walk(t, start, end, t0, t1, stride=0.62, phase=0.0, arms='hang'):
    """Walking from start to end (plan points) between t0 and t1: a long mechanical stride, feet planted while down
    (never sliding), the body bobbing a little at each step, facing the way it goes."""
    sx, sz = start
    ex, ez = end
    L = math.hypot(ex - sx, ez - sz) or 1e-6
    u = min(1.0, max(0.0, (t - t0) / max(1e-6, t1 - t0)))
    dist = L * u
    yaw = math.degrees(math.atan2(ex - sx, ez - sz))
    pos = (sx + (ex - sx) * u, sz + (ez - sz) * u)
    cyc = dist / (2 * stride) + phase
    if t >= t1 or t <= t0:
        cyc_on = False
    else:
        cyc_on = True
    feet = {}
    for s, sg, off in (('R', 1, 0.0), ('L', -1, 0.5)):
        ph = (cyc + off) % 1.0
        if not cyc_on:
            fz, fy = 0.03, 0.08
        elif ph < 0.6:                                         # planted: moving back under the body as it goes on
            fz = stride * 0.5 - (ph / 0.6) * stride
            fy = 0.08
        else:                                                  # swinging forward, lifted
            k = (ph - 0.6) / 0.4
            fz = -stride * 0.5 + k * stride
            fy = 0.08 + 0.12 * math.sin(math.pi * k)
        feet['foot' + s] = (sg * 0.13, fy, fz)
    bob = -0.03 * abs(math.sin(2 * math.pi * cyc)) if cyc_on else 0.0
    sw = math.sin(2 * math.pi * cyc) if cyc_on else 0.0
    q = dict(pos=pos, yaw=yaw, y=bob, lean=6.0 if cyc_on else 0.0, **feet)
    if arms == 'hang':                                         # the arms swing against the legs
        q['handR'] = (0.33, 0.98, 0.08 - 0.16 * sw)
        q['handL'] = (-0.33, 0.98, 0.08 + 0.16 * sw)
    return q


def aim(target, origin, yaw, side='R', reach=0.6, height=1.62):
    """A hand reaching straight out at a world target (the cannon's palm or the blade's point), in the body's own
    frame (facing `yaw`): returns (hand, pole)."""
    sg = 1 if side == 'R' else -1
    d = np.asarray(target, float) - np.asarray([origin[0], height, origin[1]])
    W = yaw_m(yaw)
    loc = W.T @ d
    loc = _n(loc)
    sh = np.array([sg * 0.27, 1.62, 0.0])                    # the shoulder in its own frame (height is in the world)
    hand = sh + loc * reach
    return tuple(hand), (sg * 0.4, -0.6, -0.5)


if __name__ == '__main__':
    print(__doc__)
