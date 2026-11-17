#!/usr/bin/env python3
"""MAP  The places kit's meeting-table pieces (Milburn, 17 Nov: the Cabinet Room; any film's boardroom, committee room or
negotiating table can use them). Each registers into places_parts.KINDS, drawn in the house look (flat colour, ink
outline) at its true size through any level camera.

  table top ...... a table's top seen from across it, in perspective: `x A to B, z TOP, depth FAR, near NEAR`; cloth
                   (baize) with a wooden rim along the far edge and the near edge's thickness
  curtain ........ a hanging curtain in folds (light and shade strips), a damask pattern, a wavy hem, a tie-back
  tumbler ........ a cut-glass water tumbler on a table (the point: its foot, middle), water level, facets, a glint
  name card ...... a white folded name card on a table (the point: its foot, middle), its lettering scaled to width
  folder ......... a leather folder lying flat on a table, in perspective: `x A to B, z TOP, depth FAR, near NEAR`;
                   a gold crest stamped in the middle

Map: table top 30 | curtain 70 | tumbler 115 | name card 140 | folder 160
"""
import math
import random

from ed import INK
from places_parts import kind, wob, quad, mix, dk


def _flat(a, x0, x1, z, d0, d1):
    """The four corners of a flat rectangle at height z from depth d0 (far) to d1 (near), in the piece's units."""
    P = a['piece'].P
    return [P(x0, z, d0), P(x1, z, d0), P(x1, z, d1), P(x0, z, d1)]


# ================================================================================================ table top
@kind('table top', params={'colour': 'c', 'rim': 'c', 'near': 'n', 'thick': 'n', 'streaks': 'n'},
      defaults={'colour': (44, 104, 92), 'rim': (96, 58, 36), 'near': 0.5, 'thick': 0.05, 'streaks': 5}, band=True)
def table_top(p, img, cam, a, t):
    """A table's top from across it: the cloth in perspective, a few soft lighter streaks of nap running away from
    the eye, the wooden rim along the far edge, the near edge's thickness (when in the picture)."""
    pc = a['piece']
    x0, x1, z, d0, d1 = pc.x0, pc.x1, pc.z1, pc.d0, float(a['near'])
    p.poly(_flat(a, x0, x1, z, d0, d1), a['colour'], INK, 2.4)
    r = random.Random(a['seed'])
    for k in range(int(a['streaks'])):                 # the nap catches the light in long soft bands
        u = (k + 0.5) / a['streaks'] + r.uniform(-0.04, 0.04)
        xa, xb = x0 + (x1 - x0) * (u - 0.008), x0 + (x1 - x0) * (u + 0.008)
        p.poly(_flat(a, xa, xb, z, d0, d1), mix(a['colour'], (255, 255, 255), 0.06), None)
    rim = 0.035                                         # the polished rim along the far edge
    p.poly([pc.P(x0, z, d0), pc.P(x1, z, d0), pc.P(x1, z, d0 - rim), pc.P(x0, z, d0 - rim)], a['rim'], INK, 1.6)
    th = float(a['thick'])
    p.poly([pc.P(x0, z, d1), pc.P(x1, z, d1), pc.P(x1, z - th, d1), pc.P(x0, z - th, d1)], a['rim'], INK, 2.4)


# ================================================================================================ curtain
@kind('curtain', ref=300, params={'colour': 'c', 'dark': 'c', 'pattern': 'c', 'folds': 'n', 'tie': 'n'},
      defaults={'colour': (40, 120, 70), 'dark': (24, 82, 46), 'pattern': (60, 146, 92), 'folds': 5, 'tie': 0.0})
def curtain(p, img, cam, a, t):
    """A hanging curtain: `folds` deep folds (a lit face, a shaded face each), a damask pattern of small diamonds and
    leaves that follows the folds, a wavy hem; `tie` (0-1): gathered in by a tie-back at that share of the way down."""
    w, h = a['w'], a['h']
    r = random.Random(a['seed'])
    n = max(2, int(a['folds']))
    tie = a['tie']

    def X(u, y):
        """Across share u at height y, pulled in towards the middle by a tie-back."""
        if not tie:
            return u * w
        ty = h * tie
        pull = max(0.0, 1.0 - abs(y - ty) / (h * 0.45)) * 0.35
        return (0.5 + (u - 0.5) * (1 - pull)) * w

    ys = [h * k / 24 for k in range(25)]
    out = [(X(0, y), y) for y in ys] + [(X(1, y), y) for y in reversed(ys)]
    p.poly(out, a['colour'], INK, 2.6)
    for k in range(n):                                   # each fold: the shaded half
        u0, u1 = (k + 0.5) / n, (k + 0.95) / n
        side = [(X(u0, y), y) for y in ys] + [(X(u1, y), y) for y in reversed(ys)]
        p.poly(side, a['dark'], None)
        p.line([(X(u0, y), y) for y in ys], dk(a['dark'], 0.8), 1.4)
    for row in range(int(h / 46)):                       # the damask: a small diamond and two leaves, staggered
        y = 30 + row * 46
        for k in range(n * 2):
            u = (k + 0.25 + 0.5 * (row % 2)) / (n * 2)
            if not 0.1 < u < 0.9:                    # the pattern stays inside the curtain's edges
                continue
            cx = X(u, y)
            c = a['pattern'] if (k % 2 == 0) else mix(a['pattern'], a['dark'], 0.5)
            p.poly([(cx, y - 9), (cx + 6, y), (cx, y + 9), (cx - 6, y)], c, None)
            p.ell(cx - 9, y + 12, 4, 2.4, c, None)
            p.ell(cx + 9, y + 12, 4, 2.4, c, None)
    hem = [(X(k / 20, h), h + (6 if k % 2 else -2) + r.uniform(-1.5, 1.5)) for k in range(21)]
    p.line(hem, INK, 2.6)
    if tie:                                              # the tie-back: a gold cord round the gathered folds
        ty = h * tie
        p.poly(quad(X(0, ty) - 4, ty - 10, X(1, ty) + 4, ty + 10), (196, 160, 70), INK, 1.8)
        p.ell(X(0, ty) - 6, ty + 18, 9, 14, (196, 160, 70), INK, 1.6)


# ================================================================================================ tumbler
@kind('tumbler', ref=1000, params={'full': 'n'}, defaults={'full': 0.6}, box=lambda a: (-42, -104, 42, 4))
def tumbler(p, img, cam, a, t):
    """A cut-glass water tumbler standing on a table (the point: its foot, middle; about 8 cm across, 10 cm tall):
    the glass, the water `full` of the way up, the cut facets low down, a glint."""
    glass, water, edge = (214, 230, 236), (176, 208, 222), (150, 176, 190)
    p.poly([(-34, 0), (34, 0), (40, -100), (-40, -100)], glass, INK, 2.0)
    wy = -100 * a['full']
    p.poly([(-34, 0), (34, 0), (34 + 6 * a['full'], wy), (-34 - 6 * a['full'], wy)], water, None)
    p.ell(0, wy, 34 + 6 * a['full'], 4, mix(water, (255, 255, 255), 0.3), None)
    p.ell(0, -100, 40, 6, mix(glass, (255, 255, 255), 0.4), INK, 1.6)
    for k in range(-3, 4):                               # the cut: a row of tall diamonds round the foot
        x = k * 10
        p.line([(x, -4), (x + 5, -30), (x + 10, -4)], edge, 1.2)
    p.poly([(-34, 0), (34, 0), (34, -8), (-34, -8)], mix(glass, edge, 0.5), INK, 1.6)
    p.line([(-26, -88), (-24, -40)], (255, 255, 255), 3.0)


# ================================================================================================ name card
@kind('name card', ref=1000, params={'text': 's', 'width': 'n'}, defaults={'text': '', 'width': 0.17},
      box=lambda a: (-a['width'] * 500 - 4, -66, a['width'] * 500 + 4, 2))
def name_card(p, img, cam, a, t):
    """A white folded name card standing on a table, its face to the camera (the point: its foot, middle; 6 cm tall),
    its lettering scaled to most of its width; its back half shows as a sliver of shade above."""
    import blessed_sets as BS
    hw = a['width'] * 500
    p.poly([(-hw + 6, -64), (hw - 6, -64), (hw - 10, -70), (-hw + 10, -70)], (200, 200, 196), INK, 1.4)
    p.poly([(-hw, 0), (hw, 0), (hw - 6, -64), (-hw + 6, -64)], (250, 250, 246), INK, 1.8)
    if a['text']:
        BS.sign(img, cam, a['text'], 0, -32, hw * 1.5, (40, 40, 48))
    else:
        for k, f in enumerate((0.7, 0.45)):
            p.line([(-hw * f, -40 + 16 * k), (hw * f, -40 + 16 * k)], (130, 130, 136), 3.0)


# ================================================================================================ folder
@kind('folder', params={'colour': 'c', 'crest': 'c', 'near': 'n'},
      defaults={'colour': (150, 36, 40), 'crest': (206, 170, 80)})
def folder(p, img, cam, a, t):
    """A leather folder lying flat on a table (the official red despatch folder): `x A to B, z TOP, depth FAR` with
    `near NEAR` in metres, a darker edge band, a gold crest stamped in the middle."""
    pc = a['piece']
    near = float(a.get('near', pc.d0 - 0.3))
    x0, x1, z, d0 = pc.x0, pc.x1, pc.z1, pc.d0
    th = 0.012
    P = pc.P
    p.poly([P(x0, z, near), P(x1, z, near), P(x1, z + th, near), P(x0, z + th, near)], dk(a['colour'], 0.7), INK, 1.6)
    top = [P(x0, z + th, d0), P(x1, z + th, d0), P(x1, z + th, near), P(x0, z + th, near)]
    p.poly(top, a['colour'], INK, 2.0)
    m = 0.018
    inner = [P(x0 + m, z + th, d0 - m), P(x1 - m, z + th, d0 - m), P(x1 - m, z + th, near + m),
             P(x0 + m, z + th, near + m)]
    p.poly(inner, mix(a['colour'], (255, 255, 255), 0.08), None)
    cx, cd = (x0 + x1) / 2, (d0 + near) / 2
    X, Y = P(cx, z + th, cd)
    rx = abs(P(cx + 0.03, z + th, cd)[0] - X)
    ry = abs(P(cx, z + th, cd - 0.03)[1] - Y)
    p.ell(X, Y, rx, max(1.5, ry), a['crest'], None)

