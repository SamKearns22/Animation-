#!/usr/bin/env python3
"""MAP  beardkit (7 Nov, Sam: "build a tool that can nail both those final results on first analysis"): facial hair
read from straight-on photos and drawn in the house style, in one pass.

Why: Vance's beard took eight notes and Abdul's moustache and goatee four, because each fix followed the words of the
note and drew by eye. The finals that worked share one method, which this tool now does from the photo itself:
    SHAPE    from the photo's own hair map, not from words: every patch of hair (moustache, the patch under the lip,
             the beard and how far up the chin and cheeks it reaches) and every patch of skin between them.
    STYLE    flat house shapes only (Sam, 7 Nov: the flecked, many-toned beard was "convoluted, sort of disgusting"):
             one flat colour per region, a darker flat band where the photo's beard is darkest (under the jaw), the
             moustache in its own colour when it differs; every edge facing skin a row of small sharp tufts; the
             silhouette below the jaw inked; a soft, even grain of short strokes falling down and in, only when the
             photo's hair is salt-and-pepper (light hairs among dark).
    COLOUR   measured against the photo's own clean skin and carried onto the cartoon's skin (the same ratio).

How it reads hair: the face is found (MediaPipe's 478 points), turned level and scaled to a standard size; the
clean skin is sampled on the cheekbones and forehead; each pixel scores as hair where it differs from that skin in
colour AND is grainy (hair has fine texture, skin and soft shadow are smooth). Eyes, brows, lips and nostrils are
left out. The score is laid on the cartoon face's own frame (anchored at the eyes, nose base, lip lines, mouth
corners, chin and face edge), averaged over the photos and with its mirror image (front-on faces are symmetrical),
and traced into shapes. Shapes are stored in that anchored frame, so they fit any measured face (likeness heads).

    python3 source/beardkit.py analyse NAME PHOTO [PHOTO ...] [--says "chin=goatee, moustache=thin"] [--out DIR]
        Reads the FIRST photo (the best straight-on, close, recent one: beards change; averaging photos let light
        and expression blur the reading); the others only warn where they read differently. Prints what the photo
        shows in five plain lines (moustache, patch under the lip, chin, cheeks, colour) for Sam to confirm; any line
        the photo can't judge is set with --says (7 Nov: neither finished beard was a pure photo reading: Vance's bare
        patches hold more stubble than Abdul's "goatee" chin):
            chin=gap|goatee   moustache=thin|medium|full   colour=ash|dark   corners=apart
        Writes DIR/NAME-beard.json (the spec) and DIR/NAME-beard.jpg (the photo, its hair map, the grid, and the beard
        on an empty face). Tested 7 Nov: Vance (vance-front-2026 + "chin=gap, moustache=medium") and Abdul
        (18d7e6e5 + "chin=goatee, moustache=thin, colour=dark") come out largely as their approved finals
        (review/beardkit-test.jpg).
    In a cast file:  import beardkit;  SPEC = beardkit.load(PATH);  beardkit.draw(p, f, L, skin, SPEC)
        draw it after the face's skin and before the nose and mouth.

Map: frame 60 | photo analysis 150 | grid and shapes 260 | colours 330 | drawing 380 | sheet 470 | CLI 540
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

NOSE = [129, 49, 64, 98, 97, 2, 326, 327, 294, 279, 358, 4]
SKIN_AT = [117, 346, 151, 50, 280]                # cheekbones, forehead, upper cheeks: clean skin on nearly everyone
STD_EYE_CHIN = 520.0                              # the standard face: eye line to chin, in pixels
STD_W, STD_H, STD_EYE = 1000, 1000, (500, 300)


# ---------------------------------------------------------------------------------------------- the anchored frame
# Vertical anchors: the eye line, the nose's base, the upper lip's top, the mouth line, the lower lip's bottom, the
# chin. Horizontal: the mouth corner, then the face's edge at that height. A point is stored as (a, b):
#   b = i + t between anchors i and i+1 (below the chin, 5 + t in units of lip17-to-chin)
#   a = |u| / mouth half-width inside the mouth corner (0..1), then 1 + the share of the way to the face edge (1..2,
#       beyond 2 outside the face). Sign of u kept separately (shapes are drawn symmetrically from the right half).
V_NAMES = ('eye_y', 'nose_y', 'lip0', 'lip13', 'lip17')


def v_anchors(L):
    return [L['eye_y'], L['nose_y'], L['lip0'], L['lip13'], L['lip17'], 1.0]


def b_of_v(v, anc):
    if v <= anc[0]:
        return (v - anc[0]) / (anc[1] - anc[0])
    for i in range(5):
        if v <= anc[i + 1]:
            return i + (v - anc[i]) / (anc[i + 1] - anc[i])
    return 5 + (v - 1.0) / (1.0 - anc[4])


def v_of_b(b, anc):
    if b <= 0:
        return anc[0] + b * (anc[1] - anc[0])
    if b >= 5:
        return 1.0 + (b - 5) * (1.0 - anc[4])
    i = int(b)
    return anc[i] + (b - i) * (anc[i + 1] - anc[i])


def cartoon_edge(L, chin_w=0.4):
    """The cartoon face's half-width at height v (from patriots4's outline)."""
    import patriots4_cast as P4
    pts = P4.outline_uv(L, chin_w)
    right = sorted({(round(v, 4), abs(u)) for u, v in pts if u >= 0 and v >= 0.0})
    vs = np.array([v for v, _ in right])
    us = np.array([u for _, u in right])

    def edge(v):
        if v >= 1.0:
            return max(0.0, float(np.interp(1.0, vs, us)) * (1 - (v - 1.0) * 6))
        return float(np.interp(v, vs, us))
    return edge


def uv_of_ab(a, b, L, edge):
    sg = -1.0 if a < 0 else 1.0
    a = abs(a)
    v = v_of_b(b, v_anchors(L))
    mh = L['mw'] / 2
    if a <= 1:
        return sg * a * mh, v
    e = max(edge(min(v, 1.0)), mh + 0.02)
    return sg * (mh + (a - 1) * (e - mh)), v


def ab_of_uv(u, v, L, edge):
    b = b_of_v(v, v_anchors(L))
    mh = L['mw'] / 2
    u = abs(u)
    if u <= mh:
        return u / mh, b
    e = max(edge(min(v, 1.0)), mh + 0.02)
    return 1 + (u - mh) / (e - mh), b


# ---------------------------------------------------------------------------------------------- the photo
def standard_face(path):
    """The face turned level and scaled so the eye line to chin is STD_EYE_CHIN pixels; its points moved with it."""
    import likeness as LK
    im, face = LK.pick_face(path)
    P = face['P'][:, :2]
    _, yaw = LK.frontal(face['P'])
    el, er = P[LK.EYE_R].mean(0), P[LK.EYE_L].mean(0)
    mid = (el + er) / 2
    ang = math.atan2(er[1] - el[1], er[0] - el[0])
    chin = P[152]
    up = np.array([math.sin(ang), -math.cos(ang)])
    dist = abs(np.dot(chin - mid, -up))
    k = STD_EYE_CHIN / dist
    c, s = math.cos(-ang) * k, math.sin(-ang) * k
    M = np.array([[c, -s, 0.0], [s, c, 0.0]])
    M[:, 2] = np.array(STD_EYE) - M[:, :2] @ mid
    img = cv2.warpAffine(np.asarray(im.convert('RGB')), M, (STD_W, STD_H), flags=cv2.INTER_CUBIC,
                         borderMode=cv2.BORDER_REPLICATE)
    Q = P @ M[:, :2].T + M[:, 2]
    return img, Q, yaw, dist


def hair_score(img, Q):
    """0..1 per pixel: how surely it is hair (differs from the clean skin in colour and is grainy)."""
    import likeness as LK
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB).astype(np.float32)
    lab[..., 0] *= 100 / 255.0
    lab[..., 1:] -= 128
    L = lab[..., 0]
    hp = np.abs(L - cv2.GaussianBlur(L, (0, 0), 2.5))
    tex = cv2.GaussianBlur(hp, (0, 0), 5)
    skin = []
    for i in SKIN_AT:
        x, y = Q[i].astype(int)
        skin.append(lab[y - 10:y + 11, x - 10:x + 11].reshape(-1, 3))
    skin = np.concatenate(skin)
    ref = np.median(skin, 0)
    d = np.sqrt(((lab[..., 0] - ref[0]) ** 2) + 2.0 * ((lab[..., 1] - ref[1]) ** 2 + (lab[..., 2] - ref[2]) ** 2))
    d = cv2.GaussianBlur(d, (0, 0), 4)
    ts = []
    ds = []
    for i in SKIN_AT:
        x, y = Q[i].astype(int)
        ts.append(tex[y - 10:y + 11, x - 10:x + 11].ravel())
        ds.append(d[y - 10:y + 11, x - 10:x + 11].ravel())
    ts, ds = np.concatenate(ts), np.concatenate(ds)
    zt = (tex - np.median(ts)) / (ts.std() + 0.3)
    zd = (d - np.median(ds)) / (ds.std() + 1.5)
    score = np.clip((np.minimum(zt, 8) * 0.5 + np.minimum(zd, 8) * 0.5 - 2.2) / 2.0, 0, 1)
    mask = Image.new('L', (img.shape[1], img.shape[0]), 0)
    dr = ImageDraw.Draw(mask)
    for poly, grow in ((LK.EYE_R, 10), (LK.EYE_L, 10), (LK.BROW_R, 8), (LK.BROW_L, 8), (LK.LIPS_OUT, 3), (NOSE, 6)):
        pts = Q[poly]
        c = pts.mean(0)
        pts = c + (pts - c) * (1 + grow / max(10.0, np.abs(pts - c).max()))
        dr.polygon([tuple(p) for p in pts], fill=255)
    out = np.asarray(mask) > 0
    score[out] = 0
    lips = Image.new('L', (img.shape[1], img.shape[0]), 0)
    ImageDraw.Draw(lips).polygon([tuple(p) for p in Q[LK.LIPS_OUT]], fill=255)
    lips = cv2.dilate(np.asarray(lips), np.ones((7, 7), np.uint8)) > 0
    # the lips are under the cartoon's own mouth: count them as hair where hair surrounds them (left and right of
    # the mouth line), so the beard and moustache run up to the drawn lips instead of leaving a ring of skin
    near = cv2.GaussianBlur(np.where(lips, 0, score).astype(np.float32), (0, 0), 14)
    wt = cv2.GaussianBlur((~lips).astype(np.float32), (0, 0), 14)
    score[lips] = np.clip(near[lips] / np.maximum(wt[lips], 1e-3) * 1.4, 0, 1)
    return score, ref, lab, out


# ---------------------------------------------------------------------------------------------- the photo's frame
class PhotoFrame:
    """Photo pixels of the anchored frame (a, b) on one standard face."""

    def __init__(self, Q):
        import likeness as LK
        eye = (Q[LK.EYE_R].mean(0) + Q[LK.EYE_L].mean(0)) / 2
        self.mid = (eye[0] + Q[152][0]) / 2
        self.ys = [eye[1], Q[2][1], Q[0][1], (Q[13][1] + Q[14][1]) / 2, Q[17][1], Q[152][1]]
        self.mh = (abs(Q[61][0] - self.mid) + abs(Q[291][0] - self.mid)) / 2
        oval = Q[LK.OVAL]
        right = oval[oval[:, 0] >= self.mid]
        left = oval[oval[:, 0] < self.mid]
        def half(side):
            o = side[np.argsort(side[:, 1])]
            return o[:, 1], np.abs(o[:, 0] - self.mid)
        self.ry, self.rx = half(right)
        self.ly, self.lx = half(left)

    def y_of_b(self, b):
        ys = self.ys
        if b <= 0:
            return ys[0] + b * (ys[1] - ys[0])
        if b >= 5:
            return ys[5] + (b - 5) * (ys[5] - ys[4])
        i = int(b)
        return ys[i] + (b - i) * (ys[i + 1] - ys[i])

    def edge(self, y, sgn):
        yy, xx = (self.ry, self.rx) if sgn > 0 else (self.ly, self.lx)
        if y > yy.max():
            return max(0.0, float(np.interp(yy.max(), yy, xx)) * (1 - (y - yy.max()) / 120))
        return float(np.interp(y, yy, xx))

    def xy(self, a, b, sgn):
        y = self.y_of_b(b)
        if a <= 1:
            return self.mid + sgn * a * self.mh, y
        e = max(self.edge(min(y, self.ys[5]), sgn), self.mh + 4)
        return self.mid + sgn * (self.mh + (a - 1) * (e - self.mh)), y


# ---------------------------------------------------------------------------------------------- grid and shapes
A_MAX, B_MIN, B_MAX = 2.35, -0.2, 5.45
NA, NB = 94, 226


def grid_of(score, frame, img=None):
    """The hair score on the (a, b) grid, both halves (right, left), each cell the mean over a small window; and the
    photo colour per cell when img is given."""
    As = np.linspace(0, A_MAX, NA)
    Bs = np.linspace(B_MIN, B_MAX, NB)
    G = np.zeros((2, NB, NA))
    C = np.zeros((2, NB, NA, 3))
    blur = cv2.GaussianBlur(score, (0, 0), 3)
    imgb = cv2.GaussianBlur(img.astype(np.float32), (0, 0), 3) if img is not None else None
    for k, sgn in enumerate((1, -1)):
        for j, b in enumerate(Bs):
            for i, a in enumerate(As):
                x, y = frame.xy(a, b, sgn)
                xi, yi = int(round(x)), int(round(y))
                if 0 <= xi < score.shape[1] and 0 <= yi < score.shape[0]:
                    G[k, j, i] = blur[yi, xi]
                    if imgb is not None:
                        C[k, j, i] = imgb[yi, xi]
    return G, C, As, Bs


def shapes_of(mask, As, Bs, min_cells=25):
    """Outlines of the hair on the whole face (the right half's grid mirrored onto the left), each with its holes
    (the mouth, skin gaps): [{'outer': [(a, b)...], 'holes': [[(a, b)...], ...]}], a signed (minus = our left)."""
    m = mask.astype(np.float32) if mask.dtype != bool else mask.astype(np.float32)
    full = np.concatenate([m[:, :0:-1], m], 1)                # a from -A_MAX to A_MAX (the middle column once)
    na = full.shape[1]
    up = cv2.resize(full, (na * 4, NB * 4), interpolation=cv2.INTER_CUBIC)   # the smooth strength, traced at 0.5
    up = (cv2.GaussianBlur(up, (0, 0), 2.5) > 0.5).astype(np.uint8)
    cs, hier = cv2.findContours(up, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    def ab(c):
        c = c[:, 0, :].astype(float)
        k = 18                                                 # a moving average round the ring: no stair steps
        c = np.array([c[np.arange(i - k, i + k + 1) % len(c)].mean(0) for i in range(len(c))])
        c = cv2.approxPolyDP(c.astype(np.float32).reshape(-1, 1, 2), 1.2, True)[:, 0, :].astype(float)
        a = (c[:, 0] / (na * 4 - 1) * 2 - 1) * A_MAX
        b = B_MIN + c[:, 1] / (NB * 4 - 1) * (B_MAX - B_MIN)
        return [(float(x), float(y)) for x, y in zip(a, b)]
    out = []
    if hier is None:
        return out
    for i, c in enumerate(cs):
        if hier[0][i][3] != -1 or cv2.contourArea(c) < min_cells * 16:
            continue
        holes = []
        j = hier[0][i][2]
        while j != -1:
            if cv2.contourArea(cs[j]) >= 22 * 16 and len(cs[j]) > 6:      # specks of skin (pores, nostril edges) dropped
                h = ab(cs[j])
                if np.mean([b for _, b in h]) > 3.0:          # a moustache is drawn solid: no gaps above the mouth line
                    holes.append(h)
            j = hier[0][j][0]
        out.append(dict(outer=ab(c), holes=holes))
    return out


def analyse(name, paths, out_dir=None, says=None):
    says = dict(says or {})
    import likeness as LK
    G_all, C_all, skins, warns = [], [], [], []
    faces = []
    for path in paths:
        try:
            img, Q, yaw, _ = standard_face(path)
        except SystemExit:
            warns.append(f'{os.path.basename(path)}: no whole face found, left out')
            continue
        if yaw > 15:
            warns.append(f'{os.path.basename(path)}: turned {yaw:.0f} degrees, left out (front-on photos only)')
            continue
        score, ref, lab, out = hair_score(img, Q)
        frame = PhotoFrame(Q)
        G, C, As, Bs = grid_of(score, frame, img)
        skin_rgb = np.median(np.concatenate([img[int(Q[i][1]) - 10:int(Q[i][1]) + 11,
                                                 int(Q[i][0]) - 10:int(Q[i][0]) + 11].reshape(-1, 3) for i in SKIN_AT]), 0)
        G_all.append(G)
        C_all.append(C / np.maximum(skin_rgb, 1))           # colour as a share of that photo's own skin
        faces.append((path, img, Q, score))
    if not G_all:
        raise SystemExit('no usable front-on photo')
    # beards change (Vance's 2023 portrait has a fuller, darker beard than his 2026 one): every photo is compared
    # with the first, and one whose beard differs is left out, with a warning
    first = G_all[0].mean(0) > 0.5
    agree = [0]
    for k in range(1, len(G_all)):
        m = G_all[k].mean(0) > 0.5
        iou = (first & m).sum() / max(1, (first | m).sum())
        if iou < 0.6:
            warns.append(f'{os.path.basename(faces[k][0])}: its beard reads differently from the first photo ({iou:.0%} '
                         f'alike: grown, trimmed, or the light?)')
    # one photo is read (the first: the best straight-on shot); averaging photos let light and expression blur the
    # reading even where the beard was the same (7 Nov: Vance's three portraits read as a near-black goatee)
    G_all, C_all, faces = G_all[:1], C_all[:1], faces[:1]
    G = np.mean([g.mean(0) for g in G_all], 0)               # both halves and every photo: symmetrical, steadier
    R = np.mean([c.mean(0) for c in C_all], 0)
    AA, BB = np.meshgrid(As, Bs)
    allowed = ((AA <= 2.02) | (BB > 4.4)) & (AA <= 2.12) & (BB <= 5.17)   # the face, a little spill below the jaw
    G = np.where(allowed, G, 0.0)
    G = cv2.GaussianBlur(G.astype(np.float32), (0, 0), 1.2)
    hair = G > 0.5
    # the lips' row and the skin gaps are what the photo says; only specks are cleaned
    hair = cv2.morphologyEx(hair.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    hair = cv2.morphologyEx(hair, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)) > 0
    # facial hair grows round the mouth and jaw: keep only regions reaching below the upper lip's top (crow's feet,
    # creases by the nose and stray background are dropped)
    n, lab_ = cv2.connectedComponents(hair.astype(np.uint8))
    keep = np.zeros_like(hair)
    for k in range(1, n):
        reg = lab_ == k
        if BB[reg].max() > 2.2 and reg.sum() >= 12:
            keep |= reg
    # the moustache's top runs along the nostrils, which were left out of the photo: close small gaps there
    band = (BB > 0.7) & (BB < 2.2)
    closed = cv2.morphologyEx(keep.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) > 0
    keep = keep | (closed & band)
    hair = keep
    # Sam's words where the photos can't tell (7 Nov: Abdul's chin stubble is too faint for any photo measure, and
    # Vance's bare patches beside the lip hold more stubble than Abdul's chin): chin=goatee fills the chin's middle,
    # keeping small clear notches either side of the patch under the lip; chin=gap leaves it as the photos read
    chin_mid = hair[(BB > 4.3) & (BB < 4.6) & (AA < 0.3)].mean() if hair.any() else 0
    if says.get('chin') == 'gap':                     # a clean bare band round the lip patch, down to where the
        col = AA < 0.15                               # photos' chin beard starts (Vance: "halfway up the chin")
        up = [b for b in np.unique(BB) if 4.0 < b < 5.0 and hair[col & (BB >= b) & (BB <= 5.0)].mean() > 0.8]
        b_bot = min(up) if up else 4.5
        gap = (BB > 3.98) & (BB < b_bot) & (AA < 0.85) & ~((AA < 0.16) & (BB < 4.24))
        hair = hair & ~gap
        keep = hair
        G = np.where(gap, 0.0, G)
    if says.get('moustache') in ('thin', 'medium'):
        keep_from = 2.0 - (0.2 if says['moustache'] == 'thin' else 0.6)
        cut = (BB > 0.7) & (BB < keep_from) & (AA < 1.3)
        hair = hair & ~cut
        keep = hair
        G = np.where(cut, 0.0, G)
    if says.get('chin') == 'goatee':
        fill = (BB > 3.95) & (BB < 5.0) & (AA < 1.25 + (BB - 3.95) * 0.5)        # out to the jaw band
        notch = (BB > 3.98) & (BB < 4.2) & (AA > 0.28 + (BB - 3.98) * 1.3) & (AA < 0.95 - (BB - 3.98) * 1.3)   # small V
        hair = hair | (fill & ~notch)
        keep = hair
        G = np.where(fill & ~notch, np.maximum(G, 0.8), G)
    # the moustache meets the beard at the mouth corners whenever there are both (both finals; Sam, 4 Nov: "the
    # thin moustache meets it at the mouth corners")
    has_m = hair[(BB > 1.75) & (BB < 2.0) & (AA < 0.5)].mean() > 0.5 if hair.any() else False
    has_b = hair[(BB > 3.5) & (BB < 5.0) & (AA > 1.4)].mean() > 0.5 if hair.any() else False
    if has_m and has_b and says.get('corners') != 'apart':
        bridge = (BB > 1.75) & (BB < 4.0) & (AA > 0.92) & (AA < 1.32)
        hair = hair | bridge
        keep = hair
        G = np.where(bridge, np.maximum(G, 0.8), G)
    field = np.where(cv2.dilate(keep.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0, np.maximum(G, keep * 0.55), 0)
    shapes = shapes_of(field, As, Bs)
    # colours: the hair's own share of skin, its darkest part, the moustache, the light hairs
    lum = R.mean(-1)
    h = lum[hair]
    spec = dict(name=name, photos=[os.path.relpath(p) for p in paths], warnings=warns, shapes=shapes)
    if h.size:
        base = np.median(R[hair], 0)
        lum_s = cv2.GaussianBlur(np.where(hair, lum, np.median(h)).astype(np.float32), (0, 0), 2.5)
        hs = lum_s[hair]
        dark = hair & (lum_s < np.percentile(hs, 25)) & (lum_s < np.median(hs) * 0.85)
        dark &= cv2.erode(hair.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
        dark &= (BB > 4.25) | (AA > 1.55)                     # the jaw's underside and sides, never the mouth's corners
        dark = cv2.morphologyEx(dark.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0
        spec['dark_shapes'] = shapes_of(cv2.GaussianBlur(dark.astype(np.float32), (0, 0), 1.2), As, Bs, min_cells=60)
        # the moustache: hair between the nose's base and the mouth line, tapering out to the mouth corners
        bc = (Bs[:, None] - 0.9) / (2.6 - 0.9)
        mz = hair & (bc > 0) & (bc < 1) & (As[None, :] < 0.55 + 0.55 * np.sqrt(np.clip(bc, 0, 1)))
        spec['moustache_shapes'] = shapes_of(cv2.GaussianBlur(mz.astype(np.float32), (0, 0), 1.0), As, Bs, min_cells=10)
        # colours from the strands themselves (sure hair pixels by lightness), not cell averages that mix in the skin
        # showing through: base at the 60th centile of lightness, the dark band at the 40th, the moustache at the
        # 60th of its own pixels, the light (salt) hairs at the 90th made greyer (Vance's approved beard, 7 Nov)
        def band_col(px, q):
            l = px.mean(1)
            sel = px[(l > np.percentile(l, q - 10)) & (l < np.percentile(l, q + 10))]
            return np.median(sel, 0)
        cols = dict(base=[], dark=[], moustache=[], grain=[], spread=[])
        import likeness as LK
        for path, img, Q, score in faces:
            sk = np.median(np.concatenate([img[int(Q[i][1]) - 10:int(Q[i][1]) + 11,
                                               int(Q[i][0]) - 10:int(Q[i][0]) + 11].reshape(-1, 3) for i in SKIN_AT]), 0)
            sure = score > 0.85
            px = img[sure].reshape(-1, 3).astype(float)
            if len(px) < 300:
                continue
            cols['base'].append(band_col(px, 60) / sk)
            cols['dark'].append(band_col(px, 40) / sk)
            ys, xs = np.mgrid[0:img.shape[0], 0:img.shape[1]]
            mzp = sure & (ys > Q[2][1] + 4) & (ys < Q[0][1] - 2) & (np.abs(xs - (Q[61][0] + Q[291][0]) / 2) <
                                                                   abs(Q[291][0] - Q[61][0]) / 2)
            if mzp.sum() > 80:
                cols['moustache'].append(band_col(img[mzp].reshape(-1, 3).astype(float), 60) / sk)
            hi = band_col(px, 90)
            grey = hi.mean()
            cols['grain'].append((hi * 0.5 + grey * 0.5) / sk)
            l = px.mean(1)
            cols['spread'].append(np.percentile(l, 90) / max(1.0, np.percentile(l, 50)))
        mean = {k: np.mean(v, 0) for k, v in cols.items() if v}
        dark_hair = np.mean([np.mean(d) for d in cols['dark']]) < 0.37      # the 40th centile against the skin
        colour = says.get('colour') or ('dark' if dark_hair else 'ash')
        spec['colour_word'] = colour
        if colour == 'dark':                                  # near-black, even: one tone, no silver
            mean['base'] = np.mean(cols['dark'], 0) * 0.7 + 0.3          # the strands, with a little skin through
            mean['dark'] = mean['base']
            mean['moustache'] = mean['base']
            mean['spread'] = 1.0
        spec['base'] = [float(x) for x in mean['base']]
        spec['dark'] = [float(x) for x in mean['dark']]
        lum_d = float(np.mean(mean['base']) - np.mean(mean['dark']))
        if lum_d < 0.04 or not dark.any():
            spec['dark_shapes'] = []                           # an even beard (black, say): no band
        if 'moustache' in mean:
            spec['moustache'] = [float(x) for x in mean['moustache']]
            spec['moustache_own'] = bool(np.abs(mean['moustache'] - mean['base']).mean() > 0.04)
            if not spec['moustache_own']:
                spec['moustache_shapes'] = []
        spread = float(mean['spread'])
        spec['grain'] = [float(x) for x in mean['grain']] if spread > 1.35 else None
        spec['grain_spread'] = spread
    spec['coverage'] = float(hair.mean())
    spec['reads'] = reads(hair, AA, BB, spec, chin_mid, says)
    out_dir = out_dir or os.path.dirname(paths[0])
    jpath = os.path.join(out_dir, f'{name}-beard.json')
    json.dump(spec, open(jpath, 'w'), indent=1)
    if 'base' not in spec:                                    # no beard hair found in any photo: nothing to draw
        return jpath, None, spec
    sheet = check_sheet(spec, faces, G, As, Bs, os.path.join(out_dir, f'{name}-beard.jpg'))
    return jpath, sheet, spec


LEVELS = [(0.5, 'the eyes'), (1.15, "the nose's base"), (2.1, 'the upper lip'), (3.1, 'the mouth line'),
          (4.1, 'the lower lip'), (4.8, 'the chin'), (99, 'the jaw')]


def level(b):
    return next(name for lim, name in LEVELS if b < lim)


def moustache_depth(hair, AA, BB):
    """How far the moustache reaches up from the upper lip's top (b = 2) towards the nose's base (b = 1)."""
    col = hair[:, 0] if hair.ndim == 2 else hair
    bs = BB[:, 0]
    cols = AA[0] < 0.25
    rows = [b for b, h in zip(bs, hair[:, cols].mean(1) > 0.5) if h and 0.9 < b < 2.0]
    return (2.0 - min(rows)) if rows else 0.0


def reads(hair, AA, BB, spec, chin_mid, says):
    """What the photos show, in plain words, for Sam to confirm or correct (each line a switch for --says)."""
    def frac(m):
        return hair[m].mean() if m.any() else 0.0
    d = moustache_depth(hair, AA, BB)
    must = says.get('moustache') or ('none' if d == 0 else f"from the upper lip up to {level(2.0 - d)} (say thin, medium "
                                                          f"or full: the photos can't judge thickness)")
    patch = 'yes' if frac((AA < 0.3) & (BB > 4.0) & (BB < 4.2)) > 0.5 else 'no'
    col = AA < 0.15
    up = [b for b in np.unique(BB) if 4.0 < b < 5.0 and frac(col & (BB >= b) & (BB <= 5.0)) > 0.8]
    reach = (5.0 - min(up)) if up else 0.0
    chin = says.get('chin') or ('goatee' if chin_mid > 0.5 else 'gap')

    def top(a0, a1):
        rows = [b for b in np.unique(BB) if frac((AA > a0) & (AA < a1) & (BB == b)) > 0.5]
        return min(rows) if rows else 99
    t_out, t_mid = top(1.8, 2.0), top(1.25, 1.5)
    cheeks = 'bare' if t_out > 6 else f"covered: the top edge runs from {level(t_out)} at the face's edge to {level(t_mid)} mid-cheek"
    return [f"moustache: {must}",
            f"patch under the lip: {patch}",
            f"chin: {chin} ({'filled' if chin == 'goatee' else f'bare in the middle; the beard comes {reach:.0%} of the way up the chin'})",
            f"cheeks: {cheeks}",
            f"colour: {spec.get('colour_word', '?')} ({'ash brown with silver, darker under the jaw' if spec.get('colour_word') == 'ash' else 'near-black, even'})"]


def load(path):
    return json.load(open(path))


# ---------------------------------------------------------------------------------------------- drawing
def _col(share, skin):
    return tuple(int(max(0, min(255, round(s * c)))) for s, c in zip(share, skin))


def _inside(poly, x, y):
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
            c = not c
    return c


def _tufted(pts, amps, step, seed, hole=False):
    """A closed outline as a row of small sharp tufts (Vance's approved beard): the ring is resampled at even
    spacing, smoothed a little, and every other point pushed out by its amplitude (amps per input point) towards
    the skin: away from the middle for an outer edge, into the hole for a hole."""
    import random
    rng = random.Random(seed)
    P = np.array(pts, float)
    A = np.array(amps, float)
    seg = np.r_[np.hypot(*np.diff(np.r_[P, P[:1]], axis=0).T)]
    cum = np.r_[0, np.cumsum(seg)]
    total = cum[-1]
    n = max(8, int(total / (step / 2)))
    t = np.linspace(0, total, n, endpoint=False)
    R = np.c_[np.interp(t, cum, np.r_[P[:, 0], P[0, 0]]), np.interp(t, cum, np.r_[P[:, 1], P[0, 1]])]
    Ar = np.interp(t, cum, np.r_[A, A[0]])
    for _ in range(2):                                            # a light smoothing of the guide line
        R = (np.roll(R, 1, 0) + 2 * R + np.roll(R, -1, 0)) / 4
    c = R.mean(0)
    out = []
    for i in range(n):
        q = R[i]
        if i % 2:
            tang = R[(i + 1) % n] - R[i - 1]
            nrm = np.array([tang[1], -tang[0]]) / (np.hypot(*tang) + 1e-9)
            if (np.dot(nrm, q - c) < 0) != hole:
                nrm = -nrm
            q = q + nrm * Ar[i] * rng.uniform(0.6, 1.0)
        out.append((float(q[0]), float(q[1])))
    return out


def draw(p, f, L, skin, spec, chin_w=0.4, seed=7):
    """Draw the facial hair on a face (patriots4 frame f, layout L) in house style. Call after the face's skin and
    outline, before the nose and mouth."""
    import random
    import patriots4_cast as P4
    from ed import INK
    rng = random.Random(seed)
    edge = cartoon_edge(L, chin_w)
    base = _col(spec['base'], skin)
    dark = _col(spec.get('dark', [c * 0.75 for c in spec['base']]), skin)
    face_poly = f.pts(P4.outline_uv(L, chin_w))

    sil = []
    for u, v in P4.outline_uv(L, chin_w):
        if v > 0.4:
            spill = 0.012 + 0.04 * max(0.0, (v - 0.8) / 0.2)
            du, dv = u, v - 0.55
            n = math.hypot(du, dv) + 1e-9
            sil.append((u + du / n * spill, v + dv / n * spill))
    sil = np.array(sorted(sil, key=lambda q: math.atan2(q[0], q[1] - 0.55)))
    dense = np.concatenate([np.linspace(sil[i], sil[i + 1], 8, endpoint=False) for i in range(len(sil) - 1)])

    def snap(u, v):
        x, y = f(u, v)
        if _inside(face_poly, x, y) and abs(u) < edge(min(v, 1.0)) - 0.01 and v < 0.985:
            return u, v
        d = ((dense - (u, v)) ** 2).sum(1)
        return tuple(dense[int(np.argmin(d))])

    def ring(shape_pts, seed_, hole=False):
        uv = [snap(*uv_of_ab(a, b, L, edge)) for a, b in shape_pts]
        amps = []
        for u, v in uv:                    # tufts where the edge faces skin; small ones on the silhouette
            x, y = f(u, v)
            inside = _inside(face_poly, x, y) and v < 0.97 and abs(u) < edge(v) - 0.025
            amps.append(0.012 if inside else 0.006)
        return uv, amps, f.pts(_tufted(uv, amps, 0.014, seed_, hole))

    bodies = []
    for k, sh in enumerate(spec['shapes']):
        uv, amps, poly = ring(sh['outer'], seed + k)
        p.poly(poly, base, None)
        holes = [ring(h, seed + 50 + k, True)[2] for h in sh['holes']]
        bodies.append((poly, holes, uv, amps))
    for k, sh in enumerate(spec.get('dark_shapes', [])):
        p.poly(ring(sh['outer'], seed + 100 + k)[2], dark, None)
        for h in sh['holes']:
            p.poly(ring(h, seed + 120 + k, True)[2], base, None)
    if spec.get('moustache_own'):                             # the moustache in its own colour
        mcol = _col(spec['moustache'], skin)
        for k, sh in enumerate(spec.get('moustache_shapes', [])):
            p.poly(ring(sh['outer'], seed + 200 + k)[2], mcol, None)
    for poly, holes, uv, amps in bodies:                       # the holes show skin (gaps, the mouth)
        for h in holes:
            p.poly(h, skin, None)
    if spec.get('grain'):
        gcol = _col(spec['grain'], skin)
        gcol = tuple(int(0.78 * g + 0.22 * b) for g, b in zip(gcol, base))
        mh = L['mw'] / 2
        for r, gv in enumerate(np.arange(0.46, 1.06, 0.042)):
            for gu in np.arange(-0.5 + (0.021 if r % 2 else 0.0), 0.5, 0.042):
                u, v = gu + rng.uniform(-0.015, 0.015), gv + rng.uniform(-0.015, 0.015)
                q = f(u, v)
                if not any(_inside(poly, q[0], q[1]) and not any(_inside(h, q[0], q[1]) for h in holes)
                           for poly, holes, _, _ in bodies):
                    continue
                if abs(u) < mh * 1.15 and L['nose_y'] < v < L['lip17'] + 0.03:
                    continue                                   # the moustache and the lip patch stay clean
                du, dv = -u * 0.5, 1.0
                n = math.hypot(du, dv)
                ln = rng.uniform(0.016, 0.024)
                p.line([q, f(u + du / n * ln, v + dv / n * ln)], gcol, 1.5)
    for poly, holes, uv, amps in bodies:                       # ink round the silhouette (below the jaw) only
        segs, cur = [], []
        for (u, v), a in zip(uv + uv[:1], amps + amps[:1]):
            if a < 0.01:
                cur.append(f(u, v))
            elif cur:
                segs.append(cur)
                cur = []
        if cur:
            segs.append(cur)
        for sgm in segs:
            if len(sgm) > 1:
                p.line(sgm, INK, 2.2)


# ---------------------------------------------------------------------------------------------- the check sheet
def empty_face(spec, out_size=520, L=None, skin=(232, 178, 152)):
    """The beard on an empty face (skin, ears, nose, lips) in the house style, for the check sheet."""
    import burnham as B
    import patriots4_cast as P4
    from ed import INK, curve, oval
    if L is None:
        L = P4.layout(P4.AVG)
    im = Image.new('RGBA', (1080, 1300), (255, 255, 255, 255))

    class Pen:
        def __init__(self, img):
            self.d = ImageDraw.Draw(img)

        def poly(self, pts, fill, line, w=2.0):
            pts = [tuple(map(float, q)) for q in pts]
            if fill:
                self.d.polygon(pts, fill=tuple(fill))
            if line:
                self.d.line(pts + [pts[0]], fill=tuple(line), width=max(1, int(round(w))))

        def line(self, pts, col, w=2.0):
            self.d.line([tuple(map(float, q)) for q in pts], fill=tuple(col), width=max(1, int(round(w))))

        def ell(self, x, y, rx, ry, fill, line, w=1.0):
            self.d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=fill, outline=line)
    p = Pen(im)
    pts = P4.outline_uv(L, 0.4)
    f = _BigFace(540, 300, 900)
    p.poly(f.pts(pts), skin, INK, 3)
    draw(p, f, L, skin, spec)
    P4.nose(p, f, L, skin)
    hw = L['mw'] / 2
    p.poly(f.pts([(-hw, L['lip13']), (0, L['lip0'] + 0.01), (hw, L['lip13']), (0, L['lip17'])]), (200, 128, 116), INK, 2)
    p.line(f.pts([(-hw, L['lip13']), (hw, L['lip13'])]), INK, 2)
    return im.convert('RGB').crop((140, 300 + int(0.3 * 900) - 40, 940, 300 + int(1.12 * 900)))


class _BigFace:
    """A plain front-on frame for the check sheet: u, v to pixels."""
    tq = 0.0

    def __init__(self, cx, top, size):
        self.cx, self.top, self.s = cx, top, size

    def __call__(self, u, v):
        return (self.cx + u * self.s, self.top + v * self.s)

    def pts(self, uv):
        return [self(u, v) for u, v in uv]


def check_sheet(spec, faces, G, As, Bs, out):
    tiles = []
    H = 520
    for path, img, Q, score in faces:
        y0, y1 = int(Q[6][1]), int(min(img.shape[0], Q[152][1] + 0.25 * (Q[152][1] - Q[6][1])))
        x0 = int(max(0, Q[234][0] - 30))
        x1 = int(min(img.shape[1], Q[454][0] + 30))
        crop = Image.fromarray(img[y0:y1, x0:x1])
        heat = np.zeros((y1 - y0, x1 - x0, 3), np.uint8)
        heat[..., 0] = (score[y0:y1, x0:x1] * 255).astype(np.uint8)
        heat[..., 2] = (score[y0:y1, x0:x1] * 120).astype(np.uint8)
        over = Image.blend(crop, Image.fromarray(heat), 0.5)
        k = H / crop.height
        tiles.append(crop.resize((int(crop.width * k), H)))
        tiles.append(over.resize((int(crop.width * k), H)))
    g = (np.concatenate([G[:, ::-1], G], 1) * 255).astype(np.uint8)          # the grid, both halves
    gt = Image.fromarray(g).resize((int(H * 2 * NA / NB * 1.2), H), Image.NEAREST).convert('RGB')
    tiles.append(gt)
    ours = empty_face(spec)
    k = H / ours.height
    tiles.append(ours.resize((int(ours.width * k), H)))
    W = sum(t.width for t in tiles) + 12 * (len(tiles) - 1)
    sheet = Image.new('RGB', (W, H + 46), (232, 228, 222))
    d = ImageDraw.Draw(sheet)
    from midterminal_cast import FONT
    font = ImageFont.truetype(FONT, 24)
    x = 0
    labels = []
    for path, *_ in faces:
        labels += [os.path.basename(path)[:22], 'hair map']
    labels += ['grid', 'ours (empty face)']
    for t, lab in zip(tiles, labels):
        sheet.paste(t, (x, 46))
        d.text((x + 6, 10), lab, fill=(30, 30, 30), font=font)
        x += t.width + 12
    sheet.save(out, quality=88)
    return out


# ---------------------------------------------------------------------------------------------- CLI
if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or args[0] != 'analyse':
        print(__doc__)
        sys.exit(0)
    out = None
    if '--out' in args:
        i = args.index('--out')
        out = args[i + 1]
        args = args[:i] + args[i + 2:]
    says = {}
    if '--says' in args:
        i = args.index('--says')
        says = dict(kv.strip().split('=') for kv in args[i + 1].split(',') if '=' in kv)
        args = args[:i] + args[i + 2:]
    j, s, spec = analyse(args[1], args[2:], out, says)
    print('  what the photos show (correct any line with --says "chin=goatee, colour=dark"):')
    for line in spec['reads']:
        print('    ' + line)
    for w in spec['warnings']:
        print('  ' + w)
    print(f"  coverage {spec['coverage']:.2f}; shapes {len(spec['shapes'])}; dark {len(spec.get('dark_shapes', []))}; "
          f"moustache own colour: {spec.get('moustache_own')}; salt-and-pepper grain: {bool(spec.get('grain'))} "
          f"(spread {spec.get('grain_spread', 0):.2f})")
    print(j)
    print(s)
