#!/usr/bin/env python3
"""Protest Tiers: the cast (chat 5, 14 Nov). Everyone is a Glimpse (rule 24): wide shots, small, one view per job.

MAP
  setup ............. the people kit's bodies (story/protest-tiers-people.txt), circle hands, the arm guard
  glass ............. see-through fills (visors, shields) on a small layer, composited
  FORCES / officer .. one riot officer, four forces' colours (Mossos, Polizei, CRS, Policia)
  riot_helmet ....... dome, see-through visor down, neck guard; every view (head prop)
  armour ............ chest and back plates, belt (body prop); shoulder badges on the arm (Albania)
  shield / baton .... long clear shield with the force's label band (held in front); short black baton
  rioter ............ black hoodie with the hood up (hood + mask head prop; pocket and drawstrings body prop)
  protester ......... a crowd member for tier t1..t4; keys, placard, phone, flag held up
  props ............. stone, bottle (Molotov), give-way road sign on its pole, RPG
  POSES ............. officer: line, baton_up, pushed; rioter: run(t), throw(u), swing(u), haul; marcher: march,
                      keys, placard, phone, flag
  moped ............. 3D-projected scooter (side, three-quarter) with a driver and the RPG passenger
  dress (round 1) ... TOURIST_DRESS: caps, visor, bags, camera, headscarf, cardigan, skirt, apron; tourist(who)
  cart .............. the Molotov seller's cart (umbrella behind him, the rest over his legs); seller_scene
  shrug / peace ..... the passenger's shrug (end shot C), the selfie's peace sign / thumb (pose 'selfie')
  sheet ............. the cast sheet (everyone alone, large) and glimpse panels (each in its tier's rough frame)

    python3 source/protest_tiers_cast.py sheet OUT.jpg       the cast sheet for Sam
    python3 source/protest_tiers_cast.py newcast OUT.jpg     round 1's new cast (tourists, granny, seller + cart, ...)
    python3 source/protest_tiers_cast.py glimpses OUTDIR     each piece in its shot's rough frame + 2x crop + close-up
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import people as PK                  # noqa: E402
import people_parts as PPt           # noqa: E402
import moves                         # noqa: E402
import grips                         # noqa: E402
from ed import INK, curve, oval      # noqa: E402
from satire_style import install_circle_hands   # noqa: E402

B = PPt.B
V = PPt.AV.MC.V
import figure as F                   # noqa: E402
install_circle_hands(B)
F.guard(B)

FILM = 'protest-tiers'
CAST = PK.install(PK.load(FILM))
CROWD = PK.crowds(FILM)['protester']
M = V.M_PER_UNIT
U = 1.0 / M                          # person units per metre


def P3(j, pt):
    """A body-frame point (before lean) -> its 2D point in the person's own drawing frame for this view."""
    return V.project(V.leaned(pt, j.get('lean', 0.0)), j['_yaw'])[0]


# ------------------------------------------------------------------------------------------------ glass
def glass(p, pts, col, alpha, line=INK, lw=2.0):
    """A see-through fill (a visor, a shield): drawn on a small layer the size of its box, then composited."""
    q = [p.cam.P(*a) for a in pts]
    x0, y0 = int(min(a[0] for a in q)) - 4, int(min(a[1] for a in q)) - 4
    x1, y1 = int(max(a[0] for a in q)) + 5, int(max(a[1] for a in q)) + 5
    W, H = p.img.size
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if x1 <= x0 or y1 <= y0:
        return
    lay = Image.new('RGBA', (x1 - x0, y1 - y0), (0, 0, 0, 0))
    ImageDraw.Draw(lay).polygon([(a[0] - x0, a[1] - y0) for a in q], fill=tuple(col) + (int(alpha),))
    p.img.alpha_composite(lay, (x0, y0))
    if line:
        p.poly(pts, None, line, lw)


def _holed(outer, inner):
    """One polygon with a hole: the outline, a cut in to the hole, round it, and back out the same way."""
    k = int(np.argmin([(x - inner[0][0]) ** 2 + (y - inner[0][1]) ** 2 for x, y in outer]))
    return outer[:k + 1] + inner + [inner[0]] + outer[k:]


# ------------------------------------------------------------------------------------------------ the forces
# References: es4/es5 (Mossos: black kit, clear long shields labelled "Policia Mossos d'Esquadra"), de2/de5 (German:
# dark blue-grey padded suits, dark helmets), fr5 (CRS: navy-black, dark helmets, visors), al3/al4 (Albania: WHITE
# helmets with visors, black kit, red shoulder badges, clear shields "POLICIA").
FORCES = {
    'mossos': dict(name='Mossos (Barcelona)', helmet=(30, 32, 40), uniform=(32, 36, 48), armour=(46, 50, 62),
                   label='MOSSOS', label_c=(40, 70, 150), badge=None),
    'polizei': dict(name='Polizei (Frankfurt)', helmet=(48, 60, 84), uniform=(60, 68, 80), armour=(74, 82, 96),
                    label='POLIZEI', label_c=(30, 60, 120), badge=None),
    'crs': dict(name='CRS (Paris)', helmet=(28, 34, 54), uniform=(32, 36, 52), armour=(44, 50, 68),
                label='POLICE', label_c=(30, 40, 90), badge=None),
    'policia': dict(name='Policia (Tirana)', helmet=(236, 236, 232), uniform=(28, 28, 32), armour=(42, 42, 48),
                    label='POLICIA', label_c=(170, 26, 34), badge=(186, 28, 34)),
}
VISOR = (70, 86, 104)
SHIELD = (200, 214, 226)


def officer(force='mossos'):
    f = FORCES[force]
    sp = dict(CAST['officer'])
    sp.update(jacket=f['uniform'], sleeve=f['uniform'], trousers=f['uniform'], glove=(26, 26, 28), force=force,
              name=f"Riot officer, {f['name']}")
    return sp


# ------------------------------------------------------------------------------------------------ fit to the head
# The kit's heads are drawn larger than hw x hh (about 1.5 hw wide with the ears, the crown about 1.9 hh above the head
# centre): a helmet or hood sized from hw/hh left the skull or hair showing over it (chat 6). So each is drawn in its
# own hw/hh design and stretched, per side, to cover the head as it is really drawn in that view (measured once).
_BOX = {}
_VIEW_YAW = {'front': 0, 'three': 45, 'side': 90, 'three_back': 135, 'back': 180}


def head_box(sp, view):
    """(left, right, top) of the bare head as drawn in this view, in person units from the head centre."""
    key = (sp.get('who'), sp.get('hw'), sp.get('hh'), sp.get('head_dy'), view)
    if key not in _BOX:
        ss, B.SS = B.SS, 1
        img = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
        cam = B.Cam(1.0, 540, 960)
        bare = dict(sp, force=None)
        j = V.standing(bare)
        j['_dressed'] = True
        V.person(img, cam, 540, 700, 1.0, dict(bare, full=True, pose='custom'), 0.0, _VIEW_YAW[view], j)
        B.SS = ss
        m = (np.abs(np.asarray(img.convert('RGB')).astype(int) - 255).sum(2) > 20)
        hy = int(700 - 150 + sp.get('head_dy', 10))
        top = int(np.nonzero(m[:hy].any(1))[0].min())
        xs = np.nonzero(m[top:hy + 40].any(0))[0]
        _BOX[key] = (float(xs.min() - 540), float(xs.max() - 540), float(top - hy))
    return _BOX[key]


class FitPen:
    """A pen that stretches a head prop drawn round (hx, hy): x by kl / kr each side, y by kt above and kb below."""
    def __init__(self, p, hx, hy, kl, kr, kt, kb):
        self.p, self.hx, self.hy, self.k = p, hx, hy, (kl, kr, kt, kb)
        self.img = p.img
        pen = self

        class _Cam:
            def P(self, x, y):
                return p.cam.P(*pen.f((x, y)))
        self.cam = _Cam()

    def f(self, q):
        kl, kr, kt, kb = self.k
        x, y = q[0] - self.hx, q[1] - self.hy
        return (self.hx + x * (kl if x < 0 else kr), self.hy + y * (kt if y < 0 else kb))

    def poly(self, pts, *a, **k):
        return self.p.poly([self.f(q) for q in pts], *a, **k)

    def line(self, pts, *a, **k):
        return self.p.line([self.f(q) for q in pts], *a, **k)

    def ell(self, x, y, rx, ry, *a, **k):
        return self.p.ell(*self.f((x, y)), rx, ry, *a, **k)


def fit(p, sp, view, hx, hy, hw, hh, design, margin=12.0):
    """A FitPen that makes a prop whose design reaches (L, R, T, B) hw/hh units cover the drawn head plus a margin."""
    L, R, T, Bt = design[view]
    l, r, t = head_box(sp, view)
    kt = max(1.0, (-t + margin) / (T * hh))
    kb = max(1.0, (1.13 * sp.get('hh', 94) + margin) / (Bt * hh))
    return FitPen(p, hx, hy, max(1.0, (-l + margin) / (L * hw)), max(1.0, (r + margin) / (R * hw)), kt, kb)


HELMET_REACH = {'front': (1.2, 1.2, 1.3, 1.14), 'three': (1.28, 1.28, 1.3, 1.14), 'side': (1.55, 1.48, 1.3, 1.1),
                'three_back': (1.18, 1.18, 1.28, 1.3), 'back': (1.18, 1.18, 1.28, 1.3)}
HOOD_REACH = {'front': (1.34, 1.34, 1.32, 1.18), 'three': (1.4, 1.2, 1.3, 1.18), 'side': (1.6, 1.3, 1.28, 1.18),
              'three_back': (1.3, 1.3, 1.3, 1.5), 'back': (1.3, 1.3, 1.3, 1.5)}


def riot_helmet(p, view, sp, hx, hy):
    """The riot helmet, visor down: a round dome over the ears, the clear tinted visor from the brow to below the chin
    (the face shows through, dimmed), a fabric neck guard behind (refs es4, es5, fr5, al3, al4)."""
    f = FORCES[sp['force']]
    hc, dk = f['helmet'], B.dk(f['helmet'], 0.72)
    hw, hh = sp.get('hw', 68) * 1.06, sp.get('hh', 92)
    p = fit(p, sp, view, hx, hy, hw, hh, HELMET_REACH)
    guard = B.dk(f['uniform'], 0.85)
    if view in ('back', 'three_back'):
        o = -0.18 * hw if view == 'three_back' else 0.0
        neck = [(hx - hw * 0.95, hy + hh * 0.1), (hx + hw * 0.95, hy + hh * 0.1), (hx + hw * 0.8, hy + hh * 1.45),
                (hx - hw * 0.8, hy + hh * 1.45)]
        p.poly(curve(neck, 2), guard, INK, 2.4)
        dome = [(hx - hw * 1.18, hy + hh * 0.22), (hx - hw * 1.2 + o, hy - hh * 0.5), (hx - hw * 0.8 + o, hy - hh * 1.12),
                (hx + o, hy - hh * 1.3), (hx + hw * 0.8 + o, hy - hh * 1.12), (hx + hw * 1.2 + o, hy - hh * 0.5),
                (hx + hw * 1.18, hy + hh * 0.22), (hx, hy + hh * 0.3)]
        p.poly(curve(dome, 4), hc, INK, 2.6)
        p.line([(hx - hw * 1.1, hy + hh * 0.05), (hx, hy + hh * 0.12), (hx + hw * 1.1, hy + hh * 0.05)], dk, 2.0)
        if view == 'three_back':                   # the visor's edge just shows past the far cheek
            p.line([(hx + hw * 1.12, hy - hh * 0.35), (hx + hw * 1.2, hy + hh * 0.7)], INK, 2.2)
        return
    if view == 'side':
        neck = [(hx - hw * 1.45, hy + hh * 0.15), (hx - hw * 1.4, hy + hh * 1.5), (hx - hw * 0.6, hy + hh * 1.35),
                (hx - hw * 0.45, hy + hh * 0.3)]
        p.poly(curve(neck, 2), guard, INK, 2.4)
        dome = [(hx + hw * 1.02, hy - hh * 0.42), (hx + hw * 0.85, hy - hh * 1.02), (hx - hw * 0.1, hy - hh * 1.32),
                (hx - hw * 1.2, hy - hh * 1.0), (hx - hw * 1.58, hy - hh * 0.2), (hx - hw * 1.5, hy + hh * 0.28),
                (hx - hw * 0.5, hy + hh * 0.3), (hx + hw * 0.1, hy - hh * 0.05), (hx + hw * 0.5, hy - hh * 0.4)]
        p.poly(curve(dome, 4), hc, INK, 2.6)
        p.line([(hx - hw * 1.48, hy + hh * 0.1), (hx - hw * 0.5, hy + hh * 0.12), (hx + hw * 0.2, hy - hh * 0.2)], dk, 2.0)
        vis = [(hx + hw * 0.25, hy - hh * 0.45), (hx + hw * 1.1, hy - hh * 0.48), (hx + hw * 1.45, hy - hh * 0.2),
               (hx + hw * 1.5, hy + hh * 0.5), (hx + hw * 1.25, hy + hh * 1.12), (hx + hw * 0.55, hy + hh * 1.12),
               (hx + hw * 0.3, hy + hh * 0.2)]
        vc = curve(vis, 3)
        glass(p, vc, VISOR, 120, INK, 2.2)
        p.line([(hx + hw * 1.3, hy - hh * 0.25), (hx + hw * 1.0, hy + hh * 0.6)], (236, 242, 248), 2.6)   # the glint
        p.line([(hx + hw * 0.25, hy - hh * 0.45), (hx + hw * 1.15, hy - hh * 0.5)], dk, 4.0)           # the hinge rim
        p.ell(hx + hw * 0.32, hy - hh * 0.3, 7, 7, dk, INK, 1.4)
        return
    three = view == 'three'
    fx = hx + (0.32 * hw if three else 0.0)
    if three:
        dome = [(hx - hw * 1.22, hy + hh * 0.22), (hx - hw * 1.3, hy - hh * 0.45), (hx - hw * 0.9, hy - hh * 1.12),
                (hx + hw * 0.1, hy - hh * 1.32), (hx + hw * 0.95, hy - hh * 1.0), (hx + hw * 1.15, hy - hh * 0.35),
                (hx + hw * 1.1, hy + hh * 0.15), (hx, hy + hh * 0.2)]
        vis = [(fx - hw * 0.95, hy - hh * 0.46), (fx + hw * 0.88, hy - hh * 0.5), (fx + hw * 0.98, hy + hh * 0.3),
               (fx + hw * 0.78, hy + hh * 1.08), (fx - hw * 0.1, hy + hh * 1.16), (fx - hw * 0.85, hy + hh * 0.95),
               (fx - hw * 1.0, hy + hh * 0.2)]
    else:
        dome = [(hx - hw * 1.18, hy + hh * 0.22), (hx - hw * 1.22, hy - hh * 0.5), (hx - hw * 0.82, hy - hh * 1.14),
                (hx, hy - hh * 1.32), (hx + hw * 0.82, hy - hh * 1.14), (hx + hw * 1.22, hy - hh * 0.5),
                (hx + hw * 1.18, hy + hh * 0.22), (hx, hy + hh * 0.2)]
        vis = [(hx - hw * 1.06, hy - hh * 0.46), (hx + hw * 1.06, hy - hh * 0.46), (hx + hw * 1.08, hy + hh * 0.3),
               (hx + hw * 0.8, hy + hh * 1.06), (hx, hy + hh * 1.16), (hx - hw * 0.8, hy + hh * 1.06),
               (hx - hw * 1.08, hy + hh * 0.3)]
    p.poly(curve(dome, 4), hc, INK, 2.6)
    glass(p, curve(vis, 3), VISOR, 120, INK, 2.2)
    p.line([(fx + hw * 0.62, hy - hh * 0.3), (fx + hw * 0.2, hy + hh * 0.75)], (236, 242, 248), 2.6)   # the glint
    p.line([vis[0], vis[1]], dk, 4.5)                                                               # the hinge rim
    for x in ((hx + hw * 1.06,) if three else (hx - hw * 1.08, hx + hw * 1.08)):
        p.ell(x, hy - hh * 0.32, 7, 7, dk, INK, 1.4)


def armour(p, view, sp):
    """Chest and back plates over the uniform, and the belt (ref de2, es4, al4)."""
    f = FORCES[sp['force']]
    a = f['armour']
    sw = sp.get('shoulders', 170)
    if view in ('front', 'back'):
        plate = [(-sw + 40, 40), (sw - 40, 40), (sw - 34, 300), (sw - 50, 340), (-sw + 50, 340), (-sw + 34, 300)]
        p.poly(plate, a, INK, 2.2)
        p.line([(-sw + 50, 190), (sw - 50, 190)], B.dk(a, 0.75), 1.8)
        if view == 'back':                          # the force's word across the back plate (a light band at this size)
            p.poly([(-sw + 60, 220), (sw - 60, 220), (sw - 60, 270), (-sw + 60, 270)], (214, 210, 196), None)
    elif view in ('three', 'three_back'):
        sg = 1 if view == 'three' else -1
        plate = [(-sw * 0.55, 40), (sw * 0.75, 40), (sw * 0.8, 300), (sw * 0.7, 340), (-sw * 0.5, 340), (-sw * 0.6, 300)]
        plate = [(x * sg, y) for x, y in plate]
        p.poly(plate, a, INK, 2.2)
    else:
        p.poly([(-70, 46), (40, 40), (78, 120), (80, 320), (-80, 330), (-92, 120)], a, INK, 2.2)
    belt = 400
    p.poly([(-sw + 30, belt), (sw - 30, belt), (sw - 30, belt + 30), (-sw + 30, belt + 30)] if view != 'side'
           else [(-80, belt), (80, belt), (80, belt + 30), (-80, belt + 30)], (22, 22, 24), INK, 1.6)


_ARM = V.arm


def _arm(p, j2, side, sp, shape=None):
    """The arm, then (Albania) the red badge on the upper arm (ref al4), on the outside of the near arm."""
    _ARM(p, j2, side, sp, shape)
    badge = sp.get('force') and FORCES[sp['force']]['badge']
    if badge:
        sh, el = j2['sh' + side], j2['el' + side]
        if math.hypot(el[0] - sh[0], el[1] - sh[1]) > 80:
            c = (sh[0] + (el[0] - sh[0]) * 0.32, sh[1] + (el[1] - sh[1]) * 0.32)
            p.ell(c[0], c[1], 24, 30, badge, INK, 1.6)


V.arm = _arm


def shield(j, sp, centre=(-30.0, 330.0, 175.0), tilt=0.0, turn=0.0):
    """The long clear shield (about 0.6 x 1.2 m) held upright in front by the left hand; its label band across the
    top third (es5: "Policia Mossos d'Esquadra"; al3: POLICIA). tilt leans its top forward (+) or back; turn swings it
    about upright (degrees). Drawn after the arms: the body and arms show dimmed through it; from behind, under him."""
    f = FORCES[sp['force']]
    w, h = 0.6 * U / 2, 1.2 * U / 2
    cx, cy, cz = centre
    t, r = math.radians(tilt), math.radians(turn)

    def pt(u, v):                                   # u across (-1..1), v down (-1..1)
        x, y, z = u * w, v * h, 0.0
        y, z = y * math.cos(t), z - v * h * math.sin(t)
        x, z = x * math.cos(r) + z * math.sin(r), -x * math.sin(r) + z * math.cos(r)
        return (cx + x, cy + y, cz + z)

    def draw(p, j2, first=False):
        yaw = j2['yaw']
        if yaw > 100 and not first:
            return
        q = lambda u, v: P3(dict(j, _yaw=yaw), pt(u, v))           # noqa: E731
        edge = abs(math.sin(math.radians(yaw) + r)) > 0.97          # side on: the shield is a thin slab
        if edge:
            a, b = q(0, -1), q(0, 1)
            nx = 14
            p.poly([(a[0] - nx, a[1]), (a[0] + nx, a[1]), (b[0] + nx, b[1]), (b[0] - nx, b[1])], (176, 190, 204), INK, 2.2)
            return
        out = [q(-1, -1), q(1, -1), q(1, 1), q(-1, 1)]
        glass(p, out, SHIELD, 92, INK, 2.4)
        if yaw < 120:                               # the label: a thin white strip with the force's word in its colour
            band = [q(-0.86, -0.64), q(0.86, -0.64), q(0.86, -0.52), q(-0.86, -0.52)]   # (chat 6: a two-colour band
            p.poly(band, (246, 246, 242), f['label_c'], 1.4)                          # read as a flag stripe)
            px = [p.cam.P(*a) for a in band]
            xs, ys = [a[0] for a in px], [a[1] for a in px]
            bw, bh = max(xs) - min(xs), max(ys) - min(ys)
            if bw > 30:
                fs = max(6, int(min(bh * 0.8, bw / (0.62 * len(f['label']) + 1))))
                fnt = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), fs)
                cxy = p.cam.P(*q(0, -0.58))
                ImageDraw.Draw(p.img).text(cxy, f['label'], font=fnt, fill=f['label_c'], anchor='mm')
        g0, g1 = q(-0.55, -0.85), q(-0.15, 0.6)
        p.line([g0, g1], (248, 250, 252), 3.0)      # one glint
    def rear(p, j2, view):                         # from behind it is beyond his whole body, legs too: drawn first
        if view in ('back', 'three_back'):          # (chat 6: drawn after the legs, it lay over them)
            draw(p, j2, True)

    j.setdefault('pre', []).append(rear)
    draw.rear_under = True
    return draw


def baton(j, sp, side='R', dirn=(0.0, 0.55, 0.85), length=0.55):
    """A short black baton from the fist (dirn: which way it points, body frame); the fist drawn over its butt."""
    def draw(p, j2):
        jj = dict(j, _yaw=j2['yaw'])
        el, wr = j['el' + side], j['wr' + side]
        d = np.subtract(wr, el)
        hc = np.add(wr, d / (np.linalg.norm(d) or 1) * 12)
        u = np.asarray(dirn, float)
        u = u / (np.linalg.norm(u) or 1)
        a, b = P3(jj, tuple(hc - u * 30)), P3(jj, tuple(hc + u * length * U))
        p.line([a, b], INK, 17)
        p.line([a, b], (36, 36, 40), 11)
        c = P3(jj, tuple(hc))
        p.ell(c[0], c[1], 26, 26, sp.get('glove', sp['skin']), INK, 2.4)
    return draw


# ------------------------------------------------------------------------------------------------ the rioter
HOOD, HOOD_D, MASK = (30, 30, 34), (20, 20, 22), (16, 16, 18)


def rioter(who='rioter'):
    sp = dict(CAST[who])
    sp['glove'] = (24, 24, 26)                      # black gloves (ref de4: one orange, most dark)
    return sp


def hood(p, view, sp, hx, hy):
    """Hood up over a black face mask, only a band round the eyes showing (refs de1, de4, es3, fr4). From behind, the
    hood's rounded point and its centre seam."""
    hw, hh = sp.get('hw', 66), sp.get('hh', 94)
    p = fit(p, sp, view, hx, hy, hw, hh, HOOD_REACH)
    if view in ('back', 'three_back'):
        o = -0.12 * hw if view == 'three_back' else 0.0
        out = [(hx - hw * 1.25, hy + hh * 1.55), (hx - hw * 1.32, hy + hh * 0.2), (hx - hw * 1.05 + o, hy - hh * 0.95),
               (hx + o, hy - hh * 1.32), (hx + hw * 1.05 + o, hy - hh * 0.95), (hx + hw * 1.32, hy + hh * 0.2),
               (hx + hw * 1.25, hy + hh * 1.55)]
        p.poly(curve(out, 4), HOOD, INK, 2.6)
        p.line(curve([(hx + o, hy - hh * 1.3), (hx + o * 0.6, hy), (hx, hy + hh * 1.3)], 4)[:-4], HOOD_D, 2.2)
        return
    if view == 'side':
        out = [(hx + hw * 0.9, hy - hh * 0.72), (hx + hw * 0.2, hy - hh * 1.3), (hx - hw * 0.9, hy - hh * 1.22),
               (hx - hw * 1.62, hy - hh * 0.55), (hx - hw * 1.5, hy + hh * 0.5), (hx - hw * 1.1, hy + hh * 1.6),
               (hx + hw * 0.5, hy + hh * 1.6), (hx + hw * 0.55, hy + hh * 0.9), (hx + hw * 0.35, hy - hh * 0.2),
               (hx + hw * 0.6, hy - hh * 0.55)]
        mask = [(hx + hw * 0.3, hy + hh * 0.12), (hx + hw * 1.3, hy + hh * 0.06), (hx + hw * 1.32, hy + hh * 0.42),
                (hx + hw * 1.12, hy + hh * 1.05), (hx + hw * 0.6, hy + hh * 1.2), (hx + hw * 0.3, hy + hh * 0.9)]
        p.poly(curve(mask, 3), MASK, INK, 2.2)
        p.poly(curve(out, 4), HOOD, INK, 2.6)
        p.line(curve([(hx + hw * 0.62, hy - hh * 0.6), (hx + hw * 0.4, hy + hh * 0.3), (hx + hw * 0.5, hy + hh * 1.2)],
                     3)[:-3], HOOD_D, 2.2)
        return
    three = view == 'three'
    fx = hx + (0.34 * hw if three else 0.0)
    if three:
        out = [(hx - hw * 1.3, hy + hh * 1.55), (hx - hw * 1.42, hy + hh * 0.2), (hx - hw * 1.12, hy - hh * 0.95),
               (hx - hw * 0.1, hy - hh * 1.32), (hx + hw * 0.9, hy - hh * 1.0), (hx + hw * 1.22, hy - hh * 0.1),
               (hx + hw * 1.18, hy + hh * 1.55)]
        hole = oval(fx + hw * 0.08, hy + hh * 0.12, hw * 0.78, hh * 0.98, 30)
    else:
        out = [(hx - hw * 1.28, hy + hh * 1.55), (hx - hw * 1.36, hy + hh * 0.2), (hx - hw * 1.06, hy - hh * 0.98),
               (hx, hy - hh * 1.34), (hx + hw * 1.06, hy - hh * 0.98), (hx + hw * 1.36, hy + hh * 0.2),
               (hx + hw * 1.28, hy + hh * 1.55)]
        hole = oval(hx, hy + hh * 0.12, hw * 0.84, hh * 1.0, 30)
    mx = fx + (hw * 0.08 if three else 0.0)
    mask = [(mx - hw * 0.86, hy + hh * 0.1), (mx - hw * 0.3, hy + hh * 0.02), (mx, hy + hh * 0.08),
            (mx + hw * 0.3, hy + hh * 0.02), (mx + hw * 0.86, hy + hh * 0.1), (mx + hw * 0.8, hy + hh * 1.2),
            (mx - hw * 0.8, hy + hh * 1.2)]
    p.poly(curve(mask, 3), MASK, None)
    ring = curve(out, 4)
    p.poly(_holed(ring, hole[::-1]), HOOD, None)
    p.poly(ring, None, INK, 2.6)
    p.poly(hole, None, INK, 2.2)
    p.line([(mx - hw * 0.8, hy + hh * 0.1), (mx, hy + hh * 0.06), (mx + hw * 0.8, hy + hh * 0.1)], INK, 2.0)


def hoodie(p, view, sp):
    """The hoodie's front pocket and drawstrings (front); the pocket's edge from the side."""
    sw = sp.get('shoulders', 156)
    if view in ('front', 'three'):
        o = 20 if view == 'three' else 0
        p.poly([(-sw * 0.62 + o, 320), (sw * 0.62 + o, 320), (sw * 0.75 + o, 440), (-sw * 0.75 + o, 440)], HOOD_D, INK, 1.8)
        for sg in (-1, 1):
            p.line([(sg * 26 + o, 6), (sg * 30 + o, 120)], (200, 200, 196), 3.0)
    elif view == 'side':
        p.line([(40, 320), (70, 440)], INK, 1.8)


def dress_rioter(j):
    j['head_props'] = [hood] + j.get('head_props', [])
    j['body_props'] = [hoodie] + j.get('body_props', [])
    return j


def dress_officer(j):
    j['head_props'] = [riot_helmet] + j.get('head_props', [])
    j['body_props'] = [armour] + j.get('body_props', [])
    return j


# ------------------------------------------------------------------------------------------------ the marchers
def marcher(i, tier='t1', s=0):
    sp = PK.crowd_person(CROWD, i, s, tier)
    PK.install({'m': sp})
    return sp


# ------------------------------------------------------------------------------------------------ props
def _hand_c(j, side):
    el, wr = np.asarray(j['el' + side]), np.asarray(j['wr' + side])
    d = wr - el
    return wr + d / (np.linalg.norm(d) or 1) * 12


def stone(j, side='R', r=26):
    def draw(p, j2):
        c = P3(dict(j, _yaw=j2['yaw']), tuple(_hand_c(j, side) + (0, -18, 0)))
        p.poly(curve([(c[0] - r, c[1]), (c[0] - r * 0.4, c[1] - r * 0.9), (c[0] + r, c[1] - r * 0.6),
                      (c[0] + r * 0.8, c[1] + r * 0.5), (c[0] - r * 0.3, c[1] + r * 0.8)], 2), (150, 146, 138), INK, 2.0)
    return draw


def bottle(j, side='R', lit=True):
    """A Molotov: a green bottle, a rag at its neck, a small flame (house fire colours)."""
    def draw(p, j2):
        jj = dict(j, _yaw=j2['yaw'])
        c = _hand_c(j, side)
        a, b = P3(jj, tuple(c + (0, 40, 0))), P3(jj, tuple(c + (0, -110, -20)))
        p.line([a, b], INK, 30)
        p.line([a, b], (60, 110, 60), 24)
        if lit:
            x, y = b
            p.poly(curve([(x - 18, y), (x - 8, y - 46), (x + 4, y - 70), (x + 14, y - 40), (x + 18, y)], 2),
                   (250, 150, 40), INK, 1.6)
            p.poly(curve([(x - 8, y - 4), (x, y - 36), (x + 8, y - 4)], 2), (255, 222, 90), None)
    return draw


def road_sign(j, hands=('R', 'L'), dirn=(0.0, -0.75, -0.66), pole=1.1):
    """The give-way sign on its ripped-up pole (ref de4): grey pole from the hands, the white triangle with its thick red
    border on the far end, its point towards the hands (point-down as it stood). The triangle's plane holds the pole
    and lies across the body's front-back plane, so the side view (the swing's shot) sees it full on, the front view
    edge on (chat 6: it was edge-on in the side view)."""
    def draw(p, j2):
        jj = dict(j, _yaw=j2['yaw'])
        c = (_hand_c(j, hands[0]) + _hand_c(j, hands[1])) / 2
        u = np.asarray(dirn, float)
        u /= np.linalg.norm(u)
        base, top = c - u * 60, c + u * pole * U
        side = 0.7 * U
        w = np.cross(u, (1.0, 0.0, 0.0))
        w = w / (np.linalg.norm(w) or 1)
        tri = [top - u * side * 0.577, top + u * side * 0.289 + w * side / 2, top + u * side * 0.289 - w * side / 2]
        tri2 = [P3(jj, tuple(q)) for q in tri]
        a, b = P3(jj, tuple(base)), P3(jj, tuple(top))
        p.line([a, b], INK, 15)
        p.line([a, b], (150, 152, 156), 9)
        cx = sum(q[0] for q in tri2) / 3
        cy = sum(q[1] for q in tri2) / 3
        if abs(V.project(tuple(np.cross(u, w)), j2['yaw'])[1]) < 0.2 and \
                math.hypot(tri2[1][0] - tri2[2][0], tri2[1][1] - tri2[2][1]) < 40:
            p.line([tri2[0], ((tri2[1][0] + tri2[2][0]) / 2, (tri2[1][1] + tri2[2][1]) / 2)], INK, 12)
            return                                  # edge on: a thin red slab
        p.poly(tri2, (200, 28, 36), INK, 2.4)
        inner = [(cx + (q[0] - cx) * 0.55, cy + (q[1] - cy) * 0.55) for q in tri2]
        p.poly(inner, (246, 246, 242), None)
    return draw


def keys(j, side='R'):
    """A bunch of house keys held up (ref es6): two small grey keys and the ring above the fist, a glint."""
    def draw(p, j2):
        c = P3(dict(j, _yaw=j2['yaw']), tuple(_hand_c(j, side)))
        x, y = c
        # drawn about twice true size so a bunch reads at crowd scale (chat 14: at true size they vanished)
        p.ell(x, y - 46, 22, 22, None, INK, 9)
        p.ell(x, y - 46, 22, 22, None, (214, 216, 220), 5)
        for dx, ang, col in ((-16, -0.55, (214, 190, 96)), (2, 0.05, (200, 204, 210)), (16, 0.6, (214, 190, 96))):
            bx, by = x + dx, y - 60
            ex, ey = bx + 80 * math.sin(ang), by - 80 * math.cos(ang)
            p.line([(bx, by), (ex, ey)], INK, 18)
            p.line([(bx, by), (ex, ey)], col, 11)
        p.ell(x + 8, y - 120, 10, 10, (255, 252, 230), None)
    return draw


def placard(j, text='NEIN!', hands=('R', 'L'), board=(250, 246, 232), w=0.6, h=0.42, pole=0.7):
    """A placard on a stick held up in both hands, printed both sides; the hands grip the stick below the board."""
    def draw(p, j2):
        jj = dict(j, _yaw=j2['yaw'])
        c = (_hand_c(j, hands[0]) + _hand_c(j, hands[1])) / 2
        top = c + (0, -pole * U, 0)
        a, b = P3(jj, tuple(c + (0, 40, 0))), P3(jj, tuple(top))
        p.line([a, b], INK, 13)
        p.line([a, b], (170, 130, 80), 8)
        q = [P3(jj, tuple(top + d)) for d in ((-w * U / 2, -h * U, 0), (w * U / 2, -h * U, 0), (w * U / 2, 0, 0),
                                              (-w * U / 2, 0, 0))]
        p.poly(q, board, INK, 2.4)                  # printed both sides (the T2 crowd is seen from behind)
        if text:
            x0, y0 = p.cam.P(*q[0])
            x1, y1 = p.cam.P(*q[2])
            fs = max(6, int(abs(y1 - y0) * 0.42))
            try:
                fnt = ImageFont.truetype(os.path.join(HERE, 'fonts', 'Anton-Regular.ttf'), fs)
            except OSError:
                fnt = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), fs)
            ImageDraw.Draw(p.img).text(((x0 + x1) / 2, (y0 + y1) / 2), text, font=fnt, fill=(30, 28, 30), anchor='mm')
    draw.held = True
    return draw


def flag(j, kind='catalan', side='R', pole=1.6, wave=0.0):
    """A flag on a pole held up in one hand: Catalan senyera (es2), UGT red (es2), tricolour (T3), Albania (al5)."""
    def draw(p, j2):
        jj = dict(j, _yaw=j2['yaw'])
        c = _hand_c(j, side)
        top = c + (0, -pole * U, 0)
        a, b = P3(jj, tuple(c + (0, 60, 0))), P3(jj, tuple(top))
        p.line([a, b], INK, 11)
        p.line([a, b], (120, 110, 100), 6)
        fw, fh = 0.9 * U, 0.6 * U
        x, y = b
        sx = 1 if (j2['yaw'] >= 0) else -1
        pts = [(x, y), (x + sx * fw * 0.5, y + 14 * math.sin(wave)), (x + sx * fw, y + 6),
               (x + sx * fw, y + fh + 6), (x + sx * fw * 0.5, y + fh + 14 * math.sin(wave)), (x, y + fh)]
        if kind == 'catalan':
            p.poly(pts, (250, 214, 40), None)
            for k in range(4):
                yy = y + fh * (1 + 2 * k) / 9
                p.poly([(x, yy), (x + sx * fw, yy + 6), (x + sx * fw, yy + 6 + fh / 9), (x, yy + fh / 9)],
                       (200, 30, 36), None)
        elif kind == 'tricolour':
            for k, col in enumerate(((30, 50, 140), (246, 246, 242), (210, 36, 44))):
                x0, x1 = x + sx * fw * k / 3, x + sx * fw * (k + 1) / 3
                p.poly([(x0, y + 4 * k / 3), (x1, y + 4 * (k + 1) / 3), (x1, y + fh + 4 * (k + 1) / 3),
                        (x0, y + fh + 4 * k / 3)], col, None)
        elif kind == 'albania':
            p.poly(pts, (206, 26, 36), None)
            ex, ey = x + sx * fw * 0.5, y + fh * 0.5
            p.poly(curve([(ex - 40, ey - 30), (ex, ey - 50), (ex + 40, ey - 30), (ex + 30, ey + 30), (ex, ey + 50),
                          (ex - 30, ey + 30)], 2), (20, 18, 20), None)
        else:                                       # 'ugt': red with a white bar
            p.poly(pts, (196, 28, 36), None)
            p.poly([(x + sx * 20, y + fh * 0.4), (x + sx * (fw - 20), y + fh * 0.4), (x + sx * (fw - 20), y + fh * 0.6),
                    (x + sx * 20, y + fh * 0.6)], (246, 240, 230), None)
        p.poly(pts, None, INK, 2.2)
    return draw


def phone(j, side='R'):
    """A phone held up filming, portrait, its screen facing the holder (Sam's note 1): from in front we see its dark
    back and the camera lens; from behind, the lit screen; side on, a thin slab. Held with grips.held (drawn in front
    of the face when it is in front of the face)."""
    def draw(p, j2):
        c = P3(dict(j, _yaw=j2['yaw']), tuple(_hand_c(j, side)))
        k = abs(math.cos(math.radians(j2['yaw'])))
        hw = max(5.0, 25.0 * k)
        top, bot = c[1] - 92, c[1] + 12
        box = [(c[0] - hw, top), (c[0] + hw, top), (c[0] + hw, bot), (c[0] - hw, bot)]
        if j2['yaw'] > 95:                          # from behind: the lit screen, a red record dot
            p.poly(box, (30, 32, 38), INK, 2.0)
            if hw > 10:
                p.poly([(c[0] - hw + 4, top + 6), (c[0] + hw - 4, top + 6), (c[0] + hw - 4, bot - 6),
                        (c[0] - hw + 4, bot - 6)], (196, 226, 255), None)
                p.ell(c[0], top + 18, 5, 5, (220, 40, 40), None)
        else:                                       # from in front: the dark back, the lens at its top corner
            p.poly(box, (52, 56, 66), INK, 2.0)
            if hw > 10:
                p.ell(c[0] - hw * 0.45, top + 16, 8, 8, (20, 20, 24), (120, 124, 130), 1.6)
    return draw


def peace(j, side='L', thumb=False):
    """Two fingers up in a V over the fist (the selfie's peace sign), or a thumb up (checking the photo). A gloved
    hand: black fingers with a light edge, drawn thick enough to read at phone size."""
    def draw(p, j2):
        c = P3(dict(j, _yaw=j2['yaw']), tuple(_hand_c(j, side)))
        x, y = c
        p.ell(x, y, 26, 24, (24, 24, 26), INK, 2.4)
        if thumb:
            p.poly([(x - 34, y - 22), (x + 30, y - 22), (x + 34, y + 26), (x - 30, y + 28)], (24, 24, 26), INK, 2.4)
            for k in range(3):                     # the curled fingers' knuckles, facing us
                p.line([(x - 28, y - 8 + k * 14), (x + 6, y - 8 + k * 14)], (90, 90, 96), 2.0)
            p.ell(x + 10, y - 44, 13, 26, (24, 24, 26), INK, 2.2)   # the thumb, short and thick, off the top
            return
        fingers = [((x - 8, y - 16), (x - 30, y - 82)), ((x + 8, y - 16), (x + 26, y - 82))]
        for a, b in fingers:
            p.line([a, b], INK, 22)
            p.line([a, b], (24, 24, 26), 15)
    draw.side = side
    return draw


# ------------------------------------------------------------------------------------------------ poses
def pose(sp, name, u=0.0, t=0.0, force=None):
    """One of the cast's poses (body frame, before lean): u is how far through a move (0-1), t a gait's time."""
    sw = sp.get('shoulders', 160)
    if name == 'run':
        j = moves.gait(sp, t, 'sprint')
    elif name == 'run_sign':                        # running carrying the sign low (T2 runners)
        j = moves.gait(sp, t, 'run')
    elif name.startswith('carry') or name == 'push':  # round 1: T2 looters jog with stock; T3 shove the car
        j = moves.gait(sp, t, 'walk' if name == 'push' else 'brisk')   # chat 29: laden, a brisk walk (run: 9 m/s feet)
    else:
        j = V.standing(sp)
    if name == 'line':                              # in the shield line: shield up in front, baton down by the side
        V.arm_to(j, 'L', (-30.0, 250.0, 160.0), 'down')
        V.arm_to(j, 'R', (sw - 6, 420.0, 70.0), 'out')
        j['props'] = [baton(j, sp, 'R', (0.0, 0.6, 0.8)), shield(j, sp)]
    elif name == 'baton_up':                        # baton raised over the shoulder, shield forward
        V.arm_to(j, 'L', (-30.0, 250.0, 170.0), 'down')
        V.arm_to(j, 'R', (j['shR'][0] + 40, -300.0, -60.0), 'out')   # clear above the helmet (chat 6: hand on it)
        j['props'] = [baton(j, sp, 'R', (-0.1, -0.5, -0.86)), shield(j, sp, tilt=-6)]
    elif name == 'pushed':                          # driven back (T4): leaning back, shield knocked askew
        j['lean'] = -9
        j['footR'] = (60, V.ANKLE_Y, -120.0)
        j['footL'] = (-60, V.ANKLE_Y, 90.0)
        V.arm_to(j, 'L', (-60.0, 200.0, 170.0), 'down')
        V.arm_to(j, 'R', (sw + 60, 120.0, 80.0), 'out')
        j['props'] = [baton(j, sp, 'R', (0.3, -0.4, 0.86)), shield(j, sp, centre=(-50.0, 300.0, 175.0), tilt=-14,
                                                                     turn=18)]
    elif name in ('throw', 'molotov'):              # u 0: wound up (arm back high, weight back); 1: thrown through
        e = moves.ease(u)
        j['lean'] = -6 + 18 * e
        j['footL'] = (-60, V.ANKLE_Y, 140.0)
        j['footR'] = (60, V.ANKLE_Y - 30 * e, -130.0)
        j['toeR'] = 14 * e
        back, through = np.array((sw + 70, -40.0, -300.0)), np.array((40.0, 250.0, 260.0))
        V.arm_to(j, 'R', tuple(back + (through - back) * e), 'out' if e < 0.5 else 'down')
        V.arm_to(j, 'L', (-sw + 40 - 140 * e, 120.0 + 200 * e, 260.0 - 160 * e), 'down')
        if e < 0.6:                                 # the stone in the throwing hand until it leaves
            grips.held(j, 'R', sp, stone(j, 'R') if name == 'throw' else bottle(j, 'R'))
    elif name == 'swing':                           # the road sign: wound up over the right shoulder -> swung down
        e = moves.ease(u)
        j['lean'] = -4 + 16 * e
        j['footL'] = (-70, V.ANKLE_Y, 150.0)
        j['footR'] = (70, V.ANKLE_Y, -110.0)
        hand = np.array((sw + 40, 20.0, -170.0)) * (1 - e) + np.array((-20.0, 300.0, 200.0)) * e
        V.arm_to(j, 'R', tuple(hand + (0, 0, 10)), 'out')
        V.arm_to(j, 'L', tuple(hand + (30, 60, 40)), 'down')   # on the pole's lower end, beside the body (chat 8: was pushed into its sleeve)
        ang = math.radians(-60 + 150 * e)               # pole angle from straight up, swinging forward
        j['props'] = [road_sign(j, dirn=(0.0, -math.cos(ang), math.sin(ang)))]
        j['grip'] = ('L', 'R')                      # both fists over the pole
    elif name == 'haul':                            # hauling the shutter up (T2): both hands high, leaning back
        j['lean'] = -8
        V.arm_to(j, 'R', (60.0, -330.0, 150.0), 'down')
        V.arm_to(j, 'L', (-60.0, -310.0, 150.0), 'down')
    elif name == 'carry_front':                     # round 1 (T2): a TV or a tower of boxes held out in front at chest
        V.arm_to(j, 'R', (j['shR'][0] + 10, 150.0, 260.0), 'down')
        V.arm_to(j, 'L', (j['shL'][0] - 10, 150.0, 260.0), 'down')
    elif name == 'carry_up':                        # round 1 (T2): the mannequin held up flat over the head, both hands
        V.arm_to(j, 'R', (j['shR'][0] - 20, -430.0, 40.0), 'out')
        V.arm_to(j, 'L', (j['shL'][0] + 20, -430.0, 40.0), 'out')
    elif name == 'push':                            # round 1 (T3): shoving the car, leaning in, arms out straight
        j['lean'] = 16
        V.arm_to(j, 'R', (j['shR'][0] - 20, 60.0, 360.0), 'down')
        V.arm_to(j, 'L', (j['shL'][0] + 20, 60.0, 360.0), 'down')
    elif name == 'march':                           # walking away from us (T1, T3)
        j = moves.gait(sp, t, 'walk')
    # Held up high: the hand is beside the head or clearly in front of the face, never over or behind it (Sam's
    # note 1; chat 6: keys, placard, phone and flag all had the arm behind the head)
    elif name == 'keys':                            # keys raised high beside the head (T1, ref es6)
        V.arm_to(j, 'R', (j['shR'][0] - 10, -470.0, 70.0), 'out')
        j['props'] = [keys(j)]
        j['grip'] = ('R',)
    elif name == 'placard':                         # both hands on the stick below the board, out in front, to his right
        x = j['shR'][0] * 0.75
        V.arm_to(j, 'R', (x, -60.0, 230.0), 'down')
        V.arm_to(j, 'L', (x, 70.0, 230.0), 'down')
        j['props'] = [placard(j)]
        j['grip'] = ('L', 'R')
    elif name == 'phone':                           # filming: arm forward, the phone at eye height in front of the face
        V.arm_to(j, 'R', (j['shR'][0] * 0.65, -175.0, 270.0), 'down')
        grips.held(j, 'R', sp, phone(j))
    elif name == 'selfie':                          # T4 gag b: back to the helicopter, phone up at arm's length in
        e = moves.ease(u)                           # front of him (we see its back), the other hand a peace sign by
        V.arm_to(j, 'R', (j['shR'][0] + 120, -300.0, 260.0), 'out')   # out clear of the hood (hunt 1)   # his head; u: the thumbs-up after (0..1)
        grips.held(j, 'R', sp, phone(j))
        V.arm_to(j, 'L', (j['shL'][0] - 60, -250.0 + 120 * e, 90.0), 'out')
        j['props'] = j.get('props', []) + [peace(j, 'L', thumb=e > 0.5)]
        j['head_roll'] = 10 * (1 - e)               # the selfie head tilt
    elif name == 'cheer':                           # T4 (round 1): a fist punched up high beside the head
        V.arm_to(j, 'R', (j['shR'][0] + 30, -440.0 + 60 * u, 60.0), 'out')
        V.arm_to(j, 'L', (j['shL'][0] - 40, -300.0 + 200 * u, 80.0), 'out')
    elif name == 'flag':                            # the pole held up beside him, the fist level with his brow
        V.arm_to(j, 'R', (j['shR'][0] + 40, -230.0, 70.0), 'out')
        j['props'] = [flag(j, force or 'catalan')]
        j['grip'] = ('R',)
    return j


# ------------------------------------------------------------------------------------------------ the new cast's dress
# Round 1 (chat 22): what the tourists, the granny and the seller wear on top of the people kit's bodies. Each is a
# head prop (p, view, sp, hx, hy) or a body prop (p, view, sp) in the torso's frame (neck base 0, hips 450, soles
# 928); TOURIST_DRESS names who wears what and draw() puts them on. Sized from head_box (the head as really drawn).
CAP, CAP_D = (200, 44, 52), (150, 30, 38)                 # his red baseball cap
VISOR_C, SHADES = (250, 250, 246), (30, 30, 34)
SCARF, SCARF_D = (206, 62, 58), (150, 40, 38)             # chat 27 (notes hunt 2: plum read as purple hair): a red babushka scarf
SCARF_DOT = (246, 234, 206)                                # its cream polka dots
FLAT, FLAT_D = (96, 90, 78), (70, 64, 56)                 # the seller's tweed flat cap
APRON, APRON_D = (236, 232, 222), (190, 184, 170)
BUMBAG, CAMERA = (40, 44, 52), (34, 34, 38)
TOTE = (232, 222, 196)
CARDIGAN, CARDIGAN_D = (204, 184, 152), (150, 132, 104)   # oatmeal: her sleeve stands off the dark dress (hunt 1)


def _side(view):
    return view in ('side',)


def baseball_cap(p, view, sp, hx, hy):
    """A red baseball cap: a crown over the top of the head, the peak out over the brow (front: a flat band below the
    crown; side: sticking forward)."""
    l, r, t = head_box(sp, view)
    hh = sp.get('hh', 94)
    top, brow = hy + t - 6, hy + t + 0.62 * hh
    if view == 'side':
        crown = [(hx + l + 6, brow + 6), (hx + l - 2, top + 0.45 * hh), (hx + (l + r) * 0.5 - 10, top - 2),
                 (hx + r - 6, top + 0.4 * hh), (hx + r, brow)]
        p.poly(curve(crown, 3), CAP, INK, 2.4)
        p.poly([(hx + r - 14, brow - 10), (hx + r + 62, brow + 4), (hx + r + 58, brow + 14), (hx + r - 10, brow + 8)],
               CAP_D, INK, 2.2)
        return
    if view in ('back', 'three_back'):
        crown = [(hx + l - 4, brow + 10), (hx + l - 4, top + 0.4 * hh), (hx, top - 4), (hx + r + 4, top + 0.4 * hh),
                 (hx + r + 4, brow + 10)]
        p.poly(curve(crown, 3), CAP, INK, 2.4)
        p.poly([(hx - 22, brow - 6), (hx + 22, brow - 6), (hx + 18, brow + 10), (hx - 18, brow + 10)], (240, 230, 220),
               INK, 1.6)                                  # the strap gap at the back
        return
    o = 0.2 * (r - l) if view == 'three' else 0.0
    top -= 0.25 * hh                                      # a tall round crown, the panels' seams showing (hunt 1: a
    crown = [(hx + l + 4, brow + 6), (hx + l + 2, top + 0.5 * hh), (hx + l + 0.2 * (r - l), top + 0.08 * hh),   # flat
             (hx + o * 0.4, top - 4), (hx + r - 0.2 * (r - l), top + 0.08 * hh), (hx + r - 2, top + 0.5 * hh),  # crown
             (hx + r - 4, brow + 6)]                                                                       # read as a beret)
    p.poly(curve(crown, 3), CAP, INK, 2.4)
    for k in (-0.28, 0.0, 0.28):                          # the crown's seams
        p.line(curve([(hx + o * 0.4, top), (hx + o * 0.4 + k * (r - l), top + 0.5 * hh),
                      (hx + o * 0.4 + k * 1.2 * (r - l), brow - 4)], 2), CAP_D, 2.0)
    p.ell(hx + o * 0.4, top + 2, 8, 6, CAP_D, INK, 1.2)                  # the button on top
    peak = [(hx + l + 4 + o, brow), (hx + r - 4 + o, brow), (hx + r + 14 + o, brow + 22), (hx + o, brow + 40),
            (hx + l - 14 + o, brow + 22)]
    p.poly(curve(peak, 2), CAP_D, INK, 2.2)


def sun_visor(p, view, sp, hx, hy):
    """A white sun visor (a band round the head, no crown, the hair showing over it) and sunglasses pushed up on the
    hair above it."""
    l, r, t = head_box(sp, view)
    hh = sp.get('hh', 94)
    band = hy - 1.0 * hh                                  # the top of the forehead, above the brows
    if view == 'side':
        p.poly([(hx + l + 30, band - 4), (hx + r, band - 10), (hx + r, band + 6), (hx + l + 30, band + 12)], VISOR_C,
               INK, 2.0)
        p.poly([(hx + r - 16, band - 4), (hx + r + 66, band + 10), (hx + r + 60, band + 22), (hx + r - 12, band + 14)],
               VISOR_C, INK, 2.0)
        p.ell(hx + r - 26, band - 26, 18, 10, SHADES, INK, 1.6)
        return
    if view in ('back', 'three_back'):
        p.poly([(hx + l - 2, band - 6), (hx + r + 2, band - 6), (hx + r + 2, band + 8), (hx + l - 2, band + 8)],
               VISOR_C, INK, 2.0)
        return
    o = 0.2 * (r - l) if view == 'three' else 0.0
    p.poly([(hx + l - 2, band - 8), (hx + r + 2, band - 8), (hx + r + 2, band + 8), (hx + l - 2, band + 8)], VISOR_C,
           INK, 2.0)
    peak = [(hx + l + 10 + o, band + 4), (hx + r - 10 + o, band + 4), (hx + r + 2 + o, band + 14), (hx + o, band + 20),
            (hx + l - 2 + o, band + 14)]
    p.poly(curve(peak, 2), VISOR_C, INK, 2.0)
    for sg in (-1, 1):                                    # the sunglasses pushed up on the hair, above the band
        p.ell(hx + o + sg * 0.3 * (r - l), band - 34, 0.18 * (r - l), 15, SHADES, INK, 1.8)
        p.line([(hx + o + sg * 0.48 * (r - l), band - 36), (hx + o + sg * 0.62 * (r - l), band - 20)], INK, 2.0)
    p.line([(hx + o - 0.12 * (r - l), band - 36), (hx + o + 0.12 * (r - l), band - 36)], INK, 3.0)


def headscarf(p, view, sp, hx, hy):
    """A plum headscarf over the hair, framing the face, tied under the chin (the knot shows in front)."""
    l, r, t = head_box(sp, view)
    hw, hh = sp.get('hw', 64), sp.get('hh', 90)
    top = hy - 1.62 * hh                                  # over the hair (the box top is the bun, which is off under it)
    if view == 'side':
        top = min(top, hy + t - 6)
        out = [(hx + 0.3 * hw, hy + 1.05 * hh), (hx + 0.42 * hw, hy + 0.2 * hh), (hx + 0.55 * hw, hy - 0.75 * hh),
               (hx + r - 0.1 * hw, hy - 0.95 * hh), (hx + 0.1 * hw, top), (hx + l - 4, top + 0.5 * hh),
               (hx + l - 14, hy + 0.5 * hh), (hx + l + 10, hy + 1.2 * hh), (hx - 0.1 * hw, hy + 1.2 * hh)]
        p.poly(curve(out, 3), SCARF, INK, 2.4)
        p.line(curve([(hx + l + 10, hy + 1.2 * hh), (hx + l - 4, hy + 1.55 * hh)], 1), SCARF_D, 9)   # the tail
        p.ell(hx + 0.3 * hw, hy + 1.12 * hh, 14, 11, SCARF_D, INK, 1.6)          # the knot under her chin
        for k in range(4):
            p.ell(hx - 0.2 * hw + k * 0.0, top + (0.35 + 0.3 * k) * hh, 6, 6, SCARF_DOT, None)
        return
    if view in ('back', 'three_back'):
        out = [(hx + l - 6, hy + 0.9 * hh), (hx + l - 8, top + 0.5 * hh), (hx, top - 4), (hx + r + 8, top + 0.5 * hh),
               (hx + r + 6, hy + 0.9 * hh), (hx + 0.4 * hw, hy + 1.45 * hh), (hx - 0.4 * hw, hy + 1.45 * hh)]
        p.poly(curve(out, 3), SCARF, INK, 2.4)
        return
    o = 0.2 * (r - l) if view == 'three' else 0.0
    out = [(hx + l - 8, hy + 0.85 * hh), (hx + l - 10, top + 0.5 * hh), (hx + o * 0.5, top - 6),
           (hx + r + 10, top + 0.5 * hh), (hx + r + 8, hy + 0.85 * hh), (hx + o + 0.3 * hw, hy + 1.2 * hh),
           (hx + o - 0.3 * hw, hy + 1.2 * hh)]
    hole = oval(hx + o, hy + 0.12 * hh, 0.8 * hw, 0.98 * hh, 30)
    ring = curve(out, 3)
    p.poly(_holed(ring, hole[::-1]), SCARF, None)
    p.poly(ring, None, INK, 2.4)
    p.poly(hole, None, INK, 2.0)
    for k in range(5):                                    # a little printed pattern: dots on the top
        p.ell(hx + o * 0.5 + (k - 2) * 0.35 * hw, top + 0.32 * hh + abs(k - 2) * 8, 6, 6, SCARF_DOT, None)
    kx, ky = hx + o, hy + 1.18 * hh                       # the knot under the chin
    p.ell(kx, ky, 16, 12, SCARF_D, INK, 1.8)
    p.poly([(kx - 6, ky + 6), (kx - 22, ky + 40), (kx - 4, ky + 34)], SCARF, INK, 1.6)
    p.poly([(kx + 6, ky + 6), (kx + 24, ky + 38), (kx + 6, ky + 32)], SCARF, INK, 1.6)


def flat_cap(p, view, sp, hx, hy):
    """A tweed flat cap: low and flat, the short peak over the brow."""
    l, r, t = head_box(sp, view)
    hh = sp.get('hh', 92)
    top, brow = hy + t - 4, hy + t + 0.55 * hh
    if view == 'side':
        cap = [(hx + l - 6, brow + 4), (hx + l - 4, top + 0.25 * hh), (hx, top), (hx + r + 4, top + 0.3 * hh),
               (hx + r + 40, brow - 2), (hx + r + 36, brow + 10), (hx + r - 10, brow + 8)]
        p.poly(curve(cap, 2), FLAT, INK, 2.4)
        return
    o = 0.2 * (r - l) if view == 'three' else 0.0
    cap = [(hx + l - 10, brow + 6), (hx + l - 6, top + 0.25 * hh), (hx + o * 0.4, top - 2), (hx + r + 6, top + 0.25 * hh),
           (hx + r + 10, brow + 6)]
    p.poly(curve(cap, 3), FLAT, INK, 2.4)
    for k in (-1, 0, 1):                                  # the tweed: a few flecks
        p.line([(hx + o * 0.4 + k * 30 - 6, top + 0.25 * hh), (hx + o * 0.4 + k * 30 + 6, top + 0.3 * hh)], FLAT_D, 2.0)
    if view not in ('back', 'three_back'):
        p.poly(curve([(hx + l + 4 + o, brow), (hx + r - 4 + o, brow), (hx + r + 2 + o, brow + 12), (hx + o, brow + 18),
                      (hx + l - 2 + o, brow + 12)], 2), FLAT_D, INK, 2.0)


def moustache(p, view, sp, hx, hy):
    """A thick dark moustache over the mouth."""
    if view in ('back', 'three_back'):
        return
    hw, hh = sp.get('hw', 72), sp.get('hh', 92)
    col = sp.get('hair_c', sp.get('brow_c', (40, 34, 30)))
    col = (40, 34, 30) if not isinstance(col, tuple) else col
    my = hy + 0.58 * hh
    if view == 'side':
        x0 = hx + 0.92 * hw
        p.poly(curve([(x0 - 30, my - 6), (x0 + 4, my - 8), (x0 + 6, my + 6), (x0 - 26, my + 10)], 2), col, INK, 1.6)
        return
    o = 0.3 * hw if view == 'three' else 0.0
    m = [(hx + o - 0.56 * hw, my - 10), (hx + o - 0.4 * hw, my - 4), (hx + o, my - 10), (hx + o + 0.4 * hw, my - 4),
         (hx + o + 0.56 * hw, my - 10), (hx + o + 0.3 * hw, my + 6), (hx + o, my + 4), (hx + o - 0.3 * hw, my + 6)]
    # the ends turned up, so the mouth under it reads as a grin (hunt 1: the down-turned ends read as a frown)
    p.poly(curve(m, 3), col, INK, 1.6)


def polo_collar(p, view, sp):
    """The polo shirt's collar and placket (front)."""
    if view not in ('front', 'three'):
        return
    o = 16 if view == 'three' else 0
    c = B.dk(sp.get('jacket', (92, 160, 210)), 0.8)
    for sg in (-1, 1):
        p.poly([(o + sg * 4, 6), (o + sg * 58, -6), (o + sg * 64, 22), (o + sg * 18, 40)], sp.get('jacket'), INK, 1.8)
    p.line([(o, 30), (o, 110)], c, 2.2)
    for yy in (52, 80):
        p.ell(o, yy, 4, 4, (240, 240, 236), None)


def shorts(p, view, sp):
    """Knee-length shorts over the legs (the legs below are bare: the kit's trousers set to skin)."""
    col = sp.get('shorts', (196, 176, 128))
    if view in ('side',):
        p.poly([(-70, 470), (70, 470), (78, 650), (-60, 650)], col, INK, 2.2)
        return
    sw = sp.get('shoulders', 168)
    w = sw * 0.62
    p.poly([(-w, 470), (w, 470), (w + 10, 650), (8, 650), (0, 580), (-8, 650), (-w - 10, 650)], col, INK, 2.2)
    p.line([(-w + 20, 520), (-w + 60, 520)], B.dk(col, 0.8), 2.0)


def bum_bag(p, view, sp):
    """A black bum bag on its strap at the belly, the zip across it."""
    sw = sp.get('shoulders', 168)
    if view == 'side':
        p.poly([(30, 420), (96, 418), (100, 470), (34, 474)], BUMBAG, INK, 2.0)
        return
    if view in ('back', 'three_back'):
        p.line([(-sw * 0.85, 440), (sw * 0.85, 440)], BUMBAG, 8)
        return
    o = 16 if view == 'three' else 0
    p.line([(-sw * 0.9, 430), (sw * 0.9, 430)], BUMBAG, 8)
    p.poly(curve([(o - 74, 420), (o + 74, 420), (o + 82, 470), (o + 60, 488), (o - 60, 488), (o - 82, 470)], 2),
           BUMBAG, INK, 2.0)
    p.line([(o - 66, 444), (o + 66, 444)], (150, 150, 150), 2.0)


def camera(p, view, sp):
    """A camera on a strap round his neck, resting on his chest."""
    if view in ('back', 'three_back'):
        return
    if view == 'side':
        p.line([(10, 0), (60, 200)], INK, 4)
        p.poly([(40, 190), (100, 190), (100, 250), (40, 250)], CAMERA, INK, 2.0)
        p.ell(112, 220, 16, 22, (60, 62, 66), INK, 1.6)
        return
    o = 16 if view == 'three' else 0
    p.line(curve([(o - 60, -4), (o - 50, 120), (o - 30, 200)], 3), INK, 4)
    p.line(curve([(o + 60, -4), (o + 50, 120), (o + 30, 200)], 3), INK, 4)
    p.poly([(o - 56, 190), (o + 56, 190), (o + 56, 262), (o - 56, 262)], CAMERA, INK, 2.2)
    p.poly([(o - 40, 180), (o - 10, 180), (o - 10, 192), (o - 40, 192)], CAMERA, INK, 1.6)
    p.ell(o + 6, 228, 26, 26, (70, 72, 78), INK, 2.0)
    p.ell(o + 6, 228, 14, 14, (20, 22, 30), None)
    p.ell(o + 10, 222, 4, 4, (200, 210, 230), None)


def txt(p, x, y, words, size, col):
    """Text centred at (x, y) in a pen's own units (scaled with the person)."""
    L = p.L if hasattr(p, 'L') else None
    try:
        X, Y = p.cam.P(x, y) if hasattr(p, 'cam') else L.P(x, y)
        k = abs((p.cam if hasattr(p, 'cam') else L).S(size))
    except Exception:
        return
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), max(6, int(k)))
    ImageDraw.Draw(p.img).text((X, Y), words, font=f, fill=col, anchor='mm')


def tote(p, view, sp):
    """A canvas tote on her left shoulder (screen right from the front): GREETINGS FROM TIRANA."""
    if view in ('back', 'three_back'):
        return
    sw = sp.get('shoulders', 140)
    if view == 'side':
        p.line([(-10, 4), (-4, 330)], TOTE, 7)
        p.line([(-10, 4), (-4, 330)], INK, 1.2)
        p.poly([(-50, 330), (40, 330), (46, 470), (-56, 470)], TOTE, INK, 2.0)
        return
    x = -10                                               # worn cross-body, the bag on her front: her hands at her
    p.line([(sw * 0.6, 6), (x + 70, 320)], TOTE, 7)        # sides no longer cover the words (hunt 2, line O1)
    p.line([(sw * 0.6, 6), (x + 70, 320)], INK, 1.2)
    p.poly([(x - 60, 320), (x + 80, 320), (x + 90, 490), (x - 70, 490)], TOTE, INK, 2.0)
    p.ell(x + 10, 378, 34, 20, (90, 150, 200), None)           # a little sun-and-sea print
    p.ell(x + 10, 360, 12, 12, (240, 180, 60), None)
    for k, w in enumerate(('GREETINGS', 'FROM', 'TIRANA')):    # the words, in the pen's own units (hunt 1: dashes)
        txt(p, x + 10, 420 + k * 24, w, 22 if k < 2 else 30, (200, 40, 50))


def cardigan(p, view, sp):
    """An open cardigan over her dress: two fronts, buttons down one edge."""
    sw = sp.get('shoulders', 136)
    if view == 'side':                                    # its open front edge, the dark dress showing behind it, so
        p.poly([(40, 20), (66, 30), (74, 505), (46, 505)], CARDIGAN, INK, 2.0)   # her red sleeve reads (hunt 1)
        return
    if view in ('back', 'three_back'):
        return
    o = 12 if view == 'three' else 0
    for sg in (-1, 1):
        p.poly([(o + sg * 30, 10), (sg * (sw - 6), 18), (sg * (sw + 2), 505), (o + sg * 46, 505)], CARDIGAN, INK, 2.0)
    for yy in (140, 230, 320, 410):
        p.ell(o - 40, yy, 6, 6, CARDIGAN_D, None)


def long_skirt(p, view, sp):
    """Her dress carries on to a long skirt, mid-calf."""
    col = sp.get('dress', (44, 40, 46))
    if view == 'side':
        p.poly(curve([(-74, 470), (70, 470), (92, 820), (-96, 826)], 1), col, INK, 2.2)
        return
    sw = sp.get('shoulders', 136)
    p.poly([(-sw * 0.68, 480), (sw * 0.68, 480), (sw * 0.86, 820), (-sw * 0.86, 820)], col, INK, 2.2)
    p.line([(-sw * 0.3, 560), (-sw * 0.36, 810)], B.dk(col, 0.7), 1.8)


def apron(p, view, sp):
    """A white apron from the chest to the knee, its neck strap and a pocket with a lighter in it."""
    if view in ('back', 'three_back'):
        return
    if view == 'side':
        p.poly([(50, 120), (78, 120), (92, 700), (60, 700)], APRON, INK, 2.0)
        return
    o = 14 if view == 'three' else 0
    sw = sp.get('shoulders', 174)
    p.line([(o - 50, 120), (o - 30, 4)], APRON_D, 6)
    p.line([(o + 50, 120), (o + 30, 4)], APRON_D, 6)
    p.poly([(o - 64, 120), (o + 64, 120), (o + 70, 400), (o + sw * 0.7, 410), (o + sw * 0.66, 700),
            (o - sw * 0.66, 700), (o - sw * 0.7, 410), (o - 70, 400)], APRON, INK, 2.2)
    p.poly([(o - 50, 470), (o + 50, 470), (o + 50, 550), (o - 50, 550)], APRON_D, INK, 1.6)
    p.poly([(o + 14, 448), (o + 34, 448), (o + 34, 480), (o + 14, 480)], (200, 50, 40), INK, 1.4)   # the lighter
    for k in range(3):                                    # soot smudges: he works with petrol
        p.ell(o - 30 + k * 40, 600 + (k % 2) * 30, 10, 6, (150, 144, 134), None)


def shopping_bag(j, side='L'):
    """A string shopping bag of oranges hanging off her forearm (a prop at the elbow, drawn over the arm)."""
    def draw(p, j2):
        el = np.asarray(j['el' + side])
        wr = np.asarray(j['wr' + side])
        c = P3(dict(j, _yaw=j2['yaw']), tuple(el + (wr - el) * 0.3))
        x, y = c[0] + (-34 if j2['yaw'] < 60 else 0), c[1]      # hung off the forearm's outside, her hand clear
        p.line([(x - 26, y + 6), (x, y - 10), (x + 26, y + 6)], (60, 60, 56), 3)
        p.poly(curve([(x - 40, y + 6), (x + 40, y + 6), (x + 50, y + 70), (x + 24, y + 110), (x - 24, y + 110),
                      (x - 50, y + 70)], 3), (240, 236, 220), INK, 2.0)
        for dx, dy in ((-20, 40), (14, 44), (-4, 76), (24, 80), (-26, 82)):
            p.ell(x + dx, y + dy, 13, 13, (240, 150, 40), INK, 1.2)
    draw.side = side
    return draw


TOURIST_DRESS = {   # who -> (head props, body props, sp changes): what draw() puts on them
    'husband': ([baseball_cap], [shorts, polo_collar, bum_bag, camera], dict(trousers='skin', shorts=(196, 176, 128))),
    'wife': ([sun_visor], [shorts, tote], dict(trousers='skin', shorts=(240, 236, 226))),
    'granny': ([headscarf], [long_skirt, cardigan], {}),
    'seller': ([flat_cap, moustache], [apron], {}),
}


def tourist(who):
    """The new cast's sp, with their dress's changes (bare legs under shorts: the trousers in skin colour)."""
    sp = dict(CAST[who])
    for k, v in TOURIST_DRESS[who][2].items():
        sp[k] = sp['skin'] if v == 'skin' else v
    if who == 'granny':                                   # under the headscarf: no bun poking through it
        sp['kit_face'] = dict(sp['kit_face'], hair='crop', turned='crop')
    if who == 'seller':                                   # a seller's patter, not a frown (hunt 1, line O3)
        sp.update(smile=0.7, brow_up=0.03)
    return sp


def dress_new(j, sp):
    heads, bodies, _ = TOURIST_DRESS[sp['who']]
    j['head_props'] = list(heads) + j.get('head_props', [])
    j['body_props'] = list(bodies) + j.get('body_props', [])
    return j


# ------------------------------------------------------------------------------------------------ drawing one
def draw(img, cam, x, y, s, sp, j, yaw, kind=None, head=None):
    """One of the cast at neck base (x, y), scale s for a 1.75 m person (their own height applied here)."""
    kind = kind or ('officer' if sp.get('force') else 'rioter' if sp['who'] in ('rioter', 'rider', 'gunner')
                    else 'marcher')
    if not j.get('_dressed'):
        if kind == 'officer':
            dress_officer(j)
        elif kind == 'rioter':
            dress_rioter(j)
        elif sp.get('who') in TOURIST_DRESS:
            dress_new(j, sp)
        j['_dressed'] = True
    j['_yaw'] = V.snap(yaw)[0]
    s2 = s * sp.get('height', 1.75) / 1.75
    return V.person(img, cam, x, y - (928 * (s2 - s)), s2, dict(sp, full=True, pose='custom'), 0.0, yaw, j,
                    head_yaw=head)


# ------------------------------------------------------------------------------------------------ the seller's cart
CART_WOOD, CART_WOOD_D = (150, 104, 62), (108, 72, 42)
UMB_A, UMB_B = (214, 52, 48), (246, 240, 226)
BOTTLE_G = (84, 132, 80)


def cart(img, cam, x, y, s, flame=0.0, bottles=12, front=True):
    """The Molotov seller's street cart, front on, in the seller's frame (neck base (x, y), scale s for 1.75 m; the
    ground at 928): two cart wheels, a wooden box at waist height with two crates of bottles (rags in their necks), a
    striped umbrella on a pole, a hand-painted sign "MOLOTOV 200 LEK" hung on the front, a tin can with a little flame
    (flame: 0..1 flicker phase). front False draws only the umbrella (behind him); front True the rest (over his
    legs). bottles: how many are left in the crates (he hands them over)."""
    L = B.Local(cam, x, y, s, 1)
    p = B.Pen(img, L)
    if not front:
        p.line([(250, 470), (250, -560)], (60, 60, 64), 9)
        n = 8
        for i in range(n):                         # the umbrella's canopy: alternating red and cream panels
            a0, a1 = -170 + i * 340 / n, -170 + (i + 1) * 340 / n
            pts = [(250, -600)] + [(250 + 360 * math.sin(math.radians(a)), -470 + 40 * math.cos(math.radians(a)) * 0)
                                   for a in (a0 + (a1 - a0) * k / 4 for k in range(5))]
            p.poly(pts, UMB_A if i % 2 == 0 else UMB_B, INK, 2.2)
        for i in range(n + 1):                     # the scalloped hem
            a = -170 + i * 340 / n
            p.ell(250 + 360 * math.sin(math.radians(a)), -466, 14, 10, UMB_A if i % 2 == 0 else UMB_B, INK, 1.4)
        p.ell(250, -606, 12, 12, (60, 60, 64), INK, 1.6)
        return
    top, bot = 380, 700
    for wx in (-300, 300):                          # the wheels, half behind the box
        p.ell(wx, 840, 86, 86, (60, 56, 52), INK, 3.0)
        p.ell(wx, 840, 22, 22, CART_WOOD_D, INK, 1.8)
        for k in range(6):
            a = math.radians(k * 60)
            p.line([(wx, 840), (wx + 70 * math.cos(a), 840 + 70 * math.sin(a))], CART_WOOD_D, 6)
    p.poly([(-420, top), (420, top), (410, bot), (-410, bot)], CART_WOOD, INK, 3.0)
    for yy in (460, 540, 620):                      # planks
        p.line([(-410, yy), (410, yy)], CART_WOOD_D, 2.4)
    p.line([(420, top + 30), (560, top - 20)], CART_WOOD_D, 14)     # the push handle out to the side
    # the crates on top, bottles standing in them (necks up, rags in their necks)
    k = 0
    for cx0 in (-380, -20):
        for i in range(6):
            if k >= bottles:
                break
            bx = cx0 + 34 + i * 54
            p.poly([(bx - 18, top - 10), (bx + 18, top - 10), (bx + 18, top - 110), (bx + 8, top - 130),
                    (bx + 8, top - 170), (bx - 8, top - 170), (bx - 8, top - 130), (bx - 18, top - 110)],
                   BOTTLE_G, INK, 1.8)
            p.poly([(bx - 10, top - 168), (bx + 10, top - 168), (bx + 22, top - 224), (bx + 2, top - 214),
                    (bx - 14, top - 230)], (246, 240, 226), INK, 1.8)          # the rag (hunt 1: too small to see)
            k += 1
        p.poly([(cx0, top - 80), (cx0 + 340, top - 80), (cx0 + 340, top), (cx0, top)], (196, 160, 104), INK, 2.4)
        p.line([(cx0 + 10, top - 40), (cx0 + 330, top - 40)], CART_WOOD_D, 2.0)
    # the tin with its little flame (he lights the rags from it), on the cart's right end
    tx = 360
    p.poly([(tx - 30, top - 70), (tx + 30, top - 70), (tx + 30, top), (tx - 30, top)], (160, 164, 170), INK, 2.0)
    w = 1.0 + 0.18 * math.sin(flame * 2 * math.pi)
    p.poly(curve([(tx - 26, top - 70), (tx - 20 * w, top - 120), (tx - 4, top - 150 * w), (tx + 8, top - 118),
                  (tx + 22 * w, top - 140), (tx + 26, top - 70)], 3), (250, 150, 40), INK, 1.8)
    p.poly(curve([(tx - 12, top - 70), (tx - 6, top - 108 * w), (tx + 10, top - 96), (tx + 12, top - 70)], 3),
           (255, 226, 120), None)
    # the hand-painted sign, cardboard, hung on the front of the box
    p.poly([(-260, 470), (260, 466), (256, 650), (-256, 654)], (226, 200, 150), INK, 2.6)
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), max(8, int(abs(L.S(78)))))
    f2 = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), max(8, int(abs(L.S(62)))))
    d = ImageDraw.Draw(img)
    d.text(L.P(0, 520), 'MOLOTOV', font=f, fill=(170, 30, 30), anchor='mm')
    d.text(L.P(0, 600), '200 LEK', font=f2, fill=(30, 30, 30), anchor='mm')


def seller_scene(img, cam, x, y, s, j=None, flame=0.0, bottles=12):
    """The seller behind his cart: the umbrella, him, then the cart over his legs."""
    sp = tourist('seller')
    j = j if j is not None else V.standing(sp)
    cart(img, cam, x, y, s, flame, bottles, front=False)
    draw(img, cam, x, y, s, sp, j, 0)
    cart(img, cam, x, y, s, flame, bottles, front=True)


# ------------------------------------------------------------------------------------------------ the moped
MOPED, MOPED_D, TYRE = (176, 34, 40), (120, 22, 28), (30, 30, 32)
RPG_C, RPG_D, WARHEAD = (86, 92, 70), (60, 64, 50), (90, 96, 76)


def _moped_parts(X):
    """The scooter in the driver's body frame (units; z forward, y down; ground at y = X['ground']). About 1.8 m
    long, 12-inch wheels, a step-through floor, a front apron, the seat, the handlebar with its headlight."""
    g = X['ground']
    r = 0.22 * U
    fz, bz = 0.62 * U, -0.66 * U                     # wheel centres (front, back) relative to the driver's hips
    seat = g - 0.78 * U
    return dict(r=r, front=(0.0, g - r, fz), back=(0.0, g - r, bz), seat=seat, g=g, fz=fz, bz=bz)


def moped_back(p, j, X):
    """Wheels, the rear body under the seat, the floor (drawn before the riders)."""
    m = _moped_parts(X)
    yaw = X['yaw']

    def q(x, y, z):
        return V.project((x, y, z), yaw)[0]

    def wheel(c):
        pts = [q(c[0], c[1] + m['r'] * math.sin(a), c[2] + m['r'] * math.cos(a)) for a in np.linspace(0, 2 * math.pi, 28)]
        p.poly(pts, TYRE, INK, 2.4)
        pts = [q(c[0], c[1] + m['r'] * 0.5 * math.sin(a), c[2] + m['r'] * 0.5 * math.cos(a))
               for a in np.linspace(0, 2 * math.pi, 20)]
        p.poly(pts, (170, 170, 168), INK, 1.6)
    wheel(m['back'])
    wheel(m['front'])
    g, s, bz, fz = m['g'], m['seat'], m['bz'], m['fz']
    body = [(bz - 0.22 * U, s + 30), (bz - 0.12 * U, s - 10), (0.12 * U, s - 10), (0.18 * U, s + 60),
            (0.16 * U, g - 0.3 * U), (0.42 * U, g - 0.28 * U), (0.46 * U, g - 0.2 * U), (-0.1 * U, g - 0.16 * U),
            (bz + 0.1 * U, g - 0.2 * U), (bz - 0.12 * U, g - 0.34 * U)]
    p.poly(curve([q(0, y, z) for z, y in body], 2), MOPED, INK, 2.6)
    p.poly(curve([q(0, y, z) for z, y in [(bz - 0.18 * U, s + 20), (bz - 0.08 * U, s - 4), (bz + 0.1 * U, s + 40),
                                         (bz - 0.12 * U, s + 70)]], 2), MOPED_D, None)           # side panel shade
    seat = [(bz - 0.14 * U, s - 6), (bz - 0.06 * U, s - 36), (0.14 * U, s - 36), (0.18 * U, s - 4)]
    p.poly(curve([q(0, y, z) for z, y in seat], 2), (26, 24, 26), INK, 2.2)
    p.ell(*q(0, s + 10, bz - 0.24 * U), 12, 9, (220, 40, 30), INK, 1.4)                         # tail light


def moped_front(p, j, X):
    """The apron in front of the driver's shins, the steering column, the handlebar and the headlight (drawn after
    his legs, before his arms: his hands go over the grips)."""
    m = _moped_parts(X)
    yaw = X['yaw']

    def q(x, y, z):
        return V.project((x, y, z), yaw)[0]
    g, fz = m['g'], m['fz']
    hb = X['bar']                                  # the handlebar's grip point (y, z)
    col = [(fz - 0.06 * U, g - m['r']), (hb[1] - 0.02 * U, hb[0] + 30)]
    p.line([q(0, y, z) for z, y in col], INK, 18)
    p.line([q(0, y, z) for z, y in col], (60, 60, 64), 11)
    apron = [(0.34 * U, g - 0.26 * U), (0.42 * U, g - 0.5 * U), (hb[1] - 0.04 * U, hb[0] + 60), (hb[1] + 0.06 * U, hb[0] + 40),
             (fz + 0.02 * U, g - 0.52 * U), (fz - 0.04 * U, g - 0.3 * U), (0.5 * U, g - 0.2 * U)]
    p.poly(curve([q(0, y, z) for z, y in apron], 2), MOPED, INK, 2.6)
    p.poly(curve([q(0, y, z) for z, y in [(fz - 0.08 * U, g - m['r'] - 40), (fz, g - m['r'] - 70), (fz + 0.12 * U, g - m['r'] - 40),
                                         (fz + 0.06 * U, g - m['r'] - 10)]], 2), MOPED, INK, 2.2)   # mudguard
    head = [(hb[1] - 0.02 * U, hb[0] - 10), (hb[1] + 0.12 * U, hb[0] - 4), (hb[1] + 0.14 * U, hb[0] + 50),
            (hb[1] - 0.02 * U, hb[0] + 60)]
    p.poly(curve([q(0, y, z) for z, y in head], 2), MOPED, INK, 2.4)
    p.ell(*q(0, hb[0] + 24, hb[1] + 0.14 * U), 10, 18, (250, 246, 200), INK, 1.6)               # headlight
    p.line([q(-90, hb[0], hb[1]), q(90, hb[0], hb[1])], INK, 12)                                 # the bar


def driver_pose(sp, X):
    j = V.standing(sp)
    j['bob'] = X['bob']
    j['seated'] = True
    j['chair_draw'] = lambda *a, **k: None
    j['lean'] = 12
    floor = X['ground'] - 0.24 * U - 38 - X['bob']
    for s, sg in (('L', -1), ('R', 1)):
        j['foot' + s] = (sg * 60, floor, 150.0)
        j['knee_pole' + s] = (0.1 * sg, -1.0, 0.7)
    for s, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, s, (sg * 90, X['bar'][0] - X['bob'], X['bar'][1] - 20), 'out')
    return j


def gunner_pose(sp, X, aim=38.0):
    """Sitting behind the driver, the RPG on his right shoulder aimed up and forward (aim degrees above level)."""
    j = V.standing(sp)
    j['bob'] = X['bob'] - 26
    j['seated'] = True
    j['chair_draw'] = lambda *a, **k: None
    j['lean'] = 4
    floor = X['ground'] - 0.3 * U - 38 - j['bob']
    for s, sg in (('L', -1), ('R', 1)):
        j['foot' + s] = (sg * 70, floor, 60.0)
        j['knee_pole' + s] = (0.1 * sg, -1.0, 0.6)
    a = math.radians(aim)
    u = np.array((0.0, -math.sin(a), math.cos(a)))
    sh = np.array((sp.get('shoulders', 150) - 30.0, 30.0, 0.0))
    j['_rpg'] = (sh, u)
    V.arm_to(j, 'R', tuple(sh + u * 150 + (0, 70, 0)), 'down')
    V.arm_to(j, 'L', tuple(sh + u * 330 + (-30, 50, 0)), 'down')
    return j


def open_palm(j, side='R'):
    """An open gloved hand, palm up, fingers spread (the shrug): a black glove with a grey palm so it reads."""
    def draw(p, j2):
        if j.get('_free') != side:
            return
        x, y = P3(dict(j, _yaw=j2['yaw']), tuple(_hand_c(j, side)))
        p.ell(x, y, 28, 18, (24, 24, 26), INK, 2.2)
        p.ell(x, y - 4, 18, 9, (120, 120, 126), None)
        for k in range(4):
            a = math.radians(-160 + k * 30)
            p.line([(x + 18 * math.cos(a), y - 8 + 10 * math.sin(a)), (x + 46 * math.cos(a), y - 14 + 30 * math.sin(a))],
                   INK, 11)
            p.line([(x + 18 * math.cos(a), y - 8 + 10 * math.sin(a)), (x + 46 * math.cos(a), y - 14 + 30 * math.sin(a))],
                   (24, 24, 26), 7)
    draw.side = side
    return draw


def shrug(j, sp, u):
    """The passenger's shrug (end shot C), u 0..1 eased in: his near (right) hand lets go of the launcher's grip and
    opens palm up, raised out behind him at head height, both shoulders lift, the head tips; the RPG stays on his shoulder, steadied by
    his far hand (the near hand: side on, the far one is hidden behind him)."""
    e = moves.ease(min(1.0, max(0.0, u)))
    if e <= 0:
        return j
    sw = sp.get('shoulders', 150)
    for sd in 'LR':
        x, y, z = j['sh' + sd]
        j['sh' + sd] = (x, y - 28 * e, z)
    hold = np.asarray(j['wrR'], float)
    out = np.array((200.0, -20.0, -200.0))           # up and out behind him, palm up at head height: side on, the only
    bulge = np.array((150.0, 0.0, 0.0)) * math.sin(math.pi * e)   # chat 24: mid-way the straight path passed the
    V.arm_to(j, 'R', tuple(hold + (out - hold) * e + bulge), 'out')   # shoulder (elbow folded): swing out round it
    if e > 0.5:
        j.setdefault('hand', {})['R'] = 'palm'
    j['_free'] = 'R'
    j['head_roll'] = -8 * e
    return j


def rpg(p, j, yaw, fired=False):
    """The RPG launcher on the shoulder: an olive tube about 0.95 m, the bulbous warhead in front (none once fired),
    a grip, the sight; drawn over the rider (it is on his near shoulder), then his near hand over its grip."""
    sh, u = j['_rpg']
    jj = dict(j, _yaw=V.snap(yaw)[0])
    rear, front = sh - u * 0.38 * U, sh + u * 0.57 * U
    a, b = P3(jj, tuple(rear)), P3(jj, tuple(front))
    p.line([a, b], INK, 44)                                # chat 15 (moves hunt 1: "no RPG shape" at phone size):
    p.line([a, b], RPG_C, 36)                              # drawn thicker than true, as a Glimpse prop must read
    mid = P3(jj, tuple(sh + u * 0.05 * U))
    mid2 = P3(jj, tuple(sh + u * 0.25 * U))
    p.line([mid, mid2], RPG_D, 38)                         # the wooden heat guard (dark band)
    p.line([a, P3(jj, tuple(rear + u * 0.06 * U))], INK, 52)   # the flared rear venturi
    if not fired:
        w0 = P3(jj, tuple(front))
        w1 = P3(jj, tuple(front + u * 0.32 * U))
        dx, dy = w1[0] - w0[0], w1[1] - w0[1]
        n = math.hypot(dx, dy) or 1
        nx, ny = -dy / n, dx / n
        pts = [(w0[0] + nx * 14, w0[1] + ny * 14), (w0[0] + dx * 0.45 + nx * 30, w0[1] + dy * 0.45 + ny * 30),
               (w1[0], w1[1]), (w0[0] + dx * 0.45 - nx * 30, w0[1] + dy * 0.45 - ny * 30), (w0[0] - nx * 14, w0[1] - ny * 14)]
        p.poly(curve(pts, 2), WARHEAD, INK, 2.4)
    for side in 'RL':
        if j.get('_free') == side:                 # that hand has let go (the shrug): the kit draws it
            continue
        c = P3(jj, tuple(_hand_c(j, side)))
        p.ell(c[0], c[1], 26, 26, (24, 24, 26), INK, 2.4)


def moped_scene(img, cam, x, y, s, yaw=90, aim=38.0, fired=False, both=True, drv_head=None, gun_head=None,
                shrug_u=0.0, rim=None, drv_roll=0.0):
    """The moped racing in with its driver and (both) the RPG passenger. (x, y): the driver's neck base at scale s;
    returns nothing. Side on (90) or three-quarter (45) facing right. drv_head / gun_head: where each one's head faces
    (degrees, as yaw: -30 turned back over his shoulder toward us, 0 to camera; None = with the body). shrug_u: the
    passenger's shrug (0..1). rim: a light colour drawn as a thin outline round the whole group, so dark hoodies
    read against a dark road (round 1 critique: the riders merged into the road)."""
    if rim is not None:
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        moped_scene(lay, cam, x, y, s, yaw, aim, fired, both, drv_head, gun_head, shrug_u, None, drv_roll)
        from PIL import ImageFilter
        a = lay.split()[3]
        w = max(3, int(round(abs(cam.S(1.0) if hasattr(cam, 'S') else 1.0) * s * 14)) | 1)
        grown = a.filter(ImageFilter.MaxFilter(w))
        glow = Image.new('RGBA', img.size, tuple(rim) + (0,))
        glow.putalpha(grown.point(lambda v: 230 if v > 40 else 0))
        img.alpha_composite(glow)
        img.alpha_composite(lay)
        return
    drv, gun = rioter('rider'), rioter('gunner')
    X = dict(ground=928.0 - (-30.0), bob=-30.0, yaw=V.snap(yaw)[0])
    X['ground'] = 928.0 + 0.0                     # in the driver's body frame: soles of a standing driver
    X['bar'] = (928.0 - 1.02 * U, 0.5 * U)        # grip height 1.02 m, 0.5 m ahead of his hips
    X['bob'] = (450.0 - (928.0 - 0.8 * U))        # hips on the seat (0.8 m up): negative = raised
    jd = driver_pose(drv, X)
    if drv_roll:                                  # end shot C: the driver's small head tilt on "protest"
        jd['head_roll'] = drv_roll
    jg = gunner_pose(gun, X, aim)
    if shrug_u > 0:
        shrug(jg, gun, shrug_u)
        jg['props'] = jg.get('props', []) + [open_palm(jg, 'R')]
    sd = s * drv['height'] / 1.75
    L = B.Local(cam, x, y, sd, 1)
    pen = B.Pen(img, L)
    moped_back(pen, jd, X)
    gz = -0.42 * U                                # the passenger sits 0.42 m behind the driver
    gx, _ = V.project((0.0, 0.0, gz), X['yaw'])[0]
    if both:
        draw(img, cam, x + gx * sd, y, s, gun, jg, yaw, 'rioter', head=gun_head)
    jd['mid'] = [lambda p, j2, view: moped_front(p, jd, X)]
    draw(img, cam, x, y, s, drv, jd, yaw, 'rioter', head=drv_head)
    if both:
        Lg = B.Local(cam, x + gx * sd, y + jg['bob'] * s * gun['height'] / 1.75, s * gun['height'] / 1.75, 1)
        rpg(B.Pen(img, Lg), jg, yaw, fired)


def rpg_ends(cam, x, y, s, yaw=90, aim=38.0):
    """Where moped_scene draws the launcher's rear and muzzle on screen (the same maths): the end scene's backblast
    and rocket start there."""
    gun = rioter('gunner')
    X = dict(ground=928.0, yaw=V.snap(yaw)[0])
    X['bar'] = (928.0 - 1.02 * U, 0.5 * U)
    X['bob'] = (450.0 - (928.0 - 0.8 * U))
    jg = gunner_pose(gun, X, aim)
    sd = s * rioter('rider')['height'] / 1.75
    gx, _ = V.project((0.0, 0.0, -0.42 * U), X['yaw'])[0]
    sg = s * gun['height'] / 1.75
    Lg = B.Local(cam, x + gx * sd, y + jg['bob'] * sg, sg, 1)
    sh, u = jg['_rpg']
    jj = dict(jg, _yaw=X['yaw'])
    return Lg.P(*P3(jj, tuple(sh - u * 0.38 * U))), Lg.P(*P3(jj, tuple(sh + u * 0.57 * U)))


# ------------------------------------------------------------------------------------------------ sheets
def font(n):
    return ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)


TILE_FAULTS = []    # (label, fault) from every tile drawn: the hand check runs on each (rule 41; chat 8: chat 5's sheet
                    # was never checked, so the phone behind the head (note 1) reached Sam)


# hand-check faults on the cast sheet that are meant, each looked at on a 2x crop (chat 8): (label pattern, side,
# kind pattern, why). The check sees a hand under a prop as covered even when the prop is see-through.
HANDS_OK = [
    ('Mossos (Barcelona)', 'L', 'no hand', 'the shield hand, behind the clear shield: seen through the glass'),
    ('Polizei (Frankfurt)', 'L', 'no hand', 'the shield hand, behind the clear shield: seen through the glass'),
    ('CRS (Paris)', 'L', 'no hand', 'the shield hand, behind the clear shield: seen through the glass'),
    ('Policia (Tirana)', 'L', 'no hand', 'the shield hand, behind the clear shield: seen through the glass'),
    ('Policia, baton up', 'L', 'no hand', 'the shield hand, behind the clear shield: seen through the glass'),
    ('Policia, baton up', 'R', 'no hand', 'the fist shows on the baton grip above his helmet (the baton is drawn over it)'),
    ('Mossos from behind', '*', 'no hand', 'from behind: the shield is held in front, his hands hidden by his back'),
    ('Moped + RPG', 'R', 'no hand', 'the far hands (handlebar, launcher) are beyond the bodies, side on'),
    ('Moped + RPG', 'L', 'over *', 'two riders on one moped: the rider sits against the passenger'),
    ('Riders*', '*', 'no hand', 'side on: the far hands (handlebar, launcher) are beyond the bodies'),
    ('Riders*', '*', 'over *', 'two riders on one moped: the rider sits against the passenger'),
    ('Selfie*', 'L', 'no hand', 'the peace sign / thumb is drawn over the fist, its own hand'),
    ('Granny*', 'L', 'no hand', 'the shopping bag hangs off her forearm in front of the hand'),
    ('Seller*', '*', 'no hand', 'his hands are behind the cart'),
]


def tile(fn, w=360, h=640, bg=(232, 228, 222), label='?', wide=False):
    """Draw fn(img, cam) on a 1080 x 1920 canvas and return the tight crop around what was drawn, fitted to w x h.
    The hand check (handcheck: no hand, in sleeve, behind or under the head, ...) runs on the drawing; its faults go
    in TILE_FAULTS and are printed."""
    import handcheck as H
    H.install()
    B.SS = 1
    img = Image.new('RGBA', (1080, 1920), bg + (255,))
    cam = B.Cam(1.0, 540, 960)
    H.begin()
    fn(img, cam)
    import fnmatch
    for f in H.end(0.0, label):
        ok = [why for lab, sd, kd, why in HANDS_OK if fnmatch.fnmatchcase(label, lab) and sd in ('*', f['side'])
              and fnmatch.fnmatchcase(f['kind'], kd)]
        if ok:
            continue
        TILE_FAULTS.append((label, f))
        print(f"HANDS: {label}: {f.get('who', f.get('name', '?'))} {f.get('side', '')}: {f.get('kind', '?')}")
    a = np.asarray(img.convert('RGB')).astype(int)
    diff = np.abs(a - np.array(bg)).sum(2) > 12
    ys, xs = np.nonzero(diff)
    if len(xs):
        box = [max(0, xs.min() - 16), max(0, ys.min() - 16), min(1080, xs.max() + 16), min(1920, ys.max() + 16)]
        cx = (xs.min() + xs.max()) / 2              # a long prop (the sign's pole) never shrinks the figure: the
        if box[2] - box[0] > (1080 if wide else 760):                   # crop is capped round the drawing's middle (chat 6)
            box[0], box[2] = int(max(0, cx - 380)), int(min(1080, cx + 380))
        if not wide and box[3] - box[1] > 1250:
            box[1] = box[3] - 1250
        img = img.crop(box)
    img.thumbnail((w, h))
    return img


def cast_items():
    """(label, fn) for everyone alone, large: each force in the line, the rioter's poses, the marchers, the moped."""
    items = []
    for f in FORCES:
        def one(img, cam, f=f):
            sp = officer(f)
            draw(img, cam, 540, 700, 0.62, sp, pose(sp, 'line'), -45)
        items.append((FORCES[f]['name'], one))
    sp0 = officer('policia')
    items.append(('Policia, side, line', lambda img, cam: draw(img, cam, 540, 700, 0.62, officer('policia'),
                                                                pose(officer('policia'), 'line'), -90)))
    items.append(('Policia, baton up', lambda img, cam: draw(img, cam, 540, 700, 0.62, sp0, pose(sp0, 'baton_up'), -45)))
    items.append(('Mossos from behind', lambda img, cam: draw(img, cam, 540, 700, 0.62, officer('mossos'),
                                                              pose(officer('mossos'), 'line'), 180)))
    r = rioter()
    items.append(('Rioter, front', lambda img, cam: draw(img, cam, 540, 700, 0.62, r, V.standing(r), 0)))
    items.append(('Rioter, running', lambda img, cam: draw(img, cam, 540, 700, 0.62, r, pose(r, 'run', t=0.1), 90)))
    items.append(('Rioter, throwing (wind-up)', lambda img, cam: draw(img, cam, 540, 700, 0.62, r,
                                                                      pose(r, 'throw', 0.0), 90)))
    items.append(('Rioter, sign swing', lambda img, cam: draw(img, cam, 640, 760, 0.62, r, pose(r, 'swing', 0.2), 90)))
    items.append(('Rioter, from behind', lambda img, cam: draw(img, cam, 540, 700, 0.62, r, V.standing(r), 180)))
    for i, (tier, nm, kind) in enumerate((('t1', 'keys', None), ('t1', 'flag', 'catalan'), ('t2', 'placard', None),
                                          ('t2', 'phone', None), ('t3', 'flag', 'tricolour'), ('t4', 'flag', 'albania'))):
        def one(img, cam, i=i, tier=tier, nm=nm, kind=kind):
            sp = marcher(i, tier)
            draw(img, cam, 540, 700, 0.62, sp, pose(sp, nm, force=kind), 180 if nm in ('keys', 'flag') else 0)
        items.append((f'Marcher {tier}, {nm}', one))
    items.append(('Moped + RPG', lambda img, cam: moped_scene(img, cam, 640, 800, 0.5)))
    return items


def new_cast_items():
    """Round 1's cast (chat 22): the tourists, the granny, the seller and his cart, the selfie rioter, the riders."""
    items = []
    for who, label in (('husband', 'Husband (tourist)'), ('wife', 'Wife (tourist)')):
        for yaw, vw in ((0, 'front'), (90, 'side')):
            items.append((f'{label}, {vw}', lambda img, cam, who=who, yaw=yaw:
                          draw(img, cam, 540, 700, 0.62, tourist(who), V.standing(tourist(who)), yaw)))

    def granny(img, cam):
        sp = tourist('granny')
        j = V.standing(sp)
        j['props'] = [shopping_bag(j, 'L')]
        draw(img, cam, 540, 700, 0.62, sp, j, 90)
    items.append(('Granny, side', granny))
    items.append(('Seller + cart', lambda img, cam: seller_scene(img, cam, 540, 700, 0.62)))
    r = rioter()
    items.append(('Selfie rioter', lambda img, cam: draw(img, cam, 540, 700, 0.62, r, pose(r, 'selfie', 0.0), 0)))
    items.append(('Selfie, thumbs up', lambda img, cam: draw(img, cam, 540, 700, 0.62, r, pose(r, 'selfie', 1.0), 0)))
    items.append(('Riders, heads turned', lambda img, cam: moped_scene(img, cam, 640, 800, 0.5, aim=62, drv_head=0,
                                                                       gun_head=0, rim=RIM)))
    items.append(('Riders, the shrug', lambda img, cam: moped_scene(img, cam, 640, 800, 0.5, aim=62, drv_head=-30,
                                                                    gun_head=0, shrug_u=1.0, fired=True, rim=RIM)))
    return items


RIM = (255, 170, 90)                              # the riders' rim light: the fire's orange (end shots A and C)


def sheet(out, items=None, title='PROTEST TIERS: the cast (Glimpses: drawn large here, small in the film)'):
    items = items or cast_items()
    cols, tw, th = 6, 340, 560
    wide = {'Rioter, sign swing'}                   # the long pole: two tiles wide, so he is drawn full size (chat 8)
    places, k = [], 0
    for label, _ in items:
        n = 2 if label in wide else 1
        if k % cols + n > cols:
            k += cols - k % cols
        places.append((k, n))
        k += n
    rows = (k + cols - 1) // cols
    img = Image.new('RGB', (cols * tw + 40, rows * (th + 40) + 90), (232, 228, 222))
    d = ImageDraw.Draw(img)
    d.text((20, 20), title, font=font(34),
           fill=(30, 30, 30))
    for (label, fn), (k, n) in zip(items, places):
        t = tile(fn, tw * n - 10, th - 10, label=label, wide=n > 1)
        x0, y0 = 20 + (k % cols) * tw, 80 + (k // cols) * (th + 40)
        img.paste(t.convert('RGB'), (x0 + (tw * n - t.size[0]) // 2, y0 + th - t.size[1]))
        d.text((x0 + tw * n // 2, y0 + th + 18), label, font=font(20), fill=(30, 30, 30), anchor='mm')
    img.save(out, quality=88)
    print(f'hand check: {len(TILE_FAULTS)} fault(s) on {len(items)} tiles' if TILE_FAULTS else
          f'hand check: all {len(items)} tiles clean')
    return out


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    elif len(sys.argv) > 2 and sys.argv[1] == 'newcast':
        print(sheet(sys.argv[2], new_cast_items(), 'PROTEST TIERS round 1: the new cast'))
    else:
        print(__doc__)
