#!/usr/bin/env python3
"""Patriots 4: the winner's room, painted once all the way round (film-quality rule 39: 2D, no 3D build).

The camera turns on the spot over the coins (Sam's "swivel", 1 Nov): the room is one panorama strip, 360 degrees
round, each thing at its clock angle from Claudia (0 = 12 o'clock, the arch behind her; clockwise: the Patriot 60,
Romesh 210, Bash 270). The table top and the coin pile are a fixed foreground layer in the middle of the frame, so
while the room and the people slide past behind them it reads as the camera circling the pile.

World units: x = K pixels per degree of turn (so a thing at angle a is at x = K * a); y in pixels on the 1920-tall
frame at zoom 1, the eye line at HORIZON. A PanCam (heading, zoom, centre y) gives burnham's camera for any frame.

    python3 source/patriots4_room.py OUT.jpg     the panorama strip and four views of it (the set, for the sheet)

Refs (references/patriots-4): 01 (the coin pile, the table's cream ring and light rim), 03 (the arch and lattice
behind Claudia, the fire basket), 09 (lattice either side of the arch, the panelled doors beyond it), 10 (the lantern),
12 (from above: the arch at the end, fire baskets on stands either side, panelled walls, candles).
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
from ed import INK, curve, oval  # noqa: E402
from satire_style import rough   # noqa: E402

K = 20.0              # pixels per degree at zoom 1 (a 54 degree field of view across the 1080 frame)
HORIZON = 820         # the eye line
WALL_PX = 300         # pixels per metre on the walls (about 4 m away)
FLOOR_PX = 767        # pixels per metre where the people stand (about 1.5 m away)
FLOOR_Y = HORIZON + 1.5 * FLOOR_PX      # the floor line under the people
TABLE_EDGE = FLOOR_Y - 0.95 * FLOOR_PX  # the table top's far edge (0.95 m high), at the people's waists
ANGLES = {'claudia': 0.0, 'patriot': 60.0, 'romesh': 210.0, 'bash': 270.0}

WOOD = (96, 54, 32)
WOOD_L = (124, 74, 44)
WOOD_D = (62, 34, 20)
ARCH = (112, 44, 28)
ARCH_L = (140, 62, 38)
GLOW = (164, 66, 38)               # the red-lit panes behind the lattice
LATTICE = (44, 24, 14)
IRON = (40, 36, 36)
FLAME = (252, 170, 60)
FLAME_IN = (255, 228, 140)
CANDLE = (238, 226, 196)
TABLE = (140, 60, 40)
TABLE_D = (108, 44, 30)
TABLE_RIM = (196, 132, 92)
CREAM = (230, 210, 172)
GOLD = (232, 186, 74)
GOLD_S = (184, 132, 40)
GOLD_L = (252, 222, 130)


def wrap(a):
    return (a + 180.0) % 360.0 - 180.0


class PanCam:
    """The camera turning on the spot: `heading` (degrees, as the clock angles above), `zoom`, `cy` the world y at the
    frame's middle. .cam is burnham's camera; .x(angle) the world x of something at that angle, unwrapped so it sits
    nearest the camera (the strip joins up behind it)."""

    def __init__(self, heading, zoom=1.0, cy=960.0):
        self.heading, self.zoom, self.cy = heading % 360.0, zoom, cy
        self.cam = B.Cam(zoom, K * self.heading, cy)

    def x(self, angle):
        return K * (self.heading + wrap(angle - self.heading))

    def seen(self, angle, half_w=0.0):
        """Whether something at this angle (half_w world pixels wide each side) is in the frame."""
        return abs(wrap(angle - self.heading)) * K * self.zoom <= 540 + half_w * self.zoom

    def screen(self, angle, y):
        return self.cam.P(self.x(angle), y)


def wy(m):
    """World y of a height m metres above the floor, on the walls."""
    return HORIZON - (m - 1.5) * WALL_PX


# ------------------------------------------------------------------------------------------------ pieces
def lattice(p, x0, x1, y0, y1, step=34, glow=GLOW):
    """A diamond lattice grille over red-lit panes (refs 03, 09): the glow behind, the dark diagonal bars over it."""
    p.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], glow, INK, 2.2)
    h = y1 - y0
    for u in range(-int(h / step) - 1, int((x1 - x0) / step) + 2):
        xa = x0 + u * step
        a = (max(x0, xa), y0 + max(0, x0 - xa))
        b = (min(x1, xa + h), y0 + min(h, x1 - xa))
        if b[0] > a[0]:
            p.line([a, b], LATTICE, 5.0)
        xb = x1 - u * step
        a = (min(x1, xb), y0 + max(0, xb - x1))
        b = (max(x0, xb - h), y0 + min(h, xb - x0))
        if a[0] > b[0]:
            p.line([a, b], LATTICE, 5.0)


def panels(p, x0, x1, seed=0):
    """Tall dark wooden panels from the floor to the frieze (refs 09, 10, 12): a framed panel per 80 px, the frame
    lighter, the inner panel with a moulding; a lattice frieze along the top, a rail below it."""
    top, frieze, bot = wy(4.2), wy(3.5), wy(0.0)
    p.poly([(x0, top), (x1, top), (x1, bot), (x0, bot)], WOOD, None)
    lattice(p, x0, x1, top + 20, frieze, 30, (120, 50, 30))
    p.poly([(x0, frieze), (x1, frieze), (x1, frieze + 26), (x0, frieze + 26)], WOOD_L, INK, 2.2)
    i0 = int(math.floor(x0 / 80.0))
    for i in range(i0, int(math.ceil(x1 / 80.0)) + 1):
        x = i * 80.0
        if x + 80 < x0 or x > x1:
            continue
        a, b = max(x0, x + 6), min(x1, x + 74)
        if b - a < 10:
            continue
        p.poly(rough([(a, frieze + 40), (b, frieze + 40), (b, bot - 10), (a, bot - 10)], 2, seed + i), WOOD_L, INK, 2.0)
        if b - a > 30:
            p.poly(rough([(a + 12, frieze + 58), (b - 12, frieze + 58), (b - 12, bot - 28), (a + 12, bot - 28)], 2,
                         seed + i + 500), WOOD, WOOD_D, 1.6)
            p.line([(a + 12, wy(2.2)), (b - 12, wy(2.2))], WOOD_D, 1.6)       # the panel's middle rail
    p.line([(x0, top), (x1, top)], INK, 2.4)


def flame(p, x, y, w, h, t, seed=0):
    """A fire's flames: three or four lumpy tongues, flickering (shape changes every few frames, never a loop)."""
    k = int(t * 8)
    rng = np.random.default_rng(seed * 1000 + k)
    for i, (dx, sc) in enumerate(((-0.35, 0.7), (0.0, 1.0), (0.32, 0.8), (0.12, 0.55))):
        hh = h * sc * rng.uniform(0.8, 1.1)
        cx = x + dx * w
        tip = (cx + rng.uniform(-0.15, 0.15) * w, y - hh)
        body = [(cx - w * 0.3 * sc, y), (cx - w * 0.28 * sc, y - hh * 0.45), tip, (cx + w * 0.28 * sc, y - hh * 0.45),
                (cx + w * 0.3 * sc, y)]
        p.poly(curve(body, 3), FLAME, INK, 1.6)
        p.poly(curve([(cx - w * 0.14 * sc, y), (cx - w * 0.1 * sc, y - hh * 0.35), (cx, y - hh * 0.62),
                      (cx + w * 0.1 * sc, y - hh * 0.35), (cx + w * 0.14 * sc, y)], 3), FLAME_IN, None)


def fire_basket(p, x, t, seed=0):
    """A fire basket on an iron stand (ref 12): a tall pole and three feet, an open iron cage bowl, the flames."""
    top = wy(1.45)
    p.poly([(x - 6, top + 40), (x + 6, top + 40), (x + 6, wy(0.0)), (x - 6, wy(0.0))], IRON, INK, 1.8)
    flame(p, x, top + 8, 120, 120, t, seed)
    bowl = [(x - 70, top - 10), (x + 70, top - 10), (x + 50, top + 40), (x - 50, top + 40)]
    p.poly(bowl, None, INK, 4.0)
    for k in range(-3, 4):
        p.line([(x + k * 20, top - 10), (x + k * 14, top + 40)], IRON, 4.0)
    p.line([(x - 72, top - 10), (x + 72, top - 10)], IRON, 6.0)
    p.line([(x - 50, top + 40), (x + 50, top + 40)], IRON, 6.0)


def torch(p, x, t, seed=0):
    """A torch in an iron cage on a wall bracket (refs 10, 12)."""
    y = wy(2.3)
    p.line([(x, y + 70), (x, y + 140), (x - 30, y + 160)], IRON, 6.0)                # the bracket
    flame(p, x, y + 50, 64, 76, t, seed)
    for k in (-1, 0, 1):                                                              # the cage
        p.line([(x + k * 24, y - 6), (x + k * 18, y + 70)], IRON, 4.0)
    p.line([(x - 28, y - 6), (x + 28, y - 6)], IRON, 5.0)
    p.line([(x - 20, y + 70), (x + 20, y + 70)], IRON, 5.0)


def candles(p, x, t, n=5, seed=0):
    """Pillar candles of different heights on a ledge (ref 12)."""
    ledge = wy(1.0)
    p.poly([(x - 30 - 34 * n / 2, ledge), (x + 30 + 34 * n / 2, ledge), (x + 30 + 34 * n / 2, ledge + 22),
            (x - 30 - 34 * n / 2, ledge + 22)], WOOD_L, INK, 2.0)
    rng = np.random.default_rng(seed)
    for i in range(n):
        cx = x + (i - (n - 1) / 2) * 34
        h = rng.uniform(60, 130)
        p.poly(rough([(cx - 12, ledge), (cx + 12, ledge), (cx + 12, ledge - h), (cx - 12, ledge - h)], 1.5, seed + i),
               CANDLE, INK, 1.8)
        k = 0.85 + 0.15 * math.sin(t * 9 + i * 2.1 + seed)
        p.poly(curve([(cx - 5, ledge - h - 2), (cx, ledge - h - 22 * k), (cx + 5, ledge - h - 2)], 3), FLAME, INK, 1.2)


def arch(p, x, t):
    """The arch the banished leave by (refs 01, 03, 09, 12): a pointed wooden arch, lattice above and either side over
    red-lit panes, and the dark passage beyond with its panelled double doors."""
    half, spring, bot = 330.0, wy(2.0), wy(0.0)
    lattice(p, x - 600, x + 600, wy(4.2), bot)                    # the screen wall the arch is cut through
    for sg in (-1, 1):                                            # posts framing it
        p.poly(rough([(x + sg * 560, wy(4.2)), (x + sg * 600, wy(4.2)), (x + sg * 600, bot), (x + sg * 560, bot)], 2, 3),
               ARCH, INK, 2.2)
    c = half * 0.6                                                # a pointed (Gothic) arch: two arcs, each centred
    R = half + c                                                  # on the far side, meeting at the apex
    top = math.acos(c / R)
    opening = [(x - half, bot), (x - half, spring)] + \
        [(x + c - R * math.cos(a), spring - R * math.sin(a)) for a in np.linspace(0.05, top, 10)] + \
        [(x - c + R * math.cos(a), spring - R * math.sin(a)) for a in np.linspace(top, 0.05, 10)] + \
        [(x + half, spring), (x + half, bot)]
    outer = [(px + (px - x) * 0.17, py - (bot - py) * 0.05) for px, py in opening]
    p.poly(outer, ARCH_L, INK, 2.6)                               # the arch's moulded frame
    p.poly(opening, (36, 20, 14), INK, 2.4)                       # the passage beyond, dark
    dt, db = wy(2.6), bot                                         # the panelled double doors (ref 09)
    for sg in (-1, 1):
        a, b = x + sg * 14, x + sg * 230
        lo, hi = min(a, b), max(a, b)
        p.poly([(lo, dt), (hi, dt), (hi, db), (lo, db)], (90, 52, 30), INK, 2.0)
        for k in range(1, 6):                                     # linenfold ribs
            xx = lo + (hi - lo) * k / 6
            p.line([(xx, dt + 30), (xx, db - 20)], (64, 36, 22), 2.0)
        p.line([(lo + 10, wy(1.3)), (hi - 10, wy(1.3))], (64, 36, 22), 3.0)
    lattice(p, x - 230, x + 230, wy(3.1), dt - 10, 28)            # the grille in the arch's head
    p.poly(opening, None, INK, 2.6)


def round_table_room(p, img, x, t):
    """The opening to the Round Table hall behind Romesh: its panelled walls with lamps and the Round Table itself,
    far off and small (reused: traitors.wall, traitors.round_table)."""
    import traitors as TR
    half, top, bot = 560.0, wy(3.4), wy(0.0)
    hall_floor = HORIZON + 1.5 * 70
    p.poly([(x - half, top), (x + half, top), (x + half, bot), (x - half, bot)], (70, 48, 34), None)
    sub = B.Cam(p.cam.z, p.cam.cx, p.cam.cy)
    TR.wall(img, sub, x - half, x + half, HORIZON - 1.6 * 110, hall_floor, seed=7, panel_w=110,
            lamps=[(x - 300, HORIZON - 70), (x + 300, HORIZON - 70)])
    p.poly([(x - half, hall_floor), (x + half, hall_floor), (x + half, bot), (x - half, bot)], (78, 56, 40), INK, 2.0)
    TR.round_table(img, sub, x + 20, hall_floor + 40, 300, 46, [a for a in np.linspace(0, 2 * math.pi, 12, endpoint=False)],
                   thick=14)
    for sg in (-1, 1):                                            # the opening's posts and lintel
        p.poly(rough([(x + sg * half - 30, top), (x + sg * half + 30, top), (x + sg * half + 30, bot),
                      (x + sg * half - 30, bot)], 2, 11), ARCH, INK, 2.4)
    p.poly(rough([(x - half - 30, top - 40), (x + half + 30, top - 40), (x + half + 30, top + 6), (x - half - 30, top + 6)], 2, 12),
           ARCH, INK, 2.4)


# What stands where round the room (angle in degrees; the people's angles in ANGLES).
OPEN = [(-30.0, 30.0, 'arch'), (178.0, 236.0, 'round table')]
DRESS = [('basket', -24.0, 1), ('basket', 24.0, 2), ('torch', 92.0, 3), ('candles', 130.0, 4), ('torch', 160.0, 5),
         ('candles', 252.0, 6), ('torch', 292.0, 7), ('candles', 318.0, 8), ('candles', 76.0, 9)]


def room(img, pc, t):
    """The panorama as this camera sees it."""
    p = B.Pen(img, pc.cam)
    span = (540 / pc.zoom + 400) / K                               # degrees either side worth drawing
    a0, a1 = pc.heading - span, pc.heading + span
    p.poly([(K * a0 - 200, -600), (K * a1 + 200, -600), (K * a1 + 200, 2600), (K * a0 - 200, 2600)], (30, 18, 12), None)
    # the walls between the openings
    cuts = sorted((pc.x((a + b) / 2) - K * (b - a) / 2, pc.x((a + b) / 2) + K * (b - a) / 2) for a, b, _ in OPEN)
    x = K * a0
    for c0, c1 in cuts + [(K * a1, K * a1)]:
        if c0 > x:
            panels(p, x, min(c0, K * a1), seed=int(x) // 80)
        x = max(x, c1)
    for a, b, kind in OPEN:
        mid = (a + b) / 2
        if pc.seen(mid, K * (b - a) / 2 + 300):
            if kind == 'arch':
                arch(p, pc.x(mid), t)
            else:
                round_table_room(p, img, pc.x(mid), t)
    for kind, a, seed in DRESS:
        if pc.seen(a, 200):
            {'basket': fire_basket, 'torch': torch, 'candles': candles}[kind](p, pc.x(a), t, seed=seed)
    p.poly([(K * a0 - 200, -600), (K * a1 + 200, -600), (K * a1 + 200, wy(4.2)), (K * a0 - 200, wy(4.2))], (36, 22, 14), None)
    for k in range(int(a0 // 12) - 1, int(a1 // 12) + 2):           # ceiling beams
        bx = K * k * 12
        p.poly([(bx - 26, -600), (bx + 26, -600), (bx + 26, wy(4.2)), (bx - 26, wy(4.2))], WOOD_D, INK, 1.8)


# ------------------------------------------------------------------------------------------------ the foreground
TABLE_RX, TABLE_RY = 1180.0, 470.0


def table_top(img, pc):
    """The round winner's table top (ref 01): red-brown, a light rim, a cream inlaid ring. Fixed in the frame's middle
    (the camera turns over its centre); its far edge at the people's waists."""
    p = B.Pen(img, pc.cam)
    cx, cy = K * pc.heading, TABLE_EDGE + TABLE_RY
    E = lambda r, n=120: [(cx + TABLE_RX * r * math.cos(a), cy + TABLE_RY * r * math.sin(a))
                          for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    p.poly(E(1.0), TABLE_RIM, INK, 2.6)
    p.poly(E(0.965), TABLE, INK, 2.0)
    p.poly(E(0.8), CREAM, INK, 1.6)
    p.poly(E(0.76), TABLE, INK, 1.6)
    p.poly(E(0.5), TABLE_D, None)
    return cx, cy


COIN_RX, COIN_RY, COIN_T = 54.0, 19.0, 24.0


def coin(p, x, y, k=1.0):
    """One big gold coin seen from a little above: its rim band and its face (ref 01)."""
    rx, ry, th = COIN_RX * k, COIN_RY * k, COIN_T * k
    p.poly([(x - rx, y)] + [(x + rx * math.cos(a), y + ry * math.sin(a)) for a in np.linspace(math.pi, 0, 16)] +
           [(x + rx, y - th)] + [(x + rx * math.cos(a), y - th + ry * math.sin(a)) for a in np.linspace(0, math.pi, 16)],
           GOLD_S, INK, 1.6)
    p.poly(oval(x, y - th, rx, ry, 24), GOLD, INK, 1.6)
    p.poly(oval(x, y - th, rx * 0.7, ry * 0.7, 20), None, GOLD_S, 1.4)
    p.line([(x - rx * 0.4, y - th - ry * 0.3), (x - rx * 0.1, y - th - ry * 0.55)], GOLD_L, 2.0)


def coin_pile(img, pc):
    """The coin pile in about 7 tiers, more coins scattered round its base (ref 01): stacks on a grid, tallest in the
    middle, drawn back to front."""
    p = B.Pen(img, pc.cam)
    cx = K * pc.heading
    base = TABLE_EDGE + 300
    rng = np.random.default_rng(4)
    stacks = []
    for j in range(-3, 4):                                   # rows, back (-) to front (+)
        for i in range(-4, 5):
            r = math.hypot(i * 1.0, j * 1.2)
            n = int(round(7.6 - 1.75 * r + rng.uniform(-0.4, 0.4)))
            if n <= 0 and rng.random() < 0.55:
                continue
            stacks.append((j, i, max(1, n)))
    for j, i, n in sorted(stacks):
        x = cx + i * 96 + (j % 2) * 48 + rng.uniform(-8, 8)
        y = base + j * 36
        for k in range(n):
            coin(p, x + rng.uniform(-4, 4), y - k * COIN_T)
    for _ in range(9):                                       # a few scattered round the base
        a = rng.uniform(0.2, math.pi - 0.2)
        x, y = cx + 470 * math.cos(a) * rng.uniform(0.9, 1.1), base + 170 * math.sin(a) + 40
        coin(p, x, y)


def foreground(img, pc):
    table_top(img, pc)
    coin_pile(img, pc)


# ------------------------------------------------------------------------------------------------ the set sheet
def sheet(out):
    B.SS = 1
    font = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 26)
    views = [(0, 'Claudia (12): the arch'), (60, 'the Patriot (2)'), (210, 'Romesh (7): the Round Table hall'),
             (270, 'Bash (9)')]
    tiles = []
    for h, label in views:
        im = B.canvas((0, 0, 0))
        pc = PanCam(h)
        room(im, pc, 0.0)
        foreground(im, pc)
        im = im.convert('RGB').resize((540, 960))
        ImageDraw.Draw(im).text((12, 12), label, font=font, fill=(255, 255, 255))
        tiles.append(im)
    W = Image.new('RGB', (540 * 4 + 50, 980), (20, 20, 20))
    for i, t in enumerate(tiles):
        W.paste(t, (10 + i * 550, 10))
    W.save(out, quality=86)
    return out


if __name__ == '__main__':
    print(sheet(sys.argv[1]))
