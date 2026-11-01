#!/usr/bin/env python3
"""Flying Whales, the opening scene (planning, 1 Nov): the plan in metres as numbers, and the rough composition sheet.

The scene (Sam, 1 Nov; notes/flying-whales.md, "Opening scene"): about 5.6 s under the sea at dusk. Five humpbacks
(the same five as the rig scene) swim at us on a slight diagonal; the camera swings round to their side and swims
alongside; on "imagined" they tilt up and race for the bright surface; hard cut to the rig scene (they burst out
flying, heading up and to the right, as on the rig composition sheet: rule 16, direction holds across the cut).

The world (whale.py axes: x right, y away from the first camera, z up; metres):
- the sea surface is z = 0; open water, no sea bed (it fades to deep blue below); you can see about 45 m;
- the pod swims along +x (screen right once the camera is at their side); the lead whale's middle starts 14 m down;
- each whale follows the lead's track a set distance behind, offset to the side and up/down (FORMATION), so when the
  lead tilts up the others tilt up as they reach the same spot (no marching in step, rule 9);
- the camera is placed round the pod in the pod's own frame (angle from straight ahead of the pod towards its right,
  distance, height) and looks at a point 7 m behind the lead (CAM_KEYS); one lens all scene (focal 1400, the rig
  scene's lens).
The water, surface, light shafts, specks, bubbles and the fish shoal are the underwater set,
`source/flying_whales_under.py` (built 1 Nov after Sam's yes; benchmarked against his refs, rule 3).

    python3 source/flying_whales_opener.py comp OUT.jpg     the rough composition sheet (four key moments + the plan)
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import whale as W                                     # noqa: E402
import flying_whales_under as U                       # noqa: E402

SIZE = (1080, 1920)
FOCAL = 1400.0
HOOK_BAND = (245, 460)                                # screen y: the Hook Text band, as on the rig composition sheet

# timings (s): placeholders until Sam's recording; re-pinned to his word times when it arrives
LINE = (0.3, 5.0)                                     # "This series, we will see animal behaviour we could scarcely have imagined."
IMAGINED = 4.2                                        # the word that starts the rise
CUT = 5.6                                             # hard cut to the rig scene
RISE_PITCH = 40.0                                     # degrees, nose up, reached 0.6 s after the rise starts

# the pod: pattern (whale.PATTERNS), metres behind the lead along its track, to its right, above it
FORMATION = [
    (0, 0.0, 0.0, 0.0),        # Inky leads, nearest the camera's side
    (1, -9.0, -6.0, 3.0),      # Blaze, a length back, further off, a little higher
    (2, -15.0, 5.0, -5.0),     # Freckle, our side and low: passes under the lens (the foreground layer)
    (3, -21.0, -11.0, -1.0),   # Bib, far side
    (4, -28.0, -3.0, 4.0),     # Ghost, last and high
]

# the camera round the pod: (t, angle from straight ahead towards the pod's right (deg), distance (m), height (m))
CAM_KEYS = [
    (0.0, 20.0, 44.0, 1.0),    # in front, a little to their right: they come at us on a slight diagonal
    (1.8, 24.0, 27.0, 0.0),    # they close on us (the lead's face and brow big)
    (3.4, 92.0, 21.0, -1.0),   # swung round to their right side: they cross the screen left to right
    (4.2, 98.0, 21.0, -2.0),   # alongside, pacing them
    (CUT, 112.0, 24.0, -10.0), # dropping below them and tilting up as they race for the surface
]


def speed(t):
    """The pod's speed (m/s): 6 rising to 8 as they come (they speed up, never slow), then 13 on the rise."""
    if t < IMAGINED:
        return 6.0 + 2.0 * max(t, 0.0) / IMAGINED
    return 8.0 + 5.0 * min((t - IMAGINED) / 1.0, 1.0)


def _ease(a):
    a = min(max(a, 0.0), 1.0)
    return a * a * (3 - 2 * a)


def pitch(t):
    return RISE_PITCH * _ease((t - IMAGINED) / 0.6)


_DT = 1 / 120


def _track():
    """The lead's track: arc length -> (position, pitch), sampled from t = -6 s to the cut (behind us it is level)."""
    pts, s, p = [], 0.0, np.array([0.0, 0.0, -14.0])
    t = -6.0
    p = p - np.array([sum(speed(-6 + k * _DT) * _DT for k in range(int(6 / _DT))), 0, 0])
    out = []
    while t <= CUT + 0.5:
        pc = pitch(t)
        out.append((t, s, p.copy(), pc))
        v = speed(t) * _DT
        p = p + v * np.array([math.cos(math.radians(pc)), 0.0, math.sin(math.radians(pc))])
        s += v
        t += _DT
    return out


TRACK = _track()
_S = np.array([r[1] for r in TRACK])
_T = np.array([r[0] for r in TRACK])


def _at_s(s):
    i = int(np.clip(np.searchsorted(_S, s), 1, len(TRACK) - 1))
    a = TRACK[i - 1]
    return a[2], a[3]


def lead_s(t):
    return float(np.interp(t, _T, _S))


def poses(t):
    """[(pattern, whale.Pose)] for the five at time t: each on the lead's track, offset in the track's frame."""
    out = []
    s0 = lead_s(t)
    for pat, back, right, up in FORMATION:
        pos, pc = _at_s(s0 + back)
        f = np.array([math.cos(math.radians(pc)), 0.0, math.sin(math.radians(pc))])
        u = np.array([-math.sin(math.radians(pc)), 0.0, math.cos(math.radians(pc))])
        r = np.array([0.0, -1.0, 0.0])                       # the pod's right (heading +x) is -y
        out.append((pat, W.Pose(pos + right * r + up * u, yaw=-90.0, pitch=pc, roll=0.0)))
    return out


def _key(t):
    ks = CAM_KEYS
    if t <= ks[0][0]:
        return ks[0][1:]
    for a, b in zip(ks, ks[1:]):
        if t <= b[0]:
            e = _ease((t - a[0]) / (b[0] - a[0]))
            return tuple(x + (y - x) * e for x, y in zip(a[1:], b[1:]))
    return ks[-1][1:]


def camera(t):
    """The film's camera at t: placed round the aim point (7 m behind the lead, 2 m once they rise) in the pod's level
    frame."""
    aim, _ = _at_s(lead_s(t) - 7.0 + 5.0 * _ease((t - IMAGINED) / 1.0))   # on the rise, aim nearer the lead
    ang, dist, h = _key(t)
    a = math.radians(ang)
    pos = aim + np.array([dist * math.cos(a), -dist * math.sin(a), h])
    pos[2] = min(pos[2], -1.5)                               # the lens stays under the water
    return W.Cam.looking_at(aim, pos, FOCAL, SIZE)


# ------------------------------------------- the frame (the set: flying_whales_under) -------------------------------
def blowhole(t, k):
    """Whale k's blowhole (world, m) at time t: on top of the head, about a quarter back from the snout."""
    pat, pose = poses(t)[k]
    sz = W.PATTERNS[pat]['size']
    return pose.world(np.array([3.78 * sz, 0.0, 0.95 * sz]))


def _pod_axes(t):
    out = []
    for pat, pose in poses(t):
        sz = W.PATTERNS[pat]['size']
        out.append((pose.world(np.array([-6.2 * sz, 0, 0])), pose.world(np.array([6.4 * sz, 0, 0])), 1.7 * sz))
    return out


U.set_pod('opener', _pod_axes)
TINT = (30, 100, 170, 0.2)                            # the blue-teal of the water on every whale


def frame(t, ss=1):
    cam = camera(t)
    sprs = []
    for k, (pat, pose) in enumerate(poses(t)):
        spr = W.draw(cam, pose, pattern=pat, t=t + k * 0.37, flap=0.6, beat=1.0, tint=TINT, phase=k * 0.9)
        if spr:
            k_h = U.haze(float(np.linalg.norm(pose.pos - cam.pos)))      # fade into the water with distance (B5)
            arr = np.asarray(spr.img).astype(np.float32)
            arr[..., :3] = arr[..., :3] * (1 - k_h) + np.array(U.HAZE) * k_h
            spr.img = Image.fromarray(arr.astype(np.uint8), 'RGBA')
            sprs.append(spr)
    im = U.compose(cam, t, sprs, blowhole=blowhole, since=IMAGINED, pod_key='opener', ss=ss)
    return im, cam


# ------------------------------------------------- the sheet --------------------------------------------------------
MOMENTS = [
    (0.4, '1  0.4 s  "This series..."', 'they come at us on a slight diagonal'),
    (2.0, '2  2.0 s  "...we will see..."', 'the lead close: its face and brow'),
    (3.6, '3  3.6 s  "...animal behaviour..."', 'camera alongside: left to right'),
    (5.3, '4  5.3 s  "...imagined."', 'up for the surface; hard cut at 5.6'),
]


def _plan_view(w, h):
    """Top-down (x right, y up the page) and side (x right, z up) sketch: the lead's track, the camera's path."""
    im = Image.new('RGB', (w, h), (244, 240, 232))
    dr = ImageDraw.Draw(im)
    f = W._font(22)
    ts = np.arange(0, CUT + 1e-6, 0.4)
    allp = [pose.pos for tt in ts for _, pose in poses(tt)] + [camera(tt).pos for tt in ts]
    P = np.array(allp)
    x0, x1 = P[:, 0].min() - 8, P[:, 0].max() + 8
    y0, y1 = P[:, 1].min() - 6, P[:, 1].max() + 6
    half = h // 2
    sc = min((w - 60) / (x1 - x0), (half - 90) / (y1 - y0), (half - 110) / (P[:, 2].max().clip(0) + 24))

    def top(p):
        return 30 + (p[0] - x0) * sc, 50 + (y1 - p[1]) * sc

    def side(p):
        return 30 + (p[0] - x0) * sc, half + 60 - p[2] * sc

    dr.text((12, 8), 'From above: the pod (grey) swims left to right;', fill=(30, 30, 30), font=f)
    dr.text((12, 32), 'the camera (red) swings round to its right side (the bottom of this view)', fill=(30, 30, 30),
            font=f)
    dr.line([0, half, w, half], fill=(200, 196, 188), width=2)
    dr.text((12, half + 8), 'From the side: sea surface at 0 m; the rise starts on "imagined"', fill=(30, 30, 30), font=f)
    dr.line([side((x0, 0, 0)), side((x1, 0, 0))], fill=(60, 140, 190), width=3)
    dr.text((side((x1, 0, 0))[0] - 120, side((x1, 0, 0))[1] - 26), 'surface 0 m', fill=(60, 140, 190), font=f)
    for depth in (10, 20):
        y = side((0, 0, -depth))[1]
        dr.text((6, y - 10), f'-{depth}', fill=(120, 120, 120), font=f)
    for tt in ts:
        for pat, pose in poses(tt):
            for fn in (top, side):
                x, y = fn(pose.pos)
                dr.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(150, 150, 160))
        c = camera(tt)
        for fn in (top, side):
            x, y = fn(c.pos)
            dr.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(210, 50, 40))
    for k, (tt, _, _) in enumerate(MOMENTS):
        c = camera(tt)
        lead = poses(tt)[0][1].pos
        for fn in (top, side):
            x, y = fn(c.pos)
            lx, ly = fn(lead)
            dr.line([x, y, lx, ly], fill=(210, 50, 40), width=2)
            dr.text((x + 8, y + 4), str(k + 1), fill=(210, 50, 40), font=W._font(26))
    dr.line([30, h - 30, 30 + 20 * sc, h - 30], fill=(30, 30, 30), width=4)
    dr.text((36 + 20 * sc, h - 44), '20 m', fill=(30, 30, 30), font=f)
    return im


def comp(out):
    tw, th = 540, 960
    pad, head = 24, 80
    tiles = []
    for t, l1, l2 in MOMENTS:
        im, cam = frame(t)
        im = im.resize((tw, th), Image.LANCZOS)
        dr = ImageDraw.Draw(im)
        y0, y1 = HOOK_BAND[0] / 2, HOOK_BAND[1] / 2
        dr.rectangle([30, y0, tw - 30, y1], outline=(255, 255, 255), width=3)
        dr.text((tw / 2 - 90, (y0 + y1) / 2 - 12), 'Hook Text band', fill=(255, 255, 255), font=W._font(22))
        tiles.append(((l1, l2), im))
    pw = 2 * tw + pad
    plan = _plan_view(pw, th)
    W_ = pad + 4 * (tw + pad)
    sheet = Image.new('RGB', (W_ + pw + pad, head + th + pad), (244, 240, 232))
    dr = ImageDraw.Draw(sheet)
    for k, (label, im) in enumerate(tiles):
        x = pad + k * (tw + pad)
        sheet.paste(im, (x, head))
        dr.text((x, 14), label[0], fill=(30, 30, 30), font=W._font(22))
        dr.text((x, 44), label[1], fill=(70, 70, 70), font=W._font(20))
    sheet.paste(plan, (W_, head))
    dr.text((W_, 14), 'The plan in metres (dots every 0.4 s; red lines:', fill=(30, 30, 30), font=W._font(22))
    dr.text((W_, 44), 'the camera to the lead whale at moments 1-4)', fill=(70, 70, 70), font=W._font(20))
    sheet.save(out, quality=88)
    print(out, sheet.size)


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'comp':
        comp(sys.argv[2])
    else:
        print(__doc__)
