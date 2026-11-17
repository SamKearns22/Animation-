#!/usr/bin/env python3
"""Milburn: the two new paintings (chat 2, 17 Nov). The Cabinet Room is the places kit (story/milburn-places.txt).

MAP
  helpers .......... SS (drawn at 2x, shrunk: smooth edges), ink polygons, mix, ease
  shaft ............ the lift shaft seen level from the rising platform (camera 1.6 m, 6 m from the shaft's middle):
                     the round concrete wall (rings above eye level bow up, below bow down), segment joints, two steel
                     guide rails, caged lamps; it all slides DOWN as the platform rises (RISE m/s); the light from the
                     opening above sweeps down the wall (light_line(t): the lit edge's height above the deck);
                     the deck with its hazard rim. SHAFT_CAM: where the people stand (metres -> screen)
  field ............ the field from above (camera 90 m up, 102 m back, looking down 28 deg; FIELD_CAM):
                     sky, two ranges of alpine peaks with snow, forested foothills, the forest ring (radius 300 m) as a
                     treeline band, the meadow inside it with wind waves running across (per frame, numpy), the
                     shaft's mouth (radius 8.5 m) at the middle with the platform rising up into it (deck_z(u))
  sheet ............ both paintings at three moments each, for a look

    python3 source/milburn_sets.py sheet OUT.jpg
"""
import math
import os
import random
import sys
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ed import INK                     # noqa: E402

W, H = 1080, 1920
SS = 2                                 # paintings drawn at twice the size and shrunk: smooth edges


def mix(a, b, u):
    return tuple(int(round(x + (y - x) * u)) for x, y in zip(a, b))


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def _poly(d, pts, fill, line=2.4, ink=INK):
    pts = [(x * SS, y * SS) for x, y in pts]
    d.polygon(pts, fill=fill)
    if line:
        d.line(pts + [pts[0]], fill=ink, width=max(1, int(round(line * SS))), joint='curve')


def _line(d, pts, fill, w):
    d.line([(x * SS, y * SS) for x, y in pts], fill=fill, width=max(1, int(round(w * SS))), joint='curve')


# ================================================================================================= the shaft
class LevelCam:
    """A level camera: height `up` m, horizon row, lens px; x across, d forward from the lens, z up (metres)."""
    def __init__(self, up, horizon, lens):
        self.up, self.hz, self.L = up, horizon, lens

    def p(self, x, d, z):
        return 540 + x * self.L / d, self.hz - (z - self.up) * self.L / d

    def ppm(self, d):
        return self.L / d


SHAFT_CAM = LevelCam(1.6, 1250, 2000)    # medium shot: the nearest one cut at the bottom of the torso, room above
R_SHAFT = 8.5                            # the shaft's radius (17 m across: ten people holding hands)
C_BACK = 6.0                             # the lens is 6 m from the shaft's middle (the camera stands on the deck)
RISE = 2.4                               # m/s: the wall slides down past them
CONCRETE = (92, 90, 92)
CONCRETE_LIT = (232, 214, 170)
DECK = (88, 92, 98)


def wall_pt(phi, z, cam=SHAFT_CAM):
    """A point on the shaft wall at angle phi (0 = straight ahead) and height z above the deck -> screen."""
    x, d = R_SHAFT * math.sin(phi), C_BACK + R_SHAFT * math.cos(phi)
    return cam.p(x, d, z)


def light_line(t, t0, t1):
    """The lit edge's height above the deck (m) as the light sweeps down the wall: from high above the frame at t0
    to just above their heads at t1."""
    return 14.0 - 11.4 * ease((t - t0) / max(0.01, t1 - t0))


def shaft(t, lit_z=14.0, travelled=None):
    """The shaft at time t (seconds into the rise): returns an RGB image. `lit_z`: the lit edge's height (m)."""
    cam = SHAFT_CAM
    big = Image.new('RGB', (W * SS, H * SS), (40, 40, 46))
    d = ImageDraw.Draw(big)
    off = (RISE * t if travelled is None else travelled)
    phis = [math.radians(a) for a in np.linspace(-68, 68, 69)]
    zs_top, zs_bot = 40.0, 0.0
    # the wall in vertical strips: dark below the lit edge, warm above it, a soft band between
    for i in range(len(phis) - 1):
        a0, a1 = phis[i], phis[i + 1]
        for z0, z1, col in ((zs_bot, lit_z - 0.6, CONCRETE), (lit_z - 0.6, lit_z, mix(CONCRETE, CONCRETE_LIT, 0.5)),
                            (lit_z, zs_top, CONCRETE_LIT)):
            if z1 <= z0:
                continue
            shade = 0.9 + 0.1 * math.cos((a0 + a1) / 2)            # the wall facing us is a touch lighter
            c = tuple(int(v * shade) for v in col)
            pts = [wall_pt(a0, z0), wall_pt(a1, z0), wall_pt(a1, z1), wall_pt(a0, z1)]
            _poly(d, pts, c, line=0)
    # ring joints every 1.5 m (they slide down as the deck rises): arcs, bowing up above eye level, down below
    step = 1.5
    k0 = math.floor((zs_bot + off) / step)
    for k in range(k0, k0 + 30):
        z = k * step - off
        if z < 0 or z > zs_top:
            continue
        col = (70, 68, 66) if z < lit_z else (170, 150, 116)
        _line(d, [wall_pt(a, z) for a in phis], col, 1.8)
    # segment joints every 15 deg, staggered by ring (a bricklaid tunnel lining)
    for k in range(k0, k0 + 30):
        z0, z1 = k * step - off, (k + 1) * step - off
        if z1 < 0 or z0 > zs_top:
            continue
        stag = 7.5 if k % 2 else 0.0
        for a in range(-75, 76, 15):
            ph = math.radians(a + stag)
            if abs(ph) > math.radians(68):
                continue
            zc = max(0.0, z0), min(zs_top, z1)
            col = (70, 68, 66) if zc[1] < lit_z else (170, 150, 116)
            _line(d, [wall_pt(ph, zc[0]), wall_pt(ph, zc[1])], col, 1.4)
    # two steel guide rails and caged lamps every 6 m on the rails' side
    for a in (-17.0, 17.0):
        ph = math.radians(a)
        for dph in (-0.8, 0.8):
            p0, p1 = wall_pt(math.radians(a + dph), 0), wall_pt(math.radians(a + dph), zs_top)
            _line(d, [p0, p1], INK, 2.2)
        pts = [wall_pt(math.radians(a - 0.8), 0), wall_pt(math.radians(a + 0.8), 0),
               wall_pt(math.radians(a + 0.8), zs_top), wall_pt(math.radians(a - 0.8), zs_top)]
        _poly(d, pts, (150, 150, 156), line=2.0)
        for k in range(-2, 12):
            z = k * 6.0 + 3.0 - (off % 6.0)
            if not 0.3 < z < zs_top:
                continue
            ph2 = math.radians(a + (3 if a > 0 else -3))
            X, Y = wall_pt(ph2, z)
            s = cam.ppm(C_BACK + R_SHAFT * math.cos(ph2)) * 0.16
            glow = (255, 236, 170) if z < lit_z else (255, 246, 214)
            _poly(d, [(X - s, Y - s * 1.4), (X + s, Y - s * 1.4), (X + s, Y + s * 1.4), (X - s, Y + s * 1.4)], glow, 1.8)
            _line(d, [(X - s, Y), (X + s, Y)], INK, 1.2)
            _line(d, [(X, Y - s * 1.4), (X, Y + s * 1.4)], INK, 1.2)
    # light from the opening: pale rays slanting down over the lit wall
    ray = Image.new('L', big.size, 0)
    rd = ImageDraw.Draw(ray)
    ly = wall_pt(0, lit_z)[1] * SS
    for k, x in enumerate((-260, 80, 420, 760, 1100)):
        x *= SS
        rd.polygon([(x, -10), (x + 180 * SS, -10), (x + 60 * SS, ly + 300 * SS), (x - 120 * SS, ly + 300 * SS)],
                   fill=36 + 10 * (k % 2))
    ray = ray.filter(ImageFilter.GaussianBlur(24 * SS))
    big = Image.composite(Image.new('RGB', big.size, (255, 250, 228)), big, ray)
    d = ImageDraw.Draw(big)
    # the deck: steel tread, the gap and the hazard rim along the far wall
    rim = [cam.p(R_SHAFT * 0.97 * math.sin(a), C_BACK + R_SHAFT * 0.97 * math.cos(a), 0) for a in phis]
    _poly(d, rim + [(1200, 1990), (-120, 1990)], DECK, line=2.6)
    for k in range(1, 9):                                         # tread lines running away from us
        x = -6 + k * 1.5
        _line(d, [cam.p(x, 2.4, 0), cam.p(x * 1.0, 14.0, 0)], (76, 80, 86), 1.0)
    band = [cam.p(R_SHAFT * 0.9 * math.sin(a), C_BACK + R_SHAFT * 0.9 * math.cos(a), 0) for a in phis]
    _poly(d, rim + band[::-1], (226, 186, 40), line=1.6)
    for i in range(0, len(phis) - 1, 2):                          # black chevrons on the rim
        a0, a1 = phis[i], phis[i + 1]
        q = [cam.p(R_SHAFT * r * math.sin(a), C_BACK + R_SHAFT * r * math.cos(a), 0)
             for r, a in ((0.97, a0), (0.97, a1), (0.9, (a0 + a1) / 2 + 0.03), (0.9, (a0 + a1) / 2 - 0.03))]
        _poly(d, q, (30, 30, 30), line=0)
    lit = max(0.0, min(1.0, (5.0 - lit_z) / 3.0))               # the light reaching the deck at the end
    out = big.resize((W, H), Image.LANCZOS)
    if lit > 0:
        out = Image.blend(out, Image.new('RGB', out.size, (255, 244, 210)), 0.12 * lit)
    return out


# ================================================================================================= the field
class TiltCam:
    """A camera `h` m up, `back` m behind the middle of the world (x across, y away, z up), pitched down `pitch` deg."""
    def __init__(self, h, back, pitch, lens):
        self.h, self.back, self.L = h, back, lens
        self.th = math.radians(pitch)
        self.f = (0.0, math.cos(self.th), -math.sin(self.th))
        self.u = (0.0, math.sin(self.th), math.cos(self.th))

    def p(self, x, y, z):
        rx, ry, rz = x, y + self.back, z - self.h
        fw = ry * self.f[1] + rz * self.f[2]
        up = ry * self.u[1] + rz * self.u[2]
        return 540 + self.L * rx / fw, 960 - self.L * up / fw, fw

    def horizon(self):
        return 960 - self.L * math.tan(self.th)

    def ground(self, X, Y):
        """Screen points (arrays) -> where their rays meet the ground (x, y); NaN above the horizon."""
        dx = (X - 540) / self.L
        dy = -(Y - 960) / self.L
        dirx = dx
        diry = self.f[1] + dy * self.u[1]
        dirz = self.f[2] + dy * self.u[2]
        with np.errstate(divide='ignore', invalid='ignore'):
            s = np.where(dirz < 0, -self.h / dirz, np.nan)
        return dirx * s, diry * s - self.back


FIELD_CAM = TiltCam(70.0, 79.0, 28.0, 1000.0)
R_RING = 300.0                         # the forest ring's inner edge (m from the shaft)
GRASS = ((84, 150, 62), (104, 172, 72), (132, 194, 86))
FOREST = (36, 86, 52)


def _peak_range(d, cam, dist, top, n, seed, col, snow, line):
    """A range of peaks `dist` m away, up to `top` m high, as one ridge polygon with snowcaps."""
    r = random.Random(seed)
    xs = np.linspace(-dist * 0.9, dist * 0.9, n)
    pts = []
    for i, x in enumerate(xs):
        z = (top * r.uniform(0.45, 1.0)) if i % 2 else top * r.uniform(0.18, 0.38)
        pts.append((x + r.uniform(-dist * 0.02, dist * 0.02), dist, z))
    scr = [cam.p(*q)[:2] for q in pts]
    base = cam.horizon() + 40
    _poly(d, [(scr[0][0], base)] + scr + [(scr[-1][0], base)], col, line)
    for i in range(1, len(scr) - 1, 2):                          # snow on each summit: down a third of its height
        (xa, ya), (xp, yp), (xb, yb) = scr[i - 1], scr[i], scr[i + 1]
        k = 0.34 + 0.08 * r.random()
        la = (xp + (xa - xp) * k, yp + (ya - yp) * k)
        lb = (xp + (xb - xp) * k, yp + (yb - yp) * k)
        mid = ((la[0] + lb[0]) / 2, (la[1] + lb[1]) / 2)
        teeth = [la, (la[0] + (mid[0] - la[0]) * 0.5, mid[1] - (mid[1] - yp) * 0.1), mid,
                 (mid[0] + (lb[0] - mid[0]) * 0.5, mid[1] + (lb[1] - mid[1]) * 0.3), lb]
        _poly(d, [(xp, yp)] + teeth[::-1], snow, line * 0.8)


def _tree(d, X, Y, s, kind, col, seed):
    """One tree standing at screen (X, Y) (its foot), s px per metre: a conifer (stacked tiers) or a round crown."""
    r = random.Random(seed)
    h = s * r.uniform(14, 22)
    if kind == 'fir':
        w = h * 0.36
        for k in range(3):
            y0 = Y - h * (0.25 + 0.25 * k)
            ww = w * (1 - 0.28 * k)
            _poly(d, [(X - ww, y0 + h * 0.16), (X + ww, y0 + h * 0.16), (X, y0 - h * 0.3)], mix(col, (0, 0, 0), 0.08 * k),
                  1.1)
    else:
        rr = h * 0.3
        cx, cy = X, Y - h * 0.62
        pts = [(cx + rr * (1 + 0.12 * math.sin(5 * a + seed)) * math.cos(a),
                cy + rr * 0.85 * (1 + 0.12 * math.sin(5 * a + seed)) * math.sin(a)) for a in np.linspace(0, 6.2, 18)]
        _poly(d, pts, mix(col, (60, 120, 50), 0.4), 1.1)


@lru_cache(None)
def _field_layers():
    """The still parts, drawn once: (back RGB: sky, peaks, hills, the forest beyond the ring) and (front RGBA: the
    treeline along the ring's inner edge, over the meadow)."""
    cam = FIELD_CAM
    hz = cam.horizon()
    back = Image.new('RGB', (W * SS, H * SS), (150, 200, 236))
    d = ImageDraw.Draw(back)
    for k, c in enumerate(((120, 178, 228), (138, 192, 234), (160, 206, 238), (184, 220, 240))):   # flat sky bands
        y0 = k * hz / 4
        _poly(d, [(0, y0), (W, y0), (W, hz + 60), (0, hz + 60)], c, line=0)
    for cx, cy, s in ((200, 130, 1.0), (760, 210, 0.8), (980, 90, 0.6)):                      # a few flat clouds
        for dx, dy, r in ((0, 0, 50), (46, -16, 38), (-44, 6, 34), (86, 8, 30)):
            d.ellipse([((cx + dx * s) - r * s) * SS, ((cy + dy * s) - r * s * 0.7) * SS,
                       ((cx + dx * s) + r * s) * SS, ((cy + dy * s) + r * s * 0.7) * SS], fill=(246, 250, 252))
    _peak_range(d, cam, 18000, 3900, 15, 4, (150, 166, 196), (246, 248, 252), 1.6)
    _peak_range(d, cam, 11000, 2500, 11, 9, (106, 124, 158), (236, 242, 250), 2.0)
    r = random.Random(3)                                                     # forested foothills, rolling
    for dist, col in ((3200, (54, 98, 82)), (1600, (44, 90, 64))):
        xs = np.linspace(-dist * 1.2, dist * 1.2, 40)
        pts = [cam.p(x, dist, 140 * (dist / 3200) * (0.5 + 0.5 * math.sin(x / dist * 7 + r.random())))[:2] for x in xs]
        _poly(d, pts + [(pts[-1][0], H), (pts[0][0], H)], col, 1.6)
    # the forest beyond the ring: dark ground from the ring out to the hills
    ring = [cam.p(R_RING * math.sin(a), R_RING * math.cos(a), 0)[:2] for a in np.linspace(-1.5, 1.5, 120)]
    _poly(d, [(-50, hz + 30)] + ring + [(1130, hz + 30)], FOREST, line=0)
    front = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    fd = ImageDraw.Draw(front)
    trees = []
    rr = random.Random(11)
    for row, rad in enumerate((R_RING + 40, R_RING + 22, R_RING + 8, R_RING)):
        n = 700
        for i in range(n):
            a = -1.4 + 2.8 * (i + rr.random()) / n
            x, y = rad * math.sin(a), rad * math.cos(a)
            X, Y, fw = cam.p(x, y, 0)
            if -40 < X < W + 40 and fw > 0:
                trees.append((fw, X, Y, cam.L / fw, 'fir' if rr.random() < 0.6 else 'oak', i * 7 + row))
    for fw, X, Y, s, kind, seed in sorted(trees, reverse=True):
        _tree(fd, X, Y, s, kind, mix(FOREST, (70, 130, 80), random.Random(seed).random() * 0.5), seed)
    return back.resize((W, H), Image.LANCZOS), front.resize((W, H), Image.LANCZOS)


@lru_cache(None)
def _ground_grid():
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    gx, gy = FIELD_CAM.ground(xs + 0.5, ys + 0.5)
    inside = np.nan_to_num(gx ** 2 + gy ** 2, nan=1e12) < R_RING ** 2
    return gx, gy, inside


def meadow(t):
    """The grass inside the ring at time t: three flat greens; gusts run across it from the left and far side."""
    gx, gy, inside = _ground_grid()
    a = math.radians(-30)
    u = gx * math.cos(a) + gy * math.sin(a)
    w = (np.sin(u * 0.045 - t * 1.9) + 0.45 * np.sin(u * 0.13 + gy * 0.03 - t * 2.9)
         + 0.25 * np.sin(gx * 0.9 + gy * 0.6 - t * 4.0))
    tone = np.where(w > 1.0, 2, np.where(w > -0.9, 1, 0))
    pal = np.array(GRASS, np.uint8)
    img = pal[tone]
    far = np.clip((np.nan_to_num(gy, nan=0) + 0) / R_RING, 0, 1)[..., None]            # a touch paler far off
    img = (img * (1 - 0.18 * far) + np.array((170, 200, 190)) * 0.18 * far).astype(np.uint8)
    return img, inside


def deck_z(u):
    """The platform's height (m, 0 = level with the grass) at share u of the rise: up from 9 m down, easing to a stop."""
    return -9.0 * (1 - ease(u)) ** 1.0


def mouth(img, z, t, figures=None):
    """The shaft's mouth at the middle of the field and the platform `z` m below the grass, seen from above."""
    cam = FIELD_CAM
    big = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    A = np.linspace(0, 2 * math.pi, 90)
    top = [cam.p(R_SHAFT * math.sin(a), R_SHAFT * math.cos(a), 0)[:2] for a in A]
    lip = [cam.p((R_SHAFT + 0.9) * math.sin(a), (R_SHAFT + 0.9) * math.cos(a), 0)[:2] for a in A]
    _poly(d, lip, (196, 192, 184), 2.0)                                     # the concrete lip on the grass
    _poly(d, top, (34, 34, 38), 1.6)                                        # the dark hole
    mask = Image.new('L', big.size, 0)
    ImageDraw.Draw(mask).polygon([(x * SS, y * SS) for x, y in top], fill=255)
    inner = Image.new('RGBA', big.size, (0, 0, 0, 0))
    di = ImageDraw.Draw(inner)
    if z < -0.02:
        far = [cam.p(R_SHAFT * math.sin(a), R_SHAFT * math.cos(a), zz)[:2]
               for zz, aa in ((0, None), (z, None)) for a in (np.linspace(-1.6, 1.6, 40) if zz == 0 else
                                                              np.linspace(1.6, -1.6, 40))]
        _poly(di, far, (150, 146, 140), 1.2)                                # the far inner wall, lit from above
        for k in range(1, 7):
            zz = -1.5 * k
            if zz > z:
                _line(di, [cam.p(R_SHAFT * math.sin(a), R_SHAFT * math.cos(a), zz)[:2]
                           for a in np.linspace(-1.6, 1.6, 30)], (110, 106, 102), 1.0)
    deck = [cam.p(R_SHAFT * 0.99 * math.sin(a), R_SHAFT * 0.99 * math.cos(a), z)[:2] for a in A]
    band = [cam.p(R_SHAFT * 0.9 * math.sin(a), R_SHAFT * 0.9 * math.cos(a), z)[:2] for a in A]
    _poly(di, deck, (226, 186, 40), 1.4)
    _poly(di, band, (110, 114, 120), 1.2)
    if figures:
        tiny_people(di, z, figures)
    big = Image.alpha_composite(big, Image.composite(inner, Image.new('RGBA', big.size, (0, 0, 0, 0)), mask))
    small = big.resize((W, H), Image.LANCZOS)
    img.alpha_composite(small) if img.mode == 'RGBA' else img.paste(small, (0, 0), small)
    return img


def tiny_people(d, z, figures):
    """Tiny people standing on the deck (z m), seen from above (F8: a few pixels each): `figures` is a list of
    (x, y, height m, top colour, hair colour, skin colour); far ones first. Drawn inside the shaft's mouth, so the
    near rim hides them until the deck comes up."""
    cam = FIELD_CAM
    for x, y, h, top, hair, skin in sorted(figures, key=lambda f: -f[1]):
        fx, fy, _ = cam.p(x, y, z)
        hx, hy, fw = cam.p(x, y, z + h)
        s = cam.L / fw
        r = 0.26 * s
        _poly(d, [(fx - r, fy), (fx + r, fy), (hx + r * 0.9, hy + r * 1.6), (hx - r * 0.9, hy + r * 1.6)], top, 0.6)
        d.ellipse([(hx - r * 0.7) * SS, (hy - r * 0.2) * SS, (hx + r * 0.7) * SS, (hy + r * 1.2) * SS], fill=skin,
                  outline=INK, width=1)
        d.ellipse([(hx - r * 0.75) * SS, (hy - r * 0.35) * SS, (hx + r * 0.75) * SS, (hy + r * 0.5) * SS], fill=hair)


def field(t, z, figures=None):
    """The whole field picture at time t with the platform at height z; `figures`: the tiny people (tiny_people)."""
    back, front = _field_layers()
    g, inside = meadow(t)
    base = np.array(back)
    base[inside] = g[inside]
    img = Image.fromarray(base).convert('RGBA')
    img.alpha_composite(front)
    mouth(img, z, t, figures)
    return img.convert('RGB')


def field_point(x, y, z):
    """World metres in the field -> screen (X, Y) and px per metre there."""
    X, Y, fw = FIELD_CAM.p(x, y, z)
    return X, Y, FIELD_CAM.L / fw


def sheet(out):
    tiles = [shaft(0.0, 14.0), shaft(1.5, 8.0), shaft(3.0, 2.6),
             field(0.0, deck_z(0.0)), field(1.5, deck_z(0.5)), field(3.0, deck_z(1.0))]
    s = Image.new('RGB', (3 * 360, 2 * 640), (230, 228, 222))
    for i, im in enumerate(tiles):
        s.paste(im.resize((360, 640)), ((i % 3) * 360, (i // 3) * 640))
    s.save(out, quality=86)
    return out


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    else:
        print(__doc__)
