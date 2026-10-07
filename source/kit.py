#!/usr/bin/env python3
"""Shared polish for the flat cartoon films (any burnham.py person): contact shadows, a hands library, and
secondary motion (things that sway a beat behind the body). General tools, not tied to one film; read
guides/figure-rig.md.

    import kit
    kit.install(B)                                   # teaches burnham's hands the new shapes
    kit.contact_shadow(img, cam, x, floor_y, width)  # under feet, chair castors, props
    sp['arms']['R'] = rig.arm('R', target, 'cup')    # a hand holding a takeaway cup (figure.HAND has its offset)
    swing = kit.follow(t, keys)                      # a damped lag for lanyards, scarves, ropes, ponytails
    kit.dangle(p, top, length, angle, colr)          # draw a hanging strap/rope at that swing

    python3 kit.py sheet OUT.png                     # every hand shape, shadows, and a lanyard swinging
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFilter

INK = (24, 20, 22)


# ------------------------------------------------------------------------------------------- shadows
def contact_shadow(img, cam, x, y, w, h=None, alpha=0.28, colr=(0, 0, 0)):
    """A soft, flat shadow where something meets the ground (world units): x, y the contact point, w its width.
    Feet, chair castors, bins and boxes all get one, so nothing floats."""
    h = h if h is not None else w * 0.18
    X, Y = cam.P(x, y)
    W, H = cam.S(w), cam.S(h)
    pad = int(H * 2 + 4)
    lay = Image.new('RGBA', (int(W) + 2 * pad, int(H) + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([pad, pad, pad + W, pad + H], fill=colr + (int(255 * alpha),))
    lay = lay.filter(ImageFilter.GaussianBlur(max(1, H * 0.35)))
    img.alpha_composite(lay, (int(X - W / 2 - pad), int(Y - H / 2 - pad)))


def feet_shadow(img, cam, x, y, s, stance=0.0, alpha=0.28):
    """The shadow under a standing burnham person (x, y the neck base, s the scale): one soft pool under both shoes."""
    import figure as F
    contact_shadow(img, cam, x, y + F.SOLE_Y * s, (300 + 2 * stance) * s, alpha=alpha)


# ------------------------------------------------------------------------------------------- hands
# Contact offsets beyond the wrist along the forearm, for figure.Rig (added to figure.HAND by install()).
HAND_OFFSETS = {'relaxed': 18, 'flat': 34, 'cup': 22, 'phone': 26, 'pen': 30, 'wave': 34, 'thumbs': 20, 'grip': 16}


def _frame(el, wr):
    dx, dy = wr[0] - el[0], wr[1] - el[1]
    n = math.hypot(dx, dy) or 1
    d = (dx / n, dy / n)
    return d, (-d[1], d[0])


def hand(p, el, wr, shape, skin, extra=None, t=0.0):
    """The extra hand shapes (person's own units). Returns True if drawn here (else burnham draws its own)."""
    from burnham import dk, finger
    from ed import curve
    d, nrm = _frame(el, wr)
    c = (wr[0] + d[0] * 16, wr[1] + d[1] * 16)
    shade = dk(skin, 0.8)
    P = lambda a, b: (c[0] + d[0] * a + nrm[0] * b, c[1] + d[1] * a + nrm[1] * b)
    if shape == 'relaxed':       # loosely curled fingers, thumb resting along them
        p.poly(curve([P(-14, -18), P(16, -20), P(30, -10), P(28, 14), P(8, 20), P(-14, 16)], 3), skin, INK, 2.4)
        for k in range(3):
            p.line([P(14 + 4 * k, -14 + 9 * k), P(26, -12 + 9 * k)], shade, 1.6)
        return True
    if shape == 'flat':          # resting flat on a surface, fingers together
        p.poly(curve([P(-12, -20), P(40, -18), P(50, -6), P(48, 10), P(-12, 18)], 3), skin, INK, 2.4)
        for k in range(3):
            p.line([P(26, -12 + 8 * k), P(46, -11 + 8 * k)], shade, 1.4)
        return True
    if shape == 'cup':           # holding a takeaway cup upright (a 12 oz cup is about half a head tall)
        cx, cy = P(18, 0)
        p.poly([(cx - 22, cy - 46), (cx + 22, cy - 46), (cx + 17, cy + 40), (cx - 17, cy + 40)], (246, 245, 241), INK, 2.2)
        p.poly([(cx - 25, cy - 56), (cx + 25, cy - 56), (cx + 23, cy - 44), (cx - 23, cy - 44)], (60, 60, 66), INK, 2.0)
        p.poly([(cx - 21, cy - 8), (cx + 21, cy - 8), (cx + 20, cy + 14), (cx - 20, cy + 14)], (170, 120, 80), None)
        p.ell(cx - 6, cy + 2, 24, 22, skin, INK, 2.4)            # fingers wrapped round the front
        for k in range(3):
            p.line([(cx - 22, cy - 8 + 9 * k), (cx + 10, cy - 8 + 9 * k)], shade, 1.6)
        return True
    if shape == 'phone':         # a phone held up, screen towards the viewer's side
        cx, cy = P(20, 0)
        p.poly([(cx - 20, cy - 38), (cx + 20, cy - 38), (cx + 20, cy + 38), (cx - 20, cy + 38)], (30, 30, 34), INK, 2.2)
        p.poly([(cx - 16, cy - 33), (cx + 16, cy - 33), (cx + 16, cy + 33), (cx - 16, cy + 33)], (150, 190, 230), None)
        p.ell(cx, cy + 22, 20, 18, skin, INK, 2.2)
        p.line([(cx + 14, cy + 8), (cx + 20, cy - 6)], skin, 7)   # thumb over the screen edge
        return True
    if shape == 'pen':           # pinching a pen between thumb and fingers
        p.ell(c[0], c[1], 20, 18, skin, INK, 2.4)
        tip = P(46, 6)
        p.line([P(-6, -14), tip], (30, 50, 120), 4.5)
        p.line([P(36, 4), tip], (220, 220, 220), 2.0)
        return True
    if shape == 'wave':          # open hand, fingers spread (a wave or a 'stop')
        for k in range(4):
            a = -0.5 + 0.33 * k
            u = (d[0] * math.cos(a) - d[1] * math.sin(a), d[1] * math.cos(a) + d[0] * math.sin(a))
            finger(p, (c[0] + u[0] * 14, c[1] + u[1] * 14), u, 30, skin, 7)
        thumb = (d[0] * math.cos(-1.3) - d[1] * math.sin(-1.3), d[1] * math.cos(-1.3) + d[0] * math.sin(-1.3))
        finger(p, (c[0] + thumb[0] * 12, c[1] + thumb[1] * 12), thumb, 22, skin, 7)
        p.ell(c[0], c[1], 22, 20, skin, INK, 2.4)
        return True
    if shape == 'thumbs':        # thumbs up
        finger(p, (c[0], c[1] - 14), (0.1, -1), 28, skin, 9)
        p.ell(c[0], c[1], 24, 22, skin, INK, 2.6)
        for k in range(3):
            p.line([(c[0] - 14, c[1] - 6 + 8 * k), (c[0] + 12, c[1] - 8 + 8 * k)], shade, 1.8)
        return True
    if shape == 'grip':          # closed round a rail, rope or handle (draw the rail through the fist yourself)
        p.ell(c[0], c[1], 24, 21, skin, INK, 2.6)
        for k in range(4):
            p.line([P(-4 + 6 * k, -16), P(-2 + 6 * k, 14)], shade, 1.6)
        return True
    return False


_installed = {}


def install(B):
    """Teach burnham's hands the shapes above, and the figure rig their contact offsets."""
    if 'hand' in _installed:
        return
    import figure as F
    F.HAND.update(HAND_OFFSETS)
    inner = B.gesture_hand
    _installed['hand'] = inner

    def gesture_hand(p, el, wr, shape, skin, extra=None, t=0.0):
        if not hand(p, el, wr, shape, skin, extra, t):
            inner(p, el, wr, shape, skin, extra, t)
    B.gesture_hand = gesture_hand


# ------------------------------------------------------------------------------------------- secondary motion
def follow(t, keys, lag=0.12, freq=1.6, damping=3.0, gain=1.0):
    """Follow-through for things hanging off a moving body (lanyards, scarves, ponytails, ropes, a dangling sign).
    keys: [(time, body value)] (e.g. the head's sideways position or the body's lean); returns the hanging part's
    offset from the body: it lags behind each change, swings past and settles (a damped spring). Units as keys."""
    out = 0.0
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        jump = v1 - v0
        if t >= t1:
            u = t - t1 - lag
            if u >= 0:
                out += -jump * gain * math.exp(-damping * u) * math.cos(2 * math.pi * freq * u)
            else:
                out += -jump * gain
    return out


def idle_sway(t, phase=0.0, amp=2.0, period=3.5):
    """A gentle drift for anything hanging when the body is still (keeps a held pose alive)."""
    return amp * math.sin(2 * math.pi * (t / period + phase))


def dangle(p, top, length, angle, colr, width=5, tag=None):
    """A hanging strap or rope from top, swung by angle (radians, 0 = straight down), with an optional tag
    (badge, weight) at the end: tag = (w, h, fill)."""
    end = (top[0] + length * math.sin(angle), top[1] + length * math.cos(angle))
    mid = (top[0] + length * 0.5 * math.sin(angle * 0.6), top[1] + length * 0.5 * math.cos(angle * 0.6))
    p.line([top, mid, end], colr, width)
    if tag:
        w, h, fill = tag
        p.poly([(end[0] - w / 2, end[1]), (end[0] + w / 2, end[1]), (end[0] + w / 2, end[1] + h), (end[0] - w / 2, end[1] + h)],
               fill, INK, 1.8)
    return end


# ------------------------------------------------------------------------------------------- the test sheet
def sheet(out):
    import burnham as B
    import figure as F
    from PIL import ImageFont
    install(B)
    B.SS = 1
    F.guard(B)
    base = dict(skin=B.PALE, hw=68, hh=90, jaw='square', hair='crop', hair_c=(80, 60, 44), outfit='jumper',
                jacket=(52, 78, 132), trousers=(40, 44, 60), shoulders=146, bottom=560, pose='custom', full=True)
    rig = F.Rig(base, name='test')
    shapes = ['relaxed', 'flat', 'cup', 'phone', 'pen', 'wave', 'thumbs', 'grip']
    tw, th = 300, 314
    img = Image.new('RGB', (tw * 4, th * 2 + 260), (240, 238, 232))
    f = ImageFont.truetype(B.SANS, 20)
    for i, s in enumerate(shapes):
        target, bend = {'relaxed': ((150, 440), 'depth'), 'flat': ((150, 440), 'depth'), 'grip': ((150, 430), 'depth'),
                        'wave': ((300, -40), 'out')}.get(s, ((250, 200), 'out'))
        if s in ('cup', 'phone', 'pen', 'thumbs'):
            arms = {'L': rig.pose('sides')['L'], 'R': rig.pose('hold', side='R', shape=s, lift=0.6)['R']}
        else:
            arms = {'L': rig.pose('sides')['L'], 'R': rig.arm('R', target, s, bend)}
        c = B.canvas((246, 244, 240))
        cam = B.Cam(1.0, 540, 960)
        feet_shadow(c, cam, 540, 700, 0.5)
        B.person(c, cam, 540, 700, 0.5, dict(base, arms=arms), 0.0)
        tile = c.convert('RGB').crop((350, 560, 770, 1000)).resize((tw, th))
        img.paste(tile, ((i % 4) * tw, (i // 4) * th))
        ImageDraw.Draw(img).text(((i % 4) * tw + 8, (i // 4) * th + 6), s, font=f, fill=(20, 20, 20))
    # a lanyard following a head that jumps sideways at t = 0.2 s, drawn every 0.1 s
    d = ImageDraw.Draw(img)
    d.text((10, th * 2 + 10), 'lanyard after a quick turn at 0.2 s (every 0.1 s): lags, swings past, settles',
           font=f, fill=(20, 20, 20))

    class Flat:
        s = 1.0

        def P(self, x, y):
            return (x, y)

        def S(self, v):
            return v
    pen = B.Pen(img, Flat())
    for k in range(12):
        t = k * 0.1
        body = 0.0 if t < 0.2 else 1.0
        swing = follow(t, [(0.0, 0.0), (0.2, 0.6)])
        x0 = 40 + k * 82
        pen.line([(x0 - 20 + 20 * body, th * 2 + 60), (x0 + 20 + 20 * body, th * 2 + 60)], (60, 60, 70), 6)
        dangle(pen, (x0 + 20 * body, th * 2 + 60), 120, swing, (40, 90, 160), 4, tag=(30, 36, (248, 248, 248)))
    img.save(out)


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
