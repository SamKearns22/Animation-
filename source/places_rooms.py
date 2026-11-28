#!/usr/bin/env python3
"""MAP  The places kit's indoor pieces (ranking item 5; overnight chat 5c, 14 Nov): rooms seen from inside (walls,
ceiling and floor running from the back wall to the picture's corners), ruled lines (brick courses, floor ribs,
lino joints, tiles), brick marks, strokes and studs, washes, glows and a TV's flicker; a vehicle's cell (its moulded
seat, a vent, a CCTV sticker, a window onto a street going by, the open door leaf by the lens), a prison cell (a barred
window, a steel basin and toilet, a shelf, a pinboard, a bed along the wall, the open cell door onto the landing),
a cot seen from above and its blanket, wall PIN phones under hoods and pinned notices, an association room (a cork
noticeboard, a caged clock, a door with wired glass, a pool table) and a TV on a wall bracket showing a feed.
Lifted unchanged in look from Blessed's van, cell, cot_top, phone, tvroom and tv (blessed_sets.py) and made
general: each piece draws in its own units from its front face's top-left (or its point) at its REF px per metre.
Registered into places_parts.KINDS (places_parts imports this file at its end).

A camera looking straight down (cot_top) is described as a level camera on the floor: x across, z up the screen,
depth the height above the floor (the arithmetic is the same).

Map: helpers 30 | rooms, lines, bricks 45 | strokes, studs, light 120 | the van 185 | the cell 245 |
     the cot from above 355 | the phone room 385 | the association room 430 | the TV 500
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from ink import INK, curve
from places_parts import kind, wob, quad, mix, dk, bricks_in

STEEL = (176, 182, 188)
CANVAS = (-300, -400, 1380, 2400)            # the picture's corners as the sets paint them (past the frame's edges)


def _soft(img, cam, box, col, a, blur):
    """A soft light or shade wash over a box (Blessed's `soft`): no outline."""
    lay = Image.new('RGBA', img.size, col + (0,))
    x0, y0 = cam.P(box[0], box[1])
    x1, y1 = cam.P(box[2], box[3])
    ImageDraw.Draw(lay).ellipse([x0, y0, x1, y1], fill=col + (int(255 * a),))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(cam.S(blur))))


# ================================================================================================ rooms, lines, bricks
@kind('room', params={'fill': 'c', 'back': 'c', 'left': 'c', 'right': 'c', 'ceiling': 'c', 'floor': 'c', 'line': 'n',
                      'ceiling line': 'n', 'order': 's', 'canvas': 'nums'},
      defaults={'fill': None, 'back': None, 'left': None, 'right': None, 'ceiling': None, 'floor': None, 'line': 2.4,
                'ceiling line': 0, 'order': 'fill ceiling left right back floor', 'canvas': CANVAS}, band=True)
def room(p, img, cam, a, t):
    """A room seen from inside: x, z give the back wall (its face); the side walls, ceiling and floor run from its
    corners out to the picture's corners. Each surface is drawn only when its colour is given, in `order`. A floor
    alone (no back wall) is a room with only `floor`: x, z then give its far edge (z the same at both ends)."""
    pc = a['piece']
    cx0, cy0, cx1, cy1 = a['canvas']
    tl, tr, bl, br = pc.screen(cx0, cy0), pc.screen(cx1, cy0), pc.screen(cx0, cy1), pc.screen(cx1, cy1)
    w, h, lw = a['w'], a['h'], a['line']
    shapes = {'fill': (quad(tl[0], tl[1], br[0], br[1]), None),
              'ceiling': ([tl, tr, (w, 0), (0, 0)], a['ceiling line'] or lw),
              'left': ([tl, (0, 0), (0, h), bl], lw), 'right': ([tr, (w, 0), (w, h), br], lw),
              'back': (quad(0, 0, w, h), lw), 'floor': ([bl, (0, h), (w, h), br], lw)}
    for s in a['order'].split():
        if a[s] is not None:
            pts, l = shapes[s]
            p.poly(pts, a[s], INK if l else None, l or 4)


@kind('lines', params={'n': 'n', 'start': 'n', 'first': 'm', 'every': 'm', 'grow': 'n', 'inset': 'm', 'drop': 'm',
                       'colour': 'c', 'width': 'n'},
      defaults={'n': 10, 'start': 0, 'first': 0.0, 'every': 60, 'grow': 0.0, 'inset': 0.0, 'drop': 0.0,
                'colour': (150, 150, 150), 'width': 1.4}, band=True)
def lines(p, img, cam, a, t):
    """Ruled lines across a face (brick courses, a van floor's ribs, lino joints, floor tiles): n of them, the first
    `first` down, `every` apart (each gap `grow` times longer than the last, for a floor going away), `inset` in from
    both sides, each falling `drop` from left to right."""
    for k in range(int(a['start']), int(a['start']) + int(a['n'])):
        y = a['first'] + a['every'] * k * (1 + a['grow'] * k)
        p.line([(a['inset'], y), (a['w'] - a['inset'], y + a['drop'])], a['colour'], a['width'])


@kind('brick marks', params={'colour': 'c', 'brick width': 'm', 'brick height': 'm', 'n': 'n', 'line': 'n'},
      defaults={'colour': (226, 216, 190), 'brick width': 40, 'brick height': 22, 'n': 30, 'line': 1.0}, band=True)
def brick_marks(p, img, cam, a, t):
    """Painted brick: scattered patches of a few bricks over the face (the house's brick, never a ruled grid)."""
    bricks_in(p, (0, 0, a['w'], a['h']), a['colour'], a['seed'], cw=a['brick width'], ch=a['brick height'],
              n=int(a['n']), lw=a['line'])


# ================================================================================================ strokes, studs, light
@kind('stroke', params={'to': 'pt', 'via': 'pts', 'colour': 'c', 'width': 'n', 'core': 'n'},
      defaults={'to': (0, 0), 'via': [], 'colour': (150, 154, 160), 'width': 2.0, 'core': 0},
      box=lambda a: (min(0, a['to'][0]) - 4, min(0, a['to'][1]) - 4, max(0, a['to'][0]) + 4, max(0, a['to'][1]) + 4))
def stroke(p, img, cam, a, t):
    """A painted line from its point to `to` (through `via`): a seam, a rail, a pipe; `core` an ink line along it."""
    pts = [(0, 0)] + list(a['via']) + [a['to']]
    p.line(pts, a['colour'], a['width'])
    if a['core']:
        p.line(pts, INK, a['core'])


@kind('studs', params={'points': 'pts', 'radius': 'm', 'colour': 'c', 'line': 'n'},
      defaults={'points': [], 'radius': 5, 'colour': (150, 158, 166), 'line': 1.0}, band=True)
def studs(p, img, cam, a, t):
    """Round studs (rivets, bolts) at the points given (metres)."""
    r = a['radius']
    for x, y in a['points']:
        p.ell(x, y, r, r, a['colour'], INK if a['line'] else None, a['line'] or 1)


@kind('oval', params={'rx': 'm', 'ry': 'm', 'colour': 'c', 'line': 'n'},
      defaults={'rx': 120, 'ry': 26, 'colour': (236, 240, 230), 'line': 2.0},
      box=lambda a: (-a['rx'], -a['ry'], a['rx'], a['ry']))
def oval(p, img, cam, a, t):
    """A flat oval (a ceiling light seen from below, a round plate), its middle the point."""
    p.ell(0, 0, a['rx'], a['ry'], a['colour'], INK if a['line'] else None, a['line'] or 1)


@kind('wash', params={'colour': 'nums'}, defaults={'colour': (30, 40, 70, 60)}, overall=True)
def wash(p, img, cam, a, t):
    """A light over the whole picture (dim cold light in a van): a flat tint, colour R G B and its strength A."""
    img.alpha_composite(Image.new('RGBA', img.size, tuple(int(v) for v in a['colour'])))


@kind('glow', params={'colour': 'c', 'strength': 'n', 'blur': 'n', 'sweep': 'm', 'period': 'n'},
      defaults={'colour': (240, 210, 150), 'strength': 0.1, 'blur': 120, 'sweep': 0, 'period': 1.6}, band=True)
def glow(p, img, cam, a, t):
    """A soft oval of light over its box (a TV's glow on a wall, a passing street light), sliding `sweep` to the
    left every `period` seconds when given."""
    u = (t / a['period']) % 1.0 if a['sweep'] else 0.0
    dx = -a['sweep'] * u
    _soft(img, cam, (dx, 0, a['w'] + dx, a['h']), a['colour'], a['strength'], a['blur'])


@kind('flicker', params={'strength': 'n'}, defaults={'strength': 1.0}, overall=True)
def flicker(p, img, cam, a, t):
    """A TV's light on everyone (over the cast): the room gone blue-dark and a cool glow from above the lens, its
    level jumping as the picture cuts (a fixed, irregular pattern, never a smooth pulse)."""
    s = a['strength']
    r = random.Random(int(t * 4))
    k = s * (0.55 + 0.45 * r.random())
    img.alpha_composite(Image.new('RGBA', img.size, (8, 16, 60, int(34 * s))))
    _soft(img, cam, (-100, 400, 1180, 1300), (120, 170, 255), 0.16 * k, 220)


# ================================================================================================ the van
VAN_W = (196, 202, 208)
VAN_D = (150, 158, 166)


@kind('cctv sticker', ref=800, params={'colour': 'c'}, defaults={'colour': (246, 214, 60)})
def cctv_sticker(p, img, cam, a, t):
    """A square yellow CCTV warning sticker with a camera on it."""
    p.poly(wob(quad(0, 0, a['w'], a['h']), 0.8, a['seed']), a['colour'], INK, 1.6)
    p.ell(40, 34, 16, 10, (40, 40, 44), None)
    p.poly(quad(22, 52, 58, 62), (40, 40, 44), None)


@kind('vent', ref=800, params={'colour': 'c', 'slats': 'c', 'n': 'n'},
      defaults={'colour': (220, 222, 226), 'slats': dk(VAN_W, 0.7), 'n': 4})
def vent(p, img, cam, a, t):
    """An air vent: a plate with slats across it."""
    p.poly(quad(0, 0, a['w'], a['h']), a['colour'], INK, 2.0)
    for k in range(int(a['n'])):
        p.line([(12, 10 + 10 * k), (a['w'] - 12, 10 + 10 * k)], a['slats'], 1.6)


@kind('street window', ref=800, params={'glass': 'c', 'slant': 'm', 'period': 'n', 'bar': 'c'},
      defaults={'glass': (24, 28, 40), 'slant': 60, 'period': 1.6, 'bar': (60, 64, 70)})
def street_window(p, img, cam, a, t):
    """A small tinted window in a side wall (its near top corner `slant` higher than the far one) with a street's
    lights sliding past it at night, every `period` seconds, and a bar down the middle."""
    import body as B
    w, h, s = a['w'], a['h'], a['slant']
    win = [(w, 0), (0, s), (0, h), (w, h)]
    p.poly(win, a['glass'], INK, 2.6)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    lp = B.Pen(lay, cam)
    for k in range(5):
        u = ((t / a['period']) + k / 5) % 1.0
        x = w * u
        y = 110 + 40 * k
        lp.poly(quad(x - 22, y, x + 22, y + 8), (240, 200, 110, 210) if k % 2 else (236, 236, 240, 200), None)
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).polygon([cam.P(*q) for q in win], fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay)[..., 3], np.asarray(m))))
    img.alpha_composite(lay)
    p.poly(win, None, INK, 2.6)
    p.line([(w / 2, s / 2), (w / 2, h)], a['bar'], 3.0)


@kind('moulded seat', ref=800, params={'colour': 'c', 'front': 'c', 'top': 'm', 'flare': 'm'},
      defaults={'colour': mix(VAN_W, VAN_D, 0.5), 'front': dk(VAN_W, 0.78), 'top': 180, 'flare': 30})
def moulded_seat(p, img, cam, a, t):
    """A moulded plastic bench seat across a wall: its top `top` deep, its front flaring out `flare` at the floor."""
    w, h, tp, f = a['w'], a['h'], a['top'], a['flare']
    p.poly(wob(quad(0, 0, w, tp), 1.2, a['seed']), a['colour'], INK, 2.6)
    p.poly([(0, tp), (w, tp), (w + f, h), (-f, h)], a['front'], INK, 2.4)


@kind('door leaf', ref=2000, params={'colour': 'c', 'hatch': 'c', 'mesh': 'c', 'far': 'r'},
      defaults={'colour': (138, 144, 152), 'hatch': (60, 64, 70), 'mesh': (110, 116, 124), 'far': (360, 2500)})
def door_leaf(p, img, cam, a, t):
    """An open steel door right by the lens, seen from inside (a van's cubicle): its near edge the box's right side,
    its far edge `far` (from, to) down from the box's top, a mesh hatch and a lock."""
    w, h = a['w'], a['h']
    f0, f1 = a['far']
    p.poly([(0, f0), (w, 0), (w, h), (0, f1)], a['colour'], INK, 3.0)
    p.poly([(20, 900), (w, 840), (w, 1220), (20, 1200)], a['hatch'], INK, 2.4)
    for k in range(7):
        y = 920 + 42 * k
        p.line([(20, y), (w, y - 8)], a['mesh'], 1.6)
    for k in range(4):
        p.line([(40 + 18 * k, 900), (40 + 18 * k, 1200)], a['mesh'], 1.6)
    p.ell(50, 1600, 14, 30, (90, 96, 104), INK, 1.6)


# ================================================================================================ the cell
CELL = (226, 216, 190)
CELL_D = (198, 186, 160)
MATT = (70, 110, 170)
BLANKET = (84, 128, 92)
DOOR_BLUE = (52, 92, 150)


@kind('barred window', ref=312.5, params={'frame': 'c', 'glass': 'c', 'ground': 'c', 'bars': 'n', 'bar': 'c',
                                          'sill': 'c'},
      defaults={'frame': (210, 226, 236), 'glass': (176, 204, 224), 'ground': (160, 184, 150), 'bars': 4,
                'bar': (70, 74, 80), 'sill': CELL_D})
def barred_window(p, img, cam, a, t):
    """A cell window high in a wall: the sky, a strip of the yard's grass, steel bars, a sill under it."""
    w, h = a['w'], a['h']
    p.poly(wob(quad(0, 0, w, h), 1.2, a['seed']), a['frame'], INK, 3.0)
    p.poly(quad(12, 12, w - 12, h - 12), a['glass'], None)
    p.poly(quad(12, h - 80, w - 12, h - 12), a['ground'], None)
    for k in range(int(a['bars'])):
        p.line([(50 + 40 * k, 4), (50 + 40 * k, h - 4)], a['bar'], 4.0)
    p.poly(quad(-10, h, w + 10, h + 16), a['sill'], INK, 1.8)


@kind('basin', ref=312.5, params={'colour': 'c'}, defaults={'colour': STEEL},
      box=lambda a: (0, -20, a['w'], a['h'] + 70))
def basin(p, img, cam, a, t):
    """A steel wall basin (x, z: its rim's front), its bowl tapering below, a tap behind."""
    w, h, c = a['w'], a['h'], a['colour']
    p.poly(quad(0, 0, w, h), c, INK, 2.0)
    p.poly([(10, h), (w - 10, h), (w - 30, h + 70), (30, h + 70)], dk(c, 0.9), INK, 1.8)
    p.line([(w / 2 + 5, 0), (w / 2 + 5, -20), (w / 2 - 7, -20)], c, 4.0)


@kind('toilet', ref=312.5, params={'colour': 'c'}, defaults={'colour': STEEL}, box=lambda a: (-60, -22, 60, 62))
def toilet(p, img, cam, a, t):
    """A steel prison toilet without a seat (its rim's middle the point)."""
    c = a['colour']
    p.ell(0, 0, 60, 22, c, INK, 2.0)
    p.poly([(-50, 0), (50, 0), (30, 62), (-30, 62)], dk(c, 0.92), INK, 1.8)
    p.ell(0, -4, 44, 13, dk(c, 0.7), None)


@kind('shelf', ref=312.5, params={'colour': 'c', 'leg': 'm'}, defaults={'colour': (190, 160, 120), 'leg': 160},
      box=lambda a: (0, 0, a['w'], a['h'] + a['leg']))
def shelf(p, img, cam, a, t):
    """A shelf-desk on a wall, one bracket leg under it."""
    p.poly(quad(0, 0, a['w'], a['h']), a['colour'], INK, 1.8)
    p.poly(quad(20, a['h'], 34, a['h'] + a['leg']), a['colour'], INK, 1.4)


@kind('pinboard', ref=312.5, params={'colour': 'c'}, defaults={'colour': (176, 140, 100)})
def pinboard(p, img, cam, a, t):
    """A small pinboard with three sheets on it (a letter, a yellow form, a photo)."""
    p.poly(quad(0, 0, a['w'], a['h']), a['colour'], INK, 1.8)
    for x, y, c in ((20, 16, (246, 246, 240)), (80, 30, (230, 220, 160)), (130, 12, (246, 246, 240))):
        p.poly(quad(x, y, x + 42, y + 56), c, INK, 1.0)
        p.line([(x + 6, y + 14), (x + 34, y + 14)], (160, 160, 160), 1.0)


def _blanket(p, top, near, col):
    """Blessed note 17: a prison blanket thrown over the near two-thirds of the mattress, its edge turned down in a
    lighter fold, soft rucks along it, its side hanging over the mattress's room side."""
    (nlx, nly), (flx, fly), (frx, fry), (nrx, nry) = top

    def at(u, v):
        lx, ly = nlx + (flx - nlx) * u, nly + (fly - nly) * u
        rx, ry = nrx + (frx - nrx) * u, nry + (fry - nry) * u
        return lx + (rx - lx) * v, ly + (ry - ly) * v
    e = 0.62
    edge = [at(e + 0.03 * math.sin(7 * v + 1.0), v) for v in (k / 8 for k in range(9))]
    body = [at(0, -0.02)] + edge + [at(e * 0.5, 1.03), at(0, 1.03)]
    hang = [at(0, 1.0), at(e * 0.95, 1.0), (at(e * 0.95, 1.0)[0] + 6, at(e * 0.95, 1.0)[1] + 70),
            (nrx + 10, near - 20), (nrx - 20, near - 4)]
    p.poly(curve(hang, 3), dk(col, 0.78), INK, 2.2)
    p.poly(curve(body, 3), col, INK, 2.4)
    fold = [at(e - 0.07 + 0.02 * math.sin(5 * v), v) for v in (k / 8 for k in range(9))]
    p.poly(curve(edge + fold[::-1], 3), mix(col, (255, 255, 255), 0.22), INK, 1.8)
    for u, v0, v1 in ((0.2, 0.15, 0.55), (0.36, 0.45, 0.85), (0.12, 0.6, 0.9)):
        p.line(curve([at(u, v0), at(u + 0.05, (v0 + v1) / 2), at(u, v1)], 3), dk(col, 0.72), 2.0)


@kind('prison bed', ref=400, params={'mattress': 'c', 'blanket': 'c', 'frame': 'c'},
      defaults={'mattress': MATT, 'blanket': BLANKET, 'frame': (90, 96, 104)}, box=lambda a: (0, 0, 740, 690))
def prison_bed(p, img, cam, a, t):
    """A metal-framed bed along a room's left wall, seen from the door end (x, z: its top-left corner, the far
    pillow end): a thin mattress, a blanket thrown over its near two-thirds, a flat pillow, steel legs."""
    near, far, bx = 610, 70, 530                       # the near end, the far end, the wall's corner (own units)
    top = [(0, near - 120), (bx - 10, far - 60), (bx + 210, far - 50), (680, near - 120)]
    p.poly(top, a['mattress'], INK, 2.6)
    p.poly(quad(0, near - 120, 680, near - 40), dk(a['mattress'], 0.78), INK, 2.4)
    _blanket(p, top, near, a['blanket'])
    p.poly([(bx + 10, far - 70), (bx + 190, far - 62), (bx + 200, far - 38), (bx + 20, far - 44)],
           (236, 236, 232), INK, 1.8)
    for x in (100, 660):
        p.poly(quad(x, near - 40, x + 18, near + 80), a['frame'], INK, 1.6)
    p.poly(quad(bx + 196, far - 50, bx + 208, far + 20), a['frame'], INK, 1.4)


@kind('cell door', ref=312.5, params={'colour': 'c', 'opening': 'c', 'landing': 'c', 'rail': 'c', 'netting': 'c'},
      defaults={'colour': DOOR_BLUE, 'opening': (76, 80, 90), 'landing': (232, 230, 222), 'rail': (60, 120, 160),
                'netting': (210, 214, 210)}, box=lambda a: (0, 0, 250, 1500))
def cell_door(p, img, cam, a, t):
    """A cell's steel door standing open on the right-hand wall (x, z: the box round it), the landing beyond: its
    blue railing, the suicide netting, the door leaf opened in with its observation slot."""
    p.poly([(40, 170), (250, 0), (250, 1500), (40, 1100)], a['opening'], INK, 2.4)
    p.poly([(50, 220), (250, 80), (250, 700), (50, 710)], a['landing'], None)
    for y in (680, 760):
        p.line([(50, y), (250, y - 30)], a['rail'], 4.0)
    p.poly([(50, 800), (250, 780), (250, 940), (50, 920)], a['netting'], None)
    for k in range(8):
        x = 60 + 22 * k
        p.line([(x, 800), (x + 10, 930)], (150, 150, 150), 1.0)
    p.poly([(0, 180), (50, 170), (50, 1100), (0, 1120)], a['colour'], INK, 2.6)
    p.poly([(10, 400), (40, 396), (40, 460), (10, 464)], (40, 44, 50), INK, 1.4)


# ================================================================================================ the cot from above
@kind('cot from above', ref=1000, params={'frame': 'c', 'mattress': 'c', 'pillow': 'c'},
      defaults={'frame': STEEL, 'mattress': MATT, 'pillow': (236, 234, 226)},
      box=lambda a: (-34, -40, a['w'] + 34, a['h'] + 40))
def cot_from_above(p, img, cam, a, t):
    """A cot seen from straight above (x, z: the mattress): the steel frame round it, the thin mattress, a flat
    pillow at the top (a soft rectangle with rounded corners) with a crease in it."""
    w, h = a['w'], a['h']
    p.poly(quad(-34, -40, w + 34, h + 40), a['frame'], INK, 2.6)
    p.poly(quad(0, 0, w, h), a['mattress'], INK, 2.4)
    px0, px1, py0, py1 = 110, w - 110, 36, 290
    p.poly(curve([(px0 + 26, py0), (px1 - 26, py0 - 4), (px1, py0 + 30), (px1 + 6, py1 - 40), (px1 - 22, py1),
                  (px0 + 22, py1 + 4), (px0 - 6, py1 - 40), (px0, py0 + 32)], 3), a['pillow'], INK, 2.4)
    p.line([(80, 170), (150, 178)], (206, 204, 196), 2.0)


@kind('blanket from above', ref=1250, params={'colour': 'c', 'sheet': 'c', 'edge': 'm'},
      defaults={'colour': BLANKET, 'sheet': (232, 230, 222), 'edge': 1050},
      box=lambda a: (-22, a['edge'] - 8, a['w'] + 22, a['h'] + 30))
def blanket_from_above(p, img, cam, a, t):
    """A blanket over someone lying on a cot, seen from above (x, z: the mattress; stand it nearer the lens than
    them): from `edge` down, the sheet folded over it, folds over the legs, two bumps for the feet."""
    w, h, e, c = a['w'], a['h'], a['edge'], a['colour']
    m = w / 2
    p.poly([(-14, e + 10), (120, e - 8), (w - 140, e - 4), (w + 14, e + 14), (w + 22, h + 30), (-22, h + 30)],
           c, INK, 2.4)
    p.poly([(-14, e + 10), (120, e - 8), (w - 140, e - 4), (w + 14, e + 14), (w + 10, e + 80), (-8, e + 74)],
           a['sheet'], INK, 2.2)
    for fx, fy in ((-120, 360), (60, 520), (-40, 700)):
        p.line(curve([(m + fx, e + fy), (m + fx + 40, e + fy + 60), (m + fx + 30, e + fy + 160)], 3), dk(c, 0.8), 2.0)
    for fx in (-70, 70):
        p.poly(curve([(m + fx - 52, h - 150), (m + fx, h - 196), (m + fx + 52, h - 150), (m + fx + 44, h - 100),
                      (m + fx - 44, h - 100)], 3), mix(c, (255, 255, 255), 0.08), INK, 2.0)


# ================================================================================================ the phone room
@kind('pin phone', ref=1000, params={'hood': 'c', 'empty': 'n', 'label': 's'},
      defaults={'hood': (50, 84, 136), 'empty': 0, 'label': 'PIN PHONE'}, box=lambda a: (0, 0, 650, 820))
def pin_phone(p, img, cam, a, t):
    """A prison PIN phone on the wall under its blue acoustic hood (x, z: the hood's box): the hood's back, cheeks
    and canopy, its perforations, the steel phone with keypad and screen, the cradle, a label over it. empty 1: the
    handset hung up, its cord coiled below (someone else's phone holds the handset in his hand)."""
    import body as B
    import blessed_sets as BS                     # the house lettering
    lc = B.Local(cam, -180, -300, 1.0)            # drawn in the booth's original units (the hood's corner 180, 300)
    q = lambda x0, y0, x1, y1: quad(x0, y0, x1, y1)
    hd = a['hood']
    pp = B.Pen(img, lc)
    pp.poly(q(250, 380, 760, 1040), (214, 214, 208), INK, 2.4)
    pp.poly([(250, 380), (180, 300), (180, 1120), (250, 1040)], hd, INK, 2.8)
    pp.poly([(760, 380), (830, 300), (830, 1120), (760, 1040)], (hd[0] + 10, hd[1] + 12, hd[2] + 14), INK, 2.8)
    pp.poly([(180, 300), (830, 300), (760, 380), (250, 380)], (hd[0] - 6, hd[1] - 8, hd[2] - 10), INK, 2.8)
    pp.poly(q(250, 380, 760, 430), (180, 180, 176), None)
    for k in range(9):
        for j in range(5):
            pp.ell(300 + k * 50, 450 + j * 120, 3, 3, (186, 186, 180), None)
    pp.poly(wob(q(420, 520, 600, 860), 1.0, a['seed']), STEEL, INK, 2.6)
    for k in range(4):
        for j in range(3):
            pp.poly(q(470 + j * 30, 660 + k * 34, 494 + j * 30, 686 + k * 34), (230, 232, 234), INK, 1.0)
    pp.poly(q(450, 560, 570, 620), (40, 60, 50), INK, 1.4)
    pp.poly(q(404, 540, 426, 760), (120, 124, 128), INK, 1.4)
    pp.poly(q(408, 548, 422, 752), (60, 62, 66), None)
    pp.poly(q(500, 860, 520, 900), (150, 156, 160), INK, 1.4)
    if a['empty']:
        pp.poly(wob(q(388, 520, 436, 790), 0.8, 9), (40, 42, 46), INK, 2.2)
        cord = [(510, 900)] + [(520 + 26 * math.sin(k * 1.3), 930 + k * 14) for k in range(12)] + \
               [(436, 1000), (412, 790)]
        pp.line(cord, (150, 156, 162), 6.0)
        pp.line(cord, INK, 1.0)
    if a['label']:
        BS.sign(img, lc, a['label'], 510, 486, 150, (40, 40, 44))


@kind('notice', ref=1000, params={'colour': 'c', 'text': 's', 'rows': 'n', 'pin': 'c'},
      defaults={'colour': (250, 250, 246), 'text': '', 'rows': 0, 'pin': (200, 40, 40)})
def notice(p, img, cam, a, t):
    """A notice pinned to a wall: a sheet, a heading scaled to its width, ruled lines of text, a red drawing pin."""
    import blessed_sets as BS
    w, h = a['w'], a['h']
    p.poly(wob(quad(0, 0, w, h), 1.0, a['seed']), a['colour'], INK, 1.6)
    if a['text']:
        BS.sign(img, cam, a['text'], w / 2, 36, w * 0.74, (40, 40, 44))
    for j in range(int(a['rows']) or (3 if h < 240 else 4)):
        p.line([(18, 80 + j * 36), (w - 22 - 16 * (j % 2), 80 + j * 36)], (150, 150, 150), 2.0)
    p.ell(w / 2, 10, 5, 5, a['pin'], INK, 1.0)


# ================================================================================================ the association room
@kind('noticeboard', ref=250, params={'colour': 'c', 'n': 'n'}, defaults={'colour': (150, 112, 74), 'n': 7})
def noticeboard(p, img, cam, a, t):
    """A cork noticeboard with sheets pinned on it in rows of four (white, yellow, blue), each with lines of text."""
    p.poly(wob(quad(0, 0, a['w'], a['h']), 0.8, a['seed']), a['colour'], INK, 2.4)
    r = random.Random(a['seed'] + 2)
    for k in range(int(a['n'])):
        x, y = 20 + (k % 4) * 70 + r.uniform(-6, 6), 20 + (k // 4) * 110 + r.uniform(-6, 6)
        p.poly(wob(quad(x, y, x + 58, y + 80), 0.6, a['seed'] + 9 + k),
               ((240, 238, 228), (250, 236, 150), (220, 230, 240))[k % 3], INK, 1.2)
        for q in range(3):
            p.line([(x + 8, y + 20 + 16 * q), (x + 48, y + 20 + 16 * q)], (150, 150, 150), 1.2)
        p.ell(x + 29, y + 6, 4, 4, (200, 40, 40), None)


@kind('caged clock', ref=250, params={'face': 'c', 'cage': 'c'},
      defaults={'face': (240, 238, 230), 'cage': (90, 96, 104)}, box=lambda a: (-60, -60, 60, 60))
def caged_clock(p, img, cam, a, t):
    """A wall clock behind a steel cage (an institution's), its middle the point."""
    p.ell(0, 0, 60, 60, a['face'], INK, 2.4)
    p.line([(0, 0), (0, -36)], INK, 2.6)
    p.line([(0, 0), (28, 8)], INK, 2.6)
    for k in range(5):
        p.line([(-60 + 30 * k, -58), (-60 + 30 * k, 58)], a['cage'], 1.6)


@kind('wired door', ref=250, params={'colour': 'c', 'glass': 'c', 'wire': 'c'},
      defaults={'colour': (110, 112, 116), 'glass': (60, 70, 86), 'wire': (90, 100, 116)})
def wired_door(p, img, cam, a, t):
    """A plain steel door with a panel of wired glass in its top half."""
    p.poly(quad(0, 0, a['w'], a['h']), a['colour'], INK, 2.4)
    p.poly(quad(30, 50, 150, 230), a['glass'], INK, 1.6)
    for k in range(6):
        p.line([(30 + 20 * k, 50), (30 + 20 * k, 230)], a['wire'], 1.0)
        p.line([(30, 50 + 30 * k), (150, 50 + 30 * k)], a['wire'], 1.0)


@kind('pool table', ref=250, params={'wood': 'c', 'dark': 'c', 'cloth': 'c'},
      defaults={'wood': (104, 66, 40), 'dark': (70, 44, 28), 'cloth': (40, 110, 70)}, box=lambda a: (0, 0, 566, 296))
def pool_table(p, img, cam, a, t):
    """A pub pool table seen from its long side, a little from above (x, z: its box): a solid wooden cabinet to the
    floor, a cushioned rim round the green cloth, six pockets, three balls, the coin slot (Blessed's note N8)."""
    f, n, fl = 12, 80, 296
    a0, a1, b0, b1 = 68, 512, 16, 550
    wood, dark = a['wood'], a['dark']
    p.poly([(b0, n), (a0, f), (a0, fl - 80), (b0, fl)], dk(wood, 0.8), INK, 2.2)
    p.poly([(b1, n), (a1, f), (a1, fl - 80), (b1, fl)], dk(wood, 0.8), INK, 2.2)
    p.poly([(a0 - 14, f - 12), (a1 + 14, f - 12), (b1 + 16, n + 10), (b0 - 16, n + 10)], wood, INK, 2.4)
    p.poly([(a0, f), (a1, f), (b1, n), (b0, n)], a['cloth'], INK, 2.0)
    p.poly(quad(b0 - 16, n + 10, b1 + 16, fl), wood, INK, 2.4)
    p.poly(quad(b0 - 10, fl - 26, b1 + 10, fl), dark, INK, 1.8)
    p.poly(quad(260, n + 60, 320, n + 96), (150, 150, 156), INK, 1.6)
    p.line([(272, n + 78), (308, n + 78)], INK, 2.0)
    for x, y in ((a0, f), ((a0 + a1) / 2, f - 2), (a1, f), (b0, n), ((b0 + b1) / 2, n + 2), (b1, n)):
        p.ell(x, y, 13, 7, (20, 20, 22), INK, 1.0)
    for k, (x, y) in enumerate(((130, 52), (190, 40), (360, 62))):
        p.ell(x, y, 9, 9, ((200, 40, 40), (240, 200, 60), (40, 70, 170))[k], INK, 1.2)


# ================================================================================================ the TV
@kind('wall tv', ref=1000, params={'colour': 'c', 'screen': 'c', 'bracket': 'n'},
      defaults={'colour': (24, 24, 28), 'screen': (40, 50, 70), 'bracket': 1},
      box=lambda a: (0, -320 if a['bracket'] else 0, a['w'], a['h']))
def wall_tv(p, img, cam, a, t):
    """A TV on a wall bracket (x, z: the set): the wall plate and its bolts, the arm, the set, the picture (the
    feed the film passes in, else a dark screen), a sheen on the glass, the standby light."""
    import body as B
    w, h = a['w'], a['h']
    mx = w / 2
    if a['bracket']:
        p.poly(quad(mx - 100, -320, mx + 100, -270), (70, 72, 78), INK, 2.0)
        for x in (mx - 80, mx + 80):
            p.ell(x, -295, 6, 6, (140, 144, 150), INK, 1.0)
        p.poly(quad(mx - 40, -270, mx + 40, 160), (50, 52, 56), INK, 2.0)
    p.poly(wob(quad(0, 0, w, h), 0.8, a['seed']), a['colour'], INK, 3.2)
    sx0, sy0, sx1, sy1 = 26, 26, w - 26, h - 34
    feed = a.get('feed')
    if feed is not None:
        X0, Y0 = cam.P(sx0, sy0)
        X1, Y1 = cam.P(sx1, sy1)
        img.alpha_composite(feed.convert('RGBA').resize((int(X1 - X0), int(Y1 - Y0)), Image.LANCZOS),
                            (int(X0), int(Y0)))
    else:
        p.poly(quad(sx0, sy0, sx1, sy1), a['screen'], None)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    B.Pen(lay, cam).poly([(sx0, sy0), (sx0 + 300, sy0), (sx0 + 120, sy1), (sx0, sy1)], (255, 255, 255, 26), None)
    img.alpha_composite(lay)
    p.ell(w - 70, h - 16, 6, 4, (220, 60, 50), None)


# ================================================================================================ the night cell
# Patriots 5 chat 6 (Sam, 28 Nov, note 10: "we will need a different cell due to the scene layout/mood of the opening
# moment"): a cell seen dead ahead, the cot along its back wall, a small grated window high above it, the room night
# blue, one shaft of moonlight on the man on the cot. Every piece here has ref None and draws in TRUE DEPTH through
# a['piece'].P(x, z, d) (as places_site.py does), so the same plan in metres serves the side view, the grate close-ups
# and the view from behind the cot. References: references/blessed/13-cell-bunk-bbc.jpg (steel bed frame with rails,
# a thin mattress, a green prison blanket; a window with bars and a steel mesh grille); a Victorian cell's window
# is small, high and set deep in a thick wall.
NIGHT = (92, 112, 170)                       # the night's colour: every colour multiplied by it (moonless room light)
MOON = (214, 228, 255)                       # moonlight


def _D(a):
    pc = a['piece']
    return pc, (lambda x, z, d: pc.P(x, z, d)), (lambda d: pc.L.ppm(d) / pc.k)


def _box(p, P, x0, x1, z0, z1, d0, d1, col, lw=2.0, faces='front top'):
    """A box in metres (x across, z up, d from the lens: d0 near, d1 far): its front face and, where the camera sees
    them, its top (camera above it), its left or right side (the box beside the lens's line)."""
    if 'top' in faces:
        p.poly([P(x0, z1, d0), P(x1, z1, d0), P(x1, z1, d1), P(x0, z1, d1)], mix(col, (255, 255, 255), 0.12), INK, lw)
    if 'left' in faces:
        p.poly([P(x0, z0, d0), P(x0, z1, d0), P(x0, z1, d1), P(x0, z0, d1)], dk(col, 0.8), INK, lw)
    if 'right' in faces:
        p.poly([P(x1, z0, d0), P(x1, z1, d0), P(x1, z1, d1), P(x1, z0, d1)], dk(col, 0.8), INK, lw)
    if 'front' in faces:
        p.poly([P(x0, z0, d0), P(x1, z0, d0), P(x1, z1, d0), P(x0, z1, d0)], col, INK, lw)


@kind('cot along wall', params={'frame': 'c', 'mattress': 'c', 'blanket': 'c', 'pillow': 'c', 'rail': 'n',
                                'pillow end': 's', 'blanket from': 'n'},
      defaults={'frame': STEEL, 'mattress': (64, 96, 70), 'blanket': (70, 110, 76), 'pillow': (228, 228, 222),
                'rail': 0.05, 'pillow end': 'left', 'blanket from': 0.45})
def cot_along_wall(p, img, cam, a, t):
    """A prison cot standing along a wall, seen in true depth from anywhere in the room (x: its ends, z: the floor to
    the mattress top, depth: its near side to its far side, against the wall). A steel tube frame on four legs, a
    side rail under the mattress, a thin green mattress, a flat pillow at `pillow end`, a green blanket folded over
    the other part of the mattress from `blanket from` (0 the pillow end, 1 the far end)."""
    pc, P, ppm = _D(a)
    x0, x1, z0, z1, d0, d1 = pc.x0, pc.x1, pc.z0, pc.z1, pc.d0, pc.d1
    mt = 0.11                                          # the mattress's thickness
    zr = z1 - mt                                       # the frame's top rail
    tube = a['rail']
    left_seen, right_seen = x0 > 0, x1 < 0             # the lens (at x 0) sees an end only from beyond it
    for x in (x0 + 0.02, x1 - 0.02 - tube):            # the far legs (behind the mattress, against the wall)
        _box(p, P, x, x + tube, z0, zr, d1 - tube - 0.02, d1 - 0.02, dk(a['frame'], 0.75), 1.4, 'front')
    for x in (x0 + 0.02, x1 - 0.02 - tube):            # the near legs
        _box(p, P, x, x + tube, z0, zr, d0 + 0.02, d0 + 0.02 + tube, a['frame'], 1.6, 'front')
    _box(p, P, x0, x1, zr - 0.07, zr, d0 + 0.02, d0 + 0.02 + tube, a['frame'], 1.8, 'front')     # the side rail
    side = ('left' if left_seen else '') + (' right' if right_seen else '')
    _box(p, P, x0, x1, zr, z1, d0, d1, a['mattress'], 2.2, 'top front ' + side)                 # the mattress
    # the pillow: a soft slab at one end, its top a little rounded
    pe = a['pillow end']
    px0, px1 = (x0 + 0.04, x0 + 0.5) if pe == 'left' else (x1 - 0.5, x1 - 0.04)
    pz = z1 + 0.13
    pf, pb = d0 + 0.1, d1 - 0.08
    top = [P(px0 + 0.02, z1 + 0.02, pf), P(px0 + 0.06, pz, pf + 0.05), P(px1 - 0.06, pz, pf + 0.05),
           P(px1 - 0.02, z1 + 0.02, pf), P(px1 - 0.03, z1 + 0.06, pb), P(px0 + 0.03, z1 + 0.06, pb)]
    p.poly(curve(top, 3), a['pillow'], INK, 1.8)
    face = [P(px0, z1, pf), P(px0 + 0.02, z1 + 0.07, pf - 0.005), P(px0 + 0.06, pz, pf + 0.05),
            P(px1 - 0.06, pz, pf + 0.05), P(px1 - 0.02, z1 + 0.07, pf - 0.005), P(px1, z1, pf)]
    p.poly(curve(face, 3), dk(a['pillow'], 0.86), INK, 1.8)
    p.line(curve([P(px0 + 0.16, z1 + 0.09, pf + 0.02), P((px0 + px1) / 2, z1 + 0.1, pf + 0.06),
                  P(px1 - 0.18, z1 + 0.09, pf + 0.03)], 3), dk(a['pillow'], 0.75), 1.4)
    # the blanket: folded over the far part, hanging over the near side a little
    u = a['blanket from']
    bx0, bx1 = (x0 + (x1 - x0) * u, x1) if pe == 'left' else (x0, x1 - (x1 - x0) * u)
    bz = z1 + 0.035
    top = [P(bx0, bz, d0 - 0.01), P(bx1 + 0.01, bz, d0 - 0.01), P(bx1 + 0.01, bz, d1 - 0.02), P(bx0, bz, d1 - 0.02)]
    p.poly(top, a['blanket'], INK, 2.0)
    hang = [P(bx0, bz, d0 - 0.01), P(bx1 + 0.01, bz, d0 - 0.01), P(bx1 + 0.01, zr - 0.06, d0 - 0.015),
            P((bx0 + bx1) / 2, zr - 0.09, d0 - 0.015), P(bx0, zr - 0.05, d0 - 0.015)]
    p.poly(hang, dk(a['blanket'], 0.8), INK, 2.0)
    fx = bx0 + 0.09 if pe == 'left' else bx1 - 0.09                       # the fold's turned-back edge
    p.line([P(fx, bz, d0), P(fx + 0.02, bz, d1 - 0.04)], mix(a['blanket'], (255, 255, 255), 0.3), 2.0)


@kind('grated window', params={'frame': 'c', 'sky': 'c', 'reveal': 'c', 'sill': 'c', 'bars': 'n', 'bar': 'c',
                               'mesh': 'c', 'deep': 'n', 'mesh pitch': 'n', 'moon': 'n'},
      defaults={'frame': (150, 156, 164), 'sky': (40, 58, 110), 'reveal': (226, 216, 190), 'sill': (206, 196, 170),
                'bars': 3, 'bar': (70, 74, 80), 'mesh': (120, 126, 134), 'deep': 0.45, 'mesh pitch': 0.045,
                'moon': 1})
def grated_window(p, img, cam, a, t):
    """A small cell window high in a thick wall, in true depth (x, z: the opening on the room's face of the wall,
    depth: that face; `deep`: the wall's thickness). The sky at the outer face (night blue, the moon's glow), steel
    bars at the outer face, a steel mesh grille just inside them, the reveal's sides, top and sloping sill running back
    to it in perspective (the lens sees the sides it faces)."""
    pc, P, ppm = _D(a)
    x0, x1, z0, z1, d = pc.x0, pc.x1, pc.z0, pc.z1, pc.d0
    D = d + a['deep']
    out = [P(x0, z0 + 0.06, D), P(x1, z0 + 0.06, D), P(x1, z1, D), P(x0, z1, D)]
    p.poly(out, a['sky'], None)
    if a['moon']:                                      # the moon's glow in the top corner of the sky
        _soft(img, cam, (P(x1 - 0.25, z1 + 0.1, D)[0], P(x1, z1 + 0.1, D)[1], P(x1 + 0.15, z1 - 0.15, D)[0],
                         P(x1, z1 - 0.15, D)[1]), MOON, 0.55, 30)
    # the mesh grille: a fine diamond lattice across the opening, just inside the bars
    dm = D - 0.04
    pitch = a['mesh pitch']
    n = int((x1 - x0 + z1 - z0) / pitch) + 2
    for k in range(n):
        s = k * pitch
        for sg in (1, -1):
            pts = []
            for u in (0.0, 1.0):
                xx = x0 + s - u * (z1 - z0) if sg > 0 else x1 - s + u * (z1 - z0)
                zz = z0 + u * (z1 - z0)
                pts.append((xx, zz))
            (ax, az), (bx, bz) = pts
            # clip to the opening
            def clip(ax, az, bx, bz):
                tl, th = 0.0, 1.0
                for v0, dv, lo, hi in ((ax, bx - ax, x0, x1), (az, bz - az, z0 + 0.06, z1)):
                    if abs(dv) < 1e-9:
                        if v0 < lo or v0 > hi:
                            return None
                        continue
                    t0, t1 = (lo - v0) / dv, (hi - v0) / dv
                    if t0 > t1:
                        t0, t1 = t1, t0
                    tl, th = max(tl, t0), min(th, t1)
                return (tl, th) if tl < th else None
            c = clip(ax, az, bx, bz)
            if c:
                q0 = (ax + (bx - ax) * c[0], az + (bz - az) * c[0])
                q1 = (ax + (bx - ax) * c[1], az + (bz - az) * c[1])
                p.line([P(q0[0], q0[1], dm), P(q1[0], q1[1], dm)], a['mesh'], max(1.0, 0.008 * ppm(dm)))
    nb = int(a['bars'])                                # the bars, upright at the outer face
    for k in range(nb):
        xx = x0 + (x1 - x0) * (k + 1) / (nb + 1)
        p.poly([P(xx - 0.012, z0 + 0.06, D), P(xx + 0.012, z0 + 0.06, D), P(xx + 0.012, z1, D),
                P(xx - 0.012, z1, D)], a['bar'], INK, 1.2)
    p.poly([P(x0, z1 - 0.03, D), P(x1, z1 - 0.03, D), P(x1, z1, D), P(x0, z1, D)], a['bar'], INK, 1.2)
    p.poly(out, None, INK, 1.8)
    # the reveal: top, sides and the sloping sill, from the room's face back to the outer face
    rv = a['reveal']
    p.poly([P(x0, z1, d), P(x1, z1, d), P(x1, z1, D), P(x0, z1, D)], dk(rv, 0.72), INK, 2.0)
    p.poly([P(x0, z0, d), P(x0, z1, d), P(x0, z1, D), P(x0, z0 + 0.06, D)], dk(rv, 0.86), INK, 2.0)
    p.poly([P(x1, z0, d), P(x1, z1, d), P(x1, z1, D), P(x1, z0 + 0.06, D)], dk(rv, 0.86), INK, 2.0)
    p.poly([P(x0, z0, d), P(x1, z0, d), P(x1, z0 + 0.06, D), P(x0, z0 + 0.06, D)], a['sill'], INK, 2.0)


@kind('night', params={'colour': 'nums'}, defaults={'colour': NIGHT}, overall=True)
def night(p, img, cam, a, t):
    """Night over the whole picture (over the cast too, so set and people share one light): every colour multiplied
    by `colour` (R G B), the dark blue of a room lit only from outside."""
    arr = np.asarray(img).astype(np.float32)
    arr[..., :3] *= np.array(a['colour'][:3], np.float32) / 255.0
    img.paste(Image.fromarray(arr.clip(0, 255).astype(np.uint8), 'RGBA'))


@kind('moonbeam', params={'travel': 'nums', 'floor': 'n', 'strength': 'n', 'haze': 'n', 'bars': 'n', 'blur': 'n',
                          'pool': 'n', 'lit': 'n'},
      defaults={'travel': (0.0, -0.5, -1.0), 'floor': 0.0, 'strength': 0.55, 'haze': 0.16, 'bars': 3, 'blur': 0.03,
                'pool': 1.0, 'lit': 0.0}, overall=True)
def moonbeam(p, img, cam, a, t):
    """One shaft of moonlight through a window (x, z: the window's opening, depth: its outer face), in true depth:
    the light travels `travel` (x, depth, z per metre) until it meets the level `floor` (m: the cot's top, the floor).
    A faint haze fills the shaft; where it lands (the pool) it lifts what it falls on back towards full colour, with
    the bars' shadows across it. On the set the shaft's own screen shape is mostly air (the wall behind it is not
    lit), so `lit` is 0 there; a film paints the people standing IN the shaft on their own layer and calls
    moon_on(layer, piece) to light them by the shaft (lit, no haze, no pool). Drawn over the night (layer over)."""
    pc, P, ppm = _D(a)
    x0, x1, z0, z1, d = pc.x0, pc.x1, pc.z0, pc.z1, pc.d0
    tx, td, tz = a['travel']
    fl = a['floor']

    def land(x, z):
        k = (z - fl) / -tz
        return x + tx * k, z + tz * k, d + td * k
    win = [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]
    near = [land(x, z) for x, z in win]
    scr = lambda x, z, dd: cam.P(*P(x, z, dd))
    W, H = img.size
    shaft = Image.new('L', (W, H), 0)
    dr = ImageDraw.Draw(shaft)
    pts = [scr(x, z, d) for x, z in win] + [scr(*q) for q in near]
    from scipy.spatial import ConvexHull
    hull = ConvexHull(np.array(pts))
    dr.polygon([tuple(pts[i]) for i in hull.vertices], fill=255)
    pool = Image.new('L', (W, H), 0)
    ImageDraw.Draw(pool).polygon([scr(*q) for q in near], fill=255)
    nb = int(a['bars'])                                 # the bars' shadows across the light
    bars = Image.new('L', (W, H), 255)
    bd = ImageDraw.Draw(bars)
    for k in range(nb):
        xx = x0 + (x1 - x0) * (k + 1) / (nb + 1)
        q = [(xx - 0.014, z0), (xx + 0.014, z0), (xx + 0.014, z1), (xx - 0.014, z1)]
        bd.polygon([scr(x, z, d) for x, z in q] + [scr(*land(x, z)) for x, z in q[::-1]], fill=70)
    blur = max(1.0, a['blur'] * ppm(d) * cam.k if hasattr(cam, 'k') else a['blur'] * ppm(d))
    sh = np.asarray(shaft.filter(ImageFilter.GaussianBlur(blur * 3))).astype(np.float32) / 255
    po = np.asarray(pool.filter(ImageFilter.GaussianBlur(blur * 6))).astype(np.float32) / 255
    ba = np.asarray(bars.filter(ImageFilter.GaussianBlur(blur))).astype(np.float32) / 255
    for alpha, bd in a.get('blockers') or []:           # people in the shaft cast their shadow into the pool (and
        shade = 1.0 - _cast_shadow(alpha, bd, pc, cam, (tx, td, tz), fl, img.size, blur)   # the air under them)
        po, sh = po * shade, sh * (0.35 + 0.65 * shade)
    arr = np.asarray(img).astype(np.float32)
    rgb = arr[..., :3]
    moon = np.array(MOON, np.float32)
    lift = (a['strength'] * np.maximum(a['lit'] * sh, a['pool'] * po) * ba)[..., None]
    # light falling on a thing lifts it back towards its own day colour (undoing the night), tinted by the moon
    night = np.array(NIGHT, np.float32) / 255
    day = np.clip(rgb / night * (moon / 255), 0, 255)
    rgb = rgb + (day - rgb) * lift
    rgb = rgb + (moon - rgb) * (a['haze'] * sh * ba)[..., None]                  # the haze in the air
    arr[..., :3] = rgb
    img.paste(Image.fromarray(arr.clip(0, 255).astype(np.uint8), 'RGBA'))


def _cast_shadow(alpha, bd, pc, cam, travel, fl, size, blur):
    """Where a person (their layer's alpha, standing at depth bd) blocks the moonlight on the level `fl`: each of
    their pixels taken back to the world (a flat figure at depth bd), carried along the light down to the level,
    and put back on the screen; filled and softened. 0-1 per pixel."""
    W, H = size
    ys, xs = np.nonzero(np.asarray(alpha) > 128)
    if not len(xs):
        return np.zeros((H, W), np.float32)
    step = max(1, len(xs) // 40000)
    xs, ys = xs[::step], ys[::step]
    zoom = W / 1080.0
    L = pc.L                                                        # remakes_sets.Level: h, hz, f, cx
    X, Y = xs / zoom, ys / zoom                                     # world px
    x = (X - L.cx) * bd / L.f
    z = L.h - (Y - L.hz) * bd / L.f
    tx, td, tz = travel
    k = np.maximum(0.0, (z - fl) / -tz)
    lx, ld = x + tx * k, bd + td * k
    ok = ld > 0.3
    SX = L.cx + lx[ok] * L.f / ld[ok]
    SY = L.hz - (fl - L.h) * L.f / ld[ok]
    m = np.zeros((H, W), np.float32)
    ix, iy = (SX * zoom).astype(int), (SY * zoom).astype(int)
    keep = (ix >= 0) & (ix < W) & (iy >= 0) & (iy < H)
    m[iy[keep], ix[keep]] = 1.0
    im = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(blur * 2))).astype(np.float32) / 255


def moon_on(layer, piece, cam, t=0.0, lit=0.3, rim=0.95, rim_px=12):
    """Light a layer of people standing in a moonbeam piece's shaft (their own layer, already under the night). The
    light comes from the window BEHIND and above them, so it falls on what faces up and back: a rim along the tops of
    the head, shoulders, arms and lap (`rim`, `rim_px` deep at full size), the side facing us only faintly (`lit`,
    light bounced off the room); the bars' shadows across both; no haze and no pool (those are the set's)."""
    import body as B
    al = np.asarray(layer)[..., 3].astype(np.float32) / 255
    n = max(2, int(rim_px * layer.size[0] / 1080.0))
    above = np.zeros_like(al)
    for k in range(1, n + 1):                         # pixels with open air within n px above them: the top edges
        sh = np.zeros_like(al)
        sh[k:] = al[:-k]
        above = np.maximum(above, 1.0 - sh)
    edge = Image.fromarray((np.clip(above * al, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(n / 3))
    edge = np.asarray(edge).astype(np.float32) / 255 * al
    base = layer.copy()
    a = dict(piece.args, lit=1.0, haze=0.0, pool=0.0, strength=1.0)
    lc = B.Local(cam, piece.ox, piece.oy, piece.k)
    moonbeam(B.Pen(base, lc), base, lc, a, t)        # fully lit by the shaft (bars' shadows too)
    full, dim = np.asarray(base).astype(np.float32), np.asarray(layer).astype(np.float32)
    w = np.clip(lit + (rim - lit) * edge, 0, 1)[..., None]
    out = dim.copy()
    out[..., :3] = dim[..., :3] + (full[..., :3] - dim[..., :3]) * w
    layer.paste(Image.fromarray(out.clip(0, 255).astype(np.uint8), 'RGBA'))
