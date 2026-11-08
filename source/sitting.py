#!/usr/bin/env python3
"""sitting: the sitting kit (Sam, 7 Nov: "the full gamut of sitting animation"; plan in notes/sitting-kit.md).

MAP
- Seat, Desk: the seat and desk measured once (person units: 1 unit = 1.52 mm; floor at 928 below the standing neck).
  Kinds: office (swivels, reclines), armchair (low, deep, arms, the cushion gives), stool (no back). Each draws
  itself from all five views, split into what is beyond the person ('pre') and what is nearer ('mid').
- Spec -> realize(): a pose is a few numbers (lean, lift off the seat, forward travel dz, feet on the floor, each
  hand's target in the body's frame, resting arms laid on a surface). Moves interpolate specs, never joints, so the
  arms are solved fresh each drawing and keep their length.
- POSES: upright (hands on thighs), hands_folded (forearms on the desk; Vance, line 1), lean_in (elbows on the desk,
  hands together), lean_back (chair reclined, hands behind the head), lean_back_belly, armrests (armchair).
- MOVES (12 drawings a second; DUR): stand_up, sit_down (and a 'plonk'), lean_back_move, idle (the moving hold),
  gesture (any moves.pose gesture from the seat).
- CHECKS: check_frame (hips on the seat, feet on the floor, legs reach and bend the right way, resting arms on their
  surface, the chair follows the lean), check_no_sink (rule 80), check_balance, run over a whole move by audit().
- python3 source/sitting.py sheet OUT.jpg | refs OUT.jpg | clips OUT_DIR | audit

Front on (rule 38) the knees and lap show: realize() sets j['lap'] and views.leg draws the thigh over the shin
with a round knee (rule 80). Old films keep moves.seated; new films use this kit.
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import figure as F           # noqa: E402
import views as V            # noqa: E402
from ed import INK           # noqa: E402

FPS = 12
SIT = 40.0                   # the hip joint sits this far above the seat: the thigh's half-thickness (no thigh in the seat)
FLOOR = 928.0
ANKLE_UP = FLOOR - V.ANKLE_Y  # 38: the ankle above the sole
SLEEVE = 17.0                # a resting forearm's centre line is this far above the surface it lies on
DUR = {'stand_up': 1.1, 'stand_up_quick': 0.7, 'stand_up_weary': 1.8, 'sit_down': 1.3, 'plonk': 0.55,
       'sit_down_careful': 2.0, 'lean_back': 0.6}


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, k):
    return a + (b - a) * k


def seg(u, a, b):
    """0 before a, 1 after b, eased between."""
    return ease((u - a) / (b - a)) if b > a else float(u >= a)


def vlerp(a, b, k):
    return tuple(x + (y - x) * k for x, y in zip(a, b))


def rot(v, lean):
    """A direction tipped forward by `lean` degrees (as views.leaned, without the pivot)."""
    L = math.radians(lean)
    x, y, z = v
    return x, y * math.cos(L) + z * math.sin(L), z * math.cos(L) - y * math.sin(L)


# ------------------------------------------------------------------------------------------------ the set pieces
def _box(p, yaw, x0, x1, y0, y1, z0, z1, col, top=None, tilt=0.0, shift=0.0):
    """A box in the body's frame (x across, y down, z forward), tipped back `tilt` degrees about the hips (a
    reclined chair back) and moved `shift` along z (the body's own forward travel, undone). Drawn as its outline,
    then its top face lighter (the camera is a little above)."""
    def P(x, y, z):
        q = V.leaned((x, y, z), tilt) if tilt else (x, y, z)
        return V.project((q[0], q[1], q[2] + shift), yaw)[0]
    pts = [P(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    p.poly(V._hull(pts), col, INK, 2.4)
    if top:
        p.poly([P(x0, y0, z0), P(x1, y0, z0), P(x1, y0, z1), P(x0, y0, z1)], top, INK, 1.6)


def _depth(x, z, yaw):
    return V.project((x, 0.0, z), yaw)[1]


class Seat:
    """A seat, measured: `h` its top above the floor, `front` its front edge and `rear` its back edge (z from the
    hip joint), `back_top` how high the back rises above the seat (None: no back), `arms` the armrests' height above
    the seat (None: none), `cushion` how far the hips sink in. Defaults are an office chair: 0.40 m (in our people's
    proportions, thighs a little down to the knee, as a real 0.45 m chair is for a real body)."""
    KINDS = {
        'office': dict(h=260, front=130, rear=-125, width=125, back_top=300, arms=None, cushion=0, swivel=True,
                       col=(58, 60, 68), top=(84, 86, 96)),
        'armchair': dict(h=190, front=165, rear=-160, width=150, back_top=330, arms=205, cushion=22, swivel=False,
                         col=(122, 58, 52), top=(150, 76, 68)),
        'stool': dict(h=270, front=95, rear=-95, width=105, back_top=None, arms=None, cushion=0, swivel=False,
                      col=(128, 96, 64), top=(160, 124, 86)),
    }

    def __init__(self, kind='office', desk=None, **kw):
        self.kind = kind
        for k, v in dict(self.KINDS[kind], **kw).items():
            setattr(self, k, v)
        self.desk = desk

    @property
    def bob(self):
        """How far the body drops to sit (person units): the hips on the seat."""
        return FLOOR - self.h - (V.HIP_Y + SIT) + self.cushion

    def surface(self):
        """The seat's top in the body frame of a seated person."""
        return V.HIP_Y + SIT - self.cushion

    def draw(self, p, view, j, layer):
        yaw = j2yaw(view)
        bob, dz, lean = j.get('bob', 0.0), j.get('dz', 0.0), j.get('lean', 0.0)
        sh = -dz                                         # the seat stays put while the body travels
        floor = FLOOR - bob
        top = floor - self.h                             # the seat's top, wherever the body is
        recline = max(0.0, -lean) if j.get('lift', 0.0) < 0.05 else 0.0   # the back gives with a lean back
        j['_recline'] = recline
        w, c, ct = self.width, self.col, self.top
        parts = []                                       # (depth, layer-fixed, draw)
        if self.kind == 'office':
            def base(p):
                hub = V.project((0.0, floor - 36, -5 + sh), yaw)[0]
                for k in range(5):
                    a = math.radians(90 + 72 * k)
                    end3 = (190 * math.cos(a), floor - 22, -5 + 190 * math.sin(a) + sh)
                    end = V.project(end3, yaw)[0]
                    p.line([hub, end], (34, 34, 38), 11)
                    p.ell(end[0], end[1] + 8, 15, 11, (26, 26, 30), INK, 1.6)
                col_top = V.project((0.0, top + 30, -5 + sh), yaw)[0]
                p.line([col_top, hub], (40, 40, 46), 14)
            parts.append((-999, 'pre', base))
        else:
            leg_h = self.h - (40 if self.kind == 'armchair' else 30)
            for lx in (-w + 14, w - 14):
                for lz in (self.rear + 14, self.front - 14):
                    def leg(p, lx=lx, lz=lz):
                        a = V.project((lx, top + 30, lz + sh), yaw)[0]
                        b = V.project((lx * (1.08 if self.kind == 'stool' else 1), floor, lz * (1.08 if self.kind == 'stool' else 1) + sh), yaw)[0]
                        p.line([a, b], (52, 40, 30) if self.kind == 'stool' else (40, 30, 26), 10)
                    parts.append((_depth(lx, lz + sh, yaw) - 400, 'pre', leg))
            if self.kind == 'armchair':
                parts.append((-500, 'pre', lambda p: _box(p, yaw, -w - 50, w + 50, top + 6, floor - 30, self.rear,
                                                          self.front, c, None, 0, sh)))
        parts.append((-300, 'pre', lambda p: _box(p, yaw, -w, w, top, top + 30, self.rear, self.front, c, ct, 0, sh)))
        if self.back_top:
            bz = -78 if self.kind == 'office' else -86
            thick = 28 if self.kind == 'office' else 60
            bw = w - 10 if self.kind == 'office' else w + 50

            def back(p):
                _box(p, yaw, -bw, bw, top - self.back_top, top - 8, bz - thick, bz, c, ct, -recline, sh)
            parts.append((_depth(0, bz - thick / 2 + sh, yaw), 'auto', back))
        if self.arms:
            for sx in (-1, 1):
                def arm(p, sx=sx):
                    x0, x1 = sorted((sx * w, sx * (w + 50)))
                    _box(p, yaw, x0, x1, top - self.arms, top + 10, self.rear, self.front, c, ct, 0, sh)
                parts.append((_depth(sx * (w + 25), (self.rear + self.front) / 2 + sh, yaw), 'auto', arm))
        for d, fixed, fn in sorted(parts, key=lambda q: q[0]):
            lay = fixed if fixed != 'auto' else ('mid' if d > 70 else 'pre')
            if lay == layer:
                fn(p)


class Desk:
    """A plain desk in front of a seated person: top `h` above the floor (0.71 m), its near edge `front` units in
    front of the hips, `depth` deep, `width` wide (0.76 m: a hand's width above the seated elbow, as real desks are
    for real bodies); a modesty panel on the far side and a panel at each end."""
    def __init__(self, h=500, front=125, depth=430, width=440, col=(122, 88, 58), top=(150, 112, 76)):
        self.h, self.front, self.depth, self.width, self.col, self.top_col = h, front, depth, width, col, top

    def surface(self, bob):
        return FLOOR - self.h - bob

    def draw(self, p, view, j, layer):
        yaw = j2yaw(view)
        bob, sh = j.get('bob', 0.0), -j.get('dz', 0.0)
        floor, top = FLOOR - bob, FLOOR - self.h - bob
        w, z0, z1 = self.width, self.front, self.front + self.depth
        parts = [
            (_depth(0, z1 - 10 + sh, yaw), lambda p: _box(p, yaw, -w + 20, w - 20, top + 30, floor - 60, z1 - 30, z1 - 14,
                                                           self.col, None, 0, sh)),
            (_depth(-w + 18, (z0 + z1) / 2 + sh, yaw), lambda p: _box(p, yaw, -w, -w + 36, top + 20, floor, z0 + 10, z1,
                                                                       self.col, self.top_col, 0, sh)),
            (_depth(w - 18, (z0 + z1) / 2 + sh, yaw), lambda p: _box(p, yaw, w - 36, w, top + 20, floor, z0 + 10, z1,
                                                                      self.col, self.top_col, 0, sh)),
            (_depth(0, (z0 + z1) / 2 + sh, yaw), lambda p: _box(p, yaw, -w, w, top, top + 26, z0, z1, self.col,
                                                                 self.top_col, 0, sh)),
        ]
        for d, fn in sorted(parts, key=lambda q: q[0]):
            if ('mid' if d > -40 else 'pre') == layer:
                fn(p)


def j2yaw(view):
    return {'front': 0, 'three': 45, 'side': 90, 'three_back': 135, 'back': 180}[view]


# ------------------------------------------------------------------------------------------------ specs
def _spec(**kw):
    s = dict(lean=0.0, lift=0.0, dz=0.0, head_dy=0.0, feet=None, foot_up=None, arms={}, recline=0.0)
    s.update(kw)
    return s


def mix(a, b, k):
    """A spec part-way between two (numbers and hand targets eased; a hand's shape from the nearer one)."""
    out = {}
    for key in set(a) | set(b):
        x, y = a.get(key), b.get(key)
        if key == 'arms':
            out[key] = {}
            for s in 'LR':
                ax, bx = x.get(s), y.get(s)
                if ax is None or bx is None:
                    out[key][s] = ax or bx
                    continue
                out[key][s] = dict(hand=vlerp(ax['hand'], bx['hand'], k),
                                   pole=vlerp(ax['pole'], bx['pole'], k),
                                   shape=(ax if k < 0.5 else bx)['shape'],
                                   rest=(ax if k < 0.5 else bx).get('rest'),
                                   elbow_rest=(ax if k < 0.5 else bx).get('elbow_rest'))
        elif key in ('feet', 'foot_up'):
            if x is None or y is None:
                out[key] = x if k < 0.5 else y
            else:
                out[key] = {s: (vlerp(x[s], y[s], k) if isinstance(x[s], tuple) else lerp(x[s], y[s], k)) for s in x}
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)):
            out[key] = lerp(x, y, k)
        else:
            out[key] = x if k < 0.5 else y
    return out


def keyed(u, keys):
    """A spec from timed keys [(u, spec)], eased between neighbours."""
    if u <= keys[0][0]:
        return keys[0][1]
    for (u0, a), (u1, b) in zip(keys, keys[1:]):
        if u <= u1:
            return mix(a, b, ease((u - u0) / (u1 - u0)))
    return keys[-1][1]


def _elbow_on_plane(S, H, yp, U, Fo, sg):
    """An elbow lying on the plane y = yp, `U` from the shoulder S and `Fo` from the hand H: the outer of the two
    places (the forearm turns in a little, rule 78). None if the shoulder can't reach the plane there."""
    r1 = U * U - (yp - S[1]) ** 2
    r2 = Fo * Fo - (yp - H[1]) ** 2
    if r1 <= 0 or r2 <= 0:
        return None
    r1, r2 = math.sqrt(r1), math.sqrt(r2)
    dx, dz = H[0] - S[0], H[2] - S[2]
    d = math.hypot(dx, dz)
    if d > r1 + r2 or d < abs(r1 - r2) or d < 1e-6:
        return None
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, r1 * r1 - a * a))
    px, pz = S[0] + a * dx / d, S[2] + a * dz / d
    c1 = (px + h * dz / d, yp, pz - h * dx / d)
    c2 = (px - h * dz / d, yp, pz + h * dx / d)
    return max((c1, c2), key=lambda e: sg * e[0])


def arm_free(hand, pole=(0.35, 1.0, -0.25), shape='fist'):
    """A hand at a point in the body's frame (after the lean), the elbow towards `pole` (x as for the right arm)."""
    return dict(hand=tuple(hand), pole=tuple(pole), shape=shape)


def arm_rest(hand, surface_y, shape='fist'):
    """A forearm lying on a surface (desk, armrest): the hand and the elbow both on it (rule 78)."""
    return dict(hand=(hand[0], surface_y - SLEEVE, hand[2]), pole=(0.6, 0.6, -0.2), shape=shape,
                rest=surface_y - SLEEVE)


def realize(sp, seat, spec, lap=True):
    """The joints for views.person: hips on the seat (or rising off it), feet on the floor, arms solved."""
    j = V.standing(sp)
    lift, lean, dz = spec['lift'], spec['lean'], spec['dz']
    bob = seat.bob * (1 - lift) + spec.get('dip', 0.0)
    j['bob'], j['lean'], j['dz'], j['lift'] = bob, lean, dz, lift
    j['head_dy'] = spec.get('head_dy', 0.0)
    floor = FLOOR - bob
    feet = spec['feet'] or {'L': (-64, 235.0), 'R': (64, 235.0)}
    up = spec.get('foot_up') or {}
    for s, sg in (('L', -1), ('R', 1)):
        fx, fz = feet[s]
        j['foot' + s] = (fx, floor - ANKLE_UP - up.get(s, 0.0), fz - dz)
        k = ease(min(1.0, lift / 0.85))
        j['knee_pole' + s] = (sg * lerp(0.1, 0.12, k), lerp(-1.0, 0.0, k), lerp(0.7, 1.0, k))
    j['_faults'] = []
    for s, sg in (('L', -1), ('R', 1)):
        a = spec['arms'].get(s)
        if not a:
            continue
        S = V.leaned(j['sh' + s], lean)
        H = (a['hand'][0] * (1 if s == 'R' else -1), a['hand'][1], a['hand'][2])
        off = F.HAND.get(a['shape'], 14)
        U, Fo = F.UPPER * 0.98, F.FORE * 0.98 + off
        pole = (a['pole'][0] * sg, a['pole'][1], a['pole'][2])
        plane = a.get('rest') if a.get('rest') is not None else a.get('elbow_rest')
        if plane is not None:
            E = _elbow_on_plane(S, H, plane, U, Fo, sg)
            if E is None:
                j['_faults'].append(f'{s} forearm cannot lie on the surface from here: lean in, or move the desk')
            else:
                mid = vlerp(S, H, 0.5)
                pole = tuple(e - m for e, m in zip(E, mid))
        Ht = V.leaned(H, -lean)
        Pt = rot(pole, -lean)
        V.arm_to(j, s, Ht, (Pt[0] * sg, Pt[1], Pt[2]), a['shape'])
    j['seated'] = lift < 0.3
    j['lap'] = lap
    j['spec'], j['seat'] = spec, seat
    j['chair_draw'] = lambda p, view, j2, sp_, under=True: seat.draw(p, view, j, 'pre')
    j['mid'] = [lambda p, j2, view: seat.draw(p, view, j, 'mid')]
    j['pre'] = []
    if seat.desk:
        j['pre'].append(lambda p, j2, view: seat.desk.draw(p, view, j, 'pre'))
        j['mid'].append(lambda p, j2, view: seat.desk.draw(p, view, j, 'mid'))
    if spec.get('tucked'):
        j['tucked'] = spec['tucked']
    if not j['seated']:                       # standing: views draws no chair, so the seat comes in through the layers
        j['pre'].insert(0, lambda p, j2, view: seat.draw(p, view, j, 'pre'))
    return j


# ------------------------------------------------------------------------------------------------ poses
def _thigh_rest(seat, sg, u=0.62):
    """A hand resting on the top of the thigh, `u` of the way to the knee (body frame, seated)."""
    knee_z = 215.0
    y = V.HIP_Y - 46 + 30 * u
    return (sg * 78.0, y, knee_z * u)


def spec_upright(sp, seat, hands='thighs'):
    sw = sp.get('shoulders', 150)
    arms = {}
    if hands == 'thighs':
        for s, sg in (('L', -1), ('R', 1)):
            arms[s] = arm_free(_thigh_rest(seat, 1), (0.25, 0.3, -1.0), 'palm')
    elif hands == 'lap':
        for s in 'LR':
            arms[s] = arm_free((14.0, 420.0, 150.0), (0.6, 0.6, -0.3), 'fist')
    return _spec(arms=arms)


def spec_hands_folded(sp, seat):
    """Forearms on the desk, hands meeting in front (Ad-Vanced Notice line 1: seated upright, hands folded)."""
    d = seat.desk
    y = d.surface(seat.bob)
    arms = {s: arm_rest((13.0, y, d.front + 125.0), y, 'fist') for s in 'LR'}
    return _spec(lean=7.0, arms=arms)


def spec_lean_in(sp, seat):
    """Elbows on the desk, forearms up, hands together in front of the chin: interested, or scheming."""
    d = seat.desk
    y = d.surface(seat.bob)
    lean = 18.0
    arms = {}
    for s in 'LR':
        arms[s] = dict(arm_free((10.0, y - 150.0, d.front + 70.0), (0.9, 0.9, -0.1), 'fist'), elbow_rest=y - SLEEVE)
    return _spec(lean=lean, arms=arms)


def spec_lean_back(sp, seat, hands='head', amount=18.0):
    """Leaning back, the chair reclined with him: hands cupping the back of the head, elbows wide (smug, in charge),
    or 'belly' (fingers laced on the stomach: content)."""
    arms = {}
    if hands == 'head':
        for s in 'LR':
            hb = V.leaned((86.0, -148.0, -30.0), -amount)     # the back of the head's sides, the head leaned with him
            arms[s] = arm_free(hb, (1.0, -0.5, -0.4), 'palm')
        tucked = 'hands behind the head: the fingers show at the sides of the head'
    else:
        for s in 'LR':
            arms[s] = arm_free(V.leaned((16.0, 360.0, 105.0), -amount), (0.7, 0.8, -0.2), 'fist')
        tucked = None
    return _spec(lean=-amount, arms=arms, tucked=tucked,
                 feet={'L': (-70, 275.0), 'R': (70, 275.0)})


def spec_armrests(sp, seat):
    """Back in an armchair, forearms along the armrests, hands over their ends."""
    y = seat.surface() - seat.arms
    arms = {s: arm_rest((seat.width + 26.0, y, seat.front - 35.0), y, 'palm') for s in 'LR'}
    return _spec(lean=-17.0, arms=arms, feet={'L': (-74, 285.0), 'R': (74, 285.0)})


POSES = {
    'upright': (lambda sp, seat: spec_upright(sp, seat), 'office'),
    'hands folded': (spec_hands_folded, 'office+desk'),
    'lean in': (spec_lean_in, 'office+desk'),
    'lean back': (lambda sp, seat: spec_lean_back(sp, seat, 'head'), 'office'),
    'lean back, belly': (lambda sp, seat: spec_lean_back(sp, seat, 'belly', 14.0), 'office'),
    'armchair': (spec_armrests, 'armchair'),
    'stool': (lambda sp, seat: spec_upright(sp, seat), 'stool'),
}


def seat_for(where):
    kind, _, desk = where.partition('+')
    return Seat(kind, desk=Desk() if desk else None)


def pose(sp, name, seat=None, **kw):
    build, where = POSES[name]
    seat = seat or seat_for(where)
    return realize(sp, seat, build(sp, seat, **kw))


# ------------------------------------------------------------------------------------------------ moves
def _standing_spec(sp, seat, tuck_z):
    sw = sp.get('shoulders', 150)
    arms = {s: arm_free((sw + 24.0, 466.0, 44.0), (0.25, 0.3, -1.0), 'fist') for s in 'LR'}
    return _spec(lift=1.0, dz=tuck_z - 6.0, arms=arms, feet={'L': (-60, tuck_z), 'R': (60, tuck_z)})


def stand_up(sp, seat, u, kind='normal', start=None):
    """Rising from the seat, u 0-1 over DUR['stand_up'] (1.1 s; 'quick' 0.7 s, 'weary' 1.8 s). The feet step back
    under the seat edge first (so little lean is needed: Janssen 2002), the hips leave the seat as the trunk tips
    forward (never a lean and sink first: Sam, Islamocommunism note 10; rule 80), the body travels forward over the
    feet, the legs straighten, a small settle."""
    sit = start or spec_upright(sp, seat)
    tuck = 150.0
    st = _standing_spec(sp, seat, tuck)
    peak = {'normal': 20.0, 'quick': 24.0, 'weary': 26.0}[kind]
    feet0 = sit['feet'] or {'L': (-64, 235.0), 'R': (64, 235.0)}
    win = {'R': (0.0, 0.14), 'L': (0.05, 0.19)}          # each foot steps back in turn, lifted as it moves
    feet = {s: vlerp(feet0[s], (feet0[s][0], tuck), seg(u, *win[s])) for s in 'LR'}
    step = {s: 18.0 * math.sin(math.pi * min(1.0, max(0.0, (u - win[s][0]) / (win[s][1] - win[s][0])))) for s in 'LR'}
    lift = seg(u, 0.19, 0.86)
    lean = peak * seg(u, 0.06, 0.34) * (1 - seg(u, 0.4, 0.88)) - 2.0 * math.sin(math.pi * seg(u, 0.84, 1.0))
    arms_k = seg(u, 0.12, 0.9)
    s = mix(sit, st, arms_k)
    s.update(lift=lift, lean=lean, dz=st['dz'] * seg(u, 0.16, 0.8), feet=feet, foot_up=step, recline=0.0,
             tucked=None)
    s['dip'] = 0.0
    return _no_sink(sp, seat, s, sit)


def _no_sink(sp, seat, s, sit, tol=4.0):
    """Lift the hips just enough that the head stays at or above its seated height front on (rule 80): the body
    rises into the lean instead of sinking into it."""
    seated = head_y(dict(bob=seat.bob, lean=sit['lean'], dz=0.0))
    for _ in range(3):
        j = dict(bob=seat.bob * (1 - s['lift']) + s.get('dip', 0.0), lean=s['lean'], dz=s['dz'])
        over = head_y(j) - seated - tol
        if over <= 0:
            break
        s['lift'] = min(1.0, s['lift'] + over / seat.bob)
    return s


def sit_down(sp, seat, u, kind='normal', end=None):
    """Sitting down, u 0-1 over DUR['sit_down'] (1.3 s; 'plonk' 0.55 s, tired; 'careful' 2 s). The bottom leads back
    and down, the trunk tips forward to balance and comes up again before the seat (the head never drops below its
    seated height: rule 80), the descent slows just above the seat (a controlled landing; Jeon 2024), lands, the
    cushion gives and settles, the feet slide forward to rest."""
    tuck = 150.0
    st = _standing_spec(sp, seat, tuck)
    sit = end or spec_upright(sp, seat)
    feet1 = sit['feet'] or {'L': (-64, 235.0), 'R': (64, 235.0)}
    if kind == 'plonk':
        fall = min(1.0, max(0.0, (u - 0.08) / 0.6)) ** 1.6       # gives way: accelerates down, hard landing
        land = 0.68
        lean = 14.0 * math.sin(math.pi * min(1.0, u / 0.68)) - 6.0 * math.sin(math.pi * seg(u, 0.68, 1.0))
        dip = 12.0 * math.sin(math.pi * seg(u, 0.68, 0.9))
    else:
        fall = seg(u, 0.1, 0.82)
        land = 0.82
        lean = 18.0 * seg(u, 0.08, 0.4) * (1 - seg(u, 0.45, 0.8)) - 2.5 * math.sin(math.pi * seg(u, 0.82, 1.0))
        dip = 5.0 * math.sin(math.pi * seg(u, 0.82, 0.96))
    lift = 1.0 - fall
    dz = st['dz'] * (1 - seg(u, 0.1, land - 0.08))
    k_feet = seg(u, land, 1.0)
    feet = {s: vlerp((feet1[s][0], tuck), feet1[s], k_feet) for s in 'LR'}
    s = mix(st, sit, seg(u, 0.1, land))
    s.update(lift=lift, lean=lean, dz=dz, feet=feet, foot_up=None, dip=dip, tucked=None)
    if lift > 0:
        s = _no_sink(sp, seat, s, sit)
    return s


def lean_back_move(sp, seat, u, hands='head'):
    """Upright to leaning back (0.6 s): the shoulders go first, the chair gives, a small rock as it settles; the hands
    travel up and out to the head (out to the side on the way, never through the shoulder)."""
    a, b = spec_upright(sp, seat), spec_lean_back(sp, seat, hands)
    s = mix(a, b, seg(u, 0.0, 0.7))
    s['lean'] = b['lean'] * seg(u, 0.0, 0.62) - 3.0 * math.sin(math.pi * seg(u, 0.62, 1.0))
    if hands == 'head':
        k = seg(u, 0.0, 0.7)
        for side in 'LR':
            h = s['arms'][side]['hand']
            s['arms'][side] = dict(s['arms'][side], hand=(h[0] + 90 * math.sin(math.pi * k), h[1], h[2]))
    s['tucked'] = b['tucked'] if u > 0.6 else None
    return s


def idle(spec, t, seed=0, talking=False):
    """The moving hold (figure-rig s.6): breathing as a lean (rule 64), a small shift of weight every 4-8 s, hands
    easing a few units. Never a frozen statue."""
    rnd = random.Random(seed)
    s = dict(spec)
    s['arms'] = {k: dict(v) for k, v in spec['arms'].items()}
    s['lean'] = spec['lean'] + 0.7 * math.sin(2 * math.pi * (t / 4.0 + rnd.random()))
    tt, shift, last = 0.0, 0.0, 0.0
    while tt < t:
        gap = rnd.uniform(4.0, 8.0)
        nxt = rnd.uniform(-1.6, 1.6)
        if tt + gap > t:
            break
        last, shift, tt = shift, nxt, tt + gap
    k = seg(t - tt, 0.0, 0.6)
    s['lean'] += lerp(last, shift, k)
    for side, a in s['arms'].items():
        if a and a.get('rest') is None:
            h = a['hand']
            s['arms'][side]['hand'] = (h[0], h[1] + 3 * math.sin(2 * math.pi * (t / 5.3 + rnd.random())), h[2])
    return s


def gesture(sp, seat, name, beat, base=None, t=0.0, seed=0, amount=1.0):
    """A talking gesture from the seat: any moves.pose gesture's raised arms on top of a seated pose; a hand the
    gesture leaves low stays resting where the seated pose had it. `amount` 0-1 eases the arm from its rest into the
    gesture and back (about 0.3 s each way: never a jump). The blend never lengthens a bone."""
    import moves
    base = base or spec_upright(sp, seat)
    j = realize(sp, seat, idle(base, t, seed))
    g = moves.pose(sp, name, beat)
    k = ease(amount)
    lean = j['lean']
    desk = seat.desk
    for s in 'LR':
        wy, wz = g['wr' + s][1], g['wr' + s][2]
        if wy >= 400 or (wy > 250 and wz < 60):      # this hand stays down (or goes to the hip): it keeps resting
            continue
        sg = -1 if s == 'L' else 1
        shape = g['hand'].get(s, 'fist') if k > 0.5 else j['hand'].get(s, 'fist')
        d = V._unit(V._sub(g['wr' + s], g['el' + s]))
        want = V.leaned(V._add(g['wr' + s], V._mul(d, F.HAND.get(shape, 14))), lean)   # the gesture's hand, seated
        if desk is not None and want[2] > desk.front - 40:                           # over the desk: keep it above
            want = (want[0], min(want[1], desk.surface(seat.bob) - 55.0), want[2])
        d0 = V._unit(V._sub(j['wr' + s], j['el' + s]))
        have = V.leaned(V._add(j['wr' + s], V._mul(d0, F.HAND.get(j['hand'].get(s, 'fist'), 14))), lean)
        target = V.leaned(vlerp(have, want, k), -lean)
        pole_g = V._sub(g['el' + s], vlerp(j['sh' + s], g['wr' + s], 0.5))
        pole_r = V._sub(j['el' + s], vlerp(j['sh' + s], j['wr' + s], 0.5))
        pole = vlerp(pole_r, pole_g, k)
        V.arm_to(j, s, target, (pole[0] * sg, pole[1], pole[2]), shape)
        rest = base['arms'].get(s)
        if rest and k > 0:                            # lifted off the desk: no longer resting
            j['spec'] = dict(j['spec'], arms=dict(j['spec']['arms'], **{s: dict(rest, rest=None, elbow_rest=None)}))
    if k > 0.5:
        j['props'] = j.get('props', []) + g.get('props', [])
        for key in ('on_face', 'tucked'):             # a hand on the face is drawn over it (views); hidden on purpose
            if g.get(key):
                j[key] = g[key]
    return j


def acting_demo(sp, seat, base, t, beats, seed=3):
    """A run of seated gestures [(start, name, length)] over the moving hold (for the test clip and as a pattern)."""
    for t0, name, length in beats:
        if t0 <= t < t0 + length:
            u = (t - t0) / length
            amount = min(1.0, u / 0.25, (1 - u) / 0.25)
            return gesture(sp, seat, name, math.sin(math.pi * u), base, t, seed, amount)
    return realize(sp, seat, idle(base, t, seed))


# ------------------------------------------------------------------------------------------------ checks
def head_y(j):
    """Where the head's centre lands on screen, front on (person units, the whole body's drop included)."""
    n = V.leaned((0.0, -150.0, 0.0), j.get('lean', 0.0))
    return j.get('bob', 0.0) + n[1] + V.ELEV * (n[2] + j.get('dz', 0.0))


def check_frame(j, t=0.0, where='someone seated'):
    """Faults in one drawing, in plain words."""
    out = [f'{where} at {t:.2f} s: {f}' for f in j.get('_faults', [])]
    seat, spec = j['seat'], j['spec']
    floor = FLOOR - j['bob']
    off = V.HIP_Y + SIT + j['bob'] - spec.get('dip', 0.0) - (FLOOR - seat.h + seat.cushion)
    if j['lift'] == 0 and abs(off) > 3:                 # (a landing's settle, `dip`, is the cushion giving)
        out.append(f'{where} at {t:.2f} s: hips {off:+.0f} off the seat')
    if spec.get('dip', 0.0) > 14:
        out.append(f'{where} at {t:.2f} s: the seat gives {spec["dip"]:.0f}: too soft')
    up = spec.get('foot_up') or {}
    for s in 'LR':
        hip, foot = j['hip' + s], j['foot' + s]
        if up.get(s, 0) < 1 and abs(foot[1] + ANKLE_UP - floor) > 3:
            out.append(f'{where} at {t:.2f} s: {s} foot {foot[1] + ANKLE_UP - floor:+.0f} off the floor')
        sg = -1 if s == 'L' else 1
        knee, end = V.ik3(hip, foot, V.THIGH, V.SHIN, j.get('knee_pole' + s, (0.12 * sg, 0.0, 1.0)))
        gap = math.dist(end, foot)
        if gap > 4:
            out.append(f'{where} at {t:.2f} s: {s} leg {gap:.0f} short of the foot (it would stretch: move the feet or seat)')
        a, b = V._sub(hip, knee), V._sub(foot, knee)
        cosang = V._dot(a, b) / ((math.sqrt(V._dot(a, a)) * math.sqrt(V._dot(b, b))) or 1)
        if math.degrees(math.acos(max(-1, min(1, cosang)))) < 35:
            out.append(f'{where} at {t:.2f} s: {s} knee folded tighter than 35 degrees')
        mid = vlerp(hip, foot, 0.5)
        if knee[2] < mid[2] - 4:
            out.append(f'{where} at {t:.2f} s: {s} knee bends backwards')
        a = spec['arms'].get(s)
        if a and a.get('rest') is not None:
            lean = j['lean']
            for joint in ('el', 'wr'):
                y = V.leaned(j[joint + s], lean)[1]
                if abs(y - a['rest']) > 6:
                    out.append(f'{where} at {t:.2f} s: {s} {"elbow" if joint == "el" else "wrist"} '
                               f'{y - a["rest"]:+.0f} off its resting surface (rule 78: never sinks, never floats)')
        if a and a.get('elbow_rest') is not None:
            y = V.leaned(j['el' + s], j['lean'])[1]
            if abs(y - a['elbow_rest']) > 6:
                out.append(f'{where} at {t:.2f} s: {s} elbow {y - a["elbow_rest"]:+.0f} off the desk (rule 78)')
    rec = j.get('_recline')
    if rec is not None and j['lean'] < -1 and j['lift'] < 0.05 and abs(rec + j['lean']) > 1:
        out.append(f'{where} at {t:.2f} s: the chair back does not follow the lean')
    return out


def check_no_sink(frames, seated_head, tol=8.0, where='rising or sitting'):
    """Rule 80: front on, the head never drops below its seated height."""
    worst = max(frames, key=lambda f: head_y(f[1]))
    d = head_y(worst[1]) - seated_head
    return [] if d <= tol else [f'{where}: the head dips {d:.0f} below its seated height at {worst[0]:.2f} s (rule 80)']


def check_balance(frames, where='rising'):
    """The hips are a third of the way up only once the neck is over the feet (side on: no rising on air)."""
    for t, j in frames:
        if 0.33 < j['lift'] < 0.9:
            neck_z = V.leaned((0.0, 0.0, 0.0), j['lean'])[2] + j['dz']
            feet_z = (j['footL'][2] + j['footR'][2]) / 2 + j['dz']
            if neck_z < feet_z - 30:
                return [f'{where} at {t:.2f} s: hips up but the neck {feet_z - neck_z:.0f} behind the feet (off balance)']
    return []


def check_feet_planted(frames, where='rising or sitting'):
    """A foot on the floor stays put (no sliding) unless it is stepping (lifted)."""
    out = []
    for s in 'LR':
        prev = None
        for t, j in frames:
            up = (j['spec'].get('foot_up') or {}).get(s, 0.0)
            z = j['foot' + s][2] + j['dz']
            if prev is not None and up < 1 and prev[1] < 1 and abs(z - prev[0]) > 6 and j['lift'] > 0:
                if True:                      # seated, the feet carry no weight: sliding them is fine
                    out.append(f'{where} at {t:.2f} s: {s} foot slides {z - prev[0]:+.0f} while planted')
            prev = (z, up)
    return out


def frames_of(fn, dur):
    n = int(round(dur * FPS))
    return [(k / FPS, fn(k / n)) for k in range(n + 1)]


def audit(sp=None):
    """Every pose and move in the kit, checked. Returns the faults (empty = clean)."""
    import posegallery as G
    sp = sp or G.MODEL
    out = []
    for name in POSES:
        out += check_frame(pose(sp, name), 0.0, f'pose "{name}"')
    seat = Seat('office')
    seated_head = head_y(realize(sp, seat, spec_upright(sp, seat)))
    moves = [('stand up', lambda u: stand_up(sp, seat, u), DUR['stand_up']),
             ('stand up quick', lambda u: stand_up(sp, seat, u, 'quick'), DUR['stand_up_quick']),
             ('stand up weary', lambda u: stand_up(sp, seat, u, 'weary'), DUR['stand_up_weary']),
             ('sit down', lambda u: sit_down(sp, seat, u), DUR['sit_down']),
             ('plonk', lambda u: sit_down(sp, seat, u, 'plonk'), DUR['plonk']),
             ('lean back', lambda u: lean_back_move(sp, seat, u), DUR['lean_back'])]
    for name, fn, dur in moves:
        fr = [(t, realize(sp, seat, s)) for t, s in frames_of(fn, dur)]
        for t, j in fr:
            out += check_frame(j, t, name)
        if name != 'lean back':                      # rule 80 is about rising and sitting
            out += check_no_sink(fr, seated_head, where=name)
        if name.startswith('stand'):
            out += check_balance(fr, name)
        out += check_feet_planted(fr, name)
    return out


# ------------------------------------------------------------------------------------------------ sheet and clips
def _setup():
    import burnham as B
    import handcheck as H
    import kitchecks
    import limbs
    from satire_style import install_circle_hands
    B.SS = 1
    F.guard(B)
    F._ALLOW.append('the sitting kit')
    install_circle_hands(B)
    limbs.install(B)
    kitchecks.install()
    H.install()
    return B, H


def draw_one(B, H, sp, j, deg, t=0.0, size=(600, 900), at=(300, 200), s=0.62, check=True):
    from PIL import Image
    im = Image.new('RGBA', size, (226, 222, 214, 255))
    if check:
        H.begin()
    V.person(im, B.Cam(1.0, 540, 960), at[0], at[1], s, sp, t, float(deg), j)
    faults = H.end(t, 'sitting') if check else []
    return im, faults


AVOID = {   # views where a hand is hidden (rule 41): a film never shows the pose from there
    'upright': {'behind': 'hands in his lap, hidden by his back'},
    'hands folded': {'three-quarter': 'the far hand hidden by his body', 'behind': 'both hands beyond his back'},
    'lean in': {'three-quarter': 'the far hand hidden by his body'},
    'lean back, belly': {'three-quarter': 'the far hand hidden by his body', 'behind': 'hands on his stomach'},
    'armchair': {'behind': 'the chair back hides his hands'},
    'stool': {'behind': 'hands in his lap, hidden by his back'},
}
REFS = {   # each pose beside its photos (rule 76); paths from the project root
    'upright': ['references/newsdesk/presenter-1.jpg'],
    'hands folded': ['references/traitors/06-players-across-table.jpg'],
    'lean in': ['references/traitors/09-seated-close-hands.jpg', 'references/body-weight/leaning-on-table-forearm-forward.jpg'],
    'armchair': ['references/sitting/oval-office-armchairs-sofas.jpg'],
}


def refsheet(out):
    """Each pose front on (the armchair three-quarter, as in its photo) beside its reference photos (rule 76)."""
    from PIL import Image, ImageDraw, ImageFont
    import posegallery as G
    B, H = _setup()
    sp = G.MODEL
    root = os.path.dirname(HERE)
    font = ImageFont.truetype(B.SANS, 22)
    rows = list(REFS)
    rh = 250
    img = Image.new('RGB', (1080, 44 + rh * len(rows)), (16, 16, 20))
    d = ImageDraw.Draw(img)
    d.text((10, 10), 'Ours (left) beside the photos (rule 76)', font=font, fill=(255, 255, 255))
    for r, name in enumerate(rows):
        y = 44 + r * rh
        im, _ = draw_one(B, H, sp, pose(sp, name), 45 if name == 'armchair' else 0, at=(300, 230), check=False)
        img.paste(im.convert('RGB').crop((60, 80, 540, 800)).resize((166, rh - 10)), (0, y))
        x = 176
        for f in REFS[name]:
            ph = Image.open(os.path.join(root, f)).convert('RGB')
            ph.thumbnail((440, rh - 10))
            img.paste(ph, (x, y))
            x += ph.width + 8
        d.text((4, y + 2), name, font=ImageFont.truetype(B.SANS, 16), fill=(20, 20, 20))
    img.save(out, quality=85)
    print('reference sheet:', out)


def sheet(out):
    """Every pose from the five views, the hand check (rule 41) and the kit's checks under each."""
    from PIL import Image, ImageDraw, ImageFont
    import posegallery as G
    B, H = _setup()
    sp = G.MODEL
    font, small = ImageFont.truetype(B.SANS, 22), ImageFont.truetype(B.SANS, 16)
    views = G.VIEWS
    tw, th = 180, 270
    names = list(POSES)
    img = Image.new('RGB', (170 + tw * len(views), (th + 50) * len(names) + 50), (16, 16, 20))
    d = ImageDraw.Draw(img)
    d.text((10, 12), 'Sitting kit, part 1: every pose, five views, checked',
           font=font, fill=(255, 255, 255))
    bad = 0
    for r, name in enumerate(names):
        y = 50 + r * (th + 50)
        d.text((10, y + 10), name, font=font, fill=(255, 255, 255))
        d.text((10, y + 40), POSES[name][1], font=small, fill=(170, 170, 170))
        j = pose(sp, name)
        kit = check_frame(j, 0.0, name)
        for c, (deg, label) in enumerate(views):
            im, fs = draw_one(B, H, sp, pose(sp, name), deg, at=(300, 230))
            img.paste(im.convert('RGB').crop((40, 60, 560, 840)).resize((tw, th)), (170 + c * tw, y))
            avoid = AVOID.get(name, {}).get(label)
            msg = 'OK' if not fs and not kit else ('avoid: hand hidden' if avoid and not kit else
                                                   '; '.join([f['kind'] for f in fs] + (['kit'] if kit else [])))
            d.text((174 + c * tw, y + th + 2), label, font=small, fill=(200, 200, 200))
            d.text((174 + c * tw, y + th + 22), msg[:26], font=small,
                   fill=(140, 230, 140) if msg == 'OK' else (200, 200, 120) if msg.startswith('avoid') else (255, 160, 110))
            bad += bool(fs) and not avoid
        for f in kit:
            print('  ', f)
    img.save(out, quality=85)
    print('sheet:', out, '| hand faults not in AVOID:', bad)


def clip(out, fn, dur, views=(0, 90), hold=0.4, small=True, label=''):
    """A short clip of one move, front and side by side (12 drawings a second), held a moment at each end."""
    import subprocess
    import tempfile
    from PIL import Image, ImageDraw, ImageFont
    import posegallery as G
    B, H = _setup()
    sp = G.MODEL
    tmp = tempfile.mkdtemp()
    n = int(round(dur * FPS))
    seq = [0.0] * int(hold * FPS) + [k / n for k in range(n + 1)] + [1.0] * int(hold * FPS)
    font = ImageFont.truetype(B.SANS, 22)
    for i, u in enumerate(seq):
        frame = Image.new('RGB', (540 * len(views), 760), (226, 222, 214))
        for c, deg in enumerate(views):
            j = fn(u)
            im, _ = draw_one(B, H, sp, j, deg, i / FPS, size=(540, 760), at=(270, 190), s=0.55, check=False)
            frame.paste(im.convert('RGB'), (540 * c, 0))
        ImageDraw.Draw(frame).text((14, 10), label, font=font, fill=(40, 40, 40))
        frame.save(os.path.join(tmp, f'{i:04d}.png'))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.png'),
                    '-vf', 'scale=iw/2*2:ih/2*2' if not small else 'scale=iw*0.75:-2', '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', '-crf', '26', out], check=True)
    print('clip:', out)


def clips(outdir):
    import posegallery as G
    sp = G.MODEL
    os.makedirs(outdir, exist_ok=True)
    seat, dseat = Seat('office'), Seat('office', desk=Desk())
    R = lambda s: realize(sp, seat, s)   # noqa: E731
    clip(os.path.join(outdir, 'sit-stand-up.mp4'), lambda u: R(stand_up(sp, seat, u)), DUR['stand_up'],
         label='stand up (1.1 s)')
    clip(os.path.join(outdir, 'sit-sit-down.mp4'), lambda u: R(sit_down(sp, seat, u)), DUR['sit_down'],
         label='sit down (1.3 s)')
    clip(os.path.join(outdir, 'sit-plonk.mp4'), lambda u: R(sit_down(sp, seat, u, 'plonk')), DUR['plonk'],
         label='plonk (0.55 s)')
    clip(os.path.join(outdir, 'sit-lean-back.mp4'), lambda u: R(lean_back_move(sp, seat, u)), DUR['lean_back'],
         label='lean back (0.6 s)')
    base = spec_hands_folded(sp, dseat)
    beats = [(0.8, 'point', 1.3), (2.4, 'chop', 1.0), (3.6, 'shrug', 1.1)]
    clip(os.path.join(outdir, 'sit-acting.mp4'), lambda u: acting_demo(sp, dseat, base, u * 5.0, beats), 5.0,
         hold=0.0, label='seated acting: point, chop, shrug (5 s)')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        sheet(a[1])
    elif a and a[0] == 'refs':
        refsheet(a[1])
    elif a and a[0] == 'clips':
        clips(a[1])
    elif a and a[0] == 'audit':
        fs = audit()
        print('\n'.join(fs) or 'sitting kit: clean')
        sys.exit(1 if fs else 0)
    else:
        print(__doc__)
