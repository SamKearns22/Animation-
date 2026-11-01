#!/usr/bin/env python3
"""Flying Whales, the rig scene's effects (1 Nov: the water burst; the fireballs, smoke, deck fires, steam, crown
splash and dust join this file in the effects stage).

The water burst (Showstopper U12 and rule 16: they burst out of the sea heading up and to the right; rule 15: an
effect is lumpy, never regular spikes; the house look: flat colour, a lit and a shadow tone, one ink outline round the
whole shape, no glows or gradients, no motion lines):
- a collar of lumpy water hugging the whale at the waterline for as long as its body is crossing the surface (it
  hides the cut where whale.draw(cut_z=0) stops the body);
- a column of lumps thrown up with the whale and outwards, flying under gravity, thinning to drops and falling back
  (each lump gone when it drops below the sea);
- a ring of foam on the sea spreading from the hole and breaking into patches (it never fades out: it breaks up).
Everything is laid out in metres in the world and drawn through the rig scene's camera, so it shrinks with distance.
Lumps nearer the lens than the whale's middle are drawn over it, the rest behind (two layers).

    python3 source/flying_whales_fx.py sheet OUT.jpg     the burst at six ages, large, for checking the shape
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import whale as W                                     # noqa: E402
import flying_whales_sea as SEA                       # noqa: E402

G = 9.8
INK = W.INK
WATER = ((242, 228, 232), (200, 184, 206))            # lit, shadow: white water in the pink dusk light
FOAM = ((236, 222, 230), (186, 168, 196))
SIZE = SEA.SIZE


def _crossing(pose, sz):
    """Where the whale's long axis meets the sea surface (world point), or None if it is not crossing it."""
    f = pose.R[:, 0]
    if abs(f[2]) < 1e-3:
        return None
    s = -pose.pos[2] / f[2]
    if -6.2 * sz <= s <= 6.4 * sz:
        return pose.pos + f * s
    return None


def _lumps(seed, n):
    rng = np.random.default_rng(seed)
    th = rng.uniform(0, 2 * math.pi, n)
    out = rng.uniform(1.5, 6.5, n)                    # m/s outwards
    up = rng.uniform(4.0, 13.0, n)                    # m/s up
    r = rng.uniform(0.4, 1.05, n)                     # m
    ring = rng.uniform(1.4, 2.6, n)                   # m from the axis where it leaves
    return th, out, up, r, ring


def burst_parts(cam, whale_pose, sz, age, seed, heading, hole):
    """The burst's lumps at `age` seconds after the whale broke the surface: [(world centre, radius m, lit?,
    velocity m/s)].
    heading: the whale's direction along the sea (unit x, y), so the column leans the way it is going. hole: where it
    broke the surface (world, z = 0): the column and spray are thrown from there, wherever the whale has gone since."""
    out = []
    hole = np.asarray(hole, float)
    # the collar, while the body is still crossing the surface
    c = _crossing(whale_pose, sz)
    if c is not None:
        rng = np.random.default_rng(seed + 7)
        n = 14
        for i in range(n):
            a = 2 * math.pi * i / n + rng.uniform(-0.15, 0.15)
            rad = 2.1 * sz * (0.9 + 0.25 * math.sin(7.0 * age + i * 1.7))
            h = rng.uniform(0.1, 0.7) * (1 + 0.4 * math.sin(9.0 * age + i))
            p = c + np.array([math.cos(a) * rad, math.sin(a) * rad, h])
            out.append((p, rng.uniform(0.6, 1.0) * sz, a < math.pi, np.zeros(3)))   # round froth, no tails
    # the column and spray: thrown at the moment the nose comes out (age 0) and for the next 0.5 s
    if age >= 0:
        for wave in range(3):
            t0 = wave * 0.18
            a = age - t0
            if a < 0:
                continue
            th, vo, vu, r, ring = _lumps(seed + wave * 101, 24)
            for i in range(len(th)):
                d = np.array([math.cos(th[i]), math.sin(th[i]), 0.0])
                v = d * vo[i] + np.array([0, 0, vu[i] * (1.0 - 0.25 * wave)])
                v[:2] += np.asarray(heading) * 3.5                 # leans the way the whale is going
                p = hole + d * ring[i] * sz + v * a + np.array([0, 0, -0.5 * G * a * a])
                if p[2] <= 0:
                    continue
                k = max(0.0, 1.0 - a / 1.0)                         # shrinks to drops as it flies
                rr = r[i] * sz * (0.25 + 0.75 * k)
                out.append((p, rr, (th[i] % (2 * math.pi)) > math.pi * 0.6, v + np.array([0, 0, -G * a])))
    return out


def foam_ring(cam, hole, age, seed, sz=1.0):
    """Foam on the sea round the hole: [polygon in world, z = 0]. One joined, lumpy ring while it spreads (seen this
    low, separate slivers lie side by side like motion lines: viewchecks), then it breaks into floating clumps of
    froth that shrink away (it never fades: the house style has no see-through)."""
    if age < 0 or age > 2.4:
        return []
    rng = np.random.default_rng(seed + 3)
    R = 2.8 * sz + 6.0 * (1 - math.exp(-age * 1.4))
    w0 = (2.4 - 0.9 * min(age, 2.0) / 2.0) * sz            # the ring's width across, m
    n = 72
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    lump = 1 + 0.28 * np.sin(ang * 5 + seed) + 0.18 * np.sin(ang * 11 + seed * 2.3)
    outer = R + w0 * 0.5 * lump
    inner = R - w0 * 0.5 * (2 - lump) * 0.6
    if age < 0.9:                                          # whole: an outer edge and the hole in it
        ring = [hole + np.array([math.cos(a) * r, math.sin(a) * r, 0.0]) for a, r in zip(ang, outer)]
        hole_pts = [hole + np.array([math.cos(a) * r, math.sin(a) * r, 0.0]) for a, r in zip(ang, inner)]
        return [('ring', np.array(ring), np.array(hole_pts))]
    pieces = []                                            # broken up: floating clumps of froth, shrinking away
    k = max(0.0, 1.0 - (age - 0.9) / 1.5)
    for i in range(16):
        a = 2 * math.pi * (i + rng.uniform(-0.3, 0.3)) / 16
        if rng.uniform() > 0.35 + 0.65 * k:
            continue
        r = float(np.interp(a, ang, (outer + inner) / 2, period=2 * math.pi)) + rng.uniform(-0.4, 0.4) * sz
        c = hole + np.array([math.cos(a) * r, math.sin(a) * r, 0.0])
        pieces.append(('clump', c, (0.5 + 0.5 * rng.uniform()) * sz * (0.35 + 0.65 * k)))
    return pieces


def _teardrop(x, y, tx, ty, rp, seed):
    """A smooth drop: round front of radius rp at (x, y), tapering to a point at (tx, ty) (where it was a moment ago,
    so the tail follows its arc and grows with its speed); a still drop is simply round. The edge is a little uneven
    (seeded), so no two are alike."""
    dx, dy = x - tx, y - ty
    L = math.hypot(dx, dy)
    if L < rp * 0.6:
        n = 20
        return [(x + rp * (1 + 0.06 * math.sin(seed * 17 + k * 2.1)) * math.cos(2 * math.pi * k / n),
                 y + rp * (1 + 0.06 * math.sin(seed * 17 + k * 2.1)) * math.sin(2 * math.pi * k / n)) for k in range(n)]
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    pts = []
    for k in range(17):                                           # the round front, one side round to the other
        a = -math.pi / 2 + math.pi * k / 16
        w = rp * (1 + 0.06 * math.sin(seed * 31.0 + k * 1.9))
        pts.append((x + (ux * math.cos(a) + px * math.sin(a)) * w, y + (uy * math.cos(a) + py * math.sin(a)) * w))
    # the front ends on the +p side; go down that side to the tip, then back up the -p side
    for k in range(1, 9):
        f = k / 8
        w = rp * (1 - f) ** 1.6
        pts.append((x - ux * L * f + px * w, y - uy * L * f + py * w))
    for k in range(7, 0, -1):
        f = k / 8
        w = rp * (1 - f) ** 1.6
        pts.append((x - ux * L * f - px * w, y - uy * L * f - py * w))
    return pts


def _ink_layer(mask, lit, shadow_col, lit_col, ol, ss):
    """One flat shape: shadow tone, lit tone where `lit`, one ink outline round the whole (outside the mask)."""
    m = np.asarray(mask) > 0
    k = max(3, int(round(ol * ss)) | 1)
    outer = np.asarray(mask.filter(ImageFilter.MaxFilter(k))) > 0
    ink = outer & ~m
    rgb = np.zeros(m.shape + (3,), np.uint8)
    rgb[m] = shadow_col
    rgb[m & (np.asarray(lit) > 0)] = lit_col
    rgb[ink] = INK
    a = (outer * 255).astype(np.uint8)
    img = Image.fromarray(np.dstack([rgb, a]), 'RGBA')
    if ss == 1:
        return img
    small = np.asarray(img.resize((img.width // ss, img.height // ss), Image.LANCZOS)).copy()
    small[..., 3][small[..., 3] < 10] = 0              # the faint ringing the shrink leaves round every edge
    return Image.fromarray(small, 'RGBA')


def _crop(polys, pad, margin=60):
    """The screen box (x0, y0, x1, y1) round some polygons, padded, kept near the frame; None if empty."""
    pts = [np.asarray(p, float).reshape(-1, 2) for p in polys if len(p)]
    if not pts:
        return None
    allp = np.concatenate(pts)
    x0, y0 = np.floor(allp.min(0) - pad)
    x1, y1 = np.ceil(allp.max(0) + pad)
    x0, y0 = max(x0, -margin), max(y0, -margin)
    x1, y1 = min(x1, SIZE[0] + margin), min(y1, SIZE[1] + margin)
    if x1 - x0 < 2 or y1 - y0 < 2:
        return None
    return int(x0), int(y0), int(x1), int(y1)


def _sprite(img, x0, y0, depth):
    bb = img.getbbox()
    if not bb:
        return None
    return W.Sprite(img, (x0, y0), None, (bb[0] + x0, bb[1] + y0, bb[2] + x0, bb[3] + y0), depth, None)


def shape_sprite(tones, depth, ss=2, ol=5.0):
    """One flat shape in a few tones, cropped to its box: tones = [(colour, [screen polygons])]; the first tone is the
    whole silhouette, each later one is painted over it (inside); one ink outline round the silhouette. A Sprite or
    None. (Rule 15 and the house look: flat tones, one outline, no glow, no see-through.)"""
    if not tones or not tones[0][1]:
        return None
    olp = ol * SIZE[0] / 1080
    box = _crop([p for _, ps in tones for p in ps], olp * 2 + 4)
    if box is None:
        return None
    x0, y0, x1, y1 = box
    w, h = (x1 - x0) * ss, (y1 - y0) * ss
    tr = lambda p: [((x - x0) * ss, (y - y0) * ss) for x, y in p]
    mask = Image.new('L', (w, h), 0)
    dm = ImageDraw.Draw(mask)
    for p in tones[0][1]:
        if len(p) > 2:
            dm.polygon(tr(p), fill=255)
    rgb = Image.new('RGB', (w, h), tones[0][0])
    dr = ImageDraw.Draw(rgb)
    for col, ps in tones[1:]:
        for p in ps:
            if len(p) > 2:
                dr.polygon(tr(p), fill=col)
    m = np.asarray(mask) > 0
    k = max(3, int(round(olp * ss)) | 1)
    outer = np.asarray(mask.filter(ImageFilter.MaxFilter(k))) > 0
    arr = np.asarray(rgb).copy()
    arr[outer & ~m] = INK
    img = Image.fromarray(np.dstack([arr, (outer * 255).astype(np.uint8)]), 'RGBA')
    if ss > 1:
        small = np.asarray(img.resize((x1 - x0, y1 - y0), Image.LANCZOS)).copy()
        small[..., 3][small[..., 3] < 10] = 0
        img = Image.fromarray(small, 'RGBA')
    return _sprite(img, x0, y0, depth)


def pieces_sprite(items, depth, ss=2, ol=4.0):
    """Separate flat pieces, each with its OWN ink outline, drawn in order (far first): items = [(screen polygon,
    colour, inner polygon or None, inner colour)]. Smoke clumps, flying bits: they overlap as separate things, never
    melting into one cloud. A Sprite or None."""
    items = [it for it in items if len(it[0]) > 2]
    if not items:
        return None
    olp = ol * SIZE[0] / 1080
    box = _crop([it[0] for it in items], olp * 2 + 4)
    if box is None:
        return None
    x0, y0, x1, y1 = box
    w, h = (x1 - x0) * ss, (y1 - y0) * ss
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for pts, col, inner, icol in items:
        P = np.asarray(pts, float)
        c = P.mean(0)
        v = P - c
        L = np.linalg.norm(v, axis=1, keepdims=True) + 1e-6
        ink = c + v * (L + olp) / L                     # the outline: the piece grown by one line's width
        d.polygon([((x - x0) * ss, (y - y0) * ss) for x, y in ink], fill=INK + (255,))
        d.polygon([((x - x0) * ss, (y - y0) * ss) for x, y in P], fill=tuple(col) + (255,))
        if inner is not None and len(inner) > 2:
            d.polygon([((x - x0) * ss, (y - y0) * ss) for x, y in inner], fill=tuple(icol) + (255,))
    if ss > 1:
        small = np.asarray(img.resize((x1 - x0, y1 - y0), Image.LANCZOS)).copy()
        small[..., 3][small[..., 3] < 10] = 0
        img = Image.fromarray(small, 'RGBA')
    return _sprite(img, x0, y0, depth)


def lumps_sprite(cam, lumps, depth, ss=2, ol=5.0, cols=None):
    """Lumps [(world centre, radius m, lit?, velocity)] as one flat shape (a Sprite, cropped), or None. Each lump is
    a teardrop: round at the front, drawn out into a tail behind it by its speed (thrown water streams; a falling
    drop points down), so the water reads as water, never as cotton wool or a row of coins."""
    cols = cols or WATER
    sil, lit = [], []
    for p, r, is_lit, v in lumps:
        p = np.asarray(p, float)
        s, d = cam.screen(p)
        if d < 1.0:
            continue
        rp = cam.focal * r / d
        x, y = s[0], s[1]
        if x < -rp * 4 - 60 or y < -rp * 4 - 60 or x > SIZE[0] + rp * 4 + 60 or y > SIZE[1] + rp * 4 + 60:
            continue
        tx, ty = cam.screen(p - np.asarray(v) * (0.13 if v[2] > 0 else 0.07))[0]   # where it was a moment ago
        sil.append(_teardrop(x, y, tx, ty, rp, r))
        if is_lit:                       # the lit side faces the sunset (left) and the sky: smaller, up and left
            o = rp * 0.28
            lit.append(_teardrop(x - o, y - o, tx - o, ty - o, rp * 0.6, r))
    if not sil:
        return None
    return shape_sprite([(cols[1], sil), (cols[0], lit)], depth, ss, ol)


def draw_lumps(cam, lumps, ss=2, ol=5.0):
    """The lumps (see lumps_sprite) over a clear full frame (RGBA), or None."""
    spr = lumps_sprite(cam, lumps, 0.0, ss, ol)
    if spr is None:
        return None
    img = Image.new('RGBA', cam.size, (0, 0, 0, 0))
    spr.paste(img)
    return img


def draw_foam(img, cam, polys, ss=2, ol=4.0):
    """Foam on the sea, drawn straight onto img (RGBA): one flat shape (lit nearer edge, shadow far edge), one outline.
    polys: from foam_ring ('ring' with its hole, or 'clump' with its centre and size)."""
    if not polys:
        return
    sil, holes, lit = [], [], []

    def scr(P):
        s, d = cam.screen(P)
        return None if (d < 1.0).any() else [(x, y) for x, y in s]
    for kind, P, H in polys:
        if kind == 'clump':                                          # a squat lump of froth sitting on the sea
            s, d = cam.screen(P)
            if d < 1.0:
                continue
            w = cam.focal * H / d
            h = max(w * 0.5, 3.0)
            x, y = s[0], s[1]
            n = 14
            sil.append([(x + w * math.cos(a), y + (h if math.sin(a) < 0 else h * 0.4) * math.sin(a))
                        for a in np.linspace(0, 2 * math.pi, n, endpoint=False)])
            lit.append([(x - w * 0.22 + w * 0.62 * math.cos(a), y - h * 0.5 + h * 0.4 * math.sin(a))
                        for a in np.linspace(0, 2 * math.pi, n, endpoint=False)])
            continue
        q = scr(P)
        if q is None:
            continue
        sil.append(q)
        ys = [y for _, y in q]
        cut = min(ys) + (max(ys) - min(ys)) * 0.45                    # the near half of the ring catches the sky
        lit.append([(x, max(y, cut)) for x, y in q])
        if H is not None:
            h = scr(H)
            if h:
                holes.append(h)
    if not sil:
        return
    olp = ol * SIZE[0] / 1080
    box = _crop(sil, olp * 2 + 4)
    if box is None:
        return
    x0, y0, x1, y1 = box
    w, h = (x1 - x0) * ss, (y1 - y0) * ss
    tr = lambda p: [((x - x0) * ss, (y - y0) * ss) for x, y in p]
    mask = Image.new('L', (w, h), 0)
    lm = Image.new('L', (w, h), 0)
    dm, dl = ImageDraw.Draw(mask), ImageDraw.Draw(lm)
    for p in sil:
        dm.polygon(tr(p), fill=255)
    for p in lit:
        dl.polygon(tr(p), fill=255)
    for p in holes:
        dm.polygon(tr(p), fill=0)
        dl.polygon(tr(p), fill=0)
    lay = _ink_layer(mask, lm, FOAM[1], FOAM[0], olp, ss)
    img.alpha_composite(lay, (x0, y0))


# ================================ the hits' effects (1 Nov, effects stage) ===========================================
# Fire: dark red edge, orange, yellow core (refs fire-*); smoke in separate dark clumps (refs collapse-cranes-fireball);
# white steam; beige-grey dust (ref collapse-dust). All flat, each with one ink outline; nothing fades (see-through
# is off-style): smoke and dust rise and drift off, or shrink away at the end of their life.
FIRE = ((172, 48, 40), (246, 126, 40), (255, 214, 96))     # edge, middle, core
PUFF_COLS = {'smoke': ((92, 78, 88), (46, 40, 50)),       # (lit, shadow): the lit side faces the sunset (left)
             'steam': ((242, 232, 238), (196, 182, 206)),
             'dust': ((206, 186, 168), (156, 140, 134))}
WIND = np.array([3.0, 0.0, 0.0])                          # m/s: the flare's flame leans right; smoke drifts right


def _blob(x, y, r, seed, n=11, squash=1.0, rough=0.22):
    """A lumpy round outline (screen): n soft lobes of different sizes, hand-cut, never points (rule 15)."""
    rng = np.random.default_rng(int(seed) % (1 << 31))
    a0 = rng.uniform(0, 2 * math.pi)
    rad = rng.uniform(1 - rough, 1.0, n)
    pts = []
    for i in range(n * 3):
        f = i / 3
        i0, i1 = int(f) % n, (int(f) + 1) % n
        w = f - int(f)
        rr = rad[i0] + (rad[i1] - rad[i0]) * (3 * w * w - 2 * w * w * w) + 0.06 * math.sin(math.pi * w)
        a = a0 + 2 * math.pi * f / n
        pts.append((x + r * rr * math.cos(a), y + r * rr * squash * math.sin(a)))
    return pts


def _scaled(pts, k, dx=0.0, dy=0.0):
    P = np.asarray(pts, float)
    c = P.mean(0)
    return [tuple(q) for q in c + (P - c) * k + (dx, dy)]


# ------------------------------------------------- fireball ---------------------------------------------------------
def fireball_lumps(centre, size, age, seed):
    """The fireball at `age` s: [(world centre, radius m)]. It bursts out fast (most of its size in 0.15 s), taller
    than wide, rising; it is gone by 1.0 s (its smoke, spawned by the film, carries on)."""
    if not (0.0 <= age <= 1.0):
        return []
    rng = np.random.default_rng(seed)
    n = 15
    d = rng.normal(0, 1, (n, 3))
    d[:, 2] = np.abs(d[:, 2]) * 2.0 + 0.6                 # mostly up: a tall column, taller than wide
    d[:, :2] *= 0.7
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    D = size * rng.uniform(0.25, 1.25, n)
    r = size * rng.uniform(0.32, 0.55, n)
    e = 1 - math.exp(-age / 0.07)
    end = 1.0 if age < 0.78 else max(0.0, (1.0 - age) / 0.22)   # it burns out: the lumps shrink away
    c = np.asarray(centre, float) + np.array([0, 0, 5.0 * age])
    return [(c + d[i] * D[i] * e, r[i] * (0.45 + 0.55 * e) * (1 + 0.35 * age) * end) for i in range(n) if end > 0]


def fireball_sprite(cam, centre, size, age, seed, depth):
    """The fireball as one flat shape: dark red edge, orange, a yellow core that burns down first."""
    lumps = fireball_lumps(centre, size, age, seed)
    if not lumps:
        return None
    blobs = []
    for i, (p, r) in enumerate(lumps):
        s, d = cam.screen(p)
        if d < 1.0 or r <= 0:
            continue
        blobs.append(_blob(s[0], s[1], cam.focal * r / d, seed * 31 + i, n=9))
    if not blobs:
        return None
    ko = max(0.0, 0.78 - 0.55 * age)                      # the orange shrinks as it cools
    ky = max(0.0, 0.8 * (1 - age / 0.42))                 # the yellow core goes first
    cy = max(y for b in blobs for _, y in b) - min(y for b in blobs for _, y in b)
    tones = [(R_tint(FIRE[0]), blobs)]
    if ko > 0.05:
        tones.append((R_tint(FIRE[1]), [_scaled(b, ko, 0, cy * 0.06) for b in blobs]))
    if ky > 0.3:              # one joined core from the middle lumps (smaller, it would break into yellow freckles)
        mid = np.mean([np.mean(b, 0) for b in blobs], 0)
        core = sorted(blobs, key=lambda b: np.linalg.norm(np.mean(b, 0) - mid))[:6]
        tones.append((FIRE[2], [_scaled(b, ky, 0, cy * 0.1) for b in core]))
    return shape_sprite(tones, depth, ol=5.0)


def R_tint(c):
    """Dusk tint, as the rig's (fires keep their heat: a light touch)."""
    tr, tg, tb, tk = SEA.DUSK_TINT
    tk *= 0.35
    return tuple(int(c[i] * (1 - tk) + (tr, tg, tb)[i] * tk) for i in range(3))


# ------------------------------------------------- smoke, steam, dust -----------------------------------------------
class Puff:
    """One clump of smoke, steam or dust: born at t0 at p0 (world) thrown at v0 (slowed by the air, k per s), rising
    at `rise` m/s and drifting with the wind, growing from r0 to r1 m; at the end of its life it shrinks away."""
    __slots__ = ('t0', 'p0', 'v0', 'rise', 'r0', 'r1', 'tau', 'life', 'kind', 'seed', 'k')

    def __init__(self, t0, p0, v0, rise, r0, r1, life, kind, seed, tau=0.8, k=2.5):
        self.t0, self.p0, self.v0 = t0, np.asarray(p0, float), np.asarray(v0, float)
        self.rise, self.r0, self.r1, self.life, self.kind, self.seed, self.tau, self.k = \
            rise, r0, r1, life, kind, seed, tau, k

    def at(self, t):
        u = t - self.t0
        if u < 0 or u > self.life:
            return None
        g = (1 - math.exp(-self.k * u)) / self.k
        wind = WIND * (0.5 if self.kind == 'dust' else 1.0)
        p = self.p0 + self.v0 * g + wind * u + np.array([0, 0, self.rise * u])
        r = self.r0 + (self.r1 - self.r0) * (1 - math.exp(-u / self.tau))
        r *= min(1.0, (self.life - u) / 0.7)
        if p[2] + r < 0 or r <= 0.05:                     # a dust clump sinking into the sea is gone
            return None
        return p, r


def puffs_sprite(cam, puffs, t, depth, ol=4.0):
    """Clumps drawn far to near, each its own lumpy blob with its own outline and a lit side up and to the left."""
    live = []
    for pf in puffs:
        st = pf.at(t)
        if st is None:
            continue
        p, r = st
        s, d = cam.screen(p)
        if d < 1.0:
            continue
        rp = cam.focal * r / d
        if rp < 1.5 or s[1] < -rp - 40 or s[0] < -rp - 40 or s[0] > SIZE[0] + rp + 40 or s[1] > SIZE[1] + rp:
            continue
        live.append((d, s, rp, pf))
    if not live:
        return None
    items = []
    for d, s, rp, pf in sorted(live, key=lambda q: -q[0]):
        lit, shadow = PUFF_COLS[pf.kind]
        b = _blob(s[0], s[1], rp, pf.seed, n=9, squash=0.9)
        items.append((b, shadow, _scaled(b, 0.62, -rp * 0.2, -rp * 0.22), lit))
    return pieces_sprite(items, depth, ol=ol)


# ------------------------------------------------- fire on a deck ---------------------------------------------------
def fire_sprite(cam, base, along, half, height, t, seed, depth, n=4):
    """Flames licking out of a hole: n tongues standing on a line (world: base +- along * half m), each its own
    height, leaning right with the wind, flickering (a new shape every 3 frames at 24 fps); orange with a yellow
    heart, one outline round them all."""
    rng = np.random.default_rng(seed * 977 + int(t * 8))
    outer, inner = [], []
    along = np.asarray(along, float)
    for i in range(n):
        f = (i + 0.5) / n * 2 - 1
        b = np.asarray(base, float) + along * half * f * 0.85
        (sx, sy), d = cam.screen(b)
        if d < 1.0:
            continue
        k = cam.focal / d
        h = height * rng.uniform(0.55, 1.0) * (1.0 - 0.3 * abs(f))
        wd = half / n * 1.5 * rng.uniform(0.8, 1.2)
        for shrink, lst in ((0.0, outer), (0.45, inner)):
            hh = h * (1 - shrink * 0.55)
            pts = []
            m = 9
            for side in (1, -1):
                rng2 = np.random.default_rng(seed * 13 + i * 7 + int(t * 8) + (side > 0))
                for j in (range(m) if side > 0 else range(m - 1, -1, -1)):
                    g = j / (m - 1)
                    w = wd * math.sin(math.pi * min(1.0, g * 1.1 + 0.08)) * (1 - shrink) + 0.25
                    lean = 0.55 * hh * g ** 1.5                     # bending over with the wind
                    x = sx + (lean + side * w * (1 + 0.22 * rng2.uniform(-1, 1))) * k
                    pts.append((x, sy - hh * g * k))
            lst.append(pts)
    if not outer:
        return None
    return shape_sprite([(R_tint(FIRE[1]), outer), (FIRE[2], inner)], depth, ol=5.0)


# ------------------------------------------------- splashes ---------------------------------------------------------
def splash_parts(at, size, age, seed, ring=None, n=None, high=2.0):
    """Water thrown up where something hits the sea: [(world centre, radius m, lit?, velocity)] like the burst's.
    A ring of lumps thrown up and out (each its own speed, so never a regular crown of spikes), then a column rising
    in the middle as the ring falls back. size: the thing's size in m (a 1 m bit makes a splash about 2 m high, the
    deck block one 25 m high). ring: the ring's radius (m), size * 0.4 if not given."""
    if age < 0 or age > 2.2:
        return []
    rng = np.random.default_rng(seed)
    n = n or int(8 + min(18, size * 1.5))
    ring = size * 0.4 if ring is None else ring
    at = np.asarray(at, float) * np.array([1, 1, 0])
    out = []
    th = rng.uniform(0, 2 * math.pi, n)
    H = size * rng.uniform(0.6, 1.0, n) * high
    vu = np.sqrt(2 * G * H)
    vo = vu * rng.uniform(0.18, 0.42, n)
    rad = size * rng.uniform(0.16, 0.3, n)
    for i in range(n):
        d = np.array([math.cos(th[i]), math.sin(th[i]), 0.0])
        v = d * vo[i] + np.array([0, 0, vu[i]])
        p = at + d * ring * rng.uniform(0.7, 1.1) + v * age + np.array([0, 0, -0.5 * G * age * age])
        if p[2] <= 0:
            continue
        k = max(0.0, 1.0 - age / (2 * vu[i] / G + 0.2))
        out.append((p, rad[i] * (0.35 + 0.65 * k), (th[i] % (2 * math.pi)) > math.pi * 0.6,
                    v + np.array([0, 0, -G * age])))
    if age < 0.7:                                         # the mound of white water at its foot, joining it all
        k = 1 - age / 0.7
        for j in range(6):
            a = th[j % n] + j * 1.1
            p = at + np.array([math.cos(a) * ring * 0.6, math.sin(a) * ring * 0.6, size * 0.25 * k])
            out.append((p, size * (0.22 + 0.2 * k) * (0.8 + 0.1 * j % 3), j % 2 == 0, np.zeros(3)))
    a2 = age - 0.25                                       # the column in the middle as the ring falls back
    if a2 > 0:
        for j in range(3):
            vu2 = math.sqrt(2 * G * size * high * (0.55 + 0.2 * j))
            p = at + np.array([rng.uniform(-0.15, 0.15) * size, rng.uniform(-0.15, 0.15) * size, 0]) + \
                np.array([0, 0, vu2 * a2 - 0.5 * G * a2 * a2])
            if p[2] > 0:
                out.append((p, size * (0.32 - 0.07 * j), j == 0, np.array([0, 0, vu2 - G * a2])))
    return out


def chunk_poly(cam, p, size, ang, seed):
    """A flying bit of the rig on screen: an uneven 4-6 sided chunk (never a stick: no motion lines), turning."""
    s, d = cam.screen(p)
    if d < 1.0:
        return None
    r = cam.focal * size / d
    if r < 1.2:
        r = 1.2
    rng = np.random.default_rng(seed)
    nv = int(rng.integers(4, 7))
    rad = rng.uniform(0.55, 1.0, nv)
    sq = rng.uniform(0.6, 1.0)
    a = np.linspace(0, 2 * math.pi, nv, endpoint=False) + rng.uniform(-0.3, 0.3, nv)
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    for rr, aa in zip(rad, a):
        x, y = r * rr * math.cos(aa), r * rr * sq * math.sin(aa)
        pts.append((s[0] + x * ca - y * sa, s[1] + x * sa + y * ca))
    return pts


# ------------------------------------------------- a hole in a deck -------------------------------------------------
HOLE_DARK = (54, 40, 46)
EMBER = (255, 190, 100)                                   # one of the rig's lamp colours: not tinted


def hole_items(c, u, v, n, r, seed):
    """Spot items (flying_whales_rig 'spot': painted on the face) for a ragged hole torn in a face: an ink rim, the
    dark inside, embers glowing low in it. c: the centre (world), u and v: the face's directions (unit), n: its
    outward normal; r: radius in m."""
    rng = np.random.default_rng(seed)
    m = 13
    a = np.linspace(0, 2 * math.pi, m, endpoint=False) + rng.uniform(-0.18, 0.18, m)
    rad = rng.uniform(0.62, 1.12, m)
    c = np.asarray(c, float) + np.asarray(n) * 0.06
    ring = lambda k, dz=0.0: np.array([c + (u * math.cos(t) * q + v * (math.sin(t) * q * 0.85 + dz)) * r * k
                                       for t, q in zip(a, rad)])
    emb = np.array([c + (u * math.cos(t) * 0.5 + v * (math.sin(t) * 0.28 - 0.35)) * r * q
                    for t, q in zip(a, rng.uniform(0.7, 1.0, m))])
    return [dict(kind='spot', pts=ring(1.0 + 0.45 / r), n=np.asarray(n, float), col=INK),
            dict(kind='spot', pts=ring(1.0), n=np.asarray(n, float), col=HOLE_DARK),
            dict(kind='spot', pts=emb, n=np.asarray(n, float), col=EMBER)]


def _test_pose(age, sz=1.0):
    v = np.array([0.35, 0.6, 0.72])
    v /= np.linalg.norm(v)
    ps = W.Pose(v * (16.0 * age - 6.4))                     # the middle; the nose broke the surface at age 0
    up = np.array([0, 0, 1.0]) - v * v[2]
    up /= np.linalg.norm(up)
    ps.R = np.stack([v, np.cross(up, v), up], axis=1)
    return ps, v


TEST_CAM = W.Cam(pos=(0.0, -40.0, 4.0), yaw=0.0, pitch=8.0, focal=1400.0, size=SIZE)
TEST_FAR = W.Cam(pos=(0.0, -120.0, 8.0), yaw=0.0, pitch=8.0, focal=1400.0, size=SIZE)


def test_draw(age, what='burst'):
    """One effect alone at `age` for the film's EFFECTS list (viewchecks tests its shape, rule 15): 'burst' (the
    collar, column and spray) or 'foam' (the flat ring on the sea: tested apart, since its long flat ellipse round the
    burst would read to the star test as two long points)."""
    def draw(img):
        cam = TEST_CAM
        spr = None
        if what == 'foam':
            draw_foam(img, cam, foam_ring(cam, np.zeros(3), age, 5))
            return
        if what == 'fireball':
            spr = fireball_sprite(cam, np.array([0, 0, 8.0]), 8.0, age, 7, 0.0)
        elif what in ('smoke', 'steam', 'dust'):
            rng = np.random.default_rng(3)
            pf = [Puff(-rng.uniform(0, 2.5), (rng.uniform(-3, 3), rng.uniform(-2, 2), 6.0), rng.normal(0, 1, 3),
                       2.0 if what != 'dust' else 0.3, 1.0, 3.5, 5.0, what, int(rng.integers(1 << 20)))
                  for _ in range(14)]
            spr = puffs_sprite(cam, pf, 0.0, 0.0)
        elif what == 'fire':
            spr = fire_sprite(cam, np.array([0, 0, 6.0]), np.array([1.0, 0, 0]), 2.5, 7.0, age, 4, 0.0, n=5)
        elif what == 'splash':
            spr = lumps_sprite(cam, splash_parts(np.zeros(3), 2.0, age, 9), 0.0)
        elif what == 'crown':
            spr = lumps_sprite(TEST_FAR, splash_parts(np.zeros(3), 13.0, age, 77, ring=9.0, n=34, high=1.9), 0.0)
        elif what == 'bits':
            rng = np.random.default_rng(2)
            items = [(chunk_poly(cam, (rng.uniform(-6, 6), rng.uniform(-3, 3), rng.uniform(2, 12)),
                                 rng.uniform(0.2, 0.6), rng.uniform(0, 6), int(rng.integers(1 << 20))),
                      (150, 150, 160), None, None) for _ in range(16)]
            spr = pieces_sprite([it for it in items if it[0]], 0.0, ol=3.0)
        if what != 'burst':
            if spr:
                spr.paste(img)
            return
        ps, v = _test_pose(age)
        lay = draw_lumps(TEST_CAM, burst_parts(TEST_CAM, ps, 1.0, age, 5, v[:2] / np.linalg.norm(v[:2]), np.zeros(3)))
        if lay:
            img.alpha_composite(lay.resize(img.size) if lay.size != img.size else lay)
    return draw


def sheet(out):
    """The burst at six ages, on the dusk sea, through a closer camera (shape check)."""
    cam = W.Cam(pos=(0.0, -40.0, 4.0), yaw=0.0, pitch=8.0, focal=1400.0, size=SIZE)
    tiles = []
    for age in (0.0, 0.2, 0.4, 0.7, 1.0, 1.5):
        im = SEA.paint(age, cam=cam, ss=1).convert('RGBA')
        sz = 1.0
        v = np.array([0.35, 0.6, 0.72])
        v /= np.linalg.norm(v)
        nose_out = np.array([0.0, 0.0, 0.0])
        pos = nose_out + v * (16.0 * age - 6.4)                     # the middle; the nose broke the surface at age 0
        f = v
        up = np.array([0, 0, 1.0]) - f * f[2]
        up /= np.linalg.norm(up)
        ps = W.Pose(pos)
        ps.R = np.stack([f, np.cross(up, f), up], axis=1)
        lumps = burst_parts(cam, ps, sz, age, 5, v[:2] / np.linalg.norm(v[:2]), np.zeros(3))
        draw_foam(im, cam, foam_ring(cam, np.array([0.0, 0, 0]), age, 5))
        back = [l for l in lumps if np.linalg.norm(l[0] - cam.pos) >= np.linalg.norm(ps.pos - cam.pos)]
        front = [l for l in lumps if np.linalg.norm(l[0] - cam.pos) < np.linalg.norm(ps.pos - cam.pos)]
        for lay in (draw_lumps(cam, back),):
            if lay:
                im.alpha_composite(lay)
        spr = W.draw(cam, ps, pattern=0, t=age, cut_z=0.0, tint=SEA.DUSK_TINT)
        if spr:
            spr.paste(im)
        lay = draw_lumps(cam, front)
        if lay:
            im.alpha_composite(lay)
        SEA._label(im, f'{age:.1f} s after the nose comes out')
        tiles.append(im.convert('RGB').crop((0, 300, 1080, 1500)).resize((540, 600)))
    sh = Image.new('RGB', (1620, 1200))
    for i, t in enumerate(tiles):
        sh.paste(t, ((i % 3) * 540, (i // 3) * 600))
    sh.save(out, quality=88)
    print('saved', out)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
    else:
        print(__doc__)
