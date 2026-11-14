#!/usr/bin/env python3
"""MAP  The places kit's outdoor pieces (ranking item 5; overnight chat 5b, 14 Nov): skies, brick and stone fronts,
ribbons of windows, an entrance, sign boards, paving and tarmac, planted walls, steps and their rails, trees, lamp
posts, bollards, a gatehouse's pilasters, arched windows and arched gate. Lifted unchanged in look from Blessed's
court_out and gates (blessed_sets.py) and made general: every position is in metres (the piece's own x, z and
depth, through `pc.P(x, z, depth)`), every trim is in the piece's own units at its REF (or its look's).
Registered into places_parts.KINDS (places_parts imports this file at its end).

Map: helpers 30 | sky and clouds 50 | fronts 75 | windows 130 | entrance and signs 175 | ground 235 |
     walls, steps, rails 300 | trees and posts 360 | the gatehouse 400
"""
import math
import random

import numpy as np

from ed import INK
from places_parts import kind, wob, quad, mix, dk, window_box, bricks_in
from remakes_sets import blob, clump


def _L(a):
    """(piece, Lp(x, d, z) -> own units, ppm(d) in own units)"""
    pc = a['piece']
    return pc, (lambda x, d, z: pc.P(x, z, d)), (lambda d: pc.L.ppm(d) / pc.k)


def _face(Lp, x0, x1, d, z0, z1):
    (ax, ay), (bx, by) = Lp(x0, d, z1), Lp(x1, d, z0)
    return quad(ax, ay, bx, by)


def _box(Lp, x0, x1, d, z0, z1):
    (ax, ay), (bx, by) = Lp(x0, d, z1), Lp(x1, d, z0)
    return (ax, ay, bx, by)


# ================================================================================================ sky and clouds
@kind('sky', params={'colour': 'c'}, defaults={'colour': (214, 222, 228)}, band=True)
def sky(p, img, cam, a, t):
    """The sky: a flat colour band (stand it far off, a hundred metres or more, so it sits behind everything)."""
    p.poly(quad(0, 0, a['w'], a['h']), a['colour'], None)


@kind('cloud', params={'rx': 'm', 'ry': 'm', 'colour': 'c'}, defaults={'rx': 220, 'ry': 70, 'colour': (232, 236, 240)},
      box=lambda a: (-a['rx'], -a['ry'], a['rx'], a['ry']))
def cloud(p, img, cam, a, t):
    """A flat scalloped cloud (its middle is the point)."""
    p.poly(blob(0, 0, a['rx'], a['ry'], 10, 0.12, a['seed']), a['colour'], None)


# ================================================================================================ fronts
FRONT_LOOKS = {   # a brick front's texture (brick w, h, how many patches, line) at the REF it was drawn at
    'court': dict(ref=1500 / 17, bricks=(10, 4, 220, 0.6), line=3.0),
    'court pier': dict(ref=1500 / 16.4, bricks=(11, 5, 30, 0.6), line=2.6),
    'planted wall': dict(ref=1500 / 11, bricks=(14, 6, 40, 0.6), line=2.6),
    'gatehouse': dict(ref=1100 / 9, bricks=(10, 4, 160, 0.6), line=3.0),
    'gatehouse centre': dict(ref=1100 / 9.3, bricks=(10, 4, 140, 0.6), line=3.0),
}


@kind('brick front', params={'colour': 'c', 'line': 'n', 'inset': 'm', 'parapet': 'm', 'parapet colour': 'c',
                             'bricks': 'nums'}, looks=FRONT_LOOKS,
      defaults=dict(FRONT_LOOKS['court'], colour=(192, 156, 112), inset=0, parapet=0, **{'parapet colour': None}))
def brick_front(p, img, cam, a, t):
    """A flat brick front (a building, a pier, a tower): the colour, its outline, scattered brick patches (inset
    from the sides), a darker parapet along the top."""
    w, h = a['w'], a['h']
    p.poly(quad(0, 0, w, h), a['colour'], INK, a['line'])
    cw, ch, n, lw = a['bricks']
    bricks_in(p, (a['inset'], 0, w - a['inset'], h), a['colour'], a['seed'], cw=cw, ch=ch, n=int(n), lw=lw)
    if a['parapet']:
        p.poly(quad(0, 0, w, a['parapet']), a['parapet colour'] or dk(a['colour'], 0.84), INK, 2.4)


@kind('window grid', params={'pitch': 'n', 'size': 'nums', 'rows': 'nums', 'skip': 'nums', 'frame': 'c', 'glass': 'c',
                             'bars': 'n', 'line': 'n', 'blinds': 'n', 'row seed': 'n', 'blind colour': 'c'},
      defaults={'pitch': 2.55, 'size': (1.9, 1.9), 'rows': (), 'skip': (), 'frame': (62, 52, 46),
                'glass': (172, 186, 192), 'bars': 2, 'line': 1.8, 'blinds': 0, 'row seed': 20,
                'blind colour': (226, 204, 140)}, band=True)
def window_grid(p, img, cam, a, t):
    """Rows of windows across a front (ribbon windows, shop glazing): centres from x's start to its end every
    `pitch` m, one row per bottom height in `rows`, `size` W H m, none whose centre falls inside a `skip` pair;
    `blinds` 1: some blinds part-way down (the house's scatter)."""
    pc, Lp, _ = _L(a)
    d = pc.d0
    w2, h = a['size'][0] / 2, a['size'][1]
    sk = a['skip']
    for r, zb in enumerate(a['rows']):
        fl = r + 1
        for i, xc in enumerate(np.arange(pc.x0, pc.x1, a['pitch'])):
            if any(lo < xc < hi for lo, hi in zip(sk[::2], sk[1::2])):
                continue
            bl = None
            if a['blinds'] and (i * 7 + fl * 3) % 5 < 2:
                bl = [0.2, 0.55, 0.35][(i + fl) % 3]
            (ax, ay), (bx, by) = Lp(xc - w2, d, zb + h), Lp(xc + w2, d, zb)
            window_box(p, (ax, ay, bx, by), a['frame'], a['glass'], int(a['seed'] + i + a['row seed'] * fl),
                       bars=int(a['bars']), blind=bl, blind_colour=a['blind colour'], lw=a['line'])


# ================================================================================================ entrance and signs
@kind('entrance', params={'colour': 'c', 'doors': 'nums', 'door width': 'n', 'door height': 'n', 'glass': 'c',
                          'handle': 'c'},
      defaults={'colour': (52, 56, 62), 'doors': (), 'door width': 1.3, 'door height': 2.4, 'glass': (104, 120, 128),
                'handle': (200, 200, 204)})
def entrance(p, img, cam, a, t):
    """A dark entrance recess with glass doors (centres in `doors`, 2 cm in front of it), each with its middle
    line and two pull handles."""
    pc, Lp, _ = _L(a)
    p.poly(quad(0, 0, a['w'], a['h']), a['colour'], INK, 2.4)
    d, z0 = pc.d0 - 0.01, pc.z0
    hw = a['door width'] / 2
    for xc in a['doors']:
        p.poly(_face(Lp, xc - hw, xc + hw, d, z0, z0 + a['door height']), a['glass'], INK, 2.0)
        p.line([Lp(xc, d, z0 + a['door height']), Lp(xc, d, z0)], INK, 2.0)
        for sg in (-1, 1):
            p.line([Lp(xc + sg * 0.12, d, z0 + 1.3), Lp(xc + sg * 0.12, d, z0 + 0.9)], a['handle'], 2.6)


SIGN_LOOKS = {'on posts': dict(ref=1100 / 7.4, posts=(10, 4))}


@kind('sign board', params={'colour': 'c', 'line': 'n', 'text': 's', 'text at': 'n', 'text width': 'm',
                            'text colour': 'c', 'text2': 's', 'text2 at': 'n', 'text2 width': 'm', 'text2 colour': 'c'},
      looks=SIGN_LOOKS, defaults={'colour': (30, 34, 40), 'line': 2.6, 'text': '', 'text at': 0.5, 'text width': 0,
                                  'text colour': (236, 236, 232), 'text2': '', 'text2 at': 0.74, 'text2 width': 0,
                                  'text2 colour': (60, 60, 64), 'posts': None})
def sign_board(p, img, cam, a, t):
    """A sign board (a fascia band, a sign on two posts down to the ground): its lettering scaled to an exact
    width, centred across, `text at` of the way down."""
    import blessed_sets as BS                     # the house lettering (sign: drawn once large, scaled to width)
    pc, Lp, _ = _L(a)
    w, h = a['w'], a['h']
    if a['posts']:
        inset, hw = a['posts']
        gy = Lp(0, pc.d0, 0)[1]
        for x in (inset, w - inset):
            p.poly(quad(x - hw, h, x + hw, gy), (60, 62, 66), INK, 1.2)
    p.poly(quad(0, 0, w, h), a['colour'], INK, a['line'])
    for k in ('text', 'text2'):
        if a[k]:
            BS.sign(img, cam, a[k], w / 2, h * a[k + ' at'], a[k + ' width'], a[k + ' colour'])


@kind('small sign', ref=1500 / 16.38, params={'colour': 'c'}, defaults={'colour': (196, 40, 44)},
      box=lambda a: (-9, -12, 9, 12))
def small_sign(p, img, cam, a, t):
    """A small sign on a wall (a red 'no entry' plate), its middle the point."""
    p.poly(quad(-9, -12, 9, 12), a['colour'], INK, 1.4)
    p.poly(quad(-6, -2, 6, 2), (246, 246, 246), None)


# ================================================================================================ ground
GROUND_LOOKS = {
    'paving': dict(colour=(178, 176, 170), joints=(156, 154, 148), across=(1.2, 0, 0.9), across_line=1.4, rise=0,
                   along=(-12, 12.1, 0.9, 1.0), along_line=1.2, kerb=None, stains=(26, 5, 1.5, 10, 6, 30, 10)),
    'tarmac': dict(colour=(110, 112, 116), joints=(100, 102, 106), across=(3.0, 5.5), across_line=2.0, rise=3,
                   along=None, kerb=(90, 90, 94), stains=(26, 9, 2, -0.8, 5, 60, 14), stain=(98, 100, 104)),
    'plain': dict(colour=(196, 190, 180), across=None, along=None, kerb=None, stains=None),
}


@kind('ground', params={'colour': 'c', 'joints': 'c', 'height': 'n'}, looks=GROUND_LOOKS,
      defaults=dict(GROUND_LOOKS['plain'], height=0.0, joints=(0, 0, 0), stain=None), band=True)
def ground(p, img, cam, a, t):
    """Level ground across the whole picture from its far depth to its near one (0: the picture's foot), at
    `height` m: paving slabs (joints across and along, stains), tarmac (a kerb at the far edge, lines, stains), or
    a plain forecourt."""
    pc, Lp, _ = _L(a)
    far, near, z = pc.d0, pc.d1, a['height']
    X0, X1 = pc.screen(-300, 0)[0], pc.screen(1380, 0)[0]
    y0 = Lp(0, far, z)[1]
    y1 = Lp(0, near, z)[1] if near else pc.screen(0, 2400)[1]
    p.poly(quad(X0, y0, X1, y1), a['colour'], None)
    if a['kerb']:
        p.poly(quad(X0, y0 - 4, X1, y0 + 6), a['kerb'], INK, 1.2)
    ac = a['across']
    if ac and len(ac) == 3:
        for dd in np.arange(ac[0], far, ac[2]):
            y = Lp(0, dd, z)[1]
            p.line([(X0, y), (X1, y + a['rise'])], a['joints'], a['across_line'])
    elif ac:
        for dd in ac:
            y = Lp(0, dd, z)[1]
            p.line([(X0, y), (X1, y + a['rise'])], a['joints'], a['across_line'])
    if a['along']:
        lo, hi, step, front = a['along']
        for xx in np.arange(lo, hi, step):
            p.line([Lp(xx, far, z), Lp(xx, front, z)], a['joints'], a['along_line'])
    if a['stains']:
        n, seed, dlo, dhi, xs, sw, sh = a['stains']
        r = random.Random(int(seed))
        for _ in range(int(n)):
            dd = r.uniform(dlo, dhi if dhi > 0 else far + dhi)
            x, y = Lp(r.uniform(-xs, xs), dd, z)
            p.ell(x, y, sw / dd, sh / dd, a['stain'] or a['joints'], None)


# ================================================================================================ walls, steps, rails
@kind('planted wall', ref=1500 / 11, params={'colour': 'c', 'bed': 'n', 'shrubs': 'nums', 'leaves': 'c', 'flowers': 'c',
                                             'brick seed': 'n', 'coping': 'c'},
      defaults={'colour': (192, 156, 112), 'bed': 0.8, 'shrubs': (0.6, 1.15, 0.2), 'leaves': (86, 120, 66),
                'flowers': (150, 70, 60), 'brick seed': 0, 'coping': (200, 190, 178)})
def planted_wall(p, img, cam, a, t):
    """A low brick wall with a coping, a bed of shrubs behind it (`bed` m back; shrubs from `shrubs` first, every,
    and how far above the wall's top; every fourth in flower)."""
    pc, Lp, _ = _L(a)
    first, every, above = a['shrubs']
    dd = pc.d0 + a['bed']
    for k, xc in enumerate(np.arange(pc.x0 + first, pc.x1, every)):
        c = Lp(xc, dd, pc.z1 + above)
        clump(p, c[0], c[1], 32 + 8 * (k % 3), 26, a['leaves'] if k % 4 else a['flowers'], a['seed'] + k,
              marks=True, lw=1.8)
    w, h = a['w'], a['h']
    p.poly(quad(0, 0, w, h), a['colour'], INK, 2.6)
    cw, ch, n, lw = FRONT_LOOKS['planted wall']['bricks']
    bricks_in(p, (0, 0, w, h), a['colour'], int(a['brick seed']), cw=cw, ch=ch, n=n, lw=lw)
    p.poly(quad(-3, -6, w + 3, 2), a['coping'], INK, 1.8)


@kind('steps', params={'colour': 'c', 'n': 'n', 'going': 'n'}, defaults={'colour': (178, 176, 170), 'n': 6, 'going': 0.3})
def steps(p, img, cam, a, t):
    """A flight of steps going up and away from the lens: x across, z from the foot to the top, depth the first
    step's front; `n` steps `going` m deep, every other one a touch lighter."""
    pc, Lp, _ = _L(a)
    n, g = int(a['n']), a['going']
    rise = (pc.z1 - pc.z0) / n
    for k in range(n):
        z = pc.z0 + (pc.z1 - pc.z0) * (k + 1) / n
        dd = pc.d0 + g + g * k
        (ax, ay), (bx, by) = Lp(pc.x0, dd, z), Lp(pc.x1, dd - g, z - rise)
        p.poly(quad(ax, ay, bx, by), mix(a['colour'], (255, 255, 255), 0.1 * (k % 2)), INK, 1.6)


@kind('stair rail', params={'colour': 'c', 'height': 'n', 'n': 'n', 'posts': 'nums'},
      defaults={'colour': (210, 214, 218), 'height': 0.95, 'n': 6, 'posts': (0, 3, 6)})
def stair_rail(p, img, cam, a, t):
    """A handrail up a flight (x where it runs; depth from the flight's foot to its top; z its rise), `height` m
    above the steps, on posts at the steps numbered in `posts`."""
    pc, Lp, _ = _L(a)
    n = int(a['n'])
    xr, g = pc.x0, (pc.d1 - pc.d0) / n
    zs = [(pc.z1 - pc.z0) * k / n for k in range(n + 1)]
    pts = [Lp(xr, pc.d0 + g * k, pc.z0 + zs[k] + a['height']) for k in range(n + 1)]
    p.line(pts, a['colour'], 3.4)
    p.line(pts, INK, 1.0)
    for k in a['posts']:
        k = int(k)
        p.line([pts[k], Lp(xr, pc.d0 + g * k, pc.z0 + zs[k])], a['colour'], 2.6)


# ================================================================================================ trees and posts
@kind('tree', ref=120, params={'height': 'n', 'trunk': 'c', 'leaves': 'c', 'leaves2': 'c', 'canopy seed': 'n'},
      defaults={'height': 7.5, 'trunk': (92, 74, 58), 'leaves': (170, 160, 72), 'leaves2': (86, 120, 66),
                'canopy seed': 900},
      box=lambda a: (-2.6 * a['ppm'], -10.8 * a['ppm'], 2.6 * a['ppm'], 0))
def tree(p, img, cam, a, t):
    """A street tree (the point: the trunk's foot): a trunk `height` m to the crown, four scalloped clumps of
    leaves (autumn by default), alternate ones mixed toward `leaves2`."""
    pc, Lp, ppm = _L(a)
    x, d = pc.x0, pc.d0
    base, top = Lp(x, d, pc.z0), Lp(x, d, pc.z0 + a['height'])
    p.poly(wob(quad(base[0] - 9, top[1], base[0] + 9, base[1]), 1.5, a['seed']), a['trunk'], INK, 2.2)
    for j, (ox, oz, rr) in enumerate(((0, 8.2, 2.6), (-1.6, 6.6, 1.9), (1.7, 6.9, 2.0), (0.4, 5.6, 1.5))):
        c = Lp(x + ox, d, pc.z0 + oz)
        clump(p, c[0], c[1], rr * ppm(d), rr * ppm(d) * 0.8, mix(a['leaves'], a['leaves2'], 0.35 * (j % 2)),
              int(a['canopy seed']) + j, lw=2.2)


@kind('lamp post', ref=1500 / 8.5, params={'height': 'n', 'colour': 'c', 'head': 'c'},
      defaults={'height': 8.0, 'colour': (120, 124, 128), 'head': (110, 114, 118)},
      box=lambda a: (-22, -a['height'] * a['ppm'] - 10, 8, 0))
def lamp_post(p, img, cam, a, t):
    """A tall street lamp (the point: its foot): a slim grey post and a lamp head reaching left."""
    pc, Lp, _ = _L(a)
    lp, lt = Lp(pc.x0, pc.d0, pc.z0), Lp(pc.x0, pc.d0, pc.z0 + a['height'])
    p.poly(quad(lp[0] - 5, lt[1], lp[0] + 5, lp[1]), a['colour'], INK, 1.8)
    p.poly(quad(lp[0] - 22, lt[1] - 10, lp[0] + 8, lt[1] + 4), a['head'], INK, 1.6)


@kind('bollard', params={'height': 'n', 'radius': 'n', 'colour': 'c', 'top': 'c'},
      defaults={'height': 0.9, 'radius': 0.12, 'colour': (230, 196, 40), 'top': (240, 210, 70)},
      box=lambda a: (-0.12 * a['ppm'], -0.95 * a['ppm'], 0.12 * a['ppm'], 0))
def bollard(p, img, cam, a, t):
    """A painted bollard (the point: its foot)."""
    pc, Lp, ppm = _L(a)
    bl, bt = Lp(pc.x0, pc.d0, pc.z0), Lp(pc.x0, pc.d0, pc.z0 + a['height'])
    w = ppm(pc.d0) * a['radius']
    p.poly(quad(bl[0] - w, bt[1], bl[0] + w, bl[1]), a['colour'], INK, 2.0)
    p.ell(bl[0], bt[1], w, w * 0.4, a['top'], INK, 1.4)


# ================================================================================================ the gatehouse
STONE = (186, 160, 128)
STONE_D = (70, 64, 60)


@kind('pilaster', params={'colour': 'c', 'step': 'n', 'plinth': 'c'},
      defaults={'colour': STONE_D, 'step': 0.62, 'plinth': STONE_D}, band=True)
def pilaster(p, img, cam, a, t):
    """A rusticated stone pilaster (big dark blocks, a deeper course every other one) on a plinth with a cap; the
    plinth runs from the ground to the pilaster's foot."""
    pc, Lp, _ = _L(a)
    x0, x1, d, z0, z1 = pc.x0, pc.x1, pc.d0, pc.z0, pc.z1
    p.poly(_face(Lp, x0, x1, d, z0, z1), a['colour'], INK, 2.4)
    k = 0
    for z in np.arange(z0, z1 - 0.05, a['step']):
        inset = 0.06 if k % 2 else 0.0
        p.poly(_face(Lp, x0 + inset, x1 - inset, d - 0.02, z + 0.04, min(z1, z + a['step']) - 0.04),
               dk(a['colour'], 1.1 if k % 2 else 0.95), INK, 1.2)
        k += 1
    p.poly(_face(Lp, x0 - 0.15, x1 + 0.15, d - 0.05, 0, z0), a['plinth'], INK, 2.4)
    p.poly(_face(Lp, x0 - 0.1, x1 + 0.1, d - 0.03, z0 - 0.15, z0 + 0.05), dk(a['plinth'], 1.2), INK, 1.4)


@kind('arched window', params={'stone': 'c', 'frame': 'c', 'glass': 'c'},
      defaults={'stone': STONE, 'frame': (130, 60, 40), 'glass': (58, 66, 80)})
def arched_window(p, img, cam, a, t):
    """A tall round-headed window: a stone surround and hood, a red-brown frame, small panes, a sill, a keystone."""
    pc, Lp, _ = _L(a)
    STONE_, FRAME = a['stone'], a['frame']
    (ax, ay), (bx, by) = Lp(pc.x0, pc.d0, pc.z1), Lp(pc.x1, pc.d0, pc.z0)
    r_ = (bx - ax) / 2
    cx_, spring = ax + r_, ay + r_

    def head(rr, n=14):
        return [(cx_ + rr * math.cos(u), spring - rr * math.sin(u)) for u in np.linspace(0, math.pi, n)]
    m = r_ * 0.38
    p.poly([(bx + m, by + m * 0.6)] + head(r_ + m) + [(ax - m, by + m * 0.6)], STONE_, INK, 2.0)
    p.poly([(bx, by)] + head(r_) + [(ax, by)], FRAME, INK, 2.0)
    mm = r_ * 0.16
    p.poly([(bx - mm, by - mm)] + head(r_ - mm) + [(ax + mm, by - mm)], a['glass'], None)
    for k in (1, 2):
        x = ax + (bx - ax) * k / 3
        p.line([(x, ay + r_ * 0.2), (x, by - mm)], FRAME, 2.0)
    for y in np.arange(spring + r_ * 0.5, by - mm, r_ * 0.55):
        p.line([(ax + mm, y), (bx - mm, y)], FRAME, 1.8)
    p.poly(quad(ax - m, by, bx + m, by + m * 0.7), STONE_, INK, 1.6)
    p.poly(quad(cx_ - m * 0.6, ay - m * 1.2, cx_ + m * 0.6, ay + m * 0.3), STONE_, INK, 1.4)


@kind('arched gate', params={'stone': 'c', 'timber': 'c', 'jamb': 'n', 'wall': 'n', 'wicket': 'nums'},
      defaults={'stone': STONE, 'timber': (120, 80, 52), 'jamb': 0.5, 'wall': 0.28, 'wicket': ()},
      box=lambda a: (-a['jamb'] * a['ppm'], -0.36 * a['w'], a['w'] + a['jamb'] * a['ppm'], a['h']))
def arched_gate(p, img, cam, a, t):
    """A stone round arch over a timber double gate (x: the opening; z: ground to the arch's spring): a surround
    `jamb` m wide with voussoirs and a keystone, a square iron grille in the arch, the gate's boards and two leaves,
    a wicket door (x0 x1 height, m) standing open onto a dark yard. `wall`: how far behind the wall's face it is."""
    pc, Lp, _ = _L(a)
    STONE_, TIMBER = a['stone'], a['timber']
    d, hw, sp_z = pc.d0, (pc.x1 - pc.x0) / 2, pc.z1
    xm = (pc.x0 + pc.x1) / 2
    (ax, ay), (bx, by) = Lp(pc.x0, d, sp_z), Lp(pc.x1, d, pc.z0)
    r_ = (bx - ax) / 2
    cx_, spring = ax + r_, ay
    ro = r_ * 1.36
    jl, jr = Lp(xm - hw - a['jamb'], d, pc.z0), Lp(xm + hw + a['jamb'], d, pc.z0)
    p.poly([(jr[0], jr[1])] + [(cx_ + ro * math.cos(u), spring - ro * math.sin(u)) for u in np.linspace(0, math.pi, 24)]
           + [(jl[0], jl[1])], STONE_, INK, 2.6)
    for k in range(1, 13):
        u = math.pi * k / 13
        p.line([(cx_ + r_ * math.cos(u), spring - r_ * math.sin(u)),
                (cx_ + ro * math.cos(u), spring - ro * math.sin(u))], dk(STONE_, 0.72), 1.8)
    dw = d - a['wall']
    for z in np.arange(0.5, sp_z, 0.55):
        for sx in (-1, 1):
            y = Lp(xm, d, pc.z0 + z)[1]
            x_in, x_out = Lp(xm + sx * hw, dw, pc.z0)[0], Lp(xm + sx * (hw + a['jamb']), dw, pc.z0)[0]
            p.line([(x_in, y), (x_out, y)], dk(STONE_, 0.72), 1.6)
    p.poly([(cx_ - r_ * 0.16, spring - ro - 10), (cx_ + r_ * 0.16, spring - ro - 10), (cx_ + r_ * 0.12, spring - r_ + 4),
            (cx_ - r_ * 0.12, spring - r_ + 4)], STONE_, INK, 2.2)
    head = [(cx_ + r_ * math.cos(u), spring - r_ * math.sin(u)) for u in np.linspace(0, math.pi, 24)]
    p.poly(head, (34, 32, 32), INK, 2.4)
    gx = np.linspace(ax, bx, 13)
    for x in gx[1:-1]:
        top = spring - math.sqrt(max(0.0, r_ ** 2 - (x - cx_) ** 2))
        p.line([(x, top + 2), (x, spring)], (130, 120, 108), 2.2)
    for y in np.arange(spring - (gx[1] - gx[0]), spring - r_, -(gx[1] - gx[0])):
        half = math.sqrt(max(0.0, r_ ** 2 - (spring - y) ** 2))
        p.line([(cx_ - half + 2, y), (cx_ + half - 2, y)], (130, 120, 108), 2.2)
    p.poly(quad(ax, spring, bx, by), TIMBER, INK, 2.8)
    p.poly(quad(ax, spring - 4, bx, spring + 8), (50, 40, 34), INK, 1.6)
    for k in range(1, 16):
        x = ax + (bx - ax) * k / 16
        p.line([(x, spring + 8), (x, by)], dk(TIMBER, 0.8), 1.4)
    p.line([(cx_, spring + 8), (cx_, by)], INK, 2.4)
    if a['wicket']:
        w0, w1, wh = a['wicket']
        wx0, wx1 = Lp(w0, d - 0.01, pc.z0 + wh), Lp(w1, d - 0.01, pc.z0)
        p.poly(quad(wx0[0], wx0[1], wx1[0], wx1[1]), (24, 22, 22), INK, 2.4)
        p.poly(quad(wx0[0] + 4, wx1[1] - 20, wx1[0] - 4, wx1[1]), (70, 66, 60), None)
        p.poly([(wx1[0], wx0[1]), (wx1[0] + 26, wx0[1] + 10), (wx1[0] + 26, wx1[1] + 4), (wx1[0], wx1[1])],
               dk(TIMBER, 0.86), INK, 2.2)
