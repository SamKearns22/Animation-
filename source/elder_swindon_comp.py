#!/usr/bin/env python3
"""elder_swindon_comp: the rough composition sheet for Elder Scrolls: Swindon (rule 11): the 4 key shots.

MAP
- 25: the world in metres (the man, scroll, can, packet, litter, dog) and the top-down camera
- 50: props: lying cylinders of revolution (can, scroll), packet, drool
- 190: dog: a Staffordshire bull terrier from above, house style, jaws on the trouser hem
- 240: aerial: the Magic Roundabout from above, flat house style, rough traffic
- 330: title: gold rings, "The Elder Scrolls VI", "SWINDON"
- 370: panels and the sheet

    python3 source/elder_swindon_comp.py comp OUT.jpg
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B                    # noqa: E402
import elder_swindon_ground as G       # noqa: E402
import hook_text as HT                 # noqa: E402
import lying as L                      # noqa: E402
import sets as S                       # noqa: E402
from ed import INK                     # noqa: E402

SS = B.SS
HOOK = 'Elder Scrolls reveals new location!'
MAN = dict(name='DROOLER', skin=(232, 190, 160), hw=72, hh=94, jaw='round', hair='crop', hair_c=(90, 66, 44),
           brow_c=(80, 60, 44), brow_w=4.0, outfit='tracksuit', jacket=(150, 152, 158), trousers=(150, 152, 158),
           belt=(140, 142, 148), shoe=(236, 236, 232), shoulders=150, mouth='line', seed=5, blink=True)
MAN['mouth'] = 'open'                                    # slack-jawed, drooling
SCROLL = ((-0.86, -0.52), (-0.86, -1.16))               # the scroll's two tips (x, z): in front of his flung hand
CAN = ((-0.60, -0.84), (-0.62, -0.99))                  # base and top of the lager can, lying by his hand
PACKET = (-0.70, -0.30, 25.0)                            # the sandwich packet: centre (x, z), turn
LITTER = [('butt', -0.48, -1.12, 30), ('butt', -0.72, -0.70, 120), ('butt', -0.95, -1.00, -20),
          ('butt', -0.30, -0.35, 75), ('ringpull', -0.70, -1.10, 0)]


def topcam(x, z, d, width):
    """Straight down (0.4 degrees off, as lying.py's test cameras) from d metres, `width` metres across the frame."""
    return S.Cam((x, d, z + d * math.cos(math.radians(89.6))), (x, 0.0, z), focal=1080 * d / width)


def angcam(at, d, el, width):
    """From the side his face points (-x), looking down `el` degrees at floor point at=(x, z): screen right is -z
    (towards his flung hand), screen up is +x (away over his head)."""
    e = math.radians(el)
    x, z = at
    return S.Cam((x - d * math.cos(e), d * math.sin(e), z), (x, 0.0, z), focal=1080 * d / width)


def orbit(at, az, el, d, width):
    """Looking down `el` degrees at floor point at=(x, z) from bearing `az` (degrees from +x towards +z)."""
    a, e = math.radians(az), math.radians(el)
    x, z = at
    return S.Cam((x + d * math.cos(e) * math.cos(a), d * math.sin(e), z + d * math.cos(e) * math.sin(a)),
                 (x, 0.0, z), focal=1080 * d / width)


def man():
    return L.lie(MAN, 'face_down', 0.0, 0.0, 90.0)


# ------------------------------------------------------------------------------------------------ props
def _prof_scroll(t):
    """The Elder Scroll's radius (metres) and material along its length t 0..1 (reference: Sam's elder-scroll.jpg:
    spiked tips, dark wrapped grips, carved end caps, the plain case in the middle)."""
    u = min(t, 1 - t)                                    # mirrored about the middle
    if u < 0.025:
        return 0.004 + 0.3 * u, 'gold'                   # the spike
    if u < 0.05:
        return 0.016 * math.sin((u - 0.025) / 0.025 * math.pi) + 0.006, 'gold'   # the finial bead
    if u < 0.13:
        return 0.010, 'grip'                             # the dark wrapped grip
    if u < 0.15:
        return 0.016, 'gold'                             # a collar
    if u < 0.27:
        return 0.030 - 0.006 * ((u - 0.15) / 0.12 - 0.5) ** 2 * 4, 'carved'   # the carved end cap
    if u < 0.29:
        return 0.027, 'gold'                             # the cap's lip
    return 0.021, 'case'


def lying_rev(img, cam, a, b, prof, mat, H=None, bury=0.0, seed=0):
    """A lying solid of revolution on the floor from a to b (x, z), radius prof(t) -> (r, kind); coloured by
    mat(kind, t, nrm) and shaded near-real (sun from screen left). `bury`: how much of it the soil covers (0..1),
    drawn as soil clumps over it. img: float RGB (SS canvas)."""
    h, w, _ = img.shape
    (ax, ay), k = cam.project((a[0], 0.02, a[1]))
    (bx, by), _ = cam.project((b[0], 0.02, b[1]))
    ax, ay, bx, by, k = ax * SS, ay * SS, bx * SS, by * SS, k * SS
    Lp = math.hypot(bx - ax, by - ay)
    dx, dy = (bx - ax) / Lp, (by - ay) / Lp
    rmax = max(prof(t)[0] for t in np.linspace(0, 1, 200)) * k
    x0, x1 = int(max(0, min(ax, bx) - rmax - 2)), int(min(w, max(ax, bx) + rmax + 2))
    y0, y1 = int(max(0, min(ay, by) - rmax - 2)), int(min(h, max(ay, by) + rmax + 2))
    if x1 <= x0 or y1 <= y0:                             # wholly out of shot
        return img
    ys, xs = np.mgrid[y0:y1, x0:x1]
    px, py = xs + 0.5 - ax, ys + 0.5 - ay
    t = (px * dx + py * dy) / Lp
    s = (-px * dy + py * dx)
    tt = np.clip(t, 0, 1)
    tab = np.array([prof(v)[0] for v in np.linspace(0, 1, 512)]) * k
    kinds = [prof(v)[1] for v in np.linspace(0, 1, 512)]
    idx = np.clip((tt * 511).astype(int), 0, 511)
    r = tab[idx]
    inside = (t >= 0) & (t <= 1) & (np.abs(s) < r)
    # soft shadow first, cast away from the sun (to screen right and down)
    sh = np.zeros((y1 - y0, x1 - x0))
    off = 0.6
    s2 = (-(px - r * off) * dy + (py - r * off * 0.6) * dx)
    t2 = ((px - r * off) * dx + (py - r * off * 0.6) * dy) / Lp
    sh[(t2 >= 0) & (t2 <= 1) & (np.abs(s2) < r * 1.05)] = 1
    sh = np.asarray(Image.fromarray((sh * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3 * SS)), float) / 255
    reg = img[y0:y1, x0:x1]
    soil0 = reg.copy()
    reg *= (1 - 0.55 * sh)[..., None]
    nrm = np.where(inside, s / np.maximum(r, 1e-6), 0)
    out = reg.copy()
    for kind in set(kinds):
        sel = inside & (np.array(kinds)[idx] == kind)
        if not sel.any():
            continue
        base, metal, spec = mat(kind, tt[sel], nrm[sel])
        out[sel] = G.shade_cyl(nrm[sel], (0.5, 0.5, 0.5), spec, metal) * 0 + _shade(base, nrm[sel], metal, spec)
    if bury > 0:                                         # soil drifted over one end and along its lower side
        nz = G.noise(xs / k * 3.0, ys / k * 3.0, 0.02, seed + 40)
        cover = inside & ((tt + 0.12 * nz) < bury) | inside & (nrm > 0.55 + 0.25 * nz)
        out[cover] = soil0[cover]
    reg[:] = out
    return img


def _shade(base, nrm, metal, spec):
    base = np.asarray(base, float)
    if base.ndim == 1:
        base = np.tile(base, (len(nrm), 1))
    c = np.sqrt(np.clip(1 - nrm ** 2, 0, 1))
    lam = np.clip(0.55 * c - 0.48 * nrm + 0.25, 0, 1)
    out = base * (0.30 + 0.95 * lam)[:, None]
    if metal:
        band = np.exp(-((nrm + 0.38) / 0.10) ** 2) * spec + np.exp(-((nrm - 0.55) / 0.07) ** 2) * spec * 0.3
        out = out * (0.5 + 0.5 * c)[:, None] + np.array([1.0, 0.93, 0.72])[None, :] * band[:, None]
    else:
        out = out + np.exp(-((nrm + 0.42) / 0.09) ** 2)[:, None] * spec
    return np.clip(out, 0, 1)


GOLD = (0.78, 0.60, 0.26)


def scroll_mat(kind, t, nrm):
    n = len(t)
    if kind == 'grip':                                   # dark leather wrapped in a spiral
        band = (np.sin((t * 120 + nrm * 3) * math.pi) > 0.2)
        c = np.where(band[:, None], np.array([0.20, 0.12, 0.08]), np.array([0.32, 0.20, 0.12]))
        return c, False, 0.15
    if kind == 'carved':                                 # carved gold: a lattice of grooves
        g = (np.abs(np.sin(t * 160 + nrm * 6)) < 0.25) | (np.abs(np.sin(t * 160 - nrm * 6)) < 0.25)
        c = np.where(g[:, None], np.array(GOLD) * 0.45, np.array(GOLD))
        return c, True, 0.9
    if kind == 'case':                                   # the case: a seam along it (the slot of the reference)
        c = np.tile(np.array(GOLD) * 0.92, (n, 1))
        c[np.abs(nrm + 0.1) < 0.05] *= 0.4
        return c, True, 1.0
    return np.tile(np.array(GOLD), (n, 1)), True, 1.0


def _prof_can(t):
    if t < 0.03 or t > 0.97:
        return 0.029, 'rim'
    return 0.033, 'body'


def _can_label():
    """The label laid round the can: silver, a red band, EXPORT LAGER in white (Sam, Q5: plain EXPORT LAGER)."""
    w, h = 600, 300                                       # along the can x round the can
    im = Image.new('RGB', (w, h), (196, 200, 206))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 90, w, 210], fill=(176, 28, 34))
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 64)
    d.text((w / 2, 150), 'EXPORT LAGER', font=f, fill=(250, 250, 248), anchor='mm')
    d.text((w / 2, 245), '4.0% vol  440ml', font=ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 26),
           fill=(60, 60, 70), anchor='mm')
    return np.asarray(im, float) / 255


_LABEL = None


def can_mat(kind, t, nrm):
    global _LABEL
    if _LABEL is None:
        _LABEL = _can_label()
    if kind == 'rim':
        return np.tile(np.array([0.70, 0.72, 0.75]), (len(t), 1)), True, 0.8
    h, w, _ = _LABEL.shape
    u = np.clip(((t - 0.03) / 0.94) * (w - 1), 0, w - 1).astype(int)
    v = np.clip((np.arcsin(np.clip(nrm, -1, 1)) / math.pi + 0.5) * (h - 1), 0, h - 1).astype(int)
    dent = 0.25 * np.exp(-(((t - 0.6) / 0.08) ** 2 + ((nrm + 0.2) / 0.3) ** 2))   # a dent catches the light
    return _LABEL[v, u] * (1 - dent[:, None]), True, 0.7


def packet(pil, cam, x, z, ang, scale=1.0):
    """A supermarket sandwich wedge from above: card sleeve, film window onto the egg mayo, EGG MAYO label."""
    (cx, cy), k = cam.project((x, 0.03, z))
    cx, cy, k = cx * SS, cy * SS, k * SS * scale
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))

    def P(u, v):
        return (cx + (u * ca - v * sa) * k, cy + (u * sa + v * ca) * k)
    d = ImageDraw.Draw(pil)
    tri = [P(-0.065, 0.065), P(0.065, 0.065), P(-0.065, -0.065)]
    d.polygon([(px + 6, py + 5) for px, py in tri], fill=(40, 30, 22))
    d.polygon(tri, fill=(232, 234, 228))
    d.polygon([P(-0.05, 0.05), P(0.025, 0.05), P(-0.05, -0.025)], fill=(236, 214, 150))    # egg mayo through the film
    d.line([P(-0.05, 0.05), P(0.025, 0.05), P(-0.05, -0.025), P(-0.05, 0.05)], fill=(250, 250, 250), width=3)
    d.polygon([P(-0.065, 0.065), P(0.065, 0.065), P(0.05, 0.05), P(-0.05, 0.05)], fill=(52, 120, 70))
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), max(10, int(0.012 * k)))
    lab = Image.new('RGBA', (int(0.09 * k), int(0.02 * k)), (0, 0, 0, 0))
    ImageDraw.Draw(lab).text((lab.width / 2, lab.height / 2), 'EGG MAYO', font=f, fill=(255, 255, 255), anchor='mm')
    lab = lab.rotate(-ang, expand=True)
    p = P(0.0, 0.058)
    pil.alpha_composite(lab, (int(p[0] - lab.width / 2), int(p[1] - lab.height / 2)))


def drool(pil, cam, k):
    """A wet string from the corner of his mouth to a dark damp patch on the soil (near-real: a highlight)."""
    head = np.asarray(k['head'])
    fwd, up = np.asarray(k['hfwd']), np.asarray(k['hup'])
    mouth = head + fwd * 0.085 - up * 0.045
    pool = mouth + fwd * 0.02 + np.array([0, -mouth[1], 0])
    (mx, my), kk = cam.project(tuple(mouth))
    (qx, qy), _ = cam.project(tuple(pool))
    mx, my, qx, qy, kk = mx * SS, my * SS, qx * SS, qy * SS, kk * SS
    d = ImageDraw.Draw(pil)
    R = 0.035 * kk
    d.ellipse([qx - R, qy - R * 0.7, qx + R, qy + R * 0.7], fill=(70, 52, 40, 200))
    d.line([(mx, my), ((mx + qx) / 2 + 0.006 * kk, (my + qy) / 2), (qx, qy)], fill=(214, 226, 230, 220),
           width=max(2, int(0.006 * kk)))
    d.ellipse([qx - R * 0.3, qy - R * 0.25, qx, qy], fill=(230, 236, 240, 200))


# ------------------------------------------------------------------------------------------------ dog
STAFFIE = dict(coat=(122, 84, 56), dark=(88, 58, 38), chest=(236, 230, 220), nose=(30, 26, 26))


def dog(pil, cam, head_at, heading, pull=0.0, run=None):
    """A Staffordshire bull terrier from above, house style (flat colour, one outline): broad head with the jaws
    clamped on the trouser hem at `head_at` (x, z), body braced away along `heading` degrees, legs splayed."""
    hx, hz = head_at
    a = math.radians(heading)
    fx, fz = math.cos(a), math.sin(a)                    # from the head towards the tail
    sx, sz = -fz, fx

    def W(u, v):                                         # u back from the head, v to the dog's side (metres)
        return (hx + fx * u + sx * v, 0.25, hz + fz * u + sz * v)

    def poly(pts, fill, lw=2.6):
        P = [tuple(c * SS for c in cam.project(W(*p))[0]) for p in pts]
        ImageDraw.Draw(pil).polygon(P, fill=fill)
        ImageDraw.Draw(pil).line(P + [P[0]], fill=INK, width=int(lw * SS), joint='curve')

    def ell(u, v, ru, rv, fill, n=24):
        pts = [(u + ru * math.cos(t), v + rv * math.sin(t)) for t in np.linspace(0, 2 * math.pi, n, endpoint=False)]
        poly(pts, fill)
    d = ImageDraw.Draw(pil)
    SS = B.SS
    # shadow
    sh = [tuple(c * SS for c in cam.project((W(u, v)[0] + 0.04, 0.0, W(u, v)[2] + 0.03))[0])
          for u, v in [(0.0, -0.12), (0.5, -0.15), (0.6, 0.0), (0.5, 0.15), (0.0, 0.12)]]
    d.polygon(sh, fill=(30, 22, 16, 110))
    for u, v, du, dv in ((0.12, -0.09, -0.05, -0.07), (0.12, 0.09, -0.05, 0.07), (0.44, -0.09, 0.07, -0.06),
                         (0.44, 0.09, 0.07, 0.06)):  # short legs braced out, paws dug in
        if run is not None:                              # running: legs reach and push in a gallop
            sw = 0.11 * math.sin(run + (0 if u < 0.3 else math.pi) + (0.5 if v > 0 else 0))
            du, dv = sw - 0.02, dv * 0.5
        poly([(u - 0.035, v), (u + du - 0.03, v + dv), (u + du + 0.03, v + dv), (u + 0.035, v)], STAFFIE['dark'])
    poly([(0.50, -0.02), (0.64 + pull * 0.02, -0.006), (0.64 + pull * 0.02, 0.006), (0.50, 0.02)], STAFFIE['coat'])  # tapered tail
    # one silhouette: broad shoulders, narrow waist, rump; the head as wide as the shoulders (the Staffie's)
    body = [(0.06, -0.13), (0.16, -0.155), (0.28, -0.12), (0.40, -0.10), (0.50, -0.11), (0.55, -0.06), (0.56, 0.0),
            (0.55, 0.06), (0.50, 0.11), (0.40, 0.10), (0.28, 0.12), (0.16, 0.155), (0.06, 0.13)]
    poly(body, STAFFIE['coat'])
    for u in (0.24, 0.31, 0.38, 0.45):                   # brindle stripes across the back
        (a0, b0), _ = cam.project(W(u, -0.08))
        (a1, b1), _ = cam.project(W(u + 0.02, 0.08))
        d.line([(a0 * SS, b0 * SS), (a1 * SS, b1 * SS)], fill=STAFFIE['dark'], width=int(4 * SS))
    head = [(-0.05, -0.07), (-0.02, -0.13), (0.06, -0.15), (0.12, -0.12), (0.13, 0.0), (0.12, 0.12), (0.06, 0.15),
            (-0.02, 0.13), (-0.05, 0.07)]
    poly(head, STAFFIE['coat'])                          # the wide head with its cheek muscles
    poly([(-0.10, -0.055), (-0.04, -0.075), (-0.04, 0.075), (-0.10, 0.055)], STAFFIE['dark'])   # short muzzle
    poly([(-0.02, -0.018), (0.10, -0.012), (0.10, 0.012), (-0.02, 0.018)], STAFFIE['chest'])     # white blaze
    for v in (-1, 1):                                    # rose ears folded back
        poly([(0.07, v * 0.11), (0.13, v * 0.17), (0.14, v * 0.10)], STAFFIE['dark'])
    ell(-0.105, 0.0, 0.014, 0.022, STAFFIE['nose'])
    for v in (-0.05, 0.05):                              # eyes narrowed, brows down: angry
        (ex, ey), kk = cam.project(W(0.02, v))
        ex, ey, kk = ex * SS, ey * SS, kk * SS
        r = 0.012 * kk
        d.ellipse([ex - r, ey - r * 0.5, ex + r, ey + r * 0.5], fill=(20, 16, 14))
        (bx, by), _ = cam.project(W(-0.005, v * 0.6))
        (cx, cy), _ = cam.project(W(0.0, v * 1.4))
        d.line([(bx * SS, by * SS), (cx * SS, cy * SS)], fill=INK, width=int(3 * SS))


# ------------------------------------------------------------------------------------------------ aerial
MINIS = [211, 282, 339, 45, 148]                        # the five mini roundabouts' bearings (screen degrees)
GREY = (150, 150, 152)


def aerial(t=0.0, scale=6.4):
    """The Magic Roundabout from straight above, flat house style (rough, for the composition sheet)."""
    w, h = B.W * SS, B.H * SS
    s = scale * SS
    cx, cy = w / 2, h * 0.30
    im = Image.new('RGBA', (w, h), (118, 160, 84, 255))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(4)

    def P(r, ang):
        return (cx + r * s * math.cos(math.radians(ang)), cy + r * s * math.sin(math.radians(ang)))

    def disc(x, y, r, fill, outline=None, lw=2.6):
        d.ellipse([x - r * s, y - r * s, x + r * s, y + r * s], fill=fill,
                  outline=outline, width=int(lw * SS) if outline else 0)
    # the estate round it: houses with brown roofs, a flat-roofed block, trees
    for i in range(70):
        ang = rng.uniform(0, 360)
        r = rng.uniform(75, 160)
        if min(abs((ang - m + 180) % 360 - 180) for m in MINIS) < 9:
            continue
        x, y = P(r, ang)
        ww, hh = rng.uniform(9, 14) * s, rng.uniform(6, 8) * s
        roof = tuple(int(v) for v in rng.choice([(150, 96, 70), (128, 84, 64), (110, 92, 84)]))
        d.rectangle([x - ww / 2, y - hh / 2, x + ww / 2, y + hh / 2], fill=roof, outline=INK, width=int(2 * SS))
        d.line([x - ww / 2, y, x + ww / 2, y], fill=B.dk(roof, 0.75) if hasattr(B, 'dk') else INK, width=int(2 * SS))
    d.rectangle([w * 0.72, h * 0.12, w * 1.0, h * 0.2], fill=(186, 182, 176), outline=INK, width=int(2.6 * SS))
    for i in range(40):
        x, y = P(rng.uniform(58, 150), rng.uniform(0, 360))
        r = rng.uniform(3, 6)
        disc(x, y, r, (70, 112, 58), INK, 2)
    # tarmac: arms first, then the big shared area
    for m in MINIS:
        a0, b0 = P(42, m), P(220, m)
        d.line([a0, b0], fill=(205, 205, 200), width=int(21 * s))       # pavements
        d.line([a0, b0], fill=GREY, width=int(15 * s))
    disc(cx, cy, 58, (205, 205, 200))
    disc(cx, cy, 55, GREY)
    # raised kerbed islands between the minis
    for i in range(5):
        a1, a2 = MINIS[i], MINIS[(i + 1) % 5]
        mid = (a1 + ((a2 - a1) % 360) / 2) % 360
        x, y = P(36, mid)
        pts = [P(36 + dv, mid + du) for du, dv in ((-9, -3), (9, -3), (9, 3), (-9, 3))]
        d.polygon(pts, fill=(96, 92, 90), outline=(244, 244, 240))
    # the inner ring and the central island: dark paving, white kerb, a soil-and-grass patch, the lamp post
    disc(cx, cy, 15, (82, 80, 80), (244, 244, 240), 3)
    d.ellipse([cx - 6 * s, cy - 1 * s, cx + 1 * s, cy + 5 * s], fill=(118, 90, 64))       # the soil patch (Q2)
    d.ellipse([cx - 5 * s, cy + 0 * s, cx - 1 * s, cy + 3 * s], fill=(120, 140, 70))
    disc(cx + 0.0, cy, 0.8, (60, 60, 64), INK, 2)
    d.line([(cx, cy), (cx + 30 * s, cy - 30 * s)], fill=(60, 60, 64, 160), width=int(1.2 * s))   # its long shadow
    for r in (23,):
        for a in range(0, 360, 12):
            d.arc([cx - r * s, cy - r * s, cx + r * s, cy + r * s], a, a + 5, fill=(244, 244, 240), width=int(0.5 * s))
    for m in MINIS:                                      # mini roundabouts: white dome and dashed ring
        x, y = P(42, m)
        disc(x, y, 2.2, (244, 244, 240), INK, 1.5)
        for a in range(0, 360, 30):
            d.arc([x - 6 * s, y - 6 * s, x + 6 * s, y + 6 * s], a, a + 15, fill=(244, 244, 240), width=int(0.4 * s))
        for side in (-1, 1):                             # give-way dashes on the arm
            for j in range(6):
                q = P(55 + j * 2.0, m + side * 3)
                d.rectangle([q[0] - 0.5 * s, q[1] - 0.5 * s, q[0] + 0.5 * s, q[1] + 0.5 * s], fill=(244, 244, 240))
    # traffic (rough): cars on the inner ring, round each mini and on the arms; a bus
    cols = [(240, 240, 238), (30, 30, 34), (170, 172, 178), (176, 30, 36), (40, 70, 150), (240, 240, 238)]

    def car(x, y, ang, Lm=4.4, Wm=1.85, col=(240, 240, 238)):
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        pts = [(x + (u * ca - v * sa) * s, y + (u * sa + v * ca) * s)
               for u, v in ((-Lm / 2, -Wm / 2), (Lm / 2, -Wm / 2), (Lm / 2, Wm / 2), (-Lm / 2, Wm / 2))]
        d.polygon(pts, fill=col, outline=INK)
        wpts = [(x + (u * ca - v * sa) * s, y + (u * sa + v * ca) * s)
                for u, v in ((Lm * 0.12, -Wm * 0.4), (Lm * 0.3, -Wm * 0.4), (Lm * 0.3, Wm * 0.4), (Lm * 0.12, Wm * 0.4))]
        d.polygon(wpts, fill=(40, 46, 56))
    for i in range(9):                                   # anticlockwise round the inner ring
        a = i * 40 + t * -25 + rng.uniform(-8, 8)
        x, y = P(19, a)
        car(x, y, a - 90, col=cols[i % 6])
    for m in MINIS:                                      # clockwise round each mini, queues on the arms
        mx, my = P(42, m)
        for j in range(2):
            a = rng.uniform(0, 360) + t * 40
            car(mx + 9 * s * math.cos(math.radians(a)), my + 9 * s * math.sin(math.radians(a)), a + 90,
                col=cols[rng.integers(0, 6)])
        for j in range(3):
            x, y = P(64 + j * 7, m - 2.5)
            car(x, y, m + 180, col=cols[rng.integers(0, 6)])
            x, y = P(70 + j * 9, m + 2.5)
            car(x, y, m, col=cols[rng.integers(0, 6)])
    x, y = P(47, 100)
    car(x, y, 10, 12.0, 2.55, (232, 196, 40))            # a bus
    return im


# ------------------------------------------------------------------------------------------------ title
def title(pil, small=1.0, big=1.0, rings=1.0, dim=0.55):
    """The teaser's end card over the picture: the picture dims (the teaser goes to black; ours half way), gold
    rings, "The Elder Scrolls VI" small with a rule under it, "SWINDON" big, gold with the house outline."""
    w, h = pil.size
    k = w / 1080
    if dim:
        pil.alpha_composite(Image.new('RGBA', pil.size, (8, 6, 4, int(255 * dim))))
    d = ImageDraw.Draw(pil)
    cy = 1160 * k
    gold = (214, 170, 104)
    for (ox, oy, r) in ((-150, -60, 300), (170, -40, 280), (0, 160, 330), (-60, -260, 230), (120, 260, 260)):
        a = int(255 * 0.8 * rings)
        d.ellipse([w / 2 + (ox - r) * k, cy + (oy - r) * k, w / 2 + (ox + r) * k, cy + (oy + r) * k],
                  outline=gold + (a,), width=int(3 * k))
    fs = ImageFont.truetype(os.path.join(HERE, 'fonts', 'Cinzel-Variable.ttf'), int(52 * k))
    fb = ImageFont.truetype(os.path.join(HERE, 'fonts', 'Cinzel-Variable.ttf'), int(178 * k))
    try:
        fb.set_variation_by_name('Bold')
    except Exception:
        pass
    a = int(255 * small)
    d.text((w / 2, cy - 120 * k), 'The Elder Scrolls VI', font=fs, fill=gold + (a,), anchor='mm',
           stroke_width=int(3 * k), stroke_fill=INK + (a,) if len(INK) == 3 else INK)
    d.line([w / 2 - 240 * k, cy - 78 * k, w / 2 + 240 * k, cy - 78 * k], fill=gold + (a,), width=int(3 * k))
    a = int(255 * big)
    d.text((w / 2, cy + 40 * k), 'SWINDON', font=fb, fill=(226, 184, 118, a), anchor='mm',
           stroke_width=int(5 * k), stroke_fill=INK + (a,) if len(INK) == 3 else INK)


# ------------------------------------------------------------------------------------------------ panels
def near_real(cam, t, with_dog=False, scroll_bury=1.0, show_packet=True, k=None):
    img, H = G.soil(cam, ss=SS, grass=0.45)
    img = G.litter(img, cam, SS, LITTER)
    img = lying_rev(img, cam, CAN[0], CAN[1], _prof_can, can_mat, bury=0.35, seed=2)
    if scroll_bury < 1:                                  # fully buried: not there yet
        img = lying_rev(img, cam, SCROLL[0], SCROLL[1], _prof_scroll, scroll_mat, bury=scroll_bury, seed=3)
    pil = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).convert('RGBA')
    if show_packet:
        packet(pil, cam, *PACKET)
    k, surf = man()
    L.draw(pil, cam, k, MAN, t, surfaces=[(p0, n) for _, p0, n in surf])
    drool(pil, cam, k)
    if with_dog:
        an = k['anL']
        dog(pil, cam, (an[0] + 0.02, an[2] + 0.04), 50.0)
    out = np.asarray(pil.convert('RGB'), float) / 255
    out = G.dust(out, cam, SS, t, strength=0.8)
    # a moody vignette, warm
    hh, ww, _ = out.shape
    yy, xx = np.mgrid[0:hh, 0:ww]
    v = 1 - 0.55 * np.clip(((xx - ww / 2) / ww) ** 2 * 2.2 + ((yy - hh / 2) / hh) ** 2 * 2.2, 0, 1)
    out = out * v[..., None]
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).convert('RGBA')


def panel(n, tmp):
    if n == 0:                                           # 1.0 s: the can and his splayed hand from frame one
        im = near_real(orbit((-0.62, -0.98), 225, 70, 0.9, 0.62), 1.0, show_packet=False)
        im = im.resize((1080, 1920), Image.LANCZOS)
        path = os.path.join(tmp, 'hook.png')
        HT.card(1080, 1920, HOOK, 1240, path)
        im.alpha_composite(Image.open(path).convert('RGBA'))
        return im, '1.0 s  shot 1: can and hand, Hook Text'
    if n == 1:                                           # 11 s: the scroll uncovered beside his hand and face
        im = near_real(orbit((-0.42, -0.86), 225, 70, 1.2, 1.0), 11.0, scroll_bury=0.15, show_packet=False)
        return im.resize((1080, 1920), Image.LANCZOS), '11 s  shot 2: his face, the scroll uncovered'
    if n == 2:                                           # 16.2 s: the camera starts to climb; the Staffie on his leg
        im = near_real(topcam(0.0, -0.3, 3.0, 2.6), 16.2, with_dog=True, scroll_bury=0.0)
        return im.resize((1080, 1920), Image.LANCZOS), '16.2 s  shot 5: the climb, the Staffie'
    im = aerial(26.0)
    title(im)
    return im.resize((1080, 1920), Image.LANCZOS), '26 s  shot 6: the roundabout, SWINDON'


def comp(out):
    import tempfile
    tmp = tempfile.mkdtemp()
    tiles = []
    for n in range(4):
        im, lab = panel(n, tmp)
        tiles.append((im.convert('RGB').resize((540, 960), Image.LANCZOS), lab))
    sheet = Image.new('RGB', (1080, 1920 + 2 * 34), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 17)
    for i, (im, lab) in enumerate(tiles):
        x, y = (i % 2) * 540, (i // 2) * (960 + 34)
        d.text((x + 8, y + 8), lab, font=f, fill=(255, 230, 120))
        sheet.paste(im, (x, y + 34))
    sheet.save(out, quality=88)
    print('composition sheet:', out)


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'comp':
        comp(sys.argv[2])
    else:
        print(__doc__)
