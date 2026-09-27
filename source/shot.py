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
    drawing need to know. A frame may have the mother, the daughter or both; with pov=True the camera is the
    mother's eyes (her head and hair are left out)."""
    t0 = time.time()
    b = S.Builder()
    chars = {}
    if 'mother' in frame:
        st = mother.prepare(mother.solve(frame['mother']))
        mother.build(b, st, pov=frame.get('pov', False))
        chars['mother'] = st
    if 'daughter' in frame:
        import daughter
        sd = daughter.prepare(daughter.solve(frame['daughter']))
        daughter.build(b, sd)
        chars['daughter'] = sd
    press = None
    if 'mother' in chars:
        o, R, _ = chars['mother']['hands'][1]
        press = (mother.hand_parts()[1][0], o, R)
    frame['ham'].build(b, press=press)
    frame['cleaver'].build(b)
    n_moving = len(b.groups)
    frame['board'].build(b)                  # the board stays put: part of the set
    for extra in frame.get('extras', ()):     # other things on the set (the plate of tartlets...)
        extra.build(b)
    SP = new_params()
    face = frame.get('face', 'mother')
    if face == 'daughter':
        import daughter
        daughter.fill_params(SP, chars['daughter'])
    elif 'mother' in chars:
        mother.fill_params(SP, chars['mother'])
    frame['ham'].fill_params(SP)
    SP[46:49] = (1.0, 0.0, 0.0)          # the board's grain runs along x
    flames = kitchen.build_environment(b, SP, front=frame.get('front_wall', False))
    P, G = b.build()
    GB = b.grid_buffer()
    print(f'  built in {time.time() - t0:.0f}s: {len(P)} shapes in {len(G)} objects', flush=True)
    return dict(frame=frame, state=chars.get('mother'), chars=chars, P=P, G=G, GB=GB, SP=SP, flames=flames,
                group_names=[g['name'] for g in b.groups],
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
            sm.add(P, G[scene['moving']], GB, L, c, ext, res, tan, bias=bias, base=static_maps[i],
                   within=moving_corners(scene))
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


def solid_box(grid, o=None, R=None, pad=0.01):
    """A tight world box round the solid part of a grid (optionally in a frame o, R)."""
    lo, d, vox = grid[0], grid[1], grid[2]
    idx = np.argwhere(d[::2, ::2, ::2] < 0)
    if not len(idx):
        return None
    a, b = lo + idx.min(0) * 2 * vox - pad, lo + idx.max(0) * 2 * vox + pad
    if R is None:
        return a, b
    corners = np.array([[x, y, z] for x in (a[0], b[0]) for y in (a[1], b[1]) for z in (a[2], b[2])])
    w = corners @ np.asarray(R).T + o
    return w.min(0), w.max(0)


def moving_corners(scene):
    """Corners of tight boxes round everything that moves: the characters' pieces and the props."""
    boxes = []
    for name, st in scene['chars'].items():
        mod = mother if name == 'mother' else __import__('daughter')
        boxes += [bx for bx in (solid_box(*pc) for pc in mod.pieces(st, pov=scene['frame'].get('pov', False)
                                                                    and name == 'mother')) if bx is not None]
    names, G = scene['group_names'], scene['G']
    for i in scene['moving']:
        if names[i] in ('ham', 'frill', 'garnish', 'cleaver') or names[i].startswith('slice'):
            boxes.append((G[i, 0:3] - G[i, 3], G[i, 0:3] + G[i, 3]))
    return np.array([[x, y, z] for a, b_ in boxes for x in (a[0], b_[0]) for y in (a[1], b_[1])
                     for z in (a[2], b_[2])])


def merge_spans(spans, rows=32):
    """Join row pieces into rectangles (fewer, larger calls to the renderer): a piece joins the rectangle
    above it when their columns overlap and the rectangle is not yet `rows` tall."""
    rects = []
    for y0, y1, x0, x1 in sorted(spans):
        for i, (a0, a1, b0, b1) in enumerate(rects):
            if a1 >= y0 and x0 <= b1 and x1 >= b0 and y1 - a0 <= rows:
                rects[i] = (a0, max(a1, y1), min(b0, x0), max(b1, x1))
                break
        else:
            rects.append((y0, y1, x0, x1))
    return rects


def changed_rows(lo_now, lo_ref, W, H, thresh=0.01, grow=3):
    """Where a quick quarter-size render differs from the shot's first frame (by more than would show in
    pencil): for each quarter-size row, the runs of columns to redo. Grown a little all round."""
    from scipy import ndimage
    d = np.abs(lo_now - lo_ref).max(-1) > thresh
    d = ndimage.binary_dilation(d, iterations=grow)
    h, w = d.shape
    sx, sy = W / w, H / h
    spans = []
    for j in range(h):
        row = np.concatenate([[False], d[j], [False]])
        edges = np.nonzero(np.diff(row.astype(np.int8)))[0]
        for a, b in zip(edges[::2], edges[1::2]):
            spans.append((int(j * sy), int(min(H, (j + 1) * sy)), int(a * sx), int(min(W, b * sx))))
    return spans


def drawing_passes(scene, res, cam, W, H):
    """What the pencil needs besides the render: which way the hair runs and the knit's ribs run at each
    pixel (3D directions), where the eye should go, and the blade's direction."""
    import materials as MT
    pos, mat = res['pos'], res['mat']
    hairdir = np.zeros(pos.shape, np.float16)
    hairdir[..., 1] = -1
    for name, st in scene['chars'].items():
        hm = MT.HAIR if name == 'mother' else MT.STRAW_HAIR
        hair = mat == hm
        if not hair.any():
            continue
        lo, d, vox, flow = st['hair']
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
    knit = mat == MT.KNIT
    st = scene['chars'].get('mother')
    if st is not None and knit.any():
        lo, d, vox, part = st['jumper']
        J = st['joints']
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
    if 'focus' in fr:
        focus = fr['focus']
    else:
        focus = [st['head'][0], cl.o + cl.R @ np.array([0.03, 0.04, 0]), st['hands'][1][0]]
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
        times = getattr(rec, 'TIMES', None)          # a recipe may choose its drawings (fast action on ones)
        if times is None:
            times = np.arange(0, rec.DURATION - 1e-9, every / fps)
    log = []
    t_all = time.time()
    base = static = stats = lo_ref = first = None
    M = mat_table()
    for n, t in enumerate(times):
        t0 = time.time()
        scene = build(rec.frame(float(t)))
        checks.run(scene, verbose=False)
        if static is None:
            static = static_shadows(scene)
            print(f'  shadows of the set {time.time() - t0:.0f}s', flush=True)
        t1 = time.time()
        sm = shadows(scene, static)
        SM, SMP = sm.arrays()
        Lt = kitchen.light_rows(scene['flames'])
        print(f'  shadows {time.time() - t1:.0f}s', flush=True)
        cam = camera(scene['frame'], W, H)
        # a quick quarter-size render first: where does this frame differ from the first?
        t1 = time.time()
        lo = S.render_image(W // 4, H // 4, camera(scene['frame'], W // 4, H // 4), scene['P'], scene['G'], M, Lt,
                            scene['SP'], scene['GB'], SM, SMP, bands=4, verbose=False)['rgb']
        if base is None:
            lo_ref = lo
            res, cam = render(scene, W, H, sm, verbose=False)
            base, spans = res, None
        else:
            spans = changed_rows(lo, lo_ref, W, H)
            res = {k: v.copy() for k, v in base.items()}
            for y0, y1, x0, x1 in merge_spans(spans):
                S.render(W, H, cam, scene['P'], scene['G'], scene['GB'], M, Lt, scene['SP'], SM, SMP, res['rgb'],
                         res['depth'], res['normal'], res['mat'], res['pos'], res['glass'], y0, y1, x0, x1)
        print(f'  rendered {time.time() - t1:.0f}s', flush=True)
        passes = os.path.join(out_dir, f'passes_{n:04d}.npz')
        save_passes(passes, res, cam, scene, W, H)
        out = os.path.join(out_dir, f'draw_{n:04d}.png')
        box = None
        if spans is None:
            stats = graphite.draw(passes, out)
            first = np.asarray(Image.open(out))
        elif not spans:
            Image.fromarray(first).save(out, optimize=True)      # nothing moved
        else:
            m = 64                                       # redraw a little beyond, paste the inside
            y0, y1 = min(sp[0] for sp in spans), max(sp[1] for sp in spans)
            x0, x1 = min(sp[2] for sp in spans), max(sp[3] for sp in spans)
            box = (x0, y0, x1, y1)
            wx0, wy0, wx1, wy1 = max(0, x0 - m), max(0, y0 - m), min(W, x1 + m), min(H, y1 + m)
            patch = os.path.join(out_dir, 'patch.png')
            graphite.draw(passes, patch, crop=(wx0, wy0, wx1, wy1), stats=stats)
            img = first.copy()
            img[y0:y1, x0:x1] = np.asarray(Image.open(patch))[y0 - wy0:y1 - wy0, x0 - wx0:x1 - wx0]
            Image.fromarray(img).save(out, optimize=True)
            os.remove(patch)
        dt = time.time() - t0
        area = 0 if spans is None else sum((y1 - y0) * (x1 - x0) for y0, y1, x0, x1 in spans) / (W * H)
        log.append(dict(n=n, t=float(t), seconds=round(dt, 1), redrawn=round(area, 3), box=box))
        print(f'drawing {n} (t={t:.3f}s) done in {dt:.0f}s, {area * 100:.0f}% of the picture re-rendered',
              flush=True)
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
