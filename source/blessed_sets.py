#!/usr/bin/env python3
"""Blessed (Sam, 11 Nov): the sets. Flat paintings in the house style (flat colour, one ink outline, hand-cut
edges), one painting per camera (rule 39), real metres through a level camera (`Level`), drawn fresh from the
references in references/blessed/ (never traced). The cast draw on top through the same B.Cam (world = 1080 x 1920
px at zoom 1), so a push-in is a zoomed camera on the same painting.

MAP (rule 61)
  helpers ........... 40   Level, wob, quad, blob, clump (from remakes_sets), sign (lettering), bricks, window
  court outside ..... 120  court_out: Southwark Crown Court (ref 00): buff brick, the dark sign band, steps, beds
  courtroom ......... 250  court_box (refs 05, 07: witness box, judge behind), court_bench (the gavel close-up),
                           court_dock (refs 08, 11: the glass dock), _arms (the royal arms over the bench)
  van ............... 400  van: the cubicle (no photo found: Sam's list), street lights sliding past its window
  prison ............ 450  cell (refs 12-14: bed, window, toilet, blue door open to the landing), cell_cot (a
                           camera on the same painting), phone (the landing wall phone under its hood, netting)
  TV room ........... 590  tvroom (Brand among the others, the TV off-screen above the lens), tv (the set on its
                           bracket, the studio in it), tv_flicker (the light on everyone, over the cast)
  studio ............ 660  studio_feed(t, draw_reader): newsdesk_set restyled red (BBC News look, Sam's answer 5)
  gates ............. 720  gates: a Victorian prison gatehouse (refs 18-20), the wicket door he steps out of
  stage ............. 800  STAGE: per view, where each person stands (screen x, ground y, pixels per metre)
  checks ............ 830  SET_BOXES / SET_MEANT (rule 83), BENCHMARK (rule 3)
  sheets ............ 930  painting(view, t), picture(view), alone(OUT) every view at phone size with the cast

    python3 source/blessed_sets.py alone OUT.jpg [--bare]
    python3 source/blessed_sets.py one VIEW OUT.jpg [--bare]
    python3 source/benchmark.py blessed_sets OUT.jpg
    python3 source/setcheck.py blessed_sets
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
from ed import INK               # noqa: E402
from remakes_sets import Level, blob, wob, quad, clump, mix, dk, foot_shadow   # noqa: E402,F401

NAME = 'blessed'
W, H = 1080, 1920
SANS = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
_GLYPHS = {}


# ================================================================================================ helpers
def s_for(ppm, height=1.75):
    """The cast's scale s for someone `height` m tall where one metre is ppm pixels (views.person: neck to soles
    928 units, head top about 247 above the neck)."""
    return ppm * height / 1175.0


def sign(img, cam, text, cx, cy, width, colr, font=SANS):
    """Lettering drawn once large, then scaled to an exact width (it never pulses or spills: satire.md)."""
    key = (text, colr, font)
    if key not in _GLYPHS:
        f = ImageFont.truetype(font, 200)
        l, t, r, b = f.getbbox(text)
        lay = Image.new('RGBA', (r - l + 16, b - t + 16), colr + (0,))
        ImageDraw.Draw(lay).text((8 - l, 8 - t), text, font=f, fill=colr + (255,))
        _GLYPHS[key] = lay
    src = _GLYPHS[key]
    w = cam.S(width)
    if w < 3:
        return
    k = w / src.width
    im = src.resize((max(1, int(round(w))), max(1, int(round(src.height * k)))), Image.LANCZOS)
    X, Y = cam.P(cx, cy)
    img.alpha_composite(im, (int(round(X - im.width / 2)), int(round(Y - im.height / 2))))


def P(L, x, d, z):
    return L.p(x, d, z)


def face(L, x0, x1, d, z0, z1):
    """A flat upright rectangle facing the lens at depth d (a wall, a door, a sign), in screen px."""
    (a, b), (c, e) = L.p(x0, d, z1), L.p(x1, d, z0)
    return quad(a, b, c, e)


def bricks(p, box, base, seed, cw=34, ch=13, n=40, lw=1.0):
    """Brick texture without a ruled grid: scattered patches of a few bricks, each a touch lighter or darker, with
    their mortar lines, so the wall reads as brick at phone size and never as wallpaper (S5)."""
    x0, y0, x1, y1 = box
    r = random.Random(seed)
    for _ in range(n):
        x, y = r.uniform(x0, x1 - cw * 3), r.uniform(y0, y1 - ch * 3)
        y = y0 + round((y - y0) / ch) * ch
        rows = r.randint(1, 3)
        for k in range(rows):
            off = (cw / 2) * (k % 2)
            for j in range(r.randint(1, 3)):
                bx, by = x + off + j * cw, y + k * ch
                if bx + cw > x1 or by + ch > y1:
                    continue
                col = dk(base, r.uniform(0.86, 0.95)) if r.random() < 0.6 else mix(base, (250, 236, 210), 0.12)
                p.poly(quad(bx, by, bx + cw - 2, by + ch - 2), col, dk(base, 0.72), lw)


def window(p, box, frame, glass, seed, bars=2, blind=None, lw=2.2):
    """A window: the frame, the glass, glazing bars, a blind part-way down (some of them), a sill."""
    x0, y0, x1, y1 = box
    p.poly(wob(quad(x0, y0, x1, y1), 1.2, seed), frame, INK, lw)
    m = max(2.0, (x1 - x0) * 0.08)
    p.poly(quad(x0 + m, y0 + m, x1 - m, y1 - m), glass, None)
    if blind:
        p.poly(quad(x0 + m, y0 + m, x1 - m, y0 + m + (y1 - y0 - 2 * m) * blind[1]), blind[0], None)
    for k in range(1, bars):
        x = x0 + (x1 - x0) * k / bars
        p.line([(x, y0 + m), (x, y1 - m)], frame, max(1.5, m * 0.6))
    p.line([(x0 + m * 1.4, y0 + m * 1.6), (x0 + (x1 - x0) * 0.35, y0 + m * 1.6)], mix(glass, (255, 255, 255), 0.5), 1.4)
    p.poly(quad(x0 - m * 0.6, y1, x1 + m * 0.6, y1 + m * 0.9), mix(frame, (200, 196, 190), 0.5), INK, lw * 0.7)


def soft(img, cam, box, col, a, blur):
    """A soft light or shade wash over a world box (the TV's glow, a window's light): no outline."""
    lay = Image.new('RGBA', img.size, col + (0,))
    x0, y0 = cam.P(box[0], box[1])
    x1, y1 = cam.P(box[2], box[3])
    ImageDraw.Draw(lay).ellipse([x0, y0, x1, y1], fill=col + (int(255 * a),))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(cam.S(blur))))


# ================================================================================================ the court outside
# Southwark Crown Court (ref 00): a long low block in buff-orange brick, ribbon windows in dark frames, the entrance
# set in under a dark sign band 'CROWN COURT SOUTHWARK', brick piers, a raised forecourt behind low brick walls and
# planted beds, steps with rails on the left, a tall lamp post, trees at both ends. The camera stands on the
# pavement 2.4 m up (over the press pack's heads), looking at the doors.
OUT = Level(2.4, 820.0, 1500.0)
BRICK = (178, 116, 82)
BRICK_D = (148, 92, 64)
FRAME = (62, 52, 46)
GLASS = (172, 186, 192)
BLIND = (226, 204, 140)
PAVE = (178, 176, 170)
PAVE_D = (156, 154, 148)
PLANT = (86, 120, 66)
PLANT_D = (64, 92, 52)
AUTUMN = (170, 160, 72)
SKY = (214, 222, 228)
FACADE_D = 17.0
PLAZA_D0, PLAZA_Z = 11.0, 0.7


def court_out(img, cam, t=0.0):
    p = B.Pen(img, cam)
    L = OUT
    p.poly(quad(-300, -800, W + 300, 1200), SKY, None)
    for k, (x, y, rx) in enumerate(((180, 60, 220), (760, 10, 260))):                       # flat clouds
        p.poly(blob(x, y, rx, 70, 10, 0.12, 30 + k), (232, 236, 240), None)
    # the facade: four floors, 3.6 m each, from the forecourt (z PLAZA_Z) up
    d, z0 = FACADE_D, PLAZA_Z
    top = z0 + 4 * 3.6 + 0.6
    p.poly(face(L, -14, 14, d, z0, top), BRICK, INK, 3.0)
    x0, y0 = L.p(-14, d, top)
    x1, y1 = L.p(14, d, z0)
    bricks(p, (x0, y0, x1, y1), BRICK, 7, cw=10, ch=4, n=220, lw=0.6)
    p.poly(face(L, -14, 14, d, top - 0.35, top), BRICK_D, INK, 2.4)                         # the parapet
    for fl in range(1, 4):                                                                 # ribbon windows
        zb = z0 + fl * 3.6 + 0.9
        for i, xc in enumerate(np.arange(-12.6, 13.0, 2.55)):
            if abs(xc - 1.4) < 1.2 and fl == 1:
                continue
            bl = (BLIND, [0.2, 0.55, 0.35][(i + fl) % 3]) if (i * 7 + fl * 3) % 5 < 2 else None
            a = L.p(xc - 0.95, d, zb + 1.9)
            b = L.p(xc + 0.95, d, zb)
            window(p, (a[0], a[1], b[0], b[1]), FRAME, GLASS, 100 + i + 20 * fl, bars=2, blind=bl, lw=1.8)
    # the ground floor: brick piers between dark glazing, the entrance recess and its sign band
    for i, xc in enumerate(np.arange(-12.6, 13.0, 2.55)):
        if -1.4 < xc < 4.4:
            continue
        a, b = L.p(xc - 0.95, d, z0 + 2.9), L.p(xc + 0.95, d, z0 + 0.5)
        window(p, (a[0], a[1], b[0], b[1]), FRAME, mix(GLASS, (60, 70, 80), 0.45), 300 + i, bars=1, lw=1.8)
    p.poly(face(L, -1.4, 4.4, d - 0.01, z0, z0 + 3.0), (52, 56, 62), INK, 2.4)              # the recess, dark
    for k, xc in enumerate((-0.6, 0.9, 2.4)):                                              # glass doors
        p.poly(face(L, xc - 0.65, xc + 0.65, d - 0.02, z0, z0 + 2.4), (104, 120, 128), INK, 2.0)
        a, b = L.p(xc, d - 0.02, z0 + 2.4), L.p(xc, d - 0.02, z0)
        p.line([a, b], INK, 2.0)
        for sgn in (-1, 1):
            h0, h1 = L.p(xc + sgn * 0.12, d - 0.02, z0 + 1.3), L.p(xc + sgn * 0.12, d - 0.02, z0 + 0.9)
            p.line([h0, h1], (200, 200, 204), 2.6)
    for xc in (-1.7, 4.7):                                                                 # brick piers
        p.poly(face(L, xc - 0.45, xc + 0.45, d - 0.6, z0, z0 + 3.4), BRICK, INK, 2.6)
        a, b = L.p(xc - 0.45, d - 0.6, z0 + 3.4), L.p(xc + 0.45, d - 0.6, z0)
        bricks(p, (a[0], a[1], b[0], b[1]), BRICK, int(xc * 10) + 50, cw=11, ch=5, n=30, lw=0.6)
    p.poly(face(L, -2.3, 5.3, d - 0.7, z0 + 2.75, z0 + 3.55), (30, 34, 40), INK, 2.6)        # the sign band
    sx, sy = L.p(1.5, d - 0.7, z0 + 3.15)
    sign(img, cam, 'CROWN COURT SOUTHWARK', sx, sy, 6.4 * L.ppm(d - 0.7), (236, 236, 232))
    a = L.p(4.85, d - 0.62, z0 + 1.8)                                                      # a small red sign on a
    p.poly(quad(a[0] - 9, a[1] - 12, a[0] + 9, a[1] + 12), (196, 40, 44), INK, 1.4)         # pier (ref 00)
    p.poly(quad(a[0] - 6, a[1] - 2, a[0] + 6, a[1] + 2), (246, 246, 246), None)
    # the forecourt and its low brick walls with planted beds, the steps and rails on the left
    p.poly(quad(-300, L.p(0, d, z0)[1], W + 300, L.p(0, PLAZA_D0, PLAZA_Z)[1]), (196, 190, 180), None)
    for (xa, xb) in ((-14, -5.2), (-1.6, 14)):
        a, b = L.p(xa, PLAZA_D0, PLAZA_Z + 0.55), L.p(xb, PLAZA_D0, 0.0)
        for k, xc in enumerate(np.arange(xa + 0.6, xb, 1.15)):                              # the shrubs in the bed
            c = L.p(xc, PLAZA_D0 + 0.8, PLAZA_Z + 0.75)
            clump(p, c[0], c[1], 32 + 8 * (k % 3), 26, PLANT if k % 4 else (150, 70, 60), 600 + k + int(xa),
                  marks=True, lw=1.8)
        p.poly(quad(a[0], a[1], b[0], b[1]), BRICK, INK, 2.6)                                 # the low wall
        bricks(p, (a[0], a[1], b[0], b[1]), BRICK, 70 + int(xa), cw=14, ch=6, n=40, lw=0.6)
        p.poly(quad(a[0] - 3, a[1] - 6, b[0] + 3, a[1] + 2), (200, 190, 178), INK, 1.8)        # its coping
    for k in range(6):                                                                     # the steps
        z = PLAZA_Z * (k + 1) / 6
        dd = PLAZA_D0 - 1.8 + 0.3 * k
        a, b = L.p(-5.2, dd, z), L.p(-1.6, dd - 0.3, z - PLAZA_Z / 6)
        p.poly(quad(a[0], a[1], b[0], b[1]), mix(PAVE, (255, 255, 255), 0.1 * (k % 2)), INK, 1.6)
    for xr in (-4.9, -1.9):                                                                # the rails
        pts = [L.p(xr, PLAZA_D0 - 1.8 + 0.3 * k, PLAZA_Z * k / 6 + 0.95) for k in range(7)]
        p.line(pts, (210, 214, 218), 3.4)
        p.line(pts, INK, 1.0)
        for k in (0, 3, 6):
            q = pts[k]
            g = L.p(xr, PLAZA_D0 - 1.8 + 0.3 * k, PLAZA_Z * k / 6)
            p.line([q, g], (210, 214, 218), 2.6)
    # the trees at both ends (autumn, 13 Oct), the lamp post
    for k, (x, dd) in enumerate(((-7.6, 12.5), (8.2, 13.0), (-10.5, 14.0))):
        base, topp = L.p(x, dd, 0.0), L.p(x, dd, 7.5)
        p.poly(wob(quad(base[0] - 9, topp[1], base[0] + 9, base[1]), 1.5, 40 + k), (92, 74, 58), INK, 2.2)
        for j, (ox, oz, rr) in enumerate(((0, 8.2, 2.6), (-1.6, 6.6, 1.9), (1.7, 6.9, 2.0), (0.4, 5.6, 1.5))):
            c = L.p(x + ox, dd, oz)
            clump(p, c[0], c[1], rr * L.ppm(dd), rr * L.ppm(dd) * 0.8,
                  mix(AUTUMN, PLANT, 0.35 * (j % 2)), 900 + 10 * k + j, lw=2.2)
    lp, lt = L.p(-3.9, 8.5, 0.0), L.p(-3.9, 8.5, 8.0)
    p.poly(quad(lp[0] - 5, lt[1], lp[0] + 5, lp[1]), (120, 124, 128), INK, 1.8)
    p.poly(quad(lp[0] - 22, lt[1] - 10, lp[0] + 8, lt[1] + 4), (110, 114, 118), INK, 1.6)
    # the pavement: grey slabs, joints in perspective, a kerb at the front
    g0 = L.p(0, PLAZA_D0, 0)[1]
    p.poly(quad(-300, g0, W + 300, 2400), PAVE, None)
    for dd in np.arange(1.2, PLAZA_D0, 0.9):
        y = L.p(0, dd, 0)[1]
        p.line([(-300, y), (W + 300, y)], PAVE_D, 1.4)
    for xx in np.arange(-12, 12.1, 0.9):
        a, b = L.p(xx, PLAZA_D0, 0), L.p(xx, 1.0, 0)
        p.line([a, b], PAVE_D, 1.2)
    r = random.Random(5)
    for _ in range(26):                                                                    # stains, chewing gum
        dd = r.uniform(1.5, 10)
        x, y = L.p(r.uniform(-6, 6), dd, 0)
        p.ell(x, y, 30 / dd, 10 / dd, PAVE_D, None)


# ================================================================================================ the courtroom
# Refs 05, 07, 08, 11 (the sketch artists): pale walls of tall light-wood panels, pale oak furniture, the judge in red
# high at the bench with a microphone on a stalk, the witness box with its own microphone, the dock walled in glass
# on a wood base, security officers seated behind the defendant. Over the bench: the royal arms (every English Crown
# Court has them; not in the sketches' crops, added so the room reads as a court at phone size).
WALL = (226, 214, 194)
WALL_L = (236, 226, 208)
OAK = (204, 166, 116)
OAK_D = (170, 130, 86)
OAK_L = (222, 190, 144)
JUDGE_CHAIR = (128, 34, 40)
METAL = (60, 62, 66)


def _panels(p, x0, y0, x1, y1, step, seed):
    """Tall light-wood wall panels (the sketches' vertical strokes): each its own width, a darker joint."""
    r = random.Random(seed)
    p.poly(quad(x0, y0, x1, y1), WALL, None)
    x = x0
    while x < x1:
        w = step * r.uniform(0.8, 1.2)
        p.poly(quad(x + 3, y0, x + w - 3, y1), mix(WALL, WALL_L, r.uniform(0, 1)), None)
        p.line([(x, y0), (x + r.uniform(-2, 2), y1)], dk(WALL, 0.84), 1.6)
        x += w


def _arms(p, img, cam, cx, cy, s):
    """The royal arms, simplified: a quartered shield in a blue garter, a crown on top, the motto scroll below."""
    p.ell(cx, cy, 120 * s, 140 * s, (40, 50, 110), INK, 2.4)                              # the garter
    p.ell(cx, cy, 98 * s, 118 * s, WALL_L, None)
    sh = [(cx - 70 * s, cy - 84 * s), (cx + 70 * s, cy - 84 * s), (cx + 70 * s, cy + 10 * s),
          (cx, cy + 96 * s), (cx - 70 * s, cy + 10 * s)]
    p.poly(sh, (190, 40, 46), INK, 2.2)
    p.poly([(cx + 0.5, cy - 84 * s), (cx + 70 * s, cy - 84 * s), (cx + 70 * s, cy + 6 * s), (cx + 0.5, cy + 6 * s)],
           (220, 180, 60), None)                                                          # gold and blue quarters
    p.poly([(cx - 70 * s, cy + 6 * s), (cx, cy + 6 * s), (cx, cy + 96 * s), (cx - 70 * s, cy + 10 * s)],
           (220, 180, 60), None)
    p.poly([(cx, cy + 6 * s), (cx + 70 * s, cy + 6 * s), (cx + 70 * s, cy + 10 * s), (cx, cy + 96 * s)],
           (190, 40, 46), None)
    p.poly(sh, None, INK, 2.2)
    p.line([(cx, cy - 84 * s), (cx, cy + 96 * s)], INK, 1.6)
    p.line([(cx - 70 * s, cy + 6 * s), (cx + 70 * s, cy + 6 * s)], INK, 1.6)
    for qx, qy, c in ((-35, -40, (236, 200, 80)), (35, 50, (236, 200, 80)), (35, -40, (190, 40, 46)),
                      (-35, 50, (190, 40, 46))):                                          # a beast in each, as marks
        p.ell(cx + qx * s, cy + qy * s, 16 * s, 11 * s, dk(c, 0.75) if c[0] > 200 else (236, 200, 80), INK, 1.0)
    cr = [(cx - 62 * s, cy - 150 * s), (cx - 50 * s, cy - 196 * s), (cx - 24 * s, cy - 172 * s), (cx, cy - 214 * s),
          (cx + 24 * s, cy - 172 * s), (cx + 50 * s, cy - 196 * s), (cx + 62 * s, cy - 150 * s)]
    p.poly(cr, (222, 178, 60), INK, 2.2)                                                  # the crown
    p.poly(quad(cx - 62 * s, cy - 152 * s, cx + 62 * s, cy - 136 * s), (180, 40, 46), INK, 1.8)
    p.ell(cx, cy - 214 * s, 8 * s, 8 * s, (222, 178, 60), INK, 1.4)
    p.poly([(cx - 130 * s, cy + 150 * s), (cx + 130 * s, cy + 150 * s), (cx + 118 * s, cy + 186 * s),
            (cx - 118 * s, cy + 186 * s)], (240, 232, 214), INK, 1.8)                     # the motto scroll
    p.line([(cx - 90 * s, cy + 168 * s), (cx + 90 * s, cy + 168 * s)], (150, 140, 120), 1.4)


def _mic(p, base, tip, lw=2.4):
    """A courtroom microphone on a thin curved stalk (refs 05, 07, 10, 11)."""
    mx = (base[0] * 0.6 + tip[0] * 0.4, base[1] * 0.2 + tip[1] * 0.8 - 20)
    pts = [base, mx, tip]
    p.line(pts, METAL, lw)
    p.ell(tip[0], tip[1], 6, 9, (34, 34, 36), INK, 1.2, rot=0.6)
    p.ell(base[0], base[1] + 3, 14, 5, METAL, INK, 1.2)


def _bench(p, img, cam, x0, x1, ytop, yfloor, papers=True):
    """The judge's bench: a long pale-oak desk front in raised panels, a ledge, papers and a laptop on it."""
    p.poly(wob(quad(x0, ytop, x1, yfloor), 1.4, 9), OAK, INK, 3.0)
    p.poly(quad(x0 - 8, ytop - 16, x1 + 8, ytop + 4), OAK_L, INK, 2.4)                    # the ledge
    n = max(2, int((x1 - x0) / 170))
    for k in range(n):
        a = x0 + (x1 - x0) * k / n + 16
        b = x0 + (x1 - x0) * (k + 1) / n - 16
        p.poly(quad(a, ytop + 30, b, yfloor - 26), OAK_D, INK, 1.6)
        p.poly(quad(a + 8, ytop + 38, b - 8, yfloor - 34), mix(OAK, OAK_D, 0.4), None)
    if papers:
        p.poly([(x0 + 60, ytop - 16), (x0 + 200, ytop - 16), (x0 + 210, ytop - 30), (x0 + 70, ytop - 30)],
               (246, 244, 236), INK, 1.4)


def court_box(img, cam, t=0.0):
    """Line 2 (refs 05, 07): Brand side-on in the witness box (lower right, near), the judge behind him (upper left)
    at the bench under the royal arms, a microphone at each."""
    p = B.Pen(img, cam)
    _panels(p, -300, -400, W + 300, 1250, 120, 3)
    p.poly(quad(-300, 120, W + 300, 136), dk(WALL, 0.88), INK, 1.4)                         # a picture rail
    _arms(p, img, cam, 300, 360, 0.95)
    p.poly(wob(quad(130, 640, 470, 1080), 2, 11), JUDGE_CHAIR, INK, 2.8)                    # the judge's chair back
    p.poly(quad(150, 664, 450, 1080), dk(JUDGE_CHAIR, 0.82), None)
    for k in range(3):                                                                     # its buttoned leather
        for j in range(3):
            p.ell(200 + k * 100, 710 + j * 100, 5, 5, dk(JUDGE_CHAIR, 0.6), None)
    p.poly(quad(-300, 1250, W + 300, 1290), dk(WALL, 0.8), INK, 2.0)                        # the dais edge
    p.poly(quad(-300, 1300, W + 300, 2400), (150, 96, 70), None)                            # the well: carpet
    for k in range(9):
        y = 1340 + k * 70
        p.line([(-300, y), (W + 300, y + 10)], (138, 88, 64), 1.6)


def court_box_mid(img, cam, t=0.0):
    """The judge's bench and microphone, over the seated judge, under Brand."""
    p = B.Pen(img, cam)
    _bench(p, img, cam, -120, 760, 1020, 1420)
    _mic(p, (520, 1004), (430, 900))


def court_box_front(img, cam, t=0.0):
    """The witness box's front and ledge, drawn over Brand's lower body, with his microphone (ref 07)."""
    p = B.Pen(img, cam)
    p.poly(wob(quad(470, 1690, W + 300, 2400), 1.6, 21), OAK, INK, 3.2)
    p.poly(quad(452, 1668, W + 300, 1706), OAK_L, INK, 2.6)                                 # the ledge
    p.poly(quad(530, 1760, 1000, 2000), OAK_D, INK, 1.8)
    p.poly(quad(540, 1770, 990, 1990), mix(OAK, OAK_D, 0.45), None)
    p.poly([(860, 1668), (1010, 1668), (1020, 1648), (872, 1648)], (40, 36, 34), INK, 1.6)   # the Bible on the ledge
    _mic(p, (520, 1664), (610, 1300), 3.0)


def court_bench(img, cam, t=0.0):
    """The gavel: the judge front-on at the bench (chest up), the arms over him, papers and the gavel block."""
    p = B.Pen(img, cam)
    _panels(p, -300, -400, W + 300, 1500, 150, 13)
    _arms(p, img, cam, 540, 300, 1.25)
    p.poly(wob(quad(260, 640, 820, 1420), 2, 31), JUDGE_CHAIR, INK, 3.0)                    # the chair back
    p.poly(quad(288, 676, 792, 1420), dk(JUDGE_CHAIR, 0.82), None)
    for k in range(5):
        for j in range(4):
            p.ell(330 + k * 105, 730 + j * 110, 6, 6, dk(JUDGE_CHAIR, 0.6), None)


def court_bench_front(img, cam, t=0.0):
    p = B.Pen(img, cam)
    _bench(p, img, cam, -200, W + 200, 1460, 2400, papers=False)
    for k, (x, y, w) in enumerate(((150, 1420, 230), (200, 1404, 210))):                   # papers
        p.poly([(x, y + 40), (x + w, y + 40), (x + w + 16, y), (x + 14, y)], (248, 246, 238), INK, 1.4)
    p.ell(760, 1430, 70, 18, (110, 70, 44), INK, 2.0)                                      # the sound block
    p.poly(quad(690, 1412, 830, 1430), (124, 80, 50), None)
    _mic(p, (330, 1446), (450, 1270), 3.0)


def court_dock(img, cam, t=0.0):
    """Line 3 (refs 08, 11): the glass dock, Brand standing in it; the wall and two seated officers behind (the
    officers are cast, drawn by the film); the glass and wood base go over him (court_dock_front)."""
    p = B.Pen(img, cam)
    _panels(p, -300, -400, W + 300, 1500, 110, 23)
    p.poly(quad(-300, 1060, W + 300, 1080), dk(WALL, 0.86), INK, 1.4)                       # a dado rail
    p.poly(quad(-300, 1080, W + 300, 1500), mix(WALL, OAK, 0.25), None)
    for k in range(7):                                                                     # the dock's back bench
        x = -60 + k * 180
        p.poly(quad(x, 1270, x + 170, 1330), OAK_D, INK, 1.8)
    p.poly(quad(-300, 1330, W + 300, 2400), (176, 150, 116), None)                          # the dock's floor


def court_dock_front(img, cam, t=0.0):
    """The dock's glass (thin steel uprights, a top rail, pale reflections) over a pale-oak base (ref 08)."""
    p = B.Pen(img, cam)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    lp = B.Pen(lay, cam)
    lp.poly(quad(-300, 420, W + 300, 1740), (220, 236, 240, 46), None)                     # the glass, faint
    for x0, x1 in ((80, 150), (620, 660), (700, 790)):                                     # reflections
        lp.poly([(x0, 420), (x1, 420), (x1 - 300, 1740), (x0 - 300, 1740)], (255, 255, 255, 56), None)
    img.alpha_composite(lay)
    for x in (-40, 300, 780, 1120):                                                        # the uprights
        p.poly(quad(x - 7, 400, x + 7, 1740), (120, 126, 132), INK, 1.6)
    p.poly(quad(-300, 396, W + 300, 414), (120, 126, 132), INK, 1.8)                        # the top rail
    p.poly(wob(quad(-300, 1740, W + 300, 2400), 1.6, 41), OAK, INK, 3.2)                   # the wood base
    p.poly(quad(-300, 1726, W + 300, 1760), OAK_L, INK, 2.6)
    for k in range(4):
        x = 20 + k * 270
        p.poly(quad(x, 1810, x + 230, 2100), mix(OAK, OAK_D, 0.45), INK, 1.6)


# ================================================================================================ the van
# The escort van's cell (no photo reached us: Sam's list): a cubicle under a metre wide, white moulded plastic
# walls, a moulded bench seat, a small square window of dark tinted glass on the side wall with the street's lights
# sliding past, a steel door with a mesh hatch behind the lens. Cold, dim, grey-blue.
VAN_W = (196, 202, 208)
VAN_D = (150, 158, 166)


def van(img, cam, t=0.0):
    p = B.Pen(img, cam)
    p.poly(quad(-300, -400, W + 300, 2400), dk(VAN_W, 0.9), None)
    p.poly([(-300, -400), (160, 200), (160, 1500), (-300, 2400)], VAN_D, INK, 2.6)          # the left wall
    p.poly([(W + 300, -400), (920, 200), (920, 1500), (W + 300, 2400)], dk(VAN_D, 0.92), INK, 2.6)   # the right wall
    p.poly(quad(160, 200, 920, 1500), VAN_W, INK, 2.6)                                      # the back wall
    p.poly([(-300, -400), (W + 300, -400), (920, 200), (160, 200)], dk(VAN_W, 0.8), INK, 2.4)   # the ceiling
    p.ell(540, 40, 120, 26, (236, 240, 230), INK, 2.0)                                      # the ceiling light
    for x in (350, 730):                                                                   # moulded panel seams
        p.line([(x, 206), (x + 4, 1176)], dk(VAN_W, 0.86), 2.0)
    p.poly(wob(quad(250, 300, 330, 380), 0.8, 63), (246, 214, 60), INK, 1.6)                 # a CCTV sticker
    p.ell(290, 334, 16, 10, (40, 40, 44), None)
    p.poly(quad(272, 352, 308, 362), (40, 40, 44), None)
    p.poly(quad(480, 560, 610, 610), (220, 222, 226), INK, 2.0)                               # an air vent
    for k in range(4):
        p.line([(492, 570 + 10 * k), (598, 570 + 10 * k)], dk(VAN_W, 0.7), 1.6)
    p.line([(180, 700), (176, 1000)], (150, 154, 160), 7.0)                                  # a grab rail
    p.line([(180, 700), (176, 1000)], INK, 1.2)
    for x, y in ((210, 260), (870, 260), (210, 1450), (870, 1450)):                       # rivets at the corners
        p.ell(x, y, 5, 5, VAN_D, INK, 1.0)
    # the window on the right wall: the street going by (lights slide left to right, looping every 1.6 s)
    win = [(1040, 360), (940, 420), (940, 700), (1040, 700)]
    p.poly(win, (24, 28, 40), INK, 2.6)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    lp = B.Pen(lay, cam)
    for k in range(5):
        u = ((t / 1.6) + k / 5) % 1.0
        x = 940 + 100 * u
        y = 470 + 40 * k
        lp.poly(quad(x - 22, y, x + 22, y + 8), (240, 200, 110, 210) if k % 2 else (236, 236, 240, 200), None)
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).polygon([cam.P(*q) for q in win], fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay)[..., 3], np.asarray(m))))
    img.alpha_composite(lay)
    p.poly(win, None, INK, 2.6)
    p.line([(990, 390), (990, 700)], (60, 64, 70), 3.0)                                     # the bars in it
    # the moulded seat across the back
    p.poly(wob(quad(150, 1180, 930, 1290), 1.2, 61), mix(VAN_W, VAN_D, 0.5), INK, 2.6)
    p.poly([(150, 1290), (930, 1290), (980, 1600), (100, 1600)], dk(VAN_W, 0.78), INK, 2.4)
    p.poly([(-300, 2400), (100, 1600), (980, 1600), (W + 300, 2400)], (84, 88, 96), INK, 2.4)   # the floor
    for k in range(6):                                                                     # its ribbed rubber
        u = k / 6
        p.line([(100 + (-400) * u * 0, 1640 + 120 * k), (980, 1640 + 120 * k)], (70, 74, 80), 2.0)


def van_front(img, cam, t=0.0):
    """Dim cold light over everyone in the van, and the window's passing lights sweeping over them."""
    lay = Image.new('RGBA', img.size, (30, 40, 70, 60))
    img.alpha_composite(lay)
    u = (t / 1.6) % 1.0
    soft(img, cam, (900 - 700 * u, 300, 1300 - 700 * u, 1500), (240, 210, 150), 0.10, 120)


# ================================================================================================ the prison
# Refs 12, 13, 14: a narrow cell, cream walls (painted brick in the old wings), one barred window high in the back
# wall, a metal-framed bed along the left wall (thin blue mattress, green blanket), a steel toilet and basin in the
# back right corner, a shelf-desk, a pinboard; the blue steel door with its observation slot standing open on the
# right, the landing's railings beyond it. One painting; the cot close-up is a camera on it.
CELL = (226, 216, 190)
CELL_D = (198, 186, 160)
CELL_FLOOR = (150, 140, 124)
DOOR_BLUE = (52, 92, 150)
MATT = (70, 110, 170)
BLANKET = (84, 128, 92)
STEEL = (176, 182, 188)


def cell(img, cam, t=0.0):
    p = B.Pen(img, cam)
    p.poly(quad(-300, -400, W + 300, 2400), CELL, None)
    # the back wall (far), the left and right walls in perspective, ceiling and floor
    bx0, by0, bx1, by1 = 230, 330, 880, 1260
    p.poly([(-300, -400), (W + 300, -400), (bx1, by0), (bx0, by0)], mix(CELL, (255, 255, 255), 0.25), INK, 2.2)
    p.poly([(-300, -400), (bx0, by0), (bx0, by1), (-300, 2400)], CELL_D, INK, 2.4)
    p.poly([(W + 300, -400), (bx1, by0), (bx1, by1), (W + 300, 2400)], dk(CELL_D, 0.95), INK, 2.4)
    p.poly(quad(bx0, by0, bx1, by1), CELL, INK, 2.4)
    p.poly([(-300, 2400), (bx0, by1), (bx1, by1), (W + 300, 2400)], CELL_FLOOR, INK, 2.4)
    for k in range(10):                                                                     # painted brick courses
        y = by0 + 40 + k * 88
        p.line([(bx0 + 6, y), (bx1 - 6, y + 2)], CELL_D, 1.2)
    bricks(p, (bx0, by0, bx1, by1), CELL, 77, cw=40, ch=22, n=26, lw=0.8)
    p.poly(quad(bx0, by1 - 70, bx1, by1), mix(CELL, DOOR_BLUE, 0.35), INK, 1.6)            # a painted dado
    # the window, high, barred
    p.poly(wob(quad(450, 420, 660, 640), 1.2, 3), (210, 226, 236), INK, 3.0)
    p.poly(quad(462, 432, 648, 628), (176, 204, 224), None)
    p.poly(quad(462, 560, 648, 628), (160, 184, 150), None)                                 # the yard's grass
    for x in (500, 540, 580, 620):
        p.line([(x, 424), (x, 636)], (70, 74, 80), 4.0)
    p.poly(quad(440, 640, 670, 656), CELL_D, INK, 1.8)
    # the steel toilet and basin in the back right corner
    p.poly(quad(760, 960, 870, 1020), STEEL, INK, 2.0)                                      # basin
    p.poly([(770, 1020), (860, 1020), (840, 1090), (790, 1090)], dk(STEEL, 0.9), INK, 1.8)
    p.line([(820, 960), (820, 940), (808, 940)], STEEL, 4.0)
    p.ell(790, 1200, 60, 22, STEEL, INK, 2.0)                                               # the toilet bowl
    p.poly([(740, 1200), (840, 1200), (820, 1262), (760, 1262)], dk(STEEL, 0.92), INK, 1.8)
    p.ell(790, 1196, 44, 13, dk(STEEL, 0.7), None)
    # the shelf-desk and pinboard on the back wall, middle
    p.poly(quad(470, 880, 700, 900), (190, 160, 120), INK, 1.8)
    p.poly(quad(490, 900, 504, 1060), (190, 160, 120), INK, 1.4)
    p.poly(quad(500, 700, 690, 840), (176, 140, 100), INK, 1.8)
    for k, (x, y, c) in enumerate(((520, 716, (246, 246, 240)), (580, 730, (230, 220, 160)), (630, 712, (246, 246, 240)))):
        p.poly(quad(x, y, x + 42, y + 56), c, INK, 1.0)
        p.line([(x + 6, y + 14), (x + 34, y + 14)], (160, 160, 160), 1.0)
    p.poly(quad(560, 858, 620, 880), (240, 240, 236), INK, 1.2)                             # a plastic mug
    # the bed along the left wall: a steel frame, thin blue mattress, green blanket, a flat pillow
    near, far = 1720, 1180
    p.poly([(-300, near - 120), (bx0 - 10, far - 60), (bx0 + 210, far - 50), (380, near - 120)], MATT, INK, 2.6)
    p.poly([(-300, near - 120), (380, near - 120), (380, near - 40), (-300, near - 40)], dk(MATT, 0.78), INK, 2.4)
    p.poly([(-300, near - 150), (120, near - 150), (bx0 + 120, far - 40), (bx0 + 40, far - 52)],
           BLANKET, INK, 2.2)                                                               # the blanket, folded back
    p.poly([(bx0 + 10, far - 70), (bx0 + 190, far - 62), (bx0 + 200, far - 38), (bx0 + 20, far - 44)],
           (236, 236, 232), INK, 1.8)                                                       # the pillow
    for x in (-200, 360):                                                                   # the frame's legs
        p.poly(quad(x, near - 40, x + 18, near + 80), (90, 96, 104), INK, 1.6)
    p.poly(quad(bx0 + 196, far - 50, bx0 + 208, far + 20), (90, 96, 104), INK, 1.4)
    # the open blue door on the right wall, the landing beyond it
    dx0, dx1 = 930, 1080
    p.poly([(dx0, 470), (dx1 + 60, 300), (dx1 + 60, 1800), (dx0, 1400)], (76, 80, 90), INK, 2.4)   # the opening
    p.poly([(dx0 + 10, 520), (dx1 + 60, 380), (dx1 + 60, 1000), (dx0 + 10, 1010)], (198, 196, 190), None)  # the landing
    for y in (980, 1060):                                                                   # its railing
        p.line([(dx0 + 10, y), (dx1 + 60, y - 30)], (60, 120, 160), 4.0)
    p.poly([(dx0 + 10, 1100), (dx1 + 60, 1080), (dx1 + 60, 1240), (dx0 + 10, 1220)], (210, 214, 210), None)  # netting
    for k in range(8):
        x = dx0 + 20 + 22 * k
        p.line([(x, 1100), (x + 10, 1230)], (150, 150, 150), 1.0)
    p.poly([(dx0 - 40, 480), (dx0 + 10, 470), (dx0 + 10, 1400), (dx0 - 40, 1420)], DOOR_BLUE, INK, 2.6)  # the door,
    p.poly([(dx0 - 30, 700), (dx0, 696), (dx0, 760), (dx0 - 30, 764)], (40, 44, 50), INK, 1.4)          # opened in


PHONE_DY = 330
PHONE_CORD = (510, 900 + PHONE_DY)          # where the handset's steel cord leaves the phone (screen px)


def phone(img, cam, t=0.0):
    """Line 4: the landing's wall phone (a steel PIN phone under a blue acoustic hood, a cord to the handset), the
    painted brick wall with notices, the railing and safety net at the right, the far landing's doors beyond."""
    p = B.Pen(img, cam)
    p.poly(quad(-300, -400, W + 300, 2400), CELL, None)
    bricks(p, (-300, -400, 860, 2400), CELL, 88, cw=70, ch=30, n=70, lw=1.0)
    for k in range(40):
        y = -380 + k * 60
        p.line([(-300, y), (860, y + 2)], CELL_D, 1.2)
    p.poly(quad(-300, 1500, 860, 2400), mix(CELL, DOOR_BLUE, 0.4), INK, 2.0)               # the painted dado
    # the far landing through the drop (right), behind the railing and the net
    p.poly(quad(860, -400, W + 300, 2400), (150, 150, 146), INK, 2.4)
    for k in range(3):                                                                     # far cell doors
        y = -120 + k * 640
        p.poly(quad(900, y, 1010, y + 300), DOOR_BLUE, INK, 2.0)
        p.poly(quad(940, y + 60, 970, y + 110), (40, 44, 50), None)
        p.poly(quad(860, y + 360, W + 300, y + 390), (120, 124, 130), INK, 1.6)            # their landing's edge
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    lp = B.Pen(lay, cam)
    lp.poly(quad(860, 1200, W + 300, 1700), (230, 232, 230, 120), None)                    # the safety net
    img.alpha_composite(lay)
    for k in range(10):
        p.line([(860 + 24 * k, 1200), (880 + 24 * k, 1700)], (170, 170, 168), 1.0)
        p.line([(860, 1200 + 50 * k), (W + 300, 1210 + 50 * k)], (170, 170, 168), 1.0)
    p.poly(quad(840, -400, 880, 2400), (60, 120, 160), INK, 2.2)                            # the railing post
    # the hood, the phone, its cord, the notices (all PHONE_DY lower: beside his head)
    p = B.Pen(img, B.Local(cam, 0, PHONE_DY, 1.0))
    p.poly([(250, 380), (760, 380), (800, 1040), (210, 1040)], (60, 96, 150), INK, 3.0)     # the acoustic hood
    p.poly([(280, 410), (730, 410), (764, 1010), (246, 1010)], (220, 220, 214), None)
    for k in range(9):                                                                     # its perforations
        for j in range(5):
            p.ell(300 + k * 50, 450 + j * 120, 3, 3, (186, 186, 180), None)
    p.poly(wob(quad(420, 520, 600, 860), 1.0, 5), STEEL, INK, 2.6)                          # the PIN phone
    for k in range(4):                                                                     # its keypad
        for j in range(3):
            p.poly(quad(470 + j * 30, 660 + k * 34, 494 + j * 30, 686 + k * 34), (230, 232, 234), INK, 1.0)
    p.poly(quad(450, 560, 570, 620), (40, 60, 50), INK, 1.4)                                 # its little screen
    p.poly(quad(400, 540, 430, 760), (40, 40, 44), INK, 1.6)                                 # the handset cradle
    p.poly(quad(500, 860, 520, 900), (150, 156, 160), INK, 1.4)                              # where the cord leaves
    sign(img, cam, 'PIN PHONE', 510, 486 + PHONE_DY, 150, (40, 40, 44))
    for k, (x, y, w_, h_, c, txt) in enumerate(((10, 440, 190, 300, (250, 250, 246), 'NOTICE'),
                                                 (20, 830, 180, 250, (250, 236, 120), 'SAMARITANS'),
                                                 (820, 440, 60, 90, (246, 246, 246), ''))):
        p.poly(wob(quad(x, y, x + w_, y + h_), 1.0, 70 + k), c, INK, 1.6)
        if txt:
            sign(img, cam, txt, x + w_ / 2, y + 36 + PHONE_DY, w_ * 0.74, (40, 40, 44))
        for j in range(4):
            p.line([(x + 20, y + 80 + j * 36), (x + w_ - 24 - 16 * (j % 2), y + 80 + j * 36)], (150, 150, 150), 2.0)
        p.ell(x + w_ / 2, y + 10, 5, 5, (200, 40, 40), INK, 1.0)                          # a drawing pin


# ================================================================================================ the TV room
# Association (no photo reached us: Sam's list): a dim room, walls two-tone (dark green below a rail, cream above),
# moulded plastic chairs, a pool table under its lamp at the back, a barred window gone dark blue, a noticeboard,
# a door with wired glass. The TV hangs on a bracket high up behind the lens: its flicker lights the room.
TV_GREEN = (70, 100, 84)
TV_CREAM = (196, 186, 160)


def tvroom(img, cam, t=0.0):
    p = B.Pen(img, cam)
    p.poly(quad(-300, -400, W + 300, 1240), TV_CREAM, None)
    bricks(p, (-300, -400, W + 300, 1240), TV_CREAM, 99, cw=60, ch=26, n=50, lw=0.9)
    p.poly(quad(-300, 1000, W + 300, 1240), TV_GREEN, INK, 2.2)                              # the green dado
    p.poly(quad(-300, 990, W + 300, 1006), dk(TV_GREEN, 0.7), INK, 1.4)
    window(p, (90, 420, 330, 760), (90, 96, 104), (40, 52, 90), 11, bars=4, lw=2.4)         # night outside
    p.poly(quad(700, 360, 1000, 600), (160, 120, 80), INK, 2.0)                              # the noticeboard
    for k, (x, y) in enumerate(((720, 380), (800, 400), (880, 376), (760, 480), (870, 490))):
        p.poly(quad(x, y, x + 64, y + 80), (246, 246, 238) if k % 2 else (240, 228, 150), INK, 1.0)
    p.poly(quad(420, 470, 600, 1240), (110, 112, 116), INK, 2.4)                             # the door
    p.poly(quad(450, 520, 570, 700), (60, 70, 86), INK, 1.6)                                 # its wired glass
    for k in range(6):
        p.line([(450 + 20 * k, 520), (450 + 20 * k, 700)], (90, 100, 116), 1.0)
        p.line([(450, 520 + 30 * k), (570, 520 + 30 * k)], (90, 100, 116), 1.0)
    p.poly(quad(-300, 1240, W + 300, 2400), (104, 98, 90), None)                            # the lino
    for k in range(10):
        y = 1260 + k * 60 * (1 + k * 0.15)
        p.line([(-300, y), (W + 300, y)], (94, 88, 80), 1.6)
    # the pool table at the back right, its lamp
    p.poly([(640, 1120), (1040, 1120), (1080, 1210), (600, 1210)], (40, 110, 70), INK, 2.4)
    p.poly(quad(600, 1210, 1080, 1260), (90, 60, 40), INK, 2.0)
    for x in (630, 1050):
        p.poly(quad(x - 10, 1260, x + 10, 1320), (90, 60, 40), INK, 1.6)
    p.line([(840, -400), (840, 880)], (40, 40, 44), 2.0)
    p.poly([(770, 880), (910, 880), (940, 940), (740, 940)], (40, 70, 50), INK, 2.0)
    for k, x in enumerate((700, 760, 990)):                                                 # balls
        p.ell(x, 1150, 9, 6, ((200, 40, 40), (240, 200, 60), (240, 240, 240))[k], INK, 1.0)
    # rows of moulded plastic chairs (the seated men are cast: the film draws them on these)
    for k, x in enumerate((60, 330, 600, 870)):
        _chair(p, x, 1560, 1.0, k)


def _chair(p, x, y, s, k):
    """A moulded plastic chair seen from the front: a curved shell back, the seat, four splayed steel legs."""
    c = ((70, 90, 140), (150, 60, 50), (70, 90, 140), (90, 110, 70))[k % 4]
    p.poly(wob(quad(x - 90 * s, y - 250 * s, x + 90 * s, y - 60 * s), 1.2, 400 + k), c, INK, 2.2)
    p.poly([(x - 100 * s, y - 60 * s), (x + 100 * s, y - 60 * s), (x + 110 * s, y), (x - 110 * s, y)],
           dk(c, 0.85), INK, 2.2)
    for sx in (-1, 1):
        p.line([(x + sx * 80 * s, y), (x + sx * 100 * s, y + 160 * s)], (140, 146, 152), 3.0)


def tv_flicker(img, cam, t, strength=1.0):
    """The TV's light on everyone (over the cast): a cool wash from above the lens, its level jumping as the
    picture cuts (a fixed, irregular pattern; never a smooth pulse)."""
    r = random.Random(int(t * 4))
    k = strength * (0.55 + 0.45 * r.random())
    lay = Image.new('RGBA', img.size, (14, 18, 40, int(110 * strength)))
    img.alpha_composite(lay)
    soft(img, cam, (-200, -300, 1280, 1500), (150, 180, 255), 0.22 * k, 260)


def tv(img, cam, t=0.0, feed=None):
    """The TV on its wall bracket, high in the corner, the news on it (feed: an RGBA picture, 16:9)."""
    p = B.Pen(img, cam)
    p.poly(quad(-300, -400, W + 300, 2400), dk(TV_CREAM, 0.6), None)
    bricks(p, (-300, -400, W + 300, 2400), dk(TV_CREAM, 0.6), 101, cw=60, ch=26, n=70, lw=0.9)
    p.poly(quad(-300, 1700, W + 300, 2400), dk(TV_GREEN, 0.6), INK, 2.2)
    p.poly(quad(500, 500, 580, 900), (50, 52, 56), INK, 2.0)                                 # the bracket arm
    p.poly(quad(460, 440, 620, 520), (50, 52, 56), INK, 2.0)
    p.poly(wob(quad(70, 740, 1010, 1300), 0.8, 7), (24, 24, 28), INK, 3.2)                   # the set
    sx0, sy0, sx1, sy1 = 96, 766, 984, 1266
    if feed is not None:
        X0, Y0 = cam.P(sx0, sy0)
        X1, Y1 = cam.P(sx1, sy1)
        img.alpha_composite(feed.convert('RGBA').resize((int(X1 - X0), int(Y1 - Y0)), Image.LANCZOS),
                            (int(X0), int(Y0)))
    else:
        p.poly(quad(sx0, sy0, sx1, sy1), (40, 50, 70), None)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    B.Pen(lay, cam).poly([(sx0, sy0), (sx0 + 300, sy0), (sx0 + 120, sy1), (sx0, sy1)], (255, 255, 255, 26), None)
    img.alpha_composite(lay)                                                                # a sheen on the glass
    p.ell(940, 1284, 6, 4, (220, 60, 50), None)                                             # the standby light
    soft(img, cam, (-100, 600, 1180, 1500), (150, 180, 255), 0.18, 200)


# ================================================================================================ the studio on the TV
def studio_feed(t=0.0, reader=None, size=(960, 540)):
    """The BBC-style studio (Sam's answer 5): newsdesk_set restyled red and white, the newsreader (reader: his sp,
    mouth and all) seated at the desk, the red 'BREAKING NEWS' band and 'BBC NEWS' box over it, 16:9."""
    import newsdesk_set as ND
    _restyle(ND)
    keep = B.SS
    B.SS = 1
    img = B.canvas((0, 0, 0))
    import sets as S3
    cm = S3.Cam((0.0, 1.32, -0.6), (0.0, 1.12, 4.15), focal=1500)     # a mid shot: desk, him, the screen
    people = None
    if reader is not None:
        px, pz = ND.PRESENTER_AT
        people = [(px, pz + 0.05, lambda im, c: ND.put_seated(im, c, reader, px, pz, 180.0, t))]
    ND.render(img, cm, people)
    B.SS = keep
    y0 = 960 - 300
    crop = img.crop((0, y0, 1080, y0 + 608)).resize(size, Image.LANCZOS)
    a = np.asarray(crop).astype(np.int16).copy()                 # the studio's remaining blues (the swirl, the
    r, g, b = a[..., 0], a[..., 1], a[..., 2]                    # newsroom screens) turned BBC red
    m = (b > r + 25) & (b > g)
    a[..., 0] = np.where(m, np.clip(b + 10, 0, 255), r)
    a[..., 1] = np.where(m, g // 4, g)
    a[..., 2] = np.where(m, g // 4, b)
    crop = Image.fromarray(a.astype(np.uint8), 'RGBA')
    d = ImageDraw.Draw(crop)
    w, h = size
    f = lambda n: ImageFont.truetype(SANS, n)
    d.rectangle([0, int(h * 0.74), w, int(h * 0.86)], fill=(184, 18, 24))                  # the breaking band
    d.rectangle([0, int(h * 0.86), w, int(h * 0.93)], fill=(246, 246, 246))                # the strap
    d.text((int(w * 0.04), int(h * 0.80)), 'BREAKING NEWS', font=f(int(h * 0.075)), fill=(255, 255, 255), anchor='lm')
    d.text((int(w * 0.04), int(h * 0.895)), 'Early release scheme: new round announced', font=f(int(h * 0.045)),
           fill=(30, 30, 30), anchor='lm')
    d.rectangle([0, int(h * 0.93), w, h], fill=(30, 30, 34))                                # the ticker
    tk = 'PRISONS AT CAPACITY  •  GOVERNMENT ANNOUNCES EARLY RELEASES  •  '
    off = int((t * 60) % (w * 1.2))
    d.text((int(w * 0.02) - off, int(h * 0.965)), tk * 2, font=f(int(h * 0.04)), fill=(240, 240, 240), anchor='lm')
    bx = int(w * 0.04)                                                                      # 'BBC NEWS' bug
    d.rectangle([bx, int(h * 0.06), bx + int(w * 0.20), int(h * 0.15)], fill=(184, 18, 24))
    d.text((bx + int(w * 0.10), int(h * 0.105)), 'BBC NEWS', font=f(int(h * 0.055)), fill=(255, 255, 255), anchor='mm')
    return crop


_RESTYLED = []


def _restyle(ND):
    """Newsdesk's studio in BBC News red and white: the colours swapped at the module, English lettering."""
    if _RESTYLED:
        return
    _RESTYLED.append(1)
    for k, v in dict(DISC_BLUE=(184, 18, 24), DISC_MID=(206, 40, 44), DISC_PALE=(232, 120, 120),
                     DISC_NAVY=(70, 10, 14), DISC_RED=(250, 250, 250), DISC_ARC=(236, 226, 226),
                     DESK_BLUE=(170, 20, 26), DESK_LIGHT=(230, 110, 110), DESK_TOP=(246, 246, 246),
                     WALL_NAVY=(60, 12, 18), WALL_DARK=(30, 10, 12), LED_BLUE=(176, 20, 28),
                     RED_LIGHT=(250, 250, 250)).items():
        setattr(ND, k, v)
    ND.SCREEN_CAPTION = ('BREAKING', 'NEWS')

    def text(s, px, col, pad=8):
        s = {'חדשות': 'NEWS'}.get(s, s)
        f = ImageFont.truetype(SANS, px)
        l, t, r, b = f.getbbox(s)
        im = Image.new('RGBA', (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((pad - l, pad - t), s, font=f, fill=col)
        return im
    ND.heb_text = text


# ================================================================================================ the prison gates
# Refs 18-20 (HMP Wandsworth's gatehouse; a prison gate in daylight): a Victorian gatehouse in dark sooty brick with
# pale stone dressings, two square towers either side of a tall round arch, a timber double gate filling it with a
# small wicket door cut in it (he walks out through it), barred arched windows, the brick wall running off both
# ways, a white 'HM Prison' sign, a forecourt of tarmac with a yellow bollard, overcast sky. Camera as at the court.
GATE = Level(2.4, 1150.0, 1100.0)    # a wider lens than the court: the whole gatehouse in
SOOT = (88, 80, 74)
SOOT_D = (66, 60, 56)
STONE = (186, 176, 158)
TIMBER = (112, 74, 48)
GATE_D = 18.0


def gates(img, cam, t=0.0):
    p = B.Pen(img, cam)
    L = GATE
    p.poly(quad(-300, -800, W + 300, 1200), (206, 210, 214), None)                          # overcast
    for k, (x, y, rx) in enumerate(((100, 80, 300), (820, 30, 340), (500, 180, 220))):
        p.poly(blob(x, y, rx, 60, 10, 0.12, 60 + k), (222, 224, 228) if k % 2 else (190, 194, 200), None)
    d = GATE_D
    p.poly(face(L, -16, 16, d + 3, 0, 5.4), SOOT, INK, 2.6)                                 # the long wall behind
    a, b = L.p(-16, d + 3, 5.4), L.p(16, d + 3, 0)
    bricks(p, (a[0], a[1], b[0], b[1]), SOOT, 11, cw=12, ch=5, n=200, lw=0.6)
    p.poly(face(L, -16, 16, d + 3, 5.4, 5.8), STONE, INK, 2.0)                              # its coping
    for sx in (-1, 1):                                                                      # the two towers
        x0, x1 = (-5.6, -2.4) if sx < 0 else (2.4, 5.6)
        p.poly(face(L, x0, x1, d, 0, 15.5), SOOT, INK, 3.0)
        a, b = L.p(x0, d, 15.5), L.p(x1, d, 0)
        bricks(p, (a[0], a[1], b[0], b[1]), SOOT, 20 + sx, cw=12, ch=5, n=150, lw=0.6)
        p.poly(face(L, x0 - 0.2, x1 + 0.2, d - 0.05, 14.7, 15.5), STONE, INK, 2.2)          # the cornice
        p.poly(face(L, x0 - 0.1, x1 + 0.1, d - 0.05, 0, 0.8), STONE, INK, 2.0)              # the plinth
        for zb in (3.4, 7.6, 11.2):                                                         # the arched windows
            xc = (x0 + x1) / 2
            a, b = L.p(xc - 0.55, d - 0.02, zb + 2.0), L.p(xc + 0.55, d - 0.02, zb)
            r_ = (b[0] - a[0]) / 2
            arch = [(a[0] + r_ + r_ * math.cos(u), a[1] + r_ - r_ * math.sin(u)) for u in np.linspace(0, math.pi, 12)]
            pts = [(b[0], b[1])] + arch + [(a[0], b[1])]
            outer = [(x + (x - (a[0] + r_)) * 0.32, y - 8) for x, y in arch]
            p.poly([(b[0] + r_ * 0.32, b[1] + 6)] + outer + [(a[0] - r_ * 0.32, b[1] + 6)], STONE, INK, 2.0)
            p.poly(pts, (44, 48, 56), INK, 2.0)
            for k in range(1, 3):
                x = a[0] + (b[0] - a[0]) * k / 3
                p.line([(x, a[1] + r_ * 0.4), (x, b[1])], (120, 124, 130), 1.6)
    # the centre block over the arch, the arch and the timber gate with its wicket door
    p.poly(face(L, -2.4, 2.4, d + 0.4, 0, 12.0), SOOT_D, INK, 3.0)
    a, b = L.p(-2.4, d + 0.4, 12.0), L.p(2.4, d + 0.4, 0)
    bricks(p, (a[0], a[1], b[0], b[1]), SOOT_D, 31, cw=12, ch=5, n=90, lw=0.6)
    p.poly(face(L, -2.6, 2.6, d + 0.35, 11.4, 12.4), STONE, INK, 2.2)
    a, b = L.p(-1.9, d + 0.38, 6.4), L.p(1.9, d + 0.38, 0)
    r_ = (b[0] - a[0]) / 2
    spring = a[1] + r_
    arch = [(a[0] + r_ + r_ * math.cos(u), spring - r_ * math.sin(u)) for u in np.linspace(0, math.pi, 20)]
    ring = [(a[0] + r_ + r_ * 1.2 * math.cos(u), spring - r_ * 1.2 * math.sin(u)) for u in np.linspace(0, math.pi, 20)]
    p.poly([(b[0] + r_ * 0.2, b[1])] + ring + [(a[0] - r_ * 0.2, b[1])], STONE, INK, 2.4)   # the stone ring
    for k in range(1, 12):                                                                  # its voussoirs
        u = math.pi * k / 12
        p.line([(a[0] + r_ + r_ * math.cos(u), spring - r_ * math.sin(u)),
                (a[0] + r_ + r_ * 1.2 * math.cos(u), spring - r_ * 1.2 * math.sin(u))], dk(STONE, 0.8), 1.4)
    gate = [(b[0], b[1])] + arch + [(a[0], b[1])]
    p.poly(gate, TIMBER, INK, 2.8)
    for k in range(1, 9):                                                                    # its planks
        x = a[0] + (b[0] - a[0]) * k / 9
        top = spring - math.sqrt(max(0.0, r_ ** 2 - (x - a[0] - r_) ** 2))
        p.line([(x, top + 4), (x, b[1])], dk(TIMBER, 0.78), 1.6)
    p.line([(a[0] + r_, spring - r_), (a[0] + r_, b[1])], INK, 2.4)                          # the two leaves
    for z in (1.2, 3.6):                                                                    # iron straps, studs
        y = L.p(0, d + 0.38, z)[1]
        p.line([(a[0] + 4, y), (b[0] - 4, y)], (50, 46, 44), 3.0)
    wx0, wx1 = L.p(0.15, d + 0.37, 2.1), L.p(1.15, d + 0.37, 0)
    p.poly(quad(wx0[0], wx0[1], wx1[0], wx1[1]), dk(TIMBER, 0.86), INK, 2.4)                 # the wicket door
    p.ell(wx1[0] - 10, (wx0[1] + wx1[1]) / 2, 4, 4, (180, 170, 140), INK, 1.0)
    # the sign on the wall, left (ref 20), the forecourt, a bollard, a kerb
    a, b = L.p(-10.4, d + 2.9, 3.2), L.p(-6.6, d + 2.9, 1.6)
    p.poly(quad(a[0], a[1], b[0], b[1]), (250, 250, 248), INK, 2.0)
    sign(img, cam, 'HM PRISON', (a[0] + b[0]) / 2, a[1] + (b[1] - a[1]) * 0.32, (b[0] - a[0]) * 0.7, (30, 30, 34))
    sign(img, cam, 'VISITS AND RECEPTION', (a[0] + b[0]) / 2, a[1] + (b[1] - a[1]) * 0.72, (b[0] - a[0]) * 0.8,
         (60, 60, 64))
    g0 = L.p(0, d + 3, 0)[1]
    p.poly(quad(-300, g0, W + 300, 2400), (110, 112, 116), None)                             # tarmac
    for dd in (3.0, 6.0, 9.5):
        y = L.p(0, dd, 0)[1]
        p.line([(-300, y), (W + 300, y + 3)], (100, 102, 106), 2.0)
    r = random.Random(9)
    for _ in range(30):
        dd = r.uniform(2, 14)
        x, y = L.p(r.uniform(-8, 8), dd, 0)
        p.ell(x, y, 60 / dd, 14 / dd, (98, 100, 104), None)
    bl, bt = L.p(-3.4, 9.0, 0), L.p(-3.4, 9.0, 1.0)
    p.poly(quad(bl[0] - 12, bt[1], bl[0] + 12, bl[1]), (230, 196, 40), INK, 2.0)             # the yellow bollard
    p.poly(quad(bl[0] - 12, bt[1] + 20, bl[0] + 12, bt[1] + 30), (40, 40, 40), None)


# ================================================================================================ stage marks
def _mark(L, x, d):
    X, Y = L.p(x, d, 0.0)
    return (X, Y, L.ppm(d))


STAGE = {   # where each person stands: (screen x, ground y, pixels per metre); the shots take these
    'court_out': {'brand': _mark(OUT, 0.45, 3.9), 'press': [(-1.15, 2.5), (-0.45, 2.3), (0.35, 2.45), (1.1, 2.35),
                                                           (1.7, 2.7), (-1.75, 2.8), (-0.8, 3.1), (0.95, 3.2)]},
    'court_box': {'brand': (730, 2140, 520.0), 'judge': (300, 1330, 420.0)},     # judge: neck point's x, seat
    'court_bench': {'judge': (540, 1780, 620.0)},
    'court_dock': {'brand': (560, 2240, 600.0), 'guard1': (190, 1400, 300.0), 'guard2': (900, 1400, 300.0)},
    'van': {'brand': (540, 1600, 760.0)},                                        # seated, bent over
    'cell': {'brand': (760, 1820, 520.0), 'officer': (990, 1760, 500.0)},
    'cell_cot': {'brand': (230, 1700, 560.0)},
    'phone': {'brand': (520, 2500, 820.0)},
    'tvroom': {'brand': (600, 1560, 640.0), 'inmate1': (330, 1560, 600.0), 'inmate2': (870, 1560, 600.0),
               'inmate3': (60, 1560, 560.0)},
    'gates': {'brand': _mark(GATE, 0.6, 4.6), 'press': [(-1.2, 2.3), (-0.4, 2.15), (0.45, 2.4), (1.25, 2.25),
                                                         (1.85, 2.6), (-1.85, 2.7), (-0.9, 3.0), (1.0, 3.1)]},
}
CAMS = {   # a camera on a painting: (view, zoom, centre x, centre y). cell_cot is the cell painting, closer.
    'cell_cot': ('cell', 1.55, 330, 1240),
}


# ================================================================================================ checks
def _box_from(pts):
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    return (min(xs), min(ys), max(xs), max(ys))


def _out_boxes(off):
    L = OUT
    b = lambda x0, x1, d, z0, z1: tuple(v + (off if i % 2 == 0 else 0)
                                        for i, v in enumerate(_box_from(face(L, x0, x1, d, z0, z1))))
    return [('court_out sign band', b(-2.3, 5.3, FACADE_D - 0.7, PLAZA_Z + 2.75, PLAZA_Z + 3.55)),
            ('court_out lamp post', b(-3.95, -3.85, 8.5, 0, 8.0)),
            ('court_out left tree', b(-7.7, -7.5, 12.5, 0, 7.5)),
            ('court_out right tree', b(8.1, 8.3, 13.0, 0, 7.5))]


SET_BOXES = _out_boxes(0) + [
    ('court_box arms', (300 - 124 + 4000, 360 - 210, 300 + 124 + 4000, 360 + 190)),
    ('court_box chair', (130 + 4000, 640, 470 + 4000, 1080)),
    ('court_box bench', (-120 + 4000, 1004, 760 + 4000, 1300)),
    ('court_box witness box', (452 + 4000, 1648, 1080 + 4000, 1920)),
    ('cell window', (440 + 8000, 420, 670 + 8000, 656)),
    ('cell pinboard', (500 + 8000, 700, 690 + 8000, 840)),
    ('cell desk', (470 + 8000, 858, 700 + 8000, 1060)),
    ('cell basin', (760 + 8000, 940, 870 + 8000, 1090)),
    ('cell toilet', (730 + 8000, 1178, 850 + 8000, 1262)),
    ('cell bed', (-300 + 8000, 1110, 380 + 8000, 1800)),
    ('cell door', (890 + 8000, 470, 1140 + 8000, 1800)),
    ('phone hood', (210 + 12000, 380 + PHONE_DY, 800 + 12000, 1040 + PHONE_DY)),
    ('phone notice', (10 + 12000, 440 + PHONE_DY, 200 + 12000, 740 + PHONE_DY)),
    ('phone samaritans', (20 + 12000, 830 + PHONE_DY, 200 + 12000, 1080 + PHONE_DY)),
    ('phone railing', (840 + 12000, -400, 880 + 12000, 2400)),
    ('tvroom window', (90 + 16000, 420, 330 + 16000, 770)),
    ('tvroom door', (420 + 16000, 470, 600 + 16000, 1240)),
    ('tvroom noticeboard', (700 + 16000, 360, 1000 + 16000, 600)),
    ('tvroom pool table', (600 + 16000, 1120, 1080 + 16000, 1320)),
    ('tvroom pool lamp', (740 + 16000, 880, 940 + 16000, 940)),
]
SET_MEANT = [
    ('court_box chair', 'court_box bench', 'the bench stands in front of the judge\'s chair'),
    ('court_box arms', 'court_box chair', 'the arms hang on the wall above and behind the chair back'),
    ('court_box bench', 'court_box witness box', 'the witness box stands 3 m nearer the lens, below the bench'),
    ('cell desk', 'cell pinboard', 'the pinboard hangs on the wall above the desk shelf'),
    ('cell bed', 'cell door', 'never: (the bed is on the left wall, the door on the right)'),
    ('tvroom door', 'tvroom pool lamp', 'never'),
    ('tvroom pool table', 'tvroom pool lamp', 'the lamp hangs over the table'),
    ('phone railing', 'phone hood', 'never'),
]
SET_MEANT = [m for m in SET_MEANT if not m[2].startswith('never')]

BENCHMARK = [
    dict(place='Southwark Crown Court outside', refs=['00-court-exterior-wikimedia.jpg'], at='court_out',
         items=[('buff-orange brick block, long and low', 'done: four floors, scattered brick patches'),
                ('ribbon windows in dark frames, some blinds down', 'done: rows of paired-bar windows'),
                ('dark sign band "CROWN COURT SOUTHWARK" over the entrance', 'done: white caps on a dark band'),
                ('glass doors in a dark recess between brick piers', 'done: three doors, two piers'),
                ('raised forecourt behind low brick walls with planted beds', 'done: two walls, shrubs, coping'),
                ('steps with rails on the left', 'done: six steps, two rails'),
                ('tall lamp post on the pavement', 'done'),
                ('trees at both ends', 'done: autumn, 13 Oct'),
                ('grey slab pavement where the press stand', 'done: joints in perspective, stains')]),
    dict(place='Courtroom: the witness box, judge behind', refs=['07-witness-judge-sketch-cook.jpg',
                                                                 '05-witness-box-sketch-cook.jpg'], at='court_box',
         items=[('pale walls of tall light panels (the sketches\' strokes)', 'done: _panels'),
                ('the judge in red, wig, behind and above, upper left', 'done: chair and bench there; the judge is cast'),
                ('pale oak bench with raised panels', 'done'),
                ('a microphone on a thin stalk at the bench', 'done'),
                ('the witness box: pale oak front and ledge, Brand behind it side-on', 'done: court_box_front'),
                ('a microphone on a stalk at the witness box', 'done'),
                ('the oath Bible on the ledge', 'done'),
                ('the royal arms over the bench (a Crown Court; not in the crop)', 'done: added, simplified')]),
    dict(place='Courtroom: the glass dock', refs=['08-sentencing-sketch-sky.jpg', '11-verdict-bbc.webp'],
         at='court_dock',
         items=[('glass walls round the dock, thin steel uprights, top rail', 'done: court_dock_front'),
                ('pale reflections on the glass', 'done: three diagonal sheens'),
                ('a pale-oak base to the dock, panelled', 'done'),
                ('the defendant standing, waist behind the base', 'done: the stage mark puts his waist there'),
                ('security officers seated behind him', 'done: two marks (cast)'),
                ('pale panelled wall behind', 'done'),
                ('a bench along the back of the dock', 'done'),
                ('flat even courtroom light', 'done: no shading bands')]),
    dict(place='Prison cell', refs=['12-cell-prefab-guardian.jpg', '14-cell-tv-sky.jpg', '13-cell-bunk-bbc.jpg'],
         at='cell',
         items=[('narrow room, cream painted walls', 'done: painted brick courses'),
                ('one barred window high in the back wall', 'done: four bars, the yard'),
                ('metal-framed bed along one wall, thin blue mattress', 'done: left wall'),
                ('green prison blanket', 'done: folded back'),
                ('steel toilet and basin in the corner', 'done: back right'),
                ('shelf-desk, pinboard with papers, a plastic mug', 'done'),
                ('blue steel door with an observation slot', 'done: open on the right'),
                ('the landing beyond the door: railing and safety net', 'done')]),
    dict(place='Prison landing wall phone', refs=['14-cell-tv-sky.jpg', '13-cell-bunk-bbc.jpg'], at='phone',
         items=[('a steel PIN phone with keypad and screen', 'done'),
                ('a blue acoustic hood over it, perforated', 'done'),
                ('a steel cord to the handset at his ear', 'done: PHONE_CORD (the film draws it to his hand)'),
                ('painted brick wall, blue dado', 'done: as the cell (ref 13 blue paint)'),
                ('notices: Samaritans, a general notice', 'done: neutral, no gags'),
                ('landing railing and safety net', 'done: right edge'),
                ('far landing with blue cell doors', 'done'),
                ('flat, institutional light', 'done')]),
    dict(place='Prison gates', refs=['18-gate-wandsworth-sky.jpg', '20-gate-wandsworth-sign-bbc.jpg',
                                     '19-gate-release-guardian.jpg'], at='gates',
         items=[('Victorian gatehouse in dark sooty brick', 'done'),
                ('two square towers either side', 'done: with cornices and plinths'),
                ('tall round arch with a stone ring', 'done: voussoirs'),
                ('timber double gate filling the arch', 'done: planks, iron straps'),
                ('small wicket door cut in the gate (he steps out of it)', 'done: right leaf'),
                ('arched barred windows with stone dressings', 'done: three per tower'),
                ('the long brick wall running off both ways', 'done'),
                ('white "HM Prison" sign on the wall', 'done: neutral, no prison named'),
                ('tarmac forecourt, a yellow bollard, overcast sky', 'done')]),
    dict(place='The van cubicle', refs=['14-cell-tv-sky.jpg'], at='van',
         items=[('tiny cubicle, white moulded walls', 'done: no photo reached us (Sam\'s list)'),
                ('moulded bench seat', 'done'),
                ('small dark tinted window, bars', 'done: right wall'),
                ('street lights sliding past the window', 'done: loops every 1.6 s'),
                ('ceiling light, rivets', 'done'),
                ('ribbed rubber floor', 'done'),
                ('cold dim grey-blue light', 'done: van_front over the cast'),
                ('passing light sweeps over him', 'done: van_front')]),
    dict(place='The TV room', refs=['14-cell-tv-sky.jpg'], at='tvroom',
         items=[('dim association room, two-tone walls', 'done: green dado, cream above; no photo (Sam\'s list)'),
                ('moulded plastic chairs in a row', 'done: four'),
                ('a pool table under its lamp', 'done'),
                ('barred window, dark outside', 'done'),
                ('noticeboard, a door with wired glass', 'done'),
                ('the TV high on a bracket (the reverse shot)', 'done: tv()'),
                ('TV light flickering over everyone', 'done: tv_flicker, a jumping level'),
                ('the BBC-style news on the screen', 'done: studio_feed')]),
]


# ================================================================================================ sheets
VIEWS = ('court_out', 'court_box', 'court_bench', 'court_dock', 'van', 'cell', 'cell_cot', 'phone', 'tvroom', 'tv',
         'gates')
BACK = {'court_out': court_out, 'court_box': court_box, 'court_bench': court_bench, 'court_dock': court_dock,
        'van': van, 'cell': cell, 'phone': phone, 'tvroom': tvroom, 'gates': gates}
MID = {'court_box': court_box_mid}
FRONT = {'court_box': court_box_front, 'court_bench': court_bench_front, 'court_dock': court_dock_front,
         'van': van_front, 'tvroom': lambda img, cam, t: tv_flicker(img, cam, t)}


def view_cam(view):
    if view in CAMS:
        v, z, cx, cy = CAMS[view]
        return v, B.Cam(z, cx, cy)
    return view, B.Cam(1.0)


def back(view, img, cam, t=0.0, feed=None):
    """The painting behind the cast."""
    if view == 'tv':
        tv(img, cam, t, feed)
    else:
        BACK[view](img, cam, t)


def mid(view, img, cam, t=0.0):
    """What stands between the people at the back and those in front (the bench before the judge)."""
    if view in MID:
        MID[view](img, cam, t)


def front(view, img, cam, t=0.0):
    """What the set draws over the cast (the box and bench fronts, the dock glass, the van's and TV's light)."""
    if view in FRONT:
        FRONT[view](img, cam, t)


def painting(view, t=0.0):
    v, cam = view_cam(view)
    img = B.canvas((0, 0, 0))
    back(v, img, cam, t, studio_feed(t, _reader()) if v == 'tv' else None)
    mid(v, img, cam, t)
    front(v, img, cam, t)
    return img


def _reader():
    import blessed_cast as BC
    return dict(BC.NEWSREADER, mood='neutral')


def picture(view):
    return painting(view).resize((W, H), Image.LANCZOS)


def alone(out, cast=True):
    """Every view at phone size (360 x 640 each) on one sheet; with the cast at their marks (blessed.py)."""
    if cast:
        import blessed
        tiles = [(v, blessed.set_still(v)) for v in VIEWS]
    else:
        tiles = [(v, picture(v)) for v in VIEWS]
    cols = 6
    tw, th = 360, 640
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (tw + 10) + 10, rows * (th + 50) + 10), (250, 248, 244))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(SANS, 24)
    for i, (v, im) in enumerate(tiles):
        x, y = 10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 50)
        sheet.paste(im.convert('RGB').resize((tw, th), Image.LANCZOS), (x, y + 40))
        d.text((x, y + 8), v.replace('_', ' '), font=f, fill=(30, 30, 30))
    sheet.save(out, quality=88)
    return out


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'alone':
        print(alone(sys.argv[2], '--bare' not in sys.argv))
    elif cmd == 'one':
        if '--bare' in sys.argv:
            picture(sys.argv[2]).convert('RGB').save(sys.argv[3], quality=90)
        else:
            import blessed
            blessed.set_still(sys.argv[2]).convert('RGB').save(sys.argv[3], quality=90)
        print(sys.argv[3])
