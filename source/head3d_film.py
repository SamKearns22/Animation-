#!/usr/bin/env python3
"""MAP  head3d_film: the back of a head from the measured 3D body (MakeHuman's skull, ears, jaw and neck), posed on
a skeleton's head and drawn through the film's own camera in the flat look, with a buzz cut painted on its skull.

Why (GTA shot 4, chat 26 F1/F5, chat 28: "the back of the head is a tall brown flowerpot"): the house's head is
drawn face-on and turned in five fixed views; its back view is a flat brown shape with a straight lower edge. From
behind, a real head is a round skull on a neck, the hair ending low at the nape, the ears standing off the sides,
the jaw's corner showing past the cheek. The face side stays the house's drawn face; only views from behind use
this.

  head_mesh() ...... the head and upper neck of Jason's build (hand3d_film.MAN), smoothed, closed at the neck cut,
                     each point marked skin or hair (HAIRLINE: the buzz cut's edge, low at the nape, over the ears)
  draw(img, cam, k, hair, skin, neck_px, height_px)
                     onto img: the head turned as k's (hup, hfwd), its neck on neck_px (frame pixels, where the house
                     trunk's collar is), chin to crown height_px tall (the house head's size, so it never jumps)
  sheet(OUT) ....... the head from 8 directions round it, level and from above (the test before any film frame)

    python3 source/head3d_film.py sheet OUT.jpg
"""
import functools
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import arm3d_film as A3     # noqa: E402
import hand3d_film as HF    # noqa: E402
import hands3d as H3        # noqa: E402
import mesh_sdf             # noqa: E402
import mhuman as H          # noqa: E402

NECK_CUT = 8.45             # decimetres up (MakeHuman): the head's neck is cut here (the house neck runs on below)
# the buzz cut's lower edge (MakeHuman decimetres): height of the edge against how far forward (z), round the head
HAIR_Z = [-0.8, -0.2, 0.25, 0.75, 1.15, 2.0]
HAIR_Y = [9.12, 9.22, 9.80, 10.00, 10.32, 10.40]
CHIN, CROWN = 8.30, 10.85


def _u(v):
    v = np.asarray(v, float)
    return v / (np.linalg.norm(v) or 1.0)


def _perp(v, a):
    return np.asarray(v, float) - a * (np.asarray(v, float) @ a)


def hair_of(p):
    """> 0 where a point (MakeHuman, decimetres) is under the buzz cut, < 0 skin (face, ears, neck): a smooth value,
    so the hair's edge is found per pixel between points."""
    x, y, z = p
    f = y - np.interp(z, HAIR_Z, HAIR_Y)
    ear = min(abs(x) - 0.80, y - 9.15, 10.0 - y, z + 0.35, 0.75 - z)    # the ears stand out of the hair
    if ear > 0:
        f = min(f, -ear)
    return f


@functools.lru_cache(maxsize=2)
def head_mesh():
    v, g, sk = H3.body(tuple(sorted(HF.MAN.items())))
    keep = v[:, 1] > NECK_CUT
    faces = [f for f in g['body'] if keep[f].any()]
    V2, q2 = mesh_sdf.catmull_clark(v, faces)
    T = np.array(mesh_sdf.triangulate(q2))
    used, T = np.unique(T, return_inverse=True)
    V2 = A3.clamp(V2[used], np.array([0, NECK_CUT, 0.0]), np.array([0, 1.0, 0]))
    V2, T = A3._cap(V2, T.reshape(-1, 3))
    kind = np.array([hair_of(p) for p in V2])
    M = sk.pose_matrices({})
    neck = H.bone_ends(sk, M, 'neck01')[0]
    return V2, T, kind, neck


def pose(k, scale):
    """The head's points in the world (metres): MakeHuman's (left, up, front) onto the skeleton head's."""
    V, T, kind, neck = head_mesh()
    up = _u(k['hup'])
    fw = _u(_perp(k['hfwd'], up))
    left = _u(_perp(_perp(np.asarray(k['shL'], float) - k['shR'], up), fw))
    R = np.stack([left, up, fw], 1)
    return np.asarray(k['neck'], float) + ((V - neck) * 0.1 * scale) @ R.T, T, kind


def _roll_to(W, cam, centre, up_w, up_px):
    """Turn the points about the lens's axis through centre so the head's up lands along up_px on screen (the house
    head's own lean: the face keeps its turn from us, only its tilt in the picture follows the drawn neck)."""
    c = np.asarray(centre, float)
    p0 = np.array(cam.project(tuple(c))[0], float)

    def ang(Wx, u):
        q = np.array(cam.project(tuple(c + u * 0.1))[0], float) - p0
        return math.atan2(q[1], q[0])
    want = math.atan2(up_px[1], up_px[0])
    ax = np.asarray(cam.f, float)
    best = None
    for sg in (1, -1):
        a = sg * (want - ang(W, up_w))
        a = (a + math.pi) % (2 * math.pi) - math.pi
        K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
        R = np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K
        err = abs((ang(None, R @ up_w) - want + math.pi) % (2 * math.pi) - math.pi)
        if best is None or err < best[0]:
            best = (err, R)
    R = best[1]
    return c + (W - c) @ R.T


def draw(img, cam, k, hair, skin, neck_px=None, height_px=None, outline=None, up_px=None):
    """The head onto img (RGBA, full size). neck_px, height_px: 1080-wide frame pixels; up_px: the drawn head's up on
    screen (a 2D direction). Returns the box or None."""
    ss = img.width / 1080.0
    head = np.asarray(k['head'], float)
    scale = 1.0
    if height_px:
        kw = cam.focal / max(cam.NEAR, cam.depth(tuple(head)))
        scale = height_px / kw / ((CROWN - CHIN) * 0.1)
    W, T, kind = pose(k, scale)
    if up_px is not None:
        W = _roll_to(W, cam, k['neck'], _u(k['hup']), up_px)
    if neck_px is not None:
        cp, cr, cu, cf = (np.asarray(x, float) for x in (cam.pos, cam.r, cam.u, cam.f))
        dpx = np.asarray(neck_px, float) - np.array(cam.project(tuple(k['neck']))[0], float)
        kwv = cam.focal / np.maximum((W - cp) @ cf, cam.NEAR)
        W = W + (dpx[0] / kwv)[:, None] * cr - (dpx[1] / kwv)[:, None] * cu
    got = HF.paint(img, cam, W, T, skin, W.mean(0), outline, 0.35, ss,
                   colours=(tuple(skin), tuple(hair)), field=kind)
    if got is None:
        return None
    lay, (x0, y0), _ = got
    img.alpha_composite(lay, (x0, y0))
    return (x0, y0, x0 + lay.width, y0 + lay.height)


def sheet(out):
    import gta_cast as GC
    import sets as S
    sp = GC.cast()['jason']
    k = {'neck': np.zeros(3), 'head': np.array([0, 0.15, 0.0]), 'hup': np.array([0, 1.0, 0]),
         'hfwd': np.array([0, 0, 1.0]), 'shL': np.array([-0.25, 0, 0]), 'shR': np.array([0.25, 0, 0])}
    tiles = []
    for el in (5, 35):
        for deg in range(0, 360, 45):
            a, e = math.radians(deg), math.radians(el)
            pos = (math.sin(a) * math.cos(e) * 1.2, 0.12 + math.sin(e) * 1.2, math.cos(a) * math.cos(e) * 1.2)
            cam = S.Cam(pos, (0.0, 0.12, 0.0), focal=1000 * 1.2 / 0.7)
            im = Image.new('RGBA', (2160, 3840), (235, 230, 222, 255))
            draw(im, cam, k, sp['hair_c'], sp['skin'])
            t = im.crop((480, 1320, 1680, 2520)).convert('RGB').resize((260, 260), Image.LANCZOS)
            ImageDraw.Draw(t).text((6, 6), f'{deg} el{el}', fill=(0, 0, 0))
            tiles.append(t)
    sh = Image.new('RGB', (260 * 8, 260 * 2), 'white')
    for i, t in enumerate(tiles):
        sh.paste(t, ((i % 8) * 260, (i // 8) * 260))
    sh.save(out, quality=88)


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
