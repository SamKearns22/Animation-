"""PART OF facehouse.py: runs inside facehouse (one module, parts.py); import facehouse, never this file.
It holds the balaclava (Patriots 5 chat 1, 27 Nov: the Patriot brought into the house look).

MAP
  balaclava_front() .. The black knitted balaclava over a house head, front on: a hood fitted to the head's own
                       shape (a round crown, over the ears, down the jaw into the neck), an eye opening showing his
                       house eyes and brows, ribs, the rolled edge round the opening, the knit over the mouth moving
                       as he talks. Person lines: `balaclava` (and `bala_c`, `slot` to tune the opening).
  balaclava_turned() . The same hood from three-quarter, the side, three-quarter behind and behind: the turned
                       head's silhouette (with the nose) thickened by the knit, the opening carried round the face,
                       the ribs on the head's meridians.
  niqab_front/turned . Patriots 5 (brief row 17, Sam: "at least two" in black face veils over the balaclavas): a
                       black veil over the knit, a hood over the crown falling past the chin onto the chest and
                       shoulders, the eye slit the balaclava's own opening, a tie band over the brow, soft folds.
                       Person line: `niqab`.
  kufi_front/turned .. Patriots 5: a white knitted prayer cap on the crown, over the balaclava (`kufi`).
  _knit() ............ Paints a knit layer kept inside the hood's shape and out of the opening, then inks both.
  tables: BALA, BALA_RIB, BALA_EDGE
"""
if __name__ == 'facehouse_d': raise ImportError('facehouse_d is part of facehouse.py: import facehouse')
# ---------------------------------------------------------------------------------------------- the balaclava
BALA, BALA_RIB, BALA_EDGE = (30, 30, 34), (52, 52, 60), (58, 58, 66)    # The Patriots' knit (patriots3_cast)


def _talk_level(sp):
    """How far his jaw is open behind the knit (0 shut .. 1 wide), from the mouth shape the film gives him."""
    m = sp.get('mouth', 'rest')
    if isinstance(m, str) and m.startswith('v:'):
        return {'rest': 0.0, 'MBP': 0.0, 'etc': 0.45, 'E': 0.6, 'AI': 1.0, 'O': 0.8, 'U': 0.5, 'WQ': 0.4,
                'FV': 0.3, 'L': 0.6}.get(m[2:], 0.5)
    return {'talk': 0.6, 'shout': 1.0, 'open': 0.8, 'mid': 0.5, 'small': 0.3}.get(m, 0.0)


def _slot_uv(L, kh):
    """The eye opening in face units: a soft-cornered band from above the brows to under the eyes, out past the
    outer corners (The Patriots' opening, as wide as his eyes and brows need)."""
    s = kh.get('slot') or {}
    top = L['brow_y'] - s.get('above', 0.11)
    bot = L['eye_y'] + s.get('below', 0.085)
    w = L['ecx'] + L['ew'] * 0.5 + s.get('side', 0.085)
    r = min(0.05, (bot - top) * 0.35)
    pts = []
    for cx, cy, a0 in ((w - r, top + r, -90), (w - r, bot - r, 0), (-w + r, bot - r, 90), (-w + r, top + r, 180)):
        for a in np.linspace(a0, a0 + 90, 6):
            pts.append((cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)) * 0.9))
    # the knit sags a little in the middle of the lower edge and lifts over the brows' middle (it is cloth)
    return [(u, v + (0.012 * math.cos(u / w * math.pi / 2) if v > (top + bot) / 2 else -0.006 * math.cos(u / w * math.pi / 2)))
            for u, v in pts]


def _knit(img, p, outer, slot, ribs, mouth=None, lw=2.6, dilate=0, soften=0, fill=None, edge=None):
    """outer, slot: polygons in pen units (slot may be None); ribs(pen) draws the ribs; mouth: a polygon of the jaw
    working under the knit. The knit is kept inside `outer` (grown by `dilate` pixels) and out of `slot`."""
    from PIL import Image, ImageDraw
    import cv2
    import body as B
    base = p.pen if hasattr(p, 'pen') else p
    cam = base.cam
    W, Hh = img.size
    m = Image.new('L', img.size, 0)
    for poly in outer:
        ImageDraw.Draw(m).polygon([cam.P(*q) for q in poly], fill=255)
    a = np.asarray(m).copy()
    if dilate:
        k = 2 * int(dilate) + 1
        a = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
        a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k + 4, k + 4)))
    if soften:                                             # knit drapes: no hard corners at the jaw (back views)
        k = 2 * int(soften) + 1
        a = np.where(cv2.GaussianBlur(a, (k, k), soften / 2.0) > 127, 255, 0).astype(np.uint8)
    hole = np.zeros_like(a)
    if slot:
        hole_img = Image.new('L', img.size, 0)
        ImageDraw.Draw(hole_img).polygon([cam.P(*q) for q in slot], fill=255)
        hole = np.asarray(hole_img)
    hole = np.where(a > 0, hole, 0).astype(np.uint8)          # the opening only where the hood is (turned: its
    keep = np.where(hole > 0, 0, a).astype(np.uint8)          # far edge held on the head's outline)
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    pen = B.Pen(layer, cam)
    ImageDraw.Draw(layer).bitmap((0, 0), Image.fromarray(keep), fill=tuple(fill or BALA) + (255,))
    ribs(pen)
    if mouth:
        pen.poly(mouth, (16, 16, 19), None)
    al = np.asarray(layer)[:, :, 3].astype(np.uint16) * keep // 255
    layer.putalpha(Image.fromarray(al.astype(np.uint8)))
    img.alpha_composite(layer)
    d = ImageDraw.Draw(img)
    cs, _ = cv2.findContours(a, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    big = max((cv2.contourArea(c) for c in cs), default=0)
    for c in cs:                                           # the hood's edge, smoothed as the hair's is
        if cv2.contourArea(c) < 0.03 * big:
            continue
        c = c[:, 0, :].astype(float)
        k = max(3, len(c) // 80)
        c = np.array([c[np.arange(i - k, i + k + 1) % len(c)].mean(0) for i in range(len(c))])[::2]
        q = [(x, y) for x, y in c]
        d.line(q + q[:1], fill=INK, width=base.w(lw), joint='curve')
    if slot and hole.any():                                # the rolled edge round the opening, then its ink
        hs, _ = cv2.findContours(hole, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for c in hs:
            c = c[:, 0, :].astype(float)
            k = max(2, len(c) // 100)
            c = np.array([c[np.arange(i - k, i + k + 1) % len(c)].mean(0) for i in range(len(c))])[::2]
            q = [(x, y) for x, y in c]
            d.line(q + q[:1], fill=tuple(edge or BALA_EDGE), width=base.w(lw * 2.6), joint='curve')
            d.line(q + q[:1], fill=INK, width=base.w(2.2), joint='curve')


def _mouth_uv(L, lv):
    """The jaw working under the knit: a soft dark hollow over the mouth, taller as it opens."""
    hw, hh = L['mw'] * (0.42 - 0.08 * lv), 0.012 + 0.055 * lv
    cy = L['lip13'] + 0.02 * lv
    return [(hw * math.cos(a), cy + hh * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24, endpoint=False)]


def balaclava_front(img, p, f, L, kh, sp):
    W = max(_face_u(L, 0.0) + 0.1, L['fw'] * 0.5 + 0.08)          # over the temples (the hard hat's width)
    top = kh.get('bala_top', -0.5)
    vc = 0.12
    right = [(W * math.cos(a), vc - (vc - top) * math.sin(a)) for a in np.linspace(math.pi / 2, 0, 12)]
    ear = _face_u(L, 0.42) + 0.075                                    # over the ears: a soft bulge
    right += [(W + 0.02, 0.24), (ear, 0.38), (ear - 0.005, 0.52), (_face_u(L, 0.66) + 0.035, 0.66),
              (_face_u(L, 0.8) + 0.03, 0.8), (_face_u(L, 0.9) + 0.03, 0.9)]
    nk = kh.get('bala_neck', 0.24) * sp.get('neck_w', 1.0)                                    # down into the neck (the torso's neck: neck_c)
    nv = 1.12 if sp.get('collar') == 'band' else 1.3                  # a band collar shows round the neck (note 4)
    right += ([(max(nk, 0.3), 1.0), (nk, 1.06), (nk, nv - 0.02), (nk, nv), (nk * 0.5, nv)] if nv < 1.3 else
              [(max(nk, 0.3), 1.0), (nk, 1.1), (nk + 0.01, 1.3)])   # band: a square foot, no flare at the corners
    outer = curve(f.pts([(0.0, top)] + right + [(-u, v) for u, v in right[::-1]]), 4)
    slot = curve(f.pts(_slot_uv(L, kh)), 3)
    lv = _talk_level(sp)
    mouth = curve(f.pts(_mouth_uv(L, lv)), 3) if lv > 0.05 else None

    def ribs(pen):
        n = int(2 * (W + 0.03) / 0.045)
        for u in np.linspace(-W - 0.02, W + 0.02, n):
            bow = [(u * (0.86 + 0.14 * min(1.0, abs(v - 0.3) / 0.8)), v) for v in np.linspace(top - 0.02, 1.32, 14)]
            pen.line(f.pts(bow), BALA_RIB, 1.3)
    _knit(img, p, [outer], slot, ribs, mouth)


def balaclava_turned(img, p, f, L, sp, view):
    import turnhead as TH
    H = TH.H
    kh = sp['kit_house']
    sil = TH.silhouette(f)
    outer = [[(x, y) for x, y, _, _ in sil]]
    top_v = f.v0
    # the crown rounded and the neck carried down into the collar (the torso's neck is the knit's colour: neck_c)
    n0, n1 = TH.NECK.get(view, (-32, 32))
    yb = f.top + f.v1 * H
    outer.append([(f.hx + n0 - 6, yb - 0.25 * H), (f.hx + n1 + 6, yb - 0.25 * H), (f.hx + n1 + 6, yb + 0.06 * H),
                  (f.hx + n0 - 6, yb + 0.06 * H)])   # to the collar's top: the collar shows round it (Sam, 27 Nov)
    if view in ('three', 'side'):                                       # the knit over the nose: a bump, not a cut
        ny, ey, tip = L['nose_y'], L['eye_y'], f.prof.get('nose_tip', 0.2)
        outer.append([f.at(0.0, ey + 0.03, 0.0), f.at(0.0, (ey + ny) / 2, tip * 0.6), f.at(0.0, ny - 0.04, tip * 0.95),
                      f.at(0.0, ny + 0.005, tip * 0.6), f.at(-0.06, ny + 0.02, 0.0), f.at(-0.06, ey + 0.04, 0.0)])
        lv = _talk_level(sp)
        outer.append([f.at(0.0, L['lip0'] - 0.02, 0.03), f.at(0.0, L['lip17'] + 0.03 * lv, 0.03),
                      f.at(-0.1, L['lip17'], 0.0), f.at(-0.1, L['lip0'], 0.0)])   # the lips' bump under the knit
    slot = None
    mouth = None
    if view in ('three', 'side'):
        slot = curve(f.pts(_slot_uv(L, kh)), 3)
        lv = _talk_level(sp)
        if lv > 0.05:
            mouth = curve(f.pts(_mouth_uv(L, lv)), 3)
    ps = np.arange(-180, 180, 8.0)

    def ribs(pen):
        vs = np.linspace(top_v, f.v1 - 0.1, 30)          # not the bottom rings: the meridians crowd there
        for psi in ps:
            seg = []
            for v in vs:
                x, z = f.ring(np.array([psi]), v)
                X, Z = f.view(x, z)
                if float(Z[0]) > 0.02:
                    seg.append((f.cx + float(X[0]) * H, f.top + v * H))
                elif len(seg) > 1:
                    pen.line(seg, BALA_RIB, 1.3)
                    seg = []
                else:
                    seg = []
            if len(seg) > 1:
                pen.line(seg, BALA_RIB, 1.3)
        for x in np.arange(f.hx + n0 - 4, f.hx + n1 + 6, 0.045 * H):    # the neck's ribs, straight down
            pen.line([(x, yb - 0.2 * H), (x, yb + 0.06 * H)], BALA_RIB, 1.3)
    base = p.pen if hasattr(p, 'pen') else p
    _knit(img, p, outer, slot, ribs, mouth, dilate=max(2, int(round(base.cam.S(0.022 * H)))),
          soften=max(2, int(round(base.cam.S(0.08 * H)))) if view in ('three_back', 'back') else 0)


# ---------------------------------------------------------------------------------------------- disguise (Patriots 5)
NIQAB, NIQAB_FOLD, NIQAB_EDGE = (14, 14, 17), (40, 40, 48), (26, 26, 30)
KUFI, KUFI_KNIT = (238, 236, 228), (196, 194, 186)


def _veil_uv(L, W, top):
    """The niqab's outline in face units: over the crown a little above the knit, down past the ears, flaring onto
    the shoulders and chest, its lower edge a soft curve below the chin."""
    right = [(W * math.cos(a), 0.12 - (0.12 - top) * math.sin(a)) for a in np.linspace(math.pi / 2, 0, 12)]
    right += [(W + 0.03, 0.3), (W + 0.07, 0.6), (W + 0.16, 0.95), (W + 0.26, 1.28), (W + 0.2, 1.42), (0.5 * W, 1.5)]
    return [(0.0, top)] + right + [(-u, v) for u, v in right[::-1]]


def niqab_front(img, p, f, L, kh, sp):
    W = max(_face_u(L, 0.0) + 0.14, L['fw'] * 0.5 + 0.12)
    top = kh.get('bala_top', -0.5) - 0.05
    outer = curve(f.pts(_veil_uv(L, W, top)), 4)
    slot = curve(f.pts(_slot_uv(L, dict(kh, slot=dict(above=0.07, below=0.07, side=0.06)))), 3)

    def folds(pen):
        for u in (-0.55, -0.3, 0.3, 0.55):                 # soft folds down from the chin
            pen.line(f.pts([(u * W, 0.75), (u * W * 1.12, 1.1), (u * W * 1.25, 1.4)]), NIQAB_FOLD, 1.6)
        bv = L['brow_y'] - 0.1                              # the tie band over the brow
        pen.line(f.pts([(-W + 0.02, bv + 0.02), (0.0, bv - 0.01), (W - 0.02, bv + 0.02)]), NIQAB_FOLD, 2.2)
    _knit(img, p, [outer], slot, folds, fill=NIQAB, edge=NIQAB_EDGE)


def niqab_turned(img, p, f, L, sp, view):
    import turnhead as TH
    H = TH.H
    kh = sp['kit_house']
    sil = [(x, y) for x, y, _, _ in TH.silhouette(f)]
    xs = [x for x, _ in sil]
    yb = f.top + f.v1 * H
    l, r = min(xs), max(xs)
    drape = [(l - 0.04 * H, f.top + 0.45 * H), (r + 0.04 * H, f.top + 0.45 * H), (r + 0.22 * H, yb + 0.32 * H),
             (0.5 * (l + r), yb + 0.42 * H), (l - 0.22 * H, yb + 0.32 * H)]
    slot = None
    if view in ('three', 'side'):
        slot = curve(f.pts(_slot_uv(L, dict(kh, slot=dict(above=0.07, below=0.07, side=0.06)))), 3)

    def folds(pen):
        for k in (0.25, 0.5, 0.75):
            x = l + (r - l) * k
            pen.line([(x, yb - 0.05 * H), (x + (k - 0.5) * 0.3 * H, yb + 0.3 * H)], NIQAB_FOLD, 1.6)
    base = p.pen if hasattr(p, 'pen') else p
    _knit(img, p, [sil, drape], slot, folds, dilate=max(3, int(round(base.cam.S(0.05 * H)))),
          soften=max(2, int(round(base.cam.S(0.08 * H)))), fill=NIQAB, edge=NIQAB_EDGE)


def kufi_front(img, p, f, L, kh, sp):
    """The cap follows the knit's own crown (the balaclava's top curve), a touch bigger, down to a third of the way
    to the brows: it sits ON the head, never a lid above it."""
    W = max(_face_u(L, 0.0) + 0.1, L['fw'] * 0.5 + 0.08) + 0.018
    top = kh.get('bala_top', -0.5) - 0.022
    vc = 0.12
    foot = top + 0.26
    hw = lambda v: W * math.sqrt(max(0.0, 1 - ((vc - v) / (vc - top)) ** 2))   # noqa: E731
    vs = np.linspace(foot, top, 10)
    pts = [(hw(v), v) for v in vs] + [(-hw(v), v) for v in vs[::-1]]
    pts += [(-hw(foot) - 0.004, foot + 0.03), (hw(foot) + 0.004, foot + 0.03)]
    p.poly(curve(f.pts(pts), 3), KUFI, INK, 2.4)
    p.line(curve(f.pts([(-hw(foot), foot), (0.0, foot + 0.008), (hw(foot), foot)]), 3), KUFI_KNIT, 2.0)   # the band
    for v in np.arange(top + 0.045, foot - 0.01, 0.04):     # the knit's rows of small holes
        for u in np.arange(-hw(v) + 0.035, hw(v) - 0.03, 0.05):
            p.ell(*f(u, v), 1.8, 1.8, KUFI_KNIT, None)


def kufi_turned(img, p, f, L, sp, view):
    """The head's turned outline above the cap's foot, pushed out a little from the head's middle: it hugs the
    crown from every side."""
    import turnhead as TH
    H = TH.H
    sil = [(x, y) for x, y, _, _ in TH.silhouette(f)]
    top = min(y for _, y in sil)
    cut = top + 0.27 * H
    cx = sum(x for x, _ in sil) / len(sil)
    cy = top + 0.45 * H
    cap = [(x, y) for x, y in sil if y <= cut]
    if len(cap) < 3:
        return
    grow = 0.022 * H
    cap = [(x + grow * (x - cx) / (math.hypot(x - cx, y - cy) or 1), y + grow * (y - cy) / (math.hypot(x - cx, y - cy) or 1))
           for x, y in cap]
    cap = sorted(cap, key=lambda q: math.atan2(q[1] - cy, q[0] - cx))
    xs = [x for x, _ in cap]
    l, r = min(xs), max(xs)
    poly = cap + [(r, cut + 0.03 * H), (l, cut + 0.03 * H)]
    poly = sorted(poly, key=lambda q: math.atan2(q[1] - cy, q[0] - cx))
    p.poly(poly, KUFI, INK, 2.4)
    for y in np.arange(top + 0.04 * H, cut, 0.04 * H):
        row = [x for x, yy in cap if abs(yy - y) < 0.03 * H]
        if not row:
            continue
        for x in np.arange(min(row) + 0.035 * H, max(row) - 0.03 * H, 0.05 * H):
            p.ell(x, y, 1.8, 1.8, KUFI_KNIT, None)
