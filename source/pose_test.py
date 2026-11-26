#!/usr/bin/env python3
"""MAP  pose_test: a blank test scene (Sam, 26 Nov: "Open a fresh chat and open a blank test environment. Run the
background people and their movements on the new model engine and show me a five second render of each"). Open
Wounds' background people (notes/brexit-is-done.md brief items 6, 7, 8, 11), moving as the film moves them (their
poses are read from brexit_is_done_action, never changed), each drawn on R7's body tool (solid_seat mode 'body': the
MakeHuman body posed by its joints, the posted outfit on top) on a plain background. Learning only: no film uses it.
Notes and results: notes/learn/pose-test/.

  STAND .............. the body tool, opened to standing and moving people for this scene only (views.r7_on is
                       seated only): stand_solid on the spec; lay_over (seated knees over the jacket) off when not
                       seated; _smooth cropped to the person (same result, a quarter of the time)
  cam(), at() ........ a level 3D camera (sets.Cam) on a 1080 x 1920 canvas; someone at floor point x, z, height up
  torn(u) ............ item 6: W1 digging, the hit (0.6 s), knees and hips (moves.fall) on the body tool; from the hips
                       landing (1.1 s) the body on the floor CANNOT be drawn on the body tool yet: drawn by the old
                       lying body (lying.draw), labelled so on the frame
  runner(u) .......... item 7: W2's sprint (moves.gait 'sprint', open_back), the leap off the end (3.6 s), side on
  bars(u) ............ item 8: W3-W5 with steel tubes (_bar_man jabs, W5's overhead swing); arms still flat on top
  flee(u) ............ item 11: a guest out of the doors at us (front_run), three-quarter, then side on across
  render(who) ........ 5 s at 24 fps, MP4 in notes/learn/pose-test/; checks stray_ink, leg_tone on sampled frames

    python3 source/pose_test.py WHO [--frames N]     WHO: torn, runner, bars, flee, all
"""
import math
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import brexit_is_done_action as A    # noqa: E402  (read only: the film's poses and timings)
import lying                         # noqa: E402
import moves as MV                   # noqa: E402
import people_parts as PPt           # noqa: E402
import people as PK                  # noqa: E402
import sets                          # noqa: E402
import solid_seat as SS              # noqa: E402

B, V = PPt.B, PPt.V
PK.install(PK.load('brexit-is-done'))   # the crowd pack's heads, hair and hats, as the film installs them (Sam, 26 Nov:
#                                         without it everyone fell back to the old default head: bald, no hard hat)
OUT = os.path.join(HERE, '..', 'notes', 'learn', 'pose-test')
W, H, FPS, SECS = 1080, 1920, 24, 5.0   # full film size (Sam, 26 Nov: no low-resolution practice)
BG = (236, 232, 224)
FLOOR = (205, 199, 188)

# ================================================================================================= STAND
_r7_on = V.r7_on
V.r7_on = lambda j, sp, view: (bool(sp.get('stand_solid')) and view in V.SEATED_R7_VIEWS) or _r7_on(j, sp, view)
_lay_over = SS.lay_over


def _lay(img, p=None):
    if (SS.LAST.get('j') or {}).get('lap'):
        return _lay_over(img, p)


SS.lay_over = _lay
_smooth = SS._smooth


def _smooth_crop(zb, pb, ob, ab, r):
    ys, xs = np.where(ob >= 0)
    if not len(ys):
        return
    m = int(6 * r) + 12
    y0, y1 = max(0, ys.min() - m), min(zb.shape[0], ys.max() + m + 1)
    x0, x1 = max(0, xs.min() - m), min(zb.shape[1], xs.max() + m + 1)
    _smooth(zb[y0:y1, x0:x1], pb[y0:y1, x0:x1], ob[y0:y1, x0:x1], ab[y0:y1, x0:x1], r)


SS._smooth = _smooth_crop


def body(sp):
    sp = dict(sp)
    sp.update(seat_solid='body', seat_r7=True, stand_solid=True, legs_soft=True)
    return sp


# ================================================================================================= camera
def cam(dist=3.2, hgt=1.0):
    """Level, 1.0 m up, looking north at a floor point `dist` m away, centred on the canvas."""
    return sets.Cam((0.0, hgt, -dist), (0.0, hgt, 0.0), focal=1000.0 * W / 540, shake=(W / 2 - 540, H / 2 - 960))


def at(img, c, sp, x, z, yaw, j, t, up=0.0, shadow=True):
    """Someone standing at floor point (x, z) through 3D camera c, `up` m off the floor; returns the drawn joints."""
    Xf, Yf, s, _, _ = lying.place(c, x, z)
    ppm = c.project((x, 0.0, z))[1]
    if shadow:
        g = A.glaze(img)
        k = max(0.3, 1.0 - up / 1.5)
        g.ellipse([Xf - 150 * s * k, Yf - 18 * s * k, Xf + 150 * s * k, Yf + 18 * s * k], fill=(0, 0, 0, 55))
    B.SS = 1
    y = Yf - A.FEET * s - up * ppm
    # drawn on a sheet just round the person, then laid on the frame: the body tool works over its whole canvas, so
    # at full film size a whole-frame canvas cost about 15x (same picture: the camera is shifted to the sheet)
    hw, top, bot = int(700 * s), int(y - 520 * s), int(y + (A.FEET + 160) * s)
    x0, y0 = int(Xf) - hw, top
    sub = Image.new('RGBA', (2 * hw, bot - top), (0, 0, 0, 0))
    jj = V.person(sub, B.Cam(1.0, x0 + 540, y0 + 960), Xf, y, s, sp, t, yaw, j)
    img.alpha_composite(sub, (max(0, x0), max(0, y0)), (max(0, -x0), max(0, -y0)))
    return A._screen(jj, Xf, y, s, yaw)


def canvas(c, scroll=0.0, edge=None):
    """Plain background, a floor below the horizon; ticks on the floor scroll with a runner (speed reads). `edge`:
    the floor ends this far (m) right of the middle (the lift's end he leaps from; beyond it, the drop)."""
    img = Image.new('RGBA', (W, H), BG + (255,))
    g = ImageDraw.Draw(img)
    hz = c.project((0.0, c.pos[1], 50.0))[0][1]
    g.rectangle([0, hz, W, H], fill=FLOOR)
    if edge is not None:
        ex = c.project((edge, 0.0, -0.8))[0][0]
        g.rectangle([0, hz, ex, H], fill=BG)
        g.rectangle([ex - 6, c.project((edge, 0.0, -0.8))[0][1] - 4, ex, H], fill=(150, 156, 164))
    for k in range(-20, 21):
        x = k * 1.0 - (scroll % 1.0)
        if edge is not None and x < edge:
            continue
        a = c.project((x, 0.0, 0.6))[0]
        b = c.project((x, 0.0, -0.6))[0]
        g.line([a, b], fill=(186, 180, 170), width=3)
    return img


def label(img, text):
    g = ImageDraw.Draw(img)
    g.rectangle([0, 0, W, 34], fill=(255, 255, 255))
    g.text((10, 10), text, fill=(20, 20, 20))


# ================================================================================================= the four
def torn(u):
    """Item 6: W1 digs (side on, a little towards us: the film's 195 degrees), the wolves hit him at 0.6 s, knees and
    hips; then on the floor (the old lying body: the body tool cannot lie down yet)."""
    c = cam()
    img = canvas(c)
    sp = body(A.WORKERS[0])
    tw = math.radians(195.0 - 10.0 * A.ease((u - A.HIT) / 0.5))
    face = (math.cos(tw), math.sin(tw))
    yaw = c.yaw_of((0.0, 0, 0.0), face)
    if u < A.HIT:
        j = A._worker1_pose(sp, u)
        jj = at(img, c, sp, 0.0, 0.0, yaw, j, u)
        a, b = jj['wrR_px'], jj['wrL_px']
        gy = c.project((0.0, 0.0, 0.0))[0][1] - 0.05 * c.project((0, 0, 0))[1]
        k = (gy - a[1]) / max(1.0, b[1] - a[1])
        heel = (a[0] + (b[0] - a[0]) * k, gy)
        g = ImageDraw.Draw(img)
        g.line([(a[0] - (b[0] - a[0]) * 0.35, a[1] - (b[1] - a[1]) * 0.35), heel], fill=(120, 84, 50), width=6)
        return img, 'body tool: digging'
    bare = dict(sp, kit_hat=None)
    kind, *rest = lying.fall(bare, u, A.HIT, 0.0, 0.0, (math.cos(math.radians(185.0)), math.sin(math.radians(185.0))))
    if kind == 'views':
        at(img, c, bare, 0.0, 0.0, c.yaw_of((0.0, 0, 0.0), face), rest[0], u)
        return img, 'body tool: knocked down'
    k, surf = rest
    plain = dict(A.WORKERS[0], kit_hat=None)
    lying.draw(img, c, k, plain, u, surfaces=surf)
    label(img, 'NOT the body tool: old lying body (cannot lie down yet)')
    return img, 'old lying body'


def runner(u):
    """Item 7: W2 sprints side on (the film's gait and speed), leaps off the lift's end at 3.6 s, out of frame."""
    c = cam(4.2)
    sp = body(A.WORKERS[1])
    t0, leap = 0.0, 3.6
    run = A.RUN_SPEED
    x, up = 0.0, 0.0
    j = MV.open_back(MV.gait(sp, u - t0, 'sprint', stride=1.5 / V.M_PER_UNIT, steps_per_s=run / 1.5), 'sprint',
                     yaw=-90.0)
    scroll = run * u
    edge = None
    if u > leap:
        v = u - leap
        up = 3.2 * v - 4.9 * v * v
        edge = run * v - 0.3
        j = MV.gait(sp, 0.12, 'sprint')
        j['lean'] = 18
        for s_, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s_, (sg * 200.0, 60.0, 200.0), 'out', 'palm')
    img = canvas(c, -scroll, edge)
    if up < -2.6:
        return img, 'gone'
    with A.FG.allow('a sprint seen side on: the back arm swings behind the body (moves.gait)'):
        at(img, c, sp, x, 0.0, -90.0, j, u, up=up, shadow=u <= leap)
    return img, 'body tool: sprint' if u <= leap else 'body tool: leap'


def bars(u):
    """Item 8: three men with steel tubes as the film's W3-W5: two jab as a wolf lunges (a step back first), W5's
    overhead swing clangs at 4.3 s. Film time u + 0.0 (lunges at 0.5, 2.0, 3.5)."""
    c = cam(5.6)
    img = canvas(c)
    for n, m in sorted(enumerate(A.BAR_MEN), key=lambda nm: -nm[1]['d']):      # far to near
        sp = body(A.WORKERS[m['i']])
        x = (m['x'] - A.BAR_MEN[1]['x']) * 1.15 + 0.15
        z = (m['d'] - A.LIFT_D) * 1.6
        if n < 2:
            j, jab, _ = A._bar_man(sp, u, n)
        else:
            j = V.standing(sp)
            v = u - (A.CLANG - 0.45)
            ang = A.keyed(v, [(0.0, 0.0), (0.3, 1.0), (0.45, 0.55), (0.52, 0.62), (0.7, 0.58), (1.6, 0.0)])
            j['lean'] = 4 + 8 * ang
            hy = 300.0 - 260.0 * math.sin(math.pi * ang * 0.9)
            V.arm_to(j, 'L', (-40.0, hy, 240.0 - 40 * ang), 'down', 'fist')
            V.arm_to(j, 'R', (40.0, hy + 40, 140.0 - 20 * ang), 'down', 'fist')
        jj = at(img, c, sp, x, z, -90.0, j, u)
        a, b = jj['wrR_px'], jj['wrL_px']
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        ext = 0.9 * c.project((x, 0, z))[1] * 0.5
        e = (b[0] + dx / L * ext, b[1] + dy / L * ext)
        s_ = (a[0] - dx / L * 20, a[1] - dy / L * 20)
        A.tube(img, s_, e, max(3, int(0.035 * c.project((x, 0, z))[1])))
    return img, 'body tool: bars (arms flat on top)'


def flee(u):
    """Item 11: a guest runs out of the doors straight at us (front_run, 0-1.2 s), turns three-quarter (to 1.8 s),
    then side on across (the film's run, open_back), at the film's 4.4 m/s."""
    sp = body(A.GUESTS[2])      # a man in a suit (a dress is not yet on the body tool)
    c = cam(4.2)
    if u < 1.2:
        z = 3.0 - A.GUEST_V * 0.55 * u
        yaw, j = 0.0, MV.gait(sp, u, 'front_run')
        x, scroll = 0.0, 0.0
    else:
        z = 3.0 - A.GUEST_V * 0.55 * 1.2
        yaw = -45.0 if u < 1.8 else -90.0
        j = MV.open_back(MV.gait(sp, u + 0.13, 'run', steps_per_s=A.GUEST_V / A.RUN_STEP), 'run', yaw=yaw)
        x, scroll = 0.0, A.GUEST_V * (u - 1.2)
        if u < 1.8:
            z -= A.GUEST_V * 0.4 * (u - 1.2)
        else:
            z -= A.GUEST_V * 0.4 * 0.6
    img = canvas(c, -scroll)
    with A.FG.allow('a run seen side on: the far arm swings behind the body (moves.gait)'):
        at(img, c, sp, x, z, yaw, j, u)
    return img, 'body tool: %s' % ('front run' if yaw == 0 else 'run')


WHO = dict(torn=torn, runner=runner, bars=bars, flee=flee)
SPEC = dict(torn=lambda: body(A.WORKERS[0]), runner=lambda: body(A.WORKERS[1]),
            bars=lambda: body(A.WORKERS[2]), flee=lambda: body(A.GUESTS[2]))


# ================================================================================================= render
def render(who, frames=None):
    os.makedirs(OUT, exist_ok=True)
    n = int(SECS * FPS) if frames is None else frames
    tmp = tempfile.mkdtemp(prefix='pt_' + who, dir=os.environ.get('PT_TMP'))
    sp = SPEC[who]()
    bad = PK.head_faults(sp)
    if bad:
        sys.exit('pose_test REFUSED: ' + '; '.join(bad))
    faults, what = [], {}
    import humancheck as HC
    wr = HC.Writer('pose-test ' + who)
    for i in range(n):
        u = i / FPS
        HC.frame_begin()
        img, kind = WHO[who](u)
        wr.frame(u, HC.frame_end(u))
        what[kind] = what.get(kind, 0) + 1
        rgb = img.convert('RGB')
        rgb.save(os.path.join(tmp, '%04d.png' % i))
        if i % 12 == 0 and kind.startswith('body tool'):
            si = SS.stray_ink(rgb, sp)
            lt = SS.leg_tone_faults(rgb, sp)
            if si or lt:
                faults.append('%.2f s: %s%s' % (u, ('stray ink %s ' % si[:3]) if si else '', '; '.join(lt)))
            rgb.save(os.path.join(tmp, 'check_%04d.png' % i))
    mp4 = os.path.join(OUT, 'pose-test-%s.mp4' % who)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '23', mp4], check=True)
    wr.finish(mp4, notes=open(os.path.join(HERE, '..', 'notes', 'pose-test.md')).read())
    print(who, mp4, '%.1f MB' % (os.path.getsize(mp4) / 1e6), what, 'frames in', tmp)
    print('CHECKS', who, faults or 'clean')
    return mp4, faults


if __name__ == '__main__':
    args = sys.argv[1:]
    fr = int(args[args.index('--frames') + 1]) if '--frames' in args else None
    for w in (WHO if args[0] == 'all' else [args[0]]):
        render(w, fr)
