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
    return None                        # voices only, none yet (Sam records them): no captions


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
    if kind == 'officer':
        return C.officer(force)
    if kind == 'rioter':
        return C.rioter()
    return C.marcher(i, tier)


def make_pose(sp, state, u=0.0, t=0.0, force=None):
    """The cast's pose by name, plus the film's own: 'stand', 'placard:TEXT:R,G,B[:lift]', 'flag:KIND', 'keys'."""
    if state == 'stand':
        return V.standing(sp)
    if state == 'throw' and 0.42 < u < 0.57:          # the rig folds the elbow too tight mid-throw: pass through it
        u = 0.42 if u < 0.495 else 0.57
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
    if state == 'swing' and 0.285 < u < 0.45:           # the same elbow fold mid-swing (chat 14): pass through it
        u = 0.285 if u < 0.37 else 0.45
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
                 dark=0.0, tier='t1'):
        if state.startswith('run') and 75 <= abs(yaw) <= 105:   # chat 14: the rig's run fails its arm guard side on
            yaw = 115 if yaw > 0 else -115                     # (14-17 of 24 phases, either way): three-quarter, away
        self.name, self.kind, self.x, self.d, self.yaw = name, kind, x, d, yaw
        self.state, self.u, self.t, self.i, self.force = state, u, t, i, force
        self.extra, self.clip, self.dark, self.tier = extra, clip, dark, tier

    def sp(self):
        return make_person(self.kind, self.i, self.tier, self.force)

    def pose(self, sp):
        j = make_pose(sp, self.state, self.u, self.t, self.force)
        if self.extra:
            self.extra(j)
        return j


def draw_actor(img, cam, a):
    s = scale_at(cam, a.d)
    gx, gy = cam.p(a.x, a.d)
    sp = a.sp()
    j = a.pose(sp)
    if a.clip or a.dark:
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        C.draw(lay, _cam2(), gx, gy - FEET * s, s, sp, j, a.yaw, a.kind if a.kind != 'marcher' else None)
        if a.dark:
            lay = _darken(lay, a.dark)
        if a.clip:
            m = Image.new('L', img.size, 0)
            ImageDraw.Draw(m).rectangle(a.clip, fill=255)
            al = np.minimum(np.asarray(lay.getchannel('A')), np.asarray(m))
            lay.putalpha(Image.fromarray(al))
        img.alpha_composite(lay)
    else:
        C.draw(img, _cam2(), gx, gy - FEET * s, s, sp, j, a.yaw, a.kind if a.kind != 'marcher' else None)
    return j


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
        if running:
            out.append(Actor(f'hauler{k + 1}', 'rioter', x, d, 90, 'run', t=tt, tier='t2'))
        elif tt < 1.3:
            out.append(Actor(f'hauler{k + 1}', 'rioter', x, de, 180, 'haul', tier='t2'))
        else:
            u = ease((tt - 1.3) / 0.4)
            out.append(Actor(f'hauler{k + 1}', 'rioter', xe + 0.3 * u, de + 1.6 * u, 180,
                             'throw' if u >= 1 else 'stand', u=(tt * 1.7 + k * .5) % 1, tier='t2',
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
        out.append(Actor(f'crowd{k + 1}', 'marcher', x + 0.04 * math.sin(tt * 3 + k), d, 180, st, i=i, tier='t2'))
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
    # the impact flash where the sign meets the glass (1.0)
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


def t3_actors(lt):
    out = []
    jet = lt > 2.6 + J3
    for k, x in enumerate(np.arange(-2.0, 0.15, 0.7)):      # the black-clad front line, facing the police (right);
        # chat 14: 0.7 m apart (at 0.55 each throwing hand passed into the next one's back)
        dx, _ = field('t3', x, 11.8, lt, k)
        if jet and lt > 2.7 + J3 + 0.05 * k:                  # broken by the jet: running out left
            u = lt - 2.7 - J3 - 0.05 * k                          # chat 18: lane step eased (it snapped 0.9 m)
            out.append(Actor(f'front{k + 1}', 'rioter', x + dx * .3 - 4.5 * u, 11.8 - (.3 * k % 1) * ease(min(1.0, u / .35)), -90, 'run', t=lt,
                             tier='t3'))
        elif 0.75 <= lt < 2.6 + J3:
            u = ((lt - 0.75) * 1.6 + k * 0.37) % 1.0
            out.append(Actor(f'front{k + 1}', 'rioter', x + dx * .3, 11.8, 90, 'throw', u=u, tier='t3'))
        else:
            out.append(Actor(f'front{k + 1}', 'rioter', x + dx * .3, 11.8, 90, 'stand', tier='t3'))
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
    for (sx, sy, sd) in (R3(110, 860) + (1,), R3(760, 1010) + (2,)):
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
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * 0.88 * a)))
        img.alpha_composite(lay)
    # the water cannon jet (2.5-4.0): a white tapering stream from the roof cannon, sweeping the front line
    if lt >= 2.55 + J3:
        nx, ny = nozzle(lt)
        sweep = ease((lt - 2.55 - J3) / 1.3)
        ix, iy = cam.p(lerp(1.4, -2.0, sweep) - 1.5 * ease((lt - 5.5) / 1.0), 11.6, 1.3)
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


def t4_actors(lt):
    out = []
    push = ease((lt - 2.0) / 1.0)
    for k in range(8):                                     # the shield line, facing left; buckles 1.6, breaks 2.0
        x = 1.2 + k * 0.55 + push * (1.2 + 0.3 * (k % 3))
        d = 17.5 + (0.6 * push if k % 2 else -0.4 * push)
        state = 'line' if lt < 1.6 else 'pushed' if (k % 3 != 1 or lt < 2.0) else 'baton_up'
        out.append(Actor(f'policia{k + 1}', 'officer', x, d, -55, state, force='policia', tier='t4'))  # chat 14:
        # turned toward us a little so the shields show their faces (side on they read as thin lines)
    for k in range(6):                                     # the rioters at the front: surge, slam, swarm through
        x0 = -2.0 + k * 0.62                                 # chat 14: 0.62 apart, three ranks (was 0.45: arms in backs)
        dx = 1.6 * ease((lt - 0.9) / 1.0) + 1.4 * push
        state = 'run' if 0.9 < lt < 1.9 else 'throw'
        u = ((lt * 1.8) + k * .29) % 1.0
        out.append(Actor(f'rioter{k + 1}', 'rioter', x0 + dx, 16.9 + 0.65 * (k % 3), 90, state, u=u, t=lt + .35,
                         tier='t4'))   # chat 18: +.35 starts the run on the step nearest the throw stance (feet snapped 68 cm)
    return out


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
        gx, gy = cam.p(x, d)
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
    if 0.98 <= lt < 1.3:                                   # the hit: a flash and a burst at the helicopter
        a = (lt - 0.98) / 0.32
        hx, hy = R4(S.HELI_HOME[0], S.HELI_HOME[1])
        S.glow_disc(img, hx, hy, 180 * (0.5 + a), (255, 230, 160), amt=.55 * (1 - a))
        S.flames(img, hx, hy + 46, 160 * (0.6 + a), 138 * (0.6 + a), lt, seed=91, n=6)
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
    # two Molotovs from the crowd into the bank's ground-floor windows (2.2-2.7), the glass blooming orange
    for k, (t0, sx, sy, ex, ey) in enumerate(((2.0, 330, 1050, 90, 860), (2.12, 380, 1070, 175, 880))):  # chat 16
        a = (lt - t0) / 0.45
        (sx, sy), (ex, ey) = R4(sx, sy), R4(ex, ey)
        if 0 <= a < 1:
            x, y = lerp(sx, ex, a), lerp(sy, ey, a) - 160 * math.sin(math.pi * a)
            ang = a * 8
            IS.poly(img, [(x + 24 * math.cos(ang), y + 24 * math.sin(ang)), (x - 24 * math.cos(ang), y - 24 * math.sin(ang))],
                    None, INK, 15, 0)
            IS.poly(img, [(x + 24 * math.cos(ang), y + 24 * math.sin(ang)), (x - 24 * math.cos(ang), y - 24 * math.sin(ang))],
                    None, (70, 140, 70), 10, 0)
            S.glow_disc(img, x + 24 * math.cos(ang), y + 24 * math.sin(ang), 30, (255, 190, 80), amt=.8)
        elif a >= 1:
            g = min(1.0, (a - 1) * 2)
            S.glow_disc(img, ex, ey, 90 + 50 * g, (255, 160, 60), amt=.55)
            S.flames(img, ex, ey + 30, 90 + 40 * g, 80 + 70 * g, lt + k, seed=93 + k, n=5)
    # melee dust and shield-impact flashes (1.6-3.0); ground fog and flares through
    if 1.5 < lt < 3.4:
        cam = T4CAM
        rng = np.random.default_rng(int(lt * 12))
        dl = Image.new('RGBA', img.size, (0, 0, 0, 0))     # chat 16 (hunt 2 read them as boulders): wide, low, soft
        for _ in range(5):
            x = rng.uniform(0.5, 4.0) + 1.2 * ease((lt - 2.0) / 1.0)
            sx, sy = cam.p(x, 17.6, 0.5)
            r = rng.uniform(40, 70)
            S.smoke(dl, [(sx - r * .6, sy, r * .7), (sx + r * .6, sy + 4, r * .6), (sx, sy - r * .3, r * .8)],
                    (176, 146, 120), (206, 178, 150), line=None, lw=1)
        dl.putalpha(dl.getchannel('A').point(lambda v: int(v * 0.5)))
        img.alpha_composite(dl)
        if int(lt * 12) % 3 == 0 and lt < 2.4:
            sx, sy = cam.p(rng.uniform(1.0, 2.0), 17.4, 1.2)
            S.glow_disc(img, sx, sy, 40, (255, 250, 220), amt=.6)
    cam = T4CAM
    for fx, fd in ((-5.2, 24.0), (-7.4, 30.0)):            # two red flares held up in the crowd (chat 14: on sticks,
        bx, by = cam.p(fx, fd, 1.9)                         # in the crowd, not red balls over the mopeds)
        tx, ty = cam.p(fx + 0.05, fd, 2.5)
        IS.poly(img, [(bx, by), (tx, ty)], None, (40, 30, 30), 4, 0)
        S.glow_disc(img, tx, ty, 34 + 5 * math.sin(lt * 20 + fd), (255, 70, 50), amt=.4)
        IS.ell(img, tx, ty, 5, 5, (255, 236, 220), None)


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


def end_actors(tier, lt):
    return []


def end_picture(tier, lt):
    """Placeholder until the end scene is built (build order step 4): T4's last frame."""
    return picture(at('t4', 9.9))


END_CAM = {e: T4CAM for e in END}      # replaced as each end shot is built
# ================================================================================================= picture
def picture(t):
    """The frame WITHOUT the headlines (overlay puts those on last)."""
    _cam2()
    tier, lt = scene_of(t)
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
            draw_actor(back, cam, a)
            if a.name == 'runner5':                         # the A-board goes in among the street's depths
                pass
        t2_fx(back, lt)
        phone_lights(back, acts, cam)
        blue_wash(back, lt)
    elif tier == 't3':
        back, front = S.t3(lt)
        back = reframe3(back)
        front = reframe3(front) if front is not None else None
        cam = T3CAM
        t3_crowd(back, lt)
        t3_columns(back, lt)                                # chat 15: smoke, then the truck, then its bikes, sharp
        S.truck(back, cam, truck_x(lt), T3_TRUCK_D, lt, 'drive', 'fr', 12, float(int(lt * 6) % 2))
        S._bikes(back, cam, 2.1, 14, lt)
        t3_debris(back)
        for a in sorted(t3_actors(lt), key=lambda a: -a.d):
            draw_actor(back, cam, a)
        t3_fx(back, lt)
    else:
        h = heli_state(lt)
        h['under'] = lambda img: t4_under(img, lt)
        back, front = S.t4(lt, heli=h)
        back = RF4.image(back)
        front = RF4.image(front) if front is not None else None
        cam = T4CAM
        ppl = Image.new('RGBA', back.size, (0, 0, 0, 0))
        t4_crowd(ppl, lt)
        for a in sorted(t4_actors(lt), key=lambda a: -a.d):
            draw_actor(ppl, cam, a)
        t4_mopeds(ppl, lt)
        back.alpha_composite(backlight(back, lt, ppl))
        t4_fx(back, lt)
        if lt > 2.0:
            haze(back, lt - 2.0, [(R4(x, 1230), 220) for x in (100, 400, 700, 1000)], 0.3, (200, 170, 150), .1, 7)
        if lt > 3.0:                                        # chat 16 (hunt 2: no tear gas at the end): white gas at the line
            g = ease((lt - 3.0) / 0.6)
            gl = Image.new('RGBA', back.size, (0, 0, 0, 0))
            S.smoke(gl, [(cam.p(x, 17.0, 0.6)[0] + dx, cam.p(x, 17.0, 0.6)[1], 50 + 60 * g) for x in (2.6, 4.2, 5.6)
                         for dx in (-40, 40)], (226, 228, 226), (250, 250, 248), line=None, lw=1)
            gl.putalpha(gl.getchannel('A').point(lambda v: int(v * 0.6)))
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
        out.append(audit.Thing(a.name, audit.placed(a.name, j, a.x, a.d, facing(a.yaw), sp.get('height', 1.75), sp=sp)))
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
    if tier not in HEADLINES:                              # the end scene has no headings (round 1 plan)
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
    return mix


# Rule S7: each tier's effects drawn alone on a clear frame at the moment they peak, shape-tested (viewchecks)
def _fx_at(fn, lt):
    return lambda img: fn(img, lt)


EFFECTS = [('T1 firework string', 'trail', _fx_at(t1_fx, 1.2)), ('T1 three bursts', 'burst', _fx_at(t1_fx, 1.95)),
           ('T1 tear-gas haze', 'smoke', _fx_at(t1_fx, 3.6)), ('T2 sign-on-glass flash', 'flash', _fx_at(t2_fx, 1.05)),
           ('T3 stones and gas', 'sparks', _fx_at(t3_fx, 1.6)), ('T3 gas and jet', 'smoke', _fx_at(t3_fx, 3.0)),
           ('T4 rocket trail', 'trail', _fx_at(t4_fx, 0.9)), ('T4 helicopter hit', 'burst', _fx_at(t4_fx, 1.1)),
           ('T4 Molotovs and melee dust', 'burst', _fx_at(t4_fx, 2.6)), ('T4 fireball', 'burst', _fx_at(t4_fx, 3.5))]


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
           # the stone throws: a throwing hand really reaches ~20 m/s (clipcheck caps it at 12, the forearm at 10)
           + [(f'{w}{k}.{part}{sd}', t0, t1) for w, ks, t0, t1 in (
               ('runner', range(1, 6), at('t2', 0.6), at('t2', T2_FREEZE + 0.05)),
               ('hauler', (1, 2), at('t2', 1.2), at('t2', T2_FREEZE + 0.05)),
               ('front', range(1, 5), at('t3', 0.7), at('t3', 2.65 + J3)),
               ('rioter', range(1, 9), at('t4', 0.0), at('t4', 10.0)))
              for k in ks for part in ('hand', 'forearm') for sd in 'LR'])
TOUCHES = [('hauler*', 'runner*', at('t2', 0), at('t2', .85), 'T2 run-in: the raiders crush through one gap in the glass', 0.18),
           ('hauler*', 'hauler*', at('t2', 0), at('t2', .85), 'T2 run-in: the haulers drop the shutter and pile in', 0.12),
           ('runner*', 'runner*', at('t2', 0), at('t2', T2_FREEZE + .75), 'T2 run-in: the raiders crush through one gap; packed inside', 0.18),
           ('runner*', 'swinger', at('t2', 0), at('t2', .85), 'T2 run-in: the swinger is in the crush', 0.10),
           ('front*', 'front*', at('t3', 2.7 + J3), at('t3', 3.3 + J3), 'T3 run-out: the front line breaks and runs left as a pack', 0.04),
           ('policia*', 'rioter*', at('t4', 0), at('t4', 10), 'T4 melee: rioters slam into the shields (brief 26)', 0.20),
           ('policia*', 'policia*', at('t4', 2), at('t4', 10), 'T4 melee: the shield line buckles back into itself', 0.06)]
ORDER_SWAPS = [(a, b, t0, t1, w) for a, b, t0, t1, w in (
    ('hauler*', 'runner*', at('t2', 0), at('t2', .85), 'T2 run-in: they cross in the crush'),
    ('hauler*', 'hauler*', at('t2', 0), at('t2', .85), 'T2 run-in'), ('runner*', 'runner*', at('t2', 0), at('t2', .85), 'T2 run-in'),
    ('runner*', 'swinger', at('t2', 0), at('t2', .85), 'T2 run-in'), ('hauler*', 'swinger', at('t2', 0), at('t2', .85), 'T2 run-in'),
    ('front*', 'front*', at('t3', 2.7 + J3), at('t3', 3.3 + J3), 'T3 run-out'),
    ('crs*', 'front*', at('t3', 2.7 + J3), at('t3', 3.3 + J3), 'T3 run-out'),
    ('policia*', 'policia*', at('t4', 2.0), at('t4', 2.3), 'T4 melee: the line buckles'),
    ('policia*', 'rioter*', at('t4', 2.0), at('t4', 2.3), 'T4 melee: rioters break through the line'))]
ALLOWED = [(a, b, t0, t1) for a, b, t0, t1, *_ in TOUCHES]   # clipcheck reads the same meant contacts


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
