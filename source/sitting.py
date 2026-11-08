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
- PART 2 (8 Nov): legs placed by their ankles (spec 'ankle', 'on' = what each foot rests on). POSES add cross, knee
  over knee; cross, ankle on knee; feet up; perch, chair edge; perch, desk corner (Seat('desk')); slump. MOVES add
  cross_legs (and uncross: u played backwards), feet_up_move, feet_down_move ('snap'), scoot_to_perch, slump_move
  ('collapse'), swivel (draw him at spec['yaw'], head at spec['head_yaw']; the desk stays put). part2_moves() lists them.
- CHECKS: check_frame (hips on the seat, feet on their surface, legs reach and bend the right way, resting arms on
  their surface, the chair follows the lean) with check_legs (nothing through the seat, desk or other leg) and
  check_back (back on, or clear of, the chair back); check_no_sink (rule 80), check_balance, check_desk_still; run
  over every pose and move by audit().
- python3 source/sitting.py sheet OUT.jpg [2] | refs OUT.jpg [2] | clips OUT_DIR | clips2 OUT.mp4 | audit

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
PERCH_SIT = 30.0             # perched on a desk, the hip joint this far above its top (a thigh lying on it)
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
def _box(p, yaw, x0, x1, y0, y1, z0, z1, col, top=None, tilt=0.0, shift=0.0, xf=None):
    """A box in the body's frame (x across, y down, z forward), tipped back `tilt` degrees about the hips (a
    reclined chair back) and moved `shift` along z (the body's own forward travel, undone); or placed by `xf` (a
    desk turned in the room: Desk.xf). Drawn as its outline, then its top face lighter (the camera is a little
    above)."""
    def P(x, y, z):
        if xf:
            return V.project(xf(x, y, z), yaw)[0]
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
        'office': dict(h=260, front=130, rear=-125, width=125, back_top=300, back_z=-78, arms=None, cushion=0, swivel=True,
                       col=(58, 60, 68), top=(84, 86, 96)),
        'armchair': dict(h=190, front=165, rear=-160, width=150, back_top=330, back_z=-86, arms=205, cushion=22, swivel=False,
                         col=(122, 58, 52), top=(150, 76, 68)),
        'stool': dict(h=270, front=95, rear=-95, width=105, back_top=None, arms=None, cushion=0, swivel=False,
                      col=(128, 96, 64), top=(160, 124, 86)),
        # perched on a desk's corner (part 2): he stands beside the desk's front end, his left thigh up along its
        # top, the knee over its end and the shin hanging in front of it; the right leg stands. The desk runs away
        # from him on his left (its side at side_x).
        'desk': dict(h=500, front=200, rear=-680, width=440, back_top=None, arms=None, cushion=0, swivel=False,
                     col=(122, 88, 58), top=(150, 112, 76), side_x=-20.0),
    }

    def __init__(self, kind='office', desk=None, **kw):
        self.kind = kind
        for k, v in dict(self.KINDS[kind], **kw).items():
            setattr(self, k, v)
        self.desk = desk
        if kind == 'desk':                      # the desk itself, turned end-on to him
            self.as_desk = Desk(h=self.h, front=-self.side_x, turn=-90.0, z=self.front - 440.0)

    def on_top(self, x, z):
        """Is a hip at (x, z) (chair frame) over the seat's top?"""
        x0 = -self.width if self.kind != 'desk' else self.side_x - 430
        x1 = self.width if self.kind != 'desk' else self.side_x
        return x0 - 4 <= x <= x1 + 4 and self.rear - 4 <= z <= self.front + 4

    @property
    def bob(self):
        """How far the body drops to sit (person units): the hips on the seat. Perched on a desk he stands: the
        thigh on the desk lifts its own hip instead (desk_hip_dy)."""
        if self.kind == 'desk':
            return 0.0
        return FLOOR - self.h - (V.HIP_Y + SIT) + self.cushion

    def desk_hip_dy(self):
        return FLOOR - self.h - PERCH_SIT - V.HIP_Y

    def surface(self):
        """The seat's top in the body frame of a seated person."""
        return V.HIP_Y + SIT - self.cushion

    def draw(self, p, view, j, layer):
        if self.kind == 'desk':
            return self.as_desk.draw(p, view, j, layer, seat_frame=True)
        yaw = j2yaw(view)
        bob, dz, lean = j.get('bob', 0.0), j.get('dz', 0.0) - j.get('roll', 0.0), j.get('lean', 0.0)
        sh = -dz                                         # the seat stays put while the body travels (it rolls with him)
        floor = FLOOR - bob
        top = floor - self.h                             # the seat's top, wherever the body is
        recline = recline_of(j)                          # the back gives with a lean back ('give': how much)
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
    for real bodies); a modesty panel on the far side and a panel at each end. `turn` (degrees) and `x` place it
    otherwise in the room (a desk behind someone perched on it). It stays put in the room: the body's travel is
    undone, and when someone swivels (j['swivel'], the yaw he is drawn at, the desk facing 0) it turns the other way
    in his frame, so on screen it never moves."""
    def __init__(self, h=500, front=125, depth=430, width=440, col=(122, 88, 58), top=(150, 112, 76), turn=0.0, x=0.0,
                 z=0.0):
        self.h, self.front, self.depth, self.width, self.col, self.top_col = h, front, depth, width, col, top
        self.turn, self.x, self.z = turn, x, z

    def surface(self, bob):
        return FLOOR - self.h - bob

    def boxes(self, bob):
        """The desk's solid parts in its own frame (body-frame heights): (x0, x1, y0, y1, z0, z1, has top)."""
        floor, top = FLOOR - bob, FLOOR - self.h - bob
        w, z0, z1 = self.width, self.front, self.front + self.depth
        return [(-w + 20, w - 20, top + 30, floor - 60, z1 - 30, z1 - 14, False),    # modesty panel
                (-w, -w + 36, top + 20, floor, z0 + 10, z1, True),                     # the end panels
                (w - 36, w, top + 20, floor, z0 + 10, z1, True),
                (-w, w, top, top + 26, z0, z1, True)]                                  # the top

    def xf(self, j, seat_frame=False):
        """The desk's frame to the person's body frame (and its inverse): turned, placed, the swivel undone, the
        body's travel undone."""
        sw = None if seat_frame else j.get('swivel')
        deg, mir = V.snap(sw) if sw is not None else (0, False)
        sg = -deg if mir else deg
        shift = -(j.get('dz', 0.0) - j.get('roll', 0.0)) if seat_frame else -j.get('dz', 0.0)
        t, b = math.radians(self.turn), math.radians(-sg)
        ct, st, cb, sb = math.cos(t), math.sin(t), math.cos(b), math.sin(b)

        def T(x, y, z):
            x, z = x * ct + z * st, -x * st + z * ct
            x, z = x + self.x, z + self.z
            x, z = x * cb + z * sb, -x * sb + z * cb
            return (-x if mir else x, y, z + shift)

        def inv(x, y, z):
            z -= shift
            x = -x if mir else x
            x, z = x * cb - z * sb, x * sb + z * cb
            x, z = x - self.x, z - self.z
            return (x * ct - z * st, y, x * st + z * ct)
        return T, inv

    def draw(self, p, view, j, layer, seat_frame=False):
        yaw = j2yaw(view)
        T, _ = self.xf(j, seat_frame)
        parts = []
        for x0, x1, y0, y1, z0, z1, has_top in self.boxes(j.get('bob', 0.0)):
            d = V.project(T((x0 + x1) / 2, y0, (z0 + z1) / 2), yaw)[1]
            parts.append((d, lambda p, b=(x0, x1, y0, y1, z0, z1, has_top): _box(
                p, yaw, *b[:6], self.col, self.top_col if b[6] else None, xf=T)))
        for d, fn in sorted(parts, key=lambda q: q[0]):
            if ('mid' if d > -40 else 'pre') == layer:
                fn(p)


def recline_of(j):
    """How far the chair back is reclined: the lean back times `give` (1: the back follows the trunk; a slump's
    back gives less than the trunk leans), never while rising."""
    if j.get('lift', 0.0) >= 0.05:
        return 0.0
    return max(0.0, -j.get('lean', 0.0)) * j.get('give', 1.0)


def j2yaw(view):
    return {'front': 0, 'three': 45, 'side': 90, 'three_back': 135, 'back': 180}[view]


# ------------------------------------------------------------------------------------------------ specs
def _spec(**kw):
    s = dict(lean=0.0, lift=0.0, dz=0.0, head_dy=0.0, feet=None, foot_up=None, arms={}, recline=0.0)
    s.update(kw)
    return s


# Part 2: per-leg keys. 'ankle' {side: (x, height above the floor, z in the chair's frame)} puts an ankle anywhere
# (on a desk, on the other knee, dangling); 'on' {side: 'floor' | 'desk' | 'knee' | 'leg' | 'air'} says what the
# foot rests on (the checks test it); 'knee_pole', 'toe', 'foot_yaw', 'foot_roll', 'hip_dy' as in views.
SIDED = ('ankle', 'knee_pole', 'toe', 'foot_yaw', 'foot_roll', 'hip_dy')
SIDED_FLAGS = ('sole', 'on')


def _default_sided(spec, key, s):
    sg = -1 if s == 'L' else 1
    if key == 'ankle':
        fx, fz = (spec.get('feet') or {'L': (-64, 235.0), 'R': (64, 235.0)})[s]
        return (fx, ANKLE_UP + (spec.get('foot_up') or {}).get(s, 0.0), fz)
    if key == 'knee_pole':
        k = ease(min(1.0, spec.get('lift', 0.0) / 0.85))
        return (sg * lerp(0.1, 0.12, k), lerp(-1.0, 0.0, k), lerp(0.7, 1.0, k))
    return 0.0


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
        elif key in SIDED:
            if not x and not y:
                out[key] = x or y
                continue
            out[key] = {}
            for s in 'LR':
                xa = (x or {}).get(s, _default_sided(a, key, s))
                ya = (y or {}).get(s, _default_sided(b, key, s))
                out[key][s] = vlerp(xa, ya, k) if isinstance(xa, tuple) else lerp(xa, ya, k)
        elif key in SIDED_FLAGS:
            out[key] = {s: ((x or {}) if k < 0.5 else (y or {})).get(s) for s in 'LR'}
        elif key in ('feet', 'foot_up'):
            if x is None or y is None:
                out[key] = x if k < 0.5 else y
            else:
                out[key] = {s: (vlerp(x[s], y[s], k) if isinstance(x[s], tuple) else lerp(x[s], y[s], k)) for s in x}
        elif (x is None) != (y is None) and isinstance(x if y is None else y, (int, float)) and \
                not isinstance(x if y is None else y, bool):    # a number one spec leaves out: its resting value
            d = {'give': 1.0}.get(key, 0.0)
            out[key] = lerp(d if x is None else x, d if y is None else y, k)
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
    roll = spec.get('roll', 0.0)                 # the chair rolled back (-) or in, the body with it
    bob = seat.bob * (1 - lift) + spec.get('dip', 0.0) + spec.get('tail', 0.0)   # tail: slid down onto the tailbone
    j['bob'], j['lean'], j['dz'], j['lift'], j['roll'] = bob, lean, dz + roll, lift, roll
    j['head_dy'] = spec.get('head_dy', 0.0)
    j['head_lean'] = spec.get('head_lean', 0.0)
    j['give'] = spec.get('give', 1.0)
    j['cross'] = spec.get('cross')
    j['swivel'] = spec.get('swivel')
    floor = FLOOR - bob
    for s, sg in (('L', -1), ('R', 1)):
        dy = (spec.get('hip_dy') or {}).get(s, 0.0)
        j['hip' + s] = (j['hip' + s][0], V.HIP_Y + dy, 0.0)
        x, h, z = (spec.get('ankle') or {}).get(s) or _default_sided(spec, 'ankle', s)
        j['foot' + s] = (x, floor - h, z - dz)
        j['knee_pole' + s] = (spec.get('knee_pole') or {}).get(s) or _default_sided(spec, 'knee_pole', s)
        for key in ('toe', 'foot_yaw', 'foot_roll'):
            v = (spec.get(key) or {}).get(s)
            if v:
                j[key + s] = v
        if (spec.get('sole') or {}).get(s):
            j['sole' + s] = True
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
    j['_shoulders'] = sp.get('shoulders', 150)
    j['chair_draw'] = lambda p, view, j2, sp_, under=True: seat.draw(p, view, j, 'pre')
    j['mid'] = [lambda p, j2, view: seat.draw(p, view, j, 'mid')]
    j['pre'] = []
    if seat.desk:
        j['pre'].append(lambda p, j2, view: seat.desk.draw(p, view, j, 'pre'))
        j['mid'].append(lambda p, j2, view: seat.desk.draw(p, view, j, 'mid'))
    if spec.get('tucked'):
        j['tucked'] = spec['tucked']
    over = spec.get('legs_over') or {}
    if over == 'above the desk':                  # only what rises above the desk top shows over it (feet up)
        over = {s: _rise_above(j, s, seat.desk.surface(bob)) for s in 'LR'}
        over = {s: u for s, u in over.items() if u is not None}
        j['legs_over_views'] = ('front', 'three')    # side on, nothing of the desk is in front of them
    j['legs_over'] = over
    if seat.desk:                                # a hand below the desk top and beyond its near edge is under it
        top = seat.desk.surface(bob)
        j['arms_under'] = {s for s in 'LR' if V.leaned(j['wr' + s], lean)[1] > top + 10 and
                           V.leaned(j['wr' + s], lean)[2] < seat.desk.front - (dz + roll) + 60}
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
    return _spec(lean=-amount, arms=arms, tucked=tucked, back_on='shoulders',
                 feet={'L': (-70, 275.0), 'R': (70, 275.0)})


def spec_armrests(sp, seat):
    """Back in an armchair, forearms along the armrests, hands over their ends."""
    y = seat.surface() - seat.arms
    arms = {s: arm_rest((seat.width + 26.0, y, seat.front - 35.0), y, 'palm') for s in 'LR'}
    return _spec(lean=-17.0, arms=arms, back_on='shoulders', feet={'L': (-74, 285.0), 'R': (74, 285.0)})


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


# ------------------------------------------------------------------------------------------------ part 2 poses
THIGH_R, KNEE_R, ANKLE_R = 24.0, 19.0, 13.5       # the legs' half-widths as views.leg draws them (thigh, knee, ankle)


def knees(sp, seat, spec):
    """Where the knees land for a spec (body frame), worked out by drawing nothing."""
    j = realize(sp, seat, dict(spec, arms={}))
    return {s: tuple(V.knee_of(j, s)) for s in 'LR'}, j


def _chair(j, q):
    """A body-frame point in the chair's frame (heights above the floor; z from the seat's hip mark)."""
    return (q[0], FLOOR - j['bob'] - q[1], q[2] + j['dz'] - j['roll'])


def _leg_by_knee(hip, knee_dir, shin_dir):
    """A leg placed by where the knee goes (a direction from the hip) and where the shin hangs (a direction from
    the knee): the ankle, and the pole that makes views solve that same knee. Body frame."""
    K = V._add(hip, V._mul(V._unit(knee_dir), V.THIGH))
    A = V._add(K, V._mul(V._unit(shin_dir), V.SHIN))
    pole = V._sub(K, vlerp(hip, A, 0.5))
    return K, A, pole


def _ankle_spec(j, A):
    """A body-frame ankle as the spec's (x, height above the floor, chair z)."""
    x, h, z = _chair(j, A)
    return (x, h, z)


def spec_cross_knee(sp, seat, top='R'):
    """Knee over knee (prim, closed, careful: Pease): the thighs together, the top thigh lying on the lower one
    just behind its knee, the top calf hanging over the lower knee, its foot off the floor beside the lower shin."""
    lo = 'L' if top == 'R' else 'R'
    sl = -1 if lo == 'L' else 1                  # the lower leg's side
    base = spec_upright(sp, seat, 'lap')
    base['feet'] = {lo: (sl * 34, 238.0), top: (-sl * 64, 235.0)}
    kn, j = knees(sp, seat, base)
    KL = kn[lo]
    hip = j['hip' + top]
    want = V._add(KL, (-sl * 22.0, -(THIGH_R + THIGH_R - 6), 26.0))   # on the lower thigh, past its knee
    K, A, pole = _leg_by_knee(hip, V._sub(want, hip), (sl * 0.32, 0.86, 0.34))
    base.update(ankle={top: _ankle_spec(j, A)}, knee_pole={top: pole}, toe={top: -18.0},
                on={top: 'air', lo: 'floor'}, cross=top, contact={top: ('thigh on knee', lo)})
    base['arms'] = {s: arm_free(((K[0] + (30 if s == 'R' else -30)) * (1 if s == 'R' else -1), K[1] - 38.0, K[2] - 34.0),
                                (0.5, 0.7, -0.4), 'palm') for s in 'LR'}     # both hands on the top knee, side by side
    return base


def spec_figure_four(sp, seat, top='R'):
    """Ankle on knee, the "figure four" (cocky, dominant, at ease: Pease): the top ankle on the lower knee, the top
    knee out wide, the sole turned forward; hands on the raised shin and the lower knee, or one arm out."""
    lo = 'L' if top == 'R' else 'R'
    sl = -1 if lo == 'L' else 1
    base = spec_upright(sp, seat)
    base['feet'] = {lo: (sl * 70, 232.0), top: (-sl * 64, 235.0)}
    base['lean'] = -6.0
    kn, j = knees(sp, seat, base)
    A = V._add(kn[lo], (-sl * 4.0, -(THIGH_R + ANKLE_R) + 2, -30.0))      # the ankle on the lower thigh, behind the knee
    hip = j['hip' + top]
    # the knee out wide and up a little: the pole points away from the body's middle
    base.update(ankle={top: _ankle_spec(j, A)}, knee_pole={top: (-sl * 1.0, -0.35, 0.25)},
                toe={top: 8.0}, foot_yaw={top: sl * 78.0}, foot_roll={top: -sl * 48.0}, sole={top: True},
                on={top: 'knee', lo: 'floor'}, cross=top, contact={top: ('ankle on knee', lo)})
    jj = realize(sp, seat, base)
    Kt = V.knee_of(jj, top)
    shin_mid = vlerp(Kt, A, 0.45)
    base['arms'] = {
        top: arm_free((abs(shin_mid[0]) * (1 if top == 'R' else 1), shin_mid[1] - 30, shin_mid[2]), (0.8, 0.4, -0.5), 'palm'),
        lo: arm_free((abs(kn[lo][0]) + 4, kn[lo][1] - 34, kn[lo][2] - 8), (0.5, 0.3, -0.9), 'palm'),
    }
    return base


def spec_feet_up(sp, seat, roll=-60.0, amount=17.0):
    """Feet up on the desk (ownership, contempt: Pease): the chair pushed back a little and reclined, hands behind
    the head, both heels on the desk top, ankles crossed (the right over the left); front on we see his soles. Our
    people's legs are short for a desk this high, so the knees stay up a little and the calves clear its edge."""
    d = seat.desk
    edge = d.front - roll                                    # the desk's near edge in the chair's frame
    toe = 70.0
    sole_drop = _shoe_low((0, 0, 0), toe, sole=True)         # how far the heel sits below the ankle
    h = d.h + sole_drop
    sp_ = spec_lean_back(sp, seat, 'head', amount)
    ank = {'L': (14.0, h, edge + 118.0), 'R': (-22.0, h + 2 * ANKLE_R, edge + 104.0)}
    sp_.update(roll=roll, ankle=ank, legs_over='above the desk', toe={'L': toe, 'R': toe - 6}, sole={'L': True, 'R': True},
               knee_pole={'L': (-0.15, -1.0, -0.15), 'R': (0.15, -1.0, -0.15)},
               on={'L': 'desk', 'R': 'leg'}, cross='R', contact={'R': ('ankle on ankle', 'L')})
    j = realize(sp, seat, dict(sp_, arms={}))          # the right ankle laid on the left shin, just above its ankle
    A, K = j['footL'], tuple(V.knee_of(j, 'L'))
    on = vlerp(A, K, 0.16)
    up = V._unit(V._sub((0.0, -1.0, 0.0), V._mul(V._unit(V._sub(K, A)), V._dot((0.0, -1.0, 0.0), V._unit(V._sub(K, A))))))
    side = V._unit(V._add(up, (-0.8, 0.0, 0.0)))       # on top and a little to his right of it: crossed
    R_ = V._add(on, V._mul(side, lerp(ANKLE_R, KNEE_R, 0.16) + ANKLE_R + 1))
    sp_['ankle']['R'] = _ankle_spec(j, R_)
    return sp_


def spec_perch(sp, seat, hands='knees'):
    """Perched on the chair's front edge (eager, nervous, about to go: Navarro): the hips on the front third of the
    seat, the trunk forward, the feet drawn back, hands on the knees (or 'grip': gripping the seat's edge)."""
    dz = seat.front - (seat.front - seat.rear) / 3 + 34.0
    base = _spec(lean=14.0, dz=dz, feet={'L': (-70, dz + 150.0), 'R': (70, dz + 150.0)})
    kn, j = knees(sp, seat, base)
    if hands == 'knees':
        base['arms'] = {s: arm_free((abs(kn[s][0]) + 4, kn[s][1] - 36, kn[s][2] - 6), (0.5, 0.6, -0.6), 'palm')
                        for s in 'LR'}
    else:
        y = FLOOR - j['bob'] - seat.h
        base['arms'] = {s: arm_free((seat.width - 30.0, y - 6, seat.front - dz - 18), (0.3, 0.2, -1.0), 'fist')
                        for s in 'LR'}
    base['back_off'] = True
    base['perch'] = True
    return base


def spec_perch_desk(sp, seat):
    """Perched on a desk's corner (the casual boss, "let's chat"): standing beside the desk's front end, the left
    thigh up along its top (the hip lifts with it), the knee just past its end, the shin hanging in front of it; the
    right leg stands; the left hand flat on the desk beside him, the right hand resting on the raised knee."""
    hy = seat.desk_hip_dy()
    base = _spec(lean=-3.0, hip_dy={'L': hy})
    hipL = (-55.0, V.HIP_Y + hy, 0.0)
    K, A, pole = _leg_by_knee(hipL, (-0.04, 0.0, 1.0), (-0.02, 0.98, 0.16))
    j0 = realize(sp, seat, base)
    base.update(ankle={'L': _ankle_spec(j0, A), 'R': (88.0, ANKLE_UP, 34.0)}, knee_pole={'L': pole},
                toe={'L': -24.0}, on={'R': 'floor', 'L': 'air'}, legs_over={'L': 0.3})
    y = FLOOR - seat.h
    base['arms'] = {'L': dict(arm_free((215.0, y - 16, -40.0), (0.6, 0.0, -0.6), 'palm'), flat_on=y),
                    'R': arm_free((K[0] + 14, K[1] - 40, K[2] - 30), (0.3, 0.9, -0.3), 'palm')}
    return base


def spec_slump(sp, seat):
    """Slumped (defeated, bored, sulking): the hips slid forward to the seat's front, the back rounded against the
    chair (the shoulders on its back, the lower back off it), the chair back giving a little, the head forward and
    down, arms limp in the lap, legs out."""
    dz = 70.0
    base = _spec(lean=-21.0, dz=dz, give=0.4, head_lean=24.0, head_dy=34.0, tail=17.0,
                 feet={'L': (-128, dz + 296.0), 'R': (124, dz + 288.0)},           # legs out and splayed
                 knee_pole={'L': (-0.45, -1.0, 0.6), 'R': (0.45, -1.0, 0.6)})
    base['arms'] = {s: arm_free((30.0, 470.0, 128.0), (0.5, 1.0, -0.1), 'palm') for s in 'LR'}
    base['back_on'] = 'shoulders'
    return base


def _rise_above(j, s, top, pad=6.0):
    """Where along a leg (0-1 the thigh, 1-2 the shin) it rises above a surface at body height `top`."""
    hip, knee, foot = j['hip' + s], tuple(V.knee_of(j, s)), j['foot' + s]
    for k in range(41):
        u = k / 20
        q = vlerp(hip, knee, u) if u <= 1 else vlerp(knee, foot, u - 1)
        if q[1] < top - pad:
            return max(0.3, u)
    return None


def _shoe_low(foot, toe, yaw=0.0, roll=0.0, sole=False):
    """How far the shoe's lowest point is below the ankle (views' shoe, toes lifted `toe` degrees)."""
    j = {'footX': foot, 'toeX': toe, 'foot_yawX': yaw, 'foot_rollX': roll, 'soleX': sole}
    f = V.shoe_frame(j, 'X')
    return max(f(sx, sy, sz)[1] for sx in (-28, 28) for sy in (0, 36) for sz in (-28, 92)) - foot[1]


PART1 = list(POSES)
POSES.update({
    'cross, knee over knee': (spec_cross_knee, 'office'),
    'cross, ankle on knee': (spec_figure_four, 'office'),
    'feet up': (spec_feet_up, 'office+desk'),
    'perch, chair edge': (spec_perch, 'office'),
    'perch, desk corner': (spec_perch_desk, 'desk'),
    'slump': (spec_slump, 'office'),
})


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


# ------------------------------------------------------------------------------------------------ part 2 moves
DUR.update({'cross': 0.7, 'uncross': 0.5, 'feet_up': 1.5, 'feet_down': 0.8, 'feet_down_snap': 0.4, 'scoot': 0.4,
            'slump': 1.5, 'slump_collapse': 0.4, 'swivel': 0.8})


def _path(u, pts):
    """A point along a few waypoints [(u, point)], eased between each pair."""
    if u <= pts[0][0]:
        return pts[0][1]
    for (u0, a), (u1, b) in zip(pts, pts[1:]):
        if u <= u1:
            return vlerp(a, b, ease((u - u0) / (u1 - u0)))
    return pts[-1][1]


def cross_legs(sp, seat, u, kind='knee', top='R', start=None):
    """Crossing the legs (0.7 s; uncross: the same played back over 0.5 s): the weight shifts and the lower foot
    comes in, the top knee lifts, swings over (always above the other knee: never through it), and settles. kind:
    'knee' (knee over knee) or 'four' (ankle on knee)."""
    a = start or spec_upright(sp, seat, 'lap' if kind == 'knee' else 'thighs')
    b = (spec_cross_knee if kind == 'knee' else spec_figure_four)(sp, seat, top)
    lo = 'L' if top == 'R' else 'R'
    s = mix(a, b, seg(u, 0.1, 0.95))
    A0 = _default_sided(a, 'ankle', top)
    A1 = b['ankle'][top]
    kn, _ = knees(sp, seat, b)
    over_h = FLOOR - realize(sp, seat, dict(b, arms={}))['bob'] - kn[lo][1]     # the lower knee's height
    if kind == 'knee':
        way = [(0.0, A0), (0.35, (A0[0], A0[1] + 130.0, A0[2] + 70.0)),
               (0.7, (A1[0] * 0.5 + A0[0] * 0.5, max(A1[1], over_h) + 70.0, A1[2] + 50.0)), (1.0, A1)]
    else:
        way = [(0.0, A0), (0.35, (A0[0] + 30.0, A0[1] + 170.0, A0[2] - 10.0)),
               (0.72, (A1[0], A1[1] + 85.0, A1[2] + 10.0)), (1.0, A1)]
    s['ankle'] = dict(s.get('ankle') or {}, **{top: _path(u, way)})
    s['on'] = dict(b['on'], **({top: 'step'} if u < 0.999 else {}))
    s['contact'] = b['contact'] if u > 0.9 else None
    s['cross'] = top
    return s


def feet_up_move(sp, seat, u):
    """Feet up on the desk (1.5 s): a push back from the desk (the chair rolls), the lean back with the hands going
    to the head, the left leg swings up and lands its heel (0.4 s), the right lands crossed on it (0.3 s), a settle."""
    a, b = spec_upright(sp, seat), spec_feet_up(sp, seat)
    lb = lean_back_move(sp, seat, seg(u, 0.12, 0.42), 'head')
    s = dict(lb)
    s['roll'] = b['roll'] * seg(u, 0.0, 0.22)
    s['lean'] = lb['lean'] * (b['lean'] / -18.0 if b['lean'] else 1) - 1.5 * math.sin(math.pi * seg(u, 0.87, 1.0))
    edge = seat.desk.front - s['roll']
    ank, on = {}, {}
    for side, (u0, u1) in (('L', (0.4, 0.67)), ('R', (0.62, 0.87))):
        A0 = _default_sided(a, 'ankle', side)
        A1 = b['ankle'][side]
        hi = (lerp(A0[0], A1[0], 0.5), seat.desk.h + 120.0, edge - 60.0)      # up behind the desk's edge first
        ank[side] = _path(seg(u, u0, u1), [(0.0, A0), (0.45, hi), (0.75, (A1[0], A1[1] + 40.0, A1[2] - 10.0)),
                                            (1.0, A1)])
        on[side] = 'floor' if u <= u0 else b['on'][side] if u >= u1 else 'step'
    s.update(ankle=ank, on=on, cross='R', legs_over='above the desk', back_on=None,
             toe={sd: b['toe'][sd] * seg(u, w0, w1) for sd, (w0, w1) in (('L', (0.45, 0.67)), ('R', (0.66, 0.87)))},
             sole=b['sole'], knee_pole=b['knee_pole'], contact=b['contact'] if u > 0.78 else None)
    return s


def feet_down_move(sp, seat, u, kind='normal'):
    """Feet down off the desk (0.8 s; 'snap', caught out: 0.4 s): the legs first (the top one, then the other; both
    at once when snapped), then he sits up, the hands coming down to the thighs; the chair stays where it rolled."""
    b, a = spec_feet_up(sp, seat), spec_upright(sp, seat)
    a = dict(a, roll=b['roll'])
    wins = {'R': (0.0, 0.4), 'L': (0.2, 0.6)} if kind == 'normal' else {'R': (0.0, 0.5), 'L': (0.0, 0.5)}
    up_k = seg(u, 0.45, 1.0) if kind == 'normal' else seg(u, 0.25, 0.85)
    s = mix(b, a, up_k)
    if kind == 'snap':
        s['lean'] += 4.0 * math.sin(math.pi * seg(u, 0.6, 1.0))        # sits up a touch too far: caught out
    edge = seat.desk.front - b['roll']
    ank, on = {}, {}
    for side, (u0, u1) in wins.items():
        A0, A1 = b['ankle'][side], _default_sided(a, 'ankle', side)
        k = seg(u, u0, u1)
        ank[side] = _path(k, [(0.0, A0), (0.3, (A0[0], A0[1] + 30.0, A0[2] - 10.0)),
                              (0.6, (lerp(A0[0], A1[0], 0.6), seat.desk.h + 60.0, edge - 40.0)), (1.0, A1)])
        on[side] = b['on'][side] if k == 0 else 'floor' if k >= 1 else 'step'
    s.update(ankle=ank, on=on, cross='R', legs_over='above the desk', back_on=None,
             toe={sd: b['toe'][sd] * (1 - seg(u, *wins[sd])) for sd in 'LR'},
             sole={sd: seg(u, *wins[sd]) < 0.5 for sd in 'LR'},
             knee_pole={sd: vlerp(b['knee_pole'][sd], _default_sided(a, 'knee_pole', sd), seg(u, *wins[sd]))
                        for sd in 'LR'},
             contact=b['contact'] if u < 0.2 else None)
    s['arms'] = mix(b, a, seg(u, 0.4 if kind == 'normal' else 0.2, 1.0))['arms']
    if 0 < seg(u, 0.4, 1.0) < 1 and kind == 'normal':        # the hands come out and down, past the shoulders
        k = seg(u, 0.4, 1.0)
        for side in 'LR':
            h = s['arms'][side]['hand']
            s['arms'][side] = dict(s['arms'][side], hand=(h[0] + 45 * math.sin(math.pi * k), h[1], h[2]))
    s['tucked'] = b['tucked'] if up_k < 0.3 else None
    return s


def scoot_to_perch(sp, seat, u):
    """Two small hip shuffles forward to the seat's front edge (0.4 s), leaning in, the hands going to the knees."""
    a, b = spec_upright(sp, seat), spec_perch(sp, seat)
    s = mix(a, b, seg(u, 0.0, 1.0))
    s['dz'] = b['dz'] * (0.5 * seg(u, 0.0, 0.45) + 0.5 * seg(u, 0.5, 0.95))
    s['lift'] = 0.0
    s['tail'] = 0.0
    hop = 0.035 * (math.sin(math.pi * seg(u, 0.0, 0.45)) + math.sin(math.pi * seg(u, 0.5, 0.95)))
    s['dip'] = -seat.bob * hop                                 # each shuffle lifts the hips a little off the seat
    s['back_off'] = None
    s['perch'] = None
    return s


def slump_move(sp, seat, u, kind='slow'):
    """Slumping (1.5 s slow deflate; 'collapse' 0.4 s, comic): a breath out, the shoulders drop first, the hips
    slide forward, the back rounds against the chair, the head goes last (overlapping action, Williams)."""
    a, b = spec_upright(sp, seat), spec_slump(sp, seat)
    if kind == 'collapse':
        k = seg(u, 0.0, 0.75)
        s = mix(a, b, k)
        s['lean'] = b['lean'] * k + 3.0 * math.sin(math.pi * seg(u, 0.75, 1.0))     # a small bounce off the back
        s['head_lean'] = b['head_lean'] * seg(u, 0.1, 0.9)
        s['tail'] = b['tail'] * seg(u, 0.35, 0.8)
        s['feet'] = mix(a, b, seg(u, 0.3, 0.85))['feet']           # the feet slide out after the hips
        s['back_on'] = b['back_on'] if u >= 0.75 else None
        return s
    s = mix(a, b, seg(u, 0.2, 0.85))
    s['lean'] = -2.5 * math.sin(math.pi * seg(u, 0.0, 0.22)) + b['lean'] * seg(u, 0.22, 0.85)   # the breath, then back
    s['head_dy'] = b['head_dy'] * seg(u, 0.12, 0.5)                                            # shoulders drop first
    s['head_lean'] = b['head_lean'] * seg(u, 0.55, 1.0)                                        # the head last
    s['dz'] = b['dz'] * seg(u, 0.25, 0.8)
    s['tail'] = b['tail'] * seg(u, 0.45, 0.9)
    s['feet'] = mix(a, b, seg(u, 0.35, 0.95))['feet']
    s['give'] = 1.0 - (1.0 - b['give']) * seg(u, 0.2, 0.5)
    s['back_on'] = b['back_on'] if u >= 0.85 else None
    return s


def spec_steeple(sp, seat):
    """Upright, fingertips together in front of the chest (the villain's steeple)."""
    sp_ = spec_upright(sp, seat)
    sp_['arms'] = {s: arm_free((10.0, 250.0, 150.0), (0.9, 0.7, -0.3), 'point') for s in 'LR'}
    return sp_


def swivel(sp, seat, u, frm=180.0, to=0.0, hands=None):
    """The swivel-chair turn (0.8 s; the villain's reveal): he and the chair turn together, the head a beat ahead
    (the eyes lead: figure-rig s.6), a small wind-up first and a lean-in settle; the desk stays put in the room.
    Returns the spec; spec['yaw'] and spec['head_yaw'] are the angles to draw him at.
    hands: 'folded' (the default at a desk: he arrives with his hands already folded on it, so there is no hands-down
    move after the turn; Sam, 8 Nov, Ad-Vanced Notice note 47c: "the perfect swivel") or 'steeple' (fingertips together
    in front of his chest; the default away from a desk)."""
    hands = hands or ('folded' if getattr(seat, 'desk', None) is not None else 'steeple')
    s = spec_hands_folded(sp, seat) if hands == 'folded' else spec_steeple(sp, seat)
    k = seg(u, 0.12, 0.85)
    yaw = frm + (to - frm) * k - 8.0 * math.sin(math.pi * seg(u, 0.0, 0.12)) * (1 if to < frm else -1)
    head = frm + (to - frm) * seg(u, 0.05, 0.7)
    s['lean'] = 4.0 * math.sin(math.pi * seg(u, 0.8, 1.0)) + 2.0 * seg(u, 0.85, 1.0)
    s['yaw'], s['head_yaw'] = yaw, head
    s['swivel'] = yaw
    return s


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
    if seat.kind == 'desk':                             # perched on a desk: the left thigh lies on its top
        off = j['hipL'][1] + PERCH_SIT + j['bob'] - (FLOOR - seat.h)
        x, _, z = _chair(j, j['hipL'])
        if abs(off) > 3 or not seat.on_top(x, z):
            out.append(f'{where} at {t:.2f} s: the perched hip is {off:+.0f} off the desk top'
                       + ('' if seat.on_top(x, z) else ', and not over it'))
    else:
        off = V.HIP_Y + SIT + j['bob'] - spec.get('dip', 0.0) - spec.get('tail', 0.0) - (FLOOR - seat.h + seat.cushion)
        if spec.get('tail', 0.0) > 24:
            out.append(f'{where} at {t:.2f} s: slid {spec["tail"]:.0f} down the seat: more than the thigh allows')
        if j['lift'] == 0 and abs(off) > 3:                 # (a landing's settle, `dip`, is the cushion giving)
            out.append(f'{where} at {t:.2f} s: hips {off:+.0f} off the seat')
        hz = j['dz'] - j['roll']
        if j['lift'] == 0 and not seat.on_top(0.0, hz):
            out.append(f'{where} at {t:.2f} s: hips {hz:+.0f} along the seat: off its edge')
        if spec.get('perch') and hz < seat.front - (seat.front - seat.rear) / 3 - 2:
            out.append(f'{where} at {t:.2f} s: a perch sits on the seat\'s front third (hips {hz:.0f}, want '
                       f'{seat.front - (seat.front - seat.rear) / 3:.0f} or more)')
    if spec.get('dip', 0.0) > 14:
        out.append(f'{where} at {t:.2f} s: the seat gives {spec["dip"]:.0f}: too soft')
    out += [f'{where} at {t:.2f} s: {f}' for f in check_legs(j)]
    out += [f'{where} at {t:.2f} s: {f}' for f in check_back(j)]
    for s in 'LR':
        hip, foot = j['hip' + s], j['foot' + s]
        sg = -1 if s == 'L' else 1
        knee, end = V.ik3(hip, foot, V.THIGH, V.SHIN, j.get('knee_pole' + s, (0.12 * sg, 0.0, 1.0)))
        gap = math.dist(end, foot)
        if gap > 4:
            out.append(f'{where} at {t:.2f} s: {s} leg {gap:.0f} short of the foot (it would stretch: move the feet or seat)')
        a, b = V._sub(hip, knee), V._sub(foot, knee)
        cosang = V._dot(a, b) / ((math.sqrt(V._dot(a, a)) * math.sqrt(V._dot(b, b))) or 1)
        if math.degrees(math.acos(max(-1, min(1, cosang)))) < 35:
            out.append(f'{where} at {t:.2f} s: {s} knee folded tighter than 35 degrees')
        th, sh_ = V._unit(V._sub(knee, hip)), V._unit(V._sub(foot, knee))
        ax = (th[1] * sh_[2] - th[2] * sh_[1], th[2] * sh_[0] - th[0] * sh_[2], th[0] * sh_[1] - th[1] * sh_[0])
        n = math.sqrt(V._dot(ax, ax))
        if n > 0.15 and abs(ax[0]) > 0.7 * n and ax[0] > 0:   # the knee's hinge, side to side: the shin must fold
            out.append(f'{where} at {t:.2f} s: {s} knee bends backwards')   # back (a turned-out knee is the pole's job)
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
    if rec is not None and j['lean'] < -1 and j['lift'] < 0.05 and abs(rec - recline_of(j)) > 1:
        out.append(f'{where} at {t:.2f} s: the chair back does not follow the lean')
    return out


def shoe_points(j, s):
    """The shoe's corners (body frame), as views draws it."""
    f = V.shoe_frame(j, s)
    return [f(sx, sy, sz) for sx in (-28, 28) for sy in (0, 36) for sz in (-28, 92)]


def leg_gap(j, s, q, part=None):
    """How far a point is from the surface of a leg (or one part of it: 'thigh', 'shin'); - = inside it."""
    hip, foot, knee = j['hip' + s], j['foot' + s], tuple(V.knee_of(j, s))
    best = 1e9
    for a, b, ra, rb, name in ((hip, knee, THIGH_R, KNEE_R, 'thigh'), (knee, foot, KNEE_R, ANKLE_R, 'shin')):
        if part and name != part:
            continue
        ab = V._sub(b, a)
        u = max(0.0, min(1.0, V._dot(V._sub(q, a), ab) / (V._dot(ab, ab) or 1)))
        best = min(best, math.dist(q, vlerp(a, b, u)) - lerp(ra, rb, u))
    return best


def leg_samples(j, s, n=14):
    """Points along a leg with the leg's half-width there (body frame): the thigh then the shin."""
    hip, foot, knee = j['hip' + s], j['foot' + s], tuple(V.knee_of(j, s))
    out = []
    for a, b, ra, rb, part in ((hip, knee, THIGH_R, KNEE_R, 'thigh'), (knee, foot, KNEE_R, ANKLE_R, 'shin')):
        for i in range(n):
            u = i / (n - 1)
            out.append((vlerp(a, b, u), lerp(ra, rb, u), part))
    return out


def _into_box(q, r, box):
    """How far a ball (centre q, radius r) sinks into a box (x0, x1, y0, y1, z0, z1): > 0 = into it."""
    x0, x1, y0, y1, z0, z1 = box[:6]
    c = (min(max(q[0], x0), x1), min(max(q[1], y0), y1), min(max(q[2], z0), z1))
    if c == tuple(q):                               # inside: the distance to the nearest face, plus the radius
        return r + min(q[0] - x0, x1 - q[0], q[1] - y0, y1 - q[1], q[2] - z0, z1 - q[2])
    return r - math.dist(c, q)


def _solids(j):
    """Every solid set piece near the legs, each as (name, box in its own frame, body-to-own-frame, allowance)."""
    seat, out = j['seat'], []
    bob = j['bob']
    if seat.kind == 'desk':
        _, inv = seat.as_desk.xf(j, seat_frame=True)
        out += [('the desk he sits on', b, inv, 6.0) for b in seat.as_desk.boxes(bob)]
    else:
        top = FLOOR - bob - seat.h
        rel = j['dz'] - j['roll']
        out.append(('the seat', (-seat.width, seat.width, top, top + 30, seat.rear, seat.front),
                    lambda x, y, z: (x, y, z + rel), 6.0 + seat.cushion))
    if seat.desk:
        _, inv = seat.desk.xf(j)
        out += [('the desk', b, inv, 6.0) for b in seat.desk.boxes(bob)]
    return out


def check_legs(j):
    """Part 2's leg checks, in plain words: each foot on what it rests on (floor, desk top, the other knee or leg;
    or clear of everything when dangling), and no leg or shoe through the seat, the desk or the other leg."""
    out, spec, seat = [], j['spec'], j['seat']
    floor = FLOOR - j['bob']
    up = spec.get('foot_up') or {}
    on = spec.get('on') or {}
    samples = {s: leg_samples(j, s) for s in 'LR'}
    solids = _solids(j)
    for s in 'LR':
        o = on.get(s) or ('step' if up.get(s, 0) >= 1 else 'floor')   # a foot stepping back is in the air
        shoe = shoe_points(j, s)
        low = max(q[1] for q in shoe)
        other = 'R' if s == 'L' else 'L'
        if o == 'floor' and abs(low - floor) > 4:
            out.append(f'{s} foot {"sinks " if low > floor else ""}{abs(low - floor):.0f} '
                       f'{"into" if low > floor else "off"} the floor')
        elif o == 'air' and low > floor - 10:
            out.append(f'{s} foot is meant to dangle but reaches the floor')
        elif o == 'desk':
            d = seat.desk
            top = FLOOR - j['bob'] - d.h
            _, inv = d.xf(j)
            heel = max(shoe, key=lambda q: q[1])
            hx, _, hz = inv(*heel)
            if abs(heel[1] - top) > 5:
                out.append(f'{s} heel {heel[1] - top:+.0f} off the desk top')
            if not (-d.width <= hx <= d.width and d.front <= hz <= d.front + d.depth):
                out.append(f'{s} heel is not over the desk')
        elif o in ('knee', 'leg'):
            part = 'thigh' if o == 'knee' else 'shin'
            ankle = j['foot' + s]
            gap = leg_gap(j, other, ankle, part) - ANKLE_R
            deep = -(leg_gap(j, other, ankle) - ANKLE_R)
            if gap > 10:
                out.append(f'{s} ankle floats {gap:.0f} above the other {"knee" if o == "knee" else "leg"}')
            if deep > 14:
                out.append(f'{s} ankle sinks {deep:.0f} into the other leg')
        for name, box, inv, allow in solids:
            deep = max([_into_box(inv(*q), r, box) - (8 if p == 'thigh' and name == 'the seat' else 0)
                        for q, r, p in samples[s]] + [_into_box(inv(*q), 0.0, box) for q in shoe])
            if deep > allow:                    # (a thigh presses the seat's front edge a little: it gives)
                out.append(f'{s} leg goes {deep:.0f} into {name}')
    # the legs against each other: never through, except where one is meant to rest on the other
    rest = spec.get('contact') or {}
    spots = []
    for s, (_, other) in rest.items():
        spots.append(j['foot' + s] if 'ankle' in rest[s][0] else tuple(V.knee_of(j, other)))
    worst = 0.0
    for qa, ra, _ in samples['L'] + [(q, 0.0, 'shoe') for q in shoe_points(j, 'L')]:
        for qb, rb, _ in samples['R'] + [(q, 0.0, 'shoe') for q in shoe_points(j, 'R')]:
            if any(math.dist(qa, c) < 70 and math.dist(qb, c) < 70 for c in spots):
                continue
            worst = max(worst, 0.8 * (ra + rb) + (8 if not (ra and rb) else 0) - math.dist(qa, qb))
    if worst > 0:
        out.append(f'the legs pass {worst:.0f} through each other')
    return out


def back_gap(j, hb):
    """The gap between his back and the chair back's face at body height `hb` (before the lean): + = a gap, - =
    into the cushion. None if the seat has no back or the back doesn't reach that high."""
    seat = j['seat']
    if not seat.back_top or seat.kind == 'desk':
        return None
    T = 0.612 * j.get('_shoulders', 150)
    P = V.leaned((0.0, hb, -T), j['lean'])
    P = (0.0, P[1], P[2] + j['dz'] - j['roll'])
    rec = recline_of(j)
    top = FLOOR - j['bob'] - seat.h
    a = V.leaned((0.0, top - seat.back_top, seat.back_z), -rec)
    b = V.leaned((0.0, top - 8, seat.back_z), -rec)
    ly, lz = b[1] - a[1], b[2] - a[2]
    L = math.hypot(ly, lz)
    u = ((P[1] - a[1]) * ly + (P[2] - a[2]) * lz) / (L * L)
    if not 0.0 <= u <= 1.0:
        return None
    ny, nz = -lz / L, ly / L                       # the face's normal, pointing forward (+z)
    if nz < 0:
        ny, nz = -ny, -nz
    return (P[1] - a[1]) * ny + (P[2] - a[2]) * nz


def check_back(j):
    """Back on the chair back (lean back, feet up, slump: the shoulders touch it), clear of it (a perch), never
    through it."""
    out, spec = [], j['spec']
    if j['lift'] > 0.05:
        return out
    gaps = {hb: back_gap(j, hb) for hb in range(60, 420, 20)}
    for hb, g in gaps.items():
        if g is not None and g < -26:
            out.append(f'the back goes {-g:.0f} through the chair back')
            break
    g = next((g for g in gaps.values() if g is not None), None)     # the top of the chair back: shoulder blades
    if spec.get('back_on') and (g is None or g > 8):
        out.append('a gap behind his shoulders: they should rest on the chair back'
                   + (f' ({g:.0f})' if g is not None else ''))
    if spec.get('back_off') and any(g is not None and g < 15 for g in gaps.values()):
        out.append('his back touches the chair back: a perch sits clear of it')
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
    out += audit_part2(sp)
    return out


def part2_moves(sp):
    """Part 2's moves: (name, seat, u -> spec, length)."""
    o, d = Seat('office'), Seat('office', desk=Desk())
    return [
        ('cross, knee over knee', o, lambda u: cross_legs(sp, o, u, 'knee'), DUR['cross']),
        ('uncross, knee over knee', o, lambda u: cross_legs(sp, o, 1 - u, 'knee'), DUR['uncross']),
        ('cross, ankle on knee', o, lambda u: cross_legs(sp, o, u, 'four'), DUR['cross']),
        ('uncross, ankle on knee', o, lambda u: cross_legs(sp, o, 1 - u, 'four'), DUR['uncross']),
        ('feet up', d, lambda u: feet_up_move(sp, d, u), DUR['feet_up']),
        ('feet down', d, lambda u: feet_down_move(sp, d, u), DUR['feet_down']),
        ('feet down, caught out', d, lambda u: feet_down_move(sp, d, u, 'snap'), DUR['feet_down_snap']),
        ('scoot to perch', o, lambda u: scoot_to_perch(sp, o, u), DUR['scoot']),
        ('slump', o, lambda u: slump_move(sp, o, u), DUR['slump']),
        ('slump, collapse', o, lambda u: slump_move(sp, o, u, 'collapse'), DUR['slump_collapse']),
        ('swivel turn', d, lambda u: swivel(sp, d, u), DUR['swivel']),
    ]


def check_desk_still(frames, where='swivel turn'):
    """The chair follows the turn, the desk doesn't: a desk corner stays on the same spot on screen while he
    swivels (the person drawn at his own yaw, snapped and mirrored as views draws him)."""
    spots = []
    for t, j in frames:
        deg, mir = V.snap(j['spec']['yaw'])
        T, _ = j['seat'].desk.xf(j)
        (ox, oy), _ = V.project((0.0, 0.0, j['dz']), deg)
        (cx, cy), _ = V.project(T(-440.0, FLOOR - j['bob'] - 500.0, 555.0), deg)
        m = -1 if mir else 1
        spots.append((t, m * (ox + cx), oy + cy + j['bob']))
    x0, y0 = spots[0][1:]
    for t, x, y in spots:
        if math.hypot(x - x0, y - y0) > 3:
            return [f'{where} at {t:.2f} s: the desk moves {math.hypot(x - x0, y - y0):.0f} on screen (it turned with him)']
    return []


def audit_part2(sp):
    out = []
    for name, seat, fn, dur in part2_moves(sp):
        fr = [(t, realize(sp, seat, s)) for t, s in frames_of(fn, dur)]
        for t, j in fr:
            out += check_frame(j, t, name)
        if name == 'swivel turn':
            out += check_desk_still(fr)
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


def draw_one(B, H, sp, j, deg, t=0.0, size=(600, 900), at=(300, 200), s=0.62, check=True, head_yaw=None):
    from PIL import Image
    im = Image.new('RGBA', size, (226, 222, 214, 255))
    if check:
        H.begin()
    V.person(im, B.Cam(1.0, 540, 960), at[0], at[1], s, sp, t, float(deg), j, head_yaw=head_yaw)
    faults = H.end(t, 'sitting') if check else []
    return im, faults


AVOID = {   # views where a hand is hidden (rule 41): a film never shows the pose from there
    'perch, desk corner': {'three-quarter': 'the far hand (on his knee) hidden by his body'},
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
    'cross, knee over knee': ['references/sitting/oval-office-armchairs-sofas.jpg'],
    'cross, ankle on knee': ['references/sitting/ankle-on-knee-bench.jpg'],
    'feet up': ['references/sitting/feet-up-on-desk.jpg', 'references/sitting/feet-on-desk-soles.jpg'],
    'perch, desk corner': ['references/sitting/legs-dangling-from-desk-edge.jpg'],
}
REF_VIEW = {'armchair': 45, 'cross, knee over knee': 45, 'cross, ankle on knee': 135, 'feet up': 0,
            'perch, desk corner': 90}     # each drawn from the photo's own angle


def refsheet(out, rows=None):
    """Each pose from its photo's angle (REF_VIEW; else front on) beside its reference photos (rule 76)."""
    from PIL import Image, ImageDraw, ImageFont
    import posegallery as G
    B, H = _setup()
    sp = G.MODEL
    root = os.path.dirname(HERE)
    font = ImageFont.truetype(B.SANS, 22)
    rows = rows or list(REFS)
    rh = 250
    img = Image.new('RGB', (1080, 44 + rh * len(rows)), (16, 16, 20))
    d = ImageDraw.Draw(img)
    d.text((10, 10), 'Ours (left) beside the photos (rule 76)', font=font, fill=(255, 255, 255))
    for r, name in enumerate(rows):
        y = 44 + r * rh
        im, _ = draw_one(B, H, sp, pose(sp, name), REF_VIEW.get(name, 0), at=(300, 230), check=False)
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


def sheet(out, names=None, title='Sitting kit: every pose, five views, checked'):
    """Every pose from the five views, the hand check (rule 41) and the kit's checks under each."""
    from PIL import Image, ImageDraw, ImageFont
    import posegallery as G
    B, H = _setup()
    sp = G.MODEL
    font, small = ImageFont.truetype(B.SANS, 22), ImageFont.truetype(B.SANS, 16)
    views = G.VIEWS
    tw, th = 180, 270
    names = names or list(POSES)
    img = Image.new('RGB', (170 + tw * len(views), (th + 50) * len(names) + 50), (16, 16, 20))
    d = ImageDraw.Draw(img)
    d.text((10, 12), title, font=font, fill=(255, 255, 255))
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


def clip(out, fn, dur, views=(0, 90), hold=0.4, small=True, label='', pad=None):
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
        frame = Image.new('RGB', (pad or 540 * len(views), 760), (226, 222, 214))
        x0 = ((pad or 540 * len(views)) - 540 * len(views)) // 2
        for c, deg in enumerate(views):
            j = fn(u)
            yaw = j['spec'].get('yaw')
            im, _ = draw_one(B, H, sp, j, deg if yaw is None else yaw, i / FPS, size=(540, 760), at=(270, 190),
                             s=0.55, check=False, head_yaw=j['spec'].get('head_yaw'))
            frame.paste(im.convert('RGB'), (x0 + 540 * c, 0))
        ImageDraw.Draw(frame).text((14, 10), label, font=font, fill=(40, 40, 40))
        frame.save(os.path.join(tmp, f'{i:04d}.png'))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.png'),
                    '-vf', 'scale=iw/2*2:ih/2*2' if not small else 'scale=iw*0.75:-2', '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', '-crf', '26', out], check=True)
    print('clip:', out)


def clips2(out):
    """Part 2's moves in one small video (front and side; the swivel from the front, the desk staying put),
    each labelled and held a moment at each end."""
    import shutil
    import subprocess
    import tempfile
    import posegallery as G
    sp = G.MODEL
    tmp = tempfile.mkdtemp()
    parts = []
    names = {n: (seat, fn, dur) for n, seat, fn, dur in part2_moves(sp)}
    order = ['cross, knee over knee', 'uncross, knee over knee', 'cross, ankle on knee', 'uncross, ankle on knee',
             'feet up', 'feet down', 'feet down, caught out', 'scoot to perch', 'slump', 'slump, collapse',
             'swivel turn']
    for i, name in enumerate(order):
        seat, fn, dur = names[name]
        f = os.path.join(tmp, f'{i:02d}.mp4')
        clip(f, lambda u, fn=fn, seat=seat: realize(sp, seat, fn(u)), dur,
             views=(0,) if name == 'swivel turn' else (0, 90), label=f'{name} ({dur:g} s)', pad=1080)
        parts.append(f)
    lst = os.path.join(tmp, 'list.txt')
    with open(lst, 'w') as fh:
        fh.write(''.join(f"file '{f}'\n" for f in parts))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out],
                   check=True)
    shutil.rmtree(tmp)
    print('moves video:', out, f'{os.path.getsize(out) / 1e6:.1f} MB')


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
        sheet(a[1], [n for n in POSES if n not in PART1] if a[2:] == ['2'] else None,
              'Sitting kit, part 2: every pose, five views, checked' if a[2:] == ['2'] else
              'Sitting kit: every pose, five views, checked')
    elif a and a[0] == 'refs':
        refsheet(a[1], [n for n in REFS if n not in PART1] if a[2:] == ['2'] else None)
    elif a and a[0] == 'clips':
        clips(a[1])
    elif a and a[0] == 'clips2':
        clips2(a[1])
    elif a and a[0] == 'audit':
        fs = audit()
        print('\n'.join(fs) or 'sitting kit: clean')
        sys.exit(1 if fs else 0)
    else:
        print(__doc__)
