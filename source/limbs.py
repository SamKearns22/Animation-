#!/usr/bin/env python3
"""limbs: the new arm and leg SHAPES for the people library (burnham.py), everything else in the look unchanged.

  Arms: one continuous sleeve, fuller at the shoulder and tapering to the wrist, with a real but gently rounded elbow.
        It comes out from behind the body's edge at the shoulder (the part over the body near the shoulder is hidden),
        so the body's own outline stays crisp over the join. Drawn as a solid tube, so a sharp elbow cannot fold.
  Legs: one smooth shape: fuller at the thigh, in at the knee, a little calf, slim at the ankle; a gentle curve
        through the knee. Pockets and seams drawn on a leg follow its shape. Shoes unchanged.
  Both keep the film's soft shading on the shadow side, like the limbs they replace.

Nothing in any film changes: the shapes are swapped in memory while a picture or video is drawn.

  python3 source/limbs.py still OUT.jpg          The Patriots' two-shot, today and with the new limbs, side by side
  python3 source/limbs.py animatic OUT.mp4       The Patriots animatic (540 x 960) with the new limbs
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ed import curve  # noqa: E402

INK = (24, 20, 22)


def _resample(P, step):
    seg = np.hypot(*np.diff(P, axis=0).T)
    s = np.concatenate([[0], np.cumsum(seg)])
    if s[-1] < 1e-6:
        return P, s
    n = max(2, int(s[-1] / step) + 1)
    u = np.linspace(0, s[-1], n)
    return np.stack([np.interp(u, s, P[:, 0]), np.interp(u, s, P[:, 1])], 1), u


def _normals(spine):
    t = np.gradient(spine, axis=0)
    return np.stack([-t[:, 1], t[:, 0]], 1) / (np.hypot(*t.T)[:, None] + 1e-9)


def _inside(pt, poly):
    x, y = pt
    c = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-9) + x1:
            c = not c
    return c


def _who(cam):
    """The same person's pen, even when the film makes a fresh one to redraw an arm on top."""
    if hasattr(cam, 'ox'):
        return (round(cam.ox, 1), round(cam.oy, 1), round(cam.k, 4), getattr(cam, 'flip', 1))
    return id(cam)


def _shade(lay, cam, pts, alpha, blur):
    """The film's soft shading (a blurred dark band), kept inside the shape already drawn on `lay`."""
    q = [cam.P(*v) for v in pts]
    pad = int(cam.S(blur) * 3) + 2
    x0, y0 = max(0, int(min(v[0] for v in q)) - pad), max(0, int(min(v[1] for v in q)) - pad)
    x1, y1 = min(lay.width, int(max(v[0] for v in q)) + pad), min(lay.height, int(max(v[1] for v in q)) + pad)
    if x1 <= x0 or y1 <= y0:
        return
    sh = Image.new('RGBA', (x1 - x0, y1 - y0), (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(a - x0, b - y0) for a, b in q], fill=(0, 0, 0, int(255 * alpha)))
    sh = sh.filter(ImageFilter.GaussianBlur(float(cam.S(blur))))
    keep = lay.crop((x0, y0, x1, y1)).getchannel('A')
    sh.putalpha(Image.fromarray(np.minimum(np.asarray(sh.getchannel('A')), np.asarray(keep))))
    lay.alpha_composite(sh, (x0, y0))


# ------------------------------------------------------------------------------------------------ arms

def _arm_spine(sh, el, wr, w):
    S, E, Wr = (np.asarray(v, float) for v in (sh, el, wr))
    l1, l2 = np.hypot(*(E - S)) or 1.0, np.hypot(*(Wr - E)) or 1.0
    d1, d2 = (E - S) / l1, (Wr - E) / l2
    r = min(0.9 * w, 0.4 * l1, 0.4 * l2)                   # a real elbow, its point gently rounded
    u = np.linspace(0, 1, 10)[:, None]
    corner = (1 - u) ** 2 * (E - d1 * r) + 2 * (1 - u) * u * E + u ** 2 * (E + d2 * r)
    a = S + (E - d1 * r - S) * u
    b = (E + d2 * r) + (Wr - E - d2 * r) * u
    spine = np.vstack([a, corner[1:], b[1:]])
    s = np.linspace(0, 1, len(spine))
    hw = w * (1.15 - 0.42 * s) * (1 + 0.05 * np.sin(2 * math.pi * s))   # fuller at the shoulder, slim at the wrist
    return spine, hw


def install(B):
    """Swap the people library's arms and legs for the new shapes. Returns a function that puts the old ones back."""
    old = {'arm': B.arm, 'legs': B.legs, 'poly': B.Pen.poly, 'line': B.Pen.line}
    drawn, busy = [], []
    orig_poly, orig_line = B.Pen.poly, B.Pen.line

    def follow(self, pts):
        """Things drawn on a leg (pockets, seams) move from the old straight leg onto the new one."""
        m = getattr(self, '_legmap', None)
        if not m or min(q[1] for q in pts) < 500 or max(abs(q[0]) for q in pts) > 112 + m['o']:
            return pts
        o, out = m['o'], []
        for x, y in pts:
            sgn = 1 if x > 0 else -1
            spine, hw = m[sgn]
            u = (y - 440) / 460
            c_old, h_old = sgn * (55 + (5 + o * 0.6) * u), 49 - 19 * u
            c_new, h_new = np.interp(y, spine[:, 1], spine[:, 0]), np.interp(y, spine[:, 1], hw)
            out.append((c_new + (x - c_old) * h_new / h_old, y))
        return out

    def poly(self, pts, fill, line=INK, lw=4):
        pts = follow(self, pts)
        if fill is not None and len(pts) >= 6 and not busy:  # remembered, so an arm can find the body it hangs from
            drawn.append((_who(self.cam), list(pts)))
            del drawn[:-80]
        return orig_poly(self, pts, fill, line, lw)

    def pline(self, pts, colr=INK, lw=4):
        return orig_line(self, follow(self, pts), colr, lw)

    def arm(p, sh, el, wr, sleeve, w=30):
        body = next((pts for who, pts in reversed(drawn) if who == _who(p.cam) and _inside(sh, pts)), None)
        busy.append(1)
        try:
            spine, hw = _arm_spine(sh, el, wr, w)
            lay = Image.new('RGBA', p.img.size, (0, 0, 0, 0))
            q = B.Pen(lay, p.cam)
            o = q.w(2.6) / p.cam.S(1)
            dense, sdd = _resample(spine, max(1.0, w * 0.25))
            sd = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(spine, axis=0).T))])
            hwd = np.interp(sdd / (sdd[-1] or 1.0), sd / (sd[-1] or 1.0), hw)
            for col, extra in ((INK, o), (sleeve, 0.0)):    # a solid tube, its outline underneath
                for (x_, y_), r_ in zip(dense, hwd):
                    q.ell(x_, y_, r_ + extra, r_ + extra, col, None, n=20)
            n = _normals(spine)                              # the film's soft shading, on the lower side
            left, right = spine + n * hw[:, None], spine - n * hw[:, None]
            lower = 1 if left[:, 1].mean() > right[:, 1].mean() else -1
            edge = spine + lower * n * (hw - 4)[:, None]
            inner = spine + lower * n * (hw * 0.45)[:, None]
            _shade(lay, p.cam, [tuple(v) for v in np.vstack([edge, inner[::-1]])], 0.25, 6)
            if body is not None:                             # tucked in: hidden where it lies over the body near the
                mask = Image.new('L', p.img.size, 0)         # shoulder, so it comes out from behind the body's edge
                bp = [p.cam.P(*v) for v in body]
                md = ImageDraw.Draw(mask)
                md.polygon(bp, fill=255)
                md.line(bp + bp[:1], fill=255, width=q.w(2.6) + 2, joint='curve')
                near = Image.new('L', p.img.size, 0)
                X, Y = p.cam.P(*sh)
                R = p.cam.S(math.hypot(el[0] - sh[0], el[1] - sh[1]) * 0.6)
                ImageDraw.Draw(near).ellipse([X - R, Y - R, X + R, Y + R], fill=255)
                near = near.filter(ImageFilter.GaussianBlur(float(p.cam.S(w * 0.6))))   # a soft end, never a cut
                hide = np.minimum(np.asarray(mask), np.asarray(near))
                a = np.asarray(lay.getchannel('A')).astype(np.int16) - hide
                lay.putalpha(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))
            p.img.alpha_composite(lay)
        finally:
            busy.pop()

    def legs(img, p, sp):
        tc = sp.get('trousers', sp.get('jacket', B.NAVY))
        o = sp.get('stance', 0)
        maps = {'o': o}
        for sgn in (-1, 1):
            hip, knee, ankle = (np.array(v, float) for v in ([sgn * 55, 450], [sgn * (62 + o * 0.6), 690],
                                                             [sgn * (58 + o), 890]))
            u = np.linspace(0, 1, 40)[:, None]               # one gentle curve through the knee, no corner
            spine = (1 - u) ** 2 * hip + 2 * (1 - u) * u * (2 * knee - (hip + ankle) / 2) + u ** 2 * ankle
            s = np.linspace(0, 1, len(spine))
            hw = np.interp(s, [0, 0.2, 0.48, 0.62, 0.78, 1.0], [50, 48, 37, 39, 34, 27])   # thigh, knee, calf, ankle
            k = np.exp(-0.5 * (np.arange(-6, 7) / 2.5) ** 2)
            hw = np.convolve(np.pad(hw, 6, mode='edge'), k / k.sum(), mode='valid')
            n = _normals(spine)
            left, right = spine + n * hw[:, None], spine - n * hw[:, None]
            orig_poly(p, [tuple(v) for v in np.vstack([left, right[::-1]])], tc, INK, 2.6)
            out_side = 1 if abs(left[:, 0]).mean() > abs(right[:, 0]).mean() else -1      # the film's soft shading,
            edge = spine + out_side * n * (hw - 4)[:, None]                                  # down the outer side
            inner = spine + out_side * n * (hw * 0.4)[:, None]
            B.soft(img, p.cam, [tuple(v) for v in np.vstack([edge, inner[::-1]])], (0, 0, 0), 0.3, 6)
            maps[sgn] = (spine, hw)
            orig_poly(p, curve([(sgn * (24 + o), 896), (sgn * (94 + o), 894), (sgn * (128 + o), 910),
                                (sgn * (124 + o), 928), (sgn * (20 + o), 928)], 4), (22, 20, 22), INK, 2.4)
        p._legmap = maps

    B.arm, B.legs, B.Pen.poly, B.Pen.line = arm, legs, poly, pline

    def restore():
        B.arm, B.legs, B.Pen.poly, B.Pen.line = old['arm'], old['legs'], old['poly'], old['line']
    return restore


# ------------------------------------------------------------------------------------------------ The Patriots

def patriots_frame(PP, t):
    """The Patriots' frame at t without title and captions, drawn by the film's own code."""
    B = PP.B
    view = next(v for v, a, b in PP.SHOTS if a <= t < b)
    img = B.canvas()
    cam = B.Cam(*PP.CAMS[view])
    g = PP.background(img, cam, t)
    PP.gulls(img, cam, t)
    PP.mates(img, cam, g, t, PP.MATES[:1])
    PP.stuck(img, cam, g, t, PP.WHERE)
    PP.mates(img, cam, g, t, PP.MATES[1:])
    (_, fy), s = g.feet(0, 1.0)
    sp, target = PP.rep_state(t, view)
    pst = PP.pro_state(t)
    PP.protester(img, cam, 670, fy - 928 * s, s, pst, t)
    B.person(img, cam, 220, fy - 928 * s, s, sp, t)
    PP.mic(img, B.Local(cam, 220, fy - 928 * s, s), sp['arms']['R'][1], sp['arms']['R'][0], target)
    if pst['arms']['L'][2] == 'point':
        PP.protester(img, cam, 670, fy - 928 * s, s, dict(pst, arm_only='L'), t)
    return img.convert('RGB').resize((1080, 1920), Image.LANCZOS)


def still(out, t=0.6):
    import peepee as PP
    PP.B.SS = 2
    today = patriots_frame(PP, t)
    restore = install(PP.B)
    try:
        new = patriots_frame(PP, t)
    finally:
        restore()
    w, h = 760, int(760 * 1920 / 1080)
    sheet = Image.new('RGB', (2 * w + 60, h + 110), (240, 236, 228))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 30)
    for i, (im, lab) in enumerate(((today, 'Today'), (new, 'New arm and leg shapes, everything else as today'))):
        sheet.paste(im.resize((w, h), Image.LANCZOS), (20 + i * (w + 20), 20))
        d.text((20 + i * (w + 20), h + 40), lab, font=f, fill=(20, 20, 20))
    sheet.save(out, quality=90)
    print(out)


def main():
    a = sys.argv[1:]
    if a[0] == 'still':
        still(a[1])
    elif a[0] == 'animatic':
        import peepee as PP
        install(PP.B)                                        # the render's helper processes inherit the new limbs
        PP.render(a[1], (540, 960), 26, 1)


if __name__ == '__main__':
    main()
