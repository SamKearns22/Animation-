#!/usr/bin/env python3
"""MAP  MidTerminal's moving parts (5 Nov), built on midterminal_set + midterminal_cast; the film file uses these.

    door_item(t_open)          the east door (wall angle 112) swung open by `t_open` (0 shut .. 1 wide), the corridor
                               behind it; a people-list item for set.render (sorted with everyone else)
    DOOR_SLAM                  the slam's curve: shut fast, a small bounce
    trump_path(d)              where Trump is and which way he faces after walking `d` metres from the corridor
    trump_item(t, d, sp)       Trump walking (moves.gait 'brisk'); clipped to the doorway while he's behind the wall
    satan_item(t, sp)          Satan floating: a slow bob and a slow wing beat
    epstein_item(t, sp, fade, melt)   the hellfire ghost: fades in/out (0..1), a flame tail below the waist, his face
                               melting into a flaming skull (melt 0..1)
    flames(...)                flat flame tongues (dark red edge, orange, yellow heart; no glow)

    python3 source/midterminal_moves.py sheet OUT.jpg      each move at a few moments
    python3 source/midterminal_moves.py reel OUT.mp4       a short test reel (small)

Map: door 40 | walk 110 | float 160 | flames 175 | ghost and skull 215 | sheet, reel 320
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B                  # noqa: E402
import midterminal_set as MS         # noqa: E402
import midterminal_cast as MC        # noqa: E402
import moves                         # noqa: E402
import views as V                    # noqa: E402
from ed import INK                   # noqa: E402
from satire_style import install_circle_hands   # noqa: E402

install_circle_hands(B)


def _install_point_finger():
    """Power Crime Action's 'point' hand (as patriots4.install_point_finger): the plain circle with one round-ended
    finger out along the forearm."""
    circle = B.gesture_hand
    if getattr(circle, 'point_finger', False):
        return

    def gesture_hand(p, el, wr, shape, skin, extra=None, t=0.0):
        if shape == 'point':
            dx, dy = wr[0] - el[0], wr[1] - el[1]
            n = math.hypot(dx, dy) or 1.0
            ux, uy = dx / n, dy / n
            cx, cy = wr[0] + ux * 12, wr[1] + uy * 12
            tip = (cx + ux * 62, cy + uy * 62)
            w = 10.5
            p.poly([(cx - uy * w, cy + ux * w), (tip[0] - uy * w, tip[1] + ux * w), (tip[0] + uy * w, tip[1] - ux * w),
                    (cx + uy * w, cy - ux * w)], skin, INK, 2.2)
            p.ell(tip[0], tip[1], w, w, skin, INK, 2.2)
        return circle(p, el, wr, shape, skin, extra, t)
    gesture_hand.point_finger = True
    B.gesture_hand = gesture_hand


_install_point_finger()

DOOR_A, DOOR_H = 112.0, 4.7          # the door's wall angle and half-width (degrees), as midterminal_set.door
DOOR_T = 0.05                        # the leaf's thickness (m)
DOOR_W = 0.7                         # the opening (and our leaf) reaches this much further each side, to the frame's edge
CORRIDOR = (236, 226, 204)           # the West Wing corridor seen through the door: cream walls, a red runner
RUNNER = (150, 44, 40)


# ---------------------------------------------------------------------------------------------- door
def _rot_out(p, hinge, ang):
    """Point p (on the closed leaf) turned `ang` degrees about the vertical through the hinge, into the room."""
    x, y, z = p
    hx, _, hz = hinge
    dx, dz = x - hx, z - hz
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    # which way is 'into the room': towards the centre (0, 0)
    nx, nz = -hx, -hz
    sg = -1 if (dx * nz - dz * nx) < 0 else 1
    s *= sg
    return (hx + dx * c - dz * s, y, hz + dx * s + dz * c)


def door_open(img, cm, t_open, part='both', flash=0):
    """The doorway (the corridor behind, filling the opening to the frame on both sides) and the leaf swung `t_open`
    (0..1 = 0..100 degrees) INTO the room about its hinge (north side: on the left seen from inside; Sam, 4 Nov); the
    knob on the free edge. The leaf is drawn even when shut, over the set's own door, so someone behind it stays
    hidden until it opens (Sam, 4 Nov)."""
    c, h = DOOR_A, DOOR_H + DOOR_W
    if part in ('hole', 'both'):
        if t_open > 0.001:
            corridor(img, cm, flash)
    if part == 'hole':
        return
    ang = 100.0 * max(0.0, t_open)
    hinge = MS.wp(c - h, 0.0, 0.015)
    corners = ((c - h, 0.0), (c + h, 0.0), (c + h, 2.45), (c - h, 2.45))
    leaf = [_rot_out(MS.wp(a, y, 0.015), hinge, ang) for a, y in corners]
    back = [_rot_out(MS.wp(a, y, 0.015 + DOOR_T), hinge, ang) for a, y in corners]
    if ang > 1.0:                                 # a real door's thickness (Sam, 4 Nov: paper thin side on): the
        MS.poly(img, cm, back, (228, 226, 216), None, 0)      # fills only: no outline inside the thickness
        MS.poly(img, cm, [leaf[1], back[1], back[2], leaf[2]], (214, 210, 198), None, 0)    # (Sam, 4 Nov: a line
        MS.poly(img, cm, [leaf[2], back[2], back[3], leaf[3]], (214, 210, 198), None, 0)    # showed through)
        MS.lines(img, cm, [back[2], back[1]], INK, 2.0)                  # the outer outline only
    MS.poly(img, cm, leaf, (240, 238, 230), None, 0)
    MS.lines(img, cm, [leaf[3], leaf[0], leaf[1], leaf[2], leaf[3]], INK, 2.0)
    if ang > 1.0:                                 # the cap of the thick side at the top and foot (Sam, 4 Nov: it had lost its line)
        MS.lines(img, cm, [leaf[2], back[2]], INK, 2.0)
        MS.lines(img, cm, [leaf[1], back[1]], INK, 2.0)     # the leaf's whole outline, top edge too
    for y0, y1 in ((0.15, 0.9), (1.05, 1.55), (1.7, 2.3)):                      # the six panels
        for a0, a1 in ((c - h + 0.7, c - 0.5), (c + 0.5, c + h - 0.7)):
            MS.poly(img, cm, [_rot_out(MS.wp(a, y, 0.02), hinge, ang) for a, y in ((a0, y0), (a1, y0), (a1, y1), (a0, y1))],
                    None, MS.dk(MS.WHITE, 0.8), 1.4)
    k = _rot_out(MS.wp(c + h - 1.0, 1.0, 0.04), hinge, ang)
    MS.poly(img, cm, [(k[0] + 0.04 * math.cos(u), k[1] + 0.04 * math.sin(u), k[2]) for u in np.linspace(0, 6.28, 10)],
            MS.GOLD, INK, 1.2)


CW, CD, CH = 1.25, 7.5, 2.9          # the corridor: half its width, how deep we see, its height (m)


def _cor(s, d, y):
    """A point in the corridor: s metres sideways (along the wall, + = towards larger wall angles), d metres out from
    the doorway, y up."""
    o = MS.wp(DOOR_A, 0.0, 0.0)
    n = MS.wp(DOOR_A, 0.0, -1.0)
    nx, nz = n[0] - o[0], n[2] - o[2]
    tx, tz = -nz, nx                              # along the wall
    a = MS.wp(DOOR_A + 1.0, 0.0, 0.0)
    if (a[0] - o[0]) * tx + (a[2] - o[2]) * tz < 0:
        tx, tz = -tx, -tz
    return (o[0] + nx * d + tx * s, y, o[2] + nz * d + tz * s)


def corridor(img, cm, flash=0):
    """The West Wing corridor through the doorway, a real space in depth (Sam's note 31): side walls with a white dado
    and gold sconces, a ceiling with hanging lights, a wooden floor with the red runner running away, a door at the
    far end; clipped to the doorway. `flash` (0..1): a press camera flash from the left side (off-screen) this frame."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    P = lambda pts, fill, lw=1.8, line=INK: MS.poly(lay, cm, [_cor(*q) for q in pts], fill, line, lw)  # noqa: E731
    wall, side = CORRIDOR, MS.dk(CORRIDOR, 0.9)
    P([(-CW, 0, 0), (CW, 0, 0), (CW, CD, 0), (-CW, CD, 0)], (150, 112, 74))                        # floor boards
    for k in range(1, 6):
        MS.lines(lay, cm, [_cor(-CW, CD * k / 6, 0), _cor(CW, CD * k / 6, 0)], (120, 88, 58), 1.0)
    P([(-0.6, -0.5, 0.002), (0.6, -0.5, 0.002), (0.6, CD, 0.002), (-0.6, CD, 0.002)], RUNNER, 1.4)     # the runner
    for sg in (-1, 1):
        P([(0.6 * sg, -0.5, 0.004), (0.53 * sg, -0.5, 0.004), (0.53 * sg, CD, 0.004), (0.6 * sg, CD, 0.004)],
          MS.GOLD, 0, None)            # its gold edges
    P([(-CW, CD, 0), (CW, CD, 0), (CW, CD, CH), (-CW, CD, CH)], wall)                                 # the far end
    P([(-0.5, CD, 0), (0.5, CD, 0), (0.5, CD, 2.2), (-0.5, CD, 2.2)], MS.WHITE, 1.6)                  # its white door
    P([(-0.12, CD, 2.3), (0.12, CD, 2.3), (0.0, CD, 2.55)], MS.WHITE, 1.2)
    for sg in (-1, 1):                                                                                # side walls
        P([(sg * CW, -0.5, 0), (sg * CW, CD, 0), (sg * CW, CD, CH), (sg * CW, -0.5, CH)], side)
        P([(sg * CW, -0.5, 0), (sg * CW, CD, 0), (sg * CW, CD, 0.95), (sg * CW, -0.5, 0.95)], MS.WHITE, 1.4)  # dado
        P([(sg * CW, -0.5, 0.95), (sg * CW, CD, 0.95), (sg * CW, CD, 1.0), (sg * CW, -0.5, 1.0)], MS.dk(MS.WHITE, 0.88), 1.0)
        for d in (1.4, 4.0, 6.4):                                                                     # a framed picture
            P([(sg * CW * 0.995, d - 0.45, 1.35), (sg * CW * 0.995, d + 0.45, 1.35), (sg * CW * 0.995, d + 0.45, 2.0),
               (sg * CW * 0.995, d - 0.45, 2.0)], MS.GOLD, 1.4)
            P([(sg * CW * 0.99, d - 0.36, 1.43), (sg * CW * 0.99, d + 0.36, 1.43), (sg * CW * 0.99, d + 0.36, 1.92),
               (sg * CW * 0.99, d - 0.36, 1.92)], (120, 140, 120) if sg < 0 else (150, 120, 90), 1.0)
        for d in (2.7, 5.2):                                                                          # gold sconces
            MS.poly(lay, cm, [_cor(sg * CW * 0.98, d + 0.08 * math.cos(u), 1.75 + 0.1 * math.sin(u))
                              for u in np.linspace(0, 6.28, 10)], (255, 236, 170), INK, 1.2)
            MS.poly(lay, cm, [_cor(sg * CW * 0.98, d - 0.05, 1.55), _cor(sg * CW * 0.98, d + 0.05, 1.55),
                              _cor(sg * CW * 0.98, d + 0.03, 1.68), _cor(sg * CW * 0.98, d - 0.03, 1.68)], MS.GOLD, INK, 1.0)
    P([(-CW, -0.5, CH), (CW, -0.5, CH), (CW, CD, CH), (-CW, CD, CH)], MS.lt(CORRIDOR, 1.04))         # ceiling
    for d in (1.8, 4.6):                                                                              # hanging lights
        MS.lines(lay, cm, [_cor(0, d, CH), _cor(0, d, CH - 0.35)], INK, 1.2)
        MS.poly(lay, cm, [_cor(0.16 * math.cos(u), d, CH - 0.45 + 0.1 * math.sin(u)) for u in np.linspace(0, 6.28, 10)],
                (255, 240, 190), INK, 1.4)
    if flash > 0:                                                                                     # a camera flash
        box = opening_mask(img.size, cm).getbbox()            # just inside the doorway's left edge, head high
        sx, sy = box[0] / B.SS + 25, box[1] / B.SS + 0.45 * (box[3] - box[1]) / B.SS
        rng = np.random.default_rng(int(flash * 1000))
        wash = Image.new('RGBA', img.size, (255, 255, 255, int(110 * flash)))
        lay.alpha_composite(wash)
        d = ImageDraw.Draw(lay)
        pts = []
        for k in range(14):                       # a lumpy starburst (house style: no glow, flat shapes)
            r = (150 if k % 2 == 0 else 60) * rng.uniform(0.8, 1.2) * B.SS
            u = 2 * math.pi * k / 14 + rng.uniform(-0.1, 0.1)
            pts.append((sx * B.SS + r * math.cos(u), sy * B.SS + r * math.sin(u)))
        d.polygon(pts, fill=(255, 255, 236, 255), outline=INK + (255,), width=int(2 * B.SS))
    m = np.minimum(np.asarray(lay.getchannel('A')), np.asarray(opening_mask(img.size, cm)))
    lay.putalpha(Image.fromarray(m))
    img.alpha_composite(lay)


def door_items(t_open, flash=0):
    """Two people-list items: the doorway (sorted as far as the corridor, so someone in it draws over it) and the
    leaf (sorted at its middle, in the room)."""
    hx, _, hz = MS.wp(DOOR_A, 0.0, -2.0)
    lx, _, lz = MS.wp(DOOR_A, 0.0, 0.6)
    return [(hx, hz, lambda im, c: door_open(im, c, t_open, 'hole', flash)),
            (lx, lz, lambda im, c: door_open(im, c, t_open, 'leaf'))]


def door_curve(t, t0, t_wide, t_slam):
    """How far open at time t: swung open from t0 to t_wide (eased), held, slammed shut from t_slam in 0.25 s with
    one small bounce (Sam's door slam lands at t_slam + 0.25)."""
    if t < t0:
        return 0.0
    if t < t_wide:
        u = (t - t0) / (t_wide - t0)
        return 1 - (1 - u) ** 2
    if t < t_slam:
        return 1.0
    u = (t - t_slam) / 0.25
    if u < 1:
        return 1 - u * u
    u = (t - t_slam - 0.25) / 0.2
    return 0.06 * math.sin(math.pi * u) if u < 1 else 0.0


def opening_mask(img_size, cm):
    """The doorway's outline on screen (for clipping someone still behind the wall)."""
    m = Image.new('L', img_size, 0)
    pts = [cm.project(p)[0] for p in MS.band(DOOR_A - DOOR_H - DOOR_W, DOOR_A + DOOR_H + DOOR_W, -0.3, 2.45, 0.016, 1.0)]
    ImageDraw.Draw(m).polygon([(x * B.SS, y * B.SS) for x, y in pts], fill=255)
    return m


# ---------------------------------------------------------------------------------------------- walk
WALK_TO = (0.7, 1.0)                 # his mark (Sam, 4 Nov: Trump right, Satan middle, Epstein left)
SATAN_AT = (0.0, 1.45)            # forward of the desk, bigger in frame (Sam's note 33)
EPSTEIN_AT = (-1.8, 2.85)          # beside the desk, left; clear of Satan's wing (note 38)


ENTRY = [(1.9, 1.0), (1.35, 1.0), WALK_TO]  # shot 2: in from frame RIGHT to his mark, short: he stops early (note 32)


def _path_pts(pts=None):
    if pts is not None:
        return pts
    a = MS.wp(DOOR_A, 0.0, -0.9)     # in the corridor
    b = MS.wp(DOOR_A, 0.0, 1.35)     # straight in, past the open leaf (it swings in on his left)
    return [(a[0], a[2]), (b[0], b[2]), WALK_TO]


def path_length(pts=None):
    p = _path_pts(pts)
    return sum(math.dist(p[i], p[i + 1]) for i in range(len(p) - 1))


def trump_path(d, pts=None):
    """(x, z, facing) after walking d metres along corridor -> threshold -> his mark (or along `pts`); the
    facing turns smoothly."""
    p = _path_pts(pts)
    for i in range(len(p) - 1):
        L = math.dist(p[i], p[i + 1])
        if d <= L or i == len(p) - 2:
            u = max(0.0, min(1.0, d / L))
            x = p[i][0] + (p[i + 1][0] - p[i][0]) * u
            z = p[i][1] + (p[i + 1][1] - p[i][1]) * u
            f0 = math.degrees(math.atan2(p[1][0] - p[0][0], p[1][1] - p[0][1]))
            f1 = math.degrees(math.atan2(p[2][0] - p[1][0], p[2][1] - p[1][1]))
            if i == 0:
                k = max(0.0, (u - 0.6) / 0.4)
            else:
                k = 1.0
            return x, z, f0 + (((f1 - f0 + 180) % 360) - 180) * k * k * (3 - 2 * k)
        d -= L


def behind_wall(x, z):
    r = (x / MS.A) ** 2 + (z / MS.BZ) ** 2
    return r > 1.0


def point_at(j, c, x, z, target):
    """His right arm (our left, front on) thrust out at `target` (x, y, z in metres) through camera c: the screen
    direction to it, put into his own units, nearly straight, a finger out (Sam, 4 Nov: accusing as he walks in)."""
    (Xs, Ys), _ = c.project((x, 1.45, z))
    (Xt, Yt), _ = c.project(target)
    dx, dy = Xt - Xs, Yt - Ys
    n = math.hypot(dx, dy) or 1.0
    if abs(dx) < 90:                              # walking past in front of the target: arms down for that moment,
        return j                                  # then the other arm takes up the point
    side = 'L' if dx < 0 else 'R'                 # the arm on the target's side, never across the body
    sx, sy, sz = j['sh' + side]
    reach = (V.F.UPPER + V.F.FORE) * 0.95
    d = (dx / n * 0.85, dy / n * 0.85 + 0.05, 0.5)
    m = math.sqrt(sum(v * v for v in d))
    V.arm_to(j, side, (sx + d[0] / m * reach, sy + d[1] / m * reach, sz + d[2] / m * reach), 'down', 'point')
    return j


def _copy(j):
    return {k: (set(v) if isinstance(v, set) else dict(v) if isinstance(v, dict) else list(v) if isinstance(v, list)
                else v) for k, v in j.items()}


def trump_item(t, d, sp, facing=None, walking=True, front=False, point=None, pts=None, arms=None):
    """Trump d metres along his path at time t (walking: the brisk gait; else standing). `facing` overrides; `front`
    keeps him square to the lens all the way (Sam, 4 Nov); `point`: a world point he points at. Over the last 0.5 m
    he turns square to the lens anyway (rule 38: front on at his mark)."""
    x, z, f0 = trump_path(d, pts)
    left = path_length(pts) - d
    j = moves.gait(sp, t, 'brisk') if walking and left > 0.02 else V.standing(sp)

    def draw(im, c):
        f = f0
        jj = _copy(j)
        if facing is not None:
            f = facing
        elif front:
            f = MS.to_cam(c, x, z)
        elif left < 0.5:
            k = 1 - max(0.0, left) / 0.5
            k = k * k * (3 - 2 * k)
            f = f0 + (((MS.to_cam(c, x, z) - f0 + 180) % 360) - 180) * k
        if point is not None:
            point_at(jj, c, x, z, point)
        if arms is not None:                      # the film's own gesture over the walk (e.g. a palm to the press)
            jj = arms(jj, c, x, z)
        if behind_wall(x, z):
            lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
            MS.put(lay, c, sp, x, z, f, jj)
            lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay.getchannel('A')), np.asarray(opening_mask(im.size, c)))))
            im.alpha_composite(lay)
        else:
            MS.put(im, c, sp, x, z, f, jj)
    return (x, z, draw)


# ---------------------------------------------------------------------------------------------- float
def satan_float(t):
    """(lift in metres, wing spread): a slow bob (1.6 s) and a slow beat, the body rising as the wings press down."""
    beat = math.sin(2 * math.pi * t / 0.9)
    return 0.30 + 0.035 * math.sin(2 * math.pi * t / 1.6 + 0.6) - 0.012 * beat, 0.5 + 0.13 * beat


def satan_item(t, sp, x=SATAN_AT[0], z=SATAN_AT[1], facing=None):
    lift, spread = satan_float(t)

    def draw(im, c):
        f = MS.to_cam(c, x, z) if facing is None else facing
        MS.put(im, c, dict(sp, spread=spread), x, z, f, lift=lift)
    return (x, z, draw)


# ---------------------------------------------------------------------------------------------- flames
def flames(d, cx, base_y, width, height, t, seed, n=5, lw=3.0, bed=False):
    """Flat flame tongues on screen standing on a line (cx +- width/2 at base_y), flickering (a new shape every 2
    frames at 12 fps): dark red edge, orange, a yellow heart; one ink outline round each."""
    rng = np.random.default_rng(seed * 977 + int(t * 6))
    for layer, col, k in ((0, (176, 40, 24), 1.0), (1, (238, 120, 30), 0.72), (2, (252, 214, 80), 0.42)):
        for i in range(n):
            f = (i + 0.5) / n * 2 - 1
            r2 = np.random.default_rng(seed * 31 + i * 7 + int(t * 6))
            h = height * k * r2.uniform(0.55, 1.0) * (1.0 - 0.35 * abs(f))
            w = width / n * 1.25 * k
            x0 = cx + f * width / 2 * 0.85
            sway = r2.uniform(-0.25, 0.25) * w
            pts = [(x0 - w / 2, base_y), (x0 - w * 0.35 + sway * 0.3, base_y - h * 0.45),
                   (x0 + sway, base_y - h), (x0 + w * 0.35 + sway * 0.6, base_y - h * 0.4), (x0 + w / 2, base_y)]
            d.polygon(pts, fill=col + (255,), outline=INK + (255,) if layer == 0 else None,
                      width=int(lw) if layer == 0 else 0)
    if bed:                       # a bed of embers over the flames' foot (Sam, 4 Nov: no hard line where they end):
        r0 = width / n * 0.8      # glowing lumps of three sizes in a ragged heap, and a few sparks drifting up
        N = int(n * 3)
        for i in range(N):        # spread evenly along the whole foot (with a jitter), so no stretch of edge shows
            r2 = np.random.default_rng(seed * 53 + i)
            ex = cx + ((((i * 7) % N) + 0.5) / N - 0.5) * width * 1.02 + r2.uniform(-0.3, 0.3) * r0
            ey = base_y + r2.uniform(-0.45, 0.35) * r0
            r = r0 * r2.uniform(0.6, 1.0) * (1 - 0.35 * abs(ex - cx) / width * 2)
            col = ((150, 34, 22), (204, 70, 28), (238, 120, 30))[i % 3]
            d.ellipse((ex - r, ey - r * 0.75, ex + r, ey + r * 0.75), fill=col + (255,), outline=INK + (255,), width=int(lw))
            if i % 3 == 2:
                d.ellipse((ex - r * 0.4, ey - r * 0.3, ex + r * 0.4, ey + r * 0.3), fill=(252, 214, 80, 255))
        for i in range(6):        # sparks: small, rising and fading out of the frame, each on its own cycle
            r2 = np.random.default_rng(seed * 71 + i)
            ph = (t * 0.9 + r2.uniform()) % 1.0
            sx = cx + r2.uniform(-0.5, 0.5) * width + math.sin(ph * 6 + i) * r0 * 0.6
            sy = base_y - ph * abs(height) * 1.2
            rs = r0 * 0.16 * (1 - ph)
            if rs > 0.8:
                d.ellipse((sx - rs, sy - rs, sx + rs, sy + rs), fill=(252, 190, 60, 255), outline=INK + (255,), width=1)
    del rng


# ---------------------------------------------------------------------------------------------- ghost and skull
def _neck_screen(cm, sp, x, z, lift):
    f = sp.get('height', 1.75) / 1.75
    (Xn, Yn), _ = cm.project((x, 928 * V.M_PER_UNIT * f + lift, z))
    (Xf, Yf), _ = cm.project((x, lift, z))
    return Xf * B.SS, (Yf - (Yf - Yn)) * B.SS, (Yf - Yn) / 928.0 * B.SS


def skull(size, t, seed=3, lw=2.4):
    """The flaming skull, in the house style (Sam, 4 Nov, ref: a full, rounded real skull wreathed in fire): flat
    tones, the characters' line weight, no extra detail. A big round cranium; full cheekbones flush with it (no caving
    round the mouth); the jaw dropped open in a scream, as wide as the cheeks; the mouth and the deep sockets lit by
    fire inside; an upside-down-heart nose; one shade tone down the side; a crack; flames over the crown."""
    S = int(size)
    im = Image.new('RGBA', (S, int(S * 2.3)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    oy = int(S * 0.78)                                    # the top of the cranium; flames above
    lw = max(1, int(round(lw)))
    flames(d, S / 2, oy + S * 0.4, S * 1.05, S * 1.0, t, seed, n=7, lw=lw)
    bone, shade = (236, 226, 202), (206, 190, 160)        # like the characters' skin: one flat tone, one shade
    sock, fire, core = (74, 30, 22), (238, 120, 30), (252, 214, 80)

    def P(pts):
        return [(S * x, oy + S * y) for x, y in pts]
    jaw = P([(0.17, 0.80), (0.19, 1.18), (0.29, 1.42), (0.50, 1.50), (0.71, 1.42), (0.81, 1.18), (0.83, 0.80)])
    d.polygon(jaw, fill=bone, outline=INK, width=lw)                       # the jaw, dropped (behind the face)
    d.polygon(P([(0.27, 1.02), (0.73, 1.02), (0.71, 1.32), (0.5, 1.38), (0.29, 1.32)]), fill=fire)   # mouth: fire
    d.polygon(P([(0.38, 1.06), (0.62, 1.06), (0.59, 1.24), (0.5, 1.30), (0.41, 1.24)]), fill=core)
    for i in range(6):                                                     # lower teeth, a full row
        x0 = 0.29 + i * 0.07
        d.rounded_rectangle((S * x0, oy + S * 1.29, S * (x0 + 0.065), oy + S * 1.38), int(S * 0.015),
                            fill=bone, outline=INK, width=max(1, lw - 1))
    face = [(0.5 + 0.43 * math.cos(u), 0.45 - 0.45 * math.sin(u)) for u in np.linspace(math.pi, 0, 24)]
    face += [(0.92, 0.62), (0.88, 0.80), (0.78, 0.92), (0.74, 1.04), (0.26, 1.04), (0.22, 0.92), (0.12, 0.80),
             (0.08, 0.62)]                                                 # cranium into broad cheekbones and a full upper jaw
    d.polygon(P(face), fill=bone, outline=INK, width=lw)
    d.polygon(P([(0.09, 0.45), (0.16, 0.28), (0.15, 0.62), (0.22, 0.86), (0.14, 0.80), (0.10, 0.62)]), fill=shade)
    for i in range(6):                                                     # upper teeth, a full row
        x0 = 0.29 + i * 0.07
        d.rounded_rectangle((S * x0, oy + S * 0.95, S * (x0 + 0.065), oy + S * 1.05), int(S * 0.015),
                            fill=bone, outline=INK, width=max(1, lw - 1))
    for sgn in (-1, 1):                                                    # sockets: big, round, a little slanted
        cx = 0.5 + sgn * 0.185
        pts = [(cx + 0.13 * math.cos(u), 0.56 + 0.105 * math.sin(u) - sgn * 0.025 * math.cos(u))
               for u in np.linspace(0, 2 * math.pi, 18)]
        d.polygon(P(pts), fill=sock, outline=INK, width=lw)
        fl = 0.03 * math.sin(t * 9 + sgn)                                  # fire flickering inside
        d.polygon(P([(cx - 0.06, 0.62), (cx - 0.02, 0.53 + fl), (cx + 0.01, 0.58), (cx + 0.04, 0.50 - fl), (cx + 0.07, 0.62)]),
                  fill=fire)
    d.polygon(P([(0.5, 0.70), (0.455, 0.80), (0.47, 0.85), (0.5, 0.83), (0.53, 0.85), (0.545, 0.80)]),
              fill=sock, outline=INK, width=max(1, lw - 1))                # the nose
    d.line(P([(0.60, 0.02), (0.63, 0.12), (0.59, 0.20), (0.64, 0.28)]), fill=INK, width=max(1, lw - 1))   # a crack
    return im


def _melt(layer, box, k, seed=5):
    """Drip the picture inside box (x0, y0, x1, y1) downward: each column slides by its own amount, up to k * box
    height, and the top fades. Flat: no blur."""
    x0, y0, x1, y1 = [int(v) for v in box]
    a = np.asarray(layer).copy()
    H, W = a.shape[:2]
    x0, x1 = max(0, x0), min(W, x1)
    y0, y1 = max(0, y0), min(H, y1)
    if x1 <= x0 or y1 <= y0:
        return layer
    rng = np.random.default_rng(seed)
    n = x1 - x0
    knots = rng.uniform(0.3, 1.0, max(3, n // 18))
    drop = np.interp(np.arange(n), np.linspace(0, n - 1, len(knots)), knots) * k * (y1 - y0) * 0.9
    src = a[y0:H, x0:x1].copy()
    out = a[y0:H, x0:x1]
    out[:] = 0
    hh = src.shape[0]
    for i in range(n):
        dpx = int(drop[i])
        if dpx >= hh:
            continue
        col = src[:hh - dpx, i]
        out[dpx:, i] = np.where(col[..., 3:4] > 0, col, out[dpx:, i])
        out[:dpx, i] = src[:dpx, i] * 0                      # the head runs down, leaving the top empty
    a[:y0] = a[:y0]
    return Image.fromarray(a, 'RGBA')


BONE, BONE_D = (236, 226, 202), (206, 190, 160)
GHOST_ALPHA = 0.9                    # Sam's note 39: half again as solid as before (0.72), still a little see-through


def _frame_of(c, sp, x, z, facing, lift):
    """The person's own drawing frame on the full-size canvas (as MS.put places them): a burnham Local and the drawn
    view, so bones can be drawn on the same joints as the body."""
    f = sp.get('height', 1.75) / 1.75
    neck = 928 * V.M_PER_UNIT * f + lift
    (Xn, Yn), _ = c.project((x, neck, z))
    (Xf, Yf), _ = c.project((x, lift, z))
    s = max(1e-3, (Yf - Yn) / 928.0)
    fd = (math.sin(math.radians(facing)), math.cos(math.radians(facing)))
    view_deg, mirror = V.snap(c.yaw_of((x, 0, z), fd))
    return B.Local(MS.FLAT, Xf, Yf - 928 * s, s, -1 if mirror else 1), view_deg


def _bone(p, a, b, w):
    p.line([a, b], INK, w + 4.4)
    p.line([a, b], BONE, w)
    for q in (a, b):                                  # knobbly ends
        p.ell(q[0], q[1], w * 0.62, w * 0.62, BONE, INK, 2.0)


def skeleton(img, L, view_deg, j, t, burn=1.0):
    """A burning skeleton in the house style (Sam's note 41, standard anatomy, no reference): collarbones, a spine,
    a ribcage, the pelvis top, and both arms (upper arm, two forearm bones, a plain round bone hand), on his joints;
    small flames licking over it. Drawn in his own frame (neck base 0, 0)."""
    p = B.Pen(img, L)
    P = {k: V.project(V.leaned(j[k], j.get('lean', 0.0)), view_deg)[0] for k in ('shL', 'shR', 'elL', 'elR', 'wrL', 'wrR')}
    for y in range(20, 430, 34):                      # the spine: a column of vertebrae
        p.poly([(-11, y), (11, y), (9, y + 26), (-9, y + 26)], BONE, INK, 2.0)
    for k in range(6):                                # ribs: arcs either side from the spine round to the front
        y = 70 + 30 * k
        w = 92 - 6 * k
        for sg in (-1, 1):
            p.line([(sg * 10, y), (sg * w * 0.7, y - 10), (sg * w, y + 12), (sg * w * 0.85, y + 40)], INK, 13.0)
            p.line([(sg * 10, y), (sg * w * 0.7, y - 10), (sg * w, y + 12), (sg * w * 0.85, y + 40)], BONE, 8.0)
    p.poly([(-8, 62), (8, 62), (6, 200), (-6, 200)], BONE_D, INK, 1.8)            # the breastbone
    for sg in (-1, 1):                                # the pelvis top: two wings of bone
        p.poly([(sg * 12, 400), (sg * 96, 380), (sg * 112, 430), (sg * 70, 470), (sg * 14, 460)], BONE, INK, 2.2)
    for sd in 'LR':
        sh, el, wr = P['sh' + sd], P['el' + sd], P['wr' + sd]
        _bone(p, (0, 4), sh, 10)                      # collarbone
        _bone(p, sh, el, 15)                          # upper arm
        n = (wr[1] - el[1], el[0] - wr[0])
        m = math.hypot(*n) or 1.0
        for sg in (-1, 1):                            # two forearm bones
            o = (sg * n[0] / m * 5, sg * n[1] / m * 5)
            _bone(p, (el[0] + o[0], el[1] + o[1]), (wr[0] + o[0], wr[1] + o[1]), 7)
        d = (wr[0] - el[0], wr[1] - el[1])
        k = math.hypot(*d) or 1.0
        p.ell(wr[0] + d[0] / k * 14, wr[1] + d[1] / k * 14, 22, 22, BONE, INK, 2.4)   # the hand: a plain bone circle
    if burn > 0:                                      # flames licking over the bones
        d = ImageDraw.Draw(img)
        for i, (bx, by) in enumerate([(0, 120), (-60, 220), (60, 260), P['elL'], P['elR'], P['shL'], P['shR']]):
            if (i + int(t * 3)) % 3 == 0:
                continue
            X, Y = L.P(bx, by)
            flames(d, X, Y + 20 * L.s * B.SS, 70 * L.s * B.SS, 120 * burn * L.s * B.SS, t, 40 + i, n=3,
                   lw=2.0 * B.SS)


def body_flames(d, nx, ny, s, t):
    """Sam's note 39: now and then a small flame flickers up on his body (two at a time, each lasting 0.5 s)."""
    spots = [(-100, 60), (110, 70), (-40, 220), (60, 300), (-70, 360), (20, 140), (90, 200)]
    slot = int(t / 0.5)
    for k in range(2):
        r = np.random.default_rng(slot * 7 + k)
        if r.random() < 0.35:                         # some slots stay quiet: "occasional"
            continue
        bx, by = spots[int(r.integers(len(spots)))]
        flames(d, nx + bx * s, ny + by * s, 60 * s, 110 * s, t, 60 + slot * 2 + k, n=3, lw=2.0 * B.SS)


def entrance(over, nx, ny, s, age, seed=21):
    """Sam's note 38: he arrives in a burst of flames and light smoke: flames roar up the height of a man and die back
    over 0.9 s; pale smoke clumps (each its own outline, house style) rise and shrink away over 1.1 s."""
    d = ImageDraw.Draw(over)
    if 0 <= age < 0.9:
        h = 1.0 - ((age - 0.18) / 0.72) ** 2 if age > 0.18 else age / 0.18
        flames(d, nx, ny + 820 * s, 760 * s, 1500 * s * max(0.0, h), age, seed, n=9, lw=2.6 * B.SS)
    for i in range(9):
        r = np.random.default_rng(seed * 13 + i)
        t0 = r.uniform(0.0, 0.35)
        u = (age - t0) / 1.1
        if not 0 <= u <= 1:
            continue
        cx = nx + r.uniform(-300, 300) * s + r.uniform(-60, 60) * s * u
        cy = ny + r.uniform(250, 700) * s - 650 * s * u
        rad = (90 + 130 * min(1.0, u * 3)) * s * (1 - max(0.0, (u - 0.7) / 0.3))   # grows, then shrinks away
        if rad < 2:
            continue
        pts = []
        for k in range(10):
            a = 2 * math.pi * k / 10
            rr = rad * (1 + 0.18 * math.sin(3 * a + i))
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, fill=(214, 210, 206, 150), outline=INK + (150,), width=int(2 * B.SS))


def epstein_item(t, sp, fade=1.0, melt=0.0, x=EPSTEIN_AT[0], z=EPSTEIN_AT[1], facing=None, look=0.8, j=None,
                 arrive=None):
    """The hellfire ghost of Epstein, floating with a slow bob; below the waist his body gives way to a flame tail;
    now and then a flame on his body. fade 0..1 (see-through to there), melt 0..1 (his face runs down to a flaming
    skull, then the melt spreads over his shoulders, arms and body to a burning skeleton). arrive: seconds since the
    burst he arrives in (None = no burst)."""
    lift = 0.5 + 0.03 * math.sin(2 * math.pi * t / 1.4)   # high enough to float over the chair (note 38)

    def draw(im, c):
        f = MS.to_cam(c, x, z) if facing is None else facing
        nx, ny, s = _neck_screen(c, sp, x, z, lift)
        over = Image.new('RGBA', im.size, (0, 0, 0, 0))     # drawn flat over the ghost, not tinted (house style)
        burst = Image.new('RGBA', im.size, (0, 0, 0, 0))    # the arrival burst: never faded with him
        if arrive is not None and 0 <= arrive < 2.0:
            entrance(burst, nx, ny, s, arrive)
        if fade <= 0.01:
            im.alpha_composite(burst)
            return
        jj = j if j is not None else V.standing(sp)
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
        MS.put(lay, c, dict(sp, look=look), x, z, f, j, lift=lift)
        probe = lay                                       # the head is measured with his arms DOWN: raised arms (the
        if j is not None and melt > 0:                    # silly-ghost wave) widened the box to arm's reach and the
            probe = Image.new('RGBA', im.size, (0, 0, 0, 0))   # skull grew to his whole body (Sam, 4 Nov)
            MS.put(probe, c, dict(sp, look=look), x, z, f, lift=lift)
        # the tail: the body fades out from the hips down, flames take its place
        a = np.asarray(lay).copy()
        hip, knee = int(ny + 450 * s), int(ny + 680 * s)
        if hip < a.shape[0]:
            ramp = np.clip((np.arange(a.shape[0]) - hip) / max(1, knee - hip), 0, 1)
            a[..., 3] = (a[..., 3] * (1 - ramp[:, None])).astype(np.uint8)
        lay = Image.fromarray(a, 'RGBA')
        dov = ImageDraw.Draw(over)
        # the tail: flames roaring UP from below the knees to his waist (Sam, 4 Nov), where his legs fade away
        flames(dov, nx, ny + 790 * s, 430 * s, 600 * s, t, 11, n=6, lw=2.4 * B.SS, bed=True)
        body = 0.0
        if melt > 0:
            al = np.asarray(probe.getchannel('A'))
            rows = np.where(al[:int(ny)].max(axis=1) > 0)[0] if ny > 0 else []
            top = rows[0] if len(rows) else ny - 200 * s
            cols = np.where(al[int(top):int(ny)].max(axis=0) > 0)[0]
            hx0, hx1 = (cols[0], cols[-1]) if len(cols) else (nx - 80 * s, nx + 80 * s)
            hw = hx1 - hx0
            sk = skull(hw * (0.85 + 0.15 * min(1.0, melt * 1.4)), t, lw=2.4 * B.SS)   # his own head's size (Sam, 4 Nov)
            sk.putalpha(sk.getchannel('A').point(lambda v: int(v * min(1.0, max(0.0, melt - 0.15) * 2.2))))
            head_y = (top + ny) / 2
            under = Image.new('RGBA', im.size, (0, 0, 0, 0))      # under the skin: the bones the melt uncovers
            body = min(1.0, max(0.0, (melt - 0.35) / 0.5))       # note 41: the melt spreads down his body
            if body > 0:
                L, vd = _frame_of(c, sp, x, z, f, lift)
                bones = Image.new('RGBA', im.size, (0, 0, 0, 0))
                skeleton(bones, L, vd, jj, t, burn=body)
                bones.putalpha(bones.getchannel('A').point(lambda v: int(v * min(1.0, body * 1.6))))
                under.alpha_composite(bones)
            under.alpha_composite(sk, (int((hx0 + hx1) / 2 - sk.width / 2), int(head_y - sk.width * 1.25)))
            # note 41: as ghostly as he is (the skull was full strength under him)
            under.putalpha(under.getchannel('A').point(lambda v: int(v * fade * GHOST_ALPHA)))
            im.alpha_composite(under)
            lay = _melt(lay, (hx0 - 4, top, hx1 + 4, ny + 40 * s), melt)
            if body > 0:                                          # shoulders, arms, body run down after the face
                bb = np.where(np.asarray(lay.getchannel('A')) > 0)
                if len(bb[0]):
                    lay = _melt(lay, (bb[1].min() - 4, bb[0].min(), bb[1].max() + 4, ny + 470 * s), body, seed=9)   # hands too
        if melt > 0:                                  # what runs down never shows below his flame tail
            a = np.asarray(lay).copy()
            if hip < a.shape[0]:
                a[..., 3] = (a[..., 3] * (1 - ramp[:, None])).astype(np.uint8)
            lay = Image.fromarray(a, 'RGBA')
        if body < 0.5:
            body_flames(dov, nx, ny, s, t)
        MS.ghost(im, lambda L: L.alpha_composite(lay), alpha=GHOST_ALPHA * fade, own=0.65)
        if fade < 1:
            over.putalpha(over.getchannel('A').point(lambda v: int(v * fade)))
        im.alpha_composite(over)
        im.alpha_composite(burst)
    return (x, z, draw)


# ---------------------------------------------------------------------------------------------- sheet, reel
SHOT_CAMS = {name: (pos, look, focal) for name, (_, (pos, look, focal), _w) in
             zip(('door', 'two', 'three', 'epstein'), MS.COMP)}


def frame(t, cam_name, door_t=None, walk_d=None, ep_fade=0.0, ep_melt=0.0):
    pos, look, focal = SHOT_CAMS[cam_name]
    cm = MS.S.Cam(pos, look, focal=focal)
    ppl = []
    if door_t is not None:
        ppl += door_items(door_t)
    if walk_d is not None:
        if cam_name == 'door':
            ppl.append(trump_item(t, walk_d, dict(MC.TRUMP, look=0.9 if walk_d < 1.2 else 0.0)))
        else:
            sx, sz = SATAN_AT
            ppl.append(trump_item(t, walk_d, dict(MC.TRUMP, look=-0.8, frown=0.03), front=True,
                                  point=(sx, 1.45 + satan_float(t)[0], sz), pts=ENTRY))
    if cam_name != 'door':
        ppl.append(satan_item(t, MC.SATAN))
    if ep_fade > 0:
        ppl.append(epstein_item(t, MC.EPSTEIN, ep_fade, ep_melt))
    img = Image.new('RGBA', (1080 * B.SS, 1920 * B.SS), (0, 0, 0, 255))
    MS.render(img, cm, ppl)
    return img


SLAM = 1.3                           # the door starts to slam; shut at SLAM + 0.25, and the cut to shot 2 comes there,
CUT = SLAM + 0.25                    # with "Satan, what the f***?" starting on the cut (Sam, 4 Nov note 2)


def test_timeline(t):
    """The test reel: the door and walk-in (0-1.55 s, Trump starting just behind the door), the cut on the slam to
    Trump striding in from frame left, pointing at Satan (1.55-4.4), the ghost fading in and melting (4.4-8.4)."""
    if t < CUT:
        return frame(t, "door", door_t=door_curve(t, 0.1, 0.45, SLAM), walk_d=0.6 + 1.35 * t)
    if t < 4.4:
        return frame(t, 'two', walk_d=min(path_length(ENTRY), 1.35 * (t - CUT)))
    fade = min(1.0, (t - 4.4) / 0.8) if t < 7.6 else max(0.0, 1 - (t - 7.6) / 0.8)
    return frame(t, 'epstein', ep_fade=fade, ep_melt=max(0.0, min(1.0, (t - 5.8) / 1.4)))


def sheet(out):
    B.SS = 1
    times = [0.05, 0.5, 1.2, 1.5, 2.2, 3.6, 4.8, 6.2, 6.9, 7.4]
    tiles = [(t, test_timeline(t)) for t in times]
    w, h = 324, 576
    sh = Image.new('RGB', (5 * w + 6 * 12, 2 * (h + 40) + 12), (232, 228, 222))
    d = ImageDraw.Draw(sh)
    f = ImageFont.truetype(MS.FONT, 20)
    for i, (t, im) in enumerate(tiles):
        x, y = 12 + (i % 5) * (w + 12), 6 + (i // 5) * (h + 40)
        d.text((x, y), f'{t:.1f} s', font=f, fill=(30, 30, 30))
        sh.paste(im.convert('RGB').resize((w, h), Image.LANCZOS), (x, y + 30))
    sh.save(out, quality=86)
    return out


def reel(out, fps=12, dur=8.4):
    B.SS = 1
    tmp = out + '.frames'
    os.makedirs(tmp, exist_ok=True)
    for i in range(int(dur * fps)):
        test_timeline(i / fps).convert('RGB').resize((540, 960), Image.LANCZOS).save(f'{tmp}/{i:04d}.png')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', f'{tmp}/%04d.png',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '26', out], check=True)
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    elif sys.argv[1] == 'reel':
        print(reel(sys.argv[2]))
