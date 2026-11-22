#!/usr/bin/env python3
"""MAP  hand3d_film: real hands with fingers (hands3d's MakeHuman hand, posed) drawn through ANY film camera at a
skeleton's wrist, in the house's flat look (flat skin, ink outlines, knuckle creases).

Why (GTA shot 4, Sam 21 Nov: "a great shot but a broken drawing": "the hand on the door a blob", F2/F13): the house's
circle hand reads as a hand only from in front at phone size. From behind or side-on, at full size, it is a disc on
the end of a tube. The project already had a measured hand that wraps a handle or hooks over an edge (hands3d, built
for Russiadent Evil's phone and the severed-arm gag), but only from one fixed view. Here the same hand is turned into
the film's world and drawn through the film's own camera, so it reads from wherever the shot looks at it.

  POSES ............ 'edge': palm down on a ledge, fingers hooked over its far edge (a hand on a car's door top);
                     'grip': closed round a handle (a pistol's grip), the thumb wrapped over
  _mesh(pose, side)  the posed hand and a short wrist, in its own frame (metres): anchor at 0, A along +x, B along +y
                     (edge: anchor the wrist, A the fingers' way, B out of the back of the hand;
                      grip: anchor the handle's middle, A up the handle to the index finger, B out of the back)
  draw(img, cam, pose, side, anchor, A, B, skin, scale)
                     onto img (RGBA, full size) in a small crop: world -> camera -> hands3d.render; the wrist end is
                     faded out towards the elbow so it joins the drawn forearm with no cut line. Returns the drawn box.

    python3 source/hand3d_film.py test OUT.jpg     the two hands from 8 directions round them
"""
import functools
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import hands3d as H3       # noqa: E402
import mhuman as H         # noqa: E402
import mesh_sdf            # noqa: E402

MAN = dict(gender=1.0, age=0.5, muscle=0.75, weight=0.55, height=0.6, proportions=0.6)   # Jason's build
EDGE_X = [5, 70] * 4 + [10, 10, 10, -10]       # hands3d.edge_grab's bends: fingers flat to the knuckles, hooked over
AA = 3                                         # the hand is drawn 3x and shrunk (smooth edges)
WRIST_KEEP = 0.045                             # metres of forearm kept past the wrist (faded into the drawn arm)


def _u(v):
    v = np.asarray(v, float)
    return v / (np.linalg.norm(v) or 1.0)


@functools.lru_cache(maxsize=8)
def _mesh(pose, side):
    """(V, tris, wrist, fore_dir) in the pose's own frame (metres): anchor at 0, A = +x, B = +y."""
    v, g, sk = H3.body(tuple(sorted(MAN.items())))
    if pose == 'edge':
        local = H3.finger_pose(side, EDGE_X)
        R0, o0 = H3.palm_frame(sk, sk.pose_matrices({}), side)
        a, b = R0[:, 0], R0[:, 1]                                  # fingers' way, out of the back of the hand
        anchor = sk.rest['wrist.' + side][:3, 3]
    elif pose == 'grip':
        local, c, d, _ = H.solve_grip(sk, side, 0.13)
        M = sk.pose_matrices(local)
        R0, _ = H3.palm_frame(sk, M, side)
        tip = H.bone_ends(sk, M, 'finger2-1.' + side)[0]           # up the handle: towards the index finger
        if (tip - c) @ d < 0:
            d = -d
        a = _u(d)
        b = _u(R0[:, 1] - a * (R0[:, 1] @ a))
        anchor = c
    else:
        raise KeyError(pose)
    b = _u(b - a * (a @ b))
    R = np.stack([a, b, np.cross(a, b)], 1)                       # MH -> (A, B, A x B)
    v2 = sk.skin(v, local)
    faces, _ = H3.part_faces(g, sk, v, side, H3.ARM_BONES)
    to = lambda q: ((np.asarray(q, float) - anchor) @ R) * 0.1    # noqa: E731  decimetres -> metres
    V = to(v2)
    wr = to(sk.rest['wrist.' + side][:3, 3])
    fore = to(sk.rest['lowerarm02.' + side][:3, 3])
    fd = _u(fore - wr)
    keep = [f for f in faces if (((V[f] - wr) @ fd) < WRIST_KEEP + 0.03).all()]
    V2, q2 = mesh_sdf.catmull_clark(V, keep)
    T = np.array(mesh_sdf.triangulate(q2))
    used, T = np.unique(T, return_inverse=True)                   # only the hand's own points (the rest of the
    return V2[used], T.reshape(-1, 3), wr, fd                     # body's would stretch the drawing box)


def frame_of(A, B):
    A = _u(A)
    B = _u(np.asarray(B, float) - A * (A @ _u(B)) * np.linalg.norm(B))
    return np.stack([A, B, np.cross(A, B)], 1)


def paint(img, cam, W, tris, skin, ref, outline=None, crease=0.2, ss=None, colours=None, kind=None, shade=False, field=None):
    """Any mesh already in the world (W: points, metres) drawn through the film's camera in the flat look onto a
    fresh layer the size of its own box. ref: a world point near the mesh's middle (its depth sets the perspective).
    Returns (layer RGBA, (x0, y0), kw = camera pixels per metre at ref) or None (behind the lens, off frame)."""
    ss = ss or img.width / 1080.0
    cp, cr, cu, cf = (np.asarray(x, float) for x in (cam.pos, cam.r, cam.u, cam.f))
    dw = float((np.asarray(ref, float) - cp) @ cf)
    if dw <= cam.NEAR:
        return None
    D = np.asarray(W, float) - cp
    C = np.stack([D @ cr, D @ cu, dw - D @ cf], 1)                 # camera frame: x right, y up, z towards us
    if (dw - C[:, 2]).min() <= cam.NEAR:
        return None
    kw = cam.focal / dw
    roll = getattr(cam, 'roll', 0.0) or 0.0
    sh = getattr(cam, 'shake', (0.0, 0.0))

    def scr(x, y):
        X, Y = x * kw, -y * kw
        if roll:
            c, s = math.cos(roll), math.sin(roll)
            X, Y = X * c - Y * s, X * s + Y * c
        return (540 + X + sh[0]) * ss, (960 + Y + sh[1]) * ss
    k = dw / np.maximum(0.05, dw - C[:, 2])
    P = np.array([scr(x * kk, y * kk) for (x, y), kk in zip(C[:, :2], k)])
    pad = 8
    x0, y0 = np.floor(P.min(0)).astype(int) - pad
    x1, y1 = np.ceil(P.max(0)).astype(int) + pad
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(img.width, x1), min(img.height, y1)
    if x1 - x0 < 4 or y1 - y0 < 4:
        return None
    size = (x1 - x0, y1 - y0)
    kind = np.zeros(len(W), int) if kind is None else kind
    ol = outline if outline is not None else max(3.0, 1.6 * ss)
    mesh = H3.mesh_entry(C, tris, kind, colours or (tuple(skin), tuple(skin)), 1)
    if field is not None:
        H3._FIELD[id(tris)] = np.asarray(field, float)
    big = (size[0] * AA, size[1] * AA)                             # drawn at AA x and shrunk: smooth edges, as the
    lay = H3.render([mesh], big, lambda x, y: ((scr(x, y)[0] - x0) * AA, (scr(x, y)[1] - y0) * AA), eye_d=dw,
                    outline=int(ol * AA) | 1, flat=not shade, crease=crease)   # house's other lines
    H3._FIELD.pop(id(tris), None)
    return lay.resize(size, Image.LANCZOS), (int(x0), int(y0)), kw


def draw(img, cam, pose, side, anchor, A, B, skin, scale=1.0, outline=None, ss=None):
    """The hand onto img at world point `anchor`, its A axis along world A, B along world B (see _mesh)."""
    V, tris, wr, fd = _mesh(pose, side)
    ss = ss or img.width / 1080.0
    R = frame_of(A, B)
    W = np.asarray(anchor, float) + (V * scale) @ R.T             # world points
    wr_w = np.asarray(anchor, float) + (wr * scale) @ R.T
    fd_w = R @ fd
    dw = float((wr_w - np.asarray(cam.pos, float)) @ np.asarray(cam.f, float))
    if dw <= cam.NEAR:
        return None
    kw0 = cam.focal / dw
    # a small hand: only the main knuckle creases
    small = (np.ptp(np.array([cam.project(tuple(q))[0] for q in W[::max(1, len(W) // 60)]])[:, 1]) * ss) < 244
    got = paint(img, cam, W, tris, skin, wr_w, outline, 0.0 if small else 0.2, ss)
    if got is None:
        return None
    lay, (x0, y0), kw = got
    size = lay.size
    # the wrist end fades into the drawn forearm: past the wrist (towards the elbow) the hand is cleared, so the
    # arm's own outline runs on and no cut ring shows
    a = np.asarray(lay.getchannel('A'), np.float32)
    w0 = np.array(cam.project(tuple(wr_w))[0]) * ss - (x0, y0)
    w1 = np.array(cam.project(tuple(wr_w + fd_w * 0.1))[0]) * ss - (x0, y0)
    dd = w1 - w0
    n = np.linalg.norm(dd)
    if n > 1 and FADE[0]:
        dd /= n
        yy, xx = np.mgrid[0:size[1], 0:size[0]]
        along = (xx - w0[0]) * dd[0] + (yy - w0[1]) * dd[1]
        off, lim = 0.022 * kw * ss * scale, 0.015 * kw * ss * scale   # the wrist's stub covers the arm's end,
        a *= np.clip(1 - (along - off) / max(1.0, lim), 0, 1)           # then fades into the drawn forearm
    lay.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(lay, (int(x0), int(y0)))
    return (x0, y0, x0 + size[0], y0 + size[1])


FADE = [True]        # the wrist fade (off when the 3D arm, arm3d_film, carries on under the hand)


def test(out):
    import sets as S
    from PIL import ImageDraw
    tiles = []
    for pose, A, B in (('edge', (1, 0, 0), (0, 1, 0)), ('grip', (0, 1, 0.3), (1, 0, 0))):
        for deg in range(0, 360, 45):
            a = math.radians(deg)
            cam = S.Cam((math.sin(a) * 0.6, 0.15, math.cos(a) * 0.6), (0, 0, 0), focal=1000 * 0.6 / 0.25)
            im = Image.new('RGBA', (2160, 3840), (235, 230, 222, 255))
            draw(im, cam, pose, 'L' if pose == 'edge' else 'R', (0, 0, 0), A, B, (236, 196, 168))
            t = im.crop((480, 1320, 1680, 2520)).resize((300, 300))
            ImageDraw.Draw(t).text((6, 6), f'{pose} {deg}', fill=(0, 0, 0))
            tiles.append(t)
    sh = Image.new('RGB', (300 * 8, 600), 'white')
    for i, t in enumerate(tiles):
        sh.paste(t, ((i % 8) * 300, (i // 8) * 300))
    sh.save(out, quality=88)


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        test(sys.argv[2])
