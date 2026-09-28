#!/usr/bin/env python3
"""Redraw a 3D render as a graphite pencil drawing, the way an illustrator would: firm outlines where one form
passes in front of another, lighter lines at creases; tone built up with hatching that follows each surface -
along the ribs of the knit, down the hair, round the curve of a cheek - soft smudged graphite on skin, looser
and lighter work in the background, highlights left as bare paper.

Usage:
    python3 graphite.py PASSES.npz OUT.png [--scale 0.75]
"""
import sys

import numpy as np
from numba import njit, prange
from PIL import Image

import materials as MS
import sdf3d as S

# which materials belong to what
CHAR_SKIN = {MS.SKIN, MS.LIPS, MS.LID, MS.NOSTRIL, MS.NAIL}
CHAR_SKIN = CHAR_SKIN | {MS.MAN_SKIN}
CHAR = CHAR_SKIN | {MS.EYE, MS.HAIR, MS.STRAW_HAIR, MS.KNIT, MS.TROUSERS, MS.COTTON, MS.FELT, MS.FUR,
                    MS.SHIRT, MS.MAN_HAIR, MS.SOCK}
PROPS = {MS.WOOD, MS.MEAT, MS.BONE, MS.STEEL, MS.HANDLE, MS.HAMPINK, MS.PINEAPPLE, MS.CHERRY, MS.PAPER,
         MS.PASTRY, MS.CHERRY_FILL, MS.ICING, MS.ICING_GREEN,
         MS.GIFTWRAP, MS.RIBBON, MS.GORE, MS.BLOOD, MS.GIFT_RED, MS.XMAS_JUMPER, MS.LINEN, MS.GLASS, MS.SHELL,
         MS.LEATHER, MS.COAT, MS.CLOTH_LIGHT, MS.CLOTH_MID, MS.DENIM, MS.PLASTIC, MS.SCREEN,
         MS.XMAS_GREEN_KNIT}


# ---------------------------------------------------------------------------
# small image tools
# ---------------------------------------------------------------------------
def blur(a, sigma):
    if sigma <= 0:
        return a
    h, w = a.shape
    ph, pw = h + int(4 * sigma), w + int(4 * sigma)
    p = np.pad(a, ((0, ph - h), (0, pw - w)), mode='reflect')
    fy = np.fft.fftfreq(ph)[:, None]
    fx = np.fft.rfftfreq(pw)[None, :]
    k = np.exp(-2 * (np.pi * sigma) ** 2 * (fx ** 2 + fy ** 2))
    return np.fft.irfft2(np.fft.rfft2(p) * k, (ph, pw))[:h, :w]


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


@njit(fastmath=True, cache=True)
def _bil(a, x, y):
    h, w = a.shape
    if x < 0.0:
        x = 0.0
    if y < 0.0:
        y = 0.0
    if x > w - 1.001:
        x = w - 1.001
    if y > h - 1.001:
        y = h - 1.001
    x0, y0 = int(x), int(y)
    fx, fy = x - x0, y - y0
    return (a[y0, x0] * (1 - fx) * (1 - fy) + a[y0, x0 + 1] * fx * (1 - fy)
            + a[y0 + 1, x0] * (1 - fx) * fy + a[y0 + 1, x0 + 1] * fx * fy)


@njit(parallel=True, fastmath=True, cache=True)
def lic(noise, vx, vy, length, region):
    """Smear noise along the direction field: pencil strokes. Strokes stop at region boundaries so they don't
    run from the hair into the face or from the jumper into the wall."""
    h, w = noise.shape
    out = np.zeros((h, w), np.float32)
    for j in prange(h):
        for i in range(w):
            acc = noise[j, i]
            wsum = 1.0
            reg = region[j, i]
            for sgn in (1.0, -1.0):
                x, y = float(i), float(j)
                px, py = vx[j, i] * sgn, vy[j, i] * sgn
                for k in range(length):
                    xi, yi = int(x + 0.5), int(y + 0.5)
                    if xi < 0 or yi < 0 or xi >= w or yi >= h:
                        break
                    dx, dy = vx[yi, xi], vy[yi, xi]
                    if dx * px + dy * py < 0:
                        dx, dy = -dx, -dy
                    x += dx
                    y += dy
                    px, py = dx, dy
                    xi, yi = int(x + 0.5), int(y + 0.5)
                    if xi < 0 or yi < 0 or xi >= w or yi >= h or region[yi, xi] != reg:
                        break
                    wt = 1.0 - k / length
                    acc += _bil(noise, x, y) * wt
                    wsum += wt
            out[j, i] = acc / wsum
    return out


def project_dirs(dir3, pos, cam, W, H):
    """Screen-space direction (unit) of a 3D direction field at each pixel."""
    o = cam[0:3]
    f, r, u = cam[3:6], cam[6:9], cam[9:12]
    th, aspect = cam[12], cam[13]

    def proj(p):
        d = p - o
        z = d @ f
        x = (d @ r) / (z * th * aspect)
        y = (d @ u) / (z * th)
        return (x + 1) * 0.5 * W, (1 - y) * 0.5 * H

    x0, y0 = proj(pos)
    x1, y1 = proj(pos + dir3 * 0.01)
    dx, dy = x1 - x0, y1 - y0
    L = np.sqrt(dx * dx + dy * dy) + 1e-9
    return (dx / L).astype(np.float32), (dy / L).astype(np.float32)


def angle_field(deg, shape):
    a = np.radians(deg)
    return np.full(shape, np.cos(a), np.float32), np.full(shape, np.sin(a), np.float32)


# ---------------------------------------------------------------------------
# the drawing
# ---------------------------------------------------------------------------
# Things that keep their colour in the drawing: the food, fruit, the tree and the decorations, laid in with
# coloured pencil over a graphite world - warmth now, and later, blood against grey.
def colour_mats():
    """Pencil colour for each coloured material (what an illustrator would pick from the tin)."""
    return {MS.MEAT: (0.80, 0.45, 0.14), MS.HAMPINK: (0.93, 0.58, 0.55), MS.PINEAPPLE: (0.98, 0.84, 0.25),
            MS.CHERRY: (0.85, 0.08, 0.10), MS.CLEMENTINE: (0.98, 0.55, 0.12), MS.NEEDLES: (0.18, 0.48, 0.26),
            MS.GOLD: (0.90, 0.70, 0.22), MS.BAUBLE_RED: (0.85, 0.10, 0.12), MS.FAIRY: (1.0, 0.85, 0.40),
            MS.FLAME: (1.0, 0.72, 0.28), MS.FELT: (0.82, 0.12, 0.14),
            MS.CHERRY_FILL: (0.72, 0.05, 0.10), MS.ICING_GREEN: (0.32, 0.62, 0.28),
            MS.COTTON: (0.64, 0.82, 0.96),      # the daughter's top: light sky blue
            # the spare room: the present's paper and ribbon, the Christmas clothes and presents, and blood -
            # bright where it is fresh on the wall, nearly black-red where it seeps from the present
            MS.GIFTWRAP: (0.20, 0.52, 0.30), MS.RIBBON: (0.90, 0.70, 0.22), MS.GIFT_RED: (0.84, 0.12, 0.14),
            MS.XMAS_JUMPER: (0.82, 0.12, 0.14), MS.BLOOD: (0.86, 0.04, 0.06), MS.GORE: (0.40, 0.03, 0.05),
            MS.XMAS_GREEN_KNIT: (0.22, 0.55, 0.30),
            MS.LIGHT_RED: (1.0, 0.30, 0.25), MS.LIGHT_GREEN: (0.40, 0.95, 0.45), MS.LIGHT_BLUE: (0.40, 0.60, 1.0),
            MS.LIGHT_YELLOW: (1.0, 0.88, 0.35), MS.LIGHT_ORANGE: (1.0, 0.60, 0.25),
            MS.DEAD_RED: (0.70, 0.20, 0.20), MS.DEAD_GREEN: (0.25, 0.50, 0.30), MS.DEAD_BLUE: (0.25, 0.35, 0.65),
            MS.DEAD_YELLOW: (0.75, 0.65, 0.30), MS.DEAD_ORANGE: (0.75, 0.45, 0.20)}


def colour_pencil(rgbo, grey, rgb, mat, strokes, px):
    """Lay coloured pencil over the colour things: each its own pencil colour, carried by the drawing's own
    light and shade and broken by the stroke texture, the graphite lifted where colour replaces it."""
    cols = colour_mats()
    mask = np.zeros(mat.shape, np.float32)
    hue = np.ones(mat.shape + (3,), np.float32)
    for m, c in cols.items():
        sel = mat == m
        mask[sel] = 1.0
        hue[sel] = c
    mask = blur(mask, 0.7 * px)  # a soft pencil edge, not a cut-out
    for k in range(3):
        hue[..., k] = blur(hue[..., k], 0.7 * px)
    amount = np.clip(0.80 + 0.2 * strokes, 0.55, 1.0)
    # colour laid over the finished graphite drawing, not instead of it: its outlines, shading and hatching
    # show through, so the coloured things are drawn by the same hand as everything else
    lifted = 1 - (1 - grey) * 0.80
    col = lifted[..., None] * (1 - amount[..., None] * (1 - hue))
    return rgbo * (1 - mask[..., None]) + col * mask[..., None]


def focus_map(cam, W, H, fx, fy, points):
    """Where the drawing wants the eye (the shot says: her face, the raised blade and the hand under it). 1
    there, falling to 0 away from them. An illustrator spends the detail and the darkest lines here and lets
    the rest go."""
    o, f, r, u = cam[0:3], cam[3:6], cam[6:9], cam[9:12]
    th, aspect = cam[12], cam[13]
    out = np.zeros(fx.shape, np.float32)
    for p, rad in zip(points, (0.16, 0.14, 0.12, 0.12, 0.12)):
        d = p - o
        z = d @ f
        x = ((d @ r) / (z * th * aspect) + 1) * 0.5
        y = (1 - (d @ u) / (z * th)) * 0.5
        dist = np.sqrt(((fx - x) * aspect) ** 2 + (fy - y) ** 2)
        out = np.maximum(out, np.exp(-(dist / rad) ** 2))
    return out


def draw(npz_path, out_path, scale=1.0, seed=3, crop=None, px=None, stats=None):
    """Draw the whole frame, or (crop) just a window of it - for animation, where only the part that moved is
    redrawn. A window comes out stroke for stroke the same as that part of the whole drawing (the paper grain
    and stroke noise are made for the whole frame; `stats` from the whole drawing keep the tones the same), so
    it can be pasted in without a seam. Returns the stats."""
    Z = np.load(npz_path)
    rgb, depth, normal, mat, pos, glass, cam = (Z['rgb'], Z['depth'], Z['normal'], Z['mat'], Z['pos'],
                                                Z['glass'], Z['cam'])
    H0, W0 = depth.shape
    fy, fx = np.mgrid[0:H0, 0:W0].astype(np.float32)
    fx, fy = fx / W0, fy / H0  # where each pixel sits in the whole frame, 0..1
    foc = focus_map(Z['cam'], W0, H0, fx, fy, Z['focus'])
    char0 = np.isin(mat, list(CHAR))
    near_d = np.median(depth[char0]) if char0.any() else 3.0      # (from the whole frame)
    px = W0 / 2560 if px is None else px  # stroke sizes are designed at 2560 wide
    win = (slice(crop[1], crop[3]), slice(crop[0], crop[2])) if crop is not None else (slice(None), slice(None))
    rngs = np.random.SeedSequence(seed).spawn(6)

    def noise(k, sigma, normal=False):
        """The k-th paper/stroke noise, made for the whole frame, then cut to the window."""
        g = np.random.default_rng(rngs[k])
        a = g.standard_normal((H0, W0)) if normal else g.random((H0, W0))
        return blur(a, sigma)[win].astype(np.float32)
    if crop is not None:  # a window of the frame, for quick trials (x0, y0, x1, y1)
        x0, y0, x1, y1 = crop
        rgb, depth, normal, mat, pos, glass, fx, fy, foc = (a[y0:y1, x0:x1] for a in
                                                            (rgb, depth, normal, mat, pos, glass, fx, fy, foc))
    fx0, fy0 = fx, fy
    sl = (slice(crop[1], crop[3]), slice(crop[0], crop[2])) if crop is not None else (slice(None), slice(None))
    H, W = depth.shape

    tone = S.tonemap(rgb, 1.05) @ np.array([0.30, 0.59, 0.11])
    char = np.isin(mat, list(CHAR))
    props = np.isin(mat, list(PROPS))
    subject = char | props
    coloured = np.isin(mat, list(colour_mats()))
    drawn = subject | coloured  # given a firm pencil outline
    skin = np.isin(mat, list(CHAR_SKIN))
    hair = np.isin(mat, [MS.HAIR, MS.STRAW_HAIR, MS.MAN_HAIR])
    fair = mat == MS.STRAW_HAIR          # fair hair: drawn lightly, a few fine strands, bright where it shines
    knit = mat == MS.KNIT
    eye = mat == MS.EYE
    bg = ~subject
    # how far behind her each thing is, 0 near her .. 1 at the back wall
    recede = np.clip((depth - near_d - 0.3) / 2.0, 0, 1) * bg

    # --- tone the drawing aims for. The background is lighter and flatter, as a draughtsman would leave it.
    T = tone.copy()
    T = np.where(bg, 0.16 + 0.84 * np.clip(T, 0, 1) ** 0.9, T)
    T = np.where(bg, T + (1 - T) * 0.25 * recede, T)
    # the light falls off towards the ceiling and the far corners of the room: a soft darkening of the
    # background away from her, which also keeps the eye on her
    fall = np.clip(((fx - 0.42) / 0.62) ** 2 + ((fy - 0.55) / 0.75) ** 2, 0, 1.5)
    T = np.where(bg, T * (1 - 0.16 * fall), T)
    T = np.where(skin, 0.10 + 0.90 * np.clip(T, 0, 1) ** 1.15, T)  # skin: light, smoothly modelled
    T = np.where(hair & ~fair, 0.10 + 0.90 * np.clip(T, 0, 1) ** 0.6, T)
    T = np.where(fair, 0.38 + 0.62 * np.clip(T, 0, 1), T)
    # hollows (eye sockets, under the nose, corners of the mouth, under the jaw) a touch darker, as an artist
    # would press into them: where the surface bends away (the normals converge on screen)
    ncx = normal @ cam[6:9]
    ncy = normal @ cam[9:12]
    div = np.gradient(blur(ncx, 1.5 * px), axis=1) - np.gradient(blur(ncy, 1.5 * px), axis=0)
    cav = np.clip(-div / (0.05 / px), 0, 1) * (depth > 0)
    cav = blur(cav, 2.0 * px)
    T = T - 0.14 * cav * skin - 0.22 * cav * (char & ~skin) - 0.10 * cav * props
    # local contrast: bring out the modelling of forms
    T = np.clip(T + 0.45 * (T - blur(T, 18 * px)) * (subject + 0.4 * bg), 0, 1)
    dark = 1 - T

    # --- region labels (strokes stop at these edges)
    region = np.zeros((H, W), np.int32)
    region[skin | eye] = 1
    region[hair] = 2
    region[knit] = 3
    region[props] = 4
    region[bg] = 5
    region[mat == MS.MARBLE] = 6

    # --- direction fields
    vx, vy = angle_field(-58.0, (H, W))  # the natural slant of a right-handed artist's hatching
    ok = depth > 0
    hx, hy = project_dirs(Z['hairdir'].astype(np.float32)[sl], pos, cam, W0, H0)
    vx = np.where(hair, hx, vx)
    vy = np.where(hair, hy, vy)
    kx, ky = project_dirs(Z['knitdir'].astype(np.float32)[sl], pos, cam, W0, H0)
    vx = np.where(knit, kx, vx)
    vy = np.where(knit, ky, vy)
    # skin: follow the form - along the lines of equal light, blended with the slant
    gy, gx = np.gradient(blur(T, 3 * px))
    gl = np.sqrt(gx * gx + gy * gy) + 1e-6
    wgt = np.clip(gl / 0.01, 0, 1) * 0.7
    sx, sy = -gy / gl, gx / gl
    flip = (sx * vx + sy * vy) < 0
    sx, sy = np.where(flip, -sx, sx), np.where(flip, -sy, sy)
    fx = vx * (1 - wgt) + sx * wgt
    fy = vy * (1 - wgt) + sy * wgt
    fl = np.sqrt(fx * fx + fy * fy) + 1e-6
    vx = np.where(skin, fx / fl, vx).astype(np.float32)
    vy = np.where(skin, fy / fl, vy).astype(np.float32)
    # the board along its grain, the blade along its length
    bdx, bdy = project_dirs(np.broadcast_to(np.array([1.0, 0, 0]), pos.shape), pos, cam, W0, H0)
    wood = mat == MS.WOOD
    vx = np.where(wood, bdx, vx)
    vy = np.where(wood, bdy, vy)
    blx, bly = project_dirs(np.broadcast_to(Z['bladedir'], pos.shape), pos, cam, W0, H0)
    steel = mat == MS.STEEL
    vx = np.where(steel, blx, vx)
    vy = np.where(steel, bly, vy)
    vx = vx.astype(np.float32)
    vy = vy.astype(np.float32)

    # --- strokes
    L = max(4, int(13 * px))
    grain = noise(0, 0.7 * px)
    s1 = lic(grain, vx, vy, L, region)
    grain2 = noise(1, 0.7 * px)
    c, s_ = np.cos(np.radians(62)), np.sin(np.radians(62))
    s2 = lic(grain2, (vx * c - vy * s_).astype(np.float32), (vx * s_ + vy * c).astype(np.float32), L, region)
    hl = max(6, int(34 * px))  # long strands in the hair
    grain3 = noise(2, 0.5 * px)
    s3 = lic(grain3, vx, vy, hl, region)

    new_stats = {} if stats is None else stats

    def nrm(z, key):
        if key not in new_stats:
            new_stats[key] = (float(z.mean()), float(z.std()) + 1e-9)
        m, sd = new_stats[key]
        return (z - m) / sd

    s1, s2, s3 = nrm(s1, 's1'), nrm(s2, 's2'), nrm(s3, 's3')

    # graphite rubbed smooth for soft gradations; hatching laid over it as tone deepens; cross-hatching in
    # the deepest shadows; long dark strands in the hair
    smudge_amt = np.where(skin, 0.72, np.where(fair, 0.28, np.where(hair, 0.45, np.where(bg, 0.40, 0.55))))
    grain_mod = np.where(skin, 0.97 + 0.03 * s1, 0.85 + 0.15 * s1)  # skin blended smooth with a stump
    smudge = np.clip(np.where(skin, blur(dark, 3.5 * px), blur(dark, 2.2 * px)), 0, 1) ** 1.1 * smudge_amt * \
        np.clip(grain_mod, 0.5, 1.2)
    hatch_start = np.where(skin, 0.50, np.where(bg, 0.34, 0.30))
    m1 = np.clip((dark * 2.2 - 0.95 - s1 * 0.45) * 1.8, 0, 1) * np.clip((dark - hatch_start) * 2.4, 0, 1)
    m1 = m1 * np.where(skin, 0.55, 1.0)  # skin is blended more than hatched
    m2 = np.clip((dark * 2.3 - 1.65 - s2 * 0.45) * 2.0, 0, 1) * (1 - 0.6 * skin) * (1 - 0.75 * knit)
    m2 = m2 * np.clip((dark - 0.40) * 4.0, 0, 1)  # cross-hatching only where it is really dark
    strands = np.clip((dark * 1.9 - 0.55 - s3 * 0.75) * 1.6, 0, 1) * (hair & ~fair)
    # fair hair: fewer, finer, lighter strands, and none where the light catches it
    sheen = smoothstep(0.62, 0.85, tone)
    strands = strands + np.clip((dark * 1.9 - 0.62 - s3 * 0.9) * 1.3, 0, 1) * 0.55 * (1 - sheen) * fair
    marks = 1 - (1 - smudge) * (1 - m1 * 0.62) * (1 - m2 * 0.6) * (1 - strands * 0.8)
    # away from the focus the shading is left lighter and looser, fading out towards the frame's edges the
    # way a drawing is left unfinished at its margins
    margin = smoothstep(0.30, 0.52, np.maximum(np.abs(fx0 - 0.5), np.abs(fy0 - 0.5) * 0.9))
    marks = marks * np.where(bg, 0.78 + 0.22 * foc, 0.86 + 0.14 * foc) * (1 - 0.35 * margin * bg)

    # --- outlines from the geometry
    dz = np.maximum.reduce([np.abs(np.roll(depth, s, a) - depth) for s in (1, -1) for a in (0, 1)])
    occl = smoothstep(0.012, 0.05, dz / np.maximum(depth, 1e-3)) * ok
    nd = np.minimum.reduce([(np.roll(normal, s, a) * normal).sum(-1) for s in (1, -1) for a in (0, 1)])
    crease = smoothstep(0.10, 0.45, 1 - nd) * ok
    matedge = np.zeros((H, W), bool)
    for s in (1, -1):
        for a in (0, 1):
            other = np.roll(mat, s, a)
            # where hair meets skin there is no line: the hairline is drawn only by the strokes of the hair
            soft = (np.isin(other, [MS.HAIR, MS.STRAW_HAIR]) & skin) | (np.isin(mat, [MS.HAIR, MS.STRAW_HAIR]) & np.isin(other, list(CHAR_SKIN)))
            matedge |= (other != mat) & ~soft
    crease_bg = smoothstep(0.25, 0.6, 1 - nd) * ok  # only the sharper corners in the background
    crease = np.where(subject, crease, crease_bg)
    crease = crease * ~(knit | hair)  # the knit's ribs and the hair's strands come through as tone, not lines
    lines = np.maximum(occl, np.where(skin, 0.25, 0.5) * crease)
    lines = np.maximum(lines, 0.45 * matedge * (drawn | np.roll(drawn, 1, 0) | np.roll(drawn, 1, 1)))
    # the subject drawn with a firmer line, the coloured things with a clear one; the rest finer and paler
    wt = np.where(subject | np.roll(subject, 2, 1) | np.roll(subject, -2, 1), 0.85,
                  np.where(drawn | np.roll(drawn, 2, 1) | np.roll(drawn, -2, 1), 0.65, 0.42 * (1 - 0.55 * recede)))
    # more line where the eye should go, less far from it
    wt = wt * (0.72 + 0.40 * foc)
    lines = blur(lines, 0.6 * px) * wt
    # pressure varies along the line
    press = 0.75 + 0.35 * nrm(noise(3, 6 * px), 'press')
    line_dark = np.clip(lines * 1.6 * press, 0, 1)
    # a thicker line along her outer silhouette
    sil = blur(occl * subject, 1.2 * px)
    line_dark = np.maximum(line_dark, np.clip(sil * 1.1, 0, 1) * 0.6 * (0.6 + 0.4 * dark))

    # --- a little of the render's own detail lines (eyelids, lips, knit) via a colour-dodge sketch
    g = tone
    inv = blur(1 - g, 2.5 * px)
    dodge = np.clip(g / (1 - inv + 1e-3), 0, 1)
    dodge = 1 - np.clip((dodge - 0.55) / 0.45, 0, 1) ** 1.5
    detail = dodge * (0.8 * subject + 0.18 * bg)

    # --- highlights stay paper: candle flames, bulbs, the glint on the blade, catchlights
    bright = smoothstep(0.93, 1.0, tone)

    # --- put it together on the paper
    tooth = noise(4, 0.6 * px, normal=True) * 0.022
    paper = 0.968 + tooth
    ink = 1 - (1 - marks * 0.93) * (1 - line_dark * 0.92) * (1 - detail * 0.5)
    ink = ink * (1 - 0.85 * bright)
    ink = np.maximum(ink, glass * 0.55)
    out = paper * (1 - ink)
    # graphite catches the tooth of the paper in the mid-tones
    out = out + tooth * np.where(skin, 0.5, 1.2) * smoothstep(0.1, 0.5, ink) * (1 - smoothstep(0.6, 0.9, ink))
    out = np.clip(out, 0, 1)
    rgbo = np.stack([out, out * 0.988, out * 0.965], -1)
    rgbo = colour_pencil(rgbo, out, rgb, mat, s1, px)
    img = Image.fromarray((np.clip(rgbo, 0, 1) * 255).astype(np.uint8))
    if scale != 1.0:
        img = img.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
    img.save(out_path, optimize=True)
    print('saved', out_path)
    return new_stats


if __name__ == '__main__':
    args = sys.argv[1:]
    scale = float(args[args.index('--scale') + 1]) if '--scale' in args else 1.0
    crop = tuple(int(v) for v in args[args.index('--crop') + 1].split(',')) if '--crop' in args else None
    draw(args[0], args[1], scale, crop=crop)
