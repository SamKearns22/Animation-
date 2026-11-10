#!/usr/bin/env python3
"""MAP  Turned heads drawn FROM a person's own front face (Ad-Vanced Notice note 42e, 8 Nov: "neither the side nor the
three-quarter view looks like him: a different draw style, the eyes different in each pose").

Why the old turned heads failed: the front head is each person's measured face (patriots4 layout: u across, v down
from the top of the forehead, in face heights), but the side and three-quarter heads were one generic drawing
(views.head_view) that only borrowed the hair colour and beard kind. Turning him swapped in a different face.

The fix: TurnFace is the same frame as patriots4's Face (f(u, v) -> screen, f.pts), but on a 3D head. Each row v of
the head is a ring: its widest points are the front outline's edges (so at 0 degrees it IS the front head), a
flattish face in front (deeper at the muzzle), the skull behind. Turned by yaw (45 three-quarter, 90 side, 135 back
three-quarter, facing our right), every front-design point is carried round the head; a point past the head's edge
on the far side is held on that edge (never drawn through the head). So the person's own eyes, brows, beard, mouth
and hair shapes are drawn by their own code, moved and foreshortened round the head; only what has no front-view
drawing (the head's outline, the nose's bridge, the ear, the back of the hair) is drawn here, from the same rings.

    f = TurnFace(hx, hy, yaw, L, PROFILE)    f(u, v), f.pts(...), f.k(u, v) (how much a feature there narrows)
    outline(p, f, view, skin)                 the head's silhouette, inked except where it sits on the neck
    ear(p, f, skin)  nose(p, f, L, skin, prof)  hair(img, p, f, front_polys, colour, prof) -> mask, clipped(...)
    inside(img, p, head_poly, draw)           draw kept inside the head (a beard held round from behind)
    neck_over(p, f, view, skin)               from behind, the neck drawn again over the jaw (standing only)
    register(Person(...)); install(views)     any person with a front design turns (built when a shot needs it)
    squashed(p, cx, k)                        a pen that narrows a screen-drawn feature (an eye, a talking mouth)

Map: rings 38 | frame 54 | outline 206 | features 271 | hair 315 | people 420 (register, draw, install, fitted)
"""
import math
from contextlib import contextmanager

import numpy as np
import cv2

from ed import INK, curve, oval

H = 172.0                                   # patriots4's face height in person units (top of forehead to chin)
NECK = {'three': (-24, 40), 'side': (-26, 24), 'three_back': (-32, 32), 'back': (-32, 32)}   # views.torso_view's neck at its top


# ------------------------------------------------------------------------------------------------ rings
def _interp(keys, v):
    ks = sorted(keys)
    vs = [k[0] for k in ks]
    return float(np.interp(v, vs, [k[1] for k in ks]))


def half_widths(outline_uv):
    """The front outline's half width at each height (its right half), from the person's own outline_uv."""
    pts = sorted({(round(v, 4), abs(u)) for u, v in outline_uv if u >= -1e-9}, key=lambda q: q[0])
    best = {}
    for v, u in pts:
        best[v] = max(best.get(v, 0.0), u)
    return sorted(best.items())


# ------------------------------------------------------------------------------------------------ frame
class TurnFace:
    """patriots4.Face on a 3D head. PROFILE (face heights, the ear's plane at z = 0, + = towards the face):
    'front' [(v, z)]: the face's centre line from the side (forehead, brow ridge, the dip at the eyes, lips, chin);
    'back' [(v, z)]: the back of the head (skull, the nape, the jaw's back under the ear);
    'point' [(v, p)]: how pointed the face is in plan at that height (1 = round, more = a muzzle);
    'sockets': how far the eyes sit back from the face's surface; 'bottom': the lowest row (the chin with its beard);
    'hair_top' (hair): no hair above this row (a bald pate), 'hair_front' the angle the hair starts round from the face."""

    def __init__(self, hx, hy, yaw, L, prof, widths, down=0.0, turn=0.0):
        self.cx, self.top = hx + turn * 12, hy - 72 + 10 * down
        self.hx, self.tq, self.L, self.prof = hx, 0.0, L, prof
        self.th = math.radians(yaw)
        self.c, self.s = math.cos(self.th), math.sin(self.th)
        self.widths = widths
        self._vis = {}
        self.v0, self.v1 = min(widths[0][0], prof.get('crown', [(9, 0)])[0][0]), prof.get('bottom', 1.06)

    # the ring at height v ------------------------------------------------------------------------------------
    def a(self, v):
        w = self.widths
        chin = self.prof.get('chin')                # the chin's own half widths from below (rounder than the outline's)
        if chin and v >= chin[0][0]:
            return _interp(chin, v)
        crown = self.prof.get('crown')              # the top of the skull: round from behind (the front outline's
        if crown and v <= crown[-1][0]:             # crown is hidden under the hair and comes to a point)
            return max(_interp(crown, v), float(np.interp(v, [q[0] for q in w], [q[1] for q in w])))
        return float(np.interp(v, [q[0] for q in w], [q[1] for q in w]))

    def ring(self, psi, v):
        """(x, z) of the ring at height v, angle psi (degrees: 0 the face's centre, -90 our left edge, +-180 the back)."""
        psi = np.asarray(psi, float)
        r = np.radians(psi)
        a, zf, zb = self.a(v), _interp(self.prof['front'], v), _interp(self.prof['back'], v)
        pw = _interp(self.prof['point'], v)
        cs = np.cos(r)
        x = a * np.sin(r)
        if 'back_w' in self.prof:                  # behind the ears at jaw height it is the neck, not the jaw's width
            ab = min(a, _interp(self.prof['back_w'], v))
            x = np.where(cs >= 0, x, np.sin(r) * (ab + (a - ab) * (1 - np.abs(cs)) ** 2))
        zm = max(0.0, zb)                          # the ring's widest line: the ear's plane, or (under the jaw, where
        z = np.where(cs >= 0, zm + (zf - zm) * np.abs(cs) ** pw,  # the head ends in front of it) its own back
                     zm + (zb - zm) * np.abs(cs) ** 0.9)
        return x, z

    def view(self, x, z):
        return x * self.c + z * self.s, -x * self.s + z * self.c

    def visible(self, v):
        """The arc of the ring at v that faces the camera (psi from, to; it may run past +-180 round the back)."""
        key = round(v, 3)
        if key not in self._vis:
            ps = np.linspace(-180, 180, 721)
            x, z = self.ring(ps, v)
            _, Z = self.view(x, z)
            mid = ps[int(np.argmax(Z))]                  # the point facing us most; the arc is found round it
            ps = mid + np.linspace(-180, 180, 721)
            x, z = self.ring(ps, v)
            X, Z = self.view(x, z)
            dX = np.gradient(X)
            i = 360
            lo = i
            while lo > 0 and dX[lo - 1] > 0:
                lo -= 1
            hi = i
            while hi < len(ps) - 1 and dX[hi + 1] > 0:
                hi += 1
            self._vis[key] = (ps[lo], ps[hi])
        return self._vis[key]

    def hold(self, p, v):
        """A point's angle on the ring, kept on the visible arc: as it is if seen (the arc may run past +-180, so
        the same point a turn round counts); else held at the arc's end it would reach moving round towards the
        face's centre (a far cheek stays on the face's edge, never jumps to the back of the head)."""
        lo, hi = self.visible(v)
        for q in ((p, p - 360, p + 360) if abs(p) > 150 else (p,)):   # only the back of the head is seen "a turn
            if lo <= q <= hi:                                          # round"; a far cheek or jaw never is
                return q
        return hi if p > hi else lo

    def psi(self, u, v):
        a = max(self.a(v), 1e-6)
        if abs(u) <= a:
            return math.degrees(math.asin(u / a))
        return math.copysign(90 + (abs(u) - a) / a * 90, u)     # past the edge: on round the side of the head

    def wrap(self, v, deg):
        """The u that reaches angle `deg` at height v (beyond +-90: round the side of the head)."""
        a = self.a(v)
        if abs(deg) <= 90:
            return a * math.sin(math.radians(deg))
        return math.copysign(a + (abs(deg) - 90) / 90 * a, deg)

    def recess(self, u, v):
        """Eye sockets: the eyes sit back from the face's surface (so in profile the eye is behind the bridge)."""
        L, d = self.L, self.prof.get('sockets', 0.0)
        if not d or abs(u) > self.a(v):
            return 0.0
        du = (abs(u) - L['ecx']) / 0.09
        dv = (v - L['eye_y'] - 0.01) / 0.04
        return -d * math.exp(-(du * du + dv * dv) / 2)

    def at(self, u, v, dz=0.0, clamp=True):
        """Screen point of front-design (u, v), lifted dz off the surface (a nose, a wing of the nostril)."""
        p0 = p = self.psi(u, v)
        if clamp:
            p0 = p = self.hold(p, v)
        x, z = self.ring(p, v)
        z = float(z) + (self.recess(u, v) + dz if abs(p - p0) < 3.0 else 0.0)   # held on the edge: no lift
        X, _ = self.view(float(x), z)
        return (self.cx + X * H, self.top + v * H)

    def __call__(self, u, v):
        return self.at(u, v)

    def pts(self, uvs):
        return [self(u, v) for u, v in uvs]

    def k(self, u, v):
        """How square-on the face is to us at (u, v): 1 facing us, 0 edge on, < 0 turned away (the far side)."""
        p = self.psi(u, v)
        lo, hi = self.visible(v)
        p = next((q for q in (p, p - 360, p + 360) if lo - 1 <= q <= hi + 1), p)
        x0, z0 = self.ring(p - 1.0, v)
        x1, z1 = self.ring(p + 1.0, v)
        tx, tz = float(x1 - x0), float(z1 - z0)
        n = math.hypot(tx, tz) or 1.0
        return (tx * self.c + tz * self.s) / n


@contextmanager
def squashed(p, cx, k):
    """Draw a screen-space feature (an eye, a talking mouth) narrowed by k about x = cx: its pen's camera is swapped
    for the turn (the eye checker, views.Eyes, still notes it)."""
    base = p.pen if hasattr(p, 'pen') else p
    cam = base.cam

    class Sq:
        s, flip = cam.s, getattr(cam, 'flip', 1)

        def P(self, x, y):
            return cam.P(cx + (x - cx) * k, y)

        def S(self, v):
            return cam.S(v)

    base.cam = Sq()
    try:
        yield p
    finally:
        base.cam = cam


# ------------------------------------------------------------------------------------------------ outline
def silhouette(f, step=0.01):
    """The head's outline from the rings: the far edge top to bottom, the bottom row, the near edge back up.
    Returns [(x, y, v, part)] in head units; part is 'far', 'bottom' or 'near'."""
    vs = np.arange(f.v0, f.v1 + 1e-9, step)
    ps = np.linspace(-180, 180, 361)
    far, near = [], []
    for v in vs:
        x, z = f.ring(ps, v)
        X, _ = f.view(x, z)
        y = f.top + v * H
        far.append((f.cx + X.max() * H, y, v, 'far'))
        near.append((f.cx + X.min() * H, y, v, 'near'))
    bot = [(far[-1][0] + (near[-1][0] - far[-1][0]) * t, far[-1][1], f.v1, 'bottom') for t in np.linspace(0, 1, 12)[1:-1]]
    return far + bot + near[::-1]


def inside(img, p, poly, draw):
    """Draw `draw(pen)` kept inside the head's outline (a face seen from behind: the beard's far edge, held round
    the head, never spills over the neck)."""
    from PIL import Image, ImageDraw
    import burnham as B
    base = p.pen if hasattr(p, 'pen') else p
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw(B.Pen(layer, base.cam))
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).polygon([base.cam.P(*q) for q in poly], fill=255)
    a = np.asarray(layer)[:, :, 3].astype(np.uint16) * np.asarray(m) // 255
    layer.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(layer)


def outline(p, f, view, skin, lw=2.6, fill=True, ink=True, whole=False):
    """Fill the head in skin and ink its edge, except where the edge only crosses the neck (from the side the neck
    carries on down from the nape and the throat; from behind it rises into the head)."""
    sil = silhouette(f)
    poly = [(x, y) for x, y, _, _ in sil]
    if fill:
        p.poly(poly, skin, None)
    if not ink:
        return poly
    n0, n1 = (0, 0) if whole else NECK.get(view, (0, 0))   # whole: inked all round (no neck runs into it)
    hx = f.hx

    def inked(q):
        x, y, v, part = q
        if view in ('three', 'side') or v < 0.8:      # side on, the jaw overhangs the neck and the nape meets it
            return True
        on_neck = hx + n0 + 2 <= x <= hx + n1 - 2
        if view == 'side':
            return not (on_neck and part in ('near', 'bottom'))
        return not on_neck                         # from behind: the nape runs into the neck
    run = []
    for q in sil + sil[:1]:
        if inked(q):
            run.append((q[0], q[1]))
        elif run:
            if len(run) > 1:
                p.line(run, INK, lw)
            run = []
    if len(run) > 1:
        p.line(run, INK, lw)
    return poly


# ------------------------------------------------------------------------------------------------ features
def ear(p, f, skin, v=0.42, deg=-91):
    """The near ear, on the side of the head (the far ear is hidden from 30 degrees round)."""
    x, z = f.ring(deg, v)
    X, Z = f.view(float(x), float(z))
    if Z < -0.05:
        return
    ex, ey = f.cx + X * H, f.top + v * H
    face = max(0.45, abs(math.sin(math.radians(deg)) * f.s - math.cos(math.radians(deg)) * 0))   # side on: full
    rx, ry = 11 + 8 * face, 24
    p.poly(oval(ex, ey, rx, ry, 20), skin, INK, 2.4)
    p.line(curve([(ex + rx * 0.35, ey - ry * 0.6), (ex - rx * 0.35, ey - ry * 0.45), (ex - rx * 0.45, ey + ry * 0.1),
                  (ex - rx * 0.1, ey + ry * 0.55)], 3), INK, 1.4)
    p.line([(ex + rx * 0.05, ey - ry * 0.1), (ex + rx * 0.3, ey + ry * 0.12)], tuple(int(c * 0.7) for c in skin), 1.6)
    return ex, ey


def nose(p, f, L, skin, prof):
    """The nose from the side and three-quarter: the bridge from between the eyes out to the tip and back under to the
    nostril (its far edge is the bridge's silhouette), the near nostril's wing, a nostril."""
    ny, ey, nw = L['nose_y'], L['eye_y'], L['nw']
    tip, length = prof.get('nose_tip', 0.2), prof.get('nose_v', 0.03)
    sd = tuple(int(c * 0.72) for c in skin)
    ball = prof.get('nose_ball', 0.0)                      # a rounder nose: the bridge fuller, the tip a bigger
    nas = f.at(0.0, ey + 0.01, 0.0)                         # ball that turns back under more gently (the driver)
    mid = f.at(0.0, (ey + ny) / 2, tip * (0.55 + 0.17 * ball))
    top = f.at(0.0, ny - length - 0.06 - 0.02 * ball, tip * (0.9 - 0.04 * ball))   # the tip is a ball, not a point
    tp = f.at(0.0, ny - length - 0.015, tip)
    low = f.at(0.0, ny - length + 0.025 + 0.012 * ball, tip * (0.9 - 0.04 * ball))
    und = f.at(0.0, ny + 0.002, tip * (0.5 + 0.2 * ball))
    base = f.at(0.0, ny + 0.01, 0.02)
    back = [f.at(-0.06, ny + 0.01, 0.0), f.at(-0.06, ey + 0.04, 0.0)]
    bridge = curve([nas, mid, top, tp], 4)
    under = curve([tp, low, und, base], 4)
    p.poly(bridge + under + back, skin, None)
    p.line(bridge + under[1:], INK, 2.0)
    wing = [f.at(-nw * 0.26, ny - 0.075, 0.05), f.at(-nw * 0.42, ny - 0.05, 0.05), f.at(-nw * 0.42, ny - 0.012, 0.04),
            f.at(-nw * 0.24, ny + 0.002, 0.04)]
    p.line(curve(wing, 3), INK, 1.8)
    if f.s < 0.95:                                 # three-quarter: the near nostril shows under the tip
        nx, nyy = f.at(-nw * 0.12, ny - 0.01, tip * 0.45)
        p.poly(oval(nx, nyy, 5 * max(0.5, f.c + 0.3), 3, 10), tuple(int(c * 0.5) for c in skin), None)
    p.line([f.at(-0.025, ey + 0.04, 0.0), f.at(-0.04, ny - 0.09, tip * 0.2)], sd, 1.6)


# ------------------------------------------------------------------------------------------------ hair
def hair_top(prof, ap, psi):
    """The highest row with hair at angle psi (ap: its distance from the face, degrees): none set, no limit. A bald
    pate's horseshoe: 'hair_top' at the temples falling to 'hair_top_back' behind, its edge uneven by 'hair_ragged'."""
    top = prof.get('hair_top')
    if top is None:
        return -9.0
    back = prof.get('hair_top_back', top)
    top = top + (back - top) * min(1.0, max(0.0, (ap - 90) / 90))
    rag = prof.get('hair_ragged', 0.0)
    return top + rag * (math.sin(math.radians(psi) * 11) + 0.5 * math.sin(math.radians(psi) * 23 + 1.0))


def hair(img, p, f, fronts, colour, prof, lw=2.4):
    """The hair as one mass: the person's own front hair shapes (carried round by f) and the back of the head
    (sampled over the rings behind the front hair, down to the nape), filled and inked round as one shape (no line
    where they meet). fronts: polygons already in head units (f.pts of the front design)."""
    base = p.pen if hasattr(p, 'pen') else p
    cam = base.cam
    W, Hh = img.size
    pts = []
    vs = np.arange(f.v0, prof.get('nape', 0.64) + 1e-9, 0.008)
    for v in vs:
        lo, hi = f.visible(v)
        bottom_side = prof.get('hair_low', 0.36)
        for psi in np.arange(lo, hi + 1e-9, 1.5):
            ap = abs((psi + 180) % 360 - 180)
            vb = bottom_side if ap < 100 else bottom_side + (prof.get('nape', 0.64) - bottom_side) * min(1, (ap - 100) / 30)
            if v > vb or (ap < prof.get('hair_front', 84) and v > -0.2):
                continue
            if v < hair_top(prof, ap, psi):        # a bald pate: hair only in a band round the sides and back
                continue
            x, z = f.ring(psi, v)
            puff = 1.0 + prof.get('volume', 0.03) * (1 - max(0.0, v) / 0.7)
            X, _ = f.view(float(x) * puff, float(z) * puff)
            pts.append(cam.P(f.cx + X * H, f.top + (v - 0.012 * min(1.0, max(0.0, -v / 0.3))) * H))
    xs = [q[0] for q in pts] + [q[0] for poly in fronts for q in (cam.P(*r) for r in poly)]
    ys = [q[1] for q in pts] + [q[1] for poly in fronts for q in (cam.P(*r) for r in poly)]
    if not xs:
        return None
    pad = 12
    x0, y0 = int(max(0, min(xs) - pad)), int(max(0, min(ys) - pad))
    x1, y1 = int(min(W, max(xs) + pad)), int(min(Hh, max(ys) + pad))
    if x1 <= x0 or y1 <= y0:
        return None
    m = np.zeros((y1 - y0, x1 - x0), np.uint8)
    if pts:                                        # the back of the head: dense samples joined into one shape
        q = np.round(np.array(pts) - (x0, y0)).astype(int)
        ok = (q[:, 0] >= 0) & (q[:, 0] < m.shape[1]) & (q[:, 1] >= 0) & (q[:, 1] < m.shape[0])
        m[q[ok, 1], q[ok, 0]] = 255
        r = max(2, int(round(cam.S(2.6))))
        m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)))
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 3, 2 * r + 3)))
        m = cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (r + 1, r + 1)))
    for poly in fronts:                            # the front design's own hair, exactly
        q = np.array([cam.P(*r) for r in poly], float) - (x0, y0)
        cv2.fillPoly(m, [np.round(q).astype(np.int32)], 255)
    o = max(2, int(round(cam.S(2.2))))             # no slivers: hair carried past the far edge piles up there as a
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * o + 1, 2 * o + 1)))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)   # thread along the profile: opened away
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    big = max((cv2.contourArea(c) for c in cs), default=0)
    for c in cs:
        if cv2.contourArea(c) < max(30, 0.03 * big):     # a crumb left on the far edge: not hair
            continue
        c = c[:, 0, :].astype(float)
        k = max(3, len(c) // 60)
        c = np.array([c[np.arange(i - k, i + k + 1) % len(c)].mean(0) for i in range(len(c))])[::2]
        q = [(x + x0, y + y0) for x, y in c]
        d.polygon(q, fill=colour)
        d.line(q + q[:1], fill=INK, width=base.w(lw), joint='curve')
    return m, x0, y0


def clipped(img, p, mask, draw):
    """Draw `draw(pen)` (hair strokes, a parting) kept inside the hair's shape (mask from hair()), clear of its ink."""
    from PIL import Image
    if mask is None:
        return
    m, x0, y0 = mask
    base = p.pen if hasattr(p, 'pen') else p
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    import burnham as B
    draw(B.Pen(layer, base.cam))
    keep = cv2.erode(m, np.ones((5, 5), np.uint8))
    full = np.zeros((img.size[1], img.size[0]), np.uint8)
    full[y0:y0 + m.shape[0], x0:x0 + m.shape[1]] = keep
    a = np.asarray(layer)[:, :, 3].astype(np.uint16) * full // 255
    layer.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(layer)


def neck_over(p, f, view, skin, v_top=0.7, lw=2.6):
    """From behind, the neck is nearer than the jaw: its top drawn again over the head's lower half (up to the nape),
    so only the near cheek shows beside it."""
    n0, n1 = NECK.get(view, (-32, 32))
    y0, y1 = f.top + v_top * H, f.top + (f.v1 + 0.04) * H     # down past the head's lowest row
    hx = f.hx
    out = lambda x, y: hx + x + (1 if x > 0 else -1) * 4 * (y + 80) / 90    # the body's neck widens 4 a 90 down
    p.poly([(out(n0, y0), y0), (out(n1, y0), y0), (out(n1, y1), y1), (out(n0, y1), y1)], skin, None)
    for x in (n0, n1):
        p.line([(out(x, y0), y0), (out(x, y1), y1)], INK, lw)


def dense(uv, step=0.01):
    """A shape's points every `step` (face fractions), so that held on the far edge it follows the edge's curve."""
    out = []
    for (u0, v0), (u1, v1) in zip(uv, uv[1:] + uv[:1]):
        n = max(1, int(math.hypot(u1 - u0, v1 - v0) / step))
        out += [(u0 + (u1 - u0) * i / n, v0 + (v1 - v0) * i / n) for i in range(n)]
    return out


# ------------------------------------------------------------------------------------------------ people
# (Job I faces, Sam 11 Nov: "a turned head for ANY character, but built only when a shot needs it".) Any person whose
# front head is a measured patriots4 layout can turn: their cast file registers a Person (the few pieces only they
# have: hair, beard, mood) and install(views) sends views.head_view's turned views to it. A person's head is built (its
# layout, rings and measures) the first time a shot draws it turned, never before; every (person, view) drawn is
# recorded in SEEN, and one a shot asks for that has no Person yet in MISSING, so pre-flight lists both and puts the
# turnaround of exactly those on the check sheet.
YAW = {'three': 45, 'side': 90, 'three_back': 135, 'back': 180}

# The standard head (Vance's, measured for Ad-Vanced Notice note 44: 1.15 face heights deep, brow to the back of the
# skull, the ear at its middle), at the rows of his own front layout. fitted() moves it to anyone else's rows.
TEMPLATE = dict(
    front=[(-0.42, -0.08), (-0.38, 0.1), (-0.3, 0.22), (-0.2, 0.31), (-0.1, 0.37), (0.0, 0.42), (0.15, 0.46),
           (0.265, 0.495), (0.34, 0.445), (0.45, 0.46), (0.552, 0.47), (0.62, 0.49), (0.65, 0.475), (0.70, 0.485),
           (0.76, 0.44), (0.84, 0.455), (0.92, 0.47), (0.97, 0.44), (1.0, 0.40), (1.06, 0.30)],
    back=[(-0.42, -0.08), (-0.38, -0.28), (-0.3, -0.39), (-0.2, -0.47), (-0.1, -0.52), (0.0, -0.55), (0.15, -0.57),
          (0.3, -0.56), (0.45, -0.5), (0.55, -0.44), (0.62, -0.31), (0.68, -0.21), (0.76, -0.16), (0.82, -0.14),
          (0.9, -0.03), (1.0, 0.14), (1.06, 0.25)],
    crown=[(-0.43, 0.000), (-0.425, 0.088), (-0.415, 0.138), (-0.4, 0.182), (-0.38, 0.222), (-0.36, 0.252),
           (-0.32, 0.296), (-0.28, 0.326), (-0.24, 0.348), (-0.2, 0.365), (-0.15, 0.379), (-0.1, 0.387),
           (-0.05, 0.391), (0.0, 0.392)],   # a round dome to the temples' width
    back_w=[(0.5, 0.5), (0.62, 0.36), (0.72, 0.2), (1.06, 0.18)],
    point=[(-0.42, 0.8), (0.2, 0.9), (0.34, 1.2), (0.5, 1.5), (0.7, 1.6), (0.9, 1.4), (1.06, 1.2)],
    chin=[(0.965, 0.193), (1.0, 0.15), (1.035, 0.09), (1.06, 0.0)],
    sockets=0.07, nose_tip=0.15, nose_v=0.03, bottom=1.06, nape=0.7, hair_low=0.36, volume=0.03)
TEMPLATE_ROWS = dict(crown=-0.42, brow_y=0.265, eye_y=0.32, nose_y=0.552, lip13=0.646, bottom=1.06, nw=0.332)


def fitted(L, crown_v, bottom, **own):
    """The standard head moved to a person's own front layout L: its rows (crown, brow, eyes, nose, mouth, chin) slid
    to theirs, the nose's reach scaled by their nose's width; `own` overrides any measure (a bald dome, their chin)."""
    T = TEMPLATE_ROWS
    a = (T['crown'], 0.0, T['brow_y'], T['eye_y'], T['nose_y'], T['lip13'], T['bottom'])
    b = (crown_v, 0.0, L['brow_y'], L['eye_y'], L['nose_y'], L['lip13'], bottom)
    rows = lambda pts: [(float(np.interp(v, a, b)), z) for v, z in pts]
    prof = dict(TEMPLATE, bottom=bottom, nose_tip=TEMPLATE['nose_tip'] * L['nw'] / T['nw'])
    for key in ('front', 'back', 'point', 'back_w', 'chin'):
        prof[key] = rows(TEMPLATE[key])
    prof['crown'] = [(float(np.interp(v, a, b)), z) for v, z in TEMPLATE['crown']]
    prof.update(own)
    return prof


class Person:
    """What one person's turned head needs from their cast file (front design pieces only they have).
    layout(sp) -> L; crown: the outline's crown (patriots4.outline_uv); widths_pad: outline_uv's padding;
    profile(L) -> PROFILE (usually fitted(L, ...)); skin, iris, brow and lip colours; mood(sp, f) -> (eye state, brow
    raise, frown);
    face(pen, f, L, sp): drawn on the skin inside the head (a beard); over(img, p, f, L, sp, view): after the outline
    (a shine, a goatee that stands off the chin); mouth(p, f, L, sp, fx, my): the resting lips; hair(img, p, f, L, sp);
    hood: hooded outer eye corners; brow_thick; sheet: the cast entry the turnaround draws."""

    def __init__(self, who, layout, crown, pad, profile, skin, iris, brow_c, lip_c, mood, mouth, hair, face=None,
                 over=None, hood=False, brow_thick=0.05, sheet=None):
        self.who, self.layout, self.crown, self.pad, self.profile = who, layout, crown, pad, profile
        self.lip_c = lip_c
        self.skin, self.iris, self.brow_c, self.mood, self.mouth, self.hair = skin, iris, brow_c, mood, mouth, hair
        self.face, self.over, self.hood, self.brow_thick, self.sheet = face, over, hood, brow_thick, sheet
        self.built = {}

    def build(self, sp):
        """(L, profile, widths): made the first time a shot needs this person turned, then kept."""
        key = bool(sp.get('average', False))
        if key not in self.built:
            import patriots4_cast as P4
            L = self.layout(sp)
            self.built[key] = (L, self.profile(L), half_widths(P4.outline_uv(L, self.pad, crown=self.crown)))
        return self.built[key]


PEOPLE = {}
SEEN, MISSING = [], []          # (who, view) drawn turned; (who, view) asked for with no Person (pre-flight reads)


def register(person):
    PEOPLE[person.who] = person
    return person


def draw(img, p, sp, t, view, hx, hy):
    """A registered person's head from three-quarter (45), the side (90), three-quarter behind (135) or behind,
    facing our right: their own front face carried round the head."""
    P = PEOPLE[sp['who']]
    L, prof, widths = P.build(sp)
    SEEN.append((P.who, view))
    f = TurnFace(hx, hy, YAW[view], L, prof, widths, sp.get('down', 0.0), sp.get('turn', 0.0))
    skin = P.skin
    st, raise_, frown = P.mood(sp, f)
    head = outline(p, f, view, skin, ink=False)
    if P.face and view != 'back':                             # from straight behind a beard is hidden
        inside(img, p, head, lambda pen: P.face(pen, f, L, sp))
    lying = bool(sp.get('nape_in_head'))              # lying (lying_flat): the collar, not a neck, meets the nape
    outline(p, f, view, skin, fill=False, whole=lying)    # (Sam, 11 Nov, lying 18: the neck drawn over the head,
    if view in ('three_back', 'back') and not lying:      # tipped off its neck, was a square block, a blindfold
        neck_over(p, f, view, skin)                       # with his hair band): the head inked all round, no neck
    if P.over:
        P.over(img, p, f, L, sp, view)
    fx, my = f(0.0, L['lip13'])
    if view not in ('three_back', 'back'):
        eyes(p, f, L, st, P.iris, skin, hood=P.hood and not sp.get('blink'))
        brows(p, f, L, P.brow_c, raise_, frown, P.brow_thick)
        nose(p, f, L, skin, prof)
        mouth(p, f, L, sp, P.lip_c, lambda: P.mouth(p, f, L, sp, fx, my))
    P.hair(img, p, f, L, sp)
    ear(p, f, skin)
    if view == 'back':                                        # straight from behind: both ears
        ear(p, f, skin, deg=91)
    return fx


def install(V):
    """views.head_view's turned views go to the person's own turned head when they have one; a person with a measured
    front design but no Person yet is recorded (pre-flight: build it) and drawn the old way. Installed once."""
    if getattr(V.head_view, 'turnhead', False):
        return
    old = V.head_view

    def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
        who = sp.get('who')
        if view in YAW and who in PEOPLE:
            return draw(img, p, sp, t, view, hx, hy)
        if view in YAW and who:
            import patriots4_cast as P4
            if who in P4.MEASURED:
                MISSING.append((who, view))
        return old(img, p, sp, t, view, hx, hy)
    head_view.turnhead = True
    V.head_view = head_view


def eyes(p, f, L, st, iris, skin, hood=False):
    """A turned face's eyes (traitors_cast.eye, as the front design draws them), each narrowed as it turns; the far one
    hidden behind the bridge of the nose once it turns away. hood: hooded outer corners (Vance)."""
    import patriots4_cast as P4
    import traitors_cast as TC
    dk = lambda c, k: tuple(int(x * k) for x in c)
    w, h = L['ew'] * P4.H / 2, L['eh'] * P4.H / 1.8
    for sgn in (-1, 1):
        u = sgn * L['ecx']
        k = f.k(u, L['eye_y'])
        if k < 0.3:                                           # turned away: hidden behind the bridge of the nose
            continue
        k = max(k, 0.55) if sgn < 0 else k                    # an eye is a ball: from the side it still shows
        ex, ey = f(u, L['eye_y'])
        with squashed(p, ex, k):
            TC.eye(p, ex, ey, sgn, w, h, iris, st, dk(skin, 0.82), liner=2.6)
            if hood:
                hd = [(ex + sgn * w * 0.05, ey - h * 1.25), (ex + sgn * w * 1.2, ey - h * 1.0),
                      (ex + sgn * w * 1.12, ey + h * 0.15), (ex + sgn * w * 0.6, ey - h * 0.55),
                      (ex + sgn * w * 0.05, ey - h * 0.92)]
                p.poly(hd, skin, None)
                p.line(curve([(ex + sgn * w * 0.05, ey - h * 0.92), (ex + sgn * w * 0.6, ey - h * 0.55),
                              (ex + sgn * w * 1.12, ey + h * 0.15)], 3), INK, 2.4)


def brows(p, f, L, col, raise_, frown, thick=0.05):
    """patriots4.brows on a turned face: the far brow only while it is seen."""
    for sgn in (-1, 1):
        if f.k(sgn * L['ecx'], L['brow_y']) < 0.3:
            continue
        ecx, ew = L['ecx'], L['ew']
        xi, xo, xm = ecx - 0.69 * ew, ecx + 0.98 * ew, ecx + 0.21 * ew
        up_ = raise_[0 if sgn < 0 else 1] if isinstance(raise_, (tuple, list)) else raise_
        y_m = L['brow_y'] - thick * 0.35 - up_
        yi, yo, ym = y_m + L['slope'] * (xm - xi) + frown, y_m - L['slope'] * (xo - xm), y_m - 0.008
        uv = [(xi, yi - thick * 0.45), (xm, ym - thick * 0.6), (xo, yo - thick * 0.2), (xo + 0.01, yo + thick * 0.15),
              (xm, ym + thick * 0.45), (xi, yi + thick * 0.55)]
        p.poly(curve(f.pts([(sgn * u, v) for u, v in uv]), 3), col, None)


def mouth(p, f, L, sp, lip_c, rest):
    """A turned face's mouth: a talking shape (mouths.draw) narrowed round the head, else rest() (its own lips)."""
    m = sp.get('mouth', 'rest')
    if isinstance(m, str) and m.startswith('v:') and m != 'v:rest':
        import mouths
        u = -L['mw'] * 0.22 * f.s                             # the mouth's middle, nearer the corner we see
        cx, my2 = f(u, L['lip13'])
        with squashed(p, cx, max(0.4, f.k(u, L['lip13']))):
            mouths.draw(p, dict(sp, lips=True, lip_c=lip_c), cx, my2 - 6, m[2:])
        return True
    rest()
    return False


NAMES = {'front': 'front', 'three': 'three-quarter', 'side': 'side', 'three_back': 'three-quarter behind',
         'back': 'behind'}


def turnaround(pairs, moods=None, first=None):
    """The turnaround of exactly these (who, view) pairs: each person's front beside the views a shot needs (pre-flight
    puts it on the check sheet; Sam's faces sheet). moods: {who: [sp overrides per row]}; a person with no Person
    (MISSING) shows the old drawing, labelled. -> PIL image, or None for no pairs."""
    from PIL import Image, ImageDraw, ImageFont
    import burnham as B
    import views as V
    who_views = {}
    for who, view in pairs:
        who_views.setdefault(who, set()).add(view)
    if not who_views:
        return None
    order = ('front', 'three', 'side', 'three_back', 'back')
    yaw = dict(YAW, front=0)
    tw, th = 330, 400
    rows = [(who, m) for who in who_views for m in (moods or {}).get(who, [{}])]
    cols = max(1 + len(v - {'front'}) for v in who_views.values())
    img = Image.new('RGB', (tw * cols, (th + 40) * len(rows)), (232, 228, 222))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(B.SANS, 22)
    ss = B.SS
    B.SS = 1
    try:
        for r, (who, extra) in enumerate(rows):
            P = PEOPLE.get(who)
            sp = dict(P.sheet() if P and P.sheet else {'who': who}, **extra)
            views = ['front'] + [v for v in order if v in who_views[who] and v != 'front']
            for c, view in enumerate(views):
                im = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
                V.person(im, B.Cam(1.0, 540, 960), 540, 1060, 1.25, sp, 0.0, yaw[view])
                img.paste(im.crop((375, 620, 705, 1020)).convert('RGB'), (tw * c, (th + 40) * r + 40))
                n = f'{first + r * cols + c}: ' if first else ''   # numbered on from another sheet (Sam answers by number)
                lab = f"{n}{sp.get('name', who)}, {NAMES[view]}" + ('' if P or view == 'front' else ' (OLD: no turned head)')
                d.text((tw * c + 8, (th + 40) * r + 10), lab + (f" {extra.get('label', '')}" if extra else ''),
                       font=font, fill=(40, 40, 40))
    finally:
        B.SS = ss
    return img


if __name__ == '__main__':
    # python3 source/turnhead.py sheet OUT.jpg CAST_MODULE WHO [VIEW ...] [--from N]   a person all the way round
    # (or these views), the panels numbered from N
    import importlib
    import sys
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        importlib.import_module(a[2])               # the cast registers its people on the module 'turnhead'
        T = importlib.import_module('turnhead')       # (run as a script this file is also '__main__')
        first = int(a[a.index('--from') + 1]) if '--from' in a else None
        vs = [v for v in a[4:] if v in YAW] or list(YAW)
        T.turnaround([(a[3], v) for v in vs], first=first).save(a[1], quality=90)
        print(a[1])
