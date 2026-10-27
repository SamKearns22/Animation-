#!/usr/bin/env python3
"""Patriots 3: the MG42 crew at the bunker slit (refs bunker-1..4, mg42-1..6 in references/patriots-3/).

One small world in metres (patriots3_cast.Spot): the Gunner stands at the slit with the MG42 on its bipod on the
concrete sill, the butt in his shoulder, right hand on the pistol grip, left hand on top of the stock; the Loader
stands at his left (the belt feeds in from the gun's left side) and either feeds the belt with both hands, watches
through binoculars, or points and shouts. The embrasure is built from the gun: the sill is where the bipod's feet
stand, the wall 70 cm thick, the slit 1.9 m wide and up to 1.78 m.

Three cameras on the same world: from inside behind the crew (the beach through the slit), from the beach looking
in (the crew in the dark slit, the gun pointing at us), and from the side with the wall cut through (a section).

    python3 source/patriots3_bunker.py sheet OUT.jpg       the MG42 and the crew from the three cameras, Loader's poses
    python3 source/patriots3_bunker.py clip OUT.mp4        about 6 s: firing from inside, then from the beach (silent)
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import views as V                # noqa: E402
import patriots3_cast as C       # noqa: E402
from ed import INK, curve, oval  # noqa: E402
from satire_style import rough   # noqa: E402

M = V.M_PER_UNIT
GUNNER_AT = (0.0, 0.0)
LOADER_AT = (-0.55, 0.1)          # half a step forward, beside the gun (Sam, 27 Oct: his reach read as a cuddle)
LEAN_G = 16.0
SLIT_X = (-1.3, 0.62)          # the slit's sides, metres (the crew fit in it, seen from the beach)
SLIT_TOP = 2.05       # tall enough that the crew's faces show from the beach (the camera sees them from below the lintel)
THICK = 0.7
CONCRETE, CONCRETE_D, CONCRETE_L = (150, 146, 136), (116, 112, 104), (170, 166, 156)
INSIDE = (70, 70, 68)
DARK = (28, 28, 32)
EARTH, GRASS, GRASS_D = (112, 96, 72), (104, 124, 72), (78, 96, 54)
SKY, SKY_D = (196, 198, 196), (150, 154, 156)
SEA, SEA_D, SURF = (96, 110, 114), (74, 86, 92), (226, 228, 222)
WET, SAND = (150, 140, 122), (188, 176, 150)
IRON = (52, 46, 42)
CRAFT, CRAFT_D = (104, 110, 112), (70, 76, 80)


# ------------------------------------------------------------------------------------------------ the crew
class Crew:
    """The two soldiers, the gun, the belt and the box at one moment. `loader`: 'feed', 'spot' or 'point'.
    `fire_t`: seconds since the burst began (None: not firing)."""
    def __init__(self, loader='feed', fire_t=None, t=0.0):
        self.g_spot = C.Spot(C.GUNNER, *GUNNER_AT)
        self.l_spot = C.Spot(C.LOADER, *LOADER_AT)
        self.t, self.fire_t, self.loader = t, fire_t, loader
        frame = int(round((fire_t or 0.0) * 12))
        self.firing = fire_t is not None and fire_t >= 0
        self.kick = 0.016 if (self.firing and frame % 2 == 0) else 0.0
        self.flash = 1.0 if (self.firing and frame % 3 != 2) else 0.0
        self.jg = self._gunner()
        self.g = self.gun
        feet = C._bipod(C.Gun(self.butt, self.aim))
        self.sill = float(np.mean([f[1][1] for f in feet]))
        self.z_in = min(f[1][2] for f in feet) - 0.12
        self.z_out = self.z_in + THICK
        self.box_at = (-0.42, self.sill, (self.z_in + self.z_out) / 2 - 0.12)
        self.jl = self._loader()

    def _gunner(self):
        sp, spot = C.GUNNER, self.g_spot
        j = V.standing(sp)
        j['lean'] = LEAN_G
        j['footL'] = (-70.0, V.ANKLE_Y, 64.0)
        j['footR'] = (84.0, V.ANKLE_Y, -56.0)
        j['head_dy'] = 26
        sh = V.leaned(j['shR'], LEAN_G)
        butt_b = (sh[0] * 0.38, sh[1] + 6, sh[2] + 16)
        self.butt = spot.to_world(butt_b)
        self.aim = (0.0, -0.035, 1.0)
        self.gun = C.Gun(self.butt, self.aim, self.kick)
        g = self.gun
        V.arm_to(j, 'R', spot.unlean(g(0.39, -0.115), LEAN_G), 'down', 'fist')
        V.arm_to(j, 'L', spot.unlean(g(0.13, -0.075), LEAN_G), 'down', 'fist')   # under the stock, pulling it in
        j['grip'] = {'L', 'R'}
        j['props'] = [self._gun_prop()]
        return j

    def belt_points(self):
        g = self.gun
        feed = np.asarray(g(0.46, 0.022, -0.036))
        box_top = np.asarray(self.box_at) + np.asarray((0.0, 0.2, 0.0))
        if self.loader == 'feed':
            h1 = feed + np.asarray((-0.14, -0.13, 0.04))       # just under the feed, low by the gun
            h2 = np.asarray((self.box_at[0] - 0.04, self.sill + 0.26, self.box_at[2] - 0.06))
            return [feed, h1, h2, box_top]
        return [feed, feed + np.asarray((-0.16, -0.04, -0.02)), box_top]

    def _gun_prop(self):
        crew = self

        def draw(p, j2):
            yaw = j2['yaw']
            to_body = crew.g_spot.to_body
            path = C.belt_path(crew.belt_points(), 48)
            phase = -(crew.fire_t or 0.0) * 20 * 0.032 if crew.firing else 0.0
            C.draw_box(p, to_body, yaw, crew.box_at)
            C.draw_belt(p, to_body, yaw, path, crew.gun.a, phase)
            C.draw_mg42(p, to_body, yaw, crew.gun, crew.flash, seed=int((crew.fire_t or 0) * 12))
            if crew.firing:
                C.cases(p, to_body, yaw, crew.gun, crew.fire_t)
        draw.held = True
        return draw

    def _loader(self):
        sp, spot = C.LOADER, self.l_spot
        j = V.standing(sp)
        if self.loader == 'feed':
            lean = 14.0
            j['lean'] = lean
            j['footL'] = (-76.0, V.ANKLE_Y, 30.0)
            j['footR'] = (70.0, V.ANKLE_Y, -20.0)
            pts = self.belt_points()
            V.arm_to(j, 'R', spot.unlean(tuple(pts[1]), lean), 'down', 'fist')
            V.arm_to(j, 'L', spot.unlean(tuple(pts[2]), lean), 'down', 'fist')
            j['head_dy'] = 12
        elif self.loader == 'spot':
            lean = 4.0
            j['lean'] = lean
            for side, sg in (('L', -1), ('R', 1)):     # seen from behind (shot 2): the binoculars are hidden by his head,
                V.arm_to(j, side, (sg * 70.0, -60.0, 110.0), 'down', 'fist')   # so the hands show at the sides of it, not
            # wrapped round the back of the head with no hands (Sam, 27 Oct)
            j['face_props'] = [binoculars(lean)]
        else:                                          # pointing out of the slit, shouting
            lean = 6.0
            j['lean'] = lean
            V.arm_to(j, 'R', (-30.0, -190.0, 370.0), 'down', 'fist')
        return j

    def people(self):
        """[(spot, sp, joints)] for drawing."""
        lsp = dict(C.LOADER)
        if self.loader == 'point':
            lsp.update(mouth='v:AI', brows='alarm')
        elif self.loader == 'spot':
            lsp.update(brows='serious')
        gsp = dict(C.GUNNER, brows='fierce' if self.firing else 'serious')
        if self.firing:
            gsp['lid'] = 4
        return [(self.g_spot, gsp, self.jg), (self.l_spot, lsp, self.jl)]


def binoculars(lean):
    """6x30 field binoculars held to the eyes: two barrels pointing out from the face (end on from the front: two
    dark lenses), a hand on each side (drawn here, over them)."""
    def draw(p, j2):
        yaw = j2['yaw']
        if yaw in (135, 180):
            return
        tubes = []
        for sg in (-1, 1):
            a = V.project(V.leaned((sg * 20.0, -160.0, 70.0), lean), yaw)
            b = V.project(V.leaned((sg * 20.0, -166.0, 152.0), lean), yaw)
            tubes.append(((a[1] + b[1]) / 2, a[0], b[0]))
        tubes.sort()
        for _, a, b in tubes:
            dx, dy = b[0] - a[0], b[1] - a[1]
            n = math.hypot(dx, dy)
            if n < 20:
                p.ell(b[0], b[1], 21, 21, (30, 30, 32), INK, 2.0)
                p.ell(b[0], b[1], 13, 13, (60, 76, 92), INK, 1.4)
                p.ell(b[0] - 4, b[1] - 4, 4, 4, (170, 190, 206), None)
                continue
            nx, ny = -dy / n, dx / n
            p.poly([(a[0] + nx * 15, a[1] + ny * 15), (b[0] + nx * 19, b[1] + ny * 19), (b[0] - nx * 19, b[1] - ny * 19),
                    (a[0] - nx * 15, a[1] - ny * 15)], (36, 36, 38), INK, 2.0)
            p.line([(a[0] + dx * 0.3 + nx * 16, a[1] + dy * 0.3 + ny * 16), (a[0] + dx * 0.3 - nx * 16, a[1] + dy * 0.3 - ny * 16)],
                   (70, 70, 72), 1.6)
        for sd in 'LR':
            el, wr = j2['el' + sd], j2['wr' + sd]
            B.gesture_hand(p, el, wr, 'fist', C.LOADER['skin'])
    return draw


# ------------------------------------------------------------------------------------------------ cameras
REF = C.Spot(dict(name=None), 0.0, 0.0)


class View:
    """One camera on the world: yaw (0 from the beach, 180 from inside, 90 the side), the screen position of the
    world origin's neck height and a scale (screen pixels per 1.75 m person unit)."""
    def __init__(self, yaw, ox, oy, s0):
        self.yaw, self.ox, self.oy, self.s0 = yaw, ox, oy, s0
        self.deg, self.mirror = V.snap(yaw)
        self.flip = -1 if self.mirror else 1

    def pen(self, img, cam):
        return B.Pen(img, B.Local(cam, self.ox, self.oy, self.s0, self.flip))

    def body(self, W):
        return V.project(REF.to_body(W), self.deg)

    def screen(self, W):
        (px, py), dep = self.body(W)
        return self.ox + self.s0 * px * self.flip, self.oy + self.s0 * py, dep


def _with_hole(p, outer, hole, fill):
    """A flat shape with a hole in it (one keyhole polygon), outlined round both edges."""
    k = int(np.argmin([(x - hole[0][0]) ** 2 + (y - hole[0][1]) ** 2 for x, y in outer]))
    p.poly(outer[:k + 1] + hole + [hole[0]] + outer[k:], fill, None)
    p.poly(outer, None, INK, 2.4)
    p.poly(hole, None, INK, 2.4)


def _board_marks(p, v, z, x0, x1, y0, y1, seed):
    """The marks of the wooden formwork on a concrete face: faint horizontal lines and a few stains."""
    rng = np.random.default_rng(seed)
    y = y0 + 0.14
    while y < y1:
        a, b = v.body((x0 + 0.02, y, z))[0], v.body((x1 - 0.02, y + rng.uniform(-0.01, 0.01), z))[0]
        p.line([a, b], CONCRETE_D, 1.2)
        y += rng.uniform(0.14, 0.2)


def beach_layer(size, horizon, seed=4):
    """The beach seen from the bunker (refs lander-pov-4, mg42-2, -3): grey sky, the sea to a high horizon with ships,
    landing craft on the water, the surf line, wet then dry sand with steel hedgehogs, smoke. Screen space."""
    w, h = size
    img = Image.new('RGBA', size, SKY + (255,))
    cam = B.Cam(1.0, w / 2, h / 2)
    cam.P = lambda x, y: (x, y)
    cam.S = lambda v: v
    p = B.Pen(img, cam)
    rng = np.random.default_rng(seed)
    for k in range(4):                               # low cloud
        y = horizon - 60 - 50 * k
        x = rng.uniform(-100, w)
        p.poly(curve([(x, y), (x + 300, y - 20), (x + 620, y + 4), (x + 400, y + 26), (x + 60, y + 22)], 4), SKY_D, None)
    p.poly([(0, horizon), (w, horizon), (w, h), (0, h)], SEA, None)
    for k in range(8):                               # the fleet on the horizon
        x = rng.uniform(0, w)
        sw = rng.uniform(26, 60)
        p.poly([(x, horizon), (x + sw, horizon), (x + sw * 0.8, horizon - 8), (x + sw * 0.5, horizon - 8),
                (x + sw * 0.46, horizon - 18), (x + sw * 0.36, horizon - 18), (x + sw * 0.32, horizon - 8), (x + sw * 0.1, horizon - 6)],
               (70, 76, 80), None)
    surf = horizon + (h - horizon) * 0.42
    for k in range(5):                               # wave lines
        y = horizon + (surf - horizon) * (k + 1) / 6
        p.line([(0, y), (w * 0.3, y + 3), (w * 0.7, y - 2), (w, y + 2)], SEA_D, 1.4)
    for x, y, sc in ((w * 0.22, horizon + (surf - horizon) * 0.16, 0.45), (w * 0.64, horizon + (surf - horizon) * 0.3, 0.6)):   # out at sea, still coming in (Sam: on the beach they'd be unloading)
        craft(p, x, y, 120 * sc)
    p.poly(curve([(-20, surf), (w * 0.3, surf - 6), (w * 0.6, surf + 4), (w + 20, surf - 2), (w + 20, surf + 16),
                  (w * 0.6, surf + 20), (w * 0.3, surf + 10), (-20, surf + 16)], 3), SURF, None)
    wet = surf + 14
    p.poly([(0, wet), (w, wet), (w, h), (0, h)], WET, None)
    dry = wet + (h - wet) * 0.5
    p.poly(curve([(-20, dry), (w * 0.4, dry - 8), (w + 20, dry + 6), (w + 20, h + 20), (-20, h + 20)], 3), SAND, None)
    for k in range(18):                              # the steel hedgehogs, bigger as they come nearer
        y = rng.uniform(wet + 4, h - 10)
        x = rng.uniform(0, w)
        sz = 12 + 40 * (y - wet) / max(1, h - wet)
        hedgehog(p, x, y, sz, k)
    for k in range(3):                               # smoke from shell bursts, flat
        x = rng.uniform(w * 0.1, w * 0.9)
        y = rng.uniform(wet, dry)
        r = rng.uniform(16, 30)
        lumps = [(x + rng.uniform(-r, r), y - r * k * 0.9, r * rng.uniform(0.6, 1.0)) for k in range(4)]
        for cx, cy, rr in lumps:
            p.ell(cx, cy, rr, rr * 0.8, (120, 118, 116), None)
        for cx, cy, rr in lumps:
            p.ell(cx, cy, rr - 2, rr * 0.8 - 2, (176, 174, 170), None)
    return img


def craft(p, x, y, w):
    """A landing craft seen bow on: the boxy grey hull, the ramp up, a white bow wave."""
    h = w * 0.42
    p.poly(curve([(x - w * 0.9, y + h * 0.3), (x + w * 0.9, y + h * 0.3), (x + w * 0.6, y + h * 0.5),
                  (x - w * 0.6, y + h * 0.5)], 2), SURF, None)
    p.poly([(x - w * 0.5, y - h * 0.5), (x + w * 0.5, y - h * 0.5), (x + w * 0.56, y + h * 0.36), (x - w * 0.56, y + h * 0.36)],
           CRAFT, INK, 1.6)
    p.poly([(x - w * 0.34, y - h * 0.7), (x + w * 0.34, y - h * 0.7), (x + w * 0.38, y + h * 0.1), (x - w * 0.38, y + h * 0.1)],
           CRAFT_D, INK, 1.6)
    for k in range(3):
        p.line([(x - w * 0.3, y - h * 0.5 + k * h * 0.18), (x + w * 0.3, y - h * 0.5 + k * h * 0.18)], CRAFT, 1.2)


def hedgehog(p, x, y, sz, seed):
    """A Czech hedgehog: three steel beams crossed at the middle, standing on their ends."""
    rng = np.random.default_rng(seed)
    a0 = rng.uniform(0, 0.6)
    for k in range(3):
        a = a0 + k * math.pi / 3
        dx, dy = math.cos(a) * sz, math.sin(a) * sz * 0.8
        p.line([(x - dx, y - sz * 0.7 - dy * 0.6), (x + dx, y - sz * 0.7 + dy * 0.6)], IRON, max(2.0, sz * 0.12))


# ------------------------------------------------------------------------------------------------ the shots
def draw_person(img, cam, v, spot, sp, j, t):
    nx, ny, _ = v.screen(spot.to_world((0.0, 0.0, 0.0)))
    j = dict(j)
    j.pop('_dressed', None)
    return C.person(img, cam, nx, ny, v.s0, sp, t, v.yaw, j)


def inside(img, cam, v, crew, t=0.0, box=None):
    """From inside behind the crew: the inner face of the wall, the beach through the slit, the sill top, then them."""
    p = v.pen(img, cam)
    x0, x1 = SLIT_X
    zi, zo, sill = crew.z_in, crew.z_out, crew.sill
    img.alpha_composite(Image.new('RGBA', img.size, INSIDE + (255,)))
    inner = [v.screen((x, y, zi))[:2] for x, y in ((x0, sill), (x1, sill), (x1, SLIT_TOP), (x0, SLIT_TOP))]
    outer = [v.screen((x, y, zo))[:2] for x, y in ((x0, sill), (x1, sill), (x1, SLIT_TOP), (x0, SLIT_TOP))]
    allp = inner + outer
    bx0, by0 = int(min(a for a, _ in allp)) - 4, int(min(b for _, b in allp)) - 4
    bx1, by1 = int(max(a for a, _ in allp)) + 4, int(max(b for _, b in allp)) + 4
    lay = beach_layer((bx1 - bx0, by1 - by0), int((by1 - by0) * 0.34))
    mask = Image.new('L', lay.size, 0)
    ImageDraw.Draw(mask).polygon([(a - bx0, b - by0) for a, b in inner], fill=255)
    lay.putalpha(mask)
    img.alpha_composite(lay, (bx0, by0))
    for xr in (x0, x1):                              # the slit's side faces (only the one turned to us shows)
        p.poly([v.body(q)[0] for q in ((xr, sill, zi), (xr, sill, zo), (xr, SLIT_TOP, zo), (xr, SLIT_TOP, zi))],
               CONCRETE_D, INK, 2.0)
    p.poly([v.body(q)[0] for q in ((x0, SLIT_TOP, zi), (x1, SLIT_TOP, zi), (x1, SLIT_TOP, zo), (x0, SLIT_TOP, zo))],
           CONCRETE_D, INK, 2.0)
    # the sill's top, seen from above between the wall's two faces
    sill_top = [v.body(q)[0] for q in ((x0, sill, zi), (x1, sill, zi), (x1, sill, zo), (x0, sill, zo))]
    p.poly(sill_top, CONCRETE_L, INK, 2.0)
    # the inner face with the slit cut in it, the floor in front
    face = [v.body((x, y, zi))[0] for x, y in ((-2.6, 0.0), (2.0, 0.0), (2.0, 2.6), (-2.6, 2.6))]
    hole = [v.body((x, y, zi))[0] for x, y in ((x0, sill), (x0, SLIT_TOP), (x1, SLIT_TOP), (x1, sill))]
    floor = [v.body(q)[0] for q in ((-2.6, 0.0, zi), (2.0, 0.0, zi), (2.0, 0.0, -2.4), (-2.6, 0.0, -2.4))]
    p.poly(floor, (96, 94, 88), INK, 2.0)
    _with_hole(p, face, hole, INSIDE)
    _board_marks(p, v, zi, -2.6, x0, 0.0, 2.6, 1)
    _board_marks(p, v, zi, x1, 2.0, 0.0, 2.6, 2)
    order = sorted(crew.people(), key=lambda q: v.screen(q[0].to_world((0.0, 0.0, 0.0)))[2])
    for spot, sp, j in order:
        draw_person(img, cam, v, spot, sp, j, t)


def outside(img, cam, v, crew, t=0.0):
    """From the beach: the outer face of the bunker under its earth and grass, the crew in the dark slit, the gun on
    the sill pointing at us. The crew below the sill's inner edge are hidden by the sill."""
    p = v.pen(img, cam)
    x0, x1 = SLIT_X
    zi, zo, sill = crew.z_in, crew.z_out, crew.sill
    img.alpha_composite(Image.new('RGBA', img.size, SKY + (255,)))
    hole = [v.body((x, y, zo))[0] for x, y in ((x0, sill), (x0, SLIT_TOP), (x1, SLIT_TOP), (x1, sill))]
    p.poly(hole, DARK, None)
    back = [v.body((x, y, zi))[0] for x, y in ((x0, sill), (x0, SLIT_TOP), (x1, SLIT_TOP), (x1, sill))]
    p.poly(back, (40, 40, 44), None)
    # the crew, without the gun: drawn on their own layer and cut off below the sill's inner edge
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    gun_prop = crew.jg['props']
    jg = dict(crew.jg, props=[], grip=set())
    jg['hand'] = {'L': 'fist', 'R': 'fist'}
    people = [(crew.g_spot, crew.people()[0][1], jg), crew.people()[1]]
    for spot, sp, j in sorted(people, key=lambda q: v.screen(q[0].to_world((0.0, 0.0, 0.0)))[2]):
        draw_person(lay, cam, v, spot, sp, j, t)
    edge = [v.screen(q) for q in ((x0 - 0.5, sill, zi), (x1 + 0.5, sill, zi))]
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).polygon([(edge[0][0], edge[0][1]), (edge[1][0], edge[1][1]), (edge[1][0], 0), (edge[0][0], 0)], fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay.split()[3]), np.asarray(mask))))
    img.alpha_composite(lay)
    sill_top = [v.body(q)[0] for q in ((x0, sill, zi), (x1, sill, zi), (x1, sill, zo), (x0, sill, zo))]
    p.poly(sill_top, CONCRETE_L, INK, 2.0)
    # the gun, belt and box on the sill, drawn through the Gunner's frame
    gp = B.Pen(img, B.Local(cam, *v.screen(crew.g_spot.to_world((0.0, 0.0, 0.0)))[:2], C.scale_for(C.GUNNER, v.s0), v.flip))
    for draw in gun_prop:
        draw(gp, dict(yaw=v.deg))
    # the outer face, its earth bank and grass, the slit cut through it
    face = [v.body((x, y, zo))[0] for x, y in ((-2.8, -0.2), (2.4, -0.2), (2.4, 2.3), (-2.8, 2.3))]
    _with_hole(p, face, hole[::-1] if False else [hole[0], hole[3], hole[2], hole[1]], CONCRETE)
    _board_marks(p, v, zo, -2.8, x0, 0.0, 2.3, 3)
    _board_marks(p, v, zo, x1, 2.4, 0.0, 2.3, 4)
    _board_marks(p, v, zo, x0, x1, SLIT_TOP + 0.02, 2.3, 5)
    bank = [v.body((x, y, zo + dz))[0] for x, y, dz in ((-3.2, 2.2, 0), (-1.5, 2.5, -0.2), (0.4, 2.62, -0.3), (2.0, 2.4, -0.1),
                                                          (2.9, 2.1, 0.0), (2.9, 3.4, 0), (-3.2, 3.4, 0))]
    p.poly(curve(bank, 3), EARTH, INK, 2.2)
    rng = np.random.default_rng(7)
    for k in range(26):                              # grass tufts along the bank's edge
        x = rng.uniform(-3.0, 2.8)
        y = 2.3 + 0.28 * (1 - ((x + 0.5) / 3.2) ** 2)
        a = v.body((x, y, zo - 0.1))[0]
        for q in (-0.5, 0.0, 0.5):
            p.line([a, (a[0] + q * 30, a[1] - 60 - rng.uniform(0, 30))], GRASS_D, 3.0)
    ground = [v.body((x, y, zo + 0.4))[0] for x, y in ((-3.2, -0.3), (2.9, -0.3), (2.9, 0.25), (-3.2, 0.25))]
    p.poly(ground, GRASS, INK, 2.2)


def side(img, cam, v, crew, t=0.0):
    """From the side, the wall cut through at the gun (a section, like ref bunker-1): the room behind, the concrete
    below the sill and above the slit, the beach falling away outside; the crew and the gun on the sill."""
    p = v.pen(img, cam)
    zi, zo, sill = crew.z_in, crew.z_out, crew.sill
    X = SLIT_X[0]
    room = [v.body((X, y, z))[0] for y, z in ((0.0, -2.6), (0.0, zi), (2.4, zi), (2.4, -2.6))]
    p.poly(room, INSIDE, None)
    out = [v.body((X, y, z))[0] for y, z in ((-0.6, zo), (-0.6, zo + 2.6), (3.2, zo + 2.6), (3.2, zo))]
    p.poly(out, SKY, None)
    sand = [v.body((X, y, z))[0] for y, z in ((0.3, zo), (-0.6, zo + 2.6), (-0.8, zo + 2.6), (-0.8, zo))]
    p.poly(sand, SAND, INK, 2.0)
    floor = [v.body((X, y, z))[0] for y, z in ((0.0, -2.6), (0.0, zi), (-0.4, zi), (-0.4, -2.6))]
    p.poly(floor, CONCRETE_D, INK, 2.0)
    far = SLIT_X[1]
    p.poly([v.body(q)[0] for q in ((far, sill, zi), (far, sill, zo), (X, sill, zo), (X, sill, zi))], CONCRETE_L, INK, 2.0)
    p.poly([v.body(q)[0] for q in ((far, SLIT_TOP, zi), (far, SLIT_TOP, zo), (far, sill, zo), (far, sill, zi))], CONCRETE_D, INK, 2.0)
    for (y0, y1) in ((-0.4, sill), (SLIT_TOP, 2.4)):
        blk = [v.body((X, y, z))[0] for y, z in ((y0, zi), (y0, zo), (y1, zo), (y1, zi))]
        p.poly(blk, CONCRETE, INK, 2.4)
        a, b = v.body((X, y0, zi))[0], v.body((X, y1, zo))[0]
        for k in range(1, 9):                        # section hatching
            u = k / 9
            p.line([(a[0] + (b[0] - a[0]) * u, a[1]), (a[0], a[1] + (b[1] - a[1]) * u)], CONCRETE_D, 1.2)
    roof = [v.body((X, y, z))[0] for y, z in ((2.4, -2.6), (2.4, zo), (2.75, zo), (2.75, -2.6))]
    p.poly(roof, CONCRETE, INK, 2.4)
    bank = [v.body((X, y, z))[0] for y, z in ((2.75, -2.6), (2.75, zo), (2.5, zo + 0.6), (3.2, zo + 0.6), (3.2, -2.6))]
    p.poly(bank, EARTH, INK, 2.2)
    order = sorted(crew.people(), key=lambda q: v.screen(q[0].to_world((0.0, 0.0, 0.0)))[2])
    for spot, sp, j in order:
        draw_person(img, cam, v, spot, sp, j, t)


# ------------------------------------------------------------------------------------------------ sheet and clip
def _font(n):
    return ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)


def panel(draw, size, bg=(232, 228, 222)):
    img = Image.new('RGBA', size, bg + (255,))
    cam = B.Cam(1.0, size[0] / 2, size[1] / 2)
    cam.P = lambda x, y: (x, y)
    cam.S = lambda v: v
    draw(img, cam)
    return img


def sheet(out):
    """The crew and the MG42 on one sheet: from inside, from the beach, the side section; the Loader's three poses;
    the gun alone side on beside a 1 m ruler."""
    B.SS = 1
    W, H = 2700, 2000
    img = Image.new('RGBA', (W, H), (232, 228, 222, 255))
    d = ImageDraw.Draw(img)
    d.text((30, 18), 'PATRIOTS 3: the MG42 crew at the bunker slit (firing; the Loader feeding the belt)', font=_font(40),
           fill=(30, 30, 30))
    crew = Crew('feed', fire_t=0.25)
    panels = [('from inside, behind them', lambda im, cm: inside(im, cm, View(135, 470, 330, 0.36), crew)),
              ('from the beach', lambda im, cm: outside(im, cm, View(0, 520, 360, 0.36), crew)),
              ('from the side, the wall cut through', lambda im, cm: side(im, cm, View(90, 330, 330, 0.36), crew))]
    for i, (label, fn) in enumerate(panels):
        pim = panel(fn, (880, 1000))
        img.alpha_composite(pim, (20 + 893 * i, 80))
        d.text((20 + 893 * i + 440, 1100), label, font=_font(30), fill=(40, 40, 40), anchor='mm')
    for i, (pose, label) in enumerate((('feed', 'Loader feeds the belt'), ('spot', 'Loader with binoculars'),
                                       ('point', 'Loader points and shouts'))):
        c2 = Crew(pose)
        pim = panel(lambda im, cm, c2=c2: _pose_only(im, cm, c2), (600, 820))
        img.alpha_composite(pim, (20 + 610 * i, 1140))
        d.text((20 + 610 * i + 300, 1975), label, font=_font(28), fill=(40, 40, 40), anchor='mm')
    gim = panel(_gun_alone, (820, 820))
    img.alpha_composite(gim, (1860, 1140))
    d.text((2270, 1975), 'MG42 (1.22 m), ammo box, 1 m ruler', font=_font(28), fill=(40, 40, 40), anchor='mm')
    img.convert('RGB').save(out, quality=90)
    return out


def _pose_only(img, cam, crew):
    """The crew alone at three-quarter, the sill shown see-through (so their legs still show)."""
    v = View(30, 330, 260, 0.42)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    x0, x1 = SLIT_X
    pts = [v.screen((x, y, z))[:2] for x in (x0, x1) for y in (0.0, crew.sill) for z in (crew.z_in, crew.z_out)]
    B.Pen(lay, cam).poly(V._hull(pts), CONCRETE, INK, 2.0)
    lay.putalpha(lay.split()[3].point(lambda a: a * 0.4))
    img.alpha_composite(lay)
    order = sorted(crew.people(), key=lambda q: v.screen(q[0].to_world((0.0, 0.0, 0.0)))[2])
    for spot, sp, j in order:
        draw_person(img, cam, v, spot, sp, j, 0.0)


def _gun_alone(img, cam):
    v = View(90, 380, -60, 0.62)
    g = C.Gun((-0.5, 1.2, -0.62), (0, 0, 1))
    p = v.pen(img, cam)
    ground = float(np.mean([f[1][1] for f in C._bipod(g)]))
    C.draw_mg42(p, REF.to_body, v.deg, g)
    C.draw_box(p, REF.to_body, v.deg, (0.0, ground, 0.85))
    a, b = v.body((0, ground - 0.05, -0.62))[0], v.body((0, ground - 0.05, 0.38))[0]
    p.line([a, b], (90, 90, 90), 3.0)
    for k in range(11):
        u = k / 10
        x = a[0] + (b[0] - a[0]) * u
        p.line([(x, a[1] - (14 if k % 5 == 0 else 7)), (x, a[1])], (90, 90, 90), 2.0)


def clip(out, seconds=6.0, fps=12):
    """Silent test: 3 s from inside (the Loader feeding, the Gunner firing a burst from 0.6 s), 3 s from the beach."""
    import subprocess
    import tempfile
    B.SS = 1
    tmp = tempfile.mkdtemp()
    n = int(seconds * fps)
    for f in range(n):
        t = f / fps
        burst = t - 0.6 if t < 3.0 else t - 3.4
        crew = Crew('feed', fire_t=burst if burst >= 0 and (burst % 1.4) < 1.0 else None, t=t)
        if t < 3.0:
            im = panel(lambda i, c: inside(i, c, View(-135, 640, 700, 0.62), crew, t), (1080, 1920), bg=(40, 40, 40))
        else:
            im = panel(lambda i, c: outside(i, c, View(0, 600, 900, 0.62), crew, t), (1080, 1920), bg=SKY)
        im.convert('RGB').save(os.path.join(tmp, f'{f:04d}.png'))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(tmp, '%04d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', '-vf', 'fps=24', out], check=True)
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    elif sys.argv[1] == 'clip':
        print(clip(sys.argv[2]))
