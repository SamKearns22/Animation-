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
LENS = (('t1', 6.0), ('t2', 8.5), ('t3', 8.0), ('t4', 12.5), ('ea', 2.4), ('eb', 2.8), ('ec', 3.4))   # A12: C +1 s for the shrug after the line
TIERS = ('t1', 't2', 't3', 't4')
SHOTS, _t = [], 0.0
for _n, _l in LENS:
    SHOTS.append((_n, _t, round(_t + _l, 3)))
    _t = round(_t + _l, 3)
DUR = _t
BLACK_AT = DUR
START = {n: t0 for n, t0, _ in SHOTS}
J3 = 0.95                    # T3: the water cannon's beat (round 4, F23: truck in from 2.0, jet on 3.5, it sweeps the
                             # rioters 3.55-7.0 so the action spreads through the shot; was 1.95: all of it at the end)


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


def make_person(kind, i=0, tier='t1', force=None, seed=None):
    if kind in C.TOURIST_DRESS:                     # round 1: granny, seller, the tourists
        return C.tourist(kind)
    if kind == 'officer':
        if not seed and tier == 't3' and i >= 10:           # round 4 (F13): the reserve's sprites each their own man
            seed = f'reserve{i}'
        return C.officer(force, seed=seed, tier=tier) if seed else C.officer(force)
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
    if state.startswith('p:'):                             # round 3 (A4): any cast pose at a fixed step, 'p:NAME:U'
        _, nm, uu = state.split(':')
        return C.pose(sp, nm, float(uu), 0.0, force)
    if state.startswith('shield_up:'):                    # round 4 (F13): a reserve sprite with its shield raised
        return C.pose(sp, 'shield_up', float(state.split(':')[1]), 0.0, force)
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
        # round 4 (F12): already pressed up behind the front line at the first frame (no surge in); F22: no sliding
        # away from the jet: the crowd stays and protests, only the acted rioters it strikes run
        dx += 0.55 + 0.12 * math.sin(2 * math.pi * 0.8 * t + ph * 1.7)
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
        self.spr = False                            # round 3 (A4): drawn from a cached sprite (p:NAME:U states)

    def blend(self, state, u=0.0, t=0.0, w=1.0):
        """Chat 29 (pre-flight: 107 teleports and snaps): pass from another pose into this one over a few frames."""
        if w < 1.0:
            self.mix = (state, u, t, max(0.0, w))
        return self

    def sp(self):
        if self.kind == 'rioter':                   # Sam O4: each rioter their own face, from their city's mix
            return make_person('rioter', self.i, self.tier, force=self.name)
        if self.kind == 'officer' and self.tier == 't3':   # round 3 (F5): each French officer his own build and kit
            return make_person('officer', self.i, 't3', self.force, seed=self.name)
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
    if a.spr:                                       # round 3 (A4): a crowd member pasted from its cached sprite
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0)) if a.clip else img
        paste(lay, a.kind, a.i, a.tier, a.state, a.yaw, gx, gy, s, force=a.name if a.kind == 'rioter' else a.force)
        if a.clip:
            m = Image.new('L', img.size, 0)
            ImageDraw.Draw(m).rectangle(a.clip, fill=255)
            lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay.getchannel('A')), np.asarray(m))))
            img.alpha_composite(lay)
        return None
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


def draw_prop(img, cam, a):
    """What someone carries, cut to the door's opening while they are inside (G14: the stock showed through the wall)."""
    if not a.clip:
        return a.prop(img, cam, a)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    a.prop(lay, cam, a)
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).rectangle(a.clip, fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.asarray(lay.getchannel('A')), np.asarray(m))))
    img.alpha_composite(lay)


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
T2_HIT = 1.6                        # G3: the sign meets the glass (the first of four hits, G13)
# G13 (Sam: he broke it in one, then just flapped the sign about): four hits in four places, more cracks each time,
# the fourth goes through. (time, his x, u at contact, yaw, star (x, height) measured off the sign's head at contact)
SIGN_HITS = ((1.6, 0.2, 0.55, 125, (0.8, 1.92)), (2.05, 0.0, 0.45, 125, (0.05, 2.06)),
             (2.5, 0.3, 0.65, 125, (1.13, 1.63)), (2.95, -0.3, 0.6, 125, (0.4, 1.79)))
T2_SHATTER = SIGN_HITS[-1][0]       # the glass goes (it was T2_HIT)
SIGN_DROP = 3.2                     # G13: he flings the sign down, then celebrates and loots
T2_DOOR = 2.45                      # G4: hauler1's foot on the door
DOOR_X0, DOOR_X1, DOOR_H = S.DOOR2
DOOR_C, FRONT_D = (DOOR_X0 + DOOR_X1) / 2, 14.0
T2_SW = (0.2, 12.7)                 # the swinger's mark (the sign's head reaches the glass at T2_HIT)
T2_STAR = (0.8, 1.92)               # where it meets the glass (x, height); chat 3: on the sign's head at T2_HIT
BOARD = (-0.4, 12.75)               # G22 (Sam: 'move the sign right a little'): was -0.7. G7: the A-board, kicked at BOARD_KICK, lands at BOARD_LAND
BOARD_KICK, BOARD_LAND, BOARD_TO = 2.42, 3.17, (1.3, 9.8)   # G22: leaves on the foot's strike (u 0.6 of the kick); G18 (Sam: "flies further"): 0.75 s, 3.4 m (was 1.9), toward us and right, low past the swinger
# G2: stones thrown from off frame left and near: (hits the glass at, x, height)
T2_STONES = ((0.35, -1.4, 1.6), (0.5, 0.6, 2.0), (0.62, -0.4, 1.2), (0.8, 1.3, 1.7), (0.95, -1.0, 2.2), (1.1, 0.2, 1.4))
# G15 (Sam: 'some rocks hit the upper window'): three thrown from off right and near at the lit first-floor window
# (x 2.2-3.5, height 5.0-7.4 on the front): two chip it, the third goes through. (hits at, x, height)
UP_STONES = ((3.9, 2.6, 6.7), (4.5, 3.15, 5.6), (5.2, 2.8, 6.2))
UP_FROM = (4.8, 9.2, 1.8)            # off the frame's right edge, near us: where they are thrown from
# G9 (FAZ 31 Oct: two weapons taken): who takes which pistol: (cubby column, row height, when it leaves its cubby)
GUN_RUN = {'runner1': ((0.9, 12.0), (-4.0, 9.9)), 'runner2': ((4.5, 10.0),), 'swinger': ((-5.0, 13.0),)}   # G21: each one's way out (off frame); runner1 clear of the swinger first
TAKE = {'runner1': (6, 0.98, 3.6), 'runner2': (8, 1.35, 3.75), 'swinger': (4, 0.98, 4.85)}   # G13: after the shatter
# G4/G5: the four who go in through the door come back out of it with stock: (in at, out at, lane, prop)
# chat 3: out 1 s apart in one lane clear of the wall and the swinger (0.5 s apart, they walked into each other)
DOOR_IN = {'hauler1': (2.75, 4.6, 13.4, 'crate'), 'hauler2': (3.15, 6.6, 13.4, 'crate'),
           'runner4': (3.5, 5.6, 13.4, 'boxes'), 'runner5': (3.75, 7.6, 13.4, 'boxes')}
IN_D, IN_SIDE = 15.2, DOOR_X0 - 0.7     # G14: how far in they run, and where they go to behind the wall
OUT_D = 16.0                         # G14: they come back further in (0.8 m behind anyone still going in)
# G17: each one's own way out, four directions: right along the shop front, toward us and right, toward us and left,
# and straight at us (hauler2 and runner5 are still in sight as the scene cuts)
EXIT = {'hauler1': (6.5, 13.2), 'runner4': (5.2, 10.4), 'hauler2': (-4.2, 10.9), 'runner5': (0.6, 9.9)}


def swinger_swing(tt):
    """G13: (his x, the swing's u, yaw) from his mark (0.85 s) to SIGN_DROP: wind up, then each hit: the swing in to
    the contact u, a jolt back off the glass and round again, a half step to the next place; the last goes through."""
    if tt < 1.35:
        return T2_SW[0], 0.25 * ease((tt - 0.95) / 0.4), 125
    prev = (1.35, T2_SW[0], 0.25, 125)
    for th, x, uc, yaw, _ in SIGN_HITS:
        t0, x0, u0, _y = prev
        if tt < th:                                         # winding back to 0.1 then swinging in to the glass
            w = (tt - t0) / (th - t0)
            if w < 0.45:
                return lerp(x0, x, ease(w / 0.45)), lerp(u0, 0.1, ease(w / 0.45)), yaw
            return x, lerp(0.1, uc, ease((w - 0.45) / 0.55) ** 1.6), yaw
        if th == T2_SHATTER:
            if tt < th + 0.15:                              # through: the follow-through
                return x, uc + (1 - uc) * ease((tt - th) / 0.15), yaw
            return x, 1.0 - 0.1 * ease((tt - th - 0.15) / 0.2), yaw
        if tt < th + 0.06:                                  # the jolt: held on the glass a beat
            return x, uc, yaw
        prev = (th + 0.06, x, uc - 0.08, yaw)
    return SIGN_HITS[-1][1], 0.9, 125


def t2_state(lt):
    return dict(shutter=0.5 + 0.5 * ease((lt - 1.0) / 0.5),
                glass='whole' if lt < T2_SHATTER else 'starred' if lt < T2_SHATTER + 0.1 else 'gone',
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
    """G4: in through the door and, later, out of it with the stock. G14 (Sam: they vanished mid-frame): in, they run
    on to IN_D and then sideways behind the wall to the door's left (the opening's clip hides them as they pass the
    jamb), and come back the same way. G17 (Sam: 'sprint out in different directions, fleeing'): out of the door at
    a burst, then a flat-out sprint to their own EXIT. -> (x, d, yaw, state, inside) or None while out of sight."""
    t_in, t_out, lane, _ = DOOR_IN[name]
    if t_in <= tt < t_in + 0.5:                             # through the doorway, away from us
        d = lerp(13.35, IN_D, (tt - t_in) / 0.5)
        return DOOR_C, d, 180, 'run', d > FRONT_D - 0.2
    if t_in + 0.5 <= tt < t_in + 0.9:                       # G14: round the corner inside, behind the wall
        return lerp(DOOR_C, IN_SIDE, ease((tt - t_in - 0.5) / 0.4)), IN_D, -100, 'run', True
    if tt < t_out - 0.4:
        return None
    if tt < t_out:                                          # G14: back from behind the wall to the doorway, laden
        return lerp(IN_SIDE, DOOR_C, ease((tt - t_out + 0.4) / 0.4)), OUT_D, 100, 'carry_run', True
    a = tt - t_out
    if a < 0.5:                                             # G17: bursting out of the door toward us
        d = lerp(OUT_D, lane, a / 0.5)
        return DOOR_C, d, 0, 'carry_run', d > FRONT_D - 0.2
    b = a - 0.5                                             # the sprint: 5.5 m/s (the gait's own speed) to their exit
    ex, ed = EXIT[name]
    L = math.hypot(ex - DOOR_C, ed - lane)
    v = min(1.0, b * moves.speed('sprint') / L)
    yaw = math.degrees(math.atan2(ex - DOOR_C, -(ed - lane)))
    return lerp(DOOR_C, ex, v), lerp(lane, ed, v), yaw * ease(min(1.0, b / 0.2)), 'carry_run', False


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

    def gun_flee(name, xr, take_t, way, reach):
        """G21 (Sam: 'they pace off with the same movements in the same direction'): after the take a 0.25 s step back
        off the glass, turning toward his way out, then a flat-out sprint (gun_run) through the points `way`, the pistol
        held up."""
        t0, to = take_t + 0.45, way[0]
        along = abs(to[1] - 13.45) < 0.5                    # off along the shop front: the step back is a turn sideways
        bx, bd = (xr + 0.25 * math.copysign(1, to[0] - xr), 13.45) if along else (xr, 13.15)
        keys, tk = [(t0 + 0.25, bx, bd)], t0 + 0.25
        for p in way:
            tk += math.hypot(p[0] - keys[-1][1], p[1] - keys[-1][2]) / moves.speed('sprint')
            keys.append((tk, *p))
        if tt < t0 + 0.25:                                  # the step back, turning
            v = ease((tt - t0) / 0.25)
            a = A(name, 'rioter', lerp(xr, bx, v), lerp(13.45, bd, v), lerp(180, _heading(keys, 0), v), 'gun_up', t=tt)
            a.blend(reach, 2.0, w=v * 1.5)
            return
        if tt >= keys[-1][0]:                               # off frame: gone (not jogging on the spot out of view)
            return
        x, d, i, u = _keys(tt, keys)
        A(name, 'rioter', x, d, _heading(keys, min(max(i, 0), len(keys) - 2)), 'gun_run', t=tt)

    # the haulers: sprint in, lever the shutter up (1.0-1.5), run to the door; hauler1 kicks it in (G4)
    for k, (xs, xh) in enumerate(((-3.8, -0.9), (-3.3, 0.9))):
        name = f'hauler{k + 1}'
        if tt >= DOOR_IN[name][0]:
            w = _door_walk(name, tt)
            if w:
                x, d, yaw, st, inside = w
                a = A(name, 'rioter', x, d, yaw, st, t=tt, clip=DOOR_CLIP if inside else None)
                if st.startswith('carry'):
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
    # the swinger (G3, G13): runs in, turns to the glass, and hits it four times in four places (more cracks each
    # time, SIGN_HITS); the fourth goes through. He flings the sign down (SIGN_DROP), celebrates, then loots a pistol.
    keys = [(0.15, -3.8, 11.9), (0.65, -0.4, 12.2), (0.85, *T2_SW)]     # chat 3: on his mark before the runners pass
    x, d, i, u = _keys(tt, keys)
    if 0 <= i < len(keys) - 1:
        A('swinger', 'rioter', x, d, _heading(keys, i), 'run_sign', t=tt)
    elif i >= 0 and tt < SIGN_DROP:
        sx, us, yaw = swinger_swing(tt)
        a = A('swinger', 'rioter', sx, d, yaw, 'swing_face', u=us)
        a.blend('run_sign', 0, tt, w=(tt - 0.95) / 0.25)
    elif i >= 0:
        xs = SIGN_HITS[-1][1]
        xr, take_t = -0.2, TAKE['swinger'][2]
        if tt < SIGN_DROP + 0.25:                           # the fling: arms thrown down and out, the sign gone
            a = A('swinger', 'rioter', xs, d, 125, 'cheer', u=1.0)
            a.blend('swing_face', 1.0, w=1 - (tt - SIGN_DROP) / 0.25)
        elif tt < take_t - 0.65:                            # celebrating: turned half to us, fists pumped up
            yaw = lerp(125, 30, ease((tt - SIGN_DROP - 0.25) / 0.4))
            A('swinger', 'rioter', xs, d, yaw, 'cheer', u=0.5 + 0.5 * math.sin((tt - SIGN_DROP) * 2 * math.pi * 1.6))
        elif tt < take_t - 0.35:                            # to the window
            v = ease((tt - take_t + 0.65) / 0.3)
            a = A('swinger', 'rioter', lerp(xs, xr, v), lerp(d, 13.45, v), 180, 'stand')
            a.blend('cheer', 0.5, w=1 - v)
        elif tt < take_t + 0.45:
            A('swinger', 'rioter', xr, 13.45, 180, 'reach_lo',
              u=(tt - take_t + 0.35) / 0.35 if tt < take_t else 1 + (tt - take_t) / 0.45)
        else:                                               # G21: a step back and turn, then a sprint off left along the shop front
            gun_flee('swinger', xr, take_t, GUN_RUN['swinger'], 'reach_lo')
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
        gun_flee(name, xr, take_t, GUN_RUN[name], reach)   # G21: each sprints off his own way
    # runner3 (G7): the A-board: a sprint in, three steps' run-up, a hard kick; then he throws stones into the shop
    keys = [(1.35, -3.3, 12.7), (1.85, -1.95, 12.7), (2.12, -1.2, 12.7)]   # G22: 0.3 m right with the board
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
            if st.startswith('carry'):
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
             (2.3, 7.7, 'phone', 6), (2.95, 8.8, 'placard:GEN Z REGELT:240,220,60', 5), (3.2, 9.5, 'stand', 3),
             # G12 (Sam: more foreground protesters, the action kept clear): heads and shoulders cut by the frame's left
             # and right edges, near us (d 4.4-5.6: their heads stay below the pavement line, so the door, the window
             # and everyone in front of the shop are clear)
             (-0.55, 4.5, 'stand', 7), (-0.75, 5.7, 'phone', 8), (1.05, 4.4, 'stand', 9), (1.5, 5.4, 'phone', 10),
             (1.85, 6.4, 'stand', 11)]
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
    z = 1.0 * 4 * u * (1 - u)                               # G18: a 1 m arc (1.5 m hid the third hit)
    if u >= 1:                                              # down: G22 a 0.1 m bounce, then a skid, then flat
        b = (lt - BOARD_LAND) / 0.15
        if b < 1:
            return x, d, 0.1 * 4 * b * (1 - b), 810.0
        s = ease(min(1.0, (lt - BOARD_LAND - 0.15) / 0.25))
        return x + 0.25 * s, d, 0.0, 810.0
    return x, d, z, 810 * ease(u)                           # G22: from standing, two and a quarter turns, face down (was a snap 0 -> 90)


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
    lift = 0.5 * (1 - min(1.0, tilt / 810))                 # G22: the pivot slides from its foot (standing) to its middle
    if tilt >= 90 and lt >= BOARD_LAND:                     # lying face down: its back, the frame, squashed flat
        spr = spr.resize((spr.width, max(6, int(spr.height * .22))))
        spr = Image.eval(spr, lambda v: v)
        dk = Image.new('RGBA', spr.size, (110, 78, 46, 255))
        dk.putalpha(spr.getchannel('A'))
        spr = dk
        tilt, lift = 0.0, 0.5
    r = spr.rotate(-tilt, expand=True, resample=Image.BICUBIC)
    gx, gy = cam.p(x, d, z)
    cy = gy - spr.height * lift
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
    for n, (th, x, z) in enumerate(UP_STONES):              # G15: up at the first-floor window
        t0 = th - 0.6
        if lt < t0 or (n == len(UP_STONES) - 1 and lt >= th):   # the last one goes in through the glass
            continue
        if lt < th:                                         # in the air: up from off right, an arc 0.9 m over the line
            u = (lt - t0) / 0.6
            p = (lerp(UP_FROM[0], x, u), lerp(UP_FROM[1], FRONT_D - 0.05, u), lerp(UP_FROM[2], z, u) + 0.9 * 4 * u * (1 - u))
        elif lt < th + 0.7:                                 # off the glass and down to the pavement
            u = (lt - th) / 0.7
            p = (x + 0.3 * u, FRONT_D - 0.05 - 0.6 * u, max(0.0, z * (1 - u * u)))
        else:
            p = (x + 0.3, FRONT_D - 0.65, 0.0)
        gx, gy = cam.p(*p)
        rr = 0.07 * cam.ppm(p[1])
        IS.poly(img, [(gx + rr * math.cos(a) * (1 + .25 * math.sin(3 * a + n)), gy + rr * .8 * math.sin(a))
                      for a in np.linspace(0, 6.28, 9)[:-1]], (150, 146, 138), INK, 2)
        if th <= lt < th + 0.08:
            S.glow_disc(img, *cam.p(x, FRONT_D, z), 30, (255, 255, 240), amt=.6)


def t2_chips(img, lt):
    """G2: each stone's small star of cracks on the glass, until the sign takes the glass out. G20 (Sam: 'some of the
    fractures spread beyond the frame'): drawn on their own layer and kept inside the pane T2_WR."""
    if lt >= T2_SHATTER + 0.1:
        return
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    _t2_chips_draw(lay, lt)
    x0, y0, x1, y1 = T2_WR
    box = (max(0, int(min(x0, x1))), max(0, int(min(y0, y1))),
           min(img.size[0], int(max(x0, x1))), min(img.size[1], int(max(y0, y1))))
    if box[2] > box[0] and box[3] > box[1]:
        img.alpha_composite(lay.crop(box), dest=box[:2])


def _t2_chips_draw(img, lt):
    cam = RF2.cam
    # G13: each sign hit leaves a bigger star, the later ones' cracks running across the pane toward the earlier ones
    for k, (th, _x, _u, _y, (sx, sz)) in enumerate(SIGN_HITS[:-1]):
        if lt < th:
            continue
        cx, cy = cam.p(sx, FRONT_D, sz)
        rng = np.random.default_rng(40 + k)
        for q in range(9 + 4 * k):
            a = q * 2 * math.pi / (9 + 4 * k) + rng.uniform(-.2, .2)
            r = rng.uniform(60, 150) * (1 + 0.5 * k)
            mid = (cx + r * .5 * math.cos(a + .15), cy + r * .5 * math.sin(a + .15))
            IS.poly(img, [(cx, cy), mid, (cx + r * math.cos(a), cy + r * math.sin(a))], None, (70, 88, 100), 2.2, 0)
        for rr in (22, 48 + 10 * k):                        # the rings of the star
            IS.poly(img, [(cx + rr * math.cos(a) * rng.uniform(.8, 1.2), cy + rr * math.sin(a) * rng.uniform(.8, 1.2))
                          for a in np.linspace(0, 6.28, 10)], None, (70, 88, 100), 1.8, 0)
        IS.poly(img, [(cx + 14 * math.cos(a), cy + 14 * math.sin(a)) for a in np.linspace(0, 6.28, 9)], (236, 244, 248),
                (70, 88, 100), 1.4, 0)
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
    t2_sign(img, lt)


def t2_sign(img, lt):
    """G13: the road sign flung down at SIGN_DROP: out of his hands, a turn in the air, then lying on the pavement."""
    if lt < SIGN_DROP:
        return
    cam = RF2.cam
    x0, d0 = SIGN_HITS[-1][1] + 0.4, T2_SW[1] - 0.3         # from his hands, down to his right, by his feet
    x1, d1 = x0 + 0.5, d0 - 0.35
    u = min(1.0, (lt - SIGN_DROP) / 0.35)
    x, d = lerp(x0, x1, u), lerp(d0, d1, u)
    z = lerp(1.2, 0.03, u) + 0.4 * 4 * u * (1 - u)
    L = 1.1
    if u < 1:                                               # turning in the street's plane, pole end leading
        ang = math.radians(100 - 150 * ease(u))
        base = (x - 0.5 * L * math.cos(ang), d, z - 0.5 * L * math.sin(ang) * 0.5)
        top = (x + 0.5 * L * math.cos(ang), d, z + 0.5 * L * math.sin(ang) * 0.5)
    else:                                                   # flat on the pavement, the sign end to the right
        base, top = (x - 0.5 * L, d + 0.1, 0.03), (x + 0.5 * L, d - 0.1, 0.03)
    a, b = cam.p(*base), cam.p(*top)
    k = cam.ppm(d)
    IS.poly(img, [a, b], None, INK, max(4, .07 * k), 0)
    IS.poly(img, [a, b], None, (150, 152, 156), max(2, .045 * k), 0)
    side, sq = 0.7 * k, (0.3 if u >= 1 else 1.0)            # the triangle, squashed flat once it lies on the ground
    dx, dy = (b[0] - a[0]), (b[1] - a[1])
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    tri = [b, (b[0] + ux * side * .87 - uy * side * .5 * sq, b[1] + uy * side * .87 * sq + ux * side * .5 * sq),
           (b[0] + ux * side * .87 + uy * side * .5 * sq, b[1] + uy * side * .87 * sq - ux * side * .5 * sq)]
    IS.poly(img, tri, (200, 28, 36), INK, 2.4)
    cx, cy = sum(q[0] for q in tri) / 3, sum(q[1] for q in tri) / 3
    IS.poly(img, [(cx + (q[0] - cx) * .55, cy + (q[1] - cy) * .55) for q in tri], (246, 246, 242), None, 0)


def t2_flash(img, tt):
    """The impact flash where the sign meets the glass (each of G13's four hits); its own function so the shape check
    draws it alone."""
    for th, _x, _u, _y, (sx, sz) in SIGN_HITS:
        if th - 0.02 <= tt < th + 0.15:
            S.glow_disc(img, *RF2.cam.p(sx, FRONT_D, sz), 70, (255, 250, 210), amt=.5)     # chat 3: small, so the contact reads     # chat 3: small, so the contact reads


def t2_upstairs(img, lt):
    """G15: the lit first-floor window: a small star of cracks for each stone that bounces off; the third goes through
    (a jagged hole, the room's light behind it, a ring of cracks) and its glass falls to the pavement and lies still."""
    cam = RF2.cam
    for n, (th, x, z) in enumerate(UP_STONES[:-1]):
        if lt < th:
            continue
        cx, cy = cam.p(x, FRONT_D, z)
        for q in range(8):
            a = q * 0.8 + n * 1.3
            r = 18 + 10 * ((q * 3 + n) % 3)
            IS.poly(img, [(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))], None, (90, 70, 40), 1.8, 0)
        IS.poly(img, [(cx + 7 * math.cos(a), cy + 7 * math.sin(a)) for a in np.linspace(0, 6.28, 8)], (255, 246, 214),
                (90, 70, 40), 1.4, 0)
    th, x, z = UP_STONES[-1]
    if lt < th:
        return
    cx, cy = cam.p(x, FRONT_D, z)
    k = cam.ppm(FRONT_D)
    rng = np.random.default_rng(15)
    hole = [(cx + k * (.13 + .13 * (q % 2)) * rng.uniform(.8, 1.2) * math.cos(a),
             cy + k * (.15 + .15 * (q % 2)) * rng.uniform(.8, 1.2) * math.sin(a))
            for q, a in enumerate(np.linspace(0, 6.28, 17)[:-1])]   # jagged: glass teeth pointing in
    IS.poly(img, hole, (255, 236, 186), INK, 2.4)                # the lit room behind, brighter than the blind
    IS.poly(img, [(cx + (p[0] - cx) * .5, cy + (p[1] - cy) * .5 + 4) for p in hole], (250, 214, 140), None, 0)
    for q in range(12):                                       # cracks out from the hole's edge across the pane
        a = q * 2 * math.pi / 12 + rng.uniform(-.2, .2)
        r0, r1 = k * .26, k * rng.uniform(.5, .8)
        IS.poly(img, [(cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
                      (cx + r1 * math.cos(a + .1), cy + r1 * math.sin(a + .1))], None, (90, 70, 40), 1.8, 0)
    for q in range(9):                                        # the glass falling (1 s from 6 m), then lying still
        sx, sz = x + rng.uniform(-.4, .4), z + rng.uniform(-.4, .4)
        tl = math.sqrt(2 * sz / 9.8)
        u = min(1.0, (lt - th - 0.05 * q) / tl) if lt >= th + 0.05 * q else 0.0
        px, pd, pz = sx + 0.25 * u * rng.uniform(-1, 1), FRONT_D - 0.1 - 0.5 * u, sz * (1 - u * u)
        gx, gy = cam.p(px, pd, pz)
        r = 0.06 * cam.ppm(pd)
        spin = (lt - th) * 9 * (q % 3 - 1) if u < 1 else q
        tri = [(gx + r * math.cos(spin + j * 2.2), gy + r * (0.35 if u >= 1 else 1) * math.sin(spin + j * 2.2))
               for j in range(3)]
        IS.poly(img, tri, (226, 238, 244), (80, 96, 108), 1.4)


def t2_teeth(img, lt):
    """Drawn before the people (in front of the window they hide it)."""
    tt = lt
    t2_chips(img, lt)
    t2_upstairs(img, lt)
    if tt >= T2_SHATTER + 0.1:                             # chat 16 (hunt 2: glass looked whole): jagged teeth left
        x0, y0, x1, y1 = T2_WR                             # in the frame, a star of cracks round the hole
        rng = np.random.default_rng(9)
        # G3: the swinger knocks the teeth out as he goes on (1.75-3.85): fewer are left after each swing
        left = 1.0                                         # G13: he flings the sign down after the shatter
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
        a = tt - (T2_SHATTER + 0.05) - rng.uniform(0, .15)
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
    # round 4 (F23): rolls in slower and earlier, 2.0-3.4, so it is coming while the stones fly
    return lerp(9.0, 1.2, ease((lt - TRUCK_IN) / 1.4)) - 1.5 * ease((lt - 5.5) / 1.0)


TRUCK_IN = 2.0
JET_ON = 2.55 + J3                  # 3.5: the jet opens up
SWEEP = (3.55, 7.0, 16.6, 9.4)     # round 4 (F23): the jet's aim walks down the rioters' line, far (d 16.6) to near


def jet_aim(lt):
    """Round 4 (F23, F22): where the jet strikes (x, d m) at shot time lt: down the throwers' line from the far end
    to the near, then after the last of them, left."""
    t0, t1, d0, d1 = SWEEP
    u = max(0.0, min(1.0, (lt - t0) / (t1 - t0)))
    d = lerp(d0, d1, u)
    x = -2.3 + 0.25 * math.sin(lt * 5.0) - 1.6 * ease((lt - t1) / 0.8)
    return x, d


def jet_reaches(d):
    """When the jet's aim passes depth d."""
    t0, t1, d0, d1 = SWEEP
    return t0 + (d0 - d) / (d0 - d1) * (t1 - t0)


def nozzle(lt, aim=12.0):
    cam = T3CAM
    k = cam.ppm(T3_TRUCK_D)
    gx, gy = cam.p(truck_x(lt), T3_TRUCK_D)
    bx, by = gx + 1.4 * k, gy - 3.3 * k
    a = math.radians(aim)
    return bx - 1.45 * k * math.cos(a), by - 1.45 * k * math.sin(a)


def car2_fx_depth():
    """Round 4 (F17): the second car's nearest depth (drawn among the crowd in depth order)."""
    X0, X1, D0, D1 = S.CAR3B
    return min(S.car_pt(a, b, CAR2_MOVE, S.CAR3B)[1] for a in (X0, X1) for b in (D0, D1))


CAR2_MOVE = (0.0, 0.0, 35.0)        # round 4 (F17): its own angle: rear and right side to us, nose away right


def draw_car3b(img, lt):
    S._car(img, T3CAM, lt + 0.37, CAR2_MOVE, fire=1.0, box=S.CAR3B, col=S.CAR3B_COL)


VOLLEY2 = 2.5                       # round 1: the second volley (the back row) starts throwing
CAR_T0, CAR_LET, CAR_STOP = 6.0, 6.9, 7.6   # the shove starts, they let go, it stops in the jet
CAR_HIT = 7.2                        # the jet hits the car: a burst of steam, the fire knocked down


NEAR3 = 7.4                          # the nearest people are drawn over the jet (the old car's rear + 1 m)
CAR_YAW = 80.0                       # round 3 (F10): the car stands where it was set alight (S.CAR3), turned this far


def car_move(lt):
    """Round 3 (F10, Sam Y 16 Nov: 'a burning car in the upper left, near the statue, behind the protesters', as fr3):
    no shove now; the car stands still (S.car_pt with no move but its own turn)."""
    return 0.0, 0.0, CAR_YAW


def car_fire(lt):
    return 1.0                                              # F10: it burns the whole shot (the jet never reaches it)


def car_roof(lt):
    X0, X1, D0, _ = S.CAR3
    return S.car_pt(X1 - 0.5, D0 + 2.4, car_move(lt))


def car_fx(img, lt):
    """T3 7.2-8.0: the jet hits the burning car: a burst of white steam boiling up off it, drifting left."""
    return                                                  # F10: the jet never reaches the car now: no steam
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


OFF_L = -4.8                       # round 3 (F7): the front line further left; past this they are gone (was -4.2)
PUSH_IN = 1.5                       # the pushers' run in from the left


def _jit(name, lo, hi):
    """Round 3 (F9, Sam: 'no group moves uniformly'): one person's own fixed value in lo..hi (timing, stride, angle)."""
    import zlib
    return lo + (hi - lo) * (zlib.crc32(name.encode()) % 10007) / 10006.0


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


# round 3 (F7, Sam: 'too little distance between protesters and police'): the gap opened from 2.4 m to 4.6 m
FRONT3 = ((-2.0, 10.0), (-1.85, 12.0), (-2.05, 14.0), (-1.9, 16.0))   # the front line runs away from us (a wall
BACK3 = ((-2.65, 11.0), (-2.6, 13.0), (-2.7, 15.0))     # facing right); the back row steps up in its gaps
# Round 4 (F16, rule 30: F9 only spread the rates 1.47-1.71 a second and the phases; every throw was the same overarm
# curve from the same stance, so they still read as one): each thrower his own way of throwing, his own speed of arm
# (0.5-0.9 s a throw), and between throws he bends for the next stone, for his own time each time (0.25-1.3 s)
STYLE = {'front1': 'throw', 'front2': 'throw_side', 'front3': 'throw_lob', 'front4': 'throw',
         'back1': 'throw_side', 'back2': 'throw_lob', 'back3': 'throw'}
FLIGHT = {'throw': 0.45, 'throw_side': 0.38, 'throw_lob': 0.75}


@lru_cache(None)
def throw_plan(name):
    """[(t0, t1, t2)]: one throw t0-t1 (released at t0 + 0.6 (t1 - t0)), then bending for a stone t1-t2. Starts
    before the shot (F12: they are already throwing at its first frame)."""
    T = _jit(name + 'T', 0.5, 0.9)
    out, t, n = [], -3.0 + _jit(name + 'p', 0.0, 1.5), 0
    while t < 8.5:
        P = _jit(f'{name}P{n}', 0.25, 1.3) * (0.4 if n % 3 == 1 else 1.0)   # now and then straight on to the next
        out.append((t, t + T, t + T + P))
        t, n = t + T + P, n + 1
    return tuple(out)


def throw_state(name, lt):
    """(state, u, w_in): what the thrower is doing at lt, how far through it, and how far into it (for the blend)."""
    for t0, t1, t2 in throw_plan(name):
        if t0 <= lt < t1:
            c = (lt - t0) / (t1 - t0)
            return STYLE[name], _volley(c), (lt - t0) / 0.18
        if t1 <= lt < t2:
            return 'pickup', (lt - t1) / (t2 - t1), (lt - t1) / 0.18
    return STYLE[name], 0.0, 1.0


def _thrower(n, x, d, lt):
    """The thrower's pose at lt, blended in from what he was doing just before (no snaps between throw and pick-up)."""
    st, u, w = throw_state(n, lt)
    lean = _jit(n + 'L', -4, 5)
    a = Actor(n, 'rioter', x, d, 90 + _jit(n + 'a', -12, 12), st, u=u, tier='t3')
    if w < 1.0:
        pst, pu, _ = throw_state(n, lt - 0.19)
        if pst != st:
            a.blend(pst, u=pu, w=w)
    a.extra = (lambda j, lean=lean: j.__setitem__('lean', j.get('lean', 0) + lean))
    return a, st, u
CRS_YAW = -60   # round 2 (F2): turned three-quarters to the camera so the raised shields show their face, not an edge
# round 3 (F8): the block split in two, a lane between (d 11.4-15.0) that the water cannon drives up
CRS_X, CRS_D = (2.6, 3.35, 4.1), (9.3, 10.2, 11.1, 15.3, 16.2, 17.1)
SHIELD_X = CRS_X[0] - 0.42                             # the front rank's shield face (x m), before the advance
ADV_T, ADV_STEP, ADV_N = 3.7, 0.5, 3                    # F2: when the cannon opens up, 3 steps of 0.4 m in lockstep (F23: 3.7)
JET_T = 2.6 + J3                                       # the jet reaches the front line
# round 3 (F11): what each throw is (row, thrower, throw number); the rest are stones
MISSILES = {('f', 1, 2): 'firework', ('b', 0, 1): 'firework',
            ('f', 0, 3): 'bottle', ('f', 2, 1): 'bottle', ('f', 3, 5): 'bottle', ('b', 2, 3): 'bottle',
            ('f', 0, 1): 'fruit', ('f', 1, 4): 'fruit', ('f', 2, 5): 'fruit', ('f', 3, 2): 'fruit',
            ('b', 0, 2): 'fruit', ('b', 1, 3): 'fruit', ('b', 1, 0): 'cone', ('b', 2, 1): 'wheel'}


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
    """Shields up (0..1). Round 4 (F18, rule 30: F2/F9 lowered them once the cannon came, 4.5 on, while stones still
    landed): up from the first frame (they are already under fire) until the last missile has landed."""
    return 1.0 - ease((lt - last_land() - 0.4) / 0.4)


@lru_cache(None)
def last_land():
    return max(t0 + fl for *_, t0, fl in _throws())


@lru_cache(None)
def hits():
    """Round 4 (F18): every missile's hit on the police: (depth row d, file 0 front / 2 rear (lobs), time)."""
    return tuple((d1, 2 if STYLE[('front' if row == 'f' else 'back') + str(k + 1)] == 'throw_lob' else 0, t0 + fl)
                 for row, k, rep, what, x0, d0, d1, t0, fl in _throws())


def jolt(d, c, lt):
    """How hard officer (row d, file c) is rocked by a hit at lt (0..1): the one hit most, the file beside him less."""
    out = 0.0
    for d1, c1, th in hits():
        u = (lt - th) / 0.35
        if 0 < u < 1 and abs(d1 - d) < 0.2:
            out = max(out, math.sin(math.pi * u) * (1.0 if c == c1 else 0.35 if abs(c - c1) == 1 else 0.0))
    return out


def _break(name, k):
    """F9: when this rioter breaks from the jet, how fast he runs and where he heads (his own, not the row's)."""
    # (the heading stays -115: other run headings blended from a throw fold the elbow back, the rig's guard stops them)
    # round 4 (F23): each breaks when the jet reaches him (it walks down the line 3.55-7.0), not all at 4.6
    d = dict(zip([f'front{i + 1}' for i in range(4)] + [f'back{i + 1}' for i in range(3)],
                 [p[1] for p in FRONT3 + BACK3]))[name]
    return jet_reaches(d) + 0.12 + _jit(name + 'b', 0.0, 0.15), 4.5 * _jit(name + 'v', 0.82, 1.16), -115


# round 3 (F4, Sam: 'protesters clambering up and celebrating on the statue', fr3): on Marianne's base (the painting's
# front face at d MON_D: the top step at z 1.5, the ledge round the drum at z 5.0). (name, x off her centre, z, start)
MON_CHEER = (('mon1', -5.6, 5.0, 0.0), ('mon2', 3.9, 5.0, 0.0), ('mon3', -1.8, 5.0, 0.0), ('mon4', 6.4, 1.5, 0.0),
             ('mon5', -8.2, 1.5, 0.0))
MON_CLIMB = (('climb1', -3.6, 0.6, 1.5), ('climb2', 5.4, 2.4, 1.4))     # (name, x, starts hauling, takes s)


def mon_actors(lt):
    out = []
    d = S.MON_D - 0.8
    for k, (n, x, z, _) in enumerate(MON_CHEER):
        rate = _jit(n + 'r', 4.5, 7.5)
        if k == 2:                                          # one waves the tricolour from the ledge
            out.append(Actor(n, 'marcher', S.MON_X + x, d, -10 + 20 * math.sin(lt * 2.1), 'flag:tricolour',
                             i=k + 3, tier='t3', lift=z))
        else:
            out.append(Actor(n, 'marcher', S.MON_X + x, d, _jit(n + 'y', -25, 25), 'cheer',
                             u=abs(math.sin(lt * rate + k)), i=k + 5, tier='t3', lift=z))
    for k, (n, x, t0, dur) in enumerate(MON_CLIMB):     # hauling himself up the plinth face (back to us), then on
        u = (lt - t0) / dur                                 # the ledge, turning round to punch the air
        if u < 0:
            out.append(Actor(n, 'marcher', S.MON_X + x, d + 0.2, 180, 'reach_hi', u=0.9 * ease(min(1.0, lt / 0.4)),
                             i=k + 11, tier='t3', lift=1.5))
        elif u < 1:
            z = 1.5 + 3.5 * ease(u)
            out.append(Actor(n, 'marcher', S.MON_X + x, d + 0.2, 180, 'reach_hi', u=0.9 + 0.1 * math.sin(u * 9),
                             i=k + 11, tier='t3', lift=z, ))
        else:
            w = (lt - t0 - dur) / 0.35
            out.append(Actor(n, 'marcher', S.MON_X + x, d + 0.2, _turn(180, 10, w), 'cheer',
                             u=abs(math.sin(lt * 6 + k)), i=k + 11, tier='t3', lift=5.0)
                       .blend('reach_hi', 1.0, w=w))
    return out


def t3_actors(lt):
    out = mon_actors(lt)
    # round 4 (F12, Sam: 'start with the crowds already throwing'): no walk-in; both rows in place at the first frame,
    # each thrower mid-way through his own throw (throw_plan); F23: each breaks as the jet reaches him
    for k, (x, d) in enumerate(FRONT3 + BACK3):
        n = f'front{k + 1}' if k < 4 else f'back{k - 3}'
        dx, _ = field('t3', x, d, lt, k)
        x = x + dx * .3
        tb, v, yb = _break(n, k)
        if lt > tb:                                         # struck by the jet: knocked a step, turns, runs out left
            u = lt - tb
            st, su, _ = throw_state(n, tb)
            x1 = x - 0.35 * ease(u / 0.25) - _getaway(max(0.0, u - 0.2), v)
            d1 = d + (0.3 if k >= 4 else -0.2) * ease(u / .6)
            if T3CAM.p(x1, d1)[0] < -140:                   # out of the frame's left edge (no vanishing in it)
                continue
            out.append(Actor(n, 'rioter', x1, d1, _turn(90, yb, (u - 0.1) / .35), 'run',
                             t=lt * _jit(n + 's', .92, 1.08) + .3 * (k >= 4), tier='t3')
                       .blend(st, su, w=(u - 0.05) / .35))
        else:
            a, st, u = _thrower(n, x, d, lt)
            out.append(a)
    # F10 (Sam Y, 16 Nov): no pushers; the car burns where it stands (draw_car3)
    # round 2 (F2): the police: shields up against the missiles, then forward together when the cannon opens up.
    # Round 3: two groups, a lane between (F8); each officer a beat off the others, his own stride and stance (F9).
    # Round 4 (F18): all three files guard (the rear one with shields over their heads against the lobs), each
    # rocked back when a missile hits his shield, shuffling and turning a little between hits; shields up as they step
    for c, x in enumerate(CRS_X):
        for r, d in enumerate(CRS_D):
            k = c * len(CRS_D) + r
            n = f'crs{k + 1}'
            o = 0.05 * c + _jit(n + 'o', -0.05, 0.05)       # check (round 3): rear files set off a beat after the
            adv, stepping = crs_adv(lt - o)                 # ones in front, so their feet never step into them
            g = crs_guard(lt - 1.5 * o) * _jit(n + 'g', .85, 1.0)
            jo = jolt(d, c, lt)
            sh = 0.05 * math.sin(lt * _jit(n + 'f', 1.3, 2.4) + _jit(n + 'q', 0, 6.3))   # small shuffles
            yaw = CRS_YAW + _jit(n + 'y', -7, 7) + 6 * math.sin(lt * _jit(n + 'w', 0.7, 1.4) + k) - 14 * jo
            lean = _jit(n + 'l', -3.5, 3.5)
            x1, d1 = x - adv + _jit(n + 'x', -0.06, 0.06) + 0.06 * jo, d + _jit(n + 'd', -0.12, 0.12) + sh
            if stepping:
                a = Actor(n, 'officer', x1, d1, yaw, 'shield_walk' if c < 2 and g > .5 else 'line_walk',
                          t=(lt - ADV_T - o) * _jit(n + 's', .9, 1.1), force='crs', tier='t3')
            elif c == 2 and g > 0:
                a = Actor(n, 'officer', x1, d1, yaw, 'shield_over', u=g, t=jo, force='crs', tier='t3')
            elif g > 0:
                a = Actor(n, 'officer', x1, d1, yaw, 'shield_up', u=g, t=jo, force='crs', tier='t3')
            else:
                a = Actor(n, 'officer', x1, d1, yaw, 'line', force='crs', tier='t3')
            a.extra = (lambda j, lean=lean: j.__setitem__('lean', j.get('lean', 0) + lean))
            a.i = (k * 5) % 7
            out.append(a)
    return out


def _on_base(x, d, pad=0.4):
    """Round 3 (F4): is ground point (x, d) inside Marianne's round stepped base (radius 11 m)?"""
    dx = x - S.MON_X
    return abs(dx) < 11.0 and d > S.MON_D - math.sqrt(max(0.0, 11.0 ** 2 - dx * dx)) - pad


@lru_cache(None)
def crowd_t3():
    rng = np.random.default_rng(31)
    out = []
    for d in np.arange(9.0, 44.0, 0.9):                     # round 2 (F1): from 9 m, left of the front line
        # round 3 (F7: the gap opened; F4: the crowd fills the square up to Marianne's base and round its front)
        xmax = (-3.3 if d < 16.5 else -2.6) + (d - 13) * .03 + max(0.0, d - 20) * 0.45
        for x in np.arange(-12.0, xmax, 0.7):
            r = rng.uniform()
            state = 'flag:tricolour' if r < .12 else 'stand'
            if d > 22 and r > .86:
                state = 'placard:CGT:200,30,40'
            m = dict(x=x + rng.uniform(-.25, .25), d=d + rng.uniform(-.3, .3), i=int(rng.integers(0, 32)),
                     state=state, ph=rng.uniform(0, 6.28), v=rng.uniform(.75, 1.25), dl=rng.uniform(0, .3),
                     su=rng.uniform(.65, 1.2))
            if state != 'stand' and car_clear(m['x'], m['d'], pad=3.0, front=17.0):
                state = 'stand'                             # F10: no flag over the car from the people beside it
                m['state'] = state
            if not _on_base(m['x'], m['d']) and not car_clear(m['x'], m['d']):
                out.append(m)
    # chat 7 (full-size look): one marcher stood alone in the gap before the base (her neighbours fell in the car's
    # clearing); anyone with no one within 1.3 m is dropped
    out = [m for m in out if any(o is not m and abs(o['x'] - m['x']) < 1.3 and abs(o['d'] - m['d']) < 1.3
                                 for o in out)]
    # F4: more of them up on the base, sprites standing along the top step and the ledge (the painting's front face)
    for n, (x, z) in enumerate(((-9.6, 1.5), (-7.2, 1.5), (-4.6, 1.5), (-2.4, 1.5), (1.4, 1.5), (3.6, 1.5),
                                (8.4, 1.5), (-6.6, 5.0), (-3.2, 5.0), (1.9, 5.0), (5.9, 5.0))):
        out.append(dict(x=S.MON_X + x, d=S.MON_D - 0.9, z=z, i=(n * 7) % 16, state='flag:tricolour' if n % 3 == 0
                        else 'stand', ph=n * 1.3, v=1.0, dl=0.0, su=1.0, on=True))
    # round 4 (F13, Sam: 'more police and more crowds around the statue; no empty space in this mass riot'): a CRS
    # reserve round the second car and behind the block, a cordon along the base's right side, and the crowd packed
    # round the base's right beyond the cordon
    def put(x, d, **kw):
        m = dict(x=x + rng.uniform(-.2, .2), d=d + rng.uniform(-.25, .25), ph=rng.uniform(0, 6.28), v=1.0, dl=0.0,
                 su=1.0, **kw)
        if not car_clear(m['x'], m['d'], box=S.CAR3B, move=CAR2_MOVE, pad=1.0, front=2.5) and \
                not _on_base(m['x'], m['d'], pad=0.6):
            out.append(m)
    for d in np.arange(18.6, 27.0, 0.95):                   # the reserve: the block's depth carried back, then right
        for x in np.arange(2.6, 12.5, 0.78):
            if d < 21.0 and x > 5.0 or rng.uniform() < .12:
                continue
            put(x, d, kind='officer', i=int(rng.integers(10, 40)), yaw=int(rng.choice((-60, -60, -75, -45))),
                state='shield_up:1' if rng.uniform() < .45 else 'line')
    for x in np.arange(3.0, 15.5, 0.72):                    # the cordon along the base's right side
        put(x, 28.2 + 0.08 * (x - 3), kind='officer', i=int(rng.integers(10, 40)), yaw=-30, state='line')
    for d in np.arange(29.5, 46.0, 0.85):                   # the crowd round the base's right side
        for x in np.arange(8.5 + max(0.0, 40 - d) * 0.05, 20.0, 0.72):
            r = rng.uniform()
            put(x, d, i=int(rng.integers(0, 32)), state='flag:tricolour' if r < .14 else
                'placard:CGT:200,30,40' if r > .9 else 'stand', yaw=-90 if r < .5 else -120)
    return out


def car_clear(x, d, pad=1.4, front=7.0, box=None, move=None):
    """F10: the burning car's own ground (its corners as stood, padded) and a clearing in front of it, widening toward
    us (people keep off a fire; and from this height the heads in front hid it): the crowd keeps off both."""
    X0, X1, D0, D1 = box or S.CAR3
    pts = [S.car_pt(a, b, move or car_move(0), box) for a in (X0, X1) for b in (D0, D1)]
    xa, xb = min(p[0] for p in pts) - pad, max(p[0] for p in pts) + pad
    da, db = min(p[1] for p in pts), max(p[1] for p in pts) + pad
    if da - front <= d < da:
        w = 1.6 * (da - d) / front                          # the clearing fans out a little toward the camera
        return xa - w <= x <= xb + w
    return xa <= x <= xb and da - pad <= d <= db


def car_depth():
    """F10: the depth the car is drawn at among the crowd: its nearest point (people nearer are drawn over it)."""
    X0, X1, D0, D1 = S.CAR3
    return min(S.car_pt(a, b, car_move(0))[1] for a in (X0, X1) for b in (D0, D1))


def t3_crowd(img, lt, d_hi=1e9, d_lo=-1e9):
    """The crowd sprites with d_lo < d <= d_hi (the picture draws them in bands round the two cars, F10/F17).
    Round 4 (F22, Sam: 'some of the crowd slide backwards at the touch of the water cannon: keep them protesting in
    place'): they stay and keep protesting; F14: those near where the gas lands turn away from it."""
    cam = T3CAM
    gx0, gd0 = GAS_LAND
    for m in sorted(crowd_t3(), key=lambda m: -m['d']):
        if not d_lo < m['d'] <= d_hi:
            continue
        if m.get('on'):                                     # up on the monument: they stay, swaying
            gx, gy = cam.p(m['x'] + 0.08 * math.sin(lt * 2 + m['ph']), m['d'], m['z'])
            paste(img, 'marcher', m['i'], 't3', m['state'], 90 if m['x'] < S.MON_X else -90, gx, gy,
                  scale_at(cam, m['d']))
            continue
        dx, dd = field('t3', m['x'], m['d'], lt, m['ph'])
        x, d = m['x'] + dx, max(8.8, m['d'] + dd)
        gx, gy = cam.p(x, d)
        if gx < -80 or gx > W + 80:
            continue
        if m.get('kind') == 'officer':
            st = m['state']
            if st.startswith('shield_up'):
                st = 'shield_up:1'
            paste(img, 'officer', m['i'], 't3', st, m['yaw'], gx, gy, scale_at(cam, d), force='crs')
            continue
        yaw = m.get('yaw', 90)
        state = m['state']
        if lt > GAS_T + 0.2 and math.hypot(m['x'] - gx0, m['d'] - gd0) < 3.2:   # F14: gassed: turned away, stand
            yaw, state = (-90 if (int(m['ph'] * 10) % 2) else 180), 'stand'
        paste(img, 'marcher', m['i'], 't3', state, yaw, gx, gy, scale_at(cam, d))


def t3_columns(img, lt):
    """Smoke climbing from the two cars, drawn before the truck and the people. Round 4 (F21, Sam: 'the smoke hangs
    limply when it could be drifting over the crowd'): the wind takes it right to left over the crowd, each puff
    rolling and thinning as it goes, new every frame."""
    for (sx, sy), n0, k in ((T3CAM.p(*car_roof(lt), 2.0), 0, 1.0),
                            (T3CAM.p(*S.car_pt(8.0, 23.6, CAR2_MOVE, S.CAR3B), 2.0), 3, 0.8)):
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        lumps = []
        for n in range(18):                                     # chat 7: 18 puffs (was 9), so the column is unbroken:
            a = (lt * 0.32 + n / 18 + n0 * .07) % 1.0               # 9 left lone round puffs that read as rocks

            lumps.append((sx - 700 * a * k + 26 * math.sin(lt * 1.7 + n * 2.1),
                          sy - 70 - (260 * min(1.0, a * 2.5) + 120 * a) * k + 14 * math.cos(lt * 1.3 + n),
                          (26 + 120 * a) * k, a))
        for lo, hi, f in ((0.85, 1.01, .3), (0.65, 0.85, .62), (0.0, 0.07, .45), (0.07, 0.65, 1.0)):   # thinning: oldest
            band = [q[:3] for q in lumps if lo <= q[3] < hi]                       # puffs first, faintest
            if band:
                one = Image.new('RGBA', img.size, (0, 0, 0, 0))
                S.smoke(one, band, (58, 54, 56), (138, 128, 124), lw=2.5)
                if f < 1:
                    one.putalpha(one.getchannel('A').point(lambda v, f=f: int(v * f)))
                lay.alpha_composite(one)
        img.alpha_composite(lay)


def t3_debris(img):
    """Chat 16 (hunt 2: bare grey ground filled the lower third): the square's near ground littered, as in the
    references: thrown cobbles, leaflets, a dropped tricolour and a yellow vest. Round 3 (F6): cobbles smaller, matt."""
    cam = T3CAM
    rng = np.random.default_rng(23)
    for _ in range(22):                                    # cobbles
        x, d = rng.uniform(-2.6, 3.6), rng.uniform(6.6, 9.4)     # round 2: the near ground in the raised frame
        sx, sy = cam.p(x, d)
        k = cam.ppm(d)
        IS.ell(img, sx, sy - .025 * k, .05 * k, .034 * k, STONE3, INK, 1.3)   # F20: 5 cm cobbles
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


STONE3 = (112, 104, 94)                 # round 3 (F6): a matt grey-brown cobble, no shine
FRUIT3 = ((206, 48, 38), (238, 134, 32), (126, 166, 58))      # tomato, orange, apple
BOTTLE3 = ((58, 104, 62), (112, 70, 34))                       # green, brown glass


def _rot(cx, cy, pts, a):
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def _missile(img, cam, what, x0, d0, d1, t0, lt, flight=0.45, spin=0, seed=0, lob=False):
    """Round 2 (F2): one thrown thing from (x0, d0) at the police's shields (d1): up in an arc, hits the raised
    shield face (a flash). Stones, cones and wheels bounce back off it and lie in front of the line. Round 3 (F11):
    fruit splats on the shield and drops; a bottle smashes there (shards fly and lie); a firework trails sparks and
    bursts on it."""
    a = (lt - t0) / flight
    if a < 0:
        return
    hx = SHIELD_X - crs_adv(t0 + flight)[0]                    # the shield face where it gets there
    hz = 1.6
    if lob:                                                    # round 4 (F16/F18): a lob drops on the rear file's
        hx, hz = CRS_X[2] - crs_adv(t0 + flight)[0], 2.45     # shields held over their heads
    k = cam.ppm(d1)
    top = 3.6 if lob else 2.4
    path = lambda q: (lerp(x0 + 0.3, hx, q), 1.9 + top * math.sin(math.pi * q) + (hz - 1.9) * q, lerp(d0, d1, q))  # noqa
    hsx, hsy = cam.p(hx, d1, hz)
    if a < 1:                                                  # in the air
        x, z, d = path(a)
    elif what in ('fruit', 'bottle', 'firework'):              # F11: they do not bounce
        b = min(1.0, (a - 1) / 0.6)
        x, z, d = hx - 0.15 * b, max(0.0, hz - hz * b * b), d1
    else:                                                      # off the shield: back 0.7 m, down to the ground
        b = min(1.0, (a - 1) / 0.8)
        x, z, d = hx - 0.7 * b, max(0.0, hz + 0.5 * math.sin(math.pi * b * .6) - (hz + .15) * b * b), d1
    if 1 <= a < 1.25 and what != 'firework':                    # the hit: a white flash on the shield
        S.glow_disc(img, hsx, hsy, k * (0.45 * (1.25 - a) / 0.25 + .15), (255, 246, 200), amt=.7)
    sx, sy = cam.p(x, d, z)
    k = cam.ppm(d)
    rot = spin * min(a, 1.0) + spin * .3 * max(0.0, min(a, 1.8) - 1)
    rng = np.random.default_rng(seed)
    if what == 'cone':
        S.prop_cone(img, sx, sy, 1.4 * k, rot)
    elif what == 'wheel':
        S.prop_wheel(img, sx, sy, .8 * k, rot)        # chat 7: .8 (was 1.25: read bigger than the officers' heads x3)
    elif what == 'fruit':
        col = FRUIT3[seed % 3]
        if a < 1:
            IS.ell(img, sx, sy, .1 * k, .09 * k, col, INK, 2.2)
            IS.poly(img, [(sx, sy - .09 * k), (sx + .03 * k, sy - .15 * k)], None, (70, 100, 40), 3, 0)
        else:                                                  # splat: juice on the shield, the squashed fruit drops
            if a < 2.2:
                f = 1 - (a - 1) / 1.2
                for q in range(6):
                    ang = q * 1.05 + seed
                    IS.ell(img, hsx + math.cos(ang) * .14 * k, hsy + math.sin(ang) * .1 * k + (a - 1) * .2 * k,
                           .05 * k * f + 1, .04 * k * f + 1, col, None)
            IS.ell(img, sx, sy - .03 * k, .13 * k, .05 * k, col, INK, 2)
    elif what == 'bottle':
        col = BOTTLE3[seed % 2]
        if a < 1:
            ang = math.radians(rot + 720 * a)
            body = [(-.06, -.14), (.06, -.14), (.06, .08), (.025, .12), (.025, .2), (-.025, .2), (-.025, .12),
                    (-.06, .08)]
            IS.poly(img, _rot(sx, sy, [(u * k, v * k) for u, v in body], ang), col, INK, 2)
        else:                                                  # smashed: shards burst off the shield and fall still
            b = min(1.0, (a - 1) / 0.7)
            for q in range(8):
                ox, oz = rng.uniform(-.6, -.05), rng.uniform(-.2, .5)
                qd = d1 + rng.uniform(-.4, .4)
                px, pz = hx + ox * b, max(0.0, hz + oz * b * 2 - (hz + 1.0) * b * b)
                qx, qy = cam.p(px, qd, pz)
                r = rng.uniform(.03, .06) * cam.ppm(qd)
                IS.poly(img, _rot(qx, qy, [(-r, 0), (r * .3, -r), (r, r * .4)], rng.uniform(0, 6) + 8 * b * (pz > 0)),
                        (200, 226, 214) if q % 2 else col, INK, 1.2)
    elif what == 'firework':
        if a < 1:
            ang = math.atan2(*(np.array(cam.p(*path(min(1, a + .05)))[::-1]) - (sy, sx)))
            for q in range(1, 7):                              # the spark trail behind it
                tx, tz, td = path(max(0.0, a - q * 0.045))
                px, py = cam.p(tx, td, tz)
                IS.ell(img, px + rng.uniform(-4, 4), py + rng.uniform(-4, 4), 7 - q * .7, 7 - q * .7,
                       (255, 214, 90) if q % 2 else (255, 140, 50), None)
            IS.poly(img, _rot(sx, sy, [(-.14 * k, -.035 * k), (.1 * k, -.035 * k), (.16 * k, 0), (.1 * k, .035 * k),
                                       (-.14 * k, .035 * k)], ang), (200, 36, 40), INK, 1.8)
        elif a < 1.9:                                          # the burst on the shield: sparks flying out, fading
            b = (a - 1) / 0.9
            S.glow_disc(img, hsx, hsy, k * (.7 * (1 - b) + .2), (255, 236, 170), amt=.8 * (1 - b))
            for q in range(14):
                ang = q / 14 * 6.283 + seed
                r0, r1 = .2 * k + .9 * k * b, .35 * k + 1.2 * k * b
                col = ((255, 226, 100), (255, 120, 60), (150, 210, 255))[q % 3]
                IS.poly(img, [(hsx + math.cos(ang) * r0, hsy + math.sin(ang) * r0 + 40 * b * b),
                              (hsx + math.cos(ang) * r1, hsy + math.sin(ang) * r1 + 60 * b * b)], None, col,
                        max(1.0, 4 * (1 - b)), 0)
    else:
        # F6: smaller (was .18) and matt; round 4 (F20, rule 30: F6's .10 m still read big from this height, and
        # every missile in the air drew its stone at the old size): a 5-6 cm cobble, a thinner outline
        IS.ell(img, sx, sy, .055 * k, .042 * k, STONE3, INK, 1.4)


@lru_cache(None)
def _throws():
    """Every throw: (row, k, rep, kind, x0, d0, d1, t0, flight). Round 4 (F16): from each thrower's own plan (his
    style, speed of arm, pauses for stones), released 0.6 through his throw; none once the jet has reached him."""
    out = []
    for row, line in (('f', FRONT3), ('b', BACK3)):
        for k, (x0, d0) in enumerate(line):
            n = ('front' if row == 'f' else 'back') + str(k + 1)
            near = sorted(CRS_D, key=lambda d: abs(d - d0))[:2]     # the nearer of the two police groups
            tb = _break(n, k)[0]
            for rep, (t0, t1, _) in enumerate(throw_plan(n)):
                tr = t0 + 0.6 * (t1 - t0)
                if tr >= tb:
                    break
                what = MISSILES.get((row, k, rep % 7), 'stone')
                out.append((row, k, rep, what, x0, d0, near[rep % 2], tr, FLIGHT[STYLE[n]]))
    return tuple(out)


GAS_T, GAS_LAND = 1.25, (-3.9, 18.6)    # round 4 (F14, Sam: 'the canister lands amongst the police, not the crowd'):
GAS_FROM = (4.1, 16.2, 2.2)             # fired from the police block into the crowd's front rows


def t3_gas(img, lt):
    """F14: the canister arcs from the police into the crowd behind the throwers (1.25-1.65), the gas swells there
    and the wind takes it left and thins it (F21). Drawn over the crowd, under the acted people in front of it."""
    cam = T3CAM
    lx, ld = GAS_LAND
    t1 = GAS_T + 0.45
    if GAS_T <= lt < t1:
        def pos(u):
            x, d = lerp(GAS_FROM[0], lx, u), lerp(GAS_FROM[1], ld, u)
            return cam.p(x, d, lerp(GAS_FROM[2], 0.1, u) + 3.2 * math.sin(math.pi * u))
        a = (lt - GAS_T) / 0.45
        trail = [pos(max(0.0, a - q * 0.06)) + (8 + 6 * q,) for q in range(1, 6)]
        S.smoke(img, trail, (226, 228, 226), (250, 250, 248), line=(170, 176, 180), lw=2, fade=False)
        sx, sy = pos(a)
        IS.ell(img, sx, sy, 15, 8, (86, 94, 86), INK, 2.2)
        IS.ell(img, sx - 10, sy, 4, 7, (200, 60, 40), None)
    if lt < t1:
        return
    bx, by = cam.p(lx, ld, 0.3)
    k = cam.ppm(ld) / 60.0
    g = ease((lt - t1) / 0.6)
    if lt < t1 + 0.15:                                      # the landing: a quick white burst ring
        S.glow_disc(img, bx, by, 90 * k * (lt - t1 + .05) / 0.2, (255, 255, 255), amt=.7)
    wind = 70 * max(0.0, lt - t1 - 0.4)                     # F21: carried left (px), the gas rolling as it goes
    lumps = [(bx + k * dx * g - wind * (0.6 + 0.4 * (q % 3) / 2) + 10 * math.sin(lt * 1.6 + q),
              by - k * dy * g - 8 * math.cos(lt * 1.2 + q), k * (34 + r * g) * (1 + 0.12 * max(0.0, lt - t1)))
             for q, (dx, dy, r) in enumerate(((0, 0, 60), (-120, 20, 62), (130, 15, 62), (-60, 100, 66),
                                              (70, 115, 66), (0, 190, 70), (-190, 60, 50), (200, 55, 50)))]
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    S.smoke(lay, lumps, (226, 230, 230), (252, 252, 250), line=(170, 176, 180), lw=2.5)
    a = min(1.0, (lt - t1) / 0.3) * (1.0 - 0.6 * ease((lt - t1 - 1.5) / 3.0))    # thinning
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * 0.85 * a)))
    img.alpha_composite(lay)


def t3_fx(img, lt):
    cam = T3CAM
    # the throws (round 4: from the first frame until the jet reaches each thrower): stones, fruit, bottles, two fireworks, a cone, a wheel
    for row, k, rep, what, x0, d0, d1, t0, fl in _throws():
        if lt < t0 + fl * 2.9:
            _missile(img, cam, what, x0, d0, d1, t0, lt, flight=fl, spin=540 if what in ('cone', 'wheel') else 0,
                     seed=k * 7 + rep, lob=fl > 0.6)
    # the spent missiles lying in front of each group's shields (they pile up as the volleys land)
    rng = np.random.default_rng(17)
    for n in range(int(min(10, 4 + max(0, lt * 1.5)))):         # F12: some already there at the first frame
        d = rng.choice(CRS_D) + rng.uniform(-.4, .4)
        sx, sy = cam.p(SHIELD_X - rng.uniform(0.5, 0.9), d)
        k = cam.ppm(d)
        IS.ell(img, sx, sy - .02 * k, .045 * k, .03 * k, STONE3, INK, 1.2)   # F20: 5 cm
    # the water cannon jet: a white tapering stream from the roof cannon, sweeping the front line
    if lt >= 2.55 + J3:
        nx, ny = nozzle(lt)
        sweep = ease((lt - 2.55 - J3) / 1.3)
        ix, iy = cam.p(*jet_aim(lt), 1.3)                  # round 4 (F23/F22): down the rioters' line, on them
        if False:                                           # F10: the car stands far off now; the jet stays on the crowd
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
# Round 3 (Sam's notes A4-A16; the build plan in notes "## Round 3 Albania notes"): three crowds on the square, all
# 12.5 s: FRONT a melee with the police (d 12.2-16.4), MIDDLE gunmen + throwers (d 18-25) against police crouched
# behind a sandbag wall (A16, d 26.3), BACK dancers + Molotov throwers at the bank and the ministry (d 29-40). The
# helicopter flies in midway (4.6), the mopeds race in (5.5) and shoot it down (6.5), it lands behind the ministry and
# blows up at once (8.1): the cheer, the shield surf over the middle crowd, the fireworks. Everyone but the granny and
# the selfie is a sprite Actor (spr: drawn once per pose step, pasted), still one depth sort and still in the audit.
T4_LEN = dict(LENS)['t4']
MOPED0 = 5.5                       # A7: the mopeds race in; hl = lt - MOPED0: fire 0.6, hit 1.0, fall 1.0-2.6
HELI_IN = (4.6, 5.6)               # A7: the helicopter flies in from off the top right, midway
T4_FALL = 1.6
T4_HIT = MOPED0 + 1.0              # 6.5: the RPG hits it
T4_FIRE = T4_HIT + T4_FALL         # 8.1: it lands behind the ministry: the huge explosion at once (A7)
CHEER, HOLD, FW0 = 8.3, 8.6, 8.6   # the jubilation; the jumping hold; the fireworks
SURF, SURF_D, SURF_X = (8.6, 11.8), 21.0, (-5.6, -2.0)   # the shield surf over the middle crowd (on screen at d 21)
HELI_S = S.HELI_HOME[2] * 1.6     # chat 15 (hunt 1: "helicopter tiny and grey"): drawn larger than its depth
MOPED_D, MOPED_X = (10.5, 11.8), (-2.4, -3.4)   # A7: in from the left and they STAY (the selfie is to their right)
SELFIE = (1.7, 10.4)
MELEE_D = (12.2, 13.6, 15.0, 16.4)               # A4 FRONT: four rows, rioters left, police right
WALL_D, WALL_X, WALL_Z = 26.3, (1.5, 9.0), 1.05  # A16: the sandbag wall (no raised terrace)
COVER_D = 27.2
GRANNY = (-4.3, 17.6)                            # A8: in front of the middle crowd (no cart, no buying)
GRANNY_THROW, GRANNY_HIT = 3.4, 4.1
CROUCH = -0.6                                    # behind the wall: sunk so only the helmet peeps (cut at the wall top)


def onscreen_x(d, pad=0.35):
    """The leftmost / rightmost world x seen at depth d (T4CAM), pulled in by pad m."""
    c = T4CAM
    return (0 - c.VX) * d / c.F + pad, (W - c.VX) * d / c.F - pad


def heli_state(lt):
    x, y = S.HELI_HOME[0], S.HELI_HOME[1]
    if lt < HELI_IN[0]:
        return None
    if lt < HELI_IN[1]:                                    # A7: flies in nose first, banking, slowing to the hover
        u = ease((lt - HELI_IN[0]) / (HELI_IN[1] - HELI_IN[0]))
        return dict(x=lerp(W + 280, x, u), y=lerp(100, y, u), s=HELI_S, turn=0, roll=-4 - 12 * (1 - u), hit=False)
    if lt < T4_HIT:
        a = lt - HELI_IN[1]
        g = 1 - ease((lt - T4_HIT + 0.3) / 0.3)            # the bob settles into the hit's position
        return dict(x=x + 6 * math.sin(a * 2) * g, y=y + 4 * math.sin(a * 3) * g, s=HELI_S, turn=0, roll=-4, hit=False)
    u = min(1.0, (lt - T4_HIT) / T4_FALL)
    turn = (int(u * 14 * T4_FALL) * 45) % 360              # three drawn turns and their mirrors, stepped in 45s
    return dict(x=x - 60 * u + 30 * math.sin(u * 9), y=y + 520 * u ** 3 + 40 * u, s=HELI_S * (1 - .2 * u),
                turn=turn, roll=-4 + 40 * u, hit=True)


def moped_pos(lt, k):
    """A7: the two mopeds brake in from off the left (MOPED0) and stay; None before."""
    hl = lt - MOPED0
    if hl < 0:
        return None
    u = min(1.0, hl / 0.6)
    return lerp(-6.0 - 1.0 * k, MOPED_X[k], 1 - (1 - u) ** 3), MOPED_D[k]


def _q(u):
    """u in steps of 0.2 (six drawings a move: each sprite is drawn once and cached)."""
    return round(max(0.0, min(1.0, u)) * 5) / 5


def _cyc(lt, rate, off):
    return (lt * rate + off) % 1.0


def spr(name, kind, x, d, yaw, pose, u=0.0, lift=0.0, clip=None):
    """A crowd member drawn from a cached sprite of the cast's pose `pose` at step u (A4, build plan step 1)."""
    a = Actor(name, kind, x, d, int(round(yaw)), f'p:{pose}:{_q(u):.1f}', tier='t4', lift=lift, clip=clip,
              force='policia' if kind == 'officer' else None)
    a.spr = True
    return a


def _jump(lt, k):
    """The gleeful hold: everyone bouncing on their own beat (m off the ground)."""
    if lt < HOLD - 0.4:
        return 0.0
    return 0.42 * abs(math.sin(lt * 7.5 + k * 1.3)) * ease((lt - HOLD + 0.4) / 0.4)


def _throw_u(c, t_rel=0.62):
    """A throw's u over one cycle c (0..1): wound up and held, whipped through at t_rel, then follow through."""
    return 0.0 if c < t_rel - 0.12 else min(1.0, (c - t_rel + 0.12) / 0.2)


# ---- FRONT: the melee (A4), contact line wandering a little, all through the shot (A7: it carries on after the crash)
def melee_cx(d, lt):
    return 0.6 + 0.35 * math.sin(lt * 1.3 + d)


THROW_P = (1.45, 0.45)              # stone throws: a cycle every 1/0.7 s; the stone leaves at c 0.62, 0.45 s in the air


def melee(lt):
    out = []
    for r, d in enumerate(MELEE_D):
        cx = melee_cx(d, lt)
        for c in range(6):
            n = r * 6 + c
            off = (n * 0.37) % 1.0
            jit = 0.08 * math.sin(lt * 2.1 + n)
            if c == 0 and r % 2 == 0 or (c == 1 and r in (1, 3)):          # fists
                u = 1 - abs(2 * _cyc(lt, 1.6, off) - 1)
                out.append(spr(f'mr{n + 1}', 'rioter', cx - 0.42 - 0.62 * c + 0.12 * u + jit, d, 90, 'punch', u))
            elif c == 0:                                                    # machetes
                k = _cyc(lt, 1.1, off)
                u = min(1.0, k / 0.3) if k < 0.3 else 1 - (k - 0.3) / 0.7
                out.append(spr(f'mr{n + 1}', 'rioter', cx - 0.42 + jit, d, 90, 'machete', u))
            else:                                                           # stones at the police from behind
                u = _throw_u(_cyc(lt, 0.7, off))
                out.append(spr(f'mr{n + 1}', 'rioter', cx - 0.42 - 0.62 * c + jit, d, 90, 'throw', u))
            off2 = (n * 0.53 + 0.2) % 1.0
            px = cx + 0.42 + 0.6 * c - 0.05 * math.sin(lt * 1.7 + n)
            if c == 0:                                                      # batons v fists: hit, then driven back
                st = 'baton_up' if _cyc(lt, 0.75, off2) < 0.55 else 'pushed'
                out.append(spr(f'mp{n + 1}', 'officer', px, d + 0.1, -55, st))
            elif c == 1:
                out.append(spr(f'mp{n + 1}', 'officer', px, d + 0.1, -55, 'shield_up', 1.0))
            else:
                out.append(spr(f'mp{n + 1}', 'officer', px, d + 0.1, -55, 'line'))
    return out


def melee_stones(lt):
    """(t0, P0, P1) for each stone thrown in the melee (world), landing on the police shields."""
    out = []
    for r, d in enumerate(MELEE_D):
        for c in range(2, 6):
            n = r * 6 + c
            off = (n * 0.37) % 1.0
            per = 1 / 0.7
            k = math.floor(lt * 0.7 + off - 0.62) if lt > 0 else -1        # the last throw's index
            for q in (k - 1, k):
                t0 = (q + 0.62 - off) * per
                if 0 <= lt - t0 < THROW_P[1]:
                    cx = melee_cx(d, t0)
                    out.append((t0, (cx - 0.42 - 0.62 * c, d, 2.0), (cx + 0.5 + 0.3 * (n % 3), d + 0.1, 1.5)))
    return out


# ---- MIDDLE: gunmen and throwers against the police behind the wall (A4); the granny with her own bottle (A8)
@lru_cache(None)
def middle_spots():
    rng = np.random.default_rng(43)
    guns = [(-1.2 + 0.15 * math.sin(i * 2.1), 18.6 + i * 0.85, 'aim_rifle' if i % 8 not in (2, 5, 7) else 'aim_pistol')
            for i in range(8)]
    rest = []
    while len(rest) < 16:
        d = rng.uniform(18.0, 25.0)
        x = rng.uniform(max(-7.0, onscreen_x(d)[0]), -2.0)
        if any(abs(x - a) < 0.55 and abs(d - b) < 0.6 for a, b, *_ in rest + guns):
            continue
        rest.append((x, d, 'throw' if len(rest) % 8 < 5 else 'cheer', rng.uniform(0, 1)))
    return guns, rest


GUN_P, GUN_B = 1.6, 0.4             # a burst of 0.4 s every 1.6 s, each gunman at his own offset


def gun_burst(i, lt, per=GUN_P, off=None):
    """Firing this frame? (a burst, flashing on alternate frames)."""
    o = (i * 0.61) % 1.0 if off is None else off
    c = (lt / per + o) % 1.0
    return c < GUN_B / per and int(round(lt * FPS)) % 2 == 0


def middle(lt):
    out = []
    guns, rest = middle_spots()
    cheer = lt >= CHEER
    for i, (x, d, kind) in enumerate(guns):
        if cheer:                                          # A7: into the air for the crash
            st = 'rifle_up' if kind == 'aim_rifle' else 'cheer'
            u = (1.0 if gun_burst(i, lt, 0.5) else 0.0) if kind == 'aim_rifle' else 0.5 + 0.5 * math.sin(lt * 8 + i)
            out.append(spr(f'gun{i + 1}', 'rioter', x, d, 100, st, u, lift=_jump(lt, i) * 0.6))
        else:
            out.append(spr(f'gun{i + 1}', 'rioter', x, d, 100, kind, 1.0 if gun_burst(i, lt) else 0.0))
    for i, (x, d, kind, off) in enumerate(rest):
        x += 0.06 * math.sin(lt * 1.9 + i)
        if cheer:
            out.append(spr(f'mid{i + 1}', 'rioter', x, d, 70 + 30 * (i % 2), 'cheer', 0.5 + 0.5 * math.sin(lt * 9 + i),
                           lift=_jump(lt, i + 3)))
        elif kind == 'throw':
            out.append(spr(f'mid{i + 1}', 'rioter', x, d, 105, 'throw', _throw_u(_cyc(lt, 0.6, off))))
        else:                                              # yelling at the police: a fist pumped
            out.append(spr(f'mid{i + 1}', 'rioter', x, d, 100, 'cheer', 0.5 + 0.5 * math.sin(lt * 7 + i * 1.7)))
    return out + granny(lt)


def middle_stones(lt):
    """Stones from the middle crowd's throwers onto the sandbags and over (world)."""
    out = []
    _, rest = middle_spots()
    if lt >= CHEER:
        return out
    for i, (x, d, kind, off) in enumerate(rest):
        if kind != 'throw':
            continue
        per = 1 / 0.6
        k = math.floor(lt * 0.6 + off - 0.62)
        for q in (k - 1, k):
            t0 = (q + 0.62 - off) * per
            if 0 <= lt - t0 < 0.7:
                out.append((t0, (x + 0.3, d, 2.0), (2.2 + (i * 1.3) % 6.0, WALL_D - 0.1, WALL_Z + 0.1 * (i % 3))))
    return out


def granny(lt):
    """A8: she already has her bottle (no cart, no buying): steps up, winds up, throws overarm at the bank's first
    floor (the highest arc of the film), cheers her hit, and again for the crash."""
    x, d = GRANNY
    if lt < GRANNY_THROW - 0.5:
        return [Actor('granny', 'granny', x, d, -130, 'stand', tier='t4', extra=_bag)]
    if lt < GRANNY_HIT + 0.1:
        u = ease((lt - GRANNY_THROW + 0.1) / 0.3)
        return [Actor('granny', 'granny', x, d, -130, 'molotov', u=u, tier='t4', extra=_bag)
                .blend('stand', w=(lt - GRANNY_THROW + 0.5) / 0.25)]
    if lt < CHEER and lt > GRANNY_HIT + 1.2:
        return [Actor('granny', 'granny', x, d, -110, 'stand', tier='t4', extra=_bag).blend('cheer', u=1, w=(lt - GRANNY_HIT - 1.2) / 0.25)]
    return [Actor('granny', 'granny', x, d, -70, 'cheer', u=0.5 + 0.5 * math.sin(lt * 8), tier='t4', extra=_bag,
                  lift=_jump(lt, 9) * 0.4)]


def _bag(j):
    j['props'] = j.get('props', []) + [C.shopping_bag(j, 'L')]


def _bag_bottle(j):
    _bag(j)
    C.grips.held(j, 'R', None, C.bottle(j, 'R'))


# ---- POLICE IN COVER (A4, A16): crouched behind the sandbags, popping up to fire back; never after the crash
COVER_X = tuple(2.0 + 0.66 * i for i in range(10))
POP_P, POP_W = 2.0, 0.6


def cover_lift(i, lt):
    """How high officer i stands behind the wall (m): CROUCH hidden, 0 up and firing; the pop takes 0.12 s."""
    if lt >= CHEER - 0.4:
        return CROUCH, False
    c = (lt / POP_P + (i * 0.43) % 1.0) % 1.0 * POP_P
    up = ease(min(c, POP_W - c) / 0.12) if c < POP_W else 0.0
    return lerp(CROUCH, 0.0, up), up > 0.9


def wall_top_y():
    return T4CAM.p(0, WALL_D, WALL_Z)[1]


def cover(lt):
    out = []
    clip = (0, 0, W, int(wall_top_y()) + 1)
    for i, x in enumerate(COVER_X):
        lift, up = cover_lift(i, lt)
        if up:
            out.append(spr(f'cov{i + 1}', 'officer', x, COVER_D, -80, 'aim_pistol',
                           1.0 if gun_burst(i + 20, lt, 0.7) else 0.0, lift=lift, clip=clip))
        else:
            out.append(spr(f'cov{i + 1}', 'officer', x, COVER_D, -60, 'stand', 0.0, lift=lift, clip=clip))
    return out


def draw_wall(img):
    """A16: the sandbag wall: three courses of khaki bags, staggered, on the ground across x 1.5-9 at WALL_D, with a
    short return back along x 1.5 (the officers behind it)."""
    cam = T4CAM
    z0 = 0.0
    bag_w, bag_h = 0.62, WALL_Z / 3
    cols = ((168, 150, 104), (150, 134, 92), (180, 162, 114))
    for course in range(3):
        z = z0 + course * bag_h
        x = WALL_X[0] - (0.31 if course % 2 else 0.0)
        n = 0
        while x < WALL_X[1]:
            xa, xb = max(x, WALL_X[0]), min(x + bag_w, WALL_X[1])
            a, b = cam.p(xa, WALL_D, z), cam.p(xb, WALL_D, z + bag_h)
            cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            IS.ell(img, cx, cy, (b[0] - a[0]) / 2 + 2, (a[1] - b[1]) / 2 + 2, cols[(n + course) % 3], INK)
            IS.ell(img, cx - (b[0] - a[0]) * 0.18, cy - (a[1] - b[1]) * 0.15, (b[0] - a[0]) * 0.18,
                   (a[1] - b[1]) * 0.12, (196, 180, 134), None)
            x += bag_w
            n += 1
    for course in range(3):                                # the return, going back from the wall's left end
        z = z0 + course * bag_h
        for q in range(3):
            d0 = WALL_D + 0.55 * q + 0.35
            a, b = cam.p(WALL_X[0], d0, z), cam.p(WALL_X[0], d0 + 0.5, z + bag_h)
            IS.ell(img, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 9 + abs(b[0] - a[0]) / 2, (a[1] - b[1]) / 2 + 2,
                   cols[(q + course + 1) % 3], INK)


# ---- BACK: dancers and Molotov throwers (A4); the bottles land on the bank's and the ministry's windows (A5)
BANK_WIN = [(-9.0, 37.3, 2.4), (-9.0, 47.3, 2.4), (-9.0, 42.3, 7.8), (-9.0, 52.3, 11.8)]
MIN_WIN = [(10.0, 64.0, 5.5), (13.0, 64.0, 9.3)]
GRANNY_TO = (-9.0, 32.3, 7.8)                     # the bank's first floor, nearest window on screen


@lru_cache(None)
def back_spots():
    rng = np.random.default_rng(47)
    out = []
    while len(out) < 18:
        d = rng.uniform(29.0, 40.0)
        x = rng.uniform(max(-8.0, onscreen_x(d)[0]), -1.5)
        if any(abs(x - a) < 0.6 and abs(d - b) < 0.7 for a, b, *_ in out):
            continue
        out.append((x, d, rng.uniform(0, 1)))
    return out


MOL_P = 2.4


def back(lt):
    out = []
    for i, (x, d, off) in enumerate(back_spots()):
        if i < 13:                                         # dancing (jumps in time)
            out.append(spr(f'dan{i + 1}', 'rioter', x, d, (-20, 20, 0)[i % 3], 'dance', _cyc(lt, 1.0, off),
                           lift=0.22 * abs(math.sin(lt * 6.0 + i)) + _jump(lt, i) * 0.4))
        else:
            k = i - 13
            yaw = -90 if k < 3 else 162
            c = _cyc(lt, 1 / MOL_P, off)
            out.append(spr(f'mol{k + 1}', 'rioter', x, d, yaw, 'molotov', _throw_u(c, 0.5)))
    return out


def throws():
    """Every Molotov of the shot (t0, t1, P0, P1, apex m, big, target index): the back throwers' and the granny's."""
    out = []
    for i, (x, d, off) in enumerate(back_spots()[13:]):
        tgts = BANK_WIN if i < 3 else MIN_WIN
        q = 0
        while True:
            t0 = (q + 0.5 - off) * MOL_P
            q += 1
            if t0 < 0:
                continue
            if t0 > T4_LEN + 3.0:
                break
            p1 = tgts[(i + q) % len(tgts)]
            fl = 0.9 if i < 3 else 1.6
            out.append((t0, t0 + fl, (x, d, 2.2), p1, 4.0 if i < 3 else 9.0, 0.9, ('bank' if i < 3 else 'min', p1)))
    x, d = GRANNY
    out.append((GRANNY_THROW, GRANNY_HIT, (x - 0.2, d, 2.0), GRANNY_TO, 11.0, 1.9, ('granny', GRANNY_TO)))
    return out


def t4_actors(lt):
    out = melee(lt) + middle(lt) + cover(lt) + back(lt) + carriers(lt)
    if _PLATE:
        out = [a for a in out if a.name != 'granny']
    else:
        out += selfie(lt)
    return out + surfer(lt)


# ---- the surf (A7): a rioter on a captured riot shield carried over the middle crowd by four cheering carriers
def surf_pos(lt):
    t0, t1 = SURF
    rise = ease((lt - t0) / 0.3)
    u = ease(min(1.0, max(0.0, (lt - t0 - 0.2) / (t1 - t0 - 0.2))))
    x = lerp(SURF_X[0], SURF_X[1], u) + 0.12 * math.sin(lt * 9.0) * min(u * 8, 1.0)
    z = lerp(1.6, 2.1, rise) + 0.07 * math.sin(lt * 14 + 1)
    z += 0.45 * abs(math.sin((lt - t0) * 6.2)) * ease((lt - t0 - 0.6) / 0.3)   # the blanket toss
    return x, z


CARRY = ((-0.4, -0.22), (0.4, -0.22), (-0.4, 0.22), (0.4, 0.22))


def carriers(lt):
    if lt < SURF[0]:
        return []
    x, z = surf_pos(lt)
    return [spr(f'carrier{k + 1}', 'rioter', x + cx, SURF_D + cd, 90 if k % 2 else -90, 'dance', 0.0,
                lift=max(0.0, z - 2.1) * 0.4) for k, (cx, cd) in enumerate(CARRY)]


def surfer(lt):
    if lt < SURF[0]:
        return []
    x, z = surf_pos(lt)
    return [Actor('surfer', 'rioter', x, SURF_D, 25 + 18 * math.sin(lt * 4.3), 'flag:albania', tier='t4', lift=z)]


def draw_surf_shield(img, lt):
    """The riot shield flat over the carriers' raised hands."""
    if lt < SURF[0]:
        return
    cam = T4CAM
    x, z = surf_pos(lt)
    pts = [cam.p(x + px, SURF_D + pd, z) for px, pd in ((-0.6, 0.3), (0.6, 0.3), (0.6, -0.3), (-0.6, -0.3))]
    lip = [pts[3], pts[2], cam.p(x + 0.6, SURF_D - 0.3, z - 0.05), cam.p(x - 0.6, SURF_D - 0.3, z - 0.05)]
    S.shape(img, [lip], (150, 166, 180), INK, 2)
    S.shape(img, [pts], (206, 222, 232), INK, 2.5)
    band = [cam.p(x + px, SURF_D + pd, z) for px, pd in ((-0.6, 0.05), (0.6, 0.05), (0.6, -0.07), (-0.6, -0.07))]
    S.shape(img, [band], (40, 50, 120), None)


def selfie(lt):
    """Gag b (A7: keyed on the mopeds): watching the riot, back to us; turns his back on the helicopter at the hit +
    0.2, phone up, peace sign; the flash with it falling behind his head; thumbs up; then cheers the crash."""
    x, d = SELFIE
    hl = lt - MOPED0
    if hl < 1.2:
        return [Actor('selfie', 'rioter', x, d, 180, 'stand', tier='t4')]
    if hl < 1.45:
        yaw = (135, 90, 45)[min(2, int((hl - 1.2) / 0.085))]
        return [Actor('selfie', 'rioter', x, d, -yaw, 'stand', tier='t4')]
    if lt < CHEER:
        u = ease((hl - 2.4) / 0.2)
        w = (hl - 1.45) / 0.25
        return [Actor('selfie', 'rioter', x, d, _turn(-45, 0, w), 'selfie', u=u, tier='t4').blend('stand', w=w)]
    return [Actor('selfie', 'rioter', x, d, 10, 'cheer', u=0.5 + 0.5 * math.sin(lt * 8), tier='t4',
                  lift=_jump(lt, 4)).blend('selfie', u=1.0, w=(lt - CHEER) / 0.25)]


# ---- the helicopter's fire trail and the huge explosion (behind the ministry)
def t4_under(img, lt):
    """Drawn in the painting behind the ministry: the helicopter's fire trail and the fireball."""
    if lt >= T4_HIT:
        for n in range(10):
            a = lt - T4_HIT - n * 0.1
            if a < 0:
                continue
            h = heli_state(T4_HIT + n * 0.1)
            r = 20 + 30 * min(a, 1.2)
            S.smoke(img, [(h['x'] + 10, h['y'] - 10 - 30 * a, r)], (60, 40, 40), (96, 70, 66), lw=2)
    t4_fireball(img, lt)


BOOM = 1.7                          # A7/step 9: the huge explosion, 1.7x the old fireball


def t4_fireball(img, lt):
    """The huge explosion the moment the helicopter lands (T4_FIRE): a layered fireball rising, 1.7x."""
    if lt >= T4_FIRE:
        g = ease((lt - T4_FIRE) / 0.6)
        k = BOOM
        cx, cy = 720, lerp(700, 420, g)
        S.glow_disc(img, cx, cy, (160 * g + 60) * k, (255, 190, 110), amt=.25)
        S.smoke(img, [(cx + k * 1.3 * dx * g, cy - 40 * g + k * 1.3 * dy * g, k * 1.3 * r * (0.4 + 0.6 * g))
                      for dx, dy, r in ((0, -110, 120), (-130, -60, 90), (130, -70, 100), (-60, -200, 90),
                                        (80, -210, 90))], (70, 40, 36), (170, 96, 60), lw=2.5)
        S.flames(img, cx, cy + (140 * g + 60) * k * 0.8, 360 * k * (0.5 + 0.5 * g), 420 * k * (0.4 + 0.6 * g), lt,
                 seed=95, n=8)
        S.flames(img, cx, cy + (80 * g + 40) * k * 0.8, 220 * k * (0.5 + 0.5 * g), 260 * k * (0.4 + 0.6 * g), lt + .3,
                 seed=97, n=6)
        S.glow_disc(img, cx, cy + 40, (90 * g + 20) * k, (255, 250, 200), amt=.5)


def boom_fx(img, lt):
    """Over everything: the white flash (0.15 s), the shock ring and the debris of the huge explosion."""
    a = lt - T4_FIRE
    if a < 0 or a > 1.6:
        return
    cx, cy = 720, 700
    if a < 0.15:
        fl = Image.new('RGBA', img.size, (255, 250, 236, int(230 * (1 - a / 0.15))))
        img.alpha_composite(fl)
    if a < 0.6:
        r = 120 + 1400 * ease(a / 0.6)
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse((cx - r, cy - r * 0.42, cx + r, cy + r * 0.42), outline=(255, 236, 200, 255),
                                    width=int(14 * (1 - a / 0.6)) + 2)
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * (1 - a / 0.6))))
        img.alpha_composite(lay)
    rng = np.random.default_rng(88)
    for q in range(22):
        ang = rng.uniform(-math.pi * 0.95, -math.pi * 0.05)
        v = rng.uniform(500, 1300)
        x = cx + math.cos(ang) * v * a
        y = cy + math.sin(ang) * v * a + 900 * a * a
        s = rng.uniform(6, 16)
        rot = a * rng.uniform(6, 14)
        pts = [(x + s * math.cos(rot + t), y + s * 0.6 * math.sin(rot + t)) for t in (0, 2.1, 3.6, 5.0)]
        IS.poly(img, pts, (36, 30, 30), INK, 1.5, 0)
        if q % 3 == 0:
            S.glow_disc(img, x, y, 10, (255, 170, 60), amt=.5)


def t4_mopeds(img, lt):
    cam = T4CAM
    for k in (1, 0):
        p = moped_pos(lt, k)
        if p is None:
            continue
        gx, gy = cam.p(*p)
        s = scale_at(cam, p[1])
        C.moped_scene(img, _cam2(), gx, gy - FEET * s, s, yaw=90, aim=38.0,
                      fired=(k == 0 and lt >= MOPED0 + 0.6), both=True)


def rpg_tip():
    x, d = moped_pos(MOPED0 + 0.6, 0)
    return T4CAM.p(x - 0.1, d, 2.05)


def _world_arc(p0, p1, apex, u):
    """A thrown thing in the world: straight from p0 to p1, a parabola `apex` m over the higher end."""
    x, d, z = (lerp(a, b, u) for a, b in zip(p0, p1))
    return x, d, z + 4 * apex * u * (1 - u)


def stones(img, lt):
    cam = T4CAM
    for t0, p0, p1 in melee_stones(lt) + middle_stones(lt):
        fl = THROW_P[1] if p1[1] < 20 else 0.7
        u = (lt - t0) / fl
        x, y = cam.p(*_world_arc(p0, p1, 0.6 if p1[1] < 20 else 1.5, u))
        r = max(2.5, 0.09 * cam.ppm(p0[1]))
        IS.ell(img, x, y, r, r, (112, 104, 94), INK)
        if u > 0.85 and p1[1] > 20:                         # a puff of grit off the sandbags
            gx, gy = cam.p(*p1)
            IS.ell(img, gx, gy - 4, 7, 4, (200, 184, 150), None)


def gunfire(img, lt):
    """Muzzle flashes (a glow and a star) on the flash frames, a 1-frame tracer to the target, sparks and dust off the
    sandbags; the police flashes back at the middle crowd."""
    cam = T4CAM
    pen = IS.pen(img)
    rng = np.random.default_rng(int(lt * FPS) + 5)
    shots = []
    guns, rest = middle_spots()
    for i, (x, d, kind) in enumerate(guns):
        if lt < CHEER and gun_burst(i, lt):
            shots.append(((x, d, 100, 0.0), (rng.uniform(2.2, 8.5), WALL_D, WALL_Z + rng.uniform(0, 0.3)), True))
        elif lt >= CHEER and kind == 'aim_rifle' and gun_burst(i, lt, 0.5):
            fx, fd = facing(100)
            shots.append(((x, d, 100, _jump(lt, i) * 0.6), None, True))
    for i, x in enumerate(COVER_X):
        lift, up = cover_lift(i, lt)
        if up and gun_burst(i + 20, lt, 0.7):
            gx, gd, *_ = guns[i % len(guns)]
            shots.append(((x, COVER_D, -80, lift), (gx - 0.5, gd - 0.6, 1.3), False))
    for (x, d, yaw, lift), tgt, ours in shots:
        fx, fd = facing(yaw)
        up = tgt is None
        m = (x + fx * 0.9, d + fd * 0.9, (2.5 if up else 1.45) + lift)
        mx, my = cam.p(*m)
        S.glow_disc(img, mx, my, 0.5 * cam.ppm(d), (255, 210, 120), amt=.75)
        glint(img, mx, my, 0.28 * cam.ppm(d))
        if up:
            pen.line([(mx, my), (mx + 30, my - 260)], (255, 236, 170), 2)
            continue
        tx, ty = cam.p(*tgt)
        pen.line([(mx, my), (lerp(mx, tx, 0.85), lerp(my, ty, 0.85))], (255, 236, 170), 2)
        if ours:                                           # it smacks the sandbags: sparks and a puff of dust
            for q in range(4):
                a = rng.uniform(-2.6, -0.5)
                pen.line([(tx, ty), (tx + 12 * math.cos(a), ty + 12 * math.sin(a))], (255, 220, 120), 2)
            IS.ell(img, tx, ty - 5, 9, 5, (206, 190, 150), None)


def t4_fx(img, lt):
    cam = T4CAM
    hl = lt - MOPED0
    if hl >= 0.6:                                          # the rocket: fired, climbs to the helicopter, hits at 1.0
        x0, y0 = rpg_tip()
        hx, hy = R4(S.HELI_HOME[0], S.HELI_HOME[1])
        u = min(1.0, (hl - 0.6) / 0.4)
        N = 110
        lumps = []
        for k in range(int(N * u) + 1):
            v = k / N
            age = max(0.0, hl - 0.6 - v * 0.4)
            g = min(age, 2.0)
            r = 9 + 16 * g / (1 + 0.5 * g) + 2.5 * math.sin(k * 1.7)
            lumps.append((lerp(x0, hx, v) + 30 * g + 6 * math.sin(k * 2.3 + g * 3), lerp(y0, hy, v)
                          - 40 * math.sin(math.pi * v) - 18 * g, r))
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        S.smoke(lay, lumps, (190, 176, 170), (226, 214, 206), lw=2)
        fade = 1 - 0.75 * ease((hl - 1.4) / 2.0)
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * fade)))
        img.alpha_composite(lay)
        if u < 1:
            rx, ry = lerp(x0, hx, u), lerp(y0, hy, u) - 40 * math.sin(math.pi * u)
            S.glow_disc(img, rx, ry, 26, (255, 230, 150), amt=.6)
    t4_hit(img, lt)
    if 0.6 <= hl < 1.1:                                    # the backblast out of the launcher's rear
        a = (hl - 0.6) / 0.5
        tx, ty = rpg_tip()
        bx, by = tx - 150, ty + 120
        bl = Image.new('RGBA', img.size, (0, 0, 0, 0))
        S.smoke(bl, [(bx - 70 * a - 34 * q, by + 40 * a + 22 * q, 22 + 46 * a + 8 * q) for q in range(4)],
                (226, 220, 210), (250, 246, 240), line=None, lw=1)
        bl.putalpha(bl.getchannel('A').point(lambda v: int(v * 0.55 * (1 - a))))
        img.alpha_composite(bl)
        if a < 0.3:
            S.glow_disc(img, tx, ty, 40, (255, 230, 150), amt=.55)
    molotovs(img, lt)
    stones(img, lt)
    gunfire(img, lt)
    rng = np.random.default_rng(int(lt * 12))              # A4: the melee's dust, all through (low, soft, see-through)
    dl = Image.new('RGBA', img.size, (0, 0, 0, 0))
    for _ in range(4):
        d = MELEE_D[int(rng.integers(0, 4))]
        sx, sy = cam.p(melee_cx(d, lt) + rng.uniform(-1.2, 1.2), d, 0.1)
        r = rng.uniform(22, 38)
        S.smoke(dl, [(sx - r * .6, sy, r * .7), (sx + r * .6, sy + 4, r * .6), (sx, sy - r * .3, r * .8)],
                (176, 146, 120), (206, 178, 150), line=None, lw=1)
    dl.putalpha(dl.getchannel('A').point(lambda v: int(v * 0.3)))
    img.alpha_composite(dl)
    if int(lt * 12) % 3 == 0:                              # a shield-impact flash somewhere on the line
        d = MELEE_D[int(rng.integers(0, 4))]
        sx, sy = cam.p(melee_cx(d, lt) + 0.3, d, 1.2)
        S.glow_disc(img, sx, sy, 30, (255, 250, 220), amt=.5)
    for fx, fd in ((-5.2, 24.0), (-7.4, 30.0)):            # two red flares held up in the crowd
        bx, by = cam.p(fx, fd, 1.9)
        tx, ty = cam.p(fx + 0.05, fd, 2.5)
        IS.poly(img, [(bx, by), (tx, ty)], None, (40, 30, 30), 4, 0)
        S.glow_disc(img, tx, ty, 34 + 5 * math.sin(lt * 20 + fd), (255, 70, 50), amt=.4)
        IS.ell(img, tx, ty, 5, 5, (255, 236, 220), None)
    flying_shield(img, lt)
    if 1.8 <= hl < 1.95 and not _PLATE:                    # gag b: the selfie's flash, the helicopter falling behind him
        x, d = SELFIE
        fx, fy = cam.p(x - 0.05, d, 2.25)
        S.glow_disc(img, fx, fy, 30 * (1 - (hl - 1.8) / 0.15) + 12, (255, 255, 245), amt=.85)
    embers(img, lt)
    if lt >= FW0 - 0.2:
        for k, (t0, x, y, col) in enumerate(FIREWORKS):
            n = int((lt - t0) // 0.75)
            for rep_ in (n - 1, n):
                if rep_ >= 0:
                    burst(img, x + 40 * (rep_ % 3), y + 30 * (rep_ % 2), lt - t0 - 0.75 * rep_, col, k + rep_)
    boom_fx(img, lt)


FIREWORKS = ((FW0 - 0.2, 260, 230, (255, 90, 70)), (FW0 + 0.05, 760, 150, (255, 250, 210)),   # over the
             (FW0 + 0.3, 520, 290, (110, 255, 150)), (FW0 + 0.5, 930, 300, (255, 200, 60)))    # headings


def t4_hit(img, lt):
    """The hit (hl 0.98-1.3): a flash and a burst at the helicopter."""
    hl = lt - MOPED0
    if 0.98 <= hl < 1.3:
        a = (hl - 0.98) / 0.32
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


def molotovs(img, lt, only=None):
    """A4/A8: the back throwers' bottles and the granny's, each tumbling along its arc (world) into a window and
    blooming orange; each window hit stays alight (the biggest fire there)."""
    cam = T4CAM
    lit = {}
    for n, (t0, t1, p0, p1, apex, big, tag) in enumerate(throws()):
        if only is not None and n != only:
            continue
        if t0 <= lt < t1:
            u = (lt - t0) / (t1 - t0)
            x, y = cam.p(*_world_arc(p0, p1, apex, u))
            ang = u * (9 + 3 * big)
            sz = max(10.0, 0.22 * cam.ppm(lerp(p0[1], p1[1], u)) * big)
            ca, sa = sz * math.cos(ang), sz * math.sin(ang)
            IS.poly(img, [(x + ca, y + sa), (x - ca, y - sa)], None, INK, max(6, sz * 0.6), 0)
            IS.poly(img, [(x + ca, y + sa), (x - ca, y - sa)], None, (70, 140, 70), max(4, sz * 0.4), 0)
            S.glow_disc(img, x + ca, y + sa, sz * 1.3, (255, 190, 80), amt=.8)
            for q in range(1, 6):
                tx, ty = cam.p(*_world_arc(p0, p1, apex, max(0.0, u - q * 0.025)))
                IS.ell(img, tx, ty, sz * 0.35 - q, sz * 0.35 - q, (255, 170 + 12 * q, 60), None)
        elif lt >= t1:
            a = lt - t1
            ex, ey = cam.p(*p1)
            k = cam.ppm(p1[1]) / 40.0                       # sized by the window's distance
            if a < 0.25:
                g = ease(a / 0.25)
                S.glow_disc(img, ex, ey, (90 + 80 * g) * big ** 0.7 * k, (255, 220, 120), amt=.7 * (1 - g) + .2)
                IS.ell(img, ex, ey, (40 * big * (1 - g) + 6) * k, (40 * big * (1 - g) + 6) * k, (255, 252, 230), None)
            key = tag[1]
            lit[key] = max(lit.get(key, (0, 0))[0], big), max(lit.get(key, (0, 0))[1], min(1.0, a / 0.6))
    for (x, d, z), (big, g) in lit.items():
        k = cam.ppm(d) / 40.0
        ex, ey = cam.p(x, d, z)
        S.glow_disc(img, ex, ey - 20 * k, (80 + 40 * g) * big * k, (255, 150, 50), amt=.35)
        S.flames(img, ex, ey + 34 * big * k, (90 + 50 * g) * big * k, (70 + 90 * g) * big * k, lt + x * .37,
                 seed=93 + int(d), n=5)


def flying_shield(img, lt):
    """The melee's one clear gag: a riot shield knocked spinning up out of the line (3.0) and down behind it."""
    t0, t1 = 3.0, 4.0
    if not t0 <= lt < t1:
        return
    cam = T4CAM
    u = (lt - t0) / (t1 - t0)
    x0, y0 = cam.p(1.0, MELEE_D[1], 1.2)
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
    """The explosion behind the ministry backlights the square (lighter than before: the cheer must read)."""
    if lt < T4_FIRE:
        return ppl
    k = 0.32 * ease((lt - T4_FIRE) / 0.5)
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
    return -45, 45, roll                           # A11/A12: each turned to the other (eye contact), not to camera


SHRUG = (2.25, 0.6)                                # A12: the shrug AFTER the line (Sam's take ends ~2.05)


def rider_faces(tier, lt):
    """A11/A12 (shot C): the driver's eyes on the passenger; the passenger's on the driver, brows up and knit,
    genuinely perplexed through the shrug."""
    if tier != 'ec':
        return None, None
    e = ease((lt - SHRUG[0]) / SHRUG[1])
    return (dict(look=-0.6),
            dict(look=0.6, brow_up=0.02 + 0.05 * e, frown=0.004 + 0.016 * e, smile=-0.2 - 0.4 * e))


def end_riders(img, tier, lt, z):
    cam = z.cam
    x = moped2_x(lt) if tier == 'ea' else MOPED2_X
    gx, gy = cam.p(x, MOPED2_D)
    s = scale_at(cam, MOPED2_D)
    aim = (38 + 24 * ease((lt - 0.3) / 0.4)) if tier == 'ea' else 62.0   # C: the cast sheet's shrug angle (45 folded his arm)
    dh, gh, roll = rider_heads(tier, lt)
    shrug_u = ease((lt - SHRUG[0]) / SHRUG[1]) if tier == 'ec' else 0.0
    df, gf = rider_faces(tier, lt)
    fired = tier == 'ea' and lt >= 0.8                     # chat 27: shot C has already reloaded (the warhead reads as an RPG)
    C.moped_scene(img, _cam2(), gx, gy - FEET * s, s, yaw=90, aim=aim, fired=fired, both=True, drv_head=dh,
                  gun_head=gh, shrug_u=shrug_u, rim=None, drv_roll=roll, drv_face=df, gun_face=gf)   # A9: no outline
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
        hide = int(cam.p(0, 2.62, 0.53)[1])                 # A10: half way down the bins, through the camera (was 1300)
        ppl.paste((0, 0, 0, 0), (0, hide, W, H))            # below the lids they are hidden: no feet under the bins
        back.alpha_composite(ppl)
        back.alpha_composite(front)
        return back
    z = ZA if tier == 'ea' else ZC
    bg = END_BG0 + (lt if tier == 'ea' else dict(LENS)['ea'] + dict(LENS)['eb'] + lt)
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
                draw_prop(back, cam, a)
            draw_actor(back, cam, a)
            if a.prop and not a.prop_before:
                draw_prop(back, cam, a)
        if not board:
            t2_board(back, lt)
        t2_fx(back, lt)
        phone_lights(back, acts, cam)
        blue_wash(back, lt)
    elif tier == 't3':
        back, front = S.t3(lt, car=False, kiosk=False, drift=True)   # round 4: no kiosk (F17), the far smoke drifts (F21)
        back = reframe3(back)
        front = reframe3(front) if front is not None else None
        cam = T3CAM
        acts = sorted(t3_actors(lt), key=lambda a: -a.d)
        rear, rear2 = car_depth(), car2_fx_depth()          # F10: the car among the crowd by Marianne; F17: the second
        t3_crowd(back, lt, d_lo=rear)
        for a in [a for a in acts if a.d > rear]:           # the people on the base, beyond the car
            draw_actor(back, cam, a)
        draw_car3(back, lt)
        t3_crowd(back, lt, d_hi=rear, d_lo=rear2)
        draw_car3b(back, lt)
        t3_crowd(back, lt, d_hi=rear2)
        t3_columns(back, lt)                                # chat 15: smoke, then the people beyond the truck
        t3_gas(back, lt)                                    # round 4 (F14): the gas in the crowd, under the throwers
        t3_debris(back)
        for a in [a for a in acts if rear >= a.d > T3_TRUCK_D]:   # round 3 (F8): the far police group behind the truck,
            draw_actor(back, cam, a)                        # which drives up the lane between the two groups
        S.truck(back, cam, truck_x(lt), T3_TRUCK_D, lt, 'drive', 'fr', 12, float(int(lt * 6) % 2))
        for a in [a for a in acts if NEAR3 < a.d <= T3_TRUCK_D]:
            draw_actor(back, cam, a)
        t3_fx(back, lt)                                     # the jet and the missiles over them,
        for a in [a for a in acts if a.d <= NEAR3]:         # under the nearest (where the car's rear stood till F10)
            draw_actor(back, cam, a)
    else:
        h = heli_state(lt)
        under = lambda img: t4_under(img, lt)              # noqa: E731
        if h:
            h['under'] = under
        back, front = S.t4(lt, heli=h)
        if not h:
            under(back)
        back = RF4.image(back)
        front = RF4.image(front) if front is not None else None
        cam = T4CAM
        ppl = Image.new('RGBA', back.size, (0, 0, 0, 0))
        for a in sorted(t4_actors(lt) + ['wall'], key=lambda a: -(WALL_D if a == 'wall' else a.d)):
            if a == 'wall':
                draw_wall(ppl)                              # A16: the sandbags in their place among the people
            elif a.name == 'surfer':
                pass                                        # drawn after the backlight (he is lit: the new action)
            else:
                draw_actor(ppl, cam, a)
        if not _PLATE:
            t4_mopeds(ppl, lt)
        back.alpha_composite(backlight(back, lt, ppl))
        if lt >= SURF[0] and not _PLATE:                    # the surfer lit (not in the end's A/C)
            sx, sz = surf_pos(lt)
            gx, gy = cam.p(sx, SURF_D, sz + 1.2)
            S.glow_disc(back, gx, gy, 2.2 * cam.ppm(SURF_D), (255, 190, 110), amt=.3)
            draw_surf_shield(back, lt)
            for a in surfer(lt):
                draw_actor(back, cam, a)
        t4_fx(back, lt)
        hy = 1230 if RF4 is RF4_LOW else 1477
        haze(back, lt, [(R4(x, hy), 220) for x in (100, 400, 700, 1000)], 0.3, (200, 170, 150), .1, 7)
        if lt > 1.0:                                        # white gas between the melee and the sandbags
            g = ease((lt - 1.0) / 0.6)
            gl = Image.new('RGBA', back.size, (0, 0, 0, 0))
            S.smoke(gl, [(cam.p(x, 19.5, 0.3)[0] + dx, cam.p(x, 19.5, 0.3)[1], 26 + 30 * g) for x in (4.2, 5.6, 7.0)
                         for dx in (-30, 30)], (226, 228, 226), (250, 250, 248), line=None, lw=1)
            gl.putalpha(gl.getchannel('A').point(lambda v: int(v * 0.4)))
            back.alpha_composite(gl)
    if front is not None:
        back.alpha_composite(front)
    return back


def draw_order(t):
    tier, lt = scene_of(t)
    names = {'t1': lambda: ['painting', 'police'] + [a.name for a in t1_actors(lt)] + ['march', 'fx', 'haze'],
             't2': lambda: ['painting'] + [a.name for a in sorted(t2_actors(lt), key=lambda a: -a.d)] + ['fx', 'blue'],
             't3': lambda: ['painting', 'crowd'] + [a.name for a in sorted(t3_actors(lt), key=lambda a: -a.d)
                                                    if a.d > T3_TRUCK_D] + ['truck'] +
                           [a.name for a in sorted(t3_actors(lt), key=lambda a: -a.d) if a.d <= T3_TRUCK_D]
             + ['fx', 'car'],
             't4': lambda: ['painting', 'helicopter', 'ministry'] +
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
    if lt < T2_SHATTER + 0.1:
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
        if lt >= INTENSITY_AT:                             # O8: 50% bigger (81 px). The number pops in (a short grow) in its tier's colour
            u = min(1.0, (lt - INTENSITY_AT) / 0.12)
            fn = _font(max(8, int(81 * k * (0.6 + 0.4 * u + 0.15 * math.sin(math.pi * u)))))
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
SFX = os.path.join(os.path.dirname(HERE), 'sounds', 'protest-tiers')


def sfx(name, a=0.0, b=None, peak=0.5, fade=0.08):
    """Sam's sound file `name` (sounds/protest-tiers/NAME.mp3) cut to a-b seconds, scaled to `peak`, a short fade out
    (O9, G19)."""
    import mossad_audio as MA
    x = MA.load(os.path.join(SFX, name + '.mp3'))
    x = x[int(a * MA.SR):None if b is None else int(b * MA.SR)].astype(float)
    x = x / (np.abs(x).max() or 1) * peak
    nf = min(len(x), int(fade * MA.SR))
    if nf:
        x[-nf:] *= np.linspace(1, 0, nf)
    return x


PARIS = os.path.join(HERE, '..', 'sounds', 'protest-tiers')
T3_CROWD = (0.4, 6.4)        # F24: paris-riot.mp3 by loudness over time: 0.4-6.4 shouting/chanting crowd (voiced,
T3_CANNON = (9.6, 13.4)      # mid-heavy); 7.0-14.7 the water cannon's broadband hiss (loudest spray 10.5-12.75); no engine


def _cut(x, sr, a, b, fade=0.03):
    """x[a:b] seconds with short fades so no slice clicks."""
    y = x[int(a * sr):int(b * sr)].copy()
    k = min(int(fade * sr), len(y) // 2)
    if k:
        y[:k] *= np.linspace(0, 1, k)
        y[-k:] *= np.linspace(1, 0, k)
    return y


def t3_sound(mix, sr, load):
    """Round 5 (F24, Sam: 'take sound from' his Paris riot recording + banked effects): T3's crowd bed (looped with a
    crossfade under all 8 s), the water cannon JET_ON -> SWEEP end, stone-hit on each stone's shield hit, glass-smash on
    each bottle's, a firework crackle on each firework's. Fruit lands soft: no sound."""
    t0, L = START['t3'], dict(LENS)['t3']
    riot = load(os.path.join(PARIS, 'paris-riot.mp3'))
    bed, xf = _cut(riot, sr, *T3_CROWD, fade=0.5), int(0.5 * sr)
    out = bed.copy()
    while len(out) < (L + 0.6) * sr:                       # loop with a 0.5 s overlap (fades cross)
        out = np.concatenate([out[:-xf], out[-xf:] + bed[:xf], bed[xf:]])
    bed = out[:int((L + 0.3) * sr)]
    bed[-int(0.3 * sr):] *= np.linspace(1, 0, int(0.3 * sr))   # out under the cut to T4
    i = int(t0 * sr)
    mix[i:i + len(bed)] += 0.35 * bed[:max(0, len(mix) - i)]
    jet = _cut(riot, sr, T3_CANNON[0], T3_CANNON[0] + SWEEP[1] - JET_ON + 0.4, fade=0.08)
    jet[-int(0.4 * sr):] *= np.linspace(1, 0, int(0.4 * sr))   # the jet shuts off at the sweep's end
    i = int(at('t3', JET_ON) * sr)
    mix[i:i + len(jet)] += 0.5 * jet[:max(0, len(mix) - i)]
    stone, glass = load(os.path.join(PARIS, 'stone-hit.mp3')), load(os.path.join(PARIS, 'glass-smash.mp3'))
    fw = load(os.path.join(PARIS, 'fireworks.mp3'))
    kits = {'stone': ([_cut(stone, sr, s, s + 0.3) for s in (0.0, 1.0, 2.0)], 0.28),
            'bottle': ([_cut(glass, sr, 0.0, 0.9, 0.05), _cut(glass, sr, 1.5, 2.4, 0.05)], 0.25),
            'firework': ([_cut(fw, sr, 0.0, 0.7, 0.05), _cut(fw, sr, 14.0, 14.7, 0.05)], 0.4)}
    n = {}
    for row, k, rep, what, x0, d0, d1, th, fl in sorted(_throws(), key=lambda r: r[7] + r[8]):
        land = th + fl
        if what not in kits or not 0 <= land < L:
            continue
        clips, g = kits[what]
        c = clips[n.get(what, 0) % len(clips)]
        n[what] = n.get(what, 0) + 1
        g *= 0.75 if d1 > 14 else 1.0                       # the far police block a touch quieter
        i = int(at('t3', land) * sr)
        mix[i:i + len(c)] += g * c[:max(0, len(mix) - i)]
    return mix


METAL = os.path.join(SFX, 'heavy-metal.mp3')
RIFF_AT = 19.88              # A14: the riff's first hit in Sam's track (loudness jumps 0.11 -> 0.43 at 19.88 s)
METAL_LUFS, DUCK = -21.0, (0.35, 1800.0)   # under the scene; under each line: 35% and muffled above 1.8 kHz


def t4_sound(mix, sr):
    """A14: Sam's heavy-metal track from its riff's first hit at T4's first frame, on through the end scene, ducked
    (quieter and muffled) under each line of dialogue, back up between; A15: the Blue Planet film's explosions,
    levelled as there (flying_whales_sound.clip): the minor one on the RPG hit, the major one on the landing."""
    import mossad_audio as MA
    import filmkit
    from scipy.signal import butter, sosfilt
    x = MA.load(METAL)
    t0 = at('t4', 0.0)
    m = x[int(RIFF_AT * sr):int((RIFF_AT + DUR - t0) * sr)].astype(float)
    m *= 10 ** ((METAL_LUFS - MA.lufs(m)) / 20)
    nf = int(0.5 * sr)
    m[-nf:] *= np.linspace(1, 0, nf)
    low = sosfilt(butter(4, DUCK[1], 'low', fs=sr, output='sos'), m)
    w = np.zeros(len(m))
    for ln in voices():
        a, b = int((ln['start'] - t0 - 0.12) * sr), int((ln['end'] - t0 + 0.15) * sr)
        w[max(0, a):max(0, b)] = 1.0
    k = int(0.12 * sr)                                       # 0.12 s in and out
    w = np.convolve(w, np.ones(k) / k, 'same')
    m = m * (1 - w) + low * DUCK[0] * w
    i = int(t0 * sr)
    mix[i:i + len(m)] += m[:max(0, len(mix) - i)]
    import flying_whales_sound as FW
    filmkit.place(mix, FW.clip('explosion-minor', -20.0), at=at('t4', T4_HIT), sr=sr)
    filmkit.place(mix, FW.clip('explosion-major', -17.0), at=at('t4', T4_FIRE), sr=sr)


def soundtrack(stems=False):
    """The siren (the brief names it, on the T2 blue wash), the intensity dings (Sam O1, O9), Germany's sounds (G19:
    Sam asked for them) and T3's sound (F24)."""
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
    import filmkit
    t3_sound(mix, MA.SR, MA.load)                           # F24: France (Sam's Paris recording + banked effects)
    dg = sfx('ding', 0.0, 1.6, peak=0.3, fade=0.4)         # O9 (Sam 16 Nov): Sam's ding (it replaces the made one)
    for tr in TIERS:
        filmkit.place(mix, dg, at=at(tr, INTENSITY_AT) - 0.06, sr=MA.SR)
    # G19 (Sam 16 Nov): Germany's sounds. The crowd from 15 s into its file (voices from there), under the whole scene
    t0, t1 = at('t2', 0.0), at('t2', T2_END)
    cr = sfx('protest-crowd', 15.0, 15.0 + (t1 - t0), peak=0.35, fade=0.25)
    nf = int(0.25 * MA.SR)
    cr[:nf] *= np.linspace(0, 1, nf)
    filmkit.place(mix, cr, at=t0, sr=MA.SR)
    wood = sfx('wood-smash', 0.0, 0.9, peak=0.55, fade=0.3)
    for th, *_ in SIGN_HITS:                                # every sign hit on the glass
        filmkit.place(mix, wood, at=at('t2', th) - 0.04, sr=MA.SR)
    filmkit.place(mix, sfx('glass-smash', 0.0, 1.4, peak=0.75, fade=0.3), at=at('t2', T2_SHATTER) - 0.02, sr=MA.SR)
    stones = [sfx('stone-hit', a, a + 0.45, peak=0.42, fade=0.15) for a in (0.0, 1.0, 2.0)]   # the file's three hits
    for q, th in enumerate([q[0] for q in T2_STONES] + [q[0] for q in UP_STONES]):
        filmkit.place(mix, stones[q % 3], at=at('t2', th) - 0.035, sr=MA.SR)
    filmkit.place(mix, sfx('glass-smash', 0.0, 1.0, peak=0.4, fade=0.3), at=at('t2', UP_STONES[-1][0]) - 0.02,
                  sr=MA.SR)                                 # G15: the upstairs window goes
    t4_sound(mix, MA.SR)                                    # A14 (music) and A15 (the crash's explosions)
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
           ('T1 tear-gas haze', 'smoke', _fx_at(t1_fx, 3.6)), ('T2 sign-on-glass flash', 'flash', _fx_at(t2_flash, SIGN_HITS[0][0] + 0.05)),
           ('T3 stones and gas', 'sparks', _fx_at(t3_fx, 1.6)), ('T3 gas and jet', 'smoke', _fx_at(t3_fx, 3.0)),
           ('T4 rocket trail', 'trail', _fx_at(t4_fx, MOPED0 + 0.9)),
           ('T4 helicopter hit', 'burst', _fx_at(t4_hit, MOPED0 + 1.1)),
           ('T4 first Molotov bloom', 'burst', _fx_at(molotovs, throws()[0][1] + 0.1, 0)),
           ("T4 granny's Molotov", 'burst', _fx_at(molotovs, GRANNY_HIT + 0.1, len(throws()) - 1)),
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
           + [(p, at('t3', SWEEP[0]), at('t3', 8.0)) for p in ('front*',)]   # T3 run-out: each from when the jet reaches him (F23, chat 7)
           # round 3 (A4): the selfie's turn and cheer; the crowds' sprites step their moves in sixths (punches,
           # machetes, throws, dances, bursts): hands and arms jump a step a frame by design
           + [(f'{w}.{part}{sd}', at('t4', 0.0), at('t4', T4_LEN)) for w in
              ('mr*', 'mp*', 'gun*', 'mid*', 'mol*', 'dan*', 'cov*', 'carrier*', 'granny*', 'selfie*')
              for part in ('hand', 'forearm', 'arm', 'thigh', 'shin', 'foot') for sd in 'LR']
           # chat 29: round 1's new runners, the same sprint (legs only: thighs, shins, feet at 2-2.8x the body's
           # speed; their turns and arms were snaps and are fixed, so arms and bodies are still checked)
           + [(f'{w}{k}.{part}{sd}', t0, t1) for w, ks, t0, t1 in (
               ('back', (1, 2, 3), at('t3', 2.75 + J3), at('t3', 8.0)),
               )
              for k in ks for part in ('thigh', 'shin', 'foot') for sd in 'LR']
           # the stone throws: a throwing hand really reaches ~20 m/s (clipcheck caps it at 12, the forearm at 10)
           + [(f'{w}{k}.{part}{sd}', t0, t1) for w, ks, t0, t1 in (
               ('runner', range(1, 6), at('t2', 0.6), at('t2', T2_FREEZE + 0.05)),
               ('hauler', (1, 2), at('t2', 1.2), at('t2', T2_FREEZE + 0.05)),
               ('front', range(1, 5), at('t3', 0.0), at('t3', SWEEP[1] + 0.2)),   # F12/F23 (chat 7): throws from frame 0 till the jet
               )
              for k in ks for part in ('hand', 'forearm') for sd in 'LR'])
# round 1 (chat 26, notes "## Exceptions"): who comes on in mid-frame for a reason the audit cannot see
# G14: they go out of sight round the corner inside, behind the wall (drawn clipped to the doorway; the audit sees
# the spot, not the clip): gone at tin + 0.9, back at tout - 0.4
ALLOWED_POPS = [(n, at('t2', tin + 0.8), at('t2', tin + 0.95), 'round the corner inside the shop, behind the wall (G14)')
                for n, (tin, tout, *_) in DOOR_IN.items()] + [
                (n, at('t2', tout - 0.45), at('t2', tout - 0.3), 'back from behind the wall inside the shop (G14)')
                for n, (tin, tout, *_) in DOOR_IN.items()] + [
                ('back*', at('t3', VOLLEY2 - 0.35), at('t3', VOLLEY2), 'step up out of the packed crowd behind'),
                ('surfer', at('t4', SURF[0]), at('t4', SURF[0] + 0.15), 'hoisted up out of the middle crowd (A7)'),
                ('carrier*', at('t4', SURF[0]), at('t4', SURF[0] + 0.15), 'step up out of the middle crowd under the shield (A7)')]
# chat 29: these were TOUCHES (a hand meant to be ON a thing, checked every frame); they are crowd crushes the
# audit should allow, not hand contacts, so the touch check found 5-900 cm gaps: allowed contacts, depth-capped
ALLOWED_CONTACTS = [('swinger', 'GLASS', at('t2', T2_HIT - 0.1), at('t2', T2_SHATTER + 0.1), 'G3/G13: the sign hits the glass four times', 0.30),
           ('hauler1', 'DOOR', at('t2', T2_DOOR - 0.1), at('t2', T2_DOOR), 'G4: the kick on the door', 0.25),
           ('hauler*', 'runner*', at('t2', 0), at('t2', .85), 'T2 run-in: the raiders crush through one gap in the glass', 0.18),
           ('hauler*', 'hauler*', at('t2', 0), at('t2', .85), 'T2 run-in: the haulers drop the shutter and pile in', 0.12),
           ('runner*', 'runner*', at('t2', 0), at('t2', T2_FREEZE + .75), 'T2 run-in: the raiders crush through one gap; packed inside', 0.18),
           ('runner*', 'swinger', at('t2', 0), at('t2', .85), 'T2 run-in: the swinger is in the crush', 0.10),
           ('front*', 'front*', at('t3', SWEEP[0]), at('t3', SWEEP[1] + 0.6), 'T3 run-out: the front line breaks and runs left as a pack', 0.04),
           ('mp*', 'mr*', at('t4', 0), at('t4', T4_LEN), 'A4 melee: fists, machetes and batons meet on the line', 0.25),
           ('mp*', 'mp*', at('t4', 0), at('t4', T4_LEN), 'A4 melee: the police ranks packed behind their shields', 0.08),
           ('mr*', 'mr*', at('t4', 0), at('t4', T4_LEN), 'A4 melee: the rioters packed behind the front rank', 0.08),
           ('carrier*', 'surfer', at('t4', SURF[0]), at('t4', T4_LEN), 'A7: the carriers hold the surf shield up', 0.2),
           ('carrier*', 'carrier*', at('t4', SURF[0]), at('t4', T4_LEN), 'A7: the carriers shoulder to shoulder under it', 0.08)]
ORDER_SWAPS = [(a, b, t0, t1, w) for a, b, t0, t1, w in (
    ('hauler*', 'runner*', at('t2', 0), at('t2', .85), 'T2 run-in: they cross in the crush'),
    ('hauler*', 'hauler*', at('t2', 0), at('t2', .85), 'T2 run-in'), ('runner*', 'runner*', at('t2', 0), at('t2', .85), 'T2 run-in'),
    ('runner*', 'swinger', at('t2', 0), at('t2', .85), 'T2 run-in'), ('hauler*', 'swinger', at('t2', 0), at('t2', .85), 'T2 run-in'),
    # Germany chat 6b (G17/G21): the gun runners and the looters sprint off in their own lanes, passing in front of/behind each other
    ('runner*', 'swinger', at('t2', 3.9), at('t2', 8.5), 'G21: gun runners pass the swinger in separate lanes'),
    ('runner*', 'runner*', at('t2', 3.9), at('t2', 8.5), 'G17/G21: runners and looters flee in separate lanes'),
    ('hauler*', 'runner*', at('t2', 3.9), at('t2', 8.5), 'G17: looters out the door pass the runners'),
    ('hauler*', 'swinger', at('t2', 3.9), at('t2', 8.5), 'G17: looters out the door pass the swinger'),
    ('front*', 'front*', at('t3', SWEEP[0]), at('t3', SWEEP[1] + 0.6), 'T3 run-out'),
    ('crs*', 'front*', at('t3', SWEEP[0]), at('t3', SWEEP[1] + 0.6), 'T3 run-out'),
    ('mp*', 'mr*', at('t4', 0), at('t4', T4_LEN), 'A4 melee: the contact line wanders'),
    ('carrier*', 'mid*', at('t4', SURF[0]), at('t4', T4_LEN), 'A7: the surf carried through the middle crowd'),
    ('carrier*', 'gun*', at('t4', SURF[0]), at('t4', T4_LEN), 'A7: the surf carried through the middle crowd'))]
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
