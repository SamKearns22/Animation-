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

import mother_scene as MS
import sdf3d as S

# which materials belong to what
CHAR_SKIN = {MS.SKIN, MS.LIPS, MS.LID, MS.NOSTRIL, MS.NAIL}
CHAR = CHAR_SKIN | {MS.EYE, MS.HAIR, MS.KNIT}
PROPS = {MS.WOOD, MS.MEAT, MS.BONE, MS.STEEL, MS.HANDLE}


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
# direction fields from the 3D scene
# ---------------------------------------------------------------------------
def hair_flow(pos, mask):
    """Direction the hair runs, looked up in the sculpt's own lock directions."""
    lo, d, voxel, flow = MS.get_hair_grid()
    out = np.zeros(pos.shape, np.float32)
    out[..., 1] = -1
    idx = np.round((pos[mask] - lo) / voxel).astype(int)
    idx = np.clip(idx, 0, np.array(flow.shape[:3]) - 1)
    # search a little way in for a lock direction (the surface voxel may sit just outside the locks)
    f = flow[idx[:, 0], idx[:, 1], idx[:, 2]]
    for off in ((0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0)):
        missing = np.linalg.norm(f, axis=1) < 0.5
        if not missing.any():
            break
        j = np.clip(idx + off, 0, np.array(flow.shape[:3]) - 1)
        f[missing] = flow[j[missing, 0], j[missing, 1], j[missing, 2]]
    missing = np.linalg.norm(f, axis=1) < 0.5
    f[missing] = (0, -1, 0)
    out[mask] = f
    return out


def knit_dirs(pos, mask):
    """Ribs of the knit: up the body, along the sleeves (which part is which comes from the sculpt)."""
    lo, dd, voxel, part = MS.get_body_grid()
    d = np.zeros(pos.shape, np.float32)
    d[..., 1] = 1
    idx = np.clip(np.round((pos[mask] - lo) / voxel).astype(int), 0, np.array(part.shape) - 1)
    pid = np.zeros(pos.shape[:2], np.int32)
    pid[mask] = part[idx[:, 0], idx[:, 1], idx[:, 2]].round().astype(int)
    for k, segs in ((1, ((MS.R_SHOULDER, MS.R_ELBOW), (MS.R_ELBOW, MS.R_WRIST))),
                    (2, ((MS.L_SHOULDER, MS.L_ELBOW), (MS.L_ELBOW, MS.L_WRIST)))):
        best = np.full(pos.shape[:2], 1e9, np.float32)
        for a, b in segs:
            ba = b - a
            h = np.clip(((pos - a) @ ba) / (ba @ ba), 0, 1)
            dist = np.linalg.norm(pos - (a + h[..., None] * ba), axis=-1)
            sel = (pid == k) & (dist < best)
            d[sel] = ba / np.linalg.norm(ba)
            best = np.where(sel, dist, best)
    return d


# ---------------------------------------------------------------------------
# the drawing
# ---------------------------------------------------------------------------
def draw(npz_path, out_path, scale=1.0, seed=3, crop=None, px=None):
    Z = np.load(npz_path)
    rgb, depth, normal, mat, pos, glass, cam = (Z['rgb'], Z['depth'], Z['normal'], Z['mat'], Z['pos'],
                                                Z['glass'], Z['cam'])
    H0, W0 = depth.shape
    fy, fx = np.mgrid[0:H0, 0:W0].astype(np.float32)
    fx, fy = fx / W0, fy / H0  # where each pixel sits in the whole frame, 0..1
    if crop is not None:  # a window of the frame, for quick trials (x0, y0, x1, y1)
        x0, y0, x1, y1 = crop
        rgb, depth, normal, mat, pos, glass, fx, fy = (a[y0:y1, x0:x1] for a in
                                                       (rgb, depth, normal, mat, pos, glass, fx, fy))
    H, W = depth.shape
    rng = np.random.default_rng(seed)
    px = W / 2560 if px is None else px  # stroke sizes are designed at 2560 wide

    tone = S.tonemap(rgb, 1.05) @ np.array([0.30, 0.59, 0.11])
    char = np.isin(mat, list(CHAR))
    props = np.isin(mat, list(PROPS))
    subject = char | props
    skin = np.isin(mat, list(CHAR_SKIN))
    hair = mat == MS.HAIR
    knit = mat == MS.KNIT
    eye = mat == MS.EYE
    near_d = np.median(depth[char]) if char.any() else 3.0
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
    T = np.where(hair, 0.10 + 0.90 * np.clip(T, 0, 1) ** 0.6, T)
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
    hf = hair_flow(pos, hair & ok)
    hx, hy = project_dirs(hf, pos, cam, W, H)
    vx = np.where(hair, hx, vx)
    vy = np.where(hair, hy, vy)
    kd = knit_dirs(pos, knit & ok)
    kx, ky = project_dirs(kd, pos, cam, W, H)
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
    bdx, bdy = project_dirs(np.broadcast_to(MS.rot(yaw=-MS.RACK_ANGLE) @ np.array([1.0, 0, 0]), pos.shape), pos, cam, W, H)
    wood = mat == MS.WOOD
    vx = np.where(wood, bdx, vx)
    vy = np.where(wood, bdy, vy)
    blx, bly = project_dirs(np.broadcast_to(MS.BLADE_B, pos.shape), pos, cam, W, H)
    steel = mat == MS.STEEL
    vx = np.where(steel, blx, vx)
    vy = np.where(steel, bly, vy)
    vx = vx.astype(np.float32)
    vy = vy.astype(np.float32)

    # --- strokes
    L = max(4, int(13 * px))
    grain = blur(rng.random((H, W)), 0.7 * px).astype(np.float32)
    s1 = lic(grain, vx, vy, L, region)
    grain2 = blur(rng.random((H, W)), 0.7 * px).astype(np.float32)
    c, s_ = np.cos(np.radians(62)), np.sin(np.radians(62))
    s2 = lic(grain2, (vx * c - vy * s_).astype(np.float32), (vx * s_ + vy * c).astype(np.float32), L, region)
    hl = max(6, int(34 * px))  # long strands in the hair
    grain3 = blur(rng.random((H, W)), 0.5 * px).astype(np.float32)
    s3 = lic(grain3, vx, vy, hl, region)

    def nrm(z):
        return (z - z.mean()) / (z.std() + 1e-9)

    s1, s2, s3 = nrm(s1), nrm(s2), nrm(s3)

    # graphite rubbed smooth for soft gradations; hatching laid over it as tone deepens; cross-hatching in
    # the deepest shadows; long dark strands in the hair
    smudge_amt = np.where(skin, 0.72, np.where(hair, 0.45, np.where(bg, 0.40, 0.55)))
    grain_mod = np.where(skin, 0.97 + 0.03 * s1, 0.85 + 0.15 * s1)  # skin blended smooth with a stump
    smudge = np.clip(np.where(skin, blur(dark, 3.5 * px), blur(dark, 2.2 * px)), 0, 1) ** 1.1 * smudge_amt * \
        np.clip(grain_mod, 0.5, 1.2)
    hatch_start = np.where(skin, 0.50, np.where(bg, 0.34, 0.30))
    m1 = np.clip((dark * 2.2 - 0.95 - s1 * 0.45) * 1.8, 0, 1) * np.clip((dark - hatch_start) * 2.4, 0, 1)
    m1 = m1 * np.where(skin, 0.55, 1.0)  # skin is blended more than hatched
    m2 = np.clip((dark * 2.3 - 1.65 - s2 * 0.45) * 2.0, 0, 1) * (1 - 0.6 * skin) * (1 - 0.75 * knit)
    m2 = m2 * np.clip((dark - 0.40) * 4.0, 0, 1)  # cross-hatching only where it is really dark
    strands = np.clip((dark * 1.9 - 0.55 - s3 * 0.75) * 1.6, 0, 1) * hair
    marks = 1 - (1 - smudge) * (1 - m1 * 0.62) * (1 - m2 * 0.6) * (1 - strands * 0.8)

    # --- outlines from the geometry
    dz = np.maximum.reduce([np.abs(np.roll(depth, s, a) - depth) for s in (1, -1) for a in (0, 1)])
    occl = smoothstep(0.012, 0.05, dz / np.maximum(depth, 1e-3)) * ok
    nd = np.minimum.reduce([(np.roll(normal, s, a) * normal).sum(-1) for s in (1, -1) for a in (0, 1)])
    crease = smoothstep(0.10, 0.45, 1 - nd) * ok
    matedge = np.zeros((H, W), bool)
    for s in (1, -1):
        for a in (0, 1):
            matedge |= np.roll(mat, s, a) != mat
    crease_bg = smoothstep(0.25, 0.6, 1 - nd) * ok  # only the sharper corners in the background
    crease = np.where(subject, crease, crease_bg)
    crease = crease * ~(knit | hair)  # the knit's ribs and the hair's strands come through as tone, not lines
    lines = np.maximum(occl, np.where(skin, 0.25, 0.5) * crease)
    lines = np.maximum(lines, 0.45 * matedge * (subject | np.roll(subject, 1, 0) | np.roll(subject, 1, 1)))
    # the subject drawn with a firmer line; background lines finer and paler
    wt = np.where(subject | np.roll(subject, 2, 1) | np.roll(subject, -2, 1), 0.85, 0.42 * (1 - 0.55 * recede))
    lines = blur(lines, 0.6 * px) * wt
    # pressure varies along the line
    press = 0.75 + 0.35 * nrm(blur(rng.random((H, W)), 6 * px))
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
    tooth = blur(rng.standard_normal((H, W)), 0.6 * px) * 0.022
    paper = 0.968 + tooth
    ink = 1 - (1 - marks * 0.93) * (1 - line_dark * 0.92) * (1 - detail * 0.5)
    ink = ink * (1 - 0.85 * bright)
    ink = np.maximum(ink, glass * 0.55)
    out = paper * (1 - ink)
    # graphite catches the tooth of the paper in the mid-tones
    out = out + tooth * np.where(skin, 0.5, 1.2) * smoothstep(0.1, 0.5, ink) * (1 - smoothstep(0.6, 0.9, ink))
    out = np.clip(out, 0, 1)
    rgbo = np.stack([out, out * 0.988, out * 0.965], -1)
    img = Image.fromarray((rgbo * 255).astype(np.uint8))
    if scale != 1.0:
        img = img.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
    img.save(out_path, optimize=True)
    print('saved', out_path)


if __name__ == '__main__':
    args = sys.argv[1:]
    scale = float(args[args.index('--scale') + 1]) if '--scale' in args else 1.0
    crop = tuple(int(v) for v in args[args.index('--crop') + 1].split(',')) if '--crop' in args else None
    draw(args[0], args[1], scale, crop=crop, px=1.0 if crop else None)
