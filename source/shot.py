#!/usr/bin/env python3
"""Rendering shots from their recipes.

A shot is a small recipe file in shots/ that says, for any moment t (seconds) of the shot, where the camera
is, how each character stands and moves, and where the props are: `frame(t)` returns a plain dictionary

    camera   dict(pos=, target=, vfov=)            metres and degrees
    mother   her spec (see mother.solve)
    board, ham, cleaver                            props (see props.py)
    focus    points the drawing should favour      (optional; defaults to her face, the blade, her hand)

This module builds the scene for a frame from the reusable parts - the kitchen (kitchen.py), the props
(props.py), the characters (mother.py) - checks it (checks.py), renders it and saves the passes the pencil
drawing needs (graphite.py).

For animation it only redraws what moves: the kitchen's shadows are made once per shot and only the moving
things are added to them each frame, and each frame renders only the part of the picture the moving things
can reach; the rest comes from the shot's first frame.

Usage:
    python3 shot.py still shots/s1_chop.py OUT_DIR [W H [T]]     one frame: passes + render + drawing
    python3 shot.py sequence shots/s1_chop.py OUT_DIR [W H]     the whole shot, drawn on twos
"""
import importlib.util
import os
import sys
import time

import numpy as np

import kitchen
import mother
import sdf3d as S
from materials import mat_table, new_params
from rig import unit

W_VIDEO, H_VIDEO = 1920, 1080


def load_recipe(path):
    spec = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(path))[0], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(frame):
    """The whole scene for one frame. Returns a dict with the renderer's inputs and what the checks and the
    drawing need to know."""
    t0 = time.time()
    state = mother.prepare(mother.solve(frame['mother']))
    b = S.Builder()
    mother.build(b, state)
    frame['board'].build(b)
    hand = mother.hand_parts()[1][0]
    o, R, _ = state['hands'][1]
    frame['ham'].build(b, press=(hand, o, R))
    frame['cleaver'].build(b)
    n_moving = len(b.groups)
    SP = new_params()
    mother.fill_params(SP, state)
    frame['ham'].fill_params(SP)
    SP[46:49] = (1.0, 0.0, 0.0)          # the board's grain runs along x
    flames = kitchen.build_environment(b, SP)
    P, G = b.build()
    GB = b.grid_buffer()
    print(f'  built in {time.time() - t0:.0f}s: {len(P)} shapes in {len(G)} objects', flush=True)
    return dict(frame=frame, state=state, P=P, G=G, GB=GB, SP=SP, flames=flames,
                moving=np.arange(n_moving), static=np.arange(n_moving, len(G)))


def shadows(scene, static_maps=None):
    """Shadow maps for a frame. static_maps: the set's own maps (made once per shot with shadows(..., None)
    on the static objects only); the moving objects are then drawn into them."""
    P, G, GB = scene['P'], scene['G'], scene['GB']
    focus = scene['frame'].get('shadow_focus', (0.0, 1.25, -0.55))
    sm = S.ShadowMaps()
    for i, (L, c, ext, res, tan, bias) in enumerate(kitchen.shadow_maps(focus)):
        if static_maps is None:
            sm.add(P, G, GB, L, c, ext, res, tan, bias=bias)
        else:
            sm.add(P, G[scene['moving']], GB, L, c, ext, res, tan, bias=bias, base=static_maps[i])
    return sm


def static_shadows(scene):
    """The set's shadows alone (everything that never moves), to reuse for every frame of a shot - and kept
    on disk, so they are made once for as long as the set and the lights stay the same."""
    import hashlib
    import pickle
    from cache import CACHE_DIR
    P, G, GB = scene['P'], scene['G'], scene['GB']
    st = scene['static']
    rows = np.concatenate([P[int(G[i, 4]):int(G[i, 5])].ravel() for i in st])
    h = hashlib.sha1(rows.tobytes() + G[st].tobytes() + repr(kitchen.shadow_maps(
        scene['frame'].get('shadow_focus', (0.0, 1.25, -0.55)))).encode()).hexdigest()[:12]
    path = os.path.join(CACHE_DIR, f'setshadows_{h}.pkl')
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    maps = _static_shadows(scene)
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(maps, f, protocol=4)
    return maps


def _static_shadows(scene):
    P, G, GB = scene['P'], scene['G'], scene['GB']
    focus = scene['frame'].get('shadow_focus', (0.0, 1.25, -0.55))
    maps = []
    for (L, c, ext, res, tan, bias) in kitchen.shadow_maps(focus):
        sm = S.ShadowMaps()
        sm.add(P, G[scene['static']], GB, L, c, ext, res, tan, bias=bias)
        maps.append(sm.maps[0])
    return maps


def camera(frame, W, H):
    c = frame['camera']
    return S.camera(tuple(c['pos']), tuple(c['target']), c['vfov'], W / H)


def project(cam, W, H, p):
    """Pixel position of world points."""
    o, f, r, u = cam[0:3], cam[3:6], cam[6:9], cam[9:12]
    th, aspect = cam[12], cam[13]
    d = np.atleast_2d(p) - o
    z = d @ f
    x = (d @ r) / (z * th * aspect)
    y = (d @ u) / (z * th)
    return np.stack([(x + 1) * 0.5 * W, (1 - y) * 0.5 * H], 1)


def moving_box(scene, cam, W, H, margin=40):
    """The part of the picture the moving things can change: what they cover (their bounding spheres), where
    their shadows fall (followed from each thing along the sun and the back light down to the worktop), plus
    a margin for soft edges. (x0, y0, x1, y1)."""
    G = scene['G'][scene['moving']]
    pts = []
    top = kitchen.ISLAND['top']
    for c, r in zip(G[:, 0:3], G[:, 3]):
        centres = [c]
        I = kitchen.ISLAND
        for L in (kitchen.KEY, kitchen.RIM):
            if L[1] > 0 and c[1] > top:
                q = c - L * (c[1] - top) / L[1]          # where its shadow meets the worktop
                if I['x0'] - r < q[0] < I['x1'] + r and I['z0'] - r < q[2] < I['z1'] + r:
                    centres.append(q)
        for cc in centres:
            for dv in np.vstack([np.eye(3), -np.eye(3)]):
                pts.append(cc + dv * r)
    xy = project(cam, W, H, np.array(pts))
    x0, y0 = np.floor(xy.min(0)).astype(int) - margin
    x1, y1 = np.ceil(xy.max(0)).astype(int) + margin
    return max(0, x0), max(0, y0), min(W, x1), min(H, y1)


def drawing_passes(scene, res, cam, W, H):
    """What the pencil needs besides the render: which way the hair runs and the knit's ribs run at each
    pixel (3D directions), where the eye should go, and the blade's direction."""
    st = scene['state']
    pos, mat = res['pos'], res['mat']
    import materials as MT
    hair = mat == MT.HAIR
    knit = mat == MT.KNIT
    hairdir = np.zeros(pos.shape, np.float16)
    hairdir[..., 1] = -1
    lo, d, vox, flow = st['hair']
    if hair.any():
        idx = np.clip(np.round((pos[hair] - lo) / vox).astype(int), 0, np.array(flow.shape[:3]) - 1)
        f = flow[idx[:, 0], idx[:, 1], idx[:, 2]]
        for off in ((0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0)):
            miss = np.linalg.norm(f, axis=1) < 0.5
            if not miss.any():
                break
            j = np.clip(idx + off, 0, np.array(flow.shape[:3]) - 1)
            f[miss] = flow[j[miss, 0], j[miss, 1], j[miss, 2]]
        f[np.linalg.norm(f, axis=1) < 0.5] = (0, -1, 0)
        hairdir[hair] = f
    # the knit: up the body; along the sleeves (which part is which comes from the jumper's own part map)
    knitdir = np.zeros(pos.shape, np.float16)
    knitdir[..., 1] = 1
    lo, d, vox, part = st['jumper']
    J = st['joints']
    if knit.any():
        idx = np.clip(np.round((pos[knit] - lo) / vox).astype(int), 0, np.array(part.shape) - 1)
        pid = part[idx[:, 0], idx[:, 1], idx[:, 2]].round().astype(int)
        p = pos[knit]
        dirs = np.tile(np.array([0, 1.0, 0]), (len(p), 1))
        for k, s in ((1, 'R'), (2, 'L')):
            segs = ((J['shoulder.' + s], J['elbow.' + s]), (J['elbow.' + s], J['wrist.' + s]))
            best = np.full(len(p), 1e9)
            for a, b_ in segs:
                ba = b_ - a
                h = np.clip(((p - a) @ ba) / (ba @ ba), 0, 1)
                dist = np.linalg.norm(p - (a + h[:, None] * ba), axis=1)
                sel = (pid == k) & (dist < best)
                dirs[sel] = unit(ba)
                best = np.where(sel, dist, best)
        knitdir[knit] = dirs
    fr = scene['frame']
    cl = fr['cleaver']
    focus = fr.get('focus', [st['head'][0], cl.o + cl.R @ np.array([0.03, 0.04, 0]), st['hands'][1][0]])
    return dict(hairdir=hairdir, knitdir=knitdir, focus=np.array(focus, float), bladedir=unit(cl.x))


def render(scene, W, H, sm=None, crop=None, verbose=True):
    t0 = time.time()
    if sm is None:
        sm = shadows(scene)
        print(f'  shadows {time.time() - t0:.0f}s', flush=True)
    SM, SMP = sm.arrays()
    Lt = kitchen.light_rows(scene['flames'])
    cam = camera(scene['frame'], W, H)
    res = S.render_image(W, H, cam, scene['P'], scene['G'], mat_table(), Lt, scene['SP'], scene['GB'], SM, SMP,
                         bands=8, crop=crop, verbose=verbose)
    print(f'  rendered {time.time() - t0:.0f}s', flush=True)
    return res, cam


def save_passes(path, res, cam, scene, W, H):
    extra = drawing_passes(scene, res, cam, W, H)
    np.savez_compressed(path, cam=cam, SP=scene['SP'], **res, **extra)


def sequence(recipe_path, out_dir, W=W_VIDEO, H=H_VIDEO, fps=24, every=2, times=None):
    """Render a shot as a numbered series of drawings (one every `every` frames: on twos by default).
    The first is rendered and drawn whole; after that only the part of the picture the moving things can
    reach is rendered and redrawn, and pasted over the first. The set's shadows are made once."""
    import json
    import checks
    import graphite
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    rec = load_recipe(recipe_path)
    if times is None:
        times = np.arange(0, rec.DURATION - 1e-9, every / fps)
    log = []
    t_all = time.time()
    base = static = stats = box0 = None
    for n, t in enumerate(times):
        t0 = time.time()
        scene = build(rec.frame(float(t)))
        checks.run(scene, verbose=False)
        if static is None:
            static = static_shadows(scene)
            print(f'  shadows of the set {time.time() - t0:.0f}s', flush=True)
        t1 = time.time()
        sm = shadows(scene, static)
        print(f'  shadows {time.time() - t1:.0f}s', flush=True)
        cam = camera(scene['frame'], W, H)
        box = moving_box(scene, cam, W, H)
        if box0 is None:
            box0, crop = box, None
        else:
            crop = (min(box[0], box0[0]), min(box[1], box0[1]), max(box[2], box0[2]), max(box[3], box0[3]))
        res, cam = render(scene, W, H, sm, crop=crop, verbose=False)
        if base is None:
            base = res
        else:
            x0, y0, x1, y1 = crop
            full = {k: v.copy() for k, v in base.items()}
            for k in full:
                full[k][y0:y1, x0:x1] = res[k][y0:y1, x0:x1]
            res = full
        passes = os.path.join(out_dir, f'passes_{n:04d}.npz')
        save_passes(passes, res, cam, scene, W, H)
        out = os.path.join(out_dir, f'draw_{n:04d}.png')
        if crop is None:
            stats = graphite.draw(passes, out)
            first = np.asarray(Image.open(out))
        else:
            m = 64                                       # redraw a little beyond, paste the inside
            x0, y0, x1, y1 = crop
            wx0, wy0, wx1, wy1 = max(0, x0 - m), max(0, y0 - m), min(W, x1 + m), min(H, y1 + m)
            patch = os.path.join(out_dir, 'patch.png')
            graphite.draw(passes, patch, crop=(wx0, wy0, wx1, wy1), stats=stats)
            img = first.copy()
            img[y0:y1, x0:x1] = np.asarray(Image.open(patch))[y0 - wy0:y1 - wy0, x0 - wx0:x1 - wx0]
            Image.fromarray(img).save(out, optimize=True)
            os.remove(patch)
        dt = time.time() - t0
        log.append(dict(n=n, t=float(t), seconds=round(dt, 1), crop=crop))
        print(f'drawing {n} (t={t:.3f}s) done in {dt:.0f}s, window {crop}', flush=True)
    with open(os.path.join(out_dir, 'log.json'), 'w') as f:
        json.dump(log, f, indent=1)
    print(f'{len(times)} drawings in {time.time() - t_all:.0f}s', flush=True)


def still(recipe_path, out_dir, W=W_VIDEO, H=H_VIDEO, t=0.0):
    import checks
    from PIL import Image
    import graphite
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    frame = load_recipe(recipe_path).frame(t)
    scene = build(frame)
    checks.run(scene)
    res, cam = render(scene, W, H)
    passes = os.path.join(out_dir, 'passes.npz')
    save_passes(passes, res, cam, scene, W, H)
    Image.fromarray((S.tonemap(res['rgb'], 1.05) * 255).astype(np.uint8)).save(os.path.join(out_dir, 'render.png'))
    graphite.draw(passes, os.path.join(out_dir, 'draw.png'))
    print(f'done in {time.time() - t0:.0f}s', flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'sequence':
        sequence(a[1], a[2], *(int(v) for v in a[3:5]))
    if a[0] == 'still':
        still(a[1], a[2], *(int(v) for v in a[3:5]), *(float(v) for v in a[5:6]))
