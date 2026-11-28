#!/usr/bin/env python3
"""walking_boat: a small orange inflatable walked along on its crew's legs, the legs through holes cut in its floor,
side-on, left to right (The Patriot 5, shot 8; learned in notes/learn/walking-boat/lesson.md).

MAP
  Boat(men, s, ground_y, x0) .. the boat and its crew: two rows of four, staggered (the near row in front of the far)
  Boat.pose(t) ........ every man's walk (moves.gait, each at his own moment: out of step), the boat's height and
                        nose-up/down tip (the best-fit line through the men's pushes, lowered until no leg is stretched),
                        each man's frame (turned with the boat) and his feet on the ground (planted feet stay put)
  Boat.draw(img, t) ... far tube, far row, near row (body + legs), the floor's sag, the torn hole lips, near tube,
                        the near row's hands on the tube. Each man's layers (shoulder_tower's key-colour split) are drawn
                        once per drawing in the step cycle and slid on: the whole boat repeats every cycle
  faults(bt, t) ....... the joins measured: planted feet still and on the ground, no leg stretched, both thighs inside
                        their hole for the whole stride, every far-row head showing between the near row
  practice: clip(out) / still(out): the practice clip (Kind: practice) on a plain night ground; the joins at full size

    python3 source/walking_boat.py clip OUT.mp4 [secs]
    python3 source/walking_boat.py still OUT.png [t]
    python3 source/walking_boat.py check
"""
import math
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import moves as MV            # noqa: E402
import shoulder_tower as ST   # noqa: E402  (the layer split, frames, practice men)
from ink import INK, curve    # noqa: E402

B, V = ST.B, ST.V
UPM = 1.0 / V.M_PER_UNIT      # person units per metre

ORANGE = (240, 116, 34)
ORANGE_D = (196, 86, 22)      # the far tube, in the boat's own shade
ORANGE_L = (255, 170, 100)
FLOOR = (128, 66, 34)         # the soft floor's underside
ROPE = (60, 44, 40)
FLAP = (150, 80, 42)           # a cut flap, its cut face catching a little light

FPS = 12                      # drawings a second (output doubled to 24)
SPS = 2.0                     # steps a second: short, quick, sheepish steps; the boat repeats every 2/SPS s
STEP = 0.25                   # step length (m): 0.5 m/s
GAIT = 'stroll'
BEND = 22.0                   # every knee a little bent (person units): the boat rides a touch below standing hips
AMP = 2.6                     # each man's push at mid-step, times the gait's own hip rise (the boat's bob and tip)
CROTCH = 40.0                 # the floor's top sits this far below the shortest man's hip joints (person units)
ROW_GAP = 0.70                # m between the two rows (the near row 0.35 m in from the near tube)
SPACING = 0.56                # m between men in a row; the far row sits half a place further forward
HOLE = 0.23                   # m: each hole's half width along the boat: both thighs through the whole stride (0.15 m
#                             let the thigh through the floor at the stride's ends: the check measured 0.22 needed)
SHIFT = 0.0                   # m: the crew sits this far back of the boat's middle (the bow sweeps up; the floor
#                             ends before it, so the front man's legs come out of the floor, never under the tube)
PHASES = (0.00, 0.41, 0.77, 0.18, 0.58, 0.93, 0.29, 0.66)   # each man's moment in his step: out of step
HEAD_TIP = 14.0               # sheepish: heads bowed (bent_neck), shoulders hunched
HUNCH = 7.0


def _rot(p, a):
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def _dress(sp):
    """The pose extras a film's man brings with him (sp['_dress']: body_props, head_props, props, kit), copied so a
    pose never shares a list with another drawing."""
    return {k: (list(v) if isinstance(v, list) else v) for k, v in sp.get('_dress', {}).items()}


class Boat:
    def __init__(self, men, s, ground_y, x0, speed=None):
        """men: 8 person descriptions (near row first 4, far row last 4). s: scale for a 1.78 m man (as views.person).
        ground_y: the near row's ground line (world px). x0: the boat's middle at t=0 (world px)."""
        self.men, self.s, self.G, self.x0 = men, s, ground_y, x0
        self.ppm = s * UPM                                     # px per metre at a 1.78 m man's scale
        self.v = (speed or SPS * STEP) * self.ppm              # px a second
        self.tw = ST.Tower(men, (0, 0), s)                     # its renderer: the key-colour layer split
        self.k = self.tw.k
        kmin = min(self.k)
        n = len(men)
        self.row = [0 if i < n // 2 else 1 for i in range(n)]
        half = n // 2
        self.u = [((i % half) - (half - 1) / 2 + (-0.25 if self.row[i] == 0 else 0.25)) * SPACING * self.ppm
                  - SHIFT * self.ppm for i in range(n)]
        e = V.ELEV * self.ppm                                  # px a metre nearer sits lower
        self.dE = [0.0 if r == 0 else -ROW_GAP * e for r in self.row]
        self.dE_near_tube, self.dE_far_tube = 0.35 * e, -(ROW_GAP + 0.35) * e
        # each man's hip joint, rigid in the boat (px above the floor's top): taller men stand higher in it
        self.vh = [-((928 - V.HIP_Y - BEND) * (k - kmin) + CROTCH * kmin) for k in self.k]
        self.rest = (928 - V.HIP_Y - BEND - CROTCH) * kmin    # floor top above the ground at rest (px)
        self.Rt = 0.16 * self.ppm                              # tube radius
        self.vc = -0.75 * self.Rt                              # tube centre line (floor top: v = 0)
        self.Ls, self.Lb = 1.3 * self.ppm, 1.45 * self.ppm    # stern and bow ends of the tubes from the middle
        self.cache = {}

    # ------------------------------------------------------------------------------------------ the motion
    def X(self, t):
        return self.x0 + self.v * t

    def gaits(self, t):
        return [MV.gait(sp, t + PHASES[i] * 2.0 / SPS, GAIT, stride=STEP * UPM, steps_per_s=SPS)
                for i, sp in enumerate(self.men)]

    def pose(self, t):
        """(cx, cy, a, js, frames, feet): the boat's middle and tip, and every man's pose in his own frame."""
        gs = self.gaits(t)
        cx = self.X(t)
        xs, want, nat = [], [], []
        for i, g in enumerate(gs):
            k = self.k[i]
            nat_hip = self.G - (928 - V.HIP_Y - g['bob']) * k               # highest his legs allow (screen y)
            hip = self.G - (928 - V.HIP_Y - BEND - AMP * g['bob']) * k      # where he pushes it
            xs.append(cx + self.u[i])
            want.append(hip - self.vh[i])
            nat.append(nat_hip - self.vh[i])
        xa = np.array(xs) - cx
        b, a0 = np.polyfit(xa, np.array(want), 1)
        line = a0 + b * xa
        a0 += max(0.0, float(np.max(np.array(nat) - line)))                # never a stretched leg
        cy, ang = a0, math.atan(b)
        js, frames, feet = [], [], []
        for i, g in enumerate(gs):
            k = self.k[i]
            hw = self.W(cx, cy, ang, self.u[i], self.vh[i])
            fr = ST.Frame(k, (0.0, V.HIP_Y), hw, ang)
            j = dict(g)
            j.update(_dress(self.men[i]))                  # a film's own clothes and kit on the man (sp['_dress'])
            ft = {}
            for sd, sg in (('L', -1), ('R', 1)):
                fx, fy, fz = g['foot' + sd]
                lift = V.ANKLE_Y - fy - g['bob']
                w = (cx + self.u[i] + fz * k, self.G - (928 - V.ANKLE_Y) * k - lift * k)
                ft[sd] = w
                z, y = fr.L(w)
                j['foot' + sd] = (fx, y, z)
            self.arms(i, j)
            j['lean'] = HUNCH
            j['head_lean'], j['bent_neck'] = HEAD_TIP, True
            js.append(j)
            frames.append(fr)
            feet.append(ft)
        return cx, cy, ang, js, frames, feet

    def W(self, cx, cy, a, u, v):
        """A point of the boat (u along it, v down from the floor's top, px) in the world (the near row's plane)."""
        d = _rot((u, v), a)
        return (cx + d[0], cy + d[1])

    def arms(self, i, j):
        """The near row grip the near tube's top with the near hand (drawn over the tube); the far hand and the far
        row's hands rest down inside the boat, hidden by the tube."""
        k = self.k[i]
        st = V.standing(self.men[i])
        for sd in 'LR':
            j['sh' + sd], j['el' + sd], j['wr' + sd] = st['sh' + sd], st['el' + sd], st['wr' + sd]
        j['hand'] = {'L': 'fist', 'R': 'fist'}
        if self.row[i] == 0:
            top = self.vc - self.Rt + self.dE_near_tube                     # the tube's top (px from the floor top)
            y = V.HIP_Y + (top - self.vh[i]) / k - 4.0 - V.ELEV * 200.0     # in his units (the hand is 200 nearer)
            V.arm_to(j, 'L', ST.unlean((-200.0, y, 95.0), HUNCH), 'down', 'grip')
            V.arm_to(j, 'R', ST.unlean((120.0, y + 30, 70.0), HUNCH), 'down', 'grip')

    # ------------------------------------------------------------------------------------------ the drawing
    def layers(self, i, t, j, fr):
        """Man i's three layers, turned with the boat, and where his hip joint is on them. Reused every cycle."""
        key = (i, round((t * SPS / 2.0) % 1.0 * FPS * 2 / SPS) % int(FPS * 2 / SPS))
        L = self.cache.get(key)
        if L is None:
            raw = self.tw.man_layers(i, self.men[i], j, t)
            nx, ny = raw['o']
            k = self.k[i]
            pv = (nx * B.SS, (ny + V.HIP_Y * k) * B.SS)
            deg = -math.degrees(fr.a)
            L = {nm: raw[nm].rotate(deg, resample=Image.BICUBIC, center=pv) for nm in ('core', 'leg', 'arm')}
            L['pv'] = pv
            self.cache[key] = L
        return L

    def tube(self, cx, cy, a, dE, fill, img, cam, detail=True):
        """One side tube (the near one, or the far one shifted up by depth), its bow swept up, stern cones behind."""
        Rt, vc, Ls, Lb, m = self.Rt, self.vc, self.Ls, self.Lb, self.ppm
        pts = [(-Ls - 0.16 * m, vc - 0.05 * Rt), (-Ls, vc - Rt), (-0.4 * m, vc - Rt), (Lb - 0.55 * m, vc - 1.05 * Rt),
               (Lb - 0.12 * m, vc - 1.5 * Rt), (Lb + 0.12 * m, vc - 1.75 * Rt), (Lb + 0.3 * m, vc - 1.2 * Rt),
               (Lb + 0.22 * m, vc - 0.1 * Rt), (Lb - 0.1 * m, vc + 0.75 * Rt), (Lb - 0.6 * m, vc + Rt),
               (-0.4 * m, vc + Rt), (-Ls, vc + Rt), (-Ls - 0.14 * m, vc + 0.55 * Rt)]
        wp = [self.W(cx, cy, a, u, v + dE) for u, v in pts]
        p = B.Pen(img, cam)
        p.poly(curve(wp, 4), fill, INK, 3.0)
        if not detail:
            return
        hi = [self.W(cx, cy, a, u, vc - 0.62 * Rt + dE) for u in np.linspace(-Ls + 0.05 * m, Lb - 0.5 * m, 12)]
        p.line(hi, ORANGE_L, 0.22 * Rt)                                        # the light along the tube's top
        sh = [self.W(cx, cy, a, u, vc + 0.72 * Rt + dE) for u in np.linspace(-Ls + 0.05 * m, Lb - 0.6 * m, 12)]
        p.line(sh, ORANGE_D, 0.3 * Rt)                                         # the shade along its underside
        for u in (-Ls + 0.02 * m, Lb - 0.62 * m):                              # chamber seams
            p.line([self.W(cx, cy, a, u, vc - Rt + dE), self.W(cx, cy, a, u, vc + Rt + dE)], ORANGE_D, 2.4)
        n = 7                                                                  # the grab line in loops along the side
        us = np.linspace(-Ls + 0.15 * m, Lb - 0.75 * m, n + 1)
        for k0, k1 in zip(us, us[1:]):
            q = [self.W(cx, cy, a, u, vc - 0.05 * Rt + 0.28 * Rt * math.sin(math.pi * (u - k0) / (k1 - k0)) + dE)
                 for u in np.linspace(k0, k1, 6)]
            p.line(q, ROPE, 2.6)
            p.ell(*self.W(cx, cy, a, k0, vc - 0.05 * Rt + dE), 4, 4, ROPE, None)

    def sag_bottom(self, u):
        """The soft floor's lowest edge (px below the floor top): sagging most where the men stand in it."""
        base = self.vc + self.Rt + 0.03 * self.ppm
        bump = sum(math.exp(-((u - self.u[i]) / (0.16 * self.ppm)) ** 2) for i in range(len(self.men))
                   if self.row[i] == 0)
        return base + 0.02 * self.ppm * bump

    def floor_ends(self):
        """Where the soft floor's sag starts and ends along the boat (px): between the stern and where the bow's
        underside starts to sweep up."""
        return -self.Ls + 0.05 * self.ppm, self.Lb - 0.2 * self.ppm

    def floor(self, cx, cy, a, img, cam):
        Rt, vc, m = self.Rt, self.vc, self.ppm
        us = np.linspace(*self.floor_ends(), 40)
        top = [self.W(cx, cy, a, u, vc + 0.4 * Rt) for u in us]
        bot = [self.W(cx, cy, a, u, self.sag_bottom(u)) for u in us[::-1]]
        B.Pen(img, cam).poly(top + bot, FLOOR, INK, 2.6)

    def lip(self, i, cx, cy, a, img, cam):
        """Man i's hole, cut in the floor: the dark opening round his thighs, a cut flap folded down at each end of the
        hole and short torn teeth along its front edge (drawn over his legs, so they read as coming out of it)."""
        m, u0 = self.ppm, self.u[i]
        hw = HOLE * m
        rnd = np.random.default_rng(31 + i)
        p = B.Pen(img, cam)
        sb = self.sag_bottom
        for sg in (-1, 1):                     # the two end flaps: a triangle of floor cut on two sides, hanging
            e = u0 + sg * hw
            w0, w1 = e - sg * (0.09 + 0.02 * rnd.random()) * m, e + sg * 0.01 * m
            tip = (e + sg * (0.01 + 0.02 * rnd.random()) * m, sb(e) + (0.11 + 0.03 * rnd.random()) * m)
            p.poly([self.W(cx, cy, a, w0, sb(w0) - 2), self.W(cx, cy, a, w1, sb(w1) - 2), self.W(cx, cy, a, *tip)],
                   FLAP, INK, 2.4)
        us = np.linspace(u0 - hw + 0.07 * m, u0 + hw - 0.07 * m, 7)
        edge = [self.W(cx, cy, a, u, sb(u) - 2) for u in us]
        teeth = []
        for q, u in enumerate(us):
            teeth.append(self.W(cx, cy, a, u, sb(u) + (0.008 + 0.016 * rnd.random()) * m))
            if q < len(us) - 1:
                um = (u + us[q + 1]) / 2
                teeth.append(self.W(cx, cy, a, um, sb(um) + 0.004 * m))
        p.poly(edge + teeth[::-1], FLOOR, INK, 2.0)

    def draw(self, img, cam, t):
        """The boat and its crew at time t."""
        cx, cy, a, js, frames, feet = self.pose(t)
        lay = []
        for i in range(len(self.men)):
            L = self.layers(i, t, js[i], frames[i])
            hp = cam.P(*frames[i].pw)
            off = (int(round(hp[0] - L['pv'][0])), int(round(hp[1] + self.dE[i] * B.SS - L['pv'][1])))
            lay.append((L, off))

        def put(i, nm):
            L, off = lay[i]
            img.alpha_composite(*ST._clip(img, L[nm], off))
        n = len(self.men)
        far = [i for i in range(n) if self.row[i] == 1]
        near = [i for i in range(n) if self.row[i] == 0]
        self.tube(cx, cy, a, self.dE_far_tube, ORANGE_D, img, cam, detail=False)
        for i in far:
            put(i, 'core')
        for i in far:
            put(i, 'leg')
            put(i, 'arm')
        for i in near:
            put(i, 'core')
        for i in near:
            put(i, 'leg')
        self.floor(cx, cy + 0.0, a, img, cam)
        for i in near:
            self.lip(i, cx, cy, a, img, cam)
        self.tube(cx, cy, a, self.dE_near_tube, ORANGE, img, cam)
        for i in near:
            put(i, 'arm')
        return cx, cy, a, js, frames, feet


# ------------------------------------------------------------------------------------------------ the checks
def faults(bt, t, dt=1.0 / 48):
    """The joins, measured: a planted foot stays put and on the ground (two moments apart), no leg stretched, both
    thighs inside their hole the whole stride."""
    out = []
    f0, f1 = bt.floor_ends()
    for i in range(len(bt.men)):                   # every hole inside the floor (else the legs come out under the tube)
        if bt.u[i] - HOLE * bt.ppm < f0 or bt.u[i] + HOLE * bt.ppm > f1:
            out.append(f'man {i + 1}: his hole runs past the end of the floor (his legs come out under the tube)')
    cx, cy, a, js, frames, feet = bt.pose(t)
    _, _, _, js2, _, feet2 = bt.pose(t + dt)
    for i, j in enumerate(js):
        k = bt.k[i]
        for sd in 'LR':
            d = math.dist(j['hip' + sd], j['foot' + sd])
            if d > (V.THIGH + V.SHIN) * 0.995:
                out.append(f'{t:.2f}s man {i + 1}: {sd} leg stretched ({d:.0f} of {V.THIGH + V.SHIN})')
            if j['planted'][sd] and js2[i]['planted'][sd]:
                slide = math.dist(feet[i][sd], feet2[i][sd])
                if slide > 0.6:
                    out.append(f'{t:.2f}s man {i + 1}: planted {sd} foot slides {slide:.1f} px')
                if abs(feet[i][sd][1] - (bt.G - (928 - V.ANKLE_Y) * k)) > 0.6:
                    out.append(f'{t:.2f}s man {i + 1}: planted {sd} foot off the ground')
            # the thigh where it crosses the floor's lowest edge, in the boat's own frame: inside the hole
            hip = frames[i].W((j['hip' + sd][2], j['hip' + sd][1]))
            knee, _ = V.ik3(j['hip' + sd], j['foot' + sd], V.THIGH, V.SHIN, (0.0, 0.0, 1.0))
            kn = frames[i].W((knee[2], knee[1]))
            hb = _rot((hip[0] - cx, hip[1] - cy), -a)
            kb = _rot((kn[0] - cx, kn[1] - cy), -a)
            vb = bt.sag_bottom(bt.u[i])
            if kb[1] > vb > hb[1]:
                ux = hb[0] + (kb[0] - hb[0]) * (vb - hb[1]) / (kb[1] - hb[1])
                half = 48 * k                                       # the thigh's half width there
                if abs(ux - bt.u[i]) + half > HOLE * bt.ppm:
                    out.append(f'{t:.2f}s man {i + 1}: {sd} thigh {abs(ux - bt.u[i]) + half - HOLE * bt.ppm:.0f} px '
                               f'outside its hole (through the floor)')
    return out


# ------------------------------------------------------------------------------------------------ the practice scene
NIGHT = (30, 36, 58)
NIGHT_LOW = (44, 50, 74)
GROUND = (52, 54, 60)
GROUND_D = (40, 42, 48)


def practice_men():
    """Eight men from the crowd pack (men only, no peaked caps), between 1.70 and 1.84 m: one boat, one floor."""
    ST.PK.install(ST.PK.load('brexit-is-done'))
    men, i = [], 0
    while len(men) < 8:
        m = ST.PK.pooled(i, 'london')
        i += 1
        if m.get('figure') in V.WOMAN_LEGS or m.get('hat_c') or not 1.70 <= m.get('height', 1.78) <= 1.84:
            continue
        men.append(m)
    assert not any(ST.PK.head_faults(m) for m in men)
    return men


S = 0.42
GROUND_Y = 1250.0


def practice_boat(x0=200.0):
    return Boat(practice_men(), S, GROUND_Y, x0)


_SHADOW = {}


def scene(img, cam, cx, bt):
    p = B.Pen(img, cam)
    p.poly([(0, 0), (1080, 0), (1080, GROUND_Y - 60), (0, GROUND_Y - 60)], NIGHT, None)
    p.poly([(0, GROUND_Y - 60), (1080, GROUND_Y - 60), (1080, 1920), (0, 1920)], GROUND, None)
    p.poly([(0, GROUND_Y + 160), (1080, GROUND_Y + 160), (1080, 1920), (0, 1920)], GROUND_D, None)
    p.line([(0, GROUND_Y - 60), (1080, GROUND_Y - 60)], (36, 38, 46), 3)
    sh = _SHADOW.get(B.SS)
    if sh is None:                         # the boat's soft shadow on the ground (one sprite, slid along)
        w, h = int(2.9 * bt.ppm * B.SS), int(0.45 * bt.ppm * B.SS)
        sh = Image.new('RGBA', (w + 80 * B.SS, h + 80 * B.SS), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse((40 * B.SS, 40 * B.SS, w + 40 * B.SS, h + 40 * B.SS), (10, 10, 16, 110))
        sh = sh.filter(ImageFilter.GaussianBlur(18 * B.SS))
        _SHADOW[B.SS] = sh
    c = cam.P(cx - SHIFT * bt.ppm, GROUND_Y - 0.1 * bt.ppm)
    img.alpha_composite(*ST._clip(img, sh, (int(c[0] - sh.width / 2), int(c[1] - sh.height / 2))))


def frame_at(bt, t):
    B.SS = 2
    img = B.canvas(NIGHT)
    cam = B.Cam(1.0, 540, 960)
    scene(img, cam, bt.X(t), bt)
    bt.draw(img, cam, t)
    return img.resize((1080, 1920), Image.LANCZOS).convert('RGB')


def _run(a):
    frames, tmp = a
    bt = practice_boat()
    for f in frames:
        frame_at(bt, f / FPS).save(os.path.join(tmp, f'{f:04d}.png'))
    return len(frames)


def clip(out, secs=4.0):
    """The practice clip: each worker draws whole step-cycle positions (so its reused layers stay its own)."""
    tmp = tempfile.mkdtemp()
    nf = int(secs * FPS)
    cyc = int(FPS * 2 / SPS)
    bt = practice_boat()
    probs = [p for f in range(nf) for p in faults(bt, f / FPS)]
    from multiprocessing import Pool
    w = min(4, os.cpu_count() or 1)
    runs = [([f for f in range(nf) if (f % cyc) % w == r], tmp) for r in range(w)]
    with Pool(w) as pool:
        pool.map(_run, runs)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.png'),
                    '-vf', 'fps=24', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', out], check=True)
    return probs


def main(argv):
    cmd = argv[1] if len(argv) > 1 else 'check'
    if cmd == 'clip':
        probs = clip(argv[2], float(argv[3]) if len(argv) > 3 else 4.0)
        print('\n'.join(probs) or 'joins: no faults')
    elif cmd == 'still':
        bt = practice_boat()
        frame_at(bt, float(argv[3]) if len(argv) > 3 else 1.5).save(argv[2])
    elif cmd == 'check':
        bt = practice_boat()
        probs = [p for f in range(48) for p in faults(bt, f / FPS)]
        print('\n'.join(probs) or 'joins: no faults')


if __name__ == '__main__':
    main(sys.argv)
