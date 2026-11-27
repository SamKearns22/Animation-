#!/usr/bin/env python3
"""MAP  ink: the kit's line and shading helpers (one-route-kit Change 2, 20 Nov). Lifted out of An Honest Chat's
film file (ed.py, now frozen at its bookmark) so no kit file loads a finished film. Same code, same pictures.

Map: INK, HARD | smooth | soft (flat painted shadow) | bent_check (a check printed round a body) | curve (closed) |
open_curve (ends) | oval | Pen (a plain pen) | glaze (see-through fills that blend)
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

INK = (24, 20, 22)
HARD = True   # Job K (Sam, 10 Nov): shading as one hard-edged shape, never an airbrushed band (an "AI" tell); kept
#               inside the shape it shades by soft(clip=); a parody quoting the airbrush sets it False


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def soft(img, cam, pts, colr, alpha, blur=6, clip=None):
    """A painted shadow or highlight: one flat, hard-edged shape (ink.HARD); blurred only when ink.HARD is False, on a
    small layer round the shape (the same picture as blurring the whole frame, many times faster). clip: the outline
    of the shape it shades (same units as pts); the shading stays inside it (Job K build 2: a hard band past a
    torso's edge darkened a hand seen from behind)."""
    if HARD:
        blur = 0
    q = [cam.P(*p) for p in pts]
    r = float(cam.S(blur)) if blur else 0.0               # a plain number (a numpy one confuses PIL)
    pad = int(3 * r) + 3
    x0 = max(0, int(min(x for x, _ in q)) - pad)
    y0 = max(0, int(min(y for _, y in q)) - pad)
    x1 = min(img.width, int(max(x for x, _ in q)) + pad + 1)
    y1 = min(img.height, int(max(y for _, y in q)) + pad + 1)
    if x1 <= x0 or y1 <= y0:
        return
    lay = Image.new('RGBA', (x1 - x0, y1 - y0), (0, 0, 0, 0))
    ImageDraw.Draw(lay).polygon([(x - x0, y - y0) for x, y in q], fill=colr + (int(255 * alpha),))
    if blur:
        lay = lay.filter(ImageFilter.GaussianBlur(r))
    if clip is not None:
        m = Image.new('L', lay.size, 0)
        ImageDraw.Draw(m).polygon([(x - x0, y - y0) for x, y in (cam.P(*c) for c in clip)], fill=255)
        a = lay.getchannel('A')
        lay.putalpha(Image.composite(a, m, m))
    img.alpha_composite(lay, (x0, y0))


def bent_check(pen, poly, step, col, width, y0, y1, a=1.1, sag=8.0, split=None, pad=None):
    """A check (or stripes) printed on cloth round a body, not flat on the screen (Job K, proposal 4: a flat grid
    reads as a pasted texture). The upright bands are spaced evenly round a cylinder as wide as `poly`, so they bunch
    and thin towards its edges (x = cx + hw*sin(a*v)/sin(a)); the cross bands sag `sag` units in the middle. split:
    an x (a shirt's placket) right of which the upright bands sit half a step over, as two fronts buttoned. The
    bands run past the cloth; the caller keeps only what lies on the cloth."""
    xs = [q[0] for q in poly]
    cx, hw = (min(xs) + max(xs)) / 2, (max(xs) - min(xs)) / 2 or 1.0
    pad = step if pad is None else pad
    k = math.sin(a) / a                                  # v per unit at the middle
    dv = step / hw * k
    for half in ((None,) if split is None else ('L', 'R')):
        shift = 0.5 if half == 'R' else 0.0
        n = int(1 / dv) + 2
        for i in range(-n, n + 1):
            v = (i + shift) * dv
            if abs(v) > 1.0:
                continue
            x = cx + hw * math.sin(a * v) / math.sin(a)
            if half == 'L' and x > split + width or half == 'R' and x < split - width:
                continue
            w = max(1.0, width * math.cos(a * v))
            pen.line([(x, y0 - pad), (x, y1 + pad)], col, w)
    xx = np.linspace(cx - hw - pad, cx + hw + pad, 24)
    yy = sag * np.clip(1 - ((xx - cx) / hw) ** 2, 0, 1)
    for y in range(int(y0) // step * step - step, int(y1) + step, step):
        pen.line([(float(x), y + float(d)) for x, d in zip(xx, yy)], col, width)


def once(pts):
    """The points of a closed outline with no point twice in a row, the last not the first again (see curve)."""
    q = []
    for x, y in pts:
        if not q or abs(x - q[-1][0]) > 1e-6 or abs(y - q[-1][1]) > 1e-6:
            q.append((x, y))
    while len(q) > 3 and abs(q[0][0] - q[-1][0]) < 1e-6 and abs(q[0][1] - q[-1][1]) < 1e-6:
        q.pop()
    return q


def curve(pts, n=6):
    """Catmull-Rom through the points, CLOSED (the end joins back to the start): for shapes with an outline (a face,
    a belly, a puddle). For anything that simply ends (an arm, an antenna, a tail, a wire, a line) use open_curve:
    a tube or line drawn on this one doubles back from its end to its start (Poker Mon's wing, 19 Oct).
    Each point once (R8 A4, 27 Nov; Sam's note 11 on Blair's grin, Kemi's hat nub, Open Wounds chat 9): a point given
    twice in a row (or the last the same as the first) loops the curve out into a spike, so repeats are dropped here,
    in the one curve every outline uses, and no hair, hat or mouth can spike."""
    p = np.asarray(once(pts), float)
    out = []
    for i in range(len(p)):
        p0, p1, p2, p3 = p[i - 1], p[i], p[(i + 1) % len(p)], p[(i + 2) % len(p)]
        for u in np.linspace(0, 1, n, endpoint=False):
            out.append(tuple(0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                                    + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)))
    return out


def open_curve(pts, n=6):
    """Catmull-Rom through the points, end to end, stopping at the last point: for limbs, antennae, tails, wires and
    lines (curve() is the closed one, for outlined shapes)."""
    q = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = (np.asarray(q[i + d], float) for d in (-1, 0, 1, 2))
        for u in np.linspace(0, 1, n, endpoint=False):
            out.append(tuple(0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                                    + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)))
    out.append(tuple(map(float, pts[-1])))
    return out


def oval(cx, cy, rx, ry, n=48, a0=0.0, a1=2 * math.pi):
    return [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in np.linspace(a0, a1, n)]


class Pen:
    """A plain pen on a camera with P (point) and S (size): polygons, ellipses and lines in INK."""
    def __init__(self, img, cam):
        self.img, self.cam = img, cam
        self.d = ImageDraw.Draw(img)

    def poly(self, pts, fill, line=INK, lw=4):
        q = [self.cam.P(*p) for p in pts]
        if fill is not None:
            self.d.polygon(q, fill=fill)
        if line:
            self.d.line(q + [q[0]], fill=line, width=max(1, int(self.cam.S(lw) / 2)), joint='curve')

    def ell(self, cx, cy, rx, ry, fill, line=INK, lw=4, rot=0, n=40):
        pts = [(cx + rx * math.cos(a) * math.cos(rot) - ry * math.sin(a) * math.sin(rot),
                cy + rx * math.cos(a) * math.sin(rot) + ry * math.sin(a) * math.cos(rot))
               for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]
        self.poly(pts, fill, line, lw)

    def line(self, pts, colr=INK, lw=4):
        self.d.line([self.cam.P(*p) for p in pts], fill=colr, width=max(1, int(self.cam.S(lw) / 2)), joint='curve')


def glaze(img):
    """A drawer whose see-through fills (soft shadows, wet shine) blend onto what is already painted (Open Wounds chat
    12: ImageDraw.Draw(img, 'RGBA') on an RGBA frame WRITES the fill's alpha instead of blending it, so every soft
    shadow came out solid black once the frame was turned to RGB). On a frame that is already opaque it blends; on a
    see-through layer (painted later onto the frame) it writes as before, which is right there."""
    d = ImageDraw.Draw(img, 'RGBA')
    if img.mode == 'RGBA' and img.getpixel((0, 0))[3] == 255:
        d.draw = Image.core.draw(img.im, 1)
    return d

