#!/usr/bin/env python3
"""shoulder_tower: people stacked on each other's shoulders, side-on, swaying (The Patriot 5, shot 4; learned in
notes/learn/shoulder-tower/lesson.md, Sam 27 Nov: "you will have to learn this pose").

MAP
  SEAT, KNEE, FOOT .. where a sitter rests on the man below, in the LOWER man's own units (neck base 0,0; x forward,
                      y down): his hips just behind and above the lower man's neck, his knees in front of the lower
                      man's upper chest, his feet at the lower man's belly (photo 01, side-on)
  sway(i, t, ...) ... each tier's lean from upright (radians): the column pivots about the base's feet and every tier
                      follows a little later and a little further (overlapping action)
  Tower(men) ........ the stack: tiers(t) works out every man's frame, legs and hands; draw(img, cam, t) draws them
  layers ............ each man drawn three times (core; + near leg; + near arm) on his own canvas and split by
                      difference, so the layers interleave between men: upper cores, then lower cores (the lower man's
                      head goes in front of the sitter's belly), then every near leg (over the lower man's neck and
                      chest), then every near arm (the lower man's hand over the sitter's shin). Each man's layers turn
                      about his pivot (the base: his feet; the rest: their hips) by his sway
  faults(tw, t) ..... the joins measured: base soles on the ground, hips on the shoulders, hands on the shins,
                      the stack's weight over the base's feet, no leg stretched
  practice(out) ..... the grey practice clip (Kind: practice): eight men against a wall with a window; still(out):
                      the joins at full size

    python3 source/shoulder_tower.py clip OUT.mp4 [--secs 4] [--n 8]
    python3 source/shoulder_tower.py still OUT.png
    python3 source/shoulder_tower.py check
"""
import math
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import people as PK          # noqa: E402
import people_parts as PP    # noqa: E402

B, V = PP.B, PP.V

# ------------------------------------------------------------------------------------------------ the seat
SEAT_UP = 52.0            # sitter's hip joints this far above the lower man's neck base (seated on the shoulders)
SEAT = (-163.0, -52.0)     # sitter's hip joint: behind the neck (his crotch against the back of the head), on the shoulders
KNEE_POLE = 0.55          # how far up the knee is pushed (thighs forward over the shoulders, not hanging)
FOOT = (15.0, 212.0)      # sitter's ankle: tucked back under the lower man's arm, at the side of his chest (a
#                           cheerleader's shoulder sit: with our big heads, feet at the belly stood on the head below)
LEG_OUT = 150.0           # sitter's feet apart: the shins round the outside of the lower man's chest, his own units
GRIP = 0.8               # where the lower man holds the shin (0 knee .. 1 ankle)
BEND = 46.0               # the base's knees bent (soles this far up from a straight stand): the weight shows
HEAD_TIP = 25.0            # a lower man's head tipped forward by the seat pressing it (degrees)
BALANCE_ARMS = ()        # tiers that let go with the near hand at the sway's ends (none: Sam, 27 Nov, "I don't like the
#                           hand thrusting"; both hands stay on the shins, the sway reads from the column and the top man)
TOP_LEAN = 30.0           # the top man leans in to look through the window
LEAN = 18.0                # every man tipped a little forward at the hips, so the seat (behind his neck) comes back over
#                           his own hips: the column stays straight over the base's feet (SEAT x = -450 sin LEAN)
CLIP_LIMIT = 0.04         # share of a head allowed to overlap the body above (the seat pressing on it)
KEY = ((255, 0, 255), (0, 255, 0), (0, 128, 255), (255, 128, 0))   # mask colours: top, sleeve, trousers, shoes


def column_seat():
    """The seat's place behind the lower man's neck that keeps the column straight: his lean brings his neck
    forward by exactly this, so each man's hips sit over the hips below (the weight stays over the base's feet)."""
    return (-(V.HIP_Y + SEAT_UP) * math.tan(math.radians(LEAN)), -SEAT_UP)


def seat_at(p):
    """A point given in the lower man's upright units (forward, down from the neck), carried by his lean."""
    x, y, z = V.leaned((0.0, p[1], p[0]), LEAN)
    return (z, y)


def unlean(p3, lean):
    """A hand target seen in his own (leaned) units, back in the torso's frame before the lean (arm_to takes that)."""
    L = math.radians(lean)
    x, y, z = p3
    dy = y - V.HIP_Y
    return x, V.HIP_Y + dy * math.cos(L) - z * math.sin(L), dy * math.sin(L) + z * math.cos(L)


def balance(i, t):
    """How far man i's near hand is out (0 on the shin .. 1 thrown out), eased, near the sway's far ends."""
    if i not in BALANCE_ARMS:
        return 0.0
    peak = abs(sway(i, 0.5 + 0.07 * i))
    u = (abs(sway(i, t)) / peak - 0.72) / 0.22
    u = min(1.0, max(0.0, u))
    return round(5 * u * u * (3 - 2 * u)) / 5           # six positions (each drawn once, reused)


def sway(i, t, amp=0.011, period=2.0, lag=0.07, grow=0.22):
    """Tier i's lean from upright (radians, + forward): the base's lean about his feet, each tier above a little later
    and further (a whip, not a stick). amp 0.016 rad at the base: the top man moves about 0.2 m either way."""
    return amp * (1 + grow * i) * math.sin(2 * math.pi * (t - lag * i) / period)


def _rot(p, a):
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


class Frame:
    """A man's own units (neck base 0,0; x forward, y down) -> world, turned by `a` about his pivot."""
    def __init__(self, k, pivot_local, pivot_world, a):
        self.k, self.pl, self.pw, self.a = k, pivot_local, pivot_world, a

    def W(self, p):
        d = _rot(((p[0] - self.pl[0]) * self.k, (p[1] - self.pl[1]) * self.k), self.a)
        return (self.pw[0] + d[0], self.pw[1] + d[1])

    def L(self, w):
        d = _rot((w[0] - self.pw[0], w[1] - self.pw[1]), -self.a)
        return (d[0] / self.k + self.pl[0], d[1] / self.k + self.pl[1])


class CropCam:
    """A small canvas of its own (one man's layer): world units are pixels at zoom 1."""
    def __init__(self, w, h):
        self.z = self.s = 1.0
        self.w, self.h = w, h

    def P(self, x, y):
        return x * B.SS, y * B.SS

    def S(self, v):
        return v * B.SS


class Tower:
    def __init__(self, men, ground, s, top_hands=None):
        """men: person descriptions, base first. ground: world point under the base's feet. s: scale (as views.person)
        for a 1.78 m man; each man scales by his own height. top_hands(j, frame, t): the top man's arms (else held up
        for balance)."""
        self.men, self.ground, self.s = men, ground, s
        self.top_hands = top_hands
        self.k = [s * m.get('height', 1.78) / 1.78 for m in men]

    # ---------------------------------------------------------------------------------------- the poses
    def frames(self, t):
        """Every man's frame at time t (base first)."""
        fr = []
        for i in range(len(self.men)):
            a = sway(i, t)
            if i == 0:
                fr.append(Frame(self.k[0], (0.0, 928.0 - BEND), self.ground, a))
            else:
                fr.append(Frame(self.k[i], (0.0, V.HIP_Y), fr[i - 1].W(seat_at(column_seat())), a))
        return fr

    def tiers(self, t):
        n = len(self.men)
        fr = self.frames(t)
        js = []
        for i, sp in enumerate(self.men):
            j = V.standing(sp)
            j['hand'] = {}
            j['lean'] = LEAN
            if i == 0:
                for sd, sg in (('L', -1), ('R', 1)):
                    j['foot' + sd] = (sg * 70.0, V.ANKLE_Y - BEND, 14.0 + (18.0 if sd == 'L' else -12.0))
                    j['knee_pole' + sd] = (0.1 * sg, 0.0, 1.0)
            else:
                f = fr[i].L(fr[i - 1].W(seat_at(FOOT)))         # the lower man's belly in my own units
                for sd, sg in (('L', -1), ('R', 1)):
                    j['foot' + sd] = (sg * LEG_OUT, f[1], f[0])
                    j['knee_pole' + sd] = (0.25 * sg, -KNEE_POLE, 1.0)
            if i < n - 1:
                j['head_lean'], j['bent_neck'] = HEAD_TIP, True      # bowed under the seat; the neck bends with it
            js.append(j)
        info = []
        for i, j in enumerate(js):
            kn = {}
            for sd in 'LR':
                knee, _ = V.ik3(j['hip' + sd], j['foot' + sd], V.THIGH, V.SHIN, j['knee_pole' + sd])
                kn[sd] = knee
            info.append(kn)
        for i, j in enumerate(js):            # each man with someone on him grips that man's shins
            if i < n - 1:
                up, kn = js[i + 1], info[i + 1]
                for sd, sg in (('L', -1), ('R', 1)):
                    g = tuple(kn[sd][c] + (up['foot' + sd][c] - kn[sd][c]) * GRIP for c in range(3))
                    w = fr[i].L(fr[i + 1].W((g[2], g[1])))       # that shin point in my units
                    x = g[0] * self.k[i + 1] / self.k[i]
                    grip = unlean((x + sg * 10.0, w[1], w[0] - 6.0), LEAN)
                    u = balance(i, t) if sd == 'L' else 0.0
                    if u > 0:                                    # lets go and throws the hand out the way he is
                        back = 1 if sway(i, t) < 0 else -1       # falling from, then grabs the shin again
                        out = (-170.0, 40.0, back * 330.0)
                        tgt = tuple(a + (b - a) * u for a, b in zip(grip, out))
                        V.arm_to(j, sd, tgt, 'down', 'fist' if u > 0.5 else 'grip')
                    else:
                        V.arm_to(j, sd, grip, 'down', 'grip')
            elif self.top_hands:
                self.top_hands(j, fr[i], t)
            else:
                for sd, sg in (('L', -1), ('R', 1)):
                    V.arm_to(j, sd, (sg * 230.0, -60.0 + 40 * sg, 60.0 * sg), 'out', 'fist')
        return fr, js, info

    # ---------------------------------------------------------------------------------------- the layers
    def _canvas(self, k):
        w, h = int(900 * k) + 40, int(1300 * k) + 40
        return CropCam(w, h), (w, h), (int(450 * k) + 20, int(330 * k) + 20)   # neck placed here on its canvas

    def _render(self, sp, j, k, legs='both', near_arm=True, t=0.0, key=False):
        """legs: 'both', 'far' (near hidden), 'near' (far hidden), 'none'. key: flat key colours (for the masks)."""
        cam, (w, h), (nx, ny) = self._canvas(k)
        img = Image.new('RGBA', (w * B.SS, h * B.SS), (0, 0, 0, 0))
        jj = dict(j)
        jj['behind'] = set(j.get('behind', set()))
        jj['hide_legs'] = {'both': set(), 'far': {'L'}, 'near': {'R'}, 'none': {'L', 'R'}}[legs]
        if not near_arm:                                         # tucked behind his own body (hidden by it)
            jj['elL'], jj['wrL'] = (-100.0, 270.0, -10.0), (-100.0, 440.0, -20.0)
            jj['behind'].add('L')
            jj['hand'] = dict(j.get('hand', {}), L='fist')
        q = dict(sp, bottom=min(sp.get('bottom', V.JACKET), 470))
        if key:
            q.update(jacket=KEY[0], shirt=KEY[0], sleeve=KEY[1], trousers=KEY[2], shoe=KEY[3], shoes=KEY[3])
        V.person(img, cam, nx, ny, k, q, t, 90, jj)
        return img, (nx, ny)

    def man_layers(self, i, sp, j, t):
        """His core (far leg, body, head, far arm), near leg and near arm as three layers, and two masks for the
        clipping check: his head (and hat) and his body. The layer masks come from renders in flat key colours (a
        near leg over the far leg, or a sleeve over a jacket of the same colour, would otherwise leave only
        outlines); the pixels from the real renders."""
        k = self.k[i]
        R = lambda **kw: np.asarray(self._render(sp, j, k, t=t, **kw)[0])
        core, (nx, ny) = self._render(sp, j, k, legs='far', near_arm=False, t=t)
        k0 = R(legs='none', near_arm=False, key=True)
        k1 = R(legs='near', near_arm=False, key=True)
        k2 = R(legs='none', near_arm=True, key=True)
        leg_px = R(legs='near', near_arm=False)
        arm_px = R(legs='both', near_arm=True)
        m_leg = np.any(k0 != k1, axis=2, keepdims=True)
        m_arm = np.any(k0 != k2, axis=2, keepdims=True)
        leg = np.where(m_leg, leg_px, 0).astype(np.uint8)
        arm = np.where(m_arm, arm_px, 0).astype(np.uint8)
        rgb = k0[..., :3].astype(int)
        torso = np.all(np.abs(rgb - KEY[0]) < 40, axis=2) & (k0[..., 3] > 0)
        keyed = np.zeros_like(torso)
        for c in KEY:
            keyed |= np.all(np.abs(rgb - c) < 40, axis=2)
        head = (k0[..., 3] > 0) & ~keyed
        neck_px = int((ny + 10 * k) * B.SS)                      # head, hair and hat: above his neck base
        head[neck_px:] = False
        body = torso.copy()
        body[:int((ny + 30 * k) * B.SS)] = False                 # his body (the jacket), below the collar
        feet = np.all(np.abs(k1[..., :3].astype(int) - KEY[3]) < 40, axis=2) & m_leg[..., 0]   # his near shoe
        mk = lambda m: Image.fromarray((m * 255).astype(np.uint8), 'L')
        return dict(core=core, leg=Image.fromarray(leg, 'RGBA'), arm=Image.fromarray(arm, 'RGBA'),
                    head=mk(head), body=mk(body), feet=mk(feet), o=(nx, ny))

    def _key(self, i, t):
        """Which of man i's drawings can be reused at time t (None: draw him afresh). Only the sway changes between
        frames, and that is a turn of his finished layers; the top man (his hand stays on the sill) and the two who
        throw an arm out are drawn per position."""
        n = len(self.men)
        if i == n - 1:
            return None
        if i in BALANCE_ARMS:
            return (i, balance(i, t), sway(i, t) < 0 if balance(i, t) > 0 else None)
        return (i,)

    def draw(self, img, cam, t, cache=None):
        """Draw the tower at time t on img (a B.canvas). Returns (frames, joints, knees); self.clips holds the
        clipping check's findings for this frame (a head pushed into the body of the man sitting on it)."""
        fr, js, info = self.tiers(t)
        n = len(self.men)
        cache = {} if cache is None else cache
        parts, masks = [], []
        for i in range(n):
            key = self._key(i, t)
            L = cache.get(key) if key else None
            if L is None:
                L = self.man_layers(i, self.men[i], js[i], t)
                if key:
                    cache[key] = L
            nx, ny = L['o']
            k = self.k[i]
            pl = fr[i].pl
            pvx, pvy = (nx + pl[0] * k) * B.SS, (ny + pl[1] * k) * B.SS     # his pivot on his own canvas
            pw = cam.P(*fr[i].pw)
            deg = -math.degrees(fr[i].a)
            off = (int(round(pw[0] - pvx)), int(round(pw[1] - pvy)))
            turn = lambda lay: lay.rotate(deg, resample=Image.BICUBIC, center=(pvx, pvy))
            parts.append([(turn(L[nm]), off) for nm in ('core', 'leg', 'arm')])
            masks.append({nm: (turn(L[nm]), off) for nm in ('head', 'body', 'feet')})
        for i in reversed(range(n)):          # cores: the top man first, so each lower head goes over the sitter
            img.alpha_composite(*_clip(img, *parts[i][0]))
        for i in range(n):
            img.alpha_composite(*_clip(img, *parts[i][1]))
        for i in range(n):
            img.alpha_composite(*_clip(img, *parts[i][2]))
        self.clips = []
        self.alpha = np.zeros((img.height, img.width), bool)     # where the tower is (the wall check reads it)
        for i in range(n):
            for lay, off in parts[i]:
                a = lay.getchannel('A')
                self.alpha |= _world(img, a, off)
        for i in range(n - 1):                # a head may touch the seat above it, never sink into that man's body
            h, b = _world(img, *masks[i]['head']), _world(img, *masks[i + 1]['body'])
            area = h.sum()
            over = (h & b).sum()
            if area and over / area > CLIP_LIMIT:
                self.clips.append(f'{t:.2f}s man {i + 1}\'s head {100 * over / area:.0f}% inside man {i + 2}\'s body')
        from PIL import ImageFilter
        for i in range(n):                    # nobody's shoe on, or touching, anybody else's head (reads as a kick)
            hm, ho = masks[i]['head']         # the head grown by a few pixels: a shoe resting on the hair counts
            h = _world(img, hm.filter(ImageFilter.MaxFilter(4 * B.SS + 1)), ho)
            for m in range(n):
                if m != i:
                    over = (h & _world(img, *masks[m]['feet'])).sum()
                    if over > 2 * B.SS * B.SS:          # any touch: a shoe on a head reads as a kick
                        self.clips.append(f'{t:.2f}s man {m + 1}\'s foot over man {i + 1}\'s head ({over} px)')
        return fr, js, info


def _world(img, m, off):
    """A turned mask placed on the frame (a boolean array the frame's size)."""
    w = Image.new('L', img.size, 0)
    lay, o = _clip(img, m, off)
    w.paste(lay, o)
    return np.asarray(w) > 127


def _clip(img, lay, off):
    """alpha_composite needs the layer inside the image: crop what falls outside."""
    x, y = off
    l, tp = max(0, -x), max(0, -y)
    r, b = min(lay.width, img.width - x), min(lay.height, img.height - y)
    if r <= l or b <= tp:
        return Image.new('RGBA', (1, 1), (0, 0, 0, 0)), (0, 0)
    return lay.crop((l, tp, r, b)), (x + l, y + tp)


# ------------------------------------------------------------------------------------------------ the checks
def faults(tw, t):
    """The joins, measured in world units: base soles on the ground, each sitter's hips on the shoulders, each hand on
    its shin, no leg stretched, the stack's weight over the base's feet (a foot's length either way)."""
    fr, js, info = tw.tiers(t)
    out = []
    n = len(js)
    for i, j in enumerate(js):
        for sd in 'LR':
            d = math.dist(j['hip' + sd], j['foot' + sd])
            if d > (V.THIGH + V.SHIN) * 0.995:
                out.append(f'{t:.2f}s man {i + 1}: {sd} leg stretched ({d:.0f} of {V.THIGH + V.SHIN})')
        if i < n - 1 and not (i in BALANCE_ARMS):
            for sd in 'LR':
                if j['hand'].get(sd) == 'grip':
                    tgt_ok = V.reach_ok(j, sd, (j['wr' + sd][0], j['wr' + sd][1], j['wr' + sd][2]), 'grip')
                    if not tgt_ok:
                        out.append(f'{t:.2f}s man {i + 1}: {sd} hand cannot reach the shin')
    sole = fr[0].W((0.0, 928.0 - BEND))
    if abs(sole[1] - tw.ground[1]) > 1.0:
        out.append(f'{t:.2f}s base off the ground by {sole[1] - tw.ground[1]:.1f}')
    # weight over the feet: every man's middle (his hips; the base: half way up), weighted by his mass (height)
    xs, ws = [], []
    for i in range(n):
        mid = fr[i].W((0.0, V.HIP_Y * (0.6 if i else 0.5)))
        xs.append(mid[0])
        ws.append(tw.men[i].get('height', 1.78) ** 3)
    cx = sum(x * w for x, w in zip(xs, ws)) / sum(ws)
    foot = 150.0 * tw.k[0]                    # a shoe's length about the ankle line
    if abs(cx - tw.ground[0]) > foot * 0.5:
        out.append(f'{t:.2f}s weight {cx - tw.ground[0]:+.0f} px off the base\'s feet (limit {foot * 0.5:.0f})')
    return out


# ------------------------------------------------------------------------------------------------ the practice scene
WALL = (178, 170, 160)
WALL_D = (150, 142, 132)
NIGHT = (34, 40, 62)
GROUND = (62, 64, 70)
CELL = (24, 22, 26)


def practice_men(n=8):
    PK.install(PK.load('brexit-is-done'))      # the crowd pack's heads (never the old bald default head)
    men, i = [], 0
    while len(men) < n:
        m = PK.pooled(i, 'london')
        i += 1
        if m.get('figure') in V.WOMAN_LEGS or m.get('hat_c'):   # men only; no peaked caps (a bowed head turned
            continue                                              # the cap into a black blob; the film's men wear
            #                                                       balaclavas)
        men.append(m)
    assert not any(PK.head_faults(m) for m in men)
    return men


def scene(img, cam, wall_x, sill_y, top_y):
    """Night outside a prison wall seen edge-on (cut through at the window): the wall a band on the right, the cell's
    dark through the window opening, bars seen end-on."""
    p = B.Pen(img, cam)
    p.poly([(0, 0), (1080, 0), (1080, 1920), (0, 1920)], NIGHT, None)
    gy = 1800
    p.poly([(0, gy), (1080, gy), (1080, 1920), (0, 1920)], GROUND, None)
    p.line([(0, gy), (1080, gy)], (40, 42, 48), 3)
    wt = 150                                   # wall thickness on screen
    p.poly([(wall_x, -10), (1100, -10), (1100, gy), (wall_x, gy)], WALL, INK_W, 3)
    p.poly([(wall_x + wt, -10), (1100, -10), (1100, gy), (wall_x + wt, gy)], CELL, None)   # the cell beyond, cut
    p.poly([(wall_x, top_y), (wall_x + wt, top_y), (wall_x + wt, sill_y), (wall_x, sill_y)], CELL, INK_W, 3)
    p.poly([(wall_x - 14, sill_y), (wall_x + wt, sill_y), (wall_x + wt, sill_y + 18), (wall_x - 14, sill_y + 18)],
           WALL_D, INK_W, 3)
    for bx in (wall_x + 40, wall_x + 70):      # the bars, end on, in the opening
        p.poly([(bx, top_y), (bx + 10, top_y), (bx + 10, sill_y), (bx, sill_y)], (70, 70, 76), INK_W, 2)
    for yy in range(int(sill_y + 60), gy, 64):  # brick courses on the cut face
        p.line([(wall_x, yy), (wall_x + wt, yy)], WALL_D, 2)
    for yy in range(40, int(top_y) - 20, 64):
        p.line([(wall_x, yy), (wall_x + wt, yy)], WALL_D, 2)


INK_W = (30, 28, 30)


def practice_tower(n=8, s=0.35):
    men = practice_men(n)
    gx = 440
    tw = Tower(men, (gx, 1800.0), s)
    wall_x = int(gx + 520 * tw.k[0])                  # clear of every knee and hat brim through the sway

    def top_hands(j, fr, t):               # the top man leans in to the window: near hand on the sill's lip,
        j['lean'] = TOP_LEAN               # far arm out behind for balance, against the sway
        lip = fr.L((wall_x - 8, sill_of(tw) - 2))
        V.arm_to(j, 'L', unlean((-70.0, lip[1], lip[0]), TOP_LEAN), 'down', 'palm')
        a = sway(n - 1, t) / 0.03                        # about -1 .. 1 through the sway
        V.arm_to(j, 'R', (150.0, 40.0 - 100 * a, -190.0 + 40 * a), 'out', 'fist')
    tw.top_hands = top_hands
    return tw, wall_x


def sill_of(tw):
    """The window sill: at the top man's chest when he sits upright (his head and shoulders in the opening)."""
    return tw.frames(0.0)[-1].W((0.0, 150.0))[1]


def frame_at(tw, wall_x, t, sill_y=None, top_y=None, cache=None):
    B.SS = 2
    img = B.canvas(NIGHT)
    cam = B.Cam(1.0, 540, 960)
    sill = sill_y if sill_y is not None else sill_of(tw)
    top = top_y if top_y is not None else sill - 330 * tw.k[-1] * 1.4
    scene(img, cam, wall_x, sill, top)
    tw.draw(img, cam, t, cache)
    x0 = int(cam.P(wall_x + 3, 0)[0])                 # nothing through the wall (the top man's hand rests on the sill lip)
    inside = int(tw.alpha[:, x0:].sum())
    if inside > 30 * B.SS * B.SS:
        tw.clips.append(f'{t:.2f}s the tower goes {inside // (B.SS * B.SS)} px into the wall')
    return img.resize((1080, 1920), Image.LANCZOS).convert('RGB')


def clip(out, secs=4.0, n=8, fps=12):
    """The practice clip: 12 drawings a second, each man's drawings reused while only the sway turns them, the frames
    split in runs across the processors. Returns the joins' and the clipping check's findings."""
    tmp = tempfile.mkdtemp()
    nf = int(secs * fps)
    tw, _ = practice_tower(n)
    probs = [p for f in range(nf) for p in faults(tw, f / fps)]
    from multiprocessing import Pool
    w = min(4, os.cpu_count() or 1)
    runs = [(n, fps, list(range(r, nf, w)), tmp) for r in range(w)]
    with Pool(w) as pool:
        for c in pool.map(_run, runs):
            probs += c
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(tmp, '%04d.png'),
                    '-vf', 'fps=24', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', out], check=True)
    return probs


def _run(a):
    n, fps, frames, tmp = a
    tw, wall_x = practice_tower(n)
    cache, clips = {}, []
    for f in frames:
        frame_at(tw, wall_x, f / fps, cache=cache).save(os.path.join(tmp, f'{f:04d}.png'))
        clips += tw.clips
    return clips


def main(argv):
    cmd = argv[1] if len(argv) > 1 else 'check'
    if cmd == 'clip':
        probs = clip(argv[2])
        print('\n'.join(probs) or 'joins: no faults')
    elif cmd == 'still':
        tw, wall_x = practice_tower()
        frame_at(tw, wall_x, float(argv[3]) if len(argv) > 3 else 0.5).save(argv[2])
        print('\n'.join(tw.clips) or 'clipping: none')
    elif cmd == 'check':
        tw, _ = practice_tower()
        probs = [p for k in range(48) for p in faults(tw, k / 12)]
        print('\n'.join(probs) or 'joins: no faults')


if __name__ == '__main__':
    main(sys.argv)
