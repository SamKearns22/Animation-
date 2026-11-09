#!/usr/bin/env python3
"""grips: hands on things, right from every view (Job G, 9 Nov; Sam's notes: 10 of 60 body notes were a hand on a
prop or surface, the biggest group).

- `held(j, side, sp, draw, at=None)`: a prop in a hand (a phone, a cup, a glass) put in the right place in the drawing
  order for each view: hidden by his body when it is behind it (seen from behind, a cup held in front of him is
  behind his back: never drawn over it), hidden by his head when behind that, over his face when in front of it, and
  the hand drawn over it (the fingers wrap the side we see), so the hand always shows. `draw(p, j2)` is the prop's own
  2D drawing (moves.py's phone and cup); `at` its middle in the body frame (default: the hand).
- `Table` and `on_table(j, side, table, x, shape)`: a table measured once in the person's own frame; the hand's
  contact point put on its top, the table drawn from the same numbers in every view (beyond him from behind,
  between his body and his arms in front), and the contact noted in `j['contacts']`.
- `contact_faults(j)`: every noted contact checked in 3D: a hand more than HOVER above the surface (hovering, or out
  of reach: views.arm_to stops at full reach without saying so) or more than SINK into it; off the table's edge.
  handcheck runs it on every person it probes, so films get it too.
- `Carry`: a prop passed from place to place (on the table, in a hand, in another person's hand): one owner at a time,
  and at every change of owner the hand is on the prop (no jump; Islamocommunism notes 9, 16, 19: the glass jumped,
  the handset slid into the base, two hands held one handset). `Carry.faults()` lists every jump.

Body frame: views' torso frame (units; neck base at 0, y down, z towards the viewer when he faces us).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import figure as F           # noqa: E402
import views as V            # noqa: E402
from ed import INK           # noqa: E402

HOVER = 10.0                  # units (1.5 cm): a resting hand's contact point at most this far above its surface
SINK = 7.0                    # ... and at most this far into it
JUMP = 12.0                   # units: a prop changing owner moves at most this far between frames
RX, RZ = 0.92, 0.42           # the torso as an oval cylinder: half its width and depth, times the shoulders
REAR = ('back', 'three_back')


def _ray_hits(c, yaw, rx, rz, cx=0.0, cz=0.0):
    """Does the ray from body-frame point c towards the camera cross the upright oval (rx, rz) round (cx, cz)?"""
    a = math.radians(yaw)
    dx, dz = -math.sin(a), math.cos(a)
    x, z = c[0] - cx, c[2] - cz
    A = dx * dx / rx ** 2 + dz * dz / rz ** 2
    B = 2 * (x * dx / rx ** 2 + z * dz / rz ** 2)
    C = x * x / rx ** 2 + z * z / rz ** 2 - 1
    disc = B * B - 4 * A * C
    return disc >= 0 and (-B + math.sqrt(disc)) / (2 * A) > 0


def hidden_by(c, yaw, sp):
    """'torso', 'head' or None: what of his own body hides the body-frame point c from this view."""
    sw, hw = sp.get('shoulders', 150), sp.get('hw', 70)
    if -5.0 <= c[1] <= sp.get('bottom', V.JACKET) - 20 and _ray_hits(c, yaw, RX * sw * 0.95, RZ * sw * 0.95):
        return 'torso'
    if -250.0 <= c[1] <= -40.0 and _ray_hits(c, yaw, hw * 0.95, hw * 0.95):
        return 'head'
    return None


def hand_centre(j, side):
    el, wr = j['el' + side], j['wr' + side]
    u = V._unit(V._sub(wr, el))
    return V._add(wr, V._mul(u, 12.0))


# ------------------------------------------------------------------------------------------------ held props
def held(j, side, sp, draw, at=None, hand_over=True):
    """Hold a prop drawn by `draw(p, j2)` in the hand on `side` (already placed): see the module's note."""
    def where(j2):
        c = at if at is not None else hand_centre(j, side)
        yaw = j2['yaw']
        hid = hidden_by(c, yaw, sp)
        if hid == 'torso':
            return 'pre'
        if hid == 'head':
            return 'props'
        return 'face' if c[1] < 20.0 else 'props'

    def go(p, j2):
        draw(p, j2)
        if hand_over:                                # the fingers wrap the side we see: the hand over the prop
            V.hand(p, j2, side, sp, j2.get('hand', {}).get(side, 'fist'))

    j.setdefault('pre', []).append(lambda p, j2, view: where(j2) == 'pre' and go(p, j2))
    j.setdefault('props', []).append(lambda p, j2: where(j2) == 'props' and go(p, j2))
    j.setdefault('face_props', []).append(lambda p, j2: where(j2) == 'face' and go(p, j2))
    if c_on_face(j, side):
        j.setdefault('on_face', set()).add(side)
    return j


def c_on_face(j, side):
    """A hand up at the face (a phone at the ear, a cup at the lips) is drawn over the face when in front of it."""
    return hand_centre(j, side)[1] < 20.0


# ------------------------------------------------------------------------------------------------ surfaces
class Table:
    """A table in the person's own frame: its top `h` metres off the floor, the near edge `z0` units in front of
    him, `w` units each side of his middle, `depth` units deep."""
    def __init__(self, h=0.95, z0=95.0, w=260.0, depth=260.0, height_m=1.75, col=(150, 108, 70)):
        self.y = 928.0 - h / V.M_PER_UNIT * 1.75 / height_m
        self.z0, self.w, self.depth, self.col = z0, w, depth, col

    def corners(self, y=None):
        y = self.y if y is None else y
        return [(-self.w, y, self.z0), (self.w, y, self.z0), (self.w, y, self.z0 + self.depth),
                (-self.w, y, self.z0 + self.depth)]

    def on(self, x, inset=30.0):
        """A point on the top, `inset` units in from the near edge."""
        return (x, self.y, self.z0 + inset)

    def inside(self, pt, margin=4.0):
        return -self.w - margin <= pt[0] <= self.w + margin and \
            self.z0 - margin <= pt[2] <= self.z0 + self.depth + margin

    def draw(self, p, j2):
        yaw = j2['yaw']
        P = lambda q: V.project(q, yaw)[0]
        dk = tuple(int(c * 0.72) for c in self.col)
        T = 34.0
        for x in (-self.w + 20, self.w - 20):                  # legs (near pair; the far pair hide behind the top)
            for z in (self.z0 + 20, self.z0 + self.depth - 20):
                a, b = P((x, self.y + T, z)), P((x, 928.0, z))
                p.line([a, b], dk, 14)
        top = [P(q) for q in self.corners()]
        sides = []
        for i in range(4):                                     # the edge faces turned to us, under the top
            q0, q1 = self.corners()[i], self.corners()[(i + 1) % 4]
            mid = ((q0[0] + q1[0]) / 2, 0, (q0[2] + q1[2]) / 2)
            out = (mid[0], 0, mid[2] - (self.z0 + self.depth / 2))
            n = math.hypot(out[0], out[2]) or 1
            if V.project((out[0] / n, 0, out[2] / n), yaw)[1] > 0.05:
                sides.append([P(q0), P(q1), P((q1[0], self.y + T, q1[2])), P((q0[0], self.y + T, q0[2]))])
        for s in sides:
            p.poly(s, dk, INK, 2.4)
        p.poly(top, self.col, INK, 2.6)


def on_table(j, side, table, x, shape='palm', pole='back', inset=30.0):
    """Rest a hand on the table top at `x`: the contact point on the surface, the table drawn in the right order for
    each view (beyond him from behind: before everything; in front: between his body and his arms)."""
    target = table.on(x, inset)
    V.arm_to(j, side, target, pole, shape)
    j.setdefault('contacts', []).append(('rest', side, shape, table, target))
    if not any(getattr(d, 'table', None) is table for d in j.get('pre', [])):
        def pre(p, j2, view, table=table):
            if view in REAR:
                table.draw(p, j2)

        def mid(p, j2, view, table=table):
            if view not in REAR:
                table.draw(p, j2)
        pre.table = mid.table = table
        j.setdefault('pre', []).append(pre)
        j.setdefault('mid', []).append(mid)
    return j


def contact_point(j, side, shape):
    el, wr = j['el' + side], j['wr' + side]
    return V._add(wr, V._mul(V._unit(V._sub(wr, el)), F.HAND.get(shape, 14)))


def contact_faults(j):
    """[(side, kind, text)] for every contact noted in j['contacts'] (see the module's note)."""
    out = []
    for kind, side, shape, thing, target in j.get('contacts', ()):
        c = contact_point(j, side, shape)
        if kind == 'rest':
            above = thing.y - c[1]
            if above > HOVER:
                out.append((side, 'hovers', f'the hand hovers {above * V.M_PER_UNIT * 100:.0f} cm above the surface '
                                            '(out of reach? move the body or the table, never stretch the arm)'))
            elif -above > SINK:
                out.append((side, 'sinks', f'the hand sinks {-above * V.M_PER_UNIT * 100:.0f} cm into the surface'))
            if not thing.inside(c):
                out.append((side, 'off edge', 'the hand is off the edge of the table'))
        else:
            gap = math.dist(c, target)
            if gap > HOVER:
                out.append((side, 'off grip', f'the hand is {gap * V.M_PER_UNIT * 100:.0f} cm off its grip '
                                              '(Patriots 3 note 9: a hand beside the gun, not on it)'))
    return out


def grip(j, side, target, shape='fist', pole='down', name='grip'):
    """A hand onto a grip point (a gun's receiver, a handle): placed, and noted so contact_faults checks it."""
    V.arm_to(j, side, target, pole, shape)
    j.setdefault('contacts', []).append(('grip', side, shape, name, target))
    return j


# ------------------------------------------------------------------------------------------------ passing things
class Carry:
    """A prop passed between owners over time. `owners`: [(t, owner)], each owner a function t -> the prop's
    position (world or screen units: one system per Carry), e.g. a resting spot or a hand's grip. The prop is where
    its current owner says; the change at each t must not jump."""
    def __init__(self, owners):
        self.owners = sorted(owners, key=lambda o: o[0])

    def owner(self, t):
        cur = self.owners[0][1]
        for t0, o in self.owners:
            if t >= t0:
                cur = o
        return cur

    def at(self, t):
        return self.owner(t)(t)

    def faults(self, fps=12):
        out = []
        for (t0, a), (t1, b) in zip(self.owners, self.owners[1:]):
            d = math.dist(a(t1), b(t1))
            if d > JUMP:
                out.append((t1, f'the prop jumps {d:.0f} units as it changes hands at {t1:.2f} s (the hand is not '
                                f'on it yet: time the take for when it arrives)'))
        return out
