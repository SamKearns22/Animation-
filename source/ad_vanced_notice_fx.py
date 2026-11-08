#!/usr/bin/env python3
"""MAP  Ad-Vanced Notice (8 Nov): the showstopper. In the cliff shot, behind Vance, a missile from Iran drops on the
moving tanker: a white flash, a huge fireball swallowing the ship's middle, flaming pieces (deck plates, pipework,
the funnel top) thrown high and tumbling into the sea with a splash each, black smoke pouring up and leaning with the
wind, and the wreck left stopped and burning with the sea lit orange under it (the showstopper list in
notes/ad-vanced-notice.md, items 4b-12; the hull stays whole, rule 54).

Everything is laid out in metres in the strait's world (x right, y out to sea, z up; the near tanker 1.2 km out) and
drawn through whichever camera is given, so the close-up shows the same burning wreck and smoke. Flat house style:
flat tones, one ink outline, lumpy shapes (rule 15). The effects reuse Flying Whales' kit (flying_whales_fx: the
fireball lumps, smoke clumps, deck fire, splashes, flat-shape drawing), re-coloured for hazy daylight.

    python3 source/ad_vanced_notice_fx.py sheet OUT.jpg            key moments of the hit + the close-up's wreck
    python3 source/ad_vanced_notice_fx.py clip OUT.mp4 [--small]   the rehearsal clip (rule 40), silent

Map: timing 40 | the missile 70 | pieces 95 | smoke 150 | glow 185 | fx() 205 | flash, jolt 245 | frames 275 | main 330

Use in the film (u = seconds since the missile lands; the film sets its own T_HIT):
    near(u)        the near tanker for sets.strait(): ('sail', x) before the hit, ('wreck', X_HIT) after
    fx(u)          fn(img, cam) for sets.strait(..., fx=): every effect behind the cliff top (any camera)
    flash(img, u)  the white flash over the finished frame (people included)
    held(u)        the 2-frame freeze on the hit: use held(u) as the time for everything in the shot
    jolt(u)        the camera jolt (px): shift the finished frame with shift(img, dx, dy)
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ad_vanced_notice_sets as S        # noqa: E402
import flying_whales_fx as FX            # noqa: E402

FPS = 12                                 # the satire films' rate (satire_template)
F = 1.0 / FPS

# ---------------------------------------------------------------------------------------------- timing (s from the hit)
MISSILE_T = 0.4                          # it drops in about 0.4 s
FLASH_FULL = 3 * F                       # the whole frame white for 3 frames
FLASH_FADE = 0.3                         # then fades over 0.3 s
FREEZE_AT, FREEZE = FLASH_FULL, 2 * F    # the 2-frame hold on the first frame the fireball shows
FIREBALL_T = 1.5                         # swells and climbs, burns down to fire in about 1.5 s
HIT = np.array([S.X_HIT, S.NEAR_Y, 8.0])  # amidships, on deck
FB_SIZE = 150.0                          # the fireball's lump size (m): about 600 m tall, swallowing the middle
FB_SEED = 11
GP = 260.0                               # the flying pieces' gravity (m/s2): a cartoon cheat so a 150 m throw
                                         # lands in about 3 s (true gravity at 1.2 km looks like slow motion)
WIND = np.array([14.0, 0.0, 0.0])         # the smoke leans right
DAY_WATER = ((246, 250, 250), (196, 214, 218))
SMOKE = ((96, 90, 92), (44, 40, 44))     # lit (up and left: the high sun behind us to the left), shadow
FX.PUFF_COLS['oil'] = SMOKE


def held(u):
    """The time everything in the shot shows: the clock stops for 2 frames on the first fireball frame."""
    if u <= FREEZE_AT:
        return u
    return u - min(u - FREEZE_AT, FREEZE)


def near(u):
    if u < 0:
        return ('sail', S.near_x(u, 0.0))
    return ('wreck', S.X_HIT)


# ---------------------------------------------------------------------------------------------- the missile
M_FROM = np.array([470.0, -70.0])        # screen: in from the top left, steep (clear of Vance's head, x 270-450)


def missile_poly(u, cam):
    """The missile as a small black dart, no smoke trail (list 4b): screen polygon, or None when not in flight."""
    if not (-MISSILE_T <= u < 0):
        return None
    hx, hy = cam.screen(HIT)[0]
    k = ((u + MISSILE_T) / MISSILE_T) ** 1.5                    # speeding up as it falls
    p = M_FROM + (np.array([hx, hy - 6]) - M_FROM) * k
    d = np.array([hx, hy]) - M_FROM
    d /= np.linalg.norm(d)
    n = np.array([-d[1], d[0]])
    L, w = 56.0, 6.0
    nose, tail = p, p - d * L
    fin = tail + d * 7
    pts = [nose, p - d * 9 + n * w, fin + n * w, tail + n * 14, tail + n * 4, tail - n * 4, tail - n * 14, fin - n * w,
           p - d * 9 - n * w]
    return [tuple(q) for q in pts]


# ---------------------------------------------------------------------------------------------- flying pieces
L = S.NEAR_L
FUNNEL_TOP = np.array([S.X_HIT - L / 2 + 8.5, S.NEAR_Y, 7.5 + 24.0])   # where the funnel top sat (wreck state cuts it)


def _pieces():
    """Each piece: (kind, start, velocity m/s, size m, spin rad/s, seed, delay s). Deck plates and pipework from the
    hole amidships, thrown high and wide both ways (more to the right, away from Vance); the funnel top a beat later
    as the blast reaches the stern, up and back."""
    rng = np.random.default_rng(23)
    out = []
    for i in range(13):
        kind = 'plate' if i % 3 else 'pipe'
        side = 1 if i % 4 else -1
        vx = side * rng.uniform(40, 150)
        vz = rng.uniform(290, 440)
        vy = rng.uniform(-35, 35)
        size = rng.uniform(18, 30) if kind == 'plate' else rng.uniform(12, 18)
        start = HIT + np.array([rng.uniform(-15, 15), rng.uniform(-6, 6), 4.0])
        out.append((kind, start, np.array([vx, vy, vz]), size, rng.uniform(-7, 7), 100 + i, rng.uniform(0.0, 0.12)))
    out.append(('funnel', FUNNEL_TOP, np.array([-60.0, -10.0, 400.0]), 24.0, -4.5, 300, 0.15))
    return out


PIECES = _pieces()


def piece_at(pc, u):
    """(position, velocity) at u, or None before it flies; after it meets the sea: ('sea', where, when)."""
    kind, p0, v0, size, spin, seed, delay = pc
    a = u - delay
    if a < 0:
        return None
    vz, z0 = v0[2], p0[2]
    t_sea = (vz + math.sqrt(vz * vz + 2 * GP * z0)) / GP
    if a >= t_sea:
        return ('sea', p0 + v0 * t_sea + np.array([0, 0, -0.5 * GP * t_sea ** 2]), delay + t_sea)
    return (p0 + v0 * a + np.array([0, 0, -0.5 * GP * a * a]), v0 + np.array([0, 0, -GP * a]))


def _piece_shape(kind, x, y, r, ang, seed):
    """A piece on screen: an uneven plate (4-6 sides), a stubby length of pipe, or the funnel top (a short drum with
    its black rim): never a stick or a line (rule 15)."""
    ca, sa = math.cos(ang), math.sin(ang)
    rot = lambda pts: [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts]
    if kind == 'funnel':
        w, h = r, r * 0.62
        body = rot([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2 + 0.06 * w, h / 2), (-w / 2 - 0.04 * w, h / 2)])
        rim = rot([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, -h / 4), (-w / 2, -h / 4)])
        return body, rim
    if kind == 'pipe':
        w, h = r, r * 0.42
        return rot([(-w / 2, -h / 2), (w / 2, -h / 2 + 0.05 * h), (w / 2 + 0.08 * w, h / 2), (-w / 2, h / 2)]), None
    rng = np.random.default_rng(seed)
    nv = int(rng.integers(4, 7))
    rad = rng.uniform(0.6, 1.0, nv)
    a = np.linspace(0, 2 * math.pi, nv, endpoint=False) + rng.uniform(-0.3, 0.3, nv)
    return rot([(r * q * math.cos(t), r * q * 0.62 * math.sin(t)) for q, t in zip(rad, a)]), None


PIECE_COLS = {'plate': ((58, 50, 50), (150, 40, 34)), 'pipe': ((150, 144, 132), (90, 84, 78)),
              'funnel': ((232, 228, 220), (30, 30, 32))}


def pieces_items(cam, u):
    """Flying pieces with their trailing flames: [(poly, colour, inner, inner colour)] far to near, and the splashes
    [(where, size, age, seed)] of the ones that have met the sea."""
    live, splashes = [], []
    for pc in PIECES:
        kind, p0, v0, size, spin, seed, delay = pc
        st = piece_at(pc, u)
        if st is None:
            continue
        if isinstance(st[0], str):
            splashes.append((st[1], size, u - st[2], seed))
            continue
        p, v = st
        s, d = cam.screen(p)
        if d < 1.0:
            continue
        rp = max(3.0, cam.focal * size / d * 1.3)                 # drawn a touch large so they read at 1.2 km
        s2, _ = cam.screen(p - v * 0.16)          # where it was a moment ago: the flame streams there, and up (fire rises)
        fl = FX._teardrop(s[0], s[1], s2[0], s2[1] - rp * 1.2, rp * 0.7, seed)
        flame = (fl, FX.FIRE[1], FX._scaled(fl, 0.5, 0, 0), FX.FIRE[2])
        body, rim = _piece_shape(kind, s[0], s[1], rp, (u - delay) * spin + seed, seed)
        col, icol = PIECE_COLS[kind]
        live.append((d, [flame, (body, col, rim, icol)]))
    items = [it for _, its in sorted(live, key=lambda q: -q[0]) for it in its]
    return items, splashes


# ---------------------------------------------------------------------------------------------- smoke
class Smoke(FX.Puff):
    """A clump of oily smoke: as Flying Whales' Puff, with this film's wind (it leans right)."""
    __slots__ = ()

    def at(self, t):
        u = t - self.t0
        if u < 0 or u > self.life:
            return None
        g = (1 - math.exp(-self.k * u)) / self.k
        p = self.p0 + self.v0 * g + WIND * u * (1 + u * 0.08) + np.array([0, 0, self.rise * u])
        r = self.r0 + (self.r1 - self.r0) * (1 - math.exp(-u / self.tau))
        return p, r


def _smoke():
    """The first billow where the fireball burns down, then a column pouring from the hole for good (never fades:
    the clumps rise out of the top of the frame)."""
    rng = np.random.default_rng(5)
    out = []
    for i, (p, r) in enumerate(FX.fireball_lumps(HIT, FB_SIZE, 0.7, FB_SEED)):   # the fireball turning to smoke
        out.append(Smoke(1.05 + 0.05 * (i % 6), p, (0, 0, 30), 60.0, r * 0.8, r * 1.2, 40.0, 'oil', 700 + i,
                         tau=1.4, k=1.5))
    t = 1.0
    while t < 30.0:                                                              # the column, for the rest of the scene
        x = rng.uniform(-35, 35)
        out.append(Smoke(t, HIT + np.array([x, rng.uniform(-5, 5), 10.0]), (x * 0.6, 0, 60.0), 75.0,
                         rng.uniform(22, 32), rng.uniform(70, 110), 40.0, 'oil', 1000 + int(t * 100), tau=1.3, k=1.6))
        t += rng.uniform(0.06, 0.11)
    return out


SMOKE_PUFFS = _smoke()


# ---------------------------------------------------------------------------------------------- the sea lit orange
GLOW = (236, 140, 70)


def glow_items(cam, u, strength):
    """The fire's light on the sea (list 11): broken flat streaks of orange under the burning ship, brightest nearest
    the fire, wobbling with it; strength 0-1 sets how far they spread. Bright dashes on the blue, never a solid patch
    (a solid one reads as an oil slick)."""
    if strength <= 0:
        return []
    rng = np.random.default_rng(int(u * 6) + 3)
    out = []
    rows = 12
    for i in range(rows):
        y = S.NEAR_Y - 8 - i * 55.0 * strength
        half = 140.0 * strength * (1 - i / (rows + 3))
        x = S.X_HIT + rng.uniform(-15, 15)
        col = S.mix((255, 214, 120), (236, 120, 56), i / rows)
        for j in range(int(rng.integers(2, 4))):                 # each row broken into a few dashes
            c = x + rng.uniform(-half, half) * 0.8
            w = half * rng.uniform(0.2, 0.42)
            P, d = cam.screen(np.array([(c - w, y, 0), (c + w, y, 0)]))
            if (d < 1).any():
                continue
            (x0, y0), (x1, y1) = P
            th = 1.6 + 1.6 * (1 - i / rows)
            out.append(([(x0, y0), (x0 + th * 2, y0 - th), (x1 - th * 2, y1 - th), (x1, y1), (x1 - th * 2, y1 + th),
                         (x0 + th * 2, y0 + th)], col))
    return out


# ---------------------------------------------------------------------------------------------- fx(u)
def _fireball(cam, u):
    """The fireball (list 6), stretched to burn down over FIREBALL_T: dark red edge, orange, a yellow core that goes
    first. Daylight colours (no dusk tint)."""
    age = u / FIREBALL_T
    lumps = FX.fireball_lumps(HIT, FB_SIZE, age, FB_SEED)
    if not lumps:
        return None
    blobs = []
    for i, (p, r) in enumerate(lumps):
        s, d = cam.screen(p)
        if d < 1.0 or r <= 0:
            continue
        blobs.append(FX._blob(s[0], s[1], cam.focal * r / d, FB_SEED * 31 + i, n=9))
    if not blobs:
        return None
    ko = max(0.0, 0.8 - 0.5 * age)
    ky = max(0.0, 0.82 * (1 - age / 0.45))
    tall = max(y for b in blobs for _, y in b) - min(y for b in blobs for _, y in b)
    tones = [((176, 50, 38), blobs), (FX.FIRE[1], [FX._scaled(b, ko, 0, tall * 0.06) for b in blobs])]
    if ky > 0.3:
        mid = np.mean([np.mean(b, 0) for b in blobs], 0)
        core = sorted(blobs, key=lambda b: np.linalg.norm(np.mean(b, 0) - mid))[:6]
        tones.append((FX.FIRE[2], [FX._scaled(b, ky, 0, tall * 0.1) for b in core]))
    return FX.shape_sprite(tones, 0.0, ol=5.0)


def fx(u):
    """Every effect at u, drawn between the ships and the cliff top, through any camera: the sea's glow, the smoke,
    the wreck's fires, the fireball, the flying pieces, the splashes, the missile."""
    def draw(img, cam):
        if u < -MISSILE_T:
            return
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        if u >= 0:
            fire_k = 1.0 if u < FIREBALL_T else 0.55 + 0.08 * math.sin(u * 9)
            for poly, col in glow_items(cam, u, fire_k):
                d.polygon(poly, fill=col + (255,))
        sprites = [_fireball(cam, u) if u >= 0 else None,      # it burns down inside the smoke
                   FX.puffs_sprite(cam, SMOKE_PUFFS, u, 0.0, ol=4.0)]
        if u >= 0.35:                                            # the wreck burning in the hole and on the funnel stub
            grow = min(1.0, (u - 0.35) / 0.8)
            for k, (dx, half, tall, n, seed) in enumerate(((-14, 20.0, 40.0, 3, 3), (12, 16.0, 62.0, 2, 4),
                                                          (30, 9.0, 28.0, 2, 5))):   # uneven tongues, never a row
                sprites.append(FX.fire_sprite(cam, HIT + np.array([dx, -4.0 - k, -1.0]), (1, 0, 0), half,
                                              tall * grow, u, seed, 0.0, n=n))
            sprites.append(FX.fire_sprite(cam, FUNNEL_TOP + np.array([0, -1.0, -3.0]), (1, 0, 0), 5.0, 9.0 * grow, u,
                                          8, 0.0, n=2))
        if u >= 0:
            items, splashes = pieces_items(cam, u)
            sprites.append(FX.pieces_sprite(items, 0.0, ol=3.0))
            lumps = []
            for at, size, age, seed in splashes:
                lumps += FX.splash_parts(at, size * 1.3, age, seed, high=2.2)
            if lumps:
                sprites.append(FX.lumps_sprite(cam, lumps, 0.0, ol=3.0, cols=DAY_WATER))
        mp = missile_poly(u, cam)
        if mp:
            d.polygon(mp, fill=(22, 22, 26, 255), outline=S.INK + (255,))
        img.alpha_composite(lay)
        for spr in sprites:
            if spr is not None:
                spr.paste(img)
    return draw


# ---------------------------------------------------------------------------------------------- flash, jolt
def flash(img, u):
    """The whole frame white for 3 frames, then fading over 0.3 s (list 5)."""
    if u < 0 or u >= FLASH_FULL + FLASH_FADE:
        return img
    k = 1.0 if u < FLASH_FULL else 1.0 - (u - FLASH_FULL) / FLASH_FADE
    white = Image.new('RGBA', img.size, (255, 252, 240, 255))
    return Image.blend(img.convert('RGBA'), white, k)


def jolt(u):
    """The camera jolt on the hit (list 12): sharp, dying away in about half a second."""
    a = u - FREEZE_AT
    if a < 0 or a > 0.6:
        return 0.0, 0.0
    k = 16.0 * math.exp(-a * 6.5)
    f = int(round(a * FPS))
    return k * (1 if f % 2 else -1), k * 0.6 * (1 if f % 3 else -1)


def shift(img, dx, dy):
    """The finished frame moved by (dx, dy) px, the uncovered edge filled from the nearest row or column."""
    dx, dy = int(round(dx)), int(round(dy))
    if not dx and not dy:
        return img
    a = np.roll(np.asarray(img), (dy, dx), axis=(0, 1)).copy()
    if dy > 0:
        a[:dy] = a[dy]
    elif dy < 0:
        a[dy:] = a[dy - 1]
    if dx > 0:
        a[:, :dx] = a[:, dx:dx + 1]
    elif dx < 0:
        a[:, dx:] = a[:, dx - 1:dx]
    return Image.fromarray(a, img.mode)


# ---------------------------------------------------------------------------------------------- frames
def wide_frame(u, t0=6.0):
    """The cliff shot at u s from the hit: Vance at his mark, calm, never looking round (the film adds his acting)."""
    v = held(u)
    CP = S._cast()
    import ad_vanced_notice_cast as AC
    im = S.strait('wide', t0 + v, near(v), fx(v))
    x, y, ppm = S.place_cliff(*S.VANCE_MARK)
    S.cliff_shadow(im, x, y, ppm)
    CP.person(im, AC.VANCE, x, y, ppm, 0, mood='sincere', mouth='rest')
    im = flash(im, u)
    return shift(im, *jolt(u))


def close_frame(u, t0=6.0):
    """The close-up's wreck, smoke and glow (list 10, brief 18): the same world through the close camera."""
    CP = S._cast()
    import ad_vanced_notice_cast as AC
    im = S.strait('close', t0 + u, near(u), fx(u))
    CP.person(im, AC.VANCE, 430, 1920 + 1500, 1500, 0, mood='sincere', mouth='rest')
    return im


EFFECTS = [  # rule 15: each effect alone, shape-tested (viewchecks.shape_faults)
    ('fireball', 'burst', lambda img: _fireball(S.CLIFF, 0.25).paste(img)),
    ('smoke column', 'smoke', lambda img: FX.puffs_sprite(S.CLIFF, SMOKE_PUFFS, 3.0, 0.0).paste(img)),
    ('flying pieces', 'chunks', lambda img: FX.pieces_sprite(pieces_items(S.CLIFF, 0.8)[0], 0.0, ol=3.0).paste(img)),
]


def sheet(out):
    import sheet as SH
    shots = [(-0.2, 'missile'), (0.1, 'flash'), (0.45, 'fireball'), (0.9, 'pieces fly'), (1.6, 'splashes, smoke'),
             (4.0, 'wreck burning')]
    frames = [(wide_frame(u), f'{lbl} ({u:+.1f} s)') for u, lbl in shots]
    frames.append((close_frame(6.0), 'close-up (+6 s)'))
    _plain_sheet(frames, out)


def _plain_sheet(frames, out, cols=4, w=270):
    h = int(w * 1920 / 1080)
    rows = (len(frames) + cols - 1) // cols
    sh = Image.new('RGB', (cols * w, rows * (h + 26)), (250, 250, 250))
    d = ImageDraw.Draw(sh)
    for i, (im, lbl) in enumerate(frames):
        x, y = (i % cols) * w, (i // cols) * (h + 26)
        sh.paste(im.convert('RGB').resize((w, h), Image.LANCZOS), (x, y + 26))
        d.text((x + 6, y + 6), lbl, fill=(20, 20, 20))
    sh.save(out, quality=88)
    print(out)


def clip(out, small=False, u0=-1.4, u1=5.6):
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    n = int(round((u1 - u0) * FPS))
    size = (540, 960) if small else (1080, 1920)
    p = subprocess.Popen([ff, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s',
                          f'{size[0]}x{size[1]}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                          '-crf', '23' if small else '20', '-preset', 'slow', '-movflags', '+faststart', out],
                         stdin=subprocess.PIPE)
    for i in range(n):
        im = wide_frame(u0 + i * F).convert('RGB')
        if small:
            im = im.resize(size, Image.LANCZOS)
        p.stdin.write(im.tobytes())
    p.stdin.close()
    p.wait()
    print(f'{out}: {os.path.getsize(out) / 1e6:.1f} MB, {n / FPS:.1f} s')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'sheet':
        sheet(a[1])
    elif a and a[0] == 'clip':
        clip(a[1], '--small' in a)
    else:
        print(__doc__)
