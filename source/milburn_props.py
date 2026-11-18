#!/usr/bin/env python3
"""Milburn: the held weapons and the plinths (chat 6, 17 Nov; scenes 3 and 6).

MAP
  shapes ........... SHAPES: each prop as flat parts in metres (x along its length from the grip, y across, down +):
                     crossbow, katana, uzi, grenade (ostrich-egg size, Sam Q2), mace (spiked, Sam Q3), stapler ("DLC")
  draw ............. draw(name, poly, origin, ang, k): the parts turned `ang` degrees, k units per metre, through
                     `poly(pts, fill, ink_width)` (a person's Pen or a picture's ImageDraw)
  held ............. in_hands(j, sp, name, a, b): the prop laid from hand A's grip towards hand B (two hands) or at
                     angle b (one hand), with grips.held so each hand is drawn over it
  plinth ........... plinth(d, cam, x, dep, prop): a grey plinth 1.0 m high, 0.5 m square, seen by a level camera
                     (front, top, the side we see), its prop lying on the top; the "DLC" tag on the stapler's

    python3 source/milburn_props.py sheet OUT.jpg       every prop alone, big, on white
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ed import INK          # noqa: E402

WOOD, WOOD_D = (128, 84, 50), (96, 60, 36)
STEEL, STEEL_D, BLADE = (96, 100, 108), (60, 62, 68), (214, 222, 230)
BLACK, GOLD, OLIVE = (40, 40, 44), (196, 160, 70), (92, 104, 58)


def _rect(x0, x1, h0, h1):
    return [(x0, h0), (x1, h0), (x1, h1), (x0, h1)]


def _ell(cx, cy, rx, ry, n=20):
    return [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in [2 * math.pi * i / n for i in range(n)]]


def _spikes(cx, cy, r, n, ln):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        b1, b2 = a - 0.22, a + 0.22
        out.append([(cx + r * math.cos(b1), cy + r * math.sin(b1)), (cx + (r + ln) * math.cos(a),
                                                                       cy + (r + ln) * math.sin(a)),
                    (cx + r * math.cos(b2), cy + r * math.sin(b2))])
    return out


SHAPES = {
    'crossbow': [(_rect(-0.30, -0.06, -0.05, 0.06), WOOD_D, 2.0),          # the butt
                 (_rect(-0.08, 0.46, -0.035, 0.035), WOOD, 2.0),           # the stock
                 (_rect(0.0, 0.06, 0.03, 0.12), WOOD_D, 1.8),              # the trigger grip under the hand
                 ([(0.40, -0.36), (0.47, -0.33), (0.50, 0.0), (0.47, 0.33), (0.40, 0.36), (0.44, 0.0)],
                  BLACK, 2.0),                                             # the bow's limbs
                 ([(0.41, -0.35), (0.12, -0.02), (0.12, 0.02), (0.41, 0.35)], None, 1.2),   # the string
                 (_rect(0.12, 0.58, -0.012, 0.012), STEEL, 1.4),           # the bolt
                 ([(0.58, -0.025), (0.65, 0.0), (0.58, 0.025)], STEEL_D, 1.4)],
    'katana': [(_rect(-0.14, 0.12, -0.018, 0.018), BLACK, 1.8),             # the wrapped hilt
               (_ell(0.13, 0.0, 0.012, 0.045), GOLD, 1.6),                  # the guard
               ([(0.14, -0.016), (0.80, -0.02), (0.87, 0.004), (0.80, 0.014), (0.14, 0.016)], BLADE, 1.8)],
    'uzi': [(_rect(-0.07, 0.20, -0.075, -0.015), STEEL_D, 1.8),             # the body over the hand
            (_rect(0.20, 0.25, -0.06, -0.035), BLACK, 1.4),                 # the barrel stub
            (_rect(-0.02, 0.035, -0.02, 0.15), BLACK, 1.8)],                # the grip and its magazine
    'grenade': [(_ell(0.0, 0.0, 0.085, 0.105), OLIVE, 2.2),                 # an egg the size of an ostrich's
                (_rect(-0.03, 0.03, -0.135, -0.1), STEEL, 1.6),            # the fuse
                ([(0.02, -0.13), (0.07, -0.12), (0.075, -0.02), (0.06, -0.02), (0.055, -0.11), (0.02, -0.115)],
                 STEEL, 1.4),                                              # the lever
                (_ell(-0.045, -0.13, 0.022, 0.022), None, 1.6)],           # the pin's ring
    'mace': [(_rect(-0.05, 0.5, -0.016, 0.016), WOOD, 1.8)]
            + [(s, STEEL, 1.4) for s in _spikes(0.58, 0.0, 0.075, 10, 0.05)]
            + [(_ell(0.58, 0.0, 0.08, 0.08), STEEL_D, 2.0)],
    'stapler': [(_rect(-0.09, 0.09, 0.0, 0.016), BLACK, 1.6),               # the base
                ([(-0.09, 0.0), (-0.09, -0.04), (0.09, -0.03), (0.09, -0.012), (-0.07, -0.01)], (200, 40, 40), 1.8)],
}
SCALE = {'uzi': 1.6, 'grenade': 1.04}           # cartoon sizes so they read at phone size (the grenade 35% smaller, Sam chat 11; an
#                                                    ostrich egg, Sam Q2)
LENGTH = {'crossbow': 0.95, 'katana': 1.0, 'uzi': 0.32, 'grenade': 0.22, 'mace': 0.7, 'stapler': 0.18}


def draw(name, poly, origin, ang, k, flip=False):
    """The prop's parts turned `ang` degrees (0: along +x on screen, + clockwise as y runs down), k per metre."""
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    ox, oy = origin
    k *= SCALE.get(name, 1.0)
    for pts, fill, w in SHAPES[name]:
        q = [(ox + k * (x * c - (-y if flip else y) * s), oy + k * (x * s + (-y if flip else y) * c)) for x, y in pts]
        poly(q, fill, w)


def units_per_m(sp):
    return 928.0 / (0.84 * sp['height'])


def in_hands(j, sp, name, a='R', b='L', ang=None, flip=False, along=0.0):
    """The prop held in hand `a` (its grip in that hand) pointing at hand `b` (or at `ang` degrees when b is None);
    `along` slides it along its axis (m). Each holding hand is drawn over it."""
    import grips
    import views as V
    k = units_per_m(sp)

    def pen_poly(p):
        def poly(q, fill, w):
            if fill is None:
                p.line(q, INK, w)
            else:
                p.poly(q, fill, INK, w)
        return poly

    def go(p, j2):
        ha = grips.hand_centre(j2_3(j2, a), a)
        if b:
            hb = grips.hand_centre(j2_3(j2, b), b)
            an = math.degrees(math.atan2(hb[1] - ha[1], hb[0] - ha[0]))
        else:
            an = ang
        c = math.cos(math.radians(an)), math.sin(math.radians(an))
        draw(name, pen_poly(p), (ha[0] + c[0] * along * k, ha[1] + c[1] * along * k), an, k, flip)
    grips.held(j, a, sp, go)
    if b:
        grips.held(j, b, sp, lambda p, j2: None)
    return j


def j2_3(j2, side):
    """The 2D drawn joints as 3D points (depth 0) for grips.hand_centre."""
    return {'el' + side: (*j2['el' + side], 0.0), 'wr' + side: (*j2['wr' + side], 0.0)}


# ------------------------------------------------------------------------------------------------ plinths
GREY, GREY_TOP, GREY_SIDE = (150, 152, 156), (184, 186, 190), (122, 124, 128)


def plinth(d, cam, x, dep, prop=None, ss=1, tag=False):
    """A grey plinth (1.0 m high, 0.5 m square) at (x, dep) seen by a level camera `cam` (cam.p(x, d, z) in
    pixels), on ImageDraw `d` drawn `ss` times big; its prop lying on the top."""
    def P(xx, dd, zz):
        X, Y = cam.p(xx, dd, zz)
        return X * ss, Y * ss
    h, r = 1.0, 0.25
    x0, x1, d0, d1 = x - r, x + r, dep - r, dep + r
    if x > 0:                                                    # right of the lens: its left side shows
        d.polygon([P(x0, d0, 0), P(x0, d1, 0), P(x0, d1, h), P(x0, d0, h)], fill=GREY_SIDE, outline=INK)
    else:
        d.polygon([P(x1, d0, 0), P(x1, d1, 0), P(x1, d1, h), P(x1, d0, h)], fill=GREY_SIDE, outline=INK)
    d.polygon([P(x0, d0, h), P(x1, d0, h), P(x1, d1, h), P(x0, d1, h)], fill=GREY_TOP, outline=INK)
    d.polygon([P(x0, d0, 0), P(x1, d0, 0), P(x1, d0, h), P(x0, d0, h)], fill=GREY, outline=INK)
    w = max(1, int(2.2 * ss))
    for a, b in ((P(x0, d0, 0), P(x0, d0, h)), (P(x1, d0, 0), P(x1, d0, h)), (P(x0, d0, h), P(x1, d0, h))):
        d.line([a, b], fill=INK, width=w)
    if prop:
        k = cam.ppm(dep) * ss
        X, Y = P(x, dep - 0.05, h)

        def poly(q, fill, lw):
            if fill is None:
                d.line(q, fill=INK, width=max(1, int(lw * ss * k / 700)))
            else:
                d.polygon(q, fill=fill, outline=INK)
        lift = {'grenade': 0.105, 'stapler': 0.03, 'mace': 0.13}.get(prop, 0.04)
        big = {'stapler': 2.6}.get(prop, 1.0)                     # the stapler drawn big enough to read as one
        mid = {'mace': 0.5}.get(prop, LENGTH[prop] * 0.0)       # the mace's head on the plinth, its handle out
        draw(prop, poly, (X - mid * k * big - (0.0 if prop == 'mace' else 0.0), Y - lift * k * big), 0.0, k * big,
             flip=False)
        if tag:                                                   # the "DLC" sticker on the stapler's plinth
            from PIL import ImageFont
            fx0, fy = P(x - 0.1, d0, h - 0.1)
            fx1, fy1 = P(x + 0.1, d0, h - 0.2)
            d.rounded_rectangle([fx0, fy, fx1, fy1], radius=int(6 * ss), fill=(255, 196, 0), outline=INK,
                                width=max(1, int(2 * ss)))
            f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), max(8, int((fy1 - fy) * 0.62)))
            d.text(((fx0 + fx1) / 2, (fy + fy1) / 2), 'DLC', font=f, fill=INK, anchor='mm')


def sheet(out):
    from PIL import Image, ImageDraw
    im = Image.new('RGB', (1500, 900), 'white')
    d = ImageDraw.Draw(im)
    for i, n in enumerate(SHAPES):
        k = 600 if n not in ('grenade', 'stapler', 'uzi') else 1400
        ox, oy = 80 + (i % 3) * 480, 200 + (i // 3) * 420

        def poly(q, fill, lw):
            if fill is None:
                d.line(q, fill=INK, width=2)
            else:
                d.polygon(q, fill=fill, outline=INK)
        draw(n, poly, (ox + (60 if k > 600 else 0), oy), 0.0, k)
        d.text((ox, oy + 160), n, fill='black')
    im.save(out)
    return out


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    else:
        print(__doc__)
