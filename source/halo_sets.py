#!/usr/bin/env python3
"""Halo No-No's places (notes/halo-no-no.md), each a flat painting per camera (film-quality rule 39):

- space_wide(): shot 1 (ref 01): the orange planet on the left, its night side top-left, the thin dark Halo ring
  tilted in front of its lower half, the bright galaxy core right of centre, stars and nebula. Painted once.
- ring_close(): shot 6 (ref 02): the ring's dark hull sweeping across from the top left down to the lower right, then
  the far side rising up the right as a thin strip of seas, land and cloud; the planet behind on the left, the blue
  galaxy band top right. The ring itself is a true circle projected through one camera (so the sweep and the far arc
  sit right), then painted flat. Painted once.
- cabin_back() / cabin_front(): shots 2-5, the Roadster's inside seen from the windscreen facing back (refs 03-05):
  one painting, two framings (WIDE: both seats; CLOSE: Musk). Back: the black glass roof, the rear window onto space
  (a Roadster from the armada drifting past now and then: Sam's yes, 29 Oct), the doors with their red light strips,
  the white ROADSTER seats. Front: the dash, drawn over Musk's lap (it hides him below the belt, as halo_cast.chief
  expects).

The plan in metres (rule 1): left-hand drive, seats 0.74 m apart (centres), each 0.54 m wide and 0.86 m tall from
the cushion; in the wide framing the seats' plane is 680 px a metre (Musk at scale 0.8).

    python3 source/halo_sets.py sheet OUT.jpg     every set, with the cast in place, beside Sam's references
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B                    # noqa: E402  Cam, Pen: flat fills, black outlines
from burnham import INK, dk, lt, SS    # noqa: E402
from satire_style import rough         # noqa: E402
from ed import curve                   # noqa: E402

SANS = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
REFS = os.path.join(HERE, '..', 'references', 'halo-no-no')

SPACE = (12, 12, 30)
NEB_V = (40, 26, 66)          # violet nebula
NEB_B = (24, 34, 78)          # blue nebula

# ============================================== THE PLAN (metres -> pixels) =========================================
PX_M = 680                    # wide framing: pixels per metre at the seats
MUSK = (760, 940, 0.8)        # Musk's neck base and scale in the wide framing (driver's seat, frame right)
SEAT_X = {'driver': 760, 'passenger': 257}       # 0.74 m apart
CUSHION_Y = 1292              # the cushion top (Musk's hips)
SEAT_W, SEAT_H = 0.54, 0.86
DASH_Y = 1300                 # the dash's far edge (it hides Musk below the belt and the yoke's column)
WINDOW = [(150, 430), (930, 430), (968, 800), (112, 800)]       # the rear window (behind the seats)
CORTANA_AT = (257, 760)       # over the passenger seat, standing in mid-air (her neck base; the film sets her scale)


def cam_wide():
    return B.Cam(1.0, 540, 960)


def cam_close():
    """The close-up on Musk: the same painting, nearer (a hard cut, Sam 29 Oct)."""
    return B.Cam(3.4, MUSK[0], 880)


# ================================================ SHARED BITS =======================================================
def _dots(p, pts, rng, size=(1.0, 3.2), cols=None):
    cols = cols or [(255, 255, 255), (220, 228, 255), (255, 240, 214), (200, 210, 255)]
    for x, y in pts:
        r = rng.uniform(*size) * (2.2 if rng.random() < 0.03 else 1.0)
        p.ell(x, y, r, r, cols[rng.integers(len(cols))], None, n=10)


def _stars(p, box, n, seed, size=(1.0, 3.2)):
    r = np.random.default_rng(seed)
    x0, y0, x1, y1 = box
    _dots(p, zip(r.uniform(x0, x1, n), r.uniform(y0, y1, n)), r, size)


def _nebula(p, centre, along, n, size, cols, seed):
    """Flat lumpy patches of colour along a direction (no outline: it is light, not a thing)."""
    r = np.random.default_rng(seed)
    cx, cy = centre
    a = math.radians(along)
    for i in range(n):
        u = r.uniform(-1, 1)
        x = cx + u * size * 1.6 * math.cos(a) + r.normal(0, size * 0.25)
        y = cy + u * size * 1.6 * math.sin(a) + r.normal(0, size * 0.25)
        rx = size * r.uniform(0.35, 0.7)
        p.poly(rough(curve([(x + rx * math.cos(t), y + rx * 0.45 * math.sin(t)) for t in np.linspace(0, 6.28, 9)[:-1]], 3),
                     rx * 0.12, seed + i), cols[i % len(cols)], None)


def _layer_masked(img, mask, draw):
    """Draw onto a clear layer, then keep only what lies inside `mask` (an L image the size of img)."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw(lay)
    a = np.minimum(np.array(lay.split()[3]), np.array(mask))
    lay.putalpha(Image.fromarray(a))
    img.alpha_composite(lay)


def _poly_mask(img, cam, pts):
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).polygon([cam.P(*q) for q in pts], fill=255)
    return m


def _ell_pts(cx, cy, rx, ry, rot=0.0, n=120):
    c, s = math.cos(rot), math.sin(rot)
    return [(cx + rx * math.cos(t) * c - ry * math.sin(t) * s, cy + rx * math.cos(t) * s + ry * math.sin(t) * c)
            for t in np.linspace(0, 2 * math.pi, n, endpoint=False)]


# ================================================ SHOT 1: THE WIDE =================================================
PLANET = (60, 1000, 640)                     # centre and radius (ref 01: the left half, cut by the frame edge)
HALO = (300, 1180, 215, 88, 33)              # the ring: centre, radii, tilt (degrees); in front of the planet's lower half
CORE = (770, 700)                            # the galaxy core (ref 01: bright, right of centre)
PLANET_COL = (198, 122, 74)


def _galaxy_core(p, x, y, k=1.25, tilt=-9):
    a = math.radians(tilt)
    for (rx, ry, col) in ((470, 150, (30, 24, 58)), (380, 92, (52, 36, 92)), (270, 58, (112, 70, 140)), (190, 40, (196, 112, 120)),
                          (124, 27, (240, 168, 104)), (74, 16, (255, 226, 170)), (34, 9, (255, 252, 238))):
        p.poly(rough(_ell_pts(x, y, rx * k, ry * k, a, 40), 4 * k, int(rx)), col, None)
    for i, (u, w) in enumerate(((-0.55, 7), (-0.2, 9), (0.3, 8))):           # dark dust lanes across it
        cx, cy = x + u * 260 * k * math.cos(a), y + u * 260 * k * math.sin(a) + 10 * k
        p.poly(rough(_ell_pts(cx, cy, 60 * k, w * 0.45 * k, a + 0.05, 20), 1.5 * k, 40 + i), (124, 70, 112), None)


def _planet(img, cam, p, cx, cy, R, col, night=(0.34, 0.40), seed=3, lit_from=(1, 1)):
    """A planet: flat colour, flat bands and blotches, a two-step night side away from `lit_from`, one outline."""
    disc = _ell_pts(cx, cy, R, R, 0, 160)
    p.poly(disc, col, None)
    mask = _poly_mask(img, cam, disc)
    r = np.random.default_rng(seed)
    lx, ly = lit_from
    n = math.hypot(lx, ly)
    lx, ly = lx / n, ly / n

    def paint(lay):
        q = B.Pen(lay, cam)
        for i in range(16):                                          # bands, gently tilted, each its own shade
            yy = cy - R + (i + r.uniform(0.2, 0.8)) * 2 * R / 16
            th = R * r.uniform(0.03, 0.08)
            shade = dk(col, r.uniform(0.88, 0.94)) if i % 2 else lt(col, r.uniform(1.04, 1.09))
            pts = [(cx - R * 1.1 + j * R * 0.22, yy + r.normal(0, th * 0.25) + j * R * 0.012) for j in range(11)]
            pts = pts + [(x, y + th) for x, y in pts[::-1]]
            q.poly(rough(pts, th * 0.15, 60 + i), shade, None)
        for i in range(10):                                          # storms and blotches
            a, rho = r.uniform(0, 6.28), r.uniform(0.1, 0.85)
            q.poly(rough(_ell_pts(cx + R * rho * math.cos(a), cy + R * rho * math.sin(a), R * r.uniform(0.04, 0.09),
                                  R * r.uniform(0.02, 0.04), 0.1, 18), R * 0.008, 80 + i), dk(col, 0.9), None)
        k1, k2 = night
        q.poly(_crescent(cx, cy, R, lx, ly, k1 + k2), dk(col, 0.66), None)        # the dusk band
        q.poly(_crescent(cx, cy, R, lx, ly, k1), dk(col, 0.36), None)             # the night side
    _layer_masked(img, mask, paint)
    p.poly(disc, None, INK, 4)


def _crescent(cx, cy, R, lx, ly, k):
    """The part of the disc away from the light: the disc minus the same disc shifted towards the light by k R."""
    out = []
    ox, oy = cx + lx * R * k, cy + ly * R * k
    for t in np.linspace(0, 2 * math.pi, 200, endpoint=False):
        x, y = cx + R * math.cos(t), cy + R * math.sin(t)
        if (x - ox) ** 2 + (y - oy) ** 2 > R * R:
            out.append((t, x, y))
    if not out:
        return []
    # the edge of the shifted disc inside ours closes the shape
    ts = [o[0] for o in out]
    # angles run round the far side; order them as one arc
    gap = np.argmax(np.diff(ts)) + 1 if len(ts) > 1 and max(np.diff(ts)) > 0.2 else 0
    arc = out[gap:] + out[:gap]
    inner = []
    a0 = math.atan2(arc[-1][2] - oy, arc[-1][1] - ox)
    a1 = math.atan2(arc[0][2] - oy, arc[0][1] - ox)
    d = (a1 - a0) % (2 * math.pi)
    if d > math.pi:
        d -= 2 * math.pi
    for u in np.linspace(0, 1, 60):
        a = a0 + d * u
        inner.append((ox + R * math.cos(a), oy + R * math.sin(a)))
    return [(x, y) for _, x, y in arc] + inner


def _halo_far(p, x, y, rx, ry, tilt):
    """The ring's far half: its inner face shows as a thin pale strip (seas and land, far off)."""
    a = math.radians(tilt)
    outer = _ell_pts(x, y, rx, ry, a, 160)
    inner = _ell_pts(x, y - 0, rx - 9, ry - 7, a, 160)
    half = lambda pts: pts[80:] + pts[:1]                            # the upper (far) half
    o, i = half(outer), half(inner)
    p.poly(o + i[::-1], (126, 162, 176), INK, 2.6)


def _halo_near(p, x, y, rx, ry, tilt):
    """The near half: the dark hull, a little thicker (we look at its outside)."""
    a = math.radians(tilt)
    outer = _ell_pts(x, y, rx + 3, ry + 3, a, 160)
    inner = _ell_pts(x, y, rx - 9, ry - 8, a, 160)
    o, i = outer[:81], inner[:81]
    p.poly(o + i[::-1], (40, 42, 52), INK, 2.6)
    for k in range(6, 76, 7):                                        # tiny lights along the hull
        mx, my = (o[k][0] + i[k][0]) / 2, (o[k][1] + i[k][1]) / 2
        p.ell(mx, my, 1.6, 1.6, (236, 230, 190), None, n=8)


def space_wide():
    """Shot 1's painting (RGBA, at SS). The armada flies over it (the film draws the cars)."""
    img = B.canvas(SPACE)
    cam = cam_wide()
    p = B.Pen(img, cam)
    _nebula(p, (640, 760), -25, 14, 260, [NEB_V, NEB_B, (54, 30, 80)], 5)
    _nebula(p, (900, 1500), 30, 8, 220, [NEB_B, (20, 28, 60)], 9)
    _stars(p, (0, 0, 1080, 1920), 520, 11)
    _galaxy_core(p, *CORE)
    _stars(p, (CORE[0] - 300, CORE[1] - 70, CORE[0] + 300, CORE[1] + 70), 60, 12, (0.8, 2.0))
    _halo_far(p, *HALO)
    _planet(img, cam, p, *PLANET, PLANET_COL, night=(0.42, 0.22), seed=3, lit_from=(1, 0.75))
    _halo_far(p, *HALO)                    # the far half shows against the planet too (it is in front of it)
    _halo_near(p, *HALO)
    return img


# ================================================ SHOT 6: THE RING CLOSE-UP ========================================
# The ring as a real circle (radius 1, its axis up), seen from just outside the hull and a little below it.
RING_W = 0.064                               # Halo: 318 km wide, 10,000 km across
RING_CAM = dict(pos=(1.06, 0.0, -0.06), fwd=(-0.5, 1.0, 0.3), f=1900.0, roll=-80.0, at=(470, 900))


class RingCam:
    def __init__(self, pos, fwd, f, roll, at):
        self.C = np.array(pos, float)
        F = np.array(fwd, float)
        self.F = F / np.linalg.norm(F)
        Rt = np.cross(self.F, [0, 0, 1.0])
        self.Rt = Rt / np.linalg.norm(Rt)
        self.U = np.cross(self.Rt, self.F)
        self.f, self.at = f, at
        self.c, self.s = math.cos(math.radians(roll)), math.sin(math.radians(roll))

    def __call__(self, P):
        """World point -> (screen x, y in world px, depth); None behind the camera."""
        d = np.asarray(P, float) - self.C
        z = d @ self.F
        if z < 2e-3:
            return None
        x, y = -(d @ self.Rt) / z * self.f, -(d @ self.U) / z * self.f
        return (self.at[0] + x * self.c - y * self.s, self.at[1] + x * self.s + y * self.c), z


def ring_point(th, h, lift=0.0):
    """A point on the hull (lift > 0: that far out from it, towards the camera's side)."""
    r = 1.0 + lift
    return (r * math.cos(th), r * math.sin(th), h)


def _surface_cols(n, seed):
    """The inner face's colour along the ring: seas, coasts, land, and cloud (ref 02)."""
    r = np.random.default_rng(seed)
    sea, deep, land, sand = (64, 126, 196), (46, 98, 170), (110, 150, 86), (196, 176, 122)
    out, v = [], 0.0
    for i in range(n):
        v = 0.92 * v + r.normal(0, 0.35)
        out.append(deep if v < -0.4 else sea if v < 0.15 else sand if v < 0.3 else land)
    return out


def ring_close():
    """Shot 6's painting (RGBA, at SS). The armada skims the hull over it (the film draws the cars)."""
    img = B.canvas(SPACE)
    cam = cam_wide()
    p = B.Pen(img, cam)
    rc = RingCam(**RING_CAM)
    _nebula(p, (760, 260), -35, 12, 240, [NEB_B, NEB_V], 21)
    _stars(p, (0, 0, 1080, 1920), 560, 22)
    # the blue galaxy band, top right (ref 02): lumpy flat layers along a diagonal, brightest in the middle
    a = math.radians(-58)
    gx, gy = 860, 420
    for k_, (w, col) in enumerate(((210, (30, 46, 100)), (130, (52, 88, 158)), (70, (110, 160, 214)), (26, (226, 240, 252)))):
        top, bot = [], []
        for u in np.linspace(-1, 1, 18):
            x, y = gx + u * 700 * math.cos(a), gy + u * 700 * math.sin(a)
            ww = w * (1 - 0.6 * u * u) * (1 + 0.22 * math.sin(u * 11 + k_))
            top.append((x - ww * math.sin(a), y + ww * math.cos(a)))
            bot.append((x + ww * math.sin(a) * 0.8, y - ww * math.cos(a) * 0.8))
        p.poly(rough(curve(top + bot[::-1], 3), 6, w), col, None)
    _stars(p, (500, 0, 1080, 900), 110, 23, (0.8, 2.2))
    # the planet behind, on the left, mostly in shadow (lit from the right)
    _planet(img, cam, p, -120, 1300, 560, (150, 96, 64), night=(1.15, 0.3), seed=4, lit_from=(1, -0.2))
    _ring(img, p, rc)
    return img


def _ring(img, p, rc):
    n, rows = 900, 6
    th0, th1 = math.radians(-10), math.radians(200)
    cols = _surface_cols(n, 7)
    quads = []
    r = np.random.default_rng(31)
    for i in range(n):
        a0 = th0 + (th1 - th0) * i / n
        a1 = th0 + (th1 - th0) * (i + 1) / n
        mid = (a0 + a1) / 2
        rad = np.array([math.cos(mid), math.sin(mid), 0.0])
        outer = (rc.C - np.array([math.cos(mid), math.sin(mid), 0])) @ rad > 0
        for j in range(rows):
            h0 = -RING_W / 2 + RING_W * j / rows
            h1 = h0 + RING_W / rows
            P = [rc(ring_point(a, h)) for a, h in ((a0, h0), (a1, h0), (a1, h1), (a0, h1))]
            if any(q is None for q in P):
                continue
            pts = [q[0] for q in P]
            depth = sum(q[1] for q in P) / 4
            if outer:
                panel = (i // 6 + j) % 3
                col = (46, 52, 48) if panel == 0 else (40, 46, 43) if panel == 1 else (52, 57, 52)
            else:
                col = cols[i] if j in (1, 2, 3, 4) else (92, 98, 96)                     # rim walls at the edges
            quads.append((depth, pts, col, outer, i, j))
    quads.sort(key=lambda q: -q[0])
    for depth, pts, col, outer, i, j in quads:
        p.poly(pts, col, None)
    # clouds over the inner face, in drifting banks stretched along the ring; kept to the land strip where it shows
    # (a mask drawn far to near, so the nearer hull still hides them and none hangs off the rim)
    cam = p.cam
    vis = Image.new('L', img.size, 0)
    dv = ImageDraw.Draw(vis)
    for depth, pts, col, outer, i, j in quads:
        dv.polygon([cam.P(*q) for q in pts], fill=255 if (not outer and j in (1, 2, 3, 4)) else 0)
    cloud = np.convolve(r.normal(0, 1, n), np.ones(9) / 9, 'same')

    def clouds(lay):
        q_ = B.Pen(lay, cam)
        for depth, pts, col, outer, i, j in quads:
            if not outer and j in (1, 2, 3, 4) and cloud[i] > 0.26 + 0.12 * abs(j - 2.5) and i % 2 == 0:
                cx, cy = sum(x for x, _ in pts) / 4, sum(y for _, y in pts) / 4
                along = math.dist(pts[0], pts[1]) * 2.4 + 1.5
                across = math.dist(pts[0], pts[3]) * 0.75 + 1.0
                rot = math.atan2(pts[1][1] - pts[0][1], pts[1][0] - pts[0][0])
                q_.ell(cx, cy, along, across, (238, 242, 246), None, rot=rot, n=12)
    _layer_masked(img, vis, clouds)
    seam = (28, 32, 30)
    for depth, pts, col, outer, i, j in quads:
        if not outer:
            continue
        size = math.dist(pts[0], pts[2])
        if i % 6 == 0 and size > 6:
            p.line([pts[0], pts[3]], seam, max(1.2, min(4, size / 30)))
        if j > 0 and size > 10:
            p.line([pts[0], pts[1]], seam, max(1.0, min(3, size / 40)))
        if size > 26 and (i % 12 == 3) and j in (1, 4):          # round ports (ref 02)
            cx, cy = sum(x for x, _ in pts) / 4, sum(y for _, y in pts) / 4
            rr = size * 0.22
            p.ell(cx, cy, rr, rr * 0.8, (26, 30, 30), INK, max(1.0, min(3, size / 40)))
            p.ell(cx, cy, rr * 0.55, rr * 0.45, (60, 66, 62), None)
        if size > 5:                                            # specks of light
            for k in range(1 + int(size / 40)):
                if r.random() < 0.45:
                    u, v = r.uniform(0.1, 0.9), r.uniform(0.1, 0.9)
                    x = pts[0][0] + (pts[1][0] - pts[0][0]) * u + (pts[3][0] - pts[0][0]) * v
                    y = pts[0][1] + (pts[1][1] - pts[0][1]) * u + (pts[3][1] - pts[0][1]) * v
                    s_ = max(1.0, min(3.2, size / 60))
                    p.ell(x, y, s_, s_, (240, 228, 170) if r.random() < 0.7 else (200, 220, 255), None, n=8)
    # outlines: trace each band edge per face
    for outer in (True, False):
        for edge_j, edge_h in ((0, -RING_W / 2), (5, RING_W / 2)):
            run = []
            for depth, pts, col, o, i, j in sorted((q for q in quads if q[3] == outer and q[5] == edge_j), key=lambda q: q[4]):
                run.append(pts[0] if edge_j == 0 else pts[3])
            if len(run) > 1:
                p.line(run, INK, 4)
    # the silhouette where the hull turns away (the band's end, seen side on)
    turn = [q for q in quads if q[3]]
    if turn:
        last = max(turn, key=lambda q: q[4])[4]
        ends = sorted((q for q in turn if q[4] == last), key=lambda q: q[5])
        p.line([ends[0][1][1]] + [q[1][2] for q in ends], INK, 4)


# ================================================ SHOTS 2-5: THE CABIN =============================================
ROOF = (26, 26, 30)
TRIM = (40, 40, 46)
SEAT = (238, 238, 234)
SEAT_D = (204, 204, 202)
SEAT_P = (226, 226, 222)     # the textured middle panel (ref 05)
RED = (226, 46, 52)


def _space_in(img, cam, pts, seed, t=0.0, drift=None):
    """A window onto space: dark sky and stars, clipped to the window; a Roadster drifting past if `drift` (0..1)."""
    mask = _poly_mask(img, cam, pts)

    def paint(lay):
        q = B.Pen(lay, cam)
        xs, ys = [x for x, _ in pts], [y for _, y in pts]
        box = (min(xs), min(ys), max(xs), max(ys))
        q.poly(pts, SPACE, None)
        _nebula(q, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), -20, 5, (box[2] - box[0]) * 0.3, [NEB_V, NEB_B], seed)
        area = (box[2] - box[0]) * (box[3] - box[1])
        _stars(q, box, int(area / 1500), seed + 1)
        if drift is not None:
            import roadster as RD
            x = box[0] - 120 + (box[2] - box[0] + 240) * drift
            y = box[1] + (box[3] - box[1]) * 0.32 + 30 * drift
            RD.car(lay, cam, x, y, 0.30, RD.View(yaw=-30 + 40 * drift, elev=18, flip=25 * drift, roll=10), smoke=False)
    _layer_masked(img, mask, paint)


def _seat(p, img, cam, cx, plate=True):
    """A white Roadster sport seat, front on (refs 03-05): a tall back with shoulder wings, the headrest built in with
    the black ROADSTER plate, grey side bolsters (the right one in flat shadow: the light comes from the upper left)."""
    k = PX_M
    Y = lambda v: CUSHION_Y - v * k
    X = lambda u: cx + u * k
    out = [(-0.13, 0.86), (0.13, 0.86), (0.155, 0.80), (0.145, 0.67), (0.25, 0.62), (0.28, 0.48), (0.27, 0.04),
           (-0.27, 0.04), (-0.28, 0.48), (-0.25, 0.62), (-0.145, 0.67), (-0.155, 0.80)]
    pts = rough([(X(u), Y(v)) for u, v in out], 2, int(cx))
    p.poly(curve(pts, 4), SEAT, INK, 4)
    for sg in (-1, 1):                                                   # the side bolsters
        bol = [(sg * 0.17, 0.60), (sg * 0.25, 0.60), (sg * 0.272, 0.48), (sg * 0.262, 0.06), (sg * 0.17, 0.06), (sg * 0.155, 0.40)]
        p.poly(curve([(X(u), Y(v)) for u, v in bol], 3), SEAT_D if sg > 0 else SEAT, INK, 2.6)
    panel = [(-0.155, 0.58), (0.155, 0.58), (0.15, 0.08), (-0.15, 0.08)]
    p.poly(rough([(X(u), Y(v)) for u, v in panel], 2, int(cx) + 1), SEAT_P, INK, 2.2)
    for v in (0.42, 0.25):                                               # stitched seams across the panel
        p.line([(X(-0.15), Y(v)), (X(0.15), Y(v + 0.005))], dk(SEAT_P, 0.82), 1.6)
    p.poly([(X(0.03), Y(0.86)), (X(0.13), Y(0.86)), (X(0.155), Y(0.80)), (X(0.145), Y(0.67)), (X(0.06), Y(0.67))],
           dk(SEAT, 0.93), None)                                         # the headrest's shadow side
    if plate:                                                            # the ROADSTER plate on the headrest (refs 04-05)
        pl = [(X(-0.095), Y(0.765)), (X(0.095), Y(0.765)), (X(0.085), Y(0.715)), (X(-0.085), Y(0.715))]
        p.poly(pl, (22, 22, 26), INK, 2)
        from press_secretary import stamp_text
        stamp_text(img, cam, 'ROADSTER', cx, Y(0.74), 0.15 * k, RED, font=SANS)


def cabin_back(img, cam, t=0.0, drift=None):
    """Everything behind Musk and Cortana. drift: where the passing Roadster is across the rear window (0..1), or None."""
    p = B.Pen(img, cam)
    # the roof: a black frame round two glass panels onto space (ref 03), receding to the rear window
    p.poly([(-40, -40), (1120, -40), (1120, 470), (-40, 470)], ROOF, None)
    g1 = [(150, -40), (930, -40), (900, 170), (180, 170)]
    g2 = [(196, 214), (884, 214), (868, 380), (212, 380)]
    _space_in(img, cam, g1, 41)
    _space_in(img, cam, g2, 43)
    for g in (g1, g2):
        p.poly(g, None, INK, 3)
    p.line([(180, 192), (900, 192)], (54, 54, 60), 6)                    # the cross bar's lit edge
    # the side windows, above the doors, onto space
    sl = [(-40, 120), (70, 420), (60, 760), (-40, 820)]
    sr = [(1120, 120), (1010, 420), (1020, 760), (1120, 820)]
    for g, sd in ((sl, 51), (sr, 53)):
        _space_in(img, cam, g, sd)
        p.poly(g, None, INK, 3)
    # the rear window, with the armada's stragglers beyond
    _space_in(img, cam, WINDOW, 61, t, drift)
    p.poly(WINDOW, None, INK, 4)
    p.poly([(150, 430), (930, 430), (936, 452), (144, 452)], TRIM, INK, 2)          # the window's top frame
    # the rear bulkhead under the window: dark, with the red light strip and a speaker grille between the seats
    p.poly([(112, 800), (968, 800), (1000, 1340), (80, 1340)], (34, 34, 38), INK, 4)
    p.poly([(112, 800), (968, 800), (972, 826), (108, 826)], TRIM, INK, 2)
    p.line([(120, 842), (960, 842)], RED, 5)
    for gx in range(470, 600, 14):
        for gy in range(880, 1060, 14):
            p.ell(gx, gy, 3, 3, (20, 20, 24), None, n=8)
    # the doors at the frame edges: dark panels, a red light strip, a handle
    for sg, x0, x1 in ((-1, -40, 112), (1, 1120, 968)):
        d = [(x0, 820), (x1, 800), (x1 + sg * 30, 1340), (x0, 1420)]
        p.poly(d, (30, 30, 34), INK, 4)
        p.poly([(x0, 820), (x1, 800), (x1 + sg * 3, 830), (x0, 852)], TRIM, None)           # the door's top rail
        p.line([(x0, 1110), (x1 + sg * 14, 1040)], RED, 6)                                # ref 03's red strip
        hx = x1 - sg * 40
        p.poly(rough([(hx - 26, 960), (hx + 26, 956), (hx + 24, 976), (hx - 24, 980)], 1, 70 + sg), (70, 70, 78), INK, 2)
    # the centre console between the seats (black, a silver edge, cup holders)
    p.poly([(452, 1090), (560, 1090), (600, 1340), (420, 1340)], (24, 24, 28), INK, 3)
    p.line([(452, 1094), (560, 1094)], (126, 126, 134), 3)
    for cy in (1150, 1210):
        p.ell(506, cy, 30, 12, (12, 12, 14), INK, 2)
    # the seats: the passenger's (frame left, Cortana above it), the driver's (behind Musk)
    _seat(p, img, cam, SEAT_X['passenger'])
    _seat(p, img, cam, SEAT_X['driver'])
    # the back of the centre screen on its stalk between the seats (ref 05), clear of Musk's arms; the dash hides its foot
    scr = [(424, 1196), (540, 1184), (548, 1300), (432, 1310)]
    p.poly(scr, (20, 20, 24), INK, 4)
    p.poly([(540, 1184), (548, 1300), (556, 1296), (548, 1182)], (110, 110, 118), INK, 2)
    p.poly([(474, 1306), (504, 1303), (508, 1340), (478, 1343)], (40, 40, 46), INK, 2)


def cabin_front(img, cam):
    """The dash, nearest the camera: over Musk's lap and the yoke's column."""
    p = B.Pen(img, cam)
    top = [(-40, DASH_Y + 30), (200, DASH_Y + 6), (540, DASH_Y - 6), (880, DASH_Y + 2), (1120, DASH_Y + 26)]
    body = curve(top + [(1120, 2000), (-40, 2000)], 4)
    p.poly(body, (30, 30, 34), INK, 4)
    lip = top + [(x, y + 26) for x, y in top[::-1]]
    p.poly(rough(lip, 1, 81), (50, 50, 56), INK, 2.6)                  # the dash's rounded far edge
    p.line([(x, y + 34) for x, y in top], RED, 4)                       # the red light strip under it (ref 03)
    # lumps of soft-touch shading and the defroster slots by the windscreen (nearest us)
    r = np.random.default_rng(83)
    for i in range(6):
        x, y = r.uniform(60, 1020), r.uniform(1450, 1700)
        p.poly(rough(_ell_pts(x, y, r.uniform(80, 160), r.uniform(20, 36), 0, 16), 6, 90 + i), (33, 33, 38), None)
    p.line([(x, y + 150) for x, y in top], (22, 22, 26), 2.4)          # the seam where the dash top meets its face
    for gx_, sg in ((150, -1), (930, 1)):                              # the tweeter grilles in the dash corners
        p.ell(gx_, 1400, 56, 22, (22, 22, 26), INK, 2.4)
        for k in range(-3, 4):
            p.line([(gx_ + k * 12, 1386), (gx_ + k * 12, 1414)], (48, 48, 54), 1.6)
    for row, y in enumerate((1770, 1810)):
        for x in range(90 + row * 20, 1000, 46):
            p.poly([(x, y), (x + 30, y), (x + 30, y + 10), (x, y + 10)], (16, 16, 18), None)


# ================================================ THE SHEET ========================================================
def _ref(i, w, h):
    im = Image.open(os.path.join(REFS, f'{i:02d}.jpg')).convert('RGB')
    k = min(w / im.width, h / im.height)
    return im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)


def sheet(out):
    import halo_cast as HC
    tiles = []
    img = space_wide()
    tiles.append(('1. shot 1: the wide (ref 01)', img, 1))
    img = ring_close()
    tiles.append(('2. shot 6: the ring close-up (ref 02)', img, 2))
    for lab, cam, drift in (('3. cabin, wide (shots 2, 4)', cam_wide(), 0.45), ('4. cabin, close (shots 3, 5)', cam_close(), None)):
        img = B.canvas(SPACE)
        cabin_back(img, cam, 0.0, drift)
        HC.chief(img, cam, *MUSK, dict(turn=-12))
        if cam.z == 1.0:
            HC.cortana(img, cam, *CORTANA_AT, 0.36, dict(pose='point', hip=-0.8), t=1.0)
        cabin_front(img, cam)
        tiles.append((lab, img, 3 if cam.z == 1.0 else 5))
    img = B.canvas(SPACE)
    cabin_back(img, cam_wide(), 0.0, None)
    cabin_front(img, cam_wide())
    tiles.append(('5. cabin, empty', img, 4))
    W_, H_, band, rw = 432, 768, 44, 300
    S = Image.new('RGB', (len(tiles) * (W_ + 8) + 8, H_ + band + rw + 30), (36, 36, 36))
    d = ImageDraw.Draw(S)
    f = ImageFont.truetype(SANS, 18)
    for i, (lab, im, ref) in enumerate(tiles):
        x = 8 + i * (W_ + 8)
        S.paste(im.convert('RGB').resize((W_, H_), Image.LANCZOS), (x, band))
        d.text((x + 2, 12), lab, font=f, fill=(255, 255, 255))
        r = _ref(ref, W_, rw)
        S.paste(r, (x, band + H_ + 20))
        d.text((x + 4, band + H_ + 24), f'ref {ref:02d}', font=f, fill=(255, 230, 0))
    S.save(out, quality=90)
    print('wrote', out)


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
    else:
        print(__doc__)
