#!/usr/bin/env python3
"""MAP  Islamocommunism's Oval Office (Sam, 4 Nov: "make the MidTerminal Oval Office respectfully communist and
Islamic"; "and change the flag"). MidTerminal's room (midterminal_set) redressed: importing this module swaps a few
of that room's drawing pieces for the film's own, so MidTerminal itself never imports it and stays as it was.

Respectful means: Islamic art through its geometry (eight-point stars, pointed arches, tilework, pierced brass
lanterns), communism through its emblems (red stars, wheat sheaves, the red banner), and NO holy writing, no
calligraphy, no religious figures, no real person's portrait anywhere.

What changes (each one also listed as "Added" / "Lost" in notes/islamocommunism.md):
  - flags: the US flag -> the film's flag (red and green stripes, a navy canton with gold hammers and sickles and white
    crescents with stars); the President's navy flag -> a red banner with a gold star-and-crescent; the eagle finials
    -> gold crescents
  - windows: pointed-arch heads, the corners above the arch in blue tiles with white eight-point stars
  - the gold valance: a band of small eight-point stars along its board
  - the dado: blue-and-white tilework (eight-point stars) in place of the white panels
  - the carpet: a deep green field (red and gold border, its flower garland kept); the seal: a gold eight-point star
    holding a red five-point star, in a gold ring with wheat ears
  - the Resolute desk's oval carving: a gold eight-point star
  - the portraits (generic gentlemen): original poster-style paintings (a sun rising over a domed hall, a factory and
    a wheat field; no words)
  - on the low table behind the desk: a brass samovar with tea glasses beside the family photos
  - two pierced brass lanterns hanging between the windows
  - Lost: the two gold-seat chairs facing the desk (their backs hid the desk in the flat front view)

    python3 source/islamocommunism_office.py test OUT.jpg    the redressed room from the film's flat cameras

Map: colours 40 | helpers 55 | flags 85 | windows, valance, dado 150 | carpet 215 | posters 265 | desk 300 |
samovar, lanterns 335 | install 400 | test 425
"""
import functools
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import midterminal_set as MS    # noqa: E402
from sets import Face, obox, cylinder, dk, lt   # noqa: E402
from ed import INK               # noqa: E402

# ---------------------------------------------------------------------------------------------- colours
F_RED = (190, 34, 40)
F_GREEN = (22, 124, 66)
F_NAVY = (26, 40, 96)
GOLD, GOLD_D, GOLD_L = MS.GOLD, MS.GOLD_D, MS.GOLD_L
TILE = (32, 86, 160)             # cobalt tile
TILE_D = (22, 60, 118)
WHITE = MS.WHITE
BRASS = (198, 150, 64)
BRASS_D = (150, 106, 40)
TEA = (176, 70, 34)
CARPET = (28, 92, 62)            # deep green field
CARPET_D = (20, 70, 48)


# ---------------------------------------------------------------------------------------------- helpers
def _mpd(a):
    """Metres along the wall per degree at wall angle a (near enough on this gentle oval)."""
    x, _, z = MS.wp(a, 0.0)
    return math.hypot(x, z) * math.pi / 180.0


def wall_pt(a, s, y, inset):
    """A wall point s metres along the wall from angle a, at height y."""
    return MS.wp(a + s / _mpd(a), y, inset)


def star_pts(cx, cy, r, n=8, inner=0.765, rot=0.0):
    """A star's outline in 2D: n points (an eight-point star is two squares overlapped)."""
    out = []
    for k in range(2 * n):
        rr = r if k % 2 == 0 else r * inner
        t = rot + math.pi * k / n
        out.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    return out


def wall_star(img, cm, a, y, r, inset, fill, line=None, lw=1.2, n=8, inner=0.765):
    pts = [wall_pt(a, sx, sy, inset) for sx, sy in star_pts(0.0, y, r, n, inner, math.pi / 8 if n == 8 else -math.pi / 2)]
    MS.poly(img, cm, pts, fill, line, lw)


# ---------------------------------------------------------------------------------------------- flags
def _crescent(cm, p, cx, cy, z, r, col, back):
    """A crescent opening right (a disc with a smaller disc taken out, drawn as the back colour over it)."""
    cm.poly(p, [(cx + r * math.cos(t), cy + r * math.sin(t), z) for t in np.linspace(0, 6.28, 14)], col, None)
    cm.poly(p, [(cx + 0.35 * r + 0.8 * r * math.cos(t), cy + 0.8 * r * math.sin(t), z - 0.0005)
                for t in np.linspace(0, 6.28, 14)], back, None)


def _star3(cm, p, cx, cy, z, r, col, n=5):
    cm.poly(p, [(x, y, z) for x, y in star_pts(cx, cy, r, n, 0.42, math.pi / 2)], col, None)


def flag_parts(x, z, kind):
    """The room's two flags on tall poles, hanging in folds, gold crescent finials: 'us' is now the film's flag (red
    and green stripes, a navy canton with gold hammers and sickles and white crescents with stars: the same flag as
    the White House's); 'pres' is a red banner with a gold star-and-crescent and a gold fringe."""
    parts = [cylinder((x, 0, z), 0.16, 0.06, {'side': GOLD_D, 'top': GOLD}, n=10),
             cylinder((x, 0.06, z), 0.02, 2.7, {'side': (150, 110, 60), 'top': GOLD}, n=6)]
    top, low = 2.55, 1.0

    def cloth(img, cm, p):
        n, w = 7, 0.5

        def edge(e):
            return x - 0.03 + w * e / n, z - 0.05 * (e % 2), low + 0.25 * (e / n) + 0.04 * (e % 2)
        for k in range(n):
            (u0, z0, h0), (u1, z1, h1) = edge(k), edge(k + 1)
            shade = 1.0 if k % 2 == 0 else 0.88
            base = F_GREEN if kind == 'us' else F_RED
            cm.poly(p, [(u0, top, z0), (u1, top, z1), (u1, h1, z1), (u0, h0, z0)], dk(base, shade), INK, 1.4)
            if kind == 'us':                           # red stripes over the green (13 in all)
                for y in np.arange(max(h0, h1) + 0.1, top, 0.16):
                    cm.poly(p, [(u0, y, z0 - 0.001), (u1, y, z1 - 0.001), (u1, y + 0.08, z1 - 0.001),
                                (u0, y + 0.08, z0 - 0.001)], dk(F_RED, shade), None)
            else:                                      # the gold fringe
                cm.poly(p, [(u0, h0, z0 - 0.001), (u1, h1, z1 - 0.001), (u1, h1 + 0.07, z1 - 0.001),
                            (u0, h0 + 0.07, z0 - 0.001)], GOLD, None)
        zf = z - 0.06
        if kind == 'us':
            cm.poly(p, [(x - 0.03, top, zf), (x + 0.24, top, zf), (x + 0.24, top - 0.55, zf), (x - 0.03, top - 0.55, zf)],
                    F_NAVY, INK, 1.4)
            for k in range(6):                         # alternating: gold hammer-and-sickle marks, white crescents
                cx, cy = x + 0.03 + 0.075 * (k % 3), top - 0.12 - 0.2 * (k // 3) - (0.08 if k % 2 else 0)
                if k % 2 == 0:
                    _crescent(cm, p, cx, cy, zf - 0.001, 0.028, WHITE, F_NAVY)
                    _star3(cm, p, cx + 0.022, cy, zf - 0.002, 0.012, WHITE)
                else:
                    cm.line(p, [(cx - 0.02, cy - 0.02, zf - 0.001), (cx + 0.02, cy + 0.02, zf - 0.001)], GOLD, 2.0)
                    cm.poly(p, [(cx + 0.025 * math.cos(t), cy + 0.025 * math.sin(t), zf - 0.002)
                                for t in np.linspace(math.pi * 0.6, math.pi * 1.9, 8)] +
                            [(cx + 0.017 * math.cos(t), cy + 0.017 * math.sin(t), zf - 0.002)
                             for t in np.linspace(math.pi * 1.9, math.pi * 0.6, 8)], GOLD, None)
        else:
            cx, cy = x + 0.2, top - 0.55
            _crescent(cm, p, cx, cy, zf, 0.12, GOLD, F_RED)
            _star3(cm, p, cx + 0.1, cy, zf - 0.002, 0.05, GOLD)
        # the finial: a gold ball and a crescent opening upwards
        cm.poly(p, [(x + 0.05 * math.cos(t), 2.82 + 0.05 * math.sin(t), z) for t in np.linspace(0, 6.28, 10)], GOLD, INK, 1.4)
        outer = [(x + 0.11 * math.cos(t), 3.0 + 0.11 * math.sin(t), z) for t in np.linspace(math.pi * 1.05, math.pi * 1.95, 10)]
        inner = [(x + 0.08 * math.cos(t), 3.04 + 0.07 * math.sin(t), z) for t in np.linspace(math.pi * 1.95, math.pi * 1.05, 10)]
        cm.poly(p, outer + inner, GOLD, INK, 1.2)
    parts.append([Face([(x, 2.0, z)] * 3, None, None, None, 0, None)])
    parts[-1][0].draw = lambda img, cm, p: cloth(img, cm, p)
    return parts


# ---------------------------------------------------------------------------------------------- windows, valance, dado
_window0, _valance0, _walls0 = MS.window, MS.valance, MS.walls


def window(img, cm, c):
    """MidTerminal's window, its head made a pointed arch: the corners above the arch in blue tiles with white stars."""
    _window0(img, cm, c)
    a0, a1 = c - MS.WIN_HALF + 1.5, c + MS.WIN_HALF - 1.5
    h = (a1 - a0) / 2 * _mpd(c)                       # half the glass's width, metres
    y1, rise = 4.0, 0.95
    ys = y1 - rise
    k = rise / (math.sqrt(3) * h)                     # an equilateral pointed arch, squashed to `rise`
    left = [(h - 2 * h * math.cos(t), ys + k * 2 * h * math.sin(t)) for t in np.linspace(0, math.pi / 3, 14)]
    right = [(-sx, sy) for sx, sy in left]
    ins = 0.016
    for arc, corner in ((left, -h), (right, h)):
        pts = [(corner, y1), (corner, ys)] + arc
        MS.poly(img, cm, [wall_pt(c, sx, sy, ins) for sx, sy in pts], TILE, INK, 1.8)
        sx, sy = corner * 0.78, y1 - 0.2                # one white star in each corner
        MS.poly(img, cm, [wall_pt(c, px, py, ins + 0.001) for px, py in star_pts(sx, sy, 0.07, 8, 0.765, math.pi / 8)],
                WHITE, None)
    MS.lines(img, cm, [wall_pt(c, sx, sy, ins + 0.002) for sx, sy in left + right[::-1]], WHITE, 5.0)   # the moulding
    MS.lines(img, cm, [wall_pt(c, sx, sy, ins + 0.003) for sx, sy in left + right[::-1]], INK, 1.4)


def valance(img, cm):
    """MidTerminal's gold swag valance with a band of small eight-point stars along its board."""
    _valance0(img, cm)
    lo, hi = MS.WINDOWS[0] - MS.WIN_HALF - 6, MS.WINDOWS[-1] + MS.WIN_HALF + 6
    for a in np.arange(lo, hi + 0.01, 2.2):
        wall_star(img, cm, a, 4.9, 0.075, 0.147, GOLD_L, GOLD_D, 1.2)


def walls(img, cm):
    """MidTerminal's walls with the dado tiled: cobalt with white eight-point stars, a border line above."""
    _walls0(img, cm)
    for a0 in np.arange(-180, 180, 3.0):
        if MS._skip(a0) or MS._skip(a0 + 3):
            continue
        MS.poly(img, cm, MS.band(a0, a0 + 3.0, 0.16, MS.DADO_H - 0.1, 0.007), TILE, None)
    for a in np.arange(-180, 180, 4.5):
        if MS._skip(a - 1.5) or MS._skip(a + 1.5):
            continue
        wall_star(img, cm, a, (0.16 + MS.DADO_H - 0.1) / 2, 0.2, 0.008, WHITE, TILE_D, 1.0)
        wall_star(img, cm, a, (0.16 + MS.DADO_H - 0.1) / 2, 0.08, 0.009, TILE_D, None)
    for y in (0.16, MS.DADO_H - 0.1):
        MS.lines(img, cm, [MS.wp(a, y, 0.009) for a in np.arange(-180, 181, 3) if not MS._skip(a)], INK, 1.6)


# ---------------------------------------------------------------------------------------------- the carpet
@functools.lru_cache(maxsize=1)
def carpet_art():
    """The oval carpet from above (1 px a cm): a deep green field, a red and gold border with the flower garland kept,
    a ring of small gold eight-point stars, and the seal: a gold eight-point star holding a red five-point star, in a
    gold ring with wheat ears. No words."""
    RX, RZ = 3.8, 4.8
    W, H = int(RX * 200), int(RZ * 200)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = W / 2, H / 2

    def ell(k, fill, outline=None, width=0):
        d.ellipse([cx - cx * k, cy - cy * k, cx + cx * k, cy + cy * k], fill=fill, outline=outline, width=width)
    ell(1.0, F_RED + (255,), INK + (255,), 4)
    ell(0.985, GOLD + (255,))
    ell(0.97, F_RED + (255,))
    rng = np.random.default_rng(5)
    for t in np.linspace(0, 2 * math.pi, 120, endpoint=False):
        r = 0.915 + 0.02 * math.sin(t * 9)
        x, y = cx + cx * r * math.cos(t), cy + cy * r * math.sin(t)
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(70, 120, 70))
        col = [(240, 220, 170), (226, 160, 60), (246, 236, 214)][int(rng.integers(3))]
        d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=col)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=GOLD_L)
    ell(0.86, GOLD + (255,))
    ell(0.85, CARPET + (255,))
    for t in np.linspace(0, 2 * math.pi, 36, endpoint=False):
        x, y = cx + cx * 0.78 * math.cos(t), cy + cy * 0.78 * math.sin(t)
        d.polygon(star_pts(x, y, 13, 8, 0.765, math.pi / 8), fill=GOLD)
    R = 200                                           # the seal
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=GOLD, outline=INK, width=3)
    d.ellipse([cx - R + 18, cy - R + 18, cx + R - 18, cy + R - 18], fill=F_RED)
    for sgn in (-1, 1):                               # wheat ears up each side of the ring
        for k in range(9):
            t = math.pi / 2 + sgn * (0.35 + k * 0.27)
            x, y = cx + (R - 40) * math.cos(t), cy + (R - 40) * math.sin(t)
            d.ellipse([x - 8, y - 15, x + 8, y + 15], fill=GOLD_L, outline=GOLD_D)
    d.polygon(star_pts(cx, cy, 120, 8, 0.765, math.pi / 8), fill=GOLD, outline=INK)
    d.polygon(star_pts(cx, cy, 70, 5, 0.42, -math.pi / 2), fill=F_RED, outline=INK)
    return im.resize((W * 2, H * 2), Image.LANCZOS)


# ---------------------------------------------------------------------------------------------- posters
@functools.lru_cache(maxsize=2)
def portrait_art(seed):
    """An original poster-style painting (no words, no real face): a gold sun rising behind a domed hall with a slim
    tower, a factory with a chimney, a field of wheat in front, on a red sky cut by a black diagonal."""
    w, h = 300, 380
    im = Image.new('RGBA', (w, h), F_RED + (255,))
    d = ImageDraw.Draw(im)
    d.polygon([(0, 260), (w, 120), (w, 170), (0, 310)], fill=(30, 26, 28))           # the black diagonal
    sx, sy = (110, 230) if seed == 0 else (190, 230)
    for k in range(14):                                                              # sun rays
        t = math.pi + math.pi * k / 13
        d.polygon([(sx, sy), (sx + 300 * math.cos(t - 0.05), sy + 300 * math.sin(t - 0.05)),
                   (sx + 300 * math.cos(t + 0.05), sy + 300 * math.sin(t + 0.05))], fill=(214, 66, 52))
    d.ellipse([sx - 60, sy - 60, sx + 60, sy + 60], fill=GOLD)
    d.rectangle([40, 210, 140, 280], fill=(236, 230, 214))                          # the domed hall
    d.pieslice([50, 150, 130, 270], 180, 360, fill=GOLD_L)
    d.rectangle([150, 120, 162, 280], fill=(236, 230, 214))                          # its slim tower
    d.polygon([(148, 120), (164, 120), (156, 98)], fill=GOLD_L)
    d.polygon([(180, 280), (180, 220), (210, 240), (210, 220), (240, 240), (240, 220), (270, 240), (270, 280)],
              fill=(60, 56, 58))                                                     # the factory
    d.rectangle([250, 160, 264, 240], fill=(60, 56, 58))
    d.rectangle([0, 280, w, h], fill=GOLD)                                           # the wheat field
    for x in range(8, w, 18):
        d.line([(x, h), (x + 6, 292)], fill=GOLD_D, width=3)
        d.ellipse([x + 1, 282, x + 11, 302], fill=GOLD_L)
    return im


# ---------------------------------------------------------------------------------------------- the desk
_desk0 = MS.desk_parts


def desk_parts():
    """The Resolute desk as MidTerminal's, its oval carving covered by a gold eight-point star on a red ground."""
    parts = _desk0()
    x, z = MS.DESK
    at = MS._at(x, z, 180.0)

    def star(img, cm, p):
        cm.poly(p, [at(0.19 * math.cos(t), 0.35 + 0.21 * math.sin(t), 0.459) for t in np.linspace(0, 6.28, 18)],
                F_RED, INK, 1.6)
        cm.poly(p, [at(sx, sy, 0.46) for sx, sy in star_pts(0.0, 0.35, 0.15, 8, 0.765, math.pi / 8)], GOLD, INK, 1.4)
    parts.append([Face([at(0, 0.35, 0.47)] * 3, None, None, None, 0, None)])
    parts[-1][0].draw = star
    return parts


# ---------------------------------------------------------------------------------------------- samovar, lanterns
def credenza_parts():
    """The low table behind the desk: the family photos on its left, a brass samovar with two tea glasses on its
    right."""
    x, z = 0.0, 4.75
    parts = [MS.obox((x, 0.0, z), (2.0, 0.78, 0.42), 180, {'all': MS.WOOD, 'top': MS.WOOD_L})]
    for k, u in enumerate((-0.8, -0.5, -0.2)):
        hh = 0.22 + 0.06 * (k % 2)
        parts.append(MS.obox((x + u, 0.78, z), (0.18, hh, 0.03), 180, {'all': GOLD, 'front': (190, 196, 204)}))
    sx, y0 = x + 0.55, 0.78
    br = {'side': BRASS, 'top': lt(BRASS, 1.1)}
    parts += [cylinder((sx, y0, z), 0.11, 0.05, br, n=12),                       # foot
              cylinder((sx, y0 + 0.05, z), 0.05, 0.06, br, n=10),                # waist
              cylinder((sx, y0 + 0.11, z), 0.15, 0.3, br, n=14),                  # the urn
              cylinder((sx, y0 + 0.41, z), 0.09, 0.05, br, n=12),
              cylinder((sx, y0 + 0.46, z), 0.08, 0.14, {'side': (236, 234, 230), 'top': (240, 238, 232)}, n=10),   # teapot
              cylinder((sx, y0 + 0.60, z), 0.03, 0.04, br, n=8)]
    for u in (0.82, 0.9):                                                          # tea glasses
        parts.append(cylinder((x + u, y0, z - 0.08), 0.03, 0.09, {'side': TEA, 'top': lt(TEA, 1.2)}, n=8))

    def tap(img, cm, p):
        q = (sx, y0 + 0.2, z - 0.16)
        cm.poly(p, [q, (sx + 0.0, y0 + 0.22, z - 0.24), (sx, y0 + 0.18, z - 0.24), (sx, y0 + 0.16, z - 0.16)],
                BRASS_D, INK, 1.2)
        for sg in (-1, 1):                                                         # handles
            cm.line(p, [(sx + sg * 0.15, y0 + 0.36, z), (sx + sg * 0.21, y0 + 0.34, z), (sx + sg * 0.15, y0 + 0.24, z)],
                    INK, 3.0)
    parts.append([Face([(sx, y0 + 0.2, z - 0.2)] * 3, None, None, None, 0, None)])
    parts[-1][0].draw = tap
    return parts


LANTERNS = ((-1.3, 5.0), (1.3, 5.0))                 # between the windows, near the wall
L_TOP, L_BOT = 3.55, 2.95                            # the lantern's top and bottom (m); a chain to the ceiling


def lantern_parts(x, z):
    """A pierced brass lantern (a domed cap, a six-sided body with star piercings glowing warm, a drop finial)."""
    def draw(img, cm, p):
        cm.line(p, [(x, MS.CEIL_H, z), (x, L_TOP + 0.12, z)], (80, 64, 40), 2.0)
        cap = [(x + 0.17 * math.cos(t), L_TOP + 0.12 * math.sin(t), z) for t in np.linspace(0, math.pi, 10)]
        cm.poly(p, cap + [(x - 0.19, L_TOP - 0.02, z), (x + 0.19, L_TOP - 0.02, z)][::-1], BRASS, INK, 1.6)
        body = [(x - 0.16, L_TOP - 0.02, z), (x + 0.16, L_TOP - 0.02, z), (x + 0.19, (L_TOP + L_BOT) / 2, z),
                (x + 0.12, L_BOT + 0.06, z), (x - 0.12, L_BOT + 0.06, z), (x - 0.19, (L_TOP + L_BOT) / 2, z)]
        cm.poly(p, body, BRASS_D, INK, 1.8)
        for sx, sy, r in ((0.0, (L_TOP + L_BOT) / 2 + 0.02, 0.07), (-0.1, L_TOP - 0.13, 0.03), (0.1, L_TOP - 0.13, 0.03),
                          (-0.08, L_BOT + 0.15, 0.03), (0.08, L_BOT + 0.15, 0.03)):
            cm.poly(p, [(x + px, py, z - 0.001) for px, py in star_pts(sx, sy, r, 8, 0.765, math.pi / 8)],
                    (255, 214, 120), None)
        cm.poly(p, [(x - 0.12, L_BOT + 0.06, z), (x + 0.12, L_BOT + 0.06, z), (x, L_BOT - 0.06, z)], BRASS, INK, 1.4)
    part = [Face([(x, (L_TOP + L_BOT) / 2, z)] * 3, None, None, None, 0, None)]
    part[0].draw = draw
    return [part]


_items0 = MS.items


def items(people=None):
    out = _items0(people)
    for x, z in LANTERNS:
        out.append(((x, 3.2, z), lambda img, cm, x=x, z=z: MS.draw_parts(img, cm, lantern_parts(x, z), MS._pen(img))))
    return out


# ---------------------------------------------------------------------------------------------- install
def install():
    """Swap the room's pieces for ours (MS looks each up by name when it draws)."""
    MS.flag_parts = flag_parts
    MS.window = window
    MS.valance = valance
    MS.walls = walls
    MS.carpet_art = carpet_art
    MS.portrait_art = portrait_art
    MS.desk_parts = desk_parts
    MS.credenza_parts = credenza_parts
    MS.items = items
    MS.VISITOR_CHAIRS = ()                        # the two gold chairs facing the desk hid it in the flat front view


install()
render, put, put_seated, wp, to_cam = MS.render, MS.put, MS.put_seated, MS.wp, MS.to_cam


# ---------------------------------------------------------------------------------------------- test
TEST_CAMS = [('office (front on)', ((0.0, 1.45, -1.5), (0.0, 1.45, 4.4), 1350)),
             ('two-shot (front on)', ((0.55, 1.45, -0.2), (0.55, 1.45, 4.4), 1350)),
             ('door wall (square on)', None)]


def door_cam():
    """Square on to the east door (wall angle 112), from across the room, level."""
    dx, _, dz = MS.wp(112.0, 0.0)
    yaw = math.radians(MS.wall_yaw(112.0))
    nx, nz = -math.sin(yaw), -math.cos(yaw)
    if nx * -dx + nz * -dz < 0:                       # the normal pointing into the room
        nx, nz = -nx, -nz
    return ((dx + nx * 3.0, 1.3, dz + nz * 3.0), (dx, 1.3, dz), 1050)


def test(out):
    import islamocommunism_set as ISET
    ISET.B.SS = 1
    tiles = []
    for label, c in TEST_CAMS:
        pos, look, focal = c if c else door_cam()
        img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 255))
        render(img, MS.S.Cam(pos, look, focal=focal), [])
        tiles.append(img.convert('RGB'))
    sheet = Image.new('RGB', (3 * 360, 640))
    for i, t in enumerate(tiles):
        sheet.paste(t.resize((360, 640), Image.LANCZOS), (i * 360, 0))
    sheet.save(out, quality=88)


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        test(sys.argv[2])
