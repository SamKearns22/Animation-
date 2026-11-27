#!/usr/bin/env python3
"""sitting: the sitting kit (Sam, 7 Nov: "the full gamut of sitting animation"; plan in notes/sitting-kit.md).

PARTS: one module in 3 files (cost-spike fix 5c; parts.py runs them inside sitting, so setters reach all):
  sitting_b.py (specs); sitting_c.py (checks). Import sitting, never a part; touch.py NAME gives the file and line.

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
from ink import INK           # noqa: E402
import parts as _PARTS        # noqa  (cost-spike fix 5c: this module is kept in parts; parts.py)

FPS = 12
SIT = 40.0                   # the hip joint sits this far above the seat: the thigh's half-thickness (no thigh in the seat)
FLOOR = 928.0
ANKLE_UP = FLOOR - V.ANKLE_Y  # 38: the ankle above the sole
PERCH_SIT = 30.0             # perched on a desk, the hip joint this far above its top (a thigh lying on it)
ARMREST_DROP = 22.0          # Open Wounds note 19: a resting hand's centre this far below the forearm's line
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
        # a moulded plastic stacking chair (Blessed's TV room, chat 5): shell seat and back in one colour, four
        # splayed steel legs (Seat('plastic', col=..., top=...) for another colour)
        'plastic': dict(h=255, front=120, rear=-118, width=118, back_top=270, back_z=-78, arms=None, cushion=0,
                        swivel=False, col=(62, 84, 136), top=(84, 108, 160), legs=(150, 154, 160)),
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
                col_top = V.project((0.0, top + 52, -5 + sh), yaw)[0]
                p.line([col_top, hub], (40, 40, 46), 14)
            parts.append((-999, 'pre', base))
        else:
            leg_h = self.h - (40 if self.kind == 'armchair' else 30)
            for lx in (-w + 14, w - 14):
                for lz in (self.rear + 14, self.front - 14):
                    def leg(p, lx=lx, lz=lz):
                        a = V.project((lx, top + 30, lz + sh), yaw)[0]
                        sp_ = 1.08 if self.kind in ('stool', 'plastic') else 1
                        b = V.project((lx * sp_, floor, lz * sp_ + sh), yaw)[0]
                        lc = getattr(self, 'legs', None) or ((52, 40, 30) if self.kind == 'stool' else (40, 30, 26))
                        p.line([a, b], lc, 10)
                        if self.kind == 'plastic':
                            p.line([a, b], INK, 1.2)
                    parts.append((_depth(lx, lz + sh, yaw) - 400, 'pre', leg))
            if self.kind == 'armchair':
                parts.append((-500, 'pre', lambda p: _box(p, yaw, -w - 50, w + 50, top + 6, floor - 30, self.rear,
                                                          self.front, c, None, 0, sh)))
        pad = 52 if self.kind == 'office' else 30        # Open Wounds chat 32 (critique r27: "the seat is a thin
        #                                                  slab"): an office seat is a padded cushion about 8 cm deep
        parts.append((-300, 'pre', lambda p: _box(p, yaw, -w, w, top, top + pad, self.rear, self.front, c, ct, 0, sh)))
        if self.back_top:
            bz = -78 if self.kind in ('office', 'plastic') else -86
            bz = min(bz, j.get('_back_face', bz))      # R7 chat 14: against the full body's back (views.r7_back_face)
            thick = 28 if self.kind in ('office', 'plastic') else 60
            bw = w - 10 if self.kind in ('office', 'plastic') else w + 50

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


_PARTS.include(globals(), 'sitting_b', 'sitting_c')


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
