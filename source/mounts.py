#!/usr/bin/env python3
"""mounts: a horse (or donkey, or pony) to ride, side-on, in the house style, with a rider on top.

    python3 source/mounts.py reel OUT.mp4      the test reel: standing, walk, trot, canter, gallop, a donkey (540 x 960)
    python3 source/mounts.py sheet OUT.jpg     key drawings of every gait on one sheet (for checking)
    python3 source/mounts.py check             the checks on every gait (hooves planted, legs and rider in reach)

In a film:
    m = Mount('horse')                        # or Mount('donkey'), Mount('horse', coat='grey')
    m.draw(img, cam, gx, gy, s, t, 'canter', rider=ZACK, flip=False)
gx, gy: the ground point under the withers (world); s: the same scale as the people (person units). The film slides the
world past at m.speed(gait, s) pixels a second (like driving: the mount stays put, the ground moves).

Built from Muybridge's photographs (The Horse in Motion, 1878: Sallie Gardner, standing and at the gallop) and the
standard footfall orders: walk four beats (LH LF RH RF), trot two (diagonal pairs), canter three (trailing hind, the
diagonal pair, the leading fore, then a moment in the air), gallop four with the legs gathered under the belly in the
air (never stretched out like a rocking horse). Everything is in person units (1 unit = 1.52 mm): a horse stands
1.6 m at the withers. Side view only (facing right, or left with flip=True).
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import figure as F           # noqa: E402
import kit                   # noqa: E402
import views as V            # noqa: E402
from ed import INK, curve, open_curve   # noqa: E402

M = 1.0 / V.M_PER_UNIT       # person units in a metre (658)
FH = 120.0                   # fetlock height above the ground, standing

# ------------------------------------------------------------------------------------------------ the gaits
# period: one full stride (s); duty: share of it each hoof is on the ground; stance: how far a planted hoof travels
# back under the body (units); lift: fetlock lift at the top of the swing; knee, hock: fold at the top of the swing
# (degrees); reach: how far past its landing spot the hoof swings before setting down (swing-leg retraction).
# Offsets: when in the stride each hoof lands (canter and gallop on the right lead).
GAITS = {
    'stand':  dict(period=1.0, duty=1.0, stance=0, lift=0, knee=0, hock=0, reach=0,
                   off=dict(LH=0, LF=0, RH=0, RF=0)),
    'walk':   dict(period=1.05, duty=0.62, stance=520, lift=70, knee=70, hock=35, reach=20,
                   off=dict(LH=0.0, LF=0.25, RH=0.5, RF=0.75)),
    'trot':   dict(period=0.72, duty=0.42, stance=520, lift=150, knee=95, hock=50, reach=40,
                   off=dict(LH=0.0, RF=0.0, RH=0.5, LF=0.5)),
    'canter': dict(period=0.60, duty=0.36, stance=540, lift=190, knee=105, hock=55, reach=70,
                   off=dict(LH=0.0, RH=0.2, LF=0.2, RF=0.38)),
    'gallop': dict(period=0.45, duty=0.27, stance=580, lift=230, knee=115, hock=60, reach=110,
                   off=dict(LH=0.0, RH=0.1, LF=0.38, RF=0.48)),
}
# How the rider goes with each gait: seat ('sit', 'rise' = rising trot, 'two_point' = up off the saddle, crouched),
# lean (degrees forward), lift (hips above the saddle), drop (stirrup below the seat).
RIDING = {'stand': dict(seat='sit', lean=2, lift=0, drop=385),
          'walk': dict(seat='sit', lean=4, lift=0, drop=385),
          'trot': dict(seat='rise', lean=14, lift=45, drop=360),
          'canter': dict(seat='sit', lean=10, lift=0, drop=375),
          'gallop': dict(seat='two_point', lean=26, lift=90, drop=290)}

LEGS = ('LH', 'LF', 'RH', 'RF')     # L is the side towards us (the drawing is mirrored when facing left)

# ------------------------------------------------------------------------------------------------ the breeds
COATS = {'bay': dict(coat=(150, 92, 54), points=(44, 36, 34), mane=(40, 32, 30)),
         'chestnut': dict(coat=(184, 104, 54), points=(184, 104, 54), mane=(150, 78, 40)),
         'grey': dict(coat=(208, 208, 204), points=(150, 150, 150), mane=(160, 160, 158)),
         'black': dict(coat=(56, 50, 52), points=(42, 38, 40), mane=(30, 28, 30)),
         'palomino': dict(coat=(222, 182, 110), points=(222, 182, 110), mane=(246, 236, 210))}
KINDS = {'horse': dict(k=1.0, ear=110, mane='flowing', tail='flowing', coat='bay', muzzle=None),
         'pony': dict(k=0.8, ear=90, mane='thick', tail='flowing', coat='grey', muzzle=None),
         'donkey': dict(k=0.72, ear=230, mane='brush', tail='tuft', coat=None, muzzle=(232, 228, 220),
                        colours=dict(coat=(146, 136, 128), points=(146, 136, 128), mane=(70, 62, 58)))}

# The body's outline (horse frame: x forward, y down, ground at 0), each point with how much the neck's nod moves it
BODY = [(0, -1050, 0), (-130, -1005, 0), (-300, -998, 0), (-450, -1012, 0), (-600, -1048, 0), (-710, -1035, 0),
        (-780, -995, 0), (-830, -915, 0), (-838, -830, 0), (-808, -740, 0), (-742, -662, 0), (-650, -612, 0),
        (-520, -612, 0), (-430, -640, 0), (-250, -606, 0), (-60, -594, 0), (80, -604, 0), (150, -616, 0),
        (235, -655, 0), (296, -740, 0), (322, -832, 0.05), (372, -930, 0.2), (440, -1060, 0.5), (498, -1210, 0.8),
        (520, -1330, 1.0), (472, -1440, 1.0), (362, -1392, 0.9), (240, -1272, 0.65), (120, -1142, 0.35)]
POLL = (472, -1440)
NECK_PIVOT = (250, -950)
CENTRE = (-250, -820)
SEAT = (-170, -1005)
STIRRUP = (-115, -1000)
SHOULDER = (190, -830)        # front leg's top joint
HIP = (-560, -890)            # hind leg's top joint
ROOT = {'F': 200.0, 'H': -600.0}   # where each hoof stands, under the body
FRONT = (250, 300, 225)       # humerus, forearm, cannon
HIND = (320, 330, 290)        # femur, gaskin, cannon
HEAD_LEN = 420


def _rot(p, a, c=(0.0, 0.0)):
    ca, sa = math.cos(a), math.sin(a)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)


def _ik(root, target, l1, l2, pole):
    """2D two-bone: the middle joint on the `pole` side (a direction). Returns (middle, stretched?)."""
    dx, dy = target[0] - root[0], target[1] - root[1]
    d = math.hypot(dx, dy) or 1e-6
    stretched = d > (l1 + l2) * 0.995
    dc = min(max(d, abs(l1 - l2) + 1e-3), l1 + l2 - 1e-3)
    nx, ny = dx / d, dy / d
    along = (l1 * l1 - l2 * l2 + dc * dc) / (2 * dc)
    h = math.sqrt(max(0.0, l1 * l1 - along * along))
    px, py = -ny, nx
    if px * pole[0] + py * pole[1] < 0:
        px, py = -px, -py
    return (root[0] + nx * along + px * h, root[1] + ny * along + py * h), stretched


def _ease(u):
    return u * u * (3 - 2 * u)


class Frame:
    """Horse frame -> world: x forward, y down, ground at 0, scaled like a person (flip: facing left)."""
    def __init__(self, cam, gx, gy, s, flip=False):
        self.cam, self.gx, self.gy, self.k, self.f = cam, gx, gy, s, -1 if flip else 1
        self.s = cam.s * s

    def W(self, x, y):
        return self.gx + self.f * self.k * x, self.gy + self.k * y

    def P(self, x, y):
        return self.cam.P(*self.W(x, y))

    def S(self, v):
        return self.cam.S(v * self.k)


def _tube(p, pts, widths, col, lw=2.4):
    """A tapering limb through the points, outlined (a hoof or a strand of tail on the same pen)."""
    P = np.asarray(pts, float)
    dense, wd = [], []
    for i in range(len(P) - 1):
        for u in np.linspace(0, 1, 10, endpoint=False):
            dense.append(P[i] + (P[i + 1] - P[i]) * u)
            wd.append(widths[i] + (widths[i + 1] - widths[i]) * u)
    dense.append(P[-1])
    wd.append(widths[-1])
    D = np.asarray(dense)
    T = np.gradient(D, axis=0)
    N = np.stack([-T[:, 1], T[:, 0]], 1) / (np.hypot(*T.T)[:, None] + 1e-9)
    left, right = D + N * np.asarray(wd)[:, None], D - N * np.asarray(wd)[:, None]
    p.poly(curve([tuple(v) for v in np.vstack([left, right[::-1]])], 2), col, INK, lw)


class Mount:
    def __init__(self, kind='horse', coat=None, blaze=False, saddle=(92, 56, 36), cloth=(190, 44, 52)):
        self.kind = kind
        self.kd = dict(KINDS[kind])
        self.c = dict(self.kd.get('colours') or COATS[coat or self.kd['coat']])
        self.blaze, self.saddle_c, self.cloth = blaze, saddle, cloth
        self.k = self.kd['k']

    # -------------------------------------------------------------------------------------------- motion
    def speed(self, gait, s=1.0):
        """World pixels a second the ground slides past (planted hooves stay put on it)."""
        g = GAITS[gait]
        if gait == 'stand':
            return 0.0
        return g['stance'] * self.k / (g['period'] * g['duty']) * s

    def phase(self, gait, t):
        return (t / GAITS[gait]['period']) % 1.0

    def body_motion(self, gait, t):
        """(bob down, pitch nose-down radians, neck nod radians) for this moment."""
        p = self.phase(gait, t)
        if gait == 'stand':
            return 1.5 * math.sin(2 * math.pi * t / 4.2), 0.0, math.radians(1.5 * math.sin(2 * math.pi * t / 5.1))
        if gait == 'walk':
            return 10 * math.cos(4 * math.pi * (p - 0.18)), math.radians(1.2 * math.sin(2 * math.pi * p)), \
                math.radians(4 * math.cos(4 * math.pi * (p - 0.3)))
        if gait == 'trot':
            return 24 * math.cos(4 * math.pi * (p - 0.21)), 0.0, math.radians(1.5 * math.cos(4 * math.pi * (p - 0.25)))
        if gait == 'canter':
            return 26 * math.cos(2 * math.pi * (p - 0.38)), math.radians(4 * math.sin(2 * math.pi * (p - 0.12))), \
                math.radians(7 * math.cos(2 * math.pi * (p - 0.5)))
        return 30 * math.cos(2 * math.pi * (p - 0.42)), math.radians(5 * math.sin(2 * math.pi * (p - 0.17))), \
            math.radians(10 * math.cos(2 * math.pi * (p - 0.5)))

    def body(self, pt, w, motion):
        """A body point (horse frame, unscaled) after the neck's nod, the pitch and the bob, scaled to the kind."""
        bob, pitch, nod = motion
        q = _rot(pt, nod * w, NECK_PIVOT) if w else pt
        q = _rot(q, pitch, CENTRE)
        return q[0] * self.k, q[1] * self.k + bob * self.k

    def hoof(self, gait, leg, t):
        """(fetlock point, hoof angle radians (+ = toe folding back), planted?) in the horse frame (scaled)."""
        g, k = GAITS[gait], self.k
        root = ROOT[leg[1]]
        if gait == 'stand':
            return (root * k - 62 * k, -FH * k), 0.0, True
        p = (t / g['period'] - g['off'][leg]) % 1.0
        L, duty = g['stance'], g['duty']

        def stance_at(u):
            hx = root + L / 2 - L * u                          # the hoof's contact point, sliding back at the body's speed
            tilt = math.radians(30) * max(0.0, (u - 0.8) / 0.2) ** 1.5   # heel lifting over the toe at push-off
            toe = (hx + 43, 0.0)
            f = _rot((hx - 62, -FH), tilt, toe)               # rotate the fetlock about the toe
            return f, tilt
        if p < duty:
            f, a = stance_at(p / duty)
            return (f[0] * k, f[1] * k), a, True
        u = (p - duty) / (1 - duty)
        f0, a0 = stance_at(1.0)
        f1, _ = stance_at(0.0)
        fold = math.sin(math.pi * min(1.0, u / 0.85)) if u < 0.85 else 0.0
        if u < 0.8:                                           # forward, a little past the landing spot...
            x = f0[0] + (f1[0] + g['reach'] - f0[0]) * _ease(u / 0.8)
        else:                                                 # ...then drawn back onto it (swing-leg retraction)
            x = f1[0] + g['reach'] * (1 - _ease((u - 0.8) / 0.2))
        lift = g['lift'] * math.sin(math.pi * u) ** 0.8
        y = f0[1] + (f1[1] - f0[1]) * u - lift
        peak = math.radians(g['knee'] if leg[1] == 'F' else g['hock'] * 1.6)
        a = a0 * max(0.0, 1 - u / 0.3) + peak * fold - math.radians(8) * math.sin(math.pi * max(0.0, (u - 0.8) / 0.2))
        return (x * k, y * k), a, False

    def legs(self, gait, t, motion):
        """Every leg's joints (scaled horse frame): dict leg -> list of points top to fetlock, the hoof angle, and
        any problems (a leg that would have to stretch)."""
        g = GAITS[gait]
        out, bad = {}, []
        k = self.k
        for leg in LEGS:
            f, a, planted = self.hoof(gait, leg, t)
            p = (t / g['period'] - g['off'][leg]) % 1.0
            u = 0.0 if planted else (p - g['duty']) / (1 - g['duty'])
            fold = math.sin(math.pi * min(1.0, u / 0.85)) if (not planted and u < 0.85) else 0.0
            if leg[1] == 'F':
                top = self.body(SHOULDER, 0, motion)
                hu, fo, ca = (v * k for v in FRONT)
                kn = math.radians(g['knee']) * fold
                eff = math.sqrt(fo * fo + ca * ca + 2 * fo * ca * math.cos(kn))
                elbow, s1 = _ik(top, f, hu, eff, (-1.0, 0.25))     # the elbow points back
                knee, _ = _ik(elbow, f, fo, ca, (1.0, 0.0))       # the knee folds forward
                pts = [top, elbow, knee, f]
                stretched = s1
            else:
                top = self.body(HIP, 0, motion)
                fe, ga, ca = (v * k for v in HIND)
                gam = math.radians(8 + 0.06 * (f[0] / k - (ROOT['H'] - 62)))
                gam -= math.radians(g['hock']) * fold
                hock = (f[0] - ca * math.sin(gam), f[1] - ca * math.cos(gam))
                stifle, stretched = _ik(top, hock, fe, ga, (1.0, 0.1))  # the stifle points forward
                pts = [top, stifle, hock, f]
            if stretched:
                bad.append(f'{self.kind} {gait} {leg} at {t:.2f}s: the leg would have to stretch')
            out[leg] = (pts, a, planted)
        return out, bad

    # -------------------------------------------------------------------------------------------- drawing
    def _leg(self, p, pts, a, leg, far):
        c = self.c
        k, w = self.k, self.k ** 0.55                              # small mounts keep sturdy legs
        coat = B.dk(c['coat'], 0.8) if far else c['coat']
        pts_c = B.dk(c['points'], 0.8) if far else c['points']
        f = pts[-1]
        hoof = [(25, 62), (65, 58), (105, 120), (20, 120)]      # coronet back, front, toe, heel (fetlock at 0, 0)
        q = [(f[0] + v[0] * k, f[1] + v[1] * k) for v in [_rot(h, a) for h in hoof]]
        pc = [(f[0] + v[0] * k, f[1] + v[1] * k) for v in [_rot(h, a) for h in [(-16, -10), (20, -16), (62, 66), (22, 66)]]]
        p.poly(curve(q, 2), B.dk((70, 64, 62), 0.85) if far else (70, 64, 62), INK, 2.4)
        p.poly(curve(pc, 3), pts_c, INK, 2.2)                     # the pastern
        p.ell(f[0], f[1], 26 * w, 24 * w, pts_c, INK, 2.2)        # the fetlock joint, under the cannon's end
        top = [62 * w, 38 * w, 28 * w] if leg[1] == 'F' else [76 * w, 44 * w, 28 * w]
        _tube(p, pts[:3], top, coat)
        _tube(p, pts[2:], [29 * w, 23 * w], pts_c)

    def _tail(self, p, gait, t, motion):
        k, kd = self.k, self.kd
        root = self.body((-780, -995), 0, motion)
        swing = {'stand': 8, 'walk': 18, 'trot': 35, 'canter': 55, 'gallop': 72}[gait]
        swish = 6 * math.sin(2 * math.pi * t / 2.8) if gait == 'stand' else 5 * math.sin(2 * math.pi * self.phase(gait, t))
        a0 = math.radians(swing + swish)                          # from straight down, swung back
        spine = []
        n = 6
        ln = (560 if kd['tail'] == 'flowing' else 420) * k
        for i in range(n + 1):
            u = i / n
            a = a0 + math.radians(10 * u * math.sin(2 * math.pi * (t * 1.3 - u * 0.6)))
            prev = spine[-1] if spine else root
            if not spine:
                spine.append(root)
                continue
            seg = ln / n
            spine.append((prev[0] - math.sin(a) * seg, prev[1] + math.cos(a) * seg - (u * 30 * k if i == 1 else 0)))
        if kd['tail'] == 'tuft':
            _tube(p, spine[:-1], [14 * k] * (len(spine) - 1), self.c['coat'])
            e = spine[-2]
            d = (spine[-1][0] - e[0], spine[-1][1] - e[1])
            tip = [(e[0] + d[0] * 1.6, e[1] + d[1] * 1.6)]
            p.poly(curve([(e[0] - 18 * k, e[1]), (e[0] + 18 * k, e[1])] + tip, 3), self.c['mane'], INK, 2.2)
            return
        widths = [26 * k, 46 * k, 58 * k, 60 * k, 54 * k, 40 * k, 8 * k]
        _tube(p, spine, widths, self.c['mane'])

    def _head(self, p, motion, t, blink):
        k, c = self.k, self.c
        bob, pitch, nod = motion
        poll = self.body(POLL, 1.0, motion)
        phi = math.radians(52) + nod * 1.3 + pitch
        ux, uy = math.cos(phi), math.sin(phi)
        nx, ny = -math.sin(phi), math.cos(phi)
        L = HEAD_LEN / 420.0 * k * (1.12 if self.kind == 'donkey' else 1.0)

        def H(a, b):
            return poll[0] + (a * ux + b * nx) * L, poll[1] + (a * uy + b * ny) * L
        ear = self.kd['ear']
        for far in (True, False):                                 # the far ear behind the head
            dx = 22 if far else 0
            tip = (-ear * 0.86 + dx, -ear * 0.42 - 6)
            pts = [H(4 + dx, -2), H(-ear * 0.35 + dx, -ear * 0.32), H(*tip), H(-ear * 0.5 + dx, -ear * 0.08), H(44 + dx, -14)]
            col = B.dk(c['coat'], 0.8) if far else c['coat']
            if far:
                p.poly(curve(pts, 4), col, INK, 2.4)
        head = [(0, -16), (80, -26), (160, -24), (260, -16), (360, -6), (412, 14), (432, 50), (426, 92), (398, 112),
                (330, 108), (262, 132), (196, 190), (120, 214), (46, 190), (6, 130), (-14, 60)]
        p.poly(curve([H(*v) for v in head], 4), c['coat'], INK, 2.6)
        if self.kd['muzzle']:
            p.poly(curve([H(*v) for v in [(330, 0), (412, 14), (432, 50), (426, 92), (398, 112), (330, 108), (316, 60)]], 4),
                   self.kd['muzzle'], INK, 2.2)
        if self.blaze:
            p.poly(curve([H(*v) for v in [(70, -18), (120, 10), (300, 18), (410, 30), (400, -2), (260, -14), (110, -24)]], 3),
                   (246, 244, 238), None)
        # ear in front, then the face: eye (almond, small pupil), nostril, mouth, bridle
        pts = [H(4, -2), H(-ear * 0.35, -ear * 0.32), H(-ear * 0.86, -ear * 0.42 - 6), H(-ear * 0.5, -ear * 0.08), H(44, -14)]
        p.poly(curve(pts, 4), c['coat'], INK, 2.4)
        p.poly(curve([H(-ear * 0.3, -ear * 0.22), H(-ear * 0.7, -ear * 0.34), H(-ear * 0.45, -ear * 0.12)], 3),
               B.dk(c['coat'], 0.7), None)
        ex, ey = H(118, 34)
        if blink:
            p.line([H(98, 30), H(138, 38)], INK, 2.6)
        else:
            eye = [H(96, 32), H(112, 20), H(134, 24), H(146, 38), H(128, 46), H(108, 44)]
            p.poly(curve(eye, 4), (250, 246, 238), INK, 2.2)
            p.ell(ex + 2 * k, ey, 9 * k, 9 * k, (60, 40, 30), None)
            p.ell(ex + 2 * k, ey, 4.5 * k, 4.5 * k, INK, None)
            p.line(open_curve([H(94, 28), H(116, 16), H(146, 30)], 4), INK, 2.6)   # the upper lid
        p.line(open_curve([H(374, 40), H(392, 50), H(386, 64)], 4), INK, 3.0)       # nostril
        p.line(open_curve([H(424, 92), H(392, 96), H(360, 92)], 4), INK, 2.4)       # mouth
        strap = (40, 30, 26)
        p.line([H(36, -18), H(70, 190)], strap, 9)                                   # cheekpiece
        p.line([H(30, -12), H(56, -30)], strap, 9)                                   # browband
        p.line([H(300, -14), H(318, 112)], strap, 9)                                 # noseband
        bit = H(352, 96)
        p.ell(bit[0], bit[1], 13 * k, 13 * k, None, (196, 196, 200), 4)
        return bit

    def _mane(self, p, motion, t, gait):
        k, kd = self.k, self.kd
        crest = [self.body(v, w, motion) for v in [(472, -1440), (362, -1392), (240, -1272), (120, -1142), (10, -1060)]
                 for w in [{472: 1.0, 362: 0.9, 240: 0.65, 120: 0.35, 10: 0.0}[v[0]]]]
        stream = {'stand': 0, 'walk': 10, 'trot': 25, 'canter': 45, 'gallop': 70}[gait]
        top, low = [], []
        for i, (x, y) in enumerate(crest):
            u = i / (len(crest) - 1)
            wave = 10 * math.sin(2 * math.pi * (t * 1.5 + u * 1.2))
            if kd['mane'] == 'brush':                               # a donkey's short upright mane
                top.append((x + 6 * k, y - 34 * k))
                low.append((x - 6 * k, y + 22 * k))
                continue
            hang = (95 if kd['mane'] == 'thick' else 75) * k
            top.append((x - 4 * k, y - 16 * k))
            low.append((x - (stream + wave * 0.4) * k * 1.4 - 10 * k, y + hang - stream * k * 0.5 + wave * k))
        lumpy = []
        for i, q in enumerate(low[::-1]):
            lumpy.append(q)
            if 0 < i < len(low):
                a, b = low[::-1][i - 1], q
                lumpy.append(((a[0] + b[0]) / 2 - 8 * k, (a[1] + b[1]) / 2 - 22 * k))
        p.poly(curve(top + lumpy, 3), self.c['mane'], INK, 2.4)
        if kd['mane'] != 'brush':                                   # the forelock over the brow
            poll = crest[0]
            p.poly(curve([(poll[0] - 4 * k, poll[1] - 10 * k), (poll[0] + 50 * k, poll[1] + 10 * k),
                          (poll[0] + 70 * k, poll[1] + 70 * k), (poll[0] + 30 * k, poll[1] + 40 * k)], 3),
                   self.c['mane'], INK, 2.2)

    def _saddle(self, p, motion):
        k = self.k
        cloth = [self.body(v, 0, motion) for v in [(-20, -1052), (-350, -1004), (-345, -870), (-40, -880)]]
        p.poly(curve(cloth, 2), self.cloth, INK, 2.4)
        seat = [self.body(v, 0, motion) for v in [(-30, -1080), (-60, -1040), (-280, -1030), (-320, -1066),
                                                  (-300, -1010), (-60, -1010)]]
        p.poly(curve(seat, 3), self.saddle_c, INK, 2.4)
        flap = [self.body(v, 0, motion) for v in [(-60, -1016), (-230, -1012), (-215, -905), (-90, -900)]]
        p.poly(curve(flap, 2), B.dk(self.saddle_c, 0.9), INK, 2.2)
        g0, g1 = self.body((-120, -900), 0, motion), self.body((-60, -600), 0, motion)
        p.line([g0, g1], (60, 46, 38), 16 * k)                    # the girth

    def draw(self, img, cam, gx, gy, s, t, gait, rider=None, flip=False, blink=False):
        """The mount (and its rider) with the ground point under the withers at world (gx, gy), scale s."""
        fr = Frame(cam, gx, gy, s, flip)
        p = B.Pen(img, fr)
        motion = self.body_motion(gait, t)
        legs, bad = self.legs(gait, t, motion)
        kit.contact_shadow(img, cam, gx - (1 if not flip else -1) * 260 * s * self.k, gy, 1300 * s * self.k, alpha=0.22)
        for leg in ('RH', 'RF'):
            pts, a, _ = legs[leg]
            self._leg(p, pts, a, leg, True)
        self._tail(p, gait, t, motion)
        for leg in ('LH', 'LF'):
            pts, a, _ = legs[leg]
            self._leg(p, pts, a, leg, False)
        outline = [self.body((x, y), w, motion) for x, y, w in BODY]
        p.poly(curve(outline, 4), self.c['coat'], INK, 2.8)
        sh = B.dk(self.c['coat'], 0.86)                           # soft modelling: belly shadow, shoulder and hip lines
        p.poly(curve([self.body(v, 0, motion) for v in [(-400, -660), (-250, -606), (-60, -594), (80, -604), (60, -650),
                                                         (-120, -640), (-300, -652)]], 3), sh, None)
        p.line(open_curve([self.body(v, 0, motion) for v in [(150, -1000), (215, -860), (230, -720)]], 4), sh, 5)
        p.line(open_curve([self.body(v, 0, motion) for v in [(-470, -1000), (-560, -880), (-520, -700)]], 4), sh, 5)
        bit = self._head(p, motion, t, blink)
        self._mane(p, motion, t, gait)
        out = dict(legs=legs, bad=bad, bit=fr.W(*bit), frame=fr)
        if rider:
            self._saddle(p, motion)
            out['rider'] = self.ride(img, cam, fr, rider, gait, t, motion, bit, flip)
        return out

    # -------------------------------------------------------------------------------------------- the rider
    def ride(self, img, cam, fr, sp, gait, t, motion, bit, flip):
        r = RIDING[gait]
        bob, pitch, nod = motion
        p = self.phase(gait, t)
        lift = r['lift']
        if r['seat'] == 'rise':                                     # up on one diagonal, down on the other
            lift = r['lift'] * 0.5 * (1 - math.cos(2 * math.pi * (p - 0.06)))
        elif r['seat'] == 'two_point':                              # knees soak up the bounce: the hips stay steadier
            lift = r['lift'] + 0.6 * bob * self.k
        lean = r['lean'] - math.degrees(pitch) * 0.6
        seat = self.body(SEAT, 0, motion)
        sw = fr.W(*seat)
        s = fr.k
        f = fr.f
        rx, ry = sw[0], sw[1] - (V.HIP_Y + lift) * s
        j = V.standing(sp)
        j['lean'], j['bob'] = lean, 0.0
        j['hide_legs'] = {'R'}                                      # the far leg is behind the horse

        def local(w):                                              # world -> rider units (z forward, y down)
            return (w[0] - rx) / (s * f), (w[1] - ry) / s
        st = fr.W(*self.body(STIRRUP, 0, motion))
        z, _ = local(st)
        drop = r['drop']
        for side, sg in (('L', -1), ('R', 1)):                      # feet in the stirrups, either side of the barrel
            j['foot' + side] = (sg * max(115.0, 165.0 * self.k), V.HIP_Y + lift + drop,
                                z + (10.0 if r['seat'] == 'two_point' else 40.0))
            j['knee_pole' + side] = (0.35 * sg, -0.2, 1.0)
        # hands low over the withers, either side of the neck, giving a little with the head's nod
        hand_h = self.body((95 if r['seat'] != 'two_point' else 115, -1110 if r['seat'] != 'two_point' else -1085),
                           0.25, (bob, pitch, nod * 1.4))
        hz, hy = local(fr.W(*hand_h))
        L_ = math.radians(lean)
        dy = (hy - V.HIP_Y) * math.cos(L_) - hz * math.sin(L_)     # unlean: arm_to takes the torso's own frame
        zz = (hy - V.HIP_Y) * math.sin(L_) + hz * math.cos(L_)
        probs = []
        for side, sg in (('L', -1), ('R', 1)):
            tgt = (sg * 62.0, V.HIP_Y + dy, zz)
            if not V.reach_ok(j, side, tgt, 'grip'):
                probs.append(f'rider {gait} at {t:.2f}s: the {side} hand cannot reach the reins')
            V.arm_to(j, side, tgt, 'down', 'grip')
            hip = (sg * 55.0, V.HIP_Y, 0.0)
            d = math.dist(hip, j['foot' + side])
            if d > (V.THIGH + V.SHIN) * 0.99:
                probs.append(f'rider {gait} at {t:.2f}s: the {side} leg cannot reach the stirrup ({d:.0f})')
        q = dict(sp, bottom=min(sp.get('bottom', V.JACKET), 470))
        j2 = V.person(img, cam, rx, ry, s, q, t, -90 if flip else 90, j)
        L = B.Local(cam, rx, ry, s, f)
        pen = B.Pen(img, L)
        fl = j2['footL']                                           # the near stirrup: leather from the saddle, the iron
        sw_l = local(fr.W(*self.body((STIRRUP[0], STIRRUP[1] + 30), 0, motion)))
        pen.line([(sw_l[0], sw_l[1]), (fl[0] + 20, fl[1] + 26)], (60, 44, 34), 9)
        pen.poly([(fl[0] - 6, fl[1] + 20), (fl[0] + 48, fl[1] + 20), (fl[0] + 44, fl[1] + 46), (fl[0] - 2, fl[1] + 46)],
                 None, (176, 176, 182), 6)
        # reins: from each fist to the bit, with a little slack
        bw = local(fr.W(*bit))
        for sd in ('R', 'L'):
            el, wr = j2['el' + sd], j2['wr' + sd]
            dx, dyy = wr[0] - el[0], wr[1] - el[1]
            n = math.hypot(dx, dyy) or 1
            hand = (wr[0] + dx / n * 14, wr[1] + dyy / n * 14)
            mid = ((hand[0] + bw[0]) / 2, (hand[1] + bw[1]) / 2 + 26)
            pen.line(open_curve([hand, mid, bw], 6), (52, 36, 28), 7)
            if sd == 'L':
                B.gesture_hand(pen, el, wr, 'grip', sp.get('glove', sp['skin']))   # the near fist over its rein
        return dict(problems=probs, j2=j2)


# ------------------------------------------------------------------------------------------------ checks
def check(mount=None, gaits=None):
    """Every gait sampled finely: planted hooves never slide on the ground, no leg stretches, the rider reaches."""
    import burnham as B_
    B_.SS = 1
    probs = []
    for kind in ([mount] if mount else ['horse', 'donkey']):
        m = Mount(kind)
        for gait in gaits or GAITS:
            g = GAITS[gait]
            v = m.speed(gait)
            last = {}
            for i in range(int(g['period'] * 240) + 1):
                t = i / 240.0
                motion = m.body_motion(gait, t)
                legs, bad = m.legs(gait, t, motion)
                probs += bad
                for leg in LEGS:
                    f, a, planted = m.hoof(gait, leg, t)
                    toe_w = f[0] + v * t                            # world position of the fetlock
                    if planted and a == 0.0:
                        if leg in last and abs(last[leg] - toe_w) > 1.0:
                            probs.append(f'{kind} {gait} {leg} at {t:.3f}s: a planted hoof slid {abs(last[leg] - toe_w):.1f}')
                        last[leg] = toe_w
                    else:
                        last.pop(leg, None)
                    if not planted and f[1] > -FH * m.k + 1:
                        probs.append(f'{kind} {gait} {leg} at {t:.3f}s: a lifted hoof goes through the ground')
                n_down = sum(m.hoof(gait, lg, t)[2] for lg in LEGS)
                if gait == 'walk' and n_down < 2:
                    probs.append(f'{kind} walk at {t:.3f}s: fewer than two hooves down')
    return sorted(set(probs))


# ------------------------------------------------------------------------------------------------ test reel
SKY, GRASS, GRASS_D, HILL = (196, 222, 236), (150, 186, 110), (128, 164, 92), (170, 200, 140)
GROUND_Y = 1520
SCALE = 0.56
SECTIONS = [('Standing (breathing, tail swish)', 'stand', 2.5, 'horse', False),
            ('Walk: four beats, left hind, left fore, right hind, right fore', 'walk', 4.0, 'horse', False),
            ('Trot: diagonal pairs; the rider rises every other beat', 'trot', 4.0, 'horse', False),
            ('Canter: three beats and a moment in the air', 'canter', 4.0, 'horse', False),
            ('Gallop: legs gathered under the belly in the air; rider up off the saddle', 'gallop', 4.0, 'horse', False),
            ('Gallop, the other way', 'gallop', 2.5, 'horse', True),
            ('Donkey: the same walk, smaller, long ears', 'walk', 3.5, 'donkey', False)]


def scene(img, cam, x_world, speed_scale=1.0):
    """A field that slides past: sky, far hills (slow), grass, fence posts and tufts (at the ground's speed)."""
    p = B.Pen(img, cam)
    p.poly([(0, 0), (1080, 0), (1080, GROUND_Y), (0, GROUND_Y)], SKY, None)
    off = x_world * 0.15
    hills = [(-200 + i * 30 - (off % 600) , GROUND_Y - 140 - 60 * math.sin(i * 0.35)) for i in range(0, 60)]
    p.poly(hills + [(1600, GROUND_Y), (-300, GROUND_Y)], HILL, None)
    p.poly([(0, GROUND_Y), (1080, GROUND_Y), (1080, 1920), (0, 1920)], GRASS, None)
    p.line([(0, GROUND_Y), (1080, GROUND_Y)], GRASS_D, 3)
    gap = 2.0 * M * SCALE                                           # a post every 2 m
    base = -(x_world % gap)
    k = 0
    while base + k * gap < 1300:
        x = base + k * gap
        p.poly([(x - 9, GROUND_Y - 300), (x + 9, GROUND_Y - 300), (x + 9, GROUND_Y - 30), (x - 9, GROUND_Y - 30)],
               (150, 116, 80), INK, 2.4)
        k += 1
    p.line([(-20, GROUND_Y - 260), (1100, GROUND_Y - 260)], (150, 116, 80), 8)
    p.line([(-20, GROUND_Y - 150), (1100, GROUND_Y - 150)], (150, 116, 80), 8)
    gap2 = 0.7 * M * SCALE
    base2 = -(x_world % gap2)
    for i in range(12):
        x = base2 + i * gap2 + 40
        y = GROUND_Y + 140 + 60 * ((i * 7) % 3)
        p.line(open_curve([(x - 14, y), (x - 6, y - 26), (x, y)], 4), GRASS_D, 4)
        p.line(open_curve([(x, y), (x + 8, y - 30), (x + 16, y)], 4), GRASS_D, 4)


def frame(gait, kind, t, flip, label=None, x_offset=0.0):
    from polanski import ZACK
    B.SS = 1
    kit.install(B)
    m = Mount(kind)
    img = B.canvas(SKY)
    cam = B.Cam(1.0, 540, 960)
    v = m.speed(gait, SCALE)
    x_world = v * t * (-1 if flip else 1)
    scene(img, cam, x_world)
    blink = (t % 3.7) < 0.17
    out = m.draw(img, cam, 610 if not flip else 470, GROUND_Y, SCALE, t, gait,
                 rider=dict(ZACK, mouth='set', brows=None), flip=flip, blink=blink)
    if label:
        from PIL import ImageDraw, ImageFont
        d = ImageDraw.Draw(img)
        f = ImageFont.truetype(B.SANS, 40)
        rows = B.wrap(label, f, 940)
        h = 50 * len(rows) + 40
        d.rectangle([0, 150, 1080, 150 + h], fill=(28, 30, 36))
        for k_, r in enumerate(rows):
            d.text((540, 190 + 50 * k_), r, font=f, fill=(210, 212, 218), anchor='mm')
    return img, out


def picture(kind='horse'):
    """One still for the kit catalogue's sheet: the mount cantering with a rider."""
    return frame('canter' if kind == 'horse' else 'walk', kind, 0.2, False)[0]


def reel_frame(i):
    from PIL import Image
    t = i / 12.0
    for label, gait, dur, kind, flip in SECTIONS:
        if t < dur:
            img, _ = frame(gait, kind, t, flip, label)
            return np.asarray(img.convert('RGB').resize((540, 960), Image.LANCZOS)).tobytes()
        t -= dur
    return bytes(540 * 960 * 3)


def reel(out):
    import subprocess
    from multiprocessing import Pool
    import imageio_ffmpeg
    n = int(sum(s[2] for s in SECTIONS) * 12)
    pr = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt',
                           'rgb24', '-s', '540x960', '-r', '12', '-i', '-', '-c:v', 'libx264', '-crf', '22', '-pix_fmt',
                           'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for fr in pool.imap(reel_frame, range(n), chunksize=4):
            pr.stdin.write(fr)
    pr.stdin.close()
    pr.wait()
    print('reel:', out, f'({n / 12:.1f} s, {os.path.getsize(out) / 1e6:.1f} MB)')


def sheet(out, gaits=('stand', 'walk', 'trot', 'canter', 'gallop'), n=6, kind='horse'):
    """Each gait across one row: n drawings through one stride (cropped to the horse)."""
    from PIL import Image
    tw, th = 360, 380
    rows = []
    for gait in gaits:
        per = GAITS[gait]['period'] if gait != 'stand' else 1.0
        row = Image.new('RGB', (tw * n, th), (255, 255, 255))
        for i in range(n):
            img, _ = frame(gait, kind, per * i / n, False)
            im = img.convert('RGB').crop((40, 560, 1080, 1640)).resize((tw, int(tw * 1080 / 1040)))
            row.paste(im.crop((0, 0, tw, th)) if im.height >= th else im, (i * tw, 0))
        rows.append(row)
    sh = Image.new('RGB', (tw * n, th * len(rows)), (255, 255, 255))
    for k_, r in enumerate(rows):
        sh.paste(r, (0, k_ * th))
    sh.save(out, quality=88)
    print('sheet:', out)


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'reel':
        reel(sys.argv[2])
    elif len(sys.argv) >= 3 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
    elif len(sys.argv) >= 2 and sys.argv[1] == 'check':
        pr = check()
        print('\n'.join(pr[:40]) or 'mounts: all checks pass')
        print(len(pr), 'problems')
    else:
        print(__doc__)
