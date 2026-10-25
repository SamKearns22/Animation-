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
From the drawing (pre-flight's pass over every 3rd frame; every views.py person drawn is logged):
  facing      a head turned no more than 95 degrees from its body; seen from behind, nothing held out in front
              drawn over the back (Prepper notes 11, 12, 16)
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
        self.fps = film.FPS
        self.found = {}                    # (kind, names) -> [(t, text)]
        self.last_props = {}               # prop name -> (frame, pos)
        self.hand_track = {}               # (thing, part) -> [frame, pos, still since]

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

    def frame(self, i, t, shot, things, cam):
        # touches: the hand on the thing, and seen
        for hand, target, t0, t1, why, *_ in self.touches:
            if not _in(t, t0, t1):
                continue
            hs = [(n, s) for n, th in things.items() for s in _hands(th) if _hit(hand, n, s.part)]
            ts = [th for n, th in things.items() if _hit(target, n)]
            if not hs or not ts:
                self._fault('touch', (hand, target), t, f'{t:.2f} s ({shot}): {hand} or {target} is not in the scene '
                                                        f'(TOUCHES: {why})')
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
            near = [o for o, oth in things.items() if o != n and any(_gap(s, th) <= CLEAR for s in _hands(oth))]
            if not near:
                self._fault('held', (n,), t, f'{t:.2f} s ({shot}): {n} moves with no hand on it (list it in '
                                             f'FREE_MOVES if it flies, falls or slides)')
        # resting: a hand held still keeps clear of what it is not meant to touch
        for n, th in things.items():
            if not _figure(th):
                continue
            for s in _hands(th):
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
                for o, oth in things.items():
                    if o == n:
                        continue
                    g = _gap(s, oth)
                    if -0.02 < g < CLEAR and not self._allowed(n, s.part, o, t):
                        self._fault('resting', (f'{n}.{s.part}', o), t,
                                    f'{t:.2f} s ({shot}): {n}\'s resting {s.part} sits {max(g, 0) * 100:.0f} cm from '
                                    f'{o} (keep 3 cm clear, or list the touch in TOUCHES)')

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


def install():
    """Log every views.py person drawn (their view, head turn and what they hold), for facing(). Patches views.person
    and every module that took its own name for it."""
    import views
    if getattr(views.person, '_logged', False):
        return
    real = views.person

    def person(img, cam, x, y, s, sp, t, yaw, joints=None, head_yaw=None):
        j2 = real(img, cam, x, y, s, sp, t, yaw, joints, head_yaw)
        try:
            import figure as F
            where = F.CONTEXT.get('where', '')
        except Exception:
            where = ''
        if isinstance(j2, dict) and '_drawn' in j2:
            DRAWN.append((where, sp.get('name', 'someone'), dict(j2['_drawn'])))
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
            draw(t)
        drawn = DRAWN[n0:]
    return facing(drawn) + marks(film) + sounds(film)


def main():
    film = importlib.import_module(sys.argv[1])
    import audit
    fs = run(film) + [f for f in audit.check(film) if f.split(': ', 2)[1] in ('TOUCH', 'HIDDEN', 'HELD', 'RESTING')]
    print('\n'.join(fs) or 'kitchecks: clean')


if __name__ == '__main__':
    main()
