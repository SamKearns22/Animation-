#!/usr/bin/env python3
"""Remakes (the Ocarina of Time remake satire): the three sets, flat paintings in the house style (flat colour, one
ink outline, hand-cut edges), one painting per camera (rule 39), from Sam's references 01, 17, 19-24. Drawn fresh,
never traced. The cast draw on top through the same B.Cam (world = 1080 x 1920 px at zoom 1), so a push-in is a
zoomed camera on the same painting.

MAP (rule 61)
  helpers ............. Level (a level pinhole in metres), blob (a scalloped clump), hand-cut edges, leaves, glow,
                        foot_shadow + SHADOW_W (Sam's soft shadows), shafts, flowers, moss_patches, s_for
  Kokiri Forest ....... forest(img, cam, view, t): 'up' (S1 up at KG's branch, S3 on him), 'down' (S2 from KG's eyes
                        on Link and Navi), 'close' (S4, S6 Link's close-ups), 'edge' (S5 the gunman's patch);
                        forest_front(img, cam, view) the near leaves over the cast; kg_on_branch (S1/S3: his
                        tail behind the branch); STUMP_DOWN / STUMP_SEED (one tree house for S2, S4, S6)
  the camp ............ camp(img, cam, t, gate=k): the walled Far Cry yard, one 3D-metre layout (CAMP), the gate
                        k 0 shut to 1 blown in ('camp_open' on the sheet); _near_yard, _tower_box (the lookout
                        stands in it), _camo_net, _tyres, BARRELS; camp_front(img, cam) the tower box and sandbags
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
# Rule 87: the three-pass survivors, each drawn two or three ways for Sam (options(); 'now' = as built)
OPT = {'up': 'cap', 'shafts': 'dark', 'edge': 'warm', 'wall': 'shelter', 'fountain': 'dark'}   # all A (Claude's
# picks, set 10 Nov so the animatic isn't held up; Sam can swap any letter)
MIST = (232, 236, 206)


def _sky(p, y0, y1, seed=0):
    """Three flat bands, deep overhead to pale low, with hand-cut wavy edges."""
    p.poly(quad(-200, y0, W + 900, y1), SKY_LO, None)                  # (to W + 900: remakes note 67's camp pan)
    for col, yy in ((SKY_MID, y0 + (y1 - y0) * 0.55), (SKY_HI, y0 + (y1 - y0) * 0.25)):
        edge = [(x, yy + 14 * math.sin(x / 130 + seed)) for x in np.linspace(-200, W + 900, 34)]
        p.poly([(-200, y0)] + edge + [(W + 900, y0)], col, None)


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
    """A paper lantern hung from a crooked wooden arm pegged into the bark (pass 1: flat squares, unhung; pass 3: a
    round body under a cap read as a hand bell): a tall glowing oval with rings round it, a dark band top and foot,
    a little tassel, the light all round it."""
    p.line(open_curve([(x - r * 2.2, y - r * 2.9), (x - r * 1.0, y - r * 3.2), (x, y - r * 2.9)], 4), (84, 62, 44), 4.0)
    p.ell(x - r * 2.2, y - r * 2.9, r * 0.3, r * 0.3, (60, 44, 34), INK, 1.4)           # the peg in the bark
    p.line([(x, y - r * 2.9), (x, y - r * 1.5)], INK, 1.8)                             # the cord
    glow(img, cam, x, y, r * 4.5, (255, 190, 90), 0.5)
    p.ell(x, y, r * 0.78, r * 1.3, LANTERN, INK, 2.0)                                  # the tall paper body
    p.ell(x - r * 0.18, y - r * 0.1, r * 0.4, r * 0.9, (255, 214, 140), None)          # lit from inside
    for v in (-0.75, -0.4, 0.0, 0.4, 0.75):                                            # the rings round it
        hw = r * 0.78 * math.sqrt(max(0.0, 1 - v * v))
        p.line(open_curve([(x - hw, y + r * 1.3 * v), (x, y + r * 1.3 * v + r * 0.12), (x + hw, y + r * 1.3 * v)], 3),
               (206, 110, 36), 1.4)
    for yy in (y - r * 1.38, y + r * 1.2):                                              # the dark bands top and foot
        p.poly(quad(x - r * 0.42, yy, x + r * 0.42, yy + r * 0.22), (64, 40, 30), INK, 1.4)
    p.line([(x, y + r * 1.42), (x, y + r * 1.9)], (190, 40, 36), 2.4)                  # the tassel
    p.poly([(x - r * 0.14, y + r * 1.8), (x + r * 0.14, y + r * 1.8), (x + r * 0.2, y + r * 2.3), (x - r * 0.2, y + r * 2.3)],
           (200, 48, 40), INK, 1.2)


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
        _door(p, x + w * 0.05, y - h * 0.01, w * 0.15)    # pass 3: it was shorter than Link
        wx_, wy_, ww_ = x - w * 0.25, y - h * 0.7, w * 0.07                # an arched window, lamp-lit, barred
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
    if OPT['up'] in ('steep', 'cap'):
        _forest_up_steep(img, p, cam, t)
    else:
        _forest_up_open(img, p, cam, t)
    for pts, w0, sd in (([(110, 600), (260, 380), (420, 240)], 90, 26), ([(90, 360), (40, 160), (-20, 60)], 80, 27),
                        ([(120, 900), (420, 760), (700, 640), (980, 520)], 70, 28)):   # boughs up into the canopy
        bark(p, pts, w0, w0 * 0.35, TRUNK, sd, MOSS, 2)
    _forest_up_branch(img, p, cam, t)


def _forest_up_steep(img, p, cam, t):
    """Option (rule 87, S1 reads level): a true worm's-eye view. No treetops below: the lower frame is the forest's
    own dim floor-level green with trunks rising out of it, all leaning in to one point high above; the sky only a
    bright hole in the canopy behind KG."""
    p.poly(quad(-200, -400, W + 200, 2400), mix(LEAF_D, (36, 58, 34), 0.35), None)
    hx, hy = 700, 300
    p.poly(blob(hx, hy, 470, 420, 16, 0.12, 3), SKY_LO, None)
    p.poly(blob(hx + 20, hy - 40, 360, 300, 14, 0.12, 4), SKY_MID, None)
    p.poly(blob(hx + 30, hy - 90, 240, 190, 12, 0.12, 5), SKY_HI, None)
    for x, y, w, sd in ((800, 240, 200, 1), (560, 420, 130, 2)):
        _cloud(p, x + 6 * math.sin(t * 0.3 + sd), y, w, sd)
    vx, vy = 640, -1400                                                 # where every trunk leans to
    for fx, w0, fade, sd in ((1250, 330, 0.0, 41), (520, 110, 0.45, 42), (830, 140, 0.35, 43), (330, 160, 0.3, 44),
                             (1010, 210, 0.15, 45)):
        far = fade >= 0.3                                               # remakes Fable r3 #38: the far trunks run on
        us = (0.3, 0.55, 0.95) if far else (0.3, 0.55)                  # up out of frame, tapering (cut off flat in
        pts = [(fx, 2200)] + [(fx + (vx - fx) * u, 2200 + (vy - 2200) * u) for u in us]   # the sky they read as
        bark(p, pts, w0, w0 * (0.2 if far else 0.45), mix(TRUNK, (40, 60, 40), fade), sd, MOSS, 3)   # chimneys)
    for ang, rx, ry, c, sd in ((200, 330, 230, LEAF_D, 11), (240, 300, 210, LEAF, 12), (285, 320, 220, LEAF_D, 13),
                               (330, 300, 210, LEAF, 14), (10, 320, 240, LEAF_D, 15), (60, 340, 260, LEAF, 16),
                               (110, 360, 240, LEAF_D, 17), (150, 300, 220, LEAF, 18)):   # the canopy round the hole
        a = math.radians(ang)
        clump(p, hx + math.cos(a) * 520, hy + math.sin(a) * 470, rx, ry, c, sd)
    for x, y, rx, ry, sd in ((150, 1500, 260, 200, 19), (560, 1700, 300, 190, 20), (980, 1580, 260, 200, 21),
                             (360, 1950, 340, 200, 22), (900, 1960, 320, 200, 23)):   # leaves at the trunks' feet
        clump(p, x, y, rx, ry, mix(LEAF_D, (36, 58, 34), 0.2), 600 + sd)


def _forest_up_open(img, p, cam, t):
    """S1 as built: blue sky, clouds, the canopy round the top, treetops low in the frame."""
    _sky(p, -400, 1500, 0.6)
    for x, y, w, sd in ((760, 380, 230, 1), (240, 640, 160, 2), (900, 900, 200, 3), (520, 1120, 150, 4)):
        _cloud(p, x + 6 * math.sin(t * 0.3 + sd), y, w, sd)
    for x, y, rx, ry, sd in ((-40, 1500, 340, 260, 5), (300, 1560, 300, 200, 6), (640, 1520, 320, 220, 7),
                             (1000, 1480, 320, 260, 8)):                # the far trees, low and hazy
        clump(p, x, y, rx, ry, mix(LEAF_L, SKY_LO, 0.22), sd, lw=2.4)   # pass 3: pale blobs read as clouds
    bark(p, [(1200, 2000), (1110, 900), (1000, -200)], 120, 50, mix(TRUNK, (150, 170, 150), 0.4), 29, None, 2)
    # (a far trunk leaning in to the top, pass 2: S1 read level)
    # the foot (first look: a flat sage block): treetops in rows, each nearer one greener and darker, a light shaft
    p.poly(quad(-200, 1700, W + 200, 2400), mix(LEAF, SKY_LO, 0.15), None)
    for k, x in enumerate((-60, 250, 560, 860, 1160)):                  # the middle row, a little hazy
        clump(p, x, 1700 + 50 * (k % 2), 210, 170, mix(LEAF_L, SKY_LO, 0.1), 30 + k, lw=2.6)
    shafts(img, cam, [[(560, 1300), (700, 1300), (900, 2000), (640, 2000)]], a=0.14)
    for k, x in enumerate((60, 420, 780, 1120)):                         # the near row, the nearest leaves
        clump(p, x, 1880 + 40 * (k % 2), 250, 190, LEAF if k % 2 else mix(LEAF, LEAF_L, 0.4), 36 + k)
    for x, y, rx, ry, c, sd in ((-80, 60, 420, 260, LEAF_D, 11), (330, -60, 360, 200, LEAF, 12),
                                (980, -40, 400, 260, LEAF_D, 13), (1160, 300, 220, 260, LEAF, 14),
                                (160, 210, 300, 170, LEAF, 15), (720, 90, 260, 150, LEAF_L, 16)):   # the canopy
        clump(p, x, y, rx, ry, c, sd)
    haze(img, cam, 1350, 1600, (236, 240, 236), 0.22)                   # mist among the far trees (ref 19)


def _forest_up_branch(img, p, cam, t):
    """S1's near things, every option: leaves over the boughs, the branch and its underside, the great trunk."""
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


def kg_on_branch(img, cam, x, s, mood='hype', wings='wide', t=0.0, sway=0.0, **kw):
    """KG perched on the S1/S3 branch (pass 2: his talons floated in front of it): his tail hangs BEHIND the branch,
    the branch is laid back over it, then his body sits on top with the toes curling over its front edge.
    sway: degrees he rocks about his toes on the branch (remakes note 44: he was frozen)."""
    import remakes_creatures as CR
    y = branch_y(x) - 236 * s - 4 * s                                    # his toe roots on the branch's top
    pivot = cam.P(x, branch_y(x))

    def rocked(lay):
        return lay.rotate(sway, center=pivot, resample=Image.BICUBIC) if sway else lay
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    CR.kg(lay, cam, x, y, s, view='front', perched=True, wings=wings, mood=mood, t=t, part='tail', **kw)
    lay = rocked(lay)
    m = Image.new('L', img.size, 255)
    ImageDraw.Draw(m).polygon([cam.P(*q) for q in branch_poly()], fill=0)
    a = lay.getchannel('A')
    lay.putalpha(Image.fromarray(np.minimum(np.asarray(a), np.asarray(m))))
    img.alpha_composite(lay)
    foot_shadow(img, cam, x, branch_y(x) + 14, 420.0, SHADOW_W['kg'], clip=branch_poly())
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    CR.kg(lay, cam, x, y, s, view='front', perched=True, wings=wings, mood=mood, t=t, part='body', **kw)
    img.alpha_composite(rocked(lay))


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


def _flag(p, xa, ya, xb, yb, seed, col):
    """One worn path stone (pass 3: the path read as even patio bricks): a rounded, uneven slab inside the box, its
    corners knocked off, a lit top edge."""
    rr = random.Random(seed)
    cx, cy, rx, ry = (xa + xb) / 2, (ya + yb) / 2, (xb - xa) / 2, (yb - ya) / 2
    n, a0 = rr.randint(5, 7), rr.uniform(0, 6.3)
    pts = []
    for k in range(n):
        a = a0 + 2 * math.pi * k / n + rr.uniform(-0.3, 0.3)
        f = rr.uniform(0.9, 1.04)
        pts.append((cx + math.cos(a) * rx * f, cy + math.sin(a) * ry * f))
    st = curve(pts, 3)
    p.poly(st, col, INK, 1.8)
    p.line(open_curve([(cx - rx * 0.6, cy - ry * 0.55), (cx, cy - ry * 0.72), (cx + rx * 0.5, cy - ry * 0.6)], 3),
           mix(col, (255, 255, 240), 0.35), 1.6)


def _flag_rows(p, edges, y0, y1, row_h, seed):
    """Irregular stones laid in loose rows between edges(y) -> (x0, x1): each row its own height, each stone its
    own width and offset, mossy gaps between, a stone missing here and there."""
    rr = random.Random(seed)
    y, row = y0, 0
    while y < y1:
        hgt = row_h(y) * rr.uniform(0.8, 1.25)
        x0, x1 = edges(y + hgt / 2)
        x = x0 - rr.uniform(0, 1) * hgt * 0.8
        while x < x1:
            sw = hgt * rr.uniform(1.1, 2.2)
            xa, xb = max(x, x0 + 2), min(x + sw, x1 - 2)
            if xb - xa > hgt * 0.45 and rr.random() > 0.04:
                g = hgt * rr.uniform(0.02, 0.05)
                c_ = mix(STONE, STONE_L, rr.uniform(0, 1)) if rr.random() > 0.3 else mix(STONE, STONE_D, 0.5)
                _flag(p, xa + g, y + g, xb - g, y + hgt - g, seed * 7 + row * 31 + int(x), mix(c_, MOSS, 0.2))
            x += sw
        y += hgt
        row += 1


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
    p.poly(left + right, mix(MOSS, GROUND_D, 0.45), INK, 2.6)        # mossy earth in the gaps
    _flag_rows(p, lambda y: (_path_x(y) - _path_w(y), _path_x(y) + _path_w(y)), PATH_TOP + 4, 2000,
               lambda y: down_ppm(y) * 0.42, 51)
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
    p.poly([(pl(y)[0], y) for y in ys] + [(pl(y)[1], y) for y in ys[::-1]], mix(MOSS, GROUND_D, 0.45), INK, 2.0)
    _flag_rows(p, pl, 1304, 2000, lambda y: 14 + (y - 1300) * 0.14, 52)    # the same worn stones as S2
    _stump_house(img, p, cam, 840, 1310, 620, 620, seed=STUMP_SEED)   # S2's stump, nearer (pass 2: it differed); on
    rr = random.Random(96)                                               # the grass, the path running to its door
    for k in range(26):
        y = rr.uniform(1320, 1900)
        x = rr.choice([rr.uniform(-20, pl(y)[0] - 10), rr.uniform(pl(y)[1] + 10, 1120)])
        tuft(p, x, y, 20 + (y - 1300) * 0.08, LEAF_D if k % 2 else MOSS_L, k + 300)
    rays = [[(160, -200), (330, -200), (640, 1700), (380, 1700)], [(560, -200), (650, -200), (990, 1500), (880, 1500)]]
    if OPT['shafts'] == 'dapple':                                       # option: no shafts; sun dapples on the
        rr2 = random.Random(77)                                         # grass, the stump and the path
        for k in range(16):
            x, y = rr2.uniform(0, 1080), rr2.uniform(1330, 1950)
            shafts(img, cam, [blob(x, y, 40 + (y - 1300) * 0.12, 12 + (y - 1300) * 0.03, 8, 0.3, k)], (255, 240, 170), 0.5)
        for x, y in ((700, 1000), (960, 860), (860, 1180)):
            shafts(img, cam, [blob(x, y, 50, 30, 8, 0.3, int(x))], (255, 240, 170), 0.45)
    elif OPT['shafts'] in ('strong', 'dark'):
        if OPT['shafts'] == 'dark':                                     # option: the wood darker round them, so
            haze(img, cam, -400, 2400, (34, 56, 34), 0.3)              # the light stands out
        shafts(img, cam, rays, col=(255, 240, 170), a=0.62)
        for x0, x1, y in ((380, 640, 1700), (880, 990, 1500)):          # where each shaft lands: a bright pool
            shafts(img, cam, [blob((x0 + x1) / 2, y, (x1 - x0) * 0.9, 40, 10, 0.2, int(x0))], (255, 244, 190), 0.55)
    else:
        shafts(img, cam, rays, col=(255, 244, 190), a=0.34)
    clump(p, -40, 1750, 300, 220, LEAF_D, 97)
    clump(p, 1120, 1840, 260, 180, LEAF, 98)
    _bell_flower(img, p, cam, 950, 1560, 46)     # pass 2: its glow showed but the flower hid behind the bush
    _purple_patch(p, 140, 1820, 160, 99, 8)


EDGE_LEAF, EDGE_LEAF_D, EDGE_SKY = (104, 124, 96), (70, 88, 66), (196, 206, 206)
EDGE_TRUNKS = ((470, 40, 8, 1330, 0.55), (760, 46, -10, 1345, 0.5), (180, 52, 12, 1360, 0.45), (980, 60, -14, 1380, 0.35),
               (620, 74, 10, 1420, 0.22), (300, 92, -20, 1470, 0.12), (40, 130, 30, 1560, 0.0), (1040, 120, -26, 1540, 0.0))
EDGE_OPTS = {   # rule 87 (S5: even poles, a grey forest unlike the rest): palette and trunks for each option
    'warm': dict(pal=((112, 150, 70), (74, 112, 50), (214, 222, 180)),
                 trunks=((560, 26, 4, 1320, 0.6), (850, 34, -6, 1330, 0.55), (700, 60, 14, 1350, 0.45),
                         (420, 44, -18, 1365, 0.4), (960, 96, -10, 1400, 0.28), (610, 150, 26, 1460, 0.15),
                         (1080, 260, -40, 1620, 0.0), (330, 70, 34, 1430, 0.25))),
    'mist': dict(pal=((118, 146, 96), (80, 108, 66), (226, 230, 206)),
                 trunks=((500, 22, 0, 1310, 0.75), (650, 28, 6, 1315, 0.72), (820, 30, -8, 1320, 0.7),
                         (930, 40, 10, 1330, 0.6), (400, 36, -10, 1335, 0.62), (720, 70, 18, 1380, 0.4),
                         (1000, 130, -22, 1450, 0.2), (1110, 300, -50, 1700, 0.0))),
}


def forest_edge(img, p, cam, t):
    """S5, the gunman's patch (ref 17): the same forest gone cooler and greyer where the soldiers creep: an
    overcast sky through the trees, thin dark trunks, ferns and long grass, a mossy rock."""
    global EDGE_LEAF, EDGE_LEAF_D, EDGE_SKY
    keep = (EDGE_LEAF, EDGE_LEAF_D, EDGE_SKY)
    trunks = EDGE_TRUNKS
    if OPT['edge'] in EDGE_OPTS:
        (EDGE_LEAF, EDGE_LEAF_D, EDGE_SKY), trunks = EDGE_OPTS[OPT['edge']]['pal'], EDGE_OPTS[OPT['edge']]['trunks']
    try:
        _forest_edge(img, p, cam, t, trunks)
    finally:
        EDGE_LEAF, EDGE_LEAF_D, EDGE_SKY = keep


def _forest_edge(img, p, cam, t, trunks):
    p.poly(quad(-200, -400, W + 200, 2400), EDGE_SKY, None)
    for k, (x, rx) in enumerate(((100, 320), (520, 300), (980, 330))):
        p.poly(blob(x, 560 + 60 * (k % 2), rx, 300, 12, 0.2, 110 + k), mix(EDGE_LEAF, EDGE_SKY, 0.4), INK, 2.0)
    EDGE_TRUNK = mix(TRUNK, EDGE_SKY, 0.25)                             # pass 1: the forest's own bark, gone grey
    p.poly(quad(-200, 1300, W + 200, 2400), (110, 124, 92), None)
    # gnarled trunks at staggered depths (pass 2: all in one row): far ones thin, pale and footed high, near ones
    # thick, darker, footed low; the far ones first
    if OPT['edge'] == 'mist':
        haze(img, cam, 600, 1400, EDGE_SKY, 0.35)
    for x, w, lean, foot, fade in sorted(trunks, key=lambda q: -q[4]):
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
    if view == 'up' and OPT['up'] == 'cap':
        _link_cap(img, cam, t)


def _link_cap(img, cam, t=0.0):
    """The back of Link's head and shoulders in the near corner looking up (ref 01), so KG towers over him. It is
    the cast's own Link seen from behind (note 30: a separate hand-drawn cap with loose hair spikes and a floating
    ear read as broken pieces; the real back view cannot come apart)."""
    import remakes_cast as RC
    sp = dict(RC.CAST['link'])
    s = s_for(1500.0)
    k = RC.scale_for(sp, s)
    RC.person(img, cam, 230, 3110 - 928 * k + 5 * math.sin(t * 1.3), s, sp, t, 180)


# ================================================================================================ the camp
CAMP = Level(h=1.6, hz=860.0, f=1100.0)   # pass 1: the horizon lower, less empty yard below the action
DIRT, DIRT_D, DIRT_L = (198, 166, 116), (170, 138, 92), (218, 192, 146)
TIN, TIN_D, TIN_L = (138, 142, 144), (108, 112, 116), (166, 168, 166)
RUST = (168, 96, 52)
PLANK, PLANK_D = (150, 112, 72), (112, 82, 52)
CONT_BLUE, CONT_ORANGE = (46, 96, 150), (214, 110, 40)
SAND, SAND_D = (186, 168, 120), (150, 132, 92)
FLAG_C = (40, 80, 150)            # pass 1: blue as ref 24's, an invented white mark
WALL_TINS = ((176, 150, 112), (150, 108, 72), (184, 176, 150), (128, 140, 100), (166, 124, 84))   # pass 2: warm
# bleached and rusted tin, faded green: the dark gunmen read against it (they were grey on grey)
WALL_D, WALL_H = 10.0, 2.6        # the back wall: depth and height (m)
GATE_HALF = 1.8                   # the gate opening's half width (m)
TOWER = (3.0, 9.0)
BARRELS = ((-1.4, 7.3, (60, 96, 70)), (-1.3, 6.4, (150, 60, 44)))   # x, d, colour                # the watchtower's middle (x, d), inside the wall on the right
CONTAINERS = {'blue container': (-5.0, -2.6, 7.4, 2.4), 'orange container': (-5.0, -2.6, 7.6, 2.2)}   # x0, x1, d, depth


def _tin_sheet(p, pts, col, seed, ribs=8, rust=True):
    """One corrugated sheet: the panel, its ribs, a rust streak or two."""
    p.poly(pts, col, INK, 2.2)
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
    if OPT['wall'] in ('tin', 'shelter') and ribs >= 8:                 # option (rule 87: it read as a plank
        n = ribs * 2                                                    # fence): deep corrugations, each a lit
        wv = abs(x1 - x0) / n                                           # and a shadowed stripe, the top edge
        for k in range(n):                                              # waved, bolt rows
            u0, u1 = k / n, (k + 0.5) / n
            q = lambda u, top: (x0 + (x1 - x0) * u, y0 + (y1 - y0) * u) if top else (x3 + (x2 - x3) * u, y3 + (y2 - y3) * u)
            p.poly([q(u0, 1), q(u1, 1), q(u1, 0), q(u0, 0)], mix(col, (255, 255, 255), 0.18), None)
            p.line([q(u1, 1), q(u1, 0)], dk(col, 0.7), 1.6)
            p.ell(q((u0 + u1) / 2, 1)[0], q((u0 + u1) / 2, 1)[1], wv * 0.5, wv * 0.3, mix(col, (255, 255, 255), 0.18),
                  INK, 1.2)
        for v in (0.08, 0.92):
            for k in range(0, n, 2):
                u = (k + 0.25) / n
                a, b = (x0 + (x1 - x0) * u, y0 + (y1 - y0) * u), (x3 + (x2 - x3) * u, y3 + (y2 - y3) * u)
                p.ell(a[0] + (b[0] - a[0]) * v, a[1] + (b[1] - a[1]) * v, 2.4, 2.4, (70, 66, 62), None)
        p.poly(pts, None, INK, 2.2)
    else:
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


def _lean_to(p):
    """Option (rule 87: no middle layer, no shacks): an open tin lean-to over the crates and barrels on the left, two
    rough posts at its front, its corrugated roof sloping down to us."""
    x0, x1, df, db = -2.75, -0.85, 6.0, 7.3
    for x in (x0, x1):
        a, b = CAMP.p(x, df, 0), CAMP.p(x, df, 2.25)
        p.poly(wob(quad(a[0] - 7, b[1], a[0] + 7, a[1]), 1.5, int(x * 10)), PLANK_D, INK, 2.0)
    roof = [CAMP.p(x0 - 0.15, db, 2.7), CAMP.p(x1 + 0.15, db, 2.7), CAMP.p(x1 + 0.15, df - 0.2, 2.2),
            CAMP.p(x0 - 0.15, df - 0.2, 2.2)]
    _tin_sheet(p, roof, TIN_L, 701, 10)
    p.line([CAMP.p(x0 - 0.15, df - 0.2, 2.2), CAMP.p(x1 + 0.15, df - 0.2, 2.2)], PLANK_D, 5.0)   # the front beam


def _wire(p, x0, x1, y, r):
    """A coil of barbed wire along a wall top, on short iron posts (pass 2: a hairline)."""
    xp = x0
    while xp < x1:                                                       # the posts, one each metre or so
        p.line([(xp, y + 2), (xp + 3, y - r * 2.6)], (56, 50, 46), 4.0)
        xp += r * 7
    x = x0
    while x < x1:
        p.ell(x, y - r * 1.1, r, r * 1.0, None, (44, 44, 44), 3.6)
        p.ell(x + r * 0.6, y - r * 1.2, r * 0.8, r * 0.85, None, (70, 70, 70), 2.2)
        for dx, dy in ((-0.3, -2.0), (0.4, -0.15)):                     # barbs
            p.line([(x + r * dx - 5, y + r * dy - 3), (x + r * dx + 5, y + r * dy + 3)], (44, 44, 44), 2.6)
        x += r * 1.25


def _gate_fallen(p):
    """The right gate leaf blown off its hinges (pass 3: both leaves stood whole): lying flat in the yard just inside
    the gateway, skewed, its planks splintered at the far end, the top hinge strap torn loose on the post."""
    pts = [(0.3, WALL_D - 0.7), (2.2, WALL_D - 0.35), (2.05, WALL_D - 2.7), (0.2, WALL_D - 2.95)]
    sc = [CAMP.p(x, d, 0.06) for x, d in pts]
    p.poly(sc, PLANK, INK, 2.6)
    for u in (0.25, 0.5, 0.75):
        p.line([(sc[0][0] + (sc[1][0] - sc[0][0]) * u, sc[0][1] + (sc[1][1] - sc[0][1]) * u),
                (sc[3][0] + (sc[2][0] - sc[3][0]) * u, sc[3][1] + (sc[2][1] - sc[3][1]) * u)], PLANK_D, 1.8)
    for k in range(5):                                                  # the splintered far end: jagged points
        u0, u1 = k / 5, (k + 1) / 5
        a = (sc[0][0] + (sc[1][0] - sc[0][0]) * u0, sc[0][1] + (sc[1][1] - sc[0][1]) * u0)
        b = (sc[0][0] + (sc[1][0] - sc[0][0]) * u1, sc[0][1] + (sc[1][1] - sc[0][1]) * u1)
        p.poly([a, ((a[0] + b[0]) / 2 + 4, (a[1] + b[1]) / 2 - 14 - 8 * (k % 2)), b], PLANK, INK, 1.6)
    p.poly([(sc[3][0] + (sc[2][0] - sc[3][0]) * 0.15, sc[3][1] + (sc[2][1] - sc[3][1]) * 0.15 - 30),
            (sc[3][0] + (sc[2][0] - sc[3][0]) * 0.85, sc[3][1] + (sc[2][1] - sc[3][1]) * 0.85 - 30),
            (sc[3][0] + (sc[2][0] - sc[3][0]) * 0.85, sc[3][1] + (sc[2][1] - sc[3][1]) * 0.85 - 14),
            (sc[3][0] + (sc[2][0] - sc[3][0]) * 0.15, sc[3][1] + (sc[2][1] - sc[3][1]) * 0.15 - 14)], PLANK_D, INK, 1.6)
    h0 = CAMP.p(GATE_HALF - 0.1, WALL_D, 1.9)                           # the torn hinge strap on the post
    p.line([h0, (h0[0] - 22, h0[1] + 18)], (62, 56, 54), 5.0)


def _gate_debris(p):
    """Splintered planks and chips flung into the yard by the blast (pass 3)."""
    rr = random.Random(271)
    for k in range(14):
        d = rr.uniform(6.0, 9.4)
        x = rr.uniform(-2.4, 2.6)
        q = CAMP.p(x, d, 0)
        u = CAMP.ppm(d)
        a = rr.uniform(-0.6, 0.6)
        ln = u * rr.uniform(0.15, 0.5)
        w_ = u * rr.uniform(0.03, 0.06)
        c, s_ = math.cos(a), math.sin(a)
        p.poly([(q[0] - c * ln / 2, q[1] - s_ * ln / 2 * 0.3), (q[0] + c * ln / 2, q[1] + s_ * ln / 2 * 0.3 - w_ * 0.4),
                (q[0] + c * ln / 2 - 4, q[1] + s_ * ln / 2 * 0.3 + w_), (q[0] - c * ln / 2, q[1] - s_ * ln / 2 * 0.3 + w_)],
               PLANK if k % 2 else PLANK_D, INK, 1.2)


def _gate_leaf(p, hinge_x, side, k, d=WALL_D, broken=False):
    """One gate leaf hinged at hinge_x (m), swinging in towards the lens by k (0 shut, 1 blown flat open); broken:
    its free end blasted into splinters (pass 3)."""
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
    if broken:                                                          # the free end shattered: a jagged bite out
        bite = [m(1.0, 0.05), m(0.78, 0.18), m(0.9, 0.3), m(0.7, 0.42), m(0.86, 0.55), m(0.74, 0.7), m(1.0, 0.8)]
        p.poly(bite, (52, 40, 30), INK, 1.8)


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
    bw, bh = 0.75 * ppm, 0.3 * ppm                                      # pass 2: they read as pebbles
    r = random.Random(seed)
    base = CAMP.p(0, d, 0)[1]
    for row in range(rows):
        y = base - bh * (row + 0.5)
        x = CAMP.p(x0, d)[0] + (row % 2) * bw * 0.5
        xe = CAMP.p(x1, d)[0]
        while x < xe - bw * 0.3:
            c = SAND if r.random() > 0.3 else mix(SAND, SAND_D, 0.5)
            p.poly(curve([(x + bw * 0.05, y - bh * 0.1), (x + bw * 0.15, y - bh * 0.48), (x + bw * 0.5, y - bh * 0.55),
                          (x + bw * 0.85, y - bh * 0.48), (x + bw * 0.97, y - bh * 0.1), (x + bw * 0.88, y + bh * 0.45),
                          (x + bw * 0.5, y + bh * 0.52), (x + bw * 0.12, y + bh * 0.45)], 4), c, INK, 2.2)   # a pillow
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


def _tower_box(p):
    """The watchtower's plank platform box (drawn again over the cast: the lookout stands in it, waist deep)."""
    tx, td = TOWER
    pa, pb = CAMP.p(tx - 1.1, td, 4.4), CAMP.p(tx + 1.1, td, 5.05)   # pass 3: lower, the lookout read as a smudge
    p.poly(quad(pa[0], pb[1], pb[0], pa[1]), PLANK, INK, 2.4)
    for u in np.linspace(0.1, 0.9, 7):                                 # planks (pass 1: a blank box)
        p.line([(pa[0] + (pb[0] - pa[0]) * u, pb[1] + 3), (pa[0] + (pb[0] - pa[0]) * u, pa[1] - 3)], PLANK_D, 2.0)
    p.poly(quad(pa[0] + (pb[0] - pa[0]) * 0.3, pb[1] + 10, pa[0] + (pb[0] - pa[0]) * 0.7, pb[1] + 26), (40, 34, 30),
           INK, 1.6)


def _camo_net(p, x0, x1, d, z0, z1, seed):
    """A camouflage net hung over the wall (pass 2: the right wall was blank): a sagging mesh, leaf scraps tied in."""
    r = random.Random(seed)
    top = [CAMP.p(x0 + (x1 - x0) * u, d - 0.05, z1 - 0.25 * math.sin(u * math.pi * 2) ** 2) for u in np.linspace(0, 1, 9)]
    hem = [CAMP.p(x0 + (x1 - x0) * u, d - 0.05, z0 + 0.3 * r.random()) for u in np.linspace(1, 0, 9)]
    p.poly(top + hem, (92, 104, 70), INK, 2.2)
    for k in range(26):                                                 # the leaf scraps
        u, v = r.random(), r.uniform(0.1, 0.9)
        q = CAMP.p(x0 + (x1 - x0) * u, d - 0.05, z0 + (z1 - z0) * v)
        rr_ = CAMP.ppm(d) * r.uniform(0.08, 0.14)
        p.poly(blob(q[0], q[1], rr_, rr_ * 0.7, 6, 0.3, seed + k), r.choice(((70, 84, 52), (126, 118, 76), (60, 70, 44))),
               None)
    for u in np.linspace(0.05, 0.95, 8):                                # the mesh cords
        a, b = CAMP.p(x0 + (x1 - x0) * u, d - 0.05, z1), CAMP.p(x0 + (x1 - x0) * (u + 0.06), d - 0.05, z0 + 0.2)
        p.line([a, b], (60, 66, 46), 1.4)


def _tyres(p, x, d, n=3):
    """A stack of old tyres."""
    u = CAMP.ppm(d)
    for k in range(n):
        q = CAMP.p(x, d, 0.24 * k)
        p.poly(quad(q[0] - u * 0.36, q[1] - u * 0.24, q[0] + u * 0.36, q[1]), (44, 44, 44), INK, 2.0)
        p.ell(q[0], q[1] - u * 0.24, u * 0.36, u * 0.1, (36, 36, 36), INK, 2.0)
        p.ell(q[0], q[1] - u * 0.24, u * 0.18, u * 0.05, DIRT_D, None)


def _near_yard(p):
    """The yard nearest the lens (pass 2: still empty dirt at the foot): an open ammo box spilling a belt, spent cases,
    boot prints along the ruts, a shallow puddle with the sky in it, a broken pallet, weeds."""
    r = random.Random(294)
    for k in range(4):                                                  # weeds, clear of the box and pallet
        d = r.uniform(2.4, 2.9)
        wq = CAMP.p(r.choice((-1, 1)) * r.uniform(0.25, 0.5), d, 0)
        tuft(p, wq[0], wq[1], 0.2 * CAMP.ppm(d), (120, 136, 72), 296 + k, 7, 2.4)
    q = CAMP.p(-0.62, 2.3, 0)                                           # the ammo box, bottom left (pass 3: it
    u = CAMP.ppm(2.3) * 0.55                                            # was bigger than Link: now a real 0.33 m can)
    p.poly(quad(q[0] - u * 0.3, q[1] - u * 0.2, q[0] + u * 0.3, q[1]), (88, 98, 62), INK, 2.4)
    p.poly([(q[0] - u * 0.3, q[1] - u * 0.2), (q[0] + u * 0.3, q[1] - u * 0.2), (q[0] + u * 0.36, q[1] - u * 0.36),
            (q[0] - u * 0.24, q[1] - u * 0.36)], (70, 80, 50), INK, 2.0)  # its lid, flipped open
    p.poly(quad(q[0] - u * 0.06, q[1] - u * 0.14, q[0] + u * 0.06, q[1] - u * 0.1), (200, 190, 150), INK, 1.2)   # stencil
    # the belt (pass 3: a stiff rod): over the box's rim, sagging down its side and snaking off over the dirt
    belt = open_curve([(q[0] + u * 0.1, q[1] - u * 0.2), (q[0] + u * 0.3, q[1] - u * 0.22), (q[0] + u * 0.4, q[1] - u * 0.06),
                       (q[0] + u * 0.5, q[1] + u * 0.02), (q[0] + u * 0.72, q[1] - u * 0.03), (q[0] + u * 0.9, q[1] + u * 0.05),
                       (q[0] + u * 1.1, q[1] + u * 0.02), (q[0] + u * 1.3, q[1] + u * 0.08)], 5)
    p.poly(ribbon(belt, u * 0.05, u * 0.05), (58, 54, 44), INK, 1.2)
    for k, (bx, by) in enumerate(belt[::2]):                            # its rounds
        p.poly(quad(bx - u * 0.018, by - u * 0.07, bx + u * 0.018, by - u * 0.01), (206, 160, 60), INK, 1.0)
    q2 = CAMP.p(0.42, 2.35, 0)                                          # a shallow puddle, the sky in it
    u2 = CAMP.ppm(2.35)
    # pass 3: a scalloped pale blob read as a cloud on the ground: now dark muddy water with a smooth uneven edge,
    # a wet rim, a streak of sky in it
    rr2 = random.Random(291)
    edge = [(q2[0] + math.cos(a) * u2 * 0.42 * rr2.uniform(0.8, 1.0), q2[1] + math.sin(a) * u2 * 0.1 * rr2.uniform(0.75, 1.0))
            for a in np.linspace(0, 2 * math.pi, 9)[:-1]]
    p.poly(curve([(x_ + (x_ - q2[0]) * 0.12, y_ + (y_ - q2[1]) * 0.35) for x_, y_ in edge], 4), dk(DIRT, 0.8), None)
    p.poly(curve(edge, 4), (122, 134, 132), INK, 1.6)
    p.line(open_curve([(q2[0] - u2 * 0.24, q2[1] - u2 * 0.02), (q2[0] - u2 * 0.02, q2[1] - u2 * 0.035),
                       (q2[0] + u2 * 0.2, q2[1] - u2 * 0.01)], 3), (176, 200, 220), max(3.0, u2 * 0.02))
    for k in range(7):                                                  # boot prints along the left rut
        d = 1.9 + 0.55 * k
        bq = CAMP.p(-0.35 + 0.12 * (k % 2), d, 0)
        bu = CAMP.ppm(d)
        p.ell(bq[0], bq[1], bu * 0.06, bu * 0.025, dk(DIRT, 0.86), None)
        p.ell(bq[0], bq[1] - bu * 0.045, bu * 0.05, bu * 0.02, dk(DIRT, 0.86), None)
    pq = CAMP.p(1.15, 2.2, 0)                                           # a broken pallet, bottom right
    pu = CAMP.ppm(2.2)
    for k in range(4):
        yy = pq[1] - pu * 0.12 * k
        p.poly(wob(quad(pq[0] - pu * 0.45 + k * 6, yy - pu * 0.08, pq[0] + pu * (0.45 - 0.08 * (k == 2)), yy), 2, 293 + k),
               PLANK if k % 2 else PLANK_D, INK, 1.8)
    for k in range(12):                                                 # spent cases
        d = r.uniform(1.8, 2.8)
        cq = CAMP.p(r.uniform(-0.5, 0.9), d, 0)
        cu = CAMP.ppm(d)
        a = r.uniform(0, math.pi)
        p.poly(ribbon([(cq[0], cq[1]), (cq[0] + math.cos(a) * cu * 0.03, cq[1] + math.sin(a) * cu * 0.01)], cu * 0.01,
                      cu * 0.009), (206, 160, 60), INK, 0.8)


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
    p.poly(blob(1500, 800, 600, 200, 14, 0.12, 205), mix(LEAF_D, SKY_LO, 0.4), INK, 2.0)  # (note 67: wider)
    for k, (x, rx, ry) in enumerate(((60, 220, 210), (330, 200, 180), (700, 210, 200), (1010, 230, 220),
                                     (1300, 220, 200), (1560, 240, 220), (1820, 220, 200))):
        clump(p, x, 700 - 40 * (k % 2), rx, ry, LEAF if k % 2 else LEAF_D, 210 + k)
    for x, h, sd, lean in ((300, 520, 221, -0.06), (580, 640, 222, 0.14), (900, 420, 223, -0.22),
                           (1480, 560, 224, 0.1)):                      # pass 2: one
                                                                        # grew out of the orange container
        _palm(p, x, 760, h, sd, lean=lean)
    p.poly(quad(-200, 760, W + 900, 2400), DIRT, None)                  # the yard
    # the flag and the watchtower stand behind the wall's line, drawn before it
    fp0, fp1 = CAMP.p(-0.6, 12.0, 0), CAMP.p(-0.6, 12.0, 7.0)
    p.line([fp0, fp1], (70, 70, 70), 4.0)
    wave = [(fp1[0] + 16 * k, fp1[1] + 8 * math.sin(t * 6 + k * 0.9)) for k in range(9)]
    p.poly(wave + [(x, y + 80) for x, y in wave[::-1]], FLAG_C, INK, 2.0)   # an invented flag: black, a white band
    p.poly([wave[2], wave[4], (wave[6][0], wave[6][1] + 80), (wave[4][0], wave[4][1] + 80)], (236, 232, 220), None)
    # the back wall, sheet by sheet, the gate's posts and the opening
    x = -6.0
    k = 0
    while x < 11.0:                                                     # (to 11 m: remakes note 67's camp pan)
        if abs(x + 0.5) < GATE_HALF + 0.5:
            x += 1.0
            continue
        a, b = CAMP.p(x, WALL_D, 0), CAMP.p(x + 1.0, WALL_D, WALL_H + 0.15 * math.sin(k * 2.1))
        _tin_sheet(p, quad(a[0], b[1], b[0], a[1]), WALL_TINS[k % 5], 240 + k)
        x += 1.0
        k += 1
    o0, o1 = CAMP.p(-GATE_HALF, WALL_D + 0.05, 0), CAMP.p(GATE_HALF, WALL_D + 0.05, 2.4)
    p.poly(quad(o0[0], o1[1], o1[0], o0[1]), (62, 92, 54), INK, 2.0)  # through the gate (pass 3: a blank olive
    gy = o0[1] - (o0[1] - o1[1]) * 0.42                                 # block): the jungle beyond, its undergrowth,
    p.poly([(o0[0], gy)] + [(o0[0] + (o1[0] - o0[0]) * u_, gy + 10 * math.sin(u_ * 9))
            for u_ in np.linspace(0, 1, 10)] + [(o1[0], o0[1]), (o0[0], o0[1])], (96, 128, 66), None)   # and the track
    for u_ in (0.15, 0.4, 0.7, 0.9):                                    # running out into it
        p.poly(blob(o0[0] + (o1[0] - o0[0]) * u_, gy - 10, 26, 18, 7, 0.3, int(u_ * 40)), (78, 110, 58), None)
    ta, tb = CAMP.p(-0.9, WALL_D + 0.05, 0), CAMP.p(0.9, WALL_D + 0.05, 0)
    tf = CAMP.p(0.3, 40.0, 0)
    ym = o0[1] - (o0[1] - gy) * 0.7                                     # remakes Fable r3 #46: the track bends away
    p.poly([ta, tb, (tf[0] + 90, ym), (tf[0] + 20, ym)], DIRT_D, None)  # into the trees (a point read as a pyramid)
    p.poly(blob(tf[0] + 55, ym - 4, 70, 16, 7, 0.3, 77), (78, 110, 58), None)
    for sx in (-1, 1):                                                  # the gate posts
        q0, q1 = CAMP.p(sx * GATE_HALF - 0.12, WALL_D, 0), CAMP.p(sx * GATE_HALF + 0.12, WALL_D, 2.9)
        p.poly(quad(q0[0], q1[1], q1[0], q0[1]), PLANK_D, INK, 2.4)
    for sx in (-1, 1):
        if gate >= 1.0 and sx > 0:
            _gate_fallen(p)                                             # pass 3: blown in, one leaf off its hinges
        else:
            _gate_leaf(p, sx * GATE_HALF, sx, gate, broken=gate >= 1.0)
    if gate >= 1.0:
        _gate_debris(p)
    _wire(p, CAMP.p(-6, WALL_D)[0], CAMP.p(-GATE_HALF - 0.2, WALL_D)[0], CAMP.p(0, WALL_D, WALL_H)[1], 16)
    _wire(p, CAMP.p(GATE_HALF + 0.2, WALL_D)[0], CAMP.p(6, WALL_D)[0], CAMP.p(0, WALL_D, WALL_H)[1], 16)
    _camo_net(p, 3.7, 6.2, WALL_D, 0.3, 2.4, 255)                     # over the right wall (pass 2: blank)
    _tyres(p, 4.7, 9.3, 3)
    # the watchtower (inside, right): four legs, cross braces, a plank platform, a tin roof, a ladder
    tx, td = TOWER
    for lx in (tx - 0.9, tx + 0.9):
        a, b = CAMP.p(lx, td, 0), CAMP.p(lx + (0.25 if lx < tx else -0.25), td, 4.5)
        p.poly([(a[0] - 6, a[1]), (a[0] + 6, a[1]), (b[0] + 6, b[1]), (b[0] - 6, b[1])], PLANK_D, INK, 2.0)
    for z0, z1 in ((0.4, 2.4), (2.4, 4.4)):
        p.line([CAMP.p(tx - 0.85, td, z0), CAMP.p(tx + 0.75, td, z1)], PLANK_D, 3.0)
        p.line([CAMP.p(tx + 0.85, td, z0), CAMP.p(tx - 0.75, td, z1)], PLANK_D, 3.0)
    _tower_box(p)
    for lx in (tx - 1.0, tx + 1.0):                                     # the roof posts (pass 1: the roof floated)
        a_, b_ = CAMP.p(lx, td, 5.4), CAMP.p(lx, td, 6.3)
        p.poly(quad(a_[0] - 5, b_[1], a_[0] + 5, a_[1]), PLANK_D, INK, 1.8)
    p.line([CAMP.p(tx - 1.1, td, 5.75), CAMP.p(tx + 1.1, td, 5.75)], PLANK_D, 3.0)   # the rail
    ra, rb = CAMP.p(tx - 1.4, td, 6.2), CAMP.p(tx + 1.4, td, 6.2)
    rt = CAMP.p(tx, td, 6.9)
    _tin_sheet(p, [(ra[0], rb[1]), (rb[0], rb[1]), (rb[0] - 20, rt[1]), (ra[0] + 20, rt[1])][::1], TIN_D, 251, 6)
    # the yard floor: tyre ruts from the gate, stones, a dark patch, weeds at the wall's foot
    for sx in (-1, 1):
        rut = [CAMP.p(sx * 0.8 - 0.1, WALL_D, 0), CAMP.p(sx * 0.8 + 0.1, WALL_D, 0), CAMP.p(sx * 0.95 + 0.1, 1.0, 0),
               CAMP.p(sx * 0.95 - 0.1, 1.0, 0)]                           # tyre ruts (pass 2: far too wide)
        p.poly(rut, DIRT_D, None)
        for kk in range(14):                                            # tread marks across each
            d = 1.2 + kk ** 1.35 * 0.32
            if d > WALL_D:
                break
            xm = sx * (0.95 + (0.8 - 0.95) * (d - 1.0) / (WALL_D - 1.0))
            p.line([CAMP.p(xm - 0.1, d, 0), CAMP.p(xm + 0.1, d, 0)], dk(DIRT_D, 0.85), 1.6)
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
    _near_yard(p)
    # containers (left), the orange one stacked on the blue (ref 23), both inside the wall; crates and barrels
    _container(p, *CONTAINERS['blue container'], CONT_BLUE, 281)
    _container(p, *CONTAINERS['orange container'], CONT_ORANGE, 282, z0=2.6)
    _crate(p, -2.2, 6.6, 0.9, 0, 283)
    _crate(p, -2.15, 6.6, 0.7, 0.9, 284)
    for bx, bd, bc in BARRELS:                                          # pass 2: KG hid them; now left of Link
        _barrel(p, bx, bd, bc)
    if OPT['wall'] == 'shelter':
        _lean_to(p)
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
    _tower_box(p)                                                       # the lookout stands in it, waist deep
    _sandbags(p, 1.25, 2.4, 3.4, 2, 302)                               # a low emplacement, the bottom right corner


# ================================================================================================ Castle Town
TOWN = Level(h=2.4, hz=600.0, f=1100.0)   # build chat 8: raised, so KG stands below the line-up, not over it
PLASTER = [(236, 224, 196), (240, 216, 176), (232, 206, 196), (226, 226, 210), (226, 190, 180)]
BEAM, ROOF, ROOF_D = (98, 66, 44), (196, 92, 56), (156, 68, 42)
ROOFS = [(196, 92, 56), (178, 76, 52), (206, 110, 66), (150, 84, 70)]
BANNER, BANNER_D, GOLD = (86, 126, 190), (56, 88, 150), (226, 186, 70)     # pass 2: pale blue, gold frame (ref 22)
WALLSTONE, WALLSTONE_D, WALLSTONE_L, MORTAR = (170, 168, 162), (136, 134, 130), (196, 194, 186), (104, 100, 96)
FLAG, FLAG_D, FLAG_L, FLAG_J = (150, 156, 168), (118, 124, 138), (176, 182, 192), (88, 92, 104)
CASTLE = (196, 206, 222)
TENT_R = (198, 54, 50)


def _flagstones(p, lev, d_far, seed, slab_d=0.55, slab_w=(0.5, 1.05)):
    """Grey-blue paving slabs (refs 21, 22) in true perspective: the side joints run to the vanishing point and the
    rows shrink with distance (pass 2: oval cobbles that did not shrink)."""
    d_near = lev.d_at(H + 80)
    y_far = lev.p(0, d_far)[1]
    p.poly(quad(-300, y_far, W + 300, H + 300), mix(FLAG, FLAG_D, 0.5), None)
    rr = random.Random(seed)
    d = d_near
    while d < d_far:
        da, db = min(d_far, d + slab_d * rr.uniform(0.85, 1.15)), d
        ya, yb = lev.p(0, da)[1], lev.p(0, db)[1]
        lw = max(0.8, min(2.8, (yb - ya) * 0.05))
        x = (-300 - lev.cx) * da / lev.f - rr.uniform(0, 0.9)
        x_hi = (W + 300 - lev.cx) * da / lev.f
        while x < x_hi:
            w = rr.uniform(*slab_w)
            c = rr.choice([FLAG, FLAG, FLAG_L, mix(FLAG, FLAG_D, 0.4), mix(FLAG, (168, 158, 146), 0.45)])
            p.poly([lev.p(x, da), lev.p(x + w, da), lev.p(x + w, db), lev.p(x, db)], c, FLAG_J, lw)
            if yb - ya > 26 and rr.random() < 0.25:                    # a worn chip or crack on the near slabs
                cx_, cy_ = lev.p(x + w * rr.uniform(0.3, 0.7), db + (da - db) * rr.uniform(0.3, 0.7))
                p.line([(cx_ - (yb - ya) * 0.3, cy_), (cx_, cy_ + (yb - ya) * 0.12), (cx_ + (yb - ya) * 0.25, cy_ - 3)],
                       FLAG_J, 1.4)
            x += w
        d = da


def _house(img, p, x0, x1, base, top, roof_h, col, seed, floors=3, wins=2, roof='gable', stone=False, frame='brace',
           jetty=False, balcony=False, sign=None, chimney=False, shut=None):
    """A Castle Town house front (ref 21): plaster in dark timber framing, shuttered windows, a door, a tiled roof.
    Pass 2: each house its own build (floors, windows, roof shape, stone or plaster ground floor, jetty, framing,
    balcony, shop sign, chimney), not one repeated block."""
    r = random.Random(seed)
    w = x1 - x0
    fl = (base - top) / floors
    ov = w * 0.05 if jetty else 0.0                                     # the jettied upper floors stand out
    rc = ROOFS[seed % len(ROOFS)]
    cx = (x0 + x1) / 2
    ux0, ux1 = x0 - ov, x1 + ov
    if roof == 'gable':
        rpts = [(ux0 - w * 0.06, top + 4), (cx, top - roof_h), (ux1 + w * 0.06, top + 4)]
    elif roof == 'side':
        rpts = [(ux0 - w * 0.06, top + 4), (ux0 + w * 0.1, top - roof_h * 0.6), (ux1 - w * 0.1, top - roof_h * 0.6),
                (ux1 + w * 0.06, top + 4)]
    else:                                                               # 'tower': a tall pointed spire
        rpts = [(ux0 - w * 0.08, top + 4), (cx, top - roof_h * 1.6), (ux1 + w * 0.08, top + 4)]
    if chimney:
        chx = cx + w * (0.22 if seed % 2 else -0.22)
        p.poly(quad(chx - w * 0.05, top - roof_h * 0.75, chx + w * 0.05, top - roof_h * 0.2), (150, 100, 80), INK, 2.0)
        p.poly(quad(chx - w * 0.065, top - roof_h * 0.8, chx + w * 0.065, top - roof_h * 0.72), (120, 80, 64), INK, 1.6)
    p.poly(rpts, rc, INK, 2.6)
    ytop = min(q[1] for q in rpts)
    for k in range(1, 6):                                               # tile rows, each a run of small scallops
        yy = top + 4 - (top + 4 - ytop) * k / 6
        xs_ = [q[0] for q in rpts]
        # where the roof's sides cross this row
        lft = ux0 - w * 0.06 + (cx - ux0) * (k / 6) * (1 if roof != 'side' else 0.6)
        rgt = ux1 + w * 0.06 - (ux1 - cx) * (k / 6) * (1 if roof != 'side' else 0.6)
        if rgt - lft < 8:
            continue
        p.line([(lft, yy), (rgt, yy)], dk(rc, 0.78), 1.5)
        n = max(2, int((rgt - lft) / 14))
        for i in range(n):
            xx = lft + (rgt - lft) * (i + (k % 2) * 0.5) / n
            if lft < xx < rgt:
                p.line([(xx, yy), (xx, yy + (top + 4 - ytop) / 6 * 0.8)], dk(rc, 0.85), 1.0)
    if roof == 'gable':                                                 # a round attic window in the gable
        p.ell(cx, top - roof_h * 0.35, w * 0.06, w * 0.06, (70, 90, 120), INK, 1.8)
    if roof == 'side' and w > 160:                                      # a dormer
        p.poly([(cx - w * 0.1, top - roof_h * 0.12), (cx - w * 0.1, top - roof_h * 0.42), (cx, top - roof_h * 0.6),
                (cx + w * 0.1, top - roof_h * 0.42), (cx + w * 0.1, top - roof_h * 0.12)], col, INK, 2.0)
        p.poly(quad(cx - w * 0.05, top - roof_h * 0.4, cx + w * 0.05, top - roof_h * 0.16), (70, 90, 120), INK, 1.6)
    # the walls: the ground floor (stone or plaster), the upper floors (jettied over it)
    p.poly(quad(ux0, top, ux1, base - fl), col, INK, 2.6)
    gcol = WALLSTONE_D if stone else col
    p.poly(quad(x0, base - fl, x1, base), gcol, INK, 2.6)
    if stone:                                   # pass 3: the S12 wall's own rough grey blocks (it was like nothing
        for rw in range(3):                     # in the square): uneven widths, a lit top edge, mortar between
            yy = base - fl + fl * rw / 3
            xx = x0 - r.uniform(0, 1) * fl * 0.5
            while xx < x1:
                bw = fl / 3 * r.uniform(1.3, 2.4)
                a_, b_ = max(xx, x0) + 1.5, min(xx + bw, x1) - 1.5
                if b_ - a_ > 4:
                    c_ = mix(WALLSTONE, WALLSTONE_L, r.uniform(0, 0.5))
                    p.poly(wob(quad(a_, yy + 1.5, b_, yy + fl / 3 - 1.5), 1.2, int(xx * 7) + seed, 10), c_, INK, 1.2)
                    p.line([(a_ + 2, yy + 3.5), (b_ - 2, yy + 3.5)], mix(c_, WALLSTONE_L, 0.7), 1.4)
                xx += bw
    if jetty:
        p.poly(quad(ux0, base - fl - 6, ux1, base - fl + 4), BEAM, INK, 1.8)
        for k in range(6):                                              # the joist ends under the jetty
            xx = ux0 + (ux1 - ux0) * (k + 0.5) / 6
            p.poly(quad(xx - 3, base - fl + 4, xx + 3, base - fl + 10), BEAM, None)
    for k in range(1, floors - 1):                                      # the timber frame on the upper floors
        p.line([(ux0, top + fl * k), (ux1, top + fl * k)], BEAM, 6.0)
    if frame:
        for u in (0.02, 0.5, 0.98):
            p.line([(ux0 + (ux1 - ux0) * u, top), (ux0 + (ux1 - ux0) * u, base - fl)], BEAM, 5.0)
        for k in range(floors - 1):
            ya_, yb_ = top + fl * k, top + fl * (k + 1)
            if frame == 'brace':
                p.line([(ux0, yb_), (ux0 + w * 0.2, ya_)], BEAM, 4.0)
                p.line([(ux1, yb_), (ux1 - w * 0.2, ya_)], BEAM, 4.0)
            elif frame == 'x':
                m = (ux0 + ux1) / 2
                for xa, xb in ((ux0, m), (m, ux1)):
                    p.line([(xa, ya_), (xb, yb_)], BEAM, 3.6)
                    p.line([(xa, yb_), (xb, ya_)], BEAM, 3.6)
            elif frame == 'studs':
                for kk in range(1, 6):
                    xx = ux0 + (ux1 - ux0) * kk / 6
                    p.line([(xx, ya_), (xx, yb_)], BEAM, 3.0)
    sc = shut or r.choice([(70, 120, 90), (60, 90, 140), (150, 60, 50), (120, 90, 60)])
    for row in range(floors - 1):                                       # upper windows
        for i in range(wins):
            u = (i + 0.5) / wins
            wx, wy = ux0 + (ux1 - ux0) * u, top + fl * (row + 0.48)
            ww, wh = min(w * 0.1, 0.32 * w / wins), fl * 0.42
            arch = seed % 3 == 0
            pts = (curve([(wx - ww, wy + wh / 2), (wx - ww, wy - wh * 0.2), (wx, wy - wh / 2 - ww * 0.4),
                          (wx + ww, wy - wh * 0.2), (wx + ww, wy + wh / 2)], 2) if arch else
                   quad(wx - ww, wy - wh / 2, wx + ww, wy + wh / 2))
            p.poly(pts, (70, 90, 120), INK, 2.0)
            p.line([(wx, wy - wh / 2), (wx, wy + wh / 2)], BEAM, 1.6)
            for sg in (-1, 1):
                p.poly(quad(wx + sg * ww, wy - wh / 2, wx + sg * ww * 1.7, wy + wh / 2), sc, INK, 1.8)
            if (row + i + seed) % 2 == 0:                               # a flower box under some
                p.poly(quad(wx - ww * 1.1, wy + wh / 2, wx + ww * 1.1, wy + wh / 2 + fl * 0.09), BEAM, INK, 1.6)
                for kk in range(4):
                    p.ell(wx - ww + ww * 0.66 * kk, wy + wh / 2 - 3, ww * 0.24, ww * 0.2,
                          (210, 50, 60) if kk % 2 else (150, 80, 180), INK, 1.2)
    dx = x0 + w * (0.3 if seed % 2 else 0.7)                            # the door, arched
    dw = min(w * 0.12, 30)
    p.poly(curve([(dx - dw, base), (dx - dw, base - fl * 0.62), (dx, base - fl * 0.86), (dx + dw, base - fl * 0.62),
                  (dx + dw, base)], 2), (110, 70, 44), INK, 2.2)
    p.line([(dx, base - fl * 0.84), (dx, base)], dk((110, 70, 44), 0.7), 1.4)
    if sign:                                                            # a shop: a wide window and a hanging sign
        sx0 = x0 + w * (0.5 if seed % 2 else 0.12)
        p.poly(quad(sx0, base - fl * 0.7, sx0 + w * 0.36, base - fl * 0.18), (90, 110, 130), INK, 2.0)
        for k in range(1, 3):
            p.line([(sx0 + w * 0.12 * k, base - fl * 0.7), (sx0 + w * 0.12 * k, base - fl * 0.18)], BEAM, 1.6)
        bx_ = x1 - 4 if seed % 2 else x0 + 4
        sg = 1 if seed % 2 else -1
        p.line([(bx_, base - fl * 0.95), (bx_ + sg * w * 0.22, base - fl * 0.95)], (50, 46, 44), 3.0)
        p.poly(quad(min(bx_ + sg * w * 0.05, bx_ + sg * w * 0.2), base - fl * 0.9,
                    max(bx_ + sg * w * 0.05, bx_ + sg * w * 0.2), base - fl * 0.62), sign, INK, 1.8)
    else:
        wx = x0 + w * (0.7 if seed % 2 else 0.3)
        ww, wh = min(w * 0.1, 26), fl * 0.36
        p.poly(quad(wx - ww, base - fl * 0.72, wx + ww, base - fl * 0.72 + wh), (70, 90, 120), INK, 2.0)
    if balcony:
        by = base - fl - 2
        p.poly(quad(ux0 + w * 0.12, by, ux1 - w * 0.12, by + fl * 0.1), BEAM, INK, 2.0)
        for kk in range(9):
            xx = ux0 + w * 0.14 + (w * 0.72) * kk / 8
            p.line([(xx, by - fl * 0.25), (xx, by)], BEAM, 2.0)
        p.line([(ux0 + w * 0.12, by - fl * 0.25), (ux1 - w * 0.12, by - fl * 0.25)], BEAM, 2.4)


def _feather(p, root, tip, wd, col):
    (ax, ay), (bx, by) = root, tip
    L = math.hypot(bx - ax, by - ay) or 1.0
    nx, ny = -(by - ay) / L * wd, (bx - ax) / L * wd
    mx, my = ax + (bx - ax) * 0.45, ay + (by - ay) * 0.45
    p.poly(curve([(ax, ay), (mx + nx, my + ny), (bx, by), (mx - nx, my - ny)], 3), col, INK, 1.2)


def _crest(p, x, y, r):
    """An invented gold crest (not the game's): a gold-edged shield holding a bird with spread wings, a round head
    and a fanned tail (pass 2: it read as a V over a triangle)."""
    shield = curve([(x - r, y - r), (x + r, y - r), (x + r, y + r * 0.15), (x + r * 0.55, y + r * 0.9), (x, y + r * 1.25),
                    (x - r * 0.55, y + r * 0.9), (x - r, y + r * 0.15)], 2)
    p.poly(shield, BANNER_D, None)
    p.line(shield + shield[:1], GOLD, max(2.0, r * 0.12))
    for sg in (-1, 1):                                                  # the wings: three feathers each, fanned up
        for k, (ang, ln) in enumerate(((10, 0.78), (35, 0.8), (62, 0.7))):
            a = math.radians(ang)
            _feather(p, (x + sg * r * 0.12, y - r * 0.05),
                     (x + sg * r * ln * math.cos(a), y - r * 0.05 - r * ln * math.sin(a)), r * 0.1, GOLD)
    for ang in (-20, 0, 20):                                            # the tail
        a = math.radians(90 + ang)
        _feather(p, (x, y + r * 0.3), (x + r * 0.55 * math.cos(a), y + r * 0.3 + r * 0.55 * math.sin(a)), r * 0.09, GOLD)
    p.ell(x, y + r * 0.1, r * 0.17, r * 0.3, GOLD, INK, 1.2)            # body
    p.ell(x, y - r * 0.38, r * 0.15, r * 0.15, GOLD, INK, 1.2)          # head
    p.poly([(x + r * 0.12, y - r * 0.4), (x + r * 0.3, y - r * 0.34), (x + r * 0.12, y - r * 0.3)], GOLD, INK, 1.0)


def _banner(p, x, top, w, h, t=0.0):
    """A tall pale-blue banner (ref 22): a gold frame all round, a pointed foot with a tassel, a small diamond
    pattern, the gold crest; hung from a rod with round finials."""
    sway = 6 * math.sin(t * 1.4 + x)
    outer = [(x - w / 2, top), (x + w / 2, top), (x + w / 2 + sway, top + h), (x + sway, top + h * 1.12),
             (x - w / 2 + sway, top + h)]
    b = max(4.0, w * 0.08)
    inner = [(x - w / 2 + b, top + b), (x + w / 2 - b, top + b), (x + w / 2 + sway - b, top + h - b * 0.5),
             (x + sway, top + h * 1.12 - b * 1.5), (x - w / 2 + sway + b, top + h - b * 0.5)]
    p.poly(outer, GOLD, INK, 2.4)
    p.poly(inner, BANNER, None)
    p.line(inner + inner[:1], dk(GOLD, 0.75), 1.4)
    for i in range(4):                                                  # the woven diamond pattern
        for j in range(9):
            u, v = (i + 0.5) / 4, (j + 0.5) / 9
            if 0.32 < v < 0.62:
                continue                                                # leave the crest clear
            cx_, cy_ = x - w / 2 + b + (w - 2 * b) * u + sway * v, top + b + (h - 2 * b) * v
            dd = w * 0.045
            p.poly([(cx_, cy_ - dd), (cx_ + dd, cy_), (cx_, cy_ + dd), (cx_ - dd, cy_)], BANNER_D, None)
    _crest(p, x + sway * 0.5, top + h * 0.44, w * 0.3)
    tx_, ty_ = x + sway, top + h * 1.12                                 # the tassel (pass 3: a gold ball read as a
    p.line([(tx_, ty_), (tx_, ty_ + w * 0.12)], dk(GOLD, 0.8), 2.0)    # yellow blob): a cord, a knob, a fringe
    p.ell(tx_, ty_ + w * 0.14, w * 0.035, w * 0.03, GOLD, INK, 1.2)
    fr = [(tx_ - w * 0.04, ty_ + w * 0.16), (tx_ + w * 0.04, ty_ + w * 0.16), (tx_ + w * 0.06, ty_ + w * 0.3),
          (tx_ - w * 0.06, ty_ + w * 0.3)]
    p.poly(fr, GOLD, INK, 1.2)
    for u in (0.25, 0.5, 0.75):
        p.line([(tx_ - w * 0.04 + w * 0.08 * u, ty_ + w * 0.17), (tx_ - w * 0.06 + w * 0.12 * u, ty_ + w * 0.29)],
               dk(GOLD, 0.7), 1.0)
    p.line([(x - w * 0.62, top), (x + w * 0.62, top)], (60, 50, 40), 4.0)  # the rod and its finials
    for sg in (-1, 1):
        p.ell(x + sg * w * 0.64, top, w * 0.05, w * 0.05, GOLD, INK, 1.4)


def _bunting(p, xa, ya, xb, yb, sag, n, t=0.0):
    pts = [(xa + (xb - xa) * u, ya + (yb - ya) * u + sag * 4 * u * (1 - u)) for u in np.linspace(0, 1, n + 1)]
    p.line(open_curve(pts, 3), (70, 60, 50), 1.8)
    for k in range(n):
        (x0, y0), (x1, y1) = pts[k], pts[k + 1]
        c = ((178, 92, 84), (88, 112, 156), (204, 182, 112))[k % 3]   # pass 3: louder than the line-up's faces:
        p.poly([(x0, y0), (x1, y1), ((x0 + x1) / 2, (y0 + y1) / 2 + abs(x1 - x0) * 0.75)], c, INK, 1.0)   # softer


FOUNTAIN_STONE = {'now': ((180, 180, 186), (150, 146, 140), (160, 156, 150), (200, 198, 202), (210, 208, 210)),
                  'dark': ((128, 124, 116), (104, 100, 94), (112, 108, 100), (138, 134, 126), (92, 96, 92)),
                  'bird': ((128, 124, 116), (104, 100, 94), (112, 108, 100), (138, 134, 126), (86, 142, 122))}
                  # floor, wall, pillar, tiers, statue (rule 87: pale and statue-less; ref 21 dark stone, statues)


def _fountain(p, x, d, t):
    """The square's stone fountain (ref 21): a round basin, a pillar with two tiers, an invented stone figure
    holding a jug on top, water falling from the tiers into the basin."""
    floor_c, wall_c, pil_c, tier_c, fig_c = FOUNTAIN_STONE[OPT['fountain']]
    ppm = TOWN.ppm(d)
    bx, by = TOWN.p(x, d, 0)
    R = 2.4 * ppm
    p.ell(bx, by, R, R * 0.2, floor_c, INK, 2.4)                        # the basin floor
    p.poly(quad(bx - R, by - 0.7 * ppm, bx + R, by), wall_c, INK, 2.4)  # its wall (pass 1: darker, ref 21)
    p.ell(bx, by - 0.7 * ppm, R, R * 0.2, (120, 170, 210), INK, 2.4)     # the water
    p.ell(bx, by - 0.7 * ppm, R * 0.8, R * 0.13, (160, 200, 230), None)
    for k in range(-5, 6):
        p.line([(bx + R * k / 5.5, by - 0.62 * ppm), (bx + R * k / 5.5, by - 0.05 * ppm)], mix(wall_c, (255, 255, 255), 0.15), 1.4)
    col_top = by - 3.0 * ppm
    p.poly(quad(bx - 0.25 * ppm, col_top, bx + 0.25 * ppm, by - 0.7 * ppm), pil_c, INK, 2.2)
    for z, rr in ((1.7, 1.0), (2.6, 0.6)):                              # two tiers
        ty = by - z * ppm
        p.poly([(bx - rr * ppm, ty), (bx + rr * ppm, ty), (bx + rr * 0.6 * ppm, ty + 0.25 * ppm),
                (bx - rr * 0.6 * ppm, ty + 0.25 * ppm)], tier_c, INK, 2.2)
        for sg in (-1, 1):                                              # falling water
            p.poly(ribbon(open_curve([(bx + sg * rr * ppm, ty), (bx + sg * (rr + 0.25) * ppm, ty + 0.4 * ppm),
                                      (bx + sg * (rr + 0.35) * ppm, by - 0.75 * ppm)], 5), 0.08 * ppm, 0.14 * ppm),
                   (180, 214, 240), None)
    if OPT['fountain'] == 'now':
        _statue_now(p, bx, col_top, 1.5 * ppm, fig_c)
    elif OPT['fountain'] == 'dark':
        _statue_robed(p, bx, col_top, 2.0 * ppm, fig_c)
    else:
        _statue_bird(p, bx, col_top, 2.0 * ppm, fig_c)


def _statue_now(p, fx, fy, sp, c):
    p.poly([(fx - 0.18 * sp, fy), (fx + 0.18 * sp, fy), (fx + 0.14 * sp, fy - 0.9 * sp),
            (fx - 0.14 * sp, fy - 0.9 * sp)], c, INK, 2.0)              # the figure's robe
    p.ell(fx, fy - 1.02 * sp, 0.12 * sp, 0.13 * sp, c, INK, 2.0)
    p.poly([(fx + 0.12 * sp, fy - 0.8 * sp), (fx + 0.4 * sp, fy - 0.9 * sp), (fx + 0.42 * sp, fy - 0.7 * sp),
            (fx + 0.3 * sp, fy - 0.62 * sp)], c, INK, 1.8)              # the jug on her shoulder
    p.poly(ribbon(open_curve([(fx + 0.42 * sp, fy - 0.72 * sp), (fx + 0.6 * sp, fy - 0.5 * sp),
                              (fx + 0.75 * sp, fy + 0.4 * sp)], 5), 0.05 * sp, 0.1 * sp), (180, 214, 240), None)


def _statue_robed(p, fx, fy, sp, c):
    """Option A (rule 87): a dark weathered stone maiden on a plinth, hooded, her robe in folds, tipping a jug on her
    shoulder; the water pours from it; moss streaks down the stone."""
    lit, sh = mix(c, (255, 255, 255), 0.25), dk(c, 0.75)
    p.poly(quad(fx - 0.3 * sp, fy - 0.12 * sp, fx + 0.3 * sp, fy), dk(c, 0.9), INK, 2.0)   # the plinth
    robe = curve([(fx - 0.24 * sp, fy - 0.12 * sp), (fx - 0.2 * sp, fy - 0.6 * sp), (fx - 0.13 * sp, fy - 0.95 * sp),
                  (fx + 0.13 * sp, fy - 0.95 * sp), (fx + 0.2 * sp, fy - 0.6 * sp), (fx + 0.26 * sp, fy - 0.12 * sp)], 4)
    p.poly(robe, c, INK, 2.2)
    for u in (-0.1, 0.0, 0.1):                                          # the folds
        p.line(open_curve([(fx + u * sp, fy - 0.9 * sp), (fx + u * 1.3 * sp, fy - 0.5 * sp), (fx + u * 1.8 * sp, fy - 0.14 * sp)], 3),
               sh, 1.6)
    p.poly(curve([(fx - 0.15 * sp, fy - 0.92 * sp), (fx - 0.15 * sp, fy - 1.14 * sp), (fx, fy - 1.26 * sp),
                  (fx + 0.15 * sp, fy - 1.14 * sp), (fx + 0.15 * sp, fy - 0.92 * sp)], 3), c, INK, 2.0)   # the hood
    p.ell(fx - 0.02 * sp, fy - 1.06 * sp, 0.08 * sp, 0.1 * sp, lit, INK, 1.6)   # her face in it
    p.poly(ribbon(open_curve([(fx + 0.14 * sp, fy - 0.85 * sp), (fx + 0.3 * sp, fy - 1.0 * sp), (fx + 0.3 * sp, fy - 1.12 * sp)], 3),
                  0.07 * sp, 0.06 * sp), c, INK, 1.6)                   # her raised arm
    p.poly(curve([(fx + 0.22 * sp, fy - 1.22 * sp), (fx + 0.5 * sp, fy - 1.3 * sp), (fx + 0.56 * sp, fy - 1.06 * sp),
                  (fx + 0.36 * sp, fy - 0.98 * sp)], 3), c, INK, 1.8)   # the jug, tipped
    p.poly(ribbon(open_curve([(fx + 0.56 * sp, fy - 1.1 * sp), (fx + 0.72 * sp, fy - 0.8 * sp),
                              (fx + 0.82 * sp, fy + 0.4 * sp)], 5), 0.05 * sp, 0.1 * sp), (180, 214, 240), None)
    for u in (-0.15, 0.08):                                             # moss streaks
        p.line([(fx + u * sp, fy - 0.5 * sp), (fx + u * sp, fy - 0.15 * sp)], (96, 120, 70), 2.0)


def _statue_bird(p, fx, fy, sp, c):
    """Option B (rule 87): dark stone, and on the pillar a green-bronze bird with spread wings, the crest's bird,
    on a stone ball; water spouts from its beak."""
    sh = dk(c, 0.7)
    p.ell(fx, fy - 0.12 * sp, 0.16 * sp, 0.14 * sp, (112, 108, 100), INK, 2.0)   # the ball
    for sg in (-1, 1):                                                  # the spread wings, feathers fanned
        for k in range(5):
            a = math.radians(-90 + sg * (20 + k * 16))
            tip = (fx + sg * 0.1 * sp + math.cos(a) * (0.62 - 0.06 * k) * sp * sg * sg, fy - 0.55 * sp + math.sin(a) * (0.62 - 0.06 * k) * sp)
            p.poly(curve([(fx + sg * 0.06 * sp, fy - 0.5 * sp), (tip[0] - sg * 0.05 * sp, tip[1] + 0.06 * sp), tip,
                          (tip[0] + sg * 0.04 * sp, tip[1] + 0.12 * sp), (fx + sg * 0.1 * sp, fy - 0.4 * sp)], 3),
                   c if k % 2 else sh, INK, 1.6)
    p.poly(curve([(fx - 0.12 * sp, fy - 0.22 * sp), (fx - 0.13 * sp, fy - 0.6 * sp), (fx, fy - 0.72 * sp),
                  (fx + 0.13 * sp, fy - 0.6 * sp), (fx + 0.12 * sp, fy - 0.22 * sp)], 4), c, INK, 2.0)   # its body
    p.ell(fx, fy - 0.82 * sp, 0.1 * sp, 0.1 * sp, c, INK, 2.0)          # its head
    p.poly([(fx + 0.08 * sp, fy - 0.84 * sp), (fx + 0.2 * sp, fy - 0.8 * sp), (fx + 0.08 * sp, fy - 0.76 * sp)],
           (196, 160, 70), INK, 1.4)                                    # its beak
    p.poly(ribbon(open_curve([(fx + 0.2 * sp, fy - 0.8 * sp), (fx + 0.45 * sp, fy - 0.7 * sp),
                              (fx + 0.62 * sp, fy + 0.4 * sp)], 5), 0.04 * sp, 0.09 * sp), (180, 214, 240), None)


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
    """A wooden barrel (pass 3: unreadable at phone size): bulging staves, three dark iron hoops, the lid's rim."""
    ppm = TOWN.ppm(d)
    bx, by = TOWN.p(x, d, 0)
    a, b = (bx - 0.3 * ppm, by), (bx + 0.3 * ppm, by - 0.9 * ppm)
    wood = (156, 102, 58)
    p.poly(curve([(a[0], a[1]), (a[0] - 0.06 * ppm, by - 0.45 * ppm), (a[0], b[1]), (b[0], b[1]), (b[0] + 0.06 * ppm,
                                                                                                   by - 0.45 * ppm),
                  (b[0], a[1])], 2), wood, INK, 2.2)
    for u in (-0.15, 0.15):                                             # staves
        p.line(open_curve([(bx + u * ppm, by - 0.02 * ppm), (bx + u * 1.25 * ppm, by - 0.45 * ppm),
                           (bx + u * ppm, by - 0.88 * ppm)], 3), dk(wood, 0.75), 1.4)
    for u in (0.12, 0.5, 0.88):                                         # the iron hoops
        bulge = 0.06 * ppm * math.sin(math.pi * u)
        p.line([(a[0] - bulge, by - 0.9 * ppm * u), (b[0] + bulge, by - 0.9 * ppm * u)], (54, 50, 48), max(2.5, 0.04 * ppm))
    p.ell(bx, b[1], 0.3 * ppm, 0.07 * ppm, dk(wood, 0.8), INK, 1.8)        # the lid


def _sack(p, x, d):
    ppm = TOWN.ppm(d)
    bx, by = TOWN.p(x, d, 0)
    p.poly(curve([(bx - 0.25 * ppm, by), (bx - 0.28 * ppm, by - 0.4 * ppm), (bx - 0.08 * ppm, by - 0.62 * ppm),
                  (bx + 0.1 * ppm, by - 0.6 * ppm), (bx + 0.28 * ppm, by - 0.38 * ppm), (bx + 0.24 * ppm, by)], 3),
           (206, 186, 140), INK, 2.0)


def _townsfolk(p, x, d, col, seed, lev=None):
    """A townsperson in the house style (pass 2: capsules that read as bollards): legs and shoes or a long skirt,
    a tunic with a belt, two arms with hands, a head with hair, and for some a hat, a headscarf or a basket."""
    lev = lev or TOWN
    r = random.Random(seed)
    ppm = lev.ppm(d)
    bx, by = lev.p(x, d, 0)
    h = r.uniform(1.55, 1.78) * ppm
    skin = r.choice([(240, 206, 180), (214, 170, 130), (180, 130, 96)])
    hair = r.choice([(90, 60, 40), (200, 150, 70), (60, 40, 30), (150, 70, 40)])
    kind = seed % 3                                                     # 0 a woman in a long skirt, 1 a man, 2 a man in a hat
    lw = max(1.0, min(1.8, ppm / 60))
    sh_y, hip_y = by - h * 0.8, by - h * 0.47
    p.ell(bx, by, 0.3 * ppm, 0.06 * ppm, mix(FLAG_D, (60, 60, 70), 0.4), None)
    if kind == 0:
        p.poly(curve([(bx - 0.13 * ppm, hip_y), (bx + 0.13 * ppm, hip_y), (bx + 0.26 * ppm, by - 0.02 * ppm),
                      (bx - 0.26 * ppm, by - 0.02 * ppm)], 2), dk(col, 0.8), INK, lw)
    else:
        for sg in (-1, 1):                                              # legs and shoes
            p.poly(quad(bx + sg * 0.03 * ppm - (sg < 0) * 0.08 * ppm, hip_y, bx + sg * 0.03 * ppm + (sg > 0) * 0.08 * ppm,
                        by - 0.04 * ppm), (88, 72, 60), INK, lw)
            p.ell(bx + sg * 0.08 * ppm, by - 0.03 * ppm, 0.07 * ppm, 0.035 * ppm, (60, 44, 34), INK, lw)
    body = [(bx - 0.15 * ppm, sh_y), (bx + 0.15 * ppm, sh_y), (bx + 0.17 * ppm, hip_y + 0.08 * ppm),
            (bx - 0.17 * ppm, hip_y + 0.08 * ppm)]
    p.poly(body, col, INK, lw)
    p.line([(bx - 0.165 * ppm, hip_y), (bx + 0.165 * ppm, hip_y)], (90, 66, 44), max(1.5, 0.035 * ppm))
    wave = seed % 4 == 1
    for sg in (-1, 1):                                                  # arms and hands
        if wave and sg > 0:
            pts = [(bx + 0.15 * ppm, sh_y + 0.03 * ppm), (bx + 0.3 * ppm, sh_y - 0.12 * ppm), (bx + 0.34 * ppm, sh_y - 0.32 * ppm)]
        else:
            pts = [(bx + sg * 0.15 * ppm, sh_y + 0.03 * ppm), (bx + sg * 0.2 * ppm, sh_y + 0.2 * ppm),
                   (bx + sg * 0.21 * ppm, hip_y + 0.06 * ppm)]
        p.poly(ribbon(pts, 0.05 * ppm, 0.04 * ppm), col, INK, lw)
        p.ell(pts[-1][0], pts[-1][1], 0.04 * ppm, 0.04 * ppm, skin, INK, lw * 0.8)
    if seed % 5 == 3:                                                   # a basket on the arm
        p.poly(curve([(bx - 0.36 * ppm, hip_y - 0.02 * ppm), (bx - 0.14 * ppm, hip_y - 0.02 * ppm),
                      (bx - 0.17 * ppm, hip_y + 0.14 * ppm), (bx - 0.33 * ppm, hip_y + 0.14 * ppm)], 2), (180, 140, 80), INK, lw)
        p.ell(bx - 0.25 * ppm, hip_y - 0.04 * ppm, 0.07 * ppm, 0.04 * ppm, (220, 70, 50), None)
    hy = by - h * 0.89
    p.poly(quad(bx - 0.035 * ppm, sh_y - 0.06 * ppm, bx + 0.035 * ppm, sh_y + 0.01 * ppm), skin, None)   # neck
    p.ell(bx, hy, 0.1 * ppm, 0.115 * ppm, skin, INK, lw)
    if kind == 0:                                                       # a headscarf
        p.poly(curve([(bx - 0.12 * ppm, hy + 0.04 * ppm), (bx - 0.11 * ppm, hy - 0.1 * ppm), (bx, hy - 0.15 * ppm),
                      (bx + 0.11 * ppm, hy - 0.1 * ppm), (bx + 0.12 * ppm, hy + 0.04 * ppm), (bx + 0.14 * ppm, hy + 0.14 * ppm),
                      (bx - 0.14 * ppm, hy + 0.14 * ppm)], 3), r.choice([(230, 220, 200), (200, 80, 70), (90, 120, 170)]),
               INK, lw)
    else:
        p.poly(curve([(bx - 0.1 * ppm, hy), (bx - 0.09 * ppm, hy - 0.1 * ppm), (bx, hy - 0.13 * ppm),
                      (bx + 0.09 * ppm, hy - 0.1 * ppm), (bx + 0.1 * ppm, hy)], 3), hair, INK, lw)
        if kind == 2:                                                   # a brimmed hat
            p.ell(bx, hy - 0.09 * ppm, 0.17 * ppm, 0.035 * ppm, (110, 80, 50), INK, lw)
            p.poly(quad(bx - 0.08 * ppm, hy - 0.2 * ppm, bx + 0.08 * ppm, hy - 0.09 * ppm), (110, 80, 50), INK, lw)


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


def _palm_bed(p, x, d, seed):
    """The palm's grass bed in a stone kerb (ref 21), drawn over the trunk's foot so the palm stands in it."""
    ppm = TOWN.ppm(d)
    bx, by = TOWN.p(x, d)
    rx, ry = 1.0 * ppm, 1.0 * ppm * TOWN.h / d
    p.ell(bx, by, rx + 0.12 * ppm, ry + 0.06 * ppm, FLAG_L, INK, 2.2)
    p.ell(bx, by - 0.05 * ppm, rx, ry, LEAF, INK, 1.8)
    rr = random.Random(seed)
    for k in range(14):
        a = rr.uniform(0, 2 * math.pi)
        rad = rr.uniform(0.1, 0.85)
        tuft(p, bx + math.cos(a) * rx * rad, by - 0.05 * ppm + math.sin(a) * ry * rad, 0.35 * ppm, LEAF_D, seed + k, 5, 2.0)
    for k in range(6):
        tuft(p, bx + (k - 2.5) * 0.12 * ppm, by - 0.02 * ppm, 0.45 * ppm, LEAF_L, seed + 40 + k, 6, 2.2)


def _planter(p, lev, x, d, w, seed):
    """A stone flower trough (ref 22): rough grey stone, red and purple flowers, trailing leaves."""
    ppm = lev.ppm(d)
    bx, by = lev.p(x, d)
    x0, x1 = bx - w / 2 * ppm, bx + w / 2 * ppm
    top = by - 0.62 * ppm
    p.poly(quad(x0, top, x1, by), (166, 164, 158), INK, 2.6)
    p.poly(quad(x0 - 0.05 * ppm, top - 0.06 * ppm, x1 + 0.05 * ppm, top + 0.04 * ppm), (190, 188, 180), INK, 2.4)
    p.line([(x0, by - 0.1 * ppm), (x1, by - 0.1 * ppm)], (130, 128, 124), 2.0)
    rr = random.Random(seed)
    p.poly(blob(bx, top - 0.06 * ppm, (x1 - x0) * 0.44, 0.13 * ppm, 14, 0.15, seed, flat_bottom=True), LEAF, INK, 1.8)
    # (pass 3: the flowers bulged off the trough: now they sit inside its lip, a low mound)
    for k in range(int(w * 6)):
        xx = x0 + (x1 - x0) * (k + 0.5) / (w * 6)
        p.poly(curve([(xx - 0.05 * ppm, top), (xx + rr.uniform(-0.04, 0.04) * ppm, top - 0.16 * ppm), (xx + 0.05 * ppm, top)], 3),
               LEAF, INK, 1.4)
    for k in range(int(w * 16)):
        flower(p, x0 + (x1 - x0) * rr.uniform(0.12, 0.88), top - rr.uniform(0.04, 0.17) * ppm, 0.06 * ppm,
               (210, 50, 60) if k % 2 else PURPLE)
    for k in range(int(w * 3)):                                         # leaves trailing over the lip
        xx = x0 + (x1 - x0) * rr.uniform(0.05, 0.95)
        p.poly(ribbon([(xx, top), (xx + 0.03 * ppm, top + 0.12 * ppm), (xx - 0.02 * ppm, top + 0.22 * ppm)],
                      0.04 * ppm, 0.015 * ppm), LEAF_D, INK, 1.2)


SQUARE_HOUSES = [   # the far row (pass 2: one block repeated): x0, x1, wall top, roof height, colour, build
    (-170, 90, 470, 150, 0, dict(floors=3, wins=2, roof='gable', stone=True, frame='brace', balcony=True)),
    (96, 300, 520, 110, 1, dict(floors=2, wins=2, roof='side', stone=True, frame='studs', sign=(200, 60, 50), chimney=True)),
    (306, 440, 380, 120, 4, dict(floors=3, wins=1, roof='tower', frame='x', jetty=True)),
    (690, 800, 500, 90, 3, dict(floors=2, wins=1, roof='gable', frame=None, shut=(60, 90, 140))),
    (806, 1000, 430, 140, 2, dict(floors=3, wins=3, roof='side', stone=True, frame='x', balcony=True, chimney=True)),
    (1006, 1260, 480, 160, 4, dict(floors=3, wins=2, roof='gable', stone=True, jetty=True, frame='brace',
                                   sign=(60, 110, 70))),
]


def town_square(img, p, cam, t):
    """S10, the line-up (ref 21, 22): Castle Town square: blue sky, the hazy castle behind the rooftops, six different
    timber-framed houses with red-orange roofs, the fountain and its statue, a palm in a grass bed, the red-striped
    stall, barrels and sacks, banners, two strings of bunting high overhead, townsfolk, paving slabs to the lens,
    a stone flower trough in the near right corner."""
    _sky(p, -400, 950, 2.0)
    for x, y, w, sd in ((180, 200, 180, 401), (860, 300, 200, 402)):
        _cloud(p, x, y, w, sd)
    _castle(p, 560, 640, 1.0)
    haze(img, cam, 300, 700, (230, 236, 244), 0.25)
    base = TOWN.p(0, 24.0)[1]
    for k, (x0, x1, top, rh, ci, kw) in enumerate(SQUARE_HOUSES):
        _house(img, p, x0, x1, base, top, rh, PLASTER[ci], 410 + k, **kw)
    _flagstones(p, TOWN, 24.0, 420, 0.42, (0.4, 0.8))
    _bunting(p, -40, 470, 1120, 450, 40, 22, t)                         # the far string, across the square's back
    for x, d, c, sd in ((-1.8, 20.0, (120, 90, 150), 1), (2.6, 21.0, (90, 120, 90), 2), (-4.2, 19.0, (170, 110, 70), 3),
                        (4.6, 18.5, (190, 160, 90), 6), (-0.9, 21.5, (160, 70, 70), 8)):
        _townsfolk(p, x, d, c, sd)
    _fountain(p, 0.2, 15.0, t)
    # the near sides: a palm in its bed on the left, the stall, barrels and sacks on the right; banners on poles
    q = TOWN.p(-3.4, 11.0)
    _palm(p, q[0], q[1], 7.0 * TOWN.ppm(11.0), 431)
    _palm_bed(p, -3.4, 11.0, 433)
    _tent(p, 3.3, 10.0)
    for x, d in ((1.9, 10.2), (2.25, 10.4)):                            # pass 1: barrels and sacks AT the stall
        _barrel_t(p, x, d)
    for x, d in ((4.7, 10.1), (4.95, 10.3)):
        _sack(p, x, d)
    for k, (x, d, c) in enumerate(((-3.0, 12.6, (110, 80, 140)), (2.5, 11.4, (80, 110, 150)), (-1.4, 13.0, (150, 100, 60)),
                                   (4.0, 11.0, (170, 70, 60)))):
        _townsfolk(p, x, d, c, 10 + k)                                  # pass 1: townsfolk nearer, so they show
    tops = []
    for x, d in ((-2.9, 8.0), (3.4, 7.6)):
        a, b = TOWN.p(x, d, 0), TOWN.p(x, d, 4.4)
        p.line([a, b], (70, 60, 50), 4.0)
        p.ell(b[0], b[1] - 4, 7, 7, GOLD, INK, 1.4)
        _banner(p, b[0] + 46 * (1 if x < 0 else -1), b[1] + 20, 0.8 * TOWN.ppm(d), 2.2 * TOWN.ppm(d), t)
        tops.append(b)
    (xa, ya), (xb, yb) = tops                                           # pass 2: the near string high, pole top to top
    _bunting(p, xa, ya + 6, xb, yb + 6, 90, 14, t)
    _planter(p, TOWN, 1.5, 2.35, 1.6, 441)                              # the near right corner (pass 2: empty)


WALL_VIEW = dict(base=1640, ppm=560.0)         # S12, S13: the wall's foot on screen and pixels per metre there
WALL_LEV = Level(h=1.0, hz=1080.0, f=1680.0)   # the ground in front of it: at d = 3 m, y = 1640 and 560 px a metre


def _stone_block(p, x0, y0, x1, y1, seed, c):
    """One rough grey block: a hand-cut edge, a lit top edge, a shadowed foot, a chip or two (pass 2: neat beige
    rectangles)."""
    rr = random.Random(seed)
    pts = wob(quad(x0, y0, x1, y1), 4.0, seed, 22)
    p.poly(pts, c, INK, 2.0)
    hgt = y1 - y0
    p.poly(wob([(x0 + 6, y0 + 5), (x1 - 6, y0 + 5), (x1 - 12, y0 + hgt * 0.16), (x0 + 10, y0 + hgt * 0.16)], 2.0, seed + 1, 30),
           mix(c, WALLSTONE_L, 0.6), None)
    p.poly(wob([(x0 + 8, y1 - hgt * 0.18), (x1 - 5, y1 - hgt * 0.22), (x1 - 5, y1 - 5), (x0 + 6, y1 - 5)], 2.0, seed + 2, 30),
           mix(c, WALLSTONE_D, 0.7), None)
    for k in range(rr.randint(0, 2)):
        cx_, cy_ = rr.uniform(x0 + 20, x1 - 20), rr.uniform(y0 + 20, y1 - 20)
        if rr.random() < 0.5:
            p.line(open_curve([(cx_, cy_), (cx_ + rr.uniform(-18, 18), cy_ + 16), (cx_ + rr.uniform(-24, 24), cy_ + 34)], 3),
                   WALLSTONE_D, 1.6)
        else:
            p.poly(curve([(cx_, cy_), (cx_ + 12, cy_ - 5), (cx_ + 18, cy_ + 6), (cx_ + 6, cy_ + 10)], 3), WALLSTONE_D, None)


def town_wall(img, p, cam, t):
    """S12 and S13, the slam (ref 22): a rough grey stone wall filling the frame (pass 2: neat beige blocks, no
    depth): uneven hand-cut blocks with lit tops and shadowed feet; a stepped-out plinth at the foot and a moulded
    ledge above head height, both casting a shadow; a shuttered window set deep in its reveal on a stone sill with
    a flower box (red and purple); a tall pale-blue banner with the gold crest on an iron bracket; bunting; a
    stone flower trough; paving slabs at its foot."""
    ppm = WALL_VIEW['ppm']
    base = WALL_VIEW['base']
    p.poly(quad(-200, -400, W + 200, base), MORTAR, None)
    rr = random.Random(501)
    y = base - 0.55 * ppm                                               # above the plinth
    row = 0
    while y > -400:                                                     # the blocks, row by row, uneven
        bh = 0.36 * ppm * rr.uniform(0.8, 1.25)
        x = -200 - rr.uniform(0, 0.4) * ppm
        while x < W + 200:
            bw = 0.36 * ppm * rr.uniform(1.2, 2.4)
            c = mix(WALLSTONE, rr.choice([WALLSTONE_D, WALLSTONE_L, (176, 170, 156)]), rr.uniform(0, 0.5))
            _stone_block(p, x + 3, y - bh + 3, x + bw - 3, y - 3, row * 97 + int(x), c)
            x += bw
        y -= bh
        row += 1
    ly = 520                                                            # the moulded ledge, with its shadow below
    p.poly(quad(-200, ly + 22, W + 200, ly + 56), mix(MORTAR, WALLSTONE_D, 0.3), None)
    p.poly(quad(-200, ly - 26, W + 200, ly + 22), WALLSTONE_L, INK, 2.6)
    p.line([(-200, ly + 4), (W + 200, ly + 4)], WALLSTONE_D, 3.0)
    wx, wy = 820, 260                                                   # the window, high right, set deep in the wall
    p.poly(quad(wx - 250, wy - 200, wx + 250, wy + 190), (92, 88, 84), INK, 3.0)       # the reveal (its depth)
    p.poly([(wx - 250, wy - 200), (wx + 250, wy - 200), (wx + 226, wy - 176), (wx - 226, wy - 176)], (70, 66, 64), None)
    p.poly([(wx - 250, wy - 200), (wx - 226, wy - 176), (wx - 226, wy + 190), (wx - 250, wy + 190)], (120, 116, 110), None)
    p.poly(quad(wx - 130, wy - 170, wx + 130, wy + 170), (70, 90, 120), INK, 3.0)
    p.line([(wx, wy - 170), (wx, wy + 170)], BEAM, 3.0)
    p.line([(wx - 130, wy), (wx + 130, wy)], BEAM, 3.0)
    for sg in (-1, 1):
        p.poly(quad(wx + sg * 130, wy - 170, wx + sg * 224, wy + 170), (60, 90, 140), INK, 2.6)
        for k in range(1, 12):                                          # louvres (pass 1: flat panels)
            yy = wy - 170 + 340 * k / 12
            p.poly(quad(wx + sg * 136 - (sg < 0) * 82, yy - 9, wx + sg * 136 + (sg > 0) * 82, yy), (82, 112, 160), None)
            p.line([(wx + sg * 136, yy), (wx + sg * 218, yy)], (36, 58, 100), 2.2)
        for yy in (wy - 120, wy + 120):                                 # the iron hinges
            p.poly(quad(wx + sg * 130 - (sg < 0) * 40, yy - 6, wx + sg * 130 + (sg > 0) * 40, yy + 6), (40, 40, 40), INK, 1.2)
    p.poly(quad(wx - 280, wy + 190, wx + 280, wy + 226), WALLSTONE_L, INK, 2.6)        # the stone sill, stepped out
    p.poly(quad(wx - 270, wy + 226, wx + 270, wy + 250), mix(MORTAR, WALLSTONE_D, 0.3), None)
    p.poly(quad(wx - 170, wy + 140, wx + 170, wy + 196), BEAM, INK, 2.6)   # the flower box on the sill
    for k in range(8):
        flower(p, wx - 150 + 43 * k, wy + 132 - 18 * (k % 2), 30, (210, 50, 60) if k % 2 else PURPLE)
    for k in range(5):
        p.poly(curve([(wx - 140 + 70 * k, wy + 196), (wx - 120 + 70 * k, wy + 262), (wx - 100 + 70 * k, wy + 196)], 3), LEAF,
               INK, 1.6)
    pt = base - 0.55 * ppm                                              # the plinth: big blocks stepped out
    p.poly(quad(-200, pt - 30, W + 200, pt + 4), WALLSTONE_L, INK, 2.6)
    x = -200
    k = 0
    while x < W + 200:
        bw = 0.7 * ppm * rr.uniform(0.8, 1.2)
        _stone_block(p, x + 3, pt + 6, x + bw - 3, base - 3, 900 + k, mix(WALLSTONE, WALLSTONE_D, rr.uniform(0.2, 0.5)))
        x += bw
        k += 1
    p.poly(quad(-200, pt + 4, W + 200, pt + 22), mix(MORTAR, WALLSTONE_D, 0.2), None)   # the ledge's shadow
    p.poly(quad(120, 120, 175, 140), (50, 46, 44), INK, 2.0)            # the iron bracket
    p.line([(130, 130), (330, 130)], (50, 46, 44), 6.0)
    p.line([(140, 140), (250, 220)], (50, 46, 44), 4.0)
    _banner(p, 240, 140, 0.7 * ppm, 2.0 * ppm, t)
    _bunting(p, -40, -20, 1120, 30, 60, 8, t)
    _flagstones(p, WALL_LEV, 3.0, 502, 0.34, (0.35, 0.7))
    p.line([(-200, base), (W + 200, base)], INK, 3.0)
    _planter(p, WALL_LEV, -0.78, 2.6, 0.6, 503)                         # a trough at the wall's foot, left



STREET_LEV = Level(h=1.6, hz=470.0, f=812.0)   # note 56's street: the vanishing point above Link's cap in S11


def _street_side(p, sg, houses, t, style='timber'):
    """One side of the street (sg -1 left, +1 right) in one-point perspective to (540, 470): house fronts running
    away from us, each its own plaster, timber posts and floor beams, shuttered windows with flower boxes, a red
    tiled eave along the top (ref 25)."""
    def at(u, v):                                                       # u 0 near .. 1 far; v 0 ground .. 1 eaves
        x = 540 + sg * (310 - 240 * u ** 0.8)
        g, top = 1000 - 480 * u ** 0.8, 40 + 330 * u ** 0.8
        return x, g + (top - g) * v
    for k, (u0, u1, col, floors, sd) in enumerate(houses):
        p.poly([at(u0, 0), at(u1, 0), at(u1, 1), at(u0, 1)], col, INK, 2.0)
        p.poly([at(u0, 0), at(u1, 0), at(u1, 0.28), at(u0, 0.28)], mix(col, WALLSTONE, 0.6), INK, 1.6)
        for f in range(1, floors + 1):                                  # floor beams
            v = 0.28 + (0.72 / (floors + 0.3)) * f
            p.line([at(u0, v), at(u1, v)], (96, 66, 44), 3.0)
        for u in (u0 + 0.02, u1 - 0.02):
            p.line([at(u, 0.28), at(u, 0.98)], (96, 66, 44), 3.0)
        fl = [0.28 + (0.72 / (floors + 0.3)) * f for f in range(floors + 1)]
        if style == 'timber':                                           # critique r3 / note 61: braces between beams
            nb = max(2, int((u1 - u0) * 8))
            for f in range(floors):
                for b in range(nb):
                    a_, b_ = u0 + (u1 - u0) * b / nb, u0 + (u1 - u0) * (b + 1) / nb
                    p.line([at(a_, fl[f] + 0.01), at(a_ + (b_ - a_) * 0.25, fl[f] + 0.04)], (96, 66, 44), 2.4)
                    p.line([at(b_, fl[f] + 0.01), at(b_ - (b_ - a_) * 0.25, fl[f] + 0.04)], (96, 66, 44), 2.4)
        else:                                                           # stone below, a balcony rail on floor one
            for q in range(1, 5):
                p.line([at(u0, 0.28 * q / 5), at(u1, 0.28 * q / 5)], dk(WALLSTONE, 0.85), 1.4)
            v = fl[1] - 0.02
            p.poly([at(u0 + 0.03, v), at(u1 - 0.03, v), at(u1 - 0.03, v + 0.05), at(u0 + 0.03, v + 0.05)],
                   (92, 70, 52), INK, 1.6)
            for q in range(int((u1 - u0) * 30)):
                uu = u0 + 0.03 + (u1 - u0 - 0.06) * q / max(1, int((u1 - u0) * 30) - 1)
                p.line([at(uu, v + 0.05), at(uu, v + 0.12)], (92, 70, 52), 1.8)
            p.line([at(u0 + 0.03, v + 0.12), at(u1 - 0.03, v + 0.12)], (92, 70, 52), 2.6)
        nw = max(1, int((u1 - u0) * 9))
        for f in range(floors):                                         # windows, shutters, flower boxes
            v0 = 0.33 + (0.72 / (floors + 0.3)) * f
            v1 = v0 + 0.13
            for w in range(nw):
                a, b = u0 + (u1 - u0) * (w + 0.3) / nw, u0 + (u1 - u0) * (w + 0.7) / nw
                p.poly([at(a, v0), at(b, v0), at(b, v1), at(a, v1)], (70, 96, 140), INK, 1.4)
                p.poly([at(a, v0 - 0.015), at(b, v0 - 0.015), at(b, v0 + 0.01), at(a, v0 + 0.01)], (120, 80, 50), None)
                rr = random.Random(sd * 31 + f * 7 + w)
                for q in range(4):
                    fx, fy = at(a + (b - a) * (q + 0.5) / 4, v0 + 0.005)
                    p.ell(fx, fy - 3, 5 * (1 - 0.5 * a), 5 * (1 - 0.5 * a), rr.choice([(214, 50, 60), (150, 70, 170)]), INK, 1.0)
        if k == 0 and style != 'timber':                                # a red-and-white striped shop awning
            n_ = 6
            for q in range(n_):
                a_, b_ = u0 + (u1 - u0) * (0.1 + 0.8 * q / n_), u0 + (u1 - u0) * (0.1 + 0.8 * (q + 1) / n_)
                (xa, ya), (xb, yb) = at(a_, 0.31), at(b_, 0.31)
                dd = -sg * 70
                p.poly([(xa, ya), (xb, yb), (xb + dd * (1 - b_), yb + 40 * (1 - b_)), (xa + dd * (1 - a_), ya + 40 * (1 - a_))],
                       (200, 50, 50) if q % 2 else (244, 238, 226), INK, 1.4)
        if k == 1:                                                      # a hanging shop sign on a bracket
            bx, by = at(u0 + 0.02, 0.5)
            p.line([(bx, by), (bx - sg * 50, by)], (60, 50, 40), 3.0)
            p.poly(quad(bx - sg * 50 - 18, by + 6, bx - sg * 50 + 18, by + 40), GOLD if sg < 0 else (60, 110, 70),
                   INK, 1.6)
        door = (u0 + 0.35 * (u1 - u0), u0 + 0.55 * (u1 - u0))           # a round-topped door
        p.poly([at(door[0], 0), at(door[1], 0), at(door[1], 0.22), at(door[0], 0.22)], (110, 70, 44), INK, 1.6)
        e0, e1 = at(u0, 1.0), at(u1, 1.0)                               # the eave
        p.poly([e0, e1, (e1[0] + sg * 18 * (1 - u1), e1[1] - 26 * (1 - 0.6 * u1)),
                (e0[0] + sg * 40, e0[1] - 60)], (196, 92, 56), INK, 2.0)


def _swag_wall(p, x0, x1, ytop, ybot, t):
    """A stone balustrade with blue drapes swagged along it, gold-trimmed (ref 25), square posts at each end with
    a flower urn on top."""
    p.poly(quad(x0, ytop, x1, ybot), (214, 208, 196), INK, 2.0)
    n = 6
    for k in range(n):                                                  # balusters
        bx = x0 + (x1 - x0) * (k + 0.5) / n
        p.poly(curve([(bx - 9, ytop + 16), (bx + 9, ytop + 16), (bx + 13, ytop + 45), (bx + 7, ybot - 10),
                      (bx - 7, ybot - 10), (bx - 13, ytop + 45)], 3), (230, 226, 216), INK, 1.4)
    p.poly(quad(x0 - 6, ytop - 6, x1 + 6, ytop + 14), (232, 228, 218), INK, 2.0)
    for k in range(3):                                                  # the drapes
        a, b = x0 + (x1 - x0) * k / 3, x0 + (x1 - x0) * (k + 1) / 3
        sag = 38 + 4 * math.sin(t * 2 + k)
        top = [(a, ytop + 12), (b, ytop + 12)]
        bot = [(a + (b - a) * u, ytop + 14 + sag * math.sin(math.pi * u)) for u in np.linspace(1, 0, 9)]
        p.poly(top + bot, BANNER, INK, 1.6)
        p.line(bot, GOLD, 3.0)
    for px in (x0, x1):                                                 # posts and urns
        p.poly(quad(px - 18, ytop - 30, px + 18, ybot), (222, 216, 204), INK, 2.0)
        p.poly(quad(px - 22, ytop - 38, px + 22, ytop - 28), (236, 232, 222), INK, 1.6)
        p.poly(curve([(px - 16, ytop - 38), (px + 16, ytop - 38), (px + 10, ytop - 62), (px - 10, ytop - 62)], 3),
               (200, 190, 176), INK, 1.4)
        for q in range(5):
            p.ell(px - 14 + 7 * q, ytop - 68 - 6 * (q % 2), 8, 8, (214, 50, 60) if q % 2 else (150, 70, 170), INK, 1.0)


def town_reverse(img, p, cam, t):
    """S11 (notes 56, 59: the camera turned 180 to Link; modelled on Sam's picture, ref 25): the street out of the
    square climbing away from us; house fronts with flower boxes down both sides;
    shallow steps; a row of houses closing its far end (no castle: note 61); nearer, a stone balustrade each side hung with blue gold-trimmed drapes, a tall blue banner on
    a pole either side framing Link, stone planters of purple flowers at their feet."""
    _sky(p, -400, 900, 9)
    _cloud(p, 520, 200, 160, 491)
    for k, (x0, x1, top, rh, ci, kw) in enumerate((                    # note 61 (Sam): no castle (it would be a
            (440, 500, 400, 40, 4, dict(floors=2, wins=1, roof='gable', frame='brace')),   # second one): the street
            (500, 572, 380, 46, 0, dict(floors=2, wins=2, roof='side', frame='x')),        # ends in a far row of
            (572, 640, 410, 36, 2, dict(floors=2, wins=1, roof='gable', frame='studs')))): # houses across it
        _house(img, p, x0, x1, 520, top, rh, PLASTER[ci], 495 + k, **kw)
    haze(img, cam, 300, 560, (230, 236, 244), 0.3)
    p.poly([(-200, 1100), (230, 1000), (470, 520), (610, 520), (850, 1000), (1280, 1100), (1280, 2000), (-200, 2000)],
           mix((206, 200, 188), FLAG, 0.65), None)                      # the paving: Fable r3 #41, the square's
                                                                        # blue-grey slabs (it was cream here only)
    for k in range(9):                                                  # joints running away to the vanishing point
        bx = -100 + k * 160
        p.line([(bx, 1300), (540 + (bx - 540) * 0.12, 540)], FLAG_J, 1.6)
    y = 540
    while y < 1300:
        p.line([(-200, y), (1280, y)], FLAG_J, 1.4)
        y += 10 + (y - 520) * 0.18
    for k in range(4):                                                  # shallow steps up the street
        y0 = 600 + 22 * k
        w = 80 + 22 * k
        p.poly(quad(540 - w, y0, 540 + w, y0 + 8), (226, 222, 212), None)
        p.line([(540 - w, y0 + 8), (540 + w, y0 + 8)], (150, 144, 134), 2.0)
    _street_side(p, -1, [(0.0, 0.42, PLASTER[1], 3, 1), (0.42, 0.72, PLASTER[3], 2, 2), (0.72, 1.0, PLASTER[0], 3, 3)], t)
    _street_side(p, 1, [(0.0, 0.34, PLASTER[2], 2, 4), (0.34, 0.6, PLASTER[4], 3, 5), (0.6, 0.82, PLASTER[3], 2, 6),
                        (0.82, 1.0, PLASTER[1], 3, 7)], t, style='stone')   # critique r3: each side its own build
    _bunting(p, 440, 440, 640, 440, 22, 9, t)
    for x, d, c, sd in ((-0.9, 21.0, (90, 120, 150), 21), (0.4, 30.0, (120, 140, 90), 23),   # remakes note 68: on
                        (-0.5, 15.0, (170, 110, 70), 24), (0.9, 12.5, (110, 80, 140), 25)):   # the paving, not in the
                                                                        # house fronts; two fewer (it was busy)
        _townsfolk(p, x, d, c, sd, lev=STREET_LEV)
    _swag_wall(p, 200, 400, 800, 900, t)
    _swag_wall(p, 680, 880, 800, 900, t)
    for bx, sg in ((300, -1), (780, 1)):                                # the banners on their poles
        p.line([(bx - sg * 70, 960), (bx - sg * 70, 170)], (70, 60, 50), 5.0)
        p.line([(bx - sg * 70, 180), (bx + sg * 10, 180)], (70, 60, 50), 4.0)
        p.ell(bx - sg * 70, 166, 8, 8, GOLD, INK, 1.4)
        _banner(p, bx - sg * 15, 186, 100, 330, t)
    for px in (250, 830):                                               # planters of purple flowers
        p.poly(quad(px - 70, 900, px + 70, 1000), (180, 174, 164), INK, 2.2)
        rr = random.Random(px)
        for q in range(14):
            p.ell(px - 60 + rr.uniform(0, 120), 895 - rr.uniform(0, 30), 11, 11,
                  rr.choice([(150, 70, 170), (190, 120, 210), (120, 60, 150)]), INK, 1.0)


TOWN_VIEWS = {'square': town_square, 'wall': town_wall, 'reverse': town_reverse}


def town(img, cam, view, t=0.0):
    p = B.Pen(img, cam)
    TOWN_VIEWS[view](img, p, cam, t)


# ================================================================================================ stage
def _camp_mark(x, d, z=0.0):
    sx, sy = CAMP.p(x, d, z)
    return sx, sy, CAMP.ppm(d)


def _town_mark(x, d):
    sx, sy = TOWN.p(x, d)
    return sx, sy, TOWN.ppm(d)


STAGE = {      # where the cast stand: (screen x, ground y, pixels per metre). KG's perch is his feet on the branch.
    'forest_up': {'kg': (640, branch_y(640), 420.0)},
    'forest_down': {'link': (560, 1330, down_ppm(1330)), 'navi': (700, 1050, down_ppm(1330))},
    'forest_close': {'link': (540, 2300, 1100.0)},            # a close-up: his feet well below the frame
    'forest_edge': {'gunman': (140, 2950, 1250.0)},       # pass 3: a close-up (he was small, lower left); left
                                                          # so his muzzle stays in frame
    'camp': {'kg': _camp_mark(0.0, 4.6), 'link': _camp_mark(-1.25, 5.0), 'gunman1': _camp_mark(3.0, 9.3, 4.4),
             'gunman2': _camp_mark(1.2, 4.2), 'gunman3': _camp_mark(-0.95, 3.3)},   # note 32 (Sam): nobody behind
                                                                    # KG. He comes in through the gate; the lookout is
                                                                    # up in the tower, one man runs in lower left
                                                                    # (nearest the lens), one middle right, level
                                                                    # with him; Link follows through the gate
    'town_square': {n: _town_mark(x, d) for n, x, d in (('zelda', -0.40, 4.0), ('malon', 0.08, 4.2), ('ruto', 0.55, 3.95),
                                                          ('goron', 1.15, 4.3), ('saria', 1.68, 4.05))},
                                                                    # pass 2: right and staggered, KG wholly in front
    'town_wall': {'link': (400, WALL_VIEW['base'], WALL_VIEW['ppm']),       # on the cobbles: the shot lifts him
                  'kg': (720, WALL_VIEW['base'], WALL_VIEW['ppm'])},      # pass 2: closer, not cut by the edge
}
CAMP_MARKS = {'kg': (0.0, 4.6), 'link': (-1.25, 5.0)}   # the same marks in metres (x, depth), for the moves
STAGE['camp_open'] = dict(STAGE['camp'])               # S8-S9: the same yard, the gate blown in
ON_HIGH = {('camp', 'gunman1'), ('camp_open', 'gunman1')}   # the tower lookout: no ground shadow
STAGE['town_square']['kg'] = _town_mark(-0.88, 2.55)   # in front, below the line, presenting it (pass 2: whole)


# ================================================================================================ boxes (rule 83)
def _box(level, x0, x1, d, z0, z1):
    a, b = level.p(x0, d, z0), level.p(x1, d, z1)
    return (a[0], b[1], b[0], a[1])


SET_BOXES = [   # the camp's solid things, screen px (the S7 camera); nothing may overlap unless meant
    ('blue container', _box(CAMP, -5.0, -2.6, 7.4, 0, 2.6)),
    ('orange container', _box(CAMP, -5.0, -2.6, 7.6, 2.6, 5.2)),
    ('crates', _box(CAMP, -2.65, -1.75, 6.6, 0, 1.6)),
    ('barrels', _box(CAMP, -1.65, -1.0, 6.4, 0, 0.9)),
    ('camo net', _box(CAMP, 3.7, 6.2, WALL_D, 0.3, 2.4)),
    ('tyres', _box(CAMP, 4.34, 5.06, 9.3, 0, 0.72)),
    ('gate', _box(CAMP, -GATE_HALF, GATE_HALF, WALL_D, 0, 2.4)),
    ('watchtower', _box(CAMP, TOWER[0] - 1.1, TOWER[0] + 1.1, TOWER[1], 0, 6.9)),
    ('lean-to', _box(CAMP, -2.9, -0.7, 6.0, 0, 2.7)),
]
SET_MEANT = [
    ('blue container', 'orange container', 'the orange one sits stacked on top of the blue (ref 23)'),
    ('crates', 'blue container', 'the crates stand in front of it, 0.8 m nearer the lens'),
    ('barrels', 'gate', 'the barrels stand 3.6 m nearer the lens, below the gate on screen'),
    ('camo net', 'watchtower', 'the net hangs on the wall 1 m behind the tower'),
    ('tyres', 'camo net', 'the tyres stand at the wall foot in front of the net'),
    ('tyres', 'watchtower', 'the tyres stand right of the tower, 0.3 m nearer'),
    ('lean-to', 'crates', 'the crates stand under it'), ('lean-to', 'barrels', 'the barrels stand under it'),
    ('lean-to', 'blue container', 'it stands against the container, 1.4 m nearer'),
    ('lean-to', 'orange container', 'its roof meets the stacked container behind'),
    ('lean-to', 'gate', 'its right post stands 4 m nearer than the gate'),
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
         items=[('grey-blue paving slabs', 'done: in perspective, rows shrinking away'),
                ('a stone fountain with a statue in the middle', 'done: basin, two tiers, an invented statue with a jug'),
                ('timber-framed houses with red-orange tiled roofs', 'done: six, each its own build'),
                ('balconies and flower boxes', 'done'),
                ('a palm-like tree left', 'done: in a grass bed with a stone kerb'),
                ('a red-striped market tent', 'done: with a counter of fruit'),
                ('barrels and sacks', 'done'),
                ('townsfolk', 'done: nine, with arms, legs, hats, a basket'),
                ('the castle pale and hazy far behind', 'done'),
                ('pale blue banners with a gold frame and crest, bunting high', 'done: an invented crest (a bird in a shield)')]),
    dict(place='The town wall (S12, S13)', refs=['22-town.jpg'], at='town_wall',
         items=[('stone walls', 'done: rough grey blocks, a plinth and a ledge for depth'),
                ('tall blue banners with a gold crest', 'done: one on a bracket'),
                ('flower boxes, red and purple', 'done: under the window'),
                ('bunting across', 'done'),
                ('paving slabs at the foot', 'done'),
                ('shuttered window', 'done: blue shutters'),
                ('stone balustrades with blue-and-gold drapes', 'left out: the wall shot is tight; the banner carries it'),
                ('stone flower troughs', 'done: one at the foot'),
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
    elif at.startswith('camp'):
        camp(img, cam, t, 1.0 if at == 'camp_open' else gate)
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
    elif at.startswith('camp'):
        camp(img, cam, t, 1.0 if at == 'camp_open' else gate)
    else:
        town(img, cam, at.split('_')[1], t)
    for who, (x, y, ppm) in st.items():                                 # the soft foot shadows first (Sam Q3)
        if who != 'navi' and at != 'forest_up' and (at, who) not in ON_HIGH:   # Navi is a flying light: none;
                                                                         # KG's branch: kg_on_branch
            foot_shadow(img, cam, x, y, ppm, SHADOW_W['gunman' if who.startswith('gunman') else who],
                        clip=branch_poly() if at == 'forest_up' else None)
    for who, (x, y, ppm) in sorted(st.items(), key=lambda kv: kv[1][1]):
        s = s_for(ppm)
        if who == 'kg' and at == 'forest_up':
            wings, mood = KG_BEAT[at]
            kg_on_branch(img, cam, x, s, mood=mood, wings=wings, t=t)
        elif who == 'kg':
            # standing, his talons touch about 272 units below his middle (remakes_creatures.kg stand)
            view = 'side' if at in ('town_wall',) else 'front'
            wings, mood = KG_BEAT.get(at, ('fold', 'kindly'))
            CR.kg(img, cam, x, y - 272 * s, s, view=view, perched=False, stand=True, wings=wings,   # pass 3: he
                  band=at in ('camp', 'camp_open', 'town_wall'), mood=mood,                       # floated
                  flip=-1 if at == 'town_wall' else 1)
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
                fl = -1 if (at.startswith('camp') and x > 540) else 1
                RC.person(img, B.Local(cam, x, 0, 1.0, fl) if fl < 0 else cam, (0 if fl < 0 else x), y - 928 * k, s, sp,
                          yaw=j['_yaw'], j=j)
            else:
                RC.person(img, cam, x, y - 928 * k, s, sp)
    if at.startswith('forest'):
        forest_front(img, cam, at.split('_')[1], t)
    elif at.startswith('camp'):
        camp_front(img, cam, t)
    return img.resize((W, H), Image.LANCZOS)


KG_BEAT = {'forest_up': ('wide', 'hype'), 'camp': ('gun', 'war'), 'camp_open': ('gun', 'war'), 'town_square': ('present', 'show'),
           'town_wall': ('fold', 'fury')}       # each set sheet shows KG as his shot has him (line 1, 7, 11, 13)

SETS = {'forest': ('forest_up', 'forest_down', 'forest_close', 'forest_edge'), 'camp': ('camp', 'camp_open'),
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


# ================================================================================================ options (rule 87)
SURVIVORS = [   # (number, what survived three passes, view, crop box in the frame, [(letter, label, settings)])
    (1, 'S1 reads level; KG doesn\'t tower (treetops below him, open sky)', 'forest_up', None,
     [('A', 'look straight up: trunks rise from below, sky only through the canopy, Link\'s cap in the corner (ref 01)',
       dict(up='cap')),
      ('B', 'look straight up, no cap', dict(up='steep')),
      ('C', 'as now, KG a third bigger', dict(kg_big=1.35))]),
    (2, 'S4/S6: the light shafts don\'t read', 'forest_close', None,
     [('A', 'wood darker round them, the shafts bright, a pool where each lands', dict(shafts='dark')),
      ('B', 'bright shafts and pools, wood as now', dict(shafts='strong')),
      ('C', 'no shafts: sun dapples on the grass, path and stump', dict(shafts='dapple'))]),
    (3, 'S5: grey, unlike the rest of the forest; trunks even poles', 'forest_edge', None,
     [('A', 'the forest\'s own green-gold; trunks thin far off to one huge near one', dict(edge='warm')),
      ('B', 'soft green, far trunks fading into mist', dict(edge='mist'))]),
    (4, 'Camp: the walls read as a plank fence; no middle layer', 'camp', None,
     [('A', 'deep corrugated tin with bolts, and a tin lean-to over the crates', dict(wall='shelter')),
      ('B', 'deep corrugated tin only', dict(wall='tin'))]),
    (5, 'Town: the fountain pale and statue-less (ref 21: dark stone, statues)', 'town_square', (300, 330, 780, 1183),
     [('A', 'dark weathered stone, a hooded maiden pouring from a jug', dict(fountain='dark')),
      ('B', 'dark stone, a green-bronze bird with spread wings (the banners\' bird)', dict(fountain='bird'))]),
    (6, 'S12: KG\'s spit reads as flowers he\'s offering', 'town_wall', (240, 900, 780, 1860),
     [('A', 'a fine spray of tiny drops', dict(spit='spray')),
      ('B', 'foamy flecks and a string of drool', dict(spit='foam')),
      ('C', 'one gob flung out, speed lines', dict(spit='glob'))]),
]


def _with_opts(view, opts):
    import remakes_creatures as CR
    keep, kst, ksp = dict(OPT), dict(STAGE[view]), CR.SPIT
    try:
        OPT.update({k: v for k, v in opts.items() if k in OPT})
        CR.SPIT = opts.get('spit', CR.SPIT)
        if 'kg_big' in opts:
            x, y, ppm = STAGE[view]['kg']
            STAGE[view]['kg'] = (x, y, ppm * opts['kg_big'])
        return with_cast(view).convert('RGB')
    finally:
        OPT.clear(), OPT.update(keep)
        STAGE[view].clear(), STAGE[view].update(kst)
        CR.SPIT = ksp


def options(out):
    """ONE sheet for Sam (rule 87): every three-pass survivor in a row, 'now' first, then its options, my pick as A."""
    import remakes_creatures as CR
    pw, ph, gap = 450, 800, 24
    cols = 1 + max(len(o) for *_, o in SURVIVORS)
    rows = []
    for num, what, view, box, opts in SURVIVORS:
        ims = [('now', 'as built', {})] + [(l, lab, o) for l, lab, o in opts]
        tiles = []
        for l, lab, o in ims:
            im = _with_opts(view, o)
            if box:
                im = im.crop(box)
            tiles.append((l, lab, im.resize((pw, ph), Image.LANCZOS)))
        rows.append((num, what, tiles))
    W = gap + cols * (pw + gap)
    rh = 70 + ph + 160
    sheet = Image.new('RGB', (W, 110 + len(rows) * rh), (250, 248, 244))
    d = ImageDraw.Draw(sheet)
    d.text((gap, 14), 'Remakes: the six things that survived three critique passes.', font=CR._font(30), fill=(30, 30, 30))
    d.text((gap, 56), 'Pick a letter for each (A, in red, is my pick).', font=CR._font(26), fill=(60, 60, 60))
    y = 110
    for num, what, tiles in rows:
        d.text((gap, y + 14), f'{num}. {what}', font=CR._font(30), fill=(20, 20, 20))
        for i, (l, lab, im) in enumerate(tiles):
            x = gap + i * (pw + gap)
            sheet.paste(im, (x, y + 64))
            tag = 'Now' if l == 'now' else f'{num}{l}'
            d.text((x, y + 64 + ph + 10), tag, font=CR._font(30), fill=(150, 40, 40) if l == 'A' else (30, 30, 30))
            words, line, ly = lab.split(), '', y + 64 + ph + 48
            for w_ in words:                                            # wrap the label
                if d.textlength(line + ' ' + w_, font=CR._font(20)) > pw:
                    d.text((x, ly), line.strip(), font=CR._font(20), fill=(60, 60, 60))
                    line, ly = '', ly + 24
                line += ' ' + w_
            d.text((x, ly), line.strip(), font=CR._font(20), fill=(60, 60, 60))
        y += rh
    sheet.save(out, quality=88)
    return out


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'alone':
        print(alone(sys.argv[2], sys.argv[3], '--bare' not in sys.argv))
    elif cmd == 'options':
        print(options(sys.argv[2]))
    elif cmd == 'one':
        (with_cast(sys.argv[2]) if '--bare' not in sys.argv else picture(sys.argv[2])).convert('RGB').save(sys.argv[3],
                                                                                                          quality=90)
