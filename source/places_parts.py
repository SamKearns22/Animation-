#!/usr/bin/env python3
"""MAP  The places kit's library (ranking item 5; overnight chat 5, 14 Nov): every piece a place is made of, lifted
unchanged in look from Blessed's set file (blessed_sets.py) and made general: each piece draws in its own units
(pixels at REF pixels per metre, from its front face's top-left corner, or from its point for a point piece), so the
kit (places.py) can stand it anywhere in metres and any level camera draws it at its true size.

A KIND is a dict: fn(p, img, cam, a, t) draws it (p a Pen in the piece's own units; a its params, with w and h the
front face's size in those units; a['piece'].P(x, z) turns a point in metres into them); ref = REF (None: no trim,
lines and edges at the house width at any distance); params {name: type} the lines it reads ('c' colour, 'm' metres,
'n' number, 'pt' a point 'X Z', 'nums' numbers, 's' text); looks {NAME: values} its house trims, each with the REF it
was drawn at; overall = True for a light over the whole picture (no depth); band = True for a wall, rail or floor
(not a thing for the collision check).

Map: helpers 40 | walls, rails, floors 60 | courtroom pieces 110 | the table 380
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ed import INK                                     # noqa: E402
from remakes_sets import wob, quad, mix, dk            # noqa: E402

KINDS = {}


def kind(name, ref=None, params=None, looks=None, defaults=None, **extra):
    def reg(fn):
        KINDS[name] = dict(fn=fn, ref=ref, params=params or {}, looks=looks or {}, defaults=defaults or {}, **extra)
        return fn
    return reg


def _lc(v):
    return None if v is None or v == 0 else v


# ================================================================================================ walls, rails, floors
@kind('block', params={'colour': 'c', 'line': 'n', 'wob': 'n', 'no line': 'n'},
      defaults={'colour': (200, 200, 200), 'line': 2.0, 'wob': 0.0}, band=True)
def block(p, img, cam, a, t):
    """A flat coloured face with the house outline (a rail, a ledge, a dado, a band of floor, a strip of wall)."""
    pts = quad(0, 0, a['w'], a['h'])
    if a['wob']:
        pts = wob(pts, a['wob'], a['seed'])
    p.poly(pts, a['colour'], INK if a['line'] else None, a['line'] or 4)


@kind('row', params={'colour': 'c', 'line': 'n', 'n': 'n', 'pitch': 'm'},
      defaults={'colour': (170, 130, 86), 'line': 1.8, 'n': 1, 'pitch': 0.0})
def row(p, img, cam, a, t):
    """n blocks the size of the first, each `pitch` along (bench seats, a strip of panels)."""
    for k in range(int(a['n'])):
        x = k * a['pitch']
        p.poly(quad(x, 0, x + a['w'], a['h']), a['colour'], INK if a['line'] else None, a['line'] or 4)


@kind('panels', ref=250, params={'step': 'm', 'wall': 'c', 'light': 'c'},
      defaults={'wall': (226, 214, 194), 'light': (236, 226, 208), 'step': 120}, band=True)
def panels(p, img, cam, a, t):
    """Tall light-wood wall panels (Blessed's courtroom, the sketches' vertical strokes): each its own width and
    shade between `wall` and `light`, a darker joint."""
    r = random.Random(a['seed'])
    x0, y0, x1, y1 = 0, 0, a['w'], a['h']
    p.poly(quad(x0, y0, x1, y1), a['wall'], None)
    x = x0
    while x < x1:
        w = a['step'] * r.uniform(0.8, 1.2)
        p.poly(quad(x + 3, y0, x + w - 3, y1), mix(a['wall'], a['light'], r.uniform(0, 1)), None)
        p.line([(x, y0), (x + r.uniform(-2, 2), y1)], dk(a['wall'], 0.84), 1.6)
        x += w


@kind('carpet', params={'colour': 'c', 'lines': 'c', 'n': 'n', 'first': 'm', 'every': 'm', 'drop': 'n'},
      defaults={'colour': (150, 96, 70), 'lines': (138, 88, 64), 'n': 9, 'first': 40, 'every': 70, 'drop': 10},
      band=True)
def carpet(p, img, cam, a, t):
    """A band of carpet with a few long pile lines across it."""
    p.poly(quad(0, 0, a['w'], a['h']), a['colour'], None)
    for k in range(int(a['n'])):
        y = a['first'] + k * a['every']
        p.line([(0, y), (a['w'], y + a['drop'])], a['lines'], 1.6)


# ================================================================================================ courtroom pieces
@kind('royal arms', ref=250, params={'size': 'n', 'wall': 'c'}, defaults={'size': 1.0, 'wall': (236, 226, 208)},
      box=lambda a: (-124 * a['size'], -214 * a['size'], 124 * a['size'], 186 * a['size']))
def royal_arms(p, img, cam, a, t):
    """The royal arms (every English Crown Court has them), simplified: a quartered shield in a blue garter, a crown,
    the lion and the unicorn rearing either side, the motto scroll; `size` 1 is about 1.6 m tall."""
    s, cx, cy = a['size'], 0.0, 0.0
    p.ell(cx, cy, 120 * s, 140 * s, (40, 50, 110), INK, 2.4)                              # the garter
    p.ell(cx, cy, 98 * s, 118 * s, a['wall'], None)
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
    """A supporter of the arms, rearing and facing the shield (sg -1: the lion, left; +1: the unicorn, right)."""
    q = lambda u, v: (x - sg * u * s, y + v * s)
    p.poly([q(-30, 120), q(-34, 150), q(-14, 152), q(-10, 120)], col, INK, 1.6)
    p.poly([q(10, 120), q(12, 152), q(30, 150), q(26, 118)], col, INK, 1.6)
    p.poly([q(-36, -10), q(20, -40), q(44, 20), q(30, 124), q(-34, 124), q(-44, 40)], col, INK, 2.0)
    p.poly([q(18, -30), q(66, -60), q(74, -44), q(30, -6)], col, INK, 1.6)
    p.line([q(-40, 100), q(-76, 70), q(-70, 20)], col, 5.0)
    p.line([q(-40, 100), q(-76, 70), q(-70, 20)], INK, 1.0)
    p.ell(q(-70, 18)[0], q(-70, 18)[1], 9 * s, 9 * s, mane, INK, 1.0)
    if not horn:
        cx, cy = q(34, -78)
        ring = [(cx + (46 + (9 if k % 2 else 0)) * s * math.cos(a), cy + (46 + (9 if k % 2 else 0)) * s * math.sin(a))
                for k, a in enumerate([i * 2 * math.pi / 22 for i in range(22)])]
        p.poly(ring, (176, 112, 36), INK, 1.8)
        p.ell(cx, cy, 27 * s, 29 * s, col, INK, 1.6)
        p.ell(cx - 9 * s, cy - 6 * s, 3 * s, 3 * s, INK, None)
        p.ell(cx + 9 * s, cy - 6 * s, 3 * s, 3 * s, INK, None)
        p.poly([(cx - 6 * s, cy + 4 * s), (cx + 6 * s, cy + 4 * s), (cx, cy + 11 * s)], (120, 70, 40), None)
        p.poly([(cx - 5 * s, cy + 15 * s), (cx + 5 * s, cy + 15 * s), (cx, cy + 27 * s)], (200, 40, 40), INK, 1.0)
        p.poly([(cx - 22 * s, cy - 44 * s), (cx - 12 * s, cy - 64 * s), (cx, cy - 48 * s), (cx + 12 * s, cy - 64 * s),
                (cx + 22 * s, cy - 44 * s)], (222, 178, 60), INK, 1.2)
    else:
        p.poly([q(-30, -40), q(-6, -100), q(10, -104), q(-8, -60), q(-22, -10)], mane, INK, 1.6)
        p.poly([q(-2, -104), q(22, -112), q(78, -78), q(84, -62), q(70, -54), q(20, -66), q(4, -50)], col, INK, 1.8)
        p.ell(q(28, -92)[0], q(28, -92)[1], 3.4 * s, 3.4 * s, INK, None)
        p.poly([q(2, -110), q(-4, -132), q(12, -114)], col, INK, 1.2)
        hp = [q(22, -110), q(64, -178), q(32, -106)]
        p.poly(hp, (236, 210, 120), INK, 1.4)
        for k in (0.3, 0.55, 0.78):
            a0 = (hp[0][0] + (hp[1][0] - hp[0][0]) * k, hp[0][1] + (hp[1][1] - hp[0][1]) * k)
            p.line([(a0[0] - 5 * s, a0[1] + 2 * s), (a0[0] + 5 * s, a0[1] - 2 * s)], INK, 1.0)


@kind('clock', ref=250, params={'radius': 'm', 'face': 'c'}, defaults={'radius': 70, 'face': (246, 244, 236)},
      box=lambda a: (-a['radius'], -a['radius'], a['radius'], a['radius']))
def clock(p, img, cam, a, t):
    """A plain wall clock: white face, twelve ticks, hands at ten past twelve."""
    r = a['radius']
    p.ell(0, 0, r, r, a['face'], INK, 2.6)
    for k in range(12):
        an = 2 * math.pi * k / 12
        p.line([(r * 0.8 * math.cos(an), r * 0.8 * math.sin(an)), (r * 64 / 70 * math.cos(an), r * 64 / 70 * math.sin(an))],
               INK, 2.0)
    p.line([(0, 0), (0, -r * 44 / 70)], INK, 3.0)
    p.line([(0, 0), (r * 34 / 70, r * 14 / 70)], INK, 3.0)


DOOR_LOOKS = {   # panel insets in the door's own units (REF 250: px at 250 px per metre)
    'court': dict(side=30, top=40, split=(280, 320), bottom=40, knob=(20, 340, 9), wob=1.4, line=2.6, pline=1.6),
    'jury room': dict(side=20, top=30, split=(280, 320), bottom=20, knob=(150, 300, 7), wob=1.2, line=2.4, pline=1.4),
}


@kind('door', ref=250, params={'colour': 'c', 'panel': 'c', 'knob colour': 'c'}, looks=DOOR_LOOKS,
      defaults=dict(DOOR_LOOKS['court'], colour='oak dark', panel='oak / oak dark 0.4', **{'knob colour': (200, 170, 90)}))
def door(p, img, cam, a, t):
    """A panelled wooden door, shut: two raised panels and a round knob."""
    w, h = a['w'], a['h']
    p.poly(wob(quad(0, 0, w, h), a['wob'], a['seed']), a['colour'], INK, a['line'])
    s0, s1 = a['split']
    p.poly(quad(a['side'], a['top'], w - a['side'], s0), a['panel'], INK, a['pline'])
    p.poly(quad(a['side'], s1, w - a['side'], h - a['bottom']), a['panel'], INK, a['pline'])
    kx, ky, kr = a['knob']
    p.ell(kx, ky, kr, kr, a['knob colour'], INK, 1.2)


CHAIR_LOOKS = {   # the judge's high-backed chair (REF 400)
    'witness view': dict(inset=(20, 24), buttons=(3, 3), first=(70, 70), every=(100, 100), r=5, wob=2.0, line=2.8),
    'close': dict(inset=(28, 36), buttons=(5, 4), first=(70, 90), every=(105, 110), r=6, wob=2.0, line=3.0),
}


@kind('chair back', ref=400, params={'colour': 'c'}, looks=CHAIR_LOOKS,
      defaults=dict(CHAIR_LOOKS['witness view'], colour='chair red'))
def chair_back(p, img, cam, a, t):
    """A tall buttoned leather chair back seen from the front (the judge's): its face, a darker seat panel, buttons."""
    w, h = a['w'], a['h']
    c = a['colour']
    p.poly(wob(quad(0, 0, w, h), a['wob'], a['seed']), c, INK, a['line'])
    ix, iy = a['inset']
    p.poly(quad(ix, iy, w - ix, h), dk(c, 0.82), None)
    nx, ny = a['buttons']
    for k in range(nx):
        for j in range(ny):
            p.ell(a['first'][0] + k * a['every'][0], a['first'][1] + j * a['every'][1], a['r'], a['r'], dk(c, 0.6), None)


@kind('bench', ref=500, params={'colour': 'c', 'dark': 'c', 'light': 'c', 'papers': 'n'},
      defaults={'colour': 'oak', 'dark': 'oak dark', 'light': 'oak light', 'papers': 1})
def bench(p, img, cam, a, t):
    """The judge's bench: a long pale-oak desk front in raised panels (one per 1.7 m at REF), a ledge, papers."""
    x0, x1, ytop, yfloor = 0, a['w'], 0, a['h']
    OAK, OAK_D, OAK_L = a['colour'], a['dark'], a['light']
    p.poly(wob(quad(x0, ytop, x1, yfloor), 1.4, 9), OAK, INK, 3.0)
    p.poly(quad(x0 - 8, ytop - 16, x1 + 8, ytop + 4), OAK_L, INK, 2.4)
    n = max(2, int((x1 - x0) / 170))
    for k in range(n):
        u = x0 + (x1 - x0) * k / n + 16
        v = x0 + (x1 - x0) * (k + 1) / n - 16
        p.poly(quad(u, ytop + 30, v, yfloor - 26), OAK_D, INK, 1.6)
        p.poly(quad(u + 8, ytop + 38, v - 8, yfloor - 34), mix(OAK, OAK_D, 0.4), None)
    if a['papers']:
        p.poly([(x0 + 60, ytop - 16), (x0 + 200, ytop - 16), (x0 + 210, ytop - 30), (x0 + 70, ytop - 30)],
               (246, 244, 236), INK, 1.4)


@kind('microphone', ref=500, params={'tip': 'pt', 'line': 'n'}, defaults={'line': 2.4, 'tip': (0, -100)},
      box=lambda a: (min(0, a['tip'][0]) - 14, min(0, a['tip'][1]) - 9, max(0, a['tip'][0]) + 14, 8))
def microphone(p, img, cam, a, t):
    """A courtroom microphone on a thin curved stalk, from its base (the piece's point) to its tip."""
    base, tip = (0.0, 0.0), a['tip']
    mx = (base[0] * 0.6 + tip[0] * 0.4, base[1] * 0.2 + tip[1] * 0.8 - 20)
    p.line([base, mx, tip], (60, 62, 66), a['line'])
    p.ell(tip[0], tip[1], 6, 9, (34, 34, 36), INK, 1.2, rot=0.6)
    p.ell(base[0], base[1] + 3, 14, 5, (60, 62, 66), INK, 1.2)


@kind('witness box', ref=625, params={'colour': 'c', 'dark': 'c', 'light': 'c'},
      defaults={'colour': 'oak', 'dark': 'oak dark', 'light': 'oak light'})
def witness_box(p, img, cam, a, t):
    """The witness box seen from inside the court, its near corner at the left: the pale-oak front and ledge (over
    the witness's lower body), the near side and its rail, a raised panel. The box from its rail's corner."""
    OAK, OAK_D, OAK_L = a['colour'], a['dark'], a['light']
    w, h = a['w'], a['h']
    q = lambda x0, y0, x1, y1: quad(x0, y0, x1, y1)
    p.poly(wob(q(84, 212, w, h), 1.6, 21), OAK, INK, 3.2)
    p.poly([(14, 22), (84, 42), (84, h), (14, h)], OAK_D, INK, 2.8)
    p.poly([(0, 0), (94, 22), (94, 52), (0, 30)], OAK_L, INK, 2.2)
    p.poly(q(66, 190, w, 228), OAK_L, INK, 2.6)
    p.poly(q(144, 282, 614, 522), OAK_D, INK, 1.8)
    p.poly(q(154, 292, 604, 512), mix(OAK, OAK_D, 0.45), None)


@kind('book', ref=625, params={'colour': 'c', 'width': 'm'}, defaults={'colour': (40, 36, 34), 'width': 150},
      box=lambda a: (0, -20, a['width'] + 10, 0))
def book(p, img, cam, a, t):
    """A closed book lying on a ledge (the oath Bible), seen from a little above; the point is its near left corner."""
    w = a['width']
    p.poly([(0, 0), (w, 0), (w + 10, -20), (12, -20)], a['colour'], INK, 1.6)


WINDOW_FRAME = (200, 196, 186)


@kind('window', ref=250, params={'frame': 'c', 'glass': 'c', 'bars': 'n', 'blind': 'n', 'blind colour': 'c',
                                 'line': 'n'},
      defaults={'frame': WINDOW_FRAME, 'glass': (186, 204, 214), 'bars': 2, 'blind': 0, 'line': 2.2,
                'blind colour': (226, 204, 140)})
def window(p, img, cam, a, t):
    """A window: the frame, the glass, glazing bars, a blind part-way down (blind: the share drawn), a sill."""
    window_box(p, (0, 0, a['w'], a['h']), a['frame'], a['glass'], a['seed'], bars=int(a['bars']),
               blind=a['blind'] or None, blind_colour=a['blind colour'], lw=a['line'])


def window_box(p, box, frame, glass, seed, bars=2, blind=None, blind_colour=(226, 204, 140), lw=2.2):
    """The house window in a box (own units): frame, glass, glazing bars, a blind `blind` of the way down, a sill."""
    x0, y0, x1, y1 = box
    p.poly(wob(quad(x0, y0, x1, y1), 1.2, seed), frame, INK, lw)
    m = max(2.0, (x1 - x0) * 0.08)
    p.poly(quad(x0 + m, y0 + m, x1 - m, y1 - m), glass, None)
    if blind:
        p.poly(quad(x0 + m, y0 + m, x1 - m, y0 + m + (y1 - y0 - 2 * m) * blind), blind_colour, None)
    for k in range(1, int(bars)):
        x = x0 + (x1 - x0) * k / bars
        p.line([(x, y0 + m), (x, y1 - m)], frame, max(1.5, m * 0.6))
    p.line([(x0 + m * 1.4, y0 + m * 1.6), (x0 + (x1 - x0) * 0.35, y0 + m * 1.6)], mix(glass, (255, 255, 255), 0.5), 1.4)
    p.poly(quad(x0 - m * 0.6, y1, x1 + m * 0.6, y1 + m * 0.9), mix(frame, (200, 196, 190), 0.5), INK, lw * 0.7)


def bricks_in(p, box, base, seed, cw=34, ch=13, n=40, lw=1.0):
    """Brick texture without a ruled grid (the house's: Blessed's `bricks`): scattered patches of a few bricks, each
    a touch lighter or darker, with their mortar lines; box and sizes in own units."""
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


PANELLED_LOOKS = {   # a long panelled wooden front (a bench back, a box front, a dock's base); in its own units
    # ledge: (top, bottom, overhang left, overhang right, colour, line, 'before'/'after' the panels)
    # panels: (first x, pitch, count, width, top, bottom); inner: inset (0: none)
    'jury bench back': dict(ref=300, wob=1.2, line=3.0, ledge=(-10, 20, 0, 0, 'oak light', 2.2, 'after'),
                            panels=(54, 160, 9, 132, 30, 330), pcolour='oak / oak dark 0.35', pline=1.4, inner=0),
    'jury box': dict(ref=400, wob=1.2, line=3.0, ledge=(-18, 6, 0, 0, 'oak light', 2.4, 'before'),
                     panels=(54, 160, 9, 132, 34, 260), pcolour='oak / oak dark 0.35', pline=1.4, inner=0),
    'jury box near': dict(ref=500, wob=1.4, line=3.2, ledge=(-26, 8, 0, 0, 'oak light', 2.6, 'after'),
                          panels=(88, 230, 7, 194, 50, 270), pcolour='oak dark', pline=1.6, inner=10,
                          icolour='oak / oak dark 0.4'),
    'dock bench': dict(ref=500, wob=1.2, line=2.6, colour='oak dark', ledge=(-10, 12, 0, 0, 'oak light', 2.0, 'before'),
                       panels=(260, 200, 6, 170, 40, 230), pcolour='oak / oak dark 0.5', pline=1.4, inner=0),
    'dock base': dict(ref=750, wob=1.6, line=3.2, ledge=(-14, 20, 0, 0, 'oak light', 2.6, 'before'),
                      panels=(320, 270, 4, 230, 70, 360), pcolour='oak / oak dark 0.45', pline=1.6, inner=0),
}


@kind('panelled', ref=500, params={'colour': 'c', 'pcolour': 'c', 'icolour': 'c'}, looks=PANELLED_LOOKS,
      defaults=dict(PANELLED_LOOKS['jury box'], colour='oak', icolour='oak / oak dark 0.4'), band=True)
def panelled(p, img, cam, a, t):
    """A long wooden front in raised panels with a ledge along its top (a bench back, a box front, a dock's base)."""
    w, h = a['w'], a['h']
    p.poly(wob(quad(0, 0, w, h), a['wob'], a['seed']), a['colour'], INK, a['line'])
    lt, lb, ol, orr, lc, ll, when = a['ledge']
    from places import colour
    lc = colour(lc, a['piece'].words) if isinstance(lc, str) else lc

    def ledge():
        p.poly(quad(-ol, lt, w + orr, lb), lc, INK, ll)
    if when == 'before':
        ledge()
    x, pitch, n, pw, top, bot = a['panels']
    for k in range(int(n)):
        u = x + k * pitch
        p.poly(quad(u, top, u + pw, bot), a['pcolour'], INK, a['pline'])
        if a['inner']:
            i = a['inner']
            p.poly(quad(u + i, top + i, u + pw - i, bot - i), a['icolour'], None)
    if when == 'after':
        ledge()


@kind('notepad', ref=400, params={'colour': 'c', 'pen': 'c'},
      looks={'pad': dict(ref=400, size=(70, 12, 10), pen=None),
             'pad and pen': dict(ref=500, size=(100, 18, 12), pen=(30, 60, 140))},
      defaults=dict(size=(70, 12, 10), pen=None, colour=(246, 244, 236)),
      box=lambda a: (0, -a['size'][1], a['size'][0] + a['size'][2], 0))
def notepad(p, img, cam, a, t):
    """A notepad lying on a ledge, seen from a little above (its near left corner is the point); a pen on it."""
    w, d, sk = a['size']
    if a['pen'] is None:
        p.poly([(0, 0), (w, 0), (w + sk, -d), (sk, -d)], a['colour'], INK, 1.2)
    else:
        p.poly([(0, 0), (w, 0), (w + sk, -d), (sk, -d)], a['colour'], INK, 1.4)
        p.line([(30, -10), (80, -14)], a['pen'], 3.0)


@kind('water jug', ref=500, box=lambda a: (-90, -118, 98, 0))
def water_jug(p, img, cam, a, t):
    """A glass water jug with two tumblers either side, standing on a ledge (the point: the jug's foot, middle)."""
    p.poly([(-30, 0), (30, 0), (34, -74), (20, -92), (-26, -90), (-34, -74)], (214, 228, 234), INK, 2.0)
    p.poly(quad(-28, -54, 30, -4), (186, 210, 222), None)
    p.line([(30, -70), (50, -60), (48, -24), (32, -18)], INK, 2.2)
    for x in (-74, 80):
        p.poly([(x - 16, 0), (x + 16, 0), (x + 18, -44), (x - 18, -44)], (214, 228, 234), INK, 1.6)


@kind('papers', ref=1000, params={'width': 'm'}, defaults={'width': 230},
      box=lambda a: (0, -40, a['width'] + 16, 0))
def papers(p, img, cam, a, t):
    """A sheet of paper lying on a desk, seen from a little above (the point: its near left corner)."""
    w = a['width']
    p.poly([(0, 0), (w, 0), (w + 16, -40), (14, -40)], (248, 246, 238), INK, 1.4)


@kind('gavel block', ref=1000, box=lambda a: (-90, -30, 90, 42))
def gavel_block(p, img, cam, a, t):
    """The round sound block under a gavel: a thick disc of dark wood, its top and its side."""
    p.poly(quad(-90, -10, 90, 22), (100, 62, 38), INK, 2.2)
    p.ell(0, 22, 90, 20, (100, 62, 38), INK, 2.2)
    p.ell(0, -10, 90, 20, (136, 88, 54), INK, 2.2)


@kind('gavel', ref=1000, params={'angle': 'n', 'lifted': 'nums'}, defaults={'angle': 180, 'lifted': (-1, -1)},
      box=lambda a: (-60, -26, 160, 26))
def gavel(p, img, cam, a, t):
    """A gavel resting (its head's middle is the point; angle: the handle's direction in degrees, 0 = left). Not
    drawn while `lifted` (from, to seconds): someone holds it then."""
    if a['lifted'][0] <= t <= a['lifted'][1]:
        return
    import blessed_sets as BS                  # the film sets the moment the judge holds it
    if BS.GAVEL_LIFT[0] <= t <= BS.GAVEL_LIFT[1]:
        return
    BS.gavel(p, 0, 0, math.radians(a['angle']))


@kind('glass screen', ref=750, params={'uprights': 'nums', 'shines': 'nums', 'metal': 'c'},
      defaults={'uprights': (), 'shines': (), 'metal': (120, 126, 132)}, band=True)
def glass_screen(p, img, cam, a, t):
    """A glass screen (a dock's): faint glass, slanting pale shines (pairs of x across the top, in metres), steel
    uprights (x in metres) and a top rail."""
    from PIL import Image
    import burnham as B
    w, h = a['w'], a['h']
    pc = a['piece']
    X = lambda xm: pc.P(xm, pc.z1)[0]
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    lp = B.Pen(lay, cam)
    lp.poly(quad(0, 24, w, h), (220, 236, 240, 46), None)
    s = a['shines']
    for x0, x1 in zip(s[::2], s[1::2]):
        x0, x1 = X(x0), X(x1)
        lp.poly([(x0, 24), (x1, 24), (x1 - 300, h), (x0 - 300, h)], (255, 255, 255, 56), None)
    img.alpha_composite(lay)
    for xm in a['uprights']:
        x = X(xm)
        p.poly(quad(x - 7, 4, x + 7, h), a['metal'], INK, 1.6)
    p.poly(quad(0, 0, w, 18), a['metal'], INK, 1.8)


import places_outside   # noqa: E402,F401  (registers the outdoor pieces into KINDS)
