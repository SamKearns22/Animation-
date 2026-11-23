#!/usr/bin/env python3
"""MAP  jason3d_film: the dressed 3D Jason (the bench move Sam approved, 23 Nov: "It looks very good") drawn INTO the
film: through the film's own camera and the moving Tulip, over the film's frame, in place of the flat Jason.

The pose is the bench's (bench_move: goals -> solved skin), the drawing is the bench's (bench_move.dressed_draw:
house colours, house ink, house head with its planned views, neck column, circle hands, the pistol with chat 43's
grip). Only two things are new here: every point goes from the car's frame to the world with the car (its place,
turn and lean, gta_cars body_pt), and only Jason's own dots (his body, hands, pistol and the ink round them) are kept
as a layer: the bench's car solids still hide him by depth, the film's car is what shows.

  pose_at(t) ........ the solved bench pose at shot 4's time t (shot 3, t < 0: K1 held, seated, pistol flat on
                      his chest); cached per process
  head_view(t) ...... the drawn head view at t (bench_move.head_plan over shot 4's 24 frames a second, the plan
                      of the clip Sam approved; shot 3 holds its first view); cached in HEAD_PLAN_FILE
  layer(img, cam, car, t, face) ... draws him over img (the film's canvas, any drawing scale); returns world joints
  flash ............. the muzzle flash on the shot's frame (leanout.flash's star, at the bench pistol's muzzle)

    python3 source/jason3d_film.py plan                  (re)write the head plan file
    python3 source/jason3d_film.py still T OUT.png       one film frame of shot 3/4 at shot 4's time T
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CHECK = [True]                    # check each shots 5-8 pose as drawn (FAULTS: (t, faults))
FAULTS = []
ON = [True]                       # the film draws this Jason in shots 3-4 (False: the old flat lean-out)
HEAD_PLAN_FILE = os.path.join(HERE, 'data', 'gta-jason3d-headplan.json')
FPS = 24
_POSE = {}


def _bm():
    import bench_move as BM
    if not _POSE.get('fit'):             # the seat, knee and ankle fits, as the bench run makes them first
        BM.fit_seat()
        BM.fit_knee()
        BM.fit_ankles()
        _POSE['fit'] = True
    return BM


def pose_at(t):
    """The bench pose at shot 4's time t (t < 0, shot 3: K1 as at t = 0)."""
    BM = _bm()
    tt = round(max(0.0, float(t)) * FPS) / FPS
    if tt not in _POSE:
        if len(_POSE) > 64:
            keep = {k: _POSE[k] for k in ('fit', 'plan') if k in _POSE}
            _POSE.clear()
            _POSE.update(keep)
        _POSE[tt] = BM.solve(BM.goals_at(tt))
    return _POSE[tt], tt


def _plan():
    if 'plan' in _POSE:
        return _POSE['plan']
    if os.path.exists(HEAD_PLAN_FILE):
        _POSE['plan'] = json.load(open(HEAD_PLAN_FILE))
        return _POSE['plan']
    return write_plan()


def write_plan():
    import gta_rehearse as GR
    BM = _bm()
    n = int(round(GR.SHOT4_LEN * FPS)) + 1
    ys = []
    for i in range(n):
        out, tt = pose_at(i / FPS)
        ys.append(float(BM.head_yaw(out, tt)))
    plan = [int(v) for v in BM.head_plan(ys)]
    os.makedirs(os.path.dirname(HEAD_PLAN_FILE), exist_ok=True)
    json.dump(plan, open(HEAD_PLAN_FILE, 'w'))
    _POSE['plan'] = plan
    return plan


def head_view(t):
    p = _plan()
    i = int(round(max(0.0, t) * FPS))
    return p[min(i, len(p) - 1)]


def _xf(car):
    """car frame -> world, as one affine map (gta_cars body_pt: the car's place, turn and lean)."""
    o = np.asarray(car.body_pt((0.0, 0.0, 0.0)), float)
    M = np.stack([np.asarray(car.body_pt(tuple(e)), float) - o for e in np.eye(3)], 1)
    return lambda P: np.asarray(P, float) @ M.T + o, M, o


def _muzzle(out):
    Pg = np.asarray(out['gun'][0], float)
    d = np.asarray(out['aim'], float)
    d = d / (np.linalg.norm(d) + 1e-12)
    return Pg[np.argmax(Pg @ d)], d


def flash(img, cam, muzzle, d, age):
    """leanout.flash's star at the bench pistol's muzzle (world points), on the canvas img."""
    import body as B
    import sets as S
    tip = muzzle + d * 0.03
    if cam.depth(tuple(tip)) <= cam.NEAR:
        return
    (X, Y), kk = cam.project(tuple(tip))
    (X2, Y2), _ = cam.project(tuple(tip + d * 0.3))
    ang = math.atan2(Y2 - Y, X2 - X)
    r = max(10.0, 0.16 * kk) * (1.0 - 0.35 * age / 0.042)
    p = B.Pen(img, S.FLAT)
    for col, f in (((255, 196, 70), 1.0), ((255, 248, 214), 0.5)):
        pts = []
        for i in range(10):
            a = ang + i * math.pi / 5
            rr = r * f * (1.0 if i % 2 == 0 else 0.45) * (1.6 if i == 0 else 1.0)
            pts.append((X + rr * math.cos(a), Y + rr * math.sin(a)))
        p.poly(pts, col, (40, 24, 10) if f == 1.0 else None, 2.0 if f == 1.0 else 0)


def pose_goals(g):
    """A solved pose from ready goals (shots 5-8: seated, the gun hand acting), cached by the goals' numbers."""
    BM = _bm()
    key = repr(sorted((k, repr(v)) for k, v in g.items()))
    if key not in _POSE:
        if len(_POSE) > 64:
            keep = {k: _POSE[k] for k in ('fit', 'plan') if k in _POSE}
            _POSE.clear()
            _POSE.update(keep)
        _POSE[key] = BM.solve(g)
    return _POSE[key]


def view_for(out, cam, car):
    """The drawn head view from the head's own turn against this camera (shots 5-8: no planned run)."""
    import lying_flat as LF
    BM = _bm()
    f, M, o = _xf(car)
    k = BM.house_pose(out)
    hup, hfwd = LF._unit(M @ k['hup']), LF._unit(M @ k['hfwd'])
    d = LF._unit(np.asarray(cam.pos, float) - f(np.asarray(k['head'], float)[None])[0])
    y = abs(float(LF.yaw_seen(d, LF._unit(np.cross(hup, hfwd)), hfwd)))
    return sorted(BM.VIEWS_DEG)[int(np.searchsorted(BM.HEAD_BOUNDS, y))]


def layer(img, cam, car, t, face=None, glass=None, scale=2, goals=None):
    """Jason at shot 4's time t (shot 3: t < 0) over img through the film's cam in the moving car. face: the house
    head's acting keys (mood, squint, mouth, blink, ...). glass: (mask 0..1 at img size, dim) for closed panes in
    front of him. Returns (alpha at img size, world joints)."""
    import body as B
    BM = _bm()
    if goals is None:
        out, tt = pose_at(t)
        hv = head_view(t)
    else:
        out, tt = pose_goals(goals), 0.0
        hv = view_for(out, cam, car)
        if CHECK[0]:                     # shots 5-8's seated acting is checked as it is drawn (the shot 4 move by
            c = BM.check_frame(out, goals)   # the bench run): into the car, into himself, the pistol, joint range
            bad = {k: v for k, v in c.items() if k in ('car', 'self', 'pistol', 'rom') and v}
            if bad:
                FAULTS.append((round(float(t), 3), bad))
    f, M, o = _xf(car)
    ss = B.SS
    B.SS = 1                                     # the bench draws at the frame's 1080 x 1920 (x scale inside)
    try:
        lay = BM.dressed_draw(out, tt, view='shot', scale=scale, head_vd=hv, cam=cam, xf=f,
                              face=face, car=car, layer=True)
    finally:
        B.SS = ss
    if lay.size != img.size:
        lay = lay.resize(img.size, Image.LANCZOS)
    al = np.asarray(lay.split()[3], np.float32)
    img.alpha_composite(lay)
    if glass is not None:
        import gta_cars as G
        gm, dim = glass
        img.alpha_composite(G.glass_tint(img.size, al * gm * dim))
    J = {n: f(np.asarray(v, float)[None])[0] for n, v in out['J'].items()}
    J['_gun_hand'] = f(np.asarray(out['balls']['R'], float)[None])[0]
    mz, d = _muzzle(out)
    J['_muzzle'], J['_aim'] = f(mz[None])[0], M @ d
    return al, J


def still(t, path):
    import gta_rehearse as GR
    if t < 0:
        im = GR.shot3(t + GR.SHOT3_LEN)
    else:
        im = GR.shot4(t)
    im.convert('RGB').resize((1080, 1920), Image.LANCZOS).save(path)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'plan':
        p = write_plan()
        print(len(p), 'frames; views', sorted(set(p)))
    elif a[0] == 'still':
        still(float(a[1]), a[2])
