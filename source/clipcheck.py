#!/usr/bin/env python3
"""clipcheck: nothing passes through anything, and nothing moves in a way a real thing can't (Sam, 18 Oct: 'a
generalised thorough system that catches clipping and objects sliding through each other, not piecemeal rules').
One shared check for every film, run by preflight.py before every animatic. A film opts in by defining any of:

  solids(t)   -> [Solid]: every person's parts (person_solids gives them from a views.py pose), every prop, piece of
                 furniture and flying thing, in metres (X across, + right; Y up from the floor; Z away from the camera)
  layers(t)   -> [(name, depth, draw)]: the things drawn as separate pieces, in the order the film draws them;
                 depth in metres from the camera, or (nearest, furthest) for something deep like a desk;
                 draw(img) paints one alone on a clear 1080 x 1920 layer
  ALLOWED     =  [(a, b, t0, t1)]: deliberate contacts (a hand on a desk, a punch landing); a/b = owner or owner.part
  IN_SHOT     =  [(name, t0, t1)]: a layer that must never touch the frame's edge in that time
  CONTACTS    =  [(a, b, t)]: the script says a hits b at t: they must touch then
  MOMENTUM    =  [(owner, t0, t1, min_speed)]: a stumble or fall that must keep moving (m/s along the floor)
  PUSHES      =  [(pusher, t, [owners])]: things knocked flying at t go the way the pusher was moving
  FAST_OK     =  [(owner.part, t0, t1)]: a deliberate whip-fast move (a slap) allowed past the speed limit
  CLIP_SPAN   =  (t0, t1): the stretch to check (default the whole film); SHOTS: no speed is judged across a cut

The checks:
1. Solids: no two solids of different owners overlap by more than TOUCH, unless the pair is ALLOWED then.
2. Drawing order: wherever two layers overlap on screen, the one drawn later must not be further away. And when two
   layers swap front and back between frames, they must be apart on screen in both frames (or a part jumps from
   behind to in front, or out from behind somebody to somewhere else, in one frame: Jenrick's arm and Farage, 18 Oct).
3. In shot: IN_SHOT layers never touch the frame's edge.
4. Movement: no part of a person moves faster than a real one can in one frame (a hand 12 m/s, anything else 7 m/s):
   anything faster has teleported. CONTACTS really touch. MOMENTUM never drops below its speed. PUSHES go the way
   they were pushed.

    python3 source/clipcheck.py FILM          run everything the film defines and list every fault
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
SOLE = 928.0                     # person units from the neck to the soles
TOUCH = 0.02                     # an overlap this small is a touch, not a pass-through
ORDER_TOL = 0.05                 # drawing order: depth differences smaller than this are side by side
SPEED = {'hand': 12.0, 'forearm': 10.0}      # m/s: the fastest a part can really move (others: 7)
SCREEN = (1080, 1920)


class Solid:
    """kind 'capsule' (a line from a to b, radius r; a sphere when a == b) or 'box' (corners a, b)."""
    def __init__(self, owner, part, kind, a, b, r=0.0):
        self.owner, self.part, self.kind, self.r = owner, part, kind, r
        self.a, self.b = np.asarray(a, float), np.asarray(b, float)

    @property
    def centre(self):
        return (self.a + self.b) / 2

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
    """How far two solids pass into each other (metres; <= 0 means apart, the gap between them)."""
    if s1.kind == 'box' and s2.kind == 'box':
        d = np.minimum(s1.b, s2.b) - np.maximum(s1.a, s2.a)
        return float(d.min())
    if s1.kind == 'box':
        s1, s2 = s2, s1
    if s2.kind == 'box':
        return s1.r - _seg_box(s1.a, s1.b, s2.a, s2.b)
    return s1.r + s2.r - _seg_seg(s1.a, s1.b, s2.a, s2.b)


# ------------------------------------------------------------------------------------------------- people
def person_solids(owner, j, X, Z, yaw=0.0, sp=None, roll=0.0):
    """A person's solids from their views.py pose: j is the joints (person units: x across, y down from the neck, z
    towards the way they face), with the dance's j['_sway'] (the whole body shifted across), j['bob'] (lowered) and
    j['lean'] (upper body tipped forward). They stand at (X, Z) on the floor, facing `yaw` (0 = towards us, 90 = to
    our right); roll tips the whole body sideways about the feet (degrees, + = top towards our left), as a film
    that rotates a falling person's layer does."""
    sp = sp or {}
    a = math.radians(yaw)
    bob, lean, sway = j.get('bob', 0.0), j.get('lean', 0.0), j.get('_sway', 0.0)
    rr = math.radians(roll)

    def W(p3, upper=False):
        if upper:
            p3 = V.leaned(p3, lean)
        x, y, z = p3
        x += sway
        dx, dy = (x * math.cos(a) + z * math.sin(a)) * U, (SOLE - y - bob) * U
        dx, dy = dx * math.cos(rr) - dy * math.sin(rr), dx * math.sin(rr) + dy * math.cos(rr)
        return np.array((X + dx, dy, Z + (x * math.sin(a) - z * math.cos(a)) * U))
    out = []
    for dx in (-60, 60):                                     # the torso: two capsules side by side, shoulders to hips
        out.append(capsule(owner, 'body', W((dx, 60, 0), True), W((dx * 0.8, 440, 0)), 0.11))
    hh = sp.get('hh', 90)
    out.append(sphere(owner, 'head', W((sp.get('head_dx', 0.0), -hh + j.get('head_dy', 0.0), 0), True),
                      sp.get('hw', 64) * U))
    for side in 'LR':
        sh, el, wr = W(j['sh' + side], True), W(j['el' + side], True), W(j['wr' + side], True)
        out.append(capsule(owner, 'arm' + side, sh, el, 0.045))
        out.append(capsule(owner, 'forearm' + side, el, wr, 0.04))
        d = wr - el
        out.append(sphere(owner, 'hand' + side, wr + d / (np.linalg.norm(d) or 1.0) * 0.02, 0.045))
        hip, foot = W(j['hip' + side]), W(j['foot' + side])
        knee = W(V.knee_of(j, side))
        out.append(capsule(owner, 'thigh' + side, hip, knee, 0.065))
        out.append(capsule(owner, 'shin' + side, knee, foot, 0.05))
        out.append(capsule(owner, 'foot' + side, foot, W(np.add(j['foot' + side], (0, 25, 90))), 0.04))
    return out


# ------------------------------------------------------------------------------------------------- the checks
def _match(s, name):
    return s.owner == name or repr(s) == name or (name.endswith('*') and repr(s).startswith(name[:-1]))


def _allowed(film, a, b, t):
    for oa, ob, t0, t1 in getattr(film, 'ALLOWED', ()):
        if t0 <= t <= t1 and ((_match(a, oa) and _match(b, ob)) or (_match(b, oa) and _match(a, ob))):
            return True
    return False


def _times(film, step=1):
    fps = getattr(film, 'FPS', 12)
    t0, t1 = getattr(film, 'CLIP_SPAN', (0.0, getattr(film, 'DUR', 0.0)))
    return [i / fps for i in range(int(round(t0 * fps)), int(round(t1 * fps)), step)], fps


def _shot(film, t):
    return next((s[0] for s in getattr(film, 'SHOTS', []) if s[1] <= t < s[2]), '')


def solid_faults(film, times):
    """Pass-throughs: the first time each pair of owners overlaps (the parts and how deep)."""
    faults, seen = [], set()
    for t in times:
        sols = film.solids(t)
        for i in range(len(sols)):
            for k in range(i + 1, len(sols)):
                a, b = sols[i], sols[k]
                key = tuple(sorted((a.owner, b.owner)))
                if a.owner == b.owner or key in seen:
                    continue
                o = overlap(a, b)
                if o > TOUCH and not _allowed(film, a, b, t):
                    seen.add(key)
                    faults.append(f'{t:.2f} s: {a!r} passes through {b!r} (by {o * 100:.0f} cm)')
    return faults


def motion_faults(film, times, fps):
    """Teleports (a part faster than it can move), contacts that never touch, stumbles that stop, pushes the wrong way."""
    faults, seen = [], set()
    prev, prev_t = None, None
    track = {}
    for t in times:
        sols = {repr(s): s for s in film.solids(t)}
        for nm, s in sols.items():
            track.setdefault(s.owner, {})[t] = s
        if prev is not None and _shot(film, t) == _shot(film, prev_t):
            for nm, s in sols.items():
                p = prev.get(nm)
                if p is None or s.kind == 'box':
                    continue
                v = float(np.linalg.norm(s.centre - p.centre)) * fps
                lim = SPEED.get(s.part.rstrip('LR'), 7.0)
                fast_ok = any(_match(s, n) and t0 <= t <= t1 for n, t0, t1 in getattr(film, 'FAST_OK', ()))
                if v > lim and not fast_ok and nm not in seen:
                    seen.add(nm)
                    faults.append(f'{t:.2f} s: {nm} jumps {v / fps * 100:.0f} cm in one frame ({v:.0f} m/s: it has '
                                  f'teleported; add in-between poses or slow the move)')
        prev, prev_t = sols, t
    for a, b, t in getattr(film, 'CONTACTS', ()):
        sols = film.solids(t)
        A = [s for s in sols if _match(s, a)]
        Bs = [s for s in sols if _match(s, b)]
        best = max((overlap(x, y) for x in A for y in Bs), default=-1.0)
        if best < -TOUCH:
            faults.append(f'{t:.2f} s: {a} should hit {b} but stops {-best * 100:.0f} cm short')

    def body_xz(owner, t):
        s = [x for x in film.solids(t) if x.owner == owner and x.part == 'body']
        return np.mean([x.centre[[0, 2]] for x in s], axis=0) if s else None
    for owner, t0, t1, vmin in getattr(film, 'MOMENTUM', ()):
        ts = [x for x in np.arange(t0, t1, 1 / fps)]
        for ta, tb in zip(ts, ts[1:]):
            pa, pb = body_xz(owner, ta), body_xz(owner, tb)
            v = float(np.linalg.norm(pb - pa)) * fps
            if v < vmin:
                faults.append(f'{ta:.2f} s: {owner} slows to {v:.2f} m/s (should keep moving: at least {vmin} m/s; '
                              f'he steadies himself)')
                break
    for pusher, t, owners in getattr(film, 'PUSHES', ()):
        pa, pb = body_xz(pusher, t - 2 / fps), body_xz(pusher, t)
        push = pb - pa
        for o in owners:
            s0 = [x for x in film.solids(t + 1 / fps) if x.owner == o]
            s1 = [x for x in film.solids(t + 3 / fps) if x.owner == o]
            if s0 and s1:
                go = (s1[0].centre - s0[0].centre)[[0, 2]]
                if float(go @ push) < 0:
                    faults.append(f'{t:.2f} s: {o} flies against the way {pusher} pushed it')
    return faults


def _alpha(draw, size=(270, 480)):
    from PIL import Image
    lay = Image.new('RGBA', SCREEN, (0, 0, 0, 0))
    draw(lay)
    bb = lay.getbbox()
    return np.asarray(lay.split()[3].resize(size)) > 100, bb


def order_faults(film, times, fps):
    """Drawing order on screen, and swaps front to back that make a part jump between frames."""
    faults, seen = [], set()
    prev = None
    cache = {}

    def masks(t):
        if t not in cache:
            cache[t] = {name: (depth, _alpha(draw)) for name, depth, draw in film.layers(t)}
        return cache[t]
    for n, t in enumerate(times):
        items = film.layers(t)
        order = {name: i for i, (name, _, _) in enumerate(items)}
        rng = {name: (d, d) if isinstance(d, (int, float)) else tuple(d) for name, d, _ in items}
        depth = {name: (r[0] + r[1]) / 2 for name, r in rng.items()}
        if prev is not None and _shot(film, t) == _shot(film, prev[0]):
            pt, pdepth, prng = prev

            def rel(r, a, b):          # -1: a wholly nearer than b; +1: wholly further; 0: side by side in depth
                return -1 if r[a][1] < r[b][0] else (1 if r[a][0] > r[b][1] else 0)
            for a in depth:
                for b in depth:
                    if a >= b or a not in pdepth or b not in pdepth or (a, b, 'swap') in seen:
                        continue
                    if rel(prng, a, b) * rel(rng, a, b) < 0:                    # they swapped front and back
                        # the one that moved the most must not be hidden behind the other on the frame where it is
                        # the further of the two: coming forward it would jump out from behind; going back it would
                        # vanish behind in one frame
                        mv, ot = (a, b) if abs(depth[a] - pdepth[a]) >= abs(depth[b] - pdepth[b]) else (b, a)
                        tt = pt if pdepth[mv] > pdepth[ot] else t
                        m = masks(tt)
                        if (m[a][1][0] & m[b][1][0]).sum() > 6:
                            seen.add((a, b, 'swap'))
                            faults.append(f'{t:.2f} s: {mv} passes {ot} while partly hidden behind them on screen (a '
                                          f'part jumps out from behind, or vanishes, in one frame): keep them apart on '
                                          f'screen as they pass')
        if n % 3 == 0:                                       # the order itself, on every 3rd frame
            m = masks(t)
            for a in depth:
                for b in depth:
                    if order[a] < order[b] and rng[b][0] > rng[a][1] + ORDER_TOL and (a, b) not in seen:
                        if (m[a][1][0] & m[b][1][0]).sum() > 6:
                            seen.add((a, b))
                            faults.append(f'{t:.2f} s: {b} ({rng[b][0]:.2f} m away) is drawn over {a} '
                                          f'({rng[a][1]:.2f} m, nearer)')
        prev = (t, depth, rng)
        for old in [k for k in cache if k < t - 1.5 / fps]:
            del cache[old]
    return faults


def in_shot_faults(film):
    faults = []
    fps = getattr(film, 'FPS', 12)
    for name, t0, t1 in getattr(film, 'IN_SHOT', ()):
        for i in range(int(round(t0 * fps)), int(round(t1 * fps))):
            t = i / fps
            for nm, depth, draw in film.layers(t):
                if nm != name:
                    continue
                _, bb = _alpha(draw)
                if bb and (bb[0] <= 0 or bb[1] <= 0 or bb[2] >= SCREEN[0]):   # (the bottom edge may cut off legs)
                    faults.append(f'{t:.2f} s: {name} touches the edge of the frame {bb}')
                    break
            else:
                continue
            break
    return faults


def run(film):
    times, fps = _times(film)
    faults = []
    if hasattr(film, 'solids'):
        faults += solid_faults(film, times) + motion_faults(film, times, fps)
    if hasattr(film, 'layers'):
        faults += order_faults(film, times, fps)
    faults += in_shot_faults(film)
    return faults


if __name__ == '__main__':
    import burnham as B
    B.SS = 1
    film = importlib.import_module(sys.argv[1])
    f = run(film)
    print('\n'.join(f) if f else 'clip check: clean (nothing passes through anything; nothing teleports)')
