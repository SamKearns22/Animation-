#!/usr/bin/env python3
"""Humpback whale (Flying Whales, 1 Nov): one model in metres, drawn flat in the house style from ANY view.

Why a model and not drawings: Sam needs the whales from every side (this film's rear three-quarter, side, from below,
front three-quarter, and a prior scene not yet written), at any size from a speck to frame-filling, pitching up and
down, flippers waving and the tail beating (rule 39: seen from three or more angles, so a model). It is drawn like
the Roadster: flat colours (a lit and a shadow tone only), one ink outline round the outside, round every part and
along every colour change (dark back / pale belly, the belly patterns), nothing shiny.

Real size (refs whale-side-*, whale-patterns-below): 14 m long, flippers 4.5 m (a third of the body), flukes 5 m
across; a broad flat head with knobbly bumps (tubercles), throat grooves from chin to navel, a small hump and fin
two thirds back, a thin tail stock, notched flukes with a ragged back edge.

Whale-local axes: x forward (snout at +6.4 m), y to the whale's left, z up; origin mid-body.

    python3 source/whale.py sheet OUT.jpg          every view, the five patterns, a 14 m scale bar (for Sam)
    python3 source/whale.py moves OUT.jpg          flipper wave, tail beat, climb and dive, blow, one row each
    python3 source/whale.py reel OUT.mp4 [--small] a few seconds of a whale flying past, waving and blowing
    python3 source/whale.py check                  the line-work check on each pattern (linecheck.analyse)

Use in a film:
    import whale as W
    cam = W.Cam(pos=(0, -120, 8), yaw=0, pitch=4, focal=1400, size=(1080, 1920))
    pose = W.Pose(pos=(10, -40, 20), yaw=90, pitch=10, roll=0)      # yaw 0 = nose along +y (away from us)
    spr = W.draw(cam, pose, pattern=2, t=1.3, flap=1.0, beat=1.0)    # a Sprite: .img (RGBA), .xy (where to paste)
    frame.alpha_composite(spr.img, spr.xy)                           # (use spr.paste(frame))
    spr.blowhole, spr.bbox, spr.depth                                # for the spray, contact tests and draw order
"""
import functools
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

INK = (20, 16, 16)                                  # the house outline colour (satire_style.OUT)
LENGTH = 14.0                                       # m, snout to fluke tips
BODY_L = 12.8                                       # m, snout to the fluke root
SNOUT_X = 6.4
FLIPPER_L = 4.5
FLUKE_SPAN = 5.0
LIGHT = np.array([0.35, -0.45, 0.82])              # world: from above, a little towards the camera (dusk: film may pass its own)
LIGHT = LIGHT / np.linalg.norm(LIGHT)

# colours: kept above the line check's ink darkness (luma 85) so a dark back never reads as a line
DARK = ((90, 108, 130), (77, 93, 114))              # slate back: lit, shadow
PALE = ((232, 234, 232), (192, 200, 210))           # white belly, flippers, fluke undersides: lit, shadow
GROOVE = {0: (112, 130, 152), 1: (168, 178, 190)}    # throat-groove lines on dark / on pale (thin, paler than ink)
KNOB = (66, 80, 98)                                 # tubercles on the head
BLOW = ((236, 244, 248), (196, 214, 226))           # blow spray: lit, shadow

# ------------------------------------------------- the body shape ---------------------------------------------------
# s = 0 at the snout, 1 at the fluke root. half-width, half-height, centre lift (all m), from the side and top refs.
PROFILE = np.array([
    # s     half-w half-h  lift      ("determined fat torpedoes": a deep chest and belly, a thin tail stock)
    [0.00, 0.10, 0.06, 0.00],
    [0.02, 0.48, 0.30, -0.04],
    [0.06, 0.84, 0.58, -0.12],
    [0.12, 1.22, 0.92, -0.20],
    [0.20, 1.56, 1.26, -0.26],
    [0.30, 1.82, 1.54, -0.26],
    [0.40, 1.88, 1.64, -0.18],
    [0.50, 1.74, 1.58, -0.08],
    [0.60, 1.40, 1.36, 0.02],
    [0.70, 0.96, 1.06, 0.10],
    [0.80, 0.54, 0.72, 0.14],
    [0.88, 0.30, 0.46, 0.14],
    [0.95, 0.20, 0.30, 0.10],
    [1.00, 0.16, 0.22, 0.08],
])


def _prof(s):
    return [np.interp(s, PROFILE[:, 0], PROFILE[:, k]) for k in (1, 2, 3)]


# ---------------------------------------------- the five patterns ---------------------------------------------------
# From ref whale-patterns-below, left to right: 0 nearly all black underneath (white specks on the fluke edge);
# 1 black with a white chest blaze and a white patch by the navel; 2 black with a speckled white throat; 3 white chest
# and belly, dark tail stock; 4 nearly all white (fluke undersides white too). Flippers white underneath on all;
# on top white on 3 and 4, dark with a white leading edge on the others. Each whale also gets its own size (+-6%).
PATTERNS = [
    dict(name='Inky', belly=0.0, chest=0.0, speckle=0.0, fluke_white=0.10, flip_top_white=False, size=1.00, seed=11),
    dict(name='Blaze', belly=0.0, chest=0.55, speckle=0.0, fluke_white=0.55, flip_top_white=False, size=0.95, seed=23),
    dict(name='Freckle', belly=0.0, chest=0.0, speckle=1.0, fluke_white=0.25, flip_top_white=False, size=1.04, seed=37),
    dict(name='Bib', belly=0.75, chest=0.8, speckle=0.0, fluke_white=0.70, flip_top_white=True, size=0.97, seed=41),
    dict(name='Ghost', belly=1.0, chest=1.0, speckle=0.0, fluke_white=0.95, flip_top_white=True, size=1.06, seed=53),
]


@functools.lru_cache(None)
def _lumps(seed, k=5):
    r = np.random.default_rng(seed)
    return r.uniform(0.6, 2.4, k), r.uniform(0, 2 * math.pi, k), r.uniform(0.3, 1.0, k)


def _body_pale(pat, s, phi):
    """> 0 where the body is pale. phi: angle from the belly's midline (0 belly, pi the back). Smooth, so the edge
    between dark and pale is cut cleanly through the mesh, never stair-stepped."""
    fr, fp, fa = _lumps(pat['seed'])
    wob = sum(a * math.sin(f * 2 * math.pi * s * 3 + p) for f, p, a in zip(fr, fp, fa)) / len(fr)
    side = math.sin(phi * 3 + s * 9 + pat['seed'])
    # the belly field: wide where 'belly' is high, narrowing to nothing towards the tail
    tail = np.clip((0.86 - s) / 0.2, 0, 1)
    head = np.clip((s - 0.03) / 0.06, 0, 1)
    reach = (0.25 + 1.25 * pat['belly'] + 0.18 * wob + 0.05 * side) * tail * head
    f = reach - phi
    if pat['belly'] <= 0.0:
        f = -1.0
    # the chest blaze: a pale band across the throat and chest (s 0.12-0.42)
    if pat['chest'] > 0:
        band = max(0.0, 1 - ((s - 0.27) / (0.11 + 0.13 * pat['chest'])) ** 2) ** 0.5      # rounded ends
        if band > 0:
            f = max(f, band * (0.55 + 0.9 * pat['chest'] + 0.08 * wob) - phi)
    # the navel patch (pattern 1): a pale oval low on the belly at s 0.6
    if pat['name'] == 'Blaze':
        g = 1 - math.hypot((s - 0.6) / 0.06, phi / 0.6)
        f = max(f, g)
    # (pattern 2's speckled throat is drawn as pale specks over the skin, in draw(): too fine for the mesh)
    return f


def _fluke_pale(pat, u, v, under):
    """u 0 root -> 1 tip along the span (either side), v 0 leading -> 1 trailing edge. Underside only is patterned."""
    if not under:
        return -1.0
    fw = pat['fluke_white']
    fr, fp, fa = _lumps(pat['seed'] + 5, 6)
    wob = sum(a * math.sin(f * 2 * math.pi * u * 2 + p) for f, p, a in zip(fr, fp, fa)) / len(fr)
    f = fw - 0.5 + 0.35 * (0.6 - abs(u - 0.5)) + 0.25 * wob - 0.25 * (1 - v)
    if fw < 0.2:   # specks along the trailing edge only
        sp = math.sin(u * 61 + pat['seed']) * math.sin(u * 37 + 1.3)
        f = (sp - 0.55) * 2 + (v - 0.8) * 3
    return f


def _flipper_pale(pat, u, v, under):
    """u 0 root -> 1 tip, v 0 leading -> 1 trailing edge."""
    if under or pat['flip_top_white']:
        return 1.0 - 1.4 * max(0.0, 0.18 - u) / 0.18 if under else 1.0
    # dark on top with a white leading edge that widens towards the tip
    return (0.18 + 0.35 * u) - v


# ------------------------------------------------- posing -----------------------------------------------------------
def _rot(axis, a):
    c, s = math.cos(a), math.sin(a)
    if axis == 'x':
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == 'y':
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


class Pose:
    """Where the whale is in the world (m; x right, y away from a camera at yaw 0, z up) and which way it points.
    yaw: degrees, 0 = nose along +y, 90 = nose along -x (to screen left for a camera looking along +y), 180 = nose
    at a camera looking along +y. pitch: nose up, degrees. roll: banking, degrees (positive = left flipper up)."""
    def __init__(self, pos=(0, 0, 0), yaw=0.0, pitch=0.0, roll=0.0):
        self.pos = np.asarray(pos, float)
        # whale-local x (forward) to world: first point the nose along +y, then turn, pitch, roll
        base = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], float)   # local x -> world +y, local y -> world -x
        self.R = _rot('z', math.radians(yaw)) @ base @ _rot('y', -math.radians(pitch)) @ _rot('x', math.radians(roll))

    def world(self, P):
        return np.asarray(P, float) @ self.R.T + self.pos


class Cam:
    """A pinhole camera: pos (m), yaw (degrees; 0 looks along +y, 90 along -x), pitch (degrees, up), focal in px,
    size the frame (w, h). The film's own camera: give the same one to every whale and the rig."""
    def __init__(self, pos=(0, -30, 0), yaw=0.0, pitch=0.0, focal=1400.0, size=(1080, 1920), roll=0.0):
        self.pos = np.asarray(pos, float)
        self.size = size
        self.focal = focal
        # world -> camera: camera x right, y forward (depth), z up
        self.R = (_rot('y', math.radians(roll)) @ _rot('x', -math.radians(pitch)) @ _rot('z', -math.radians(yaw)))

    def cam(self, P):
        return (np.asarray(P, float) - self.pos) @ self.R.T

    def screen(self, P):
        q = self.cam(P)
        d = np.maximum(q[..., 1], 0.05)
        x = self.size[0] / 2 + self.focal * q[..., 0] / d
        y = self.size[1] / 2 - self.focal * q[..., 2] / d
        return np.stack([x, y], -1), q[..., 1]

    @staticmethod
    def basis(pos, right, fwd, focal=1400.0, size=(1080, 1920)):
        """A camera at pos looking along fwd with right as the screen's right (up = right x fwd)."""
        f = np.asarray(fwd, float) / np.linalg.norm(fwd)
        r = np.asarray(right, float)
        r = r - f * np.dot(r, f)
        r /= np.linalg.norm(r)
        c = Cam(pos, 0, 0, focal, size)
        c.R = np.stack([r, f, np.cross(r, f)])
        return c

    @staticmethod
    def looking_at(target, frm, focal=1400.0, size=(1080, 1920)):
        t, f = np.asarray(target, float), np.asarray(frm, float)
        d = t - f
        yaw = math.degrees(math.atan2(-d[0], d[1]))
        pitch = math.degrees(math.atan2(d[2], math.hypot(d[0], d[1])))
        return Cam(f, yaw, pitch, focal, size)


# ------------------------------------------------- the model --------------------------------------------------------
NS, NA = 56, 40            # body sections, points round each section


def _spine(sz, t, beat, arch):
    """The backbone: points, tangents and up-vectors along s in whale-local metres, bent by the tail beat (an up-down
    wave running back down the body, mostly in the tail third) and an arch (nose and tail both down, + = arched up)."""
    s = np.linspace(0, 1, NS)
    x = (SNOUT_X - s * BODY_L) * sz
    amp = 0.95 * beat * sz * np.clip((s - 0.45) / 0.55, 0, 1) ** 2
    z = amp * np.sin(2 * math.pi * (t * 0.55) - 2.4 * s) - arch * sz * 1.6 * (2 * s - 1) ** 2
    pts = np.stack([x, np.zeros_like(x), z], 1)
    tan = np.gradient(pts, axis=0)
    tan /= np.linalg.norm(tan, axis=1, keepdims=True)
    tan = -tan                                           # point forward (towards the snout)
    up = np.stack([-tan[:, 2], np.zeros_like(x), tan[:, 0]], 1)
    return s, pts, tan, up


def _body(sz, t, beat, arch, pat):
    s, pts, tan, up = _spine(sz, t, beat, arch)
    a = np.linspace(0, 2 * math.pi, NA, endpoint=False)          # 0 = the back, pi = the belly
    left = np.array([0, 1.0, 0])
    V = np.zeros((NS, NA, 3))
    F = np.zeros((NS, NA))
    for i, si in enumerate(s):
        hw, hh, lift = _prof(si)
        hw, hh, lift = hw * sz, hh * sz, lift * sz
        cz = np.cos(a)
        sy = np.sin(a)
        belly = cz < 0
        zz = np.where(belly, cz * hh * 1.08, cz * hh * (0.92 if si < 0.25 else 1.0))   # flatter head top, full belly
        yy = sy * hw * np.where(belly, 0.98, 1.0)
        V[i] = pts[i] + up[i] * (zz + lift)[:, None] + left * yy[:, None]
        phi = np.array([abs(((ai + math.pi) % (2 * math.pi)) - math.pi) for ai in a])  # distance from the back
        phi = math.pi - phi
        F[i] = [_body_pale(pat, si, p) for p in phi]
    # close the skin along the back: repeat the first ring point at the end (no seam, no gap down the spine)
    V = np.concatenate([V, V[:, :1]], 1)
    F = np.concatenate([F, F[:, :1]], 1)
    return V, F, (s, pts, tan, up)


def _plate(root, axis_u, axis_v, normal, outline_fn, nu, nv, thick):
    """A thin plate (flipper, fluke): outline_fn(u) -> (v0, v1) chord from leading to trailing edge in metres along
    axis_v at span u*length along axis_u. Returns top and bottom grids (nu x nv x 3) and (u, v) params."""
    U = np.linspace(0, 1, nu)
    Vp = np.linspace(0, 1, nv)
    top = np.zeros((nu, nv, 3))
    bot = np.zeros((nu, nv, 3))
    for i, u in enumerate(U):
        span, v0, v1, th = outline_fn(u)
        for j, v in enumerate(Vp):
            p = root + axis_u * span + axis_v * (v0 + (v1 - v0) * v)
            k = thick * th * math.sin(math.pi * min(1, max(0, v))) ** 0.5
            top[i, j] = p + normal * k
            bot[i, j] = p - normal * k
    return top, bot, U, Vp


def _flipper(side, sz, spine, flap, t, phase):
    """side +1 = left. Root low on the flank a third back; swept back, waving up and down (flap 0..1)."""
    s, pts, tan, up = spine
    i = int(0.30 * (NS - 1))
    hw, hh, lift = _prof(0.30)
    root = pts[i] + up[i] * (lift - 0.45 * hh) * sz + np.array([0, side * hw * 0.82 * sz, 0])
    wave = math.radians(-18 + 26 * flap * math.sin(2 * math.pi * 0.45 * t + phase))   # dihedral: + = tip up
    sweep = math.radians(38)
    out = np.array([0, side * 1.0, 0])
    span_dir = math.cos(sweep) * out - math.sin(sweep) * tan[i]
    span_dir = span_dir * math.cos(wave) + up[i] * math.sin(wave)
    span_dir /= np.linalg.norm(span_dir)
    chord_dir = -tan[i]
    normal = np.cross(span_dir, chord_dir) * side
    normal /= np.linalg.norm(normal)
    L = FLIPPER_L * sz

    def outline(u):
        # long and narrow; scalloped leading edge (the knobs), chord 1.1 m at the root to 0.25 m at the tip
        chord = (1.45 + 0.25 * math.sin(u * math.pi * 0.8) - 1.25 * u ** 1.6) * sz
        scal = 0.07 * sz * max(0, math.sin(u * math.pi * 9)) * (u > 0.15)
        bend = 0.25 * sz * math.sin(u * math.pi) - 0.35 * sz * u ** 2     # gently curved back
        v0 = -chord * 0.35 + bend - scal
        v1 = chord * 0.65 + bend
        if u > 0.93:
            k = (u - 0.93) / 0.07
            mid = (v0 + v1) / 2
            v0, v1 = mid + (v0 - mid) * (1 - k * 0.9), mid + (v1 - mid) * (1 - k * 0.9)
        return u * L, v0, v1, (1 - 0.7 * u)
    return _plate(root, span_dir, chord_dir, normal, outline, 22, 7, 0.16 * sz)


def _flukes(side, sz, spine):
    s, pts, tan, up = spine
    root = pts[-1] + up[-1] * _prof(1.0)[2] * sz
    back = -tan[-1]
    out = np.array([0, side * 1.0, 0])
    normal = up[-1]
    half = FLUKE_SPAN / 2 * sz

    def outline(u):
        # leading edge swept back; tips pointed; trailing edge S-curved and ragged; notch in the middle
        sweep = 0.55 * sz * u ** 1.4 + 0.25 * sz * u
        chord = (1.25 - 1.1 * u ** 1.8) * sz
        rag = 0.05 * sz * math.sin(u * 47 + side) * (0.2 < u < 0.95)
        notch = -0.28 * sz * max(0, 1 - u / 0.12)
        v0 = sweep - 0.15 * sz
        v1 = sweep + chord + rag + notch - 0.25 * sz * math.sin(u * math.pi) * 0.6
        v1 = max(v1, v0 + 0.06 * sz)
        return u * half, v0, v1, (1 - 0.8 * u)
    return _plate(root, out, back, normal, outline, 18, 6, 0.12 * sz)


def _fin(sz, spine):
    """The small dorsal fin on its hump, two thirds back: a little swept wedge (four faces), so from behind it shows
    as a small filled triangle, not a line."""
    s, pts, tan, up = spine

    def at(si, h, side=0.0, back=0.0):
        i = int(si * (NS - 1))
        hw, hh, lift = _prof(si)
        return pts[i] + up[i] * (lift + hh - 0.04 + h) * sz - tan[i] * back * sz + np.array([0, side * sz, 0])
    front, rear = at(0.585, 0.0), at(0.705, 0.0)
    tip = at(0.672, 0.40, back=0.22)                     # small and stubby, swept back (not a shark's fin)
    ml, mr = at(0.65, 0.0, 0.13), at(0.65, 0.0, -0.13)
    return [[front, ml, tip], [ml, rear, tip], [front, tip, mr], [mr, tip, rear]]


# ------------------------------------------------- drawing ----------------------------------------------------------
class Sprite:
    def __init__(self, img, xy, blowhole, bbox, depth, outline):
        self.img, self.xy, self.blowhole, self.bbox, self.depth = img, xy, blowhole, bbox, depth
        self.outline = outline            # screen polygon points of the silhouette (rough), for contact tests

    def paste(self, frame):
        frame.alpha_composite(self.img, (int(self.xy[0]), int(self.xy[1])))


def _clip(poly, vals):
    """Sutherland-Hodgman: keep the part of a polygon where a linear field >= 0 (and the part where it is < 0).
    poly: list of (attributes array); vals: field per vertex."""
    pos, neg = [], []
    n = len(poly)
    for k in range(n):
        a, b = poly[k], poly[(k + 1) % n]
        fa, fb = vals[k], vals[(k + 1) % n]
        (pos if fa >= 0 else neg).append(a)
        if (fa >= 0) != (fb >= 0):
            m = a + (b - a) * (fa / (fa - fb))
            pos.append(m)
            neg.append(m)
    return pos, neg


def _faces(grid, field, lit, uvs, flip=False):
    """Triangles of a grid split cleanly along the pale/dark field and the lit/shadow field.
    Yields (3D points, pale?, lit?)."""
    nu, nv = grid.shape[:2]
    for i in range(nu - 1):
        for j in range(nv - 1):
            quad = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
            if flip:
                quad = quad[::-1]
            for tri in ((quad[0], quad[1], quad[2]), (quad[0], quad[2], quad[3])):
                P = [np.concatenate([grid[a], [field[a], lit[a]]]) for a in tri]
                f = [p[3] for p in P]
                for part, pale in zip(_clip(P, f), (True, False)):
                    if len(part) < 3:
                        continue
                    g = [p[4] for p in part]
                    for piece, is_lit in zip(_clip(part, g), (True, False)):
                        if len(piece) >= 3:
                            yield np.array([p[:3] for p in piece]), pale, is_lit


def _normals(grid, outward_ref=None):
    du = np.gradient(grid, axis=0)
    dv = np.gradient(grid, axis=1)
    n = np.cross(du, dv)
    n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9
    return n


def draw(cam, pose, pattern=0, t=0.0, flap=1.0, beat=1.0, arch=0.0, mouth=0.0, light=None, ol=None, ss=2,
         blow=None, tint=None, phase=0.0):
    """Draw one whale. pattern 0-4 (PATTERNS) sets the markings and size. t seconds (drives the wave and beat);
    flap 0..1 how much the flippers wave; beat 0..1 how much the tail beats; arch -1..1 (+ nose and tail down: a
    hump, - a dip). blow: seconds since the last blow (None = no spray). ol: outline width in px (default: the house
    5 px at a 1080-wide frame). tint: (r, g, b, k) mixes the dusk light into every colour. Returns a Sprite."""
    pat = PATTERNS[pattern] if isinstance(pattern, int) else pattern
    sz = pat['size']
    L = (np.asarray(light, float) if light is not None else LIGHT)
    L = L / np.linalg.norm(L)
    W, H = cam.size
    ol = ol if ol is not None else max(2.0, 5.0 * W / 1080)

    Vb, Fb, spine = _body(sz, t, beat, arch, pat)
    parts = []                                         # (name, grid, pale field, uv flip)
    parts.append(('body', Vb, Fb, True))           # (its grid winds inwards)
    for side in (1, -1):
        top, bot, U, Vp = _flipper(side, sz, spine, flap, t, phase + (0 if side > 0 else 0.4))
        ft = np.array([[_flipper_pale(pat, u, v, False) for v in Vp] for u in U])
        fb = np.array([[_flipper_pale(pat, u, v, True) for v in Vp] for u in U])
        parts.append((f'flipper{side}', top, ft, side < 0))
        parts.append((f'flipper{side}', bot, fb, side > 0))
    for side in (1, -1):
        top, bot, U, Vp = _flukes(side, sz, spine)
        ft = np.full((len(U), len(Vp)), -1.0)
        fb = np.array([[_fluke_pale(pat, u, v, True) for v in Vp] for u in U])
        parts.append((f'fluke{side}', top, ft, side < 0))
        parts.append((f'fluke{side}', bot, fb, side > 0))

    # to world and camera
    campos = cam.pos
    polys = []                                         # (depth, screen pts, colour, id)
    pid = {}
    for name, grid, field, flip in parts:
        Wg = pose.world(grid.reshape(-1, 3)).reshape(grid.shape)
        n = _normals(Wg)
        if flip:
            n = -n
        lit = (n @ L) - 0.05
        if name == 'body':
            # body normals: make sure they point outwards (away from the spine)
            pass
        part_id = pid.setdefault(name, len(pid) + 1)
        for tri, pale, is_lit in _faces(Wg, field, lit, None, flip):
            c = tri.mean(0)
            nn = np.cross(tri[1] - tri[0], tri[2] - tri[0])
            if np.linalg.norm(nn) < 1e-12:
                continue
            facing = np.dot(nn, c - campos) < 0
            if not facing:
                continue
            P, d = cam.screen(tri)
            if (d < 0.3).any():
                continue
            col = (PALE if pale else DARK)[0 if is_lit else 1]
            polys.append((float(np.linalg.norm(c - campos)), P, col, part_id * 2 + (1 if pale else 0)))
    fin_id = pid.setdefault('fin', len(pid) + 1)
    for tri in _fin(sz, spine):
        tri = pose.world(np.array(tri))
        P, d = cam.screen(tri)
        if (d < 0.3).any():
            continue
        nf = np.cross(tri[1] - tri[0], tri[2] - tri[0])
        nf = nf / (np.linalg.norm(nf) + 1e-9)
        if np.dot(nf, tri.mean(0) - pose.world(np.array(_fin(sz, spine))).reshape(-1, 3).mean(0)) < 0:
            nf = -nf                                    # point it out of the wedge
        if np.dot(nf, tri.mean(0) - campos) > 0:
            continue                                    # its far faces are hidden
        litf = np.dot(nf, L)
        polys.append((float(np.linalg.norm(tri.mean(0) - campos)) - 0.05, P, DARK[0 if abs(litf) > 0.25 else 1],
                      fin_id * 2))
    if not polys:
        return None
    allp = np.concatenate([p[1] for p in polys])
    x0, y0 = np.floor(allp.min(0)) - 4 * ol - 4
    x1, y1 = np.ceil(allp.max(0)) + 4 * ol + 4
    x0, y0 = max(x0, -W), max(y0, -H)
    x1, y1 = min(x1, 2 * W), min(y1, 2 * H)
    bw, bh = int(x1 - x0), int(y1 - y0)
    if bw < 2 or bh < 2:
        return None
    S = ss
    col = Image.new('RGB', (bw * S, bh * S), (0, 0, 0))
    ids = Image.new('L', (bw * S, bh * S), 0)
    dep = Image.new('I', (bw * S, bh * S), 0)
    dc, di, dd = ImageDraw.Draw(col), ImageDraw.Draw(ids), ImageDraw.Draw(dep)
    for depth, P, c, i in sorted(polys, key=lambda p: -p[0]):
        Q = [((x - x0) * S, (y - y0) * S) for x, y in P]
        dc.polygon(Q, fill=c, outline=c)
        di.polygon(Q, fill=i + 1, outline=i + 1)
        dd.polygon(Q, fill=int(depth * 100), outline=int(depth * 100))

    # details on the body, drawn where they can be seen (depth test against what was drawn)
    D = np.asarray(dep, np.int64)
    idarr = np.asarray(ids)

    def seen(p3):
        P, d = cam.screen(p3)
        x, y = int((P[0] - x0) * S), int((P[1] - y0) * S)
        if not (0 <= x < bw * S and 0 <= y < bh * S):
            return None
        dist = float(np.linalg.norm(p3 - campos)) * 100
        if idarr[y, x] in (3, 4) and abs(D[y, x] - dist) < 35 * sz + 4:
            return (x, y)
        return None

    s_, pts, tan, up = spine
    left = np.array([0, 1.0, 0])

    def surf(si, a, lift_out=0.0):
        """A point on the body at s, angle a (0 back, pi belly, + towards the left)."""
        hw, hh, lift = _prof(si)
        i = si * (NS - 1)
        i0 = int(min(NS - 2, i))
        k = i - i0
        p = pts[i0] * (1 - k) + pts[i0 + 1] * k
        u = up[i0] * (1 - k) + up[i0 + 1] * k
        cz, sy = math.cos(a), math.sin(a)
        zz = cz * hh * (1.08 if cz < 0 else (0.92 if si < 0.25 else 1.0)) * sz
        yy = sy * hw * sz * (0.98 if cz < 0 else 1.0)
        q = p + u * (zz + lift * sz) + left * yy
        return pose.world(q + (q - p) * lift_out)

    lw = max(1, int(ol * S * 0.45))
    # throat grooves: lines from the chin back to the navel, under the head
    for g in np.linspace(-1.05, 1.05, 13):
        run = []
        for si in np.linspace(0.05, 0.48 - 0.08 * abs(g), 18):
            a = math.pi + g * (0.85 + 0.6 * si)
            q = seen(surf(si, a, 0.01))
            pale = _body_pale(pat, si, abs(g * (0.85 + 0.6 * si))) > 0
            if q is None:
                if len(run) > 1:
                    dc.line(run, fill=GROOVE[1 if pale else 0], width=lw)
                run = []
                continue
            run.append(q)
            last_pale = pale
        if len(run) > 1:
            dc.line(run, fill=GROOVE[1 if last_pale else 0], width=lw)
    # the mouth line: from the snout back and down to under the eye (one ink line on each side)
    for side in (1, -1):
        run = []
        for si in np.linspace(0.015, 0.21, 16):
            a = side * (math.pi * (0.56 + 0.12 * (si / 0.21) ** 1.5))
            q = seen(surf(si, a, 0.01))
            if q is None:
                if len(run) > 1:
                    dc.line(run, fill=INK, width=max(1, int(round(ol * S))), joint='curve')
                run = []
                continue
            run.append(q)
        if len(run) > 1:
            dc.line(run, fill=INK, width=max(1, int(round(ol * S))), joint='curve')
        # the eye: a small dark oval just above the end of the mouth
        q = seen(surf(0.225, side * math.pi * 0.58, 0.01))
        if q:
            r = max(1.5, 0.11 * sz * cam.focal / max(1, np.linalg.norm(surf(0.225, side * 1.8) - campos)) * S)
            dc.ellipse([q[0] - r, q[1] - r * 0.7, q[0] + r, q[1] + r * 0.7], fill=INK)
    # tubercles: rows of knobs along the top of the head and the jaw tip
    rng = np.random.default_rng(pat['seed'])
    knobs = [(si, a) for si in np.linspace(0.02, 0.17, 7) for a in (-0.35, -0.12, 0.12, 0.35)]
    knobs += [(si, side * math.pi * 0.62) for si in np.linspace(0.02, 0.12, 4) for side in (1, -1)]
    for si, a in knobs:
        si += rng.uniform(-0.006, 0.006)
        a += rng.uniform(-0.05, 0.05)
        p3 = surf(si, a, 0.0)
        q = seen(p3)
        if q:
            r = max(1.0, 0.06 * sz * cam.focal / max(1, np.linalg.norm(p3 - campos)) * S)
            dc.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=KNOB)
    # freckles (pattern 2, ref whale-patterns-below): pale specks over the throat and chest
    if pat.get('speckle', 0) > 0:
        for k in range(int(140 * pat['speckle'])):
            si = rng.uniform(0.05, 0.46)
            a = math.pi + rng.normal(0, 0.55) * (1.2 - si)
            p3 = surf(si, a, 0.0)
            q = seen(p3)
            if q:
                r = max(1.0, rng.uniform(0.05, 0.11) * sz * cam.focal / max(1, np.linalg.norm(p3 - campos)) * S)
                dc.ellipse([q[0] - r, q[1] - r * 0.6, q[0] + r, q[1] + r * 0.6], fill=PALE[0])
    # blowhole: a short pale-edged slit on top of the head (two strokes)
    bh_p = surf(0.205, 0.0, 0.02)
    q = seen(bh_p)
    if q:
        r = max(1.5, 0.22 * sz * cam.focal / max(1, np.linalg.norm(bh_p - campos)) * S)
        dc.line([(q[0] - r * 0.4, q[1] - r * 0.15), (q[0] + r * 0.4, q[1] + r * 0.15)], fill=GROOVE[0], width=lw)

    # the ink: the silhouette, every change of part or colour, and every fold where one part passes in front of
    # another (a jump in depth), all at one weight
    alpha = np.asarray(ids) > 0
    I = np.asarray(ids).astype(np.int32)
    edge = np.zeros_like(alpha)
    jump = 120 * sz
    for dy, dx in ((0, 1), (1, 0)):
        a1 = I[:I.shape[0] - dy, :I.shape[1] - dx]
        a2 = I[dy:, dx:]
        d1 = D[:D.shape[0] - dy, :D.shape[1] - dx]
        d2 = D[dy:, dx:]
        e = (a1 != a2) | ((np.abs(d1 - d2) > jump) & (a1 > 0) & (a2 > 0))
        edge[:I.shape[0] - dy, :I.shape[1] - dx] |= e
    edge_img = Image.fromarray((edge * 255).astype(np.uint8))
    k = max(3, int(round(ol * S)) | 1)
    edge_img = edge_img.filter(ImageFilter.MaxFilter(k if k % 2 else k + 1))
    ink = np.asarray(edge_img) > 0
    full_alpha = alpha | ink
    out = np.asarray(col).copy()
    out[ink] = INK
    if tint is not None:
        tr, tg, tb, tk = tint
        m = full_alpha & ~ink
        out[m] = (out[m] * (1 - tk) + np.array([tr, tg, tb]) * tk).astype(np.uint8)
    rgba = np.dstack([out, (full_alpha * 255).astype(np.uint8)])
    img = Image.fromarray(rgba, 'RGBA')
    # depth in metres per pixel (inf where empty; an ink line takes the nearest depth beside it), so a film can lay
    # the whale in among other things pixel by pixel (flying_whales_rig.composite)
    from scipy import ndimage as _ND
    Dm = np.where(alpha, D / 100.0, np.inf)
    Dm = np.where(ink, _ND.minimum_filter(Dm, size=k if k % 2 else k + 1), Dm)
    if S != 1:
        img = img.resize((bw, bh), Image.LANCZOS)
        Dm = Dm[:bh * S, :bw * S].reshape(bh, S, bw, S).min(axis=(1, 3))

    blow_xy = cam.screen(surf(0.205, 0.0, 0.02))[0]
    bb = img.getbbox()
    bbox = (bb[0] + x0, bb[1] + y0, bb[2] + x0, bb[3] + y0) if bb else None
    spr = Sprite(img, (x0, y0), tuple(blow_xy), bbox, float(np.linalg.norm(pose.pos - campos)), None)
    spr.depth_map = Dm.astype(np.float32)
    if blow is not None:
        _blow(spr, cam, pose, surf(0.205, 0.0, 0.02), blow, sz, ol)
    return spr


def _blow(spr, cam, pose, top, age, sz, ol):
    """The blow: a bushy column of spray shot up and a little forward from the blowhole, lumpy, flat white with a
    shadow side, one outline round the whole cloud. age seconds since it fired; over in about 1.6 s (it bursts up
    over 0.35 s, then drifts back as the whale flies on and breaks into a few drops)."""
    if age < 0 or age > 1.6:
        return
    up = pose.R @ np.array([0.25, 0, 1.0])
    up /= np.linalg.norm(up)
    back = pose.R @ np.array([-1.0, 0, 0])
    h = 3.4 * sz * min(1.0, age / 0.35) ** 0.6
    drift = back * max(0, age - 0.35) * 2.2 * sz
    rng = np.random.default_rng(int(sz * 1000))
    blobs = []
    n = 9
    for k in range(n):
        f = (k + 1) / n
        c = top + up * h * f + drift * f ** 0.5
        r = (0.25 + 0.75 * f ** 0.8) * sz * (1.0 - 0.5 * max(0, age - 1.0))
        c = c + pose.R @ np.array([rng.uniform(-0.3, 0.3), rng.uniform(-0.4, 0.4), 0]) * f
        blobs.append((c, r * rng.uniform(0.8, 1.15)))
    if age > 1.0:
        blobs = blobs[int((age - 1.0) / 0.6 * n):]
    pts = []
    for c, r in blobs:
        P, d = cam.screen(c)
        if d < 0.5:
            continue
        pts.append((P[0], P[1], r * cam.focal / d))
    if not pts:
        return
    x0, y0 = spr.xy
    pad = 40
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    rs = [p[2] for p in pts]
    bx0 = int(min(min(xs) - max(rs), x0) - pad)
    by0 = int(min(min(ys) - max(rs), y0) - pad)
    bx1 = int(max(max(xs) + max(rs), x0 + spr.img.width) + pad)
    by1 = int(max(max(ys) + max(rs), y0 + spr.img.height) + pad)
    canvas = Image.new('RGBA', (bx1 - bx0, by1 - by0), (0, 0, 0, 0))
    canvas.alpha_composite(spr.img, (int(x0 - bx0), int(y0 - by0)))
    lay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    w = max(2, int(ol))
    for x, y, r in pts:
        d.ellipse([x - bx0 - r - w, y - by0 - r - w, x - bx0 + r + w, y - by0 + r + w], fill=INK + (255,))
    for x, y, r in pts:
        d.ellipse([x - bx0 - r, y - by0 - r, x - bx0 + r, y - by0 + r], fill=BLOW[1] + (255,))
    for x, y, r in pts:                                   # the lit side: each puff nudged up-left
        d.ellipse([x - bx0 - r * 0.85 - r * 0.15, y - by0 - r * 0.85 - r * 0.18,
                   x - bx0 + r * 0.85 - r * 0.15, y - by0 + r * 0.85 - r * 0.18], fill=BLOW[0] + (255,))
    canvas.alpha_composite(lay)
    dm = getattr(spr, 'depth_map', None)
    if dm is not None:                                    # the spray sits at the blowhole's depth
        big = np.full((canvas.height, canvas.width), np.inf, np.float32)
        ox, oy = int(x0 - bx0), int(y0 - by0)
        big[oy:oy + dm.shape[0], ox:ox + dm.shape[1]] = dm
        sp = np.asarray(lay)[..., 3] > 0
        big[sp] = np.minimum(big[sp], float(np.linalg.norm(top - cam.pos)) - 1.0)
        spr.depth_map = big
    spr.img = canvas
    spr.xy = (bx0, by0)


# ------------------------------------------------- sheets -----------------------------------------------------------
SANS = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')


def _font(n):
    try:
        return ImageFont.truetype(SANS, n)
    except OSError:
        return ImageFont.load_default()


# the named views (camera placed around a whale at the origin): (label, camera position, focal scale)
VIEWS = [
    ('side (from its left)', (0.0, 30.0, 0.0)),
    ('rear three-quarter, from behind and above', (-26.0, 11.0, 13.0)),
    ('from below', (0.0, 0.0, -30.0)),
    ('front three-quarter', (22.0, 18.0, 4.0)),
    ('from above', (0.0, 0.0, 30.0)),
    ('head on', (30.0, 0.0, 2.0)),
]


def view_cam(eye, size, fit=15.5, right=None):
    """A camera at eye (whale-local offsets, m, for a whale at Pose()) looking at its middle, framed so about fit m
    fill the frame's width. Straight above or below, the nose points to the screen's right unless right is given."""
    eye = np.asarray(eye, float)
    dist = np.linalg.norm(eye)
    focal = size[0] * dist / fit
    world_eye = np.array([-eye[1], eye[0], eye[2]])        # Pose(): local x -> world +y, local y -> world -x
    if math.hypot(eye[0], eye[1]) < 1e-2:
        return Cam.basis(world_eye, right if right is not None else (0, 1, 0), -world_eye, focal, size)
    return Cam.looking_at((0, 0, 0), world_eye, focal, size)


def _tile(label, img, w, h, bg):
    t = Image.new('RGB', (w, h), bg)
    if img is not None:
        im = img.copy()
        im.thumbnail((w - 20, h - 50))
        t.paste(im, ((w - im.width) // 2, 40 + (h - 50 - im.height) // 2), im)
    ImageDraw.Draw(t).text((12, 8), label, fill=(30, 30, 30), font=_font(22))
    return t


def _render_view(eye, pattern, size=(900, 600), **kw):
    cam = view_cam(eye, size)
    spr = draw(cam, Pose(), pattern=pattern, ol=5, **kw)
    frame = Image.new('RGBA', size, (0, 0, 0, 0))
    if spr:
        spr.paste(frame)
    return frame


def picture(t=0.0):
    """One whale from the rear three-quarter on the dusk mauve (for catalogue.py)."""
    bg = Image.new('RGBA', (900, 600), (214, 200, 214, 255))
    bg.alpha_composite(_render_view(VIEWS[1][1], 1, (900, 600), t=t, flap=1.0, beat=1.0))
    return bg


def sheet(out):
    BG = (214, 200, 214)                                   # a dusk mauve, so the pale belly and the outline both read
    tw, th = 900, 560
    rows = []
    # row 1-2: every view of one whale (pattern 1, the blaze, shows the most)
    tiles = []
    for label, eye in VIEWS:
        tiles.append(_tile(label, _render_view(eye, 1, (tw, th - 40), t=0.3, flap=0.0, beat=0.0), tw, th, BG))
    rows.append(tiles[:3])
    rows.append(tiles[3:])
    # row 3: the five patterns from below (ref whale-patterns-below), each its own size
    pt = []
    for k, p in enumerate(PATTERNS):
        cam = view_cam((0.0, 0.0, -34.0), (540, 900), fit=17, right=(-1, 0, 0))   # nose up the tile
        spr = draw(cam, Pose(), pattern=k, ol=5, flap=0.0, beat=0.0)
        fr = Image.new('RGBA', (540, 900), (0, 0, 0, 0))
        spr.paste(fr)
        pt.append(_tile(f"{k + 1}. {p['name']} (x{p['size']:.2f})", fr, 540, 960, BG))
    # row 4: the five from the rear three-quarter, as they will fly at the rig
    pr = []
    for k, p in enumerate(PATTERNS):
        fr = _render_view((-26.0, 11.0, 13.0), k, (540, 420), t=0.8 + k * 0.4, flap=1.0, beat=1.0)
        pr.append(_tile(f"{k + 1}. {p['name']} from behind", fr, 540, 460, BG))
    # scale bar row: the side view with a 14 m bar and a 1.75 m person for size
    sw, sh = 2700, 760
    sc = Image.new('RGB', (sw, sh), BG)
    cam = view_cam((0.0, 80.0, 0.0), (sw, sh - 120), fit=22.0)
    spr = draw(cam, Pose(), pattern=0, ol=5, flap=0.0, beat=0.0)
    lay = Image.new('RGBA', (sw, sh - 120), (0, 0, 0, 0))
    spr.paste(lay)
    sc.paste(lay, (0, 40), lay)
    px_m = cam.focal / 80.0
    d = ImageDraw.Draw(sc)
    bx0 = sw / 2 - 7.0 * px_m
    y = sh - 80
    for m in range(14):                                   # one block per metre, black and white in turn
        x = bx0 + m * px_m
        d.rectangle([x, y, x + px_m, y + 16], fill=INK if m % 2 == 0 else (245, 245, 245), outline=INK, width=2)
    d.text((bx0 - 8, y + 24), '0', fill=INK, font=_font(24))
    d.text((bx0 + 7 * px_m - 20, y + 24), '7 m', fill=INK, font=_font(24))
    d.text((bx0 + 14 * px_m - 30, y + 24), '14 m', fill=INK, font=_font(24))
    # a person for scale, 1.75 m, standing just left of the bar
    pxh = 1.75 * px_m
    px = bx0 - 90
    d.rectangle([px - 0.22 * px_m, y + 16 - pxh + 0.3 * px_m, px + 0.22 * px_m, y + 16], fill=(80, 90, 120), outline=INK, width=3)
    d.ellipse([px - 0.13 * px_m, y + 16 - pxh, px + 0.13 * px_m, y + 16 - pxh + 0.3 * px_m], fill=(200, 160, 130), outline=INK, width=3)
    d.text((px - 90, y + 24), 'person 1.75 m', fill=INK, font=_font(20))
    d.text((12, 8), 'real size: 14 m long, flippers 4.5 m, flukes 5 m across (pattern 1, Inky, at x1.00)',
           fill=(30, 30, 30), font=_font(26))

    W_ = 2700
    def strip(tiles, h):
        im = Image.new('RGB', (W_, h), BG)
        x = 0
        for t in tiles:
            im.paste(t, (x, 0))
            x += t.width
        return im
    parts = [strip(rows[0], th), strip(rows[1], th), strip(pt, 960), strip(pr, 460), sc]
    tot = sum(p.height for p in parts) + 90
    im = Image.new('RGB', (W_, tot), (250, 250, 250))
    d = ImageDraw.Draw(im)
    d.text((16, 20), 'FLYING WHALES: the humpback, every view (pattern 2 "Blaze"), the five patterns, real size',
           fill=INK, font=_font(36))
    y = 90
    for p in parts:
        im.paste(p, (0, y))
        y += p.height
    im.save(out, quality=88)
    return out


def moves(out):
    BG = (214, 200, 214)
    tw, th = 540, 400
    rows = []
    eye = (-26.0, 11.0, 13.0)
    labels = []
    r1 = [_tile(f'flipper wave t={t:.1f}s', _render_view(eye, 3, (tw, th - 40), t=t, flap=1.0, beat=0.0), tw, th, BG)
          for t in (0.0, 0.55, 1.1, 1.65, 2.2)]
    side = (0.0, 30.0, 0.0)
    r2 = [_tile(f'tail beat t={t:.1f}s', _render_view(side, 3, (tw, th - 40), t=t, flap=0.0, beat=1.0), tw, th, BG)
          for t in (0.0, 0.45, 0.9, 1.35, 1.8)]
    r3 = []
    for label, pitch, arch in (('climb 25', 25, -0.25), ('level', 0, 0.0), ('dive -25', -25, 0.25),
                               ('steep climb 45', 45, -0.15), ('arched', 0, 0.4)):
        cam = view_cam(side, (tw, th - 40), fit=18)
        spr = draw(cam, Pose(pitch=pitch), pattern=3, ol=5, flap=0.3, beat=0.3, arch=arch)
        fr = Image.new('RGBA', (tw, th - 40), (0, 0, 0, 0))
        spr.paste(fr)
        r3.append(_tile(label, fr, tw, th, BG))
    r4 = []
    for age in (0.1, 0.3, 0.6, 1.0, 1.4):
        cam = view_cam((-10.0, 22.0, 8.0), (tw, th - 40), fit=19)
        spr = draw(cam, Pose(), pattern=3, ol=5, flap=0.5, beat=0.5, blow=age)
        fr = Image.new('RGBA', (tw, th - 40), (0, 0, 0, 0))
        spr.paste(fr)
        r4.append(_tile(f'blow {age:.1f}s', fr, tw, th, BG))
    im = Image.new('RGB', (tw * 5, th * 4), BG)
    for r, row in enumerate((r1, r2, r3, r4)):
        for c, t in enumerate(row):
            im.paste(t, (c * tw, r * th))
    im.save(out, quality=88)
    return out


def reel(out, small=False):
    import imageio.v2 as iio
    size = (540, 960) if small else (1080, 1920)
    cam = Cam((0, -32, 6), 0, 4, focal=900 * size[0] / 1080, size=size)
    fps = 24
    wr = iio.get_writer(out, fps=fps, codec='libx264', quality=7, macro_block_size=1)
    for f in range(fps * 4):
        t = f / fps
        frame = Image.new('RGBA', size, (214, 200, 214, 255))
        # as in the film: from just behind the camera, low, away towards the rig and rising, speeding up
        pose = Pose((3 + 1.2 * t, -20 + 5 * t + 2.2 * t * t, 4 + 1.6 * t + 0.3 * t * t), yaw=-8, pitch=10, roll=-6)
        spr = draw(cam, pose, pattern=1, t=t, flap=1.0, beat=1.0, blow=(t - 1.0) if t > 1.0 else None)
        if spr:
            spr.paste(frame)
        wr.append_data(np.asarray(frame.convert('RGB')))
    wr.close()
    return out


def check():
    import linecheck
    bad = []
    for k in range(5):
        lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        for i, eye in enumerate(((0.0, 30.0, 0.0), (-22.0, 16.0, 14.0))):
            cam = view_cam(eye, (1080, 900))
            spr = draw(cam, Pose(), pattern=k, ol=5, t=0.4, flap=1.0, beat=1.0)
            fr = Image.new('RGBA', (1080, 900), (0, 0, 0, 0))
            spr.paste(fr)
            lay.alpha_composite(fr, (0, i * 960))
        found, _ = linecheck.analyse(lay)
        bad += [f"{PATTERNS[k]['name']}: {kd} at ({x}, {y}): {det}" for kd, x, y, det in found]
    print('\n'.join(bad) if bad else 'whale line work: every shape outlined, one weight')
    return bad


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'sheet'
    if cmd == 'sheet':
        print(sheet(sys.argv[2]))
    elif cmd == 'moves':
        print(moves(sys.argv[2]))
    elif cmd == 'reel':
        print(reel(sys.argv[2], '--small' in sys.argv))
    elif cmd == 'check':
        check()
