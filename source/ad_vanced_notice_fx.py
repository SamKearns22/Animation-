#!/usr/bin/env python3
"""MAP  Ad-Vanced Notice (8 Nov): the showstopper. In the cliff shot, behind Vance, a missile from Iran drops on the
moving tanker: orange flame-light and a hard jolt (no white flash: Sam, 8 Nov), a ring of spray over the water, a huge
oil fireball climbing for 4.6 s onto a column of fire that burns for good, flaming pieces (hull plating, deck plates,
pipe, a crane jib, the funnel top, scraps, burning oil) of many sizes tumbling into the sea with a splash each, black
smoke pouring from the fire's top and leaning with the wind, and the tanker torn in two, burning, the sea lit orange
(the showstopper list in notes/archive/ad-vanced-notice.md, items 4b-12; note 29).

Everything is laid out in metres in the strait's world (x right, y out to sea, z up; the near tanker 1.2 km out) and
drawn through whichever camera is given, so the close-up shows the same burning wreck and smoke. Flat house style:
flat tones, one ink outline, lumpy shapes (rule 15). The effects reuse Flying Whales' kit (flying_whales_fx: the
fireball lumps, smoke clumps, deck fire, splashes, flat-shape drawing), re-coloured for hazy daylight.

    python3 source/ad_vanced_notice_fx.py sheet OUT.jpg            key moments of the hit + the close-up's wreck
    python3 source/ad_vanced_notice_fx.py clip OUT.mp4 [--small]   the rehearsal clip (rule 40), silent

Map: timing 41 | the missile 88 | pieces 112 | fireball 233 | smoke 291 | glow 336 | blast ring 364 | blaze 390 | fx() 443 | light, jolt 485 | frames 540 | main 610

Use in the film (u = seconds since the missile lands; the film sets its own T_HIT):
    near(u)        the near tanker for sets.strait(): ('sail', x) before the hit, ('wreck', X_HIT) after
    fx(u)          fn(img, cam) for sets.strait(..., fx=): every effect behind the cliff top (any camera)
    light(img, u, cam)  the fire's orange light over the finished frame (people included)
    hellfire(layer, u)  someone's own layer lit orange from the fire's side (the close-up, note 31)
    held(u)        the 2-frame freeze on the hit: use held(u) as the time for everything in the shot
    jolt(u)        the camera jolt (px): shift the finished frame with shift(img, dx, dy)
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ad_vanced_notice_sets as S        # noqa: E402
import flying_whales_fx as FX            # noqa: E402

FPS = 12                                 # the satire films' rate (satire_template)
F = 1.0 / FPS

# ---------------------------------------------------------------------------------------------- timing (s from the hit)
MISSILE_T = 0.4                          # it drops in about 0.4 s
FREEZE_AT, FREEZE = 2 * F, 2 * F         # the 2-frame hold on the fireball's first big frame
FB_T = 4.6                               # the oil fireball swells, climbs and rolls up for 4.6 s, its top turning to
                                         # black smoke from 3.0 s while the blaze below it keeps burning (Sam, 8 Nov:
                                         # an oil fire rising, not one that dwindles into smoke and embers)
HIT = np.array([S.X_HIT, S.NEAR_Y, 8.0])  # amidships, on deck
FB_SIZE = 150.0                          # the fireball's lump size (m)
FB_SEED = 11
GP = 260.0                               # the flying pieces' gravity (m/s2): a cartoon cheat so a 150 m throw
                                         # lands in about 3 s (true gravity at 1.2 km looks like slow motion)
WIND = np.array([14.0, 0.0, 0.0])         # the smoke leans right
DAY_WATER = ((246, 250, 250), (196, 214, 218))
SMOKE = ((96, 90, 92), (44, 40, 44))     # lit (up and left: the high sun behind us to the left), shadow
FX.PUFF_COLS['oil'] = SMOKE
L = S.NEAR_L


def held(u):
    """The time everything in the shot shows: the clock stops for 2 frames on the fireball's first big frame."""
    if u <= FREEZE_AT:
        return u
    return u - min(u - FREEZE_AT, FREEZE)


def brk(u):
    """The tanker breaking in two (sets.tanker 'wreck'): most of it in the blast, then the halves keep settling."""
    if u < 0:
        return (0.0, 0.0, 0.0)
    a, b = 1 - math.exp(-u / 0.25), min(1.0, u / 7.0)
    ang, gap, sink = S.WRECK_FULL
    return (ang * (0.5 * a + 0.5 * b), gap * (0.55 * a + 0.45 * b), sink * b)


def near(u):
    if u < 0:
        return ('sail', S.near_x(u, 0.0))
    return ('wreck', S.X_HIT, brk(u))


def on_wreck(u_local, z, u):
    """A point of the tanker (u along the hull, z up, before the break) in the world at time u."""
    a, b = S.wreck_xform(u_local, z, L, brk(u))
    return np.array([S.X_HIT + a, S.NEAR_Y, b])


# ---------------------------------------------------------------------------------------------- the missile
M_FROM = np.array([470.0, -70.0])        # screen: in from the top left, steep (clear of Vance's head, x 270-450)


def missile_poly(u, cam):
    """The missile as a small black dart, no smoke trail (list 4b): screen polygon, or None when not in flight."""
    if not (-MISSILE_T <= u < 0):
        return None
    hx, hy = cam.screen(HIT)[0]
    k = ((u + MISSILE_T) / MISSILE_T) ** 1.5                    # speeding up as it falls
    p = M_FROM + (np.array([hx, hy - 6]) - M_FROM) * k
    d = np.array([hx, hy]) - M_FROM
    d /= np.linalg.norm(d)
    n = np.array([-d[1], d[0]])
    Lm, w = 56.0, 6.0
    nose, tail = p, p - d * Lm
    fin = tail + d * 7
    pts = [nose, p - d * 9 + n * w, fin + n * w, tail + n * 14, tail + n * 4, tail - n * 4, tail - n * 14, fin - n * w,
           p - d * 9 - n * w]
    return [tuple(q) for q in pts]


# ---------------------------------------------------------------------------------------------- flying pieces
FUNNEL_U, FUNNEL_Z = -L / 2 + 8.5, 9.0 + 21.0        # where the funnel top sat (wreck state cuts it off)

# kind: (count, size m, up speed m/s, side speed m/s, spin rad/s, flame size x the piece)
KINDS = {'hull': (3, (24, 40), (170, 230), (50, 110), (0.8, 1.6), 0.55),     # torn side plating, the red bottom on it
         'deck': (4, (17, 28), (250, 350), (40, 150), (2.0, 4.0), 0.7),      # deck plates, a pipe run across each
         'pipe': (4, (13, 24), (290, 420), (40, 160), (3.0, 6.0), 0.7),      # lengths of the deck pipe run, flanged
         'crane': (1, (22, 22), (330, 330), (70, 70), (2.5, 2.5), 0.6),      # a hose crane's jib from amidships
         'scrap': (9, (3, 8), (320, 480), (60, 200), (6.0, 10.0), 1.25),     # small burning scraps
         'gob': (5, (6, 12), (250, 380), (30, 120), (0.0, 0.0), 1.0)}        # flying blobs of burning oil


def _pieces():
    """Each piece: (kind, start, velocity m/s, size m, spin rad/s, seed, delay s). Thrown from the break, high and
    wide both ways (more to the right, away from Vance): big side plates low and heavy, small scraps highest and
    fastest; the funnel top a beat later as the blast reaches the stern, up and back."""
    rng = np.random.default_rng(23)
    out = []
    i = 0
    for kind, (n, sz, vz, vx, sp, _) in KINDS.items():
        for j in range(n):
            side = -1 if (i * 7 + 3) % 10 < 3 else 1                       # about 3 in 10 to the left
            start = HIT + np.array([rng.uniform(-14, 14), rng.uniform(-8, 4), -4.0 if kind == 'hull' else 4.0])
            sx = rng.uniform(*vx) if side > 0 else rng.uniform(20, 60)       # leftward ones kept short of Vance
            v = np.array([side * sx, rng.uniform(-35, 35), rng.uniform(*vz)])
            out.append((kind, start, v, rng.uniform(*sz), rng.choice([-1, 1]) * rng.uniform(*sp), 100 + i,
                        rng.uniform(0.0, 0.1)))
            i += 1
    out.append(('funnel', on_wreck(FUNNEL_U, FUNNEL_Z, 0.0), np.array([-60.0, -10.0, 400.0]), 24.0, -4.5, 300, 0.15))
    return out


PIECES = _pieces()


def piece_at(pc, u):
    """(position, velocity) at u, or None before it flies; after it meets the sea: ('sea', where, when)."""
    kind, p0, v0, size, spin, seed, delay = pc
    a = u - delay
    if a < 0:
        return None
    vz, z0 = v0[2], max(0.0, p0[2])
    t_sea = (vz + math.sqrt(vz * vz + 2 * GP * z0)) / GP
    if a >= t_sea:
        return ('sea', p0 + v0 * t_sea + np.array([0, 0, -0.5 * GP * t_sea ** 2]), delay + t_sea)
    return (p0 + v0 * a + np.array([0, 0, -0.5 * GP * a * a]), v0 + np.array([0, 0, -GP * a]))


def _jag(r, w, h, n, seed, squash=1.0):
    rng = np.random.default_rng(seed)
    a = np.linspace(0, 2 * math.pi, n, endpoint=False) + rng.uniform(-0.25, 0.25, n)
    q = rng.uniform(0.72, 1.0, n)
    return [(w / 2 * qq * math.cos(t), h / 2 * qq * math.sin(t) * squash) for qq, t in zip(q, a)]


def _piece_shape(kind, x, y, r, ang, seed):
    """A piece on screen, (body, inner) in local shapes turned by ang: never a stick or a line (rule 15).
    hull: a big bent slab of black side plating with the red bottom along one edge; deck: a rust-red deck plate with
    a stub of pale pipe across it; pipe: a fat length of pale pipe with a dark flange; crane: a white tapered jib with
    its dark hook block; funnel: the white drum with its black rim; scrap: a small dark jagged bit."""
    ca, sa = math.cos(ang), math.sin(ang)
    rot = lambda pts: [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts]
    if kind == 'funnel':
        w, h = r, r * 0.62
        body = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2 + 0.06 * w, h / 2), (-w / 2 - 0.04 * w, h / 2)]
        return rot(body), rot([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, -h / 4), (-w / 2, -h / 4)])
    if kind == 'hull':
        w, h = r * 1.5, r * 0.8
        body = [(-w / 2, -h * 0.42), (-w * 0.1, -h / 2), (w * 0.3, -h * 0.36), (w / 2, -h * 0.5), (w * 0.46, h * 0.1),
                (w / 2, h / 2), (-w * 0.2, h * 0.44), (-w * 0.46, h * 0.5)]
        red = S.clip_up(body, lambda p: p[1] - h * 0.18)                # the red bottom band along the lower edge
        return rot(body), rot(red)
    if kind == 'deck':
        w, h = r * 1.3, r * 0.85
        body = _jag(r, w, h, 6, seed)
        return rot(body), rot([(-w * 0.36, -h * 0.1), (w * 0.36, -h * 0.14), (w * 0.36, h * 0.08), (-w * 0.36, h * 0.12)])
    if kind == 'pipe':
        w, h = r * 1.4, r * 0.36
        body = [(-w / 2, -h / 2), (w / 2, -h / 2 + 0.06 * h), (w / 2, h / 2), (-w / 2, h / 2)]
        return rot(body), rot([(w * 0.3, -h / 2 + 0.06 * h), (w / 2, -h / 2 + 0.06 * h), (w / 2, h / 2), (w * 0.3, h / 2)])
    if kind == 'crane':
        w, h = r * 1.6, r * 0.34
        body = [(-w / 2, -h / 2), (w / 2, -h * 0.22), (w / 2, h * 0.22), (-w / 2, h / 2)]
        return rot(body), rot([(w * 0.28, -h * 0.26), (w / 2, -h * 0.22), (w / 2, h * 0.22), (w * 0.28, h * 0.26)])
    return rot(_jag(r, r * 1.2, r * 0.9, 5, seed)), None


PIECE_COLS = {'hull': ((40, 38, 40), (150, 40, 34)), 'deck': ((122, 62, 46), (196, 190, 176)),
              'pipe': ((196, 190, 176), (70, 66, 62)), 'crane': ((226, 222, 210), (50, 50, 54)),
              'funnel': ((232, 228, 220), (30, 30, 32)), 'scrap': ((52, 46, 46), None)}


def pieces_items(cam, u):
    """Flying pieces with their trailing flames: [(poly, colour, inner, inner colour)] far to near, and the splashes
    [(where, size, age, seed)] of the ones that have met the sea."""
    live, splashes = [], []
    for pc in PIECES:
        kind, p0, v0, size, spin, seed, delay = pc
        st = piece_at(pc, u)
        if st is None:
            continue
        if isinstance(st[0], str):
            splashes.append((st[1], size, u - st[2], seed))
            continue
        p, v = st
        s, d = cam.screen(p)
        if d < 1.0:
            continue
        rp = max(3.0, cam.focal * size / d * 1.3)                 # drawn a touch large so they read at 1.2 km
        fk = KINDS[kind][5] if kind in KINDS else 0.6
        s2, _ = cam.screen(p - v * 0.16)          # where it was a moment ago: the flame streams there, and up (fire rises)
        rf = max(2.5, rp * fk * 0.55)                 # the flame trails behind the piece, which leads, dark and clear
        bx, by = s[0] - (s[0] - s2[0]) * 0.35, s[1] - (s[1] - s2[1]) * 0.35 - rf * 0.3
        fl = FX._teardrop(bx, by, s2[0], s2[1] - rf * 1.6, rf, seed)
        its = [(fl, FX.FIRE[1], FX._scaled(fl, 0.5, 0, 0), FX.FIRE[2])]
        if kind != 'gob':
            body, inner = _piece_shape(kind, s[0], s[1], rp * 0.9, (u - delay) * spin + seed, seed)
            col, icol = PIECE_COLS[kind]
            its.append((body, col, inner, icol))
        live.append((d, its))
    items = [it for _, its in sorted(live, key=lambda q: -q[0]) for it in its]
    return items, splashes


# ---------------------------------------------------------------------------------------------- the fireball
def fb_lumps(age):
    """The oil fireball at `age` s: [(world centre, radius m, smoke time)]. It bursts out in about 0.2 s, wider than a
    gas flash and taller than wide, then climbs and swells as it rolls up (the top lumps fastest); from 3.0 s each
    lump, top first, burns out into a clump of black smoke (born at its smoke time) while the blaze below goes on."""
    if not (0.0 <= age <= FB_T):
        return []
    rng = np.random.default_rng(FB_SEED)
    n = 22
    d = rng.normal(0, 1, (n, 3))
    d[:, 2] = np.abs(d[:, 2]) * 1.5 + 0.5
    d[:, 1] *= 0.35
    d[:, 0] = d[:, 0] * 0.75 + 0.3                                       # leaning right, clear of Vance
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    D = FB_SIZE * rng.uniform(0.2, 1.2, n)
    r = FB_SIZE * rng.uniform(0.3, 0.52, n)
    e = 1 - math.exp(-age / 0.09)
    hi = d[:, 2] * D / FB_SIZE                                            # how high up the fireball each lump sits
    order = np.argsort(-hi)
    t_smoke = np.empty(n)
    t_smoke[order] = 3.0 + np.linspace(0, 1.4, n)                         # top lumps turn to smoke first
    out = []
    for i in range(n):
        climb = (80 + 40 * hi[i]) * age - 6 * age * age                   # it climbs, the top fastest
        p = HIT + d[i] * D[i] * e * (1 + 0.12 * age) + np.array([0, 0, climb])
        end = 1.0 if age < t_smoke[i] else max(0.0, 1 - (age - t_smoke[i]) / 0.45)
        rr = r[i] * (0.45 + 0.55 * e) * (1 + 0.28 * age) * end
        out.append((p, rr, t_smoke[i]))                                   # burnt-out lumps kept (r 0): fixed order
    return out


def _fireball(cam, u):
    """The fireball as one flat shape: a dark red, smoke-browning edge, a big orange body that stays, and a yellow
    heart for the first second. Daylight colours."""
    lumps = fb_lumps(u)
    if not lumps:
        return None
    blobs = []
    for i, (p, r, _) in enumerate(lumps):
        s, d = cam.screen(p)
        if d < 1.0 or r <= 0:
            continue
        blobs.append(FX._blob(s[0], s[1], cam.focal * r / d, FB_SEED * 31 + i, n=9))
    if not blobs:
        return None
    age = u / FB_T
    ko = 0.8 - 0.15 * age
    ky = max(0.0, 0.82 * (1 - u / 1.2))
    tall = max(y for b in blobs for _, y in b) - min(y for b in blobs for _, y in b)
    edge = S.mix((176, 50, 38), (96, 44, 36), min(1.0, age * 1.3))
    tones = [(edge, blobs), (FX.FIRE[1], [FX._scaled(b, ko, 0, tall * 0.05) for b in blobs])]
    if ky > 0.3:
        mid = np.mean([np.mean(b, 0) for b in blobs], 0)
        core = sorted(blobs, key=lambda b: np.linalg.norm(np.mean(b, 0) - mid))[:7]
        tones.append((FX.FIRE[2], [FX._scaled(b, ky, 0, tall * 0.08) for b in core]))
    return FX.shape_sprite(tones, 0.0, ol=5.0)


# ---------------------------------------------------------------------------------------------- smoke
class Smoke(FX.Puff):
    """A clump of oily smoke: as Flying Whales' Puff, with this film's wind (it leans right)."""
    __slots__ = ()

    def at(self, t):
        u = t - self.t0
        if u < 0 or u > self.life:
            return None
        g = (1 - math.exp(-self.k * u)) / self.k
        p = self.p0 + self.v0 * g + WIND * u * (1 + u * 0.08) + np.array([0, 0, self.rise * u])
        r = self.r0 + (self.r1 - self.r0) * (1 - math.exp(-u / self.tau))
        return p, r


BLAZE_TOP = 260.0                         # the blaze's flames are about this tall (m): the column pours from there


def _smoke():
    """Each fireball lump's own clump as it burns out (top first, carrying on up), then a column pouring from the top
    of the blaze for good (never fades: the clumps rise out of the top of the frame)."""
    rng = np.random.default_rng(5)
    out = []
    n = len(fb_lumps(0.5))
    for i in range(n):
        ts = fb_lumps(0.0)[i][2]
        p, r, _ = fb_lumps(ts)[i]
        climb_v = 80 + 30 - 12 * ts
        out.append(Smoke(ts, p, (0, 0, climb_v * 0.5), 60.0, r * 0.8, r * 1.05, climb_v * 0.45, 'oil', 700 + i,
                         tau=1.2, k=1.2))
    t = 1.2
    while t < 30.0:                                                              # the column, for the rest of the scene
        x = rng.uniform(-40, 40)
        out.append(Smoke(t, HIT + np.array([x + 60, rng.uniform(-5, 5), BLAZE_TOP * 0.7]), (x * 0.6, 0, 60.0), 75.0,
                         rng.uniform(26, 36), rng.uniform(80, 120), 45.0, 'oil', 1000 + int(t * 100), tau=1.3, k=1.6))
        t += rng.uniform(0.06, 0.1)
    return out


SMOKE_PUFFS = _smoke()


# ---------------------------------------------------------------------------------------------- the sea lit orange
GLOW = (236, 140, 70)


def glow_items(cam, u, strength):
    """The fire's light on the sea (list 11): broken flat streaks of orange under the burning ship, brightest nearest
    the fire, wobbling with it; strength 0-1 sets how far they spread. Bright dashes on the blue, never a solid patch
    (a solid one reads as an oil slick)."""
    if strength <= 0:
        return []
    rng = np.random.default_rng(int(u * 6) + 3)
    out = []
    rows = 12
    for i in range(rows):
        y = S.NEAR_Y - 8 - i * 55.0 * strength
        half = 180.0 * strength * (1 - i / (rows + 3))
        x = S.X_HIT + rng.uniform(-15, 15)
        col = S.mix((255, 214, 120), (236, 120, 56), i / rows)
        for j in range(int(rng.integers(2, 4))):                 # each row broken into a few dashes
            c = x + rng.uniform(-half, half) * 0.8
            w = half * rng.uniform(0.2, 0.42)
            P, d = cam.screen(np.array([(c - w, y, 0), (c + w, y, 0)]))
            if (d < 1).any():
                continue
            (x0, y0), (x1, y1) = P
            th = 1.6 + 1.6 * (1 - i / rows)
            out.append(([(x0, y0), (x0 + th * 2, y0 - th), (x1 - th * 2, y1 - th), (x1, y1), (x1 - th * 2, y1 + th),
                         (x0 + th * 2, y0 + th)], col))
    return out


# ---------------------------------------------------------------------------------------------- the blast's force
def ring_items(cam, u):
    """The blast racing out over the water (force, Sam 8 Nov): a broken ring of white spray spreading 450 m from the
    ship in about a second, thinning as it goes; hidden where the hull stands in front of its far side."""
    if not (0 <= u < 1.1):
        return []
    R = 450.0 * (1 - math.exp(-u / 0.32))
    w = 10.0 + 14.0 * (1 - u / 1.1)
    col = S.mix((250, 252, 252), S.SEA_DAY[3], u / 1.1)
    out = []
    for k in range(36):
        if k % 4 == 3:
            continue                                             # broken, not a ruled ring
        a0, a1 = k * 10.0, k * 10.0 + 8.0
        arc = np.radians(np.linspace(a0, a1, 4))
        if np.sin(arc).mean() > 0 and abs(R * np.cos(arc).mean()) < L / 2 + 20:
            continue                                             # behind the hull
        outer = [(S.X_HIT + (R + w) * math.cos(t), S.NEAR_Y + (R + w) * math.sin(t), 0) for t in arc]
        inner = [(S.X_HIT + R * math.cos(t), S.NEAR_Y + R * math.sin(t), 0) for t in arc[::-1]]
        P, d = cam.screen(np.array(outer + inner))
        if (d < 1).any():
            continue
        out.append(([tuple(p) for p in P], col))
    return out


# ---------------------------------------------------------------------------------------------- the blaze
def blaze_lumps(u):
    """The oil fire's rolling column (Sam, 8 Nov: an oil fire, not embers): clumps of flame born at the break every
    0.08 s, rolling up and swelling as they climb, leaning a little with the wind, and burning out about 190 m up,
    where the smoke column takes over. [(world centre, radius m, age s)]."""
    out = []
    i = 0
    while True:
        tb = 0.3 + i * 0.08
        if tb > u:
            break
        a = u - tb
        if a < 2.4:
            rng = np.random.default_rng(4000 + i)
            grow = min(1.0, 0.35 + (tb - 0.3) / 1.4)
            p = HIT + np.array([rng.uniform(-40, 40) + 14 * a, rng.uniform(-4, 4), 70 * a + 8 * a * a + 14])
            r = (24 + 32 * (1 - math.exp(-a / 0.6))) * grow * rng.uniform(0.85, 1.15)
            if a > 1.8:
                r *= max(0.0, 1 - (a - 1.8) / 0.6)
            out.append((p, r, a))
        i += 1
    return out


def blaze_sprites(cam, u):
    """The blaze that follows the fireball and burns for good: the rolling column of flame out of the break (one flat
    shape: dark red edge, orange, a yellow heart low down), burning oil spreading over the water round it, and a
    small fire on the funnel stub."""
    if u < 0.3:
        return []
    grow = min(1.0, (u - 0.3) / 1.6)
    gap = brk(u)[1]
    blobs, hearts = [], []
    for i, (p, r, a) in enumerate(blaze_lumps(u)):
        sc, d = cam.screen(p)
        if d < 1.0 or r <= 0:
            continue
        b = FX._blob(sc[0], sc[1], cam.focal * r / d, 5000 + i, n=8)
        blobs.append(b)
        if a < 0.8:
            hearts.append(FX._scaled(b, 0.5, 0, 0))
    out = []
    if blobs:
        out.append(FX.shape_sprite([((176, 50, 38), blobs), (FX.FIRE[1], [FX._scaled(b, 0.72, 0, 0) for b in blobs]),
                                    (FX.FIRE[2], hearts)], 0.0, ol=5.0))
    spread = 30 + gap / 2 + 30 * min(1.0, max(0.0, u - 0.6) / 6.0)      # burning oil in the gap, spreading a little
    out.append(FX.fire_sprite(cam, np.array([S.X_HIT + 6, S.NEAR_Y - 22, 0.0]), (1, 0, 0), spread, 26 * grow, u,
                              22, 0.0, n=5))
    out.append(FX.fire_sprite(cam, on_wreck(FUNNEL_U, FUNNEL_Z - 3, u) + np.array([0, -1.0, 0]), (1, 0, 0), 5.0,
                              12.0 * grow, u, 8, 0.0, n=2))
    return out


# ---------------------------------------------------------------------------------------------- fx(u)
def fx(u):
    """Every effect at u, drawn between the ships and the cliff top, through any camera: the sea's glow, the blast
    ring, the smoke, the fireball, the blaze, the flying pieces, the splashes, the missile."""
    def draw(img, cam):
        if u < -MISSILE_T:
            return
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        if u >= 0:
            fire_k = min(1.0, 0.6 + u) if u < FB_T else 0.8 + 0.08 * math.sin(u * 9)
            for poly, col in glow_items(cam, u, fire_k):
                d.polygon(poly, fill=col + (255,))
            for poly, col in ring_items(cam, u):
                d.polygon(poly, fill=col + (255,), outline=S.mix(S.INK, col, 0.5) + (255,))
        sprites = [FX.puffs_sprite(cam, SMOKE_PUFFS, u, 0.0, ol=4.0)]
        if u >= 0:
            heave = []                                           # the sea heaved up white round the ship by the blast
            for k, (dx, dy, sz) in enumerate(((0, -14, 60), (-70, -10, 34), (80, -12, 40))):
                heave += FX.splash_parts(HIT + np.array([dx, dy, 0]), sz, u - 0.02 * k, 61 + k, high=1.4)
            sprites.append(_fireball(cam, u))
            sprites += blaze_sprites(cam, u)
            if heave:
                sprites.append(FX.lumps_sprite(cam, heave, 0.0, ol=3.0, cols=DAY_WATER))
            items, splashes = pieces_items(cam, u)
            sprites.append(FX.pieces_sprite(items, 0.0, ol=3.0))
            lumps = []
            for at, size, age, seed in splashes:
                lumps += FX.splash_parts(at, size * 1.3, age, seed, high=2.2)
            if lumps:
                sprites.append(FX.lumps_sprite(cam, lumps, 0.0, ol=3.0, cols=DAY_WATER))
        mp = missile_poly(u, cam)
        if mp:
            d.polygon(mp, fill=(22, 22, 26, 255), outline=S.INK + (255,))
        img.alpha_composite(lay)
        for spr in sprites:
            if spr is not None:
                spr.paste(img)
    return draw


# ---------------------------------------------------------------------------------------------- flame-light, jolt
_GRID = {}


def light(img, u, cam=None):
    """The fire's light over the finished frame (people included), in place of a white flash (Sam, 8 Nov: a white
    flash reads as nuclear): a hot orange glow from the fireball, strongest round it and reaching across the whole
    frame on the hit, settling to a warm glow round the blaze for as long as it burns."""
    if u < 0:
        return img
    cam = cam or S.CLIFF
    peak = 0.55 * (u / 0.08 if u < 0.08 else math.exp(-(u - 0.08) / 0.5))
    k = max(peak, 0.16 + 0.12 * math.exp(-u / 1.5) + 0.02 * math.sin(u * 11))
    (hx, hy), _ = cam.screen(HIT + np.array([0, 0, 120.0]))
    W, H = img.size
    if (W, H) not in _GRID:
        _GRID[(W, H)] = np.mgrid[0:H, 0:W].astype(np.float32)
    yy, xx = _GRID[(W, H)]
    sc = W / 1080
    dist = np.hypot(xx - hx * sc, (yy - hy * sc) * 0.8) / (900 * sc)
    a = k * (np.clip(1 - dist, 0, 1) ** 1.5 + 0.3 * min(1.0, peak / 0.3))
    a = np.clip(a, 0, 0.75)[..., None]
    arr = np.asarray(img.convert('RGBA')).astype(np.float32) / 255
    col = np.array([1.0, 0.55, 0.18], np.float32)
    rgb = 1 - (1 - arr[..., :3]) * (1 - a * col)                  # screen blend: brighter and warmer, never white
    out = np.concatenate([rgb, arr[..., 3:]], -1)
    return Image.fromarray((out * 255 + 0.5).astype(np.uint8), 'RGBA')


def hellfire(layer, u, strength=1.0):
    """The burning wreck's light on someone in front of it (Sam, 8 Nov, note 31: "slightly lit by hellfire" in the
    close-up): their own drawing (an RGBA layer, transparent round them) warmed orange, strongest on the side towards
    the fire (screen right) and flickering with it. Returns the layer."""
    if u < 0.3:
        return layer
    arr = np.asarray(layer).astype(np.float32) / 255
    al = arr[..., 3]
    ys, xs = np.nonzero(al > 0.01)
    if not len(xs):
        return layer
    x0, x1 = xs.min(), xs.max()
    W = arr.shape[1]
    ramp = np.clip((np.arange(W, dtype=np.float32) - x0) / max(1, x1 - x0), 0, 1)[None, :]
    fl = 1.0 + 0.12 * math.sin(u * 13) + 0.08 * math.sin(u * 29 + 1)
    k = min(1.0, (u - 0.3) / 1.0) * strength * fl
    rgb = arr[..., :3]
    lum = rgb @ np.array([0.3, 0.55, 0.15], np.float32)
    ink = np.clip((lum - 0.06) / 0.08, 0.15, 1.0)                    # the outlines stay dark
    a = (0.07 + 0.4 * ramp ** 2.5) * k * ink                          # a warm wash, a rim of fire on the right
    col = np.array([1.0, 0.5, 0.16], np.float32)
    rgb = 1 - (1 - rgb) * (1 - a[..., None] * col)                # screen blend: warmer and brighter
    return Image.fromarray((np.dstack([rgb, al]) * 255 + 0.5).clip(0, 255).astype(np.uint8), 'RGBA')


def jolt(u):
    """The camera jolt on the hit (list 12): a hard kick, dying away in about 0.8 s."""
    a = u - FREEZE_AT
    if a < 0 or a > 0.8:
        return 0.0, 0.0
    k = 26.0 * math.exp(-a * 5.0)
    f = int(round(a * FPS))
    return k * (1 if f % 2 else -1), k * 0.6 * (1 if f % 3 else -1)


def shift(img, dx, dy):
    """The finished frame moved by (dx, dy) px, the uncovered edge filled from the nearest row or column."""
    dx, dy = int(round(dx)), int(round(dy))
    if not dx and not dy:
        return img
    a = np.roll(np.asarray(img), (dy, dx), axis=(0, 1)).copy()
    if dy > 0:
        a[:dy] = a[dy]
    elif dy < 0:
        a[dy:] = a[dy - 1]
    if dx > 0:
        a[:, :dx] = a[:, dx:dx + 1]
    elif dx < 0:
        a[:, dx:] = a[:, dx - 1:dx]
    return Image.fromarray(a, img.mode)


# ---------------------------------------------------------------------------------------------- frames
def wide_frame(u, t0=6.0):
    """The cliff shot at u s from the hit: Vance at his mark, calm, never looking round (the film adds his acting)."""
    v = held(u)
    CP = S._cast()
    import ad_vanced_notice_cast as AC
    im = S.strait('wide', t0 + v, near(v), fx(v))
    x, y, ppm = S.place_cliff(*S.VANCE_MARK)
    S.cliff_shadow(im, x, y, ppm)
    CP.person(im, AC.VANCE, x, y, ppm, 0, mood='sincere', mouth='rest')
    im = light(im, v)
    return shift(im, *jolt(u))


def close_frame(u, t0=6.0):
    """The close-up's wreck, smoke and glow (list 10, brief 18): the same world through the close camera."""
    CP = S._cast()
    import ad_vanced_notice_cast as AC
    im = S.strait('close', t0 + u, near(u), fx(u))
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
    CP.person(lay, AC.VANCE, 430, 1920 + 1500, 1500, 0, mood='sincere', mouth='rest')
    im.alpha_composite(hellfire(lay, u))
    return light(im, u, S.CLOSE)


EFFECTS = [  # rule 15: each effect alone, shape-tested (viewchecks.shape_faults)
    ('fireball', 'burst', lambda img: _fireball(S.CLIFF, 0.25).paste(img)),
    ('fireball climbing', 'burst', lambda img: _fireball(S.CLIFF, 2.4).paste(img)),
    ('blaze', 'burst', lambda img: [sp.paste(img) for sp in blaze_sprites(S.CLIFF, 4.0) if sp is not None]),
    ('smoke column', 'smoke', lambda img: FX.puffs_sprite(S.CLIFF, SMOKE_PUFFS, 3.0, 0.0).paste(img)),
    ('flying pieces', 'chunks', lambda img: FX.pieces_sprite(pieces_items(S.CLIFF, 0.8)[0], 0.0, ol=3.0).paste(img)),
]


def sheet(out):
    import sheet as SH
    shots = [(-0.2, 'missile'), (0.25, 'hit, flame-light'), (0.7, 'fireball'), (1.2, 'pieces fly'),
             (2.4, 'fireball climbs'), (4.0, 'oil fire'), (6.0, 'burning for good')]
    frames = [(wide_frame(u), f'{lbl} ({u:+.1f} s)') for u, lbl in shots]
    frames.append((close_frame(7.0), 'close-up (+7 s)'))
    _plain_sheet(frames, out)


def _plain_sheet(frames, out, cols=4, w=270):
    h = int(w * 1920 / 1080)
    rows = (len(frames) + cols - 1) // cols
    sh = Image.new('RGB', (cols * w, rows * (h + 26)), (250, 250, 250))
    d = ImageDraw.Draw(sh)
    for i, (im, lbl) in enumerate(frames):
        x, y = (i % cols) * w, (i // cols) * (h + 26)
        sh.paste(im.convert('RGB').resize((w, h), Image.LANCZOS), (x, y + 26))
        d.text((x + 6, y + 6), lbl, fill=(20, 20, 20))
    sh.save(out, quality=88)
    print(out)


def clip(out, small=False, u0=-1.4, u1=6.6):
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    n = int(round((u1 - u0) * FPS))
    size = (540, 960) if small else (1080, 1920)
    p = subprocess.Popen([ff, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s',
                          f'{size[0]}x{size[1]}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                          '-crf', '23' if small else '20', '-preset', 'slow', '-movflags', '+faststart', out],
                         stdin=subprocess.PIPE)
    for i in range(n):
        im = wide_frame(u0 + i * F).convert('RGB')
        if small:
            im = im.resize(size, Image.LANCZOS)
        p.stdin.write(im.tobytes())
    p.stdin.close()
    p.wait()
    print(f'{out}: {os.path.getsize(out) / 1e6:.1f} MB, {n / FPS:.1f} s')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        sheet(a[1])
    elif a and a[0] == 'clip':
        clip(a[1], '--small' in a)
    else:
        print(__doc__)
