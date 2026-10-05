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
        p = [(x * S, y * S) for x, y in pts]
        self.dl.polygon(p, fill=BS.IDX[wool])
        self.da.polygon(p, fill=float(ang))
        if outline:
            self.line(list(pts) + [pts[0]], outline, ow, ang)

    def line(self, pts, wool, w, ang=None):
        p = [(x * S, y * S) for x, y in pts]
        for (x0, y0), (x1, y1) in zip(p, p[1:]):
            a = math.atan2(y1 - y0, x1 - x0) if ang is None else ang
            self.dl.line([(x0, y0), (x1, y1)], fill=BS.IDX[wool], width=max(1, int(round(w * S))))
            self.da.line([(x0, y0), (x1, y1)], fill=float(a), width=max(1, int(round(w * S))))
            r = w * S / 2
            for (x, y) in ((x0, y0), (x1, y1)):
                self.dl.ellipse([x - r, y - r, x + r, y + r], fill=BS.IDX[wool])
                self.da.ellipse([x - r, y - r, x + r, y + r], fill=float(a))

    def ellipse(self, cx, cy, rx, ry, wool, ang=0.0, outline=None, ow=1.4):
        n = 40
        pts = [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
        self.poly(pts, wool, ang, outline, ow)

    def arrays(self):
        return np.asarray(self.lab, np.int16), np.asarray(self.ang, np.float32)


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
    hand = (304, 111)
    ang = math.atan2(24, -45)                    # out to the left and down, over the next horse's neck
    K = 0.82
    f = local(hand, ang, K)
    a = ang
    L.poly(f([(-22, -15), (8, -18), (18, -12), (18, 12), (8, 18), (-22, 15)]), 'navy', a, 'black')        # cuff
    L.poly(f([(-18, -9), (12, -11), (12, -6), (-18, -4)]), 'ice', a)                                       # frost light
    L.poly(f([(10, -22), (34, -24), (42, -10), (42, 12), (34, 24), (10, 22)]), 'black', a, 'black')        # palm housing
    L.ellipse(*f([(26, 0)])[0], 6, 6, 'ice', a, 'navy')                                                    # core
    # three ice fingers, each in two jointed pieces, curving like talons
    for sp, cv in ((-0.55, 1), (0.0, 1), (0.55, 1)):
        base = (40, sp * 30)
        g = local(f([base])[0], a + sp * 0.9, K)
        L.poly(g(rect(0, 18, -5, 5)), 'black', a + sp * 0.9, 'black')
        tip = [(16, -6), (30, -6), (58, 2 + 6 * sp), (34, 7), (16, 6)]
        L.poly(g(tip), 'ice', a + sp * 0.9, 'navy')
        L.poly(g([(20, -3), (40, -2), (50, 2 + 6 * sp), (38, 1)]), 'frost', a + sp * 0.9)
    # stitched frost around it: short pale lines and stars
    cx, cy = f([(50, 0)])[0]
    rng = np.random.default_rng(3)
    for i in range(16):
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

def william_skin(L):
    """PARTY SUIT: purple suit, wide flared cuffs, feather boa, rhinestone boots, big purple cowboy hat."""
    v = math.pi / 2
    L.poly([(232, 172), (300, 172), (305, 240), (307, 332), (276, 334), (262, 252), (238, 200)], 'purple', v, 'black')
    L.line([(282, 176), (290, 330)], 'lilac', 1.4)                                                 # trouser crease
    L.poly([(270, 328), (310, 328), (318, 350), (304, 362), (268, 360)], 'frost', 0.0, 'navy')       # boots
    rng = np.random.default_rng(5)
    for _ in range(14):                                                                          # rhinestones
        L.ellipse(272 + rng.uniform(0, 40), 332 + rng.uniform(0, 26), 1.6, 1.6, rng.choice(['ice', 'lilac', 'plasmapale']))
    L.poly([(212, 88), (300, 86), (306, 122), (301, 180), (230, 182), (212, 140)], 'purple', v, 'black')  # jacket
    L.line([(258, 90), (250, 130), (258, 178)], 'lilac', 1.6)                                    # lapel edge
    L.line([(272, 90), (266, 130)], 'lilac', 1.6)
    for y in (140, 156):
        L.ellipse(262, y, 2.2, 2.2, 'ochre')                                                    # buttons
    L.poly([(286, 86), (322, 88), (322, 114), (292, 120)], 'purple', 0.1, 'black')               # pointing sleeve
    L.poly([(318, 82), (342, 72), (346, 120), (318, 116)], 'lilac', v, 'purple')                 # wide cuff
    L.poly([(238, 94), (262, 92), (288, 116), (272, 132), (248, 120)], 'purple', 0.8, 'black')   # club arm
    L.poly([(260, 108), (278, 104), (282, 126), (266, 128)], 'lilac', 0.8, 'purple')             # its cuff
    # the boa: fluffy loops round his neck, trailing down his back
    pts = [(222, 86), (240, 92), (258, 94), (276, 92), (292, 86)] + [(210, 96), (202, 112), (198, 130), (200, 150),
                                                                       (206, 168), (204, 186)]
    for i, (x, y) in enumerate(pts):
        L.ellipse(x, y, 9, 7, 'boa', i * 0.7, 'lilac', 1.0)
        L.ellipse(x + 3, y - 2, 3, 2, 'lilac', 0.0)
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
    L.poly([(150, 380), (210, 380), (220, 432), (146, 432)], 'shark', v, 'navy', 1.6)            # costume feet
    L.poly([(298, 110), (344, 72), (336, 134)], 'shark', 0.6, 'navy', 1.6)                         # dorsal fin
    L.poly([(292, 372), (334, 396), (352, 432), (318, 428), (284, 404)], 'shark', 0.8, 'navy', 1.6)  # tail
    L.ellipse(250, 82, 44, 40, 'shark', v, 'navy', 1.6)                                          # hood
    L.poly([(186, 38), (250, 40), (318, 28), (318, 54), (250, 60), (186, 60)], 'shark', 0.0, 'navy', 1.8)  # hammer
    L.ellipse(186, 49, 12, 11, 'shark', 0.0, 'navy', 1.6)
    L.ellipse(320, 41, 12, 13, 'shark', 0.0, 'navy', 1.6)
    for ex, ey in ((186, 48), (322, 38)):
        L.ellipse(ex, ey, 6, 6, 'black')
        L.ellipse(ex + 1.5, ey - 1.5, 1.8, 1.8, 'frost')
    for i in range(7):                                                                            # teeth round the face
        x = 226 + i * 6.5
        L.poly([(x, 104), (x + 6, 104), (x + 3, 96)], 'frost', 0.0)
        L.poly([(x, 54), (x + 6, 54), (x + 3, 61)], 'frost', 0.0)
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
    L.poly([(345, 178), (420, 162), (456, 186), (472, 216), (502, 262), (506, 326), (460, 334), (404, 336),
            (344, 330), (328, 290), (318, 240), (334, 204)], 'yellow', v, 'madder', 1.6)          # onesie
    for x in (366, 394):                                                                          # foot paws
        L.ellipse(x, 338, 14, 8, 'yellow', 0.0, 'madder', 1.2)
    L.ellipse(386, 152, 42, 46, 'yellow', v, 'madder', 1.6)                                       # hood
    L.poly([(362, 122), (338, 46), (354, 50), (378, 118)], 'yellow', 1.9, 'madder', 1.4)          # ears
    L.poly([(338, 46), (343, 66), (352, 64), (354, 50)], 'black', 1.9)
    L.poly([(396, 118), (412, 44), (426, 48), (410, 124)], 'yellow', 1.4, 'madder', 1.4)
    L.poly([(412, 44), (426, 48), (422, 64), (410, 62)], 'black', 1.4)
    for cx in (352, 420):                                                                         # cheek patches
        L.ellipse(cx, 166, 6.5, 6.5, 'terracotta', 0.0, 'madder', 1.0)
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
                   show=[[(228, 60), (266, 60), (268, 98), (232, 100)],                   # face
                         [(162, 58), (206, 58), (206, 102), (166, 102)]]),                # raised hand
    'edward': dict(erase=[], keep=[], over=[], draw=edward_skin,
                   show=[[(361, 130), (411, 130), (414, 194), (362, 196)],                # his whole face and beard
                         [(383, 220), (400, 220), (400, 240), (383, 240)]]),             # sceptre hand
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


def scene_labels(name, after=True, **kw):
    """(wool map, forced thread angles) for a scene, before or after its swap."""
    lab = BS.trace(name, S)
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
