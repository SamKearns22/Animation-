#!/usr/bin/env python3
"""MAP  The places kit's building-site and grand-room pieces (Open Wounds chat 5, 23 Nov; shared: every film can use
them by name in its story/FILM-places.txt). Registered into places_parts.KINDS (imported at that file's end).

Every piece here has ref None (lines at the house width at any distance) and draws in screen units through
a['piece'] (Lp(x, d, z) for any point in metres, so a piece can have depth: scaffolding, a door that swings).
Sizes are real (sizes from the references: UK tube-and-fitting scaffold, 2 m bays, 1.3 m deep, guard rails at 1.0 and
0.5 m, toe boards 0.15 m; storeys 3.2 m; Heras panels 3.5 x 2.0 m; an 8-yard skip 3.7 x 1.7 x 1.2 m).

  Outside:  dirt, skyline, concrete frame, scaffold (part back / part front: people stand between), pipe stack, pipe,
            tower crane, heras fence, skip, portacabin, hoarding, cone, pallet, heap
  Inside:   bookcase (Ad-Vanced Notice's book drawing made general), double doors (thrown open at `open at` s, a
            bounce off the stops, the lit corridor beyond), chandelier

Map: helpers 40 | dirt, skyline 60 | the frame 120 | scaffold 175 | pipes, crane 250 | site dressing 320 |
     bookcase 400 | doors 450 | chandelier 510
"""
import math
import random

import numpy as np

from ink import INK
from places_parts import kind, wob, quad, mix, dk   # (the kit's own helpers: no finished film loaded here)

CONC, CONC_D, CONC_L = (176, 174, 168), (120, 118, 114), (198, 196, 190)
TUBE, TUBE_D = (150, 154, 160), (92, 96, 104)
BOARD = (196, 160, 104)
RED, YEL = (200, 52, 44), (236, 196, 58)


def _L(a):
    pc = a['piece']
    return pc, (lambda x, d, z: pc.P(x, z, d)), (lambda d: pc.L.ppm(d) / pc.k)


def _face(Lp, x0, x1, d, z0, z1):
    (ax, ay), (bx, by) = Lp(x0, d, z1), Lp(x1, d, z0)
    return quad(ax, ay, bx, by)


def _w(ppm, metres, lo=1.4):
    """A line as wide as `metres` at this depth, never thinner than `lo` px (so it still reads)."""
    return max(lo, metres * ppm)


# ================================================================================================ dirt, skyline
@kind('dirt', params={'colour': 'c', 'dark': 'c', 'light': 'c', 'ruts': 'n', 'stones': 'n', 'puddles': 'n'},
      defaults={'colour': (186, 164, 130), 'dark': (160, 138, 106), 'light': (204, 186, 154), 'ruts': 3,
                'stones': 60, 'puddles': 2}, band=True)
def dirt(p, img, cam, a, t):
    """A dusty building-site ground from its far depth to its near one: flat dust, darker and paler patches, tyre ruts
    curving off into the distance, scattered stones, a puddle or two of grey sky."""
    pc, Lp, ppm = _L(a)
    far, near = pc.d0, (pc.d1 or 1.0)
    X0, X1 = pc.screen(-300, 0)[0], pc.screen(1380, 0)[0]
    y0, y1 = Lp(0, far, 0)[1], pc.screen(0, 2400)[1]
    p.poly(quad(X0, y0, X1, y1), a['colour'], None)
    r = random.Random(a['seed'])
    for _ in range(14):                                         # patches of darker / paler dust
        d = r.uniform(near + 1, far)
        x = r.uniform(-12, 12) * d / 10
        c = a['dark'] if r.random() < 0.55 else a['light']
        cx, cy = Lp(x, d, 0)
        rx, ry = r.uniform(1.5, 4) * ppm(d), r.uniform(0.3, 0.8) * ppm(d) * 0.25
        p.ell(cx, cy, rx, ry, mix(a['colour'], c, 0.7), None)
    for k in range(int(a['ruts'])):                             # tyre ruts: pairs of curves into the distance
        xa, xb = r.uniform(-8, 8), r.uniform(-14, 14)
        for off in (0, 1.8):
            pts = []
            for u in np.linspace(0, 1, 18):
                d = near + 0.5 + (far - near - 0.5) * u
                x = xa + (xb - xa) * u * u + off
                pts.append(Lp(x, d, 0))
            p.line(pts, a['dark'], 2.0)
    for _ in range(int(a['stones'])):                           # stones, bigger near
        d = r.uniform(near + 0.5, far)
        cx, cy = Lp(r.uniform(-1.2, 1.2) * d, d, 0)
        s = r.uniform(0.04, 0.14) * ppm(d)
        if s < 1.2:
            continue
        p.ell(cx, cy, s, s * 0.6, mix(a['dark'], (120, 116, 110), r.random()), INK if s > 4 else None, 1.2)
    for _ in range(int(a['puddles'])):                          # puddles: the grey sky lying on the dirt
        d = r.uniform(near + 3, far * 0.7)
        cx, cy = Lp(r.uniform(-0.8, 0.8) * d, d, 0)
        rx = r.uniform(0.8, 1.6) * ppm(d)
        p.poly(wob([(cx + rx * math.cos(u), cy + rx * 0.16 * math.sin(u)) for u in np.linspace(0, 2 * math.pi, 22)],
                   2.0, int(d * 10)), (176, 182, 186), INK, 1.4)


@kind('skyline', params={'colour': 'c', 'far': 'c'}, defaults={'colour': (150, 152, 156), 'far': (176, 178, 182)},
      band=True)
def skyline(p, img, cam, a, t):
    """A far grey town and industry along the horizon (as Kemi's photo): low blocks, chimneys, a gasholder, a tower;
    two flat greys, no lines (distance)."""
    pc, Lp, ppm = _L(a)
    d = pc.d0
    r = random.Random(a['seed'])
    for col, top, n in ((a['far'], 28, 30), (a['colour'], 16, 26)):
        x = pc.x0
        while x < pc.x1:
            w = r.uniform(8, 30)
            h = r.uniform(4, top)
            p.poly(_face(Lp, x, x + w, d, 0, h), col, None)
            if r.random() < 0.18:                               # a chimney
                cx = x + w * r.uniform(0.2, 0.8)
                p.poly(_face(Lp, cx, cx + 2.5, d, 0, h + r.uniform(25, 55)), col, None)
            if r.random() < 0.06:                               # a gasholder
                cx, cy = Lp(x + w / 2, d, 0)
                rr = 14 * ppm(d)
                p.poly(quad(cx - rr, cy - rr * 1.6, cx + rr, cy), col, None)
                p.ell(cx, cy - rr * 1.6, rr, rr * 0.18, col, None)
            x += w * r.uniform(0.6, 1.1)


# ================================================================================================ the concrete frame
@kind('concrete frame', params={'storey': 'n', 'bay': 'n', 'colour': 'c', 'dark': 'c', 'inside': 'c', 'blocks': 'n',
                                'core': 'nums', 'rebar': 'n'},
      defaults={'storey': 3.2, 'bay': 6.0, 'colour': CONC, 'dark': CONC_D, 'inside': (70, 70, 72), 'blocks': 0.25,
                'core': [], 'rebar': 1})
def concrete_frame(p, img, cam, a, t):
    """A building's bare concrete frame under construction: slab edges every storey, square columns every bay, the
    floors open (holes) with the dark inside and the slab undersides showing, some bays part-filled with blockwork,
    a solid stair core (core: x from, x to in metres), rebar bristling from the top columns."""
    pc, Lp, ppm = _L(a)
    d, x0, x1, z0, z1 = pc.d0, pc.x0, pc.x1, pc.z0, pc.z1
    r = random.Random(a['seed'])
    s, bay = a['storey'], a['bay']
    pp = ppm(d)
    p.poly(_face(Lp, x0, x1, d, z0, z1), a['inside'], INK, 2.4)                 # the dark inside, outlined
    for z in np.arange(z0 + s, z1 + 0.01, s):                                    # each floor's ceiling: the slab's
        p.poly(_face(Lp, x0, x1, d + 6, z - 0.45, z - 0.3), dk(a['inside'], 0.8), None)  # underside deep inside
    x = x0
    while x < x1 - 0.1:                                                          # back columns deep inside
        p.poly(_face(Lp, x + bay * 0.5 - 0.2, x + bay * 0.5 + 0.2, d + 6, z0, z1), mix(a['inside'], a['dark'], 0.4), None)
        x += bay
    for z in np.arange(z0, z1 - 0.1, s):                                         # blockwork part-filling some bays
        x = x0
        while x < x1 - 0.1:
            if r.random() < a['blocks']:
                top = z + s * r.choice((0.35, 0.6, 1.0))
                p.poly(_face(Lp, x + 0.3, x + bay - 0.3, d, z, top - 0.3), (164, 160, 150), INK, 1.6)
                for zz in np.arange(z + 0.22, top - 0.3, 0.22):
                    (lx, ly), (rx_, _) = Lp(x + 0.3, d, zz), Lp(x + bay - 0.3, d, zz)
                    p.line([(lx, ly), (rx_, ly)], (140, 136, 128), 1.0)
            x += bay
    for c0, c1 in zip(a['core'][::2], a['core'][1::2]):                          # the stair core, solid
        p.poly(wob(_face(Lp, c0, c1, d - 0.1, z0, z1 + s * 0.6), 1.5, a['seed'] + 3), a['colour'], INK, 2.2)
        for z in np.arange(z0 + s, z1 + s, s):
            (lx, ly), (rx_, _) = Lp(c0, d - 0.1, z), Lp(c1, d - 0.1, z)
            p.line([(lx, ly), (rx_, ly)], a['dark'], 1.4)
        cx = (c0 + c1) / 2
        p.poly(_face(Lp, cx - 0.5, cx + 0.5, d - 0.11, z1 - s * 0.6, z1 + s * 0.2), a['inside'], INK, 1.6)
    x = x0
    while x < x1 + 0.01:                                                         # columns
        p.poly(wob(_face(Lp, x - 0.25, x + 0.25, d - 0.05, z0, z1), 1.0, int(x * 7)), a['colour'], INK, 2.0)
        if a['rebar']:
            for k in range(3):
                bx = x - 0.15 + 0.15 * k
                p.line([Lp(bx, d - 0.05, z1), Lp(bx + r.uniform(-0.08, 0.08), d - 0.05, z1 + r.uniform(0.6, 1.0))],
                       (120, 74, 52), _w(pp, 0.03))
        x += bay
    for z in np.arange(z0 + s, z1 + 0.01, s):                                    # slab edges
        p.poly(wob(_face(Lp, x0 - 0.3, x1 + 0.3, d - 0.1, z - 0.3, z), 1.0, int(z * 11)), CONC_L, INK, 2.0)


# ================================================================================================ scaffold
@kind('scaffold', params={'lifts': 'nums', 'bay': 'n', 'deep': 'n', 'part': 's', 'ladder': 'n', 'barrier': 'n',
                          'end': 's'},
      defaults={'lifts': [3.2, 6.4, 9.6], 'bay': 2.0, 'deep': 1.3, 'part': 'back', 'ladder': 2, 'barrier': 0.3,
                'end': 'both'})
def scaffold(p, img, cam, a, t):
    """Tube-and-board scaffolding along a face, in two parts so its people stand between them: 'back' (the inner
    standards, the ledgers, the boards seen edge on, ladders between lifts, braces) at its depth, 'front' (the outer
    standards, guard rails at 1.0 and 0.5 m, toe boards, red-and-yellow edge barriers here and there) `deep` m
    nearer. Its people's feet stand on a lift's height (lifts: board tops in metres)."""
    pc, Lp, ppm = _L(a)
    d, x0, x1, z0, z1 = pc.d0, pc.x0, pc.x1, pc.z0, pc.z1
    r = random.Random(a['seed'])
    bay = a['bay']
    xs = list(np.arange(x0, x1 + 0.01, bay))
    if a['part'] == 'back':
        dd = d
        pp = ppm(dd)
        for z in a['lifts']:                                     # the boards: a band 0.06 m thick, seen edge on
            p.poly(_face(Lp, x0 - 0.2, x1 + 0.2, dd - a['deep'] * 0.5, z - 0.06, z), BOARD, INK, 1.6)
            p.line([Lp(x0, dd, z - 0.1), Lp(x1, dd, z - 0.1)], TUBE_D, _w(pp, 0.05))   # the ledger under them
        for k, x in enumerate(xs):                               # inner standards
            p.line([Lp(x, dd, z0), Lp(x, dd, z1)], TUBE_D, _w(pp, 0.05))
        lifts = [z0] + list(a['lifts'])
        for k, (za, zb) in enumerate(zip(lifts, lifts[1:])):     # ladders, zigzagging up one bay
            bx = x0 + bay * (int(a['ladder']) + (k % 2))
            if bx + 0.6 > x1:
                continue
            for side in (0.0, 0.5):
                p.line([Lp(bx + 0.4 + side + 0.25, dd - 0.6, za), Lp(bx + 0.4 + side, dd - 0.6, zb + 1.0)],
                       (150, 118, 70), _w(pp, 0.05))
            for zz in np.arange(za + 0.3, zb + 0.9, 0.3):
                u = (zz - za) / (zb + 1.0 - za)
                p.line([Lp(bx + 0.4 + 0.25 * (1 - u), dd - 0.6, zz), Lp(bx + 0.9 + 0.25 * (1 - u), dd - 0.6, zz)],
                       (150, 118, 70), _w(pp, 0.03))
        for k in range(0, len(xs) - 1, 3):                       # facade braces
            p.line([Lp(xs[k], dd, z0), Lp(xs[min(k + 3, len(xs) - 1)], dd, min(z1, z0 + 3 * bay))], TUBE_D,
                   _w(pp, 0.04))
    else:
        dd = d
        pp = ppm(dd)
        for z in a['lifts']:
            p.poly(_face(Lp, x0 - 0.2, x1 + 0.2, dd, z, z + 0.15), (182, 150, 98), INK, 1.4)   # toe board
            for hz in (0.5, 1.0):                                                            # guard rails
                p.line([Lp(x0 - 0.2, dd, z + hz), Lp(x1 + 0.2, dd, z + hz)], TUBE, _w(pp, 0.05))
                p.line([Lp(x0 - 0.2, dd, z + hz + 0.02), Lp(x1 + 0.2, dd, z + hz + 0.02)], INK, 1.0)
            x = x0
            while x < x1 - bay:                                  # edge barriers, red and yellow, here and there
                if r.random() < a['barrier']:
                    for k, xx in enumerate(np.arange(x, x + bay, 0.25)):
                        p.poly(_face(Lp, xx, xx + 0.25, dd + 0.02, z + 0.55, z + 0.95), (RED, YEL)[k % 2], None)
                    p.poly(_face(Lp, x, x + bay, dd + 0.02, z + 0.55, z + 0.95), None, INK, 1.2)
                x += bay
        ends = {'both': (xs[0], xs[-1]), 'left': (xs[0],), 'right': (xs[-1],), 'none': ()}[a['end']]
        for x in xs:                                             # outer standards
            p.line([Lp(x, dd, z0), Lp(x, dd, z1)], TUBE, _w(pp, 0.05))
            p.line([Lp(x + 0.02, dd, z0), Lp(x + 0.02, dd, z1)], INK, 1.0)
            if x in ends:                                        # an end's guard rails return to the face
                for z in a['lifts']:
                    for hz in (0.5, 1.0):
                        p.line([Lp(x, dd, z + hz), Lp(x, dd + a['deep'], z + hz)], TUBE, _w(pp, 0.05))
            p.poly(_face(Lp, x - 0.12, x + 0.12, dd, z0, z0 + 0.04), TUBE_D, INK, 1.0)          # base plate


# ================================================================================================ pipes, crane
@kind('pipe stack', params={'radius': 'n', 'rows': 'n', 'colour': 'c'},
      defaults={'radius': 0.45, 'rows': 3, 'colour': (170, 164, 152)})
def pipe_stack(p, img, cam, a, t):
    """Big concrete pipes stacked in a pyramid, ends to the lens (the rim, the dark bore, a pale inside edge), chocked
    with timber; x is where the bottom row starts."""
    pc, Lp, ppm = _L(a)
    d, R, n = pc.d0, a['radius'], int(a['rows'])
    pp = ppm(d)
    for row in range(n):
        for k in range(n - row):
            x = pc.x0 + R + (2 * R) * k + R * row
            z = R + row * R * 1.73
            cx, cy = Lp(x, d, z)
            p.ell(cx, cy, R * pp, R * pp, a['colour'], INK, 2.0)
            p.ell(cx, cy, R * pp * 0.78, R * pp * 0.78, (58, 56, 56), INK, 1.4)
            p.ell(cx + R * pp * 0.12, cy + R * pp * 0.1, R * pp * 0.55, R * pp * 0.55, (40, 38, 40), None)
    p.poly(_face(Lp, pc.x0 - 0.1, pc.x0 + 0.15, d - 0.1, 0, 0.25), (150, 118, 70), INK, 1.4)


@kind('pipe', params={'to': 'pt', 'radius': 'n', 'colour': 'c', 'open': 'n'},
      defaults={'to': (0, 0), 'radius': 0.15, 'colour': (40, 40, 44), 'open': 1})
def pipe(p, img, cam, a, t):
    """A pipe from its point to `to` (a drain run down the face, an end sticking out of a slab): an inked tube, the
    open end a dark ring."""
    pc, Lp, ppm = _L(a)
    w = 2 * a['radius'] * ppm(pc.d0)
    p.line([(0, 0), a['to']], INK, w + 3)
    p.line([(0, 0), a['to']], a['colour'], max(1.0, w - 1))
    p.line([(-w * 0.15, 0), (a['to'][0] - w * 0.15, a['to'][1])], mix(a['colour'], (255, 255, 255), 0.25),
           max(1.0, w * 0.2))
    if a['open']:
        dx, dy = a['to'][0], a['to'][1]
        ang = math.degrees(math.atan2(dy, dx))
        p.ell(dx, dy, w * 0.22, w * 0.5, (24, 22, 24), INK, 1.4, rot=ang)   # the open end, seen from the side


@kind('tower crane', params={'colour': 'c', 'jib': 'n', 'counter': 'n', 'hook': 'n'},
      defaults={'colour': (60, 90, 170), 'jib': 40.0, 'counter': 12.0, 'hook': 20.0})
def tower_crane(p, img, cam, a, t):
    """A tower crane far behind (as the site photos): a lattice mast from x (its width) up to z, a jib `jib` m to the
    right (negative: left), a counter-jib with its weights, the cab, the hook line `hook` m down from the jib's end."""
    pc, Lp, ppm = _L(a)
    d, x0, x1, top = pc.d0, pc.x0, pc.x1, pc.z1
    lw = 1.6
    c = a['colour']
    for x in (x0, x1):
        p.line([Lp(x, d, 0), Lp(x, d, top)], c, lw + 0.6)
    zz, k = 0.0, 0
    while zz < top:
        p.line([Lp((x0, x1)[k % 2], d, zz), Lp((x1, x0)[k % 2], d, zz + (x1 - x0))], c, lw)
        zz += x1 - x0
        k += 1
    sgn = 1 if a['jib'] > 0 else -1
    base = x1 if sgn > 0 else x0
    tip = base + a['jib']
    back = (x0 if sgn > 0 else x1) - sgn * a['counter']
    for z in (top, top + 1.6):
        p.line([Lp(back, d, z), Lp(tip, d, z if z == top else top + 0.6)], c, lw)
    xx = min(back, tip)
    while xx < max(back, tip) - 1.6:
        p.line([Lp(xx, d, top), Lp(xx + 1.6, d, top + 1.4)], c, 1.0)
        xx += 1.6
    p.poly(_face(Lp, back - sgn * 0.0, back + sgn * 4, d, top - 2.4, top), (130, 130, 128), INK, 1.2)   # weights
    p.poly(_face(Lp, min(x0, x1) - 0.6, max(x0, x1) + 0.6, d, top - 2.6, top - 0.4), (236, 236, 230), INK, 1.2)
    p.line([Lp(tip - sgn * 3, d, top), Lp(tip - sgn * 3, d, top - a['hook'])], INK, 1.0)
    hx, hy = Lp(tip - sgn * 3, d, top - a['hook'])
    p.ell(hx, hy, 3, 3, (240, 200, 60), INK, 1.0)


# ================================================================================================ site dressing
@kind('heras fence', params={'colour': 'c'}, defaults={'colour': (150, 156, 160)})
def heras_fence(p, img, cam, a, t):
    """Temporary mesh fence panels (3.5 m x 2 m) on concrete feet along x at its depth."""
    pc, Lp, ppm = _L(a)
    d, pp = pc.d0, ppm(pc.d0)
    x = pc.x0
    while x < pc.x1 - 0.1:
        xe = min(x + 3.5, pc.x1)
        p.poly(_face(Lp, x, xe, d, 0.1, 2.0), None, a['colour'], max(1.2, 0.04 * pp))
        for xx in np.arange(x, xe, 0.25):
            p.line([Lp(xx, d, 0.1), Lp(xx, d, 2.0)], a['colour'], 1.0)
        for zz in np.arange(0.1, 2.0, 0.3):
            p.line([Lp(x, d, zz), Lp(xe, d, zz)], a['colour'], 1.0)
        p.poly(_face(Lp, x - 0.3, x + 0.3, d, 0, 0.14), (140, 138, 132), INK, 1.4)
        x = xe
    p.poly(_face(Lp, x - 0.3, x + 0.3, d, 0, 0.14), (140, 138, 132), INK, 1.4)


@kind('skip', params={'colour': 'c'}, defaults={'colour': (232, 182, 40)})
def skip(p, img, cam, a, t):
    """A builder's skip, side on (3.7 m long, 1.2 m high; sloped ends), heaped with rubble and timber."""
    pc, Lp, ppm = _L(a)
    d, x0, x1, h = pc.d0, pc.x0, pc.x1, pc.z1 - pc.z0
    r = random.Random(a['seed'])
    top = [Lp(x0, d, h), Lp(x1, d, h)]
    rub = [Lp(x0 + 0.2, d, h)]
    for u in np.linspace(0.05, 0.95, 9):
        rub.append(Lp(x0 + (x1 - x0) * u, d, h + 0.2 + 0.5 * math.sin(u * math.pi) * r.uniform(0.6, 1.2)))
    rub.append(Lp(x1 - 0.2, d, h))
    p.poly(rub, (150, 140, 128), INK, 1.6)
    p.poly([top[0], top[1], Lp(x1 - 0.5, d, 0), Lp(x0 + 0.5, d, 0)], a['colour'], INK, 2.0)
    for k in (0.3, 0.7):
        p.line([Lp(x0 + 0.5 + (x1 - x0 - 1) * k, d, 0.1), Lp(x0 + 0.2 + (x1 - x0 - 0.4) * k, d, h - 0.1)],
               dk(a['colour'], 0.8), 2.0)


@kind('portacabin', params={'colour': 'c'}, defaults={'colour': (226, 226, 218)})
def portacabin(p, img, cam, a, t):
    """A site cabin on blocks: ribbed walls, two windows with grilles, a door with steps."""
    pc, Lp, ppm = _L(a)
    d, x0, x1, z0, z1 = pc.d0, pc.x0, pc.x1, pc.z0, pc.z1
    p.poly(_face(Lp, x0, x1, d, z0 + 0.3, z1), a['colour'], INK, 2.0)
    for xx in np.arange(x0 + 0.3, x1, 0.3):
        p.line([Lp(xx, d, z0 + 0.35), Lp(xx, d, z1 - 0.05)], dk(a['colour'], 0.9), 1.0)
    for wx in (x0 + 0.6, x1 - 2.0):
        p.poly(_face(Lp, wx, wx + 1.3, d, z0 + 1.3, z0 + 2.2), (150, 166, 176), INK, 1.6)
        for xx in np.arange(wx + 0.15, wx + 1.3, 0.15):
            p.line([Lp(xx, d, z0 + 1.3), Lp(xx, d, z0 + 2.2)], (90, 94, 100), 1.0)
    mx = (x0 + x1) / 2
    p.poly(_face(Lp, mx - 0.45, mx + 0.45, d, z0 + 0.3, z0 + 2.3), dk(a['colour'], 0.82), INK, 1.6)
    p.poly(_face(Lp, mx - 0.6, mx + 0.6, d - 0.3, z0, z0 + 0.3), (120, 120, 118), INK, 1.4)


@kind('hoarding', params={'colour': 'c', 'panel': 'n'}, defaults={'colour': (40, 86, 160), 'panel': 2.4})
def hoarding(p, img, cam, a, t):
    """A site hoarding: painted plywood panels with dark joints (blue, as the site photos)."""
    pc, Lp, ppm = _L(a)
    d = pc.d0
    p.poly(_face(Lp, pc.x0, pc.x1, d, pc.z0, pc.z1), a['colour'], INK, 2.0)
    for xx in np.arange(pc.x0 + a['panel'], pc.x1, a['panel']):
        p.line([Lp(xx, d, pc.z0), Lp(xx, d, pc.z1)], dk(a['colour'], 0.75), 1.4)


@kind('cone', params={'size': 'n'}, defaults={'size': 0.75})
def cone(p, img, cam, a, t):
    """A traffic cone (0.75 m): orange, one white band, a black square foot."""
    pc, Lp, ppm = _L(a)
    s = a['size'] * ppm(pc.d0)
    p.poly(quad(-s * 0.3, -s * 0.06, s * 0.3, 0), (40, 40, 40), INK, 1.2)
    p.poly([(-s * 0.06, -s), (s * 0.06, -s), (s * 0.2, -s * 0.06), (-s * 0.2, -s * 0.06)], (236, 110, 30), INK, 1.6)
    p.poly([(-s * 0.1, -s * 0.66), (s * 0.1, -s * 0.66), (s * 0.13, -s * 0.48), (-s * 0.13, -s * 0.48)],
           (246, 246, 240), None)


@kind('pallet', params={'colour': 'c', 'courses': 'n'}, defaults={'colour': (172, 168, 160), 'courses': 4})
def pallet(p, img, cam, a, t):
    """Concrete blocks stacked on a timber pallet (x and z: the stack's face)."""
    pc, Lp, ppm = _L(a)
    d, x0, x1 = pc.d0, pc.x0, pc.x1
    p.poly(_face(Lp, x0, x1, d, 0, 0.14), (160, 124, 76), INK, 1.4)
    n = int(a['courses'])
    for k in range(n):
        z = 0.14 + 0.215 * k
        off = 0.22 * (k % 2)
        xx = x0 + off - 0.44 * (k % 2)
        while xx < x1 - 0.05:
            xa, xb = max(x0, xx), min(x1, xx + 0.44)
            p.poly(_face(Lp, xa, xb, d, z, z + 0.215), a['colour'], INK, 1.2)
            xx += 0.44


@kind('heap', params={'colour': 'c', 'dark': 'c'}, defaults={'colour': (206, 178, 120), 'dark': (180, 150, 96)})
def heap(p, img, cam, a, t):
    """A heap of sand or spoil: a lumpy mound across x, z1 high, a shaded side."""
    pc, Lp, ppm = _L(a)
    d, x0, x1, h = pc.d0, pc.x0, pc.x1, pc.z1
    r = random.Random(a['seed'])
    pts = [Lp(x0, d, 0)]
    for u in np.linspace(0.05, 0.95, 14):
        pts.append(Lp(x0 + (x1 - x0) * u, d, h * math.sin(u * math.pi) ** 0.8 * r.uniform(0.92, 1.05)))
    pts.append(Lp(x1, d, 0))
    p.poly(pts, a['colour'], INK, 2.0)
    half = [pts[0]] + pts[1:8] + [Lp(x0 + (x1 - x0) * 0.45, d, 0)]
    p.poly(half, a['dark'], None)


# ================================================================================================ bookcase
BOOKS = [(112, 62, 34), (86, 48, 26), (142, 86, 44), (122, 30, 30), (96, 24, 28), (38, 72, 48), (28, 56, 40),
         (176, 132, 80), (38, 46, 76), (70, 40, 26)]
GOLD = (214, 172, 76)


@kind('bookcase', params={'colour': 'c', 'dark': 'c', 'light': 'c', 'bays': 'n', 'shelf': 'n', 'plinth': 'n'},
      defaults={'colour': 'oak', 'dark': 'oak dark', 'light': 'oak light', 'bays': 2, 'shelf': 0.36, 'plinth': 0.8})
def bookcase(p, img, cam, a, t):
    """Floor-to-cornice oak bookcases packed with leather books (Ad-Vanced Notice's study, made general): `bays`
    bays across x, shelves every `shelf` m above a cupboard plinth, books in ten leathers with gold spine bands,
    a short stack lying flat now and then, a cornice."""
    pc, Lp, ppm = _L(a)
    d, x0, x1, z0, z1 = pc.d0, pc.x0, pc.x1, pc.z0, pc.z1
    pp = ppm(d)
    n = int(a['bays'])
    ups = [x0 + (x1 - x0) * k / n for k in range(n + 1)]
    for a0, b0 in zip(ups, ups[1:]):
        p.poly(_face(Lp, a0, b0, d + 0.3, z0, z1 - 0.25), dk(a['dark'], 0.55), None)
        z = z0 + a['plinth']
        k = 0
        while z + 0.22 < z1 - 0.25:
            ztop = min(z + a['shelf'], z1 - 0.25)
            r = random.Random(a['seed'] * 977 + int(a0 * 100) + 31 * k)
            x = a0 + 0.06
            while x < b0 - 0.08:
                bw = r.uniform(0.025, 0.065)
                if r.random() < 0.06 and x < b0 - 0.35:            # a short stack lying flat
                    hh = 0.0
                    for j in range(r.randint(2, 4)):
                        th = r.uniform(0.035, 0.06)
                        p.poly(_face(Lp, x, x + r.uniform(0.18, 0.26), d + 0.1, z + 0.03 + hh, z + 0.03 + hh + th),
                               r.choice(BOOKS), INK, 1.0)
                        hh += th
                    x += 0.3
                    continue
                bh = min(ztop - z - 0.05, r.uniform(0.2, 0.31))
                col = r.choice(BOOKS)
                p.poly(_face(Lp, x, x + bw, d + 0.1, z + 0.03, z + 0.03 + bh), col, INK, 1.0)
                if bw * pp > 5:
                    for zz in (z + 0.06, z + bh - 0.01):
                        (lx, ly), (rx_, _) = Lp(x + 0.005, d + 0.1, zz), Lp(x + bw - 0.005, d + 0.1, zz)
                        p.line([(lx, ly), (rx_, ly)], GOLD, max(1.0, 0.012 * pp))
                x += bw + r.uniform(0.0, 0.006)
            p.poly(_face(Lp, a0, b0, d, z, z + 0.035), a['light'], INK, 1.4)
            z = ztop
            k += 1
        p.poly(_face(Lp, a0, b0, d, z0, z0 + a['plinth']), a['colour'], INK, 1.8)      # the cupboard plinth
        for dx in (0.0, (b0 - a0) / 2):
            p.poly(_face(Lp, a0 + dx + 0.08, a0 + dx + (b0 - a0) / 2 - 0.04, d - 0.01, z0 + 0.1, z0 + a['plinth'] - 0.1),
                   a['dark'], INK, 1.2)
    for u in ups:                                                                    # the uprights
        p.poly(_face(Lp, u - 0.05, u + 0.05, d - 0.02, z0, z1 - 0.2), a['colour'], INK, 1.8)
    p.poly(_face(Lp, x0 - 0.12, x1 + 0.12, d - 0.04, z1 - 0.25, z1), a['colour'], INK, 2.0)  # cornice
    p.poly(_face(Lp, x0 - 0.16, x1 + 0.16, d - 0.06, z1 - 0.08, z1), a['light'], INK, 1.6)


# ================================================================================================ double doors
def door_angle(t, at, swing=0.35):
    """How far each leaf has swung (degrees): shut before `at`, thrown open over `swing` s (fast, eased out), hitting
    its stop at 100 degrees, bouncing back to about 84, settling at 92 (a door slammed open, Sam's rule 5)."""
    if at is None or t < at:
        return 0.0
    u = (t - at) / swing
    if u < 1.0:
        return 100.0 * (1 - (1 - u) ** 2.2)
    v = (t - at - swing) / 0.5
    if v < 1.0:
        return 92.0 + 8.0 * math.cos(v * math.pi * 1.5) * math.exp(-2.5 * v)
    return 92.0


def _beyond(img, draws, opening):
    """Whoever is in the space beyond an opening (paint_with's `beyond`), drawn on their own layer and clipped to the
    opening (screen polygon), so nothing in the corridor shows on the wall beside the doorway."""
    from PIL import Image, ImageDraw
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    # far to near (Open Wounds chat 37, Sam's note 23.4: drawn in list order, a farther guest came out over a nearer
    # wolf in the corridor): (depth m, draw) pairs are sorted; a bare draw keeps its place, farthest
    keyed = [(float('inf'), n, fn) if callable(fn) else (fn[0], n, fn[1]) for n, fn in enumerate(draws)]
    import cover
    with cover.through():
        for _, _, fn in sorted(keyed, key=lambda q: (-q[0], q[1])):
            fn(layer)
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).polygon([tuple(map(float, q)) for q in opening], fill=255)
    a = np.asarray(layer).copy()
    a[..., 3] = (a[..., 3].astype(np.uint16) * np.asarray(mask) // 255).astype(np.uint8)
    img.alpha_composite(Image.fromarray(a))


@kind('double doors', params={'colour': 'c', 'panel': 'c', 'beyond': 'c', 'floor': 'c', 'open at': 'n',
                              'swing': 'n', 'open': 'n', 'corridor': 'n', 'passage': 'n'},
      defaults={'colour': 'oak', 'panel': 'oak dark', 'beyond': (232, 214, 172), 'floor': (150, 100, 64),
                'open at': -1.0, 'swing': 0.35, 'open': 0.0, 'corridor': 3.0, 'passage': 0.0})
def double_doors(p, img, cam, a, t):
    """A pair of tall panelled doors in a moulded architrave; from `open at` s they are thrown open into the room
    (both leaves swing towards the lens, hit their stops, bounce, stay), showing the lit corridor beyond (its back
    wall, floor, a wall light). `open` 1 draws them open from the start. The leaves are drawn in depth (each hinge at
    the opening's side), so they turn as real doors would through this camera."""
    pc, Lp, ppm = _L(a)
    d, x0, x1, z0, z1 = pc.d0, pc.x0, pc.x1, pc.z0, pc.z1
    pp = ppm(d)
    ang = 92.0 if a['open'] else door_angle(t, a['open at'] if a['open at'] >= 0 else None, a['swing'])
    # the corridor beyond, seen through the opening only: its floor, side walls and ceiling running `corridor` m back
    # to its far wall (each face from the opening's edge, so perspective keeps all of it inside the doorway), a wall
    # light. Open Wounds note 15 (Sam, 26 Nov: "all of the characters appear from a sudden blank void at the end of the
    # corridor"): a long corridor (`corridor` 9) is a real place to come from: a runner down the floor, panelled doors
    # and lights along the walls, a tall lit window at its end, and (`passage` m from the doorway) a cross passage whose
    # openings people come round, out of sight behind the corridor's walls until they turn into it.
    D = d + a['corridor']
    shade = mix(a['beyond'], (120, 100, 80), 0.3)
    p.poly([Lp(x0, d, z0), Lp(x1, d, z0), Lp(x1, D, z0), Lp(x0, D, z0)], a['floor'], None)
    p.poly([Lp(x0, d, z1), Lp(x1, d, z1), Lp(x1, D, z1), Lp(x0, D, z1)], dk(a['beyond'], 0.8), None)
    p.poly([Lp(x0, d, z0), Lp(x0, D, z0), Lp(x0, D, z1), Lp(x0, d, z1)], shade, None)
    p.poly([Lp(x1, d, z0), Lp(x1, D, z0), Lp(x1, D, z1), Lp(x1, d, z1)], shade, None)
    p.poly(_face(Lp, x0, x1, D, z0, z1), a['beyond'], INK, 1.2)
    long_ = a['corridor'] > 4.0
    if long_:
        w_ = x1 - x0
        p.poly([Lp(x0 + w_ * 0.22, d, z0), Lp(x1 - w_ * 0.22, d, z0), Lp(x1 - w_ * 0.22, D, z0),
                Lp(x0 + w_ * 0.22, D, z0)], (120, 34, 36), INK, 1.0)                  # the runner down the floor
        for wd in [d + k for k in (1.6, 3.6)] + ([d + a['passage'] - 1.4] if a['passage'] else []):
            if wd + 1.0 < D:                                                        # panelled doors in the left wall
                p.poly([Lp(x0, wd, z0), Lp(x0, wd + 0.9, z0), Lp(x0, wd + 0.9, z0 + 2.1), Lp(x0, wd, z0 + 2.1)],
                       dk(shade, 0.85), INK, 1.0)
        if a['passage']:                                                            # the cross passage: dark mouths
            pa, pb = d + a['passage'], d + a['passage'] + 1.6
            for xw in (x0, x1):
                p.poly([Lp(xw, pa, z0), Lp(xw, pb, z0), Lp(xw, pb, z0 + 2.5), Lp(xw, pa, z0 + 2.5)],
                       dk(shade, 0.62), INK, 1.0)
        wx0, wx1 = x0 + w_ * 0.25, x1 - w_ * 0.25                                   # the tall window at the end
        p.poly(_face(Lp, wx0, wx1, D - 0.01, z0 + 0.6, z1 - 0.3), (214, 228, 236), INK, 1.2)
        p.poly(_face(Lp, (wx0 + wx1) / 2 - 0.03, (wx0 + wx1) / 2 + 0.03, D - 0.02, z0 + 0.6, z1 - 0.3), a['beyond'], None)
        for ld in (d + 2.6, d + 6.0):                                               # wall lights down the left wall
            if ld < D:
                lx, ly = Lp(x0, ld, z0 + 2.0)
                p.ell(lx, ly, 0.08 * ppm(ld), 0.12 * ppm(ld), (250, 236, 190), INK, 1.0)
    else:
        lx, ly = Lp((x0 + x1) / 2, D, z0 + 2.0)
        p.ell(lx, ly, 0.12 * ppm(D), 0.16 * ppm(D), (250, 236, 190), INK, 1.2)
    if a.get('through'):                                          # who is in the corridor (paint_with's beyond):
        _beyond(img, a['through'], [pc.L.p(x, d, z) for x, z in ((x0, z0), (x1, z0), (x1, z1), (x0, z1))])
    p.poly(_face(Lp, x0, x1, d + 0.001, z0, z1), None, INK, 2.0)
    # the architrave round the opening
    m = 0.16
    for (xa, xb, za, zb) in ((x0 - m, x0, z0, z1 + m), (x1, x1 + m, z0, z1 + m), (x0 - m, x1 + m, z1, z1 + m)):
        p.poly(_face(Lp, xa, xb, d - 0.02, za, zb), a['colour'], INK, 1.8)
    p.poly(_face(Lp, x0 - m - 0.1, x1 + m + 0.1, d - 0.04, z1 + m, z1 + m + 0.14), dk(a['colour'], 1.08), INK, 1.8)
    half = (x1 - x0) / 2
    th = math.radians(ang)
    for hinge, sgn in ((x0, 1), (x1, -1)):                       # each leaf: hinge to its swinging edge, in depth
        ex, ed = hinge + sgn * half * math.cos(th), d - half * math.sin(th)
        def at(u, z, hinge=hinge, ex=ex, ed=ed):
            return Lp(hinge + (ex - hinge) * u, d + (ed - d) * u, z)
        p.poly([at(0, z1), at(1, z1), at(1, z0), at(0, z0)], a['colour'], INK, 2.0)
        for (ua, ub, za, zb) in ((0.15, 0.85, z0 + (z1 - z0) * 0.55, z1 - 0.2), (0.15, 0.85, z0 + 0.2, z0 + (z1 - z0) * 0.48)):
            p.poly([at(ua, zb), at(ub, zb), at(ub, za), at(ua, za)], a['panel'], INK, 1.4)
        kx, ky = at(0.9, z0 + 1.05)
        p.ell(kx, ky, max(1.5, 0.03 * pp), max(1.5, 0.03 * pp), GOLD, INK, 1.0)


# ================================================================================================ chandelier
@kind('chandelier', params={'arms': 'n', 'drop': 'n', 'colour': 'c'}, defaults={'arms': 8, 'drop': 0.9,
                                                                               'colour': (196, 160, 80)})
def chandelier(p, img, cam, a, t):
    """A brass chandelier hanging from the ceiling at its point: the chain (`drop` m), a ring of candle arms seen from
    below the level (an ellipse), cream candle lamps, a few crystal drops."""
    pc, Lp, ppm = _L(a)
    s = ppm(pc.d0)
    top = (0, -a['drop'] * s)
    p.line([top, (0, -0.25 * s)], INK, max(1.4, 0.02 * s))
    R = 0.45 * s
    n = int(a['arms'])
    back = [k for k in range(n) if math.sin(2 * math.pi * k / n) < 0]
    front = [k for k in range(n) if k not in back]
    def arm(k):
        u = 2 * math.pi * k / n
        ex, ey = R * math.cos(u), R * 0.25 * math.sin(u)
        p.line([(0, 0), (ex * 0.6, ey * 0.6 + 0.06 * s), (ex, ey)], a['colour'], max(1.6, 0.025 * s))
        p.poly(quad(ex - 0.025 * s, ey - 0.14 * s, ex + 0.025 * s, ey), (246, 240, 222), INK, 1.0)
        p.ell(ex, ey - 0.17 * s, 0.035 * s, 0.05 * s, (252, 236, 180), INK, 1.0)
        p.ell(ex, ey + 0.05 * s, 0.015 * s, 0.03 * s, (226, 234, 238), INK, 0.8)
    for k in back:
        arm(k)
    p.ell(0, 0, 0.09 * s, 0.14 * s, a['colour'], INK, 1.6)
    p.ell(0, 0.18 * s, 0.03 * s, 0.06 * s, (226, 234, 238), INK, 1.0)
    for k in front:
        arm(k)
