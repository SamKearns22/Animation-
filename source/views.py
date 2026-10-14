#!/usr/bin/env python3
"""views: people from any angle, walking on a perspective floor (the LOOK TEST for the movement system,
guides/movement-system-plan.md and guides/reference-pack.md).

How it works (South Park's method, reference pack section 0 and 2):
- Five real drawings per person, facing right: 'front', 'three' (three-quarter), 'side' (profile), 'three_back',
  'back'; facing left is the same drawing mirrored. A turn swaps from drawing to drawing, never squashes one.
- Arms and legs come from a small hidden 3D skeleton (x across the body, y down, z forward), turned to the view's angle
  and flattened: limbs on the far side are drawn behind the body, the near ones in front. So a walk works at any angle.
- The walk follows Williams' four poses a step (contact, down, passing, up), two steps a second, a planted foot never
  sliding (it moves back in the body's frame exactly as fast as the body moves on).
- Placement on the floor is series.Room: a perspective camera in metres, so size follows distance.

    python3 source/views.py looktest OUT_DIR      the sheet (five views, a walk strip) and a short clip
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import figure as F           # noqa: E402
from ed import INK, curve, oval, soft   # noqa: E402

VIEWS = {0: 'front', 45: 'three', 90: 'side', 135: 'three_back', 180: 'back'}
THIGH, SHIN, ANKLE_Y = 228, 218, 890          # person units: hips at 450, soles at 928 (knees just soft standing)
M_PER_UNIT = 0.00152                          # metres per person unit (series.py: neck to soles 1.41 m)


def blend(a, b, k):
    return tuple(int(round(x + (y - x) * k)) for x, y in zip(a, b))


def snap(yaw):
    """The nearest drawn view to an angle (degrees; 0 = facing us, 90 = facing right, -90 = facing left, 180 = away).
    Returns (view angle 0-180, mirror?)."""
    y = ((yaw + 180) % 360) - 180
    m = min(VIEWS, key=lambda v: abs(abs(y) - v))
    return m, y < 0


def project(p3, yaw):
    """A body point (x across, y down, z forward) seen from the camera when the body faces `yaw` degrees to the right:
    (screen x, y) and its depth (bigger = nearer the camera)."""
    a = math.radians(yaw)
    x, y, z = p3
    return (x * math.cos(a) + z * math.sin(a), y), -x * math.sin(a) + z * math.cos(a)


# ------------------------------------------------------------------------------------------------ the skeleton
def two_bone(hip, foot, l1, l2, bend=1.0):
    """Knee for a leg in its own forward plane (y, z): knee goes forward (bend=+1) as people's knees do."""
    hy, hz = hip
    fy, fz = foot
    d = math.hypot(fy - hy, fz - hz)
    d = min(d, l1 + l2 - 1e-3)
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, l1 * l1 - a * a))
    uy, uz = (fy - hy) / (d or 1), (fz - hz) / (d or 1)
    my, mz = hy + uy * a, hz + uz * a
    k1 = (my - uz * h, mz + uy * h)
    k2 = (my + uz * h, mz - uy * h)
    return k1 if (k1[1] - mz) * bend > (k2[1] - mz) * bend else k2


def standing(sp):
    """The skeleton standing relaxed: feet a little apart, arms hanging just in front of the body."""
    sw = sp.get('shoulders', 150)
    j = {'bob': 0.0}
    for side, sg in (('L', -1), ('R', 1)):
        j['hip' + side] = (sg * 55, 450.0, 0.0)
        j['foot' + side] = (sg * 60, ANKLE_Y, 6.0)
        j['sh' + side] = (sg * (sw - 14), 60.0, 0.0)
        set_arm(j, side, 0.06, 0.12)
    return j


def set_arm(j, side, swing, bend, out=0.05):
    """Arm joints from angles, so both bones keep the rig's lengths: `swing` (radians) brings the upper arm forward
    (+) or back (-) from hanging; `bend` adds the forearm's bend forward at the elbow; `out` angles it from the body."""
    sg = -1 if side == 'L' else 1
    sx, sy, sz = j['sh' + side]
    u = (sg * math.sin(out), math.cos(swing) * math.cos(out), math.sin(swing) * math.cos(out))
    el = (sx + u[0] * F.UPPER * 0.98, sy + u[1] * F.UPPER * 0.98, sz + u[2] * F.UPPER * 0.98)
    a = swing + bend
    v = (sg * math.sin(out) * 0.5, math.cos(a), math.sin(a))
    n = math.sqrt(sum(c * c for c in v))
    wr = tuple(e + c / n * F.FORE * 0.98 for e, c in zip(el, v))
    j['el' + side], j['wr' + side] = el, wr


def walking(sp, t, steps_per_s=2.0, stride=330.0):
    """Williams' walk: four poses a step. `stride` = how far (person units) one step carries the body.
    Contact (u=0): legs widest, heel down. Down (0.25): weight on, knee bends, body lowest, arms widest.
    Passing (0.5): the free leg passes, body rising. Up (0.75): push off, body highest."""
    j = standing(sp)
    cyc = (t * steps_per_s / 2.0) % 1.0                  # one cycle = two steps (left then right)
    half = stride / 2
    for side, ph0 in (('L', 0.0), ('R', 0.5)):
        u = (cyc + ph0) % 1.0
        if u < 0.5:                                       # this foot on the ground: planted, moving back under the body
            k = u / 0.5
            z, lift = half - stride * k, 0.0
        else:                                             # swinging forward: picks up slowly, puts down fast
            k = (u - 0.5) / 0.5
            e = 1 - (1 - k) ** 1.6
            z, lift = -half + stride * e, 58 * math.sin(math.pi * k) ** 1.3
        sg = -1 if side == 'L' else 1
        j['foot' + side] = (sg * 50, ANKLE_Y - lift, z)
        j['planted' + side] = u < 0.5
        other = 'R' if side == 'L' else 'L'
        swing = -z / half                                 # arms opposite the legs
        set_arm(j, other, 0.32 * swing, 0.18 + 0.22 * max(0.0, swing))
    # the body drops as far as it must for both feet to reach the floor (lowest with the legs widest, at contact and
    # down), and rises over the straight standing leg at passing: the walk's ups and downs come from the legs themselves
    reach = 0.99 * (THIGH + SHIN)
    drop = 0.0
    for side in 'LR':
        fx, fy, fz = j['foot' + side]
        if j['planted' + side]:                            # only the standing foot holds the body up
            drop = max(drop, fy - 450 - math.sqrt(max(0.0, reach * reach - fz * fz)))
    j['bob'] = drop + 3 * math.cos(2 * math.pi * ((cyc * 2.0) % 1.0))
    for side in 'LR':                                     # hips (and so the whole body) move down with the bob
        hx, hy, hz = j['hip' + side]
        j['hip' + side] = (hx, hy, hz)
    for side in 'LR':                                     # feet are on the floor: express them in the lowered body's frame
        fx, fy, fz = j['foot' + side]
        fy -= j['bob']
        if not j['planted' + side]:                       # the trailing foot peels off: its heel lifts as far as the
            fy = min(fy, 450 + math.sqrt(max(0.0, reach * reach - fz * fz)))   # straight leg allows (toe-off)
        j['foot' + side] = (fx, fy, fz)
    return j


# ------------------------------------------------------------------------------------------------ the limbs
def tube(p, pts, widths, col):
    """One smooth limb through the points (a gentle round at each joint), tapering through `widths`."""
    P = np.asarray(pts, float)
    dense, wd = [], []
    for i in range(len(P) - 1):
        for u in np.linspace(0, 1, 12, endpoint=False):
            dense.append(P[i] + (P[i + 1] - P[i]) * u)
            wd.append(widths[i] + (widths[i + 1] - widths[i]) * u)
    dense.append(P[-1])
    wd.append(widths[-1])
    D = np.asarray(dense)
    T = np.gradient(D, axis=0)
    N = np.stack([-T[:, 1], T[:, 0]], 1) / (np.hypot(*T.T)[:, None] + 1e-9)
    left = D + N * np.asarray(wd)[:, None]
    right = D - N * np.asarray(wd)[:, None]
    p.poly(curve([tuple(v) for v in np.vstack([left, right[::-1]])], 2), col, INK, 2.6)


def leg(p, j, side, yaw, sp, shoe=(22, 20, 22)):
    hip3, foot3 = j['hip' + side], j['foot' + side]
    ky, kz = two_bone((hip3[1], hip3[2]), (foot3[1], foot3[2]), THIGH, SHIN)
    knee3 = ((hip3[0] + foot3[0]) / 2, ky, kz)
    pts = [project(q, yaw)[0] for q in (hip3, knee3, foot3)]
    tube(p, pts, [48, 38, 27], sp.get('trousers', (40, 40, 46)))
    fx, fy, fz = foot3
    sole = [(fx - 30, fy + 38, fz - 34), (fx + 30, fy + 38, fz - 34), (fx + 30, fy + 38, fz + 96), (fx - 30, fy + 38, fz + 96)]
    top = [(fx - 26, fy + 4, fz - 30), (fx + 26, fy + 4, fz - 30), (fx + 24, fy + 22, fz + 90), (fx - 24, fy + 22, fz + 90)]
    pts = [project(q, yaw)[0] for q in sole + top]
    hull = _hull(pts)
    p.poly(curve(hull, 3), shoe, INK, 2.4)


def _hull(pts):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))
    if len(pts) < 3:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], q) <= 0:
            hi.pop()
        hi.append(q)
    return lo[:-1] + hi[:-1]


def arm(p, j, side, yaw, sp):
    sh, el, wr = (project(j[k + side], yaw)[0] for k in ('sh', 'el', 'wr'))
    B.arm(p, sh, el, wr, sp.get('jacket', (40, 40, 46)))
    d = (wr[0] - el[0], wr[1] - el[1])
    n = math.hypot(*d) or 1.0
    p.ell(wr[0] + d[0] / n * 12, wr[1] + d[1] / n * 12, 26, 26, sp['skin'], INK, 2.4)


# ------------------------------------------------------------------------------------------------ torso views
def torso_view(img, p, sp, view):
    """The torso drawn for each view, facing right (jacket over an open-necked shirt, as the cast wear it)."""
    sw, bottom, skin = sp.get('shoulders', 150), sp.get('bottom', 560), sp['skin']
    jc, sc = sp.get('jacket', (40, 40, 46)), sp.get('shirt', (244, 244, 240))
    jd = B.dk(jc, 0.72)
    if view == 'three':
        o = 0.32 * sw                                      # the centre of the chest has come round to the right
        p.poly([(-24, -80), (40, -80), (46, 10), (-20, 10)], skin, INK, 2.6)          # neck
        p.poly([(-30, -4), (-sw * 0.74, 12), (-sw * 0.92, 50), (-sw * 0.97, 200), (-sw * 0.86, bottom), (sw * 0.78, bottom),
                (sw * 0.84, 200), (sw * 0.8, 50), (sw * 0.62, 12), (52, -4)], jc, INK, 2.6)
        p.poly([(o - 28, -4), (o + 26, -4), (o + 14, 150), (o + 2, 220), (o - 18, 150)], sc, INK, 2.2)
        p.poly([(o - 28, -4), (o - 4, 40), (o - 14, 54), (o - 34, 6)], sc, INK, 2.0)     # collar points
        p.poly([(o + 26, -4), (o + 6, 38), (o + 14, 50), (o + 30, 6)], sc, INK, 2.0)
        p.poly([(o - 4, 40), (o + 6, 38), (o, 60)], skin, None)
        for sg, k in ((-1, 1.0), (1, 0.6)):                # lapels, the far one narrower
            p.poly([(o + sg * 30, -2), (o + sg * 52 * k, 30), (o + sg * 34 * k, 110), (o + sg * 46 * k, 150),
                    (o + sg * 4, 240), (o + sg * 16 * k, 150)], jc, INK, 2.2)
        p.line([(o, 240), (o + 4, bottom)], jd, 2.2)
        p.ell(o + 10, 300, 5, 5, jd, None)
        p.line([(-sw * 0.6, 60), (-sw * 0.72, bottom - 10)], jd, 2.0)                  # the side seam
        soft(img, p.cam, [(-sw * 0.97, 50), (-sw * 0.6, 40), (-sw * 0.6, bottom), (-sw * 0.88, bottom)], (0, 0, 0), 0.25, 10)
        if sp.get('rosette'):
            p.ell(o - 70, 120, 20, 20, (40, 156, 72), INK, 1.8)
            p.ell(o - 70, 120, 8, 8, (248, 248, 240), INK, 1.4)
    elif view == 'side':
        d = 0.6 * sw
        p.poly([(-26, -80), (24, -80), (34, 8), (-30, 8)], skin, INK, 2.6)
        p.poly(curve([(-34, -8), (-d * 0.92, 22), (-d * 1.02, 130), (-d * 0.96, 320), (-d * 0.92, bottom), (d * 1.0, bottom),
                      (d * 1.02, 300), (d * 1.12, 140), (d * 0.86, 30), (30, -6)], 3), jc, INK, 2.6)
        p.poly([(4, -14), (36, -6), (34, 24), (16, 12)], sc, INK, 2.0)                  # the shirt collar at the throat
        p.line([(34, 0), (d * 0.86, 120), (d * 1.0, 290)], jd, 2.2)                     # lapel and the jacket's front edge
        p.ell(d * 0.98, 300, 5, 5, jd, None)
        soft(img, p.cam, [(-d * 1.02, 60), (-d * 0.5, 60), (-d * 0.5, bottom), (-d * 0.92, bottom)], (0, 0, 0), 0.25, 10)
        if sp.get('rosette'):
            p.ell(d * 0.7, 120, 16, 20, (40, 156, 72), INK, 1.8)
    else:                                                    # 'three_back' and 'back': the back of the jacket
        k, off = (0.9, -0.22 * sw) if view == 'three_back' else (1.0, 0.0)
        p.poly([(-32 + off, -80), (32 + off, -80), (36 + off, 10), (-36 + off, 10)], skin, INK, 2.6)
        p.poly([(-40 + off, -4), (-sw * 0.8 * k, 12), (-sw * k, 50), (-(sw + 6) * k, 200), (-(sw - 6) * k, bottom),
                ((sw - 6) * k, bottom), ((sw + 6) * k, 200), (sw * k, 50), (sw * 0.8 * k, 12), (40 + off, -4)], jc, INK, 2.6)
        p.poly([(-40 + off, -12), (40 + off, -12), (44 + off, 8), (-44 + off, 8)], sc, INK, 2.0)
        p.poly([(-44 + off, 6), (44 + off, 6), (40 + off, 26), (-40 + off, 26)], B.dk(jc, 0.85), INK, 2.0)
        p.line([(off, 26), (off, bottom - 110)], jd, 2.2)
        p.line([(off, bottom - 110), (off, bottom)], INK, 2.2)
        soft(img, p.cam, [(-sw * k, 60), (-sw * 0.4 * k, 30), (-sw * 0.5 * k, bottom), (-sw * k, bottom)], (0, 0, 0), 0.22, 10)


# ------------------------------------------------------------------------------------------------ head views
def _fade_colours(sp):
    c, skin = sp.get('hair_c', (72, 58, 48)), sp['skin']
    return c, blend(skin, c, 0.42)


def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
    """The head for each view, facing right: 'three' and 'side' are new drawings; 'front' is the library's own;
    'back' and 'three_back' the back of the head (the face coming round on the right in 'three_back')."""
    hw, hh, skin = sp.get('hw', 72), sp.get('hh', 90), sp['skin']
    c, side_c = _fade_colours(sp)
    bc = sp.get('brow_c', B.dk(c, 0.8))
    beard = blend(skin, sp.get('beard_c', (112, 96, 86)), 0.55)
    if view == 'three':
        fx = hx + 0.4 * hw                                  # the middle of the face, come round to the right
        p.poly(oval(hx - 0.5 * hw, hy + 6, 12, 22), skin, INK, 2.4)                      # the ear on the far cheek
        outline = curve([(hx - hw, hy - 10), (hx - hw * 0.86, hy - hh * 0.72), (hx - hw * 0.3, hy - hh * 1.04),
                         (hx + hw * 0.45, hy - hh * 0.98), (hx + hw * 0.92, hy - hh * 0.6), (hx + hw * 1.0, hy - 6),
                         (hx + hw * 0.92, hy + hh * 0.55), (hx + hw * 0.62, hy + hh * 1.0), (hx + hw * 0.3, hy + hh * 1.14),
                         (hx - hw * 0.22, hy + hh * 1.04), (hx - hw * 0.72, hy + hh * 0.66), (hx - hw * 0.96, hy + hh * 0.3)], 4)
        p.poly(outline, skin, INK, 2.6)
        p.poly(oval(hx - 0.5 * hw, hy + 6, 12, 22), skin, INK, 2.4)
        p.line([(hx - 0.5 * hw - 2, hy - 4), (hx - 0.5 * hw + 3, hy + 12)], B.dk(skin, 0.8), 1.6)
        # the short beard: along the jaw from below the ear round to the far cheek, a clean cheek line
        p.poly(curve([(hx - hw * 0.62, hy + 22), (hx - hw * 0.8, hy + hh * 0.6), (hx - hw * 0.22, hy + hh * 1.04),
                      (hx + hw * 0.3, hy + hh * 1.14), (hx + hw * 0.62, hy + hh * 1.0), (hx + hw * 0.92, hy + hh * 0.55),
                      (hx + hw * 0.9, hy + 40), (fx + 22, hy + 74), (fx - 10, hy + 76), (hx - hw * 0.1, hy + 62),
                      (hx - hw * 0.4, hy + 40)], 4), beard, blend(skin, sp.get('beard_c', (112, 96, 86)), 0.85), 1.6)
        p.poly(curve([(fx - 26, hy + 56), (fx - 6, hy + 49), (fx + 10, hy + 49), (fx + 24, hy + 55), (fx + 14, hy + 57),
                      (fx - 18, hy + 58)], 4), beard, None)
        blink = sp.get('blink')
        for ex, w in ((fx - 26, 1.0), (fx + 24, 0.62)):    # near eye full, far eye narrower
            ey = hy - 8
            if blink:
                p.line([(ex - 15 * w, ey), (ex, ey + 3), (ex + 15 * w, ey)], INK, 2.4)
            else:
                p.poly([(ex - 17 * w, ey), (ex - 8 * w, ey - 8), (ex + 8 * w, ey - 8), (ex + 17 * w, ey), (ex + 8 * w, ey + 7),
                        (ex - 8 * w, ey + 7)], (250, 250, 248), INK, 2.0)
                p.ell(ex + 5 * w, ey + 1, 4.5 * w, 4.5, INK, None)
            p.line([(ex - 16 * w, ey - 20), (ex + 18 * w, ey - 22)], bc, sp.get('brow_w', 3.6) * (0.85 + 0.15 * w))
        p.line([(fx, hy - 6), (fx + 22, hy + 28), (fx + 10, hy + 35)], INK, 2.0)          # the nose, pointing our way
        p.line([(fx + 2, hy + 33), (fx + 6, hy + 36)], INK, 1.6)
        B.mouth(p, sp, t, fx + 4, hy + 62)
        # hair: the clipped back and side, then the darker top over a receding hairline
        p.poly(curve([(hx - hw * 0.98, hy - 20), (hx - hw * 0.84, hy - hh * 0.7), (hx - hw * 0.3, hy - hh * 1.04),
                      (hx + hw * 0.2, hy - hh * 1.0), (hx - hw * 0.05, hy - hh * 0.6), (hx - hw * 0.32, hy - 10),
                      (hx - hw * 0.62, hy + 4), (hx - hw * 0.95, hy + 24)], 4), side_c, None)
        p.poly(curve([(hx - hw * 0.9, hy - hh * 0.5), (hx - hw * 0.74, hy - hh * 0.92), (hx - hw * 0.1, hy - hh * 1.08),
                      (hx + hw * 0.55, hy - hh * 0.96), (hx + hw * 0.72, hy - hh * 0.72), (hx + hw * 0.4, hy - hh * 0.8),
                      (hx + hw * 0.12, hy - hh * 0.7), (hx - hw * 0.25, hy - hh * 0.62)], 4), c, INK, 2.2)
        p.poly(outline, None, INK, 2.6)
    elif view == 'side':
        face = [(hx - 62, hy - 70), (hx - 40, hy - hh - 6), (hx + 20, hy - hh - 4), (hx + 58, hy - 56), (hx + 64, hy - 24),
                (hx + 62, hy - 6), (hx + 84, hy + 28), (hx + 64, hy + 36), (hx + 68, hy + 52), (hx + 62, hy + 60),
                (hx + 66, hy + 74), (hx + 54, hy + 100), (hx + 18, hy + 108), (hx - 22, hy + 88), (hx - 60, hy + 40)]
        outline = curve(face, 3)
        p.poly(outline, skin, INK, 2.6)
        p.poly(curve([(hx - 40, hy + 26), (hx - 22, hy + 88), (hx + 18, hy + 108), (hx + 54, hy + 100), (hx + 66, hy + 74),
                      (hx + 60, hy + 64), (hx + 40, hy + 66), (hx + 30, hy + 50), (hx + 40, hy + 40), (hx + 66, hy + 44),
                      (hx + 62, hy + 36), (hx + 20, hy + 34), (hx - 6, hy + 20)], 3), beard,
               blend(skin, sp.get('beard_c', (112, 96, 86)), 0.85), 1.4)                   # beard and moustache, side-on
        p.poly(curve([(hx - 66, hy - 30), (hx - 70, hy - 76), (hx - 34, hy - hh - 16), (hx + 24, hy - hh - 14),
                      (hx + 44, hy - hh + 8), (hx + 20, hy - hh + 14), (hx - 6, hy - 56), (hx - 34, hy - 20), (hx - 40, hy + 30),
                      (hx - 62, hy + 24)], 3), side_c, None)                               # clipped back and side
        p.poly(curve([(hx - 62, hy - 64), (hx - 36, hy - hh - 18), (hx + 26, hy - hh - 16), (hx + 46, hy - hh + 6),
                      (hx + 18, hy - hh + 12), (hx - 10, hy - 62), (hx - 44, hy - 46)], 3), c, INK, 2.2)
        p.poly(oval(hx - 18, hy + 8, 12, 22), skin, INK, 2.2)                               # the ear
        p.line([(hx - 20, hy - 4), (hx - 14, hy + 12)], B.dk(skin, 0.8), 1.6)
        ex, ey = hx + 42, hy - 10
        if sp.get('blink'):
            p.line([(ex - 10, ey), (ex + 10, ey + 2)], INK, 2.2)
        else:
            p.poly([(ex - 10, ey), (ex + 2, ey - 7), (ex + 12, ey - 2), (ex + 4, ey + 5)], (250, 250, 248), INK, 1.8)
            p.ell(ex + 5, ey - 1, 3.4, 3.4, INK, None)
        p.line([(ex - 12, ey - 18), (ex + 2, ey - 22), (ex + 16, ey - 18)], bc, sp.get('brow_w', 3.6))
        m = sp.get('mouth', 'set')
        if isinstance(m, str) and m.startswith('v:') and m[2:] not in ('rest', 'MBP'):
            p.poly([(hx + 50, hy + 50), (hx + 66, hy + 48), (hx + 64, hy + 64), (hx + 50, hy + 62)], (120, 30, 40), INK, 1.8)
        else:
            p.line([(hx + 46, hy + 58), (hx + 64, hy + 56)], INK, 2.2)
        p.poly(outline, None, INK, 2.6)
    else:                                                     # the back of the head
        sgn = 1.0
        bt = 0.6 if view == 'three_back' else 0.0
        for side in (-1, 1):
            if side > 0 and bt > 0:
                continue
            p.poly(oval(hx + side * (hw + 2), hy + 6, 12, 22), skin, INK, 2.4)
        outline = B.head_outline(hx, hy, hw, hh, sp.get('jaw', 'round'))
        p.poly(outline, skin, INK, 2.6)
        p.poly(curve([(hx - hw * 0.98, hy - 30), (hx - hw, hy + 20), (hx - hw * 0.8, hy + hh * 0.62), (hx, hy + hh * 0.74),
                      (hx + hw * 0.8, hy + hh * 0.62), (hx + hw, hy + 20), (hx + hw * 0.98, hy - 30), (hx, hy - hh * 0.5)], 4),
               side_c, None)
        p.poly(curve([(hx - hw * 0.96, hy - hh * 0.5), (hx - hw * 0.8, hy - hh * 0.92), (hx, hy - hh * 1.06),
                      (hx + hw * 0.8, hy - hh * 0.92), (hx + hw * 0.96, hy - hh * 0.5), (hx + hw * 0.5, hy - hh * 0.1),
                      (hx, hy), (hx - hw * 0.5, hy - hh * 0.1)], 4), c, None)
        if bt > 0:                                            # three-quarter back: the cheek and beard edge on the right
            w = hw * 0.5 * bt * sgn
            p.poly(curve([(hx + hw * 0.99, hy - hh * 0.35), (hx + hw - w, hy - hh * 0.4), (hx + hw - w * 1.15, hy + hh * 0.4),
                          (hx + hw - w * 0.8, hy + hh * 1.0), (hx + hw * 0.8, hy + hh * 0.86), (hx + hw * 0.99, hy + 10)], 4),
                   skin, None)
            p.poly(curve([(hx + hw * 0.99, hy + 22), (hx + hw - w * 1.1, hy + 26), (hx + hw - w * 0.85, hy + hh * 1.02),
                          (hx + hw * 0.82, hy + hh * 0.88)], 4), beard, None)
            p.line([(hx + hw - w * 0.2, hy - hh * 0.38), (hx + hw - w * 0.9, hy - hh * 0.42)], bc, 3.2)
            p.poly([(hx + hw - 2, hy - 2), (hx + hw + 8, hy + 24), (hx + hw - 2, hy + 34)], skin, INK, 2.0)
            p.poly(oval(hx + hw + 2 - hw * 0.42 * bt, hy + 6, 12, 22), skin, INK, 2.4)
        p.poly(outline, None, INK, 2.6)
        p.line([(hx - 18, hy + hh * 0.95), (hx, hy + hh * 0.9), (hx + 18, hy + hh * 0.95)], B.dk(skin, 0.8), 1.8)


# ------------------------------------------------------------------------------------------------ one person
def person(img, cam, x, y, s, sp, t, yaw, joints=None, head_yaw=None):
    """Draw someone facing `yaw` degrees (snapped to the nearest drawn view), neck base at world (x, y), scale s.
    joints: a skeleton pose (standing() or walking()); it is turned to the same view, so limbs match the drawing."""
    view_deg, mirror = snap(yaw)
    view = VIEWS[view_deg]
    j = joints or standing(sp)
    if view == 'front':                                       # the library's own front view, legs from the skeleton
        L = B.Local(cam, x, y + j.get('bob', 0.0) * s, s, -1 if mirror else 1)
        p = B.Pen(img, L)
        sp = dict(sp, pose='custom', full=False)
        sp['arms'] = {sd: (project(j['el' + sd], 0)[0], project(j['wr' + sd], 0)[0], 'fist') for sd in 'LR'}
        for sd in 'LR':
            leg(p, j, sd, 0, sp)
        B.person(img, cam, x, y + j.get('bob', 0.0) * s, s, sp, t, -1 if mirror else 1)
        return
    L = B.Local(cam, x, y + j.get('bob', 0.0) * s, s, -1 if mirror else 1)
    p = B.Pen(img, L)
    yaw_d = view_deg
    depth = {sd: project(j['hip' + sd], yaw_d)[1] for sd in 'LR'}
    far, near = sorted('LR', key=lambda sd: depth[sd])
    leg(p, j, far, yaw_d, sp)
    if view != 'side':
        leg(p, j, near, yaw_d, sp)
    if view in ('three', 'side', 'three_back'):
        arm(p, j, far, yaw_d, sp)                             # the far arm, behind the body
    if view == 'side':
        leg(p, j, near, yaw_d, sp)
    torso_view(img, p, sp, view)
    if view in ('three', 'side'):
        arm(p, j, near, yaw_d, sp)
    elif view == 'three_back':
        arm(p, j, near, yaw_d, sp)
    else:                                                     # back: both arms at the sides, over the jacket's edges
        for sd in 'LR':
            arm(p, j, sd, yaw_d, sp)
    hv = VIEWS[snap(head_yaw)[0]] if head_yaw is not None else view
    head_view(img, p, sp, t, hv)


# ------------------------------------------------------------------------------------------------ the look test
def looktest(out_dir):
    import series
    import polanski as PZ                                     # Zack, with his hair, beard and the satire installs
    os.makedirs(out_dir, exist_ok=True)
    B.SS = 2
    sp = dict(PZ.ZACK, mouth='set', brows=None)
    # 1. the five views, standing (and the mirrored three-quarter, facing left)
    tiles = []
    for label, yaw in (('front', 0), ('three-quarter', 45), ('side', 90), ('three-quarter back', 135), ('back', 180),
                       ('three-quarter, facing left', -45)):
        img = B.canvas((226, 228, 214))
        cam = B.Cam(1.25, 540, 960)
        person(img, cam, 540, 640, 0.8, sp, 0.0, yaw)
        im = img.convert('RGB').resize((360, 640), Image.LANCZOS).crop((40, 80, 320, 600))
        ImageDraw.Draw(im).text((8, 490), label, font=ImageFont.truetype(B.SANS, 18), fill=(30, 30, 30))
        tiles.append(im)
    sheet = Image.new('RGB', (6 * 284, 524), (40, 40, 40))
    for i, im in enumerate(tiles):
        sheet.paste(im, (i * 284, 0))
    sheet.save(os.path.join(out_dir, 'views.jpg'), quality=90)
    # 2. one step of the walk, side view: contact, down, passing, up (and the other foot's)
    tiles = []
    for k in range(8):
        t = k / 12.0
        img = B.canvas((226, 228, 214))
        person(img, B.Cam(1.25, 540, 960), 540, 640, 0.8, sp, t, 90, walking(sp, t))
        tiles.append(img.convert('RGB').resize((360, 640), Image.LANCZOS).crop((60, 120, 300, 640)))
    strip = Image.new('RGB', (8 * 244, 520), (40, 40, 40))
    for i, im in enumerate(tiles):
        strip.paste(im, (i * 244, 0))
    strip.save(os.path.join(out_dir, 'walk-strip.jpg'), quality=90)
    clip(os.path.join(out_dir, 'looktest.mp4'), sp)
    print('sheets in', out_dir)


def clip(out, sp):
    """The look-test clip, on a perspective floor: he walks towards us on a diagonal (three-quarter view, growing as he
    comes), stops, turns round view by view (head first), and walks away into the distance (back view, shrinking)."""
    import series
    import subprocess
    import imageio_ffmpeg
    room = series.Room(0.0, 1.5, 8.0, 2100.0, sx=540, sy=560)
    speed = 1.2                                                   # metres a second: an unhurried walk
    start, stop = (-2.2, 0.4), (0.15, 5.0)                       # (X, Z) in metres; the camera is at Z = 9
    dist = math.hypot(stop[0] - start[0], stop[1] - start[1])
    yaw_in = math.degrees(math.atan2(stop[0] - start[0], stop[1] - start[1]))
    T1 = dist / speed
    TURN = [(T1 + 0.25, 90), (T1 + 0.42, 135), (T1 + 0.58, 180)]    # body views swap; the head leads by a drawing
    T2 = T1 + 0.75
    T3 = T2 + 2.4
    fps, frames = 12, int((T3 + 0.4) * 12)

    def place(t):
        if t < T1:
            u = t / T1
            return start[0] + (stop[0] - start[0]) * u, start[1] + (stop[1] - start[1]) * u
        if t < T2:
            return stop
        return stop[0], stop[1] - speed * (t - T2)

    def frame(t):
        img = B.canvas((214, 210, 196))
        cam = B.Cam(1.0, 540, 960)
        p = B.Pen(img, cam)
        p.poly(room.quad([(-6, 0, 0), (6, 0, 0), (6, 3.2, 0), (-6, 3.2, 0)]), (226, 228, 214), INK, 3)       # back wall
        p.poly(room.quad([(-6, 0, 0), (6, 0, 0), (6, 0, 8.6), (-6, 0, 8.6)]), (150, 154, 152), INK, 3)       # floor
        for k in range(-6, 7):
            p.line(room.quad([(k, 0, 0), (k, 0, 8.6)]), (130, 134, 132), 2)
        for z in np.arange(0, 8.6, 1.0):
            p.line(room.quad([(-6, 0, z), (6, 0, z)]), (130, 134, 132), 2)
        X, Z = place(t)
        x, y, s = room.person(X, Z)
        if t < T1:
            yaw, head, j = yaw_in, None, walking(sp, t, stride=speed / 2.0 / M_PER_UNIT)
        elif t < T2:
            yaw = yaw_in
            for at, v in TURN:
                if t >= at:
                    yaw = v
            head = next((v for at, v in TURN if at - 1 / 12 <= t < at), None)   # the head a drawing ahead
            head = head if head is not None else yaw
            j = standing(sp)
        else:
            yaw, head, j = 180, None, walking(sp, t - T2, stride=speed / 2.0 / M_PER_UNIT)
        import kit
        kit.contact_shadow(img, cam, x, y + F.SOLE_Y * s, 300 * s)
        person(img, cam, x, y, s, sp, t, yaw, j, head)
        return img

    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', '540x960', '-r', str(fps), '-i', '-', '-c:v', 'libx264', '-crf', '22', '-pix_fmt', 'yuv420p',
                          '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for i in range(frames):
        p.stdin.write(np.asarray(frame(i / fps).convert('RGB').resize((540, 960), Image.LANCZOS)).tobytes())
    p.stdin.close()
    p.wait()
    print('clip:', out, f'({frames / fps:.1f} s)')


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'looktest':
        looktest(sys.argv[2])
    else:
        print(__doc__)
