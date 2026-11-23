#!/usr/bin/env python3
"""gta_cars: the getaway Declasse Tulip and the VCPD cruiser as 3D solids (metres, y up), copied from the game's
pictures in references/grand-theft-autism/ (Grand Theft Autism, chat 5). Any camera, any angle; the body leans
on its wheels (roll, pitch) while the wheels stay on the road; front wheels steer, all wheels turn.

MAP
  colours ........... TULIP_*, COP_*, CHROME, GLASS, TYRE, LIGHT (the sun's way)
  SPECS ............. each car's numbers: body stations, greenhouse, wheels, seats (who sits where)
  class Car ......... one car's state at a moment: where, which way, lean, steer, wheel turn, crash (crush, shatter)
  local_pt/solid_at . a world point back in the car's frame; which solid part of the car it is inside (for
                      viewchecks.solid_faults: the cabin is air, an OPEN window is a hole, glass is solid)
  _body/_house ...... the two convex solids (lower body, glass house), built in the car's own frame
  _tulip_decals ..... stripes, weathering, grille, round lamps, door seams, handles, chrome, plates, tail lamps
  _cop_decals ....... blue side stripe, POLICE, badge, black grille, swept lamps, VICE CITY POLICE on the boot
  _parts ............ bumpers, mirrors, push bar, light bar: each tied to the body face it sits on (draw order)
  _wheel ............ tyre and rim seen from anywhere; lug nuts turn with the wheel
  cover_masks ....... what of the car is between the lens and a point (to rub out someone leaning out of it)
  draw_car .......... shadow, then parts behind, body, parts in front, glass with the people inside seen through
  glow / paste_quad . soft light (lamps, light bar); a picture (lettering) laid on a 3D quad
  sheet ............. both cars from every side the film uses, the crashed cruiser, beside the game pictures

    python3 source/gta_cars.py sheet OUT.jpg
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import body as B                 # noqa: E402  the one kit (burnham kept its own SS: the street drew at half size, chat 13)
import sets as S                 # noqa: E402
from ed import INK               # noqa: E402

ROOT = os.path.dirname(HERE)
REFS = os.path.join(ROOT, 'references', 'grand-theft-autism')
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

# ------------------------------------------------------------------------------------------------ colours
TULIP_RED = (190, 62, 48)
TULIP_FADE = (210, 96, 78)        # sun-faded patches (the game's car is worn pink on the flanks and bonnet)
TULIP_DEEP = (150, 42, 36)
STRIPE = (58, 50, 52)               # weathered black paint (pure black read as holes from above)
STRIPE_EDGE = (120, 74, 70)         # the worn edge where the red shows through
STRIPE_SHINE = (98, 90, 98)        # the sky's shine on the black stripes (chat 33b, F15)
TULIP_SHINE = (222, 112, 96)       # the same shine on the red
VINYL = (52, 48, 42)
CHROME = (206, 212, 218)
CHROME_DK = (150, 148, 142)
GLASS = (58, 74, 84)
GLASS_HI = (132, 150, 160)
CABIN = (46, 40, 44)               # the dark cabin seen through a wound-down window
TYRE = (34, 33, 35)
STEEL = (78, 78, 80)
GRILLE = (30, 30, 32)
COP_WHITE = (240, 240, 236)
COP_BLUE = (34, 58, 128)
COP_BLACK = (30, 30, 34)
RED_LAMP = (196, 30, 36)
RED_LIT = (255, 70, 60)
BLUE_LAMP = (30, 60, 190)
BLUE_LIT = (90, 150, 255)
AMBER = (232, 150, 40)
LIGHT = S._norm((-0.55, 0.62, 0.56))     # low sunset sun from behind the camera's left (set by the film per shot)
EPS = 0.006


# ------------------------------------------------------------------------------------------------ the cars' numbers
SPECS = {
    # 1970s four-door hardtop (the trailer's car): long bonnet, formal vinyl roof, flat sides, chrome bumpers
    'tulip': dict(
        stations=[(-2.64, 0.93, 0.33, 0.90), (-2.48, 1.0, 0.26, 0.95), (2.40, 1.0, 0.26, 0.93), (2.64, 0.96, 0.30, 0.89)],
        half_w=0.985, bevel=0.10, top_in=0.92,
        house=dict(base=(-1.98, 0.80), roof=(-1.12, 0.30), hw=(0.86, 0.70), y=(0.95, 1.47)),  # roof +14 cm (Sam Y to ~10, chat 13; +4 more and the cast sat 6 cm lower, chat 14: heads clear the rail)
        wheels=dict(z=(1.44, -1.52), x=0.90, r=0.34, w=0.28),
        seats=[(-0.42, 0.10, 'driver'), (0.42, 0.10, 'front'), (0.0, -0.80, 'back')],
        body=TULIP_RED, house_col=VINYL),
    # 2010s police saloon (the game's VCPD car): high waist, sloping screen, white with a blue stripe, light bar
    'cruiser': dict(
        stations=[(-2.58, 0.86, 0.42, 0.92), (-2.50, 0.96, 0.34, 1.02), (-2.30, 1.0, 0.30, 1.06), (1.40, 1.0, 0.30, 1.04),
                  (2.10, 0.99, 0.30, 0.98), (2.40, 0.95, 0.33, 0.90), (2.56, 0.86, 0.42, 0.80)],
        half_w=0.97, bevel=0.12, top_in=0.90,
        house=dict(base=(-1.86, 1.08), roof=(-1.18, -0.02), hw=(0.86, 0.69), y=(1.05, 1.55)),
        wheels=dict(z=(1.50, -1.40), x=0.86, r=0.37, w=0.24),
        seats=[(-0.42, 0.0, 'driver'), (0.42, 0.0, 'front')],
        body=COP_WHITE, house_col=COP_BLACK),
}


# ------------------------------------------------------------------------------------------------ a car's state
class Car:
    """One car at one moment. pos (x, z) on the road, yaw in degrees (0 = north, 90 = east, the sets' handedness),
    roll (+ leans to its own right), pitch (+ nose up), steer (front wheels, + to its right), spin (wheel turn,
    radians), crush (0-1, the front pushed in), shatter (0-1, the windscreen crazed), lamps (the light bar on)."""
    def __init__(self, kind, pos=(0.0, 0.0), yaw=0.0, roll=0.0, pitch=0.0, steer=0.0, spin=0.0, crush=0.0,
                 shatter=0.0, lamps=True, lift=0.0):
        self.kind, self.spec = kind, SPECS[kind]
        self.pos, self.yaw, self.roll, self.pitch, self.steer = pos, yaw, roll, pitch, steer
        self.spin, self.crush, self.shatter, self.lamps, self.lift = spin, crush, shatter, lamps, lift

    def body_pt(self, p):
        """Car frame (x right, y up, z forward) to the world, with the body's lean (about its own centre line)."""
        x, y, z = p
        r, q = math.radians(self.roll), math.radians(self.pitch)
        yc = 0.55
        x, y = x * math.cos(r) - (y - yc) * math.sin(r), x * math.sin(r) + (y - yc) * math.cos(r) + yc
        y, z = (y - yc) * math.cos(q) + z * math.sin(q) + yc, -(y - yc) * math.sin(q) + z * math.cos(q)
        w = S.rot_y((x, y + self.lift, z), self.yaw)
        return (self.pos[0] + w[0], w[1], self.pos[1] + w[2])

    def ground_pt(self, p):
        w = S.rot_y(p, self.yaw)
        return (self.pos[0] + w[0], w[1], self.pos[1] + w[2])

    def body_dir(self, v):
        o = self.body_pt((0, 0, 0))
        e = self.body_pt(v)
        return (e[0] - o[0], e[1] - o[1], e[2] - o[2])


def local_pt(car, w):
    """A world point in the car's own frame (the inverse of Car.body_pt)."""
    v = S.rot_y((w[0] - car.pos[0], w[1], w[2] - car.pos[1]), -car.yaw)
    yc = 0.55
    r, q = math.radians(car.roll), math.radians(car.pitch)
    Y, zz = v[1] - car.lift - yc, v[2]
    a = Y * math.cos(q) - zz * math.sin(q)
    z = Y * math.sin(q) + zz * math.cos(q)
    x = v[0] * math.cos(r) + a * math.sin(r)
    b = -v[0] * math.sin(r) + a * math.cos(r)
    return (x, b + yc, z)


def solid_at(car, w, open_windows=(), wall=0.07):
    """Which solid part of the car the world point w is inside, or None (outside, or in the cabin's air). The cabin
    runs between the glass house's base ends above the floor; door walls are `wall` thick; the house's shell is
    solid except an open side window (open_windows: (side, pane) with side +1 the car's right, pane 1 the front)."""
    x, y, z = local_pt(car, w)
    st = _stations(car)
    h = car.spec['house']
    (zb0, zb1), (zr0, zr1), (wb, wr), (yb, yr) = h['base'], h['roof'], h['hw'], h['y']
    who = 'the ' + car.kind
    if st[0][0] <= z <= st[-1][0] and abs(x) < half_w(car, z) and _interp(st, z, 2) - 0.05 < y < top_y(car, z):
        cabin = zb0 + 0.06 < z < zb1 - 0.06 and abs(x) < half_w(car, z) - wall and y > 0.27
        if cabin:
            return None
        if y <= 0.27 and zb0 < z < zb1:
            return who + "'s floor"
        if abs(x) >= half_w(car, z) - wall and zb0 < z < zb1:
            return who + "'s door"
        return who + ("'s bonnet" if z > 0 else "'s boot")
    v = (y - yb) / (yr - yb)
    if 0 <= v <= 1:
        zf, zk = zb1 + (zr1 - zb1) * v, zb0 + (zr0 - zb0) * v
        hw = wb + (wr - wb) * v
        if zk <= z <= zf and abs(x) <= hw:
            sh = 0.05
            if v > 1 - sh / (yr - yb):
                return who + "'s roof"
            if z > zf - sh:
                return who + "'s windscreen"
            if z < zk + sh:
                return who + "'s back screen"
            if abs(x) > hw - sh:
                u = (z - zk) / (zf - zk)
                wins = [(0.20, 0.50), (0.52, 0.94)] if car.kind == 'tulip' else [(0.10, 0.20), (0.23, 0.53), (0.57, 0.95)]
                side = 1 if x > 0 else -1
                for k, (u0, u1) in enumerate(wins):
                    if u0 <= u <= u1 and 0.10 <= v <= 0.90:
                        if (side, k) in open_windows:
                            return None
                        return who + "'s side window (glass)"
                return who + "'s window pillar"
    return None


def _stations(car):
    st = [list(s) for s in car.spec['stations']]
    c = car.crush
    if c > 0:                      # the front shoved back and the bonnet buckled up into a ridge
        st[-1][0] -= 0.62 * c
        st[-2][0] -= 0.42 * c
        st[-1][1] -= 0.08 * c
        st[-1][3] += 0.04 * c
        zr = st[-2][0] - 0.35 - 0.1 * c
        ridge = [zr, 1.0, st[-2][2], st[-2][3] + 0.22 * c]
        st.insert(len(st) - 2, ridge)
        st.sort(key=lambda s: s[0])
    return st


def _profile(spec, wscale, yb, yt):
    hw, bev, ti = spec['half_w'] * wscale, spec['bevel'], spec['top_in']
    return [(hw, yb), (hw, yt - bev), (hw * ti, yt), (-hw * ti, yt), (-hw, yt - bev), (-hw, yb)]


def _interp(st, z, k):
    if z <= st[0][0]:
        return st[0][k]
    for a, b in zip(st, st[1:]):
        if a[0] <= z <= b[0]:
            u = (z - a[0]) / ((b[0] - a[0]) or 1)
            return a[k] + (b[k] - a[k]) * u
    return st[-1][k]


def top_y(car, z):
    return _interp(_stations(car), z, 3)


def half_w(car, z):
    return car.spec['half_w'] * _interp(_stations(car), z, 1)


# ------------------------------------------------------------------------------------------------ shading
def shade(col, n, k=0.34):
    d = S._dot(S._norm(n), LIGHT)
    up = max(0.0, n[1]) * 0.06
    f = 0.84 + k * 0.7 * max(0.0, d) - 0.07 * max(0.0, -d) + up
    return tuple(max(0, min(255, int(v * f))) for v in col[:3])


def _outward(pts, centre):
    a, b, c = pts[0], pts[1], pts[2]
    n = S._norm(S._cross(S._sub(b, a), S._sub(c, a)))
    mid = tuple(sum(q[i] for q in pts) / len(pts) for i in range(3))
    if S._dot(n, S._sub(mid, centre)) < 0:
        n = (-n[0], -n[1], -n[2])
    return n


def _solid(car, local_faces, centre_local):
    """local_faces: [(pts, colour, tag)] -> world Faces, shaded, each with its normal (convex: no sorting needed)."""
    centre = car.body_pt(centre_local)
    out = []
    for pts, col, tag in local_faces:
        w = [car.body_pt(p) for p in pts]
        n = _outward(w, centre)
        f = S.Face(w, n, shade(col, n), INK, 2.2)
        f.tag = tag
        out.append(f)
    return out


def _body(car):
    spec = car.spec
    st = _stations(car)
    rings = [[(x, y, z) for x, y in _profile(spec, ws, yb, yt)] for z, ws, yb, yt in st]
    if car.crush > 0:
        for k, extra in ((-1, 0.34), (-2, 0.18)):
            rings[k] = [(x, y, z - extra * car.crush * (x > 0)) for x, y, z in rings[k]]
    faces = []
    tags = ['right', 'rbevel', 'top', 'lbevel', 'left', 'under']
    for ra, rb in zip(rings, rings[1:]):
        for i in range(6):
            j = (i + 1) % 6
            col = spec['body'] if tags[i] != 'under' else (40, 36, 36)
            faces.append(([ra[i], ra[j], rb[j], rb[i]], col, tags[i]))
    faces.append((rings[0], spec['body'], 'back'))
    faces.append((rings[-1], spec['body'], 'front'))
    return _solid(car, faces, (0.0, 0.62, (st[0][0] + st[-1][0]) / 2))


def _house_pts(car):
    h = car.spec['house']
    (zb0, zb1), (zr0, zr1), (wb, wr), (yb, yr) = h['base'], h['roof'], h['hw'], h['y']
    if car.crush > 0:
        zb1 -= 0.25 * car.crush
    def P(side, u, v):
        z = (zb0 + (zr0 - zb0) * v) + ((zb1 + (zr1 - zb1) * v) - (zb0 + (zr0 - zb0) * v)) * u
        return (side * (wb + (wr - wb) * v), yb + (yr - yb) * v, z)
    return P


def _house(car):
    P = _house_pts(car)
    col = car.spec['house_col']
    faces = [
        ([P(-1, 0, 1), P(1, 0, 1), P(1, 1, 1), P(-1, 1, 1)], col, 'roof'),
        ([P(-1, 1, 0), P(1, 1, 0), P(1, 1, 1), P(-1, 1, 1)], col, 'screen'),
        ([P(-1, 0, 0), P(1, 0, 0), P(1, 0, 1), P(-1, 0, 1)], col, 'rearscreen'),
        ([P(1, 0, 0), P(1, 1, 0), P(1, 1, 1), P(1, 0, 1)], col, 'hright'),
        ([P(-1, 0, 0), P(-1, 1, 0), P(-1, 1, 1), P(-1, 0, 1)], col, 'hleft'),
    ]
    h = car.spec['house']
    return _solid(car, faces, (0.0, (h['y'][0] + h['y'][1]) / 2, sum(h['base']) / 2))


# ------------------------------------------------------------------------------------------------ decals
class Decal:
    """A flat shape laid on the car (car frame points, already on the surface); n_local is the surface's way out.
    kind 'poly' (fill, line), 'glass' (a window: the people inside show through it), 'text' (a picture on a quad),
    'lamp' (a light: glows when lit)."""
    def __init__(self, pts, n_local, fill, line=None, lw=1.2, kind='poly', pic=None, glow=None):
        self.pts, self.n_local, self.fill, self.line, self.lw = pts, n_local, fill, line, lw
        self.kind, self.pic, self.glow = kind, pic, glow


def _side_pt(car, side, z, y):
    return (side * (half_w(car, z) + EPS), y, z)


def _top_pt(car, x, z):
    return (x, top_y(car, z) + EPS, z)


def _end_z(car, front):
    st = _stations(car)
    return st[-1][0] + EPS if front else st[0][0] - EPS


def _ring2(cx, cy, r, n=18, ry=None):
    ry = ry or r
    return [(cx + r * math.cos(a), cy + ry * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]


def _arch(car, side, zc):
    w = car.spec['wheels']
    r = w['r'] + 0.085
    sill = car.spec['stations'][1][2]
    a0 = math.asin(max(-1, min(1, (sill - w['r']) / r)))
    pts = []
    for a in np.linspace(a0, math.pi - a0, 16):
        pts.append(_side_pt(car, side, zc + r * math.cos(a), w['r'] + r * math.sin(a)))
    return Decal(pts, (side, 0, 0), (26, 22, 22), INK, 1.8)


def arch_mask(car, cam, side, zc, size, pad=0.01):
    """Where a near-side wheel may show (canvas mask, 255): its arch in the body's side, open down to the road (GTA
    v5 note 6: the wheel was drawn whole over the wing). The arch is the one _arch draws, a little wider (pad)."""
    from PIL import ImageDraw
    w = car.spec['wheels']
    r = w['r'] + 0.085 + pad
    sill = car.spec['stations'][1][2]
    a0 = math.asin(max(-1, min(1, (sill - w['r']) / r)))
    yz = [(w['r'] + r * math.sin(a), zc + r * math.cos(a)) for a in np.linspace(a0, math.pi - a0, 24)]
    yz += [(sill, zc - 3 * r), (-0.6, zc - 3 * r), (-0.6, zc + 3 * r), (sill, zc + 3 * r)]   # nothing of the body
    m = Image.new('L', size, 0)                                       # is below the sill: the tyre shows whole there
    dr = ImageDraw.Draw(m)
    # the arch cut in the body's side: what of the wheel is outside it (a steered wheel swung out, a near wheel seen
    # from close behind) is behind the wing and the door
    xs = half_w(car, zc) + EPS
    q = cam.clip([car.body_pt((side * xs, y, z)) for y, z in yz])
    if len(q) > 2:
        dr.polygon([(x * B.SS, y * B.SS) for x, y in q], fill=255)
    # under the sill the tyre is in the open: its tread seen from in front or behind, through the wheel's width
    # (only then: seen from the side the tread's box would show under the sill as a black block)
    c0 = np.asarray(car.body_pt((side * xs, w['r'], zc)), float)
    nrm = np.asarray(car.body_pt((side * (xs + 1.0), w['r'], zc)), float) - c0
    to_cam = np.asarray(cam.pos, float) - c0
    if float(nrm @ to_cam) / (np.linalg.norm(nrm) * np.linalg.norm(to_cam) + 1e-9) > 0.45:
        return m
    pts = []
    for xa in (w['x'] - w['w'] / 2, max(xs, w['x'] + w['w'] / 2)):
        q = cam.clip([car.body_pt((side * xa, y, z)) for y, z in ((sill, zc - r), (sill, zc + r), (-0.6, zc + r), (-0.6, zc - r))])
        pts += [(x * B.SS, y * B.SS) for x, y in q]
    if len(pts) > 2:
        from scipy.spatial import ConvexHull
        try:
            h = ConvexHull(np.asarray(pts))
            dr.polygon([tuple(pts[i]) for i in h.vertices], fill=255)
        except Exception:
            pass
    return m


def _ragged(x0, x1, z0, z1, seed, step=0.22, amt=0.007):
    """A worn stripe edge: never ruler-straight."""
    rng = np.random.RandomState(seed)
    zs = list(np.arange(z0, z1, step)) + [z1]
    left = [(x0 + rng.uniform(-amt, amt), z) for z in zs]
    right = [(x1 + rng.uniform(-amt, amt), z) for z in reversed(zs)]
    return left + right


def _tulip_decals(car):
    d = []
    st = _stations(car)
    zf, zb = st[-1][0], st[0][0]
    yt = st[1][3]
    H = car.spec['house']
    for s in (-1, 1):
        # wheel arches, door seams, handles, the long chrome sill strip, side lamps
        for zc in car.spec['wheels']['z']:
            d.append(_arch(car, s, zc))
        for zc in (0.86, -0.36, -1.30):
            d.append(Decal([_side_pt(car, s, zc, 0.33), _side_pt(car, s, zc + 0.012, yt - 0.10)], (s, 0, 0), None, INK, 1.4, 'line'))
        for zc in (0.30, -0.80):
            d.append(Decal([_side_pt(car, s, zc, 0.74), _side_pt(car, s, zc + 0.16, 0.74), _side_pt(car, s, zc + 0.16, 0.77),
                            _side_pt(car, s, zc, 0.77)], (s, 0, 0), CHROME, INK, 1.0))
        d.append(Decal([_side_pt(car, s, 1.08, 0.335), _side_pt(car, s, -0.95, 0.335), _side_pt(car, s, -0.95, 0.36),
                        _side_pt(car, s, 1.08, 0.36)], (s, 0, 0), CHROME, INK, 0.9))
        d.append(Decal([_side_pt(car, s, 2.28, 0.60), _side_pt(car, s, 2.40, 0.60), _side_pt(car, s, 2.40, 0.66),
                        _side_pt(car, s, 2.28, 0.66)], (s, 0, 0), AMBER, INK, 0.9, 'lamp'))
        d.append(Decal([_side_pt(car, s, -2.30, 0.62), _side_pt(car, s, -2.42, 0.62), _side_pt(car, s, -2.42, 0.68),
                        _side_pt(car, s, -2.30, 0.68)], (s, 0, 0), RED_LAMP, INK, 0.9))
        # sun-faded flanks (the game's car is worn pink along the doors and the rear wing)
        for z0, z1, y0, y1 in ((-0.70, 0.90, 0.50, 0.86), (-2.30, -1.20, 0.56, 0.90), (1.10, 2.25, 0.66, 0.90)):
            rng = np.random.RandomState(int(abs(z0 * 100)) + (3 if s > 0 else 7))
            pts = []
            for a in np.linspace(0, 2 * math.pi, 16, endpoint=False):
                k = rng.uniform(0.55, 1.0)
                pts.append(_side_pt(car, s, (z0 + z1) / 2 + (z1 - z0) / 2 * k * math.cos(a), (y0 + y1) / 2 + (y1 - y0) / 2 * k * math.sin(a)))
            d.append(Decal(pts, (s, 0, 0), TULIP_FADE, None, 0))
    for s in (-1, 1):            # the hip line: dips along the doors, kicks up over the rear wheel (the muscle-car curve)
        zs = np.linspace(2.35, -2.40, 24)
        def crest(z):
            return 0.80 - 0.07 * math.exp(-((z + 0.2) / 1.0) ** 2) + 0.06 * math.exp(-((z + 1.55) / 0.55) ** 2)
        top = [_side_pt(car, s, z, crest(z)) for z in zs]
        low = [_side_pt(car, s, z, crest(z) - 0.07) for z in reversed(zs)]
        d.append(Decal(top + low, (s, 0, 0), TULIP_DEEP, None, 0))
        d.append(Decal(top, (s, 0, 0), None, INK, 1.3, 'line'))
    for z0, z1, x0, x1, sd in ((1.10, 2.10, -0.80, -0.10, 31), (0.95, 1.60, 0.35, 0.85, 37), (-2.45, -2.05, -0.75, 0.20, 41)):
        rng = np.random.RandomState(sd)
        pts = [_top_pt(car, (x0 + x1) / 2 + (x1 - x0) / 2 * rng.uniform(0.6, 1.0) * math.cos(a),
                       (z0 + z1) / 2 + (z1 - z0) / 2 * rng.uniform(0.6, 1.0) * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 14, endpoint=False)]
        d.append(Decal(pts, (0, 1, 0), TULIP_FADE, None, 0))
    # the two weathered black stripes on the bonnet and the boot, and a faded patch on the bonnet
    for x0, x1 in ((-0.36, -0.11), (0.11, 0.36)):       # Sam 22 Nov (F15, his 1): 25 cm each, a wider red gap
        for z0, z1, seed in ((H['base'][1] + 0.04, zf - 0.03, 11), (zb + 0.03, H['base'][0] - 0.04, 23)):
            pts = [_top_pt(car, x, z) for x, z in _ragged(x0, x1, z0, z1, seed + int(x0 * 10))]
            d.append(Decal(pts, (0, 1, 0), STRIPE, STRIPE_EDGE, 1.6))
            # chips where the red shows through, along the stripe's edges (chat 33b, F15: the grey patches in the
            # middle read as pockets and the stripes as a pair of trousers lying on the bonnet)
            rng = np.random.RandomState(seed + 5 + int(x1 * 10))
            for k in range(3):
                zc = rng.uniform(z0 + 0.15, z1 - 0.15)
                xe, inw = (x0, 1) if k % 2 == 0 else (x1, -1)
                pts = [_top_pt(car, xe + inw * 0.022 * (1 + math.cos(a)) * rng.uniform(0.6, 1.0), zc + 0.05 * math.sin(a))
                       for a in np.linspace(0, 2 * math.pi, 7, endpoint=False)]
                d.append(Decal(pts, (0, 1, 0), STRIPE_EDGE, None, 0))
    # one shine across the whole bonnet, over the stripes and the red alike: the stripes read as paint on a glossy
    # panel, not as cloth lying on it (chat 33b, F15). Split at the stripes' edges so each piece keeps its own colour.
    zb0, zb1 = H['base'][1] + 0.04, zf - 0.03
    zm = zb0 + 0.42 * (zb1 - zb0)
    hw = half_w(car, zm) * 0.93
    cuts = [-hw, -0.36, -0.11, 0.11, 0.36, hw]
    for w0, w1 in ((0.0, 0.10), (0.15, 0.18)):          # a broad band and a thin one beside it
        for i in range(len(cuts) - 1):
            xa, xb = cuts[i], cuts[i + 1]
            on_stripe = i in (1, 3)
            zz = lambda x, w: zm + 0.18 * x + w
            pts = [_top_pt(car, xa, zz(xa, w0)), _top_pt(car, xb, zz(xb, w0)), _top_pt(car, xb, zz(xb, w1)),
                   _top_pt(car, xa, zz(xa, w1))]
            d.append(Decal(pts, (0, 1, 0), STRIPE_SHINE if on_stripe else TULIP_SHINE, None, 0))
    # the front: chrome-edged black grille across, a round lamp in each end, the badge
    zfe = _end_z(car, True)
    hwf = half_w(car, zf) * 0.97
    yb_f, yt_f = st[-1][2], st[-1][3]
    gy0, gy1 = yb_f + 0.15, yt_f - 0.06
    d.append(Decal([(-hwf, gy0, zfe), (hwf, gy0, zfe), (hwf, gy1, zfe), (-hwf, gy1, zfe)], (0, 0, 1), CHROME, INK, 1.4))
    d.append(Decal([(-hwf + 0.25, gy0 + 0.03, zfe + 0.002), (hwf - 0.25, gy0 + 0.03, zfe + 0.002),
                    (hwf - 0.25, gy1 - 0.03, zfe + 0.002), (-hwf + 0.25, gy1 - 0.03, zfe + 0.002)], (0, 0, 1), GRILLE, INK, 1.2))
    for k in range(1, 5):
        y = gy0 + 0.03 + (gy1 - gy0 - 0.06) * k / 5
        d.append(Decal([(-hwf + 0.27, y, zfe + 0.004), (hwf - 0.27, y, zfe + 0.004)], (0, 0, 1), None, CHROME_DK, 1.0, 'line'))
    for s in (-1, 1):
        cx, cy = s * (hwf - 0.13), (gy0 + gy1) / 2
        d.append(Decal([(x, y, zfe + 0.004) for x, y in _ring2(cx, cy, 0.105)], (0, 0, 1), CHROME, INK, 1.2))
        d.append(Decal([(x, y, zfe + 0.006) for x, y in _ring2(cx, cy, 0.078)], (0, 0, 1), (250, 244, 214), INK, 1.0,
                       'lamp', glow=(255, 240, 200)))
    d.append(Decal([(x, y, zfe + 0.006) for x, y in _ring2(0, (gy0 + gy1) / 2, 0.045, 6, 0.03)], (0, 0, 1), CHROME, INK, 1.0))
    # the back: boot face, the plate (tail lamps sit in the bumper part)
    zbe = _end_z(car, False)
    d.append(Decal([(-0.25, 0.52, zbe), (0.25, 0.52, zbe), (0.25, 0.72, zbe), (-0.25, 0.72, zbe)], (0, 0, -1),
                   (226, 220, 196), INK, 1.0, 'text', pic=('M9C T48', (40, 40, 60))))
    return d + _house_decals(car, 'tulip')


def dk_(c, k):
    return tuple(int(v * k) for v in c[:3])


def _house_decals(car, kind):
    """Windows on the glass house: screen, back screen, side windows (hardtop: a thin chrome divider; the cruiser:
    black pillars)."""
    P = _house_pts(car)
    d = []
    h = car.spec['house']
    # windscreen and back screen
    for face, u, n in (('screen', 1, (0, 0, 1)), ('rearscreen', 0, (0, 0, -1))):
        pts = []
        for s, v in ((-0.90, 0.06), (0.90, 0.06), (0.86, 0.93), (-0.86, 0.93)):
            p0, p1 = P(-1, u, v), P(1, u, v)
            x = p0[0] + (p1[0] - p0[0]) * (s + 1) / 2
            pts.append((x, p0[1], p0[2]))
        n_loc = _outward([P(-1, u, 0), P(1, u, 0), P(1, u, 1)], (0, (h['y'][0] + h['y'][1]) / 2, sum(h['base']) / 2))
        pts = [S._add(p, S._mul(n_loc, EPS)) for p in pts]
        d.append(Decal(pts, n_loc, GLASS, INK, 1.4, 'glass', glow=face))
    # side windows (u along from back to front at each height, v up)
    wins = [(0.20, 0.50), (0.52, 0.94)] if kind == 'tulip' else [(0.10, 0.20), (0.23, 0.53), (0.57, 0.95)]
    for s in (-1, 1):
        n_loc = _outward([P(s, 0, 0), P(s, 1, 0), P(s, 1, 1)], (0, (h['y'][0] + h['y'][1]) / 2, sum(h['base']) / 2))
        for k, (u0, u1) in enumerate(wins):
            pts = [P(s, u0, 0.10), P(s, u1, 0.10), P(s, u1, 0.90), P(s, u0, 0.90)]
            pts = [S._add(p, S._mul(n_loc, EPS)) for p in pts]
            d.append(Decal(pts, n_loc, GLASS, INK, 1.3, 'glass', glow='side'))
            d[-1].open = (s, k) in getattr(car, 'open_windows', ())     # wound down: a hole onto the dark cabin
        if kind == 'tulip':      # the chrome window surround
            pts = [P(s, 0.18, 0.06), P(s, 0.955, 0.06)]
            d.append(Decal([S._add(p, S._mul(n_loc, EPS * 2)) for p in pts], n_loc, None, CHROME, 2.0, 'line'))
    for x in d:
        x.house = True
    return d


def _cop_decals(car):
    d = []
    st = _stations(car)
    zf, zb = st[-1][0], st[0][0]
    for s in (-1, 1):
        for zc in car.spec['wheels']['z']:
            d.append(_arch(car, s, zc))
        for zc in (1.02, -0.30, -1.36):
            d.append(Decal([_side_pt(car, s, zc, 0.36), _side_pt(car, s, zc + 0.01, 0.96)], (s, 0, 0), None, INK, 1.4, 'line'))
        # the dark blue stripe the length of the car, kinked up at the back, and POLICE on the front door
        y0, y1 = 0.62, 0.72
        pts = [_side_pt(car, s, 2.30, y0 + 0.02), _side_pt(car, s, -1.55, y0), _side_pt(car, s, -2.30, y0 + 0.16),
               _side_pt(car, s, -2.30, y1 + 0.16), _side_pt(car, s, -1.62, y1), _side_pt(car, s, 2.30, y1 + 0.02)]
        d.append(Decal(pts, (s, 0, 0), COP_BLUE, INK, 1.0))
        za, zb_ = (-0.26, 0.98) if s > 0 else (0.98, -0.26)
        d.append(Decal([_side_pt(car, s, za, 0.74), _side_pt(car, s, zb_, 0.74), _side_pt(car, s, zb_, 0.93),
                        _side_pt(car, s, za, 0.93)], (s, 0, 0), None, None, 0, 'text', pic=('POLICE', COP_BLUE)))
        # the badge on the rear door
        cz = -0.85
        d.append(Decal([_side_pt(car, s, cz + 0.17 * math.cos(a), 0.83 + 0.15 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 7, endpoint=False)],
                       (s, 0, 0), (214, 176, 70), INK, 1.4))
        d.append(Decal([_side_pt(car, s, cz + 0.08 * math.cos(a), 0.83 + 0.07 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 5, endpoint=False)],
                       (s, 0, 0), COP_BLUE, None, 0))
        for zc in (0.45, -0.85):
            d.append(Decal([_side_pt(car, s, zc, 0.93), _side_pt(car, s, zc + 0.15, 0.93), _side_pt(car, s, zc + 0.15, 0.96),
                            _side_pt(car, s, zc, 0.96)], (s, 0, 0), COP_BLACK, INK, 0.9))
    # the front: black grille, swept lamps; the back: wide red lamps, VICE CITY POLICE, the plate
    zfe, zbe = _end_z(car, True), _end_z(car, False)
    hwf = half_w(car, zf) * 0.96
    yb_f, yt_f = st[-1][2], st[-1][3]
    d.append(Decal([(-0.42, yb_f + 0.04, zfe), (0.42, yb_f + 0.04, zfe), (0.46, yt_f - 0.10, zfe), (-0.46, yt_f - 0.10, zfe)],
                   (0, 0, 1), GRILLE, INK, 1.3))
    for s in (-1, 1):
        d.append(Decal([(s * 0.50, yt_f - 0.06, zfe), (s * hwf, yt_f - 0.03, zfe), (s * hwf, yt_f - 0.17, zfe),
                        (s * 0.52, yt_f - 0.20, zfe)], (0, 0, 1), (236, 238, 240) if not (car.crush > 0.4 and s > 0) else (50, 50, 56),
                       INK, 1.2, 'lamp', glow=None if (car.crush > 0.4 and s > 0) else (255, 250, 235)))
        yb_b, yt_b = st[0][2], st[0][3]
        hwb = half_w(car, zb) * 0.96
        d.append(Decal([(s * 0.30, yt_b - 0.04, zbe), (s * hwb, yt_b - 0.03, zbe), (s * hwb, yt_b - 0.14, zbe),
                        (s * 0.30, yt_b - 0.11, zbe)], (0, 0, -1), RED_LAMP, INK, 1.2, 'lamp', glow=(255, 60, 50)))
    d.append(Decal([(-0.66, 0.74, zbe), (0.66, 0.74, zbe), (0.66, 0.84, zbe), (-0.66, 0.84, zbe)], (0, 0, -1),
                   None, None, 0, 'text', pic=('VICE CITY POLICE', (40, 44, 60))))
    d.append(Decal([(-0.24, 0.48, zbe), (0.24, 0.48, zbe), (0.24, 0.68, zbe), (-0.24, 0.68, zbe)], (0, 0, -1),
                   (236, 236, 230), INK, 1.0, 'text', pic=('VCPD07', (30, 40, 110))))
    d = d + _house_decals(car, 'cruiser')
    if car.shatter > 0:
        d += _cracks(car)
    if car.crush > 0:
        d += _crumple(car)
    return d


def _crumple(car):
    """The crumpled front: dark folds across the buckled bonnet and the pushed-in nose, one lamp smashed."""
    st = _stations(car)
    zf = st[-1][0]
    c = car.crush
    rng = np.random.RandomState(9)
    d = []
    for z0 in (zf - 0.22, zf - 0.55, zf - 0.85):            # folds across the bonnet: dark zig-zag bands
        xs = np.linspace(-0.82, 0.82, 9)
        up = [_top_pt(car, x, z0 + rng.uniform(-0.06, 0.06) * c) for x in xs]
        down = [_top_pt(car, x, z0 + 0.07 + rng.uniform(-0.04, 0.04)) for x in reversed(xs)]
        d.append(Decal(up + down, (0, 1, 0), (138, 136, 146), None, 0))
        d.append(Decal(up, (0, 1, 0), None, INK, 2.4, 'line'))
    zfe = _end_z(car, True)
    yb_f, yt_f = st[-1][2], st[-1][3]
    pts = [(x, yb_f + 0.08 + rng.uniform(0, 0.12), zfe + 0.003) for x in np.linspace(-0.7, 0.7, 7)]
    pts += [(x, yt_f - 0.04 - rng.uniform(0, 0.10), zfe + 0.003) for x in np.linspace(0.7, -0.7, 7)]
    d.append(Decal(pts, (0, 0, 1), (64, 60, 62), INK, 1.2))
    for s in (-1, 1):                                         # the wings' folds where the nose was shoved back
        for z0 in (zf - 0.15, zf - 0.45):
            pts = [_side_pt(car, s, z0 + 0.08 * ((k % 2) * 2 - 1) * c, y) for k, y in enumerate(np.linspace(0.36, top_y(car, z0) - 0.12, 6))]
            d.append(Decal(pts, (s, 0, 0), None, INK, 2.6, 'line'))
    return d


def _cracks(car):
    """The windscreen crazed: a white star of cracks round the bullet hole, in front of the driver."""
    P = _house_pts(car)
    h = car.spec['house']
    n_loc = _outward([P(-1, 1, 0), P(1, 1, 0), P(1, 1, 1)], (0, (h['y'][0] + h['y'][1]) / 2, sum(h['base']) / 2))
    def on(xf, v):                       # xf: -1 left edge .. 1 right edge, v up the screen
        p0, p1 = P(-1, 1, v), P(1, 1, v)
        x = p0[0] + (p1[0] - p0[0]) * (xf + 1) / 2
        return S._add((x, p0[1], p0[2]), S._mul(n_loc, EPS * 3))
    rng = np.random.RandomState(4)
    d = []
    c = (-0.50, 0.50)
    k = car.shatter
    # a frosted pale patch round the hole first: at phone size the web reads as one white star, not hairlines
    rf = np.random.RandomState(8)
    d.append(Decal([on(max(-0.9, min(0.9, c[0] + 0.30 * k * rf.uniform(0.7, 1.0) * math.cos(a))),
                       max(0.06, min(0.92, c[1] + 0.30 * k * 0.9 * rf.uniform(0.7, 1.0) * math.sin(a))))
                    for a in np.linspace(0, 2 * math.pi, 14, endpoint=False)], n_loc, (196, 214, 226), (236, 244, 248), 1.2))
    spokes = []
    for i in range(11):
        a = i / 11 * 2 * math.pi + rng.uniform(-0.2, 0.2)
        L = rng.uniform(0.35, 0.75) * k
        pts = [on(c[0], c[1])]
        for j in range(1, 4):
            r = L * j / 3
            pts.append(on(max(-0.88, min(0.88, c[0] + r * math.cos(a) + rng.uniform(-0.04, 0.04))),
                          max(0.08, min(0.9, c[1] + r * 0.9 * math.sin(a)))))
        spokes.append(pts)
    for pts in spokes:                   # bold: an ink edge under each white crack (hairlines vanish on a phone)
        d.append(Decal(pts, n_loc, None, INK, 7.0, 'line'))
    for pts in spokes:
        d.append(Decal(pts, n_loc, None, (246, 250, 252), 4.4, 'line'))
    for r in (0.12, 0.26):               # the rings of the web
        pts = [on(max(-0.88, min(0.88, c[0] + r * k * math.cos(a))), max(0.08, min(0.9, c[1] + r * k * 0.9 * math.sin(a))))
               for a in np.linspace(0, 2 * math.pi, 12)]
        d.append(Decal(pts, n_loc, None, (236, 244, 248), 2.4, 'line'))
    d.append(Decal([on(c[0] + 0.10 * math.cos(a), c[1] + 0.12 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 10, endpoint=False)],
                   n_loc, (210, 222, 230), INK, 1.2))
    d.append(Decal([on(c[0] + 0.055 * math.cos(a), c[1] + 0.065 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 8, endpoint=False)],
                   n_loc, (14, 14, 18), INK, 1.4))
    for x in d:
        x.house = True
    return d


# ------------------------------------------------------------------------------------------------ parts on the body
class Part:
    """A small solid fixed to one face of the body: drawn after the body when that face is seen, before it if not."""
    def __init__(self, faces, anchor_pt, anchor_n, level=1, decals=(), ground=False):
        self.faces, self.anchor_pt, self.anchor_n, self.level = faces, anchor_pt, anchor_n, level
        self.decals, self.ground = list(decals), ground


def _box(car, c, size, col, yaw=0.0, lw=2.0):
    faces = S.obox(c, size, yaw, cols={'all': col}, lw=lw)
    out = []
    w, hgt, dp = size
    centre = (c[0], c[1] + hgt / 2, c[2])
    for f in faces:
        pts = [car.body_pt(p) for p in f.pts]
        n = _outward(pts, car.body_pt(centre))
        g = S.Face(pts, n, shade(col, n), INK, lw)
        out.append(g)
    return out


def _parts(car):
    sp = car.spec
    st = _stations(car)
    zf, zb = st[-1][0], st[0][0]
    hw = sp['half_w']
    parts = []
    if car.kind == 'tulip':
        cr = car.crush
        parts.append(Part(_box(car, (0, st[-1][2] + 0.02, zf + 0.04), (2 * half_w(car, zf) - 0.04, 0.11, 0.09), CHROME),
                          (0, 0.5, zf), (0, 0, 1)))
        rear = _box(car, (0, st[0][2] - 0.02, zb - 0.06), (2 * half_w(car, zb) - 0.04, 0.24, 0.14), CHROME)   # inside the body's width: never a box poking out
        lamps = []
        zbb = zb - 0.13 - EPS
        for s in (-1, 1):
            for k in range(2):
                x0 = s * (0.50 + 0.17 * k)
                lamps.append(Decal([(x0, st[0][2] + 0.03, zbb), (x0 + s * 0.13, st[0][2] + 0.03, zbb),
                                    (x0 + s * 0.13, st[0][2] + 0.18, zbb), (x0, st[0][2] + 0.18, zbb)], (0, 0, -1),
                                   RED_LAMP, INK, 1.0, 'lamp', glow=(255, 60, 50)))
                for j in (1, 2):
                    xs = x0 + s * 0.13 * j / 3
                    lamps.append(Decal([(xs, st[0][2] + 0.04, zbb - 0.002), (xs, st[0][2] + 0.17, zbb - 0.002)], (0, 0, -1),
                                       None, (90, 10, 14), 1.4, 'line'))
        parts.append(Part(rear, (0, 0.5, zb), (0, 0, -1), decals=lamps))
        P = _house_pts(car)
        for s in (-1, 1):                # the wing mirror: a stalk out of the door top into a small round-ish head
            m = P(s, 0.98, 0.0)
            xd = abs(m[0])               # the door's skin at the screen's foot (the body tucks in above the waist)
            # Sam, v5 note 2 ("broken cube effects"): the stalk ran 3 cm into the head, so the two boxes cut each
            # other into loose blocks; now a thin dark stalk meets the head's inner face, one clean head on it
            stalk = _box(car, (s * (xd + 0.03), 0.905, m[2] - 0.03), (0.06, 0.025, 0.03), (44, 38, 38))
            head = _box(car, (s * (xd + 0.11), 0.91, m[2] - 0.04), (0.10, 0.08, 0.06), TULIP_RED)
            parts.append(Part(stalk + head, (s * xd, 0.9, m[2]), (s, 0, 0)))
    else:
        parts.append(Part(_box(car, (0, st[-1][2] - 0.04, zf + 0.04), (2 * hw - 0.10, 0.20, 0.12), COP_BLACK),
                          (0, 0.5, zf), (0, 0, 1)))
        # the push bar: two uprights and a cross bar in front of the grille
        pb = []
        cr = car.crush
        for x in (-0.36, 0.36):
            pb += _box(car, (x, st[-1][2] + 0.05 - 0.08 * cr * (x < 0), zf + 0.16 + 0.12 * cr * (x > 0)), (0.07, 0.42, 0.07), COP_BLACK)
        pb += _box(car, (0.05 * cr, st[-1][2] + 0.28 - 0.10 * cr, zf + 0.16 + 0.06 * cr), (0.86, 0.07, 0.07), COP_BLACK, yaw=-28 * cr)
        parts.append(Part(pb, (0, 0.5, zf + 0.1), (0, 0, 1), level=2))
        parts.append(Part(_box(car, (0, st[0][2] - 0.04, zb - 0.04), (2 * hw - 0.08, 0.22, 0.12), COP_WHITE),
                          (0, 0.5, zb), (0, 0, -1)))
        P = _house_pts(car)
        for s in (-1, 1):
            m = P(s, 0.97, 0.05)
            parts.append(Part(_box(car, (s * (hw + 0.07), m[1] - 0.02, m[2] - 0.08), (0.14, 0.12, 0.08), COP_BLACK),
                              (s * hw, 1.0, m[2]), (s, 0, 0)))
        # the light bar across the roof: black base, red lens on the driver's side, blue on the passenger's
        h = sp['house']
        yr, zm = h['y'][1], (h['roof'][0] + h['roof'][1]) / 2 + 0.1
        bar = _box(car, (0, yr, zm), (1.24, 0.05, 0.30), COP_BLACK)
        red_on, blue_on = flash(car)
        bar += _box(car, (-0.33, yr + 0.05, zm), (0.56, 0.08, 0.26), RED_LIT if red_on else RED_LAMP, lw=1.6)
        bar += _box(car, (0.33, yr + 0.05, zm), (0.56, 0.08, 0.26), BLUE_LIT if blue_on else BLUE_LAMP, lw=1.6)
        parts.append(Part(bar, (0, yr, zm), None, level=3))
    return parts


def flash(car):
    """The light bar's beat: red and blue take turns, each a quick double flash (about 2.5 a second)."""
    if not car.lamps:
        return False, False
    f = (getattr(car, 't', 0.0) * 2.5) % 1.0
    red = (0.0 <= f < 0.12) or (0.20 <= f < 0.32)
    blue = (0.5 <= f < 0.62) or (0.70 <= f < 0.82)
    return red, blue


# ------------------------------------------------------------------------------------------------ wheels
def _wheel(img, cam, p, car, side, zc, front):
    w = car.spec['wheels']
    r, width, x_out = w['r'], w['w'], side * w['x']
    steer = car.steer if front else 0.0
    def L(x, y, z):                         # wheel frame: steer about the wheel's upright, then the car's yaw
        dx, dz = x - x_out, z - zc
        a = math.radians(steer)
        dx, dz = dx * math.cos(a) + dz * math.sin(a), -dx * math.sin(a) + dz * math.cos(a)
        return car.ground_pt((x_out + dx, y, zc + dz))
    xin = x_out - side * width
    angs = np.linspace(0, 2 * math.pi, 22, endpoint=False)
    outer = [L(x_out, r + r * math.cos(a), zc + r * math.sin(a)) for a in angs]
    inner = [L(xin, r + r * math.cos(a), zc + r * math.sin(a)) for a in angs]
    if any(cam.depth(q) < cam.NEAR for q in outer + inner):
        return
    hull = S._hull([cam.project(q)[0] for q in outer + inner])
    if len(hull) >= 3:
        p.poly(hull, TYRE, INK, 2.0)
    n = S._norm(S._sub(L(x_out + side, r, zc), L(x_out, r, zc)))
    cen = L(x_out, r, zc)
    if S._dot(n, S._sub(cam.pos, cen)) <= 0:
        return
    rim_col = STEEL if car.kind == 'tulip' else (44, 44, 48)
    xo = x_out + side * 0.004
    cam.poly(p, [L(xo, r + 0.66 * r * math.cos(a), zc + 0.66 * r * math.sin(a)) for a in angs], rim_col, INK, 1.4)
    cam.poly(p, [L(xo + side * 0.004, r + 0.42 * r * math.cos(a), zc + 0.42 * r * math.sin(a)) for a in angs[::2]],
             dk_(rim_col, 0.72), INK, 1.0)
    cam.poly(p, [L(xo + side * 0.008, r + 0.20 * r * math.cos(a), zc + 0.20 * r * math.sin(a)) for a in angs[::2]],
             CHROME, INK, 1.0)
    for k in range(5):                       # lug nuts: they turn, so the wheel reads as rolling
        a = car.spin * side + k * 2 * math.pi / 5
        c3 = (r + 0.31 * r * math.cos(a), zc + 0.31 * r * math.sin(a))
        cam.poly(p, [L(xo + side * 0.01, c3[0] + 0.022 * math.cos(b), c3[1] + 0.022 * math.sin(b))
                     for b in np.linspace(0, 2 * math.pi, 6, endpoint=False)], (30, 30, 30), None, 0)


# ------------------------------------------------------------------------------------------------ light and pictures
def glow(img, pt, radius, colour, strength=1.0):
    """A soft pool of light round a frame point (1080 x 1920 units), added on top."""
    x, y = pt[0] * B.SS, pt[1] * B.SS
    R = max(4, int(radius * B.SS))
    x0, y0 = int(x - 2 * R), int(y - 2 * R)
    size = 4 * R
    if x0 > img.width or y0 > img.height or x0 + size < 0 or y0 + size < 0:
        return
    lay = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([R, R, 3 * R, 3 * R], fill=colour[:3] + (int(255 * min(1.0, strength)),))
    lay = lay.filter(ImageFilter.GaussianBlur(R * 0.5))
    img.alpha_composite(lay, (max(0, x0), max(0, y0)), (max(0, -x0), max(0, -y0)))


def _coeffs(src, dst):
    """Perspective coefficients mapping the output (dst quad) back to the picture (src quad)."""
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        b += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(b, float)).tolist()


def paste_quad(img, quad, pic):
    """Lay a picture on four frame points (1080 x 1920 units, picture corners TL, TR, BR, BL)."""
    q = [(x * B.SS, y * B.SS) for x, y in quad]
    xs, ys = [p[0] for p in q], [p[1] for p in q]
    x0, y0 = int(max(0, min(xs))), int(max(0, min(ys)))
    x1, y1 = int(min(img.width, max(xs) + 1)), int(min(img.height, max(ys) + 1))
    if x1 - x0 < 2 or y1 - y0 < 2:
        return
    w, h = pic.size
    co = _coeffs([(0, 0), (w, 0), (w, h), (0, h)], [(x - x0, y - y0) for x, y in q])
    lay = pic.transform((x1 - x0, y1 - y0), Image.PERSPECTIVE, co, Image.BICUBIC)
    img.alpha_composite(lay, (x0, y0))


def _text_pic(text, colour, bg=None):
    f = ImageFont.truetype(BOLD, 90)
    w = int(f.getlength(text)) + 30
    im = Image.new('RGBA', (w, 120), (bg[:3] + (255,)) if bg else (0, 0, 0, 0))
    ImageDraw.Draw(im).text((15, 8), text, font=f, fill=colour[:3] + (255,))
    return im


# ------------------------------------------------------------------------------------------------ drawing
def _decal_draw(img, cam, p, car, dc, t, lit):
    pts = [car.body_pt(q) for q in dc.pts]
    n = S._norm(car.body_dir(dc.n_local))
    c = tuple(sum(q[i] for q in pts) / len(pts) for i in range(3))
    if S._dot(n, S._sub(cam.pos, c)) <= 1e-4:
        return None
    if dc.kind == 'line':
        cam.line(p, pts, dc.line, dc.lw)
        return None
    if dc.kind == 'text':
        if dc.fill:
            cam.poly(p, pts, shade(dc.fill, n, 0.2), INK, dc.lw)
        if any(cam.depth(q) < cam.NEAR for q in pts):
            return None
        text, col = dc.pic
        paste_quad(img, [cam.project(q)[0] for q in (pts[3], pts[2], pts[1], pts[0])], _text_pic(text, col))
        return None
    fill = dc.fill
    if dc.kind == 'glass' and getattr(dc, 'open', False):
        cam.poly(p, pts, CABIN, dc.line, dc.lw)
        return ('glass', pts, n, True)
    if dc.kind == 'glass':
        fill = shade(GLASS, n, 0.5)
    elif dc.kind != 'lamp':
        fill = shade(fill, n, 0.30) if fill else None
    cam.poly(p, pts, fill, dc.line, dc.lw)
    if dc.kind == 'glass':
        return ('glass', pts, n)
    if dc.kind == 'lamp' and dc.glow and lit:
        return ('lamp', c, dc.glow)
    return None


def _draw_faces(img, cam, p, faces):
    for f in faces:
        if f.seen(cam):
            cam.poly(p, f.pts, f.fill, f.line, f.lw)


def shadow(img, cam, car):
    """The soft dark pool under the car, on the road (follows the car, not its lean)."""
    st = car.spec['stations']
    hw = car.spec['half_w'] - 0.04
    pts = [car.ground_pt((x, 0.004, z)) for x, z in ((-hw, st[0][0] + 0.15), (hw, st[0][0] + 0.15), (hw, st[-1][0] - 0.15), (-hw, st[-1][0] - 0.15))]
    if any(cam.depth(q) < cam.NEAR for q in pts):
        return
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    q = [cam.project(v)[0] for v in pts]
    ImageDraw.Draw(lay).polygon([(x * B.SS, y * B.SS) for x, y in q], fill=(20, 10, 30, 130))
    xs, ys = [v[0] * B.SS for v in q], [v[1] * B.SS for v in q]
    blur = max(2, int((max(ys) - min(ys)) * 0.03 + 3))
    box = (int(max(0, min(xs) - 3 * blur)), int(max(0, min(ys) - 3 * blur)),
           int(min(img.width, max(xs) + 3 * blur)), int(min(img.height, max(ys) + 3 * blur)))
    if box[2] <= box[0] or box[3] <= box[1]:
        return
    crop = lay.crop(box).filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(crop, box[:2])


def seat_people(img_layer, cam, car, who=None):
    """The default people seen through the glass: dark heads and shoulders in the seats (the film passes its own
    painter for close shots)."""
    p = S.pen(img_layer)
    seats = car.spec['seats'] if who is None else [s for s in car.spec['seats'] if s[2] in who]
    for x, z, name in sorted(seats, key=lambda s: -math.dist(car.body_pt((s[0], 1.1, s[1])), cam.pos)):
        y0 = car.spec['house']['y'][0]
        sh = [car.body_pt((x + 0.24 * math.cos(a), y0 + 0.02 + 0.16 * max(0, math.sin(a)), z + 0.10 * math.sin(a * 2)))
              for a in np.linspace(0, math.pi, 9)]
        sh += [car.body_pt((x + dx, y0 - 0.1, z + dz)) for dx in (-0.24, 0.24) for dz in (-0.1, 0.1)]
        S.blob3(img_layer, cam, p, sh, (34, 30, 34), None, 0)
        S.blob3(img_layer, cam, p, S.sphere_pts(car.body_pt((x, y0 + 0.27, z)), 0.11, 7, 1.15), (30, 26, 30), None, 0)


def draw_car(img, cam, car, t=0.0, inside=seat_people, lit=True):
    """The whole car through `cam` at time t. inside(layer, cam, car) paints what is seen through the glass."""
    car.t = t
    car._bg = img.copy()                 # what lies behind the car: seen through its far windows (chat 13)
    p = S.pen(img)
    shadow(img, cam, car)
    body = _body(car)
    house = _house(car)
    decals = _tulip_decals(car) if car.kind == 'tulip' else _cop_decals(car)
    parts = _parts(car)
    wz = car.spec['wheels']['z']
    wx = car.spec['wheels']['x']
    for s in (-1, 1):
        for i, zc in enumerate(wz):
            parts.append(Part([], (s * wx, car.spec['wheels']['r'], zc), (s, 0, 0), level=0, ground=True))
            parts[-1].wheel = (s, zc, i == 0)
    h = car.spec['house']
    hp = Part(house, (0, h['y'][0], 0), (0, 1, 0), level=1)
    hp.house = True
    parts.append(hp)

    def facing(pt):
        if pt.anchor_n is None:
            return True, 0.0
        a = car.ground_pt(pt.anchor_pt) if pt.ground else car.body_pt(pt.anchor_pt)
        n = S.rot_y(pt.anchor_n, car.yaw) if pt.ground else S._norm(car.body_dir(pt.anchor_n))
        return S._dot(n, S._sub(cam.pos, a)) > 0, math.dist(a, cam.pos)

    behind, front = [], []
    for pt in parts:
        seen, dist = facing(pt)
        (front if seen else behind).append((pt, dist))
    glows = []

    def draw_part(pt, near=False):
        if hasattr(pt, 'wheel'):
            s, zc, fr = pt.wheel
            if not near:
                _wheel(img, cam, p, car, s, zc, fr)
                return
            # Sam, GTA v5 note 6 ("wheel clipping through chassis"): a near-side wheel is drawn after the body, so it
            # showed whole over the wing; it is seen only through its arch (and below the sill), the body hides the rest
            lay = Image.new(img.mode, img.size, (0, 0, 0, 0) if img.mode == 'RGBA' else 0)
            _wheel(lay, cam, S.pen(lay), car, s, zc, fr)
            m = arch_mask(car, cam, s, zc, img.size)
            if lay.mode == 'RGBA':
                a = np.asarray(lay.split()[3], np.float32) * (np.asarray(m, np.float32) / 255)
                lay.putalpha(Image.fromarray(a.astype(np.uint8)))
                img.alpha_composite(lay)
            else:
                img.paste(lay, (0, 0), m)
            return
        _draw_faces(img, cam, p, pt.faces)
        if getattr(pt, 'house', False):
            glass = []
            for dc in decals:
                if dc in house_decals:
                    r = _decal_draw(img, cam, p, car, dc, t, lit)
                    if r and r[0] == 'glass':
                        glass.append(r)
            _through_glass(img, cam, car, glass, inside)
        for dc in pt.decals:
            r = _decal_draw(img, cam, p, car, dc, t, lit)
            if r and r[0] == 'lamp':
                glows.append(r)

    house_decals = set(_house_ids(decals))
    for pt, _ in sorted(behind, key=lambda e: -e[1]):
        draw_part(pt)
    _draw_faces(img, cam, p, body)
    for dc in decals:
        if dc not in house_decals:
            r = _decal_draw(img, cam, p, car, dc, t, lit)
            if r and r[0] == 'lamp':
                glows.append(r)
    for pt, _ in sorted(front, key=lambda e: (e[0].level, -e[1])):
        draw_part(pt, near=True)
    if lit:
        for _, c, col in glows:
            if cam.depth(c) > cam.NEAR:
                (x, y), k = cam.project(c)
                glow(img, (x, y), max(6, 0.22 * k), col, 0.55)
        if car.kind == 'cruiser':
            red, blue = flash(car)
            yr = h['y'][1] + 0.1
            zm = (h['roof'][0] + h['roof'][1]) / 2 + 0.1
            for on, x, col in ((red, -0.33, (255, 50, 50)), (blue, 0.33, (70, 130, 255))):
                c = car.body_pt((x, yr, zm))
                if on and cam.depth(c) > cam.NEAR:
                    (sx, sy), k = cam.project(c)
                    glow(img, (sx, sy), max(10, 0.42 * k), col, 0.85)   # v4 N3 (chat 33d): 0.75 m pools floated
                    #                                   above the car as a smear; 0.42 m sits on the bar


def cover_masks(car, cam, ref, size):
    """What of the car stands between the lens and the point `ref` (someone leaning out of it, or sat in it), as two
    canvas masks: solid (body sides, bonnet, boot, pillars, roof: rub them out there) and glass (closed panes: seen
    through, a little dimmed). Only faces whose plane cuts the line from the lens to ref count, so a man in front of
    the door is never rubbed out by it (chat 11's floating chest). The cabin's top is open air; an open window a hole."""
    solid, pane = Image.new('L', size, 0), Image.new('L', size, 0)
    sd, gd = ImageDraw.Draw(solid), ImageDraw.Draw(pane)
    c = np.asarray(cam.pos, float)
    r = np.asarray(ref, float)

    def between(pts):
        a, b, d = (np.asarray(q, float) for q in pts[:3])
        n = np.cross(b - a, d - a)
        den = float(n @ (r - c))
        if abs(den) < 1e-9:
            return False
        u = float(n @ (a - c)) / den
        if not 0.0 < u < 0.999:
            return False
        # and the sight line must pass THROUGH the face, not just its endless plane (chat 14: the roof rubbed out the
        # arm and chest of Jason sat on the sill, outside the roof's edge): inside the polygon, 5 cm of slack
        p = c + u * (r - c)
        P = [np.asarray(q, float) for q in pts]
        nn = n / (np.linalg.norm(n) + 1e-12)
        sgn = 0.0
        for i in range(len(P)):
            e = P[(i + 1) % len(P)] - P[i]
            le = np.linalg.norm(e)
            if le < 1e-9:
                continue
            side = float(np.cross(e, p - P[i]) @ nn) / le          # signed distance from this edge, in metres
            if sgn == 0.0 and abs(side) > 0.05:
                sgn = 1.0 if side > 0 else -1.0
            if sgn and side * sgn < -0.05:
                return False
        return True

    used = []

    def poly(dr, pts, name='the ' + car.kind):
        used.append((name, pts))
        q2 = cam.clip(pts)
        if len(q2) > 2:
            dr.polygon([(x * B.SS, y * B.SS) for x, y in q2], fill=255)
    h = car.spec['house']
    for f in _body(car):
        if not f.seen(cam):
            continue
        if f.tag == 'top':                                   # only the bonnet and boot: the cabin is open
            loc = [local_pt(car, q) for q in f.pts]
            z0, z1 = min(q[2] for q in loc), max(q[2] for q in loc)
            parts = [(max(z0, h['base'][1]), z1), (z0, min(z1, h['base'][0]))]
            ys = sorted(q[1] for q in loc)[-1]
            xs = max(abs(q[0]) for q in loc)
            for a_, b_ in parts:
                if b_ - a_ > 0.01:
                    pts = [car.body_pt(q) for q in ((-xs, ys, a_), (xs, ys, a_), (xs, ys, b_), (-xs, ys, b_))]
                    if between(pts):
                        poly(sd, pts, "the %s's %s" % (car.kind, 'bonnet' if a_ > 0 else 'boot'))
            continue
        if between(f.pts):
            poly(sd, f.pts, "the %s's %s" % (car.kind, f.tag))
    wins = [d for d in _house_decals(car, car.kind) if d.kind == 'glass']
    for f in _house(car):
        if not f.seen(cam) or not between(f.pts):
            continue
        poly(sd, f.pts, "the %s's %s" % (car.kind, f.tag))
        fn = S._norm(f.n)
        for d in wins:                                       # this face's windows: cut out of the solid
            dn = S._norm(car.body_dir(d.n_local))
            if S._dot(dn, fn) < 0.98:
                continue
            w = [car.body_pt(q) for q in d.pts]
            q2 = cam.clip(w)
            if len(q2) > 2:
                sd.polygon([(x * B.SS, y * B.SS) for x, y in q2], fill=0)
                if not getattr(d, 'open', False):
                    gd.polygon([(x * B.SS, y * B.SS) for x, y in q2], fill=255)
    return solid, pane, used


def _house_ids(decals):
    return [d for d in decals if getattr(d, 'house', False)]


def glass_tint(size, alpha):
    """A layer of the glass colour with the given alpha (a float array, 0-255): laid over what is behind a pane."""
    t = Image.new('RGBA', size, GLASS + (0,))
    t.putalpha(Image.fromarray(np.clip(alpha, 0, 255).astype(np.uint8)))
    return t


def _through_glass(img, cam, car, glass, inside):
    """What is seen through the windows: painted into its own layer, kept only inside the seen glass, a little
    dimmed by the glass, then a soft sky streak across each pane."""
    if not glass:
        return
    mask = Image.new('L', img.size, 0)
    omask = Image.new('L', img.size, 0)              # wound-down windows: the people seen plainly, no glass
    md, od = ImageDraw.Draw(mask), ImageDraw.Draw(omask)
    for g in glass:
        pts = g[1]
        if any(cam.depth(q) < cam.NEAR for q in pts):
            continue
        poly = [(x * B.SS, y * B.SS) for x, y in (cam.project(q)[0] for q in pts)]
        (od if len(g) > 3 else md).polygon(poly, fill=255)
    bg = getattr(car, '_bg', None)
    if bg is not None:                 # through the near glass and out of the far glass: the street behind, glass-dimmed
        far = Image.new('L', img.size, 0)
        fd = ImageDraw.Draw(far)
        for dc in _house_decals(car, car.kind):
            if dc.kind != 'glass':
                continue
            w = [car.body_pt(q) for q in dc.pts]
            c = tuple(sum(q[i] for q in w) / len(w) for i in range(3))
            if S._dot(S._norm(car.body_dir(dc.n_local)), S._sub(cam.pos, c)) >= 0 or getattr(dc, 'open', False):
                continue
            if any(cam.depth(q) < cam.NEAR for q in w):
                continue
            fd.polygon([(x * B.SS, y * B.SS) for x, y in (cam.project(q)[0] for q in w)], fill=255)
        k = np.minimum(np.asarray(far, np.float32), np.maximum(np.asarray(mask, np.float32), np.asarray(omask, np.float32)))
        if k.any():
            tint = Image.blend(bg.convert('RGB'), Image.new('RGB', img.size, GLASS), 0.28).convert('RGBA')
            # keep what is behind see-through: drawn alone (the layer check's clear sheet) the pane is a faint veil, not
            # an opaque dark panel that made every car behind it read as 'drawn over' this one (chat 15); unchanged in
            # the film, where the street behind is always solid
            ba = np.asarray(bg.convert('RGBA').split()[3], np.uint8)
            tint.putalpha(Image.fromarray(np.maximum(ba, 72).astype(np.uint8)))
            img.paste(tint, (0, 0), Image.fromarray(k.astype(np.uint8)))
    people = None
    if inside:
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        inside(lay, cam, car)
        a = np.asarray(lay.split()[3], np.float32)
        people = a
        k = np.maximum(np.asarray(mask, np.float32), np.asarray(omask, np.float32)) / 255
        lay.putalpha(Image.fromarray((a * k).astype(np.uint8)))
        img.alpha_composite(lay)
        # the glass dims them with a tint laid OVER them: never by thinning them (chat 14: faces showed the seats through)
        g = np.asarray(mask, np.float32) / 255 * (a / 255) * 0.15 * 255
        img.alpha_composite(glass_tint(img.size, g))
    p = S.pen(img)
    for g in glass:                    # the sky streak and the pane's edge again on top
        _, pts, n = g[:3]
        if len(g) > 3:
            cam.poly(p, pts, None, INK, 1.4)
            continue
        if any(cam.depth(q) < cam.NEAR for q in pts):
            continue
        a, b, c, d = pts[0], pts[1], pts[2], pts[3]
        def at(u, v):
            lo = S._add(a, S._mul(S._sub(b, a), u))
            hi = S._add(d, S._mul(S._sub(c, d), u))
            return S._add(S._add(lo, S._mul(S._sub(hi, lo), v)), S._mul(n, 0.002))
        streak = [at(0.18, 0.95), at(0.34, 0.95), at(0.16, 0.05), at(0.02, 0.05)]
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        S.pen(lay).poly([cam.project(q)[0] for q in streak], GLASS_HI + (90,), None, 0)
        sa = np.minimum(np.asarray(lay.split()[3]), np.asarray(mask)).astype(np.float32)
        if people is not None:         # the streak lies on the glass over the street, never over a face (chat 33b, F12:
            sa *= 1 - people / 255     # a see-through grey panel over Lucia's face and hair the whole of shot 6)
        lay.putalpha(Image.fromarray(sa.astype(np.uint8)))
        img.alpha_composite(lay)
        cam.poly(p, pts, None, INK, 1.4)


# ------------------------------------------------------------------------------------------------ the sheet
def _ground(img, cam, col=(120, 108, 118)):
    """A plain road under the cars for the sheet (the film paints its own streets)."""
    p = S.pen(img)
    S.Face([(-40, 0, -40), (40, 0, -40), (40, 0, 40), (-40, 0, 40)], None, col, None, 0)
    cam.poly(p, [(-40, 0, -40), (40, 0, -40), (40, 0, 40), (-40, 0, 40)], col, None, 0)


def views():
    """(label, kind, camera pos, look-at, focal, car state) for the sheet: the angles the film's shots use."""
    T, C = 'tulip', 'cruiser'
    return [
        ('Tulip: side (ref: trailer side)', T, (-9.0, 1.0, 1.0), (0, 0.75, 0.0), 1350, {}),
        ('Tulip: front three-quarter', T, (-5.0, 1.6, 7.0), (0, 0.7, 0.3), 1200, {}),
        ('Tulip: rear three-quarter (ref)', T, (-4.5, 1.5, -7.0), (0, 0.7, -0.3), 1200, {}),
        ('Tulip: shot 2, low at the kerb, mid-swerve (leaning, wheels turned)', T, (-3.0, 0.4, 4.4), (-0.3, 1.0, 0.6), 520, dict(yaw=-48, roll=-8, steer=-28, spin=1.0)),
        ('Cruiser: front three-quarter (shot 4)', C, (5.0, 1.5, 7.5), (0, 0.8, 0.0), 1200, {}),
        ('Cruiser: rear three-quarter (ref)', C, (4.5, 1.6, -7.5), (0, 0.8, 0.0), 1200, {}),
        ('Cruiser: side', C, (9.0, 1.1, 0.0), (0, 0.8, 0.0), 1350, {}),
        ('Both cars nose to tail, side on (sizes)', 'both', (-16.0, 1.2, 0.0), (0.0, 0.8, 0.0), 1000, {}),
        ('Cruiser: crashed, shot through', C, (3.0, 1.5, 6.2), (0, 0.8, 0.8), 900, dict(crush=1.2, shatter=1.0, yaw=14, roll=4, pitch=-3.5)),
    ]


def _ref(name, w, h):
    im = Image.open(os.path.join(REFS, name)).convert('RGB')
    k = min(w / im.width, h / im.height)
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    out = Image.new('RGB', (w, h), (36, 36, 36))
    out.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return out


def render(i, w=1080, h=1920, t=0.0):
    lab, kind, pos, at, focal, kw = views()[i]
    img = B.canvas((240, 170, 170))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for y in range(0, img.height, 8):
        k = y / img.height
        d.line([(0, y), (img.width, y)], fill=(int(250 - 40 * k), int(170 + 20 * k), int(180 + 20 * k), 255), width=8)
    img.alpha_composite(lay)
    cam = S.Cam(pos, at, focal)
    _ground(img, cam)
    if kind == 'both':
        cars = [Car('tulip', pos=(0.0, 2.9)), Car('cruiser', pos=(0.0, -2.9))]
        for c in sorted(cars, key=lambda c: -math.dist(cam.pos, (c.pos[0], 0.8, c.pos[1]))):
            draw_car(img, cam, c, t=t)
    else:
        draw_car(img, cam, Car(kind, **kw), t=t)
    return lab, img.convert('RGB').resize((w, h), Image.LANCZOS)


def sheet(out, which=None):
    """Every view on one sheet, cropped to the car (each frame is a full 9:16 picture), game pictures underneath."""
    vs = views()
    idx = which or list(range(len(vs)))
    tiles = []
    for i in idx:
        lab, im = render(i, t=0.05)
        tiles.append((lab, im.crop((0, 560, 1080, 1360))))
    cw, ch = 540, 400
    cols = 4
    rows = (len(tiles) + cols - 1) // cols
    refs = ['tulip-side-trailer1.jpg', 'tulip-rear-three-quarter.jpg', 'vcpd-cruiser-rear.jpg', 'vcpd-cruiser-above.jpg']
    rh = 300
    Sh = Image.new('RGB', (cols * (cw + 8) + 8, rows * (ch + 40) + rh + 60), (34, 34, 34))
    d = ImageDraw.Draw(Sh)
    f = ImageFont.truetype(BOLD, 18)
    for k, (lab, im) in enumerate(tiles):
        x, y = 8 + (k % cols) * (cw + 8), 8 + (k // cols) * (ch + 40)
        d.text((x, y), f'{k + 1}. {lab}', font=f, fill=(255, 255, 255))
        Sh.paste(im.resize((cw, ch), Image.LANCZOS), (x, y + 28))
    y = 8 + rows * (ch + 40) + 10
    d.text((8, y), 'The game (references/grand-theft-autism/)', font=f, fill=(255, 230, 0))
    for k, r in enumerate(refs):
        Sh.paste(_ref(r, cw, rh), (8 + k * (cw + 8), y + 28))
    Sh.save(out, quality=88)
    print('wrote', out, Sh.size)


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == 'view':
        lab, im = render(int(sys.argv[2]))
        im.save(sys.argv[3], quality=90)
        print('wrote', sys.argv[3], lab)
    else:
        print(__doc__)
