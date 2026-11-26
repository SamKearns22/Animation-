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


# ================================================================================================ the kit (Open Wounds)
# Every film after Cry Minister draws its wolves here: `pose` (what the body does) then `draw` (side-on) or
# `draw_front`. side() and front() above are Cry Minister's, left exactly as they were (its frames must not change).
# What is new (Open Wounds, 24 Nov, "spruced up with the new body kits and rules"):
#   ONE outline round the whole animal: every shape's outline is laid down first, then every fill (no seams, no
#   haunch circles drawn over the body); a thin crease in the coat's own dark marks where a near leg crosses the body.
#   Legs reach their paws (two-bone reach, `_ik`): a planted paw stays put on the ground while the body moves over it
#   (walk and run are driven by the distance walked, not the clock), so nothing slides.
#   Eyes through the eye kit (rule S5): the pin pupil is cut to the eye's outline at any glance.
#   Poses: stand, walk, run, leap, land, feed (head down into the kill, the right way up, then a hunk ripped up held
#   in the jaws), sit (tail on the ground, looks round), paw (rakes the dirt), lunge (and recoil: flinch and yelp),
#   skid. Worn things: a hard hat between the ears and a hi-vis vest on the ribs, both moving with the body.
#   The blood plan (Sam's Y, 24 Nov): two reds and a wet shine, stains per wolf (muzzle, ruff, paws, vest), drops that
#   fly in arcs, land and soak in; torn vest scraps; the hat that tumbles; dust at every leap and landing.
#
#   P = wolf.pose('walk', d)                 d = wolf units walked since the start (move x by face * d * s yourself)
#   wolf.shadow(X, x, y, s, face, P)         under it, on the ground, first
#   wolf.draw(X, x, y, s, face, pal, P, wear=dict(hat=0, vest=1), blood=0.5, seed=3)
#   wolf.dust(X, x, y, s, age, seed)         a puff where a paw lands (age in seconds since it landed)
#   wolf.drops(X, x, y, ground, s, age, seed)  blood thrown up at (x, y), landing on the ground row `ground`
HAT_COLS = [(244, 204, 32), (246, 246, 240), (240, 128, 28)]      # yellow, white, orange site helmets
VEST_COLS = [((250, 122, 24), (206, 92, 14)), ((222, 236, 44), (178, 190, 30))]   # hi-vis orange, hi-vis yellow
SILVER = (206, 212, 216)
SILVER_D = (150, 156, 162)
WET = (255, 236, 236)
SOAK = (98, 30, 30)
MEAT, MEAT_D, FAT = (206, 76, 86), (150, 34, 48), (242, 204, 192)    # raw meat: pinker than blood, so it reads apart                                                # blood soaked into dust: the dark blot that stays
DUST = ((214, 196, 166), (186, 166, 136), (236, 224, 200))         # site dust: mid, under, lit


def _ellp(cx, cy, rx, ry, ang=0.0, n=28):
    c, s_ = math.cos(ang), math.sin(ang)
    return [(cx + rx * math.cos(t) * c - ry * math.sin(t) * s_, cy + rx * math.cos(t) * s_ + ry * math.sin(t) * c)
            for t in (2 * math.pi * i / n for i in range(n))]


def _lerp(a, b, u):
    return a + (b - a) * u


def _ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _ik(r, p, l1, l2, bend):
    """Two-bone reach from r towards p: the joint (elbow or knee) and the end actually reached. bend +1 puts the joint
    behind the line (a foreleg's elbow), -1 in front (a hind leg's knee). Too far: the leg goes straight."""
    dx, dy = p[0] - r[0], p[1] - r[1]
    d = max(abs(l1 - l2) + 1e-3, min(math.hypot(dx, dy), l1 + l2 - 1e-3))
    a = math.atan2(dy, dx)
    b = math.acos(max(-1.0, min(1.0, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d))))
    j = (r[0] + l1 * math.cos(a + bend * b), r[1] + l1 * math.sin(a + bend * b))
    return j, (r[0] + d * math.cos(a), r[1] + d * math.sin(a))


class _Ops:
    """The drawing as a list, so the outline can go down first for everything (one outline round the animal)."""
    def __init__(self):
        self.ops = []

    def part(self, pts, fill):                    # part of the silhouette: outlined from outside only
        self.ops.append(('part', pts, fill))

    def fill(self, pts, fill):                    # inside the silhouette: no line
        self.ops.append(('fill', pts, fill))

    def obj(self, pts, fill, w=1.0):              # a thing on the animal with its own outline (hat, vest, nose, eye)
        self.ops.append(('obj', pts, fill, w))

    def line(self, pts, w, col=OUT):
        self.ops.append(('line', pts, w, col))

    def call(self, fn):
        self.ops.append(('call', fn))

    def render(self, X):
        ol = X.ol
        k_line = getattr(X, 'line_k', 1.0)        # house_ctx: the coat's creases thin with the outline (note 16)
        X.ol = ol * 2
        for op in self.ops:
            if op[0] == 'part':
                X.poly(op[1], OUT, line=True)
        X.ol = ol
        for op in self.ops:
            k = op[0]
            if k in ('part', 'fill'):
                X.poly(op[1], op[2], line=False)
            elif k == 'obj':
                X.ol = ol * op[3]
                X.poly(op[1], op[2], line=True)
                X.ol = ol
            elif k == 'line':
                P = [X.c.p(*q) for q in op[1]]
                X.d.line(P, fill=op[3], width=max(1, int(round(X.c.w(op[2]) * k_line))), joint='curve')
            else:
                op[1](X)


def _chain(o, pts, widths, col):
    """A tapered limb as silhouette parts (quads between joints, a disc at each joint)."""
    for i in range(len(pts) - 1):
        a, b, wa, wb = pts[i], pts[i + 1], widths[i] / 2, widths[i + 1] / 2
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1e-6
        nx, ny = -dy / n, dx / n
        o.part([(a[0] + nx * wa, a[1] + ny * wa), (b[0] + nx * wb, b[1] + ny * wb),
                (b[0] - nx * wb, b[1] - ny * wb), (a[0] - nx * wa, a[1] - ny * wa)], col)
    for p, w in zip(pts, widths):
        o.part(_ellp(p[0], p[1], w / 2, w / 2, 0, 18), col)


def house_ol(ppm):
    """Open Wounds note 16 (Sam, 26 Nov: "the line work on the wolves is very thick in comparison to our house style"):
    a kit wolf's outline is the house line of a person standing at the same depth (lying._lw, the people's own weight
    for a body this many frame pixels a metre), never the old 5 wolf units, which drew about twice the people's."""
    import lying
    return float(lying._lw(ppm))


def house_ctx(X, s, ppm):
    """Set a drawing context for a kit wolf of scale s at ppm frame pixels a metre to the house line weight: the
    outline (X.ol) and every crease and brow line in proportion (X.line_k). Every film's wolves go through this."""
    ol = house_ol(ppm)
    X.line_k = min(1.0, ol / max(1e-6, 5.0 * s))
    X.ol = min(5.0 * s, ol) if 5.0 * s > 1.0 else ol
    return X


# ------------------------------------------------------------------------------------------------ poses
LEGS = dict(f1=80, f2=72, f3=22, h1=76, h2=68, h3=58)     # foreleg: upper arm, forearm, pastern; hind: thigh, shank, hock
HOME = dict(ff=64, fb=82, hf=-90, hb=-72)                  # where each paw stands under a standing wolf (x, wolf units)
WALK = dict(stride=150, duty=0.62, off=dict(hb=0.0, fb=0.25, hf=0.5, ff=0.75), lift=30)
RUN = dict(stride=400, duty=0.3, off=dict(hb=0.0, hf=0.1, ff=0.5, fb=0.6), lift=70)


def _base():
    return dict(M=(0.0, -150.0), a=0.0, st=0.0, cr=0.0,
                paws={k: (v, 0.0) for k, v in HOME.items()}, fold={k: 0.0 for k in HOME},
                neck=-0.35, pitch=0.0, jaw=0.25, snarl=1.0, ears=0.0, blink=False, look=0.0, back=False,
                tail=-0.4, curl=0.0, yelp=False, hunk=None, kind='stand')


def _gait(P, d, g, bob=4.0):
    """Walk or run from the distance travelled d: a paw on the ground stays where it landed (in the world)."""
    S_, du = g['stride'], g['duty']
    for leg, off in g['off'].items():
        u = (d / S_ + off) % 1.0
        if u < du:
            rel, y, f = du * S_ / 2 - u * S_, 0.0, 0.0
        else:
            v = (u - du) / (1 - du)
            rel = -du * S_ / 2 + _ease(v) * du * S_
            y, f = -g['lift'] * math.sin(math.pi * v), math.sin(math.pi * v)
        P['paws'][leg] = (HOME[leg] + rel, y)
        P['fold'][leg] = f
    ph = 2 * math.pi * d / S_
    return ph


def pose(kind='stand', u=0.0, **kw):
    """The body's state for one frame. kind and u:
      stand   u unused                      walk  u = distance walked (wolf units; 150 a stride)
      run     u = distance run (400 a bound) leap  u = 0 crouch .. 1 full stretch (lift= how high, from the caller)
      land    u = 0 touchdown .. 1 settled   feed  u = 0 head down in the kill .. 1 a hunk ripped up to the sky
      sit     u = seconds (the tail sweeps)  paw   u = rakes (1 a rake: lift forward, drag back through the dirt)
      lunge   u = 0 .. 1 lunge; flinch= 0 .. 1 the recoil when struck (eyes shut, ears flat, the yelp)
      skid    u = 0 running in .. 1 stopped, braced
    Extra keywords override any field (look=, back= to look over its shoulder, jaw=, snarl=, tail=, neck=, hunk=)."""
    P = _base()
    P['kind'] = kind
    if kind == 'walk':
        ph = _gait(P, u, WALK)
        P['M'] = (0.0, -150.0 + 3 * math.cos(2 * ph))
        P.update(neck=-0.18 + 0.05 * math.sin(ph), jaw=0.15, snarl=0.4, tail=-0.5 + 0.12 * math.sin(ph))
    elif kind == 'run':
        ph = _gait(P, u, RUN)
        P['M'] = (0.0, -150.0 - 16 * max(0.0, math.sin(ph + 0.9)))
        P.update(st=16 * math.sin(ph), a=-0.05 * math.sin(ph + 0.4), neck=-0.2 + 0.08 * math.sin(ph), jaw=0.45,
                 tail=0.2)
    elif kind == 'leap':
        v = max(0.0, min(1.0, u))
        lift = kw.pop('lift', 120 * math.sin(math.pi * v))
        P['M'] = (0.0, -150.0 + 30 * (1 - v) * (v < 0.15) - lift)
        mx, my = P['M']
        P.update(st=26 * v, a=-0.3 * v + 0.1 * max(0.0, v - 0.7) / 0.3, neck=-0.45 * v - 0.2, jaw=0.3 + 0.7 * v,
                 tail=0.5)
        P['paws'] = dict(ff=(mx + 160 + 60 * v, my + 110 - 70 * v), fb=(mx + 140 + 60 * v, my + 120 - 60 * v),
                         hf=(mx - 200 - 50 * v, my + 90 + 10 * v), hb=(mx - 180 - 60 * v, my + 80))
        P['fold'] = dict(ff=0.2, fb=0.3, hf=0.9, hb=0.9)
    elif kind == 'land':
        v = _ease(u)
        P['M'] = (0.0, -150.0 + 26 * math.sin(math.pi * min(1.0, u * 1.4)))
        P.update(cr=0.5 * (1 - v), a=0.12 * (1 - v), neck=-0.1, jaw=0.4)
        P['paws'].update(ff=(HOME['ff'] + 30, 0.0), fb=(HOME['fb'] + 40, 0.0))
    elif kind == 'feed':
        v = _ease(u)
        P['M'] = (-10 * (1 - v), _lerp(-128.0, -146.0, v))
        P.update(a=_lerp(0.22, -0.12, v), cr=_lerp(0.3, 0.05, v), neck=_lerp(0.36, -1.0, v),
                 pitch=_lerp(0.62, -0.62, v), jaw=_lerp(0.3, 0.32, v), snarl=1.0, tail=_lerp(-0.2, 0.1, v))
        P['paws'].update(ff=(HOME['ff'] + 10 + 24 * v, 0.0), fb=(HOME['fb'] - 36 + 10 * v, 0.0), hf=(HOME['hf'] - 22 * v, 0.0),
                         hb=(HOME['hb'] - 30 * v, 0.0))
    elif kind == 'sit':
        P['M'] = (-12.0, -122.0)
        P.update(a=-0.95, neck=-0.1, pitch=0.9, jaw=0.12, snarl=0.3, tail=-2.2 + 0.25 * math.sin(2.4 * u))
        P['paws'] = dict(ff=(26.0, 0.0), fb=(42.0, 0.0), hf=(-28.0, 0.0), hb=(-14.0, 0.0))
        P['fold'] = dict(ff=0.0, fb=0.0, hf=-1.0, hb=-1.0)          # -1: the hock lies flat on the ground
    elif kind == 'paw':
        v = u % 1.0
        hx = HOME['ff']
        if v < 0.4:
            w = v / 0.4
            x, y, f = _lerp(hx - 40, hx + 56, _ease(w)), -64 * math.sin(math.pi * w), 0.9 * math.sin(math.pi * w)
        else:
            w = (v - 0.4) / 0.6
            x, y, f = _lerp(hx + 46, hx - 40, w), 0.0, 0.0
        P['paws']['ff'] = (x, y)
        P['fold']['ff'] = f
        P['M'] = (-6.0, -146.0)
        P.update(a=0.06, neck=0.55, pitch=0.35, jaw=0.1, snarl=0.5, look=0.6, tail=-0.3)
    elif kind == 'lunge':
        fl = max(0.0, min(1.0, kw.pop('flinch', 0.0)))
        v = _ease(u) * (1 - fl)
        P['M'] = (60 * v - 44 * fl, -150.0 - 18 * v + 14 * fl)
        P.update(a=-0.16 * v - 0.12 * fl, cr=0.3 * fl, neck=-0.05 * v - 0.95 * fl, pitch=-0.1 * v - 0.35 * fl,
                 jaw=0.25 + 0.7 * v + 0.3 * fl, snarl=1.0 - fl, ears=fl, blink=fl > 0.25, yelp=fl > 0.25,
                 tail=0.3 * v - 1.3 * fl)
        mx, my = P['M']
        P['paws'].update(ff=(HOME['ff'] + mx + 50 * v, -46 * v), fb=(HOME['fb'] + mx + 30 * v, -30 * v))
        P['fold'].update(ff=0.6 * v, fb=0.5 * v)
        if fl:
            P['paws'].update(ff=(HOME['ff'] + mx + 10, -26 * math.sin(math.pi * fl)), fb=(HOME['fb'] + mx, 0.0))
    elif kind == 'skid':
        v = _ease(u)
        P['M'] = (-10 * v, _lerp(-146.0, -122.0, v))
        P.update(a=-0.18 * v, cr=0.4 * v, neck=_lerp(-0.2, -0.75, v), pitch=-0.1 * v, jaw=0.5, tail=0.1)
        P['paws'].update(ff=(HOME['ff'] + 84 * v, 0.0), fb=(HOME['fb'] + 70 * v, 0.0), hf=(HOME['hf'] + 40 * v, 0.0),
                         hb=(HOME['hb'] + 50 * v, 0.0))
    P.update(kw)
    return P


# ------------------------------------------------------------------------------------------------ the side view
def _frame(P):
    """The skeleton: body middle, shoulder, hip, neck base, head centre, all in wolf units (x forward, y down)."""
    mx, my = P['M']
    a, st, cr = P['a'], P['st'], P['cr'] * 40

    def B(px, py):
        q = _rot((px, py), a)
        return (mx + q[0], my + q[1])
    S = (58 + st / 2, cr)
    Hp = (-82 - st / 2, 2 + cr * 0.6)
    nb = B(S[0] + 30, S[1] - 30)
    na = a + P['neck']
    hc = (nb[0] + 70 * math.cos(na), nb[1] + 70 * math.sin(na))
    return B, S, Hp, nb, hc


def _legs(P, B, S, Hp):
    """Each leg's points from its root to its paw: (points, widths, paw centre, planted)."""
    L = LEGS
    out = {}
    for leg in ('ff', 'fb', 'hf', 'hb'):
        px, py = P['paws'][leg]
        f = P['fold'][leg]
        planted = py >= -0.5 and f == 0.0
        c = (px + 8, py - 10)                                  # the paw's middle (its bottom on the ground row)
        k = 1.0 if leg[1] == 'f' else 0.9
        if leg[0] == 'f':
            r = B(*S)
            th = math.radians(_lerp(76, 168, max(0.0, f)))     # pastern: down and a little forward; folded back
            wr = (c[0] - L['f3'] * math.cos(th), c[1] - L['f3'] * math.sin(th))
            el, wr = _ik(r, wr, L['f1'], L['f2'], 1)
            c = (wr[0] + L['f3'] * math.cos(th), wr[1] + L['f3'] * math.sin(th))
            out[leg] = ([r, el, wr, c], [62 * k, 30 * k, 19 * k, 17 * k], c, planted, th)
        else:
            r = B(*Hp)
            if f < 0:                                          # sitting: hock flat on the ground behind the paw
                th = math.radians(4)
            else:
                th = math.radians(_lerp(72, 150, f))
            hk = (c[0] - L['h3'] * math.cos(th), c[1] - L['h3'] * math.sin(th))
            kn, hk = _ik(r, hk, L['h1'], L['h2'], -1)
            c = (hk[0] + L['h3'] * math.cos(th), hk[1] + L['h3'] * math.sin(th))
            out[leg] = ([r, kn, hk, c], [84 * k, 46 * k, 21 * k, 17 * k], c, planted, th)
    return out



def stain(o, x, y, r, seed, wet=True, flat=1.0, drips=2):
    """Blood soaked into fur or cloth (recorded on o): a ragged patch of the dark red, the bright red where it is
    fresh, drips running down from it (screen down), and (wet) one small shine. Flat, never a lump."""
    rd = random.Random(seed)
    o.fill(shag(x, y, r, r * 0.62 * flat, 9, 0.18, seed, rd.uniform(-0.3, 0.3)), RED_D)
    for _ in range(3):
        o.fill(_ellp(x + rd.uniform(-0.45, 0.45) * r, y + rd.uniform(-0.3, 0.2) * r * flat, r * rd.uniform(0.2, 0.36),
                     r * rd.uniform(0.14, 0.24) * flat, rd.uniform(0, 3), 12), RED)
    for _ in range(drips):
        dx = rd.uniform(-0.6, 0.6) * r
        ln = r * rd.uniform(0.5, 1.1)
        w = max(1.0, r * 0.12)
        o.fill([(x + dx - w, y), (x + dx + w, y), (x + dx + w * 0.6, y + ln), (x + dx, y + ln + w),
                (x + dx - w * 0.6, y + ln)], RED_D)
    if wet and r > 8:
        o.fill(_ellp(x - r * 0.25, y - r * 0.16 * flat, r * 0.1, r * 0.06, -0.4, 10), WET)


def _amount(blood, part):
    return blood.get(part, 0.0) if isinstance(blood, dict) else float(blood or 0.0)


def draw(X, x, y, s, face, pal=0, P=None, wear=None, blood=0.0, seed=0):
    """One wolf side-on with ONE outline. (x, y) the ground under its middle, s its size (1: shoulder 200 units),
    face +1 right. P from pose(). wear = dict(hat=colour index or None, vest=colour index or None, torn=0-1).
    blood: 0-1, or per part dict(muzzle=, ruff=, paws=, vest=). Returns where the front of its jaws is (world)."""
    P = P or pose()
    wear = wear or {}
    base, dark, light = PALS[pal % len(PALS)]
    B, S, Hp, nb, hc = _frame(P)
    W = lambda px, py: (x + face * px * s, y + py * s)
    Wl = lambda pts: [W(*q) for q in pts]
    o = _Ops()
    legs = _legs(P, B, S, Hp)

    def leg(name, col, near):
        pts, ws, c, planted, th = legs[name]
        _chain(o, Wl(pts), [w_ * s for w_ in ws], col)
        _paw_w(c, col, planted, near)
        return pts

    def _paw_w(c, col, planted, near):
        o.part(Wl(_ellp(c[0] + 4, c[1] + 1, 22, 11 if planted else 12, 0.0 if planted else 0.3, 20)), col)
        if near:
            o.line(Wl([(c[0] + 14, c[1] - 3), (c[0] + 18, c[1] + 8)]), 2.6 * s)
            o.line(Wl([(c[0] + 4, c[1] - 3), (c[0] + 7, c[1] + 9)]), 2.6 * s)

    # far legs, in the coat's shadow
    leg('fb', dark, False)
    leg('hb', dark, False)
    # the tail: from the rump, streaming back (raised running, hanging, lying on the ground sitting)
    tr = B(Hp[0] - 30, Hp[1] - 24)
    ta = math.pi + 0.55 * P['tail']
    tm = (tr[0] + 52 * math.cos(ta), tr[1] + 52 * math.sin(ta))
    tip_a = ta - 0.5 * P['curl']
    tt = (tm[0] + 46 * math.cos(tip_a), tm[1] + 46 * math.sin(tip_a))
    if P['kind'] == 'sit':                                     # lying along the ground behind it, sweeping
        sw = P['tail'] + 2.2
        tm = (tr[0] - 62, -22.0)
        tt = (tm[0] - 60, -22.0 - 24 * sw)
        tip_a = math.atan2(tt[1] - tm[1], tt[0] - tm[0])
    a1 = math.atan2(tm[1] - tr[1], tm[0] - tr[0])
    o.part(Wl(shag((tr[0] + tm[0]) / 2, (tr[1] + tm[1]) / 2, 44, 22, 7, 0.2, seed + 2, a1)), base)
    o.part(Wl(shag(*tm, 46, 30, 8, 0.24, seed + 3, (a1 + tip_a) / 2)), base)
    o.part(Wl(shag(*tt, 34, 24, 6, 0.24, seed + 4, tip_a)), base)
    o.fill(Wl(shag(tt[0] + 12 * math.cos(tip_a), tt[1] + 12 * math.sin(tip_a), 24, 17, 5, 0.18, seed + 5, tip_a)),
           dark)
    # the body: chest, belly and rump as one shape, a shaggy back, a darker saddle, a pale belly
    mid = ((S[0] + Hp[0]) / 2, 0.0 + P['cr'] * 40)
    for (cx, cy, rx, ry) in ((S[0] + 6, S[1] - 4, 76, 64), (mid[0], mid[1], 94, 48), (Hp[0] + 4, Hp[1] - 6, 64, 56)):
        o.part(Wl([B(*q) for q in _ellp(cx, cy, rx, ry, 0, 30)]), base)
    o.part(Wl([B(*q) for q in shag(mid[0], mid[1] - 14, 150 + P['st'] / 2, 46, 16, 0.12, seed + 1, 0,
                                    math.pi * 1.05, math.pi * 1.95)]), base)
    o.fill(Wl([B(*q) for q in shag(mid[0] - 10, mid[1] - 36, 110, 18, 10, 0.25, seed + 5, 0,
                                    math.pi * 1.1, math.pi * 1.9)]), dark)
    o.fill(Wl([B(*q) for q in _ellp(mid[0], mid[1] + 32, 72, 14, 0, 20)]), light)
    # near legs, a crease in the coat's dark where each crosses the body
    hp_pts = leg('hf', base, True)
    o.line(Wl([(hp_pts[0][0] + 30, hp_pts[0][1] + 4), _mid(hp_pts[0], hp_pts[1], 0.6, 22)]), 3.0 * s, dark)
    fp_pts = leg('ff', base, True)
    o.line(Wl([(fp_pts[0][0] - 26, fp_pts[0][1] + 10), _mid(fp_pts[0], fp_pts[1], 0.65, -14)]), 3.0 * s, dark)
    b = _amount(blood, 'paws')
    if b > 0:                                                  # forepaws soaked to the wrist (a sock), hind a little
        for name in ('ff', 'fb', 'hf', 'hb'):
            pts, ws = legs[name][0], legs[name][1]
            k = b if name[0] == 'f' else 0.4 * b
            if k < 0.15:
                continue
            c = pts[3]
            stain(o, *W(c[0] + 6, c[1] - 4), (11 + 9 * k) * s, seed + 30 + ord(name[1]) + ord(name[0]), wet=False,
                  flat=0.7, drips=0)
    # the hi-vis vest on the ribs: follows the body (its points ride on the body's own frame), two silver bands
    vest = wear.get('vest')
    if vest is not None:
        _vest(o, B, W, S, Hp, P, VEST_COLS[vest % len(VEST_COLS)], wear.get('torn', 0.5), seed,
              _amount(blood, 'vest'), base)
    # the neck and the great ruff
    na = P['a'] + P['neck']
    for (cx, cy, rx, ry, an) in ((nb[0], nb[1], 58, 50, P['a']),
                                 ((nb[0] + hc[0]) / 2, (nb[1] + hc[1]) / 2, 48, 40, na)):
        o.part(Wl(_ellp(cx, cy, rx, ry, an, 24)), base)
    rf = (nb[0] + 4 * math.cos(P['a']) - 20 * math.sin(P['a']), nb[1] + 20 * math.cos(P['a']) + 4 * math.sin(P['a']))
    o.part(Wl(shag(*rf, 52, 72, 11, 0.22, seed + 6, P['a'] + 0.2, -math.pi * 0.4, math.pi * 0.75)), light)
    b = _amount(blood, 'ruff')
    if b > 0:
        stain(o, *W(rf[0] + 14, rf[1] + 30), 26 * s * b + 4 * s, seed + 9, drips=3)
    jaws = _head(o, W, hc, P, s, face, base, dark, light, wear, _amount(blood, 'muzzle'), seed)
    o.render(X)
    return jaws


def _chain_pts(a, b, wa, wb):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1e-6
    nx, ny = -dy / n, dx / n
    return [(a[0] + nx * wa, a[1] + ny * wa), (b[0] + nx * wb, b[1] + ny * wb), (b[0] - nx * wb, b[1] - ny * wb),
            (a[0] - nx * wa, a[1] - ny * wa)]


def _mid(a, b, u, off):
    """A point u of the way from a to b, pushed off to one side (for a crease along a limb's edge)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1
    return (a[0] + dx * u - dy / n * off, a[1] + dy * u + dx / n * off)


def _vest(o, B, W, S, Hp, P, cols, torn, seed, bl, fur):
    """The hi-vis vest: wraps the ribs from behind the shoulder blades to the loin, its points on the body's frame so
    it bends and tilts with it; two silver bands round the barrel; a torn hem (rips show the fur); blood soaked in."""
    col, dk = cols
    rd = random.Random(seed + 77)
    sx, hx = S[0], Hp[0]
    top = lambda u: (_lerp(hx + 34, sx + 30, u), _lerp(Hp[1] - 58, S[1] - 68, u))     # along the back
    bot = lambda u: (_lerp(hx + 46, sx + 30, u), _lerp(Hp[1] + 44, S[1] + 62, u))     # along the belly
    edge = [top(i / 8) for i in range(9)] + [(sx + 62, S[1] - 30), (sx + 64, S[1] + 20)]
    hem = []
    for i in range(9):
        u = 1 - i / 8
        p = bot(u)
        rip = torn * (rd.uniform(4, 16) if i % 2 else rd.uniform(-2, 3))
        hem.append((p[0], p[1] - rip))
    pts = edge + hem + [(hx + 30, Hp[1] - 6)]
    o.obj(W_([B(*q) for q in pts], W), col)
    for u in (0.32, 0.62):                                        # the silver bands (each a stripe round the barrel)
        a0, a1 = top(u - 0.045), top(u + 0.045)
        b0, b1 = bot(u - 0.045), bot(u + 0.045)
        band = [a0, a1, (b1[0], b1[1] - 6), (b0[0], b0[1] - 6)]
        o.fill(W_([B(*q) for q in band], W), SILVER)
        o.line(W_([B(*a0), B(*(b0[0], b0[1] - 6))], W), 1.6, SILVER_D)
    o.line(W_([B(*q) for q in (top(0.0), (hx + 40, Hp[1] - 4))], W), 2.0, dk)            # the back seam's fold
    if torn > 0.3:                                                # a rip in the side shows the fur under it
        c = bot(0.45)
        hole = shag(c[0], c[1] - 26, 16 * torn, 8 * torn, 6, 0.35, seed + 78)
        o.obj(W_([B(*q) for q in hole], W), fur, 0.6)
    if bl > 0:
        for k in range(3):
            u = 0.75 - 0.25 * k
            c = (_lerp(top(u)[0], bot(u)[0], 0.55), _lerp(top(u)[1], bot(u)[1], 0.55))
            stain(o, *W(*B(*c)), (16 + 8 * (k == 0)) * bl * abs(W(1, 0)[0] - W(0, 0)[0]) + 2, seed + 80 + k,
                  drips=1)


def _hunk(X, H, s, seed):
    """The hunk held in the jaws: a torn slab of meat clamped across the front teeth, hanging down below the chin
    (screen down, whatever the head's pitch), a pale fat edge, a strip dangling from it."""
    rd = random.Random(seed)
    tx, ty = H(80, 16)                                  # where the front teeth bite
    lumps = [(tx + rd.uniform(-6, 6) * s, ty + (26 + 24 * k) * s, (34 - 5 * k) * s * rd.uniform(0.9, 1.1),
              (22 - 2 * k) * s, rd.uniform(-0.4, 0.4)) for k in range(3)]
    X.poly([(tx - 8 * s, ty), (tx + 8 * s, ty), (tx + 14 * s, ty + 28 * s), (tx - 14 * s, ty + 28 * s)], MEAT)
    blob(X, lumps, MEAT, ol=X.ol)
    X.rell(tx - 6 * s, ty + 18 * s, 22 * s, 7 * s, 0.1, FAT, line=False)                 # the fat edge under the teeth
    for k in range(3):                                                                # the grain of the muscle
        X.seg((tx - 16 * s, ty + (36 + 14 * k) * s), (tx + 14 * s, ty + (40 + 14 * k) * s), 3 * s, MEAT_D)
    X.poly([(tx + 14 * s, ty + 78 * s), (tx + 22 * s, ty + 80 * s), (tx + 18 * s, ty + 108 * s),
            (tx + 12 * s, ty + 106 * s)], MEAT)                                               # a strip dangling


def W_(pts, W):
    return [W(*q) for q in pts]


def _head(o, W, hc, P, s, face, base, dark, light, wear, bl, seed):
    """The head: a heavy skull, a long muzzle, a hinged lower jaw of oversized serrated teeth; the eye through the eye
    kit; a hard hat between the ears if worn. back=True: looking back over its shoulder."""
    dirx = -1 if P['back'] else 1
    pitch = P['a'] + P['pitch']

    def H(px, py):
        q = _rot((dirx * px, py), dirx * pitch)
        return W(hc[0] + q[0], hc[1] + q[1])
    ja = 0.12 + 0.8 * P['jaw']
    hinge = (-6, 14)

    def lj(px, py):
        q = _rot((px - hinge[0], py - hinge[1]), ja)
        return H(hinge[0] + q[0], hinge[1] + q[1])
    flat = P['ears']
    ear = lambda base_, tip, back_: [H(*base_), H(_lerp(tip[0], -96, flat), _lerp(tip[1], -30, flat)), H(*back_)]
    o.part(ear((-34, -26), (-50, -86), (-6, -40)), dark)                                  # the far ear
    o.part([lj(-8, 12), lj(86, 16), lj(90, 30), lj(70, 36), lj(-6, 34)], light)            # the lower jaw
    o.fill([lj(-2, 14), lj(84, 16), lj(84, 22), lj(0, 22)], GUM)
    o.call(lambda X: teeth(X, lj(4, 14), lj(84, 16), 7, 15 * s, -1, big=(5,)))
    o.part(shag(*H(0, -6), 50 * s, 40 * s, 10, 0.12, seed + 7, (pitch if face * dirx > 0 else math.pi - pitch)), base)
    o.part([H(18, -30), H(70, -20), H(104, -6), H(106, 8), H(96, 14), H(10, 12)], base)   # the muzzle
    o.fill([H(30, 2), H(96, 8), H(96, 14), H(10, 12)], light)
    sn = 0.0 if P['yelp'] else P['snarl']
    if sn > 0:
        o.fill([H(8, 12), H(98, 14), H(96, 4 + 6 * (1 - sn)), H(10, 6)], GUM)
        for k in range(3):
            o.line([H(36 + 14 * k, -22 + 2 * k), H(44 + 14 * k, -12 + 2 * k)], 3 * s)
    o.call(lambda X: teeth(X, H(6, 12), H(96, 14), 8, 16 * s, 1, big=(1, 6)))
    o.obj(_ellp(*H(104, 0), 11 * s, 9 * s, 0, 16), NOSE)
    if bl > 0:
        stain(o, *H(80, 16), 24 * s * bl + 3 * s, seed + 8)
        stain(o, *lj(60, 30), 14 * s * bl + 2 * s, seed + 18)
    if P['hunk'] is not None:                       # a hunk clamped in the front teeth, the teeth sunk into it
        o.call(lambda X: _hunk(X, H, s, P['hunk']))
        o.call(lambda X: teeth(X, H(58, 13), H(96, 14), 3, 16 * s, 1, big=(1,)))
        o.call(lambda X: teeth(X, lj(56, 15), lj(84, 16), 3, 15 * s, -1))
    hat = wear.get('hat')
    if hat is not None:                              # the hard hat, perched between the ears, tilting with the head
        tilt = wear.get('hat_tilt', -0.12)
        def hq(px, py):                              # hat units: rotated by tilt about its base on the skull
            q = _rot((px - 14, py + 40), tilt)
            return H(14 + q[0], -40 + q[1])
        dome = [hq(-16, -38)] + [hq(14 + 31 * math.cos(t), -40 - 34 * math.sin(t))
                                 for t in (math.pi * (1 - i / 12) for i in range(13))]
        hc_ = HAT_COLS[hat % len(HAT_COLS)]
        o.obj(dome, hc_)
        o.obj([hq(-24, -42), hq(56, -42), hq(58, -34), hq(-24, -34)], hc_)               # the brim
        o.line([hq(12, -73), hq(18, -42)], 4 * s, tuple(int(c * 0.82) for c in hc_))     # the ridge
        if bl > 0.3:
            stain(o, *hq(28, -50), 8 * s * bl, seed + 19, wet=False)
    o.part(ear((-20, -26), (-36, -92), (4, -38)), base)                                    # the near ear
    o.fill(ear((-18, -34), (-31, -76), (-4, -40)), dark)
    import eyekit
    if P['blink']:
        o.line([H(4, -20), H(20, -12), H(38, -18)], 5 * s)                                  # squeezed shut: a chevron
        o.line([H(8, -4), H(32, -6)], 3 * s)
    else:
        eye = [H(6, -12), H(18, -22), H(36, -16), H(26, -6)]
        o.obj(eye, EYE, 0.6)
        cx, cy = H(22 + 7 * P['look'], -14)
        o.call(lambda X: eyekit.iris_and_pupil(X, eye, cx, cy, 0, None, 3.4 * s, shine=None))
    if P['yelp']:
        o.line([H(0, -30), H(40, -30)], 6 * s)                                             # brows up: hurt
    else:
        o.line([H(0, -26), H(40, -14)], 7 * s)                                             # brows down: manic
    return H(100, 20)




FRONT_K = 0.72   # Open Wounds chat 12: draw_front at the same s stands 1.38x taller than draw() (stand: 490 px against
#                  355 at one depth), so a front-on wolf among side-on ones looked twice the size; a film placing wolves
#                  at real size multiplies s by this for the front view (Cry Minister's lunges at the lens keep theirs)


def draw_front(X, x, y, s, pal=0, run=None, leap=None, jaw=0.6, blood=0.0, seed=0, look=(0.0, 0.0), blink=False,
               wear=None):
    """A dire wolf coming straight at us, with ONE outline and eye-kit eyes (Cry Minister's front(), spruced up).
    run = gait phase (forelegs pumping in turn, the head bobbing; a paw down stays down); leap 0-1 = launching at the
    lens, forelegs flung wide, jaws at full gape. wear and blood as draw()."""
    import eyekit
    wear = wear or {}
    base, dark, light = PALS[pal % len(PALS)]
    o = _Ops()
    P_ = lambda px, py: (x + px * s, y + py * s)
    bob = 14 * max(0.0, math.sin(2 * math.pi * run + 0.6)) if run is not None else 0.0
    u = max(0.0, min(1.0, leap)) if leap is not None else 0.0
    yy = -bob - 60 * u
    for k in (-1, 1):                                          # hind legs and haunches, small behind the chest
        ph = 0.0 if run is None else math.sin(2 * math.pi * (run + 0.5 + 0.1 * k))
        foot = P_(k * 66, -12 - 18 * max(0.0, ph) - 80 * u) if u or run is not None else P_(k * 66, -12)
        _chain(o, [P_(k * 58, -150 + yy), foot], [40 * s, 24 * s], dark)
        o.part(_ellp(foot[0], foot[1] + 2 * s, 22 * s, 12 * s, 0, 16), dark)
    for (cx, cy, rx, ry) in ((0, -190 + yy, 96, 74), (0, -150 + yy, 84, 50)):
        o.part(_ellp(*P_(cx, cy), rx * s, ry * s, 0, 30), base)
    vest = wear.get('vest')
    if vest is not None:                                       # the vest's front: straps round the chest, two bands
        col, dk = VEST_COLS[vest % len(VEST_COLS)]
        o.obj([P_(-98, -210 + yy), P_(98, -210 + yy), P_(90, -112 + yy), P_(-90, -112 + yy)], col)
        for k in (-1, 1):
            o.fill([P_(k * 78, -208 + yy), P_(k * 62, -208 + yy), P_(k * 56, -114 + yy), P_(k * 72, -114 + yy)], SILVER)
    paws = []
    for k in (-1, 1):                                          # forelegs: pumping in turn, or flung wide (leaping)
        if u > 0:
            sh, pw = P_(k * 60, -196 + yy), P_(k * (90 + 100 * u), -190 + yy - 70 * u)   # reaching out and up at us
        else:
            lift = 0.0 if run is None else max(0.0, math.sin(2 * math.pi * run + (0 if k < 0 else math.pi)))
            sh, pw = P_(k * 50, -170 + yy), P_(k * 48, -14 - 70 * lift)        # a planted paw stays on the ground
        mid = ((sh[0] + pw[0]) / 2 + k * (10 + 26 * u) * s, (sh[1] + pw[1]) / 2 + 20 * u * s)
        _chain(o, [sh, mid, pw], [58 * s, 36 * s, 28 * s], base)
        paws.append(pw)
    for pw in paws:
        o.part(_ellp(pw[0], pw[1], (26 + 8 * u) * s, (16 + 6 * u) * s, 0, 18), base)
        for d_ in (-12, 0, 12):
            o.line([(pw[0] + d_ * s, pw[1] + 2 * s), (pw[0] + d_ * s, pw[1] + 14 * s)], 3.4 * s,
                   TOOTH if u > 0.3 else OUT)
        if _amount(blood, 'paws') > 0.15:
            stain(o, pw[0], pw[1] - 6 * s, 16 * s * _amount(blood, 'paws'), seed + int(pw[0]), wet=False, drips=0)
    rr = 0.72 if vest is not None else 1.0
    o.part(shag(*P_(0, -226 + yy - 20 * (1 - rr)), 104 * s * rr, 84 * s * rr, 14, 0.2, seed + 1), light)   # the ruff
    if _amount(blood, 'ruff') > 0:
        stain(o, *P_(0, -186 + yy), 40 * s * _amount(blood, 'ruff') + 5 * s, seed + 9, drips=3)
    hy = -300 + yy - 10 * u
    jw = max(jaw, u)
    flat = 0.0
    for k in (-1, 1):                                          # ears up, pinned forward
        o.part([P_(k * 30, hy - 30), P_(k * 66, hy - 110), P_(k * 74, hy - 20)], base)
        o.fill([P_(k * 40, hy - 34), P_(k * 62, hy - 88), P_(k * 64, hy - 30)], dark)
    o.part(shag(*P_(0, hy), 80 * s, 64 * s, 12, 0.14, seed + 2), base)
    o.fill(shag(*P_(0, hy + 26), 66 * s, 40 * s, 10, 0.12, seed + 3, 0, 0.1, math.pi - 0.1), light)
    g = 18 + 52 * jw                                           # the mouth: two rows of serrated teeth, red gums
    o.obj([P_(-44, hy + 16), P_(44, hy + 16), P_(30, hy + 18 + g), P_(0, hy + 24 + g), P_(-30, hy + 18 + g)], MOUTH)
    if jw > 0.4:
        o.fill(_ellp(*P_(0, hy + 12 + g), 20 * s, 10 * s, 0, 16), (200, 80, 96))
    o.fill([P_(-46, hy + 8), P_(46, hy + 8), P_(44, hy + 18), P_(-44, hy + 18)], GUM)
    o.call(lambda X: teeth(X, P_(-44, hy + 16), P_(44, hy + 16), 8, 18 * s, 1, big=(0, 7)))
    o.fill([P_(-32, hy + 14 + g), P_(32, hy + 14 + g), P_(30, hy + 24 + g), P_(-30, hy + 24 + g)], GUM)
    o.call(lambda X: teeth(X, P_(-32, hy + 16 + g), P_(32, hy + 16 + g), 6, 16 * s, -1, big=(0, 5)))
    o.fill(shag(*P_(0, hy - 2), 30 * s, 14 * s, 7, 0.1, seed + 4), light)                # the muzzle, snarling
    o.obj(_ellp(*P_(0, hy - 6), 20 * s, 13 * s, 0, 18), NOSE)
    for k in (-1, 1):
        o.line([P_(k * 10, hy - 26), P_(k * 24, hy - 16)], 3 * s)
    if _amount(blood, 'muzzle') > 0:
        for k in (-1, 1):                                      # the lips and jowls, either side of the mouth
            stain(o, *P_(k * 38, hy + 22), 16 * s * _amount(blood, 'muzzle') + 2 * s, seed + 8 + k, drips=1)
    for k in (-1, 1):                                          # manic eyes through the eye kit, brows driven down
        ex, ey = P_(k * 32, hy - 30)
        if blink:
            o.line([(ex - 14 * s, ey), (ex + 14 * s, ey)], 4 * s)
        else:
            eye = [(ex - 15 * s, ey + 2 * s), (ex - 4 * s * k, ey - 9 * s), (ex + 15 * s, ey + 2 * s),
                   (ex + 2 * s * k, ey + 8 * s)]
            o.obj(eye, EYE, 0.6)
            px, py = ex + look[0] * 6 * s, ey + look[1] * 4 * s
            o.call(lambda X, eye=eye, px=px, py=py: eyekit.iris_and_pupil(X, eye, px, py, 0, None, 3.4 * s,
                                                                         shine=None))
        o.line([P_(k * 12, hy - 36), P_(k * 52, hy - 50)], 8 * s)
    hat = wear.get('hat')
    if hat is not None:                                        # the hard hat, square on, between the ears
        hc_ = HAT_COLS[hat % len(HAT_COLS)]
        o.obj([P_(-40, hy - 44)] + [P_(40 * math.cos(t), hy - 46 - 40 * math.sin(t))
                                    for t in (math.pi * i / 12 for i in range(13))], hc_)
        o.obj([P_(-56, hy - 48), P_(56, hy - 48), P_(56, hy - 40), P_(-56, hy - 40)], hc_)
        o.line([P_(0, hy - 86), P_(0, hy - 48)], 4 * s, tuple(int(c * 0.82) for c in hc_))
    o.render(X)


# ------------------------------------------------------------------------------------------------ on the ground
def _blend(X):
    from ink import glaze
    return glaze(X.d._image)          # blends onto an opaque RGBA frame (ink.glaze: these were solid black)


def shadow(X, x, y, s, face, P, alpha=0.26):
    """Under the wolf on the ground, drawn first: one pool under the body (smaller and fainter as it rises) and a flat
    oval under each paw on the ground."""
    d = _blend(X)
    B, S, Hp, nb, hc = _frame(P)
    up = max(0.0, -150.0 - P['M'][1]) / 150.0
    k = max(0.25, 1 - 0.6 * up)

    def oval(cx, rx, ry, a):
        p0, p1 = X.c.p(x + face * cx * s - rx * s, y - ry * s), X.c.p(x + face * cx * s + rx * s, y + ry * s)
        d.ellipse([min(p0[0], p1[0]), p0[1], max(p0[0], p1[0]), p1[1]], fill=(0, 0, 0, int(255 * a)))
    oval(P['M'][0] - 10, 170 * k, 16 * k, alpha * 0.8 * k)
    for name, (px, py) in P['paws'].items():
        if py >= -0.5 and P['fold'][name] == 0.0:
            oval(px + 12, 28, 7, alpha)


def dust(X, x, y, s, age, seed=0, size=1.0, spray=0.0):
    """A dust puff where a paw lands or skids (age seconds since; gone by 1.2 s): one cloud of overlapping clumps with
    one outline round it, lit on top, darker underneath, swelling fast, rising and drifting, then shrinking away.
    spray>0 throws it forward (+x, the way the skid goes)."""
    if age < 0 or age > 1.2:
        return
    rd = random.Random(seed)
    u = age / 1.2
    grow = min(1.0, age / 0.12) * (1.0 if u < 0.45 else max(0.0, 1 - (u - 0.45) / 0.55))
    o = _Ops()
    clumps = []
    for i in range(10):
        ang = math.pi * (0.05 + 0.9 * i / 9)
        far = rd.uniform(0.7, 1.3)
        dx = math.cos(ang) * 70 * far * size * (0.5 + 0.8 * u) + spray * 150 * (0.3 + u) * rd.uniform(0.4, 1.2)
        dy = -math.sin(ang) * 34 * far * size * (0.5 + u) - 40 * u * size + rd.uniform(-6, 6)
        r = rd.uniform(16, 30) * size * grow * (1.1 - 0.35 * abs(math.cos(ang)))
        if r * s < 1.5:
            continue
        clumps.append((x + dx * s, y + dy * s, r * s))
    for cx, cy, r in clumps:
        o.part(_ellp(cx, cy, r, r * 0.82, 0, 18), DUST[0])
    for cx, cy, r in clumps:
        o.fill(_ellp(cx + r * 0.1, cy + r * 0.34, r * 0.8, r * 0.42, 0, 16), DUST[1])
    for cx, cy, r in clumps:
        o.fill(_ellp(cx - r * 0.22, cy - r * 0.34, r * 0.5, r * 0.3, 0, 14), DUST[2])
    o.render(X)


def scrape(X, x, y, s, rakes, seed=0, face=1):
    """Grooves raked in the dirt by a pawing wolf (x, y where the paw rakes): one more groove per rake, each one stays,
    and the dirt it throws back piles in a low heap behind the grooves."""
    rd = random.Random(seed)
    n = min(4, int(rakes + 0.999))
    for i in range(n):
        L = min(1.0, rakes - i) * 96
        oy = (i - 1.5) * 6
        x0 = x + face * (rd.uniform(-8, 8) + 40) * s
        x1 = x0 - face * L * s
        X.d.line([X.c.p(x0, y + oy * s), X.c.p(x1, y + (oy + 1) * s)], fill=(104, 84, 62),
                 width=max(1, int(X.c.w(6 * s))))
        X.d.line([X.c.p(x0, y + (oy + 3.5) * s), X.c.p(x1, y + (oy + 4) * s)], fill=(236, 222, 196),
                 width=max(1, int(X.c.w(2 * s))))
    if rakes > 0.3:
        h = min(1.0, rakes / 3)
        hx = x - face * 70 * s
        X.poly(shag(hx, y + 2 * s, 34 * s * (0.6 + 0.4 * h), 12 * s * h, 6, 0.3, seed + 1, 0, math.pi, 2 * math.pi),
               DUST[1])


def drops(X, x, y, ground, s, age, seed=0, n=9, power=1.0, face=1):
    """Blood thrown up from (x, y): drops fly in arcs under gravity (wolf units per second at size s), land on the
    ground row and soak in as dark blots that stay. age = seconds since they were thrown."""
    rd = random.Random(seed)
    g = 1800.0 * s
    for i in range(n):
        vx = face * rd.uniform(-120, 420) * power * s
        vy = -rd.uniform(300, 720) * power * s
        r = rd.uniform(4, 9) * s
        gy = ground + rd.uniform(-12, 12) * s                     # each lands on its own spot of the ground
        # when it lands: y + vy t + g t^2 / 2 = gy
        A, Bq, C = g / 2, vy, y - gy
        tl = (-Bq + math.sqrt(max(0.0, Bq * Bq - 4 * A * C))) / (2 * A)
        if age < tl:
            px, py = x + vx * age, y + vy * age + g * age * age / 2
            vyy = vy + g * age
            sp = math.hypot(vx, vyy) or 1
            X.rell(px, py, r * 1.5, r, math.atan2(vyy, vx), RED, line=False)
            X.ell(px - vx / sp * r * 0.3, py - vyy / sp * r * 0.3, r * 0.6, r * 0.6, RED_D, line=False)
        else:
            lx = x + vx * tl
            k = min(1.0, (age - tl) / 0.4)                         # spreads as it soaks in, then stays
            X.rell(lx, gy, r * (1.4 + 0.8 * k), r * (0.5 + 0.2 * k), 0.0, RED if k < 1 else SOAK, line=False)
            X.rell(lx, gy, r * (0.8 + 0.5 * k), r * 0.35, 0.0, SOAK, line=False)


def hat_prop(X, x, y, s, ang, col=0, blood=0.0, seed=0):
    """A hard hat on its own (knocked off: the caller tumbles ang and moves it; it rests brim-down or on its side)."""
    hc_ = HAT_COLS[col % len(HAT_COLS)]
    P_ = lambda px, py: (x + _rot((px, py), ang)[0] * s, y + _rot((px, py), ang)[1] * s)
    dome = [P_(-30, 4)] + [P_(31 * math.cos(t), -34 * math.sin(t) + 4) for t in (math.pi * (1 - i / 12)
                                                                                    for i in range(13))]
    X.poly(dome, hc_)
    X.poly([P_(-40, 0), P_(42, 0), P_(44, 8), P_(-40, 8)], hc_)
    X.seg(P_(0, -30), P_(4, 2), 4 * s, tuple(int(c * 0.82) for c in hc_))
    if blood:
        o = _Ops()
        stain(o, *P_(10, -12), 10 * s * blood, seed, wet=True)
        o.render(X)


def scrap(X, x, y, s, ang, col=0, seed=0):
    """A torn scrap of hi-vis vest (flung from a kill): a jagged bit with a piece of silver band."""
    c, dk = VEST_COLS[col % len(VEST_COLS)]
    rd = random.Random(seed)
    base_ = [(-40, -16), (-14, -22), (10, -14), (38, -20), (44, 4), (20, 16), (30, 22), (-8, 18), (-34, 22), (-44, 2)]
    pts = [(x + q[0] * s, y + q[1] * s) for q in (_rot((px + rd.uniform(-4, 4), py), ang) for px, py in base_)]
    X.poly(pts, c)
    for bx in (-12, 14):
        band = [_rot((bx - 5, -19), ang), _rot((bx + 5, -19), ang), _rot((bx + 5, 18), ang), _rot((bx - 5, 18), ang)]
        X.poly([(x + q[0] * s, y + q[1] * s) for q in band], SILVER, line=False)


# ------------------------------------------------------------------------------------------------ test sheet
def cast_sheet(out):
    """The catalogue's tile (catalogue.py 'cast'): the kit's sheet."""
    kit_sheet(out)


KIT_CELLS = [
    ('stand', dict(P=('stand', 0.0), pal=0)),
    ('walk 0', dict(P=('walk', 0.0), pal=1, wear=dict(hat=0, vest=0, torn=0.2), blood=0.3)),
    ('walk 1/3', dict(P=('walk', 50.0), pal=1, wear=dict(hat=0, vest=0, torn=0.2), blood=0.3)),
    ('walk 2/3', dict(P=('walk', 100.0), pal=1, wear=dict(hat=0, vest=0, torn=0.2), blood=0.3)),
    ('run 0', dict(P=('run', 0.0), pal=3)),
    ('run 1/3', dict(P=('run', 133.0), pal=3)),
    ('leap', dict(P=('leap', 1.0), pal=4, y=-60)),
    ('land', dict(P=('land', 0.2), pal=4)),
    ('feed: head down (on a kill)', dict(P=('feed', 0.0), pal=2, blood=0.8, wear=dict(vest=1, torn=0.8), kill=True)),
    ('feed: ripping up', dict(P=('feed', 1.0, dict(hunk=3)), pal=4, blood=dict(ruff=0.8, paws=0.8, muzzle=0.3),
                              face=-1)),
    ('sit', dict(P=('sit', 0.0), pal=0, wear=dict(hat=1, vest=0, torn=0.6), blood=dict(muzzle=0.5, vest=0.6))),
    ('sit, looks round', dict(P=('sit', 1.0, dict(back=True)), pal=0, wear=dict(hat=1, vest=0, torn=0.6),
                              blood=dict(muzzle=0.5, vest=0.6))),
    ('paw the dirt', dict(P=('paw', 0.2 + 2), pal=1, wear=dict(hat=2, vest=1, torn=0.4), blood=0.4, scrape=1.6)),
    ('lunge', dict(P=('lunge', 1.0), pal=3)),
    ('recoil (struck by a bar)', dict(P=('lunge', 1.0, dict(flinch=1.0)), pal=3, bar=True)),
    ('skid', dict(P=('skid', 1.0), pal=2, dust=0.25, dx=-60)),
    ('front: run', dict(front=dict(run=0.2), pal=0, wear=dict(hat=0, vest=0), blood=0.4)),
    ('front: leap at us', dict(front=dict(leap=1.0), pal=1, blood=dict(muzzle=0.7), wear=dict(hat=1), lift=90)),
    ('hat knocked off, scrap, drops', dict(props=True)),
    ('walk, hat and vest, blood 0', dict(P=('walk', 112.0), pal=4, wear=dict(hat=2, vest=1, torn=0.0))),
]


def kit_sheet(out, cells=None, cols=4, look=True):
    """The kit's test sheet: every pose alone, on a dirt line, with its shadow (and the house look)."""
    from PIL import Image, ImageDraw, ImageFont
    from satire_style import Cam, Ctx
    cells = cells or KIT_CELLS
    rows = (len(cells) + cols - 1) // cols
    img = Image.new('RGB', (cols * 470, rows * 480 + 40), (226, 222, 214))
    X = Ctx(ImageDraw.Draw(img), Cam(0, 0, 1.0, 1), ol=4)
    X.c.p = lambda x, y: (x, y)
    d = ImageDraw.Draw(img)
    f = ImageFont.load_default(size=24)
    for i, (name, c) in enumerate(cells):
        cx, cy = 235 + (i % cols) * 470, 420 + (i // cols) * 480
        d.rectangle([cx - 235, cy, cx + 235, cy + 60], fill=(200, 184, 156))
        if c.get('front'):
            lf = c.get('lift', 0) * 0.8
            if lf:
                _blend(X).ellipse([cx - 70, cy - 8, cx + 70, cy + 8], fill=(0, 0, 0, 50))
            draw_front(X, cx, cy - lf, 0.7, c.get('pal', 0), wear=c.get('wear'), blood=c.get('blood', 0.0), seed=i,
                       **c['front'])
            d.text((cx - 215, cy + 22), name, fill=(0, 0, 0), font=f)
            continue
        if c.get('props'):
            hat_prop(X, cx - 170, cy - 22, 0.9, 0.5, 0, blood=0.6, seed=2)
            hat_prop(X, cx - 70, cy - 5, 0.9, 0.0, 1)
            scrap(X, cx + 20, cy - 10, 1.1, 0.25, 0, seed=4)
            drops(X, cx - 20, cy - 260, cy + 30, 0.8, 0.15, seed=5)
            drops(X, cx - 120, cy - 120, cy + 30, 0.8, 0.9, seed=6)
            dust(X, cx + 150, cy, 0.7, 0.25, seed=7)
            d.text((cx - 215, cy + 22), name, fill=(0, 0, 0), font=f)
            continue
        spec = c['P']
        P = pose(spec[0], spec[1], **(spec[2] if len(spec) > 2 else {}))
        face = c.get('face', 1)
        cx += c.get('dx', 0)
        shadow(X, cx, cy, 0.8, face, P)
        if c.get('kill'):                     # a stand-in kill on the dirt: a body in torn hi-vis under the head
            kx = cx + face * 150 * 0.8
            X.poly(shag(kx + 20, cy - 16, 60, 18, 8, 0.15, 3), (60, 64, 80))
            X.poly(shag(kx - 10, cy - 24, 34, 16, 6, 0.3, 4), VEST_COLS[0][0])
            blood(X, kx + 10, cy + 6, 70, 2, 0.2)
        if c.get('scrape'):
            scrape(X, cx + face * (HOME['ff'] - 20) * 0.8, cy + 4, 0.8, c['scrape'], face=face)
        draw(X, cx, cy + c.get('y', 0), 0.8, face, c.get('pal', 0), P, wear=c.get('wear'), blood=c.get('blood', 0.0),
             seed=i)
        if c.get('bar'):                      # the steel bar that struck it, at its muzzle
            jx, jy = cx + face * 170 * 0.8, cy - 230 * 0.8
            X.seg((jx + 10, jy - 90), (jx + 50, jy + 60), 16, OUT)
            X.seg((jx + 10, jy - 90), (jx + 50, jy + 60), 10, (150, 156, 164))
        if c.get('dust') is not None:
            for k, nm in enumerate(('ff', 'fb')):
                px = P['paws'][nm][0]
                dust(X, cx + face * (px + 20) * 0.8, cy, 0.8, c['dust'] + 0.05 * k, seed=k, spray=1.0, size=1.3)
        d.text((cx - 215, cy + 22), name, fill=(0, 0, 0), font=f)
    if look:
        import house_look
        img = house_look.apply(img)
    img.save(out)


def sheet(out):
    """Cry Minister's own test sheet (side(), front(): as that film drew them)."""
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
        kit_sheet(sys.argv[2])
    elif sys.argv[1] == 'cmsheet':
        sheet(sys.argv[2])
