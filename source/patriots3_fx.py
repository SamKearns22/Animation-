#!/usr/bin/env python3
"""Patriots 3: the shell hitting the slit's lip (shot 8 on) and the muzzle light (shots 2 and 9), house style: flat,
lumpy, one frame for flashes, no stars or glows (prepper_fx). Refs blast-1 (a shell bursting on a building: a dark
churning cloud with a bright core, debris thrown out), blast-2 (a burst on concrete: orange fire, black smoke, chips).

Everything the blast leaves stays (rule 32 and 'anything that changes stays changed'): the bite out of the lintel and
the chips on the floor are drawn in every later shot.
"""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import sets as S                 # noqa: E402
import prepper_fx as FX          # noqa: E402
import patriots3_plan as PL      # noqa: E402
import patriots3_act as A        # noqa: E402
from ed import INK               # noqa: E402

LIP = (-0.45, 2.1, PL.Z_OUT + 0.08)                 # where the shell bursts: the outer top edge of the slit
X0, Z0, X1, Z1 = PL.ROOMS['casemate']
CONC, CONC_D, RAW = (150, 146, 136), (112, 108, 100), (178, 172, 160)
DUST, DUST_D = (176, 170, 158), (128, 124, 116)
PIECES = None


def pieces():
    """The concrete chips knocked in off the lintel's inner edge: each its own size and speed, landing on the floor
    and staying (prepper_fx.Piece bounces them off the walls)."""
    global PIECES
    if PIECES is None:
        PIECES = FX.burst(A.T_BLAST + 0.04, (-0.4, 2.0, PL.Z_IN - 0.05), 16, 3.2, seed=44, kind='chip', col=CONC,
                          size=0.05, up=0.6, dirn=(0.15, -0.2, -1.0), box=(X0, X1, Z0, Z1), spread=0.8)
        PIECES += FX.burst(A.T_BLAST + 0.06, (-0.2, 2.0, PL.Z_IN - 0.05), 14, 2.2, seed=45, kind='chip', col=CONC_D,
                           size=0.028, up=0.4, dirn=(-0.1, -0.3, -1.0), box=(X0, X1, Z0, Z1), spread=1.0)
        _spread_out(PIECES)
    return PIECES


def _spread_out(ps):
    """Rule 32: no piece rests on another. Where two would come to rest overlapping, the later one is nudged along
    the floor (its whole track after it lands) until it lies clear."""
    rest = []
    for pc in ps:
        (x, y, z), a = pc.track[-1]
        for _ in range(20):
            hit = next(((rx, rz, rr) for rx, rz, rr in rest if math.hypot(x - rx, z - rz) < (pc.size + rr) * 0.7), None)
            if hit is None:
                break
            d = np.array([x - hit[0], z - hit[1]]) + 1e-3
            d = d / np.linalg.norm(d) * (pc.size + hit[2]) * 0.75
            x, z = hit[0] + d[0], hit[1] + d[1]
        land = len(pc.track) - 1
        while land > 0 and pc.track[land - 1][0] == pc.track[-1][0]:
            land -= 1
        ox, oz = pc.track[-1][0][0], pc.track[-1][0][2]
        if (x, z) != (ox, oz):
            for i in range(max(0, land - 12), len(pc.track)):        # eased in over its last bounce (no jump)
                w = min(1.0, (i - max(0, land - 12)) / 12)
                (px, py, pz), pa = pc.track[i]
                pc.track[i] = ((px + (x - ox) * w, py, pz + (z - oz) * w), pa)
        rest.append((x, z, pc.size))


def lintel_bite(img, cam, t):
    """The bite the shell took out of the lintel's edge: raw lighter concrete, a jagged edge (drawn on the slit wall's
    inner face just above the slit head, from the blast on)."""
    if t < A.T_BLAST:
        return
    p = S.pen(img)
    z = PL.Z_IN - 0.004
    head = PL.SLIT_TOP
    xs = np.linspace(-0.85, 0.05, 9)
    rng = np.random.default_rng(12)
    top = [(x, head + 0.06 + rng.uniform(0.0, 0.16) * math.sin(math.pi * (x + 0.85) / 0.9), z) for x in xs]
    pts = [(-0.9, head, z)] + top + [(0.1, head, z)]
    cam.poly(p, pts, RAW, INK, 2.0)
    for i in range(3):                                 # a couple of cracks running up from it
        x = -0.7 + i * 0.3
        cam.line(p, [(x, head + 0.1, z), (x + 0.05, head + 0.2, z), (x + 0.02, head + 0.3, z)], CONC_D, 1.6)
    if cam.pos[2] > PL.Z_IN or cam.depth((0, head, z)) > 0:   # the bite runs through the reveal's head too
        cam.poly(p, [(-0.85, head - 0.003, PL.Z_IN), (0.05, head - 0.003, PL.Z_IN), (0.1, head - 0.003, PL.Z_OUT),
                     (-0.95, head - 0.003, PL.Z_OUT)], (88, 84, 78), None)


def chips(img, cam, t):
    for pc in pieces():
        FX.draw_piece(img, cam, pc, t)


def puffs(t):
    """The dust cloud: lumpy grey puffs pouring in through the slit and rolling into the room, thinning out over
    about 3 s. Each puff is (centre, radius in metres, opacity, seed); the film draws them in depth order with the
    people (a puff behind someone is hidden by them)."""
    u = t - A.T_BLAST
    if not (0.0 <= u <= 4.0):
        return []
    rng = np.random.default_rng(9)
    out = []
    for i in range(16):
        x0 = rng.uniform(-1.2, 0.5)
        y0 = rng.uniform(1.1, 2.0)
        sp = rng.uniform(0.8, 1.6)
        d0 = rng.uniform(0.0, 0.25)
        dx, sz, seed = rng.uniform(-0.05, 0.45), rng.uniform(0.8, 1.2), int(rng.integers(1 << 20))   # drifting east,

        w = u - d0
        if w <= 0:
            continue
        reach = 1.9 * (1 - math.exp(-w * sp))         # rolling in, slowing down (never past the Patriot)
        c = (x0 + dx * reach, y0 - 0.15 * reach + 0.1 * w, PL.Z_IN - 0.1 - reach)
        a = int(170 * max(0.0, 1 - w / 2.4))
        if a > 4:
            out.append((c, (0.14 + 0.24 * min(1.0, w / 1.2)) * sz, a, seed))
    return out


def draw_puff(img, cam, pf):
    c, rm, a, seed = pf
    if cam.depth(c) < 0.25:
        return
    (X, Y), k = cam.project(c)
    r = rm * k
    rng = np.random.default_rng(seed)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    p = S.pen(lay)
    pts = [(X + r * rng.uniform(0.8, 1.15) * math.cos(q), Y + r * 0.85 * rng.uniform(0.8, 1.15) * math.sin(q))
           for q in np.linspace(0, 2 * math.pi, 11, endpoint=False)]
    p.poly(pts, DUST_D + (a,), None)
    p.poly([(X + (x - X) * 0.7 - r * 0.08, Y + (y - Y) * 0.7 - r * 0.1) for x, y in pts], DUST + (a,), None)
    img.alpha_composite(lay)


def dust(img, cam, t):
    """Over the whole frame after the people: grit falling from the ceiling and the room dulled by dust, clearing."""
    u = t - A.T_BLAST
    if not (0.0 <= u <= 4.0):
        return
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    p = S.pen(lay)
    rng = np.random.default_rng(10)
    for i in range(10):                                # grit falling from the ceiling
        x, z = rng.uniform(-1.2, 0.6), rng.uniform(-0.6, 0.9)
        d0 = rng.uniform(0.05, 1.2)
        w = u - d0
        if not (0 <= w <= 0.6):
            continue
        y = PL.CEIL - 0.5 * 9.8 * w * w
        if y < 0.02:
            continue
        cam.line(p, [(x, y + 0.04, z), (x, y, z)], (90, 86, 80, 230), 2.4)
    img.alpha_composite(lay)
    haze = int(50 * max(0.0, 1 - u / 3.0))
    if haze > 0:
        img.alpha_composite(Image.new('RGBA', img.size, DUST + (haze,)))


def blast_flash(img, cam, t):
    """The burst itself: two frames of a big lumpy orange flash at the lip (seen through the slit and over its edge),
    then a dark churning cloud outside for a second (ref blast-1), and the room lit by it."""
    u = t - A.T_BLAST
    if 0.0 <= u < 0.17:
        FX.flash(img, cam, LIP, 1.6, seed=3)
        FX.room_flash(img, 1.0)
    if 0.12 <= u < 1.4:                                 # the black smoke outside the slit
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        p = S.pen(lay)
        rng = np.random.default_rng(21)
        for i in range(9):
            c = (LIP[0] + rng.uniform(-0.9, 0.9), LIP[1] - 0.2 + rng.uniform(-0.4, 0.3) + 0.4 * u,
                 LIP[2] + rng.uniform(0.2, 0.9))
            if cam.depth(c) < 0.25:
                continue
            (X, Y), k = cam.project(c)
            r = (0.3 + 0.4 * u) * k * rng.uniform(0.8, 1.2)
            a = int(235 * max(0.0, 1 - (u - 0.12) / 1.3))
            pts = [(X + r * rng.uniform(0.8, 1.15) * math.cos(q), Y + r * 0.85 * rng.uniform(0.8, 1.15) * math.sin(q))
                   for q in np.linspace(0, 2 * math.pi, 11, endpoint=False)]
            p.poly(pts, (48, 46, 46, a), None)
            if u < 0.4:
                p.poly([(X + (x - X) * 0.45, Y + (y - Y) * 0.45) for x, y in pts], (236, 140, 50, a), None)
        img.alpha_composite(lay)


def shake(t):
    """The camera kicked by the blast: a few quick decaying jolts (pixels)."""
    u = t - A.T_BLAST
    if not (0 <= u < 0.6):
        return (0.0, 0.0)
    k = math.exp(-u * 7) * 26
    f = int(u * 12)
    return (k * (1 if f % 2 else -1), k * 0.6 * (1 if f % 3 else -1))


def muzzle_light(img, t):
    """The room lit by the muzzle flash on the frames it fires (shots 2 and 9): a flat warm step lighter."""
    a = A.flash_on(t)
    if a:
        FX.room_flash(img, 0.85 * a)
