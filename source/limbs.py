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
  python3 source/limbs.py cryminister OUT.mp4 [--fixes]   Cry Minister's quick look (540 x 960) with the new limbs;
                                                 --fixes: steady elbows, in-betweens, no flat folds, slower arm pump
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


def _smooth(e0, e1, x):
    u = min(1.0, max(0.0, (x - e0) / (e1 - e0)))
    return u * u * (3 - 2 * u)


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
    bend = math.degrees(math.acos(max(-1.0, min(1.0, float(d1 @ d2)))))
    fold = max(0.0, min(1.0, (bend - 100) / 50))           # a tight fold: slimmer at the elbow, so it reads as a bend
    s_el = (len(a) + 4) / len(spine)
    hw = hw * (1 - 0.22 * fold * np.exp(-((s - s_el) / 0.1) ** 2))
    return spine, hw, fold, len(a) + 4, float(d1[0] * d2[1] - d1[1] * d2[0])


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
        import figure
        if 'arm' in figure._GUARDED and w <= 40:            # the film's arm checker still measures every arm
            figure.audit_arm(sh, el, wr)
        body = next((pts for who, pts in reversed(drawn) if who == _who(p.cam) and _inside(sh, pts)), None)
        busy.append(1)
        try:
            spine, hw, fold, k_el, turn = _arm_spine(sh, el, wr, w)
            lay = Image.new('RGBA', p.img.size, (0, 0, 0, 0))
            q = B.Pen(lay, p.cam)
            o = q.w(2.6) / p.cam.S(1)
            dense, sdd = _resample(spine, max(1.0, w * 0.25))
            sd = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(spine, axis=0).T))])
            hwd = np.interp(sdd / (sdd[-1] or 1.0), sd / (sd[-1] or 1.0), hw)
            for col, extra in ((INK, o), (sleeve, 0.0)):    # a solid tube, its outline underneath
                for (x_, y_), r_ in zip(dense, hwd):
                    q.ell(x_, y_, r_ + extra, r_ + extra, col, None, n=20)
            n = _normals(spine)
            if fold > 0.2:                                   # a small crease inside a tight bend
                side = -1 if turn > 0 else 1
                c0 = spine[k_el] + side * n[k_el] * hw[k_el] * 0.95
                q.line([tuple(c0), tuple(c0 - side * n[k_el] * hw[k_el] * 0.6 * fold)], INK, 2.0)
            # the film's soft shading, on the lower side
            left, right = spine + n * hw[:, None], spine - n * hw[:, None]
            lower = 1 if left[:, 1].mean() > right[:, 1].mean() else -1
            edge = spine + lower * n * (hw - 4)[:, None]
            inner = spine + lower * n * (hw * 0.45)[:, None]
            _shade(lay, p.cam, [tuple(v) for v in np.vstack([edge, inner[::-1]])], 0.25, 6)
            if body is not None:
                # Tucked in: only the top of the UPPER arm (where it grows out of the shoulder) is hidden where it lies
                # over the body, fading out along the arm. The forearm and hand are never hidden, wherever they go
                # (a hand brought up across the chest near the shoulder stays in front of the body).
                l1 = math.hypot(el[0] - sh[0], el[1] - sh[1]) or 1.0
                along = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(spine, axis=0).T))])
                upper = Image.new('L', p.img.size, 0)
                ud = ImageDraw.Draw(upper)
                for i in range(k_el, -1, -1):                # from the elbow back to the shoulder, rising weight
                    wgt = 1.0 - _smooth(0.3 * l1, 0.6 * l1, along[i])
                    if wgt <= 0:
                        continue
                    X, Y = p.cam.P(*spine[i])
                    R = p.cam.S(hw[i] + o) + 2
                    ud.ellipse([X - R, Y - R, X + R, Y + R], fill=int(255 * wgt))
                fore = Image.new('L', p.img.size, 0)
                fd = ImageDraw.Draw(fore)
                for i in range(k_el, len(spine)):
                    X, Y = p.cam.P(*spine[i])
                    R = p.cam.S(hw[i] + o) + 2
                    fd.ellipse([X - R, Y - R, X + R, Y + R], fill=255)
                mask = Image.new('L', p.img.size, 0)
                bp = [p.cam.P(*v) for v in body]
                md = ImageDraw.Draw(mask)
                md.polygon(bp, fill=255)
                md.line(bp + bp[:1], fill=255, width=q.w(2.6) + 2, joint='curve')
                hide = np.minimum(np.asarray(mask), np.asarray(upper)).astype(np.int16)
                hide[np.asarray(fore) > 0] = 0
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


# ------------------------------------------------------------------------------------------------ Cry Minister fixes

def _arm_near(F, rig, side, target, bend, prev):
    """The rig's arm, but with the elbow on whichever of its two possible sides is nearer to where it was a frame ago
    (the bend rule only chooses the first frame), so an elbow never flips across in a single frame."""
    sh = rig.shoulder(side)
    U, Fh = rig.upper, rig.fore + F.HAND.get('fist', 14)
    dx, dy = target[0] - sh[0], target[1] - sh[1]
    d = min(math.hypot(dx, dy), U + Fh)
    d = max(d, abs(U - Fh) + 1e-3)
    a = math.acos(max(-1.0, min(1.0, (U * U + d * d - Fh * Fh) / (2 * U * d))))
    base = math.atan2(dy, dx)
    cands = [(sh[0] + U * math.cos(base + s_ * a), sh[1] + U * math.sin(base + s_ * a)) for s_ in (1, -1)]
    if prev is None:
        sgn = -1 if side == 'L' else 1
        key = {'out': lambda e: sgn * e[0], 'in': lambda e: -sgn * e[0], 'down': lambda e: e[1], 'up': lambda e: -e[1]}[bend]
        el = max(cands, key=key)
    else:
        el = min(cands, key=lambda e: math.hypot(e[0] - prev[0], e[1] - prev[1]))
    dd = math.hypot(target[0] - el[0], target[1] - el[1]) or 1.0
    wr = (el[0] + (target[0] - el[0]) / dd * rig.fore, el[1] + (target[1] - el[1]) / dd * rig.fore)
    return el, wr


def cryminister_fixes(CM):
    F = CM.F
    B_ = CM.B_
    # 3. moves too fast for 12 frames a second: an in-between for "Any job", a longer face-palm swing
    CM.GEST[10] = dict(
        L=B_(10, (-0.1, 'set-up', (-200, 300)), (0.12, 'lift', (-330, 170)), (0.42, 'wide', (-410, 30), 'slow'), (2.0, 'hold', (-400, 40))),
        R=B_(10, (-0.1, 'set-up', (200, 300)), (0.12, 'lift', (330, 170)), (0.42, 'wide', (410, 30), 'slow'), (2.0, 'hold', (400, 40))))
    CM.GEST[15] = dict(R=B_(15, (-0.3, 'set-up', (140, 260)), (-0.17, 'swing out', (290, 60)), (-0.05, 'up', (190, -160)),
                            (0.14, 'palm', (-8, -212)), (4.0, 'hold', (-10, -214))))
    CM.GEST[18] = {sd: B_(18, (-0.05, 'set-up', (g * 200, 260)), (0.1, 'lift', (g * 255, 150)),
                          (0.32, 'palms out', (g * 260, -30)), (2.0, 'hold', (g * 250, -20)))
                   for sd, g in (('L', -1), ('R', 1))}
    # 2. "COME ON": fists to the chest a little lower and further out, so the arms bend instead of folding flat
    CM.GEST[16] = {sd: B_(16, (-0.12, 'raise', (g * 330, 0)), (0.18, 'pull', (g * 250, 190), 'fast'),
                          (0.3, 'COME ON', (g * 160, 250), 'fast'), (0.5, 'shake', (g * 170, 228)),
                          (0.7, 'COME ON', (g * 160, 255), 'fast'), (1.4, 'hold', (g * 165, 250)))
                   for sd, g in (('L', -1), ('R', 1))}
    # 1. elbows keep to the side they were on: each frame's elbow is the solution nearest the last frame's, walked
    #    through from the start of the shot (so every frame is the same however the render splits the work)
    orig = CM.andy_sp

    def andy_sp(t, n=None):
        sp = orig(t, n)
        n = n or CM.line_of_t(t)
        g = CM.GEST.get(n)
        if not g:
            return sp
        rig = F.Rig(sp)
        t0 = CM.shot_at(t)[1]
        for side, beats in g.items():
            bend = CM.BEND.get(n, {}).get(side, 'out')
            prev = None
            k = math.ceil(t0 * CM.FPS - 1e-6)
            steps = [k / CM.FPS for k in range(k, int(math.floor(t * CM.FPS + 1e-6)) + 1)] or [t]
            if abs(steps[-1] - t) > 1e-6:
                steps.append(t)
            for tt in steps:
                el, wr = _arm_near(F, rig, side, beats.at(tt), bend, prev)
                prev = el
            sp['arms'][side] = (el, wr, 'fist')
        return sp
    CM.andy_sp = andy_sp
    # 4. the running man pumps his arms twice a second (six drawings a pump) instead of three (four drawings)
    orig_man = CM.alley_man
    CM.alley_man = lambda img, X, d, duck, u: orig_man(img, X, d, duck, u * 2 / 3)


def main():
    a = sys.argv[1:]
    if a[0] == 'still':
        still(a[1])
    elif a[0] == 'animatic':
        import peepee as PP
        install(PP.B)                                        # the render's helper processes inherit the new limbs
        PP.render(a[1], (540, 960), 26, 1)
    elif a[0] == 'cryminister':
        import cryminister as CM
        install(CM.B)                                        # after the film's own arm checker, which stays on
        if '--fixes' in a:
            cryminister_fixes(CM)
        CM.E.render('cryminister-limbs', a[1], size=(540, 960), ss=1, fps=CM.FPS, dur=CM.DUR, picture=CM.picture,
                    overlay=CM.overlay, shot_of=CM.shot_of, sound=CM.soundtrack, write_wav=CM.MA.write_wav,
                    set_ss=lambda v: setattr(CM.B, 'SS', v), crf=26)


if __name__ == '__main__':
    main()
