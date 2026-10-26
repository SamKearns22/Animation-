#!/usr/bin/env python3
"""Newsdesk (untitled film, Sam 26 Oct): an Israeli TV news studio, built once in 3D (metres) and seen through any
camera (guides/satire.md, 'One set, one plan'). Drawn from Sam's two studio photos (references/newsdesk/set-1, -2)
in the house style: flat colour, one outline, hand-cut corners, no glows.

The channel is an invented one: no real broadcaster's name, logo or lettering anywhere (Sam's photos are of a real
channel's studio). The only words are generic Hebrew: 'חדשות' (News) on the floor and 'משדר מיוחד' (Special Broadcast)
on the tall screen; the logo is our own (a white wave in a blue circle).

What makes the place (the BENCHMARK list in the notes):
  - a glossy black floor with a big round floor graphic: a blue centre with the channel's mark, a navy band, a thin
    red ring, pale arcs round the outside
  - the presenters' desk: a huge curved ring round the back of the disc, open towards the cameras; a thick white top,
    a blue front with a lighter band; black mesh high-back chairs behind it
  - a tall free-standing blue screen behind the desk with a soft swirl and a white upright bar (with the caption)
  - the back wall: navy screens with a row of short white upright ticks; white pillars edged in red light
  - glass to the working newsroom behind (desks, monitors, red and blue screens on its far wall)
  - a dark ceiling with a lighting grid and spotlights; a studio camera on its pedestal and a floor monitor

Plan (x east, z north, y up): the disc's centre at (0, 1.2); the desk ring round its north side; the presenter's
seat at (0, 4.15) facing south (towards the main camera). Studio x -7..7, z -4..8, ceiling 4.6 m; newsroom behind the
glass at z 8..12, x -7..-2.5.

    python3 source/newsdesk_set.py test OUT.jpg      the set from four cameras on one sheet, the presenter at the desk
    python3 source/newsdesk_set.py refs OUT.jpg      Sam's photos beside ours (studio, presenter, chairs)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import sets as S                 # noqa: E402
from sets import Face, obox, cylinder, draw_parts, dk, lt, jit   # noqa: E402
from ed import INK               # noqa: E402

FLAT = S.FLAT
HEB = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')    # DejaVu carries the Hebrew letters

# ---------------------------------------------------------------------------------------------- colours
FLOOR = (18, 20, 27)
FLOOR_SHEEN = (28, 31, 42)
DISC_BLUE = (36, 116, 216)
DISC_MID = (58, 146, 232)
DISC_PALE = (110, 182, 244)
DISC_NAVY = (20, 34, 80)
DISC_RED = (214, 40, 48)
DISC_ARC = (236, 216, 216)
DESK_BLUE = (32, 90, 194)
DESK_LIGHT = (120, 176, 240)
DESK_TOP = (244, 244, 246)
DESK_BACK = (46, 50, 64)
WALL_NAVY = (24, 40, 92)
WALL_DARK = (20, 24, 40)
LED_BLUE = (30, 74, 176)
PILLAR = (232, 234, 240)
RED_LIGHT = (214, 36, 48)
CEIL = (14, 16, 22)
CHAIR = (30, 30, 36)
METAL = (150, 154, 162)

# ---------------------------------------------------------------------------------------------- the plan
X0, X1, Z0, Z1, CEIL_H = -7.0, 7.0, -4.0, 8.0, 4.6
NEWS = (-7.0, 8.0, -2.5, 12.0)                  # the newsroom behind the glass (x0, z0, x1, z1)
NEWS_CEIL = 3.2
GLASS = (-7.0, -2.5, 0.0, 3.4)                  # the glass in the north wall: x0, x1, sill, head
DISC = (0.0, 1.2)                               # the floor graphic's centre
DISC_R = 2.0
DESK_R0, DESK_R1, DESK_H = 2.15, 2.72, 0.8     # the desk ring: inner and outer radius, height
DESK_A0, DESK_A1 = -24.0, 204.0                 # its ends (degrees from east, anticlockwise seen from above)
SEAT_R = 3.05                                   # the chairs behind it
SEATS = {'presenter': 90.0, 'left2': 128.0, 'left1': 108.0, 'right1': 72.0, 'right2': 52.0}
PRESENTER_AT = (DISC[0] + SEAT_R * math.cos(math.radians(90)), DISC[1] + SEAT_R * math.sin(math.radians(90)))

ROOMS = {'studio': (X0, Z0, X1, Z1), 'newsroom': (NEWS[0], NEWS[1], NEWS[2], NEWS[3])}
OPENINGS = {'newsroom glass': dict(wall=('z', Z1), span=(GLASS[0], GLASS[1]), sill=GLASS[2], head=GLASS[3])}

CAMS = {   # the test sheet's cameras (a film adds its own)
    'wide': dict(pos=(0.5, 1.75, -3.0), look=(0.0, 0.95, 4.0), focal=700),
    'anchor': dict(pos=(0.0, 1.3, -0.2), look=(0.0, 1.08, 4.15), focal=3500),
    'high': dict(pos=(-3.6, 3.9, -2.6), look=(0.2, 0.3, 2.6), focal=620),
    'side': dict(pos=(5.6, 1.55, 0.2), look=(-0.6, 1.1, 3.8), focal=760),
}


def cam(name):
    c = CAMS[name]
    return S.Cam(c['pos'], c['look'], focal=c['focal'])


# ---------------------------------------------------------------------------------------------- helpers
def _pen(img):
    return B.Pen(img, FLAT)


def poly(img, cm, pts, fill, line=INK, lw=2.0):
    cm.poly(_pen(img), pts, fill, line, lw)


def lines(img, cm, pts, col=INK, lw=2.0):
    cm.line(_pen(img), [jit(q) for q in pts], col, lw)


def ring(c, r, a0=0.0, a1=360.0, y=0.0, n=None):
    n = n or max(8, int(abs(a1 - a0) / 3))
    return [(c[0] + r * math.cos(math.radians(a)), y, c[1] + r * math.sin(math.radians(a)))
            for a in np.linspace(a0, a1, n)]


def band(c, r0, r1, a0=0.0, a1=360.0, y=0.0):
    return ring(c, r1, a0, a1, y) + ring(c, r0, a1, a0, y)


def _persp(src, dst):
    """Coefficients for PIL's PERSPECTIVE transform: output pixel (dst) -> input pixel (src)."""
    A, bv = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); bv.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); bv.append(v)
    return np.linalg.solve(np.array(A, float), np.array(bv, float)).tolist()


def paste_on(img, cm, quad, art):
    """Lay a flat picture (RGBA) onto a 3D rectangle: quad = its top-left, top-right, bottom-right, bottom-left
    corners in the world. Through the camera, so it sits on the floor or a wall in perspective."""
    if any(cm.depth(q) < cm.NEAR + 0.05 for q in quad):
        return
    ss = img.width / 1080.0
    dst = [(x * ss, y * ss) for x, y in (cm.project(q)[0] for q in quad)]
    w, h = art.size
    co = _persp([(0, 0), (w, 0), (w, h), (0, h)], dst)
    lay = art.transform(img.size, Image.PERSPECTIVE, co, Image.BILINEAR)
    img.alpha_composite(lay)


def heb_text(text, px, col, pad=8):
    f = ImageFont.truetype(HEB, px)
    box = f.getbbox(text, direction='rtl')
    im = Image.new('RGBA', (box[2] - box[0] + 2 * pad, box[3] - box[1] + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - box[0], pad - box[1]), text, font=f, fill=col, direction='rtl')
    return im


# ---------------------------------------------------------------------------------------------- the newsroom (behind glass)
def newsroom(img, cm):
    x0, z0, x1, z1 = NEWS
    poly(img, cm, [(x0, 0, z0), (x1, 0, z0), (x1, 0, z1), (x0, 0, z1)], (70, 72, 82))
    poly(img, cm, [(x0, NEWS_CEIL, z0), (x1, NEWS_CEIL, z0), (x1, NEWS_CEIL, z1), (x0, NEWS_CEIL, z1)], (190, 192, 198))
    poly(img, cm, [(x0, 0, z1), (x1, 0, z1), (x1, NEWS_CEIL, z1), (x0, NEWS_CEIL, z1)], (206, 206, 212))     # far wall
    poly(img, cm, [(x1, 0, z0), (x1, 0, z1), (x1, NEWS_CEIL, z1), (x1, NEWS_CEIL, z0)], (186, 186, 194))     # east wall
    for i, (a, b, c) in enumerate(((-6.6, -5.2, (196, 36, 46)), (-5.0, -3.6, (34, 80, 180)), (-3.4, -2.7, (196, 36, 46)))):
        poly(img, cm, [(a, 1.6, z1 - 0.02), (b, 1.6, z1 - 0.02), (b, 2.5, z1 - 0.02), (a, 2.5, z1 - 0.02)], c)
        lines(img, cm, [(a + 0.15, 2.25, z1 - 0.03), (b - 0.4, 2.25, z1 - 0.03)], (240, 240, 244), 2.0)
        lines(img, cm, [(a + 0.15, 2.05, z1 - 0.03), (b - 0.2, 2.05, z1 - 0.03)], dk(c, 1.25) if False else lt(c, 1.4), 1.6)
    for k in range(6):                                  # ceiling strip lights
        z = z0 + 0.6 + k * 0.6
        poly(img, cm, [(x0 + 0.3, NEWS_CEIL - 0.01, z), (x1 - 0.3, NEWS_CEIL - 0.01, z),
                       (x1 - 0.3, NEWS_CEIL - 0.01, z + 0.12), (x0 + 0.3, NEWS_CEIL - 0.01, z + 0.12)], (250, 250, 240), None)
    parts = []
    rng = np.random.default_rng(4)
    for row, z in enumerate((9.0, 10.4)):              # two rows of desks, monitors on each
        for k, x in enumerate((-6.2, -4.9, -3.6)):
            parts.append(obox((x, 0.0, z), (1.15, 0.74, 0.7), 0, {'all': (226, 226, 230), 'top': (238, 238, 242)}))
            for m in (-0.25, 0.25):
                c = (x + m, 0.74, z + 0.1)
                parts.append(obox(c, (0.46, 0.34, 0.05), 180, {'all': (30, 30, 36),
                                  'front': (40, 90, 170) if rng.random() < 0.6 else (60, 64, 72)}))
            if rng.random() < 0.7:                        # someone at work: a dark head and shoulders over the desk
                c = (x + rng.uniform(-0.2, 0.2), 0.0, z + 0.65)
                parts.append(obox(c, (0.42, 1.2, 0.26), 0, {'all': tuple(int(v) for v in rng.choice(
                    [(60, 64, 80), (120, 80, 70), (190, 190, 196), (70, 90, 70)]))}))
    draw_parts(img, cm, parts, _pen(img))


# ---------------------------------------------------------------------------------------------- walls, ceiling, glass
def walls(img, cm):
    gx0, gx1, sill, head = GLASS
    north = [((gx1, 0), (X1, CEIL_H)), ((gx0, head), (gx1, CEIL_H))]
    for (a, y0), (b, y1) in north:
        poly(img, cm, [(a, y0, Z1), (b, y0, Z1), (b, y1, Z1), (a, y1, Z1)], WALL_NAVY)
    for k in range(int((X1 - gx1) / 0.42)):             # the LED wall's row of short white ticks
        x = gx1 + 0.3 + k * 0.42
        if 0.4 < x - gx1 and x < X1 - 0.2:
            poly(img, cm, [(x, 2.55, Z1 - 0.01), (x + 0.045, 2.55, Z1 - 0.01), (x + 0.045, 3.05, Z1 - 0.01),
                           (x, 3.05, Z1 - 0.01)], (236, 238, 246), None)
    for y in (1.0, 2.0, 3.6):                           # screen joins: faint seams across the panels
        lines(img, cm, [(gx1 + 0.05, y, Z1 - 0.01), (X1 - 0.05, y, Z1 - 0.01)], dk(WALL_NAVY, 0.78), 1.4)
    for k in range(int((X1 - gx1) / 1.6)):
        x = gx1 + 1.6 * (k + 1)
        lines(img, cm, [(x, 0.05, Z1 - 0.01), (x, CEIL_H - 0.05, Z1 - 0.01)], dk(WALL_NAVY, 0.78), 1.4)
    # east wall: navy screens, ticks
    poly(img, cm, [(X1, 0, Z0), (X1, 0, Z1), (X1, CEIL_H, Z1), (X1, CEIL_H, Z0)], dk(WALL_NAVY, 0.9))
    for k in range(int((Z1 - Z0) / 0.42)):
        z = Z0 + 0.3 + k * 0.42
        poly(img, cm, [(X1 - 0.01, 2.55, z), (X1 - 0.01, 2.55, z + 0.045), (X1 - 0.01, 3.05, z + 0.045),
                       (X1 - 0.01, 3.05, z)], (226, 228, 238), None)
    # west wall: dark, with a red light strip at its far corner
    poly(img, cm, [(X0, 0, Z0), (X0, 0, Z1), (X0, CEIL_H, Z1), (X0, CEIL_H, Z0)], WALL_DARK)
    poly(img, cm, [(X0 + 0.01, 0.2, Z1 - 0.5), (X0 + 0.01, 0.2, Z1 - 0.38), (X0 + 0.01, CEIL_H - 0.3, Z1 - 0.38),
                   (X0 + 0.01, CEIL_H - 0.3, Z1 - 0.5)], RED_LIGHT, None)
    # ceiling
    poly(img, cm, [(X0, CEIL_H, Z0), (X0, CEIL_H, Z1), (X1, CEIL_H, Z1), (X1, CEIL_H, Z0)], CEIL)


def glass(img, cm):
    """The newsroom glass: a faint pale sheen with a few flat streaks, dark mullions (house style: no glows)."""
    gx0, gx1, sill, head = GLASS
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    q = [(gx0, sill, Z1), (gx1, sill, Z1), (gx1, head, Z1), (gx0, head, Z1)]
    _pen_l = B.Pen(lay, FLAT)
    cm.poly(_pen_l, q, (150, 180, 220, 46), None)
    for a in (-6.4, -4.1):                              # flat streaks
        cm.poly(_pen_l, [(a, sill + 0.4, Z1), (a + 0.25, sill + 0.4, Z1), (a + 0.9, head - 0.3, Z1),
                         (a + 0.65, head - 0.3, Z1)], (255, 255, 255, 34), None)
    img.alpha_composite(lay)
    for x in np.arange(gx0, gx1 + 0.01, 1.5):
        poly(img, cm, [(x - 0.04, sill, Z1), (x + 0.04, sill, Z1), (x + 0.04, head, Z1), (x - 0.04, head, Z1)], (40, 42, 50))
    poly(img, cm, [(gx0, sill, Z1), (gx1, sill, Z1), (gx1, sill + 0.35, Z1), (gx0, sill + 0.35, Z1)], (34, 36, 44))
    poly(img, cm, [(gx0, head - 0.06, Z1), (gx1, head - 0.06, Z1), (gx1, head, Z1), (gx0, head, Z1)], (40, 42, 50))


def rig_parts():
    """The lighting grid: black bars under the ceiling, spotlights hanging from them."""
    parts = []
    for z in (-1.0, 1.4, 3.8, 6.2):
        parts.append(obox((0.0, CEIL_H - 0.36, z), (13.0, 0.08, 0.08), 0, {'all': (26, 26, 30)}))
        for x in np.arange(-5.5, 5.6, 2.2):
            parts.append(obox((x, CEIL_H - 0.62, z), (0.22, 0.26, 0.26), 0, {'all': (36, 36, 42),
                              'bottom': (250, 246, 220)}))
    return parts


# ---------------------------------------------------------------------------------------------- the floor and its graphic
def floor(img, cm):
    poly(img, cm, [(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)], FLOOR)
    for a, b in ((-5.6, -5.3), (3.8, 4.0), (-2.9, -2.75), (5.6, 5.85)):   # flat reflections of the lights: long streaks
        poly(img, cm, [(a, 0.001, Z0 + 0.5), (b, 0.001, Z0 + 0.5), (b + 0.3, 0.001, Z1 - 0.5), (a + 0.3, 0.001, Z1 - 0.5)],
             FLOOR_SHEEN, None)
    c = DISC
    y = 0.003
    poly(img, cm, band(c, DISC_R - 0.24, DISC_R + 0.18, 200, 340, y), DISC_ARC, INK, 1.6)       # pale arcs
    poly(img, cm, band(c, DISC_R + 0.3, DISC_R + 0.52, 215, 300, y), DISC_ARC, INK, 1.6)
    poly(img, cm, band(c, DISC_R + 0.3, DISC_R + 0.52, 310, 330, y), DISC_ARC, INK, 1.6)
    poly(img, cm, ring(c, DISC_R - 0.24, y=y + 0.001), DISC_NAVY, INK, 1.8)
    poly(img, cm, band(c, DISC_R - 0.46, DISC_R - 0.38, y=y + 0.002), DISC_RED, None)            # the thin red ring
    poly(img, cm, ring(c, DISC_R - 0.62, y=y + 0.003), DISC_BLUE, INK, 1.6)
    poly(img, cm, [(c[0] + 0.25 + 0.8 * math.cos(math.radians(a)), y + 0.004, c[1] - 0.15 + 0.8 * math.sin(math.radians(a)))
                   for a in range(0, 360, 6)], DISC_MID, None)                                     # soft rings, flat
    poly(img, cm, [(c[0] + 0.35 + 0.42 * math.cos(math.radians(a)), y + 0.005, c[1] - 0.2 + 0.42 * math.sin(math.radians(a)))
                   for a in range(0, 360, 8)], DISC_PALE, None)
    # the channel's mark (our own): 'חדשות' beside a white wave in a circle, read from the main camera's side
    mark = Image.new('RGBA', (900, 220), (0, 0, 0, 0))
    d = ImageDraw.Draw(mark)
    d.ellipse([640, 20, 820, 200], fill=(255, 255, 255, 255))
    d.ellipse([656, 36, 804, 184], fill=DISC_BLUE + (255,))
    wave = [(670 + k * 6, 110 + 22 * math.sin(k / 3.2)) for k in range(23)]
    d.line(wave, fill=(255, 255, 255, 255), width=16, joint='curve')
    txt = heb_text('חדשות', 150, (255, 255, 255, 255))
    mark.alpha_composite(txt, (max(0, 600 - txt.width), max(0, (220 - txt.height) // 2)))
    w, h = 2.0, 2.0 * 220 / 900
    cx, cz = c[0], c[1] - 0.05
    paste_on(img, cm, [(cx - w / 2, y + 0.006, cz + h / 2), (cx + w / 2, y + 0.006, cz + h / 2),
                       (cx + w / 2, y + 0.006, cz - h / 2), (cx - w / 2, y + 0.006, cz - h / 2)], mark)


# ---------------------------------------------------------------------------------------------- the desk
def _dp(a, r, y):
    return (DISC[0] + r * math.cos(math.radians(a)), y, DISC[1] + r * math.sin(math.radians(a)))


DESK_STEPS = np.linspace(DESK_A0, DESK_A1, 77)   # 76 slices of 3 degrees
DESK_PIECE = 4                                   # slices per drawn piece (12 degrees): each piece is sorted on its own,
                                                 # so whoever stands nearer is always drawn on top (Netan-Yahoo!, 26 Oct)


def _desk_faces(cm, a, r, out):
    p = _dp(a, r, DESK_H / 2)
    n = (math.cos(math.radians(a)) * (1 if out else -1), 0, math.sin(math.radians(a)) * (1 if out else -1))
    return (cm.pos[0] - p[0]) * n[0] + (cm.pos[2] - p[2]) * n[2] > 0


def _desk_runs(cm, r, out):
    """Index runs [k0, k1] of DESK_STEPS where that side of the desk faces the camera (whole desk, not per piece)."""
    runs, k0 = [], None
    for k, a in enumerate(DESK_STEPS):
        if _desk_faces(cm, a, r, out):
            k0 = k if k0 is None else k0
        elif k0 is not None:
            runs.append((k0, k - 1))
            k0 = None
    if k0 is not None:
        runs.append((k0, len(DESK_STEPS) - 1))
    return runs


def desk(img, cm, i0=0, i1=None):
    """The curved ring desk, or the stretch of it from step i0 to i1: per slice, the side that faces the camera (inner
    blue front, or outer dark back) and the white top, filled far to near without lines; then one outline round what
    shows (house style: one outline). Silhouette edges come from the whole desk's runs, so pieces join seamlessly."""
    steps = DESK_STEPS
    i1 = len(steps) - 1 if i1 is None else i1
    pos = cm.pos
    slices = []
    for k in range(i0, i1):
        a0, a1 = steps[k], steps[k + 1]
        m = (a0 + a1) / 2
        slices.append((math.dist(_dp(m, (DESK_R0 + DESK_R1) / 2, DESK_H / 2), pos), a0, a1, m))
    slices.sort(reverse=True)
    band_y = DESK_H * 0.62
    for _, a0, a1, m in slices:
        if _desk_faces(cm, m, DESK_R1, True):            # the dark outer back
            poly(img, cm, [_dp(a0, DESK_R1, 0), _dp(a1, DESK_R1, 0), _dp(a1, DESK_R1, DESK_H), _dp(a0, DESK_R1, DESK_H)],
                 DESK_BACK, None)
        if _desk_faces(cm, m, DESK_R0, False):           # the blue front: dark lower, a lighter band, a white strip
            r = DESK_R0
            poly(img, cm, [_dp(a0, r, 0), _dp(a1, r, 0), _dp(a1, r, band_y), _dp(a0, r, band_y)], DESK_BLUE, None)
            poly(img, cm, [_dp(a0, r, band_y), _dp(a1, r, band_y), _dp(a1, r, DESK_H - 0.09), _dp(a0, r, DESK_H - 0.09)],
                 DESK_LIGHT, None)
            poly(img, cm, [_dp(a0, r, DESK_H - 0.09), _dp(a1, r, DESK_H - 0.09), _dp(a1, r, DESK_H), _dp(a0, r, DESK_H)],
                 DESK_TOP, None)
        if pos[1] > DESK_H:
            poly(img, cm, [_dp(a0, DESK_R0, DESK_H), _dp(a1, DESK_R0, DESK_H), _dp(a1, DESK_R1, DESK_H),
                           _dp(a0, DESK_R1, DESK_H)], DESK_TOP, None)
    # the outlines: the top's two edges, the bottom edge and the band lines of whatever front shows, the ends
    seg = steps[i0:i1 + 1]
    lines(img, cm, [_dp(a, DESK_R0, DESK_H) for a in seg])
    lines(img, cm, [_dp(a, DESK_R1, DESK_H) for a in seg])
    for r, out in ((DESK_R0, False), (DESK_R1, True)):
        for k0, k1 in _desk_runs(cm, r, out):
            lo, hi = max(k0, i0), min(k1, i1)
            if hi > lo:
                _outline_run(img, cm, list(steps[lo:hi + 1]), r, out,
                             ends=[steps[k] for k in (k0, k1) if lo <= k <= hi])
    for k, a in ((0, DESK_A0), (len(steps) - 1, DESK_A1)):   # the white end caps
        if not i0 <= k <= i1:
            continue
        q = [_dp(a, DESK_R0, 0), _dp(a, DESK_R1, 0), _dp(a, DESK_R1, DESK_H), _dp(a, DESK_R0, DESK_H)]
        tang = (-math.sin(math.radians(a)), 0, math.cos(math.radians(a)))
        sgn = -1 if a == DESK_A0 else 1
        c = _dp(a, (DESK_R0 + DESK_R1) / 2, DESK_H / 2)
        if (pos[0] - c[0]) * tang[0] * sgn + (pos[2] - c[2]) * tang[2] * sgn > 0:
            poly(img, cm, q, DESK_TOP, INK, 2.2)


def desk_items():
    """The desk as pieces, each (reference point, draw(img, cam)), for the far-to-near sort."""
    out, n = [], len(DESK_STEPS) - 1
    for i0 in range(0, n, DESK_PIECE):
        i1 = min(n, i0 + DESK_PIECE)
        m = (DESK_STEPS[i0] + DESK_STEPS[i1]) / 2
        out.append((_dp(m, (DESK_R0 + DESK_R1) / 2, DESK_H / 2), lambda img, cm, i0=i0, i1=i1: desk(img, cm, i0, i1)))
    return out


def desk_plan_things(n=24):
    """The desk for a film's PLAN THINGS (rule 12): n straight blocks, each wholly covering its stretch of the ring
    (its inside face is the chord, so the blocks reach a little nearer the centre than the real desk: on the safe
    side for clearance checks)."""
    out = {}
    da = (DESK_A1 - DESK_A0) / n
    h = math.radians(da / 2)
    for i in range(n):
        m = DESK_A0 + (i + 0.5) * da
        rin = DESK_R0 * math.cos(h)
        rc = (rin + DESK_R1) / 2
        x, z = DISC[0] + rc * math.cos(math.radians(m)), DISC[1] + rc * math.sin(math.radians(m))
        f = -(90.0 + m)                          # turn that lays its width along the ring (rot_y's way)
        t = ((f + 45.0) % 90.0) - 45.0           # the plan gives sizes along the nearest axes (plan.tilt)
        w, d = 2 * DESK_R1 * math.sin(h), DESK_R1 - rin
        if round((f - t) / 90.0) % 2:
            w, d = d, w
        out[f'desk{i + 1:02d}'] = dict(at=(round(x, 4), round(z, 4)), size=(round(w, 4), round(d, 4), DESK_H),
                                       facing=round(t, 3), part_of='desk')
    return out

def _outline_run(img, cm, run, r, out, ends=None):
    lines(img, cm, [_dp(a, r, 0.0) for a in run], INK, 2.2)
    if not out:
        lines(img, cm, [_dp(a, r, DESK_H * 0.62) for a in run], dk(DESK_BLUE, 0.7), 1.4)
        lines(img, cm, [_dp(a, r, DESK_H - 0.09) for a in run], dk(DESK_LIGHT, 0.7), 1.2)
    for a in ((run[0], run[-1]) if ends is None else ends):   # where the face turns away: its silhouette edge
        if DESK_A0 < a < DESK_A1:
            lines(img, cm, [_dp(a, r, 0.0), _dp(a, r, DESK_H)], INK, 2.2)


# ---------------------------------------------------------------------------------------------- free-standing pieces
def screen_parts():
    """The tall blue screen behind the desk (left of centre), and the two white pillars edged in red light."""
    x0, x1, z, h = -2.5, -0.7, 6.9, 4.2

    def front(img, cm, p):
        zf = z - 0.08
        for cx, cy, r, col in ((-1.3, 2.6, 0.95, (44, 100, 206)), (-1.15, 2.45, 0.62, (66, 136, 230)),
                               (-1.05, 2.35, 0.32, (104, 172, 246))):     # the swirl: flat circles, hand-cut
            pts = [(max(x0 + 0.02, min(x1 - 0.02, cx + r * math.cos(a))), max(0.05, min(h - 0.05, cy + r * 1.1 * math.sin(a))), zf - 0.002)
                   for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
            poly(img, cm, pts, col, None)
        poly(img, cm, [(-1.0, 0.9, zf - 0.004), (-0.94, 0.9, zf - 0.004), (-0.94, 3.6, zf - 0.004), (-1.0, 3.6, zf - 0.004)],
             (246, 246, 250), None)                     # the white upright bar
        txt = heb_text('משדר מיוחד', 64, (246, 246, 250, 255))
        w = 0.62
        hh = w * txt.height / txt.width
        paste_on(img, cm, [(-1.62, 1.05 + hh, zf - 0.005), (-1.0, 1.05 + hh, zf - 0.005), (-1.0, 1.05, zf - 0.005),
                           (-1.62, 1.05, zf - 0.005)], txt)
    led = obox(((x0 + x1) / 2, 0.0, z), (x1 - x0, h, 0.16), 180, {'all': LED_BLUE, 'front': LED_BLUE}, extras={'front': front})
    parts = [led]
    for px in (-3.1, 2.9):                              # white pillars, a red light down one edge
        def edge(img, cm, p, px=px):
            sx = px + (0.26 if px < 0 else -0.26)
            poly(img, cm, [(sx - 0.03, 0.1, 6.79), (sx + 0.03, 0.1, 6.79), (sx + 0.03, 4.1, 6.79), (sx - 0.03, 4.1, 6.79)],
                 RED_LIGHT, None)
        parts.append(obox((px, 0.0, 7.0), (0.56, CEIL_H - 0.4, 0.4), 180, {'all': PILLAR, 'front': PILLAR},
                          extras={'front': edge}))
    return parts


def mesh_chair_parts(x, z, facing):
    """A black mesh high-back office chair (ref set-2): a five-star base, a column, the seat, a tall back with mesh
    lines, armrests. `facing`: plan degrees (0 north)."""
    yaw = facing
    def at(lx, ly, lz):
        q = S.rot_y((lx, ly, lz), yaw)
        return (x + q[0], ly, z + q[2])
    parts = [cylinder(at(0, 0.0, 0), 0.32, 0.06, {'side': (24, 24, 28), 'top': (40, 40, 46)}, n=12),
             cylinder(at(0, 0.06, 0), 0.03, 0.36, {'side': METAL, 'top': METAL}, n=8),
             obox(at(0, 0.42, 0.02), (0.52, 0.09, 0.5), yaw, {'all': CHAIR})]

    def mesh(img, cm, p):
        for k in range(1, 6):
            u = -0.24 + k * 0.08
            a, b = at(u, 0.6, -0.27), at(u, 1.18, -0.27)
            lines(img, cm, [a, b], (58, 58, 66), 1.2)
    parts.append(obox(at(0, 0.55, -0.26), (0.5, 0.68, 0.06), yaw, {'all': CHAIR, 'front': (40, 40, 48)},
                      extras={'front': mesh}))
    for sgn in (-1, 1):
        parts.append(obox(at(sgn * 0.27, 0.58, 0.0), (0.05, 0.05, 0.34), yaw, {'all': CHAIR}))
    return parts


def studio_camera_parts(x, z, facing):
    """A studio camera on its pedestal: the column, the head, a prompter hood in front, a pan bar back."""
    yaw = facing
    def at(lx, ly, lz):
        q = S.rot_y((lx, ly, lz), yaw)
        return (x + q[0], ly, z + q[2])
    return [cylinder(at(0, 0, 0), 0.42, 0.18, {'side': (34, 34, 40), 'top': (50, 50, 58)}, n=14),
            cylinder(at(0, 0.18, 0), 0.08, 1.05, {'side': (60, 62, 70), 'top': (70, 70, 80)}, n=10),
            obox(at(0, 1.23, -0.05), (0.32, 0.34, 0.6), yaw, {'all': (44, 46, 52)}),
            obox(at(0, 1.18, 0.38), (0.42, 0.44, 0.34), yaw, {'all': (24, 24, 28), 'front': (60, 66, 80)}),
            obox(at(0.18, 1.3, -0.5), (0.04, 0.04, 0.5), yaw, {'all': METAL})]


def monitor_parts(x, z, facing):
    """A floor monitor on a stand (the presenter's return feed), its screen showing the studio's blue."""
    yaw = facing
    def at(lx, ly, lz):
        q = S.rot_y((lx, ly, lz), yaw)
        return (x + q[0], ly, z + q[2])
    return [cylinder(at(0, 0, 0), 0.26, 0.04, {'side': (30, 30, 36), 'top': (44, 44, 50)}, n=12),
            cylinder(at(0, 0.04, 0), 0.03, 0.95, {'side': METAL, 'top': METAL}, n=8),
            obox(at(0, 0.95, 0), (0.95, 0.56, 0.08), yaw, {'all': (26, 26, 30), 'front': (52, 112, 210)})]


# ---------------------------------------------------------------------------------------------- the whole set
def items(people=None):
    """Everything standing in the studio, each (reference point, draw(img, cam)), drawn far to near after the floor.
    people: [(x, z, draw)] for anyone in it (the desk is drawn after everyone behind it)."""
    out = []
    def part_item(parts, ref):
        return (ref, lambda img, cm, parts=parts: draw_parts(img, cm, parts, _pen(img)))
    out.append(part_item(screen_parts(), (-1.6, 2.0, 6.9)))
    for name, a in SEATS.items():
        x, z = DISC[0] + SEAT_R * math.cos(math.radians(a)), DISC[1] + SEAT_R * math.sin(math.radians(a))
        facing = math.degrees(math.atan2(DISC[0] - x, DISC[1] - z))
        out.append(part_item(mesh_chair_parts(x, z, facing), (x + 0.2 * math.sin(math.radians(facing + 180)), 0.8,
                                                             z + 0.2 * math.cos(math.radians(facing + 180)))))
    out.append(part_item(studio_camera_parts(4.6, -1.4, -55), (4.6, 1.0, -1.4)))
    out.append(part_item(monitor_parts(-4.9, 1.6, 75), (-4.9, 1.0, 1.6)))
    out.extend(desk_items())
    for x, z, fn in people or []:
        out.append(((x, 1.0, z), fn))
    return out


def render(img, cm, people=None):
    """The studio through `cm` on img (a frame: 1080 x 1920 times B.SS)."""
    img.paste(CEIL + (255,), (0, 0) + img.size)
    newsroom(img, cm)
    walls(img, cm)
    glass(img, cm)
    draw_parts(img, cm, rig_parts(), _pen(img))
    floor(img, cm)
    for ref, fn in sorted(items(people), key=lambda it: -math.dist(it[0], cm.pos)):
        fn(img, cm)
    return img


# ---------------------------------------------------------------------------------------------- the presenter in it
def put_seated(img, cm, sp, x, z, facing, t=0.0):
    """Someone seated on a chair at floor point (x, z) facing `facing` (plan degrees), through the camera (Prepper's
    put(), seated: the pose's own drop lowers him onto the seat)."""
    import views as V
    import moves
    M = V.M_PER_UNIT
    f = sp.get('height', 1.75) / 1.75
    neck = 928 * M * f
    (Xn, Yn), k = cm.project((x, neck, z))
    (Xf, Yf), _ = cm.project((x, 0.0, z))
    s = max(1e-3, (Yf - Yn) / 928.0)
    fd = (math.sin(math.radians(facing)), math.cos(math.radians(facing)))
    yaw = cm.yaw_of((x, 0, z), fd)
    j = moves.seated(sp)
    j['seated'] = False                                  # the set draws his chair
    return V.person(img, FLAT, Xf, Yf - 928 * s, s, dict(sp, full=True, pose='custom'), t, yaw, j)


def test(out):
    import newsdesk_cast as NC
    B.SS = 1
    tiles = []
    for name in ('wide', 'anchor', 'high', 'side'):
        cm = cam(name)
        img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 255))
        px, pz = PRESENTER_AT
        people = [(px, pz + 0.05, lambda im, c: put_seated(im, c, NC.PRESENTER, px, pz, 180.0))]
        render(img, cm, people)
        tiles.append((name, img))
    W = 4 * 540 + 5 * 20
    sheet = Image.new('RGB', (W, 960 + 90), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(HEB, 30)
    for i, (name, img) in enumerate(tiles):
        sheet.paste(img.convert('RGB').resize((540, 960), Image.LANCZOS), (20 + i * 560, 70))
        d.text((20 + i * 560, 20), f'camera: {name}', font=f, fill=(30, 30, 30))
    sheet.save(out, quality=90)
    return out


def picture(name='wide'):
    """One frame of the set from a named camera (CAMS), the presenter at the desk: the kit catalogue's tile."""
    import newsdesk_cast as NC
    img = Image.new('RGBA', (1080 * B.SS, 1920 * B.SS), (0, 0, 0, 255))
    px, pz = PRESENTER_AT
    return render(img, cam(name), [(px, pz + 0.05, lambda im, c: put_seated(im, c, NC.PRESENTER, px, pz, 180.0))])


def refsheet(out):
    """Rule 3 by hand (there is no film module yet for benchmark.py): Sam's photos beside ours, row by row: the
    studio from the front and from above, the presenters, the chairs."""
    import newsdesk_cast as NC
    import newsdesk_props as NP
    B.SS = 1
    ref = os.path.join(os.path.dirname(HERE), 'references', 'newsdesk')

    def frame(name):
        img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 255))
        px, pz = PRESENTER_AT
        render(img, cam(name), [(px, pz + 0.05, lambda im, c: put_seated(im, c, NC.PRESENTER, px, pz, 180.0))])
        return img.convert('RGB')
    H = 420

    def fit(im):
        return im.resize((int(im.width * H / im.height), H), Image.LANCZOS)
    chairs = Image.new('RGBA', (1080, 1920), NP.STAGE + (255,))
    c1 = S.Cam((0.0, 1.45, -3.2), (0.0, 0.42, 0.0), focal=1500)
    for x in (-0.65, 0.65):
        NP.pool(chairs, c1, x, 0.0)
        NP.shadow(chairs, c1, x, 0.0, 180)
    for x in (-0.65, 0.65):
        NP.round_chair(chairs, c1, x, 0.0, 180)
    rows = [('studio, front', ['set-2-desk-front.jpg'], frame('wide').crop((0, 540, 1080, 1340))),
            ('studio, from above', ['set-1-wide-desk.jpg'], frame('high').crop((0, 640, 1080, 1240))),
            ('presenter (type, not a face)', ['presenter-1.jpg', 'presenter-2.jpg', 'presenter-3.jpg'],
             frame('anchor').crop((140, 560, 940, 1240))),
            ('chairs', ['chairs-1.jpg'], chairs.convert('RGB').crop((0, 560, 1080, 1360)))]
    tiles = []
    for label, refs, ours in rows:
        ims = [fit(Image.open(os.path.join(ref, r)).convert('RGB')) for r in refs] + [fit(ours)]
        tiles.append((label, ims))
    W = max(sum(i.width for i in ims) + 20 * (len(ims) + 1) for _, ims in tiles)
    sheet = Image.new('RGB', (W, len(tiles) * (H + 70) + 20), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(HEB, 28)
    y = 20
    for label, ims in tiles:
        d.text((20, y), f'{label}: Sam\'s photo(s) left, ours right', font=f, fill=(30, 30, 30))
        x = 20
        for k, im in enumerate(ims):
            sheet.paste(im, (x, y + 40))
            if k == len(ims) - 1:
                d.rectangle([x - 4, y + 36, x + im.width + 3, y + 43 + H], outline=(200, 40, 50), width=4)
            x += im.width + 20
        y += H + 70
    sheet.save(out, quality=88)
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        print(test(sys.argv[2]))
    elif sys.argv[1] == 'refs':
        print(refsheet(sys.argv[2]))
