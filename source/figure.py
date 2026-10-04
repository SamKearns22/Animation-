#!/usr/bin/env python3
"""The figure system for the flat cartoon series (burnham.py people): body proportions, limbs solved from where
the hand or foot must be, joint limits, contacts, timing helpers and the checks that stop a render when a body goes
wrong. Read guides/figure-rig.md first.

Why it exists (The Patriots 2): every arm was typed in by hand, shot by shot, as an elbow point and a wrist point.
Nothing tied those points to the body, so the same person's forearm measured anything from 112 to 260 units between
shots, the medical staff's hands hung to their knees to reach a trolley drawn too low, and the protester's fingers
landed on the desk instead of the keyboard. Here a limb has one length per character; poses are given as *targets*
(where the hand goes) and the elbow is worked out (two-bone inverse kinematics); a target the arm cannot reach is an
error, so the body or the prop moves instead of the arm stretching.

Units are the person's own (burnham.Local): neck base at (0, 0), y down, head about 190 tall for hh=90.

Usage (in a film module):
    import figure as F
    rig = F.Rig(sp)                               # sp: the burnham person spec
    sp['arms'] = {'L': rig.arm('L', rig.at('hip', 'L'), 'fist'),
                  'R': rig.arm('R', (90, 300), 'point')}
    F.guard(B)                                     # every arm drawn anywhere is measured; a bad one stops the render
    with F.allow('rubber-arm gag in shot 3'):      # a deliberate break, named
        ...

    python3 figure.py sheet OUT.png                # the pose test sheet (every standard pose, checked)
"""
import contextlib
import math
import sys

import numpy as np

# ------------------------------------------------------------------------------------------- the body
# Landmarks of the series' standing adult (burnham.person), in the person's own units. Drawing canon (Loomis; the
# classic figure-drawing rules): elbows at the bottom of the rib cage (the waist), wrists at the crotch, fingertips
# about mid-thigh. Our cartoon adult is about 6 heads tall (big head, short legs), so the arms are measured from
# these landmarks, not from a realistic 8-head canon.
SHOULDER_Y = 60          # shoulder joint height (both arms)
WAIST_Y = 270            # where a hanging elbow sits
CROTCH_Y = 440           # where a hanging wrist sits; also where the legs start (hip joints)
KNEE_Y = 700
SOLE_Y = 928             # under the shoes: the floor line for a standing person
UPPER = 210              # shoulder to elbow
FORE = 170               # elbow to wrist
HAND = {'fist': 14, 'palm': 30, 'point': 66, 'thumb': 20, 'flap': 40, 'quote': 30, 'sword': 14}
# where each hand shape's contact point is, beyond the wrist along the forearm (burnham.gesture_hand / peepee.hand)

TOL_LONG = 1.06          # a drawn segment may be at most 6% longer than the rig's
TOL_SHORT = 0.40         # ...and no shorter than 40% (shorter = seen end-on, towards or away from the camera)
ELBOW_MAX = 160          # degrees between upper arm and forearm when straight-ish; never past straight
SEAT_TO_HIP = 0          # seated: the hip line (CROTCH_Y) sits on the seat


class FigureError(ValueError):
    pass


_ALLOW = []              # named deliberate breaks (a stretchy gag); while set, checks warn instead of stopping
LOG = []                 # warnings collected during a render (printed by report())
CONTEXT = {'where': ''}  # set by the caller (e.g. preflight: the shot and time) to say where a fault is


@contextlib.contextmanager
def allow(reason):
    """A deliberate break of the body rules, by name (a cartoon stretch, a gag). Checks warn instead of stopping."""
    _ALLOW.append(reason)
    try:
        yield
    finally:
        _ALLOW.pop()


def fail(msg):
    if CONTEXT['where']:
        msg = f"{CONTEXT['where']}: {msg}"
    if _ALLOW:
        LOG.append(f'{msg} (allowed: {_ALLOW[-1]})')
        return
    raise FigureError('figure check: ' + msg)


def report():
    """Each distinct fault once, with how often it happened and where it first did."""
    seen = {}
    for m in LOG:
        where, _, what = m.partition(': ')
        what = what.rsplit(' (allowed', 1)[0]
        key = (where.split(' ')[0], what.split(':')[-1].strip()[:60])
        seen.setdefault(key, [0, m])[0] += 1
    for (shot, _), (n, first) in seen.items():
        print(f'figure: {n} x  {first}')


def _norm(v):
    n = math.hypot(*v)
    return (v[0] / n, v[1] / n) if n else (0.0, 0.0)


class Rig:
    """One person's skeleton in their own units. sp: the burnham person spec (shoulders, hh)."""

    def __init__(self, sp=None, upper=UPPER, fore=FORE, name='person'):
        sp = sp or {}
        self.name = sp.get('name', name)
        self.sw = sp.get('shoulders', 150)
        self.hh = sp.get('hh', 90)
        self.upper, self.fore = upper, fore

    # landmarks -------------------------------------------------------------------------------------
    def shoulder(self, side):
        return ((-1 if side == 'L' else 1) * (self.sw - 14), SHOULDER_Y)

    def at(self, where, side='L', dx=0.0, dy=0.0):
        """A body landmark (for hand targets): hip, thigh, waist, chest, heart, chin, mouth, temple, brow, crown."""
        sgn = -1 if side == 'L' else 1
        hy = -150
        pts = {'hip': (sgn * (self.sw - 4), CROTCH_Y - 30), 'thigh': (sgn * (self.sw - 30), CROTCH_Y + 60),
               'waist': (sgn * (self.sw - 20), WAIST_Y), 'chest': (sgn * 50, 170), 'heart': (40, 160),
               'belly': (0, 330), 'chin': (0, hy + self.hh * 1.12), 'mouth': (0, hy + 60), 'temple': (sgn * 70, hy - 40),
               'brow': (sgn * 30, hy - 30), 'crown': (0, hy - self.hh), 'ear': (sgn * 74, hy + 6)}
        x, y = pts[where]
        return (x + dx, y + dy)

    def reach(self, shape='fist'):
        return self.upper + self.fore + HAND.get(shape, 14)

    # the arm: two-bone inverse kinematics --------------------------------------------------------------
    def arm(self, side, target, shape='fist', bend='out', depth=0.0, extra=None, strict=True):
        """(elbow, wrist, shape[, extra]) for burnham's 'custom' arms, with the hand's contact point on `target`.
        bend: which way the elbow points: 'out' (away from the body, the default), 'in', 'down' or 'up'.
        depth: 0 = the arm lies in the picture plane; up to 0.6 = reaching towards or away from the camera, which
        shortens it on screen (foreshortening). A target out of reach is an error (move the body or the prop)."""
        sh = self.shoulder(side)
        k = 1.0 - max(0.0, min(0.6, depth))
        U, Fh = self.upper * k, (self.fore + HAND.get(shape, 14)) * k
        dx, dy = target[0] - sh[0], target[1] - sh[1]
        d = math.hypot(dx, dy)
        if d > U + Fh + 0.5:
            if strict:
                fail(f'{self.name}: {side} hand cannot reach {tuple(round(v) for v in target)} '
                     f'(needs {d:.0f}, arm reaches {U + Fh:.0f}): move the body or the prop, never stretch the arm')
            d = U + Fh
        d = max(d, abs(U - Fh) + 1e-3)
        a = math.acos(max(-1.0, min(1.0, (U * U + d * d - Fh * Fh) / (2 * U * d))))
        base = math.atan2(dy, dx)
        cands = [(sh[0] + U * math.cos(base + s * a), sh[1] + U * math.sin(base + s * a)) for s in (1, -1)]
        sgn = -1 if side == 'L' else 1
        key = {'out': lambda e: sgn * e[0], 'in': lambda e: -sgn * e[0], 'down': lambda e: e[1], 'up': lambda e: -e[1]}[bend]
        el = max(cands, key=key)
        u = _norm((target[0] - el[0], target[1] - el[1]))
        wr = (el[0] + u[0] * self.fore * k, el[1] + u[1] * self.fore * k)
        out = (el, wr, shape) if extra is None else (el, wr, shape, extra)
        return out

    def arms(self, L, R):
        """Both arms at once from (target, shape[, bend, depth]) tuples."""
        return {'L': self.arm('L', *L), 'R': self.arm('R', *R)}

    # the standard poses ----------------------------------------------------------------------------------
    def pose(self, name, **kw):
        """Named poses built from targets (all solved by the rig, so the arms always keep their length)."""
        if name == 'sides':        # hanging relaxed: wrists at the crotch, elbows at the waist
            return {s: self.arm(s, self.at('hip', s, dx=(6 if s == 'R' else -6), dy=40), 'fist', 'down') for s in 'LR'}
        if name == 'hips':         # hands on hips, elbows out
            return {s: self.arm(s, self.at('hip', s, dy=-40), 'fist', 'out') for s in 'LR'}
        if name == 'clasped':      # hands together in front, below the belly
            return {'L': self.arm('L', (-14, CROTCH_Y - 30), 'fist', 'down'), 'R': self.arm('R', (14, CROTCH_Y - 26), 'fist', 'down')}
        if name == 'rail':         # both hands resting on a rail or mattress edge at height y (default: the waist)
            y = kw.get('y', WAIST_Y + 150)
            xs = kw.get('xs', (-0.75 * self.sw, 0.5 * self.sw))
            return {'L': self.arm('L', (xs[0], y), 'fist', 'down'), 'R': self.arm('R', (xs[1], y), 'fist', 'down')}
        if name == 'clutch':       # hand pressed to the heart, the other grabbing at the chest
            return {'L': self.arm('L', self.at('heart', 'L', dx=-60, dy=10), 'fist', 'down'),
                    'R': self.arm('R', self.at('heart', 'R'), 'fist', 'down')}
        if name == 'point':        # accusing point at a target (his units), the other hand on the hip
            side = kw.get('side', 'R')
            other = 'L' if side == 'R' else 'R'
            return {side: self.arm(side, self._toward(side, kw['target'], 'point'), 'point', 'down'),
                    other: self.arm(other, self.at('hip', other, dy=-40), 'fist', 'out')}
        if name == 'reach':        # reaching out a hand (palm) towards a target, as far as the arm allows
            side = kw.get('side', 'R')
            return {side: self.arm(side, self._toward(side, kw['target'], 'palm'), 'palm', 'down', strict=False)}
        if name == 'typing':       # index fingertips on two points of a keyboard (his units)
            tips = kw['tips']
            depth = kw.get('depth', 0.0)
            return {s: self.arm(s, tips[s], 'point', 'out', depth) for s in 'LR'}
        raise KeyError(name)

    def _toward(self, side, target, shape):
        """The nearest point towards target that the hand can reach (for points and reaches into the distance)."""
        sh = self.shoulder(side)
        v = (target[0] - sh[0], target[1] - sh[1])
        d = math.hypot(*v)
        r = self.reach(shape) * 0.97
        if d <= r:
            return target
        u = _norm(v)
        return (sh[0] + u[0] * r, sh[1] + u[1] * r)


# ------------------------------------------------------------------------------- the guard on every arm drawn
def audit_arm(sh, el, wr, where='an arm'):
    """Measure one drawn arm against the rig (for arms typed by hand or made by other code)."""
    up, fo = math.dist(sh, el), math.dist(el, wr)
    if up > UPPER * TOL_LONG:
        fail(f'{where}: upper arm {up:.0f} is longer than {UPPER} (+6%)')
    if fo > FORE * TOL_LONG:
        fail(f'{where}: forearm {fo:.0f} is longer than {FORE} (+6%)')
    if up < UPPER * TOL_SHORT or fo < FORE * TOL_SHORT:
        fail(f'{where}: arm squashed to {up:.0f}/{fo:.0f} (shorter than 40%: no real arm looks like that)')
    a, b = (sh[0] - el[0], sh[1] - el[1]), (wr[0] - el[0], wr[1] - el[1])
    cosang = (a[0] * b[0] + a[1] * b[1]) / ((math.hypot(*a) * math.hypot(*b)) or 1)
    if math.degrees(math.acos(max(-1, min(1, cosang)))) < 25:
        fail(f'{where}: elbow folded tighter than 25 degrees')


_GUARDED = {}


def guard(B, people=True):
    """Wrap burnham's arm drawing so every arm drawn in the film is measured (strict: a bad arm stops the render).
    Call once, after any other wrappers are installed."""
    if 'arm' in _GUARDED:
        return
    inner = B.arm
    _GUARDED['arm'] = inner

    def guarded(p, sh, el, wr, sleeve, w=30):
        if w <= 40:                 # people's arms (wider pieces are close-up hands drawn as arms, not limbs)
            audit_arm(sh, el, wr)
        return inner(p, sh, el, wr, sleeve, w)
    B.arm = guarded


# ------------------------------------------------------------------------------------------- legs and contact
def check_feet_on(floor_y, person_y, s, where='a person', tol=6):
    """A standing person's soles must be on the floor (world units): person_y is the neck base, s the scale."""
    sole = person_y + SOLE_Y * s
    if abs(sole - floor_y) > tol:
        fail(f'{where}: feet {sole - floor_y:+.0f} off the floor (floating or sunk)')


def check_seated(seat_y, person_y, s, where='a seated person', tol=12):
    """A seated person's hips sit on the seat (world units)."""
    hip = person_y + CROTCH_Y * s
    if abs(hip - seat_y) > tol:
        fail(f'{where}: hips {hip - seat_y:+.0f} off the seat')


def check_on(point, box, where='a contact'):
    """A contact point (a fingertip, a hand on a rail) must land inside box (x0, y0, x1, y1), world units."""
    x, y = point
    if not (box[0] <= x <= box[2] and box[1] <= y <= box[3]):
        fail(f'{where}: ({x:.0f}, {y:.0f}) is outside {tuple(round(v) for v in box)}')


def check_apart(where, items, margin=2):
    """Set pieces that must stay separate never overlap. items: {name: (x0, y0, x1, y1)}."""
    names = list(items)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            A, Bb = items[a], items[b]
            w = min(A[2], Bb[2]) - max(A[0], Bb[0])
            h = min(A[3], Bb[3]) - max(A[1], Bb[1])
            if w > margin and h > margin:
                fail(f'in {where}, the {a} overlaps the {b} by {w:.0f} x {h:.0f}')


# ------------------------------------------------------------------------------------------- timing
def ease(u):
    """Slow in, slow out (0-1)."""
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def anticipate(u, back=0.12):
    """A move with a small opposite movement first (anticipation): dips to -back, then eases to 1."""
    u = max(0.0, min(1.0, u))
    if u < 0.25:
        return -back * math.sin(math.pi * u / 0.25 / 2) ** 2
    return -back + (1 + back) * ease((u - 0.25) / 0.75)


def overshoot(u, amt=0.08):
    """Arrives a touch past the pose and settles back (follow-through)."""
    u = max(0.0, min(1.0, u))
    return ease(u) + amt * math.sin(math.pi * u) * u


def blinks(seed, t0, t1, per_min=(12, 18), talking=False):
    """Irregular blink start times between t0 and t1 (8-21 a minute at rest, more when talking or emotional)."""
    rng = np.random.default_rng(seed)
    lo, hi = per_min
    if talking:
        lo, hi = lo + 4, hi + 6
    t, out = t0 + rng.uniform(0.3, 2.0), []
    while t < t1:
        out.append(round(t, 3))
        t += 60.0 / rng.uniform(lo, hi) * rng.uniform(0.6, 1.4)
    return out


def blinking(t, times, d=0.14):
    """Closed for about two drawings at 12 fps (a spontaneous blink is 100-400 ms; the lid shuts faster than it opens)."""
    return any(b <= t < b + d for b in times)


def breath(t, period=4.0, amp=3.0, phase=0.0):
    """The chest and shoulders rising with breathing (12-20 breaths a minute at rest): an offset in his units."""
    return amp * 0.5 * (1 - math.cos(2 * math.pi * (t / period + phase)))


def saccade(t, keys):
    """Gaze that jumps (eyes move in one drawing, never eased): keys = [(time, look)] -> the look at time t."""
    look = keys[0][1]
    for k, v in keys:
        if t >= k:
            look = v
    return look


def eyes_then_head(t, t0, look, head_lag=0.15, head_share=0.6):
    """A glance: the eyes jump at t0; the head follows over ~0.3 s, a beat later; returns (look, turn)."""
    turn = head_share * look * ease((t - t0 - head_lag) / 0.3) if t >= t0 else 0.0
    return (look if t >= t0 else 0.0), turn


def walk(t, speed, s=1.0, steps_per_s=2.0):
    """A walk with no sliding feet: (phase for burnham walking legs, bob in his units, stride in world units).
    speed: world units a second. Stride (one step) = speed / steps; keep it within half the leg length."""
    stride = speed / steps_per_s
    if stride > 0.5 * (SOLE_Y - CROTCH_Y) * s * 1.2:
        fail(f'walk: stride {stride:.0f} is too long for the legs (speed it up with more steps, or slow down)')
    ph = 2 * math.pi * steps_per_s / 2 * t
    return ph, 6 * abs(math.sin(ph)), stride


def look_at(me_x, target_x, spread=600.0):
    """The burnham 'look' (-1 to 1) for eyes pointing at a person or thing at target_x (world units)."""
    return max(-1.0, min(1.0, (target_x - me_x) / spread))


# ------------------------------------------------------------------------------------------- the pose test sheet
def sheet(out):
    """Every standard pose on the series' person, drawn and checked (and one bad, hand-typed arm, caught)."""
    import burnham as B
    from PIL import Image, ImageDraw, ImageFont
    B.SS = 1
    base = dict(skin=B.PALE, hw=68, hh=90, jaw='square', hair='crop', hair_c=(80, 60, 44), outfit='jumper',
                jacket=(46, 92, 70), trousers=(46, 92, 70), shoulders=146, bottom=600, pose='custom', full=True)
    rig = Rig(base, name='test person')
    poses = [('sides', rig.pose('sides')), ('hips', rig.pose('hips')), ('clasped', rig.pose('clasped')),
             ('rail (waist)', rig.pose('rail')), ('clutch', rig.pose('clutch')),
             ('point', rig.pose('point', target=(700, -100))), ('reach', dict(rig.pose('sides'), **rig.pose('reach', target=(900, 200)))),
             ('typing', rig.pose('typing', tips={'L': (-120, 330), 'R': (70, 330)}, depth=0.35))]
    cw, ch = 360, 520
    img = Image.new('RGB', (cw * 4, ch * 2 + 40), (240, 238, 232))
    f = ImageFont.truetype(B.SANS, 18)
    for i, (name, arms) in enumerate(poses):
        canvas = B.canvas((246, 244, 240))
        B.person(canvas, B.Cam(1.0, 540, 960), 540, 760, 0.62, dict(base, arms=arms), 0.0)
        tile = canvas.convert('RGB').crop((90, 480, 990, 1780)).resize((cw, ch))
        img.paste(tile, ((i % 4) * cw, (i // 4) * ch))
        ImageDraw.Draw(img).text(((i % 4) * cw + 8, (i // 4) * ch + 8), name, font=f, fill=(20, 20, 20))
    try:
        audit_arm(rig.shoulder('L'), (-200 - 40, 280), (-480, 380), 'the old dinghy reach (typed by hand)')
        caught = 'NOT caught'
    except FigureError as e:
        caught = str(e)
    ImageDraw.Draw(img).text((8, ch * 2 + 10), caught[:150], font=f, fill=(170, 20, 30))
    img.save(out)
    print(caught)


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
