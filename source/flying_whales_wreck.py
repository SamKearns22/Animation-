#!/usr/bin/env python3
"""Flying Whales: the wreck (1 Nov, effects stage). What each whale breaks, when, and how every piece then moves:
knocked loose, thrown the way the whale was going, falling under gravity, hitting the sea (a splash) and sinking (the
sea cuts it off as it goes under: flying_whales_rig clips everything below z = 0); and the finale, where the whole
rig tips and slides into the sea. Also every effect's timing: holes torn in the decks, fireballs, deck fires and their
smoke, dust, steam, flying bits, splashes, the flare's smoke ribbon, the glow on the sea, the freeze and camera shake
on each hit (rule 25).

Times are the rig scene's story clock (0 = the hard cut). The film's real clock runs 2 frames longer at each of the
seven main hits (the freeze): `story(real)` turns one into the other.

The hits (CONTACTS: from flying_whales_paths.contacts(); `check` confirms they still match the paths):
- knocked loose and thrown (THROWN): the braces, lifeboats, the stair tower, the helideck and its truss, the crane
  (its boom whipping down as it goes), the flare boom (its flame riding it down, out in a burst of steam), the stacks,
  the front left leg;
- holed (the decks): a ragged hole torn where the whale went in, on the faces we can see, dust and flying bits; three
  burn on (FIRES) with black smoke drifting right;
- fireballs (FIREBALLS): Blaze's two hits, Bib's helideck, and a gas burst where Ghost snaps the flare boom;
- bent (the derrick, Blaze's knock-on): it whips over and stays leaning;
- the finale (from TF, Bib taking out the front left leg): everything still standing tips as one block towards the
  missing leg, then slides under, the far end rising, the derrick last; a crown splash where the deck first hits the
  sea, froth all along the waterline as it goes in, steam where the fires go under.

    python3 source/flying_whales_wreck.py check        contacts still match; nothing left above the sea at the end
    python3 source/flying_whales_wreck.py table        every event with its time
"""
import functools
import math
import os
import sys
import zlib

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import whale as W                                     # noqa: E402
import flying_whales_sea as SEA                       # noqa: E402
import flying_whales_rig as R                         # noqa: E402
import flying_whales_paths as PATHS                   # noqa: E402
import flying_whales_fx as FX                         # noqa: E402

G = 9.8
CAM = SEA.CAM
FPS = 24

# (story time of first touch, whale, piece): paths.contacts(), 1 Nov
CONTACTS = [(2.56, 0, 'brace_front_low'), (2.98, 0, 'brace_back'), (3.03, 1, 'lifeboat_1'),
            (3.12, 1, 'deck_cellar_r'), (3.20, 1, 'lifeboat_2'), (3.71, 3, 'stair_tower'), (3.80, 3, 'deck_mezz_l'),
            (3.80, 3, 'helideck_truss'), (3.97, 1, 'deck_mezz_r'), (4.11, 3, 'helideck'), (4.25, 2, 'deck_top_l'),
            (4.41, 2, 'crane_house'), (5.02, 4, 'flare_boom'), (5.14, 2, 'stack_1'), (5.20, 2, 'stack_2'),
            (6.47, 1, 'deck_top_r'), (6.74, 1, 'derrick'), (7.59, 3, 'brace_front_high'), (7.59, 3, 'brace_left'),
            (7.59, 3, 'leg_fl')]
MAIN = [2.56, 3.03, 3.71, 4.25, 5.02, 6.47, 7.59]     # the main hits: a freeze and a jolt on each (rule 25)
HOLD = 2 / FPS                                        # the freeze: two frames
TF = 7.62                                             # the finale starts (the leg is gone)

# piece: (share of the whale's velocity it takes, m/s up, spin deg/s, m/s kicked out along the rig's long side)
THROWN = {
    'brace_front_low': (0.35, 3.0, 160, 0.0), 'brace_back': (0.3, 2.0, -120, 0.0),
    'lifeboat_1': (0.16, 5.0, 320, 5.0), 'lifeboat_2': (0.16, 6.0, -360, -4.0),
    'stair_tower': (0.2, 2.5, 75, 3.0), 'helideck_truss': (0.3, 3.0, 150, 0.0), 'helideck': (0.36, 7.0, 240, 0.0),
    'crane_house': (0.28, 5.0, 95, 0.0), 'flare_boom': (0.1, 1.5, 10, 0.0), 'stack_1': (0.32, 4.0, 210, 0.0),
    'stack_2': (0.32, 5.0, -230, 0.0), 'leg_fl': (0.2, 0.0, 55, 7.0), 'brace_front_high': (0.3, 2.0, 140, 2.0),
    'brace_left': (0.25, 1.0, -100, 5.0), 'crane_boom': (0.15, 2.0, -120, 0.0)}
BENT = {'derrick'}
FIREBALLS = {'deck_cellar_r': 12.0, 'helideck': 10.0, 'deck_top_r': 12.0, 'flare_boom': 6.0}   # size, m
FIRES = {'deck_cellar_r', 'deck_top_l', 'deck_top_r'}
DEBRIS_COLS = {'deck_cellar': ('grey', 'dark', 'yellow', 'clad'), 'deck_mezz': ('clad', 'yellow', 'grey', 'white'),
               'deck_top': ('clad', 'white', 'grey', 'blue'), 'brace': ('yellow',), 'lifeboat': ('orange', 'white'),
               'leg': ('yellow',), 'helideck': ('deck', 'white', 'orange'), 'stair': ('yellow', 'grey'),
               'crane': ('yellow', 'white'), 'flare': ('grey', 'dark'), 'stack': ('grey', 'dark')}
CROWN = (19.0, 13.0, 52, 4.0)                        # the crown splash: size m, ring m, lumps, height (was 13, 9, 34, 2.8)
CROWN_BITS = 46                                      # debris thrown up with it (note 12)
FRONT, BACK = 60.0, 250.0                            # m: the finale's splashes and bits drawn over the whole rig,
                                                     # its smoke behind it all (notes 9, 11)
HELI_SIDE, HELI_UP = 16.0, 12.0                   # m/s: the helideck batted aside (note 8)
SINK = 6.0                                            # m/s: a piece going down through the water


def story(real):
    """The story time shown at real rig-scene time `real`: it stands still for HOLD at each main hit."""
    acc = 0.0
    for th in MAIN:
        start = th + acc
        if real < start:
            break
        if real < start + HOLD:
            return th
        acc += HOLD
    return real - acc


def real_of(ts):
    """The real time a story time first shows."""
    return ts + HOLD * sum(1 for th in MAIN if th < ts)


# ------------------------------------------------- moving the pieces ------------------------------------------------
def _compose(M1, M2):
    """M1 after M2 (affine (A, b): p -> A p + b)."""
    return M1[0] @ M2[0], M1[0] @ M2[1] + M1[1]


def _apply(M, p):
    return np.asarray(p, float) @ M[0].T + M[1]


I3 = (np.eye(3), np.zeros(3))


def _about(Rm, c):
    """A rotation Rm about the point c, as an affine."""
    c = np.asarray(c, float)
    return Rm, c - Rm @ c


def _rot(axis, deg):
    return R.rot(np.asarray(axis, float), deg)


@functools.lru_cache(None)
def _samples(name):
    """Points spread over a piece at rest (world), for its waterline and its lowest and highest point."""
    pts = []
    for it in R.PARTS[name].items:
        if it['kind'] in ('poly', 'spot'):
            pts += list(it['pts'])
        elif it['kind'] in ('tube', 'line'):
            for f in (0.0, 0.25, 0.5, 0.75, 1.0):
                pts.append(it['p0'] + (it['p1'] - it['p0']) * f)
    P = np.array(pts, float)
    if len(P) > 240:
        P = P[np.linspace(0, len(P) - 1, 240).astype(int)]
    return P


# the finale: the block (everything still standing) tips about the line through the feet of the front right and back
# left legs, towards the missing front left leg, then slides down and under, sliding a little towards the front left
H0, H1 = R._leg_pt('leg_fr', 0.0), R._leg_pt('leg_bl', 0.0)
AXIS = (H1 - H0) / np.linalg.norm(H1 - H0)
if np.dot(np.cross(AXIS, R.P(50, 0, 25) - H0), [0, 0, 1]) > 0:   # turn it the way that drops the front left corner
    AXIS = -AXIS
SLIDE = (R.EU - R.EV) / np.linalg.norm(R.EU - R.EV)


def finale_angle(u):
    return 10.0 * (u / 0.8) ** 2 if u < 0.8 else 10.0 + 25.0 * (u - 0.8) - 1.5 * (u - 0.8) ** 2


def finale_drop(u):
    return 0.0 if u < 0.3 else 0.5 * 16.0 * (u - 0.3) ** 2


def block(t):
    u = t - TF
    if u <= 0:
        return I3
    M = _about(_rot(AXIS, finale_angle(u)), H0)
    d = finale_drop(u)
    return M[0], M[1] + np.array([0, 0, -d]) + SLIDE * 0.25 * d


def _whale_dir(k, t):
    v = PATHS.vel(k, t)
    return v, v / (np.linalg.norm(v) + 1e-9)


BREAK = {}
for _t, _k, _n in CONTACTS:
    BREAK.setdefault(_n, (_t, _k))
BREAK['crane_boom'] = (4.56, 2)                       # it whips over and snaps off its crane a moment after the hit


def _local(name, t):
    """A piece's own bend on its parent: the derrick whipping over and staying bent; the crane boom whipping down
    once the crane is knocked loose."""
    if name == 'derrick' and t > BREAK['derrick'][0]:
        t0, k = BREAK['derrick']
        u = t - t0
        _, f = _whale_dir(k, t0)
        ax = np.cross([0, 0, 1.0], f)
        ax /= np.linalg.norm(ax)
        ang = 16.0 * (1 - math.exp(-5 * u) * math.cos(12 * u))
        return _about(_rot(ax, ang), R.P(12.0, 22.0, R.LEVELS[3]))
    if name == 'crane_boom' and t > BREAK['crane_house'][0]:
        u = t - BREAK['crane_house'][0]
        bd = np.array([math.cos(math.radians(58)), -0.12, math.sin(math.radians(58))])
        bdw = bd[0] * R.EU + bd[1] * R.EV + bd[2] * R.EZ
        ax = np.cross([0, 0, 1.0], bdw)
        ax /= np.linalg.norm(ax)
        root = R.P(29.0 + 1.5, 7.0, R.LEVELS[3] + 10.0)
        return _about(_rot(ax, 40.0 * (1 - math.exp(-6 * u))), root)
    return I3


PARENT = dict(R.PARENT)
for _n in ('deck_cellar_r', 'deck_cellar_l'):
    PARENT[_n] = 'BLOCK'                              # the decks stand on the jacket as one block


class Fall:
    """A piece knocked loose at t0: flying (gravity), into the sea (a splash), sinking (slowed by the water, its
    tumble dying) until it is all under. Tracked at 120 Hz."""
    def __init__(self, name, t0, M0, v0, axis, rate):
        self.name, self.t0 = name, t0
        self.M0 = M0
        P0 = _apply(M0, _samples(name))
        c0 = _apply(M0, R.PARTS[name].pivot)
        self.c0 = c0
        self.axis = np.asarray(axis, float) / (np.linalg.norm(axis) + 1e-9)
        dt = 1 / 120
        c, v, ang = c0.copy(), np.asarray(v0, float).copy(), 0.0
        self.track = []
        self.entry, self.froth, self.gone = None, [], None
        size = float(np.linalg.norm(P0.max(0) - P0.min(0)))
        self.size = size
        wet = False
        last_froth = -1.0
        for i in range(int(9.0 / dt)):
            t = t0 + i * dt
            Rb = _rot(self.axis, ang)
            P = (P0 - c0) @ Rb.T + c
            zmin, zmax = P[:, 2].min(), P[:, 2].max()
            self.track.append((c.copy(), ang))
            if not wet and zmin <= 0.0:
                wet = True
                low = P[np.argmin(P[:, 2])]
                # a leg or brace standing in the sea when it is hit makes no splash going in
                self.entry = (t, None if i == 0 else low * np.array([1, 1, 0]), float(np.linalg.norm(v)))
            if wet and zmax > 0.3 and t - last_froth >= 0.25 and t > self.entry[0] + 0.1:
                near = P[np.abs(P[:, 2]) < 1.5]
                if len(near):
                    self.froth.append((t, near.mean(0) * np.array([1, 1, 0]), float(np.ptp(near[:, 0]) +
                                                                                  np.ptp(near[:, 1]))))
                    last_froth = t
            if zmax < -0.5 and self.gone is None:
                self.gone = t                         # (kept sinking: what hangs on it may still show)
            if zmax < -60:
                break
            if not wet:
                v[2] -= G * dt
            else:
                # the bigger it is the faster it goes down; it keeps toppling over as it goes, so a long piece
                # lies down in the sea and never stands on its end (rule 32)
                target = np.array([v[0] * 0.15, v[1] * 0.15, -(SINK + 0.15 * size)])
                v += (target - v) * min(1.0, dt / 0.22)
                rate *= math.exp(-1.2 * dt)
            c = c + v * dt
            ang += rate * dt

    def affine(self, t):
        i = min(len(self.track) - 1, max(0, int((t - self.t0) * 120)))
        c, ang = self.track[i]
        Rb = _rot(self.axis, ang)
        return _compose((Rb, c - Rb @ self.c0), self.M0)


FALLS = {}


def _world_raw(name, t):
    if name == 'BLOCK':
        return block(t)
    f = FALLS.get(name)
    if f is not None and t >= f.t0:
        return f.affine(t)
    return _compose(_world_raw(PARENT.get(name, 'BLOCK'), t), _local(name, t))


def _build_falls():
    for name in sorted(THROWN, key=lambda n: BREAK[n][0]):
        t0, k = BREAK[name]
        push, up, spin, kick = THROWN[name]
        v, f = _whale_dir(k, t0)
        M0 = _world_raw(name, t0)
        v0 = v * push
        v0[2] = min(v0[2], 3.0) + up                  # a climbing whale doesn't fling it skywards
        v0 = v0 + R.EU * kick
        if name == 'helideck':                        # Sam, 2 Nov (note 8): the whale passed THROUGH it while it was
                                                      # only nudged; now batted off the whale's path, out to our left
                                                      # and up, so the whale sails past under it
            h = np.array([f[0], f[1], 0.0]) / (np.linalg.norm(f[:2]) + 1e-9)
            side = np.array([-h[1], h[0], 0.0])       # 90 degrees left of the whale's way: towards us
            v0 = v * 0.5 + side * HELI_SIDE + np.array([0, 0, HELI_UP])
        if name == 'flare_boom':                      # it snaps at the root and drops, levelling as it falls, so
                                                      # it lands flat (spin chosen by trial: rule 32)
            fd = R.FLARE_DIR[0] * R.EU + R.FLARE_DIR[1] * R.EV + R.FLARE_DIR[2] * R.EZ
            axis = np.cross([0, 0, 1.0], fd)
        elif name == 'helideck':                      # spinning like a thrown plate, tipping over
            axis = np.array([0, 0, 1.0]) + 0.5 * np.cross([0, 0, 1.0], f)
        else:                                         # tumbling over forwards, the way it was hit
            axis = np.cross([0, 0, 1.0], f) + np.array([0, 0, 0.25 * np.sign(spin)])
        FALLS[name] = Fall(name, t0, M0, v0, axis, abs(spin) * np.sign(spin))


_build_falls()


@functools.lru_cache(4096)
def _world_q(name, tq):
    return _world_raw(name, tq / 480.0)


def world(name, t):
    """A piece's placement at story time t: affine (A, b), world point p -> A p + b."""
    return _world_q(name, int(round(t * 480)))


def xf_of(name, t):
    """The rig's xf (Rm about the pivot, T) for a piece, or None if it is still where it was built."""
    A, b = world(name, t)
    if np.allclose(A, np.eye(3), atol=1e-9) and np.allclose(b, 0, atol=1e-6):
        return None
    piv = R.PARTS[name].pivot
    return A, A @ piv + b - piv


def zrange(name, t):
    P = _apply(world(name, t), _samples(name))
    return P[:, 2].min(), P[:, 2].max()


# ------------------------------------------------- holes ------------------------------------------------------------
def _to_rig(p):
    q = np.asarray(p, float) - R.ORIGIN
    return np.stack([q @ R.EU, q @ R.EV, q[..., 2]], -1)


def _from_rig(q):
    return R.P(*q)


FACES = [('front', 1, 0, -R.EV, R.EU, R.EZ), ('right', 0, 0, -R.EU, R.EV, R.EZ), ('bottom', 2, 0, -R.EZ, R.EU, R.EV),
         ('back', 1, 1, R.EV, R.EU, R.EZ), ('left', 0, 1, R.EU, R.EV, R.EZ), ('top', 2, 1, R.EZ, R.EU, R.EV)]


def _holes(name, t0, k):
    """Where whale k tore into deck `name`: [(centre world, u, v, n, radius m)] on the faces the camera sees."""
    q = np.concatenate([_to_rig(it['pts']) for it in R.PARTS[name].items if it['kind'] == 'poly'])
    lo, hi = q.min(0), q.max(0)
    sz = W.PATTERNS[k]['size']
    ts = np.arange(t0 - 0.3, t0 + 0.8, 1 / 192)
    C = _to_rig(np.array([PATHS.pos(k, t) for t in ts]))
    out = []
    for fname, ax, side, n, u, v in FACES:
        plane = hi[ax] if side else lo[ax]
        others = [i for i in range(3) if i != ax]
        P = C.copy()
        P[:, ax] = plane
        for i in others:                                  # the nearest point of the face to each point on the path
            P[:, i] = np.clip(P[:, i], lo[i] + 1.2, hi[i] - 1.2)
        d = np.linalg.norm(P - C, axis=1)
        j = int(np.argmin(d))
        reach = 2.3 * sz
        if d[j] > reach:
            continue
        cw = _from_rig(P[j])
        if np.dot(n, cw - CAM.pos) >= 0:                  # a face we can't see
            continue
        r = max(1.6, 3.6 * sz * math.sqrt(max(0.0, 1 - d[j] / reach)))
        r = min(r, 0.45 * min(hi[i] - lo[i] for i in others))
        out.append((cw, u, v, n, r))
    return out


HOLES = {n: _holes(n, t, k) for t, k, n in CONTACTS if n.startswith('deck_')}


@functools.lru_cache(None)
def _holed_part(name):
    p = R.PARTS[name]
    items = list(p.items)
    for i, (c, u, v, n, r) in enumerate(HOLES[name]):
        items += FX.hole_items(c, u, v, n, r, seed=_seed(name, i))
    return R.Part(name, p.label, items, p.pivot)


def swaps(t):
    return {n: ('holed', _holed_part(n)) for n, hs in HOLES.items() if hs and t >= BREAK[n][0]}


# ------------------------------------------------- the events -------------------------------------------------------
def _seed(*a):
    return zlib.crc32(repr(a).encode()) % (1 << 30)    # the same every run (Python's hash() is not)


def _contact_point(name, t0, k):
    """Where the whale meets the piece: the point of the piece nearest the whale's nose (world, at rest place)."""
    ps = PATHS.pose(k, t0)
    nose = ps.pos + ps.R[:, 0] * 4.5 * W.PATTERNS[k]['size']
    P = _apply(world(name, t0 - 1e-3), _samples(name))
    return P[np.argmin(np.linalg.norm(P - nose, axis=1))]


def _kind(name):
    for key in DEBRIS_COLS:
        if name.startswith(key):
            return key
    return {'stair_tower': 'stair', 'crane_house': 'crane', 'flare_boom': 'flare', 'helideck_truss': 'helideck'}.get(
        name, 'deck_top')


class Bit:
    """A small flying bit of the rig: thrown, falling, gone into a splash where it hits the sea."""
    __slots__ = ('t0', 'p0', 'v0', 'size', 'col', 'seed', 'spin', 't_wet')

    def __init__(self, t0, p0, v0, size, col, seed, spin):
        self.t0, self.p0, self.v0, self.size, self.col, self.seed, self.spin = t0, p0, v0, size, col, seed, spin
        a, b, c = -0.5 * G, v0[2], p0[2]
        self.t_wet = t0 + (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a) if c > 0 else t0

    def at(self, t):
        u = t - self.t0
        return self.p0 + self.v0 * u + np.array([0, 0, -0.5 * G * u * u])


def _events():
    bits, splashes, puffs, fireballs, fires, jolts = [], [], [], [], [], []
    for t0, k, name in CONTACTS:
        v, f = _whale_dir(k, t0)
        rng = np.random.default_rng(_seed(name, k))
        kind = _kind(name)
        holes = HOLES.get(name, [])
        at = holes[0][0] if holes else _contact_point(name, t0, k)
        n_bits = {'deck_cellar': 22, 'deck_mezz': 14, 'deck_top': 20, 'brace': 8, 'lifeboat': 5, 'leg': 9}.get(kind, 10)
        big = kind.startswith('deck')
        for i in range(n_bits):
            vb = v * rng.uniform(0.2, 0.55) + rng.normal(0, 7.0, 3) + np.array([0, 0, rng.uniform(2, 9)])
            if holes:
                vb += holes[0][3] * rng.uniform(2, 8)      # some of it blown back out of the hole, towards us
            size = rng.uniform(0.4, 2.0 if big else 1.2)
            col = R._tint(R.COL[DEBRIS_COLS[kind][i % len(DEBRIS_COLS[kind])]][int(rng.integers(0, 2))])
            bits.append(Bit(t0 + rng.uniform(0, 0.08), at + rng.normal(0, 1.0, 3), vb, size, col,
                            int(rng.integers(1 << 30)), rng.uniform(-12, 12)))
        if big:                                       # dust billowing out of the hole
            n = holes[0][3] if holes else -f
            for i in range(9):
                vd = n * rng.uniform(3, 9) + rng.normal(0, 4.0, 3) + v * 0.08
                puffs.append(('dust', name, FX.Puff(t0 + rng.uniform(0, 0.15), at + rng.normal(0, 1.2, 3), vd,
                                                    0.6, rng.uniform(1.0, 2.0), rng.uniform(3.5, 6.0),
                                                    rng.uniform(1.4, 2.2), 'dust', int(rng.integers(1 << 30)),
                                                    tau=0.6, k=2.2)))
        if name in FIREBALLS:
            size = FIREBALLS[name]
            c = (holes[0][0] + holes[0][3] * 2.5) if holes else (
                R.P(*R.FLARE_ROOT) if name == 'flare_boom' else at)
            fireballs.append((t0, c, size, _seed(name, 'fb')))
            for i in range(14):                       # its black smoke, rising from the top as it burns out
                ts_ = t0 + 0.15 + i * 0.055
                age = ts_ - t0
                p = c + np.array([rng.uniform(-0.4, 0.4) * size, rng.uniform(-0.3, 0.3) * size,
                                  size * 0.7 + 5.0 * age])
                puffs.append(('smoke', name + '_fb', FX.Puff(ts_, p, rng.normal(0, 2.0, 3), 8.5,
                                                             size * rng.uniform(0.3, 0.45),
                                                             size * rng.uniform(0.6, 0.85), 5.5, 'smoke',
                                                             int(rng.integers(1 << 30)), tau=1.2)))
        if name in FIRES and holes:
            c, u, vv, n, r = holes[0]
            fires.append((name, t0 + 0.2, c, u, vv, n, r))
        if name in BENT:
            for i in range(6):
                bits.append(Bit(t0, at + rng.normal(0, 1.0, 3), v * rng.uniform(0.2, 0.4) + rng.normal(0, 5, 3),
                                rng.uniform(0.4, 1.0), R._tint(R.COL['red'][i % 2]), int(rng.integers(1 << 30)),
                                rng.uniform(-12, 12)))
    for t0 in MAIN:
        jolts.append((real_of(t0), 11.0))
    # the bits hitting the sea
    for b in bits:
        if b.t_wet > b.t0:
            splashes.append((b.t_wet, b.at(b.t_wet), b.size * 1.3, b.seed, None, None))
    # the big pieces hitting the sea, and their froth as they go under
    for name, f in FALLS.items():
        if f.entry and f.entry[1] is not None:
            te, at, sp = f.entry
            size = float(np.clip(f.size * 0.3, 2.0, 10.0))
            splashes.append((te, at, size, _seed(name, 'in'), None, None))
            if size > 4:
                jolts.append((real_of(te), 4.0))
        for tf_, at, w in f.froth:
            splashes.append((tf_, at, float(np.clip(w * 0.15, 1.5, 5.0)), _seed(name, tf_), None, None))
    # the finale: every block piece's waterline as it goes in; the crown where the deck first meets the sea
    blocks = [n for n in R.PARTS if n not in FALLS]
    first = None
    for tq in np.arange(TF, TF + 4.0, 0.15):
        for n in blocks:
            if not (n.startswith('deck') or n.startswith('leg') or n in ('module_a', 'module_b', 'derrick')):
                continue
            P = _apply(world(n, tq), _samples(n))
            if P[:, 2].max() < 0.3 or P[:, 2].min() > 0:
                continue
            if n.startswith('leg') and tq < TF + 0.5:     # the legs stand in the sea already: no splash yet
                continue
            near = P[np.abs(P[:, 2]) < 2.0]
            if not len(near):
                continue
            if n.startswith('deck') and first is None:
                first = (tq, near.mean(0) * np.array([1, 1, 0]))
            w = float(np.ptp(near[:, 0]) + np.ptp(near[:, 1]))
            splashes.append((tq + 0.05, near.mean(0) * np.array([1, 1, 0]), float(np.clip(w * 0.12, 3.0, 8.0)),
                             _seed(n, tq), None, None))
    if first:
        # Sam, 2 Nov (note 12): an even bigger throw of spray and debris where the deck hits the sea
        splashes.append((first[0], first[1], CROWN[0], 77, CROWN[1], CROWN[2]))
        rng = np.random.default_rng(78)
        cols = DEBRIS_COLS['deck_top'] + DEBRIS_COLS['deck_cellar'] + ('yellow', 'orange')
        for i in range(CROWN_BITS):
            a = rng.uniform(0, 2 * math.pi)
            out_ = rng.uniform(3.0, 13.0)
            p0 = first[1] + np.array([math.cos(a) * 6.0, math.sin(a) * 6.0, rng.uniform(1.0, 4.0)])
            v0 = np.array([math.cos(a) * out_, math.sin(a) * out_, rng.uniform(18.0, 34.0)])
            bits.append(Bit(first[0] + rng.uniform(0, 0.15), p0, v0, float(rng.uniform(1.2, 3.5)),
                            R._tint(R.COL[cols[int(rng.integers(len(cols)))]][int(rng.integers(0, 2))]),
                            int(rng.integers(1 << 30)), float(rng.uniform(-12, 12))))
        jolts.append((real_of(first[0]), 26.0))
    return bits, splashes, puffs, fireballs, fires, jolts


BITS, SPLASHES, PUFFS, FIREBALLS_AT, FIRES_AT, JOLTS = _events()


def _fire_place(fire, t):
    """A burning hole's flame base, along-direction and size at t (it rides its deck); None once it's under."""
    name, t0, c, u, v, n, r = fire
    if t < t0:
        return None
    M = world(name, t)
    base = _apply(M, c + v * r * 0.25 + n * 0.3)     # licking out of the top of the hole
    if base[2] < 0.8:
        return None
    return base, M[0] @ u, M[0] @ n, r


def _fire_out(fire):
    """When a fire goes under (story time), or None."""
    name, t0 = fire[0], fire[1]
    for t in np.arange(max(t0, TF), TF + 4.0, 1 / 48):
        if _fire_place(fire, t) is None:
            return t
    return None


def _flare_tip(t):
    return _apply(world('flare_boom', t), R.FLARE_TIP)


def _flare_out():
    for t in np.arange(BREAK['flare_boom'][0], BREAK['flare_boom'][0] + 6, 1 / 48):
        if _flare_tip(t)[2] < 0.5:
            return t
    return None


FLARE_OUT = _flare_out()


def _smoke_streams():
    """Puffs from what keeps burning: each deck fire, the flare (its smoke ribbon, Showstopper 3), steam where a
    fire or the flare goes under."""
    out = []
    rng = np.random.default_rng(5)
    for fire in FIRES_AT:
        tout = _fire_out(fire) or 99.0
        for i, ts_ in enumerate(np.arange(fire[1], min(tout, 12.0), 0.09)):
            pl = _fire_place(fire, ts_)
            if pl is None:
                break
            base, u, n, r = pl
            p = base + np.array([0, 0, 6.0]) + u * rng.uniform(-r, r)
            # big from the start and quick to grow, so the column stays one dark mass, never a string of beads
            out.append(('smoke', fire[0], FX.Puff(ts_, p, n * 1.5, 7.0, 3.2, rng.uniform(5.5, 8.0), 5.5, 'smoke',
                                                  int(rng.integers(1 << 30)), tau=0.8)))
        if tout < 99:
            pl = _fire_place(fire, tout - 1 / 48)
            at = pl[0] * np.array([1, 1, 0]) if pl else None
            if at is not None:
                for i in range(10):
                    out.append(('steam', fire[0] + '_st', FX.Puff(tout + i * 0.05, at + rng.normal(0, 3, 3) *
                                                                   np.array([1, 1, 0]), rng.normal(0, 2, 3), 6.0,
                                                                   2.0, rng.uniform(5, 8), 3.0, 'steam',
                                                                   int(rng.integers(1 << 30)), tau=0.8)))
    # the ribbon: already there at the cut; it stops when the boom snaps (the gas line is cut; what was in the air
    # drifts off), so a falling flame never strings out a row of beads
    for ts_ in np.arange(-7.0, BREAK['flare_boom'][0], 0.09):
        out.append(('smoke', 'flare', FX.Puff(ts_, R.FLARE_TIP + np.array([1.0, 0, 6.0]) + rng.normal(0, 0.4, 3),
                                              np.zeros(3), 4.5 * rng.uniform(0.85, 1.15), 0.9,
                                              rng.uniform(4.0, 6.0), 7.0, 'smoke', int(rng.integers(1 << 30)),
                                              tau=2.2)))
    if FLARE_OUT:
        at = _flare_tip(FLARE_OUT) * np.array([1, 1, 0])
        for i in range(8):
            out.append(('steam', 'flare_st', FX.Puff(FLARE_OUT + i * 0.05, at + rng.normal(0, 2, 3) *
                                                     np.array([1, 1, 0]), rng.normal(0, 2, 3), 5.0, 1.5,
                                                     rng.uniform(4, 6), 2.6, 'steam', int(rng.integers(1 << 30)))))
    return out


PUFFS = PUFFS + _smoke_streams()
SMOKE_SRCS = {src for kind, src, _ in PUFFS if kind == 'smoke'}
_GROUPS = {}
for _kind_, _src, _pf in PUFFS:
    _GROUPS.setdefault(_src, []).append(_pf)


# ------------------------------------------------- the frame --------------------------------------------------------
def rig_state(t):
    """For flying_whales_rig.draw at story time t: xf (moved pieces), gone (all under), swap (holed decks)."""
    xf, gone = {}, set()
    for n in R.PARTS:
        m = xf_of(n, t)
        if m is None:
            continue
        f = FALLS.get(n)
        if f is not None and f.gone is not None and t >= f.gone:
            gone.add(n)
            continue
        if t > TF and zrange(n, t)[1] < -0.3:
            gone.add(n)
            continue
        xf[n] = m
    return xf, gone, swaps(t)


def _dist(p):
    return float(np.linalg.norm(np.asarray(p, float) - CAM.pos))


def effects(t):
    """Every effect at story time t: ([(distance m, Sprite)] to sort in among the rig and whales, foam polygons for
    the sea, glows for the sea)."""
    cam = CAM
    extra, foam, glows = [], [], []
    # flying bits, grouped by the hit they came from (one sprite each, every bit its own outline)
    groups = {}
    for b in BITS:
        if b.t0 <= t < b.t_wet:
            groups.setdefault((b.t0 // 0.2), []).append(b)
    for key, bs in groups.items():
        items, ds = [], []
        for b in sorted(bs, key=lambda b: -_dist(b.at(t))):
            p = b.at(t)
            poly = FX.chunk_poly(cam, p, b.size, b.spin * (t - b.t0), b.seed)
            if poly:
                items.append((poly, b.col, None, None))
                ds.append(_dist(p))
        if items:
            spr = FX.pieces_sprite(items, 0.0, ol=3.0)
            if spr:
                d = float(np.median(ds))
                extra.append((min(d, FRONT) if key * 0.2 >= TF else d, spr))
    # splashes
    for ts_, at, size, seed, ring, n in SPLASHES:
        age = t - ts_
        if 0 <= age <= 2.2:
            lumps = FX.splash_parts(at, size, age, seed, ring=ring, n=n, high=2.0 if ring is None else (CROWN[3] if size >= CROWN[0] else 2.8))
            spr = FX.lumps_sprite(cam, lumps, 0.0, ol=4.0 if size < 4 else 5.0)
            if spr:
                # the finale's water is thrown up in front of the falling block (note 11: it showed behind the sign)
                extra.append((min(_dist(at) - 1.0, FRONT) if ts_ >= TF else _dist(at) - 1.0, spr))
            if size >= 2.0:
                foam += FX.foam_ring(cam, at, age * (0.9 if size > 8 else 1.2), seed,
                                     size * (0.9 if ring else 0.45))
    # fireballs
    for t0, c, size, seed in FIREBALLS_AT:
        age = t - t0
        if 0 <= age <= 1.0:
            spr = FX.fireball_sprite(cam, c, size, age, seed, 0.0)
            if spr:
                extra.append((_dist(c) - size * 0.3, spr))
            glows.append((tuple(c), 1.0 - 0.5 * age, size * 2.6))
    # deck fires
    for fire in FIRES_AT:
        pl = _fire_place(fire, t)
        if pl is None:
            continue
        base, u, n, r = pl
        spr = FX.fire_sprite(cam, base, u, r * 1.0, 10.0, t, _seed(fire[0], 'fire'), 0.0, n=5)
        if spr:
            extra.append((_dist(base) - 1.5, spr))
        glows.append((tuple(base), 0.55, 16.0))
    # the burning helideck and the flare's flame riding their pieces down
    if t >= BREAK['flare_boom'][0] and (FLARE_OUT is None or t < FLARE_OUT):
        tip = _flare_tip(t)
        lay = Image.new('RGBA', cam.size, (0, 0, 0, 0))
        R.flame(lay, t, tip=tip)
        bb = lay.getbbox()
        if bb:
            extra.append((_dist(tip) - 0.5, W.Sprite(lay.crop(bb), bb[:2], None, bb, 0.0, None)))
    # smoke, steam and dust, one sprite per source
    for src, pfs in _GROUPS.items():
        live = [pf for pf in pfs if pf.at(t) is not None]
        if not live:
            continue
        spr = FX.puffs_sprite(cam, live, t, 0.0)
        if spr:
            ds = [_dist(pf.at(t)[0]) for pf in live]
            d = float(np.median(ds)) - 2.0
            # the tipping block leaned into its own smoke, half the columns in front of it and half behind (note 9):
            # in the finale the smoke goes wholly behind the rig, so the sinking block stays in view
            extra.append((max(d, BACK) if t > TF and src in SMOKE_SRCS else d, spr))
    return extra, foam, glows


def shake(real):
    """Camera jolts (pixels) at real rig-scene time `real`: on each main hit, the big pieces' splashes and the
    finale's crown (the biggest)."""
    dx = dy = 0.0
    for tj, amp in JOLTS:
        u = real - tj
        if 0 <= u < 0.6:
            k = math.exp(-u * 7) * amp
            f = int(u * FPS)
            dx += k * (1 if f % 2 else -1)
            dy += k * 0.6 * (1 if f % 3 else -1)
    return dx, dy


def shift(img, dx, dy):
    """The finished frame moved by (dx, dy) px, the edge it uncovers filled from the nearest row or column."""
    dx, dy = int(round(dx)), int(round(dy))
    if not dx and not dy:
        return img
    a = np.asarray(img)
    a = np.roll(a, (dy, dx), axis=(0, 1))
    if dy > 0:
        a[:dy] = a[dy]
    elif dy < 0:
        a[dy:] = a[dy - 1]
    if dx > 0:
        a[:, :dx] = a[:, dx:dx + 1]
    elif dx < 0:
        a[:, dx:] = a[:, dx - 1:dx]
    return Image.fromarray(a)


# ------------------------------------------------- checks -----------------------------------------------------------
def check():
    """Faults: a contact that no longer matches the paths; anything still above the sea at the end."""
    faults = []
    got = {(k, n): t for t, k, n in PATHS.contacts()}
    for t, k, n in CONTACTS:
        if (k, n) not in got:
            faults.append(f'{PATHS.NAMES[k]} no longer touches {n}')
        elif abs(got[(k, n)] - t) > 0.03:
            faults.append(f'{PATHS.NAMES[k]} touches {n} at {got[(k, n)]:.2f}, the wreck says {t:.2f}')
    end = story(12.0)
    for n in R.PARTS:
        if zrange(n, end)[1] > 0.0:
            faults.append(f'{n} is still above the sea at the end ({zrange(n, end)[1]:.1f} m)')
    for n, f in FALLS.items():
        if f.entry is None:
            faults.append(f'{n} never reaches the sea')
    return faults


def table():
    for t, k, n in CONTACTS:
        what = ('thrown' if n in THROWN else 'holed' if n in HOLES else 'bent' if n in BENT else '')
        extra = (' + fireball' if n in FIREBALLS else '') + (' + fire' if n in FIRES else '')
        print(f'{t:5.2f}  {PATHS.NAMES[k]:8s} {n:18s} {what}{extra}' +
              (f'  holes: {len(HOLES[n])}' if n in HOLES else ''))
    for n, f in FALLS.items():
        print(f'   {n:18s} in the sea {f.entry[0]:.2f}' if f.entry else f'   {n} never in the sea',
              f'gone {f.gone:.2f}' if f.gone else 'not gone')
    for fire in FIRES_AT:
        print(f'   fire on {fire[0]}: {fire[1]:.2f} to {_fire_out(fire)}')
    print(f'   flare out {FLARE_OUT}')
    tq = TF
    while tq < 13:
        top = max(zrange(n, tq)[1] for n in R.PARTS if n not in FALLS)
        if top < 0:
            break
        tq += 0.05
    print(f'   finale: {TF:.2f}, all under at {tq:.2f} (story); real end of scene = story {story(12.0):.2f}')
    print(f'   {len(BITS)} bits, {len(SPLASHES)} splashes, {len(PUFFS)} puffs')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'table'
    if cmd == 'check':
        fs = check()
        for f in fs:
            print('FAULT:', f)
        print('wreck check: clean' if not fs else f'{len(fs)} faults')
    else:
        table()
