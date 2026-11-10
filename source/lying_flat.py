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

SOLE_C = (128, 112, 96)
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
def _leg(p, sc, cam, k, side, sp, M):
    s = sc.s
    pts = [_proj(cam, k[n + side]) / s for n in ('hip', 'kn', 'an')]
    pts[0] = sc.hips[side]
    lk = sp.get('leg_k', 1.0)
    col = sp.get('trousers', (40, 40, 46))
    a_, b_ = pts[0] - pts[1], pts[2] - pts[1]
    fold = np.dot(a_, b_) / ((np.linalg.norm(a_) * np.linalg.norm(b_)) or 1)
    if fold > 0.4:                                   # folded tight on screen: thigh, shin over it, a round knee
        V.tube(p, [tuple(pts[0]), tuple(pts[1])], [48 * lk, 38 * lk], col)
        V.tube(p, [tuple(pts[1]), tuple(pts[2])], [38 * lk, 27 * lk], col)
        p.ell(pts[1][0], pts[1][1], 38 * lk, 38 * lk, col, None)
    else:
        V.tube(p, [tuple(q) for q in pts], [48 * lk, 38 * lk, 27 * lk], col)
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
        p.poly(curve([tuple(q) for q in sole], 3), sp.get('sole_c', SOLE_C), INK, 2.0)


def _arm(p, sc, cam, k, side, sp):
    s = sc.s
    j2 = {'sh' + side: tuple(sc.shoulders[side]), 'el' + side: tuple(_proj(cam, k['el' + side]) / s),
          'wr' + side: tuple(_proj(cam, k['wr' + side]) / s), 'hand': {side: sp.get('lying_hand', 'fist')}}
    V.arm(p, j2, side, sp)


def _head(img, cam, k, sp, t, sc, aff, tag, M):
    """The rig's head, turned about the neck base towards the projected head; its view from where the face points."""
    hup, hfwd = _unit(k['hup']), _unit(k['hfwd'])
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
    hcam = HeadCam(neck, rvec, dvec, sc.s, tag)
    q = dict(sp)
    V.head_view(img, B.Pen(img, hcam), q, t, hv, q.get('head_dx', 0.0), -150.0 + q.get('head_dy', 0))


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
        sc.hips = {sd: (A @ V.project((g * 55, V.HIP_Y, 0), vd)[0] + tt) / s for sd, g in (('L', -1), ('R', 1))}
    finally:
        V._E[0] = old
    p = B.Pen(img, sc)
    dt = cam.depth(tuple(mid))
    dep = {('arm', sd): cam.depth(tuple((k['el' + sd] + k['wr' + sd]) / 2)) for sd in 'LR'}
    dep.update({('leg', sd): cam.depth(tuple(k['kn' + sd])) for sd in 'LR'})
    first, last = [], []
    for key, dd in dep.items():
        lim = 0.2 if key[0] == 'leg' else -0.03       # legs go under the jacket unless clearly in front of it
        (last if dd < dt - lim else first).append((dd, key))
    sp_draw = dict(sp)

    def piece(key):
        kind, sd = key
        if kind == 'leg':
            _leg(p, sc, cam, k, sd, sp_draw, M)
        else:
            _arm(p, sc, cam, k, sd, sp_draw)
    head_behind = cam.depth(tuple(k['head'])) > dt + 0.3
    if head_behind:
        _head(img, cam, k, sp_draw, t, sc, aff, tag, M)
    for _, key in sorted(first, key=lambda v: -v[0]):
        piece(key)
    tp = B.Pen(img, aff)
    if view == 'front':
        q = dict(sp_draw, pose='none', full=False)
        q.setdefault('bottom', V.JACKET)
        B.torso(img, tp, q, t)
    else:
        V.torso_view(img, tp, sp_draw, view, False)
    for _, key in sorted(last, key=lambda v: -v[0]):
        piece(key)
    if not head_behind:
        _head(img, cam, k, sp_draw, t, sc, aff, tag, M)
    return {n: cam.project(tuple(k[n]))[0] for n in L.POINTS}


# ---------------------------------------------------------------------------------------------- the sheet
def sheet(out, who='vance'):
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
             ('back', 30, 90.0), ('slump', None, -60.0)]
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
    d.text((14, 12), 'Job I: Vance standing (our usual drawing) beside Vance lying: top, the old drawing; '
                     'bottom, the new', fill=(20, 20, 20), font=font)
    for i, im in enumerate(cells):
        im = im.copy()
        im.thumbnail((230, 2 * (cw + 40) - 40))
        sh.paste(im, (14 + i * 245, 90))
    d.text((14, 60), 'standing (front, side)', fill=(20, 20, 20), font=small)
    names = ['on the back, eye level', 'on the back, 60 down', 'face down, 30 down', 'curled, 30 down',
             'on the back, head away', 'slumped, eye level']
    x0 = 2 * 245 + 30
    for r, (label, row) in enumerate((('OLD', rows[0]), ('NEW', rows[1]))):
        y = 70 + r * (cw + 40)
        for c, im in enumerate(row):
            if r == 0:
                d.text((x0 + c * cw + 4, 46), names[c], fill=(20, 20, 20), font=small)
            sh.paste(im.resize((cw - 8, cw - 8), Image.LANCZOS), (x0 + c * cw + 4, y + 20))
        d.text((x0 + 6, y + 22), label, fill=(170, 20, 20) if r == 0 else (20, 110, 40), font=font)
    sh.save(out, quality=88)
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        sheet(a[1] if len(a) > 1 else 'lying-flat-sheet.jpg')
    else:
        print(__doc__)
