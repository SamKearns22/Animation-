#!/usr/bin/env python3
"""Blessed (Sam, 11 Nov): the sets. Flat paintings in the house style (flat colour, one ink outline, hand-cut
edges), one painting per camera (rule 39), real metres through a level camera (`Level`), drawn fresh from the
references in references/blessed/ (never traced). The cast draw on top through the same B.Cam (world = 1080 x 1920
px at zoom 1), so a push-in is a zoomed camera on the same painting.

MAP (rule 61)
  helpers ........... 40   Level, wob, quad, blob, clump (from remakes_sets), sign (lettering), bricks, window
  court outside ..... 120  court_out: Southwark Crown Court (ref 00): buff brick, the dark sign band, steps, beds
  courtroom ......... 250  court_box (refs 05, 07: witness box, judge behind), court_jury (the reverse onto the jury
                           box, Sam's note 10), court_bench (the gavel close-up, unused since 12 Nov),
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
from ed import INK, curve        # noqa: E402
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
OUT = Level(1.7, 1090.0, 1500.0)    # note 11: lower, amongst the press (was 2.4 m up, horizon 820)
BRICK = (192, 156, 112)                           # buff (ref 00; hunt 1: it read orange)
BRICK_D = (162, 128, 90)
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
    for (xa, xb) in ((-14, -0.9), (3.9, 14)):
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
        a, b = L.p(-0.9, dd, z), L.p(3.9, dd - 0.3, z - PLAZA_Z / 6)
        p.poly(quad(a[0], a[1], b[0], b[1]), mix(PAVE, (255, 255, 255), 0.1 * (k % 2)), INK, 1.6)
    for xr in (-0.6, 3.6):                                                                 # the rails
        pts = [L.p(xr, PLAZA_D0 - 1.8 + 0.3 * k, PLAZA_Z * k / 6 + 0.95) for k in range(7)]
        p.line(pts, (210, 214, 218), 3.4)
        p.line(pts, INK, 1.0)
        for k in (0, 3, 6):
            q = pts[k]
            g = L.p(xr, PLAZA_D0 - 1.8 + 0.3 * k, PLAZA_Z * k / 6)
            p.line([q, g], (210, 214, 218), 2.6)
    # the trees at both ends (autumn, 13 Oct), the lamp post
    for k, (x, dd) in enumerate(((-5.4, 12.5), (6.6, 13.0), (-9.0, 14.0))):
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
    for sg, col, mane in ((-1, (222, 178, 60), (190, 140, 40)), (1, (246, 244, 236), (210, 206, 196))):
        _beast(p, cx + sg * 150 * s, cy + 10 * s, s, sg, col, mane, horn=sg > 0)
    p.poly([(cx - 130 * s, cy + 150 * s), (cx + 130 * s, cy + 150 * s), (cx + 118 * s, cy + 186 * s),
            (cx - 118 * s, cy + 186 * s)], (240, 232, 214), INK, 1.8)                     # the motto scroll
    p.line([(cx - 90 * s, cy + 168 * s), (cx + 90 * s, cy + 168 * s)], (150, 140, 120), 1.4)


def _beast(p, x, y, s, sg, col, mane, horn=False):
    """A supporter of the arms, rearing on its hind legs and facing the shield (sg: -1 the lion on the left, +1 the
    unicorn on the right): body, a raised foreleg on the shield, hind legs on the scroll, head, mane, tail, a horn."""
    q = lambda u, v: (x - sg * u * s, y + v * s)                  # u towards the shield
    p.poly([q(-30, 120), q(-34, 150), q(-14, 152), q(-10, 120)], col, INK, 1.6)       # hind legs
    p.poly([q(10, 120), q(12, 152), q(30, 150), q(26, 118)], col, INK, 1.6)
    p.poly([q(-36, -10), q(20, -40), q(44, 20), q(30, 124), q(-34, 124), q(-44, 40)], col, INK, 2.0)   # body
    p.poly([q(18, -30), q(66, -60), q(74, -44), q(30, -6)], col, INK, 1.6)           # foreleg on the shield
    p.line([q(-40, 100), q(-76, 70), q(-70, 20)], col, 5.0)                          # tail
    p.line([q(-40, 100), q(-76, 70), q(-70, 20)], INK, 1.0)
    p.ell(q(-70, 18)[0], q(-70, 18)[1], 9 * s, 9 * s, mane, INK, 1.0)
    if not horn:   # the lion (hunt 1, 12 Nov: "a dog"): a big shaggy mane all round a round face, a red tongue
        cx, cy = q(34, -78)
        ring = [(cx + (46 + (9 if k % 2 else 0)) * s * math.cos(a), cy + (46 + (9 if k % 2 else 0)) * s * math.sin(a))
                for k, a in enumerate([i * 2 * math.pi / 22 for i in range(22)])]
        p.poly(ring, (176, 112, 36), INK, 1.8)
        p.ell(cx, cy, 27 * s, 29 * s, col, INK, 1.6)                                   # the face
        p.ell(cx - 9 * s, cy - 6 * s, 3 * s, 3 * s, INK, None)
        p.ell(cx + 9 * s, cy - 6 * s, 3 * s, 3 * s, INK, None)
        p.poly([(cx - 6 * s, cy + 4 * s), (cx + 6 * s, cy + 4 * s), (cx, cy + 11 * s)], (120, 70, 40), None)
        p.poly([(cx - 5 * s, cy + 15 * s), (cx + 5 * s, cy + 15 * s), (cx, cy + 27 * s)], (200, 40, 40), INK, 1.0)
        p.poly([(cx - 22 * s, cy - 44 * s), (cx - 12 * s, cy - 64 * s), (cx, cy - 48 * s), (cx + 12 * s, cy - 64 * s),
                (cx + 22 * s, cy - 44 * s)], (222, 178, 60), INK, 1.2)                   # the lion's crown
    else:          # the unicorn (hunt 1: "a goat"): a long horse head, a flowing mane down the neck, a long horn
        p.poly([q(-30, -40), q(-6, -100), q(10, -104), q(-8, -60), q(-22, -10)], mane, INK, 1.6)   # the mane
        p.poly([q(-2, -104), q(22, -112), q(78, -78), q(84, -62), q(70, -54), q(20, -66), q(4, -50)], col, INK, 1.8)
        p.ell(q(28, -92)[0], q(28, -92)[1], 3.4 * s, 3.4 * s, INK, None)
        p.poly([q(2, -110), q(-4, -132), q(12, -114)], col, INK, 1.2)                  # the ear
        hp = [q(22, -110), q(64, -178), q(32, -106)]
        p.poly(hp, (236, 210, 120), INK, 1.4)                                           # the long horn
        for k in (0.3, 0.55, 0.78):
            a0 = (hp[0][0] + (hp[1][0] - hp[0][0]) * k, hp[0][1] + (hp[1][1] - hp[0][1]) * k)
            p.line([(a0[0] - 5 * s, a0[1] + 2 * s), (a0[0] + 5 * s, a0[1] - 2 * s)], INK, 1.0)


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
    p.ell(860, 330, 70, 70, (246, 244, 236), INK, 2.6)                                      # the clock
    for k in range(12):
        a = 2 * math.pi * k / 12
        p.line([(860 + 56 * math.cos(a), 330 + 56 * math.sin(a)), (860 + 64 * math.cos(a), 330 + 64 * math.sin(a))], INK, 2.0)
    p.line([(860, 330), (860, 286)], INK, 3.0)
    p.line([(860, 330), (894, 344)], INK, 3.0)
    p.poly(wob(quad(700, 620, 1000, 1250), 1.4, 12), OAK_D, INK, 2.6)                       # a door in the panelling
    p.poly(quad(730, 660, 970, 900), mix(OAK, OAK_D, 0.4), INK, 1.6)
    p.poly(quad(730, 940, 970, 1210), mix(OAK, OAK_D, 0.4), INK, 1.6)
    p.ell(720, 960, 9, 9, (200, 170, 90), INK, 1.2)
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
    p.poly([(400, 1500), (470, 1520), (470, 2400), (400, 2400)], OAK_D, INK, 2.8)            # the box's near side
    p.poly([(386, 1478), (480, 1500), (480, 1530), (386, 1508)], OAK_L, INK, 2.2)            # and its rail
    p.poly(quad(452, 1668, W + 300, 1706), OAK_L, INK, 2.6)                                 # the ledge
    p.poly(quad(530, 1760, 1000, 2000), OAK_D, INK, 1.8)
    p.poly(quad(540, 1770, 990, 1990), mix(OAK, OAK_D, 0.45), None)
    p.poly([(860, 1668), (1010, 1668), (1020, 1648), (872, 1648)], (40, 36, 34), INK, 1.6)   # the Bible on the ledge
    _mic(p, (520, 1664), (610, 1300), 3.0)


JURY_FRONT_Y = 1690          # the front row's ledge (screen y): over their chests
JURY_BACK_Y = 1420           # the back row's: their own box rail, between the two rows


def court_jury(img, cam, t=0.0):
    """Sam's note 10 (12 Nov): the reverse shot from the witness box onto the jury box across the court: the same
    pale panelled walls (refs 05, 07), tall windows with their blinds half down, a picture rail, the back row's
    high oak bench back; two tiers of six jurors (cast, drawn by the film between this, the mid rail and the front)."""
    p = B.Pen(img, cam)
    _panels(p, -300, -400, W + 300, 1250, 120, 31)
    p.poly(quad(-300, 120, W + 300, 136), dk(WALL, 0.88), INK, 1.4)                         # the picture rail
    for k, x in enumerate((110, 690)):                                                      # two tall windows
        window(p, (x, 230, x + 280, 760), (200, 196, 186), (186, 204, 214), 41 + k, bars=2, blind=(BLIND, 0.45))
    p.poly(wob(quad(450, 300, 630, 900), 1.2, 44), OAK_D, INK, 2.4)                         # a door to the jury room
    p.poly(quad(470, 330, 610, 580), mix(OAK, OAK_D, 0.4), INK, 1.4)
    p.poly(quad(470, 620, 610, 880), mix(OAK, OAK_D, 0.4), INK, 1.4)
    p.ell(600, 600, 7, 7, (200, 170, 90), INK, 1.2)
    p.poly(quad(-300, 930, W + 300, 962), OAK_D, INK, 2.0)                                  # the dado rail
    p.poly(wob(quad(-300, 970, W + 300, 1460), 1.2, 45), OAK, INK, 3.0)                     # the back row's high bench
    for k in range(9):                                                                     # back, in raised panels
        a = -260 + k * 160
        p.poly(quad(a + 14, 1000, a + 146, 1300), mix(OAK, OAK_D, 0.35), INK, 1.4)
    p.poly(quad(-300, 960, W + 300, 990), OAK_L, INK, 2.2)                                  # its top rail


def court_jury_mid(img, cam, t=0.0):
    """The back row's own box front, over their laps, under the front row (and the front row's bench back)."""
    p = B.Pen(img, cam)
    y = JURY_BACK_Y
    p.poly(wob(quad(-300, y, W + 300, 2400), 1.2, 46), OAK, INK, 3.0)
    p.poly(quad(-300, y - 18, W + 300, y + 6), OAK_L, INK, 2.4)                             # the ledge
    for k in range(9):
        a = -260 + k * 160
        p.poly(quad(a + 14, y + 34, a + 146, y + 260), mix(OAK, OAK_D, 0.35), INK, 1.4)
    for x in (130, 560, 930):                                                               # notepads on the ledge
        p.poly([(x, y - 18), (x + 70, y - 18), (x + 80, y - 30), (x + 10, y - 30)], (246, 244, 236), INK, 1.2)


def court_jury_front(img, cam, t=0.0):
    """The front row's box: pale oak front and ledge over their chests; notepads, pens, a water jug and tumblers."""
    p = B.Pen(img, cam)
    y = JURY_FRONT_Y
    p.poly(wob(quad(-300, y, W + 300, 2400), 1.4, 47), OAK, INK, 3.2)
    for k in range(7):
        a = -230 + k * 230
        p.poly(quad(a + 18, y + 50, a + 212, 1960), OAK_D, INK, 1.6)
        p.poly(quad(a + 28, y + 60, a + 202, 1950), mix(OAK, OAK_D, 0.4), None)
    p.poly(quad(-300, y - 26, W + 300, y + 8), OAK_L, INK, 2.6)                             # the ledge
    r = random.Random(48)
    for x in (60, 300, 760, 1000):                                                          # notepads and pens
        x += r.uniform(-20, 20)
        p.poly([(x - 50, y - 26), (x + 50, y - 26), (x + 62, y - 44), (x - 38, y - 44)], (246, 244, 236), INK, 1.4)
        p.line([(x - 20, y - 36), (x + 30, y - 40)], (30, 60, 140), 3.0)
    jx = 540                                                                               # the water jug, tumblers
    p.poly([(jx - 30, y - 26), (jx + 30, y - 26), (jx + 34, y - 100), (jx + 20, y - 118), (jx - 26, y - 116),
            (jx - 34, y - 100)], (214, 228, 234), INK, 2.0)
    p.poly(quad(jx - 28, y - 80, jx + 30, y - 30), (186, 210, 222), None)                   # the water in it
    p.line([(jx + 30, y - 96), (jx + 50, y - 86), (jx + 48, y - 50), (jx + 32, y - 44)], INK, 2.2)   # its handle
    for x in (jx - 74, jx + 80):
        p.poly([(x - 16, y - 26), (x + 16, y - 26), (x + 18, y - 70), (x - 18, y - 70)], (214, 228, 234), INK, 1.6)


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
    gavel_block(p, 760, 1440)
    if t < GAVEL_LIFT[0] or t > GAVEL_LIFT[1]:
        gavel(p, 760, 1404, math.pi)                                                        # resting on the block
    _mic(p, (330, 1446), (450, 1270), 3.0)


GAVEL_LIFT = (-1.0, -1.0)      # the film sets when the judge holds it (blessed.py); otherwise it rests here


def gavel_block(p, x, y):
    """The round sound block: a thick disc of dark wood, its top and its side."""
    p.poly(quad(x - 90, y - 10, x + 90, y + 22), (100, 62, 38), INK, 2.2)
    p.ell(x, y + 22, 90, 20, (100, 62, 38), INK, 2.2)
    p.ell(x, y - 10, 90, 20, (136, 88, 54), INK, 2.2)


def gavel(p, x, y, ang, s=1.0):
    """A gavel: a barrel head with two pale bands, a turned handle; (x, y) the head's middle, ang the handle's
    direction (radians, 0 = to the left)."""
    c, si = math.cos(ang), math.sin(ang)
    hx, hy = x - 150 * s * c, y + 150 * s * si
    p.line([(x, y), (hx, hy)], (120, 76, 44), 12 * s)
    p.line([(x, y), (hx, hy)], INK, 1.4)
    p.ell(hx, hy, 9 * s, 9 * s, (120, 76, 44), INK, 1.4)
    k = lambda u, v: (x + u * s * si + v * s * c, y + u * s * c - v * s * si)      # u along the head, v across
    p.poly([k(-56, -24), k(56, -24), k(56, 24), k(-56, 24)], (110, 66, 40), INK, 2.2)
    for u in (-40, 40):
        p.poly([k(u - 5, -25), k(u + 5, -25), k(u + 5, 25), k(u - 5, 25)], (200, 170, 110), INK, 1.2)
    p.poly([k(-62, -20), k(-56, -20), k(-56, 20), k(-62, 20)], (90, 54, 32), INK, 1.4)
    p.poly([k(56, -20), k(62, -20), k(62, 20), k(56, 20)], (90, 54, 32), INK, 1.4)


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


def court_dock_mid(img, cam, t=0.0):
    """The dock's back bench front, in front of the seated officers' legs, behind Brand."""
    p = B.Pen(img, cam)
    p.poly(wob(quad(-300, 1300, W + 300, 1760), 1.2, 43), OAK_D, INK, 2.6)
    p.poly(quad(-300, 1290, W + 300, 1312), OAK_L, INK, 2.0)
    for k in range(6):
        x = -40 + k * 200
        p.poly(quad(x, 1340, x + 170, 1530), mix(OAK, OAK_D, 0.5), INK, 1.4)


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
    p.poly(wob(quad(150, 1150, 930, 1330), 1.2, 61), mix(VAN_W, VAN_D, 0.5), INK, 2.6)
    p.poly([(150, 1330), (930, 1330), (960, 1560), (120, 1560)], dk(VAN_W, 0.78), INK, 2.4)
    p.poly([(-300, 2400), (100, 1600), (980, 1600), (W + 300, 2400)], (84, 88, 96), INK, 2.4)   # the floor
    for k in range(6):                                                                     # its ribbed rubber
        u = k / 6
        p.line([(100 + (-400) * u * 0, 1640 + 120 * k), (980, 1640 + 120 * k)], (70, 74, 80), 2.0)


def van_front(img, cam, t=0.0):
    """Dim cold light over everyone in the van, the window's passing lights sweeping over them, and the cubicle's
    open steel door frame round the lens (the door leaf on the right with its mesh hatch)."""
    lay = Image.new('RGBA', img.size, (30, 40, 70, 60))
    img.alpha_composite(lay)
    u = (t / 1.6) % 1.0
    soft(img, cam, (900 - 700 * u, 300, 1300 - 700 * u, 1500), (240, 210, 150), 0.10, 120)
    p = B.Pen(img, cam)
    p.poly(quad(-300, -400, 40, 2400), (120, 126, 134), INK, 3.0)                           # the frame, left
    p.poly(quad(-300, -400, W + 300, -40), (120, 126, 134), INK, 3.0)                       # and top
    p.poly([(1010, -40), (W + 300, -400), (W + 300, 2400), (1010, 2100)], (138, 144, 152), INK, 3.0)  # the door leaf
    p.poly([(1030, 500), (W + 300, 440), (W + 300, 820), (1030, 800)], (60, 64, 70), INK, 2.4)        # its hatch
    for k in range(7):
        y = 520 + 42 * k
        p.line([(1030, y), (W + 300, y - 8)], (110, 116, 124), 1.6)
    for k in range(4):
        p.line([(1050 + 18 * k, 500), (1050 + 18 * k, 800)], (110, 116, 124), 1.6)
    p.ell(1060, 1200, 14, 30, (90, 96, 104), INK, 1.6)                                      # the lock


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


def _blanket(p, top, near):
    """Note 17: a prison blanket thrown over the near two-thirds of the mattress, not a flat strip: its edge across
    the bed turned down in a lighter fold, soft rucks along it, and its side hanging over the mattress's room side."""
    (nlx, nly), (flx, fly), (frx, fry), (nrx, nry) = top

    def at(u, v):                                   # u: along the bed (0 near, 1 far); v: across (0 wall, 1 room)
        lx, ly = nlx + (flx - nlx) * u, nly + (fly - nly) * u
        rx, ry = nrx + (frx - nrx) * u, nry + (fry - nry) * u
        return lx + (rx - lx) * v, ly + (ry - ly) * v
    e = 0.62                                        # how far up the bed it reaches
    edge = [at(e + 0.03 * math.sin(7 * v + 1.0), v) for v in (k / 8 for k in range(9))]
    body = [at(0, -0.02)] + edge + [at(e * 0.5, 1.03), at(0, 1.03)]
    hang = [at(0, 1.0), at(e * 0.95, 1.0), (at(e * 0.95, 1.0)[0] + 6, at(e * 0.95, 1.0)[1] + 70),
            (nrx + 10, near - 20), (nrx - 20, near - 4)]
    p.poly(curve(hang, 3), dk(BLANKET, 0.78), INK, 2.2)                     # over the room side
    p.poly(curve(body, 3), BLANKET, INK, 2.4)
    fold = [at(e - 0.07 + 0.02 * math.sin(5 * v), v) for v in (k / 8 for k in range(9))]
    p.poly(curve(edge + fold[::-1], 3), mix(BLANKET, (255, 255, 255), 0.22), INK, 1.8)   # the turned-down edge
    for u, v0, v1 in ((0.2, 0.15, 0.55), (0.36, 0.45, 0.85), (0.12, 0.6, 0.9)):         # rucks where it was thrown
        p.line(curve([at(u, v0), at(u + 0.05, (v0 + v1) / 2), at(u, v1)], 3), dk(BLANKET, 0.72), 2.0)
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
    _blanket(p, [(-300, near - 120), (bx0 - 10, far - 60), (bx0 + 210, far - 50), (380, near - 120)], near)
    p.poly([(bx0 + 10, far - 70), (bx0 + 190, far - 62), (bx0 + 200, far - 38), (bx0 + 20, far - 44)],
           (236, 236, 232), INK, 1.8)                                                       # the pillow
    for x in (-200, 360):                                                                   # the frame's legs
        p.poly(quad(x, near - 40, x + 18, near + 80), (90, 96, 104), INK, 1.6)
    p.poly(quad(bx0 + 196, far - 50, bx0 + 208, far + 20), (90, 96, 104), INK, 1.4)
    # the open blue door on the right wall, the landing beyond it
    dx0, dx1 = 930, 1080
    p.poly([(dx0, 470), (dx1 + 60, 300), (dx1 + 60, 1800), (dx0, 1400)], (76, 80, 90), INK, 2.4)   # the opening
    p.poly([(dx0 + 10, 520), (dx1 + 60, 380), (dx1 + 60, 1000), (dx0 + 10, 1010)], (232, 230, 222), None)  # the landing
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
    """Line 4: the phone room off the landing (Sam's note 20, 12 Nov: "set it in a room, next to another phone
    booth"): painted brick wall and dado all across, two steel PIN phones side by side under blue acoustic hoods
    (his on the left, the empty one on the right), notices between and beside them. The camera sits 200 px right of
    centre (blessed._cam) so he is central and the second booth is in frame."""
    p = B.Pen(img, cam)
    p.poly(quad(-300, -400, W + 700, 2400), CELL, None)
    bricks(p, (-300, -400, W + 700, 2400), CELL, 88, cw=70, ch=30, n=110, lw=1.0)
    for k in range(40):
        y = -380 + k * 60
        p.line([(-300, y), (W + 700, y + 2)], CELL_D, 1.2)
    p.poly(quad(-300, 1500, W + 700, 2400), mix(CELL, DOOR_BLUE, 0.4), INK, 2.0)            # the painted dado
    p.poly(quad(-300, 1490, W + 700, 1512), dk(mix(CELL, DOOR_BLUE, 0.4), 0.8), INK, 1.6)   # its rail
    p.poly(quad(-300, 2200, W + 700, 2400), (120, 112, 100), INK, 2.0)                      # the floor
    p = B.Pen(img, B.Local(cam, 0, PHONE_DY, 1.0))
    for k, dx in enumerate((0, 660)):                                                      # the two booths
        _booth(p, dx, empty=(k == 1))
    sign(img, cam, 'PIN PHONE', 510, 486 + PHONE_DY, 150, (40, 40, 44))
    sign(img, cam, 'PIN PHONE', 1170, 486 + PHONE_DY, 150, (40, 40, 44))
    for k, (x, y, w_, h_, c, txt) in enumerate(((-140, 440, 150, 300, (250, 250, 246), 'NOTICE'),
                                                 (858, 520, 130, 220, (250, 236, 120), 'SAMARITANS'),
                                                 (840, -60, 170, 220, (246, 246, 246), 'CALLS'),
                                                 (1520, 440, 150, 260, (226, 236, 250), 'VISITS'))):
        p.poly(wob(quad(x, y, x + w_, y + h_), 1.0, 70 + k), c, INK, 1.6)
        sign(img, cam, txt, x + w_ / 2, y + 36 + PHONE_DY, w_ * 0.74, (40, 40, 44))
        for j in range(3 if h_ < 240 else 4):
            p.line([(x + 18, y + 80 + j * 36), (x + w_ - 22 - 16 * (j % 2), y + 80 + j * 36)], (150, 150, 150), 2.0)
        p.ell(x + w_ / 2, y + 10, 5, 5, (200, 40, 40), INK, 1.0)                          # a drawing pin


def _booth(p, dx, empty=False):
    """One wall phone under its blue acoustic hood (the hood's back, two cheeks, the canopy, perforations), dx to the
    right of his. empty: the handset sits in its cradle and its cord coils below it."""
    q = lambda x0, y0, x1, y1: quad(x0 + dx, y0, x1 + dx, y1)
    p.poly(q(250, 380, 760, 1040), (214, 214, 208), INK, 2.4)                               # the hood's back
    p.poly([(250 + dx, 380), (180 + dx, 300), (180 + dx, 1120), (250 + dx, 1040)], (50, 84, 136), INK, 2.8)
    p.poly([(760 + dx, 380), (830 + dx, 300), (830 + dx, 1120), (760 + dx, 1040)], (60, 96, 150), INK, 2.8)
    p.poly([(180 + dx, 300), (830 + dx, 300), (760 + dx, 380), (250 + dx, 380)], (44, 76, 126), INK, 2.8)
    p.poly(q(250, 380, 760, 430), (180, 180, 176), None)                                    # the shadow under it
    for k in range(9):                                                                     # its perforations
        for j in range(5):
            p.ell(300 + dx + k * 50, 450 + j * 120, 3, 3, (186, 186, 180), None)
    p.poly(wob(q(420, 520, 600, 860), 1.0, 5 + dx), STEEL, INK, 2.6)                        # the PIN phone
    for k in range(4):                                                                     # its keypad
        for j in range(3):
            p.poly(q(470 + j * 30, 660 + k * 34, 494 + j * 30, 686 + k * 34), (230, 232, 234), INK, 1.0)
    p.poly(q(450, 560, 570, 620), (40, 60, 50), INK, 1.4)                                   # its little screen
    p.poly(q(404, 540, 426, 760), (120, 124, 128), INK, 1.4)                                # the cradle
    p.poly(q(408, 548, 422, 752), (60, 62, 66), None)
    p.poly(q(500, 860, 520, 900), (150, 156, 160), INK, 1.4)                                # where the cord leaves
    if empty:                                                                              # its handset, hung up
        p.poly(wob(q(388, 520, 436, 790), 0.8, 9), (40, 42, 46), INK, 2.2)
        cord = [(510 + dx, 900)] + [(520 + dx + 26 * math.sin(k * 1.3), 930 + k * 14) for k in range(12)] + \
               [(436 + dx, 1000), (412 + dx, 790)]
        p.line(cord, (150, 156, 162), 6.0)
        p.line(cord, INK, 1.0)


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
    for k in range(3):                                                                     # a high strip of small
        x = 40 + 130 * k                                                                   # barred windows, night
        window(p, (x, 260, x + 100, 380), (90, 96, 104), (40, 52, 90), 11 + k, bars=3, lw=2.0)
    p.poly(wob(quad(700, 400, 1010, 640), 0.8, 21), (150, 112, 74), INK, 2.4)                 # a cork noticeboard
    r = random.Random(23)
    for k in range(7):                                                                     # its pinned sheets
        x, y = 720 + (k % 4) * 70 + r.uniform(-6, 6), 420 + (k // 4) * 110 + r.uniform(-6, 6)
        p.poly(wob(quad(x, y, x + 58, y + 80), 0.6, 30 + k), ((240, 238, 228), (250, 236, 150), (220, 230, 240))[k % 3],
               INK, 1.2)
        for q in range(3):
            p.line([(x + 8, y + 20 + 16 * q), (x + 48, y + 20 + 16 * q)], (150, 150, 150), 1.2)
        p.ell(x + 29, y + 6, 4, 4, (200, 40, 40), None)
    p.ell(220, 620, 60, 60, (240, 238, 230), INK, 2.4)                                      # a caged wall clock
    p.line([(220, 620), (220, 584)], INK, 2.6)
    p.line([(220, 620), (248, 628)], INK, 2.6)
    for k in range(5):
        p.line([(160 + 30 * k, 562), (160 + 30 * k, 678)], (90, 96, 104), 1.6)
    p.poly(quad(420, 470, 600, 1240), (110, 112, 116), INK, 2.4)                             # the door
    p.poly(quad(450, 520, 570, 700), (60, 70, 86), INK, 1.6)                                 # its wired glass
    for k in range(6):
        p.line([(450 + 20 * k, 520), (450 + 20 * k, 700)], (90, 100, 116), 1.0)
        p.line([(450, 520 + 30 * k), (570, 520 + 30 * k)], (90, 100, 116), 1.0)
    p.poly(quad(-300, 1240, W + 300, 2400), (104, 98, 90), None)                            # the lino
    for k in range(10):
        y = 1260 + k * 60 * (1 + k * 0.15)
        p.line([(-300, y), (W + 300, y)], (94, 88, 80), 1.6)
    # the pool table at the back right (pool_table; the film draws it again over the man bent over it), its lamp
    pool_table(p)
    # chat 5 (the hard critique: 'a lamp over nothing'): the lamp hangs low over the cloth's middle on a long cord,
    # its light falling in a pool on the table
    p.line([(840, -400), (840, 1010)], (40, 40, 44), 3.0)                                   # (3 m nearer than the
    p.poly([(780, 1010), (900, 1010), (930, 1052), (750, 1052)], (74, 78, 84), INK, 2.2)     # board: its cord
    #                                                                                        crosses in front)
    p.poly([(770, 1046), (910, 1046), (918, 1056), (762, 1056)], (250, 236, 180), None)
    soft(img, cam, (660, 1080, 1020, 1220), (255, 240, 190), 0.3, 60)                       # its light on the cloth
    # Sam's note 22: moulded plastic chairs (adult wings: heavy-duty, wipe-clean), not a bench. Chat 5: the chairs
    # are drawn with the people now (sitting.Seat('plastic')), so the seat shows round them from every view


def pool_table(p, front_only=False):
    """The pool table at the back right: green cloth, wooden rails and legs, three balls (front_only: the near
    rail and legs, drawn again over the man standing behind it)."""
    if not front_only:
        p.poly([(640, 1120), (1040, 1120), (1080, 1210), (600, 1210)], (40, 110, 70), INK, 2.4)
    p.poly(quad(600, 1210, 1080, 1260), (90, 60, 40), INK, 2.0)
    for x in (630, 1050):
        p.poly(quad(x - 10, 1260, x + 10, 1320), (90, 60, 40), INK, 1.6)
    if front_only:
        return
    for x, y in ((644, 1124), (840, 1122), (1036, 1124), (606, 1206), (840, 1208), (1074, 1206)):   # the pockets
        p.ell(x, y, 11, 6, (20, 20, 22), None)                                               # (critique: 'a desk')
    for k, x in enumerate((700, 760, 990)):                                                 # balls
        p.ell(x, 1150, 9, 6, ((200, 40, 40), (240, 200, 60), (240, 240, 240))[k], INK, 1.0)


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
    lay = Image.new('RGBA', img.size, (8, 16, 60, int(34 * strength)))                   # the room gone blue-dark
    img.alpha_composite(lay)                       # (chat 5: lighter, and a weaker glow: the picture read washed out)
    soft(img, cam, (-100, 400, 1180, 1300), (120, 170, 255), 0.16 * k, 220)                # the blue glow on their
    #                                                                                        faces, from above


def tv(img, cam, t=0.0, feed=None):
    """The TV on its wall bracket, high in the corner, the news on it (feed: an RGBA picture, 16:9)."""
    p = B.Pen(img, cam)
    wall = dk(TV_CREAM, 0.72)
    p.poly(quad(-300, -400, W + 300, 2400), wall, None)
    bricks(p, (-300, -400, W + 300, 2400), wall, 101, cw=60, ch=26, n=70, lw=0.9)
    p.poly(quad(-300, 1700, W + 300, 2400), dk(TV_GREEN, 0.72), INK, 2.2)                   # the green dado
    p.poly(quad(-300, 1690, W + 300, 1706), dk(TV_GREEN, 0.5), INK, 1.4)                   # and its rail
    p.poly(quad(440, 420, 640, 470), (70, 72, 78), INK, 2.0)                                 # the wall plate
    for x in (460, 620):
        p.ell(x, 445, 6, 6, (140, 144, 150), INK, 1.0)                                       # its bolts
    p.poly(quad(500, 470, 580, 900), (50, 52, 56), INK, 2.0)                                 # the bracket arm
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
    cm = S3.Cam((0.0, 1.16, -0.6), (0.0, 1.10, 4.15), focal=1500)     # a mid shot: desk, him, the screen
    people = None
    if reader is not None:
        px, pz = ND.PRESENTER_AT
        people = [(px, pz + 0.05, lambda im, c: ND.put_seated(im, c, reader, px, pz, 180.0, t))]
    ND.render(img, cm, people)
    B.SS = keep
    y0 = 960 - 260
    crop = img.crop((0, y0, 1080, y0 + 608)).resize(size, Image.LANCZOS)
    a = np.asarray(crop).astype(np.int16).copy()                 # the studio's remaining blues (the swirl, the
    r, g, b = a[..., 0], a[..., 1], a[..., 2]                    # newsroom screens) turned BBC red
    m = (b > r + 70) & (b > g)                                  # (not his navy suit)
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
                     DESK_BLUE=(170, 20, 26), DESK_LIGHT=(206, 36, 42), DESK_TOP=(236, 232, 232),
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
GATE = Level(2.4, 1150.0, 1100.0)    # the camera as at the court
SOOT = (88, 80, 74)
SOOT_D = (66, 60, 56)
STONE = (186, 160, 128)              # the sandstone dressings, warm (ref 18)
STONE_D = (70, 64, 60)               # the dark rusticated pilasters and plinths
TIMBER = (120, 80, 52)
FRAME = (130, 60, 40)                # the red-brown window frames
GATE_D = 9.0                         # close enough that he reads at the wicket (critique: he was tiny at 18 m)


def _rustic(p, L, x0, x1, d, z0, z1, step=0.62):
    """A rusticated stone pilaster: big dark blocks, each outlined, a deeper course every other one."""
    p.poly(face(L, x0, x1, d, z0, z1), STONE_D, INK, 2.4)
    k = 0
    for z in np.arange(z0, z1 - 0.05, step):
        inset = 0.06 if k % 2 else 0.0
        p.poly(face(L, x0 + inset, x1 - inset, d - 0.02, z + 0.04, min(z1, z + step) - 0.04), dk(STONE_D, 1.1 if k % 2
               else 0.95), INK, 1.2)
        k += 1


def _arched_window(p, L, xc, d, z0, z1, w=1.0):
    """A tall round-headed window: a stone surround and hood, red-brown frame, small panes (ref 18)."""
    a, b = L.p(xc - w / 2, d, z1), L.p(xc + w / 2, d, z0)
    r_ = (b[0] - a[0]) / 2
    cx_, spring = a[0] + r_, a[1] + r_
    def head(rr, n=14):
        return [(cx_ + rr * math.cos(u), spring - rr * math.sin(u)) for u in np.linspace(0, math.pi, n)]
    m = r_ * 0.38
    p.poly([(b[0] + m, b[1] + m * 0.6)] + head(r_ + m) + [(a[0] - m, b[1] + m * 0.6)], STONE, INK, 2.0)
    p.poly([(b[0], b[1])] + head(r_) + [(a[0], b[1])], FRAME, INK, 2.0)
    mm = r_ * 0.16
    glass = [(b[0] - mm, b[1] - mm)] + head(r_ - mm) + [(a[0] + mm, b[1] - mm)]
    p.poly(glass, (58, 66, 80), None)
    for k in (1, 2):
        x = a[0] + (b[0] - a[0]) * k / 3
        p.line([(x, a[1] + r_ * 0.2), (x, b[1] - mm)], FRAME, 2.0)
    for y in np.arange(spring + r_ * 0.5, b[1] - mm, r_ * 0.55):
        p.line([(a[0] + mm, y), (b[0] - mm, y)], FRAME, 1.8)
    p.poly(quad(a[0] - m, b[1], b[0] + m, b[1] + m * 0.7), STONE, INK, 1.6)               # the sill
    p.poly(quad(cx_ - m * 0.6, a[1] - m * 1.2, cx_ + m * 0.6, a[1] + m * 0.3), STONE, INK, 1.4)   # the keystone


def gates(img, cam, t=0.0):
    """HMP Wandsworth's gatehouse (ref 18): a wide sooty-brick front, two towers either side of a lower centre block,
    each tower edged with dark rusticated pilasters; a sandstone round arch with a square iron grille above a plain
    timber double gate (the wicket door cut in it, open); round-headed windows with red-brown frames; heavy cornices;
    yellow bollards either side of the gate; a white 'HM PRISON' sign on posts in the forecourt."""
    p = B.Pen(img, cam)
    L = GATE
    d = GATE_D
    p.poly(quad(-300, -800, W + 300, 1200), (214, 216, 220), None)                          # pale overcast
    for k, (x, y, rx) in enumerate(((240, 140, 260), (820, 60, 300))):
        p.poly(blob(x, y, rx, 50, 10, 0.12, 60 + k), (226, 228, 232) if k % 2 else (198, 202, 208), None)
    # the centre block (set back a little), its cornice
    p.poly(face(L, -2.45, 2.45, d + 0.3, 0, 9.8), SOOT_D, INK, 3.0)   # wide enough to meet the towers
    a, b = L.p(-2.3, d + 0.3, 9.8), L.p(2.3, d + 0.3, 0)
    bricks(p, (a[0], a[1], b[0], b[1]), SOOT_D, 31, cw=10, ch=4, n=140, lw=0.6)
    p.poly(face(L, -2.5, 2.5, d + 0.25, 8.4, 9.0), STONE, INK, 2.0)                          # the frieze
    for x in np.arange(-2.3, 2.3, 0.32):                                                    # its brackets
        p.poly(face(L, x, x + 0.14, d + 0.22, 8.5, 8.9), dk(STONE, 0.8), INK, 1.0)
    p.poly(face(L, -2.7, 2.7, d + 0.2, 9.0, 9.8), STONE_D, INK, 2.4)                         # the cornice
    # the two towers, nearer, each with two rusticated pilasters, windows between, a heavy cornice
    for sx in (-1, 1):
        x0, x1 = (-5.3, -2.3) if sx < 0 else (2.3, 5.3)
        p.poly(face(L, x0, x1, d, 0, 12.0), SOOT, INK, 3.0)
        a, b = L.p(x0, d, 12.0), L.p(x1, d, 0)
        bricks(p, (a[0], a[1], b[0], b[1]), SOOT, 20 + sx, cw=10, ch=4, n=160, lw=0.6)
        for px0 in (x0, x1 - 0.7):
            _rustic(p, L, px0, px0 + 0.7, d - 0.1, 1.4, 11.0)
            p.poly(face(L, px0 - 0.15, px0 + 0.85, d - 0.15, 0, 1.4), STONE_D, INK, 2.4)    # its plinth
            p.poly(face(L, px0 - 0.1, px0 + 0.8, d - 0.13, 1.25, 1.45), dk(STONE_D, 1.2), INK, 1.4)
        xc = (x0 + x1) / 2
        for zb in (1.6, 5.2, 8.6):
            _arched_window(p, L, xc, d - 0.02, zb, zb + 2.1, 0.9)
        p.poly(face(L, x0 - 0.3, x1 + 0.3, d - 0.2, 11.0, 12.0), STONE_D, INK, 2.6)          # the cornice
        for x in np.arange(x0 - 0.2, x1 + 0.2, 0.36):
            p.poly(face(L, x, x + 0.16, d - 0.18, 10.6, 11.0), dk(STONE, 0.8), INK, 1.0)
    # the arch: stone jambs and voussoirs, a keystone, the square grille above a plain timber gate
    sp_z, hw = 4.2, 1.4
    a, b = L.p(-hw, d + 0.28, sp_z), L.p(hw, d + 0.28, 0)
    r_ = (b[0] - a[0]) / 2
    cx_, spring = a[0] + r_, a[1]
    ro = r_ * 1.36
    jl, jr = L.p(-hw - 0.5, d + 0.28, 0), L.p(hw + 0.5, d + 0.28, 0)
    p.poly([(jr[0], jr[1])] + [(cx_ + ro * math.cos(u), spring - ro * math.sin(u)) for u in np.linspace(0, math.pi, 24)]
           + [(jl[0], jl[1])], STONE, INK, 2.6)                                              # the stone surround
    for k in range(1, 13):                                                                  # voussoirs
        u = math.pi * k / 13
        p.line([(cx_ + r_ * math.cos(u), spring - r_ * math.sin(u)),
                (cx_ + ro * math.cos(u), spring - ro * math.sin(u))], dk(STONE, 0.72), 1.8)
    for z in np.arange(0.5, sp_z, 0.55):                                                    # the jambs' blocks
        for sx in (-1, 1):
            y = L.p(0, d + 0.28, z)[1]
            x_in, x_out = L.p(sx * hw, d, 0)[0], L.p(sx * (hw + 0.5), d, 0)[0]
            p.line([(x_in, y), (x_out, y)], dk(STONE, 0.72), 1.6)
    p.poly([(cx_ - r_ * 0.16, spring - ro - 10), (cx_ + r_ * 0.16, spring - ro - 10), (cx_ + r_ * 0.12, spring - r_ + 4),
            (cx_ - r_ * 0.12, spring - r_ + 4)], STONE, INK, 2.2)                            # the keystone
    head = [(cx_ + r_ * math.cos(u), spring - r_ * math.sin(u)) for u in np.linspace(0, math.pi, 24)]
    p.poly(head, (34, 32, 32), INK, 2.4)                                                     # the grille: dark,
    gx = np.linspace(a[0], b[0], 13)
    for x in gx[1:-1]:                                                                       # a square iron grid
        top = spring - math.sqrt(max(0.0, r_ ** 2 - (x - cx_) ** 2))
        p.line([(x, top + 2), (x, spring)], (130, 120, 108), 2.2)
    for y in np.arange(spring - (gx[1] - gx[0]), spring - r_, -(gx[1] - gx[0])):
        half = math.sqrt(max(0.0, r_ ** 2 - (spring - y) ** 2))
        p.line([(cx_ - half + 2, y), (cx_ + half - 2, y)], (130, 120, 108), 2.2)
    p.poly(quad(a[0], spring, b[0], b[1]), TIMBER, INK, 2.8)                                 # the timber gate
    p.poly(quad(a[0], spring - 4, b[0], spring + 8), (50, 40, 34), INK, 1.6)                 # its head rail
    for k in range(1, 16):
        x = a[0] + (b[0] - a[0]) * k / 16
        p.line([(x, spring + 8), (x, b[1])], dk(TIMBER, 0.8), 1.4)
    p.line([(cx_, spring + 8), (cx_, b[1])], INK, 2.4)                                       # the two leaves
    wx0, wx1 = L.p(0.15, d + 0.27, 2.1), L.p(1.15, d + 0.27, 0)
    p.poly(quad(wx0[0], wx0[1], wx1[0], wx1[1]), (24, 22, 22), INK, 2.4)                     # the wicket door, open:
    p.poly(quad(wx0[0] + 4, wx1[1] - 20, wx1[0] - 4, wx1[1]), (70, 66, 60), None)            # the yard beyond
    p.poly([(wx1[0], wx0[1]), (wx1[0] + 26, wx0[1] + 10), (wx1[0] + 26, wx1[1] + 4), (wx1[0], wx1[1])],
           dk(TIMBER, 0.86), INK, 2.2)                                                       # its leaf, swung out
    # the forecourt: tarmac, a kerb line, the yellow bollards either side of the gate, the sign on its posts
    g0 = L.p(0, d + 0.3, 0)[1]
    p.poly(quad(-300, g0, W + 300, 2400), (110, 112, 116), None)
    p.poly(quad(-300, g0 - 4, W + 300, g0 + 6), (90, 90, 94), INK, 1.2)
    for dd in (3.0, 5.5):
        y = L.p(0, dd, 0)[1]
        p.line([(-300, y), (W + 300, y + 3)], (100, 102, 106), 2.0)
    r = random.Random(9)
    for _ in range(26):
        dd = r.uniform(2, d - 0.5)
        x, y = L.p(r.uniform(-5, 5), dd, 0)
        p.ell(x, y, 60 / dd, 14 / dd, (98, 100, 104), None)
    for sx in (-1, 1):
        bl, bt = L.p(sx * 1.75, d - 0.4, 0), L.p(sx * 1.75, d - 0.4, 0.9)
        w_ = L.ppm(d - 0.4) * 0.12
        p.poly(quad(bl[0] - w_, bt[1], bl[0] + w_, bl[1]), (230, 196, 40), INK, 2.0)
        p.ell(bl[0], bt[1], w_, w_ * 0.4, (240, 210, 70), INK, 1.4)
    a, b = L.p(-3.3, d - 1.6, 2.7), L.p(-1.9, d - 1.6, 1.95)                                  # the sign (ref 20; nearer the gate so it stays whole in frame, hunt 2)
    for x in (a[0] + 10, b[0] - 10):
        gy = L.p(0, d - 1.6, 0)[1]
        p.poly(quad(x - 4, b[1], x + 4, gy), (60, 62, 66), INK, 1.2)
    p.poly(quad(a[0], a[1], b[0], b[1]), (250, 250, 248), INK, 2.0)
    sign(img, cam, 'HM PRISON', (a[0] + b[0]) / 2, a[1] + (b[1] - a[1]) * 0.34, (b[0] - a[0]) * 0.74, (30, 30, 34))
    sign(img, cam, 'VISITS AND RECEPTION', (a[0] + b[0]) / 2, a[1] + (b[1] - a[1]) * 0.74, (b[0] - a[0]) * 0.82,
         (60, 60, 64))


# ---- cot_top (Sam's note 18, 12 Nov): looking straight down on the cot; he lies flat on his back, the Bible beside
#      him on the sheet. Seen from above a man on his back is drawn as a man standing front-on (the house style's
#      front view), so the bed is laid out down the screen: the pillow at the top, the blanket over him from the waist.
COT_BED = (160, 280, 920, 1980)                    # the mattress (screen px at zoom 1)
COT_BLANKET_Y = 1330                               # the blanket's turned-down edge


def cot_top(img, cam, t=0.0):
    p = B.Pen(img, cam)
    p.poly(quad(-300, -400, W + 300, 2400), CELL_FLOOR, None)
    for k in range(-2, 9):                                                          # the floor's tiles
        p.line([(-300, 120 + k * 260), (W + 300, 150 + k * 260)], dk(CELL_FLOOR, 0.92), 1.4)
    x0, y0, x1, y1 = COT_BED
    p.poly(quad(x0 - 34, y0 - 40, x1 + 34, y1 + 40), STEEL, INK, 2.6)                # the steel frame
    p.poly(quad(x0, y0, x1, y1), MATT, INK, 2.4)                                     # the thin blue mattress
    p.poly(curve([(x0 + 150, y0 + 40), (x1 - 150, y0 + 34), (x1 - 130, y0 + 290), (x0 + 130, y0 + 296)], 2),
           (236, 234, 226), INK, 2.4)                                                 # the flat pillow
    p.line([(x0 + 80, y0 + 170), (x0 + 150, y0 + 178)], (206, 204, 196), 2.0)        # a crease in it
    bx, by = 845, 1120                                                                 # the Bible on the sheet, by his hand
    pts = [(bx - 62, by - 88), (bx + 58, by - 80), (bx + 66, by + 86), (bx - 54, by + 92)]
    p.poly(pts, (40, 36, 40), INK, 2.4)
    p.line([(bx - 46, by - 74), (bx - 40, by + 80)], (70, 64, 66), 2.0)               # the spine's edge
    g = (214, 176, 70)
    p.poly([(bx - 2, by - 40), (bx + 8, by - 40), (bx + 11, by + 34), (bx + 1, by + 34)], g, None)
    p.poly([(bx - 22, by - 16), (bx + 30, by - 13), (bx + 30, by - 4), (bx - 22, by - 7)], g, None)


def cot_top_front(img, cam, t=0.0):
    """The blanket over him from the waist down (drawn over the cast), its edge turned down, his feet two bumps."""
    p = B.Pen(img, cam)
    x0, y0, x1, y1 = COT_BED
    e = COT_BLANKET_Y
    p.poly([(x0 - 14, e + 10), (x0 + 120, e - 8), (x1 - 140, e - 4), (x1 + 14, e + 14), (x1 + 22, y1 + 30),
            (x0 - 22, y1 + 30)], BLANKET, INK, 2.4)
    p.poly([(x0 - 14, e + 10), (x0 + 120, e - 8), (x1 - 140, e - 4), (x1 + 14, e + 14), (x1 + 10, e + 80),
            (x0 - 8, e + 74)], (232, 230, 222), INK, 2.2)                    # the sheet folded over it
    for fx, fy in ((-120, 360), (60, 520), (-40, 700)):                                # folds over his legs
        p.line(curve([(540 + fx, e + fy), (540 + fx + 40, e + fy + 60), (540 + fx + 30, e + fy + 160)], 3),
               dk(BLANKET, 0.8), 2.0)
    for fx in (-70, 70):                                                               # his feet under it
        p.poly(curve([(540 + fx - 52, y1 - 150), (540 + fx, y1 - 196), (540 + fx + 52, y1 - 150),
                      (540 + fx + 44, y1 - 100), (540 + fx - 44, y1 - 100)], 3), mix(BLANKET, (255, 255, 255), 0.08),
               INK, 2.0)


# ================================================================================================ stage marks
def _mark(L, x, d):
    X, Y = L.p(x, d, 0.0)
    return (X, Y, L.ppm(d))


def press_spots(bx, bd, rows, seed, cx=0.0, half=1.6, gap=0.5, step=0.5):
    """A press pack round his mark (notes 12 and 24, 'tons of press'): rows of people at the depths in `rows`, spread
    across the picture (cx, half: the picture's centre and half-width in metres at his depth, scaled by depth) about `step`
    apart, jittered, with a gap on the line from the lens to him so the pack never hides him."""
    rng = np.random.default_rng(seed)
    out = []
    for d in rows:
        line, c = bx * d / bd, cx * d / bd
        w = half * d / bd + 0.3                    # a little past the frame's edges: cut-off shoulders, amongst them
        x = c - w + rng.uniform(0, step)
        while x < c + w:
            g = 0.45 if d > bd else gap * (0.55 + 0.45 * d / bd) + 0.3 * (bd - d) / bd   # behind him: beside his head only
            if bd - 0.6 < d <= bd + 0.1:
                g = max(g, 0.85)                     # level with him: room for his arms flung wide
            if abs(x - line) > g:
                out.append((round(x, 2), round(d + rng.uniform(-0.12, 0.12), 2)))
            x += step * rng.uniform(0.85, 1.2)
    return out


STAGE = {   # where each person stands: (screen x, ground y, pixels per metre); the shots take these
    'court_out': {'brand': _mark(OUT, 0.45, 3.9), 'press': press_spots(0.45, 3.9, (3.4, 3.0, 2.6), 7, cx=0.26, half=1.25, gap=0.4, step=0.45)},
    'court_box': {'brand': (720, 2240, 600.0), 'judge': (300, 1330, 420.0)},     # judge: neck point's x, seat
    'court_bench': {'judge': (540, 1780, 620.0)},
    'court_jury': {'back': [(30 + 206 * k, 1643, 380.0) for k in range(6)],      # seated: feet on each tier
                   'front': [(-60 + 240 * k, 1945, 430.0) for k in range(6)]},
    'court_dock': {'brand': (560, 2240, 600.0), 'guard1': (170, 1540, 400.0), 'guard2': (910, 1540, 400.0)},
    'van': {'brand': (540, 1600, 760.0)},                                        # seated, bent over
    'cell': {'brand': (600, 1820, 520.0), 'officer': (1000, 1700, 480.0)},
    'cell_cot': {'brand': (230, 1700, 560.0)},
    'cot_top': {'brand': (540, 1800, 740.0)},        # lying: drawn as standing front-on, seen from above
    'phone': {'brand': (690, 2500, 820.0)},
    'tvroom': {'brand': (540, 1770, 700.0), 'inmate1': (190, 1330, 300.0), 'inmate2': (960, 1290, 250.0)},
    #          chat 5: Brand nearer and lower (no empty floor under him); the pool player at the table's right end
    #          note 22: Brand alone near; the sleeper behind left; the pool player behind the table, right
    'gates': {'brand': _mark(GATE, 0.6, 7.6),       # the pack crowds the gate in a horseshoe (Sam, 11 Nov)
              'press': press_spots(0.6, 7.6, (7.3, 6.7, 6.1, 5.5, 4.9), 11, cx=0.15, half=2.3, step=0.6)},
}
CAMS = {   # a camera on a painting: (view, zoom, centre x, centre y). cell_cot is the cell painting, closer.
    'cell_cot': ('cell', 1.55, 330, 1240),
    'gates2': ('gates', 1.9, 0.0, 0.0),           # closer on his mark (set below, from STAGE)
}

CAMS['gates2'] = ('gates', 1.9, STAGE['gates']['brand'][0], STAGE['gates']['brand'][1] - 0.95 * STAGE['gates']['brand'][2])


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
            ('court_out left tree', b(-5.5, -5.3, 12.5, 0, 7.5)),
            ('court_out right tree', b(6.5, 6.7, 13.0, 0, 7.5))]


SET_BOXES = _out_boxes(0) + [
    ('court_box arms', (300 - 124 + 4000, 360 - 210, 300 + 124 + 4000, 360 + 190)),
    ('court_box chair', (130 + 4000, 640, 470 + 4000, 1080)),
    ('court_box bench', (-120 + 4000, 1004, 760 + 4000, 1300)),
    ('court_box witness box', (386 + 4000, 1478, 1080 + 4000, 1920)),
    ('court_box clock', (790 + 4000, 260, 930 + 4000, 400)),
    ('court_box door', (700 + 4000, 620, 1000 + 4000, 1250)),
    ('cell window', (440 + 8000, 420, 670 + 8000, 656)),
    ('cell pinboard', (500 + 8000, 700, 690 + 8000, 840)),
    ('cell desk', (470 + 8000, 858, 700 + 8000, 1060)),
    ('cell basin', (760 + 8000, 940, 870 + 8000, 1090)),
    ('cell toilet', (730 + 8000, 1178, 850 + 8000, 1262)),
    ('cell bed', (-300 + 8000, 1110, 380 + 8000, 1800)),
    ('cell door', (890 + 8000, 470, 1140 + 8000, 1800)),
    ('phone hood', (180 + 12000, 300 + PHONE_DY, 830 + 12000, 1120 + PHONE_DY)),
    ('phone notice', (14 + 12000, 440 + PHONE_DY, 164 + 12000, 740 + PHONE_DY)),
    ('phone samaritans', (14 + 12000, 830 + PHONE_DY, 164 + 12000, 1080 + PHONE_DY)),
    ('phone railing', (840 + 12000, -400, 880 + 12000, 2400)),
    ('tvroom windows', (40 + 16000, 260, 400 + 16000, 390)),
    ('tvroom clock', (160 + 16000, 560, 280 + 16000, 680)),
    ('tvroom door', (420 + 16000, 470, 600 + 16000, 1240)),
    ('tvroom cue rack', (720 + 16000, 380, 1000 + 16000, 910)),
    ('tvroom pool table', (600 + 16000, 1120, 1080 + 16000, 1320)),
    ('tvroom pool lamp', (740 + 16000, 1000, 940 + 16000, 1050)),
    # chat 3 (rule 59: the sets with no boxes were never checked). The dock is all full-width bands (rails, panels,
    # glass), no separate objects to overlap.
    ('court_jury left window', (110 + 20000, 230, 390 + 20000, 760)),
    ('court_jury door', (450 + 20000, 300, 630 + 20000, 900)),
    ('court_jury right window', (690 + 20000, 230, 970 + 20000, 760)),
    ('van ceiling light', (420 + 24000, 14, 660 + 24000, 66)),
    ('van sticker', (250 + 24000, 300, 330 + 24000, 380)),
    ('van air vent', (480 + 24000, 560, 610 + 24000, 610)),
    ('van grab rail', (170 + 24000, 700, 186 + 24000, 1000)),
    ('van window', (940 + 24000, 360, 1040 + 24000, 700)),
] + [('gates ' + n, tuple(v + (28000 if i % 2 == 0 else 0) for i, v in enumerate(_box_from(q)))) for n, q in (
    ('left tower', face(GATE, -5.3, -2.3, GATE_D, 0, 12.0)), ('right tower', face(GATE, 2.3, 5.3, GATE_D, 0, 12.0)),
    ('centre block', face(GATE, -2.45, 2.45, GATE_D + 0.3, 0, 9.8)),
    ('left bollard', face(GATE, -1.87, -1.63, GATE_D - 0.4, 0, 0.9)),
    ('right bollard', face(GATE, 1.63, 1.87, GATE_D - 0.4, 0, 0.9)),
    ('sign', face(GATE, -3.3, -1.9, GATE_D - 1.6, 1.95, 2.7)))]
SET_MEANT = [
    ('court_box chair', 'court_box bench', 'the bench stands in front of the judge\'s chair'),
    ('court_box arms', 'court_box chair', 'the arms hang on the wall above and behind the chair back'),
    ('court_box bench', 'court_box door', 'the bench stands 2 m in front of the wall the door is in'),
    ('court_box bench', 'court_box witness box', 'the witness box stands 3 m nearer the lens, below the bench'),
    ('cell desk', 'cell pinboard', 'the pinboard hangs on the wall above the desk shelf'),
    ('cell bed', 'cell door', 'never: (the bed is on the left wall, the door on the right)'),
    ('tvroom door', 'tvroom pool lamp', 'never'),
    ('tvroom pool table', 'tvroom pool lamp', 'the lamp hangs over the table'),
    ('tvroom cue rack', 'tvroom pool lamp', 'the lamp hangs 3 m nearer than the rack on the back wall'),
    ('phone railing', 'phone hood', 'never'),
    ('gates left tower', 'gates centre block', 'the centre block is set back 0.3 m and runs in behind both towers'),
    ('gates right tower', 'gates centre block', 'the centre block is set back 0.3 m and runs in behind both towers'),
    ('gates left bollard', 'gates centre block', 'the bollards stand on the forecourt 0.7 m in front of the gate'),
    ('gates right bollard', 'gates centre block', 'the bollards stand on the forecourt 0.7 m in front of the gate'),
    ('gates sign', 'gates left tower', 'the sign stands on posts 1.6 m in front of the tower'),
    ('gates centre block', 'gates sign', 'the sign stands on posts 1.9 m in front of the gate'),
]
SET_MEANT = [m for m in SET_MEANT if not m[2].startswith('never')]

BENCHMARK = [
    dict(place='Southwark Crown Court outside', refs=['00-court-exterior-wikimedia.jpg'], at='court_out',
         items=[('buff-orange brick block, long and low', 'done: four floors, scattered brick patches'),
                ('ribbon windows in dark frames, some blinds down', 'done: rows of paired-bar windows'),
                ('dark sign band "CROWN COURT SOUTHWARK" over the entrance', 'done: white caps on a dark band'),
                ('glass doors in a dark recess between brick piers', 'done: three doors, two piers'),
                ('raised forecourt behind low brick walls with planted beds', 'done: two walls, shrubs, coping'),
                ('steps with rails up to the doors', 'done: six steps, two rails; in front of the doors (pass 1)'),
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
    dict(place='Courtroom: the jury box (Sam\'s note 10)', refs=['05-witness-box-sketch-cook.jpg',
                                                               '07-witness-judge-sketch-cook.jpg'], at='court_jury',
         items=[('the same pale panelled walls as the witness box (no photo of this jury box found)', 'done: panels, '
                 'picture rail, dado'),
                ('two tiers of six jurors in a pale oak box, the back row raised', 'done: two benches, box fronts'),
                ('tall windows with blinds half down', 'done: two'),
                ('a door to the jury room', 'done: middle, between the windows'),
                ('a picture rail and a dado rail', 'done'),
                ('bench backs and box fronts in raised oak panels', 'done'),
                ('a water jug and glasses on the ledge', 'done'),
                ('papers on the ledge in front of each juror', 'done: white cards'),
                ('jurors in everyday clothes, no robes or wigs', 'done: the cast (blessed_jury)')]),
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
                ('two square towers either side', 'done: cornices, quoins, parapet blocks, plinths'),
                ('tall round arch with a stone ring', 'done: voussoirs'),
                ('timber double gate filling the arch', 'done: planks, iron straps'),
                ('small wicket door cut in the gate (he steps out of it)', 'done: right leaf, open'),
                ('an iron grille in the arch\'s top', 'done'),
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
                ('high barred windows, dark outside', 'done: a strip of three'),
                ('a cue rack, a caged clock, a door with wired glass', 'done'),
                ('the TV high on a bracket (the reverse shot)', 'done: tv()'),
                ('TV light flickering over everyone', 'done: tv_flicker, a jumping level'),
                ('the BBC-style news on the screen', 'done: studio_feed')]),
]


# ================================================================================================ sheets
VIEWS = ('court_out', 'court_box', 'court_jury', 'court_bench', 'court_dock', 'van', 'cell', 'cell_cot', 'cot_top', 'phone', 'tvroom',
         'tv', 'gates')
BACK = {'court_out': court_out, 'court_box': court_box, 'court_jury': court_jury, 'court_bench': court_bench, 'court_dock': court_dock,
        'van': van, 'cell': cell, 'cot_top': cot_top, 'phone': phone, 'tvroom': tvroom, 'gates': gates}
MID = {'court_box': court_box_mid, 'court_dock': court_dock_mid, 'court_jury': court_jury_mid}
FRONT = {'court_box': court_box_front, 'court_jury': court_jury_front, 'court_bench': court_bench_front, 'court_dock': court_dock_front,
         'van': van_front, 'cot_top': cot_top_front, 'tvroom': lambda img, cam, t: tv_flicker(img, cam, t)}


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
