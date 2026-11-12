#!/usr/bin/env python3
"""kitchecks: the checks that used to live in one film's file, moved into the shared kit (guides/film-quality-rules.md,
rule 13). Pre-flight runs every one on every film; each says out loud when a film lacks what it needs.

Why: Poker Mon's contact check was never copied into Prepper Minister, so the bean tin slid with no hand on it (note
60); Prepper's facing, marks and crockery checks would have been lost the same way on the next film.

From what the audit already sees (scene(t) and the set; run inside audit.py's pass over every frame):
  touches     TOUCHES = [(hand, thing, t0, t1, why)]: the hand ('Andy.handR', * wildcards) is on the thing
              (within 3 cm) on every frame of the span, and (with a 3D camera) seen: nothing else stands between it
              and the lens (Poker Mon: the pot pulled with no hand on it; hands hidden under the table)
  held        a prop that moves (a thing of its own, not a person or the set) has a hand on it, unless
              FREE_MOVES = [(thing, t0, t1, why)] says it flies, falls or slides (Poker Mon: the pot slid by itself)
  resting     a hand held still for half a second keeps 3 cm clear of everything it is not meant to touch
              (TOUCHES, ALLOWED_CONTACTS) (Poker Mon: the resting hand in the chip stacks)
  rests       RESTS = [(forearm, surface, t0, t1, why)] (rule 78), copied from the arms the film's notes list as
              resting: the forearm ('Andy.forearmL', * wildcards) and its elbow never go more than 1 cm below the
              surface (a thing's name: 'desk'), the elbow lies on it (no more than 3 cm above) and over it (not off
              its edge). Flat films test the same list on the drawing (below)
From the drawing (pre-flight's pass over every 3rd frame; every views.py person drawn is logged):
  facing      a head turned no more than 95 degrees from its body; seen from behind, nothing held out in front
              drawn over the back (Prepper notes 11, 12, 16)
  copies      no two people in one frame drawn from one copy (Job K, Sam: Y, 10 Nov; the crowds-from-behind rule made
              automatic): the same build, height, hair, skin and clothes is flagged; meant copies (twins, a reflection)
              in the film's COPIES_OK = [(name, name, why)]. The fix: each one a different build, height and kit detail
  rests       rule 78 for flat films: each RESTS arm, as drawn, against 'desk' (the sitting kit's desk in the
              pose), 'armrest', 'seat' or a number (a height above the floor, person units: Ad-Vanced Notice's
              painted desk is 500): the forearm and elbow never more than 4 units (about 1 cm) below the surface,
              the elbow on it (no more than 12 units above) and, on a desk, over its top. An arm the sitting kit
              poses resting that RESTS leaves out is named, so it is never left unchecked in silence
From the film's lists:
  marks       all_marks() -> [dict(at=(x, y, z), t=, kind=)]: every bullet hole and scorch on a real surface (a
              wall, a thing, the floor or ceiling of a room), never in an opening (Prepper note 18)
  sounds      sound_events() -> [(name, at, ...)] and SOUND_SOURCES = {name: (x, y, z) or fn(t)}: a sound tied to
              a thing plays only with it in frame, once per hit (never doubled) (Prepper note 23)

    python3 source/kitchecks.py FILM        every check (draws every 2nd frame for the facing check: minutes)
"""
import fnmatch
import importlib
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CLEAR = 0.03                  # metres: a hand on a thing is within this; a resting hand keeps at least this clear
STILL = 0.01                  # metres a frame: a hand moving less than this is resting
REST = 0.5                    # seconds still before a hand counts as resting
MOVED = 0.002                 # metres a frame: a prop moving more than this is moving
MAX_TURN = 95                 # degrees: a head turned further from its body looks backwards
SINK = 0.01                   # metres: a resting forearm or elbow this far below its surface has sunk into it (rule 78)
SINK_U = 4.0                  # the same in person units (flat films; about 1 cm)
FLOAT_U = 12.0                # person units: a resting elbow further above its surface than this is not resting on it
SURFACES = ('desk', 'armrest', 'seat')   # flat films' surfaces, found in the pose (a number: a height above the floor)


def _flat_surface(x):
    return isinstance(x, (int, float)) or x in SURFACES


def _hit(pattern, thing, part=None):
    return fnmatch.fnmatchcase(thing, pattern) or (part is not None and fnmatch.fnmatchcase(f'{thing}.{part}', pattern))


def _in(t, t0, t1):
    return (t0 is None or t >= t0) and (t1 is None or t <= t1)


def _figure(th):
    """A person or creature (or the part of one in shot: a hand), not a prop."""
    return any(s.part in ('body', 'torso', 'head', 'legs', 'hips') or s.part.startswith('hand') for s in th.solids)


def _hands(th):
    return [s for s in th.solids if s.part.startswith('hand')]


def _gap(sol, th):
    """The nearest a solid comes to a thing (metres; negative: inside it)."""
    import clipcheck as CC
    lo, hi = CC.bounds(sol)
    m = np.all((th.slo < hi + 0.2) & (th.shi > lo - 0.2), axis=1)
    return min([-CC.overlap(sol, s) for s, k in zip(th.solids, m) if k] or [9.0])


class SceneChecks:
    """touches, held and resting, fed one frame at a time by audit.run (things: {name: Thing}, cam)."""
    def __init__(self, film):
        self.film = film
        self.touches = list(getattr(film, 'TOUCHES', ()))
        self.free = list(getattr(film, 'FREE_MOVES', ()))
        self.rests = [r for r in getattr(film, 'RESTS', ()) if not _flat_surface(r[1])]
        self.fps = film.FPS
        self.found = {}                    # (kind, names) -> [(t, text)]
        self.last_props = {}               # prop name -> (frame, pos)
        self.hand_track = {}               # (thing, part) -> [frame, pos, still since]
        self._boxes = None

    def _fault(self, kind, names, t, text):
        self.found.setdefault((kind, names), []).append((t, text))

    def _allowed(self, a, pa, b, t):
        for ent in self.touches:
            if _in(t, ent[2], ent[3]) and _hit(ent[0], a, pa) and _hit(ent[1], b):
                return True
        for ent in getattr(self.film, 'ALLOWED_CONTACTS', ()):
            x, y, t0, t1 = ent[:4]
            if _in(t, t0, t1) and ((_hit(x, a, pa) and _hit(y, b)) or (_hit(y, a, pa) and _hit(x, b))):
                return True
        return False

    def _near(self, things, lo, hi, pad):
        """The things whose boxes come within `pad` of the box lo-hi (one array test, not one per thing)."""
        if self._boxes is None:
            names = list(things)
            self._boxes = (names, np.array([things[n].lo for n in names]), np.array([things[n].hi for n in names]))
        names, L, H = self._boxes
        if not names:
            return []
        m = np.all((L < hi + pad) & (H > lo - pad), axis=1)
        return [names[k] for k in np.nonzero(m)[0]]

    def frame(self, i, t, shot, things, cam):
        self._boxes = None
        # touches: the hand on the thing, and seen
        for hand, target, t0, t1, why, *_ in self.touches:
            if not _in(t, t0, t1):
                continue
            hs = [(n, s) for n, th in things.items() for s in _hands(th) if _hit(hand, n, s.part)]
            ts = [th for n, th in things.items() if _hit(target, n)]
            if not hs or not ts:
                self._fault('untested', (hand, target), t, f'{t:.2f} s ({shot}): the touch check found no {hand} or no {target} '
                                                            f'in the scene, so it checked NOTHING (TOUCHES: {why}). Look at this '
                                                            f'moment by eye at full size, or fix the name, before the animatic')
                continue
            gap = min(_gap(s, th) for _, s in hs for th in ts if th.name != _)
            if gap > CLEAR:
                self._fault('touch', (hand, target), t, f'{t:.2f} s ({shot}): {hand} is {gap * 100:.0f} cm off '
                                                        f'{target} (TOUCHES: {why})')
            elif hasattr(cam, 'pos'):
                n, s = min(hs, key=lambda q: min(_gap(q[1], th) for th in ts))
                hider = self._hidden(s, n, ts, things, cam)
                if hider:
                    self._fault('hidden', (hand, target), t, f'{t:.2f} s ({shot}): {hand} on {target} is hidden '
                                                             f'behind {hider} (TOUCHES: {why})')
        # held: a prop that moves has a hand on it
        for n, th in things.items():
            if th.kind == 'set' or _figure(th):
                continue
            prev = self.last_props.get(n)
            self.last_props[n] = (i, th.pos)
            if not prev or prev[0] != i - 1 or np.linalg.norm(th.pos - prev[1]) < MOVED:
                continue
            if any(fnmatch.fnmatchcase(n, f[0]) and _in(t, f[1], f[2]) for f in self.free):
                continue
            near = [o for o in self._near(things, th.lo, th.hi, CLEAR) if o != n and
                    any(_gap(s, th) <= CLEAR for s in _hands(things[o]))]
            if not near:
                self._fault('held', (n,), t, f'{t:.2f} s ({shot}): {n} moves with no hand on it (list it in '
                                             f'FREE_MOVES if it flies, falls or slides)')
        # resting: a hand held still keeps clear of what it is not meant to touch
        for n, th in things.items():
            hands = _hands(th)
            if not hands:
                continue
            for s in hands:
                key = (n, s.part)
                c = (s.a + s.b) / 2
                tr = self.hand_track.get(key)
                if tr and tr[0] == i - 1 and np.linalg.norm(c - tr[1]) < STILL:
                    since = tr[2]
                else:
                    since = t
                self.hand_track[key] = [i, c, since]
                if t - since < REST:
                    continue
                import clipcheck as CC
                slo, shi = CC.bounds(s)
                for o in self._near(things, slo, shi, CLEAR):
                    if o == n:
                        continue
                    g = _gap(s, things[o])
                    if -0.02 < g < CLEAR and not self._allowed(n, s.part, o, t):
                        self._fault('resting', (f'{n}.{s.part}', o), t,
                                    f'{t:.2f} s ({shot}): {n}\'s resting {s.part} sits {max(g, 0) * 100:.0f} cm from '
                                    f'{o} (keep 3 cm clear, or list the touch in TOUCHES)')

        # rests (rule 78): a listed resting forearm and elbow never below the surface, the elbow on it and over it
        for arm, surf, t0, t1, why, *_ in self.rests:
            if not _in(t, t0, t1):
                continue
            fs = [(n, s) for n, th in things.items() for s in th.solids
                  if s.part.startswith('forearm') and _hit(arm, n, s.part)]
            ts = [th for n, th in things.items() if _hit(surf, n)]
            if not fs or not ts:
                self._fault('untested', ('RESTS', arm, surf), t,
                            f'{t:.2f} s ({shot}): the resting-arm check found no {arm} or no {surf} in the scene, so '
                            f'it checked NOTHING (RESTS: {why}). Look at this moment by eye at full size, or fix '
                            f'the name, before the animatic')
                continue
            for n, s in fs:
                deep, top_el = self._under(s, ts)
                if deep > SINK:
                    self._fault('rests', (f'{n}.{s.part}', surf), t,
                                f'{t:.2f} s ({shot}): {n}\'s resting {s.part} goes {deep * 100:.0f} cm below the '
                                f'top of {surf} (rule 78: never below the surface; RESTS: {why})')
                if top_el is None:
                    self._fault('rests', (f'{n}.{s.part}', surf, 'off'), t,
                                f'{t:.2f} s ({shot}): {n}\'s resting elbow ({s.part}) is off the edge of {surf}, '
                                f'with nothing under it (rule 78; RESTS: {why})')
                elif s.a[1] - s.r - top_el > CLEAR:
                    self._fault('rests', (f'{n}.{s.part}', surf, 'up'), t,
                                f'{t:.2f} s ({shot}): {n}\'s resting elbow ({s.part}) floats '
                                f'{(s.a[1] - s.r - top_el) * 100:.0f} cm above {surf} (rule 78: the weight on it; '
                                f'RESTS: {why})')

    @staticmethod
    def _under(s, surfaces):
        """How far a forearm capsule (a: the elbow, b: the wrist; y up) goes below the top of the surfaces' solids
        under it (metres, 0 if never), and the top under the elbow (None: nothing under it)."""
        import clipcheck as CC
        L = float(np.linalg.norm(s.b - s.a))
        n = max(2, int(L / 0.02) + 1)
        deep, top_el = 0.0, None
        for k in range(n):
            p = s.a + (s.b - s.a) * (k / (n - 1))
            for th in surfaces:
                for lo, hi in zip(th.slo, th.shi):
                    if lo[0] <= p[0] <= hi[0] and lo[2] <= p[2] <= hi[2]:
                        deep = max(deep, hi[1] - (p[1] - s.r))
                        if k == 0:
                            top_el = hi[1] if top_el is None else max(top_el, hi[1])
        return deep, top_el

    def _hidden(self, s, owner, targets, things, cam):
        """What stands between a hand and the lens (a 3D camera), or None."""
        import clipcheck as CC
        c = (s.a + s.b) / 2
        d = np.asarray(cam.pos, float) - c
        L = float(np.linalg.norm(d))
        if L < 0.1:
            return None
        u = d / L
        pts = [c + u * x for x in np.arange(0.07, L - 0.05, 0.03)]
        if not pts:
            return None
        P = np.array(pts)
        plo, phi = P.min(0), P.max(0)
        for n, th in things.items():
            for sol, lo, hi in zip(th.solids, th.slo, th.shi):
                if n == owner and (sol.part.startswith(('hand', 'forearm', 'arm')) or sol is s):
                    continue
                if np.any(hi < plo) or np.any(lo > phi):
                    continue
                inside = P[np.all((P > lo) & (P < hi), axis=1)]
                for p in inside[::2]:
                    if CC.overlap(CC.sphere('_', '_', p, 0.004), sol) > 0.001:
                        return f'{n}.{sol.part}' if n == owner else n
        return None

    def faults(self):
        """One fault per kind and pair (audit.py's form): the first moment, and how long it lasts."""
        out = []
        for (kind, names), hs in self.found.items():
            ts = [h[0] for h in hs]
            span = f'{len(hs)} frames, to {max(ts):.2f} s' if len(hs) > 1 else 'one frame'
            out.append(dict(what=kind, t=ts[0], names=names, text=f'{hs[0][1]} ({span})'))
        return out


# ------------------------------------------------------------------------------------------------ from the drawing
DRAWN = []                    # every views.py person drawn since install(): (where, name, drawn dict)
POSES = []                    # everyone drawn holding something: (where, name, sp, joints, t), for viewchecks' turn test


_INSTALLED = []


def install():
    """Log every views.py person drawn (their view, head turn and what they hold), for facing(). Patches views.person
    and every module that took its own name for it."""
    import views
    if getattr(views.person, '_logged', False) or _INSTALLED:
        return
    _INSTALLED.append(1)
    real = views.person

    def person(img, cam, x, y, s, sp, t, yaw, joints=None, head_yaw=None, tilt=None):   # tilt: a 3D camera's
        j2 = real(img, cam, x, y, s, sp, t, yaw, joints, head_yaw, tilt=tilt)            # real tilt (Patriots 3)
        try:
            import figure as F
            where, ft = F.CONTEXT.get('where', ''), F.CONTEXT.get('t')
        except Exception:
            where, ft = '', None
        if isinstance(j2, dict) and '_drawn' in j2:
            d = dict(j2['_drawn'])
            r = _rest_record(joints, t)
            if r:
                d['_rest'] = r            # rule 78: the arms' heights against the surfaces in the pose (rests())
            if ft is not None:
                d['_t'] = ft              # the film's time (pre-flight's drawing pass), for cut_rests and faces
            d['_look'] = look(sp)
            d['_who'] = sp.get('who')     # waivers.unseen_faults: CAST keys
            DRAWN.append((where, sp.get('name', 'someone'), d))
        if joints and joints.get('props'):
            POSES.append((where, sp.get('name', 'someone'), sp, joints, t))
        return j2
    person._logged = True
    for m in list(sys.modules.values()):
        try:
            for k, v in list(vars(m).items()):
                if v is real:
                    setattr(m, k, person)
        except TypeError:
            continue


def facing(records):
    """Rule 13 (Prepper notes 11, 12, 16): from DRAWN records, a head turned past 95 degrees from its body, or a held
    thing drawn over someone's back."""
    out, seen = [], set()
    for where, name, d in records:
        turn = abs((d['head_yaw'] - d['yaw'] + 180) % 360 - 180)
        if turn > MAX_TURN and (name, 'turn') not in seen:
            seen.add((name, 'turn'))
            out.append(f'FACING: {where}: {name}\'s head turned {turn:.0f} degrees from the body (first of these)')
        if d.get('held_over_back') and (name, 'back') not in seen:
            seen.add((name, 'back'))
            out.append(f'FACING: {where}: seen from behind, what {name} holds is drawn over the back (first of these)')
    return out


LOOK_KEYS = ('height', 'shoulders', 'hw', 'hh', 'leg_k', 'skin', 'hair', 'hair_c', 'beard', 'beard_c', 'outfit',
             'jacket', 'sleeve', 'trousers', 'shirt', 'tie', 'shoe', 'dress', 'who')


def look(sp):
    """What someone looks like, as one string (everything that tells two people apart at a glance; not the name)."""
    return repr(tuple((k, sp.get(k)) for k in LOOK_KEYS))


def copies(film, records):
    """Job K (Sam: Y, 10 Nov): two people in one frame with the same look are one copy pasted twice (the ICE
    officers' identical vests, builds and masks). Once per pair of names."""
    ok = {frozenset(r[:2]) for r in getattr(film, 'COPIES_OK', [])}
    frames, out, seen = {}, [], set()
    for where, name, d in records:
        if d.get('_look'):
            frames.setdefault(where, []).append((name, d['_look']))
    for where, ppl in frames.items():
        for i, (a, la) in enumerate(ppl):
            for b, lb in ppl[i + 1:]:
                pair = frozenset((a, b))
                if la == lb and pair not in ok and (len(pair) == 2 or a == b) and (a, b) not in seen:
                    seen.add((a, b))
                    out.append(f"COPIES: {where}: {a} and {b} are drawn from one copy (same build, height, hair and "
                               f"clothes): give each a different build, height and kit detail, or list them in "
                               f"COPIES_OK (first of these)")
    return out


def _rest_record(j, t):
    """For rests(): where each elbow and wrist is (body frame, y down, after the lean) and the tops of the surfaces
    the pose knows of (the sitting kit's desk, armrests, seat), as plain numbers (pre-flight's workers send them back).
    None for a pose with no arms to test."""
    if not isinstance(j, dict) or not all(k in j for k in ('elL', 'wrL', 'elR', 'wrR')):
        return None
    try:
        import views as V
        import sitting as SK
        lean, bob = j.get('lean', 0.0) or 0.0, j.get('bob', 0.0) or 0.0
        rec = dict(t=t, bob=bob, floor=SK.FLOOR, arms={}, tops={}, posed={}, on_desk={})
        for s in 'LR':
            rec['arms'][s] = (tuple(V.leaned(j['el' + s], lean)), tuple(V.leaned(j['wr' + s], lean)))
            if 'sh' + s in j:                            # the shoulder too (cut_rests: how far from hanging at rest)
                rec.setdefault('sh', {})[s] = tuple(V.leaned(j['sh' + s], lean))
        seat = j.get('seat')
        if seat is not None:
            rec['tops']['seat'] = SK.FLOOR - seat.h - bob
            if getattr(seat, 'arms', None):
                rec['tops']['armrest'] = SK.FLOOR - seat.h - bob - seat.arms
            desk = getattr(seat, 'desk', None)
            if desk is not None:
                rec['tops']['desk'] = desk.surface(bob)
                _, inv = desk.xf(j)
                for s in 'LR':                           # the elbow over the desk's top, not off its edge
                    x, _, z = inv(*rec['arms'][s][0])
                    rec['on_desk'][s] = abs(x) <= desk.width and desk.front <= z <= desk.front + desk.depth
        for s, a in ((j.get('spec') or {}).get('arms') or {}).items():
            if a and (a.get('rest') is not None or a.get('elbow_rest') is not None):
                rec['posed'][s] = True                   # the kit posed this forearm resting on something
        return rec
    except Exception:
        return None


def rests(film, records):
    """Rule 78 on flat films, from DRAWN records: each RESTS arm whose surface is 'desk', 'armrest', 'seat' or a
    height (person units above the floor): its forearm and elbow never below the surface, the elbow on it and (a
    desk) over it. An arm the sitting kit posed resting that RESTS leaves out is named."""
    listed = [r for r in getattr(film, 'RESTS', ()) if _flat_surface(r[1])]
    found, seen, unlisted = {}, set(), {}
    cm = lambda u: u * _unit_m() * 100
    for where, name, d in records:
        r = d.get('_rest')
        if not r:
            continue
        t = r['t']
        where = where or f'{t:.2f} s'
        for s in 'LR':
            covered = [e for e in listed if _in(t, e[2], e[3]) and _hit(e[0], name, 'forearm' + s)]
            if r['posed'].get(s) and not covered and not any(
                    _in(t, e[2], e[3]) and _hit(e[0], name, 'forearm' + s) for e in getattr(film, 'RESTS', ())):
                unlisted.setdefault((name, s), where)
            for arm, surf, t0, t1, why, *_ in covered:
                seen.add((arm, surf, t0, t1))
                top = (r['floor'] - surf - r['bob']) if isinstance(surf, (int, float)) else r['tops'].get(surf)
                if top is None:
                    found.setdefault(('none', name, s, surf), []).append(
                        (t, f'{where}: the resting-arm check found no {surf} in {name}\'s pose, so it checked '
                            f'NOTHING (RESTS: {why}). Give the height as a number, or check by eye at full size'))
                    continue
                import sitting as SK
                line = top - SK.SLEEVE                   # where a forearm's centre line lies when it rests on it
                el, wr = r['arms'][s]
                deep = max(el[1], wr[1]) - line          # y is down: more is lower
                if deep > SINK_U:
                    part = 'elbow' if el[1] >= wr[1] else 'wrist end of the forearm'
                    found.setdefault(('below', name, s, surf), []).append(
                        (t, f'{where}: {name}\'s resting {s} {part} goes {cm(deep):.0f} cm below the {surf} top '
                            f'(rule 78: never below the surface; RESTS: {why})'))
                if line - el[1] > FLOAT_U:
                    found.setdefault(('up', name, s, surf), []).append(
                        (t, f'{where}: {name}\'s resting {s} elbow floats {cm(line - el[1]):.0f} cm above the '
                            f'{surf} (rule 78: the weight on it; RESTS: {why})'))
                if surf == 'desk' and r['on_desk'].get(s) is False:
                    found.setdefault(('off', name, s, surf), []).append(
                        (t, f'{where}: {name}\'s resting {s} elbow is off the desk\'s edge, with nothing under it '
                            f'(rule 78; RESTS: {why})'))
    out = []
    for hs in found.values():
        span = f'{len(hs)} frames, to {max(h[0] for h in hs):.2f} s' if len(hs) > 1 else 'one frame'
        out.append(f'RESTS: {hs[0][1]} ({span})')
    if not hasattr(film, 'scene'):                       # a 3D film's scene checks test its own entries
        for arm, surf, t0, t1, why, *_ in listed:
            if (arm, surf, t0, t1) not in seen:
                out.append(f'RESTS: COULD NOT TEST: no drawn frame between {t0} and {t1} s showed {arm} in a pose '
                           f'the check can read, so it checked NOTHING (RESTS: {why}). Fix the name, or look by eye '
                           f'at full size before the animatic')
    for (name, s), where in unlisted.items():
        out.append(f'RESTS: {where}: {name}\'s {s} forearm is posed resting on a surface, but RESTS does not list '
                   f'it, so nothing checks it never sinks (rule 78): copy it in from the film\'s notes (first of these)')
    return out


def _unit_m():
    import views as V
    return V.M_PER_UNIT


# ------------------------------------------------------------------------------------------------ from the lists
def marks(film):
    """Every mark (bullet hole, scorch) sits on a real surface: within 3 cm of a wall piece or a THING, or on a room's
    floor or ceiling; never in an opening (Prepper note 18)."""
    if not hasattr(film, 'all_marks'):
        return []
    import clipcheck as CC
    import plan as PLN
    import sets
    P = PLN.of(film)
    if P is None:
        return ['MARKS: the film has marks but no PLAN to put them on']
    out = []
    static = sets.solids(film, 0.0)
    for m in film.all_marks():
        p = np.asarray(m['at'], float)
        room = P.room_of(p[0], p[2], 0.02)
        on_floor = room is not None and (abs(p[1]) < 0.02 or abs(p[1] - P.ceil) < 0.02)
        probe = CC.sphere('_', '_', p, CLEAR)
        on_thing = any(CC.overlap(probe, s) > 0 for th in static for s in th.solids)
        if not (on_floor or on_thing):
            out.append(f"MARKS: {m.get('t', 0):.2f} s: a {m.get('kind', 'mark')} at ({p[0]:.2f}, {p[1]:.2f}, "
                       f"{p[2]:.2f}) is on no surface (in an opening, or in mid-air)")
    return out


def sounds(film):
    """A sound tied to a thing (SOUND_SOURCES) plays only with the thing in frame, and once per hit (Prepper note 23)."""
    src = getattr(film, 'SOUND_SOURCES', None)
    if not src or not hasattr(film, 'sound_events'):
        return []
    import audit as A
    out = []
    ev = sorted((e[1], e[0]) for e in film.sound_events() if e[0] in src)
    for (ta, na), (tb, nb) in zip(ev, ev[1:]):
        if na == nb and tb - ta < 0.1:
            out.append(f'SOUNDS: {ta:.2f} s and {tb:.2f} s: the {na} sound twice for one hit')
    for at, name in ev:
        p = src[name](at) if callable(src[name]) else src[name]
        pr = A._project(film, film.cam_for(at), np.asarray(p, float)[None])
        if pr is not None and not (pr[2][0] > 0.3 and 60 < pr[0][0] < 1020 and 60 < pr[1][0] < 1860):
            out.append(f'SOUNDS: {at:.2f} s: the {name} sound plays with what makes it out of frame')
    return out


def run(film, drawn=None):
    """The list checks, and the facing check on drawing records (pre-flight passes its own; else every 2nd frame is
    drawn here). The scene checks run inside audit.run."""
    if drawn is None:
        install()
        import figure as F
        B = getattr(film, 'B', None)
        if B is not None:
            B.SS = 1
        n0 = len(DRAWN)
        draw = getattr(film, 'picture', None) or film.frame_image
        for i in range(0, int(getattr(film, 'BLACK_AT', film.DUR) * film.FPS), 2):
            t = i / film.FPS
            shot = next((s[0] for s in film.SHOTS if s[1] <= t < s[2]), '')
            F.CONTEXT['where'] = f'{shot} {t:.2f}s'
            F.CONTEXT['t'] = t
            draw(t)
        drawn = DRAWN[n0:]
    return (facing(drawn) + rests(film, drawn) + cut_rests(film, drawn) + faces(film, drawn) + marks(film) +
            sounds(film))



# ------------------------------------------------------------------------------------------------ cuts and faces (Job L)
CUT_TAIL = 0.4          # rule 72: no pose returns to rest in the last 0.4 s before a cut
NEAR_REST, FAR_REST = 0.2, 0.45   # wrist from its hanging place, in arm lengths: at rest / clearly posed


def _rest_gap(r, s):
    """How far an arm's wrist is from where it hangs at rest (views.standing), in arm lengths; None if unknown."""
    sh = (r.get('sh') or {}).get(s)
    if sh is None:
        return None
    import figure as Fg
    sg = -1 if s == 'L' else 1
    up = np.array((sg * 0.12, 0.99, -0.04)); up /= np.linalg.norm(up)
    fo = np.array((sg * -0.04, 0.99, 0.13)); fo /= np.linalg.norm(fo)
    rest = np.array(sh) + up * Fg.UPPER * 0.98 + fo * Fg.FORE * 0.98
    return float(np.linalg.norm(np.array(r['arms'][s][1]) - rest) / (Fg.UPPER + Fg.FORE))


def cut_rests(film, records):
    """Rule 72 (Job L; was by hand on the check sheet): from the drawing pass, a standing person's arm that is clearly
    posed (wrist over FAR_REST arm lengths from hanging) and then hangs at rest (under NEAR_REST) within the last
    CUT_TAIL s of a shot: the shot shows the pose dropping back; cut before the return. People seated (their pose
    knows a seat or desk) are left out: their rest is on the lap or desk. CUT_RESTS_OK = [(name, shot, why)] lets one
    through (a shrug meant to land)."""
    shots = getattr(film, 'SHOTS', [])
    ok = [(n, sh) for n, sh, *_ in getattr(film, 'CUT_RESTS_OK', ())]
    seen = {}
    for where, name, d in records:
        r, t = d.get('_rest'), d.get('_t')
        if not r or t is None or r.get('tops'):
            continue
        shot = next((x for x in shots if x[1] <= t < x[2]), None)
        if shot is None or shot[2] >= getattr(film, 'BLACK_AT', getattr(film, 'DUR', 1e9)) - 1e-6:
            continue                                      # the film's last shot ends on black, not a cut
        for s in 'LR':
            g = _rest_gap(r, s)
            if g is not None:
                seen.setdefault((name, shot, s), []).append((t, g))
    out, told = [], set()
    for (name, shot, s), ts in seen.items():
        if any(fnmatch.fnmatch(name, n) and fnmatch.fnmatch(shot[0], sh) for n, sh in ok) or (name, shot) in told:
            continue
        ts.sort()
        tail = [(t, g) for t, g in ts if t >= shot[2] - CUT_TAIL]
        landed = next((t for t, g in tail if g < NEAR_REST), None)
        if landed is None:
            continue
        before = [(t, g) for t, g in ts if landed - 0.8 <= t < landed]
        if any(g > FAR_REST for _, g in before):
            told.add((name, shot))
            out.append(f'CUT: shot {shot[0]} (cut at {shot[2]:.2f} s): {name}\'s {s} arm drops back to rest by '
                       f'{landed:.2f} s, in the last {CUT_TAIL} s before the cut (rule 72: cut before the return, or '
                       f'hold the pose; CUT_RESTS_OK if meant)')
    return out


FACE_MIN = 240          # rule 50: px tall on a 1920-tall frame, once per famous person


def faces(film, records, ask=True):
    """Rule 50 (Job L; was by hand): every name in the film's FAMOUS list gets at least one drawn frame with the face
    on screen and at least FACE_MIN px tall. Faces come from mouths_seen(t)'s head height when the film has it (any
    kind of drawing), else from the drawing pass's views.py people. A film with people and no FAMOUS is asked for one
    (FAMOUS = [] when nobody is famous); with ask=False (a film from before the 10 Nov template) only printed."""
    if not hasattr(film, 'FAMOUS'):
        if 'people' in set(getattr(film, 'HAS', ('people',))) and not ask:
            print('WARNING: no FAMOUS list: rule 50 (a famous face 240 px tall once) not checked')
        elif 'people' in set(getattr(film, 'HAS', ('people',))):
            return ['FACES: the film has people but no FAMOUS list, so nothing checks rule 50 (a famous face 240 px '
                    'tall once): FAMOUS = [names as drawn], or [] for nobody famous']
        return []
    best = {n: 0.0 for n in film.FAMOUS}
    for where, name, d in records:
        if d.get('face_in') is False:
            continue
        for n in best:
            if fnmatch.fnmatch(str(name).lower(), n.lower()):
                best[n] = max(best[n], d.get('face_px') or 0.0)
    if hasattr(film, 'mouths_seen') and any(v < FACE_MIN for v in best.values()):
        end = getattr(film, 'BLACK_AT', getattr(film, 'DUR', 0))
        fps = getattr(film, 'FPS', 12)
        for i in range(0, int(end * fps), 3):
            try:
                seen = film.mouths_seen(i / fps)
            except Exception:
                break
            for name, _m, _yaw, px, *_ in seen or ():
                for n in best:
                    if fnmatch.fnmatch(str(name).lower(), n.lower()):
                        best[n] = max(best[n], px or 0.0)
    return [f'FACES: {n}\'s face is never {FACE_MIN} px tall (largest {v:.0f} px; rule 50: one shot close enough to '
            f'know them)' if v else f'FACES: {n} (FAMOUS) was never found drawn: check the name as drawn'
            for n, v in best.items() if v < FACE_MIN]

def main():
    film = importlib.import_module(sys.argv[1])
    import audit
    fs = run(film) + [f for f in audit.check(film) if f.split(': ', 2)[1] in ('COULD NOT TEST', 'TOUCH', 'HIDDEN', 'HELD', 'RESTING',
                                                                                 'RESTING ARM')]
    print('\n'.join(fs) or 'kitchecks: clean')


if __name__ == '__main__':
    main()
