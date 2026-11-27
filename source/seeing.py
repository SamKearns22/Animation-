#!/usr/bin/env python3
"""seeing: four more ways of looking at a moving span, beside the plain frames (proposal seeing-five-candidates,
option 1; Sam's Y 26 Nov: "1. Y but lose option 5"). Each view is ADVICE only (rule 93): it prints and draws, it
never stops a render or a send.

  1 whereis  a "who is where" copy drawn by our own engine: every layer the film paints (each person, each arm and
             head where the people kit draws them, each set piece) is one flat colour, painted in the film's own
             drawing order, so who is in front and what touches what comes from the drawing, not a guess. Printed:
             a layer that vanishes or pops mid-shot away from the frame's edge, and two people whose front/behind order
             flips. Needs the film's code (any commit's copy of source/).
  2 motion   frame-to-frame movement measured on the finished pictures (OpenCV's DIS optical flow): colour = which
             way and how far each part moved since the last frame; red boxes = what the movement cannot explain
             (something appeared or vanished); a graph of the fastest movement per frame. Printed: jumps, appearances.
  3 cutout   a picture cut-out model on the finished pictures (MediaPipe's multiclass person segmenter: hair, skin,
             clothes; and u2netp, a small general "main object" cut-out, run through onnxruntime). Printed: how many
             separate people it finds per frame and when that changes.
  4 pose     a body-pose finder on the finished pictures (MediaPipe pose landmarker, full model, and its hand
             landmarker): skeletons, and the wrists' paths through the span. Printed: people found per frame, wrist
             jumps.

MAP
  models 70 ....... URLS, model(name): fetched once into source/models/ (not on GitHub; like likeness.py)
  render 90 ....... frames(src, film, t0, t1, out): every frame of the span from the film's code in `src` (a copy of
                    source/ at any commit, or this one), the clean picture and its layers: cover's recorder (films
                    drawn through places/views/cover) plus an item wrapper for films that paint a sorted list of
                    (name, depth, draw) items (Grand Theft Autism's street)
  1 whereis 260 ... whereis(case): flat-colour copies and their events
  2 motion 340 .... motion(case): flow pictures, the graph, events; truth(case): the flow beside the layers' own
                    movement (how true the measure is, for the test; never shown to a judge)
  3 cutout 430 .... cutout(case)
  4 pose 480 ...... pose(case)
  5 watch ......... watch(case): every frame in order, 8 to a sheet, each person outlined (outline_image); the
                    "watch the clip" test (Sam's Y 27 Nov): the model sees pictures, not video, so this is the
                    nearest honest thing to watching
  sheet 560 ....... sheet(case, view): 6 frames across the span, the plain frame left, the view right (view 'plain':
                    the plain frames only); the printed events beside it (case/VIEW.txt)

    python3 source/seeing.py render CASE_DIR --film MODULE --span T0 T1 [--src DIR]
    python3 source/seeing.py views CASE_DIR [plain whereis motion cutout pose]
    python3 source/seeing.py watch CASE_DIR                 every frame, 8 to a sheet, people outlined
    python3 source/seeing.py clip FILM T0 T1 OUT_DIR       render with this copy's code, then every view and sheet
"""
import builtins
import colorsys
import contextlib
import glob
import hashlib
import json
import math
import os
import sys
import urllib.request

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, 'models')
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
W, H = 540, 960                 # every view is worked at half the film's size (1080 x 1920)
URLS = {
    'pose_landmarker_full.task': 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task',
    'hand_landmarker.task': 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task',
    'selfie_multiclass.tflite': 'https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite',
    'u2netp.onnx': 'https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2netp.onnx',
}
CUT = 25.0                      # mean grey change (0-255) between two frames above which it is a cut, not movement


# ---------------------------------------------------------------------------------------------- models
def model(name):
    p = os.path.join(MODELS, name)
    if not os.path.exists(p):
        os.makedirs(MODELS, exist_ok=True)
        urllib.request.urlretrieve(URLS[name], p + '.part')
        os.replace(p + '.part', p)
    return p


def _font(n):
    try:
        return ImageFont.truetype(FONT, n)
    except OSError:
        return ImageFont.load_default()


# ---------------------------------------------------------------------------------------------- render
class _Rec:
    """The item wrapper's record: each wrapped draw call's painted pixels, in the order they finish."""
    def __init__(self):
        self.items = []
        self.stack = []


REC = [None]


def _mask_small(diff_mask, box, size):
    """A painted mask (box crop at `size`) as a W x H bool map (a cell counts when a third of it was painted)."""
    full = np.zeros((size[1], size[0]), np.float32)
    x0, y0 = box[0], box[1]
    full[y0:y0 + diff_mask.shape[0], x0:x0 + diff_mask.shape[1]] = diff_mask
    im = Image.fromarray((full * 255).astype(np.uint8)).resize((W, H), Image.BOX)
    return np.asarray(im) > 85


def _painted(before, img):
    d = ImageChops.difference(img.convert('RGB'), before.convert('RGB'))
    bb = d.getbbox()
    if not bb:
        return None
    m = np.asarray(d.crop(bb)).max(-1) > 8
    return (bb, m) if m.any() else None


def _wrapped(fn, name, depth=None):
    """fn drawn as one recorded layer (its first argument is the picture it paints on)."""
    if getattr(fn, '_seeing', False):
        return fn

    def run(*a, **k):
        r = REC[0]
        if r is None or not a or not isinstance(a[0], Image.Image):
            return fn(*a, **k)
        img = a[0]
        before = img.copy()
        me = dict(name=name, depth=depth, kids=[])
        r.stack.append(me)
        try:
            return fn(*a, **k)
        finally:
            r.stack.pop()
            got = _painted(before, img)
            if got:
                m = _mask_small(got[1], got[0], img.size)
                for kd in me['kids']:
                    m &= ~kd['mask']               # a layer holding layers: only its own pixels
                me['mask'] = m
                r.items.append(me)
                if r.stack:
                    r.stack[-1]['kids'].append(me)
    run._seeing = True
    return run


def _sorted(it, *a, **k):
    out = builtins.sorted(it, *a, **k)
    if REC[0] is not None and out and all(isinstance(e, tuple) and len(e) >= 3 and callable(e[2])
                                          and isinstance(e[0], str) for e in out):
        out = [(e[0], e[1], _wrapped(e[2], e[0], e[1] if isinstance(e[1], (int, float)) else None)) + tuple(e[3:])
               for e in out]
    return out


# draw functions painted as their own layer wherever a film module has them (first argument: the picture)
WRAP_FNS = {'jason_layer': 'jason', 'shop_block': 'shop block', 'strip_ground': 'ground', 'hydrant_stump': 'hydrant'}


def _install(mods):
    for m in mods:
        if hasattr(m, 'world4') or hasattr(m, 'shot_fn'):          # films that paint a sorted item list
            m.sorted = _sorted
        for fn, label in WRAP_FNS.items():
            if callable(getattr(m, fn, None)):
                setattr(m, fn, _wrapped(getattr(m, fn), label))


def _pic_fn(F):
    for n in ('picture', 'frame_image', 'frame'):
        if callable(getattr(F, n, None)):
            return getattr(F, n)
    raise SystemExit(f'{F.__name__}: no picture(t) / frame_image(t)')


def frames(src, film, t0, t1, out, fps=None):
    """Draw every frame of [t0, t1) with the film code in `src`; save out/frames/NNN.png (W x H) and
    out/layers/NNN.npz (ids: the visible layer per pixel, -1 none; painted: each layer's own mask, packed)."""
    src = os.path.abspath(src)
    if HERE in sys.path and src != HERE:
        sys.path.remove(HERE)                  # the film's own copy of the kit, never this one
    sys.path.insert(0, src)
    os.chdir(src)
    import importlib
    F = importlib.import_module(film)
    try:
        cover = importlib.import_module('cover')
    except ImportError:
        cover = None
    _install([m for m in list(sys.modules.values()) if getattr(m, '__file__', None)
              and os.path.abspath(m.__file__).startswith(src)])
    pic = _pic_fn(F)
    fps = fps or getattr(F, 'FPS', 12)
    os.makedirs(os.path.join(out, 'frames'), exist_ok=True)
    os.makedirs(os.path.join(out, 'layers'), exist_ok=True)
    n = int(round((t1 - t0) * fps))
    meta = dict(film=film, src=src, t0=t0, t1=t1, fps=fps, times=[])
    for i in range(n):
        t = round(t0 + i / fps, 4)
        REC[0] = _Rec()
        if cover is not None and hasattr(cover, 'begin'):
            cover.begin('cover')
        try:
            img = pic(t)
        finally:
            crec = cover.end() if cover is not None and hasattr(cover, 'end') and cover.recording() else None
            wrec = REC[0]
            REC[0] = None
        img.convert('RGB').resize((W, H), Image.LANCZOS).save(os.path.join(out, 'frames', f'{i:03d}.png'))
        layers = []
        if crec is not None:
            for it in crec.items:
                m = _mask_small(it['mask'], it['box'], it['size'])
                if m.any():
                    layers.append(dict(name=it['name'], owner=it.get('owner') or it['name'],
                                       kind=it.get('kind', ''), depth=float(np.mean(it['rng'])) if it.get('rng') else None,
                                       mask=m))
        for it in wrec.items:
            layers.append(dict(name=it['name'], owner=it['name'], kind='item', depth=it['depth'], mask=it['mask']))
        _save_layers(os.path.join(out, 'layers', f'{i:03d}.npz'), layers)
        meta['times'].append(t)
        print(f'{t:.3f}s: {len(layers)} layers', flush=True)
    with open(os.path.join(out, 'meta.json'), 'w') as fh:
        json.dump(meta, fh)
    return meta


def _save_layers(path, layers):
    ids = np.full((H, W), -1, np.int16)
    for k, L in enumerate(layers):            # painted in drawing order: what was painted last is in front
        ids[L['mask']] = k
    np.savez_compressed(path, ids=ids, painted=np.packbits(np.stack([L['mask'] for L in layers]) if layers
                                                             else np.zeros((0, H, W), bool), axis=-1),
                        meta=json.dumps([{k: v for k, v in L.items() if k != 'mask'} for L in layers]))


def load_layers(path):
    z = np.load(path)
    meta = json.loads(str(z['meta']))
    painted = np.unpackbits(z['painted'], axis=-1)[..., :W].astype(bool) if len(meta) else np.zeros((0, H, W), bool)
    return z['ids'], painted, meta


def case_frames(case):
    meta = json.load(open(os.path.join(case, 'meta.json')))
    fr = sorted(glob.glob(os.path.join(case, 'frames', '*.png')))
    return meta, fr


# ---------------------------------------------------------------------------------------------- 1 whereis
def _is_person(L):
    n = L['name'].lower()
    return L.get('kind') == 'person' or n.startswith('person') or any(w in n for w in (
        'jason', 'wolf', 'guest', 'worker', 'kemi', 'may', 'blair', 'tony', 'man ', 'woman', 'cop', 'lucia'))


def _colour(L):
    h = int(hashlib.md5(L['owner'].encode()).hexdigest()[:6], 16)
    if _is_person(L):
        hue = (h % 360) / 360.0
        n = L['name']
        v, s = 0.95, 0.85
        if 'head' in n:
            v, s = 1.0, 0.45
        elif 'arm' in n:
            hue, v = (hue + 0.08) % 1, 0.65
        r, g, b = colorsys.hsv_to_rgb(hue, s, v)
    else:
        g0 = 0.55 + (h % 30) / 100.0
        r, g, b = g0, g0, g0 * 1.04
    return tuple(int(c * 255) for c in (r, g, min(1, b)))


def whereis_image(frame_png, layers_npz):
    ids, painted, meta = load_layers(layers_npz)
    base = np.asarray(Image.open(frame_png).convert('L').convert('RGB'), np.float32) * 0.35 + 150
    out = base.astype(np.uint8)
    for k, L in enumerate(meta):
        out[ids == k] = _colour(L)
    im = Image.fromarray(out)
    d = ImageDraw.Draw(im)                     # each person layer's name at its visible middle
    f = _font(13)
    seen = set()
    for k, L in enumerate(meta):
        if not _is_person(L) or L['owner'] in seen:
            continue
        ys, xs = np.nonzero(np.isin(ids, [j for j, M in enumerate(meta) if M['owner'] == L['owner']]))
        if len(xs) > 60:
            seen.add(L['owner'])
            d.text((int(xs.mean()) - 20, int(ys.mean())), L['owner'][:14], fill=(0, 0, 0), font=f)
    return im


def _edge(m, pad=4):
    return m[:pad].any() or m[-pad:].any() or m[:, :pad].any() or m[:, -pad:].any()


def whereis_events(case):
    meta, fr = case_frames(case)
    T = meta['times']
    rows = []
    prev = None
    grey_prev = None
    for i, f in enumerate(fr):
        ids, painted, lm = load_layers(os.path.join(case, 'layers', f'{i:03d}.npz'))
        g = np.asarray(Image.open(f).convert('L'), np.float32)
        cut = grey_prev is not None and np.abs(g - grey_prev).mean() > CUT
        grey_prev = g
        own = {}
        for k, L in enumerate(lm):
            if not _is_person(L):
                continue
            o = own.setdefault(L['owner'], dict(vis=0, painted=np.zeros((H, W), bool), order=k))
            o['vis'] += int((ids == k).sum())
            o['painted'] |= painted[k]
            o['order'] = max(o['order'], k)
        if prev is not None and not cut:
            for o, a in prev.items():
                if o not in own or own[o]['vis'] == 0:
                    if a['vis'] > 150 and not _edge(a['painted']):
                        rows.append((T[i], f'{o} vanished mid-frame (had {a["vis"]} px, not at the edge)'))
            for o, b in own.items():
                if (o not in prev or prev[o]['vis'] == 0) and b['vis'] > 150 and not _edge(b['painted']):
                    rows.append((T[i], f'{o} appeared mid-frame ({b["vis"]} px, not from the edge)'))
            names = sorted(own)
            for x in range(len(names)):
                for y in range(x + 1, len(names)):
                    a, b = names[x], names[y]
                    if a not in prev or b not in prev:
                        continue
                    ov = (own[a]['painted'] & own[b]['painted']).sum()
                    ovp = (prev[a]['painted'] & prev[b]['painted']).sum()
                    if ov > 40 and ovp > 40:
                        front, frontp = own[a]['order'] > own[b]['order'], prev[a]['order'] > prev[b]['order']
                        if front != frontp:
                            rows.append((T[i], f'{a} and {b} swap front/behind while overlapping ({ov} px)'))
        prev = own
    return rows


# ---------------------------------------------------------------------------------------------- 2 motion
def _grey(f):
    return np.asarray(Image.open(f).convert('L'))


def flows(case):
    import cv2
    meta, fr = case_frames(case)
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    out = []
    for i in range(1, len(fr)):
        a, b = _grey(fr[i - 1]), _grey(fr[i])
        cut = np.abs(a.astype(np.float32) - b).mean() > CUT
        fwd = dis.calc(a, b, None)
        back = dis.calc(b, a, None)
        out.append(dict(i=i, cut=cut, fwd=fwd, back=back))
    return meta, fr, out


def _residual(fa, fb, back):
    """What the movement cannot explain: the earlier frame moved along the flow, compared with the later one."""
    import cv2
    A = np.asarray(Image.open(fa).convert('RGB'), np.float32)
    B = np.asarray(Image.open(fb).convert('RGB'), np.float32)
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    warped = cv2.remap(A, gx + back[..., 0], gy + back[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    r = (np.abs(warped - B).max(-1) > 70).astype(np.uint8)
    r = cv2.morphologyEx(r, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(r)
    boxes = [tuple(int(v) for v in st[k, :4]) for k in range(1, n) if st[k, 4] >= 180]
    return boxes


def motion_events(case, F=None):
    meta, fr, fl = F or flows(case)
    T = meta['times']
    mags = []
    rows = []
    for e in fl:
        m = np.hypot(e['fwd'][..., 0], e['fwd'][..., 1])
        e['mag'] = 0.0 if e['cut'] else float(np.percentile(m, 99.5))
        e['boxes'] = [] if e['cut'] else _residual(fr[e['i'] - 1], fr[e['i']], e['back'])
        mags.append(e['mag'])
    med = float(np.median([m for m in mags if m > 0] or [0]))
    for e in fl:
        t = T[e['i']]
        if e['cut']:
            rows.append((t, 'cut'))
            continue
        if e['mag'] > max(8.0, 3 * med):
            rows.append((t, f'jump: the fastest part moved {e["mag"]:.0f} px in one frame (span usual {med:.0f})'))
        if e['boxes']:
            x, y, w, h = max(e['boxes'], key=lambda b: b[2] * b[3])
            rows.append((t, f'{len(e["boxes"])} unexplained change(s) (appeared, vanished or changed shape faster '
                            f'than it moved); largest {w}x{h} px at ({x + w // 2},{y + h // 2}) of {W}x{H}'))
    return rows, (meta, fr, fl)


def motion_image(frame_png, e):
    import cv2
    base = np.asarray(Image.open(frame_png).convert('L').convert('RGB'), np.float32) * 0.4
    if e is None or e['cut']:
        im = Image.fromarray(base.astype(np.uint8))
    else:
        fx, fy = e['fwd'][..., 0], e['fwd'][..., 1]
        mag = np.minimum(np.hypot(fx, fy) / 20.0, 1.0)
        hsv = np.stack([(np.degrees(np.arctan2(fy, fx)) % 360) / 2, np.full_like(mag, 255), mag * 255], -1).astype(np.uint8)
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB).astype(np.float32)
        a = mag[..., None]
        im = Image.fromarray((base * (1 - a) + rgb * a).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for (x, y, w, h) in (e or {}).get('boxes', []):
        d.rectangle((x, y, x + w, y + h), outline=(255, 40, 40), width=3)
    return im


def truth(case, F=None):
    """The flow beside the engine's own movement: per person layer, the centre of its painted mask from one frame to
    the next against the median flow inside it. (Mean error in px, how many layer-steps compared.)"""
    meta, fr, fl = F or flows(case)
    errs, n = [], 0
    for e in fl:
        if e['cut']:
            continue
        i = e['i']
        _, pa, la = load_layers(os.path.join(case, 'layers', f'{i - 1:03d}.npz'))
        _, pb, lb = load_layers(os.path.join(case, 'layers', f'{i:03d}.npz'))
        names_b = {L['name']: k for k, L in enumerate(lb)}
        for k, L in enumerate(la):
            if not _is_person(L) or L['name'] not in names_b:
                continue
            ma, mb = pa[k], pb[names_b[L['name']]]
            if ma.sum() < 150 or mb.sum() < 150:
                continue
            ya, xa = np.nonzero(ma)
            yb, xb = np.nonzero(mb)
            true = np.array([xb.mean() - xa.mean(), yb.mean() - ya.mean()])
            est = np.median(e['fwd'][ma], axis=0)
            errs.append(float(np.hypot(*(true - est))))
            n += 1
    return (float(np.mean(errs)) if errs else None, float(np.median(errs)) if errs else None, n)


# ---------------------------------------------------------------------------------------------- 3 cutout
_SEG = [None]
_U2 = [None]
SEG_COL = {1: (120, 60, 20), 2: (255, 170, 140), 3: (255, 120, 90), 4: (60, 120, 255), 5: (200, 0, 200)}


def _seg(arr):
    import mediapipe as mp
    from mediapipe.tasks.python import BaseOptions, vision
    if _SEG[0] is None:
        _SEG[0] = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
            base_options=BaseOptions(model_asset_path=model('selfie_multiclass.tflite')), output_category_mask=True))
    r = _SEG[0].segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(arr)))
    m = r.category_mask.numpy_view().copy()
    return m.reshape(m.shape[0], m.shape[1])


def _u2(arr):
    import onnxruntime as ort
    if _U2[0] is None:
        _U2[0] = ort.InferenceSession(model('u2netp.onnx'), providers=['CPUExecutionProvider'])
    s = _U2[0]
    x = np.asarray(Image.fromarray(arr).resize((320, 320)), np.float32) / 255.0
    x = (x - (0.485, 0.456, 0.406)) / (0.229, 0.224, 0.225)
    x = x.transpose(2, 0, 1)[None].astype(np.float32)
    y = s.run(None, {s.get_inputs()[0].name: x})[0][0, 0]
    y = (y - y.min()) / (y.max() - y.min() + 1e-6)
    return np.asarray(Image.fromarray((y * 255).astype(np.uint8)).resize((W, H))) > 128


def cutout_frame(frame_png):
    import cv2
    arr = np.asarray(Image.open(frame_png).convert('RGB'))
    cat = _seg(arr)
    sal = _u2(arr)
    person = (cat > 0).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(person)
    blobs = [tuple(int(v) for v in st[k, :5]) for k in range(1, n) if st[k, 4] >= 300]
    return arr, cat, sal, blobs


def cutout_image(res):
    import cv2
    arr, cat, sal, blobs = res
    out = arr.astype(np.float32) * 0.45 + 120
    for c, col in SEG_COL.items():
        out[cat == c] = out[cat == c] * 0.3 + np.array(col) * 0.7
    out = out.astype(np.uint8)
    cs, _ = cv2.findContours(sal.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(out, cs, -1, (255, 230, 0), 2)
    return Image.fromarray(out)


def cutout_events(case, R):
    meta, fr = case_frames(case)
    T = meta['times']
    rows = []
    for i in range(1, len(R)):
        a, b = len(R[i - 1][3]), len(R[i][3])
        if a != b:
            rows.append((T[i], f'people found: {a} -> {b}'))
        sa, sb = R[i - 1][2].sum(), R[i][2].sum()
        if sa > 500 and abs(sb - sa) > 0.35 * sa:
            rows.append((T[i], f'main object cut-out size {sa} -> {sb} px'))
    return rows


# ---------------------------------------------------------------------------------------------- 4 pose
_POSE = [None]
_HAND = [None]
BONES = [(11, 12), (11, 13), (13, 15), (12, 14), (14, 16), (11, 23), (12, 24), (23, 24), (23, 25), (25, 27),
         (24, 26), (26, 28), (0, 11), (0, 12)]
HAND_BONES = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (5, 9), (9, 13), (13, 17), (0, 17),
              (9, 10), (10, 11), (11, 12), (13, 14), (14, 15), (15, 16), (17, 18), (18, 19), (19, 20)]


def pose_frame(frame_png):
    import mediapipe as mp
    from mediapipe.tasks.python import BaseOptions, vision
    if _POSE[0] is None:
        _POSE[0] = vision.PoseLandmarker.create_from_options(vision.PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model('pose_landmarker_full.task')), num_poses=6,
            min_pose_detection_confidence=0.3, min_pose_presence_confidence=0.3))
        _HAND[0] = vision.HandLandmarker.create_from_options(vision.HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model('hand_landmarker.task')), num_hands=6,
            min_hand_detection_confidence=0.3))
    arr = np.ascontiguousarray(np.asarray(Image.open(frame_png).convert('RGB')))
    im = mp.Image(image_format=mp.ImageFormat.SRGB, data=arr)
    poses = [[(p.x * W, p.y * H, p.visibility or 0) for p in lm] for lm in _POSE[0].detect(im).pose_landmarks]
    hands = [[(p.x * W, p.y * H) for p in lm] for lm in _HAND[0].detect(im).hand_landmarks]
    return dict(poses=poses, hands=hands)


def pose_image(frame_png, res, trail):
    im = Image.fromarray((np.asarray(Image.open(frame_png).convert('RGB'), np.float32) * 0.5 + 100).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for k, (pts, col) in enumerate(trail):     # the wrists' paths so far in the span
        if len(pts) > 1:
            d.line(pts, fill=col, width=2)
    for P in res['poses']:
        for a, b in BONES:
            if P[a][2] > 0.3 and P[b][2] > 0.3:
                d.line((P[a][:2], P[b][:2]), fill=(0, 220, 0), width=3)
        for q in (15, 16):
            d.ellipse((P[q][0] - 5, P[q][1] - 5, P[q][0] + 5, P[q][1] + 5), outline=(255, 0, 0), width=2)
    for Hn in res['hands']:
        for a, b in HAND_BONES:
            d.line((Hn[a], Hn[b]), fill=(0, 160, 255), width=2)
    return im


def pose_events(case, R):
    meta, fr = case_frames(case)
    T = meta['times']
    rows = []
    for i in range(1, len(R)):
        a, b = R[i - 1], R[i]
        if len(a['poses']) != len(b['poses']):
            rows.append((T[i], f'bodies found: {len(a["poses"])} -> {len(b["poses"])}'))
        if len(a['hands']) != len(b['hands']):
            rows.append((T[i], f'hands found: {len(a["hands"])} -> {len(b["hands"])}'))
        wa = [P[q][:2] for P in a['poses'] for q in (15, 16)]
        for P in b['poses']:
            for q in (15, 16):
                if wa:
                    dmin = min(math.dist(P[q][:2], w) for w in wa)
                    if dmin > 45:
                        rows.append((T[i], f'a wrist jumped {dmin:.0f} px at ({P[q][0]:.0f},{P[q][1]:.0f})'))
    return rows


def _trails(R, upto):
    tr = {}
    for i in range(upto + 1):
        for k, P in enumerate(R[i]['poses']):
            for q, col in ((15, (255, 60, 60)), (16, (255, 160, 0))):
                tr.setdefault((k, q), ([], col))[0].append(P[q][:2])
    return list(tr.values())


# ---------------------------------------------------------------------------------------------- sheet
CELL = (240, 427)


def picks(n, k=6):
    return sorted(set(int(round(x)) for x in np.linspace(0, n - 1, k)))


def sheet(case, view, cells, events, out_name=None, graph=None):
    """cells: [(t, plain_img, view_img or None)]. 3 columns x 2 rows; a plain-only sheet for view 'plain'."""
    meta, _ = case_frames(case)
    cw = CELL[0] * (1 if view == 'plain' else 2) + 8
    head = 34
    gh = 90 if graph is not None else 0
    rows = math.ceil(len(cells) / 3)
    S = Image.new('RGB', (cw * 3, head + rows * (CELL[1] + 22) + gh), (255, 255, 255))
    d = ImageDraw.Draw(S)
    d.text((8, 8), f'case {os.path.basename(case)}  {meta["t0"]:.2f}-{meta["t1"]:.2f} s  view: {view}',
           fill=(0, 0, 0), font=_font(18))
    for k, (t, a, b) in enumerate(cells):
        x, y = (k % 3) * cw, head + (k // 3) * (CELL[1] + 22)
        S.paste(a.resize(CELL, Image.LANCZOS), (x, y + 20))
        if b is not None:
            S.paste(b.resize(CELL, Image.LANCZOS), (x + CELL[0], y + 20))
        d.text((x + 4, y + 2), f'{t:.2f} s', fill=(0, 0, 0), font=_font(14))
    if graph is not None:
        _graph(d, graph, 0, S.size[1] - gh, S.size[0], gh, meta)
    S.save(os.path.join(case, (out_name or view) + '.jpg'), quality=88)
    with open(os.path.join(case, (out_name or view) + '.txt'), 'w') as fh:
        for t, msg in events:
            fh.write(f'{t:.2f} s  {msg}\n')
        if not events:
            fh.write('nothing printed\n')
    return S


def _graph(d, vals, x0, y0, w, h, meta):
    T = meta['times']
    top = max(max(v for _, v in vals) if vals else 1, 1)
    d.rectangle((x0, y0, x0 + w - 1, y0 + h - 1), outline=(180, 180, 180))
    d.text((x0 + 6, y0 + 2), f'fastest movement per frame (px, top {top:.0f})', fill=(0, 0, 0), font=_font(13))
    pts = [(x0 + 10 + (t - T[0]) / max(T[-1] - T[0], 1e-6) * (w - 20), y0 + h - 6 - v / top * (h - 26))
           for t, v in vals]
    if len(pts) > 1:
        d.line(pts, fill=(200, 0, 0), width=2)


def views(case, which=('plain', 'whereis', 'motion', 'cutout', 'pose')):
    meta, fr = case_frames(case)
    T = meta['times']
    P = picks(len(fr))
    plain = {i: Image.open(fr[i]).convert('RGB') for i in P}
    if 'plain' in which:
        sheet(case, 'plain', [(T[i], plain[i], None) for i in P], [])
    if 'whereis' in which:
        ev = whereis_events(case)
        sheet(case, 'whereis', [(T[i], plain[i], whereis_image(fr[i], os.path.join(case, 'layers', f'{i:03d}.npz')))
                                for i in P], ev)
    if 'motion' in which:
        ev, F = motion_events(case)
        byi = {e['i']: e for e in F[2]}
        sheet(case, 'motion', [(T[i], plain[i], motion_image(fr[i], byi.get(i))) for i in P], ev,
              graph=[(T[e['i']], e['mag']) for e in F[2]])
        tr = truth(case, F)
        with open(os.path.join(case, 'truth.json'), 'w') as fh:
            json.dump(dict(flow_vs_engine_px_mean=tr[0], median=tr[1], compared=tr[2]), fh)
    if 'cutout' in which:
        R = [cutout_frame(f) for f in fr]
        sheet(case, 'cutout', [(T[i], plain[i], cutout_image(R[i])) for i in P], cutout_events(case, R))
    if 'pose' in which:
        R = [pose_frame(f) for f in fr]
        sheet(case, 'pose', [(T[i], plain[i], pose_image(fr[i], R[i], _trails(R, i))) for i in P], pose_events(case, R))


# ---------------------------------------------------------------------------------------------- 5 watch
WCELL = (300, 533)              # each frame on a watch sheet: big enough to see a hand on a chair arm
WCOLS, WROWS = 4, 2             # 8 frames a sheet, read left to right, top to bottom


def _owners(meta):
    """Each person's layers grouped: owner -> [layer index]."""
    by = {}
    for k, L in enumerate(meta):
        if _is_person(L):
            by.setdefault(L['owner'], []).append(k)
    return by


def outline_image(frame_png, layers_npz):
    """The plain frame with a thin line round each person's visible shape, one colour per person (the same
    colour in every frame), and the person's name at the top of the shape."""
    import cv2
    im = Image.open(frame_png).convert('RGB')
    if not os.path.exists(layers_npz):
        return im
    ids, _, meta = load_layers(layers_npz)
    arr = np.asarray(im).copy()
    labels = []
    for owner, ks in _owners(meta).items():
        m = np.isin(ids, ks).astype(np.uint8)
        if m.sum() < 30:
            continue
        edge = m - cv2.erode(m, np.ones((3, 3), np.uint8))
        edge = cv2.dilate(edge, np.ones((2, 2), np.uint8)).astype(bool)
        h = int(hashlib.md5(owner.encode()).hexdigest()[:6], 16)
        r, g, b = colorsys.hsv_to_rgb((h % 360) / 360.0, 1.0, 1.0)
        arr[edge] = (int(r * 255), int(g * 255), int(b * 255))
        n, lab, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
        big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])) if n > 1 else 0
        if big and st[big, cv2.CC_STAT_AREA] > 1500:         # the name over the biggest piece of that person
            x, y, w = st[big, cv2.CC_STAT_LEFT], st[big, cv2.CC_STAT_TOP], st[big, cv2.CC_STAT_WIDTH]
            labels.append((int(x + w // 2 - 20), max(0, int(y) - 12), owner[:12],
                           (int(r * 255), int(g * 255), int(b * 255))))
    im = Image.fromarray(arr)
    d = ImageDraw.Draw(im)
    for x, y, s, c in labels:
        d.text((x, y), s, fill=c, font=_font(11), stroke_width=2, stroke_fill=(0, 0, 0))
    return im


def busy_box(fr, thresh=25, keep=0.8, min_side=180, max_area=0.55):
    """Where things move most across the span: the box holding the middle `keep` of every pixel that changed
    between two frames in a row, padded. None when the whole picture moves (a moving camera) or the box is
    already most of the frame (then the full frames are the close-up). Changes inside a person who already fills
    an eighth of the frame are left out: they are big enough to see on the whole-frame sheets."""
    prev, acc, moving = None, np.zeros((H, W), np.float32), 0
    for f in fr:
        g = np.asarray(Image.open(f).convert('L'), np.int16)
        if prev is not None:
            ch = np.abs(g - prev) > thresh
            moving += ch.mean() > 0.35
            lay = os.path.join(os.path.dirname(os.path.dirname(f)), 'layers', os.path.basename(f)[:-4] + '.npz')
            if os.path.exists(lay):                # a person already big on screen needs no close-up
                ids, _, meta = load_layers(lay)
                for ks in _owners(meta).values():
                    m = np.isin(ids, ks)
                    if m.mean() > 0.12:
                        ch &= ~m
            acc += ch
        prev = g
    if acc.sum() == 0 or moving > len(fr) / 3:
        return None
    lo, hi = (1 - keep) / 2, 1 - (1 - keep) / 2

    def span(v):
        c = np.cumsum(v) / v.sum()
        return int(np.searchsorted(c, lo)), int(np.searchsorted(c, hi))
    x0, x1 = span(acc.sum(0))
    y0, y1 = span(acc.sum(1))
    px, py = max(20, (x1 - x0) // 6), max(20, (y1 - y0) // 6)
    x0, x1, y0, y1 = x0 - px, x1 + px, y0 - py, y1 + py
    w, h = max(x1 - x0, min_side), max(y1 - y0, min_side)
    if h < w * WCELL[1] / WCELL[0]:              # the cell's shape, so nothing is squashed
        h = int(w * WCELL[1] / WCELL[0])
    else:
        w = int(h * WCELL[0] / WCELL[1])
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    x0, y0 = min(max(0, cx - w // 2), max(0, W - w)), min(max(0, cy - h // 2), max(0, H - h))
    box = (x0, y0, min(W, x0 + w), min(H, y0 + h))
    if (box[2] - box[0]) * (box[3] - box[1]) > max_area * W * H:
        return None
    return box


def watch(case, cols=WCOLS, rows=WROWS):
    """Every frame of the span, in order, 8 to a sheet (each sheet starts on the last frame of the one before, so
    no step between frames is unseen), each person outlined. Saved case/watch-NN.jpg; returns the paths."""
    meta, fr = case_frames(case)
    T = meta['times']
    per = cols * rows
    starts = list(range(0, max(len(fr) - 1, 1), per - 1))
    out = []
    box = busy_box(fr)
    for zoom in ((None, box) if box else (None,)):
        out += _watch_sheets(case, meta, fr, T, starts, per, cols, rows, zoom)
    return out


def _watch_sheets(case, meta, fr, T, starts, per, cols, rows, zoom):
    out = []
    for s_no, s in enumerate(starts):
        idx = list(range(s, min(s + per, len(fr))))
        head = 30
        S = Image.new('RGB', (cols * (WCELL[0] + 6), head + rows * (WCELL[1] + 20)), (255, 255, 255))
        d = ImageDraw.Draw(S)
        what = 'CLOSE-UP of where most moves' if zoom else 'whole frame'
        d.text((6, 6), f'case {os.path.basename(case)}  {what}, sheet {s_no + 1} of {len(starts)}: every frame '
                       f'({meta["fps"]} a second), left to right, then the next row', fill=(0, 0, 0), font=_font(16))
        for k, i in enumerate(idx):
            x, y = (k % cols) * (WCELL[0] + 6), head + (k // cols) * (WCELL[1] + 20)
            img = outline_image(fr[i], os.path.join(case, 'layers', f'{i:03d}.npz'))
            if zoom:
                img = img.crop(zoom)
            S.paste(img.resize(WCELL, Image.LANCZOS), (x, y + 18))
            d.text((x + 3, y + 1), f'{T[i]:.3f} s', fill=(0, 0, 0), font=_font(14))
        p = os.path.join(case, f'watch-{"zoom-" if zoom else ""}{s_no + 1:02d}.jpg')
        S.save(p, quality=90)
        out.append(p)
    return out


# ---------------------------------------------------------------------------------------------- main
def main(a):
    if not a or a[0] not in ('render', 'views', 'clip', 'watch'):
        print(__doc__)
        return 2
    if a[0] == 'watch':
        print('\n'.join(watch(a[1])))
        return 0
    if a[0] == 'render':
        case = a[1]
        film = a[a.index('--film') + 1]
        i = a.index('--span')
        src = a[a.index('--src') + 1] if '--src' in a else HERE
        frames(src, film, float(a[i + 1]), float(a[i + 2]), os.path.abspath(case))
    elif a[0] == 'views':
        views(a[1], tuple(a[2:]) or ('plain', 'whereis', 'motion', 'cutout', 'pose'))
    else:
        film, t0, t1, out = a[1], float(a[2]), float(a[3]), os.path.abspath(a[4])
        frames(HERE, film.replace('-', '_'), t0, t1, out)
        views(out)
        print('sheets:', ', '.join(sorted(glob.glob(os.path.join(out, '*.jpg')))))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
