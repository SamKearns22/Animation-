"""The Season Pass weapons, stitched into Sam's reference scenes.

For each scene: the original weapon is erased completely (every pixel of it given back to the linen, tunic or
horse it crossed), then the new weapon is drawn in the same hand, at the same place, as wool areas with their
own thread directions, and stitched with exactly the same stitches as the rest of the tapestry.
Coordinates are in the reference photograph's pixels; the trace is S times bigger.

    python3 bayeux_weapons.py check OUT_DIR    before / after / erase-mask sheets for every scene
    python3 bayeux_weapons.py build            stitch every scene (before and after) into the cache
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

import bayeux_stitch as BS

S = 2.5                      # trace scale (pixels per reference pixel)
CACHE = os.path.join(BS.HERE, 'data', 'bayeux')
NONE = 255


class Layer:
    """A drawing of wool areas: an index image (NONE = nothing) and the thread angle of each area."""

    def __init__(self, w, h):
        self.lab = Image.new('L', (w, h), NONE)
        self.ang = Image.new('F', (w, h), float('nan'))
        self.dl, self.da = ImageDraw.Draw(self.lab), ImageDraw.Draw(self.ang)

    def poly(self, pts, wool, ang, outline=None, ow=1.4):
        pts = wobble(list(pts) + [pts[0]])[:-1]          # hand-sewn: never a ruler-straight edge
        p = [(x * S, y * S) for x, y in pts]
        self.dl.polygon(p, fill=BS.IDX[wool])
        self.da.polygon(p, fill=float(ang))
        if outline:
            self.line(list(pts) + [pts[0]], outline, ow, ang, raw=True)

    def line(self, pts, wool, w, ang=None, raw=False):
        if not raw:
            pts = wobble(list(pts))
        p = [(x * S, y * S) for x, y in pts]
        for i, ((x0, y0), (x1, y1)) in enumerate(zip(p, p[1:])):
            a = math.atan2(y1 - y0, x1 - x0) if ang is None else ang
            ww = w * (0.85 + 0.3 * _n1(x0 * 0.07 + y0 * 0.05))   # the thread thickens and thins a little
            self.dl.line([(x0, y0), (x1, y1)], fill=BS.IDX[wool], width=max(1, int(round(ww * S))))
            self.da.line([(x0, y0), (x1, y1)], fill=float(a), width=max(1, int(round(ww * S))))
            r = ww * S / 2
            for (x, y) in ((x0, y0), (x1, y1)):
                self.dl.ellipse([x - r, y - r, x + r, y + r], fill=BS.IDX[wool])
                self.da.ellipse([x - r, y - r, x + r, y + r], fill=float(a))

    def ellipse(self, cx, cy, rx, ry, wool, ang=0.0, outline=None, ow=1.4):
        n = 40
        pts = [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
        self.poly(pts, wool, ang, outline, ow)

    def arrays(self):
        return np.asarray(self.lab, np.int16), np.asarray(self.ang, np.float32)


def _n1(u):
    """Smooth, repeatable wobble (-1..1) from a position: the same shape always wobbles the same way."""
    return (math.sin(u * 1.7 + 0.3) * 0.5 + math.sin(u * 3.1 + 1.9) * 0.3 + math.sin(u * 5.3 + 4.1) * 0.2)


def wobble(pts, amp=0.55, step=2.5):
    """A path made hand-sewn: split into short pieces and nudged gently sideways, so edges are never ruler-straight
    and curves are never perfect, like the rest of the tapestry (amp and step in reference pixels)."""
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L / step))
        nx, ny = (-(y1 - y0) / L, (x1 - x0) / L) if L > 1e-6 else (0.0, 0.0)
        for i in range(n):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            d = amp * _n1(x * 0.21 + y * 0.17)
            out.append((x + nx * d, y + ny * d))
    out.append(pts[-1])
    return out


def local(origin, ang, k=1.0):
    """A drawing frame along a weapon: u along it, v across it (positive v = below), scaled by k."""
    ox, oy = origin
    c, s = math.cos(ang) * k, math.sin(ang) * k

    def f(pts):
        return [(ox + u * c - v * s, oy + u * s + v * c) for u, v in pts]
    return f


def rect(u0, u1, v0, v1):
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


# --------------------------------------------------------------------------------------------- the scenes
# erase: (polyline, width) in reference pixels; keep: polygons never erased (the hands); over: polygons whose
# original wool is drawn back on top of the new weapon (fingers wrapped round it).

def rifle_weapon(L):
    """Plasma Longshot Rifle: chunky, sage-grey body, black barrel, glowing green wool."""
    rear, front = (336, 141), (481, 97)
    ang = math.atan2(front[1] - rear[1], front[0] - rear[0])
    d = (math.cos(ang), math.sin(ang))
    f = local((rear[0] - 46 * d[0], rear[1] - 46 * d[1]), ang)
    a = ang
    L.poly(f([(0, -13), (6, -15), (78, -9), (78, 9), (30, 12), (4, 18), (0, 16)]), 'sage', a, 'black')   # stock
    L.poly(f(rect(14, 40, -6, 4)), 'navy', a)                                                              # cheek rest
    L.poly(f([(40, 6), (54, 6), (58, 30), (46, 32)]), 'black', a + 1.2, 'black')                          # grip
    L.poly(f([(72, -15), (176, -13), (180, -6), (180, 11), (150, 13), (128, 13), (72, 11)]), 'sage', a, 'black')  # receiver
    L.poly(f(rect(112, 132, 12, 34)), 'black', a + math.pi / 2, 'black')                                   # energy cell
    L.poly(f(rect(115, 129, 16, 31)), 'plasma', a + math.pi / 2)
    L.poly(f(rect(98, 168, -31, -18)), 'black', a, 'black')                                                # scope
    L.poly(f(rect(164, 170, -33, -16)), 'plasmapale', a + math.pi / 2)                                     # lens
    L.poly(f(rect(112, 118, -18, -14)), 'black', a)
    L.poly(f(rect(150, 156, -18, -14)), 'black', a)
    L.poly(f(rect(176, 236, -9, 9)), 'sage', a, 'black')                                                   # shroud
    L.poly(f(rect(232, 290, -4, 4)), 'black', a, 'black')                                                  # barrel
    L.poly(f(rect(284, 298, -8, 8)), 'black', a + math.pi / 2, 'black')                                    # muzzle
    L.poly(f(rect(80, 172, -3, 2)), 'plasma', a)                                                           # glow line
    for u in (186, 202, 218):                                                                              # vents
        L.poly(f(rect(u, u + 8, -5, 4)), 'plasma', a + math.pi / 2)


def claw_weapon(L):
    """Ice Claw: a mechanised gauntlet the size of half the rider, three fingers of bladed ice, frost."""
    claw_at(L, (304, 111), math.atan2(24, -45), 0.82)    # out to the left and down, over the next horse's neck


def claw_at(L, hand, ang, K, frost=16):
    f = local(hand, ang, K)
    a = ang
    L.poly(f([(-22, -15), (8, -18), (18, -12), (18, 12), (8, 18), (-22, 15)]), 'navy', a, 'black')        # cuff
    L.poly(f([(-18, -9), (12, -11), (12, -6), (-18, -4)]), 'ice', a)                                       # frost light
    L.poly(f([(10, -22), (34, -24), (42, -10), (42, 12), (34, 24), (10, 22)]), 'black', a, 'black')        # palm housing
    L.ellipse(*f([(26, 0)])[0], 6 * K / 0.82, 6 * K / 0.82, 'ice', a, 'navy')                              # core
    # three ice fingers, each in two jointed pieces, curving like talons
    for sp in (-0.55, 0.0, 0.55):
        base = (40, sp * 30)
        g = local(f([base])[0], a + sp * 0.9, K)
        L.poly(g(rect(0, 18, -5, 5)), 'black', a + sp * 0.9, 'black')
        tip = [(16, -6), (30, -6), (58, 2 + 6 * sp), (34, 7), (16, 6)]
        L.poly(g(tip), 'ice', a + sp * 0.9, 'navy')
        L.poly(g([(20, -3), (40, -2), (50, 2 + 6 * sp), (38, 1)]), 'frost', a + sp * 0.9)
    # stitched frost around it: short pale lines and stars
    cx, cy = f([(50, 0)])[0]
    rng = np.random.default_rng(3)
    for i in range(frost):
        r = (48 + rng.uniform(0, 26)) * K
        t = rng.uniform(0, 2 * math.pi)
        x, y = cx + r * math.cos(t), cy + r * 0.8 * math.sin(t)
        k = 2.5 + rng.uniform(0, 2)
        for j in range(3):                         # a small stitched frost star
            q = j * math.pi / 3 + t
            L.line([(x - k * math.cos(q), y - k * math.sin(q)), (x + k * math.cos(q), y + k * math.sin(q))],
                   'frost' if j else 'ice', 1.1)


def ghost_weapon(L, grow=1.0, text=True):
    """Ghost Pistol: a small black pistol; a long, silly ghost streaming out of it; WOOOOOO!! stitched above."""
    hand = (222, 56)
    a = math.radians(-12)
    f = local(hand, a)
    L.poly(f([(-6, -9), (30, -9), (32, -4), (30, -2), (4, -2), (2, 2)]), 'pistol', a, 'black')             # slide
    L.poly(f([(-6, -3), (6, -3), (10, 16), (0, 18), (-8, 2)]), 'pistol', a + 1.3, 'black')                 # grip
    L.poly(f(rect(30, 34, -8, -4)), 'black', a)
    if grow <= 0:
        return
    # the ghost: a long sheet from the muzzle, wavy edges, a round head at the far end
    mx, my = f([(35, -6)])[0]
    length = 215 * grow
    top, bot = [], []
    n = 40
    for i in range(n + 1):
        t = i / n
        x = mx + 6 + t * length
        w = 3 + 22 * t ** 1.3
        y = my + 30 * t + 9 * math.sin(t * 7.5) * t
        top.append((x, y - w))
        bot.append((x, y + w + 5 * math.sin(i * 1.9) * t))
    # the head: a round dome at the far end, facing on to the right
    hx, hy = top[-1][0], (top[-1][1] + bot[-1][1]) / 2
    R = 30 * grow
    dome = [(hx + R * 0.2 + R * math.cos(t), hy - R * 0.1 + R * math.sin(t))
            for t in np.linspace(-math.pi * 0.62, math.pi * 0.62, 18)]
    pts = top + dome + bot[::-1]
    L.poly(pts, 'ghost', 0.0, 'navy', 1.6)
    head_x, head_y = hx, hy
    if grow > 0.6:
        g = (grow - 0.6) / 0.4
        L.ellipse(head_x + 10, head_y - 9, 4 * g + 1, 6 * g + 1, 'black')
        L.ellipse(head_x + 26, head_y - 10, 4 * g + 1, 6 * g + 1, 'black')
        L.ellipse(head_x + 19, head_y + 9, 5 * g + 1, 8 * g + 1, 'black')
        for u in (0.25, 0.5, 0.75):        # its wavy tail lines
            i = int(u * n)
            L.line([top[i], ((top[i][0] + bot[i][0]) / 2 + 6, (top[i][1] + bot[i][1]) / 2)], 'buff', 1.1)


def ghost_caption(L, letters=9):
    """WOOOOOO!! stitched in capitals like the Latin captions above the scene."""
    word = 'WOOOOOO!!'[:letters]
    x, y, h = 340, 10, 22
    for ch in word:
        if ch == 'W':
            L.line([(x, y), (x + 5, y + h), (x + 9, y + 8), (x + 13, y + h), (x + 18, y)], 'navy', 2.2)
            x += 24
        elif ch == 'O':
            n = 24
            pts = [(x + 7 + 7 * math.cos(2 * math.pi * i / n), y + h / 2 + h / 2 * math.sin(2 * math.pi * i / n))
                   for i in range(n + 1)]
            L.line(pts, 'navy', 2.2)
            x += 19
        elif ch == '!':
            L.line([(x + 3, y), (x + 3, y + h - 7)], 'navy', 2.4)
            L.ellipse(x + 3, y + h - 1, 1.6, 1.6, 'navy')
            x += 9


def stapler_weapon(L):
    """Stapler: literally a stapler, embroidered with the same care as everything else."""
    a = math.radians(-4)
    f = local((252, 161), a)
    L.poly(f([(0, 0), (62, 0), (64, 5), (60, 8), (2, 8), (-2, 5)]), 'black', a, 'black')                   # base
    L.poly(f([(2, -2), (58, -6), (62, -2), (58, 1), (4, 1)]), 'buff', a)                                   # metal
    L.poly(f([(-4, -6), (4, -15), (56, -13), (64, -9), (62, -3), (4, -2), (-4, -2)]), 'terracotta', a, 'madder')  # top
    L.poly(f(rect(8, 52, -12, -10)), 'ochre', a)                                                           # shine
    L.ellipse(*f([(3, -3)])[0], 4, 4, 'black', a)                                                          # hinge


SCENES = {
    'rifle': dict(
        erase=[([(436, -4), (446, 25), (462, 55), (480, 80), (490, 94)], 15, ('madder', 'terracotta', 'ochre', 'black', 'buff')),
               ([(490, 94), (497, 120), (497, 165), (487, 200), (474, 234), (468, 252)], 17, ('madder', 'terracotta', 'ochre', 'black', 'buff')),
               ([(431, 31), (404, 92)], 6, ('madder', 'terracotta', 'ochre', 'black', 'buff')),
               ([(526, 60), (470, 91), (400, 123), (332, 141), (294, 149)], 8, ('ochre', 'buff', 'madder'))],
        keep=[[(470, 86), (490, 84), (494, 106), (472, 110)], [(326, 130), (348, 128), (350, 150), (328, 152)]],
        over=[[(472, 86), (490, 86), (492, 104), (474, 108)], [(328, 132), (346, 130), (348, 148), (330, 150)]],
        draw=rifle_weapon),
    'claw': dict(
        erase=[([(160, 92), (230, 97), (296, 104)], 4.5)],
        keep=[[(298, 100), (312, 100), (312, 114), (298, 114)]],
        over=[],
        draw=claw_weapon),
    'ghost': dict(
        erase=[([(396, 5), (300, 33), (232, 52)], 8, ('madder', 'black', 'navy')),
               ([(212, 58), (150, 72), (86, 93)], 8, ('linen', 'madder', 'black', 'navy', 'terracotta'))],
        keep=[[(212, 42), (232, 42), (234, 70), (212, 70)]],
        over=[[(214, 46), (230, 46), (232, 66), (214, 66)]],
        draw=ghost_weapon),
    'stapler': dict(
        erase=[([(268, 116), (268, 352)], 22),
               ([(258, 122), (298, 100), (316, 110), (316, 158), (280, 152), (258, 140)], 'poly')],
        keep=[[(254, 146), (288, 146), (288, 167), (254, 167)]],
        over=[[(254, 147), (286, 147), (286, 166), (254, 166)]],
        draw=stapler_weapon),
}


def stroke_masks(name, shape):
    """One mask per erase stroke, each with the wools it must not borrow from (the weapon's own)."""
    sc = SCENES[name]
    out = []
    for item in sc['erase']:
        pts, w = item[0], item[1]
        excl = item[2] if len(item) > 2 else ()
        er = Image.new('L', (shape[1], shape[0]), 0)
        d = ImageDraw.Draw(er)
        p = [(x * S, y * S) for x, y in pts]
        if w == 'poly':
            d.polygon(p, fill=255)
        else:
            d.line(p, fill=255, width=int(w * S))
            for x, y in p:
                r = w * S / 2
                d.ellipse([x - r, y - r, x + r, y + r], fill=255)
        for poly in sc['keep']:
            d.polygon([(x * S, y * S) for x, y in poly], fill=0)
        out.append((np.asarray(er) > 0, excl))
    return out


# ------------------------------------------------------------------------------------------- the new skins
# Each figure keeps his face, hands and whatever he holds ('show': copied back on top, linen and all); only his
# clothing is replaced. Coordinates are in the (pre-scaled) reference's pixels.

def oval(cx, cy, rx, ry, n=28):
    return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def ring_line(L, cx, cy, rx, ry, wool, w):
    pts = oval(cx, cy, rx, ry, 40)
    L.line(pts + [pts[0]], wool, w)


def boa(L, pts, seed=5):
    """A feather boa: a loose chain of fluffy tufts of different sizes, each with a few feathery wisps."""
    rng = np.random.default_rng(seed)
    path = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / 5))
        path += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n)]
    for i, (x, y) in enumerate(path):
        r = rng.uniform(5.5, 9.5)
        x += rng.uniform(-2.5, 2.5)
        y += rng.uniform(-2.5, 2.5)
        wool = 'boa' if rng.random() < 0.7 else 'lilac'
        L.ellipse(x, y, r, r * rng.uniform(0.7, 1.0), wool, rng.uniform(0, 3), 'lilac' if wool == 'boa' else 'purple', 0.8)
        for _ in range(2):                                                                 # feathery wisps
            q = rng.uniform(0, 2 * math.pi)
            L.line([(x + r * 0.6 * math.cos(q), y + r * 0.6 * math.sin(q)),
                    (x + r * 1.35 * math.cos(q + 0.3), y + r * 1.35 * math.sin(q + 0.3))], 'boa', 0.9)


def william_skin(L):
    """PARTY SUIT: purple suit, wide flared cuffs, feather boa, rhinestone boots, big purple cowboy hat."""
    v = math.pi / 2
    # the trouser leg, down the horse's side: tapering, a little bend at the knee, a crease down it
    L.poly([(244, 196), (302, 192), (304, 232), (303, 268), (300, 330), (272, 332), (262, 280), (254, 236)],
           'purple', v, 'black')
    L.line([(280, 200), (283, 240), (282, 274), (287, 326)], 'lilac', 1.3)
    # the cowboy boot: a shaft, a heel and a pointed toe, covered in rhinestones
    L.poly([(268, 322), (302, 320), (304, 340), (324, 348), (330, 356), (300, 360), (276, 360), (268, 346)],
           'frost', 0.0, 'navy', 1.2)
    L.poly([(268, 352), (280, 352), (280, 364), (268, 364)], 'navy', v)
    rng = np.random.default_rng(5)
    for _ in range(16):
        L.ellipse(272 + rng.uniform(0, 48), 326 + rng.uniform(0, 30), 1.5, 1.5,
                  rng.choice(['ice', 'lilac', 'plasmapale', 'boa']))
    # the jacket: padded shoulders, nipped at the waist, its tails flaring over the saddle
    L.poly([(222, 96), (236, 86), (296, 84), (310, 94), (306, 128), (302, 166), (318, 206), (296, 212), (262, 214),
            (228, 208), (240, 168), (226, 130)], 'purple', v, 'black')
    L.line([(252, 88), (262, 130), (266, 168)], 'lilac', 1.6)                                   # lapels
    L.line([(282, 88), (272, 130), (266, 168)], 'lilac', 1.6)
    L.line([(242, 172), (300, 170)], 'lilac', 1.2)                                             # waist seam
    for y in (138, 152):
        L.ellipse(268, y, 2.2, 2.2, 'ochre')                                                    # buttons
    L.poly([(286, 86), (322, 88), (322, 114), (292, 120)], 'purple', 0.1, 'black')               # pointing sleeve
    L.poly([(318, 82), (342, 72), (346, 120), (318, 116)], 'lilac', v, 'purple')                 # wide cuff
    L.poly([(238, 94), (262, 92), (288, 116), (272, 132), (248, 120)], 'purple', 0.8, 'black')   # club arm
    L.poly([(260, 108), (278, 104), (282, 126), (266, 128)], 'lilac', 0.8, 'purple')             # its cuff
    boa(L, [(220, 92), (240, 96), (262, 98), (284, 94), (298, 88)], seed=5)                    # round his neck...
    boa(L, [(214, 96), (206, 120), (204, 146), (210, 172), (206, 196)], seed=6)                # ...and trailing behind
    # the hat: big purple cowboy hat with a band
    L.poly([(212, 48), (230, 40), (290, 40), (308, 46), (300, 54), (260, 50), (220, 54)], 'purple', 0.0, 'black')
    L.poly([(238, 42), (240, 18), (252, 12), (258, 18), (266, 12), (278, 18), (280, 42)], 'purple', v, 'black')
    L.poly([(239, 34), (279, 34), (280, 41), (238, 41)], 'lilac', 0.0)
    # his club, redrawn in front of the suit as it was in front of his mail
    a = math.atan2(140 - 50, 336 - 188)
    f = local((188, 50), a)
    L.poly(f([(0, -7), (60, -5), (172, -3), (172, 3), (60, 5), (0, 7)]), 'ochre', a, 'madder', 1.2)


def harold_skin(L):
    """SHARK WARRIOR: a huge hammerhead-shark Halloween costume, only his face showing."""
    v = math.pi / 2
    body = [(176, 108), (215, 98), (270, 98), (304, 112), (318, 160), (320, 230), (316, 310), (298, 380), (262, 422),
            (190, 430), (152, 410), (156, 340), (176, 270), (168, 200), (164, 150)]
    L.poly(body, 'shark', v, 'navy', 1.8)
    L.poly([(168, 150), (196, 138), (206, 300), (184, 384), (162, 398), (170, 300)], 'buff', v, 'shark')    # belly
    for y in range(160, 380, 22):                                                                   # belly ridges
        L.line([(170, y), (200, y + 4)], 'shark', 1.0)
    L.ellipse(170, 422, 26, 12, 'shark', 0.0, 'navy', 1.6)                                      # costume feet
    L.ellipse(208, 426, 24, 11, 'shark', 0.0, 'navy', 1.6)
    L.poly([(298, 110), (344, 72), (336, 134)], 'shark', 0.6, 'navy', 1.6)                         # dorsal fin
    L.poly([(292, 372), (334, 396), (352, 432), (318, 428), (284, 404)], 'shark', 0.8, 'navy', 1.6)  # tail
    L.ellipse(250, 82, 44, 40, 'shark', v, 'navy', 1.6)                                          # hood
    L.poly([(186, 38), (250, 40), (318, 28), (318, 54), (250, 60), (186, 60)], 'shark', 0.0, 'navy', 1.8)  # hammer
    L.ellipse(186, 49, 12, 11, 'shark', 0.0, 'navy', 1.6)
    L.ellipse(320, 41, 12, 13, 'shark', 0.0, 'navy', 1.6)
    for ex, ey in ((186, 48), (322, 38)):
        L.ellipse(ex, ey, 6, 6, 'black')
        L.ellipse(ex + 1.5, ey - 1.5, 1.8, 1.8, 'frost')
    ring_line(L, 249, 80, 20, 23, 'navy', 1.6)                                                  # the round mouth...
    for i in range(14):                                                                           # ...ringed with teeth
        q = 2 * math.pi * i / 14
        bx, by = 249 + 21 * math.cos(q), 80 + 24 * math.sin(q)
        tx, ty = 249 + 15 * math.cos(q), 80 + 17 * math.sin(q)
        nx, ny = -math.sin(q) * 3, math.cos(q) * 3
        L.poly([(bx - nx, by - ny), (bx + nx, by + ny), (tx, ty)], 'frost', 0.0)
    # his kite shield, stitched clean on top of the costume: pale with spots, an ochre rim and a boss
    shield = [(266, 160), (300, 166), (314, 200), (312, 250), (298, 310), (272, 366), (252, 366), (232, 310),
              (218, 250), (220, 196), (236, 168)]
    L.poly(shield, 'mail', v, 'ochre', 2.6)
    L.line([(266, 166), (266, 356)], 'bluegreen', 1.6)
    L.line([(226, 236), (306, 236)], 'bluegreen', 1.6)
    L.ellipse(266, 236, 9, 9, 'ochre', 0.0, 'madder', 1.2)
    rng = np.random.default_rng(8)
    for _ in range(14):
        L.ellipse(rng.uniform(232, 300), rng.uniform(180, 330), 2.2, 2.2, rng.choice(['madder', 'bluegreen']))
    # the arrow he clutches, redrawn over the costume
    L.line([(172, 80), (354, 18)], 'madder', 1.6)
    L.poly([(354, 18), (346, 14), (348, 24)], 'black', 0.0)


def edward_skin(L):
    """ELECTRIC MOUSE: a yellow hooded onesie, long dark-tipped ears, red cheek patches, a lightning-bolt tail."""
    v = math.pi / 2
    L.poly([(495, 300), (520, 268), (508, 262), (540, 224), (528, 218), (566, 178), (578, 186), (550, 228),
            (562, 236), (530, 276), (542, 284), (508, 314)], 'yellow', 0.9, 'madder', 1.6)        # tail
    L.poly([(496, 300), (510, 284), (522, 292), (508, 314)], 'ochre', 0.9)                        # its root
    # the onesie, seated: shoulders, a round tummy, his lap out to the knees, shins down to big paw feet
    L.poly([(350, 192), (372, 182), (404, 180), (442, 184), (470, 200), (478, 236), (490, 266), (488, 300),
            (470, 314), (444, 318), (438, 334), (360, 336), (350, 300), (338, 262), (336, 226)], 'yellow', v,
           'madder', 1.6)
    L.line([(448, 252), (480, 262)], 'ochre', 1.4)                                              # the fold at his knee
    L.line([(366, 300), (440, 304)], 'ochre', 1.2)
    for x in (378, 418):                                                                          # foot paws
        L.ellipse(x, 338, 16, 8, 'yellow', 0.0, 'madder', 1.2)
        for d in (-6, 0, 6):
            L.line([(x + d, 334), (x + d, 343)], 'madder', 0.8)
    L.poly([(352, 196), (338, 230), (346, 252), (356, 248), (350, 228), (366, 202)], 'yellow', 1.2, 'madder', 1.3)
    L.ellipse(352, 252, 8, 7, 'yellow', 0.0, 'madder', 1.1)                                       # resting paw
    L.poly([(420, 192), (430, 218), (402, 238), (394, 228), (414, 212)], 'yellow', 2.4, 'madder', 1.3)
    L.ellipse(394, 234, 8, 7, 'yellow', 0.0, 'madder', 1.1)                                       # sceptre paw
    L.ellipse(386, 156, 40, 46, 'yellow', v, 'madder', 1.6)                                       # hood
    ring_line(L, 386, 160, 24, 31, 'ochre', 2.2)                                                  # its round opening
    L.poly([(362, 122), (338, 46), (354, 50), (378, 118)], 'yellow', 1.9, 'madder', 1.4)          # ears
    L.poly([(338, 46), (343, 66), (352, 64), (354, 50)], 'black', 1.9)
    L.poly([(396, 118), (412, 44), (426, 48), (410, 124)], 'yellow', 1.4, 'madder', 1.4)
    L.poly([(412, 44), (426, 48), (422, 64), (410, 62)], 'black', 1.4)
    for cx in (352, 420):                                                                         # cheek patches
        L.ellipse(cx, 168, 6.5, 6.5, 'terracotta', 0.0, 'madder', 1.0)
    # his sceptre, redrawn in front of the costume
    L.line([(392, 236), (466, 150)], 'ochre', 3.2)
    for dx, dy in ((0, -8), (-7, -2), (7, -2)):
        L.ellipse(468 + dx, 146 + dy, 3.5, 3.5, 'buff', 0.0, 'madder', 1.0)


SKINS = {
    'william': dict(erase=[], keep=[], over=[], draw=william_skin,
                    show=[[(248, 50), (282, 50), (286, 86), (252, 90)],                   # face
                          [(340, 52), (374, 50), (374, 98), (344, 98)],                   # pointing hand
                          [(264, 114), (286, 114), (286, 132), (264, 132)]]),            # club hand
    'harold': dict(erase=[], keep=[], over=[], draw=harold_skin,
                   show=[oval(249, 80, 15, 18),                                            # face
                         [(162, 58), (206, 58), (206, 102), (166, 102)]]),                # raised hand
    'edward': dict(erase=[], keep=[], over=[], draw=edward_skin,
                   show=[oval(386, 160, 22, 29)]),                                        # his whole face and beard
}
SCENES.update(SKINS)


def masks(name, shape):
    sc = SCENES[name]
    er = np.zeros(shape, bool)
    for m, _ in stroke_masks(name, shape):
        er |= m
    ov = Image.new('L', (shape[1], shape[0]), 0)
    d = ImageDraw.Draw(ov)
    for poly in sc['over']:
        d.polygon([(x * S, y * S) for x, y in poly], fill=255)
    return er, np.asarray(ov) > 0


def clear(L, poly):
    """Unpick a patch of the tracing back to plain linen (broken fragments under a figure being re-stitched)."""
    p = [(x * S, y * S) for x, y in poly]
    L.dl.polygon(p, fill=BS.IDX['linen'])
    L.da.polygon(p, fill=float('nan'))


def sleeve(L, sh_a, sh_b, wr_a, wr_b, cuff, cuff_len=0.28):
    """A mail sleeve from the shoulder to the wrist, tapering, with a coloured cuff band at the wrist."""
    L.poly([sh_a, wr_a, wr_b, sh_b], 'mail', math.atan2(wr_a[1] - sh_a[1], wr_a[0] - sh_a[0]), 'madder', 1.2)
    ca = (wr_a[0] + (sh_a[0] - wr_a[0]) * cuff_len, wr_a[1] + (sh_a[1] - wr_a[1]) * cuff_len)
    cb = (wr_b[0] + (sh_b[0] - wr_b[0]) * cuff_len, wr_b[1] + (sh_b[1] - wr_b[1]) * cuff_len)
    L.poly([ca, wr_a, wr_b, cb], cuff, math.atan2(wr_a[1] - sh_a[1], wr_a[0] - sh_a[0]) + math.pi / 2, 'madder', 1.1)


def profile_head(L, cx, cy, r, facing=1, helmet='madder'):
    """A face in profile, the tapestry's way (a pale oval with a jutting nose and a dot eye), under a conical
    helmet with a nose guard."""
    f = facing
    L.poly([(cx - r * 0.9 * f, cy - r * 0.2), (cx - r * 0.6 * f, cy - r * 0.9), (cx + r * 0.5 * f, cy - r * 0.9),
            (cx + r * 0.85 * f, cy - r * 0.2), (cx + r * 1.2 * f, cy + r * 0.25), (cx + r * 0.85 * f, cy + r * 0.45),
            (cx + r * 0.7 * f, cy + r * 0.95), (cx - r * 0.3 * f, cy + r * 1.05), (cx - r * 0.9 * f, cy + r * 0.5)],
           'linen', math.pi / 2, 'madder', 1.1)
    L.ellipse(cx + r * 0.42 * f, cy + r * 0.02, r * 0.11, r * 0.11, 'black')
    L.line([(cx + r * 0.3 * f, cy + r * 0.72), (cx + r * 0.62 * f, cy + r * 0.68)], 'madder', 0.8)    # mouth
    L.poly([(cx - r * 1.05 * f, cy - r * 0.3), (cx + r * 1.0 * f, cy - r * 0.3), (cx + r * 0.1 * f, cy - r * 2.3)],
           helmet, math.pi / 2, 'black', 1.2)
    L.line([(cx + r * 0.62 * f, cy - r * 0.3), (cx + r * 0.7 * f, cy + r * 0.5)], 'black', r * 0.22)  # nose guard


def ghost_repair(L):
    """The pistol rider, re-stitched whole from the reference: leaning in the saddle, his mail coat flaring over the
    horse, one arm raised (the pistol), one reaching forward to the reins, his leg down the horse's side."""
    clear(L, [(250, 36), (335, 36), (398, 84), (398, 108), (346, 116), (352, 140), (300, 142), (288, 118),
              (252, 98)])
    clear(L, [(216, 52), (252, 52), (252, 96), (232, 92)])
    v = math.pi / 2
    L.poly([(334, 196), (350, 208), (356, 232), (372, 256), (388, 262), (384, 268), (364, 266), (346, 238),
            (334, 214)], 'navy', 1.0, 'black', 1.1)                                              # leg and foot
    L.line([(352, 250), (380, 250)], 'black', 1.0)                                             # stirrup strap
    L.poly([(288, 98), (304, 92), (322, 96), (334, 118), (340, 150), (350, 182), (358, 210), (340, 216),
            (318, 214), (306, 194), (300, 162), (294, 132)], 'mail', v, 'madder', 1.4)       # mail coat, flaring
    L.line([(304, 190), (330, 196), (356, 206)], 'madder', 1.0)                                # its hem fold
    sleeve(L, (292, 100), (298, 114), (238, 70), (244, 82), 'madder')                         # raised arm
    L.ellipse(229, 63, 6, 7, 'linen', 0.0, 'madder', 1.0)                                      # fist
    sleeve(L, (318, 98), (324, 110), (374, 90), (376, 102), 'madder')                          # rein arm
    L.ellipse(384, 96, 6, 5, 'linen', 0.0, 'madder', 1.0)
    L.line([(386, 98), (394, 120), (398, 140)], 'black', 0.9)                                  # rein
    L.line([(304, 92), (306, 84)], 'linen', 4.0)                                               # neck
    profile_head(L, 304, 76, 10, facing=1, helmet='madder')


def claw_repair(L):
    """The Ice Claw rider, re-stitched whole: arms flung out, his mail coat hanging down the horse's side, his leg
    below it, a profile face looking back along his claw."""
    clear(L, [(300, 68), (366, 68), (366, 126), (360, 148), (362, 206), (326, 206), (326, 150), (300, 124)])
    v = math.pi / 2
    L.poly([(340, 196), (352, 198), (354, 228), (366, 240), (362, 246), (344, 244), (342, 222)], 'navy', v, 'black', 1.1)
    L.poly([(334, 108), (352, 106), (360, 130), (362, 166), (366, 202), (346, 206), (326, 202), (330, 164), (330, 132)],
           'mail', v, 'madder', 1.4)
    L.line([(328, 190), (346, 194), (364, 190)], 'madder', 1.0)
    sleeve(L, (336, 106), (334, 120), (306, 104), (306, 116), 'madder', 0.0)                   # under the claw's cuff
    sleeve(L, (350, 106), (354, 120), (380, 104), (380, 116), 'madder')
    L.ellipse(386, 110, 5, 6, 'linen', 0.0, 'madder', 1.0)
    L.line([(343, 106), (343, 98)], 'linen', 4.0)
    profile_head(L, 342, 90, 9, facing=-1, helmet='sage')


REPAIRS = {'ghost': ghost_repair, 'claw': claw_repair}


def scene_labels(name, after=True, **kw):
    """(wool map, forced thread angles) for a scene, before or after its swap."""
    lab = BS.trace(name, S)
    if name in REPAIRS:
        L0 = Layer(lab.shape[1], lab.shape[0])
        REPAIRS[name](L0)
        wl, _ = L0.arrays()
        lab = lab.copy()
        lab[wl != NONE] = wl[wl != NONE]
    if not after:
        return lab, None
    er, ov = masks(name, lab.shape)
    clean = lab
    for m, excl in stroke_masks(name, lab.shape):
        clean = BS.fill_from_neighbours(clean, m, excl)
    L = Layer(lab.shape[1], lab.shape[0])
    SCENES[name]['draw'](L, **kw)
    if name == 'ghost' and kw.get('text', True) and kw.get('grow', 1.0) >= 1.0:
        ghost_caption(L)
    wl, wa = L.arrays()
    out = clean.copy()
    on = wl != NONE
    out[on] = wl[on]
    hand = ov & (clean != BS.IDX['linen'])
    out[hand] = clean[hand]
    show = np.zeros(lab.shape, bool)
    if SCENES[name].get('show'):
        im = Image.new('L', (lab.shape[1], lab.shape[0]), 0)
        dd = ImageDraw.Draw(im)
        for poly in SCENES[name]['show']:
            dd.polygon([(x * S, y * S) for x, y in poly], fill=255)
        show = np.asarray(im) > 0
        out[show] = clean[show]
    hand |= show
    forced = np.where(on & ~hand, wa, np.nan).astype(np.float32)
    return out, forced


def build(names=None):
    os.makedirs(CACHE, exist_ok=True)
    for name in names or SCENES:
        lab, _ = scene_labels(name, after=False)
        Image.fromarray(BS.stitch(lab, 3.0, seed=7)).save(os.path.join(CACHE, f'{name}-before.png'))
        lab2, forced = scene_labels(name)
        Image.fromarray(BS.stitch(lab2, 3.0, forced, seed=7)).save(os.path.join(CACHE, f'{name}-after.png'))
        if name == 'ghost':
            lab3, forced3 = scene_labels(name, grow=0.0, text=False)
            Image.fromarray(BS.stitch(lab3, 3.0, forced3, seed=7)).save(os.path.join(CACHE, 'ghost-pistol.png'))
        print('built', name, lab.shape, flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'build':
        build(sys.argv[2:] or None)
    elif sys.argv[1] == 'check':
        out = sys.argv[2]
        os.makedirs(out, exist_ok=True)
        for name in SCENES:
            lab = BS.trace(name, S)
            er, ov = masks(name, lab.shape)
            im = BS.RGB[lab].copy()
            im[er] = im[er] * 0.3 + np.array([255, 0, 200]) * 0.7
            im[ov] = im[ov] * 0.5 + np.array([0, 255, 0]) * 0.5
            lab2, _ = scene_labels(name)
            both = np.concatenate([im, BS.RGB[lab2]], 1).astype(np.uint8)
            Image.fromarray(both).save(os.path.join(out, f'{name}-check.png'))
