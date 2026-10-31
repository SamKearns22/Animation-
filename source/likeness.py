#!/usr/bin/env python3
"""Likeness tools (after Halo No-No, 31 Oct: people did not recognise Damon in Roadster; Farage and Musk each took
several passes). Measuring by eye on compare.py's guide lines was the weak step, so this measures for us.

A face finder (MediaPipe's face mesh: 478 points on a face) reads each photo. The face is turned to face the camera
and laid over an AVERAGE face (MediaPipe's own model of one); what makes a person recognisable is how they differ from
that average (the caricaturist's rule: find the difference, push it further). A second model marks hair, skin, and
accessories such as glasses, for the big shapes (hair outline, beard, glasses) that read first at phone size.

    python3 source/likeness.py average
        rebuild source/likeness_average.json (the average real face) from every face in references/ and refs/;
        run it when a film's references are filed, so the crowd grows.
    python3 source/likeness.py card PHOTO [PHOTO ...] OUT.jpg [--face N] [--name NAME]
        the face card: what is distinctive, strongest first, with how far to push each; the JSON beside it holds
        every measure. Several photos of one person: the measures are averaged and any that disagree are marked unsure.
    python3 source/likeness.py head PHOTO OUT.png [--face N] [--push 1.6]
        a starter head in house style drawn from the measurements, each difference pushed (1 = the photo, 1.6 =
        60% further). A starting point to restyle by hand, never the finished head. Also saves OUT-average.png:
        the average face drawn the same way, so check can take away what the drawing style itself does.
    python3 source/likeness.py check PHOTO OURS.png OUT.jpg [--face N] [--ours-face N] [--others PHOTO ...]
                                     [--bias AVERAGE.png]
        our drawing measured the same way: every distinctive measure must go the SAME way as the photo's, and at
        least as far (a feature pushed the wrong way is the commonest cause of "who is that?"). Adds the
        phone-size strip (both faces at the sizes they appear in a vertical video) and, with --others, a line-up:
        our drawing must sit closer to its own person than to anyone else. --bias (or OURS-average.png beside
        OURS) is the average face drawn in the same style; without it, the style's own pull is left in.

--face N picks a face when a photo holds several (0 = leftmost). Small faces in big photos are found by searching
crops. Models live in source/models/ (downloaded at session start by .claude/hooks/setup.sh, never on GitHub).
"""
import json
import math
import os
import subprocess
import sys

os.environ.setdefault('GLOG_minloglevel', '3')
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '3')

import numpy as np                                    # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, 'models')
SANS = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
SANS_R = SANS
URLS = {
    'face_landmarker.task': 'https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task',
    'canonical_face_model.obj': 'https://raw.githubusercontent.com/google-ai-edge/mediapipe/master/mediapipe/modules/face_geometry/data/canonical_face_model.obj',
    'yunet.onnx': 'https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx',
    'selfie_multiclass.tflite': 'https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite',
}

# ---------------------------------------------------------------------------------------------- the face mesh's points
OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149,
        150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
LIPS_OUT = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146]
LIPS_IN = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
EYE_R = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]       # the person's right (our left)
EYE_L = [263, 466, 388, 387, 386, 385, 384, 398, 362, 382, 381, 380, 374, 373, 390, 249]
BROW_R = [70, 63, 105, 66, 107, 55, 65, 52, 53, 46]                                         # top edge out->in, then under
BROW_L = [300, 293, 334, 296, 336, 285, 295, 282, 283, 276]


def _d(P, a, b):
    return float(np.hypot(*(P[a, :2] - P[b, :2])))


def _eye_w(P):
    return (_d(P, 33, 133) + _d(P, 362, 263)) / 2


def _ipd(P):
    r, l = (P[33, :2] + P[133, :2]) / 2, (P[362, :2] + P[263, :2]) / 2
    return float(np.hypot(*(r - l)))


def _ang(P, a, b, sg):
    """Rise from a to b in degrees (y up), mirrored so both sides read the same way."""
    v = P[b, :2] - P[a, :2]
    return math.degrees(math.atan2(v[1], sg * v[0]))


# (key, what it means when bigger, when smaller, the measure, mouth/eyes that a smile changes)
MEASURES = [
    ('face_wide', 'a wide, broad face', 'a long, narrow face', lambda P: _d(P, 234, 454) / _d(P, 10, 152), ''),
    ('jaw_wide', 'a broad, square jaw', 'a narrow, tapering jaw', lambda P: _d(P, 172, 397) / _d(P, 234, 454), ''),
    ('forehead_wide', 'a wide forehead', 'a narrow forehead', lambda P: _d(P, 21, 251) / _d(P, 234, 454), ''),
    ('eyes_apart', 'eyes set wide apart', 'close-set eyes', lambda P: _d(P, 133, 362) / _eye_w(P), ''),
    ('eye_size', 'big eyes', 'small eyes', lambda P: _eye_w(P) / _d(P, 234, 454), ''),
    ('eye_open', 'round, open eyes', 'narrow, hooded eyes', lambda P: (_d(P, 159, 145) + _d(P, 386, 374)) / 2 / _eye_w(P), 'smile'),
    ('eye_tilt', 'eyes tilting up at the outer corners', 'eyes drooping at the outer corners',
     lambda P: (_ang(P, 133, 33, -1) + _ang(P, 362, 263, 1)) / 2, 'angle'),
    ('brow_high', 'brows set high above the eyes', 'brows low and heavy over the eyes',
     lambda P: (_d(P, 52, 159) + _d(P, 282, 386)) / 2 / _eye_w(P), ''),
    ('brow_slope', 'brows rising to the outside', 'brows sloping down at the outside',
     lambda P: (_ang(P, 107, 70, -1) + _ang(P, 336, 300, 1)) / 2, 'angle'),
    ('nose_long', 'a long nose', 'a short nose', lambda P: _d(P, 168, 2) / _d(P, 168, 152), ''),
    ('nose_wide', 'a wide nose', 'a narrow nose', lambda P: _d(P, 129, 358) / _ipd(P), ''),
    ('mouth_wide', 'a wide mouth', 'a small mouth', lambda P: _d(P, 61, 291) / _ipd(P), 'smile'),
    ('lip_top', 'a full upper lip', 'a thin upper lip', lambda P: _d(P, 0, 13) / _d(P, 61, 291), 'smile'),
    ('lip_low', 'a full lower lip', 'a thin lower lip', lambda P: _d(P, 14, 17) / _d(P, 61, 291), 'smile'),
    ('philtrum', 'a long gap from nose to lip', 'a short gap from nose to lip', lambda P: _d(P, 2, 0) / _d(P, 168, 152), 'smile'),
    ('chin_long', 'a long chin', 'a short chin', lambda P: _d(P, 17, 152) / _d(P, 168, 152), 'smile'),
]
NOTICE = 0.6           # closer to the middle than this (in spreads: about 73 in 100 faces) is not worth drawing


# ------------------------------------------------------------------------------------------------------- models
def _model(name):
    os.makedirs(MODELS, exist_ok=True)
    path = os.path.join(MODELS, name)
    if not os.path.exists(path):
        subprocess.run(['curl', '-sS', '-L', '-o', path, URLS[name]], check=True)
    return path


_CACHE = {}


def _landmarker():
    if 'lm' not in _CACHE:
        from mediapipe.tasks.python import vision, BaseOptions
        opt = vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=_model('face_landmarker.task')),
                                           num_faces=4, output_face_blendshapes=True,
                                           min_face_detection_confidence=0.3, min_face_presence_confidence=0.3)
        _CACHE['lm'] = vision.FaceLandmarker.create_from_options(opt)
    return _CACHE['lm']


def canonical():
    """The average face (MediaPipe's canonical model, centimetres, y up, z towards us)."""
    if 'can' not in _CACHE:
        v = [list(map(float, l.split()[1:4])) for l in open(_model('canonical_face_model.obj')) if l.startswith('v ')]
        _CACHE['can'] = np.array(v[:468])
    return _CACHE['can']


# ------------------------------------------------------------------------------------------------ finding faces
def _detect(im):
    import mediapipe as mp
    arr = np.ascontiguousarray(np.asarray(im.convert('RGB')))
    r = _landmarker().detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=arr))
    if not r.face_landmarks:
        return None
    # the face nearest the middle (the crop is centred on the face we want; a neighbour may show at its edge)
    i = min(range(len(r.face_landmarks)), key=lambda j: abs(np.mean([p.x for p in r.face_landmarks[j]]) - 0.5)
            + abs(np.mean([p.y for p in r.face_landmarks[j]]) - 0.5))
    pts = np.array([[p.x, p.y, p.z] for p in r.face_landmarks[i]])
    bs = {c.category_name: c.score for c in r.face_blendshapes[i]} if r.face_blendshapes else {}
    return pts, bs


def _boxes(im):
    """Face boxes (x, y, w, h) from OpenCV's YuNet detector, which finds small faces in big photos; the photo is
    also tried enlarged so faces under 40 pixels are found."""
    import cv2
    arr = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
    out = []
    for k in (1.0, 2.0):
        a = arr if k == 1 else cv2.resize(arr, None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC)
        if max(a.shape[:2]) > 4000:
            continue
        det = cv2.FaceDetectorYN.create(_model('yunet.onnx'), '', (a.shape[1], a.shape[0]), 0.6)
        _, f = det.detect(a)
        for r in (f if f is not None else []):
            b = r[:4] / k
            if all(abs(b[0] - o[0]) > 0.5 * o[2] or abs(b[1] - o[1]) > 0.5 * o[3] for o in out):
                out.append(tuple(float(v) for v in b))
    return out


def find_faces(path):
    """Every face in the photo: points in the photo's pixels (x, y, depth), the expression scores, the face box.
    The face finder only sees faces that fill a good part of the picture, so smaller ones are looked for in
    enlarged crops."""
    im = Image.open(path).convert('RGB')
    W, H = im.size
    found = []

    def add(box):
        x0, y0, x1, y1 = box
        crop = im.crop(box)
        k = 640 / max(crop.size)
        r = _detect(crop.resize((max(1, int(crop.width * k)), max(1, int(crop.height * k))), Image.LANCZOS))
        if r is None:
            return
        pts, bs = r
        P = np.c_[x0 + pts[:, 0] * (x1 - x0), y0 + pts[:, 1] * (y1 - y0), pts[:, 2] * (x1 - x0)]
        lo, hi = P[:468, :2].min(0), P[:468, :2].max(0)
        size = (hi - lo).max()
        if size > 0.95 * max(x1 - x0, y1 - y0) or size < 12:
            return                               # cut off by the crop's edge, or too small to measure
        c = (lo + hi) / 2
        for f in found:
            if np.hypot(*(f['centre'] - c)) < 0.4 * f['size']:
                if size > f['size'] * 0.9 and min(lo) > 0:
                    pass
                return
        found.append(dict(P=P, bs=bs, centre=c, size=size, box=(lo, hi)))

    for x, y, w, h in _boxes(im):
        side = max(w, h) * 1.7                     # the face and a margin round it, enlarged for the mesh
        cx, cy = x + w / 2, y + h / 2
        add((int(cx - side), int(cy - side * 1.1), int(cx + side), int(cy + side * 0.9)))
    if not found:                                  # drawings the detector misses: try the whole picture
        add((0, 0, W, H))
    found.sort(key=lambda f: f['centre'][0])
    return im, found


def pick_face(path, n=None):
    im, faces = find_faces(path)
    if not faces:
        raise SystemExit(f'{path}: no face found (a straight-on photo with the face at least 60 pixels tall works best)')
    if n is None:
        if len(faces) > 1:
            print(f'{path}: {len(faces)} faces found, using the biggest (choose with --face 0..{len(faces) - 1}, left to right)')
        n = max(range(len(faces)), key=lambda i: faces[i]['size'])
    return im, faces[n]


# ------------------------------------------------------------------------------------------- front on, measured
def frontal(P):
    """The face turned to look straight at us and scaled onto the average face (centimetres, y up)."""
    X = np.c_[P[:468, 0], -P[:468, 1], -P[:468, 2]]
    C = canonical()
    mx, mc = X.mean(0), C.mean(0)
    A, B = X - mx, C - mc
    U, S, Vt = np.linalg.svd(A.T @ B)
    D = np.eye(3)
    D[2, 2] = np.sign(np.linalg.det(U @ Vt))
    R = U @ D @ Vt
    s = (S * np.diag(D)).sum() / (A ** 2).sum()
    F = s * A @ R + mc
    yaw = math.degrees(math.atan2(R[0, 2], R[2, 2]))
    return F, abs(yaw)


def measure(P):
    return {k: float(f(P)) for k, _, _, f, _ in MEASURES}


AVERAGE = os.path.join(HERE, 'likeness_average.json')


def baseline(smiling=False):
    """The average real face and how much faces vary, measured on every usable face in references/ and refs/
    (`likeness.py average` rebuilds it). Smiling or talking photos are compared with smiling faces, since a grin
    widens the mouth and narrows the eyes. Falls back to MediaPipe's model face if the file is missing."""
    if 'base' not in _CACHE:
        if os.path.exists(AVERAGE):
            _CACHE['base'] = json.load(open(AVERAGE))
        else:
            m = measure(canonical())
            sp = {k: (2.5 if kind == 'angle' else 0.08 * m[k]) for k, _, _, _, kind in MEASURES}
            _CACHE['base'] = {'neutral': dict(n=0, med=m, spread=sp, shape=canonical().tolist())}
    b = _CACHE['base']
    if smiling and b.get('smiling', {}).get('n', 0) >= 8:
        return b['smiling']
    return b['neutral']


def is_smiling(bs):
    return bool(bs) and (max(bs.get('mouthSmileLeft', 0), bs.get('mouthSmileRight', 0)) > 0.35
                         or bs.get('jawOpen', 0) > 0.25)


def out_of_100(z):
    """'wider than 93 in 100 faces' from a difference in spreads."""
    return int(round(100 * 0.5 * (1 + math.erf(abs(z) / math.sqrt(2)))))


def differences(meas, bs, unsure=()):
    """Each measure against real faces, in spreads (0 = the middle of the crowd, 1 = more than about 84 in 100
    faces, 2 = more than about 98 in 100): + bigger, - smaller; strongest first."""
    smiling = is_smiling(bs)
    base = baseline(smiling)
    out = []
    for k, big, small, _, kind in MEASURES:
        dev = (meas[k] - base['med'][k]) / base['spread'][k]
        warn = ''
        if kind == 'smile' and smiling:
            warn = 'smiling in this photo: compared with smiling faces; check on a straight face'
        if k in unsure:
            warn = (warn + '; ' if warn else '') + 'the photos disagree'
        out.append(dict(key=k, dev=dev, words=big if dev > 0 else small, warn=warn, value=meas[k], avg=base['med'][k]))
    out.sort(key=lambda r: -abs(r['dev']))
    return out


def build_average(out=AVERAGE):
    """Measure every face in references/ and refs/ (turned under 25 degrees, at least 40 pixels) and keep the
    middle value and spread of each measure, for straight and smiling faces, and the middle face shape."""
    import glob
    root = os.path.dirname(HERE)
    files = sorted(f for d in ('references', 'refs') for f in glob.glob(os.path.join(root, d, '**', '*'), recursive=True)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')))
    groups = {'neutral': [], 'smiling': []}
    for f in files:
        try:
            _, faces = find_faces(f)
        except Exception:
            continue
        for fc in faces:
            F, yaw = frontal(fc['P'])
            if yaw < 25 and fc['size'] >= 40:
                groups['smiling' if is_smiling(fc['bs']) else 'neutral'].append((measure(F), F))
    res = {}
    for g, rows in groups.items():
        if not rows:
            continue
        med, spread = {}, {}
        for k, _, _, _, kind in MEASURES:
            v = np.array([m[k] for m, _ in rows])
            med[k] = float(np.median(v))
            spread[k] = float(max(np.median(abs(v - med[k])) * 1.4826, 1e-3))     # robust: cartoons in the pile barely move it
        shape = np.median(np.array([F for _, F in rows]), 0)
        res[g] = dict(n=len(rows), med=med, spread=spread, shape=shape.round(3).tolist())
    res['made_from'] = f'{len(files)} pictures in references/ and refs/'
    json.dump(res, open(out, 'w'))
    print(out, {g: res[g]['n'] for g in groups if g in res})


# -------------------------------------------------------------------------------------------- the big shapes
def _segmenter():
    if 'seg' not in _CACHE:
        from mediapipe.tasks.python import vision, BaseOptions
        opt = vision.ImageSegmenterOptions(base_options=BaseOptions(model_asset_path=_model('selfie_multiclass.tflite')),
                                           output_category_mask=True)
        _CACHE['seg'] = vision.ImageSegmenter.create_from_options(opt)
    return _CACHE['seg']


def segment(im, face):
    """Hair, face skin and accessories round one face: a crop twice the face's size, each pixel labelled
    (0 background, 1 hair, 2 body skin, 3 face skin, 4 clothes, 5 accessories such as glasses)."""
    import mediapipe as mp
    (x0, y0), (x1, y1) = face['box']
    c, s = (np.array([x0, y0]) + [x1, y1]) / 2, max(x1 - x0, y1 - y0)
    box = (int(c[0] - 1.1 * s), int(c[1] - 1.25 * s), int(c[0] + 1.1 * s), int(c[1] + 0.95 * s))
    crop = im.crop(box).resize((512, 512), Image.LANCZOS)
    arr = np.ascontiguousarray(np.asarray(crop))
    r = _segmenter().segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=arr))
    mask = np.squeeze(r.category_mask.numpy_view()).copy()
    return crop, mask, box


def big_shapes(im, face):
    """What reads first at phone size: hair (outline, volume, fringe, colour), beard, glasses, skin colour."""
    crop, mask, box = segment(im, face)
    P = face['P']
    k = 512 / (box[2] - box[0])
    to = lambda x, y: ((x - box[0]) * k, (y - box[1]) * (512 / (box[3] - box[1])))
    px = np.asarray(crop).astype(float)
    top, chin = to(*P[10, :2]), to(*P[152, :2])
    fh = chin[1] - top[1]
    cx = to(*P[168, :2])[0]
    lw, rw = to(*P[234, :2])[0], to(*P[454, :2])[0]
    out = {}
    hair = _own_region(mask == 1, top, chin)
    mask = np.where((mask == 1) & ~hair, 0, mask)           # a neighbour's hair is not this person's
    ys, xs = np.nonzero(hair)
    if len(ys) > 50:
        out['hair_top'] = float((top[1] - ys.min()) / fh)        # how far the hair rises above the forehead
        out['hair_wide'] = float((xs.max() - xs.min()) / (rw - lw))
        col = int(round(cx))
        colm = mask[:, max(0, col - 3):col + 4]
        skin_rows = np.nonzero((colm == 3).any(1))[0]
        out['hairline'] = float((top[1] - skin_rows.min()) / fh) if len(skin_rows) else None   # + above point 10
        brow_y = to(*P[9, :2])[1]
        band = hair[int(top[1]):int(brow_y), int(lw):int(rw)]
        out['fringe'] = float(band.mean()) if band.size else 0.0
        out['hair_rgb'] = [int(v) for v in np.median(px[hair], 0)]
        out['hair_below_ears'] = float((ys.max() - to(*P[234, :2])[1]) / fh)
    skin = mask == 3
    cheek = np.zeros_like(skin)
    for i in (50, 280, 101, 330):                                 # the cheeks under the eyes
        x, y = to(*P[i, :2])
        cheek[int(y) - 6:int(y) + 6, int(x) - 6:int(x) + 6] = True
    sk = px[skin & cheek] if (skin & cheek).sum() > 20 else px[skin]
    out['skin_rgb'] = [int(v) for v in np.median(sk, 0)] if len(sk) else [220, 180, 150]
    lum = lambda a: a @ [0.3, 0.59, 0.11]
    skin_l = float(np.median(lum(sk))) if len(sk) else 150.0
    # beard: the chin and jaw below the mouth, darker than the cheeks (or labelled hair)
    def region_dark(ids):
        poly = [to(*P[i, :2]) for i in ids]
        m = Image.new('L', (512, 512), 0)
        ImageDraw.Draw(m).polygon(poly, fill=255)
        sel = np.asarray(m) > 0
        if sel.sum() < 10:
            return 0.0, 0.0
        return float(1 - np.median(lum(px[sel])) / max(1, skin_l)), float(hair[sel].mean())
    chin_dark, chin_hair = region_dark([57, 43, 106, 182, 83, 18, 313, 406, 335, 273, 287, 288, 397, 365, 379, 378,
                                        400, 377, 152, 148, 176, 149, 150, 136, 172, 58])
    lip_dark, lip_hair = region_dark([98, 97, 2, 326, 327, 391, 393, 164, 167, 165, 92])
    out['beard'] = round(max(chin_dark, chin_hair), 2)
    out['moustache'] = round(max(lip_dark, lip_hair), 2)
    # glasses: accessories over the eyes, or a dark ring round them
    eyes = np.zeros_like(skin)
    for a, b in ((33, 133), (362, 263)):
        (xa, ya), (xb, yb) = to(*P[a, :2]), to(*P[b, :2])
        w = abs(xb - xa)
        eyes[int(min(ya, yb) - 0.7 * w):int(max(ya, yb) + 0.7 * w), int(min(xa, xb) - 0.35 * w):int(max(xa, xb) + 0.35 * w)] = True
    out['glasses'] = round(float((mask[eyes] == 5).mean()), 2)
    return out, (crop, mask, box)


def _own_region(m, top, chin):
    """Only the hair touching this face's top (a neighbour's hair in the crop is dropped)."""
    from scipy import ndimage
    lab, n = ndimage.label(ndimage.binary_closing(m, iterations=2))
    if n == 0:
        return m
    fh = chin[1] - top[1]
    y0, y1 = int(max(0, top[1] - 0.6 * fh)), int(top[1] + 0.3 * fh)
    x0, x1 = int(max(0, top[0] - 0.6 * fh)), int(top[0] + 0.6 * fh)
    near = lab[y0:y1, x0:x1]
    ids, counts = np.unique(near[near > 0], return_counts=True)
    if len(ids) == 0:
        return np.zeros_like(m)
    return m & (lab == ids[np.argmax(counts)])


def describe_shapes(bsh):
    lines = []
    ht = bsh.get('hair_top')
    if ht is None:
        lines.append(('hair', 'little or no hair found: bald or shaved? check the photo'))
    else:
        vol = 'big, high hair' if ht > 0.32 else ('flat, close hair' if ht < 0.16 else 'medium-height hair')
        wide = ', wide past the ears' if bsh['hair_wide'] > 1.35 else ''
        fr = (', a fringe over the forehead' if bsh['fringe'] > 0.35 else
              (', hair partly over the forehead' if bsh['fringe'] > 0.12 else ', forehead clear'))
        long_ = ', down past the jaw' if bsh.get('hair_below_ears', 0) > 0.6 else ''
        hl = bsh.get('hairline')
        rec = ''
        if hl is not None and hl > 0.12:
            rec = ', a high or receding hairline'
        lines.append(('hair', f'{vol}{wide}{fr}{long_}{rec}; colour {_name_col(bsh["hair_rgb"])}'))
    if bsh['beard'] > 0.2 or bsh['moustache'] > 0.4:
        what = ('a full beard and moustache' if bsh['beard'] > 0.2 and bsh['moustache'] > 0.4 else
                'a beard on the chin and jaw' if bsh['beard'] > 0.2 else 'a moustache')
        lines.append(('facial hair', f'{what} (darkness {bsh["beard"]:.2f} chin, {bsh["moustache"]:.2f} lip): draw it as a shape'))
    else:
        lines.append(('facial hair', 'clean-shaven (or very light stubble)'))
    lines.append(('glasses', 'GLASSES: draw the frames, they are the first thing people see' if bsh['glasses'] > 0.08
                  else 'none found (check by eye: thin rimless frames can be missed)'))
    r, g, b = bsh['skin_rgb']
    l = 0.3 * r + 0.59 * g + 0.11 * b
    lines.append(('skin', f"{'light' if l > 175 else 'medium' if l > 130 else 'brown' if l > 85 else 'dark brown'} "
                          f"{tuple(bsh['skin_rgb'])} (photo light changes it: check by eye)"))
    return lines


def _name_col(rgb):
    r, g, b = rgb
    l = 0.3 * r + 0.59 * g + 0.11 * b
    if max(rgb) - min(rgb) < 18:
        return f'grey {tuple(rgb)}' if l > 90 else f'near black {tuple(rgb)}'
    word = 'very dark' if l < 55 else 'dark' if l < 95 else 'mid' if l < 150 else 'light'
    hue = 'blond' if (r > 150 and g > 120 and b < 120) else 'red-brown' if r > g * 1.35 else 'brown'
    return f'{word} {hue} {tuple(rgb)}'


# ---------------------------------------------------------------------------------------------- the face card
def analyse(paths, faces=None, name=None):
    """Measure one person over one or more photos."""
    per, bss, shapes, firsts = [], [], [], None
    for i, path in enumerate(paths):
        n = faces[i] if faces and i < len(faces) else None
        im, f = pick_face(path, n)
        F, yaw = frontal(f['P'])
        m = measure(F)
        per.append(m)
        bss.append(f['bs'])
        try:
            shapes.append(big_shapes(im, f)[0])
        except Exception as e:                       # the segmenter is a help, not essential
            print('big shapes skipped:', e)
        if yaw > 25:
            if len(paths) > 1:
                print(f'{path}: turned {yaw:.0f} degrees from the camera, left out of the measures (best under 15)')
                per.pop()
                bss.pop()
                if len(shapes) > len(per):
                    shapes.pop()
                continue
            print(f'{path}: turned {yaw:.0f} degrees from the camera, measures less sure (best under 15)')
        if firsts is None:
            firsts = (im, f, F)
    meas = {k: float(np.mean([m[k] for m in per])) for k in per[0]}
    bs = {k: float(np.mean([b.get(k, 0) for b in bss])) for k in bss[0]} if bss and bss[0] else {}
    base = baseline(is_smiling(bs))
    unsure = []
    if len(per) > 1:
        for k in meas:
            vals = np.array([m[k] for m in per])
            dev = abs(meas[k] - base['med'][k]) / base['spread'][k]
            if vals.std() / base['spread'][k] > max(0.5, dev * 0.6):
                unsure.append(k)
    diffs = differences(meas, bs, unsure)
    avg = base['med']
    shape = shapes[0] if shapes else None
    return dict(name=name or os.path.splitext(os.path.basename(paths[0]))[0], photos=paths, measures=meas,
                average=avg, diffs=diffs, shapes=shape, smile=max(bs.get('mouthSmileLeft', 0), bs.get('mouthSmileRight', 0)),
                first=firsts)


def push_words(dev):
    a = abs(dev)
    return 'strong: push it hard' if a > 1.5 else 'clear: push it' if a > 1.0 else 'slight: show it' if a > NOTICE else ''


def card(paths, out, faces=None, name=None):
    A = analyse(paths, faces, name)
    im, f, F = A['first']
    P = f['P']
    (x0, y0), (x1, y1) = f['box']
    s = max(x1 - x0, y1 - y0)
    box = (int(x0 - 0.45 * s), int(y0 - 0.6 * s), int(x1 + 0.45 * s), int(y1 + 0.3 * s))
    ph = im.crop(box)
    k = 620 / ph.height
    ph = ph.resize((int(ph.width * k), 620), Image.LANCZOS)
    d = ImageDraw.Draw(ph, 'RGBA')
    q = lambda i: ((P[i, 0] - box[0]) * k, (P[i, 1] - box[1]) * k)
    for ring in (OVAL, LIPS_OUT, EYE_R, EYE_L, BROW_R, BROW_L):
        d.line([q(i) for i in ring] + [q(ring[0])], fill=(0, 255, 160, 200), width=2)
    for a, b in ((234, 454), (172, 397), (133, 362), (168, 2), (61, 291), (17, 152)):
        d.line([q(a), q(b)], fill=(255, 60, 120, 220), width=2)
    # the frontal face over the average one
    fr = Image.new('RGB', (420, 620), (250, 250, 250))
    dd = ImageDraw.Draw(fr)
    C = np.array(baseline(is_smiling(f['bs']))['shape'])
    def map2(X):
        return [(210 + 21 * x, 300 - 21 * y) for x, y in X[:, :2]]
    for X, colr in ((C, (170, 170, 170)), (F, (220, 30, 90))):
        pts = map2(X)
        for ring in (OVAL, LIPS_OUT, EYE_R, EYE_L, BROW_R, BROW_L):
            dd.line([pts[i] for i in ring] + [pts[ring[0]]], fill=colr, width=3 if colr[0] == 220 else 2)
        dd.line([pts[168], pts[2]], fill=colr, width=2)
        dd.line([pts[129], pts[2], pts[358]], fill=colr, width=2)
    ft = ImageFont.truetype(SANS, 22)
    fs = ImageFont.truetype(SANS_R, 19)
    dd.text((10, 8), 'grey: the average face', font=fs, fill=(120, 120, 120))
    dd.text((10, 32), 'pink: this face, front on', font=fs, fill=(220, 30, 90))
    rows = [r for r in A['diffs'] if abs(r['dev']) > NOTICE]
    lines = [(f"{A['name']}: what makes this face recognisable", ft, (0, 0, 0)), ('', fs, 0)]
    for r in rows:
        lines.append((f"{r['words']}: more so than {out_of_100(r['dev'])} in 100 faces  ({push_words(r['dev'])})",
                      fs, (0, 0, 0) if not r['warn'] else (150, 110, 0)))
        if r['warn']:
            lines.append((f"        ({r['warn']})", fs, (150, 110, 0)))
    if not rows:
        lines.append(('very close to the average face: likeness lives in the big shapes below', fs, (0, 0, 0)))
    lines.append(('', fs, 0))
    lines.append(('The big shapes (they read first at phone size):', ft, (0, 0, 0)))
    if A['shapes']:
        for k2, v in describe_shapes(A['shapes']):
            lines.append((f'{k2}: {v}', fs, (0, 0, 0)))
    tw = 900
    th = max(620, 40 + 28 * len(lines))
    sheet = Image.new('RGB', (ph.width + 420 + tw + 40, th), (255, 255, 255))
    sheet.paste(ph, (0, 0))
    sheet.paste(fr, (ph.width + 10, 0))
    ds = ImageDraw.Draw(sheet)
    y = 14
    for text, font, colr in lines:
        ds.text((ph.width + 450, y), text, font=font, fill=colr)
        y += 28
    sheet.save(out, quality=88)
    js = os.path.splitext(out)[0] + '.json'
    with open(js, 'w') as fh:
        json.dump({k: v for k, v in A.items() if k != 'first'}, fh, indent=1)
    print(out, js)
    for t, _, _ in lines[2:]:
        if t:
            print(' ', t)
    return A


# ------------------------------------------------------------------------------------------- a starter head
INK = (24, 22, 28)


def _flat(rgb, lift=1.0):
    """A photo colour made flat for the house style: a little cleaner and lighter."""
    r, g, b = [min(255, int(v * lift)) for v in rgb]
    m = (r + g + b) / 3
    return tuple(int(min(255, m + (v - m) * 1.15)) for v in (r, g, b))


def _dk(c, k):
    return tuple(int(v * k) for v in c)


def _smooth(pts, n=6, closed=True):
    sys.path.insert(0, HERE)
    from ed import curve, open_curve
    return curve(pts, n) if closed else open_curve(pts, n)


def head(photo, out, face=None, push=1.6, size=700, A=None, twin=True):
    """A front-on head in the house style (flat fills, black outlines, hands-off), drawn from the measured face with
    every difference from the average pushed `push` times: the start for a likeness head, to restyle by hand."""
    if A is None:
        A = analyse([photo], [face] if face is not None else None)
    im, f, F = A['first']
    C = np.array(baseline(is_smiling(f['bs']))['shape'])
    X = C + push * (F - C)                                  # the caricature: the difference, pushed
    sh = A['shapes'] or {}
    SS = 3
    S = size * SS
    img = Image.new('RGB', (S, int(S * 1.15)), (238, 236, 230))
    d = ImageDraw.Draw(img)
    u = S / 26.0                                            # px per cm
    ox, oy = S / 2, S * 0.56
    pt = lambda i: (ox + u * X[i, 0], oy - u * X[i, 1])
    lw = lambda w: max(1, int(w * SS))
    skin = _flat(sh.get('skin_rgb', [222, 180, 150]), 1.04)
    hair = _flat(sh.get('hair_rgb', [70, 52, 40]), 1.0)
    # hair and forehead skin from the photo's own masks, laid onto the frontal face by matching the face outlines
    hair_m = skin_m = None
    try:
        import cv2
        crop, mask, box = segment(im, f)
        P = f['P']
        kx, ky = (box[2] - box[0]) / 512, (box[3] - box[1]) / 512
        tp = ((P[10, 0] - box[0]) / kx, (P[10, 1] - box[1]) / ky)
        cp = ((P[152, 0] - box[0]) / kx, (P[152, 1] - box[1]) / ky)
        own = _own_region(mask == 1, tp, cp)
        M = _fit2d(P[OVAL, :2], np.array([pt(i) for i in OVAL]))
        Aff = M @ np.array([[kx, 0, box[0]], [0, ky, box[1]], [0, 0, 1.0]])
        def warp(m):
            w = cv2.warpAffine((m * 255).astype(np.uint8), Aff, img.size, flags=cv2.INTER_LINEAR)
            w = cv2.GaussianBlur(w, (0, 0), 4 * SS)                 # smooth, flat-cartoon edges
            return Image.fromarray(((w > 127) * 255).astype(np.uint8))
        from scipy import ndimage
        hair_m, skin_m = warp(own), warp(mask == 3)
        lab, n = ndimage.label(np.asarray(hair_m) > 0)            # one piece of hair: drop stray bits
        if n > 1:
            big = 1 + int(np.argmax(ndimage.sum(lab > 0, lab, range(1, n + 1))))
            hair_m = Image.fromarray(((lab == big) * 255).astype(np.uint8))
    except Exception as e:
        print('hair from the photo skipped:', e)
    from PIL import ImageChops
    # neck and ears behind
    nx = (pt(172)[0] + pt(397)[0]) / 2
    nw = abs(pt(397)[0] - pt(172)[0]) * 0.36
    d.polygon([(nx - nw, pt(152)[1] - 30 * SS), (nx + nw, pt(152)[1] - 30 * SS), (nx + nw * 1.1, S * 1.15),
               (nx - nw * 1.1, S * 1.15)], fill=_dk(skin, 0.9), outline=INK)
    d.line([(nx - nw, pt(152)[1] - 30 * SS), (nx - nw * 1.1, S * 1.15)], fill=INK, width=lw(3))
    d.line([(nx + nw, pt(152)[1] - 30 * SS), (nx + nw * 1.1, S * 1.15)], fill=INK, width=lw(3))
    if hair_m is not None:
        img.paste(Image.new('RGB', img.size, _dk(hair, 0.85)), (0, 0), hair_m)
        img.paste(Image.new('RGB', img.size, INK), (0, 0), ImageChops.subtract(hair_m.filter(ImageFilter.MaxFilter(9)), hair_m))
        d = ImageDraw.Draw(img)
    for a, b, sg in ((234, 93, -1), (454, 323, 1)):
        (xa, ya), (xb, yb) = pt(a), pt(b)
        ear = [(xa, ya), (xa + sg * 0.9 * u, ya - 0.2 * u), (xa + sg * 1.2 * u, (ya + yb) / 2),
               (xb + sg * 0.6 * u, yb + 0.6 * u), (xb, yb + 0.4 * u)]
        e = _smooth(ear, 6)
        d.polygon(e, fill=skin)
        d.line(e + [e[0]], fill=INK, width=lw(3))
    # the face
    face_pts = _smooth([pt(i) for i in OVAL], 4)
    d.polygon(face_pts, fill=skin)
    if skin_m is not None:                                   # the forehead up to the real hairline
        top = Image.new('L', img.size, 0)
        ImageDraw.Draw(top).rectangle([0, 0, img.width, pt(9)[1]], fill=255)
        img.paste(Image.new('RGB', img.size, skin), (0, 0), ImageChops.multiply(skin_m, top))
        d = ImageDraw.Draw(img)
    # beard and moustache as shapes under the outline
    if sh.get('beard', 0) > 0.2:
        ids = [234, 93, 132, 58, 172, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 397, 288, 361, 323, 454]
        lower = [pt(i) for i in ids]
        top_edge = [pt(i) for i in (454, 352, 411, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146, 61, 187, 123, 234)]
        bshape = _smooth(lower + top_edge[1:-1], 3)
        d.polygon(bshape, fill=_mix(hair, skin, 0.35))
    if sh.get('moustache', 0) > 0.4:
        m = [pt(i) for i in (61, 186, 92, 165, 167, 164, 393, 391, 322, 410, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185)]
        d.polygon(_smooth(m, 3), fill=_mix(hair, skin, 0.3))
    d.line(face_pts + [face_pts[0]], fill=INK, width=lw(4))
    if skin_m is not None:                                   # no outline across the forehead: it runs on to the hairline
        top = Image.new('L', img.size, 0)
        ImageDraw.Draw(top).rectangle([0, 0, img.width, pt(9)[1]], fill=255)
        inner = Image.new('L', img.size, 0)
        ImageDraw.Draw(inner).polygon(face_pts, fill=255)
        img.paste(Image.new('RGB', img.size, skin), (0, 0),
                  ImageChops.multiply(ImageChops.multiply(skin_m.filter(ImageFilter.MinFilter(15)), top), inner.filter(ImageFilter.MaxFilter(15))))
        d = ImageDraw.Draw(img)
    # hair over the face's top: the fringe and temples exactly where the photo has hair
    if hair_m is not None:
        sides = Image.new('L', img.size, 0)
        ImageDraw.Draw(sides).polygon(face_pts, fill=255)
        top_only = Image.new('L', img.size, 0)
        ImageDraw.Draw(top_only).rectangle([0, 0, img.width, pt(159)[1] - 0.4 * u], fill=255)
        over = ImageChops.multiply(hair_m, ImageChops.lighter(top_only, ImageChops.invert(sides)))
        img.paste(Image.new('RGB', img.size, hair), (0, 0), over)
        edge = ImageChops.subtract(over.filter(ImageFilter.MaxFilter(9)), over.filter(ImageFilter.MinFilter(3)))
        edge = ImageChops.multiply(edge, ImageChops.lighter(sides, hair_m))
        img.paste(Image.new('RGB', img.size, INK), (0, 0), ImageChops.multiply(edge, ImageChops.invert(over.filter(ImageFilter.MinFilter(9)))))
    d = ImageDraw.Draw(img)
    # brows: the measured band, filled dark
    for ids in (BROW_R, BROW_L):
        b = _smooth([pt(i) for i in ids], 4)
        d.polygon(b, fill=_dk(hair, 0.7))
    # eyes: the measured opening, white, a round iris cut to it, a heavy upper lid
    for ids, ir in ((EYE_R, 468), (EYE_L, 473)):
        e = _smooth([pt(i) for i in ids], 4)
        d.polygon(e, fill=(250, 250, 246))
        cx = np.mean([p[0] for p in e])
        cy = np.mean([p[1] for p in e])
        w = max(p[0] for p in e) - min(p[0] for p in e)
        r = w * 0.22
        m = Image.new('L', img.size, 0)
        ImageDraw.Draw(m).polygon(e, fill=255)
        iris = Image.new('L', img.size, 0)
        ImageDraw.Draw(iris).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
        from PIL import ImageChops
        img.paste(Image.new('RGB', img.size, (92, 70, 52)), (0, 0), ImageChops.multiply(m, iris))
        pup = Image.new('L', img.size, 0)
        ImageDraw.Draw(pup).ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45], fill=255)
        img.paste(Image.new('RGB', img.size, INK), (0, 0), ImageChops.multiply(m, pup))
        d = ImageDraw.Draw(img)
        n = len(e) // 2
        d.line(e[:n + 1], fill=INK, width=lw(4))
        d.line(e[n:] + [e[0]], fill=INK, width=lw(2))
    # nose: one side of the bridge, the tip's underside, the wings
    d.line(_smooth([pt(i) for i in (193, 245, 188, 174, 236)], 4, False), fill=_dk(skin, 0.72), width=lw(2.5))
    d.line(_smooth([pt(i) for i in (129, 98, 97, 2, 326, 327, 358)], 4, False), fill=_dk(skin, 0.6), width=lw(3))
    for ids in ((129, 203, 98), (358, 423, 327)):
        d.line(_smooth([pt(i) for i in ids], 4, False), fill=_dk(skin, 0.6), width=lw(2.5))
    # mouth: the measured lips, open if the photo's mouth is open (teeth)
    outer = _smooth([pt(i) for i in LIPS_OUT], 3)
    inner = _smooth([pt(i) for i in LIPS_IN], 3)
    lip = _mix((196, 112, 108), skin, 0.45)
    d.polygon(outer, fill=lip)
    gap = _d(F, 13, 14) / max(1e-6, _d(F, 61, 291))
    if gap > 0.06:
        d.polygon(inner, fill=(60, 20, 24))
        ys = [p[1] for p in inner]
        tm = Image.new('L', img.size, 0)
        ImageDraw.Draw(tm).polygon(inner, fill=255)
        teeth = Image.new('L', img.size, 0)
        ImageDraw.Draw(teeth).rectangle([0, 0, img.width, min(ys) + (max(ys) - min(ys)) * 0.55], fill=255)
        from PIL import ImageChops
        img.paste(Image.new('RGB', img.size, (246, 244, 236)), (0, 0), ImageChops.multiply(tm, teeth))
        d = ImageDraw.Draw(img)
        d.line(inner + [inner[0]], fill=INK, width=lw(2.5))
    else:
        d.line([pt(i) for i in (61, 78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 291)], fill=INK, width=lw(3))
    d.line(outer + [outer[0]], fill=_dk(lip, 0.7), width=lw(1.5))
    # glasses
    if sh.get('glasses', 0) > 0.08:
        for a, b, tb in ((33, 133, (159, 145)), (362, 263, (386, 374))):
            (xa, ya), (xb, yb) = pt(a), pt(b)
            cx, cy = (xa + xb) / 2, (ya + yb) / 2
            w = abs(xb - xa) * 0.82
            h = w * 0.72
            d.rounded_rectangle([cx - w, cy - h * 0.85, cx + w, cy + h], radius=w * 0.45, outline=INK, width=lw(5))
        d.line([(pt(133)[0] + 0.2 * u, pt(133)[1] - 0.5 * u), (pt(362)[0] - 0.2 * u, pt(362)[1] - 0.5 * u)],
               fill=INK, width=lw(4))
    img = img.resize((size, int(size * 1.15)), Image.LANCZOS)
    img.save(out)
    print(out)
    if push != 0 and twin:
        # the AVERAGE face drawn the same way (same hair, beard, glasses): what the drawing style itself does to the
        # measures, so check can take it away
        head(photo, os.path.splitext(out)[0] + '-average.png', face, 0.0, size, A, twin=False)
    return out, A


def _mix(a, b, k):
    return tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))


def _fit2d(src, dst):
    """The 2D similarity (turn, scale, shift) taking src points onto dst."""
    ms, md = src.mean(0), dst.mean(0)
    A, B = src - ms, dst - md
    U, S, Vt = np.linalg.svd(A.T @ B)
    D = np.eye(2)
    D[1, 1] = np.sign(np.linalg.det(U @ Vt))
    R = (U @ D @ Vt)
    s = (S * np.diag(D)).sum() / (A ** 2).sum()
    M = np.zeros((2, 3))
    M[:, :2] = s * R.T
    M[:, 2] = md - s * R.T @ ms
    return M


def _outline(mask):
    """The biggest region's outer edge, in order (a simple border walk on a coarse grid)."""
    from scipy import ndimage
    lab, n = ndimage.label(mask)
    if n == 0:
        return None
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    m = lab == (1 + int(np.argmax(sizes)))
    m = ndimage.binary_fill_holes(m)
    ys, xs = np.nonzero(m)
    cy, cx = ys.mean(), xs.mean()
    pts = []
    for a in np.linspace(-math.pi, math.pi, 180, endpoint=False):         # the furthest edge along each ray
        dx, dy = math.cos(a), math.sin(a)
        r = 0
        best = None
        while True:
            x, y = int(cx + dx * r), int(cy + dy * r)
            if not (0 <= x < m.shape[1] and 0 <= y < m.shape[0]):
                break
            if m[y, x]:
                best = (x, y)
            r += 1
        if best:
            pts.append(best)
    return pts


# ------------------------------------------------------------------------------------------------------ check
def check(photo, ours, out, face=None, ours_face=None, others=(), bias=None):
    A = analyse([photo], [face] if face is not None else None)
    try:
        B = analyse([ours], [ours_face] if ours_face is not None else None)
    except SystemExit:
        B = None
    lines = []
    bias = bias or (os.path.splitext(ours)[0] + '-average.png')
    if B is not None and os.path.exists(bias):
        # the drawing style's own pull: the average face drawn the same way should measure as average
        try:
            Z = analyse([bias], [ours_face] if ours_face is not None else None)
            zb = {r['key']: r['dev'] for r in Z['diffs']}
            for r in B['diffs']:
                r['dev'] -= zb[r['key']]
            lines.append((f'(the drawing style\'s own pull taken away, measured on {os.path.basename(bias)})', (90, 90, 90)))
        except SystemExit:
            pass
    elif B is not None:
        lines.append(('(no average-face twin of this drawing: the style\'s own pull is NOT taken away; read with care)',
                      (150, 110, 0)))
    score = None
    if B is None:
        lines.append(('The face finder cannot see a face in our drawing at all.', (180, 0, 0)))
        lines.append(('That alone is a warning: eyes, nose and mouth may be too small or too far from a face\'s layout.',
                      (180, 0, 0)))
    else:
        bd = {r['key']: r for r in B['diffs']}
        good = bad = weak = 0
        lines.append(('measure (in spreads from the middle)  photo  ours   verdict', (0, 0, 0)))
        for r in A['diffs']:
            if abs(r['dev']) <= NOTICE:
                continue
            o = bd[r['key']]['dev']
            if np.sign(o) != np.sign(r['dev']) and abs(o) > 0.2:
                v, colr = 'WRONG WAY: this undoes the likeness', (190, 0, 0)
                bad += 1
            elif abs(o) < abs(r['dev']) * 0.9:
                v, colr = 'too timid: push further', (170, 110, 0)
                weak += 1
            else:
                v, colr = 'good', (0, 120, 40)
                good += 1
            note = '  (photo smiling: unsure)' if r['warn'] else ''
            lines.append((f"{r['words'][:36]:<36} {r['dev']:+5.1f} {o:+5.1f}   {v}{note}", colr))
        lines.append(('', (0, 0, 0)))
        lines.append((f'{good} good, {weak} too timid, {bad} the wrong way', (0, 0, 0)))
        keys = [k for k, *_ in MEASURES]
        va = np.array([next(x['dev'] for x in A['diffs'] if x['key'] == k) for k in keys])
        vb = np.array([bd[k]['dev'] for k in keys])
        score = float(va @ vb / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-9))
        lines.append((f'match with the photo: {score * 100:.0f}% (the face\'s differences pointing the same way; '
                      f'aim for 60%+)', (0, 0, 0)))
        if others:
            ranks = [(A['name'] + ' (target)', score)]
            for o in others:
                try:
                    Ao = analyse([o])
                except SystemExit:
                    continue
                vo = np.array([next(x['dev'] for x in Ao['diffs'] if x['key'] == k) for k in keys])
                ranks.append((os.path.splitext(os.path.basename(o))[0], float(vo @ vb / (np.linalg.norm(vo) * np.linalg.norm(vb) + 1e-9))))
            ranks.sort(key=lambda t: -t[1])
            pos = [n for n, _ in ranks].index(A['name'] + ' (target)') + 1
            lines.append(('', (0, 0, 0)))
            lines.append((f'line-up: our drawing comes out closest to number {pos} of {len(ranks)}'
                          + (' (the right person)' if pos == 1 else ' (NOT the right person)'), (0, 120, 40) if pos == 1 else (190, 0, 0)))
            for n_, s_ in ranks[:6]:
                lines.append((f'   {s_ * 100:+4.0f}%  {n_}', (60, 60, 60)))
    # big shapes: the hair and glasses finder only reads photos, so these are ticked by eye on the sheet
    if A['shapes']:
        lines.append(('', (0, 0, 0)))
        lines.append(('big shapes in the photo (tick each by eye on our drawing):', (0, 0, 0)))
        for k, v in describe_shapes(A['shapes']):
            lines.append((f'  [ ] {k}: {v}', (0, 0, 0)))
    # the sheet: photo | ours (same face height), the phone-size strip under them
    def face_crop(R, h):
        im, f, _ = R['first']
        (x0, y0), (x1, y1) = f['box']
        s = max(x1 - x0, y1 - y0)
        c = im.crop((int(x0 - 0.5 * s), int(y0 - 0.6 * s), int(x1 + 0.5 * s), int(y1 + 0.35 * s)))
        return c.resize((max(1, int(c.width * h / c.height)), h), Image.LANCZOS)
    pa_ = face_crop(A, 520)
    pb_ = face_crop(B, 520) if B else Image.open(ours).convert('RGB').resize((450, 520))
    ft = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSansMono.ttf') if os.path.exists(
        os.path.join(HERE, 'fonts', 'DejaVuSansMono.ttf')) else SANS_R, 18)
    tw = 1000
    strip_h = 200
    H = max(520 + strip_h + 40, 30 + 24 * len(lines))
    sheet = Image.new('RGB', (pa_.width + pb_.width + 20 + tw, H), (255, 255, 255))
    sheet.paste(pa_, (0, 0))
    sheet.paste(pb_, (pa_.width + 20, 0))
    ds = ImageDraw.Draw(sheet)
    ds.text((10, 530), 'phone size (a face this tall in a 1920-tall vertical video, seen on a phone):', font=ft, fill=(0, 0, 0))
    x = 10
    for hh in (40, 70, 120):                               # a crowd, a seated wide shot, a medium shot
        for R, fall in ((A, None), (B, ours)):
            if R:
                small = face_crop(R, hh * 2)
            else:
                small = Image.open(fall).convert('RGB').resize((hh * 2, hh * 2))
            small = small.resize((max(1, small.width // 2), hh), Image.LANCZOS).resize((small.width, hh * 2), Image.NEAREST)
            sheet.paste(small, (x, 560))
            x += small.width + 6
        x += 24
    y = 10
    for t, colr in lines:
        ds.text((pa_.width + pb_.width + 40, y), t, font=ft, fill=colr)
        y += 24
    sheet.save(out, quality=88)
    print(out)
    for t, _ in lines:
        print(' ', t)
    return score


# --------------------------------------------------------------------------------------------------------- main
def _opts(args, flags, multi=()):
    o = {}
    for fl in flags:
        if fl in args:
            i = args.index(fl)
            if fl in multi:
                j = i + 1
                while j < len(args) and not args[j].startswith('--'):
                    j += 1
                o[fl] = args[i + 1:j]
                del args[i:j]
            else:
                o[fl] = args[i + 1]
                del args[i:i + 2]
    return o


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    cmd = args.pop(0)
    o = _opts(args, ('--face', '--name', '--push', '--ours-face', '--others', '--bias'), multi=('--others',))
    fc = [int(o['--face'])] * 10 if '--face' in o else None
    if cmd == 'average':
        build_average()
    elif cmd == 'card':
        card(args[:-1], args[-1], fc, o.get('--name'))
    elif cmd == 'head':
        head(args[0], args[1], fc[0] if fc else None, float(o.get('--push', 1.6)))
    elif cmd == 'check':
        check(args[0], args[1], args[2], fc[0] if fc else None,
              int(o['--ours-face']) if '--ours-face' in o else None, o.get('--others', ()), o.get('--bias'))
    else:
        print(__doc__)
