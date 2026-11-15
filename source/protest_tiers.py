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
LENS = (('t1', 4.0), ('t2', 6.0), ('t3', 8.0), ('t4', 10.0), ('ea', 2.4), ('eb', 2.8), ('ec', 2.4))
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
HOOK = ('European protests, ranked', {'y': 1300, 'until': 3.6})          # notes: Re-staged, T1 (over the near backs)
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
SHOT_CAST = {'t1': ['hooded*'], 't2': ['hauler*', 'swinger', 'runner*', 'crowd*'], 't3': ['front*', 'crs*'],
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
        return C.rioter()
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
        dx += 1.2 * ease((t - 0.8) / 1.2) + 0.9 * ease((t - 2.0) / 1.0)   # the surge into the shields, then through
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
        return make_person(self.kind, self.i, self.tier, self.force)

    def pose(self, sp):
        j = make_pose(sp, self.state, self.u, self.t, self.force)
        if self.mix:
            st, u, t, w = self.mix
            j = moves.mix_poses(make_pose(sp, st, u, t, self.force), j, ease(w))
            _resolve_mixed_arms(j)
        if self.extra:
            self.extra(j)
        return j


def _resolve_mixed_arms(j):
    """Chat 31 (Sam's note 1 on animatic 2, 'frames missing'): mixing two poses slides each joint straight across, so
    part-way from a run into a throw the arm came out the wrong length or folded back across the body (the guard
    stopped the drawing at T4 20.75 s). An arm the mix spoiled is re-bent onto its mixed hand."""
    for s in 'LR':
        sh, el, wr = (np.array(j[k + s][:3], float) for k in ('sh', 'el', 'wr'))
        up, fo = np.linalg.norm(el - sh), np.linalg.norm(wr - el)
        a, b = sh - el, wr - el
        ang = math.degrees(math.acos(max(-1.0, min(1.0, float(a @ b) / ((up * fo) or 1)))))
        across = (1 if sh[0] >= 0 else -1) * (el[0] - sh[0]) < -0.3 * C.F.UPPER
        if abs(up / (C.F.UPPER * .98) - 1) > .05 or abs(fo / (C.F.FORE * .98) - 1) > .05 or ang < 40 or across:
            hand = C._clear_of_shoulder(j, s, wr)
            C.V.arm_to(j, s, hand, 'down' if hand[1] > 60 else 'out', shape=j.get('hand', {}).get(s, 'fist'))


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
    # the police line across the far end (front on), one pace forward at 3.0
    step = ease((lt - 3.0) / 0.4)
    for k, x in enumerate(np.arange(-10.0, 14.0, 1.7)):
        d = T1_LINE_D - 6.0 * step                        # chat 15: one long pace (6 m) so the step reads
        gx, gy = cam.p(x, d)
        bob = 9 * math.sin(math.pi * min(1, max(0, (lt - 3.0) / 0.4)))
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
            if lt < 0.2 + (T1_FRONT - m['d']) / (T1_FRONT - 46) * 1.1:
                state = 'stand'
        elif state == 'placard':
            state = 'placard:' + T1_PLACARDS[m['i'] % len(T1_PLACARDS)]
        yaw = 180
        if lt > 1.55 + m['turn']:                          # heads turn to the bursts over the line (centre)
            yaw = 135 if gx < 470 else -135
        jig = -1 if (m['state'] == 'keys' and state == 'keys' and (int(lt * 12) + m['i']) % 2) else 0
        sc = scale_at(cam, d)
        paste(img, 'marcher', m['i'], 't1', state, yaw, gx, gy + jig, sc)
        if state == 'keys' and (int(lt * 12) + int(m['ph'] * 7)) % 3 == 0:     # chat 16 (hunt 2: no keys at phone size): every 3rd frame, bigger
            q = max(4, int(round(sc / S_REF * 400)))
            tx, ty = _top('marcher', m['i'], 't1', state, yaw, None, q)
            glint(img, gx + tx, gy + jig + ty + 2, max(5.0, 40 * sc))


def t1_actors(lt):
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
    # the firework string flying from the flicker's hand to over the line (0.85-1.55): a fizzing head and a spark tail
    if 0.85 <= lt < 1.55:
        u = (lt - 0.85) / 0.7
        x0, y0 = cam.p(-0.4, 122.5, 1.7)
        x1, y1 = cam.p(-1.6, T1_LINE_D + 1, 5.0)
        pt = lambda uu: (lerp(x0, x1, uu), lerp(y0, y1, uu) - 120 * math.sin(math.pi * uu))   # noqa: E731
        dr = ImageDraw.Draw(img)
        tail = [pt(max(0.0, u - k * 0.03)) for k in range(16)]   # chat 16 (hunt 2: no flick read): a long hot tail
        for k in range(len(tail) - 1):
            dr.line([tail[k], tail[k + 1]], fill=(255, max(60, 230 - 11 * k), max(40, 150 - 9 * k)), width=max(2, 9 - k // 2))
        hx, hy = tail[0]
        S.glow_disc(img, hx, hy, 60, (255, 200, 110), amt=.8)
        IS.ell(img, hx, hy, 9, 9, (255, 255, 235), None)
        rng = np.random.default_rng(int(lt * 100))
        for _ in range(8):                                   # sparks shed behind it
            sx, sy = hx + rng.uniform(-22, 22), hy + rng.uniform(-10, 26)
            IS.ell(img, sx, sy, 2, 2, (255, 240, 180), None)
    # three bursts over the line (chat 15: bigger, brighter, one at a time, each with a flash and falling sparks)
    # chat 16 (hunt 2: one big red wheel, brief: three SMALL bursts): smaller, staggered 0.15 s so the three show at once
    for k, (t0, x, z, col) in enumerate(((1.55, -3.4, 6.2, (255, 90, 70)), (1.72, 0.6, 7.4, (255, 250, 210)),
                                         (1.89, 4.4, 5.6, (110, 255, 150)))):
        a = lt - t0
        if 0 <= a < 0.6:
            cx, cy = cam.p(x, T1_LINE_D + 1, z)
            r = 18 + 62 * ease(a / 0.3)
            fade = 1 - a / 0.6
            S.glow_disc(img, cx, cy, r * 1.6, col, amt=.6 * fade)
            if a < 0.07:                                      # the flash
                S.glow_disc(img, cx, cy, 60, (255, 255, 255), amt=.8)
                IS.ell(img, cx, cy, 12, 12, (255, 255, 255), None)
            dr = ImageDraw.Draw(img)
            for n in range(16):
                ang = n * math.pi / 8 + k * 0.3
                r0, r1 = r * 0.4, r
                droop = 40 * a * a / 0.36
                ex, ey = cx + r1 * math.cos(ang), cy + r1 * math.sin(ang) + droop
                dr.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang) + droop * .5), (ex, ey)],
                        fill=col, width=4)
                IS.ell(img, ex, ey, 4, 4, (255, 255, 240), None)
    # the tear-gas haze drifting left to right through the keys (3.0-4.0)
    if lt > 2.9:
        haze(img, lt - 2.9, [(cam.p(x, d, 1.6), 9 * cam.ppm(d)) for x, d in
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
T2_WIN = (174, 754, 786, 1089)
T2_WASH, T2_FREEZE = 5.0, 5.2       # round 1 (T2 6 s): the blue wash and the freeze, 2 s later (was 3.0, 3.2)


def t2_state(lt):
    shutter = 0.5 + 0.5 * ease((lt - 0.45) / 0.55)
    glass = 'whole' if lt < 1.0 else 'starred' if lt < 1.1 else 'gone'
    return dict(shutter=shutter, glass=glass)


def t2_actors(lt):
    tt = min(lt, T2_FREEZE)                                 # everyone freezes mid-swing in the blue (round 1: 5.2)
    out = []

    LANES = (10.4, 10.8, 11.2, 11.6, 12.0, 13.0, 13.4)      # chat 14: each runner its own depth lane on the way in
    SPRINT = 6.2                                            # (same lane: they ran through each other)

    def dash(n, x0, x1, de, t1):
        """chat 18 (pre-flight: 9-14 m/s, they ran 4-6 m in half a second): the run's length is set by a real sprint
        (SPRINT m/s at its fastest), arriving at t1 as before; x even, the depth lane eased smoothly to the mark.
        -> (x, d, running). t0 may be before the cut: they are already running when the tier opens."""
        dl = LANES[n] if n is not None else de
        T = math.hypot(x1 - x0, 1.5 * (de - dl)) / SPRINT
        u = (tt - (t1 - T)) / T
        v = min(1.0, max(0.0, u))
        return lerp(x0, x1, v), lerp(dl, de, ease(v)), u < 1.0

    def run_in(x0, x1, t0, t1):
        x, _, running = dash(None, x0, x1, 0.0, t1)
        return x, running

    # haulers (0.4-1.0), then they slide through the gap into the shop (1.3-1.7)
    for k, (xe, de) in enumerate(((-0.9, 13.3), (0.6, 13.3))):
        x, d, running = dash(k, -3.3 - k * 0.5, xe, de, 0.45)
        if tt >= WAVE['hauler1'][1]:                      # round 1: back out with the mannequin (second_wave)
            continue
        if running:
            out.append(Actor(f'hauler{k + 1}', 'rioter', x, d, 90, 'run', t=tt, tier='t2'))
        elif tt < 1.3:
            out.append(Actor(f'hauler{k + 1}', 'rioter', x, de, 180, 'haul', tier='t2'))
        else:
            u = ease((tt - 1.3) / 0.4)
            out.append(Actor(f'hauler{k + 1}', 'rioter', xe - 0.1 * k * u, de + (1.85 - 0.2 * k) * u, 180,
                             'throw' if u >= 1 else 'stand', u=_hauler_u(k, tt), tier='t2',
                             clip=T2_WR if u > 0.5 else None))
    # the road-sign swinger: runs in carrying it low, winds up 0.6, swings through the glass at 1.0, keeps swinging
    x, running = run_in(-3.3, -0.5, 0.05, 0.6)            # chat 15: mid-window (was -1.55: the sign at the frame edge)
    if running:
        out.append(Actor('swinger', 'rioter', x, 12.0, 90, 'run_sign', t=tt, tier='t2'))
    else:
        if tt < 0.9:
            u = 0.2 * ease((tt - 0.6) / 0.3)
        elif tt < 1.05:
            u = 0.2 + 0.8 * ease((tt - 0.9) / 0.15)
        else:
            c = ((tt - 1.05) % 0.7) / 0.7
            u = 1 - 0.8 * math.sin(math.pi * c) if tt < T2_WASH else 0.55
        out.append(Actor('swinger', 'rioter', x, 12.0, 90, 'swing', u=u, tier='t2'))
    # five more: two throw stones into the shop, one kicks the A-board over (1.4), two by the closed shop
    for k, (xe, de) in enumerate(((0.9, 12.4), (1.55, 11.9), (-2.15, 12.3), (2.25, 12.5), (2.9, 12.0))):
        x, d, running = dash(k + 2, -3.3 - k * .3, xe, de, 0.6 + k * .05)
        if running:
            out.append(Actor(f'runner{k + 1}', 'rioter', x, d, 90, 'run', t=tt + k * .1, tier='t2'))
        else:
            u = ((tt - 0.6) * 1.4 + k * .3) % 1.0
            yaw = 180 if k < 2 else 90 if k == 2 else 135
            out.append(Actor(f'runner{k + 1}', 'rioter', x, de, yaw, 'throw', u=u if lt < T2_FREEZE else 0.3, tier='t2'))
    # the crowd on the near pavement, seen from behind, all facing the store (chanting: signs jab on the beat)
    beat = abs(math.sin(math.pi * 2.2 * tt))
    # chat 15 (moves hunt 1: the near crowd at 3.3-5.8 m hid the smash and lost its feet): back to 7-8.6 m, at the
    # two sides only, so the window and the swing stay clear in the middle; whole people, feet on the road
    # chat 16 (hunt 2: the near crowd still covered the window): to the frame's two edges (the window spans x 100-860)
    crowd = [(-1.38, 7.8, 'placard:WAFFEN RAUS:250,246,232', 0), (-1.75, 8.9, 'phone', 1), (-1.6, 9.6, 'stand', 2),
             (1.42, 7.7, 'phone', 6), (1.7, 8.8, 'placard:GEN Z REGELT:240,220,60', 5), (1.95, 9.5, 'stand', 3)]
    for k, (x, d, st, i) in enumerate(crowd):
        if st.startswith('placard'):
            st = st + ':' + str(int(90 * beat))
        yaw = 180
        if st == 'phone':                                   # round 1: the phones swing round after the looters
            yaw = 180 - (30 if x < 0 else 45) * ease((tt - 3.1) / 0.5)
        out.append(Actor(f'crowd{k + 1}', 'marcher', x + 0.04 * math.sin(tt * 3 + k), d, yaw, st, i=i, tier='t2'))
    return out + second_wave(tt)


# Round 1 (T2 3.0-5.2, notes "## Round 1 plan"): the second wave comes back out through the gap and jogs off right
# with the stock: name -> (x where they step out, out at, lane d, jog m/s, pose, prop). The haulers carry the
# mannequin between them, 1.4 m apart, so it stays rigid; frozen mid-frame at 5.2.
WAVE = {'runner6': (-0.2, 3.0, 12.95, 1.2, 'carry_front', 'tv'),       # chat 29 (pre-flight: feet 8-10 m/s, 74 cm a
        'runner7': (0.1, 3.15, 13.3, 1.8, 'carry_front', 'boxes'),   # frame): a laden brisk walk, not a run; each
        'hauler2': (0.5, 3.95, 13.55, 1.3, 'carry_up', None),         # its own lane (same lane: they swapped front and
        'hauler1': (-0.9, 3.95, 13.75, 1.3, 'carry_up', 'mannequin')} # back in one frame), hauler2 in front
WAVE_IN = 14.8                                              # the shop floor they come out from
WAVE_OUT, WAVE_TURN = 0.9, 0.3                              # chat 29: step out over 0.9 s (was 0.45: 8 m/s), turn in 0.3


def wave_pos(name, tt):
    """-> (x, d, yaw, inside) or None before they come out."""
    x0, t0, lane, v, _, _ = WAVE[name]
    if tt < t0:
        return None
    u = (tt - t0) / WAVE_OUT
    if u < 1:                                               # stepping out toward us through the gap
        d0 = WAVE_IN + (lane - 13.4) * name.startswith('hauler')   # from where each hauler stood (no swap)
        d = lerp(d0, lane, ease(u))
        return x0, d, 0, d > 13.9
    a = tt - t0 - WAVE_OUT
    k = min(1.0, a / WAVE_TURN)                             # turning right, then walking off (no snap of 115 degrees)
    x = x0 + v * (a - WAVE_TURN / 2) if k >= 1 else x0 + v * WAVE_TURN / 2 * k * k
    return x, lane, 115 * ease(k), False                    # three-quarter away: the run's safe yaw


def _carried(kind):
    def draw(img, cam, a):
        k = cam.ppm(a.d)
        fwd = 0.28 if a.yaw > 90 else 0.0                   # out in front of them, toward where they go
        dd = 0.15 if a.yaw > 90 else -0.3
        if kind == 'tv':
            S.prop_tv(img, *cam.p(a.x + fwd, a.d + dd, 1.2), k, -6, lit=True)
        elif kind == 'boxes':
            S.prop_boxes(img, *cam.p(a.x + fwd * .7, a.d + dd, 0.95), k, 3)
        else:                                               # the mannequin, flat over both carriers' heads
            xf = wave_pos('hauler2', a.t)
            if xf:
                S.prop_mannequin(img, *cam.p((a.x + xf[0]) / 2, a.d, 2.12), k, 0)
    return draw


def _hauler_u(k, tt):
    """The haulers' stone throws inside the shop; they stop mid-throw at 3.3 to pick up the mannequin (chat 29)."""
    return (min(tt, 3.3) * 1.7 + k * .5) % 1


def second_wave(tt):
    out = []
    for name, (_, t0, _, _, st, prop) in WAVE.items():
        w = wave_pos(name, tt)
        if w is None:
            continue
        x, d, yaw, inside = w
        if name.startswith('hauler'):                       # chat 29: they turn round and lift it (was a snap of
            k = (tt - t0) / 0.4                             # 180 degrees and throw -> carry in one frame)
            yaw = yaw if k >= 1 else 180 * (1 - ease(k))
        a = Actor(name, 'rioter', x, d, yaw, st, t=tt, tier='t2', clip=T2_WR if inside else None)
        if name.startswith('hauler'):
            a.blend('throw', _hauler_u(int(name[-1]) - 1, tt), w=(tt - t0) / 0.4)
        if prop:
            a.prop, a.prop_before = _carried(prop), yaw > 90 and prop != 'mannequin'
        out.append(a)
    return out


def t2_fx(img, lt):
    cam = RF2.cam
    tt = min(lt, T2_FREEZE)
    # the A-board by the doorway, kicked over at 1.4
    bx, by = cam.p(-1.6, 12.8)                             # chat 15: in frame after the T2 reframe (was -3.4)
    k = cam.ppm(12.6)
    ang = math.radians(85 * ease((tt - 1.4) / 0.25))
    hgt, wd = 1.15 * k, 0.72 * k                           # chat 14: a pavement A-board's true size (was small)
    pts = [(-wd / 2, 0), (wd / 2, 0), (wd / 2 - 8, -hgt), (-wd / 2 + 8, -hgt)]
    rot = lambda q: [(bx + px * math.cos(ang) - py * math.sin(ang), by + px * math.sin(ang) + py * math.cos(ang))  # noqa
                     for px, py in q]
    IS.poly(img, rot(pts), (60, 52, 44), INK, 2.4)              # the wooden frame, a chalkboard face
    IS.poly(img, rot([(-wd / 2 + 12, -10), (wd / 2 - 12, -10), (wd / 2 - 18, -hgt + 12), (-wd / 2 + 18, -hgt + 12)]),
            (34, 38, 36), None, 0)
    for f in (0.3, 0.45, 0.6, 0.72):                        # chalk lines (prices)
        IS.poly(img, rot([(-wd * .3, -hgt * f), (wd * (.3 - .25 * (f > .5)), -hgt * f)]), None, (220, 222, 214), 3, 0)
    # the pry bar (0.45-1.3): hauler 1 levers the shutter's hem up from beside his head; the hem rides up with it
    if 0.45 <= tt < 1.3:
        st = t2_state(tt)
        hem = .45 + (2.9 - .45) * st['shutter']
        hx = -0.9 + 0.12
        a, b = cam.p(hx, 13.3, 1.9), cam.p(hx + 0.35, 13.95, hem + 0.02)
        IS.poly(img, [a, b], None, INK, 16, 0)                 # chat 16 (hunt 2: no crowbar read): twice as thick
        IS.poly(img, [a, b], None, (220, 40, 36), 10, 0)       # a red-painted crowbar
        IS.poly(img, [b, (b[0] + 18, b[1] - 14)], None, INK, 12, 0)
        IS.poly(img, [b, (b[0] + 18, b[1] - 14)], None, (220, 40, 36), 6, 0)
    t2_flash(img, tt)


def t2_flash(img, tt):
    """The impact flash where the sign meets the glass (1.0); its own function so the shape check draws it alone."""
    if 0.98 <= tt < 1.15:
        S.glow_disc(img, *RF2.R(500, 905), 130, (255, 250, 210), amt=.7)


def t2_teeth(img, lt):
    """Drawn before the people (in front of the window they hide it)."""
    tt = min(lt, T2_FREEZE)
    if tt >= 1.1:                                          # chat 16 (hunt 2: glass looked whole): jagged teeth left
        x0, y0, x1, y1 = T2_WR                             # in the frame, a star of cracks round the hole
        rng = np.random.default_rng(9)
        for side in range(4):
            n = 9
            for q in range(n):
                u0, u1 = q / n, (q + 1) / n
                dep = rng.uniform(25, 95)
                um = (u0 + u1) / 2 + rng.uniform(-.03, .03)
                if side == 0:
                    tri = [(lerp(x0, x1, u0), y0), (lerp(x0, x1, u1), y0), (lerp(x0, x1, um), y0 + dep)]
                elif side == 1:
                    tri = [(lerp(x0, x1, u0), y1), (lerp(x0, x1, u1), y1), (lerp(x0, x1, um), y1 - dep * .7)]
                elif side == 2:
                    tri = [(x0, lerp(y0, y1, u0)), (x0, lerp(y0, y1, u1)), (x0 + dep, lerp(y0, y1, um))]
                else:
                    tri = [(x1, lerp(y0, y1, u0)), (x1, lerp(y0, y1, u1)), (x1 - dep, lerp(y0, y1, um))]
                IS.poly(img, tri, (200, 226, 236), (90, 120, 130), 2, 0)

    # chat 16: the falling glass falls in the window's plane, behind the raiders
    # falling glass with glints (1.05-1.6), then shards on the pavement glinting
    rng = np.random.default_rng(5)
    for n in range(60):
        x0, y0 = rng.uniform(T2_WR[0] + 10, T2_WR[2] - 10), rng.uniform(T2_WR[1] + 10, T2_WR[3] - 20)
        a = tt - 1.05 - rng.uniform(0, .15)
        if a < 0:
            continue
        yy = min(RF2.R(0, 1175)[1] + rng.uniform(-20, 15), y0 + 1100 * a * a)
        xx = x0 + rng.uniform(-60, 60) * min(a, .4)
        r = rng.uniform(10, 24)
        sp = rng.uniform(0, 6.28) + a * 9
        tri = [(xx + r * math.cos(sp + q * 2.1), yy + r * .7 * math.sin(sp + q * 2.1)) for q in range(3)]
        IS.poly(img, tri, (210, 230, 238), (120, 150, 160), 1.2, 0)
        if (n + int(lt * 12)) % 7 == 0:
            S.glow_disc(img, xx, yy, 9, (255, 255, 255), amt=.7)


def blue_wash(img, lt):
    """T2 5.0-6.0 (round 1; was 3.0-4.0): the blue light from the far right end of the street sweeping across crowd and store; faces,
    signs and the wet ground turn blue (the last light layer, over everything)."""
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
    for a in actors:
        if a.state == 'phone':
            gx, gy = cam.p(a.x + 0.12, a.d, 1.62)
            S.glow_disc(img, gx, gy, 0.09 * cam.ppm(a.d), (235, 245, 255), amt=.55)   # chat 15: was 0.25 (a grey disc)


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
RF3 = Reframe(S.CAMS['t3'], 1.2, 540, 68.0)
RF4 = Reframe(S.CAMS['t4'], 1.15, 0, 80.0)   # chat 15: about x 0 (was 250), so BANKA and the mopeds stay in frame
T3K, T3CAM, R3, reframe3 = RF3.k, RF3.cam, RF3.R, RF3.image
T4CAM, R4 = RF4.cam, RF4.R
# chat 15 (moves hunt 1: the runners and the swing too small, the near crowd hid them): T2 nearer too; the near crowd
# moved back to the two sides, so the bottom of the frame is them, not bare road
RF2 = Reframe(S.CAMS['t2'], 1.25, 480, -5.0)
T2_WR = (*RF2.R(T2_WIN[0], T2_WIN[1]), *RF2.R(T2_WIN[2], T2_WIN[3]))


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
    for d in np.arange(13.5, 44.0, 0.9):
        for x in np.arange(-12.0, 0.6 + (d - 13) * .05, 0.7):
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
    return 1.6 * m, 3.4 * m, 12.0 * m


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


def t3_actors(lt):
    out = []
    jet = lt > 2.6 + J3
    for k, x in enumerate(np.arange(-2.0, 0.15, 0.7)):      # the black-clad front line, facing the police (right);
        # chat 14: 0.7 m apart (at 0.55 each throwing hand passed into the next one's back)
        dx, _ = field('t3', x, 11.8, lt, k)
        if jet and lt > 2.7 + J3 + 0.05 * k:                  # broken by the jet: running out left
            u = lt - 2.7 - J3 - 0.05 * k                          # chat 18: lane step eased (it snapped 0.9 m)
            if x + dx * .3 - 4.5 * u < OFF_L:                     # chat 29: gone off the left edge (they ran on
                continue                                          # through each other off screen)
            out.append(Actor(f'front{k + 1}', 'rioter', x + dx * .3 - 4.5 * u, 11.8 - (.3 * k % 1) * ease(min(1.0, u / .35)), -90, 'run', t=lt,
                             tier='t3'))
        elif 0.75 <= lt < 2.6 + J3:
            u = ((lt - 0.75) * 1.6 + k * 0.37) % 1.0
            out.append(Actor(f'front{k + 1}', 'rioter', x + dx * .3, 11.8, 90, 'throw', u=u, tier='t3'))
        else:
            out.append(Actor(f'front{k + 1}', 'rioter', x + dx * .3, 11.8, 90, 'stand', tier='t3'))
    # round 1 (T3 2.5-4.0): the second volley, twice the throwers: a back row steps up between the front line's gaps
    for k, x in enumerate(np.arange(-1.65, 0.4, 0.7)):
        if lt < VOLLEY2 - 0.3:
            continue
        if jet and lt > 2.75 + J3 + 0.05 * k:
            u = lt - 2.75 - J3 - 0.05 * k                   # chat 29: turns and gets going (snapped throw -> sprint,
            ut = ((2.75 + J3 + 0.05 * k - VOLLEY2) * 1.6 + k * 0.29) % 1.0   # hands 13 m/s)
            if x - _getaway(u) < OFF_L:
                continue
            out.append(Actor(f'back{k + 1}', 'rioter', x - _getaway(u), 13.0, _turn(90, -115, u / .3), 'run',
                             t=lt + .3, tier='t3').blend('throw', _volley(ut), w=u / .3))
        elif lt >= VOLLEY2:
            u = ((lt - VOLLEY2) * 1.6 + k * 0.29) % 1.0
            out.append(Actor(f'back{k + 1}', 'rioter', x, 13.0, 90, 'throw', u=_volley(u), tier='t3'))
        else:                                               # stepping up from the crowd behind
            out.append(Actor(f'back{k + 1}', 'rioter', x - 0.6 * (VOLLEY2 - lt) / 0.3, 13.0, 90, 'stand', tier='t3'))
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
    # chat 15 (hunt 1: "no two rows of riot police": they stood at the right edge, off frame): two rows in frame
    for k, (x, d) in enumerate(((1.3, 11.0), (1.9, 11.0), (2.5, 11.0), (1.6, 12.0), (2.2, 12.0), (2.8, 12.0))):
        out.append(Actor(f'crs{k + 1}', 'officer', x, d, -90, 'line', force='crs', tier='t3'))
    return out


def t3_crowd(img, lt):
    cam = T3CAM
    for m in sorted(crowd_t3(), key=lambda m: -m['d']):
        dx, dd = field('t3', m['x'], m['d'], lt, m['ph'])
        x, d = m['x'] + dx, max(12.6, m['d'] + dd)
        gx, gy = cam.p(x, d)
        if gx < -80 or gx > W + 80:
            continue
        running = lt > 2.6 + J3 and m['d'] < 30 and lt - 2.6 - J3 - 0.02 * max(0, m['x'] + 2) > 0.1
        if running:                                         # chat 16 (hunt 2: crowd not breaking): they run out left
            x -= 3.2 * (lt - 2.7 - J3 - 0.02 * max(0, m['x'] + 2))
            gx, gy = cam.p(x, d)
        yaw = -90 if running else 90
        paste(img, 'marcher', m['i'], 't3', m['state'] if not running else 'stand', yaw, gx, gy, scale_at(cam, d))


def t3_columns(img, lt):
    """Smoke climbing from the car (left) and the bike heap (mid-right) from 0.0. Chat 15: drawn before the truck and
    the people (the bikes burn at d 14, behind the police: their smoke had hidden the water cannon truck)."""
    X0, X1, D0, _ = S.CAR3
    p0, p1 = T3CAM.p(*S.car_pt(X1 - .5, D0 + 2.4, (0, 0, 0)), 2.5), T3CAM.p(*car_roof(lt), 2.5)
    cdx, cdy = p1[0] - p0[0], p1[1] - p0[1]                 # round 1: the car's smoke goes where the car goes
    for (sx, sy, sd) in ((R3(110, 860)[0] + cdx, R3(110, 860)[1] + cdy, 1), R3(760, 1010) + (2,)):
        if sd == 1 and lt > CAR_HIT + 0.3:                  # the jet put it out: steam (car_fx) instead
            continue
        lumps = []
        for n in range(6):
            a = (lt * 0.9 + n / 6) % 1.0
            lumps.append((sx + 48 * a + 18 * math.sin(n * 2.1), sy - 620 * a, 48 + 108 * a))
        S.smoke(img, lumps, (58, 54, 56), (138, 128, 124), lw=2.5)


def t3_debris(img):
    """Chat 16 (hunt 2: bare grey ground filled the lower third): the square's near ground littered, as in the
    references: thrown cobbles, leaflets, a dropped tricolour and a yellow vest."""
    cam = T3CAM
    rng = np.random.default_rng(23)
    for _ in range(22):                                    # cobbles
        x, d = rng.uniform(-3.2, 3.4), rng.uniform(4.6, 10.8)
        sx, sy = cam.p(x, d)
        k = cam.ppm(d)
        IS.ell(img, sx, sy - .06 * k, .13 * k, .08 * k, (128, 118, 106), INK, 2)
        IS.ell(img, sx - .03 * k, sy - .09 * k, .05 * k, .03 * k, (170, 160, 146), None)
    for _ in range(9):                                     # leaflets
        x, d = rng.uniform(-3.0, 3.2), rng.uniform(4.8, 10.5)
        k = cam.ppm(d)
        sx, sy = cam.p(x, d)
        w_, h_, sk = .32 * k, .1 * k, rng.uniform(-.4, .4) * k * .2
        IS.poly(img, [(sx - w_, sy), (sx + w_, sy + sk), (sx + w_ * .8, sy - h_ + sk), (sx - w_ * 1.1, sy - h_)],
                (240, 238, 228), INK, 1.6)
    # a dropped tricolour (near left) and a yellow vest (near right), lying flat
    for (x, d, cols) in ((-1.6, 6.2, ((40, 60, 150), (245, 245, 240), (200, 40, 50))),
                         (1.7, 7.4, ((236, 214, 40),) * 3)):
        k = cam.ppm(d)
        sx, sy = cam.p(x, d)
        w3 = .3 * k
        for q, col in enumerate(cols):
            x0 = sx - 1.5 * w3 + q * w3
            IS.poly(img, [(x0, sy), (x0 + w3, sy + 4), (x0 + w3 + 6, sy - .22 * k + 4), (x0 + 6, sy - .22 * k)], col,
                    INK, 2)


def t3_fx(img, lt):
    cam = T3CAM
    # stones in arcs from the front line to the shields (1.0-2.6); chat 15: bigger (a fist-sized cobble reads at
    # phone size only drawn about twice true), four in the air per thrower, a few already lying at the shields' feet
    for k in range(4):
        for rep in range(4):
            t0 = 0.75 + ((k * 0.37 + 0.6) % 1.0) / 1.6 + rep / 1.6     # chat 16 (hunt 2: none in the air at 1.2)
            a = (lt - t0) / 0.45
            if 0 <= a < 1 and t0 < 2.6 + J3:
                x0 = -2.0 + 0.7 * k
                x, z = lerp(x0 + 0.3, 1.25, a), 1.9 + 3.6 * math.sin(math.pi * a) - 0.6 * a   # up against the sky
                d = lerp(11.8, 11.0, a)
                sx, sy = cam.p(x, d, z)
                IS.ell(img, sx, sy, 26, 20, (120, 108, 96), INK, 3.5)
                IS.ell(img, sx - 7, sy - 7, 10, 7, (176, 164, 150), None)
    # round 1 (T3 2.5-4.55): the back row's volley, over the front line's heads: stones, a traffic cone, a bike wheel,
    # each one flashing off the shields where it lands
    for k in range(3):
        for rep in range(5):
            t0 = VOLLEY2 + ((k * 0.29 + 0.6) % 1.0) / 1.6 + rep / 1.6
            a = (lt - t0) / 0.5
            if t0 >= 2.6 + J3 or a < 0:
                continue
            x0 = -1.65 + 0.7 * k
            if a < 1:
                x, z = lerp(x0 + 0.3, 1.3, a), 2.1 + 4.2 * math.sin(math.pi * a) - 0.7 * a
                sx, sy = cam.p(x, lerp(13.0, 11.0, a), z)
                what = 'cone' if (k, rep) == (1, 0) else 'wheel' if (k, rep) == (2, 1) else 'stone'
                if what == 'cone':
                    S.prop_cone(img, sx, sy, 1.6 * cam.ppm(11.5), 360 * a * 1.5)
                elif what == 'wheel':
                    S.prop_wheel(img, sx, sy, 1.4 * cam.ppm(11.5), 540 * a)
                else:
                    IS.ell(img, sx, sy, 26, 20, (120, 108, 96), INK, 3.5)
                    IS.ell(img, sx - 7, sy - 7, 10, 7, (176, 164, 150), None)
            elif a < 1.3:                                   # the hit: a white-yellow flash on the shield
                sx, sy = cam.p(1.3, 11.0, 1.0 + 0.3 * k)
                S.glow_disc(img, sx, sy, 90 * (1.3 - a) / 0.3 + 30, (255, 246, 200), amt=.8)
    rng = np.random.default_rng(17)
    for n in range(int(min(9, max(0, (lt - 1.45) * 7)))):
        sx, sy = cam.p(rng.uniform(0.7, 1.2), rng.uniform(10.4, 11.2))
        IS.ell(img, sx, sy - 6, 15, 10, (150, 146, 138), INK, 2)
    # the tear-gas canister lands at 1.6 by Marianne's base, trailing white; the gas swells over her lower half
    # (chat 15: hunt 1 saw no landing and the gas over the crowd: it lands nearer her base, set y 870, with a puff)
    if 1.2 <= lt < 1.6:
        a = (lt - 1.2) / 0.4
        pos = lambda u: R3(lerp(1100, 470, u), lerp(760, 870, u) - 220 * math.sin(math.pi * u))   # noqa: E731
        trail = [pos(max(0.0, a - q * 0.06)) + (10 + 7 * q,) for q in range(1, 6)]
        S.smoke(img, trail, (226, 228, 226), (250, 250, 248), line=(170, 176, 180), lw=2, fade=False)
        sx, sy = pos(a)
        IS.ell(img, sx, sy, 20, 11, (86, 94, 86), INK, 2.5)
        IS.ell(img, sx - 14, sy, 5, 9, (200, 60, 40), None)
    if lt >= 1.6:
        g = ease((lt - 1.6) / 0.6)                          # chat 16 (hunt 2: gas tiny): swells in 0.6 s, 1.35x
        bx, by = R3(470, 870)
        if lt < 1.75:                                       # the landing: a quick white burst ring
            S.glow_disc(img, bx, by, 110 * (lt - 1.55) / 0.2, (255, 255, 255), amt=.7)
        lumps = [(bx + 1.35 * T3K * dx * g, by - 1.35 * T3K * dy * g, 1.35 * T3K * (36 + r * g)) for dx, dy, r in
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
        ix, iy = cam.p(lerp(1.4, -2.0, sweep) - 1.5 * ease((lt - 5.5) / 1.0), 11.6, 1.3)
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
    for d in np.arange(18.5, 48.0, 0.9):
        for x in np.arange(-14.0, 0.8, 0.7):
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
HOLD = 8.0                                         # the gleeful hold: jumping, fireworks
# where each Molotov lands (screen, after the reframe): the bank's ground-floor windows, then (granny) its first floor
LAND = [R4(70, 845), R4(160, 870), R4(235, 860)]
G_LAND = R4(140, 640)


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
    return out


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
    if lt >= HOLD - 0.2:
        for k, (t0, x, y, col) in enumerate(FIREWORKS):
            for rep_ in range(3):                            # each one bursts again every 0.75 s through the hold
                burst(img, x + 40 * rep_, y + 30 * (rep_ % 2), lt - t0 - 0.75 * rep_, col, k + rep_)


FIREWORKS = ((HOLD - 0.2, 260, 230, (255, 90, 70)), (HOLD + 0.05, 760, 150, (255, 250, 210)),   # over the
             (HOLD + 0.3, 520, 290, (110, 255, 150)), (HOLD + 0.5, 930, 300, (255, 200, 60)))    # headings


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
        shots.append((t0 + 0.27, t0 + 0.85, (hx, hy), LAND[k], 260, 1.0, k))
    hx, hy = cam.p(SLOT[0] - 0.2, SLOT[1], 1.95)
    shots.append((GRANNY_THROW, GRANNY_HIT, (hx, hy), G_LAND, 820, 1.9, 3))
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
END_BG0 = 8.0                    # the T4 moment behind shot A's first frame; it runs on through A, then C


def t4_plate(lt):
    _PLATE.append(1)
    try:
        return picture(at('t4', 0.0) + lt) if lt < 10.0 else _t4_late(lt)
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
        c = T4CAM
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
        t2_teeth(back, lt)
        for a in acts:
            if a.prop and a.prop_before:
                a.prop(back, cam, a)
            draw_actor(back, cam, a)
            if a.prop and not a.prop_before:
                a.prop(back, cam, a)
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
        for a in sorted(t4_actors(lt) + ([] if _PLATE else ['cart']),
                        key=lambda a: -(CART[1] + 0.05 if a == 'cart' else a.d)):
            if a == 'cart':
                draw_cart(ppl, lt)
            else:
                draw_actor(ppl, cam, a)
        if not _PLATE:
            t4_mopeds(ppl, lt)
        back.alpha_composite(backlight(back, lt, ppl))
        t4_fx(back, lt)
        if lt > 2.0:
            haze(back, lt - 2.0, [(R4(x, 1230), 220) for x in (100, 400, 700, 1000)], 0.3, (200, 170, 150), .1, 7)
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
    if lt >= 1.0:                                          # Sam R3: the Intensity line, red, a little smaller
        d.text((72 * k, 514 * k), f'Intensity Level: {INTENSITY[tier]}/10', font=_font(int(36 * k)), fill=INTENSITY_RED,
               stroke_width=int(4 * k), stroke_fill=(0, 0, 0))
    img.alpha_composite(lay)
    return img


def frame_image(t):
    return overlay(picture(t), t)


# Rule 75: what the Hook Text (0.5-3.6 s, y ~1300) must never cover in T1
def _box_t1(x, d, z0, z1, w):
    cam = S.CAMS['t1']
    (ax, ay), (_, by) = cam.p(x - w / 2, d, z1), cam.p(x, d, z0)
    return (ax, ay, ax + w * cam.ppm(d), by)


KEEP_CLEAR = [('the knot and the burning container', lambda t: _box_t1(0.6, 162, 0, 3.0, 8.0) if t < 4 else None),
              ('the bursts over the line', lambda t: _box_t1(1.0, 186, 4.0, 8.5, 9.0) if 1.5 < t < 3.0 else None),
              ('the police line', lambda t: _box_t1(2.0, 185, 0, 2.0, 26.0) if t < 4 else None)]


# ------------------------------------------------------------------------------------------------- sound
def soundtrack(stems=False):
    """Siren only (the brief names the siren cue, on the T2 blue wash); no other effects."""
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
               ('rioter', range(1, 9), at('t4', 0.0), at('t4', 10.0)))
              for k in ks for part in ('hand', 'forearm') for sd in 'LR'])
# round 1 (chat 26, notes "## Exceptions"): who comes on in mid-frame for a reason the audit cannot see
ALLOWED_POPS = [('runner6', at('t2', 2.95), at('t2', 3.3), 'out of the dark shop, through the gap in the glass'),
                ('runner7', at('t2', 3.15), at('t2', 3.5), 'out of the dark shop, through the gap in the glass'),
                ('back*', at('t3', VOLLEY2 - 0.35), at('t3', VOLLEY2), 'step up out of the packed crowd behind'),
                ('buyer*', at('t4', ENTER), at('t4', ENTER + 0.15), 'step out of the packed crowd into the queue'),
                ('granny', at('t4', 5.7), at('t4', 5.85), 'steps out of the packed crowd to the cart')]
# chat 29: these were TOUCHES (a hand meant to be ON a thing, checked every frame); they are crowd crushes the
# audit should allow, not hand contacts, so the touch check found 5-900 cm gaps: allowed contacts, depth-capped
ALLOWED_CONTACTS = [('hauler*', 'runner*', at('t2', 0), at('t2', .85), 'T2 run-in: the raiders crush through one gap in the glass', 0.18),
           ('hauler*', 'hauler*', at('t2', 0), at('t2', .85), 'T2 run-in: the haulers drop the shutter and pile in', 0.12),
           ('runner*', 'runner*', at('t2', 0), at('t2', T2_FREEZE + .75), 'T2 run-in: the raiders crush through one gap; packed inside', 0.18),
           ('runner*', 'swinger', at('t2', 0), at('t2', .85), 'T2 run-in: the swinger is in the crush', 0.10),
           ('front*', 'front*', at('t3', 2.7 + J3), at('t3', 3.3 + J3), 'T3 run-out: the front line breaks and runs left as a pack', 0.04),
           ('policia*', 'rioter*', at('t4', 0), at('t4', 9.95), 'T4 melee: rioters slam into the shields (brief 26)', 0.20),
           ('policia*', 'policia*', at('t4', 2), at('t4', 9.95), 'T4 melee: the shield line buckles back into itself', 0.06)]
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
