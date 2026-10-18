#!/usr/bin/env python3
"""clipcheck: nothing passes through anything (Sam, 18 Oct: 'a generalised thorough system that catches clipping and
objects sliding through each other, not piecemeal rules'). One check for every film, run by preflight.py before every
animatic when the film module defines `solids(t)` (and, for the drawing-order part, `scene(t)`).

1. Solids. Every person (body, head, upper and lower arms, hands, thighs, shins, feet), prop, piece of furniture and
   flying thing is a simple solid in the room, in metres (X across, + right; Y up from the floor; Z away from the
   camera): capsules (a line with a radius), spheres and boxes. On every frame, no two solids of DIFFERENT owners may
   overlap by more than TOUCH metres, unless the pair is a listed, deliberate contact (`ALLOWED`: a hand on a desk,
   a punch landing), with the times it is allowed.
2. Drawing order. On sampled frames each drawn item (`scene(t)`: name, depth, draw) is drawn alone; wherever two
   items overlap on screen, the one drawn later must not be further from the camera than the earlier one (by more
   than ORDER_TOL metres). This catches what a 3D test cannot: an arm painted in front of someone it is behind.
3. In shot. Anyone listed in the film's `IN_SHOT` [(name, t0, t1)] never touches the frame's edge.

People's solids come from their pose (views.py's 3D skeleton), so any film drawing people with views.person gets
them for free: `person_solids(owner, j, X, Z, yaw, sp)`.

    python3 source/clipcheck.py FILM          run all three on a film and list every fault
"""
import importlib
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import views as V                # noqa: E402

U = V.M_PER_UNIT                 # metres per person unit
SOLE = 928.0
TOUCH = 0.02                     # an overlap this small is a touch, not a pass-through
ORDER_TOL = 0.25                 # drawing order: depth differences smaller than this are not judged


class Solid:
    """kind 'capsule' (a, b, r), 'sphere' (a, r), 'box' (lo, hi): points are (X, Y, Z) in metres."""
    def __init__(self, owner, part, kind, a, b=None, r=0.0):
        self.owner, self.part, self.kind, self.a, self.b, self.r = owner, part, kind, np.asarray(a, float), \
            None if b is None else np.asarray(b, float), r

    def __repr__(self):
        return f'{self.owner}.{self.part}'


def capsule(owner, part, a, b, r):
    return Solid(owner, part, 'capsule', a, b, r)


def sphere(owner, part, a, r):
    return Solid(owner, part, 'capsule', a, a, r)


def box(owner, part, lo, hi):
    return Solid(owner, part, 'box', lo, hi)


# ------------------------------------------------------------------------------------------------- distances
def _seg_seg(p1, q1, p2, q2):
    """The shortest distance between two segments (Ericson, Real-Time Collision Detection 5.1.9)."""
    d1, d2, r = q1 - p1, q2 - p2, p1 - p2
    a, e, f = d1 @ d1, d2 @ d2, d2 @ r
    if a < 1e-12 and e < 1e-12:
        return float(np.linalg.norm(r))
    if a < 1e-12:
        s, t = 0.0, min(1.0, max(0.0, f / e))
    else:
        c = d1 @ r
        if e < 1e-12:
            t, s = 0.0, min(1.0, max(0.0, -c / a))
        else:
            b = d1 @ d2
            den = a * e - b * b
            s = min(1.0, max(0.0, (b * f - c * e) / den)) if den > 1e-12 else 0.0
            t = (b * s + f) / e
            if t < 0:
                t, s = 0.0, min(1.0, max(0.0, -c / a))
            elif t > 1:
                t, s = 1.0, min(1.0, max(0.0, (b - c) / a))
    return float(np.linalg.norm((p1 + d1 * s) - (p2 + d2 * t)))


def _seg_box(p, q, lo, hi, n=12):
    """Distance from a segment to a box (sampled along the segment: plenty for people-sized things)."""
    best = 1e9
    for u in np.linspace(0, 1, n):
        x = p + (q - p) * u
        d = np.maximum(np.maximum(lo - x, 0), x - hi)
        best = min(best, float(np.linalg.norm(d)))
    return best


def overlap(s1, s2):
    """How far two solids pass into each other (metres; <= 0 means apart)."""
    if s1.kind == 'box' and s2.kind == 'box':
        d = np.minimum(s1.b, s2.b) - np.maximum(s1.a, s2.a)
        return float(d.min()) if (d > 0).all() else -1.0
    if s1.kind == 'box':
        s1, s2 = s2, s1
    if s2.kind == 'box':
        return s1.r - _seg_box(s1.a, s1.b, s2.a, s2.b)
    return s1.r + s2.r - _seg_seg(s1.a, s1.b, s2.a, s2.b)


# ------------------------------------------------------------------------------------------------- people
def person_solids(owner, j, X, Z, yaw=0.0, sp=None, sway_units=0.0):
    """A person's solids from their pose: j is views.py's joints (person units, x across, y down from the neck, z
    towards the way they face), standing on the floor at (X, Z), facing `yaw` (0 = towards us, 90 = to our right),
    drawn shifted across by sway_units (the dance's whole-body sway). Upper-body points take the pose's lean."""
    sp = sp or {}
    view, mirror = V.snap(yaw)
    a = math.radians(-view if mirror else view)
    bob = j.get('bob', 0.0)
    lean = j.get('lean', 0.0)

    def W(p3, upper=False):
        if upper:
            p3 = V.leaned(p3, lean)
        x, y, z = p3
        x += sway_units
        return (X + (x * math.cos(a) + z * math.sin(a)) * U, (SOLE - y - bob) * U,
                Z + (x * math.sin(a) - z * math.cos(a)) * U)
    out = []
    sw = sp.get('shoulders', 150)
    for dx in (-0.06, 0.06):                                 # the torso: two capsules side by side, shoulders to hips
        out.append(capsule(owner, 'body', np.add(W((0, 70, 0), True), (dx, 0, 0)), np.add(W((0, 440, 0)), (dx, 0, 0)),
                           min(0.13, sw * 0.6 * U)))
    hd = j.get('head_dy', 0.0) + sp.get('head_dy', 0.0)
    out.append(sphere(owner, 'head', W((sp.get('head_dx', 0.0), -150 + hd, 0), True), sp.get('hw', 70) * 0.95 * U))
    for side in 'LR':
        sh, el, wr = W(j['sh' + side], True), W(j['el' + side], True), W(j['wr' + side], True)
        out.append(capsule(owner, 'arm' + side, sh, el, 0.045))
        out.append(capsule(owner, 'forearm' + side, el, wr, 0.04))
        d = np.subtract(wr, el)
        n = float(np.linalg.norm(d)) or 1.0
        out.append(sphere(owner, 'hand' + side, np.add(wr, d / n * 12 * U), 0.045))
        hip, foot = W(j['hip' + side]), W(j['foot' + side])
        knee = W(V.knee_of(j, side))
        out.append(capsule(owner, 'thigh' + side, hip, knee, 0.065))
        out.append(capsule(owner, 'shin' + side, knee, foot, 0.05))
        toe = W(np.add(j['foot' + side], (0, 30, 80)))
        out.append(capsule(owner, 'foot' + side, foot, toe, 0.045))
    return out


# ------------------------------------------------------------------------------------------------- the checks
def _allowed(film, a, b, t):
    for oa, ob, t0, t1 in getattr(film, 'ALLOWED', ()):
        for x, y in ((a, b), (b, a)):
            if (x.owner == oa or repr(x) == oa) and (y.owner == ob or repr(y) == ob) and t0 <= t <= t1:
                return True
    return False


def solid_faults(film, times):
    """Pass-throughs: the first time each pair of owners overlaps (the parts and the depth named)."""
    faults, seen = [], set()
    for t in times:
        sols = film.solids(t)
        for i in range(len(sols)):
            for k in range(i + 1, len(sols)):
                a, b = sols[i], sols[k]
                if a.owner == b.owner:
                    continue
                key = tuple(sorted((a.owner, b.owner)))
                if key in seen:
                    continue
                o = overlap(a, b)
                if o > TOUCH and not _allowed(film, a, b, t):
                    seen.add(key)
                    faults.append(f'{t:.2f} s: {a!r} passes through {b!r} (by {o * 100:.0f} cm)')
    return faults


def order_faults(film, times, size=(540, 960)):
    """Drawing order: each item of film.scene(t) drawn alone; a later item must not cover an earlier, nearer one."""
    from PIL import Image
    faults, seen = [], set()
    for t in times:
        items = film.scene(t)
        alphas = []
        for name, depth, draw in items:
            lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
            draw(lay)
            alphas.append(np.asarray(lay.split()[3].resize(size)) > 128)
        for i in range(len(items)):
            for k in range(i + 1, len(items)):
                (na, da, _), (nb, db, _) = items[i], items[k]
                if na == nb or (na, nb) in seen:
                    continue
                if db > da + ORDER_TOL and (alphas[i] & alphas[k]).sum() > 40:
                    seen.add((na, nb))
                    faults.append(f'{t:.2f} s: {nb} (at {db:.2f} m) is drawn over {na} (nearer, at {da:.2f} m)')
    return faults


def run(film, step=1):
    fps = getattr(film, 'FPS', 12)
    t0, t1 = getattr(film, 'CLIP_SPAN', (0.0, getattr(film, 'DUR', 0.0)))
    times = [i / fps for i in range(int(t0 * fps), int(t1 * fps), step)]
    faults = solid_faults(film, times) if hasattr(film, 'solids') else []
    if hasattr(film, 'scene'):
        faults += order_faults(film, times[::3])
    if hasattr(film, 'in_shot_faults'):
        faults += film.in_shot_faults()
    return faults


if __name__ == '__main__':
    import burnham as B
    B.SS = 1
    film = importlib.import_module(sys.argv[1])
    f = run(film)
    print('\n'.join(f) if f else 'clip check: clean (nothing passes through anything)')
