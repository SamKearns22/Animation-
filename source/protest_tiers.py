#!/usr/bin/env python3
"""Protest Tiers: the film (moves stage, chat 13, 15 Nov). Four European protests, each tier worse; 4.0 s a tier,
hard cuts, 16 s + the 1.6 s sign-off (finish.py). Everyone is a Glimpse (rule 24). Plan: notes "Moves plan (chat 12)".

MAP (rule 61)
  setup ............. NAME, HAS, FPS, DUR, SHOTS, HOOK, KEEP_CLEAR, SHOT_CAST, HEADLINES; scene_of(t) -> (tier, lt)
  sprites ........... crowd members drawn once with the cast's own rig at a reference scale, cached on disk
                      (~/.cache/protest-tiers-sprites, keyed by the cast file's hash), resized per depth; ground anchor
  field ............. field(tier, x, d, t) -> (dx, dd): sway, surge, the T3 split; one function for every crowd
  actors ............ actors(tier, lt) -> [Actor]: every live-drawn (acted) person: name, x, d, pose, yaw; picture()
                      draws them, scene() turns them into the audit's solids (one list, so the audit sees the drawing)
  t1 ................ crowd_t1 (thousands of backs, keys wave front to back, heads turn), knot, firework string,
                      bursts over the line, the line's pace, tear-gas haze
  t2 ................ runners, the shutter haul + pry bar, the road-sign swing, glass whole/starred/gone, shards and
                      glints, two slide through, the A-board kicked over, the near-pavement crowd (signs jab, phones),
                      freeze at 3.2, the blue strobe wash 3.0-4.0 (last light layer)
  t3 ................ crowd mass (tricolours, CGT banners), front line throws stones, the canister and the gas over
                      Marianne's base, smoke from car and bikes, the truck drives in, the jet, the split left
  t4 ................ mopeds + RPG, the rocket trail, the hit, the helicopter spiral (behind the ministry: sets' `under`
                      hook), shield line buckles and breaks, melee, two Molotovs into the bank, the fireball, backlight
  picture/overlay ... painting back, people (far to near), front layer, effects, light layers; headlines on top
  checks / main ..... checks(), audits(); stills, clip, final (film_engine.render)

    python3 source/protest_tiers.py stills OUT_DIR T [T ...]
    python3 source/protest_tiers.py final OUT.mp4 [--small] [--span T0 T1]
    python3 source/protest_tiers.py check
"""
import hashlib
import math
import os
import sys
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from PIL.PngImagePlugin import PngInfo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import protest_tiers_cast as C       # noqa: E402
import moves                         # noqa: E402
import protest_tiers_sets as S       # noqa: E402
import islamocommunism_set as IS     # noqa: E402
from ed import INK                   # noqa: E402

B, V = C.B, C.V
W, H = 1080, 1920
CAM2 = None                          # the 2D person camera (identity at SS 1); made in _cam2()

# ================================================================================================= setup
NAME = 'protest_tiers'
FILM = 'protest-tiers'
NOTES = os.path.join(os.path.dirname(HERE), 'notes', 'protest-tiers.md')
HAS = {'people', 'effects', 'props'}
FPS = 12
# round 1 (Sam R4, 15 Nov): tiers 4 / 6 / 8 / 10 s, then the end scene's three shots (notes "## Round 1 plan")
# round 2 (A2, Sam: Albania 2-3 s longer, new action at full speed): T4 10 -> 12.5 s; the end scene starts later
LENS = (('t1', 6.0), ('t2', 8.5), ('t3', 8.0), ('t4', 12.5), ('ea', 2.4), ('eb', 2.8), ('ec', 2.4))
TIERS = ('t1', 't2', 't3', 't4')
SHOTS, _t = [], 0.0
for _n, _l in LENS:
    SHOTS.append((_n, _t, round(_t + _l, 3)))
    _t = round(_t + _l, 3)
DUR = _t
BLACK_AT = DUR
START = {n: t0 for n, t0, _ in SHOTS}
J3 = 1.95                    # T3: the water cannon's whole beat moved this much later (truck in 3.85, jet on 4.5)


def at(tier, lt):
    """Film time of a moment in a shot (check tables are written in shot time, so a re-time moves them too)."""
    return round(START[tier] + lt, 3)
HOOK = ('European protests, ranked', {'y': 1300, 'until': 2.0, 'tilt': -7})   # Sam O3 (16 Nov): Blessed's diagonal, gone at 2 s
def caption_at(t):
    """Rule 62: the end scene's lines captioned (the voices: notes "## Round 1 plan"; stand-ins until Sam records)."""
    if t < START['ea']:
        return None
    import subtitles
    return subtitles.caption_at(voices(), t)


HEADLINES = {'t1': ('SPAIN', 'Barcelona, Passeig de Gràcia'), 't2': ('GERMANY', 'Frankfurt, Berliner Straße'),
             't3': ('FRANCE', 'Paris, Place de la République'), 't4': ('ALBANIA', 'Tirana, Ministry of Education')}
# chat 16: patterns of the acted names the audit sees (the group words matched no one); the crowds, T1's police line
# and the mopeds are sprites the audit does not list (seen on every frame of their shot)
INTENSITY = {'t1': 2, 't2': 4, 't3': 8, 't4': 11}      # Sam R3 / Q2: Albania reads 11 from its first frame
INTENSITY_RED = (220, 40, 40)                             # the blue-strobe-safe red of the T4 fire
INTENSITY_COL = {'t1': (60, 200, 80), 't2': (255, 150, 30), 't3': (230, 40, 40), 't4': (150, 0, 10)}   # Sam O1 (16 Nov)
INTENSITY_AT = 2.0                                        # Sam O1: the number appears 2 s into the scene, with a ding
SHOT_CAST = {'t1': [], 't2': ['hauler*', 'swinger', 'runner*', 'crowd*'], 't3': ['front*', 'crs*'],
             't4': ['policia*', 'rioter*']}
SIREN = os.path.join(HERE, 'audio', 'power-crime-siren.mp3')


def scene_of(t):
    for n, t0, t1 in SHOTS:
        if t < t1:
            return n, t - t0
    n, t0, _ = SHOTS[-1]
    return n, t - t0


def shot_of(t):
    return scene_of(t)[0]


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def _cam2():
    global CAM2
    B.SS = 1
    if CAM2 is None:
        CAM2 = B.Cam(1.0, 540, 960)
    return CAM2


# ================================================================================================= sprites
SPR_DIR = os.path.join(os.path.expanduser('~/.cache'), 'protest-tiers-sprites')
S_REF = 0.32                         # reference scale: a 1.75 m person ~370 px
FEET = 928.0                         # neck base to sole, in person units (cast.draw keeps the soles at y + 928 s)


@lru_cache(None)
def _cast_hash():
    h = hashlib.md5()
    for f in ('protest_tiers_cast.py', 'people.py', 'people_parts.py', 'views.py'):
        p = os.path.join(HERE, f)
        if os.path.exists(p):
            h.update(open(p, 'rb').read())
    h.update(b'v1')
    return h.hexdigest()[:10]


def make_person(kind, i=0, tier='t1', force=None):
    if kind in C.TOURIST_DRESS:                     # round 1: granny, seller, the tourists
        return C.tourist(kind)
    if kind == 'officer':
        return C.officer(force)
    if kind == 'rioter':
        return C.rioter(seed=force, tier=tier) if force else C.rioter()
    return C.marcher(i, tier)


def make_pose(sp, state, u=0.0, t=0.0, force=None):
    """The cast's pose by name, plus the film's own: 'stand', 'placard:TEXT:R,G,B[:lift]', 'flag:KIND', 'keys'."""
    if state == 'stand':
        return V.standing(sp)
    # chat 31: the skips over mid-throw and mid-swing (chats 14, 25) are gone: they were sized to one build, so other
    # builds and blends still folded the elbow shut (3 stopped drawings in animatic 2); the cast's pose now swings the
    # hand round clear of the shoulder (protest_tiers_cast._clear_of_shoulder) for every build
    if state.startswith('placard:'):
        parts = state.split(':')
        j = C.pose(sp, 'placard')
        lift = float(parts[3]) if len(parts) > 3 else 0.0
        if lift:                                   # signs jab on the beat: both hands up together
            x = j['shR'][0] * 0.75
            V.arm_to(j, 'R', (x, -60.0 - lift, 230.0), 'down')
            V.arm_to(j, 'L', (x, 70.0 - lift, 230.0), 'down')
        board = tuple(int(v) for v in parts[2].split(',')) if parts[2] else (250, 246, 232)
        w = 1.0 if len(parts[1]) > 9 else 0.6
        j['props'] = [C.placard(j, text=parts[1], board=board, w=w)]
        j['grip'] = ('L', 'R')
        return j
    if state == 'run':                                     # the 'run' gait: 0 of 24 phases fail at three-quarter
        return moves.gait(sp, t, 'run')
    if state.startswith('flag:'):
        return C.pose(sp, 'flag', force=state.split(':')[1])
    return C.pose(sp, state, u, t, force)


def sprite(kind, i, tier, state, yaw, force=None):
    """(RGBA image at S_REF, (ax, ay) the ground point under the neck in the image). Drawn once, cached on disk."""
    key = f'{_cast_hash()}-{kind}-{i}-{tier}-{state}-{yaw}-{force}'.replace('/', '_').replace(' ', '_').replace(':', '~')
    key = hashlib.md5(key.encode()).hexdigest()[:16]
    path = os.path.join(SPR_DIR, key + '.png')
    if os.path.exists(path):
        im = Image.open(path)
        im.load()
        ax, ay = (float(v) for v in im.text['anchor'].split(','))
        return im, (ax, ay)
    cam = _cam2()
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sp = make_person(kind, i, tier, force)
    j = make_pose(sp, state, force=force)
    C.draw(img, cam, 540, 700, S_REF, sp, j, yaw, None if kind != 'officer' else 'officer')
    box = img.getbbox() or (0, 0, 1, 1)
    im = img.crop(box)
    ax, ay = 540 - box[0], 700 + FEET * S_REF - box[1]
    os.makedirs(SPR_DIR, exist_ok=True)
    info = PngInfo()
    info.add_text('anchor', f'{ax},{ay}')
    tmp = path + f'.{os.getpid()}.tmp'
    im.save(tmp, format='PNG', pnginfo=info)
    os.replace(tmp, path)
    return im, (ax, ay)


@lru_cache(maxsize=6000)
def _scaled(kind, i, tier, state, yaw, force, q):
    im, (ax, ay) = sprite(kind, i, tier, state, yaw, force)
    k = q / 400.0
    w, h = max(1, int(round(im.width * k))), max(1, int(round(im.height * k)))
    return im.resize((w, h), Image.LANCZOS), (ax * k, ay * k)


def paste(img, kind, i, tier, state, yaw, gx, gy, s, force=None, dark=0.0):
    """One crowd member standing on screen point (gx, gy) at person scale s."""
    q = max(4, int(round(s / S_REF * 400)))
    im, (ax, ay) = _scaled(kind, i, tier, state, yaw, force, q)
    if dark:
        im = _darken(im, dark)
    img.paste(im, (int(round(gx - ax)), int(round(gy - ay))), im)


@lru_cache(maxsize=6000)
def _top(kind, i, tier, state, yaw, force, q):
    """The sprite's highest drawn point relative to its ground anchor (where raised keys are): (dx, dy)."""
    im, (ax, ay) = _scaled(kind, i, tier, state, yaw, force, q)
    a = np.asarray(im)[..., 3]
    ys = np.nonzero(a.max(1) > 128)[0]
    if not len(ys):
        return 0.0, 0.0
    y = ys[0]
    xs = np.nonzero(a[y] > 128)[0]
    return float(xs.mean()) - ax, float(y) - ay


def glint(img, x, y, r, amt=1.0):
    """A four-point star: the sparkle off a raised key ring (T1) or a shard (T2)."""
    dr = ImageDraw.Draw(img)
    c = (255, 252, 230)
    w = max(1, int(r / 5))
    dr.line([(x - r, y), (x + r, y)], fill=c, width=w)
    dr.line([(x, y - r * 1.3), (x, y + r * 1.3)], fill=c, width=w)
    dr.ellipse((x - w * 1.5, y - w * 1.5, x + w * 1.5, y + w * 1.5), fill=(255, 255, 255))


def _darken(im, k):
    a = np.asarray(im).astype(np.float32)
    a[..., :3] *= (1 - k)
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def scale_at(cam, d):
    return cam.ppm(d) * C.M


# ================================================================================================= field
def field(tier, x, d, t, seed=0.0):
    """How a crowd member at (x, d) is displaced at tier time t: (dx, dd) metres. Sway is one slow wave rolling
    through the crowd; surges and the T3 split are added per tier."""
    ph = 0.35 * x + 0.21 * d + seed
    sway = 0.07 * math.sin(2 * math.pi * 0.55 * t + ph)
    dx, dd = sway, 0.04 * math.sin(2 * math.pi * 0.5 * t + ph * 1.3)
    if tier == 't1':
        dd += 0.5 * ease(t / 1.5)                         # swaying forward toward the line
    elif tier == 't3':
        dx += 0.55 * ease((t - 0.2) / 0.8)                 # the surge behind the front line (toward the police)
        if t > 2.6 + J3 and d < 30:                        # the jet: the crowd breaks into two currents, out left
            u = t - 2.6 - J3 - 0.02 * max(0.0, x + 2)
            dx -= (2.6 if d < 18 else 1.4) * max(0.0, u) ** 1.2
            dd += (-1.5 if d < 18 else 2.0) * ease(u / 1.4)
    elif tier == 't4':
        lag, amt = 0.22 * math.sin(seed * 2.3), 1 + 0.18 * math.sin(seed * 3.1)   # round 2 (F9): each their own
        dx += amt * (1.2 * ease((t - 0.8 - lag) / 1.2) + 0.9 * ease((t - 2.0 - lag) / 1.0))   # the surge, then through
    return dx, dd


# ================================================================================================= actors
class Actor:
    """One live-drawn person: kind ('officer', 'rioter', 'marcher'), at (x, d) metres facing yaw, in a pose."""
    def __init__(self, name, kind, x, d, yaw, state='stand', u=0.0, t=0.0, i=0, force=None, extra=None, clip=None,
                 dark=0.0, tier='t1', lift=0.0, head=None):
        if state.startswith('run') and 75 <= abs(yaw) <= 105:   # chat 14: the rig's run fails its arm guard side on
            yaw = 115 if yaw > 0 else -115                     # (14-17 of 24 phases, either way): three-quarter, away
        self.name, self.kind, self.x, self.d, self.yaw = name, kind, x, d, yaw
        self.state, self.u, self.t, self.i, self.force = state, u, t, i, force
        self.extra, self.clip, self.dark, self.tier = extra, clip, dark, tier
        self.lift, self.head = lift, head           # round 1: off the ground (a vault, a jump), m; head yaw
        self.prop, self.prop_before = None, False   # round 1: a carried thing drawn with them: prop(img, cam, actor)
        self.mix = None                             # chat 29: (state, u, t, w): blend from that pose (w 0) to this one

    def blend(self, state, u=0.0, t=0.0, w=1.0):
        """Chat 29 (pre-flight: 107 teleports and snaps): pass from another pose into this one over a few frames."""
        if w < 1.0:
            self.mix = (state, u, t, max(0.0, w))
        return self

    def sp(self):
        if self.kind == 'rioter':                   # Sam O4: each rioter their own face, from their city's mix
            return make_person('rioter', self.i, self.tier, force=self.name)
        return make_person(self.kind, self.i, self.tier, self.force)

    def pose(self, sp):
        j = make_pose(sp, self.state, self.u, self.t, self.force)
        if self.mix:
            st, u, t, w = self.mix
            j = moves.mix_poses(make_pose(sp, st, u, t, self.force), j, ease(w))
            _resolve_mixed_arms(j, self.yaw)
        if self.extra:
            self.extra(j)
        return j


def _resolve_mixed_arms(j, yaw):
    """Chat 31 (Sam's note 1 on animatic 2, 'frames missing'): mixing two poses slides each joint straight across, so
    part-way from a run into a throw the arm came out the wrong length or folded back across the body (the guard
    stopped the drawing at T4 20.75 s). Each mixed arm is re-bent onto its mixed hand by the rig, the elbow pointing
    the way the mix put it (so it still looks like the blend); if the guard would still stop it as seen at this turn,
    the next elbow direction that it passes."""
    def seen(q):
        return C.V.project(C.V.leaned(q, j.get('lean', 0.0)), yaw)[0]
    for s in 'LR':
        sg = -1 if s == 'L' else 1
        sh, el, wr = (np.array(j[k + s][:3], float) for k in ('sh', 'el', 'wr'))
        pole = el - (sh + wr) / 2
        pole[0] = max(sg * pole[0], 0.35 * (np.linalg.norm(pole) or 1.0))   # the elbow out to his side, never across
        n = np.linalg.norm(pole)
        hand = C._clear_of_shoulder(j, s, wr)
        for p in ((tuple(pole / n),) if n > 1e-6 else ()) + ('down', 'out', 'front', 'back'):
            C.V.arm_to(j, s, hand, p, shape=j.get('hand', {}).get(s, 'fist'))
            try:
                C.F.audit_arm(*(seen(j[k + s]) for k in ('sh', 'el', 'wr')))
                break
            except Exception:
                continue


def draw_actor(img, cam, a):
    s = scale_at(cam, a.d)
    gx, gy = cam.p(a.x, a.d, getattr(a, 'lift', 0.0))
    sp = a.sp()
    j = a.pose(sp)
    if a.clip or a.dark:
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        C.draw(lay, _cam2(), gx, gy - FEET * s, s, sp, j, a.yaw, _kind(a), head=a.head)
        if a.dark:
            lay = _darken(lay, a.dark)
        if a.clip:
            m = Image.new('L', img.size, 0)
            ImageDraw.Draw(m).rectangle(a.clip, fill=255)
            al = np.minimum(np.asarray(lay.getchannel('A')), np.asarray(m))
            lay.putalpha(Image.fromarray(al))
        img.alpha_composite(lay)
    else:
        C.draw(img, _cam2(), gx, gy - FEET * s, s, sp, j, a.yaw, _kind(a), head=a.head)
    return j


def _kind(a):
    return a.kind if a.kind in ('officer', 'rioter') else None


def facing(yaw):
    r = math.radians(yaw)
    return (math.sin(r), -math.cos(r))


# ================================================================================================= T1
T1_LINE_D = 150.0      # chat 15: was 185; the line, container and knot come nearer so the beats read at phone size
T1_FRONT = 106.0       # the march's front rank (was 135): a clear stretch of lit road for the knot
T1_KEYS, T1_STEP, T1_HAZE = 3.0, 4.0, 4.2   # Sam S1 (16 Nov, T1 6 s): keys up at 3 s; the line's pace; the gas
# Sam S3 (16 Nov): no black bloc; fireworks lobbed out of the crowd's front ranks, high, at their own times, across
# the width: (launch time, x where thrown, x where it bursts, peak height above the line m, colour)
T1_ROCKETS = [(0.45, -3.0, -4.0, 5.5, (255, 90, 70)), (1.05, 2.5, 1.0, 6.3, (255, 250, 210)),
              (1.5, -6.5, -6.0, 5.0, (110, 255, 150)), (2.1, 5.5, 6.5, 5.9, (255, 200, 60)),
              (2.6, -1.0, 0.5, 6.7, (255, 120, 220)), (3.25, 7.5, 9.0, 5.0, (255, 90, 70)),
              (3.8, -5.0, -3.0, 6.3, (110, 220, 255)), (4.35, 1.5, 3.0, 5.5, (255, 250, 210)),
              (4.85, -8.0, -7.5, 5.9, (110, 255, 150)), (5.3, 4.0, 4.5, 6.7, (255, 200, 60))]
T1_FLY = 0.8                                        # seconds in the air


@lru_cache(None)
def crowd_t1():
    """The march: thousands of backs from 46 m to 156 m (the long lens: the frame is 7-25 m wide down there)."""
    cam = S.CAMS['t1']
    rng = np.random.default_rng(11)
    out = []
    for d in np.arange(46.0, T1_FRONT, 0.72):        # stops short: the gap shows the knot and the container
        x0 = (0 - cam.VX - 40) * d / cam.F
        x1 = (W - cam.VX + 40) * d / cam.F
        for x in np.arange(x0, x1, 0.62):
            xx = x + rng.uniform(-.2, .2)
            r = rng.uniform()
            # keys are the main thing; ~1% flags (Catalan and UGT), ~1.5% placards (chat 14: 5% read as a sea)
            state = ('keys' if r < .5 else 'flag:catalan' if r < .506 else 'flag:ugt' if r < .51 else
                     'placard' if r < .525 else 'stand')
            if state.startswith('flag') and d < 75:        # near flags filled a quarter of the frame: mid and far only
                state = 'keys'
            out.append(dict(x=xx, d=d + rng.uniform(-.25, .25), i=int(rng.integers(0, 16)), state=state,
                            ph=rng.uniform(0, 6.28), turn=rng.uniform(0, .35)))
    return out


T1_PLACARDS = ['VIVIENDA DIGNA:250,246,232', 'BAJAD ALQUILERES:210,40,40', 'CCOO:200,30,40', 'UGT:220,50,40',
               'GIRONA:250,246,232', 'TARRAGONA:240,220,120', 'LLEIDA:250,246,232', 'SINDICAT LLOGATERES:240,200,60']


def t1_people(img, lt):
    cam = S.CAMS['t1']
    # the police line across the far end (front on), one pace forward at T1_STEP; Sam S5 (16 Nov): a second rank two
    # paces (1.6 m) behind, each officer in a gap of the first; drawn first (further away)
    step = ease((lt - T1_STEP) / 0.4)
    bob = 9 * math.sin(math.pi * min(1, max(0, (lt - T1_STEP) / 0.4)))
    for rank, off, back in ((1, 0.85, 1.6), (0, 0.0, 0.0)):
        for k, x in enumerate(np.arange(-10.0 + off, 14.0, 1.7)):
            d = T1_LINE_D + back - 6.0 * step                 # chat 15: one long pace (6 m) so the step reads
            gx, gy = cam.p(x, d)
            paste(img, 'officer', 0, 't1', 'line', 0, gx, gy - bob, scale_at(cam, d), force='mossos')
    # the knot by the container (live), then the march (sprites), far to near
    for a in t1_actors(lt):
        draw_actor(img, cam, a)
    members = crowd_t1()
    for m in sorted(members, key=lambda m: -m['d']):
        dx, dd = field('t1', m['x'], m['d'], lt, m['ph'])
        x, d = m['x'] + dx, m['d'] + dd
        gx, gy = cam.p(x, d)
        if gx < -60 or gx > W + 60:
            continue
        state = m['state']
        if state == 'keys':                                # the key wave: from the front (far) back toward us
            if lt < T1_KEYS + (T1_FRONT - m['d']) / (T1_FRONT - 46) * 0.7:   # Sam S1: up at 3 s, half the crowd
                state = 'stand'
        elif state == 'placard':
            state = 'placard:' + T1_PLACARDS[m['i'] % len(T1_PLACARDS)]
        yaw = 180
        if lt > 1.3 + m['turn']:                           # heads turn to the bursts over the line (centre)
            yaw = 135 if gx < 470 else -135
        jig = -1 if (m['state'] == 'keys' and state == 'keys' and (int(lt * 12) + m['i']) % 2) else 0
        sc = scale_at(cam, d)
        paste(img, 'marcher', m['i'], 't1', state, yaw, gx, gy + jig, sc)
        if state == 'keys' and (int(lt * 12) + int(m['ph'] * 7)) % 3 == 0:     # chat 16 (hunt 2: no keys at phone size): every 3rd frame, bigger
            q = max(4, int(round(sc / S_REF * 400)))
            tx, ty = _top('marcher', m['i'], 't1', state, yaw, None, q)
            glint(img, gx + tx, gy + jig + ty + 2, max(5.0, 40 * sc))


def t1_actors(lt):
    return []                                      # Sam S3 (16 Nov): no black-clad knot in Spain


def _t1_actors_old(lt):
    out = []
    knot = [(-2.4, 123.0), (-1.5, 124.5), (-0.6, 122.5), (2.6, 124.0), (3.3, 122.8)]   # chat 15: was d 161
    for k, (x, d) in enumerate(knot):
        state, u, yaw = 'stand', 0.0, 180
        if k == 2:                                         # the firework string: wound up 0.5, flicked 0.85
            state, yaw = 'throw', 135
            u = 0.0 if lt < 0.5 else ease((lt - 0.55) / 0.3) if lt < 1.2 else 1.0
        extra = None
        if k == 3 and 1.5 < lt < 2.3:                      # one ducks at the bursts
            def extra(j):
                j['lean'] = 22
        out.append(Actor(f'hooded{k + 1}', 'rioter', x, d, yaw, state, u, extra=extra, tier='t1'))
    return out


def t1_fx(img, lt):
    cam = S.CAMS['t1']
    dr = ImageDraw.Draw(img)
    for k, (t0, xa, xb, peak, col) in enumerate(T1_ROCKETS):
        a = lt - t0
        if 0 <= a < 0.12:                                  # the throw: a spark in a hand over the front ranks
            hx, hy = cam.p(xa, T1_FRONT - 2.0, 2.3 + 2.0 * a)
            S.glow_disc(img, hx, hy, 34, (255, 210, 120), amt=.8)
            IS.ell(img, hx, hy, 6, 6, (255, 255, 235), None)
        if 0 <= a < T1_FLY:                                # the flight: a high arc, a fizzing head, a spark tail
            def pt(u):
                d = lerp(T1_FRONT - 2.0, T1_LINE_D + 2.0, u)
                z = lerp(2.3, 7.0, u) + 4 * peak * u * (1 - u)
                return cam.p(lerp(xa, xb, u), d, z)
            u = a / T1_FLY
            tail = [pt(max(0.0, u - q * 0.025)) for q in range(14)]
            for q in range(len(tail) - 1):
                dr.line([tail[q], tail[q + 1]], fill=(255, max(60, 230 - 12 * q), max(40, 150 - 9 * q)),
                        width=max(2, 8 - q // 2))
            hx, hy = tail[0]
            S.glow_disc(img, hx, hy, 44, (255, 200, 110), amt=.75)
            IS.ell(img, hx, hy, 7, 7, (255, 255, 235), None)
            rng = np.random.default_rng(int(lt * 100) + k)
            for _ in range(6):
                IS.ell(img, hx + rng.uniform(-18, 18), hy + rng.uniform(-8, 22), 2, 2, (255, 240, 180), None)
        b = a - T1_FLY                                     # the burst over the line
        if 0 <= b < 0.6:
            cx, cy = cam.p(xb, T1_LINE_D + 2.0, 7.0)
            r = 18 + 62 * ease(b / 0.3)
            fade = 1 - b / 0.6
            S.glow_disc(img, cx, cy, r * 1.6, col, amt=.6 * fade)
            if b < 0.07:
                S.glow_disc(img, cx, cy, 60, (255, 255, 255), amt=.8)
                IS.ell(img, cx, cy, 12, 12, (255, 255, 255), None)
            for n in range(16):
                ang = n * math.pi / 8 + k * 0.3
                r0, r1 = r * 0.4, r
                droop = 40 * b * b / 0.36
                ex, ey = cx + r1 * math.cos(ang), cy + r1 * math.sin(ang) + droop
                dr.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang) + droop * .5), (ex, ey)], fill=col, width=4)
                IS.ell(img, ex, ey, 4, 4, (255, 255, 240), None)
    # the tear-gas haze drifting left to right through the keys (3.0-4.0)
    if lt > T1_HAZE:
        haze(img, lt - T1_HAZE, [(cam.p(x, d, 1.6), 9 * cam.ppm(d)) for x, d in
                             ((-4, 128), (-1, 118), (2, 135), (5, 108), (-6, 100), (1, 92), (-3, 84))], 0.9,
             (232, 232, 222))


def haze(img, age, centres, speed, col, alpha=0.42, seed=3):
    """Soft drifting gas: blurred lumps on a quarter-size layer (cheap), fading in over 0.6 s."""
    q = 4
    lay = Image.new('L', (W // q, H // q), 0)
    dr = ImageDraw.Draw(lay)
    rng = np.random.default_rng(seed)
    for (x, y), r in centres:
        x += speed * age * 60
        for _ in range(3):
            ox, oy, rr = rng.uniform(-.6, .6) * r, rng.uniform(-.25, .25) * r, r * rng.uniform(.5, .9)
            dr.ellipse(((x + ox - rr) / q, (y + oy - rr * .45) / q, (x + ox + rr) / q, (y + oy + rr * .45) / q), fill=255)
    lay = lay.filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR)
    a = np.asarray(lay, np.float32)[..., None] / 255 * alpha * ease(age / 0.6)
    base = np.asarray(img.convert('RGB'), np.float32)
    out = base * (1 - a) + np.array(col, np.float32) * a
    img.paste(Image.fromarray(out.astype(np.uint8)).convert('RGBA'), (0, 0))


# ================================================================================================= T2
# Round 2 (Sam's G notes, 16 Nov; notes "## Round 2 notes"): 8.5 s, no freeze. Stones from off frame left hit the
# glass (0.3-1.1); the swinger, facing the glass, smashes it at T2_HIT; the haulers lift the shutter; the A-board is
# kicked across the pavement; the shop door (right of the window) is kicked open and four go in; two take a pistol
# each from the window; the four come back out of the door with stock and walk off left; the sirens at T2_WASH, and
# everyone keeps going.
T2_WIN = (174, 754, 786, 1089)
T2_END = 8.5
T2_WASH = 6.8                       # G1/G10: the blue at 6.8 s, the action carries on
T2_FREEZE = T2_END                  # G10: no freeze; the old name is kept by the audit tables as the shot's end
T2_HIT = 1.6                        # G3: the sign meets the glass
T2_DOOR = 2.45                      # G4: hauler1's foot on the door
DOOR_X0, DOOR_X1, DOOR_H = S.DOOR2
DOOR_C, FRONT_D = (DOOR_X0 + DOOR_X1) / 2, 14.0
T2_SW = (0.2, 12.7)                 # the swinger's mark (the sign's head reaches the glass at T2_HIT)
T2_STAR = (0.8, 1.92)               # where it meets the glass (x, height); chat 3: on the sign's head at T2_HIT
BOARD = (-0.7, 12.75)               # G7: the A-board, kicked at BOARD_KICK, lands at BOARD_LAND
BOARD_KICK, BOARD_LAND, BOARD_TO = 2.3, 2.8, (-0.15, 11.0)
# G2: stones thrown from off frame left and near: (hits the glass at, x, height)
T2_STONES = ((0.35, -1.4, 1.6), (0.5, 0.6, 2.0), (0.62, -0.4, 1.2), (0.8, 1.3, 1.7), (0.95, -1.0, 2.2), (1.1, 0.2, 1.4))
# G9 (FAZ 31 Oct: two weapons taken): who takes which pistol: (cubby column, row height, when it leaves its cubby)
TAKE = {'runner1': (6, 0.98, 2.95), 'runner2': (8, 1.35, 3.05)}
# G4/G5: the four who go in through the door come back out of it with stock: (in at, out at, lane, prop)
# chat 3: out 1 s apart in one lane clear of the wall and the swinger (0.5 s apart, they walked into each other)
DOOR_IN = {'hauler1': (2.75, 4.6, 13.4, 'crate'), 'hauler2': (3.15, 6.6, 13.4, 'crate'),
           'runner4': (3.5, 5.6, 13.4, 'boxes'), 'runner5': (3.75, 7.6, 13.4, 'boxes')}
WALK_OUT = 1.5                       # m/s: laden, a brisk walk off left along the shop front


def t2_state(lt):
    return dict(shutter=0.5 + 0.5 * ease((lt - 1.0) / 0.5),
                glass='whole' if lt < T2_HIT else 'starred' if lt < T2_HIT + 0.1 else 'gone',
                taken=tuple((i, z) for i, z, t in TAKE.values() if lt >= t), star=T2_STAR)


def door_angle(lt):
    """G4: degrees the door's leaf is open (0 shut): flung open by the kick, it bounces back a little off the rack."""
    if lt < T2_DOOR:
        return 0.0
    return 100 * ease((lt - T2_DOOR) / 0.2) - 14 * math.sin(math.pi * min(1.0, max(0.0, (lt - T2_DOOR - 0.2) / 0.5)))


def _keys(tt, keys):
    """keys [(t, x, d), ...] -> (x, d, i, u): where someone is at tt, moving at an even speed between keys; i is the
    segment (-1 before the first key, len - 1 after the last), u how far through it."""
    if tt <= keys[0][0]:
        return keys[0][1], keys[0][2], -1, 0.0
    for i in range(len(keys) - 1):
        t0, x0, d0 = keys[i]
        t1, x1, d1 = keys[i + 1]
        if tt < t1:
            u = (tt - t0) / (t1 - t0)
            return lerp(x0, x1, u), lerp(d0, d1, u), i, u
    return keys[-1][1], keys[-1][2], len(keys) - 1, 1.0


def _heading(keys, i):
    (_, x0, d0), (_, x1, d1) = keys[i], keys[i + 1]
    return math.degrees(math.atan2(x1 - x0, -(d1 - d0)))   # yaw: 0 toward us, 90 right, 180 away


DOOR_CLIP = None                     # the door's opening on screen (set once RF2 exists, below)


def _door_walk(name, tt):
    """G4: in through the door and, later, out of it with the stock and off left along the shop front. -> (x, d, yaw,
    state, inside) or None while they are in the shop."""
    t_in, t_out, lane, _ = DOOR_IN[name]
    if t_in <= tt < t_in + 0.45:                            # through the doorway, away from us
        d = lerp(13.35, 14.9, (tt - t_in) / 0.45)
        return DOOR_C, d, 180, 'run', d > FRONT_D - 0.2
    if t_in + 0.45 <= tt < t_out:
        return None
    a = tt - t_out
    if a < 0.9:                                             # stepping out toward us, laden
        d = lerp(14.9, lane, ease(a / 0.9))
        return DOOR_C, d, 0, 'carry_front', d > FRONT_D - 0.2
    b = a - 0.9
    k = min(1.0, b / 0.3)                                   # turning left, then walking off along the shop front
    x = DOOR_C - WALK_OUT * (b - 0.15) if k >= 1 else DOOR_C - WALK_OUT * 0.15 * k * k
    return x, lane, -115 * ease(k), 'carry_front', False


def t2_actors(lt):
    tt = lt
    out = []
    A = lambda *a, **k: out.append(Actor(*a, tier='t2', **k)) or out[-1]   # noqa: E731

    def run_keys(name, keys, after, **k):
        """Run along keys; once there, `after(i, u)` gives (yaw, state, u) for the time since the last key."""
        x, d, i, u = _keys(tt, keys)
        if 0 <= i < len(keys) - 1:
            return A(name, 'rioter', x, d, _heading(keys, i), 'run', t=tt, **k)
        if i < 0:
            return None
        yaw, st, uu = after(tt - keys[-1][0])
        return A(name, 'rioter', x, d, yaw, st, u=uu, t=tt, **k)

    # the haulers: sprint in, lever the shutter up (1.0-1.5), run to the door; hauler1 kicks it in (G4)
    for k, (xs, xh) in enumerate(((-3.8, -0.9), (-3.3, 0.9))):
        name = f'hauler{k + 1}'
        if tt >= DOOR_IN[name][0]:
            w = _door_walk(name, tt)
            if w:
                x, d, yaw, st, inside = w
                a = A(name, 'rioter', x, d, yaw, st, t=tt, clip=DOOR_CLIP if inside else None)
                if st == 'carry_front':
                    a.prop, a.prop_before = _carried(DOOR_IN[name][3]), abs(yaw) > 90
            continue
        wait = (DOOR_C, 13.3) if k == 0 else (3.6, 13.25)       # chat 3: hauler2 waits right of the door (hauler1 ran through him)
        keys = [(0.2, xs, 13.3 + 0.15 * k), (0.95 - 0.13 * k, xh, 13.3)]     # chat 3: hauler2 leads (he overtook through people)
        x, d, i, u = _keys(tt, keys)
        if i < len(keys) - 1:
            if i >= 0:
                A(name, 'rioter', x, d, 90, 'run', t=tt)
            continue
        if tt < 1.55:                                       # hauling the shutter up
            A(name, 'rioter', xh, 13.3, 180, 'haul')
            continue
        keys2 = [(1.55, xh, 13.3), (2.25 + 0.05 * k, *wait)]
        x, d, i, u = _keys(tt, keys2)
        if i == 0:
            A(name, 'rioter', x, d, _heading(keys2, 0), 'run', t=tt)
        elif k == 0:                                        # the kick: knee up 2.25, foot on the door at T2_DOOR
            uk = (tt - (T2_DOOR - 0.12)) / 0.3 * 0.5 + 0.0 if tt < T2_DOOR else 0.5 + (tt - T2_DOOR) / 0.3 * 0.5
            A(name, 'rioter', x, d, 180, 'kick' if tt > T2_DOOR - 0.25 else 'stand',
              u=min(1.0, max(0.0, uk)))
        elif tt > DOOR_IN[name][0] - 0.3:                   # chat 3: his dash to the door (he jumped there)
            v = (tt - DOOR_IN[name][0] + 0.3) / 0.3
            A(name, 'rioter', lerp(x, DOOR_C, v), lerp(d, 13.35, v), _heading([(0, x, d), (1, DOOR_C, 13.35)], 0), 'run', t=tt)
        else:                                               # waiting his turn, egging them on
            A(name, 'rioter', x, d, 160, 'throw', u=((tt - 2.25) * 1.6) % 1)
    # the swinger (G3): runs in, turns to the glass, winds up, the sign's head meets the glass at T2_HIT; swings on
    keys = [(0.15, -3.8, 11.9), (0.65, -0.4, 12.2), (0.85, *T2_SW)]     # chat 3: on his mark before the runners pass
    x, d, i, u = _keys(tt, keys)
    if 0 <= i < len(keys) - 1:
        A('swinger', 'rioter', x, d, _heading(keys, i), 'run_sign', t=tt)
    elif i >= 0:
        if tt < 1.35:
            us = 0.25 * ease((tt - 0.95) / 0.4)
        elif tt < T2_HIT:
            us = 0.25 + 0.3 * ease((tt - 1.35) / (T2_HIT - 1.35))    # chat 3: the head meets the glass at 0.55, high
        elif tt < 1.75:
            us = 0.55 + 0.45 * ease((tt - T2_HIT) / 0.15)
        elif tt < 3.85:                                     # knocks the teeth out of the frame: three more swings
            c = ((tt - 1.75) % 0.7) / 0.7
            us = 1 - 0.75 * math.sin(math.pi * c)
        else:                                               # then the sign up on his shoulder, bouncing to the chant
            us = lerp(1.0, 0.15, ease((tt - 3.85) / 0.5)) + 0.04 * math.sin(tt * 2 * math.pi * 1.1)
        a = A('swinger', 'rioter', x, d, 125, 'swing_face', u=us)     # chat 3: angled, so the sign lands beside him, not behind his back
        a.blend('run_sign', 0, tt, w=(tt - 0.95) / 0.25)
    # runner1, runner2 (G9): run in, throw stones into the shop, step up to the window and each take a pistol, then
    # walk off left with it held up
    for k, (xm, dm, xr, take_t) in enumerate(((1.05, 12.35, 0.95, TAKE['runner1'][2]),
                                               (1.75, 12.3, 1.7, TAKE['runner2'][2]))):
        name = f'runner{k + 1}'
        keys = [(0.45 + 0.1 * k, -3.8, 12.25 - 0.1 * k), (0.92 + 0.1 * k, 0.2, 11.75 - 0.1 * k),   # chat 3: in front of
                (1.1 + 0.1 * k, xm, dm)]                    # the swinger (they ran through him)
        x, d, i, u = _keys(tt, keys)
        if 0 <= i < len(keys) - 1:
            A(name, 'rioter', x, d, _heading(keys, i), 'run', t=tt + k * .1)
            continue
        if i < 0:
            continue
        t_up = take_t - 0.65                                # step up 0.3 s, reach 0.35 s, the pistol out at take_t
        if tt < t_up:
            A(name, 'rioter', xm, dm, 180, 'throw', u=((tt - 1.05) * 1.4 + k * .3) % 1.0)
            continue
        reach = 'reach_lo' if k == 0 else 'reach_hi'
        if tt < t_up + 0.3:
            v = ease((tt - t_up) / 0.3)
            a = A(name, 'rioter', lerp(xm, xr, v), lerp(dm, 13.45, v), 180, 'stand')
            a.blend('throw', 0.0, w=v * 3)
            continue
        if tt < take_t + 0.45:
            A(name, 'rioter', xr, 13.45, 180, reach, u=(tt - (t_up + 0.3)) / 0.35 if tt < take_t else 1 + (tt - take_t) / 0.45)
            continue
        lane = 11.8 - 0.2 * k                               # chat 3: clear of the swinger; back off the window, turn, walk off left
        keys2 = [(take_t + 0.45, xr, 13.45), (take_t + 0.95, xr - 0.3, lane), (take_t + 6.0, xr - 0.3 - 7.6, lane)]
        x, d, i, u = _keys(tt, keys2)
        yaw = lerp(180, -115, ease((tt - take_t - 0.45) / 0.5))
        a = A(name, 'rioter', x, d, yaw, 'gun_up', t=tt)
        a.blend(reach, 2.0, w=(tt - take_t - 0.45) / 0.3)
    # runner3 (G7): the A-board: a sprint in, three steps' run-up, a hard kick; then he throws stones into the shop
    keys = [(1.35, -3.6, 12.7), (1.85, -2.25, 12.7), (2.12, -1.5, 12.7)]
    x, d, i, u = _keys(tt, keys)
    if 0 <= i < len(keys) - 1:
        A('runner3', 'rioter', x, d, 90, 'run', t=tt)
    elif i >= 0:
        if tt < 2.62:
            A('runner3', 'rioter', x, d, 90, 'kick', u=min(1.0, (tt - 2.12) / 0.5))
        else:
            a = A('runner3', 'rioter', x, d, 160, 'throw', u=((tt - 2.62) * 1.3) % 1.0)
            a.blend('kick', 1.0, w=(tt - 2.62) / 0.25)
    # runner4, runner5: run in and wait by the door, egging it on; in after the haulers (G4)
    for k, (wx, wd, tin) in enumerate(((2.5, 12.3, 1.55), (3.0, 12.2, 1.7))):
        name = f'runner{k + 4}'
        if tt >= DOOR_IN[name][0]:
            w = _door_walk(name, tt)
            if not w:
                continue
            if w[2] == 180 and tt < DOOR_IN[name][0] + 0.45:
                pass
            x, d, yaw, st, inside = w
            a = A(name, 'rioter', x, d, yaw, st, t=tt, clip=DOOR_CLIP if inside else None)
            if st == 'carry_front':
                a.prop, a.prop_before = _carried(DOOR_IN[name][3]), abs(yaw) > 90
            continue
        keys = [(tin - 1.1, -3.6, 11.35 - 0.3 * k), (tin - 0.5, 0.3, 11.35 - 0.3 * k),   # chat 3: in front of the swinger
                (tin, wx, wd), (DOOR_IN[name][0], DOOR_C, 13.35)]
        x, d, i, u = _keys(tt, keys)
        if i in (0, 1) or (i == 2 and tt > DOOR_IN[name][0] - 0.3):
            ii = min(i, 2) if i < 2 else 2
            if i == 2:                                      # his dash to the door
                x, d = lerp(wx, DOOR_C, (tt - DOOR_IN[name][0] + 0.3) / 0.3), lerp(wd, 13.35, (tt - DOOR_IN[name][0] + 0.3) / 0.3)
            A(name, 'rioter', x, d, _heading(keys, ii), 'run', t=tt)
        elif i == 2:
            A(name, 'rioter', wx, wd, 150, 'throw', u=((tt - tin) * 1.5 + k * .4) % 1.0)
    # the crowd on the near pavement, seen from behind, all facing the store (chanting: signs jab on the beat)
    beat = abs(math.sin(math.pi * 2.2 * tt))
    # round 2 (G4: the camera moved right): the left side 0.2 m in; the right group out at the frame's edge, clear of the door (chat 3)
    crowd = [(-1.18, 7.8, 'placard:WAFFEN RAUS:250,246,232', 0), (-1.55, 8.9, 'phone', 1), (-1.4, 9.6, 'stand', 2),
             (2.3, 7.7, 'phone', 6), (2.95, 8.8, 'placard:GEN Z REGELT:240,220,60', 5), (3.2, 9.5, 'stand', 3)]
    for k, (x, d, st, i) in enumerate(crowd):
        if st.startswith('placard'):
            st = st + ':' + str(int(90 * beat))
        yaw = 180
        if st == 'phone':                                   # the phones swing round after the looters out the door
            yaw = 180 + (25 if x < 0 else 35) * ease((tt - 4.7) / 0.6)
        out.append(Actor(f'crowd{k + 1}', 'marcher', x + 0.04 * math.sin(tt * 3 + k), d, yaw, st, i=i, tier='t2'))
    return out


def _carried(kind):
    def draw(img, cam, a):
        k = cam.ppm(a.d)
        dirn = -1 if a.yaw < -45 else 1 if a.yaw > 45 else 0   # out in front of them, toward where they go
        fwd = 0.3 * dirn
        dd = 0.0 if dirn else -0.3
        if kind == 'crate':
            S.prop_crate(img, *cam.p(a.x + fwd, a.d + dd, 1.05), k)
        else:
            S.prop_boxes(img, *cam.p(a.x + fwd * .7, a.d + dd, 0.95), k, 3)
    return draw


def board_pose(lt):
    """G7: the A-board's (x, d, height, tilt degrees): stands, kicked over and through the air, lands face down."""
    if lt < BOARD_KICK:
        return BOARD[0], BOARD[1], 0.0, 0.0
    u = min(1.0, (lt - BOARD_KICK) / (BOARD_LAND - BOARD_KICK))
    x, d = lerp(BOARD[0], BOARD_TO[0], u), lerp(BOARD[1], BOARD_TO[1], u)
    z = 0.9 * 4 * u * (1 - u)
    if u >= 1:                                              # down: a skid, then flat
        s = ease(min(1.0, (lt - BOARD_LAND) / 0.25))
        return x + 0.25 * s, d, 0.0, 90.0
    return x, d, z, 90 + 270 * ease(u)                      # one and a quarter turns, flat on its face


@lru_cache(maxsize=4)
def _board_sprite(px):
    """G7 (Sam: 'the sign drawn clearer'): a pavement A-board seen from the front, px tall: a wooden frame with two
    legs, a chalkboard face, ANGEBOT in chalk and two prices."""
    h, w = px, int(px * .62)
    im = Image.new('RGBA', (w + 8, h + 8), (0, 0, 0, 0))
    pts = lambda q: [(4 + x * w, 4 + y * h) for x, y in q]          # noqa: E731
    IS.poly(im, pts([(.06, 1), (.16, 1), (.2, .8), (.1, .8)]), (120, 84, 50), INK, 2)   # legs
    IS.poly(im, pts([(.84, 1), (.94, 1), (.9, .8), (.8, .8)]), (120, 84, 50), INK, 2)
    IS.poly(im, pts([(.04, .84), (.96, .84), (.9, 0), (.1, 0)]), (150, 106, 62), INK, 2.4)   # frame
    IS.poly(im, pts([(.12, .78), (.88, .78), (.84, .07), (.16, .07)]), (34, 44, 40), None, 0)  # chalkboard
    S.text(im, (4 + w * .5, 4 + h * .2), 'ANGEBOT', max(7, int(h * .13)), (244, 244, 236), maxw=w * .64)
    S.text(im, (4 + w * .5, 4 + h * .42), '9,99 €', max(7, int(h * .12)), (250, 220, 90), maxw=w * .6)
    S.text(im, (4 + w * .5, 4 + h * .62), '24,90 €', max(7, int(h * .12)), (230, 232, 226), maxw=w * .6)
    return im


def t2_board(img, lt):
    x, d, z, tilt = board_pose(lt)
    cam = RF2.cam
    k = cam.ppm(d)
    spr = _board_sprite(int(1.15 * k))
    if tilt >= 90 and lt >= BOARD_LAND:                     # lying face down: its back, the frame, squashed flat
        spr = spr.resize((spr.width, max(6, int(spr.height * .22))))
        spr = Image.eval(spr, lambda v: v)
        dk = Image.new('RGBA', spr.size, (110, 78, 46, 255))
        dk.putalpha(spr.getchannel('A'))
        spr = dk
        tilt = 0.0
    r = spr.rotate(-tilt, expand=True, resample=Image.BICUBIC)
    gx, gy = cam.p(x, d, z)
    cy = gy - (spr.height / 2 if tilt == 0 else 0)
    img.alpha_composite(r, (int(gx - r.width / 2), int(cy - r.height / 2)))


def t2_door(img, lt):
    """G4: the door's glass leaf on its hinge (the far jamb, x DOOR_X1), swinging in (drawn behind the people)."""
    cam = RF2.cam
    th = math.radians(door_angle(lt))
    L = DOOR_X1 - DOOR_X0
    hx = DOOR_X1
    fx, fd = hx - L * math.cos(th), FRONT_D + L * math.sin(th)
    q = [cam.p(hx, FRONT_D, 0), cam.p(fx, fd, 0), cam.p(fx, fd, DOOR_H), cam.p(hx, FRONT_D, DOOR_H)]
    IS.poly(img, q, (40, 42, 48), INK, 2.4)                 # the steel frame
    inn = [(lerp(q[0][0], q[1][0], a), lerp(q[0][1], q[1][1], a)) for a in (.1, .9)]
    top = [(lerp(q[3][0], q[2][0], a), lerp(q[3][1], q[2][1], a)) for a in (.1, .9)]
    g = [(inn[0][0], inn[0][1] - .06 * (q[0][1] - q[3][1])), (inn[1][0], inn[1][1] - .06 * (q[1][1] - q[2][1])),
         (top[1][0], top[1][1] + .06 * (q[1][1] - q[2][1])), (top[0][0], top[0][1] + .06 * (q[0][1] - q[3][1]))]
    IS.poly(img, g, (150, 176, 186) if th < 0.05 else (96, 112, 120), None, 0)   # the glass panel
    hb = [cam.p(lerp(hx, fx, .82), lerp(FRONT_D, fd, .82), z) for z in (0.95, 1.1)]
    IS.poly(img, hb, None, (200, 200, 206), 5, 0)          # the push bar's handle
    if th < 0.05:                                           # shut: the opening hours sticker
        c = cam.p(lerp(hx, fx, .5), FRONT_D, 1.55)
        S.text(img, c, 'GEÖFFNET', max(7, int(.09 * cam.ppm(FRONT_D))), (250, 250, 240))


def t2_stones(img, lt):
    """G2: stones hurled from off frame left and near, arcing onto the glass; each bounces off to the plinth (the
    glass holds until the sign); each leaves a small star of cracks (t2_chips)."""
    cam = RF2.cam
    for n, (th, x, z) in enumerate(T2_STONES):
        t0 = th - 0.55
        if lt < t0:
            continue
        r = 0.07 * cam.ppm(13)
        if lt < th:                                         # in the air: from (-4.2, 9.5, 1.7), an arc 1.1 m high
            u = (lt - t0) / 0.55
            p = (lerp(-4.2, x, u), lerp(9.5, FRONT_D - 0.05, u), lerp(1.7, z, u) + 1.1 * 4 * u * (1 - u))
        elif lt < th + 0.35:                                # off the glass and down onto the pavement
            u = (lt - th) / 0.35
            p = (x - 0.2 * u, FRONT_D - 0.05 - 0.5 * u, max(0.0, z * (1 - u * u)))
        else:
            p = (x - 0.2, FRONT_D - 0.55, 0.0)
        gx, gy = cam.p(*p)
        rr = r * cam.ppm(p[1]) / cam.ppm(13)
        IS.poly(img, [(gx + rr * math.cos(a) * (1 + .25 * math.sin(3 * a + n)), gy + rr * .8 * math.sin(a))
                      for a in np.linspace(0, 6.28, 9)[:-1]], (150, 146, 138), INK, 2)
        if th <= lt < th + 0.08:
            S.glow_disc(img, *cam.p(x, FRONT_D, z), 34, (255, 255, 240), amt=.6)


def t2_chips(img, lt):
    """G2: each stone's small star of cracks on the glass, until the sign takes the glass out."""
    if lt >= T2_HIT + 0.1:
        return
    cam = RF2.cam
    for n, (th, x, z) in enumerate(T2_STONES):
        if lt < th:
            continue
        cx, cy = cam.p(x, FRONT_D, z)
        for q in range(7):
            a = q * 0.9 + n
            r = 26 + 14 * ((q * 3 + n) % 3)
            IS.poly(img, [(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))], None, (80, 96, 108), 1.8, 0)
        IS.poly(img, [(cx + 9 * math.cos(a), cy + 9 * math.sin(a)) for a in np.linspace(0, 6.28, 8)], (236, 244, 248),
                (80, 96, 108), 1.4, 0)


def t2_fx(img, lt):
    cam = RF2.cam
    tt = lt
    # the pry bar (1.0-1.55): hauler 1 levers the shutter's hem up from beside his head; the hem rides up with it
    if 1.0 <= tt < 1.55:
        st = t2_state(tt)
        hem = .45 + (2.9 - .45) * st['shutter']
        hx = -0.9 + 0.12
        a, b = cam.p(hx, 13.3, 1.9), cam.p(hx + 0.35, 13.95, hem + 0.02)
        IS.poly(img, [a, b], None, INK, 16, 0)                 # chat 16 (hunt 2: no crowbar read): twice as thick
        IS.poly(img, [a, b], None, (220, 40, 36), 10, 0)       # a red-painted crowbar
        IS.poly(img, [b, (b[0] + 18, b[1] - 14)], None, INK, 12, 0)
        IS.poly(img, [b, (b[0] + 18, b[1] - 14)], None, (220, 40, 36), 6, 0)
    t2_stones(img, lt)
    t2_flash(img, tt)


def t2_flash(img, tt):
    """The impact flash where the sign meets the glass (T2_HIT); its own function so the shape check draws it alone."""
    if T2_HIT - 0.02 <= tt < T2_HIT + 0.15:
        S.glow_disc(img, *RF2.cam.p(T2_STAR[0], FRONT_D, T2_STAR[1]), 70, (255, 250, 210), amt=.5)     # chat 3: small, so the contact reads


def t2_teeth(img, lt):
    """Drawn before the people (in front of the window they hide it)."""
    tt = lt
    t2_chips(img, lt)
    if tt >= T2_HIT + 0.1:                                 # chat 16 (hunt 2: glass looked whole): jagged teeth left
        x0, y0, x1, y1 = T2_WR                             # in the frame, a star of cracks round the hole
        rng = np.random.default_rng(9)
        # G3: the swinger knocks the teeth out as he goes on (1.75-3.85): fewer are left after each swing
        left = 1.0 - 0.5 * min(1.0, max(0.0, (tt - 1.75) / 2.1))
        for side in range(4):
            n = 9
            for q in range(n):
                u0, u1 = q / n, (q + 1) / n
                dep = rng.uniform(25, 95)
                um = (u0 + u1) / 2 + rng.uniform(-.03, .03)
                if rng.uniform() > left:
                    continue
                if side == 0:
                    tri = [(lerp(x0, x1, u0), y0), (lerp(x0, x1, u1), y0), (lerp(x0, x1, um), y0 + dep)]
                elif side == 1:
                    tri = [(lerp(x0, x1, u0), y1), (lerp(x0, x1, u1), y1), (lerp(x0, x1, um), y1 - dep * .7)]
                elif side == 2:
                    tri = [(x0, lerp(y0, y1, u0)), (x0, lerp(y0, y1, u1)), (x0 + dep, lerp(y0, y1, um))]
                else:
                    tri = [(x1, lerp(y0, y1, u0)), (x1, lerp(y0, y1, u1)), (x1 - dep, lerp(y0, y1, um))]
                IS.poly(img, tri, (200, 226, 236), (90, 120, 130), 2, 0)

    # chat 16: the falling glass falls in the window's plane, behind the raiders; then shards on the pavement glinting
    # G6 (Sam: 'why does the broken glass dance on the ground?'): a landed shard lies still (it spun for ever)
    rng = np.random.default_rng(5)
    ground = RF2.R(0, 1175)[1]
    for n in range(60):
        x0, y0 = rng.uniform(T2_WR[0] + 10, T2_WR[2] - 10), rng.uniform(T2_WR[1] + 10, T2_WR[3] - 20)
        a = tt - (T2_HIT + 0.05) - rng.uniform(0, .15)
        gy = ground + rng.uniform(-20, 15)
        dx, r, sp0 = rng.uniform(-60, 60), rng.uniform(10, 24), rng.uniform(0, 6.28)
        if a < 0:
            continue
        land = math.sqrt(max(0.0, gy - y0) / 1100)
        a = min(a, land)
        yy = min(gy, y0 + 1100 * a * a)
        xx = x0 + dx * min(a, .4)
        sp = sp0 + a * 9
        tri = [(xx + r * math.cos(sp + q * 2.1), yy + r * .7 * math.sin(sp + q * 2.1)) for q in range(3)]
        IS.poly(img, tri, (210, 230, 238), (120, 150, 160), 1.2, 0)
        if (n + int(lt * 12)) % 7 == 0:
            S.glow_disc(img, xx, yy, 9, (255, 255, 255), amt=.7)


def blue_wash(img, lt):
    """T2 from T2_WASH (round 2: 6.8; was 5.0): the blue light from the far right end of the street sweeping across
    crowd and store; faces, signs and the wet ground turn blue (the last light layer, over everything)."""
    if lt < T2_WASH:
        return
    lt = lt - (T2_WASH - 3.0)                              # the sweep's own clock, as it was
    u = ease((lt - 3.0) / 0.35)
    a = np.asarray(img.convert('RGB'), np.float32)
    xs = np.arange(W, dtype=np.float32)[None, :]
    sweep = W - ((lt - 3.0) * 1600) % (W * 1.6)                # a bright band crossing right to left, again and again
    band = np.exp(-((xs - sweep) / 220.0) ** 2)
    strobe = 0.75 + 0.25 * (int(lt * 8) % 2)
    tint = np.array((0.42, 0.55, 1.05), np.float32)
    k = (0.32 * u * strobe + 0.62 * band * u)[..., None]   # chat 15: the sweep, not a flat tint, carries it
    out = a * (1 - k) + (a * tint + np.array((10, 30, 90), np.float32)) * k
    ys = np.arange(H, dtype=np.float32)[:, None]
    wet = ((ys > 1420) & (ys < 1630)).astype(np.float32) * band * u * 0.5
    out += wet[..., None] * np.array((40, 80, 200), np.float32)
    on = 1.0 if int(lt * 8) % 2 == 0 else 0.45               # the van's light bar just off the right edge, strobing
    edge = np.exp(-((W - xs) / 260.0) ** 2) * np.exp(-((ys - 1050) / 700.0) ** 2) * on * u * 0.8
    out += edge[..., None] * np.array((60, 110, 255), np.float32)
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert('RGBA'), (0, 0))


def phone_lights(img, actors, cam):
    """G8 (Sam: 'white glints on the backs of heads?'): the glow was drawn at eye height for every phone, so a phone
    held in front of the face by someone seen from behind put a white disc on the back of their head. The phone's lit
    screen is drawn by the cast's phone itself; the glow only for a phone turned to us (its torch), at the hand."""
    for a in actors:
        if a.state == 'phone' and math.cos(math.radians(a.yaw)) > 0.5:
            gx, gy = cam.p(a.x + 0.12, a.d, 1.62)
            S.glow_disc(img, gx, gy, 0.09 * cam.ppm(a.d), (235, 245, 255), amt=.55)


# ================================================================================================= T3
T3_TRUCK_D = S.TRUCK_D3
class Reframe:
    """A longer lens from the same spot: the set's painting zoomed k about screen x cx and moved down c px (k*y + c).
    `cam` is the same lens maths for drawing people and effects sharp onto it; `R(x, y)` maps the set's pixels."""
    def __init__(self, cam0, k, cx, c):
        self.k, self.cx, self.c = k, cx, c
        self.cam = S.Cam(cx + k * (cam0.VX - cx), k * cam0.VY + c, k * cam0.F, cam0.CH)

    def R(self, x, y):
        return self.cx + self.k * (x - self.cx), self.k * y + self.c

    def image(self, im):
        k, cx, c = self.k, self.cx, self.c
        out = im.transform(im.size, Image.AFFINE, (1 / k, 0, cx - cx / k, 0, 1 / k, -c / k), Image.BICUBIC)
        if c > 0 and im.getpixel((540, 2))[3] > 0:         # an opaque painting: fill the top strip with its sky
            out.paste(im.crop((0, 0, W, 1)).resize((W, int(c) + 2)), (0, 0))
        return out


# chat 14: the sets' low cameras left the bottom 45% (T3) and 25% (T4) of the frame bare ground
RF3 = Reframe(S.CAMS['t3'], 1.0, 540, 0.0)   # round 2 (F1): the raised camera needs no zoom
RF4 = Reframe(S.CAMS['t4'], 1.0, 540, 0.0)   # round 2 (A1): the raised, wider camera needs no zoom
RF4_LOW = Reframe(S.CAM4_LOW, 1.15, 0, 80.0)  # the old street-level T4 (chat 15): the end scene's shots A and C
T3K, T3CAM, R3, reframe3 = RF3.k, RF3.cam, RF3.R, RF3.image
T4CAM, R4 = RF4.cam, RF4.R
# chat 15 (moves hunt 1: the runners and the swing too small, the near crowd hid them): T2 nearer too; the near crowd
# moved back to the two sides, so the bottom of the frame is them, not bare road
# round 2 (G4, Sam: 'camera a little right, the window's left edge on the screen's left edge'): about x 750 (was 480),
# so the window's frame (x -2.2 m) sits at screen x 0 and the shop door fits on the right
RF2 = Reframe(S.CAMS['t2'], 1.25, 750, -5.0)
T2_WR = (*RF2.R(T2_WIN[0], T2_WIN[1]), *RF2.R(T2_WIN[2], T2_WIN[3]))
DOOR_CLIP = (*RF2.cam.p(DOOR_X0, FRONT_D, DOOR_H), *RF2.cam.p(DOOR_X1, FRONT_D, 0))   # G4: inside shows only here


def truck_x(lt):
    # chat 15: drives right into frame (was 2.8: a cropped block); round 1: J3 later, then pushes 1.5 m on (5.5-6.5)
    return lerp(9.0, 1.2, ease((lt - 1.9 - J3) / 0.7)) - 1.5 * ease((lt - 5.5) / 1.0)


def nozzle(lt, aim=12.0):
    cam = T3CAM
    k = cam.ppm(T3_TRUCK_D)
    gx, gy = cam.p(truck_x(lt), T3_TRUCK_D)
    bx, by = gx + 1.4 * k, gy - 3.3 * k
    a = math.radians(aim)
    return bx - 1.45 * k * math.cos(a), by - 1.45 * k * math.sin(a)


@lru_cache(None)
def crowd_t3():
    rng = np.random.default_rng(31)
    out = []
    for d in np.arange(9.0, 44.0, 0.9):                     # round 2 (F1): from 9 m, left of the front line
        for x in np.arange(-12.0, (-2.3 if d < 13.5 else -1.6) + (d - 13) * .03, 0.7):
            r = rng.uniform()
            state = 'flag:tricolour' if r < .12 else 'stand'
            if d > 33 and r > .8:
                state = 'placard:CGT:200,30,40'
            out.append(dict(x=x + rng.uniform(-.25, .25), d=d + rng.uniform(-.3, .3), i=int(rng.integers(0, 16)),
                            state=state, ph=rng.uniform(0, 6.28)))
    return out


VOLLEY2 = 2.5                       # round 1: the second volley (the back row) starts throwing
CAR_T0, CAR_LET, CAR_STOP = 6.0, 6.9, 7.6   # the shove starts, they let go, it stops in the jet
CAR_HIT = 7.2                        # the jet hits the car: a burst of steam, the fire knocked down


def car_move(lt):
    """The T3 car's shove (S.car_pt): (dx, dd, yaw) - 1.6 m right, 3.4 m on toward the police, the nose 12 deg right."""
    u = min(1.0, max(0.0, (lt - CAR_T0) / (CAR_STOP - CAR_T0)))
    m = u * u * (2.2 - 1.2 * u) if u < 1 else 1.0          # slow off the mark, rolling freely, then caught by the jet
    m = min(1.0, m)
    return 0.9 * m, 3.2 * m, 10.0 * m


def car_fire(lt):
    return 1.0 - 0.75 * ease((lt - CAR_HIT) / 0.5)


def car_roof(lt):
    X0, X1, D0, _ = S.CAR3
    return S.car_pt(X1 - 0.5, D0 + 2.4, car_move(lt))


def car_fx(img, lt):
    """T3 7.2-8.0: the jet hits the burning car: a burst of white steam boiling up off it, drifting left."""
    if lt < CAR_HIT:
        return
    u = lt - CAR_HIT
    cx, cy = T3CAM.p(*car_roof(lt), 1.4)
    k = T3CAM.ppm(car_roof(lt)[1])
    lumps = []
    for n in range(9):
        a = min(1.0, u / 0.8) * (0.4 + 0.6 * ((n * .37) % 1))
        lumps.append((cx + k * (-.6 + .17 * n) * (0.5 + a) - 120 * u, cy - k * (0.3 + 2.0 * a) + 18 * math.sin(n * 1.7),
                      k * (0.3 + 0.5 * a)))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    S.smoke(lay, lumps, (228, 234, 238), (252, 252, 252), line=(170, 178, 186), lw=2.4)
    img.alpha_composite(lay)


def draw_car3(img, lt):
    mv = car_move(lt)
    S._car(img, T3CAM, lt, mv, fire=car_fire(lt), roll=mv[1] / 0.34)


OFF_L = -4.2                       # chat 29: T3's left edge is x -2.4 at the front line; past this they are gone
PUSH_IN = 1.5                       # the pushers' run in from the left


def _volley(c):
    """A throwing cycle (0..1) -> the throw's u: through in 0.6 of it, then the arm comes back (it snapped back to
    wound up in one frame: hands 13 m/s, chat 29)."""
    return c / 0.6 if c < 0.6 else 1 - (c - 0.6) / 0.4


def _getaway(u, v=4.5, acc=0.35):
    """Metres run u s after setting off: up to speed v over `acc` s (it went 0 -> 4.5 m/s in one frame)."""
    return v * u * u / (2 * acc) if u < acc else v * (u - acc / 2)


def _turn(y0, y1, w):
    """Yaw turning from y0 to y1 the short way round as w goes 0 -> 1 (eased)."""
    dy = (y1 - y0 + 180) % 360 - 180
    y = y0 + dy * ease(min(1.0, max(0.0, w)))
    return (y + 180) % 360 - 180


FRONT3 = ((-0.95, 10.4), (-0.75, 11.4), (-1.0, 12.4), (-0.8, 13.4))   # round 2 (F1): the front line runs away from
BACK3 = ((-1.6, 10.9), (-1.55, 11.9), (-1.65, 12.9))     # us (a wall facing right); the back row steps up in its gaps
CRS_YAW = -60   # round 2 (F2): turned three-quarters to the camera so the raised shields show their face, not an edge
CRS_X, CRS_D = (1.9, 2.55, 3.2), (9.9, 10.9, 11.9, 12.9, 13.9)   # round 2 (F2): the police block, 3 ranks of 5
SHIELD_X = 1.9 - 0.42                                  # the front rank's shield face (x m), before the advance
ADV_T, ADV_STEP, ADV_N = 4.7, 0.5, 3                    # F2: when the cannon opens up, 3 steps of 0.4 m in lockstep


def crs_adv(lt):
    """The block's advance (m, toward the crowd) and whether it is mid-step: one step every 0.5 s, all together."""
    u = (lt - ADV_T) / ADV_STEP
    if u <= 0:
        return 0.0, False
    n = int(u)
    if n >= ADV_N:
        return 0.4 * ADV_N, False
    return 0.4 * (n + ease(u - n)), True


def crs_guard(lt):
    """Shields up (0..1): raised as the first stones come over (0.8), lowered once the cannon takes over."""
    return ease((lt - 0.8) / 0.3) * (1 - ease((lt - 2.6 - J3) / 0.3))


def t3_actors(lt):
    out = []
    jet = lt > 2.6 + J3
    walk_in = 1.4 * (1 - ease(min(1.0, lt / 0.75)))        # round 2 (F3): the front line advances 0-0.75 s
    for k, (x, d) in enumerate(FRONT3):                     # the black-clad front line, facing the police (right)
        dx, _ = field('t3', x, d, lt, k)
        if jet and lt > 2.7 + J3 + 0.05 * k:                  # broken by the jet: running out left
            u = lt - 2.7 - J3 - 0.05 * k
            if x + dx * .3 - _getaway(u) < OFF_L:
                continue
            ut = ((2.7 + J3 + 0.05 * k - 0.75) * 1.6 + k * 0.37) % 1.0
            out.append(Actor(f'front{k + 1}', 'rioter', x + dx * .3 - _getaway(u), d, _turn(90, -115, u / .3), 'run',
                             t=lt, tier='t3').blend('throw', _volley(ut), w=u / .3))
        elif 0.75 <= lt:
            u = ((lt - 0.75) * 1.6 + k * 0.37) % 1.0
            out.append(Actor(f'front{k + 1}', 'rioter', x + dx * .3, d, 90, 'throw', u=_volley(u), tier='t3')
                       .blend('march', t=0.75, w=(lt - 0.75) / 0.2))
        else:
            out.append(Actor(f'front{k + 1}', 'rioter', x - walk_in, d, 90, 'march', t=lt, tier='t3'))
    # round 1 (T3 2.5-4.0): the second volley, twice the throwers: a back row steps up between the front line's gaps
    for k, (x, d) in enumerate(BACK3):
        if lt < VOLLEY2 - 0.3:
            continue
        if jet and lt > 2.6 + J3 + 0.05 * k:                  # round 2: the back row breaks first (it ran through the front line)
            u = lt - 2.6 - J3 - 0.05 * k
            ut = ((2.6 + J3 + 0.05 * k - VOLLEY2) * 1.6 + k * 0.29) % 1.0
            if x - _getaway(u) < OFF_L:
                continue
            out.append(Actor(f'back{k + 1}', 'rioter', x - _getaway(u), d, _turn(90, -115, u / .3), 'run',
                             t=lt + .3, tier='t3').blend('throw', _volley(ut), w=u / .3))
        elif lt >= VOLLEY2:
            u = ((lt - VOLLEY2) * 1.6 + k * 0.29) % 1.0
            out.append(Actor(f'back{k + 1}', 'rioter', x, d, 90, 'throw', u=_volley(u), tier='t3')
                       .blend('march', t=VOLLEY2, w=(lt - VOLLEY2) / 0.2))
        else:                                               # stepping up from the crowd behind
            out.append(Actor(f'back{k + 1}', 'rioter', x - 0.6 * (VOLLEY2 - lt) / 0.3, d, 90, 'march', t=lt,
                             tier='t3'))
    # round 1 (T3 6.0-8.0): four rioters shove the burning car into the gap, let go at 6.9, cheer it on, run off left
    if CAR_T0 - PUSH_IN - 0.1 <= lt < CAR_T0 - 0.1:     # chat 27: they run in from off the left edge (no pop)
        X0, X1, D0, _ = S.CAR3                              # chat 29: over 1.5 s (0.65: bodies 7.5 m/s, feet 8)
        u = ease((lt - CAR_T0 + PUSH_IN + 0.1) / PUSH_IN)
        for k, (px, pd) in enumerate(((X1 - 0.15, D0 - 0.45), (X1 + 0.4, D0 + 0.35), (X1 + 0.45, D0 + 1.25),
                                      (X1 + 0.45, D0 + 2.15))):
            x, d = S.car_pt(px, pd, car_move(lt))
            out.append(Actor(f'pusher{k + 1}', 'rioter', x - 3.2 * (1 - u), d, 115, 'run', t=lt + k * .2, tier='t3'))
    if CAR_T0 - 0.1 <= lt:
        mv = car_move(lt)
        X0, X1, D0, _ = S.CAR3
        xc = (X0 + X1) / 2
        # chat 27 (notes hunt 1: three of four pushers stood off the left edge): one at the rear's right corner, three
        # down the right flank leaning into it, all in frame; (x, d) in the car's own frame, moved with it by car_pt
        spots = ((X1 - 0.15, D0 - 0.45), (X1 + 0.4, D0 + 0.35), (X1 + 0.45, D0 + 1.25), (X1 + 0.45, D0 + 2.15))
        for k, (px, pd) in enumerate(spots):
            if lt < CAR_LET:
                x, d = S.car_pt(px, pd, mv)
                w = (lt - CAR_T0 + 0.1) / 0.25                # chat 29: from the run into the shove, 3 frames
                out.append(Actor(f'pusher{k + 1}', 'rioter', x, d, _turn(115, 140, w), 'push', t=lt * 1.6 + k * .3,
                                 tier='t3').blend('run', t=CAR_T0 - 0.1 + k * .2, w=w))
            else:
                x, d = S.car_pt(px, pd, car_move(CAR_LET))
                u = lt - CAR_LET - 0.4 - 0.08 * k
                if u < 0:
                    out.append(Actor(f'pusher{k + 1}', 'rioter', x, d, 150, 'cheer', u=abs(math.sin(lt * 9 + k)),
                                     tier='t3'))
                elif x - _getaway(u) >= OFF_L:            # chat 29: turn and get going (snapped cheer -> sprint)
                    t0 = CAR_LET + 0.4 + 0.08 * k
                    out.append(Actor(f'pusher{k + 1}', 'rioter', x - _getaway(u), d - 0.3 * k * ease(u / .3),
                                     _turn(150, -115, u / .3), 'run', t=lt + k * .2, tier='t3')
                               .blend('cheer', abs(math.sin(t0 * 9 + k)), w=u / .3))
    # round 2 (F2, Sam: 'police are static'): a block 3 deep, 5 wide; the front ranks' shields up against the
    # missiles, then the whole block steps forward together when the cannon opens up
    adv, stepping = crs_adv(lt)
    g = crs_guard(lt)
    for c, x in enumerate(CRS_X):
        for r, d in enumerate(CRS_D):
            k = c * len(CRS_D) + r
            if stepping:
                a = Actor(f'crs{k + 1}', 'officer', x - adv, d, CRS_YAW, 'line_walk', t=lt - ADV_T, force='crs', tier='t3')
            elif c < 2 and g > 0:
                a = Actor(f'crs{k + 1}', 'officer', x - adv, d, CRS_YAW, 'shield_up', u=g * (1.0 if c == 0 else .5),
                          force='crs', tier='t3')
            else:
                a = Actor(f'crs{k + 1}', 'officer', x - adv, d, CRS_YAW, 'line', force='crs', tier='t3')
            a.i = (k * 5) % 7
            out.append(a)
    return out


def t3_crowd(img, lt):
    cam = T3CAM
    for m in sorted(crowd_t3(), key=lambda m: -m['d']):
        dx, dd = field('t3', m['x'], m['d'], lt, m['ph'])
        x, d = m['x'] + dx, max(8.8, m['d'] + dd)
        gx, gy = cam.p(x, d)
        if gx < -80 or gx > W + 80:
            continue
        x -= 0.9 * (1 - ease(lt / 0.9))                     # round 2 (F3): the crowd surges in behind its front line
        gx, gy = cam.p(x, d)
        running = lt > 2.6 + J3 and m['d'] < 30 and lt - 2.6 - J3 - 0.02 * max(0, m['x'] + 2) > 0.1
        if running:                                         # chat 16 (hunt 2: crowd not breaking): they run out left
            x -= 3.2 * (lt - 2.7 - J3 - 0.02 * max(0, m['x'] + 2))
            gx, gy = cam.p(x, d)
        yaw = -90 if running else 90
        paste(img, 'marcher', m['i'], 't3', m['state'] if not running else 'stand', yaw, gx, gy, scale_at(cam, d))


def t3_columns(img, lt):
    """Smoke climbing from the car (left) and the bike heap (mid-right) from 0.0. Chat 15: drawn before the truck and
    the people (the bikes burn at d 14, behind the police: their smoke had hidden the water cannon truck)."""
    cx, cy = T3CAM.p(*car_roof(lt), 2.0)                    # round 2 (F1): from the car and the bikes where they are
    bx, by = T3CAM.p(*S.BIKES3, 1.2)                        # (round 1: the car's smoke goes where the car goes)
    for (sx, sy, sd) in ((cx, cy, 1), (bx, by, 2)):
        if sd == 1 and lt > CAR_HIT + 0.3:                  # the jet put it out: steam (car_fx) instead
            continue
        lumps = []
        for n in range(6):
            a = (lt * 0.9 + n / 6) % 1.0
            drift = -150 if sd == 1 else 130                 # round 2: the car's smoke leans left, the bikes' right,
            lumps.append((sx + drift * a + 18 * math.sin(n * 2.1), sy - 520 * a, 40 + 90 * a))   # clear of Marianne
        S.smoke(img, lumps, (58, 54, 56), (138, 128, 124), lw=2.5)


def t3_debris(img):
    """Chat 16 (hunt 2: bare grey ground filled the lower third): the square's near ground littered, as in the
    references: thrown cobbles, leaflets, a dropped tricolour and a yellow vest."""
    cam = T3CAM
    rng = np.random.default_rng(23)
    for _ in range(22):                                    # cobbles
        x, d = rng.uniform(-2.6, 3.6), rng.uniform(6.6, 9.4)     # round 2: the near ground in the raised frame
        sx, sy = cam.p(x, d)
        k = cam.ppm(d)
        IS.ell(img, sx, sy - .06 * k, .13 * k, .08 * k, (128, 118, 106), INK, 2)
        IS.ell(img, sx - .03 * k, sy - .09 * k, .05 * k, .03 * k, (170, 160, 146), None)
    for _ in range(9):                                     # leaflets
        x, d = rng.uniform(-2.6, 3.6), rng.uniform(6.6, 9.4)
        k = cam.ppm(d)
        sx, sy = cam.p(x, d)
        w_, h_, sk = .32 * k, .1 * k, rng.uniform(-.4, .4) * k * .2
        IS.poly(img, [(sx - w_, sy), (sx + w_, sy + sk), (sx + w_ * .8, sy - h_ + sk), (sx - w_ * 1.1, sy - h_)],
                (240, 238, 228), INK, 1.6)
    # a dropped tricolour (near left) and a yellow vest (near right), lying flat
    for (x, d, cols) in ((0.9, 7.0, ((40, 60, 150), (245, 245, 240), (200, 40, 50))),
                         (2.9, 8.2, ((236, 214, 40),) * 3)):
        k = cam.ppm(d)
        sx, sy = cam.p(x, d)
        w3 = .3 * k
        for q, col in enumerate(cols):
            x0 = sx - 1.5 * w3 + q * w3
            IS.poly(img, [(x0, sy), (x0 + w3, sy + 4), (x0 + w3 + 6, sy - .22 * k + 4), (x0 + 6, sy - .22 * k)], col,
                    INK, 2)


def _missile(img, cam, what, x0, d0, d1, t0, lt, flight=0.45, spin=0):
    """Round 2 (F2): one thrown thing from (x0, d0) at the police block's shields (d1): up in an arc, hits the raised
    shield face (a flash), bounces back off it and drops to the paving in front of the line, where it lies."""
    a = (lt - t0) / flight
    if a < 0:
        return
    hx = SHIELD_X - crs_adv(t0 + flight)[0]                    # the shield face where it gets there
    k = cam.ppm(d1)
    if a < 1:                                                  # in the air
        x, z = lerp(x0 + 0.3, hx, a), 1.9 + 2.4 * math.sin(math.pi * a) - 0.3 * a
        d = lerp(d0, d1, a)
    else:                                                      # off the shield: back 0.7 m, down to the ground
        b = min(1.0, (a - 1) / 0.8)
        x, z, d = hx - 0.7 * b, max(0.0, 1.6 + 0.5 * math.sin(math.pi * b * .6) - 1.75 * b * b), d1
        if a < 1.25:                                           # the hit: a white flash on the shield
            sx, sy = cam.p(hx, d1, 1.6)
            S.glow_disc(img, sx, sy, k * (0.55 * (1.25 - a) / 0.25 + .2), (255, 246, 200), amt=.8)
    sx, sy = cam.p(x, d, z)
    k = cam.ppm(d)
    rot = spin * min(a, 1.0) + spin * .3 * max(0.0, min(a, 1.8) - 1)
    if what == 'cone':
        S.prop_cone(img, sx, sy, 1.4 * k, rot)
    elif what == 'wheel':
        S.prop_wheel(img, sx, sy, 1.25 * k, rot)
    else:
        IS.ell(img, sx, sy, .18 * k, .14 * k, (120, 108, 96), INK, 3)     # drawn ~3x true to read at phone size
        IS.ell(img, sx - .05 * k, sy - .05 * k, .07 * k, .05 * k, (176, 164, 150), None)


def t3_fx(img, lt):
    cam = T3CAM
    # the front line's stones (0.75-4.5), each at the shield facing its thrower; round 2: they hit and bounce off
    for k, (x0, d0) in enumerate(FRONT3):
        for rep in range(7):
            t0 = 0.75 + ((k * 0.37 + 0.6) % 1.0) / 1.6 + rep / 1.6
            if t0 < 2.6 + J3 and lt < t0 + 0.45 + 0.8 * 0.45 + 0.05:
                _missile(img, cam, 'stone', x0, d0, CRS_D[min(4, k + (rep % 2))], t0, lt)
    # round 1 (T3 2.5-4.55): the back row's volley, over the front line's heads: stones, a traffic cone, a bike wheel
    for k, (x0, d0) in enumerate(BACK3):
        for rep in range(5):
            t0 = VOLLEY2 + ((k * 0.29 + 0.6) % 1.0) / 1.6 + rep / 1.6
            if t0 >= 2.6 + J3 or lt > t0 + 0.5 + 0.8 * 0.5 + 0.05:
                continue
            what = 'cone' if (k, rep) == (1, 0) else 'wheel' if (k, rep) == (2, 1) else 'stone'
            _missile(img, cam, what, x0, d0, CRS_D[k + 1], t0, lt, flight=0.5, spin=540 if what != 'stone' else 0)
    # the spent missiles lying in front of the shields (they pile up as the volleys land)
    rng = np.random.default_rng(17)
    for n in range(int(min(12, max(0, (lt - 1.45) * 5)))):
        sx, sy = cam.p(SHIELD_X - rng.uniform(0.5, 0.9), rng.uniform(9.6, 14.2))
        k = cam.ppm(11)
        IS.ell(img, sx, sy - .03 * k, .11 * k, .07 * k, (150, 146, 138), INK, 2)
    # the tear-gas canister lands at 1.6 by Marianne's base, trailing white; the gas swells over her lower half
    # (chat 15: hunt 1 saw no landing and the gas over the crowd: it lands nearer her base, set y 870, with a puff)
    if 1.2 <= lt < 1.6:
        a = (lt - 1.2) / 0.4
        bx, by = cam.p(S.MON_X - 0.4, 74, 2.0)            # round 2: lands at her base, wherever the camera puts it
        pos = lambda u: (lerp(W + 20, bx, u), lerp(by - 110, by, u) - 160 * math.sin(math.pi * u))   # noqa: E731
        trail = [pos(max(0.0, a - q * 0.06)) + (10 + 7 * q,) for q in range(1, 6)]
        S.smoke(img, trail, (226, 228, 226), (250, 250, 248), line=(170, 176, 180), lw=2, fade=False)
        sx, sy = pos(a)
        IS.ell(img, sx, sy, 20, 11, (86, 94, 86), INK, 2.5)
        IS.ell(img, sx - 14, sy, 5, 9, (200, 60, 40), None)
    if lt >= 1.6:
        g = ease((lt - 1.6) / 0.6)                          # chat 16 (hunt 2: gas tiny): swells in 0.6 s, 1.35x
        bx, by = cam.p(S.MON_X - 0.4, 74, 2.0)
        G3 = 1.35 * cam.ppm(80) / 24.0                      # round 2: the gas's size, from the monument's scale
        if lt < 1.75:                                       # the landing: a quick white burst ring
            S.glow_disc(img, bx, by, 110 * G3 / 1.6 * (lt - 1.55) / 0.2, (255, 255, 255), amt=.7)
        lumps = [(bx + G3 * dx * g, by - G3 * dy * g, G3 * (36 + r * g)) for dx, dy, r in
                 ((0, 0, 70), (-140, 20, 75), (150, 15, 75), (-70, 120, 80), (80, 135, 80), (0, 220, 85),
                  (-210, 70, 60), (230, 60, 60), (-30, 300, 60))]
        a = min(1.0, (lt - 1.6) / 0.3)
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        S.smoke(lay, lumps, (226, 230, 230), (252, 252, 250), line=(170, 176, 180), lw=2.5)
        if lt > 2.6 + J3:                                  # the jet blows it left
            lay = lay.transform(lay.size, Image.AFFINE, (1, 0, 190 * (lt - 2.6 - J3), 0, 1, 0))
        a *= 1.0 - 0.55 * ease((lt - VOLLEY2 + 0.5) / 0.5)   # chat 27 (notes hunt 1: the gas hid the second volley)
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * 0.88 * a)))
        img.alpha_composite(lay)
    # the water cannon jet (2.5-4.0): a white tapering stream from the roof cannon, sweeping the front line
    if lt >= 2.55 + J3:
        nx, ny = nozzle(lt)
        sweep = ease((lt - 2.55 - J3) / 1.3)
        ix, iy = cam.p(lerp(0.4, -2.2, sweep) - 1.0 * ease((lt - 5.5) / 1.0), 11.8, 1.3)   # round 2: from the gap
        if lt > CAR_HIT - 0.4:                              # round 1: the jet swings onto the rolling car (7.2)
            cx, cy = cam.p(*car_roof(lt), 1.5)
            r = ease((lt - CAR_HIT + 0.4) / 0.4)
            ix, iy = lerp(ix, cx, r), lerp(iy, cy, r)
        g = min(1.0, (lt - 2.55 - J3) / 0.12)
        ix, iy = lerp(nx, ix, g), lerp(ny, iy, g)
        mx, my = (nx + ix) / 2, min(ny, iy) - 70
        pts_top, pts_bot = [], []
        for n in range(13):
            u = n / 12
            x = (1 - u) ** 2 * nx + 2 * (1 - u) * u * mx + u * u * ix
            y = (1 - u) ** 2 * ny + 2 * (1 - u) * u * my + u * u * iy
            w = 12 + 40 * u                                 # chat 16 (hunt 2: a thin arc)
            pts_top.append((x, y - w))
            pts_bot.append((x, y + w))
        IS.poly(img, pts_top + pts_bot[::-1], (236, 244, 252), (150, 176, 200), 2.4, 0)
        IS.poly(img, pts_top[:9] + [(x, y + 5) for x, y in pts_top[8::-1]], (255, 255, 255), None, 0, 0)
        rng = np.random.default_rng(int(lt * 12))
        spray = [(ix + rng.uniform(-90, 60), iy + rng.uniform(-80, 40), rng.uniform(20, 50)) for _ in range(7)]
        S.smoke(img, spray, (226, 238, 248), (250, 252, 255), line=(160, 184, 204), lw=2)


# ================================================================================================= T4
def heli_state(lt):
    x, y = S.HELI_HOME[0], S.HELI_HOME[1]
    if lt < 1.0:
        return dict(x=x + 6 * math.sin(lt * 2), y=y + 4 * math.sin(lt * 3), s=HELI_S, turn=0, roll=-4, hit=False)
    u = min(1.0, (lt - 1.0) / T4_FALL)                      # round 1: a longer fall at the same spin rate
    turn = (int(u * 14 * T4_FALL) * 45) % 360                         # three drawn turns and their mirrors, stepped in 45s
    return dict(x=x - 60 * u + 30 * math.sin(u * 9), y=y + 520 * u ** 3 + 40 * u, s=HELI_S * (1 - .2 * u),  # chat 16
                turn=turn, roll=-4 + 40 * u, hit=True)


T4_LEN = dict(LENS)['t4']
MOPED_D = 10.5
T4_FALL, T4_FIRE = 1.6, 7.5        # round 1 (T4 10 s): the fall 1.0-2.6 (was 1 s), the big fireball at 7.5 (was 3.0)
HELI_S = S.HELI_HOME[2] * 1.6     # chat 15 (hunt 1: "helicopter tiny and grey"): drawn larger than its depth


def moped_pos(lt, k):
    x = lerp(-4.2 - k * 1.2, -0.7 - k * 1.1, ease(min(1.0, lt / 0.6)))   # chat 15: rear one in frame
    if lt > 1.1:                                   # round 1: they rev off right after the hit (frees the corner for
        x += 11.0 * (lt - 1.1) ** 2                # the seller's cart)
    return x, MOPED_D + 2.6 * k


@lru_cache(None)
def crowd_t4():
    rng = np.random.default_rng(41)
    out = []
    for d in np.arange(13.7, 62.0, 0.9):          # round 2 (A1): the wider T4 sees deeper and nearer: 13.7-62 m
        for x in np.arange(-14.0, 0.8, 0.7):          # (was 18.5-48), x to the bank's face at -9 (people were in it)
            if x < -8.4 or (d < 18.5 and x > -2.7):     # the near rows: left of the melee's rioters (x -2 on)
                continue
            r = rng.uniform()
            state = 'flag:albania' if r < .018 else 'stand'    # chat 14: 14% made a solid red band
            out.append(dict(x=x + rng.uniform(-.25, .25), d=d + rng.uniform(-.3, .3), i=int(rng.integers(0, 16)),
                            state=state, ph=rng.uniform(0, 6.28)))
    return out


# ---- round 1 (Sam's gags a, b, c and R5): the T4 beats are in notes "## Round 1 plan", Beat list
MD = 3.0                                           # round 1: the melee 3 m nearer (it read as a grey smear)
SELFIE = (0.35, 10.3)                              # gag b: front and centre, between the cart and the melee
#                                                    (chat 29: 0.6 m nearer, out of the queue's line: they walked through him)
CART = (-1.6, 10.6)                               # the seller's cart, by the bank (bottom left)
SLOT = (-0.3, 11.0)                               # where the buyer at the front of the queue stands
SALES = (3.1, 4.15, 5.2)                           # gag a: he hands a lit bottle over (each buyer throws at once)
#                                                    chat 29: 1.05 s apart (0.4: the next one stepped up into the last)
GRANNY_BUY, GRANNY_THROW, GRANNY_HIT = 6.35, 6.6, 7.3
CHEER = 7.35                                       # her hit: the seller applauds, fists go up
# round 2 (A2): 7.9-10.4 the new action: a rioter hoisted on a captured riot shield and carried over the crowd
# with the flag (SURF), while the beaten police turn and run off right, each in his own time (ROUT); then the hold
SURF, SURF_D, SURF_X = (7.9, 10.4), 16.6, (-5.4, -1.0)   # over the near rows (bigger on screen than the main crowd)
ROUT = 8.0
ROUT_LAG = (0.0, 0.22, 0.08, 0.35, 0.15, 0.41, 0.27, 0.05)   # F9: no group moves as one
ROUT_V = (4.4, 3.8, 4.7, 3.6, 4.1, 3.9, 4.5, 4.2)
ROUT_LANE = (-0.2, 0.4, -0.35, -0.6, -0.2, 0.3, -0.45, 0.15)   # each his own lane (2 ran through 4 at 8.45)
FW0 = 8.0                                          # the fireworks start with the new action (were with the hold)
HOLD = 10.4                                        # the gleeful hold: jumping (was 8.0, round 2: after the surf)
# where each Molotov lands: the bank's ground-floor windows, then (granny) its first floor. Round 2 (A1): world
# points on the bank's face (x -9, a window's middle), so they stay on it through any camera (were screen pixels)
LAND_W = [(-9.0, 37.3, 2.4), (-9.0, 47.3, 2.4), (-9.0, 57.3, 2.4), (-9.0, 42.3, 11.8)]


def land(k):
    """Molotov k's landing on screen (k 3: the granny's), through whichever T4 camera is drawing."""
    return T4CAM.p(*LAND_W[k])


def _throw_u(lt, t0):
    """A throw's u (0 wound up .. 1 through) for a bottle handed over at t0: wound 0.1 s, through by +0.4."""
    return ease((lt - t0 - 0.12) / 0.28)


def t4_actors(lt):
    out = []
    push = ease((lt - 2.0) / 1.0)
    back = 0.15 * max(0.0, lt - 3.0)               # round 1: the line keeps giving ground after it breaks
    for k in range(8):                                     # the shield line, facing left; buckles 1.6, breaks 2.0
        if k == 3 and lt >= 2.15:                          # his shield is the one that spins up (gag of the melee)
            pass
        x = 1.2 + k * 0.55 + push * (0.8 + 0.25 * (k % 3)) + back * (1 + 0.2 * (k % 2))
        d = 17.5 - MD + (0.6 * push if k % 2 else -0.4 * push)
        state = 'line' if lt < 1.6 else 'pushed' if (k % 3 != 1 or lt < 2.0) else 'baton_up'
        a = lt - ROUT - ROUT_LAG[k]
        if a > 0:                                          # round 2 (A2): routed, off right, each his own pace
            x += _getaway(a, ROUT_V[k], 0.3)
            if x > 0.33 * d + 1.2:                         # off the right edge
                continue
            out.append(Actor(f'policia{k + 1}', 'officer', x, d + ROUT_LANE[k] * ease(a / 0.3),
                             -55 if a < 0.08 else 10 if a < 0.17 else 115, 'run', t=lt + 0.13 * k, force='policia', tier='t4')
                       .blend(state, w=a / 0.12))   # the turn in 3 drawings: mid-turn run yaws fold the arm
            continue
        out.append(Actor(f'policia{k + 1}', 'officer', x, d, -55, state, force='policia', tier='t4'))  # chat 14:
        # turned toward us a little so the shields show their faces (side on they read as thin lines)
    cheer = lt >= CHEER
    for k in range(6):                                     # the rioters at the front: surge, slam, swarm through
        x0 = -2.0 + k * 0.62                                 # chat 14: 0.62 apart, three ranks (was 0.45: arms in backs)
        dx = 1.6 * ease((lt - 0.9) / 1.0) + 1.4 * push + back
        vault = k in (1, 4) and lt >= 1.95                 # round 1: two vault the shields (clear silhouettes)
        t_land = 1.95 + 0.12 * (k == 4) + 0.75            # chat 29: a 0.75 s vault (0.6: landing at 8 m/s)
        u = min(max((lt - t_land + 0.75) / 0.75, 0.0), 1.0) if vault else 0.0
        over = 1.8 * u                                     # chat 29: they stay over the line once landed (they
        d = 16.9 - MD + 0.65 * (k % 3)                     # snapped back 1.8 m at 2.75); their own depth throughout
        if vault and lt < t_land:
            out.append(Actor(f'rioter{k + 1}', 'rioter', x0 + dx + over, d, 90, 'run', t=lt, tier='t4',
                             lift=1.0 * math.sin(math.pi * u)))
            continue
        land = (lt - t_land) / 0.25 if vault else 1.0      # from the vault's run into the throw, 3 frames
        if cheer:
            u = 0.5 + 0.5 * math.sin(lt * 9 + k)
            out.append(Actor(f'rioter{k + 1}', 'rioter', x0 + dx + over, d, 60, 'cheer', u=u,
                             tier='t4', lift=_jump(lt, k)))
            continue
        state = 'run' if 0.9 < lt < 1.9 else 'throw'
        u = ((lt * 1.8) + (0, .29, .12, .87, 1.16, .99)[k]) % 1.0   # chat 29: 3 and 6 thrown through (arm low)
        # as the vaulters go over them (wound up, their arms were in the vaulters' bodies)
        out.append(Actor(f'rioter{k + 1}', 'rioter', x0 + dx + over, d, 90, state, u=u, t=lt + .35,
                         tier='t4').blend('run', t=t_land if vault else lt, w=land))
        # chat 18: +.35 starts the run on the step nearest the throw stance (feet snapped 68 cm)
    if not _PLATE:                                         # the end's background plate: just the riot
        out += selfie(lt) + buyers(lt) + granny(lt)
    out += surfer(lt)
    return out


def surf_pos(lt):
    """(x, z) of the riot shield under the surfer (depth SURF_D): hoisted out of the crowd 7.9-8.2, passed hand to
    hand left to right (lurching, not a glide), then tossed up and down on it through the hold."""
    t0, t1 = SURF
    rise = ease((lt - t0) / 0.3)
    u = ease(min(1.0, max(0.0, (lt - t0 - 0.2) / (t1 - t0 - 0.2))))
    x = lerp(SURF_X[0], SURF_X[1], u) + 0.12 * math.sin(lt * 9.0) * min(u * 8, 1.0)
    z = 1.95 * rise + 0.07 * math.sin(lt * 14 + 1)
    if lt > HOLD - 0.3:
        z += 0.55 * abs(math.sin((lt - HOLD + 0.3) * 6.2)) * ease((lt - HOLD + 0.3) / 0.3)   # the blanket toss
    return x, z


def surfer(lt):
    """The shield surfer: one of the crowd, flag up, riding a captured riot shield over everyone's heads."""
    if lt < SURF[0]:
        return []
    x, z = surf_pos(lt)
    return [Actor('surfer', 'rioter', x, SURF_D, 25 + 18 * math.sin(lt * 4.3), 'flag:albania', tier='t4', lift=z)]


def draw_surf_shield(img, lt):
    """The riot shield flat over the crowd, the arms of the people under it raised to hold it (drawn just before
    the surfer, after the crowd: from 6 m up the shield sits clear above the nearer rows' heads)."""
    if lt < SURF[0]:
        return
    cam = T4CAM
    x, z = surf_pos(lt)
    pen = IS.pen(img)
    for m in crowd_t4():
        dx, dd = field('t4', m['x'], m['d'], lt, m['ph'])
        mx, md = m['x'] + dx, m['d'] + dd
        if abs(mx - x) > 0.65 or abs(md - SURF_D) > 0.5 or z < 1.6:
            continue
        mz = _jump(lt, m['ph'] * 3) * (0.6 + 0.4 * (m['ph'] > 3))
        for sd in (-1, 1):
            sh = cam.p(mx + 0.17 * sd, md, 1.42 + mz)
            hand = cam.p(min(max(mx + 0.1 * sd, x - 0.5), x + 0.5), min(max(md, SURF_D - 0.28), SURF_D + 0.28), z)
            pen.line([sh, hand], INK, 9)
            pen.line([sh, hand], (44, 42, 50), 6)
            IS.ell(img, hand[0], hand[1], 4, 4, (226, 178, 146), INK)
    pts = [cam.p(x + px, SURF_D + pd, z) for px, pd in ((-0.55, 0.3), (0.55, 0.3), (0.55, -0.3), (-0.55, -0.3))]
    lip = [pts[3], pts[2], cam.p(x + 0.55, SURF_D - 0.3, z - 0.05), cam.p(x - 0.55, SURF_D - 0.3, z - 0.05)]
    S.shape(img, [lip], (150, 166, 180), INK, 2)
    S.shape(img, [pts], (206, 222, 232), INK, 2.5)
    band = [cam.p(x + px, SURF_D + pd, z) for px, pd in ((-0.55, 0.05), (0.55, 0.05), (0.55, -0.07), (-0.55, -0.07))]
    S.shape(img, [band], (40, 50, 120), None)


def _jump(lt, k):
    """The gleeful hold: everyone bouncing on their own beat (m off the ground)."""
    if lt < HOLD - 0.4:
        return 0.0
    return 0.42 * abs(math.sin(lt * 7.5 + k * 1.3)) * ease((lt - HOLD + 0.4) / 0.4)   # chat 27: was 0.22 ("nobody jumping")


def selfie(lt):
    """Gag b: watching the helicopter (back to us), turns his back on it at 1.2, phone up, peace sign; the flash
    at 1.8 with it spiralling down right behind his head (chat 27, notes hunt 1: at 2.6 it had already gone behind the
    ministry, so the gag was lost); checks the photo, thumbs up at 2.4; runs off to the melee at 3.25."""
    x, d = SELFIE
    if lt < 1.2:
        return [Actor('selfie', 'rioter', x, d, 180, 'stand', tier='t4')]
    if lt < 1.45:
        yaw = (135, 90, 45)[min(2, int((lt - 1.2) / 0.085))]
        return [Actor('selfie', 'rioter', x, d, -yaw, 'stand', tier='t4')]
    if lt < 3.25:                                  # chat 29: phone up over 3 frames (it snapped up: hands 14 m/s)
        u = ease((lt - 2.4) / 0.2)
        w = (lt - 1.45) / 0.25
        return [Actor('selfie', 'rioter', x, d, _turn(-45, 0, w), 'selfie', u=u, tier='t4').blend('stand', w=w)]
    a = lt - 3.25                                  # off into the melee, right, in front of the queue (chat 29: he
    if x + _getaway(a, 3.2) > 4.5:                 # set off at 4.5 m/s from a standstill, and ran through the queue)
        return []
    return [Actor('selfie', 'rioter', x + _getaway(a, 3.2), d - 0.25 * ease(a / 0.6), _turn(0, 90, a / 0.3), 'run',
                  t=lt, tier='t4')
            .blend('selfie', u=1.0, w=a / 0.25)]


ENTER = 2.2                                        # chat 29: they walk into the queue 2.2-3.1
Q_GAP = 0.72                                       # chat 29: the queue's spacing (0.62: strides overlapped)
BUYER_I = (3, 8, 13)                               # ordinary Tirana lads in colour: they read against the dark crowd


def buyer_x(k, lt):
    """Buyer k (0, 1, 2) in the queue: steps up a place once the one ahead has thrown and gone (0.3 s, walking)."""
    gone = [t0 + 0.8 for t0 in SALES]                 # chat 29: the one served throws, steps out of the way
    place, moving, still = k, False, ENTER + 0.9      # still: when they last stopped walking
    for j, tg in enumerate(gone[:k]):
        if lt >= tg + 0.3:
            place -= 1
            still = tg + 0.3
        elif lt >= tg:
            place -= ease((lt - tg) / 0.3)
            moving = True
    return SLOT[0] + Q_GAP * place, SLOT[1] + 0.12 * place, moving, still


def buyers(lt):
    """Gag a: three rioters queue at the cart from 2.6; each takes a lit bottle and throws it at once (the bank is
    to their left: they face it), then runs off right, in front of the queue (chat 29: they ran back through it and
    into the melee). They walk in from the crowd at the right over 0.9 s (was a 0.5 s dash: 7 m/s)."""
    out = []
    if lt < ENTER:
        return out
    for k, t0 in enumerate(SALES):
        name = f'buyer{k + 1}'
        if lt < t0:
            x, d, moving, still = buyer_x(k, lt)
            ent = ease((lt - ENTER) / 0.9)            # they come in from the right, into the queue
            if ent < 1 or moving:
                out.append(Actor(name, 'marcher', x + 1.2 * (1 - ent), d, -90, 'march', t=lt, tier='t4',
                                 i=BUYER_I[k]))
            else:                                     # feet together over 0.2 s as they stop
                out.append(Actor(name, 'marcher', x, d, -90, 'stand', tier='t4', i=BUYER_I[k])
                           .blend('march', t=still, w=(lt - still) / 0.2))
        elif lt < t0 + 0.45:
            x, d = SLOT
            out.append(Actor(name, 'marcher', x, d, -90, 'molotov', u=_throw_u(lt, t0), tier='t4', i=BUYER_I[k])
                       .blend('stand', w=(lt - t0) / 0.12))
        else:
            x, d = SLOT
            a = lt - t0 - 0.45
            run = _getaway(a, 2.8, 0.25)   # a step toward us out of the queue first, each its own lane
            if x + run > 4.5:                         # off the right edge
                continue
            out.append(Actor(name, 'marcher', x + run, d - (0.8 - 0.1 * k) * ease(a / 0.3), _turn(-90, 90, a / 0.3),
                             'run', t=lt, tier='t4', i=BUYER_I[k]).blend('molotov', u=1.0, w=a / 0.3))
    return out


def granny(lt):
    """Gag c: she steps up (5.7), pays, takes one (6.35), throws overarm (6.6): the highest arc of the film."""
    if lt < 5.7:
        return []
    x, d = SLOT
    if lt < 6.2:
        u = ease((lt - 5.7) / 0.5)
        return [Actor('granny', 'granny', x + 1.6 * (1 - u), d + 0.4 * (1 - u), -90,   # chat 29: from behind the
                      # last buyer's run-off (same line: they met) 'march' if u < 1 else 'stand', t=lt,
                      tier='t4', extra=_bag)]
    if lt < GRANNY_BUY:
        return [Actor('granny', 'granny', x, d, -90, 'stand', tier='t4', extra=_pay)]
    if lt < CHEER:
        u = ease((lt - GRANNY_BUY - 0.05) / 0.3)
        return [Actor('granny', 'granny', x, d, -90, 'molotov', u=u, tier='t4', extra=_bag)]
    return [Actor('granny', 'granny', x, d, -70, 'cheer', u=0.5 + 0.5 * math.sin(lt * 8), tier='t4', extra=_bag,
                  lift=_jump(lt, 9) * 0.4)]


def _bag(j):
    j['props'] = j.get('props', []) + [C.shopping_bag(j, 'L')]


def _pay(j):
    V.arm_to(j, 'R', (j['shR'][0] - 20, 180.0, 330.0), 'down')      # her hand out with the coins
    _bag(j)


def seller_j(lt):
    """The seller, front on behind his cart: lights each rag at the tin (his right hand), hands the bottle over to
    the queue on his left (screen right), applauds the granny's hit."""
    sp = C.tourist('seller')
    j = V.standing(sp)
    sw = j['shR'][0]
    if lt >= CHEER:
        g = 60 + 50 * (0.5 + 0.5 * math.sin(lt * 25))   # clapping: hands meet in front of his chest
        V.arm_to(j, 'R', (g, 140.0, 240.0), 'down')
        V.arm_to(j, 'L', (-g, 140.0, 240.0), 'down')
        return j
    for t0 in SALES + (GRANNY_BUY,):
        if t0 - 0.35 <= lt < t0 - 0.12:                  # dips the rag in the tin's flame
            V.arm_to(j, 'R', (sw + 60, 330.0, 150.0), 'down')
            C.grips.held(j, 'R', sp, C.bottle(j, 'R'))
            return j
        if t0 - 0.12 <= lt < t0:                         # holds it out to the buyer
            V.arm_to(j, 'R', (sw + 260, 200.0, 120.0), 'out')
            C.grips.held(j, 'R', sp, C.bottle(j, 'R'))
            return j
    return j


def sold(lt):
    return sum(1 for t0 in SALES + (GRANNY_BUY,) if lt >= t0 - 0.35)


def draw_cart(img, lt):
    cam = T4CAM
    if lt < 1.7:
        return
    x, d = CART
    x -= 3.2 * (1 - ease((lt - 1.7) / 0.8))           # he wheels it in from the left once the mopeds have gone
    gx, gy = cam.p(x, d)
    s = scale_at(cam, d)
    C.seller_scene(img, _cam2(), gx, gy - FEET * s, s, seller_j(lt), flame=(lt * 3) % 1.0, bottles=12 - sold(lt))


def t4_under(img, lt):
    """Drawn in the painting behind the ministry: the helicopter's fire trail and the fireball rising (3.0)."""
    if lt >= 1.0:
        for n in range(10):
            a = lt - 1.0 - n * 0.1
            if a < 0:
                continue
            h = heli_state(1.0 + n * 0.1)
            r = 20 + 30 * min(a, 1.2)
            S.smoke(img, [(h['x'] + 10, h['y'] - 10 - 30 * a, r)], (60, 40, 40), (96, 70, 66), lw=2)
    t4_fireball(img, lt)


def t4_fireball(img, lt):
    """The big fireball rising behind the ministry (7.5); its own function so the shape check draws it alone."""
    if lt >= T4_FIRE:                                      # chat 15: a layered fireball rising (was a flat disc)
        g = ease((lt - T4_FIRE) / 0.7)
        cx, cy = 720, lerp(640, 400, g)                    # chat 16 (hunt 2: flat disc cut by the edge): in frame,
        S.glow_disc(img, cx, cy, 160 * g + 60, (255, 190, 110), amt=.22)     # a smaller glow, a bigger smoke cap
        S.smoke(img, [(cx + 1.3 * dx * g, cy - 40 * g + 1.3 * dy * g, 1.3 * r * (0.4 + 0.6 * g)) for dx, dy, r in
                      ((0, -110, 120), (-130, -60, 90), (130, -70, 100), (-60, -200, 90), (80, -210, 90))],
                (70, 40, 36), (170, 96, 60), lw=2.5)
        S.flames(img, cx, cy + 140 * g + 60, 360 * (0.5 + 0.5 * g), 420 * (0.4 + 0.6 * g), lt, seed=95, n=7)
        S.flames(img, cx, cy + 80 * g + 40, 220 * (0.5 + 0.5 * g), 260 * (0.4 + 0.6 * g), lt + .3, seed=97, n=5)
        S.glow_disc(img, cx, cy + 40, 90 * g + 20, (255, 250, 200), amt=.5)


def t4_crowd(img, lt):
    cam = T4CAM
    for m in sorted(crowd_t4(), key=lambda m: -m['d']):
        dx, dd = field('t4', m['x'], m['d'], lt, m['ph'])
        x, d = m['x'] + dx, m['d'] + dd
        gx, gy = cam.p(x, d, _jump(lt, m['ph'] * 3) * (0.6 + 0.4 * (m['ph'] > 3)))   # the hold: they jump
        if gx < -80 or gx > W + 80:
            continue
        paste(img, 'marcher', m['i'], 't4', m['state'], 90, gx, gy, scale_at(cam, d))


def t4_mopeds(img, lt):
    cam = T4CAM
    for k in (1, 0):
        x, d = moped_pos(lt, k)
        gx, gy = cam.p(x, d)
        s = scale_at(cam, d)
        C.moped_scene(img, _cam2(), gx, gy - FEET * s, s, yaw=90, aim=38.0, fired=(k == 0 and lt >= 0.6), both=True)


def rpg_tip(lt):
    cam = T4CAM
    x, d = moped_pos(lt, 0)
    return cam.p(x - 0.1, d, 2.05)


def t4_fx(img, lt):
    # the rocket: fired 0.6, climbs the frame's height to the helicopter, hits 1.0; its smoke trail hangs
    if lt >= 0.6:
        x0, y0 = rpg_tip(0.6)
        hx, hy = R4(S.HELI_HOME[0], S.HELI_HOME[1])
        u = min(1.0, (lt - 0.6) / 0.4)
        N = 110                                            # chat 14: close-set lumps that taper to the head, grow
        n = int(N * u) + 1                                 # with age and drift up and right (no string of beads)
        lumps = []
        for k in range(n):
            v = k / N
            age = max(0.0, lt - 0.6 - v * 0.4)
            g = min(age, 2.0)
            r = 9 + 16 * g / (1 + 0.5 * g) + 2.5 * math.sin(k * 1.7)
            lumps.append((lerp(x0, hx, v) + 30 * g + 6 * math.sin(k * 2.3 + g * 3), lerp(y0, hy, v)
                          - 40 * math.sin(math.pi * v) - 18 * g, r))
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        S.smoke(lay, lumps, (190, 176, 170), (226, 214, 206), lw=2)
        fade = 1 - 0.75 * ease((lt - 1.4) / 2.0)          # the trail thins out once the helicopter is hit
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * fade)))
        img.alpha_composite(lay)
        if u < 1:
            rx, ry = lerp(x0, hx, u), lerp(y0, hy, u) - 40 * math.sin(math.pi * u)
            S.glow_disc(img, rx, ry, 26, (255, 230, 150), amt=.6)
    t4_hit(img, lt)
    if 0.6 <= lt < 1.1:                                    # chat 15: the backblast out of the launcher's rear
        a = (lt - 0.6) / 0.5
        tx, ty = rpg_tip(0.6)
        bx, by = tx - 150, ty + 120                         # behind and below the tube, along its line
        bl = Image.new('RGBA', img.size, (0, 0, 0, 0))     # chat 16 (hunt 2 read it as a boulder): soft, see-through
        S.smoke(bl, [(bx - 70 * a - 34 * q, by + 40 * a + 22 * q, 22 + 46 * a + 8 * q) for q in range(4)],
                (226, 220, 210), (250, 246, 240), line=None, lw=1)
        bl.putalpha(bl.getchannel('A').point(lambda v: int(v * 0.55 * (1 - a))))
        img.alpha_composite(bl)
        if a < 0.3:
            S.glow_disc(img, tx, ty, 40, (255, 230, 150), amt=.55)
    molotovs(img, lt)
    # melee dust and shield-impact flashes (1.6-3.0); ground fog and flares through
    if 1.5 < lt < 3.4:
        cam = T4CAM
        rng = np.random.default_rng(int(lt * 12))
        dl = Image.new('RGBA', img.size, (0, 0, 0, 0))     # chat 16 (hunt 2 read them as boulders): wide, low, soft
        for _ in range(3):                                 # round 1: fewer, lower (they hid the melee)
            x = rng.uniform(0.5, 4.0) + 1.2 * ease((lt - 2.0) / 1.0)
            sx, sy = cam.p(x, 17.6 - MD, 0.1)
            r = rng.uniform(26, 44)
            S.smoke(dl, [(sx - r * .6, sy, r * .7), (sx + r * .6, sy + 4, r * .6), (sx, sy - r * .3, r * .8)],
                    (176, 146, 120), (206, 178, 150), line=None, lw=1)
        dl.putalpha(dl.getchannel('A').point(lambda v: int(v * 0.35)))
        img.alpha_composite(dl)
        if int(lt * 12) % 3 == 0 and lt < 2.4:
            sx, sy = cam.p(rng.uniform(1.0, 2.0), 17.4 - MD, 1.2)
            S.glow_disc(img, sx, sy, 40, (255, 250, 220), amt=.6)
    cam = T4CAM
    for fx, fd in ((-5.2, 24.0), (-7.4, 30.0)):            # two red flares held up in the crowd (chat 14: on sticks,
        bx, by = cam.p(fx, fd, 1.9)                         # in the crowd, not red balls over the mopeds)
        tx, ty = cam.p(fx + 0.05, fd, 2.5)
        IS.poly(img, [(bx, by), (tx, ty)], None, (40, 30, 30), 4, 0)
        S.glow_disc(img, tx, ty, 34 + 5 * math.sin(lt * 20 + fd), (255, 70, 50), amt=.4)
        IS.ell(img, tx, ty, 5, 5, (255, 236, 220), None)
    flying_shield(img, lt)
    if 1.8 <= lt < 1.95:                                   # gag b: the selfie's flash, the helicopter falling behind him
        x, d = SELFIE                                      # chat 27: smaller, so his peace sign still reads through it
        fx, fy = cam.p(x - 0.05, d, 2.25)
        S.glow_disc(img, fx, fy, 30 * (1 - (lt - 1.8) / 0.15) + 12, (255, 255, 245), amt=.85)
    embers(img, lt)
    if lt >= FW0 - 0.2:
        for k, (t0, x, y, col) in enumerate(FIREWORKS):
            n = int((lt - t0) // 0.75)                       # each one bursts again every 0.75 s to the end
            for rep_ in (n - 1, n):                          # two rounds with the surf, then again for the hold
                if rep_ >= 0 and (rep_ < 2 or t0 + 0.75 * rep_ >= HOLD - 0.3):
                    burst(img, x + 40 * (rep_ % 3), y + 30 * (rep_ % 2), lt - t0 - 0.75 * rep_, col, k + rep_)


FIREWORKS = ((FW0 - 0.2, 260, 230, (255, 90, 70)), (FW0 + 0.05, 760, 150, (255, 250, 210)),   # over the
             (FW0 + 0.3, 520, 290, (110, 255, 150)), (FW0 + 0.5, 930, 300, (255, 200, 60)))    # headings


def t4_hit(img, lt):
    """The hit (0.98-1.3): a flash and a burst at the helicopter; its own function so the shape check draws it alone."""
    if 0.98 <= lt < 1.3:
        a = (lt - 0.98) / 0.32
        hx, hy = R4(S.HELI_HOME[0], S.HELI_HOME[1])
        S.glow_disc(img, hx, hy, 180 * (0.5 + a), (255, 230, 160), amt=.55 * (1 - a))
        S.flames(img, hx, hy + 46, 160 * (0.6 + a), 138 * (0.6 + a), lt, seed=91, n=6)


def burst(img, cx, cy, a, col, k):
    """One firework burst a seconds after it goes off: a flash, sixteen rays drooping as they fade (as T1's)."""
    if not 0 <= a < 0.6:
        return
    r = 26 + 90 * ease(a / 0.3)
    fade = 1 - a / 0.6
    S.glow_disc(img, cx, cy, r * 1.6, col, amt=.55 * fade)
    if a < 0.07:
        S.glow_disc(img, cx, cy, 70, (255, 255, 255), amt=.8)
        IS.ell(img, cx, cy, 14, 14, (255, 255, 255), None)
    dr = ImageDraw.Draw(img)
    droop = 50 * a * a / 0.36
    for n in range(16):
        ang = n * math.pi / 8 + k * 0.3
        ex, ey = cx + r * math.cos(ang), cy + r * math.sin(ang) + droop
        dr.line([(cx + .4 * r * math.cos(ang), cy + .4 * r * math.sin(ang) + droop * .5), (ex, ey)], fill=col, width=4)
        IS.ell(img, ex, ey, 4, 4, (255, 255, 240), None)


def embers(img, lt):
    """R5: sparks rising off the fires all through T4, drifting and flickering out (each loops on its own beat)."""
    rng = np.random.default_rng(77)
    n = 26 if lt < CHEER else 44
    for i in range(n):
        x0, y0, v, ph, life = rng.uniform(0, W), rng.uniform(900, 1300), rng.uniform(140, 260), rng.uniform(0, 9), \
            rng.uniform(1.2, 2.2)
        a = (lt + ph) % life
        x = x0 + 30 * math.sin(a * 3 + ph) + 40 * a
        y = y0 - v * a
        f = 1 - a / life
        if f > 0.15:
            S.glow_disc(img, x, y, 9 * f + 3, (255, 170, 60), amt=.5 * f)
            IS.ell(img, x, y, 2.5 * f + 1, 2.5 * f + 1, (255, 236, 160), None)


def _arc(p0, p1, apex, u):
    """A thrown thing's screen path: straight in x, a parabola in y peaking `apex` px above the higher end."""
    top = min(p0[1], p1[1]) - apex
    x = lerp(p0[0], p1[0], u)
    # a parabola through p0 (u 0), p1 (u 1) and the apex height
    yb = lerp(p0[1], p1[1], u)
    return x, yb - 4 * (min(p0[1], p1[1]) - top) * u * (1 - u)


def molotovs(img, lt, only=None):
    """Gag a (three buyers) and gag c (the granny): each bottle leaves the thrower's hand, tumbles along its arc
    into the bank and blooms orange; the fires stay, round and flickering; the granny's is the biggest."""
    cam = T4CAM
    shots = []
    for k, t0 in enumerate(SALES):
        hx, hy = cam.p(SLOT[0] - 0.25, SLOT[1], 2.15)
        shots.append((t0 + 0.27, t0 + 0.85, (hx, hy), land(k), 260, 1.0, k))
    hx, hy = cam.p(SLOT[0] - 0.2, SLOT[1], 1.95)
    shots.append((GRANNY_THROW, GRANNY_HIT, (hx, hy), land(3), 820, 1.9, 3))
    for t0, t1, p0, p1, apex, big, k in shots:
        if only is not None and k != only:                 # the shape check draws one bottle alone
            continue
        if t0 <= lt < t1:
            u = (lt - t0) / (t1 - t0)
            x, y = _arc(p0, p1, apex, u)
            ang = u * (9 + 3 * big)
            ca, sa = 26 * math.cos(ang), 26 * math.sin(ang)
            IS.poly(img, [(x + ca, y + sa), (x - ca, y - sa)], None, INK, 16, 0)
            IS.poly(img, [(x + ca, y + sa), (x - ca, y - sa)], None, (70, 140, 70), 11, 0)
            S.glow_disc(img, x + ca, y + sa, 34, (255, 190, 80), amt=.8)
            for q in range(1, 6):                          # a short trail of the rag's flame
                tx, ty = _arc(p0, p1, apex, max(0.0, u - q * 0.025))
                IS.ell(img, tx, ty, 9 - q, 9 - q, (255, 170 + 12 * q, 60), None)
        elif lt >= t1:
            a = lt - t1
            ex, ey = p1
            if a < 0.25:                                    # the bloom: a round flash, a ring pushing out
                g = ease(a / 0.25)
                S.glow_disc(img, ex, ey, (90 + 80 * g) * big ** 0.7, (255, 220, 120), amt=.7 * (1 - g) + .2)
                IS.ell(img, ex, ey, 40 * big * (1 - g) + 6, 40 * big * (1 - g) + 6, (255, 252, 230), None)
            g = min(1.0, a / 0.6)
            S.glow_disc(img, ex, ey - 20, (80 + 40 * g) * big, (255, 150, 50), amt=.35)
            S.flames(img, ex, ey + 34 * big, (90 + 50 * g) * big, (70 + 90 * g) * big, lt + k * .37, seed=93 + k, n=5)


def flying_shield(img, lt):
    """The melee's one clear gag: a riot shield knocked spinning up out of the line (2.15) and down behind it."""
    t0, t1 = 2.15, 3.15
    if not t0 <= lt < t1:
        return
    cam = T4CAM
    u = (lt - t0) / (t1 - t0)
    x0, y0 = cam.p(3.5, 17.6 - MD, 1.2)
    x, y = x0 + 260 * u, y0 - 820 * u + 900 * u * u
    ang = u * 9.0
    hw, hh = 34, 62
    pts = [(x + px * math.cos(ang) - py * math.sin(ang), y + px * math.sin(ang) + py * math.cos(ang))
           for px, py in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    S.shape(lay, [pts], (206, 222, 232), INK, 3)
    bx = [(x + px * math.cos(ang) - py * math.sin(ang), y + px * math.sin(ang) + py * math.cos(ang))
          for px, py in ((-hw, -10), (hw, -10), (hw, 6), (-hw, 6))]
    S.shape(lay, [bx], (40, 50, 120), None)
    a = np.asarray(lay.getchannel('A')).astype(np.float32) * 0.85
    lay.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(lay)


def backlight(img, lt, ppl):
    """T4 3.0-4.0: the fireball behind the ministry backlights the melee into one silhouette (F5)."""
    if lt < T4_FIRE:
        return ppl
    k = 0.5 * ease((lt - T4_FIRE) / 0.5)                     # chat 15: was 0.75 (the melee went to one grey smear)
    a = np.asarray(ppl).astype(np.float32)
    a[..., :3] = a[..., :3] * (1 - k) + np.array((40, 18, 20), np.float32) * k
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


# ================================================================================================= end
END = ('ea', 'eb', 'ec')        # round 1 (Sam R2): A the second moped, B the side alley, C the two riders
# Notes "## Round 1 plan", End scene + the acting list. A and C: the T4 frame itself (its painting, crowd, melee and
# fire, no mopeds) zoomed in on the bottom left and softened (a long lens: the riders sharp in front); the riders are
# drawn sharp through the zoom's own camera. B: the side alley (sets), the couple between the wall and the bins.
_PLATE = []                      # set while the T4 frame is drawn as the end's background (no T4 mopeds in it)
END_BG0 = T4_LEN                 # the T4 moment behind shot A's first frame; it runs on through A, then C
#                                  (round 2: straight on from the cut, was 2 s back to the hold's start)


class low_cam:
    """Round 2 (A3): the end scene's shots A and C look at the T4 riot through the old street-level long lens (a cut
    to a close-up; the wide T4 from 6 m up left only crowd and road behind the riders). Same world, other camera."""
    def __enter__(self):
        global RF4, T4CAM, R4
        self.keep = RF4, T4CAM, R4, S.CAMS['t4']
        RF4, T4CAM, R4 = RF4_LOW, RF4_LOW.cam, RF4_LOW.R
        S.CAMS['t4'] = S.CAM4_LOW

    def __exit__(self, *a):
        global RF4, T4CAM, R4
        RF4, T4CAM, R4, S.CAMS['t4'] = self.keep


def t4_plate(lt):
    _PLATE.append(1)
    try:
        with low_cam():
            return picture(at('t4', 0.0) + lt) if lt < T4_LEN else _t4_late(lt)
    finally:
        _PLATE.pop()


def _t4_late(lt):
    """T4 drawn past its own 10 s (the end scene's background runs on after the cut)."""
    global SHOTS
    keep = SHOTS
    SHOTS = [('t4', 0.0, 1e9)]
    try:
        return picture(lt)
    finally:
        SHOTS = keep


class Zoom:
    """A 2D zoom of a finished T4 frame: window from (x0, y0), k times; `cam` draws sharp people into it."""
    def __init__(self, k, x0, y0):
        self.k, self.x0, self.y0 = k, x0, y0
        c = RF4_LOW.cam                                    # round 2 (A3): the street-level lens (low_cam)
        self.cam = S.Cam(k * (c.VX - x0), k * (c.VY - y0), k * c.F, c.CH)

    def image(self, im, blur=2.2):
        k = self.k
        out = im.transform(im.size, Image.AFFINE, (1 / k, 0, self.x0, 0, 1 / k, self.y0), Image.BICUBIC)
        return out.filter(ImageFilter.GaussianBlur(blur)) if blur else out


ZA = Zoom(2.0, 330, 930)         # shot A: the bottom left of the T4 frame, the melee at the right behind
ZC = Zoom(2.6, 373, 1130)        # shot C: tighter on the riders
MOPED2_D = 10.1                  # the second moped's depth (about 2.1x the T4 riders on screen in A, 2.7x in C)
MOPED2_X = 0.31                  # where it stops (the driver over x 560 in A, 620 in C; the road at y ~1790)


def moped2_x(lt):
    """Shot A: skids in from the left, stops at 0.5 (ease out: braking hard)."""
    u = min(1.0, max(0.0, lt / 0.5))
    return lerp(MOPED2_X - 4.6, MOPED2_X, 1 - (1 - u) ** 3)


def rider_heads(tier, lt):
    """(driver head yaw, passenger head yaw, driver roll): None = with the body (facing right). A: on "Hey!" both
    snap round to the left in three drawings (1.8-2.1); C: the driver back to the passenger; the passenger to camera
    for the shrug (the acting list)."""
    if tier == 'ea':
        if lt < 1.8:
            return None, None, 0.0
        h = 45 if lt < 1.9 else 0 if lt < 2.0 else -45
        return h, (45 if lt < 1.85 else 0 if lt < 1.95 else -45), 0.0
    roll = -6.0 * math.sin(math.pi * min(1.0, max(0.0, (lt - 0.75) / 0.5)))   # the small tilt on "protest"
    return (-45 if lt < 0.1 else -30), (-45 if lt < 1.4 else 0), roll


def end_riders(img, tier, lt, z):
    cam = z.cam
    x = moped2_x(lt) if tier == 'ea' else MOPED2_X
    gx, gy = cam.p(x, MOPED2_D)
    s = scale_at(cam, MOPED2_D)
    aim = (38 + 24 * ease((lt - 0.3) / 0.4)) if tier == 'ea' else 62.0   # C: the cast sheet's shrug angle (45 folded his arm)
    dh, gh, roll = rider_heads(tier, lt)
    shrug_u = ease((lt - 1.4) / 0.6) if tier == 'ec' else 0.0
    fired = tier == 'ea' and lt >= 0.8                     # chat 27: shot C has already reloaded (the warhead reads as an RPG)
    C.moped_scene(img, _cam2(), gx, gy - FEET * s, s, yaw=90, aim=aim, fired=fired, both=True, drv_head=dh,
                  gun_head=gh, shrug_u=shrug_u, rim=C.RIM, drv_roll=roll)
    return gx, gy, s, aim


def skid_fx(img, lt, cam):
    """Shot A: tyre smoke and dust off the back wheel as it brakes (0.1-1.4), two skid marks left on the road."""
    x = moped2_x(lt)
    gx, gy = cam.p(x - 0.55, MOPED2_D)
    x0 = cam.p(moped2_x(0.25) - 0.55, MOPED2_D)[0]
    if lt > 0.25:
        pen = IS.pen(img)
        for dy in (-6, 6):
            pen.line([(x0, gy + dy), (gx, gy + dy)], (30, 22, 22), 7)
    if 0.1 < lt < 1.6:
        a = (lt - 0.1) / 1.5
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        rng = np.random.default_rng(7)
        puffs = []
        for q in range(7):
            age = a + q * 0.05
            px = gx - 60 - q * 70 * (0.5 + age) + rng.uniform(-20, 20)
            puffs.append((px, gy - 30 - 90 * age * (0.6 + 0.1 * q), 50 + 90 * age + 10 * q))
        S.smoke(lay, puffs, (150, 132, 124), (200, 186, 176), line=None, lw=1)
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * 0.7 * (1 - a))))
        img.alpha_composite(lay)


def rocket_fx(img, lt, rear, front):
    """Shot A: fired at 0.8: the backblast out of the rear, the rocket climbing out of the top right of the frame
    (gone by 1.05), its smoke trail hanging and drifting."""
    if lt < 0.8:
        return
    (rx, ry), (fx, fy) = rear, front
    dx, dy = fx - rx, fy - ry
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    a = (lt - 0.8) / 0.5
    if a < 1:                                              # the backblast: soft, see-through, out behind the tube
        bl = Image.new('RGBA', img.size, (0, 0, 0, 0))
        S.smoke(bl, [(rx - ux * (60 + 160 * a + 40 * q), ry - uy * (60 + 160 * a + 40 * q) + 30 * q * a,
                      30 + 80 * a + 12 * q) for q in range(4)], (226, 220, 210), (250, 246, 240), line=None, lw=1)
        bl.putalpha(bl.getchannel('A').point(lambda v: int(v * 0.6 * (1 - a))))
        img.alpha_composite(bl)
        if a < 0.45:                                       # chat 27 (notes hunt 1: "a stick, no flash"): a big muzzle flash
            S.glow_disc(img, fx, fy, 110 * (1 - a), (255, 150, 50), amt=.7)   # hunt 2: smaller white core (O6)
            S.glow_disc(img, fx, fy, 34 * (1 - a), (255, 240, 190), amt=.85)
    L = 2600.0                                             # the path: straight out along the tube, off the top
    u = min(1.0, (lt - 0.8) / 0.3)
    N = 200                                                # close-set lumps (chat 14: never a string of beads)
    lumps = []
    for k in range(int(N * u) + 1):
        v = k / N
        age = max(0.0, lt - 0.8 - v * 0.3)
        g = min(age, 2.0)
        r = 22 + 34 * g / (1 + 0.5 * g) + 4 * math.sin(k * 1.7)
        lumps.append((fx + ux * L * v + 40 * g + 8 * math.sin(k * 2.3 + g * 3), fy + uy * L * v - 24 * g, r))
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    S.smoke(lay, lumps, (190, 176, 170), (226, 214, 206), lw=2)
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * (1 - 0.5 * ease((lt - 1.4) / 1.0)))))
    img.alpha_composite(lay)
    if u < 1:
        S.glow_disc(img, fx + ux * L * u, fy + uy * L * u, 40, (255, 230, 150), amt=.7)


# --- the voices: Sam's takes when they exist (source/audio/protest-tiers-KEY.m4a), else espeak-ng stand-ins, for
# timing only and never heard in anything sent (best-practice "Straight to the animatic"): the captions carry them
VOICE_LINES = [dict(n=1, key='hey', who='husband', shot='ea', at=1.6, text='Hey!', es=['-v', 'en-us', '-s', '175', '-p', '45']),
               dict(n=2, key='tourists', who='husband', shot='eb', at=0.3,
                    text="We're just tourists! Why are y'all protesting?", es=['-v', 'en-us', '-s', '205', '-p', '45']),
               dict(n=3, key='bro', who='driver', shot='ec', at=0.2, text="Bro, what's a 'protest'?",
                    say="Bro, what's a protest?", es=['-v', 'en-us', '-s', '200', '-p', '30'])]


def _take(ln):
    import mossad_audio as MA
    name = 'protest-tiers-' + ln['key']
    if os.path.exists(os.path.join(HERE, 'audio', name + '.m4a')):
        return MA.line(name), True
    import shutil
    import subprocess
    path = os.path.join(HERE, 'data', 'standin-' + name + '.wav')
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not shutil.which('espeak-ng'):
            return np.zeros(int(MA.SR * len(ln['text'].split()) / 3.0)), False
        subprocess.run(['espeak-ng'] + ln['es'] + ['-w', path, ln.get('say', ln['text'])], check=True,
                       stdout=subprocess.DEVNULL)
    from burnham_film import load
    x = load(path)
    return x / (np.abs(x).max() + 1e-9) * 0.4, False


@lru_cache(None)
def voices():
    """The end scene's lines, each cut to its speech and placed at its moment: start, end, _voice, _stretches."""
    import mossad_audio as MA
    out = []
    for ln in VOICE_LINES:
        ln = dict(ln)
        x, real = _take(ln)
        st = MA.pauses(x, 0.12)
        a, b = max(0, int((st[0][0] - 0.05) * MA.SR)), min(len(x), int((st[-1][1] + 0.12) * MA.SR))
        x = x[a:b].copy()
        ln.update(_voice=x, _dur=len(x) / MA.SR, _stretches=MA.pauses(x, 0.18), real=real)
        ln['start'] = at(ln['shot'], ln['at'])
        ln['end'] = ln['start'] + ln['_dur']
        out.append(ln)
    return out


@lru_cache(None)
def mouth_track(who):
    import mouths
    return [(a + ln['start'], b + ln['start'], sh) for ln in voices() if ln['who'] == who
            for a, b, sh in mouths.track(ln['text'], ln['_stretches'])]


@lru_cache(None)
def head_life(who):
    import headlife
    import mossad_audio as MA
    env = np.zeros(int((DUR + 1) * FPS))
    n = MA.SR // FPS
    for ln in voices():
        if ln['who'] == who:
            v = ln['_voice']
            e = [np.sqrt(np.mean(v[i * n:(i + 1) * n] ** 2)) for i in range(len(v) // n)]
            i0 = int(round(ln['start'] * FPS))
            env[i0:i0 + len(e)] = e[:len(env) - i0]
    return headlife.HeadLife(env, 0.0, seed=17)


# --- shot B: the couple behind the bins
COUPLE = {'husband': (0.42, 3.2), 'wife': (-0.42, 3.2)}    # (x, d): the husband on the street side (screen right)


class Tourist(Actor):
    """The couple: their own dress (cast.tourist) and an acted pose per moment (end shot B)."""
    def __init__(self, who, lt):
        x, d = COUPLE[who]
        super().__init__(who, who, x, d, 18, 'stand', t=lt, tier='eb')
        self.who = who

    def sp(self):
        return C.tourist(self.who)

    def pose(self, sp):
        return tourist_pose(self.who, sp, self.t)


def crouch(who, lt):
    """How far each is sunk behind the bins (m): crouched; the husband rises a little at 0.3 for his line."""
    if who == 'wife':
        return 0.22
    return lerp(0.24, 0.06, ease((lt - 0.3) / 0.3))


def tourist_pose(who, sp, lt):
    j = V.standing(sp)
    t = at('eb', lt)
    if who == 'wife':                                      # the gasp at 0.0: her near hand to her mouth, held
        g = ease(lt / 0.25)
        hand = (-20.0, -150.0, 150.0)
        rest = j['wrL']
        V.arm_to(j, 'L', tuple(np.asarray(rest) + (np.asarray(hand) - np.asarray(rest)) * g), 'down', 'palm')
        j['head_roll'] = 3.0 * g
        j['nod'] = 0.0
        return j
    # the husband: palms out at "tourists" (0.6), one hand flicks toward the street on "protesting" (about 2.0)
    pal = ease((lt - 0.35) / 0.3)
    for side, sg in (('L', -1), ('R', 1)):
        rest = np.asarray(j['wr' + side])
        out = np.array((sg * 250.0, 170.0, 230.0))
        V.arm_to(j, side, tuple(rest + (out - rest) * pal), 'out', 'palm' if pal > 0.5 else 'fist')
    ln = voices()[1]
    fl = ease((t - (ln['start'] + ln['_stretches'][-1][0] + 0.35)) / 0.2)
    if fl > 0:                                             # "protesting": the hand on screen right out to the street
        rest = np.asarray(j['wrR'])                       # (his right arm is the one on screen right, front on)
        V.arm_to(j, 'R', tuple(rest + (np.array((430.0, 60.0, 160.0)) - rest) * fl), 'out', 'palm')
    roll, nod = head_life('husband').at_time(t)
    j['head_roll'], j['nod'] = roll, nod
    return j


def tourist_face(who, lt):
    """The acting list's faces: brows up and together, eyes looking right (to the riders); his mouth on his take."""
    t = at('eb', lt)
    if who == 'wife':
        f = dict(brow_up=0.05, frown=0.012, look=0.6 if lt > 0.5 else 0.2, smile=-0.6,
                 mouth='v:O' if lt < 0.5 else 'rest', blink=1.35 < lt < 1.45)
    else:
        import mouths
        f = dict(brow_up=0.045, frown=0.015, look=0.55, smile=-0.5, blink=0.05 < lt < 0.15)
        sh = mouths.at(mouth_track('husband'), t)
        f['mouth'] = 'rest' if sh == 'rest' else 'v:' + sh
    return f


def end_actors(tier, lt):
    if tier == 'eb':
        return [Tourist('husband', lt), Tourist('wife', lt)]
    return []


def end_picture(tier, lt):
    if tier == 'eb':
        back, front = S.alley(lt)
        cam = S.ALLEY_CAM
        ppl = Image.new('RGBA', back.size, (0, 0, 0, 0))
        for a in sorted(end_actors(tier, lt), key=lambda a: -a.d):
            s = scale_at(cam, a.d)
            gx, gy = cam.p(a.x, a.d)
            sp = dict(a.sp(), **tourist_face(a.who, lt))
            j = a.pose(sp)
            C.draw(ppl, _cam2(), gx, gy - FEET * s + crouch(a.who, lt) * cam.ppm(a.d), s, sp, j, a.yaw, a.who,
                   head=40 if a.who == 'husband' else 30)
        ppl.paste((0, 0, 0, 0), (0, 1300, W, H))            # below the lids they are hidden: no feet under the bins
        back.alpha_composite(ppl)
        back.alpha_composite(front)
        return back
    z = ZA if tier == 'ea' else ZC
    bg = END_BG0 + (lt if tier == 'ea' else 2.4 + 2.8 + lt)
    back = z.image(t4_plate(bg))
    if tier == 'ea':
        skid_fx(back, lt, z.cam)
    gx, gy, s, aim = end_riders(back, tier, lt, z)
    if tier == 'ea':
        rear, front = C.rpg_ends(_cam2(), gx, gy - FEET * s, s, 90, aim)
        rocket_fx(back, lt, rear, front)
    return back


END_CAM = {'ea': ZA.cam, 'eb': S.ALLEY_CAM, 'ec': ZC.cam}
# ================================================================================================= picture
def picture(t):
    """The frame WITHOUT the headlines (overlay puts those on last)."""
    _cam2()
    tier, lt = scene_of(t)
    S.ROUND_FIRE = tier == 't4' or tier in END            # round 1 (R5): Albania's fire is round, no spikes
    if tier in END:
        return end_picture(tier, lt)
    if tier == 't1':
        back, front = S.t1(lt)
        t1_people(back, lt)
        t1_fx(back, lt)
    elif tier == 't2':
        back, front = S.t2(lt, **t2_state(lt))
        back = RF2.image(back)
        front = RF2.image(front) if front is not None else None
        cam = RF2.cam
        acts = sorted(t2_actors(lt), key=lambda a: -a.d)
        t2_door(back, lt)
        t2_teeth(back, lt)
        bd, board = board_pose(lt)[1], False
        for a in acts:
            if not board and a.d < bd:                     # G7: the A-board in its place among the people
                t2_board(back, lt)
                board = True
            if a.prop and a.prop_before:
                a.prop(back, cam, a)
            draw_actor(back, cam, a)
            if a.prop and not a.prop_before:
                a.prop(back, cam, a)
        if not board:
            t2_board(back, lt)
        t2_fx(back, lt)
        phone_lights(back, acts, cam)
        blue_wash(back, lt)
    elif tier == 't3':
        back, front = S.t3(lt, car=False)
        back = reframe3(back)
        front = reframe3(front) if front is not None else None
        cam = T3CAM
        t3_crowd(back, lt)
        t3_columns(back, lt)                                # chat 15: smoke, then the truck, then its bikes, sharp
        S.truck(back, cam, truck_x(lt), T3_TRUCK_D, lt, 'drive', 'fr', 12, float(int(lt * 6) % 2))
        S._bikes(back, cam, 2.1, 14, lt)
        t3_debris(back)
        rear = S.CAR3[2] + car_move(lt)[1] + 1.0           # round 1: the car is drawn among the people (it rolls)
        acts = sorted(t3_actors(lt), key=lambda a: -a.d)
        for a in [a for a in acts if a.d > rear]:
            draw_actor(back, cam, a)
        t3_fx(back, lt)
        draw_car3(back, lt)
        car_fx(back, lt)
        for a in [a for a in acts if a.d <= rear]:
            draw_actor(back, cam, a)
    else:
        h = heli_state(lt)
        h['under'] = lambda img: t4_under(img, lt)
        back, front = S.t4(lt, heli=h)
        back = RF4.image(back)
        front = RF4.image(front) if front is not None else None
        cam = T4CAM
        ppl = Image.new('RGBA', back.size, (0, 0, 0, 0))
        t4_crowd(ppl, lt)
        for a in sorted(t4_actors(lt) + ([] if _PLATE else ['cart']) + ['shield'],
                        key=lambda a: -(CART[1] + 0.05 if a == 'cart' else SURF_D + 0.01 if a == 'shield' else a.d)):
            if a == 'cart':
                draw_cart(ppl, lt)
            elif a == 'shield' or a.name == 'surfer':
                pass                                        # drawn after the backlight (he is lit: the new action)
            else:
                draw_actor(ppl, cam, a)
        if not _PLATE:
            t4_mopeds(ppl, lt)
        back.alpha_composite(backlight(back, lt, ppl))
        if lt >= SURF[0] and not _PLATE:                    # round 2 (A2): the surfer lit (not in the end's A/C:
            # from street level he floated huge in the top corner)
            sx, sz = surf_pos(lt)
            gx, gy = cam.p(sx, SURF_D, sz + 1.2)
            S.glow_disc(back, gx, gy, 2.2 * cam.ppm(SURF_D), (255, 190, 110), amt=.3)
            draw_surf_shield(back, lt)
            for a in surfer(lt):
                draw_actor(back, cam, a)
        t4_fx(back, lt)
        if lt > 2.0:
            hy = 1230 if RF4 is RF4_LOW else 1477           # round 2 (A1): at the melee's feet in the raised T4
            haze(back, lt - 2.0, [(R4(x, hy), 220) for x in (100, 400, 700, 1000)], 0.3, (200, 170, 150), .1, 7)
        if lt > 3.0:                                        # chat 16 (hunt 2: no tear gas at the end): white gas at the line
            g = ease((lt - 3.0) / 0.6)
            gl = Image.new('RGBA', back.size, (0, 0, 0, 0))
            S.smoke(gl, [(cam.p(x, 19.5, 0.3)[0] + dx, cam.p(x, 19.5, 0.3)[1], 26 + 30 * g) for x in (4.2, 5.6, 7.0)
                         for dx in (-30, 30)], (226, 228, 226), (250, 250, 248), line=None, lw=1)
            gl.putalpha(gl.getchannel('A').point(lambda v: int(v * 0.4)))   # round 1: low, thin, behind the melee
            back.alpha_composite(gl)
    if front is not None:
        back.alpha_composite(front)
    return back


def draw_order(t):
    tier, lt = scene_of(t)
    names = {'t1': lambda: ['painting', 'police'] + [a.name for a in t1_actors(lt)] + ['march', 'fx', 'haze'],
             't2': lambda: ['painting'] + [a.name for a in sorted(t2_actors(lt), key=lambda a: -a.d)] + ['fx', 'blue'],
             't3': lambda: ['painting', 'truck', 'crowd'] + [a.name for a in sorted(t3_actors(lt), key=lambda a: -a.d)]
             + ['fx', 'car'],
             't4': lambda: ['painting', 'helicopter', 'ministry', 'crowd'] +
             [a.name for a in sorted(t4_actors(lt), key=lambda a: -a.d)] + ['mopeds', 'fx', 'haze']}
    if tier in END:
        return ['painting'] + [a.name for a in end_actors(tier, lt)] + ['fx']
    return names[tier]()


ACTORS = {'t1': t1_actors, 't2': t2_actors, 't3': t3_actors, 't4': t4_actors,
          'ea': lambda lt: end_actors('ea', lt), 'eb': lambda lt: end_actors('eb', lt),
          'ec': lambda lt: end_actors('ec', lt)}


def cam_for(t):
    tier = scene_of(t)[0]
    if tier in END:
        return END_CAM[tier]
    return {'t2': RF2.cam, 't3': T3CAM, 't4': T4CAM}.get(tier, S.CAMS[tier])


def project(cam, P):
    P = np.asarray(P, float)
    d = np.maximum(P[:, 2], 1e-3)
    return cam.VX + cam.F * P[:, 0] / d, cam.VY + cam.F * (cam.CH - P[:, 1]) / d, d


def scene(t):
    """Everyone live-drawn at time t as the audit's solids (the crowds are painted sprites: not in the audit)."""
    import audit
    tier, lt = scene_of(t)
    out = []
    for a in ACTORS[tier](lt):
        sp = a.sp()
        j = a.pose(sp)
        out.append(audit.Thing(a.name, audit.placed(a.name, j, a.x, a.d, facing(a.yaw), sp.get('height', 1.75),
                                                    lift=getattr(a, 'lift', 0.0), sp=sp)))   # chat 29: the audit
        # did not see a vault's or a jump's height (bodies in the air read as passing through the shields)
    if tier == 't2':
        out += shopfront(lt)
    return out


def shopfront(lt):
    """Round 2 (G4, chat 3): the gun shop's front as the audit's set pieces, so a person or a carried thing passing
    through the plinth, the walls, the door's frame, the glass (until the sign takes it) or the door (until the kick)
    is a fault every frame (rule 83, automatic). Before this the audit's solids were only people."""
    import audit
    import clipcheck as CC
    F, B = FRONT_D, FRONT_D + 0.3                       # the shop front's face and its back (metres from the camera)
    bx = lambda nm, x0, x1, y0, y1, z0=F, z1=B: CC.box('SHOPFRONT', nm, np.array((x0, y0, z0)),    # noqa: E731
                                                       np.array((x1, y1, z1)))
    parts = [bx('plinth', -2.2, 2.2, 0.0, 0.45), bx('wall left', -5.0, -2.2, 0.0, 3.55),
             bx('pier', 2.2, DOOR_X0 - 0.09, 0.0, 3.55), bx('jamb left', DOOR_X0 - 0.09, DOOR_X0, 0.0, DOOR_H + 0.09),
             bx('jamb right', DOOR_X1, DOOR_X1 + 0.09, 0.0, DOOR_H + 0.09), bx('wall right', DOOR_X1 + 0.09, 5.4, 0.0, 3.55),
             bx('lintel', DOOR_X0 - 0.09, DOOR_X1 + 0.09, DOOR_H + 0.09, 3.55), bx('fascia', -2.2, 2.2, 2.9, 3.55)]
    out = [audit.Thing('SHOPFRONT', parts, 'set')]
    if lt < T2_HIT + 0.1:
        out.append(audit.Thing('GLASS', [bx('glass', -2.0, 2.0, 0.45, 2.9, F, F + 0.03)], 'set'))
    if lt < T2_DOOR:
        out.append(audit.Thing('DOOR', [bx('door leaf', DOOR_X0, DOOR_X1, 0.0, DOOR_H, F, F + 0.05)], 'set'))
    return out


def solids(t):
    """clipcheck (rule 19): the same solids the audit sees (one list: scene()), so speed and teleports are checked."""
    return [x for th in scene(t) for x in th.solids]


# ------------------------------------------------------------------------------------------------- overlay
def _font(n):
    return ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)


def overlay(img, t):
    """The headlines (brief 2): white, country on the cut, location 0.5 s later underneath, top-left; round 1 (Sam
    R3): "Intensity Level: N/10" in red under them at 1.0 s; none in the end scene."""
    tier, lt = scene_of(t)
    if tier not in HEADLINES:                              # the end scene has no headings (round 1 plan): captions
        c = caption_at(t)
        if c:
            import subtitles
            subtitles.draw(img, c, ss=img.width / W)
        return img
    country, place = HEADLINES[tier]
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    k = img.width / W
    d.text((70 * k, 350 * k), country, font=_font(int(84 * k)), fill=(255, 255, 255), stroke_width=int(6 * k),
           stroke_fill=(0, 0, 0))
    if lt >= 0.5:
        d.text((72 * k, 452 * k), place, font=_font(int(44 * k)), fill=(255, 255, 255), stroke_width=int(4 * k),
               stroke_fill=(0, 0, 0))
    if lt >= 1.0:                                          # Sam R3 / O1 (16 Nov): bigger; the label at 1 s, white
        f = _font(int(54 * k))
        lab = 'Intensity Level: '
        d.text((72 * k, 514 * k), lab, font=f, fill=(255, 255, 255), stroke_width=int(5 * k), stroke_fill=(0, 0, 0))
        if lt >= INTENSITY_AT:                             # the number pops in (a short grow) in its tier's colour
            u = min(1.0, (lt - INTENSITY_AT) / 0.12)
            fn = _font(max(8, int(54 * k * (0.6 + 0.4 * u + 0.15 * math.sin(math.pi * u)))))
            x = 72 * k + d.textlength(lab, font=f)
            d.text((x, 514 * k + 27 * k), f'{INTENSITY[tier]}/10', font=fn, fill=INTENSITY_COL[tier],
                   stroke_width=int(5 * k), stroke_fill=(0, 0, 0), anchor='lm')
    img.alpha_composite(lay)
    return img


def frame_image(t):
    return overlay(picture(t), t)


# Rule 75: what the Hook Text (0.5-3.6 s, y ~1300) must never cover in T1
def _box_t1(x, d, z0, z1, w):
    cam = S.CAMS['t1']
    (ax, ay), (_, by) = cam.p(x - w / 2, d, z1), cam.p(x, d, z0)
    return (ax, ay, ax + w * cam.ppm(d), by)


KEEP_CLEAR = [('the burning skip', lambda t: _box_t1(-7.0, 176, 0, 5.0, 3.0) if t < 6 else None),
              ('the bursts over the line', lambda t: _box_t1(0.0, 152, 4.0, 9.5, 20.0) if 1.2 < t < 2.0 else None),
              ('the police line', lambda t: _box_t1(2.0, 185, 0, 2.0, 26.0) if t < 4 else None)]


# ------------------------------------------------------------------------------------------------- sound
def ding(sr):
    """A soft bell: two sine partials (E6 and its bright overtone), a 6 ms rise and a 0.9 s fade; quiet (peak 0.22)."""
    t = np.arange(int(0.9 * sr)) / sr
    env = np.minimum(1.0, t / 0.006) * np.exp(-t * 5.5)
    return 0.22 * env * (np.sin(2 * np.pi * 1318.5 * t) + 0.35 * np.sin(2 * np.pi * 3955.5 * t) * np.exp(-t * 6))


def soundtrack(stems=False):
    """The siren (the brief names it, on the T2 blue wash) and the intensity dings (Sam O1); no other effects."""
    import mossad_audio as MA
    n = int((DUR + 0.3) * MA.SR)
    mix = np.zeros(n)
    try:
        import filmkit
        s = MA.load(SIREN) if hasattr(MA, 'load') else None
        if s is not None:
            filmkit.place(mix, s[:int(1.2 * MA.SR)] * 0.6, at=at('t2', T2_WASH), sr=MA.SR)
    except Exception as e:                                  # the film still renders; the fault is printed
        print('SOUND: siren not placed:', e)
    dg = ding(MA.SR)                                        # Sam O1 (16 Nov): a gentle ding as each number appears
    for tr in TIERS:
        i = int(at(tr, INTENSITY_AT) * MA.SR)
        mix[i:i + len(dg)] += dg[:max(0, n - i)]
    for ln in voices():                                     # Sam's takes only: a stand-in is never heard
        if ln['real']:
            i = int(ln['start'] * MA.SR)
            mix[i:i + len(ln['_voice'])] += ln['_voice'][:max(0, n - i)]
    return mix


# Rule S7: each tier's effects drawn alone on a clear frame at the moment they peak, shape-tested (viewchecks)
def _fx_at(fn, lt, *args):
    """One effect drawn alone for the shape check, as the film draws it, and only what shows (chat 30).
    T4's fire is round only while S.ROUND_FIRE is on (chat 29). Each entry draws only its own effect (chat 30: the
    whole fx layer's scatter of embers, flares and trails read as a star), and the test sees only visible pixels:
    glow_disc leaves an opaque, unchanged square round each disc on a clear layer, so the effect is drawn on black and
    on white and kept where either changed."""
    def draw(img):
        keep = S.ROUND_FIRE
        S.ROUND_FIRE = fn in (t4_hit, molotovs, t4_fireball)
        seen = np.zeros((img.size[1], img.size[0]), bool)
        try:
            for bg in ((0, 0, 0, 255), (255, 255, 255, 255)):
                lay = Image.new('RGBA', img.size, bg)
                fn(lay, lt, *args)
                d = np.abs(np.asarray(lay.convert('RGB'), np.int16) - np.array(bg[:3], np.int16)).max(-1)
                seen |= d > 24
        finally:
            S.ROUND_FIRE = keep
        out = np.zeros((img.size[1], img.size[0], 4), np.uint8)
        out[seen] = (255, 255, 255, 255)
        img.alpha_composite(Image.fromarray(out, 'RGBA'))
    return draw


EFFECTS = [('T1 firework string', 'trail', _fx_at(t1_fx, 1.2)), ('T1 three bursts', 'burst', _fx_at(t1_fx, 1.95)),
           ('T1 tear-gas haze', 'smoke', _fx_at(t1_fx, 3.6)), ('T2 sign-on-glass flash', 'flash', _fx_at(t2_flash, 1.05)),
           ('T3 stones and gas', 'sparks', _fx_at(t3_fx, 1.6)), ('T3 gas and jet', 'smoke', _fx_at(t3_fx, 3.0)),
           ('T4 rocket trail', 'trail', _fx_at(t4_fx, 0.9)), ('T4 helicopter hit', 'burst', _fx_at(t4_hit, 1.1)),
           ('T4 first Molotov bloom', 'burst', _fx_at(molotovs, SALES[0] + 0.95, 0)),
           ("T4 granny's Molotov", 'burst', _fx_at(molotovs, GRANNY_HIT + 0.1, 3)),
           ('T4 fireball', 'burst', _fx_at(t4_fireball, T4_FIRE + 0.5))]


# Rule 18: the props a beat needs, measured on screen where they act (world x, height, depth; size in metres)
JOKE_PROPS = [('red crowbar', [at('t2', 0.6), at('t2', 1.0)], (-0.7, 1.6, 13.6), 1.0),
              ('WAFFEN sign', [at('t2', 1.0), at('t2', 3.0)], (0.0, 3.6, 14.0), 0.5),
              ('WAFFEN RAUS placard', [at('t2', 1.5), at('t2', 2.5)], (-1.38, 2.0, 7.8), 0.45),
              ('BANKA sign', [at('t4', 0.5), at('t4', 1.5)], (-9.0, 5.2, 52.0), 0.95)]


# Rule 3: the sets' benchmark (sets stage, ticked on its sheet beside the references) in the form benchmark.py reads
BENCHMARK = [dict(place=S.TITLES[tier], refs=[f'references/protest-tiers/{r}.jpg' for r in S.REFS_OF[tier]],
                  at=at(tier, 0.4),
                  items=[(w, 'built: sets stage, ticked on its sheet (critique passes 1-2)') for w in S.BENCHMARK[tier]])
             for tier in TIERS]
# real sizes (sizes.py): the one prop drawn from a size in metres that the table knows; everything else is drawn
# through the set's camera at the reference's size (sets stage)
PROP_SIZES = [('T2 A-board', 'pavement a-board', 0.72, 1.15, None)]
LINE_OK = [('rioter t2', 'line weight', 540, 731)]   # notes "## Exceptions": the black-bloc eye slits
OUTFIT = {}                       # hoodies, jackets, riot kit: no skirt, jacket hem or cuffs to place (as Elder Swindon)


def LINE_SUBJECTS():
    """Each of the cast's kinds alone, large (linecheck.py): the officers of each tier, a rioter, a marcher."""
    cam = S.Cam(540, 788, 2280, 1.6)

    def one(kind, tier, force):
        return lambda img: draw_actor(img, cam, Actor(f'{kind} {tier}', kind, 0.0, 4.0, 20, 'stand', tier=tier,
                                                      force=force))
    return [(f'{k} {t}' + (f' {f}' if f else ''), one(k, t, f)) for k, t, f in (
        ('officer', 't1', 'mossos'), ('officer', 't3', 'crs'), ('officer', 't4', 'policia'), ('rioter', 't2', None),
        ('marcher', 't1', None), ('marcher', 't3', None))]


# chat 17 (pre-flight): the three crowd moments the staging means, looked at full size (notes "## Exceptions")
# chat 18: the run-in is a real sprint (bodies 6.2 m/s at most, dash()); a sprinter's feet, shins and arms swing at up
# to twice the body's speed, past clipcheck's 7 m/s walking cap (Exceptions row 'FAST_OK')
# round 1: written in shot time (at()), so the re-time to 4/6/8/10 s moved them with the action
FAST_OK = ([(p, at('t2', 0.0), at('t2', 0.9)) for p in ('hauler*', 'runner*', 'swinger')]
           + [(p, at('t3', 2.7 + J3), at('t3', 8.0)) for p in ('front*',)]   # T3 run-out: the same sprint from the jet
           + [(f'rioter{k}.foot{sd}', at('t4', 0.9), at('t4', 1.9)) for k in range(1, 7) for sd in 'LR']   # T4 surge
           # chat 29: the T4 runners (the vault's leap, the selfie and the buyers off right): the same sprint legs; a
           # buyer's upper arm pumps at 7.2-7.4 m/s; their snaps (turns, pose changes) were fixed, bodies still checked
           + [(f'{w}.{part}{sd}', t0, t1) for w, t0, t1, parts in (
               ('rioter2', at('t4', 1.9), at('t4', 2.8), ('thigh', 'shin', 'foot')),
               ('rioter5', at('t4', 1.9), at('t4', 2.9), ('thigh', 'shin', 'foot')),
               ('selfie', at('t4', 3.25), at('t4', 6.0), ('thigh', 'shin', 'foot')),
               ('buyer1', at('t4', SALES[0] + 0.45), at('t4', 6.0), ('thigh', 'shin', 'foot', 'arm')),
               ('buyer2', at('t4', SALES[1] + 0.45), at('t4', 7.0), ('thigh', 'shin', 'foot', 'arm')),
               ('buyer3', at('t4', SALES[2] + 0.45), at('t4', 8.0), ('thigh', 'shin', 'foot', 'arm')))
              for part in parts for sd in 'LR']
           # chat 29: round 1's new runners, the same sprint (legs only: thighs, shins, feet at 2-2.8x the body's
           # speed; their turns and arms were snaps and are fixed, so arms and bodies are still checked)
           + [(f'{w}{k}.{part}{sd}', t0, t1) for w, ks, t0, t1 in (
               ('back', (1, 2, 3), at('t3', 2.75 + J3), at('t3', 8.0)),
               ('pusher', (1, 2, 3, 4), at('t3', CAR_T0 - PUSH_IN - 0.1), at('t3', CAR_T0 + 0.2)),
               ('pusher', (1, 2, 3, 4), at('t3', CAR_LET + 0.4), at('t3', 8.0)))
              for k in ks for part in ('thigh', 'shin', 'foot') for sd in 'LR']
           # the stone throws: a throwing hand really reaches ~20 m/s (clipcheck caps it at 12, the forearm at 10)
           + [(f'{w}{k}.{part}{sd}', t0, t1) for w, ks, t0, t1 in (
               ('runner', range(1, 6), at('t2', 0.6), at('t2', T2_FREEZE + 0.05)),
               ('hauler', (1, 2), at('t2', 1.2), at('t2', T2_FREEZE + 0.05)),
               ('front', range(1, 5), at('t3', 0.7), at('t3', 2.65 + J3)),
               ('rioter', range(1, 9), at('t4', 0.0), at('t4', T4_LEN)))
              for k in ks for part in ('hand', 'forearm') for sd in 'LR'])
# round 1 (chat 26, notes "## Exceptions"): who comes on in mid-frame for a reason the audit cannot see
ALLOWED_POPS = [(n, at('t2', tin + 0.3), at('t2', tin + 0.5), 'into the dark shop through its door (G4)')
                for n, (tin, tout, *_) in DOOR_IN.items()] + [
                (n, at('t2', tout - 0.05), at('t2', tout + 0.15), 'out of the dark shop through its door (G4)')
                for n, (tin, tout, *_) in DOOR_IN.items()] + [
                ('back*', at('t3', VOLLEY2 - 0.35), at('t3', VOLLEY2), 'step up out of the packed crowd behind'),
                ('buyer*', at('t4', ENTER), at('t4', ENTER + 0.15), 'step out of the packed crowd into the queue'),
                ('granny', at('t4', 5.7), at('t4', 5.85), 'steps out of the packed crowd to the cart'),
                ('surfer', at('t4', SURF[0]), at('t4', SURF[0] + 0.15), 'hoisted up out of the packed crowd (A2)')]
# chat 29: these were TOUCHES (a hand meant to be ON a thing, checked every frame); they are crowd crushes the
# audit should allow, not hand contacts, so the touch check found 5-900 cm gaps: allowed contacts, depth-capped
ALLOWED_CONTACTS = [('swinger', 'GLASS', at('t2', T2_HIT - 0.1), at('t2', T2_HIT + 0.1), 'G3: the sign meets the glass', 0.30),
           ('hauler1', 'DOOR', at('t2', T2_DOOR - 0.1), at('t2', T2_DOOR), 'G4: the kick on the door', 0.25),
           ('hauler*', 'runner*', at('t2', 0), at('t2', .85), 'T2 run-in: the raiders crush through one gap in the glass', 0.18),
           ('hauler*', 'hauler*', at('t2', 0), at('t2', .85), 'T2 run-in: the haulers drop the shutter and pile in', 0.12),
           ('runner*', 'runner*', at('t2', 0), at('t2', T2_FREEZE + .75), 'T2 run-in: the raiders crush through one gap; packed inside', 0.18),
           ('runner*', 'swinger', at('t2', 0), at('t2', .85), 'T2 run-in: the swinger is in the crush', 0.10),
           ('front*', 'front*', at('t3', 2.7 + J3), at('t3', 3.3 + J3), 'T3 run-out: the front line breaks and runs left as a pack', 0.04),
           ('policia*', 'rioter*', at('t4', 0), at('t4', T4_LEN - .05), 'T4 melee: rioters slam into the shields (brief 26)', 0.20),
           ('policia*', 'policia*', at('t4', 2), at('t4', T4_LEN - .05), 'T4 melee: the shield line buckles back into itself', 0.06)]
ORDER_SWAPS = [(a, b, t0, t1, w) for a, b, t0, t1, w in (
    ('hauler*', 'runner*', at('t2', 0), at('t2', .85), 'T2 run-in: they cross in the crush'),
    ('hauler*', 'hauler*', at('t2', 0), at('t2', .85), 'T2 run-in'), ('runner*', 'runner*', at('t2', 0), at('t2', .85), 'T2 run-in'),
    ('runner*', 'swinger', at('t2', 0), at('t2', .85), 'T2 run-in'), ('hauler*', 'swinger', at('t2', 0), at('t2', .85), 'T2 run-in'),
    ('front*', 'front*', at('t3', 2.7 + J3), at('t3', 3.3 + J3), 'T3 run-out'),
    ('crs*', 'front*', at('t3', 2.7 + J3), at('t3', 3.3 + J3), 'T3 run-out'),
    ('policia*', 'policia*', at('t4', 2.0), at('t4', 2.3), 'T4 melee: the line buckles'),
    ('policia*', 'rioter*', at('t4', 2.0), at('t4', 2.3), 'T4 melee: rioters break through the line'))]
ALLOWED = [(a, b, t0, t1) for a, b, t0, t1, *_ in ALLOWED_CONTACTS]   # clipcheck reads the same meant contacts


# ================================================================================================= checks / main
def checks():
    S.checks()
    return []


def audits():
    import audit
    return [x[len('AUDIT: '):] for x in audit.check(sys.modules[__name__])]


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    if a[0] == 'stills':
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'check':
        checks()
        print('\n'.join('AUDIT: ' + f for f in audits()) or 'audit: clean')
    elif a[0] == 'final':
        import film_engine as E
        import mossad_audio as MA
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', 1), crf=26 if small else 20,
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)
        print(f'finish it with  python3 source/finish.py {a[1]} OUT.mp4 --film {NAME}')


if __name__ == '__main__':
    main()
