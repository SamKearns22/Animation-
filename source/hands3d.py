#!/usr/bin/env python3
"""Hands for the flat cartoon films, built on MakeHuman's real hand (CC0) and drawn in our flat style.

Hands are the hardest thing to invent in flat shapes: drawn freehand from circles and sausages they come out as
claws, mittens or worse (Russiadent Evil, 6 Oct 2026). So, like the bodies in the trailer (character-anatomy.md),
hands start from MakeHuman's measured hand with its real bones: the fingers are bent by the skeleton, a solver
finds the bends that make the hand hold the prop (the fingers rest on it without passing through it, the thumb
lands where it should), and a small renderer draws the result as flat skin with one shadow tone and clean
black outlines (silhouette, the edges where one finger crosses another, and the knuckle creases). The prop
itself (a phone, a cup) is in the render too, so whatever is behind it is hidden.

Units: metres. The prop's frame: X to the right, Y up, Z towards the viewer.

    import hands3d
    lay = hands3d.phone_hands(size, to_px, tap=0.0)   # an RGBA layer: both hands holding a phone
    python3 hands3d.py phone OUT.png                    # a test picture

Everything slow (the shaped body, the solved poses) is cached in memory for the run.
"""
import functools
import math
import sys

import numpy as np
from PIL import Image, ImageFilter

import mhuman as H
import mesh_sdf

INK = (24, 20, 22)
HAND_BONES = ('wrist', 'metacarpal', 'finger')
ARM_BONES = HAND_BONES + ('lowerarm',)
# a woman of about 30, slim (the reporter); other characters can pass their own shape
WOMAN = dict(gender=0.0, age=0.45, muscle=0.45, weight=0.4, height=0.5, proportions=0.7)


@functools.lru_cache(maxsize=4)
def body(shape_items=tuple(sorted(WOMAN.items()))):
    v, g = H.load_base()
    H.apply_macros(v, H.macro_values(**dict(shape_items)))
    return v, g, H.Skeleton(v)


def part_faces(g, sk, v, side, bones):
    """Faces of the body moved mostly by the given bones on one side."""
    own, tot = np.zeros(len(v)), np.zeros(len(v))
    for b, (idx, w) in sk.weights.items():
        tot[idx] += w
        if b.endswith('.' + side) and b.startswith(bones):
            own[idx] += w
    part = own / np.maximum(tot, 1e-9) > 0.5
    return [f for f in g['body'] if part[f].all()], own / np.maximum(tot, 1e-9)


def finger_pose(side, x):
    """x: 8 finger bends (base, middle for fingers 2-5; the tip joint follows the middle at 0.7) and 4 thumb
    angles (base flex, middle, tip, base swing)."""
    local = {}
    for i, f in enumerate((2, 3, 4, 5)):
        k, m = x[2 * i], x[2 * i + 1]
        for j, a in enumerate((k, m, 0.7 * m)):
            local['finger%d-%d.%s' % (f, j + 1, side)] = H.axis_angle([1, 0, 0], a)
    t0, t1, t2, t3 = x[8:12]
    local['finger1-1.%s' % side] = H.axis_angle([1, 0, 0], t0) @ H.axis_angle([0, 0, 1], t3)
    local['finger1-2.%s' % side] = H.axis_angle([1, 0, 0], t1)
    local['finger1-3.%s' % side] = H.axis_angle([1, 0, 0], t2)
    return local


def palm_frame(sk, M, side):
    """The palm's frame in MakeHuman space: x along the middle metacarpal (towards the fingers), y out of the back
    of the hand, z = x cross y; origin at the middle of the palm. Returns (R columns, origin) in decimetres."""
    h3, t3 = H.bone_ends(sk, M, 'metacarpal3.' + side)
    h2, _ = H.bone_ends(sk, M, 'metacarpal2.' + side)
    h4, _ = H.bone_ends(sk, M, 'metacarpal4.' + side)
    x = (t3 - h3) / np.linalg.norm(t3 - h3)
    across = h2 - h4
    y = np.cross(across, x)
    y -= x * (y @ x)
    y /= np.linalg.norm(y)
    # fingers flex towards the palm, so the back of the hand is on the other side from where a curled tip goes
    Mc = sk.pose_matrices(finger_pose(side, [60] * 8 + [0] * 4))
    tip = H.bone_ends(sk, Mc, 'finger3-3.' + side)[1]
    if (tip - t3) @ y > 0:
        y = -y
    return np.stack([x, y, np.cross(x, y)], 1), (h3 + t3) / 2


def place(side, palm_x, palm_back, origin):
    """The rigid move taking the palm frame onto the prop frame: palm_x (fingers' direction), palm_back (out of
    the back of the hand), origin (palm centre), all in metres in the prop frame."""
    x = np.asarray(palm_x, float)
    x /= np.linalg.norm(x)
    y = np.asarray(palm_back, float)
    y -= x * (y @ x)
    y /= np.linalg.norm(y)
    return np.stack([x, y, np.cross(x, y)], 1), np.asarray(origin, float)


def bone_points(sk, M, side, R0, o0, Rp, op):
    """Sample points along the finger and thumb bones, moved into the prop frame (metres)."""
    out = {}
    for f in (1, 2, 3, 4, 5):
        pts = []
        for j in (1, 2, 3):
            h, t = H.bone_ends(sk, M, 'finger%d-%d.%s' % (f, j, side))
            pts += [h + (t - h) * s for s in (0.0, 0.5, 1.0)]
        pts = np.array(pts)
        out[f] = ((pts - o0) @ R0 * 0.1) @ Rp.T + op
    return out


def solve(side, palm_x, palm_back, origin, thumb_tip, prop_box, x0=None, finger_r=0.0085, nail_z=0.88):
    """Bend the fingers and thumb to hold a box-shaped prop (prop_box = (half w, half h, back z, front z)): the
    fingers rest against its back (never through it), the thumb's tip lands on thumb_tip (on the front)."""
    from scipy.optimize import minimize
    v, g, sk = body()
    M0 = sk.pose_matrices({})
    R0, o0 = palm_frame(sk, M0, side)
    Rp, op = place(side, palm_x, palm_back, origin)
    hw, hh, zb, zf = prop_box
    tip = np.asarray(thumb_tip, float)

    def inside(p, r):
        """How far points p (with radius r) dig into the box (0 when clear)."""
        dx = hw - np.abs(p[:, 0])
        dy = hh - np.abs(p[:, 1])
        dz = np.minimum(p[:, 2] - zb + r, zf + r - p[:, 2])
        return np.maximum(0, np.minimum(np.minimum(dx + r, dy + r), dz))

    def cost(x):
        M = sk.pose_matrices(finger_pose(side, x))
        P = bone_points(sk, M, side, R0, o0, Rp, op)
        e = 0.0
        for f in (2, 3, 4, 5):   # fingers: rest on the back (their pads touching it), never inside it
            q = P[f][3:]
            e += 4e4 * (inside(q, finger_r) ** 2).sum()
            e += 2e3 * ((q[:, 2] - (zb - finger_r)) ** 2).sum()
        q = P[1]
        # the thumbnail faces us (a thumb on a screen shows its nail, never its pad): bend the tip joint a little
        # more and see which way the tip moves; that is the pad's side, so the nail faces the other way
        x2 = np.array(x, float)
        x2[10] += 25
        q2 = bone_points(sk, sk.pose_matrices(finger_pose(side, x2)), side, R0, o0, Rp, op)[1]
        b = q[-1] - q[-4]
        b /= np.linalg.norm(b)
        mv = q2[-1] - q[-1]
        nail = -(mv - b * (mv @ b))
        nail /= max(1e-9, np.linalg.norm(nail))
        e += 3000 * max(0.0, nail_z - nail[2]) ** 2
        e += 4e4 * (inside(q[2:], finger_r) ** 2).sum()
        e += 3e4 * ((q[-1] - tip) ** 2).sum()                      # the thumb's tip where it should be
        e += 1e-4 * (np.maximum(0, x[:8] - 90) ** 2).sum() + 1e-4 * (np.maximum(0, -10 - x[:8]) ** 2).sum()
        e += 1e-3 * sum(np.maximum(0, x[8 + i] - hi) ** 2 + np.maximum(0, lo - x[8 + i]) ** 2
                        for i, (lo, hi) in enumerate(((-30, 60), (-10, 60), (-10, 70), (-60, 60))))
        e += 1e-5 * ((x[:8] - 20) ** 2).sum()
        return e
    x0 = np.array([20, 20] * 4 + [0, 10, 10, 0], float) if x0 is None else x0
    res = minimize(cost, x0, method='Powell', options={'maxiter': 6000, 'xtol': 1e-2, 'ftol': 1e-9})
    return res.x, res.fun


def hand_mesh(side, x, palm_x, palm_back, origin, sleeve_from=0.035):
    """The posed hand and forearm, subdivided, in the prop frame (metres). Returns (V, tris, kind) where kind
    is 0 for skin, 1 for sleeve (the forearm beyond sleeve_from metres from the wrist)."""
    v, g, sk = body()
    local = finger_pose(side, x)
    M = sk.pose_matrices(local)
    R0, o0 = palm_frame(sk, sk.pose_matrices({}), side)
    Rp, op = place(side, palm_x, palm_back, origin)
    v2 = sk.skin(v, local)
    faces, _ = part_faces(g, sk, v, side, ARM_BONES)
    V = ((v2 - o0) @ R0 * 0.1) @ Rp.T + op
    V2, q2 = mesh_sdf.catmull_clark(V, faces)
    tris = np.array(mesh_sdf.triangulate(q2))
    wr = ((sk.rest['wrist.' + side][:3, 3] - o0) @ R0 * 0.1) @ Rp.T + op
    fore = ((sk.rest['lowerarm02.' + side][:3, 3] - o0) @ R0 * 0.1) @ Rp.T + op
    d = (fore - wr) / np.linalg.norm(fore - wr)
    kind = (((V2 - wr) @ d) > sleeve_from).astype(int)
    return V2, tris, kind


def nail_meshes(side, x, palm_x, palm_back, origin):
    """The nails (MakeHuman's mesh has none: they are only painted on its skin texture). Each sits on the back of
    the last joint of its finger, over the last 60% of it: we find the back by bending that joint a little - the
    tip moves towards the pad, so the nail faces the other way. Returns [(V, tris)] in the prop frame."""
    v, g, sk = body()
    R0, o0 = palm_frame(sk, sk.pose_matrices({}), side)
    Rp, op = place(side, palm_x, palm_back, origin)
    x = np.asarray(x, float)
    P = bone_points(sk, sk.pose_matrices(finger_pose(side, x)), side, R0, o0, Rp, op)
    out = []
    for f in (1, 2, 3, 4, 5):
        x2 = x.copy()
        x2[10 if f == 1 else 2 * (f - 2) + 1] += 25
        q2 = bone_points(sk, sk.pose_matrices(finger_pose(side, x2)), side, R0, o0, Rp, op)[f]
        h_, t_ = P[f][6], P[f][8]
        b = (t_ - h_) / np.linalg.norm(t_ - h_)
        mv = q2[-1] - P[f][-1]
        n = -(mv - b * (mv @ b))
        n /= np.linalg.norm(n)
        a = np.cross(n, b)
        r, ln, wd = (0.0086, 0.0054, 0.0038) if f == 1 else (0.0072, 0.0044, 0.0032)
        c = h_ + (t_ - h_) * 0.68 + n * r
        ring = [c + b * ln * math.cos(u) + a * wd * math.sin(u) - n * 0.0012 * (math.sin(u) ** 2)
                for u in np.linspace(0, 2 * math.pi, 16, endpoint=False)]
        V = np.array([c + n * 0.0004] + ring)
        tris = np.array([(0, 1 + k, 1 + (k + 1) % 16) for k in range(16)])
        out.append((V, tris))
    return out


# ------------------------------------------------------------------------------------------- the flat renderer
def render(meshes, size, to_px, light=(-0.3, 0.5, 0.85), eye_d=0.45, outline=3.0, hide=(9,)):
    """Draw meshes [(V, tris, colours per kind, id)] in our flat style onto an RGBA layer of `size`.
    to_px(X, Y) maps the prop frame (metres, at Z = 0) to layer pixels; points nearer the viewer (Z > 0) are
    drawn a little larger (a mild perspective, eye_d metres away). Meshes whose id is 0 only hide what is
    behind them (the prop): they are not drawn."""
    w, h = size
    zbuf = np.full((h, w), -1e9)
    ibuf = np.zeros((h, w), np.int16)
    nbuf = np.zeros((h, w, 3))
    cbuf = np.zeros((h, w, 3))
    L = np.asarray(light, float)
    L /= np.linalg.norm(L)
    for V, tris, colours, mid in meshes:
        k = eye_d / np.maximum(0.05, eye_d - V[:, 2])
        P = np.array([to_px(x * kk, y * kk) for (x, y), kk in zip(V[:, :2], k)])
        # vertex normals
        tv = V[tris]
        fn = np.cross(tv[:, 1] - tv[:, 0], tv[:, 2] - tv[:, 0])
        vn = np.zeros_like(V)
        for j in range(3):
            np.add.at(vn, tris[:, j], fn)
        vn /= np.maximum(1e-12, np.linalg.norm(vn, axis=1))[:, None]
        for ti, (a, b, c) in enumerate(tris):
            pa, pb, pc = P[a], P[b], P[c]
            x0, x1 = int(max(0, min(pa[0], pb[0], pc[0]))), int(min(w - 1, max(pa[0], pb[0], pc[0])) + 1)
            y0, y1 = int(max(0, min(pa[1], pb[1], pc[1]))), int(min(h - 1, max(pa[1], pb[1], pc[1])) + 1)
            if x1 <= x0 or y1 <= y0:
                continue
            det = (pb[1] - pc[1]) * (pa[0] - pc[0]) + (pc[0] - pb[0]) * (pa[1] - pc[1])
            if abs(det) < 1e-9:
                continue
            X, Y = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
            l1 = ((pb[1] - pc[1]) * (X - pc[0]) + (pc[0] - pb[0]) * (Y - pc[1])) / det
            l2 = ((pc[1] - pa[1]) * (X - pc[0]) + (pa[0] - pc[0]) * (Y - pc[1])) / det
            l3 = 1 - l1 - l2
            m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
            if not m.any():
                continue
            z = l1 * V[a, 2] + l2 * V[b, 2] + l3 * V[c, 2]
            sub = zbuf[y0:y1, x0:x1]
            m &= z > sub
            if not m.any():
                continue
            sub[m] = z[m]
            ibuf[y0:y1, x0:x1][m] = mid
            n = l1[..., None] * vn[a] + l2[..., None] * vn[b] + l3[..., None] * vn[c]
            nbuf[y0:y1, x0:x1][m] = n[m]
            cbuf[y0:y1, x0:x1][m] = colours[kind_of(tris, ti)]
    # flat shading: one light tone, one shadow tone
    nn = nbuf / np.maximum(1e-9, np.linalg.norm(nbuf, axis=2))[..., None]
    lit = nn @ L
    shade = np.where(lit > -0.05, 1.0, 0.88)
    rgb = cbuf * shade[..., None]
    # outlines: where the thing drawn changes, where the depth jumps (one finger over another), where the surface
    # turns sharply away (the creases at the knuckles)
    edge = np.zeros((h, w), bool)
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        a_i, b_i = ibuf, np.roll(np.roll(ibuf, dy, 0), dx, 1)
        a_z, b_z = zbuf, np.roll(np.roll(zbuf, dy, 0), dx, 1)
        a_n, b_n = nn, np.roll(np.roll(nn, dy, 0), dx, 1)
        e = (a_i != b_i) | ((np.abs(a_z - b_z) > 0.004) & (a_i > 0) & (b_i > 0))
        e |= ((a_n * b_n).sum(2) < 0.3) & (a_i > 0) & (b_i > 0) & (a_i == b_i)
        edge |= e
    drawn = (ibuf > 0) & ~np.isin(ibuf, hide)
    mask = Image.fromarray((drawn * 255).astype(np.uint8))
    ed = Image.fromarray((edge & (drawn | np.roll(drawn, 1, 0) | np.roll(drawn, 1, 1)) * 255).astype(np.uint8))
    ed = ed.filter(ImageFilter.MaxFilter(int(outline) | 1))
    out = np.zeros((h, w, 4), np.uint8)
    out[..., :3] = np.clip(rgb, 0, 255)
    out[..., 3] = np.asarray(mask)
    E = np.asarray(ed) > 0
    E &= (np.asarray(mask.filter(ImageFilter.MaxFilter(int(outline) | 1))) > 0)
    out[E, :3] = INK
    out[E, 3] = 255
    return Image.fromarray(out, 'RGBA')


_KIND = {}


def kind_of(tris, ti):
    return _KIND[id(tris)][ti]


def mesh_entry(V, tris, kind, colours, mid):
    """A mesh for render(): the colour of each triangle comes from its vertices' kind (skin or sleeve)."""
    _KIND[id(tris)] = np.max(kind[tris], axis=1)
    return (V, tris, colours, mid)


def box_mesh(hw, hh, zb, zf, r=0.009, n=6):
    """A box with rounded corners seen from the front (the phone): a rounded rectangle extruded from zb to zf."""
    ring = []
    for cx, cy, a0 in ((hw - r, hh - r, 0), (-hw + r, hh - r, 90), (-hw + r, -hh + r, 180), (hw - r, -hh + r, 270)):
        ring += [(cx + r * math.cos(math.radians(a0 + 90 * k / n)), cy + r * math.sin(math.radians(a0 + 90 * k / n)))
                 for k in range(n + 1)]
    m = len(ring)
    V = np.array([(x, y, z) for z in (zb, zf) for x, y in ring] + [(0, 0, zb), (0, 0, zf)], float)
    tris = []
    for i in range(m):
        j = (i + 1) % m
        tris += [(i, j, m + j), (i, m + j, m + i), (2 * m, j, i), (2 * m + 1, m + i, m + j)]
    return V, np.array(tris), np.zeros(len(V), int)


# ------------------------------------------------------------------------------------------- the phone grip
PHONE = (0.0375, 0.077, -0.0085, 0.0)       # half width, half height, back, front (metres)
SKIN = (240, 226, 216)


CACHE = __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'data',
                                   'hands3d_cache.json')


def cached(key, fn):
    """Solved poses are kept in source/data/hands3d_cache.json (small), keyed by everything that shapes them."""
    import json
    import os
    db = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    if key not in db:
        db[key] = fn()
        json.dump(db, open(CACHE, 'w'), indent=1)
    return db[key]


@functools.lru_cache(maxsize=8)
def phone_grip(side, tap_key=0):
    """One hand holding the phone from below, as people type with both thumbs: the palm under the phone's lower
    corner, the fingers spread behind it, the thumb over the screen. tap_key 0-2: the right thumb's positions
    while typing (lifted, pressing...). Returns (x, placement)."""
    hw, hh, zb, zf = PHONE
    sg = -1 if side == 'L' else 1
    palm_x = (-sg * 0.42, 0.9, -0.15)                # fingers up and in, behind the phone
    palm_back = (sg * 0.55, -0.15, -1.0)             # the back of the hand away from us, turned out a little
    origin = (sg * (hw - 0.002), -hh + 0.012, zb - 0.022)
    taps = [(0.012, -0.016, 0.010), (0.016, -0.022, 0.004)]          # lifted, pressed
    tip = (sg * 0.006, -0.03, 0.006) if side == 'L' else taps[tap_key]
    key = repr(('phone3', side, palm_x, palm_back, origin, tip, PHONE, sorted(WOMAN.items())))
    x, err = cached(key, lambda: [list(map(float, r)) if hasattr(r, '__len__') else float(r)
                                  for r in solve(side, palm_x, palm_back, origin, tip, PHONE)])
    return tuple(x), (palm_x, palm_back, origin), err


def phone_hands(size, to_px, tap_key=0, skin=SKIN, sleeve=(240, 230, 206), outline=3.0):
    """Both hands holding the phone, as an RGBA layer (the phone itself is not drawn: it only hides what is
    behind it; draw the phone first, then this on top)."""
    meshes = [mesh_entry(*box_mesh(*PHONE), (skin, skin), 9)]
    for side, mid in (('L', 1), ('R', 2)):
        x, (px, pb, o), _ = phone_grip(side, tap_key if side == 'R' else 0)
        V, tris, kind = hand_mesh(side, np.array(x), px, pb, o)
        meshes.append(mesh_entry(V, tris, kind, (skin, sleeve), mid))
        nc = tuple(min(255, int(c * 1.04 + 6)) for c in skin)
        for j, (Vn, tn) in enumerate(nail_meshes(side, np.array(x), px, pb, o)):
            meshes.append(mesh_entry(Vn, tn, np.zeros(len(Vn), int), (nc, nc), 10 + 5 * mid + j))
    return render(meshes, size, to_px, outline=outline)   # the phone's own pixels stay transparent


if __name__ == '__main__':
    if sys.argv[1] == 'phone':
        W_, H_ = 1080, 1920
        k = 7000.0
        lay = phone_hands((W_, H_), lambda X, Y: (540 + X * k, 820 - Y * k))
        bg = Image.new('RGBA', (W_, H_), (90, 70, 56, 255))
        from PIL import ImageDraw
        d = ImageDraw.Draw(bg)
        hw, hh = PHONE[0] * k, PHONE[1] * k
        d.rounded_rectangle([540 - hw, 820 - hh, 540 + hw, 820 + hh], 60, fill=(24, 24, 28))
        d.rounded_rectangle([540 - hw + 22, 820 - hh + 22, 540 + hw - 22, 820 + hh - 22], 46, fill=(240, 240, 244))
        bg.alpha_composite(lay)
        bg.convert('RGB').save(sys.argv[2])
        for side in 'LR':
            print(side, np.round(phone_grip(side)[0], 1), 'error', phone_grip(side)[2])
