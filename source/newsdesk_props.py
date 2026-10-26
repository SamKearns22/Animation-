#!/usr/bin/env python3
"""Newsdesk (untitled film, Sam 26 Oct): the props. The two chairs from Sam's photo (references/newsdesk/chairs-1.jpg):
curved-back wooden armchairs, each in its own pool of blue spotlight on a black stage.

The chair, in the house style (flat fills, one outline, hand-cut corners), built in 3D so any camera can see it:
  - a warm teak frame: four round legs, the front two rising to carry the arm ends
  - one continuous curved top rail that wraps round the back and runs forward into the arms, deepest at the back
    and slimming to the arm ends, which sit a little lower
  - a tan leather seat on a wooden seat frame
  Real size: seat 0.44 m high, 0.76 m to the top of the rail, 0.63 m across the arms, 0.52 m deep (a typical
  wooden armchair; added to sizes.py).
The spotlight pool is a flat blue oval on the floor (no glow: house style).

    round_chair(img, cam, x, z, facing)   one chair at floor point (x, z) facing `facing` (plan degrees, 0 = north)
    pool(img, cam, x, z)                  its spotlight pool (draw first)
    python3 source/newsdesk_props.py sheet OUT.jpg   both chairs on their pools as in Sam's photo, a three-quarter and a
                                                     side view, and one beside a 1.75 m person
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import sets as S                 # noqa: E402
from sets import obox, cylinder, draw_parts, dk, jit   # noqa: E402
from ed import INK               # noqa: E402

FLAT = S.FLAT
TEAK = (182, 102, 62)
TEAK_D = (140, 74, 44)
TEAK_L = (206, 130, 84)
LEATHER = (198, 160, 108)
POOL = (44, 62, 164)
STAGE = (10, 10, 14)

SEAT_H, RAIL_TOP, ARM_TOP = 0.44, 0.76, 0.66
RAIL_R = 0.31                                  # the rail's centre line, round the chair's middle
RAIL_A0, RAIL_A1 = -42.0, 222.0                # its ends: the arm tips (0 = the chair's right, 90 = its back)


def _pen(img):
    return B.Pen(img, FLAT)


def _local(x, z, facing):
    def at(lx, ly, lz):
        q = S.rot_y((lx, ly, lz), facing)
        return (x + q[0], ly, z + q[2])
    return at


def _rail_shape(a):
    """The rail at angle a: (top height, depth top-to-bottom, width across): deepest and widest at the back."""
    k = math.sin(math.radians(max(0.0, min(180.0, a))))          # 1 at the back, 0 at the sides and arms
    top = ARM_TOP + (RAIL_TOP - ARM_TOP) * min(1.0, k * 1.6)
    return top, 0.035 + 0.06 * k, 0.04 + 0.03 * k


def _rail_piece(img, cm, at, a0, a1):
    """One stretch of the rail: per slice the side that faces the camera (outer or inner) and the top, filled far to
    near without lines; then one outline round what shows."""
    steps = np.linspace(a0, a1, max(4, int(abs(a1 - a0) / 6)))

    def P(a, r_off, which):
        top, depth, width = _rail_shape(a)
        r = RAIL_R + r_off * width / 2
        y = top if which == 'top' else top - depth
        return at(r * math.cos(math.radians(a)), y, -r * math.sin(math.radians(a)))

    def faces(a, out):
        p = P(a, 1 if out else -1, 'top')
        c = P(a, 0, 'top')
        n = (p[0] - c[0], 0, p[2] - c[2])
        return (cm.pos[0] - p[0]) * n[0] + (cm.pos[2] - p[2]) * n[2] > 0
    sl = sorted(zip(steps, steps[1:]), key=lambda ab: -math.dist(P((ab[0] + ab[1]) / 2, 0, 'top'), cm.pos))
    pen = _pen(img)

    def fpoly(pts, fill, line=None, lw=2.0):         # the rail is too thin to hand-cut: exact corners
        q = cm.clip(pts)
        if len(q) >= 3:
            pen.poly(q, fill, line, lw)

    def fline(pts):
        for u, v in zip(pts, pts[1:]):
            q = cm.clip([u, v, v])
            if len(q) >= 2:
                pen.line(q[:2], INK, 2.0)
    for b0, b1 in sl:
        m = (b0 + b1) / 2
        for out in (True, False):
            if faces(m, out):
                o = 1 if out else -1
                fpoly([P(b0, o, 'bot'), P(b1, o, 'bot'), P(b1, o, 'top'), P(b0, o, 'top')],
                        TEAK if out else TEAK_D, None)
        fpoly([P(b0, -1, 'top'), P(b1, -1, 'top'), P(b1, 1, 'top'), P(b0, 1, 'top')], TEAK_L, None)
    fline([P(a, -1, 'top') for a in steps])
    fline([P(a, 1, 'top') for a in steps])
    for out in (True, False):
        o = 1 if out else -1
        run = [a for a in steps if faces(a, out)]
        if run:
            fline([P(a, o, 'bot') for a in run])
    for a in (a0, a1):                                   # the cut ends
        fpoly([P(a, -1, 'bot'), P(a, 1, 'bot'), P(a, 1, 'top'), P(a, -1, 'top')], TEAK_D, INK, 1.8)


def round_chair(img, cm, x, z, facing):
    at = _local(x, z, facing)
    items = []

    def leg(a, top):
        r = RAIL_R
        lx, lz = r * math.cos(math.radians(a)), -r * math.sin(math.radians(a))
        foot = at(lx, 0.0, lz)                              # straight under the rail
        parts = [cylinder(foot, 0.022, top, {'side': TEAK, 'top': TEAK_L}, n=10)]
        return (at(lx, top / 2, lz), lambda im, c, parts=parts: draw_parts(im, c, parts, _pen(im)))
    for a in (RAIL_A0, RAIL_A1):                             # front legs under the arm tips
        items.append(leg(a, ARM_TOP - 0.03))
    for a in (40.0, 140.0):                                  # back legs into the rail
        items.append(leg(a, _rail_shape(a)[0] - 0.05))
    seat = [obox(at(0, SEAT_H - 0.07, 0.0), (0.44, 0.05, 0.4), facing, {'all': TEAK}),           # inside the legs
            obox(at(0, SEAT_H - 0.02, 0.01), (0.41, 0.05, 0.37), facing, {'all': LEATHER, 'top': (210, 174, 122)})]
    items.append((at(0, SEAT_H, 0.02), lambda im, c: draw_parts(im, c, seat, _pen(im))))
    for a0, a1 in ((RAIL_A0, 40.0), (40.0, 140.0), (140.0, RAIL_A1)):
        m = (a0 + a1) / 2
        ref = at(RAIL_R * math.cos(math.radians(m)), ARM_TOP, -RAIL_R * math.sin(math.radians(m)))
        items.append((ref, lambda im, c, a0=a0, a1=a1: _rail_piece(im, c, at, a0, a1)))
    for ref, fn in sorted(items, key=lambda it: -math.dist(it[0], cm.pos)):
        fn(img, cm)


def pool(img, cm, x, z, r=0.62):
    pts = [(x + r * math.cos(u), 0.002, z + r * 0.92 * math.sin(u)) for u in np.linspace(0, 2 * math.pi, 48, endpoint=False)]
    cm.poly(_pen(img), pts, POOL, None)


def shadow(img, cm, x, z, facing):
    """The chair's shadow in its pool: a flat darker blue below and behind it (the spot is straight above)."""
    at = _local(x, z, facing)
    pts = [at(0.34 * math.cos(u), 0.003, 0.3 * math.sin(u) - 0.02) for u in np.linspace(0, 2 * math.pi, 32, endpoint=False)]
    cm.poly(_pen(img), pts, dk(POOL, 0.55), None)


def sheet(out):
    import views as V
    import sizes
    B.SS = 1
    font = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 30)
    W, H = 1080 * 3 // 2 + 20 * 4 + 400, 980 + 90
    sheet_img = Image.new('RGB', (2100, 1120), (232, 228, 222))
    d = ImageDraw.Draw(sheet_img)

    def frame(cm, draw):
        img = Image.new('RGBA', (1080, 1920), STAGE + (255,))
        draw(img, cm)
        return img.convert('RGB')

    def two(img, cm):                                    # as Sam's photo: two chairs, each on its pool, facing us
        for x in (-0.65, 0.65):
            pool(img, cm, x, 0.0)
            shadow(img, cm, x, 0.0, 180)
        for x in (-0.65, 0.65):
            round_chair(img, cm, x, 0.0, 180)
    c1 = S.Cam((0.0, 1.45, -3.2), (0.0, 0.42, 0.0), focal=1500)
    im = frame(c1, two).crop((0, 560, 1080, 1360))
    sheet_img.paste(im.resize((1080 * 3 // 4, 800 * 3 // 4)), (20, 70))
    d.text((20, 20), 'as in the photo: two chairs, blue spotlight pools', font=font, fill=(30, 30, 30))

    def one(yaw):
        def dr(img, cm):
            pool(img, cm, 0.0, 0.0)
            shadow(img, cm, 0.0, 0.0, yaw)
            round_chair(img, cm, 0.0, 0.0, yaw)
        return dr
    c2 = S.Cam((0.0, 1.3, -2.4), (0.0, 0.4, 0.0), focal=1500)
    for i, (yaw, lab) in enumerate(((225, 'three-quarter'), (270, 'side'), (0, 'from behind'))):
        im = frame(c2, one(yaw)).crop((240, 560, 840, 1360)).resize((270, 360))
        sheet_img.paste(im, (20 + 290 * i, 740))
        d.text((20 + 290 * i, 694), lab, font=font, fill=(30, 30, 30))

    # beside a 1.75 m person, the same camera, both at real size
    def scale(img, cm):
        pool(img, cm, 0.0, 0.0)
        round_chair(img, cm, 0.0, 0.0, 200)
    c3 = S.Cam((0.0, 0.95, -5.0), (0.0, 0.95, 0.0), focal=1500)
    img = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
    scale(img, c3)
    (fx, fy), k = c3.project((0.0, 0.0, 0.0))
    sizes.scale_ref(ImageDraw.Draw(img), fx - 0.85 * k, fy, k)
    sheet_img.paste(img.convert('RGB').crop((140, 300, 940, 1400)).resize((560, 770)), (1080 * 3 // 4 + 60 + 300, 70))
    d.text((1080 * 3 // 4 + 360, 20), 'real size: beside a 1.75 m person', font=font, fill=(30, 30, 30))
    sheet_img.save(out, quality=90)
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
