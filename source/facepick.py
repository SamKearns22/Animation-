#!/usr/bin/env python3
"""MAP  facepick (13 Nov, ranking item 2, "likeness in one sitting"; Sam: Y). From a likeness pack, one command
makes THREE heads that differ on the card's unsure measures, each tuned until likeness.py's check passes, and lays
them on one sheet beside the photos at phone size, with the name test packed. Sam picks one; the film builds on it.

Why: Walliams' face took five chats (18.6% of a week) because every step was by hand: measures read off the card,
a drawing pushed by eye (x2 when it needed x8), the silhouette guessed (a pear, then a box), the check run, the
push changed, again. The steps that worked are now done by the tool:
    SILHOUETTE  hair, neck and shoulders are TRACED from the photo's own segmentation (likeness.segment), laid on
                the cartoon face's frame (anchored at the eyes, chin and cheek width), smoothed into flat house
                shapes with an ink edge (rule 49.1: the outline at phone size first). Hair over the forehead and
                down the sides is drawn over the face; the eyes and brows are never covered.
    PUSH        a closed loop, not a guess (rule 49.2): each head is drawn, measured by the same face finder, and
                every measure moved until the drawing differs from the average face the same way as the photo and
                at least `GAIN` times as far (the drawing style's own pull taken away with the average twin).
    CLEAN TWIN  the head is measured bare: no glasses, no beard (rule 49.3); they are drawn after, from the photo
                (glasses: the frames' size and colour from the segmentation; beard: beardkit).
    THREE HEADS the card's unsure measures (the photos disagree, or a smile moves them) are drawn three ways:
                A as the card says, B at the average, C the other way (Walliams' nose: the card said short, by eye
                it was long). With nothing unsure, the three differ in strength (x1.3, x1.7, x2.3).

    python3 source/facepick.py NAME OUT_DIR FRONT.jpg[:N] ... [--tq PHOTO[:N] ...] [--lineup "A,B,..."]
                               [--gain 1.6] [--says "beard=yes|no, glasses=yes|no"]
        FRONT photos: straight on, close, not smiling, current (rule 49: 3+); ':N' picks face N (0 = leftmost).
        --tq: three-quarter photos, shown on the sheet only. --lineup: look-alike names for the name test.
        Writes OUT_DIR/NAME-sheet.jpg (Sam's sheet), NAME-A.png .. NAME-C.png (the heads, glasses and beard on),
        NAME-pick.json (each head's measures: what the film's head code reads), check sheets, name-test packs.
    python3 source/facepick.py sheet OUT_DIR NAME     redraw the sheet, adding the name test's answers once in
    python3 source/facepick.py head OUT_DIR NAME A OUT.png [--size 600]   one picked head, for the cast code

Map: pack and card 60 | the frame 120 | traced shapes 150 | the head 215 | glasses 300 | tuning 340 |
     the sheet 400 | main 480
"""
import glob
import json
import os
import sys

os.environ.setdefault('GLOG_minloglevel', '3')
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '3')

import numpy as np                                       # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import likeness as LK                                    # noqa: E402
import patriots4_cast as P4                              # noqa: E402  (the measured face layout and its parts)
from ed import INK, Pen, curve                           # noqa: E402

FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
KEYS = [k for k, *_ in LK.MEASURES]
GAIN = 1.6            # the drawing differs from the average this many times as far as the photo (check wants 0.9+)
ROUNDS = 5            # tuning rounds per head
SC = 3                # canvas pixels per person unit (the head is ~200 units tall)
HX, HY = 200, 190     # where the face sits on the canvas (person units): Face.top = HY - 72
CW, CH = 400, 460


# ---------------------------------------------------------------------------------------------- pack and card
def _split(arg):
    if ':' in os.path.basename(arg):
        p, n = arg.rsplit(':', 1)
        return p, int(n)
    return arg, None


def card(fronts):
    """The card (likeness.analyse on the front photos) and the measures it is unsure of, most distinctive first."""
    paths, faces = zip(*fronts)
    A = LK.analyse(list(paths), list(faces) if any(f is not None for f in faces) else None)
    spread = LK.baseline(LK.is_smiling({}))['spread']
    dev = {r['key']: r['dev'] for r in A['diffs']}
    unsure = [r for r in A['diffs'] if r['warn'] and abs(r['dev']) > LK.NOTICE]
    unsure.sort(key=lambda r: ('disagree' not in r['warn'], -abs(r['dev'])))
    return A, dev, spread, [r['key'] for r in unsure[:3]], {r['key']: r['words'] for r in A['diffs']}


# ---------------------------------------------------------------------------------------------- the frame
def photo_frame(path, n):
    """The first front photo's segmentation crop and the affine that takes the cartoon face's (u, v) into it:
    the eyes' midpoint and level, the chin, and the cheek width line up (the photo's own proportions kept)."""
    im, faces = LK.find_faces(path)
    face = faces[n if n is not None else int(np.argmax([f['box'][1][0] - f['box'][0][0] for f in faces]))]
    crop, mask, box = LK.segment(im, face)
    P = face['P']
    kx, ky = 512 / (box[2] - box[0]), 512 / (box[3] - box[1])
    q = lambda i: np.array([(P[i, 0] - box[0]) * kx, (P[i, 1] - box[1]) * ky])
    er, el = (q(33) + q(133)) / 2, (q(362) + q(263)) / 2
    mid = (er + el) / 2
    ax = (el - er) / np.linalg.norm(el - er)                  # along the eyes
    ay = np.array([-ax[1], ax[0]])                            # down the face
    chin = float((q(152) - mid) @ ay)
    cheek = float(abs((q(454) - q(234)) @ ax))
    return dict(im=im, face=face, crop=crop, mask=mask, box=box, mid=mid, ax=ax, ay=ay, chin=chin, cheek=cheek,
                ipd=float(np.linalg.norm(el - er)), q=q)


def _uv_to_photo(fr, L):
    """2x3 matrix: canvas pixel (X, Y) -> segmentation crop pixel, for this head's layout L."""
    # canvas -> (u, v): u = (X/SC - HX)/H, v = (Y/SC - top)/H
    top = HY - 72
    H = P4.H
    # (u, v) -> photo: along = u / fw * cheek ; down = (v - eye_y) / (1 - eye_y) * chin
    sa = fr['cheek'] / L['fw']
    sd = fr['chin'] / (1.0 - L['eye_y'])
    # canvas X -> u: u = X/(SC*H) - HX/H ; v = Y/(SC*H) - top/H
    M = np.zeros((2, 3))
    for r in range(2):
        a, d = fr['ax'][r], fr['ay'][r]
        M[r, 0] = a * sa / (SC * H)
        M[r, 1] = d * sd / (SC * H)
        M[r, 2] = fr['mid'][r] + a * sa * (-HX / H) + d * sd * (-top / H - L['eye_y'])
    return M


def _warp(fr, L, sel):
    """A 0/1 mask from the photo's segmentation, laid on the canvas and smoothed into a flat shape."""
    m = Image.fromarray((sel * 255).astype(np.uint8))
    M = _uv_to_photo(fr, L)
    out = m.transform((CW * SC, CH * SC), Image.AFFINE, tuple(M.flatten()), resample=Image.BILINEAR)
    out = out.filter(ImageFilter.GaussianBlur(SC * 2.2))
    return np.asarray(out) > 127


# ---------------------------------------------------------------------------------------------- traced shapes
def traced(fr, n_fronts=()):
    """The masks the head is built on: hair (this person's own, not a neighbour's), body skin, clothes, glasses."""
    m, P = fr['mask'], fr['face']['P']
    q = fr['q']
    top, chin = q(10), q(152)
    hair = LK._own_region(m == 1, top, chin)
    return dict(hair=hair, skin2=(m == 2), clothes=(m == 4), acc=(m == 5))


def colours(fr, shapes):
    """Flat house colours measured from the photo: skin, hair, brows, lips, clothes."""
    px = np.asarray(fr['crop']).astype(float)
    m = fr['mask']
    q = fr['q']
    cheek = np.zeros(m.shape, bool)
    for i in (50, 280, 101, 330):
        x, y = q(i).astype(int)
        cheek[y - 6:y + 6, x - 6:x + 6] = True
    sk = px[cheek & (m == 3)] if (cheek & (m == 3)).sum() > 20 else px[m == 3]
    skin = LK._flat(np.median(sk, 0), 1.05)
    hair = LK._flat(np.median(px[shapes['hair']], 0)) if shapes['hair'].sum() > 50 else LK._dk(skin, 0.5)
    lip_m = Image.new('L', m.shape[::-1], 0)
    ImageDraw.Draw(lip_m).polygon([tuple(q(i)) for i in LK.LIPS_OUT], fill=255)
    ImageDraw.Draw(lip_m).polygon([tuple(q(i)) for i in LK.LIPS_IN], fill=0)
    lp = px[np.asarray(lip_m) > 0]
    lip = LK._flat(np.median(lp, 0), 1.0) if len(lp) > 10 else LK._dk(skin, 0.85)
    brow_m = Image.new('L', m.shape[::-1], 0)
    for ring in (LK.BROW_R, LK.BROW_L):
        ImageDraw.Draw(brow_m).polygon([tuple(q(i)) for i in ring], fill=255)
    bp = px[np.asarray(brow_m) > 0]
    brow = LK._flat(np.percentile(bp, 30, axis=0)) if len(bp) > 10 else LK._dk(hair, 0.8)
    cl = px[shapes['clothes']]
    cloth = LK._flat(np.median(cl, 0)) if len(cl) > 50 else (40, 44, 60)
    acc = px[shapes['acc']]
    rim = LK._flat(np.percentile(acc, 25, axis=0)) if len(acc) > 30 else (30, 28, 30)
    return dict(skin=skin, hair=hair, lip=lip, brow=brow, cloth=cloth, rim=rim)


def _ink_edge(mask, w=2.4):
    """The ink line round a flat shape: the mask grown by a line's width, minus itself."""
    from scipy import ndimage
    r = max(1, int(round(w * SC / 2)))
    return ndimage.binary_dilation(mask, iterations=r) & ~mask


def _paint(img, mask, colr, ink=True, w=2.4):
    a = np.asarray(img).copy()
    a[mask] = colr + (255,) if len(a.shape) == 3 and a.shape[2] == 4 else colr
    if ink:
        a[_ink_edge(mask, w)] = INK + (255,) if a.shape[2] == 4 else INK
    img.paste(Image.fromarray(a))


# ---------------------------------------------------------------------------------------------- the head
class Cam:
    def P(self, x, y):
        return x * SC, y * SC

    def S(self, v):
        return v * SC


def _face_mask(f, L):
    m = Image.new('L', (CW * SC, CH * SC), 0)
    ImageDraw.Draw(m).polygon([(x * SC, y * SC) for x, y in curve(f.pts(P4.outline_uv(L)), 4)], fill=255)
    return np.asarray(m) > 0


def draw_head(meas, fr, shapes, col, out, extras=True, beard=None, glasses=None):
    """One head, front on, on a white canvas: traced shoulders, neck and hair; the measured face; then (extras)
    the glasses and beard. meas: the 16 measures to draw (likeness.MEASURES' keys)."""
    import ad_vanced_notice_cast as AV
    L = P4.layout(meas)
    f = P4.Face(HX, HY)
    img = Image.new('RGB', (CW * SC, CH * SC), (255, 255, 255))
    p = Pen(img, Cam())
    face = _face_mask(f, L)
    rows = np.arange(CH * SC)[:, None] / SC
    below_chin = rows > (f.top + 0.9 * P4.H)
    _paint(img, _warp(fr, L, shapes['clothes']) & below_chin, col['cloth'])
    neck = _warp(fr, L, shapes['skin2']) & below_chin
    _paint(img, neck, col['skin'])
    hair = _warp(fr, L, shapes['hair'])
    if hair.any():                                            # no white gap between the traced hair and the face
        from scipy import ndimage
        both = ndimage.binary_closing(hair | face, iterations=4 * SC)
        top_half = rows < (f.top + L['eye_y'] * P4.H)
        hair = hair | (ndimage.binary_fill_holes(both) & ~face & (top_half | hair))
    _paint(img, hair & ~face, col['hair'])
    p = Pen(img, Cam())                                       # (the paste replaced the pixels: a fresh pen)
    AV._ears(p, f, L, col['skin'])
    p.poly(curve(f.pts(P4.outline_uv(L)), 4), col['skin'], INK, 2.6)
    if extras and beard:
        import beardkit
        beardkit.draw(p, f, L, col['skin'], beard)
    P4.eyes(p, f, L, dict(lid4=0.1), (66, 46, 34), P4.dk(col['skin'], 0.8), liner=2.8)
    P4.brows(p, f, L, col['brow'], 0.04)
    P4.nose(p, f, L, col['skin'])
    P4.lips(p, f, L, dict(smile=0.0), col['lip'], f(0.0, L['lip13']))
    # hair over the face: the hairline, a fringe, side curtains; never over the eyes and brows
    xs = np.arange(CW * SC)[None, :] / SC
    u = (xs - HX) / P4.H
    v = (rows - f.top) / P4.H
    keep = (v < L['brow_y'] - 0.05) | (np.abs(u) > L['ecx'] + L['ew'] * 0.75)
    front = hair & face & keep
    if front.any():
        _paint(img, front, col['hair'], ink=False)
        edge = _ink_edge(front, 2.2) & face
        a = np.asarray(img).copy()
        a[edge] = INK
        img.paste(Image.fromarray(a))
    if extras and glasses:
        draw_glasses(Pen(img, Cam()), f, L, glasses)
    img.save(out)
    return L


# ---------------------------------------------------------------------------------------------- glasses
def glasses_of(fr, shapes):
    """Each lens's frame from the photo's accessory mask, as a box relative to its eye (in eye widths), or None."""
    acc, q = shapes['acc'], fr['q']
    if acc.sum() < 200:
        return None
    ys, xs = np.nonzero(acc)
    pts = np.stack([xs, ys], 1) - fr['mid']
    a, d = pts @ fr['ax'], pts @ fr['ay']
    ew = (np.linalg.norm(q(33) - q(133)) + np.linalg.norm(q(362) - q(263))) / 2
    half = fr['ipd'] / 2
    boxes = []
    for sgn in (-1, 1):
        sel = (np.sign(a) == sgn) & (np.abs(d) < ew * 1.6)
        if sel.sum() < 50:
            return None
        aa, dd = np.abs(a[sel]), d[sel]
        boxes.append(dict(inner=float(np.percentile(aa, 3) / half), outer=float(np.percentile(aa, 97) / half),
                          top=float(np.percentile(dd, 3) / ew), bot=float(np.percentile(dd, 97) / ew)))
    g = {k: float(np.mean([b[k] for b in boxes])) for k in boxes[0]}
    g['rim_w'] = float(min(0.35, max(0.12, (g['bot'] - g['top']) * 0.14)))
    return g


def draw_glasses(p, f, L, g, colr=(30, 28, 30)):
    """Thick flat frames (house style): a rounded box round each eye at the photo's size, the bridge, the arms."""
    colr = tuple(g.get('colr', colr))
    half, ew = L['ecx'], L['ew']
    lw = g['rim_w'] * ew * P4.H
    for sgn in (-1, 1):
        x0, x1 = sorted((sgn * g['inner'] * half, sgn * g['outer'] * half))
        y0, y1 = L['eye_y'] + g['top'] * ew, L['eye_y'] + g['bot'] * ew
        r = 0.22
        box = [(x0, y0 + (y1 - y0) * r), (x0 + (x1 - x0) * r, y0), (x1 - (x1 - x0) * r, y0), (x1, y0 + (y1 - y0) * r),
               (x1, y1 - (y1 - y0) * r), (x1 - (x1 - x0) * r * 1.3, y1), (x0 + (x1 - x0) * r * 1.3, y1),
               (x0, y1 - (y1 - y0) * r)]
        pts = curve(f.pts(box), 3)
        p.line(pts + pts[:1], INK, lw * 1.0 + 2.2)
        p.line(pts + pts[:1], colr, lw)
        xo = x1 if sgn > 0 else x0
        p.line(f.pts([(xo, y0 + (y1 - y0) * 0.3), (sgn * L['fw'] * 0.5, y0 + (y1 - y0) * 0.3)]), colr, lw * 0.8)
    xi = g['inner'] * half
    yb = L['eye_y'] + g['top'] * ew + (g['bot'] - g['top']) * ew * 0.3
    p.line(curve(f.pts([(-xi, yb), (0.0, yb - 0.01), (xi, yb)]), 3), colr, lw * 0.8)


# ---------------------------------------------------------------------------------------------- tuning
def _devs(png):
    try:
        B = LK.analyse([png])
    except SystemExit:
        return None
    return {r['key']: r['dev'] for r in B['diffs']}


def tune(target, fr, shapes, col, out, rounds=ROUNDS, log=print):
    """Draw, measure, move each measure towards the target (spreads from the average, the style's pull taken
    away), again. Returns the measures drawn and the last reading."""
    spread = LK.baseline(False)['spread']
    twin = os.path.splitext(out)[0] + '-average.png'
    draw_head(dict(P4.AVG), fr, shapes, col, twin, extras=False)
    bias = _devs(twin) or {k: 0.0 for k in KEYS}
    x = {k: 1.6 * target[k] for k in KEYS}
    best = None
    for r in range(rounds):
        meas = {k: P4.AVG[k] + x[k] * spread[k] for k in KEYS}
        draw_head(meas, fr, shapes, col, out, extras=False)
        got = _devs(out)
        if got is None:                                       # the finder lost the face: pull everything back
            x = {k: v * 0.7 for k, v in x.items()}
            continue
        d = {k: got[k] - bias[k] for k in KEYS}
        va, vb = np.array([target[k] for k in KEYS]), np.array([d[k] for k in KEYS])
        score = float(va @ vb / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-9))
        short = [k for k in KEYS if abs(target[k]) > LK.NOTICE and
                 (np.sign(d[k]) != np.sign(target[k]) or abs(d[k]) < abs(target[k]) * 0.9 / GAIN * 1.0)]
        log(f'   round {r + 1}: match {score * 100:.0f}%, short of the target: {", ".join(short) or "none"}')
        if best is None or score > best[0]:
            best = (score, dict(meas), d)
        if score > 0.9 and not short:
            break
        for k in KEYS:
            x[k] = float(np.clip(x[k] + 0.5 * (target[k] - d[k]), -9, 9))   # damped: the measures pull on each other
    score, meas, d = best
    draw_head(meas, fr, shapes, col, out, extras=False)
    return meas, score


# ---------------------------------------------------------------------------------------------- the sheet
def _font(n):
    return ImageFont.truetype(FONT, n)


def _face_tile(path, n, h, pad=(0.55, 0.75, 0.55, 0.45)):
    im, faces = LK.find_faces(path)
    f = faces[n if n is not None else int(np.argmax([f['box'][1][0] - f['box'][0][0] for f in faces]))]
    (x0, y0), (x1, y1) = f['box']
    s = max(x1 - x0, y1 - y0)
    box = (int(x0 - pad[0] * s), int(y0 - pad[1] * s), int(x1 + pad[2] * s), int(y1 + pad[3] * s))
    c = Image.new('RGB', (box[2] - box[0], box[3] - box[1]), (255, 255, 255))   # past the edge: white, not black
    c.paste(im.convert('RGB'), (-box[0], -box[1]))
    return c.resize((max(1, int(c.width * h / c.height)), h), Image.LANCZOS), f


def _head_tile(png, h):
    """The head cut the way the photo tiles are: the face box padded the same, so sizes compare."""
    return _face_tile(png, None, h)[0]


def _phone(tile, face_px):
    """How a tile looks on a phone with the face this many pixels tall in a 1920-tall video (then enlarged x2
    with hard pixels, so the sheet shows the real detail a phone gets)."""
    k = face_px / (tile.height / 1.75)
    sm = tile.resize((max(1, int(tile.width * k)), max(1, int(tile.height * k))), Image.LANCZOS)
    return sm.resize((sm.width * 2, sm.height * 2), Image.NEAREST)


def sheet(out_dir, name):
    meta = json.load(open(os.path.join(out_dir, f'{name}-pick.json')))
    th = 420
    photos = [(_split(a), 'photo') for a in meta['fronts']] + [(_split(a), '3/4') for a in meta['tq']]
    ptiles = [(_face_tile(p, n, th)[0], lab) for (p, n), lab in photos]
    htiles = [(_head_tile(os.path.join(out_dir, f'{name}-{v}.png'), th), v) for v in 'ABC']
    W = max(sum(t.width + 12 for t, _ in ptiles), sum(t.width + 12 for t, _ in htiles) + 40) + 20
    W = max(W, 1500)
    lines = []
    for v in 'ABC':
        h = meta['heads'][v]
        nt = h.get('named', '')
        lines.append((f"{v}: {h['what']}", (0, 0, 0)))
        lines.append((f"    likeness {h['score']:.0f}% ({h['good']} good, {h['timid']} timid, {h['wrong']} wrong way), "
                      f"line-up {h['rank']}{nt}", (0, 110, 40) if h['pass'] else (170, 90, 0)))
    small_h = 0
    strip = []
    for t, _ in ptiles[:3] + htiles:
        s = _phone(t, 70)
        strip.append(s)
        small_h = max(small_h, s.height)
    H = 60 + th + 50 + th + 70 + small_h + 40 + 30 * len(lines) + 30
    img = Image.new('RGB', (W, H), (238, 236, 232))
    d = ImageDraw.Draw(img)
    d.text((14, 14), f"{meta['title']}: pick A, B or C (photos on top, heads below, phone size underneath)",
           font=_font(28), fill=(20, 20, 20))
    x, y = 14, 60
    for t, lab in ptiles:
        img.paste(t, (x, y))
        d.text((x + 6, y + 6), lab, font=_font(22), fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        x += t.width + 12
    x, y = 14, 60 + th + 50
    for t, v in htiles:
        img.paste(t, (x, y))
        d.text((x + 8, y + 6), v, font=_font(54), fill=(20, 20, 20))
        x += t.width + 12
    y = 60 + 2 * th + 110
    d.text((14, y - 30), 'phone size (the face 70 px tall in a 1920 video): photos, then A, B, C', font=_font(20),
           fill=(60, 60, 60))
    x = 14
    for i, s in enumerate(strip):
        img.paste(s, (x, y))
        x += s.width + (30 if i == 2 else 8)
    y += small_h + 20
    for t, colr in lines:
        d.text((14, y), t, font=_font(22), fill=colr)
        y += 30
    path = os.path.join(out_dir, f'{name}-sheet.jpg')
    img.save(path, quality=86)
    return path


# ---------------------------------------------------------------------------------------------- main
def _others(name, fronts):
    """Other people's front photos from every film's likeness folder, for the check's line-up."""
    own = {os.path.dirname(os.path.abspath(_split(a)[0])) for a in fronts}
    cands = sorted(glob.glob(os.path.join(HERE, '..', 'references', '*', 'likeness', '*front*.jpg')) +
                   glob.glob(os.path.join(HERE, '..', 'references', 'faces', '*', '*front*.jpg')))
    seen, out = set(), []
    for c in cands:
        d = os.path.dirname(os.path.abspath(c))
        tag = (d, os.path.basename(c)[:1])
        if d in own or tag in seen or name.lower()[:4] in c.lower():
            continue
        seen.add(tag)
        out.append(c)
    return out[:9]


def make(name, out_dir, fronts, tq=(), lineup=(), gain=GAIN, says=None, log=print, rounds=ROUNDS):
    os.makedirs(out_dir, exist_ok=True)
    says = says or {}
    F = [_split(a) for a in fronts]
    A, dev, spread, unsure, words = card(F)
    log(f'{name}: card on {len(F)} front photos; unsure: {", ".join(unsure) or "none"}')
    fr = photo_frame(*F[0])
    shapes = traced(fr)
    col = colours(fr, shapes)
    g = glasses_of(fr, shapes)
    if says.get('glasses') == 'no':
        g = None
    if g:
        g['colr'] = list(col['rim'])
    beard = None
    bs = A['shapes'] or {}
    if says.get('beard') == 'yes' or (says.get('beard') != 'no' and (bs.get('beard', 0) > 0.2 or bs.get('moustache', 0) > 0.4)):
        import beardkit
        try:
            beard = beardkit.analyse(name, [F[0][0]], out_dir)[2]
        except Exception as e:                                # the beard is drawn after; never stops the heads
            log(f'   beardkit skipped: {e}')
    if unsure:
        ways = {'A': 1.0, 'B': 0.0, 'C': -0.8}
        what = {'A': ', '.join(words[k] for k in unsure) + ' (as the card)',
                'B': ', '.join(k.replace('_', ' ') for k in unsure) + ': average',
                'C': ', '.join(k.replace('_', ' ') for k in unsure) + ': the other way'}
        targets = {v: {k: gain * dev[k] * (ways[v] if k in unsure else 1.0) for k in KEYS} for v in 'ABC'}
    else:
        st = {'A': 1.3 / 1.7, 'B': 1.0, 'C': 2.3 / 1.7}
        what = {v: f'every measure x{gain * st[v]:.1f}' for v in 'ABC'}
        targets = {v: {k: gain * st[v] * dev[k] for k in KEYS} for v in 'ABC'}
    others = _others(name, fronts)
    heads = {}
    for v in 'ABC':
        log(f'{name} {v}: {what[v]}')
        png = os.path.join(out_dir, f'{name}-{v}.png')
        meas, sc = tune(targets[v], fr, shapes, col, png, rounds, log)
        clean = os.path.join(out_dir, f'{name}-{v}-clean.png')
        os.replace(png, clean)
        os.replace(os.path.splitext(png)[0] + '-average.png', os.path.splitext(clean)[0] + '-average.png')
        res = _check(F[0], clean, os.path.join(out_dir, f'{name}-{v}-check.jpg'), others)
        draw_head(meas, fr, shapes, col, png, extras=True, beard=beard, glasses=g)
        heads[v] = dict(what=what[v], measures=meas, **res)
    meta = dict(title=name, fronts=list(fronts), tq=list(tq), unsure=unsure, gain=gain, glasses=g,
                beard=bool(beard), colours={k: list(c) for k, c in col.items()}, heads=heads,
                card={k: round(dev[k], 2) for k in KEYS})
    json.dump(meta, open(os.path.join(out_dir, f'{name}-pick.json'), 'w'), indent=1)
    if lineup:
        import nametest
        for v in 'ABC':
            nametest.pack(os.path.join(out_dir, f'nt-{name}-{v}'), os.path.join(out_dir, f'{name}-{v}.png'),
                          lineup=lineup)
    return sheet(out_dir, name)


def _check(front, clean, out, others):
    """likeness.check's own verdict on the clean head (as rule 49 runs it), read back from its printout."""
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        score = LK.check(front[0], clean, out, front[1], None, others)
    txt = buf.getvalue()
    good = timid = wrong = 0
    for ln in txt.splitlines():
        if ' good, ' in ln and 'too timid' in ln:
            parts = ln.strip().split()
            good, timid, wrong = int(parts[0]), int(parts[2]), int(parts[5])
    rank = '?'
    for ln in txt.splitlines():
        if 'closest to number' in ln:
            rank = ln.split('number', 1)[1].split('(')[0].strip()
    first = rank.startswith('1 ')
    return dict(score=(score or 0) * 100, good=good, timid=timid, wrong=wrong, rank=rank,
                **{'pass': bool(score and score >= 0.6 and wrong == 0 and first)})


def _says(s):
    return dict(kv.split('=', 1) for kv in (s or '').replace(' ', '').split(',') if '=' in kv)


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    o = LK._opts(args, ('--tq', '--lineup', '--gain', '--says', '--size'), multi=('--tq',))
    if args[0] == 'sheet':
        print(sheet(args[1], args[2]))
    elif args[0] == 'head':
        out_dir, name, v, out = args[1:5]
        print(os.path.join(out_dir, f'{name}-{v}.png'), '->', out)
        Image.open(os.path.join(out_dir, f'{name}-{v}.png')).save(out)
    else:
        name, out_dir, fronts = args[0], args[1], args[2:]
        lu = [s.strip() for s in o.get('--lineup', '').split(',') if s.strip()]
        print(make(name, out_dir, fronts, o.get('--tq', ()), lu, float(o.get('--gain', GAIN)), _says(o.get('--says'))))
