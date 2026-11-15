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
TIER_LEN = 4.0
DUR = 16.0
BLACK_AT = DUR
TIERS = ('t1', 't2', 't3', 't4')
SHOTS = [(t, i * TIER_LEN, (i + 1) * TIER_LEN) for i, t in enumerate(TIERS)]
HOOK = ('European protests, ranked', {'y': 1300, 'until': 3.6})          # notes: Re-staged, T1 (over the near backs)
HEADLINES = {'t1': ('SPAIN', 'Barcelona, Passeig de Gràcia'), 't2': ('GERMANY', 'Frankfurt, Berliner Straße'),
             't3': ('FRANCE', 'Paris, Place de la République'), 't4': ('ALBANIA', 'Tirana, Ministry of Education')}
SHOT_CAST = {'t1': ['marchers', 'knot', 'police'], 't2': ['runners', 'crowd'], 't3': ['front line', 'police', 'crowd'],
             't4': ['mopeds', 'police', 'rioters', 'crowd']}
SIREN = os.path.join(HERE, 'audio', 'power-crime-siren.mp3')


def scene_of(t):
    i = min(3, int(t // TIER_LEN))
    return TIERS[i], t - i * TIER_LEN


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
        if t > 2.6 and d < 30:                             # the jet: the crowd breaks into two currents, out left
            u = t - 2.6 - 0.02 * max(0.0, x + 2)
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
    if a.state.startswith('run') and a.yaw < 0:     # running left: drawn facing right and mirrored (the rig's
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))  # left-facing sprint folds the elbow across the chest)
        C.draw(lay, _cam2(), W - gx, gy - FEET * s, s, sp, j, -a.yaw, a.kind if a.kind != 'marcher' else None)
        lay = lay.transpose(Image.FLIP_LEFT_RIGHT)
        if a.dark:
            lay = _darken(lay, a.dark)
        img.alpha_composite(lay)
    elif a.clip or a.dark:
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
T1_LINE_D = 185.0


@lru_cache(None)
def crowd_t1():
    """The march: thousands of backs from 46 m to 156 m (the long lens: the frame is 7-25 m wide down there)."""
    cam = S.CAMS['t1']
    rng = np.random.default_rng(11)
    out = []
    for d in np.arange(46.0, 156.0, 0.72):
        x0 = (0 - cam.VX - 40) * d / cam.F
        x1 = (W - cam.VX + 40) * d / cam.F
        for x in np.arange(x0, x1, 0.62):
            xx = x + rng.uniform(-.2, .2)
            r = rng.uniform()
            state = 'keys' if r < .42 else 'flag:catalan' if r < .47 else 'placard' if r < .52 else 'stand'
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
        d = T1_LINE_D - 2.5 * step
        gx, gy = cam.p(x, d)
        bob = 3 * math.sin(math.pi * min(1, max(0, (lt - 3.0) / 0.4)))
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
            if lt < 0.2 + (156 - m['d']) / 110 * 1.1:
                state = 'stand'
        elif state == 'placard':
            state = 'placard:' + T1_PLACARDS[m['i'] % len(T1_PLACARDS)]
        yaw = 180
        if lt > 1.55 + m['turn']:                          # heads turn to the bursts over the line (centre)
            yaw = 135 if gx < 470 else -135
        jig = -1 if (m['state'] == 'keys' and state == 'keys' and (int(lt * 12) + m['i']) % 2) else 0
        paste(img, 'marcher', m['i'], 't1', state, yaw, gx, gy + jig, scale_at(cam, d))


def t1_actors(lt):
    out = []
    knot = [(-2.6, 161.0), (-1.7, 162.5), (-1.0, 160.5), (3.0, 162.0), (3.7, 160.8)]
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
    # the firework string flying from the flicker's hand to over the line (0.85-1.5)
    if 0.85 <= lt < 1.55:
        u = (lt - 0.85) / 0.7
        x0, y0 = cam.p(-0.8, 160.5, 1.7)
        x1, y1 = cam.p(0.5, 186, 4.5)
        for k in range(4):
            uu = max(0.0, u - k * 0.06)
            x, y = lerp(x0, x1, uu), lerp(y0, y1, uu) - 60 * math.sin(math.pi * uu)
            S.glow_disc(img, x, y, 10, (255, 220, 140), amt=.45)
            IS.ell(img, x, y, 2.5, 2.5, (255, 250, 220), None)
    # three bursts over the line
    for k, (t0, x, z, col) in enumerate(((1.55, -2.0, 6.0, (255, 90, 80)), (1.95, 1.6, 7.2, (255, 255, 230)),
                                         (2.35, 4.2, 5.4, (120, 255, 160)))):
        a = lt - t0
        if 0 <= a < 0.45:
            cx, cy = cam.p(x, T1_LINE_D + 1, z)
            r = 14 + 70 * ease(a / 0.25)
            S.glow_disc(img, cx, cy, r * 1.4, col, amt=.35 * (1 - a / 0.45))
            dr = ImageDraw.Draw(img)
            for n in range(12):
                ang = n * math.pi / 6 + k
                r0, r1 = r * 0.35, r
                dr.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)),
                         (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang) + 8 * a)], fill=col, width=3)
            if a < 0.08:
                IS.ell(img, cx, cy, 10, 10, (255, 255, 255), None)
    # the tear-gas haze drifting left to right through the keys (3.0-4.0)
    if lt > 2.9:
        haze(img, lt - 2.9, [(cam.p(x, d, 1.6), 9 * cam.ppm(d)) for x, d in
                             ((-4, 150), (-1, 140), (2, 155), (5, 135), (-6, 128), (1, 120))], 0.9, (232, 232, 222))


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


def t2_state(lt):
    shutter = 0.5 + 0.5 * ease((lt - 0.45) / 0.55)
    glass = 'whole' if lt < 1.0 else 'starred' if lt < 1.1 else 'gone'
    return dict(shutter=shutter, glass=glass)


def t2_actors(lt):
    tt = min(lt, 3.2)                                       # 3.2: everyone freezes mid-swing in the blue
    out = []

    def run_in(x0, x1, t0, t1):
        u = (tt - t0) / (t1 - t0)
        return lerp(x0, x1, min(1.0, max(0.0, u))), u < 1.0

    # haulers (0.4-1.0), then they slide through the gap into the shop (1.3-1.7)
    for k, (xe, de) in enumerate(((-0.9, 13.3), (0.6, 13.3))):
        x, running = run_in(-4.6 - k * 0.5, xe, 0.0 + k * 0.08, 0.45)
        if running:
            out.append(Actor(f'hauler{k + 1}', 'rioter', x, 12.0 + k * .4, 90, 'run', t=tt, tier='t2'))
        elif tt < 1.3:
            out.append(Actor(f'hauler{k + 1}', 'rioter', x, de, 180, 'haul', tier='t2'))
        else:
            u = ease((tt - 1.3) / 0.4)
            out.append(Actor(f'hauler{k + 1}', 'rioter', xe + 0.3 * u, de + 1.6 * u, 180,
                             'throw' if u >= 1 else 'stand', u=(tt * 1.7 + k * .5) % 1, tier='t2',
                             clip=T2_WIN if u > 0.5 else None))
    # the road-sign swinger: runs in carrying it low, winds up 0.6, swings through the glass at 1.0, keeps swinging
    x, running = run_in(-5.2, -1.55, 0.05, 0.6)
    if running:
        out.append(Actor('swinger', 'rioter', x, 12.6, 90, 'run_sign', t=tt, tier='t2'))
    else:
        if tt < 0.9:
            u = 0.2 * ease((tt - 0.6) / 0.3)
        elif tt < 1.05:
            u = 0.2 + 0.8 * ease((tt - 0.9) / 0.15)
        else:
            c = ((tt - 1.05) % 0.7) / 0.7
            u = 1 - 0.8 * math.sin(math.pi * c) if tt < 3.0 else 0.55
        out.append(Actor('swinger', 'rioter', x, 12.6, 90, 'swing', u=u, tier='t2'))
    # five more: two throw stones into the shop, one kicks the A-board over (1.4), two by the closed shop
    for k, (xe, de) in enumerate(((0.9, 12.4), (-0.2, 12.1), (-2.6, 12.2), (2.2, 12.5), (2.8, 12.0))):
        x, running = run_in(-5.0 - k * .4, xe, 0.05 + k * 0.07, 0.6 + k * .05)
        if running:
            out.append(Actor(f'runner{k + 1}', 'rioter', x, de, 90, 'run', t=tt + k * .1, tier='t2'))
        else:
            u = ((tt - 0.6) * 1.4 + k * .3) % 1.0
            yaw = 180 if k < 2 else 90 if k == 2 else 135
            out.append(Actor(f'runner{k + 1}', 'rioter', x, de, yaw, 'throw', u=u if lt < 3.2 else 0.3, tier='t2'))
    # the crowd on the near pavement, seen from behind, all facing the store (chanting: signs jab on the beat)
    beat = abs(math.sin(math.pi * 2.2 * tt))
    crowd = [(-2.5, 5.6, 'placard:WAFFEN RAUS:250,246,232', 0), (2.6, 5.5, 'phone', 1), (-1.5, 5.7, 'stand', 2),
             (1.4, 5.6, 'stand', 3), (0.2, 5.8, 'stand', 4),
             (-1.3, 4.3, 'placard:GEN Z REGELT:240,220,60', 5), (1.35, 4.4, 'phone', 6), (0.1, 4.5, 'stand', 7),
             (-0.75, 3.35, 'stand', 8), (0.85, 3.4, 'phone', 9)]
    for k, (x, d, st, i) in enumerate(crowd):
        if st.startswith('placard'):
            st = st + ':' + str(int(90 * beat))
        out.append(Actor(f'crowd{k + 1}', 'marcher', x + 0.04 * math.sin(tt * 3 + k), d, 180, st, i=i, tier='t2'))
    return out


def t2_fx(img, lt):
    cam = S.CAMS['t2']
    tt = min(lt, 3.2)
    # the A-board by the doorway, kicked over at 1.4
    bx, by = cam.p(-3.4, 12.6)
    k = cam.ppm(12.6)
    ang = math.radians(85 * ease((tt - 1.4) / 0.25))
    hgt, wd = 0.9 * k, 0.6 * k
    pts = [(-wd / 2, 0), (wd / 2, 0), (wd / 2 - 6, -hgt), (-wd / 2 + 6, -hgt)]
    rot = [(bx + px * math.cos(ang) - py * math.sin(ang), by + px * math.sin(ang) + py * math.cos(ang)) for px, py in pts]
    IS.poly(img, rot, (240, 236, 220), INK, 2.4)
    # the impact flash where the sign meets the glass (1.0)
    if 0.98 <= tt < 1.15:
        S.glow_disc(img, 330, 905, 90, (255, 250, 210), amt=.6)
    # falling glass with glints (1.05-1.6), then shards on the pavement glinting
    rng = np.random.default_rng(5)
    for n in range(60):
        x0, y0 = rng.uniform(T2_WIN[0] + 10, T2_WIN[2] - 10), rng.uniform(T2_WIN[1] + 10, T2_WIN[3] - 20)
        a = tt - 1.05 - rng.uniform(0, .15)
        if a < 0:
            continue
        yy = min(1175.0 + rng.uniform(-20, 15), y0 + 900 * a * a)
        xx = x0 + rng.uniform(-60, 60) * min(a, .4)
        r = rng.uniform(5, 14)
        sp = rng.uniform(0, 6.28) + a * 9
        tri = [(xx + r * math.cos(sp + q * 2.1), yy + r * .7 * math.sin(sp + q * 2.1)) for q in range(3)]
        IS.poly(img, tri, (210, 230, 238), (120, 150, 160), 1.2, 0)
        if (n + int(lt * 12)) % 7 == 0:
            S.glow_disc(img, xx, yy, 9, (255, 255, 255), amt=.7)


def blue_wash(img, lt):
    """T2 3.0-4.0: the blue light from the far right end of the street sweeping across crowd and store; faces,
    signs and the wet ground turn blue (the last light layer, over everything)."""
    if lt < 3.0:
        return
    u = ease((lt - 3.0) / 0.35)
    a = np.asarray(img.convert('RGB'), np.float32)
    xs = np.arange(W, dtype=np.float32)[None, :]
    sweep = W - ((lt - 3.0) * 1600) % (W * 1.6)                # a bright band crossing right to left, again and again
    band = np.exp(-((xs - sweep) / 220.0) ** 2)
    strobe = 0.75 + 0.25 * (int(lt * 8) % 2)
    tint = np.array((0.42, 0.55, 1.05), np.float32)
    k = (0.65 * u * strobe + 0.35 * band * u)[..., None]
    out = a * (1 - k) + (a * tint + np.array((10, 30, 90), np.float32)) * k
    ys = np.arange(H, dtype=np.float32)[:, None]
    wet = ((ys > 1140) & (ys < 1300)).astype(np.float32) * band * u * 0.5
    out += wet[..., None] * np.array((40, 80, 200), np.float32)
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert('RGBA'), (0, 0))


def phone_lights(img, actors, cam):
    for a in actors:
        if a.state == 'phone':
            gx, gy = cam.p(a.x + 0.12, a.d, 1.62)
            S.glow_disc(img, gx, gy, 0.25 * cam.ppm(a.d), (230, 240, 255), amt=.35)


# ================================================================================================= T3
T3_TRUCK_D = S.TRUCK_D3


def truck_x(lt):
    return lerp(9.0, 2.8, ease((lt - 2.0) / 0.6))


def nozzle(lt, aim=12.0):
    cam = S.CAMS['t3']
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
    jet = lt > 2.6
    for k, x in enumerate(np.arange(-1.7, 1.05, 0.55)):     # the black-clad front line, facing the police (right)
        dx, _ = field('t3', x, 11.8, lt, k)
        if jet and lt > 2.7 + 0.05 * k:                       # broken by the jet: running out left
            u = lt - 2.7 - 0.05 * k
            out.append(Actor(f'front{k + 1}', 'rioter', x + dx * .3 - 4.5 * u, 11.8 - .3 * k % 1, -90, 'run', t=lt,
                             tier='t3'))
        elif 1.0 <= lt < 2.6:
            u = ((lt - 1.0) * 1.6 + k * 0.37) % 1.0
            out.append(Actor(f'front{k + 1}', 'rioter', x + dx * .3, 11.8, 90, 'throw', u=u, tier='t3'))
        else:
            out.append(Actor(f'front{k + 1}', 'rioter', x + dx * .3, 11.8, 90, 'stand', tier='t3'))
    for k, (x, d) in enumerate(((2.55, 11.0), (3.15, 11.0), (3.75, 11.0), (2.85, 12.0), (3.45, 12.0), (4.05, 12.0))):
        out.append(Actor(f'crs{k + 1}', 'officer', x, d, -90, 'line', force='crs', tier='t3'))
    return out


def t3_crowd(img, lt):
    cam = S.CAMS['t3']
    for m in sorted(crowd_t3(), key=lambda m: -m['d']):
        dx, dd = field('t3', m['x'], m['d'], lt, m['ph'])
        x, d = m['x'] + dx, max(12.6, m['d'] + dd)
        gx, gy = cam.p(x, d)
        if gx < -80 or gx > W + 80:
            continue
        running = lt > 2.6 and m['d'] < 30 and lt - 2.6 - 0.02 * max(0, m['x'] + 2) > 0.1
        yaw = -90 if running else 90
        paste(img, 'marcher', m['i'], 't3', m['state'] if not running else 'stand', yaw, gx, gy, scale_at(cam, d))


def t3_fx(img, lt):
    cam = S.CAMS['t3']
    # smoke climbing from the car (left) and the bike heap (mid-right) from 0.0
    for (sx, sy, sd) in ((110, 860, 1), (760, 1010, 2)):
        lumps = []
        for n in range(6):
            a = (lt * 0.9 + n / 6) % 1.0
            lumps.append((sx + 40 * a + 15 * math.sin(n * 2.1), sy - 520 * a, 40 + 90 * a))
        S.smoke(img, lumps, (58, 54, 56), (90, 84, 86), lw=2.5)
    # stones in arcs from the front line to the shields (1.0-2.6)
    for k in range(6):
        for rep in range(3):
            t0 = 1.0 + ((k * 0.37 + 0.6) % 1.0) / 1.6 + rep / 1.6
            a = (lt - t0) / 0.45
            if 0 <= a < 1 and t0 < 2.6:
                x0 = -1.7 + 0.55 * k
                x, z = lerp(x0 + 0.3, 2.7, a), 1.9 + 2.2 * math.sin(math.pi * a) - 0.6 * a
                d = lerp(11.8, 11.0, a)
                sx, sy = cam.p(x, d, z)
                IS.ell(img, sx, sy, 9, 7, (150, 146, 138), INK, 2)
    # the tear-gas canister lands at 1.6 among the front line; the white gas swells over Marianne's base 1.8-2.5+
    if 1.25 <= lt < 1.6:
        a = (lt - 1.25) / 0.35
        sx, sy = lerp(1100, 470, a), lerp(820, 1000, a) - 160 * math.sin(math.pi * a)
        IS.ell(img, sx, sy, 10, 6, (90, 96, 90), INK, 2)
    if lt >= 1.6:
        g = ease((lt - 1.6) / 1.0)
        lumps = [(480 + dx * g, 1010 - dy * g, (40 + r * g)) for dx, dy, r in
                 ((0, 0, 80), (-130, 40, 90), (140, 30, 90), (-60, 150, 110), (90, 170, 110), (0, 260, 120),
                  (-200, 120, 80), (220, 110, 80))]
        a = min(1.0, (lt - 1.6) / 0.3)
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        S.smoke(lay, lumps, (232, 234, 232), (250, 250, 248), line=(170, 176, 180), lw=2.5)
        if lt > 2.6:                                       # the jet blows it left
            lay = lay.transform(lay.size, Image.AFFINE, (1, 0, 160 * (lt - 2.6), 0, 1, 0))
        lay.putalpha(lay.getchannel('A').point(lambda v: int(v * 0.88 * a)))
        img.alpha_composite(lay)
    # the water cannon jet (2.5-4.0): a white tapering stream from the roof cannon, sweeping the front line
    if lt >= 2.55:
        nx, ny = nozzle(lt)
        sweep = ease((lt - 2.55) / 1.3)
        ix, iy = cam.p(lerp(1.4, -2.0, sweep), 11.6, 1.3)
        g = min(1.0, (lt - 2.55) / 0.12)
        ix, iy = lerp(nx, ix, g), lerp(ny, iy, g)
        mx, my = (nx + ix) / 2, min(ny, iy) - 70
        pts_top, pts_bot = [], []
        for n in range(13):
            u = n / 12
            x = (1 - u) ** 2 * nx + 2 * (1 - u) * u * mx + u * u * ix
            y = (1 - u) ** 2 * ny + 2 * (1 - u) * u * my + u * u * iy
            w = 6 + 24 * u
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
        return dict(x=x + 6 * math.sin(lt * 2), y=y + 4 * math.sin(lt * 3), s=S.HELI_HOME[2], turn=0, roll=-4, hit=False)
    u = min(1.0, (lt - 1.0) / 1.0)
    turn = (int(u * 14) * 45) % 360                          # three drawn turns and their mirrors, stepped in 45s
    return dict(x=x - 60 * u + 30 * math.sin(u * 9), y=y + 520 * u * u + 40 * u, s=S.HELI_HOME[2] * (1 - .2 * u),
                turn=turn, roll=-4 + 40 * u, hit=True)


MOPED_D = 10.5


def moped_pos(lt, k):
    x = lerp(-4.2 - k * 1.2, -0.9 - k * 1.6, ease(min(1.0, lt / 0.6)))
    return x, MOPED_D + 2.6 * k


@lru_cache(None)
def crowd_t4():
    rng = np.random.default_rng(41)
    out = []
    for d in np.arange(18.5, 48.0, 0.9):
        for x in np.arange(-14.0, 0.8, 0.7):
            r = rng.uniform()
            state = 'flag:albania' if r < .14 else 'stand'
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
        out.append(Actor(f'policia{k + 1}', 'officer', x, d, -90, state, force='policia', tier='t4'))
    for k in range(6):                                     # the rioters at the front: surge, slam, swarm through
        x0 = -1.6 + k * 0.45
        dx = 1.6 * ease((lt - 0.9) / 1.0) + 1.4 * push
        state = 'run' if 0.9 < lt < 1.9 else 'throw'
        u = ((lt * 1.8) + k * .29) % 1.0
        out.append(Actor(f'rioter{k + 1}', 'rioter', x0 + dx, 17.2 + 0.4 * (k % 3), 90, state, u=u, t=lt, tier='t4'))
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
    if lt >= 3.0:
        g = ease((lt - 3.0) / 0.7)
        cx, cy = 820, lerp(700, 420, g)
        S.glow_disc(img, cx, cy, 340 * g + 60, (255, 200, 120), amt=.35)
        S.smoke(img, [(cx + dx * g, cy + dy * g, r * (0.4 + 0.6 * g)) for dx, dy, r in
                      ((0, -80, 120), (-120, -40, 90), (120, -50, 100), (-60, -170, 90), (70, -180, 90))],
                (70, 40, 36), (110, 60, 46), lw=2.5)
        IS.poly(img, [(cx + 230 * g * math.cos(a), cy + 30 + 170 * g * math.sin(a)) for a in np.linspace(0, 6.28, 24)],
                S.FIRE_O, S.FIRE_L, 3, 4)
        IS.poly(img, [(cx + 140 * g * math.cos(a), cy + 40 + 100 * g * math.sin(a)) for a in np.linspace(0, 6.28, 20)],
                S.FIRE_Y, None, 0, 4)


def t4_crowd(img, lt):
    cam = S.CAMS['t4']
    for m in sorted(crowd_t4(), key=lambda m: -m['d']):
        dx, dd = field('t4', m['x'], m['d'], lt, m['ph'])
        x, d = m['x'] + dx, m['d'] + dd
        gx, gy = cam.p(x, d)
        if gx < -80 or gx > W + 80:
            continue
        paste(img, 'marcher', m['i'], 't4', m['state'], 90, gx, gy, scale_at(cam, d))


def t4_mopeds(img, lt):
    cam = S.CAMS['t4']
    for k in (1, 0):
        x, d = moped_pos(lt, k)
        gx, gy = cam.p(x, d)
        s = scale_at(cam, d)
        C.moped_scene(img, _cam2(), gx, gy - FEET * s, s, yaw=90, aim=38.0, fired=(k == 0 and lt >= 0.6), both=True)


def rpg_tip(lt):
    cam = S.CAMS['t4']
    x, d = moped_pos(lt, 0)
    return cam.p(x - 0.1, d, 2.05)


def t4_fx(img, lt):
    # the rocket: fired 0.6, climbs the frame's height to the helicopter, hits 1.0; its smoke trail hangs
    if lt >= 0.6:
        x0, y0 = rpg_tip(0.6)
        hx, hy = S.HELI_HOME[0], S.HELI_HOME[1]
        u = min(1.0, (lt - 0.6) / 0.4)
        n = int(18 * u) + 1
        lumps = []
        for k in range(n):
            v = k / 18
            age = lt - 0.6 - v * 0.4
            lumps.append((lerp(x0, hx, v) + 6 * math.sin(k), lerp(y0, hy, v) - 40 * math.sin(math.pi * v),
                          8 + 14 * min(age, 1.5)))
        S.smoke(img, lumps, (190, 176, 170), (226, 214, 206), lw=2)
        if u < 1:
            rx, ry = lerp(x0, hx, u), lerp(y0, hy, u) - 40 * math.sin(math.pi * u)
            S.glow_disc(img, rx, ry, 26, (255, 230, 150), amt=.6)
    if 0.98 <= lt < 1.3:                                   # the hit: a flash and a burst at the helicopter
        a = (lt - 0.98) / 0.32
        S.glow_disc(img, S.HELI_HOME[0], S.HELI_HOME[1], 160 * (0.5 + a), (255, 230, 160), amt=.55 * (1 - a))
        S.flames(img, S.HELI_HOME[0], S.HELI_HOME[1] + 40, 140 * (0.6 + a), 120 * (0.6 + a), lt, seed=91, n=6)
    # two Molotovs from the crowd into the bank's ground-floor windows (2.2-2.7), the glass blooming orange
    for k, (t0, sx, sy, ex, ey) in enumerate(((2.2, 330, 1050, 90, 860), (2.35, 380, 1070, 175, 880))):
        a = (lt - t0) / 0.45
        if 0 <= a < 1:
            x, y = lerp(sx, ex, a), lerp(sy, ey, a) - 140 * math.sin(math.pi * a)
            ang = a * 8
            IS.poly(img, [(x + 14 * math.cos(ang), y + 14 * math.sin(ang)), (x - 14 * math.cos(ang), y - 14 * math.sin(ang))],
                    None, (60, 110, 60), 7, 0)
            S.glow_disc(img, x + 14 * math.cos(ang), y + 14 * math.sin(ang), 14, (255, 190, 80), amt=.7)
        elif a >= 1:
            g = min(1.0, (a - 1) * 2)
            S.glow_disc(img, ex, ey, 70 + 40 * g, (255, 160, 60), amt=.45)
            S.flames(img, ex, ey + 30, 70 + 30 * g, 60 + 50 * g, lt + k, seed=93 + k, n=4)
    # melee dust and shield-impact flashes (1.6-3.0); ground fog and flares through
    if 1.5 < lt < 3.4:
        cam = S.CAMS['t4']
        rng = np.random.default_rng(int(lt * 12))
        for _ in range(4):
            x = rng.uniform(0.5, 4.0) + 1.2 * ease((lt - 2.0) / 1.0)
            sx, sy = cam.p(x, 17.6, 0.3)
            S.smoke(img, [(sx, sy, rng.uniform(20, 45))], (150, 120, 100), (180, 150, 126), lw=2)
        if int(lt * 12) % 3 == 0 and lt < 2.4:
            sx, sy = cam.p(rng.uniform(1.0, 2.0), 17.4, 1.2)
            S.glow_disc(img, sx, sy, 40, (255, 250, 220), amt=.6)
    for fx, fy in ((140, 1180), (60, 1230)):                # two red flares held up in the crowd
        S.glow_disc(img, fx, fy, 50 + 6 * math.sin(lt * 20), (255, 60, 50), amt=.45)
        IS.ell(img, fx, fy, 6, 6, (255, 220, 200), None)


def backlight(img, lt, ppl):
    """T4 3.0-4.0: the fireball behind the ministry backlights the melee into one silhouette (F5)."""
    if lt < 3.0:
        return ppl
    k = 0.75 * ease((lt - 3.0) / 0.5)
    a = np.asarray(ppl).astype(np.float32)
    a[..., :3] = a[..., :3] * (1 - k) + np.array((40, 18, 20), np.float32) * k
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


# ================================================================================================= picture
def picture(t):
    """The frame WITHOUT the headlines (overlay puts those on last)."""
    _cam2()
    tier, lt = scene_of(t)
    if tier == 't1':
        back, front = S.t1(lt)
        t1_people(back, lt)
        t1_fx(back, lt)
    elif tier == 't2':
        back, front = S.t2(lt, **t2_state(lt))
        cam = S.CAMS['t2']
        acts = sorted(t2_actors(lt), key=lambda a: -a.d)
        for a in acts:
            draw_actor(back, cam, a)
            if a.name == 'runner5':                         # the A-board goes in among the street's depths
                pass
        t2_fx(back, lt)
        phone_lights(back, acts, cam)
        blue_wash(back, lt)
    elif tier == 't3':
        back, front = S.t3(lt, truck=dict(x=truck_x(lt), aim=12, flash=float(int(lt * 6) % 2)))
        cam = S.CAMS['t3']
        t3_crowd(back, lt)
        for a in sorted(t3_actors(lt), key=lambda a: -a.d):
            draw_actor(back, cam, a)
        t3_fx(back, lt)
    else:
        h = heli_state(lt)
        h['under'] = lambda img: t4_under(img, lt)
        back, front = S.t4(lt, heli=h)
        cam = S.CAMS['t4']
        ppl = Image.new('RGBA', back.size, (0, 0, 0, 0))
        t4_crowd(ppl, lt)
        for a in sorted(t4_actors(lt), key=lambda a: -a.d):
            draw_actor(ppl, cam, a)
        t4_mopeds(ppl, lt)
        back.alpha_composite(backlight(back, lt, ppl))
        t4_fx(back, lt)
        if lt > 2.0:
            haze(back, lt - 2.0, [((x, 1150), 260) for x in (100, 400, 700, 1000)], 0.3, (200, 170, 150), .3, 7)
    if front is not None:
        back.alpha_composite(front)
    return back


def draw_order(t):
    tier, lt = scene_of(t)
    names = {'t1': lambda: ['painting', 'police'] + [a.name for a in t1_actors(lt)] + ['march', 'fx'],
             't2': lambda: ['painting'] + [a.name for a in sorted(t2_actors(lt), key=lambda a: -a.d)] + ['fx', 'blue'],
             't3': lambda: ['painting', 'truck', 'crowd'] + [a.name for a in sorted(t3_actors(lt), key=lambda a: -a.d)]
             + ['fx', 'car'],
             't4': lambda: ['painting', 'helicopter', 'ministry', 'crowd'] +
             [a.name for a in sorted(t4_actors(lt), key=lambda a: -a.d)] + ['mopeds', 'fx']}
    return names[tier]()


ACTORS = {'t1': t1_actors, 't2': t2_actors, 't3': t3_actors, 't4': t4_actors}


def cam_for(t):
    return S.CAMS[scene_of(t)[0]]


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


# ------------------------------------------------------------------------------------------------- overlay
def _font(n):
    return ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)


def overlay(img, t):
    """The headlines (brief 2): white, country on the cut, location 0.5 s later underneath, top-left."""
    tier, lt = scene_of(t)
    country, place = HEADLINES[tier]
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    k = img.width / W
    d.text((70 * k, 350 * k), country, font=_font(int(84 * k)), fill=(255, 255, 255), stroke_width=int(6 * k),
           stroke_fill=(0, 0, 0))
    if lt >= 0.5:
        d.text((72 * k, 452 * k), place, font=_font(int(44 * k)), fill=(255, 255, 255), stroke_width=int(4 * k),
               stroke_fill=(0, 0, 0))
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
    """Siren only (the brief names the siren cue, T2 3.0-4.0); no other effects."""
    import mossad_audio as MA
    n = int((DUR + 0.3) * MA.SR)
    mix = np.zeros(n)
    try:
        import filmkit
        s = MA.load(SIREN) if hasattr(MA, 'load') else None
        if s is not None:
            filmkit.place(mix, s[:int(1.2 * MA.SR)] * 0.6, at=7.0, sr=MA.SR)
    except Exception as e:                                  # the film still renders; the fault is printed
        print('SOUND: siren not placed:', e)
    return mix


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
