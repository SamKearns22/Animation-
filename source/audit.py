#!/usr/bin/env python3
"""audit: the automatic collision test (rule 5) and pop-in test (rule 6) of guides/film-quality-rules.md, for any film.

Why: Power Crime Action took 16 notes from Sam for things a computer can find: a door swinging through an officer,
Jenkins walking through a door, a rifle through a face, the old lady flashing on the front of the van, people popping
in and out as the camera zoomed, an officer jumping sideways out of frame. Each was fixed as a symptom, and the next
one got through. This tests the RESULT, on every frame:

  collisions  everyone and everything solid (clipcheck.py's shapes: capsules, boxes and flat cards, in metres) is
              tested on every frame and at two moments between frames (so a slammed door or a swung arm cannot skip
              through someone); any two that pass into each other by more than clipcheck.TOUCH are flagged, unless
              the film's ALLOWED_CONTACTS names them (a hand on an arm, sitting on a chair, a finger in a chest).
              Only what is on screen counts (the rest is listed as a number).
  pop-ins     frame to frame within a shot: anyone or anything that appears or vanishes away from the frame's edge,
              changes drawing (a simple far figure becoming a full one), or jumps (moves much further in one frame
              than in the frames either side), unless the film's ALLOWED_POPS names it (gone in through a door).
  roster      who is on screen in each shot (the rule's "list of who is in each shot").
  the set     a film with a PLAN gets every wall (cut round its openings; pieces by an opening named as its frame),
              every THING and every door leaf (at film.door_angles(t)) as solids by itself (sets.solids, rule 12):
              the film lists only what to leave out, SET_EXCLUDE = [(name pattern, why)]. Set pieces touching each
              other are never a fault; they are left out of the roster.

A film joins in by giving, besides SHOTS, FPS, DUR and cam_for(t):
  scene(t)          -> [Thing]: everyone and everything solid at time t, as drawn. Make it with a Recorder: the film's
                       own picture(t) run with the drawing switched off, catching where each person and prop is put
                       (placed() turns a views.py pose into solids, props included). A hand-written copy of who is
                       where would miss the drawing's own mistakes (the old lady was drawn for one frame after she
                       landed because of a condition in the drawing code).
  ALLOWED_CONTACTS  [(a, b, t0, t1, why[, up_to])]: a and b match a thing ('ARV7') or one of its parts ('ARV7.handR'),
                       with * wildcards; t0 / t1 None = from the start / to the end; up_to (metres): deeper is still a
                       fault. Every entry says why it is meant; the report counts what each one let through.
  ALLOWED_POPS      [(name, t0, t1, why)].
  project(cam, P)   optional: world points (N x 3) -> screen x, y, depth (three arrays of N). The default handles a
                       Cam3-style camera (pos, f, r, u, focal; poker_mon_room.Cam3) on a 1080 x 1920 frame.

    python3 source/audit.py FILM [--from T0] [--to T1] [--shots a,b] [--sub 2] [--sheet OUT.jpg] [--out FULL.txt]
      FILM is the module name in source/ (power_crime). --sheet: a small frame of each fault, the things outlined.
      Prints a short summary; the whole report (roster, every fault, allowed contacts) goes to review/FILM-audit.txt
      (or --out) (rule 19).
Also run by preflight.py through the film's audits(): return audit.check(film) there.
"""
import fnmatch
import importlib
import math
import os
import re
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clipcheck as CC           # noqa: E402  the shapes and how far two pass into each other
import views as V                # noqa: E402

U = V.M_PER_UNIT
SOLE = CC.SOLE
SUB = 2                          # tests between frames (a slammed door turns ~40 degrees a frame)
EDGE = 4                         # pixels: a thing this close to the frame's edge is coming or going, not popping
JUMP = 0.25                      # metres: a jump shorter than this is never flagged (a twitch, a step)
FRAME = (1080, 1920)
LAST_ROSTER = {}                 # the last run's {shot: names on screen}


# ------------------------------------------------------------------------------------------------- what is tested
class Thing:
    """One person or prop at one moment: a name, its solids, and which drawing it is (a full figure, a far one)."""
    def __init__(self, name, solids, kind='full'):
        self.name, self.kind = name, kind
        self.solids = [s for s in solids if s is not None]
        for s in self.solids:
            s.owner = name
        b = [CC.bounds(s) for s in self.solids]
        self.slo = np.array([x[0] for x in b])
        self.shi = np.array([x[1] for x in b])
        self.lo, self.hi = self.slo.min(0), self.shi.max(0)
        body = [s for s in self.solids if s.part in ('body', 'torso')]
        self.pos = (np.mean([(s.a + s.b) / 2 for s in body], axis=0) if body else (self.lo + self.hi) / 2)
        self.key = np.round(np.concatenate([self.slo.ravel(), self.shi.ravel()]), 3).tobytes() + kind.encode()


class Recorder:
    """Runs a film's own picture code with the drawing switched off: patch() swaps a drawing function for one that
    records where things are put (restored on leaving the `with`), stub() switches one off, add() records a Thing."""
    def __init__(self):
        self.things, self._saved = [], []

    def patch(self, obj, name, fn):
        self._saved.append((obj, name, getattr(obj, name)))
        setattr(obj, name, fn)

    def stub(self, obj, *names, result=None):
        for n in names:
            self.patch(obj, n, lambda *a, _r=result, **k: _r)

    def add(self, name, solids, kind='full'):
        self.things.append(Thing(name, solids, kind))

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        for obj, name, old in reversed(self._saved):
            setattr(obj, name, old)
        self._saved = []


def _unit(v):
    v = np.asarray(v, float)
    n = float(np.linalg.norm(v))
    return v / n if n > 1e-9 else v


def placed(name, j, x, z, facing, height=1.75, lift=0.0, base=0.0, sp=None):
    """Someone's solids from their views.py pose j, standing at floor point (x, z) (metres; y up) facing (fx, fz),
    `height` tall, `lift` off the ground, on ground `base` high: clipcheck's body, head, arms, hands and legs, plus
    what they hold: a prop with .quad (corners in their own units; .qz how far in front, default 110) is a flat card,
    a prop with .along = (joint, joint, length, start) is a long thing laid through two joints (a carbine through
    both hands: from `start` x length behind the first)."""
    f = height / 1.75
    fx, fz = _unit(facing)
    rx, rz = fz, -fx                                         # the pose's +x (power_crime.to_torso's convention)
    bob, lean = j.get('bob', 0.0), j.get('lean', 0.0)

    def world(p):                                            # clipcheck's frame (X across, Y up, Z = back) to ours
        X, Y, Zl = p
        fw = -Zl
        return np.array((x + (X * rx + fw * fx) * f, base + lift + Y * f, z + (X * rz + fw * fz) * f))

    def local(p3):                                           # a point of the upper body, as person_solids places it
        q = V.leaned(tuple(p3), lean)
        return np.array((q[0] * U, (SOLE - q[1] - bob) * U, -q[2] * U))
    out = CC.person_solids(name, j, 0.0, 0.0, 0.0, sp)
    for s in out:
        s.a, s.b, s.r = world(s.a), world(s.b), s.r * f
    for p in j.get('props', []):
        quad = getattr(p, 'quad', None)
        if quad is not None:
            qz = getattr(p, 'qz', 110.0)
            c = [world(local((qx, qy, qz))) for qx, qy in quad]
            out.append(CC.card(name, 'prop', c[0], c[1] - c[0], c[3] - c[0], 0.008))
        along = getattr(p, 'along', None)
        if along is not None:
            ja, jb, L, start = along
            a, b = np.asarray(j[ja], float), np.asarray(j[jb], float)
            d = _unit(b - a)
            s0 = a - d * start * L
            out.append(CC.capsule(name, 'gun', world(local(s0)), world(local(s0 + d * L)), 0.03 * f))
    return out


def simple(name, x, z, height=1.75, base=0.0, sitting=False, facing=(0.0, 1.0)):
    """A simple far figure's solids (no arms): body, head, and legs (folded forward when sitting on the ground)."""
    f, y = height / 1.75, base
    fx, fz = _unit(facing)
    if sitting:
        return [CC.capsule(name, 'body', (x, y + 0.2 * f, z), (x, y + 0.62 * f, z), 0.14 * f),
                CC.sphere(name, 'head', (x, y + 0.9 * f, z), 0.1 * f),
                CC.capsule(name, 'legs', (x, y + 0.12 * f, z), (x + fx * 0.38 * f, y + 0.12 * f, z + fz * 0.38 * f),
                           0.07 * f)]
    return [CC.capsule(name, 'legs', (x, y + 0.1 * f, z), (x, y + 0.8 * f, z), 0.1 * f),
            CC.capsule(name, 'body', (x, y + 0.9 * f, z), (x, y + 1.32 * f, z), 0.15 * f),
            CC.sphere(name, 'head', (x, y + 1.6 * f, z), 0.1 * f)]


def card_from(name, part, corners, r=0.01):
    """A flat card from its corners (any three in order: a, a + u, ..., a + v)."""
    c = [np.asarray(p, float) for p in corners]
    return CC.card(name, part, c[0], c[1] - c[0], c[-1] - c[0], r)


# ------------------------------------------------------------------------------------------------- the camera
def _project(film, cam, P):
    """World points (N x 3) -> screen x, y and depth; None if the camera can't be read (then all counts as seen)."""
    if hasattr(film, 'project'):
        return film.project(cam, P)
    if not all(hasattr(cam, a) for a in ('pos', 'f', 'r', 'u', 'focal')):
        return None
    d = P - np.asarray(cam.pos, float)
    z = d @ np.asarray(cam.f, float)
    k = cam.focal / np.maximum(z, 0.15)
    sh = getattr(cam, 'shake', (0.0, 0.0))
    return (FRAME[0] / 2 + (d @ np.asarray(cam.r, float)) * k + sh[0],
            FRAME[1] / 2 - (d @ np.asarray(cam.u, float)) * k + sh[1], z)


def _screen_boxes(film, cam, lo, hi):
    """Each box's (lo, hi) as seen: on screen at all, wholly inside the frame (away from its edge), and its screen box."""
    n = len(lo)
    if n == 0:
        return np.zeros(0, bool), np.zeros(0, bool), np.zeros((0, 4))
    corners = np.stack([np.where(np.array([(i >> k) & 1 for k in range(3)], bool), hi, lo) for i in range(8)], 1)
    pr = _project(film, cam, corners.reshape(-1, 3))
    if pr is None:
        return np.ones(n, bool), np.zeros(n, bool), np.zeros((n, 4))
    X, Y, D = (np.asarray(a).reshape(n, 8) for a in pr)
    front = D > 0.2
    big = 1e6
    x0 = np.where(front, X, big).min(1)
    x1 = np.where(front, X, -big).max(1)
    y0 = np.where(front, Y, big).min(1)
    y1 = np.where(front, Y, -big).max(1)
    seen = front.any(1) & (x1 > 0) & (x0 < FRAME[0]) & (y1 > 0) & (y0 < FRAME[1])
    inside = front.all(1) & (x0 > EDGE) & (x1 < FRAME[0] - EDGE) & (y0 > EDGE) & (y1 < FRAME[1] - EDGE)
    return seen, inside, np.stack([x0, y0, x1, y1], 1)


# ------------------------------------------------------------------------------------------------- the lists
def _hit(pattern, thing, part):
    return fnmatch.fnmatchcase(thing, pattern) or fnmatch.fnmatchcase(f'{thing}.{part}', pattern)


def _contact_ok(film, a, pa, b, pb, t, depth=0.0):
    """The ALLOWED_CONTACTS entry that covers this contact (None: a fault). An entry's optional sixth item caps how
    deep the contact may go (a hand resting ON a table, not sunk into it)."""
    for ent in list(getattr(film, 'ALLOWED_CONTACTS', ())) + list(getattr(film, 'TOUCHES', ())):   # a meant touch
        x, y, t0, t1 = ent[:4]                                                                    # (kitchecks)
        cap = ent[5] if len(ent) > 5 else None
        if (t0 is None or t >= t0) and (t1 is None or t <= t1) and (cap is None or depth <= cap) and \
                ((_hit(x, a, pa) and _hit(y, b, pb)) or (_hit(x, b, pb) and _hit(y, a, pa))):
            return ent
    return None


def _pop_ok(film, name, t):
    return any(fnmatch.fnmatchcase(name, n) and (t0 is None or t >= t0) and (t1 is None or t <= t1)
               for n, t0, t1, *_ in getattr(film, 'ALLOWED_POPS', ()))


def _group(name):
    return re.sub(r'[#_ ]?\d+$', '', name) or name


# ------------------------------------------------------------------------------------------------- the test
def _pair_overlaps(A, B):
    """Every pair of solids (one from each) passing into each other: [(part a, part b, depth, middle point)]."""
    ia, ib = np.nonzero(np.all((A.slo[:, None] < B.shi[None]) & (A.shi[:, None] > B.slo[None]), axis=2))
    out = []
    for i, k in zip(ia, ib):
        sa, sb = A.solids[i], B.solids[k]
        o = CC.overlap(sa, sb)
        if o > CC.TOUCH:
            mid = (np.maximum(A.slo[i], B.slo[k]) + np.minimum(A.shi[i], B.shi[k])) / 2
            out.append((sa.part, sb.part, o, mid))
    return out


def run(film, t0=None, t1=None, shots=None, sub=SUB, log=print):
    """Both tests over the film (or a stretch of it). Returns the faults: dicts with 'what', 't', 'names', 'text'."""
    fps, dur = film.FPS, min(film.DUR, getattr(film, 'BLACK_AT', film.DUR))   # nothing to test in the black
    shot_of = (lambda t: next((s[0] for s in film.SHOTS if s[1] <= t < s[2]), film.SHOTS[-1][0]))
    a = 0.0 if t0 is None else t0
    b = dur if t1 is None else min(t1, dur)
    frames = [i for i in range(int(math.ceil(a * fps - 1e-6)), int(math.ceil(b * fps - 1e-6)))
              if shots is None or shot_of(i / fps) in shots]
    started = time.time()
    import sets
    set_solids = (lambda t: sets.solids(film, t)) if getattr(film, 'PLAN', None) is not None else (lambda t: [])
    import kitchecks
    shared = kitchecks.SceneChecks(film)  # rule 13: hands on what they touch, and seen; props held; resting hands
    keys, pairs = {}, {}                  # last key of each thing; pairs passing into each other {(a, b): overlaps}
    hits = {}                             # (a, b) -> [(t, depth, part a, part b, shot, on screen)]
    offscreen = 0
    used = {}                             # allowed contacts used: why -> [pairs, deepest]
    recs = []                             # each frame: (i, t, shot, {name: (kind, pos, seen, inside, box)})
    last = (None, None)
    for i in frames:
        shot = shot_of(i / fps)
        if last != (i - 1, shot):         # a cut or a gap: test everything afresh
            keys, pairs = {}, {}
        last = (i, shot)
        for k in range(sub + 1):
            t = (i + k / (sub + 1)) / fps
            if k and shot_of(t) != shot:
                break
            things = {}
            for th in film.scene(t):
                nm, n = th.name, 2
                while nm in things:       # two drawn under one name: keep both
                    nm, n = f'{th.name}~{n}', n + 1
                th.name = nm
                things[nm] = th
            for th in set_solids(t):      # rule 12: the set's walls, frames, doors and furniture, from the plan
                if th.name not in things:
                    things[th.name] = th
            names = list(things)
            lo = np.array([things[n].lo for n in names]) if names else np.zeros((0, 3))
            hi = np.array([things[n].hi for n in names]) if names else np.zeros((0, 3))
            dirty = [x for x, n in enumerate(names) if keys.get(n) != things[n].key]   # moved, changed or new
            dset, dnames = set(dirty), {names[x] for x in dirty}
            keys = {n: things[n].key for n in names}
            pairs = {p: v for p, v in pairs.items()                  # unchanged pairs keep their last result
                     if p[0] in things and p[1] in things and p[0] not in dnames and p[1] not in dnames}
            for x in dirty:
                cand = np.nonzero(np.all((lo[x] < hi) & (hi[x] > lo), axis=1))[0]
                for y in cand:
                    if y == x or (y in dset and y < x):
                        continue
                    A, B = things[names[x]], things[names[y]]
                    if A.kind == 'set' and B.kind == 'set':          # two set pieces touching never move
                        continue
                    ov = _pair_overlaps(A, B)
                    if ov:
                        pa, pb = sorted((A.name, B.name))
                        pairs[(pa, pb)] = ov if A.name == pa else [(q, p, o, m) for p, q, o, m in ov]
            cam = film.cam_for(t)
            for (pa, pb), ov in pairs.items():
                bad = []
                for o in ov:
                    ent = _contact_ok(film, pa, o[0], pb, o[1], t, o[2])
                    if ent is None:
                        bad.append(o)
                    else:
                        u = used.setdefault(ent[4], [set(), 0.0])
                        u[0].add((pa, pb))
                        u[1] = max(u[1], o[2])
                if not bad:
                    continue
                worst = max(bad, key=lambda o: o[2])
                pr = _project(film, cam, worst[3][None])
                seen = pr is None or (pr[2][0] > 0.2 and 0 <= pr[0][0] <= FRAME[0] and 0 <= pr[1][0] <= FRAME[1])
                if not seen:
                    offscreen += 1
                    continue
                hits.setdefault((pa, pb), []).append((t, worst[2], worst[0], worst[1], shot))
            if k == 0:
                shared.frame(i, t, shot, things, cam)
                seen, inside, box = _screen_boxes(film, cam, lo, hi)
                recs.append((i, t, shot, {n: (things[n].kind, things[n].pos, bool(seen[x]), bool(inside[x]), box[x])
                                          for x, n in enumerate(names)}))
    faults = _collisions(hits, fps, sub) + _pops(film, recs) + shared.faults()
    faults.sort(key=lambda f: f['t'])
    global LAST_ROSTER                    # who was on screen in each shot (pre-flight's shot cast check, rule 14)
    LAST_ROSTER = {}
    for i, t, s, R in recs:
        LAST_ROSTER.setdefault(s, set()).update(n for n, v in R.items() if v[2] and v[0] != 'set')
    if log:
        log(report(film, recs, faults, offscreen, len(frames), sub, time.time() - started, used))
    return faults


def _collisions(hits, fps, sub):
    """Overlaps tested at neighbouring moments joined into spans: one fault per pair per span."""
    out = []
    gap = 1.6 / (fps * (sub + 1))
    for (pa, pb), hs in hits.items():
        hs.sort()
        span = [hs[0]]
        for h in hs[1:] + [None]:
            if h is not None and h[0] - span[-1][0] <= gap + 1e-6 and h[4] == span[-1][4]:
                span.append(h)
                continue
            w = max(span, key=lambda s: s[1])
            when = f'{span[0][0]:.2f} s' if len(span) == 1 else f'{span[0][0]:.2f}-{span[-1][0]:.2f} s'
            out.append(dict(what='collision', t=w[0], names=(pa, pb), shot=w[4], depth=w[1],
                            text=f'{when} ({w[4]}): {pa}.{w[2]} passes {w[1] * 100:.0f} cm into {pb}.{w[3]}'))
            span = [h] if h is not None else []
    return out


def _pops(film, recs):
    out = []
    for (ia, ta, sa, A), (ib, tb, sb, B) in zip(recs, recs[1:]):
        if ib != ia + 1 or sa != sb:
            continue
        for n in set(A) | set(B):
            a, b = A.get(n), B.get(n)
            if (a or b)[0] == 'set':      # the set's own pieces (a door leaf too) never pop
                continue
            if a and not b and a[3] and not _pop_ok(film, n, ta):
                out.append(dict(what='pop', t=ta, names=(n,), shot=sa,
                                text=f'{ta:.2f} s ({sa}): {n} vanishes in the middle of the frame (next frame: gone)'))
            elif b and not a and b[3] and not _pop_ok(film, n, tb):
                out.append(dict(what='pop', t=tb, names=(n,), shot=sb,
                                text=f'{tb:.2f} s ({sb}): {n} appears from nothing in the middle of the frame'))
            elif a and b and a[0] != b[0] and (a[2] or b[2]) and not _pop_ok(film, n, tb):
                out.append(dict(what='change', t=tb, names=(n,), shot=sb,
                                text=f'{tb:.2f} s ({sb}): {n} changes drawing on screen ({a[0]} -> {b[0]})'))
    # jumps: a step much longer than the steps either side (a teleport, not a fast move)
    tracks = {}
    for i, t, s, R in recs:
        for n, (kind, pos, seen, inside, box) in R.items():
            if kind != 'set':             # a slammed door is not a teleport
                tracks.setdefault(n, []).append((i, t, s, pos, seen))
    for n, tr in tracks.items():
        steps = [(q[1], q[2], float(np.linalg.norm(q[3] - p[3])), p[4] or q[4]) if q[0] == p[0] + 1 and q[2] == p[2]
                 else None for p, q in zip(tr, tr[1:])]
        for x, st in enumerate(steps):
            if st is None or not st[3] or st[2] < JUMP:
                continue
            nb = [steps[y][2] for y in (x - 1, x + 1) if 0 <= y < len(steps) and steps[y] is not None]
            if st[2] > 3 * max(nb + [0.02]) and not _pop_ok(film, n, st[0]):
                out.append(dict(what='jump', t=st[0], names=(n,), shot=st[1],
                                text=f'{st[0]:.2f} s ({st[1]}): {n} jumps {st[2]:.2f} m in one frame '
                                     f'(the frames either side: {max(nb + [0.0]):.2f} m)'))
    return out


def _roster(recs):
    """Who is on screen in each shot, grouped (CROWD x 812 (far 790, full 22), ARV x 14, ...)."""
    lines = []
    for shot in dict.fromkeys(r[2] for r in recs):
        on = {}
        for i, t, s, R in recs:
            if s == shot:
                for n, v in R.items():
                    if v[2] and v[0] != 'set':
                        on.setdefault(n, set()).add(v[0])
        groups = {}
        for n, kinds in on.items():
            groups.setdefault(_group(n), []).append((n, kinds))
        parts = []
        for g, mem in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            if len(mem) == 1 and mem[0][1] == {'full'}:
                parts.append(mem[0][0])
                continue
            kinds = {}
            for n, ks in mem:
                for k in ks:
                    kinds[k] = kinds.get(k, 0) + 1
            extra = '' if list(kinds) == ['full'] else ' (' + ', '.join(f'{k} {v}' for k, v in sorted(kinds.items())) + ')'
            parts.append(f'{g} x {len(mem)}{extra}')
        lines.append(f'  {shot}: ' + ', '.join(parts))
    return lines


def report(film, recs, faults, offscreen, nframes, sub, secs, used=None):
    head = HEAD
    lines = [f'audit ({getattr(film, "NAME", film.__name__)}): {nframes} frames, each tested {sub + 1} times, '
             f'{secs:.0f} s', 'Who is on screen, shot by shot:'] + _roster(recs)
    if not faults:
        lines.append('audit: clean (nothing on screen passes through anything; nothing pops, changes or jumps)')
    for what in head:
        fs = [f for f in faults if f['what'] == what]
        for f in fs[:40]:
            lines.append(f'{head[what]}: {f["text"]}')
        if len(fs) > 40:
            lines.append(f'{head[what]}: ... and {len(fs) - 40} more')
    for why, (prs, deep) in (used or {}).items():
        lines.append(f'allowed (ALLOWED_CONTACTS): {why}: {len(prs)} pair(s), up to {deep * 100:.0f} cm')
    if offscreen:
        lines.append(f'(off screen, not counted: {offscreen} tests found things passing into each other)')
    return '\n'.join(lines)


HEAD = {'collision': 'PASSES THROUGH', 'pop': 'POPS', 'change': 'CHANGES DRAWING', 'jump': 'JUMPS',
        'touch': 'TOUCH', 'hidden': 'HIDDEN', 'held': 'HELD', 'resting': 'RESTING'}


def check_lines(faults):
    return [f'AUDIT: {HEAD[f["what"]]}: {f["text"]}' for f in faults]


def check(film, **kw):
    """For a film's audits() (preflight.py): the faults as lines ('AUDIT: KIND: text')."""
    return check_lines(run(film, log=None, **kw))


def sheet(film, faults, out, most=12):
    """A small frame at each fault, with the things involved outlined in red (one combined sheet)."""
    from PIL import Image, ImageDraw
    picks, seen = [], set()
    for f in faults:
        k = (f['what'], f['names'])
        if k not in seen:
            seen.add(k)
            picks.append(f)
    picks = picks[:most]
    if not picks:
        return None
    if hasattr(film, 'B'):
        film.B.SS = 1
    w, h = 270, 480
    cols = min(4, len(picks))
    img = Image.new('RGB', (cols * w, ((len(picks) + cols - 1) // cols) * (h + 40)), (255, 255, 255))
    for x, f in enumerate(picks):
        t = f['t']
        draw = getattr(film, 'frame_image', None) or film.picture
        fr = draw(t).convert('RGB').resize((w, h))
        d = ImageDraw.Draw(fr)
        import sets
        things = {th.name: th for th in list(sets.solids(film, t)) + list(film.scene(t))}
        cam = film.cam_for(t)
        for n in f['names']:
            th = things.get(n)
            if th is not None:
                x0, y0, x1, y1 = _screen_boxes(film, cam, th.lo[None], th.hi[None])[2][0]
                d.rectangle([x0 * w / FRAME[0], y0 * h / FRAME[1], x1 * w / FRAME[0], y1 * h / FRAME[1]],
                            outline=(255, 0, 0), width=2)
        cx, cy = (x % cols) * w, (x // cols) * (h + 40)
        img.paste(fr, (cx, cy))
        ImageDraw.Draw(img).text((cx + 4, cy + h + 2), f'{x + 1}. {f["text"][:44]}\n   {f["text"][44:88]}', fill=(0, 0, 0))
    img.save(out, quality=88)
    return out


def main():
    a = sys.argv[1:]
    film = importlib.import_module(a[0])

    def opt(k, cast=float):
        return cast(a[a.index(k) + 1]) if k in a else None
    if hasattr(film, 'B'):
        film.B.SS = 1
    full = []
    faults = run(film, opt('--from'), opt('--to'), opt('--shots', lambda s: s.split(',')), opt('--sub', int) or SUB,
                 log=full.append)
    import report                          # rule 19: a short summary here, the whole report in the file
    path = opt('--out', str) or os.path.join(os.path.dirname(HERE), 'review', f'{a[0]}-audit.txt')
    print(full[0].split('\n')[0])
    report.summarise('audit', [l.split(': ', 1)[1] if ': ' in l else l for l in check_lines(faults)], path,
                     notes=full)
    if '--sheet' in a:
        print('sheet:', sheet(film, faults, a[a.index('--sheet') + 1]))
    sys.exit(1 if faults else 0)


if __name__ == '__main__':
    main()
