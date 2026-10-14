#!/usr/bin/env python3
"""wolf: Satire-style dire wolves (first used in Cry Minister). Flat colour, one outline, lumpy shaggy shapes; manic
yellow eyes with pin pupils, oversized serrated teeth, red gums. Bigger and rangier than any wolf native to Britain.

Views (all drawn with satire_style's Ctx, `X`; (x, y) is the ground under the middle of the body; s = 1 is a wolf whose
shoulder stands 200 units high, about half a person's height at the people's scale 0.8 when s is about 2):
  side(X, x, y, s, face, pal, **pose)   side-on: standing, snarling, the loping gallop (run=phase 0-1), the leap at a
                                        throat (leap=0-1), feeding (feed=0-1: head down, then a hunk ripped up to the sky)
  front(X, x, y, s, pal, **pose)        coming at us: running (run=phase), leaping at the lens (leap=0-1), and tangled
                                        in a net (net=True)
  meat(X, x, y, r, seed)                a hunk of meat (flat red, a pale fat edge, sometimes a bone)
  blood(X, x, y, r, seed)               a flat red splat (cartoon blood: no wounds shown)
Test sheet: python3 source/wolf.py sheet OUT.png
"""
import math
import random
import sys

from satire_style import OUT, blob, limb

# (base, dark, light): grey, tawny (the dire wolf), cream-white, brown-grey, smoky black. Every wolf different.
PALS = [((128, 124, 120), (88, 84, 84), (196, 190, 178)),
        ((178, 118, 70), (124, 78, 46), (226, 194, 152)),
        ((226, 222, 210), (174, 168, 158), (248, 246, 238)),
        ((112, 98, 86), (72, 62, 56), (170, 156, 140)),
        ((70, 68, 72), (42, 40, 44), (132, 128, 128))]
EYE = (246, 206, 40)
GUM = (196, 44, 60)
MOUTH = (92, 18, 30)
TOOTH = (250, 248, 236)
NOSE = (28, 24, 26)
RED = (190, 20, 32)
RED_D = (140, 12, 24)


def _rot(p, a):
    c, s_ = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s_, p[0] * s_ + p[1] * c)


def shag(cx, cy, rx, ry, n=14, depth=0.16, seed=0, ang=0.0, start=0.0, end=2 * math.pi):
    """A shaggy outline: an ellipse whose edge breaks into uneven tufts (the same every frame for one seed)."""
    r = random.Random(seed)
    pts = []
    for i in range(n * 2 + 1 if end - start < 6.2 else n * 2):
        u = start + (end - start) * i / (n * 2)
        k = 1.0 + (depth * r.uniform(0.6, 1.2) if i % 2 == 0 else -depth * 0.3)
        p = _rot((rx * k * math.cos(u), ry * k * math.sin(u)), ang)
        pts.append((cx + p[0], cy + p[1]))
    return pts


def chain(X, pts, widths, col, edge=6):
    """A tapered limb along pts (widths at each point) with ONE outline round the whole thing (no seams at the joints):
    every outline piece first, then every fill piece."""
    def quad(a, b, wa, wb):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1e-6
        nx, ny = -dy / n, dx / n
        return [(a[0] + nx * wa, a[1] + ny * wa), (b[0] + nx * wb, b[1] + ny * wb),
                (b[0] - nx * wb, b[1] - ny * wb), (a[0] - nx * wa, a[1] - ny * wa)]
    for e, c in ((edge * 0.5, OUT), (0.0, col)):
        for i in range(len(pts) - 1):
            X.poly(quad(pts[i], pts[i + 1], widths[i] / 2 + e, widths[i + 1] / 2 + e), c, line=False)
        for p, w in zip(pts, widths):
            X.ell(p[0], p[1], w / 2 + e, w / 2 + e, c, line=False)


def teeth(X, a, b, n, length, down, big=(), ink=True):
    """A row of serrated teeth along the edge a-b, pointing `down` (+1) or up (-1) in the edge's own frame."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy * down, ux * down
    if ny * down < 0:
        nx, ny = -nx, -ny
    w = L / n
    for i in range(n):
        x0, y0 = a[0] + ux * w * i, a[1] + uy * w * i
        ln = length * (1.6 if i in big else (0.75 + 0.25 * ((i * 7) % 3) / 2))
        tip = (x0 + ux * w * 0.5 + nx * ln, y0 + uy * w * 0.5 + ny * ln)
        X.poly([(x0, y0), tip, (x0 + ux * w, y0 + uy * w)], TOOTH, line=ink)


# ------------------------------------------------------------------------------------------------ side view
def side_pose(run=None, leap=None, feed=None, crouch=0.0):
    """Joint angles and body offsets for a pose. Returns a dict the drawing reads."""
    P = dict(ff=(0.0, 0.0), fb=(0.05, 0.0), hf=(0.0, 0.0), hb=(-0.05, 0.0), stretch=0.0, lift=0.0, ang=0.0,
             head=0.0, crouch=crouch)
    if run is not None:                       # the loping gallop: reach and gather, legs paired a beat apart
        def leg(phase, front):
            s_ = math.sin(2 * math.pi * phase)
            c_ = math.cos(2 * math.pi * phase)
            if front:
                return (0.8 * s_, 1.1 * max(0.0, c_))
            return (-0.75 * s_, 1.0 * max(0.0, -c_))
        P.update(ff=leg(run, True), fb=leg(run + 0.09, True), hf=leg(run + 0.5 - 0.42, False),
                 hb=leg(run + 0.5 - 0.33, False))
        P['stretch'] = 14 * math.sin(2 * math.pi * run)
        P['lift'] = 22 * max(0.0, math.sin(2 * math.pi * run + 0.6))
        P['ang'] = -0.06 * math.sin(2 * math.pi * run + 0.4)
        P['head'] = 0.08 * math.sin(2 * math.pi * run)
    if leap is not None:                      # crouch, launch, full stretch at the throat
        u = max(0.0, min(1.0, leap))
        P.update(ff=(0.3 + 1.0 * u, 0.9 - 0.7 * u), fb=(0.2 + 0.95 * u, 1.0 - 0.7 * u),
                 hf=(-0.2 - 1.0 * u, 0.2 * (1 - u)), hb=(-0.3 - 0.9 * u, 0.1),
                 stretch=24 * u, lift=0, ang=-0.32 * u + 0.12 * max(0.0, u - 0.8) / 0.2, head=-0.15 * u)
    if feed is not None:                      # head down in the kill, then a hunk ripped up to the sky
        u = max(0.0, min(1.0, feed))
        P.update(ff=(0.45, 0.0), fb=(0.3, 0.0), hf=(-0.3, 0.0), hb=(-0.15, 0.0), stretch=6,
                 ang=0.18 - 0.3 * u, head=1.05 - 2.0 * u, crouch=0.25 * (1 - u))
    return P


def side(X, x, y, s, face, pal=0, run=None, leap=None, feed=None, jaw=0.25, snarl=1.0, blood=0.0, crouch=0.0,
         lift=0.0, ang=0.0, hunk=None, look=0.0, seed=0, blink=False):
    """One dire wolf side-on. face +1 = facing right. jaw 0-1 opens the mouth; snarl 0-1 wrinkles the muzzle and bares
    the gums; blood 0-1 covers muzzle, ruff and forelegs; hunk = a meat seed held in the jaws (ripped up when feeding).
    lift raises it off the ground (airborne); ang tips the whole body (radians, nose up negative)."""
    base, dark, light = PALS[pal % len(PALS)]
    P = side_pose(run, leap, feed, crouch)
    a = P['ang'] + ang
    up = P['lift'] + lift
    cr = P['crouch'] * 40
    st = P['stretch']

    def T(px, py):                        # wolf units -> world, through the body's tilt about its middle
        q = _rot((px, py + 150), a)
        return (x + face * q[0] * s, y + (q[1] - 150 - up) * s)

    sh = (58 + st / 2, -150 + cr)          # shoulder and hip joints
    hp = (-82 - st / 2, -148 + cr * 0.6)

    def front_leg(th, bend, col, near):
        el = (sh[0] + 78 * math.sin(th), sh[1] + 78 * math.cos(th))
        a2 = th - bend
        wr = (el[0] + 62 * math.sin(a2), el[1] + 62 * math.cos(a2))
        a3 = a2 + 0.5 * bend
        paw = (wr[0] + 22 * math.sin(a3) + 8, wr[1] + 22 * math.cos(a3))
        if not run and leap is None and feed is None:
            paw = (paw[0], min(paw[1], -0.0))
        k = 1.0 if near else 0.88
        chain(X, [T(*sh), T(*el), T(*wr), T(*paw)], [58 * s * k, 26 * s * k, 18 * s * k, 16 * s * k], col, 6 * s)
        X.rell(*T(paw[0] + 10, paw[1] + 2), 21 * s, 11 * s, a + (0.0 if face > 0 else math.pi), col)
        if near:
            for k in (-1, 1):
                X.seg(T(paw[0] + 16 + 6 * k, paw[1] - 4), T(paw[0] + 22 + 6 * k, paw[1] + 8), 3 * s)
        return paw

    def hind_leg(th, bend, col, near):
        kn = (hp[0] + 72 * math.sin(th + 0.45), hp[1] + 72 * math.cos(th + 0.45))
        a2 = th - 0.75 - bend
        hk = (kn[0] + 62 * math.sin(a2), kn[1] + 62 * math.cos(a2))
        a3 = th + 0.12 + 0.4 * bend
        paw = (hk[0] + 58 * math.sin(a3), hk[1] + 58 * math.cos(a3))
        k = 1.0 if near else 0.88
        chain(X, [T(*hp), T(*kn), T(*hk), T(*paw)], [78 * s * k, 40 * s * k, 18 * s * k, 16 * s * k], col, 6 * s)
        X.rell(*T(paw[0] + 10, paw[1] + 2), 22 * s, 12 * s, a + (0.0 if face > 0 else math.pi), col)
        return paw

    # far legs first, in shadow
    front_leg(*P['fb'], dark, False)
    hind_leg(*P['hb'], dark, False)
    # the bushy tail, streaming behind (higher when running or leaping)
    tl = 0.5 if (run is not None or leap is not None) else -0.2
    tail_pts = [T(*hp)]
    for i in range(1, 5):
        u = i / 4
        tail_pts.append(T(hp[0] - 40 - 90 * u, hp[1] - 18 - 60 * tl * u + 40 * u * u * (1 - tl)))
    tx, ty = tail_pts[-2]
    cxw, cyw = (tail_pts[1][0] + tail_pts[-1][0]) / 2, (tail_pts[1][1] + tail_pts[-1][1]) / 2
    tang = math.atan2(tail_pts[-1][1] - tail_pts[1][1], tail_pts[-1][0] - tail_pts[1][0])
    X.poly(shag(cxw, cyw, 72 * s, 24 * s, 9, 0.22, seed + 3, tang), base)
    X.poly(shag(*tail_pts[-1], 22 * s, 16 * s, 5, 0.2, seed + 4, tang), dark, line=False)
    # the body: chest, belly and rump in one lumpy shape, a shaggy back, a darker saddle
    lumps = [(*T(sh[0] + 6, sh[1] - 4), 74 * s, 64 * s, a), (*T((sh[0] + hp[0]) / 2, -150 + cr), 92 * s, 46 * s, a),
             (*T(hp[0] + 4, hp[1] - 6), 62 * s, 54 * s, a)]
    X.poly(shag(*T((sh[0] + hp[0]) / 2, -164 + cr), 150 * s + st * s / 2, 46 * s, 16, 0.12, seed + 1, a,
                math.pi * 1.05, math.pi * 1.95), base)
    blob(X, lumps, base, ol=X.ol / 2 if X.ol > 6 else 5)
    X.poly(shag(*T((sh[0] + hp[0]) / 2 - 10, -186 + cr), 110 * s, 18 * s, 10, 0.25, seed + 5, a,
                math.pi * 1.1, math.pi * 1.9), dark, line=False)
    X.rell(*T((sh[0] + hp[0]) / 2, -118 + cr), 70 * s, 14 * s, a, light, line=False)        # pale belly
    # near legs
    hind_leg(*P['hf'], base, True)
    front_leg(*P['ff'], base, True)
    # the neck and the big shaggy ruff
    hd = P['head']
    nb = (sh[0] + 30, sh[1] - 30)
    hang = -0.35 + hd + (0.25 if feed is not None else 0.0)
    hc = (nb[0] + 70 * math.cos(hang), nb[1] + 70 * math.sin(hang))
    blob(X, [(*T(*nb), 58 * s, 50 * s, a), (*T((nb[0] + hc[0]) / 2, (nb[1] + hc[1]) / 2), 46 * s, 40 * s, a + hang)], base, ol=5)
    X.poly(shag(*T(nb[0] + 4, nb[1] + 20), 52 * s, 72 * s, 11, 0.22, seed + 6, a + 0.2, -math.pi * 0.4, math.pi * 0.75), light)
    if blood > 0:                                                         # blood soaking the ruff and the forelegs
        smear(X, *T(nb[0] + 16, nb[1] + 44), 40 * s * blood + 4 * s, seed + 9)
    return head_side(X, T, hc, hd, a, s, face, base, dark, light, jaw, snarl, blood, hunk, seed, blink,
                     feed is not None)


def head_side(X, T, hc, hd, a, s, face, base, dark, light, jaw, snarl, blood, hunk, seed, blink, feeding):
    """The head side-on: a heavy skull, a long muzzle, a hinged lower jaw full of oversized serrated teeth."""
    hp = hd + (0.35 if feeding else 0.0)

    def H(px, py):                         # head units -> world (pitched by hp about the skull)
        q = _rot((px, py), hp)
        return T(hc[0] + q[0], hc[1] + q[1])
    ja = 0.12 + 0.8 * jaw                 # the lower jaw drops about its hinge
    hinge = (-6, 14)
    lj = lambda px, py: H(*(hinge[0] + _rot((px - hinge[0], py - hinge[1]), ja)[0],
                            hinge[1] + _rot((px - hinge[0], py - hinge[1]), ja)[1]))
    # the ear behind, then the skull
    X.poly([H(-34, -26), H(-50, -86), H(-6, -40)], dark)
    # no fill between the jaws: from the side, the gap in an open mouth shows whatever is behind the wolf (Sam's note)
    # lower jaw: gums and teeth, then the jaw itself
    X.poly([lj(-8, 12), lj(86, 16), lj(90, 30), lj(70, 36), lj(-6, 34)], light)
    X.poly([lj(-2, 14), lj(84, 16), lj(84, 22), lj(0, 22)], GUM, line=False)
    teeth(X, lj(4, 14), lj(84, 16), 7, 15 * s, -1, big=(5,))
    X.poly(shag(*H(0, -6), 50 * s, 40 * s, 10, 0.12, seed + 7, a + hp), base)
    # the muzzle (upper jaw), wrinkled in a snarl, gums bared
    X.poly([H(18, -30), H(70, -20), H(104, -6), H(106, 8), H(96, 14), H(10, 12)], base)
    X.poly([H(30, 2), H(96, 8), H(96, 14), H(10, 12)], light, line=False)
    if snarl > 0:
        X.poly([H(8, 12), H(98, 14), H(96, 4 + 6 * (1 - snarl)), H(10, 6)], GUM)
        for k in range(3):
            X.seg(H(36 + 14 * k, -22 + 2 * k), H(44 + 14 * k, -12 + 2 * k), 3 * s)
    teeth(X, H(6, 12), H(96, 14), 8, 16 * s, 1, big=(1, 6))
    X.rell(*H(104, 0), 11 * s, 9 * s, a + hp, NOSE)
    if blood > 0:
        smear(X, *H(78, 14), 24 * s * blood + 3 * s, seed + 8)
    # the near ear, the eye: manic yellow, a pin pupil, a heavy brow driven down at the nose
    X.poly([H(-20, -26), H(-36, -92), H(4, -38)], base)
    X.poly([H(-20, -36), H(-31, -74), H(-6, -40)], dark, line=False)
    if blink:
        X.seg(H(6, -14), H(36, -10), 4 * s)
    else:
        X.poly([H(6, -12), H(18, -22), H(36, -16), H(26, -6)], EYE)
        X.ell(*H(22, -14), 3.2 * s, 3.2 * s, OUT, line=False)
    X.seg(H(0, -26), H(40, -14), 7 * s)
    if hunk is not None:                  # a hunk of meat clamped in the front teeth
        mx, my = H(84, 22)
        meat(X, mx, my + 10 * s, 34 * s, hunk)
    return H(100, 20)                      # the front of the jaws (for meat and bites)


# ------------------------------------------------------------------------------------------------ front view
def front(X, x, y, s, pal=0, run=None, leap=None, jaw=0.6, blood=0.0, net=False, seed=0, look=(0.0, 0.0), struggle=0.0,
          blink=False):
    """A dire wolf coming straight at us. run = gait phase (forelegs pumping, the head bobbing); leap 0-1 = launching
    at the lens, forelegs flung out wide, jaws at full gape; net = tangled in a net, legs through the mesh."""
    base, dark, light = PALS[pal % len(PALS)]
    P = lambda px, py: (x + px * s, y + py * s)
    bob = 0.0
    if run is not None:
        bob = 14 * max(0.0, math.sin(2 * math.pi * run + 0.6))
    u = max(0.0, min(1.0, leap)) if leap is not None else 0.0
    yy = -bob - 60 * u
    # hind legs and haunches, small behind the chest (further away)
    for k in (-1, 1):
        ph = 0.0 if run is None else math.sin(2 * math.pi * (run + 0.5 + 0.1 * k))
        chain(X, [P(k * 58, -150 + yy), P(k * 66, -40 + yy - 18 * ph - 80 * u)], [40 * s, 24 * s], dark, 6 * s)
        X.ell(*P(k * 68, -36 + yy - 18 * ph - 80 * u), 22 * s, 13 * s, dark)
    blob(X, [(*P(0, -190 + yy), 96 * s, 74 * s, 0.0), (*P(0, -150 + yy), 84 * s, 50 * s, 0.0)], base)
    # forelegs: pumping in turn (running), flung wide (leaping), splayed against the mesh (net)
    paws = []
    for k in (-1, 1):
        if net:
            w = math.sin(struggle * 7 + k)
            sh, pw = P(k * 52, -180 + yy), P(k * (120 + 12 * w), -110 + yy - 40 * k * w)
        elif u > 0:
            sh, pw = P(k * 56, -190 + yy), P(k * (60 + 120 * u), -150 + yy - 190 * u)
        else:
            lift = 0.0 if run is None else max(0.0, math.sin(2 * math.pi * run + (0 if k < 0 else math.pi)))
            sh, pw = P(k * 50, -170 + yy), P(k * 48, -20 + yy - 70 * lift)
        mid = ((sh[0] + pw[0]) / 2 + k * 10 * s, (sh[1] + pw[1]) / 2)
        chain(X, [sh, mid, pw], [50 * s, 30 * s, 24 * s], base, 6 * s)
        paws.append(pw)
    for pw in paws:
        X.ell(pw[0], pw[1], 26 * s, 18 * s, base)
        for d in (-12, 0, 12):
            X.seg((pw[0] + d * s, pw[1] + 4 * s), (pw[0] + d * s, pw[1] + 22 * s), 4 * s, TOOTH if u > 0.3 else OUT)
    # the great ruff
    X.poly(shag(*P(0, -220 + yy), 104 * s, 84 * s, 14, 0.2, seed + 1), light)
    if blood > 0:
        smear(X, *P(0, -196 + yy), 50 * s * blood + 5 * s, seed + 9)
    return face_front(X, P, yy - 10 * u, s, base, dark, light, max(jaw, u), blood, seed, look, blink)


def face_front(X, P, yy, s, base, dark, light, jaw, blood, seed, look=(0.0, 0.0), blink=False):
    hy = -300 + yy
    for k in (-1, 1):                                                         # ears up, pinned forward
        X.poly([P(k * 30, hy - 30), P(k * 66, hy - 110), P(k * 74, hy - 20)], base)
        X.poly([P(k * 40, hy - 34), P(k * 62, hy - 88), P(k * 64, hy - 30)], dark, line=False)
    X.poly(shag(*P(0, hy), 80 * s, 64 * s, 12, 0.14, seed + 2), base)
    X.poly(shag(*P(0, hy + 26), 66 * s, 40 * s, 10, 0.12, seed + 3, 0, 0.1, math.pi - 0.1), light, line=False)
    # the mouth, at full stretch: upper and lower rows of oversized serrated teeth, red gums, the canines biggest
    g = 18 + 52 * jaw
    X.poly([P(-44, hy + 16), P(44, hy + 16), P(30, hy + 18 + g), P(0, hy + 24 + g), P(-30, hy + 18 + g)], MOUTH)
    if jaw > 0.4:
        X.ell(*P(0, hy + 12 + g), 20 * s, 10 * s, (200, 80, 96), line=False)            # the tongue
    X.poly([P(-46, hy + 8), P(46, hy + 8), P(44, hy + 18), P(-44, hy + 18)], GUM)
    teeth(X, P(-44, hy + 16), P(44, hy + 16), 8, 18 * s, 1, big=(0, 7))
    X.poly([P(-32, hy + 14 + g), P(32, hy + 14 + g), P(30, hy + 24 + g), P(-30, hy + 24 + g)], GUM)
    teeth(X, P(-32, hy + 16 + g), P(32, hy + 16 + g), 6, 16 * s, -1, big=(0, 5))
    X.poly([P(-30, hy - 12), P(30, hy - 12), P(22, hy + 8), P(-22, hy + 8)], light)        # the muzzle, snarling
    X.ell(*P(0, hy - 6), 20 * s, 13 * s, NOSE)
    for k in (-1, 1):
        X.seg(P(k * 10, hy - 26), P(k * 24, hy - 16), 3 * s)
    if blood > 0:
        smear(X, *P(0, hy + 30), 34 * s * blood + 3 * s, seed + 8)
    for k in (-1, 1):                                                         # manic eyes, brows driven down
        ex, ey = P(k * 32, hy - 30)
        if blink:
            X.seg((ex - 14 * s, ey), (ex + 14 * s, ey), 4 * s)
        else:
            X.poly([(ex - 15 * s, ey + 2 * s), (ex - 4 * s * k, ey - 9 * s), (ex + 15 * s, ey + 2 * s), (ex + 2 * s * k, ey + 8 * s)], EYE)
            X.ell(ex + look[0] * 6 * s, ey + look[1] * 4 * s, 3.4 * s, 3.4 * s, OUT, line=False)
        X.seg(P(k * 12, hy - 36), P(k * 52, hy - 50), 8 * s)


# ------------------------------------------------------------------------------------------------ gore (flat)
def meat(X, x, y, r, seed=0, bone=None):
    """A hunk of meat: a lumpy flat-red chunk with a pale fat edge, sometimes a bone end poking out."""
    rd = random.Random(seed)
    ang = rd.uniform(0, math.pi)
    if bone is None:
        bone = rd.random() < 0.35
    if bone:
        d = _rot((r * 1.1, 0), ang)
        X.seg((x - d[0] * 0.3, y - d[1] * 0.3), (x + d[0], y + d[1]), r * 0.3, TOOTH)
        X.ell(x + d[0], y + d[1], r * 0.2, r * 0.2, TOOTH)
    lumps = [(x + rd.uniform(-0.35, 0.35) * r, y + rd.uniform(-0.25, 0.25) * r, r * rd.uniform(0.5, 0.75),
              r * rd.uniform(0.4, 0.6), rd.uniform(0, 3)) for _ in range(3)]
    blob(X, lumps, (176, 36, 48), ol=X.ol)
    X.rell(x - r * 0.15, y - r * 0.2, r * 0.38, r * 0.16, ang, (236, 170, 160), line=False)


def smear(X, x, y, r, seed=0):
    """Blood soaked into fur: a few overlapping round blots, flat red, no outline."""
    rd = random.Random(seed)
    for _ in range(5):
        X.ell(x + rd.uniform(-0.6, 0.6) * r, y + rd.uniform(-0.5, 0.5) * r, r * rd.uniform(0.35, 0.6),
              r * rd.uniform(0.3, 0.5), RED, line=False)


def blood(X, x, y, r, seed=0, flat=0.35):
    """A flat red splat on the ground: lumpy, with a few drops round it."""
    rd = random.Random(seed)
    X.poly(shag(x, y, r, r * flat, 9, 0.3, seed), RED, line=False)
    X.poly(shag(x + r * 0.1, y, r * 0.6, r * flat * 0.5, 6, 0.25, seed + 1), RED_D, line=False)
    for _ in range(5):
        a = rd.uniform(0, 2 * math.pi)
        d = r * rd.uniform(1.15, 1.5)
        X.ell(x + d * math.cos(a), y + d * flat * math.sin(a), r * 0.07, r * 0.05, RED, line=False)


# ------------------------------------------------------------------------------------------------ test sheet
def sheet(out):
    from PIL import Image, ImageDraw, ImageFont
    from satire_style import Cam, Ctx
    img = Image.new('RGB', (1800, 1500), (226, 222, 214))
    X = Ctx(ImageDraw.Draw(img), Cam(900, 750, 1.0, 1), ol=4)
    X.c.p = lambda x, y: (x, y)
    d = ImageDraw.Draw(img)
    f = ImageFont.load_default(size=26)
    cells = [('standing snarl', lambda x, y: side(X, x, y, 0.8, 1, 0, jaw=0.5)),
             ('run 0.0', lambda x, y: side(X, x, y, 0.8, 1, 1, run=0.0)),
             ('run 0.25', lambda x, y: side(X, x, y, 0.8, 1, 1, run=0.25)),
             ('run 0.5', lambda x, y: side(X, x, y, 0.8, 1, 1, run=0.5)),
             ('run 0.75', lambda x, y: side(X, x, y, 0.8, 1, 1, run=0.75)),
             ('leap', lambda x, y: side(X, x, y - 60, 0.8, 1, 3, leap=1.0, jaw=1.0)),
             ('feed: head down', lambda x, y: side(X, x, y, 0.8, -1, 2, feed=0.0, blood=0.6)),
             ('feed: ripping up', lambda x, y: side(X, x, y, 0.8, -1, 4, feed=1.0, blood=0.8, hunk=3, jaw=0.2)),
             ('front run', lambda x, y: front(X, x, y, 0.8, 0, run=0.2)),
             ('front leap', lambda x, y: front(X, x, y, 0.8, 1, leap=1.0)),
             ('front, in the net', lambda x, y: front(X, x, y, 0.8, 3, net=True, struggle=0.4)),
             ('meat, blood', lambda x, y: (blood(X, x, y - 30, 120, 2), meat(X, x - 60, y - 140, 40, 1), meat(X, x + 60, y - 120, 34, 5)))]
    for i, (name, fn) in enumerate(cells):
        cx, cy = 230 + (i % 4) * 450, 430 + (i // 4) * 480
        fn(cx, cy)
        d.text((cx - 200, cy + 20), name, fill=(0, 0, 0), font=f)
    img.save(out)


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
