#!/usr/bin/env python3
"""MAP  faces: the measured face layout and its parts (one-route-kit Change 2, 20 Nov). Lifted out of three finished
films' files (now frozen at their bookmarks) so no kit file loads a finished film: the layout and parts from The
Patriots 4's cast, the eye and the clip from The Traitors' cast, the ears, tufts and house mouths from Ad-Vanced
Notice's cast. Same code, same pictures; the old characters' own measures (Romesh, Bash, Claudia) stay with their
films. The people kit fills MEASURED, PUSH and TUNE for a measured likeness (people_famous, people_walliams).

Map: colours dk, blend | clip_convex | eye | talk_or | the layout (AVG, MEASURED, target, layout, H, Face) |
outline_uv, eyes, brow_uv, brows, lop, nose, lips | ears, tufts, inside | house_mouth
"""
import math

import numpy as np

import mouths
from ink import INK, curve, open_curve, oval



def blend(a, b, k):
    return tuple(int(round(x + (y - x) * k)) for x, y in zip(a, b))


def dk(c, k=0.8):
    return tuple(int(v * k) for v in c)


def clip_convex(subject, window):
    """The part of a shape inside a convex window (Sutherland-Hodgman): an iris kept inside its eye."""
    def inside(q, a, b):
        return (b[0] - a[0]) * (q[1] - a[1]) - (b[1] - a[1]) * (q[0] - a[0]) >= 0

    def cross(p1, p2, a, b):
        x1, y1, x2, y2, x3, y3, x4, y4 = *p1, *p2, *a, *b
        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(d) < 1e-9:
            return p2
        u = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
        return (x1 + u * (x2 - x1), y1 + u * (y2 - y1))
    out = list(subject)
    for i in range(len(window)):
        a, b = window[i], window[(i + 1) % len(window)]
        inp, out = out, []
        if not inp:
            break
        s = inp[-1]
        for e in inp:
            if inside(e, a, b):
                if not inside(s, a, b):
                    out.append(cross(s, e, a, b))
                out.append(e)
            elif inside(s, a, b):
                out.append(cross(s, e, a, b))
            s = e
    return out


def eye(p, ex, ey, sgn, w, h, iris, st, lid_c, liner=2.6, lower=1.4, lashes=False, smoky=None, iris_r=0.95, pupil_r=0.42):
    """One opening between two lids, the iris cut to it (no line ever crosses the white). st: lid (0 open .. 1 shut),
    look (-1 .. 1 across), gaze_dy (down +), squint (lower lid up), closed."""
    us = np.linspace(-1, 1, 15)
    if smoky:                                          # made-up eyes: a flat dark shadow round the opening
        p.poly(curve([(ex - w - 4, ey + 1), (ex - w * 0.4, ey - h - 7), (ex + w * 0.5, ey - h - 8), (ex + w + 7, ey - 3),
                      (ex + w * 0.6, ey + h + 3), (ex - w * 0.5, ey + h + 3)], 4), smoky, None)
    if st.get('closed'):
        p.line([(ex + w * u, ey + 1 + h * 0.45 * (1 - u * u)) for u in us], INK, liner)
        return
    lid, squint = st.get('lid', 0.0), st.get('squint', 0.0)
    up_open = [(ex + w * u, ey - h * (1 - u * u)) for u in us]
    up = [(ex + w * u, ey - h * (1 - u * u) * (1 - lid)) for u in us]
    lo = [(ex + w * u, ey + h * 0.8 * (1 - squint) * (1 - u * u)) for u in us]
    opening = up + lo[::-1][1:-1]
    p.poly(opening, (250, 250, 247), None)
    cx, cy = ex + st.get('look', 0.0) * w * 0.38, ey + st.get('gaze_dy', 0.0)
    circ = lambda r: [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 22, endpoint=False)]
    ir = clip_convex(opening[::-1], circ(h * iris_r))
    if len(ir) >= 3:
        p.poly(ir, iris, None)
    pu = clip_convex(opening[::-1], circ(h * pupil_r))
    if len(pu) >= 3:
        p.poly(pu, INK, None)
    if lid > 0.02:
        p.poly(up_open + up[::-1], lid_c, None)
    p.line(lo, INK if smoky else dk(lid_c, 0.7), lower)
    p.line(up, INK, liner)
    if lashes:
        tip = up[-1] if sgn > 0 else up[0]
        p.line([tip, (tip[0] + sgn * 7, tip[1] - 5)], INK, liner * 0.8)


def talk_or(p, sp, t, fx, my, rest):
    m = sp.get('mouth', 'rest')
    if isinstance(m, str) and m.startswith('v:') and m != 'v:rest':
        mouths.draw(p, sp, fx, my, m[2:])
    else:
        rest()


AVG = dict(face_wide=0.872, jaw_wide=0.82, forehead_wide=0.942, eyes_apart=1.325, eye_size=0.186, eye_open=0.313,
           eye_tilt=2.474, brow_high=0.586, brow_slope=-9.371, nose_long=0.417, nose_wide=0.641, mouth_wide=0.802,
           lip_top=0.121, lip_low=0.183, philtrum=0.133, chin_long=0.295)


MEASURED = {}      # a measured likeness's face, by who (people_famous / people_walliams fill it)
PUSH = {}          # how far each likeness is pushed
TUNE = {}          # per measure, an extra push where the first check found the drawing under the photo (rule 49)


def target(who, average=False):
    """The measures to draw: the person's, pushed further from the middle (or the middle itself, for the twin)."""
    if average:
        return dict(AVG)
    m, k = MEASURED[who], PUSH[who]
    return {key: AVG[key] + k * TUNE[who].get(key, 1.0) * (m[key] - AVG[key]) for key in AVG}


def layout(m):
    """Where everything goes, as fractions of the face height H (forehead top 0 .. chin 1; x from the middle),
    laid out on MediaPipe's average face (likeness.canonical) and moved to give the measures m."""
    fw = m['face_wide']
    ew = m['eye_size'] * fw
    gap = m['eyes_apart'] * ew
    ecx = gap / 2 + ew / 2
    ipd = 2 * ecx
    eye_y = 0.32
    eh = m['eye_open'] * ew                            # the opening's height (upper lid to lower lid)
    lid_top = eye_y - eh / 2
    brow_y = lid_top - m['brow_high'] * ew             # the brow's lower edge over the pupil (landmark 52)
    slope = math.tan(math.radians(m['brow_slope']))   # + rises to the outside
    nose_y = 0.283 + m['nose_long'] * 0.717
    lip0 = nose_y + m['philtrum'] * 0.717
    mw = m['mouth_wide'] * ipd
    lip13 = lip0 + m['lip_top'] * mw
    lip17 = lip13 + 0.006 + m['lip_low'] * mw
    want17 = 1.0 - m['chin_long'] * 0.717                # the chin's length: meet it halfway by moving the mouth
    k = 1.0 + 0.5 * ((want17 - nose_y) / (lip17 - nose_y) - 1.0)
    lip0, lip13, lip17 = (nose_y + (v - nose_y) * k for v in (lip0, lip13, lip17))
    return dict(fw=fw, jw=m['jaw_wide'] * fw, fhw=m['forehead_wide'] * fw, ew=ew, ecx=ecx, eye_y=eye_y, eh=eh,
                lid_top=lid_top, brow_y=brow_y, slope=slope, nose_y=nose_y, nw=m['nose_wide'] * ipd, lip0=lip0,
                lip13=lip13, lip17=lip17, mw=mw, tilt=math.tan(math.radians(m['eye_tilt'])))


H = 172.0          # the face height in the person's own units (the library's heads are about 190 from crown to chin)


class Face:
    """Turns the layout's fractions into the person's units: x across from the face's middle, y down from the top of
    the forehead. `tq` (0..1) turns it towards a three-quarter view facing our right (features slide to the near
    side, the far half narrows), so the likeness survives the turn (newsdesk_cast's way)."""

    def __init__(self, hx, hy, tq=0.0, turn=0.0, down=0.0):
        self.cx, self.top = hx + turn * 12, hy - 72 + 10 * down
        self.hx, self.tq = hx, tq

    def x(self, u):
        k = 1.0 - 0.38 * self.tq if u < 0 else 1.0 - 0.1 * self.tq     # the far side (our left) narrows
        return self.cx + 0.2 * self.tq * H + u * H * k

    def __call__(self, u, v):
        return (self.x(u), self.top + v * H)

    def pts(self, uvs):
        return [self(u, v) for u, v in uvs]


def outline_uv(L, chin_w=0.36, crown=-0.17):
    """The head's outline (fractions), round from the left temple over the crown and down to the chin."""
    fw, jw, fhw = L['fw'], L['jw'], L['fhw']
    right = [(fhw * 0.5 * 0.93, 0.0), (fhw * 0.5, 0.16), (fw * 0.5, 0.43), (fw * 0.5 * 0.97, 0.6),
             (jw * 0.5, 0.82), (jw * 0.5 * chin_w + 0.04, 0.965), (0.0, 1.0)]
    top = [(fhw * 0.5 * 0.7, crown * 0.6), (0.0, crown)]
    left = [(-u, v) for u, v in right[::-1][1:]]
    return [(-u, v) for u, v in top[::-1]] + top[1:] + right + left + [(-fhw * 0.5 * 0.93, 0.0), (-fhw * 0.5 * 0.7, crown * 0.6)]


def eyes(p, f, L, sp, iris, lid_c, liner=2.6, wide=0.0, iris_r=0.95, pupil_r=0.42, scale=1.0):
    """Both eyes (traitors_cast.eye: one opening between two lids, the iris cut to it). wide (0..1): the stare."""
    w = L['ew'] * H / 2 * scale
    h = L['eh'] * H / 1.8 * (1 + 0.55 * wide) * scale
    st = dict(lid=sp.get('lid4', 0.08) * (1 - wide), look=sp.get('look', 0.0), squint=sp.get('squint', 0.0),
              closed=sp.get('blink', False), gaze_dy=sp.get('gaze_dy', 0.0))
    for sgn in (-1, 1):
        ex, ey = f(sgn * L['ecx'], L['eye_y'])
        ww = w * (1 - 0.3 * f.tq if sgn < 0 else 1.0)
        eye(p, ex, ey, sgn, ww, h, iris, st, lid_c, liner=liner, iris_r=iris_r, pupil_r=pupil_r)


def brow_uv(L, thick=0.034, up=0.0, frown=0.0, arch=0.0, taper=0.0, peak=0.21):
    """One brow's outline (our right side, x from the face's middle) in the layout's fractions. arch bends the two
    ENDS down from the peak (face tool chat 10: lifting the peak instead lifted the whole brow off the measured
    height, so Kemi's thin arched brows sat a fifth of an eye above her own); peak: where the peak sits, eye widths
    out from the eye's middle (0.21 the house's)."""
    ecx, ew = L['ecx'], L['ew']
    xi, xo, xm = ecx - 0.69 * ew, ecx + 0.98 * ew, ecx + peak * ew
    y_m = L['brow_y'] - thick * 0.35 - up
    yi = y_m + L['slope'] * (xm - xi) * 1.0 + frown + arch * 0.6
    yo = y_m - L['slope'] * (xo - xm) + arch
    ym = y_m - 0.008
    th = thick
    return [(xi, yi - th * 0.45), (xm, ym - th * 0.6), (xo, yo - th * 0.2 * (1 - taper)), (xo + 0.01, yo + th * 0.15 * (1 - taper)),
            (xm, ym + th * 0.45), (xi, yi + th * 0.55)]


def brows(p, f, L, c, thick=0.034, raise_=0.0, frown=0.0, arch=0.0, taper=0.0, peak=0.21):
    """Filled brows from inner to outer end at the measured height and slope. raise_ lifts them (surprise);
    frown pulls the inner ends down (narrowed, accusing). raise_ may be a pair (our left, our right): one brow up.
    arch bends the ends down from the peak; taper (0..1) thins the outer end (the face tool's house heads)."""
    for sgn in (-1, 1):
        up = raise_[0 if sgn < 0 else 1] if isinstance(raise_, (tuple, list)) else raise_
        uv = brow_uv(L, thick, up, frown, arch, taper, peak)
        p.poly(curve(f.pts([(sgn * u, v) for u, v in uv]), 3), c, None)


LOPSIDED = dict(brow=0.032, mouth=3.2, hair=0.075)   # Job K proposal 5 (Sam: Y, 11 Nov), the driver sheet's amounts


def lop(sp):
    """A face a touch uneven, for INVENTED people only (a likeness head stays as measured): sp['lopsided'] True for
    LOPSIDED, or a dict of its keys. brow: our left brow that much higher; mouth: our right corner lifted (smile
    units); hair: the side hair on our right reaching that much higher (the head's own drawing reads it)."""
    v = sp.get('lopsided')
    return dict(LOPSIDED) if v is True else dict(v or {})


def nose(p, f, L, skin):
    """The bridge as one line down one side, the tip and the nostril wings at the measured width."""
    nw, y = L['nw'], L['nose_y']
    sd = dk(skin, 0.72)
    p.line(f.pts([(-0.025, L['eye_y'] + 0.02), (-0.04, y - 0.07)]), sd, 1.8)
    for sgn in (-1, 1):                                # the wings: a curve round each side of the nose's base
        p.line(curve(f.pts([(sgn * nw * 0.32, y - 0.075), (sgn * nw * 0.5, y - 0.045), (sgn * nw * 0.46, y - 0.012),
                            (sgn * nw * 0.26, y - 0.002)]), 3), INK, 1.8)
    p.line(curve(f.pts([(-nw * 0.2, y - 0.002), (-0.03, y + 0.005), (0.0, y - 0.004), (0.03, y + 0.005),
                        (nw * 0.2, y - 0.002)]), 3), INK, 1.6)
    for sgn in (-1, 1):
        p.poly(oval(*f(sgn * nw * 0.2, y - 0.016), 5, 3, 10), dk(skin, 0.5), None)


def lips(p, f, L, sp, lip_c, fx_my):
    """Closed lips at the measured width and fullness; talking shapes from mouths.draw (the series' lip sync)."""
    fx, my = fx_my
    mw, l0, l13, l17 = L['mw'], L['lip0'], L['lip13'], L['lip17']
    smile = sp.get('smile', 0.0)
    sr = smile + lop(sp).get('mouth', 0.0)              # our right corner (lifted on a lopsided face)

    def rest():
        hw = mw / 2
        top = curve(f.pts([(-hw, l13 - 0.004 * smile), (-hw * 0.4, l0 + 0.006), (0.0, l0 + 0.012), (hw * 0.4, l0 + 0.006),
                           (hw, l13 - 0.004 * sr), (0.0, l13 + 0.004)]), 3)
        bot = curve(f.pts([(-hw, l13 - 0.004 * smile), (0.0, l13 + 0.004), (hw, l13 - 0.004 * sr), (hw * 0.5, l17 - 0.01),
                           (0.0, l17), (-hw * 0.5, l17 - 0.01)]), 3)
        p.poly(top, dk(lip_c, 0.86), INK, 1.5)
        p.poly(bot, lip_c, INK, 1.5)
        p.line(curve(f.pts([(-hw, l13 - 0.006 * smile), (-hw * 0.3, l13 + 0.004), (hw * 0.3, l13 + 0.004),
                            (hw, l13 - 0.006 * sr)]), 3), INK, 2.2)
    talk_or(p, dict(sp, lips=True, lip_c=lip_c), 0.0, fx, my, rest)


V_SKIN = (232, 178, 152)          # the house mouth's default skin and lip (fair, pink)
V_LIP = (204, 134, 120)


def ears(p, f, L, skin):
    for sgn in (-1, 1):
        if sgn < 0 and f.tq > 0.5:
            continue
        ex, ey = f(sgn * (L['fw'] * 0.5 + 0.01), 0.42)
        p.poly(oval(ex, ey, 11, 24, 20), skin, INK, 2.4)
        p.line([(ex - sgn * 2, ey - 10), (ex + sgn * 3, ey), (ex - sgn * 1, ey + 10)], dk(skin, 0.7), 1.4)


def tufts(pts, amp, step, out=1.0, seed=0):
    """A hair edge: the polyline resampled every `step` and every other point pushed `amp` to one side (out=+1 to the
    left of the travel direction, -1 to the right), so the edge is a row of small pointed tufts, not a ruled line."""
    import random
    rng = random.Random(seed)
    res = []
    for (u0, v0), (u1, v1) in zip(pts, pts[1:]):
        d = math.hypot(u1 - u0, v1 - v0)
        n = max(1, int(d / step))
        nu, nv = -(v1 - v0) / (d + 1e-9), (u1 - u0) / (d + 1e-9)
        for k in range(n):
            t = k / n
            u, v = u0 + (u1 - u0) * t, v0 + (v1 - v0) * t
            if k % 2:
                a = amp * out * rng.uniform(0.6, 1.0)
                u, v = u + nu * a, v + nv * a
            res.append((u, v))
    res.append(pts[-1])
    return res


def inside(poly, x, y):
    """Point in polygon (ray casting)."""
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
            c = not c
    return c


def house_mouth(p, f, L, kind, lip=None, skin=None, wide=1.12, gap=0.0, creases=1.0, drop=None):
    """His mouths for the moods: 'soft' (closed, corners up a little, earnest), 'grin' (open, top teeth, corners
    high), 'smirk' (closed, one corner up: our right). lip, skin: another person's colours (the face tool's house
    heads, chat 8); wide: the grin's width over the measured mouth; gap: a gap between the front teeth (its width in
    face heights); creases: the smile creases' length and depth; drop: the grin's depth below the lip line (thin-
    lipped faces measure almost none)."""
    hw, l0, l13, l17 = L['mw'] / 2, L['lip0'], L['lip13'], L['lip17']
    if drop is not None:
        l17 = max(l17, l13 + drop)
    lip, skin = lip or V_LIP, skin or V_SKIN
    if kind == 'grin':
        hw *= wide
        top = [(-hw, l13 - 0.03), (-hw * 0.5, l13 - 0.012), (0.0, l13 - 0.008), (hw * 0.5, l13 - 0.012), (hw, l13 - 0.03)]
        bot = [(hw, l13 - 0.03), (hw * 0.55, l17 + 0.012), (0.0, l17 + 0.03), (-hw * 0.55, l17 + 0.012)]
        p.poly(curve(f.pts(top + bot), 3), (70, 26, 30), INK, 2.2)
        # Open Wounds chat 7 (Sam's note 10 on Blair's grin: "Tony's teeth look a bit...fleshy"): the teeth were a thin
        # strip at the top of a deep dark mouth, the top lip's line ran ACROSS them (its middle at lip0 + 0.008, below
        # the opening's top edge on a thin-lipped face) and, drawn with the closed curve, it doubled back as a loose
        # line over the mouth. Now (his photo): a full top row filling the opening's upper half, the thin top lip ON
        # the opening's top edge, every line open (open_curve), so nothing doubles back.
        D = (l17 + 0.03) - (l13 - 0.008)                                   # the opening's depth at the middle
        teeth = [(-hw * 0.88, l13 - 0.027), (-hw * 0.5, l13 - 0.011), (0.0, l13 - 0.007), (hw * 0.5, l13 - 0.011),
                 (hw * 0.88, l13 - 0.027), (hw * 0.66, l13 - 0.008 + 0.40 * D), (0.0, l13 - 0.008 + 0.55 * D),
                 (-hw * 0.66, l13 - 0.008 + 0.40 * D)]
        p.poly(curve(f.pts(teeth), 3), (250, 248, 240), None)
        if gap:
            p.poly(curve(f.pts([(-gap / 2, l13 - 0.008), (gap / 2, l13 - 0.008), (gap / 2.4, l13 + 0.5 * D),
                                (-gap / 2.4, l13 + 0.5 * D)]), 2), (70, 26, 30), None)
        p.line(open_curve(f.pts([(-hw, l13 - 0.03), (-hw * 0.5, l13 - 0.014), (0.0, l13 - 0.011), (hw * 0.5, l13 - 0.014),
                                 (hw, l13 - 0.03)]), 3), dk(lip, 0.8), 3.0)              # the thin top lip, on the edge
        for sgn in (-1, 1):                                                                # smile creases
            if creases:
                p.line(open_curve(f.pts([(sgn * (hw + 0.03), l13 - 0.07 * creases), (sgn * (hw + 0.03 + 0.02 * creases),
                                         l13 - 0.02), (sgn * (hw + 0.035), l13 + 0.03 * creases)]), 3),
                       dk(skin, 0.75 - 0.05 * (creases - 1)), 1.6 * creases)
        return
    if kind == 'soft':
        ends = (0.014, 0.014)
    else:                                                                                  # smirk
        ends = (-0.002, 0.04)
    a, b = ends
    line = [(-hw, l13 - a), (-hw * 0.4, l13 + 0.004 - a * 0.3), (0.0, l13 + 0.004), (hw * 0.4, l13 + 0.004 - b * 0.3),
            (hw, l13 - b)]
    top = curve(f.pts([(-hw, l13 - a), (-hw * 0.4, l0 + 0.006), (0.0, l0 + 0.01), (hw * 0.4, l0 + 0.006),
                       (hw, l13 - b)] + line[::-1][1:-1]), 3)
    bot = curve(f.pts(line + [(hw * 0.5, l17 - 0.012 - b * 0.3), (0.0, l17 - 0.004), (-hw * 0.5, l17 - 0.012 - a * 0.3)]), 3)
    p.poly(top, dk(lip, 0.86), INK, 1.5)
    p.poly(bot, lip, INK, 1.5)
    p.line(curve(f.pts(line), 3), INK, 2.4)
    for sgn, e in ((-1, a), (1, b)):                                                       # a dimple at a raised corner
        if e > 0.01:
            p.line(curve(f.pts([(sgn * (hw + 0.012), l13 - e - 0.02), (sgn * (hw + 0.022), l13 - e + 0.004)]), 2),
                   dk(skin, 0.75), 1.6)
