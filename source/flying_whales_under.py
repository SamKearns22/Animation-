#!/usr/bin/env python3
"""Flying Whales, the underwater set (opening scene): open blue water at dusk, painted by view direction for any
camera, so it turns with the camera's swing (rule 39: 2D, no 3D model of the water).

What is in it (Showstopper list U1-U4, U14, and my additions Sam said yes to: dusk light, the shoal, bubbles, specks):
- the water: flat bands by how far up or down you look (deep navy below, teal level, lighter teal above), their edges
  hand-cut wavy along the compass so they move as the camera turns; warmer towards the sun's side;
- the surface seen from below (the plane z = 0): a bright ceiling broken into ripple shapes fixed on the water (so they
  slide past as the camera moves), with the round bright "window" overhead (inside about 48 degrees of straight up you
  see the dusk sky through it: warm gold; outside it the surface mirrors the deep water: silvery teal); it fades into
  the blue about 45 m off, leaving its hard far edge (benchmark B2, B8, B10);
- light shafts: flat, see-through pale wedges slanting down from the surface away from the sun, swaying (B3);
- specks (marine snow): fixed in the water, drifting slowly down; the only fixed things in open water, so they show
  the camera's move (B7);
- bubbles: streams from each whale's blowhole once they rise, left behind in the water and floating up (B4);
- the fish shoal: about 120 small silver fish milling in a ball on the pod's path; they scatter away from each whale as
  it charges through, then drift back (U14);
- distance haze: everything fades into the level-water colour with distance (B5), `haze`.

The world is whale.py's (x right, y away from the first camera, z up; m); the sea surface is z = 0.

    import flying_whales_under as U
    img = U.compose(cam, t, sprites, blowholes)     # sprites: whale Sprites (their .depth sorts them in)
    python3 source/flying_whales_under.py sheet OUT.jpg   the set alone and with the pod at the opener's four moments
"""
import functools
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import whale as W                                     # noqa: E402
from flying_whales_sea import LINE                    # noqa: E402  (the film's line weight, note 18)

INK = W.INK

# where the light comes from: the sun has just set (the same evening as the rig scene), ahead of the pod and to its
# left (+x, +y), so on the rise they race up and to the right towards the glow (rule 16 with the rig scene)
SUN_AZ = math.radians(40.0)                           # compass angle of the sun from +x towards +y
SUN = np.array([math.cos(SUN_AZ), math.sin(SUN_AZ)])
WINDOW = 90.0 - 48.6                                  # elevation above which you see the sky through the surface

# the water: (top edge, degrees of elevation, from the bottom up; colour); the edges wobble along the compass
WATER = [
    (-34.0, (6, 16, 48)),        # deep navy, straight down
    (-14.0, (10, 32, 84)),
    (-3.0, (16, 54, 118)),
    (8.0, (22, 78, 140)),        # level: the haze colour (the refs' Blue Planet blue, a shade darker for dusk)
    (19.0, (34, 102, 158)),
    (90.0, (54, 128, 174)),      # looking up
]
HAZE = WATER[3][1]
WARM = [(30, 100, 150), (52, 128, 168), (86, 154, 178)]   # the top three bands on the sun's side
# the surface from below, by distance (near -> far): inside the window, outside it; and the ripple tones
WIN = [(252, 226, 180), (240, 196, 172)]              # the window: warm gold towards the sun, peach-pink away
WIN_RIP = (255, 242, 212)
MIRROR = [(98, 158, 192), (76, 138, 178), (58, 116, 164)]
MIRROR_RIP = [(142, 192, 212), (112, 170, 198), (86, 144, 182)]
FAR = (30.0, 46.0)                                    # ripples stop, then the surface itself fades into the blue
SHAFT = (196, 228, 232)
SPECK = (200, 226, 236)
FISH = ((150, 174, 188), (214, 228, 230))             # silver back, pale belly
BUBBLE = ((222, 242, 244), (150, 196, 206))           # lit, rim


def _mix(a, b, k):
    return tuple(int(round(a[i] + (b[i] - a[i]) * k)) for i in range(3))


def haze(d):
    """How far (0-1) something d metres away has faded into the water (the opener's whales use the same)."""
    return 1.0 - math.exp(-max(d - 12.0, 0.0) / 40.0)


def _rays(cam, ss):
    w, h = cam.size
    xs = (np.arange(w * ss) + 0.5) / ss
    ys = (np.arange(h * ss) + 0.5) / ss
    a, b = np.meshgrid((xs - w / 2) / cam.focal, (h / 2 - ys) / cam.focal)
    d = a[..., None] * cam.R[0] + cam.R[1] + b[..., None] * cam.R[2]
    return d / np.linalg.norm(d, axis=-1, keepdims=True)


def _wobble(az, k):
    """Hand-cut wobble of band edge k along the compass (degrees)."""
    return (1.6 * np.sin(3 * az + 1.3 * k) + 0.9 * np.sin(7 * az + 2.1 * k + 0.5) + 0.5 * np.sin(13 * az + k))


def _ripple(x, y, t):
    """The surface's ripple field on the water (m): a few slow crossing waves; high where the light gathers."""
    f = np.zeros_like(x)
    for kx, ky, w, ph in ((0.95, 0.30, 0.9, 0.0), (-0.40, 1.10, 1.1, 1.7), (0.62, -0.85, 0.7, 3.1),
                          (-1.30, -0.35, 1.3, 4.4), (0.25, 1.55, 1.6, 2.2)):
        f += np.sin(kx * x + ky * y + w * t + ph)
    return f


def water(cam, t, ss=1):
    """The back layer: water bands, the surface from below and its ripples. RGB uint8 at the frame size."""
    d = _rays(cam, ss)
    el = np.degrees(np.arcsin(np.clip(d[..., 2], -1, 1)))
    az = np.arctan2(d[..., 1], d[..., 0])
    sun = np.cos(az - SUN_AZ)                                     # 1 towards the sun, -1 away
    img = np.zeros(el.shape + (3,), np.uint8)
    band = np.zeros(el.shape, int)
    for k, (top, _) in enumerate(WATER[:-1]):
        dome = 5.0 * np.clip(sun, 0, 1) ** 3 if k >= 3 else 0.0   # warm bands swell down towards the sun
        band += el > (top + _wobble(az, k) - dome)
    img[:] = np.array([c for _, c in WATER], np.uint8)[band]
    warm = (el > 6.0 + 26.0 * (0.9 - sun) + 1.5 * np.sin(5 * az)) & (band >= 3)   # a dome of glow round the sun
    img[warm] = np.array(WARM, np.uint8)[np.clip(band[warm] - 3, 0, 2)]
    # the surface: where each upward ray meets z = 0
    up = d[..., 2] > 0.01
    r = np.where(up, -cam.pos[2] / np.maximum(d[..., 2], 1e-3), 1e9)       # distance along the ray
    sx = cam.pos[0] + d[..., 0] * r
    sy = cam.pos[1] + d[..., 1] * r
    far_edge = FAR[1] + 3.0 * np.sin(0.21 * sx + 0.13 * sy) + 2.0 * np.sin(0.47 * sy - 0.3 * sx)
    surf = up & (r < far_edge)
    f = _ripple(sx, sy, t)
    win = surf & (el > WINDOW + 1.2 * np.sin(4 * az + 0.7 * t))
    mir = surf & ~win
    near = np.digitize(r, [14.0, FAR[0]])                            # 0 near, 1 mid, 2 far
    img[mir] = np.array(MIRROR, np.uint8)[near[mir]]
    rip = mir & (f > 1.1 + 0.5 * near) & (r < FAR[0] + 6)
    img[rip] = np.array(MIRROR_RIP, np.uint8)[near[rip]]
    wc = np.where(sun > 0.2, 0, 1)
    img[win] = np.array(WIN, np.uint8)[wc[win]]
    img[win & (f > 1.0)] = WIN_RIP
    # thin dark-teal cracks between the bright cells overhead (the broken look of the surface from below)
    crack = surf & (np.abs(f + 0.6) < 0.16) & (r < FAR[0])
    img[crack & win] = _mix(WIN[0], MIRROR[0], 0.45)
    im = Image.fromarray(img)
    if ss != 1:
        im = im.resize(cam.size, Image.LANCZOS)
    return im


# ------------------------------------------------- light shafts -----------------------------------------------------
def _clip_near(Q, near=0.4):
    """Clip a polygon in camera space (x right, y depth, z up) to y >= near."""
    out = []
    n = len(Q)
    for i in range(n):
        a, b = Q[i], Q[(i + 1) % n]
        ia, ib = a[1] >= near, b[1] >= near
        if ia:
            out.append(a)
        if ia != ib:
            k = (near - a[1]) / (b[1] - a[1])
            out.append(a + (b - a) * k)
    return out


def _poly(cam, P):
    Q = _clip_near([q for q in cam.cam(np.asarray(P, float))])
    if len(Q) < 3:
        return None
    w, h = cam.size
    return [(w / 2 + cam.focal * q[0] / q[1], h / 2 - cam.focal * q[2] / q[1]) for q in Q]


@functools.lru_cache(None)
def _shafts():
    """[(top point on the surface, width m, length m, sway phase, strength)] over the opener's water."""
    r = np.random.default_rng(7)
    out = []
    for _ in range(110):
        p = np.array([r.uniform(-50, 90), r.uniform(-50, 40), 0.0])
        out.append((p, r.uniform(0.5, 2.2), r.uniform(22, 40), r.uniform(0, 2 * math.pi), r.uniform(0.5, 1.0)))
    return out


SHAFT_DIR = np.array([-SUN[0] * math.sin(math.radians(36)), -SUN[1] * math.sin(math.radians(36)),
                      -math.cos(math.radians(36))])          # down and away from the sun, 36 deg from straight down


def shafts(cam, t, layer):
    """Flat see-through wedges (two strengths) slanting down from the surface, swaying; drawn onto RGBA layer."""
    w, h = cam.size
    lay = Image.new('RGBA', cam.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(lay)
    for p, wd, ln, ph, k in _shafts():
        sway = np.array([math.sin(0.5 * t + ph), math.cos(0.4 * t + 1.3 * ph), 0.0]) * 0.8
        top = p + sway
        bot = top + SHAFT_DIR * ln
        mid = (top + bot) / 2
        view = mid - cam.pos
        if np.linalg.norm(view) > 60:
            continue
        side = np.cross(SHAFT_DIR, view)
        side /= np.linalg.norm(side) + 1e-9
        a1 = (0.11 + 0.06 * math.sin(0.9 * t + 2 * ph)) * k
        # a wedge from the surface narrowing to a point, fading in three flat steps (no gradient: house style)
        for f0, f1, alpha in ((0.0, 0.45, a1), (0.45, 0.75, a1 * 0.6), (0.75, 1.0, a1 * 0.3)):
            w0, w1 = wd * (1 - 0.85 * f0) * 0.5, wd * (1 - 0.85 * f1) * 0.5
            p0, p1 = top + (bot - top) * f0, top + (bot - top) * f1
            q = _poly(cam, [p0 - side * w0, p0 + side * w0, p1 + side * w1, p1 - side * w1])
            if q:
                dr.polygon(q, fill=SHAFT + (int(255 * alpha),))
    layer.alpha_composite(lay)
    return layer


# ------------------------------------------------- specks -----------------------------------------------------------
CELL = 60.0                                            # specks repeat every 60 m (beyond the fog), fixed in the water


@functools.lru_cache(None)
def _speck_pool():
    r = np.random.default_rng(3)
    n = int(CELL ** 3 * 0.022)
    return r.uniform(0, CELL, (n, 3)), r.uniform(0.012, 0.04, n), r.uniform(0, 2 * math.pi, n)


def specks(cam, t):
    """[(depth, kind, data)]: each visible speck (world-fixed, drifting down) as a dot to draw in depth order."""
    q, size, ph = _speck_pool()
    drift = np.stack([0.05 * np.sin(0.3 * t + ph), 0.05 * np.cos(0.25 * t + ph), np.full_like(ph, -0.03 * t)], 1)
    p = q + drift
    p = p + CELL * np.round((cam.pos - p) / CELL)                 # the copy of each speck nearest the camera
    under = p[:, 2] < -0.3
    p, sz = p[under], size[under]
    P, z = cam.screen(p)
    w, h = cam.size
    ok = (z > 0.8) & (z < 34) & (P[:, 0] > -8) & (P[:, 0] < w + 8) & (P[:, 1] > -8) & (P[:, 1] < h + 8)
    out = []
    for (x, y), d, s in zip(P[ok], z[ok], sz[ok]):
        rr = min(7.0, max(1.1, s * cam.focal / d))
        out.append((float(d), 'speck', (x, y, rr)))
    return out


# ------------------------------------------------- bubbles ----------------------------------------------------------
RATE = 60.0                                           # bubbles a second from each blowhole


def bubbles(cam, t, blowhole, since, whales=5):
    """[(depth, kind, data)] for the bubble streams. blowhole(t, k) -> world point of whale k's blowhole at time t;
    they stream from time `since` on, each left where it was let go and floating up, wobbling, growing a little."""
    out = []
    if t <= since:
        return out
    w, h = cam.size
    n0 = int(since * RATE)
    n1 = int(t * RATE)
    for k in range(whales):
        for n in range(max(n0, n1 - int(3.0 * RATE)), n1 + 1):
            te = n / RATE
            if te < since or te > t:
                continue
            rnd = np.random.default_rng(1000 * k + n)
            age = t - te
            base = blowhole(te, k)
            jit = rnd.normal(0, 0.25, 3)
            rise = rnd.uniform(0.7, 1.4)
            size = rnd.uniform(0.06, 0.2) * (1 + 0.3 * age)
            ph = rnd.uniform(0, 2 * math.pi)
            p = base + jit + np.array([0.12 * math.sin(6 * age + ph), 0.12 * math.cos(5 * age + ph), rise * age])
            if p[2] > -0.2:
                continue
            P, d = cam.screen(p)
            if d < 0.8 or d > 40 or not (-20 < P[0] < w + 20 and -20 < P[1] < h + 20):
                continue
            out.append((float(d), 'bubble', (float(P[0]), float(P[1]), max(1.3, size * cam.focal / d))))
            if rnd.random() < 0.35:                                   # a small one tagging along
                P2, d2 = cam.screen(p + rnd.normal(0, 0.18, 3))
                if d2 > 0.8:
                    out.append((float(d2), 'bubble', (float(P2[0]), float(P2[1]), max(1.1, 0.5 * size * cam.focal / d2))))
    return out


# ------------------------------------------------- the fish shoal ---------------------------------------------------
SHOAL_C = np.array([17.0, -3.5, -13.0])               # on the pod's path: the lead charges through at about 2.6 s
SHOAL_R = np.array([4.5, 3.0, 2.4])
N_FISH = 120
FISH_L = 0.26                                         # m


@functools.lru_cache(None)
def _shoal_sim(pod_key):
    """Positions and headings of every fish at 48 steps a second from t = 0 to 6 s (fixed, so every frame agrees).
    pod_key names the pod's motion (flying_whales_opener.poses), read through _POD."""
    pod = _POD[pod_key]
    rnd = np.random.default_rng(19)
    dt = 1 / 48
    u = rnd.normal(0, 1, (N_FISH, 3))
    u /= np.linalg.norm(u, axis=1, keepdims=True)
    home = u * SHOAL_R * rnd.uniform(0.35, 1.0, (N_FISH, 1)) ** 0.5
    pos = SHOAL_C + home
    vel = np.zeros((N_FISH, 3))
    spin = 0.35                                                      # the ball mills round (rad/s)
    out_p, out_h = [], []
    steps = int(6.0 / dt) + 1
    for i in range(steps):
        t = i * dt
        ang = spin * t
        c, s = math.cos(ang), math.sin(ang)
        hm = home @ np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
        target = SHOAL_C + hm
        mill = np.cross(np.array([0, 0, 1.0]), hm) * spin            # swimming round the ball
        acc = (target - pos) * 2.2 + (mill - vel) * 1.6
        for a, b, rad in pod(t):                                     # each whale: its axis (tail a -> snout b)
            ab = b - a
            k = np.clip(((pos - a) @ ab) / (ab @ ab), 0, 1)
            near = a + k[:, None] * ab
            off = pos - near
            dist = np.linalg.norm(off, axis=1)
            push = np.clip(1 - (dist - rad) / 6.0, 0, 1) ** 2
            acc += off / (dist[:, None] + 1e-6) * push[:, None] * 160.0
        vel = vel + acc * dt
        sp = np.linalg.norm(vel, axis=1, keepdims=True)
        vel = np.where(sp > 9.0, vel / sp * 9.0, vel)
        pos = pos + vel * dt
        out_p.append(pos.copy())
        hd = vel + mill * 0.3
        out_h.append(hd / (np.linalg.norm(hd, axis=1, keepdims=True) + 1e-9))
    return np.array(out_p), np.array(out_h)


_POD = {}


def set_pod(key, fn):
    """Register the pod's motion: fn(t) -> [(tail point, snout point, body radius m)] for each whale."""
    _POD[key] = fn


def shoal(cam, t, pod_key):
    if pod_key not in _POD:
        return []
    P, H = _shoal_sim(pod_key)
    i = min(len(P) - 2, max(0, t * 48))
    i0 = int(i)
    k = i - i0
    pos = P[i0] * (1 - k) + P[i0 + 1] * k
    hd = H[i0] * (1 - k) + H[i0 + 1] * k
    out = []
    w, h = cam.size
    for n, (p, f) in enumerate(zip(pos, hd)):
        d = float(np.linalg.norm(p - cam.pos))
        if d > 40:
            continue
        upv = np.array([0, 0, 1.0]) - f * f[2]
        upv /= np.linalg.norm(upv) + 1e-9
        L = FISH_L * (0.85 + 0.3 * ((n * 37) % 11) / 10)
        wag = math.sin(14 * t + n) * 0.25
        side = np.cross(f, upv)
        pts3 = [p + f * L * 0.5,                               # nose
                p + f * L * 0.1 + upv * L * 0.17,              # back
                p - f * L * 0.3 + upv * L * 0.05,
                p - f * L * 0.42 + side * wag * L * 0.2,       # tail stock
                p - f * L * 0.3 - upv * L * 0.07,
                p + f * L * 0.1 - upv * L * 0.14]              # belly
        tail3 = [p - f * L * 0.42 + side * wag * L * 0.2,
                 p - f * L * 0.62 + upv * L * 0.16 + side * wag * L * 0.5,
                 p - f * L * 0.56 + side * wag * L * 0.45,
                 p - f * L * 0.62 - upv * L * 0.14 + side * wag * L * 0.5]
        S, z = cam.screen(np.array(pts3 + tail3))
        if (z < 0.6).any():
            continue
        if not ((-30 < S[:, 0]) & (S[:, 0] < w + 30) & (-30 < S[:, 1]) & (S[:, 1] < h + 30)).any():
            continue
        flash = (math.sin(3.1 * t + n * 1.7) > 0.93)                # a flank catching the light as it turns
        out.append((d, 'fish', ([tuple(s) for s in S[:6]], [tuple(s) for s in S[6:]], flash)))
    return out


# ------------------------------------------------- putting it together ----------------------------------------------
def _draw_small(dr, kind, data, d):
    k = haze(d)
    if kind == 'speck':
        x, y, r = data
        c = _mix(SPECK, HAZE, min(1.0, k * 1.3))
        dr.ellipse([x - r, y - r, x + r, y + r], fill=c + (255,))
    elif kind == 'bubble':
        x, y, r = data
        rim, lit = _mix(BUBBLE[1], HAZE, k), _mix(BUBBLE[0], HAZE, k)
        if r < 2.6:
            dr.ellipse([x - r, y - r, x + r, y + r], fill=lit + (255,))
        else:
            dr.ellipse([x - r, y - r, x + r, y + r], fill=rim + (255,), outline=_mix(INK, HAZE, k * 0.8) + (255,),
                       width=max(1, int(min(5, r * 0.28) * LINE)))
            dr.ellipse([x - r * 0.55, y - r * 0.62, x + r * 0.2, y + r * 0.05], fill=lit + (255,))
    elif kind == 'fish':
        body, tail, flash = data
        back, belly = (_mix(c, HAZE, k) for c in FISH)
        span = max(abs(body[0][0] - body[3][0]), abs(body[0][1] - body[3][1]))
        olw = 0 if span < 7 else max(1, int(min(3, span / 9) * LINE))
        ink = _mix(INK, HAZE, k * 0.8) + (255,)
        dr.polygon(tail, fill=back + (255,), outline=ink if olw else None, width=olw or 1)
        dr.polygon(body, fill=(_mix(belly, (255, 250, 236), 0.5) if flash else belly) + (255,),
                   outline=ink if olw else None, width=olw or 1)
        top = [body[0], body[1], body[2], body[3]]
        if span >= 5:
            dr.line(top, fill=back + (255,), width=max(1, int(span / 6)))


def compose(cam, t, sprites, blowhole=None, since=None, pod_key=None, ss=1):
    """One frame of the underwater set with the whales in it, nearest on top. RGB."""
    im = water(cam, t, ss).convert('RGBA')
    shafts(cam, t, im)
    items = specks(cam, t)
    if blowhole is not None and since is not None:
        items += bubbles(cam, t, blowhole, since)
    if pod_key is not None:
        items += shoal(cam, t, pod_key)
    items += [(s.depth, 'whale', s) for s in sprites]
    items.sort(key=lambda it: -it[0])
    lay = Image.new('RGBA', cam.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(lay)
    for d, kind, data in items:
        if kind == 'whale':
            im.alpha_composite(lay)
            lay = Image.new('RGBA', cam.size, (0, 0, 0, 0))
            dr = ImageDraw.Draw(lay)
            data.paste(im)
        else:
            _draw_small(dr, kind, data, d)
    im.alpha_composite(lay)
    return im.convert('RGB')


# ------------------------------------------------- benchmark (rule 3) -----------------------------------------------
# notes/flying-whales.md, "Underwater benchmark" B1-B10; `python3 source/benchmark.py flying_whales_under OUT.jpg`
NAME = 'flying-whales'
_ITEMS = [
    ('B1 open water, no sea bed: bright above, navy below', 'done: six flat bands by view angle, no bed'),
    ('B2 the surface from below: a wavy ceiling of ripples', 'done: ripple shapes fixed on z = 0, sliding past'),
    ('B3 light shafts fanning down from the surface', 'done: 110 swaying wedges, fading in three flat steps'),
    ('B4 a trail of bubbles behind a whale', 'done: from each blowhole on the rise, left behind, floating up'),
    ('B5 distance fades whales into the blue', 'done: haze() on whales, fish, specks, bubbles'),
    ('B6 lit from above: backs bright, bellies shaded', 'done: whale.py light from above; flippers palest'),
    ('B7 small specks and bubbles hanging in the water', 'done: marine snow fixed in the water, drifting down'),
    ('B8 the surface underside as a hard far line', 'done: the ceiling ends in a hard wavy edge 46 m off'),
    ('B9 whales blue-grey (never black), white flippers', 'done: slate with a teal tint, never near-black'),
    ('B10 dusk: the surface glowing warm gold', 'done: the window overhead gold; deeper teal water'),
]
BENCHMARK = [
    dict(place='under the sea: the pod coming (2.0 s)', at=2.0, items=_ITEMS,
         refs=['whale-rear-three-quarter.jpg', 'whale-pod-from-above.jpg', 'whale-belly-flippers.jpg']),
    dict(place='under the sea: the rise (5.3 s)', at=5.3, items=_ITEMS,
         refs=['whale-side-painting.jpg', 'whale-side-under.jpg', 'whale-tail-behind.jpg']),
]


def picture(t):
    import flying_whales_opener as O
    return O.frame(t)[0]


# ------------------------------------------------- the sheet --------------------------------------------------------
def sheet(out):
    import flying_whales_opener as O
    tiles = []
    for t, lab, _ in O.MOMENTS:
        im, _ = O.frame(t, ss=2)
        tiles.append((lab, im))
    f = W._font(30)
    tw, th = 540, 960
    img = Image.new('RGB', (tw * len(tiles) + 10 * (len(tiles) + 1), th + 70), (244, 240, 232))
    d = ImageDraw.Draw(img)
    for i, (lab, im) in enumerate(tiles):
        x = 10 + i * (tw + 10)
        img.paste(im.resize((tw, th), Image.LANCZOS), (x, 60))
        d.text((x, 14), lab, font=f, fill=(30, 30, 34))
    img.save(out, quality=88)
    return out


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    else:
        print(__doc__)
