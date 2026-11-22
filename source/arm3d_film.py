#!/usr/bin/env python3
"""MAP  arm3d_film: a bare arm from the measured 3D body (MakeHuman), posed on any skeleton's shoulder, elbow and
wrist and drawn through the film's own camera in the house's flat look (flat skin, ink outline, a crease where the
forearm folds over the upper arm).

Why (GTA shot 4, Sam 21-22 Nov: "a great shot but a broken drawing"; "the backwards arm is a gross distended
sausage", three times): the house arm is two tapered flat pieces between the projected joints, the same width all
along. Seen from behind or pointing at the lens it becomes one long tube, or a stub with a round end. A real arm
has a shoulder cap, a biceps and triceps, an elbow point, a forearm that swells near the elbow and narrows to the
wrist; when it points at us the forearm overlaps the upper arm and the outline shows where. The hands already come
from the same measured body (hand3d_film); the arm now does too, so the two meet at the wrist.

  arm_mesh(side) ..... the arm (shoulder cap to wrist) of Jason's build (hand3d_film.MAN), smoothed, in MakeHuman
                       space, with each point's share of the upper-arm / forearm / trunk bones
  pose(side, k) ...... the mesh put on skeleton k (world, metres): the trunk's part follows the trunk, the upper arm
                       runs shoulder->elbow, the forearm elbow->wrist; the elbow's bend sets which way the biceps
                       faces (the world here is mirrored against MakeHuman's: a reflection keeps left and right)
  draw(img, cam, k, side, skin, shoulder_px=None)
                       onto img; shoulder_px (frame pixels) pins the shoulder to where the flat trunk drew it (the
                       pull fades out down the upper arm, the hand end stays on the skeleton's wrist)
  sheet(OUT) ......... the arm on Jason's shot 4 poses from 8 directions round him (the test before any film frame)

    python3 source/arm3d_film.py sheet OUT.jpg
"""
import functools
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import hand3d_film as HF    # noqa: E402
import hands3d as H3        # noqa: E402
import mesh_sdf             # noqa: E402
import mhuman as H          # noqa: E402

THICK = [1.30]              # the arm's girth against the measured man's (Jason is drawn big: shoulders 0.5 m)
SHOULDER_FADE = (0.02, 0.22)  # share of the upper arm (on screen) over which the cut end fades into the shoulder
CREASE = -0.2               # a line inside the arm only where it folds hard (the elbow), never on the cut's facets
SHOULDER_IN = 0.25          # decimetres inside the shoulder joint where the arm is cut square from the trunk


def clamp(V, p, n):
    """Points behind the plane through p (normal n, the side kept) pressed onto it: a straight, clean cut."""
    n = _u(n)
    d = (V - p) @ n
    return V - np.minimum(d, 0)[:, None] * n


def _cap(V, T):
    """Close each open end (the shoulder and wrist cuts) with a fan to its middle: no hollow tube from any side."""
    from collections import defaultdict
    cnt = defaultdict(int)
    for a, b, c in T:
        for e in ((a, b), (b, c), (c, a)):
            cnt[tuple(sorted(e))] += 1
    nxt = {}
    for a, b, c in T:
        for x, y in ((a, b), (b, c), (c, a)):
            if cnt[tuple(sorted((x, y)))] == 1:
                nxt[y] = x                       # walk the open edge the other way round from its face
    V, T = list(V), [tuple(t) for t in T]
    seen = set()
    for s0 in list(nxt):
        if s0 in seen:
            continue
        loop, p = [], s0
        while p not in seen and p in nxt:
            seen.add(p)
            loop.append(p)
            p = nxt[p]
        if len(loop) < 3:
            continue
        c = len(V)
        V.append(np.mean([V[i] for i in loop], 0))
        T += [(loop[i], loop[(i + 1) % len(loop)], c) for i in range(len(loop))]
    return np.array(V), np.array(T)


def _u(v):
    v = np.asarray(v, float)
    return v / (np.linalg.norm(v) or 1.0)


def _perp(v, axis):
    v = np.asarray(v, float)
    return v - axis * (v @ axis)


@functools.lru_cache(maxsize=4)
def arm_mesh(side):
    """(V, tris, w_upper, w_fore, joints) in MakeHuman space (decimetres)."""
    v, g, sk = H3.body(tuple(sorted(HF.MAN.items())))
    own = np.zeros(len(v))
    tot = np.zeros(len(v))
    wu = np.zeros(len(v))
    wf = np.zeros(len(v))
    for b, (idx, w) in sk.weights.items():
        tot[idx] += w
        if b.endswith('.' + side):
            if b.startswith('upperarm'):
                own[idx] += w
            if b.startswith('upperarm'):
                wu[idx] += w
            if b.startswith(('lowerarm', 'wrist', 'metacarpal', 'finger')):
                wf[idx] += w
                own[idx] += w * b.startswith(('lowerarm', 'wrist'))
    t = np.maximum(tot, 1e-9)
    share = own / t
    M = sk.pose_matrices({})
    S = H.bone_ends(sk, M, 'upperarm01.' + side)[0]
    E = H.bone_ends(sk, M, 'lowerarm01.' + side)[0]
    Wr = H.bone_ends(sk, M, 'wrist.' + side)[0]
    fu = _u(Wr - E)
    # clean cuts, not the bone weights' ragged edge: a flat cut just inside the shoulder (the deltoid kept: it is
    # what makes a shoulder read from behind) and one at the wrist (the real hand carries on from there)
    um = _u(E - S)
    a_in = ((v - S) @ um) > -SHOULDER_IN          # square across the arm, just inside the shoulder joint
    a_wr = ((v - Wr) @ fu) < 0.1
    faces = [f for f in g['body'] if (share[f] > 0.5).all() and a_in[f].any() and a_wr[f].any()]
    V2, q2 = mesh_sdf.catmull_clark(v, faces)
    T = np.array(mesh_sdf.triangulate(q2))
    used, T = np.unique(T, return_inverse=True)
    V2 = clamp(clamp(V2[used], S - um * SHOULDER_IN, um), Wr + fu * 0.1, -fu)
    T = T.reshape(-1, 3)
    V2, T = _cap(V2, T)
    # the smoothed points' bone shares: from the nearest original arm point
    ids = np.unique(np.array([i for f in faces for i in f]))
    src = v[ids]
    near = np.array([ids[np.argmin(((src - p) ** 2).sum(1))] for p in V2])
    joints = dict(sh=S, el=E, wr=Wr,
                  shL=H.bone_ends(sk, M, 'upperarm01.L')[0], shR=H.bone_ends(sk, M, 'upperarm01.R')[0],
                  neck=H.bone_ends(sk, M, 'neck01')[0], pelvis=H.bone_ends(sk, M, 'root')[0])
    return V2, T, wu[near] / t[near], wf[near] / t[near], joints


def _maps(side, k):
    """The three linear maps (3x3, origin MH -> origin world) for the trunk, upper arm and forearm."""
    V, T, wu, wf, J = arm_mesh(side)
    # trunk: MakeHuman's (left, up, front) onto the skeleton's (left, up, front); the world's front is the other
    # way round from MakeHuman's (a mirror), so this is a reflection, which keeps left as left
    acm, upm = _u(J['shL'] - J['shR']), _u(J['neck'] - J['pelvis'])
    acm = _u(_perp(acm, upm))
    frm = np.cross(acm, upm)
    acw, upw = _u(np.asarray(k['shL'], float) - k['shR']), _u(np.asarray(k['neck'], float) - k['pelvis'])
    acw = _u(_perp(acw, upw))
    frw = _u(_perp(_perp(np.asarray(k['fwd'], float), upw), acw))
    sign = 1.0 if np.cross(acw, upw) @ frw > 0 else -1.0
    ratio = float(np.linalg.norm(np.asarray(k['shL'], float) - k['shR']) / (0.1 * np.linalg.norm(J['shL'] - J['shR'])))
    ct = 0.1 * min(max(ratio, 1.0), 1.35)              # the trunk's part: the skeleton's shoulder width
    Mt = np.stack([acw, upw, frw], 1) @ np.stack([acm, upm, frm], 0) * ct
    # the upper arm: along shoulder->elbow, its front where the forearm bends to
    sh, el, wr = (np.asarray(k[n + side], float) for n in ('sh', 'el', 'wr'))
    um, fm_ = _u(J['el'] - J['sh']), _u(J['wr'] - J['el'])
    fm = _u(_perp(fm_, um))
    hm = np.cross(um, fm)
    uw = _u(el - sh)
    lw = _u(wr - el)
    fb = _perp(lw, uw)
    rest = _u(_perp(Mt @ fm, uw))                     # a straight arm: its front as at rest on this trunk
    m = np.linalg.norm(fb)
    fw = _u(fb / (m or 1) * min(1.0, m / 0.35) + rest * max(0.0, 1 - m / 0.35))
    hw = sign * np.cross(uw, fw)
    c = 0.1 * THICK[0]
    lu = np.linalg.norm(el - sh) / np.linalg.norm(J['el'] - J['sh'])
    Mu = np.stack([uw * lu, fw * c, hw * c], 1) @ np.stack([um, fm, hm], 0)
    # the forearm: along elbow->wrist, the same hinge
    lm = fm_
    f2m = np.cross(hm, lm)
    f2w = sign * np.cross(hw, lw)                    # straight, it equals fw
    ll = np.linalg.norm(wr - el) / np.linalg.norm(J['wr'] - J['el'])
    Mf = np.stack([lw * ll, f2w * c, hw * c], 1) @ np.stack([lm, f2m, hm], 0)
    return (Mt, J['sh'], sh), (Mu, J['sh'], sh), (Mf, J['el'], el)


def pose(side, k):
    """The arm's points in the world (metres) and its triangles."""
    V, T, wu, wf, J = arm_mesh(side)
    (Mt, ot, wt_), (Mu, ou, wu_), (Mf, of, wf_) = _maps(side, k)
    Pt = (V - ot) @ Mt.T + wt_
    Pu = (V - ou) @ Mu.T + wu_
    Pf = (V - of) @ Mf.T + wf_
    s = np.maximum(wu + wf, 1e-9)                # the arm's own bones only (the trunk's pull made skin flaps
    W = (Pu * wu[:, None] + Pf * wf[:, None]) / s[:, None]      # when the arm is raised)
    return W, T


def draw(img, cam, k, side, skin, shoulder_px=None, outline=None):
    """The arm onto img (RGBA, full size). Returns the drawn box or None."""
    W, T = pose(side, k)
    sh, el, wr = (np.asarray(k[n + side], float) for n in ('sh', 'el', 'wr'))
    ss = img.width / 1080.0
    if shoulder_px is not None:
        # pin the shoulder to the flat trunk's: shift the points in the camera's picture plane, fully at the
        # shoulder, none from the elbow on
        cp, cr, cu, cf = (np.asarray(x, float) for x in (cam.pos, cam.r, cam.u, cam.f))
        p0 = np.array(cam.project(tuple(sh))[0], float)
        dpx = np.asarray(shoulder_px, float) - p0
        u = el - sh
        along = np.clip(((W - sh) @ u) / (u @ u), 0, 1)
        fall = (1 - along) ** 1.5
        depth = (W - cp) @ cf
        kwv = cam.focal / np.maximum(depth, cam.NEAR)
        W = W + (fall * dpx[0] / kwv)[:, None] * cr - (fall * dpx[1] / kwv)[:, None] * cu
    got = HF.paint(img, cam, W, T, skin, (sh + el) / 2, outline, CREASE, ss)
    if got is None:
        return None
    lay, (x0, y0), _ = got
    # the cut end fades into the drawn shoulder (the trunk's own shoulder line shows; no cut face on his back)
    p0 = np.array(cam.project(tuple(sh))[0], float) if shoulder_px is None else np.asarray(shoulder_px, float)
    p1 = np.array(cam.project(tuple(el))[0], float)
    dd = (p1 - p0) * ss
    n = np.linalg.norm(dd)
    if n > 4:
        a = np.asarray(lay.getchannel('A'), np.float32)
        yy, xx = np.mgrid[0:lay.height, 0:lay.width]
        along = ((xx + x0 - p0[0] * ss) * dd[0] + (yy + y0 - p0[1] * ss) * dd[1]) / (n * n)
        a *= np.clip((along - SHOULDER_FADE[0]) / (SHOULDER_FADE[1] - SHOULDER_FADE[0]), 0, 1)
        lay.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(lay, (x0, y0))
    return (x0, y0, x0 + lay.width, y0 + lay.height)


def _poses():
    import gta_cast as GC
    import leanout as LO
    sp = dict(GC.cast()['jason'])
    return [(t, LO.at(t, sp)) for t in (0.2, 1.3, 1.9, 4.2, 6.7, 7.15)]


def sheet(out, side='R', degs=range(0, 360, 45)):
    import sets as S
    rows = []
    for t, k in _poses():
        mid = (np.asarray(k['neck'], float) + k['pelvis']) / 2
        tiles = []
        for deg in degs:
            a = math.radians(deg)
            fw = _u(_perp(np.asarray(k['fwd'], float), np.array([0, 1.0, 0])))
            rt = np.cross(np.array([0, 1.0, 0]), fw)
            d = fw * math.cos(a) + rt * math.sin(a)
            cam = S.Cam(tuple(mid + d * 2.2 + np.array([0, 0.25, 0])), tuple(mid), focal=1000 * 2.2 / 1.2)
            im = Image.new('RGBA', (2160, 3840), (235, 230, 222, 255))
            for sd in ('L', 'R'):
                draw(im, cam, k, sd, (236, 196, 168))
            dr = ImageDraw.Draw(im)
            for n in ('neck', 'pelvis', 'shL', 'shR'):
                x, y = cam.project(tuple(k[n]))[0]
                dr.ellipse([x * 2 - 8, y * 2 - 8, x * 2 + 8, y * 2 + 8], fill=(40, 90, 200))
            a_, b_ = (np.array(cam.project(tuple(k[n]))[0]) * 2 for n in ('neck', 'pelvis'))
            dr.line([tuple(a_), tuple(b_)], fill=(40, 90, 200), width=6)
            tl = im.crop((180, 820, 1980, 2620)).convert('RGB').resize((300, 300), Image.LANCZOS)
            ImageDraw.Draw(tl).text((6, 6), f't{t} {deg}', fill=(0, 0, 0))
            tiles.append(tl)
        rows.append(tiles)
    sh = Image.new('RGB', (300 * len(rows[0]), 300 * len(rows)), 'white')
    for r, tiles in enumerate(rows):
        for i, tl in enumerate(tiles):
            sh.paste(tl, (i * 300, r * 300))
    sh.save(out, quality=88)


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
