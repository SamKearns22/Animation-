"""filmkit: checks and helpers that work on ANY film, whatever the body part or the action.

Why: checks written for one fault (a folded elbow, a chair swing) miss the next one (a detached neck, a leg in the
wrong place). These look at the RESULT instead, so they catch faults nobody thought of:

  silhouette_audit   draw each character alone, then test the picture over time: in pieces (a floating head, a
                     detached neck, a stray limb), popping between frames, stretching or squashing, frozen.
  Beats              write any action as beats (set-up, action, contact, follow-through, settle) with times, then
                     test every frame of the path, not just the key poses.
  check_joints       generic joint rules (angle limits, bone lengths, attachment points) for any pose given as joints.
  probe_marks        permanent marks (a smear, a broken window) must still be on screen at later times.
  visible_spots      which floor spots are on screen in all of several cameras (to place action seen in two shots).
  eyeline / check_eyelines   everyone looks at whoever they fight or talk to.
  voice_balance      the voice sits clearly above crowd, music and effects wherever someone speaks.
Used by preflight.py through a film's own audits() and checks(). See guides/preflight.md.
"""
import math

import numpy as np
from PIL import Image
from scipy import ndimage


# ------------------------------------------------------------------------------------------ silhouette audit
def _mask(img, scale=4):
    a = np.asarray(img.getchannel('A'))[::scale, ::scale] > 200       # solid pixels only (soft shadows fall away)
    return a


def _touches_edge(mask):
    return bool(mask[0].any() or mask[-1].any() or mask[:, 0].any() or mask[:, -1].any())


def _parts(mask):
    lab, n = ndimage.label(mask)
    if n == 0:
        return []
    return sorted(np.bincount(lab.ravel())[1:], reverse=True)


def silhouette_audit(actors, fps=12, allow=None, still_ok=(), min_piece=0.03, pop=0.5, area_jump=0.4, frozen_s=2.5):
    """actors: {name: (times, draw)} where draw(t) returns that character ALONE on a transparent RGBA picture.
    Returns a list of faults, each saying who, when and what:
      'in pieces'  two or more solid parts, each at least min_piece of the largest (a detached neck, head or limb);
      'pops'       the shape overlaps the previous frame by less than `pop` (a limb flips or teleports);
      'stretches'  the solid area changes by more than area_jump between frames (a limb grows or shrinks);
      'frozen'     the shape does not change at all for frozen_s seconds (a frozen pose), unless named in still_ok.
    allow: [(name, t0, t1, why)] windows where a fast move is on purpose (a body thrown across the room)."""
    allow = allow or []
    faults = []
    for name, (times, draw) in actors.items():
        prev = None
        frozen_run = 0.0
        flagged = set()
        for t in times:
            m = _mask(draw(t))
            area = int(m.sum())
            if area == 0:
                prev = None
                continue
            ok = lambda t_=t: any(n == name and a <= t_ <= b for n, a, b, _ in allow)
            if _touches_edge(m):                  # cut by the edge of the frame: its shape means nothing here
                prev = None
                continue
            ps = _parts(m)
            big = [p for p in ps if p >= min_piece * ps[0]]
            if len(big) >= 2 and 'pieces' not in flagged and not ok():
                faults.append(f'{name} at {t:.2f} s: in {len(big)} pieces (a detached part?)')
                flagged.add('pieces')
            if prev is not None:
                inter = int((m & prev).sum())
                union = int((m | prev).sum())
                iou = inter / max(1, union)
                da = abs(area - int(prev.sum())) / max(1, int(prev.sum()))
                if iou < pop and not ok() and 'pop' not in flagged:
                    faults.append(f'{name} at {t:.2f} s: pops (only {iou:.0%} of the shape matches the last frame)')
                    flagged.add('pop')
                if da > area_jump and not ok() and 'area' not in flagged:
                    faults.append(f'{name} at {t:.2f} s: stretches or squashes (area changed {da:.0%} in one frame)')
                    flagged.add('area')
                frozen_run = frozen_run + 1 / fps if iou > 0.9995 else 0.0
                if frozen_run >= frozen_s and name not in still_ok and 'frozen' not in flagged:
                    faults.append(f'{name} at {t:.2f} s: frozen for {frozen_s:.1f} s (no movement at all)')
                    flagged.add('frozen')
            prev = m
    return faults


# ------------------------------------------------------------------------------------------------- actions
def _ease(u, kind):
    u = max(0.0, min(1.0, u))
    if kind == 'fast':          # speeds up into the end of the move (a hit, a snap)
        return u * u
    if kind == 'slow':          # starts fast, settles gently (follow-through)
        return 1 - (1 - u) ** 2
    if kind == 'linear':
        return u
    return u * u * (3 - 2 * u)  # smooth: slow in, slow out


def _mix(a, b, u):
    if isinstance(a, (tuple, list)):
        return type(a)(_mix(x, y, u) for x, y in zip(a, b))
    return a + (b - a) * u


class Beats:
    """Any action as named beats. Beats([(t, 'set-up', pose), (t, 'wind-up', pose, 'smooth'), (t, 'contact', pose,
    'fast'), ...]). A pose is a number, a tuple, or a dict of those (joint positions, angles, offsets).
    The ease is how the character ARRIVES at the beat: 'smooth' (default), 'fast', 'slow', 'linear'.
    .at(t) is the pose; .phase(t) is the beat it is heading for; .audit(rule) runs a rule over every frame."""
    def __init__(self, beats):
        self.b = [(x[0], x[1], x[2], x[3] if len(x) > 3 else 'smooth') for x in beats]

    def at(self, t):
        b = self.b
        if t <= b[0][0]:
            return b[0][2]
        for (t0, _, p0, _), (t1, _, p1, e1) in zip(b, b[1:]):
            if t <= t1:
                u = _ease((t - t0) / (t1 - t0), e1)
                if isinstance(p0, dict):
                    return {k: _mix(p0[k], p1[k], u) for k in p0}
                return _mix(p0, p1, u)
        return b[-1][2]

    def phase(self, t):
        for tb, name, _, _ in self.b:
            if t <= tb:
                return name
        return self.b[-1][1]

    def audit(self, rule, fps=24, label='action'):
        """rule(pose) -> list of fault strings (or []). Runs on every frame (default 24 a second) of the whole action."""
        out, seen = [], set()
        t = self.b[0][0]
        while t <= self.b[-1][0] + 1e-9:
            for f in rule(self.at(t)):
                if f not in seen:
                    seen.add(f)
                    out.append(f'{label} at {t:.2f} s ({self.phase(t)}): {f}')
            t += 1 / fps
        return out


def angle_deg(a, b, c):
    """The angle at joint b between a-b and c-b, in degrees (180 = straight)."""
    v1, v2 = (a[0] - b[0], a[1] - b[1]), (c[0] - b[0], c[1] - b[1])
    n = (math.hypot(*v1) * math.hypot(*v2)) or 1e-9
    return math.degrees(math.acos(max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / n))))


def inside(pt, poly):
    """Is the point inside the polygon (even-odd rule)?"""
    x, y = pt
    c = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def check_joints(joints, rules):
    """Generic body rules for any pose given as {name: (x, y)}. Each rule is a tuple:
      ('angle', a, b, c, lo, hi)      the angle at joint b stays between lo and hi degrees (elbow, knee, neck, waist);
      ('length', a, b, want, tol)     the bone a-b keeps its length (no stretching);
      ('inside', point, polygon_name) an attachment point (neck base, shoulder) lies inside the body shape it joins;
      ('apart', a, b, min_dist)       two points stay apart (a hand does not pass through the head).
    Returns a list of faults."""
    out = []
    for r in rules:
        k = r[0]
        if k == 'angle':
            _, a, b, c, lo, hi = r
            v = angle_deg(joints[a], joints[b], joints[c])
            if not lo <= v <= hi:
                out.append(f'{b} bends {v:.0f} degrees (allowed {lo}-{hi})')
        elif k == 'length':
            _, a, b, want, tol = r
            v = math.dist(joints[a], joints[b])
            if abs(v - want) > tol * want:
                out.append(f'{a}-{b} is {v:.0f} long (should be {want:.0f})')
        elif k == 'inside':
            _, p, poly = r
            if not inside(joints[p], joints[poly]):
                out.append(f'{p} is outside {poly} (a gap would open)')
        elif k == 'apart':
            _, a, b, d = r
            if math.dist(joints[a], joints[b]) < d:
                out.append(f'{a} is within {d:.0f} of {b} (passing through it)')
    return out


# ------------------------------------------------------------------------------------------------ eyelines
EYES = []


def eyeline(name, t, eye, look, target):
    """Called while drawing: where a character's eyes are, which way they look (x, y: the pupils' offset) and what they
    SHOULD be looking at (the person they fight or talk to). check_eyelines() then tests them all."""
    EYES.append((name, t, tuple(eye), tuple(look), tuple(target)))


def check_eyelines(min_cos=0.3, clear=True):
    """Everyone looks at whoever they are dealing with (twice a fighter stared at nothing). Returns faults."""
    out, seen = [], set()
    for name, t, eye, look, target in EYES:
        dx, dy = target[0] - eye[0], target[1] - eye[1]
        if abs(look[1]) < 1e-9:              # pupils only move sideways: the side must be right
            ok = abs(dx) < 10 or (look[0] > 0) == (dx > 0) and abs(look[0]) > 0.2
        else:
            n = (math.hypot(dx, dy) * math.hypot(*look)) or 1e-9
            ok = (dx * look[0] + dy * look[1]) / n >= min_cos
        if not ok and name not in seen:
            seen.add(name)
            out.append(f'{name} at {t:.2f} s: not looking at who they are dealing with')
    if clear:
        EYES.clear()
    return out


# ------------------------------------------------------------------------------------------------ sound
def voice_balance(voice, rest, sr, windows, min_db=6.0, label='voice'):
    """The voice must sit clearly above everything else (crowd, music, effects) wherever someone speaks: at least
    min_db louder, measured over each speech window [(start, end) seconds]. Returns faults."""
    out = []
    for a, b in windows:
        i, j = int(a * sr), int(b * sr)
        if j - i < sr // 10:
            continue
        v = np.sqrt(np.mean(voice[i:j] ** 2)) + 1e-12
        r = np.sqrt(np.mean(rest[i:j] ** 2)) + 1e-12
        m = 20 * math.log10(v / r)
        if m < min_db:
            out.append(f'{label} at {a:.2f}-{b:.2f} s is only {m:.1f} dB above the rest of the sound (needs {min_db:.0f})')
    return out


# ----------------------------------------------------------------------------------------- permanent marks
def probe_marks(frame_at, marks):
    """Things that change the world and must STAY changed (a hand smear on a podium, a broken window, blood on a
    wall). marks: [{'name', 'box': (x0, y0, x1, y1) in picture pixels, 'colour': (r, g, b), 'tol': 60, 'min': 30,
    'times': [t, ...]}]. At each time the box must hold at least `min` pixels near the colour. frame_at(t) is a
    PIL image. Returns faults."""
    out = []
    for m in marks:
        for t in m['times']:
            im = np.asarray(frame_at(t).convert('RGB')).astype(int)
            x0, y0, x1, y1 = m['box']
            reg = im[y0:y1, x0:x1]
            near = (np.abs(reg - np.array(m['colour'])).sum(axis=2) < m.get('tol', 60)).sum()
            if near < m.get('min', 30):
                out.append(f"{m['name']} is missing at {t:.2f} s (only {near} pixels of the mark in its place)")
    return out


# --------------------------------------------------------------------------------------------- staging aid
def visible_spots(cams, xs, zs, step=0.1, y=1.2, margin=60, size=(1080, 1920)):
    """Floor spots (X, Z) whose point at height y is on screen in EVERY camera in cams (objects with
    .P(X, Y, Z) -> (sx, sy) and .depth(Z, X)). Place action there so it is seen in more than one shot."""
    out = []
    X = xs[0]
    while X <= xs[1] + 1e-9:
        Z = zs[0]
        while Z <= zs[1] + 1e-9:
            ok = True
            for c in cams:
                if c.depth(Z, X) < 0.6:
                    ok = False
                    break
                sx, sy = c.P(X, y, Z)
                if not (margin <= sx <= size[0] - margin and margin <= sy <= size[1] - margin):
                    ok = False
                    break
            if ok:
                out.append((round(X, 2), round(Z, 2)))
            Z += step
        X += step
    return out


if __name__ == '__main__':      # a quick self-test
    b = Beats([(0.0, 'set-up', 0.0), (0.5, 'wind-up', -1.0), (0.6, 'contact', 1.0, 'fast'), (1.0, 'settle', 0.2, 'slow')])
    print('beats', [round(b.at(t), 2) for t in (0, 0.25, 0.5, 0.55, 0.6, 1.0)], b.phase(0.55))
    j = {'sh': (0, 0), 'el': (0, 100), 'wr': (0, 195), 'body': [(-50, -50), (50, -50), (50, 50), (-50, 50)], 'neck': (0, 0)}
    print(check_joints(j, [('angle', 'sh', 'el', 'wr', 25, 180), ('length', 'sh', 'el', 100, 0.1), ('inside', 'neck', 'body')]))
    print(check_joints(dict(j, wr=(0, 5)), [('angle', 'sh', 'el', 'wr', 25, 180)]))
    sq = Image.new('RGBA', (400, 400), (0, 0, 0, 0))
    a = Image.new('RGBA', (100, 100), (0, 0, 0, 255))
    sq.paste(a, (20, 20))
    two = sq.copy()
    two.paste(a, (250, 250))
    print(silhouette_audit({'whole': ([0, 1 / 12], lambda t: sq), 'split': ([0], lambda t: two)}))
