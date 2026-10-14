#!/usr/bin/env python3
"""walker: people from the burnham library walking ACROSS the frame, in a three-quarter view (first used in Cry Minister).

The library draws everyone facing us. Someone walking left to right drawn that way slides sideways with their legs
stepping at the camera (the zombie fight in Russiadent Evil, Cry Minister's first shoppers). Here the body is turned
about 45 degrees towards the way they walk, so we still see face and clothes:
  - torso and head drawn narrower (as a turned body looks), the face turned the way they walk (burnham's 'turn');
  - legs in a side-on stride: the front leg reaches, the back leg pushes off, the knee bends forward, shoes point the
    way they walk; a foot on the ground stays planted (it moves back exactly as fast as the body moves on);
  - arms swing forward and back, each against its leg; a small rise and fall each step.

    walk(img, cam, B, F, x, ground, s, sp, t, d, ph, speed)   draw one walker; returns sp as drawn (for eyelines)
    python3 source/walker.py sheet OUT.png                   a test strip of one stride
"""
import math


class Squash:
    """A camera that draws narrower about a vertical line (a body turned away from us shows less width)."""
    def __init__(self, cam, ax, kx):
        self.cam, self.ax, self.kx = cam, ax, kx
        self.z, self.cx, self.cy, self.s = cam.z, cam.cx, cam.cy, cam.s

    def P(self, x, y):
        return self.cam.P(self.ax + (x - self.ax) * self.kx, y)

    def S(self, v):
        return self.cam.S(v)


THIGH, SHIN, HIP_Y = 252, 238, 450      # the person's own units (burnham: hips at 450, soles at 928)


def _leg(hip, foot, d):
    """Knee for a leg from hip to foot, bending forward (the way the walker faces, d = +1 right, -1 left)."""
    dx, dy = foot[0] - hip[0], foot[1] - hip[1]
    L = math.hypot(dx, dy) or 1e-6
    L2 = min(L, THIGH + SHIN - 1e-3)
    a = (THIGH ** 2 - SHIN ** 2 + L2 ** 2) / (2 * L2)
    h = math.sqrt(max(0.0, THIGH ** 2 - a * a))
    ux, uy = dx / L, dy / L
    mx, my = hip[0] + ux * a, hip[1] + uy * a
    k1 = (mx - uy * h, my + ux * h)
    k2 = (mx + uy * h, my - ux * h)
    return k1 if (k1[0] - mx) * d > (k2[0] - mx) * d else k2


def stride(ph, step):
    """One leg's foot through a stride (ph 0-1): on the ground for the first half, sliding back exactly as the body moves
    on (so it stays planted), then lifted and swung forward. Returns (forward offset, lift), person units."""
    if ph < 0.5:
        u = ph / 0.5
        return step * (0.5 - u), 0.0
    u = (ph - 0.5) / 0.5
    return step * (-0.5 + u), 70 * math.sin(math.pi * u)


def walk(img, cam, B, F, x, ground, s, sp, t, d, ph, speed, turn=None, kx=0.9, limb=None, shoe=(36, 32, 30),
         arms=None, blend=0.0):
    """One person walking across the frame at `speed` (world units a second) in direction d (+1 right, -1 left).
    ph: the stride phase (0-1, one full cycle = two steps); the stride length follows the speed so feet never slide.
    turn: where the face points (-1..1); default the way they walk.
    arms: a pose's arms ({'L': .., 'R': ..}, e.g. rig.pose('hips')) eased in over the swing by blend (0-1), for someone
    stopping to react. kx: how much narrower the turned body is drawn (0.78 looked too thin: Sam, 8 Oct).
    Returns the person spec as drawn."""
    cycle = 0.95                                              # strides a second
    step = speed * 0.5 / cycle / s                            # foot travel in person units over a stance (half a stride)
    sp = dict(sp)
    w = 2 * math.pi * ph
    bob = 8 * abs(math.cos(w))                                # highest as the legs pass each other
    neck = ground - (F.SOLE_Y - bob) * s
    rig = F.Rig(sp)
    sp['arms'] = {}
    for side, sg in (('L', -1), ('R', 1)):                    # arms swing against the legs on their side
        swing = math.sin(w + (0 if side == 'L' else math.pi)) * d
        sp['arms'][side] = rig.arm(side, (sg * 135 + 55 * swing, 428 - 28 * max(0.0, swing * d)), 'fist', 'out', strict=False)
        if arms is not None and blend > 0:
            a, b = sp['arms'][side], arms[side]
            mix = lambda p, q: (p[0] + (q[0] - p[0]) * blend, p[1] + (q[1] - p[1]) * blend)
            sp['arms'][side] = (mix(a[0], b[0]), mix(a[1], b[1]), b[2] if blend >= 0.5 else a[2])
    sp['turn'] = 0.55 * d if turn is None else turn
    sp.setdefault('look', 0.8 * d)
    sp['full'] = False
    trousers = sp.get('trousers', (40, 42, 50))
    from satire_style import Ctx, Cam as SCam
    from PIL import ImageDraw
    X = Ctx(ImageDraw.Draw(img), SCam(cam.cx, cam.cy, cam.z, B.SS), ol=4)
    for k, col in ((1, B.dk(trousers, 0.78)), (0, trousers)):  # far leg first, in shadow; near leg over it
        fo, lift = stride((ph + 0.5 * k) % 1.0, step)
        hip = (d * (8 if k == 0 else -8), HIP_Y)
        foot = (hip[0] + d * fo, F.SOLE_Y - 18 - lift - bob)
        knee = _leg(hip, foot, d)
        P = lambda q: (x + q[0] * s, neck + q[1] * s)
        limb(X, P(hip), P(knee), 88 * s, col)
        limb(X, P(knee), P(foot), 72 * s, col)
        toe = (foot[0] + d * 34, foot[1] + 10)
        X.rell(*P(((foot[0] + toe[0]) / 2, foot[1] + 8)), 50 * s, 20 * s, 0.0, shoe)
    B.person(img, Squash(cam, x, kx), x, neck, s, sp, t)
    return sp


def sheet(out):
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import numpy as np
    from PIL import Image
    import burnham as B
    import figure as F
    import mossad  # noqa: F401  (brows, mouths)
    from satire_style import install_circle_hands, limb
    install_circle_hands(B)
    B.SS = 1
    img = Image.new('RGBA', (1080, 1920), (230, 226, 220, 255))
    sp = B.attendee(np.random.default_rng(3))
    sp.update(lanyard=False, pose='custom', mouth='line')
    for i in range(6):
        cam = B.Cam(0.5, 900, 1300)
        ph = i / 6
        walk(img, cam, B, F, -100 + 330 * i, 1500, 0.8, sp, 0.0, 1, ph, 640, limb=limb)
    img.convert('RGB').crop((0, 520, 1080, 1100)).save(out)


if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
