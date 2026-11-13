#!/usr/bin/env python3
"""Protest Tiers: pencil roughs of the four re-staged scenes (rule 11 composition sheet).

MAP
  helpers ............ G1-G3 greys, person/officer/flag shapes, text
  t1() ............... Passeig de Gracia, high camera behind the march (perspective in metres)
  t2() ............... Frankfurt gun store from the near pavement
  t3() ............... Place de la Republique, low camera, Marianne centre
  t4() ............... Tirana avenue, burning sky, rocket diagonal
  overlay() .......... safe area, eye level, focus rings by beat, movement arrows, Hook Text box
  sheet() ............ 2 x 2 labelled sheet
Run: python3 source/protest_tiers_roughs.py OUTDIR   (writes t1..t4.png clean and sheet.jpg)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
import pencil_cartoon as pc  # noqa: E402
from pencil_cartoon import Canvas, col, ell, blob  # noqa: E402

HERE = os.path.dirname(__file__)
W, H = 1080, 1920
G1, G2, G3, G4 = col(.72, .71, .69), col(.50, .49, .48), col(.30, .29, .29), col(.14, .13, .14)
FIRE_O, FIRE_Y, FIRE_R = col(.98, .55, .15), col(1, .86, .35), col(.85, .25, .10)
BLUE, BLUE_L = col(.20, .38, .86), col(.55, .70, 1.0)
CAT_Y, CAT_R = col(.98, .82, .25), col(.82, .15, .12)
OCHRE = col(.86, .70, .32)
LIME = col(.40, .72, .30)
R = np.random.default_rng(3)


def _apply_soft(self, m, x0, y0, color, pressure, opacity, gi):
    """Roughs: solid pencil with light grain (the toolkit's own grain leaves white specks on big fills)."""
    h, w = m.shape
    ox, oy = self.goff[gi]
    g = pc.GRAIN[gi][oy + y0:oy + y0 + h, ox + x0:ox + x0 + w]
    cov = np.clip(0.80 + 0.28 * g - (1 - pressure) * .6, 0, 1)
    a = (m * cov * opacity)[..., None]
    reg = self.img[y0:y0 + h, x0:x0 + w]
    reg += (color - reg) * a


Canvas._apply = _apply_soft


def dots(c, pts, r, color, opacity=1.0):
    """Many round pencil dots (heads) in one pass."""
    if len(pts) == 0:
        return
    im = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(im)
    for x, y in pts:
        d.ellipse((x - r, y - r * 1.1, x + r, y + r * 1.1), fill=255)
    c._apply(np.asarray(im, np.float32) / 255, 0, 0, color, .95, opacity, 0)


def font(sz, bold=False, anton=False):
    if anton:
        return ImageFont.truetype(os.path.join(HERE, 'fonts', 'Anton-Regular.ttf'), sz)
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''), sz)


# ---------------------------------------------------------------- figures (screen px)
def back_person(c, x, y, h, tone=G4, arm=0, seed=0):
    """Someone seen from behind, feet at (x, y), height h px. arm: 0 none, 1 raised (keys), 2 phone up."""
    hr = h * 0.075
    hy = y - h + hr
    c.poly(ell(x, hy, hr, hr * 1.1), fill=tone, line=G4, lw=max(1.5, h * .012), jit=.4)
    sh = h * 0.17
    body = [(x - sh, hy + hr * 1.2), (x + sh, hy + hr * 1.2), (x + sh * .85, y - h * .45),
            (x + sh * .6, y), (x - sh * .6, y), (x - sh * .85, y - h * .45)]
    c.poly(body, fill=tone, line=G4, lw=max(1.5, h * .012), jit=.5)
    if arm:
        s = 1 if seed % 2 else -1
        ax, ay = x + s * sh * .8, hy + hr * 1.6
        tx, ty = ax + s * h * .06, hy - h * .28
        c.line([(ax, ay), (tx, ty)], tone, lw=max(2, h * .05), jit=.3)
        if arm == 1:  # keys glint
            c.poly(ell(tx, ty - 3, max(2, h * .02), max(2, h * .02)), fill=col(1, .95, .6), jit=0)
        elif arm == 2:
            c.poly([(tx - h * .03, ty - h * .07), (tx + h * .03, ty - h * .07), (tx + h * .03, ty), (tx - h * .03, ty)],
                   fill=col(.85, .92, 1.0), line=G4, lw=1.5, jit=0)


def front_person(c, x, y, h, tone=G4, hood=True, pose='stand', face_left=False):
    """Black-clad figure, feet at (x, y). pose: stand, run, throw, swing."""
    s = -1 if face_left else 1
    hr = h * .08
    lean = {'stand': 0, 'run': .18, 'throw': -.08, 'swing': -.12}[pose] * s
    hx, hy = x + lean * h, y - h + hr
    c.poly(ell(hx, hy, hr * (1.15 if hood else 1), hr * 1.15), fill=tone, line=G4, lw=2, jit=.4)
    hip = (x + lean * h * .4, y - h * .45)
    c.poly([(hx - h * .12, hy + hr), (hx + h * .12, hy + hr), (hip[0] + h * .09, hip[1]), (hip[0] - h * .09, hip[1])],
           fill=tone, line=G4, lw=2, jit=.5)
    if pose == 'run':
        legs = [((hip[0], hip[1]), (x + s * h * .22, y - h * .18), (x + s * h * .30, y)),
                ((hip[0], hip[1]), (x - s * h * .12, y - h * .2), (x - s * h * .28, y - h * .1))]
        arms = [((hx, hy + hr * 2), (hx + s * h * .18, hy + h * .2)), ((hx, hy + hr * 2), (hx - s * h * .16, hy + h * .3))]
    else:
        legs = [((hip[0], hip[1]), (x - h * .09, y)), ((hip[0], hip[1]), (x + h * .09, y))]
        if pose == 'throw':
            arms = [((hx, hy + hr * 2), (hx - s * h * .1, hy - h * .2)), ((hx, hy + hr * 2), (hx + s * h * .18, hy + h * .2))]
        elif pose == 'swing':
            arms = [((hx, hy + hr * 2), (hx - s * h * .05, hy - h * .15))]
        else:
            arms = [((hx, hy + hr * 2), (hx + h * .14, hy + h * .3)), ((hx, hy + hr * 2), (hx - h * .14, hy + h * .3))]
    for ln in legs + arms:
        c.line(list(ln), tone, lw=max(2, h * .09), jit=.4)
    return hx, hy


def officer(c, x, y, h, tone=G4, helmet=G3, shield=col(.80, .84, .86), face_left=True, label=False):
    s = -1 if face_left else 1
    hr = h * .085
    hx, hy = x, y - h + hr
    c.poly(ell(hx, hy, hr * 1.15, hr * 1.1), fill=helmet, line=G4, lw=2, jit=.3)
    c.poly([(hx - h * .13, hy + hr), (hx + h * .13, hy + hr), (x + h * .11, y - h * .45), (x - h * .11, y - h * .45)],
           fill=tone, line=G4, lw=2, jit=.4)
    c.line([(x - h * .06, y - h * .45), (x - h * .08, y)], tone, lw=max(2, h * .08))
    c.line([(x + h * .06, y - h * .45), (x + h * .08, y)], tone, lw=max(2, h * .08))
    sx = x + s * h * .12
    c.poly([(sx - h * .1, y - h * .78), (sx + h * .1, y - h * .78), (sx + h * .1, y - h * .08), (sx - h * .1, y - h * .08)],
           fill=shield, line=G4, lw=2, jit=.6, opacity=.85)


def flag(c, x, y, h, colours, wave=0.0, vertical=False, eagle=False):
    """Pole foot at (x, y); striped cloth (colours top to bottom, or left to right if vertical); eagle: Albania's."""
    c.line([(x, y), (x, y - h)], G3, lw=max(2, h * .03))
    fw, fh = h * .55, h * .36
    n = len(colours)
    if vertical:
        for i, cc in enumerate(colours):
            u0, u1 = i / n, (i + 1) / n
            pts = [(x + fw * u, y - h + math.sin(u * 5 + wave) * fh * .12) for u in np.linspace(u0, u1, 4)]
            pts += [(x + fw * u, y - h + fh + math.sin(u * 5 + wave) * fh * .12) for u in np.linspace(u1, u0, 4)]
            c.poly(pts, fill=cc, line=None, jit=.3)
        c.poly([(x, y - h), (x + fw, y - h), (x + fw, y - h + fh), (x, y - h + fh)], line=G3, lw=1.5, jit=.8)
        return
    for i, cc in enumerate(colours):
        y0 = y - h + fh * i / n
        y1 = y - h + fh * (i + 1) / n
        pts = []
        for k in range(9):
            u = k / 8
            pts.append((x + fw * u, y0 + math.sin(u * 5 + wave) * fh * .12))
        for k in range(8, -1, -1):
            u = k / 8
            pts.append((x + fw * u, y1 + math.sin(u * 5 + wave) * fh * .12))
        c.poly(pts, fill=cc, line=None, jit=.3)
    c.poly([(x, y - h), (x + fw, y - h), (x + fw, y - h + fh), (x, y - h + fh)], line=G3, lw=1.5, jit=.8)
    if eagle:  # black double-headed eagle: body, two heads, spread wings
        ex, ey = x + fw * .5, y - h + fh * .5
        k = fh * .4
        c.poly([(ex - k * 1.1, ey - k * .5), (ex - k * .3, ey - k * .2), (ex - k * .25, ey - k * .9), (ex, ey - k * .6),
                (ex + k * .25, ey - k * .9), (ex + k * .3, ey - k * .2), (ex + k * 1.1, ey - k * .5), (ex + k * .6, ey + k * .3),
                (ex + k * .2, ey + k * .9), (ex - k * .2, ey + k * .9), (ex - k * .6, ey + k * .3)], fill=col(.05, .04, .04), jit=.2)


def fire(c, x, y, w, h, seed=0, opacity=1.0):
    rr = np.random.default_rng(seed)
    c.glow(x, y - h * .4, max(w, h) * 1.2, FIRE_O, .35 * opacity)
    for i, (cc, sc) in enumerate(((FIRE_R, 1.0), (FIRE_O, .75), (FIRE_Y, .45))):
        for k in range(4):
            bx = x + rr.uniform(-w * .4, w * .4) * sc
            hh = h * sc * rr.uniform(.6, 1.0)
            ww = w * .32 * sc
            c.poly([(bx - ww, y), (bx - ww * .5, y - hh * .5), (bx + rr.uniform(-ww, ww), y - hh),
                    (bx + ww * .5, y - hh * .45), (bx + ww, y)], fill=cc, line=FIRE_R if i == 0 else None, lw=2,
                   jit=1.5, opacity=opacity)


def smoke(c, pts, r0, r1, tone=G3, seed=0, opacity=.9):
    for i, (x, y) in enumerate(pts):
        r = r0 + (r1 - r0) * i / max(1, len(pts) - 1)
        b = blob(x, y, r, seed + i)
        c.poly(b, fill=tone, line=G4, lw=2, jit=1, opacity=opacity)
        c.poly(blob(x - r * .25, y - r * .3, r * .55, seed + i + 50), fill=tone * .6 + .4 * col(1, 1, 1), jit=1,
               opacity=opacity * .35)
        c.hatch(b, G4 if tone.mean() > .5 else col(.5, .48, .46), spacing=14, angle=-30, lw=2, opacity=.35)


def hatch_rect(c, x0, y0, x1, y1, tone, sp=12, ang=45, op=.9, lw=3):
    c.hatch([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], tone, spacing=sp, angle=ang, lw=lw, opacity=op)


def headline(img, country, place):
    d = ImageDraw.Draw(img)
    f1, f2 = font(150, anton=True), font(64, anton=True)
    d.text((70, 330), country, font=f1, fill=(255, 255, 255), stroke_width=6, stroke_fill=(30, 26, 26))
    d.text((74, 520), place, font=f2, fill=(255, 255, 255), stroke_width=3, stroke_fill=(30, 26, 26))


# ---------------------------------------------------------------- T1 Passeig de Gracia
def t1():
    c = Canvas(0)
    VX, VY, F, CH = 480, 575, 2200, 12.0

    def P(x, z, h=0.0):
        return VX + F * x / z, VY + F * (CH - h) / z
    # dusk sky
    c.vgrad(col(.55, .55, .66), .9, .5, 0, VY)
    c.vgrad(col(.95, .72, .55), 0, .7, 200, VY + 20)
    # road surface far (wet sheen)
    c.poly([P(-30, 60), P(30, 60), P(30, 400), P(-30, 400)], fill=G2, jit=0)
    # buildings both sides: blocks of facades
    for side in (-1, 1):
        for i, z0 in enumerate(np.arange(40, 420, 34)):
            z1 = z0 + 32
            ht = 24 + 5 * ((i * 7 + side) % 3)
            xx = side * 31
            a, b, cc, dd = P(xx, z0), P(xx, z1), P(xx, z1, ht), P(xx, z0, ht)
            tone = G3 if i % 2 else G2
            c.poly([a, b, cc, dd], fill=tone, line=G4, lw=2, jit=.8)
            # windows rows
            for fl in range(1, 7):
                hh = fl * 3.4
                if hh > ht - 2:
                    break
                for k in range(4):
                    zz = z0 + 3 + k * 7.5
                    p1, p2 = P(xx, zz, hh), P(xx, zz + 3, hh + 1.8)
                    lit = ((i + fl + k) % 5 == 0)
                    c.poly([p1, (p2[0], p1[1]), p2, (p1[0], p2[1])], fill=col(1, .85, .5) if lit else G4,
                           jit=0, opacity=.8)
        # corner tower with dome (Modernista) on the left near end of view
    tx = P(-31, 120, 34)
    c.poly(ell(tx[0], tx[1], 22, 26), fill=G3, line=G4, lw=2)
    # plane trees and lamps, rows at x = +-22
    for side in (-1, 1):
        for z in np.arange(100, 400, 16):
            bx, by = P(side * 22, z)
            tx_, ty_ = P(side * 22, z, 9)
            r = F * 3.2 / z
            c.line([(bx, by), (tx_, ty_)], G4, lw=max(1.5, F * .35 / z))
            c.poly(blob(tx_, ty_, r, int(z * 3 + side)), fill=col(.33, .36, .30), line=G4, lw=2, jit=.6, opacity=.9)
            lx, ly = P(side * 17, z + 7, 0)
            lx2, ly2 = P(side * 17, z + 7, 6)
            c.line([(lx, ly), (lx2, ly2)], G4, lw=max(1.2, F * .12 / z))
            c.glow(lx2, ly2, F * 1.6 / z, col(1, .88, .55), .55)
    # police line at the far end (z 260), front on, silhouetted
    for k in range(16):
        x = -21 + k * 2.8
        bx, by = P(x, 185)
        officer(c, bx, by, F * 1.9 / 185 * 3.4, tone=G4, helmet=G4, shield=col(.85, .88, .92))
    # crowd: far painted mass then near heads
    c.hatch([P(-30, 150), P(30, 150), P(30, 90), P(-30, 90)], G3, spacing=6, angle=80, lw=2, opacity=.6)
    # front of the crowd at z 230; knot + container just beyond at z 238
    cx_, cy_ = P(0.5, 151)
    fire(c, cx_, cy_, 70, 110, seed=4)
    c.poly([(cx_ - 50, cy_), (cx_ + 50, cy_), (cx_ + 44, cy_ - 40), (cx_ - 44, cy_ - 40)], fill=G4, line=G3, lw=3, jit=.3)
    for k, dx in enumerate((-5.0, -3.4, 3.0, 4.6, 6.0)):
        bx, by = P(dx, 149 + (k % 2) * 2)
        front_person(c, bx, by, F * 1.75 / 155 * 3.4, tone=col(.04, .04, .05), pose='throw' if k == 2 else 'stand')
    # fireworks bursts over the line
    for (bx, by, rr_) in ((380, 560, 80), (540, 530, 72), (690, 575, 60)):
        for a in np.linspace(0, 2 * math.pi, 14, endpoint=False):
            c.line([(bx + math.cos(a) * rr_ * .3, by + math.sin(a) * rr_ * .3),
                    (bx + math.cos(a) * rr_, by + math.sin(a) * rr_)], FIRE_Y, lw=4, jit=.3)
        c.glow(bx, by, rr_ * 1.6, col(1, .95, .7), .5)
    # firework string from the knot to the line
    c.line([(cx_ + 30, cy_ - 40), (470, 690), (400, 650)], col(1, .8, .4), lw=2, jit=1.2, opacity=.8)
    # crowd base: one dark mass filling the avenue from the camera to the front
    c.poly([P(-80, 19), P(80, 19), P(60, 146), P(-60, 146)], fill=col(.17, .15, .17), jit=0)
    c.vgrad(col(.40, .30, .28), 0, .0, 600, 1300)
    # near crowd: heads by depth
    heads = []
    for z in np.arange(20, 146, 0.7):
        n = int(1.3 * 0.7 * 2 * 480 * z / F) + 2
        for x in R.uniform(-480 * z / F - 1, 600 * z / F + 1, int(n * 1.15)):
            px, py = P(x, z, 1.65)
            if -20 < px < W + 20 and py < 1960:
                heads.append((z, px, py, x))
    heads.sort(key=lambda t: -t[0])
    flags = [((-6, 120), [CAT_Y, CAT_R, CAT_Y, CAT_R, CAT_Y]), ((5, 90), [CAT_R, CAT_R, col(.9, .9, .9)]),
             ((-3.0, 60), [CAT_Y, CAT_R, CAT_Y, CAT_R, CAT_Y]), ((4, 45), [CAT_R, CAT_R])]
    fi = 0
    band = []
    for i, (z, px, py, x) in enumerate(heads):
        band.append((z, px, py))
    # draw heads as dots per depth band (fast)
    for lo in np.arange(20, 150, 4):
        sel = np.array([(px, py) for (z, px, py) in band if lo <= z < lo + 4])
        if not len(sel):
            continue
        r = max(2.0, F * 0.12 / (lo + 2))
        dots(c, sel + [0, r * 1.7], r * 1.5, col(.08, .07, .08))  # shoulders
        dots(c, sel, r, col(.30, .26, .26) if lo < 70 else col(.38, .32, .31))
        dots(c, sel - [r * .2, r * .45], r * .45, col(.75, .60, .50), opacity=.5)  # dusk rim
        ks = sel[::5]
        up = np.stack([ks + [r * .9, r * .8], ks + [r * 2.0, -r * 4.0]], 1)
        c.strokes(up, col(.10, .09, .10), max(2, r * .7))
        dots(c, ks + [r * 2.1, -r * 4.6], max(2.4, r * .75), col(1, .93, .55))
        c.strokes(np.stack([ks + [r * 2.1, -r * 4.4], ks + [r * 2.5, -r * 3.6]], 1), col(1, .85, .4), max(1.5, r * .4))
    # wet sheen and tear-gas haze hint
    for fi, ((fx, fz), cols_) in enumerate(sorted(flags, key=lambda f: -f[0][1])):  # flags over the heads
        bx, by = P(fx, fz, 1.6)
        flag(c, bx, by, min(260, F * 4.5 / fz), cols_, wave=fi)
    for x in np.linspace(80, 1000, 9):  # wet street: lamp glints between the feet
        c.glow(x + R.uniform(-30, 30), 1700 + R.uniform(-150, 150), 60, col(1, .85, .55), .25)
    c.vgrad(col(.10, .09, .12), 0, .6, 1250, H)
    img = Image.fromarray(c.result())
    headline(img, 'SPAIN', 'Barcelona')
    return img


# ---------------------------------------------------------------- T2 Frankfurt
def t2():
    c = Canvas(1)
    c.fill_screen(col(.16, .16, .20), opacity=.9)
    # buildings across the street, dark; upper windows
    c.poly([(0, 0), (W, 0), (W, 1150), (0, 1150)], fill=col(.22, .22, .26), jit=0)
    for row in range(5):
        for k in range(5):
            x, y = 40 + k * 210, 80 + row * 135
            c.poly([(x, y), (x + 120, y), (x + 120, y + 90), (x, y + 90)], fill=G4,
                   line=col(.35, .35, .38), lw=3, jit=.6)
    hatch_rect(c, 0, 0, W, 760, G4, sp=14, ang=60, op=.5)
    # neighbour shopfronts, dim
    c.poly([(780, 820), (1080, 820), (1080, 1150), (780, 1150)], fill=col(.28, .28, .32), line=G4, lw=3)
    c.poly([(0, 820), (170, 820), (170, 1150), (0, 1150)], fill=col(.28, .28, .32), line=G4, lw=3)
    # the gun store: sign, shutter half up, lit window
    c.poly([(180, 700), (770, 700), (770, 760), (180, 760)], fill=G4, line=G3, lw=3)
    img_txt = ('WAFFEN', (380, 708))
    c.poly([(200, 760), (760, 760), (760, 1150), (200, 1150)], fill=col(1, .97, .86), line=G4, lw=4, jit=.5)
    c.glow(480, 950, 520, col(1, .95, .75), .45)
    for sy in (850, 950, 1050):  # white shelves with guns
        c.line([(220, sy), (740, sy)], G2, lw=4)
        for gx in range(240, 720, 70):
            c.line([(gx, sy - 18), (gx + 48, sy - 24)], G4, lw=5)
    # shutter: half raised (slats) over the top
    for i in range(9):
        c.poly([(200, 760 + i * 14), (760, 760 + i * 14), (760, 772 + i * 14), (200, 772 + i * 14)],
               fill=col(.55, .55, .58), line=G4, lw=2, jit=.3)
    c.line([(200, 888), (760, 888)], G4, lw=6)
    # tiled base below window
    hatch_rect(c, 200, 1110, 760, 1150, G4, sp=9, ang=0, op=.8)
    # broken glass: starred cracks and falling shards
    cx, cy = 430, 960
    for a in np.linspace(0, 2 * math.pi, 11, endpoint=False):
        c.line([(cx, cy), (cx + math.cos(a) * 160, cy + math.sin(a) * 120)], G3, lw=2, jit=2)
    for k in range(18):
        sx, sy = R.uniform(320, 560), R.uniform(980, 1170)
        c.poly([(sx, sy), (sx + 10, sy + 4), (sx + 3, sy + 16)], fill=col(.85, .93, 1), line=col(1, 1, 1), lw=1.5)
    # hooded group silhouetted against the window (feet on far pavement y 1160)
    group = [(250, 'stand'), (560, 'throw'), (650, 'stand'), (720, 'stand'), (120, 'run'), (40, 'run'), (870, 'run')]
    for x, pose in group:
        front_person(c, x, 1165, 250, tone=col(.07, .07, .08), pose=pose)
    # the swinger with the give-way sign: the one diagonal
    hx, hy = front_person(c, 440, 1170, 270, tone=col(.07, .07, .08), pose='swing')
    c.line([(hx - 10, hy + 40), (360, 900)], G2, lw=8)
    tri = [(360 - 60, 900 - 50), (360 + 45, 900 - 75), (360 - 5, 900 + 40)]
    c.glow(370, 920, 120, col(1, 1, .9), .7)
    for a in np.linspace(0, 2 * math.pi, 10, endpoint=False):  # impact flash
        c.line([(370 + math.cos(a) * 40, 920 + math.sin(a) * 40), (370 + math.cos(a) * 95, 920 + math.sin(a) * 95)],
               col(1, 1, .85), lw=4, jit=.3)
    c.poly(tri, fill=col(.95, .95, .95), line=CAT_R, lw=12, jit=.3)
    # shutter haulers at the left end
    for x in (650, 720):  # two haul the shutter with a pry bar
        c.line([(x - 20, 960), (x, 885)], G1, lw=6)
    # wet street with reflections
    c.poly([(0, 1150), (W, 1150), (W, 1320), (0, 1320)], fill=col(.24, .24, .29), jit=0)
    c.hatch([(150, 1165), (800, 1165), (800, 1300), (150, 1300)], col(1, .93, .7), spacing=9, angle=90, lw=3, opacity=.6)
    c.hatch([(820, 1165), (1080, 1165), (1080, 1300), (820, 1300)], BLUE_L, spacing=9, angle=90, lw=3, opacity=.6)
    c.line([(0, 1162), (W, 1162)], G2, lw=5)
    # blue wash from the right
    c.glow(1100, 1050, 800, BLUE, .75, power=1.2)
    for a in (-.35, -.15, .05):  # strobe beams from the far right end
        c.poly([(1080, 1000), (1080, 1040), (1080 - 900 * math.cos(a), 1020 + 900 * math.sin(a) + 60),
                (1080 - 900 * math.cos(a), 1020 + 900 * math.sin(a) - 60)], fill=BLUE_L, opacity=.18, jit=0)
    c.glow(1100, 1200, 300, BLUE_L, .6)
    # near crowd from behind, signs and phones up toward the window
    for row, (y, h, n) in enumerate(((1760, 420, 7), (2000, 560, 6), (2350, 760, 5))):
        for k in range(n):
            x = 40 + k * (W - 80) / (n - 1) + R.uniform(-30, 30)
            back_person(c, x, y, h, tone=col(.10, .10, .12), arm=(2 if (k + row) % 3 == 0 else 0), seed=k + row)
    for (x, y, w_, h_, txt) in ((110, 1330, 300, 100, 'GEN Z REGELT'), (680, 1360, 200, 100, 'NEIN!')):
        c.line([(x + w_ / 2, y + h_), (x + w_ / 2, y + h_ + 160)], G2, lw=6)
        c.poly([(x, y), (x + w_, y), (x + w_, y + h_), (x, y + h_)], fill=col(.92, .90, .84), line=G4, lw=3)
    img = Image.fromarray(c.result())
    d = ImageDraw.Draw(img)
    d.text(img_txt[1], img_txt[0], font=font(44, bold=True), fill=(230, 225, 210))
    d.text((128, 1362), 'GEN Z REGELT', font=font(34, bold=True), fill=(30, 30, 30))
    d.text((715, 1385), 'NEIN!', font=font(40, bold=True), fill=(30, 30, 30))
    headline(img, 'GERMANY', 'Frankfurt')
    return img


# ---------------------------------------------------------------- T3 Republique
def t3():
    c = Canvas(2)
    c.vgrad(col(.70, .80, .92), .8, .3, 0, 1150)
    # Haussmann fronts low on the horizon, both sides
    for x0, x1, top in ((0, 330, 870), (630, 1080, 880)):
        c.poly([(x0, 1150), (x0, top), (x1, top + 10), (x1, 1150)], fill=col(.80, .76, .68), line=G3, lw=3)
        c.poly([(x0, top), (x0 + 10, top - 45), (x1 - 10, top - 35), (x1, top + 10)], fill=G2, line=G3, lw=3)
        for k in range(int((x1 - x0) / 46)):
            for f in range(3):
                x, y = x0 + 14 + k * 46, top + 30 + f * 60
                c.poly([(x, y), (x + 18, y), (x + 18, y + 34), (x, y + 34)], fill=G3, jit=.3)
    # trees
    for x in (60, 230, 700, 900, 1040):
        c.poly(blob(x, 930, 80, x), fill=col(.38, .46, .34), line=G4, lw=2, opacity=.9)
    # black smoke from the car (bottom-left) climbing behind Marianne
    smoke(c, [(170, 1180), (190, 1040), (230, 900), (300, 760), (390, 640), (500, 560), (620, 520), (760, 480)], 60, 140,
          tone=col(.18, .17, .17), seed=10)
    # Marianne monument: steps, drum, statue
    c.poly([(220, 1150), (740, 1150), (720, 1120), (240, 1120)], fill=col(.80, .78, .73), line=G3, lw=3)
    c.poly([(260, 1120), (700, 1120), (680, 1085), (280, 1085)], fill=col(.86, .84, .79), line=G3, lw=3)
    c.poly([(300, 1085), (660, 1085), (650, 990), (310, 990)], fill=col(.55, .48, .38), line=G3, lw=3)  # bronze reliefs
    hatch_rect(c, 310, 1000, 650, 1080, G3, sp=18, ang=90, op=.5)
    c.poly([(370, 990), (590, 990), (565, 790), (395, 790)], fill=col(.90, .88, .82), line=G3, lw=3)
    for (x, y) in ((345, 940), (615, 940), (480, 960)):  # seated figures
        c.poly(blob(x, y, 40, int(x)), fill=col(.82, .80, .74), line=G3, lw=2)
    c.poly([(380, 790), (580, 790), (560, 760), (400, 760)], fill=col(.86, .84, .78), line=G3, lw=3)
    BR = col(.28, .24, .20)
    c.poly([(445, 760), (520, 760), (530, 620), (505, 575), (465, 575), (440, 640)], fill=BR, line=G4, lw=3)
    c.poly(ell(485, 555, 20, 24), fill=BR, line=G4, lw=3)
    c.line([(505, 590), (540, 480)], BR, lw=10)  # olive branch arm raised
    for k in range(5):
        c.line([(540, 480), (530 + k * 9, 455 - (k % 2) * 12)], col(.30, .36, .24), lw=4)  # the branch's leaves
    c.poly([(440, 650), (470, 640), (470, 700), (440, 705)], fill=col(.70, .68, .60), line=G4, lw=2)  # tablet
    # graffiti on base
    c.line([(380, 1000), (420, 980), (440, 1010), (480, 975)], CAT_R, lw=5, jit=2)
    # white tear gas swallowing the base
    smoke(c, [(400, 1080), (480, 1060), (560, 1080), (450, 1010), (530, 1000), (490, 950)], 70, 60,
          tone=col(.97, .97, .96), seed=40, opacity=.85)
    # crowd mass behind, banners at the back (CGT), tricolours
    c.hatch([(0, 1080), (W, 1080), (W, 1180), (0, 1180)], G4, spacing=5, angle=90, lw=3, opacity=.8)
    for x in (40, 690, 880):
        c.poly([(x, 1050), (x + 160, 1050), (x + 160, 1090), (x, 1090)], fill=col(.88, .18, .15), line=G4, lw=2)
    for x in (120, 760, 990):
        flag(c, x, 1150, 200, [col(.15, .25, .65), col(.95, .95, .95), col(.85, .15, .15)], wave=x, vertical=True)
    # ground (open paving)
    c.poly([(0, 1180), (W, 1180), (W, H), (0, H)], fill=col(.62, .60, .57), jit=0)
    hatch_rect(c, 0, 1180, W, H, G2, sp=40, ang=8, op=.4)
    # black front line, left of centre, facing right; throwers
    for k, x in enumerate((90, 170, 250, 330, 410, 470)):
        pose = 'throw' if k % 2 else 'stand'
        front_person(c, x, 1260 - (k % 2) * 20, 330 - (k % 3) * 20, tone=col(.07, .07, .08), pose=pose)
    # stones arcs left to right
    for (x0, y0, x1, y1) in ((330, 960, 820, 1010), (420, 940, 900, 980), (250, 990, 760, 1060)):
        mx, my = (x0 + x1) / 2, min(y0, y1) - 120
        pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1)
               for t in np.linspace(0, .8, 10)]
        c.line(pts, G2, lw=2, jit=.5, opacity=.5)
        for q in pts[3::2]:
            c.poly(blob(*q, 11, int(q[0])), fill=G3, line=G4, lw=2)
    # police two rows at the right edge, shields cut by the frame
    for k, (x, y) in enumerate(((900, 1200), (960, 1200), (1020, 1200), (1080, 1200), (930, 1270), (995, 1270), (1060, 1270))):
        officer(c, x, y, 260 if y < 1250 else 300, tone=col(.10, .11, .14), helmet=col(.12, .14, .20), face_left=True)
    # burning bikes in the gap, kiosk mid-right
    fire(c, 690, 1215, 150, 150, seed=7)
    for k in range(6):  # heap of rental bikes: two wheels and a frame each, tumbled
        x, y, a = 600 + k * 34, 1225 - (k % 3) * 22, (k * 37) % 60 - 30
        cc = LIME if k % 2 else col(.95, .55, .15)
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        w1, w2 = (x - 26 * ca, y - 26 * sa), (x + 26 * ca, y + 26 * sa)
        for (wx, wy) in (w1, w2):
            c.poly(ell(wx, wy, 18, 18), line=G4, lw=4)
        c.line([w1, (x, y - 18), w2], cc, lw=5)
        c.line([(x, y - 18), (x + 6, y - 30)], cc, lw=4)
    c.poly([(760, 1180), (860, 1180), (860, 1080), (810, 1050), (760, 1080)], fill=col(.25, .35, .30), line=G4, lw=3)
    fire(c, 810, 1080, 70, 90, seed=9, opacity=.9)
    # water cannon jet from the right edge (white diagonal)
    c.poly([(1080, 1040), (1080, 1090), (620, 1240), (600, 1225)], fill=col(.96, .98, 1.0), line=G1, lw=2, opacity=.85)
    # burning car foreground-left
    # (side-on estate car, burnt-out: low body, roof, empty window holes, wheel arches)
    c.poly([(-60, 1530), (-60, 1420), (40, 1400), (110, 1320), (360, 1320), (430, 1400), (520, 1420), (540, 1530)],
           fill=col(.30, .28, .27), line=G4, lw=5)
    for wx0, wx1 in ((130, 230), (245, 345)):
        c.poly([(wx0, 1335), (wx1, 1335), (wx1 + 15, 1395), (wx0 - 15, 1395)], fill=col(.95, .55, .15), line=G4, lw=3)
    c.line([(-60, 1450), (540, 1450)], G4, lw=3)
    for wx in (60, 420):
        c.poly(ell(wx, 1530, 58, 58), fill=G4, line=G3, lw=4)
        c.poly(ell(wx, 1530, 22, 22), fill=G2, jit=.2)
    fire(c, 250, 1340, 280, 230, seed=11)
    for k in range(9):  # paving stones on the ground
        c.poly(blob(R.uniform(560, 1000), R.uniform(1300, 1480), R.uniform(8, 15), k), fill=G3, line=G4, lw=2)
    c.vgrad(col(.12, .11, .12), 0, .75, 1380, H)
    img = Image.fromarray(c.result())
    headline(img, 'FRANCE', 'Paris')
    return img


# ---------------------------------------------------------------- T4 Tirana
def t4():
    c = Canvas(3)
    c.vgrad(col(.35, .10, .08), .9, .2, 0, 980)
    c.vgrad(FIRE_O, 0, .8, 200, 980)
    hatch_rect(c, 0, 0, W, 960, FIRE_R, sp=22, ang=20, op=.35)
    smoke(c, [(150, 300), (330, 230), (540, 260), (900, 230), (1000, 380)], 120, 160, tone=col(.20, .12, .10), seed=60, opacity=.6)
    VX, VY = 470, 960
    # pastel blocks and pines down the avenue
    for side in (-1, 1):
        for k in range(6):
            x0 = VX + side * (60 + k * 50)
            h = 80 + k * 30
            c.poly([(x0, VY), (x0 + side * 46, VY), (x0 + side * 46, VY - h), (x0, VY - h)], fill=col(.45, .35, .40),
                   line=G4, lw=2, opacity=.8)
    # bank, left edge (columns, ground floor windows)
    c.poly([(0, 1180), (0, 560), (190, 620), (190, 1120)], fill=col(.55, .50, .46), line=G4, lw=4)
    for y in (680, 800, 920):
        for x in (30, 110):
            c.poly([(x, y), (x + 50, y + 8), (x + 50, y + 80), (x, y + 72)], fill=G4, jit=.4)
    for x in (20, 80, 140):
        c.poly([(x, 1030), (x + 40, 1030), (x + 40, 1120), (x, 1110)], fill=FIRE_Y, line=G4, lw=2)
    fire(c, 90, 1100, 140, 120, seed=21)
    # fireball rising behind the ministry
    c.glow(840, 600, 380, FIRE_Y, .6)
    c.poly(blob(840, 600, 190, 77), fill=FIRE_O, line=FIRE_R, lw=4, opacity=.9)
    c.poly(blob(840, 620, 100, 78), fill=FIRE_Y, opacity=.9)
    # Education Ministry, centre-right: ochre, rounded corner bay, grey balconies, ablaze
    c.poly([(540, 1050), (540, 720), (720, 700), (720, 1050)], fill=col(.80, .64, .28), line=G4, lw=4)
    c.poly([(720, 1050), (720, 690), (1080, 660), (1080, 1050)], fill=OCHRE, line=G4, lw=4)
    bay = [(650 + 75 * math.cos(a), 0) for a in np.linspace(math.pi, 0, 9)]
    c.poly([(x, 1050) for x, _ in bay] + [(x, 640 - 20 * math.sin(a)) for (x, _), a in zip(bay[::-1], np.linspace(0, math.pi, 9))],
           fill=col(.92, .76, .38), line=G4, lw=4)  # the rounded corner bay
    for xx in (600, 650, 700):
        c.line([(xx, 650), (xx, 1050)], col(.62, .50, .22), lw=2)
    c.poly(ell(650, 625, 80, 16), fill=G2, line=G4, lw=3)  # cornice cap
    for y in (740, 840, 940):  # stacked grey balconies on the bay; windows on the wings
        c.poly([(570, y + 30), (730, y + 30), (725, y + 48), (575, y + 48)], fill=col(.75, .76, .78), line=G4, lw=2)
        c.poly([(615, y - 25), (685, y - 25), (685, y + 28), (615, y + 28)], fill=G4, jit=.3)
        for x in range(760, 1060, 60):
            c.poly([(x, y - 20), (x + 30, y - 20), (x + 30, y + 30), (x, y + 30)], fill=G4, jit=.4)
    flag(c, 650, 615, 120, [CAT_R], wave=1, eagle=True)
    fire(c, 860, 680, 300, 260, seed=31)
    fire(c, 640, 700, 120, 140, seed=32)
    # helicopter upper right, hit
    hx, hy = 770, 420
    c.poly(ell(hx, hy, 115, 55, rot=-15), fill=col(.15, .17, .22), line=G4, lw=4)  # body
    c.poly(ell(hx - 55, hy - 10, 38, 30, rot=-15), fill=col(.55, .65, .75), line=G4, lw=3)  # cockpit glass
    c.line([(hx + 95, hy - 30), (hx + 260, hy - 85)], col(.15, .17, .22), lw=16)  # tail boom
    c.line([(hx + 250, hy - 120), (hx + 265, hy - 50)], G4, lw=8)  # tail rotor
    c.line([(hx - 200, hy - 110), (hx + 200, hy - 40)], G3, lw=6)  # main rotor
    c.line([(hx - 40, hy + 55), (hx + 60, hy + 30)], G4, lw=5)  # skid
    fire(c, hx + 90, hy + 15, 70, 90, seed=41)
    # rocket trail: bottom-left to the helicopter
    trail = [(240, 1175), (350, 980), (460, 790), (580, 620), (700, 480)]
    for i, (x, y) in enumerate(trail):
        c.poly(blob(x, y, 22 + i * 6, 90 + i), fill=col(.85, .82, .78), line=G2, lw=2, opacity=.85)
    for i in range(len(trail) - 1):  # extra puffs between, so it reads as smoke, not a beam
        (x0, y0), (x1, y1) = trail[i], trail[i + 1]
        c.poly(blob((x0 + x1) / 2 + 12, (y0 + y1) / 2, 18 + i * 6, 120 + i), fill=col(.78, .75, .72), line=G2, lw=2, opacity=.85)
    c.line(trail[-2:], col(1, .95, .7), lw=4)
    # road and toppled water-cannon truck burning at the line's end
    c.poly([(0, 1180), (W, 1080), (W, H), (0, H)], fill=col(.20, .16, .16), jit=0)
    # toppled water-cannon truck on its side: underside to us, wheels up, cannon turret sideways
    c.poly([(820, 1270), (820, 1150), (1100, 1120), (1100, 1250)], fill=col(.32, .34, .32), line=G4, lw=4)
    c.poly([(1000, 1124), (1100, 1114), (1100, 1080), (1010, 1088)], fill=col(.25, .27, .25), line=G4, lw=3)  # cab
    for wx in (860, 940, 1050):
        c.poly(ell(wx, 1140, 34, 16), fill=G4, line=G3, lw=3)
    c.line([(830, 1240), (770, 1255)], G4, lw=10)  # cannon barrel
    fire(c, 960, 1200, 180, 170, seed=51)
    # crowd mass left and behind
    c.hatch([(0, 1000), (600, 1000), (640, 1180), (0, 1220)], col(.06, .05, .06), spacing=5, angle=90, lw=4, opacity=.95)
    for x in range(20, 560, 38):
        back_person(c, x + R.uniform(-8, 8), 1230 + R.uniform(-10, 10), 150, tone=col(.06, .05, .06), arm=(1 if x % 3 == 0 else 0), seed=x)
    flag(c, 470, 1190, 240, [CAT_R], wave=2, eagle=True)
    # shield line mid-right facing left, white helmets, breaking at centre
    for k in range(7):
        x = 600 + k * 50
        officer(c, x, 1270 - k * 6, 200, tone=col(.08, .08, .10), helmet=col(.95, .95, .95), face_left=True)
    # melee at centre: rioters swarming over shields
    for x, pose in ((470, 'swing'), (540, 'run'), (420, 'stand'), (600, 'throw')):
        front_person(c, x, 1300, 220, tone=col(.04, .04, .05), pose=pose)
    # Molotovs arcing into the bank
    for (x0, y0, x1) in ((380, 1120, 70), (300, 1100, 140)):
        pts = [(x0 + (x1 - x0) * t, y0 - 30 * t - math.sin(t * math.pi) * 260) for t in np.linspace(0, .8, 12)]
        c.line(pts, FIRE_O, lw=4, jit=.5, opacity=.7)
        bx, by = pts[-1]
        c.poly([(bx - 8, by - 18), (bx + 8, by - 18), (bx + 10, by + 14), (bx - 10, by + 14)], fill=col(.45, .60, .40),
               line=G4, lw=2)  # the bottle
        fire(c, bx, by - 16, 26, 44, seed=int(x0))
    # mopeds bottom-left, two masked riders, launcher
    for (mx, my, s) in ((170, 1460, 1.6), (420, 1500, 1.3)):
        for wx in (mx - 70 * s, mx + 75 * s):  # small scooter wheels
            c.poly(ell(wx, my, 26 * s, 26 * s), fill=G4, line=G2, lw=4)
            c.poly(ell(wx, my, 9 * s, 9 * s), fill=G2, jit=.2)
        c.poly([(mx - 100 * s, my - 20 * s), (mx - 90 * s, my - 60 * s), (mx + 20 * s, my - 62 * s), (mx + 40 * s, my - 20 * s)],
               fill=col(.55, .12, .10), line=G4, lw=3)  # rounded rear body
        c.poly([(mx + 40 * s, my - 15 * s), (mx + 70 * s, my - 20 * s), (mx + 95 * s, my - 120 * s), (mx + 75 * s, my - 125 * s)],
               fill=col(.55, .12, .10), line=G4, lw=3)  # front leg shield up to the handlebar
        c.line([(mx + 70 * s, my - 125 * s), (mx + 110 * s, my - 140 * s)], G4, lw=6)  # handlebar
        c.line([(mx + 80 * s, my - 10 * s), (mx + 75 * s, my)], G4, lw=5)
        front_person(c, mx - 10 * s, my - 50 * s, 150 * s, tone=col(.05, .05, .06), pose='stand')
        front_person(c, mx - 50 * s, my - 60 * s, 150 * s, tone=col(.05, .05, .06), pose='stand')
    c.line([(40, 1300), (230, 1180)], col(.35, .38, .30), lw=18)  # RPG on the passenger's shoulder
    c.poly(ell(232, 1178, 16, 12, rot=-30), fill=col(.35, .38, .30), line=G4, lw=2)
    c.glow(240, 1175, 80, FIRE_Y, .9)
    c.vgrad(col(.06, .05, .05), 0, .75, 1450, H)
    img = Image.fromarray(c.result())
    headline(img, 'ALBANIA', 'Tirana')
    return img


# ---------------------------------------------------------------- overlays and sheet
def dashed(d, p0, p1, fill, w=4, dash=22):
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    n = int(L // dash)
    for i in range(0, n, 2):
        a, b = i / n, min(1, (i + 1) / n)
        d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)], fill=fill, width=w)


def arrow(d, pts, fill, w=7):
    d.line(pts, fill=fill, width=w, joint='curve')
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    a = math.atan2(y1 - y0, x1 - x0)
    for s in (-1, 1):
        d.line([(x1, y1), (x1 - 34 * math.cos(a + s * .5), y1 - 34 * math.sin(a + s * .5))], fill=fill, width=w)


SCENES = {
    't1': dict(eye=560, focus=[(487, 740, '0-1.5 knot by the fire'), (520, 610, '1.5-3 bursts'), (300, 700, '3-4 line steps')],
               moves=[[(480, 1150), (480, 900), (480, 800)], [(560, 740), (500, 640)]], hook=True,
               note='T1 Barcelona, dusk, wet. High camera behind the march: one river of heads and keys to the police line.'),
    't2': dict(eye=1000, focus=[(330, 800, '0-1.5 the sign swing'), (430, 980, '1.5-3 the glass'), (900, 1050, '3-4 blue sweeps in')],
               moves=[[(40, 1080), (300, 1100)], [(1060, 900), (700, 960)]],
               note='T2 Frankfurt, night. Phone-height camera in the crowd; the lit window is the brightest thing.'),
    't3': dict(eye=1150, focus=[(300, 1080, '0-1 surge'), (480, 1030, '1-2.5 gas at Marianne'), (800, 1120, '2.5-4 water jet')],
               moves=[[(150, 1000), (420, 1000)], [(1000, 1060), (650, 1220)], [(500, 1350), (120, 1400)]],
               note='T3 Paris, day. Low camera: Marianne above the black smoke; stones cross left to right.'),
    't4': dict(eye=960, focus=[(200, 1300, '0-1 moped and shot'), (770, 440, '1-1.6 helicopter hit'), (520, 1130, '1.6-4 melee')],
               moves=[[(240, 1175), (460, 790), (690, 500)], [(80, 1150), (420, 1180)]],
               note='T4 Tirana, dusk. The rocket trail uses the whole height; fireball backlights the melee.'),
}


def overlay(img, key):
    s = SCENES[key]
    im = img.convert('RGB').copy()
    d = ImageDraw.Draw(im)
    dashed(d, (60, 310), (900, 310), (255, 255, 255), 3)
    dashed(d, (900, 310), (900, 1500), (255, 255, 255), 3)
    dashed(d, (900, 1500), (60, 1500), (255, 255, 255), 3)
    dashed(d, (60, 1500), (60, 310), (255, 255, 255), 3)
    dashed(d, (0, s['eye']), (W, s['eye']), (250, 210, 40), 6, 30)
    d.text((W - 140, s['eye'] - 44), 'EYE', font=font(34, True), fill=(250, 210, 40), stroke_width=3, stroke_fill=(0, 0, 0))
    for m in s['moves']:
        arrow(d, m, (70, 200, 90))
    for i, (x, y, lab) in enumerate(s['focus']):
        d.ellipse((x - 70, y - 70, x + 70, y + 70), outline=(230, 40, 40), width=7)
        d.text((x - 12, y - 22), str(i + 1), font=font(40, True), fill=(230, 40, 40), stroke_width=3, stroke_fill=(255, 255, 255))
    if s.get('hook'):
        d.rounded_rectangle((140, 1250, 900, 1360), 18, fill=(255, 255, 255))
        d.text((175, 1272), 'European protests, ranked', font=font(50, True), fill=(0, 0, 0))
    return im


def sheet(frames, out):
    pw, ph = 540, 960
    cap = 150
    S = Image.new('RGB', (2 * pw + 60, 2 * (ph + cap) + 110), (246, 243, 236))
    d = ImageDraw.Draw(S)
    d.text((20, 18), 'PROTEST TIERS: pencil sketches of the four scenes (9:16)', font=font(30, True), fill=(20, 20, 20))
    d.text((20, 60), 'white dashes = safe area   yellow = eye level   red rings = focus, by beat   green = movement',
           font=font(19), fill=(60, 60, 60))
    for i, key in enumerate(('t1', 't2', 't3', 't4')):
        im = overlay(frames[key], key).resize((pw, ph), Image.LANCZOS)
        x, y = 20 + (i % 2) * (pw + 20), 100 + (i // 2) * (ph + cap)
        S.paste(im, (x, y))
        words = SCENES[key]['note'].split()
        lines, cur = [], ''
        for w_ in words:
            if len(cur) + len(w_) > 48:
                lines.append(cur)
                cur = w_
            else:
                cur = (cur + ' ' + w_).strip()
        lines.append(cur)
        for j, ln in enumerate(lines):
            d.text((x, y + ph + 8 + j * 26), ln, font=font(21, j == 0 and False), fill=(30, 30, 30))
        focus = '  '.join('%d %s' % (k + 1, f[2]) for k, f in enumerate(SCENES[key]['focus']))
        d.text((x, y + ph + 8 + len(lines) * 26 + 4), focus[:60], font=font(17), fill=(170, 30, 30))
        if len(focus) > 60:
            d.text((x, y + ph + 8 + len(lines) * 26 + 26), focus[60:120], font=font(17), fill=(170, 30, 30))
    S.save(out, quality=88)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    only = sys.argv[2:] or ['t1', 't2', 't3', 't4']
    frames = {}
    for k in ('t1', 't2', 't3', 't4'):
        p = os.path.join(out, k + '.png')
        if k in only or not os.path.exists(p):
            frames[k] = globals()[k]()
            frames[k].save(p)
        else:
            frames[k] = Image.open(p)
    sheet(frames, os.path.join(out, 'sheet.jpg'))
    print('ok')
