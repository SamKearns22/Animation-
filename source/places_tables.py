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
  fireplace ...... (Milburn chat 5) a marble chimneypiece on a wall: jambs, frieze, mantel shelf, the dark firebox and
                   an iron grate, a hearth stone
  portrait ....... (chat 5) an old oil portrait in a gilt frame: a gentleman of the 1700s in a powdered wig (nobody real)
  tall glass ..... (chat 5) a tall glass of sparkling water on a table: bubbles rising (moving), a slice of lemon
  can ............ (chat 5) a drinks can standing on a table: its colour, a band and its name across it
  coaster ........ (chat 10) a round coaster lying flat on a table, in perspective: `at X Z, depth D, width W`
                   (metres); a thin edge, a lighter inner ring (put a drink at the same point after it)

Map: table top 30 | curtain 70 | tumbler 115 | name card 140 | folder 160 | fireplace 190 | portrait 230 |
     tall glass 270 | can 300 | coaster 320
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



# ================================================================================================ fireplace
@kind('fireplace', ref=300, params={'marble': 'c', 'vein': 'c'},
      defaults={'marble': (240, 236, 226), 'vein': (206, 200, 190)})
def fireplace(p, img, cam, a, t):
    """A marble chimneypiece standing on the floor against the wall (`x A to B, z 0 to TOP`): two jambs, a frieze with
    a raised middle tablet, the mantel shelf proud of it, the dark firebox with an iron grate, a hearth stone."""
    w, h = a['w'], a['h']
    m, vein = a['marble'], a['vein']
    shade = dk(m, 0.86)
    jw = w * 0.16                                        # the jambs
    fb_top = h * 0.36                                    # the firebox's top (from the top of the piece)
    p.poly(quad(-w * 0.04, h - h * 0.05, w * 1.04, h), dk(m, 0.8), INK, 2.2)        # the hearth stone
    p.poly(quad(0, h * 0.12, w, h - h * 0.05), m, INK, 2.6)                        # the whole surround
    p.poly(quad(jw, fb_top, w - jw, h - h * 0.05), (34, 30, 30), INK, 2.4)        # the firebox
    p.poly(quad(jw + w * 0.04, fb_top + h * 0.05, w - jw - w * 0.04, h - h * 0.05), (22, 20, 20), None)
    gx0, gx1, gy = jw + w * 0.12, w - jw - w * 0.12, h * 0.8                         # the iron grate and its coals
    p.poly([(gx0, gy), (gx1, gy), (gx1 - w * 0.03, h - h * 0.07), (gx0 + w * 0.03, h - h * 0.07)], (52, 48, 46), INK, 1.8)
    for k in range(6):
        x = gx0 + (gx1 - gx0) * (k + 0.5) / 6
        p.ell(x, gy - h * 0.012, w * 0.03, h * 0.02, (64, 58, 56), None)
    for x in (gx0, gx1):
        p.line([(x, gy), (x, h - h * 0.05)], INK, 2.0)
    p.poly(quad(0, h * 0.12, w, fb_top), mix(m, (255, 255, 255), 0.2), INK, 2.2)  # the frieze
    p.poly(quad(w * 0.38, h * 0.16, w * 0.62, fb_top - h * 0.04), shade, INK, 1.8)  # its middle tablet
    for x in (jw * 0.5, w - jw * 0.5):                                                # the jambs' fluting
        for dx in (-jw * 0.22, 0, jw * 0.22):
            p.line([(x + dx, fb_top + h * 0.04), (x + dx, h - h * 0.1)], shade, 1.6)
    p.poly(quad(-w * 0.06, h * 0.07, w * 1.06, h * 0.12), m, INK, 2.4)              # the mantel shelf
    p.poly(quad(-w * 0.06, h * 0.105, w * 1.06, h * 0.12), shade, None)
    r = random.Random(a['seed'])
    for _ in range(5):                                                                # a few soft veins
        x, y = r.uniform(0.05, 0.95) * w, r.uniform(0.15, 0.9) * h
        if jw < x < w - jw and y > fb_top:
            continue
        p.line([(x, y), (x + r.uniform(-20, 20), y + r.uniform(8, 26)), (x + r.uniform(-24, 24), y + r.uniform(20, 40))],
               vein, 1.2)


# ================================================================================================ portrait
@kind('portrait', ref=300, params={'gilt': 'c', 'ground': 'c', 'coat': 'c'},
      defaults={'gilt': (196, 156, 70), 'ground': (58, 54, 40), 'coat': (110, 30, 34)})
def portrait(p, img, cam, a, t):
    """An old oil portrait on the wall in a deep gilt frame: a gentleman of the 1700s, half length, in a powdered
    wig and a red coat, on a dark ground (nobody real; the Cabinet Room's first-minister portrait as an idea)."""
    w, h = a['w'], a['h']
    g = a['gilt']
    fr = min(w, h) * 0.11
    p.poly(quad(0, 0, w, h), g, INK, 2.6)
    p.poly(quad(fr * 0.45, fr * 0.45, w - fr * 0.45, h - fr * 0.45), dk(g, 0.8), INK, 1.4)
    p.poly(quad(fr, fr, w - fr, h - fr), a['ground'], INK, 2.0)
    cx = w / 2
    iw, ih = w - 2 * fr, h - 2 * fr
    sh_y = fr + ih * 0.62                                                             # the shoulders and coat
    p.poly([(cx - iw * 0.42, h - fr), (cx - iw * 0.4, sh_y + ih * 0.08), (cx - iw * 0.18, sh_y),
            (cx + iw * 0.18, sh_y), (cx + iw * 0.4, sh_y + ih * 0.08), (cx + iw * 0.42, h - fr)], a['coat'], INK, 1.8)
    p.poly([(cx - iw * 0.07, sh_y), (cx + iw * 0.07, sh_y), (cx, h - fr - ih * 0.1)], (238, 232, 220), INK, 1.4)
    hy = fr + ih * 0.42                                                               # the wig, then the face
    p.ell(cx, hy, iw * 0.2, ih * 0.2, (226, 222, 214), INK, 1.8)
    for sgn in (-1, 1):
        p.ell(cx + sgn * iw * 0.18, hy + ih * 0.12, iw * 0.07, ih * 0.08, (220, 216, 208), INK, 1.4)
    p.ell(cx, hy + ih * 0.03, iw * 0.11, ih * 0.13, (226, 186, 160), INK, 1.6)
    for sgn in (-1, 1):
        p.ell(cx + sgn * iw * 0.04, hy, iw * 0.012, ih * 0.01, (40, 30, 26), None)
    p.line([(cx - iw * 0.03, hy + ih * 0.09), (cx + iw * 0.03, hy + ih * 0.09)], (150, 90, 80), 1.4)


# ================================================================================================ tall glass
@kind('tall glass', ref=1000, params={'full': 'n', 'lemon': 'n'}, defaults={'full': 0.8, 'lemon': 1},
      box=lambda a: (-36, -164, 36, 4))
def tall_glass(p, img, cam, a, t):
    """A tall glass of sparkling water on a table (the point: its foot, middle; 7 cm across, 16 cm tall): the water
    `full` of the way up, bubbles rising all the time (t), a slice of lemon, a glint."""
    glass, water = (216, 232, 238), (186, 216, 228)
    p.poly([(-30, 0), (30, 0), (34, -160), (-34, -160)], glass, INK, 2.0)
    wy = -160 * a['full']
    p.poly([(-30, 0), (30, 0), (30 + 4 * a['full'], wy), (-30 - 4 * a['full'], wy)], water, None)
    p.ell(0, wy, 31 + 4 * a['full'], 4, mix(water, (255, 255, 255), 0.35), None)
    r = random.Random(a['seed'])
    for k in range(14):                                  # bubbles: each its own column and speed, looping
        x = r.uniform(-22, 22)
        sp = r.uniform(40, 80)
        y = -4 - ((t * sp + r.uniform(0, 200)) % (-wy - 8))
        rr = r.uniform(1.8, 3.4)
        p.ell(x, y, rr, rr, (246, 252, 255), (150, 180, 196), 1.0)
    if a['lemon']:                                       # a lemon slice on the rim
        p.ell(-34, -150, 14, 14, (246, 214, 70), INK, 1.6)
        p.ell(-34, -150, 10, 10, (252, 236, 150), None)
    p.ell(0, -160, 34, 5, mix(glass, (255, 255, 255), 0.4), INK, 1.6)
    p.line([(-22, -146), (-20, -30)], (255, 255, 255), 3.0)


# ================================================================================================ can
@kind('can', ref=1000, params={'colour': 'c', 'band': 'c', 'text': 's', 'ink': 'c'},
      defaults={'colour': (110, 38, 120), 'band': (236, 70, 120), 'text': '', 'ink': (255, 255, 255)},
      box=lambda a: (-36, -126, 36, 4))
def can(p, img, cam, a, t):
    """A drinks can standing on a table (the point: its foot, middle; 6.6 cm across, 12 cm tall): its colour, a
    bright band, its name across it, the silver top and foot, a glint."""
    import blessed_sets as BS
    silver = (198, 200, 206)
    p.poly([(-33, -4), (33, -4), (33, -114), (-33, -114)], a['colour'], INK, 2.2)
    p.poly([(-33, -46), (33, -46), (33, -66), (-33, -66)], a['band'], None)
    p.poly([(-28, 0), (28, 0), (33, -6), (-33, -6)], silver, INK, 1.6)            # the foot
    p.poly([(-33, -114), (33, -114), (28, -122), (-28, -122)], silver, INK, 1.6)  # the shoulder and top
    p.ell(0, -122, 28, 4, dk(silver, 0.9), INK, 1.2)
    if a['text']:
        BS.sign(img, cam, a['text'], 0, -84, 60, tuple(a['ink']))
    p.line([(-24, -108), (-24, -12)], mix(a['colour'], (255, 255, 255), 0.4), 3.0)


# ================================================================================================ coaster
@kind('coaster', params={'colour': 'c', 'width': 'n'}, defaults={'colour': (120, 72, 44), 'width': 0.1})
def coaster(p, img, cam, a, t):
    """A round coaster lying flat on a table (Milburn note 10): `at X Z, depth D` its middle, `width W` across in
    metres; drawn as a true circle in perspective, its thickness, a lighter inner ring. Draw it before the drink."""
    pc = a['piece']
    P = pc.P
    cx, z, cd = (pc.x0 + pc.x1) / 2, pc.z1, pc.d0
    r, th = float(a["width"]) / 2, 0.01
    ring = lambda rr, zz: [P(cx + rr * math.cos(k * math.pi / 16), zz, cd + rr * math.sin(k * math.pi / 16))
                           for k in range(32)]
    p.poly(ring(r, z), dk(a['colour'], 0.7), INK, 1.8)                # its edge (shows below the top)
    p.poly(ring(r, z + th), a['colour'], INK, 1.8)
    p.poly(ring(r * 0.78, z + th), mix(a['colour'], (255, 255, 255), 0.14), None)
