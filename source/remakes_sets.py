#!/usr/bin/env python3
"""Remakes (the Ocarina of Time remake satire): the three sets, flat paintings in the house style (flat colour, one
ink outline, hand-cut edges), one painting per camera (rule 39), from Sam's references 01, 17, 19-24. Drawn fresh,
never traced. The cast draw on top through the same B.Cam (world = 1080 x 1920 px at zoom 1), so a push-in is a
zoomed camera on the same painting.

MAP (rule 61)
  helpers ............. Level (a level pinhole in metres), blob (a scalloped clump), hand-cut edges, leaves, glow,
                        shafts, flowers, s_for (cast scale from pixels per metre)
  Kokiri Forest ....... forest(img, cam, view, t): 'up' (S1 up at KG's branch, S3 on him), 'down' (S2 from KG's eyes
                        on Link and Navi), 'close' (S4, S6 Link's close-ups), 'edge' (S5 the gunman's patch);
                        forest_front(img, cam, view) the near leaves over the cast
  the camp ............ camp(img, cam, t, gate=k): the walled Far Cry yard, one 3D-metre layout (CAMP), the gate
                        k 0 shut to 1 blown in; camp_front(img, cam) the sandbags in front of everyone
  Castle Town ......... town(img, cam, view, t): 'square' (S10 the line-up), 'wall' (S12, S13 the slam)
  stage ............... STAGE: per view, where the cast stand (screen x, ground y, pixels per metre)
  boxes ............... SET_BOXES / SET_MEANT per set (rule 83), BENCHMARK (rule 3)
  sheets .............. picture(at) for benchmark.py; alone(SET, OUT) one set's cameras with the cast for scale

    python3 source/remakes_sets.py alone forest|camp|town OUT.jpg
    python3 source/benchmark.py remakes_sets OUT.jpg
    python3 source/setcheck.py remakes_sets
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
from ed import INK, curve, open_curve, oval   # noqa: E402

NAME = 'remakes'
W, H = 1080, 1920
ADULT_PPM_AT_S1 = (928 + 150 + 92 * 1.06) / 1.75     # the cast's drawing: pixels per metre at scale s = 1


def s_for(ppm):
    """The cast's scale s for a spot where one metre is ppm pixels (remakes_cast.person, remakes_creatures.kg)."""
    return ppm / ADULT_PPM_AT_S1


def mix(a, b, u):
    return tuple(int(round(x + (y - x) * u)) for x, y in zip(a, b))


def dk(c, k=0.75):
    return tuple(int(v * k) for v in c)


# ------------------------------------------------------------------------------------------------ helpers
class Level:
    """A level camera (verticals stay vertical, as a flat painting wants): x right, d away, z up, in metres."""
    def __init__(self, h, hz, f, cx=540.0):
        self.h, self.hz, self.f, self.cx = h, hz, f, cx

    def p(self, x, d, z=0.0):
        return self.cx + self.f * x / d, self.hz - self.f * (z - self.h) / d

    def ppm(self, d):
        return self.f / d

    def d_at(self, y):
        """The ground depth seen at screen row y (below the horizon)."""
        return self.f * self.h / max(1e-3, y - self.hz)


def blob(cx, cy, rx, ry, n=12, bump=0.16, seed=0, flat_bottom=False):
    """A scalloped clump (canopy, bush, cloud, moss): an oval whose edge is a row of round bulges."""
    r = random.Random(seed)
    pts = []
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        amp = bump * r.uniform(0.6, 1.3)
        for k in range(6):
            u = k / 6
            a = a0 + (a1 - a0) * u
            g = 1 + amp * math.sin(math.pi * u)
            y = cy + ry * g * math.sin(a)
            if flat_bottom and math.sin(a) > 0.3:
                y = cy + ry * 0.3 + (y - cy - ry * 0.3) * 0.25
            pts.append((cx + rx * g * math.cos(a), y))
    return pts


def wob(pts, amt, seed, step=36.0):
    """Long edges broken into short runs, each point nudged: a hand-drawn edge, the same every frame."""
    r = random.Random(seed)
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        for i in range(n):
            u = i / n
            out.append((x0 + (x1 - x0) * u + r.uniform(-amt, amt), y0 + (y1 - y0) * u + r.uniform(-amt, amt)))
    return out


def quad(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def leaf_marks(p, cx, cy, rx, ry, col, seed, n=10, size=22, lw=1.8):
    """A few leaf strokes inside a clump: small cupped arcs, darker, so the mass reads as leaves."""
    r = random.Random(seed)
    for _ in range(n):
        a, rr = r.uniform(0, 2 * math.pi), r.uniform(0.1, 0.8)
        x, y = cx + rx * rr * math.cos(a), cy + ry * rr * math.sin(a)
        sz = size * r.uniform(0.7, 1.2)
        p.line(open_curve([(x - sz, y - sz * 0.3), (x, y + sz * 0.25), (x + sz, y - sz * 0.3)], 4), col, lw)


def clump(p, cx, cy, rx, ry, col, seed, marks=True, lw=3.0, n=12, bump=0.16, shade=True):
    """A canopy or bush: the scalloped mass, a darker lower half (light from above), leaf strokes."""
    pts = blob(cx, cy, rx, ry, n, bump, seed)
    p.poly(pts, col, INK, lw)
    if shade:
        lo = [q for q in blob(cx, cy + ry * 0.35, rx * 0.92, ry * 0.62, n, bump, seed + 7)]
        p.poly(lo, dk(col, 0.84), None)
    if marks:
        leaf_marks(p, cx, cy, rx, ry, dk(col, 0.7), seed, n=max(4, int(rx * ry / 3000)), size=max(8, rx * 0.12))
    p.poly(pts, None, INK, lw)


def glow(img, cam, x, y, r, col, a=0.55):
    """A soft light pool (lanterns, the bell flower, the gun flash) blended over the painting."""
    lay = Image.new('RGBA', img.size, col + (0,))
    d = ImageDraw.Draw(lay)
    X, Y = cam.P(x, y)
    R = cam.S(r)
    d.ellipse([X - R, Y - R, X + R, Y + R], fill=col + (int(255 * a),))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(R * 0.45)))


SHADOW_W = {'link': 0.55, 'zelda': 0.55, 'malon': 0.55, 'ruto': 0.55, 'saria': 0.55, 'gunman': 0.75, 'kg': 0.6,
            'goron': 1.1}      # metres across each character's foot shadow (Sam, 11 Nov Q3)


def foot_shadow(img, cam, x, y, ppm, w=0.55, a=0.46, flat=0.24, lift=0.0, clip=None, col=(24, 30, 18)):
    """Sam's soft shadow under a character's feet (11 Nov Q3): a blurred dark oval on the ground at (x, y), w metres
    across; lift (m off the ground: a jump, the slam) shrinks and fades it; clip (a polygon) keeps it on a branch."""
    k = 1.0 / (1.0 + 0.9 * max(0.0, lift))
    lay = Image.new('RGBA', img.size, col + (0,))
    d = ImageDraw.Draw(lay)
    X, Y = cam.P(x, y)
    rx = cam.S(w * ppm * 0.5 * k)
    ry = rx * flat
    d.ellipse([X - rx, Y - ry, X + rx, Y + ry], fill=col + (int(255 * a * k),))
    lay = lay.filter(ImageFilter.GaussianBlur(max(1.0, ry * 0.55)))
    if clip is not None:
        m = Image.new('L', img.size, 0)
        ImageDraw.Draw(m).polygon([cam.P(*q) for q in clip], fill=255)
        lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay)[..., 3], np.asarray(m))))
    img.alpha_composite(lay)


def shafts(img, cam, rays, col=(255, 248, 210), a=0.16):
    """Misty light shafts (ref 19, 20): soft translucent bands, no outline."""
    lay = Image.new('RGBA', img.size, col + (0,))
    d = ImageDraw.Draw(lay)
    for pts in rays:
        d.polygon([cam.P(*q) for q in pts], fill=col + (int(255 * a),))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(cam.S(18))))


def haze(img, cam, y0, y1, col, a):
    """A flat band of mist over everything behind (distance)."""
    lay = Image.new('RGBA', img.size, col + (0,))
    d = ImageDraw.Draw(lay)
    d.rectangle([0, cam.P(0, y0)[1], img.size[0], cam.P(0, y1)[1]], fill=col + (int(255 * a),))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(cam.S(40))))


def flower(p, x, y, r, petal, centre=(250, 210, 80), n=5, rot=0.0):
    for k in range(n):
        a = rot + 2 * math.pi * k / n
        p.ell(x + r * 0.62 * math.cos(a), y + r * 0.62 * math.sin(a) * 0.8, r * 0.5, r * 0.4, petal, INK, 1.6, rot=a)
    p.ell(x, y, r * 0.28, r * 0.24, centre, INK, 1.4)


def tuft(p, x, y, h, col, seed, n=5, lw=2.0):
    """A grass tuft: a fan of thin blades."""
    r = random.Random(seed)
    for k in range(n):
        a = -math.pi / 2 + (k - (n - 1) / 2) * 0.28 + r.uniform(-0.1, 0.1)
        hh = h * r.uniform(0.7, 1.1)
        p.line(open_curve([(x, y), (x + math.cos(a) * hh * 0.5, y + math.sin(a) * hh * 0.5),
                           (x + math.cos(a + 0.2) * hh, y + math.sin(a) * hh)], 3), col, lw)


def ribbon(pts, w0, w1):
    """A tapering band along a line (roots, branches, stems, trunks)."""
    pts = [np.asarray(q, float) for q in pts]
    L, R = [], []
    for i, q in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        t = b - a
        t = t / (np.linalg.norm(t) + 1e-9)
        nx, ny = -t[1], t[0]
        w = w0 + (w1 - w0) * i / max(1, len(pts) - 1)
        L.append((q[0] + nx * w / 2, q[1] + ny * w / 2))
        R.append((q[0] - nx * w / 2, q[1] - ny * w / 2))
    return L + R[::-1]


def bark(p, pts, w0, w1, col, seed, moss=None, lines=4):
    """A trunk or branch: the tapering band, bark lines along it, moss on its top side."""
    path = open_curve(pts, 6)
    p.poly(ribbon(path, w0, w1), col, INK, 3.2)
    r = random.Random(seed)
    for k in range(lines):
        off = (k + 0.5) / lines - 0.5
        seg = []
        for i, q in enumerate(path):
            if i == 0 or i == len(path) - 1:
                continue
            a, b = np.asarray(path[i - 1]), np.asarray(path[i + 1])
            t = (b - a) / (np.linalg.norm(b - a) + 1e-9)
            w = w0 + (w1 - w0) * i / (len(path) - 1)
            seg.append((q[0] - t[1] * w * off * 0.8, q[1] + t[0] * w * off * 0.8))
        i0 = r.randint(0, max(0, len(seg) // 3))
        i1 = r.randint(len(seg) * 2 // 3, len(seg))
        if i1 - i0 > 2:
            p.line(seg[i0:i1], dk(col, 0.7), 1.8)
    if moss and abs(pts[-1][1] - pts[0][1]) > 1.5 * abs(pts[-1][0] - pts[0][0]):   # a trunk: moss in patches (pass 2:
        moss_patches(p, path, w0, w1, moss, seed)                              # a band up it read as tape)
    elif moss:
        top = []
        for i, q in enumerate(path):
            a, b = np.asarray(path[max(0, i - 1)]), np.asarray(path[min(len(path) - 1, i + 1)])
            t = (b - a) / (np.linalg.norm(b - a) + 1e-9)
            w = w0 + (w1 - w0) * i / (len(path) - 1)
            nx, ny = -t[1], t[0]
            if ny > 0:
                nx, ny = -nx, -ny
            top.append((q[0] + nx * w * 0.5, q[1] + ny * w * 0.5))
        under = [(x, y + 18 + 8 * math.sin(i * 1.7)) for i, (x, y) in enumerate(top)]
        bumps = [(x, y - 10 - 8 * abs(math.sin(i * 1.3))) for i, (x, y) in enumerate(top)]
        p.poly(bumps + under[::-1], moss, INK, 2.2)


def moss_patches(p, path, w0, w1, moss, seed):
    """Moss on a standing trunk: soft irregular clumps hugging one side, thickest at the foot, a few strands hanging
    from each (pass 2: one long ruled band read as tape)."""
    r = random.Random(seed + 500)
    n = len(path)
    lo = 0 if path[0][1] > path[-1][1] else n - 1                       # the foot: the lowest end
    side = r.choice((-1, 1))
    us = (0.06, 0.2, 0.42, 0.66) if w0 >= 140 else (0.05,)              # a thin trunk: only at its foot (pass 3
    for k, u in enumerate(us):                                          # check: spaced lumps read as cotton balls)
        i = int(round(lo + (u if lo == 0 else -u) * (n - 1)))
        i = min(n - 1, max(0, i))
        q = path[i]
        w = w0 + (w1 - w0) * i / (n - 1)
        size = (1.0 - 0.75 * u) * r.uniform(0.75, 1.1)
        sg = side if k % 2 == 0 else -side                                # hugging an edge, over its outline
        cx = q[0] + sg * w * 0.44
        rx, ry = w * 0.16 * size + 6, w * 0.38 * size + 10
        p.poly(blob(cx, q[1], rx, ry, 9, 0.28, seed + 510 + k), moss, INK, 2.0)
        p.poly(blob(cx - rx * 0.15, q[1] - ry * 0.25, rx * 0.55, ry * 0.4, 7, 0.25, seed + 520 + k),
               mix(moss, (230, 236, 160), 0.15), None)                  # its lit top
        for j in range(2):                                              # strands hanging from it
            x0 = cx + rx * r.uniform(-0.6, 0.6)
            y0 = q[1] + ry * 0.7
            p.poly(ribbon(open_curve([(x0, y0), (x0 + r.uniform(-4, 4), y0 + ry * 0.4),
                                      (x0 + r.uniform(-6, 6), y0 + ry * r.uniform(0.6, 1.0))], 4), 9, 2), moss, INK,
                   1.4)


# ================================================================================================ Kokiri Forest
SKY_HI, SKY_MID, SKY_LO = (82, 148, 222), (118, 180, 236), (172, 212, 242)
CLOUD, CLOUD_D = (252, 252, 250), (214, 226, 238)
LEAF_D, LEAF, LEAF_L, LEAF_GOLD = (52, 92, 46), (82, 128, 56), (128, 166, 72), (176, 186, 92)
TRUNK, TRUNK_D = (112, 84, 58), (84, 62, 44)
MOSS, MOSS_L = (104, 150, 60), (140, 178, 76)
STONE, STONE_D, STONE_L = (202, 196, 174), (160, 154, 134), (222, 216, 196)
GROUND, GROUND_D = (92, 132, 58), (70, 106, 46)
PURPLE, PURPLE_L = (138, 82, 186), (176, 126, 214)
BELL, BELL_L = (240, 136, 40), (255, 196, 90)
LANTERN = (255, 170, 60)
MIST = (232, 236, 206)


def _sky(p, y0, y1, seed=0):
    """Three flat bands, deep overhead to pale low, with hand-cut wavy edges."""
    p.poly(quad(-200, y0, W + 200, y1), SKY_LO, None)
    for col, yy in ((SKY_MID, y0 + (y1 - y0) * 0.55), (SKY_HI, y0 + (y1 - y0) * 0.25)):
        edge = [(x, yy + 14 * math.sin(x / 130 + seed)) for x in np.linspace(-200, W + 200, 24)]
        p.poly([(-200, y0)] + edge + [(W + 200, y0)], col, None)


def _cloud(p, x, y, w, seed):
    pts = blob(x, y, w, w * 0.36, 10, 0.3, seed, flat_bottom=True)
    p.poly(pts, CLOUD, INK, 2.2)
    p.poly(blob(x, y + w * 0.16, w * 0.8, w * 0.14, 8, 0.15, seed + 3), CLOUD_D, None)
    p.poly(pts, None, INK, 2.2)


def _door(p, x, y, r, lw=2.6):
    """The tree-house door (ref 20), standing on the stump's foot at (x, y): a dark arched doorway, a round-topped
    plank door in it, iron straps, a ring handle, a flat stone step (pass 2: a round door read as a magnifying glass)."""
    hgt = r * 3.2
    def arch(rw, top, base):
        return curve([(x - rw, base), (x - rw, top + rw), (x - rw * 0.7, top + rw * 0.3), (x, top),
                      (x + rw * 0.7, top + rw * 0.3), (x + rw, top + rw), (x + rw, base)], 4)
    p.poly(arch(r * 1.22, y - hgt - r * 0.22, y), (52, 36, 26), INK, lw)            # the dark doorway in the bark
    p.poly(arch(r, y - hgt, y), (132, 88, 52), INK, lw)                             # the door
    for k in (-0.5, 0.0, 0.5):                                                       # its planks
        p.line([(x + r * k, y - hgt + r * (0.55 if k else 0.05)), (x + r * k, y - 2)], (96, 62, 38), 2.0)
    for v in (0.28, 0.7):                                                            # iron straps
        yy = y - hgt * v
        p.line([(x - r * 0.96, yy), (x + r * 0.96, yy)], (62, 56, 54), 4.0)
    p.ell(x + r * 0.55, y - hgt * 0.45, r * 0.13, r * 0.13, None, (60, 50, 46), 2.4)  # the ring
    p.poly(wob(quad(x - r * 1.5, y - r * 0.06, x + r * 1.5, y + r * 0.22), 2, int(x)), STONE_D, INK, 2.0)   # the step


def _lantern(img, p, cam, x, y, r):
    """A round paper lantern hung from a crooked wooden arm pegged into the bark (pass 1: flat squares, unhung)."""
    p.line(open_curve([(x - r * 2.2, y - r * 2.6), (x - r * 1.0, y - r * 2.9), (x, y - r * 2.6)], 4), (84, 62, 44), 4.0)
    p.ell(x - r * 2.2, y - r * 2.6, r * 0.3, r * 0.3, (60, 44, 34), INK, 1.4)           # the peg in the bark
    p.line([(x, y - r * 2.6), (x, y - r * 1.2)], INK, 1.8)
    p.poly([(x - r * 0.45, y - r * 1.25), (x + r * 0.45, y - r * 1.25), (x + r * 0.4, y - r * 1.0), (x - r * 0.4, y - r * 1.0)],
           (120, 70, 40), INK, 1.4)
    p.ell(x, y - r * 0.1, r * 0.95, r * 0.9, LANTERN, INK, 2.0)
    for u in (-0.45, 0.0, 0.45):                                        # the paper ribs
        p.line(open_curve([(x + r * u * 0.6, y - r * 0.95), (x + r * u * 1.05, y - r * 0.1), (x + r * u * 0.6, y + r * 0.75)], 4),
               (214, 120, 40), 1.4)
    p.poly([(x - r * 0.4, y + r * 0.75), (x + r * 0.4, y + r * 0.75), (x + r * 0.3, y + r * 1.0), (x - r * 0.3, y + r * 1.0)],
           (120, 70, 40), INK, 1.4)
    glow(img, cam, x, y, r * 4, (255, 190, 90), 0.45)


def _stump_house(img, p, cam, x, y, w, h, seed=3, door=True):
    """The Kokiri tree house (ref 19, 20): a giant mossy stump, bark ridges, a round door, a small round window,
    orange lanterns, moss and grass on its top. (x, y) is the middle of its foot."""
    body = wob([(x - w * 0.5, y), (x - w * 0.46, y - h * 0.6), (x - w * 0.38, y - h), (x + w * 0.4, y - h),
                (x + w * 0.47, y - h * 0.55), (x + w * 0.56, y)], 6, seed)
    p.poly(body, TRUNK, INK, 3.0)
    for k in range(6):                                                  # bark ridges
        u = (k + 0.5) / 6
        xx = x - w * 0.45 + w * 0.9 * u
        p.line(open_curve([(xx, y - h * 0.96), (xx + 8 * math.sin(k), y - h * 0.5), (xx - 6, y - 6)], 4), TRUNK_D, 2.0)
    for k, (rx, dx_, dy_) in enumerate(((-0.42, -0.34, 0.05), (-0.18, -0.12, 0.08), (0.22, 0.1, 0.07), (0.5, 0.3, 0.04))):
        bark(p, [(x + w * rx, y - h * 0.16), (x + w * (rx + dx_ * 0.5), y - h * 0.02), (x + w * (rx + dx_), y + h * dy_)],
             w * 0.13, w * 0.04, TRUNK, seed + 40 + k, None, 2)        # gnarled roots spreading at the foot
    for kx, ky, kr in ((0.3, 0.75, 0.05), (-0.36, 0.38, 0.04)):         # knots in the bark
        p.ell(x + w * kx, y - h * ky, w * kr, w * kr * 1.4, TRUNK_D, INK, 2.0)
        p.ell(x + w * kx, y - h * ky, w * kr * 0.45, w * kr * 0.7, (60, 44, 34), None)
    rr = random.Random(seed + 9)
    for k in range(7):                                                  # moss hanging down from the cap, joined to it
        xx = x - w * 0.36 + w * 0.12 * k + rr.uniform(-8, 8)
        drop = h * rr.uniform(0.1, 0.26) * (1.4 if k in (1, 5) else 1.0)
        p.poly(ribbon(open_curve([(xx, y - h * 1.0), (xx + rr.uniform(-6, 6), y - h + drop * 0.5),
                                  (xx + rr.uniform(-10, 10), y - h + drop)], 5), w * 0.07, w * 0.012), MOSS, INK, 1.8)
    p.poly(blob(x, y - h, w * 0.5, h * 0.09, 14, 0.25, seed + 1), MOSS, INK, 2.6)   # moss cap
    for k in range(5):
        tuft(p, x - w * 0.4 + w * 0.2 * k, y - h * 1.03, h * 0.08, LEAF_D, seed + k)
    for rx_, rw in ((-0.42, 0.16), (0.3, 0.2)):                         # moss mounded on the roots at the foot
        p.poly(blob(x + w * rx_, y - h * 0.02, w * rw, h * 0.05, 10, 0.2, seed + 20 + int(rw * 50), flat_bottom=True),
               MOSS, INK, 2.0)
    if door:
        _door(p, x + w * 0.05, y - h * 0.01, w * 0.12)
        wx_, wy_, ww_ = x - w * 0.24, y - h * 0.62, w * 0.07                # an arched window, lamp-lit, barred
        arch = curve([(wx_ - ww_, wy_ + ww_ * 1.1), (wx_ - ww_, wy_ - ww_ * 0.4), (wx_, wy_ - ww_ * 1.2),
                      (wx_ + ww_, wy_ - ww_ * 0.4), (wx_ + ww_, wy_ + ww_ * 1.1)], 3)
        p.poly(arch, (255, 196, 110), INK, 2.4)
        p.line([(wx_, wy_ - ww_ * 1.2), (wx_, wy_ + ww_ * 1.1)], (84, 62, 44), 3.0)
        p.line([(wx_ - ww_, wy_ + ww_ * 0.1), (wx_ + ww_, wy_ + ww_ * 0.1)], (84, 62, 44), 3.0)
        p.poly(quad(wx_ - ww_ * 1.25, wy_ + ww_ * 1.1, wx_ + ww_ * 1.25, wy_ + ww_ * 1.35), (84, 62, 44), INK, 1.8)   # the sill
        _lantern(img, p, cam, x + w * 0.32, y - h * 0.46, w * 0.04)
        _lantern(img, p, cam, x - w * 0.18, y - h * 0.3, w * 0.035)


def _bell_flower(img, p, cam, x, y, r):
    """The big glowing orange bell flower (ref 20): a tall stem arching over like a crook, the bell hanging from its
    tip mouth down, flared and scalloped, glowing from inside; long leaves at its foot (pass 2: it read as a paddle).
    (x, y) is the bell's middle."""
    base = (x - r * 1.3, y + r * 3.4)
    stem = open_curve([base, (x - r * 1.5, y + r * 1.2), (x - r * 1.1, y - r * 1.5), (x - r * 0.2, y - r * 1.9),
                       (x + r * 0.15, y - r * 1.0)], 8)
    for sg, ln in ((-1, 1.9), (1, 1.5)):                                 # long leaves at its foot
        tip = (base[0] + sg * r * ln, base[1] - r * 1.3)
        p.poly(curve([base, (base[0] + sg * r * ln * 0.5, base[1] - r * 1.15), tip,
                      (base[0] + sg * r * ln * 0.45, base[1] - r * 0.45)], 4), LEAF_L if sg > 0 else LEAF, INK, 2.0)
    p.poly(ribbon(stem, r * 0.2, r * 0.11), LEAF, INK, 2.0)
    glow(img, cam, x, y + r * 0.5, r * 2.6, (255, 170, 60), 0.55)
    top = (x + r * 0.15, y - r * 1.0)
    mouth = []
    for k in range(11):                                                  # the flared, scalloped mouth
        u = k / 10
        mouth.append((x - r * 1.05 + r * 2.3 * u, y + r * (0.95 + (0.22 if k % 2 else 0.0))))
    bell = curve([top, (x + r * 0.7, y - r * 0.7), (x + r * 0.8, y + r * 0.3), (x + r * 1.25, y + r * 0.95)], 4) + \
        mouth[::-1] + curve([(x - r * 1.05, y + r * 0.95), (x - r * 0.55, y + r * 0.3), (x - r * 0.4, y - r * 0.7),
                             top], 4)
    p.poly(bell, BELL, INK, 2.4)
    p.poly(curve([(x - r * 0.15, y - r * 0.7), (x + r * 0.3, y - r * 0.55), (x + r * 0.4, y + r * 0.5),
                  (x - r * 0.1, y + r * 0.6)], 3), BELL_L, None)        # its lit side
    p.ell(x + r * 0.1, y + r * 1.0, r * 0.95, r * 0.2, (255, 226, 150), INK, 1.8)   # the glowing inside of the mouth
    p.line(open_curve([(x + r * 0.1, y + r * 0.95), (x + r * 0.2, y + r * 1.35), (x + r * 0.1, y + r * 1.6)], 3),
           (200, 110, 30), 2.4)                                         # the stamen hanging out
    p.ell(x + r * 0.1, y + r * 1.62, r * 0.1, r * 0.1, (255, 220, 120), INK, 1.2)
    p.ell(x + r * 0.15, y - r * 1.0, r * 0.18, r * 0.12, LEAF_D, INK, 1.6)   # the green cap where it hangs


def _purple_patch(p, x, y, r, seed, n=7):
    rr = random.Random(seed)
    for k in range(n):
        lx, ly = x + rr.uniform(-1, 1) * r, y + rr.uniform(-0.5, 0.5) * r
        p.poly(curve([(lx, ly + r * 0.3), (lx - r * 0.4, ly), (lx, ly - r * 0.12), (lx + r * 0.4, ly)], 3), LEAF,
               INK, 1.6)
    for k in range(n):
        flower(p, x + rr.uniform(-1, 1) * r * 0.9, y + rr.uniform(-0.5, 0.4) * r, r * rr.uniform(0.22, 0.32),
               PURPLE if k % 2 else PURPLE_L, rot=rr.uniform(0, 1))


def _rock(p, x, y, w, h, seed, moss=True):
    pts = wob(curve([(x - w, y), (x - w * 0.8, y - h * 0.7), (x - w * 0.1, y - h), (x + w * 0.7, y - h * 0.8),
                     (x + w, y)], 3), w * 0.04, seed, 20)
    p.poly(pts, (150, 150, 140), INK, 2.4)
    p.poly([(x + w * 0.2, y), (x + w * 0.7, y - h * 0.6), (x + w, y)], (122, 122, 116), None)
    if moss:
        p.poly(blob(x - w * 0.2, y - h * 0.85, w * 0.6, h * 0.25, 9, 0.3, seed), MOSS, INK, 1.8)
    p.poly(pts, None, INK, 2.4)


def forest_up(img, p, cam, t):
    """S1 and S3: low under the branch, looking up (ref 01): blue sky and white clouds, the canopy round the top,
    the great trunk on the left, the mossy branch across to KG's perch, hazy lower trees at the foot."""
    _sky(p, -400, 1500, 0.6)
    for x, y, w, sd in ((760, 380, 230, 1), (240, 640, 160, 2), (900, 900, 200, 3), (520, 1120, 150, 4)):
        _cloud(p, x + 6 * math.sin(t * 0.3 + sd), y, w, sd)
    for x, y, rx, ry, sd in ((-40, 1500, 340, 260, 5), (300, 1560, 300, 200, 6), (640, 1520, 320, 220, 7),
                             (1000, 1480, 320, 260, 8)):                # the far trees, low and hazy
        p.poly(blob(x, y, rx, ry, 12, 0.18, sd), mix(LEAF_L, SKY_LO, 0.45), INK, 2.4)
    bark(p, [(1200, 2000), (1110, 900), (1000, -200)], 120, 50, mix(TRUNK, (150, 170, 150), 0.4), 29, None, 2)
    # (a far trunk leaning in to the top, pass 2: S1 read level)
    # the foot (first look: a flat sage block): treetops in rows, each nearer one greener and darker, a light shaft
    p.poly(quad(-200, 1700, W + 200, 2400), mix(LEAF, SKY_LO, 0.3), None)
    for k, x in enumerate((-60, 250, 560, 860, 1160)):                  # the middle row, a little hazy
        clump(p, x, 1700 + 50 * (k % 2), 210, 170, mix(LEAF_L, SKY_LO, 0.25), 30 + k, lw=2.6)
    shafts(img, cam, [[(560, 1300), (700, 1300), (900, 2000), (640, 2000)]], a=0.14)
    for k, x in enumerate((60, 420, 780, 1120)):                         # the near row, the nearest leaves
        clump(p, x, 1880 + 40 * (k % 2), 250, 190, LEAF if k % 2 else mix(LEAF, LEAF_L, 0.4), 36 + k)
    for x, y, rx, ry, c, sd in ((-80, 60, 420, 260, LEAF_D, 11), (330, -60, 360, 200, LEAF, 12),
                                (980, -40, 400, 260, LEAF_D, 13), (1160, 300, 220, 260, LEAF, 14),
                                (160, 210, 300, 170, LEAF, 15), (720, 90, 260, 150, LEAF_L, 16)):   # the canopy
        clump(p, x, y, rx, ry, c, sd)
    haze(img, cam, 1350, 1700, (236, 240, 236), 0.5)                    # mist among the far trees (ref 19)
    for pts, w0, sd in (([(110, 600), (260, 380), (420, 240)], 90, 26), ([(90, 360), (40, 160), (-20, 60)], 80, 27),
                        ([(120, 900), (420, 760), (700, 640), (980, 520)], 70, 28)):   # boughs up into the canopy
        bark(p, pts, w0, w0 * 0.35, TRUNK, sd, MOSS, 2)
    for x, y, rx, ry, c, sd in ((430, 240, 220, 140, LEAF, 17), (1000, 520, 200, 150, LEAF_D, 18)):
        clump(p, x, y, rx, ry, c, sd)
    branch = BRANCH_UP
    bark(p, [(940, BRANCH_UP[-1][1] - 18), (1010, BRANCH_UP[-1][1] - 90), (1060, BRANCH_UP[-1][1] - 140)], 40, 18, TRUNK, 23)
    bark(p, [(40, BRANCH_UP[0][1] + 30)] + branch, 170, 60, TRUNK, 22, MOSS, 4)   # the branch, its root inside the trunk
    _branch_under(p)
    p.ell(branch[-1][0] + 4, branch[-1][1], 30, 34, TRUNK_D, INK, 2.4)         # its broken end, not a squared plank
    p.ell(branch[-1][0] + 4, branch[-1][1], 16, 20, (150, 118, 84), None)
    clump(p, 1060, BRANCH_UP[-1][1] - 170, 120, 90, LEAF, 24)
    clump(p, 990, BRANCH_UP[-1][1] - 60, 70, 50, LEAF_L, 25)
    # the trunk (pass 2: it stood level): wide at the foot and leaning in as it climbs, as looking up makes it
    bark(p, [(10, 2100), (90, 1500), (170, 900), (240, 300), (300, -200)], 400, 140, TRUNK, 21, MOSS, 6)
    for k, x in enumerate((330, 470, 860)):                             # moss hanging under the branch
        y = branch_y(x) + 60
        p.poly(ribbon(open_curve([(x, y - 10), (x + 6, y + 50), (x - 4, y + 100 + 20 * k)], 5), 22, 4), MOSS_L, INK,
               1.6)


BRANCH_UP = [(150, 960), (420, 900), (700, 840), (940, 760)]    # pass 1: higher, so KG towers over the lens


def _branch_under(p):
    """The branch's underside, seen from below (pass 2: S1 read level): its lower half in shadow, and bark rings."""
    path = open_curve([(40, BRANCH_UP[0][1] + 30)] + BRANCH_UP, 6)
    n = len(path)
    lo = []
    for i, q in enumerate(path):
        a, b = np.asarray(path[max(0, i - 1)]), np.asarray(path[min(n - 1, i + 1)])
        t_ = (b - a) / (np.linalg.norm(b - a) + 1e-9)
        w = 170 + (60 - 170) * i / (n - 1)
        nx, ny = -t_[1], t_[0]
        if ny < 0:
            nx, ny = -nx, -ny
        lo.append(((q[0] + nx * w * 0.5, q[1] + ny * w * 0.5), (q[0] - nx * w * 0.05, q[1] - ny * w * 0.05)))
    i0 = n // 6
    p.poly([e for e, _ in lo[i0:]] + [m for _, m in lo[i0:]][::-1], TRUNK_D, None)
    for i in range(i0 + 2, n - 2, 4):                                    # rings round the underside
        (ex, ey), (mx, my) = lo[i]
        p.line(open_curve([(mx, my), ((ex + mx) / 2 + 6, (ey + my) / 2 + 4), (ex, ey)], 3), dk(TRUNK_D, 0.75), 1.6)
    p.poly(ribbon(path, 170, 60), None, INK, 3.2)


def kg_on_branch(img, cam, x, s, mood='hype', wings='wide', t=0.0, **kw):
    """KG perched on the S1/S3 branch (pass 2: his talons floated in front of it): his tail hangs BEHIND the branch,
    the branch is laid back over it, then his body sits on top with the toes curling over its front edge."""
    import remakes_creatures as CR
    y = branch_y(x) - 236 * s - 4 * s                                    # his toe roots on the branch's top
    before = img.copy()
    CR.kg(img, cam, x, y, s, view='front', perched=True, wings=wings, mood=mood, t=t, part='tail', **kw)
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).polygon([cam.P(*q) for q in branch_poly()], fill=255)
    img.paste(before, (0, 0), m)
    foot_shadow(img, cam, x, branch_y(x) + 14, 420.0, SHADOW_W['kg'], clip=branch_poly())
    CR.kg(img, cam, x, y, s, view='front', perched=True, wings=wings, mood=mood, t=t, part='body', **kw)


def branch_poly():
    """The S1 branch's outline (the shadow under KG's talons stays on it)."""
    return ribbon(open_curve([(40, BRANCH_UP[0][1] + 30)] + BRANCH_UP, 6), 170, 60)


def branch_y(x):
    """The top of the branch at screen x (S1), for KG's feet."""
    xs = [q[0] for q in BRANCH_UP]
    ys = [q[1] for q in BRANCH_UP]
    w = 170 + (60 - 170) * (x + 40 - 40) / (940 - 40)
    return float(np.interp(x, xs, ys)) - w * 0.5


DOWN = dict(top=640, ppm0=150.0, k=0.32)       # S2: the ground row at the top and how fast pixels per metre grow


def down_ppm(y):
    return DOWN['ppm0'] + (y - DOWN['top']) * DOWN['k']


def _path_x(y):
    """The path's middle: winding, and at the top bending right to the tree house door (pass 1: it hit its side)."""
    return 560 + 110 * math.sin((y - 640) / 380.0) + 400 * max(0.0, (900 - y) / 300.0) ** 1.5


STUMP_DOWN = (820, 700, 520, 520)     # S2's tree house: the middle of its foot, width, height (px)
STUMP_SEED = 34                        # S4/S6 draw the same stump (pass 2: they differed)
PATH_TOP = 688                         # the path starts at the door's foot


def _path_w(y):
    return 0.5 * 1.6 * down_ppm(y) + 30          # about 1.6 m wide


def forest_down(img, p, cam, t):
    """S2, from KG's branch: the forest floor (ref 20): a pale stone path winding back, moss and roots either side,
    rocks, purple flowers in the near corner, the glowing bell flower, the foot of the tree house at the top."""
    p.poly(quad(-200, -400, W + 200, 2400), GROUND, None)
    rr = random.Random(5)
    for k in range(18):                                                 # darker moss patches
        y = rr.uniform(500, 1900)
        x = rr.choice([rr.uniform(-60, 300), rr.uniform(780, 1140)])
        p.poly(blob(x, y, down_ppm(y) * 0.5, down_ppm(y) * 0.2, 9, 0.25, k), GROUND_D, None)
    # the top: the base of the tree house and the tall trees behind
    clump(p, 200, 220, 360, 300, LEAF_D, 31)
    clump(p, 820, 180, 380, 260, LEAF, 32)
    bark(p, [(160, 760), (170, 300), (190, -200)], 190, 150, TRUNK, 33, MOSS, 5)
    # the path: a winding band from the door's foot (pass 2: it climbed the stump like stairs), then its stones in
    # rows that grow nearer the lens
    ys = np.linspace(PATH_TOP, 2000, 40)
    left = [(_path_x(y) - _path_w(y), y) for y in ys]
    right = [(_path_x(y) + _path_w(y), y) for y in ys[::-1]]
    p.poly(left + right, mix(STONE_D, GROUND_D, 0.3), INK, 2.6)
    y = PATH_TOP + 4
    row = 0
    while y < 2000:
        hgt = down_ppm(y) * 0.32
        x0, x1 = _path_x(y + hgt / 2) - _path_w(y), _path_x(y + hgt / 2) + _path_w(y)
        x = x0 + (row % 2) * hgt * 0.6
        while x < x1:
            sw = hgt * rr.uniform(1.2, 1.9)
            xa, xb = max(x, x0 + 4), min(x + sw, x1 - 4)
            if xb - xa > hgt * 0.4:
                st = wob(quad(xa + 3, y + 3, xb - 3, y + hgt - 3), hgt * 0.05, row * 31 + int(x), 18)
                c_ = mix(STONE, STONE_L, rr.uniform(0, 1)) if rr.random() > 0.3 else STONE
                p.poly(st, mix(c_, MOSS, 0.22), INK, 1.8)                # toned into the moss: Link, not the path, leads
            x += sw
        y += hgt
        row += 1
    _stump_house(img, p, cam, *STUMP_DOWN, seed=STUMP_SEED)          # over the path's far end: it ends at the door
    # roots crossing from the sides, rocks, tufts
    bark(p, [(-80, 1500), (120, 1460), (280, 1520), (360, 1600)], 90, 40, TRUNK, 41, MOSS, 3)
    bark(p, [(1180, 1180), (1000, 1150), (880, 1210)], 80, 34, TRUNK, 42, MOSS, 3)
    _rock(p, 150, 1180, 120, 110, 43)
    _rock(p, 990, 1600, 150, 120, 44)
    for k in range(40):                                                 # grass and moss texture (pass 1: a flat fill)
        y = rr.uniform(560, 1900)
        x = rr.choice([rr.uniform(-20, _path_x(y) - _path_w(y)), rr.uniform(_path_x(y) + _path_w(y), 1100)])
        tuft(p, x, y, down_ppm(y) * 0.16, LEAF_D if k % 3 else MOSS_L, k + 60)
    for k in range(30):
        y = rr.uniform(600, 1900)
        x = rr.choice([rr.uniform(-20, _path_x(y) - _path_w(y)), rr.uniform(_path_x(y) + _path_w(y), 1100)])
        p.ell(x, y, down_ppm(y) * 0.05, down_ppm(y) * 0.025, rr.choice([(196, 150, 60), (176, 104, 46), (120, 140, 50)]),
              None, rot=rr.uniform(0, 3))
    for k in range(10):                                                 # fallen leaves on the path and moss
        y = rr.uniform(800, 1880)
        x = _path_x(y) + rr.uniform(-1, 1) * _path_w(y)
        p.ell(x, y, down_ppm(y) * 0.05, down_ppm(y) * 0.025, rr.choice([(196, 150, 60), (176, 104, 46)]), INK, 1.2,
              rot=rr.uniform(0, 3))
    _bell_flower(img, p, cam, 960, 1300, 60)
    _purple_patch(p, 140, 1800, 170, 47, 9)
    shafts(img, cam, [[(300, -200), (520, -200), (760, 2000), (420, 2000)], [(760, -200), (860, -200), (1100, 1400),
                                                                              (980, 1400)]], a=0.14)
    for k in range(8):                                                  # dappled light on the ground
        y = rr.uniform(900, 1850)
        x = rr.uniform(200, 900)
        lay_spot(img, cam, x, y, down_ppm(y) * 0.3, down_ppm(y) * 0.12)


def lay_spot(img, cam, x, y, rx, ry, col=(250, 240, 180), a=0.22):
    lay = Image.new('RGBA', img.size, col + (0,))
    d = ImageDraw.Draw(lay)
    X, Y = cam.P(x, y)
    d.ellipse([X - cam.S(rx), Y - cam.S(ry), X + cam.S(rx), Y + cam.S(ry)], fill=col + (int(255 * a),))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(cam.S(6))))


def forest_close(img, p, cam, t):
    """S4 and S6, behind Link's close-ups at his eye height (ref 19, 20): layered forest depth in soft green-gold,
    misty far trees, the tree house behind on the right with its lanterns, light shafts, the path, near plants."""
    p.poly(quad(-200, -400, W + 200, 2400), MIST, None)
    for k, (x, rx) in enumerate(((60, 300), (430, 260), (800, 320), (1120, 240))):      # far misty canopy
        p.poly(blob(x, 300 + 40 * (k % 2), rx, 260, 12, 0.18, 70 + k), mix(LEAF_L, MIST, 0.55), INK, 2.0)
    for x, w in ((140, 70), (520, 56), (930, 80)):                         # far trunks
        p.poly(wob(quad(x - w / 2, 300, x + w / 2, 1300), 3, int(x)), mix(TRUNK, MIST, 0.55), INK, 2.0)
    p.poly(quad(-200, 1180, W + 200, 2400), mix(GROUND, MIST, 0.4), None)
    for k, (x, rx) in enumerate(((-60, 280), (330, 240), (1100, 260))):  # mid canopy
        clump(p, x, 140, rx, 220, mix(LEAF, MIST, 0.2), 80 + k)
    haze(img, cam, 200, 1250, MIST, 0.35)                                # mist between the far and mid layers
    for x, w in ((760, 60), (1010, 74)):                                  # two nearer trunks, darker, behind the
        bark(p, [(x, 1310), (x + 6, 700), (x - 4, 100)], w, w * 0.85, mix(TRUNK, MIST, 0.4), 70 + x, None, 2)  # shafts
    for x, w in ((60, 150), (330, 110)):                                 # mid trunks
        bark(p, [(x, 1400), (x + 10, 700), (x - 6, 100)], w, w * 0.8, mix(TRUNK, MIST, 0.25), 90 + int(x), None, 3)
    edge = [(x, 1300 + 14 * math.sin(x * 0.031) + 8 * math.sin(x * 0.11)) for x in range(-200, W + 240, 40)]
    p.poly(edge + [(W + 200, 2400), (-200, 2400)], GROUND, None)       # the grass's far edge rolls (pass 2: ruled)
    for k, x in enumerate(range(-60, W + 80, 95)):                       # low ferns and bushes along it
        if 520 < x < 1180:
            continue                                                    # (the stump stands there)
        clump(p, x, 1300 + 6 * (k % 3), 70 + 18 * (k % 2), 38, mix(GROUND, LEAF_D, 0.4), 400 + k, marks=False, lw=2.0)
    haze(img, cam, 1230, 1360, MIST, 0.55)                               # mist lying on the ground (ref 19)
    def pl(y):                                    # the path's edges at row y: from under the door, widening to
        u = ((y - 1300) / 700.0) ** 0.8           # the lens and curving left under Link (pass 2: it led nowhere)
        return 818 + (180 - 818) * u, 930 + (820 - 930) * u
    ys = np.linspace(1300, 2000, 16)
    p.poly([(pl(y)[0], y) for y in ys] + [(pl(y)[1], y) for y in ys[::-1]], mix(STONE, MOSS, 0.22), INK, 2.0)
    yy, row = 1306.0, 0
    while yy < 2000:                                                     # flagstones as in S2
        hh = 14 + (yy - 1300) * 0.14
        xa, xb = pl(yy)
        p.line([(xa, yy), (xb, yy)], STONE_D, 1.6)
        n_ = 2 + row % 2
        for k in range(1, n_ + 1):
            xx = xa + (xb - xa) * (k - 0.5 * (row % 2)) / (n_ + 0.5)
            p.line([(xx, yy), (xx, yy + hh)], STONE_D, 1.6)
        yy += hh
        row += 1
    _stump_house(img, p, cam, 840, 1310, 620, 620, seed=STUMP_SEED)   # S2's stump, nearer (pass 2: it differed); on
    rr = random.Random(96)                                               # the grass, the path running to its door
    for k in range(26):
        y = rr.uniform(1320, 1900)
        x = rr.choice([rr.uniform(-20, pl(y)[0] - 10), rr.uniform(pl(y)[1] + 10, 1120)])
        tuft(p, x, y, 20 + (y - 1300) * 0.08, LEAF_D if k % 2 else MOSS_L, k + 300)
    shafts(img, cam, [[(160, -200), (330, -200), (640, 1700), (380, 1700)], [(560, -200), (650, -200), (990, 1500),
                                                                             (880, 1500)]], col=(255, 244, 190), a=0.34)
    clump(p, -40, 1750, 300, 220, LEAF_D, 97)
    clump(p, 1120, 1840, 260, 180, LEAF, 98)
    _bell_flower(img, p, cam, 950, 1560, 46)     # pass 2: its glow showed but the flower hid behind the bush
    _purple_patch(p, 140, 1820, 160, 99, 8)


EDGE_LEAF, EDGE_LEAF_D, EDGE_SKY = (104, 124, 96), (70, 88, 66), (196, 206, 206)


def forest_edge(img, p, cam, t):
    """S5, the gunman's patch (ref 17): the same forest gone cooler and greyer where the soldiers creep: an
    overcast sky through the trees, thin dark trunks, ferns and long grass, a mossy rock."""
    p.poly(quad(-200, -400, W + 200, 2400), EDGE_SKY, None)
    for k, (x, rx) in enumerate(((100, 320), (520, 300), (980, 330))):
        p.poly(blob(x, 560 + 60 * (k % 2), rx, 300, 12, 0.2, 110 + k), mix(EDGE_LEAF, EDGE_SKY, 0.4), INK, 2.0)
    EDGE_TRUNK = mix(TRUNK, EDGE_SKY, 0.25)                             # pass 1: the forest's own bark, gone grey
    p.poly(quad(-200, 1300, W + 200, 2400), (110, 124, 92), None)
    # gnarled trunks at staggered depths (pass 2: all in one row): far ones thin, pale and footed high, near ones
    # thick, darker, footed low; the far ones first
    for x, w, lean, foot, fade in ((470, 40, 8, 1330, 0.55), (760, 46, -10, 1345, 0.5), (180, 52, 12, 1360, 0.45),
                                   (980, 60, -14, 1380, 0.35), (620, 74, 10, 1420, 0.22), (300, 92, -20, 1470, 0.12),
                                   (40, 130, 30, 1560, 0.0), (1040, 120, -26, 1540, 0.0)):
        col = mix(EDGE_TRUNK, EDGE_SKY, fade) if fade else dk(EDGE_TRUNK, 0.9)
        bark(p, [(x, foot), (x + lean * 0.5 + 12, foot - 400), (x + lean * 0.5 - 10, foot - 800), (x + lean, 200)],
             w, w * 0.6, col, 120 + x, mix(MOSS, EDGE_SKY, 0.3 + fade), 4)
        p.ell(x + lean * 0.4, foot - 500, w * 0.18, w * 0.26, dk(col, 0.7), INK, 1.8)   # a knot
        for k in range(2):                                              # bare side branches (ref 17)
            y = 500 + 260 * k
            sg = 1 if (x + k) % 2 else -1
            p.line(open_curve([(x + lean * 0.6, y), (x + lean * 0.6 + sg * 90, y - 60), (x + sg * 150, y - 70)], 4),
                   col, max(4.0, w * 0.08))
        p.poly(blob(x, foot + 8, w * 0.9, 18 + w * 0.12, 9, 0.3, 170 + x), mix((96, 112, 80), EDGE_SKY, fade * 0.6),
               None)                                                    # the grass round its foot
    for k, (x, rx) in enumerate(((-40, 260), (420, 220), (1120, 280), (760, 200), (200, 180))):   # canopy across the sky
        clump(p, x, (260, 340, 180, 60, -20)[k], rx, 180, EDGE_LEAF if k % 2 == 0 else EDGE_LEAF_D, 130 + k)
    _rock(p, 230, 1560, 200, 160, 160)                                  # pass 1: whole, not a sliver at the edge
    rr = random.Random(141)
    # long grass, not lawn (pass 2): bands of tall arching blades, the further rows paler and shorter, back to front
    for band, (y0, y1, hmin, hmax, n) in enumerate(((1300, 1450, 50, 90, 70), (1420, 1650, 90, 170, 80),
                                                    (1600, 1950, 160, 300, 70))):
        for k in range(n):
            x, y = rr.uniform(-40, 1120), rr.uniform(y0, y1)
            hh = rr.uniform(hmin, hmax)
            c_ = rr.choice((EDGE_LEAF_D, (128, 144, 98), (104, 124, 84), (146, 156, 108)))
            c_ = mix(c_, EDGE_SKY, 0.3 - 0.15 * band)
            for b in range(rr.randint(3, 6)):
                lean_ = rr.uniform(-0.5, 0.5) * hh
                tip = (x + lean_ + rr.uniform(-8, 8), y - hh * rr.uniform(0.7, 1.0))
                mid = (x + lean_ * 0.25, y - hh * 0.55)
                p.poly(ribbon(open_curve([(x + b * 3, y), mid, tip], 5), 5 + band * 2.5, 1), c_,
                       INK if band == 2 else None, 1.0)
    for x, y, sd in ((900, 1600, 161), (240, 1820, 162), (1000, 1880, 163)):    # ferns
        for k in range(7):
            a = -math.pi / 2 + (k - 3) * 0.38
            tip = (x + math.cos(a) * 230, y + math.sin(a) * 200)
            stem = open_curve([(x, y), ((x + tip[0]) / 2, (y + tip[1]) / 2 - 30), tip], 6)
            p.poly(ribbon(stem, 34, 6), EDGE_LEAF if k % 2 else (90, 112, 80), INK, 1.8)
            p.line(stem, EDGE_LEAF_D, 1.4)


FOREST_VIEWS = {'up': forest_up, 'down': forest_down, 'close': forest_close, 'edge': forest_edge}


def forest(img, cam, view, t=0.0):
    p = B.Pen(img, cam)
    FOREST_VIEWS[view](img, p, cam, t)


def forest_front(img, cam, view, t=0.0):
    """Leaves nearest the lens, over the cast (S2's corner plants; the rest have none)."""
    p = B.Pen(img, cam)
    if view == 'down':
        clump(p, 1120, 1960, 260, 160, LEAF_D, 170)


# ================================================================================================ the camp
CAMP = Level(h=1.6, hz=860.0, f=1100.0)   # pass 1: the horizon lower, less empty yard below the action
DIRT, DIRT_D, DIRT_L = (198, 166, 116), (170, 138, 92), (218, 192, 146)
TIN, TIN_D, TIN_L = (138, 142, 144), (108, 112, 116), (166, 168, 166)
RUST = (168, 96, 52)
PLANK, PLANK_D = (150, 112, 72), (112, 82, 52)
CONT_BLUE, CONT_ORANGE = (46, 96, 150), (214, 110, 40)
SAND, SAND_D = (186, 168, 120), (150, 132, 92)
FLAG_C = (40, 80, 150)            # pass 1: blue as ref 24's, an invented white mark
WALL_D, WALL_H = 10.0, 2.6        # the back wall: depth and height (m)
GATE_HALF = 1.8                   # the gate opening's half width (m)
TOWER = (3.0, 9.0)                # the watchtower's middle (x, d), inside the wall on the right
CONTAINERS = {'blue container': (-5.0, -2.6, 7.4, 2.4), 'orange container': (-5.0, -2.6, 7.6, 2.2)}   # x0, x1, d, depth


def _tin_sheet(p, pts, col, seed, ribs=8, rust=True):
    """One corrugated sheet: the panel, its ribs, a rust streak or two."""
    p.poly(pts, col, INK, 2.2)
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
    for k in range(1, ribs):
        u = k / ribs
        p.line([(x0 + (x1 - x0) * u, y0 + (y1 - y0) * u), (x3 + (x2 - x3) * u, y3 + (y2 - y3) * u)], dk(col, 0.82), 1.4)
    if rust:
        r = random.Random(seed)
        u = r.uniform(0.15, 0.85)
        xa, ya = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        L = r.uniform(0.3, 0.7)
        p.poly([(xa - 5, ya + 4), (xa + 5, ya + 4), (xa + 2, ya + (y3 - y0) * L), (xa - 3, ya + (y3 - y0) * L)], RUST,
               None)


def _wire(p, x0, x1, y, r):
    """A coil of barbed wire along a wall top."""
    x = x0
    while x < x1:
        p.ell(x, y - r * 0.8, r, r * 0.8, None, (50, 50, 50), 2.4)
        p.line([(x - r * 0.3, y - r * 1.6), (x + r * 0.3, y - r * 1.4)], (50, 50, 50), 2.0)   # a barb
        x += r * 1.3


def _gate_leaf(p, hinge_x, side, k, d=WALL_D):
    """One gate leaf hinged at hinge_x (m), swinging in towards the lens by k (0 shut, 1 blown flat open)."""
    th = math.radians(105 * k)
    w = GATE_HALF
    fx, fd = hinge_x - side * w * math.cos(th), d - w * math.sin(th)
    a0, a1 = CAMP.p(hinge_x, d, 0.1), CAMP.p(hinge_x, d, 2.4)
    b0, b1 = CAMP.p(fx, fd, 0.1), CAMP.p(fx, fd, 2.4)
    leaf = [a1, b1, b0, a0]
    p.poly(leaf, PLANK, INK, 2.6)
    for u in (0.25, 0.5, 0.75):                                         # the planks
        q0 = (a0[0] + (b0[0] - a0[0]) * u, a0[1] + (b0[1] - a0[1]) * u)
        q1 = (a1[0] + (b1[0] - a1[0]) * u, a1[1] + (b1[1] - a1[1]) * u)
        p.line([q0, q1], PLANK_D, 1.8)
    m = lambda u, v: (a1[0] + (b1[0] - a1[0]) * u + ((a0[0] + (b0[0] - a0[0]) * u) - (a1[0] + (b1[0] - a1[0]) * u)) * v,
                      a1[1] + (b1[1] - a1[1]) * u + ((a0[1] + (b0[1] - a0[1]) * u) - (a1[1] + (b1[1] - a1[1]) * u)) * v)
    _tin_sheet(p, [m(0.1, 0.1), m(0.9, 0.1), m(0.9, 0.45), m(0.1, 0.45)], TIN, int(hinge_x * 10) + 3, 6)
    p.poly([m(0.05, 0.55), m(0.95, 0.85), m(0.95, 0.92), m(0.05, 0.62)], PLANK_D, INK, 1.8)     # a cross brace
    p.poly([m(0.3, 0.6), m(0.7, 0.6), m(0.7, 0.66), m(0.3, 0.66)], (180, 40, 36), None)         # a painted red stripe


def _container(p, x0, x1, d, depth, col, seed, z0=0.0):
    """A shipping container end-on (its doors to us) with its long side going back; z0 > 0 stacks it on another."""
    f0, f1 = CAMP.p(x0, d, z0), CAMP.p(x1, d, z0 + 2.6)
    b0, b1 = CAMP.p(x1, d + depth, z0), CAMP.p(x1, d + depth, z0 + 2.6)
    if x1 < 0:                                                          # left of the lens: its right side shows
        p.poly([(f1[0], f0[1]), b0, b1, (f1[0], f1[1])], dk(col, 0.8), INK, 2.4)
        for k in range(1, 10):
            u = k / 10
            p.line([(f1[0] + (b0[0] - f1[0]) * u, f0[1] + (b0[1] - f0[1]) * u),
                    (f1[0] + (b1[0] - f1[0]) * u, f1[1] + (b1[1] - f1[1]) * u)], dk(col, 0.65), 1.4)
    face = quad(f0[0], f1[1], f1[0], f0[1])
    p.poly(face, col, INK, 2.6)
    cx = (f0[0] + f1[0]) / 2
    p.line([(cx, f1[1]), (cx, f0[1])], dk(col, 0.6), 2.0)               # the two doors
    for k in range(1, 8):
        xx = f0[0] + (f1[0] - f0[0]) * k / 8
        p.line([(xx, f1[1] + 8), (xx, f0[1] - 8)], dk(col, 0.72), 2.4)
    cs = (f1[0] - f0[0]) * 0.06                                         # the corner castings
    for cx_, cy_ in ((f0[0], f1[1]), (f1[0], f1[1]), (f0[0], f0[1]), (f1[0], f0[1])):
        p.poly(quad(cx_ - cs * (cx_ == f1[0]), cy_ - cs * (cy_ == f0[1]), cx_ + cs * (cx_ == f0[0]), cy_ + cs * (cy_ == f1[1])),
               (60, 60, 60), INK, 1.2)
    for xx in (cx - (f1[0] - f0[0]) * 0.12, cx + (f1[0] - f0[0]) * 0.12):  # the lock bars
        p.line([(xx, f1[1] + 10), (xx, f0[1] - 10)], (60, 60, 60), 2.4)
    r = random.Random(seed)
    for _ in range(3):
        xx = r.uniform(f0[0], f1[0])
        p.poly([(xx, f1[1] + 6), (xx + 8, f1[1] + 6), (xx + 4, f1[1] + r.uniform(40, 120))], RUST, None)
    p.poly(face, None, INK, 2.6)


def _crate(p, x, d, size, z=0.0, seed=0):
    a, b = CAMP.p(x - size / 2, d, z), CAMP.p(x + size / 2, d, z + size)
    box = quad(a[0], b[1], b[0], a[1])
    p.poly(box, PLANK, INK, 2.4)
    p.poly(quad(a[0] + 4, b[1] + 4, b[0] - 4, b[1] + (a[1] - b[1]) * 0.14), PLANK_D, None)
    p.line([(a[0] + 6, b[1] + 6), (b[0] - 6, a[1] - 6)], PLANK_D, 2.2)
    p.line([(a[0] + 6, a[1] - 6), (b[0] - 6, b[1] + 6)], PLANK_D, 2.2)
    p.poly(box, None, INK, 2.4)


def _barrel(p, x, d, col=(60, 96, 70)):
    a, b = CAMP.p(x - 0.3, d, 0), CAMP.p(x + 0.3, d, 0.9)
    p.poly(quad(a[0], b[1], b[0], a[1]), col, INK, 2.4)
    for u in (0.3, 0.7):
        y = b[1] + (a[1] - b[1]) * u
        p.line([(a[0], y), (b[0], y)], dk(col, 0.7), 2.0)
    p.ell((a[0] + b[0]) / 2, b[1], (b[0] - a[0]) / 2, (b[0] - a[0]) * 0.12, dk(col, 0.85), INK, 2.0)


def _sandbags(p, x0, x1, d, rows=3, seed=0):
    """A sandbag wall: rows of fat rounded bags, staggered."""
    ppm = CAMP.ppm(d)
    bw, bh = 0.6 * ppm, 0.24 * ppm
    r = random.Random(seed)
    base = CAMP.p(0, d, 0)[1]
    for row in range(rows):
        y = base - bh * (row + 0.5)
        x = CAMP.p(x0, d)[0] + (row % 2) * bw * 0.5
        xe = CAMP.p(x1, d)[0]
        while x < xe - bw * 0.3:
            c = SAND if r.random() > 0.3 else mix(SAND, SAND_D, 0.5)
            p.poly(curve([(x, y), (x + bw * 0.5, y - bh * 0.62), (x + bw, y), (x + bw * 0.5, y + bh * 0.55)], 4), c,
                   INK, 2.2)
            p.line([(x + bw * 0.12, y - bh * 0.05), (x + bw * 0.88, y - bh * 0.05)], SAND_D, 1.4)   # the stitched seam
            for e in (0.06, 0.94):                                                                  # the tied ends
                p.line([(x + bw * e, y - bh * 0.25), (x + bw * e, y + bh * 0.22)], SAND_D, 1.6)
            x += bw * 0.96


def _palm(p, x, y, h, seed, col=LEAF_D, lean=0.12):
    """A palm (ref 23, 24): a thin leaning trunk with ring marks, a crown of drooping fronds."""
    top = (x + h * lean, y - h)
    p.poly(ribbon(open_curve([(x, y), (x + h * lean * 0.66, y - h * 0.5), top], 6), h * 0.06, h * 0.035), (140, 116, 82),
           INK, 2.0)
    r = random.Random(seed)
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.55 + r.uniform(-0.1, 0.1)
        ln = h * r.uniform(0.38, 0.5)
        tip = (top[0] + math.cos(a) * ln, top[1] + math.sin(a) * ln * 0.5 + ln * 0.45)
        mid = (top[0] + math.cos(a) * ln * 0.55, top[1] + math.sin(a) * ln * 0.5 - ln * 0.05)
        p.poly(ribbon(open_curve([top, mid, tip], 6), h * 0.06, h * 0.01), col if k % 2 else LEAF, INK, 1.8)


def camp(img, cam, t=0.0, gate=0.0):
    """S7-S9: the walled enemy encampment in the forest (ref 23, 24): bright midday sky, jungle behind a ring of grey
    corrugated walls topped with wire, the plank-and-tin gate (gate 0 shut to 1 blown in), a blue and an orange
    container stacked on a blue one, crates, barrels, a watchtower ringed by sandbags, a flag, a dirt yard with tyre
    ruts, oil stains and weeds. (Build chat 8: the shack left this camera, it crowded the tower on the right.)"""
    p = B.Pen(img, cam)
    _sky(p, -400, 900, 1.3)
    for x, y, w, sd in ((220, 260, 200, 201), (820, 140, 240, 202), (640, 520, 150, 203)):
        _cloud(p, x, y, w, sd)
    p.poly(blob(540, 820, 900, 220, 16, 0.12, 204), mix(LEAF_D, SKY_LO, 0.4), INK, 2.0)   # far hills of trees
    for k, (x, rx, ry) in enumerate(((60, 220, 210), (330, 200, 180), (700, 210, 200), (1010, 230, 220))):
        clump(p, x, 700 - 40 * (k % 2), rx, ry, LEAF if k % 2 else LEAF_D, 210 + k)
    for x, h, sd, lean in ((180, 520, 221, -0.1), (560, 640, 222, 0.14), (900, 420, 223, -0.22)):
        _palm(p, x, 760, h, sd, lean=lean)
    p.poly(quad(-200, 760, W + 200, 2400), DIRT, None)                  # the yard
    # the flag and the watchtower stand behind the wall's line, drawn before it
    fp0, fp1 = CAMP.p(-0.6, 12.0, 0), CAMP.p(-0.6, 12.0, 7.0)
    p.line([fp0, fp1], (70, 70, 70), 4.0)
    wave = [(fp1[0] + 16 * k, fp1[1] + 8 * math.sin(t * 6 + k * 0.9)) for k in range(9)]
    p.poly(wave + [(x, y + 80) for x, y in wave[::-1]], FLAG_C, INK, 2.0)   # an invented flag: black, a white band
    p.poly([wave[2], wave[4], (wave[6][0], wave[6][1] + 80), (wave[4][0], wave[4][1] + 80)], (236, 232, 220), None)
    # the back wall, sheet by sheet, the gate's posts and the opening
    x = -6.0
    k = 0
    while x < 6.0:
        if abs(x + 0.5) < GATE_HALF + 0.5:
            x += 1.0
            continue
        a, b = CAMP.p(x, WALL_D, 0), CAMP.p(x + 1.0, WALL_D, WALL_H + 0.15 * math.sin(k * 2.1))
        _tin_sheet(p, quad(a[0], b[1], b[0], a[1]), (TIN, TIN_L, RUST, TIN, (92, 112, 122))[k % 5], 240 + k)
        x += 1.0
        k += 1
    o0, o1 = CAMP.p(-GATE_HALF, WALL_D + 0.05, 0), CAMP.p(GATE_HALF, WALL_D + 0.05, 2.4)
    p.poly(quad(o0[0], o1[1], o1[0], o0[1]), mix(DIRT_D, LEAF_D, 0.4), INK, 2.0)   # through the gate: the track out
    for sx in (-1, 1):                                                  # the gate posts
        q0, q1 = CAMP.p(sx * GATE_HALF - 0.12, WALL_D, 0), CAMP.p(sx * GATE_HALF + 0.12, WALL_D, 2.9)
        p.poly(quad(q0[0], q1[1], q1[0], q0[1]), PLANK_D, INK, 2.4)
    for sx in (-1, 1):
        _gate_leaf(p, sx * GATE_HALF, sx, gate)
    _wire(p, CAMP.p(-6, WALL_D)[0], CAMP.p(-GATE_HALF - 0.2, WALL_D)[0], CAMP.p(0, WALL_D, WALL_H)[1], 12)
    _wire(p, CAMP.p(GATE_HALF + 0.2, WALL_D)[0], CAMP.p(6, WALL_D)[0], CAMP.p(0, WALL_D, WALL_H)[1], 12)
    # the watchtower (inside, right): four legs, cross braces, a plank platform, a tin roof, a ladder
    tx, td = TOWER
    for lx in (tx - 0.9, tx + 0.9):
        a, b = CAMP.p(lx, td, 0), CAMP.p(lx + (0.25 if lx < tx else -0.25), td, 4.5)
        p.poly([(a[0] - 6, a[1]), (a[0] + 6, a[1]), (b[0] + 6, b[1]), (b[0] - 6, b[1])], PLANK_D, INK, 2.0)
    for z0, z1 in ((0.4, 2.4), (2.4, 4.4)):
        p.line([CAMP.p(tx - 0.85, td, z0), CAMP.p(tx + 0.75, td, z1)], PLANK_D, 3.0)
        p.line([CAMP.p(tx + 0.85, td, z0), CAMP.p(tx - 0.75, td, z1)], PLANK_D, 3.0)
    pa, pb = CAMP.p(tx - 1.1, td, 4.4), CAMP.p(tx + 1.1, td, 5.4)
    p.poly(quad(pa[0], pb[1], pb[0], pa[1]), PLANK, INK, 2.4)
    for u in np.linspace(0.1, 0.9, 7):                                 # planks (pass 1: a blank box)
        p.line([(pa[0] + (pb[0] - pa[0]) * u, pb[1] + 3), (pa[0] + (pb[0] - pa[0]) * u, pa[1] - 3)], PLANK_D, 2.0)
    p.poly(quad(pa[0] + (pb[0] - pa[0]) * 0.3, pb[1] + 10, pa[0] + (pb[0] - pa[0]) * 0.7, pb[1] + 26), (40, 34, 30), INK, 1.6)
    for lx in (tx - 1.0, tx + 1.0):                                     # the roof posts (pass 1: the roof floated)
        a_, b_ = CAMP.p(lx, td, 5.4), CAMP.p(lx, td, 6.3)
        p.poly(quad(a_[0] - 5, b_[1], a_[0] + 5, a_[1]), PLANK_D, INK, 1.8)
    p.line([CAMP.p(tx - 1.1, td, 5.75), CAMP.p(tx + 1.1, td, 5.75)], PLANK_D, 3.0)   # the rail
    ra, rb = CAMP.p(tx - 1.4, td, 6.2), CAMP.p(tx + 1.4, td, 6.2)
    rt = CAMP.p(tx, td, 6.9)
    _tin_sheet(p, [(ra[0], rb[1]), (rb[0], rb[1]), (rb[0] - 20, rt[1]), (ra[0] + 20, rt[1])][::1], TIN_D, 251, 6)
    # the yard floor: tyre ruts from the gate, stones, a dark patch, weeds at the wall's foot
    for sx in (-1, 1):
        rut = [CAMP.p(sx * 0.9 - 0.25, WALL_D, 0), CAMP.p(sx * 0.9 + 0.25, WALL_D, 0), CAMP.p(sx * 1.3 + 0.35, 1.4, 0),
               CAMP.p(sx * 1.3 - 0.35, 1.4, 0)]
        p.poly(rut, DIRT_D, None)
    rr = random.Random(261)
    for kk in range(0):                                                 # (pass 1: the oil stains read as shadows)
        d = rr.uniform(1.6, 3.2)
        q = CAMP.p(rr.uniform(-1.4, 1.4), d, 0)
        s_ = CAMP.ppm(d)
        p.poly(blob(q[0], q[1], s_ * rr.uniform(0.25, 0.45), s_ * 0.08, 10, 0.25, 265 + kk), mix(DIRT_D, (90, 80, 70), 0.35),
               None)
    for kk in range(40):
        d = 1.8 + (rr.random() ** 1.6) * 8.0
        q = CAMP.p(rr.uniform(-4, 4), d, 0)
        s = CAMP.ppm(d) * rr.uniform(0.06, 0.14)
        p.poly(curve([(q[0] - s, q[1]), (q[0], q[1] - s * 0.6), (q[0] + s, q[1])], 3), rr.choice([DIRT_L, (150, 140, 120)]),
               INK, 1.4)
    for kk in range(10):
        q = CAMP.p(rr.uniform(-6, 6), WALL_D - 0.1, 0)
        tuft(p, q[0], q[1] + 4, 26, (110, 130, 70), kk + 270, 5, 1.8)
    for kk in range(9):                                                 # weeds poking up through the near yard
        d = rr.uniform(1.8, 5.0)
        q = CAMP.p(rr.choice((-1, 1)) * rr.uniform(1.2, 2.6) * d / 4, d, 0)
        tuft(p, q[0], q[1], 0.25 * CAMP.ppm(d), (120, 136, 72), kk + 280, 6, 2.0)
    # containers (left), the orange one stacked on the blue (ref 23), both inside the wall; crates and barrels
    _container(p, *CONTAINERS['blue container'], CONT_BLUE, 281)
    _container(p, *CONTAINERS['orange container'], CONT_ORANGE, 282, z0=2.6)
    _crate(p, -2.2, 6.6, 0.9, 0, 283)
    _crate(p, -2.15, 6.6, 0.7, 0.9, 284)
    _barrel(p, 1.05, 6.6)                                               # pass 1: clear of the gunman's feet
    _barrel(p, 1.35, 7.2, (150, 60, 44))
    for x, d in ((2.2, 8.2), (3.9, 8.0)):                               # sandbags round the tower's foot
        _sandbags(p, x - 0.7, x + 0.7, d, 2, 300 + int(x * 10))
    for x, d, sd in ((-1.6, 2.9, 0), (1.5, 3.1, 1), (-0.4, 6.0, 2), (2.6, 4.4, 3)):   # the near yard: spent cases,
        q = CAMP.p(x, d, 0)                                             # a dropped helmet, a tyre (pass 1: empty)
        u = CAMP.ppm(d)
        if sd == 3:
            p.ell(q[0], q[1] - u * 0.18, u * 0.36, u * 0.18, (40, 40, 40), INK, 2.4)
            p.ell(q[0], q[1] - u * 0.18, u * 0.18, u * 0.08, DIRT_D, INK, 1.8)
        elif sd == 2:
            p.poly(curve([(q[0] - u * 0.16, q[1]), (q[0] - u * 0.14, q[1] - u * 0.14), (q[0] + u * 0.14, q[1] - u * 0.14),
                          (q[0] + u * 0.16, q[1])], 3), (70, 80, 64), INK, 2.0)
        else:
            for kk in range(6):
                p.poly(ribbon([(q[0] + kk * u * 0.07, q[1] - kk % 2 * u * 0.03),
                               (q[0] + kk * u * 0.07 + u * 0.05, q[1] - kk % 2 * u * 0.03 - u * 0.01)], u * 0.018, u * 0.016),
                       (206, 160, 60), INK, 1.0)


def camp_front(img, cam, t=0.0):
    """The sandbags nearest the lens, over the cast (they hide nobody's feet in S7: they sit in the corners)."""
    p = B.Pen(img, cam)
    _sandbags(p, 1.2, 2.3, 3.4, 2, 302)                                # a low emplacement, the bottom right corner


# ================================================================================================ Castle Town
TOWN = Level(h=2.4, hz=600.0, f=1100.0)   # build chat 8: raised, so KG stands below the line-up, not over it
COBBLE, COBBLE_D, COBBLE_L = (148, 148, 156), (118, 118, 128), (176, 176, 182)
PLASTER = [(236, 224, 196), (240, 216, 176), (232, 206, 196), (226, 226, 210)]
BEAM, ROOF, ROOF_D = (98, 66, 44), (196, 92, 56), (156, 68, 42)
BANNER, BANNER_D, GOLD = (44, 80, 160), (30, 56, 120), (226, 186, 70)
WALLSTONE, WALLSTONE_D = (222, 212, 192), (186, 176, 156)
CASTLE = (196, 206, 222)
TENT_R = (198, 54, 50)


def _cobbles(p, y0, y1, ppm_at, seed, x0=-200, x1=W + 200):
    """Rows of rounded grey cobbles that grow nearer the lens."""
    p.poly(quad(x0, y0, x1, y1), COBBLE_D, None)
    rr = random.Random(seed)
    y = y0
    row = 0
    while y < y1:
        h = max(5.0, ppm_at(y) * 0.16)
        x = x0 + (row % 2) * h * 0.7
        while x < x1:
            w = h * rr.uniform(1.1, 1.6)
            c = rr.choice([COBBLE, COBBLE, COBBLE_L, mix(COBBLE, COBBLE_D, 0.4)])
            p.poly(curve([(x + 2, y + h * 0.5), (x + w * 0.5, y + 2), (x + w - 2, y + h * 0.5), (x + w * 0.5, y + h - 2)],
                         3), c, INK if h > 9 else None, 1.2)
            x += w
        y += h
        row += 1


def _house(img, p, x0, x1, base, top, roof_h, col, seed, balcony=True):
    """A Castle Town house front (ref 21): cream plaster in dark timber framing, two floors of shuttered windows,
    a door, a balcony with flower boxes, a steep red-orange tiled gable."""
    w = x1 - x0
    p.poly(quad(x0, top, x1, base), col, INK, 2.6)
    cx = (x0 + x1) / 2
    roof = ([(x0 - w * 0.06, top + 4), (cx, top - roof_h), (x1 + w * 0.06, top + 4)] if seed % 2 == 0 else
            [(x0 - w * 0.06, top + 4), (x0 + w * 0.12, top - roof_h * 0.7), (x1 - w * 0.12, top - roof_h * 0.7),
             (x1 + w * 0.06, top + 4)])                                 # pass 1: a side-on roof every other house
    p.poly(roof, ROOF, INK, 2.6)
    for k in range(1, 5):                                               # the tile rows
        u = k / 5
        p.line([(x0 - w * 0.06 + (cx - x0 + w * 0.06) * u, top + 4 - roof_h * u),
                (x1 + w * 0.06 - (x1 + w * 0.06 - cx) * u, top + 4 - roof_h * u)], ROOF_D, 1.6)
    fl = (base - top) / 3
    for k in range(1, 3):                                               # timber beams: floors, posts, braces
        p.line([(x0, top + fl * k), (x1, top + fl * k)], BEAM, 6.0)
    for u in (0.02, 0.5, 0.98):
        p.line([(x0 + w * u, top), (x0 + w * u, base)], BEAM, 6.0)
    for k in range(2):                                                  # braces on both floors (pass 1: unseen)
        p.line([(x0, top + fl * (k + 1)), (x0 + w * 0.22, top + fl * k)], BEAM, 4.5)
        p.line([(x1, top + fl * (k + 1)), (x1 - w * 0.22, top + fl * k)], BEAM, 4.5)
    r = random.Random(seed)
    for row in range(2):                                                # windows with shutters
        for u in (0.25, 0.75):
            wx, wy = x0 + w * u, top + fl * (row + 0.45)
            ww, wh = w * 0.13, fl * 0.42
            p.poly(quad(wx - ww, wy - wh / 2, wx + ww, wy + wh / 2), (70, 90, 120), INK, 2.0)
            p.line([(wx, wy - wh / 2), (wx, wy + wh / 2)], BEAM, 1.6)
            sc = r.choice([(70, 120, 90), (60, 90, 140), (150, 60, 50)])
            for sg in (-1, 1):
                p.poly(quad(wx + sg * ww, wy - wh / 2, wx + sg * ww * 1.7, wy + wh / 2), sc, INK, 1.8)
            if row == 1 or r.random() > 0.5:                          # a flower box
                p.poly(quad(wx - ww * 1.1, wy + wh / 2, wx + ww * 1.1, wy + wh / 2 + fl * 0.08), BEAM, INK, 1.6)
                for kk in range(4):
                    p.ell(wx - ww + ww * 0.66 * kk, wy + wh / 2 - 3, ww * 0.22, ww * 0.18,
                          (210, 50, 60) if kk % 2 else (150, 80, 180), INK, 1.2)
    dx = x0 + w * r.choice([0.25, 0.75])
    p.poly(curve([(dx - w * 0.1, base), (dx - w * 0.1, base - fl * 0.7), (dx, base - fl * 0.85), (dx + w * 0.1, base - fl * 0.7),
                  (dx + w * 0.1, base)], 2), (110, 70, 44), INK, 2.2)
    if balcony:
        by = top + fl * 2 - 2
        p.poly(quad(x0 + w * 0.12, by, x1 - w * 0.12, by + fl * 0.1), BEAM, INK, 2.0)
        for kk in range(9):
            xx = x0 + w * 0.14 + (w * 0.72) * kk / 8
            p.line([(xx, by - fl * 0.25), (xx, by)], BEAM, 2.0)
        p.line([(x0 + w * 0.12, by - fl * 0.25), (x1 - w * 0.12, by - fl * 0.25)], BEAM, 2.4)


def _crest(p, x, y, r):
    """An invented gold crest for the banners: a bird with spread wings over a small triangle (not the game's)."""
    p.poly([(x, y - r * 0.3), (x - r, y - r * 0.6), (x - r * 0.5, y), (x, y + r * 0.2), (x + r * 0.5, y), (x + r, y - r * 0.6)],
           GOLD, INK, 1.8)
    p.poly([(x, y + r * 0.3), (x - r * 0.35, y + r * 0.9), (x + r * 0.35, y + r * 0.9)], GOLD, INK, 1.8)


def _banner(p, x, top, w, h, t=0.0):
    p.line([(x - w * 0.6, top), (x + w * 0.6, top)], (60, 50, 40), 4.0)
    sway = 6 * math.sin(t * 1.4 + x)
    p.poly([(x - w / 2, top), (x + w / 2, top), (x + w / 2 + sway, top + h), (x + sway, top + h * 1.12),
            (x - w / 2 + sway, top + h)], BANNER, INK, 2.4)
    p.poly(quad(x - w / 2 + 6, top + 4, x + w / 2 - 6, top + h * 0.08), GOLD, None)
    p.line([(x - w / 2 + 5, top + h * 0.08), (x - w / 2 + 5 + sway, top + h - 4)], GOLD, max(2.0, w * 0.04))   # gold trim
    p.line([(x + w / 2 - 5, top + h * 0.08), (x + w / 2 - 5 + sway, top + h - 4)], GOLD, max(2.0, w * 0.04))
    p.line([(x - w / 2 + sway, top + h), (x + sway, top + h * 1.12), (x + w / 2 + sway, top + h)], GOLD, max(2.0, w * 0.05))
    _crest(p, x + sway * 0.5, top + h * 0.42, w * 0.32)
    p.line([(x - w / 2 + 8, top + h * 0.08), (x - w / 2 + 8 + sway, top + h - 6)], BANNER_D, 2.0)


def _bunting(p, xa, ya, xb, yb, sag, n, t=0.0):
    pts = [(xa + (xb - xa) * u, ya + (yb - ya) * u + sag * 4 * u * (1 - u)) for u in np.linspace(0, 1, n + 1)]
    p.line(open_curve(pts, 3), (70, 60, 50), 1.8)
    for k in range(n):
        (x0, y0), (x1, y1) = pts[k], pts[k + 1]
        c = ((200, 50, 50), (50, 90, 170), (230, 190, 60))[k % 3]
        p.poly([(x0, y0), (x1, y1), ((x0 + x1) / 2, (y0 + y1) / 2 + abs(x1 - x0) * 0.9)], c, INK, 1.2)


def _fountain(p, x, d, t):
    """The square's stone fountain (ref 21): a round basin, a pillar with two tiers, an invented stone figure
    holding a jug on top, water falling from the tiers into the basin."""
    ppm = TOWN.ppm(d)
    bx, by = TOWN.p(x, d, 0)
    R = 2.4 * ppm
    p.ell(bx, by, R, R * 0.2, (180, 180, 186), INK, 2.4)                # the basin floor
    p.poly(quad(bx - R, by - 0.7 * ppm, bx + R, by), (150, 146, 140), INK, 2.4)   # its wall (pass 1: darker, ref 21)
    p.ell(bx, by - 0.7 * ppm, R, R * 0.2, (120, 170, 210), INK, 2.4)     # the water
    p.ell(bx, by - 0.7 * ppm, R * 0.8, R * 0.13, (160, 200, 230), None)
    for k in range(-5, 6):
        p.line([(bx + R * k / 5.5, by - 0.62 * ppm), (bx + R * k / 5.5, by - 0.05 * ppm)], (170, 168, 172), 1.4)
    col_top = by - 3.0 * ppm
    p.poly(quad(bx - 0.25 * ppm, col_top, bx + 0.25 * ppm, by - 0.7 * ppm), (160, 156, 150), INK, 2.2)
    for z, rr in ((1.7, 1.0), (2.6, 0.6)):                              # two tiers
        ty = by - z * ppm
        p.poly([(bx - rr * ppm, ty), (bx + rr * ppm, ty), (bx + rr * 0.6 * ppm, ty + 0.25 * ppm),
                (bx - rr * 0.6 * ppm, ty + 0.25 * ppm)], (200, 198, 202), INK, 2.2)
        for sg in (-1, 1):                                              # falling water
            p.poly(ribbon(open_curve([(bx + sg * rr * ppm, ty), (bx + sg * (rr + 0.25) * ppm, ty + 0.4 * ppm),
                                      (bx + sg * (rr + 0.35) * ppm, by - 0.75 * ppm)], 5), 0.08 * ppm, 0.14 * ppm),
                   (180, 214, 240), None)
    fx, fy = bx, col_top
    p.poly([(fx - 0.18 * ppm, fy), (fx + 0.18 * ppm, fy), (fx + 0.14 * ppm, fy - 0.9 * ppm),
            (fx - 0.14 * ppm, fy - 0.9 * ppm)], (210, 208, 210), INK, 2.0)  # the figure's robe
    p.ell(fx, fy - 1.02 * ppm, 0.12 * ppm, 0.13 * ppm, (210, 208, 210), INK, 2.0)
    p.poly([(fx + 0.12 * ppm, fy - 0.8 * ppm), (fx + 0.4 * ppm, fy - 0.9 * ppm), (fx + 0.42 * ppm, fy - 0.7 * ppm),
            (fx + 0.3 * ppm, fy - 0.62 * ppm)], (200, 198, 200), INK, 1.8)  # the jug on her shoulder
    p.poly(ribbon(open_curve([(fx + 0.42 * ppm, fy - 0.72 * ppm), (fx + 0.6 * ppm, fy - 0.5 * ppm),
                              (fx + 0.75 * ppm, fy + 0.4 * ppm)], 5), 0.05 * ppm, 0.1 * ppm), (180, 214, 240), None)


def _tent(p, x, d, w=2.6):
    """The red-striped market stall (ref 21): a striped canopy with a scalloped valance on poles, a counter of
    fruit and sacks."""
    ppm = TOWN.ppm(d)
    bx, by = TOWN.p(x, d, 0)
    x0, x1 = bx - w / 2 * ppm, bx + w / 2 * ppm
    for xx in (x0 + 6, x1 - 6):
        p.line([(xx, by), (xx, by - 2.3 * ppm)], BEAM, 3.0)
    top, eave = by - 2.9 * ppm, by - 2.3 * ppm
    p.poly([(x0 - 10, eave), (bx, top), (x1 + 10, eave)], (240, 232, 220), INK, 2.4)
    for k in range(6):
        if k % 2 == 0:
            u0, u1 = k / 6, (k + 1) / 6
            p.poly([(bx, top), (x0 - 10 + (x1 - x0 + 20) * u0, eave), (x0 - 10 + (x1 - x0 + 20) * u1, eave)], TENT_R, None)
    p.poly([(x0 - 10, eave), (bx, top), (x1 + 10, eave)], None, INK, 2.4)
    n = 7
    for k in range(n):                                                  # the scalloped valance
        xa = x0 - 10 + (x1 - x0 + 20) * k / n
        xb = x0 - 10 + (x1 - x0 + 20) * (k + 1) / n
        p.poly(curve([(xa, eave), (xb, eave), ((xa + xb) / 2, eave + 0.22 * ppm)], 3), TENT_R if k % 2 else (240, 232, 220),
               INK, 1.6)
    p.poly(quad(x0, by - 0.9 * ppm, x1, by), PLANK, INK, 2.2)           # the counter
    for k in range(9):
        p.ell(x0 + (x1 - x0) * (k + 0.5) / 9, by - 0.95 * ppm, 0.1 * ppm, 0.09 * ppm,
              ((220, 60, 40), (240, 170, 40), (120, 170, 60))[k % 3], INK, 1.2)


def _barrel_t(p, x, d):
    ppm = TOWN.ppm(d)
    bx, by = TOWN.p(x, d, 0)
    a, b = (bx - 0.3 * ppm, by), (bx + 0.3 * ppm, by - 0.9 * ppm)
    p.poly(curve([(a[0], a[1]), (a[0] - 0.04 * ppm, by - 0.45 * ppm), (a[0], b[1]), (b[0], b[1]), (b[0] + 0.04 * ppm,
                                                                                                   by - 0.45 * ppm),
                  (b[0], a[1])], 2), PLANK, INK, 2.2)
    for u in (0.2, 0.8):
        p.line([(a[0], by - 0.9 * ppm * u), (b[0], by - 0.9 * ppm * u)], (90, 80, 70), 2.0)


def _sack(p, x, d):
    ppm = TOWN.ppm(d)
    bx, by = TOWN.p(x, d, 0)
    p.poly(curve([(bx - 0.25 * ppm, by), (bx - 0.28 * ppm, by - 0.4 * ppm), (bx - 0.08 * ppm, by - 0.62 * ppm),
                  (bx + 0.1 * ppm, by - 0.6 * ppm), (bx + 0.28 * ppm, by - 0.38 * ppm), (bx + 0.24 * ppm, by)], 3),
           (206, 186, 140), INK, 2.0)


def _townsfolk(p, x, d, col, seed):
    """A small far-off townsperson: a simple robe, head and hat, no face at this size (ref 21's crowd)."""
    ppm = TOWN.ppm(d)
    bx, by = TOWN.p(x, d, 0)
    h = 1.65 * ppm
    p.poly([(bx - 0.22 * ppm, by), (bx + 0.22 * ppm, by), (bx + 0.16 * ppm, by - h * 0.78), (bx - 0.16 * ppm, by - h * 0.78)],
           col, INK, 1.6)
    p.ell(bx, by - h * 0.87, 0.11 * ppm, 0.12 * ppm, (240, 206, 180), INK, 1.4)
    if seed % 2:
        p.poly([(bx - 0.16 * ppm, by - h * 0.93), (bx + 0.16 * ppm, by - h * 0.93), (bx, by - h * 1.06)], (90, 70, 50),
               INK, 1.2)


def _castle(p, cx, base, s):
    """Hyrule Castle far behind, pale and hazy (ref 21): a keep with tall round towers and pointed roofs."""
    c, r = CASTLE, mix(CASTLE, (150, 160, 190), 0.5)
    p.poly(quad(cx - 140 * s, base - 120 * s, cx + 140 * s, base), c, mix(c, INK, 0.4), 1.6)
    for dx, h, w in ((-150, 230, 30), (-60, 300, 34), (40, 340, 40), (140, 250, 30)):
        x = cx + dx * s
        p.poly(quad(x - w * s, base - h * s, x + w * s, base), c, mix(c, INK, 0.4), 1.6)
        p.poly([(x - w * 1.2 * s, base - h * s), (x, base - (h + 90) * s), (x + w * 1.2 * s, base - h * s)], r,
               mix(c, INK, 0.4), 1.6)
        for k in range(2):
            p.poly(quad(x - 5 * s, base - (h - 40 - 60 * k) * s, x + 5 * s, base - (h - 70 - 60 * k) * s), r, None)


def town_square(img, p, cam, t):
    """S10, the line-up (ref 21, 22): Castle Town square: blue sky, the hazy castle behind the rooftops, timber-framed
    houses with red-orange roofs, the fountain, a palm, the red-striped stall, barrels and sacks, banners, bunting,
    a few townsfolk, grey cobbles to the lens."""
    _sky(p, -400, 950, 2.0)
    for x, y, w, sd in ((180, 200, 180, 401), (860, 300, 200, 402)):
        _cloud(p, x, y, w, sd)
    _castle(p, 560, 640, 1.0)
    haze(img, cam, 300, 700, (230, 236, 244), 0.25)
    xs = [-140, 150, 400, 680, 940, 1220]                                # the far row of houses, varied widths
    tops = [420, 470, 400, 450, 430]
    roofs = [160, 120, 180, 140, 150]
    base = TOWN.p(0, 24.0)[1]
    for k in range(5):
        _house(img, p, xs[k] + 6, xs[k + 1] - 6, base, tops[k] + 120, roofs[k], PLASTER[k % 4], 410 + k, k % 2 == 0)
    _cobbles(p, base, 2400, lambda y: (y - TOWN.hz) / TOWN.h, 420)
    for x, d, c, sd in ((-1.8, 20.0, (120, 90, 150), 1), (2.6, 21.0, (90, 120, 90), 2), (-4.2, 19.0, (170, 110, 70), 3)):
        _townsfolk(p, x, d, c, sd)
    _fountain(p, 0.2, 15.0, t)
    _bunting(p, -40, 760, 1120, 700, 70, 14, t)
    # the near sides: a palm on the left, the stall, barrels and sacks on the right; banners on poles
    q = TOWN.p(-3.4, 11.0)
    _palm(p, q[0], q[1], 7.0 * TOWN.ppm(11.0), 431)
    _tent(p, 3.3, 10.0)
    for x, d in ((1.9, 10.2), (2.25, 10.4)):                            # pass 1: barrels and sacks AT the stall
        _barrel_t(p, x, d)
    for x, d in ((4.7, 10.1), (4.95, 10.3)):
        _sack(p, x, d)
    for k, (x, d, c) in enumerate(((-3.0, 12.0, (110, 80, 140)), (3.1, 12.5, (80, 110, 150)), (-1.2, 13.0, (150, 100, 60)))):
        _townsfolk(p, x, d, c, 10 + k)                                  # pass 1: townsfolk nearer, so they show
    for x, d in ((-2.9, 8.0), (3.4, 7.6)):
        a, b = TOWN.p(x, d, 0), TOWN.p(x, d, 4.4)
        p.line([a, b], (70, 60, 50), 4.0)
        _banner(p, b[0] + 46 * (1 if x < 0 else -1), b[1] + 20, 0.8 * TOWN.ppm(d), 2.2 * TOWN.ppm(d), t)


WALL_VIEW = dict(base=1640, ppm=560.0)         # S12, S13: the wall's foot on screen and pixels per metre there


def town_wall(img, p, cam, t):
    """S12 and S13, the slam (ref 22): a pale stone wall filling the frame: big hand-cut blocks, a shuttered window
    with a flower box (red and purple), a tall blue banner with the gold crest on an iron bracket, a strip of
    bunting, cobbles at its foot."""
    ppm = WALL_VIEW['ppm']
    base = WALL_VIEW['base']
    p.poly(quad(-200, -400, W + 200, base), WALLSTONE, None)
    rr = random.Random(501)
    bh = 0.42 * ppm
    row = 0
    y = base
    while y > -400:                                                     # the blocks, row by row
        x = -200 - (row % 2) * bh
        while x < W + 200:
            bw = bh * rr.uniform(1.4, 2.2)
            c = mix(WALLSTONE, WALLSTONE_D, rr.uniform(0, 0.45))
            p.poly(wob(quad(x + 3, y - bh + 3, x + bw - 3, y - 3), 2.0, row * 41 + int(x), 30), c, INK, 2.0)
            x += bw
        y -= bh
        row += 1
    wx, wy = 820, 300                                                   # the window, high right
    p.poly(quad(wx - 130, wy - 170, wx + 130, wy + 170), (70, 90, 120), INK, 3.0)
    p.line([(wx, wy - 170), (wx, wy + 170)], BEAM, 3.0)
    p.line([(wx - 130, wy), (wx + 130, wy)], BEAM, 3.0)
    for sg in (-1, 1):
        p.poly(quad(wx + sg * 130, wy - 170, wx + sg * 230, wy + 170), (60, 90, 140), INK, 2.6)
        for k in range(1, 12):                                          # louvres (pass 1: flat panels)
            yy = wy - 170 + 340 * k / 12
            p.poly(quad(wx + sg * 136 - (sg < 0) * 88, yy - 9, wx + sg * 136 + (sg > 0) * 88, yy),
                   (82, 112, 160), None)
            p.line([(wx + sg * 136, yy), (wx + sg * 224, yy)], (36, 58, 100), 2.2)
        for yy in (wy - 120, wy + 120):                                 # the iron hinges
            p.poly(quad(wx + sg * 130 - (sg < 0) * 40, yy - 6, wx + sg * 130 + (sg > 0) * 40, yy + 6), (40, 40, 40), INK, 1.2)
    p.poly(quad(wx - 170, wy + 170, wx + 170, wy + 240), BEAM, INK, 2.6)   # the flower box
    for k in range(8):
        flower(p, wx - 150 + 43 * k, wy + 160 - 18 * (k % 2), 30, (210, 50, 60) if k % 2 else PURPLE)
    for k in range(5):
        p.poly(curve([(wx - 140 + 70 * k, wy + 175), (wx - 120 + 70 * k, wy + 240), (wx - 100 + 70 * k, wy + 175)], 3), LEAF,
               INK, 1.6)
    for k in range(40):                                                 # stone texture: chips, cracks, weathering
        cx_, cy_ = rr.uniform(-20, 1100), rr.uniform(-20, base - 20)
        if k % 3 == 0:
            p.line(open_curve([(cx_, cy_), (cx_ + rr.uniform(-30, 30), cy_ + 25), (cx_ + rr.uniform(-40, 40), cy_ + 55)], 3),
                   WALLSTONE_D, 1.6)
        else:
            p.poly(curve([(cx_, cy_), (cx_ + 14, cy_ - 6), (cx_ + 22, cy_ + 6), (cx_ + 8, cy_ + 12)], 3), WALLSTONE_D, None)
    sx_ = [wx - 230 + 460 * u for u in np.linspace(0, 1, 9)]             # a blue drape with gold fringe under the sill
    sw_ = [(xx, wy + 250 + 70 * math.sin(math.pi * ((i % 4) / 4))) for i, xx in enumerate(sx_)]
    p.poly([(wx - 230, wy + 240), (wx + 230, wy + 240)] + sw_[::-1], BANNER, INK, 2.4)
    p.line(sw_, GOLD, 5.0)
    p.poly(quad(30, base - 300, 190, base), (150, 90, 60), INK, 2.6)     # a planter at the wall's foot
    p.line([(30, base - 250), (190, base - 250)], (110, 64, 40), 3.0)
    for k in range(5):
        flower(p, 50 + 30 * k, base - 320 - 20 * (k % 2), 26, (210, 50, 60) if k % 2 else PURPLE)
    p.poly(quad(120, 120, 175, 140), (50, 46, 44), INK, 2.0)              # the iron bracket
    p.line([(130, 130), (330, 130)], (50, 46, 44), 6.0)
    _banner(p, 240, 140, 0.7 * ppm, 2.0 * ppm, t)
    _bunting(p, -40, -20, 1120, 30, 60, 8, t)
    _cobbles(p, base, 2400, lambda y: ppm * (1 + (y - base) / 600.0), 502)
    p.line([(-200, base), (W + 200, base)], INK, 3.0)


TOWN_VIEWS = {'square': town_square, 'wall': town_wall}


def town(img, cam, view, t=0.0):
    p = B.Pen(img, cam)
    TOWN_VIEWS[view](img, p, cam, t)


# ================================================================================================ stage
def _camp_mark(x, d):
    sx, sy = CAMP.p(x, d)
    return sx, sy, CAMP.ppm(d)


def _town_mark(x, d):
    sx, sy = TOWN.p(x, d)
    return sx, sy, TOWN.ppm(d)


STAGE = {      # where the cast stand: (screen x, ground y, pixels per metre). KG's perch is his feet on the branch.
    'forest_up': {'kg': (640, branch_y(640), 420.0)},
    'forest_down': {'link': (560, 1330, down_ppm(1330)), 'navi': (700, 1050, down_ppm(1330))},
    'forest_close': {'link': (540, 2300, 1100.0)},            # a close-up: his feet well below the frame
    'forest_edge': {'gunman': (300, 2500, 900.0)},        # pass 2: left, so his muzzle stays in frame
    'camp': {'kg': _camp_mark(0.75, 4.2), 'link': _camp_mark(-0.3, 3.5), 'gunman1': _camp_mark(-2.2, 9.2),
             'gunman2': _camp_mark(2.0, 7.6), 'gunman3': _camp_mark(3.3, 8.6)},   # the gunmen aside, the gate clear
    'town_square': {n: _town_mark(x, 4.0) for n, x in (('zelda', -0.72), ('malon', -0.22), ('ruto', 0.27),
                                                       ('goron', 0.92), ('saria', 1.55))},
    'town_wall': {'link': (400, WALL_VIEW['base'], WALL_VIEW['ppm']),       # on the cobbles: the shot lifts him
                  'kg': (860, WALL_VIEW['base'], WALL_VIEW['ppm'])},
}
STAGE['town_square']['kg'] = _town_mark(-0.95, 2.3)    # in front, below the line, presenting it


# ================================================================================================ boxes (rule 83)
def _box(level, x0, x1, d, z0, z1):
    a, b = level.p(x0, d, z0), level.p(x1, d, z1)
    return (a[0], b[1], b[0], a[1])


SET_BOXES = [   # the camp's solid things, screen px (the S7 camera); nothing may overlap unless meant
    ('blue container', _box(CAMP, -5.0, -2.6, 7.4, 0, 2.6)),
    ('orange container', _box(CAMP, -5.0, -2.6, 7.6, 2.6, 5.2)),
    ('crates', _box(CAMP, -2.65, -1.75, 6.6, 0, 1.6)),
    ('barrels', _box(CAMP, 0.75, 1.65, 6.6, 0, 0.9)),
    ('gate', _box(CAMP, -GATE_HALF, GATE_HALF, WALL_D, 0, 2.4)),
    ('watchtower', _box(CAMP, TOWER[0] - 1.1, TOWER[0] + 1.1, TOWER[1], 0, 6.9)),
]
SET_MEANT = [
    ('blue container', 'orange container', 'the orange one sits stacked on top of the blue (ref 23)'),
    ('crates', 'blue container', 'the crates stand in front of it, 0.8 m nearer the lens'),
    ('barrels', 'watchtower', 'the barrels stand 2 m nearer the lens, in front of its legs'),
    ('barrels', 'gate', 'the barrels stand 3 m nearer the lens, below the gate on screen'),
]


# ================================================================================================ BENCHMARK (rule 3)
BENCHMARK = [
    dict(place='Kokiri Forest, up at the branch (S1)', refs=['01-kg.jpg', '19-forest.jpg'], at='forest_up',
         items=[('low camera, blue sky and white clouds behind KG', 'done: three sky bands, four clouds'),
                ('a mossy branch from a great trunk, KG on it', 'done: branch_y gives his perch'),
                ('canopy round the top of the frame', 'done: six clumps with leaf marks'),
                ('Link\'s cap in the near left (the cast, not the set)', 'left out: drawn with the cast (link_head_back)'),
                ('bark on the trunk and branch', 'done: bark lines, moss on top'),
                ('moss hanging and lying on the branch', 'done'),
                ('soft green-gold distance at the foot', 'done: hazy far trees'),
                ('bright, sunny, storybook light', 'done: clear sky, pale haze')]),
    dict(place='Kokiri Forest floor (S2)', refs=['20-forest.jpg', '19-forest.jpg'], at='forest_down',
         items=[('a pale stone path winding back', 'done: stones in rows, nearer ones bigger'),
                ('mossy roots and rocks either side', 'done: two roots, two mossy rocks'),
                ('a tree house in a giant mossy stump, round door', 'done: _stump_house'),
                ('orange lanterns on the tree house', 'done: two, glowing'),
                ('purple flowers in the near corner', 'done'),
                ('a big glowing orange bell flower on the right', 'done'),
                ('tall dark trees behind', 'done: trunk and canopy at the top'),
                ('misty light shafts', 'done: two soft shafts, dappled light')]),
    dict(place='Kokiri Forest behind Link (S4, S6)', refs=['19-forest.jpg', '20-forest.jpg'], at='forest_close',
         items=[('huge rounded canopy trees in soft green-gold', 'done: far and mid clumps'),
                ('misty layered depths', 'done: three layers, paler further back'),
                ('light shafts', 'done'),
                ('the tree house trunk lower right', 'done: stump, door, window, lanterns'),
                ('the pale path', 'done'),
                ('the bell flower', 'done'),
                ('purple flowers', 'done'),
                ('near plants framing the bottom', 'done')]),
    dict(place='The gunman\'s patch (S5)', refs=['17-soldiers.jpg'], at='forest_edge',
         items=[('grey-green woodland', 'done: cooler, greyer forest'),
                ('thin trunks with bare side branches', 'done: five'),
                ('overcast pale sky through the trees', 'done'),
                ('long grass across the ground', 'done: 40 tufts'),
                ('ferns', 'done: three'),
                ('a mossy rock', 'done'),
                ('the soldier in front, rifle aimed into the trees', 'left out: drawn with the cast'),
                ('still Kokiri Forest (the brief)', 'done: the same leaf shapes, cooler')]),
    dict(place='The enemy encampment (S7-S9)', refs=['23-outpost.jpg', '24-outpost.jpg'], at='camp',
         items=[('a dirt yard', 'done: tyre ruts, stones'),
                ('ringed by grey corrugated walls', 'done: sheets with ribs and rust, wire on top'),
                ('blue and orange shipping containers', 'done: one of each'),
                ('wooden shacks with tin roofs', 'left out (build chat 8): it crowded the tower; tin roof on the tower instead'),
                ('crates', 'done: two stacked, barrels'),
                ('a flagpole', 'done: an invented black flag with a white band'),
                ('a watch post', 'done: four-legged tower, tin roof'),
                ('jungle round it, palms', 'done: three palms, clumps, far hills'),
                ('bright midday sun', 'done: clear blue sky, clouds'),
                ('parked old cars', 'left out: the narrow vertical frame has no room; the containers say "camp"')]),
    dict(place='Castle Town square (S10)', refs=['21-town.jpg', '22-town.jpg'], at='town_square',
         items=[('grey cobbles', 'done: rows growing to the lens'),
                ('a stone fountain with a statue in the middle', 'done: basin, two tiers, an invented figure'),
                ('timber-framed houses with red-orange tiled roofs', 'done: five, varied'),
                ('balconies and flower boxes', 'done'),
                ('a palm-like tree left', 'done'),
                ('a red-striped market tent', 'done: with a counter of fruit'),
                ('barrels and sacks', 'done'),
                ('townsfolk', 'done: three small, far back'),
                ('the castle pale and hazy far behind', 'done'),
                ('blue banners with a gold crest, bunting', 'done: an invented crest')]),
    dict(place='The town wall (S12, S13)', refs=['22-town.jpg'], at='town_wall',
         items=[('pale stone walls', 'done: hand-cut blocks'),
                ('tall blue banners with a gold crest', 'done: one on a bracket'),
                ('flower boxes, red and purple', 'done: under the window'),
                ('bunting across', 'done'),
                ('cobbles at the foot', 'done'),
                ('shuttered window', 'done: blue shutters'),
                ('stone balustrades with blue-and-gold drapes', 'left out: the wall shot is tight; the banner carries it'),
                ('bright daylight', 'done')]),
]


# ================================================================================================ sheets
def painting(at, t=0.0, cam=None, gate=0.0):
    """One set's painting through a camera (default: the full frame), RGBA at B.SS."""
    img = B.canvas((0, 0, 0))
    cam = cam or B.Cam(1.0)
    if at.startswith('forest'):
        v = at.split('_')[1]
        forest(img, cam, v, t)
        forest_front(img, cam, v, t)
    elif at == 'camp':
        camp(img, cam, t, gate)
        camp_front(img, cam, t)
    else:
        town(img, cam, at.split('_')[1], t)
    return img


def picture(at):
    return painting(at).resize((W, H), Image.LANCZOS)


def with_cast(at, t=0.0, gate=0.0):
    """The painting with the cast at their marks, for scale (rule 89's set sheet; O4)."""
    import remakes_cast as RC
    import remakes_creatures as CR
    img = B.canvas((0, 0, 0))
    cam = B.Cam(1.0)
    st = STAGE[at]
    if at.startswith('forest'):
        forest(img, cam, at.split('_')[1], t)
    elif at == 'camp':
        camp(img, cam, t, gate)
    else:
        town(img, cam, at.split('_')[1], t)
    for who, (x, y, ppm) in st.items():                                 # the soft foot shadows first (Sam Q3)
        if who != 'navi' and at != 'forest_up':      # Navi is a flying light: none; KG's branch: kg_on_branch
            foot_shadow(img, cam, x, y, ppm, SHADOW_W['gunman' if who.startswith('gunman') else who],
                        clip=branch_poly() if at == 'forest_up' else None)
    for who, (x, y, ppm) in sorted(st.items(), key=lambda kv: kv[1][1]):
        s = s_for(ppm)
        if who == 'kg' and at == 'forest_up':
            wings, mood = KG_BEAT[at]
            kg_on_branch(img, cam, x, s, mood=mood, wings=wings, t=t)
        elif who == 'kg':
            # his feet: about 230 units below his middle when perched (remakes_creatures._kg_feet at y + 230)
            view = 'side' if at in ('town_wall',) else 'front'
            wings, mood = KG_BEAT.get(at, ('fold', 'kindly'))
            CR.kg(img, cam, x, y - 240 * s, s, view=view, perched=(at == 'forest_up'), wings=wings,
                  band=at in ('camp', 'town_wall'), mood=mood, flip=-1 if at == 'town_wall' else 1)
        elif who == 'navi':
            CR.navi(img, cam, x, y, s * 1.2)
        elif who == 'goron':
            CR.goron(img, cam, x, y - CR.GORON_HEIGHT_U * 0.0, s)
        else:
            key = 'gunman' if who.startswith('gunman') else who
            sp = dict(RC.CAST[key])
            k = RC.scale_for(sp, s)
            if key == 'gunman':                                          # every gunman aims (ref 17), as in the shots
                j = RC.poses('gunman')['aiming']
                fl = -1 if (at == 'camp' and x > 540) else 1
                RC.person(img, B.Local(cam, x, 0, 1.0, fl) if fl < 0 else cam, (0 if fl < 0 else x), y - 928 * k, s, sp,
                          yaw=j['_yaw'], j=j)
            else:
                RC.person(img, cam, x, y - 928 * k, s, sp)
    if at.startswith('forest'):
        forest_front(img, cam, at.split('_')[1], t)
    elif at == 'camp':
        camp_front(img, cam, t)
    return img.resize((W, H), Image.LANCZOS)


KG_BEAT = {'forest_up': ('wide', 'hype'), 'camp': ('gun', 'war'), 'town_square': ('gesture', 'show'),
           'town_wall': ('fold', 'fury')}       # each set sheet shows KG as his shot has him (line 1, 7, 11, 13)

SETS = {'forest': ('forest_up', 'forest_down', 'forest_close', 'forest_edge'), 'camp': ('camp',),
        'town': ('town_square', 'town_wall')}


def alone(which, out, cast=True):
    """One set's cameras side by side at phone size (540 x 960 each), the cast at their marks for scale."""
    views = SETS[which]
    tiles = [(with_cast(v) if cast else picture(v)).convert('RGB').resize((540, 960), Image.LANCZOS) for v in views]
    sheet = Image.new('RGB', (len(tiles) * 560 + 20, 1000), (250, 248, 244))
    for i, im in enumerate(tiles):
        sheet.paste(im, (20 + i * 560, 20))
    sheet.save(out, quality=90)
    return out


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'alone':
        print(alone(sys.argv[2], sys.argv[3], '--bare' not in sys.argv))
    elif cmd == 'one':
        (with_cast(sys.argv[2]) if '--bare' not in sys.argv else picture(sys.argv[2])).convert('RGB').save(sys.argv[3],
                                                                                                          quality=90)
