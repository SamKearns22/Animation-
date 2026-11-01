#!/usr/bin/env python3
"""Flying Whales, the rig scene's whale paths (rule 1: planned in metres before anything moves; 1 Nov).

Times are the rig scene's own clock (0 = the hard cut, film time 5.6 s). World: whale.py's axes (x right, y away from
the camera, z up, m), the camera locked at (0, -120, 8) (flying_whales_sea.CAM). The rig's near right corner is at
(14, 0); its long front face runs back to the left (flying_whales_rig: P(a, b, z)).

The beats (notes/flying-whales.md, Showstoppers 4-8, 13, 17):
- 0.0-0.7  the five burst out of the sea in the foreground, 55-70 m from the lens, one after another, nose up about 40
           degrees and heading away and to the right: up and to the right on screen, as they left the opener (rule 16);
- 0.7-2.3  they climb and fan out towards the rig, speeding up all the way (they never slow; Sam: "if anything, they
           speed up"); the rig is seen whole for about 1.5 s before the first hit (rule 25);
- the hits (HITS below), 0.6 s apart: Inky through the legs (2.4), Blaze through the right cellar deck (3.0), Bib
  through the stair tower and helideck (3.6), Freckle through the left top deck into the crane (4.2), Ghost through
  the flare boom (4.8); Blaze loops up and over the rig, comes down in front of it and smashes back through the right
  top deck (6.2); Bib loops over the left half and takes out the front left leg low (7.4), which starts the finale
  (the deck tips left end first and slides into the sea, 7.6-10.5; smoke and foam settle 10.5-12);
- after their last hit each flies on, out of frame (unhurt: "no harm to the whales").
The two loops (Showstopper 17) go up behind the rig and over its top (upside down at the top: they bank by the pull
of the turn, like a plane) and down in front of it, so the rig sits inside the loop; their tops stay under about
75 m so they pass below the Hook Text band (y 245-460).

    python3 source/flying_whales_paths.py sheet OUT.jpg     the paths through the camera and from above, with times
    python3 source/flying_whales_paths.py contacts          every rig piece each whale touches, and when
    python3 source/flying_whales_paths.py speeds            each whale's speed at every key (they must not slow
                                                            into a hit)
"""
import math
import os
import sys

import numpy as np
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import whale as W                                     # noqa: E402
import flying_whales_sea as SEA                       # noqa: E402

G = 9.8
NAMES = ['Inky', 'Blaze', 'Freckle', 'Bib', 'Ghost']  # whale.PATTERNS 0-4

# The paths as shapes: (x, y, z) waypoints in world metres, joined by a smooth curve; a waypoint with a fourth number is
# PINNED to that rig-scene time (breaking the surface, at V0; each hit); the first waypoint, under the sea, only
# sets the angle they come up at. Between pins the speed
# changes evenly from one to the next and must never drop (checked: Sam, "if anything, they speed up the closer they
# get"); after the last pin it keeps rising (ACCEL). They leave the opener at 13 m/s and burst out at about 16.
KEYS = {
    0: [  # Inky: through the legs (the front low X brace), out the back, away right and up
        (-14.0, -79.0, -4.0), (-8.0, -75.0, 0.5, 0.0), (-6.0, -58.0, 7.0), (-5.5, -24.0, 11.0),
        (-6.2, -2.0, 12.0), (-5.7, 16.9, 12.0, 2.7), (0.5, 33.0, 12.5), (12.0, 47.0, 17.0), (34.0, 60.0, 30.0),
        (66.0, 70.0, 46.0), (104.0, 78.0, 64.0)],
    1: [  # Blaze: through the right cellar deck (fireball); loops up behind the rig on its right, over the top and down
          # in front on its left (anticlockwise on screen), and smashes back through the right top deck
        (-7.0, -75.0, -4.0), (-1.0, -71.0, 0.5, 0.2), (1.5, -55.0, 8.0), (3.8, -30.0, 18.0),
        (4.0, -12.0, 26.0), (4.0, 4.7, 29.0, 3.3), (9.0, 21.0, 30.0), (14.5, 37.0, 32.0),
        (24.0, 50.0, 44.0), (31.0, 55.0, 58.0), (27.0, 34.0, 69.0), (16.0, 6.0, 66.0),
        (8.0, -10.0, 57.0), (6.0, -17.0, 49.0), (6.0, -8.0, 46.5), (6.8, 3.4, 46.5, 6.5),
        (9.0, 22.0, 47.0), (13.0, 42.0, 48.5), (35.0, 60.0, 60.0), (75.0, 75.0, 82.0)],
    2: [  # Freckle: through the left top deck into the crane house (the boom whips and topples), away left
        (-21.0, -73.0, -4.0), (-15.0, -69.0, 0.5, 0.35), (-15.0, -52.0, 10.0), (-15.0, -24.0, 26.0),
        (-14.5, -5.0, 39.0), (-13.2, 12.7, 46.0), (-9.3, 18.6, 55.0, 4.75), (-14.0, 40.0, 62.0),
        (-35.0, 60.0, 70.0), (-80.0, 75.0, 80.0)],
    3: [  # Bib: through the stair tower and helideck; loops up behind the rig on its left, over the top and down in
          # front (clockwise on screen), and takes out the front left leg low
        (-26.0, -65.0, -4.0), (-20.0, -61.0, 0.5, 0.65), (-23.0, -44.0, 9.0), (-27.0, -18.0, 22.0),
        (-30.0, 2.0, 36.0), (-31.0, 16.0, 43.0), (-31.0, 26.0, 45.0, 3.9), (-38.0, 38.0, 51.0),
        (-46.0, 52.0, 57.0), (-54.0, 58.0, 66.0), (-42.0, 36.0, 70.0), (-32.0, 8.0, 64.0),
        (-28.0, -8.0, 56.0), (-26.0, -15.0, 41.0), (-24.0, -10.0, 26.0), (-22.5, 5.0, 15.0),
        (-21.5, 23.2, 12.0, 7.7), (-16.0, 40.0, 12.5), (-30.0, 65.0, 30.0), (-95.0, 90.0, 60.0)],
    4: [  # Ghost: up the right side and through the flare boom, on out of the top right
        (2.0, -89.0, -4.0), (8.0, -85.0, 0.5, 0.5), (11.0, -66.0, 9.0), (18.0, -34.0, 22.0),
        (23.0, -10.0, 36.0), (30.0, 12.0, 47.0), (40.7, 33.2, 60.6, 5.3), (55.0, 50.0, 75.0),
        (85.0, 70.0, 95.0)],
}
V0 = 16.0                                             # m/s as they burst out (they leave the opener at 13)
ACCEL = 25.0                                          # m/s gained each second after the last hit, flying off

# What each whale smashes, by its pinned hit (the pin is the whale's middle; contacts() gives the first touch, a fifth
# of a second or so earlier); and the knock-ons its body also takes out on the way (checked: any other contact is a
# fault).
HITS = [(2.7, 0, 'brace_front_low'), (3.3, 1, 'deck_cellar_r'), (3.9, 3, 'stair_tower'), (4.75, 2, 'crane_house'),
        (5.3, 4, 'flare_boom'), (6.5, 1, 'deck_top_r'), (7.7, 3, 'leg_fl')]
KNOCK_ONS = {0: {'brace_back'}, 1: {'lifeboat_1', 'lifeboat_2', 'deck_mezz_r', 'derrick'},
             2: {'deck_top_l', 'stack_1', 'stack_2'},
             3: {'deck_mezz_l', 'helideck_truss', 'helideck', 'brace_front_high', 'brace_front_low', 'brace_left'},
             4: set()}


def _build(k):
    """The curve through whale k's waypoints, and its timing (pins: (time, arc length); the speed at each pin)."""
    pts = np.array([w[:3] for w in KEYS[k]], float)
    u = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    geo = CubicSpline(u, pts, bc_type='natural')
    uu = np.linspace(0, u[-1], 4000)
    P = geo(uu)
    arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    pins = [(w[3], float(np.interp(u[i], uu, arc))) for i, w in enumerate(KEYS[k]) if len(w) > 3]
    T, Sx, V = [pins[0][0]], [pins[0][1]], [V0]
    for (t0, s0), (t1, s1) in zip(pins, pins[1:]):       # the end speed that makes the distance fit the time
        T.append(t1), Sx.append(s1), V.append(2 * (s1 - s0) / (t1 - t0) - V[-1])
    return geo, uu, arc, np.array(T), np.array(Sx), np.array(V)


_B = {k: _build(k) for k in KEYS}


def arclen(k, t):
    geo, uu, arc, T, Sx, V = _B[k]
    if t <= T[0]:
        return Sx[0] + V[0] * (t - T[0])
    i = int(np.searchsorted(T, t)) - 1
    if i >= len(T) - 1:
        dt = t - T[-1]
        return Sx[-1] + V[-1] * dt + 0.5 * ACCEL * dt * dt
    dt, h = t - T[i], T[i + 1] - T[i]
    return Sx[i] + V[i] * dt + 0.5 * (V[i + 1] - V[i]) / h * dt * dt


def span(k):
    """From its first pin to the moment it reaches the end of its path (out of frame)."""
    geo, uu, arc, T, Sx, V = _B[k]
    t = T[-1]
    while arclen(k, t) < arc[-1]:
        t += 1 / 96
    return T[0], t


def pos(k, t):
    geo, uu, arc, *_ = _B[k]
    return geo(float(np.interp(arclen(k, t), arc, uu)))


def vel(k, t, h=1 / 96):
    return (pos(k, t + h) - pos(k, t - h)) / (2 * h)


def _acc(k, t, h=1 / 24):
    return (pos(k, t + h) - 2 * pos(k, t) + pos(k, t - h)) / (h * h)


SURFACE = {k: next(w[3] for w in v if len(w) > 3 and w[2] >= 0) for k, v in KEYS.items()}   # breaking the surface


def pose(k, t):
    """whale.Pose for whale k at t: nose along its velocity, banked by the pull of its turn (up = the felt pull,
    acceleration plus gravity's lift, kept square to the nose): level in straight flight, on its side in a hard turn,
    upside down over the top of a loop."""
    p, v, a = pos(k, t), vel(k, t), _acc(k, t)
    f = v / (np.linalg.norm(v) + 1e-9)
    up = a + np.array([0.0, 0.0, G])
    up = up - f * np.dot(up, f)
    if np.linalg.norm(up) < 1e-3:
        up = np.array([0.0, 0.0, 1.0]) - f * f[2]
    up /= np.linalg.norm(up)
    left = np.cross(up, f)
    ps = W.Pose(p)
    ps.R = np.stack([f, left, up], axis=1)
    return ps


def on_screen(k, t, cam=SEA.CAM):
    if not (span(k)[0] <= t <= span(k)[1]):
        return False
    p = pos(k, t)
    return p[2] > -6.0                                # deeper than that it is hidden in the dark sea


def speeds():
    """Each whale's speed at each pin; a fault if one slows between pins."""
    faults = []
    for k in KEYS:
        geo, uu, arc, T, Sx, V = _B[k]
        print(f'{NAMES[k]:8s}', '  '.join(f'{t:.2f}s {v:.0f}' for t, v in zip(T, V)), f'm/s | off frame {span(k)[1]:.2f}s')
        if (np.diff(V) < -0.5).any():
            faults.append(f'{NAMES[k]} slows down between pins: {np.round(V, 1).tolist()}')
    for f in faults:
        print('FAULT:', f)
    return faults


def contacts(step=1 / 48):
    """Which rig pieces each whale touches, and when (rule 5: nothing passes through anything unplanned). The whale
    is a chain of spheres along its body (flippers left out: they bend round what they brush). Each piece is tested
    item by item: a tube or line as itself (so a long diagonal boom is not padded out to a box), each face by its own
    box in the rig's frame. Returns [(first t, whale, part)]."""
    import flying_whales_rig as R

    def to_rig(p):
        q = np.asarray(p, float) - R.ORIGIN
        return np.stack([q @ R.EU, q @ R.EV, q[..., 2]], -1)
    boxes, segs = [], []
    for n, part in R.PARTS.items():
        for it in part.items:
            if it['kind'] in ('poly', 'spot'):
                q = to_rig(it['pts'])
                boxes.append((n, q.min(0), q.max(0)))
            elif it['kind'] in ('tube', 'line'):
                segs.append((n, to_rig(it['p0']), to_rig(it['p1']), it.get('r', it.get('w', 0.3) / 2)))
    bn = [b[0] for b in boxes]
    lo = np.array([b[1] for b in boxes])
    hi = np.array([b[2] for b in boxes])
    sn = [x[0] for x in segs]
    A = np.array([x[1] for x in segs])
    D = np.array([x[2] for x in segs]) - A
    rr = np.array([x[3] for x in segs])
    body = [(-5.5, 0.9), (-3.0, 1.6), (0.0, 2.0), (3.0, 1.9), (5.5, 1.3)]     # (m along the body, radius)
    out = []
    for k in KEYS:
        t0, t1 = span(k)
        seen = set()
        for t in np.arange(t0, t1, step):
            ps = pose(k, t)
            for along, r in body:
                c = to_rig(ps.pos + ps.R[:, 0] * along * W.PATTERNS[k]['size'])
                d2 = (np.maximum(lo - c, 0) ** 2 + np.maximum(c - hi, 0) ** 2).sum(1)
                u = np.clip(((c - A) * D).sum(1) / ((D * D).sum(1) + 1e-9), 0, 1)
                e2 = ((A + D * u[:, None] - c) ** 2).sum(1)
                hit = [bn[i] for i in np.nonzero(d2 < r * r)[0]] + [sn[i] for i in np.nonzero(e2 < (r + rr) ** 2)[0]]
                for n in hit:
                    if n not in seen:
                        seen.add(n)
                        out.append((round(float(t), 3), k, n))
    return sorted(out)


# ------------------------------------------------- the sheet --------------------------------------------------------
COLS = [(230, 70, 60), (250, 160, 40), (90, 200, 90), (80, 150, 250), (220, 110, 230)]


def sheet(out):
    from PIL import Image, ImageDraw
    import flying_whales_rig as R
    cam = SEA.CAM
    view = R.draw(SEA.paint(0.0, ss=1), 0.0).convert('RGB')
    d = ImageDraw.Draw(view)
    lab = W._font(26)
    d.rectangle([0, 245, 1080, 460], outline=(255, 255, 255), width=3)
    d.text((14, 250), 'Hook Text band', fill=(255, 255, 255), font=lab)
    for k in KEYS:
        t0, t1 = span(k)
        ts = np.arange(max(t0, SURFACE[k]), t1, 1 / 48)
        P = np.array([pos(k, t) for t in ts])
        S, dep = cam.screen(P)
        d.line([tuple(s) for s in S], fill=COLS[k], width=6)
        for t in np.arange(math.ceil(max(t0, SURFACE[k]) * 2) / 2, t1, 0.5):
            s = cam.screen(pos(k, t))[0]
            d.ellipse([s[0] - 7, s[1] - 7, s[0] + 7, s[1] + 7], fill=(255, 255, 255), outline=COLS[k], width=3)
            d.text((s[0] + 9, s[1] - 12), f'{t:.1f}', fill=(255, 255, 255), font=W._font(20))
        for t, kk, part in HITS:
            if kk == k:
                s = cam.screen(pos(k, t))[0]
                d.rectangle([s[0] - 10, s[1] - 10, s[0] + 10, s[1] + 10], outline=(255, 255, 255), width=4)
        s = cam.screen(pos(k, max(t0, SURFACE[k])))[0]
        d.text((s[0] - 30, s[1] + 12), NAMES[k], fill=COLS[k], font=lab)
    # whales drawn at a few moments (clip (b)'s first second, and one mid-flight each)
    frame = view.convert('RGBA')
    for k in KEYS:
        for t in (SURFACE[k] + 0.35, ):
            spr = W.draw(cam, pose(k, t), pattern=k, t=t, tint=SEA.DUSK_TINT, cut_z=0.0)
            if spr:
                spr.paste(frame)
    view = frame.convert('RGB')
    # from above: x right, y up the page (away from the camera)
    top = Image.new('RGB', (1080, 1920), (236, 232, 224))
    dt = ImageDraw.Draw(top)
    sc, ox, oy = 6.0, 540, 1500

    def T(x, y):
        return ox + x * sc, oy - y * sc
    for n in ('deck_cellar_r', 'deck_cellar_l', 'helideck', 'flare_boom'):
        a, b = R.part_box(n)
        dt.rectangle([T(a[0], b[1]), T(b[0], a[1])], outline=(90, 90, 90), width=2)
    for n, (la, lb) in R.LEGS.items():
        q = T(*R.P(la, lb, 0)[:2])
        dt.ellipse([q[0] - 6, q[1] - 6, q[0] + 6, q[1] + 6], fill=(200, 160, 40))
    dt.text((20, 20), 'From above (x right, away from the camera up the page; 1 square = 10 m)', fill=(30, 30, 30),
            font=lab)
    for gx in range(-90, 100, 10):
        dt.line([T(gx, -110), T(gx, 140)], fill=(222, 218, 210))
    for gy in range(-110, 150, 10):
        dt.line([T(-90, gy), T(90, gy)], fill=(222, 218, 210))
    c = T(0, -120)
    dt.polygon([c, T(-12, -95), T(12, -95)], fill=(60, 60, 60))
    for k in KEYS:
        t0, t1 = span(k)
        ts = np.arange(t0, t1, 1 / 48)
        P = np.array([pos(k, t) for t in ts])
        dt.line([T(x, y) for x, y, z in P], fill=COLS[k], width=5)
        for t, kk, part in HITS:
            if kk == k:
                q = T(*pos(k, t)[:2])
                dt.rectangle([q[0] - 8, q[1] - 8, q[0] + 8, q[1] + 8], outline=(20, 20, 20), width=3)
                dt.text((q[0] + 10, q[1] - 10), f'{t:.2f} {part}', fill=(20, 20, 20), font=W._font(18))
        q = T(*pos(k, t0)[:2])
        dt.text((q[0] - 20, q[1] + 8), NAMES[k], fill=COLS[k], font=lab)
    sheet_img = Image.new('RGB', (2160, 1920))
    sheet_img.paste(view, (0, 0))
    sheet_img.paste(top, (1080, 0))
    sheet_img.resize((1620, 1440), Image.LANCZOS).save(out, quality=88)
    print('saved', out)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'speeds'
    if cmd == 'sheet':
        sheet(sys.argv[2])
    elif cmd == 'contacts':
        ok = {(k, n) for _, k, n in HITS} | {(k, n) for k, v in KNOCK_ONS.items() for n in v}
        for t, k, n in contacts():
            print(f'{t:5.2f}s  {NAMES[k]:8s} {n}' + ('' if (k, n) in ok else '   FAULT: not planned'))
    else:
        speeds()
