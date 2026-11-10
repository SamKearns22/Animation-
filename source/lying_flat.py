#!/usr/bin/env python3
"""MAP  lying_flat: people lying down drawn in the house style (Job I, Sam 10 Nov: "the lying down people don't look
right at all ... squiggly balloon people with inflated heads, not at all like how our characters look usually").

Cause: lying.draw painted its own look (rounded 3D tubes and balls, a 3D head with the face laid on it), never
compared with the cast. Fix: the 3D skeleton (lying.Body: poses, contacts, checks, the floor shadow) is kept; only
the drawing changes. Every joint is projected through the camera and the flat rig's own pieces are laid along them:

- the torso: the rig's own torso drawing (front, three, side, three_back, back: views.torso_view / burnham.torso),
  fitted to the projected neck, shoulders, hips and chest (one flat drawing turned and foreshortened, never lumpy);
- the arms: the rig's sleeves (B.arm, joined to the torso's outline as standing) and circle hands;
- the legs: the rig's leg tube (views.tube, the same widths) and the shoe outline round the shoe's 3D box;
- the head: the rig's own head drawing at the rig's size (never squashed by the camera), turned with the neck;
- nearer pieces over farther ones (an arm across the chest over it; arms out on the floor under the shoulders).

Map: cams 30 | frame and view 75 | pieces 120 | draw 190

    python3 source/lying_flat.py sheet OUT.jpg     Vance standing beside his lying versions (old drawing and new)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import views as V            # noqa: E402
from ed import INK, curve    # noqa: E402

BACKS = ('three_back', 'back')                         # trunk views seen from behind
HEAD_TILT = 35.0                                       # degrees the head may tip off the trunk's line
_N = [0]


# ---------------------------------------------------------------------------------------------- cams
class _Cam:
    """Drawing units -> frame pixels. `ox, oy, k` name the person (limbs joins an arm only to its own body)."""
    def __init__(self, s, tag):
        self.s, self.k = s, 1.0
        self.ox, self.oy = float(tag), 0.0

    def S(self, v):
        return v * self.s * B.SS


class ScreenCam(_Cam):
    """Frame coordinates divided by s: limbs drawn between projected joints, widths in person units."""
    def P(self, x, y):
        return x * self.s * B.SS, y * self.s * B.SS


class AffCam(_Cam):
    """The rig's own drawing coordinates (neck at 0, 0; person units) through an affine map onto the frame."""
    def __init__(self, A, t, s, tag):
        super().__init__(s, tag)
        self.A, self.t = A, t

    def P(self, x, y):
        q = self.A @ (x, y) + self.t
        return q[0] * B.SS, q[1] * B.SS


class HeadCam(_Cam):
    """The head drawing at the rig's size, turned about the neck base: never squashed (a head looks round from
    anywhere, as views' Tilted keeps it), its crown along the projected neck-to-head line."""
    def __init__(self, neck, rvec, dvec, s, tag):
        super().__init__(s, tag)
        self.n, self.r, self.d = np.asarray(neck, float), np.asarray(rvec, float), np.asarray(dvec, float)

    def P(self, x, y):
        q = self.n + (self.r * x + self.d * y) * self.s
        return q[0] * B.SS, q[1] * B.SS


def _unit(a):
    a = np.asarray(a, float)
    return a / (np.linalg.norm(a) or 1.0)


# ---------------------------------------------------------------------------------------------- frame and view
def frame(k):
    """The trunk's axes: X (to its right shoulder), up (pelvis to neck), fwd (its front)."""
    up = _unit(k['neck'] - k['pelvis'])
    X = _unit((k['shR'] - k['shL']) - up * np.dot(k['shR'] - k['shL'], up))
    fwd = np.asarray(k['fwd'], float)
    fwd = _unit(fwd - up * np.dot(fwd, up) - X * np.dot(fwd, X))
    return X, up, fwd


def yaw_seen(d, X, fwd):
    """views' yaw (0 facing us, 90 facing right, 180 away) of a body whose axes are X, fwd, seen from direction d."""
    return math.degrees(math.atan2(-np.dot(d, X), np.dot(d, fwd)))


def _proj(cam, p):
    return np.asarray(cam.project(tuple(np.asarray(p, float)))[0], float)


def _torso_fit(cam, k, sp, view_deg, X, up, fwd, M):
    """The affine map (A, t) from the rig's torso drawing to the frame, by least squares on the neck, shoulders,
    hips and the chest's front and back."""
    sw = sp.get('shoulders', 150)
    mid = (k['neck'] + k['pelvis']) / 2
    src, dst = [], []
    pts = [((0, 0, 0), k['neck']),
           ((-(sw - 14), 60, 0), k['shL']), ((sw - 14, 60, 0), k['shR']),
           ((-55, V.HIP_Y, 0), k['hipL']), ((55, V.HIP_Y, 0), k['hipR']),
           ((0, 225, 70), mid + fwd * 70 * M), ((0, 225, -70), mid - fwd * 70 * M),
           ((-(sw - 14), 225, 0), mid - X * (sw - 14) * M), ((sw - 14, 225, 0), mid + X * (sw - 14) * M)]
    old = V._E[0]
    V._E[0] = 0.0
    try:
        for p3, w in pts:
            src.append(V.project(p3, view_deg)[0])
            dst.append(_proj(cam, w))
    finally:
        V._E[0] = old
    S_ = np.c_[np.asarray(src, float), np.ones(len(src))]
    sol, *_ = np.linalg.lstsq(S_, np.asarray(dst, float), rcond=None)
    return sol[:2].T, sol[2]


# ---------------------------------------------------------------------------------------------- pieces
def _limb_piece(p, pts, widths, col, lw=2.6, keep=None):
    """One limb as ONE shape (Sam, 10 Nov: legs "clipping and not one fluid part"): the thigh and shin as tapered
    pieces with round joints, filled together on a mask, one ink outline round the whole (no lines inside at the knee,
    however tightly it folds)."""
    from PIL import ImageFilter
    img = p.img
    m = Image.new('L', img.size, 0)
    d = ImageDraw.Draw(m)
    P = [np.asarray(p.cam.P(*q), float) for q in pts]
    R = [abs(p.cam.S(w)) for w in widths]
    for a, b, ra, rb in zip(P, P[1:], R, R[1:]):
        t = b - a
        n = np.array([-t[1], t[0]]) / (np.linalg.norm(t) or 1)
        d.polygon([tuple(a + n * ra), tuple(b + n * rb), tuple(b - n * rb), tuple(a - n * ra)], fill=255)
    for c, r in zip(P, R):
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=255)
    w = max(1, int(round(p.w(lw))))
    ring = m.filter(ImageFilter.MaxFilter(2 * w + 1))
    if keep is not None:                              # only the part past the hem shows (its cut has no outline:
        from PIL import ImageChops                    # the hem's own line is there)
        a, n = (np.asarray(v, float) for v in keep)
        a = np.asarray(p.cam.P(*a), float)
        b = np.asarray(p.cam.P(*(np.asarray(keep[0], float) + n)), float)
        nn = _unit(b - a)
        tt = np.array([-nn[1], nn[0]]) * 1e5
        h = Image.new('L', img.size, 0)
        ImageDraw.Draw(h).polygon([tuple(a + tt), tuple(a - tt), tuple(a - tt + nn * 1e5), tuple(a + tt + nn * 1e5)],
                                  fill=255)
        hd = ImageDraw.Draw(h)                        # the knee and shin always show (Sam, round 3: cut at
        for a2, b2, ra, rb in zip(P[1:], P[2:], R[1:], R[2:]):   # the hem, the bent knee didn't read)
            t2 = b2 - a2
            n2 = np.array([-t2[1], t2[0]]) / (np.linalg.norm(t2) or 1)
            ra, rb = ra + w + 1, rb + w + 1
            hd.polygon([tuple(a2 + n2 * ra), tuple(b2 + n2 * rb), tuple(b2 - n2 * rb), tuple(a2 - n2 * ra)], fill=255)
        for c, r in zip(P[1:], R[1:]):
            hd.ellipse([c[0] - r - w - 1, c[1] - r - w - 1, c[0] + r + w + 1, c[1] + r + w + 1], fill=255)
        m, ring = ImageChops.multiply(m, h), ImageChops.multiply(ring, h)
    img.paste(INK, (0, 0), ring)
    img.paste(tuple(col), (0, 0), m)


def _leg(p, sc, cam, k, side, sp, M, front=False):
    """One piece from hip to ankle, one outline (Sam, 10 Nov). `front`: the knee is nearer than the trunk, so the
    whole leg is drawn after it (Sam, 10 Nov round 2: the knee to the shoe drawn on its own over a thigh under the
    shirt showed a seam at the knee (13), a ball for a knee (12) and a shin out of the chest (14, 17)). A knee past
    the hem: only the part past the hem shows, so the leg comes out from under the shirt; a knee drawn up over the
    shirt: the thigh shows over it from the hip."""
    s = sc.s
    pts = [_proj(cam, k[n + side]) / s for n in ('hip', 'kn', 'an')]
    pts[0] = sc.hips[side]
    lk = sp.get('leg_k', 1.0)
    col = sp.get('trousers', (40, 40, 46))
    keep = None
    if front and sc.hem is not None:
        a, b, up = sc.hem
        a = (a + b) / 2                               # the hem across the trunk's own up (seen side on, its two
        n = -np.asarray(up, float)                    # ends meet: Sam, round 4, a thigh from mid-shirt in 11)
        if np.dot(pts[1] - a, n) > 0:                  # the knee is past the hem
            keep = (a, _unit(n))
    _limb_piece(p, [tuple(q) for q in pts], [48 * lk, 38 * lk, 27 * lk], col, keep=keep)
    _shoe(p, sc, cam, k, side, sp, M)


def _shoe(p, sc, cam, k, side, sp, M):
    """The shoe: the rig's shoe box (56 wide, 36 ankle to sole, heel 28 behind to toe 92 ahead) in 3D, its outline;
    the sole drawn lighter when it faces the camera (soles up, face down)."""
    an, t, su = k['an' + side], _unit(k['toe' + side]), _unit(k['sup' + side])
    xs = _unit(np.cross(su, t))

    def w(dx, dy, dz):
        return an + xs * dx * M - su * dy * M + t * dz * M
    box = [_proj(cam, w(dx, dy, dz)) / sc.s for dx in (-28, 28) for dy in (0, 36) for dz in (-28, 92)]
    hull = V._hull([tuple(q) for q in box])
    p.poly(curve(hull, 3), sp.get('shoe', (22, 20, 22)), INK, 2.4)
    to_cam = _unit(np.asarray(cam.pos, float) - w(0, 36, 32))
    if np.dot(-su, to_cam) > 0.35:
        sole = [_proj(cam, w(dx, 36, dz)) / sc.s for dx, dz in ((-24, -24), (24, -24), (24, 88), (-24, 88))]
        p.poly(curve([tuple(q) for q in sole], 3), sp.get('sole_c', B.dk(sp.get('shoe', (22, 20, 22)), 0.72)), INK, 2.0)
        #                                    the shoe's own colour, darker (the critique: grey soles read as other shoes)


def _arm(p, sc, cam, k, side, sp):
    s = sc.s
    j2 = {'sh' + side: tuple(sc.shoulders[side]), 'el' + side: tuple(_proj(cam, k['el' + side]) / s),
          'wr' + side: tuple(_proj(cam, k['wr' + side]) / s), 'hand': {side: sp.get('lying_hand', 'fist')}}
    V.arm(p, j2, side, sp)


def _head(img, cam, k, sp, t, sc, aff, tag, M):  # -> (HeadCam, view)
    """The rig's head, turned about the neck base towards the projected head; its view from where the face points."""
    hup, hfwd = _unit(k['hup']), _unit(k['hfwd'])
    roll = math.radians(sp.get('head_roll', 0.0))     # Job I faces (Sam, 11 Nov: 12, 15 turned, not straight on):
    if roll:                                          # the shot says which way the face looks; + rolls it towards
        r = k['shR'] - k['shL']                       # the person's right shoulder, - the left
        r = r - hup * np.dot(r, hup)
        r = _unit(r - hfwd * np.dot(r, hfwd))
        hfwd = _unit(hfwd * math.cos(roll) + r * math.sin(roll))
    Xh = _unit(np.cross(hup, hfwd))
    d = _unit(np.asarray(cam.pos, float) - k['head'])
    a = yaw_seen(d, Xh, hfwd)
    vd, _ = V.snap(a)
    hv = V.VIEWS[vd]
    neck = np.asarray(aff.P(0, 0)) / B.SS
    hs = _proj(cam, k['head'])
    u = hs - neck
    if np.linalg.norm(u) < 0.25 * 150 * sc.s:         # the head straight at us: its crown's direction instead
        u = _proj(cam, k['head'] + hup * 0.1) - hs
    tu = _unit(np.asarray(aff.P(0, 0)) - np.asarray(aff.P(0, V.HIP_Y)))   # the trunk's up on screen
    ang = math.atan2(tu[0] * u[1] - tu[1] * u[0], np.dot(tu, u))
    lim = math.radians(HEAD_TILT)                     # the neck bends no further than the rig's (the neck stays
    if abs(ang) > lim:                                # under the collar: a tucked head is tipped, never snapped off)
        c, s_ = math.cos(math.copysign(lim, ang)), math.sin(math.copysign(lim, ang))
        u = np.array([tu[0] * c - tu[1] * s_, tu[0] * s_ + tu[1] * c])
    dvec = -_unit(u)                                  # the drawing's down
    rvec = np.array([dvec[1], -dvec[0]])               # the drawing's right
    if hv in ('three', 'side', 'three_back'):         # the face points the way the face points on screen
        fdir = _proj(cam, k['head'] + hfwd * 0.1) - hs
        if np.dot(fdir, rvec) < 0:
            rvec = -rvec
    elif hv == 'front':                               # the drawing's right: the person's left as seen
        xr = _proj(cam, k['head'] + Xh * 0.1) - hs
        if np.dot(xr, rvec) > 0:
            rvec = -rvec
    turn = 0.0               # Sam, 10 Nov round 3: the face-on head stared straight at us (12, 15); the
    #                          turned head is kept, its brows and goatee now drawn as on his face-on one (views)
    # its size (Sam, 10 Nov, second note on "balloon heads": the head stayed full standing size beside a body the
    # camera foreshortens, so it read swollen): at the head's own depth, and shrunk with the trunk, at most 22%
    sw = sp.get('shoulders', 150)
    a_, b_, c_ = (np.asarray(aff.P(*q)) / B.SS for q in ((-sw, 60), (sw, 60), (0, V.HIP_Y)))
    e1, e2 = b_ - a_, c_ - (a_ + b_) / 2
    area = abs(e1[0] * e2[1] - e1[1] * e2[0]) / (2 * sw * (V.HIP_Y - 60) * sc.s ** 2)   # the trunk as seen / face on
    hk = cam.depth(tuple((k['neck'] + k['pelvis']) / 2)) / max(cam.NEAR, cam.depth(tuple(k['head'])))
    hk *= 0.9 * float(np.clip(0.7 + 0.3 * area, 0.8, 1.0))   # lying, a tenth smaller; less again beside a trunk the
    #                                                          camera squashes (whole: 0.9, squashed flat: 0.72)
    hcam = HeadCam(neck, rvec, dvec, sc.s * hk, tag)
    hcam.turn = turn
    # the head sits where it really shows (Job I chat 2: always 150 units out, a neck pointing at or away from us
    # showed as a long loose block), from 100 (the head's foot on the collar) to the rig's 150

    lo = 70.0 if cam.depth(tuple(k['head'])) > cam.depth(tuple(k['neck'])) + 0.05 else 100.0
    hcam.hy = -float(np.clip(np.linalg.norm(hs - neck) / hcam.s, lo, 150.0))
    #                                                   a head further off may tuck its chin under the collar
    return hcam, hv


def _neck(img, hc, sp, aff, view, foot=40):
    """The neck, bending from the collar to the head (Sam, 11 Nov, lying 14 and 18: drawn as one rigid block turned
    with the head, it stood off the collar as a square block (14) or hid under it, the head stuck straight on the
    shoulder (18)). Its foot is in the trunk's drawing (under the collar, `foot` below the neck point), its top in
    the head's (up into the head); the two sides curve between them, so a head tipped off the trunk bends the neck
    instead of swinging a block. Only the sides are inked (the collar and the head cover its ends)."""
    import turnhead as TH
    hcam, hv = hc
    top = {'three': (-24, 40), 'side': (-26, 24)}.get(hv, (-32, 32))
    bot = {'three': (-20, 46), 'side': (-30, 34)}.get(view, (-36, 36))
    yt = -80.0 + (150.0 + hcam.hy)                    # a nearer head: the neck shorter by as much
    H = lambda x, y: np.asarray(hcam.P(x, y), float)
    T = lambda x, y: np.asarray(aff.P(x, y), float)
    tops = [H(top[0], yt), H(top[1], yt)]
    if np.dot(tops[1] - tops[0], T(bot[1], foot) - T(bot[0], foot)) < 0:   # the head drawn mirrored to the trunk:
        tops, top = tops[::-1], top[::-1]                                  # its sides would cross (a bow tie)
    sides = []
    for i in (0, 1):
        p0, p2 = T(bot[i], foot), tops[i]
        p1 = (H(top[i], (yt + 0) / 2 + 10) + T(bot[i], min(foot, 0) - 25)) / 2   # the bend between the two
        sides.append([tuple((1 - u) ** 2 * p0 + 2 * u * (1 - u) * p1 + u * u * p2) for u in np.linspace(0, 1, 12)])
    d = ImageDraw.Draw(img)
    d.polygon(sides[0] + sides[1][::-1], fill=tuple(sp['skin']))
    w = B.Pen(img, hcam).w(2.6)
    for sd in sides:
        d.line(sd, fill=INK, width=w, joint='curve')
    return sides


def _collar(img, hc, sp, sides):
    """The shirt collar and the jacket's collar seen from behind, wrapped round the neck's foot and turned with it
    (Sam, 11 Nov, 18: the trunk's own collar bands stood up beside the head like a block). Each band is a strip
    across the neck's foot, its thickness laid along the neck, a little wider than the neck."""
    hcam = hc[0]
    a0, b0 = np.asarray(sides[0][0], float), np.asarray(sides[1][0], float)
    a1, b1 = np.asarray(sides[0][-1], float), np.asarray(sides[1][-1], float)
    c0 = (a0 + b0) / 2
    up = _unit((a1 + b1) / 2 - c0)
    u = hcam.s * B.SS                                   # frame pixels per person unit at the head
    d = ImageDraw.Draw(img)
    w = B.Pen(img, hcam).w(2.0)
    jc = sp.get('jacket', (40, 40, 46))
    for lo, hi, wide, col in ((-14, 6, 1.22, B.dk(jc, 0.85)), (2, 18, 1.1, sp.get('shirt', (244, 244, 240)))):
        a, b = c0 + (a0 - c0) * wide, c0 + (b0 - c0) * wide
        q = [a + up * lo * u, a + up * hi * u, b + up * hi * u, b + up * lo * u]
        d.polygon([tuple(v) for v in q], fill=tuple(col), outline=INK, width=w)


def _head_draw(img, hc, sp, t):
    hcam, hv = hc
    q = dict(sp, neck_to=-14.0, no_shine=True, nape_in_head=True, turn=getattr(hcam, 'turn', 0.0))       # the back-of-head's own neck ends at the collar; no shine
    #                                                   on a bald crown seen lying (it read as a balloon, Sam 10 Nov)
    V.head_view(img, B.Pen(img, hcam), q, t, hv, q.get('head_dx', 0.0), hcam.hy + q.get('head_dy', 0))


def _sat(k, up):
    """Sitting up (the trunk upright, the thighs forward along the floor): slumped against a wall."""
    thigh = _unit((k['knL'] + k['knR']) / 2 - (k['hipL'] + k['hipR']) / 2)
    return float(up[1]) > 0.6 and float(np.dot(thigh, up)) < 0.5


class Slump:
    """The shirt of a body slumped sitting (Sam, 11 Nov, lying 16: "the shirt drawn as a stiff box"): the standing
    drawing (drawn alone on `layer`) bent as cloth on a slumped body: the shoulders slope and round off (no square
    corners), the sides bow out at the belly, the hem curves up at the sides over the lap, and soft folds cross the
    waist where the trunk bends. Bent as a finished picture, so the plaid, buttons and outline all bend with it.
    `moved(q)`: where a drawing point goes (the sleeves join the sloped shoulders); `paste(img)` puts it down."""
    def __init__(self, layer, aff, sag=1.0):
        self.layer, self.sag = layer, sag
        self.A = np.asarray(aff.A, float) * B.SS
        self.t = np.asarray(aff.t, float) * B.SS
        self.Ai = np.linalg.inv(self.A)
        a = np.asarray(layer)
        ys, xs = np.nonzero(a[:, :, 3] > 8)
        self.box = (xs.min(), ys.min(), xs.max(), ys.max()) if len(xs) else None
        if self.box is None:
            return
        uv = (np.c_[xs, ys] - self.t) @ self.Ai.T
        u0, u1 = np.percentile(uv[:, 0], [1, 99])
        self.xc, self.hw = (u0 + u1) / 2, max(1.0, (u1 - u0) / 2)
        self.bot = max(1.0, float(np.percentile(uv[:, 1], 99)))
        self._folds(aff)

    def disp(self, u, v):
        x = (u - self.xc) / self.hw
        s2 = np.clip(x * x, 0, 1.2)
        vn = v / self.bot
        du = (u - self.xc) * (0.08 * np.exp(-((vn - 0.72) / 0.22) ** 2) - 0.05 * np.clip(1 - vn / 0.35, 0, 1))
        dv = 26 * s2 * np.clip(1 - vn / 0.45, 0, 1) - 40 * s2 ** 1.5 * np.clip((vn - 0.72) / 0.28, 0, 1)
        return du * self.sag, dv * self.sag

    def moved(self, q):
        if self.box is None:
            return np.asarray(q, float)
        du, dv = self.disp(np.array([q[0]], float), np.array([q[1]], float))
        return np.array([q[0] + du[0], q[1] + dv[0]])

    def _folds(self, aff):
        """Soft folds across the waist, drawn on the shirt before it bends (kept inside it, clear of its edge)."""
        import cv2
        a = np.asarray(self.layer).copy()
        w = max(1, int(round(1.6 * B.SS * max(0.25, aff.s) ** 0.6)))
        fm = Image.new('L', self.layer.size, 0)
        d = ImageDraw.Draw(fm)
        for vn, f0, f1, sd in ((0.62, -0.95, -0.15, 1), (0.7, 0.2, 0.92, -1), (0.79, -0.7, 0.05, 1)):
            v = vn * self.bot
            pts = [(self.xc + self.hw * (f0 + (f1 - f0) * i / 8), v + sd * 9 * math.sin(math.pi * i / 8))
                   for i in range(9)]
            d.line([tuple(self.A @ q + self.t) for q in pts], fill=255, width=w, joint='curve')
        fm = np.minimum(np.asarray(fm), cv2.erode(a[:, :, 3], np.ones((2 * w + 1, 2 * w + 1), np.uint8)))
        k = fm[:, :, None] / 255.0
        a[:, :, :3] = (np.asarray(INK[:3]) * k + a[:, :, :3] * (1 - k)).astype(np.uint8)
        self.layer = Image.fromarray(a, 'RGBA')

    def paste(self, img):
        from scipy import ndimage
        if self.box is None:
            return
        a = np.asarray(self.layer).astype(float)
        a[:, :, :3] *= a[:, :, 3:4] / 255.0           # premultiplied: the edges blend cleanly
        x0, y0 = max(0, self.box[0] - 80), max(0, self.box[1] - 80)
        x1, y1 = min(a.shape[1], self.box[2] + 80), min(a.shape[0], self.box[3] + 80)
        gy, gx = np.mgrid[y0:y1, x0:x1].astype(float)
        tgt = (np.stack([gx.ravel(), gy.ravel()], 1) - self.t) @ self.Ai.T
        src = tgt.copy()
        for _ in range(5):                            # the drawing point that bends onto each pixel
            du, dv = self.disp(src[:, 0], src[:, 1])
            src = tgt - np.c_[du, dv]
        pix = src @ self.A.T + self.t
        out = np.zeros((y1 - y0, x1 - x0, 4))
        for c in range(4):
            out[:, :, c] = ndimage.map_coordinates(a[:, :, c], [pix[:, 1], pix[:, 0]], order=1,
                                                   cval=0.0).reshape(gx.shape)
        al = out[:, :, 3:4]
        out[:, :, :3] = np.where(al > 0, out[:, :, :3] * 255.0 / np.maximum(al, 1e-6), 0)
        img.alpha_composite(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGBA'), (int(x0), int(y0)))


def face_up_away(cam, k):
    """True when the camera sees a face turned up to the ceiling from beyond the shoulders (Sam, 10 Nov, 'on the back,
    head away': "the head raised and staring dead on at us"). The rig's heads turn but never tip back, so this view
    can only be drawn as a head sat up facing us: pre-flight flags it (posecheck.lying_drawn); choose another camera."""
    d = _unit(np.asarray(cam.pos, float) - k['head'])
    beyond = cam.depth(tuple(k['head'])) > cam.depth(tuple(k['neck'])) + 0.05
    return bool(beyond and 0.0 < float(np.dot(_unit(k['hfwd']), d)) < 0.9 and float(np.dot(_unit(k['hup']), d)) < -0.3)


# ---------------------------------------------------------------------------------------------- draw
def draw(img, cam, k, sp, t=0.0, M=None):
    """Draw the lying Body k through cam (sets.Cam) in the house style. Returns {joint: frame point}."""
    import limbs
    import lying as L
    M = M or L.M
    limbs.NEXT[0] += 1
    limbs.DRAW[0] = limbs.NEXT[0]
    _N[0] += 1
    tag = 900000 + _N[0]
    X, up, fwd = frame(k)
    mid = (k['neck'] + k['pelvis']) / 2
    if cam.depth(tuple(mid)) <= cam.NEAR:
        return None
    d = _unit(np.asarray(cam.pos, float) - mid)
    a = yaw_seen(d, X, fwd)
    vd, _ = V.snap(a)
    view = V.VIEWS[vd]
    A, tt = _torso_fit(cam, k, sp, vd, X, up, fwd, M)
    s = cam.focal / max(cam.NEAR, cam.depth(tuple(mid))) * M     # frame pixels per person unit at the body
    aff = AffCam(A, tt, s, tag)
    sc = ScreenCam(s, tag)
    sw = sp.get('shoulders', 150)
    old = V._E[0]
    V._E[0] = 0.0
    try:
        sc.shoulders = {sd: (A @ V.project((g * (sw - 14), 60, 0), vd)[0] + tt) / s for sd, g in (('L', -1), ('R', 1))}
        hy = V.JACKET - 8
        sc.hem = tuple(np.asarray((A @ V.project(q, vd)[0] + tt) / s, float) for q in ((-sw, hy, 0), (sw, hy, 0)))
        sc.hem = sc.hem + ((A @ V.project((0, 60, 0), vd)[0] + tt) / s - (sc.hem[0] + sc.hem[1]) / 2,)
        sc.hips = {sd: (A @ V.project((g * 55, V.HIP_Y, 0), vd)[0] + tt) / s for sd, g in (('L', -1), ('R', 1))}
    finally:
        V._E[0] = old
    p = B.Pen(img, sc)
    dt = cam.depth(tuple(mid))
    dep = {('arm', sd): cam.depth(tuple((k['el' + sd] + k['wr' + sd]) / 2)) for sd in 'LR'}
    dep.update({('leg', sd): cam.depth(tuple(k['kn' + sd])) for sd in 'LR'})
    first, last = [], []
    for key, dd in dep.items():
        lim = 0.05 if key[0] == 'leg' else -0.03      # a knee in front: the leg comes out from under the hem
        #                                               (Sam, round 3: a slumped thigh out of the shirt's side)
        (last if dd < dt - lim else first).append((dd, key))
    sp_draw = dict(sp)

    def piece(key, front=False):
        kind, sd = key
        if kind == 'leg':
            _leg(p, sc, cam, k, sd, sp_draw, M, front)
        else:
            _arm(p, sc, cam, k, sd, sp_draw)
    head_behind = cam.depth(tuple(k['head'])) > dt + 0.3
    hc = _head(img, cam, k, sp_draw, t, sc, aff, tag, M)
    _neck(img, hc, sp_draw, aff, view)
    if head_behind:
        _head_draw(img, hc, sp_draw, t)
    def trunk(on):
        tp = B.Pen(on, aff)
        sp_draw['neck_off'] = True
        sp_draw['collar_off'] = view in BACKS and not head_behind
        if view == 'front':
            q = dict(sp_draw, pose='none', full=False)
            q.setdefault('bottom', V.JACKET)
            B.torso(on, tp, q, t)
        else:
            V.torso_view(on, tp, sp_draw, view, False)
    bend = None
    if _sat(k, up):                                   # slumped sitting: the shirt drawn first on its own, bent as
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))     # cloth; the sleeves join its sloped shoulders
        trunk(layer)
        bend = Slump(layer, aff)
        for sd in 'LR':
            q = np.linalg.solve(A, np.asarray(sc.shoulders[sd], float) * s - tt)
            sc.shoulders[sd] = (A @ bend.moved(q) + tt) / s
    for _, key in sorted(first, key=lambda v: -v[0]):
        piece(key)
    if bend:
        bend.paste(img)
    else:
        trunk(img)
    if not head_behind and view in BACKS:             # seen from behind, the neck is nearer than the shirt's back
        ns = _neck(img, hc, sp_draw, aff, view, foot=-10)  # and the arms beyond it: it rises out of the collar (18)
        if sp_draw.get('outfit', 'suit') in ('suit', 'blouse'):
            _collar(img, hc, sp_draw, ns)
    for _, key in sorted(last, key=lambda v: -v[0]):
        piece(key, front=True)
    sp_draw.pop('neck_off')
    sp_draw.pop('collar_off', None)
    if not head_behind and view not in BACKS and any(kk[0] == 'arm' for _, kk in last):
        _neck(img, hc, sp_draw, aff, view, foot=-6)              # an arm in front passes behind the neck, never through it
        #                                               (from behind the collar is nearer: the neck stays under it)
    if not head_behind:
        _head_draw(img, hc, sp_draw, t)
    return {n: cam.project(tuple(k[n]))[0] for n in L.POINTS}


# ---------------------------------------------------------------------------------------------- the sheet
ROLLED = {('back', 60): -40.0, ('back', 30): 40.0}     # the sheet's heads on the back rolled to one side (12, 15)


def numbers(sh, corners, r=26):
    """Each panel's number in a black disc at its top right corner (Sam answers by number)."""
    d = ImageDraw.Draw(sh)
    f = ImageFont.truetype(B.SANS, 34)
    for n, (x, y) in enumerate(corners, 1):
        cx, cy = x - r - 6, y + r + 6
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(20, 20, 20))
        d.text((cx, cy), str(n), fill=(255, 255, 255), font=f, anchor='mm')


def sheet(out, who='vance', extra=()):
    """Vance standing (the flat rig, front and side) beside his lying versions: before (the 3D volumes) and now."""
    import ad_vanced_notice_cast as AC
    import lying as L
    sp = dict(AC.CAST[who])
    font = ImageFont.truetype(B.SANS, 24)
    small = ImageFont.truetype(B.SANS, 19)
    cells = []
    B.SS = 1
    for yaw in (0, 90):
        im = Image.new('RGBA', (1080, 1920), (214, 206, 188, 255))
        V.person(im, B.Cam(1.0, 540, 960), 540, 700, 1.0, sp, 0.0, yaw)
        cells.append(im.convert('RGB').crop((140, 450, 940, 1750)))
    shots = [('back', None, 0.0), ('back', 60, 0.0), ('face_down', 30, 0.0), ('side', 30, 0.0),
             ('back', 30, 180.0), ('slump', None, -60.0)] + list(extra)
    rows = []
    B.SS = 2
    for mode in ('volumes', 'flat'):
        row = []
        for pose, ang, yaw in shots:
            img = B.canvas((214, 206, 188))
            kk, surf = L.lie(sp, pose, 0.0, 0.0, yaw)
            look = (0, 0.35, 0) if pose == 'slump' else (0, 0.1, 0)
            cam = L._fit(L._cam_for(ang, 4.5, look), [kk[n] for n in L.POINTS] + [kk['head'] + 0.15 * kk['hup']],
                         fill=0.7)
            L._room(img, cam, (L.SLUMP_WALL if pose == 'slump' else None))
            q = dict(sp)
            if pose != 'back':
                q['blink'] = True
            if (pose, ang) in ROLLED:                 # on the back, the head rolled to one side (Sam, 11 Nov)
                q['head_roll'] = ROLLED[(pose, ang)]
            surfs = [(p0, n) for _, p0, n in surf]
            if mode == 'volumes':
                L.draw_volumes(img, cam, kk, q, 0.0, surfaces=surfs)
            else:
                L.draw(img, cam, kk, q, 0.0, surfaces=surfs)
            row.append(img.convert('RGB').resize((1080, 1920), Image.LANCZOS).crop((0, 420, 1080, 1500)))
            print(mode, pose, ang, flush=True)
        rows.append(row)
    cw = 330
    W = 2 * 240 + 30 + len(shots) * cw + 20
    H = 70 + 2 * (cw + 40) + 20
    sh = Image.new('RGB', (W, H), (246, 244, 238))
    d = ImageDraw.Draw(sh)
    nm = sp.get('name', who)
    d.text((14, 12), f'Job I: {nm} standing (our usual drawing) beside {nm} lying: top, the old drawing; '
                     'bottom, the new', fill=(20, 20, 20), font=font)
    for i, im in enumerate(cells):
        im = im.copy()
        im.thumbnail((230, 2 * (cw + 40) - 40))
        sh.paste(im, (14 + i * 245, 90))
    d.text((14, 60), 'standing (front, side)', fill=(20, 20, 20), font=small)
    names = ['on the back, eye level', 'on the back, 60 down', 'face down, 30 down', 'curled, 30 down',
             'on the back, head left', 'slumped, eye level'] + \
        [f'{p_} {a_ or 0} down, turned {int(y_)}' for p_, a_, y_ in extra]
    x0 = 2 * 245 + 30
    for r, (label, row) in enumerate((('OLD', rows[0]), ('NEW', rows[1]))):
        y = 70 + r * (cw + 40)
        for c, im in enumerate(row):
            if r == 0:
                d.text((x0 + c * cw + 4, 46), names[c], fill=(20, 20, 20), font=small)
            sh.paste(im.resize((cw - 8, cw - 8), Image.LANCZOS), (x0 + c * cw + 4, y + 20))
        d.text((x0 + 6, y + 22), label, fill=(170, 20, 20) if r == 0 else (20, 110, 40), font=font)
    boxes = [(14 + i * 245 + 230, 90) for i in range(len(cells))] + \
        [(x0 + c * cw + cw - 4, 70 + r * (cw + 40) + 20) for r in range(2) for c in range(len(shots))]
    numbers(sh, boxes)
    sh.save(out, quality=88)
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        sheet(a[1] if len(a) > 1 else 'lying-flat-sheet.jpg', *(a[2:3] or ['vance']),
              extra=[('ball', 30, 0.0), ('ball', 30, 180.0)] if 'ball' in a else ())
    else:
        print(__doc__)
