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


def draw_lumps(cam, lumps, ss=2, ol=5.0):
    """Lumps [(world centre, radius m, lit?, velocity)] drawn as one flat shape over a clear full frame (RGBA), or
    None. Each lump is a teardrop: round at the front, drawn out into a tail behind it by its speed (thrown water
    streams; a falling drop points down), so the burst reads as water, never as cotton wool or a row of coins."""
    if not lumps:
        return None
    Wd, Hd = cam.size
    mask = Image.new('L', (Wd * ss, Hd * ss), 0)
    lit = Image.new('L', (Wd * ss, Hd * ss), 0)
    dm, dl = ImageDraw.Draw(mask), ImageDraw.Draw(lit)
    drawn = 0
    for p, r, is_lit, v in lumps:
        p = np.asarray(p, float)
        s, d = cam.screen(p)
        if d < 1.0:
            continue
        rp = cam.focal * r / d * ss
        x, y = s[0] * ss, s[1] * ss
        if x < -rp * 4 or y < -rp * 4 or x > Wd * ss + rp * 4 or y > Hd * ss + rp * 4:
            continue
        back = cam.screen(p - np.asarray(v) * (0.13 if v[2] > 0 else 0.07))[0] * ss   # falling drops stay stubby          # where it was a moment ago (along its arc)
        tx, ty = back
        dm.polygon(_teardrop(x, y, tx, ty, rp, r), fill=255)
        # the lit side faces the sunset (left) and the sky: the same drop, smaller, nudged up and to the left
        if is_lit:
            o = rp * 0.28
            dl.polygon(_teardrop(x - o, y - o, tx - o, ty - o, rp * 0.6, r), fill=255)
        drawn += 1
    if not drawn:
        return None
    return _ink_layer(mask, lit, WATER[1], WATER[0], ol * Wd / 1080, ss)


def draw_foam(img, cam, polys, ss=2, ol=4.0):
    """Foam on the sea, drawn straight onto img (RGBA): one flat shape (lit nearer edge, shadow far edge), one outline.
    polys: from foam_ring ('ring' with its hole, or 'clump' with its centre and size)."""
    if not polys:
        return
    Wd, Hd = cam.size
    mask = Image.new('L', (Wd * ss, Hd * ss), 0)
    lit = Image.new('L', (Wd * ss, Hd * ss), 0)
    dm, dl = ImageDraw.Draw(mask), ImageDraw.Draw(lit)

    def scr(P):
        s, d = cam.screen(P)
        return None if (d < 1.0).any() else [(x * ss, y * ss) for x, y in s]
    for kind, P, H in polys:
        if kind == 'clump':                                          # a squat lump of froth sitting on the sea
            s, d = cam.screen(P)
            if d < 1.0:
                continue
            w = cam.focal * H / d * ss
            h = max(w * 0.5, 3.0 * ss)
            x, y = s[0] * ss, s[1] * ss
            dm.ellipse([x - w, y - h, x + w, y + h * 0.4], fill=255)
            dl.ellipse([x - w * 0.85, y - h * 0.9, x + w * 0.4, y - h * 0.1], fill=255)
            continue
        q = scr(P)
        if q is None:
            continue
        dm.polygon(q, fill=255)
        ys = [y for _, y in q]
        cut = min(ys) + (max(ys) - min(ys)) * 0.45                    # the near half of the ring catches the sky
        dl.polygon([(x, max(y, cut)) for x, y in q], fill=255)
        if H is not None:
            h = scr(H)
            if h:
                dm.polygon(h, fill=0)
                dl.polygon(h, fill=0)
    lay = _ink_layer(mask, lit, FOAM[1], FOAM[0], ol * Wd / 1080, ss)
    img.alpha_composite(lay)


def _test_pose(age, sz=1.0):
    v = np.array([0.35, 0.6, 0.72])
    v /= np.linalg.norm(v)
    ps = W.Pose(v * (16.0 * age - 6.4))                     # the middle; the nose broke the surface at age 0
    up = np.array([0, 0, 1.0]) - v * v[2]
    up /= np.linalg.norm(up)
    ps.R = np.stack([v, np.cross(up, v), up], axis=1)
    return ps, v


TEST_CAM = W.Cam(pos=(0.0, -40.0, 4.0), yaw=0.0, pitch=8.0, focal=1400.0, size=SIZE)


def test_draw(age, what='burst'):
    """One effect alone at `age` for the film's EFFECTS list (viewchecks tests its shape, rule 15): 'burst' (the
    collar, column and spray) or 'foam' (the flat ring on the sea: tested apart, since its long flat ellipse round the
    burst would read to the star test as two long points)."""
    def draw(img):
        if what == 'foam':
            draw_foam(img, TEST_CAM, foam_ring(TEST_CAM, np.zeros(3), age, 5))
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
