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
    PUSH        a search, not a guess (rule 49.2), judged by verdict(): likeness.check's own rule on its own photo
                (the FIRST front photo), line-up included. The face finder reads cartoons jumpily (a 0.1-spread
                change moves some readings 0.2), so no step-by-step solve settles: response() measures once how each
                setting moves the drawing; tune() starts at the photo's measures x GAIN and draws 6 heads a round
                round the best (one solved on that table, five shaken and pushed at what is still timid or wrong).
    CLEAN TWIN  the head is measured bare: no glasses, no beard, no age lines (rule 49.3); they are drawn after
                (age lines: agelines.py, each crease's depth measured in the front photos), from the photo
                (glasses: each lens's centre, width, top and bottom in eye widths, drawn by the cartoon's eye width;
                beard: beardkit). Hair: the top's colour and, if the temples are lighter, soft grey sides; a few strands,
                or braids (braid_score: the photo hair's fine ripple; plaits below the brows, lines from a parting).
    THREE HEADS the card's unsure measures (the photos disagree) are drawn three ways: A as the first photo, B half
                as far, C further (or the other way where that photo does not notice it: the check only judges
                what it notices). With nothing unsure, the three differ in strength (x1.3, x1.7, x2.3).
    LINE-UP     every film's '*front*' photo, one per person (faces packs, likeness folders, each film's own).

    python3 source/facepick.py NAME OUT_DIR FRONT.jpg[:N] ... [--tq PHOTO[:N] ...] [--lineup "A,B,..."]
                               [--gain 1.6] [--says "beard=yes|no, glasses=yes|no, age=N, hair=braids|plain"]
        FRONT photos: straight on, close, not smiling, current (rule 49: 3+); ':N' picks face N (0 = leftmost).
        --tq: three-quarter photos, shown on the sheet only. --lineup: look-alike names for the name test.
        Writes OUT_DIR/NAME-sheet.jpg (Sam's sheet), NAME-A.png .. NAME-C.png (the heads, glasses and beard on),
        NAME-pick.json (each head's measures: what the film's head code reads), check sheets, name-test packs.
    python3 source/facepick.py sheet OUT_DIR NAME     redraw the sheet, adding the name test's answers once in
    python3 source/facepick.py head OUT_DIR NAME A OUT.png [--size 600]   one picked head, for the cast code
    python3 source/facepick.py redraw OUT_DIR NAME    the heads again from NAME-pick.json's checked measures with
                               today's extras (eyes, braids, age lines, glasses): seconds, no tuning
    EYES (eye_look, 14 Nov): the eyes' dark share and socket shade measured from the photos; fuller, darker irises
                and a flat socket shade, drawn after the check like the glasses (the face finder reads either one as
                a brow or eye change: Burnham C 62% -> 34%, two the wrong way). Bigger eyes break the check too.
    PICKS      references/faces/NAME/pick/: Sam's pick (NAME-pick.json 'picked') and its head; the film reads these.

Map: pack and card 66 | the frame 85 | traced shapes 132 | the head 284 | glasses 379 | tuning 430 |
     the sheet 576 | main 706
"""
import glob
import math
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
ROUNDS = 6            # search rounds per head at most (it stops once the check passes with nothing timid)
POP = 6               # heads drawn per round (about 1 s each)
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
    return dict(hair=hair, skin2=(m == 2), clothes=(m == 4), acc=(m == 5),
                temple_y=float(top[1] + 0.12 * (chin[1] - top[1])))


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
    skin = _tone(np.median(sk, 0), 1.06, 0.82)          # photos run warm and ruddy: lighter, a little greyer
    hair, hair2 = _hair_tones(px, shapes)
    if hair is None:
        hair = LK._dk(skin, 0.5)
    lip_m = Image.new('L', m.shape[::-1], 0)
    ImageDraw.Draw(lip_m).polygon([tuple(q(i)) for i in LK.LIPS_OUT], fill=255)
    ImageDraw.Draw(lip_m).polygon([tuple(q(i)) for i in LK.LIPS_IN], fill=0)
    lp = px[np.asarray(lip_m) > 0]
    lip = LK._flat(np.median(lp, 0), 1.0) if len(lp) > 10 else LK._dk(skin, 0.85)
    brow_m = Image.new('L', m.shape[::-1], 0)
    for ring in (LK.BROW_R, LK.BROW_L):
        ImageDraw.Draw(brow_m).polygon([tuple(q(i)) for i in ring], fill=255)
    bp = px[np.asarray(brow_m) > 0]
    brow = _tone(np.percentile(bp, 12, axis=0), 0.95, 1.0) if len(bp) > 10 else LK._dk(hair, 0.8)
    fh = float(np.linalg.norm(q(152) - q(10)))                # the brow's thickness, in face heights
    ln = (np.linalg.norm(q(70) - q(107)) + np.linalg.norm(q(300) - q(336))) / 2
    fr['brow_th'] = float(np.clip((np.asarray(brow_m) > 0).sum() / 2 / max(ln, 1) / fh * 1.15, 0.03, 0.075))
    cl = px[shapes['clothes']]
    cloth = LK._flat(np.median(cl, 0)) if len(cl) > 50 else (40, 44, 60)
    acc = px[shapes['acc']]
    rim = LK._flat(np.percentile(acc, 25, axis=0)) if len(acc) > 30 else (30, 28, 30)
    return dict(skin=skin, hair=hair, hair2=hair2, lip=lip, brow=brow, cloth=cloth, rim=rim)


def _tone(rgb, lift=1.0, sat=1.0):
    """A photo colour made flat: lifted, and its saturation scaled (likeness._flat always adds 15%, which turns
    skin pink)."""
    r, g, b = [min(255.0, v * lift) for v in rgb]
    m = (r + g + b) / 3
    return tuple(int(np.clip(m + (v - m) * sat, 0, 255)) for v in (r, g, b))


def _eye_photo(path, n=None):
    """One front photo's eyes: the dark share of the eye opening (iris and lash shadow: hooded, dark eyes read near
    1, wide pale ones near 0.4), its colour, and the socket's brightness (lid to brow) over the cheeks' own, so the
    reading is fair to every skin tone."""
    im, faces = LK.find_faces(path)
    if not faces:
        return None
    face = faces[n if n is not None else int(np.argmax([f['box'][1][0] - f['box'][0][0] for f in faces]))]
    P = face['P']
    a = np.asarray(im.convert('RGB')).astype(float)
    lum = a @ [0.299, 0.587, 0.114]

    def poly(idx):
        m = Image.new('L', im.size, 0)
        ImageDraw.Draw(m).polygon([tuple(P[i, :2]) for i in idx], fill=255)
        return np.asarray(m) > 0
    r = max(2, int(0.06 * np.linalg.norm(P[33, :2] - P[263, :2])))
    skin = float(np.median(np.concatenate([lum[int(P[i, 1]) - r:int(P[i, 1]) + r, int(P[i, 0]) - r:int(P[i, 0]) + r].ravel()
                                          for i in (50, 280, 101, 330)])))
    eye = poly(LK.EYE_R) | poly(LK.EYE_L)
    dark = lum[eye] < 0.55 * skin
    sock = poly([246, 161, 160, 159, 158, 157, 173, 55, 65, 52, 53, 46]) | \
        poly([466, 388, 387, 386, 385, 384, 398, 285, 295, 282, 283, 276])
    return dict(dark=float(dark.mean()), sock=float(np.median(lum[sock]) / skin),
                iris=np.median(a[eye][dark], 0).tolist() if dark.sum() > 5 else None)


def eye_look(F):
    """How dark and deep-set the eyes read, from every front photo (the median), as the extras draw them after the
    check (rule 49.3): the iris's size in the opening (iris_r, in eye heights: 0.95 the house's, up to 1.45 for eyes
    that are nearly all iris in the photos), its colour, and a flat socket shade under the brow (0 none .. 1).
    Set on 14 Nov from 16 front photos of 6 people: dark share 0.4-1.0 (Burnham 0.85), socket 0.2-0.8 (Burnham
    0.45, Badenoch 0.65, Walliams 0.75; glasses rims darken it a little). Burnham's helpers: 'his big dark eyes; the
    cartoon's are small', while his measured eye size is average: the darkness, not the size, is what reads."""
    ms = [m for m in (_eye_photo(p, n) for p, n in F) if m]
    if not ms:
        return None
    dark = float(np.median([m['dark'] for m in ms]))
    sock = float(np.median([m['sock'] for m in ms]))
    ir = [m['iris'] for m in ms if m['iris']]
    k = float(np.clip((dark - 0.5) / 0.35, 0, 1))
    return dict(scale=1.0, dark=round(dark, 2), sock=round(sock, 2), iris_r=round(0.95 + 0.5 * k, 2),
                pupil_r=round(0.42 + 0.2 * k, 2), iris=list(LK._dk(np.median(ir, 0), 1.0)) if ir else None,
                shade=round(float(np.clip((0.6 - sock) / 0.2, 0, 1)), 2))


def _sockets(p, f, L, skin, look):
    """The socket shade: a flat crescent of darker skin from the upper lid up to under the brow (house style: one
    flat shape, no ink), drawn before the eyes."""
    if not look or look.get('shade', 0) < 0.1:
        return
    c = LK._dk(skin, 1 - 0.16 * look['shade'])
    for sgn in (-1, 1):
        ecx, ew, ey, by = L['ecx'], L['ew'], L['eye_y'], L['brow_y']
        top = by + 0.012
        pts = [(ecx - 0.62 * ew, ey), (ecx - 0.55 * ew, top + 0.4 * (ey - top)), (ecx - 0.2 * ew, top),
               (ecx + 0.45 * ew, top + 0.05 * (ey - top)), (ecx + 0.85 * ew, top + 0.55 * (ey - top)), (ecx + 0.62 * ew, ey)]
        p.poly(curve(f.pts([(sgn * u, v) for u, v in pts]), 4), c, None)


def _hair_tones(px, shapes):
    """The hair's colours: the top's (its mean, so salt-and-pepper reads as the grey it is, not black) and, when
    the sides at the temples are clearly lighter (greying), the sides' too; sets shapes['hair_lt'] to the sides."""
    hm = shapes['hair']
    shapes['hair_lt'] = np.zeros_like(hm)
    if hm.sum() < 50:
        return None, None
    ty = int(shapes['temple_y'])
    top, side = hm.copy(), hm.copy()
    top[ty:] = False
    side[:ty] = False
    lum = lambda c: float(np.asarray(c) @ [0.299, 0.587, 0.114])
    ct = px[top].mean(0) if top.sum() > 50 else px[hm].mean(0)
    if side.sum() < 120 or lum(px[side].mean(0)) - lum(ct) < 6:
        return _tone(px[hm].mean(0), 1.0, 0.9), None
    shapes['hair_lt'] = side
    return _tone(ct, 1.0, 0.9), _tone(px[side].mean(0), 1.3, 0.6)   # greying pushed, as the measures are


def _strands(img, hair, face, colr, top_px):
    """A few strand lines in the hair's mass above the face: arcs following the hair's outline a little inside
    it, broken into pieces (house style: a hint of the comb's direction, not drawn hair)."""
    import cv2
    m = (hair & ~face).astype(np.uint8)
    m[int(top_px + 0.1 * P4.H * SC):] = 0
    if m.sum() < 400 * SC * SC:
        return
    dist = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    p = Pen(img, Cam())
    for lev, gap in ((0.3, 0), (0.58, 1)):
        cs, _ = cv2.findContours((dist > lev * dist.max()).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for c in cs:
            c = c[:, 0, :].astype(float)
            if len(c) < 60 * SC:
                continue
            c = c[c[:, 1] < top_px + 0.02 * P4.H * SC]       # the upper arc only (the outline's inside along the top)
            n, run = len(c), int(26 * SC)
            for i in range(gap * run // 2, n - run // 2, int(run * 1.6)):
                seg = c[i:i + run:max(1, SC)]
                if len(seg) > 4 and np.abs(np.diff(seg, axis=0)).max() < 4 * SC:
                    p.line([(x / SC, y / SC) for x, y in seg], colr, 1.5)


def braid_score(fr, shapes):
    """How braided the photo's hair is: the fine light-dark ripple inside the hair below the eyes (each braid's
    plaits catch the light), as the ripple's strength over the hair's own brightness spread. Braids ~0.5+,
    straight or short hair under 0.3 (13 Nov: Badenoch 0.6; Burnham, Walliams no hair there)."""
    from scipy import ndimage
    g = np.asarray(fr['crop'].convert('L')).astype(float)
    ey = float(fr['mid'][1])
    hm = shapes['hair'].copy()
    hm[:int(ey)] = False
    hm = ndimage.binary_erosion(hm, iterations=4)
    if hm.sum() < 1500:
        return 0.0
    fine = g - ndimage.gaussian_filter(g, max(1.5, 0.04 * fr['ipd']))
    return float(np.std(fine[hm]) / max(8.0, np.std(g[hm]) + 1e-6))


def _braids(img, hair, face, f, L, light):
    """Braids, house style: below the brows, columns of small stacked chevrons down the hair (each a plait); over
    the crown, lines from a middle parting down to the sides. Drawn only on the hair, never on the face."""
    p = Pen(img, Cam())
    h, w = hair.shape
    inside = lambda x, y: 0 <= int(y * SC) < h and 0 <= int(x * SC) < w and hair[int(y * SC), int(x * SC)] \
        and not face[int(y * SC), int(x * SC)]
    step, colw = 0.028 * P4.H, 0.042 * P4.H
    y0 = f.top + (L['brow_y'] - 0.02) * P4.H
    ys = np.nonzero(hair.any(1))[0]
    if not len(ys):
        return
    ytop, ybot = ys.min() / SC, ys.max() / SC
    # where each plait starts: not one level line (a hard band at brow height, chat 3) but higher towards the
    # outside, as the crown lines curve down the sides, and a little uneven column to column; the crown lines stop
    # where the plaits take over, so each line runs on into a plait
    start = lambda x: (y0 - 0.16 * P4.H * float(np.clip((abs(x - f.cx) - 0.25 * P4.H) / (0.35 * P4.H), 0, 1))
                       + 0.03 * P4.H * math.sin(x * 1.7))
    for x in np.arange(f.cx - 1.2 * P4.H, f.cx + 1.2 * P4.H, colw):
        for y in np.arange(start(x), ybot, step):
            if inside(x, y) and inside(x, y + step):
                p.line([(x - colw * 0.36, y), (x, y + step * 0.75), (x + colw * 0.36, y)], light, 1.7)
    for a in np.linspace(-1.0, 1.0, 13):                      # the crown: from the parting down to each side
        top = (f.cx, ytop + 0.04 * P4.H)
        pts = [(f.cx + a * 0.62 * P4.H * t, top[1] + (y0 - top[1]) * (t ** 0.8)) for t in np.linspace(0.05, 1, 12)]
        run = [q for q in pts if inside(*q) and q[1] < start(q[0]) + step]
        if len(run) > 3:
            p.line(run, light, 1.3)


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


def _grey_sides(img, hair, f, L, colr):
    """Greying temples: the lighter colour blended in softly over both sides of the hair below the temples (the
    photo's lighter sides, mirrored: a hard cut along the photo's temple line drew a square patch on one side)."""
    from scipy import ndimage
    h, w = hair.shape
    u = (np.arange(w)[None, :] / SC - f.cx) / P4.H
    v = (np.arange(h)[:, None] / SC - f.top) / P4.H
    wt = np.clip((v - (L['brow_y'] - 0.12)) / 0.12, 0, 1) * np.clip((np.abs(u) - L['fw'] * 0.32) / 0.1, 0, 1)
    wt = np.clip(ndimage.gaussian_filter(wt * hair, 4 * SC) * 1.8, 0, 0.9) * hair
    a = np.asarray(img).astype(float)
    a = a * (1 - wt[..., None]) + np.array(colr, float)[None, None, :] * wt[..., None]
    img.paste(Image.fromarray(a.astype(np.uint8)))


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
    from scipy import ndimage
    clothes = _warp(fr, L, shapes['clothes']) & below_chin
    xs = np.arange(CW * SC)[None, :] / SC
    column = (np.abs(xs - f.cx) < 0.37 * L['jw'] * P4.H) & (rows > f.top + 0.7 * P4.H)   # the neck under the jaw
    neck = (_warp(fr, L, shapes['skin2']) & below_chin) | (column & ~below_chin)
    near = (np.abs(xs - f.cx) < 0.6 * L['fw'] * P4.H) & (rows > f.top + 0.78 * P4.H)
    wedge = ndimage.binary_closing(face | clothes | neck, iterations=8 * SC) & near   # jaw-to-shoulder slivers
    neck = (neck | wedge) & ~face & ~clothes
    _paint(img, neck, col['skin'])
    _paint(img, clothes, col['cloth'])
    hair = _warp(fr, L, shapes['hair'])
    if hair.any():                                            # no white gap between the traced hair and the face
        from scipy import ndimage
        both = ndimage.binary_closing(hair | face, iterations=4 * SC)
        top_half = rows < (f.top + L['eye_y'] * P4.H)
        hair = hair | (ndimage.binary_fill_holes(both) & ~face & (top_half | hair))
    _paint(img, hair & ~face, col['hair'])
    if col.get('hair2') and shapes.get('hair_lt') is not None and shapes['hair_lt'].any():
        _grey_sides(img, hair & ~face, f, L, col['hair2'])
    if shapes.get('braids'):
        _braids(img, hair, face, f, L, tuple(int(min(255, c + 85)) for c in col['hair']))
    else:
        _strands(img, hair, face, LK._dk(col['hair'], 0.55), f.top * SC)
    p = Pen(img, Cam())                                       # (the paste replaced the pixels: a fresh pen)
    AV._ears(p, f, L, col['skin'])
    p.poly(curve(f.pts(P4.outline_uv(L)), 4), col['skin'], INK, 2.6)
    if extras and beard:
        import beardkit
        beardkit.draw(p, f, L, col['skin'], beard)
    look = shapes.get('eyes') if extras else None   # the eyes' darkness, measured (eye_look), drawn after the check
    if look:
        _sockets(p, f, L, col['skin'], look)
        P4.eyes(p, f, L, dict(lid4=0.1), tuple(int(c) for c in (look.get('iris') or (66, 46, 34))),
                P4.dk(col['skin'], 0.8), liner=2.8 + 0.6 * look['shade'], iris_r=look['iris_r'], pupil_r=look['pupil_r'],
                scale=look.get('scale', 1.0))
    else:
        P4.eyes(p, f, L, dict(lid4=0.1), (66, 46, 34), P4.dk(col['skin'], 0.8), liner=2.8)
    P4.brows(p, f, L, col['brow'], fr.get('brow_th', 0.04))
    P4.nose(p, f, L, col['skin'])
    if extras and shapes.get('age'):     # the age lines measured from the photos (agelines), drawn AFTER the check like
        import agelines                  # a beard (rule 49.3): the face finder reads a cheek fold as the lips (A: chin
                                         # +0.4 -> -0.3, lip_low -0.35 -> -1.7) and crow's feet as the eyes' width
        agelines.draw(p, f, L, col['skin'], shapes['age'])
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
        lo, hi = np.percentile(aa, 3), np.percentile(aa, 97)
        boxes.append(dict(cx=float(((lo + hi) / 2 - half) / ew), w=float((hi - lo) / ew),
                          top=float(np.percentile(dd, 3) / ew), bot=float(np.percentile(dd, 97) / ew)))
    g = {k: float(np.mean([b[k] for b in boxes])) for k in boxes[0]}
    g['rim_w'] = float(min(0.3, max(0.1, (g['bot'] - g['top']) * 0.12)))
    return g


def draw_glasses(p, f, L, g, colr=(30, 28, 30)):
    """Thick flat frames (house style): a rounded box round each eye, sized and placed in the CARTOON's eye widths
    from the photo's (centre, width, top, bottom about each eye), the bridge, the arms. The lens top never rises
    past the brow's top edge, and the lenses never meet in the middle."""
    colr = tuple(g.get('colr', colr))
    half, ew = L['ecx'], L['ew']
    lw = g['rim_w'] * ew * P4.H
    y0 = max(L['eye_y'] + g['top'] * ew, L['brow_y'] - 0.03)
    y1 = L['eye_y'] + g['bot'] * ew
    for sgn in (-1, 1):
        c, w = half + g['cx'] * ew, g['w'] * ew
        x0, x1 = sorted((sgn * max(c - w / 2, 0.035), sgn * min(c + w / 2, L['fw'] * 0.52)))
        r = 0.14
        box = [(x0, y0 + (y1 - y0) * r), (x0 + (x1 - x0) * r, y0), (x1 - (x1 - x0) * r, y0), (x1, y0 + (y1 - y0) * r),
               (x1, y1 - (y1 - y0) * r), (x1 - (x1 - x0) * r * 1.3, y1), (x0 + (x1 - x0) * r * 1.3, y1),
               (x0, y1 - (y1 - y0) * r)]
        pts = curve(f.pts(box), 3)
        p.line(pts + pts[:1], INK, lw * 1.0 + 2.2)
        p.line(pts + pts[:1], colr, lw)
        xo = x1 if sgn > 0 else x0
        p.line(f.pts([(xo, y0 + (y1 - y0) * 0.3), (sgn * L['fw'] * 0.5, y0 + (y1 - y0) * 0.3)]), colr, lw * 0.8)
    xi = max(half + g['cx'] * ew - g['w'] * ew / 2, 0.035)
    yb = y0 + (y1 - y0) * 0.3
    p.line(curve(f.pts([(-xi, yb), (0.0, yb - 0.01), (xi, yb)]), 3), colr, lw * 0.8)


# ---------------------------------------------------------------------------------------------- tuning
def _devs(png):
    try:
        B = LK.analyse([png])
    except SystemExit:
        return None
    return {r['key']: r['dev'] for r in B['diffs']}


def verdict(ref, d, others_v=()):
    """likeness.check's own verdict, worked out here on the same numbers (so the tuning aims at what is judged):
    ref = the FIRST front photo's measures (check compares with that one only), d = the drawing's, its style's pull
    taken away. Score: the cosine over every measure; on the photo's noticeable measures, wrong way (the other sign
    and past 0.2) and timid (under 0.9 of the photo); line-up: the drawing closer to ref than to every other photo."""
    va, vb = np.array([ref[k] for k in KEYS]), np.array([d[k] for k in KEYS])
    cos = lambda a: float(a @ vb / (np.linalg.norm(a) * np.linalg.norm(vb) + 1e-9))
    score = cos(va)
    good, timid, wrong = [], [], []
    for k in KEYS:
        if abs(ref[k]) <= LK.NOTICE:
            continue
        if np.sign(d[k]) != np.sign(ref[k]) and abs(d[k]) > 0.2:
            wrong.append(k)
        elif abs(d[k]) < abs(ref[k]) * 0.9:
            timid.append(k)
        else:
            good.append(k)
    first = all(cos(np.array([o[k] for k in KEYS])) < score for o in others_v)
    ok = score >= 0.6 and not wrong and first
    return dict(score=score, good=good, timid=timid, wrong=wrong, first=first, ok=ok,
                key=(ok, -len(wrong), first, score - 0.04 * len(timid)))


def response(fr, shapes, col, out_dir, name, step=1.5, log=print):
    """How the drawing answers each of its 16 settings (once per person, ~16 s): the average head drawn and
    measured, then each setting moved `step` spreads alone. Returns the average head's reading (the style's own
    pull: check takes it away with the average twin) and J, where J[i, j] = how far measure i moves per spread of
    setting j. Some settings barely move their own measure (the lower lip, the jaw) and many move others (the
    mouth, lips and chin share the face's height), so the settings are solved together, not one by one."""
    spread = LK.baseline(False)['spread']
    tmp = os.path.join(out_dir, f'{name}-probe.png')
    draw_head(dict(P4.AVG), fr, shapes, col, tmp, extras=False)
    d0 = _devs(tmp)
    if d0 is None:
        raise SystemExit(f'{name}: the face finder cannot read the average head: the traced shapes hide the face')
    J = np.zeros((len(KEYS), len(KEYS)))
    for j, k in enumerate(KEYS):
        m = dict(P4.AVG)
        m[k] += step * spread[k]
        draw_head(m, fr, shapes, col, tmp, extras=False)
        d = _devs(tmp)
        if d is not None:
            J[:, j] = [(d[q] - d0[q]) / step for q in KEYS]
    os.remove(tmp)
    weak = [k for i, k in enumerate(KEYS) if abs(J[i, i]) < 0.15]
    log(f'   settings that barely move their own measure: {", ".join(weak) or "none"}')
    return d0, J


def _solve(J, off, target, ref, x0, lo=-6.0, hi=6.0):
    """The settings (in spreads) whose predicted reading J x + off best meets the target, with nothing predicted
    the wrong way on the photo's noticeable measures (a hinge), and a light pull towards the target itself for
    settings the drawing does not answer to."""
    from scipy.optimize import minimize
    t = np.array([target[k] for k in KEYS])
    r = np.array([ref[k] for k in KEYS])
    big = np.abs(r) > LK.NOTICE
    sg = np.sign(r)

    def f(x):
        d = J @ x + off
        e = d - t
        hinge = np.where(big, np.maximum(0.0, 0.35 - sg * d), 0.0)          # stay 0.35 clear of the wrong side
        timid = np.where(big, np.maximum(0.0, 0.95 * np.abs(r) - sg * d), 0.0)
        val = e @ e + 25 * hinge @ hinge + 2 * timid @ timid + 0.04 * (x - t) @ (x - t)
        g = 2 * J.T @ e - 50 * J.T @ (hinge * sg) - 4 * J.T @ (timid * sg) + 0.08 * (x - t)
        return val, g
    lo, hi = np.broadcast_to(lo, x0.shape), np.broadcast_to(hi, x0.shape)
    res = minimize(f, np.clip(x0, lo, hi), jac=True, method='L-BFGS-B', bounds=list(zip(lo, hi)))
    return res.x


def tune(target, fr, shapes, col, out, rounds=ROUNDS, log=print, ref=None, others_v=(), resp=None, seed=0):
    """A small search, judged by verdict() exactly as the check judges (the face finder reads cartoons jumpily: a
    0.1-spread change moves some readings 0.2, so no step-by-step solve settles). Start at the target (each
    setting as far as the photo, times the gain); then each round draws POP heads round the best so far: one
    solved on the response table (the table learning from every head drawn, Broyden's way), the rest shaken at
    random and pushed towards whatever the best head still has timid or the wrong way. The best head is kept;
    a round with no gain shrinks the shaking. Stops once it passes with nothing timid, or after `rounds` rounds."""
    ref = ref or target
    rng = np.random.default_rng(seed)
    spread = LK.baseline(False)['spread']
    bias, J = resp
    J = J.copy()
    twin = os.path.splitext(out)[0] + '-average.png'
    draw_head(dict(P4.AVG), fr, shapes, col, twin, extras=False)
    sg = np.sign([ref[k] for k in KEYS])
    best, sigma, n = None, 0.6, 0

    def drawn(x):
        meas = {k: P4.AVG[k] + x[i] * spread[k] for i, k in enumerate(KEYS)}
        draw_head(meas, fr, shapes, col, out, extras=False)
        got = _devs(out)
        if got is None:
            return None, None, meas
        d = np.array([got[k] - bias[k] for k in KEYS])
        return d, verdict(ref, dict(zip(KEYS, d)), others_v), meas

    x0 = np.clip(np.array([target[k] for k in KEYS]), -6, 6)
    for r in range(rounds * 2):                               # the second half only while it has not passed
        if r >= rounds and best is not None and best[0]['ok']:
            break
        if best is None:
            cands = [x0] if r == 0 else [x0 * (0.8 ** r)]
        else:
            xb, db, vb = best[2], best[3], best[0]
            bad = np.array([k in vb['timid'] or k in vb['wrong'] for k in KEYS], float)
            cands = [_solve(J, db - J @ xb, target, ref, xb, np.maximum(xb - 1.5, -6), np.minimum(xb + 1.5, 6))]
            for _ in range(POP - 1):
                push = bad * sg * rng.uniform(0.0, 1.2, len(KEYS))
                cands.append(np.clip(xb + rng.normal(0, sigma, len(KEYS)) + push, -6, 6))
        gained = False
        for x in cands:
            d, v, meas = drawn(x)
            n += 1
            if d is None:
                continue
            if best is not None:
                sx = x - best[2]
                if sx @ sx > 0.04:
                    J += np.outer((d - best[3]) - J @ sx, sx) / (sx @ sx) * 0.3
            if best is None or v['key'] > best[0]['key']:
                best, gained = (v, dict(meas), x.copy(), d), True
        if best is None:
            continue
        v = best[0]
        log(f"   round {r + 1} ({n} heads): best likeness {v['score'] * 100:.0f}%, timid: {', '.join(v['timid']) or 'none'}; "
            f"wrong way: {', '.join(v['wrong']) or 'none'}; line-up {'first' if v['first'] else 'NOT first'}")
        if v['ok'] and (not v['timid'] or (r >= 3 and not gained)):
            break
        sigma = sigma if gained else max(0.15, sigma * 0.6)
    v, meas = best[0], best[1]
    draw_head(meas, fr, shapes, col, out, extras=False)
    return meas, v


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


def _head_tile(png, h, frame=None):
    """The head cut the way the photo tiles are: padded round a face box, so sizes compare. All three heads share
    one box (the average twin's: same canvas, same place), so A, B and C are framed alike."""
    if frame and os.path.exists(frame):
        im, faces = LK.find_faces(frame)
        (x0, y0), (x1, y1) = faces[0]['box']
        s = max(x1 - x0, y1 - y0)
        c = Image.open(png).convert('RGB').crop((int(x0 - 0.55 * s), int(y0 - 0.75 * s), int(x1 + 0.55 * s),
                                                 int(y1 + 0.45 * s)))
        return c.resize((max(1, int(c.width * h / c.height)), h), Image.LANCZOS)
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
    htiles = [(_head_tile(os.path.join(out_dir, f'{name}-{v}.png'), th,
                          os.path.join(out_dir, f'{name}-A-clean-average.png')), v) for v in 'ABC']
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
    strip_w = sum(s.width + 8 for s in strip) + 22 + 28
    W = max(sum(t.width + 12 for t, _ in ptiles), sum(t.width + 12 for t, _ in htiles) + 40, strip_w) + 20
    W = max(W, 1500)
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
GENERIC = {'front', 'close', 'closer', 'full', 'three', 'quarter', 'threequarter', 'left', 'right', 'smiling',
           'talking', 'seated', 'walking', 'desk', 'sunglasses', 'eyesdown', 'pink', 'tie', 'rose', 'cuffs', 'bash',
           'winners', 'table', 'bench', 'armchair', 'and', 'back'}
THINGS = {'robot', 'van', 'set', 'sitting'}


def _who(path):
    """Who a reference photo shows: a faces pack's folder name, a likeness folder's letter, else the first name in
    the file name ('24-damon-front-closer' -> damon); '' for a photo of a thing or of nobody named."""
    path = os.path.abspath(path)
    d = os.path.dirname(path)
    if os.path.basename(os.path.dirname(d)) == 'faces':
        return os.path.basename(d)
    if os.path.basename(d) == 'likeness':
        return os.path.basename(path)[:1] + '@' + os.path.basename(os.path.dirname(d))
    toks = [t for t in os.path.splitext(os.path.basename(path))[0].lower().replace('_', '-').split('-')
            if t.isalpha() and len(t) > 2]
    if THINGS & set(toks) or THINGS & set(d.split(os.sep)):
        return ''
    return next((t for t in toks if t not in GENERIC), '')


def _others(name, fronts, most=14):
    """Other people's front photos from EVERY film's references (any '*front*' photo: the faces packs, the
    likeness folders, each film's own), one per person, for the check's line-up. Photos of things (vans, sets,
    robots) and unnamed ones are left out; a photo the face finder cannot read is dropped by the check itself."""
    root = os.path.join(HERE, '..', 'references')
    cands = sorted(set(glob.glob(os.path.join(root, '**', '*front*.jpg'), recursive=True)))
    seen, out = {name.lower()} | {_who(_split(a)[0]) for a in fronts}, []
    for c in cands:
        who = _who(c)
        if not who or who in seen or name.lower()[:4] in os.path.basename(c).lower():
            continue
        seen.add(who)
        out.append(os.path.abspath(c))
    return out[:most]


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
    ref = _devs(F[0][0]) if F[0][1] is None else {r['key']: r['dev'] for r in LK.analyse([F[0][0]], [F[0][1]])['diffs']}
    others = _others(name, fronts)
    shapes['braids'] = says.get('hair') == 'braids' or (says.get('hair') is None and braid_score(fr, shapes) > 0.45)
    log(f'   braids: {"yes" if shapes["braids"] else "no"} (ripple {braid_score(fr, shapes):.2f}; over 0.45 is braids)')
    if says.get('age') != 'no':                               # the creases, measured from every front photo
        import agelines
        shapes['age'] = agelines.person([(p, n) for p, n in F], others, says.get('age'))
        log('   age lines: ' + ', '.join(f'{k} {v:.2f} (deeper than {shapes["age"]["rank"].get(k, "-")})'
                                         for k, v in shapes['age']['strength'].items()))
    shapes['eyes'] = eye_look(F)
    log(f'   eyes: {shapes["eyes"]}')
    others_v = []
    for o in others:
        dv = _devs(o)
        if dv:
            others_v.append(dv)
    log(f'   line-up: {len(others_v)} other people')
    # the targets: the FIRST photo's measures (what the check compares with), pushed by the gain. The card's unsure
    # measures (the photos disagree) are drawn three ways: A as the photo, B half as far, C further; or C the other
    # way where the first photo does not notice it (the check only judges what that photo notices).
    if unsure:
        what, targets = {}, {}
        for v, kk in (('A', 1.0), ('B', 0.45), ('C', 1.8)):
            t = {k: gain * ref[k] for k in KEYS}
            ww = []
            for k in unsure:
                if v == 'C' and abs(ref[k]) <= LK.NOTICE:
                    t[k] = -0.8 * gain * dev[k]
                    ww.append(k.replace('_', ' ') + ' the other way')
                else:
                    t[k] = gain * ref[k] * kk
                    ww.append(words[k] if v == 'A' else k.replace('_', ' ') + (' half as far' if v == 'B' else ' further'))
            targets[v], what[v] = t, ', '.join(ww) + (' (as the photo)' if v == 'A' else '')
    else:
        st = {'A': 1.3 / 1.7, 'B': 1.0, 'C': 2.3 / 1.7}
        what = {v: f'every measure x{gain * st[v]:.1f}' for v in 'ABC'}
        targets = {v: {k: gain * st[v] * ref[k] for k in KEYS} for v in 'ABC'}
    resp = response(fr, shapes, col, out_dir, name, log=log)
    heads = {}
    for v in 'ABC':
        log(f'{name} {v}: {what[v]}')
        png = os.path.join(out_dir, f'{name}-{v}.png')
        meas, tv = tune(targets[v], fr, shapes, col, png, rounds, log, ref, others_v, resp)
        clean = os.path.join(out_dir, f'{name}-{v}-clean.png')
        os.replace(png, clean)
        os.replace(os.path.splitext(png)[0] + '-average.png', os.path.splitext(clean)[0] + '-average.png')
        res = _check(F[0], clean, os.path.join(out_dir, f'{name}-{v}-check.jpg'), others)
        if res['pass'] != tv['ok']:
            log(f'   (the tuning said {"pass" if tv["ok"] else "fail"}, the check says {"pass" if res["pass"] else "fail"}: '
                f'the check rules)')
        draw_head(meas, fr, shapes, col, png, extras=True, beard=beard, glasses=g)
        heads[v] = dict(what=what[v], measures=meas, **res)
    meta = dict(title=name, fronts=list(fronts), tq=list(tq), unsure=unsure, gain=gain, glasses=g,
                beard=bool(beard), age=shapes.get('age'), eyes=shapes.get('eyes'), braids=bool(shapes['braids']), colours={k: list(c) for k, c in col.items() if c}, heads=heads,
                card={k: round(dev[k], 2) for k in KEYS})
    json.dump(meta, open(os.path.join(out_dir, f'{name}-pick.json'), 'w'), indent=1)
    if lineup:
        import nametest
        for v in 'ABC':
            nametest.pack(os.path.join(out_dir, f'nt-{name}-{v}'), os.path.join(out_dir, f'{name}-{v}.png'),
                          lineup=lineup)
    return sheet(out_dir, name)


def redraw(out_dir, name):
    """The picked heads drawn again from NAME-pick.json's measures with today's extras (glasses, beard, age lines,
    eyes, braids), no tuning: the faces stay exactly as checked, so a fix to an extra costs seconds, not minutes."""
    meta = json.load(open(os.path.join(out_dir, f'{name}-pick.json')))
    F = [_split(a) for a in meta['fronts']]
    fr = photo_frame(*F[0])
    shapes = traced(fr)
    col = colours(fr, shapes)
    shapes['braids'] = meta.get('braids', braid_score(fr, shapes) > 0.45)
    if meta.get('age'):
        shapes['age'] = meta['age']
    shapes['eyes'] = meta['eyes'] = eye_look(F)
    beard = None
    if meta.get('beard'):
        import beardkit
        beard = beardkit.analyse(name, [F[0][0]], out_dir)[2]
    for v, h in meta['heads'].items():
        draw_head(h['measures'], fr, shapes, col, os.path.join(out_dir, f'{name}-{v}.png'), extras=True, beard=beard,
                  glasses=meta.get('glasses'))
    json.dump(meta, open(os.path.join(out_dir, f'{name}-pick.json'), 'w'), indent=1)
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
    elif args[0] == 'redraw':
        print(redraw(args[1], args[2]))
    elif args[0] == 'head':
        out_dir, name, v, out = args[1:5]
        print(os.path.join(out_dir, f'{name}-{v}.png'), '->', out)
        Image.open(os.path.join(out_dir, f'{name}-{v}.png')).save(out)
    else:
        name, out_dir, fronts = args[0], args[1], args[2:]
        lu = [s.strip() for s in o.get('--lineup', '').split(',') if s.strip()]
        print(make(name, out_dir, fronts, o.get('--tq', ()), lu, float(o.get('--gain', GAIN)), _says(o.get('--says'))))
