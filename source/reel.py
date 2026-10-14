#!/usr/bin/env python3
"""reel: the movement system's test reel for Sam (and a pose sheet to check it on one picture).

    python3 source/reel.py sheet OUT.jpg       every pose and key frame on one sheet
    python3 source/reel.py reel OUT.mp4        the moving test reel (540 x 960, silent)
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import figure as F           # noqa: E402
import kit                   # noqa: E402
import moves as MV           # noqa: E402
import views as V            # noqa: E402
from ed import INK           # noqa: E402

BG = (226, 228, 214)


def cast():
    import polanski as PZ                             # the Bingo Bingo pair, as test actors
    zack = dict(PZ.ZACK, mouth='set', brows=None)
    adv = dict(PZ.ADV, mouth='set', brows=None)
    return zack, adv


def tile(draw, label, w=300, h=560, cam_z=1.0, cy=None):
    img = B.canvas(BG)
    cam = B.Cam(cam_z, 540, cy or 900)
    p = B.Pen(img, cam)
    p.poly([(-600, 1420), (1700, 1420), (1700, 2600), (-600, 2600)], (196, 198, 186), None)
    draw(img, cam)
    im = img.convert('RGB').resize((540, 960), Image.LANCZOS).crop((120, 160, 420, 160 + h * 300 // w))
    im = im.resize((w, h))
    ImageDraw.Draw(im).text((8, h - 26), label, font=ImageFont.truetype(B.SANS, 17), fill=(30, 30, 30))
    return im


def sheet(out):
    B.SS = 1
    zack, adv = cast()
    S, X, NECK = 0.8, 540, 1420 - F.SOLE_Y * 0.8
    shots = []

    def at(sp, j, yaw=0, x=X):
        def draw(img, cam):
            kit.feet_shadow(img, cam, x, NECK, S)
            V.person(img, cam, x, NECK, S, sp, 0.0, yaw, j)
        return draw
    for name in MV.POSES:
        shots.append((at(zack, MV.pose(zack, name)), name))
    shots.append((at(adv, MV.seated(adv)), 'seated'))
    for u in (0.1, 0.3, 0.6):
        shots.append((at(adv, MV.stand_up(adv, u), 90), f'stand up {int(u * 100)}%'))
    for kind in MV.GAITS:
        shots.append((at(zack, MV.gait(zack, 0.12, kind), 90), kind))
    for dt, lab in ((-0.25, 'punch: wind-up'), (0.0, 'punch: contact')):
        shots.append((at(zack, MV.punch(zack, 1.0 + dt, 1.0)[0], 90), lab))
    shots.append((at(zack, MV.kick(zack, 1.0, 1.0)[0], 90), 'kick'))
    for dt, lab in ((-0.2, 'sword: raised'), (0.0, 'sword: cut')):
        shots.append((at(zack, MV.sword(zack, 1.0 + dt, 1.0)[0], 90), lab))
    shots.append((at(adv, MV.hit_react(adv, 1.06, 1.0)[0], -90), 'hit'))
    for dt, lab in ((0.25, 'fall: knees'), (0.5, 'fall: hips'), (1.0, 'fall: lying')):
        shots.append((at(adv, MV.fall(adv, 1.0 + dt, 1.0)[0], -90), lab))
    shots.append((at(zack, MV.driving(zack, 0.0), 90), 'driving'))
    shots.append((at(zack, MV.car_in(zack, 0.55), 90), 'getting in'))
    tiles = [tile(d, lab) for d, lab in shots]
    cols = 9
    sh = Image.new('RGB', (cols * 302, ((len(tiles) + cols - 1) // cols) * 562), (40, 40, 40))
    for i, im in enumerate(tiles):
        sh.paste(im, ((i % cols) * 302, (i // cols) * 562))
    sh.save(out, quality=85)
    print('sheet:', out, len(tiles), 'poses')


SECTIONS = []


def section(title, dur):
    def deco(fn):
        SECTIONS.append((title, dur, fn))
        return fn
    return deco


def _room(X=0.0, f=1700.0):
    import series
    return series.Room(X, 1.5, 7.5, f, sx=540, sy=600)


@section('Gaits from the side: stroll, walk, brisk, run, sprint', 9.0)
def gaits(img, cam, t, zack, adv):
    import stage
    kinds = list(MV.GAITS)
    k = min(len(kinds) - 1, int(t / 1.8))
    kind, u = kinds[k], t - k * 1.8
    X = MV.speed(kind) * u
    st = stage.Stage(_room(X))                            # the camera follows him: the floor slides under planted feet
    st.floor(img, cam, x0=X - 6, x1=X + 6)
    st.draw(img, cam, [stage.Actor(zack, X, 3.5, 90, MV.gait(zack, u, kind), t)])
    return kind


@section('Walking in perspective: towards us, across, the straight-180 turn, away', 9.0)
def angles(img, cam, t, zack, adv):
    import stage
    st = stage.Stage(_room())
    st.floor(img, cam)
    path = [(-1.6, 0.8), (-0.4, 3.6), (0.7, 3.6)]
    X, Z, yaw, state = MV.travel(path, t, 'walk')
    T = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:])) / MV.speed('walk')
    if state == 'arrived':                                 # hold, pop round (180), walk away into the distance
        u = t - T
        if u < 0.4:
            pose = V.standing(zack)
        else:
            X, Z = 0.7, 3.6 - MV.speed('walk') * (u - 0.4)
            yaw = 180
            pose = MV.gait(zack, u - 0.4, 'walk')
            if u >= 0.4 and Z < 0.5:
                Z = 0.5
        st.draw(img, cam, [stage.Actor(zack, X, Z, yaw, pose, t)])
    else:
        st.draw(img, cam, [stage.Actor(zack, X, Z, yaw, MV.gait(zack, t, 'walk'), t)])
    return None


@section('Pacing (straight-180 turns at each end)', 6.0)
def pacing(img, cam, t, zack, adv):
    import stage
    st = stage.Stage(_room())
    st.floor(img, cam)
    X, Z, yaw, pose = MV.pace(zack, t, (-1.1, 2.5), (1.1, 2.5))
    st.draw(img, cam, [stage.Actor(zack, X, Z, yaw, pose, t)])


STYLES = ['relaxed', 'hips', 'arms_folded', 'pockets', 'behind_back', 'slumped', 'palm_open', 'chop', 'shrug', 'point',
          'facepalm', 'head_in_hands', 'heart']
PROPS = ['phone_ear', 'phone_read', 'paper', 'mug', 'mug_sip', 'mic', 'pen', 'bag']


def _cycle(sp, names, t, hold=0.65):
    """Held poses, one to the next with a single in-between drawing (limited animation)."""
    k = int(t / hold)
    u = t - k * hold
    a = MV.pose(sp, names[min(k, len(names) - 1)], beat=abs(math.sin(math.pi * u / 0.33)))
    if u < 1 / 12 and k > 0:
        b = MV.pose(sp, names[k - 1])
        return MV.mix_poses(b, a, 0.5), names[min(k, len(names) - 1)]
    return a, names[min(k, len(names) - 1)]


@section('Standing styles and gestures', len(STYLES) * 0.65)
def styles(img, cam, t, zack, adv):
    import stage
    st = stage.Stage(_room(f=2300.0))
    st.floor(img, cam)
    pose, name = _cycle(zack, STYLES, t)
    st.draw(img, cam, [stage.Actor(zack, 0.0, 4.2, 0, pose, t)])
    return name.replace('_', ' ')


@section('Holding things', len(PROPS) * 0.65)
def holding(img, cam, t, zack, adv):
    import stage
    st = stage.Stage(_room(f=2300.0))
    st.floor(img, cam)
    pose, name = _cycle(zack, PROPS, t)
    st.draw(img, cam, [stage.Actor(zack, 0.0, 4.2, 0, pose, t)])
    return name.replace('_', ' ')


@section('Sitting down and standing up (the four phases)', 6.0)
def sitting(img, cam, t, zack, adv):
    import stage
    st = stage.Stage(_room(f=2100.0))
    st.floor(img, cam)
    if t < 1.8:
        pose = MV.sit_down(adv, t / 1.8)
    elif t < 3.2:
        pose = MV.seated(adv)
    elif t < 5.0:
        pose = MV.stand_up(adv, (t - 3.2) / 1.8)
    else:
        pose = V.standing(adv)
    st.draw(img, cam, [stage.Actor(adv, 0.0, 4.0, 90, pose, t)])


@section('Combat: punch, the hit and the fall, a kick, a sword swing', 9.0)
def combat(img, cam, t, zack, adv):
    import stage
    st = stage.Stage(_room(f=2000.0))
    st.floor(img, cam)
    if t < 4.2:
        hit_t = 1.2
        gap = 0.62                                         # metres between them: the fist just reaches his face
        target = (0.0, -150.0, gap / V.M_PER_UNIT - 60)
        zp, _ = MV.punch(zack, t, hit_t, target)
        if t < hit_t + 0.45:
            ap, stag = MV.hit_react(adv, t, hit_t)
        else:
            ap, _ = MV.fall(adv, t, hit_t + 0.45)
            stag = 0.25
        st.draw(img, cam, [stage.Actor(zack, -0.4, 4.0, 90, zp, t),
                           stage.Actor(adv, -0.4 + gap + stag, 4.0, -90, ap, t)])
        return 'punch, hit, fall'
    if t < 6.4:
        zp, _ = MV.kick(zack, t - 4.2, 1.0)
        st.draw(img, cam, [stage.Actor(zack, 0.0, 4.0, 90, zp, t)])
        return 'kick'
    zp, _ = MV.sword(zack, t - 6.4, 1.3)
    st.draw(img, cam, [stage.Actor(zack, 0.0, 4.0, 90, zp, t)])
    return 'sword swing'


@section('Car-ready: driving, getting in (the car is drawn per film)', 5.0)
def car(img, cam, t, zack, adv):
    import stage
    st = stage.Stage(_room(f=2100.0))
    st.floor(img, cam)
    if t < 2.5:
        st.draw(img, cam, [stage.Actor(zack, 0.0, 4.0, 90, MV.driving(zack, t, steer=math.sin(t * 2.5)), t)])
        return 'driving'
    st.draw(img, cam, [stage.Actor(zack, 0.0, 4.0, 90, MV.car_in(zack, min(1.0, (t - 2.5) / 2.2)), t)])
    return 'getting in'


def reel_frame(i):
    import burnham as B_
    B_.SS = 1
    zack, adv = cast()
    t = i / 12.0
    for title, dur, fn in SECTIONS:
        if t < dur:
            img = B.canvas(BG)
            cam = B.Cam(1.0, 540, 960)
            sub = fn(img, cam, t, zack, adv)
            d = ImageDraw.Draw(img)
            f = ImageFont.truetype(B.SANS, 34)
            rows = B.wrap(title, f, 960)
            for k, r in enumerate(rows):
                d.text((540, 360 + 44 * k), r, font=f, fill=(30, 30, 30), anchor='mm')
            if sub:
                d.text((540, 360 + 44 * len(rows) + 10), sub, font=ImageFont.truetype(B.SANS, 30), fill=(90, 90, 90), anchor='mm')
            return np.asarray(img.convert('RGB').resize((540, 960), Image.LANCZOS)).tobytes()
        t -= dur
    return np.asarray(B.canvas((0, 0, 0)).convert('RGB').resize((540, 960))).tobytes()


def reel(out):
    import imageio_ffmpeg
    from multiprocessing import Pool
    n = int(sum(d for _, d, _ in SECTIONS) * 12)
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', '540x960', '-r', '12', '-i', '-', '-c:v', 'libx264', '-crf', '22', '-pix_fmt', 'yuv420p',
                          '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for fr in pool.imap(reel_frame, range(n), chunksize=4):
            p.stdin.write(fr)
    p.stdin.close()
    p.wait()
    print('reel:', out, f'({n / 12:.1f} s, {os.path.getsize(out) / 1e6:.1f} MB)')


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'reel':
        reel(sys.argv[2])
        sys.exit()
    if len(sys.argv) >= 3 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
    else:
        print(__doc__)
