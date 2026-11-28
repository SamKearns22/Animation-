#!/usr/bin/env python3
"""MAP  disguise: the small-boat disguise worn over any person's own clothes (The Patriot 5, brief row 17, Sam 27 Nov:
"base these clothes on migrants/small boat people"; references/patriots-5/migrants 01-05). Kit pieces, for any film:

  life_jacket(col) .. body prop: an orange buoyancy vest over the jacket, cut to the person's own torso outline in
                      every view (chest panels with the opening down the middle, two black straps with buckles, the
                      fat collar behind the neck); col: its orange
  puffer(col) ....... body prop: a puffer jacket's quilting (stitched bands across the body) in the jacket's colour
  hood(col) ......... body prop: a hoodie's hood lying back round the neck (shows above the shoulders; from behind)
  blanket(base, stripe) .. head prop: a patterned blanket wrapped round the shoulders, over the arms to the elbows
                      (drawn after the arms: it covers them), a band pattern of stripes and a zig-zag
  beads(side) ....... prop: prayer beads (a loop of small beads and a tassel, no cross) hanging from one fist
  The head pieces live with the balaclava (facehouse_d): `niqab` (black face veil), `kufi` (white knitted prayer cap).
  dress(sp, j, kit) . puts a kit dict on a person (keys: life, puffer, hood, blanket, beads, niqab, kufi)
  python3 source/disguise.py sheet OUT.jpg   each piece alone on a grey test person, five turns (rule 89)
No writing anywhere (Sam). The joke targets the fascists, never Muslims or migrants (Sam).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import people_parts as PP      # noqa: E402
from ink import INK, curve     # noqa: E402

B, V = PP.B, PP.V
ORANGE = (240, 112, 28)
STRAP = (24, 24, 28)
VIEWS = ('front', 'three', 'side', 'three_back', 'back')
dk = lambda c, k=0.72: tuple(int(v * k) for v in c)   # noqa: E731


def _clip_y(poly, y0, y1):
    """The polygon cut to the band y0 <= y <= y1 (Sutherland-Hodgman on two horizontal lines)."""
    def cut(pts, keep, at):
        out = []
        for i in range(len(pts)):
            a, b = pts[i - 1], pts[i]
            ia, ib = keep(a), keep(b)
            if ia != ib:
                t = (at - a[1]) / ((b[1] - a[1]) or 1e-9)
                out.append((a[0] + t * (b[0] - a[0]), at))
            if ib:
                out.append(b)
        return out
    pts = cut(list(poly), lambda q: q[1] >= y0, y0)
    return cut(pts, lambda q: q[1] <= y1, y1) if pts else []


def _grow(poly, d):
    """Each point pushed d away from the polygon's middle (a vest is thicker than the cloth under it)."""
    cx = sum(x for x, _ in poly) / len(poly)
    cy = sum(y for _, y in poly) / len(poly)
    out = []
    for x, y in poly:
        dx, dy = x - cx, y - cy
        n = math.hypot(dx, dy) or 1.0
        out.append((x + d * dx / n, y + d * dy / n))
    return out


def _span(poly, y):
    """(left, right) of the polygon at height y."""
    xs = []
    for i in range(len(poly)):
        (x0, y0), (x1, y1) = poly[i - 1], poly[i]
        if (y0 - y) * (y1 - y) <= 0 and y0 != y1:
            xs.append(x0 + (y - y0) / (y1 - y0) * (x1 - x0))
    return (min(xs), max(xs)) if xs else None


def life_jacket(col=ORANGE):
    import limbs
    limbs.KEEP_OVER.update({tuple(col), dk(col, 0.82)})   # the arm is in front of the vest: never see-through over it

    def draw(p, view, sp):
        out = V.torso_outline(sp, view, sp.get('bottom', 500))
        sw0 = sp.get('shoulders', 150)
        # the armholes: the vest's top stays inside the shoulders' round (the arm's join is left clear, so the
        # shoulder never fades orange into the sleeve)
        vest = [(max(-0.62 * sw0, min(0.62 * sw0, x)) if y < 250 else x, y) for x, y in _clip_y(out, -8, 330)]
        vest = _grow(vest, 7)
        if len(vest) < 3:
            return
        sw = sp.get('shoulders', 150)
        # the fat collar behind the neck: seen above the shoulders front on, a roll across the back from behind
        if view in ('front', 'three'):
            for sg in (-1, 1):
                cx = sg * 52 + (12 if view == 'three' else 0)
                p.poly(curve([(cx - 26, 18), (cx - 22, -26), (cx, -40), (cx + 22, -26), (cx + 26, 18)], 3), col, INK, 2.4)
        elif view in ('back', 'three_back'):
            o = -14 if view == 'three_back' else 0
            p.poly(curve([(o - 70, 20), (o - 74, -22), (o - 30, -42), (o + 30, -42), (o + 74, -22), (o + 70, 20)], 3),
                   col, INK, 2.4)
        else:
            p.poly(curve([(-60, 20), (-64, -30), (-30, -46), (-6, -30), (-4, 20)], 3), col, INK, 2.4)
        p.poly(vest, col, INK, 2.6)
        shade = dk(col, 0.82)
        if view in ('front', 'three'):
            mid = 0 if view == 'front' else sw * 0.3
            gap = 18
            # the opening down the middle: the jacket under it shows between the two chest panels
            p.poly([(mid - gap, 30), (mid + gap, 30), (mid + gap * 0.7, 334), (mid - gap * 0.7, 334)],
                   sp.get('jacket', (30, 30, 34)), INK, 2.0)
            for sg in (-1, 1):                    # the panels' seams (the foam blocks)
                xs = mid + sg * (gap + 0.42 * sw)
                p.line([(xs, 60), (xs, 320)], shade, 2.0)
        elif view == 'side':
            sp_ = _span(vest, 200)
            if sp_:
                p.line([(0.5 * (sp_[0] + sp_[1]), 10), (0.5 * (sp_[0] + sp_[1]), 326)], shade, 2.0)   # the side seam
        else:
            p.line([(-0.45 * sw, 60), (-0.45 * sw, 320)], shade, 2.0)
            p.line([(0.45 * sw, 60), (0.45 * sw, 320)], shade, 2.0)
        for y in (210, 286):                      # two black straps round the body with their buckles
            sp_ = _span(vest, y)
            if not sp_:
                continue
            l, r = sp_
            p.poly([(l + 2, y - 9), (r - 2, y - 9), (r - 2, y + 9), (l + 2, y + 9)], STRAP, INK, 1.6)
            if view in ('front', 'three'):
                bx = 0 if view == 'front' else sw * 0.3
                p.poly([(bx - 14, y - 13), (bx + 14, y - 13), (bx + 14, y + 13), (bx - 14, y + 13)], (54, 54, 60), INK, 1.6)
    return draw


def puffer(col=None):
    """The quilting: stitched bands across the body, bowed a little (each band puffs out)."""
    def draw(p, view, sp):
        base = col or sp.get('jacket', (30, 30, 34))
        c = dk(base, 0.6) if sum(base) > 300 else tuple(min(255, int(v * 1.9 + 26)) for v in base)   # dark cloth: lighter seams
        out = V.torso_outline(sp, view, sp.get('bottom', 500))
        for y in range(80, sp.get('bottom', 500) - 20, 62):
            s = _span(out, y)
            if s:
                p.line(curve([(s[0] + 8, y), (0.5 * (s[0] + s[1]), y + 6), (s[1] - 8, y)], 3), c, 2.2)
    return draw


def hood(col=(70, 72, 80)):
    """A hoodie's hood lying back: a soft roll round the back of the neck, its edge showing over the shoulders."""
    def draw(p, view, sp):
        if view == 'front':
            for sg in (-1, 1):
                p.poly(curve([(sg * 34, -8), (sg * 70, -14), (sg * 92, 6), (sg * 60, 14)], 3), col, INK, 2.2)
        elif view == 'three':
            p.poly(curve([(-80, 6), (-60, -18), (-30, -12), (-40, 12)], 3), col, INK, 2.2)
        elif view == 'side':
            p.poly(curve([(-30, -18), (-80, -10), (-104, 40), (-70, 70), (-40, 30)], 3), col, INK, 2.2)
        else:
            p.poly(curve([(-70, -10), (0, -24), (70, -10), (64, 60), (0, 96), (-64, 60)], 3), col, INK, 2.2)
            p.line(curve([(-40, 0), (0, 70), (40, 0)], 3), dk(col), 1.8)
    return draw


def blanket(base=(176, 34, 38), stripe=(240, 236, 226)):
    """Head prop (drawn after the arms): the blanket over both shoulders and round the upper arms to the elbows,
    open at the front over the chest, a pattern of white bands and a zig-zag across it."""
    def draw(p, view, sp, hx, hy):
        sw = sp.get('shoulders', 150) + 26
        y0 = hy + 150                              # the neck's foot (the head prop's frame: head centre at hy)
        if view in ('front', 'three'):
            o = 0.22 * sw if view == 'three' else 0.0
            for sg in (-1, 1):
                k = 0.86 if (view == 'three' and sg < 0) else 1.0
                pts = [(o + sg * 30, y0 - 10), (o + sg * sw * 0.7 * k, y0 - 6), (o + sg * sw * 1.08 * k, y0 + 40),
                       (o + sg * sw * 1.14 * k, y0 + 210), (o + sg * sw * 0.86 * k, y0 + 236), (o + sg * sw * 0.5 * k, y0 + 290),
                       (o + sg * 40, y0 + 330), (o + sg * 26, y0 + 120), (o + sg * 20, y0 + 30)]
                _patterned(p, pts, base, stripe, (y0 + 70, y0 + 140, y0 + 210, y0 + 280))
        elif view == 'side':
            pts = [(-70, y0 - 14), (40, y0 - 10), (sw * 0.62, y0 + 30), (sw * 0.6, y0 + 230), (0, y0 + 290),
                   (-sw * 0.7, y0 + 260), (-sw * 0.8, y0 + 60)]
            _patterned(p, pts, base, stripe, (y0 + 70, y0 + 140, y0 + 210, y0 + 280))
        else:
            pts = [(-sw * 0.7, y0 - 8), (sw * 0.7, y0 - 8), (sw * 1.1, y0 + 40), (sw * 1.14, y0 + 230),
                   (sw * 0.5, y0 + 300), (-sw * 0.5, y0 + 296), (-sw * 1.14, y0 + 226), (-sw * 1.1, y0 + 40)]
            _patterned(p, pts, base, stripe, (y0 + 70, y0 + 140, y0 + 210, y0 + 280))
    return draw


def _patterned(p, pts, base, stripe, rows):
    """A piece of the blanket: the shape, then white bands and a zig-zag across it, kept inside."""
    from PIL import Image, ImageDraw
    shape = curve(pts, 3)
    base_pen = p.pen if hasattr(p, 'pen') else p
    img, cam = base_pen.img, base_pen.cam
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    lp = B.Pen(layer, cam)
    lp.poly(shape, base, None)
    xs = [x for x, _ in shape]
    l, r = min(xs) - 10, max(xs) + 10
    for k, y in enumerate(rows):
        if k == 1:                                 # the middle row a zig-zag, the others plain bands
            zz = []
            x = l
            while x < r:
                zz += [(x, y - 9), (x + 14, y + 9)]
                x += 28
            lp.line(zz, stripe, 4.0)
        else:
            lp.poly([(l, y - 6), (r, y - 6), (r, y + 6), (l, y + 6)], stripe, None)
            lp.line([(l, y + 12), (r, y + 12)], dk(base, 0.6), 2.0)
    ys = [y for _, y in shape]
    for k in range(1, 5):                          # the cloth's folds hanging down (a blanket, not a knit jumper)
        x = l + (r - l) * k / 5
        lp.line(curve([(x, min(ys) + 20), (x + 6, 0.5 * (min(ys) + max(ys))), (x - 4, max(ys))], 3), dk(base, 0.55), 2.6)
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).polygon([cam.P(*q) for q in shape], fill=255)
    a = layer.getchannel('A')
    from PIL import ImageChops
    layer.putalpha(ImageChops.multiply(a, m))
    img.alpha_composite(layer)
    p.line(shape + shape[:1], INK, 2.4)


def beads(side='R', col=(70, 120, 96)):
    """Prayer beads hanging from one fist: a loop of small beads, a longer marker bead and a short tassel."""
    def draw(p, j2):
        wr = j2['wr' + side]
        cx, cy = wr[0], wr[1] + 66
        n = 18
        pts = [(cx + 22 * math.sin(2 * math.pi * k / n), cy - 54 * math.cos(2 * math.pi * k / n)) for k in range(n)]
        p.line(pts + pts[:1], dk(col, 0.5), 2.0)
        for q in pts:
            p.ell(q[0], q[1], 7.0, 7.0, col, INK, 1.4)
        p.ell(cx, cy + 64, 6.0, 10.0, col, INK, 1.4)
        for dx in (-5, 0, 5):
            p.line([(cx, cy + 72), (cx + dx, cy + 98)], dk(col, 0.6), 2.6)
    return draw


def dress(sp, j, kit):
    """kit: dict of what this person wears (life, puffer, hood, blanket, beads, niqab, kufi). The head pieces go on
    the house head's lines (sp['kit_house']), the rest on the pose."""
    props = list(j.get('body_props', []))
    if kit.get('puffer'):
        props.append(puffer())
    if kit.get('life', True):
        props.append(life_jacket(kit.get('life_c', ORANGE)))
    if kit.get('hood'):                           # the hoodie's hood lies back over the vest's collar
        props.append(hood(kit['hood'] if isinstance(kit['hood'], tuple) else (70, 72, 80)))
    j['body_props'] = props
    if kit.get('blanket'):
        j['head_props'] = list(j.get('head_props', [])) + [blanket()]
    if kit.get('beads'):
        side = kit['beads'] if kit['beads'] in ('L', 'R') else 'R'
        j['props'] = list(j.get('props', [])) + [beads(side)]
        j.setdefault('hand', {})[side] = 'fist'
    kh = dict(sp.get('kit_house') or {})
    for k in ('niqab', 'kufi'):
        if kit.get(k):
            kh[k] = True
    if kh:
        sp['kit_house'] = kh
    return sp, j


def sheet(out):
    """Each piece alone on a grey test person (rule 89; people in tests are grey), five turns."""
    from PIL import Image, ImageDraw
    import patriots5_cast as P5
    P5.install()
    B.SS = 1
    rows = [('life jacket', dict(life=True)), ('puffer + hood + life jacket', dict(puffer=True, hood=True)),
            ('blanket + beads', dict(life=False, blanket=True, beads='R')), ('niqab', dict(life=False, niqab=True)),
            ('kufi', dict(life=False, kufi=True))]
    T = 300
    img = Image.new('RGB', (5 * T + 220, len(rows) * (T + 30) + 20), (232, 228, 222))
    d = ImageDraw.Draw(img)
    for r, (name, kit) in enumerate(rows):
        d.text((10, 20 + r * (T + 30) + T // 2), name, fill=(0, 0, 0))
        for k, yaw in enumerate((0, 45, 90, 135, 180)):
            sp, j = P5.grey_man()
            sp, j = dress(sp, j, kit)
            tile = Image.new('RGBA', (1080, 2600), (232, 228, 222, 255))
            P5.draw(tile, B.Cam(1.0, 540, 960), 540, 1500, 0.62, sp, j, yaw)
            t = tile.crop((290, 1250, 790, 2110)).convert('RGB')
            t.thumbnail((T, T))
            img.paste(t, (220 + k * T, 20 + r * (T + 30)))
    img.save(out, quality=88)
    return out


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    else:
        print(__doc__)
